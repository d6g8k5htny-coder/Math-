"""Exact controls for a conditional cubic sign-band bound, not Lean evidence."""
import importlib.util
import itertools
from fractions import Fraction as F
from pathlib import Path
import subprocess
import sys
import unittest

PATH = Path(__file__).with_name('cubic_band.py')

class CubicBandTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(PATH.is_file(), 'cubic-band implementation missing')
        spec = importlib.util.spec_from_file_location('cubic_band', PATH)
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)

    def test_exact_sign_band(self):
        for am,ap,bm,bp,g,r in itertools.product((-2,-1,0,1),(-2,-1,0,1,2),(0,1,2),(0,1,2),(-1,0,1,2),(F(0),F(1,4),F(1))):
            value = self.m.band_integral(am,ap,bm,bp,g,r)
            self.assertGreaterEqual(value,0)
            self.assertLessEqual(value,self.m.band_bound(am,ap,bp,g,r))

    def test_both_constants_are_exact(self):
        self.assertEqual(self.m.band_integral(-1,0,0,1,2,F(1,2)),1)
        self.assertEqual(self.m.band_bound(-1,0,1,2,F(1,2)),1)
        self.assertEqual(self.m.band_integral(-1,-1,0,0,1,0),F(1,6))
        self.assertEqual(self.m.band_bound(-1,-1,0,1,0),F(1,6))

    def test_sign_support_and_singular_edges(self):
        for t,g in itertools.product((F(-1),F(0),F(1,2),F(1),F(2)),(-1,0,1)):
            value = self.m.weight((-1,1,1,1,t-g,t),F(1,4))
            if t>=0 and value>0:
                self.assertLess(t,g)
        self.assertEqual(self.m.band_integral(0,-1,0,1,1,1),0)
        self.assertEqual(self.m.band_integral(-1,1,0,0,1,0),0)

    def test_hermite_inverses(self):
        for m,want in ((2,16),(3,2048)):
            v=self.m.hermite(m)
            self.assertEqual(self.m.determinant(v),want)
            self.assertEqual(self.m.matmul(v,self.m.inverse(v)),self.m.identity(2*m))

    def test_all_monomial_recoveries(self):
        for m in (2,3):
            for h in (F(1,2),F(1,4),F(1,8),F(1,16)):
                for degree in range(2*m):
                    p=[F(int(i==degree)) for i in range(2*m)]
                    self.assertEqual(self.m.recover(p,m,h),[F(self.m.factorial(j) if j==degree else 0) for j in range(2*m)])

    def test_gaussian_schur_and_confluent_limit(self):
        for h in (F(1,2),F(1,4),F(1,8),F(1,16)):
            rows,target=self.m.observation_rows(h)
            self.assertEqual(self.m.residual_variance(rows,target),1+h**4/4)
            self.assertEqual(len(rows),11)
            self.assertGreater(self.m.determinant(self.m.gram(rows)),0)

    def test_missing_contact_mode_is_not_uniform(self):
        for h in (F(1,2),F(1,4),F(1,8)):
            rows,target=self.m.observation_rows(h,drop_q=True)
            self.assertEqual(self.m.residual_variance(rows,target),h**4/4)

    def test_gaussian_moment_constants(self):
        for k,want in ((2,3),(4,105),(6,10395)):
            self.assertEqual(self.m.centered_even(k),want)
            for m,s in itertools.product((0,1,2),(0,1,2)):
                self.assertLessEqual(self.m.noncentral_even(m,s,k),want*(m*m+s*s)**k)

    def test_cubic_example_integral(self):
        for r in (F(1),F(1,2),F(1,4),F(1,8),F(1,16)):
            self.assertEqual(self.m.band_integral(-1,1,-1,1,3*r,r),F(5,6)*r**3)
        self.assertEqual(F(5,6)/F(1,2),F(5,3))

    def test_marginal_density_counterexample(self):
        actual,false_bound=self.m.marginal_counterexample()
        self.assertEqual(actual,F(1,6))
        self.assertEqual(false_bound,F(9,64))
        self.assertGreater(actual,false_bound)

    def test_invalid_inputs(self):
        for r in (-1,2,True,0.5):
            with self.assertRaises((ValueError,TypeError)):
                self.m.band_integral(-1,1,0,1,1,r)
        with self.assertRaises(ValueError): self.m.recover([1],3,0)
        with self.assertRaises(ValueError): self.m.inverse([[1,1],[1,1]])

    def test_cli_and_intended_rejections(self):
        reasons=['BAND_R_COEFFICIENT','BAND_CUBIC_COEFFICIENT','HERMITE_DERIVATIVE_SCALE','GAUSSIAN_TWELFTH','CONDITIONAL_NOT_MARGINAL','MARGINAL_DENSITY_NOT_SUFFICIENT']
        for flags in (['-B','-S'],['-B','-O','-S']):
            p=subprocess.run([sys.executable,*flags,str(PATH)],capture_output=True,timeout=30)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(p.stderr,b'')
            for j,reason in enumerate(reasons,1):
                p=subprocess.run([sys.executable,*flags,str(PATH),'--mutant','M'+str(j)],capture_output=True,timeout=30)
                self.assertEqual(p.returncode,1)
                self.assertEqual(p.stderr,('CUBIC_BAND_FAIL: '+reason+'\n').encode())
                self.assertEqual(p.stdout,b'')
            for args in (['--mutant','M9'],['--bogus'],['--mutant']):
                p=subprocess.run([sys.executable,*flags,str(PATH),*args],capture_output=True,timeout=30)
                self.assertEqual(p.returncode,2)

if __name__=='__main__': unittest.main()
