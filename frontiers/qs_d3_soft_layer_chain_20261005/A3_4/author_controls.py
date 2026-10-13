#!/usr/bin/env python3
"""Exact controls (standard library only) for CL-QS-A3-4-SOFT-LAYER-LAW-20261005-v1.

Usage:  python3 -B -S a34_exact.py             -> JSON summary on stdout, exit 0 iff every check passes
        python3 -B -S a34_exact.py --mutant Nk  -> runs with mutant Nk (N1..N6); must exit 1 (failure on stderr)
Unknown arguments exit 2. Output is byte-identical under -O (no check depends on an assert statement).

These check finite algebra only; the analytic steps of A3.4 are argued in the text, not tested.
  S1  Lemma S: for A = -R diag(mu1, mu2) R^T with the rational rotation c = (1 - tau^2)/(1 + tau^2), s = 2 tau/(1 + tau^2),
      the exact Jacobian of (A11, A12, A22) in (mu1, mu2, tau) is |mu2 - mu1| * 2/(1 + tau^2) (and dtheta/dtau = 2/(1 + tau^2));
      -A e1 = mu1 e1, -A e2 = mu2 e2; with mu1 = r lt/k the Jacobian in (lt, lam2, tau) is (r/k)|lam2 - r lt/k| 2/(1 + tau^2).
  S2  Lemma CM3's rank step: U0, A and t are exactly the 20 multi-indices of order <= 3 in (x, y1, y2), with no repetition;
      the 20 x 20 monomial matrix at the principal lattice {a in N^3 : |a| <= 3} is invertible (exact determinant).
  S3  Eigenframe jets: on random rational cubics, gamma = d_u^2 d_e1 f(0) and B = d_u d_e1^2 f(0), read off the restriction
      f(sigma u + rho e1) as polynomial coefficients, equal c t_xx1 + s t_xx2 and c^2 t_x11 + 2cs t_x12 + s^2 t_x22;
      w is invariant under e1 -> -e1; |b_theta|^2 = c^4 + 4c^2 s^2 + s^4 = 1 + 2c^2 s^2 lies in [1, 3/2].
  S4  Edge algebra: a_M + a_S = 12 lt, w = s(12 lt - s) on T with s = a_M or a_S, d a_M/dB = 3k = -d a_S/dB, w = 0 if lt <= 0.
  S5  Strip integral: I(delta) = int_0^Lam dlt int_0^{min(delta, 12 lt)} s(12 lt - s) ds, by exact piecewise integration, has
      (8/3) Lam^2 <= I/delta^2 <= 3 Lam^2 + Lam^2/96 for 0 < delta <= Lam, and equals its closed form.
"""
import json
import random
import sys
from fractions import Fraction as Fr
from itertools import product
from math import factorial

MUTANT = None


def fail(msg):
    sys.stderr.write(json.dumps({'failed': msg}) + '\n')
    sys.exit(1)


def det(M):
    """Exact determinant by Gaussian elimination over Fractions."""
    n = len(M)
    A = [[Fr(x) for x in row] for row in M]
    d = Fr(1)
    for i in range(n):
        piv = None
        for k in range(i, n):
            if A[k][i] != 0:
                piv = k
                break
        if piv is None:
            return Fr(0)
        if piv != i:
            A[i], A[piv] = A[piv], A[i]
            d = -d
        d *= A[i][i]
        for k in range(i + 1, n):
            if A[k][i] != 0:
                f = A[k][i] / A[i][i]
                A[k] = [A[k][j] - f * A[i][j] for j in range(n)]
    return d


def rq(lo, hi, den):
    return Fr(random.randint(lo * den, hi * den), den)


