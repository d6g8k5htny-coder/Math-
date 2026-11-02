"""Synthetic whole-shell regressions for the SIDE24 d = 5, 6 mutant wrappers.

The fixture commits a synthetic checker, the real RESULTS.json, a manifest and an
upstream pin, then runs the actual verification step of each wrapper with real
subprocesses. The synthetic checker replays the reports measured from the
unchanged checkers (tools/side24_mutant_contracts/). Each named fault must be
rejected and harmless reformatting accepted. Each wrapper's trigger paths, step
order and import line are also checked. This is protocol coverage, not a field
calculation.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

from test_legacy_workflow_triggers import covered, trigger_paths

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.legacy_json_replay import ProtocolError  # noqa: E402
from tools import side24_mutant_replay as helper  # noqa: E402

SELF = 'tests/test_side24_mutant_workflows.py'
SOURCE = Path(os.environ.get('SIDE24_MUTANT_SOURCE_ROOT', str(ROOT)))
CONTRACTS = {f: json.loads((ROOT / 'tools/side24_mutant_contracts' / (f + '.json')).read_text())
             for f in helper.INVENTORIES}
ACTIVE = [f for f in helper.INVENTORIES
          if not os.environ.get('SIDE24_MUTANT_TEST_FAMILY') or f == os.environ['SIDE24_MUTANT_TEST_FAMILY']]
if not ACTIVE:
    raise SystemExit('unknown test family')
MODES = ('normal', 'optimized')
VERIFY = '      - name: Verify sources and pins, replay both modes, reject mutants'
STEP = (
    '      - name: Check trigger coverage and the SIDE24 replay contract in both modes\n'
    '        env:\n'
    "          SIDE24_MUTANT_TEST_FAMILY: '%s'\n"
    "          PYTHONDONTWRITEBYTECODE: '1'\n"
    '        run: |\n'
    '          python -B -S ' + SELF + '\n'
    '          python -B -O -S ' + SELF + '\n'
)
ENCLOSURE = 'coefficients/side24_v1/ENCLOSURE.json'

CHILD = r'''
import builtins, json, os, sys
# QUOTES
here = os.path.dirname(os.path.abspath(__file__))
refs = json.loads(open(os.path.join(here, 'REFERENCES.txt')).read())
args = sys.argv[1:]
if args and not (len(args) == 2 and args[0] == '--mutant'):
    sys.stderr.write('unexpected arguments\n')
    sys.exit(3)
label = args[1] if args else 'baseline'
mode = 'optimized' if sys.flags.optimize else 'normal'
with open(os.environ['SIDE24_TRACE'], 'a') as f:
    f.write(json.dumps([label, mode, os.getcwd()]) + '\n')
kind = os.environ.get('SIDE24_FAULT', '') if (
    os.environ.get('SIDE24_TARGET') == label and os.environ.get('SIDE24_MODE') == mode) else ''
timing = 'seconds 0.1\n'
if kind == 'crash':
    raise RuntimeError('unrelated fixture crash')
if kind == 'silent':
    sys.exit(0 if label == 'baseline' else 1)
if label == 'baseline':
    out = open(os.path.join(here, 'RESULTS.json'), 'rb').read()
    if kind == 'baseline-byte':
        out = out[:-2] + b' \n'
    sys.stdout.buffer.write(out)
    sys.stderr.write(timing + ('unexpected diagnostic\n' if kind == 'stderr' else ''))
    sys.exit(1 if kind == 'wrong-exit' else 0)
ref = refs[label]
if ref['kind'] == 'guard':
    if kind == 'guard-stdout':
        print(json.dumps({'mutant': label, 'passed': False}))
    if kind == 'guard-other':
        raise ValueError('an unrelated failure')
    if kind == 'timing':
        sys.stderr.write(timing)
    name, _, text = ref['final_line'].partition(': ')
    raise getattr(builtins, name)(text)
report = ref['report']
text = json.dumps(report) + '\n'
if kind == 'wrong-value':
    checks = dict(report['checks'])
    first = next(k for k, v in checks.items() if v is False)
    checks[first] = True
    text = json.dumps(dict(report, checks=checks)) + '\n'
if kind == 'wrong-label':
    text = json.dumps(dict(report, mutant='another-mutant')) + '\n'
if kind == 'format':
    text = ' \n' + json.dumps(report, indent=3, sort_keys=True) + '\n\t'
if kind == 'duplicate':
    text = text.rstrip()[:-1] + ', "passed": false}\n'
if kind == 'nonfinite':
    text = text.rstrip()[:-1] + ', "unexpected": NaN}\n'
if kind == 'trailing':
    text += '{}\n'
if kind == 'extra':
    text = json.dumps(dict(report, unexpected='x')) + '\n'
if kind == 'missing':
    text = json.dumps({k: v for k, v in report.items() if k != 'checks'}) + '\n'
if kind == 'malformed':
    text = 'not JSON\n'
sys.stdout.write(text)
sys.stderr.write('' if kind == 'no-timing' else timing + ('unexpected diagnostic\n' if kind == 'stderr' else ''))
sys.exit(2 if kind == 'wrong-exit' else 1)
'''


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def row(path, data):
    return {'path': path, 'bytes': len(data), 'sha256': digest(data), 'git_blob': blob(data)}


def workflow_text(family, source=SOURCE):
    return (source / '.github/workflows' / (family + '.yml')).read_text(encoding='utf-8')


def verification_shell(text):
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(VERIFY))
    start = next(i for i in range(start, len(lines)) if lines[i].strip() == 'run: |') + 1
    end = start
    while end < len(lines) and (not lines[end].strip() or lines[end].startswith('          ')):
        end += 1
    return textwrap.dedent('\n'.join(lines[start:end])) + '\n'


def labels(family, kind):
    return [m for m in helper.INVENTORIES[family] if CONTRACTS[family]['mutants'][m]['kind'] == kind]


class SIDE24WorkflowTests(unittest.TestCase):
    maxDiff = None

    def case(self, family, label='baseline', mode='normal', fault='', tamper=None):
        with tempfile.TemporaryDirectory(prefix='side24-mutant-test-') as td:
            outside = Path(td)
            repo = outside / 'repo'
            trace = outside / 'trace'
            entry = json.loads(json.dumps(CONTRACTS[family]))
            directory = repo / entry['directory']
            directory.mkdir(parents=True)
            enclosure = (ROOT / ENCLOSURE).read_bytes()
            (repo / ENCLOSURE).parent.mkdir(parents=True, exist_ok=True)
            (repo / ENCLOSURE).write_bytes(enclosure)
            dims = json.loads(enclosure)['dimensions']
            quotes = ' '.join('"%s", "%s"' % (dims[d]['lower'], dims[d]['upper']) for d in ('2', '3'))
            data = CHILD.replace('# QUOTES', '# ' + quotes).encode()
            (directory / entry['script']).write_bytes(data)
            results = (ROOT / entry['directory'] / 'RESULTS.json').read_bytes()
            (directory / 'RESULTS.json').write_bytes(results)
            references = json.dumps(entry['mutants']).encode()
            (directory / 'REFERENCES.txt').write_bytes(references)
            upstream = b'synthetic upstream; no scientific authority\n'
            (repo / 'upstream.txt').write_bytes(upstream)
            manifest = {'files': [row(entry['script'], data), row('RESULTS.json', results),
                                  row('REFERENCES.txt', references)],
                        'pins_on_main': [dict(row('upstream.txt', upstream), label='U',
                                              workflow_checked=True)]}
            (directory / 'SOURCE_FILES.json').write_text(json.dumps(manifest))
            (repo / 'tools/side24_mutant_contracts').mkdir(parents=True)
            for name in ('side24_mutant_replay.py', 'legacy_json_replay.py'):
                if (SOURCE / 'tools' / name).exists():
                    shutil.copyfile(SOURCE / 'tools' / name, repo / 'tools' / name)
            # Only the checker identity is re-bound for this synthetic fixture.
            entry['script_git_blob'] = blob(data)
            (repo / 'tools/side24_mutant_contracts' / (family + '.json')).write_text(json.dumps(entry))
            env = os.environ.copy()
            env.update({'SIDE24_TRACE': str(trace), 'SIDE24_TARGET': label, 'SIDE24_MODE': mode,
                        'SIDE24_FAULT': fault, 'PYTHONDONTWRITEBYTECODE': '1'})
            for cmd in (['git', 'init', '-q'], ['git', 'add', '.'],
                        ['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                         '-c', 'commit.gpgsign=false', 'commit', '-qm', 'synthetic fixture']):
                subprocess.run(cmd, cwd=repo, check=True, capture_output=True, timeout=15, env=env)
            if tamper == 'packet':
                (directory / entry['script']).write_bytes(data + b'\n')
            if tamper == 'upstream':
                (repo / 'upstream.txt').write_bytes(upstream + b'x')
            shell = verification_shell(workflow_text(family))
            result = subprocess.run(['bash', '-c', shell], cwd=repo, env=env, capture_output=True, timeout=120)
            events = [json.loads(s) for s in trace.read_text().splitlines()] if trace.exists() else []
            return result, events, str(repo.resolve())

    def rejected(self, family, label, mode, fault):
        result, events, _ = self.case(family, label, mode, fault)
        self.assertNotEqual(result.returncode, 0, (family, label, mode, fault, 'false acceptance'))
        self.assertIn([label, mode], [e[:2] for e in events], (family, label, mode, fault, events))
        if b'SIDE24 protocol mismatch' in result.stderr:
            self.assertIn(('%s/%s/%s' % (family, mode, label)).encode(), result.stderr)

    def test_reference_custody(self):
        for family in ACTIVE:
            entry = helper._contract(family)
            packet = SOURCE / entry['directory']
            with self.subTest(family=family):
                self.assertEqual(blob((packet / entry['script']).read_bytes()), entry['script_git_blob'])
                results = (packet / 'RESULTS.json').read_bytes()
                self.assertEqual((len(results), digest(results)), (entry['results_bytes'], entry['results_sha256']))

    def test_valid_complete_inventory(self):
        for family in ACTIVE:
            with self.subTest(family=family):
                result, events, repo = self.case(family)
                self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))
                expected = [[label, mode, repo] for mode in MODES
                            for label in ['baseline', *helper.INVENTORIES[family]]]
                self.assertEqual(sorted(events), sorted(expected))
                self.assertEqual([e[1] for e in events], [e[1] for e in expected])

    def test_formatting_alone_is_accepted(self):
        for family in ACTIVE:
            label = labels(family, 'report')[0]
            with self.subTest(family=family):
                result, _, _ = self.case(family, label, 'optimized', 'format')
                self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))

    def test_crashes_each_mutant_each_mode(self):
        for family in ACTIVE:
            for label in helper.INVENTORIES[family]:
                for mode in MODES:
                    with self.subTest(family=family, label=label, mode=mode):
                        self.rejected(family, label, mode, 'crash')

    def test_silent_exits_and_wrong_verdicts(self):
        for family in ACTIVE:
            first, last = labels(family, 'report')[0], labels(family, 'report')[-1]
            for label, fault in ((first, 'silent'), (last, 'silent'), (first, 'wrong-value'),
                                 (last, 'wrong-value'), (first, 'wrong-label')):
                for mode in MODES:
                    with self.subTest(family=family, label=label, fault=fault, mode=mode):
                        self.rejected(family, label, mode, fault)

    def test_report_contract(self):
        for family in ACTIVE:
            label = labels(family, 'report')[0]
            for fault in ('stderr', 'no-timing', 'wrong-exit', 'duplicate', 'nonfinite', 'trailing', 'extra',
                          'missing', 'malformed'):
                for mode in MODES:
                    with self.subTest(family=family, fault=fault, mode=mode):
                        self.rejected(family, label, mode, fault)

    def test_guard_contract(self):
        for family in ACTIVE:
            for label in labels(family, 'guard'):
                for fault in ('guard-other', 'guard-stdout', 'timing', 'silent'):
                    for mode in MODES:
                        with self.subTest(family=family, label=label, fault=fault, mode=mode):
                            self.rejected(family, label, mode, fault)

    def test_baseline_contract(self):
        for family in ACTIVE:
            for fault in ('baseline-byte', 'stderr', 'wrong-exit', 'crash', 'silent'):
                for mode in MODES:
                    with self.subTest(family=family, fault=fault, mode=mode):
                        self.rejected(family, 'baseline', mode, fault)

    def test_source_guards_run_before_any_child(self):
        for family in ACTIVE:
            for tamper in ('packet', 'upstream'):
                with self.subTest(family=family, tamper=tamper):
                    result, events, _ = self.case(family, tamper=tamper)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(events, [])


class HelperTests(unittest.TestCase):
    def test_timeout_is_a_failure(self):
        family = ACTIVE[0]
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            entry = CONTRACTS[family]
            packet = repo / entry['directory']
            packet.mkdir(parents=True)
            data = b'import time\ntime.sleep(5)\n'
            (packet / entry['script']).write_bytes(data)
            results = b'{}\n'
            (packet / 'RESULTS.json').write_bytes(results)
            refs = repo / 'refs'
            refs.mkdir()
            (refs / (family + '.json')).write_text(json.dumps(dict(
                entry, script_git_blob=blob(data), results_bytes=len(results), results_sha256=digest(results))))
            with self.assertRaisesRegex(ProtocolError, 'protocol mismatch: %s/normal/' % family):
                helper.replay(family, repo, timeout=1, contracts=refs)

    def test_reference_schema(self):
        family = ACTIVE[0]
        data = CONTRACTS[family]
        report = labels(family, 'report')[0]
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            bad = path / (family + '.json')
            entry = dict(data, mutants=dict(data['mutants']))
            entry['mutants'].pop(report)
            bad.write_text(json.dumps(entry))
            with self.assertRaisesRegex(ProtocolError, 'missing, extra'):
                helper._contract(family, path)
            entry['mutants'] = dict(data['mutants'])
            entry['mutants'][report] = {'kind': 'report',
                                        'report': dict(data['mutants'][report]['report'], passed=True)}
            bad.write_text(json.dumps(entry))
            with self.assertRaisesRegex(ProtocolError, 'not a rejection report'):
                helper._contract(family, path)
            other = next(f for f in helper.INVENTORIES if f != family)
            bad.write_text(json.dumps(dict(data, family=other)))
            with self.assertRaisesRegex(ProtocolError, 'family reference schema'):
                helper._contract(family, path)
            bad.write_text(json.dumps(data)[:-1] + ', "schema": 1}')
            with self.assertRaises(ProtocolError):
                helper._contract(family, path)


class SIDE24TriggerTests(unittest.TestCase):
    def test_paths_cover_the_helper_its_inputs_and_these_tests(self):
        for family in ACTIVE:
            paths = trigger_paths(workflow_text(family))
            entry = CONTRACTS[family]
            for path in (entry['directory'] + '/' + entry['script'], '.github/workflows/%s.yml' % family,
                         'tools/side24_mutant_replay.py', 'tools/side24_mutant_contracts/%s.json' % family,
                         'tools/legacy_json_replay.py', 'tools/__init__.py', 'tools.py', SELF,
                         'tests/test_legacy_workflow_triggers.py'):
                with self.subTest(family=family, path=path):
                    self.assertTrue(covered(paths, path), 'consumed or regression path is uncovered')

    def test_contract_step_runs_in_both_modes_before_the_replay(self):
        for family in ACTIVE:
            text = workflow_text(family)
            with self.subTest(family=family):
                step = STEP % family
                self.assertEqual(text.count(step), 1)
                self.assertLess(text.index(step), text.index(VERIFY))

    def test_the_replay_is_the_only_mutant_path_and_names_its_family(self):
        for family in ACTIVE:
            shell = verification_shell(workflow_text(family))
            with self.subTest(family=family):
                lines = [line for line in shell.splitlines() if 'side24_mutant_replay' in line]
                self.assertEqual(lines, ['from tools.side24_mutant_replay import replay'])
                self.assertEqual(shell.count("replay('%s', pathlib.Path.cwd(), timeout=" % family), 1)
                self.assertNotIn('.returncode', shell)
                self.assertNotIn('--mutant', shell)
                self.assertLess(shell.index('pins_on_main'), shell.index('import replay'))


if __name__ == '__main__':
    unittest.main()
