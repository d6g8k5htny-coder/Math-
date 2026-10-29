"""Unique bounded subprocess attempts with owned-tree cleanup and wait4 receipts."""
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


def _file_sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1048576), b''):
            digest.update(chunk)
    return digest.hexdigest()


def validate_command(command, timeout, cwd, max_output_bytes):
    if type(command) not in (list, tuple) or not command or any(
            type(arg) is not str or '\0' in arg for arg in command) or not command[0]:
        raise ValueError('command must be a nonempty literal argv of non-NUL strings')
    if type(timeout) not in (int, float) or timeout <= 0 or (
            type(timeout) is float and not math.isfinite(timeout)):
        raise ValueError('timeout must be finite and positive, excluding bool')
    if type(max_output_bytes) is not int or max_output_bytes < 0:
        raise ValueError('max_output_bytes must be a nonnegative integer, excluding bool')
    if cwd is not None and not Path(cwd).is_dir():
        raise ValueError('cwd must be an existing directory')


def run_recorded(command, output, *, timeout=120, cwd=None, env=None,
                 max_output_bytes=16777216):
    validate_command(command, timeout, cwd, max_output_bytes)
    command = list(command)
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    wall, unix_ns = time.monotonic(), time.time_ns()
    process, usage, failure = None, None, None
    timed_out = overflow = False
    forced = False
    streams = [output/'stdout.txt', output/'stderr.txt']
    request = {'command': command, 'cwd': str(Path(cwd).resolve()) if cwd is not None else None,
               'output': str(output), 'parent_pid': os.getpid(), 'started_unix_ns': unix_ns,
               'cleanup_seconds': 2.0}
    request_path = output/'request.json'
    request_path.write_text(json.dumps(request, indent=2, allow_nan=False)+'\n')

    def poll():
        nonlocal usage
        waited, status, current_usage = os.wait4(process.pid, os.WNOHANG)
        if waited:
            process.returncode = os.waitstatus_to_exitcode(status)
            usage = current_usage
            return True
        return False

    def request_stop():
        try:
            os.kill(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

    def await_cleanup():
        # Bound cooperation; do not block indefinitely waiting for a killed helper.
        nonlocal forced
        deadline = time.monotonic() + 3.0
        while time.monotonic() < deadline:
            if poll():
                return
            time.sleep(0.01)
        forced = True
        try:
            os.kill(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        deadline = time.monotonic() + 0.5
        while time.monotonic() < deadline:
            if poll():
                return
            time.sleep(0.01)

    try:
        with streams[0].open('xb') as stdout, streams[1].open('xb') as stderr:
            supervisor = Path(__file__).with_name('process_supervisor.py')
            process = subprocess.Popen([sys.executable, '-I', '-B', '-S', str(supervisor), str(request_path)],
                                       env=env, stdout=stdout, stderr=stderr, start_new_session=True)
            while True:
                if poll():
                    overflow = any(p.stat().st_size > max_output_bytes for p in streams)
                    timed_out = time.monotonic()-wall >= timeout
                    break
                timed_out = time.monotonic()-wall >= timeout
                overflow = any(p.stat().st_size > max_output_bytes for p in streams)
                if timed_out or overflow:
                    request_stop()
                    await_cleanup()
                    break
                time.sleep(0.01)
    except BaseException as exc:
        failure = {'type': type(exc).__name__, 'message': str(exc)}
        if process is not None and process.returncode is None:
            request_stop()
            await_cleanup()
    try:
        tree = json.loads((output/'process_tree.json').read_text())
    except (OSError, ValueError):
        tree = {'cleanup_complete': False, 'unexpected_descendants': False,
                'supervisor_pid': process.pid if process else None,
                'observed_pids': [], 'terminated_pids': [], 'reaped_pids': [],
                'survivors': [], 'failure': {'type': 'MissingSupervisorEvidence',
                                           'message': 'no valid supervisor tree receipt'}}
    tree['supervisor_forced_exit'] = forced
    if forced or process is None or process.returncode != 0:
        tree['cleanup_complete'] = False
    if not tree['cleanup_complete'] and process is not None and process.returncode is None:
        tree['survivors'] = sorted(set(tree.get('survivors', [])) | {process.pid})
    failure = failure or tree.get('failure')
    returncode = tree.get('returncode')
    receipt = {'command': command, 'pid': tree.get('leader_pid'),
               'started_unix_ns': unix_ns, 'returncode': returncode,
               'timed_out': timed_out, 'output_limit_exceeded': overflow,
               'succeeded': returncode == 0 and not timed_out and not overflow and failure is None
                            and tree['cleanup_complete'] and not tree['unexpected_descendants'],
               'failure': failure, 'wall_seconds': time.monotonic()-wall,
               'process_tree': tree,
               'wait4': ({'user_seconds': usage.ru_utime, 'system_seconds': usage.ru_stime,
                          'max_rss_kib': usage.ru_maxrss} if usage is not None else None),
               'streams': {p.name: {'bytes': p.stat().st_size,
                           'sha256': _file_sha256(p)}
                           for p in streams if p.is_file()},
               'cost_boundary': 'One wait4 observation of the supervisor including its reaped subtree '
                                'and startup; nested receipts must not be added again. Caller parent '
                                'CPU/startup is outside this receipt. Incomplete cleanup is never success.'}
    (output/'receipt.json').write_text(json.dumps(receipt, indent=2, allow_nan=False)+'\n')
    if failure is not None:
        raise RuntimeError('Recorded child failure: '+failure['message'])
    return receipt
