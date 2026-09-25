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


def in_annulus(y: Coord, inner: int | Q, outer: int | Q) -> bool:
    a, b = exact(inner), exact(outer)
    if not 1 < a < b:
        raise ValueError('require 1 < A < B')
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


def witness_scaling_determinant_power(dimension: int = 2) -> dict[str, int]:
    """r-power of det(diag(r^{p_i})) for the witness block on this chart."""
    if dimension != 2:
        raise ValueError('this package enumerates the d=2 transverse chart only')
    power = SCALING_EXPONENTS['grad_x'] + SCALING_EXPONENTS['grad_y']
    # Height is the Kac-Rice mark, not part of the gradient-density Jacobian.
    return {
        'dimension': 2,
        'chart': 'C_transverse',
        'gradient_scaling_exponents': (
            SCALING_EXPONENTS['grad_x'],
            SCALING_EXPONENTS['grad_y'],
        ),
        'height_scaling_exponent': SCALING_EXPONENTS['height'],
        'gradient_jacobian_r_power': power,
        'spatial_volume_r_power': dimension,
        'height_window_r_power': 3,
        'meaning': (
            'det scaling for raw->J gradient map is r^(p_x+p_y); '
            'height scaling is recorded separately for the mark integral'
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


def result() -> dict:
    y = point(0, 2)
    sample = ledger_for_point(y, gap_mark=1, f_yy=2, f_xxy=0, f_xyy=0)
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
    out['sample_points_ok'] = all(transverse_chart_ok(p) for p in sample_points())
    out['pin_exclusion_ok'] = all(away_from_pins(p) for p in sample_points())
    out['gradient_jacobian_r_power'] = SCALING_EXPONENTS['grad_x'] + SCALING_EXPONENTS['grad_y']
    return out


if __name__ == '__main__':
    print(json.dumps(result(), indent=2, sort_keys=True))
