"""Exact finite Gaussian regression controls; not the periodic-field proof."""
import importlib.util
from fractions import Fraction as F
from pathlib import Path
import unittest

PATH = Path(__file__).with_name('regression_rate_check.py')
R = [F(1, 2**j) for j in range(7)]

class RegressionRateTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(PATH.is_file(), 'missing regression-rate implementation')
        spec = importlib.util.spec_from_file_location('regression_rate_check', PATH)
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)

    def test_pin_means_and_zero_pin_residual(self):
        m = self.m
        for r in R:
            q = m.model(r)
            self.assertEqual(m.mv(q['raw_pins'], q['field_mean']),
                             [F(6,5),0,0,F(6,5)-r**3/6,0,0])
            self.assertEqual(m.norm2(m.mm(q['raw_pins'],q['field_factor'])),0)

    def test_adjusted_and_physical_endpoints_agree_after_pins(self):
        m=self.m
        for r in R:
            q=m.model(r)
            self.assertEqual(m.mv(q['physical'],q['field_mean']),q['mean'])
            self.assertEqual(m.mm(q['physical'],q['field_factor']),q['factor'])

    def test_regression_schur_and_independence(self):
        m=self.m
        for r in R+[F(0)]:
            q=m.model(r)
            self.assertEqual(m.mm(q['factor'],m.tr(q['P'])),m.zeros(6,6))
            self.assertEqual(m.mm(q['factor'],m.tr(q['factor'])),q['covariance'])

    def test_singular_contact_is_allowed(self):
        m=self.m;q=m.model(F(0))
        self.assertEqual(q['mean'],[-1,1,0,0,0,0])
        self.assertEqual(m.rank(q['covariance']),2)
        self.assertEqual(q['factor'][0],m.zeros(1,12)[0])
        self.assertEqual(q['factor'][1],m.zeros(1,12)[0])
        self.assertEqual(q['factor'][2],[-x for x in q['factor'][3]])
        self.assertEqual(q['factor'][4],q['factor'][5])

    def test_positive_radius_full_rank(self):
        for r in R:
            self.assertEqual(self.m.rank(self.m.model(r)['covariance']),6)

    def test_second_order_pin_and_first_order_endpoint_bounds(self):
        m=self.m;q0=m.model(F(0))
        for r in R:
            q=m.model(r)
            self.assertLessEqual(m.norm2(m.sub(q['P'],q0['P'])), r**4)
            self.assertLessEqual(m.norm2(m.sub(q['V'],q0['V'])), r**2)
            self.assertLessEqual(m.error2(q,q0),2*r**2)
            # This toy law has a nonzero linear displacement contribution.
            self.assertGreaterEqual(m.error2(q,q0),r**2/4)

    def test_mean_term_cannot_be_dropped(self):
        m=self.m
        self.assertEqual(m.error2({'mean':[F(2)],'factor':[[F(0)]]},
                                  {'mean':[F(0)],'factor':[[F(0)]]}),4)

    def test_common_factor_cannot_be_replaced_by_marginal_covariance(self):
        m=self.m
        self.assertEqual(m.error2({'mean':[F(0)],'factor':[[F(1)]]},
                                  {'mean':[F(0)],'factor':[[F(-1)]]}),4)

    def test_kernel_constants(self):
        self.assertEqual(self.m.kernel_constants(),
                         {'pin5_mass':F(1),'pin5_second_half':F(1,40),
                          'average_second_half':F(1,24),
                          'endpoint_abs_first':F(1,8)})

    def test_invalid_radius_and_singular_pin_matrix(self):
        for r in [F(-1),F(2)]:
            with self.assertRaises(ValueError):self.m.model(r)
        with self.assertRaises(ValueError):self.m.inv([[F(1),F(1)],[F(1),F(1)]])

if __name__=='__main__':
    unittest.main()
