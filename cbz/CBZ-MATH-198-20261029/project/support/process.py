"""Unique bounded subprocess attempts with partial streams and wait4 receipts."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time


def _file_sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1048576), b''):
            digest.update(chunk)
    return digest.hexdigest()


def run_recorded(command, output, *, timeout=120, cwd=None, env=None,
                 max_output_bytes=16777216):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    command = list(map(str, command))
    wall, unix_ns = time.monotonic(), time.time_ns()
    process, usage, failure = None, None, None
    timed_out = overflow = False
    streams = [output/'stdout.txt', output/'stderr.txt']
    try:
        with streams[0].open('xb') as stdout, streams[1].open('xb') as stderr:
            process = subprocess.Popen(command, cwd=cwd, env=env, stdout=stdout,
                                       stderr=stderr, start_new_session=True)
            (output/'started.json').write_text(json.dumps({'command': command,
                'pid': process.pid, 'started_unix_ns': unix_ns}, indent=2)+'\n')
            while True:
                waited, status, usage = os.wait4(process.pid, os.WNOHANG)
                if waited:
                    process.returncode = os.waitstatus_to_exitcode(status)
                    # A short-lived child can overflow and exit between polls.
                    # Completion does not waive its output bound.
                    overflow = any(p.stat().st_size > max_output_bytes for p in streams)
                    timed_out = time.monotonic()-wall >= timeout
                    break
                timed_out = time.monotonic()-wall >= timeout
                overflow = any(p.stat().st_size > max_output_bytes for p in streams)
                if timed_out or overflow:
                    os.killpg(process.pid, signal.SIGKILL)
                    _, status, usage = os.wait4(process.pid, 0)
                    process.returncode = os.waitstatus_to_exitcode(status)
                    break
                time.sleep(0.05)
    except BaseException as exc:
        failure = {'type': type(exc).__name__, 'message': str(exc)}
        if process is not None and process.returncode is None:
            try: os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError: pass
            _, status, usage = os.wait4(process.pid, 0)
            process.returncode = os.waitstatus_to_exitcode(status)
    receipt = {'command': command, 'pid': process.pid if process else None,
               'started_unix_ns': unix_ns, 'returncode': process.returncode if process else None,
               'timed_out': timed_out, 'output_limit_exceeded': overflow,
               'succeeded': process is not None and process.returncode == 0 and not timed_out and not overflow and failure is None,
               'failure': failure, 'wall_seconds': time.monotonic()-wall,
               'wait4': ({'user_seconds': usage.ru_utime, 'system_seconds': usage.ru_stime,
                          'max_rss_kib': usage.ru_maxrss} if usage is not None else None),
               'streams': {p.name: {'bytes': p.stat().st_size,
                           'sha256': _file_sha256(p)}
                           for p in streams if p.is_file()},
               'cost_boundary': 'This child including startup and killed failures; wall and wait4 CPU are separate. Caller parent CPU/startup is outside this receipt.'}
    (output/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    if failure is not None:
        raise RuntimeError('Recorded child failure: '+failure['message'])
    return receipt
