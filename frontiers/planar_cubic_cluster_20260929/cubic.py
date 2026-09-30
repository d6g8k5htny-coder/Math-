"""Exact planar pinned-cubic classifier. Standard library; rational inputs only.

This checks finite algebra. It does not certify a Gaussian limit theorem.
"""
import argparse
import json
from fractions import Fraction as F

MUTANTS = ('omit-shear', 'omit-cubic-shear', 'close-window', 'swap-weight-sign',
           'claim-three', 'drop-jet-jacobian', 'restrict-normalizer', 'lose-linear-case')


def rational(x):
    if type(x) not in (int, F):
        raise ValueError('exact int or Fraction required')
    return F(x)


def positive_k(k):
    k = rational(k)
    if k <= 0:
        raise ValueError('k must be positive')
    return k


def canonical(k, a, beta, c):
    k = positive_k(k)
    a, beta, c = map(rational, (a, beta, c))
    return beta-a*a/(12*k), (c-a*beta/(4*k)+a**3/(72*k*k))/2


def typed(k, s, B):
    positive_k(k)
    s, B = map(rational, (s, B))
    return s < -abs(B)/2


def threshold(k, s, B):
    k = positive_k(k)
    s, B = map(rational, (s, B))
    if not typed(k, s, B):
        raise ValueError('strict maximum/saddle endpoint types required')
    return -(s-B)**2*(B+2*s)/(12*k)


def window_count(k, s, B, D):
    s, B, D = map(rational, (s, B, D))
    T = threshold(k, s, B)
    if s > B:
        return 2 if D*D < T else 1
    return int(D*D > T)


def weight(k, s, B):
    k = positive_k(k)
    s, B = map(rational, (s, B))
    if not typed(k, s, B):
        raise ValueError('strict typed support required')
    return 9*k*k*(4*s*s-B*B)


def integrated_weight(k, B, lo, hi):
    """Polynomial integral only; does not assert the interval is typed."""
    k = positive_k(k)
    B, lo, hi = map(rational, (B, lo, hi))
    if lo > hi:
        raise ValueError('ordered integration endpoints required')
    return 9*k*k*(F(4,3)*(hi**3-lo**3)-B*B*(hi-lo))


def rare_exponent():
    # Four-dimensional physical jet Jacobian r, two determinants r^4, full Z~r^2.
    return 1+4-2


def sign(x):
    return (x > 0)-(x < 0)


def surd_sign(a, b, d):
    """Exact sign of a+b*sqrt(d), d>=0, without floats."""
    a, b, d = map(rational, (a, b, d))
    if d < 0:
        raise ValueError('nonnegative radicand required')
    if b == 0 or d == 0:
        return sign(a)
    if a == 0 or sign(a) == sign(b):
        return sign(b)
    comparison = sign(a*a-b*b*d)
    return 0 if comparison == 0 else (sign(a) if comparison > 0 else sign(b))


def roots_in_open_interval(A, b, c, lo, hi):
    """Independent algebraic root counter, including linear and double roots."""
    A, b, c, lo, hi = map(rational, (A, b, c, lo, hi))
    if lo >= hi:
        raise ValueError('nonempty open interval required')
    if A == 0:
        if b == 0:
            if c == 0:
                raise ValueError('identically zero polynomial')
            return 0
        return int(lo < -c/b < hi)
    disc = b*b-4*A*c
    if disc < 0:
        return 0
    choices = (0,) if disc == 0 else (-1, 1)
    total = 0
    for eps in choices:
        left = surd_sign(-b-2*A*lo, eps, disc)*sign(A)
        right = surd_sign(-b-2*A*hi, eps, disc)*sign(A)
        total += int(left > 0 and right < 0)
    return total


def conic_oracle(k, s, B, D):
    """Independent count from the stationary conic/line and height intervals.

    Never calls window_count or threshold. Handles B=0 and D=0 separately.
    """
    k = positive_k(k)
    s, B, D = map(rational, (s, B, D))
    if not typed(k, s, B):
        raise ValueError('strict typed support required')
    if B == 0:
        if D == 0:
            return 0
        h = s**3/(6*D*D)
        return int(-k < h < 0) + int(-k < h-k < 0)
    if D == 0:
        u = -s/B
        z2 = -12*k*(u*u-F(1,4))/B
        if z2 <= 0:
            return 0
        h = -k*(u+F(1,2))+s*z2/6
        return 2*int(-k < h < 0)
    end = -F(1,2)-B/(2*s)
    lo, hi = sorted((-F(1,2), end))
    return roots_in_open_interval(12*k*D*D+B**3, 2*B*B*s,
                                  B*s*s-3*k*D*D, lo, hi)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run_checks(mutant=None):
    B, D = canonical(1, 6, 1, F(-3,2))
    if mutant == 'omit-shear': B = F(1)
    if mutant == 'omit-cubic-shear': D = F(-3,2)
    require((B,D) == (F(-2),F(0)), 'exact shear coefficients')
    count = window_count(1,F(-3,2),B,D)
    if mutant == 'claim-three': count = 3
    require(count == 2, 'two-saddle source example')
    boundary = window_count(F(5,12),-2,-1,1)
    if mutant == 'close-window': boundary = 1
    require(boundary == 0, 'strict lower height boundary')
    w = weight(1,F(-3,2),-2)
    if mutant == 'swap-weight-sign': w = -w
    require(w == 45, 'typed determinant product')
    exponent = rare_exponent()
    if mutant == 'drop-jet-jacobian': exponent = 4-2
    if mutant == 'restrict-normalizer': exponent = 1+4-5
    require(exponent == 3, 'physical jet and full normalizer ledger')
    linear = conic_oracle(F(1,12),-1,-1,1)
    if mutant == 'lose-linear-case': linear = 0
    require(linear == 1, 'degree-drop conic case')
    tested = 0
    for k in (F(1,12),F(1),F(3,2)):
        for s in (F(-3),F(-2),F(-3,2),F(-1),F(-1,3)):
            for B in map(F,(-4,-3,-2,-1,0,1,2,3,4)):
                if not typed(k,s,B): continue
                for D in (F(-3),F(-1),F(-1,3),F(0),F(1,10),F(1,3),F(1),F(3)):
                    require(window_count(k,s,B,D) == conic_oracle(k,s,B,D),
                            'classifier disagrees with exact conic roots')
                    tested += 1
    return {'passed': True, 'rational_classifier_cases': tested,
            'scientific_effect': 'NONE', 'mathematical_acceptance': False,
            'dimension': 2, 'scope': 'finite algebra only',
            'groups': ['shear','types','strict-window','weight','rare-ledger','conic-oracle']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant', choices=MUTANTS)
    args = parser.parse_args()
    try:
        result = run_checks(args.mutant)
    except ValueError as exc:
        print(json.dumps({'passed':False, 'error':str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == '__main__': raise SystemExit(main())
