"""Real-shell elder-lower-review protocol tests with SYNTHETIC fixtures.

No mathematical packet is replayed here. Real checker children record their
interpreter flags while the complete workflow block retains source/Git guards.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

WORKFLOW = Path(__file__).resolve().parents[1] / '.github/workflows/elder-lower-review.yml'
PACKET = Path('reviews/d1_elder_lower_claude_20260928')
MUTANT_FALSE = {
    'drop-aZ-over-8': (
        ('NF_pinned_normal_form', 'F_minus_P_is_O_r_generic_degree6'),
        ('NF_pinned_normal_form', 'P_satisfies_all_six_pins_for_arbitrary_jets'),
    ),
    'hessian-sign': (('G_cubic_critical_data', 'M_hessian_diag_-6k_-k_over_2_max'),),
    'path-endpoint': (
        ('PATH_elder_obstruction', 'g3_prime_ge_9_over_64'),
        ('PATH_elder_obstruction', 'path_end_17_over_64'),
        ('PATH_elder_obstruction', 'path_in_B3'),
        ('PATH_elder_obstruction', 'segment_polynomials_E6'),
    ),
    'weight-power': (('LED_ledgers', 'tilt_ledger_r_times_r4_over_r2_is_r3'),),
    'tv-half': (('TV_multiplicity', 'bernoulli_tv_equals_h_random_exact'),),
}
LABELS = tuple(MUTANT_FALSE)
BASELINE = {
    'checks': {
        'NF_pinned_normal_form': {
            'F_minus_P_is_O_r_generic_degree6': True,
            'P_satisfies_all_six_pins_for_arbitrary_jets': True,
            'synthetic_unaffected': True,
        },
        'G_cubic_critical_data': {
            'M_hessian_diag_-6k_-k_over_2_max': True,
            'synthetic_unaffected': True,
        },
        'PATH_elder_obstruction': {
            'g3_prime_ge_9_over_64': True,
            'path_end_17_over_64': True,
            'path_in_B3': True,
            'segment_polynomials_E6': True,
            'synthetic_unaffected': True,
        },
        'LED_ledgers': {'tilt_ledger_r_times_r4_over_r2_is_r3': True},
        'TV_multiplicity': {'bernoulli_tv_equals_h_random_exact': True},
    },
    'passed': True,
    'scientific_effect': 'NONE',
    'scope': 'SYNTHETIC workflow engineering fixture; no mathematical assertion',
}
def report_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def expected_mutant(label):
    value = copy.deepcopy(BASELINE)
    value['passed'] = False
    for group, check in MUTANT_FALSE[label]:
        value['checks'][group][check] = False
    return report_bytes(value)


CHILD = r'''import argparse, contextlib, copy, io, json, os, pathlib, sys
MUTANT_FALSE = ''' + repr(MUTANT_FALSE) + r'''
BASELINE = ''' + repr(BASELINE) + r'''
args = sys.argv[1:]
label = args[-1] if '--mutant' in args else 'baseline'
event = {'label': label, 'argv': args,
         'interpreter_flags': sys.orig_argv[1:sys.orig_argv.index(sys.argv[0])],
         'optimize': sys.flags.optimize, 'no_site': sys.flags.no_site,
         'dont_write_bytecode': sys.dont_write_bytecode}
with open(os.environ['ELR_EVENTS'], 'a', encoding='utf-8') as stream:
    stream.write(json.dumps(event) + '\n')
selected = label == os.environ.get('ELR_TARGET') and str(sys.flags.optimize) == os.environ.get('ELR_MODE')
kind = os.environ.get('ELR_KIND', 'valid') if selected else 'valid'
if kind == 'crash': raise RuntimeError('synthetic unrelated crash')
if kind == 'silent': sys.exit(1)
if label == 'baseline':
    out = (pathlib.Path(__file__).parent / 'RESULTS.json').read_bytes()
    if kind == 'baseline-wrong': out = b'synthetic wrong baseline bytes\n'
    if kind == 'stderr': print('synthetic unexpected stderr', file=sys.stderr)
    sys.stdout.buffer.write(out)
    sys.exit(1 if kind == 'baseline-exit' else 0)
if label == 'M99':
    stream = io.StringIO()
    parser = argparse.ArgumentParser(prog=pathlib.Path(__file__).name)
    parser.add_argument('--mutant', choices=tuple(MUTANT_FALSE))
    with contextlib.redirect_stderr(stream):
        try: parser.parse_args(['--mutant', 'M99'])
        except SystemExit as exc: rc = exc.code
    stdout, stderr = b'', stream.getvalue().encode()
    if kind == 'unknown-stdout': stdout = b'unexpected output\n'
    if kind == 'unknown-wrong-stderr': stderr = b'unrelated exit two\n'
    if kind == 'unknown-no-stderr': stderr = b''
    if kind == 'unknown-exit-one': rc = 1
    sys.stdout.buffer.write(stdout); sys.stderr.buffer.write(stderr); sys.exit(rc)
value = copy.deepcopy(BASELINE); value['passed'] = False
for group, check in MUTANT_FALSE[label]: value['checks'][group][check] = False
if kind == 'wrong-report': value['checks'][next(iter(value['checks']))]['synthetic_unaffected'] = False
out = (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
if kind == 'baseline-json': out = (pathlib.Path(__file__).parent / 'RESULTS.json').read_bytes()
if kind == 'missing-newline': out = out.rstrip(b'\n')
if kind == 'prefix-noise': out = b'unexpected prefix\n' + out
if kind == 'stderr': print('synthetic unexpected stderr', file=sys.stderr)
sys.stdout.buffer.write(out)
sys.exit({'exit-zero': 0, 'exit-two': 2}.get(kind, 1))
'''


def workflow_shell(text):
    name = '      - name: Verify sources, replay both modes, reject mutants\n'
    if text.count(name) != 1:
        raise ValueError('expected one named protocol step')
    tail = text.split(name, 1)[1].split('      - ', 1)[0]
    marker = '        run: |\n'
    lines = tail.split(marker, 1)[1].splitlines(keepends=True)
    shell = ''.join(line[10:] if line.startswith('          ') else line for line in lines)
    if not shell.startswith('set -euo pipefail\n') or not shell.endswith('git diff --exit-code\n'):
        raise ValueError('incomplete protocol shell')
    return shell


class ElderLowerReviewWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which('git') or not shutil.which('bash'):
            raise RuntimeError('these tests require Git and Bash')
        cls.workflow = WORKFLOW.read_text(encoding='utf-8')
        cls.shell = workflow_shell(cls.workflow)

    def run_fixture(self, kind='valid', target='baseline', mode=0):
        with tempfile.TemporaryDirectory(prefix='elder-lower-review-') as temp:
            outer = Path(temp); repo = outer / 'repo'; packet = repo / PACKET
            packet.mkdir(parents=True)
            bindir = outer / 'bin'; bindir.mkdir(); (bindir / 'python').symlink_to(sys.executable)
            env = {k: v for k, v in os.environ.items()
                   if not k.startswith(('GIT_', 'PYTHON', 'ELR_')) and k not in ('BASH_ENV', 'ENV')}
            env.update(PATH=str(bindir) + os.pathsep + os.environ.get('PATH', ''),
                       GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_TERMINAL_PROMPT='0', PYTHONDONTWRITEBYTECODE='1',
                       ELR_KIND=kind, ELR_TARGET=target, ELR_MODE=str(mode),
                       ELR_EVENTS=str(outer / 'events.jsonl'))

            def git(*args):
                p = subprocess.run(['git', '-c', 'gc.auto=0', *args], cwd=repo, env=env,
                                   capture_output=True, timeout=15)
                self.assertEqual(p.returncode, 0, p.stderr.decode(errors='replace'))
                return p.stdout

            payloads = {
                'elder_lower_exact_check.py': CHILD.encode(),
                'RESULTS.json': report_bytes(BASELINE),
                'REVIEW.md': b'SYNTHETIC fixture; not a mathematical review.\n',
            }
            for name, data in payloads.items(): (packet / name).write_bytes(data)
            manifest = {'synthetic_fixture': True, 'files': [
                {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                for name, data in sorted(payloads.items())]}
            (packet / 'SOURCE_FILES.json').write_bytes(report_bytes(manifest))
            (repo / 'marker.txt').write_bytes(b'original\n')
            if kind == 'hash-only':
                data = payloads['REVIEW.md']; (packet / 'REVIEW.md').write_bytes(b'X' + data[1:])
            elif kind == 'size-only':
                next(x for x in manifest['files'] if x['path'] == 'REVIEW.md')['bytes'] += 1
                (packet / 'SOURCE_FILES.json').write_bytes(report_bytes(manifest))
            elif kind == 'missing': (packet / 'REVIEW.md').unlink()
            elif kind == 'extra': (packet / 'extra.txt').write_bytes(b'extra\n')
            elif kind == 'symlink':
                (packet / 'REVIEW.md').unlink(); (outer / 'review.txt').write_bytes(payloads['REVIEW.md'])
                (packet / 'REVIEW.md').symlink_to(outer / 'review.txt')
            git('init', '-q'); git('add', '.')
            git('-c', 'user.name=Protocol fixture', '-c', 'user.email=fixture@example.invalid',
                'commit', '-qm', 'Synthetic protocol fixture only')
            head = git('rev-parse', 'HEAD')
            if kind == 'dirty': (repo / 'marker.txt').write_bytes(b'intentionally dirty\n')
            proc = subprocess.run(['bash', '-c', self.shell], cwd=repo, env=env,
                                  capture_output=True, timeout=30)
            self.assertEqual(git('rev-parse', 'HEAD'), head)
            ep = outer / 'events.jsonl'
            events = [json.loads(x) for x in ep.read_text().splitlines()] if ep.exists() else []
            return proc, events

    @staticmethod
    def event(label, mode):
        return {'label': label, 'argv': [] if label == 'baseline' else ['--mutant', label],
                'interpreter_flags': ['-B', '-S'] if mode == 0 else ['-B', '-O', '-S'],
                'optimize': mode, 'no_site': 1, 'dont_write_bytecode': True}

    @classmethod
    def sequence(cls):
        return [cls.event(label, mode) for mode in (0, 1)
                for label in ('baseline', *LABELS, 'M99')]

    def assert_refusal(self, kind, target, mode, diagnostic):
        proc, events = self.run_fixture(kind, target, mode)
        self.assertNotEqual(proc.returncode, 0, (kind, target, mode, proc.stdout, proc.stderr))
        self.assertNotIn(b'"mathematical_acceptance": false', proc.stdout)
        self.assertIn(diagnostic, proc.stderr)
        index = self.sequence().index(self.event(target, mode))
        self.assertEqual(events, self.sequence()[:index + 1])

    def check_mutants(self, kind):
        for mode in (0, 1):
            for label in LABELS:
                with self.subTest(kind=kind, mode=mode, label=label):
                    self.assert_refusal(kind, label, mode, b'mutant ' + label.encode())

    def test_valid_protocol_reaches_both_modes(self):
        proc, events = self.run_fixture()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, b'{"scientific_effect": "NONE", "mathematical_acceptance": false}\n')
        self.assertEqual(proc.stderr, b''); self.assertEqual(events, self.sequence())

    def test_unrelated_crash_is_not_a_mutant_rejection(self): self.check_mutants('crash')
    def test_silent_exit_one_is_not_a_mutant_rejection(self): self.check_mutants('silent')

    def test_exact_mutant_report_is_required(self):
        for kind in ('wrong-report', 'baseline-json', 'missing-newline', 'prefix-noise'):
            self.check_mutants(kind)

    def test_mutant_stderr_and_exit_are_exact(self):
        for kind in ('stderr', 'exit-zero', 'exit-two'): self.check_mutants(kind)

    def test_unknown_label_protocol_is_exact(self):
        for kind in ('unknown-stdout', 'unknown-wrong-stderr', 'unknown-no-stderr', 'unknown-exit-one'):
            for mode in (0, 1):
                with self.subTest(kind=kind, mode=mode):
                    self.assert_refusal(kind, 'M99', mode, b'unknown mutant label')

    def test_baseline_protocol_is_exact(self):
        for kind, diagnostic in (('stderr', b'baseline stderr'),
                                 ('baseline-wrong', b'output differs from RESULTS.json'),
                                 ('baseline-exit', b'baseline exit')):
            for mode in (0, 1):
                with self.subTest(kind=kind, mode=mode):
                    self.assert_refusal(kind, 'baseline', mode, diagnostic)

    def test_source_guards_precede_execution(self):
        for kind, diagnostic in (('hash-only', b'source identity mismatch'),
                                 ('size-only', b'source identity mismatch'),
                                 ('missing', b'packet tree differs'), ('extra', b'packet tree differs'),
                                 ('symlink', b'flat regular source required')):
            proc, events = self.run_fixture(kind)
            self.assertNotEqual(proc.returncode, 0); self.assertIn(diagnostic, proc.stderr)
            self.assertEqual(events, [])

    def test_final_git_guard_is_retained(self):
        proc, events = self.run_fixture('dirty')
        self.assertNotEqual(proc.returncode, 0); self.assertIn(b'diff --git', proc.stdout)
        self.assertEqual(events, self.sequence())

    def test_execution_contract_and_test_wiring(self):
        for needle in ("      - 'reviews/d1_elder_lower_claude_20260928/**'\n",
                       "      - 'tests/test_elder_lower_review_workflow.py'\n",
                       'permissions:\n  contents: read\n', 'timeout-minutes: 10\n',
                       'actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1',
                       'persist-credentials: false',
                       'actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0',
                       "python-version: '3.11.16'", "PYTHONDONTWRITEBYTECODE: '1'",
                       "python -B -S -m unittest discover -s tests -p 'test_elder_lower_review_workflow.py' -v",
                       "python -B -O -S -m unittest discover -s tests -p 'test_elder_lower_review_workflow.py' -v"):
            self.assertIn(needle, self.workflow)


if __name__ == '__main__':
    unittest.main()
