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
        'open_regions': open_regions,
        'cover_complete': False,
        'notes': (
            'C_transverse ∪ C_axial covers the annulus off the open thin belt '
            '0<|y2|<floor. For A>1/2 the scaled pins lie outside the annulus '
            '(PR7 convention); near-pin charts arise only for smaller A or other scales.'
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


def contact_rows(y: Coord, *, gap_mark: int | Q,
                 f_yy: int | Q, f_xxy: int | Q, f_xyy: int | Q,
                 f_yyy: int | Q = 0) -> dict[str, Q]:
    """Contact-limit J_0 rows on C_transverse after the six-pin / U_0 constraints.

    Free jet leftovers used here: f_yy, f_xxy, f_xyy, f_yyy (exact rationals).
    Gap mark k enters through f_xxx=12k at contact.
    """
    if not transverse_chart_ok(y):
        raise ValueError('point outside C_transverse chart')
    y1, y2 = y
    k = exact(gap_mark)
    a, b, c, d = map(exact, (f_yy, f_xxy, f_xyy, f_yyy))
    if k <= 0:
        raise ValueError('positive gap mark required')
    # Leading contact divided differences (coefficients of the free jet / mark).
    j_y = a * y2
    j_x = 6 * k * y1 * y1 + b * y1 * y2 + (c * y2 * y2) / 2
    j_h = (a * y2 * y2) / 2
    # Next-order height coefficient after /r^2: (f(ry)-b)/r^2 = J_height + r*H_1 + O(r^2)
    # with H_1 = 2k y1^3 + (1/2) f_xxy y1^2 y2 + (1/2) f_xyy y1 y2^2 + (1/6) f_yyy y2^3.
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
    # Small-A regime only: pins can lie inside the annulus.
    near = near_pin_diagnosis(point(Q(1, 2), Q(1, 20)), inner=Q(2, 5), outer=1)
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
    out['near_pin_sample'] = conv(near)
    out['sample_points_ok'] = all(transverse_chart_ok(p) for p in sample_points())
    out['axial_points_ok'] = all(axial_chart_ok(p) for p in sample_axial_points())
    out['pin_exclusion_ok'] = all(away_from_pins(p) for p in sample_points() + sample_axial_points())
    out['gradient_jacobian_r_power'] = SCALING_EXPONENTS['grad_x'] + SCALING_EXPONENTS['grad_y']
    out['axial_gradient_jacobian_r_power'] = (
        AXIAL_SCALING_EXPONENTS['grad_x'] + AXIAL_SCALING_EXPONENTS['grad_y']
    )
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
