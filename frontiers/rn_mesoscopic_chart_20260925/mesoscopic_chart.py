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
                                  margin: int | Q = Q(1, 10)) -> dict:
    """Frame-only pin-centred ledger: refuses midpoint U_0 rows; does not invent pin jets."""
    frame = pin_centered_frame(y, inner=inner, outer=outer, margin=margin)
    return {
        'object': 'RN-MESOSCOPIC-CHART-PIN-CENTERED-D2-20260925-v1',
        'chart': 'C_pin_centered',
        'frame': frame,
        'midpoint_U0_rows_applicable': False,
        'pin_site_jet_rows_enumerated': False,
        'contact_rows_enumerated': False,
        'hessian_ledger_evaluated': False,
        'uniform_integrand_bound_proved': False,
        'full_annulus_closed': False,
        'legacy_24jet_discharged': False,
        'pr7_fixed_annulus_A_gt_1': False,
        'complements_pr7': True,
        'status': 'OPEN_SEPARATE_CHART_REQUIRED',
        'meaning': (
            'records the pin-local frame (z = y - pin) on a small-A near-pin chart; '
            'does not supply pin-site divided-difference contact rows'
        ),
    }


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
    net = spatial - grad + hess + height
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
    transverse_bound = transverse_conditioning_uniform_bound(point(0, 2))
    # Small-A regime only: pins can lie inside the annulus.
    near = near_pin_diagnosis(point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1)
    pin_led = pin_centered_ledger_for_point(point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1)
    hess = hessian_ledger_for_point(y, gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0)
    axial_hess = axial_hessian_contact_rows(
        point(2, 0), gap_mark=1, f_yy=2, f_xxy=3, f_xyy=0)
    integrand_t = contact_integrand_power_ledger(2, chart='C_transverse')
    integrand_a = contact_integrand_power_ledger(2, chart='C_axial')
    # JSON-friendly rationals as strings
    def conv(obj):
        if isinstance(obj, Q):
            return str(obj)
        if isinstance(obj, dict):
            return {k: conv(v) for k, v in obj.items()}
        if isinstance(obj, tuple):
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
    out['transverse_conditioning_bound'] = conv(transverse_bound)
    out['near_pin_sample'] = conv(near)
    out['pin_centered_ledger'] = conv(pin_led)
    out['hessian_sample'] = conv(hess)
    out['axial_hessian_sample'] = conv(axial_hess)
    out['integrand_power_transverse'] = conv(integrand_t)
    out['integrand_power_axial'] = conv(integrand_a)
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
