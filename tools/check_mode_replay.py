#!/usr/bin/env python3
"""Authenticate the C8 check-mode checkers' acceptance and rejection verdicts.

Called AFTER each workflow's unchanged source and pin guards. Each checker runs
from its packet directory with the arguments its original wrapper passed, and
reports one verdict. Most print one JSON verdict on stdout: {"check": "ok", ...}
with exit 0, or, from their require(), {"check": "FAIL", "reason": ...,
"mutant": LABEL} with exit 1. The families in STDERR_REJECTIONS print a JSON
success line whose "check" is "passed", and reject with exit 1, nothing on
stdout and the one line "FAIL: <reason>" on stderr. The reference file holds
complete verdicts measured from the unchanged checkers, never outputs learned
from the invocation being tested, with the identities of each checker, the
packet files it loads (LOADS) and its RESULTS.json. Parsing and comparison are
those of tools/legacy_json_replay.py: formatting may differ, but every key,
type, value and list must match, and a stderr rejection must match byte for
byte. This is an engineering protocol, not a sandbox or mathematical acceptance
test.
"""
from __future__ import annotations

import concurrent.futures
import functools
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
    'c8-cap-failure-coefficient-planar': ('no-third-jet', 'sign-lo', 'variance-yyy'),
    'c8-theorem-a-constants-planar': ('no-delta', 'cap-half', 'no-zfloor-correction', 'no-om-term'),
    'c8-torus-vanishing-remainder': ('torus-const-only', 'exp-radius', 'no-lin', 'no-om-term', 'coupling-half'),
}
MODES = (('normal', ('-B', '-S')), ('optimized', ('-B', '-O', '-S')))
# Families whose original wrapper passed extra checker arguments and ran its
# mutants concurrently. As there, both baselines run first, one at a time, and
# then every mutant of both modes runs on `workers` threads; verdicts are read
# in submission order. Every other family not in PLANNED runs each mode's
# inventory in turn.
POOLED = {
    'c8-cap-failure-coefficient-planar': {'baseline': ('--procs', '2'), 'mutant': ('--procs', '1'), 'workers': 2},
}
# Families whose original wrapper ran another child list, restated by _plan()
# with each child's arguments and timeout. Their reference file holds one
# baseline verdict per mode. PER_JOB_MODE families ran one interpreter mode per
# matrix job; replay() then takes that job's flags.
PLANNED = ('c8-theorem-a-constants-planar', 'c8-torus-vanishing-remainder')
PER_JOB_MODE = {'c8-torus-vanishing-remainder'}
STDERR_REJECTIONS = {'c8-torus-vanishing-remainder'}
# Packet files a checker loads besides itself. The reference file binds them
# like the checker, so a change to any of them needs a new characterization.
LOADS = {'c8-torus-vanishing-remainder': ('theorem_b.py', 'engine_e2.py', 'engine_e3.py')}


def _plan(family: str,
          modes: tuple[str, ...]) -> list[tuple[int, list[tuple[str, str | None, tuple[str, ...], float]]]]:
    """Return the stages (workers, children); a child is (mode, label, arguments, timeout)."""
    labels = INVENTORIES[family]
    if family == 'c8-theorem-a-constants-planar':
        # One at a time: every band with --check-full in normal mode, the
        # sampled --check in optimized mode, then each mutant in normal mode only.
        return [(1, [('normal', None, ('--check-full', '--procs', '2'), 3600),
                     ('optimized', None, ('--check', '--procs', '2'), 3600),
                     *[('normal', m, ('--check', '--procs', '2', '--mutant', m), 1800) for m in labels]])]
    if family == 'c8-torus-vanishing-remainder':
        # In each job: the baseline, then all five mutants at once, which take
        # no --check.
        stages: list[tuple[int, list[tuple[str, str | None, tuple[str, ...], float]]]] = []
        for mode in modes:
            stages += [(1, [(mode, None, ('--check',), 3600)]),
                       (len(labels), [(mode, m, ('--mutant', m), 3600) for m in labels])]
        return stages
    raise ProtocolError('unknown checker family')


