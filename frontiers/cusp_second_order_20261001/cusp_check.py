#!/usr/bin/env python3
"""Exact finite controls for PROOF.md (CL-CUSP-SECOND-ORDER-20261001-v1.1).  Standard library only; exact rationals.

  C1  the quartic ridge of Theorem CU.2: g(X) = kappa[2(X+1/2)^2(X-1) + 3 phi (X^2-1/4)^2] has
      g'(X) = 6 kappa (X^2-1/4)(1+2 phi X), g(-1/2) = 0, g(1/2) = -kappa, g''(-1/2) = 6 kappa (phi-1),
      g''(1/2) = 6 kappa (phi+1); at X3 = -1/(2 phi):  g(X3) + kappa = kappa (phi+1)^3 (3 phi-1)/(16 phi^3) and
      g(X3) = kappa (phi-1)^3 (3 phi+1)/(16 phi^3); at phi = 1/3, g - g(1/2) = (kappa/16)(2X-1)^2(2X+3)^2 and at
      phi = -1/3, g = -(kappa/16)(2X-3)^2(2X+1)^2 -- all as exact polynomial identities at rational kappa, phi;
  C2  the elder window: for the 117 rational phi = n/60, |n| <= 59, n != +-20 (the two boundaries phi = +-1/3 excluded),
      the maximin connection level of M = -1/2 for g, computed by an exact one-dimensional union-find on a rational
      grid that contains every critical point (so it is the exact maximin, not an approximation), equals g(1/2) =
      -kappa iff |phi| < 1/3; typed (g''(-1/2) < 0 < g''(1/2)) iff |phi| < 1; mutant M1 asserts the threshold 1/2;
  C3  the fiber reduction: P(X,Y) = g(X) + (1/2)(Y - Y*)^T A (Y - Y*) with Y* = -(1/2)(X^2-1/4) A^{-1} gamma and
      e4 = f4 - 3 gamma^T A^{-1} gamma, exactly at rational points for m = 1, 2 (A negative definite rational);
      mutant M4 uses the coefficient 2 in place of 3;
  C4  the cusp limit field (Theorem CU.1): for pinned polynomials of degree <= 6 in d = 2 and d = 3 (the
      2(d+1) pinned coefficients solved exactly as polynomials in r from f(M) = b, f(S) = b - kappa r^4,
      grad f(M) = grad f(S) = 0), r^-4 [f(r X, r^2 Y) - b] is a polynomial in r whose constant term is exactly
      P(X,Y) = 2 kappa (X+1/2)^2(X-1) + (f4/24)(X^2-1/4)^2 + (1/2)(X^2-1/4) gamma.Y + (1/2) Y^T A Y, with (f4, gamma, A)
      the polynomial's jets at 0; mutant M3 drops the gamma.Y term;
  C5  the endpoint determinants of the model: det Hess P(M) = Y - 6 kappa Delta, det Hess P(S) = Y + 6 kappa Delta,
      Y = (f4/12) Delta - gamma^T adj(A) gamma/4, and the inertia of Hess P at M and S (exact congruence) is
      (d negative) and (d-1 negative) iff |phi| < 1 with phi = Y/(6 kappa Delta), m = 1, 2;
  C6  the cusp integrals: int_0^oo loss_eld ds = (16/7) Y^2 s1, s1 = (2|Delta|/|Y|)^(1/4), equal to
      (16/7) 2^(1/4) |Y|^(7/4) |Delta|^(1/4) (checked through the exact fourth-power identity), and the candidate
      analogue (8/7) 6^(1/4) |Y|^(7/4) |Delta|^(1/4), at rational points where the fourth roots are rational;
      mutant M2 uses 8/7 for the elder constant;
  C7  the Gaussian-kernel conditional covariances used by the exploration (exact Schur complements): d = 2:
      (f_yy, f_xxxx) | (f_xx, f_xy) has covariance [[8/3, 2], [2, 30]], f_xxy | (f_x, f_y, f_xxx) variance 2,
      Var(f_xxx | grad f) = 6, D_1 = 4/3; d = 3: (f_yy, f_zz, f_yz) | (f_xx, f_xy, f_xz) has covariance
      [[8/3, 2/3, 0], [2/3, 8/3, 0], [0, 0, 1]], f_xxxx | (f_yy, f_zz, f_yz, f_xx, f_xy, f_xz) has regression
      coefficient 3/5 on each of f_yy, f_zz and residual variance 138/5, and (f_xxy, f_xxz) | (grad f, f_xxx) has
      covariance 2 I;
  C8  the gap enters affinely (Lemma L) and the constants of Theorem CU': for the pinned polynomials of C4 in d = 2, 3,
      the family is affine in the gap with the k-shift omega = 2(x - r)(x + r/2)^2 exactly (transverse coefficients
      gap-free), d det K_M/dk = -6 det A_M and d det K_S/dk = +6 det A_S exactly, det K_M + det K_S = 2rY + O(r^2) and
      det K_S - det K_M = 12k det A(0) + O(r^2) (the common rY of the sign window); I_cand/c_1 = 3^(1/4)/2 (fourth power
      3/16); the rejected cusp integral int_{s1}^{3^(1/4)s1} (36 Delta^2 s^-8 - Y^2) ds = (16/7)Y^2 s1 - (8/7)Y^2 3^(1/4)s1
      exactly in Q(3^(1/4)); the small-kappa elder share 13/27; mutant M5 flips the sign of d det K_M/dk.
  M   mutants (--mutant M1|M2|M3|M4|M5) exit 1; an unknown label exits 2.
  Scope: C1-C8 check exact identities and finitely many rational instances.  They do NOT test Theorem CU.1 for
  non-polynomial fields, Proposition CU.3 (stability), Theorem CU.4 (Gaussian kernel limits), Lemma CU.5 (window
  probability), Lemma L for random fields, or the assemblies of Theorems CU and CU'; those are proved in prose only.
  The controls are not acceptance.
"""
import argparse
import itertools
import json
import sys
from fractions import Fraction as F

