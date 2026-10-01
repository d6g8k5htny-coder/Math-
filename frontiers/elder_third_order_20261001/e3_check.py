#!/usr/bin/env python3
"""Exact controls for CL-ELDER-THIRD-ORDER-20261001-v1 (frontiers/elder_third_order_20261001/PROOF.md).
Standard library only, exact rationals. Run: python3 -B -S e3_check.py   (and with -O; output byte-identical).
Mutants: --mutant M1|M2|M3|M4|M5 must exit 1; an unknown label exits 2.

  X1 the exponent ledger of section 4 (rho_f = l^(1/4+1/44), rho_c = l^(1/4-1/36)): least exponent 4/11, attained
     exactly by rho_f^5/l and l^2 rho_f^-6; the intermediate terms l^(1/4) S^-9, l^2 rho_c^(-7+beta), l^(7/10),
     l^((3+beta)/5) all above 4/11 for beta = min(1/8, 1/(4m)), m = 1..5; rho_c < l^(1/5); and on [l^(1/5), r1] the
     exponent facts kappa <= r and kappa^(1/2) <= r^beta
  X2 the ridge identities (M1), (M5) of Lemma Q as polynomial identities in Q[X, phi], and the closed forms (M4) of
     g(X3) at 401 rational phi (each side times 16 phi^3 is a polynomial of degree <= 8 in phi, so this is an identity)
  X3 the margins (M2)-(M4): the factorizations (phi+1)^3 - 8 phi^3 = (1-phi)(7phi^2+4phi+1) and
     (1+psi)^3 - 64 psi^3 = (1-3psi)(21psi^2+6psi+1); the margin inequalities on dense rational grids; sharpness of 3/2
  X4 the one-dimensional decision of Step Q6 under perturbations h = s (X^2-1/4)^2 q(X), scaled by rigorous coefficient
     bounds to sup|h''| <= kappa/4 and sup|h| < (3/2) kappa ||phi| - 1/3|: the path and trap inequalities of each case
     hold exactly on a rational grid of [-3, 2]
  X5 Lemma CU.1' mechanism: on exactly pinned polynomial fields (d = 2: degree 6, 7; d = 3: degree 6) with k = kappa r,
     every monomial r^a X^i Xi^j of (rescaled field) - (cusp polynomial) has a >= 1 and |j| <= a + 1, attained
  X6 Lemma S (Schur complements) on random rational instances and an extremal one (rigorous rational lower bounds for
     the square roots on the right side); the two polynomial bounds of Step Q2, coefficientwise
  X7 pointwise facts: 0 <= loss <= 9 Y^2 and loss = 36 k^2 D^2 - w_eld; the Lemma O' domination; the B_5 bound
     w <= 12 kappa |D| tau when |Y_r| < 6 kappa |D| < |Y'| and |Y_r - Y'| <= tau
"""
import argparse
import json
import random
import sys
from fractions import Fraction as Fr
from math import factorial, isqrt

MUTANT = None


# ----------------------------------------------------------------------------------------------- X1 exponents
def x1():
    q = Fr(1, 4)
    ef, ec = q + Fr(1, 44), q - Fr(1, 36)
    if MUTANT == 'M1':
        ec = q - Fr(1, 120)
    core = {'rho_f^2': 2 * ef, 'rho_f^5/l': 5 * ef - 1, 'l rho_f^-2': 1 - 2 * ef, 'l^2 rho_f^-6': 2 - 6 * ef,
            'rho_c^2': 2 * ec, 'l^2 rho_c^-7': 2 - 7 * ec}
    ok = True
    rows = {}
    for m in range(1, 6):
        beta = min(Fr(1, 8), Fr(1, 4 * m))
        inter = {'l^(5/2) rho_c^-9': Fr(5, 2) - 9 * ec, 'l^2 rho_c^(-7+beta)': 2 - (7 - beta) * ec,
                 'l^(7/10)': Fr(7, 10), 'l^((3+beta)/5)': (3 + beta) / 5}
        allt = dict(core)
        allt.update(inter)
        least = min(allt.values())
        ok &= least == Fr(4, 11) and sorted(k for k, v in allt.items() if v == least) == ['l^2 rho_f^-6', 'rho_f^5/l']
        ok &= all(v > Fr(4, 11) for v in inter.values())
        # on [l^(1/5), r1], r = l^t with 0 <= t <= 1/5: kappa = l^(1-4t) <= r = l^t and kappa^(1/2) <= r^beta
        for n in range(0, 201):
            t = Fr(1, 5) * Fr(n, 200)
            ok &= (1 - 4 * t) >= t and (1 - 4 * t) / 2 >= beta * t
        rows['m=%d' % m] = {'beta': str(beta), 'least': str(least),
                            'intermediate': {k: str(v) for k, v in sorted(inter.items())}}
    ok &= ec > Fr(1, 5) and ef > q > ec and 1 - 3 * ef >= 0 and Fr(4, 11) > Fr(1, 3)
    return {'core': {k: str(v) for k, v in sorted(core.items())}, 'by_m': rows, 'passed': bool(ok)}


