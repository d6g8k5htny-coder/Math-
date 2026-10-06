#!/usr/bin/env python3
"""Exact controls (standard library only) for CL-QS-A3-3-WEIGHT-TRANSFER-20261004-v1.

Usage:  python3 -B -S a33_exact.py            -> JSON summary on stdout, exit 0 iff every check passes
        python3 -B -S a33_exact.py --mutant Mk -> runs with mutant Mk; must exit 1 (failure reported on stderr)
Unknown arguments exit 2. Output is byte-identical under -O (no check depends on an assert statement).

F_j(X) := |det X| 1{X has exactly j negative eigenvalues}  (X real symmetric; index = number of negative eigenvalues).
Controls:
  K1  Lemma BD (a) on 1,500 bordered paths X_t = [[P, tQ], [tQ^T, R]], t in [0, 1], and every j (7,200 checks):
      |F_j(X_1) - F_j(X_0)| <= 2 sup_t |det X_t - det X_0|, blocks (2,1), (1,2), (2,2), (3,1), (2,3); the sup is exact (det X_t is
      a polynomial in u = t^2 of degree <= min block size, interpolated exactly and verified at an extra point). The random
      paths never exceed ratio 1; the explicit instance P = R = I_2, Q = (14/9) I_2 has ratio 13225/6664 > 39/20.
  K2  Lemma BD (b) ([R] (R7)), scalar corner, on 1,800 bordered matrices and every j (7,200 checks): det X_t =
      rho det P - t^2 q^T adj(P) q exactly, and |F_j(X_1) - F_j(X_0)| <= |q^T adj(P) q|; an instance attains equality.
  K3  Index additivity on 1,600 block-diagonal matrices and every j (7,200 checks): F_j(diag(P, R)) = sum_i F_i(P) F_{j-i}(R).
  K4  Pin Hessians in the window chart (d = 3), exactly pinned quartic fields in the midpoint eigenframe, r = s^2:
      Hess Fw(p) is a Laurent polynomial in s; its s^0 part is diag(P_p, -lam2/k), its s^1 part is the mixed block
      [[0, Da(p)], [Da(p)^T, 0]], it has no negative powers, and the planar/stiff blocks are even and the mixed block odd in s.
  K5  A stronger form of Proposition W3 on a mild family (r rational): |W_r/r^4 - (lam2)_+^2 w| <= C0 r Nf (|lam2| + r Nf) Pi^2
      with C0 = 2 (a control of the form, not the proof's constant), Nf = 1 + max |free jets of order 3, 4| in place of N (a
      quartic field has no finite global C^5 norm), Pi = 1 + |lam~| + gamma^2 + |B| + Nf, over r in {1e-2, 1e-3, 1e-4} and
      lam2 in {1, 1/10, 1/100, 3r, r, 0, -r, -1/10}; on the grid's lam2 <= 0 cases both sides vanish. An explicit field with
      lam2 = -G^2 r^2/144 < 0 and W_r > 0 (G = 100) exercises the negative branch. Also checks (3.5)'s identity
      W_r/r^4 = k^2 F_3(Hess Fw(M)) F_2(Hess Fw(S)) exactly at r = s^2, for k = 1 and k = 3/2.
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


# ----------------------------------------------------------------------------------------------------------- linear algebra
def det(M):
    n = len(M)
    if n == 0:
        return Fr(1)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    s = Fr(0)
    for j in range(n):
        if M[0][j] == 0:
            continue
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        s += (-1) ** j * M[0][j] * det(minor)
    return s


def adj(M):
    n = len(M)
    if n == 1:
        return [[Fr(1)]]
    A = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j + 1:] for k_, row in enumerate(M) if k_ != i]
            A[j][i] = (-1) ** (i + j) * det(minor)
    return A


def charpoly(M):
    """Coefficients of det(x I + M) = sum_k c_k x^k (Faddeev-LeVerrier on -M)."""
    n = len(M)
    # det(xI - N) with N = -M
    N = [[-v for v in row] for row in M]
    coeffs = [Fr(0)] * (n + 1)
    coeffs[n] = Fr(1)
    Mk = [[Fr(int(i == j)) for j in range(n)] for i in range(n)]
    c_prev = Fr(1)
    AM = [[Fr(0)] * n for _ in range(n)]
    for k_ in range(1, n + 1):
        # AM = N @ Mk
        AM = [[sum(N[i][l] * Mk[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        tr = sum(AM[i][i] for i in range(n))
        c = -tr / k_
        coeffs[n - k_] = c
        Mk = [[AM[i][j] + (c if i == j else 0) for j in range(n)] for i in range(n)]
    return coeffs  # det(xI - N) = det(xI + M)


def n_negative(M):
    """Exact number of negative eigenvalues of a real symmetric matrix: positive roots of det(xI + M) (real-rooted),
    counted by Descartes' rule after removing the zero roots."""
    c = charpoly(M)
    while c and c[0] == 0:
        c = c[1:]
    seq = [v for v in reversed(c) if v != 0]
    return sum(1 for a, b in zip(seq, seq[1:]) if (a > 0) != (b > 0))


