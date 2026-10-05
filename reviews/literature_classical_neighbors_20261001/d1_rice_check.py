#!/usr/bin/env python3
"""Deterministic check of the d = 1 small-amplitude constant of ADDENDUM.md section 3 (CL-LIT-CLASSICAL-NEIGHBORS-20261001-v1.1).
Standard library only (Decimal for the covariance algebra, floating point for the final one-dimensional integrals).

For the stationary Gaussian process with covariance r(t) = exp(-t^2/2) (lambda2 = 1, lambda4 = 3, lambda6 = 15), the
intensity per unit length of pairs (maximum at 0, minimum at t > 0) with X(0) - X(t) in dh is the two-point Rice density

    g(t, h) = p_{X'(0), X'(t), X(0)-X(t)}(0, 0, h) E[ X''(0)^- X''(t)^+ | X'(0) = X'(t) = 0, X(0) - X(t) = h ].

It is evaluated exactly in distribution (no sampling) in the rescaled rows U1 = (X'(0)+X'(t))/2, U2 = (X'(t)-X'(0))/t,
U3 = (6/t^2)[X'(0)+X'(t)+2(X(0)-X(t))/t] (Jacobian 12/t^4, and U3 = 12h/t^3 on the event), with the bivariate
expectation reduced to one Gauss-Legendre integral.  With f(h) = int_0^{1.5} g(t, h) dt, the prediction of section 3 is

    h^(1/3) f(h) -> C nu_max,   C = Gamma(7/6) 72^(-1/6) (2 pi)^(-1/2) (lambda6 - lambda4^2/lambda2)^(2/3) / lambda4,
                                nu_max = (2 pi)^(-1) (lambda4/lambda2)^(1/2)          (h -> 0).

  R1  the spectral moments of r and tau^2 = lambda6 - lambda4^2/lambda2 = 6, exactly (rationals);
  R2  h^(1/3) f(h) / (C nu_max) at h = 10^-2 ... 10^-10: within 5e-5 of 1 for h <= 1e-8, and the deviation shrinks
      monotonically over h <= 1e-3 (it is consistent with a relative correction of order h^(7/12));
  M   mutants (--mutant M1|M2) exit 1: M1 uses tau^2 = 5 in the prediction, M2 drops the factor 12 of the Jacobian;
      an unknown label exits 2.
  Scope: a check of the constant's arithmetic through the exact two-point Rice formula (pairs at separations up to
  1.5, intermediate extrema not excluded, which affects only the regular part).  It is not a proof of the d = 1 law.
"""
import argparse
import json
import math
import sys
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

getcontext().prec = 50


def He_dec(n, t):
    if n == 0:
        return D(1)
    h0, h1 = D(1), t
    for k in range(1, n):
        h0, h1 = h1, t * h1 - k * h0
    return h1


def rder(n, t):
    return (-1) ** n * He_dec(n, t) * (-(t * t) / 2).exp()


def cov_pt(i, si, j, sj):
    return (-1) ** j * rder(i + j, si - sj)


