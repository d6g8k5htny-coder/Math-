#!/usr/bin/env python3
"""Authenticate the SIDE24 d = 5, 6 checkers' acceptance and rejection runs.

Called AFTER each workflow's unchanged manifest and pin guards. Each checker is
run from the repository root as `<script>` or `<script> --mutant LABEL`, as the
workflows always ran it. It prints one JSON report on stdout and one timing line
`seconds N.N` on stderr, then exits 0 if every check passed and 1 otherwise.

For every child the protocol requires the exact exit status and a stderr that is
exactly one timing line. The baseline's stdout must equal RESULTS.json byte for
byte. A mutant's stdout must be one strict JSON report structurally equal to the
report measured from the unchanged checker (tools/side24_mutant_contracts/, one
file per family, each within the strict parser's size limit).
One mutant, closed-form `vandermonde`, never reaches a report: the checker's own
structural guard raises. Its reference is that guard: exit 1, empty stdout, and a
traceback whose final line is the measured exception text. Any other crash,
silent exit, extra diagnostic or different report fails. Parsing and comparison
are those of tools/legacy_json_replay.py. This is an engineering protocol, not a
sandbox or a mathematical acceptance test.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

from tools.legacy_json_replay import ProtocolError, _same, strict_json

# Mutant order within each mode, as in each wrapper's original list.
INVENTORIES = {
    'side24-d5-closed-form': (
        'shift-variance', 'vandermonde', 'erfc-sign', 'jacobian', 'mehta', 'by-parts',
        'one-erf', 'two-erf', 'jk-init', 'gauss-half', 'boundary-term', 'atom-pi',
        'cumulative-init', 'cumulative-recurrence'),
    'side24-d5-coefficient': (
        'shift-variance', 'vandermonde', 'erfc-branch', 'remainder-dropped', 'mehta',
        'sphere-area', 'image-shells', 'sandwich-exponent', 'recurrence', 'jacobian',
        'cumulative-half'),
    'side24-d6-coefficient': (
        'shift-variance', 'vandermonde', 'erfc-branch', 'jacobian', 'mehta', 'recurrence',
        'layer-init', 'two-erf', 'cumulative-half', 'remainder-dropped', 'erf-inside',
        'tail-dropped', 'image-shells', 'sandwich-exponent'),
}
MODES = (('normal', ('-B', '-S')), ('optimized', ('-B', '-O', '-S')))
TIMING = re.compile(rb'\Aseconds [0-9]+\.[0-9]\n\Z')
TRACEBACK = b'Traceback (most recent call last):\n'
CONTRACTS = Path(__file__).with_name('side24_mutant_contracts')


def _blob(data: bytes) -> str:
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def _contract(family: str, contracts: Path = CONTRACTS) -> dict[str, Any]:
    if family not in INVENTORIES:
        raise ProtocolError('unknown checker family')
    entry = strict_json((Path(contracts) / (family + '.json')).read_bytes())
    keys = {'schema', 'family', 'directory', 'script', 'script_git_blob', 'results_sha256',
            'results_bytes', 'mutants'}
    if (type(entry) is not dict or set(entry) != keys or type(entry['schema']) is not int
            or entry['schema'] != 1 or entry['family'] != family):
        raise ProtocolError('invalid family reference schema')
    if (type(entry['script']) is not str or Path(entry['script']).name != entry['script']
            or type(entry['directory']) is not str
            or type(entry['results_bytes']) is not int or entry['results_bytes'] <= 0):
        raise ProtocolError('invalid script or results metadata')
    for key, size in (('script_git_blob', 40), ('results_sha256', 64)):
        if type(entry[key]) is not str or not re.fullmatch('[0-9a-f]{%d}' % size, entry[key]):
            raise ProtocolError('invalid reference digest')
    mutants = entry['mutants']
    if type(mutants) is not dict or set(mutants) != set(INVENTORIES[family]):
        raise ProtocolError('missing, extra, or repeated mutant reference')
    for label, ref in mutants.items():
        if type(ref) is not dict or type(ref.get('kind')) is not str:
            raise ProtocolError('invalid mutant reference')
        if ref['kind'] == 'report':
            report = ref.get('report')
            if (set(ref) != {'kind', 'report'} or type(report) is not dict
                    or report.get('mutant') != label or report.get('passed') is not False
                    or type(report.get('checks')) is not dict
                    or not any(v is False for v in report['checks'].values())):
                raise ProtocolError('reference is not a rejection report')
        elif ref['kind'] == 'guard':
            line = ref.get('final_line')
            if (set(ref) != {'kind', 'final_line'} or type(line) is not str
                    or not line or '\n' in line or ': ' not in line):
                raise ProtocolError('invalid guard reference')
        else:
            raise ProtocolError('unknown mutant reference kind')
    return entry


def _check(entry: dict[str, Any], label: str | None, results: bytes,
           returncode: int, stdout: bytes, stderr: bytes) -> bool:
    if label is None:
        return returncode == 0 and stdout == results and bool(TIMING.match(stderr))
    ref = entry['mutants'][label]
    if returncode != 1:
        return False
    if ref['kind'] == 'guard':
        tail = ref['final_line'].encode('utf-8') + b'\n'
        return (not stdout and stderr.startswith(TRACEBACK) and stderr.endswith(b'\n' + tail)
                and b'\nseconds ' not in stderr)
    if not TIMING.match(stderr):
        return False
    try:
        return _same(strict_json(stdout), ref['report'])
    except ProtocolError:
        return False


def replay(family: str, repo: Path, *, timeout: float, workers: int = 4,
           contracts: Path = CONTRACTS) -> list[dict[str, Any]]:
    """Run the complete fixed inventory in both modes, or fail.

    repo is the repository root, the children's working directory as before;
    the packet directory inside it has already been source-verified. A timeout
    or OSError is a failed run, never an intended rejection. No child input,
    packet file or checker is changed.
    """
    entry = _contract(family, contracts)
    repo = Path(repo).resolve()
    root = repo / entry['directory']
    script = root / entry['script']
    if script.is_symlink() or not script.is_file():
        raise ProtocolError('regular source checker required')
    if _blob(script.read_bytes()) != entry['script_git_blob']:
        raise ProtocolError('checker differs from the characterized source')
    results = (root / 'RESULTS.json').read_bytes()
    if (len(results) != entry['results_bytes']
            or hashlib.sha256(results).hexdigest() != entry['results_sha256']):
        raise ProtocolError('RESULTS.json differs from the characterized source')

    def run(mode: str, flags: tuple[str, ...], label: str | None) -> dict[str, Any]:
        command = [sys.executable, *flags, str(script)]
        if label is not None:
            command += ['--mutant', label]
        try:
            child = subprocess.run(command, cwd=repo, capture_output=True, timeout=timeout)
            rc, out, err = child.returncode, child.stdout, child.stderr
        except (subprocess.TimeoutExpired, OSError):
            rc, out, err = None, b'', b''
        ok = rc is not None and _check(entry, label, results, rc, out, err)
        return {'family': family, 'mode': mode, 'label': label, 'returncode': rc,
                'stdout_bytes': len(out), 'stderr_bytes': len(err),
                'stdout_sha256': hashlib.sha256(out).hexdigest(),
                'stderr_sha256': hashlib.sha256(err).hexdigest(), 'protocol_ok': ok}

    records: list[dict[str, Any]] = []
    for mode, flags in MODES:
        labels = [None, *INVENTORIES[family]]
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            batch = list(pool.map(lambda label: run(mode, flags, label), labels))
        for record in batch:
            print(json.dumps(record, sort_keys=True), flush=True)
        for record in batch:
            if not record['protocol_ok']:
                raise ProtocolError('SIDE24 protocol mismatch: %s/%s/%s' %
                                    (family, mode, record['label'] or 'baseline'))
        records.extend(batch)
    return records
