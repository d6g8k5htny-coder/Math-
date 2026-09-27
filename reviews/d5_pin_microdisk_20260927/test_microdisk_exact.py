"""Exact algebra checks for the bounded D5 microdisk note."""
from fractions import Fraction as Q
from pathlib import Path
import json
import unittest
import microdisk_exact as m


class MicrodiskTests(unittest.TestCase):
    def test_exact_contract(self):
        for bad in (True, False, 0.5, '1/2', None):
            with self.assertRaises(TypeError):
                m.exact(bad)
        self.assertEqual(m.exact(3), Q(3))

    def test_gradient_rows_match_raw_scaling(self):
        vals = (Q(1, 7), Q(2), Q(1, 5), Q(1, 3), Q(5), Q(7), Q(11), Q(13))
        r, k, p, q, az, t, c, d = vals
        gx, gz = m.gradient_rows(*vals)
        fx, fz = m.raw_gradient(*vals)
        self.assertEqual(fx, r * r * gx)
        self.assertEqual(fz, r * gz)

    def test_divided_difference_rows_reconstruct_gradient(self):
        vals = (Q(1, 9), Q(3), Q(1, 4), Q(2, 5), Q(5), Q(7), Q(11), Q(13))
        r, _, _, q, _, _, _, _ = vals
        dx, dz = m.divided_difference_rows(*vals)
        fx, fz = m.raw_gradient(*vals)
        self.assertEqual(fx, r * r * q * dx)
        self.assertEqual(fz, r * q * dz)

    def test_reduced_frame_minor_is_half_minus_p(self):
        self.assertEqual(m.reduced_frame_minor_az_t(Q(1, 17), Q(1, 5), Q(2, 7)), Q(3, 10))
        self.assertEqual(m.reduced_frame_minor_az_t(Q(1, 17), Q(0), Q(2, 7)), Q(1, 2))

    def test_minor_stays_positive_on_endpoint_disk(self):
        for p in (Q(-1, 4), Q(-1, 10), Q(0), Q(1, 10), Q(1, 4)):
            self.assertGreater(m.reduced_frame_minor_az_t(Q(1, 13), p, Q(1, 3)), 0)

    def test_nested_microdisk_rows_have_exact_limit_form(self):
        r, k, P, Qcoord = Q(1, 19), Q(3), Q(2), Q(5)
        az, t, c, d = Q(7), Q(11), Q(13), Q(17)
        dx, dz = m.nested_divided_difference_rows(r, k, P, Qcoord, az, t, c, d)
        self.assertEqual(dx - (-6 * k * P / Qcoord - t / 2), r * (6 * k * P * P / Qcoord + t * P + c * Qcoord / 2))
        self.assertEqual(dz - az, r * (-t * P / (2 * Qcoord) - c / 2 + r * (t * P * P / (2 * Qcoord) + c * P + d * Qcoord / 2)))

    def test_jacobian_scales_match_nested_substitution(self):
        r, q, Qcoord = Q(1, 23), Q(2, 7), Q(5)
        self.assertEqual(m.jacobian_scale(r, q), r ** 3 * q * q)
        self.assertEqual(m.nested_jacobian_scale(r, Qcoord), m.jacobian_scale(r, r * Qcoord))

    def test_axis_solution_solves_gradient_rows(self):
        r, k, q, c, d = Q(1, 29), Q(2), Q(3, 7), Q(5), Q(11)
        az, t = m.axis_witness_solution(r, q, c, d)
        gx, gz = m.gradient_rows(r, k, Q(0), q, az, t, c, d)
        self.assertEqual(gx, 0)
        self.assertEqual(gz, 0)

    def test_axis_q_factors_match_exact_formulas(self):
        r, k, q, c, d = Q(1, 31), Q(3), Q(2, 9), Q(5), Q(7)
        factors = m.axis_q_factors(r, k, q, c, d)
        self.assertEqual(factors['M'], r * r * (3 * k * d - c * c * q / 4))
        self.assertEqual(factors['X'], r * r * (-3 * k * d - c * c * q / 4 + c * d * q * q / 2))

    def test_axis_product_has_exact_q_squared_softness(self):
        r, k, q, c, d = Q(1, 37), Q(4), Q(3, 8), Q(5), Q(7)
        dets = m.axis_witness_determinants(r, k, q, c, d)
        self.assertEqual(dets['M'] * dets['X'] * dets['S'], q * q * m.axis_product_without_q2(r, k, q, c, d))

    def test_q_zero_is_rejected_by_off_axis_frame(self):
        with self.assertRaises(ValueError):
            m.divided_difference_rows(1, 1, 0, 0, 1, 1, 1, 1)
        with self.assertRaises(ValueError):
            m.reduced_frame_matrix(1, 0, 0)
        with self.assertRaises(ValueError):
            m.axis_witness_solution(1, 0, 1, 1)

    def test_results_metadata(self):
        data = m.result()
        self.assertTrue(data['two_point_divided_difference_frame'])
        self.assertTrue(data['off_axis_frame_nondegenerate'])
        self.assertFalse(data['uniform_microdisk_majorant_closed'])
        self.assertFalse(data['all_height_O_r3_pin_neighborhood_closed'])
        self.assertEqual(data, json.loads((Path(__file__).with_name('RESULTS.json')).read_text()))


if __name__ == '__main__':
    unittest.main(verbosity=2)
