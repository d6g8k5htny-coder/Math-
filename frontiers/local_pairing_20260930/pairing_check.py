#!/usr/bin/env python3
"""Exact finite controls for LOCAL_PAIRING.md (standard library only; exact rationals).

Checked here, exactly:
  I0  the shear: [CUB] (C1) evaluated at X = u - aZ/(12k) equals (2.1) with B, D from (C2), at rational points;
  I1  the pinned cubic identities: P(u,Z) = A(u) + (Z^2/2)(s+Bu) + (D/3)Z^3 with A(u) = 2k(u-1)(u+1/2)^2,
      and A(u) + (B u/6) Z^2 = -k(u+1/2) on the conic 6k(u^2-1/4) + (B/2)Z^2 = 0 (CUB (C8)/(C9) consistency);
  I2  at an extra critical point (u1,Z1): P(S1) = A(u1) + Z1^2 (s+Bu1)/6; and the vertical-line derivative
      d/dZ P(u1,Z) = Z (s+Bu1+DZ), checked by exact differentiation of the cubic in Z (a central difference
      of a cubic equals its derivative plus exactly (D/3) h^2, which is subtracted);
  I3  A(u) + k = (k/2)(u+1)(2u-1)^2 and A'(u) = 6ku^2 - 3k/2 at rational points;
  P1  the path cases of Lemma P on a rational grid of the chart (u1, v, Z1, a): every sample is a typed jet
      with an extra strict-window root (n >= 1 by the [CUB] classifier), at least one of the paths V, U applies
      under the V-first assignment (V and U may both apply in case (iv); V is taken first), and the displayed
      path has minimum value > -k with the stated margin, rising past 0 at its far end (sampled at 2Z1, 4Z1,
      resp. 3, 6, 12 on the D side; the monotonicity itself is the one-line calculus of the text, not a check);
      for every chart point whose own root is not V-admissible (case (iv), root on the side u < u0) the OTHER
      root is computed exactly by Vieta on [CUB] (C13) and verified to be a strict-window root on the side
      u > u0, V-admissible, and higher than the chart root (Lemma P's assignment and Proposition 3.3);
  P2  the [ELDER] witness (s,a,beta,c) = (-3k/2,0,-2k,0): both extra saddles at height -7k/32, and the vertical
      line at u = -3/4 is constant (D = 0), so the polygonal path of [ELDER] (E5) is needed there (null case);
  N1  on a rational grid of typed jets with n = 0, the U hypothesis (B < 0 and s > B) never holds: consistency
      of the [CUB] classifier with Lemma P's case (iv), which always has n >= 1;
  M   semantic mutants (--mutant M1|M2|M3|M4) must fail; an unknown label exits 2.

The controls certify algebra, case coverage on the grid and the path minima; they do not prove the Gaussian
transfer (Theorem LP) or the weak convergence consumed from [SC].  Scientific effect: NONE.
"""
import argparse
import json
import sys
from fractions import Fraction as F

K_VALUES = [F(1), F(2), F(1, 3)]


def A(k, u):
    return 2*k*(u - 1)*(u + F(1, 2))**2


def P(k, s, B, D, u, Z):
    return A(k, u) + (Z*Z/2)*(s + B*u) + (D/3)*Z**3


def cub_n(k, s, a, beta, c):
    """[CUB] Theorem C classifier on the typed domain; None if not typed."""
    B = beta - a*a/(12*k)
    D = (c - a*beta/(4*k) + a**3/(72*k*k))/2
    if not (s < -abs(B)/2):
        return None
    T = -(s - B)**2*(B + 2*s)/(12*k)
    if s > B:
        return 2 if D*D < T else 1
    return 1 if D*D > T else 0


def chart(k, u1, v, Z1, a):
    b0 = 3 - 12*u1*u1
    s = -k*v/Z1**2
    B = k*b0/Z1**2
    D = k*(v - b0*u1)/Z1**3
    beta = B + a*a/(12*k)
    c = 2*D + a*B/(4*k) + a**3/(144*k*k)
    return s, B, D, beta, c