# ----------------------------------------------------------------------------------------------- polynomials in (X, phi)
def padd2(a, b):
    o = dict(a)
    for k, v in b.items():
        o[k] = o.get(k, 0) + v
    return {k: v for k, v in o.items() if v != 0}


def pmul2(a, b):
    o = {}
    for (i, j), u in a.items():
        for (k, l), v in b.items():
            o[(i + k, j + l)] = o.get((i + k, j + l), 0) + u * v
    return {k: v for k, v in o.items() if v != 0}


def psc2(a, c):
    return {k: c * v for k, v in a.items() if c * v != 0}


def cst(c):
    return {(0, 0): Fr(c)} if c != 0 else {}


XX = {(1, 0): Fr(1)}
PH = {(0, 1): Fr(1)}


def pw2(a, n):
    o = cst(1)
    for _ in range(n):
        o = pmul2(o, a)
    return o


def ev2(a, x, ph):
    return sum(v * x ** i * ph ** j for (i, j), v in a.items())


def dX(a):
    return {(i - 1, j): i * v for (i, j), v in a.items() if i > 0}


XP, XM = padd2(XX, cst(Fr(1, 2))), padd2(XX, cst(Fr(-1, 2)))
G = padd2(psc2(pmul2(pw2(XP, 2), padd2(XX, cst(-1))), 2), psc2(pmul2(PH, pw2(pmul2(XP, XM), 2)), 3))   # g / kappa


def g_val(x, ph):
    return ev2(G, x, ph)


def x2():
    ok = True
    r1 = pmul2(pw2(XM, 2), padd2(psc2(padd2(XX, cst(1)), 2), psc2(pmul2(PH, pw2(XP, 2)), 3)))
    ok &= padd2(G, cst(1)) == r1
    r2 = pmul2(pw2(XP, 2), padd2(psc2(padd2(XX, cst(-1)), 2), psc2(pmul2(PH, pw2(XM, 2)), 3)))
    ok &= G == r2
    ok &= dX(G) == psc2(pmul2(pmul2(XP, XM), padd2(cst(1), psc2(pmul2(PH, XX), 2))), 6)
    vals = {}
    for xv, a0, a1 in ((Fr(2), Fr(25, 2), Fr(675, 16)), (Fr(-3, 2), Fr(-5), Fr(12)), (Fr(-3), Fr(-50), Fr(3675, 16))):
        lin = {(0, j): v for (i, j), v in {(i, j): v * xv ** i for (i, j), v in G.items()}.items()}
        coeff = {}
        for (i, j), v in G.items():
            coeff[j] = coeff.get(j, 0) + v * xv ** i
        ok &= coeff.get(0, 0) == a0 and coeff.get(1, 0) == a1 and all(j in (0, 1) for j in coeff if coeff[j] != 0)
        vals[str(xv)] = [str(a0), str(a1)]
    n_ok = 0
    for n in range(-200, 201):
        ph = Fr(n, 200)
        if ph == 0:
            continue
        x3 = -1 / (2 * ph)
        a = 16 * ph ** 3 * (g_val(x3, ph) + 1) == (ph + 1) ** 3 * (3 * ph - 1)
        b = 16 * ph ** 3 * g_val(x3, ph) == (ph - 1) ** 3 * (3 * ph + 1)
        ok &= a and b
        n_ok += a and b
    return {'factorizations': True if ok else False, 'g_at_points': vals, 'X3_closed_forms_at_rational_phi': n_ok,
            'passed': bool(ok and n_ok == 400)}


