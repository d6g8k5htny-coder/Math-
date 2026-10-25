"""Exact finite diagnostics; not a Lean or continuum-Gaussian proof."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util,itertools,random,subprocess,sys,unittest

P=Path(__file__).with_name("typed_sign_check.py")
def le_sqrt_sum(x,A,B):
    return x*x<=A+B or (x*x-A-B)**2<=4*A*B

class TypedSignTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(P.is_file(),"typed-sign implementation not supplied")
        s=importlib.util.spec_from_file_location("typed_sign",P)
        self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m)

    def test_physical_identity(self):
        for v in itertools.product((-1,0,1),repeat=6):
            for r in (F(1,4),F(1)):
                self.assertEqual(self.m.weight(v,r),self.m.physical(v,r))

    def test_pointwise_majorant(self):
        for v in itertools.product((-1,0,1),repeat=6):
            for r in (F(0),F(1,4),F(1)):
                q=self.m.weight(v,r) if v[5]>=0 else F(0)
                terms=self.m.terms(v,r)
                self.assertLessEqual(q,sum(terms))

    def test_first_constant_is_sharp(self):
        for r,g in itertools.product((F(1,8),F(1,2),F(1)),(F(1,4),F(1),F(3))):
            v=(-1,1,0,1,-g,0)
            n=self.m.weight(v,r); first,second=self.m.terms(v,r)
            self.assertEqual(n,r*g);self.assertEqual((first,second),(n,0))

    def test_quartic_constant_is_sharp(self):
        for A,g in itertools.product((F(1,4),F(1),F(3)),repeat=2):
            v=(-A,-1,0,0,-g,g)
            n=self.m.weight(v,0); first,second=self.m.terms(v,0)
            self.assertEqual(n,A*g*g);self.assertEqual((first,second),(0,n))

    def test_scalar_product_inequalities(self):
        vals=[F(n,4) for n in range(-12,13)]
        for a in vals:
            self.assertLessEqual(max(-a,F(0)),(a-1)**2/4)
        for c,d in itertools.product(vals,repeat=2):
            if c<=0<=d:self.assertLessEqual((-c)*d,(d-c)**2/4)

    def test_gaussian_eighth(self):
        for m,s2 in itertools.product((F(-2),F(-1),F(0),F(1),F(2)),(F(0),F(1,4),F(1),F(4))):
            exact=self.m.normal_even(m,s2,4)
            self.assertLessEqual(exact,105*(m*m+s2)**4)
        self.assertEqual(self.m.normal_even(0,1,4),105)
        self.assertEqual(self.m.normal_even(2,0,4),256)

    def test_correlated_gaussian_product(self):
        for m,n,s,t in itertools.product((-1,0,1),repeat=4):
            val=self.m.mixed_fourth(m,s,n,t)
            self.assertGreaterEqual(val,0)
            self.assertLessEqual(val,105*(m*m+s*s)**2*(n*n+t*t)**2)
        self.assertEqual(self.m.mixed_fourth(0,1,0,1),105)

    def test_finite_coupling_cauchy_step(self):
        rng=random.Random(2026100516); probs=(F(1,4),F(1,4),F(1,2))
        for _ in range(180):
            vs=[tuple(F(rng.randrange(-6,7),3) for _ in range(6)) for _ in probs]
            r=F(rng.randrange(5),4)
            n=sum(p*self.m.weight(v,r) for p,v in zip(probs,vs) if v[5]>=0)
            k2=sum(p*v[0]**2 for p,v in zip(probs,vs))
            k6=sum(p*v[0]**2*v[3]**4 for p,v in zip(probs,vs))
            g2=sum(p*(v[5]-v[4])**2 for p,v in zip(probs,vs))
            r44=sum(p*(v[1]-1)**4*(v[5]-v[4])**4 for p,v in zip(probs,vs))
            self.assertTrue(le_sqrt_sum(n,r*r*k6*g2,k2*r44/256))

    def test_nongaussian_exception_and_normalization(self):
        p=F(1,1000);e2=8*p
        # Bad and good atoms both have T_r=1, but the error coordinates are not Gaussian.
        self.assertGreater(p*p,F(105,64)*e2**4)
        self.assertEqual(self.m.weight((-1,-1,0,0,-1,1),F(1,2)),1)
        self.assertEqual(self.m.weight((-1,1,0,0,-1,-1),F(1,2)),1)
        n=self.m.weight((-1,-1,0,0,F(-1,2),F(1,2)),0)
        self.assertEqual(n,F(1,4));self.assertEqual(n/n,1)

    def test_invalid_inputs(self):
        for v,r in [((0,)*5,0),((True,)*6,0),((0.0,)*6,0),((0,)*6,-1),((0,)*6,2)]:
            with self.assertRaises((ValueError,TypeError)): self.m.weight(v,r)
        for args in ((0,-1,4),(0,1,-1),(0,1,True)):
            with self.assertRaises((ValueError,TypeError)):self.m.normal_even(*args)
        with self.assertRaises(ValueError):self.m.physical((0,)*6,0)

    def test_cli_baseline_and_mutants(self):
        reasons=["RADIAL_SCALE","QUARTIC_CONSTANT","EVENT_RESTRICTION","GAUSSIAN_EIGHTH",
                 "GAUSSIAN_MEAN","GAUSSIAN_PREMISE_ESSENTIAL","NORMALIZER"]
        previous=None
        for flags in (["-B","-S"],["-B","-O","-S"]):
            b=subprocess.run([sys.executable,*flags,str(P)],capture_output=True,text=True,timeout=20)
            self.assertEqual((b.returncode,b.stderr),(0,""))
            if previous is not None:self.assertEqual(previous,b.stdout)
            previous=b.stdout
            for i,reason in enumerate(reasons,1):
                q=subprocess.run([sys.executable,*flags,str(P),"--mutant",f"M{i}"],capture_output=True,text=True,timeout=20)
                self.assertEqual((q.returncode,q.stdout,q.stderr),(1,"",f"SIGN_FAIL: {reason}\n"))

    def test_cli_invalid(self):
        for flags in (["-B","-S"],["-B","-O","-S"]):
            for args in (["--mutant","M8"],["--bogus"],["--mutant"]):
                p=subprocess.run([sys.executable,*flags,str(P),*args],capture_output=True,text=True,timeout=10)
                self.assertEqual(p.returncode,2)

if __name__=="__main__": unittest.main()
