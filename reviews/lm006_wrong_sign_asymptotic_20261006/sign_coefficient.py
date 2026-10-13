#!/usr/bin/env python3
"""Exact finite diagnostics for the LM006 wrong-sign leading coefficient.

No infinite-field integral, Gaussian simulation, numerical coefficient enclosure,
Lean proof, or scientific acceptance is supplied by this program. The continuum
argument and its exact product-covariance assumptions are in NOTE.md.
"""
from __future__ import annotations

from fractions import Fraction as F
import json
from typing import Mapping, Sequence

Rational = int | F


def band_integral(d: Rational, u: Rational) -> F:
    """Integral of (d-u-t)_+ (u-t)_+ over 0 <= t <= d_+."""
    d, u = F(d), F(u)
    if u < 0:
        raise ValueError('u is a square and must be nonnegative')
    if u == 0 or d <= u:
        return F(0)
    lo, hi = min(u, d-u), max(u, d-u)
    return lo**2 * (3*hi-lo) / 6


def layer_weight(am: Rational, ap: Rational, bm: Rational, bp: Rational,
                 d: Rational, t: Rational) -> F:
    """Exact two-factor rescaled sign layer, with its t >= 0 event."""
    am, ap, bm, bp, d, t = map(F, (am, ap, bm, bp, d, t))
    if t < 0:
        return F(0)
    return max(max(-am, 0)*max(d-t, 0)-bm**2, 0)*max(bp**2-ap*t, 0)


def physical_weight(r: Rational, am: Rational, ap: Rational, bm: Rational,
                    bp: Rational, cm: Rational, cp: Rational) -> F:
    """Original determinant/type weight for the two physical Hessians."""
    r, am, ap, bm, bp, cm, cp = map(F, (r, am, ap, bm, bp, cm, cp))
    if r <= 0:
        raise ValueError('physical radius must be positive')
    det_m, det_s = r*am*cm-r*r*bm*bm, r*ap*cp-r*r*bp*bp
    if r*am < 0 and det_m > 0 and det_s < 0:
        return -det_m*det_s
    return F(0)


def transverse_means(m2: Rational, b: Rational, r: Rational) -> tuple[F, F]:
    m2, b, r = map(F, (m2, b, r))
    return -m2*(b-r**3/12), m2*r**2/6


def transpose(a: Sequence[Sequence[Rational]]) -> list[list[F]]:
    return [list(map(F, row)) for row in zip(*a)]


def matmul(a: Sequence[Sequence[Rational]], b: Sequence[Sequence[Rational]]) -> list[list[F]]:
    if not a or not b or any(len(row) != len(b) for row in a):
        raise ValueError('incompatible matrix dimensions')
    if any(len(row) != len(b[0]) for row in b):
        raise ValueError('ragged matrix')
    return [[sum((F(x)*F(y) for x,y in zip(row,col)), F(0))
             for col in zip(*b)] for row in a]


def inverse(a: Sequence[Sequence[Rational]]) -> list[list[F]]:
    n = len(a)
    if n == 0 or any(len(row) != n for row in a):
        raise ValueError('nonempty square matrix required')
    rows = [list(map(F,row))+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j,n) if rows[i][j]), None)
        if pivot is None:
            raise ValueError('singular matrix')
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [x/scale for x in rows[j]]
        for i in range(n):
            if i != j:
                factor = rows[i][j]
                rows[i] = [x-factor*y for x,y in zip(rows[i],rows[j])]
    return [row[n:] for row in rows]


def diagnostic_spectra() -> list[dict[int,F]]:
    """Three finite even probability spectra; NONE is the exact torus spectrum."""
    return [{0:F(1,3),-1:F(1,6),1:F(1,6),-2:F(1,6),2:F(1,6)},
            {i:F(1,7) for i in range(-3,4)},
            {0:F(1,2),-1:F(1,8),1:F(1,8),-3:F(1,8),3:F(1,8)}]


