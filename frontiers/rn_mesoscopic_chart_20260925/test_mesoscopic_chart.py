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
            f_yyyyy=120)
        self.assertEqual(led['chart'], 'C_pin_centered')
        self.assertFalse(led['midpoint_U0_rows_applicable'])
        self.assertTrue(led['pin_site_jet_rows_enumerated'])
        self.assertTrue(led['pin_site_next_order_enumerated'])
        self.assertTrue(led['pin_site_quartic_enumerated'])
        self.assertTrue(led['pin_site_quintic_enumerated'])
        self.assertFalse(led['pin_site_higher_jets_enumerated'])
        self.assertTrue(led['contact_rows_enumerated'])
        self.assertEqual(led['enumeration_scope'], 'leading_morse_plus_cubic_quartic_quintic')
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
        self.assertFalse(led['quintic_rows']['sixth_and_higher_jets_enumerated'])
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
        self.assertFalse(rows['sixth_and_higher_jets_enumerated'])
        with self.assertRaises(ValueError):
            m.pin_site_morse_quintic_rows(
                0, 0, f_xxxxx=1, f_xxxxy=0, f_xxxyy=0, f_xxyyy=0, f_xyyyy=0, f_yyyyy=0)

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
        self.assertFalse(inv['charts']['C_thin_belt']['bare_1_over_abs_y2_L1'])
        self.assertTrue(inv['charts']['C_thin_belt']['jet_map_pointwise_cancel_recorded'])
        self.assertTrue(inv['charts']['C_thin_belt']['bare_reciprocal_L1_obstruction_cleared_by_cancel'])
        self.assertTrue(inv['charts']['C_thin_belt']['residual_geometric_factor_locally_L1'])
        self.assertFalse(inv['charts']['C_thin_belt']['uniform_integrand_bound_proved'])
        self.assertTrue(inv['charts']['C_pin_centered']['leading_morse_rows_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['cubic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['quartic_next_order_enumerated'])
        self.assertTrue(inv['charts']['C_pin_centered']['quintic_next_order_enumerated'])
        self.assertFalse(inv['charts']['C_pin_centered']['sixth_and_higher_jets_enumerated'])
        self.assertTrue(inv['charts']['C_transverse']['free_jet_residual_inventory_recorded'])
        self.assertTrue(inv['charts']['C_axial']['free_jet_residual_inventory_recorded'])
        self.assertTrue(inv['charts']['C_transverse']['conditioned_hessian_residual_polynomials_enumerated'])
        self.assertTrue(inv['charts']['C_axial']['conditioned_hessian_residual_polynomials_enumerated'])
        self.assertTrue(inv['charts']['C_transverse']['height_residual_after_grad_contact_enumerated'])
        self.assertFalse(inv['charts']['C_transverse']['hessian_conditioned_expectation_evaluated'])
        self.assertIn('contact_gaussian_density_factor', inv['open_blockers'])
        self.assertIn('thin_belt_contact_gaussian_density_near_y2_0', inv['open_blockers'])
        self.assertNotIn('thin_belt_uniform_integrand_after_cancel', inv['open_blockers'])
        self.assertIn('pin_sixth_and_higher_jets', inv['open_blockers'])
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
        with self.assertRaises(ValueError):
            m.transverse_free_jet_residual_inventory(m.point(2, 0))
        with self.assertRaises(ValueError):
            m.axial_free_jet_residual_inventory(m.point(0, 2))

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
        with self.assertRaises(ValueError):
            m.transverse_conditioned_hessian_residual_ledger(m.point(2, 0))
        with self.assertRaises(ValueError):
            m.axial_conditioned_hessian_residual_ledger(m.point(0, 2))

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


if __name__ == '__main__':
    unittest.main()
