"""Exact rational controls for NOTE.md; no numerical field identification.

Polynomial signs certify the stated example; grids in the test file are only
finite controls. Runtime dependencies: Python standard library only.
"""
from fractions import Fraction as F
from math import comb
import json

POLY_P = (-17405, 37524, -36320, 18464, -5440, 768)
POLY_R = (3481, -4720, 4432, -2240, 960)


def parameters(p, q, u, v):
    p, q, u, v = map(F, (p, q, u, v))
    if p <= 0 or q <= 0 or p + q > 1 or u <= 0 or v <= 0 or u == v:
        raise ValueError('require p,q>0, p+q<=1 and distinct positive u,v')
    P = p + q
    w = 1 - P
    a = p * u + q * v
    c = a / P
    g0 = p * q * (u - v) ** 2 / P
    return P, w, a, c, g0


def variance_floor(s, p, q, u, v):
    s = F(s)
    P, w, a, c, g0 = parameters(p, q, u, v)
    if s < a or (w == 0 and s != a):
        raise ValueError('mean incompatible with required masses')
    if w == 0:
        return g0
    return g0 + (P / w) * (s - c) ** 2


def attaining_squared_law(s, p, q, u, v):
    s, p, q, u, v = map(F, (s, p, q, u, v))
    _, w, a, _, _ = parameters(p, q, u, v)
    variance_floor(s, p, q, u, v)
    if w == 0:
        return [(u, p), (v, q)]
    return [(u, p), (v, q), ((s - a) / w, w)]


def endpoints(x, g):
    x, g = F(x), F(g)
    if x <= 0 or g <= 0:
        raise ValueError('positive scalar inputs required')
    return g * (g + 2 * x) / (g + x), 4 * x * (g + 2 * x) / (g + 4 * x)


def schur(s, g, t):
    s, g, t = map(F, (s, g, t))
    if s <= 0 or g <= 0 or not 0 <= t <= F(1, 4):
        raise ValueError('require s,g>0 and 0<=t<=1/4')
    x = s * s
    D0 = x * (g + x)
    D1 = g * (g + 4 * x) / 4
    D = (1 - 4 * t) * D0 + 4 * t * D1
    return x * g * (g + 2 * x) / D


def evaluate(coefficients, x):
    out = F(0)
    for coefficient in reversed(coefficients):
        out = out * x + coefficient
    return out


def bernstein(coefficients, lo, hi):
    """Exact degree-n Bernstein coefficients after s=lo+(hi-lo)t."""
    lo, hi = F(lo), F(hi)
    if not lo < hi:
        raise ValueError('ordered nonempty interval required')
    n = len(coefficients) - 1
    power = [sum(F(coefficients[k]) * comb(k, j) * lo ** (k-j) *
                 (hi-lo) ** j for k in range(j, n+1)) for j in range(n+1)]
    return [sum(power[j] * F(comb(i,j), comb(n,j)) for j in range(i+1))
            for i in range(n+1)]


def _decimal(n, digits):
    scale = 10 ** digits
    return str(n // scale) + '.' + str(n % scale).zfill(digits)


def outward_decimal(lo, hi, digits=12):
    if lo < 0 or hi < lo:
        raise ValueError('nonnegative ordered bounds required')
    scale = 10 ** digits
    down = lo.numerator * scale // lo.denominator
    up = (hi.numerator * scale + hi.denominator - 1) // hi.denominator
    return [_decimal(down, digits), _decimal(up, digits)]


def certify_example(steps=80):
    """Certify the minimum in the NOTE example, using only rational arithmetic.

    The NOTE proves that the signs of the Bernstein coefficients imply one
    root of P, and that R>0. Bisection then encloses that unique root. The
    rational rectangle evaluation uses the proved monotonicity of endpoint0.
    """
    if type(steps) is not int or not 8 <= steps <= 512:
        raise ValueError('steps must be an integer in [8,512]')
    lo, hi = F(5,4), F(5,2)
    bP, bR = bernstein(POLY_P,lo,hi), bernstein(POLY_R,lo,hi)
    if not (all(x < 0 for x in bP[:-1]) and bP[-1] > 0 and all(x > 0 for x in bR)):
        raise ArithmeticError('polynomial sign certificate failed')
    for _ in range(steps):
        mid = (lo + hi) / 2
        value = evaluate(POLY_P, mid)
        if value == 0:
            raise ArithmeticError('exact rational root requires a separate bracket')
        if value < 0:
            lo = mid
        else:
            hi = mid
    if not (evaluate(POLY_P,lo) < 0 < evaluate(POLY_P,hi)):
        raise ArithmeticError('root bracket failed')
    g_lower = F(9,8) + (hi-F(5,2))**2
    g_upper = F(9,8) + (lo-F(5,2))**2
    lower = endpoints(lo*lo,g_lower)[0]
    upper = endpoints(hi*hi,g_upper)[0]
    other_branch_min = endpoints(F(25,16), F(43,16))[1]
    if not 0 < lower < upper < other_branch_min:
        raise ArithmeticError('branch comparison failed')
    return {
        'schema_version': 1,
        'scientific_effect': 'NONE',
        'independently_reviewed': False,
        'scope': 'sharp real scalar infimum for p=q=1/4, u=1, v=4; not a field certificate',
        'bisection_steps': steps,
        'P_low_to_high': list(POLY_P),
        'R_low_to_high': list(POLY_R),
        'P_Bernstein_on_5over4_5over2': list(map(str,bP)),
        'R_Bernstein_on_5over4_5over2': list(map(str,bR)),
        'minimizer_rational_interval': list(map(str,(lo,hi))),
        'minimizer_decimal_outer': outward_decimal(lo,hi),
        'schur_rational_interval': list(map(str,(lower,upper))),
        'schur_decimal_outer': outward_decimal(lower,upper),
        'other_branch_minimum': str(other_branch_min),
        'independent_lower_input_bound': '153/86',
        'conservative_bound': '9/8',
        'attainment': 'X law: (1/4) delta_1 + (1/4) delta_2 + (1/2) delta_sqrt(2*s_star-5/2); t=0',
    }


def render_certificate():
    return json.dumps(certify_example(),sort_keys=True,indent=2)+'\n'


if __name__ == '__main__':
    import argparse
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(render_certificate(),end='')
