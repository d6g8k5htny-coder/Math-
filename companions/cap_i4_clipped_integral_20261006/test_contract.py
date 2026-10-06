"""Exact finite polynomial/boundary controls, not a substitute for the Lean proofs."""
from fractions import Fraction as F
import hashlib
from pathlib import Path
import re
import unittest
HERE=Path(__file__).resolve().parent
NAMES=['gap_integral_exact','clipped_integral_nonneg','clipped_integral_le',
       'full_chamber_integral','moving_prefactor_le','clipped_lintegral_eq']

def primitive(a,b,T):
    return T*a**3/3+T*b*a**2/2-a**4/4-b*a**3/3

def polynomial_integral(a,b,T):
    coefficients=[F(1)]
    for factor in ([F(0),F(1)],[b,F(1)],[T,F(-1)]):
        new=[F(0)]*(len(coefficients)+len(factor)-1)
        for i,x in enumerate(coefficients):
            for j,y in enumerate(factor): new[i+j]+=x*y
        coefficients=new
    return sum((q*a**(i+1)/F(i+1) for i,q in enumerate(coefficients)),F(0))

class ContractTests(unittest.TestCase):
    def test_contract_identity(self):
        self.assertEqual(hashlib.sha256((HERE/'Contract.lean').read_bytes()).hexdigest(), '01e5498258031e5d9f7c8bfc8b5b6dba20f2090c0182c4141efac278900915fe')
    def test_source_scope(self):
        s=(HERE/'CapI4ClippedIntegral.lean').read_text()
        names=re.findall(r'^theorem (\w+)',s,re.M)
        self.assertIn(names,[[],NAMES])
        s=re.sub(r'/\-.*?\-/','',s,flags=re.S)
        self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe)\b',s))
    def test_polynomial_identity_all_signs(self):
        for a in map(F,[-3,-1,0,1,2,5]):
            for b in map(F,[-2,0,1,4]):
                for T in map(F,[-1,0,2,5]):
                    self.assertEqual(primitive(a,b,T),polynomial_integral(a,b,T))
    def test_clipped_domain_nonnegative_and_upper_bound(self):
        for T in [F(0),F(1,10000),F(1,2),F(1),F(4)]:
            for L in [F(0),T/10,T,2*T,10*T]:
                for b in [F(0),F(1,10),F(2),F(10)]:
                    value=primitive(min(T,L),b,T)
                    self.assertGreaterEqual(value,0)
                    self.assertLessEqual(value,T*(L**3/3+b*L**2/2))
                    self.assertEqual(primitive(T,b,T),T**4/12+b*T**3/6)
    def test_moving_bound_and_power_accounting(self):
        for A in [F(0),F(1,3),F(2)]:
            for T in [F(0),F(1,100),F(3)]:
                for r in [F(0),F(1,100),F(1),F(2)]:
                    for D,E,U in [(F(0),F(1),F(2)),(F(2),F(0),F(3)),(F(1),F(2),F(1,2)),(F(2),F(3),F(4))]:
                        L=D*r*U*U;b=E*r*U
                        left=A*r*r*T*U**3*primitive(min(T,L),b,T)
                        right=A*r**5*T*T*(D**3*U**9/3+E*D*D*U**8/2)
                        self.assertLessEqual(left,right)
                        self.assertEqual(A*r*r*T*T*U**3*(L**3/3+b*L*L/2),right)
    def test_false_simplifications_have_explicit_witnesses(self):
        # Carrying the signed gap onto the widened interval gives a negative integral.
        self.assertGreater(primitive(F(1),F(0),F(1)),0)
        self.assertLess(primitive(F(2),F(0),F(1)),0)
        # The mixed soft term is necessary even with a tiny radius and a valid chamber.
        T,L,b=F(1),F(1,100),F(1)
        self.assertGreater(primitive(L,b,T),T*L**3/3)
        self.assertLess(primitive(F(1),F(-2),F(1)),0)
        self.assertNotEqual(primitive(F(1),F(0),F(1)),F(1,6))
    def test_endpoint_and_saturation(self):
        for b in [F(0),F(1),F(100)]:
            self.assertEqual(primitive(F(0),b,F(5)),0)
            self.assertEqual(primitive(min(F(2),F(100)),b,F(2)),primitive(F(2),b,F(2)))
        # Equality cutoff is included, and both eigenvalues may approach zero.
        for n in [10,1000,10**8]:
            T=F(1,n)
            self.assertGreater(primitive(T,F(1),T),0)
if __name__=='__main__':unittest.main(verbosity=2)
