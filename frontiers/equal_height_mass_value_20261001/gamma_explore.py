#!/usr/bin/env python3
"""EXPLORATION for NOTE.md (CL-EQUAL-HEIGHT-MASS-20261001-v1).  Standard library only, floating point, fixed seed.
NOT a control, NOT replayed by the workflow (a few minutes).

The near-field correction of Proposition V in d = 3 for the Gaussian kernel exp(-|z|^2/2):

    gamma_3 = 4 pi int_0^oo s^2 [ I(s) - beta_3 ] ds,     I(s) := int_R Psi_0(b, s e_1) db,

Psi_0 the equal-height kernel (Z2) of the stationary field on R^3: Psi_0(b, y) = p_y(v_b) E[|det H_0 det H_y|
1{H_0 < 0, index H_y = 2} | O_y = v_b], O_y = (f, grad f)(0), (f, grad f)(y), v_b = (b, 0, b, 0).  The conditional law of
the two Hessians is Gaussian with mean b m(s) and a covariance S(s) independent of b (exact covariance derivatives of
the kernel through probabilists' Hermite polynomials); E[. | b] is estimated by Monte Carlo over the residual with
common random numbers across b, and the b-integral uses Gauss-Hermite nodes for the weight exp(-q b^2/2).
beta_3 is taken from equal_height_mass.py (deterministic).  Output: GAMMA.json.
"""
import json
import math
import random
import sys

BETA3 = 7.400614572e-4          # equal_height_mass.py, Q4 (24^3 beta_3 = 10.23061)


def He(n, x):
    if n == 0:
        return 1.0
    h0, h1 = 1.0, x
    for k in range(1, n):
        h0, h1 = h1, x * h1 - k * h0
    return h1


def dK(g, z):
    out = 1.0
    for gk, zk in zip(g, z):
        out *= (-1) ** gk * He(gk, zk) * math.exp(-zk * zk / 2)
    return out


def cov(a, Pa, b, Pb):
    return (-1) ** sum(b) * dK(tuple(x + y for x, y in zip(a, b)), tuple(p - q for p, q in zip(Pa, Pb)))


OBS = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
HES = [(2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 1, 0), (1, 0, 1), (0, 1, 1)]


def solve_many(M, cols):
    """M^{-1} [cols] by Gauss-Jordan with partial pivoting."""
    n = len(M)
    A = [M[i][:] + [c[i] for c in cols] for i in range(n)]
    k = len(cols)
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[p] = A[p], A[i]
        piv = A[i][i]
        A[i] = [x / piv for x in A[i]]
        for r in range(n):
            if r != i and A[r][i] != 0.0:
                f = A[r][i]
                A[r] = [x - f * y for x, y in zip(A[r], A[i])]
    return [[A[i][n + j] for i in range(n)] for j in range(k)]


def logdet(M):
    n = len(M)
    A = [row[:] for row in M]
    s = 0.0
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[p] = A[p], A[i]
        piv = A[i][i]
        s += math.log(abs(piv))
        for r in range(i + 1, n):
            f = A[r][i] / piv
            A[r] = [x - f * y for x, y in zip(A[r], A[i])]
    return s


