"""Finite exact controls for the d=2 transverse mesoscopic chart."""
from fractions import Fraction as Q
import json
from pathlib import Path
import unittest
import mesoscopic_chart as m

ROOT = Path(__file__).resolve().parent


class MesoscopicChartControls(unittest.TestCase):
    def test_refuses_inexact(self):
        for x in (True, False, 0.5, '1', None):
            with self.assertRaises(TypeError):
                m.exact(x)

    def test_annulus_and_pins(self):
        self.assertTrue(m.in_annulus(m.point(0, 2), 2, 4))
        self.assertFalse(m.in_annulus(m.point(0, 1), 2, 4))
        self.assertFalse(m.away_from_pins(m.point(Q(1, 2), 0)))
        self.assertTrue(m.away_from_pins(m.point(0, 2)))

    def test_transverse_chart_rejects_axis(self):
        self.assertFalse(m.transverse_chart_ok(m.point(2, 0)))
        self.assertFalse(m.transverse_chart_ok(m.point(Q(1, 2), Q(1, 100))))
        self.assertTrue(m.transverse_chart_ok(m.point(0, 2)))

    def test_scaling_powers(self):
        scale = m.witness_scaling_determinant_power(2)
        self.assertEqual(scale['gradient_scaling_exponents'], (2, 1))
        self.assertEqual(scale['height_scaling_exponent'], 2)
        self.assertEqual(scale['gradient_jacobian_r_power'], 3)
        self.assertEqual(scale['spatial_volume_r_power'], 2)
        self.assertEqual(scale['height_window_r_power'], 3)
        with self.assertRaises(ValueError):
            m.witness_scaling_determinant_power(3)

    def test_contact_rows_sample(self):
        rows = m.contact_rows(m.point(0, 2), gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4)
        self.assertEqual(rows['J_grad_y'], 4)
        self.assertEqual(rows['J_grad_x'], 8)  # 0 + 0 + (1/2)*4*4
        self.assertEqual(rows['J_height'], 4)

    def test_contact_rows_general(self):
        y = m.point(2, 2)
        k, a, b, c = Q(2), Q(3), Q(5), Q(7)
        rows = m.contact_rows(y, gap_mark=k, f_yy=a, f_xxy=b, f_xyy=c)
        self.assertEqual(rows['J_grad_y'], a * 2)
        self.assertEqual(rows['J_grad_x'], 6 * k * 4 + b * 4 + (c * 4) / 2)
        self.assertEqual(rows['J_height'], (a * 4) / 2)

    def test_height_dependency_identity(self):
        for y in m.sample_points():
            rows = m.contact_rows(y, gap_mark=3, f_yy=5, f_xxy=7, f_xyy=11)
            factor = m.height_grad_y_dependency(y)
            self.assertEqual(rows['J_height'], factor * rows['J_grad_y'])

    def test_rank_symbols(self):
        rank = m.contact_gradient_rank_symbol(m.point(2, Q(1, 2)))
        # |y|=sqrt(4+0.25)>2? sqrt(4.25)>2 yes; |y2|=1/2 >= 1/4
        self.assertEqual(rank['grad_y_coefficient_f_yy'], Q(1, 2))
        self.assertEqual(rank['grad_x_coefficient_k'], 24)
        self.assertTrue(rank['height_dependent_on_grad_y_at_this_order'])
        self.assertEqual(rank['independent_grad_rows_expected'], 2)

    def test_outside_chart_refused(self):
        with self.assertRaises(ValueError):
            m.contact_rows(m.point(2, 0), gap_mark=1, f_yy=1, f_xxy=0, f_xyy=0)
        with self.assertRaises(ValueError):
            m.contact_rows(m.point(0, Q(1, 10)), gap_mark=1, f_yy=1, f_xxy=0, f_xyy=0)

    def test_gap_mark_positive(self):
        with self.assertRaises(ValueError):
            m.contact_rows(m.point(0, 2), gap_mark=0, f_yy=1, f_xxy=0, f_xyy=0)

    def test_ledger_flags(self):
        led = m.ledger_for_point(m.point(0, 2))
        self.assertFalse(led['height_row_independent_at_this_order'])
        self.assertFalse(led['hessian_ledger_evaluated'])
        self.assertFalse(led['full_annulus_closed'])
        self.assertFalse(led['legacy_24jet_discharged'])
        self.assertTrue(led['complements_pr7'])

    def test_results_bytes(self):
        payload = m.result()
        pinned = json.loads((ROOT / 'RESULTS.json').read_text())
        self.assertEqual(payload, pinned)
        self.assertEqual(payload['gradient_jacobian_r_power'], 3)
        self.assertTrue(payload['sample_points_ok'])

    def test_sample_points_cover_signs(self):
        ys = m.sample_points()
        self.assertTrue(any(y[1] > 0 for y in ys))
        self.assertTrue(any(y[1] < 0 for y in ys))
        self.assertTrue(all(m.transverse_chart_ok(y) for y in ys))


if __name__ == '__main__':
    unittest.main()