# ----------------------------------------------------------------------------------------------- X3 margins
def poly1(coeffs):
    return {i: Fr(c) for i, c in enumerate(coeffs) if c != 0}


def pmul1(a, b):
    o = {}
    for i, u in a.items():
        for j, v in b.items():
            o[i + j] = o.get(i + j, 0) + u * v
    return {k: v for k, v in o.items() if v != 0}


def padd1(a, b):
    o = dict(a)
    for k, v in b.items():
        o[k] = o.get(k, 0) + v
    return {k: v for k, v in o.items() if v != 0}


def x3():
    ok = True
    c = Fr(8, 5) if MUTANT == 'M2' else Fr(3, 2)
    one_plus = poly1([1, 1])
    lhs = padd1(pmul1(pmul1(one_plus, one_plus), one_plus), poly1([0, 0, 0, -8]))
    ok &= lhs == pmul1(poly1([1, -1]), poly1([1, 4, 7]))
    lhs2 = padd1(pmul1(pmul1(one_plus, one_plus), one_plus), poly1([0, 0, 0, -64]))
    ok &= lhs2 == pmul1(poly1([1, -3]), poly1([1, 6, 21]))
    ok &= 4 * 4 - 4 * 7 < 0 and 6 * 6 - 4 * 21 < 0          # 7x^2+4x+1 and 21x^2+6x+1 have no real roots
    worst = None
    for n in range(0, 2001):
        ph = Fr(1, 3) + Fr(2, 3) * Fr(n, 2000)                # R+ margin, and (with psi = |phi|) the R- margin
        v = (ph + 1) ** 3 * (3 * ph - 1) / (16 * ph ** 3)
        ok &= v >= c * (ph - Fr(1, 3))
        if n:
            ratio = v / (ph - Fr(1, 3))
            worst = ratio if worst is None else min(worst, ratio)
        ok &= g_val(-1 / (2 * ph), ph) + 1 == v
        ok &= -g_val(1 / (2 * ph), -ph) == v                 # phi -> -phi: |g(X3)| on the R- side
    sharp = (Fr(2) ** 3 * 2 / 16) == Fr(3, 2) * Fr(2, 3)      # equality at phi = 1
    for n in range(0, 1001):
        ps = Fr(1, 4) + Fr(1, 12) * Fr(n, 1000)              # local maximum X3 in (3/2, 2] for -1/3 <= phi < -1/4
        ok &= (ps + 1) ** 3 * (1 - 3 * ps) / (16 * ps ** 3) >= 12 * (Fr(1, 3) - ps)
    for n in range(-100, 101):                               # (M2) on [-1/2, X_R], |phi| <= 1/3
        ph = Fr(n, 300)
        xr = Fr(2) if ph >= Fr(-1, 4) else -1 / (2 * ph)
        for t in range(0, 301):
            x = Fr(-1, 2) + (xr + Fr(1, 2)) * Fr(t, 300)
            ok &= 2 * (x + 1) + 3 * ph * (x + Fr(1, 2)) ** 2 >= 1
    for n in range(-300, 101):                               # (M3) on [-3/2, 1/2], phi <= 1/3
        ph = Fr(n, 300)
        for t in range(0, 201):
            x = Fr(-3, 2) + 2 * Fr(t, 200)
            ok &= 2 * (x - 1) + 3 * ph * (x - Fr(1, 2)) ** 2 <= -1
    # (M5) thresholds
    ok &= Fr(25, 2) + Fr(675, 16) * Fr(-1, 4) == Fr(125, 64) and Fr(25, 2) + Fr(675, 16) * Fr(-1, 3) == Fr(-25, 16)
    ok &= Fr(-5) + 12 * Fr(-1, 3) == -9 and Fr(-50) + Fr(3675, 16) * Fr(1, 3) == Fr(425, 16)
    return {'margin_constant': str(c), 'min_ratio_over_grid': str(worst), 'sharp_at_phi_1': bool(sharp),
            'passed': bool(ok and sharp)}