def Fj(M, j):
    d = det(M)
    if d == 0:
        return Fr(0)
    return abs(d) if n_negative(M) == j else Fr(0)


def block(P, Q, R, t=Fr(1)):
    n1, n2 = len(P), len(R)
    X = [[Fr(0)] * (n1 + n2) for _ in range(n1 + n2)]
    for i in range(n1):
        for j in range(n1):
            X[i][j] = P[i][j]
        for j in range(n2):
            X[i][n1 + j] = t * Q[i][j]
            X[n1 + j][i] = t * Q[i][j]
    for i in range(n2):
        for j in range(n2):
            X[n1 + i][n1 + j] = R[i][j]
    return X


def rsym(n, lo=-5, hi=5, den=1):
    A = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            A[i][j] = A[j][i] = Fr(random.randint(lo * den, hi * den), den)
    return A


def rmat(n, m, lo=-5, hi=5, den=1):
    return [[Fr(random.randint(lo * den, hi * den), den) for _ in range(m)] for _ in range(n)]


def interp_even(vals_t, deg_u):
    """Given values of an even polynomial in t at t = 0, 1, ..., deg_u, return its coefficients in u = t^2 (Lagrange)."""
    us = [Fr(t * t) for t in range(deg_u + 1)]
    ys = vals_t
    coeffs = [Fr(0)] * (deg_u + 1)
    for i, (ui, yi) in enumerate(zip(us, ys)):
        # basis polynomial prod_{j != i} (u - uj)/(ui - uj)
        basis = [Fr(1)]
        denom = Fr(1)
        for j, uj in enumerate(us):
            if j == i:
                continue
            basis = [Fr(0)] + basis
            for k_ in range(len(basis) - 1):
                basis[k_] -= uj * basis[k_ + 1]
            denom *= (ui - uj)
        for k_ in range(deg_u + 1):
            coeffs[k_] += yi * basis[k_] / denom
    return coeffs


def sup_abs_poly_01(c):
    """Exact sup over u in [0, 1] of |c_1 u + c_2 u^2| (c_0 = 0 assumed, degree <= 2)."""
    assert c[0] == 0 and len(c) <= 3
    c1 = c[1] if len(c) > 1 else Fr(0)
    c2 = c[2] if len(c) > 2 else Fr(0)
    cands = [Fr(0), Fr(1)]
    if c2 != 0:
        v = -c1 / (2 * c2)
        if 0 <= v <= 1:
            cands.append(v)
    return max(abs(c1 * u + c2 * u * u) for u in cands)


