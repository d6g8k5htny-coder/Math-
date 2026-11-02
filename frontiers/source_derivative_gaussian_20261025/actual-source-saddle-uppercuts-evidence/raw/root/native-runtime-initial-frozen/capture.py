#!/usr/bin/env python3
"""Root-only prospective process capture. This module performs nothing on import."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import os
import subprocess
import sys
import time


def utc():
    return datetime.now(timezone.utc).isoformat()


def require(value, message):
    if not value:
        raise RuntimeError(message)


def put_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    sync_dir(path.parent)


def sync_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


class CaptureRun:
    def __init__(self, path, operation):
        self.path = Path(path).resolve()
        self.path.mkdir(parents=True, exist_ok=False)
        sync_dir(self.path.parent)
        self.operation = operation
        self.start = utc()
        self.tick = time.monotonic()
        self.counter = 0
        put_new(self.path / 'STARTED.json', {
            'operation': operation, 'script_argv': sys.argv, 'cwd': os.getcwd(),
            'started_utc': self.start,
            'policy': 'No automatic retry; all actual command streams remain original and separate.',
            'credential_environment_logged': False,
        })

    def event(self, value):
        with (self.path / 'EVENTS.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps({'observed_utc': utc(), **value}, ensure_ascii=False) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        sync_dir(self.path)

    def command(self, label, argv, cwd, stdin_bytes=None, stdin_binding=None, env_overrides=None):
        self.counter += 1
        folder = self.path / ('%02d-%s' % (self.counter, label))
        folder.mkdir()
        argv = [str(x) for x in argv]
        overrides = dict(env_overrides or {})
        require(set(overrides) <= {'GIT_INDEX_FILE'}, 'Only isolated-index override may be recorded here.')
        started = utc()
        tick = time.monotonic()
        intent = {'command_argv': argv, 'cwd': str(cwd), 'started_utc': started,
                  'explicit_environment_overrides': overrides,
                  'stdin_binding': stdin_binding, 'original_separate_capture': True}
        put_new(folder / 'INTENT.json', intent)
        try:
            with (folder / 'stdout.log').open('xb') as out, (folder / 'stderr.log').open('xb') as err:
                process = subprocess.run(argv, cwd=str(cwd), input=stdin_bytes,
                                         stdout=out, stderr=err,
                                         env={**os.environ, **overrides})
                out.flush()
                os.fsync(out.fileno())
                err.flush()
                os.fsync(err.fileno())
        except BaseException as exc:
            put_new(folder / 'SPAWN_FAILURE.json', {
                **intent, 'ended_utc': utc(), 'elapsed_seconds': time.monotonic() - tick,
                'exception': repr(exc), 'child_exit_code': None,
                'limit': 'No child exit code is invented for a spawn/interruption failure.'})
            raise
        receipt = {**intent, 'ended_utc': utc(), 'elapsed_seconds': time.monotonic() - tick,
                   'exit_code': process.returncode, 'stdout': 'stdout.log', 'stderr': 'stderr.log'}
        put_new(folder / 'RECEIPT.json', receipt)
        self.event({'event': 'command_finished', 'label': label, 'receipt': str(folder / 'RECEIPT.json'),
                    'exit_code': process.returncode})
        require(process.returncode == 0, 'Command failed (%s); preserve %s' % (label, folder))
        return (folder / 'stdout.log').read_bytes()

    def finish(self, value):
        result = {'operation': self.operation, 'started_utc': self.start, 'ended_utc': utc(),
                  'elapsed_seconds': time.monotonic() - self.tick, **value}
        put_new(self.path / 'RESULT.json', result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return result


def wrapper_cli():
    parser = argparse.ArgumentParser(description='Root prospective worker/outer/entry capture, no hashes.')
    parser.add_argument('--run-dir', required=True)
    parser.add_argument('--cwd', required=True)
    parser.add_argument('--scope', choices=['worker', 'outer', 'entry'], required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    require(command, 'A literal child command is required.')
    run = CaptureRun(args.run_dir, 'root65-' + args.scope + '-capture')
    try:
        run.command(args.scope, command, args.cwd)
        run.finish({'status': 'PASS_ACTUAL_CHILD_EXIT_ZERO', 'exit_code': 0,
                    'scope': args.scope, 'capture_hashes_claimed': False})
        return 0
    except Exception as exc:
        run.finish({'status': 'FAIL_PRESERVED_NO_AUTOMATIC_RETRY', 'exception': repr(exc),
                    'scope': args.scope, 'exit_code': 1,
                    'note': 'This wrapper exit is1; actual child exit remains in its command receipt.'})
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(wrapper_cli())