# ------------------------------------------------------------------------------------------------------------------- S1
def s1(n_cases=400):
    checks = 0
    for _ in range(n_cases):
        mu1, mu2, tau = rq(-5, 5, 7), rq(-5, 5, 11), rq(-3, 3, 13)
        q = 1 + tau * tau
        c, s = (1 - tau * tau) / q, 2 * tau / q
        dc, ds = -4 * tau / (q * q), 2 * (1 - tau * tau) / (q * q)
        if c * c + s * s != 1:
            fail('S1 rational rotation is not orthonormal')
        # A = -R diag(mu1, mu2) R^T, R = [[c, -s], [s, c]]
        A11, A12, A22 = -(mu1 * c * c + mu2 * s * s), -(mu1 - mu2) * c * s, -(mu1 * s * s + mu2 * c * c)
        # eigenvectors of -A
        e1, e2 = (c, s), (-s, c)
        for (lam, e) in ((mu1, e1), (mu2, e2)):
            v = (-(A11 * e[0] + A12 * e[1]), -(A12 * e[0] + A22 * e[1]))
            if v != (lam * e[0], lam * e[1]):
                fail('S1 eigenvector identity fails')
        J = [[-c * c, -s * s, -(2 * mu1 * c * dc + 2 * mu2 * s * ds)],
             [-c * s, c * s, -(mu1 - mu2) * (dc * s + c * ds)],
             [-s * s, -c * c, -(2 * mu1 * s * ds + 2 * mu2 * c * dc)]]
        dth = 2 / q
        target = abs(mu2 - mu1) * dth
        if MUTANT == 'N1':
            target = dth
        if abs(det(J)) != target:
            fail('S1 spectral Jacobian fails: mu1=%s mu2=%s tau=%s' % (mu1, mu2, tau))
        checks += 1
        # soft-layer substitution mu1 = r lt/k: chain rule factor r/k
        r, k, lt = rq(1, 1, 1) / random.choice([10, 100, 1000]), random.choice([Fr(1, 2), Fr(1), Fr(3, 2)]), rq(-4, 4, 3)
        m1 = r * lt / k
        Jb = [[J[0][0] * r / k, J[0][1], 0], [J[1][0] * r / k, J[1][1], 0], [J[2][0] * r / k, J[2][1], 0]]
        # recompute the tau column at mu1 = m1, mu2 = mu2
        Jb[0][2] = -(2 * m1 * c * dc + 2 * mu2 * s * ds)
        Jb[1][2] = -(m1 - mu2) * (dc * s + c * ds)
        Jb[2][2] = -(2 * m1 * s * ds + 2 * mu2 * c * dc)
        if abs(det(Jb)) != (r / k) * abs(mu2 - m1) * dth:
            fail('S1 soft-layer Jacobian fails')
        checks += 1
    return {'checks': checks}


# ------------------------------------------------------------------------------------------------------------------- S2
def s2():
    U0 = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (1, 0, 1)]
    A = [(0, 2, 0), (0, 1, 1), (0, 0, 2)]
    t = [al for al in product(range(4), repeat=3) if sum(al) == 3 and al != (3, 0, 0)]
    if MUTANT == 'N6':
        t = [(1, 1, 0) if al == (1, 1, 1) else al for al in t]
    allm = sorted(al for al in product(range(4), repeat=3) if sum(al) <= 3)
    listed = U0 + A + t
    if len(U0) != 8 or len(A) != 3 or len(t) != 9 or len(set(listed)) != len(listed) or sorted(listed) != allm:
        fail('S2 the 20 contact functionals are not the distinct multi-indices of order <= 3')
    pts = [p for p in product(range(4), repeat=3) if sum(p) <= 3]
    if MUTANT == 'N2':
        pts = [(a, b, 0) for a in range(5) for b in range(4)]
    M = [[Fr(p[0] ** al[0] * p[1] ** al[1] * p[2] ** al[2]) for al in allm] for p in pts]
    d = det(M)
    if len(pts) != 20 or d == 0:
        fail('S2 the monomial matrix at the lattice points is singular')
    return {'functionals': len(listed), 'lattice_points': len(pts), 'det_nonzero': True}


