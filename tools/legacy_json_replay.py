#!/usr/bin/env python3
"""Authenticate the three fixed legacy checkers' success and rejection reports.

Called AFTER each workflow's unchanged scientific source/manifest guards. The
reference file holds measured, source-bound reports, never outputs learned from
the invocation being tested. Structural JSON comparison permits formatting only;
all keys, types, values, lists and intended information must still match exactly.
This is an engineering protocol, not a sandbox or mathematical acceptance test.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

INVENTORIES = {
    'local-pairing': ('M1', 'M2', 'M3', 'M4'),
    'far-elder': ('M1', 'M2', 'M3', 'M4'),
    'c6-cluster': ('pins-not-critical', 'wrong-pin-hessian', 'drop-sigma-jacobian',
                   'three-extra-points', 'shear-drop-cubic', 's-bound-constant',
                   'cross-term-not-small', 'window-closed', 'index-sign'),
}
# The CLI's argparse choice order is distinct from the workflow execution order.
C6_CHOICES = ('pins-not-critical', 'wrong-pin-hessian', 'drop-sigma-jacobian',
              'three-extra-points', 'cross-term-not-small', 'window-closed',
              'index-sign', 'shear-drop-cubic', 's-bound-constant')


class ProtocolError(RuntimeError):
    """The supplied process is not the expected source-bound observation."""


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name, value in pairs:
        if name in result:
            raise ProtocolError('duplicate JSON key: ' + name)
        result[name] = value
    return result


def _not_integer(text: str) -> Any:
    raise ProtocolError('floating/nonfinite JSON number is outside this contract: ' + text)


def strict_json(raw: bytes) -> Any:
    if len(raw) > 256 * 1024:
        raise ProtocolError('JSON output exceeds the fixed contract limit')
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=_object,
                          parse_float=_not_integer, parse_constant=_not_integer)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ProtocolError('invalid single JSON report') from exc


def _same(actual: Any, expected: Any) -> bool:
    # In particular Python's False == 0 is not accepted as JSON type equality.
    if type(actual) is not type(expected):
        return False
    if type(expected) is dict:
        return actual.keys() == expected.keys() and all(
            _same(actual[key], value) for key, value in expected.items())
    if type(expected) is list:
        return len(actual) == len(expected) and all(
            _same(a, b) for a, b in zip(actual, expected))
    return actual == expected


def _contract(family: str) -> dict[str, Any]:
    if family not in INVENTORIES:
        raise ProtocolError('unknown checker family')
    data = strict_json(Path(__file__).with_name('legacy_json_contracts.json').read_bytes())
    if (type(data) is not dict or type(data.get('schema')) is not int
            or data['schema'] != 1 or type(data.get('families')) is not dict
            or set(data['families']) != set(INVENTORIES)):
        raise ProtocolError('invalid reference inventory')
    entry = data['families'][family]
    keys = {'directory', 'script', 'script_git_blob', 'baseline_sha256',
            'baseline_bytes', 'mutants'}
    if type(entry) is not dict or set(entry) != keys:
        raise ProtocolError('invalid family reference schema')
    if (type(entry['mutants']) is not dict
            or set(entry['mutants']) != set(INVENTORIES[family])):
        raise ProtocolError('missing, extra, or repeated mutant reference')
    if (type(entry['script']) is not str
            or Path(entry['script']).name != entry['script']
            or type(entry['directory']) is not str
            or type(entry['baseline_bytes']) is not int or entry['baseline_bytes'] < 0):
        raise ProtocolError('invalid script or baseline metadata')
    for key, size in [('script_git_blob', 40), ('baseline_sha256', 64)]:
        if type(entry[key]) is not str or not re.fullmatch('[0-9a-f]{%d}' % size, entry[key]):
            raise ProtocolError('invalid reference digest')
    for report in entry['mutants'].values():
        if type(report) is not dict or report.get('passed') is not False:
            raise ProtocolError('reference is not a rejection report')
    return entry


def _unknown_stderr(family: str, script_name: str) -> bytes:
    if family != 'c6-cluster':
        return b'unknown mutant label\n'
    # Reproduce the frozen grammar, not output learned from the checker. The
    # child has captured stdout, so shutil's terminal-width query cannot use the
    # parent's TTY. Match its positive COLUMNS override or 80-column pipe fallback.
    try:
        columns = int(os.environ.get('COLUMNS', '0'))
    except ValueError:
        columns = 0
    if columns <= 0:
        columns = 80
    # CPython 3.11--3.13 HelpFormatter subtracts two from the terminal columns.
    parser = argparse.ArgumentParser(
        prog=script_name,
        formatter_class=lambda prog: argparse.HelpFormatter(prog, width=columns - 2))
    parser.add_argument('--mutant', choices=C6_CHOICES)
    stream = io.StringIO()
    try:
        with contextlib.redirect_stderr(stream):
            parser.parse_args(['--mutant', 'unknown'])
    except SystemExit as exc:
        if exc.code != 2:
            raise ProtocolError('reference argument grammar did not reject') from exc
    else:
        raise ProtocolError('reference argument grammar unexpectedly accepted')
    return stream.getvalue().encode('utf-8')


def replay(family: str, root: Path, *, timeout: float = 600) -> list[dict[str, Any]]:
    """Run the complete fixed inventory in both modes, or fail immediately.

    root is the already source-verified packet directory. Timeout/OSError is a
    failed run, never an intended negative-control receipt. All child inputs stay
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
    expected = (root / 'RESULTS.json').read_bytes()
    if (len(expected) != entry['baseline_bytes']
            or hashlib.sha256(expected).hexdigest() != entry['baseline_sha256']):
        raise ProtocolError('baseline differs from the characterized source')
    unknown = 'unknown' if family == 'c6-cluster' else 'M9'
    unknown_stderr = _unknown_stderr(family, script.name)
    records: list[dict[str, Any]] = []
    for mode, flags in [('normal', ['-B', '-S']), ('optimized', ['-B', '-O', '-S'])]:
        for label in [None, *INVENTORIES[family], unknown]:
            command = [sys.executable, *flags, str(script)]
            if label is not None:
                command += ['--mutant', label]
            child = subprocess.run(command, capture_output=True, timeout=timeout)
            record = {'family': family, 'mode': mode, 'label': label,
                      'returncode': child.returncode,
                      'stdout_bytes': len(child.stdout), 'stderr_bytes': len(child.stderr),
                      'stdout_sha256': hashlib.sha256(child.stdout).hexdigest(),
                      'stderr_sha256': hashlib.sha256(child.stderr).hexdigest()}
            if label is None:
                ok = child.returncode == 0 and not child.stderr and child.stdout == expected
            elif label == unknown:
                ok = child.returncode == 2 and not child.stdout and child.stderr == unknown_stderr
            else:
                ok = child.returncode == 1 and not child.stderr
                if ok:
                    try:
                        ok = _same(strict_json(child.stdout), entry['mutants'][label])
                    except ProtocolError:
                        ok = False
            record['protocol_ok'] = ok
            print(json.dumps(record, sort_keys=True), flush=True)
            if not ok:
                raise ProtocolError('legacy protocol mismatch: %s/%s/%s' %
                                    (family, mode, label or 'baseline'))
            records.append(record)
    return records
