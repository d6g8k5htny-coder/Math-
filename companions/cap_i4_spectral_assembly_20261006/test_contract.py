"""Source/finite controls; not a Lean proof or a Gaussian simulation."""
from pathlib import Path
from fractions import Fraction as Q
import re, unittest
HERE=Path(__file__).resolve().parent
NAMES=['radial_positive_tonelli','entry_spectral_radial','entry_positive_spectral_lintegral','density_positive_spectral_bound']
class ContractTests(unittest.TestCase):
 def source(self):
  p=HERE/'CapI4SpectralAssembly.lean'
  self.assertTrue(p.is_file(),'missing spectral assembly implementation')
  return p.read_text()
 def test_inventory(self):
  self.assertEqual(re.findall(r'^theorem (\w+)',self.source(),re.M),NAMES)
 def test_no_admissions_or_assumed_transport(self):
  s=re.sub(r'/\-.*?\-/','',self.source(),flags=re.S)
  self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe)\b',s))
  self.assertNotIn('MatrixDepthTransport',s)
 def test_source_interfaces_and_measure(self):
  s=self.source()
  for term in ['traceCoordinates_lintegral','polar_spectral_radial','weighted_positive_chamber_change','Measurable G','∫⁻','ENNReal.ofReal Real.pi']:
   self.assertIn(term,s)
 def test_chamber_and_origin(self):
  for t in [Q(-2),Q(0),Q(1,1000),Q(3)]:
   for r in [Q(-1),Q(0),Q(1,10000),Q(2)]:
    self.assertEqual(0<r<t,0<t-r<t+r)
  self.assertFalse(0<Q(1)<Q(1))
 def test_constants_and_wrong_variants(self):
  self.assertEqual(Q(2)*Q(2)*Q(1,2)*Q(1,2),1)
  self.assertNotEqual(Q(2)*Q(2)*Q(1,2),1)
  self.assertNotEqual(Q(2)*Q(1,2)*Q(1,2),1)
 def test_anisotropic_envelope_is_inequality(self):
  for top in [Q(0),Q(1),Q(7,2)]:
   for p in [Q(0),top/3,top]:
    for f in [Q(0),Q(1),Q(9)]:self.assertLessEqual(p*f,top*f)
if __name__=='__main__':unittest.main(verbosity=2)
