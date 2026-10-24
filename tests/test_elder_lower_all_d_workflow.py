"""Real-shell elder-lower-all-d protocol tests with committed SYNTHETIC fixtures.

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

WORKFLOW = Path(__file__).resolve().parents[1] / '.github/workflows/elder-lower-all-d.yml'
PACKET = Path('frontiers/elder_lower_all_d_20260929')
# Source-derived first failed checks; native characterization is separate.
FAILURE_LINES = {
    'M1': 'FAIL L_ledger_m2\n',
    'M2': 'FAIL P2_hessian_M\n',
    'M3': 'FAIL E6_margin_below\n',
}
LABELS = tuple(FAILURE_LINES)
BASELINE = {
    'object': 'SYNTHETIC-ELDER-ALL-D-PROTOCOL-FIXTURE',
    'passed': True,
    'results': {'synthetic': 'workflow engineering fixture; no mathematical assertion'},
    'scope': 'SYNTHETIC source and child-protocol controls only',
}

# This is a real child process, never a mocked subprocess API or interpreter.
CHILD = r'''import json, os, pathlib, sys
args = sys.argv[1:]
label = args[-1] if '--mutant' in args else 'baseline'
event = {'label': label, 'argv': args,
         'interpreter_flags': sys.orig_argv[1:sys.orig_argv.index(sys.argv[0])],
         'optimize': sys.flags.optimize, 'no_site': sys.flags.no_site,
         'dont_write_bytecode': sys.dont_write_bytecode}
with open(os.environ['ELDER_ALL_D_EVENTS'], 'a', encoding='utf-8') as stream:
    stream.write(json.dumps(event)+'\n')
selected = label == os.environ.get('ELDER_ALL_D_TARGET') and str(sys.flags.optimize) == os.environ.get('ELDER_ALL_D_MODE')
kind = os.environ.get('ELDER_ALL_D_KIND', 'valid') if selected else 'valid'
if kind == 'crash': raise RuntimeError('synthetic unrelated crash')
if kind == 'silent': sys.exit(1)
expected = (pathlib.Path(__file__).parent/'RESULTS.json').read_text()
out = expected if label == 'baseline' else FAILURE_LINES[label]
if kind == 'baseline-wrong': out = 'synthetic wrong baseline bytes\n'
if kind == 'wrong-label': out = FAILURE_LINES['M2' if label == 'M1' else 'M1']
if kind == 'baseline-json': out = expected
if kind == 'missing-newline': out = out.rstrip('\n')
if kind == 'prefix-noise': out = 'unexpected prefix\n' + out
if kind == 'suffix-noise': out += 'unexpected suffix\n'
if kind == 'stderr': print('synthetic unexpected stderr', file=sys.stderr)
sys.stdout.write(out)
sys.exit({'exit-zero': 0, 'exit-two': 2, 'baseline-exit': 1}.get(kind, 0 if label == 'baseline' else 1))
'''
CHILD = 'FAILURE_LINES = ' + repr(FAILURE_LINES) + '\n' + CHILD


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


class ElderLowerAllDWorkflow(unittest.TestCase):
    shell_runs = 0

    @classmethod
    def setUpClass(cls):
        if not shutil.which('git') or not shutil.which('bash'):
            raise RuntimeError('these workflow tests require Git and Bash')
        cls.shell_runs = 0
        cls.workflow = WORKFLOW.read_text(encoding='utf-8')
        cls.shell = workflow_shell(cls.workflow)

    def run_fixture(self, kind='valid', target='baseline', mode=0):
        with tempfile.TemporaryDirectory(prefix='elder-lower-all-d-protocol-') as temp:
            outer = Path(temp)
            repo = outer / 'repo'
            packet = repo / PACKET
            packet.mkdir(parents=True)
            executable_dir = outer / 'bin'
            executable_dir.mkdir()
            (executable_dir / 'python').symlink_to(sys.executable)
            env = {key: value for key, value in os.environ.items()
                   if not key.startswith(('GIT_', 'PYTHON', 'ELDER_ALL_D_')) and key not in ('BASH_ENV', 'ENV')}
            env.update(PATH=str(executable_dir) + os.pathsep + os.environ.get('PATH', ''),
                       GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_TERMINAL_PROMPT='0', PYTHONDONTWRITEBYTECODE='1',
                       ELDER_ALL_D_KIND=kind, ELDER_ALL_D_TARGET=target, ELDER_ALL_D_MODE=str(mode),
                       ELDER_ALL_D_EVENTS=str(outer / 'events.jsonl'))

            def git(*args):
                proc = subprocess.run(['git', '-c', 'gc.auto=0', *args], cwd=repo,
                                      env=env, capture_output=True, timeout=15)
                self.assertEqual(proc.returncode, 0, proc.stderr.decode(errors='replace'))
                return proc.stdout

            payloads = {'lower_all_d_check.py': CHILD.encode(), 'RESULTS.json': report_bytes(BASELINE),
                        'PROOF.md': b'SYNTHETIC fixture; not a mathematical proof.\n'}
            for name, data in payloads.items():
                (packet / name).write_bytes(data)
            manifest = {'synthetic_fixture': True, 'files': [
                {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                for name, data in sorted(payloads.items())]}
            (packet / 'SOURCE_FILES.json').write_bytes(report_bytes(manifest))
            (repo / 'marker.txt').write_bytes(b'original\n')
            if kind == 'hash-only':
                proof = payloads['PROOF.md']
                (packet / 'PROOF.md').write_bytes(b'X' + proof[1:])  # same length, different hash
            elif kind == 'size-only':
                proof_entry = next(row for row in manifest['files'] if row['path'] == 'PROOF.md')
                proof_entry['bytes'] += 1  # actual bytes and their expected SHA256 stay unchanged
                (packet / 'SOURCE_FILES.json').write_bytes(report_bytes(manifest))
            elif kind == 'missing':
                (packet / 'PROOF.md').unlink()
            elif kind == 'extra':
                (packet / 'extra.txt').write_bytes(b'extra\n')
            elif kind == 'symlink':
                (packet / 'PROOF.md').unlink()
                (outer / 'proof.txt').write_bytes(payloads['PROOF.md'])
                (packet / 'PROOF.md').symlink_to(outer / 'proof.txt')
            git('init', '-q')
            git('add', '.')
            git('-c', 'user.name=Protocol fixture', '-c', 'user.email=fixture@example.invalid',
                'commit', '-qm', 'Synthetic protocol fixture only')
            head = git('rev-parse', 'HEAD')
            if kind == 'dirty':
                (repo / 'marker.txt').write_bytes(b'intentionally dirty\n')
            before = {p.relative_to(repo).as_posix(): p.read_bytes()
                      for p in repo.rglob('*') if p.is_file() and '.git' not in p.parts}
            type(self).shell_runs += 1
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
    def event(label, mode):
        return {'label': label, 'argv': [] if label == 'baseline' else ['--mutant', label],
                'interpreter_flags': ['-B', '-S'] if mode == 0 else ['-B', '-O', '-S'],
                'optimize': mode, 'no_site': 1, 'dont_write_bytecode': True}

    @classmethod
    def sequence(cls):
        return [cls.event(label, mode)
                for mode in (0, 1) for label in ('baseline', *LABELS)]

    def assert_refusal(self, kind, target, mode, diagnostic):
        proc, events = self.run_fixture(kind, target, mode)
        self.assertNotEqual(proc.returncode, 0, (kind, target, mode, proc.stdout, proc.stderr))
        self.assertNotIn(b'"scientific_acceptance": false', proc.stdout)
        self.assertIn(diagnostic, proc.stderr)
        index = self.sequence().index(self.event(target, mode))
        self.assertEqual(events, self.sequence()[:index + 1])

    def test_valid_baseline_and_three_failure_lines_reach_both_modes(self):
        proc, events = self.run_fixture()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, b'{"scientific_effect": "NONE", "scientific_acceptance": false}\n')
        self.assertEqual(proc.stderr, b'')
        self.assertEqual(events, self.sequence())

    def test_unrelated_crash_is_not_a_mutant_rejection(self):
        self.check_mutants('crash')

    def test_silent_exit_one_is_not_a_mutant_rejection(self):
        self.check_mutants('silent')

    def test_complete_label_failure_bytes_are_required(self):
        for kind in ('wrong-label', 'baseline-json', 'missing-newline', 'prefix-noise', 'suffix-noise'):
            self.check_mutants(kind)

    def check_mutants(self, kind):
        for mode in (0, 1):
            for label in LABELS:
                with self.subTest(kind=kind, mode=mode, label=label):
                    self.assert_refusal(kind, label, mode, b'mutant '+label.encode())

    def test_mutant_stderr_is_not_accepted(self):
        self.check_mutants('stderr')

    def test_wrong_mutant_exit_is_not_accepted(self):
        for kind in ('exit-zero', 'exit-two'):
            self.check_mutants(kind)

    def test_baseline_stderr_is_not_accepted(self):
        for mode in (0, 1):
            with self.subTest(mode=mode):
                self.assert_refusal('stderr', 'baseline', mode, b'baseline stderr')

    def test_baseline_stdout_remains_exact(self):
        for mode in (0, 1):
            with self.subTest(mode=mode):
                self.assert_refusal('baseline-wrong', 'baseline', mode, b'output differs from RESULTS.json')

    def test_baseline_nonzero_stops_before_mutants(self):
        for mode in (0, 1):
            with self.subTest(mode=mode):
                self.assert_refusal('baseline-exit', 'baseline', mode, b'CalledProcessError')

    def test_manifest_and_source_guards_precede_checker_execution(self):
        for kind, diagnostic in [('hash-only', b'source identity mismatch'),
                                 ('size-only', b'source identity mismatch'),
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
        for path in ('frontiers/elder_lower_all_d_20260929/**', '.github/workflows/elder-lower-all-d.yml'):
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
        self.assertIn("      - 'tests/test_elder_lower_all_d_workflow.py'\n", self.workflow)
        self.assertIn("python -B -S -m unittest discover -s tests -p 'test_elder_lower_all_d_workflow.py' -v", self.workflow)
        self.assertIn("python -B -O -S -m unittest discover -s tests -p 'test_elder_lower_all_d_workflow.py' -v", self.workflow)
        self.assertIn("python-version: '3.11.16'", self.workflow)
        self.assertEqual(self.shell.count('timeout=300'), 2)


if __name__ == '__main__':
    unittest.main()