# ----------------------------------------------------------------------------------------------------------- K1-K3
def k1(n_cases=300):
    worst = Fr(0)
    above1 = False
    count = 0
    for (n1, n2) in ((2, 1), (1, 2), (2, 2), (3, 1), (2, 3)):
        for _ in range(n_cases):
            P, R, Q = rsym(n1), rsym(n2), rmat(n1, n2, -3, 3)
            deg = min(n1, n2)
            vals = [det(block(P, Q, R, Fr(t))) for t in range(deg + 1)]
            cu = interp_even(vals, deg)
            # check the interpolation reproduces an extra point exactly
            tt = Fr(7, 3)
            if sum(cu[k_] * tt ** (2 * k_) for k_ in range(deg + 1)) != det(block(P, Q, R, tt)):
                fail('K1 interpolation is not exact')
            delta = sup_abs_poly_01([Fr(0)] + cu[1:])
            X0, X1 = block(P, Q, R, Fr(0)), block(P, Q, R, Fr(1))
            const = Fr(1) if MUTANT == 'M1' else Fr(2)
            for j in range(n1 + n2 + 1):
                lhs = abs(Fj(X1, j) - Fj(X0, j))
                if lhs > const * delta:
                    fail('K1 BD(a) violated: blocks (%d,%d), j=%d, lhs=%s, delta=%s' % (n1, n2, j, lhs, delta))
                if delta > 0:
                    ratio = lhs / delta
                    worst = max(worst, ratio)
                    if ratio > 1:
                        above1 = True
                count += 1
    # an explicit instance where a constant below 2 fails: P = R = I_2, Q = (14/9) I_2. Along the path the eigenvalues are
    # 1 +- tq (each double), so the index jumps from 0 to 2 at tq = 1 while det touches 0; F_2 goes from 0 to (q^2 - 1)^2.
    q = Fr(14, 9)
    P, Q, R = [[Fr(1), Fr(0)], [Fr(0), Fr(1)]], [[q, Fr(0)], [Fr(0), q]], [[Fr(1), Fr(0)], [Fr(0), Fr(1)]]
    vals = [det(block(P, Q, R, Fr(t))) for t in range(3)]
    cu = interp_even(vals, 2)
    delta = sup_abs_poly_01([Fr(0)] + cu[1:])
    lhs = max(abs(Fj(block(P, Q, R, Fr(1)), j) - Fj(block(P, Q, R, Fr(0)), j)) for j in range(5))
    explicit = lhs / delta
    const = Fr(1) if MUTANT == 'M1' else Fr(2)
    if lhs > const * delta:
        fail('K1 BD(a) violated on the explicit instance (ratio %s)' % explicit)
    if explicit <= Fr(39, 20):
        fail('K1 the explicit instance does not show that the constant 2 is needed')
    return {'checks': count, 'max_ratio_random': str(worst), 'ratio_above_1_in_random': above1,
            'explicit_instance_ratio': str(explicit), 'explicit_instance_ratio_float': round(float(explicit), 6)}