# ----------------------------------------------------------------------------------------------- X4 decision in 1D
def sup_bound(coeffs):                                       # rigorous bound of sup_{[-3,2]} |sum c_i X^i|
    return sum(abs(c) * Fr(3) ** i for i, c in enumerate(coeffs))


def pmulc(p, q):
    o = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            o[i + j] += a * b
    return o


def deriv(p):
    return [i * p[i] for i in range(1, len(p))] or [Fr(0)]


def evalc(p, x):
    return sum(c * x ** i for i, c in enumerate(p))


def x4(rng):
    thr = Fr(9, 25) if MUTANT == 'M3' else Fr(1, 3)
    base = pmulc([Fr(-1, 4), Fr(0), Fr(1)], [Fr(-1, 4), Fr(0), Fr(1)])   # (X^2 - 1/4)^2
    grid = [Fr(-3) + Fr(5) * Fr(t, 500) for t in range(501)]
    ok = True
    counts = {'E': 0, 'R+': 0, 'R-': 0}
    phis = [Fr(n, 60) for n in range(-60, 61) if abs(abs(Fr(n, 60)) - Fr(1, 3)) > 0] + [Fr(7, 20), Fr(-7, 20)]
    for ph in phis:
        for trial in range(3):
            kap = Fr(rng.randint(1, 400), 100)
            q = [Fr(rng.randint(-50, 50), 25) for _ in range(3)]
            h0 = pmulc(base, q)
            m0 = sup_bound(h0)
            m2 = sup_bound(deriv(deriv(h0)))
            margin = Fr(3, 2) * kap * abs(abs(ph) - Fr(1, 3))
            if m0 == 0 or m2 == 0:
                continue
            s = min(kap / 4 / m2, margin / m0 * Fr(99, 100))
            s *= rng.choice((1, -1)) * Fr(rng.randint(50, 100), 100)
            h = [s * c for c in h0]
            gk = lambda x: kap * g_val(x, ph) + evalc(h, x)
            if abs(ph) < thr:                                   # case E
                counts['E'] += 1
                xr = Fr(2) if ph >= Fr(-1, 4) else -1 / (2 * ph)
                ok &= all(gk(x) + kap >= 0 for x in grid if Fr(-1, 2) <= x <= xr)
                ok &= gk(xr) > 0 and gk(Fr(-3, 2)) < -kap
                ok &= all(gk(x) <= 0 for x in grid if Fr(-3, 2) <= x <= Fr(1, 2))
            elif ph > 0:                                        # case R+
                counts['R+'] += 1
                ok &= all(gk(x) > -kap for x in grid if x <= Fr(-1, 2)) and gk(Fr(-3)) > 0
            else:                                               # case R-
                counts['R-'] += 1
                ok &= all(gk(x) <= 0 for x in grid if Fr(-3, 2) <= x <= 2)
                ok &= gk(Fr(-3, 2)) < -Fr(5, 4) * kap and gk(Fr(2)) < -Fr(5, 4) * kap
    return {'threshold': str(thr), 'cases': counts, 'grid_points': len(grid), 'passed': bool(ok)}


# ----------------------------------------------------------------------------------------------- X5 pinned polynomials
def padd(p, q):
    out = list(p) + [Fr(0)] * max(0, len(q) - len(p))
    for i, c in enumerate(q):
        out[i] += c
    return out


def pmul(p, q):
    out = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                out[i + j] += a * b
    return out


def pscale(p, c):
    return [c * x for x in p]


def rpow(n):
    return [Fr(0)] * n + [Fr(1)]