HALF = F(1, 2)
QUARTER = F(1, 4)


# ------------------------------------------------------------------------------------------ small exact helpers

def det(M):
    n = len(M)
    A = [row[:] for row in M]
    d = F(1)
    for i in range(n):
        p = next((r for r in range(i, n) if A[r][i] != 0), None)
        if p is None:
            return F(0)
        if p != i:
            A[i], A[p] = A[p], A[i]
            d = -d
        d *= A[i][i]
        for r in range(i + 1, n):
            fct = A[r][i] / A[i][i]
            for c in range(i, n):
                A[r][c] -= fct * A[i][c]
    return d


def inverse(M):
    n = len(M)
    A = [M[i][:] + [F(int(i == j)) for j in range(n)] for i in range(n)]
    for i in range(n):
        p = next(r for r in range(i, n) if A[r][i] != 0)
        A[i], A[p] = A[p], A[i]
        piv = A[i][i]
        A[i] = [x / piv for x in A[i]]
        for r in range(n):
            if r != i and A[r][i] != 0:
                fct = A[r][i]
                A[r] = [x - fct * y for x, y in zip(A[r], A[i])]
    return [row[n:] for row in A]


def adj(M):
    n = len(M)
    if n == 1:
        return [[F(1)]]
    dM = det(M)
    if dM != 0:
        inv = inverse(M)
        return [[dM * inv[i][j] for j in range(n)] for i in range(n)]
    out = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [[M[a][b] for b in range(n) if b != i] for a in range(n) if a != j]
            out[i][j] = (-1) ** (i + j) * det(minor)
    return out


def quad(v, M, w):
    return sum(v[i] * M[i][j] * w[j] for i in range(len(v)) for j in range(len(w)))


def inertia(M):
    """(negative, zero, positive) counts by exact symmetric congruence diagonalisation."""
    n = len(M)
    A = [row[:] for row in M]
    neg = zero = pos = 0
    idx = list(range(n))
    while idx:
        piv = next((i for i in idx if A[i][i] != 0), None)
        if piv is None:
            pair = next(((i, j) for i in idx for j in idx if i < j and A[i][j] != 0), None)
            if pair is None:
                zero += len(idx)
                break
            i, j = pair
            for c in range(n):
                A[i][c] += A[j][c]
            for rr in range(n):
                A[rr][i] += A[rr][j]
            piv = i
        p = A[piv][piv]
        if p < 0:
            neg += 1
        else:
            pos += 1
        rest = [i for i in idx if i != piv]
        for i in rest:
            fct = A[i][piv] / p
            for c in range(n):
                A[i][c] -= fct * A[piv][c]
        for i in rest:
            A[i][piv] = A[piv][i] = F(0)
        idx = rest
    return neg, zero, pos


def iroot(nn, k):
    if nn < 0:
        return None
    lo, hi = 0, 1
    while hi ** k <= nn:
        hi *= 2
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** k < nn:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo ** k == nn else None


def rational_root(x, k):
    a, b = iroot(x.numerator, k), iroot(x.denominator, k)
    return None if a is None or b is None else F(a, b)


# ------------------------------------------------------------------------------ polynomials in one variable

def padd(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else F(0)) + (q[i] if i < len(q) else F(0)) for i in range(n)]


def pmul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                out[i + j] += a * b
    return out


def pscale(p, c):
    return [c * a for a in p]


def peval(p, x):
    out = F(0)
    for a in reversed(p):
        out = out * x + a
    return out


def pderiv(p):
    return [i * p[i] for i in range(1, len(p))] or [F(0)]


def ppow(p, k):
    out = [F(1)]
    for _ in range(k):
        out = pmul(out, p)
    return out


def ptrim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


# ------------------------------------------------------------------------------------------------ the model

def ridge_poly(kappa, phi):
    """g(X)/1 as coefficients in X: kappa [2 (X+1/2)^2 (X-1) + 3 phi (X^2-1/4)^2]."""
    a = pmul(ppow([HALF, F(1)], 2), [F(-1), F(1)])
    b = ppow([-QUARTER, F(0), F(1)], 2)
    return ptrim(pscale(padd(pscale(a, F(2)), pscale(b, 3 * phi)), kappa))