def cholesky(S):
    n = len(S)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            v = S[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                L[i][i] = math.sqrt(max(v, 1e-14))
            else:
                L[i][j] = v / L[j][j]
    return L


def hermite_nodes(n):
    """Gauss-Hermite nodes/weights for exp(-x^2)."""
    xs, ws = [], []
    for i in range(n):
        if i == 0:
            x = math.sqrt(2 * n + 1) - 1.85575 * (2 * n + 1) ** (-1 / 6)
        elif i == 1:
            x = xs[0] - 1.14 * n ** 0.426 / xs[0]
        elif i == 2:
            x = 1.86 * xs[1] - 0.86 * xs[0]
        elif i == 3:
            x = 1.91 * xs[2] - 0.91 * xs[1]
        else:
            x = 2 * xs[i - 1] - xs[i - 2]
        for _ in range(200):
            p1, p2 = math.pi ** -0.25, 0.0
            for j in range(1, n + 1):
                p3 = p2
                p2 = p1
                p1 = x * math.sqrt(2 / j) * p2 - math.sqrt((j - 1) / j) * p3
            pp = math.sqrt(2 * n) * p2
            dx = p1 / pp
            x -= dx
            if abs(dx) < 1e-15:
                break
        xs.append(x)
        ws.append(2 / (pp * pp))
    return xs, ws


def det3(a, b, c, d, e, f):
    return a * (b * c - f * f) - d * (d * c - f * e) + e * (d * f - b * e)


def I_of_s(s, NS, rng, hx, hw):
    P0, P1 = (0.0, 0.0, 0.0), (s, 0.0, 0.0)
    O = [(a, P0) for a in OBS] + [(a, P1) for a in OBS]
    H = [(a, P0) for a in HES] + [(a, P1) for a in HES]
    COO = [[cov(a, Pa, b, Pb) for (b, Pb) in O] for (a, Pa) in O]
    CHO = [[cov(a, Pa, b, Pb) for (b, Pb) in O] for (a, Pa) in H]
    CHH = [[cov(a, Pa, b, Pb) for (b, Pb) in H] for (a, Pa) in H]
    e = [1.0, 0, 0, 0, 1.0, 0, 0, 0]
    sol = solve_many(COO, [e] + [row for row in CHO])
    ce, X = sol[0], sol[1:]                      # C_OO^-1 e and C_OO^-1 C_OH (columns)
    q = sum(ei * ci for ei, ci in zip(e, ce))
    m = [sum(CHO[i][k] * ce[k] for k in range(8)) for i in range(12)]
    S = [[CHH[i][j] - sum(CHO[i][k] * X[j][k] for k in range(8)) for j in range(12)] for i in range(12)]
    L = cholesky(S)
    pref = math.exp(-0.5 * logdet(COO) - 4 * math.log(2 * math.pi))
    scale = math.sqrt(2 / q)
    bs = [x * scale for x in hx]
    NB = 5
    per = NS // NB
    batches = []
    acc = [0.0] * len(bs)
    for it in range(per * NB):
        z = [rng.gauss(0.0, 1.0) for _ in range(12)]
        R = [sum(L[i][k] * z[k] for k in range(i + 1)) for i in range(12)]
        for t, b in enumerate(bs):
            h = [R[i] + b * m[i] for i in range(12)]
            if not (h[0] < 0 and h[0] * h[1] - h[3] * h[3] > 0):
                continue
            d0 = det3(h[0], h[1], h[2], h[3], h[4], h[5])
            if d0 >= 0:
                continue
            d1 = det3(h[6], h[7], h[8], h[9], h[10], h[11])
            if d1 <= 0 or (h[6] > 0 and h[6] * h[7] - h[9] * h[9] > 0):
                continue
            acc[t] += -d0 * d1
        if (it + 1) % per == 0:
            batches.append(pref * scale * sum(w * a / per for w, a in zip(hw, acc)))
            acc = [0.0] * len(bs)
    return batches


def main():
    NS = int(sys.argv[1]) if len(sys.argv) > 1 else 200000      # GAMMA.json: the default (about two minutes)
    rng = random.Random(20261001)
    hx, hw = hermite_nodes(20)
    ss = [0.25 * j for j in range(1, 19)]          # 0.25 .. 4.5
    per_s = [I_of_s(s, NS, rng, hx, hw) for s in ss]
    vals = [sum(b) / len(b) for b in per_s]

    def gamma(v):
        # trapezoid in s on [0, 4.5] (the s^2 weight vanishes at 0); the integrand is negligible beyond 4.5
        g, prev_s, prev_f = 0.0, 0.0, 0.0
        for s, x in zip(ss, v):
            f = 4 * math.pi * s * s * (x - BETA3)
            g += 0.5 * (s - prev_s) * (f + prev_f)
            prev_s, prev_f = s, f
        return g
    gb = [gamma([b[k] for b in per_s]) for k in range(len(per_s[0]))]
    g = sum(gb) / len(gb)
    se = math.sqrt(sum((x - g) ** 2 for x in gb) / (len(gb) - 1) / len(gb))
    out = {'object': 'CL-EQUAL-HEIGHT-MASS-20261001-v1 exploration', 'not_a_control': True,
           'samples_per_separation': NS, 'beta_3': BETA3,
           'I_of_s': {('%.2f' % s): float('%.4g' % v) for s, v in zip(ss, vals)},
           'gamma_3': float('%.4g' % g), 'gamma_3_se_batches': float('%.2g' % se),
           'B_3_24': float('%.6g' % (24 ** 3 * BETA3 + g)),
           'method': 'two-point conditional Gaussian law (exact Hermite covariance derivatives), Monte Carlo over the '
                     'Hessian residual with common random numbers in b, Gauss-Hermite (20) in b, trapezoid in s, step 0.25'}
    sys.stdout.write(json.dumps(out, indent=1, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
