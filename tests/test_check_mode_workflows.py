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
    'c8-theorem-a-constants-planar': 'c8-theorem-a-constants-planar.yml',
    'c8-torus-vanishing-remainder': 'c8-torus-vanishing-remainder.yml',
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
    'c8-theorem-a-constants-planar': ('no-delta', 'cap-half', 'no-zfloor-correction', 'no-om-term'),
    'c8-torus-vanishing-remainder': ('torus-const-only', 'exp-radius', 'no-lin', 'no-om-term', 'coupling-half'),
}
MODES = ('normal', 'optimized')
FLAGS = {'normal': '-B -S', 'optimized': '-B -O -S'}
# The torus wrapper ran one interpreter mode per matrix job, from FLAGS, and its
# checker rejects with one stderr line and nothing on stdout.
PER_JOB = {'c8-torus-vanishing-remainder'}
STDERR = {'c8-torus-vanishing-remainder'}
# The packet files each checker loads besides itself.
LOADED = {'c8-torus-vanishing-remainder': ('theorem_b.py', 'engine_e2.py', 'engine_e3.py')}
VERIFY = '      - name: Verify manifest'
STEP = (
    '      - name: Check trigger coverage and the complete shell rejection contract in both modes\n'
    '        env:\n'
    "          CHECK_MODE_TEST_FAMILY: '%s'\n"
    "          PYTHONDONTWRITEBYTECODE: '1'\n"
    '        run: |\n'
    '          python -B -S ' + SELF + '\n'
    '          python -B -O -S ' + SELF + '\n'
)


def groups(family, job=None):
    """One job's children, as each original wrapper started them.

    A child is (label, mode, checker arguments). The children of one group may
    start in any order, because the wrapper ran them concurrently; a group
    starts only after the previous one. A per-job family's job is its mode.
    """
    labels = ORDERS[family]
    if family == 'c8-cap-failure-coefficient-planar':
        return ([[('baseline', m, ['--check', '--procs', '2'])] for m in MODES]
                + [[(x, m, ['--check', '--procs', '1', '--mutant', x]) for m in MODES for x in labels]])
    if family == 'c8-theorem-a-constants-planar':
        return ([[('baseline', 'normal', ['--check-full', '--procs', '2'])],
                 [('baseline', 'optimized', ['--check', '--procs', '2'])]]
                + [[(x, 'normal', ['--check', '--procs', '2', '--mutant', x])] for x in labels])
    if family == 'c8-torus-vanishing-remainder':
        return [[('baseline', job, ['--check'])], [(x, job, ['--mutant', x]) for x in labels]]
    return [[(x, m, ['--check'] if x == 'baseline' else ['--check', '--mutant', x])]
            for m in MODES for x in ('baseline', *labels)]


def jobs(family):
    return list(MODES) if family in PER_JOB else [None]


def runs(family):
    """Every child of every job, as (label, mode)."""
    return [(x, m) for job in jobs(family) for group in groups(family, job) for x, m, _ in group]


def mutant_runs(family):
    return [(x, m) for x, m in runs(family) if x != 'baseline']


def concurrent(family):
    return any(len(group) > 1 for job in jobs(family) for group in groups(family, job))


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
baselines = BASELINES
reports = REPORTS
expected = EXPECTED
stderr_rejections = STDERR_REJECTIONS
mode = 'optimized' if sys.flags.optimize else 'normal'
label = expected.get(mode, {}).get(tuple(sys.argv[1:]))
if label is None:
    sys.stderr.write('unexpected arguments\n')
    sys.exit(3)
with open(os.environ['CHECK_MODE_TRACE'], 'a') as f:
    f.write(json.dumps([label, mode, os.getcwd()]) + '\n')
