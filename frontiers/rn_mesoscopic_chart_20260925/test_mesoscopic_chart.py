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
        axial = m.witness_scaling_determinant_power(2, chart='C_axial')
        self.assertEqual(axial['gradient_scaling_exponents'], (2, 2))
        self.assertEqual(axial['height_scaling_exponent'], 3)
        self.assertEqual(axial['gradient_jacobian_r_power'], 4)
        with self.assertRaises(ValueError):
            m.witness_scaling_determinant_power(3)
        with self.assertRaises(ValueError):
            m.witness_scaling_determinant_power(2, chart='nope')

    def test_axial_chart_membership(self):
        self.assertTrue(m.axial_chart_ok(m.point(2, 0)))
        self.assertFalse(m.axial_chart_ok(m.point(2, 1)))
        self.assertFalse(m.axial_chart_ok(m.point(Q(1, 2), 0)))
        self.assertFalse(m.transverse_chart_ok(m.point(2, 0)))

    def test_axial_contact_rows(self):
        rows = m.axial_contact_rows(m.point(2, 0), gap_mark=1, f_xxy=4)
        self.assertEqual(rows['J_grad_y'], 8)   # (4*4)/2
        self.assertEqual(rows['J_grad_x'], 24)  # 6*1*4
        self.assertEqual(rows['J_height'], 16)  # 2*1*8
        led = m.axial_ledger_for_point(m.point(-2, 0), gap_mark=2, f_xxy=1)
        self.assertEqual(led['gradient_jacobian_r_power'], 4)
        self.assertTrue(led['height_independent_at_leading_axial_order'])
        self.assertTrue(led['hessian_contact_rows_enumerated'])
        self.assertFalse(led['full_annulus_closed'])

    def test_axial_refuses_transverse_point(self):
        with self.assertRaises(ValueError):
            m.axial_contact_rows(m.point(0, 2), gap_mark=1, f_xxy=1)

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
        self.assertTrue(rank['height_dependent_on_grad_y_at_leading_order'])
        self.assertTrue(rank['height_next_order_enumerated'])
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
        self.assertFalse(led['height_row_independent_at_leading_order'])
        self.assertTrue(led['height_next_order_enumerated'])
        self.assertTrue(led['hessian_contact_rows_enumerated'])
        self.assertFalse(led['hessian_ledger_evaluated'])
        self.assertFalse(led['full_annulus_closed'])
        self.assertFalse(led['legacy_24jet_discharged'])
        self.assertTrue(led['complements_pr7'])

    def test_leading_height_residual_zero(self):
        for y in m.sample_points():
            rows = m.contact_rows(y, gap_mark=3, f_yy=5, f_xxy=7, f_xyy=11, f_yyy=13)
            self.assertEqual(rows['height_residual_at_leading_order'], 0)

    def test_height_next_order_formula(self):
        y = m.point(2, 2)
        k, b, c, d = Q(2), Q(5), Q(7), Q(11)
        rows = m.contact_rows(y, gap_mark=k, f_yy=0, f_xxy=b, f_xyy=c, f_yyy=d)
        expected = 2 * k * 8 + (b * 4 * 2) / 2 + (c * 2 * 4) / 2 + (d * 8) / 6
        self.assertEqual(rows['H_height_next'], expected)
        info = m.height_next_order_independent(
            y, gap_mark=k, f_xxy=b, f_xyy=c, f_yyy=d)
        self.assertEqual(info['H_height_next'], expected)
        self.assertTrue(info['next_order_supplies_height'])
        self.assertTrue(info['explicit_r_factor_still_required'])

    def test_height_next_on_axis_mark_only(self):
        # y=(0,2): H_1 = (1/6) f_yyy y2^3 when k term and mixed y1 terms vanish.
        rows = m.contact_rows(m.point(0, 2), gap_mark=1, f_yy=0, f_xxy=0, f_xyy=0, f_yyy=6)
        self.assertEqual(rows['H_height_next'], 8)  # (6*8)/6 = 8

    def test_results_bytes(self):
        payload = m.result()
        pinned = json.loads((ROOT / 'RESULTS.json').read_text())
        self.assertEqual(payload, pinned)
        self.assertEqual(payload['gradient_jacobian_r_power'], 3)
        self.assertEqual(payload['axial_gradient_jacobian_r_power'], 4)
        self.assertEqual(payload['hessian_raw_det_leading_r_power'], 1)
        self.assertEqual(payload['transverse_net_count_r_power'], 3)
        self.assertEqual(payload['axial_net_count_r_power'], 2)
        self.assertEqual(payload['pin_centered_net_count_r_power'], 3)
        self.assertTrue(payload['sample_points_ok'])
        self.assertTrue(payload['axial_points_ok'])
        self.assertFalse(payload['hessian_sample']['hessian_ledger_evaluated'])
        self.assertTrue(payload['hessian_sample']['hessian_contact_rows_enumerated'])
        self.assertFalse(payload['integrand_power_transverse']['contact_density_bound_proved'])

    def test_sample_points_cover_signs(self):
        ys = m.sample_points()
        self.assertTrue(any(y[1] > 0 for y in ys))
        self.assertTrue(any(y[1] < 0 for y in ys))
        self.assertTrue(all(m.transverse_chart_ok(y) for y in ys))
        self.assertTrue(all(m.axial_chart_ok(y) for y in m.sample_axial_points()))

    def test_annulus_require_pr7_A(self):
        with self.assertRaises(ValueError):
            m.in_annulus(m.point(0, Q(1, 2)), Q(2, 5), 1)
        self.assertTrue(
            m.in_annulus(m.point(0, Q(1, 2)), Q(2, 5), 1, require_pr7_A=False))
        with self.assertRaises(ValueError):
            m.in_annulus(m.point(0, 1), 0, 1, require_pr7_A=False)

    def test_pins_exterior_and_cover(self):
        self.assertTrue(m.pins_exterior_to_annulus(2))
        self.assertFalse(m.pins_exterior_to_annulus(Q(2, 5)))
        self.assertFalse(m.pins_exterior_to_annulus(Q(1, 2)))
        cover = m.chart_cover_report()
        self.assertTrue(cover['pins_exterior_to_annulus'])
        self.assertEqual(cover['enumerated_charts'], ['C_transverse', 'C_axial'])
        self.assertEqual(cover['open_regions'], ['thin_belt_open'])
        self.assertTrue(cover['thin_belt_contact_rows_enumerated'])
        self.assertFalse(cover['thin_belt_uniform_bound_proved'])
        self.assertFalse(cover['cover_complete'])
        self.assertFalse(cover['full_annulus_closed'])
        self.assertFalse(cover['legacy_24jet_discharged'])

    def test_classify_partition(self):
        self.assertEqual(m.classify_annulus_point(m.point(0, 2)), 'C_transverse')
        self.assertEqual(m.classify_annulus_point(m.point(2, 0)), 'C_axial')
        self.assertEqual(m.classify_annulus_point(m.point(2, Q(1, 8))), 'thin_belt_open')
        self.assertEqual(m.classify_annulus_point(m.point(0, 1)), 'outside_annulus')
        # On the PR7 annulus A>1, scaled pins lie outside; a pin-neighbour is exterior.
        self.assertEqual(
            m.classify_annulus_point(m.point(Q(1, 2), Q(1, 20))), 'outside_annulus')
        self.assertEqual(
            m.classify_annulus_point(
                m.point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1, require_pr7_A=False),
            'near_pin')

    def test_thin_belt_conditioning(self):
        self.assertTrue(m.thin_belt_ok(m.point(2, Q(1, 8))))
        self.assertFalse(m.thin_belt_ok(m.point(0, 2)))
        self.assertFalse(m.thin_belt_ok(m.point(2, 0)))
        info = m.thin_belt_conditioning(m.point(2, Q(1, 8)))
        self.assertEqual(info['grad_y_coefficient_y2'], Q(1, 8))
        self.assertEqual(info['conditioning_factor_reciprocal_abs_y2'], 8)
        self.assertEqual(info['status'], 'OPEN_SEPARATE_CHART_REQUIRED')
        with self.assertRaises(ValueError):
            m.thin_belt_conditioning(m.point(0, 2))

    def test_thin_belt_contact_rows(self):
        y = m.point(2, Q(1, 8))
        rows = m.thin_belt_contact_rows(y, gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4)
        self.assertEqual(rows['J_grad_y'], Q(1, 4))  # 2*(1/8)
        self.assertEqual(rows['J_height'], Q(1, 64))  # (2*(1/64))/2
        self.assertEqual(rows['height_residual_at_leading_order'], 0)
        led = m.thin_belt_ledger_for_point(y, gap_mark=1, f_yy=2)
        self.assertEqual(led['chart'], 'C_thin_belt')
        self.assertTrue(led['contact_rows_enumerated'])
        self.assertFalse(led['uniform_integrand_bound_proved'])
        self.assertFalse(led['absorbed_into_C_transverse'])
        self.assertEqual(led['status'], 'OPEN_SEPARATE_CHART_REQUIRED')
        self.assertEqual(led['gradient_jacobian_r_power'], 3)
        with self.assertRaises(ValueError):
            m.thin_belt_contact_rows(m.point(0, 2), gap_mark=1, f_yy=1, f_xxy=0, f_xyy=0)

    def test_thin_belt_reciprocal_shells(self):
        for n in (1, 4, 8, 16):
            info = m.thin_belt_reciprocal_shell_lower_bound(n)
            self.assertEqual(info['integral_lower_bound'], n)
            self.assertEqual(info['eps'], Q(1, 4) / (2 ** n))
            self.assertFalse(info['bare_conditioning_factor_L1_near_zero'])
            self.assertTrue(info['additional_cancellation_required'])
            self.assertFalse(info['uniform_integrand_bound_proved'])
        # Bounds are strictly increasing in the shell count.
        self.assertLess(
            m.thin_belt_reciprocal_shell_lower_bound(3)['integral_lower_bound'],
            m.thin_belt_reciprocal_shell_lower_bound(7)['integral_lower_bound'],
        )
        with self.assertRaises(ValueError):
            m.thin_belt_reciprocal_shell_lower_bound(0)

    def test_jet_map_f_yy_factor(self):
        info = m.jet_map_f_yy_to_J_grad_y_factor(m.point(2, Q(1, 8)))
        self.assertEqual(info['partial_J_grad_y_partial_f_yy'], Q(1, 8))
        self.assertEqual(info['product_abs_factor_times_reciprocal'], 1)
        self.assertTrue(info['cancels_bare_reciprocal_pointwise'])
        self.assertFalse(info['full_density_bound_proved'])
        with self.assertRaises(ValueError):
            m.jet_map_f_yy_to_J_grad_y_factor(m.point(2, 0))

    def test_thin_belt_integrand_residual_after_cancel(self):
        led = m.thin_belt_integrand_residual_after_cancel(m.point(2, Q(1, 8)), shells=8)
        self.assertEqual(led['chart'], 'C_thin_belt')
        self.assertEqual(led['product_abs_factor_times_reciprocal'], 1)
        self.assertEqual(led['residual_geometric_factor_after_cancel'], 1)
        self.assertTrue(led['cancels_bare_reciprocal_pointwise'])
        self.assertTrue(led['residual_geometric_factor_locally_L1'])
        self.assertTrue(led['bare_reciprocal_L1_obstruction_cleared_by_cancel'])
        self.assertEqual(led['dyadic_shell_width_sum'], Q(1, 4) * (1 - Q(1, 256)))
        self.assertFalse(led['uniform_integrand_bound_proved'])
        self.assertFalse(led['contact_gaussian_density_bounded'])
        self.assertFalse(led['full_density_bound_proved'])
        with self.assertRaises(ValueError):
            m.thin_belt_integrand_residual_after_cancel(m.point(0, 2))
        with self.assertRaises(ValueError):
            m.thin_belt_integrand_residual_after_cancel(m.point(2, Q(1, 8)), shells=0)

    def test_transverse_conditioning_uniform_bound(self):
        # Interior point |y2|=2 >> δ=1/4.
        info = m.transverse_conditioning_uniform_bound(m.point(0, 2))
        self.assertEqual(info['abs_y2'], 2)
        self.assertEqual(info['conditioning_reciprocal_abs_y2'], Q(1, 2))
        self.assertEqual(info['uniform_chart_bound'], 4)
        self.assertTrue(info['reciprocal_le_uniform_bound'])
        self.assertTrue(info['chart_conditioning_singularity_cleared'])
        self.assertFalse(info['gaussian_density_factor_bounded'])
        self.assertTrue(info['thin_belt_still_open'])
        # Boundary of the chart: |y2|=δ saturates the uniform bound.
        edge = m.transverse_conditioning_uniform_bound(m.point(2, Q(1, 4)))
        self.assertEqual(edge['conditioning_reciprocal_abs_y2'], 4)
        self.assertEqual(edge['uniform_chart_bound'], 4)
        self.assertTrue(edge['reciprocal_le_uniform_bound'])
        with self.assertRaises(ValueError):
            m.transverse_conditioning_uniform_bound(m.point(2, Q(1, 8)))
        with self.assertRaises(ValueError):
            m.transverse_conditioning_uniform_bound(m.point(2, 0))

    def test_axial_conditioning_uniform_bound(self):
        info = m.axial_conditioning_uniform_bound(m.point(2, 0))
        self.assertEqual(info['abs_y1'], 2)
        self.assertEqual(info['grad_y_coefficient_y1_sq_over_2'], 2)
        self.assertEqual(info['conditioning_reciprocal'], Q(1, 2))
        self.assertEqual(info['uniform_chart_bound'], Q(1, 2))  # 2/A^2 = 2/4
        self.assertTrue(info['reciprocal_le_uniform_bound'])
        self.assertTrue(info['axial_chart_conditioning_singularity_cleared'])
        self.assertFalse(info['axial_gaussian_density_factor_bounded'])
        self.assertTrue(info['axial_area_measure_zero'])
        # Larger |y1| improves the coefficient (smaller reciprocal).
        far = m.axial_conditioning_uniform_bound(m.point(3, 0))
        self.assertEqual(far['grad_y_coefficient_y1_sq_over_2'], Q(9, 2))
        self.assertEqual(far['conditioning_reciprocal'], Q(2, 9))
        self.assertLess(far['conditioning_reciprocal'], info['conditioning_reciprocal'])
        with self.assertRaises(ValueError):
            m.axial_conditioning_uniform_bound(m.point(0, 2))
        with self.assertRaises(ValueError):
            m.axial_conditioning_uniform_bound(m.point(Q(1, 2), 0))

    def test_transverse_height_r_factor_ledger(self):
        y = m.point(0, 2)
        led = m.transverse_height_r_factor_ledger(y, gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0)
        self.assertTrue(led['leading_height_dependent_on_grad_y'])
        self.assertEqual(led['height_dependency_factor_y2_over_2'], 1)
        self.assertEqual(led['J_grad_y'], 4)  # 2*2
        self.assertEqual(led['J_height'], 4)  # (1/2)*2*4
        self.assertEqual(led['height_minus_dep_times_grad_y'], 0)
        self.assertEqual(led['unmatched_height_density_r_power'], 1)
        self.assertTrue(led['explicit_r_factor_still_required'])
        self.assertFalse(led['height_r_absorbed_into_uniform_bound'])
        self.assertTrue(led['next_order_supplies_independent_height'])
        with self.assertRaises(ValueError):
            m.transverse_height_r_factor_ledger(m.point(2, 0))

    def test_thin_belt_height_r_factor_ledger(self):
        led = m.thin_belt_height_r_factor_ledger(m.point(2, Q(1, 8)), gap_mark=1, f_yy=2)
        self.assertEqual(led['chart'], 'C_thin_belt')
        self.assertTrue(led['leading_height_dependent_on_grad_y'])
        self.assertEqual(led['height_dependency_factor_y2_over_2'], Q(1, 16))
        self.assertEqual(led['height_minus_dep_times_grad_y'], 0)
        self.assertEqual(led['J_grad_y'], Q(1, 4))  # f_yy * y2 = 2*(1/8)
        self.assertEqual(led['J_height'], Q(1, 64))  # (f_yy/2)*y2^2 = 1*(1/64)
        self.assertEqual(led['unmatched_height_density_r_power'], 1)
        self.assertTrue(led['explicit_r_factor_still_required'])
        self.assertFalse(led['height_r_absorbed_into_uniform_bound'])
        self.assertTrue(led['bare_reciprocal_L1_obstruction_cleared_by_cancel'])
        self.assertFalse(led['contact_gaussian_density_bounded'])
        with self.assertRaises(ValueError):
            m.thin_belt_height_r_factor_ledger(m.point(0, 2))

    def test_axial_height_independence_ledger(self):
        led = m.axial_height_independence_ledger(m.point(2, 0), gap_mark=1, f_xxy=2)
        self.assertTrue(led['height_independent_at_leading_axial_order'])
        self.assertFalse(led['leading_height_dependent_on_grad_y'])
        self.assertFalse(led['leading_height_dependent_on_grad_x'])
        self.assertEqual(led['unmatched_height_density_r_power'], 0)
        self.assertFalse(led['explicit_r_factor_still_required'])
        self.assertTrue(led['no_unmatched_height_r_at_leading_order'])
        self.assertEqual(led['J_height'], 16)  # 2*k*y1^3 = 2*8
        self.assertEqual(led['J_grad_x'], 24)  # 6*k*y1^2
        self.assertEqual(led['J_grad_y'], 4)   # (y1^2/2)*f_xxy = 2*2
        self.assertTrue(led['axial_area_measure_zero'])
        self.assertFalse(led['contact_gaussian_density_bounded'])
        with self.assertRaises(ValueError):
            m.axial_height_independence_ledger(m.point(0, 2))

    def test_axial_height_grad_x_shared_mark_ledger(self):
        led = m.axial_height_grad_x_shared_mark_ledger(m.point(2, 0), gap_mark=1, f_xxy=2)
        self.assertEqual(led['shared_gap_mark_coordinate'], 'k')
        self.assertEqual(led['height_over_grad_x_factor_y1_over_3'], Q(2, 3))
        self.assertEqual(led['height_minus_y1_over_3_times_grad_x'], 0)
        self.assertEqual(led['J_height'], 16)
        self.assertEqual(led['J_grad_x'], 24)
        self.assertEqual(led['grad_x_scaling_exponent'], 2)
        self.assertEqual(led['height_scaling_exponent'], 3)
        self.assertFalse(led['shared_mark_forces_unmatched_height_r'])
        self.assertEqual(led['unmatched_height_density_r_power'], 0)
        self.assertTrue(led['no_unmatched_height_r_at_leading_order'])
        self.assertFalse(led['contact_gaussian_density_bounded'])
        other = m.axial_height_grad_x_shared_mark_ledger(m.point(-3, 0), gap_mark=2, f_xxy=1)
        self.assertEqual(other['height_minus_y1_over_3_times_grad_x'], 0)
        self.assertEqual(other['height_over_grad_x_factor_y1_over_3'], -1)
        with self.assertRaises(ValueError):
            m.axial_height_grad_x_shared_mark_ledger(m.point(0, 2))

    def test_chart_boundary_transition(self):
        y = m.point(2, Q(1, 4))  # |y2|=floor; in annulus, off pins
        self.assertTrue(m.transverse_chart_ok(y))
        self.assertFalse(m.thin_belt_ok(y))
        tr = m.chart_boundary_transition(y, gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0)
        self.assertEqual(tr['transition_on_contact_rows'], 'identity')
        self.assertEqual(tr['transition_jacobian_determinant'], 1)
        self.assertFalse(tr['singular_transition'])
        self.assertEqual(tr['shared_contact_rows']['J_grad_y'], Q(1, 2))  # 2*(1/4)
        self.assertFalse(tr['uniform_integrand_bound_proved'])
        with self.assertRaises(ValueError):
            m.chart_boundary_transition(m.point(2, Q(1, 8)))

    def test_near_pin_diagnosis_small_A(self):
        with self.assertRaises(ValueError):
            m.near_pin_diagnosis(m.point(Q(1, 2), Q(1, 20)), inner=2, outer=4)
        diag = m.near_pin_diagnosis(m.point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1)
        self.assertEqual(diag['closer_pin'], 'S')
        self.assertEqual(diag['dist2_S'], Q(1, 400))
        self.assertFalse(diag['midpoint_chart_valid'])
        self.assertTrue(diag['requires_pin_centered_divided_differences'])
        self.assertEqual(diag['status'], 'OPEN_SEPARATE_CHART_REQUIRED')
        self.assertFalse(diag['pr7_fixed_annulus_A_gt_1'])
        self.assertFalse(m.near_pin_ok(m.point(0, 2)))

    def test_pin_centered_frame_ledger(self):
        y = m.point(Q(1, 2), Q(1, 20))
        frame = m.pin_centered_frame(y, inner=Q(2, 5), outer=1)
        self.assertEqual(frame['closer_pin'], 'S')
        self.assertEqual(frame['z1'], 0)
        self.assertEqual(frame['z2'], Q(1, 20))
        self.assertEqual(frame['dist2_to_closer_pin'], Q(1, 400))
        led = m.pin_centered_ledger_for_point(
            y, inner=Q(2, 5), outer=1, H_xx=-2, H_xy=0, H_yy=3, f_yyy=6, f_yyyy=24,
            f_yyyyy=120, f_yyyyyy=720, f_yyyyyyy=5040, f_yyyyyyyy=40320, f_yyyyyyyyy=362880,
            f_yyyyyyyyyy=3628800, f_yyyyyyyyyyy=39916800, f_yyyyyyyyyyyy=479001600,
            f_yyyyyyyyyyyyy=6227020800, f_yyyyyyyyyyyyyy=87178291200,
            f_yyyyyyyyyyyyyyy=1307674368000, f_yyyyyyyyyyyyyyyy=20922789888000,
            f_yyyyyyyyyyyyyyyyy=355687428096000, f_yyyyyyyyyyyyyyyyyy=6402373705728000,
            f_yyyyyyyyyyyyyyyyyyy=121645100408832000, f_yyyyyyyyyyyyyyyyyyyy=2432902008176640000,
            f_yyyyyyyyyyyyyyyyyyyyy=51090942171709440000,
            f_yyyyyyyyyyyyyyyyyyyyyy=1124000727777607680000,
            f_yyyyyyyyyyyyyyyyyyyyyyy=25852016738884976640000,
            f_yyyyyyyyyyyyyyyyyyyyyyyy=620448401733239439360000,
            f_yyyyyyyyyyyyyyyyyyyyyyyyy=15511210043330985984000000,
            f_yyyyyyyyyyyyyyyyyyyyyyyyyy=403291461126605635584000000,
            f_yyyyyyyyyyyyyyyyyyyyyyyyyyy=10888869450418352160768000000,
            f_yyyyyyyyyyyyyyyyyyyyyyyyyyyy=304888344611713860501504000000,
            f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyy=8841761993739701954543616000000,
            f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=265252859812191058636308480000000,
            f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=8222838654177922817725562880000000,
            f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=263130836933693530167218012160000000,
            f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=8683317618811886495518194401280000000,
            f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=295232799039604140847618609643520000000)
        self.assertEqual(led['chart'], 'C_pin_centered')
        self.assertFalse(led['midpoint_U0_rows_applicable'])
        self.assertTrue(led['pin_site_jet_rows_enumerated'])
        self.assertTrue(led['pin_site_next_order_enumerated'])
        self.assertTrue(led['pin_site_quartic_enumerated'])
        self.assertTrue(led['pin_site_quintic_enumerated'])
        self.assertTrue(led['pin_site_sextic_enumerated'])
        self.assertTrue(led['pin_site_septic_enumerated'])
        self.assertTrue(led['pin_site_octic_enumerated'])
        self.assertTrue(led['pin_site_nonic_enumerated'])
        self.assertTrue(led['pin_site_decic_enumerated'])
        self.assertTrue(led['pin_site_undecic_enumerated'])
        self.assertTrue(led['pin_site_dodecic_enumerated'])
        self.assertTrue(led['pin_site_tridecic_enumerated'])
        self.assertTrue(led['pin_site_tetradecic_enumerated'])
        self.assertTrue(led['pin_site_pentadecic_enumerated'])
        self.assertTrue(led['pin_site_hexadecic_enumerated'])
        self.assertTrue(led['pin_site_heptadecic_enumerated'])
        self.assertTrue(led['pin_site_octadecic_enumerated'])
        self.assertTrue(led['pin_site_nonadecic_enumerated'])
        self.assertTrue(led['pin_site_icosic_enumerated'])
        self.assertTrue(led['pin_site_henicosic_enumerated'])
        self.assertTrue(led['pin_site_docosic_enumerated'])
        self.assertTrue(led['pin_site_tricosic_enumerated'])
        self.assertTrue(led['pin_site_tetracosic_enumerated'])
        self.assertTrue(led['pin_site_pentacosic_enumerated'])
        self.assertTrue(led['pin_site_hexacosic_enumerated'])
        self.assertTrue(led['pin_site_heptacosic_enumerated'])
        self.assertTrue(led['pin_site_octacosic_enumerated'])
        self.assertTrue(led['pin_site_nonacosic_enumerated'])
        self.assertTrue(led['pin_site_triacontic_enumerated'])
        self.assertTrue(led['pin_site_hentriacontic_enumerated'])
        self.assertTrue(led['pin_site_dotriacontic_enumerated'])
        self.assertTrue(led['pin_site_tritriacontic_enumerated'])
        self.assertTrue(led['pin_site_tetratriacontic_enumerated'])
        self.assertFalse(led['pin_site_higher_jets_enumerated'])
        self.assertTrue(led['contact_rows_enumerated'])
        self.assertEqual(led['enumeration_scope'], 'leading_morse_plus_cubic_through_tetratriacontic')
        self.assertEqual(led['contact_rows']['J_grad_1'], 0)  # H_xy z2 with H_xy=0,z1=0
        self.assertEqual(led['contact_rows']['J_grad_2'], Q(3, 20))  # H_yy z2
        self.assertEqual(led['contact_rows']['J_height'], Q(3, 800))  # (1/2) H_yy z2^2
        self.assertEqual(led['contact_rows']['height_minus_half_z_dot_grad'], 0)
        # z=(0,1/20), f_yyy=6 => H_grad_next_2=(1/2)*6*(1/400)=3/400, H_height_next=(1/6)*6*(1/8000)=1/8000
        self.assertEqual(led['next_order_rows']['H_grad_next_1'], 0)
        self.assertEqual(led['next_order_rows']['H_grad_next_2'], Q(3, 400))
        self.assertEqual(led['next_order_rows']['H_height_next'], Q(1, 8000))
        self.assertEqual(led['next_order_rows']['z_dot_H_grad_next_minus_3_H_height_next'], 0)
        self.assertTrue(led['next_order_rows']['explicit_r_factor_still_required'])
        # z=(0,1/20), f_yyyy=24 => Q_grad_2=(1/6)*24*(1/8000)=1/2000, Q_height=(1/24)*24*(1/160000)=1/160000
        self.assertEqual(led['quartic_rows']['Q_grad_next_1'], 0)
        self.assertEqual(led['quartic_rows']['Q_grad_next_2'], Q(1, 2000))
        self.assertEqual(led['quartic_rows']['Q_height_next'], Q(1, 160000))
        self.assertEqual(led['quartic_rows']['z_dot_Q_grad_next_minus_4_Q_height_next'], 0)
        self.assertEqual(led['quartic_rows']['unmatched_density_r_power'], 2)
        # z=(0,1/20), f_yyyyy=120 => P_grad_2=(1/24)*120*(1/160000)=1/32000,
        # P_height=(1/120)*120*(1/3200000)=1/3200000
        self.assertEqual(led['quintic_rows']['P_grad_next_1'], 0)
        self.assertEqual(led['quintic_rows']['P_grad_next_2'], Q(1, 32000))
        self.assertEqual(led['quintic_rows']['P_height_next'], Q(1, 3200000))
        self.assertEqual(led['quintic_rows']['z_dot_P_grad_next_minus_5_P_height_next'], 0)
        self.assertEqual(led['quintic_rows']['unmatched_density_r_power'], 3)
        # z=(0,1/20), f_yyyyyy=720 => S_grad_2=(1/120)*720*(1/3200000)=3/1600000,
        # S_height=(1/720)*720*(1/64000000)=1/64000000
        self.assertEqual(led['sextic_rows']['S_grad_next_1'], 0)
        self.assertEqual(led['sextic_rows']['S_grad_next_2'], Q(3, 1600000))
        self.assertEqual(led['sextic_rows']['S_height_next'], Q(1, 64000000))
        self.assertEqual(led['sextic_rows']['z_dot_S_grad_next_minus_6_S_height_next'], 0)
        self.assertEqual(led['sextic_rows']['unmatched_density_r_power'], 4)
        # z=(0,1/20), f_yyyyyyy=5040 => T_grad_2=(1/720)*5040*(1/64000000)=7/64000000,
        # T_height=(1/5040)*5040*(1/1280000000)=1/1280000000
        self.assertEqual(led['septic_rows']['T_grad_next_1'], 0)
        self.assertEqual(led['septic_rows']['T_grad_next_2'], Q(7, 64000000))
        self.assertEqual(led['septic_rows']['T_height_next'], Q(1, 1280000000))
        self.assertEqual(led['septic_rows']['z_dot_T_grad_next_minus_7_T_height_next'], 0)
        self.assertEqual(led['septic_rows']['unmatched_density_r_power'], 5)
        # z=(0,1/20), f_yyyyyyyy=40320 => U_grad_2=(1/5040)*40320*(1/1280000000)=1/160000000,
        # U_height=(1/40320)*40320*(1/25600000000)=1/25600000000
        self.assertEqual(led['octic_rows']['U_grad_next_1'], 0)
        self.assertEqual(led['octic_rows']['U_grad_next_2'], Q(1, 160000000))
        self.assertEqual(led['octic_rows']['U_height_next'], Q(1, 25600000000))
        self.assertEqual(led['octic_rows']['z_dot_U_grad_next_minus_8_U_height_next'], 0)
        self.assertEqual(led['octic_rows']['unmatched_density_r_power'], 6)
        # z=(0,1/20), f_yyyyyyyyy=362880 => N_grad_2=(1/40320)*362880*(1/25600000000)=9/25600000000,
        # N_height=(1/362880)*362880*(1/512000000000)=1/512000000000
        self.assertEqual(led['nonic_rows']['N_grad_next_1'], 0)
        self.assertEqual(led['nonic_rows']['N_grad_next_2'], Q(9, 25600000000))
        self.assertEqual(led['nonic_rows']['N_height_next'], Q(1, 512000000000))
        self.assertEqual(led['nonic_rows']['z_dot_N_grad_next_minus_9_N_height_next'], 0)
        self.assertEqual(led['nonic_rows']['unmatched_density_r_power'], 7)
        # z=(0,1/20), f_yyyyyyyyyy=3628800 => D_grad_2=(1/362880)*3628800*(1/512000000000)=1/51200000000,
        # D_height=(1/3628800)*3628800*(1/10240000000000)=1/10240000000000
        self.assertEqual(led['decic_rows']['D_grad_next_1'], 0)
        self.assertEqual(led['decic_rows']['D_grad_next_2'], Q(1, 51200000000))
        self.assertEqual(led['decic_rows']['D_height_next'], Q(1, 10240000000000))
        self.assertEqual(led['decic_rows']['z_dot_D_grad_next_minus_10_D_height_next'], 0)
        self.assertEqual(led['decic_rows']['unmatched_density_r_power'], 8)
        # z=(0,1/20), f_yyyyyyyyyyy=39916800 => E_grad_2=(1/3628800)*39916800*(1/10240000000000)=11/10240000000000,
        # E_height=(1/39916800)*39916800*(1/204800000000000)=1/204800000000000
        self.assertEqual(led['undecic_rows']['E_grad_next_1'], 0)
        self.assertEqual(led['undecic_rows']['E_grad_next_2'], Q(11, 10240000000000))
        self.assertEqual(led['undecic_rows']['E_height_next'], Q(1, 204800000000000))
        self.assertEqual(led['undecic_rows']['z_dot_E_grad_next_minus_11_E_height_next'], 0)
        self.assertEqual(led['undecic_rows']['unmatched_density_r_power'], 9)
        # z=(0,1/20), f_yyyyyyyyyyyy=479001600 => F_grad_2=(1/39916800)*479001600*(1/204800000000000)=12/204800000000000,
        # F_height=(1/479001600)*479001600*(1/4096000000000000)=1/4096000000000000
        self.assertEqual(led['dodecic_rows']['F_grad_next_1'], 0)
        self.assertEqual(led['dodecic_rows']['F_grad_next_2'], Q(12, 204800000000000))
        self.assertEqual(led['dodecic_rows']['F_height_next'], Q(1, 4096000000000000))
        self.assertEqual(led['dodecic_rows']['z_dot_F_grad_next_minus_12_F_height_next'], 0)
        self.assertEqual(led['dodecic_rows']['unmatched_density_r_power'], 10)
        # z=(0,1/20), f_yyyyyyyyyyyyy=6227020800 => G_grad_2=(1/479001600)*6227020800*(1/4096000000000000)=13/4096000000000000,
        # G_height=(1/6227020800)*6227020800*(1/81920000000000000)=1/81920000000000000
        self.assertEqual(led['tridecic_rows']['G_grad_next_1'], 0)
        self.assertEqual(led['tridecic_rows']['G_grad_next_2'], Q(13, 4096000000000000))
        self.assertEqual(led['tridecic_rows']['G_height_next'], Q(1, 81920000000000000))
        self.assertEqual(led['tridecic_rows']['z_dot_G_grad_next_minus_13_G_height_next'], 0)
        self.assertEqual(led['tridecic_rows']['unmatched_density_r_power'], 11)
        # z=(0,1/20), f_yyyyyyyyyyyyyy=87178291200 => I_grad_2=(1/6227020800)*87178291200*(1/81920000000000000)=14/81920000000000000,
        # I_height=(1/87178291200)*87178291200*(1/1638400000000000000)=1/1638400000000000000
        self.assertEqual(led['tetradecic_rows']['I_grad_next_1'], 0)
        self.assertEqual(led['tetradecic_rows']['I_grad_next_2'], Q(7, 40960000000000000))
        self.assertEqual(led['tetradecic_rows']['I_height_next'], Q(1, 1638400000000000000))
        self.assertEqual(led['tetradecic_rows']['z_dot_I_grad_next_minus_14_I_height_next'], 0)
        self.assertEqual(led['tetradecic_rows']['unmatched_density_r_power'], 12)
        # z=(0,1/20), f_yyyyyyyyyyyyyyy=1307674368000 => J_grad_2=(1/87178291200)*1307674368000*(1/1638400000000000000)=15/1638400000000000000,
        # J_height=(1/1307674368000)*1307674368000*(1/32768000000000000000)=1/32768000000000000000
        self.assertEqual(led['pentadecic_rows']['J_grad_next_1'], 0)
        self.assertEqual(led['pentadecic_rows']['J_grad_next_2'], Q(3, 327680000000000000))
        self.assertEqual(led['pentadecic_rows']['J_height_next'], Q(1, 32768000000000000000))
        self.assertEqual(led['pentadecic_rows']['z_dot_J_grad_next_minus_15_J_height_next'], 0)
        self.assertEqual(led['pentadecic_rows']['unmatched_density_r_power'], 13)
        # z=(0,1/20), f_yyyyyyyyyyyyyyyy=20922789888000 => K_grad_2=16/(20^15)=1/2048000000000000000,
        # K_height=1/(20^16)=1/655360000000000000000
        self.assertEqual(led['hexadecic_rows']['K_grad_next_1'], 0)
        self.assertEqual(led['hexadecic_rows']['K_grad_next_2'], Q(1, 2048000000000000000))
        self.assertEqual(led['hexadecic_rows']['K_height_next'], Q(1, 655360000000000000000))
        self.assertEqual(led['hexadecic_rows']['z_dot_K_grad_next_minus_16_K_height_next'], 0)
        self.assertEqual(led['hexadecic_rows']['unmatched_density_r_power'], 14)
        self.assertFalse(led['hexadecic_rows']['seventeenth_and_higher_jets_enumerated'])
        # z=(0,1/20), f_yyyyyyyyyyyyyyyyy=17! => L_grad_2=17/20^16, L_height=1/20^17
        self.assertEqual(led['heptadecic_rows']['L_grad_next_1'], 0)
        self.assertEqual(led['heptadecic_rows']['L_grad_next_2'], Q(17, 655360000000000000000))
        self.assertEqual(led['heptadecic_rows']['L_height_next'], Q(1, 13107200000000000000000))
        self.assertEqual(led['heptadecic_rows']['z_dot_L_grad_next_minus_17_L_height_next'], 0)
        self.assertEqual(led['heptadecic_rows']['unmatched_density_r_power'], 15)
        self.assertFalse(led['heptadecic_rows']['eighteenth_and_higher_jets_enumerated'])
        # z=(0,1/20), f_yyyyyyyyyyyyyyyyyy=18! => M_grad_2=18/20^17, M_height=1/20^18
        self.assertEqual(led['octadecic_rows']['M_grad_next_1'], 0)
        self.assertEqual(led['octadecic_rows']['M_grad_next_2'], Q(18, 13107200000000000000000))
        self.assertEqual(led['octadecic_rows']['M_height_next'], Q(1, 262144000000000000000000))
        self.assertEqual(led['octadecic_rows']['z_dot_M_grad_next_minus_18_M_height_next'], 0)
        self.assertEqual(led['octadecic_rows']['unmatched_density_r_power'], 16)
        self.assertFalse(led['octadecic_rows']['nineteenth_and_higher_jets_enumerated'])
        # z=(0,1/20), f_yyyyyyyyyyyyyyyyyyy=19! => O_grad_2=19/20^18, O_height=1/20^19
        self.assertEqual(led['nonadecic_rows']['O_grad_next_1'], 0)
        self.assertEqual(led['nonadecic_rows']['O_grad_next_2'], Q(19, 262144000000000000000000))
        self.assertEqual(led['nonadecic_rows']['O_height_next'], Q(1, 5242880000000000000000000))
        self.assertEqual(led['nonadecic_rows']['z_dot_O_grad_next_minus_19_O_height_next'], 0)
        self.assertEqual(led['nonadecic_rows']['unmatched_density_r_power'], 17)
        self.assertFalse(led['nonadecic_rows']['twentieth_and_higher_jets_enumerated'])
        # z=(0,1/20), f_yyyyyyyyyyyyyyyyyyyy=20! => R_grad_2=20/20^19, R_height=1/20^20
        self.assertEqual(led['icosic_rows']['R_grad_next_1'], 0)
        self.assertEqual(led['icosic_rows']['R_grad_next_2'], Q(1, 262144000000000000000000))
        self.assertEqual(led['icosic_rows']['R_height_next'], Q(1, 104857600000000000000000000))
        self.assertEqual(led['icosic_rows']['z_dot_R_grad_next_minus_20_R_height_next'], 0)
        self.assertEqual(led['icosic_rows']['unmatched_density_r_power'], 18)
        self.assertFalse(led['icosic_rows']['twenty_first_and_higher_jets_enumerated'])
        # z=(0,1/20), f_yyyyyyyyyyyyyyyyyyyyy=21! => V_grad_2=21/20^20, V_height=1/20^21
        self.assertEqual(led['henicosic_rows']['V_grad_next_1'], 0)
        self.assertEqual(led['henicosic_rows']['V_grad_next_2'], Q(21, 104857600000000000000000000))
        self.assertEqual(led['henicosic_rows']['V_height_next'], Q(1, 2097152000000000000000000000))
        self.assertEqual(led['henicosic_rows']['z_dot_V_grad_next_minus_21_V_height_next'], 0)
        self.assertEqual(led['henicosic_rows']['unmatched_density_r_power'], 19)
        self.assertFalse(led['henicosic_rows']['twenty_second_and_higher_jets_enumerated'])
        # z=(0,1/20), f_yyyyyyyyyyyyyyyyyyyyyy=22! => W_grad_2=22/20^21, W_height=1/20^22
        self.assertEqual(led['docosic_rows']['W_grad_next_1'], 0)
        self.assertEqual(led['docosic_rows']['W_grad_next_2'], Q(11, 1048576000000000000000000000))
        self.assertEqual(led['docosic_rows']['W_height_next'], Q(1, 41943040000000000000000000000))
        self.assertEqual(led['docosic_rows']['z_dot_W_grad_next_minus_22_W_height_next'], 0)
        self.assertEqual(led['docosic_rows']['unmatched_density_r_power'], 20)
        self.assertFalse(led['docosic_rows']['twenty_third_and_higher_jets_enumerated'])
        # z=(0,1/20), f_yyyyyyyyyyyyyyyyyyyyyyy=23! => X_grad_2=23/20^22, X_height=1/20^23
        self.assertEqual(led['tricosic_rows']['X_grad_next_1'], 0)
        self.assertEqual(led['tricosic_rows']['X_grad_next_2'], Q(23, 41943040000000000000000000000))
        self.assertEqual(led['tricosic_rows']['X_height_next'], Q(1, 838860800000000000000000000000))
        self.assertEqual(led['tricosic_rows']['z_dot_X_grad_next_minus_23_X_height_next'], 0)
        self.assertEqual(led['tricosic_rows']['unmatched_density_r_power'], 21)
        self.assertFalse(led['tricosic_rows']['twenty_fourth_and_higher_jets_enumerated'])
        # z=(0,1/20), f_yyyy...yyyy=24! => Y_grad_2=24/20^23, Y_height=1/20^24
        self.assertEqual(led['tetracosic_rows']['Y_grad_next_1'], 0)
        self.assertEqual(led['tetracosic_rows']['Y_grad_next_2'], Q(3, 104857600000000000000000000000))
        self.assertEqual(led['tetracosic_rows']['Y_height_next'], Q(1, 16777216000000000000000000000000))
        self.assertEqual(led['tetracosic_rows']['z_dot_Y_grad_next_minus_24_Y_height_next'], 0)
        self.assertEqual(led['tetracosic_rows']['unmatched_density_r_power'], 22)
        self.assertFalse(led['tetracosic_rows']['twenty_fifth_and_higher_jets_enumerated'])
        self.assertEqual(led['pentacosic_rows']['Z_grad_next_1'], 0)
        self.assertEqual(led['pentacosic_rows']['Z_grad_next_2'], Q(1, 671088640000000000000000000000))
        self.assertEqual(led['pentacosic_rows']['Z_height_next'], Q(1, 335544320000000000000000000000000))
        self.assertEqual(led['pentacosic_rows']['z_dot_Z_grad_next_minus_25_Z_height_next'], 0)
        self.assertEqual(led['pentacosic_rows']['unmatched_density_r_power'], 23)
        self.assertFalse(led['pentacosic_rows']['twenty_sixth_and_higher_jets_enumerated'])
        # z=(0,1/20), f_yyyy...yyyy=26! => A_grad_2=26/20^25, A_height=1/20^26
        self.assertEqual(led['hexacosic_rows']['A_grad_next_1'], 0)
        self.assertEqual(led['hexacosic_rows']['A_grad_next_2'], Q(13, 167772160000000000000000000000000))
        self.assertEqual(led['hexacosic_rows']['A_height_next'], Q(1, 6710886400000000000000000000000000))
        self.assertEqual(led['hexacosic_rows']['z_dot_A_grad_next_minus_26_A_height_next'], 0)
        self.assertEqual(led['hexacosic_rows']['unmatched_density_r_power'], 24)
        self.assertFalse(led['hexacosic_rows']['twenty_seventh_and_higher_jets_enumerated'])
        # z=(0,1/20), f_yyyy...=27! => B_grad_2=27/20^26, B_height=1/20^27
        self.assertEqual(led['heptacosic_rows']['B_grad_next_1'], 0)
        self.assertEqual(led['heptacosic_rows']['B_grad_next_2'], Q(27, 6710886400000000000000000000000000))
        self.assertEqual(led['heptacosic_rows']['B_height_next'], Q(1, 134217728000000000000000000000000000))
        self.assertEqual(led['heptacosic_rows']['z_dot_B_grad_next_minus_27_B_height_next'], 0)
        self.assertEqual(led['heptacosic_rows']['unmatched_density_r_power'], 25)
        self.assertFalse(led['heptacosic_rows']['twenty_eighth_and_higher_jets_enumerated'])
        # z=(0,1/20), f=28! => C_grad_2=28/20^27, C_height=1/20^28
        self.assertEqual(led['octacosic_rows']['C_grad_next_1'], 0)
        self.assertEqual(led['octacosic_rows']['C_grad_next_2'], Q(7, 33554432000000000000000000000000000))
        self.assertEqual(led['octacosic_rows']['C_height_next'], Q(1, 2684354560000000000000000000000000000))
        self.assertEqual(led['octacosic_rows']['z_dot_C_grad_next_minus_28_C_height_next'], 0)
        self.assertEqual(led['octacosic_rows']['unmatched_density_r_power'], 26)
        self.assertFalse(led['octacosic_rows']['twenty_ninth_and_higher_jets_enumerated'])
        # z=(0,1/20), f=29! => AA_grad_2=29/20^28, AA_height=1/20^29
        self.assertEqual(led['nonacosic_rows']['AA_grad_next_1'], 0)
        self.assertEqual(led['nonacosic_rows']['AA_grad_next_2'], Q(29, 2684354560000000000000000000000000000))
        self.assertEqual(led['nonacosic_rows']['AA_height_next'], Q(1, 53687091200000000000000000000000000000))
        self.assertEqual(led['nonacosic_rows']['z_dot_AA_grad_next_minus_29_AA_height_next'], 0)
        self.assertEqual(led['nonacosic_rows']['unmatched_density_r_power'], 27)
        self.assertFalse(led['nonacosic_rows']['thirtieth_and_higher_jets_enumerated'])
        # z=(0,1/20), f=30! => AB_grad_2=30/20^29, AB_height=1/20^30
        self.assertEqual(led['triacontic_rows']['AB_grad_next_1'], 0)
        self.assertEqual(led['triacontic_rows']['AB_grad_next_2'], Q(3, 5368709120000000000000000000000000000))
        self.assertEqual(led['triacontic_rows']['AB_height_next'], Q(1, 1073741824000000000000000000000000000000))
        self.assertEqual(led['triacontic_rows']['z_dot_AB_grad_next_minus_30_AB_height_next'], 0)
        self.assertEqual(led['triacontic_rows']['unmatched_density_r_power'], 28)
        self.assertFalse(led['triacontic_rows']['thirty_first_and_higher_jets_enumerated'])
        # z=(0,1/20), f=31! => AC_grad_2=31/20^30, AC_height=1/20^31
        self.assertEqual(led['hentriacontic_rows']['AC_grad_next_1'], 0)
        self.assertEqual(led['hentriacontic_rows']['AC_grad_next_2'], Q(31, 1073741824000000000000000000000000000000))
        self.assertEqual(led['hentriacontic_rows']['AC_height_next'], Q(1, 21474836480000000000000000000000000000000))
        self.assertEqual(led['hentriacontic_rows']['z_dot_AC_grad_next_minus_31_AC_height_next'], 0)
        self.assertEqual(led['hentriacontic_rows']['unmatched_density_r_power'], 29)
        self.assertFalse(led['hentriacontic_rows']['thirty_second_and_higher_jets_enumerated'])
        # z=(0,1/20), f=32! => AD_grad_2=32/20^31, AD_height=1/20^32
        self.assertEqual(led['dotriacontic_rows']['AD_grad_next_1'], 0)
        self.assertEqual(led['dotriacontic_rows']['AD_grad_next_2'], Q(32, 21474836480000000000000000000000000000000))
        self.assertEqual(led['dotriacontic_rows']['AD_height_next'], Q(1, 429496729600000000000000000000000000000000))
        self.assertEqual(led['dotriacontic_rows']['z_dot_AD_grad_next_minus_32_AD_height_next'], 0)
        self.assertEqual(led['dotriacontic_rows']['unmatched_density_r_power'], 30)
        self.assertFalse(led['dotriacontic_rows']['thirty_third_and_higher_jets_enumerated'])
        # z=(0,1/20), f=33! => AE_grad_2=33/20^32, AE_height=1/20^33
        self.assertEqual(led['tritriacontic_rows']['AE_grad_next_1'], 0)
        self.assertEqual(led['tritriacontic_rows']['AE_grad_next_2'], Q(33, 429496729600000000000000000000000000000000))
        self.assertEqual(led['tritriacontic_rows']['AE_height_next'], Q(1, 8589934592000000000000000000000000000000000))
        self.assertEqual(led['tritriacontic_rows']['z_dot_AE_grad_next_minus_33_AE_height_next'], 0)
        self.assertEqual(led['tritriacontic_rows']['unmatched_density_r_power'], 31)
        self.assertFalse(led['tritriacontic_rows']['thirty_fourth_and_higher_jets_enumerated'])
        # z=(0,1/20), f=34! => AF_grad_2=34/20^33, AF_height=1/20^34
        self.assertEqual(led['tetratriacontic_rows']['AF_grad_next_1'], 0)
        self.assertEqual(led['tetratriacontic_rows']['AF_grad_next_2'], Q(34, 8589934592000000000000000000000000000000000))
        self.assertEqual(led['tetratriacontic_rows']['AF_height_next'], Q(1, 171798691840000000000000000000000000000000000))
        self.assertEqual(led['tetratriacontic_rows']['z_dot_AF_grad_next_minus_34_AF_height_next'], 0)
        self.assertEqual(led['tetratriacontic_rows']['unmatched_density_r_power'], 32)
        self.assertFalse(led['tetratriacontic_rows']['thirty_fifth_and_higher_jets_enumerated'])
        self.assertEqual(led['scaling']['gradient_jacobian_r_power'], 2)
        self.assertEqual(led['status'], 'OPEN_HIGHER_JETS_AND_DENSITY')
        self.assertEqual(led['hessian_signature']['signature_kind'], 'INDEFINITE_SADDLE')
        self.assertTrue(led['hessian_signature']['signature_matches_pin_role'])
        with self.assertRaises(ValueError):
            m.pin_centered_frame(m.point(0, 2), inner=Q(2, 5), outer=1)

    def test_pin_site_morse_quartic_rows(self):
        rows = m.pin_site_morse_quartic_rows(
            1, 2, f_xxxx=0, f_xxxy=0, f_xxyy=0, f_xyyy=0, f_yyyy=24)
        self.assertEqual(rows['Q_grad_next_1'], 0)
        self.assertEqual(rows['Q_grad_next_2'], 32)  # (1/6)*24*8
        self.assertEqual(rows['Q_height_next'], 16)  # (1/24)*24*16
        self.assertEqual(rows['z_dot_Q_grad_next_minus_4_Q_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 2)
        self.assertTrue(rows['explicit_r_factor_still_required'])
        mixed = m.pin_site_morse_quartic_rows(
            1, 1, f_xxxx=24, f_xxxy=0, f_xxyy=0, f_xyyy=0, f_yyyy=0)
        self.assertEqual(mixed['Q_grad_next_1'], 4)  # (1/6)*24
        self.assertEqual(mixed['Q_grad_next_2'], 0)
        self.assertEqual(mixed['Q_height_next'], 1)  # (1/24)*24
        self.assertEqual(mixed['z_dot_Q_grad_next_minus_4_Q_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_quartic_rows(
                0, 0, f_xxxx=1, f_xxxy=0, f_xxyy=0, f_xyyy=0, f_yyyy=0)

    def test_pin_site_morse_quintic_rows(self):
        rows = m.pin_site_morse_quintic_rows(
            1, 2, f_xxxxx=0, f_xxxxy=0, f_xxxyy=0, f_xxyyy=0, f_xyyyy=0, f_yyyyy=120)
        self.assertEqual(rows['P_grad_next_1'], 0)
        self.assertEqual(rows['P_grad_next_2'], 80)  # (1/24)*120*16
        self.assertEqual(rows['P_height_next'], 32)  # (1/120)*120*32
        self.assertEqual(rows['z_dot_P_grad_next_minus_5_P_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 3)
        with self.assertRaises(ValueError):
            m.pin_site_morse_quintic_rows(
                0, 0, f_xxxxx=1, f_xxxxy=0, f_xxxyy=0, f_xxyyy=0, f_xyyyy=0, f_yyyyy=0)

    def test_pin_site_morse_sextic_rows(self):
        rows = m.pin_site_morse_sextic_rows(
            1, 2,
            f_xxxxxx=0, f_xxxxxy=0, f_xxxxyy=0, f_xxxyyy=0,
            f_xxyyyy=0, f_xyyyyy=0, f_yyyyyy=720)
        self.assertEqual(rows['S_grad_next_1'], 0)
        self.assertEqual(rows['S_grad_next_2'], 192)  # (1/120)*720*32
        self.assertEqual(rows['S_height_next'], 64)  # (1/720)*720*64
        self.assertEqual(rows['z_dot_S_grad_next_minus_6_S_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 4)
        mixed = m.pin_site_morse_sextic_rows(
            1, 1,
            f_xxxxxx=720, f_xxxxxy=0, f_xxxxyy=0, f_xxxyyy=0,
            f_xxyyyy=0, f_xyyyyy=0, f_yyyyyy=0)
        self.assertEqual(mixed['S_grad_next_1'], 6)  # (1/120)*720
        self.assertEqual(mixed['S_grad_next_2'], 0)
        self.assertEqual(mixed['S_height_next'], 1)  # (1/720)*720
        self.assertEqual(mixed['z_dot_S_grad_next_minus_6_S_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_sextic_rows(
                0, 0,
                f_xxxxxx=1, f_xxxxxy=0, f_xxxxyy=0, f_xxxyyy=0,
                f_xxyyyy=0, f_xyyyyy=0, f_yyyyyy=0)

    def test_pin_site_morse_septic_rows(self):
        rows = m.pin_site_morse_septic_rows(
            1, 2,
            f_xxxxxxx=0, f_xxxxxxy=0, f_xxxxxyy=0, f_xxxxyyy=0,
            f_xxxyyyy=0, f_xxyyyyy=0, f_xyyyyyy=0, f_yyyyyyy=5040)
        self.assertEqual(rows['T_grad_next_1'], 0)
        self.assertEqual(rows['T_grad_next_2'], 448)  # (1/720)*5040*64
        self.assertEqual(rows['T_height_next'], 128)  # (1/5040)*5040*128
        self.assertEqual(rows['z_dot_T_grad_next_minus_7_T_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 5)
        mixed = m.pin_site_morse_septic_rows(
            1, 1,
            f_xxxxxxx=5040, f_xxxxxxy=0, f_xxxxxyy=0, f_xxxxyyy=0,
            f_xxxyyyy=0, f_xxyyyyy=0, f_xyyyyyy=0, f_yyyyyyy=0)
        self.assertEqual(mixed['T_grad_next_1'], 7)  # (1/720)*5040
        self.assertEqual(mixed['T_grad_next_2'], 0)
        self.assertEqual(mixed['T_height_next'], 1)  # (1/5040)*5040
        self.assertEqual(mixed['z_dot_T_grad_next_minus_7_T_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_septic_rows(
                0, 0,
                f_xxxxxxx=1, f_xxxxxxy=0, f_xxxxxyy=0, f_xxxxyyy=0,
                f_xxxyyyy=0, f_xxyyyyy=0, f_xyyyyyy=0, f_yyyyyyy=0)

    def test_pin_site_morse_octic_rows(self):
        rows = m.pin_site_morse_octic_rows(
            1, 2,
            f_xxxxxxxx=0, f_xxxxxxxy=0, f_xxxxxxyy=0, f_xxxxxyyy=0,
            f_xxxxyyyy=0, f_xxxyyyyy=0, f_xxyyyyyy=0, f_xyyyyyyy=0, f_yyyyyyyy=40320)
        self.assertEqual(rows['U_grad_next_1'], 0)
        self.assertEqual(rows['U_grad_next_2'], 1024)  # (1/5040)*40320*128
        self.assertEqual(rows['U_height_next'], 256)  # (1/40320)*40320*256
        self.assertEqual(rows['z_dot_U_grad_next_minus_8_U_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 6)
        mixed = m.pin_site_morse_octic_rows(
            1, 1,
            f_xxxxxxxx=40320, f_xxxxxxxy=0, f_xxxxxxyy=0, f_xxxxxyyy=0,
            f_xxxxyyyy=0, f_xxxyyyyy=0, f_xxyyyyyy=0, f_xyyyyyyy=0, f_yyyyyyyy=0)
        self.assertEqual(mixed['U_grad_next_1'], 8)  # (1/5040)*40320
        self.assertEqual(mixed['U_grad_next_2'], 0)
        self.assertEqual(mixed['U_height_next'], 1)  # (1/40320)*40320
        self.assertEqual(mixed['z_dot_U_grad_next_minus_8_U_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_octic_rows(
                0, 0,
                f_xxxxxxxx=1, f_xxxxxxxy=0, f_xxxxxxyy=0, f_xxxxxyyy=0,
                f_xxxxyyyy=0, f_xxxyyyyy=0, f_xxyyyyyy=0, f_xyyyyyyy=0, f_yyyyyyyy=0)

    def test_pin_site_morse_nonic_rows(self):
        rows = m.pin_site_morse_nonic_rows(
            1, 2,
            f_xxxxxxxxx=0, f_xxxxxxxxy=0, f_xxxxxxxyy=0, f_xxxxxxyyy=0,
            f_xxxxxyyyy=0, f_xxxxyyyyy=0, f_xxxyyyyyy=0, f_xxyyyyyyy=0,
            f_xyyyyyyyy=0, f_yyyyyyyyy=362880)
        self.assertEqual(rows['N_grad_next_1'], 0)
        self.assertEqual(rows['N_grad_next_2'], 2304)  # (1/40320)*362880*256
        self.assertEqual(rows['N_height_next'], 512)  # (1/362880)*362880*512
        self.assertEqual(rows['z_dot_N_grad_next_minus_9_N_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 7)
        mixed = m.pin_site_morse_nonic_rows(
            1, 1,
            f_xxxxxxxxx=362880, f_xxxxxxxxy=0, f_xxxxxxxyy=0, f_xxxxxxyyy=0,
            f_xxxxxyyyy=0, f_xxxxyyyyy=0, f_xxxyyyyyy=0, f_xxyyyyyyy=0,
            f_xyyyyyyyy=0, f_yyyyyyyyy=0)
        self.assertEqual(mixed['N_grad_next_1'], 9)  # (1/40320)*362880
        self.assertEqual(mixed['N_grad_next_2'], 0)
        self.assertEqual(mixed['N_height_next'], 1)  # (1/362880)*362880
        self.assertEqual(mixed['z_dot_N_grad_next_minus_9_N_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_nonic_rows(
                0, 0,
                f_xxxxxxxxx=1, f_xxxxxxxxy=0, f_xxxxxxxyy=0, f_xxxxxxyyy=0,
                f_xxxxxyyyy=0, f_xxxxyyyyy=0, f_xxxyyyyyy=0, f_xxyyyyyyy=0,
                f_xyyyyyyyy=0, f_yyyyyyyyy=0)

    def test_pin_site_morse_decic_rows(self):
        rows = m.pin_site_morse_decic_rows(
            1, 2,
            f_xxxxxxxxxx=0, f_xxxxxxxxxy=0, f_xxxxxxxxyy=0, f_xxxxxxxyyy=0,
            f_xxxxxxyyyy=0, f_xxxxxyyyyy=0, f_xxxxyyyyyy=0, f_xxxyyyyyyy=0,
            f_xxyyyyyyyy=0, f_xyyyyyyyyy=0, f_yyyyyyyyyy=3628800)
        self.assertEqual(rows['D_grad_next_1'], 0)
        self.assertEqual(rows['D_grad_next_2'], 5120)  # (1/362880)*3628800*512
        self.assertEqual(rows['D_height_next'], 1024)  # (1/3628800)*3628800*1024
        self.assertEqual(rows['z_dot_D_grad_next_minus_10_D_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 8)
        mixed = m.pin_site_morse_decic_rows(
            1, 1,
            f_xxxxxxxxxx=3628800, f_xxxxxxxxxy=0, f_xxxxxxxxyy=0, f_xxxxxxxyyy=0,
            f_xxxxxxyyyy=0, f_xxxxxyyyyy=0, f_xxxxyyyyyy=0, f_xxxyyyyyyy=0,
            f_xxyyyyyyyy=0, f_xyyyyyyyyy=0, f_yyyyyyyyyy=0)
        self.assertEqual(mixed['D_grad_next_1'], 10)  # (1/362880)*3628800
        self.assertEqual(mixed['D_grad_next_2'], 0)
        self.assertEqual(mixed['D_height_next'], 1)  # (1/3628800)*3628800
        self.assertEqual(mixed['z_dot_D_grad_next_minus_10_D_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_decic_rows(
                0, 0,
                f_xxxxxxxxxx=1, f_xxxxxxxxxy=0, f_xxxxxxxxyy=0, f_xxxxxxxyyy=0,
                f_xxxxxxyyyy=0, f_xxxxxyyyyy=0, f_xxxxyyyyyy=0, f_xxxyyyyyyy=0,
                f_xxyyyyyyyy=0, f_xyyyyyyyyy=0, f_yyyyyyyyyy=0)

    def test_pin_site_morse_undecic_rows(self):
        rows = m.pin_site_morse_undecic_rows(
            1, 2,
            f_xxxxxxxxxxx=0, f_xxxxxxxxxxy=0, f_xxxxxxxxxyy=0, f_xxxxxxxxyyy=0,
            f_xxxxxxxyyyy=0, f_xxxxxxyyyyy=0, f_xxxxxyyyyyy=0, f_xxxxyyyyyyy=0,
            f_xxxyyyyyyyy=0, f_xxyyyyyyyyy=0, f_xyyyyyyyyyy=0, f_yyyyyyyyyyy=39916800)
        self.assertEqual(rows['E_grad_next_1'], 0)
        self.assertEqual(rows['E_grad_next_2'], 11264)  # (1/3628800)*39916800*1024
        self.assertEqual(rows['E_height_next'], 2048)  # (1/39916800)*39916800*2048
        self.assertEqual(rows['z_dot_E_grad_next_minus_11_E_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 9)
        mixed = m.pin_site_morse_undecic_rows(
            1, 1,
            f_xxxxxxxxxxx=39916800, f_xxxxxxxxxxy=0, f_xxxxxxxxxyy=0, f_xxxxxxxxyyy=0,
            f_xxxxxxxyyyy=0, f_xxxxxxyyyyy=0, f_xxxxxyyyyyy=0, f_xxxxyyyyyyy=0,
            f_xxxyyyyyyyy=0, f_xxyyyyyyyyy=0, f_xyyyyyyyyyy=0, f_yyyyyyyyyyy=0)
        self.assertEqual(mixed['E_grad_next_1'], 11)  # (1/3628800)*39916800
        self.assertEqual(mixed['E_grad_next_2'], 0)
        self.assertEqual(mixed['E_height_next'], 1)  # (1/39916800)*39916800
        self.assertEqual(mixed['z_dot_E_grad_next_minus_11_E_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_undecic_rows(
                0, 0,
                f_xxxxxxxxxxx=1, f_xxxxxxxxxxy=0, f_xxxxxxxxxyy=0, f_xxxxxxxxyyy=0,
                f_xxxxxxxyyyy=0, f_xxxxxxyyyyy=0, f_xxxxxyyyyyy=0, f_xxxxyyyyyyy=0,
                f_xxxyyyyyyyy=0, f_xxyyyyyyyyy=0, f_xyyyyyyyyyy=0, f_yyyyyyyyyyy=0)

    def test_pin_site_morse_dodecic_rows(self):
        rows = m.pin_site_morse_dodecic_rows(
            1, 2,
            f_xxxxxxxxxxxx=0, f_xxxxxxxxxxxy=0, f_xxxxxxxxxxyy=0, f_xxxxxxxxxyyy=0,
            f_xxxxxxxxyyyy=0, f_xxxxxxxyyyyy=0, f_xxxxxxyyyyyy=0, f_xxxxxyyyyyyy=0,
            f_xxxxyyyyyyyy=0, f_xxxyyyyyyyyy=0, f_xxyyyyyyyyyy=0, f_xyyyyyyyyyyy=0,
            f_yyyyyyyyyyyy=479001600)
        self.assertEqual(rows['F_grad_next_1'], 0)
        self.assertEqual(rows['F_grad_next_2'], 24576)  # (1/39916800)*479001600*2048
        self.assertEqual(rows['F_height_next'], 4096)  # (1/479001600)*479001600*4096
        self.assertEqual(rows['z_dot_F_grad_next_minus_12_F_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 10)
        mixed = m.pin_site_morse_dodecic_rows(
            1, 1,
            f_xxxxxxxxxxxx=479001600, f_xxxxxxxxxxxy=0, f_xxxxxxxxxxyy=0, f_xxxxxxxxxyyy=0,
            f_xxxxxxxxyyyy=0, f_xxxxxxxyyyyy=0, f_xxxxxxyyyyyy=0, f_xxxxxyyyyyyy=0,
            f_xxxxyyyyyyyy=0, f_xxxyyyyyyyyy=0, f_xxyyyyyyyyyy=0, f_xyyyyyyyyyyy=0,
            f_yyyyyyyyyyyy=0)
        self.assertEqual(mixed['F_grad_next_1'], 12)  # (1/39916800)*479001600
        self.assertEqual(mixed['F_grad_next_2'], 0)
        self.assertEqual(mixed['F_height_next'], 1)
        self.assertEqual(mixed['z_dot_F_grad_next_minus_12_F_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_dodecic_rows(
                0, 0,
                f_xxxxxxxxxxxx=1, f_xxxxxxxxxxxy=0, f_xxxxxxxxxxyy=0, f_xxxxxxxxxyyy=0,
                f_xxxxxxxxyyyy=0, f_xxxxxxxyyyyy=0, f_xxxxxxyyyyyy=0, f_xxxxxyyyyyyy=0,
                f_xxxxyyyyyyyy=0, f_xxxyyyyyyyyy=0, f_xxyyyyyyyyyy=0, f_xyyyyyyyyyyy=0,
                f_yyyyyyyyyyyy=0)

    def test_pin_site_morse_tridecic_rows(self):
        rows = m.pin_site_morse_tridecic_rows(
            1, 2,
            f_xxxxxxxxxxxxx=0, f_xxxxxxxxxxxxy=0, f_xxxxxxxxxxxyy=0, f_xxxxxxxxxxyyy=0,
            f_xxxxxxxxxyyyy=0, f_xxxxxxxxyyyyy=0, f_xxxxxxxyyyyyy=0, f_xxxxxxyyyyyyy=0,
            f_xxxxxyyyyyyyy=0, f_xxxxyyyyyyyyy=0, f_xxxyyyyyyyyyy=0, f_xxyyyyyyyyyyy=0,
            f_xyyyyyyyyyyyy=0, f_yyyyyyyyyyyyy=6227020800)
        self.assertEqual(rows['G_grad_next_1'], 0)
        self.assertEqual(rows['G_grad_next_2'], 53248)  # (1/479001600)*6227020800*4096
        self.assertEqual(rows['G_height_next'], 8192)  # (1/6227020800)*6227020800*8192
        self.assertEqual(rows['z_dot_G_grad_next_minus_13_G_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 11)
        mixed = m.pin_site_morse_tridecic_rows(
            1, 1,
            f_xxxxxxxxxxxxx=6227020800, f_xxxxxxxxxxxxy=0, f_xxxxxxxxxxxyy=0, f_xxxxxxxxxxyyy=0,
            f_xxxxxxxxxyyyy=0, f_xxxxxxxxyyyyy=0, f_xxxxxxxyyyyyy=0, f_xxxxxxyyyyyyy=0,
            f_xxxxxyyyyyyyy=0, f_xxxxyyyyyyyyy=0, f_xxxyyyyyyyyyy=0, f_xxyyyyyyyyyyy=0,
            f_xyyyyyyyyyyyy=0, f_yyyyyyyyyyyyy=0)
        self.assertEqual(mixed['G_grad_next_1'], 13)  # (1/479001600)*6227020800
        self.assertEqual(mixed['G_grad_next_2'], 0)
        self.assertEqual(mixed['G_height_next'], 1)
        self.assertEqual(mixed['z_dot_G_grad_next_minus_13_G_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_tridecic_rows(
                0, 0,
                f_xxxxxxxxxxxxx=1, f_xxxxxxxxxxxxy=0, f_xxxxxxxxxxxyy=0, f_xxxxxxxxxxyyy=0,
                f_xxxxxxxxxyyyy=0, f_xxxxxxxxyyyyy=0, f_xxxxxxxyyyyyy=0, f_xxxxxxyyyyyyy=0,
                f_xxxxxyyyyyyyy=0, f_xxxxyyyyyyyyy=0, f_xxxyyyyyyyyyy=0, f_xxyyyyyyyyyyy=0,
                f_xyyyyyyyyyyyy=0, f_yyyyyyyyyyyyy=0)

    def test_pin_site_morse_tetradecic_rows(self):
        rows = m.pin_site_morse_tetradecic_rows(
            1, 2,
            f_xxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxyy=0, f_xxxxxxxxxxxyyy=0,
            f_xxxxxxxxxxyyyy=0, f_xxxxxxxxxyyyyy=0, f_xxxxxxxxyyyyyy=0, f_xxxxxxxyyyyyyy=0,
            f_xxxxxxyyyyyyyy=0, f_xxxxxyyyyyyyyy=0, f_xxxxyyyyyyyyyy=0, f_xxxyyyyyyyyyyy=0,
            f_xxyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyy=87178291200)
        self.assertEqual(rows['I_grad_next_1'], 0)
        self.assertEqual(rows['I_grad_next_2'], 114688)  # (1/6227020800)*87178291200*8192
        self.assertEqual(rows['I_height_next'], 16384)  # (1/87178291200)*87178291200*16384
        self.assertEqual(rows['z_dot_I_grad_next_minus_14_I_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 12)
        mixed = m.pin_site_morse_tetradecic_rows(
            1, 1,
            f_xxxxxxxxxxxxxx=87178291200, f_xxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxyy=0, f_xxxxxxxxxxxyyy=0,
            f_xxxxxxxxxxyyyy=0, f_xxxxxxxxxyyyyy=0, f_xxxxxxxxyyyyyy=0, f_xxxxxxxyyyyyyy=0,
            f_xxxxxxyyyyyyyy=0, f_xxxxxyyyyyyyyy=0, f_xxxxyyyyyyyyyy=0, f_xxxyyyyyyyyyyy=0,
            f_xxyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['I_grad_next_1'], 14)  # (1/6227020800)*87178291200
        self.assertEqual(mixed['I_grad_next_2'], 0)
        self.assertEqual(mixed['I_height_next'], 1)
        self.assertEqual(mixed['z_dot_I_grad_next_minus_14_I_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_tetradecic_rows(
                0, 0,
                f_xxxxxxxxxxxxxx=1, f_xxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxyy=0, f_xxxxxxxxxxxyyy=0,
                f_xxxxxxxxxxyyyy=0, f_xxxxxxxxxyyyyy=0, f_xxxxxxxxyyyyyy=0, f_xxxxxxxyyyyyyy=0,
                f_xxxxxxyyyyyyyy=0, f_xxxxxyyyyyyyyy=0, f_xxxxyyyyyyyyyy=0, f_xxxyyyyyyyyyyy=0,
                f_xxyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyy=0)

    def test_pin_site_morse_pentadecic_rows(self):
        rows = m.pin_site_morse_pentadecic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxyyy=0,
            f_xxxxxxxxxxxyyyy=0, f_xxxxxxxxxxyyyyy=0, f_xxxxxxxxxyyyyyy=0, f_xxxxxxxxyyyyyyy=0,
            f_xxxxxxxyyyyyyyy=0, f_xxxxxxyyyyyyyyy=0, f_xxxxxyyyyyyyyyy=0, f_xxxxyyyyyyyyyyy=0,
            f_xxxyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyy=1307674368000)
        self.assertEqual(rows['J_grad_next_1'], 0)
        self.assertEqual(rows['J_grad_next_2'], 245760)  # (1/87178291200)*1307674368000*16384
        self.assertEqual(rows['J_height_next'], 32768)  # (1/1307674368000)*1307674368000*32768
        self.assertEqual(rows['z_dot_J_grad_next_minus_15_J_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 13)
        mixed = m.pin_site_morse_pentadecic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxx=1307674368000, f_xxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxyyy=0,
            f_xxxxxxxxxxxyyyy=0, f_xxxxxxxxxxyyyyy=0, f_xxxxxxxxxyyyyyy=0, f_xxxxxxxxyyyyyyy=0,
            f_xxxxxxxyyyyyyyy=0, f_xxxxxxyyyyyyyyy=0, f_xxxxxyyyyyyyyyy=0, f_xxxxyyyyyyyyyyy=0,
            f_xxxyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['J_grad_next_1'], 15)  # (1/87178291200)*1307674368000
        self.assertEqual(mixed['J_grad_next_2'], 0)
        self.assertEqual(mixed['J_height_next'], 1)
        self.assertEqual(mixed['z_dot_J_grad_next_minus_15_J_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_pentadecic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxx=1, f_xxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxyyy=0,
                f_xxxxxxxxxxxyyyy=0, f_xxxxxxxxxxyyyyy=0, f_xxxxxxxxxyyyyyy=0, f_xxxxxxxxyyyyyyy=0,
                f_xxxxxxxyyyyyyyy=0, f_xxxxxxyyyyyyyyy=0, f_xxxxxyyyyyyyyyy=0, f_xxxxyyyyyyyyyyy=0,
                f_xxxyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyy=0)


    def test_pin_site_morse_heptadecic_rows(self):
        rows = m.pin_site_morse_heptadecic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxyyy=0,
            f_xxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxyyyyyyy=0,
            f_xxxxxxxxxyyyyyyyy=0, f_xxxxxxxxyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyy=0,
            f_xxxxxyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyy=0,
            f_xyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyy=355687428096000)
        self.assertEqual(rows['L_grad_next_1'], 0)
        self.assertEqual(rows['L_grad_next_2'], 1114112)  # 17*2^16
        self.assertEqual(rows['L_height_next'], 131072)  # 2^17
        self.assertEqual(rows['z_dot_L_grad_next_minus_17_L_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 15)
        self.assertFalse(rows['eighteenth_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_heptadecic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxx=355687428096000, f_xxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxyyy=0,
            f_xxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxyyyyyyy=0,
            f_xxxxxxxxxyyyyyyyy=0, f_xxxxxxxxyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyy=0,
            f_xxxxxyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyy=0,
            f_xyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['L_grad_next_1'], 17)
        self.assertEqual(mixed['L_grad_next_2'], 0)
        self.assertEqual(mixed['L_height_next'], 1)
        self.assertEqual(mixed['z_dot_L_grad_next_minus_17_L_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_heptadecic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxx=1, f_xxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxyyy=0,
                f_xxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxyyyyyyy=0,
                f_xxxxxxxxxyyyyyyyy=0, f_xxxxxxxxyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyy=0,
                f_xxxxxyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyy=0,
                f_xyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyy=0)

    def test_pin_site_morse_octadecic_rows(self):
        rows = m.pin_site_morse_octadecic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxyyy=0,
            f_xxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxyyyyyyy=0,
            f_xxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyy=0,
            f_xxxxxxyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyy=0,
            f_xxyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyy=6402373705728000)
        self.assertEqual(rows['M_grad_next_1'], 0)
        self.assertEqual(rows['M_grad_next_2'], 2359296)  # 18*2^17
        self.assertEqual(rows['M_height_next'], 262144)  # 2^18
        self.assertEqual(rows['z_dot_M_grad_next_minus_18_M_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 16)
        self.assertFalse(rows['nineteenth_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_octadecic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxx=6402373705728000, f_xxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxyyy=0,
            f_xxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxyyyyyyy=0,
            f_xxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyy=0,
            f_xxxxxxyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyy=0,
            f_xxyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['M_grad_next_1'], 18)
        self.assertEqual(mixed['M_grad_next_2'], 0)
        self.assertEqual(mixed['M_height_next'], 1)
        self.assertEqual(mixed['z_dot_M_grad_next_minus_18_M_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_octadecic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxx=1, f_xxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxyyy=0,
                f_xxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxyyyyyyy=0,
                f_xxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyy=0,
                f_xxxxxxyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyy=0,
                f_xxyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyy=0)

    def test_pin_site_morse_nonadecic_rows(self):
        rows = m.pin_site_morse_nonadecic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxyyy=0,
            f_xxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxyyyyyyy=0,
            f_xxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyy=0,
            f_xxxxxxxyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyy=0,
            f_xxxyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyy=121645100408832000)
        self.assertEqual(rows['O_grad_next_1'], 0)
        self.assertEqual(rows['O_grad_next_2'], 4980736)  # 19*2^18
        self.assertEqual(rows['O_height_next'], 524288)  # 2^19
        self.assertEqual(rows['z_dot_O_grad_next_minus_19_O_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 17)
        self.assertFalse(rows['twentieth_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_nonadecic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxx=121645100408832000, f_xxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxyyy=0,
            f_xxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxyyyyyyy=0,
            f_xxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyy=0,
            f_xxxxxxxyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyy=0,
            f_xxxyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['O_grad_next_1'], 19)
        self.assertEqual(mixed['O_grad_next_2'], 0)
        self.assertEqual(mixed['O_height_next'], 1)
        self.assertEqual(mixed['z_dot_O_grad_next_minus_19_O_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_nonadecic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxx=1, f_xxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxyyy=0,
                f_xxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxyyyyyyy=0,
                f_xxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyy=0,
                f_xxxxxxxyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyy=0,
                f_xxxyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyy=0)


    def test_pin_site_morse_icosic_rows(self):
        rows = m.pin_site_morse_icosic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyy=2432902008176640000)
        self.assertEqual(rows['R_grad_next_1'], 0)
        self.assertEqual(rows['R_grad_next_2'], 10485760)  # 20*2^19
        self.assertEqual(rows['R_height_next'], 1048576)  # 2^20
        self.assertEqual(rows['z_dot_R_grad_next_minus_20_R_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 18)
        self.assertFalse(rows['twenty_first_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_icosic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxx=2432902008176640000, f_xxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['R_grad_next_1'], 20)
        self.assertEqual(mixed['R_grad_next_2'], 0)
        self.assertEqual(mixed['R_height_next'], 1)
        self.assertEqual(mixed['z_dot_R_grad_next_minus_20_R_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_icosic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyy=1)

    def test_pin_site_morse_henicosic_rows(self):
        rows = m.pin_site_morse_henicosic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyy=51090942171709440000)
        self.assertEqual(rows['V_grad_next_1'], 0)
        self.assertEqual(rows['V_grad_next_2'], 22020096)  # 21*2^20
        self.assertEqual(rows['V_height_next'], 2097152)  # 2^21
        self.assertEqual(rows['z_dot_V_grad_next_minus_21_V_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 19)
        self.assertFalse(rows['twenty_second_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_henicosic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxxx=51090942171709440000, f_xxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['V_grad_next_1'], 21)
        self.assertEqual(mixed['V_grad_next_2'], 0)
        self.assertEqual(mixed['V_height_next'], 1)
        self.assertEqual(mixed['z_dot_V_grad_next_minus_21_V_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_henicosic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyy=1)


    def test_pin_site_morse_docosic_rows(self):
        rows = m.pin_site_morse_docosic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyy=1124000727777607680000)
        self.assertEqual(rows['W_grad_next_1'], 0)
        self.assertEqual(rows['W_grad_next_2'], 46137344)  # 22*2^21
        self.assertEqual(rows['W_height_next'], 4194304)  # 2^22
        self.assertEqual(rows['z_dot_W_grad_next_minus_22_W_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 20)
        self.assertFalse(rows['twenty_third_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_docosic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxxxx=1124000727777607680000, f_xxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['W_grad_next_1'], 22)
        self.assertEqual(mixed['W_grad_next_2'], 0)
        self.assertEqual(mixed['W_height_next'], 1)
        self.assertEqual(mixed['z_dot_W_grad_next_minus_22_W_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_docosic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyy=1)


    def test_pin_site_morse_tricosic_rows(self):
        rows = m.pin_site_morse_tricosic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyy=25852016738884976640000)
        self.assertEqual(rows['X_grad_next_1'], 0)
        self.assertEqual(rows['X_grad_next_2'], 96468992)  # 23*2^22
        self.assertEqual(rows['X_height_next'], 8388608)  # 2^23
        self.assertEqual(rows['z_dot_X_grad_next_minus_23_X_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 21)
        self.assertFalse(rows['twenty_fourth_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_tricosic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxxxxx=25852016738884976640000, f_xxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['X_grad_next_1'], 23)
        self.assertEqual(mixed['X_grad_next_2'], 0)
        self.assertEqual(mixed['X_height_next'], 1)
        self.assertEqual(mixed['z_dot_X_grad_next_minus_23_X_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_tricosic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyy=1)


    def test_pin_site_morse_tetracosic_rows(self):
        rows = m.pin_site_morse_tetracosic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyy=620448401733239439360000)
        self.assertEqual(rows['Y_grad_next_1'], 0)
        self.assertEqual(rows['Y_grad_next_2'], 201326592)  # 24*2^23
        self.assertEqual(rows['Y_height_next'], 16777216)  # 2^24
        self.assertEqual(rows['z_dot_Y_grad_next_minus_24_Y_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 22)
        self.assertFalse(rows['twenty_fifth_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_tetracosic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxxxxxx=620448401733239439360000, f_xxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['Y_grad_next_1'], 24)
        self.assertEqual(mixed['Y_grad_next_2'], 0)
        self.assertEqual(mixed['Y_height_next'], 1)
        self.assertEqual(mixed['z_dot_Y_grad_next_minus_24_Y_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_tetracosic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyy=1)


    def test_pin_site_morse_pentacosic_rows(self):
        rows = m.pin_site_morse_pentacosic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyy=15511210043330985984000000)
        self.assertEqual(rows['Z_grad_next_1'], 0)
        self.assertEqual(rows['Z_grad_next_2'], 419430400)  # 25*2^24
        self.assertEqual(rows['Z_height_next'], 33554432)  # 2^25
        self.assertEqual(rows['z_dot_Z_grad_next_minus_25_Z_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 23)
        self.assertFalse(rows['twenty_sixth_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_pentacosic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxxxxxxx=15511210043330985984000000, f_xxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['Z_grad_next_1'], 25)
        self.assertEqual(mixed['Z_grad_next_2'], 0)
        self.assertEqual(mixed['Z_height_next'], 1)
        self.assertEqual(mixed['z_dot_Z_grad_next_minus_25_Z_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_pentacosic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyy=1)

    def test_pin_site_morse_hexacosic_rows(self):
        rows = m.pin_site_morse_hexacosic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyy=403291461126605635584000000)
        self.assertEqual(rows['A_grad_next_1'], 0)
        self.assertEqual(rows['A_grad_next_2'], 872415232)  # 26*2^25
        self.assertEqual(rows['A_height_next'], 67108864)  # 2^26
        self.assertEqual(rows['z_dot_A_grad_next_minus_26_A_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 24)
        self.assertFalse(rows['twenty_seventh_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_hexacosic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxx=403291461126605635584000000, f_xxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['A_grad_next_1'], 26)
        self.assertEqual(mixed['A_grad_next_2'], 0)
        self.assertEqual(mixed['A_height_next'], 1)
        self.assertEqual(mixed['z_dot_A_grad_next_minus_26_A_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_hexacosic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyy=1)


    def test_pin_site_morse_heptacosic_rows(self):
        rows = m.pin_site_morse_heptacosic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyy=10888869450418352160768000000)
        self.assertEqual(rows['B_grad_next_1'], 0)
        self.assertEqual(rows['B_grad_next_2'], 1811939328)  # 27*2^26
        self.assertEqual(rows['B_height_next'], 134217728)  # 2^27
        self.assertEqual(rows['z_dot_B_grad_next_minus_27_B_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 25)
        self.assertFalse(rows['twenty_eighth_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_heptacosic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxx=10888869450418352160768000000, f_xxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['B_grad_next_1'], 27)
        self.assertEqual(mixed['B_grad_next_2'], 0)
        self.assertEqual(mixed['B_height_next'], 1)
        self.assertEqual(mixed['z_dot_B_grad_next_minus_27_B_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_heptacosic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyy=1)


    def test_pin_site_morse_octacosic_rows(self):
        rows = m.pin_site_morse_octacosic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyy=304888344611713860501504000000)
        self.assertEqual(rows['C_grad_next_1'], 0)
        self.assertEqual(rows['C_grad_next_2'], 3758096384)  # 28*2^27
        self.assertEqual(rows['C_height_next'], 268435456)  # 2^28
        self.assertEqual(rows['z_dot_C_grad_next_minus_28_C_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 26)
        self.assertFalse(rows['twenty_ninth_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_octacosic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxxx=304888344611713860501504000000, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['C_grad_next_1'], 28)
        self.assertEqual(mixed['C_grad_next_2'], 0)
        self.assertEqual(mixed['C_height_next'], 1)
        self.assertEqual(mixed['z_dot_C_grad_next_minus_28_C_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_octacosic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyy=1)


    def test_pin_site_morse_nonacosic_rows(self):
        rows = m.pin_site_morse_nonacosic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyy=8841761993739701954543616000000)
        self.assertEqual(rows['AA_grad_next_1'], 0)
        self.assertEqual(rows['AA_grad_next_2'], 7784628224)  # 29*2^28
        self.assertEqual(rows['AA_height_next'], 536870912)  # 2^29
        self.assertEqual(rows['z_dot_AA_grad_next_minus_29_AA_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 27)
        self.assertFalse(rows['thirtieth_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_nonacosic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx=8841761993739701954543616000000, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['AA_grad_next_1'], 29)
        self.assertEqual(mixed['AA_grad_next_2'], 0)
        self.assertEqual(mixed['AA_height_next'], 1)
        self.assertEqual(mixed['z_dot_AA_grad_next_minus_29_AA_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_nonacosic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyy=1)


    def test_pin_site_morse_triacontic_rows(self):
        rows = m.pin_site_morse_triacontic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=265252859812191058636308480000000)
        self.assertEqual(rows['AB_grad_next_1'], 0)
        self.assertEqual(rows['AB_grad_next_2'], 16106127360)  # 30*2^29
        self.assertEqual(rows['AB_height_next'], 1073741824)  # 2^30
        self.assertEqual(rows['z_dot_AB_grad_next_minus_30_AB_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 28)
        self.assertFalse(rows['thirty_first_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_triacontic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=265252859812191058636308480000000, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['AB_grad_next_1'], 30)
        self.assertEqual(mixed['AB_grad_next_2'], 0)
        self.assertEqual(mixed['AB_height_next'], 1)
        self.assertEqual(mixed['z_dot_AB_grad_next_minus_30_AB_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_triacontic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=1)


    def test_pin_site_morse_hentriacontic_rows(self):
        rows = m.pin_site_morse_hentriacontic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=8222838654177922817725562880000000)
        self.assertEqual(rows['AC_grad_next_1'], 0)
        self.assertEqual(rows['AC_grad_next_2'], 33285996544)  # 31*2^30
        self.assertEqual(rows['AC_height_next'], 2147483648)  # 2^31
        self.assertEqual(rows['z_dot_AC_grad_next_minus_31_AC_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 29)
        self.assertFalse(rows['thirty_second_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_hentriacontic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=8222838654177922817725562880000000, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['AC_grad_next_1'], 31)
        self.assertEqual(mixed['AC_grad_next_2'], 0)
        self.assertEqual(mixed['AC_height_next'], 1)
        self.assertEqual(mixed['z_dot_AC_grad_next_minus_31_AC_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_hentriacontic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=1)


    def test_pin_site_morse_dotriacontic_rows(self):
        rows = m.pin_site_morse_dotriacontic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=263130836933693530167218012160000000)
        self.assertEqual(rows['AD_grad_next_1'], 0)
        self.assertEqual(rows['AD_grad_next_2'], 68719476736)  # 32*2^31
        self.assertEqual(rows['AD_height_next'], 4294967296)  # 2^32
        self.assertEqual(rows['z_dot_AD_grad_next_minus_32_AD_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 30)
        self.assertFalse(rows['thirty_third_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_dotriacontic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=263130836933693530167218012160000000, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['AD_grad_next_1'], 32)
        self.assertEqual(mixed['AD_grad_next_2'], 0)
        self.assertEqual(mixed['AD_height_next'], 1)
        self.assertEqual(mixed['z_dot_AD_grad_next_minus_32_AD_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_dotriacontic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=1)

    def test_pin_site_morse_tritriacontic_rows(self):
        rows = m.pin_site_morse_tritriacontic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=8683317618811886495518194401280000000)
        self.assertEqual(rows['AE_grad_next_1'], 0)
        self.assertEqual(rows['AE_grad_next_2'], 141733920768)  # 33*2^32
        self.assertEqual(rows['AE_height_next'], 8589934592)  # 2^33
        self.assertEqual(rows['z_dot_AE_grad_next_minus_33_AE_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 31)
        self.assertFalse(rows['thirty_fourth_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_tritriacontic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=8683317618811886495518194401280000000, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['AE_grad_next_1'], 33)
        self.assertEqual(mixed['AE_grad_next_2'], 0)
        self.assertEqual(mixed['AE_height_next'], 1)
        self.assertEqual(mixed['z_dot_AE_grad_next_minus_33_AE_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_tritriacontic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=1)


    def test_pin_site_morse_tetratriacontic_rows(self):
        rows = m.pin_site_morse_tetratriacontic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=295232799039604140847618609643520000000)
        self.assertEqual(rows['AF_grad_next_1'], 0)
        self.assertEqual(rows['AF_grad_next_2'], 292057776128)  # 34*2^33
        self.assertEqual(rows['AF_height_next'], 17179869184)  # 2^34
        self.assertEqual(rows['z_dot_AF_grad_next_minus_34_AF_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 32)
        self.assertFalse(rows['thirty_fifth_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_tetratriacontic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=295232799039604140847618609643520000000, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['AF_grad_next_1'], 34)
        self.assertEqual(mixed['AF_grad_next_2'], 0)
        self.assertEqual(mixed['AF_height_next'], 1)
        self.assertEqual(mixed['z_dot_AF_grad_next_minus_34_AF_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_tetratriacontic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=0, f_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=1)


    def test_pin_site_morse_hexadecic_rows(self):
        rows = m.pin_site_morse_hexadecic_rows(
            1, 2,
            f_xxxxxxxxxxxxxxxx=0, f_xxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxyyy=0,
            f_xxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxyyyyyy=0, f_xxxxxxxxxyyyyyyy=0,
            f_xxxxxxxxyyyyyyyy=0, f_xxxxxxxyyyyyyyyy=0, f_xxxxxxyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyy=0,
            f_xxxxyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyy=0,
            f_yyyyyyyyyyyyyyyy=20922789888000)
        self.assertEqual(rows['K_grad_next_1'], 0)
        self.assertEqual(rows['K_grad_next_2'], 524288)  # (1/15!)*16!*2^15
        self.assertEqual(rows['K_height_next'], 65536)  # 2^16
        self.assertEqual(rows['z_dot_K_grad_next_minus_16_K_height_next'], 0)
        self.assertEqual(rows['unmatched_density_r_power'], 14)
        self.assertFalse(rows['seventeenth_and_higher_jets_enumerated'])
        mixed = m.pin_site_morse_hexadecic_rows(
            1, 1,
            f_xxxxxxxxxxxxxxxx=20922789888000, f_xxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxyyy=0,
            f_xxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxyyyyyy=0, f_xxxxxxxxxyyyyyyy=0,
            f_xxxxxxxxyyyyyyyy=0, f_xxxxxxxyyyyyyyyy=0, f_xxxxxxyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyy=0,
            f_xxxxyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyy=0,
            f_yyyyyyyyyyyyyyyy=0)
        self.assertEqual(mixed['K_grad_next_1'], 16)
        self.assertEqual(mixed['K_grad_next_2'], 0)
        self.assertEqual(mixed['K_height_next'], 1)
        self.assertEqual(mixed['z_dot_K_grad_next_minus_16_K_height_next'], 0)
        with self.assertRaises(ValueError):
            m.pin_site_morse_hexadecic_rows(
                0, 0,
                f_xxxxxxxxxxxxxxxx=1, f_xxxxxxxxxxxxxxxy=0, f_xxxxxxxxxxxxxxyy=0, f_xxxxxxxxxxxxxyyy=0,
                f_xxxxxxxxxxxxyyyy=0, f_xxxxxxxxxxxyyyyy=0, f_xxxxxxxxxxyyyyyy=0, f_xxxxxxxxxyyyyyyy=0,
                f_xxxxxxxxyyyyyyyy=0, f_xxxxxxxyyyyyyyyy=0, f_xxxxxxyyyyyyyyyy=0, f_xxxxxyyyyyyyyyyy=0,
                f_xxxxyyyyyyyyyyyy=0, f_xxxyyyyyyyyyyyyy=0, f_xxyyyyyyyyyyyyyy=0, f_xyyyyyyyyyyyyyyy=0,
                f_yyyyyyyyyyyyyyyy=0)

    def test_pin_site_morse_next_order_rows(self):
        rows = m.pin_site_morse_next_order_rows(1, 2, f_xxx=0, f_xxy=0, f_xyy=0, f_yyy=6)
        self.assertEqual(rows['H_grad_next_1'], 0)
        self.assertEqual(rows['H_grad_next_2'], 12)  # (1/2)*6*4
        self.assertEqual(rows['H_height_next'], 8)  # (1/6)*6*8
        self.assertEqual(rows['z_dot_H_grad_next_minus_3_H_height_next'], 0)
        self.assertTrue(rows['explicit_r_factor_still_required'])
        with self.assertRaises(ValueError):
            m.pin_site_morse_next_order_rows(0, 0, f_xxx=1, f_xxy=0, f_xyy=0, f_yyy=0)

    def test_pin_morse_hessian_signature(self):
        sad = m.pin_morse_hessian_signature(H_xx=-2, H_xy=0, H_yy=3, closer_pin='S')
        self.assertEqual(sad['det_H'], -6)
        self.assertEqual(sad['signature_kind'], 'INDEFINITE_SADDLE')
        self.assertTrue(sad['signature_matches_pin_role'])
        self.assertTrue(sad['morse_nondegenerate'])
        mx = m.pin_morse_hessian_signature(H_xx=-2, H_xy=0, H_yy=-3, closer_pin='M')
        self.assertEqual(mx['det_H'], 6)
        self.assertEqual(mx['signature_kind'], 'NEGATIVE_DEFINITE_MAX')
        self.assertTrue(mx['signature_matches_pin_role'])
        # Wrong role: saddle Hessian offered for a max pin.
        bad = m.pin_morse_hessian_signature(H_xx=-2, H_xy=0, H_yy=3, closer_pin='M')
        self.assertFalse(bad['signature_matches_pin_role'])
        deg = m.pin_morse_hessian_signature(H_xx=1, H_xy=0, H_yy=0, closer_pin='S')
        self.assertEqual(deg['signature_kind'], 'DEGENERATE')
        self.assertFalse(deg['morse_nondegenerate'])
        with self.assertRaises(ValueError):
            m.pin_morse_hessian_signature(H_xx=1, H_xy=0, H_yy=-1, closer_pin='X')

    def test_pin_site_morse_contact_rows(self):
        rows = m.pin_site_morse_contact_rows(1, 2, H_xx=1, H_xy=0, H_yy=1)
        self.assertEqual(rows['J_grad_1'], 1)
        self.assertEqual(rows['J_grad_2'], 2)
        self.assertEqual(rows['J_height'], Q(5, 2))  # (1+4)/2
        self.assertEqual(rows['height_minus_half_z_dot_grad'], 0)
        self.assertTrue(rows['height_dependent_on_grad_at_leading_order'])
        with self.assertRaises(ValueError):
            m.pin_site_morse_contact_rows(0, 0, H_xx=1, H_xy=0, H_yy=1)

    def test_pin_site_jet_obstruction_ledger(self):
        y = m.point(Q(1, 2), Q(1, 20))
        obs = m.pin_site_jet_obstruction_ledger(y, inner=Q(2, 5), outer=1)
        self.assertEqual(obs['chart'], 'C_pin_centered')
        self.assertTrue(obs['pin_site_lies_on_scaled_axis'])
        self.assertEqual(obs['spatial_distance_to_pin_r_power'], 1)
        self.assertEqual(obs['spatial_volume_r_power'], 2)
        self.assertEqual(obs['z2'], Q(1, 20))
        self.assertFalse(obs['midpoint_U0_rows_applicable'])
        self.assertTrue(obs['raw_gradient_collides_with_pin_gradient_constraints'])
        self.assertTrue(obs['near_pin_intersects_axial_thin_belt_locus'])
        self.assertTrue(obs['leading_morse_rows_enumerated_elsewhere'])
        self.assertFalse(obs['pin_site_higher_jets_enumerated'])
        self.assertIn('contact_gaussian_density_bound', obs['required_before_full_chart'])
        self.assertEqual(obs['status'], 'OPEN_HIGHER_JETS_AND_DENSITY')
        with self.assertRaises(ValueError):
            m.pin_site_jet_obstruction_ledger(m.point(0, 2), inner=Q(2, 5), outer=1)

    def test_pr7_crosswalk_flags(self):
        text = (ROOT / 'CROSSWALK.md').read_text()
        self.assertIn('RN-MESOSCOPIC-CHART-PR7-CROSSWALK-20260925-v1', text)
        self.assertIn('Scientific effect: NONE', text)
        self.assertIn('contact_density_bound_proved=false', text)
        self.assertIn('leading Morse', text)
        self.assertIn('contact_density_obstruction_inventory', text)
        self.assertIn('AUTHOR_SIDE_CANDIDATE', text)
        self.assertIn('hessian_ledger_evaluated=false', text)
        self.assertIn('transverse_conditioning_uniform_bound', text)
        self.assertIn('PR #14', text)

    def test_hessian_contact_rows(self):
        rows = m.hessian_contact_rows(
            m.point(0, 2), gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4, f_yyy=5)
        self.assertEqual(rows['H_xx_contact'], 6)   # 0 + 3*2
        self.assertEqual(rows['H_xy_contact'], 8)   # 0 + 4*2
        self.assertEqual(rows['H_yy_contact'], 2)
        self.assertEqual(rows['H_yy_next'], 10)     # 4*0 + 5*2
        self.assertEqual(rows['det_contact_leading'], 12)
        self.assertEqual(rows['det_xy_square_coefficient'], 64)
        y = m.point(2, 2)
        k, a, b, c = Q(2), Q(3), Q(5), Q(7)
        rows = m.hessian_contact_rows(y, gap_mark=k, f_yy=a, f_xxy=b, f_xyy=c)
        self.assertEqual(rows['H_xx_contact'], 12 * k * 2 + b * 2)
        self.assertEqual(rows['H_xy_contact'], b * 2 + c * 2)
        self.assertEqual(rows['H_yy_contact'], a)
        self.assertEqual(rows['det_contact_leading'], rows['H_xx_contact'] * a)

    def test_hessian_scaling_and_flags(self):
        scale = m.hessian_scaling_report(2)
        self.assertEqual(scale['hessian_scaling_exponents'], {'xx': 1, 'xy': 1, 'yy': 0})
        self.assertEqual(scale['raw_det_leading_r_power'], 1)
        self.assertFalse(scale['conditioned_expectation_evaluated'])
        axial_scale = m.hessian_scaling_report(2, chart='C_axial')
        self.assertEqual(axial_scale['raw_det_leading_r_power'], 1)
        led = m.hessian_ledger_for_point(m.point(0, 2), gap_mark=1, f_yy=2)
        self.assertEqual(led['raw_det_leading_r_power'], 1)
        self.assertTrue(led['hessian_contact_rows_enumerated'])
        self.assertFalse(led['hessian_ledger_evaluated'])
        self.assertFalse(led['conditioned_expectation_evaluated'])
        self.assertFalse(led['full_annulus_closed'])
        with self.assertRaises(ValueError):
            m.hessian_contact_rows(m.point(2, 0), gap_mark=1, f_yy=1, f_xxy=0, f_xyy=0)
        with self.assertRaises(ValueError):
            m.hessian_scaling_report(2, chart='nope')

    def test_axial_hessian_contact_rows(self):
        rows = m.axial_hessian_contact_rows(
            m.point(2, 0), gap_mark=1, f_yy=2, f_xxy=3, f_xyy=5)
        self.assertEqual(rows['H_xx_contact'], 24)  # 12*1*2
        self.assertEqual(rows['H_xy_contact'], 6)   # 3*2
        self.assertEqual(rows['H_yy_contact'], 2)
        self.assertEqual(rows['H_yy_next'], 10)     # 5*2
        self.assertEqual(rows['det_contact_leading'], 48)
        with self.assertRaises(ValueError):
            m.axial_hessian_contact_rows(m.point(0, 2), gap_mark=1, f_yy=1, f_xxy=1)

    def test_contact_integrand_powers(self):
        t = m.contact_integrand_power_ledger(2, chart='C_transverse')
        self.assertEqual(t['spatial_volume_r_power'], 2)
        self.assertEqual(t['gradient_jacobian_r_power'], 3)
        self.assertEqual(t['gradient_density_r_power'], -3)
        self.assertEqual(t['hessian_det_leading_r_power'], 1)
        self.assertEqual(t['height_window_r_power'], 3)
        self.assertEqual(t['net_count_r_power'], 3)  # 2 - 3 + 1 + 3
        self.assertFalse(t['axial_chart_has_area_measure_zero'])
        self.assertFalse(t['contact_density_bound_proved'])
        a = m.contact_integrand_power_ledger(2, chart='C_axial')
        self.assertEqual(a['gradient_jacobian_r_power'], 4)
        self.assertEqual(a['net_count_r_power'], 2)  # 2 - 4 + 1 + 3
        self.assertTrue(a['axial_chart_has_area_measure_zero'])
        self.assertFalse(a['full_annulus_closed'])

    def test_pin_centered_integrand_powers(self):
        p = m.pin_centered_integrand_power_ledger(2)
        self.assertEqual(p['chart'], 'C_pin_centered')
        self.assertEqual(p['spatial_volume_r_power'], 2)
        self.assertEqual(p['gradient_jacobian_r_power'], 2)
        self.assertEqual(p['gradient_density_r_power'], -2)
        self.assertEqual(p['hessian_det_leading_r_power'], 0)
        self.assertEqual(p['height_window_r_power'], 3)
        self.assertEqual(p['net_count_r_power'], 3)  # 2 - 2 + 0 + 3
        self.assertFalse(p['pin_contact_density_bound_proved'])
        self.assertFalse(p['pin_site_higher_jets_enumerated'])
        self.assertEqual(m.PIN_CENTERED_HESSIAN_DET_R_POWER, 0)
        with self.assertRaises(ValueError):
            m.pin_centered_integrand_power_ledger(3)

    def test_contact_density_obstruction_inventory(self):
        inv = m.contact_density_obstruction_inventory()
        self.assertFalse(inv['global_contact_density_bound_proved'])
        self.assertTrue(inv['charts']['C_transverse']['chart_conditioning_singularity_cleared'])
        self.assertFalse(inv['charts']['C_transverse']['contact_gaussian_density_bounded'])
        self.assertFalse(inv['charts']['C_transverse']['height_r_factor_absorbed'])
        self.assertTrue(inv['charts']['C_axial']['area_measure_zero_in_2d'])
        self.assertTrue(inv['charts']['C_axial']['height_independent_at_leading_axial_order'])
        self.assertTrue(inv['charts']['C_axial']['no_unmatched_height_r_at_leading_order'])
        self.assertTrue(inv['charts']['C_axial']['height_grad_x_shared_mark_identity_recorded'])
        self.assertFalse(inv['charts']['C_thin_belt']['bare_1_over_abs_y2_L1'])
        self.assertTrue(inv['charts']['C_thin_belt']['jet_map_pointwise_cancel_recorded'])
        self.assertTrue(inv['charts']['C_thin_belt']['bare_reciprocal_L1_obstruction_cleared_by_cancel'])
        self.assertTrue(inv['charts']['C_thin_belt']['residual_geometric_factor_locally_L1'])
        self.assertTrue(inv['charts']['C_thin_belt']['contact_integrand_algebraic_factor_skeleton_enumerated'])
        self.assertTrue(inv['charts']['C_thin_belt']['height_r_factor_recorded'])
        self.assertFalse(inv['charts']['C_thin_belt']['height_r_factor_absorbed'])
        self.assertTrue(inv['charts']['C_thin_belt']['algebraic_factor_times_height_r_skeleton_enumerated'])
        self.assertFalse(inv['charts']['C_thin_belt']['uniform_integrand_bound_proved'])
        self.assertTrue(inv['charts']['C_pin_centered']['leading_morse_rows_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['cubic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['quartic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['quintic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['sextic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['septic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['octic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['nonic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['decic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['undecic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['dodecic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['tridecic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['tetradecic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['pentadecic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['hexadecic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['heptadecic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['octadecic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['nonadecic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['icosic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['henicosic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['docosic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['tricosic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['tetracosic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['pentacosic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['hexacosic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['heptacosic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['octacosic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['nonacosic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['triacontic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['hentriacontic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['dotriacontic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['tritriacontic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['tetratriacontic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['unmatched_height_r_power_inventory_recorded'])
        self.assertTrue(inv['charts']['C_pin_centered']['free_jet_residual_inventory_recorded'])
        self.assertTrue(inv['charts']['C_pin_centered']['gradient_contact_jacobian_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['conditioned_hessian_residual_polynomials_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['conditioned_hessian_det_skeleton_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['contact_integrand_algebraic_factor_skeleton_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['height_r_factor_recorded'])
        self.assertFalse(inv['charts']['C_pin_centered']['height_r_factor_absorbed'])
        self.assertTrue(inv['charts']['C_pin_centered']['algebraic_factor_times_height_r_skeleton_enumerated'])
        self.assertFalse(inv['charts']['C_pin_centered']['thirty_fifth_and_higher_jets_enumerated'])
        self.assertTrue(inv['charts']['C_transverse']['free_jet_residual_inventory_recorded'])
        self.assertTrue(inv['charts']['C_axial']['free_jet_residual_inventory_recorded'])
        self.assertTrue(inv['charts']['C_thin_belt']['free_jet_residual_inventory_recorded'])
        self.assertTrue(inv['charts']['C_transverse']['gradient_contact_jacobian_enumerated'])
        self.assertTrue(inv['charts']['C_axial']['gradient_contact_jacobian_enumerated'])
        self.assertTrue(inv['charts']['C_thin_belt']['gradient_contact_jacobian_enumerated'])
        self.assertTrue(inv['charts']['C_thin_belt']['conditioned_hessian_residual_polynomials_enumerated'])
        self.assertTrue(inv['charts']['C_thin_belt']['conditioned_hessian_det_skeleton_enumerated'])
        self.assertTrue(inv['charts']['C_thin_belt']['height_residual_after_grad_contact_enumerated'])
        self.assertTrue(inv['charts']['C_thin_belt']['bare_reciprocal_L1_obstruction_cleared_by_cancel'])
        self.assertTrue(inv['charts']['C_transverse']['conditioned_hessian_residual_polynomials_enumerated'])
        self.assertTrue(inv['charts']['C_axial']['conditioned_hessian_residual_polynomials_enumerated'])
        self.assertTrue(inv['charts']['C_transverse']['conditioned_hessian_det_skeleton_enumerated'])
        self.assertTrue(inv['charts']['C_axial']['conditioned_hessian_det_skeleton_enumerated'])
        self.assertTrue(inv['charts']['C_transverse']['contact_integrand_algebraic_factor_skeleton_enumerated'])
        self.assertTrue(inv['charts']['C_axial']['contact_integrand_algebraic_factor_skeleton_enumerated'])
        self.assertTrue(inv['charts']['C_transverse']['height_residual_after_grad_contact_enumerated'])
        self.assertTrue(inv['charts']['C_transverse']['algebraic_factor_times_height_r_skeleton_enumerated'])
        self.assertFalse(inv['charts']['C_transverse']['hessian_conditioned_expectation_evaluated'])
        self.assertIn('contact_gaussian_density_factor', inv['open_blockers'])
        self.assertIn('conditioned_hessian_expectation', inv['open_blockers'])
        self.assertIn('thin_belt_contact_gaussian_density_near_y2_0', inv['open_blockers'])
        self.assertIn('thin_belt_height_r_absorption', inv['open_blockers'])
        self.assertNotIn('thin_belt_uniform_integrand_after_cancel', inv['open_blockers'])
        self.assertIn('pin_thirty_fifth_and_higher_jets', inv['open_blockers'])
        self.assertIn('pin_centered_height_r_absorption', inv['open_blockers'])
        self.assertNotIn('pin_thirty_first_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_thirtieth_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_twenty_ninth_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_twenty_eighth_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_twenty_seventh_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_twenty_sixth_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_twenty_fifth_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_twenty_fourth_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_twenty_third_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_twenty_second_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_twenty_first_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_twelfth_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_eleventh_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_tenth_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_ninth_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_eighth_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_seventh_and_higher_jets', inv['open_blockers'])
        self.assertNotIn('pin_sixth_and_higher_jets', inv['open_blockers'])
        # Every chart still blocks the global density bound.
        for chart, row in inv['charts'].items():
            self.assertFalse(row['contact_gaussian_density_bounded'], chart)

    def test_contact_free_jet_residual_inventory(self):
        t0 = m.transverse_free_jet_residual_inventory(m.point(0, 2))
        self.assertEqual(t0['leading_grad_map_rank'], 2)
        self.assertEqual(t0['free_directions_after_grad_contact'], 2)
        self.assertEqual(t0['grad_x_second_row_isolates'], 'f_xyy')
        self.assertEqual(t0['free_among_leading_grad_coords'], ['k', 'f_xxy'])
        self.assertTrue(t0['f_yyy_absent_from_leading_grad_rows'])
        self.assertFalse(t0['contact_gaussian_density_bounded'])
        self.assertFalse(t0['conditioned_hessian_expectation_evaluated'])
        t1 = m.transverse_free_jet_residual_inventory(m.point(2, 2))
        self.assertEqual(t1['free_directions_after_grad_contact'], 2)
        self.assertEqual(t1['grad_x_second_row_isolates'], 'linear_form_on_k_f_xxy_f_xyy')
        self.assertEqual(t1['grad_x_coefficient_k'], 24)
        ax = m.axial_free_jet_residual_inventory(m.point(2, 0))
        self.assertEqual(ax['free_directions_after_grad_contact'], 0)
        self.assertTrue(ax['grad_y_isolates_f_xxy'])
        self.assertTrue(ax['grad_x_isolates_k'])
        self.assertEqual(ax['free_hessian_height_jet_coords'], ['f_yy', 'f_xyy', 'f_yyy'])
        self.assertTrue(ax['axial_area_measure_zero'])
        self.assertFalse(ax['contact_gaussian_density_bounded'])
        bundled = m.contact_free_jet_residual_inventory()
        self.assertFalse(bundled['global_contact_density_bound_proved'])
        self.assertEqual(bundled['C_transverse']['free_directions_after_grad_contact'], 2)
        thin = m.thin_belt_free_jet_residual_inventory(m.point(2, Q(1, 8)))
        self.assertEqual(thin['chart'], 'C_thin_belt')
        self.assertEqual(thin['free_directions_after_grad_contact'], 2)
        self.assertEqual(thin['grad_x_second_row_isolates'], 'linear_form_on_k_f_xxy_f_xyy')
        self.assertTrue(thin['reciprocal_diverges_as_y2_to_0'])
        self.assertTrue(thin['bare_reciprocal_L1_obstruction_cleared_by_cancel'])
        self.assertFalse(thin['contact_gaussian_density_bounded'])
        self.assertEqual(bundled['C_thin_belt']['free_directions_after_grad_contact'], 2)
        pin = m.pin_centered_free_jet_residual_inventory(
            m.point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1)
        self.assertEqual(pin['leading_grad_map_rank'], 2)
        self.assertEqual(pin['free_directions_after_grad_contact'], 1)
        self.assertEqual(pin['free_among_leading_grad_coords'], ['H_xx'])
        self.assertEqual(pin['eliminated_coordinates'], ['H_xy', 'H_yy'])
        self.assertEqual(pin['elimination_branch'], 'z2_nonzero')
        self.assertEqual(pin['abs_det_grad_contact_map'], Q(1, 400))
        self.assertTrue(pin['higher_pin_jets_free_for_height_residuals'])
        self.assertFalse(pin['contact_gaussian_density_bounded'])
        self.assertEqual(bundled['C_pin_centered']['free_directions_after_grad_contact'], 1)
        pin_axis = m.pin_centered_free_jet_residual_inventory(
            m.point(Q(11, 20), 0), inner=Q(2, 5), outer=1)
        self.assertEqual(pin_axis['elimination_branch'], 'z1_nonzero_z2_zero')
        self.assertEqual(pin_axis['free_among_leading_grad_coords'], ['H_yy'])
        with self.assertRaises(ValueError):
            m.transverse_free_jet_residual_inventory(m.point(2, 0))
        with self.assertRaises(ValueError):
            m.axial_free_jet_residual_inventory(m.point(0, 2))

    def test_pin_centered_free_jet_residual_inventory(self):
        pin = m.pin_centered_free_jet_residual_inventory(
            m.point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1)
        self.assertEqual(pin['chart'], 'C_pin_centered')
        self.assertEqual(pin['leading_grad_jet_coordinates'], ['H_xx', 'H_xy', 'H_yy'])
        self.assertEqual(pin['free_directions_after_grad_contact'], 1)
        self.assertFalse(pin['conditioned_hessian_expectation_evaluated'])
        with self.assertRaises(ValueError):
            m.pin_centered_free_jet_residual_inventory(m.point(0, 2), inner=Q(2, 5), outer=1)

    def test_conditioned_hessian_residual_ledger(self):
        # Axis-aligned transverse sample: y1=0 isolates f_xyy from J_x.
        led = m.transverse_conditioned_hessian_residual_ledger(
            m.point(0, 2), gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4)
        self.assertEqual(led['free_residual_coordinates'], ['k', 'f_xxy'])
        self.assertEqual(led['f_yy_minus_solved'], 0)
        self.assertEqual(led['f_xyy_minus_solved'], 0)
        self.assertEqual(led['H_xx_minus_raw'], 0)
        self.assertEqual(led['H_xy_minus_raw'], 0)
        self.assertEqual(led['H_yy_minus_raw'], 0)
        self.assertEqual(led['H_xx_residual'], 6)   # f_xxy * y2 = 3*2
        self.assertEqual(led['H_yy_residual'], 2)
        self.assertEqual(led['H_xy_residual'], 8)   # f_xyy * y2 = 4*2
        self.assertEqual(led['det_contact_leading_residual'], 12)
        self.assertTrue(led['conditioned_hessian_residual_polynomials_enumerated'])
        self.assertFalse(led['conditioned_expectation_evaluated'])
        # Off-axis: still exact match to raw Hessian.
        off = m.transverse_conditioned_hessian_residual_ledger(
            m.point(2, 2), gap_mark=1, f_yy=5, f_xxy=3, f_xyy=7)
        self.assertEqual(off['f_yy_minus_solved'], 0)
        self.assertEqual(off['f_xyy_minus_solved'], 0)
        self.assertEqual(off['H_xx_minus_raw'], 0)
        self.assertEqual(off['H_xy_minus_raw'], 0)
        self.assertEqual(off['H_yy_minus_raw'], 0)
        ax = m.axial_conditioned_hessian_residual_ledger(
            m.point(2, 0), gap_mark=1, f_yy=5, f_xxy=3)
        self.assertEqual(ax['H_xx_minus_raw'], 0)
        self.assertEqual(ax['H_xy_minus_raw'], 0)
        self.assertEqual(ax['H_yy_minus_raw'], 0)
        self.assertEqual(ax['H_xx_from_J_grad_x'], 24)  # 12*k*y1
        self.assertEqual(ax['H_xy_from_J_grad_y'], 6)   # f_xxy*y1
        self.assertEqual(ax['H_yy_free_residual'], 5)
        self.assertTrue(ax['axial_area_measure_zero'])
        self.assertFalse(ax['conditioned_expectation_evaluated'])
        pin = m.pin_centered_conditioned_hessian_residual_ledger(
            m.point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1, H_xx=-2, H_xy=0, H_yy=3)
        self.assertEqual(pin['elimination_branch'], 'z2_nonzero')
        self.assertEqual(pin['free_residual_coordinates'], ['H_xx'])
        self.assertEqual(pin['H_xy_minus_solved'], 0)
        self.assertEqual(pin['H_yy_minus_solved'], 0)
        self.assertEqual(pin['H_xx_minus_raw'], 0)
        self.assertEqual(pin['H_xy_minus_raw'], 0)
        self.assertEqual(pin['H_yy_minus_raw'], 0)
        self.assertEqual(pin['det_contact_leading_residual'], -6)
        self.assertEqual(pin['det_minus_raw'], 0)
        self.assertTrue(pin['conditioned_hessian_residual_polynomials_enumerated'])
        self.assertFalse(pin['conditioned_expectation_evaluated'])
        pin_axis = m.pin_centered_conditioned_hessian_residual_ledger(
            m.point(Q(11, 20), 0), inner=Q(2, 5), outer=1, H_xx=-2, H_xy=1, H_yy=3)
        self.assertEqual(pin_axis['elimination_branch'], 'z1_nonzero_z2_zero')
        self.assertEqual(pin_axis['free_residual_coordinates'], ['H_yy'])
        self.assertEqual(pin_axis['H_xx_minus_solved'], 0)
        self.assertEqual(pin_axis['H_xy_minus_solved'], 0)
        self.assertEqual(pin_axis['det_minus_raw'], 0)
        thin = m.thin_belt_conditioned_hessian_residual_ledger(
            m.point(2, Q(1, 8)), gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0)
        self.assertEqual(thin['chart'], 'C_thin_belt')
        self.assertEqual(thin['f_yy_minus_solved'], 0)
        self.assertEqual(thin['f_xyy_minus_solved'], 0)
        self.assertEqual(thin['H_xx_minus_raw'], 0)
        self.assertEqual(thin['H_yy_residual'], 2)
        self.assertTrue(thin['reciprocal_diverges_as_y2_to_0'])
        self.assertFalse(thin['conditioned_expectation_evaluated'])
        with self.assertRaises(ValueError):
            m.transverse_conditioned_hessian_residual_ledger(m.point(2, 0))
        with self.assertRaises(ValueError):
            m.axial_conditioned_hessian_residual_ledger(m.point(0, 2))
        with self.assertRaises(ValueError):
            m.pin_centered_conditioned_hessian_residual_ledger(
                m.point(Q(1, 2), 0), inner=Q(2, 5), outer=1)
        with self.assertRaises(ValueError):
            m.thin_belt_conditioned_hessian_residual_ledger(m.point(0, 2))

    def test_thin_belt_conditioned_hessian_residual(self):
        thin = m.thin_belt_conditioned_hessian_residual_ledger(
            m.point(2, Q(1, 8)), gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4)
        self.assertEqual(thin['free_residual_coordinates'], ['k', 'f_xxy'])
        self.assertEqual(thin['H_xx_residual'], Q(195, 8))  # 12*1*2 + 3*(1/8)
        self.assertEqual(thin['H_yy_residual'], 2)
        self.assertEqual(thin['det_contact_leading_residual'], Q(195, 4))
        skel = m.thin_belt_conditioned_det_free_jet_skeleton(
            m.point(2, Q(1, 8)), gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4)
        self.assertEqual(skel['alpha_f_xxy'], Q(1, 4))  # J_y = f_yy y2 = 2/8
        self.assertEqual(skel['det_minus_alpha_form'], 0)
        self.assertTrue(skel['linear_in_free_residuals'])
        self.assertTrue(skel['reciprocal_diverges_as_y2_to_0'])
        self.assertFalse(skel['conditioned_expectation_evaluated'])

    def test_pin_centered_conditioned_hessian_residual(self):
        pin = m.pin_centered_conditioned_hessian_residual_ledger(
            m.point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1, H_xx=-2, H_xy=1, H_yy=4)
        self.assertEqual(pin['chart'], 'C_pin_centered')
        self.assertEqual(pin['H_xy_residual'], 1)  # J1/z2 with z1=0
        self.assertEqual(pin['H_yy_residual'], 4)
        self.assertEqual(pin['det_contact_leading_residual'], -9)  # -2*4 - 1
        self.assertFalse(pin['hessian_ledger_evaluated'])
        skel = m.pin_centered_conditioned_det_free_jet_skeleton(
            m.point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1, H_xx=-2, H_xy=1, H_yy=4)
        self.assertEqual(skel['alpha_H_xx'], 4)  # J2/z2 = H_yy
        self.assertEqual(skel['beta_const'], -1)  # -J1²/z2² = -H_xy²
        self.assertEqual(skel['det_contact_leading_from_alpha_beta'], -9)
        self.assertEqual(skel['det_minus_alpha_beta_form'], 0)
        self.assertTrue(skel['linear_in_free_residuals'])
        self.assertFalse(skel['conditioned_expectation_evaluated'])

    def test_transverse_height_residual_after_grad_contact(self):
        # y1=0: residual collapses to (1/6) f_yyy y2^3
        led = m.transverse_height_residual_after_grad_contact(
            m.point(0, 2), gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4, f_yyy=6)
        self.assertEqual(led['free_residual_coordinates'], ['k', 'f_xxy', 'f_yyy'])
        self.assertEqual(led['f_xyy_minus_solved'], 0)
        self.assertEqual(led['H_height_next_minus_raw'], 0)
        self.assertEqual(led['H_height_next_residual'], 8)  # (1/6)*6*8
        self.assertEqual(led['unmatched_height_density_r_power'], 1)
        self.assertFalse(led['height_r_absorbed_into_uniform_bound'])
        self.assertFalse(led['contact_gaussian_density_bounded'])
        # Off-axis identity check.
        off = m.transverse_height_residual_after_grad_contact(
            m.point(2, 2), gap_mark=1, f_yy=5, f_xxy=3, f_xyy=7, f_yyy=9)
        self.assertEqual(off['f_xyy_minus_solved'], 0)
        self.assertEqual(off['H_height_next_minus_raw'], 0)
        with self.assertRaises(ValueError):
            m.transverse_height_residual_after_grad_contact(m.point(2, 0))

    def test_thin_belt_height_residual_after_grad_contact(self):
        # Shared transverse residual form on thin_belt_ok; reciprocal diverges as y2→0.
        thin = m.thin_belt_height_residual_after_grad_contact(
            m.point(2, Q(1, 8)), gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0, f_yyy=6)
        self.assertEqual(thin['chart'], 'C_thin_belt')
        self.assertEqual(thin['free_residual_coordinates'], ['k', 'f_xxy', 'f_yyy'])
        self.assertEqual(thin['f_xyy_minus_solved'], 0)
        self.assertEqual(thin['H_height_next_minus_raw'], 0)
        self.assertEqual(thin['H_height_next_residual'], Q(8193, 512))  # 16 + 1/512
        self.assertEqual(thin['unmatched_height_density_r_power'], 1)
        self.assertTrue(thin['reciprocal_diverges_as_y2_to_0'])
        self.assertFalse(thin['height_r_absorbed_into_uniform_bound'])
        self.assertFalse(thin['contact_gaussian_density_bounded'])
        off = m.thin_belt_height_residual_after_grad_contact(
            m.point(2, Q(1, 8)), gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4, f_yyy=6)
        self.assertEqual(off['f_xyy_minus_solved'], 0)
        self.assertEqual(off['H_height_next_minus_raw'], 0)
        self.assertEqual(off['H_height_next_residual'], Q(8609, 512))
        with self.assertRaises(ValueError):
            m.thin_belt_height_residual_after_grad_contact(m.point(0, 2))
        with self.assertRaises(ValueError):
            m.thin_belt_height_residual_after_grad_contact(m.point(2, 0))

    def test_gradient_contact_jacobian_density_shape(self):
        t = m.transverse_gradient_contact_jacobian_ledger_with_floor(m.point(0, 2))
        self.assertEqual(t['abs_det_grad_contact_map'], 4)  # 8/2
        self.assertEqual(t['lower_bound_on_chart_abs_det'], Q(1, 128))  # (1/4)^3 / 2
        self.assertTrue(t['abs_det_ge_chart_lower_bound'])
        self.assertTrue(t['jacobian_matrix_diagonal'])
        self.assertFalse(t['contact_gaussian_density_bounded'])
        off = m.transverse_gradient_contact_jacobian_ledger(m.point(2, 2))
        self.assertEqual(off['abs_det_grad_contact_map'], 4)
        ax = m.axial_gradient_contact_jacobian_ledger(m.point(2, 0))
        self.assertEqual(ax['abs_det_grad_contact_map'], 48)  # 3*16
        self.assertTrue(ax['axial_area_measure_zero'])
        self.assertFalse(ax['contact_gaussian_density_bounded'])
        pin = m.pin_centered_gradient_contact_jacobian_ledger(
            m.point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1)
        self.assertEqual(pin['abs_det_grad_contact_map'], Q(1, 400))
        self.assertEqual(pin['elimination_branch'], 'z2_nonzero')
        self.assertEqual(pin['eliminated_coordinates'], ['H_xy', 'H_yy'])
        self.assertEqual(pin['partial_J1_partial_H_xy'], Q(1, 20))
        self.assertEqual(pin['partial_J2_partial_H_yy'], Q(1, 20))
        self.assertFalse(pin['jacobian_matrix_diagonal'])
        self.assertFalse(pin['contact_gaussian_density_bounded'])
        pin_axis = m.pin_centered_gradient_contact_jacobian_ledger(
            m.point(Q(11, 20), 0), inner=Q(2, 5), outer=1)
        self.assertEqual(pin_axis['elimination_branch'], 'z1_nonzero_z2_zero')
        self.assertEqual(pin_axis['abs_det_grad_contact_map'], Q(1, 400))
        self.assertTrue(pin_axis['jacobian_matrix_diagonal'])
        thin = m.thin_belt_gradient_contact_jacobian_ledger(m.point(2, Q(1, 8)))
        self.assertEqual(thin['abs_det_grad_contact_map'], Q(1, 1024))  # (1/8)^3 / 2
        self.assertTrue(thin['reciprocal_diverges_as_y2_to_0'])
        self.assertTrue(thin['jacobian_matrix_diagonal'])
        self.assertFalse(thin['contact_gaussian_density_bounded'])
        bundled = m.contact_gradient_jacobian_density_shape_inventory()
        self.assertFalse(bundled['global_contact_density_bound_proved'])
        self.assertEqual(bundled['C_transverse']['abs_det_grad_contact_map'], 4)
        self.assertEqual(bundled['C_pin_centered']['abs_det_grad_contact_map'], Q(1, 400))
        self.assertEqual(bundled['C_thin_belt']['abs_det_grad_contact_map'], Q(1, 1024))
        with self.assertRaises(ValueError):
            m.transverse_gradient_contact_jacobian_ledger(m.point(2, 0))
        with self.assertRaises(ValueError):
            m.axial_gradient_contact_jacobian_ledger(m.point(0, 2))
        with self.assertRaises(ValueError):
            m.pin_centered_gradient_contact_jacobian_ledger(
                m.point(0, 2), inner=Q(2, 5), outer=1)
        with self.assertRaises(ValueError):
            m.thin_belt_gradient_contact_jacobian_ledger(m.point(0, 2))

    def test_thin_belt_free_jet_and_gradient_contact_jacobian(self):
        thin = m.thin_belt_free_jet_residual_inventory(m.point(2, Q(1, 8)))
        self.assertEqual(thin['leading_grad_map_rank'], 2)
        self.assertEqual(thin['free_directions_after_grad_contact'], 2)
        self.assertTrue(thin['reciprocal_diverges_as_y2_to_0'])
        self.assertFalse(thin['uniform_integrand_bound_proved'])
        jac = m.thin_belt_gradient_contact_jacobian_ledger(m.point(2, Q(1, 8)))
        self.assertEqual(jac['chart'], 'C_thin_belt')
        self.assertEqual(jac['partial_J_y_partial_f_yy'], Q(1, 8))
        self.assertEqual(jac['partial_J_x_partial_f_xyy'], Q(1, 128))
        self.assertTrue(jac['bare_reciprocal_L1_obstruction_cleared_by_cancel'])
        with self.assertRaises(ValueError):
            m.thin_belt_free_jet_residual_inventory(m.point(0, 2))

    def test_pin_centered_gradient_contact_jacobian(self):
        pin = m.pin_centered_gradient_contact_jacobian_ledger(
            m.point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1)
        self.assertEqual(pin['chart'], 'C_pin_centered')
        self.assertEqual(pin['free_residual_coordinates'], ['H_xx'])
        self.assertEqual(pin['partial_J2_partial_H_xy'], 0)  # z1=0 at sample
        self.assertFalse(pin['global_contact_density_bound_proved'])
        with self.assertRaises(ValueError):
            m.pin_centered_gradient_contact_jacobian_ledger(
                m.point(Q(1, 2), 0), inner=Q(2, 5), outer=1)  # z = 0 at pin site
    def test_conditioned_det_free_jet_skeleton(self):
        # y1=0: α_k=0, α_f_xxy=J_grad_y=4, det=4*f_xxy=12
        t = m.transverse_conditioned_det_free_jet_skeleton(
            m.point(0, 2), gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4)
        self.assertEqual(t['alpha_k'], 0)
        self.assertEqual(t['alpha_f_xxy'], 4)
        self.assertEqual(t['det_contact_leading_from_alphas'], 12)
        self.assertEqual(t['det_minus_alpha_form'], 0)
        self.assertEqual(t['free_jet_polynomial_degree'], 1)
        self.assertTrue(t['linear_in_free_residuals'])
        self.assertTrue(t['conditioned_hessian_det_skeleton_enumerated'])
        self.assertFalse(t['conditioned_expectation_evaluated'])
        off = m.transverse_conditioned_det_free_jet_skeleton(
            m.point(2, 2), gap_mark=1, f_yy=5, f_xxy=3, f_xyy=7)
        self.assertEqual(off['det_minus_alpha_form'], 0)
        self.assertEqual(off['alpha_k'], 120)  # 12*2*10/2
        self.assertEqual(off['alpha_f_xxy'], 10)  # J_grad_y = f_yy*y2 = 5*2
        ax = m.axial_conditioned_det_free_jet_skeleton(
            m.point(2, 0), gap_mark=1, f_yy=5, f_xxy=3)
        self.assertEqual(ax['alpha_f_yy'], 24)  # 12*k*y1
        self.assertEqual(ax['det_contact_leading_from_alpha'], 120)
        self.assertEqual(ax['det_minus_alpha_form'], 0)
        self.assertTrue(ax['axial_area_measure_zero'])
        self.assertFalse(ax['conditioned_expectation_evaluated'])
        bundled = m.contact_conditioned_det_free_jet_skeleton_inventory()
        self.assertFalse(bundled['conditioned_expectation_evaluated'])
        self.assertFalse(bundled['global_contact_density_bound_proved'])
        self.assertEqual(bundled['C_transverse']['det_minus_alpha_form'], 0)
        pin = m.pin_centered_conditioned_det_free_jet_skeleton(
            m.point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1, H_xx=-2, H_xy=0, H_yy=3)
        self.assertEqual(pin['alpha_H_xx'], 3)
        self.assertEqual(pin['beta_const'], 0)
        self.assertEqual(pin['det_contact_leading_from_alpha_beta'], -6)
        self.assertEqual(pin['det_minus_alpha_beta_form'], 0)
        self.assertEqual(bundled['C_pin_centered']['det_minus_alpha_beta_form'], 0)
        thin = m.thin_belt_conditioned_det_free_jet_skeleton(
            m.point(2, Q(1, 8)), gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0)
        self.assertEqual(thin['alpha_k'], 48)  # 12*2*(1/4)/(1/8)=48
        self.assertEqual(thin['alpha_f_xxy'], Q(1, 4))
        self.assertEqual(thin['det_minus_alpha_form'], 0)
        self.assertEqual(bundled['C_thin_belt']['det_minus_alpha_form'], 0)
        pin_axis = m.pin_centered_conditioned_det_free_jet_skeleton(
            m.point(Q(11, 20), 0), inner=Q(2, 5), outer=1, H_xx=-2, H_xy=1, H_yy=3)
        self.assertEqual(pin_axis['elimination_branch'], 'z1_nonzero_z2_zero')
        self.assertEqual(pin_axis['alpha_H_yy'], -2)  # J1/z1 = H_xx
        self.assertEqual(pin_axis['det_minus_alpha_beta_form'], 0)
        with self.assertRaises(ValueError):
            m.transverse_conditioned_det_free_jet_skeleton(m.point(2, 0))
        with self.assertRaises(ValueError):
            m.axial_conditioned_det_free_jet_skeleton(m.point(0, 2))
        with self.assertRaises(ValueError):
            m.pin_centered_conditioned_det_free_jet_skeleton(
                m.point(Q(1, 2), 0), inner=Q(2, 5), outer=1)
        with self.assertRaises(ValueError):
            m.thin_belt_conditioned_det_free_jet_skeleton(m.point(0, 2))

    def test_contact_integrand_algebraic_factor_skeleton(self):
        # y=(0,2): |det J|=|y2|^3/2=4, reciprocal=1/4, |det H|=12, product=3
        t = m.transverse_contact_integrand_algebraic_factor_skeleton(
            m.point(0, 2), gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4, f_yyy=6)
        self.assertEqual(t['abs_det_grad_contact_map'], 4)
        self.assertEqual(t['reciprocal_grad_contact_jacobian'], Q(1, 4))
        self.assertEqual(t['det_contact_leading_abs'], 12)
        self.assertEqual(t['algebraic_jacobian_times_det_abs'], 3)
        self.assertEqual(t['product_minus_factors'], 0)
        self.assertEqual(t['unmatched_height_density_r_power'], 1)
        self.assertEqual(t['net_count_r_power'], 3)
        self.assertTrue(t['contact_integrand_algebraic_factor_skeleton_enumerated'])
        self.assertFalse(t['contact_gaussian_density_bounded'])
        self.assertFalse(t['height_r_absorbed_into_uniform_bound'])
        off = m.transverse_contact_integrand_algebraic_factor_skeleton(
            m.point(2, 2), gap_mark=1, f_yy=5, f_xxy=3, f_xyy=7)
        self.assertEqual(off['product_minus_factors'], 0)
        ax = m.axial_contact_integrand_algebraic_factor_skeleton(
            m.point(2, 0), gap_mark=1, f_yy=5, f_xxy=3)
        # |det J|=3*|y1|^4=48, reciprocal=1/48, |det H|=120, product=120/48=2.5=5/2
        self.assertEqual(ax['abs_det_grad_contact_map'], 48)
        self.assertEqual(ax['reciprocal_grad_contact_jacobian'], Q(1, 48))
        self.assertEqual(ax['det_contact_leading_abs'], 120)
        self.assertEqual(ax['algebraic_jacobian_times_det_abs'], Q(5, 2))
        self.assertEqual(ax['product_minus_factors'], 0)
        self.assertTrue(ax['axial_area_measure_zero'])
        bundled = m.contact_integrand_algebraic_factor_skeleton_inventory()
        self.assertFalse(bundled['global_contact_density_bound_proved'])
        self.assertEqual(bundled['C_transverse']['algebraic_jacobian_times_det_abs'], 3)
        self.assertTrue(bundled['C_thin_belt']['reciprocal_diverges_as_y2_to_0'])
        with self.assertRaises(ValueError):
            m.transverse_contact_integrand_algebraic_factor_skeleton(m.point(2, 0))
        with self.assertRaises(ValueError):
            m.axial_contact_integrand_algebraic_factor_skeleton(m.point(0, 2))

    def test_pin_centered_contact_integrand_algebraic_factor_skeleton(self):
        # z=(0,1/20), H=(-2,0,3): |det J|=z2^2=1/400, reciprocal=400, |det H|=6, product=2400
        t = m.pin_centered_contact_integrand_algebraic_factor_skeleton(
            m.point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1, H_xx=-2, H_xy=0, H_yy=3)
        self.assertEqual(t['chart'], 'C_pin_centered')
        self.assertEqual(t['abs_det_grad_contact_map'], Q(1, 400))
        self.assertEqual(t['reciprocal_grad_contact_jacobian'], 400)
        self.assertEqual(t['det_H'], -6)
        self.assertEqual(t['det_contact_leading_abs'], 6)
        self.assertEqual(t['algebraic_jacobian_times_det_abs'], 2400)
        self.assertEqual(t['product_minus_factors'], 0)
        self.assertEqual(t['elimination_branch'], 'z2_nonzero')
        self.assertEqual(t['free_residual_coordinates'], ['H_xx'])
        self.assertEqual(t['net_count_r_power'], 3)
        self.assertTrue(t['contact_integrand_algebraic_factor_skeleton_enumerated'])
        self.assertFalse(t['contact_gaussian_density_bounded'])
        self.assertFalse(t['global_contact_density_bound_proved'])
        # z with z2=0 branch: pin S at (1/2,0), take y=(1/2+1/20, 0)=(11/20,0) — may fail near_pin
        # Use synthetic z1-only via point near M with z2≈0 is hard; check z1 branch via frame point
        # Direct: point with z=(1/20,0) relative to S=(1/2,0) => y=(1/2+1/20, 0)=(11/20, 0)
        # near_pin may require both coords; instead verify branch via unit call with constructed frame
        off = m.pin_centered_contact_integrand_algebraic_factor_skeleton(
            m.point(Q(1, 2), Q(1, 25)), inner=Q(2, 5), outer=1, H_xx=-1, H_xy=0, H_yy=2)
        self.assertEqual(off['product_minus_factors'], 0)
        self.assertEqual(off['elimination_branch'], 'z2_nonzero')
        self.assertEqual(off['abs_det_grad_contact_map'], Q(1, 625))
        bundled = m.contact_integrand_algebraic_factor_skeleton_inventory()
        self.assertEqual(bundled['C_pin_centered']['algebraic_jacobian_times_det_abs'], 2400)
        with self.assertRaises(ValueError):
            # on the pin site itself z=0
            m.pin_centered_contact_integrand_algebraic_factor_skeleton(
                m.point(Q(1, 2), 0), inner=Q(2, 5), outer=1)

    def test_pin_centered_height_r_factor_ledger(self):
        led = m.pin_centered_height_r_factor_ledger(
            m.point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1,
            H_xx=-2, H_xy=0, H_yy=3, f_yyy=6)
        self.assertEqual(led['chart'], 'C_pin_centered')
        self.assertTrue(led['leading_height_dependent_on_grad'])
        self.assertEqual(led['height_dependency_factor_half'], Q(1, 2))
        self.assertEqual(led['J_height'], Q(3, 800))
        self.assertEqual(led['height_minus_half_z_dot_grad'], 0)
        self.assertEqual(led['H_height_next'], Q(1, 8000))
        self.assertEqual(led['z_dot_H_grad_next_minus_3_H_height_next'], 0)
        self.assertEqual(led['unmatched_height_density_r_power'], 1)
        self.assertTrue(led['explicit_r_factor_still_required'])
        self.assertTrue(led['next_order_supplies_independent_height'])
        self.assertFalse(led['height_r_absorbed_into_uniform_bound'])
        self.assertFalse(led['contact_gaussian_density_bounded'])
        with self.assertRaises(ValueError):
            m.pin_centered_height_r_factor_ledger(
                m.point(Q(1, 2), 0), inner=Q(2, 5), outer=1)

    def test_pin_centered_algebraic_factor_times_height_r_skeleton(self):
        # product=2400, unmatched height r^1
        t = m.pin_centered_algebraic_factor_times_height_r_skeleton(
            m.point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1,
            H_xx=-2, H_xy=0, H_yy=3, f_yyy=6)
        self.assertEqual(t['chart'], 'C_pin_centered')
        self.assertEqual(t['algebraic_jacobian_times_det_abs'], 2400)
        self.assertEqual(t['unmatched_height_density_r_power'], 1)
        self.assertEqual(t['combined_skeleton_height_r_power'], 1)
        self.assertEqual(t['algebraic_factor_r_power_after_stripping'], 0)
        self.assertEqual(t['product_minus_recorded_factors'], 0)
        self.assertEqual(t['H_height_next'], Q(1, 8000))
        self.assertTrue(t['combined_algebraic_factor_and_height_r_recorded'])
        self.assertFalse(t['height_r_absorbed_into_uniform_bound'])
        self.assertFalse(t['combined_skeleton_absorbed_into_uniform_bound'])
        self.assertFalse(t['contact_gaussian_density_bounded'])
        self.assertFalse(t['global_contact_density_bound_proved'])
        with self.assertRaises(ValueError):
            m.pin_centered_algebraic_factor_times_height_r_skeleton(
                m.point(Q(1, 2), 0), inner=Q(2, 5), outer=1)

    def test_contact_algebraic_factor_times_height_r_inventory(self):
        inv = m.contact_algebraic_factor_times_height_r_inventory()
        self.assertEqual(
            inv['charts_with_combined_skeleton'],
            ['C_transverse', 'C_thin_belt', 'C_pin_centered'],
        )
        self.assertEqual(inv['C_transverse']['algebraic_jacobian_times_det_abs'], 3)
        self.assertEqual(inv['C_transverse']['combined_skeleton_height_r_power'], 1)
        self.assertEqual(inv['C_thin_belt']['algebraic_jacobian_times_det_abs'], 49152)
        self.assertEqual(inv['C_thin_belt']['combined_skeleton_height_r_power'], 1)
        self.assertEqual(inv['C_pin_centered']['algebraic_jacobian_times_det_abs'], 2400)
        self.assertEqual(inv['C_pin_centered']['combined_skeleton_height_r_power'], 1)
        self.assertTrue(inv['C_axial']['no_unmatched_height_r_at_leading_order'])
        self.assertFalse(inv['C_axial']['combined_skeleton_applicable'])
        self.assertEqual(inv['C_axial']['unmatched_height_density_r_power'], 0)
        self.assertFalse(inv['any_combined_skeleton_absorbed_into_uniform_bound'])
        self.assertFalse(inv['global_contact_density_bound_proved'])
        self.assertFalse(inv['conditioned_expectation_evaluated'])

    def test_pin_site_unmatched_height_r_power_inventory(self):
        inv = m.pin_site_unmatched_height_r_power_inventory()
        self.assertEqual(inv['chart'], 'C_pin_centered')
        self.assertEqual(inv['enumeration_scope'], 'leading_morse_plus_cubic_through_tetratriacontic')
        self.assertEqual(len(inv['enumerated_order_names']), 32)
        self.assertEqual(inv['enumerated_order_names'][0], 'cubic')
        self.assertEqual(inv['enumerated_order_names'][-1], 'tetratriacontic')
        self.assertEqual(inv['unmatched_r_powers'], list(range(1, 33)))
        self.assertEqual(inv['orders']['cubic']['unmatched_density_r_power'], 1)
        self.assertEqual(inv['orders']['hexadecic']['unmatched_density_r_power'], 14)
        self.assertEqual(inv['orders']['heptadecic']['unmatched_density_r_power'], 15)
        self.assertEqual(inv['orders']['octadecic']['unmatched_density_r_power'], 16)
        self.assertEqual(inv['orders']['nonadecic']['unmatched_density_r_power'], 17)
        self.assertEqual(inv['orders']['icosic']['unmatched_density_r_power'], 18)
        self.assertEqual(inv['orders']['henicosic']['unmatched_density_r_power'], 19)
        self.assertEqual(inv['orders']['docosic']['unmatched_density_r_power'], 20)
        self.assertEqual(inv['orders']['tricosic']['unmatched_density_r_power'], 21)
        self.assertEqual(inv['orders']['tetracosic']['unmatched_density_r_power'], 22)
        self.assertEqual(inv['orders']['pentacosic']['unmatched_density_r_power'], 23)
        self.assertEqual(inv['orders']['hexacosic']['unmatched_density_r_power'], 24)
        self.assertEqual(inv['orders']['heptacosic']['unmatched_density_r_power'], 25)
        self.assertEqual(inv['orders']['octacosic']['unmatched_density_r_power'], 26)
        self.assertEqual(inv['orders']['nonacosic']['unmatched_density_r_power'], 27)
        self.assertEqual(inv['orders']['triacontic']['unmatched_density_r_power'], 28)
        self.assertEqual(inv['orders']['hentriacontic']['unmatched_density_r_power'], 29)
        self.assertEqual(inv['orders']['dotriacontic']['unmatched_density_r_power'], 30)
        self.assertEqual(inv['orders']['tritriacontic']['unmatched_density_r_power'], 31)
        self.assertEqual(inv['orders']['tetratriacontic']['unmatched_density_r_power'], 32)
        self.assertEqual(inv['orders']['heptadecic']['residual_symbol'], 'L_*_next')
        self.assertEqual(inv['orders']['octadecic']['residual_symbol'], 'M_*_next')
        self.assertEqual(inv['orders']['nonadecic']['residual_symbol'], 'O_*_next')
        self.assertEqual(inv['orders']['icosic']['residual_symbol'], 'R_*_next')
        self.assertEqual(inv['orders']['henicosic']['residual_symbol'], 'V_*_next')
        self.assertEqual(inv['orders']['docosic']['residual_symbol'], 'W_*_next')
        self.assertEqual(inv['orders']['tricosic']['residual_symbol'], 'X_*_next')
        self.assertEqual(inv['orders']['tetracosic']['residual_symbol'], 'Y_*_next')
        self.assertEqual(inv['orders']['pentacosic']['residual_symbol'], 'Z_*_next')
        self.assertEqual(inv['orders']['hexacosic']['residual_symbol'], 'A_*_next')
        self.assertEqual(inv['orders']['heptacosic']['residual_symbol'], 'B_*_next')
        self.assertEqual(inv['orders']['octacosic']['residual_symbol'], 'C_*_next')
        self.assertEqual(inv['orders']['nonacosic']['residual_symbol'], 'AA_*_next')
        self.assertEqual(inv['orders']['triacontic']['residual_symbol'], 'AB_*_next')
        self.assertEqual(inv['orders']['hentriacontic']['residual_symbol'], 'AC_*_next')
        self.assertEqual(inv['orders']['dotriacontic']['residual_symbol'], 'AD_*_next')
        self.assertEqual(inv['orders']['tritriacontic']['residual_symbol'], 'AE_*_next')
        self.assertEqual(inv['orders']['tetratriacontic']['residual_symbol'], 'AF_*_next')
        self.assertEqual(inv['orders']['hexadecic']['residual_symbol'], 'K_*_next')
        self.assertEqual(inv['min_unmatched_density_r_power'], 1)
        self.assertEqual(inv['max_unmatched_density_r_power'], 32)
        self.assertFalse(inv['any_height_r_absorbed_into_uniform_bound'])
        self.assertFalse(inv['pin_site_higher_jets_enumerated'])
        self.assertFalse(inv['thirty_fifth_and_higher_jets_enumerated'])
        self.assertFalse(inv['contact_gaussian_density_bounded'])
        self.assertFalse(inv['global_contact_density_bound_proved'])

    def test_thin_belt_contact_integrand_algebraic_factor_skeleton(self):
        # y=(2,1/8), f_yy=2,f_xxy=0: J_y=1/4, |det J|=1/1024, reciprocal=1024
        # α_k=48, det=48, product=49152
        t = m.thin_belt_contact_integrand_algebraic_factor_skeleton(
            m.point(2, Q(1, 8)), gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0)
        self.assertEqual(t['abs_det_grad_contact_map'], Q(1, 1024))
        self.assertEqual(t['reciprocal_grad_contact_jacobian'], 1024)
        self.assertEqual(t['alpha_k'], 48)
        self.assertEqual(t['alpha_f_xxy'], Q(1, 4))
        self.assertEqual(t['det_contact_leading_from_alphas'], 48)
        self.assertEqual(t['algebraic_jacobian_times_det_abs'], 49152)
        self.assertEqual(t['product_minus_factors'], 0)
        self.assertTrue(t['reciprocal_diverges_as_y2_to_0'])
        self.assertTrue(t['contact_integrand_algebraic_factor_skeleton_enumerated'])
        self.assertFalse(t['contact_gaussian_density_bounded'])
        self.assertFalse(t['uniform_integrand_bound_proved'])
        with self.assertRaises(ValueError):
            m.thin_belt_contact_integrand_algebraic_factor_skeleton(m.point(0, 2))
        with self.assertRaises(ValueError):
            m.thin_belt_contact_integrand_algebraic_factor_skeleton(m.point(2, 0))

    def test_transverse_algebraic_factor_times_height_r_skeleton(self):
        # y=(0,2): algebraic product=3, unmatched height r^1, combined r^1
        t = m.transverse_algebraic_factor_times_height_r_skeleton(
            m.point(0, 2), gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4, f_yyy=6)
        self.assertEqual(t['chart'], 'C_transverse')
        self.assertEqual(t['algebraic_jacobian_times_det_abs'], 3)
        self.assertEqual(t['unmatched_height_density_r_power'], 1)
        self.assertEqual(t['combined_skeleton_height_r_power'], 1)
        self.assertEqual(t['algebraic_factor_r_power_after_stripping'], 0)
        self.assertEqual(t['product_minus_recorded_factors'], 0)
        self.assertEqual(t['H_height_next_residual'], 8)
        self.assertEqual(t['free_residual_coordinates'], ['k', 'f_xxy'])
        self.assertTrue(t['combined_algebraic_factor_and_height_r_recorded'])
        self.assertFalse(t['height_r_absorbed_into_uniform_bound'])
        self.assertFalse(t['combined_skeleton_absorbed_into_uniform_bound'])
        self.assertFalse(t['contact_gaussian_density_bounded'])
        self.assertFalse(t['conditioned_expectation_evaluated'])
        self.assertFalse(t['global_contact_density_bound_proved'])
        off = m.transverse_algebraic_factor_times_height_r_skeleton(
            m.point(2, 2), gap_mark=1, f_yy=5, f_xxy=3, f_xyy=7)
        self.assertEqual(off['product_minus_recorded_factors'], 0)
        self.assertEqual(off['combined_skeleton_height_r_power'], 1)
        with self.assertRaises(ValueError):
            m.transverse_algebraic_factor_times_height_r_skeleton(m.point(2, 0))

    def test_thin_belt_algebraic_factor_times_height_r_skeleton(self):
        # y=(2,1/8): algebraic product=49152, unmatched height r^1
        t = m.thin_belt_algebraic_factor_times_height_r_skeleton(
            m.point(2, Q(1, 8)), gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0)
        self.assertEqual(t['chart'], 'C_thin_belt')
        self.assertEqual(t['algebraic_jacobian_times_det_abs'], 49152)
        self.assertEqual(t['unmatched_height_density_r_power'], 1)
        self.assertEqual(t['combined_skeleton_height_r_power'], 1)
        self.assertEqual(t['algebraic_factor_r_power_after_stripping'], 0)
        self.assertEqual(t['product_minus_recorded_factors'], 0)
        self.assertTrue(t['reciprocal_diverges_as_y2_to_0'])
        self.assertTrue(t['bare_reciprocal_L1_obstruction_cleared_by_cancel'])
        self.assertTrue(t['combined_algebraic_factor_and_height_r_recorded'])
        self.assertFalse(t['height_r_absorbed_into_uniform_bound'])
        self.assertFalse(t['combined_skeleton_absorbed_into_uniform_bound'])
        self.assertFalse(t['uniform_integrand_bound_proved'])
        self.assertFalse(t['contact_gaussian_density_bounded'])
        self.assertFalse(t['global_contact_density_bound_proved'])
        with self.assertRaises(ValueError):
            m.thin_belt_algebraic_factor_times_height_r_skeleton(m.point(0, 2))
        with self.assertRaises(ValueError):
            m.thin_belt_algebraic_factor_times_height_r_skeleton(m.point(2, 0))


if __name__ == '__main__':
    unittest.main()