def check_C1(mutant):
    pts = 0
    for kappa in (F(1), F(3, 7), F(5, 2)):
        for phi in (F(1, 5), F(-2, 7), F(3, 4), F(-9, 10), F(1, 3), F(-1, 3), F(1, 11)):
            g = ridge_poly(kappa, phi)
            gp = pderiv(g)
            target = pscale(pmul([-QUARTER, F(0), F(1)], [F(1), 2 * phi]), 6 * kappa)
            if ptrim(gp) != ptrim(target):
                return False, "g' != 6 kappa (X^2-1/4)(1+2 phi X)"
            if peval(g, -HALF) != 0 or peval(g, HALF) != -kappa:
                return False, 'pinned heights'
            gpp = pderiv(gp)
            if peval(gpp, -HALF) != 6 * kappa * (phi - 1) or peval(gpp, HALF) != 6 * kappa * (phi + 1):
                return False, 'endpoint curvatures'
            X3 = -1 / (2 * phi)
            if peval(gp, X3) != 0:
                return False, 'third critical point'
            if peval(g, X3) + kappa != kappa * (phi + 1) ** 3 * (3 * phi - 1) / (16 * phi ** 3):
                return False, 'factorisation (phi+1)^3 (3 phi - 1)'
            if peval(g, X3) != kappa * (phi - 1) ** 3 * (3 * phi + 1) / (16 * phi ** 3):
                return False, 'factorisation (phi-1)^3 (3 phi + 1)'
            pts += 1
        # boundary configurations: double roots
        gp3 = ridge_poly(kappa, F(1, 3))
        gm3 = ridge_poly(kappa, F(-1, 3))
        dbl_p = pscale(pmul(ppow([F(-1), F(2)], 2), ppow([F(3), F(2)], 2)), kappa / 16)
        dbl_m = pscale(pmul(ppow([F(-3), F(2)], 2), ppow([F(1), F(2)], 2)), -kappa / 16)
        if ptrim(padd(gp3, [kappa])) != ptrim(dbl_p) or ptrim(gm3) != ptrim(dbl_m):
            return False, 'boundary double-root identities'
    return True, {'parameter_points': pts, 'boundary_identities': 6}


def maximin_1d(xs, vals, iM):
    """Exact 1D union-find maximin: death level of the component born at index iM (the level at which it first
    merges with a component whose maximum exceeds vals[iM]); -inf if it never does."""
    n = len(xs)
    order = sorted(range(n), key=lambda i: -vals[i])
    parent = [-1] * n
    top = [None] * n

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for p in order:
        parent[p] = p
        top[p] = vals[p]
        for q in (p - 1, p + 1):
            if 0 <= q < n and parent[q] >= 0:
                a, b = find(p), find(q)
                if a != b:
                    if top[a] < top[b]:
                        a, b = b, a
                    if parent[iM] >= 0 and find(iM) == b and top[a] > vals[iM]:
                        return vals[p]
                    parent[b] = a
    return None


def check_C2(mutant):
    thr = HALF if mutant == 'M1' else F(1, 3)
    kappa = F(1)
    R = F(40)
    base = [F(n, 8) for n in range(-320, 321)]            # step 1/8 on [-40, 40]
    n_elder = n_rej = 0
    for n in range(-59, 60):
        phi = F(n, 60)
        if abs(phi) == F(1, 3):
            continue
        g = ridge_poly(kappa, phi)
        pts = set(base) | {-HALF, HALF}
        if phi != 0:
            X3 = -1 / (2 * phi)
            if abs(X3) < R:
                pts.add(X3)
        xs = sorted(pts)
        vals = [peval(g, x) for x in xs]
        iM = xs.index(-HALF)
        dl = maximin_1d(xs, vals, iM)
        elder = (dl is not None and dl == -kappa)
        if elder != (abs(phi) < thr):
            return False, 'elder window fails at phi = %s (death level %s)' % (phi, dl)
        gpp = pderiv(pderiv(g))
        typed = peval(gpp, -HALF) < 0 < peval(gpp, HALF)
        if not typed:
            return False, 'typed fails inside |phi| < 1 at phi = %s' % phi
        n_elder += elder
        n_rej += (not elder)
    for phi in (F(11, 10), F(-11, 10), F(1), F(-1)):
        gpp = pderiv(pderiv(ridge_poly(kappa, phi)))
        if peval(gpp, -HALF) < 0 < peval(gpp, HALF):
            return False, 'typed holds outside |phi| < 1'
    return True, {'phi_values': n_elder + n_rej, 'elder': n_elder, 'rejected': n_rej, 'grid': '1/8 on [-40,40] plus critical points'}


def model_P(kappa, f4, gamma, A, X, Y, drop_gamma=False):
    m = len(A)
    val = 2 * kappa * (X + HALF) ** 2 * (X - 1) + (f4 / 24) * (X * X - QUARTER) ** 2
    if not drop_gamma:
        val += HALF * (X * X - QUARTER) * sum(gamma[j] * Y[j] for j in range(m))
    val += HALF * quad(Y, A, Y)
    return val


def neg_def(m, seed):
    """A rational negative definite m x m matrix: -(B B^T + I/2)."""
    vals = [F(1, 3), F(-2, 5), F(3, 7), F(1, 2), F(-1, 4), F(2, 9)]
    B = [[vals[(seed + i * m + j) % len(vals)] for j in range(m)] for i in range(m)]
    return [[-(sum(B[i][k] * B[j][k] for k in range(m)) + (HALF if i == j else 0)) for j in range(m)] for i in range(m)]


