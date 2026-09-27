import unittest
from fractions import Fraction as Q
import finite_r_contact as m
class T(unittest.TestCase):
 def test_known_point(self):
  gx,_,ga,h=m.corrected(1,2,0,0,0,0,0)
  self.assertEqual(gx,Q(45,2)); self.assertEqual(h,Q(25,2)); self.assertEqual(ga,0)
 def test_pins(self):
  r=Q(1,10);b=Q(7);k=Q(3)
  for u,target in [(Q(-1,2),b),(Q(1,2),b-k*r**3)]:
   f,fx,fz=m.exact_witness(r,b,k,u,0,-2,5,7,11)
   self.assertEqual(f,target);self.assertEqual(fx,0);self.assertEqual(fz,0)
 def test_scaled_rows(self):
  r=Q(1,10); vals=(Q(3),Q(2),Q(1,2),Q(-2),Q(5),Q(7),Q(11))
  k,u,v,a,q,c,d=vals
  f,fx,fz=m.exact_witness(r,0,k,u,v,a,q,c,d)
  gx,gy,ga,h=m.corrected(*vals)
  self.assertEqual(fx/r**2,gx)
  self.assertEqual(f/r**2,a*v*v/Q(2)+r*h)
 def test_axial_transverse(self):
  r=Q(1,13);k=2;u=3;q=5
  _,_,fz=m.exact_witness(r,0,k,u,0,-2,q,0,0)
  self.assertEqual(fz/r**2,m.corrected(k,u,0,-2,q,0,0)[2])
 def test_transverse_leading_offset_order(self):
  r=Q(1,100);k=1;u=2;v=3;a=-2;q=5;c=7;d=11
  _,_,fz=m.exact_witness(r,0,k,u,v,a,q,c,d)
  gy=m.corrected(k,u,v,a,q,c,d)[1]
  self.assertEqual((fz/r)-gy, r*(m.corrected(k,u,v,a,q,c,d)[2]+Q(c)*Q(u)*Q(v)+Q(d)*Q(v*v)/2))
if __name__=='__main__':unittest.main()