def k2(n_cases=600):
    count = 0
    attained = False
    for n1 in (1, 2, 3):
        for _ in range(n_cases):
            P = rsym(n1)
            q = [[Fr(random.randint(-4, 4))] for _ in range(n1)]
            rho = Fr(random.randint(-6, 6))
            R = [[rho]]
            c = sum(q[i][0] * sum(adj(P)[i][j] * q[j][0] for j in range(n1)) for i in range(n1))
            for t in (Fr(1), Fr(2), Fr(1, 3)):
                if det(block(P, q, R, t)) != rho * det(P) - t * t * c:
                    fail('K2 bordered identity fails')
            X0, X1 = block(P, q, R, Fr(0)), block(P, q, R, Fr(1))
            bound = abs(c) / 2 if MUTANT == 'M2' else abs(c)
            for j in range(n1 + 2):
                lhs = abs(Fj(X1, j) - Fj(X0, j))
                if lhs > bound:
                    fail('K2 BD(b) violated: n1=%d j=%d lhs=%s |c|=%s' % (n1, j, lhs, abs(c)))
                if c != 0 and lhs == abs(c):
                    attained = True
                count += 1
    # sharp instance: P = (1), q = (1), rho = 1: det X0 = 1, det X1 = 0
    P, q, R = [[Fr(1)]], [[Fr(1)]], [[Fr(1)]]
    lhs = abs(Fj(block(P, q, R, Fr(1)), 0) - Fj(block(P, q, R, Fr(0)), 0))
    bound = Fr(1, 2) if MUTANT == 'M2' else Fr(1)
    if lhs > bound:
        fail('K2 sharp instance violates the bound')
    if lhs != 1:
        fail('K2 sharp instance not attained')
    return {'checks': count, 'matrices': count // 4, 'equality_attained_in_random_cases': attained}


def k3(n_cases=400):
    count = 0
    for (n1, n2) in ((2, 1), (2, 2), (1, 2), (3, 1)):
        for _ in range(n_cases):
            P, R = rsym(n1), rsym(n2)
            X = block(P, [[Fr(0)] * n2 for _ in range(n1)], R)
            for j in range(n1 + n2 + 1):
                if MUTANT == 'M5':
                    rhs = Fj(P, min(j, n1)) * Fj(R, min(j, n2))
                else:
                    rhs = sum(Fj(P, i) * Fj(R, j - i) for i in range(0, n1 + 1) if 0 <= j - i <= n2)
                if Fj(X, j) != rhs:
                    fail('K3 index additivity fails: (%d,%d) j=%d' % (n1, n2, j))
                count += 1
    return {'checks': count}


# ----------------------------------------------------------------------------------------------------------- pinned fields
MULTI = [al for al in product(range(5), repeat=3) if sum(al) <= 4]


def afact(al):
    return factorial(al[0]) * factorial(al[1]) * factorial(al[2])


def pinned_field(r, k, b, lam1, lam2, free):
    """Exactly pinned quartic field on R^3 in the midpoint eigenframe (x axial, y1 soft, y2 hard):
    f = sum c_al z^al / al!,  f(M) = b, f(S) = b - k r^3, grad f = 0 at M = (-r/2,0,0), S = (r/2,0,0);
    D^2_y f(0) = diag(-lam1, -lam2)."""
    a = r / 2
    c = {al: Fr(0) for al in MULTI}
    for al, v in free.items():
        c[al] = v
    c[(0, 2, 0)] = -lam1
    c[(0, 0, 2)] = -lam2
    c[(0, 1, 1)] = Fr(0)
    c4 = c[(4, 0, 0)]
    c[(3, 0, 0)] = 12 * k
    c[(1, 0, 0)] = -6 * k * a * a
    c[(2, 0, 0)] = -c4 * a * a / 6
    c[(0, 0, 0)] = b - 4 * k * a ** 3 + c4 * a ** 4 / 24
    for t in (1, 2):
        e = [0, 0, 0]
        e[t] = 1
        d2 = c[(2, e[1], e[2])]
        d3 = c[(3, e[1], e[2])]
        c[(0, e[1], e[2])] = -d2 * a * a / 2
        c[(1, e[1], e[2])] = -d3 * a * a / 6
    return c


def rand_free():
    pinned = {(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 2, 0), (0, 0, 2),
              (0, 1, 1)}
    free = {}
    for al in MULTI:
        if al in pinned or sum(al) <= 2:
            continue
        s = 2 if sum(al) == 3 else 5
        free[al] = Fr(random.randint(-4 * s, 4 * s), 4)
    return free


def eval_derivs(c, pt):
    """value, gradient and Hessian of f at pt (exact)."""
    val = Fr(0)
    g = [Fr(0)] * 3
    H = [[Fr(0)] * 3 for _ in range(3)]
    for al, v in c.items():
        if v == 0:
            continue
        base = v / afact(al)

        def mono(be):
            m = Fr(1)
            for t in range(3):
                m *= pt[t] ** be[t]
            return m
        val += base * mono(al)
        for i in range(3):
            if al[i] == 0:
                continue
            be = list(al)
            co = be[i]
            be[i] -= 1
            g[i] += base * co * mono(be)
            for j in range(3):
                if be[j] == 0:
                    continue
                be2 = list(be)
                co2 = co * be2[j]
                be2[j] -= 1
                H[i][j] += base * co2 * mono(be2)
    return val, g, H


# Laurent polynomials in s (dict exponent -> Fraction)
def lp_add(a, b):
    out = dict(a)
    for e, v in b.items():
        out[e] = out.get(e, Fr(0)) + v
    return {e: v for e, v in out.items() if v != 0}


def lp_scale(a, c, shift=0):
    return {e + shift: v * c for e, v in a.items() if v * c != 0}


def window_hessian_lp(free, k, b, lam1_tilde, lam2, pin):
    """Hess of Fw(X, zeta, eta) = (f(s^2 X, s^2 k zeta, s^3 eta) - b)/(k s^6) at (pin, 0, 0) as Laurent polynomials in s,
    for the exactly pinned field with r = s^2 (lam1 = r lam1_tilde / k). Exact symbolic computation: the pinned
    coefficients are polynomials in r = s^2."""
    # coefficients as polynomials in s: build them symbolically by evaluating the pinning formulas on polynomials
    # pinned: c100 = -6k a^2, c200 = -c4 a^2/6, c000 = b - 4k a^3 + c4 a^4/24, c0e = -d2 a^2/2, c1e = -d3 a^2/6, c020 = -lam1
    # with a = r/2 = s^2/2.
    a2 = {4: Fr(1, 4)}            # a^2 = s^4/4
    a3 = {6: Fr(1, 8)}
    a4 = {8: Fr(1, 16)}
    C = {}
    for al in MULTI:
        C[al] = {0: free[al]} if al in free and free[al] != 0 else {}
    c4 = free.get((4, 0, 0), Fr(0))
    C[(0, 2, 0)] = {2: -lam1_tilde / k}          # -lam1 = -r lam1_tilde/k = -(s^2) lam1_tilde/k
    C[(0, 0, 2)] = {0: -lam2} if lam2 != 0 else {}
    C[(0, 1, 1)] = {}
    C[(3, 0, 0)] = {0: 12 * k}
    C[(1, 0, 0)] = lp_scale(a2, -6 * k)
    C[(2, 0, 0)] = lp_scale(a2, -c4 / 6)
    C[(0, 0, 0)] = lp_add(lp_add({0: b}, lp_scale(a3, -4 * k)), lp_scale(a4, c4 / 24))
    for t in (1, 2):
        e = [0, 0, 0]
        e[t] = 1
        d2 = free.get((2, e[1], e[2]), Fr(0))
        d3 = free.get((3, e[1], e[2]), Fr(0))
        C[(0, e[1], e[2])] = lp_scale(a2, -d2 / 2)
        C[(1, e[1], e[2])] = lp_scale(a2, -d3 / 6)
    # composed monomial: c_al/al! * (s^2 X)^i (s^2 k zeta)^j (s^3 eta)^l / (k s^6)
    # Hessian w.r.t. (X, zeta, eta) at (X0, 0, 0): only monomials with j + l <= 2 contribute.
    X0 = pin
    H = [[{} for _ in range(3)] for _ in range(3)]
    for al, poly in C.items():
        if not poly:
            continue
        i, j, l = al
        if j + l > 2:
            continue
        coef = Fr(1, afact(al)) * Fr(k) ** j / k
        expo = 2 * i + 2 * j + 3 * l - 6
        # derivative of X^i zeta^j eta^l at (X0, 0, 0)
        for (p, q) in ((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)):
            # variables: 0 = X, 1 = zeta, 2 = eta
            orders = [0, 0, 0]
            orders[p] += 1
            orders[q] += 1
            if orders[1] != j or orders[2] != l:
                continue
            # d^{orders[0]}/dX^{orders[0]} X^i at X0, times j! l! from zeta^j eta^l
            o = orders[0]
            if o > i:
                continue
            dx = Fr(factorial(i), factorial(i - o)) * Fr(X0) ** (i - o)
            val = coef * dx * factorial(j) * factorial(l)
            H[p][q] = lp_add(H[p][q], lp_scale(poly, val, expo))
            if p != q:
                H[q][p] = lp_add(H[q][p], lp_scale(poly, val, expo))
    return H


def k4(n_fields=40):
    checked = 0
    for _ in range(n_fields):
        k = random.choice([Fr(1, 2), Fr(1), Fr(2), Fr(3, 2)])
        lt = Fr(random.randint(-8, 16), 4)
        lam2 = Fr(random.randint(-8, 16), 4)
        b = Fr(random.randint(-6, 6), 2)
        free = rand_free()
        gam, B = free[(2, 1, 0)], free[(1, 2, 0)]
        gam2, beta2, nu2 = free[(2, 0, 1)], free[(1, 1, 1)], free[(0, 2, 1)]
        for pin in (Fr(-1, 2), Fr(1, 2)):
            H = window_hessian_lp(free, k, b, lt, lam2, pin)
            Pm = [[Fr(12) * pin, gam * pin], [gam * pin, -lt + k * B * pin]]   # 12X, gamma X, -lam~ + k B X at X = pin
            model = [[Pm[0][0], Pm[0][1], Fr(0)], [Pm[1][0], Pm[1][1], Fr(0)], [Fr(0), Fr(0), -lam2 / k]]
            # Da at pin: a(X,z) = (gam2/(2k))(X^2 - 1/4) + beta2 X z + (k/2) nu2 z^2
            Da = [gam2 / k * pin, beta2 * pin]
            if MUTANT == 'M3':
                Da = [2 * Da[0], 2 * Da[1]]
            for p in range(3):
                for q in range(3):
                    poly = H[p][q]
                    if any(e < 0 for e in poly):
                        fail('K4 negative power of s in the pin Hessian')
                    if poly.get(0, Fr(0)) != model[p][q]:
                        fail('K4 s^0 part is not the model at entry (%d,%d)' % (p, q))
                    exp1 = Fr(0)
                    if (p, q) in ((0, 2), (2, 0)):
                        exp1 = Da[0]
                    if (p, q) in ((1, 2), (2, 1)):
                        exp1 = Da[1]
                    if poly.get(1, Fr(0)) != exp1:
                        fail('K4 s^1 part is not the mixed block at entry (%d,%d)' % (p, q))
                    odd_entry = (p == 2) != (q == 2)
                    for e in poly:
                        if (e % 2 == 1) != odd_entry:
                            fail('K4 parity in s fails at entry (%d,%d)' % (p, q))
            checked += 1
    return {'pins_checked': checked}


def k5(n_fields=24):
    rs = [Fr(1, 100), Fr(1, 1000), Fr(1, 10000)]
    C0 = Fr(2)
    worst = Fr(0)
    count = 0
    zero_cases = 0
    for _ in range(n_fields):
        k = random.choice([Fr(1, 2), Fr(1), Fr(2)])
        lt = random.choice([Fr(1, 2), Fr(1), Fr(2), Fr(5)])
        b = Fr(random.randint(-4, 4), 2)
        free = rand_free()
        Nf = 1 + max(abs(v) for al, v in free.items() if sum(al) >= 3)
        gam, B = free[(2, 1, 0)], free[(1, 2, 0)]
        Y = 3 * k * B - gam * gam / 4
        Pi = 1 + abs(lt) + gam * gam + abs(B) + Nf
        for r in rs:
            for lam2 in (Fr(1), Fr(1, 10), Fr(1, 100), 3 * r, r, Fr(0), -r, Fr(-1, 10)):
                lam1 = r * lt / k
                c = pinned_field(r, k, b, lam1, lam2, free)
                M = (-r / 2, Fr(0), Fr(0))
                S = (r / 2, Fr(0), Fr(0))
                vM, gM, HM = eval_derivs(c, M)
                vS, gS, HS = eval_derivs(c, S)
                if vM != b or vS != b - k * r ** 3 or any(gM) or any(gS):
                    fail('K5 pins are not exact')
                W = Fj(HM, 3) * Fj(HS, 2)
                Wr4 = W / r ** 4
                w = max(6 * lt + Y, Fr(0)) * max(6 * lt - Y, Fr(0))
                if MUTANT == 'M4':
                    w = max(6 * lt + Y, Fr(0)) ** 2
                lp = max(lam2, Fr(0))
                model = lp * lp * w
                eps = r * Nf * (abs(lam2) + r * Nf) * Pi ** 2
                ratio = abs(Wr4 - model) / eps
                if ratio > C0:
                    fail('K5 W3 bound violated: r=%s lam2=%s ratio=%s' % (r, lam2, ratio))
                worst = max(worst, ratio)
                if lam2 <= 0:
                    zero_cases += 1
                count += 1
    # an explicit negative-branch instance: lam2 = -G^2 r^2/144 < 0, both pins typed (W_r > 0)
    G, k, r, b, lt = Fr(100), Fr(1), Fr(1, 10000), Fr(0), Fr(1)
    lam2 = -G * G * r * r / 144
    free = {al: Fr(0) for al in MULTI if sum(al) >= 3 and al not in {(3, 0, 0), (1, 0, 1), (1, 1, 0), (0, 1, 1)}}
    free[(2, 0, 1)] = G
    free[(3, 0, 1)] = G
    free[(1, 0, 2)] = G * G / 12
    c = pinned_field(r, k, b, r * lt / k, lam2, free)
    vM, gM, HM = eval_derivs(c, (-r / 2, Fr(0), Fr(0)))
    vS, gS, HS = eval_derivs(c, (r / 2, Fr(0), Fr(0)))
    if vM != b or vS != b - k * r ** 3 or any(gM) or any(gS):
        fail('K5 pins are not exact (negative branch)')
    Wneg = Fj(HM, 3) * Fj(HS, 2) / r ** 4
    if not (lam2 < 0 and Wneg > 0):
        fail('K5 the negative-branch instance is not typed')
    Nf = 1 + max(abs(v) for al, v in free.items() if sum(al) >= 3)
    Pi = 1 + abs(lt) + Nf
    if Wneg > C0 * r * Nf * (abs(lam2) + r * Nf) * Pi ** 2:
        fail('K5 W3 bound violated on the negative-branch instance')
    # (3.5) at r = s^2: W_r/r^4 = k^2 F_3(Hess Fw(M)) F_2(Hess Fw(S)), exactly, at k = 1 and k = 3/2
    s = Fr(1, 10)
    r = s * s
    for k in (Fr(1), Fr(3, 2)):
        lt, lam2, b = Fr(2), Fr(1, 3), Fr(0)
        free = rand_free()
        c = pinned_field(r, k, b, r * lt / k, lam2, free)
        _, _, HM = eval_derivs(c, (-r / 2, Fr(0), Fr(0)))
        _, _, HS = eval_derivs(c, (r / 2, Fr(0), Fr(0)))
        lhs = Fj(HM, 3) * Fj(HS, 2) / r ** 4

        def window(pin):
            H = window_hessian_lp(free, k, b, lt, lam2, pin)
            return [[sum(v * s ** e for e, v in H[p][q].items()) for q in range(3)] for p in range(3)]
        rhs = k * k * Fj(window(Fr(-1, 2)), 3) * Fj(window(Fr(1, 2)), 2)
        if lhs != rhs or lhs == 0:
            fail('K5 identity (3.5) fails at k = %s' % k)
    return {'cases': count, 'max_ratio': str(worst.limit_denominator(10 ** 6)), 'C0': str(C0), 'grid_cases_lam2_le_0': zero_cases,
            'negative_branch_W_over_r4': str(Wneg.limit_denominator(10 ** 15)), 'identity_3_5': 'exact at k = 1, 3/2'}


def main():
    global MUTANT
    args = sys.argv[1:]
    if args:
        if len(args) == 2 and args[0] == '--mutant' and args[1] in ('M1', 'M2', 'M3', 'M4', 'M5'):
            MUTANT = args[1]
        else:
            sys.stderr.write('usage: a33_exact.py [--mutant M1|M2|M3|M4|M5]\n')
            sys.exit(2)
    random.seed(20261004)
    res = {'object': 'CL-QS-A3-3-WEIGHT-TRANSFER-20261004-v1', 'scientific_effect': 'NONE'}
    res['K1'] = k1()
    res['K2'] = k2()
    res['K3'] = k3()
    res['K4'] = k4()
    res['K5'] = k5()
    res['all_pass'] = True
    sys.stdout.write(json.dumps(res, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
