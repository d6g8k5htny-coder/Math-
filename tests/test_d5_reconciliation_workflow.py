"""Real-shell d5-reconciliation protocol tests with committed SYNTHETIC fixtures.

No mathematical packet is replayed here. Real checker children record their
interpreter flags; the full workflow block retains its source and Git guards.
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
import unittest

WORKFLOW = Path(__file__).resolve().parents[1] / '.github/workflows/d5-reconciliation.yml'
PACKET = Path('reviews/d5_reconciliation_20260929')
# Characterized from reconciliation_check.py and RESULTS.json; native replay is separate.
# Labels sharing a check intentionally share report bytes; event traces bind
# every actual invocation independently of those equivalent reports.
FAILED_CHECKS = {
    'optional-continuum': 'NEGATIVES',
    'allow-symlink': 'NEGATIVES',
    'no-hash': 'NEGATIVES',
    'drop-dependency': 'TRANSITIONS',
    'drop-edge': 'TRANSITIONS',
    'stale-fingerprint': 'TRANSITIONS',
    'drop-collar': 'TILING',
    'close-c6': 'OPEN_C6',
}
LABELS = tuple(FAILED_CHECKS)
BASELINE = {
    'checks': {'IDENTITIES': True, 'NEGATIVES': True, 'OPEN_C6': True,
               'TILING': True, 'TRANSITIONS': True, 'VERDICTS': True},
    'inventory_files': 17,
    'object': 'SYNTHETIC-D5-RECONCILIATION-PROTOCOL-FIXTURE',
    'passed': True,
    'scope': 'SYNTHETIC workflow fixture only; no mathematical assertion',
}

# This is a real child process, never a mocked subprocess API or interpreter.
CHILD = r'''import json, os, pathlib, sys
label = sys.argv[-1] if '--mutant' in sys.argv else 'baseline'
with open(os.environ['RECONCILIATION_EVENTS'], 'a', encoding='utf-8') as stream:
    stream.write(json.dumps([label, sys.flags.optimize, sys.flags.no_site, sys.dont_write_bytecode])+'\n')
selected = label == os.environ.get('RECONCILIATION_TARGET') and str(sys.flags.optimize) == os.environ.get('RECONCILIATION_MODE')
kind = os.environ.get('RECONCILIATION_KIND', 'valid') if selected else 'valid'
if kind == 'crash': raise RuntimeError('synthetic unrelated crash')
if kind == 'silent': sys.exit(1)
if kind == 'wrong-stdout': print('{}'); sys.exit(1)
if kind == 'baseline-wrong': print('synthetic wrong bytes'); sys.exit(0)
value = json.loads((pathlib.Path(__file__).parent/'RESULTS.json').read_bytes())
key = FAILED_CHECKS.get(label)
if key is not None:
    value['passed'] = False
    value['checks'][key] = False
    if kind == 'wrong-check':
        value['checks'][key] = True
        value['checks']['IDENTITIES'] = False
    if kind == 'passed-true': value['passed'] = True
    if kind == 'numeric-false': value['checks'][key] = 0
    if kind == 'string-false': value['checks'][key] = 'false'
    if kind == 'numeric-passed': value['passed'] = 0
    if kind == 'extra-field': value['extra'] = 'unexpected'
    if kind == 'missing-check': del value['checks'][key]
    if kind == 'metadata-object': value['object'] = 'OTHER-SYNTHETIC-OBJECT'
    if kind == 'metadata-scope': value['scope'] = 'changed scope'
    if kind == 'metadata-count': value['inventory_files'] += 1
    if kind == 'metadata-numeric-alias': value['inventory_files'] = float(value['inventory_files'])
if kind == 'noise': print('synthetic unexpected stderr', file=sys.stderr)
print(json.dumps(value, sort_keys=True, **({} if kind == 'format' else {'indent': 2})))
sys.exit({'exit-zero': 0, 'exit-two': 2, 'baseline-exit': 1}.get(kind, 0 if label == 'baseline' else 1))
'''
CHILD = 'FAILED_CHECKS = ' + repr(FAILED_CHECKS) + '\n' + CHILD


def report_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def workflow_shell(text):
    name = '      - name: Verify sources, replay both modes, reject mutants\n'
    if text.count(name) != 1:
        raise ValueError('expected one named protocol step')
    tail = text.split(name, 1)[1].split('      - ', 1)[0]
    marker = '        run: |\n'
    if tail.count(marker) != 1:
        raise ValueError('expected named literal run block')
    lines = tail.split(marker, 1)[1].splitlines(keepends=True)
    if any(line.strip() and not line.startswith('          ') for line in lines):
        raise ValueError('unexpected run-block indentation')
    shell = ''.join(line[10:] if line.startswith('          ') else line for line in lines)
    if not shell.startswith('set -euo pipefail\n') or not shell.endswith('git diff --exit-code\n'):
        raise ValueError('incomplete protocol shell')
    return shell


class D5ReconciliationWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which('git') or not shutil.which('bash'):
            raise RuntimeError('these workflow tests require Git and Bash')
        cls.workflow = WORKFLOW.read_text(encoding='utf-8')
        cls.shell = workflow_shell(cls.workflow)

    def run_fixture(self, kind='valid', target='baseline', mode=0):
        with tempfile.TemporaryDirectory(prefix='d5-reconciliation-protocol-') as temp:
            outer = Path(temp)
            repo = outer / 'repo'
            packet = repo / PACKET
            packet.mkdir(parents=True)
            executable_dir = outer / 'bin'
            executable_dir.mkdir()
            (executable_dir / 'python').symlink_to(sys.executable)
            env = {key: value for key, value in os.environ.items()
                   if not key.startswith(('GIT_', 'PYTHON', 'RECONCILIATION_')) and key not in ('BASH_ENV', 'ENV')}
            env.update(PATH=str(executable_dir) + os.pathsep + os.environ.get('PATH', ''),
                       GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_TERMINAL_PROMPT='0', PYTHONDONTWRITEBYTECODE='1',
                       RECONCILIATION_KIND=kind, RECONCILIATION_TARGET=target, RECONCILIATION_MODE=str(mode),
                       RECONCILIATION_EVENTS=str(outer / 'events.jsonl'))

            def git(*args):
                proc = subprocess.run(['git', '-c', 'gc.auto=0', *args], cwd=repo,
                                      env=env, capture_output=True, timeout=15)
                self.assertEqual(proc.returncode, 0, proc.stderr.decode(errors='replace'))
                return proc.stdout

            payloads = {'reconciliation_check.py': CHILD.encode(), 'RESULTS.json': report_bytes(BASELINE),
                        'RECONCILIATION.md': b'SYNTHETIC fixture; not a reconciliation verdict.\n'}
            for name, data in payloads.items():
                (packet / name).write_bytes(data)
            manifest = {'synthetic_fixture': True, 'files': [
                {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                for name, data in sorted(payloads.items())]}
            (packet / 'SOURCE_FILES.json').write_bytes(report_bytes(manifest))
            (repo / 'marker.txt').write_bytes(b'original\n')
            if kind == 'tamper':
                (packet / 'reconciliation_check.py').write_bytes(CHILD.encode() + b'\n# unbound\n')
            elif kind == 'missing':
                (packet / 'RECONCILIATION.md').unlink()
            elif kind == 'extra':
                (packet / 'extra.txt').write_bytes(b'extra\n')
            elif kind == 'symlink':
                (packet / 'RECONCILIATION.md').unlink()
                (outer / 'reconciliation.txt').write_bytes(payloads['RECONCILIATION.md'])
                (packet / 'RECONCILIATION.md').symlink_to(outer / 'reconciliation.txt')
            git('init', '-q')
            git('add', '.')
            git('-c', 'user.name=Protocol fixture', '-c', 'user.email=fixture@example.invalid',
                'commit', '-qm', 'Synthetic protocol fixture only')
            head = git('rev-parse', 'HEAD')
            if kind == 'dirty':
                (repo / 'marker.txt').write_bytes(b'intentionally dirty\n')
            before = {p.relative_to(repo).as_posix(): p.read_bytes()
                      for p in repo.rglob('*') if p.is_file() and '.git' not in p.parts}
            proc = subprocess.run(['bash', '-c', self.shell], cwd=repo, env=env,
                                  capture_output=True, timeout=30)
            after = {p.relative_to(repo).as_posix(): p.read_bytes()
                     for p in repo.rglob('*') if p.is_file() and '.git' not in p.parts}
            self.assertEqual(before, after, 'workflow changed fixture payload bytes')
            self.assertEqual(git('rev-parse', 'HEAD'), head)
            events_path = outer / 'events.jsonl'
            events = [json.loads(line) for line in events_path.read_text().splitlines()] if events_path.exists() else []
            return proc, events

    @staticmethod
    def sequence():
        return [[label, mode, 1, True] for mode in (0, 1) for label in ('baseline', *LABELS)]

    def assert_refusal(self, kind, target, mode, diagnostic):
        proc, events = self.run_fixture(kind, target, mode)
        self.assertNotEqual(proc.returncode, 0, (kind, target, mode, proc.stdout, proc.stderr))
        self.assertNotIn(b'"mathematical_acceptance": false', proc.stdout)
        self.assertIn(diagnostic, proc.stderr)
        index = self.sequence().index([target, mode, 1, True])
        self.assertEqual(events, self.sequence()[:index + 1])

    def test_valid_baselines_and_eight_label_reports_reach_both_modes(self):
        proc, events = self.run_fixture()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, b'{"scientific_effect": "NONE", "mathematical_acceptance": false}\n')
        self.assertEqual(proc.stderr, b'')
        self.assertEqual(events, self.sequence())

    def test_unrelated_crash_is_not_a_mutant_rejection(self):
        self.check_mutants('crash')

    def test_silent_exit_one_is_not_a_mutant_rejection(self):
        self.check_mutants('silent')

    def test_wrong_stdout_is_not_a_mutant_rejection(self):
        self.check_mutants('wrong-stdout')

    def test_complete_flat_label_report_and_boolean_types_are_required(self):
        for kind in ('wrong-check', 'passed-true', 'numeric-false', 'string-false',
                     'numeric-passed', 'extra-field', 'missing-check', 'format'):
            self.check_mutants(kind)

    def test_all_noncheck_report_metadata_remains_exact(self):
        for kind in ('metadata-object', 'metadata-scope', 'metadata-count', 'metadata-numeric-alias'):
            self.check_mutants(kind)

    def check_mutants(self, kind):
        for mode in (0, 1):
            for label in LABELS:
                with self.subTest(kind=kind, mode=mode, label=label):
                    self.assert_refusal(kind, label, mode, b'mutant '+label.encode())

    def test_mutant_stderr_is_not_accepted(self):
        self.check_mutants('noise')

    def test_wrong_mutant_exit_is_not_accepted(self):
        for kind in ('exit-zero', 'exit-two'):
            self.check_mutants(kind)

    def test_baseline_stderr_is_not_accepted(self):
        for mode in (0, 1):
            with self.subTest(mode=mode):
                self.assert_refusal('noise', 'baseline', mode, b'baseline stderr')

    def test_baseline_stdout_remains_exact(self):
        for mode in (0, 1):
            with self.subTest(mode=mode):
                self.assert_refusal('baseline-wrong', 'baseline', mode, b'output differs from RESULTS.json')

    def test_baseline_nonzero_stops_before_mutants(self):
        for mode in (0, 1):
            with self.subTest(mode=mode):
                self.assert_refusal('baseline-exit', 'baseline', mode, b'CalledProcessError')

    def test_manifest_and_source_guards_precede_checker_execution(self):
        for kind, diagnostic in [('tamper', b'source identity mismatch'),
                                 ('missing', b'packet tree differs'), ('extra', b'packet tree differs'),
                                 ('symlink', b'flat regular source required')]:
            with self.subTest(kind=kind):
                proc, events = self.run_fixture(kind)
                self.assertNotEqual(proc.returncode, 0)
                self.assertIn(diagnostic, proc.stderr)
                self.assertEqual(events, [])

    def test_final_git_guard_still_refuses_dirty_fixture(self):
        proc, events = self.run_fixture('dirty')
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn(b'diff --git', proc.stdout)
        self.assertEqual(events, self.sequence())

    def test_existing_workflow_execution_contract_is_preserved(self):
        for path in ('reviews/d5_reconciliation_20260929/**', '.github/workflows/d5-reconciliation.yml',
                     'reviews/d5_*/**', 'frontiers/intermediate_window_20260928/**',
                     'frontiers/remote_window_20260924/**', 'frontiers/remote_collision_20260928/**',
                     'frontiers/rn_annulus_bridge_20260925/**'):
            with self.subTest(path=path):
                self.assertIn("      - '" + path + "'\n", self.workflow)
        self.assertIn("  workflow_dispatch:\n", self.workflow)
        self.assertIn("permissions:\n  contents: read\n", self.workflow)
        self.assertIn("timeout-minutes: 10\n", self.workflow)
        self.assertIn("actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1", self.workflow)
        self.assertIn("persist-credentials: false", self.workflow)
        self.assertIn("actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0", self.workflow)
        self.assertIn("PYTHONDONTWRITEBYTECODE: '1'", self.workflow)

    def test_protocol_tests_are_wired_for_both_outer_modes(self):
        self.assertIn("      - 'tests/test_d5_reconciliation_workflow.py'\n", self.workflow)
        self.assertIn("python -B -S -m unittest discover -s tests -p 'test_d5_reconciliation_workflow.py' -v", self.workflow)
        self.assertIn("python -B -O -S -m unittest discover -s tests -p 'test_d5_reconciliation_workflow.py' -v", self.workflow)
        self.assertIn("python-version: '3.11.16'", self.workflow)
        self.assertEqual(self.shell.count('timeout=300'), 2)


if __name__ == '__main__':
    unittest.main()
