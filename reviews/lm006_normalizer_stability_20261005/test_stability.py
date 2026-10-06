"""Exact finite controls for the endpoint-weight stability note; not Lean."""
import importlib.util
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
import random
import subprocess
import sys
import unittest

PATH=Path(__file__).with_name('stability_check.py')
class StabilityTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(PATH.is_file(), 'stability implementation has not been supplied')
        spec=importlib.util.spec_from_file_location('stability_check', PATH)
        self.m=importlib.util.module_from_spec(spec); spec.loader.exec_module(self.m)

    def test_physical_typed_weight(self):
        for values in itertools.product((-1,0,1), repeat=6):
            v=tuple(map(F,values))
            for r in (F(1,8),F(1,2),F(1)):
                self.assertEqual(self.m.weight(v,r),self.m.physical_weight(v,r))

    def test_singular_and_type_boundary(self):
        for q in map(F,(-2,-1,0,1,2)):
            for a in map(F,(-3,0,4)):
                v=(F(-1),F(1),-a/2,a/2,q,q)
                self.assertEqual(self.m.weight(v,0),max(-q,F(0))**2)
        # Index decisions may alternate while the determinant-weighted value converges.
        for n in (2,3,4,8,16):
            q=F((-1)**n,n)
            v=(F(-1),F(1),F(0),F(0),q,q)
            self.assertLessEqual(self.m.weight(v,F(1,n)),F(1,n*n))

    def test_parameter_error(self):
        rng=random.Random(310301)
        for _ in range(300):
            v=tuple(F(rng.randrange(-8,9),4) for _ in range(6))
            r,s=F(rng.randrange(9),8),F(rng.randrange(9),8)
            self.assertLessEqual(abs(self.m.weight(v,r)-self.m.weight(v,s)),abs(r-s)*self.m.norm_sq(v)**2)

    def test_vector_error_squared_envelope(self):
        rng=random.Random(478)
        for _ in range(500):
            v=tuple(F(rng.randrange(-6,7),3) for _ in range(6))
            w=tuple(F(rng.randrange(-6,7),3) for _ in range(6))
            r,s=F(rng.randrange(5),4),F(rng.randrange(5),4)
            excess=max(abs(self.m.weight(v,r)-self.m.weight(w,s))-abs(r-s)*self.m.norm_sq(w)**2,F(0))
            d2=self.m.norm_sq(tuple(a-b for a,b in zip(v,w)))
            self.assertLessEqual(excess**2,8*(self.m.norm_sq(v)+self.m.norm_sq(w))**3*d2)

    def test_quartic_envelope(self):
        for values in itertools.product((-1,0,1),repeat=6):
            v=tuple(map(F,values))
            for r in (F(0),F(1,2),F(1)):
                self.assertGreaterEqual(self.m.weight(v,r),0)
                self.assertLessEqual(self.m.weight(v,r),self.m.norm_sq(v)**2)

    def test_gaussian_even_moments(self):
        for d,want in ((1,15),(2,48),(3,105),(6,480)):
            self.assertEqual(self.m.normal_norm_even(d,3),want)
        self.assertEqual(self.m.normal_norm_even(6,2),48)
        self.assertEqual(self.m.normal_norm_even(6,4),5760)

    def test_moving_mean_is_load_bearing(self):
        # Zero covariances do not imply equal Gaussian laws when their means differ.
        a=(F(-1),F(1),F(0),F(0),F(-1),F(-1))
        b=(F(-1),F(1),F(0),F(0),F(-2),F(-2))
        self.assertEqual(self.m.weight(a,0),1)
        self.assertEqual(self.m.weight(b,0),4)
        self.assertGreater(self.m.affine_gap_sq(a,((F(0),),)*6,b,((F(0),),)*6),0)

    def test_factor_coupling_identity(self):
        # Average over all +/-1 vectors has covariance I: exact second-moment identity.
        a=tuple(map(F,(-1,1,0,0,-1,-1))); b=tuple(x+F(1,5) for x in a)
        A=tuple(tuple(F((i+2*j)%5-2,3) for j in range(2)) for i in range(6))
        B=tuple(tuple(F((2*i+j)%7-3,4) for j in range(2)) for i in range(6))
        actual=F(0)
        for z in itertools.product((-1,1),repeat=2):
            diff=tuple(a[i]-b[i]+sum((A[i][j]-B[i][j])*z[j] for j in range(2)) for i in range(6))
            actual+=self.m.norm_sq(diff)/4
        self.assertEqual(actual,self.m.affine_gap_sq(a,A,b,B))

    def test_positive_limit_needed(self):
        for q,expected in ((-1,1),(0,0),(1,0)):
            self.assertEqual(self.m.weight(tuple(map(F,(-1,1,0,0,q,q))),0),expected)

    def test_input_validation(self):
        for v,r in [((0,)*5,F(1)),((0,)*6,F(-1)),((0,)*6,F(2)),((True,)*6,F(1)),((0.0,)*6,F(1))]:
            with self.assertRaises((TypeError,ValueError)): self.m.weight(v,r)
        with self.assertRaises(ValueError): self.m.physical_weight((0,)*6,F(0))

    def test_cli_baseline_and_mutants(self):
        for flags in (['-B','-S'],['-B','-O','-S']):
            out=subprocess.run([sys.executable,*flags,str(PATH)],capture_output=True,text=True,timeout=25)
            self.assertEqual(out.returncode,0,out.stderr); self.assertEqual(out.stderr,'')
            self.assertGreater(json.loads(out.stdout)['total'],0)
            for mutant in ('M1','M2','M3','M4','M5'):
                bad=subprocess.run([sys.executable,*flags,str(PATH),'--mutant',mutant],capture_output=True,text=True,timeout=25)
                self.assertEqual(bad.returncode,1,(mutant,bad.stdout,bad.stderr))
                self.assertTrue(bad.stderr.startswith('STABILITY_FAIL:'),(mutant,bad.stderr))

    def test_unknown_arguments(self):
        for args in (['--mutant','M9'],['--bogus'],['--mutant']):
            p=subprocess.run([sys.executable,'-B','-S',str(PATH),*args],capture_output=True,text=True)
            self.assertEqual(p.returncode,2)

if __name__=='__main__': unittest.main()
