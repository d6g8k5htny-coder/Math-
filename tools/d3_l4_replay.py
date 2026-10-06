#!/usr/bin/env python3
"""Fail-closed execution of the frozen PR304 coefficient packet (stdlib only).

This verifies source custody and actual execution, not mathematical acceptance.
The ten scientific packet files are immutable inputs, never updated by this tool.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import time

REPOSITORY = 'd6g8k5htny-coder/Math-'
OBJECT = 'D3-L4-ANISOTROPIC-20261005-v1'
SOURCE_COMMIT = '2f8d721e300850e36ab17464dc541c977b3ffcbf'
PACKET = 'coefficients/d3_l4_anisotropic_20261005'
MANIFEST_SHA256 = 'bba2ab2e351b644bbd3eec3b468ab88a2969242db9345f619294d4a8770a2f34'
FILE_NAMES = ('README.md', 'PROOF.md', 'certificate.py', 'test_certificate.py',
              'source_crosscheck.py', 'RESULTS.json', 'REFERENCE.json',
              'CROSSCHECKS.json', 'VALIDATION.json')
UPSTREAM = 'reviews/iba1_periodic_jet_claude_20261005/periodic_jet_check.py'


class ReplayError(ValueError):
    """Named protocol failure; a crash is never a successful negative control."""


def require(condition, code):
    if not condition:
        raise ReplayError(code)


def git_blob(data):
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def strict_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'json_duplicate_key')
            result[key] = value
        return result
    def constant(_):
        raise ReplayError('json_nonfinite')
    def floating(token):
        value = float(token)
        require(math.isfinite(value), 'json_nonfinite')
        return value
    try:
        return json.loads(data, object_pairs_hook=pairs, parse_constant=constant, parse_float=floating)
    except (UnicodeError, json.JSONDecodeError, TypeError) as exc:
        raise ReplayError('json_malformed') from exc


def safe_file(root, relative):
    require(isinstance(relative, str) and relative and '\\' not in relative, 'unsafe_path')
    path = PurePosixPath(relative)
    require(not path.is_absolute() and all(p not in ('', '.', '..') for p in relative.split('/')),
            'unsafe_path')
    current = root
    for part in path.parts:
        current = current / part
        require(not current.is_symlink(), 'symlink_in_source_path')
    require(current.is_file(), 'missing_or_nonregular_source')
    return current


def validate_snapshot(root, expected_manifest_sha=MANIFEST_SHA256):
    """Alternate digest is for explicitly synthetic unit fixtures; CLI has no override."""
    root = Path(root).resolve()
    raw = safe_file(root, PACKET + '/SOURCE_FILES.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == expected_manifest_sha, 'manifest_pin_mismatch')
    meta = strict_json(raw)
    require(isinstance(meta, dict) and meta.get('object') == OBJECT
            and meta.get('scientific_effect') == 'NONE'
            and meta.get('source_commit') == SOURCE_COMMIT
            and meta.get('source_repository') == REPOSITORY, 'manifest_scope')
    records = meta.get('files')
    require(isinstance(records, list) and len(records) == len(FILE_NAMES), 'manifest_membership')
    require(all(isinstance(e, dict) for e in records), 'manifest_record_type')
    require(sorted(e.get('path', '') for e in records) == sorted(FILE_NAMES), 'manifest_membership')
    packet = root / PACKET
    require(sorted(p.name for p in packet.iterdir()) == sorted(FILE_NAMES + ('SOURCE_FILES.json',)),
            'packet_membership')
    for entry in records:
        data = safe_file(root, PACKET + '/' + entry['path']).read_bytes()
        require(type(entry.get('bytes')) is int and len(data) == entry['bytes'], 'source_size')
        require(hashlib.sha256(data).hexdigest() == entry.get('sha256'), 'source_sha256')
        require(git_blob(data) == entry.get('git_blob'), 'source_git_blob')
    pins = meta.get('upstream_pins')
    require(isinstance(pins, list) and pins, 'upstream_pins_missing')
    seen = set()
    for entry in pins:
        require(isinstance(entry, dict) and isinstance(entry.get('path'), str), 'upstream_pin_type')
        require(entry['path'] not in seen, 'upstream_duplicate')
        seen.add(entry['path'])
        data = safe_file(root, entry['path']).read_bytes()
        require(git_blob(data) == entry.get('git_blob'), 'upstream_git_blob')
        if 'sha256' in entry:
            require(hashlib.sha256(data).hexdigest() == entry['sha256'], 'upstream_sha256')
    return meta


def compare_output(actual, expected, kind, stderr=b''):
    if kind == 'tests':
        require(actual == b'' and re.search(rb'\nRan 7 tests in [0-9.]+s\n\nOK\n\Z', stderr),
                'test_summary_missing_or_wrong')
        return
    require(stderr == b'', 'unexpected_stderr')
    if kind == 'exact':
        require(actual == expected, 'stdout_mismatch')
        return
    require(kind == 'crosschecks', 'unknown_output_contract')
    got, want = strict_json(actual), strict_json(expected)
    require(isinstance(got, dict) and isinstance(want, dict), 'crosscheck_shape')
    require(isinstance(got.get('rows'), list) and isinstance(want.get('rows'), list)
            and len(got['rows']) == len(want['rows']), 'crosscheck_shape')
    # ONLY the explicitly noncertificate disk diagnostic is allowed libm last-bit variation.
    # Every interval string, all other fields, and their JSON types must match exactly.
    for row, reference in zip(got['rows'], want['rows']):
        require(isinstance(row, dict) and isinstance(reference, dict), 'crosscheck_shape')
        key = 'independent_disk_midpoint_diagnostic'
        x, y = row.pop(key, None), reference.pop(key, None)
        require(type(x) is float and type(y) is float and math.isfinite(x) and math.isfinite(y)
                and abs(x - y) <= 1e-10, 'crosscheck_diagnostic')
        require(row.get('disk_diagnostic_is_certificate') is False, 'diagnostic_scope')
    canonical = lambda value: json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)
    require(canonical(got) == canonical(want), 'crosscheck_exact_fields')


def run_step(argv, cwd, logs, name, expected, kind, timeout=900):
    started = time.monotonic()
    try:
        run = subprocess.run(argv, cwd=cwd, capture_output=True, timeout=timeout,
                             env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    except subprocess.TimeoutExpired as exc:
        (logs / (name + '.stdout')).write_bytes(exc.stdout or b'')
        (logs / (name + '.stderr')).write_bytes(exc.stderr or b'')
        raise ReplayError(name + ': timeout') from exc
    (logs / (name + '.stdout')).write_bytes(run.stdout)
    (logs / (name + '.stderr')).write_bytes(run.stderr)
    record = dict(command=argv, returncode=run.returncode,
                  elapsed_seconds=round(time.monotonic() - started, 6),
                  stdout_sha256=hashlib.sha256(run.stdout).hexdigest(),
                  stderr_sha256=hashlib.sha256(run.stderr).hexdigest())
    (logs / (name + '.process.json')).write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    require(run.returncode == 0, name + ': unexpected_exit')
    compare_output(run.stdout, expected, kind, run.stderr)
    return record


def execution_identities(root, head):
    identities = {}
    for relative in ('tools/d3_l4_replay.py', 'tests/test_d3_l4_replay.py',
                     '.github/workflows/d3-l4-anisotropic.yml'):
        data = safe_file(root, relative).read_bytes()
        committed = subprocess.run(['git', 'rev-parse', head + ':' + relative], cwd=root,
                                   check=True, capture_output=True, text=True).stdout.strip()
        require(git_blob(data) == committed, 'execution_source_drift')
        identities[relative] = dict(git_blob=committed, sha256=hashlib.sha256(data).hexdigest())
    return identities


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mode', choices=('normal', 'optimized'), required=True)
    ap.add_argument('--root', type=Path, default=Path('.'))
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    root = args.root.resolve(); packet = root / PACKET
    logs = args.output.resolve()
    require(not logs.is_relative_to(packet), 'evidence_must_not_modify_packet')
    # Never overwrite a former run's receipt or silently reuse its output.
    require(not logs.exists(), 'evidence_directory_already_exists')
    logs.mkdir(parents=True)
    receipt = dict(object=OBJECT, repository=REPOSITORY, source_commit=SOURCE_COMMIT,
                   mode=args.mode, manifest_sha256=MANIFEST_SHA256,
                   scientific_acceptance=False, independent_review=False,
                   github_run_id=os.environ.get('GITHUB_RUN_ID'),
                   github_run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'),
                   github_event=os.environ.get('GITHUB_EVENT_NAME'),
                   status='FAIL', steps={})
    try:
        validate_snapshot(root)
        head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, check=True,
                              capture_output=True, text=True).stdout.strip()
        require(re.fullmatch('[0-9a-f]{40}', head), 'tested_commit_missing')
        receipt['tested_commit'] = head
        require(Path(__file__).resolve() == (root / 'tools/d3_l4_replay.py').resolve(),
                'execution_driver_location')
        receipt['execution_sources'] = execution_identities(root, head)
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            require(os.environ.get('GITHUB_SHA') == head
                    and os.environ.get('GITHUB_REPOSITORY') == REPOSITORY, 'host_identity_mismatch')
            require(receipt['github_run_id'] and receipt['github_run_attempt'], 'run_identity_missing')
        flags = ['-B'] + (['-O'] if args.mode == 'optimized' else []) + ['-S']
        command = [sys.executable] + flags
        specs = [('tests', ['-m', 'unittest', 'test_certificate', '-v'], None, 'tests'),
                 ('coefficient', ['certificate.py', '--n', '128'], 'RESULTS.json', 'exact'),
                 ('reference', ['certificate.py', '--reference', '--n', '4'], 'REFERENCE.json', 'exact'),
                 ('crosschecks', ['source_crosscheck.py', '--source', str(root / UPSTREAM)],
                  'CROSSCHECKS.json', 'crosschecks')]
        for name, tail, expected_name, kind in specs:
            expected = None if expected_name is None else (packet / expected_name).read_bytes()
            receipt['steps'][name] = run_step(command + tail, packet, logs, name, expected, kind)
        validate_snapshot(root)
        require(execution_identities(root, head) == receipt['execution_sources'], 'execution_source_drift')
        receipt['status'] = 'PASS'
    except Exception as exc:
        receipt['failure'] = type(exc).__name__ + ': ' + str(exc)
        raise
    finally:
        (logs / 'receipt.json').write_text(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
    print(json.dumps(receipt, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
