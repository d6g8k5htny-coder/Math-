"""Exercise the real embedded workflow driver with synthetic subprocess payloads.

Fixture hashes authenticate only these fixtures. Real jet/source replay remains
separate hosted evidence; this suite does not test Gaussian mathematics.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / '.github/workflows/iba1-periodic-jet.yml'
PACKET = Path('reviews/iba1_periodic_jet_claude_20261005')
REJECTIONS = {
    'M1': ['R3_L24_anisotropy_measured', 'R3_L4_anisotropy_visible'],
    'M2': ['R1_reference_d3_trace_frobenius', 'R1_reference_jet',
           'R4_c224_in_side24_interval'],
    'M3': ['R4_c224_in_side24_interval'],
    'M4': ['R1_reference_d3_trace_frobenius',
           'R6_transverse_frame_invariance_d3', 'R6_transverse_frame_invariance_d4'],
}
CHECKS = sorted({k for v in REJECTIONS.values() for k in v}
                | {'R2_positive_L%s_d%d' % (p, d)
                   for p in ('24', '8', '2pi', '4', '3') for d in (2, 3, 4)}
                | {'R4_c224_equals_reference'}
                | {'R5_quadrature_settled_L%s' % p for p in ('8', '2pi', '4', '3')})
BASELINE = {'object': 'CL-IBA1-ITEM2-PERIODIC-JET-20261005-v1',
            'precision_digits': 270, 'scientific_effect': 'NONE',
            'cases': {}, 'transverse_rotation_max_abs_change_L4': {}, 'c_2': {},
            'c_2_diagnostic_small_L': {}, 'checks': dict.fromkeys(CHECKS, True),
            'passed': True}


def driver(text):
    start = "          python -B -S - <<'PY'\n"
    if text.count(start) != 1:
        raise ValueError('expected one embedded driver')
    return textwrap.dedent(text.split(start, 1)[1].split('          PY\n', 1)[0])


def blob(data):
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def fixture(root):
    packet = root / PACKET
    packet.mkdir(parents=True)
    baseline = json.dumps(BASELINE, indent=1, sort_keys=True) + '\n'
    source = '''import json, os, sys
from pathlib import Path
expected = json.loads(Path('RESULTS.json').read_text())
rejections = REJECTIONS_LITERAL
label = sys.argv[2] if len(sys.argv) == 3 else 'baseline'
scenario = os.environ.get('PJ_TEST_SCENARIO', 'valid')
active = label == os.environ.get('PJ_TEST_STAGE', 'M1')
if label == 'baseline':
    data = Path('RESULTS.json').read_text()
    if active and scenario == 'baseline_changed': data += ' '
    if active and scenario == 'baseline_stderr': print('warning', file=sys.stderr)
    print(data, end=''); sys.exit(1 if active and scenario == 'wrong_exit' else 0)
if label == 'M9':
    if active and scenario == 'crash': raise RuntimeError('synthetic M9 crash')
    if active and scenario == 'stderr': print('warning', file=sys.stderr)
    print('wrong label' if active and scenario == 'm9_wrong' else 'unknown mutant',
          end='' if active and scenario == 'm9_whitespace' else '\\n')
    sys.exit(1 if active and scenario == 'wrong_exit' else 2)
expected['passed'] = False
for check in rejections[label]: expected['checks'][check] = False
if active:
    if scenario == 'crash': raise RuntimeError('synthetic mutant crash')
    if scenario == 'stderr': print('warning', file=sys.stderr)
    if scenario == 'empty': sys.exit(1)
    if scenario == 'garbage': print('not JSON'); sys.exit(1)
    if scenario == 'passed_true': expected['passed'] = True
    if scenario == 'passed_int': expected['passed'] = 0
    if scenario == 'wrong_reason':
        expected['checks'] = dict.fromkeys(expected['checks'], True)
        expected['checks']['R2_positive_L24_d2'] = False
    if scenario == 'missing_check': expected['checks'].pop('R2_positive_L24_d2')
    if scenario == 'extra_check': expected['checks']['unexpected'] = True
    if scenario == 'check_int': expected['checks'][rejections[label][0]] = 0
    if scenario == 'extra_failure': expected['checks']['R2_positive_L24_d2'] = False
    if scenario == 'missing_failure': expected['checks'][rejections[label][0]] = True
    if scenario == 'wrong_object': expected['object'] = 'different packet'
    if scenario == 'wrong_precision': expected['precision_digits'] = 270.0
    if scenario == 'wrong_effect': expected['scientific_effect'] = 'ACCEPT'
    if scenario == 'extra_field': expected['unexpected'] = True
    if scenario == 'missing_field': expected.pop('cases')
    if scenario == 'checks_list': expected['checks'] = []
    if scenario == 'root_list': expected = []
    if scenario == 'nan': expected['cases']['bad'] = float('nan')
data = json.dumps(expected, sort_keys=True)
if active and scenario == 'duplicate': data = data.replace('"passed": false', '"passed": false, "passed": false')
if active and scenario == 'overflow': data = data.replace('"cases": {}', '"cases": {"bad": 1e999}')
if active and scenario == 'trailing': data += ' trailing text'
print(data)
sys.exit(0 if active and scenario == 'wrong_exit' else 1)
'''.replace('REJECTIONS_LITERAL', repr(REJECTIONS))
    payloads = {'NOTE.md': b'Synthetic protocol fixture, not proof evidence.\n',
                'RESULTS.json': baseline.encode(), 'periodic_jet_check.py': source.encode()}
    records = []
    for name, data in payloads.items():
        (packet / name).write_bytes(data)
        records.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'git_blob': blob(data)})
    pin = root / 'synthetic-upstream.txt'; pin.write_bytes(b'synthetic upstream\n')
    meta = {'files': records, 'pins_on_main': [{'path': pin.name, 'git_blob': blob(pin.read_bytes()), 'kind': 'pins_on_main'}]}
    (packet / 'SOURCE_FILES.json').write_text(json.dumps(meta) + '\n')
    return packet


class PeriodicJetWorkflowTests(unittest.TestCase):
    def run_case(self, scenario='valid', stage='M1', mode=(), corrupt=None):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); packet = fixture(root)
            if corrupt == 'payload': (packet / 'NOTE.md').write_bytes(b'changed\n')
            if corrupt == 'pin': (root / 'synthetic-upstream.txt').write_bytes(b'changed\n')
            if corrupt == 'extra': (packet / 'extra.txt').write_bytes(b'extra\n')
            env = dict(os.environ, FLAGS=' '.join(['-B', *mode, '-S']),
                       PJ_TEST_SCENARIO=scenario, PJ_TEST_STAGE=stage)
            return subprocess.run([sys.executable, '-B', *mode, '-S', '-c', driver(WORKFLOW.read_text())],
                                  cwd=root, env=env, capture_output=True, timeout=15)

    def test_valid_protocol_both_modes(self):
        self.assertEqual(len(CHECKS), 27)
        for mode in ((), ('-O',)):
            with self.subTest(mode=mode):
                p = self.run_case(mode=mode)
                self.assertEqual(p.returncode, 0, p.stderr.decode())
                self.assertIn(b'periodic jet replay: manifest, pins, replay and mutants PASS', p.stdout)
                self.assertEqual(p.stderr, b'')

    def test_crashes_are_not_intended_rejections(self):
        for mode in ((), ('-O',)):
            for label in REJECTIONS:
                with self.subTest(mode=mode, label=label):
                    p = self.run_case('crash', label, mode)
                    self.assertNotEqual(p.returncode, 0, 'workflow accepted a mutant crash')

    def check_mutant_contract(self, label):
        scenarios = ('stderr', 'empty', 'garbage', 'passed_true', 'passed_int', 'wrong_reason',
                     'missing_check', 'extra_check', 'check_int', 'extra_failure', 'missing_failure',
                     'wrong_object', 'wrong_precision', 'wrong_effect', 'extra_field', 'missing_field',
                     'checks_list', 'root_list', 'nan', 'duplicate', 'overflow', 'trailing', 'wrong_exit')
        for mode in ((), ('-O',)):
            for case in scenarios:
                with self.subTest(mode=mode, label=label, scenario=case):
                    p = self.run_case(case, label, mode)
                    self.assertNotEqual(p.returncode, 0, f'workflow accepted {label}/{case}')

    def test_contract_M1(self):
        self.check_mutant_contract('M1')

    def test_contract_M2(self):
        self.check_mutant_contract('M2')

    def test_contract_M3(self):
        self.check_mutant_contract('M3')

    def test_contract_M4(self):
        self.check_mutant_contract('M4')

    def test_unknown_label_is_exact(self):
        for mode in ((), ('-O',)):
            for case in ('m9_wrong', 'm9_whitespace', 'stderr', 'wrong_exit', 'crash'):
                with self.subTest(mode=mode, scenario=case):
                    self.assertNotEqual(self.run_case(case, 'M9', mode).returncode, 0)

    def test_baseline_and_custody_still_fail_closed(self):
        for mode in ((), ('-O',)):
            for case in ('baseline_changed', 'baseline_stderr', 'wrong_exit'):
                with self.subTest(mode=mode, scenario=case):
                    self.assertNotEqual(self.run_case(case, 'baseline', mode).returncode, 0)
            for corrupt in ('payload', 'pin', 'extra'):
                with self.subTest(mode=mode, corruption=corrupt):
                    self.assertNotEqual(self.run_case(mode=mode, corrupt=corrupt).returncode, 0)

    def test_workflow_runs_regressions_and_retains_controls(self):
        text = WORKFLOW.read_text()
        self.assertIn("- 'tests/test_periodic_jet_workflow.py'", text)
        self.assertIn('-m unittest discover -s tests -p test_periodic_jet_workflow.py -v', text)
        self.assertIn("flags: ['-B -S', '-B -O -S']", text)
        self.assertIn('set -euo pipefail', text)
        self.assertIn('contents: read', text)
        self.assertIn('persist-credentials: false', text)
        self.assertNotIn('continue-on-error', text)
        compile(driver(text), str(WORKFLOW), 'exec')


if __name__ == '__main__':
    unittest.main()