def _accepts(family: str, report: Any) -> bool:
    if family in STDERR_REJECTIONS:
        return type(report) is dict and report.get('check') == 'passed'
    return type(report) is dict and report.get('check') == 'ok' and report.get('mutant', '') is None


def _rejects(family: str, label: str, report: Any) -> bool:
    if family in STDERR_REJECTIONS:
        return (type(report) is str and report.startswith('FAIL: ') and report.endswith('\n')
                and report.count('\n') == 1)
    return (type(report) is dict and set(report) == {'check', 'reason', 'mutant'}
            and report['check'] == 'FAIL' and report['mutant'] == label and type(report['reason']) is str)


def _contract(family: str) -> dict[str, Any]:
    if (family not in INVENTORIES or not set(POOLED) <= set(INVENTORIES)
            or not set(PLANNED) <= set(INVENTORIES) or set(POOLED) & set(PLANNED)
            or not set(LOADS) <= set(INVENTORIES)):
        raise ProtocolError('unknown checker family')
    data = strict_json(Path(__file__).with_name('check_mode_contracts.json').read_bytes())
    if (type(data) is not dict or type(data.get('schema')) is not int
            or data['schema'] != 1 or type(data.get('families')) is not dict
            or set(data['families']) != set(INVENTORIES)):
        raise ProtocolError('invalid reference inventory')
    entry = data['families'][family]
    keys = {'directory', 'script', 'script_git_blob', 'results_sha256', 'results_bytes', 'mutants',
            'baselines' if family in PLANNED else 'baseline'}
    if family in LOADS:
        keys.add('loaded_git_blobs')
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
    if family in LOADS:
        loaded = entry['loaded_git_blobs']
        if (type(loaded) is not dict or set(loaded) != set(LOADS[family])
                or not all(Path(name).name == name for name in loaded)):
            raise ProtocolError('invalid script or results metadata')
        if not all(type(value) is str and re.fullmatch('[0-9a-f]{40}', value) for value in loaded.values()):
            raise ProtocolError('invalid reference digest')
    if family in PLANNED:
        baselines = entry['baselines']
        if (type(baselines) is not dict or set(baselines) != {name for name, _ in MODES}
                or not all(_accepts(family, report) for report in baselines.values())):
            raise ProtocolError('reference is not an acceptance verdict')
    elif not _accepts(family, entry['baseline']):
        raise ProtocolError('reference is not an acceptance verdict')
    if (type(entry['mutants']) is not dict
            or set(entry['mutants']) != set(INVENTORIES[family])):
        raise ProtocolError('missing, extra, or repeated mutant reference')
    for label, report in entry['mutants'].items():
        if not _rejects(family, label, report):
            raise ProtocolError('reference is not a rejection verdict')
    return entry


def _child(family: str, root: Path, script: Path, mode: str, flags: tuple[str, ...], label: str | None,
           arguments: tuple[str, ...], timeout: float, reference: Any) -> dict[str, Any]:
    command = [sys.executable, *flags, str(script), *arguments]
    child = subprocess.run(command, cwd=root, capture_output=True, timeout=timeout)
    record = {'family': family, 'mode': mode, 'label': label,
              'returncode': child.returncode,
              'stdout_bytes': len(child.stdout), 'stderr_bytes': len(child.stderr),
              'stdout_sha256': hashlib.sha256(child.stdout).hexdigest(),
              'stderr_sha256': hashlib.sha256(child.stderr).hexdigest()}
    if label is not None and family in STDERR_REJECTIONS:
        ok = child.returncode == 1 and not child.stdout and child.stderr == reference.encode()
    else:
        ok = child.returncode == (0 if label is None else 1) and not child.stderr
        if ok:
            try:
                ok = _same(strict_json(child.stdout), reference)
            except ProtocolError:
                ok = False
    record['protocol_ok'] = ok
    return record