# ------------------------------------------------------------------------------------------------------------------- S3
def poly_restrict(coef, c, s):
    """coef: dict alpha -> coefficient of x^a1 y1^a2 y2^a3; return dict (i, j) -> coefficient of sigma^i rho^j of
    f(sigma u + rho e1), u = (1, 0, 0), e1 = (0, c, s)."""
    out = {}
    for al, v in coef.items():
        a1, a2, a3 = al
        # sigma^a1 (rho c)^a2 (rho s)^a3
        key = (a1, a2 + a3)
        out[key] = out.get(key, Fr(0)) + v * c ** a2 * s ** a3
    return out


def s3(n_cases=300):
    checks = 0
    for _ in range(n_cases):
        coef = {al: rq(-9, 9, 5) for al in product(range(4), repeat=3) if sum(al) == 3}
        tau = rq(-4, 4, 7)
        q = 1 + tau * tau
        c, s = (1 - tau * tau) / q, 2 * tau / q

        def d3(al):  # third partial at 0 in the fixed frame
            return factorial(al[0]) * factorial(al[1]) * factorial(al[2]) * coef[al]
        txx1, txx2 = d3((2, 1, 0)), d3((2, 0, 1))
        tx11, tx12, tx22 = d3((1, 2, 0)), d3((1, 1, 1)), d3((1, 0, 2))
        g = poly_restrict(coef, c, s)
        gamma_true = 2 * g.get((2, 1), Fr(0))   # d_sigma^2 d_rho of sigma^2 rho is 2
        B_true = 2 * g.get((1, 2), Fr(0))       # d_sigma d_rho^2 of sigma rho^2 is 2
        gamma_f = c * txx1 + s * txx2
        B_f = c * c * tx11 + 2 * c * s * tx12 + s * s * tx22
        if MUTANT == 'N3':
            B_f = c * tx11 + s * tx22
        if gamma_true != gamma_f or B_true != B_f:
            fail('S3 eigenframe jet formulas fail')
        g2 = poly_restrict(coef, -c, -s)
        if 2 * g2.get((2, 1), Fr(0)) != -gamma_true or 2 * g2.get((1, 2), Fr(0)) != B_true:
            fail('S3 sign behaviour under e1 -> -e1 fails')
        k, lt = random.choice([Fr(1, 2), Fr(1), Fr(2)]), rq(-3, 3, 4)
        Y1 = 3 * k * B_true - gamma_true ** 2 / 4
        Y2 = 3 * k * B_true - (-gamma_true) ** 2 / 4
        w1 = max(6 * lt + Y1, Fr(0)) * max(6 * lt - Y1, Fr(0))
        w2 = max(6 * lt + Y2, Fr(0)) * max(6 * lt - Y2, Fr(0))
        bb = c ** 4 + 4 * c * c * s * s + s ** 4
        if w1 != w2 or bb != 1 + 2 * c * c * s * s or not (1 <= bb <= Fr(3, 2)):
            fail('S3 invariance or |b_theta|^2 range fails')
        checks += 1
    return {'checks': checks}


# ------------------------------------------------------------------------------------------------------------------- S4
def s4(n_cases=2000):
    checks = 0
    for _ in range(n_cases):
        lt, gam, B = rq(-4, 4, 9), rq(-6, 6, 7), rq(-6, 6, 5)
        k = random.choice([Fr(1, 3), Fr(1), Fr(5, 2)])
        Y = 3 * k * B - gam * gam / 4
        aM, aS = 6 * lt + Y, 6 * lt - Y
        tot = 6 * lt if MUTANT == 'N4' else 12 * lt
        if aM + aS != tot:
            fail('S4 a_M + a_S != 12 lt')
        w = max(aM, Fr(0)) * max(aS, Fr(0))
        if aM > 0 and aS > 0:
            if w != aM * (12 * lt - aM) or w != aS * (12 * lt - aS):
                fail('S4 w != s(12 lt - s) on T')
        if lt <= 0 and w != 0:
            fail('S4 w != 0 for lt <= 0')
        h = Fr(1, 7)
        YB = 3 * k * (B + h) - gam * gam / 4
        if ((6 * lt + YB) - aM) / h != 3 * k or ((6 * lt - YB) - aS) / h != -3 * k:
            fail('S4 d a/dB != +-3k')
        checks += 1
    return {'checks': checks}


