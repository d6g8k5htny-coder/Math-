"""Exact d=2 transverse mesoscopic chart: contact rows and scaling powers.

Complements Math- PR7 (RN-MESOSCOPIC-ANNULUS-REDUCTION) without editing its body.
Scientific effect: NONE. Not a full-annulus RN certificate or 24-jet discharge.
"""
from __future__ import annotations

from fractions import Fraction as Q
from typing import Iterable
import json

Coord = tuple[Q, Q]


def exact(value: int | Q) -> Q:
    if type(value) is int or isinstance(value, Q):
        return Q(value)
    raise TypeError('an integer or Fraction is required; floats/bools are refused')


def point(y1: int | Q, y2: int | Q) -> Coord:
    return exact(y1), exact(y2)


def pin_sites() -> tuple[Coord, Coord]:
    """Scaled pin locations M=-e1/2 and S=+e1/2."""
    return (Q(-1, 2), Q(0)), (Q(1, 2), Q(0))


def away_from_pins(y: Coord, margin: int | Q = Q(1, 10)) -> bool:
    """True when y stays a fixed scaled distance from both pin sites."""
    m = exact(margin)
    if m <= 0:
        raise ValueError('positive margin required')
    for site in pin_sites():
        if (y[0] - site[0]) ** 2 + (y[1] - site[1]) ** 2 < m ** 2:
            return False
    return True


def in_annulus(y: Coord, inner: int | Q, outer: int | Q, *, require_pr7_A: bool = True) -> bool:
    a, b = exact(inner), exact(outer)
    if require_pr7_A:
        if not 1 < a < b:
            raise ValueError('require 1 < A < B for the PR7 mesoscopic annulus')
    elif not 0 < a < b:
        raise ValueError('require 0 < A < B')
    r2 = y[0] ** 2 + y[1] ** 2
    return a * a <= r2 <= b * b


def transverse_chart_ok(y: Coord, *, inner: int | Q = 2, outer: int | Q = 4,
                        margin: int | Q = Q(1, 10), floor_y2: int | Q = Q(1, 4)) -> bool:
    """Chart C_transverse: annulus, away from pins, |y2| bounded away from 0."""
    y1, y2 = y
    return (
        in_annulus(y, inner, outer)
        and away_from_pins(y, margin)
        and abs(y2) >= exact(floor_y2)
    )


def axial_chart_ok(y: Coord, *, inner: int | Q = 2, outer: int | Q = 4,
                   margin: int | Q = Q(1, 10)) -> bool:
    """Chart C_axial: y2=0, |y1| in the annulus, away from scaled pin sites ±1/2."""
    y1, y2 = y
    return (
        y2 == 0
        and in_annulus(y, inner, outer)
        and away_from_pins(y, margin)
    )


def thin_belt_ok(y: Coord, *, inner: int | Q = 2, outer: int | Q = 4,
                 margin: int | Q = Q(1, 10), floor_y2: int | Q = Q(1, 4)) -> bool:
    """Open belt 0<|y2|<floor between C_axial and C_transverse (off pins)."""
    y1, y2 = y
    return (
        in_annulus(y, inner, outer)
        and away_from_pins(y, margin)
        and Q(0) < abs(y2) < exact(floor_y2)
    )


def near_pin_ok(y: Coord, *, inner: int | Q = 2, outer: int | Q = 4,
                margin: int | Q = Q(1, 10), require_pr7_A: bool = True) -> bool:
    """Annulus ∩ pin-margin balls."""
    return (
        in_annulus(y, inner, outer, require_pr7_A=require_pr7_A)
        and not away_from_pins(y, margin)
    )


def pins_exterior_to_annulus(inner: int | Q = 2) -> bool:
    """True when both scaled pins have |pin| < A, hence lie outside the annulus."""
    return exact(inner) > Q(1, 2)


def pin_distance_squared(y: Coord, which: str = 'S') -> Q:
    sites = {'M': pin_sites()[0], 'S': pin_sites()[1]}
    if which not in sites:
        raise ValueError('which must be M or S')
    site = sites[which]
    return (y[0] - site[0]) ** 2 + (y[1] - site[1]) ** 2


def classify_annulus_point(y: Coord, *, inner: int | Q = 2, outer: int | Q = 4,
                           margin: int | Q = Q(1, 10),
                           floor_y2: int | Q = Q(1, 4),
                           require_pr7_A: bool = True) -> str:
    """Partition label for a point relative to the declared charts.

    Returns one of: outside_annulus, near_pin, C_axial, C_transverse, thin_belt_open.
    """
    if not in_annulus(y, inner, outer, require_pr7_A=require_pr7_A):
        return 'outside_annulus'
    if not away_from_pins(y, margin):
        return 'near_pin'
    if y[1] == 0:
        return 'C_axial'
    if abs(y[1]) >= exact(floor_y2):
        return 'C_transverse'
    if Q(0) < abs(y[1]) < exact(floor_y2):
        return 'thin_belt_open'
    return 'unclassified'


def chart_cover_report(*, inner: int | Q = 2, outer: int | Q = 4,
                       margin: int | Q = Q(1, 10),
                       floor_y2: int | Q = Q(1, 4)) -> dict:
    """Machine inventory of which annulus regions have enumerated contact rows."""
    a = exact(inner)
    pins_out = pins_exterior_to_annulus(a)
    open_regions = ['thin_belt_open']
    if not pins_out:
        open_regions.append('near_pin')
    return {
        'object': 'RN-MESOSCOPIC-CHART-COVER-20260925-v1',
        'annulus': {'A': a, 'B': exact(outer)},
        'pin_exclusion_margin': exact(margin),
        'transverse_floor_y2': exact(floor_y2),
        'pins_exterior_to_annulus': pins_out,
        'enumerated_charts': ['C_transverse', 'C_axial'],
        'thin_belt_contact_rows_enumerated': True,
        'thin_belt_uniform_bound_proved': False,
        'open_regions': open_regions,
        'cover_complete': False,
        'notes': (
            'C_transverse ∪ C_axial covers the annulus off the open thin belt '
            '0<|y2|<floor. Thin-belt contact polynomials are enumerated but not '
            'absorbed (conditioning ~1/|y2|). For A>1/2 the scaled pins lie outside '
            'the annulus (PR7 convention); near-pin charts arise only for smaller A '
            'or other scales.'
        ),
        'legacy_24jet_discharged': False,
        'full_annulus_closed': False,
    }


def thin_belt_conditioning(y: Coord) -> dict[str, Q | str]:
    """Record why the thin belt is not absorbed into C_transverse.

    Formally the C_transverse polynomials extend, but J_grad_y = f_yy y2 has coefficient
    y2→0, so the change-of-variables / Schur conditioning deteriorates as 1/|y2|.
    """
    if not thin_belt_ok(y):
        raise ValueError('point outside thin belt')
    y2 = exact(y[1])
    return {
        'region': 'thin_belt_open',
        'grad_y_coefficient_y2': y2,
        'conditioning_factor_reciprocal_abs_y2': 1 / abs(y2),
        'status': 'OPEN_SEPARATE_CHART_REQUIRED',
    }


def thin_belt_reciprocal_shell_lower_bound(shells: int, floor_y2: int | Q = Q(1, 4)) -> dict:
    """Exact dyadic lower bound showing ∫ 1/|y2| dy2 diverges as y2→0.

    On each shell [δ/2^k, δ/2^{k-1}], 1/y ≥ 2^k/δ and width = δ/2^k, so the shell
    contributes at least 1 to the integral. After n shells the truncated integral is
    at least n, hence unbounded as n→∞. This blocks absorbing the bare conditioning
    factor into a uniform L^1 bound without additional cancellation.
    """
    if type(shells) is not int or shells < 1:
        raise ValueError('positive shell count required')
    delta = exact(floor_y2)
    if delta <= 0:
        raise ValueError('positive floor required')
    # Innermost left endpoint after n shells: δ/2^n
    eps = delta / (2 ** shells)
    return {
        'object': 'RN-MESOSCOPIC-THIN-BELT-RECIPROCAL-SHELL-20260925-v1',
        'floor_y2': delta,
        'shells': shells,
        'eps': eps,
        'integral_lower_bound': shells,
        'bare_conditioning_factor_L1_near_zero': False,
        'uniform_integrand_bound_proved': False,
        'additional_cancellation_required': True,
        'status': 'OPEN_SEPARATE_CHART_REQUIRED',
        'meaning': (
            'dyadic shells each contribute >=1 to ∫ dy2/|y2|; bare 1/|y2| is not '
            'locally L1 at y2=0; not a full Kac-Rice density bound'
        ),
    }


def jet_map_f_yy_to_J_grad_y_factor(y: Coord) -> dict[str, Q | str | bool]:
    """Exact jet-space factor ∂J_grad_y/∂f_yy = y2 on transverse/thin contact rows.

    Records a possible cancellation partner for the 1/|y2| conditioning factor.
    Does not prove that the full conditioned density remains bounded.
    """
    y2 = exact(y[1])
    if y2 == 0:
        raise ValueError('factor vanishes on the axis; use C_axial instead')
    return {
        'object': 'RN-MESOSCOPIC-JET-MAP-FYY-JGRADY-20260925-v1',
        'partial_J_grad_y_partial_f_yy': y2,
        'abs_factor': abs(y2),
        'conditioning_reciprocal_abs_y2': 1 / abs(y2),
        'product_abs_factor_times_reciprocal': Q(1),
        'cancels_bare_reciprocal_pointwise': True,
        'full_density_bound_proved': False,
        'meaning': (
            'pointwise |y2|*(1/|y2|)=1 on the contact jet map; '
            'not a proof that the conditioned Gaussian density is uniformly bounded'
        ),
    }


def thin_belt_integrand_residual_after_cancel(
    y: Coord, *, shells: int = 8, floor_y2: int | Q = Q(1, 4),
) -> dict:
    """Record the thin-belt integrand residual after jet-map cancel of 1/|y2|.

    Pointwise, ∂J_grad_y/∂f_yy = y2 cancels the bare conditioning reciprocal:
      |y2| · (1/|y2|) = 1.
    The residual geometric change-of-variables factor is therefore identically 1,
    which is locally L1 on dyadic shells (each shell contributes its width, not ≥1).
    This clears the bare reciprocal L1 obstruction; the contact Gaussian density
    near y2→0 remains unbound, so the uniform integrand bound stays open.
    """
    if not thin_belt_ok(y, floor_y2=floor_y2):
        raise ValueError('point outside thin belt')
    if type(shells) is not int or shells < 1:
        raise ValueError('positive shell count required')
    delta = exact(floor_y2)
    jet = jet_map_f_yy_to_J_grad_y_factor(y)
    bare = thin_belt_conditioning(y)
    # Residual geometric factor is 1; dyadic shell widths sum to δ(1 - 2^{-n}).
    width_sum = delta * (1 - Q(1, 2 ** shells))
    return {
        'object': 'RN-MESOSCOPIC-THIN-BELT-INTEGRAND-RESIDUAL-AFTER-CANCEL-20260925-v1',
        'chart': 'C_thin_belt',
        'y': {'y1': exact(y[0]), 'y2': exact(y[1])},
        'floor_y2': delta,
        'shells': shells,
        'bare_conditioning_reciprocal': bare['conditioning_factor_reciprocal_abs_y2'],
        'jet_map_abs_factor': jet['abs_factor'],
        'product_abs_factor_times_reciprocal': jet['product_abs_factor_times_reciprocal'],
        'cancels_bare_reciprocal_pointwise': True,
        'residual_geometric_factor_after_cancel': Q(1),
        'residual_geometric_factor_locally_L1': True,
        'dyadic_shell_width_sum': width_sum,
        'bare_reciprocal_L1_obstruction_cleared_by_cancel': True,
        'uniform_integrand_bound_proved': False,
        'contact_gaussian_density_bounded': False,
        'full_density_bound_proved': False,
        'meaning': (
            'jet-map cancel clears bare 1/|y2| L1 obstruction (residual geometric '
            'factor = 1); contact Gaussian density near y2=0 remains unbound'
        ),
    }


def thin_belt_contact_integrand_algebraic_factor_skeleton(
    y: Coord, *, gap_mark: int | Q = 1,
    f_yy: int | Q = 1, f_xxy: int | Q = 0, f_xyy: int | Q = 0, f_yyy: int | Q = 0,
    floor_y2: int | Q = Q(1, 4),
) -> dict:
    """Exact algebraic Jacobian×|det H| factor product on C_thin_belt (density open).

    Same algebraic identities as C_transverse (shared jet polynomials):
      |det ∂(J_y,J_x)/∂(f_yy,f_xyy)| = |y2|^3 / 2
      det_contact_leading = α_k·k + α_f_xxy·f_xxy
        with α_k = 12 y1 J_grad_y / y2, α_f_xxy = J_grad_y
    As y2→0 the reciprocal Jacobian 2/|y2|^3 diverges, recording the open
    thin-belt contact Gaussian density obstruction near y2=0. Jet-map cancel
    of bare 1/|y2| is already recorded separately; this ledger does not bound
    the density.
    """
    if not thin_belt_ok(y, floor_y2=floor_y2):
        raise ValueError('point outside thin belt')
    y1, y2 = exact(y[0]), exact(y[1])
    k = exact(gap_mark)
    a, b, c, d = map(exact, (f_yy, f_xxy, f_xyy, f_yyy))
    if k <= 0:
        raise ValueError('positive gap mark required')
    rows = thin_belt_contact_rows(
        y, gap_mark=k, f_yy=a, f_xxy=b, f_xyy=c, f_yyy=d,
    )
    jy = rows['J_grad_y']
    abs_y2 = abs(y2)
    abs_det_jac = (abs_y2 ** 3) / 2
    reciprocal_jac = 1 / abs_det_jac
    alpha_k = (12 * y1 * jy) / y2
    alpha_f = jy
    det_from_alphas = alpha_k * k + alpha_f * b
    abs_det_h = abs(det_from_alphas)
    algebraic_product = reciprocal_jac * abs_det_h
    return {
        'object': 'RN-MESOSCOPIC-THIN-BELT-CONTACT-INTEGRAND-ALGEBRAIC-FACTOR-20260925-v1',
        'chart': 'C_thin_belt',
        'y': {'y1': y1, 'y2': y2},
        'floor_y2': exact(floor_y2),
        'abs_det_grad_contact_map': abs_det_jac,
        'reciprocal_grad_contact_jacobian': reciprocal_jac,
        'alpha_k': alpha_k,
        'alpha_f_xxy': alpha_f,
        'det_contact_leading_from_alphas': det_from_alphas,
        'det_contact_leading_abs': abs_det_h,
        'algebraic_jacobian_times_det_abs': algebraic_product,
        'product_minus_factors': algebraic_product - reciprocal_jac * abs_det_h,
        'reciprocal_diverges_as_y2_to_0': True,
        'free_residual_coordinates': ['k', 'f_xxy'],
        'bare_reciprocal_L1_obstruction_cleared_by_cancel': True,
        'contact_integrand_algebraic_factor_skeleton_enumerated': True,
        'uniform_integrand_bound_proved': False,
        'contact_gaussian_density_bounded': False,
        'global_contact_density_bound_proved': False,
        'meaning': (
            'exact thin-belt product (1/|det J_grad|)·|det H_skeleton|; '
            'reciprocal diverges as y2→0; Gaussian density near y2=0 still unbound'
        ),
    }


def transverse_conditioning_uniform_bound(
    y: Coord, *, floor_y2: int | Q = Q(1, 4),
) -> dict[str, Q | str | bool]:
    """On C_transverse, |y2|≥δ ⇒ 1/|y2| ≤ 1/δ uniformly on the chart.

    Clears the bare chart-conditioning singularity on C_transverse (the thin belt
    still carries the 1/|y2| obstruction). Does not bound the contact Gaussian
    density factor needed for γ_AB ≤ C r^(-d).
    """
    delta = exact(floor_y2)
    if delta <= 0:
        raise ValueError('positive floor required')
    if not transverse_chart_ok(y, floor_y2=delta):
        raise ValueError('point outside C_transverse chart')
    y2 = exact(y[1])
    reciprocal = 1 / abs(y2)
    uniform = 1 / delta
    return {
        'object': 'RN-MESOSCOPIC-TRANSVERSE-CONDITIONING-BOUND-20260925-v1',
        'chart': 'C_transverse',
        'floor_y2': delta,
        'abs_y2': abs(y2),
        'conditioning_reciprocal_abs_y2': reciprocal,
        'uniform_chart_bound': uniform,
        'reciprocal_le_uniform_bound': reciprocal <= uniform,
        'chart_conditioning_singularity_cleared': True,
        'gaussian_density_factor_bounded': False,
        'thin_belt_still_open': True,
        'meaning': (
            'exact |y2|>=δ ⇒ 1/|y2| <= 1/δ on C_transverse; '
            'chart singularity cleared, contact Gaussian density still unbound'
        ),
    }


def axial_conditioning_uniform_bound(
    y: Coord, *, inner: int | Q = 2, outer: int | Q = 4,
) -> dict[str, Q | str | bool]:
    """On C_axial, |y1|≥A ⇒ 2/y1^2 ≤ 2/A^2 for the J_grad_y = (y1^2/2) f_xxy coefficient.

    Clears bare chart-conditioning singularity on the axis away from pins.
    Area measure zero in the 2D annulus integral; Gaussian density still open.
    """
    a = exact(inner)
    if a <= 0:
        raise ValueError('positive inner radius required')
    if not axial_chart_ok(y, inner=inner, outer=outer):
        raise ValueError('point outside C_axial chart')
    y1 = exact(y[0])
    coeff = (y1 * y1) / 2
    reciprocal = 1 / coeff
    uniform = 2 / (a * a)
    return {
        'object': 'RN-MESOSCOPIC-AXIAL-CONDITIONING-BOUND-20260925-v1',
        'chart': 'C_axial',
        'annulus_A': a,
        'abs_y1': abs(y1),
        'grad_y_coefficient_y1_sq_over_2': coeff,
        'conditioning_reciprocal': reciprocal,
        'uniform_chart_bound': uniform,
        'reciprocal_le_uniform_bound': reciprocal <= uniform,
        'axial_chart_conditioning_singularity_cleared': True,
        'axial_gaussian_density_factor_bounded': False,
        'axial_area_measure_zero': True,
        'meaning': (
            'exact |y1|>=A ⇒ 2/y1^2 <= 2/A^2 on C_axial; '
            'chart singularity cleared, contact Gaussian density still unbound'
        ),
    }