def axis_odd_sum(c, D, h, shift, skip):
    out = [Fr(0)]
    for i in range(1, D + 2, 2):
        key = c.get(i + shift)
        if key is None or i + shift == skip:
            continue
        out = padd(out, pmul(pscale(rpow(i - 1), h ** (i - 1) / factorial(i)), key))
    return out


def axis_even_sum(c, D, h, skip):
    out = [Fr(0)]
    for i in range(0, D + 2, 2):
        key = c.get(i)
        if key is None or i == skip:
            continue
        out = padd(out, pmul(pscale(rpow(i), h ** i / factorial(i)), key))
    return out


def pinned_field(free, b, kpoly, D, m):
    """free Taylor coefficients (f = sum c_a x^i y^j / (i! j!)); returns all coefficients as polynomials in r, the
    pinned ones solved exactly from the pin rows of [R] section 2 with gap parameter k = kpoly(r)"""
    c = {key: [val] for key, val in free.items()}
    h = Fr(1, 2)
    z = (0,) * m
    ax = {i: c[(i,) + z] for i in range(D + 1) if (i,) + z in c}
    ax[2] = pscale(axis_odd_sum(ax, D, h, 1, 2), Fr(-1))
    rest = [Fr(0)]
    for j in range(5, D + 1, 2):
        if j in ax:
            rest = padd(rest, pmul(pscale(rpow(j - 3), Fr(12 * (j - 1)) * h ** (j - 1) / factorial(j)), ax[j]))
    ax[3] = padd(pscale(kpoly, Fr(12)), pscale(rest, Fr(-1)))
    ax[1] = padd(pscale(pmul(rpow(2), kpoly), Fr(-1)), pscale(axis_odd_sum(ax, D, h, 0, 1), Fr(-1)))
    ax[0] = padd(padd([b], pscale(pmul(rpow(3), kpoly), Fr(-1, 2))), pscale(axis_even_sum(ax, D, h, 0), Fr(-1)))
    for i in range(4):
        c[(i,) + z] = ax[i]
    for l in range(m):
        e = tuple(1 if t == l else 0 for t in range(m))
        tr = {i: c[(i,) + e] for i in range(D) if (i,) + e in c}
        c[(0,) + e] = pscale(axis_even_sum(tr, D, h, 0), Fr(-1))
        c[(1,) + e] = pscale(axis_odd_sum(tr, D, h, 0, 1), Fr(-1))
    return c


def multi_indices(d, D):
    out = []

    def rec(prefix, left, slots):
        if slots == 0:
            out.append(tuple(prefix))
            return
        for v in range(left + 1):
            rec(prefix + [v], left - v, slots - 1)
    rec([], D, d)
    return out


def x5(rng):
    ok = True
    rows = []
    for d, D in ((2, 6), (2, 7), (3, 6)):
        m = d - 1
        unit = lambda l: tuple(1 if t == l else 0 for t in range(m))
        pinned = {(i,) + (0,) * m for i in range(4)}
        for l in range(m):
            pinned |= {(0,) + unit(l), (1,) + unit(l)}
        for trial in range(3):
            kap = Fr(rng.randint(1, 300), 100)
            b = Fr(rng.randint(-300, 300), 97)
            free = {a: Fr(rng.randint(-26, 26), 13) for a in multi_indices(d, D) if a not in pinned}
            c = pinned_field(free, b, [Fr(0), kap], D, m)
            F = {}
            for a, poly in c.items():
                i, j = a[0], a[1:]
                s = i + 2 * sum(j) - 4
                den = factorial(i)
                for t in j:
                    den *= factorial(t)
                for p, v in enumerate(poly):
                    if v:
                        F.setdefault(a, {})
                        F[a][p + s] = F[a].get(p + s, 0) + v / den
            z = (0,) * (m + 1)
            F.setdefault(z, {})
            F[z][-4] = F[z].get(-4, 0) - b
            P = {}

            def addp(a, v):
                P[a] = P.get(a, 0) + v
            f4 = free[(4,) + (0,) * m]
            addp((3,) + (0,) * m, 2 * kap)
            addp((1,) + (0,) * m, -3 * kap / 2)
            addp(z, -kap / 2)
            addp((4,) + (0,) * m, f4 / 24)
            addp((2,) + (0,) * m, -f4 / 48)
            addp(z, f4 / 384)
            for l in range(m):
                gl = free[(2,) + unit(l)]
                addp((2,) + unit(l), gl / 2)
                addp((0,) + unit(l), -gl / 8)
            for l in range(m):
                for q in range(l, m):
                    e = tuple(unit(l)[t] + unit(q)[t] for t in range(m))
                    A = free[(0,) + e]
                    addp((0,) + e, A / 2 if l == q else A)
            gap_min = None
            nmono = 0
            for a in set(F) | set(P):
                lp = dict(F.get(a, {}))
                lp[0] = lp.get(0, 0) - P.get(a, 0)
                for p, v in lp.items():
                    if v == 0:
                        continue
                    nmono += 1
                    j = sum(a[1:])
                    lim = p if MUTANT == 'M4' else p + 1
                    ok &= p >= 1 and j <= lim
                    gap = p + 1 - j
                    gap_min = gap if gap_min is None else min(gap_min, gap)
            ok &= gap_min == 0
            rows.append({'d': d, 'degree': D, 'kappa': str(kap), 'monomials': nmono, 'min_slack': gap_min})
    return {'fields': rows, 'passed': bool(ok)}


