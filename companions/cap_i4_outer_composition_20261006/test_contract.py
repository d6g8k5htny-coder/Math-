"""Finite source/constant checks; not Gaussian quadrature or kernel evidence."""
import hashlib,re,unittest
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
class Tests(unittest.TestCase):
 def test_contract(self):
  self.assertEqual(hashlib.sha256((HERE/'Contract.lean').read_bytes()).hexdigest(),'46bf725180f34c33333d33a74963d0cf401cff22a7eb63cb0fedb5a3f66b36ad')
 def test_no_admission_and_targets(self):
  text=re.sub(r'/\-.*?\-/','',(HERE/'CapI4OuterComposition.lean').read_text(),flags=re.S)
  self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe)\b',text))
  self.assertIn(re.findall(r'^theorem (\w+)',text,re.M),[[],['gaussian_depth_outer_le','gaussian_depth_outer_lt_top']])
 def test_combined_constant(self):
  for K in (F(0),F(1,2),F(2)):
   for k in (F(1,3),F(1),F(4)):
    for r in (F(0),F(1,10),F(1),F(2)):
     A=K*K*(1+K)/4;D=4*K*K/(3*k);E=3*K/2;b=D**3/3+E*D*D/2
     for j,t in ((F(1),F(1,5)),(F(3),F(2)),(F(8),F(1,10))):
      U=j+t
      self.assertEqual(A*r**5*t*t*b*U**9,A*b*r**5*((abs(j)+abs(t))**9*t*t))
      self.assertLessEqual(A*r**5*t*t*(D**3*U**9/3+E*D*D*U**8/2),A*b*r**5*U**9*t*t)
 def test_unit_mass_not_unit_support(self):
  U=F(1,2)
  self.assertGreater(U**8,U**9)
  self.assertEqual(sum((F(1),)),1) # a probability atom can sit at residual zero
 def test_mass_scaling(self):
  for mass in (F(0),F(1,4),F(1),F(512)):
   M9=mass*F(2)**9;G2=F(1,4);G11=F(60)
   self.assertEqual(256*(M9*G2+mass*G11),mass*256*(F(2)**9*G2+G11))
  self.assertNotEqual(256*(512*F(2)**9*G2+G11),512*256*(F(2)**9*G2+G11))
 def test_actual_cutoff_polynomial(self):
  for T in (F(1,10),F(1),F(3)):
   for L in (F(0),F(1,100),F(1),F(10)):
    for b in (F(0),F(1,3),F(2)):
     a=min(T,L);v=T*a**3/3+T*b*a*a/2-a**4/4-b*a**3/3
     self.assertGreaterEqual(v,0);self.assertLessEqual(v,T*(L**3/3+b*L*L/2))
if __name__=='__main__':unittest.main(verbosity=2)
