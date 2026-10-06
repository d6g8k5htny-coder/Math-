"""Exact finite integration controls and source contracts; not a Lean replay."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import itertools
import re
import unittest
HERE=Path(__file__).resolve().parent
NAMES=['cutoff_gap_lintegral_eq','cutoff_gap_lintegral_le','depth_slice_le',
       'gaussian_depth_slice_le','gaussian_depth_slice_ninth_le']
def primitive(a,b,t):
    return t*a**3/3+t*b*a**2/2-a**4/4-b*a**3/3
class InnerTests(unittest.TestCase):
    def test_exact_contract(self):
        self.assertEqual(hashlib.sha256((HERE/'Contract.lean').read_bytes()).hexdigest(),
          '4ce6d51774aa67053a4c3984aebed4c81fad4e16a222d8a2abe630dab2d0ac38')
    def test_inventory_and_no_admission(self):
        s=(HERE/'CapI4InnerIntegration.lean').read_text()
        s=re.sub(r'/\-.*?\-/','',s,flags=re.S)
        self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe)\b',s))
        self.assertIn(re.findall(r'^theorem (\w+)',s,re.M),[[],NAMES])
    def test_original_domain_and_cutoff_equality(self):
        for t,L,b,x in itertools.product(map(F,[-1,0,1,2]),repeat=4):
            self.assertEqual(0<x<=t and x<=L,0<x<=min(t,L))
        self.assertTrue(0<F(1)<=F(2) and F(1)<=F(1))
    def test_exact_clipped_primitive_and_bound(self):
        count=0
        for t,L,b in itertools.product([F(0),F(1,10),F(1),F(3)],repeat=3):
            a=min(t,L)
            value=primitive(a,b,t)
            # Independent coefficient integration of x(x+b)(t-x).
            coeff=[F(0),b*t,t-b,F(-1)]
            direct=sum(v*a**(i+1)/(i+1) for i,v in enumerate(coeff))
            self.assertEqual(value,direct)
            self.assertGreaterEqual(value,0)
            self.assertLessEqual(value,t*(L**3/3+b*L**2/2))
            count+=1
        self.assertEqual(count,64)
    def test_actual_depth_slice_radius_ledger(self):
        count=0
        for r,K,k0,j,t in itertools.product(
          [F(0),F(1,100),F(1,2),F(1),F(2)],
          [F(0),F(1,2),F(2)],[F(1,3),F(2)],
          [F(0),F(1,2),F(1)],[F(0),F(1,3),F(2)]):
            A=K*K*(1+K)/4;D=4*K*K/(3*k0);E=3*K/2;U=j+t
            L=D*r*U*U;b=E*r*U
            exact=A*r*r*t*U**3*primitive(min(t,L),b,t)
            bound=A*r**5*t*t*(D**3*U**9/3+E*D*D*U**8/2)
            self.assertGreaterEqual(exact,0)
            self.assertLessEqual(exact,bound)
            count+=1
        self.assertEqual(count,270)
    def test_gaussian_drop_has_correct_sign(self):
        for c,x,t in itertools.product([F(0),F(1,10),F(2)],
                                      [F(-3),F(0),F(1,3)],[F(0),F(1),F(2)]):
            self.assertLessEqual(-c*(x*x+t*t),-c*t*t)
    def test_ninth_only_requires_unit_lower_bound(self):
        self.assertGreater(F(1,2)**8,F(1,2)**9)
        for U in [F(1),F(3,2),F(2),F(100)]:
            self.assertLessEqual(U**8,U**9)
        self.assertLess(primitive(F(3),F(1),F(1)),0)
        self.assertGreater(primitive(F(1),F(1),F(1)),0)
if __name__=='__main__':unittest.main(verbosity=2)