def _stage(workers: int, calls: list[Any], accept: Any) -> None:
    """Run the calls at most `workers` at a time; read verdicts in submission order."""
    if workers == 1:
        for call in calls:
            accept(call())
        return
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(call) for call in calls]
        try:
            for future in futures:
                accept(future.result())
        except BaseException:
            for future in futures:
                future.cancel()
            raise


def replay(family: str, root: Path, *, timeout: float | None = None,
           flags: list[str] | tuple[str, ...] | None = None) -> list[dict[str, Any]]:
    """Run the complete fixed inventory, or fail immediately.

    root is the already source-verified packet directory, and also each child's
    working directory, as the checkers expect. Timeout/OSError is a failed run,
    never an intended negative-control receipt. All child inputs stay
    unchanged; no synthetic output, package rehash, or checker amendment occurs.
    A concurrent stage stops at the first failing verdict too; children already
    running finish, and children not yet started are cancelled. A PLANNED
    family's timeouts are fixed by its plan; a PER_JOB_MODE family takes its
    job's interpreter flags and runs that mode only.
    """
    entry = _contract(family)
    if family in PLANNED and timeout is not None:
        raise ProtocolError('this family plan fixes its own timeouts')
    job_modes: tuple[str, ...] = ()
    if family in PER_JOB_MODE:
        job_modes = tuple(name for name, mode_flags in MODES if flags is not None and tuple(flags) == mode_flags)
        if len(job_modes) != 1:
            raise ProtocolError('this family runs one interpreter mode per job')
    elif flags is not None:
        raise ProtocolError('this family runs both interpreter modes in one job')
    root = Path(root).resolve()
    script = root / entry['script']
    if script.is_symlink() or not script.is_file():
        raise ProtocolError('regular source checker required')
    data = script.read_bytes()
    if hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest() != entry['script_git_blob']:
        raise ProtocolError('checker differs from the characterized source')
    for name, git_blob in sorted(entry.get('loaded_git_blobs', {}).items()):
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise ProtocolError('regular source checker required')
        loaded = path.read_bytes()
        if hashlib.sha1(b'blob %d\0' % len(loaded) + loaded).hexdigest() != git_blob:
            raise ProtocolError('checker differs from the characterized source')
    results = (root / 'RESULTS.json').read_bytes()
    if (len(results) != entry['results_bytes']
            or hashlib.sha256(results).hexdigest() != entry['results_sha256']):
        raise ProtocolError('RESULTS.json differs from the characterized source')
    records: list[dict[str, Any]] = []
    flags_of = dict(MODES)

    def accept(record: dict[str, Any]) -> None:
        print(json.dumps(record, sort_keys=True), flush=True)
        if not record['protocol_ok']:
            raise ProtocolError('check-mode protocol mismatch: %s/%s/%s' %
                                (family, record['mode'], record['label'] or 'baseline'))
        records.append(record)

    def call(mode: str, label: str | None, arguments: tuple[str, ...], seconds: float) -> Any:
        if label is not None:
            reference = entry['mutants'][label]
        else:
            reference = entry['baselines'][mode] if family in PLANNED else entry['baseline']
        return functools.partial(_child, family, root, script, mode, flags_of[mode], label, arguments, seconds,
                                 reference)

    if family in PLANNED:
        for workers, children in _plan(family, job_modes):
            _stage(workers, [call(*child) for child in children], accept)
        return records
    seconds = 1500 if timeout is None else timeout
    pooled = POOLED.get(family)
    if pooled is None:
        for mode, _ in MODES:
            _stage(1, [call(mode, None, ('--check',), seconds)]
                   + [call(mode, m, ('--check', '--mutant', m), seconds) for m in INVENTORIES[family]], accept)
        return records
    for mode, _ in MODES:
        _stage(1, [call(mode, None, ('--check', *pooled['baseline']), seconds)], accept)
    _stage(pooled['workers'], [call(mode, m, ('--check', *pooled['mutant'], '--mutant', m), seconds)
                               for mode, _ in MODES for m in INVENTORIES[family]], accept)
    return records