def moments(weights: Mapping[int,Rational], order: int) -> list[F]:
    w = {k:F(v) for k,v in weights.items()}
    if sum(w.values(),F(0)) != 1 or any(v <= 0 for v in w.values()):
        raise ValueError('positive probability masses required')
    if any(w.get(-k,F(0)) != v for k,v in w.items()):
        raise ValueError('even spectrum required')
    return [sum((v*F(k)**j for k,v in w.items()),F(0)) for j in range(order+1)]


def derivative_cov(alpha: tuple[int,int], beta: tuple[int,int], m: Sequence[F]) -> F:
    powers = (alpha[0]+beta[0], alpha[1]+beta[1])
    if any(x % 2 for x in powers):
        return F(0)
    sign = -1 if (sum(beta)+sum(powers)//2) % 2 else 1
    return sign*m[powers[0]]*m[powers[1]]


PINS = ((0,0),(1,0),(0,1),(2,0),(1,1),(3,0))
TARGETS = ((0,2),(2,1),(1,2))  # q, twice B, D


def contact_regression(m: Sequence[F], b: Rational) -> tuple[list[F],list[list[F]]]:
    """Compute from the full finite product-jet covariance, not from the answer."""
    gram = [[derivative_cov(x,y,m) for y in PINS] for x in PINS]
    cross = [[derivative_cov(x,y,m) for y in PINS] for x in TARGETS]
    target = [[derivative_cov(x,y,m) for y in TARGETS] for x in TARGETS]
    regression = matmul(cross,inverse(gram))
    mean = [row[0] for row in matmul(regression,[[F(b)],[0],[0],[0],[0],[2]])]
    removed = matmul(regression,transpose(cross))
    return mean, [[x-y for x,y in zip(row,loss)] for row,loss in zip(target,removed)]


def contact_laws(m2: Rational, m4: Rational, b: Rational) -> dict[str,F]:
    m2,m4,b = map(F,(m2,m4,b))
    delta = m4-m2*m2
    if m2 <= 0 or delta <= 0:
        raise ValueError('positive m2 and spectral-square variance required')
    return {'mean_q':-m2*b,'variance_q':delta,
            'variance_B':m2*delta/4,'variance_D':m2*delta}


def residual_cross(joint: Mapping[tuple[int,int],Rational]) -> F:
    """Cov(Q + E[Y^2] F, F_xx) at contact, without a product assumption."""
    if sum(map(F,joint.values()),F(0)) != 1:
        raise ValueError('probability weights required')
    x2 = sum((F(p)*x*x for (x,y),p in joint.items()),F(0))
    y2 = sum((F(p)*y*y for (x,y),p in joint.items()),F(0))
    x2y2 = sum((F(p)*x*x*y*y for (x,y),p in joint.items()),F(0))
    return x2y2-x2*y2


def power_ledger() -> dict[str,int]:
    return {'transverse_factors':2,'density_variable':1,'normalized_numerator':3,
            'physical_numerator':5,'physical_normalizer':2,'probability':3}


def diagnostics() -> dict:
    rows = []
    for weights in diagnostic_spectra():
        m = moments(weights,10)
        mean,cov = contact_regression(m,F(6,5))
        laws = contact_laws(m[2],m[4],F(6,5))
        expected = [[laws['variance_q'],0,0],
                    [0,4*laws['variance_B'],0],[0,0,laws['variance_D']]]
        if mean != [laws['mean_q'],0,0] or cov != expected:
            raise AssertionError('contact regression does not match the stated laws')
        rows.append({'m2':str(m[2]),'m4':str(m[4]),
                     'laws':{k:str(v) for k,v in laws.items()}})
    return {'object':'LM006-WRONG-SIGN-ASYMPTOTIC-20261006',
            'scientific_effect':'NONE','mathematical_acceptance':False,
            'scope':'finite rational identities only; no infinite-field coefficient evaluated',
            'spectral_models':rows,'positive_box_integral_floor':'5/1024',
            'band_examples':{'J(2,1)':str(band_integral(2,1)),
                             'J(3,1)':str(band_integral(3,1))},
            'power_ledger':power_ledger()}


if __name__=='__main__':
    print(json.dumps(diagnostics(),sort_keys=True,indent=2))
