"""Dedicated stage66 worker, original snapshots and once-per-version IDs."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

BASE = Path('/workspace/scratch/actual-source-regular-local-collar-construct')
PROJECT = Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
PUBLICATION = Path('/workspace/scratch/actual-source-regular-local-collar-publication')


def utc():
    return datetime.now(timezone.utc).isoformat()


def put(path, value, exclusive=False):
    with Path(path).open('x' if exclusive else 'w', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def identity(path, cache):
    path = Path(path)
    if not path.is_file():
        return None
    key = str(path)
    info = path.stat()
    marker = [info.st_size, info.st_mtime_ns]
    old = cache.get(key)
    if old and old.get('marker') == marker:
        return old
    row = {'path': key, 'bytes': info.st_size,
           'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
           'marker': marker, 'first_observed_utc': utc(),
           'origin': 'FIRST identity of necessary NEW actual version; cached once'}
    cache[key] = row
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('label')
    parser.add_argument('kind', choices=['documentary', 'math'])
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not args.label or '/' in args.label or args.label in {'.', '..'}:
        raise RuntimeError('Simple unique label required')
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        raise RuntimeError('Literal command required')
    if args.kind == 'math':
        release = json.loads((PUBLICATION/'ROOT_MATHEMATICAL_EXECUTION_RELEASE66.json').read_text())
        if release.get('mathematical_execution_authorized') is not True:
            raise RuntimeError('Separate root mathematical execution release required')
    run = BASE/'runs'/args.label
    run.mkdir(parents=True, exist_ok=False)
    cache_path = BASE/'FIRST_ID_CACHE.json'
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    # Root's exact copied-controls identity is reused; no old control hash.
    control = BASE/'CONTROL_CONTRACT.md'
    if str(control) not in cache:
        adopted = json.loads((PUBLICATION/'ROOT_CONTROL_CONTRACT66_COPY.json').read_text())
        st = control.stat()
        if adopted['destination'] != str(control) or st.st_size != adopted['bytes']:
            raise RuntimeError('Known root control copy binding differs')
        cache[str(control)] = {'path': str(control), 'bytes': adopted['bytes'],
            'sha256': adopted['sha256'], 'marker': [st.st_size, st.st_mtime_ns],
            'origin': 'Known exact root copied contract identity REUSED; zero hashes here',
            'copied_from': adopted['source'], 'first_observed_utc': adopted['observed_utc']}
    paths = [BASE/'FROZEN_CONTEXT.md', BASE/'INITIAL_SOURCE_COMMON.lean.txt',
             BASE/'BOOTSTRAP_PLAN.md', control,
             *sorted((BASE/'runner').glob('*.py')),
             PROJECT/'SourceActualRegularLocalCollar.lean',
             BASE/'RegularLocalCollarControls.lean', BASE/'FalseControl.lean',
             BASE/'build/SourceActualRegularLocalCollar.olean',
             BASE/'build/RegularLocalCollarControls.olean']
    paths += sorted(BASE.glob('*.lean.txt')) + sorted(BASE.glob('*.patch'))
    paths = list(dict.fromkeys(paths))
    before, snapshots = {}, {}
    snapshot = run/'before'
    snapshot.mkdir()
    for i, path in enumerate(paths):
        row = identity(path, cache)
        before[str(path)] = row
        if row is not None and path.suffix != '.olean':
            destination = snapshot/(str(i)+'-'+path.name)
            shutil.copyfile(path, destination)
            st = destination.stat()
            cache[str(destination)] = {**row, 'path': str(destination),
                'marker': [st.st_size, st.st_mtime_ns],
                'origin': 'Known exact snapshot copy identity REUSED; no hash',
                'copied_from': str(path)}
            snapshots[str(path)] = str(destination)
    put(cache_path, cache)
    start, tick = utc(), time.monotonic()
    intent = {'label': args.label, 'scope_kind': args.kind,
              'command_argv': command, 'cwd': str(PROJECT), 'start_utc': start,
              'before': before, 'before_snapshots': snapshots,
              'outer_capture_dir': str(BASE/'outer'/args.label),
              'entry_capture_dir': str(BASE/'entry'/args.label),
              'environment_recorded': {'PYTHONDONTWRITEBYTECODE': os.environ.get('PYTHONDONTWRITEBYTECODE')},
              'credential_environment_logged': False, 'automatic_retry': False}
    put(run/'STARTED.json', intent, True)
    put(run/'INTENT.json', intent, True)
    code, failure = None, None
    try:
        with (run/'stdout.log').open('xb') as out, (run/'stderr.log').open('xb') as err:
            process = subprocess.run(command, cwd=PROJECT, stdout=out, stderr=err)
            code = process.returncode
            out.flush(); os.fsync(out.fileno())
            err.flush(); os.fsync(err.fileno())
    except BaseException as exc:
        failure = repr(exc)
    end, elapsed = utc(), time.monotonic()-tick
    cache = json.loads(cache_path.read_text())
    after = {str(path): identity(path, cache) for path in paths}
    streams = {name: identity(run/name, cache) for name in ['stdout.log', 'stderr.log']}
    receipt = {**intent, 'end_utc': end, 'elapsed_seconds': elapsed,
               'exit_code': code, 'spawn_or_worker_exception': failure,
               'after': after, 'streams': streams,
               'worker_capture': 'Original separate full stdout/stderr; actual inner result retained independently of outer/entry',
               'binary_snapshot_or_canonical_object_copy': False}
    put(run/'receipt.json', receipt, True)
    put(cache_path, cache)
    print(json.dumps({'label': args.label, 'exit_code': code,
                      'receipt': str(run/'receipt.json'), 'exception': failure}))
    return code if code is not None and code >= 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
