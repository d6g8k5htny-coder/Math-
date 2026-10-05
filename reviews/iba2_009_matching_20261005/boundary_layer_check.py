#!/usr/bin/env python3
"""Exact finite checks for IBA2-009's moving-layer obstruction.

Standard library only. This diagnostic is not a Gaussian-field counterexample,
not an independent audit of imported estimates, and not a proof by sampling.
The general calculation is in REPORT.md. No check uses an assert statement.

Usage: python3 -B -S boundary_layer_check.py [--mutant M1|M2|M3|M4|M5]
Valid source exits 0 with deterministic JSON. Each documented mutant exits 1.
Invalid arguments exit 2. Optimized Python has the same behavior.
"""
from fractions import Fraction as F
import argparse
import json
from math import comb, factorial
import sys


class CheckFailure(ValueError):
    """An exact diagnostic invariant was violated."""


def require(condition, label):
    if not condition:
        raise CheckFailure(label)


def bump(t):
    """C^3 bump (t-1)^4(2-t)^4 supported on [1,2]."""
    t = F(t)
    return (t - 1)**4 * (2 - t)**4 if 1 < t < 2 else F(0)


def bump_integral(order=4):
    """Integral_1^2 (t-1)^m(2-t)^m dt by exact polynomial integration."""
    if not isinstance(order, int) or isinstance(order, bool) or order < 1:
        raise ValueError('positive integer order required')
    return sum((F((-1)**j * comb(order,j), order+j+1)
                for j in range(order+1)), F(0))


def lifetime_coefficient():
    return bump_integral() / 5


def scaling_exponents():
    # ell=k*r^3 and k^3/r fixed: solve a+3b=1 and 3a-b=0.
    return F(3,10), F(1,10), F(-1,5)  # r, k, kappa


def run_checks(mutant=None):
    if mutant not in (None, 'M1','M2','M3','M4','M5'):
        raise ValueError('unknown mutation')
    counts = dict(moving_layer=0,compact_cusp=0,fixed_gap=0,small_gap=0,integrals=0)
    xs = (F(1,64),F(1,32),F(1,16),F(1,8),F(1,4))
    ss = (F(1),F(21,20),F(11,10),F(9,8),F(8,7))
    for x in xs:
        for s in ss:
            ell=x**10; r=x**3/s; k=x*s**3; kappa=k/r; t=s**5
            y=k**3/(r**2 if mutant=='M1' else r)
            require(ell==k*r**3, 'CUBIC_LIFETIME')
            require(y==t**2==r**2*kappa**3, 'MOVING_LAYER_ARGUMENT')
            require(1<=t<2 and 0<r<=k<=F(1,2), 'K2_DOMAIN')
            h=bump(t); H=k**2*h
            raw=H if mutant=='M2' else r**2*H
            require(raw/r**2==H, 'LIFETIME_JACOBIAN')
            require(0<=h<=1, 'BUMP_BOUND')
            require(0<=raw<=k**2, 'NONNEGATIVE_SPLIT')
            require(raw<=4*r**3/k, 'C7_K2_BOUND')
            require(H<=k**2<=r**2+k**2, 'UNIFORM_QUADRATIC_BOUND')
            require(H<=r*(1+kappa), 'CE_PLUS_PLUS_BOUND')
            require(r**2*kappa**2==(-r)**2*kappa**2, 'FIXED_KAPPA_EVENNESS')
            # r=x^3/s, k=x*s^3, dr=-x^3/s^2 ds, t=s^5.
            jac=x**3/s**2
            exponent=6 if mutant=='M5' else 5
            require(H*jac==x**exponent*s**4*h, 'HALF_POWER_SCALING')
            require(s**4==5*s**4/5, 'FIFTH_POWER_SUBSTITUTION')
            counts['moving_layer']+=1
    for kappa in (F(1,4),F(1,2),F(1),F(2),F(4),F(16)):
        for j in range(1,6):
            r=1/(8*j*(1+kappa)**2)
            y=r**2*kappa**3
            active=(True if mutant=='M4' else 1<y<4)
            require(y<1 and not active, 'COMPACT_CUSP_VANISHING')
            counts['compact_cusp']+=1
    for k in (F(1,16),F(1,8),F(1,4),F(1,3),F(1,2)):
        for j in range(1,6):
            r=k**3/(8*j); y=k**3/r
            require(y>4, 'FIXED_GAP_VANISHING')
            counts['fixed_gap']+=1
    for r in (F(1,16),F(1,8),F(1,4),F(1,2),F(1)):
        for q in (F(1,4),F(1,2),F(3,4),F(1)):
            k=q*r
            require(k**3/r<=1, 'SMALL_GAP_REGION_UNCHANGED')
            counts['small_gap']+=1
    for m in (1,2,4):
        require(bump_integral(m)==F(factorial(m)**2,factorial(2*m+1)), 'BUMP_INTEGRAL')
        counts['integrals']+=1
    coefficient=bump_integral() if mutant=='M3' else lifetime_coefficient()
    require(coefficient==F(1,3150), 'INTEGRATION_FACTOR_ONE_FIFTH')
    rpower,kpower,kappapower=scaling_exponents()
    require(kpower+3*rpower==1 and 3*kpower-rpower==0, 'BAND_POWERS')
    require(2*kpower+rpower==F(1,2), 'HALF_POWER_EXPONENT')
    require(kpower-rpower==kappapower, 'ESCAPING_KAPPA')
    return {'status':'ESTIMATE_LEVEL_OBSTRUCTION_PASS','coefficient':str(coefficient),
            'counts':counts,'scientific_effect':'NONE','scientific_acceptance':False,
            'gaussian_counterexample':False,'global_absence_proved':False}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant',choices=('M1','M2','M3','M4','M5'))
    args=parser.parse_args(argv)
    try:
        result=run_checks(args.mutant)
    except CheckFailure as exc:
        print('BOUNDARY_LAYER_CHECK_FAIL: '+str(exc),file=sys.stderr)
        return 1
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
