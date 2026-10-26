#!/usr/bin/env python3
"""Authenticate the C8 check-mode checkers' acceptance and rejection verdicts.

Called AFTER each workflow's unchanged source and pin guards. Each checker runs
from its packet directory as `<script> --check [--mutant LABEL]` and prints one
JSON verdict: {"check": "ok", ...} with exit 0, or, from its require(),
{"check": "FAIL", "reason": ..., "mutant": LABEL} with exit 1. The reference
file holds complete verdicts measured from the unchanged checkers, never outputs
learned from the invocation being tested. Parsing and comparison are those of
tools/legacy_json_replay.py: formatting may differ, but every key, type, value
and list must match. This is an engineering protocol, not a sandbox or
mathematical acceptance test.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

from tools.legacy_json_replay import ProtocolError, _same, strict_json

INVENTORIES = {
    'c8-cap-failure-coefficient-dims': ('no-y-tail', 'r3-one', 'no-bp', 'frob-omega-off'),
    'c8-normalizer-floor-planar': ('swap-minmax', 'drop-torus-error', 'sign-saddle'),
}


def _contract(family: str) -> dict[str, Any]:
    if family not in INVENTORIES:
        raise ProtocolError('unknown checker family')
    data = strict_json(Path(__file__).with_name('check_mode_contracts.json').read_bytes())
    if (type(data) is not dict or type(data.get('schema')) is not int
            or data['schema'] != 1 or type(data.get('families')) is not dict
            or set(data['families']) != set(INVENTORIES)):
        raise ProtocolError('invalid reference inventory')
    entry = data['families'][family]
    keys = {'directory', 'script', 'script_git_blob', 'results_sha256',
            'results_bytes', 'baseline', 'mutants'}
    if type(entry) is not dict or set(entry) != keys:
        raise ProtocolError('invalid family reference schema')
    if (type(entry['script']) is not str
            or Path(entry['script']).name != entry['script']
            or type(entry['directory']) is not str
            or type(entry['results_bytes']) is not int or entry['results_bytes'] < 0):
        raise ProtocolError('invalid script or results metadata')
    for key, size in [('script_git_blob', 40), ('results_sha256', 64)]:
        if type(entry[key]) is not str or not re.fullmatch('[0-9a-f]{%d}' % size, entry[key]):
            raise ProtocolError('invalid reference digest')
    baseline = entry['baseline']
    if type(baseline) is not dict or baseline.get('check') != 'ok' or baseline.get('mutant', '') is not None:
        raise ProtocolError('reference is not an acceptance verdict')
    if (type(entry['mutants']) is not dict
            or set(entry['mutants']) != set(INVENTORIES[family])):
        raise ProtocolError('missing, extra, or repeated mutant reference')
    for label, report in entry['mutants'].items():
        if (type(report) is not dict or set(report) != {'check', 'reason', 'mutant'}
                or report['check'] != 'FAIL' or report['mutant'] != label
                or type(report['reason']) is not str):
            raise ProtocolError('reference is not a rejection verdict')
    return entry


def replay(family: str, root: Path, *, timeout: float = 1500) -> list[dict[str, Any]]:
    """Run the complete fixed inventory in both modes, or fail immediately.

    root is the already source-verified packet directory, and also each child's
    working directory, as the checkers expect. Timeout/OSError is a failed run,
    never an intended negative-control receipt. All child inputs stay
    unchanged; no synthetic output, package rehash, or checker amendment occurs.
    """
    entry = _contract(family)
    root = Path(root).resolve()
    script = root / entry['script']
    if script.is_symlink() or not script.is_file():
        raise ProtocolError('regular source checker required')
    data = script.read_bytes()
    if hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest() != entry['script_git_blob']:
        raise ProtocolError('checker differs from the characterized source')
    results = (root / 'RESULTS.json').read_bytes()
    if (len(results) != entry['results_bytes']
            or hashlib.sha256(results).hexdigest() != entry['results_sha256']):
        raise ProtocolError('RESULTS.json differs from the characterized source')
    records: list[dict[str, Any]] = []
    for mode, flags in [('normal', ['-B', '-S']), ('optimized', ['-B', '-O', '-S'])]:
        for label in [None, *INVENTORIES[family]]:
            command = [sys.executable, *flags, str(script), '--check']
            if label is not None:
                command += ['--mutant', label]
            child = subprocess.run(command, cwd=root, capture_output=True, timeout=timeout)
            record = {'family': family, 'mode': mode, 'label': label,
                      'returncode': child.returncode,
                      'stdout_bytes': len(child.stdout), 'stderr_bytes': len(child.stderr),
                      'stdout_sha256': hashlib.sha256(child.stdout).hexdigest(),
                      'stderr_sha256': hashlib.sha256(child.stderr).hexdigest()}
            if label is None:
                status, reference = 0, entry['baseline']
            else:
                status, reference = 1, entry['mutants'][label]
            ok = child.returncode == status and not child.stderr
            if ok:
                try:
                    ok = _same(strict_json(child.stdout), reference)
                except ProtocolError:
                    ok = False
            record['protocol_ok'] = ok
            print(json.dumps(record, sort_keys=True), flush=True)
            if not ok:
                raise ProtocolError('check-mode protocol mismatch: %s/%s/%s' %
                                    (family, mode, label or 'baseline'))
            records.append(record)
    return records
