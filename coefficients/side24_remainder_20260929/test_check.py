"""Regression tests for the additive SIDE24 remainder candidate (stdlib only)."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from fractions import Fraction as F

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("side24_remainder_check", HERE / "check.py")
MOD = None
if SPEC is not None and (HERE / "check.py").is_file():
    MOD = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(MOD)

class RemainderTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(MOD, "Missing exact remainder implementation check.py")

    def test_dimensions_and_homogeneity(self):
        self.assertEqual(MOD.dimensions(2), (6, 2, F(10, 3), F(16, 3)))
        self.assertEqual(MOD.dimensions(3), (10, 4, F(16, 3), F(28, 3)))
        for d in range(2, 13):
            n, k, p, nu = MOD.dimensions(d)
            self.assertEqual((nu-n)/2, F(-1, 3))
            self.assertEqual(n-k, 2*d)

    def test_density_score_scalar_covariance_calibration(self):
        for d in (2, 3, 7):
            first, second = MOD.scalar_score_moments(d)
            self.assertEqual(first, F(-1, 3))
            self.assertEqual(second, F(4, 9))

    def test_second_derivative_majorant(self):
        self.assertEqual(MOD.score_majorant(3), F(1012, 9))
        self.assertLessEqual(MOD.score_majorant(2), MOD.score_majorant(3))
        expected = F(1, 2)*F(1012, 9)*F(16, 9)*F(3125, 243)
        self.assertEqual(MOD.taylor_constant(), expected)
        self.assertLess(expected, 2000)

    def test_first_variation_polynomial_all_fixed_dimensions(self):
        for d in range(2, 21):
            self.assertEqual(MOD.projected_first_variation(d), MOD.closed_first_variation(d))
        self.assertEqual(MOD.closed_first_variation(2), (F(-2), F(3,2), F(-5,36)))
        self.assertEqual(MOD.closed_first_variation(3), (F(-3), F(7,5), F(-2,21)))
        self.assertEqual(MOD.first_variation_at(3,24), F(-620813376,35))
        self.assertEqual(MOD.first_variation_at(2,24), F(-26045568))

    def test_normalization_generates_second_order_term(self):
        L=24
        self.assertEqual(MOD.normalize_linear(F(-1),2*(L*L-1),F(2)),
                         (F(-1),F(2*L*L),F(-4*L*L)))
        # Formal-series multiplication, independent of any numerical q.
        a0,a1,s=F(5,7),F(-3,2),F(4,3)
        c0,c1,c2=MOD.normalize_linear(a0,a1,s)
        self.assertEqual((c0,c1+s*c0,c2+s*c1),(a0,a1,F(0)))

    def test_image_bounds_include_normalizer(self):
        z=F(1,10**125)
        data=MOD.image_bounds()
        self.assertEqual(data['B'],76*24**6+15)
        self.assertEqual(data['E'],F(21175738586478,10**125))
        self.assertEqual(data['deep_shell_coefficient'],541)
        self.assertEqual(data['normalization_coefficient'],6*1458)
        self.assertEqual(data['remainder_coefficient'],541+6*1458)
        self.assertLess(746496*z*z,1)
        self.assertLess(F(3,2)**9*z**5,F(1,2))
        self.assertLess(512*z**3,F(1,2))

    def test_exponential_bounds_prove_decimal_brackets(self):
        lo,_=MOD.exp_bounds(F(288,125),20)
        _,hi=MOD.exp_bounds(F(16,7),40)
        self.assertGreater(lo,10)
        self.assertLess(hi,10)
        qlo,qhi=MOD.q_interval()
        self.assertGreater(qlo,F(1,10**126))
        self.assertLess(qhi,F(1,10**125))
        self.assertLess(qhi-qlo,F(1,10**250))
        # Independent larger Taylor truncation must overlap the certified interval.
        elo,ehi=MOD.exp_bounds(F(9,32),110)
        exact_lo=(1/ehi)**1024
        exact_hi=(1/elo)**1024
        self.assertLessEqual(qlo,exact_hi)
        self.assertGreaterEqual(qhi,exact_lo)

    def test_final_bound_and_sign(self):
        data=MOD.image_bounds()
        expected=2000*data['epsilon']**2+F(29,3)*data['rho']
        self.assertEqual(MOD.remainder_bound(),expected)
        self.assertGreater(expected,0)
        self.assertLess(expected,F(1,10**216))
        for d in (2,3):
            lo,hi=MOD.correction_interval(d)
            self.assertLess(lo,hi)
            self.assertLess(hi,0)
            self.assertGreater(lo,F(-1,10**117))
            self.assertLess(hi,F(-1,10**119))

    def test_outward_grid_in_both_signs(self):
        for x in (F(1,3), F(-1,3), F(0), F(17,5)):
            lo,hi=MOD.outward(x,20)
            self.assertLessEqual(lo,x)
            self.assertGreaterEqual(hi,x)
            self.assertLessEqual(hi-lo,F(1,10**20))

    def test_invalid_inputs_fail_closed(self):
        for value in (True,1.5,'1',None):
            with self.assertRaises((TypeError,ValueError)):
                MOD.exact(value)
        for d in (True,1,0,-1,F(3,2)):
            with self.assertRaises((TypeError,ValueError)):
                MOD.dimensions(d)
        with self.assertRaises(ValueError):
            MOD.exp_bounds(F(-1),10)
        with self.assertRaises(ValueError):
            MOD.exp_bounds(F(20),2)

    def test_cli_both_modes_and_semantic_mutants(self):
        outputs=[]
        for flags in (['-B','-S'],['-B','-O','-S']):
            proc=subprocess.run([sys.executable,*flags,str(HERE/'check.py')],capture_output=True,check=False,timeout=30)
            self.assertEqual(proc.returncode,0,proc.stderr.decode())
            data=json.loads(proc.stdout)
            self.assertTrue(data['passed'])
            self.assertFalse(data['scientific_acceptance'])
            outputs.append(proc.stdout)
            for mutant in MOD.MUTANTS:
                bad=subprocess.run([sys.executable,*flags,str(HERE/'check.py'),'--mutant',mutant],capture_output=True,timeout=30)
                self.assertEqual(bad.returncode,1,(mutant,bad.stdout,bad.stderr))
            unknown=subprocess.run([sys.executable,*flags,str(HERE/'check.py'),'--mutant','UNKNOWN'],capture_output=True,timeout=30)
            self.assertEqual(unknown.returncode,2)
        self.assertEqual(outputs[0],outputs[1])
        if (HERE/'RESULTS.json').is_file():
            self.assertEqual(outputs[0],(HERE/'RESULTS.json').read_bytes())

if __name__=='__main__':
    unittest.main()