# ----------------------------------------------------------------------------------------------- X6 Lemma S
def sqrt_lower(x):                                          # rational lower bound of sqrt(x), x >= 0 rational
    if x <= 0:
        return Fr(0)
    p, q = x.numerator, x.denominator
    if isqrt(p) ** 2 == p and isqrt(q) ** 2 == q:          # exact for rational squares
        return Fr(isqrt(p), isqrt(q))
    scale = 10 ** 12
    return Fr(isqrt(int(x * scale * scale)), scale)


def matinv(M):
    n = len(M)
    A = [list(row) + [Fr(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for col in range(n):
        piv = next(r for r in range(col, n) if A[r][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [v / pv for v in A[col]]
        for r in range(n):
            if r != col and A[r][col] != 0:
                f = A[r][col]
                A[r] = [a - f * b for a, b in zip(A[r], A[col])]
    return [row[n:] for row in A]


def quad(b, M, c):
    return sum(b[i] * M[i][j] * c[j] for i in range(len(b)) for j in range(len(c)))


def neg_def(rng, m, lam):                                   # D = -lam I - S^T S  (so D <= -lam I)
    S = [[Fr(rng.randint(-20, 20), 10) for _ in range(m)] for _ in range(m)]
    return [[-lam * (i == j) - sum(S[t][i] * S[t][j] for t in range(m)) for j in range(m)] for i in range(m)]


def lemma_s_ok(a, b, D, a2, b2, D2, lam, coef):
    s1 = a - quad(b, matinv(D), b)
    s2 = a2 - quad(b2, matinv(D2), b2)
    m = len(b)
    nb = sqrt_lower(sum(x * x for x in b))
    nb2 = sqrt_lower(sum(x * x for x in b2))
    ndb = sqrt_lower(sum((x - y) ** 2 for x, y in zip(b, b2)))
    E = [[D2[i][j] - D[i][j] for j in range(m)] for i in range(m)]
    nE = sqrt_lower(sum(E[i][j] ** 2 for i in range(m) for j in range(m)) / m)   # Frobenius/sqrt(m) <= operator norm
    rhs = abs(a2 - a) + coef / lam * ndb * (nb + nb2) + Fr(2) / lam ** 2 * (nb * nb) * nE
    return abs(s2 - s1) <= rhs


def x6(rng):
    coef = Fr(1) if MUTANT == 'M5' else Fr(2)
    ok = True
    n = 0
    for m in (1, 2, 3):
        for _ in range(300):
            lam = Fr(rng.randint(1, 300), 100)
            D = neg_def(rng, m, lam)
            D2 = neg_def(rng, m, lam / 2)
            b = [Fr(rng.randint(-60, 60), 20) for _ in range(m)]
            b2 = [x + Fr(rng.randint(-30, 30), 40) for x in b]
            a = Fr(rng.randint(-60, 60), 20)
            a2 = a + Fr(rng.randint(-20, 20), 40)
            ok &= lemma_s_ok(a, b, D, a2, b2, D2, lam, coef)
            n += 1
    # extremal instance: m = 1, D = -lam, D' = -lam/2, a = a', b = 0, b' = delta: |s' - s| = 2 delta^2/lam
    lam, dl = Fr(3, 2), Fr(1, 3)
    ok &= lemma_s_ok(Fr(0), [Fr(0)], [[-lam]], Fr(0), [dl], [[-lam / 2]], lam, coef)
    # Step Q2 polynomial bounds, coefficientwise in Gamma >= 0
    c0 = Fr(5, 4) * Fr(21, 16)
    c1 = Fr(5, 4) * 12 + Fr(35, 8) * Fr(21, 16) + 2
    c2 = Fr(35, 8) * 12 + Fr(35, 4) + 18
    poly_ok = (c0, c1, c2) == (Fr(105, 64), Fr(2911, 128), Fr(317, 4)) and c0 <= 80 and c1 <= 160 and c2 <= 80
    sq = (Fr(25, 16), 2 * Fr(5, 4) * Fr(35, 8), Fr(35, 8) ** 2)       # (5/4 + 35G/8)^2
    poly_ok &= sq[0] <= 80 and sq[1] <= 160 and sq[2] <= 80
    return {'random_instances': n, 'coefficient': str(coef), 'Q2_C2_poly': [str(c0), str(c1), str(c2)],
            'Q2_C0_poly': [str(x) for x in sq], 'passed': bool(ok and poly_ok)}


# ----------------------------------------------------------------------------------------------- X7 pointwise
def x7(rng):
    ok = True
    for _ in range(5000):
        kap = Fr(rng.randint(1, 400), 100)
        D = Fr(rng.randint(-300, 300), 100) or Fr(1, 7)
        Y = Fr(rng.randint(-900, 900), 50)
        weld = (36 * kap * kap * D * D - Y * Y) if abs(Y) < 2 * kap * abs(D) else Fr(0)
        loss = Y * Y if abs(Y) < 2 * kap * abs(D) else 36 * kap * kap * D * D
        ok &= 0 <= loss <= 9 * Y * Y and loss == 36 * kap * kap * D * D - weld
        rej = (36 * kap * kap * D * D - Y * Y) if 2 * kap * abs(D) <= abs(Y) < 6 * kap * abs(D) else Fr(0)
        ok &= rej <= (9 * Y * Y if abs(D) <= abs(Y) / (2 * kap) else 0)
        phi = Y / (6 * kap * D)
        ok &= (abs(phi) < Fr(1, 3)) == (abs(Y) < 2 * kap * abs(D))
        tau = Fr(rng.randint(0, 200), 100)
        yr = Y + Fr(rng.randint(-100, 100), 100) * tau
        if abs(yr) < 6 * kap * abs(D) < abs(Y):
            ok &= 36 * kap * kap * D * D - yr * yr <= 12 * kap * abs(D) * tau
    return {'trials': 5000, 'passed': bool(ok)}


def main():
    global MUTANT
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', default=None)
    args = ap.parse_args()
    if args.mutant is not None and args.mutant not in ('M1', 'M2', 'M3', 'M4', 'M5'):
        sys.stderr.write('unknown mutant label\n')
        return 2
    MUTANT = args.mutant
    rng = random.Random(20261001)
    out = {'object': 'CL-ELDER-THIRD-ORDER-20261001-v1 controls', 'scientific_effect': 'NONE', 'mutant': MUTANT,
           'checks': {'X1_exponent_ledger': x1(), 'X2_ridge_identities': x2(), 'X3_margins': x3(),
                      'X4_decision_1d': x4(rng), 'X5_weighted_taylor': x5(rng), 'X6_lemma_S': x6(rng),
                      'X7_pointwise': x7(rng)}}
    out['passed'] = all(v['passed'] for v in out['checks'].values())
    sys.stdout.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
    return 0 if out['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
