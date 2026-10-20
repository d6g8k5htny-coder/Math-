"""Inert C299 artifact-master controls; never invokes the complete master."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('c299_final_master', Path(__file__).with_name('final_master.py'))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def diagnostic(name):
    conclusion = ('∃ r, r 0 = 0 ∧ ContDiffAt ℝ 2 r 0 ∧ '
        '(∀ᶠ w in 𝓝 0, ∀ (z : ↥V), (fderiv ℝ f (p + w + ↑(r w))) ↑z = 0) ∧ '
        '∀ (w : E d) (z : ↥V), hessian d f p (w + ↑((fderiv ℝ r 0) w)) ↑z = 0')
    target = 'TorusCriticalRidge.exists_negative_partial_gradient_ridge'
    if name == 'WithoutCriticality':
        expression = 'fun hcritical => ' + target + ' f p V hsmooth hcritical hneg'
        premise = 'IsCriticalPoint d f p'
    else:
        expression = target + ' f p V hsmooth hcritical'
        premise = '(∀ v ∈ V, v ≠ 0 → hessian d f p v v < 0)'
    actual = premise + ' → ' + conclusion
    out = (name + '.lean:23:2: error: Type mismatch\n  ' + expression + '\nhas type\n  ' + actual
           + '\nbut is expected to have type\n  ' + conclusion + '\n').encode()
    record = {'stdout_sha256': v.sha(out), 'stderr_sha256': v.sha(b''),
              'expression': expression, 'actual': actual, 'expected': conclusion}
    return out, record


def expected():
    return {'pr': 491, 'head': 'a' * 40, 'base': 'b' * 40, 'tree': 'c' * 40,
            'tested_commit': 'd' * 40, 'tested_tree': 'e' * 40,
            'run_id': 1234, 'run_attempt': 1, 'source_manifest_sha256': 'f' * 64,
            'support_sha256': {path: '1' * 64 for path in v.SUPPORT_PATHS},
            'module_counts': {name: 4 for name in v.MODULES[:-1]},
            'required_ci_names': ['downstream-replay', 'formal / formal-evidence', 'math-downstream-gates'],
            'negative_qualification': {'status': 'QUALIFIED', 'diagnostics': {
                name: diagnostic(name)[1] for name in v.NEGATIVES}}}


class MasterControls(unittest.TestCase):
    def test_actual_expectations_are_required_and_pending_is_rejected(self):
        self.assertTrue(hasattr(v, 'validate_expectations'), 'parameterized final admission is missing')
        v.validate_expectations(expected())
        for change in ('pending', 'missing_support', 'bool_run', 'empty_census', 'missing_ci'):
            bad = copy.deepcopy(expected())
            if change == 'pending': bad['negative_qualification']['status'] = 'PENDING'
            elif change == 'missing_support': bad['support_sha256'].pop(v.WORKFLOW)
            elif change == 'bool_run': bad['run_id'] = True
            elif change == 'empty_census': bad['module_counts']['CriticalRidge'] = 0
            else: bad['required_ci_names'] = []
            with self.subTest(change=change), self.assertRaises(ValueError):
                v.validate_expectations(bad)

    def test_source_bound_negatives_reject_mutation_even_with_rebound_hashes(self):
        self.assertTrue(hasattr(v, 'qualified_negative'), 'qualified negative acceptance is missing')
        for name in v.NEGATIVES:
            out, record = diagnostic(name)
            v.qualified_negative(name, 1, out, b'', record)
            for mutation in ('wrong_exit', 'wrong_file', 'wrong_conclusion', 'wrong_premise', 'extra_error'):
                changed, bound = out, dict(record)
                code = 1
                if mutation == 'wrong_exit': code = 0
                elif mutation == 'wrong_file': changed = out.replace(name.encode() + b'.lean', b'Other.lean')
                elif mutation == 'wrong_conclusion':
                    changed = out.replace('ContDiffAt ℝ 2 r 0'.encode(), b'True')
                    bound['actual'] = bound['actual'].replace('ContDiffAt ℝ 2 r 0', 'True')
                    bound['expected'] = bound['expected'].replace('ContDiffAt ℝ 2 r 0', 'True')
                elif mutation == 'wrong_premise':
                    old = 'IsCriticalPoint d f p' if name == 'WithoutCriticality' else '(∀ v ∈ V, v ≠ 0 → hessian d f p v v < 0)'
                    changed = out.replace((old + ' → ').encode(), 'Continuous f → '.encode())
                    bound['actual'] = bound['actual'].replace(old + ' → ', 'Continuous f → ')
                else: changed += b'Other.lean:1:1: error: unexpected token\n'
                bound['stdout_sha256'] = v.sha(changed)
                with self.subTest(name=name, mutation=mutation), self.assertRaises(ValueError):
                    v.qualified_negative(name, code, changed, b'', bound)

    def test_environment_receipt_binds_selected_values_and_contract(self):
        self.assertTrue(hasattr(v, 'environment_binding'), 'independent environment verification is missing')
        selected = {'PATH': '/tool/bin:/usr/bin', 'LEAN_PATH': '/run/objects:/deps/lib', 'LEAN_NUM_THREADS': '2'}
        contract = {'policy': v.ENVIRONMENT_POLICY, 'retained_lake_lean_path': '/deps/lib',
                    'removed_variable_names': ['LD_PRELOAD', 'LEAN_NUM_THREADS'], 'selected_environment': selected}
        contract['sha256'] = digest(contract)
        phase = {'selected_environment': dict(selected), 'environment_contract_sha256': contract['sha256'],
                 'unexpected_override_names': [], 'environment_validation_error': None,
                 'environment_sha256': digest({'selected_environment': selected, 'unexpected_override_names': []})}
        v.environment_binding({'environment_contract': contract}, phase, '/run/objects')
        for mutation in ('selected', 'loader', 'digest', 'missing_contract', 'order'):
            report, rec = {'environment_contract': copy.deepcopy(contract)}, copy.deepcopy(phase)
            if mutation == 'selected': rec['selected_environment']['LEAN_PATH'] = '/wrong'
            elif mutation == 'loader': rec['unexpected_override_names'] = ['LD_PRELOAD']
            elif mutation == 'digest': rec['environment_sha256'] = '0' * 64
            elif mutation == 'missing_contract': rec['environment_contract_sha256'] = None
            else: report['environment_contract']['removed_variable_names'].reverse()
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                v.environment_binding(report, rec, '/run/objects')

    def test_wrapped_census_rejects_hidden_marker_and_missing_target(self):
        good = ('CRITICAL_RIDGE_AUDIT_MODULE X COUNT 1\n'
                'CRITICAL_RIDGE_AUDIT_DECL X.target AXIOMS [propext,\n Classical.choice,\n Quot.sound]\n'
                'CRITICAL_RIDGE_AUDIT_STANDARD_ONLY_PASS COUNT 1\n')
        self.assertEqual(v.measured_audit(good, ('X',), {'X.target'})['declaration_count'], 1)
        for bad in (good.replace('X.target', 'X.other'), good.replace('Quot.sound]', 'sorryAx]'),
                    good + 'CRITICAL_RIDGE_AUDIT_DECL\tBad AXIOMS [sorryAx]\n',
                    good + 'CRITICAL_RIDGE_AUDIT_DECL0 Bad AXIOMS []\n'):
            with self.assertRaises(ValueError): v.measured_audit(bad, ('X',), {'X.target'})

    def test_runtime_prefix_and_same_path_launcher_cannot_diverge(self):
        report = {'runtimes': {'lean': {'path': '/p/bin/lean', 'bytes': 1, 'sha256': 'a' * 64},
                              'leanchecker': {'path': '/p/bin/leanchecker', 'bytes': 2, 'sha256': 'b' * 64}},
                  'lean_launcher': {'path': '/p/bin/lean', 'bytes': 1, 'sha256': 'a' * 64}}
        v.runtime_binding(report, b'/p\n')
        bad = copy.deepcopy(report);bad['lean_launcher']['sha256'] = 'c' * 64
        with self.assertRaises(ValueError): v.runtime_binding(bad, b'/p\n')
        bad = copy.deepcopy(report);bad['runtimes']['leanchecker']['path'] = '/wrong/bin/leanchecker'
        with self.assertRaises(ValueError): v.runtime_binding(bad, b'/p\n')

    def test_nonpassing_review_or_duplicate_role_file_is_rejected(self):
        reviews = {role: {'path': role + '.md', 'bytes': 1, 'sha256': 'a' * 64, 'verdict': verdict}
                   for role, verdict in v.REVIEW_VERDICTS.items()}
        self.assertEqual(len(v.final_review_records({'reviews': reviews})), 5)
        for mutation in ('hold', 'duplicate'):
            bad = copy.deepcopy(reviews)
            if mutation == 'hold': bad['master_source_review']['verdict'] = 'HOLD_PENDING'
            else: bad['master_source_review']['path'] = bad['source_review']['path']
            with self.assertRaises(ValueError): v.final_review_records({'reviews': bad})

    def test_wrong_source_bytes_fail_without_accepting_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve();(root / 'x').write_bytes(b'abc')
            checker = v.Master(root)
            row = {'path': 'x', 'bytes': 3, 'sha256': v.sha(b'abc')}
            checker.bound(row);(root / 'x').write_bytes(b'abd')
            with self.assertRaises(ValueError): checker.bound(row)

    def test_unrelated_packet_and_cycles_cannot_cover_accepted_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve();(root / 'PACKET').mkdir()
            (root / 'accepted').write_bytes(b'needed');(root / 'other').write_bytes(b'stale')
            (root / 'PACKET/other').write_bytes(b'stale')
            for cycle in (False, True):
                checker = v.Master(root);checker.read('accepted')
                custody = {key: {'path': key, 'bytes': 0, 'sha256': v.sha(b'')}
                           for key in ('archive', 'remote_archive', 'receipt', 'canonical_verification')}
                custody['bindings'] = [{'source_path': 'FINAL_MASTER_INPUTS.json' if cycle else 'other',
                                        'packet_path': 'other'}]
                with self.assertRaisesRegex(ValueError, 'acyclic|every actual accepted input'):
                    checker.verify_custody({'custody': custody})


if __name__ == '__main__':
    unittest.main()
