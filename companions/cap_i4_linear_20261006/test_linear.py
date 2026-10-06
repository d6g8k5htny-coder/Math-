"""Exact finite controls and source contracts, not Lean/kernel execution."""
from fractions import Fraction as F
from pathlib import Path
import re
import unittest
HERE=Path(__file__).resolve().parent
DEFS=['tracePair','spectralPair']
THEOREMS=['tracePair_apply','spectralPair_apply','det_tracePair','det_spectralPair',
 'tracePair_spectralPair','spectralPair_tracePair','map_tracePair','map_spectralPair',
 'lintegral_tracePair','lintegral_spectralPair','positive_chamber_change',
 'weighted_positive_chamber_change']
class LinearTests(unittest.TestCase):
 def source(self):
  p=HERE/'CapI4Linear.lean'
  self.assertTrue(p.is_file(),'missing linear-volume implementation')
  return p.read_text()
 def test_inventory(self):
  s=self.source()
  self.assertEqual(re.findall(r'^def (\w+)',s,re.M),DEFS)
  self.assertEqual(re.findall(r'^theorem (\w+)',s,re.M),THEOREMS)
 def test_actual_measure_theorem(self):
  s=self.source()
  self.assertIn('map_linearMap_addHaar_eq_smul_addHaar',s)
  self.assertIn('setLIntegral_map',s)
  self.assertIn('Measurable G',s)
 def test_no_admission(self):
  s=re.sub(r'/\-.*?\-/','',self.source(),flags=re.S)
  self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe)\b',s))
 def test_determinants(self):
  self.assertEqual(F(1,2)*F(-1,2)-F(1,2)**2,F(-1,2))
  self.assertEqual(F(1)*F(1)-F(-1)*F(1),2)
 def test_inverse_coordinate_relation(self):
  # tracePair spectralPair flips the traceless coordinate, not the identity.
  for t in map(F,[-4,0,1,7]):
   for r in [F(-3),F(0),F(1,1000),F(5)]:
    lo,hi=t-r,t+r
    self.assertEqual(((lo+hi)/2,(lo-hi)/2),(t,-r))
    a,d=t,r
    u,v=(a+d)/2,(a-d)/2
    self.assertEqual((u-v,u+v),(d,a))
 def test_positive_chamber(self):
  for t in [F(-4),F(0),F(1,100),F(2)]:
   for r in [F(-2),F(0),F(1,1000),F(1),F(5)]:
    self.assertEqual(0<r<t,0<t-r<t+r)
 def test_weighted_normalization(self):
  self.assertEqual(F(1,2)*F(1,2),F(1,4))
  self.assertEqual(F(2)*F(2)*F(1,4),1) # remaining angular coefficient is pi
  self.assertNotEqual(F(1,2),F(1))
 def test_all_soft_domains(self):
  for n in [10,1000,10**8]:
   r=F(1,n);t=2*r
   self.assertTrue(0<t-r<t+r)
if __name__=='__main__': unittest.main(verbosity=2)