def chart_grid():
    us = [F(n, 10) for n in range(-14, 5)]           # -1.4 .. 0.4
    out = []
    for u1 in us:
        b0 = 3 - 12*u1*u1
        lo, hi = abs(b0)/2, 3 - 6*u1
        if not lo < hi:
            continue
        for t in (F(1, 4), F(1, 2), F(3, 4)):
            v = lo + t*(hi - lo)
            for Z1 in (F(-2), F(-1), F(-1, 2), F(-1, 4), F(1, 4), F(1, 2), F(1), F(2)):
                for a in (F(-2), F(-1, 2), F(0), F(1, 2), F(2)):
                    out.append((u1, v, Z1, a))
    return out


def cub_C1(k, s, a, beta, c, X, Z):
    """[CUB] (C1): the unsheared pinned cubic."""
    return 2*k*X**3 - 3*k*X/2 - k/2 + (s/2)*Z*Z + (a/2)*(X*X - F(1, 4))*Z + (beta/2)*X*Z*Z + (c/6)*Z**3


def check_identities(k, mutant):
    rows = 0
    # I0: shear (C2) turns (C1) into (2.1)
    for (s, a, beta, c) in ((F(-3, 2), F(0), F(-2), F(0)), (F(-2), F(1), F(1, 3), F(-5, 7)), (F(-7, 5), F(-3, 2), F(2), F(4))):
        B = beta - a*a/(12*k); D = (c - a*beta/(4*k) + a**3/(72*k*k))/2
        for u in (F(-1), F(-1, 3), F(1, 2), F(5, 4)):
            for Z in (F(-2), F(1, 3), F(3)):
                X = u - a*Z/(12*k)
                if cub_C1(k, s, a, beta, c, X, Z) != P(k, s, B, D, u, Z):
                    return False, 'I0 shear identity fails'
    for u in (F(-3), F(-1), F(-1, 2), F(0), F(1, 2), F(2), F(7, 3)):
        lhs = A(k, u) + k
        rhs = (k/2)*(u + 1)*(2*u - 1)**2
        dA = 6*k*u*u - 3*k/2
        exact_dA = (A(k, u + F(1, 10**6)) - A(k, u - F(1, 10**6)))/(F(2, 10**6))   # central difference of a cubic: exact up to h^2 term
        if lhs != rhs or abs(exact_dA - dA) > F(1, 10**11):
            return False, 'I3 axis identity fails at u=%s' % u
    for u in (F(-3, 2), F(-1), F(-3, 4), F(-1, 2), F(-1, 5), F(0), F(1, 3), F(1, 2), F(2)):
        for Z in (F(-2), F(-1, 3), F(1, 2), F(3)):
            for s in (F(-3), F(-1, 2)):
                for D in (F(-1), F(2, 5)):
                    B = -12*k*(u*u - F(1, 4))/(Z*Z)          # conic through (u,Z)
                    lhs = A(k, u) + (B*u/6)*Z*Z
                    rhs = -k*(u + F(1, 2)) if mutant != 'M3' else -k*(u - F(1, 2))
                    if lhs != rhs:
                        return False, 'I1 conic identity fails at u=%s Z=%s' % (u, Z)
                    # I2: P at a critical point on the line s + Bu + DZ = 0 -> solve for D given (s,B,u,Z)
                    Dc = -(s + B*u)/Z
                    if P(k, s, B, Dc, u, Z) != A(k, u) + Z*Z*(s + B*u)/6:
                        return False, 'I2 critical value formula fails'
                    # derivative identity in Z by exact differentiation: for a cubic q(Z) the central
                    # difference (q(Z+h)-q(Z-h))/(2h) equals q'(Z) + (leading coefficient) h^2 exactly
                    h = F(1, 7)
                    central = (P(k, s, B, D, u, Z + h) - P(k, s, B, D, u, Z - h))/(2*h) - (D/3)*h*h
                    if central != Z*(s + B*u + D*Z):
                        return False, 'I2 derivative identity fails'
                    rows += 1
    return True, rows