def check_C3(mutant):
    coef = 2 if mutant == 'M4' else 3
    pts = 0
    for m in (1, 2):
        for seed in range(3):
            A = neg_def(m, seed)
            Ainv = inverse(A)
            gamma = [F(2, 3), F(-5, 4)][:m]
            for kappa, f4 in ((F(1), F(7, 3)), (F(2, 5), F(-11, 2))):
                e4 = f4 - coef * quad(gamma, Ainv, gamma)
                for X in (F(-2), F(-1, 2), F(1, 3), F(5, 4)):
                    Ys = [(X * X - QUARTER) * (-HALF) * sum(Ainv[j][k] * gamma[k] for k in range(m)) for j in range(m)]
                    gX = 2 * kappa * (X + HALF) ** 2 * (X - 1) + (e4 / 24) * (X * X - QUARTER) ** 2
                    for Y in ([F(1, 2), F(-3, 2)][:m], [F(0), F(2)][:m], [F(-7, 5), F(1, 9)][:m]):
                        Z = [Y[j] - Ys[j] for j in range(m)]
                        if model_P(kappa, f4, gamma, A, X, Y) != gX + HALF * quad(Z, A, Z):
                            return False, 'fiber identity fails (m = %d)' % m
                        pts += 1
    return True, {'points': pts}


# ------------------------------------------------------------ C4: pinned polynomials and the cusp limit field

def monomials(m, deg):
    out = []
    for total in range(deg + 1):
        for i in range(total + 1):
            for js in itertools.product(range(total - i + 1), repeat=m):
                if sum(js) == total - i:
                    out.append((i, js))
    return out


def pinned_poly_in_r(m, kappa, b, free):
    """Coefficients c[(i, js)] as polynomials in r (lists), with the 2(d+1) pinned ones solved exactly.
    M = (-r/2, 0), S = (r/2, 0); f(M) = b, f(S) = b - kappa r^4, grad f(M) = grad f(S) = 0.  h = r/2."""
    zero_js = tuple([0] * m)
    c = {key: [val] for key, val in free.items()}
    hpow = lambda k: [F(0)] * k + [F(1, 2 ** k)]            # h^k = r^k / 2^k as a polynomial in r
    ax = lambda i: c.get((i, zero_js), [F(0)])
    # transverse gradient pins: psi_j(x) = sum_i c[(i, e_j)] x^i vanishes at x = +-h
    for j in range(m):
        ej = tuple(1 if t == j else 0 for t in range(m))
        c0 = [F(0)]
        c1 = [F(0)]
        for i in range(2, 7):
            ci = c.get((i, ej), [F(0)])
            if i % 2 == 0:
                c0 = padd(c0, pscale(pmul(ci, hpow(i)), F(-1)))
            else:
                c1 = padd(c1, pscale(pmul(ci, hpow(i - 1)), F(-1)))
        c[(0, ej)] = c0
        c[(1, ej)] = c1
    # axial pins
    c2 = [F(0)]
    for i in range(4, 7):
        if i % 2 == 0:
            c2 = padd(c2, pscale(pmul(ax(i), hpow(i - 2)), F(-i, 2)))
    c3 = pscale(hpow(1), 4 * kappa)                           # 4 kappa h
    for i in range(5, 7, 2):
        c3 = padd(c3, pscale(pmul(ax(i), hpow(i - 3)), F(1 - i, 2)))
    c1 = pscale(hpow(3), -8 * kappa)
    for i in range(5, 7, 2):
        c1 = padd(c1, pscale(pmul(ax(i), hpow(i - 1)), F(-1)))
    c1 = padd(c1, pscale(pmul(c3, hpow(2)), F(-1)))
    c0 = padd([b], pscale(hpow(4), -8 * kappa))               # b - kappa r^4 / 2 = b - 8 kappa h^4
    c0 = padd(c0, pscale(pmul(c2, hpow(2)), F(-1)))
    for i in range(4, 7, 2):
        c0 = padd(c0, pscale(pmul(ax(i), hpow(i)), F(-1)))
    c[(0, zero_js)] = c0
    c[(1, zero_js)] = c1
    c[(2, zero_js)] = c2
    c[(3, zero_js)] = c3
    return c


def eval_poly_in_r(c, m, x_poly, y_polys):
    total = [F(0)]
    for (i, js), coef in c.items():
        term = pmul(coef, ppow(x_poly, i))
        for j in range(m):
            term = pmul(term, ppow(y_polys[j], js[j]))
        total = padd(total, term)
    return total