# ------------------------------------------------------------------------------------------------------------------- S5
def antider(poly):
    """poly: list of coefficients p[i] of x^i; return the antiderivative's coefficients."""
    return [Fr(0)] + [Fr(c) / (i + 1) for i, c in enumerate(poly)]


def peval(poly, x):
    return sum(c * x ** i for i, c in enumerate(poly))


def strip_integral(Lam, delta):
    # piece 1: lt in [0, delta/12]: inner = int_0^{12 lt} s (12 lt - s) ds = 288 lt^3 (by antiderivative below)
    # piece 2: lt in [delta/12, Lam]: inner = int_0^delta s (12 lt - s) ds = 6 lt delta^2 - delta^3/3
    def inner(lt, upper):
        # int_0^upper (12 lt s - s^2) ds, or the mutant int_0^upper (12 lt - s) ds
        if MUTANT == 'N5':
            P = [12 * lt, Fr(-1)]
        else:
            P = [Fr(0), 12 * lt, Fr(-1)]
        Q = antider(P)
        return peval(Q, upper) - peval(Q, Fr(0))
    # integrate in lt exactly: inner is a polynomial in lt on each piece; integrate by exact Simpson on cubics
    # (Simpson's rule is exact for polynomials of degree <= 3; both pieces have degree <= 3 in lt)
    def simpson(f, a, b):
        return (b - a) / 6 * (f(a) + 4 * f((a + b) / 2) + f(b))
    a = min(delta / 12, Lam)
    I1 = simpson(lambda x: inner(x, 12 * x), Fr(0), a)
    I2 = simpson(lambda x: inner(x, delta), a, Lam) if a < Lam else Fr(0)
    return I1 + I2


def s5():
    checks = 0
    worst_lo, worst_hi = None, None
    for Lam in (Fr(1, 2), Fr(1), Fr(3)):
        for j in range(0, 12):
            delta = Lam / Fr(2) ** j
            I = strip_integral(Lam, delta)
            closed = 3 * Lam * Lam * delta ** 2 - Lam * delta ** 3 / 3 + delta ** 4 / 96
            ratio = I / (delta * delta)
            if MUTANT != 'N5' and I != closed:
                fail('S5 closed form fails at Lam=%s delta=%s' % (Lam, delta))
            if not (Fr(8, 3) * Lam * Lam <= ratio <= 3 * Lam * Lam + Lam * Lam / 96):
                fail('S5 the strip integral is not of order delta^2: Lam=%s delta=%s ratio=%s' % (Lam, delta, ratio))
            worst_lo = ratio / (Lam * Lam) if worst_lo is None else min(worst_lo, ratio / (Lam * Lam))
            worst_hi = ratio / (Lam * Lam) if worst_hi is None else max(worst_hi, ratio / (Lam * Lam))
            checks += 1
    return {'checks': checks, 'min_ratio_over_Lam2': str(worst_lo), 'max_ratio_over_Lam2': str(worst_hi)}


def main():
    global MUTANT
    args = sys.argv[1:]
    if args:
        if len(args) == 2 and args[0] == '--mutant' and args[1] in ('N1', 'N2', 'N3', 'N4', 'N5', 'N6'):
            MUTANT = args[1]
        else:
            sys.stderr.write('usage: a34_exact.py [--mutant N1|N2|N3|N4|N5|N6]\n')
            sys.exit(2)
    random.seed(20261005)
    res = {'object': 'CL-QS-A3-4-SOFT-LAYER-LAW-20261005-v1', 'scientific_effect': 'NONE'}
    res['S1'] = s1()
    res['S2'] = s2()
    res['S3'] = s3()
    res['S4'] = s4()
    res['S5'] = s5()
    res['all_pass'] = True
    sys.stdout.write(json.dumps(res, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