value, rc = (baselines[mode], 0) if label == 'baseline' else (reports[label], 1)
on_stderr = label != 'baseline' and stderr_rejections
output, errors = ('', value) if on_stderr else (json.dumps(value) + '\n', '')
if os.environ.get('CHECK_MODE_TARGET') == label and os.environ.get('CHECK_MODE_MODE') == mode:
    kind = os.environ.get('CHECK_MODE_FAULT', '')
    if kind == 'crash':
        raise RuntimeError('unrelated fixture crash')
    if kind == 'silent':
        sys.exit(rc)
    if kind == 'stderr':
        errors += 'unexpected diagnostic\n'
    if kind == 'stdout':
        output += 'unexpected output\n'
    if kind == 'wrong-exit':
        rc = 0 if label != 'baseline' else 1
    if kind == 'wrong-reason':
        if on_stderr:
            errors = 'FAIL: unrelated check failed\n'
        else:
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
sys.stderr.write(errors)
sys.exit(rc)
'''


class CheckModeWorkflowTests(unittest.TestCase):
    maxDiff = None

    def case(self, family, label='baseline', mode='normal', fault='', tamper=None):
        # A wrapper that raises while concurrent children still run (as the old
        # torus wrapper did) can leave them writing here during the cleanup.
        with tempfile.TemporaryDirectory(prefix='check-mode-test-', ignore_cleanup_errors=True) as td:
            outside = Path(td)
            repo = outside / 'repo'
            repo.mkdir()
            trace = outside / 'trace'
            contract = json.loads(json.dumps(CONTRACTS))
            entry = contract['families'][family]
            directory = repo / entry['directory']
            directory.mkdir(parents=True)
            baselines = entry['baselines'] if 'baselines' in entry else {m: entry['baseline'] for m in MODES}
            expected = {}
            for job in jobs(family):
                for group in groups(family, job):
                    for x, m, arguments in group:
                        expected.setdefault(m, {})[tuple(arguments)] = x
            script = (CHILD.replace('BASELINES', repr(baselines)).replace('REPORTS', repr(entry['mutants']))
                      .replace('EXPECTED', repr(expected)).replace('STDERR_REJECTIONS', repr(family in STDERR)))
            data = script.encode()
            loaded = {name: ('# synthetic %s; no scientific authority\n' % name).encode()
                      for name in LOADED.get(family, ())}
            # A rebound source changes with its manifest row, as a pull request
            # would change it, but keeps its characterized reference identity.
            written = dict(loaded, **{entry['script']: data})
            if tamper == 'rebound':
                written[entry['script']] = data + b'# rebound without a new characterization\n'
            if tamper == 'rebound-loaded':
                name = LOADED[family][0]
                written[name] = loaded[name] + b'# rebound without a new characterization\n'
            for name, content in written.items():
                (directory / name).write_bytes(content)
            results = (ROOT / entry['directory'] / 'RESULTS.json').read_bytes()
            (directory / 'RESULTS.json').write_bytes(results)
            upstream = b'synthetic upstream; no scientific authority\n'
            (repo / 'upstream.txt').write_bytes(upstream)
            pin = dict(row('upstream.txt', upstream), current_required=True)
            source_map = json.dumps({'sources': [pin]}).encode()
            (directory / 'SOURCE_MAP.json').write_bytes(source_map)
            files = ([row(name, content) for name, content in sorted(written.items())]
                     + [row('RESULTS.json', results), row('SOURCE_MAP.json', source_map)])
            (directory / 'SOURCE_FILES.json').write_text(json.dumps({'files': files}))
            (repo / 'tools').mkdir()
            for helper in ('check_mode_replay.py', 'legacy_json_replay.py'):
                if (SOURCE / 'tools' / helper).exists():
                    shutil.copyfile(SOURCE / 'tools' / helper, repo / 'tools' / helper)
            entry['script_git_blob'] = blob(data)
            if family in LOADED:
                entry['loaded_git_blobs'] = {name: blob(content) for name, content in loaded.items()}
            # Only the checker identities are re-bound for this synthetic fixture.
            (repo / 'tools/check_mode_contracts.json').write_text(json.dumps(contract))
            env = os.environ.copy()
            env.update({'CHECK_MODE_TRACE': str(trace), 'CHECK_MODE_TARGET': label, 'CHECK_MODE_MODE': mode,
                        'CHECK_MODE_FAULT': fault, 'PYTHONDONTWRITEBYTECODE': '1'})
            if family in PER_JOB:
                # A matrix job: the mode under test is the job's.
                env['FLAGS'] = FLAGS[mode]
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
        if concurrent(family):
            # Children may run at once, so the faulty child need not have started last.
            self.assertIn([label, mode], [event[:2] for event in events], (family, label, mode, fault, events))
            self.assertIn('check-mode protocol mismatch: %s/%s/%s' % (family, mode, label),
                          result.stderr.decode(errors='replace'))
        else:
            self.assertEqual(events[-1][:2], [label, mode],
                             (family, label, mode, fault, events, result.stderr.decode(errors='replace')))

    def test_reference_custody(self):
        canonical = json.dumps(CONTRACTS['families'], sort_keys=True, separators=(',', ':')).encode()
        self.assertEqual(digest(canonical), '30f3b2f43f18082b0b60509747e1525fb84afb1aa8e0db0ac8b9b1818697cd1a')
        for family, entry in ACTIVE.items():
            with self.subTest(family=family):
                packet = ROOT / entry['directory']
                self.assertEqual(blob((packet / entry['script']).read_bytes()), entry['script_git_blob'])
                results = (packet / 'RESULTS.json').read_bytes()
                self.assertEqual((len(results), digest(results)), (entry['results_bytes'], entry['results_sha256']))
                # Every other Python file in the packet is a loaded source, bound like the checker.
                loaded = entry.get('loaded_git_blobs', {})
                self.assertEqual(sorted(loaded), sorted(LOADED.get(family, ())))
                self.assertEqual(sorted(p.name for p in packet.glob('*.py') if p.name != entry['script']),
                                 sorted(loaded))
                for name, git_blob in loaded.items():
                    self.assertEqual(blob((packet / name).read_bytes()), git_blob)

    def test_valid_complete_inventory(self):
        for family in ACTIVE:
            for job in jobs(family):
                with self.subTest(family=family, job=job):
                    result, events, packet = self.case(family, mode=job or 'normal')
                    self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))
                    start = 0
                    for group in groups(family, job):
                        self.assertEqual(sorted(events[start:start + len(group)]),
                                         sorted([x, m, packet] for x, m, _ in group))
                        start += len(group)
                    self.assertEqual(len(events), start)

    def test_formatting_alone_is_accepted(self):
        for family in ACTIVE:
            label = ORDERS[family][0]
            cases = [('baseline', 'optimized')]
            if family not in STDERR:
                cases.append((label, 'optimized' if (label, 'optimized') in runs(family) else 'normal'))
            for label, mode in cases:
                with self.subTest(family=family, label=label, mode=mode):
                    result, _, _ = self.case(family, label, mode, 'format')
                    self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))

    def test_crashes_each_mutant_each_mode(self):
        for family in ACTIVE:
            for label, mode in mutant_runs(family):
                with self.subTest(family=family, label=label, mode=mode):
                    self.rejected(family, label, mode, 'crash')

    def test_silent_exits_each_mutant_each_mode(self):
        for family in ACTIVE:
            for label, mode in mutant_runs(family):
                with self.subTest(family=family, label=label, mode=mode):
                    self.rejected(family, label, mode, 'silent')

    def test_wrong_reasons_each_mutant_each_mode(self):
        for family in ACTIVE:
            for label, mode in mutant_runs(family):
                with self.subTest(family=family, label=label, mode=mode):
                    self.rejected(family, label, mode, 'wrong-reason')

    def test_wrong_mutant_label(self):
        # A stderr rejection names no label, so only JSON verdicts can carry a wrong one.
        for family in ACTIVE:
            if family in STDERR:
                continue
            for label, mode in mutant_runs(family):
                if label == ORDERS[family][0]:
                    with self.subTest(family=family, mode=mode):
                        self.rejected(family, label, mode, 'wrong-label')

    def test_baseline_contract(self):
        for family in ACTIVE:
            for label, mode in runs(family):
                if label != 'baseline':
                    continue
                for fault in ('stderr', 'wrong-value', 'wrong-exit', 'missing', 'malformed'):
                    with self.subTest(family=family, fault=fault, mode=mode):
                        self.rejected(family, label, mode, fault)

    def test_json_contract(self):
        for family in ACTIVE:
            if family in STDERR:
                continue
            for label, mode in mutant_runs(family):
                if label != ORDERS[family][0]:
                    continue
                for fault in ('stderr', 'wrong-exit', 'duplicate', 'nonfinite', 'trailing', 'extra', 'missing',
                              'malformed'):
                    with self.subTest(family=family, fault=fault, mode=mode):
                        self.rejected(family, label, mode, fault)

    def test_stderr_contract(self):
        for family in ACTIVE:
            if family not in STDERR:
                continue
            for label, mode in mutant_runs(family):
                if label != ORDERS[family][0]:
                    continue
                for fault in ('stdout', 'stderr', 'wrong-exit'):
                    with self.subTest(family=family, fault=fault, mode=mode):
                        self.rejected(family, label, mode, fault)

    def test_source_guards_run_before_any_child(self):
        for family in ACTIVE:
            for tamper in ('packet', 'upstream'):
                with self.subTest(family=family, tamper=tamper):
                    result, events, _ = self.case(family, tamper=tamper)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(events, [])

    def test_rebound_sources_need_a_new_characterization(self):
        # The manifest moves with the changed source, so only the reference identities can stop it.
        for family in ACTIVE:
            for tamper in ('rebound', *(('rebound-loaded',) if family in LOADED else ())):
                with self.subTest(family=family, tamper=tamper):
                    result, events, _ = self.case(family, tamper=tamper)
                    self.assertNotEqual(result.returncode, 0, (family, tamper, 'false acceptance', events))
                    self.assertEqual(events, [])
                    self.assertIn('checker differs from the characterized source',
                                  result.stderr.decode(errors='replace'))


class CheckModeTriggerTests(unittest.TestCase):
    def test_paths_cover_the_helper_its_inputs_and_these_tests(self):
        for family, entry in ACTIVE.items():
            paths = trigger_paths(workflow_text(family))
            loaded = [entry['directory'] + '/' + name for name in sorted(entry.get('loaded_git_blobs', {}))]
            for path in (entry['directory'] + '/' + entry['script'], *loaded,
                         '.github/workflows/' + WORKFLOWS[family],
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
                shell = verification_shell(text)
                self.assertNotIn('.returncode', shell)
                self.assertNotIn('.wait(', shell)


if __name__ == '__main__':
    unittest.main()