def check_C4(mutant):
    checked = 0
    vals = [F(1, 3), F(-2, 5), F(3, 7), F(-1, 2), F(5, 4), F(-3, 8), F(2, 9), F(-7, 6), F(1, 5), F(4, 11)]
    for m in (1, 2):
        mons = monomials(m, 6)
        zero_js = tuple([0] * m)
        pinned = {(0, zero_js), (1, zero_js), (2, zero_js), (3, zero_js)}
        for j in range(m):
            ej = tuple(1 if t == j else 0 for t in range(m))
            pinned |= {(0, ej), (1, ej)}
        for trial in range(2):
            free = {}
            for idx, key in enumerate(mons):
                if key in pinned:
                    continue
                free[key] = vals[(idx * 7 + trial * 3) % len(vals)]
            # make the transverse quadratic negative definite
            for j in range(m):
                ejj = (0, tuple(2 if t == j else 0 for t in range(m)))
                free[ejj] = -abs(free.get(ejj, F(1))) - 1
            if m == 2:
                free[(0, (1, 1))] = F(1, 3)          # keep the transverse block negative definite
            kappa = [F(3, 5), F(7, 4)][trial]
            b = F(1, 7)
            c = pinned_poly_in_r(m, kappa, b, free)
            # jets at 0
            f4 = 24 * free[(4, zero_js)]
            gamma = []
            A = [[F(0)] * m for _ in range(m)]
            for j in range(m):
                ej = tuple(1 if t == j else 0 for t in range(m))
                gamma.append(2 * free.get((2, ej), F(0)))
                for k in range(m):
                    if j == k:
                        A[j][j] = 2 * free.get((0, tuple(2 if t == j else 0 for t in range(m))), F(0))
                    else:
                        A[j][k] = free.get((0, tuple(1 if t in (j, k) else 0 for t in range(m))), F(0))
            for X in (F(-1), F(1, 3), F(3, 2)):
                for Y in ([F(1, 2), F(-1)][:m], [F(-2, 3), F(1, 4)][:m]):
                    x_poly = [F(0), X]                              # r X
                    y_polys = [[F(0), F(0), Y[j]] for j in range(m)]   # r^2 Y_j
                    val = eval_poly_in_r(c, m, x_poly, y_polys)
                    val = padd(val, [-b])
                    val = val + [F(0)] * 6
                    if any(val[i] != 0 for i in range(4)):
                        return False, 'negative powers of r in r^-4 [f(rX, r^2 Y) - b] (m = %d)' % m
                    model = model_P(kappa, f4, gamma, A, X, Y, drop_gamma=(mutant == 'M3'))
                    if mutant != 'M3':
                        # the pinned -gamma.Y/8 and the other low-order terms are inside model_P already
                        pass
                    if val[4] != model:
                        return False, 'cusp limit field mismatch (m = %d): %s vs %s' % (m, val[4], model)
                    checked += 1
    return True, {'points': checked, 'dimensions': [2, 3], 'degree': 6}


# ------------------------------------------------------------------------------------ C5: model Hessians

def check_C5(mutant):
    cases = 0
    for m in (1, 2):
        for seed in range(3):
            A = neg_def(m, seed)
            Delta = det(A)
            adjA = adj(A)
            gamma = [F(3, 4), F(-1, 3)][:m]
            for kappa in (F(1, 2), F(2)):
                for f4 in (F(-40), F(-3), F(0), F(5), F(60)):
                    Y = (f4 / 12) * Delta - quad(gamma, adjA, gamma) / 4
                    n = m + 1
                    HM = [[F(0)] * n for _ in range(n)]
                    HS = [[F(0)] * n for _ in range(n)]
                    HM[0][0] = -6 * kappa + f4 / 12
                    HS[0][0] = 6 * kappa + f4 / 12
                    for j in range(m):
                        HM[0][j + 1] = HM[j + 1][0] = -gamma[j] / 2
                        HS[0][j + 1] = HS[j + 1][0] = gamma[j] / 2
                        for k in range(m):
                            HM[j + 1][k + 1] = HS[j + 1][k + 1] = A[j][k]
                    if det(HM) != Y - 6 * kappa * Delta or det(HS) != Y + 6 * kappa * Delta:
                        return False, 'endpoint determinants'
                    phi = Y / (6 * kappa * Delta)
                    typed = inertia(HM)[0] == m + 1 and inertia(HS)[0] == m and inertia(HS)[1] == 0
                    if typed != (abs(phi) < 1):
                        return False, 'typed window != |phi| < 1 at phi = %s' % phi
                    cases += 1
    return True, {'cases': cases}


# -------------------------------------------------------------------------------------- C6: cusp integrals

def check_C6(mutant):
    const_e = F(8, 7) if mutant == 'M2' else F(16, 7)
    pts = 0
    for Yv, Dv in ((F(1), F(8)), (F(1, 2), F(81, 32)), (F(2), F(1)), (F(3), F(3, 2))):
        s1 = rational_root(2 * Dv / Yv, 4)
        sc = rational_root(6 * Dv / Yv, 4)
        if s1 is not None:
            integral = Yv * Yv * s1 + F(36, 7) * Dv * Dv * s1 ** -7
            if integral != const_e * Yv * Yv * s1:
                return False, 'elder cusp integral'
            if (const_e * Yv * Yv * s1) ** 4 != const_e ** 4 * 2 * Yv ** 7 * Dv:
                return False, 'elder fourth-power identity'
            # the loss at a few s, and its continuity structure (jump at s1 from Y^2 to 9 Y^2)
            if 36 * Dv * Dv * s1 ** -8 != 9 * Yv * Yv:
                return False, 'jump at s1'
            pts += 1
        if sc is not None:
            integral = Yv * Yv * sc + F(36, 7) * Dv * Dv * sc ** -7
            if integral != F(8, 7) * Yv * Yv * sc or (F(8, 7) * Yv * Yv * sc) ** 4 != F(8, 7) ** 4 * 6 * Yv ** 7 * Dv:
                return False, 'candidate cusp integral'
            if 36 * Dv * Dv * sc ** -8 != Yv * Yv:
                return False, 'candidate loss continuity at s*'
            pts += 1
    if pts < 3:
        return False, 'too few exact points'
    # ratio of the elder and candidate constants: (16/7) 2^(1/4) / ((8/7) 6^(1/4)) = 2 * 3^(-1/4): check its 4th power
    if (F(16, 7) / F(8, 7)) ** 4 * F(2, 6) != F(16, 3):
        return False, 'ratio'
    return True, {'points': pts, 'elder_constant': '(16/7) 2^(1/4)', 'candidate_constant': '(8/7) 6^(1/4)'}