def path_case(k, s, B, D, u1, Z1):
    """Return (case, margin, message) for the explicit path of Lemma P at the extra root (u1, Z1).

    V: vertical descent at u1 (needs s + B u1 < 0 and -1 < u1 < 1/2): the path is M -> axis -> (u1,0)
       -> straight down the vertical line to S1 -> on to P -> +infinity; minimum P(S1).
    U: vertical rise at u0 = -s/B (needs B < 0, s > B, D != 0): M -> axis -> (u0,0) -> vertical line, on
       which P = A(u0) + D Z^3/3; minimum A(u0).
    Lemma P: every typed jet with a strict-window extra root admits V or U (B = 0 is included in V; D = 0
    with B < 0 < ... is the [ELDER] null case handled by its polygonal path).
    """
    P1 = P(k, s, B, D, u1, Z1)
    if s + B*u1 < 0 and -1 < u1 < F(1, 2):
        if not (A(k, u1) > P1 > -k):
            return 'V', None, 'ordering A(u1) > P(S1) > -k fails'
        if not ((D > 0) == (Z1 > 0)):
            return 'V', None, 'root not on the D side'
        far1 = P(k, s, B, D, u1, 2*Z1); far2 = P(k, s, B, D, u1, 4*Z1)
        if not (far1 > P1 and far2 > far1 and far2 > 0):
            return 'V', None, 'vertical line does not rise past 0'
        return 'V', P1 + k, 'ok'
    if B < 0 and s > B:
        u0 = -s/B
        if not (-1 < u0 < -F(1, 2)):
            return 'U', None, 'u0 outside (-1,-1/2)'
        if D == 0:
            return 'U', None, 'D = 0 (null case, [ELDER] path)'
        if not (A(k, u0) > -k):
            return 'U', None, 'A(u0) <= -k'
        Zf = F(3) if D > 0 else F(-3)
        if not (P(k, s, B, D, u0, Zf) == A(k, u0) + D*Zf**3/3 and P(k, s, B, D, u0, 2*Zf) > P(k, s, B, D, u0, Zf) > A(k, u0)):
            return 'U', None, 'vertical line at u0 not monotone'
        if not (P(k, s, B, D, u0, 4*Zf) > 0):
            return 'U', None, 'vertical line at u0 does not pass 0 by |Z|=12'
        return 'U', A(k, u0) + k, 'ok'
    return 'none', None, 'no path case applies (would contradict Lemma P)'


def check_paths(mutant):
    counts = {'V': 0, 'U': 0, 'V_at_other_root': 0}
    total = 0
    min_margin = None
    for k in K_VALUES:
        for (u1, v, Z1, a) in chart_grid():
            s, B, D, beta, c = chart(k, u1, v, Z1, a)
            if mutant == 'M1':
                s = -abs(B)/2 + F(1, 100)            # break the typed condition
            n = cub_n(k, s, a, beta, c)
            if n is None or n < 1:
                return False, 'chart sample not typed/n>=1 at %s' % ((k, u1, v, Z1, a),)
            # (u1,Z1) is a critical point in the strict window
            P1 = P(k, s, B, D, u1, Z1)
            if mutant == 'M2':
                P1 = P1 - k                            # pretend the root sits below the window
            if not (-k < P1 < 0):
                return False, 'root not in the strict window'
            gu = 6*k*u1*u1 - 3*k/2 + (B/2)*Z1*Z1      # d/du of the sheared cubic
            gz = Z1*(s + B*u1 + D*Z1)
            if not (gu == 0 and gz == 0):
                return False, 'chart point is not a critical point'
            case, margin, msg = path_case(k, s, B, D, u1, Z1)
            if margin is None:
                return False, 'case %s: %s at %s' % (case, msg, (k, u1, v, Z1, a))
            if mutant == 'M4':
                margin = -margin
            if not margin > 0:
                return False, 'nonpositive margin'
            counts[case] += 1; total += 1
            min_margin = margin if min_margin is None else min(min_margin, margin)
            if case == 'U':
                # the chart root is on the side u1 < u0; Lemma P assigns V at the other root S_V (u > u0).
                # [CUB] (C13): (12kD^2+B^3) u^2 + 2B^2 s u + B s^2 - 3kD^2 = 0 has the two roots' u-coordinates.
                lead = 12*k*D*D + B**3
                if lead == 0:
                    return False, 'U sample with a single finite root (leading coefficient of (C13) zero)'
                u2 = -2*B*B*s/lead - u1
                Z2 = -(s + B*u2)/D
                gu2 = 6*k*u2*u2 - 3*k/2 + (B/2)*Z2*Z2
                if gu2 != 0 or not (-k < P(k, s, B, D, u2, Z2) < 0):
                    return False, 'other root is not a strict-window critical point'
                u0 = -s/B
                case2, margin2, msg2 = path_case(k, s, B, D, u2, Z2)
                if not (u2 > u0 and case2 == 'V' and margin2 is not None):
                    return False, 'other root is not V-admissible on the side u > u0: %s' % msg2
                if not (P(k, s, B, D, u2, Z2) > P(k, s, B, D, u1, Z1)):
                    return False, 'other root is not the higher saddle'
                counts['V_at_other_root'] += 1
    return True, {'samples': total, 'cases': counts, 'min_margin': str(min_margin)}