def solve(M, b):
    n = len(M)
    A = [M[i][:] + [b[i]] for i in range(n)]
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[p] = A[p], A[i]
        for r in range(n):
            if r != i:
                f = A[r][i] / A[i][i]
                A[r] = [x - f * y for x, y in zip(A[r], A[i])]
    return [A[i][n] / A[i][i] for i in range(n)]


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def gauss_legendre(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


GLX, GLW = gauss_legendre(64)
KX, KW = gauss_legendre(96)


def Phi(x):
    return 0.5 * math.erfc(-x / math.sqrt(2))


def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def E_negpos(m1, m2, S11, S12, S22):
    """E[(-T1)^+ (T2)^+] for (T1, T2) ~ N((m1, m2), [[S11, S12], [S12, S22]])."""
    mx, sx = -m1, math.sqrt(S11)
    beta = -S12 / S11
    s = math.sqrt(max(S22 - S12 * S12 / S11, 1e-300))
    hi = mx + 12 * sx
    if hi <= 0:
        return 0.0
    lo = max(0.0, mx - 12 * sx)
    tot = 0.0
    for x, w in zip(GLX, GLW):
        xx = lo + (hi - lo) * (x + 1) / 2
        my = m2 + beta * (xx - mx)
        tot += w * (hi - lo) / 2 * xx * phi((xx - mx) / sx) / sx * (my * Phi(my / s) + s * phi(my / s))
    return tot


def g(t, h, jac):
    t, h, z = D(repr(t)), D(repr(h)), D(0)
    pts = [(0, z), (1, z), (2, z), (0, t), (1, t), (2, t)]
    C = [[cov_pt(i, si, j, sj) for (j, sj) in pts] for (i, si) in pts]
    U = [[z, D('0.5'), z, z, D('0.5'), z], [z, -1 / t, z, z, 1 / t, z],
         [12 / t ** 3, 6 / t ** 2, z, -12 / t ** 3, 6 / t ** 2, z]]
    T1 = [z, z, D(1), z, z, z]
    T2 = [z, z, z, z, z, D(1)]

    def cv(a, b):
        return sum(a[i] * C[i][j] * b[j] for i in range(6) for j in range(6))
    CUU = [[cv(a, b) for b in U] for a in U]
    u = [z, z, 12 * h / t ** 3]
    x = solve(CUU, u)
    y1 = solve(CUU, [cv(T1, a) for a in U])
    y2 = solve(CUU, [cv(T2, a) for a in U])
    m1 = sum(cv(T1, U[k]) * x[k] for k in range(3))
    m2 = sum(cv(T2, U[k]) * x[k] for k in range(3))
    S11 = cv(T1, T1) - sum(cv(T1, U[k]) * y1[k] for k in range(3))
    S22 = cv(T2, T2) - sum(cv(T2, U[k]) * y2[k] for k in range(3))
    S12 = cv(T1, T2) - sum(cv(T1, U[k]) * y2[k] for k in range(3))
    q = sum(u[k] * x[k] for k in range(3))
    pU = math.exp(-float(q) / 2) / math.sqrt((2 * math.pi) ** 3 * float(det3(CUU)))
    return pU * jac / float(t) ** 4 * E_negpos(float(m1), float(m2), float(S11), float(S12), float(S22))


def f(h, jac, t0=1.5):
    a, b = math.log(h / t0 ** 3), math.log(4.0)
    tot = 0.0
    for x, w in zip(KX, KW):
        k = math.exp(a + (b - a) * (x + 1) / 2)
        t = (h / k) ** (1 / 3)
        tot += w * (b - a) / 2 * k * (1 / 3) * h ** (1 / 3) * k ** (-4 / 3) * g(t, h, jac)
    return tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', default=None)
    args = ap.parse_args()
    if args.mutant is not None and args.mutant not in ('M1', 'M2'):
        sys.stderr.write('unknown mutant label\n')
        return 2
    # R1: spectral moments of exp(-t^2/2) and tau^2, exactly: lambda_{2j} = (2j-1)!!
    lam = {2 * j: F(math.prod(range(1, 2 * j, 2))) for j in (1, 2, 3)}
    tau2 = lam[6] - lam[4] ** 2 / lam[2]
    r1 = lam[2] == 1 and lam[4] == 3 and lam[6] == 15 and tau2 == 6
    tau2_used = 5.0 if args.mutant == 'M1' else float(tau2)
    C = math.gamma(7 / 6) * 72 ** (-1 / 6) * (2 * math.pi) ** -0.5 * tau2_used ** (2 / 3) / float(lam[4])
    numax = math.sqrt(float(lam[4]) / float(lam[2])) / (2 * math.pi)
    pred = C * numax
    jac = 1.0 if args.mutant == 'M2' else 12.0
    ratios = {}
    for e in range(2, 11):
        h = 10.0 ** (-e)
        ratios[e] = h ** (1 / 3) * f(h, jac) / pred
    small = all(abs(ratios[e] - 1) <= 5e-5 for e in (8, 9, 10))
    mono = all(abs(ratios[e + 1] - 1) < abs(ratios[e] - 1) for e in range(3, 9))
    r2 = small and mono
    out = {'object': 'CL-LIT-CLASSICAL-NEIGHBORS-20261001-v1.1 d1 Rice check', 'scientific_effect': 'NONE',
           'mutant': args.mutant, 'passed': bool(r1 and r2),
           'checks': {'R1_spectral_moments': {'passed': r1, 'info': {'lambda2': '1', 'lambda4': '3', 'lambda6': '15', 'tau2': str(tau2)}},
                      'R2_two_point_rice_ratio': {'passed': r2, 'info': {
                          'C': float('%.9g' % C), 'nu_max': float('%.9g' % numax), 'C_nu_max': float('%.9g' % pred),
                          'ratio_h^(1/3)f(h)/(C nu_max)': {('1e-%d' % e): float('%.7f' % ratios[e]) for e in ratios}}}}}
    sys.stdout.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
    return 0 if out['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
