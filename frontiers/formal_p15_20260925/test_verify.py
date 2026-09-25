"""Runner controls, not additional mathematical theorem claims."""
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import tempfile
import unittest
from verify import (VerificationError, Z3, build_query, check_response,
                    exact_eval, parse_expr, smt_rational, validate_case, verify_parent)

CASES = json.loads((Path(__file__).parent/'SPEC.json').read_text())['cases']

class RunnerControls(unittest.TestCase):
    def test_parent_identity_accepts_exact_bytes(self):
        raw=b'original\n'
        binding={'size_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
                 'git_blob_sha1':hashlib.sha1(b'blob 9\0'+raw).hexdigest()}
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'proof.md'; path.write_bytes(raw)
            self.assertEqual(verify_parent(path,binding),binding)
    def test_parent_identity_rejects_changed_bytes(self):
        raw=b'original\n'
        binding={'size_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
                 'git_blob_sha1':hashlib.sha1(b'blob 9\0'+raw).hexdigest()}
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'proof.md'; path.write_bytes(b'amended!\n')
            with self.assertRaises(VerificationError):
                verify_parent(path,binding)
    def test_all_explicit_witnesses_exact(self):
        for case in CASES:
            with self.subTest(case=case['id']):
                validate_case(case)
    def test_p_one_boundary_is_zero(self):
        p=m=Fraction(0)
        p=Fraction(1)
        self.assertEqual((1-p)**2*m-p*p*m, 0)
        validate_case(next(c for c in CASES if c['id']=='M_STRICT_AT_P_ONE'))
    def test_reversed_sign_witness_is_minus_three_eighths(self):
        p,m,n=Fraction(3,4),Fraction(1),Fraction(3)
        self.assertEqual((1-p)**2*n-p*p*m, Fraction(-3,8))
    def test_weakened_curvature_witness_is_positive(self):
        a,b,x=Fraction(-1),Fraction(2),Fraction(1)
        self.assertEqual(-a*b*x/(a+b*x)**2, 2)
    def test_no_command_injection(self):
        with self.assertRaises(VerificationError):
            parse_expr('(>= a 0) (assert false)', {'a'})
    def test_no_include(self):
        with self.assertRaises(VerificationError):
            parse_expr('(include secret)', set())
    def test_no_unknown_symbol(self):
        with self.assertRaises(VerificationError):
            parse_expr('(>= hidden 0)', {'a'})
    def test_unclosed_expression_rejected(self):
        with self.assertRaises(VerificationError):
            parse_expr('(> a 0', {'a'})
    def test_wrong_arity_rejected(self):
        with self.assertRaises(VerificationError):
            parse_expr('(not (> a 0) (> a 1))', {'a'})
    def test_zero_division_rejected(self):
        with self.assertRaises(VerificationError):
            exact_eval(parse_expr('(/ 1 0)',set()), {})
    def test_bad_witness_rejected(self):
        case=copy.deepcopy(CASES[1]);case['witness']['c']='2'
        with self.assertRaises(VerificationError):
            validate_case(case)
    def test_float_witness_rejected(self):
        case=copy.deepcopy(CASES[1]);case['witness']['c']=-0.25
        with self.assertRaises(VerificationError):
            validate_case(case)
    def test_missing_witness_binding_rejected(self):
        case=copy.deepcopy(CASES[1]);del case['witness']['a']
        with self.assertRaises(VerificationError):
            validate_case(case)
    def test_duplicate_variable_rejected(self):
        case=copy.deepcopy(CASES[1]);case['variables'].append('a')
        with self.assertRaises(VerificationError):
            validate_case(case)
    def test_unknown_solver_result_not_success(self):
        with self.assertRaises(VerificationError):
            check_response('unknown\n', 'unsat')
    def test_unsat_without_proof_not_success(self):
        with self.assertRaises(VerificationError):
            check_response('unsat\n', 'unsat')
    def test_solver_error_not_success(self):
        with self.assertRaises(VerificationError):
            check_response('sat\n(error "bad")', 'sat')
    def test_wrong_polarity_not_success(self):
        with self.assertRaises(VerificationError):
            check_response('sat\n()', 'unsat')
    def test_theorem_checks_negation(self):
        query, expected=build_query(CASES[1])
        self.assertEqual(expected, 'unsat')
        self.assertIn('(assert (not (<= c 0)))', query)
        self.assertIn('(get-proof)', query)
    def test_premise_satisfiability_check_has_no_negation(self):
        query, expected=build_query(CASES[1],witness_only=True)
        self.assertEqual(expected, 'sat')
        self.assertNotIn('(assert (not', query)
        self.assertIn('(assert (= c (/ (- 1) 4)))', query)
    def test_rational_serialization(self):
        self.assertEqual(smt_rational('-3/8'), '(/ (- 3) 8)')
        self.assertEqual(smt_rational('0'), '0')
    def test_api_parser_error_returns_exception_not_success(self):
        solver=Z3()
        with self.assertRaises(VerificationError):
            solver.run('(assert (> missing 0))\n(check-sat)\n', 'sat')

if __name__=='__main__':
    unittest.main()
