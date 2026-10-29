"""Prospective stage66 entry/outer capture; no action occurs on import."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def utc():
    return datetime.now(timezone.utc).isoformat()


def put_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-dir', required=True)
    parser.add_argument('--cwd', required=True)
    parser.add_argument('--scope', choices=['entry', 'outer'], required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        raise RuntimeError('Literal child command required')
    folder = Path(args.run_dir)
    folder.mkdir(parents=True, exist_ok=False)
    start, tick = utc(), time.monotonic()
    intent = {'operation': 'stage66-' + args.scope + '-capture',
              'scope': args.scope, 'script_argv': sys.argv,
              'command_argv': command, 'cwd': args.cwd,
              'started_utc': start, 'original_split_streams': True,
              'environment_recorded': {'PYTHONDONTWRITEBYTECODE': os.environ.get('PYTHONDONTWRITEBYTECODE')},
              'credential_environment_logged': False,
              'automatic_retry': False}
    put_new(folder/'STARTED.json', intent)
    put_new(folder/'INTENT.json', intent)
    code = None
    failure = None
    try:
        with (folder/'stdout.log').open('xb') as out, (folder/'stderr.log').open('xb') as err:
            process = subprocess.run(command, cwd=args.cwd, stdout=out, stderr=err)
            code = process.returncode
            out.flush(); os.fsync(out.fileno())
            err.flush(); os.fsync(err.fileno())
    except BaseException as exc:
        failure = repr(exc)
    receipt = {**intent, 'ended_utc': utc(),
               'elapsed_seconds': time.monotonic()-tick,
               'child_exit_code': code, 'spawn_or_wrapper_exception': failure,
               'stdout': str(folder/'stdout.log'), 'stderr': str(folder/'stderr.log'),
               'status': 'PASS_ACTUAL_CHILD_EXIT_ZERO' if code == 0 and failure is None else 'FAIL_PRESERVED_NO_RETRY'}
    put_new(folder/'RECEIPT.json', receipt)
    put_new(folder/'RESULT.json', receipt)
    print(json.dumps({'scope': args.scope, 'child_exit_code': code,
                      'status': receipt['status'], 'receipt': str(folder/'RECEIPT.json')}))
    if failure is not None:
        print(failure, file=sys.stderr)
    return code if code is not None and code >= 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