def check_elder_witness(mutant):
    k = F(1)
    s, a, beta, c = F(-3, 2), F(0), F(-2), F(0)
    B = beta - a*a/(12*k); D = (c - a*beta/(4*k) + a**3/(72*k*k))/2
    n = cub_n(k, s, a, beta, c)
    u0 = -s/B                                            # = -3/4
    # the two extra saddles: line s + Bu = 0 (D = 0) and conic
    Z2 = -12*k*(u0*u0 - F(1, 4))/B
    h = A(k, u0) + Z2*(s + B*u0)/6
    const = all(P(k, s, B, D, u0, Z) == A(k, u0) for Z in (F(0), F(1), F(9, 4), F(-3)))
    ok = (n == 2 and u0 == F(-3, 4) and Z2 == F(15, 8) and h == F(-7, 32) and const and D == 0)
    if mutant == 'M3':
        ok = ok and h == F(-1, 4)
    return ok, {'n': n, 'u0': str(u0), 'Z1_squared': str(Z2), 'saddle_height': str(h), 'vertical_line_constant': const}


def check_n0(mutant):
    """On typed grid jets with n = 0 the U hypothesis (B < 0 and s > B) never holds ([CUB] (C6): s > B gives n >= 1)."""
    k = F(1); found = 0; u_hypothesis = 0
    for s in (F(-3), F(-5, 2), F(-2), F(-3, 2), F(-1), F(-1, 2)):
        for a in (F(-1), F(0), F(1)):
            for beta in (F(-3), F(-1), F(0), F(1), F(2)):
                for c in (F(-2), F(0), F(2)):
                    n = cub_n(k, s, a, beta, c)
                    if n == 0:
                        found += 1
                        B = beta - a*a/(12*k)
                        if B < 0 and s > B:
                            u_hypothesis += 1
    if mutant == 'M4':
        u_hypothesis += 1
    return found > 0 and u_hypothesis == 0, {'n0_typed_grid_points': found, 'n0_points_with_U_hypothesis': u_hypothesis}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--mutant', default=None)
    args = parser.parse_args(argv)
    if args.mutant is not None and args.mutant not in ('M1', 'M2', 'M3', 'M4'):
        print('unknown mutant label', file=sys.stderr)
        return 2
    report = {'object': 'CL-LOCAL-PAIRING-20260930-v1', 'scientific_effect': 'NONE', 'checks': {}}
    ok_all = True
    for name, fn in (('I0_I3_identities', lambda: check_identities(F(1), args.mutant)),
                     ('P1_path_cases', lambda: check_paths(args.mutant)),
                     ('P2_elder_witness', lambda: check_elder_witness(args.mutant)),
                     ('N1_n0_grid', lambda: check_n0(args.mutant))):
        ok, info = fn()
        report['checks'][name] = {'passed': bool(ok), 'info': info}
        ok_all = ok_all and bool(ok)
    report['passed'] = ok_all
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if ok_all else 1


if __name__ == '__main__':
    raise SystemExit(main())
