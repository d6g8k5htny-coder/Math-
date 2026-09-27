"""Exact six-pin microdisk rows; finite algebra only, not continuum acceptance."""
from __future__ import annotations
from fractions import Fraction as Q
import json


def exact(x):
    if isinstance(x, bool) or not isinstance(x, (int, Q)):
        raise TypeError('use an integer or exact Fraction')
    return Q(x)


def gradient_rows(r, k, p, q, az, t, c, d):
    r, k, p, q, az, t, c, d = map(exact, (r, k, p, q, az, t, c, d))
    gx = 6 * k * p * (p - 1) + t * q * (p - Q(1, 2)) + c * q * q / 2
    gz = az * q + r * (t * p * (p - 1) / 2 + c * q * (p - Q(1, 2)) + d * q * q / 2)
    return gx, gz


def raw_gradient(r, k, p, q, az, t, c, d):
    gx, gz = gradient_rows(r, k, p, q, az, t, c, d)
    return r * r * gx, r * gz


def divided_difference_rows(r, k, p, q, az, t, c, d):
    r, k, p, q, az, t, c, d = map(exact, (r, k, p, q, az, t, c, d))
    if q == 0:
        raise ValueError('off-axis divided-difference frame requires q != 0')
    return (6 * k * p * (p - 1) / q + t * (p - Q(1, 2)) + c * q / 2,
            az + r * (t * p * (p - 1) / (2 * q) + c * (p - Q(1, 2)) + d * q / 2))


def reduced_frame_matrix(r, p, q):
    r, p, q = map(exact, (r, p, q))
    if q == 0:
        raise ValueError('off-axis reduced frame requires q != 0')
    return ((Q(0), p - Q(1, 2), q / 2, Q(0)),
            (Q(1), r * p * (p - 1) / (2 * q), r * (p - Q(1, 2)), r * q / 2))


def reduced_frame_minor_az_t(r, p, q):
    rows = reduced_frame_matrix(r, p, q)
    return rows[0][0] * rows[1][1] - rows[1][0] * rows[0][1]


def jacobian_scale(r, q):
    r, q = map(exact, (r, q))
    return r ** 3 * q * q


def nested_jacobian_scale(r, Qcoord):
    r, Qcoord = map(exact, (r, Qcoord))
    return r ** 5 * Qcoord * Qcoord


def nested_divided_difference_rows(r, k, P, Qcoord, az, t, c, d):
    r, P, Qcoord = map(exact, (r, P, Qcoord))
    return divided_difference_rows(r, k, r * P, r * Qcoord, az, t, c, d)


def axis_witness_solution(r, q, c, d):
    r, q, c, d = map(exact, (r, q, c, d))
    if q == 0:
        raise ValueError('axis witness solve is only for q != 0')
    return r * (c - d * q) / 2, c * q


def hessian_determinant(r, k, x, z, az, t, c, d):
    r, k, x, z, az, t, c, d = map(exact, (r, k, x, z, az, t, c, d))
    xx = 12 * k * x + t * z
    xz = t * x + c * z
    zz = az + c * x + d * z
    return xx * zz - xz * xz


def axis_witness_determinants(r, k, q, c, d):
    r, k, q, c, d = map(exact, (r, k, q, c, d))
    az, t = axis_witness_solution(r, q, c, d)
    return {
        'M': hessian_determinant(r, k, -r / 2, Q(0), az, t, c, d),
        'X': hessian_determinant(r, k, -r / 2, r * q, az, t, c, d),
        'S': hessian_determinant(r, k, r / 2, Q(0), az, t, c, d),
    }


def axis_q_factors(r, k, q, c, d):
    r, k, q, c, d = map(exact, (r, k, q, c, d))
    dets = axis_witness_determinants(r, k, q, c, d)
    return {
        'M': dets['M'] / q,
        'X': dets['X'] / q,
        'S': dets['S'],
    }


def axis_product_without_q2(r, k, q, c, d):
    r, k, q, c, d = map(exact, (r, k, q, c, d))
    dets = axis_witness_determinants(r, k, q, c, d)
    return dets['M'] * dets['X'] * dets['S'] / (q * q)


def result():
    return {
        'object': 'D5-PIN-MICRODISK-20260927-v1',
        'dimension': 2,
        'scientific_effect': 'NONE',
        'uses_original_six_endpoint_pins': True,
        'two_point_divided_difference_frame': True,
        'off_axis_frame_nondegenerate': True,
        'outer_transverse_cancellation_rechecked': True,
        'uniform_microdisk_majorant_closed': False,
        'on_axis_nested_obstruction_open': True,
        'annulus_collar_closed': False,
        'all_height_O_r3_pin_neighborhood_closed': False,
        'meaning': 'finite exact row and determinant-factor checks only; the nested on-axis microdisk remains open',
    }


if __name__ == '__main__':
    print(json.dumps(result(), indent=2, sort_keys=True))
