#!/usr/bin/env python3
"""Exact finite controls for PROOF.md (CL-FAR-ELDER-RATE-20260930-v1).  Standard library only; exact rationals.

  B1  the barrier inequality (1.1) on an explicit polynomial f(z) = -z1^2 - 2 z2^2 + z1^3 + z1 z2^2 - z1^2 z2 on
      R^2 (maximum at 0, lambda = 2): with K an explicit upper bound of 1 + sup||D^2 f|| + sup||D^3 f|| on the unit
      ball (Frobenius bounds, which only enlarge K) and R = a_L lambda / K (L = 24, a_L = 1), f(z) <= -(lambda/3)|z|^2
      holds at every rational grid point with |z| <= R;
  B2  the algebraic core of (1.1): (K/6) t^3 <= (lambda/6) t^2 for 0 <= t <= lambda/K, at rational (lambda, K, t);
      and the constants a_L = min(1, L/4), c_L = a_L^2/3 for L in {1, 2, 4, 24};
  I1  the split integral of section 3: for rational 0 < u <= 1 and q with 3q/2 > 2,
      int_0^u lambda dlambda + int_u^1 lambda (u/lambda)^(3q/2) dlambda = u^2/2 + (u^2 - u^(3q/2))/(3q/2 - 2),
      evaluated exactly at u = 1/4, 1/9, 1/100 and q in {2, 4}, and bounded by u^2 (1/2 + 1/(3q/2 - 2));
  I2  the exponent ledger by exact monomial substitution: u^3 = A^(2/q) ell gives u^2 = A^(4/(3q)) ell^(2/3);
      the cumulative count exponent 2/3 + 1 = 5/3; the inverse-moment threshold: q + 2/3 > -1 iff q > -5/3;
  N1  near-pair consistency: c_L (6 k r)^3 / K^2 <= k r^3 iff K >= 6 sqrt(6 c_L) k; (6 sqrt(6 c_L))^2 = 216 c_L < 144
      checked exactly at c_L in {1/3, 1/12, 1/48}, and the constraint verified at K = 1 + 12k for a rational (k, r);
  M   semantic mutants (--mutant M1|M2|M3|M4) exit 1; an unknown label exits 2.
"""
import argparse
import json
import sys
from fractions import Fraction as F


def f_poly(z1, z2):
    return -z1*z1 - 2*z2*z2 + z1**3 + z1*z2*z2 - z1*z1*z2


def check_barrier_polynomial(mutant):
    lam = F(2)                         # eigenvalues of -Hess f(0) = diag(2, 4)
    # explicit bound of 1 + sup||D^2 f|| + sup||D^3 f|| on |z| <= 1 (Frobenius norms majorise operator norms):
    # D^2 f = [[-2 + 6 z1 - 2 z2, 2 z2 - 2 z1], [2 z2 - 2 z1, -4 + 2 z1]]; on the unit ball the entries are
    # bounded by 10, 4, 4, 6, so the Frobenius norm is <= sqrt(100 + 16 + 16 + 36) = sqrt(168) < 13;
    # D^3 f entries: f111 = 6, f112 = f121 = f211 = -2, f122 = f212 = f221 = 2, f222 = 0 -> Frobenius sqrt(60) < 8
    K = F(1) + F(13) + F(8)
    if mutant == 'M1':
        K = F(1)                        # too small a K breaks the barrier radius
    aL = F(1)                           # L = 24 -> a_L = min(1, 6) = 1
    R = aL*lam/K
    checked = 0
    n = 24
    for i in range(-n, n+1):
        for j in range(-n, n+1):
            z1 = R*F(i, n); z2 = R*F(j, n)
            if z1*z1 + z2*z2 > R*R:
                continue
            if f_poly(z1, z2) > -(lam/3)*(z1*z1 + z2*z2):
                return False, 'barrier (1.1) fails at z=(%s,%s)' % (z1, z2)
            checked += 1
    return True, {'grid_points_in_ball': checked, 'R': str(R), 'K': str(K), 'lambda': str(lam)}


def check_algebra(mutant):
    for lam in (F(1, 3), F(2), F(7)):
        for K in (lam, 2*lam, 10*lam + 1):
            for t in [lam/K*F(n, 8) for n in range(0, 9)]:
                cubic = (K/6)*t**3; quad = (lam/6)*t*t
                if mutant == 'M2':
                    cubic = (K/6)*t**3*2
                if cubic > quad:
                    return False, 'core inequality fails at lam=%s K=%s t=%s' % (lam, K, t)
    consts = {}
    for L in (F(1), F(2), F(4), F(24)):
        aL = min(F(1), L/4); cL = aL*aL/3
        consts['L=%s' % L] = {'a_L': str(aL), 'c_L': str(cL)}
    if consts['L=24']['c_L'] != '1/3' or consts['L=1']['c_L'] != '1/48':
        return False, 'constants a_L, c_L wrong'
    return True, consts