def chart_boundary_transition(
    y: Coord, *, floor_y2: int | Q = Q(1, 4),
    gap_mark: int | Q = 1, f_yy: int | Q = 1,
    f_xxy: int | Q = 0, f_xyy: int | Q = 0, f_yyy: int | Q = 0,
) -> dict:
    """Overlap transition on |y2|=floor between C_transverse and C_thin_belt.

    Both charts use the same contact-jet polynomials, so the transition on
    (J_grad_y, J_grad_x, J_height, H_height_next) is the identity (det=1).
    """
    delta = exact(floor_y2)
    if abs(exact(y[1])) != delta:
        raise ValueError('boundary sample requires |y2| equal to transverse floor')
    if not in_annulus(y, 2, 4):
        raise ValueError('boundary sample must lie in the PR7 annulus')
    if not away_from_pins(y):
        raise ValueError('boundary sample must stay away from pins')
    # Evaluate shared polynomials without chart membership (boundary is in neither open set).
    rows = _contact_jet_polynomials(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    return {
        'object': 'RN-MESOSCOPIC-CHART-BOUNDARY-TRANSITION-20260925-v1',
        'from_chart': 'C_thin_belt',
        'to_chart': 'C_transverse',
        'boundary': '|y2|=floor_y2',
        'floor_y2': delta,
        'y': {'y1': rows['y1'], 'y2': rows['y2']},
        'shared_contact_rows': {
            'J_grad_y': rows['J_grad_y'],
            'J_grad_x': rows['J_grad_x'],
            'J_height': rows['J_height'],
            'H_height_next': rows['H_height_next'],
        },
        'transition_on_contact_rows': 'identity',
        'transition_jacobian_determinant': Q(1),
        'singular_transition': False,
        'full_annulus_closed': False,
        'uniform_integrand_bound_proved': False,
        'meaning': (
            'exact identity transition of shared contact jets across |y2|=δ; '
            'does not bound the density or close the thin-belt interior'
        ),
    }


def thin_belt_contact_rows(y: Coord, *, gap_mark: int | Q,
                           f_yy: int | Q, f_xxy: int | Q, f_xyy: int | Q,
                           f_yyy: int | Q = 0) -> dict[str, Q]:
    """Contact polynomials on the thin belt (same jet forms as C_transverse).

    Membership uses thin_belt_ok. The polynomials extend, but the chart is not absorbed
    into C_transverse because |y2| is below the transverse floor.
    """
    if not thin_belt_ok(y):
        raise ValueError('point outside thin belt')
    return _contact_jet_polynomials(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )


def thin_belt_ledger_for_point(y: Coord, gap_mark: int | Q = 1,
                               f_yy: int | Q = 1, f_xxy: int | Q = 0,
                               f_xyy: int | Q = 0, f_yyy: int | Q = 0) -> dict:
    rows = thin_belt_contact_rows(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    cond = thin_belt_conditioning(y)
    # Same gradient scaling powers as C_transverse; density may blow as 1/|y2|.
    grad = SCALING_EXPONENTS['grad_x'] + SCALING_EXPONENTS['grad_y']
    return {
        'object': 'RN-MESOSCOPIC-CHART-J0-D2-THIN-BELT-20260925-v1',
        'chart': 'C_thin_belt',
        'y': {'y1': rows['y1'], 'y2': rows['y2']},
        'contact_rows': {
            'J_grad_y': rows['J_grad_y'],
            'J_grad_x': rows['J_grad_x'],
            'J_height': rows['J_height'],
            'H_height_next': rows['H_height_next'],
            'height_residual_at_leading_order': rows['height_residual_at_leading_order'],
        },
        'conditioning': cond,
        'gradient_jacobian_r_power': grad,
        'hessian_det_leading_r_power': HESSIAN_SCALING_EXPONENTS['xx'],
        'contact_rows_enumerated': True,
        'uniform_integrand_bound_proved': False,
        'absorbed_into_C_transverse': False,
        'hessian_ledger_evaluated': False,
        'full_annulus_closed': False,
        'legacy_24jet_discharged': False,
        'complements_pr7': True,
        'status': 'OPEN_SEPARATE_CHART_REQUIRED',
        'meaning': (
            'exact thin-belt contact polynomials matching C_transverse forms; '
            'conditioning factor 1/|y2| prevents absorption; no uniform density bound'
        ),
    }


def near_pin_diagnosis(y: Coord, *, inner: int | Q = Q(2, 5), outer: int | Q = 1,
                       margin: int | Q = Q(1, 10)) -> dict[str, Q | str | bool]:
    """Diagnose a pin-neighbourhood point on a small-A annulus where pins can lie inside.

    This is a separate regime from the PR7 fixed annulus with A>1; it records that a
    pin-centered divided-difference chart is required and does not claim that chart.
    """
    if pins_exterior_to_annulus(inner):
        raise ValueError('near-pin diagnosis requires A <= 1/2 so pins can enter the annulus')
    if not near_pin_ok(y, inner=inner, outer=outer, margin=margin, require_pr7_A=False):
        raise ValueError('point not in a near-pin ball inside the small-A annulus')
    d2_m = pin_distance_squared(y, 'M')
    d2_s = pin_distance_squared(y, 'S')
    closer = 'M' if d2_m <= d2_s else 'S'
    return {
        'region': 'near_pin',
        'annulus_A': exact(inner),
        'annulus_B': exact(outer),
        'closer_pin': closer,
        'dist2_M': d2_m,
        'dist2_S': d2_s,
        'midpoint_chart_valid': False,
        'requires_pin_centered_divided_differences': True,
        'status': 'OPEN_SEPARATE_CHART_REQUIRED',
        'pr7_fixed_annulus_A_gt_1': False,
        'notes': (
            'Witness approaches a pin site; expand relative to that pin, not the midpoint U_0 chart'
        ),
    }


def pin_centered_frame(y: Coord, *, inner: int | Q = Q(2, 5), outer: int | Q = 1,
                       margin: int | Q = Q(1, 10)) -> dict:
    """Local coordinates relative to the closer scaled pin on a small-A near-pin chart."""
    diag = near_pin_diagnosis(y, inner=inner, outer=outer, margin=margin)
    closer = str(diag['closer_pin'])
    site = pin_sites()[0] if closer == 'M' else pin_sites()[1]
    z1 = exact(y[0]) - site[0]
    z2 = exact(y[1]) - site[1]
    return {
        'chart': 'C_pin_centered',
        'closer_pin': closer,
        'pin_site': {'y1': site[0], 'y2': site[1]},
        'z1': z1,
        'z2': z2,
        'dist2_to_closer_pin': z1 * z1 + z2 * z2,
        'annulus_A': exact(inner),
        'annulus_B': exact(outer),
    }


def pin_centered_ledger_for_point(y: Coord, *, inner: int | Q = Q(2, 5), outer: int | Q = 1,
                                  margin: int | Q = Q(1, 10),
                                  H_xx: int | Q = -1, H_xy: int | Q = 0, H_yy: int | Q = 1,
                                  f_xxx: int | Q = 0, f_xxy: int | Q = 0,
                                  f_xyy: int | Q = 0, f_yyy: int | Q = 0,
                                  f_xxxx: int | Q = 0, f_xxxy: int | Q = 0,
                                  f_xxyy: int | Q = 0, f_xyyy: int | Q = 0,
                                  f_yyyy: int | Q = 0,
                                  f_xxxxx: int | Q = 0, f_xxxxy: int | Q = 0,
                                  f_xxxyy: int | Q = 0, f_xxyyy: int | Q = 0,
                                  f_xyyyy: int | Q = 0, f_yyyyy: int | Q = 0,
                                  f_xxxxxx: int | Q = 0, f_xxxxxy: int | Q = 0,
                                  f_xxxxyy: int | Q = 0, f_xxxyyy: int | Q = 0,
                                  f_xxyyyy: int | Q = 0, f_xyyyyy: int | Q = 0,
                                  f_yyyyyy: int | Q = 0,
                                  f_xxxxxxx: int | Q = 0, f_xxxxxxy: int | Q = 0,
                                  f_xxxxxyy: int | Q = 0, f_xxxxyyy: int | Q = 0,
                                  f_xxxyyyy: int | Q = 0, f_xxyyyyy: int | Q = 0,
                                  f_xyyyyyy: int | Q = 0, f_yyyyyyy: int | Q = 0,
                                  f_xxxxxxxx: int | Q = 0, f_xxxxxxxy: int | Q = 0,
                                  f_xxxxxxyy: int | Q = 0, f_xxxxxyyy: int | Q = 0,
                                  f_xxxxyyyy: int | Q = 0, f_xxxyyyyy: int | Q = 0,
                                  f_xxyyyyyy: int | Q = 0, f_xyyyyyyy: int | Q = 0,
                                  f_yyyyyyyy: int | Q = 0,
                                  f_xxxxxxxxx: int | Q = 0, f_xxxxxxxxy: int | Q = 0,
                                  f_xxxxxxxyy: int | Q = 0, f_xxxxxxyyy: int | Q = 0,
                                  f_xxxxxyyyy: int | Q = 0, f_xxxxyyyyy: int | Q = 0,
                                  f_xxxyyyyyy: int | Q = 0, f_xxyyyyyyy: int | Q = 0,
                                  f_xyyyyyyyy: int | Q = 0, f_yyyyyyyyy: int | Q = 0,
                                  f_xxxxxxxxxx: int | Q = 0, f_xxxxxxxxxy: int | Q = 0,
                                  f_xxxxxxxxyy: int | Q = 0, f_xxxxxxxyyy: int | Q = 0,
                                  f_xxxxxxyyyy: int | Q = 0, f_xxxxxyyyyy: int | Q = 0,
                                  f_xxxxyyyyyy: int | Q = 0, f_xxxyyyyyyy: int | Q = 0,
                                  f_xxyyyyyyyy: int | Q = 0, f_xyyyyyyyyy: int | Q = 0,
                                  f_yyyyyyyyyy: int | Q = 0,
                                  f_xxxxxxxxxxx: int | Q = 0, f_xxxxxxxxxxy: int | Q = 0,
                                  f_xxxxxxxxxyy: int | Q = 0, f_xxxxxxxxyyy: int | Q = 0,
                                  f_xxxxxxxyyyy: int | Q = 0, f_xxxxxxyyyyy: int | Q = 0,
                                  f_xxxxxyyyyyy: int | Q = 0, f_xxxxyyyyyyy: int | Q = 0,
                                  f_xxxyyyyyyyy: int | Q = 0, f_xxyyyyyyyyy: int | Q = 0,
                                  f_xyyyyyyyyyy: int | Q = 0, f_yyyyyyyyyyy: int | Q = 0,
                                  f_xxxxxxxxxxxx: int | Q = 0, f_xxxxxxxxxxxy: int | Q = 0,
                                  f_xxxxxxxxxxyy: int | Q = 0, f_xxxxxxxxxyyy: int | Q = 0,
                                  f_xxxxxxxxyyyy: int | Q = 0, f_xxxxxxxyyyyy: int | Q = 0,
                                  f_xxxxxxyyyyyy: int | Q = 0, f_xxxxxyyyyyyy: int | Q = 0,
                                  f_xxxxyyyyyyyy: int | Q = 0, f_xxxyyyyyyyyy: int | Q = 0,
                                  f_xxyyyyyyyyyy: int | Q = 0, f_xyyyyyyyyyyy: int | Q = 0,
                                  f_yyyyyyyyyyyy: int | Q = 0,
                                  f_xxxxxxxxxxxxx: int | Q = 0, f_xxxxxxxxxxxxy: int | Q = 0,
                                  f_xxxxxxxxxxxyy: int | Q = 0, f_xxxxxxxxxxyyy: int | Q = 0,
                                  f_xxxxxxxxxyyyy: int | Q = 0, f_xxxxxxxxyyyyy: int | Q = 0,
                                  f_xxxxxxxyyyyyy: int | Q = 0, f_xxxxxxyyyyyyy: int | Q = 0,
                                  f_xxxxxyyyyyyyy: int | Q = 0, f_xxxxyyyyyyyyy: int | Q = 0,
                                  f_xxxyyyyyyyyyy: int | Q = 0, f_xxyyyyyyyyyyy: int | Q = 0,
                                  f_xyyyyyyyyyyyy: int | Q = 0, f_yyyyyyyyyyyyy: int | Q = 0,
                                  f_xxxxxxxxxxxxxx: int | Q = 0, f_xxxxxxxxxxxxxy: int | Q = 0,
                                  f_xxxxxxxxxxxxyy: int | Q = 0, f_xxxxxxxxxxxyyy: int | Q = 0,
                                  f_xxxxxxxxxxyyyy: int | Q = 0, f_xxxxxxxxxyyyyy: int | Q = 0,
                                  f_xxxxxxxxyyyyyy: int | Q = 0, f_xxxxxxxyyyyyyy: int | Q = 0,
                                  f_xxxxxxyyyyyyyy: int | Q = 0, f_xxxxxyyyyyyyyy: int | Q = 0,
                                  f_xxxxyyyyyyyyyy: int | Q = 0, f_xxxyyyyyyyyyyy: int | Q = 0,
                                  f_xxyyyyyyyyyyyy: int | Q = 0, f_xyyyyyyyyyyyyy: int | Q = 0,
                                  f_yyyyyyyyyyyyyy: int | Q = 0,
                                  f_xxxxxxxxxxxxxxx: int | Q = 0, f_xxxxxxxxxxxxxxy: int | Q = 0,
                                  f_xxxxxxxxxxxxxyy: int | Q = 0, f_xxxxxxxxxxxxyyy: int | Q = 0,
                                  f_xxxxxxxxxxxyyyy: int | Q = 0, f_xxxxxxxxxxyyyyy: int | Q = 0,
                                  f_xxxxxxxxxyyyyyy: int | Q = 0, f_xxxxxxxxyyyyyyy: int | Q = 0,
                                  f_xxxxxxxyyyyyyyy: int | Q = 0, f_xxxxxxyyyyyyyyy: int | Q = 0,
                                  f_xxxxxyyyyyyyyyy: int | Q = 0, f_xxxxyyyyyyyyyyy: int | Q = 0,
                                  f_xxxyyyyyyyyyyyy: int | Q = 0, f_xxyyyyyyyyyyyyy: int | Q = 0,
                                  f_xyyyyyyyyyyyyyy: int | Q = 0, f_yyyyyyyyyyyyyyy: int | Q = 0,
                                  f_xxxxxxxxxxxxxxxx: int | Q = 0, f_xxxxxxxxxxxxxxxy: int | Q = 0,
                                  f_xxxxxxxxxxxxxxyy: int | Q = 0, f_xxxxxxxxxxxxxyyy: int | Q = 0,
                                  f_xxxxxxxxxxxxyyyy: int | Q = 0, f_xxxxxxxxxxxyyyyy: int | Q = 0,
                                  f_xxxxxxxxxxyyyyyy: int | Q = 0, f_xxxxxxxxxyyyyyyy: int | Q = 0,
                                  f_xxxxxxxxyyyyyyyy: int | Q = 0, f_xxxxxxxyyyyyyyyy: int | Q = 0,
                                  f_xxxxxxyyyyyyyyyy: int | Q = 0, f_xxxxxyyyyyyyyyyy: int | Q = 0,
                                  f_xxxxyyyyyyyyyyyy: int | Q = 0, f_xxxyyyyyyyyyyyyy: int | Q = 0,
                                  f_xxyyyyyyyyyyyyyy: int | Q = 0, f_xyyyyyyyyyyyyyyy: int | Q = 0,
                                  f_yyyyyyyyyyyyyyyy: int | Q = 0) -> dict:
    """Pin-centred ledger with Morse through hexadecic contact residuals."""
    frame = pin_centered_frame(y, inner=inner, outer=outer, margin=margin)
    rows = pin_site_morse_contact_rows(
        frame['z1'], frame['z2'], H_xx=H_xx, H_xy=H_xy, H_yy=H_yy,
    )
    nxt = pin_site_morse_next_order_rows(
        frame['z1'], frame['z2'],
        f_xxx=f_xxx, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    quart = pin_site_morse_quartic_rows(
        frame['z1'], frame['z2'],
        f_xxxx=f_xxxx, f_xxxy=f_xxxy, f_xxyy=f_xxyy, f_xyyy=f_xyyy, f_yyyy=f_yyyy,
    )
    quint = pin_site_morse_quintic_rows(
        frame['z1'], frame['z2'],
        f_xxxxx=f_xxxxx, f_xxxxy=f_xxxxy, f_xxxyy=f_xxxyy,
        f_xxyyy=f_xxyyy, f_xyyyy=f_xyyyy, f_yyyyy=f_yyyyy,
    )
    sext = pin_site_morse_sextic_rows(
        frame['z1'], frame['z2'],
        f_xxxxxx=f_xxxxxx, f_xxxxxy=f_xxxxxy, f_xxxxyy=f_xxxxyy,
        f_xxxyyy=f_xxxyyy, f_xxyyyy=f_xxyyyy, f_xyyyyy=f_xyyyyy,
        f_yyyyyy=f_yyyyyy,
    )
    sept = pin_site_morse_septic_rows(
        frame['z1'], frame['z2'],
        f_xxxxxxx=f_xxxxxxx, f_xxxxxxy=f_xxxxxxy, f_xxxxxyy=f_xxxxxyy,
        f_xxxxyyy=f_xxxxyyy, f_xxxyyyy=f_xxxyyyy, f_xxyyyyy=f_xxyyyyy,
        f_xyyyyyy=f_xyyyyyy, f_yyyyyyy=f_yyyyyyy,
    )
    octi = pin_site_morse_octic_rows(
        frame['z1'], frame['z2'],
        f_xxxxxxxx=f_xxxxxxxx, f_xxxxxxxy=f_xxxxxxxy, f_xxxxxxyy=f_xxxxxxyy,
        f_xxxxxyyy=f_xxxxxyyy, f_xxxxyyyy=f_xxxxyyyy, f_xxxyyyyy=f_xxxyyyyy,
        f_xxyyyyyy=f_xxyyyyyy, f_xyyyyyyy=f_xyyyyyyy, f_yyyyyyyy=f_yyyyyyyy,
    )
    noni = pin_site_morse_nonic_rows(
        frame['z1'], frame['z2'],
        f_xxxxxxxxx=f_xxxxxxxxx, f_xxxxxxxxy=f_xxxxxxxxy, f_xxxxxxxyy=f_xxxxxxxyy,
        f_xxxxxxyyy=f_xxxxxxyyy, f_xxxxxyyyy=f_xxxxxyyyy, f_xxxxyyyyy=f_xxxxyyyyy,
        f_xxxyyyyyy=f_xxxyyyyyy, f_xxyyyyyyy=f_xxyyyyyyy, f_xyyyyyyyy=f_xyyyyyyyy,
        f_yyyyyyyyy=f_yyyyyyyyy,
    )
    deci = pin_site_morse_decic_rows(
        frame['z1'], frame['z2'],
        f_xxxxxxxxxx=f_xxxxxxxxxx, f_xxxxxxxxxy=f_xxxxxxxxxy, f_xxxxxxxxyy=f_xxxxxxxxyy,
        f_xxxxxxxyyy=f_xxxxxxxyyy, f_xxxxxxyyyy=f_xxxxxxyyyy, f_xxxxxyyyyy=f_xxxxxyyyyy,
        f_xxxxyyyyyy=f_xxxxyyyyyy, f_xxxyyyyyyy=f_xxxyyyyyyy, f_xxyyyyyyyy=f_xxyyyyyyyy,
        f_xyyyyyyyyy=f_xyyyyyyyyy, f_yyyyyyyyyy=f_yyyyyyyyyy,
    )
    unde = pin_site_morse_undecic_rows(
        frame['z1'], frame['z2'],
        f_xxxxxxxxxxx=f_xxxxxxxxxxx, f_xxxxxxxxxxy=f_xxxxxxxxxxy, f_xxxxxxxxxyy=f_xxxxxxxxxyy,
        f_xxxxxxxxyyy=f_xxxxxxxxyyy, f_xxxxxxxyyyy=f_xxxxxxxyyyy, f_xxxxxxyyyyy=f_xxxxxxyyyyy,
        f_xxxxxyyyyyy=f_xxxxxyyyyyy, f_xxxxyyyyyyy=f_xxxxyyyyyyy, f_xxxyyyyyyyy=f_xxxyyyyyyyy,
        f_xxyyyyyyyyy=f_xxyyyyyyyyy, f_xyyyyyyyyyy=f_xyyyyyyyyyy, f_yyyyyyyyyyy=f_yyyyyyyyyyy,
    )
    dode = pin_site_morse_dodecic_rows(
        frame['z1'], frame['z2'],
        f_xxxxxxxxxxxx=f_xxxxxxxxxxxx, f_xxxxxxxxxxxy=f_xxxxxxxxxxxy, f_xxxxxxxxxxyy=f_xxxxxxxxxxyy,
        f_xxxxxxxxxyyy=f_xxxxxxxxxyyy, f_xxxxxxxxyyyy=f_xxxxxxxxyyyy, f_xxxxxxxyyyyy=f_xxxxxxxyyyyy,
        f_xxxxxxyyyyyy=f_xxxxxxyyyyyy, f_xxxxxyyyyyyy=f_xxxxxyyyyyyy, f_xxxxyyyyyyyy=f_xxxxyyyyyyyy,
        f_xxxyyyyyyyyy=f_xxxyyyyyyyyy, f_xxyyyyyyyyyy=f_xxyyyyyyyyyy, f_xyyyyyyyyyyy=f_xyyyyyyyyyyy,
        f_yyyyyyyyyyyy=f_yyyyyyyyyyyy,
    )
    tride = pin_site_morse_tridecic_rows(
        frame['z1'], frame['z2'],
        f_xxxxxxxxxxxxx=f_xxxxxxxxxxxxx, f_xxxxxxxxxxxxy=f_xxxxxxxxxxxxy, f_xxxxxxxxxxxyy=f_xxxxxxxxxxxyy,
        f_xxxxxxxxxxyyy=f_xxxxxxxxxxyyy, f_xxxxxxxxxyyyy=f_xxxxxxxxxyyyy, f_xxxxxxxxyyyyy=f_xxxxxxxxyyyyy,
        f_xxxxxxxyyyyyy=f_xxxxxxxyyyyyy, f_xxxxxxyyyyyyy=f_xxxxxxyyyyyyy, f_xxxxxyyyyyyyy=f_xxxxxyyyyyyyy,
        f_xxxxyyyyyyyyy=f_xxxxyyyyyyyyy, f_xxxyyyyyyyyyy=f_xxxyyyyyyyyyy, f_xxyyyyyyyyyyy=f_xxyyyyyyyyyyy,
        f_xyyyyyyyyyyyy=f_xyyyyyyyyyyyy, f_yyyyyyyyyyyyy=f_yyyyyyyyyyyyy,
    )
    tetra = pin_site_morse_tetradecic_rows(
        frame['z1'], frame['z2'],
        f_xxxxxxxxxxxxxx=f_xxxxxxxxxxxxxx, f_xxxxxxxxxxxxxy=f_xxxxxxxxxxxxxy, f_xxxxxxxxxxxxyy=f_xxxxxxxxxxxxyy,
        f_xxxxxxxxxxxyyy=f_xxxxxxxxxxxyyy, f_xxxxxxxxxxyyyy=f_xxxxxxxxxxyyyy, f_xxxxxxxxxyyyyy=f_xxxxxxxxxyyyyy,
        f_xxxxxxxxyyyyyy=f_xxxxxxxxyyyyyy, f_xxxxxxxyyyyyyy=f_xxxxxxxyyyyyyy, f_xxxxxxyyyyyyyy=f_xxxxxxyyyyyyyy,
        f_xxxxxyyyyyyyyy=f_xxxxxyyyyyyyyy, f_xxxxyyyyyyyyyy=f_xxxxyyyyyyyyyy, f_xxxyyyyyyyyyyy=f_xxxyyyyyyyyyyy,
        f_xxyyyyyyyyyyyy=f_xxyyyyyyyyyyyy, f_xyyyyyyyyyyyyy=f_xyyyyyyyyyyyyy, f_yyyyyyyyyyyyyy=f_yyyyyyyyyyyyyy,
    )
    penta = pin_site_morse_pentadecic_rows(
        frame['z1'], frame['z2'],
        f_xxxxxxxxxxxxxxx=f_xxxxxxxxxxxxxxx, f_xxxxxxxxxxxxxxy=f_xxxxxxxxxxxxxxy, f_xxxxxxxxxxxxxyy=f_xxxxxxxxxxxxxyy,
        f_xxxxxxxxxxxxyyy=f_xxxxxxxxxxxxyyy, f_xxxxxxxxxxxyyyy=f_xxxxxxxxxxxyyyy, f_xxxxxxxxxxyyyyy=f_xxxxxxxxxxyyyyy,
        f_xxxxxxxxxyyyyyy=f_xxxxxxxxxyyyyyy, f_xxxxxxxxyyyyyyy=f_xxxxxxxxyyyyyyy, f_xxxxxxxyyyyyyyy=f_xxxxxxxyyyyyyyy,
        f_xxxxxxyyyyyyyyy=f_xxxxxxyyyyyyyyy, f_xxxxxyyyyyyyyyy=f_xxxxxyyyyyyyyyy, f_xxxxyyyyyyyyyyy=f_xxxxyyyyyyyyyyy,
        f_xxxyyyyyyyyyyyy=f_xxxyyyyyyyyyyyy, f_xxyyyyyyyyyyyyy=f_xxyyyyyyyyyyyyy, f_xyyyyyyyyyyyyyy=f_xyyyyyyyyyyyyyy,
        f_yyyyyyyyyyyyyyy=f_yyyyyyyyyyyyyyy,
    )
    hexa = pin_site_morse_hexadecic_rows(
        frame['z1'], frame['z2'],
        f_xxxxxxxxxxxxxxxx=f_xxxxxxxxxxxxxxxx, f_xxxxxxxxxxxxxxxy=f_xxxxxxxxxxxxxxxy, f_xxxxxxxxxxxxxxyy=f_xxxxxxxxxxxxxxyy,
        f_xxxxxxxxxxxxxyyy=f_xxxxxxxxxxxxxyyy, f_xxxxxxxxxxxxyyyy=f_xxxxxxxxxxxxyyyy, f_xxxxxxxxxxxyyyyy=f_xxxxxxxxxxxyyyyy,
        f_xxxxxxxxxxyyyyyy=f_xxxxxxxxxxyyyyyy, f_xxxxxxxxxyyyyyyy=f_xxxxxxxxxyyyyyyy, f_xxxxxxxxyyyyyyyy=f_xxxxxxxxyyyyyyyy,
        f_xxxxxxxyyyyyyyyy=f_xxxxxxxyyyyyyyyy, f_xxxxxxyyyyyyyyyy=f_xxxxxxyyyyyyyyyy, f_xxxxxyyyyyyyyyyy=f_xxxxxyyyyyyyyyyy,
        f_xxxxyyyyyyyyyyyy=f_xxxxyyyyyyyyyyyy, f_xxxyyyyyyyyyyyyy=f_xxxyyyyyyyyyyyyy, f_xxyyyyyyyyyyyyyy=f_xxyyyyyyyyyyyyyy,
        f_xyyyyyyyyyyyyyyy=f_xyyyyyyyyyyyyyyy, f_yyyyyyyyyyyyyyyy=f_yyyyyyyyyyyyyyyy,
    )
    signature = pin_morse_hessian_signature(
        H_xx=H_xx, H_xy=H_xy, H_yy=H_yy, closer_pin=str(frame['closer_pin']),
    )
    return {
        'object': 'RN-MESOSCOPIC-CHART-PIN-CENTERED-D2-20260925-v1',
        'chart': 'C_pin_centered',
        'frame': frame,
        'midpoint_U0_rows_applicable': False,
        'contact_rows': rows,
        'next_order_rows': nxt,
        'quartic_rows': quart,
        'quintic_rows': quint,
        'sextic_rows': sext,
        'septic_rows': sept,
        'octic_rows': octi,
        'nonic_rows': noni,
        'decic_rows': deci,
        'undecic_rows': unde,
        'dodecic_rows': dode,
        'tridecic_rows': tride,
        'tetradecic_rows': tetra,
        'pentadecic_rows': penta,
        'hexadecic_rows': hexa,
        'hessian_signature': signature,
        'scaling': {
            'grad': PIN_CENTERED_SCALING_EXPONENTS['grad'],
            'height': PIN_CENTERED_SCALING_EXPONENTS['height'],
            'gradient_jacobian_r_power': 2 * PIN_CENTERED_SCALING_EXPONENTS['grad'],
        },
        'pin_site_jet_rows_enumerated': True,
        'pin_site_next_order_enumerated': True,
        'pin_site_quartic_enumerated': True,
        'pin_site_quintic_enumerated': True,
        'pin_site_sextic_enumerated': True,
        'pin_site_septic_enumerated': True,
        'pin_site_octic_enumerated': True,
        'pin_site_nonic_enumerated': True,
        'pin_site_decic_enumerated': True,
        'pin_site_undecic_enumerated': True,
        'pin_site_dodecic_enumerated': True,
        'pin_site_tridecic_enumerated': True,
        'pin_site_tetradecic_enumerated': True,
        'pin_site_pentadecic_enumerated': True,
        'pin_site_hexadecic_enumerated': True,
        'pin_site_higher_jets_enumerated': False,
        'contact_rows_enumerated': True,
        'enumeration_scope': 'leading_morse_plus_cubic_through_hexadecic',
        'hessian_ledger_evaluated': False,
        'uniform_integrand_bound_proved': False,
        'full_annulus_closed': False,
        'legacy_24jet_discharged': False,
        'pr7_fixed_annulus_A_gt_1': False,
        'complements_pr7': True,
        'status': 'OPEN_HIGHER_JETS_AND_DENSITY',
        'meaning': (
            'leading Morse pin-site rows J=H z plus cubic through hexadecic '
            'H/Q/P/S/T/U/N/D/E/F/G/I/J/K_*_next; seventeenth-and-higher jets and Gaussian density remain open'
        ),
    }


def pin_site_morse_contact_rows(
    z1: int | Q, z2: int | Q, *,
    H_xx: int | Q, H_xy: int | Q, H_yy: int | Q,
) -> dict[str, Q | bool]:
    """Leading Morse contact residuals after pin constraints, in pin-local z.

    About a Morse pin with grad f(pin)=0:
      grad f(pin + r z) = r H_pin z + O(r^2)     => divide by r^1
      f(pin + r z) - f(pin) = (r^2/2) z·H_pin·z + O(r^3)  => divide by r^2
    Hence
      J_grad = H_pin z,   J_height = (1/2) z·H_pin·z,
    and J_height = (1/2) z · J_grad at this order.
    """
    a, b, c = map(exact, (H_xx, H_xy, H_yy))
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('Morse contact rows require z != 0 (witness off the pin site)')
    j1 = a * u + b * v
    j2 = b * u + c * v
    jh = (a * u * u + 2 * b * u * v + c * v * v) / 2
    return {
        'J_grad_1': j1,
        'J_grad_2': j2,
        'J_height': jh,
        'height_minus_half_z_dot_grad': jh - (u * j1 + v * j2) / 2,
        'height_dependent_on_grad_at_leading_order': True,
        'z1': u,
        'z2': v,
        'H_xx': a,
        'H_xy': b,
        'H_yy': c,
    }


def pin_site_morse_next_order_rows(
    z1: int | Q, z2: int | Q, *,
    f_xxx: int | Q, f_xxy: int | Q, f_xyy: int | Q, f_yyy: int | Q,
) -> dict[str, Q | bool]:
    """Next-order (cubic) pin-local contact residuals after Morse leading terms.

    With third derivatives at the pin:
      grad f(pin+rz) = r H z + (r^2/2) D³f(z,z) + O(r^3)
      f(pin+rz)-f(pin) = (r^2/2) z·H·z + (r^3/6) D³f(z,z,z) + O(r^4)
    so after stripping leading powers the unmatched r^1 corrections are
      H_grad_next = (1/2) D³f(z,z),   H_height_next = (1/6) D³f(z,z,z),
    with the exact identity z·H_grad_next = 3 H_height_next.
    """
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('next-order pin rows require z != 0')
    a, b, c, d = map(exact, (f_xxx, f_xxy, f_xyy, f_yyy))
    # (1/2) D³f(z,z) components
    g1 = (a * u * u + 2 * b * u * v + c * v * v) / 2
    g2 = (b * u * u + 2 * c * u * v + d * v * v) / 2
    # (1/6) D³f(z,z,z)
    h = (a * u ** 3 + 3 * b * u * u * v + 3 * c * u * v * v + d * v ** 3) / 6
    return {
        'H_grad_next_1': g1,
        'H_grad_next_2': g2,
        'H_height_next': h,
        'z_dot_H_grad_next_minus_3_H_height_next': u * g1 + v * g2 - 3 * h,
        'explicit_r_factor_still_required': True,
        'z1': u,
        'z2': v,
        'f_xxx': a,
        'f_xxy': b,
        'f_xyy': c,
        'f_yyy': d,
    }


def pin_site_morse_quartic_rows(
    z1: int | Q, z2: int | Q, *,
    f_xxxx: int | Q, f_xxxy: int | Q, f_xxyy: int | Q,
    f_xyyy: int | Q, f_yyyy: int | Q,
) -> dict[str, Q | bool | int]:
    """Quartic (fourth-order) pin-local contact residuals after cubic next-order.

    With fourth derivatives at the pin:
      grad f(pin+rz) = r H z + (r^2/2) D³f(z,z) + (r^3/6) D⁴f(z,z,z) + O(r^4)
      f(pin+rz)-f(pin) = (r^2/2) z·H·z + (r^3/6) D³f(z,z,z)
                         + (r^4/24) D⁴f(z,z,z,z) + O(r^5)
    so after stripping leading powers the unmatched r^2 corrections are
      Q_grad_next = (1/6) D⁴f(z,z,z),   Q_height_next = (1/24) D⁴f(z,z,z,z),
    with the exact identity z·Q_grad_next = 4 Q_height_next.
    Quintic-and-higher jets are enumerated separately.
    """
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('quartic pin rows require z != 0')
    a, b, c, d, e = map(exact, (f_xxxx, f_xxxy, f_xxyy, f_xyyy, f_yyyy))
    # (1/6) D⁴f(z,z,z) components
    g1 = (a * u ** 3 + 3 * b * u * u * v + 3 * c * u * v * v + d * v ** 3) / 6
    g2 = (b * u ** 3 + 3 * c * u * u * v + 3 * d * u * v * v + e * v ** 3) / 6
    # (1/24) D⁴f(z,z,z,z)
    h = (
        a * u ** 4 + 4 * b * u ** 3 * v + 6 * c * u * u * v * v
        + 4 * d * u * v ** 3 + e * v ** 4
    ) / 24
    return {
        'Q_grad_next_1': g1,
        'Q_grad_next_2': g2,
        'Q_height_next': h,
        'z_dot_Q_grad_next_minus_4_Q_height_next': u * g1 + v * g2 - 4 * h,
        'unmatched_density_r_power': 2,
        'explicit_r_factor_still_required': True,
        'z1': u,
        'z2': v,
        'f_xxxx': a,
        'f_xxxy': b,
        'f_xxyy': c,
        'f_xyyy': d,
        'f_yyyy': e,
    }


def pin_site_morse_quintic_rows(
    z1: int | Q, z2: int | Q, *,
    f_xxxxx: int | Q, f_xxxxy: int | Q, f_xxxyy: int | Q,
    f_xxyyy: int | Q, f_xyyyy: int | Q, f_yyyyy: int | Q,
) -> dict[str, Q | bool | int]:
    """Quintic (fifth-order) pin-local contact residuals after quartic next-order.

    With fifth derivatives at the pin:
      grad f(pin+rz) = … + (r^4/24) D⁵f(z,z,z,z) + O(r^5)
      f(pin+rz)-f(pin) = … + (r^5/120) D⁵f(z,z,z,z,z) + O(r^6)
    so after stripping leading powers the unmatched r^3 corrections are
      P_grad_next = (1/24) D⁵f(z,z,z,z),
      P_height_next = (1/120) D⁵f(z,z,z,z,z),
    with the exact identity z·P_grad_next = 5 P_height_next.
    Sextic jets are enumerated separately.
    """
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('quintic pin rows require z != 0')
    a, b, c, d, e, f = map(
        exact, (f_xxxxx, f_xxxxy, f_xxxyy, f_xxyyy, f_xyyyy, f_yyyyy),
    )
    # (1/24) D⁵f(z,z,z,z) components
    g1 = (
        a * u ** 4 + 4 * b * u ** 3 * v + 6 * c * u * u * v * v
        + 4 * d * u * v ** 3 + e * v ** 4
    ) / 24
    g2 = (
        b * u ** 4 + 4 * c * u ** 3 * v + 6 * d * u * u * v * v
        + 4 * e * u * v ** 3 + f * v ** 4
    ) / 24
    # (1/120) D⁵f(z,z,z,z,z)
    h = (
        a * u ** 5 + 5 * b * u ** 4 * v + 10 * c * u ** 3 * v * v
        + 10 * d * u * u * v ** 3 + 5 * e * u * v ** 4 + f * v ** 5
    ) / 120
    return {
        'P_grad_next_1': g1,
        'P_grad_next_2': g2,
        'P_height_next': h,
        'z_dot_P_grad_next_minus_5_P_height_next': u * g1 + v * g2 - 5 * h,
        'unmatched_density_r_power': 3,
        'explicit_r_factor_still_required': True,
        'z1': u,
        'z2': v,
        'f_xxxxx': a,
        'f_xxxxy': b,
        'f_xxxyy': c,
        'f_xxyyy': d,
        'f_xyyyy': e,
        'f_yyyyy': f,
    }


def pin_site_morse_sextic_rows(
    z1: int | Q, z2: int | Q, *,
    f_xxxxxx: int | Q, f_xxxxxy: int | Q, f_xxxxyy: int | Q,
    f_xxxyyy: int | Q, f_xxyyyy: int | Q, f_xyyyyy: int | Q,
    f_yyyyyy: int | Q,
) -> dict[str, Q | bool | int]:
    """Sextic (sixth-order) pin-local contact residuals after quintic next-order.

    With sixth derivatives at the pin:
      grad f(pin+rz) = … + (r^5/120) D⁶f(z,z,z,z,z) + O(r^6)
      f(pin+rz)-f(pin) = … + (r^6/720) D⁶f(z,z,z,z,z,z) + O(r^7)
    so after stripping leading powers the unmatched r^4 corrections are
      S_grad_next = (1/120) D⁶f(z,z,z,z,z),
      S_height_next = (1/720) D⁶f(z,z,z,z,z,z),
    with the exact identity z·S_grad_next = 6 S_height_next.
    Septic jets are enumerated separately.
    """
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('sextic pin rows require z != 0')
    a, b, c, d, e, f, g = map(
        exact,
        (f_xxxxxx, f_xxxxxy, f_xxxxyy, f_xxxyyy, f_xxyyyy, f_xyyyyy, f_yyyyyy),
    )
    # (1/120) D⁶f(z,z,z,z,z) components
    g1 = (
        a * u ** 5 + 5 * b * u ** 4 * v + 10 * c * u ** 3 * v * v
        + 10 * d * u * u * v ** 3 + 5 * e * u * v ** 4 + f * v ** 5
    ) / 120
    g2 = (
        b * u ** 5 + 5 * c * u ** 4 * v + 10 * d * u ** 3 * v * v
        + 10 * e * u * u * v ** 3 + 5 * f * u * v ** 4 + g * v ** 5
    ) / 120
    # (1/720) D⁶f(z,z,z,z,z,z)
    h = (
        a * u ** 6 + 6 * b * u ** 5 * v + 15 * c * u ** 4 * v * v
        + 20 * d * u ** 3 * v ** 3 + 15 * e * u * u * v ** 4
        + 6 * f * u * v ** 5 + g * v ** 6
    ) / 720
    return {
        'S_grad_next_1': g1,
        'S_grad_next_2': g2,
        'S_height_next': h,
        'z_dot_S_grad_next_minus_6_S_height_next': u * g1 + v * g2 - 6 * h,
        'unmatched_density_r_power': 4,
        'explicit_r_factor_still_required': True,
        'z1': u,
        'z2': v,
        'f_xxxxxx': a,
        'f_xxxxxy': b,
        'f_xxxxyy': c,
        'f_xxxyyy': d,
        'f_xxyyyy': e,
        'f_xyyyyy': f,
        'f_yyyyyy': g,
    }


def pin_site_morse_septic_rows(
    z1: int | Q, z2: int | Q, *,
    f_xxxxxxx: int | Q, f_xxxxxxy: int | Q, f_xxxxxyy: int | Q,
    f_xxxxyyy: int | Q, f_xxxyyyy: int | Q, f_xxyyyyy: int | Q,
    f_xyyyyyy: int | Q, f_yyyyyyy: int | Q,
) -> dict[str, Q | bool | int]:
    """Septic (seventh-order) pin-local contact residuals after sextic next-order.

    With seventh derivatives at the pin:
      grad f(pin+rz) = … + (r^6/720) D⁷f(z,z,z,z,z,z) + O(r^7)
      f(pin+rz)-f(pin) = … + (r^7/5040) D⁷f(z,z,z,z,z,z,z) + O(r^8)
    so after stripping leading powers the unmatched r^5 corrections are
      T_grad_next = (1/720) D⁷f(z,z,z,z,z,z),
      T_height_next = (1/5040) D⁷f(z,z,z,z,z,z,z),
    with the exact identity z·T_grad_next = 7 T_height_next.
    """
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('septic pin rows require z != 0')
    a, b, c, d, e, f, g, hh = map(
        exact,
        (
            f_xxxxxxx, f_xxxxxxy, f_xxxxxyy, f_xxxxyyy,
            f_xxxyyyy, f_xxyyyyy, f_xyyyyyy, f_yyyyyyy,
        ),
    )
    # (1/720) D⁷f(z,z,z,z,z,z) components
    g1 = (
        a * u ** 6 + 6 * b * u ** 5 * v + 15 * c * u ** 4 * v * v
        + 20 * d * u ** 3 * v ** 3 + 15 * e * u * u * v ** 4
        + 6 * f * u * v ** 5 + g * v ** 6
    ) / 720
    g2 = (
        b * u ** 6 + 6 * c * u ** 5 * v + 15 * d * u ** 4 * v * v
        + 20 * e * u ** 3 * v ** 3 + 15 * f * u * u * v ** 4
        + 6 * g * u * v ** 5 + hh * v ** 6
    ) / 720
    # (1/5040) D⁷f(z,z,z,z,z,z,z)
    ht = (
        a * u ** 7 + 7 * b * u ** 6 * v + 21 * c * u ** 5 * v * v
        + 35 * d * u ** 4 * v ** 3 + 35 * e * u ** 3 * v ** 4
        + 21 * f * u * u * v ** 5 + 7 * g * u * v ** 6 + hh * v ** 7
    ) / 5040
    return {
        'T_grad_next_1': g1,
        'T_grad_next_2': g2,
        'T_height_next': ht,
        'z_dot_T_grad_next_minus_7_T_height_next': u * g1 + v * g2 - 7 * ht,
        'unmatched_density_r_power': 5,
        'explicit_r_factor_still_required': True,
        'z1': u,
        'z2': v,
        'f_xxxxxxx': a,
        'f_xxxxxxy': b,
        'f_xxxxxyy': c,
        'f_xxxxyyy': d,
        'f_xxxyyyy': e,
        'f_xxyyyyy': f,
        'f_xyyyyyy': g,
        'f_yyyyyyy': hh,
    }


def pin_site_morse_octic_rows(
    z1: int | Q, z2: int | Q, *,
    f_xxxxxxxx: int | Q, f_xxxxxxxy: int | Q, f_xxxxxxyy: int | Q,
    f_xxxxxyyy: int | Q, f_xxxxyyyy: int | Q, f_xxxyyyyy: int | Q,
    f_xxyyyyyy: int | Q, f_xyyyyyyy: int | Q, f_yyyyyyyy: int | Q,
) -> dict[str, Q | bool | int]:
    """Octic (eighth-order) pin-local contact residuals after septic next-order.

    With eighth derivatives at the pin:
      grad f(pin+rz) = … + (r^7/5040) D⁸f(z,z,z,z,z,z,z) + O(r^8)
      f(pin+rz)-f(pin) = … + (r^8/40320) D⁸f(z,z,z,z,z,z,z,z) + O(r^9)
    so after stripping leading powers the unmatched r^6 corrections are
      U_grad_next = (1/5040) D⁸f(z,z,z,z,z,z,z),
      U_height_next = (1/40320) D⁸f(z,z,z,z,z,z,z,z),
    with the exact identity z·U_grad_next = 8 U_height_next.
    """
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('octic pin rows require z != 0')
    a, b, c, d, e, f, g, h, ii = map(
        exact,
        (
            f_xxxxxxxx, f_xxxxxxxy, f_xxxxxxyy, f_xxxxxyyy,
            f_xxxxyyyy, f_xxxyyyyy, f_xxyyyyyy, f_xyyyyyyy, f_yyyyyyyy,
        ),
    )
    # (1/5040) D⁸f(z,z,z,z,z,z,z) components
    g1 = (
        a * u ** 7 + 7 * b * u ** 6 * v + 21 * c * u ** 5 * v * v
        + 35 * d * u ** 4 * v ** 3 + 35 * e * u ** 3 * v ** 4
        + 21 * f * u * u * v ** 5 + 7 * g * u * v ** 6 + h * v ** 7
    ) / 5040
    g2 = (
        b * u ** 7 + 7 * c * u ** 6 * v + 21 * d * u ** 5 * v * v
        + 35 * e * u ** 4 * v ** 3 + 35 * f * u ** 3 * v ** 4
        + 21 * g * u * u * v ** 5 + 7 * h * u * v ** 6 + ii * v ** 7
    ) / 5040
    # (1/40320) D⁸f(z,z,z,z,z,z,z,z)
    ht = (
        a * u ** 8 + 8 * b * u ** 7 * v + 28 * c * u ** 6 * v * v
        + 56 * d * u ** 5 * v ** 3 + 70 * e * u ** 4 * v ** 4
        + 56 * f * u ** 3 * v ** 5 + 28 * g * u * u * v ** 6
        + 8 * h * u * v ** 7 + ii * v ** 8
    ) / 40320
    return {
        'U_grad_next_1': g1,
        'U_grad_next_2': g2,
        'U_height_next': ht,
        'z_dot_U_grad_next_minus_8_U_height_next': u * g1 + v * g2 - 8 * ht,
        'unmatched_density_r_power': 6,
        'explicit_r_factor_still_required': True,
        'z1': u,
        'z2': v,
        'f_xxxxxxxx': a,
        'f_xxxxxxxy': b,
        'f_xxxxxxyy': c,
        'f_xxxxxyyy': d,
        'f_xxxxyyyy': e,
        'f_xxxyyyyy': f,
        'f_xxyyyyyy': g,
        'f_xyyyyyyy': h,
        'f_yyyyyyyy': ii,
    }


def pin_site_morse_nonic_rows(
    z1: int | Q, z2: int | Q, *,
    f_xxxxxxxxx: int | Q, f_xxxxxxxxy: int | Q, f_xxxxxxxyy: int | Q,
    f_xxxxxxyyy: int | Q, f_xxxxxyyyy: int | Q, f_xxxxyyyyy: int | Q,
    f_xxxyyyyyy: int | Q, f_xxyyyyyyy: int | Q, f_xyyyyyyyy: int | Q,
    f_yyyyyyyyy: int | Q,
) -> dict[str, Q | bool | int]:
    """Nonic (ninth-order) pin-local contact residuals after octic next-order.

    With ninth derivatives at the pin:
      grad f(pin+rz) = … + (r^8/40320) D⁹f(z,z,z,z,z,z,z,z) + O(r^9)
      f(pin+rz)-f(pin) = … + (r^9/362880) D⁹f(z,z,z,z,z,z,z,z,z) + O(r^10)
    so after stripping leading powers the unmatched r^7 corrections are
      N_grad_next = (1/40320) D⁹f(z,z,z,z,z,z,z,z),
      N_height_next = (1/362880) D⁹f(z,z,z,z,z,z,z,z,z),
    with the exact identity z·N_grad_next = 9 N_height_next.
    """
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('nonic pin rows require z != 0')
    a, b, c, d, e, f, g, h, ii, jj = map(
        exact,
        (
            f_xxxxxxxxx, f_xxxxxxxxy, f_xxxxxxxyy, f_xxxxxxyyy,
            f_xxxxxyyyy, f_xxxxyyyyy, f_xxxyyyyyy, f_xxyyyyyyy,
            f_xyyyyyyyy, f_yyyyyyyyy,
        ),
    )
    # (1/40320) D⁹f(z^8) components
    g1 = (
        a * u ** 8 + 8 * b * u ** 7 * v + 28 * c * u ** 6 * v * v
        + 56 * d * u ** 5 * v ** 3 + 70 * e * u ** 4 * v ** 4
        + 56 * f * u ** 3 * v ** 5 + 28 * g * u * u * v ** 6
        + 8 * h * u * v ** 7 + ii * v ** 8
    ) / 40320
    g2 = (
        b * u ** 8 + 8 * c * u ** 7 * v + 28 * d * u ** 6 * v * v
        + 56 * e * u ** 5 * v ** 3 + 70 * f * u ** 4 * v ** 4
        + 56 * g * u ** 3 * v ** 5 + 28 * h * u * u * v ** 6
        + 8 * ii * u * v ** 7 + jj * v ** 8
    ) / 40320
    # (1/362880) D⁹f(z^9)
    ht = (
        a * u ** 9 + 9 * b * u ** 8 * v + 36 * c * u ** 7 * v * v
        + 84 * d * u ** 6 * v ** 3 + 126 * e * u ** 5 * v ** 4
        + 126 * f * u ** 4 * v ** 5 + 84 * g * u ** 3 * v ** 6
        + 36 * h * u * u * v ** 7 + 9 * ii * u * v ** 8 + jj * v ** 9
    ) / 362880
    return {
        'N_grad_next_1': g1,
        'N_grad_next_2': g2,
        'N_height_next': ht,
        'z_dot_N_grad_next_minus_9_N_height_next': u * g1 + v * g2 - 9 * ht,
        'unmatched_density_r_power': 7,
        'explicit_r_factor_still_required': True,
        'z1': u,
        'z2': v,
        'f_xxxxxxxxx': a,
        'f_xxxxxxxxy': b,
        'f_xxxxxxxyy': c,
        'f_xxxxxxyyy': d,
        'f_xxxxxyyyy': e,
        'f_xxxxyyyyy': f,
        'f_xxxyyyyyy': g,
        'f_xxyyyyyyy': h,
        'f_xyyyyyyyy': ii,
        'f_yyyyyyyyy': jj,
    }


def pin_site_morse_decic_rows(
    z1: int | Q, z2: int | Q, *,
    f_xxxxxxxxxx: int | Q, f_xxxxxxxxxy: int | Q, f_xxxxxxxxyy: int | Q,
    f_xxxxxxxyyy: int | Q, f_xxxxxxyyyy: int | Q, f_xxxxxyyyyy: int | Q,
    f_xxxxyyyyyy: int | Q, f_xxxyyyyyyy: int | Q, f_xxyyyyyyyy: int | Q,
    f_xyyyyyyyyy: int | Q, f_yyyyyyyyyy: int | Q,
) -> dict[str, Q | bool | int]:
    """Decic (tenth-order) pin-local contact residuals after nonic next-order.

    With tenth derivatives at the pin:
      grad f(pin+rz) = … + (r^9/362880) D¹⁰f(z^9) + O(r^10)
      f(pin+rz)-f(pin) = … + (r^10/3628800) D¹⁰f(z^10) + O(r^11)
    so after stripping leading powers the unmatched r^8 corrections are
      D_grad_next = (1/362880) D¹⁰f(z^9),
      D_height_next = (1/3628800) D¹⁰f(z^10),
    with the exact identity z·D_grad_next = 10 D_height_next.
    """
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('decic pin rows require z != 0')
    a, b, c, d, e, f, g, h, ii, jj, kk = map(
        exact,
        (
            f_xxxxxxxxxx, f_xxxxxxxxxy, f_xxxxxxxxyy, f_xxxxxxxyyy,
            f_xxxxxxyyyy, f_xxxxxyyyyy, f_xxxxyyyyyy, f_xxxyyyyyyy,
            f_xxyyyyyyyy, f_xyyyyyyyyy, f_yyyyyyyyyy,
        ),
    )
    # (1/362880) D¹⁰f(z^9) components
    g1 = (
        a * u ** 9 + 9 * b * u ** 8 * v + 36 * c * u ** 7 * v * v
        + 84 * d * u ** 6 * v ** 3 + 126 * e * u ** 5 * v ** 4
        + 126 * f * u ** 4 * v ** 5 + 84 * g * u ** 3 * v ** 6
        + 36 * h * u * u * v ** 7 + 9 * ii * u * v ** 8 + jj * v ** 9
    ) / 362880
    g2 = (
        b * u ** 9 + 9 * c * u ** 8 * v + 36 * d * u ** 7 * v * v
        + 84 * e * u ** 6 * v ** 3 + 126 * f * u ** 5 * v ** 4
        + 126 * g * u ** 4 * v ** 5 + 84 * h * u ** 3 * v ** 6
        + 36 * ii * u * u * v ** 7 + 9 * jj * u * v ** 8 + kk * v ** 9
    ) / 362880
    # (1/3628800) D¹⁰f(z^10)
    ht = (
        a * u ** 10 + 10 * b * u ** 9 * v + 45 * c * u ** 8 * v * v
        + 120 * d * u ** 7 * v ** 3 + 210 * e * u ** 6 * v ** 4
        + 252 * f * u ** 5 * v ** 5 + 210 * g * u ** 4 * v ** 6
        + 120 * h * u ** 3 * v ** 7 + 45 * ii * u * u * v ** 8
        + 10 * jj * u * v ** 9 + kk * v ** 10
    ) / 3628800
    return {
        'D_grad_next_1': g1,
        'D_grad_next_2': g2,
        'D_height_next': ht,
        'z_dot_D_grad_next_minus_10_D_height_next': u * g1 + v * g2 - 10 * ht,
        'unmatched_density_r_power': 8,
        'explicit_r_factor_still_required': True,
        'z1': u,
        'z2': v,
        'f_xxxxxxxxxx': a,
        'f_xxxxxxxxxy': b,
        'f_xxxxxxxxyy': c,
        'f_xxxxxxxyyy': d,
        'f_xxxxxxyyyy': e,
        'f_xxxxxyyyyy': f,
        'f_xxxxyyyyyy': g,
        'f_xxxyyyyyyy': h,
        'f_xxyyyyyyyy': ii,
        'f_xyyyyyyyyy': jj,
        'f_yyyyyyyyyy': kk,
    }


def pin_site_morse_undecic_rows(
    z1: int | Q, z2: int | Q, *,
    f_xxxxxxxxxxx: int | Q, f_xxxxxxxxxxy: int | Q, f_xxxxxxxxxyy: int | Q,
    f_xxxxxxxxyyy: int | Q, f_xxxxxxxyyyy: int | Q, f_xxxxxxyyyyy: int | Q,
    f_xxxxxyyyyyy: int | Q, f_xxxxyyyyyyy: int | Q, f_xxxyyyyyyyy: int | Q,
    f_xxyyyyyyyyy: int | Q, f_xyyyyyyyyyy: int | Q, f_yyyyyyyyyyy: int | Q,
) -> dict[str, Q | bool | int]:
    """Undecic (eleventh-order) pin-local contact residuals after decic next-order.

    With eleventh derivatives at the pin:
      grad f(pin+rz) = … + (r^10/3628800) D¹¹f(z^10) + O(r^11)
      f(pin+rz)-f(pin) = … + (r^11/39916800) D¹¹f(z^11) + O(r^12)
    so after stripping leading powers the unmatched r^9 corrections are
      E_grad_next = (1/3628800) D¹¹f(z^10),
      E_height_next = (1/39916800) D¹¹f(z^11),
    with the exact identity z·E_grad_next = 11 E_height_next.
    """
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('undecic pin rows require z != 0')
    a, b, c, d, e, f, g, h, ii, jj, kk, ll = map(
        exact,
        (
            f_xxxxxxxxxxx, f_xxxxxxxxxxy, f_xxxxxxxxxyy, f_xxxxxxxxyyy,
            f_xxxxxxxyyyy, f_xxxxxxyyyyy, f_xxxxxyyyyyy, f_xxxxyyyyyyy,
            f_xxxyyyyyyyy, f_xxyyyyyyyyy, f_xyyyyyyyyyy, f_yyyyyyyyyyy,
        ),
    )
    # (1/3628800) D¹¹f(z^10) components
    g1 = (
        a * u ** 10 + 10 * b * u ** 9 * v + 45 * c * u ** 8 * v * v
        + 120 * d * u ** 7 * v ** 3 + 210 * e * u ** 6 * v ** 4
        + 252 * f * u ** 5 * v ** 5 + 210 * g * u ** 4 * v ** 6
        + 120 * h * u ** 3 * v ** 7 + 45 * ii * u * u * v ** 8
        + 10 * jj * u * v ** 9 + kk * v ** 10
    ) / 3628800
    g2 = (
        b * u ** 10 + 10 * c * u ** 9 * v + 45 * d * u ** 8 * v * v
        + 120 * e * u ** 7 * v ** 3 + 210 * f * u ** 6 * v ** 4
        + 252 * g * u ** 5 * v ** 5 + 210 * h * u ** 4 * v ** 6
        + 120 * ii * u ** 3 * v ** 7 + 45 * jj * u * u * v ** 8
        + 10 * kk * u * v ** 9 + ll * v ** 10
    ) / 3628800
    # (1/39916800) D¹¹f(z^11)
    ht = (
        a * u ** 11 + 11 * b * u ** 10 * v + 55 * c * u ** 9 * v * v
        + 165 * d * u ** 8 * v ** 3 + 330 * e * u ** 7 * v ** 4
        + 462 * f * u ** 6 * v ** 5 + 462 * g * u ** 5 * v ** 6
        + 330 * h * u ** 4 * v ** 7 + 165 * ii * u ** 3 * v ** 8
        + 55 * jj * u * u * v ** 9 + 11 * kk * u * v ** 10 + ll * v ** 11
    ) / 39916800
    return {
        'E_grad_next_1': g1,
        'E_grad_next_2': g2,
        'E_height_next': ht,
        'z_dot_E_grad_next_minus_11_E_height_next': u * g1 + v * g2 - 11 * ht,
        'unmatched_density_r_power': 9,
        'explicit_r_factor_still_required': True,
        'z1': u,
        'z2': v,
        'f_xxxxxxxxxxx': a,
        'f_xxxxxxxxxxy': b,
        'f_xxxxxxxxxyy': c,
        'f_xxxxxxxxyyy': d,
        'f_xxxxxxxyyyy': e,
        'f_xxxxxxyyyyy': f,
        'f_xxxxxyyyyyy': g,
        'f_xxxxyyyyyyy': h,
        'f_xxxyyyyyyyy': ii,
        'f_xxyyyyyyyyy': jj,
        'f_xyyyyyyyyyy': kk,
        'f_yyyyyyyyyyy': ll,
    }


def pin_site_morse_dodecic_rows(
    z1: int | Q, z2: int | Q, *,
    f_xxxxxxxxxxxx: int | Q, f_xxxxxxxxxxxy: int | Q, f_xxxxxxxxxxyy: int | Q,
    f_xxxxxxxxxyyy: int | Q, f_xxxxxxxxyyyy: int | Q, f_xxxxxxxyyyyy: int | Q,
    f_xxxxxxyyyyyy: int | Q, f_xxxxxyyyyyyy: int | Q, f_xxxxyyyyyyyy: int | Q,
    f_xxxyyyyyyyyy: int | Q, f_xxyyyyyyyyyy: int | Q, f_xyyyyyyyyyyy: int | Q,
    f_yyyyyyyyyyyy: int | Q,
) -> dict[str, Q | bool | int]:
    """Dodecic (twelfth-order) pin-local contact residuals after undecic next-order.

    With twelfth derivatives at the pin:
      grad f(pin+rz) = … + (r^11/39916800) D¹²f(z^11) + O(r^12)
      f(pin+rz)-f(pin) = … + (r^12/479001600) D¹²f(z^12) + O(r^13)
    so after stripping leading powers the unmatched r^10 corrections are
      F_grad_next = (1/39916800) D¹²f(z^11),
      F_height_next = (1/479001600) D¹²f(z^12),
    with the exact identity z·F_grad_next = 12 F_height_next.
    """
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('dodecic pin rows require z != 0')
    a, b, c, d, e, f, g, h, ii, jj, kk, ll, mm = map(
        exact,
        (
            f_xxxxxxxxxxxx, f_xxxxxxxxxxxy, f_xxxxxxxxxxyy, f_xxxxxxxxxyyy,
            f_xxxxxxxxyyyy, f_xxxxxxxyyyyy, f_xxxxxxyyyyyy, f_xxxxxyyyyyyy,
            f_xxxxyyyyyyyy, f_xxxyyyyyyyyy, f_xxyyyyyyyyyy, f_xyyyyyyyyyyy,
            f_yyyyyyyyyyyy,
        ),
    )
    # (1/39916800) D¹²f(z^11) components
    g1 = (
        a * u ** 11 + 11 * b * u ** 10 * v + 55 * c * u ** 9 * v * v
        + 165 * d * u ** 8 * v ** 3 + 330 * e * u ** 7 * v ** 4
        + 462 * f * u ** 6 * v ** 5 + 462 * g * u ** 5 * v ** 6
        + 330 * h * u ** 4 * v ** 7 + 165 * ii * u ** 3 * v ** 8
        + 55 * jj * u * u * v ** 9 + 11 * kk * u * v ** 10 + ll * v ** 11
    ) / 39916800
    g2 = (
        b * u ** 11 + 11 * c * u ** 10 * v + 55 * d * u ** 9 * v * v
        + 165 * e * u ** 8 * v ** 3 + 330 * f * u ** 7 * v ** 4
        + 462 * g * u ** 6 * v ** 5 + 462 * h * u ** 5 * v ** 6
        + 330 * ii * u ** 4 * v ** 7 + 165 * jj * u ** 3 * v ** 8
        + 55 * kk * u * u * v ** 9 + 11 * ll * u * v ** 10 + mm * v ** 11
    ) / 39916800
    # (1/479001600) D¹²f(z^12)
    ht = (
        a * u ** 12 + 12 * b * u ** 11 * v + 66 * c * u ** 10 * v * v
        + 220 * d * u ** 9 * v ** 3 + 495 * e * u ** 8 * v ** 4
        + 792 * f * u ** 7 * v ** 5 + 924 * g * u ** 6 * v ** 6
        + 792 * h * u ** 5 * v ** 7 + 495 * ii * u ** 4 * v ** 8
        + 220 * jj * u ** 3 * v ** 9 + 66 * kk * u * u * v ** 10
        + 12 * ll * u * v ** 11 + mm * v ** 12
    ) / 479001600
    return {
        'F_grad_next_1': g1,
        'F_grad_next_2': g2,
        'F_height_next': ht,
        'z_dot_F_grad_next_minus_12_F_height_next': u * g1 + v * g2 - 12 * ht,
        'unmatched_density_r_power': 10,
        'explicit_r_factor_still_required': True,
        'z1': u,
        'z2': v,
        'f_xxxxxxxxxxxx': a,
        'f_xxxxxxxxxxxy': b,
        'f_xxxxxxxxxxyy': c,
        'f_xxxxxxxxxyyy': d,
        'f_xxxxxxxxyyyy': e,
        'f_xxxxxxxyyyyy': f,
        'f_xxxxxxyyyyyy': g,
        'f_xxxxxyyyyyyy': h,
        'f_xxxxyyyyyyyy': ii,
        'f_xxxyyyyyyyyy': jj,
        'f_xxyyyyyyyyyy': kk,
        'f_xyyyyyyyyyyy': ll,
        'f_yyyyyyyyyyyy': mm,
    }


def pin_site_morse_tridecic_rows(
    z1: int | Q, z2: int | Q, *,
    f_xxxxxxxxxxxxx: int | Q, f_xxxxxxxxxxxxy: int | Q, f_xxxxxxxxxxxyy: int | Q,
    f_xxxxxxxxxxyyy: int | Q, f_xxxxxxxxxyyyy: int | Q, f_xxxxxxxxyyyyy: int | Q,
    f_xxxxxxxyyyyyy: int | Q, f_xxxxxxyyyyyyy: int | Q, f_xxxxxyyyyyyyy: int | Q,
    f_xxxxyyyyyyyyy: int | Q, f_xxxyyyyyyyyyy: int | Q, f_xxyyyyyyyyyyy: int | Q,
    f_xyyyyyyyyyyyy: int | Q, f_yyyyyyyyyyyyy: int | Q,
) -> dict[str, Q | bool | int]:
    """Tridecic (thirteenth-order) pin-local contact residuals after dodecic next-order.

    With thirteenth derivatives at the pin:
      grad f(pin+rz) = … + (r^12/479001600) D¹³f(z^12) + O(r^13)
      f(pin+rz)-f(pin) = … + (r^13/6227020800) D¹³f(z^13) + O(r^14)
    so after stripping leading powers the unmatched r^11 corrections are
      G_grad_next = (1/479001600) D¹³f(z^12),
      G_height_next = (1/6227020800) D¹³f(z^13),
    with the exact identity z·G_grad_next = 13 G_height_next.
    """
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('tridecic pin rows require z != 0')
    a, b, c, d, e, f, g, h, ii, jj, kk, ll, mm, nn = map(
        exact,
        (
            f_xxxxxxxxxxxxx, f_xxxxxxxxxxxxy, f_xxxxxxxxxxxyy, f_xxxxxxxxxxyyy,
            f_xxxxxxxxxyyyy, f_xxxxxxxxyyyyy, f_xxxxxxxyyyyyy, f_xxxxxxyyyyyyy,
            f_xxxxxyyyyyyyy, f_xxxxyyyyyyyyy, f_xxxyyyyyyyyyy, f_xxyyyyyyyyyyy,
            f_xyyyyyyyyyyyy, f_yyyyyyyyyyyyy,
        ),
    )
    # (1/479001600) D¹³f(z^12) components
    g1 = (
        a * u ** 12 + 12 * b * u ** 11 * v + 66 * c * u ** 10 * v * v
        + 220 * d * u ** 9 * v ** 3 + 495 * e * u ** 8 * v ** 4
        + 792 * f * u ** 7 * v ** 5 + 924 * g * u ** 6 * v ** 6
        + 792 * h * u ** 5 * v ** 7 + 495 * ii * u ** 4 * v ** 8
        + 220 * jj * u ** 3 * v ** 9 + 66 * kk * u * u * v ** 10
        + 12 * ll * u * v ** 11 + mm * v ** 12
    ) / 479001600
    g2 = (
        b * u ** 12 + 12 * c * u ** 11 * v + 66 * d * u ** 10 * v * v
        + 220 * e * u ** 9 * v ** 3 + 495 * f * u ** 8 * v ** 4
        + 792 * g * u ** 7 * v ** 5 + 924 * h * u ** 6 * v ** 6
        + 792 * ii * u ** 5 * v ** 7 + 495 * jj * u ** 4 * v ** 8
        + 220 * kk * u ** 3 * v ** 9 + 66 * ll * u * u * v ** 10
        + 12 * mm * u * v ** 11 + nn * v ** 12
    ) / 479001600
    # (1/6227020800) D¹³f(z^13)
    ht = (
        a * u ** 13 + 13 * b * u ** 12 * v + 78 * c * u ** 11 * v * v
        + 286 * d * u ** 10 * v ** 3 + 715 * e * u ** 9 * v ** 4
        + 1287 * f * u ** 8 * v ** 5 + 1716 * g * u ** 7 * v ** 6
        + 1716 * h * u ** 6 * v ** 7 + 1287 * ii * u ** 5 * v ** 8
        + 715 * jj * u ** 4 * v ** 9 + 286 * kk * u ** 3 * v ** 10
        + 78 * ll * u * u * v ** 11 + 13 * mm * u * v ** 12 + nn * v ** 13
    ) / 6227020800
    return {
        'G_grad_next_1': g1,
        'G_grad_next_2': g2,
        'G_height_next': ht,
        'z_dot_G_grad_next_minus_13_G_height_next': u * g1 + v * g2 - 13 * ht,
        'unmatched_density_r_power': 11,
        'explicit_r_factor_still_required': True,
        'z1': u,
        'z2': v,
        'f_xxxxxxxxxxxxx': a,
        'f_xxxxxxxxxxxxy': b,
        'f_xxxxxxxxxxxyy': c,
        'f_xxxxxxxxxxyyy': d,
        'f_xxxxxxxxxyyyy': e,
        'f_xxxxxxxxyyyyy': f,
        'f_xxxxxxxyyyyyy': g,
        'f_xxxxxxyyyyyyy': h,
        'f_xxxxxyyyyyyyy': ii,
        'f_xxxxyyyyyyyyy': jj,
        'f_xxxyyyyyyyyyy': kk,
        'f_xxyyyyyyyyyyy': ll,
        'f_xyyyyyyyyyyyy': mm,
        'f_yyyyyyyyyyyyy': nn,
    }


def pin_site_morse_tetradecic_rows(
    z1: int | Q, z2: int | Q, *,
    f_xxxxxxxxxxxxxx: int | Q, f_xxxxxxxxxxxxxy: int | Q, f_xxxxxxxxxxxxyy: int | Q,
    f_xxxxxxxxxxxyyy: int | Q, f_xxxxxxxxxxyyyy: int | Q, f_xxxxxxxxxyyyyy: int | Q,
    f_xxxxxxxxyyyyyy: int | Q, f_xxxxxxxyyyyyyy: int | Q, f_xxxxxxyyyyyyyy: int | Q,
    f_xxxxxyyyyyyyyy: int | Q, f_xxxxyyyyyyyyyy: int | Q, f_xxxyyyyyyyyyyy: int | Q,
    f_xxyyyyyyyyyyyy: int | Q, f_xyyyyyyyyyyyyy: int | Q, f_yyyyyyyyyyyyyy: int | Q,
) -> dict[str, Q | bool | int]:
    """Tetradecic (fourteenth-order) pin-local contact residuals after tridecic next-order.

    With fourteenth derivatives at the pin:
      grad f(pin+rz) = … + (r^13/6227020800) D¹⁴f(z^13) + O(r^14)
      f(pin+rz)-f(pin) = … + (r^14/87178291200) D¹⁴f(z^14) + O(r^15)
    so after stripping leading powers the unmatched r^12 corrections are
      I_grad_next = (1/6227020800) D¹⁴f(z^13),
      I_height_next = (1/87178291200) D¹⁴f(z^14),
    with the exact identity z·I_grad_next = 14 I_height_next.
    """
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('tetradecic pin rows require z != 0')
    a, b, c, d, e, f, g, h, ii, jj, kk, ll, mm, nn, oo = map(
        exact,
        (
            f_xxxxxxxxxxxxxx, f_xxxxxxxxxxxxxy, f_xxxxxxxxxxxxyy, f_xxxxxxxxxxxyyy,
            f_xxxxxxxxxxyyyy, f_xxxxxxxxxyyyyy, f_xxxxxxxxyyyyyy, f_xxxxxxxyyyyyyy,
            f_xxxxxxyyyyyyyy, f_xxxxxyyyyyyyyy, f_xxxxyyyyyyyyyy, f_xxxyyyyyyyyyyy,
            f_xxyyyyyyyyyyyy, f_xyyyyyyyyyyyyy, f_yyyyyyyyyyyyyy,
        ),
    )
    # (1/6227020800) D¹⁴f(z^13) components
    g1 = (
        a * u ** 13 + 13 * b * u ** 12 * v + 78 * c * u ** 11 * v * v
        + 286 * d * u ** 10 * v ** 3 + 715 * e * u ** 9 * v ** 4
        + 1287 * f * u ** 8 * v ** 5 + 1716 * g * u ** 7 * v ** 6
        + 1716 * h * u ** 6 * v ** 7 + 1287 * ii * u ** 5 * v ** 8
        + 715 * jj * u ** 4 * v ** 9 + 286 * kk * u ** 3 * v ** 10
        + 78 * ll * u * u * v ** 11 + 13 * mm * u * v ** 12 + nn * v ** 13
    ) / 6227020800
    g2 = (
        b * u ** 13 + 13 * c * u ** 12 * v + 78 * d * u ** 11 * v * v
        + 286 * e * u ** 10 * v ** 3 + 715 * f * u ** 9 * v ** 4
        + 1287 * g * u ** 8 * v ** 5 + 1716 * h * u ** 7 * v ** 6
        + 1716 * ii * u ** 6 * v ** 7 + 1287 * jj * u ** 5 * v ** 8
        + 715 * kk * u ** 4 * v ** 9 + 286 * ll * u ** 3 * v ** 10
        + 78 * mm * u * u * v ** 11 + 13 * nn * u * v ** 12 + oo * v ** 13
    ) / 6227020800
    # (1/87178291200) D¹⁴f(z^14)
    ht = (
        a * u ** 14 + 14 * b * u ** 13 * v + 91 * c * u ** 12 * v * v
        + 364 * d * u ** 11 * v ** 3 + 1001 * e * u ** 10 * v ** 4
        + 2002 * f * u ** 9 * v ** 5 + 3003 * g * u ** 8 * v ** 6
        + 3432 * h * u ** 7 * v ** 7 + 3003 * ii * u ** 6 * v ** 8
        + 2002 * jj * u ** 5 * v ** 9 + 1001 * kk * u ** 4 * v ** 10
        + 364 * ll * u ** 3 * v ** 11 + 91 * mm * u * u * v ** 12
        + 14 * nn * u * v ** 13 + oo * v ** 14
    ) / 87178291200
    return {
        'I_grad_next_1': g1,
        'I_grad_next_2': g2,
        'I_height_next': ht,
        'z_dot_I_grad_next_minus_14_I_height_next': u * g1 + v * g2 - 14 * ht,
        'unmatched_density_r_power': 12,
        'explicit_r_factor_still_required': True,
        'z1': u,
        'z2': v,
        'f_xxxxxxxxxxxxxx': a,
        'f_xxxxxxxxxxxxxy': b,
        'f_xxxxxxxxxxxxyy': c,
        'f_xxxxxxxxxxxyyy': d,
        'f_xxxxxxxxxxyyyy': e,
        'f_xxxxxxxxxyyyyy': f,
        'f_xxxxxxxxyyyyyy': g,
        'f_xxxxxxxyyyyyyy': h,
        'f_xxxxxxyyyyyyyy': ii,
        'f_xxxxxyyyyyyyyy': jj,
        'f_xxxxyyyyyyyyyy': kk,
        'f_xxxyyyyyyyyyyy': ll,
        'f_xxyyyyyyyyyyyy': mm,
        'f_xyyyyyyyyyyyyy': nn,
        'f_yyyyyyyyyyyyyy': oo,
    }



def pin_site_morse_pentadecic_rows(
    z1: int | Q, z2: int | Q, *,
    f_xxxxxxxxxxxxxxx: int | Q, f_xxxxxxxxxxxxxxy: int | Q, f_xxxxxxxxxxxxxyy: int | Q,
    f_xxxxxxxxxxxxyyy: int | Q, f_xxxxxxxxxxxyyyy: int | Q, f_xxxxxxxxxxyyyyy: int | Q,
    f_xxxxxxxxxyyyyyy: int | Q, f_xxxxxxxxyyyyyyy: int | Q, f_xxxxxxxyyyyyyyy: int | Q,
    f_xxxxxxyyyyyyyyy: int | Q, f_xxxxxyyyyyyyyyy: int | Q, f_xxxxyyyyyyyyyyy: int | Q,
    f_xxxyyyyyyyyyyyy: int | Q, f_xxyyyyyyyyyyyyy: int | Q, f_xyyyyyyyyyyyyyy: int | Q,
    f_yyyyyyyyyyyyyyy: int | Q,
) -> dict[str, Q | bool | int]:
    """Pentadecic (fifteenth-order) pin-local contact residuals after tetradecic next-order.

    With fifteenth derivatives at the pin:
      grad f(pin+rz) = … + (r^14/87178291200) D¹⁵f(z^14) + O(r^15)
      f(pin+rz)-f(pin) = … + (r^15/1307674368000) D¹⁵f(z^15) + O(r^16)
    so after stripping leading powers the unmatched r^13 corrections are
      J_grad_next = (1/87178291200) D¹⁵f(z^14),
      J_height_next = (1/1307674368000) D¹⁵f(z^15),
    with the exact identity z·J_grad_next = 15 J_height_next.
    """
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('pentadecic pin rows require z != 0')
    a, b, c, d, e, f, g, h, ii, jj, kk, ll, mm, nn, oo, pp = map(
        exact,
        (
            f_xxxxxxxxxxxxxxx, f_xxxxxxxxxxxxxxy, f_xxxxxxxxxxxxxyy, f_xxxxxxxxxxxxyyy,
            f_xxxxxxxxxxxyyyy, f_xxxxxxxxxxyyyyy, f_xxxxxxxxxyyyyyy, f_xxxxxxxxyyyyyyy,
            f_xxxxxxxyyyyyyyy, f_xxxxxxyyyyyyyyy, f_xxxxxyyyyyyyyyy, f_xxxxyyyyyyyyyyy,
            f_xxxyyyyyyyyyyyy, f_xxyyyyyyyyyyyyy, f_xyyyyyyyyyyyyyy, f_yyyyyyyyyyyyyyy,
        ),
    )
    # (1/87178291200) D¹⁵f(z^14) components
    g1 = (
        a * u ** 14 + 14 * b * u ** 13 * v
        + 91 * c * u ** 12 * v * v + 364 * d * u ** 11 * v ** 3
        + 1001 * e * u ** 10 * v ** 4 + 2002 * f * u ** 9 * v ** 5
        + 3003 * g * u ** 8 * v ** 6 + 3432 * h * u ** 7 * v ** 7
        + 3003 * ii * u ** 6 * v ** 8 + 2002 * jj * u ** 5 * v ** 9
        + 1001 * kk * u ** 4 * v ** 10 + 364 * ll * u ** 3 * v ** 11
        + 91 * mm * u ** 2 * v ** 12 + 14 * nn * u * v ** 13
        + oo * v ** 14
    ) / 87178291200
    g2 = (
        b * u ** 14 + 14 * c * u ** 13 * v
        + 91 * d * u ** 12 * v * v + 364 * e * u ** 11 * v ** 3
        + 1001 * f * u ** 10 * v ** 4 + 2002 * g * u ** 9 * v ** 5
        + 3003 * h * u ** 8 * v ** 6 + 3432 * ii * u ** 7 * v ** 7
        + 3003 * jj * u ** 6 * v ** 8 + 2002 * kk * u ** 5 * v ** 9
        + 1001 * ll * u ** 4 * v ** 10 + 364 * mm * u ** 3 * v ** 11
        + 91 * nn * u ** 2 * v ** 12 + 14 * oo * u * v ** 13
        + pp * v ** 14
    ) / 87178291200
    # (1/1307674368000) D¹⁵f(z^15)
    ht = (
        a * u ** 15 + 15 * b * u ** 14 * v
        + 105 * c * u ** 13 * v * v + 455 * d * u ** 12 * v ** 3
        + 1365 * e * u ** 11 * v ** 4 + 3003 * f * u ** 10 * v ** 5
        + 5005 * g * u ** 9 * v ** 6 + 6435 * h * u ** 8 * v ** 7
        + 6435 * ii * u ** 7 * v ** 8 + 5005 * jj * u ** 6 * v ** 9
        + 3003 * kk * u ** 5 * v ** 10 + 1365 * ll * u ** 4 * v ** 11
        + 455 * mm * u ** 3 * v ** 12 + 105 * nn * u ** 2 * v ** 13
        + 15 * oo * u * v ** 14 + pp * v ** 15
    ) / 1307674368000
    return {
        'J_grad_next_1': g1,
        'J_grad_next_2': g2,
        'J_height_next': ht,
        'z_dot_J_grad_next_minus_15_J_height_next': u * g1 + v * g2 - 15 * ht,
        'unmatched_density_r_power': 13,
        'explicit_r_factor_still_required': True,
        'z1': u,
        'z2': v,
        'f_xxxxxxxxxxxxxxx': a,
        'f_xxxxxxxxxxxxxxy': b,
        'f_xxxxxxxxxxxxxyy': c,
        'f_xxxxxxxxxxxxyyy': d,
        'f_xxxxxxxxxxxyyyy': e,
        'f_xxxxxxxxxxyyyyy': f,
        'f_xxxxxxxxxyyyyyy': g,
        'f_xxxxxxxxyyyyyyy': h,
        'f_xxxxxxxyyyyyyyy': ii,
        'f_xxxxxxyyyyyyyyy': jj,
        'f_xxxxxyyyyyyyyyy': kk,
        'f_xxxxyyyyyyyyyyy': ll,
        'f_xxxyyyyyyyyyyyy': mm,
        'f_xxyyyyyyyyyyyyy': nn,
        'f_xyyyyyyyyyyyyyy': oo,
        'f_yyyyyyyyyyyyyyy': pp,
    }



def pin_site_morse_hexadecic_rows(
    z1: int | Q, z2: int | Q, *,
    f_xxxxxxxxxxxxxxxx: int | Q, f_xxxxxxxxxxxxxxxy: int | Q, f_xxxxxxxxxxxxxxyy: int | Q,
    f_xxxxxxxxxxxxxyyy: int | Q, f_xxxxxxxxxxxxyyyy: int | Q, f_xxxxxxxxxxxyyyyy: int | Q,
    f_xxxxxxxxxxyyyyyy: int | Q, f_xxxxxxxxxyyyyyyy: int | Q, f_xxxxxxxxyyyyyyyy: int | Q,
    f_xxxxxxxyyyyyyyyy: int | Q, f_xxxxxxyyyyyyyyyy: int | Q, f_xxxxxyyyyyyyyyyy: int | Q,
    f_xxxxyyyyyyyyyyyy: int | Q, f_xxxyyyyyyyyyyyyy: int | Q, f_xxyyyyyyyyyyyyyy: int | Q,
    f_xyyyyyyyyyyyyyyy: int | Q, f_yyyyyyyyyyyyyyyy: int | Q,
) -> dict[str, Q | bool | int]:
    """Hexadecic (sixteenth-order) pin-local contact residuals after pentadecic next-order.

    With sixteenth derivatives at the pin:
      grad f(pin+rz) = … + (r^15/1307674368000) D¹⁶f(z^15) + O(r^16)
      f(pin+rz)-f(pin) = … + (r^16/20922789888000) D¹⁶f(z^16) + O(r^17)
    so after stripping leading powers the unmatched r^14 corrections are
      K_grad_next = (1/1307674368000) D¹⁶f(z^15),
      K_height_next = (1/20922789888000) D¹⁶f(z^16),
    with the exact identity z·K_grad_next = 16 K_height_next.
    Seventeenth-and-higher jets remain open.
    """
    u, v = exact(z1), exact(z2)
    if u == 0 and v == 0:
        raise ValueError('hexadecic pin rows require z != 0')
    a, b, c, d, e, f, g, h, ii, jj, kk, ll, mm, nn, oo, pp, qq = map(
        exact,
        (
            f_xxxxxxxxxxxxxxxx, f_xxxxxxxxxxxxxxxy, f_xxxxxxxxxxxxxxyy, f_xxxxxxxxxxxxxyyy,
            f_xxxxxxxxxxxxyyyy, f_xxxxxxxxxxxyyyyy, f_xxxxxxxxxxyyyyyy, f_xxxxxxxxxyyyyyyy,
            f_xxxxxxxxyyyyyyyy, f_xxxxxxxyyyyyyyyy, f_xxxxxxyyyyyyyyyy, f_xxxxxyyyyyyyyyyy,
            f_xxxxyyyyyyyyyyyy, f_xxxyyyyyyyyyyyyy, f_xxyyyyyyyyyyyyyy, f_xyyyyyyyyyyyyyyy,
            f_yyyyyyyyyyyyyyyy,
        ),
    )
    # (1/1307674368000) D¹⁶f(z^15) components
    g1 = (
        a * u ** 15 + 15 * b * u ** 14 * v
        + 105 * c * u ** 13 * v * v + 455 * d * u ** 12 * v ** 3
        + 1365 * e * u ** 11 * v ** 4 + 3003 * f * u ** 10 * v ** 5
        + 5005 * g * u ** 9 * v ** 6 + 6435 * h * u ** 8 * v ** 7
        + 6435 * ii * u ** 7 * v ** 8 + 5005 * jj * u ** 6 * v ** 9
        + 3003 * kk * u ** 5 * v ** 10 + 1365 * ll * u ** 4 * v ** 11
        + 455 * mm * u ** 3 * v ** 12 + 105 * nn * u ** 2 * v ** 13
        + 15 * oo * u * v ** 14 + pp * v ** 15
    ) / 1307674368000
    g2 = (
        b * u ** 15 + 15 * c * u ** 14 * v
        + 105 * d * u ** 13 * v * v + 455 * e * u ** 12 * v ** 3
        + 1365 * f * u ** 11 * v ** 4 + 3003 * g * u ** 10 * v ** 5
        + 5005 * h * u ** 9 * v ** 6 + 6435 * ii * u ** 8 * v ** 7
        + 6435 * jj * u ** 7 * v ** 8 + 5005 * kk * u ** 6 * v ** 9
        + 3003 * ll * u ** 5 * v ** 10 + 1365 * mm * u ** 4 * v ** 11
        + 455 * nn * u ** 3 * v ** 12 + 105 * oo * u ** 2 * v ** 13
        + 15 * pp * u * v ** 14 + qq * v ** 15
    ) / 1307674368000
    # (1/20922789888000) D¹⁶f(z^16)
    ht = (
        a * u ** 16 + 16 * b * u ** 15 * v
        + 120 * c * u ** 14 * v * v + 560 * d * u ** 13 * v ** 3
        + 1820 * e * u ** 12 * v ** 4 + 4368 * f * u ** 11 * v ** 5
        + 8008 * g * u ** 10 * v ** 6 + 11440 * h * u ** 9 * v ** 7
        + 12870 * ii * u ** 8 * v ** 8 + 11440 * jj * u ** 7 * v ** 9
        + 8008 * kk * u ** 6 * v ** 10 + 4368 * ll * u ** 5 * v ** 11
        + 1820 * mm * u ** 4 * v ** 12 + 560 * nn * u ** 3 * v ** 13
        + 120 * oo * u ** 2 * v ** 14 + 16 * pp * u * v ** 15
        + qq * v ** 16
    ) / 20922789888000
    return {
        'K_grad_next_1': g1,
        'K_grad_next_2': g2,
        'K_height_next': ht,
        'z_dot_K_grad_next_minus_16_K_height_next': u * g1 + v * g2 - 16 * ht,
        'unmatched_density_r_power': 14,
        'explicit_r_factor_still_required': True,
        'seventeenth_and_higher_jets_enumerated': False,
        'z1': u,
        'z2': v,
        'f_xxxxxxxxxxxxxxxx': a,
        'f_xxxxxxxxxxxxxxxy': b,
        'f_xxxxxxxxxxxxxxyy': c,
        'f_xxxxxxxxxxxxxyyy': d,
        'f_xxxxxxxxxxxxyyyy': e,
        'f_xxxxxxxxxxxyyyyy': f,
        'f_xxxxxxxxxxyyyyyy': g,
        'f_xxxxxxxxxyyyyyyy': h,
        'f_xxxxxxxxyyyyyyyy': ii,
        'f_xxxxxxxyyyyyyyyy': jj,
        'f_xxxxxxyyyyyyyyyy': kk,
        'f_xxxxxyyyyyyyyyyy': ll,
        'f_xxxxyyyyyyyyyyyy': mm,
        'f_xxxyyyyyyyyyyyyy': nn,
        'f_xxyyyyyyyyyyyyyy': oo,
        'f_xyyyyyyyyyyyyyyy': pp,
        'f_yyyyyyyyyyyyyyyy': qq,
    }


def pin_morse_hessian_signature(
    *, H_xx: int | Q, H_xy: int | Q, H_yy: int | Q, closer_pin: str,
) -> dict[str, Q | str | bool]:
    """Exact 2×2 Hessian signature constraints for max (M) vs saddle (S) pins.

    Morse nondegeneracy: det H != 0. Maximum M requires negative-definite H;
    saddle S requires indefinite H (det H < 0 in d=2). Does not bound densities.
    """
    if closer_pin not in ('M', 'S'):
        raise ValueError('closer_pin must be M or S')
    a, b, c = map(exact, (H_xx, H_xy, H_yy))
    det = a * c - b * b
    trace = a + c
    if det == 0:
        kind = 'DEGENERATE'
    elif det < 0:
        kind = 'INDEFINITE_SADDLE'
    elif a < 0 and c < 0:
        kind = 'NEGATIVE_DEFINITE_MAX'
    elif a > 0 and c > 0:
        kind = 'POSITIVE_DEFINITE_MIN'
    else:
        kind = 'POSITIVE_DEFINITE_MIN' if trace > 0 else 'NEGATIVE_DEFINITE_MAX'
    if closer_pin == 'M':
        matches = kind == 'NEGATIVE_DEFINITE_MAX'
        required = 'NEGATIVE_DEFINITE_MAX'
    else:
        matches = kind == 'INDEFINITE_SADDLE'
        required = 'INDEFINITE_SADDLE'
    return {
        'object': 'RN-MESOSCOPIC-PIN-MORSE-HESSIAN-SIGNATURE-20260925-v1',
        'closer_pin': closer_pin,
        'H_xx': a,
        'H_xy': b,
        'H_yy': c,
        'det_H': det,
        'trace_H': trace,
        'signature_kind': kind,
        'required_signature_for_pin': required,
        'signature_matches_pin_role': matches,
        'morse_nondegenerate': det != 0,
        'gaussian_density_factor_bounded': False,
        'meaning': (
            'exact Sylvester signature test for pin Hessian role; '
            'not a Kac-Rice density bound'
        ),
    }


def pin_site_jet_obstruction_ledger(
    y: Coord, *, inner: int | Q = Q(2, 5), outer: int | Q = 1,
    margin: int | Q = Q(1, 10),
) -> dict:
    """Exact structural obstruction for midpoint jets near a scaled pin.

    Records pin-local geometry and why midpoint U_0 jets fail. Leading Morse
    pin-site rows are enumerated separately in pin_centered_ledger_for_point.
    """
    frame = pin_centered_frame(y, inner=inner, outer=outer, margin=margin)
    z1 = frame['z1']
    z2 = frame['z2']
    dist2 = frame['dist2_to_closer_pin']
    return {
        'object': 'RN-MESOSCOPIC-PIN-SITE-JET-OBSTRUCTION-20260925-v1',
        'chart': 'C_pin_centered',
        'frame': frame,
        'pin_site_lies_on_scaled_axis': True,
        'physical_witness_offset': 'r * z',
        'spatial_distance_to_pin_r_power': 1,
        'spatial_volume_r_power': 2,
        'z1': z1,
        'z2': z2,
        'dist2_to_closer_pin': dist2,
        'midpoint_U0_rows_applicable': False,
        'raw_gradient_collides_with_pin_gradient_constraints': True,
        'near_pin_intersects_axial_thin_belt_locus': True,
        'leading_morse_rows_enumerated_elsewhere': True,
        'pin_site_higher_jets_enumerated': False,
        'required_before_full_chart': [
            'higher_order_pin_local_divided_differences',
            'pin_hessian_signature_max_vs_saddle',
            'contact_gaussian_density_bound',
        ],
        'hessian_ledger_evaluated': False,
        'uniform_integrand_bound_proved': False,
        'status': 'OPEN_HIGHER_JETS_AND_DENSITY',
        'meaning': (
            'midpoint jets blocked near pins; leading Morse pin-site rows exist in '
            'pin_centered_ledger; higher jets and density remain open'
        ),
    }


# Pin-local Morse scaling after grad f(pin)=0:
#   grad f(pin + r z) = r H z + O(r^2)              => p_grad = 1
#   f(pin + r z)-f(pin) = (r^2/2) z·H·z + O(r^3)   => p_height = 2
PIN_CENTERED_SCALING_EXPONENTS = {
    'grad': 1,
    'height': 2,
}

# At a Morse pin the Hessian is free at leading order (pin constraints fix value
# and gradient only), so |det H_pin| is O(1): leading det r-power 0.
PIN_CENTERED_HESSIAN_DET_R_POWER = 0


# Scaling exponents for raw witness (f_x, f_y, f-b) -> divided-difference J in this chart.
# Derived from the contact Taylor jet with U_0=(f,f_x,f_xx,f_xxx,f_y,f_xy)=(b,0,0,12k,0,0):
#   f_y(ry) = r * f_yy * y2 + O(r^2)            => divide by r^1
#   f_x(ry) = (r^2/2)(12k y1^2 + ...) + O(r^3)  => divide by r^2
#   f(ry)-b = (r^2/2) f_yy y2^2 + O(r^3)        => divide by r^2
SCALING_EXPONENTS = {
    'grad_x': 2,
    'grad_y': 1,
    'height': 2,
}

# On the axis y2=0 the leading f_y and height residuals lose a power of r:
#   f_y(r y1, 0) = (r^2 y1^2 / 2) f_xxy + O(r^3)           => p_y = 2
#   f(r y1, 0)-b = 2k r^3 y1^3 + O(r^3 · other 3-jets)     => p_height = 3
#   f_x still O(r^2)                                       => p_x = 2
AXIAL_SCALING_EXPONENTS = {
    'grad_x': 2,
    'grad_y': 2,
    'height': 3,
}

# Witness Hessian at x=ry after U_0, on C_transverse (exact leading powers of r):
#   f_xx(ry) = r (12k y1 + f_xxy y2) + O(r^2)     => p_xx = 1
#   f_xy(ry) = r (f_xxy y1 + f_xyy y2) + O(r^2)    => p_xy = 1
#   f_yy(ry) = f_yy + O(r)                          => p_yy = 0
# Raw det H = f_xx f_yy - f_xy^2 is therefore O(r) at leading order.
# On C_axial (y2=0) the same leading powers hold with y2-terms dropped.
HESSIAN_SCALING_EXPONENTS = {
    'xx': 1,
    'xy': 1,
    'yy': 0,
}


def witness_scaling_determinant_power(dimension: int = 2, *, chart: str = 'C_transverse') -> dict[str, int]:
    """r-power of det(diag(r^{p_i})) for the witness block on a declared chart."""
    if dimension != 2:
        raise ValueError('this package enumerates d=2 charts only')
    if chart == 'C_transverse':
        exponents = SCALING_EXPONENTS
    elif chart == 'C_axial':
        exponents = AXIAL_SCALING_EXPONENTS
    else:
        raise ValueError('unknown chart')
    power = exponents['grad_x'] + exponents['grad_y']
    return {
        'dimension': 2,
        'chart': chart,
        'gradient_scaling_exponents': (
            exponents['grad_x'],
            exponents['grad_y'],
        ),
        'height_scaling_exponent': exponents['height'],
        'gradient_jacobian_r_power': power,
        'spatial_volume_r_power': dimension,
        'height_window_r_power': 3,
        'meaning': (
            'det scaling for raw->J gradient map is r^(p_x+p_y); '
            'height scaling is recorded separately for the mark integral'
        ),
    }


def axial_contact_rows(y: Coord, *, gap_mark: int | Q,
                       f_xxy: int | Q, f_xyy: int | Q = 0,
                       f_yyy: int | Q = 0) -> dict[str, Q]:
    """Contact rows on C_axial (y2=0) after U_0 constraints.

    Leading residuals:
      J_grad_y = (y1^2 / 2) f_xxy
      J_grad_x = 6k y1^2
      J_height = 2k y1^3
    (height already at the cubic order; p_height=3).
    """
    if not axial_chart_ok(y):
        raise ValueError('point outside C_axial chart')
    y1, y2 = y
    k = exact(gap_mark)
    b = exact(f_xxy)
    if k <= 0:
        raise ValueError('positive gap mark required')
    if y2 != 0:
        raise ValueError('axial chart requires y2=0')
    return {
        'J_grad_y': (y1 * y1 * b) / 2,
        'J_grad_x': 6 * k * y1 * y1,
        'J_height': 2 * k * y1 ** 3,
        'y1': y1,
        'y2': y2,
        'gap_mark': k,
        'f_xxy': b,
        'f_xyy': exact(f_xyy),
        'f_yyy': exact(f_yyy),
    }


def axial_ledger_for_point(y: Coord, gap_mark: int | Q = 1,
                           f_xxy: int | Q = 1) -> dict:
    rows = axial_contact_rows(y, gap_mark=gap_mark, f_xxy=f_xxy)
    scale = witness_scaling_determinant_power(2, chart='C_axial')
    return {
        'object': 'RN-MESOSCOPIC-CHART-J0-D2-AXIAL-20260925-v1',
        'chart': 'C_axial',
        'y': {'y1': rows['y1'], 'y2': rows['y2']},
        'contact_rows': {
            'J_grad_y': rows['J_grad_y'],
            'J_grad_x': rows['J_grad_x'],
            'J_height': rows['J_height'],
        },
        'scaling': scale,
        'gradient_jacobian_r_power': scale['gradient_jacobian_r_power'],
        'height_independent_at_leading_axial_order': True,
        'hessian_contact_rows_enumerated': True,
        'hessian_ledger_evaluated': False,
        'full_annulus_closed': False,
        'legacy_24jet_discharged': False,
        'independent_analytic_acceptance': False,
        'complements_pr7': True,
        'meaning': (
            'exact d=2 axial chart contact rows and gradient Jacobian r-power 4; '
            'not a continuum Gaussian evaluation'
        ),
    }


def _contact_jet_polynomials(y: Coord, *, gap_mark: int | Q,
                             f_yy: int | Q, f_xxy: int | Q, f_xyy: int | Q,
                             f_yyy: int | Q = 0) -> dict[str, Q]:
    """Shared contact-jet polynomials (no chart membership check)."""
    y1, y2 = y
    k = exact(gap_mark)
    a, b, c, d = map(exact, (f_yy, f_xxy, f_xyy, f_yyy))
    if k <= 0:
        raise ValueError('positive gap mark required')
    j_y = a * y2
    j_x = 6 * k * y1 * y1 + b * y1 * y2 + (c * y2 * y2) / 2
    j_h = (a * y2 * y2) / 2
    h1 = (
        2 * k * y1 ** 3
        + (b * y1 * y1 * y2) / 2
        + (c * y1 * y2 * y2) / 2
        + (d * y2 ** 3) / 6
    )
    return {
        'J_grad_y': j_y,
        'J_grad_x': j_x,
        'J_height': j_h,
        'H_height_next': h1,
        'height_residual_at_leading_order': j_h - (y2 / 2) * j_y,
        'y1': y1,
        'y2': y2,
        'gap_mark': k,
        'f_yy': a,
        'f_xxy': b,
        'f_xyy': c,
        'f_yyy': d,
    }


def contact_rows(y: Coord, *, gap_mark: int | Q,
                 f_yy: int | Q, f_xxy: int | Q, f_xyy: int | Q,
                 f_yyy: int | Q = 0) -> dict[str, Q]:
    """Contact-limit J_0 rows on C_transverse after the six-pin / U_0 constraints.

    Free jet leftovers used here: f_yy, f_xxy, f_xyy, f_yyy (exact rationals).
    Gap mark k enters through f_xxx=12k at contact.
    """
    if not transverse_chart_ok(y):
        raise ValueError('point outside C_transverse chart')
    return _contact_jet_polynomials(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )


def hessian_contact_rows(y: Coord, *, gap_mark: int | Q,
                         f_yy: int | Q, f_xxy: int | Q, f_xyy: int | Q,
                         f_yyy: int | Q = 0) -> dict[str, Q]:
    """Leading contact Hessian entries on C_transverse after stripping r-powers.

    H_xx_contact = f_xx(ry)/r + O(r) = 12k y1 + f_xxy y2
    H_xy_contact = f_xy(ry)/r + O(r) = f_xxy y1 + f_xyy y2
    H_yy_contact = f_yy(ry) + O(r)   = f_yy
    """
    if not transverse_chart_ok(y):
        raise ValueError('point outside C_transverse chart')
    y1, y2 = y
    k = exact(gap_mark)
    a, b, c, d = map(exact, (f_yy, f_xxy, f_xyy, f_yyy))
    if k <= 0:
        raise ValueError('positive gap mark required')
    h_xx = 12 * k * y1 + b * y2
    h_xy = b * y1 + c * y2
    h_yy = a
    # Next-order correction to f_yy(ry) after the constant term.
    h_yy_next = c * y1 + d * y2
    return {
        'H_xx_contact': h_xx,
        'H_xy_contact': h_xy,
        'H_yy_contact': h_yy,
        'H_yy_next': h_yy_next,
        'det_contact_leading': h_xx * h_yy,
        'det_xy_square_coefficient': h_xy * h_xy,
        'y1': y1,
        'y2': y2,
        'gap_mark': k,
        'f_yy': a,
        'f_xxy': b,
        'f_xyy': c,
        'f_yyy': d,
    }


def hessian_scaling_report(dimension: int = 2, *, chart: str = 'C_transverse') -> dict:
    """r-powers for the d=2 witness Hessian on a declared chart."""
    if dimension != 2:
        raise ValueError('this package enumerates d=2 charts only')
    if chart not in ('C_transverse', 'C_axial'):
        raise ValueError('Hessian scaling is enumerated on C_transverse and C_axial only')
    exp = HESSIAN_SCALING_EXPONENTS
    return {
        'dimension': 2,
        'chart': chart,
        'hessian_scaling_exponents': {
            'xx': exp['xx'],
            'xy': exp['xy'],
            'yy': exp['yy'],
        },
        'raw_det_leading_r_power': 1,
        'meaning': (
            'raw det H = r * H_xx_contact * H_yy_contact - r^2 * H_xy_contact^2 + O(r^2); '
            'leading factor is r^1; conditioned Gaussian expectation of |det H| is not evaluated'
        ),
        'conditioned_expectation_evaluated': False,
    }


def contact_integrand_power_ledger(dimension: int = 2, *, chart: str = 'C_transverse') -> dict:
    """Exact r-power bookkeeping for the mesoscopic Kac–Rice count integrand.

    Combines spatial volume, gradient change-of-variables, leading |det H|, and the
    between-pin height window. Does not bound the contact Gaussian density factor.
    """
    if dimension != 2:
        raise ValueError('this package enumerates d=2 charts only')
    if chart == 'C_transverse':
        grad = SCALING_EXPONENTS['grad_x'] + SCALING_EXPONENTS['grad_y']
        axial_measure_zero_in_area = False
    elif chart == 'C_axial':
        grad = AXIAL_SCALING_EXPONENTS['grad_x'] + AXIAL_SCALING_EXPONENTS['grad_y']
        axial_measure_zero_in_area = True
    else:
        raise ValueError('unknown chart')
    spatial = dimension
    hess = HESSIAN_SCALING_EXPONENTS['xx']  # leading det power; yy contributes r^0
    height = 3
    # Density picks up r^(-grad); |det H| contributes r^(hess); dy gives r^(spatial);
    # integrating the between-pin height window contributes r^(height).
    net = spatial - grad + hess + height  # midpoint charts
    return {
        'object': 'RN-MESOSCOPIC-CHART-INTEGRAND-POWER-D2-20260925-v1',
        'dimension': 2,
        'chart': chart,
        'spatial_volume_r_power': spatial,
        'gradient_jacobian_r_power': grad,
        'gradient_density_r_power': -grad,
        'hessian_det_leading_r_power': hess,
        'height_window_r_power': height,
        'net_count_r_power': net,
        'axial_chart_has_area_measure_zero': axial_measure_zero_in_area,
        'contact_density_bound_proved': False,
        'full_annulus_closed': False,
        'legacy_24jet_discharged': False,
        'meaning': (
            'power identity only: r^(spatial - grad_jac + hess_det + height_window); '
            'not a uniform bound on the contact integrand factor'
        ),
    }


def pin_centered_integrand_power_ledger(dimension: int = 2) -> dict:
    """Exact r-power bookkeeping for the pin-centered Morse chart integrand.

    Uses pin-local gradient Jacobian r^2, Hessian det r^0, spatial r^2, and the
    global between-pin height window r^3. Does not bound the contact density.
    """
    if dimension != 2:
        raise ValueError('this package enumerates d=2 charts only')
    spatial = dimension
    grad = 2 * PIN_CENTERED_SCALING_EXPONENTS['grad']
    hess = PIN_CENTERED_HESSIAN_DET_R_POWER
    height = 3
    net = spatial - grad + hess + height  # pin-centered Morse chart
    return {
        'object': 'RN-MESOSCOPIC-PIN-CENTERED-INTEGRAND-POWER-D2-20260925-v1',
        'dimension': 2,
        'chart': 'C_pin_centered',
        'spatial_volume_r_power': spatial,
        'gradient_jacobian_r_power': grad,
        'gradient_density_r_power': -grad,
        'hessian_det_leading_r_power': hess,
        'height_window_r_power': height,
        'net_count_r_power': net,
        'pin_contact_density_bound_proved': False,
        'pin_site_higher_jets_enumerated': False,
        'full_annulus_closed': False,
        'legacy_24jet_discharged': False,
        'meaning': (
            'pin-local power identity r^(2 - 2 + 0 + 3)=r^3; '
            'not a uniform bound on the contact integrand factor'
        ),
    }


def pin_centered_contact_integrand_algebraic_factor_skeleton(
    y: Coord, *, inner: int | Q = Q(2, 5), outer: int | Q = 1,
    margin: int | Q = Q(1, 10),
    H_xx: int | Q = -1, H_xy: int | Q = 0, H_yy: int | Q = 1,
) -> dict:
    """Exact algebraic Jacobian×|det H| factor product on C_pin_centered (density open).

    Leading Morse contact J_grad = H_pin · z. With z2≠0 eliminate (H_xy, H_yy):
      |det ∂(J1,J2)/∂(H_xy,H_yy)| = z2²
    (if z2=0 and z1≠0, eliminate (H_xx,H_xy) with |det|=z1²). The typed Hessian
    factor is |det H| = |H_xx H_yy − H_xy²| (r-power 0). Product identity only;
    Gaussian density / higher jets remain open. Small-A diagnostic chart.
    """
    frame = pin_centered_frame(y, inner=inner, outer=outer, margin=margin)
    u, v = exact(frame['z1']), exact(frame['z2'])
    if u == 0 and v == 0:
        raise ValueError('pin algebraic factor requires z != 0')
    a, b, c = map(exact, (H_xx, H_xy, H_yy))
    det_h = a * c - b * b
    abs_det_h = abs(det_h)
    if v != 0:
        abs_det_jac = v * v
        eliminated = ['H_xy', 'H_yy']
        free_residual = ['H_xx']
        elimination_branch = 'z2_nonzero'
    else:
        abs_det_jac = u * u
        eliminated = ['H_xx', 'H_xy']
        free_residual = ['H_yy']
        elimination_branch = 'z1_nonzero_z2_zero'
    reciprocal_jac = 1 / abs_det_jac
    algebraic_product = reciprocal_jac * abs_det_h
    powers = pin_centered_integrand_power_ledger(2)
    return {
        'object': 'RN-MESOSCOPIC-PIN-CENTERED-CONTACT-INTEGRAND-ALGEBRAIC-FACTOR-20260925-v1',
        'chart': 'C_pin_centered',
        'y': {'y1': exact(y[0]), 'y2': exact(y[1])},
        'z': {'z1': u, 'z2': v},
        'closer_pin': frame['closer_pin'],
        'H_xx': a,
        'H_xy': b,
        'H_yy': c,
        'det_H': det_h,
        'det_contact_leading_abs': abs_det_h,
        'abs_det_grad_contact_map': abs_det_jac,
        'reciprocal_grad_contact_jacobian': reciprocal_jac,
        'algebraic_jacobian_times_det_abs': algebraic_product,
        'product_minus_factors': algebraic_product - reciprocal_jac * abs_det_h,
        'eliminated_coordinates': eliminated,
        'free_residual_coordinates': free_residual,
        'elimination_branch': elimination_branch,
        'net_count_r_power': powers['net_count_r_power'],
        'hessian_det_leading_r_power': 0,
        'gradient_jacobian_r_power': 2,
        'contact_integrand_algebraic_factor_skeleton_enumerated': True,
        'pin_site_higher_jets_enumerated': False,
        'contact_gaussian_density_bounded': False,
        'conditioned_expectation_evaluated': False,
        'global_contact_density_bound_proved': False,
        'meaning': (
            'exact pin Morse product (1/|det J_grad|)·|det H|; '
            'Jacobian |det|=z2² (or z1² on axis); density / higher jets still unbound'
        ),
    }


def pin_centered_height_r_factor_ledger(
    y: Coord, *, inner: int | Q = Q(2, 5), outer: int | Q = 1,
    margin: int | Q = Q(1, 10),
    H_xx: int | Q = -1, H_xy: int | Q = 0, H_yy: int | Q = 1,
    f_xxx: int | Q = 0, f_xxy: int | Q = 0, f_xyy: int | Q = 0, f_yyy: int | Q = 6,
) -> dict:
    """Record unmatched height r^1 on C_pin_centered after Morse leading order.

    Leading Morse height satisfies J_height = (1/2) z · J_grad (dependent).
    Cubic H_height_next supplies an independent height observation and inserts
    unmatched density r^1. Does not absorb height-r or bound the contact density.
    Small-A diagnostic chart; higher pin jets remain separately open.
    """
    frame = pin_centered_frame(y, inner=inner, outer=outer, margin=margin)
    u, v = exact(frame['z1']), exact(frame['z2'])
    rows = pin_site_morse_contact_rows(u, v, H_xx=H_xx, H_xy=H_xy, H_yy=H_yy)
    nxt = pin_site_morse_next_order_rows(
        u, v, f_xxx=f_xxx, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    return {
        'object': 'RN-MESOSCOPIC-PIN-CENTERED-HEIGHT-R-FACTOR-20260925-v1',
        'chart': 'C_pin_centered',
        'y': {'y1': exact(y[0]), 'y2': exact(y[1])},
        'z': {'z1': u, 'z2': v},
        'closer_pin': frame['closer_pin'],
        'leading_height_dependent_on_grad': True,
        'height_dependency_factor_half': Q(1, 2),
        'J_height': rows['J_height'],
        'z_dot_J_grad': u * rows['J_grad_1'] + v * rows['J_grad_2'],
        'height_minus_half_z_dot_grad': rows['height_minus_half_z_dot_grad'],
        'H_height_next': nxt['H_height_next'],
        'z_dot_H_grad_next_minus_3_H_height_next': nxt['z_dot_H_grad_next_minus_3_H_height_next'],
        'next_order_supplies_independent_height': True,
        'unmatched_height_density_r_power': 1,
        'explicit_r_factor_still_required': True,
        'height_r_absorbed_into_uniform_bound': False,
        'pin_site_higher_jets_enumerated': False,
        'contact_gaussian_density_bounded': False,
        'meaning': (
            'leading Morse height is (1/2)z·J_grad; cubic H_height_next inserts '
            'unmatched r^1; not absorbed; density / higher jets still unbound'
        ),
    }


def pin_centered_algebraic_factor_times_height_r_skeleton(
    y: Coord, *, inner: int | Q = Q(2, 5), outer: int | Q = 1,
    margin: int | Q = Q(1, 10),
    H_xx: int | Q = -1, H_xy: int | Q = 0, H_yy: int | Q = 1,
    f_xxx: int | Q = 0, f_xxy: int | Q = 0, f_xyy: int | Q = 0, f_yyy: int | Q = 6,
) -> dict:
    """Combine pin Morse algebraic Jacobian×|det H| product with unmatched height r^1.

    Records the exact product identity
      (1/|det J_grad|)·|det H|
    together with the unmatched height density r-power 1 from cubic H_height_next.
    Neither factor is absorbed; contact Gaussian density / higher jets remain open.
    """
    alg = pin_centered_contact_integrand_algebraic_factor_skeleton(
        y, inner=inner, outer=outer, margin=margin,
        H_xx=H_xx, H_xy=H_xy, H_yy=H_yy,
    )
    height = pin_centered_height_r_factor_ledger(
        y, inner=inner, outer=outer, margin=margin,
        H_xx=H_xx, H_xy=H_xy, H_yy=H_yy,
        f_xxx=f_xxx, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    height_r = height['unmatched_height_density_r_power']
    product = alg['algebraic_jacobian_times_det_abs']
    return {
        'object': 'RN-MESOSCOPIC-PIN-CENTERED-ALGEBRAIC-FACTOR-TIMES-HEIGHT-R-20260925-v1',
        'chart': 'C_pin_centered',
        'y': alg['y'],
        'z': alg['z'],
        'closer_pin': alg['closer_pin'],
        'algebraic_jacobian_times_det_abs': product,
        'unmatched_height_density_r_power': height_r,
        'combined_skeleton_height_r_power': height_r,
        'algebraic_factor_r_power_after_stripping': 0,
        'product_minus_recorded_factors': product - alg['reciprocal_grad_contact_jacobian'] * alg['det_contact_leading_abs'],
        'H_height_next': height['H_height_next'],
        'elimination_branch': alg['elimination_branch'],
        'free_residual_coordinates': alg['free_residual_coordinates'],
        'combined_algebraic_factor_and_height_r_recorded': True,
        'height_r_absorbed_into_uniform_bound': False,
        'combined_skeleton_absorbed_into_uniform_bound': False,
        'pin_site_higher_jets_enumerated': False,
        'contact_gaussian_density_bounded': False,
        'conditioned_expectation_evaluated': False,
        'global_contact_density_bound_proved': False,
        'meaning': (
            'exact pin Morse (1/|det J|)·|det H| times unmatched height r^1; '
            'neither factor absorbed; density / higher jets still unbound'
        ),
    }


def contact_density_obstruction_inventory() -> dict:
    """Per-chart inventory of what is cleared vs still blocking γ_AB ≤ C r^(-d).

    Records exact boolean status only; does not prove any density bound.
    """
    return {
        'object': 'RN-MESOSCOPIC-CONTACT-DENSITY-OBSTRUCTION-20260925-v1',
        'target': 'gamma_AB_le_C_r_to_minus_d',
        'global_contact_density_bound_proved': False,
        'charts': {
            'C_transverse': {
                'chart_conditioning_singularity_cleared': True,
                'integrand_power_identity_recorded': True,
                'height_r_factor_absorbed': False,
                'free_jet_residual_inventory_recorded': True,
                'gradient_contact_jacobian_enumerated': True,
                'conditioned_hessian_residual_polynomials_enumerated': True,
                'conditioned_hessian_det_skeleton_enumerated': True,
                'contact_integrand_algebraic_factor_skeleton_enumerated': True,
                'height_residual_after_grad_contact_enumerated': True,
                'algebraic_factor_times_height_r_skeleton_enumerated': True,
                'hessian_conditioned_expectation_evaluated': False,
                'contact_gaussian_density_bounded': False,
            },
            'C_axial': {
                'chart_conditioning_singularity_cleared': True,
                'integrand_power_identity_recorded': True,
                'area_measure_zero_in_2d': True,
                'free_jet_residual_inventory_recorded': True,
                'gradient_contact_jacobian_enumerated': True,
                'conditioned_hessian_residual_polynomials_enumerated': True,
                'conditioned_hessian_det_skeleton_enumerated': True,
                'contact_integrand_algebraic_factor_skeleton_enumerated': True,
                'height_independent_at_leading_axial_order': True,
                'no_unmatched_height_r_at_leading_order': True,
                'height_grad_x_shared_mark_identity_recorded': True,
                'hessian_conditioned_expectation_evaluated': False,
                'contact_gaussian_density_bounded': False,
            },
            'C_thin_belt': {
                'bare_1_over_abs_y2_L1': False,
                'jet_map_pointwise_cancel_recorded': True,
                'bare_reciprocal_L1_obstruction_cleared_by_cancel': True,
                'residual_geometric_factor_locally_L1': True,
                'contact_integrand_algebraic_factor_skeleton_enumerated': True,
                'height_r_factor_recorded': True,
                'height_r_factor_absorbed': False,
                'algebraic_factor_times_height_r_skeleton_enumerated': True,
                'uniform_integrand_bound_proved': False,
                'contact_gaussian_density_bounded': False,
            },
            'C_pin_centered': {
                'leading_morse_rows_enumerated': True,
                'cubic_next_order_enumerated': True,
                'quartic_next_order_enumerated': True,
                'quintic_next_order_enumerated': True,
                'sextic_next_order_enumerated': True,
                'septic_next_order_enumerated': True,
                'octic_next_order_enumerated': True,
                'nonic_next_order_enumerated': True,
                'decic_next_order_enumerated': True,
                'undecic_next_order_enumerated': True,
                'dodecic_next_order_enumerated': True,
                'tridecic_next_order_enumerated': True,
                'tetradecic_next_order_enumerated': True,
                'pentadecic_next_order_enumerated': True,
                'hexadecic_next_order_enumerated': True,
                'unmatched_height_r_power_inventory_recorded': True,
                'free_jet_residual_inventory_recorded': True,
                'gradient_contact_jacobian_enumerated': True,
                'max_saddle_signature_test_recorded': True,
                'integrand_power_identity_recorded': True,
                'contact_integrand_algebraic_factor_skeleton_enumerated': True,
                'height_r_factor_recorded': True,
                'height_r_factor_absorbed': False,
                'algebraic_factor_times_height_r_skeleton_enumerated': True,
                'seventeenth_and_higher_jets_enumerated': False,
                'contact_gaussian_density_bounded': False,
            },
        },
        'open_blockers': [
            'contact_gaussian_density_factor',
            'conditioned_hessian_expectation',
            'thin_belt_contact_gaussian_density_near_y2_0',
            'transverse_height_r_absorption',
            'thin_belt_height_r_absorption',
            'pin_seventeenth_and_higher_jets',
            'pin_centered_height_r_absorption',
        ],
        'meaning': (
            'inventory only: chart singularities cleared on C_transverse/C_axial; '
            'thin-belt bare reciprocal L1 cleared by jet-map cancel; Gaussian density / '
            'Hessian expectation / height-r / higher pin jets remain open blockers'
        ),
    }


def transverse_free_jet_residual_inventory(y: Coord) -> dict:
    """Exact free-jet residual count on C_transverse after leading gradient contact.

    Leading gradient map on coordinates (f_yy, k, f_xxy, f_xyy):
      J_y = y2 · f_yy
      J_x = 6 y1^2 · k + y1 y2 · f_xxy + (y2^2)/2 · f_xyy
    With |y2|≥δ the map has rank 2, so 4−2=2 free directions remain among those
    coordinates; f_yyy is absent from leading gradient rows. Does not bound the
    contact Gaussian density or evaluate the conditioned Hessian expectation.
    """
    if not transverse_chart_ok(y):
        raise ValueError('point outside C_transverse chart')
    y1, y2 = y
    grad_coords = ('f_yy', 'k', 'f_xxy', 'f_xyy')
    # Case split on which second-row coefficients are nonzero (exact; y2≠0 here).
    if y1 == 0:
        second_row_isolates = 'f_xyy'
        free_among = ['k', 'f_xxy']
    else:
        # 6 y1^2 ≠ 0: k appears; residual free plane in (k, f_xxy, f_xyy) has dim 2.
        second_row_isolates = 'linear_form_on_k_f_xxy_f_xyy'
        free_among = ['residual_codim1_subspace_of_k_f_xxy_f_xyy']
    free_count = len(grad_coords) - 2
    return {
        'object': 'RN-MESOSCOPIC-TRANSVERSE-FREE-JET-RESIDUAL-20260925-v1',
        'chart': 'C_transverse',
        'leading_grad_jet_coordinates': list(grad_coords),
        'leading_grad_observation_count': 2,
        'leading_grad_map_rank': 2,
        'free_directions_after_grad_contact': free_count,
        'grad_y_isolates_f_yy': True,
        'grad_y_coefficient_f_yy': y2,
        'grad_x_coefficient_k': 6 * y1 * y1,
        'grad_x_coefficient_f_xxy': y1 * y2,
        'grad_x_coefficient_f_xyy': (y2 * y2) / 2,
        'grad_x_second_row_isolates': second_row_isolates,
        'free_among_leading_grad_coords': free_among,
        'f_yyy_absent_from_leading_grad_rows': True,
        'height_independent_at_leading_order': False,
        'hessian_entries_polynomials_in_same_jets': True,
        'contact_gaussian_density_bounded': False,
        'conditioned_hessian_expectation_evaluated': False,
        'meaning': (
            'rank-2 leading gradient contact on 4 jet coords leaves 2 free '
            'directions plus f_yyy; not a Gaussian density bound'
        ),
    }


def axial_free_jet_residual_inventory(y: Coord) -> dict:
    """Exact free-jet residual count on C_axial after leading gradient contact.

    Axial leading rows (y2=0, |y1|≥A):
      J_grad_y = (y1^2 / 2) f_xxy
      J_grad_x = 6 k y1^2
    so f_xxy and k are isolated when y1≠0. Among displayed leftovers
    (f_yy, f_xyy, f_yyy) all three remain free at this order. Area-measure zero
    in the 2D annulus; density still unbound.
    """
    if not axial_chart_ok(y):
        raise ValueError('point outside C_axial chart')
    y1, y2 = y
    return {
        'object': 'RN-MESOSCOPIC-AXIAL-FREE-JET-RESIDUAL-20260925-v1',
        'chart': 'C_axial',
        'leading_grad_jet_coordinates': ['f_xxy', 'k'],
        'leading_grad_observation_count': 2,
        'leading_grad_map_rank': 2,
        'free_directions_after_grad_contact': 0,
        'grad_y_isolates_f_xxy': True,
        'grad_x_isolates_k': True,
        'grad_y_coefficient_f_xxy': (y1 * y1) / 2,
        'grad_x_coefficient_k': 6 * y1 * y1,
        'y2_is_zero': y2 == 0,
        'free_hessian_height_jet_coords': ['f_yy', 'f_xyy', 'f_yyy'],
        'axial_area_measure_zero': True,
        'contact_gaussian_density_bounded': False,
        'conditioned_hessian_expectation_evaluated': False,
        'meaning': (
            'axial leading gradient isolates f_xxy and k; f_yy/f_xyy/f_yyy remain '
            'for Hessian/height; not a Gaussian density bound'
        ),
    }


def pin_centered_free_jet_residual_inventory(
    y: Coord, *, inner: int | Q = Q(2, 5), outer: int | Q = 1,
    margin: int | Q = Q(1, 10),
) -> dict:
    """Exact free-jet residual count on C_pin_centered after Morse gradient contact.

    Leading Morse map on Hessian coordinates (H_xx, H_xy, H_yy):
      J_grad = H_pin · z
    so two linear observations on three Hessian entries. When z≠0 the map has
    rank 2 and leaves exactly one free Hessian direction (H_xx if z2≠0, else
    H_yy). Cubic-and-higher pin jets remain free for height residuals. Small-A
    diagnostic chart; does not bound the contact Gaussian density.
    """
    frame = pin_centered_frame(y, inner=inner, outer=outer, margin=margin)
    u, v = exact(frame['z1']), exact(frame['z2'])
    if u == 0 and v == 0:
        raise ValueError('pin free-jet residual requires z != 0')
    hess_coords = ('H_xx', 'H_xy', 'H_yy')
    if v != 0:
        eliminated = ['H_xy', 'H_yy']
        free_among = ['H_xx']
        elimination_branch = 'z2_nonzero'
        abs_det_jac = v * v
    else:
        eliminated = ['H_xx', 'H_xy']
        free_among = ['H_yy']
        elimination_branch = 'z1_nonzero_z2_zero'
        abs_det_jac = u * u
    return {
        'object': 'RN-MESOSCOPIC-PIN-CENTERED-FREE-JET-RESIDUAL-20260925-v1',
        'chart': 'C_pin_centered',
        'y': {'y1': exact(y[0]), 'y2': exact(y[1])},
        'z': {'z1': u, 'z2': v},
        'closer_pin': frame['closer_pin'],
        'leading_grad_jet_coordinates': list(hess_coords),
        'leading_grad_observation_count': 2,
        'leading_grad_map_rank': 2,
        'free_directions_after_grad_contact': 1,
        'eliminated_coordinates': eliminated,
        'free_among_leading_grad_coords': free_among,
        'elimination_branch': elimination_branch,
        'abs_det_grad_contact_map': abs_det_jac,
        'higher_pin_jets_free_for_height_residuals': True,
        'height_independent_at_leading_morse_order': False,
        'pin_site_higher_jets_enumerated': False,
        'contact_gaussian_density_bounded': False,
        'conditioned_hessian_expectation_evaluated': False,
        'meaning': (
            'rank-2 Morse gradient contact on 3 Hessian coords leaves 1 free '
            'direction; higher jets / density still unbound'
        ),
    }


def contact_free_jet_residual_inventory(
    *, transverse_y: Coord | None = None, axial_y: Coord | None = None,
    pin_y: Coord | None = None,
) -> dict:
    """Bundle transverse/axial/pin free-jet residual inventories; density still open."""
    t = transverse_free_jet_residual_inventory(transverse_y or point(0, 2))
    a = axial_free_jet_residual_inventory(axial_y or point(2, 0))
    p = pin_centered_free_jet_residual_inventory(
        pin_y or point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1)
    return {
        'object': 'RN-MESOSCOPIC-CONTACT-FREE-JET-RESIDUAL-20260925-v1',
        'C_transverse': t,
        'C_axial': a,
        'C_pin_centered': p,
        'global_contact_density_bound_proved': False,
        'meaning': (
            'exact free-jet residual counts after leading gradient contact '
            '(transverse/axial/pin); prerequisite inventory only — does not '
            'bound the contact density'
        ),
    }


def transverse_gradient_contact_jacobian_ledger(y: Coord) -> dict:
    """Exact |det| of the leading gradient map on eliminated coords (f_yy, f_xyy).

    Treating free residuals (k, f_xxy) as parameters,
      J_grad_y = y2 · f_yy
      J_grad_x = 6k y1^2 + f_xxy y1 y2 + (y2^2)/2 · f_xyy
    the Jacobian matrix ∂(J_y,J_x)/∂(f_yy,f_xyy) is diagonal with entries
    (y2, y2^2/2), so
      |det| = |y2|^3 / 2.
    On C_transverse (|y2|≥δ) this is ≥ δ^3/2 > 0. Algebraic density-shape
    factor only; does not bound the Gaussian density of free residuals.
    """
    if not transverse_chart_ok(y):
        raise ValueError('point outside C_transverse chart')
    y1, y2 = y
    abs_y2 = abs(y2)
    det_abs = (abs_y2 ** 3) / 2
    return {
        'object': 'RN-MESOSCOPIC-TRANSVERSE-GRADIENT-CONTACT-JACOBIAN-20260925-v1',
        'chart': 'C_transverse',
        'eliminated_coordinates': ['f_yy', 'f_xyy'],
        'free_residual_coordinates': ['k', 'f_xxy'],
        'partial_J_y_partial_f_yy': y2,
        'partial_J_x_partial_f_xyy': (y2 * y2) / 2,
        'jacobian_matrix_diagonal': True,
        'abs_det_grad_contact_map': det_abs,
        'abs_y2': abs_y2,
        'contact_gaussian_density_bounded': False,
        'meaning': (
            'exact |det ∂(J_y,J_x)/∂(f_yy,f_xyy)| = |y2|^3/2; algebraic density '
            'shape only — free-jet Gaussian density unbound'
        ),
    }


def transverse_gradient_contact_jacobian_ledger_with_floor(
    y: Coord, *, floor_y2: int | Q = Q(1, 4),
) -> dict:
    """As transverse_gradient_contact_jacobian_ledger, plus chart lower bound δ^3/2."""
    delta = exact(floor_y2)
    if delta <= 0:
        raise ValueError('positive floor required')
    if not transverse_chart_ok(y, floor_y2=delta):
        raise ValueError('point outside C_transverse chart')
    led = transverse_gradient_contact_jacobian_ledger(y)
    lower = (delta ** 3) / 2
    led['floor_y2'] = delta
    led['lower_bound_on_chart_abs_det'] = lower
    led['abs_det_ge_chart_lower_bound'] = led['abs_det_grad_contact_map'] >= lower
    return led


def axial_gradient_contact_jacobian_ledger(y: Coord) -> dict:
    """Exact |det| of the axial leading gradient map on (f_xxy, k).

      J_grad_y = (y1^2 / 2) f_xxy
      J_grad_x = 6 k y1^2
    so ∂(J_y,J_x)/∂(f_xxy,k) has |det| = |(y1^2/2)·(6 y1^2)| = 3 |y1|^4.
    Area-measure zero in 2D; density still unbound.
    """
    if not axial_chart_ok(y):
        raise ValueError('point outside C_axial chart')
    y1, y2 = y
    abs_y1 = abs(y1)
    det_abs = 3 * (abs_y1 ** 4)
    return {
        'object': 'RN-MESOSCOPIC-AXIAL-GRADIENT-CONTACT-JACOBIAN-20260925-v1',
        'chart': 'C_axial',
        'eliminated_coordinates': ['f_xxy', 'k'],
        'free_residual_coordinates': ['f_yy', 'f_xyy', 'f_yyy'],
        'partial_J_y_partial_f_xxy': (y1 * y1) / 2,
        'partial_J_x_partial_k': 6 * y1 * y1,
        'abs_det_grad_contact_map': det_abs,
        'abs_y1': abs_y1,
        'axial_area_measure_zero': True,
        'contact_gaussian_density_bounded': False,
        'meaning': (
            'exact |det ∂(J_y,J_x)/∂(f_xxy,k)| = 3|y1|^4; algebraic density shape '
            'only — free-jet Gaussian density unbound'
        ),
    }


def pin_centered_gradient_contact_jacobian_ledger(
    y: Coord, *, inner: int | Q = Q(2, 5), outer: int | Q = 1,
    margin: int | Q = Q(1, 10),
) -> dict:
    """Exact |det| of the pin Morse gradient map on eliminated Hessian coords.

    Leading Morse contact J_grad = H_pin · z:
      J1 = H_xx z1 + H_xy z2
      J2 = H_xy z1 + H_yy z2
    With z2≠0 eliminate (H_xy, H_yy) treating H_xx free:
      ∂(J1,J2)/∂(H_xy,H_yy) = [[z2, 0], [z1, z2]] ⇒ |det| = z2².
    With z2=0 and z1≠0 eliminate (H_xx, H_xy):
      ∂(J1,J2)/∂(H_xx,H_xy) = diag(z1, z1) ⇒ |det| = z1².
    Algebraic density-shape factor only; free-jet Gaussian density unbound.
    Small-A diagnostic chart.
    """
    frame = pin_centered_frame(y, inner=inner, outer=outer, margin=margin)
    u, v = exact(frame['z1']), exact(frame['z2'])
    if u == 0 and v == 0:
        raise ValueError('pin gradient-contact Jacobian requires z != 0')
    if v != 0:
        eliminated = ['H_xy', 'H_yy']
        free_residual = ['H_xx']
        elimination_branch = 'z2_nonzero'
        abs_det_jac = v * v
        jacobian_matrix_diagonal = False
        partials = {
            'partial_J1_partial_H_xy': v,
            'partial_J1_partial_H_yy': 0,
            'partial_J2_partial_H_xy': u,
            'partial_J2_partial_H_yy': v,
        }
    else:
        eliminated = ['H_xx', 'H_xy']
        free_residual = ['H_yy']
        elimination_branch = 'z1_nonzero_z2_zero'
        abs_det_jac = u * u
        jacobian_matrix_diagonal = True
        partials = {
            'partial_J1_partial_H_xx': u,
            'partial_J1_partial_H_xy': 0,
            'partial_J2_partial_H_xx': 0,
            'partial_J2_partial_H_xy': u,
        }
    return {
        'object': 'RN-MESOSCOPIC-PIN-CENTERED-GRADIENT-CONTACT-JACOBIAN-20260925-v1',
        'chart': 'C_pin_centered',
        'y': {'y1': exact(y[0]), 'y2': exact(y[1])},
        'z': {'z1': u, 'z2': v},
        'closer_pin': frame['closer_pin'],
        'eliminated_coordinates': eliminated,
        'free_residual_coordinates': free_residual,
        'elimination_branch': elimination_branch,
        'jacobian_matrix_diagonal': jacobian_matrix_diagonal,
        'abs_det_grad_contact_map': abs_det_jac,
        'contact_gaussian_density_bounded': False,
        'global_contact_density_bound_proved': False,
        'meaning': (
            'exact |det ∂(J1,J2)/∂(eliminated Hessian)| = z2² (or z1² on axis); '
            'algebraic density shape only — free-jet Gaussian density unbound'
        ),
        **partials,
    }


def contact_gradient_jacobian_density_shape_inventory(
    *, transverse_y: Coord | None = None, axial_y: Coord | None = None,
    pin_y: Coord | None = None,
) -> dict:
    """Bundle exact gradient-contact Jacobians; density bound still open."""
    t = transverse_gradient_contact_jacobian_ledger_with_floor(
        transverse_y or point(0, 2),
    )
    a = axial_gradient_contact_jacobian_ledger(axial_y or point(2, 0))
    p = pin_centered_gradient_contact_jacobian_ledger(
        pin_y or point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1)
    return {
        'object': 'RN-MESOSCOPIC-CONTACT-GRADIENT-JACOBIAN-DENSITY-SHAPE-20260925-v1',
        'C_transverse': t,
        'C_axial': a,
        'C_pin_centered': p,
        'global_contact_density_bound_proved': False,
        'meaning': (
            'exact algebraic |det| factors for leading gradient contact maps '
            '(transverse/axial/pin); does not bound the contact Gaussian density'
        ),
    }


def transverse_conditioned_hessian_residual_ledger(
    y: Coord, *, gap_mark: int | Q = 1,
    f_yy: int | Q = 1, f_xxy: int | Q = 0, f_xyy: int | Q = 0, f_yyy: int | Q = 0,
) -> dict:
    """Express transverse Hessian contact entries in (J_grad, k, f_xxy) residuals.

    Eliminate f_yy and f_xyy via leading gradient contact (y2≠0):
      f_yy  = J_grad_y / y2
      f_xyy = (2/y2^2) (J_grad_x − 6k y1^2 − f_xxy y1 y2)
    Free residual coordinates among the four leading-grad jets: (k, f_xxy).
    Then
      H_yy = J_grad_y / y2
      H_xx = 12 k y1 + f_xxy y2
      H_xy = 2 J_grad_x / y2 − 12 k y1^2 / y2 − f_xxy y1
    Exact polynomial identities only; conditioned Gaussian expectation stays open.
    """
    if not transverse_chart_ok(y):
        raise ValueError('point outside C_transverse chart')
    y1, y2 = y
    k = exact(gap_mark)
    a, b, c, d = map(exact, (f_yy, f_xxy, f_xyy, f_yyy))
    if k <= 0:
        raise ValueError('positive gap mark required')
    rows = contact_rows(y, gap_mark=k, f_yy=a, f_xxy=b, f_xyy=c, f_yyy=d)
    jy, jx = rows['J_grad_y'], rows['J_grad_x']
    f_yy_from_jy = jy / y2
    f_xyy_from_jx = (2 / (y2 * y2)) * (jx - 6 * k * y1 * y1 - b * y1 * y2)
    h_yy = f_yy_from_jy
    h_xx = 12 * k * y1 + b * y2
    h_xy = (2 * jx) / y2 - (12 * k * y1 * y1) / y2 - b * y1
    raw = hessian_contact_rows(y, gap_mark=k, f_yy=a, f_xxy=b, f_xyy=c, f_yyy=d)
    return {
        'object': 'RN-MESOSCOPIC-TRANSVERSE-CONDITIONED-HESSIAN-RESIDUAL-20260925-v1',
        'chart': 'C_transverse',
        'y': {'y1': y1, 'y2': y2},
        'free_residual_coordinates': ['k', 'f_xxy'],
        'eliminated_by_grad_contact': ['f_yy', 'f_xyy'],
        'J_grad_y': jy,
        'J_grad_x': jx,
        'f_yy_from_J_grad_y': f_yy_from_jy,
        'f_xyy_from_J_grad_x': f_xyy_from_jx,
        'f_yy_minus_solved': a - f_yy_from_jy,
        'f_xyy_minus_solved': c - f_xyy_from_jx,
        'H_xx_residual': h_xx,
        'H_xy_residual': h_xy,
        'H_yy_residual': h_yy,
        'H_xx_minus_raw': h_xx - raw['H_xx_contact'],
        'H_xy_minus_raw': h_xy - raw['H_xy_contact'],
        'H_yy_minus_raw': h_yy - raw['H_yy_contact'],
        'det_contact_leading_residual': h_xx * h_yy,
        'det_xy_square_residual': h_xy * h_xy,
        'conditioned_hessian_residual_polynomials_enumerated': True,
        'conditioned_expectation_evaluated': False,
        'contact_gaussian_density_bounded': False,
        'hessian_ledger_evaluated': False,
        'meaning': (
            'exact residual Hessian polynomials after eliminating f_yy,f_xyy; '
            'not a conditioned Gaussian expectation of |det H|'
        ),
    }


def transverse_conditioned_det_free_jet_skeleton(
    y: Coord, *, gap_mark: int | Q = 1,
    f_yy: int | Q = 1, f_xxy: int | Q = 0, f_xyy: int | Q = 0, f_yyy: int | Q = 0,
) -> dict:
    """Exact linear skeleton of leading det H on free residual jets (C_transverse).

    After eliminating f_yy,f_xyy, the leading contact determinant factors as
      det_contact_leading = H_xx · H_yy
        = (12 k y1 + f_xxy y2) · (J_grad_y / y2)
        = α_k · k + α_f_xxy · f_xxy
    with observed coefficients
      α_k = 12 y1 J_grad_y / y2,   α_f_xxy = J_grad_y.
    Degree 1 in free residuals (k, f_xxy). Does not evaluate the conditioned
    Gaussian expectation of |det H|.
    """
    if not transverse_chart_ok(y):
        raise ValueError('point outside C_transverse chart')
    y1, y2 = y
    resid = transverse_conditioned_hessian_residual_ledger(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    jy = resid['J_grad_y']
    k = exact(gap_mark)
    b = exact(f_xxy)
    alpha_k = (12 * y1 * jy) / y2
    alpha_f = jy
    det_from_alphas = alpha_k * k + alpha_f * b
    return {
        'object': 'RN-MESOSCOPIC-TRANSVERSE-CONDITIONED-DET-FREE-JET-SKELETON-20260925-v1',
        'chart': 'C_transverse',
        'y': {'y1': y1, 'y2': y2},
        'free_residual_coordinates': ['k', 'f_xxy'],
        'eliminated_by_grad_contact': ['f_yy', 'f_xyy'],
        'J_grad_y': jy,
        'alpha_k': alpha_k,
        'alpha_f_xxy': alpha_f,
        'det_contact_leading_from_alphas': det_from_alphas,
        'det_contact_leading_residual': resid['det_contact_leading_residual'],
        'det_minus_alpha_form': det_from_alphas - resid['det_contact_leading_residual'],
        'free_jet_polynomial_degree': 1,
        'linear_in_free_residuals': True,
        'conditioned_hessian_det_skeleton_enumerated': True,
        'conditioned_expectation_evaluated': False,
        'contact_gaussian_density_bounded': False,
        'hessian_ledger_evaluated': False,
        'meaning': (
            'exact linear form det=α_k·k+α_f_xxy·f_xxy after grad contact; '
            'not a conditioned Gaussian expectation of |det H|'
        ),
    }


def axial_conditioned_det_free_jet_skeleton(
    y: Coord, *, gap_mark: int | Q = 1,
    f_yy: int | Q = 1, f_xxy: int | Q = 1, f_xyy: int | Q = 0, f_yyy: int | Q = 0,
) -> dict:
    """Exact linear skeleton of leading det H on free residual jets (C_axial).

    After isolating k,f_xxy, H_xx and H_xy are observed from gradient contact while
    H_yy = f_yy stays free:
      det_contact_leading = H_xx · H_yy = (2 J_grad_x / y1) · f_yy = α_f_yy · f_yy
    with α_f_yy = 2 J_grad_x / y1 = 12 k y1. Degree 1 in free residual f_yy.
    Area-measure zero; expectation still open.
    """
    if not axial_chart_ok(y):
        raise ValueError('point outside C_axial chart')
    y1, y2 = y
    resid = axial_conditioned_hessian_residual_ledger(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    a = exact(f_yy)
    alpha_fyy = resid['H_xx_from_J_grad_x']
    det_from_alpha = alpha_fyy * a
    return {
        'object': 'RN-MESOSCOPIC-AXIAL-CONDITIONED-DET-FREE-JET-SKELETON-20260925-v1',
        'chart': 'C_axial',
        'y': {'y1': y1, 'y2': y2},
        'free_residual_coordinates': ['f_yy', 'f_xyy', 'f_yyy'],
        'isolated_by_grad_contact': ['k', 'f_xxy'],
        'leading_det_depends_on_free': ['f_yy'],
        'alpha_f_yy': alpha_fyy,
        'det_contact_leading_from_alpha': det_from_alpha,
        'det_contact_leading_residual': resid['det_contact_leading_residual'],
        'det_minus_alpha_form': det_from_alpha - resid['det_contact_leading_residual'],
        'free_jet_polynomial_degree': 1,
        'linear_in_free_residuals': True,
        'axial_area_measure_zero': True,
        'conditioned_hessian_det_skeleton_enumerated': True,
        'conditioned_expectation_evaluated': False,
        'contact_gaussian_density_bounded': False,
        'hessian_ledger_evaluated': False,
        'meaning': (
            'exact axial form det=α_f_yy·f_yy after isolating k,f_xxy; '
            'not a conditioned Gaussian expectation'
        ),
    }


def contact_conditioned_det_free_jet_skeleton_inventory(
    *, transverse_y: Coord | None = None, axial_y: Coord | None = None,
) -> dict:
    """Bundle transverse/axial conditioned det free-jet skeletons (expectation open)."""
    ty = transverse_y if transverse_y is not None else point(0, 2)
    ay = axial_y if axial_y is not None else point(2, 0)
    return {
        'object': 'RN-MESOSCOPIC-CONTACT-CONDITIONED-DET-FREE-JET-SKELETON-20260925-v1',
        'C_transverse': transverse_conditioned_det_free_jet_skeleton(
            ty, gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4),
        'C_axial': axial_conditioned_det_free_jet_skeleton(
            ay, gap_mark=1, f_yy=2, f_xxy=3),
        'global_contact_density_bound_proved': False,
        'conditioned_expectation_evaluated': False,
        'meaning': (
            'exact free-jet linear skeletons for leading det H after grad contact; '
            'does not evaluate conditioned Gaussian expectations'
        ),
    }


def transverse_contact_integrand_algebraic_factor_skeleton(
    y: Coord, *, gap_mark: int | Q = 1,
    f_yy: int | Q = 1, f_xxy: int | Q = 0, f_xyy: int | Q = 0, f_yyy: int | Q = 0,
) -> dict:
    """Exact algebraic product of transverse Kac–Rice contact factors (density open).

    On C_transverse the contact integrand factors (after stripping exact r-powers)
    as the product of:
      1/|det ∂(J_y,J_x)/∂(f_yy,f_xyy)|   =  2/|y2|^3
      |det H|_contact leading skeleton   =  |α_k·k + α_f_xxy·f_xxy|
      unmatched height r^1 from H_height_next residual
    Times an unevaluated free-jet Gaussian density. This ledger records the exact
    reciprocal Jacobian and det skeleton factors and their product identity; it
    does not bound the Gaussian density or absorb height-r.
    """
    if not transverse_chart_ok(y):
        raise ValueError('point outside C_transverse chart')
    jac = transverse_gradient_contact_jacobian_ledger(y)
    det = transverse_conditioned_det_free_jet_skeleton(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    height = transverse_height_residual_after_grad_contact(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    powers = contact_integrand_power_ledger(2, chart='C_transverse')
    abs_det_jac = jac['abs_det_grad_contact_map']
    reciprocal_jac = 1 / abs_det_jac
    abs_det_h = abs(det['det_contact_leading_from_alphas'])
    algebraic_product = reciprocal_jac * abs_det_h
    return {
        'object': 'RN-MESOSCOPIC-TRANSVERSE-CONTACT-INTEGRAND-ALGEBRAIC-FACTOR-20260925-v1',
        'chart': 'C_transverse',
        'y': {'y1': y[0], 'y2': y[1]},
        'abs_det_grad_contact_map': abs_det_jac,
        'reciprocal_grad_contact_jacobian': reciprocal_jac,
        'det_contact_leading_abs': abs_det_h,
        'algebraic_jacobian_times_det_abs': algebraic_product,
        'product_minus_factors': algebraic_product - reciprocal_jac * abs_det_h,
        'unmatched_height_density_r_power': height['unmatched_height_density_r_power'],
        'H_height_next_residual': height['H_height_next_residual'],
        'net_count_r_power': powers['net_count_r_power'],
        'free_residual_coordinates': ['k', 'f_xxy'],
        'contact_integrand_algebraic_factor_skeleton_enumerated': True,
        'contact_gaussian_density_bounded': False,
        'conditioned_expectation_evaluated': False,
        'height_r_absorbed_into_uniform_bound': False,
        'global_contact_density_bound_proved': False,
        'meaning': (
            'exact product (1/|det J_grad|)·|det H_skeleton| after grad contact; '
            'Gaussian density / height-r absorption / expectation remain open'
        ),
    }



def transverse_algebraic_factor_times_height_r_skeleton(
    y: Coord, *, gap_mark: int | Q = 1,
    f_yy: int | Q = 1, f_xxy: int | Q = 0, f_xyy: int | Q = 0, f_yyy: int | Q = 0,
) -> dict:
    """Combine transverse algebraic Jacobian×|det H| product with unmatched height r^1.

    Records the exact product identity
      (1/|det J_grad|)·|det H_skeleton|
    together with the unmatched height density r-power 1 from H_height_next.
    The combined skeleton is not absorbed into a uniform integrand bound; the
    contact Gaussian density remains open.
    """
    if not transverse_chart_ok(y):
        raise ValueError('point outside C_transverse chart')
    alg = transverse_contact_integrand_algebraic_factor_skeleton(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    height_r = alg['unmatched_height_density_r_power']
    product = alg['algebraic_jacobian_times_det_abs']
    return {
        'object': 'RN-MESOSCOPIC-TRANSVERSE-ALGEBRAIC-FACTOR-TIMES-HEIGHT-R-20260925-v1',
        'chart': 'C_transverse',
        'y': {'y1': y[0], 'y2': y[1]},
        'algebraic_jacobian_times_det_abs': product,
        'unmatched_height_density_r_power': height_r,
        'combined_skeleton_height_r_power': height_r,
        'algebraic_factor_r_power_after_stripping': 0,
        'product_minus_recorded_factors': product - alg['reciprocal_grad_contact_jacobian'] * alg['det_contact_leading_abs'],
        'H_height_next_residual': alg['H_height_next_residual'],
        'free_residual_coordinates': ['k', 'f_xxy'],
        'combined_algebraic_factor_and_height_r_recorded': True,
        'height_r_absorbed_into_uniform_bound': False,
        'combined_skeleton_absorbed_into_uniform_bound': False,
        'contact_gaussian_density_bounded': False,
        'conditioned_expectation_evaluated': False,
        'global_contact_density_bound_proved': False,
        'meaning': (
            'exact (1/|det J|)·|det H| times unmatched height r^1 skeleton; '
            'neither factor absorbed; Gaussian density still unbound'
        ),
    }


def thin_belt_algebraic_factor_times_height_r_skeleton(
    y: Coord, *, gap_mark: int | Q = 1,
    f_yy: int | Q = 1, f_xxy: int | Q = 0, f_xyy: int | Q = 0, f_yyy: int | Q = 0,
    floor_y2: int | Q = Q(1, 4),
) -> dict:
    """Combine thin-belt algebraic Jacobian×|det H| product with unmatched height r^1.

    Records the exact product identity
      (1/|det J_grad|)·|det H_skeleton|
    together with the unmatched height density r-power 1 (shared transverse
    height–grad_y dependence). Reciprocal still diverges as y2→0; neither the
    algebraic factor nor height-r is absorbed; contact Gaussian density open.
    """
    if not thin_belt_ok(y, floor_y2=floor_y2):
        raise ValueError('point outside thin belt')
    alg = thin_belt_contact_integrand_algebraic_factor_skeleton(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
        floor_y2=floor_y2,
    )
    height = thin_belt_height_r_factor_ledger(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
        floor_y2=floor_y2,
    )
    height_r = height['unmatched_height_density_r_power']
    product = alg['algebraic_jacobian_times_det_abs']
    return {
        'object': 'RN-MESOSCOPIC-THIN-BELT-ALGEBRAIC-FACTOR-TIMES-HEIGHT-R-20260925-v1',
        'chart': 'C_thin_belt',
        'y': {'y1': y[0], 'y2': y[1]},
        'floor_y2': exact(floor_y2),
        'algebraic_jacobian_times_det_abs': product,
        'unmatched_height_density_r_power': height_r,
        'combined_skeleton_height_r_power': height_r,
        'algebraic_factor_r_power_after_stripping': 0,
        'product_minus_recorded_factors': product - alg['reciprocal_grad_contact_jacobian'] * alg['det_contact_leading_abs'],
        'H_height_next': height['H_height_next'],
        'reciprocal_diverges_as_y2_to_0': True,
        'free_residual_coordinates': ['k', 'f_xxy'],
        'bare_reciprocal_L1_obstruction_cleared_by_cancel': True,
        'combined_algebraic_factor_and_height_r_recorded': True,
        'height_r_absorbed_into_uniform_bound': False,
        'combined_skeleton_absorbed_into_uniform_bound': False,
        'uniform_integrand_bound_proved': False,
        'contact_gaussian_density_bounded': False,
        'conditioned_expectation_evaluated': False,
        'global_contact_density_bound_proved': False,
        'meaning': (
            'exact thin-belt (1/|det J|)·|det H| times unmatched height r^1; '
            'reciprocal diverges as y2→0; neither factor absorbed; density unbound'
        ),
    }


def axial_contact_integrand_algebraic_factor_skeleton(
    y: Coord, *, gap_mark: int | Q = 1,
    f_yy: int | Q = 1, f_xxy: int | Q = 1, f_xyy: int | Q = 0, f_yyy: int | Q = 0,
) -> dict:
    """Exact algebraic product of axial Kac–Rice contact factors (area-measure zero).

    Axial factors:
      1/|det ∂(J_y,J_x)/∂(f_xxy,k)| = 1/(3|y1|^4)
      |det H|_contact leading       = |α_f_yy · f_yy|
    Product identity only; density / expectation open; area-measure zero.
    """
    if not axial_chart_ok(y):
        raise ValueError('point outside C_axial chart')
    jac = axial_gradient_contact_jacobian_ledger(y)
    det = axial_conditioned_det_free_jet_skeleton(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    powers = contact_integrand_power_ledger(2, chart='C_axial')
    abs_det_jac = jac['abs_det_grad_contact_map']
    reciprocal_jac = 1 / abs_det_jac
    abs_det_h = abs(det['det_contact_leading_from_alpha'])
    algebraic_product = reciprocal_jac * abs_det_h
    return {
        'object': 'RN-MESOSCOPIC-AXIAL-CONTACT-INTEGRAND-ALGEBRAIC-FACTOR-20260925-v1',
        'chart': 'C_axial',
        'y': {'y1': y[0], 'y2': y[1]},
        'abs_det_grad_contact_map': abs_det_jac,
        'reciprocal_grad_contact_jacobian': reciprocal_jac,
        'det_contact_leading_abs': abs_det_h,
        'algebraic_jacobian_times_det_abs': algebraic_product,
        'product_minus_factors': algebraic_product - reciprocal_jac * abs_det_h,
        'net_count_r_power': powers['net_count_r_power'],
        'free_residual_coordinates': ['f_yy', 'f_xyy', 'f_yyy'],
        'axial_area_measure_zero': True,
        'contact_integrand_algebraic_factor_skeleton_enumerated': True,
        'contact_gaussian_density_bounded': False,
        'conditioned_expectation_evaluated': False,
        'global_contact_density_bound_proved': False,
        'meaning': (
            'exact axial product (1/|det J_grad|)·|det H_skeleton|; '
            'area-measure zero; Gaussian density still unbound'
        ),
    }


def contact_integrand_algebraic_factor_skeleton_inventory(
    *, transverse_y: Coord | None = None, axial_y: Coord | None = None,
    thin_y: Coord | None = None, pin_y: Coord | None = None,
) -> dict:
    """Bundle transverse/axial/thin-belt/pin-centered contact integrand algebraic factor skeletons."""
    ty = transverse_y if transverse_y is not None else point(0, 2)
    ay = axial_y if axial_y is not None else point(2, 0)
    thin = thin_y if thin_y is not None else point(2, Q(1, 8))
    py = pin_y if pin_y is not None else point(Q(1, 2), Q(1, 20))
    return {
        'object': 'RN-MESOSCOPIC-CONTACT-INTEGRAND-ALGEBRAIC-FACTOR-20260925-v1',
        'C_transverse': transverse_contact_integrand_algebraic_factor_skeleton(
            ty, gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4, f_yyy=6),
        'C_axial': axial_contact_integrand_algebraic_factor_skeleton(
            ay, gap_mark=1, f_yy=2, f_xxy=3),
        'C_thin_belt': thin_belt_contact_integrand_algebraic_factor_skeleton(
            thin, gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0),
        'C_pin_centered': pin_centered_contact_integrand_algebraic_factor_skeleton(
            py, inner=Q(2, 5), outer=1, H_xx=-2, H_xy=0, H_yy=3),
        'global_contact_density_bound_proved': False,
        'conditioned_expectation_evaluated': False,
        'meaning': (
            'exact algebraic Jacobian×|det H| factor products after grad contact; '
            'does not bound the contact Gaussian density'
        ),
    }


def contact_algebraic_factor_times_height_r_inventory(
    *, transverse_y: Coord | None = None, thin_y: Coord | None = None,
    pin_y: Coord | None = None,
) -> dict:
    """Bundle algebraic-factor × height-r combined skeletons on charts with unmatched r^1.

    C_transverse, C_thin_belt, and C_pin_centered each record the product
    (1/|det J|)·|det H| together with unmatched height r^1. C_axial has no
    unmatched height r at leading order, so it is listed as exempt rather than
    combined. Does not absorb any factor or bound the contact Gaussian density.
    """
    ty = transverse_y if transverse_y is not None else point(0, 2)
    thin = thin_y if thin_y is not None else point(2, Q(1, 8))
    py = pin_y if pin_y is not None else point(Q(1, 2), Q(1, 20))
    return {
        'object': 'RN-MESOSCOPIC-ALGEBRAIC-FACTOR-TIMES-HEIGHT-R-INVENTORY-20260925-v1',
        'C_transverse': transverse_algebraic_factor_times_height_r_skeleton(
            ty, gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4, f_yyy=6),
        'C_thin_belt': thin_belt_algebraic_factor_times_height_r_skeleton(
            thin, gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0),
        'C_pin_centered': pin_centered_algebraic_factor_times_height_r_skeleton(
            py, inner=Q(2, 5), outer=1, H_xx=-2, H_xy=0, H_yy=3, f_yyy=6),
        'C_axial': {
            'chart': 'C_axial',
            'unmatched_height_density_r_power': 0,
            'no_unmatched_height_r_at_leading_order': True,
            'combined_skeleton_applicable': False,
            'axial_area_measure_zero': True,
            'contact_gaussian_density_bounded': False,
        },
        'charts_with_combined_skeleton': ['C_transverse', 'C_thin_belt', 'C_pin_centered'],
        'any_combined_skeleton_absorbed_into_uniform_bound': False,
        'global_contact_density_bound_proved': False,
        'conditioned_expectation_evaluated': False,
        'meaning': (
            'inventory of exact (1/|det J|)·|det H| × unmatched height r^1 combined '
            'skeletons; axial exempt (no unmatched height r); density still unbound'
        ),
    }


def pin_site_unmatched_height_r_power_inventory() -> dict:
    """Exact unmatched height-r powers for enumerated pin-site next-order jets.

    After Morse leading height (1/2)z·J_grad, each homogeneous residual of total
    degree n (cubic…hexadecic) inserts an unmatched density factor r^(n-2) with
    the Euler identity z·(grad residual) = n · (height residual). None of these
    powers are absorbed into a uniform integrand bound; seventeenth-and-higher
    jets and the contact Gaussian density remain open.
    """
    orders = [
        ('cubic', 'H_*_next', 3, 1),
        ('quartic', 'Q_*_next', 4, 2),
        ('quintic', 'P_*_next', 5, 3),
        ('sextic', 'S_*_next', 6, 4),
        ('septic', 'T_*_next', 7, 5),
        ('octic', 'U_*_next', 8, 6),
        ('nonic', 'N_*_next', 9, 7),
        ('decic', 'D_*_next', 10, 8),
        ('undecic', 'E_*_next', 11, 9),
        ('dodecic', 'F_*_next', 12, 10),
        ('tridecic', 'G_*_next', 13, 11),
        ('tetradecic', 'I_*_next', 14, 12),
        ('pentadecic', 'J_*_next', 15, 13),
        ('hexadecic', 'K_*_next', 16, 14),
    ]
    by_order = {
        name: {
            'residual_symbol': symbol,
            'homogeneous_degree': degree,
            'unmatched_density_r_power': power,
            'euler_identity': f'z·grad_residual = {degree} · height_residual',
            'height_r_absorbed_into_uniform_bound': False,
        }
        for name, symbol, degree, power in orders
    }
    return {
        'object': 'RN-MESOSCOPIC-PIN-UNMATCHED-HEIGHT-R-POWER-INVENTORY-20260925-v1',
        'chart': 'C_pin_centered',
        'enumeration_scope': 'leading_morse_plus_cubic_through_hexadecic',
        'orders': by_order,
        'enumerated_order_names': [name for name, *_ in orders],
        'unmatched_r_powers': [power for *_, power in orders],
        'min_unmatched_density_r_power': 1,
        'max_unmatched_density_r_power': 14,
        'any_height_r_absorbed_into_uniform_bound': False,
        'pin_site_higher_jets_enumerated': False,
        'seventeenth_and_higher_jets_enumerated': False,
        'contact_gaussian_density_bounded': False,
        'global_contact_density_bound_proved': False,
        'meaning': (
            'exact inventory of unmatched height r^(n-2) for cubic through hexadecic '
            'pin residuals; none absorbed; seventeenth-and-higher jets / density open'
        ),
    }


def axial_conditioned_hessian_residual_ledger(
    y: Coord, *, gap_mark: int | Q = 1,
    f_yy: int | Q = 1, f_xxy: int | Q = 1, f_xyy: int | Q = 0, f_yyy: int | Q = 0,
) -> dict:
    """Express axial Hessian contact entries after isolating k and f_xxy.

    Axial gradient contact isolates k and f_xxy. Residual free jets for the
    Hessian factor include f_yy (and f_xyy,f_yyy at next order):
      H_xx = 12 k y1 = 2 J_grad_x / y1   (when y1≠0)
      H_xy = f_xxy y1 = 2 J_grad_y / y1
      H_yy = f_yy                         (free residual)
    Exact identities only; density / expectation remain open; area-measure zero.
    """
    if not axial_chart_ok(y):
        raise ValueError('point outside C_axial chart')
    y1, y2 = y
    k = exact(gap_mark)
    a, b, c, d = map(exact, (f_yy, f_xxy, f_xyy, f_yyy))
    if k <= 0:
        raise ValueError('positive gap mark required')
    rows = axial_contact_rows(y, gap_mark=k, f_xxy=b)
    jy, jx = rows['J_grad_y'], rows['J_grad_x']
    h_xx = (2 * jx) / y1
    h_xy = (2 * jy) / y1
    h_yy = a
    raw = axial_hessian_contact_rows(y, gap_mark=k, f_yy=a, f_xxy=b, f_xyy=c, f_yyy=d)
    return {
        'object': 'RN-MESOSCOPIC-AXIAL-CONDITIONED-HESSIAN-RESIDUAL-20260925-v1',
        'chart': 'C_axial',
        'y': {'y1': y1, 'y2': y2},
        'isolated_by_grad_contact': ['k', 'f_xxy'],
        'free_residual_coordinates': ['f_yy', 'f_xyy', 'f_yyy'],
        'J_grad_y': jy,
        'J_grad_x': jx,
        'H_xx_from_J_grad_x': h_xx,
        'H_xy_from_J_grad_y': h_xy,
        'H_yy_free_residual': h_yy,
        'H_xx_minus_raw': h_xx - raw['H_xx_contact'],
        'H_xy_minus_raw': h_xy - raw['H_xy_contact'],
        'H_yy_minus_raw': h_yy - raw['H_yy_contact'],
        'det_contact_leading_residual': h_xx * h_yy,
        'axial_area_measure_zero': True,
        'conditioned_hessian_residual_polynomials_enumerated': True,
        'conditioned_expectation_evaluated': False,
        'contact_gaussian_density_bounded': False,
        'hessian_ledger_evaluated': False,
        'meaning': (
            'exact axial residual Hessian after isolating k,f_xxy; H_yy stays free; '
            'not a conditioned Gaussian expectation'
        ),
    }


def axial_hessian_contact_rows(y: Coord, *, gap_mark: int | Q,
                               f_yy: int | Q, f_xxy: int | Q,
                               f_xyy: int | Q = 0, f_yyy: int | Q = 0) -> dict[str, Q]:
    """Leading contact Hessian entries on C_axial (y2=0).

    H_xx_contact = 12k y1
    H_xy_contact = f_xxy y1
    H_yy_contact = f_yy
    """
    if not axial_chart_ok(y):
        raise ValueError('point outside C_axial chart')
    y1, y2 = y
    k = exact(gap_mark)
    a, b, c, d = map(exact, (f_yy, f_xxy, f_xyy, f_yyy))
    if k <= 0:
        raise ValueError('positive gap mark required')
    if y2 != 0:
        raise ValueError('axial chart requires y2=0')
    h_xx = 12 * k * y1
    h_xy = b * y1
    h_yy = a
    h_yy_next = c * y1
    return {
        'H_xx_contact': h_xx,
        'H_xy_contact': h_xy,
        'H_yy_contact': h_yy,
        'H_yy_next': h_yy_next,
        'det_contact_leading': h_xx * h_yy,
        'det_xy_square_coefficient': h_xy * h_xy,
        'y1': y1,
        'y2': y2,
        'gap_mark': k,
        'f_yy': a,
        'f_xxy': b,
        'f_xyy': c,
        'f_yyy': d,
    }


def hessian_ledger_for_point(y: Coord, gap_mark: int | Q = 1,
                             f_yy: int | Q = 1, f_xxy: int | Q = 0,
                             f_xyy: int | Q = 0, f_yyy: int | Q = 0) -> dict:
    rows = hessian_contact_rows(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    scale = hessian_scaling_report(2, chart='C_transverse')
    return {
        'object': 'RN-MESOSCOPIC-CHART-HESSIAN-D2-TRANSVERSE-20260925-v1',
        'chart': 'C_transverse',
        'y': {'y1': rows['y1'], 'y2': rows['y2']},
        'contact_rows': {
            'H_xx_contact': rows['H_xx_contact'],
            'H_xy_contact': rows['H_xy_contact'],
            'H_yy_contact': rows['H_yy_contact'],
            'H_yy_next': rows['H_yy_next'],
            'det_contact_leading': rows['det_contact_leading'],
            'det_xy_square_coefficient': rows['det_xy_square_coefficient'],
        },
        'scaling': scale,
        'raw_det_leading_r_power': scale['raw_det_leading_r_power'],
        'hessian_contact_rows_enumerated': True,
        'hessian_ledger_evaluated': False,
        'conditioned_expectation_evaluated': False,
        'full_annulus_closed': False,
        'legacy_24jet_discharged': False,
        'complements_pr7': True,
        'meaning': (
            'exact d=2 transverse Hessian contact rows and raw det r-power 1; '
            'not a conditioned Kac-Rice Hessian expectation'
        ),
    }


def height_grad_y_dependency(y: Coord) -> Q:
    """Exact linear relation J_height - (y2/2) J_grad_y = 0 at leading jet order."""
    if not transverse_chart_ok(y):
        raise ValueError('point outside C_transverse chart')
    return exact(y[1]) / 2


def height_next_order_independent(y: Coord, *, gap_mark: int | Q,
                                  f_xxy: int | Q, f_xyy: int | Q,
                                  f_yyy: int | Q) -> dict[str, Q | bool]:
    """Independent height direction appears at the next order in r.

    On C_transverse, the leading height row is dependent on J_grad_y. The coefficient
    H_height_next supplies a new linear form in (k, f_xxy, f_xyy, f_yyy). When this
    form is not identically zero as a polynomial in y, the height mark becomes an
    independent contact observation after restoring the explicit factor of r.
    """
    rows = contact_rows(
        y, gap_mark=gap_mark, f_yy=0, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    # With f_yy=0, leading J_height vanishes; independence is carried by H_height_next.
    return {
        'H_height_next': rows['H_height_next'],
        'leading_height_residual': rows['height_residual_at_leading_order'],
        'next_order_supplies_height': True,
        'explicit_r_factor_still_required': True,
    }


def transverse_height_r_factor_ledger(
    y: Coord, *, gap_mark: int | Q = 1,
    f_yy: int | Q = 1, f_xxy: int | Q = 0, f_xyy: int | Q = 0, f_yyy: int | Q = 0,
) -> dict:
    """Record the unmatched explicit r in the transverse height density.

    Leading J_height = (y2/2) J_grad_y is dependent. Restoring independence via
    H_height_next inserts one unmatched power of r into the height density factor.
    This ledger does not absorb that r into a uniform integrand bound.
    """
    if not transverse_chart_ok(y):
        raise ValueError('point outside C_transverse chart')
    rows = contact_rows(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    dep = height_grad_y_dependency(y)
    nxt = height_next_order_independent(
        y, gap_mark=gap_mark, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    return {
        'object': 'RN-MESOSCOPIC-TRANSVERSE-HEIGHT-R-FACTOR-20260925-v1',
        'chart': 'C_transverse',
        'leading_height_dependent_on_grad_y': True,
        'height_dependency_factor_y2_over_2': dep,
        'J_height': rows['J_height'],
        'J_grad_y': rows['J_grad_y'],
        'height_minus_dep_times_grad_y': rows['J_height'] - dep * rows['J_grad_y'],
        'H_height_next': nxt['H_height_next'],
        'next_order_supplies_independent_height': True,
        'unmatched_height_density_r_power': 1,
        'explicit_r_factor_still_required': True,
        'height_r_absorbed_into_uniform_bound': False,
        'meaning': (
            'leading height is (y2/2)J_grad_y; independence needs H_height_next '
            'and inserts unmatched r^1; not absorbed into a uniform density bound'
        ),
    }


def thin_belt_height_r_factor_ledger(
    y: Coord, *, gap_mark: int | Q = 1,
    f_yy: int | Q = 1, f_xxy: int | Q = 0, f_xyy: int | Q = 0, f_yyy: int | Q = 0,
    floor_y2: int | Q = Q(1, 4),
) -> dict:
    """Record unmatched height r^1 on C_thin_belt (shared transverse jet forms).

    Same leading dependence J_height = (y2/2) J_grad_y as C_transverse; restoring
    independence via H_height_next inserts unmatched density r^1. Separately, the
    thin-belt contact Gaussian density near y2→0 remains open (bare 1/|y2| L1
    cleared by jet-map cancel). Does not absorb height-r or bound density.
    """
    if not thin_belt_ok(y, floor_y2=floor_y2):
        raise ValueError('point outside thin belt')
    rows = thin_belt_contact_rows(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    dep = exact(y[1]) / 2
    # Same H_height_next extraction as height_next_order_independent, on thin belt.
    nxt_rows = thin_belt_contact_rows(
        y, gap_mark=gap_mark, f_yy=0, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    return {
        'object': 'RN-MESOSCOPIC-THIN-BELT-HEIGHT-R-FACTOR-20260925-v1',
        'chart': 'C_thin_belt',
        'y': {'y1': rows['y1'], 'y2': rows['y2']},
        'floor_y2': exact(floor_y2),
        'leading_height_dependent_on_grad_y': True,
        'height_dependency_factor_y2_over_2': dep,
        'J_height': rows['J_height'],
        'J_grad_y': rows['J_grad_y'],
        'height_minus_dep_times_grad_y': rows['J_height'] - dep * rows['J_grad_y'],
        'H_height_next': nxt_rows['H_height_next'],
        'next_order_supplies_independent_height': True,
        'unmatched_height_density_r_power': 1,
        'explicit_r_factor_still_required': True,
        'height_r_absorbed_into_uniform_bound': False,
        'bare_reciprocal_L1_obstruction_cleared_by_cancel': True,
        'contact_gaussian_density_bounded': False,
        'meaning': (
            'thin-belt shares transverse height–grad_y dependence; unmatched r^1 '
            'not absorbed; Gaussian density near y2=0 still unbound'
        ),
    }


def axial_height_independence_ledger(
    y: Coord, *, gap_mark: int | Q = 1, f_xxy: int | Q = 1,
) -> dict:
    """Record that axial height needs no unmatched r^1 (contrast C_transverse).

    On C_axial, J_height = 2k y1^3 already sits at cubic order (p_height=3).
    It shares the gap mark k with J_grad_x = 6k y1^2 (exact identity
    J_height = (y1/3) J_grad_x), but the distinct scaling exponents mean this
    shared-mark relation does not force an H_height_next / unmatched density
    r^1 the way same-order transverse height–grad_y dependence does.
    Area-measure zero; Gaussian density still unbound.
    """
    if not axial_chart_ok(y):
        raise ValueError('point outside C_axial chart')
    rows = axial_contact_rows(y, gap_mark=gap_mark, f_xxy=f_xxy)
    y1 = rows['y1']
    jy, jx, jh = rows['J_grad_y'], rows['J_grad_x'], rows['J_height']
    return {
        'object': 'RN-MESOSCOPIC-AXIAL-HEIGHT-INDEPENDENCE-20260925-v1',
        'chart': 'C_axial',
        'y': {'y1': y1, 'y2': rows['y2']},
        'J_grad_y': jy,
        'J_grad_x': jx,
        'J_height': jh,
        'height_scaling_exponent': 3,
        'height_independent_at_leading_axial_order': True,
        'leading_height_dependent_on_grad_y': False,
        'leading_height_dependent_on_grad_x': False,
        'unmatched_height_density_r_power': 0,
        'explicit_r_factor_still_required': False,
        'no_unmatched_height_r_at_leading_order': True,
        'axial_area_measure_zero': True,
        'contact_gaussian_density_bounded': False,
        'meaning': (
            'axial J_height=2k y1^3 is independent at leading order; '
            'no unmatched height r^1 (unlike C_transverse); density still unbound'
        ),
    }


def axial_height_grad_x_shared_mark_ledger(
    y: Coord, *, gap_mark: int | Q = 1, f_xxy: int | Q = 1,
) -> dict:
    """Exact shared-gap-mark identity J_height = (y1/3) J_grad_x on C_axial.

    Both rows are linear in the gap mark k:
      J_grad_x = 6 k y1^2,   J_height = 2 k y1^3
    so J_height − (y1/3) J_grad_x = 0 whenever y1≠0. Distinct scaling exponents
    (p_x=2, p_height=3) keep unmatched height density r-power at 0 — no
    H_height_next is required. Does not bound the contact Gaussian density.
    """
    if not axial_chart_ok(y):
        raise ValueError('point outside C_axial chart')
    rows = axial_contact_rows(y, gap_mark=gap_mark, f_xxy=f_xxy)
    y1 = rows['y1']
    jx, jh = rows['J_grad_x'], rows['J_height']
    factor = y1 / 3
    return {
        'object': 'RN-MESOSCOPIC-AXIAL-HEIGHT-GRAD-X-SHARED-MARK-20260925-v1',
        'chart': 'C_axial',
        'y': {'y1': y1, 'y2': rows['y2']},
        'J_grad_x': jx,
        'J_height': jh,
        'shared_gap_mark_coordinate': 'k',
        'height_over_grad_x_factor_y1_over_3': factor,
        'height_minus_y1_over_3_times_grad_x': jh - factor * jx,
        'grad_x_scaling_exponent': 2,
        'height_scaling_exponent': 3,
        'shared_mark_forces_unmatched_height_r': False,
        'unmatched_height_density_r_power': 0,
        'explicit_r_factor_still_required': False,
        'no_unmatched_height_r_at_leading_order': True,
        'axial_area_measure_zero': True,
        'contact_gaussian_density_bounded': False,
        'meaning': (
            'exact J_height=(y1/3)J_grad_x via shared gap mark k; '
            'distinct scalings keep unmatched height r at 0; density still unbound'
        ),
    }


def transverse_height_residual_after_grad_contact(
    y: Coord, *, gap_mark: int | Q = 1,
    f_yy: int | Q = 1, f_xxy: int | Q = 0, f_xyy: int | Q = 0, f_yyy: int | Q = 0,
) -> dict:
    """Express H_height_next in free residuals after eliminating f_yy and f_xyy.

    With y2≠0, gradient contact solves
      f_yy  = J_grad_y / y2
      f_xyy = (2/y2^2) (J_grad_x − 6k y1^2 − f_xxy y1 y2)
    Substituting into H_height_next yields the exact residual form
      H_height_next = y1·J_grad_x − 4k y1^3 − (1/2) f_xxy y1^2 y2 + (1/6) f_yyy y2^3
    Free residual coordinates: (k, f_xxy, f_yyy). The unmatched density r^1 is
    still not absorbed into a uniform bound.
    """
    if not transverse_chart_ok(y):
        raise ValueError('point outside C_transverse chart')
    y1, y2 = y
    k = exact(gap_mark)
    a, b, c, d = map(exact, (f_yy, f_xxy, f_xyy, f_yyy))
    if k <= 0:
        raise ValueError('positive gap mark required')
    rows = contact_rows(y, gap_mark=k, f_yy=a, f_xxy=b, f_xyy=c, f_yyy=d)
    jy, jx = rows['J_grad_y'], rows['J_grad_x']
    f_xyy_solved = (2 / (y2 * y2)) * (jx - 6 * k * y1 * y1 - b * y1 * y2)
    h_resid = (
        y1 * jx
        - 4 * k * y1 ** 3
        - (b * y1 * y1 * y2) / 2
        + (d * y2 ** 3) / 6
    )
    h_raw = rows['H_height_next']
    return {
        'object': 'RN-MESOSCOPIC-TRANSVERSE-HEIGHT-RESIDUAL-AFTER-GRAD-20260925-v1',
        'chart': 'C_transverse',
        'y': {'y1': y1, 'y2': y2},
        'free_residual_coordinates': ['k', 'f_xxy', 'f_yyy'],
        'eliminated_by_grad_contact': ['f_yy', 'f_xyy'],
        'J_grad_y': jy,
        'J_grad_x': jx,
        'f_xyy_from_J_grad_x': f_xyy_solved,
        'f_xyy_minus_solved': c - f_xyy_solved,
        'H_height_next_residual': h_resid,
        'H_height_next_raw': h_raw,
        'H_height_next_minus_raw': h_resid - h_raw,
        'leading_height_dependent_on_grad_y': True,
        'unmatched_height_density_r_power': 1,
        'explicit_r_factor_still_required': True,
        'height_r_absorbed_into_uniform_bound': False,
        'contact_gaussian_density_bounded': False,
        'meaning': (
            'exact H_height_next residual after eliminating f_yy,f_xyy; '
            'unmatched r^1 and density bound remain open'
        ),
    }


def contact_gradient_rank_symbol(y: Coord) -> dict[str, Q | int | bool]:
    """Rank pattern of (J_grad_x, J_grad_y) as a linear map on (f_yy, f_xxy, f_xyy, k).

    Treat the contact gradient rows as:
      J_y = y2 * f_yy
      J_x = 6 y1^2 * k + y1 y2 * f_xxy + (y2^2)/2 * f_xyy
    With y2≠0 on this chart, J_y isolates f_yy. The J_x row still sees k,f_xxy,f_xyy.
    """
    if not transverse_chart_ok(y):
        raise ValueError('point outside C_transverse chart')
    y1, y2 = y
    return {
        'chart': 'C_transverse',
        'grad_y_coefficient_f_yy': y2,
        'grad_x_coefficient_k': 6 * y1 * y1,
        'grad_x_coefficient_f_xxy': y1 * y2,
        'grad_x_coefficient_f_xyy': (y2 * y2) / 2,
        'grad_y_nonzero': y2 != 0,
        'independent_grad_rows_expected': 2,
        'height_dependent_on_grad_y_at_leading_order': True,
        'height_next_order_enumerated': True,
        'height_dependency_factor': height_grad_y_dependency(y),
    }


def ledger_for_point(y: Coord, gap_mark: int | Q = 1,
                     f_yy: int | Q = 1, f_xxy: int | Q = 0, f_xyy: int | Q = 0,
                     f_yyy: int | Q = 0) -> dict:
    rows = contact_rows(
        y, gap_mark=gap_mark, f_yy=f_yy, f_xxy=f_xxy, f_xyy=f_xyy, f_yyy=f_yyy,
    )
    scale = witness_scaling_determinant_power(2)
    rank = contact_gradient_rank_symbol(y)
    return {
        'object': 'RN-MESOSCOPIC-CHART-J0-D2-TRANSVERSE-20260925-v1',
        'chart': 'C_transverse',
        'y': {'y1': rows['y1'], 'y2': rows['y2']},
        'contact_rows': {
            'J_grad_y': rows['J_grad_y'],
            'J_grad_x': rows['J_grad_x'],
            'J_height': rows['J_height'],
            'H_height_next': rows['H_height_next'],
            'height_residual_at_leading_order': rows['height_residual_at_leading_order'],
        },
        'scaling': scale,
        'rank': {k: v for k, v in rank.items()},
        'height_row_independent_at_leading_order': False,
        'height_next_order_enumerated': True,
        'hessian_contact_rows_enumerated': True,
        'hessian_ledger_evaluated': False,
        'full_annulus_closed': False,
        'legacy_24jet_discharged': False,
        'independent_analytic_acceptance': False,
        'complements_pr7': True,
        'meaning': (
            'exact d=2 transverse chart contact rows, next-order height remainder, '
            'and gradient Jacobian r-power; not a continuum Gaussian evaluation'
        ),
    }


def sample_points() -> tuple[Coord, ...]:
    return (
        point(0, 2),
        point(2, 2),
        point(-2, Q(3, 2)),
        point(Q(3, 2), Q(3, 2)),
        point(0, -2),
    )


def sample_axial_points() -> tuple[Coord, ...]:
    return (
        point(2, 0),
        point(-2, 0),
        point(3, 0),
        point(-3, 0),
    )


def result() -> dict:
    y = point(0, 2)
    sample = ledger_for_point(y, gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0)
    axial = axial_ledger_for_point(point(2, 0), gap_mark=1, f_xxy=2)
    cover = chart_cover_report()
    thin = thin_belt_conditioning(point(2, Q(1, 8)))
    thin_led = thin_belt_ledger_for_point(point(2, Q(1, 8)), gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0)
    thin_shells = thin_belt_reciprocal_shell_lower_bound(8)
    boundary = chart_boundary_transition(point(2, Q(1, 4)), gap_mark=1, f_yy=2)
    jet_map = jet_map_f_yy_to_J_grad_y_factor(point(2, Q(1, 8)))
    thin_cancel = thin_belt_integrand_residual_after_cancel(point(2, Q(1, 8)))
    transverse_bound = transverse_conditioning_uniform_bound(point(0, 2))
    axial_bound = axial_conditioning_uniform_bound(point(2, 0))
    height_r = transverse_height_r_factor_ledger(point(0, 2), gap_mark=1, f_yy=2)
    thin_height_r = thin_belt_height_r_factor_ledger(point(2, Q(1, 8)), gap_mark=1, f_yy=2)
    axial_height = axial_height_independence_ledger(point(2, 0), gap_mark=1, f_xxy=2)
    axial_shared = axial_height_grad_x_shared_mark_ledger(point(2, 0), gap_mark=1, f_xxy=2)
    # Small-A regime only: pins can lie inside the annulus.
    near = near_pin_diagnosis(point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1)
    pin_led = pin_centered_ledger_for_point(
        point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1,
        f_yyyy=24, f_yyyyy=120, f_yyyyyy=720, f_yyyyyyy=5040, f_yyyyyyyy=40320,
        f_yyyyyyyyy=362880, f_yyyyyyyyyy=3628800, f_yyyyyyyyyyy=39916800,
        f_yyyyyyyyyyyy=479001600, f_yyyyyyyyyyyyy=6227020800, f_yyyyyyyyyyyyyy=87178291200,
        f_yyyyyyyyyyyyyyy=1307674368000, f_yyyyyyyyyyyyyyyy=20922789888000)
    pin_obs = pin_site_jet_obstruction_ledger(point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1)
    hess = hessian_ledger_for_point(y, gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0)
    axial_hess = axial_hessian_contact_rows(
        point(2, 0), gap_mark=1, f_yy=2, f_xxy=3, f_xyy=0)
    integrand_t = contact_integrand_power_ledger(2, chart='C_transverse')
    integrand_a = contact_integrand_power_ledger(2, chart='C_axial')
    integrand_pin = pin_centered_integrand_power_ledger(2)
    density_obs = contact_density_obstruction_inventory()
    free_jets = contact_free_jet_residual_inventory()
    grad_jac = contact_gradient_jacobian_density_shape_inventory()
    hess_resid = transverse_conditioned_hessian_residual_ledger(
        y, gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4)
    axial_hess_resid = axial_conditioned_hessian_residual_ledger(
        point(2, 0), gap_mark=1, f_yy=2, f_xxy=3)
    height_resid = transverse_height_residual_after_grad_contact(
        y, gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4, f_yyy=6)
    det_skel = contact_conditioned_det_free_jet_skeleton_inventory()
    integrand_alg = contact_integrand_algebraic_factor_skeleton_inventory()
    pin_alg = pin_centered_contact_integrand_algebraic_factor_skeleton(
        point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1, H_xx=-2, H_xy=0, H_yy=3)
    pin_height_r = pin_centered_height_r_factor_ledger(
        point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1, H_xx=-2, H_xy=0, H_yy=3, f_yyy=6)
    pin_alg_height = pin_centered_algebraic_factor_times_height_r_skeleton(
        point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1, H_xx=-2, H_xy=0, H_yy=3, f_yyy=6)
    alg_height = transverse_algebraic_factor_times_height_r_skeleton(
        y, gap_mark=1, f_yy=2, f_xxy=3, f_xyy=4, f_yyy=6)
    thin_alg_height = thin_belt_algebraic_factor_times_height_r_skeleton(
        point(2, Q(1, 8)), gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0)
    alg_height_inv = contact_algebraic_factor_times_height_r_inventory()
    pin_r_inv = pin_site_unmatched_height_r_power_inventory()
    # JSON-friendly rationals as strings
    def conv(obj):
        if isinstance(obj, Q):
            return str(obj)
        if isinstance(obj, dict):
            return {k: conv(v) for k, v in obj.items()}
        if isinstance(obj, tuple):
            return [conv(v) for v in obj]
        if isinstance(obj, list):
            return [conv(v) for v in obj]
        return obj
    out = conv(sample)
    out['axial_sample'] = conv(axial)
    out['cover'] = conv(cover)
    out['thin_belt_sample'] = conv(thin)
    out['thin_belt_ledger'] = conv(thin_led)
    out['thin_belt_reciprocal_shells'] = conv(thin_shells)
    out['chart_boundary_transition'] = conv(boundary)
    out['jet_map_f_yy_sample'] = conv(jet_map)
    out['thin_belt_integrand_residual_after_cancel'] = conv(thin_cancel)
    out['transverse_conditioning_bound'] = conv(transverse_bound)
    out['axial_conditioning_bound'] = conv(axial_bound)
    out['transverse_height_r_factor'] = conv(height_r)
    out['thin_belt_height_r_factor'] = conv(thin_height_r)
    out['axial_height_independence'] = conv(axial_height)
    out['axial_height_grad_x_shared_mark'] = conv(axial_shared)
    out['near_pin_sample'] = conv(near)
    out['pin_centered_ledger'] = conv(pin_led)
    out['pin_site_jet_obstruction'] = conv(pin_obs)
    out['hessian_sample'] = conv(hess)
    out['axial_hessian_sample'] = conv(axial_hess)
    out['integrand_power_transverse'] = conv(integrand_t)
    out['integrand_power_axial'] = conv(integrand_a)
    out['integrand_power_pin_centered'] = conv(integrand_pin)
    out['contact_density_obstruction'] = conv(density_obs)
    out['contact_free_jet_residual'] = conv(free_jets)
    out['contact_gradient_jacobian_density_shape'] = conv(grad_jac)
    out['transverse_conditioned_hessian_residual'] = conv(hess_resid)
    out['axial_conditioned_hessian_residual'] = conv(axial_hess_resid)
    out['transverse_height_residual_after_grad'] = conv(height_resid)
    out['contact_conditioned_det_free_jet_skeleton'] = conv(det_skel)
    out['contact_integrand_algebraic_factor_skeleton'] = conv(integrand_alg)
    out['pin_centered_contact_integrand_algebraic_factor'] = conv(pin_alg)
    out['pin_centered_height_r_factor'] = conv(pin_height_r)
    out['pin_centered_algebraic_factor_times_height_r'] = conv(pin_alg_height)
    out['transverse_algebraic_factor_times_height_r'] = conv(alg_height)
    out['thin_belt_algebraic_factor_times_height_r'] = conv(thin_alg_height)
    out['contact_algebraic_factor_times_height_r_inventory'] = conv(alg_height_inv)
    out['pin_site_unmatched_height_r_power_inventory'] = conv(pin_r_inv)
    out['sample_points_ok'] = all(transverse_chart_ok(p) for p in sample_points())
    out['axial_points_ok'] = all(axial_chart_ok(p) for p in sample_axial_points())
    out['pin_exclusion_ok'] = all(away_from_pins(p) for p in sample_points() + sample_axial_points())
    out['gradient_jacobian_r_power'] = SCALING_EXPONENTS['grad_x'] + SCALING_EXPONENTS['grad_y']
    out['axial_gradient_jacobian_r_power'] = (
        AXIAL_SCALING_EXPONENTS['grad_x'] + AXIAL_SCALING_EXPONENTS['grad_y']
    )
    out['hessian_raw_det_leading_r_power'] = HESSIAN_SCALING_EXPONENTS['xx']  # =1; yy contributes r^0
    out['transverse_net_count_r_power'] = integrand_t['net_count_r_power']
    out['axial_net_count_r_power'] = integrand_a['net_count_r_power']
    out['pin_centered_net_count_r_power'] = integrand_pin['net_count_r_power']

    out['classifications'] = {
        'transverse': classify_annulus_point(point(0, 2)),
        'axial': classify_annulus_point(point(2, 0)),
        'thin': classify_annulus_point(point(2, Q(1, 8))),
        'near_pin_default_annulus': classify_annulus_point(point(Q(1, 2), Q(1, 20))),
        'outside': classify_annulus_point(point(0, 1)),
        'near_pin_small_A': classify_annulus_point(
            point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1, require_pr7_A=False),
    }
    return out


if __name__ == '__main__':
    print(json.dumps(result(), indent=2, sort_keys=True))