# ------------------------------------------------- C8: the gap enters affinely (Lemma L) and Theorem CU'

def free_coefficients(m, trial):
    """The free coefficients of check_C4 (degree 6, transverse quadratic negative definite)."""
    vals = [F(1, 3), F(-2, 5), F(3, 7), F(-1, 2), F(5, 4), F(-3, 8), F(2, 9), F(-7, 6), F(1, 5), F(4, 11)]
    zero_js = tuple([0] * m)
    pinned = {(0, zero_js), (1, zero_js), (2, zero_js), (3, zero_js)}
    for j in range(m):
        ej = tuple(1 if t == j else 0 for t in range(m))
        pinned |= {(0, ej), (1, ej)}
    free = {}
    for idx, key in enumerate(monomials(m, 6)):
        if key not in pinned:
            free[key] = vals[(idx * 7 + trial * 3) % len(vals)]
    for j in range(m):
        ejj = (0, tuple(2 if t == j else 0 for t in range(m)))
        free[ejj] = -abs(free.get(ejj, F(1))) - 1
    if m == 2:
        free[(0, (1, 1))] = F(1, 3)
    return free


def pdivr(p):
    """p / r for a polynomial p in r with zero constant term."""
    if p[0] != 0:
        raise ValueError('not divisible by r')
    return p[1:] or [F(0)]


def scaled_hessian_dets(c, m, sign):
    """det K at the pin x = sign r/2 as a polynomial in r, and det A there: K = [[alpha, sqrt(r) beta^T],
    [sqrt(r) beta, A]], alpha = f_xx/r, beta = grad_y f_x / r, A = D_y^2 f, det K = alpha det A - r beta^T adj(A) beta."""
    zero_js = tuple([0] * m)
    xp = [F(0), F(sign, 2)]
    fxx = [F(0)]
    for (i, js), coef in c.items():
        if js == zero_js and i >= 2:
            fxx = padd(fxx, pscale(pmul(coef, ppow(xp, i - 2)), F(i * (i - 1))))
    alpha = pdivr(ptrim(fxx + [F(0)]))
    beta, Am = [], [[[F(0)] for _ in range(m)] for _ in range(m)]
    for j in range(m):
        ej = tuple(1 if t == j else 0 for t in range(m))
        fxy = [F(0)]
        for (i, js), coef in c.items():
            if js == ej and i >= 1:
                fxy = padd(fxy, pscale(pmul(coef, ppow(xp, i - 1)), F(i)))
        beta.append(pdivr(ptrim(fxy + [F(0)])))
        for l in range(m):
            el = tuple((1 if t == j else 0) + (1 if t == l else 0) for t in range(m))
            mult = F(2) if j == l else F(1)
            ent = [F(0)]
            for (i, js), coef in c.items():
                if js == el:
                    ent = padd(ent, pscale(pmul(coef, ppow(xp, i)), mult))
            Am[j][l] = ent
    if m == 1:
        detA = Am[0][0]
        badjb = pmul(beta[0], beta[0])
    else:
        detA = padd(pmul(Am[0][0], Am[1][1]), pscale(pmul(Am[0][1], Am[1][0]), F(-1)))
        badjb = padd(padd(pmul(pmul(beta[0], beta[0]), Am[1][1]), pmul(pmul(beta[1], beta[1]), Am[0][0])),
                     pscale(pmul(pmul(beta[0], beta[1]), Am[0][1]), F(-2)))
    detK = padd(pmul(alpha, detA), pscale(pmul([F(0), F(1)], badjb), F(-1)))
    return ptrim(detK), ptrim(detA)


class Q4:
    """Exact arithmetic in Q(theta), theta^4 = 3 (theta = 3^(1/4)): a0 + a1 theta + a2 theta^2 + a3 theta^3."""
    def __init__(self, a):
        self.a = [F(x) for x in a] + [F(0)] * (4 - len(a))

    def __add__(self, o):
        return Q4([x + y for x, y in zip(self.a, o.a)])

    def __sub__(self, o):
        return Q4([x - y for x, y in zip(self.a, o.a)])

    def __mul__(self, o):
        out = [F(0)] * 7
        for i, x in enumerate(self.a):
            for j, y in enumerate(o.a):
                out[i + j] += x * y
        return Q4([out[k] + 3 * (out[k + 4] if k + 4 < 7 else 0) for k in range(4)])

    def __eq__(self, o):
        return self.a == o.a

    def power(self, n):
        out = Q4([1])
        base = self if n >= 0 else Q4([0, 0, 0, F(1, 3)]) if self.a == [0, 1, 0, 0] else None
        if base is None:
            raise ValueError('negative powers only of theta')
        for _ in range(abs(n)):
            out = out * base
        return out


