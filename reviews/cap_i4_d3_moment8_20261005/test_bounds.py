"""Exact finite probes for the separate M8 argument; not continuum or Lean proof."""
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import unittest
P=Path(__file__).resolve().parent
class Checks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.m=None
  if (P/'bounds.py').exists():
   spec=importlib.util.spec_from_file_location('cap_m8',P/'bounds.py');cls.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.m)
 def f(self,name,*args):
  fn=getattr(self.m,name,None);self.assertTrue(callable(fn),'missing helper '+name);return fn(*args)
 def test_partition(self):
  for s in [F(1,64),F(1,3),F(1)]:
   for J in [F(1),1/s,2/s]:
    self.assertEqual(self.f('low_region',s,J),s*s*J*J<=1)
    self.assertNotEqual(self.f('low_region',s,J),s*s*J*J>1)
 def test_low_hard_factor(self):
  for s in [F(1,64),F(1,3),F(1)]:
   for J in [F(1),1/s]:
    for L in [F(1,10**8),F(1),F(5)]:
     for K in [F(1,3),F(1),F(4)]:
      U=J+L; r=s*s
      self.assertLessEqual(L*(L+r*K*U),L*self.f('hard_low',L,K))
 def test_low_integral_identity(self):
  for r in [F(1,4096),F(1,9),F(1)]:
   for J,L in [(F(1),F(1,10**6)),(F(2),F(3))]:
    for K,k in [(F(1),F(1,3)),(F(2),F(3))]:
     D=4*K*K/(3*k);E=3*K/2;U=J+L;a=D*r*U*U
     direct=(K*K/4)*r*r*U*U*L*L*(K+(1+K)*L)*(a**3/3+E*r*U*a*a/2)
     self.assertEqual(direct,self.f('low_integrated',r,J,L,K,k))
 def test_eighth_power_envelope(self):
  for J in [F(1),F(4,3),F(9)]:
   for L in [F(0),F(1,10**6),J,F(2),F(30)]:
    self.assertLessEqual((J+L)**8,self.f('power8',J,L))
  self.assertEqual(self.f('power8',F(1),F(1)),2**8)
 def test_high_polynomial_weight(self):
  for s in [F(1,64),F(1,3),F(1)]:
   r=s*s
   for J in [1/s,2/s,10/s]:
    for L in [F(1,1000),F(1),F(10)]:
     for frac in [F(1,4),F(1)]:
      lam=frac*L;K=F(2);h=K*(J+L)
      source=r*r*h*h/4*lam*(lam+F(3,2)*r*h)*L*(L+r*h)
      self.assertLessEqual(source,self.f('high_polynomial',r,J,L,K))
 def test_tail_moment(self):
  for s in [F(1,64),F(1,3),F(1)]:
   for J in [1/s,2/s,10/s]:
    for q in [2,3,4]:
     self.assertLessEqual(J**q,self.f('tail8',s,J,q))
     if s*J==1:self.assertEqual(J**q,self.f('tail8',s,J,q))
 def test_gaussian_coefficients(self):
  self.assertEqual(self.f('half_gaussian',2,F(1)),(F(1,4),True))
  self.assertEqual(self.f('half_gaussian',3,F(1)),(F(1,2),False))
  self.assertEqual(self.f('half_gaussian',10,F(1)),(F(945,64),True))
  self.assertEqual(self.f('half_gaussian',11,F(1)),(F(60),False))
  for a in [F(1,2),F(1),F(3)]:
   for q in [2,3,4]:
    poly=self.f('tail_gaussian_polynomial',q)
    for L in [F(0),F(1,3),F(2)]:
     self.assertEqual(sum(c*L**degree for degree,c in poly.items()),L**(8-q)*(1+L)**q/2)
   for n in range(10):
    b,flag=self.f('half_gaussian',n,a);c,other=self.f('half_gaussian',n+2,a)
    self.assertEqual(flag,other);self.assertEqual(c,F(n+1,2)/a**2*b)
 def test_tail_radius_ledger(self):
  for s in [F(1,64),F(1,3),F(1)]:
   for q in [2,3,4]:
    self.assertEqual(self.f('tail_radius',s,q),s**(8+q))
    self.assertLessEqual(self.f('tail_radius',s,q),s**10)
 def test_fixed_dyadic_residual(self):
  c=F(255,256)
  for q in [0,2,4,6,7]:
   exact=self.f('dyadic_moment',q)
   partial=sum(c*F(2)**((q-8)*n) for n in range(20))
   self.assertLess(partial,exact);self.assertEqual(exact,c/(1-F(2)**(q-8)))
  self.assertEqual(self.f('dyadic_moment',2),F(85,84))
  for N in [0,1,3,8,20]:self.assertEqual(self.f('truncated_eighth',N),c*(N+1))
  with self.assertRaises(ValueError):self.f('dyadic_moment',8)
 def test_countermodel_band_and_weight(self):
  for N in [0,1,3,8]:
   r=F(1,2**(2*N+1))
   for n in range(N+1):
    J=F(2)**n;upper=r*J*J;self.assertLessEqual(upper,F(1,2))
    for L in [F(1),F(3,2),F(2)]:
     lam=upper/2;W=r*r*J*J*lam*lam*L*L/4
     source=r*r*J*J/4*lam*(lam+F(3,2)*r*J)*L*(L+r*J)
     self.assertLessEqual(W,source);self.assertGreaterEqual(L-lam,F(1,2))
   self.assertEqual(self.f('counter_lower_scaled',N),F(255,256)*(N+1)/12)
 def test_normalization_separate(self):
  for r in [F(1,64),F(1,3),F(1)]:
   C,z,M,k=F(7),F(1,3),F(2),F(4,3)
   d,e=self.f('normalized_bounds',r,C,z,M,k)
   self.assertEqual(d,C/z*r**3);self.assertEqual(e,M/z*(10/(3*k))**4*r**4)
 def test_domain_rejection(self):
  for name,args in [('hard_low',(F(-1),F(1))),('low_region',(F(2),F(1))),('tail8',(F(1,4),F(1),2)),('tail_gaussian_polynomial',(5,)),('normalized_bounds',(F(0),F(1),F(1),F(1),F(1)))]:
   with self.subTest(name=name),self.assertRaises(ValueError):self.f(name,*args)
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks))
 print(json.dumps({'scope':'finite rational controls, not continuum or Lean proof','tests':result.testsRun,'failures':[t.id().split('.')[-1] for t,_ in result.failures],'errors':[t.id().split('.')[-1] for t,_ in result.errors],'success':result.wasSuccessful()},sort_keys=True))
 raise SystemExit(0 if result.wasSuccessful() else 1)
