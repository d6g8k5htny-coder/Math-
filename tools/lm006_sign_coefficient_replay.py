#!/usr/bin/env python3
"""Replay the frozen PR362 coefficient, preserving source and process evidence.

Standard library / POSIX only. This is an execution interlock, not mathematical
acceptance or Lean formalization. The numerical files are immutable inputs.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import signal
import subprocess
import sys
import time

REPOSITORY = 'd6g8k5htny-coder/Math-'
SOURCE_COMMIT = '1f64b8f8ee450262e0f56e6bdf9dfb37931f48c6'
PACKET = 'coefficients/lm006_wrong_sign_20261006_r20'
EXECUTION_FILES = ('tools/lm006_sign_coefficient_replay.py',
                   'tests/test_lm006_sign_coefficient_replay.py',
                   '.github/workflows/lm006-sign-coefficient.yml')
PINS = {'coefficients/lm006_wrong_sign_20261006_r20/NOTE.md': 'a79f080851bba69a03ec4b8348dc93d04143bf62',
 'coefficients/lm006_wrong_sign_20261006_r20/RESULTS.json': '53b5921f40f95a2623795b6cfe9ec47420705ad3',
 'coefficients/lm006_wrong_sign_20261006_r20/SOURCES.json': 'e51a4dfb507c373baafc12ec20afed609092fd34',
 'coefficients/lm006_wrong_sign_20261006_r20/enclose.py': 'e680ddb7aa0abd4b6aab2cac6a54c1ff28efc782',
 'coefficients/lm006_wrong_sign_20261006_r20/test_enclosure.py': 'a05992a4e5d9845618aee6ea53d62e08ee776940',
 'reviews/lm006_wrong_sign_asymptotic_20261006/NOTE.md': 'ea914c1b8e0b8180b645f3f626e2081ab87700b9',
 'imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md': 'dfed3b8d318a3ab1950957f393307733a4bef3f2'}
DEPENDENCIES = ('reviews/lm006_wrong_sign_asymptotic_20261006/NOTE.md',
 'imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md')
TEST_NAMES = ('test_cli',
 'test_density_parameter_intervals',
 'test_exponential_against_unrounded_alternating_sums',
 'test_exponential_bounds',
 'test_full_rectangle_sum_against_fraction_reference',
 'test_grid_refines_and_tails_positive',
 'test_image_moment_bound',
 'test_independent_inner_primitive',
 'test_invalid_inputs',
 'test_j_exact',
 'test_normalizer',
 'test_pi_and_cdf',
 'test_rational_rounding',
 'test_rectangle_extrema',
 'test_square_root_enclosure')
MAX_STREAM_BYTES = 4 * 1024 * 1024


class ReplayError(ValueError):
    """A failure is not a successful negative control."""


def require(ok, reason):
    if not ok:
        raise ReplayError(reason)


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw):
    return hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def source_file(root, relative):
    require(type(relative) is str and relative and '\\' not in relative
            and not relative.startswith('/')
            and all(s not in ('', '.', '..') for s in relative.split('/')), 'unsafe_path')
    p = Path(root)
    for part in PurePosixPath(relative).parts:
        p = p / part
        require(not p.is_symlink(), 'source_symlink')
    require(p.is_file(), 'source_missing')
    return p


def validate_snapshot(root, pins=None):
    """Alternate pins are only for explicit synthetic tests; no CLI override exists."""
    pins = PINS if pins is None else pins
    result = {}
    for name, expected in pins.items():
        raw = source_file(root, name).read_bytes()
        actual = git_blob(raw)
        require(actual == expected, 'source_identity: ' + name)
        result[name] = {'bytes': len(raw), 'sha256': sha256(raw), 'git_blob': actual}
    names = sorted(Path(name).name for name in pins if name.startswith(PACKET + '/'))
    require(sorted(p.name for p in (Path(root) / PACKET).iterdir()) == names, 'packet_membership')
    return result


def check_output(stdout, stderr, expected, kind):
    if kind == 'tests':
        # Every named test must succeed: zero tests, skips, unknown tests, noise and
        # a forged summary without individual pass lines are not accepted.
        prefix = '\n'.join(name + ' (test_enclosure.EnclosureTests.' + name + ') ... ok'
                           for name in TEST_NAMES).encode()
        pattern = re.escape(prefix + b'\n\n' + b'-' * 70)
        pattern += rb'\nRan 15 tests in [0-9]+(?:\.[0-9]+)?s\n\nOK\n'
        require(stdout == b'' and re.fullmatch(pattern, stderr) is not None, 'test_report_mismatch')
        return
    require(kind == 'exact', 'unknown_contract')
    require(stderr == b'', 'unexpected_stderr')
    # Compare all bytes, preserving numeric strings, JSON types, the grid and
    # the immutable author-run independently_reviewed=false annotation.
    require(stdout == expected, 'stdout_mismatch')


def write_json(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write('\n')


def run_step(argv, cwd, logs, name, expected, kind, timeout=900):
    require(os.name == 'posix', 'posix_required')
    require(re.fullmatch(r'[a-z][a-z0-9_-]*', name) is not None, 'unsafe_step_name')
    logs = Path(logs)
    out, err, process = [logs / (name + suffix) for suffix in ('.stdout', '.stderr', '.process.json')]
    require(not any(p.exists() or p.is_symlink() for p in (out, err, process)), 'step_evidence_exists')
    start = time.monotonic_ns()
    record = {'command': list(map(str, argv)), 'returncode': None, 'timed_out': False,
              'status': 'FAIL', 'timeout_seconds': timeout}
    failure = None
    # Files, not PIPEs, retain partial output and avoid inherited-pipe deadlocks.
    # Kill the isolated POSIX process group on timeout. This is not an OS sandbox:
    # a hostile process deliberately leaving the group is outside this contract.
    with out.open('xb') as stdout, err.open('xb') as stderr:
        try:
            child = subprocess.Popen(argv, cwd=cwd, stdout=stdout, stderr=stderr,
                                     start_new_session=True,
                                     env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
            try:
                record['returncode'] = child.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                record['timed_out'] = True
                failure = 'timeout'
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                try:
                    record['returncode'] = child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    record['detail'] = 'process-group termination did not finish in 5 seconds'
        except OSError as exc:
            failure = 'spawn_error'
            record['detail'] = type(exc).__name__ + ': ' + str(exc)
    record['elapsed_ns'] = time.monotonic_ns() - start
    # A bound applies before reading logs into memory. Full on-disk streams remain
    # available for diagnosis even when the output contract is exceeded.
    sizes = (out.stat().st_size, err.stat().st_size)
    if max(sizes) > MAX_STREAM_BYTES:
        failure = failure or 'output_too_large'
        record['stdout_bytes'], record['stderr_bytes'] = sizes
    else:
        stdout, stderr = out.read_bytes(), err.read_bytes()
        record.update(stdout_bytes=len(stdout), stderr_bytes=len(stderr),
                      stdout_sha256=sha256(stdout), stderr_sha256=sha256(stderr))
        if failure is None:
            try:
                require(record['returncode'] == 0, 'unexpected_exit')
                check_output(stdout, stderr, expected, kind)
            except ReplayError as exc:
                failure = str(exc)
    if failure is None:
        record['status'] = 'PASS'
    else:
        record['failure'] = failure
    write_json(process, record)
    if failure is not None:
        raise ReplayError(failure)
    return record


def git(root, *args):
    p = subprocess.run(['git', *args], cwd=root, capture_output=True, timeout=30)
    require(p.returncode == 0, 'git_command_failed')
    return p.stdout.decode('ascii').strip()


def git_head(root):
    head = git(root, 'rev-parse', 'HEAD')
    require(re.fullmatch('[0-9a-f]{40}', head) is not None, 'invalid_git_head')
    return head


def execution_sources(root, head):
    result = {}
    for name in EXECUTION_FILES:
        raw = source_file(root, name).read_bytes()
        committed = git(root, 'rev-parse', head + ':' + name)
        require(committed == git_blob(raw), 'execution_source_drift')
        result[name] = {'git_blob': committed, 'sha256': sha256(raw), 'bytes': len(raw)}
    return result


def host_identity(head, env):
    if env.get('GITHUB_ACTIONS') == 'true':
        require(env.get('GITHUB_REPOSITORY') == REPOSITORY and env.get('GITHUB_SHA') == head,
                'host_identity')
        for key in ('GITHUB_RUN_ID', 'GITHUB_RUN_ATTEMPT'):
            require(re.fullmatch('[1-9][0-9]*', env.get(key, '')) is not None, 'host_identity')


def execute(root, output, mode):
    root, output = Path(root).resolve(), Path(output).resolve()
    require(mode in ('normal', 'optimized'), 'invalid_mode')
    require(not output.is_relative_to(root), 'evidence_inside_source')
    require(not output.exists(), 'evidence_exists')
    output.mkdir(parents=True)
    receipt = {'schema_version': 1, 'object': 'LM006-SIGN-COEFFICIENT-REPLAY',
               'repository': REPOSITORY, 'source_commit': SOURCE_COMMIT, 'mode': mode,
               'scientific_acceptance': False, 'formal_verification': False,
               'status': 'FAIL', 'steps': {},
               'run_id': os.environ.get('GITHUB_RUN_ID'),
               'run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT'),
               'event': os.environ.get('GITHUB_EVENT_NAME')}
    try:
        before = validate_snapshot(root)
        head = git_head(root)
        receipt['tested_commit'] = head
        host_identity(head, os.environ)
        receipt['execution_sources'] = execution_sources(root, head)
        receipt['sources'] = before
        require(Path(__file__).resolve() == root / EXECUTION_FILES[0], 'driver_location')
        require(git(root, 'status', '--porcelain', '--untracked-files=no') == '', 'tracked_source_dirty')
        packet = root / PACKET
        flags = ['-B'] + (['-O'] if mode == 'optimized' else []) + ['-S']
        specs = [('tests', ['-m', 'unittest', 'test_enclosure', '-v'], None, 'tests'),
                 ('coefficient', ['enclose.py', '--grid', '2048'],
                  (packet / 'RESULTS.json').read_bytes(), 'exact')]
        for name, args, expected, kind in specs:
            try:
                run_step([sys.executable, *flags, *args], packet, output, name, expected, kind)
            finally:
                path = output / (name + '.process.json')
                if path.is_file():
                    raw = path.read_bytes()
                    receipt['steps'][name] = {'process_sha256': sha256(raw),
                                              'record': json.loads(raw)}
        require(validate_snapshot(root) == before, 'source_changed_during_execution')
        require(execution_sources(root, head) == receipt['execution_sources'], 'execution_source_drift')
        require(git_head(root) == head, 'head_changed_during_execution')
        require(git(root, 'status', '--porcelain', '--untracked-files=no') == '', 'tracked_source_dirty')
        receipt['status'] = 'PASS'
    except Exception as exc:
        receipt['failure'] = type(exc).__name__ + ': ' + str(exc)
        raise
    finally:
        write_json(output / 'receipt.json', receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--mode', choices=('normal', 'optimized'), required=True)
    args = parser.parse_args()
    try:
        result = execute(args.root, args.output, args.mode)
    except Exception as exc:
        print('LM006_REPLAY_FAIL: ' + type(exc).__name__ + ': ' + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