def check_C8(mutant):
    sgn = 1 if mutant == 'M5' else -1
    cases = 0
    for m in (1, 2):
        for trial in range(2):
            free = free_coefficients(m, trial)
            zero_js = tuple([0] * m)
            kappa0, b = [F(3, 5), F(7, 4)][trial], F(1, 7)
            c0 = pinned_poly_in_r(m, kappa0, b, free)
            c1 = pinned_poly_in_r(m, kappa0 + 1, b, free)
            # (i) the pinned family is affine in kappa with kappa-part 2 kappa r (x - r)(x + r/2)^2, i.e. the k-shift
            #     omega = 2 (x - r)(x + r/2)^2 = 2x^3 - (3/2) r^2 x - r^3/2 per unit k = kappa r
            diff = {key: ptrim(padd(c1.get(key, [F(0)]), pscale(c0.get(key, [F(0)]), F(-1)))) for key in set(c0) | set(c1)}
            omega = {(3, zero_js): [F(0), F(2)], (1, zero_js): [F(0), F(0), F(0), F(-3, 2)],
                     (0, zero_js): [F(0), F(0), F(0), F(0), F(-1, 2)]}
            for key, val in diff.items():
                if val != ptrim(omega.get(key, [F(0)])):
                    return False, 'pinned family not affine in the gap with the cubic shift (m = %d, %s)' % (m, key)
            dM0, AM = scaled_hessian_dets(c0, m, -1)
            dS0, AS = scaled_hessian_dets(c0, m, 1)
            dM1, _ = scaled_hessian_dets(c1, m, -1)
            dS1, _ = scaled_hessian_dets(c1, m, 1)
            # (ii) d/dk det K_M = -6 det A_M and d/dk det K_S = +6 det A_S, exactly (d/dk = r^-1 d/dkappa)
            if ptrim(padd(dM1, pscale(dM0, F(-1)))) != ptrim(pscale(pmul([F(0), F(1)], AM), F(6 * sgn))):
                return False, 'd det K_M / dk != -6 det A_M (m = %d)' % m
            if ptrim(padd(dS1, pscale(dS0, F(-1)))) != ptrim(pscale(pmul([F(0), F(1)], AS), F(6))):
                return False, 'd det K_S / dk != 6 det A_S (m = %d)' % m
            # (iii) the common rY: det K_M + det K_S = 2 r Y + O(r^2), det K_S - det K_M = 12 k det A(0) + O(r^2)
            A0 = [[F(0)] * m for _ in range(m)]
            gamma = []
            for j in range(m):
                gamma.append(2 * free.get((2, tuple(1 if t == j else 0 for t in range(m))), F(0)))
                for l in range(m):
                    el = tuple((1 if t == j else 0) + (1 if t == l else 0) for t in range(m))
                    A0[j][l] = (2 if j == l else 1) * free.get((0, el), F(0))
            f4 = 24 * free[(4, zero_js)]
            Y = (f4 / 12) * det(A0) - quad(gamma, adj(A0), gamma) / 4
            for kap, dM, dS in ((kappa0, dM0, dS0), (kappa0 + 1, dM1, dS1)):
                tot = padd(dM, dS) + [F(0)] * 3
                dif = padd(padd(dS, pscale(dM, F(-1))), [F(0), -12 * kap * det(A0)]) + [F(0)] * 3
                if tot[0] != 0 or tot[1] != 2 * Y:
                    return False, 'det K_M + det K_S != 2 r Y + O(r^2) (m = %d)' % m
                if dif[0] != 0 or dif[1] != 0:
                    return False, 'det K_S - det K_M != 12 k det A(0) + O(r^2) (m = %d)' % m
                cases += 1
    # (iv) Theorem CU' constants: I_cand / c_1 = 3^(1/4)/2 (fourth power 3/16); the rejected cusp integral
    #      int_{s1}^{s2} (36 Delta^2 s^-8 - Y^2) ds = (16/7) Y^2 s1 - (8/7) Y^2 s2, s2 = 3^(1/4) s1, exactly in Q(3^(1/4));
    #      the small-kappa elder share 13/27
    if ((F(8, 7) / F(16, 7)) ** 4) * F(6, 2) != F(3, 16):
        return False, 'I_cand / c_1'
    theta = Q4([0, 1])
    pts = 0
    for Yv, Dv in ((F(1), F(8)), (F(1, 2), F(81, 32)), (F(3), F(3, 2))):
        s1 = rational_root(2 * Dv / Yv, 4)
        if s1 is None:
            continue
        anti = lambda s: Q4([0]) - Q4([F(36, 7) * Dv * Dv]) * s.power(-7) * Q4([s1 ** -7]) - Q4([Yv * Yv * s1]) * s
        # anti(t) evaluated at s = t * s1 with t in {1, theta}: F(s) = -(36/7) Delta^2 s^-7 - Y^2 s
        val = anti(theta) - (Q4([0]) - Q4([F(36, 7) * Dv * Dv * s1 ** -7]) - Q4([Yv * Yv * s1]))
        target = Q4([F(16, 7) * Yv * Yv * s1]) - Q4([F(8, 7) * Yv * Yv * s1]) * theta
        if not (val == target):
            return False, 'rejected cusp integral'
        pts += 1
    share = (72 * 2 - F(2, 3) * 2 ** 3) / (72 * 6 - F(2, 3) * 6 ** 3)
    if share != F(13, 27) or pts < 2:
        return False, 'elder share 13/27 or too few points'
    return True, {'pinned_cases': cases, 'dimensions': [2, 3], 'rejected_integral_points': pts,
                  'I_cand_over_c1': '3^(1/4)/2', 'small_kappa_elder_share': '13/27'}


