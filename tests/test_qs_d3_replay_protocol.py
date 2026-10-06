"""Real subprocess controls for QS replay; fixtures are not mathematical evidence."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / 'frontiers/qs_d3_soft_layer_chain_20261005/replay.py'


class ReplayProtocolTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('qs_replay_subject', WRAPPER)
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)

    @staticmethod
    def baseline():
        return dict(object='A3 d>=3 hard-fibre reduction (author-side exact controls)',
                    counts={'Z1': 2400, 'Z2': 3600, 'Z3': 4800, 'Z4': 1200},
                    mutant=None, all_pass=True, failures=[], scientific_effect='NONE')

    def invoke(self, scenario='valid'):
        baseline = self.baseline()
        mutant = copy.deepcopy(baseline)
        mutant.update(mutant='Z2', all_pass=False, failures=["('Z2-gain', 17)"])
        invalid = {'error': 'unknown arguments'}
        base_out = (json.dumps(baseline, sort_keys=True) + '\n').encode()
        mut_code, inv_code = 1, 2
        base_err = mut_err = inv_err = b''
        if scenario == 'crash':
            mut_code = 1; mut_err = b'Traceback: synthetic unrelated RuntimeError\n'
            mut_out = b''
        else:
            if scenario == 'wrong_reason': mutant['failures'] = ["('Z4', 17)"]
            elif scenario == 'extra_reason': mutant['failures'].append("('setup', 3)")
            elif scenario == 'wrong_mutant': mutant['mutant'] = 'Z3'
            elif scenario == 'wrong_object': mutant['object'] = 'unrelated'
            elif scenario == 'wrong_effect': mutant['scientific_effect'] = 'ACCEPT'
            elif scenario == 'all_pass': mutant['all_pass'] = True
            elif scenario == 'integer_bool': mutant['all_pass'] = 0
            elif scenario == 'empty_failures': mutant['failures'] = []
            elif scenario == 'failures_string': mutant['failures'] = "('Z2-gain', 17)"
            elif scenario == 'wrong_counts': mutant['counts']['Z1'] = True
            elif scenario == 'missing_counts': del mutant['counts']['Z2']
            elif scenario == 'extra_field': mutant['unexpected'] = 'x'
            elif scenario == 'bad_tuple': mutant['failures'] = ['not a failure tuple']
            elif scenario == 'tuple_prefix_only': mutant['failures'] = ["('Z2-gain-forged', 17)"]
            mut_out = (json.dumps(mutant, sort_keys=True) + '\n').encode()
            if scenario == 'garbage': mut_out = b'unrelated error\n'
            elif scenario == 'trailing': mut_out += b'garbage\n'
            elif scenario == 'duplicate': mut_out = mut_out.replace(b'"all_pass": false', b'"all_pass": false, "all_pass": false')
            elif scenario == 'nonfinite': mut_out = mut_out.replace(b'"Z1": 2400', b'"Z1": NaN')
            elif scenario == 'overflow': mut_out = mut_out.replace(b'"Z1": 2400', b'"Z1": 1e999')
            elif scenario == 'wrong_exit': mut_code = 2
            elif scenario == 'mutant_stderr': mut_err = b'synthetic unexpected stderr\n'
        inv_out = (json.dumps(invalid) + '\n').encode()
        if scenario == 'invalid_crash': inv_out = b''; inv_err = b'Traceback: synthetic error\n'
        elif scenario == 'invalid_wrong_reason': inv_out = b'{"error":"unrelated"}\n'
        elif scenario == 'invalid_extra_field': inv_out = b'{"error":"unknown arguments","extra":1}\n'
        elif scenario == 'invalid_wrong_exit': inv_code = 1
        elif scenario == 'invalid_stderr': inv_err = b'unexpected stderr\n'
        if scenario == 'baseline_stderr': base_err = b'unexpected stderr\n'
        actual_base = base_out if scenario != 'baseline_mismatch' else b'wrong\n'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root/'A3').mkdir()
            script = root/'A3/author_controls.py'
            # Every invocation launches this real isolated child; no subprocess mock.
            script.write_text('import sys\na=sys.argv[1:]\n'
                              f'if not a: out,err,code={actual_base!r},{base_err!r},0\n'
                              f'elif a==["--mutant","Z2"]: out,err,code={mut_out!r},{mut_err!r},{mut_code}\n'
                              f'else: out,err,code={inv_out!r},{inv_err!r},{inv_code}\n'
                              'sys.stdout.buffer.write(out)\nsys.stderr.buffer.write(err)\nsys.exit(code)\n')
            (root/'A3/author_controls_stdout.json').write_bytes(base_out)
            manifest = {'objects': [{'tag': 'A3', 'replays': [{
                'name': 'a3d_exact.py', 'script': 'A3/author_controls.py',
                'stdout': 'A3/author_controls_stdout.json', 'args': [],
                'mutants': [['--mutant','Z2']], 'invalid': [['--bogus']]}]}]}
            return self.m.replay_failures(root, manifest)

    def test_valid_protocol(self):
        self.assertEqual(self.invoke(), [])

    def test_baseline_output_contract(self):
        for scenario in ('baseline_mismatch', 'baseline_stderr'):
            with self.subTest(scenario=scenario): self.assertTrue(self.invoke(scenario))

    def test_crash_is_not_intended_rejection(self):
        self.assertTrue(self.invoke('crash'))

    def test_intended_reason_and_identity(self):
        for scenario in ('wrong_reason','extra_reason','wrong_mutant','wrong_object','wrong_effect',
                         'empty_failures','failures_string','bad_tuple','tuple_prefix_only'):
            with self.subTest(scenario=scenario): self.assertTrue(self.invoke(scenario))

    def test_json_shape_and_types(self):
        for scenario in ('all_pass','integer_bool','wrong_counts','missing_counts','extra_field',
                         'garbage','trailing','duplicate','nonfinite','overflow'):
            with self.subTest(scenario=scenario): self.assertTrue(self.invoke(scenario))

    def test_mutant_exit_and_stderr(self):
        for scenario in ('wrong_exit','mutant_stderr'):
            with self.subTest(scenario=scenario): self.assertTrue(self.invoke(scenario))

    def test_invalid_argument_contract(self):
        for scenario in ('invalid_crash','invalid_wrong_reason','invalid_extra_field',
                         'invalid_wrong_exit','invalid_stderr'):
            with self.subTest(scenario=scenario): self.assertTrue(self.invoke(scenario))

    def test_changed_constant_crash_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root/'A3_6').mkdir()
            proof = b'x'*150
            (root/'A3_6/PROOF.md').write_bytes(proof)
            script = ('from fractions import Fraction as F\nMUT=None\n'
                      'coef = F(1, 4) if MUT == "M5" else F(5, 4)\n'
                      'if coef==F(1,4): raise RuntimeError("synthetic crash")\n'
                      'print("ok")\n')
            (root/'A3_6/author_controls.py').write_text(script)
            (root/'A3_6/author_controls_stdout.json').write_bytes(b'ok\n')
            manifest = {'objects': [{'tag':'A3.6','replays':[], 'stored':[
                {'path':'A3_6/PROOF.md','bytes':len(proof),'sha256':hashlib.sha256(proof).hexdigest()}]}]}
            self.assertTrue(self.m.negative_control_failures(root, manifest))


if __name__ == '__main__':
    unittest.main()
