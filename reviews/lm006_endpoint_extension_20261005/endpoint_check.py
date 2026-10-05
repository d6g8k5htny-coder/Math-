#!/usr/bin/env python3
"""Exact rational controls for NOTE.md. Not an analytic or Lean proof.

Run with Python's standard library only. M1--M5 intentionally alter a named
factor, sign, subtraction, prescribed gap, or Gaussian dimension.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import json
import sys


def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, Q)):
        raise TypeError('exact int or Fraction required')
    return Q(x)


def radius(r):
    r = rational(r)
    if r <= 0:
        raise ValueError('r must be positive')
    return r


def six(values):
    values = tuple(rational(v) for v in values)
    if len(values) != 6:
        raise ValueError('exactly six coordinates required')
    return values


def frame(raw, r, mutant=None):
    r = radius(r)
    fm, dxm, hym, fp, dxp, hyp = six(raw)
    p0, p1, p2 = (fm+fp)/2, (dxm+dxp)/2, (hym+hyp)/2
    factor = 6 if mutant == 'M1' else 12
    return (p0, p1, p2, (dxp-dxm)/r, (hyp-hym)/r,
            factor/r**2*(p1-(fp-fm)/r))


def unframe(values, r):
    r = radius(r)
    p0, p1, p2, p3, p4, p5 = six(values)
    shift = r*p1/2-r**3*p5/24
    return (p0-shift, p1-r*p3/2, p2-r*p4/2,
            p0+shift, p1+r*p3/2, p2+r*p4/2)


def prescribed_pins(b, r, mutant=None):
    b, r = rational(b), radius(r)
    sign = 1 if mutant == 'M4' else -1
    return (b, Q(0), Q(0), b+sign*r**3/6, Q(0), Q(0))


def poly(p):
    p = tuple(rational(c) for c in p)
    if not p:
        raise ValueError('nonempty polynomial required')
    return p


def value(p, x):
    out = Q(0)
    for coefficient in reversed(p):
        out = out*x+coefficient
    return out


def diff(p, n=1):
    p = poly(p)
    for _ in range(n):
        p = tuple(j*p[j] for j in range(1,len(p))) or (Q(0),)
    return p


def weighted_integral(p, r, kernel):
    # Integrate kernel(u)*p(r*u) on [-1/2,1/2] exactly.
    terms = Q(0)
    for j, coefficient in enumerate(poly(p)):
        for k, weight in enumerate(poly(kernel)):
            power = j+k+1
            terms += coefficient*r**j*weight*(Q(1,2)**power-Q(-1,2)**power)/power
    return terms


def direct(f, h, r, mutant=None):
    r = radius(r)
    f, h = poly(f), poly(h)
    df, d2f, dh = diff(f), diff(f,2), diff(h)
    m, p = -r/2, r/2
    raw = (value(f,m),value(df,m),value(h,m),value(f,p),value(df,p),value(h,p))
    _, _, _, p3, p4, p5 = frame(raw,r,mutant)
    subtract3, subtract4 = (0,0) if mutant == 'M3' else (p3,p4)
    return {'P3':p3, 'P4':p4, 'P5':p5,
            'Aminus':(value(d2f,m)-subtract3)/r,
            'Aplus':(value(d2f,p)-subtract3)/r,
            'Bminus':(value(dh,m)-subtract4)/r,
            'Bplus':(value(dh,p)-subtract4)/r}


def kernels(f, h, r, mutant=None):
    r = radius(r)
    minus = (Q(1,2),Q(-1)) if mutant == 'M2' else (Q(-1,2),Q(1))
    plus = (Q(1,2),Q(1))
    d3f, d2h = diff(f,3),diff(h,2)
    return {'P3':weighted_integral(diff(f,2),r,(1,)),
            'P4':weighted_integral(diff(h),r,(1,)),
            'P5':weighted_integral(d3f,r,(Q(3,2),0,-6)),
            'Aminus':weighted_integral(d3f,r,minus),
            'Aplus':weighted_integral(d3f,r,plus),
            'Bminus':weighted_integral(d2h,r,minus),
            'Bplus':weighted_integral(d2h,r,plus)}


def gaussian_norm8(d, mutant=None):
    if isinstance(d,bool) or not isinstance(d,int):
        raise TypeError('dimension must be an integer')
    if d <= 0:
        raise ValueError('dimension must be positive')
    if mutant == 'M5':
        return 105  # invalid substitution of the scalar normal eighth moment
    return d*(d+2)*(d+4)*(d+6)


def run_checks(mutant=None):
    counts = Counter()
    def check(group, actual, expected):
        if actual != expected:
            raise ValueError(f'{group}: {actual!r} != {expected!r}')
        counts[group] += 1
    radii = (Q(1,128),Q(1,50),Q(1,7),Q(1,2),Q(1),Q(5,2))
    for r in radii:
        for j in range(1,21):
            raw = tuple(Q((-1)**i*(j+i),i+1) for i in range(6))
            check('frame_inversion',unframe(frame(raw,r,mutant),r),raw)
        for b in (Q(6,5),Q(-3),Q(0)):
            check('conditioned_frame',frame(prescribed_pins(b,r,mutant),r,mutant),
                  (b-r**3/12,Q(0),Q(0),Q(0),Q(0),Q(2)))
        for j in range(14):
            p = (Q(0),)*j+(Q(1),)
            lhs,rhs = direct(p,p,r,mutant),kernels(p,p,r,mutant)
            for key in lhs:
                check('kernel_identity',lhs[key],rhs[key])
        v = direct((0,0,1),(0,),r,mutant)
        check('subtraction_control',(v['Aminus'],v['Aplus']),(0,0))
    for d, expected in ((1,105),(2,384),(6,5760)):
        check('normal_eighth_moment',gaussian_norm8(d,mutant),expected)
    for k, mass in (((Q(3,2),0,-6),Q(1)),((Q(-1,2),1),Q(-1,2)),((Q(1,2),1),Q(1,2))):
        check('kernel_mass',weighted_integral((1,),Q(1),k),mass)
    return {'passed':True,'counts':dict(sorted(counts.items())),
            'total':sum(counts.values()),'arithmetic':'fractions.Fraction',
            'scope':'finite exact algebra controls; no field acceptance or Lean execution'}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant',choices=['M1','M2','M3','M4','M5'])
    args=parser.parse_args(argv)
    try:
        result=run_checks(args.mutant)
    except (ValueError,TypeError) as exc:
        print('ENDPOINT_CHECK_FAIL: '+str(exc),file=sys.stderr)
        return 1
    print(json.dumps(result,sort_keys=True,indent=2))
    return 0


if __name__=='__main__':
    sys.exit(main())