# -------------------------------------------------------------------- C7: Gaussian-kernel covariances

def kap_n(n):
    if n % 2:
        return F(0)
    dfact = 1
    for t in range(n - 1, 0, -2):
        dfact *= t
    return F((-1) ** (n // 2) * dfact)


def cov(alpha, beta):
    """E[d^alpha f(0) d^beta f(0)] for the Gaussian kernel exp(-|z|^2/2)."""
    out = F((-1) ** sum(beta))
    for a, bb in zip(alpha, beta):
        out *= kap_n(a + bb)
    return out


def schur(targets, conds):
    """Conditional covariance of targets given conds (lists of multi-indices)."""
    Cc = [[cov(a, b) for b in conds] for a in conds]
    Ct = [[cov(a, b) for b in targets] for a in targets]
    X = [[cov(a, b) for b in conds] for a in targets]
    if conds:
        inv = inverse(Cc)
        for i in range(len(targets)):
            for j in range(len(targets)):
                Ct[i][j] -= sum(X[i][p] * inv[p][q] * X[j][q] for p in range(len(conds)) for q in range(len(conds)))
    return Ct


def check_C7(mutant):
    # d = 2, coordinates (x, y)
    fyy, f4, fxx, fxy = (0, 2), (4, 0), (2, 0), (1, 1)
    C = schur([fyy, f4], [fxx, fxy])
    if C != [[F(8, 3), F(2)], [F(2), F(30)]]:
        return False, 'd=2 even block %s' % C
    g = schur([(2, 1)], [(1, 0), (0, 1), (3, 0)])
    if g != [[F(2)]]:
        return False, 'd=2 gamma variance'
    tau2 = schur([(3, 0)], [(1, 0), (0, 1)])
    if tau2 != [[F(6)]]:
        return False, 'tau^2'
    D1 = C[0][0] / 2
    if D1 != F(4, 3):
        return False, 'D_1'
    # d = 3, coordinates (x, y, z): regression of f_xxxx on (f_yy, f_zz, f_yz) after conditioning on (f_xx, f_xy, f_xz)
    ev = [(0, 2, 0), (0, 0, 2), (0, 1, 1)]
    Cy = schur(ev + [(4, 0, 0)], [(2, 0, 0), (1, 1, 0), (1, 0, 1)])
    Cyy = [row[:3] for row in Cy[:3]]
    c4y = [Cy[3][j] for j in range(3)]
    beta = [sum(inverse(Cyy)[i][j] * c4y[j] for j in range(3)) for i in range(3)]
    resid = Cy[3][3] - sum(beta[i] * c4y[i] for i in range(3))
    if beta != [F(3, 5), F(3, 5), F(0)] or resid != F(138, 5):
        return False, 'd=3 regression %s %s' % (beta, resid)
    if Cyy != [[F(8, 3), F(2, 3), F(0)], [F(2, 3), F(8, 3), F(0)], [F(0), F(0), F(1)]]:
        return False, 'd=3 transverse block'
    g3 = schur([(2, 1, 0), (2, 0, 1)], [(1, 0, 0), (0, 1, 0), (0, 0, 1), (3, 0, 0)])
    if g3 != [[F(2), F(0)], [F(0), F(2)]]:
        return False, 'd=3 gamma covariance'
    return True, {'d2_even_block': '[[8/3, 2], [2, 30]]', 'd2_gamma_var': '2', 'tau2': '6', 'D1': '4/3',
                  'd3_transverse_block': '[[8/3, 2/3, 0], [2/3, 8/3, 0], [0, 0, 1]]', 'd3_gamma_cov': '2 I',
                  'd3_regression': '3/5, 3/5, 0', 'd3_residual': '138/5'}


CHECKS = [('C1_quartic_ridge_identities', check_C1), ('C2_elder_window_exact_maximin', check_C2),
          ('C3_fiber_reduction', check_C3), ('C4_cusp_limit_field_pinned_polynomials', check_C4),
          ('C5_model_endpoint_determinants_and_typed_window', check_C5), ('C6_cusp_integrals', check_C6),
          ('C7_gaussian_kernel_covariances', check_C7), ('C8_gap_affine_structure_and_cand_constants', check_C8)]
MUTANTS = ('M1', 'M2', 'M3', 'M4', 'M5')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', default=None)
    args = ap.parse_args()
    if args.mutant is not None and args.mutant not in MUTANTS:
        sys.stderr.write('unknown mutant label\n')
        return 2
    results = {}
    ok_all = True
    for name, fn in CHECKS:
        ok, info = fn(args.mutant)
        results[name] = {'passed': ok, 'info': info}
        ok_all = ok_all and ok
    out = {'object': 'CL-CUSP-SECOND-ORDER-20261001-v1.1', 'scientific_effect': 'NONE', 'passed': ok_all,
           'mutant': args.mutant, 'checks': results}
    sys.stdout.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main())