def rational_pow(u, e):
    """u^e for Fraction u and Fraction e when the result is rational (u a perfect power); else None."""
    num, den = u.numerator, u.denominator
    p, q = e.numerator, e.denominator
    def root(n, q):
        r = round(n ** (1.0/q))
        for cand in (r-1, r, r+1):
            if cand >= 0 and cand**q == n:
                return cand
        return None
    rn, rd = root(num, q), root(den, q)
    if rn is None or rd is None:
        return None
    base = F(rn, rd)
    return base**p if p >= 0 else 1/(base**(-p))


def check_split_integral(mutant):
    rows = {}
    for q in (F(2), F(4)):
        e = 3*q/2                        # exponent 3q/2
        for u in (F(1, 4), F(1, 9), F(1, 100)):
            # int_0^u lambda dlambda = u^2/2
            first = u*u/2
            # int_u^1 lambda (u/lambda)^e dlambda = u^e int_u^1 lambda^(1-e) = u^e (1 - u^(2-e))/(2-e) = (u^2 - u^e)/(e-2)
            ue = rational_pow(u, e)
            if ue is None:
                return False, 'non-rational power'
            second = (u*u - ue)/(e-2)
            total = first + second
            bound = u*u*(F(1, 2) + 1/(e-2))
            if mutant == 'M3':
                bound = u*u*F(1, 2)
            if total > bound:
                return False, 'split integral exceeds its bound at u=%s q=%s' % (u, q)
            # independent evaluation of the second piece: u^e * [F(1) - F(u)] with F(x) = x^(2-e)/(2-e)
            u2e = rational_pow(u, 2-e)
            second_alt = ue*((F(1) - u2e)/(2-e))
            if second_alt != second:
                return False, 'second piece: antiderivative evaluation disagrees with the closed form'
            rows['q=%s,u=%s' % (q, u)] = str(total)
    return True, rows


class Mono:
    def __init__(self, ell=F(0), A=F(0)):
        self.ell, self.A = F(ell), F(A)
    def __mul__(self, o):
        return Mono(self.ell+o.ell, self.A+o.A)
    def __pow__(self, e):
        e = F(e); return Mono(self.ell*e, self.A*e)
    def key(self):
        return (self.ell, self.A)


def check_exponents(mutant):
    for q in (F(2), F(4), F(10)):
        ell, A = Mono(1, 0), Mono(0, 1)
        u3 = (A**(2/q))*ell                 # u^3
        u = u3**F(1, 3)
        u2 = u**2
        want = (F(2, 3), 4/(3*q))
        if mutant == 'M4':
            want = (F(1, 3), 4/(3*q))
        if u2.key() != want:
            return False, 'u^2 monomial wrong for q=%s: %s' % (q, u2.key())
    if F(2, 3) + 1 != F(5, 3):
        return False, 'count exponent'
    # inverse moments: int_0^t ell^(q + 2/3) dell finite at 0 iff q + 2/3 > -1 iff q > -5/3
    for qq in (F(-5, 3) + F(1, 100), F(-1), F(0)):
        if not (qq + F(2, 3) > -1):
            return False, 'moment threshold'
    if F(-5, 3) + F(2, 3) > -1:
        return False, 'threshold endpoint'
    return True, {'u^2 exponent of ell': '2/3', 'count exponent': '5/3', 'inverse moment threshold': '-5/3'}


def check_near_consistency(mutant):
    # c_L (6kr)^3 / K^2 <= k r^3  <=>  216 c_L k^2 <= K^2  <=>  K >= 6 sqrt(6 c_L) k ; and 36*6*c_L < 144 for c_L <= 1/3
    for cL in (F(1, 3), F(1, 48), F(1, 12)):
        if not (36*6*cL < 144):
            return False, 'near consistency fails for c_L=%s' % cL
        k, r = F(2, 5), F(1, 7)
        K = 12*k + 1
        if not (cL*(6*k*r)**3/(K*K) <= k*r**3):
            return False, 'near-pair barrier constraint violated at K = 1 + 12k'
    return True, {'6*sqrt(6 c_L) < 12 for c_L <= 1/3': True}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', default=None)
    args = ap.parse_args()
    mutant = args.mutant
    if mutant is not None and mutant not in ('M1', 'M2', 'M3', 'M4'):
        sys.stderr.write('unknown mutant label\n'); sys.exit(2)
    results = {}
    ok_all = True
    for name, fn in (('B1_barrier_polynomial', check_barrier_polynomial), ('B2_algebra_and_constants', check_algebra),
                     ('I1_split_integral', check_split_integral), ('I2_exponent_ledger', check_exponents),
                     ('N1_near_consistency', check_near_consistency)):
        ok, info = fn(mutant)
        results[name] = {'passed': bool(ok), 'info': info}
        ok_all = ok_all and ok
    out = {'object': 'CL-FAR-ELDER-RATE-20260930-v1', 'scientific_effect': 'NONE', 'passed': ok_all, 'checks': results}
    print(json.dumps(out, indent=1, sort_keys=True))
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
