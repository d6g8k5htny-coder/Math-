"""Finite chamber/constant controls, not Lebesgue or Lean proof evidence."""
from fractions import Fraction as F
import hashlib,re,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
NAMES=['positive_chamber_lintegral','gaussian_depth_plane_eq','gaussian_depth_plane_le','gaussian_depth_plane_lt_top']
class Tests(unittest.TestCase):
 def test_contract(self):
  self.assertEqual(hashlib.sha256((HERE/'Contract.lean').read_bytes()).hexdigest(),'1149c5823fa4e1dd6f500f5d013b5c9a881a4f209b15a01b907dd75935c176f6')
 def test_inventory_no_admission(self):
  s=re.sub(r'/\-.*?\-/','',(HERE/'CapI4ChamberBridge.lean').read_text(),flags=re.S)
  self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe)\b',s))
  self.assertIn(re.findall(r'^theorem (\w+)',s,re.M),[[],NAMES])
 def test_discrete_chamber_reordering(self):
  grid=[F(i,3) for i in range(-4,5)]
  for j in [F(0),F(1),F(3)]:
   g=lambda x,t: (j+x+2*t)**2
   plane=sum(g(x,t) for x in grid for t in grid if 0<x<t)
   nested=sum(sum(g(x,t) for x in grid if 0<x<t) for t in grid if 0<t)
   self.assertEqual(plane,nested)
 def test_triangle_monomials_and_orientation(self):
  for p in range(5):
   for q in range(5):
    # Integral x^p*T^q*(T-x) over 0<x<T<1; two elementary orders.
    inner=F(1,(p+1)*(p+2)*(p+q+3))
    other=F(1,q+2)*(F(1,p+1)-F(1,p+q+3))-F(1,q+1)*(F(1,p+2)-F(1,p+q+3))
    self.assertEqual(inner,other)
  self.assertNotEqual(F(1,2*3*4),F(1,1*2*4))
 def test_strict_domain_and_cutoff_equality(self):
  for t in [F(-1),F(0),F(1,10),F(2)]:
   for x in [F(-1),F(0),t/2,t,2*t]:
    self.assertEqual(0<x<t,(0<t and 0<x and x<t))
  x,L=F(1,4),F(1,4)
  self.assertTrue(x<=L);self.assertFalse(x<L)
 def test_unrestricted_residual_mass_in_equality(self):
  for mass in [F(0),F(1,4),F(1),F(7)]:
   a,b=F(5,3),F(7,2)
   self.assertEqual(mass*(3*a+3*b),3*mass*(a+b))
 def test_r5_and_support_not_changed(self):
  self.assertGreater(F(1,2)**8,F(1,2)**9)
  for r in [F(0),F(1,10),F(1),F(2)]:
   A,D,E=F(3,2),F(4,5),F(3,7)
   coeff=256*3*A*(D**3/3+E*D**2/2)
   self.assertEqual(coeff*r**5,256*3*A*r**5*(D**3/3+E*D**2/2))
if __name__=='__main__':unittest.main(verbosity=2)
