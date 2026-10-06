"""Finite source-law controls, not a Gaussian model or kernel execution."""
from collections import defaultdict
from fractions import Fraction as F
import hashlib
from pathlib import Path
import re
import unittest
HERE=Path(__file__).resolve().parent
NAMES=['support_transfer','ninth_integrable_iff','ninth_integral_eq','outer_inputs']
class Tests(unittest.TestCase):
 def test_contract_identity(self):
  d=(HERE/'Contract.lean').read_bytes()
  self.assertEqual(hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest(),
                   '45469b859b65876fa890aa8a5a9edf3c6d4c536e')
 def test_source_inventory_no_admission(self):
  s=re.sub(r'/\-.*?\-/','',(HERE/'CapI4ResidualLaw.lean').read_text(),flags=re.S)
  self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe)\b',s))
  self.assertIn(re.findall(r'^theorem (\w+)',s,re.M),[[],NAMES])
 def test_pushforward_collisions_mass_and_ninth_moment(self):
  for mass in [F(0),F(1,7),F(1),F(17)]:
   for values in [(F(1),F(1),F(3)),(F(-2),F(1),F(-2)),(F(0),F(0),F(0))]:
    weights=[mass*F(1,2),mass*F(1,3),mass*F(1,6)]
    marginal=defaultdict(F)
    for j,w in zip(values,weights):marginal[j]+=w
    self.assertEqual(sum(marginal.values()),mass)
    self.assertEqual(sum(w*abs(j)**9 for j,w in zip(values,weights)),
                     sum(w*abs(j)**9 for j,w in marginal.items()))
    self.assertEqual(all(j>=1 for j,w in zip(values,weights) if w>0),
                     all(j>=1 for j,w in marginal.items() if w>0))
 def test_null_exceptions_not_global_support(self):
  atoms=[(F(-100),F(0)),(F(1),F(1,3)),(F(2),F(2,3))]
  self.assertFalse(all(j>=1 for j,w in atoms))
  self.assertTrue(all(j>=1 for j,w in atoms if w>0))
  self.assertEqual(sum(w*abs(j)**9 for j,w in atoms),F(1,3)+F(2,3)*512)
 def test_unit_mass_and_mean_are_not_ninth_moment_or_support(self):
  self.assertFalse(F(0)>=1) # Dirac at zero has unit mass but not J>=1.
  for t in [F(2),F(4),F(8)]:
   p=1/t
   self.assertEqual(p*t,1)
   self.assertEqual(p*t**9,t**8)
   self.assertGreater(p*t**9,1)
if __name__=='__main__':unittest.main(verbosity=2)
