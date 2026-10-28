"""Synthetic whole-shell regressions for the C8 check-mode wrappers.

The fixture commits synthetic source, manifest and upstream bytes, then runs the
actual verification step of each wrapper with real subprocesses and the measured
verdicts from tools/check_mode_contracts.json. It also checks each wrapper's
trigger paths, step order and import line. This is protocol coverage, not a
field calculation.
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
SELF = 'tests/test_check_mode_workflows.py'
SOURCE = Path(os.environ.get('CHECK_MODE_SOURCE_ROOT', str(ROOT)))
CONTRACTS = json.loads((ROOT / 'tools/check_mode_contracts.json').read_text())
WORKFLOWS = {
    'c8-cap-failure-coefficient-dims': 'c8-cap-failure-coefficient-dims.yml',
    'c8-normalizer-floor-planar': 'c8-normalizer-floor-planar.yml',
    'c8-cap-failure-coefficient-planar': 'c8-cap-failure-coefficient-planar.yml',
}
ACTIVE = {k: v for k, v in CONTRACTS['families'].items()
          if not os.environ.get('CHECK_MODE_TEST_FAMILY') or k == os.environ['CHECK_MODE_TEST_FAMILY']}
if not ACTIVE:
    raise SystemExit('unknown test family')
# Mutant order within each mode, as in each wrapper's original loop.
ORDERS = {
    'c8-cap-failure-coefficient-dims': ('no-y-tail', 'r3-one', 'no-bp', 'frob-omega-off'),
    'c8-normalizer-floor-planar': ('swap-minmax', 'drop-torus-error', 'sign-saddle'),
    'c8-cap-failure-coefficient-planar': ('no-third-jet', 'sign-lo', 'variance-yyy'),
}
# Extra checker arguments each original wrapper passed, for the baseline and
# for each mutant. A pooled wrapper ran both baselines first and then its
# mutants concurrently, so the mutants may start in any order.
EXTRA = {'c8-cap-failure-coefficient-planar': (['--procs', '2'], ['--procs', '1'])}
POOLED = {'c8-cap-failure-coefficient-planar'}
MODES = ('normal', 'optimized')
VERIFY = '      - name: Verify manifest and main-resident pins'
STEP = (
    '      - name: Check trigger coverage and the complete shell rejection contract in both modes\n'
    '        env:\n'
    "          CHECK_MODE_TEST_FAMILY: '%s'\n"
    "          PYTHONDONTWRITEBYTECODE: '1'\n"
    '        run: |\n'
    '          python -B -S ' + SELF + '\n'
    '          python -B -O -S ' + SELF + '\n'
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def row(path, data):
    return {'path': path, 'bytes': len(data), 'sha256': digest(data), 'git_blob': blob(data)}


def workflow_text(family, source=SOURCE):
    return (source / '.github/workflows' / WORKFLOWS[family]).read_text(encoding='utf-8')


def verification_shell(text):
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(VERIFY))
    start = next(i for i in range(start, len(lines)) if lines[i].strip() == 'run: |') + 1
    end = start
    while end < len(lines) and (not lines[end].strip() or lines[end].startswith('          ')):
        end += 1
    return textwrap.dedent('\n'.join(lines[start:end])) + '\n'


CHILD = r'''
import json, os, sys
baseline = BASELINE
reports = REPORTS
extra_baseline, extra_mutant = EXTRA_ARGS
args = sys.argv[1:]
if args == ['--check', *extra_baseline]:
    label = 'baseline'
elif len(args) == len(extra_mutant) + 3 and args[:-2] == ['--check', *extra_mutant] and args[-2] == '--mutant':
    label = args[-1]
else:
    sys.stderr.write('unexpected arguments\n')
    sys.exit(3)
mode = 'optimized' if sys.flags.optimize else 'normal'
with open(os.environ['CHECK_MODE_TRACE'], 'a') as f:
    f.write(json.dumps([label, mode, os.getcwd()]) + '\n')
value, rc = (baseline, 0) if label == 'baseline' else (reports[label], 1)
output = json.dumps(value) + '\n'
if os.environ.get('CHECK_MODE_TARGET') == label and os.environ.get('CHECK_MODE_MODE') == mode:
    kind = os.environ.get('CHECK_MODE_FAULT', '')
    if kind == 'crash':
        raise RuntimeError('unrelated fixture crash')
    if kind == 'silent':
        sys.exit(rc)
    if kind == 'stderr':
        sys.stderr.write('unexpected diagnostic\n')
    if kind == 'wrong-exit':
        rc = 0 if label != 'baseline' else 1
    if kind == 'wrong-reason':
        output = json.dumps(dict(value, reason='unrelated check failed')) + '\n'
    if kind == 'wrong-label':
        output = json.dumps(dict(value, mutant='another-mutant')) + '\n'
    if kind == 'wrong-value':
        name = next(k for k in value if k not in ('check', 'mutant'))
        output = json.dumps(dict(value, **{name: 'unrelated value'})) + '\n'
    if kind == 'format':
        output = ' \n' + json.dumps(value, indent=4, sort_keys=True) + '\n\t'
    if kind == 'duplicate':
        output = output.rstrip()[:-1] + ', "check": ' + json.dumps(value['check']) + '}\n'
    if kind == 'nonfinite':
        output = output.rstrip()[:-1] + ', "unexpected": NaN}\n'
    if kind == 'trailing':
        output += '{}\n'
    if kind == 'extra':
        output = json.dumps(dict(value, unexpected='x')) + '\n'
    if kind == 'missing':
        output = json.dumps({k: v for k, v in value.items() if k != 'check'}) + '\n'
    if kind == 'malformed':
        output = 'not JSON\n'
sys.stdout.write(output)
sys.exit(rc)
'''


class CheckModeWorkflowTests(unittest.TestCase):
    maxDiff = None

    def case(self, family, label='baseline', mode='normal', fault='', tamper=None):
        with tempfile.TemporaryDirectory(prefix='check-mode-test-') as td:
            outside = Path(td)
            repo = outside / 'repo'
            repo.mkdir()
            trace = outside / 'trace'
            contract = json.loads(json.dumps(CONTRACTS))
            entry = contract['families'][family]
            directory = repo / entry['directory']
            directory.mkdir(parents=True)
            script = (CHILD.replace('BASELINE', repr(entry['baseline'])).replace('REPORTS', repr(entry['mutants']))
                      .replace('EXTRA_ARGS', repr(EXTRA.get(family, ([], [])))))
            data = script.encode()
            (directory / entry['script']).write_bytes(data)
            results = (ROOT / entry['directory'] / 'RESULTS.json').read_bytes()
            (directory / 'RESULTS.json').write_bytes(results)
            upstream = b'synthetic upstream; no scientific authority\n'
            (repo / 'upstream.txt').write_bytes(upstream)
            pin = dict(row('upstream.txt', upstream), current_required=True)
            source_map = json.dumps({'sources': [pin]}).encode()
            (directory / 'SOURCE_MAP.json').write_bytes(source_map)
            files = [row(entry['script'], data), row('RESULTS.json', results), row('SOURCE_MAP.json', source_map)]
            (directory / 'SOURCE_FILES.json').write_text(json.dumps({'files': files}))
            (repo / 'tools').mkdir()
            for helper in ('check_mode_replay.py', 'legacy_json_replay.py'):
                if (SOURCE / 'tools' / helper).exists():
                    shutil.copyfile(SOURCE / 'tools' / helper, repo / 'tools' / helper)
            entry['script_git_blob'] = blob(data)
            # Only the checker identity is re-bound for this synthetic fixture.
            (repo / 'tools/check_mode_contracts.json').write_text(json.dumps(contract))
            env = os.environ.copy()
            env.update({'CHECK_MODE_TRACE': str(trace), 'CHECK_MODE_TARGET': label, 'CHECK_MODE_MODE': mode,
                        'CHECK_MODE_FAULT': fault, 'PYTHONDONTWRITEBYTECODE': '1'})
            for cmd in (['git', 'init', '-q'], ['git', 'add', '.'],
                        ['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                         '-c', 'commit.gpgsign=false', 'commit', '-qm', 'synthetic fixture']):
                subprocess.run(cmd, cwd=repo, check=True, capture_output=True, timeout=15, env=env)
            if tamper == 'packet':
                (directory / entry['script']).write_bytes(data + b'\n')
            if tamper == 'upstream':
                (repo / 'upstream.txt').write_bytes(upstream + b'x')
            shell = verification_shell(workflow_text(family))
            result = subprocess.run(['bash', '-c', shell], cwd=repo, env=env, capture_output=True, timeout=90)
            events = [json.loads(s) for s in trace.read_text().splitlines()] if trace.exists() else []
            return result, events, str(directory.resolve())

    def rejected(self, family, label, mode, fault):
        result, events, _ = self.case(family, label, mode, fault)
        self.assertNotEqual(result.returncode, 0, (family, label, mode, fault, 'false acceptance', events))
        if family in POOLED:
            # Two mutants may run at once, so the faulty child need not have started last.
            self.assertIn([label, mode], [event[:2] for event in events], (family, label, mode, fault, events))
            self.assertIn('check-mode protocol mismatch: %s/%s/%s' % (family, mode, label),
                          result.stderr.decode(errors='replace'))
        else:
            self.assertEqual(events[-1][:2], [label, mode],
                             (family, label, mode, fault, events, result.stderr.decode(errors='replace')))

    def test_reference_custody(self):
        canonical = json.dumps(CONTRACTS['families'], sort_keys=True, separators=(',', ':')).encode()
        self.assertEqual(digest(canonical), '75133e1782b3dd8d61dc76c40478ab5886ea6ecf7f97642ad49c2d0e596809a8')
        for family, entry in ACTIVE.items():
            with self.subTest(family=family):
                packet = ROOT / entry['directory']
                self.assertEqual(blob((packet / entry['script']).read_bytes()), entry['script_git_blob'])
                results = (packet / 'RESULTS.json').read_bytes()
                self.assertEqual((len(results), digest(results)), (entry['results_bytes'], entry['results_sha256']))

    def test_valid_complete_inventory(self):
        for family in ACTIVE:
            with self.subTest(family=family):
                result, events, packet = self.case(family)
                self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))
                if family in POOLED:
                    self.assertEqual(events[:2], [['baseline', mode, packet] for mode in MODES])
                    self.assertEqual(sorted(events[2:]),
                                     sorted([label, mode, packet] for mode in MODES for label in ORDERS[family]))
                else:
                    labels = ['baseline', *ORDERS[family]]
                    self.assertEqual(events, [[label, mode, packet] for mode in MODES for label in labels])

    def test_formatting_alone_is_accepted(self):
        for family in ACTIVE:
            for label in ('baseline', ORDERS[family][0]):
                with self.subTest(family=family, label=label):
                    result, _, _ = self.case(family, label, 'optimized', 'format')
                    self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))

    def test_crashes_each_mutant_each_mode(self):
        for family in ACTIVE:
            for label in ORDERS[family]:
                for mode in MODES:
                    with self.subTest(family=family, label=label, mode=mode):
                        self.rejected(family, label, mode, 'crash')

    def test_silent_exits_each_mutant_each_mode(self):
        for family in ACTIVE:
            for label in ORDERS[family]:
                for mode in MODES:
                    with self.subTest(family=family, label=label, mode=mode):
                        self.rejected(family, label, mode, 'silent')

    def test_wrong_reasons_each_mutant_each_mode(self):
        for family in ACTIVE:
            for label in ORDERS[family]:
                for mode in MODES:
                    with self.subTest(family=family, label=label, mode=mode):
                        self.rejected(family, label, mode, 'wrong-reason')

    def test_wrong_mutant_label(self):
        for family in ACTIVE:
            for mode in MODES:
                with self.subTest(family=family, mode=mode):
                    self.rejected(family, ORDERS[family][0], mode, 'wrong-label')

    def test_baseline_contract(self):
        for family in ACTIVE:
            for fault in ('stderr', 'wrong-value', 'wrong-exit', 'missing', 'malformed'):
                for mode in MODES:
                    with self.subTest(family=family, fault=fault, mode=mode):
                        self.rejected(family, 'baseline', mode, fault)

    def test_json_contract(self):
        for family in ACTIVE:
            label = ORDERS[family][0]
            for fault in ('stderr', 'wrong-exit', 'duplicate', 'nonfinite', 'trailing', 'extra', 'missing',
                          'malformed'):
                for mode in MODES:
                    with self.subTest(family=family, fault=fault, mode=mode):
                        self.rejected(family, label, mode, fault)

    def test_source_guards_run_before_any_child(self):
        for family in ACTIVE:
            for tamper in ('packet', 'upstream'):
                with self.subTest(family=family, tamper=tamper):
                    result, events, _ = self.case(family, tamper=tamper)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(events, [])


class CheckModeTriggerTests(unittest.TestCase):
    def test_paths_cover_the_helper_its_inputs_and_these_tests(self):
        for family, entry in ACTIVE.items():
            paths = trigger_paths(workflow_text(family))
            for path in (entry['directory'] + '/' + entry['script'], '.github/workflows/' + WORKFLOWS[family],
                         'tools/check_mode_replay.py', 'tools/check_mode_contracts.json',
                         'tools/legacy_json_replay.py', 'tools/__init__.py', 'tools.py', SELF,
                         'tests/test_legacy_workflow_triggers.py'):
                with self.subTest(family=family, path=path):
                    self.assertTrue(covered(paths, path), 'consumed or regression path is uncovered')
            for path in ('README.md', 'unrelated/tools.py', 'tools_extra/file.py'):
                with self.subTest(family=family, unrelated=path):
                    self.assertFalse(covered(paths, path), 'unexpected unrelated trigger')

    def test_contract_step_runs_in_both_modes_before_the_replay(self):
        for family in ACTIVE:
            text = workflow_text(family)
            with self.subTest(family=family):
                step = STEP % family
                self.assertEqual(text.count(step), 1, 'missing exact two-mode contract step')
                self.assertLess(text.index(step), text.index(VERIFY))

    def test_the_replay_is_the_only_import_and_names_its_family(self):
        for family in ACTIVE:
            text = workflow_text(family)
            with self.subTest(family=family):
                lines = [s.strip() for s in text.splitlines() if s.strip().startswith('from tools.')]
                self.assertEqual(lines, ['from tools.check_mode_replay import replay'])
                self.assertEqual(text.count("replay('%s', root" % family), 1)
                # No exit-status-only check of a child remains beside the replay.
                self.assertNotIn('.returncode', verification_shell(text))


if __name__ == '__main__':
    unittest.main()
