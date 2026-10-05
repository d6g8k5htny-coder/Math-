"""Exact controls for the disjoint orthogonal-positivity supplement."""
from fractions import Fraction as F
from itertools import product
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('positive_tau',ROOT/'positive_tau.py')
tau=importlib.util.module_from_spec(spec)
spec.loader.exec_module(tau)
LAWS=[(1,3,15),(F(5,2),F(17,2),F(65,2)),(1,1,1),
      (F(199,100),F(10099,100),F(1000099,100))]

class PositiveTauTests(unittest.TestCase):
    def test_direct_schur(self):
        for d in range(1,6):
            for v in [(1,)*d,tuple(range(1,d+1)),tuple((-1)**i*(i+1) for i in range(d))]:
                norm2=sum(x*x for x in v)
                t=tuple(F(x*x,norm2) for x in v)
                for moments in LAWS:
                    self.assertEqual(tau.decomposed_variance(*moments,t),tau.direct_schur(*moments,v))

    def test_dimension_free_band_and_simplex_floor(self):
        for d in range(1,7):
            for moments in LAWS:
                lo,hi,delta=tau.variance_band(*moments)
                for t in tau.simplex_grid(d,5):
                    value=tau.decomposed_variance(*moments,t)
                    self.assertGreaterEqual(value,lo)
                    self.assertGreaterEqual(value,delta/d**2)
                    self.assertLessEqual(value,hi)

    def test_monomial_weights_sum_to_one(self):
        for d in range(1,6):
            for t in tau.simplex_grid(d,7):
                w=tau.monomial_weights(t)
                self.assertEqual(sum(w),1)
                self.assertGreaterEqual(min(w),0)

    def test_gaussian_band_is_exact(self):
        self.assertEqual(tau.variance_band(1,3,15),(6,6,6))
        for d in range(1,10):
            self.assertEqual(tau.decomposed_variance(1,3,15,(F(1,d),)*d),6)

    def test_zero_floor_not_falsely_positive(self):
        self.assertEqual(tau.variance_band(1,1,1),(0,6,0))
        self.assertEqual(tau.decomposed_variance(1,1,1,(F(1,2),)*2),0)

    def test_delta_alone_is_not_a_dimension_free_floor(self):
        moments=LAWS[-1]
        _,_,delta=tau.variance_band(*moments)
        value=tau.decomposed_variance(*moments,(F(1,2),)*2)
        self.assertLess(value,delta)

    def test_polynomial_summands_are_orthogonal(self):
        a,b,c=map(F,LAWS[1]);u=[F(1,3),F(2,3),F(2,3)]
        rows=[]
        for xs in product(map(F,[-2,-1,1,2]),repeat=3):
            parts=[u[i]**3*(xs[i]**3-(b/a)*xs[i]) for i in range(3)]
            parts += [3*u[i]**2*u[j]*(xs[i]**2-a)*xs[j]
                      for i in range(3) for j in range(3) if i!=j]
            parts += [6*u[0]*u[1]*u[2]*xs[0]*xs[1]*xs[2]]
            y=sum(u[i]*xs[i] for i in range(3))
            projection=sum((3*a*u[i]+(b/a-3*a)*u[i]**3)*xs[i] for i in range(3))
            self.assertEqual(sum(parts),y**3-projection)
            rows.append(parts)
        for i in range(10):
            self.assertEqual(sum(row[i] for row in rows),0)
            for j in range(i): self.assertEqual(sum(row[i]*row[j] for row in rows),0)
        var=sum(sum(row)**2 for row in rows)/len(rows)
        self.assertEqual(var,tau.decomposed_variance(a,b,c,tuple(x*x for x in u)))

    def test_invalid_input(self):
        for moments in [(0,1,1),(1,0,1),(1,3,8),(1.0,3,15),(True,3,15)]:
            with self.assertRaises((ValueError,TypeError)):tau.variance_band(*moments)
        for t in [(),(1,1),(-1,2),(.5,.5)]:
            with self.assertRaises((ValueError,TypeError)):tau.decomposed_variance(1,3,15,t)

    def test_cli_controls_both_modes(self):
        good=[]
        for flags in [[],['-O']]:
            def run(*args):
                return subprocess.run([sys.executable,'-B',*flags,'-S',str(ROOT/'positive_tau.py'),*args],
                                      capture_output=True,text=True,timeout=20)
            r=run();self.assertEqual(r.returncode,0,r.stderr);good.append(r.stdout)
            self.assertTrue(json.loads(r.stdout)['passed'])
            for label in ['M1','M2','M3','M4']:
                r=run('--mutant',label)
                self.assertEqual(r.returncode,1,(label,r.stdout,r.stderr))
                self.assertIn('POSITIVE_TAU_FAIL',r.stderr)
            self.assertEqual(run('--mutant','M9').returncode,2)
        self.assertEqual(good[0],good[1])

if __name__=='__main__':unittest.main()
