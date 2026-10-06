"""Finite algebra and source-contract tests, not kernel evidence."""
from fractions import Fraction as Q
from pathlib import Path
import importlib.util
import re
import unittest

HERE = Path(__file__).resolve().parent
THEOREMS = ['radius_nonneg','radius_sq','continuous_radius','spectrum_ordered',
 'continuous_spectrum','spectrum_sum','spectrum_product','spectrum_sq_sum',
 'continuous_eigenvalues','eigenvalues_sum','eigenvalues_product',
 'positive_trace_measurable','radius_polar','spectrum_polar',
 'polar_spectral_lintegral','polar_positive_lintegral',
 'density_polar_bound','density_positive_polar_bound','integrated_density_polar_bound']
DEFS = ['radius','spectrum','traceCoordinates','eigenvalues']

class PolarChecks(unittest.TestCase):
    def source(self):
        p=HERE/'CapI4Polar.lean'
        self.assertTrue(p.is_file(), 'missing CapI4Polar.lean implementation')
        return p.read_text()
    def test_declaration_inventory(self):
        text=self.source()
        self.assertEqual(re.findall(r'^theorem (\w+)',text,re.M),THEOREMS)
        self.assertEqual(re.findall(r'^def (\w+)',text,re.M),DEFS)
    def test_no_admission(self):
        text=self.source()
        text=re.sub(r'/\-.*?\-/','',text,flags=re.S)
        self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe)\b',text))
        self.assertIn('lintegral_comp_polarCoord_symm',text)
    def test_nonnegative_integrals_and_radius(self):
        text=self.source()
        self.assertIn('∫⁻',text)
        self.assertIn('ENNReal.ofReal p.1',text)
        self.assertIn('polarCoord.target',text)
        self.assertNotIn('MeasureTheory.integral',text)
    def test_trace_and_characteristic(self):
        for t in [Q(-3),Q(0),Q(1,2),Q(5)]:
            for rho in [Q(0),Q(1,10000),Q(3,2),Q(4)]:
                for co,si in [(Q(1),Q(0)),(Q(3,5),Q(4,5))]:
                    a,b,d=t+rho*co,rho*si,t-rho*co
                    lo,hi=t-rho,t+rho
                    self.assertEqual(lo+hi,a+d)
                    self.assertEqual(lo*hi,a*d-b*b)
                    self.assertEqual(lo*lo+hi*hi,a*a+2*b*b+d*d)
                    self.assertLessEqual(lo,hi)
    def test_boundary_not_uniform_gap(self):
        for n in [10,1000,1000000]:
            rho=Q(1,n); t=2*rho
            self.assertGreater(t-rho,0)
            self.assertLess(t+rho,1)
        self.assertEqual(Q(0),0)  # repeated-eigenvalue boundary is retained in coordinates
    def test_false_coordinate_variants(self):
        lo,hi=Q(-1),Q(1) # B=[[0,1],[1,0]]
        self.assertNotEqual(lo,hi)
        self.assertNotEqual(lo*lo+hi*hi,Q(1)) # off-diagonal counts twice
    def test_volume_factors(self):
        self.assertEqual(Q(2)*Q(1,2),1)
        self.assertEqual(Q(2)*Q(1,2)*Q(3,2),Q(3,2))

if __name__=='__main__':
    unittest.main(verbosity=2)
