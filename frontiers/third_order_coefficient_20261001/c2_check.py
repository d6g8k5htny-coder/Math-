#!/usr/bin/env python3
"""Controls for CL-THIRD-ORDER-COEFF-20261001-v1.2 (frontiers/third_order_coefficient_20261001/NOTE.md).
Standard library only. Run: python3 -B -S c2_check.py   (and with -O; output byte-identical). v1.1: every float sum is
math.fsum (exactly rounded; the built-in sum of floats changed in CPython 3.12) and the r-fit uses the scaled variable
r/max(r), so the output is the same on CPython 3.10-3.14 (checked). v1.2 (Codex P2 on v1.1): T4 runs at a refined grid
and compares with the former production grid and with the second r-set, so that its own spreads justify eight digits
(v1.1's coarse comparison grid under-resolved the height integral: 32 nodes in b moved c2 by 4.5e-8).
Mutants: --mutant M1|M2|M3|M4 must exit 1; an unknown label exits 2.

The two-point kernel of [R] (frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md):
    A_r(b, k, u) = 12 pi_r(v_r) E[|det H_M| |det H_S| 1{typed} | U_r = v_r] / r^2,
symmetric pin vector U_r and target v_r = (b - k r^3/2, -k r^2, 0, 12k, 0, ..., 0).  At fixed (b, k):
A_r = A_0 + r^2 A_2 + O(r^3).  The fold-scale finite part gives
    c  = (1/3)|S^{d-1}| int db int A_0(b,k) k^{-2/3} dk,
    c2 = (1/3)|S^{d-1}| f.p. int db int A_2(b,k) k^{-4/3} dk = (1/3)|S^{d-1}| int db int [A_2(b,k) - A_2(b,0)] k^{-4/3} dk.

  T1 d = 1, Gaussian kernel: c = C0 and c2 = 2 B2 of Math- #214 (closed forms)
  T2 d = 1, mixture (exp(-x^2/2) + exp(-2x^2))/2: c = C0 and c2 = 2 B2 (closed forms of #214, general spectral moments)
  T3 d = 2, Gaussian kernel: c = c_{2,inf} (merged reviews/side24_v1_coefficient_claude_20260929); c2 reported; two r-sets agree
  T4 d = 3, Gaussian kernel: c = c_{3,inf} = c_{3,24}(1 + O(e^{-288})) (merged coefficients/side24_v1); c2 reported at the
     grid (b 56, k 120, cone 48^2) and within 1e-8 of the grid (40, 80, 32^2) and of the second r-set
  T5 the expansion A_r = A_0 + r^2 A_2 + O(r^3) has no r^1 term (d = 2, 3, three test points each)
  T6 the subtracted term is the small-s limit of the cusp loss: A_2(b, 0) = -12 pi_0 E_0[Y^2 1{A<0} | b] (d = 2)

Numerics: conditioning in Decimal (prec 50), then floats; Gauss-Legendre quadrature; the r^2 coefficient by least squares
over five separations. Typed indicator: d = 1 none needed (exponentially small at fixed k); d = 2 1{f_yy(0) < 0};
d = 3 1{D_y^2 f(0) < 0} (2x2), the conditional expectation evaluated at A = diag(l1, l2) and integrated in eigenvalue
coordinates (transverse rotation invariance). These replacements change A_r by O(r^3) at fixed k.
"""
import argparse
import itertools
import json
import math
import sys
from decimal import Decimal, getcontext

getcontext().prec = 50
MUTANT = None


# ----------------------------------------------------------------------------------------------- small linear algebra
def dfact(n):
    out = 1
    while n > 1:
        out *= n
        n -= 2
    return out


def rho_der(kernel, g):
    """d^g rho(0) for rho = exp(-|z|^2/2) ('gauss') or (exp(-x^2/2) + exp(-2x^2))/2 ('mix', d = 1)"""
    if any(x % 2 for x in g):
        return 0
    if kernel == 'gauss':
        out = 1
        for x in g:
            out *= (-1) ** (x // 2) * dfact(x - 1)
        return out
    (x,) = g
    m = x // 2
    return Decimal((-1) ** m * dfact(x - 1) * (1 + 4 ** m)) / 2


def gauss_jordan_inv(A):
    n = len(A)
    M = [row[:] + [Decimal(int(i == j)) for j in range(n)] for i, row in enumerate(A)]
    det = Decimal(1)
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(M[i][c]))
        if p != c:
            M[c], M[p] = M[p], M[c]
            det = -det
        piv = M[c][c]
        det *= piv
        M[c] = [x / piv for x in M[c]]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return [row[n:] for row in M], det


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


# ----------------------------------------------------------------------------------------------- the pinned structure
_SIG_CACHE = {}


class Pinned:
    """jets at 0 up to total order N, pin rows of [R] section 2 at separation r along e_1, Gaussian conditioning"""

    def __init__(self, d, N, r, kernel, forms):
        self.d, self.N, self.r = d, N, Decimal(r)
        self.J = [a for n in range(N + 1) for a in itertools.product(range(n + 1), repeat=d) if sum(a) == n]
        self.idx = {a: i for i, a in enumerate(self.J)}
        key = (d, N, kernel)
        if key not in _SIG_CACHE:
            S = [[Decimal(0)] * len(self.J) for _ in self.J]
            for i, a in enumerate(self.J):
                for j, b in enumerate(self.J):
                    v = rho_der(kernel, tuple(x + y for x, y in zip(a, b)))
                    if v:
                        S[i][j] = Decimal(v) * (-1) ** sum(b)
            _SIG_CACHE[key] = S
        self.Sig = _SIG_CACHE[key]
        rows = self.pin_rows()
        n = len(self.J)
        MS = [[sum(row[t] * self.Sig[t][j] for t in range(n) if row[t]) for j in range(n)] for row in rows]
        S = [[sum(MS[i][t] * rows[j][t] for t in range(n) if rows[j][t]) for j in range(len(rows))] for i in range(len(rows))]
        Sinv, detS = gauss_jordan_inv(S)
        self.p = len(rows)
        self.Sinv = [[float(x) for x in row] for row in Sinv]
        self.detS = float(detS)
        G = [[sum(MS[q][i] * Sinv[q][j] for q in range(self.p)) for j in range(self.p)] for i in range(n)]   # Sig M^T S^-1
        self.cov, self.mcoef = {}, {}
        names = list(forms)
        vec = {u: self.deriv_at(*forms[u]) for u in names}
        Sv = {u: [sum(self.Sig[i][t] * vec[u][t] for t in range(n) if vec[u][t]) for i in range(n)] for u in names}
        MSv = {u: [sum(MS[q][t] * vec[u][t] for t in range(n) if vec[u][t]) for q in range(self.p)] for u in names}
        cG = {u: [sum(vec[u][t] * G[t][j] for t in range(n) if vec[u][t]) for j in range(self.p)] for u in names}
        for i, u in enumerate(names):
            self.mcoef[u] = [float(x) for x in cG[u]]
            for w in names[i:]:
                val = sum(vec[u][t] * Sv[w][t] for t in range(n) if vec[u][t]) - sum(cG[u][q] * MSv[w][q] for q in range(self.p))
                self.cov[(u, w)] = self.cov[(w, u)] = float(val)

    def deriv_at(self, beta, x):
        """vector over the jets of d^beta f at x e_1 (Taylor at 0, truncated at total order N)"""
        x = Decimal(x)
        c = [Decimal(0)] * len(self.J)
        j, xp, fac = 0, Decimal(1), 1
        while True:
            a = (beta[0] + j,) + tuple(beta[1:])
            if sum(a) > self.N:
                break
            c[self.idx[a]] += xp / fac
            j += 1
            xp *= x
            fac *= j
        return c

    def pin_rows(self):
        d, r = self.d, self.r
        e0, ex = (0,) * d, (1,) + (0,) * (d - 1)
        a, c = -r / 2, r / 2
        f_a, f_c, fx_a, fx_c = self.deriv_at(e0, a), self.deriv_at(e0, c), self.deriv_at(ex, a), self.deriv_at(ex, c)
        n = len(self.J)
        rows = [[(f_a[t] + f_c[t]) / 2 for t in range(n)], [(f_c[t] - f_a[t]) / r for t in range(n)],
                [(fx_c[t] - fx_a[t]) / r for t in range(n)],
                [6 / (r * r) * (fx_a[t] + fx_c[t] - 2 * (f_c[t] - f_a[t]) / r) for t in range(n)]]
        for s in range(1, d):
            ey = tuple(1 if i == s else 0 for i in range(d))
            ya, yc = self.deriv_at(ey, a), self.deriv_at(ey, c)
            rows += [[(ya[t] + yc[t]) / 2 for t in range(n)], [(yc[t] - ya[t]) / r for t in range(n)]]
        return rows

    def target(self, b, k):
        r = float(self.r)
        return [b - k * r ** 3 / 2, -k * r * r, 0.0, 12 * k] + [0.0] * (2 * (self.d - 1))

    def pi(self, v):
        q = math.fsum(v[i] * self.Sinv[i][j] * v[j] for i in range(self.p) for j in range(self.p))
        return (2 * math.pi) ** (-self.p / 2) / math.sqrt(self.detS) * math.exp(-q / 2)

    def mean(self, u, v):
        return math.fsum(c * x for c, x in zip(self.mcoef[u], v))


# ----------------------------------------------------------------------------------------------- polynomials
def pmul(p, q):
    out = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            e = tuple(x + y for x, y in zip(e1, e2))
            out[e] = out.get(e, 0.0) + c1 * c2
    return out


def matchings(lst):
    if not lst:
        yield []
        return
    first, rest = lst[0], lst[1:]
    for mm in matchings(rest):
        yield mm
    for i, x in enumerate(rest):
        for mm in matchings(rest[:i] + rest[i + 1:]):
            yield [(first, x)] + mm


def isserlis_poly(factors, aff, cov, nv):
    """E[prod (m_i + eps_i)] with affine means aff[i] (dict exponent -> coef) and covariance cov(i, j)"""
    total = {}
    zero = (0,) * nv
    n = len(factors)
    cache = {}

    def prod(us):
        key = tuple(sorted(us))
        if key not in cache:
            res = {zero: 1.0}
            for u in key:
                res = pmul(res, aff[u])
            cache[key] = res
        return cache[key]
    for mt in matchings(list(range(n))):
        c = 1.0
        used = set()
        for (a, b) in mt:
            c *= cov(factors[a], factors[b])
            used.update((a, b))
        if c == 0.0:
            continue
        for e, v in prod([factors[i] for i in range(n) if i not in used]).items():
            total[e] = total.get(e, 0.0) + c * v
    return total


# ----------------------------------------------------------------------------------------------- kernels
def forms_for(d, r):
    rf = Decimal(r)
    xM, xS = -rf / 2, rf / 2
    if d == 1:
        return {'hM': ((2,), xM), 'hS': ((2,), xS)}
    if d == 2:
        f = {}
        for nm, x in (('M', xM), ('S', xS)):
            f['xx' + nm], f['xy' + nm], f['yy' + nm] = ((2, 0), x), ((1, 1), x), ((0, 2), x)
        f['a'] = ((0, 2), Decimal(0))
        return f
    f = {}
    for nm, x in (('M', xM), ('S', xS)):
        for (i, j) in ((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)):
            beta = [0, 0, 0]
            beta[i] += 1
            beta[j] += 1
            f[(nm, i, j)] = (tuple(beta), x)
    f['a11'], f['a12'], f['a22'] = ((0, 2, 0), Decimal(0)), ((0, 1, 1), Decimal(0)), ((0, 0, 2), Decimal(0))
    return f


class Kernel:
    def __init__(self, d, N, r, kernel):
        self.d, self.r = d, float(r)
        self.P = Pinned(d, N, r, kernel, forms_for(d, r))
        if d == 2:
            self.setup2()
        if d == 3:
            self.setup3()

    # d = 2: E[X Y 1{a<0}], X = det H_M, Y = -det H_S; conditioning on a
    def setup2(self):
        P = self.P
        self.terms = [(+1, ('xxM', 'yyM', 'xxS', 'yyS')), (-1, ('xxM', 'yyM', 'xyS', 'xyS')),
                      (-1, ('xyM', 'xyM', 'xxS', 'yyS')), (+1, ('xyM', 'xyM', 'xyS', 'xyS'))]
        sa2 = P.cov[('a', 'a')]
        self.sa2 = sa2
        self.beta = {u: P.cov[(u, 'a')] / sa2 for u in P.mcoef if u != 'a'}
        self.cp = {(u, w): P.cov[(u, w)] - self.beta[u] * self.beta[w] * sa2 for u in self.beta for w in self.beta}

    def Z2(self, v):
        P = self.P
        ma = P.mean('a', v)
        mu = {u: P.mean(u, v) for u in self.beta}
        s = math.sqrt(self.sa2)
        cc = -ma
        phi = math.exp(-cc * cc / (2 * self.sa2)) / (s * math.sqrt(2 * math.pi))
        T = [0.5 * math.erfc(-cc / (s * math.sqrt(2))), -self.sa2 * phi]
        for n in range(2, 5):
            T.append((n - 1) * self.sa2 * T[n - 2] - self.sa2 * cc ** (n - 1) * phi)
        tot = 0.0
        for sgn, nm in self.terms:
            aff = {i: {(0,): mu[u], (1,): self.beta[u]} for i, u in enumerate(nm)}
            poly = isserlis_poly(list(range(4)), aff, lambda i, j: self.cp[(nm[i], nm[j])], 1)
            tot += sgn * math.fsum(c * T[e[0]] for e, c in poly.items())
        return -tot

    # d = 3: polynomial in (b_eff, k, l1, l2) of E[det H_M det H_S | A = diag(l1, l2)]
    def setup3(self):
        P = self.P
        al = ['a11', 'a12', 'a22']
        C = [[P.cov[(a, b)] for b in al] for a in al]
        det = (C[0][0] * (C[1][1] * C[2][2] - C[1][2] * C[2][1]) - C[0][1] * (C[1][0] * C[2][2] - C[1][2] * C[2][0])
               + C[0][2] * (C[1][0] * C[2][1] - C[1][1] * C[2][0]))
        inv = [[(C[(j + 1) % 3][(i + 1) % 3] * C[(j + 2) % 3][(i + 2) % 3] - C[(j + 1) % 3][(i + 2) % 3] * C[(j + 2) % 3][(i + 1) % 3]) / det
                for j in range(3)] for i in range(3)]
        self.Caa_inv, self.Caa_det = inv, det
        hn = [u for u in P.mcoef if u not in al]
        B = {u: [math.fsum(P.cov[(u, al[j])] * inv[j][i] for j in range(3)) for i in range(3)] for u in hn}
        self.cp3 = {(u, w): P.cov[(u, w)] - math.fsum(B[u][i] * P.cov[(al[i], w)] for i in range(3)) for u in hn for w in hn}
        r = self.r

        def kcoef(u):    # coefficient of k in the conditional mean: v = (b_eff, -k r^2, 0, 12k, 0, ...)
            mc = P.mcoef[u]
            return -mc[1] * r * r + 12 * mc[3]
        self.mu_a = [(P.mcoef[a][0], kcoef(a)) for a in al]
        if max(abs(m1) for (_, m1) in self.mu_a) > 1e-20:       # parity: the transverse block does not see k
            raise RuntimeError('k-dependence of the transverse mean')
        aff = {}
        for u in hn:
            cb = P.mcoef[u][0] - math.fsum(B[u][j] * P.mcoef[al[j]][0] for j in range(3))
            ck = kcoef(u) - math.fsum(B[u][j] * kcoef(al[j]) for j in range(3))
            aff[u] = {(1, 0, 0, 0): cb, (0, 1, 0, 0): ck, (0, 0, 1, 0): B[u][0], (0, 0, 0, 1): B[u][2]}
        perms = list(itertools.permutations(range(3)))

        def sgn(p):
            return 1 if sum(1 for i in range(3) for j in range(i + 1, 3) if p[i] > p[j]) % 2 == 0 else -1
        poly = {}
        for p in perms:
            for q in perms:
                fac = [('M', min(i, p[i]), max(i, p[i])) for i in range(3)] + [('S', min(i, q[i]), max(i, q[i])) for i in range(3)]
                part = isserlis_poly(fac, aff, lambda x, y: self.cp3[(x, y)], 4)
                s = sgn(p) * sgn(q)
                for e, c in part.items():
                    poly[e] = poly.get(e, 0.0) + s * c
        self.poly3 = poly

    def cone_moments(self, beff, k, nq):
        """M_ij = pi * int_{l2<l1<0} l1^i l2^j p_A(diag(l1, l2)) (l1 - l2) dl, i + j <= 6"""
        mu = [m0 * beff + m1 * k for (m0, m1) in self.mu_a]
        inv = self.Caa_inv
        norm = 1 / ((2 * math.pi) ** 1.5 * math.sqrt(self.Caa_det))
        Smax = 10 + 1.2 * abs(mu[0])
        xs, ws = gauss_legendre(nq)
        M = {}
        for x1, w1 in zip(xs, ws):
            s = Smax * (x1 + 1) / 2
            for x2, w2 in zip(xs, ws):
                t = Smax * (x2 + 1) / 2
                l1, l2 = -s, -s - t
                z = (l1 - mu[0], -mu[1], l2 - mu[2])
                q = math.fsum(z[i] * inv[i][j] * z[j] for i in range(3) for j in range(3))
                w = w1 * w2 * (Smax / 2) ** 2 * norm * math.exp(-q / 2) * (l1 - l2) * math.pi
                for i in range(7):
                    for j in range(7 - i):
                        M[(i, j)] = M.get((i, j), 0.0) + w * l1 ** i * l2 ** j
        return M

    def Z3(self, beff, k, M):
        tot = 0.0
        for (eb, ek, e1, e2), c in self.poly3.items():
            tot += c * beff ** eb * k ** ek * M[(e1, e2)]
        return -tot

    def A(self, b, k, moments=None):
        P = self.P
        if self.d == 3:
            beff = b
            v = P.target(beff + k * self.r ** 3 / 2, k)
            return 12 * P.pi(v) * self.Z3(beff, k, moments) / self.r ** 2
        v = P.target(b, k)
        if self.d == 1:
            Z = -(P.mean('hM', v) * P.mean('hS', v) + P.cov[('hM', 'hS')])
        else:
            Z = self.Z2(v)
        return 12 * P.pi(v) * Z / self.r ** 2


def coefficients(d, kernel, N, rs, nb=48, nt=80, nq=28, K=8.0):
    """c and c2 by the fold-scale finite part"""
    ks = [Kernel(d, N, r, kernel) for r in rs]
    rf = [float(r) for r in rs]
    rmax = max(rf)
    basis = [[1.0, (r / rmax) ** 2, (r / rmax) ** 3, (r / rmax) ** 4] for r in rf]      # scaled: well conditioned
    if MUTANT == 'M2':
        basis = [[1.0, (r / rmax) ** 3, (r / rmax) ** 2, (r / rmax) ** 4] for r in rf]
    # least-squares rows for the first two coefficients
    XtX = [[math.fsum(basis[i][a] * basis[i][b] for i in range(len(rf))) for b in range(4)] for a in range(4)]
    inv, _ = gauss_jordan_inv([[Decimal(x) for x in row] for row in XtX])
    inv = [[float(x) for x in row] for row in inv]
    W = [[math.fsum(inv[a][c] * basis[i][c] for c in range(4)) / (1.0 if a == 0 else rmax ** 2) for i in range(len(rf))]
         for a in range(2)]
    B, T = 8.0, K ** (1 / 3)
    xb, wb = gauss_legendre(nb)
    xt, wt = gauss_legendre(nt)
    sphere = {1: 2.0, 2: 2 * math.pi, 3: 4 * math.pi}[d]
    if MUTANT == 'M3' and d == 2:
        sphere = math.pi
    c = c2 = tail = 0.0
    for xi, wi in zip(xb, wb):
        b = B * xi
        mom = [kk.cone_moments(b, 0.0, nq) for kk in ks] if d == 3 else [None] * len(ks)
        vals0 = [kk.A(b, 0.0, m) for kk, m in zip(ks, mom)]
        A20 = math.fsum(W[1][i] * vals0[i] for i in range(len(rf)))
        tail += B * wi * (-A20)
        for xj, wj in zip(xt, wt):
            t = T * (xj + 1) / 2
            k = t ** 3
            vals = [kk.A(b, k, m) for kk, m in zip(ks, mom)]
            A0 = math.fsum(W[0][i] * vals[i] for i in range(len(rf)))
            A2 = math.fsum(W[1][i] * vals[i] for i in range(len(rf)))
            w = B * wi * T * wj / 2
            c += w * 3 * A0
            if MUTANT == 'M1':
                c2 += w * 3 * A2 / t ** 2
            else:
                c2 += w * 3 * (A2 - A20) / t ** 2
    c *= sphere / 3
    c2 = c2 * sphere / 3 + (0.0 if MUTANT == 'M4' else sphere * T ** -1 * tail)
    return c, c2


# ----------------------------------------------------------------------------------------------- closed forms of #214
def d1_closed(kernel):
    if kernel == 'gauss':
        l2, l4, l6, l8 = 1.0, 3.0, 15.0, 105.0
    else:
        l2, l4, l6, l8 = 2.5, 25.5, 487.5, 13492.5
    D = l2 * l6 - l4 * l4
    s3 = math.sqrt(D / l2)
    p12 = 1 / (2 * math.pi * math.sqrt(l2 * l4))
    C0 = 2 * 72 ** (-1 / 6) * math.gamma(7 / 6) * (2 * math.pi) ** -0.5 * p12 * s3 ** (4 / 3)
    Q = 4 * l2 ** 2 * l4 * l8 + 26 * l2 * l4 ** 2 * l6 - 5 * l2 ** 2 * l6 ** 2 - 25 * l4 ** 4
    B2 = 2 ** 0.5 * 3 ** (1 / 3) * math.gamma(5 / 6) * (2 * math.pi) ** -0.5 * p12 * s3 ** (2 / 3) * Q / (120 * l2 * l4 * D)
    return C0, 2 * B2


C2INF = 0.073406919306034271030   # reviews/side24_v1_coefficient_claude_20260929 (merged)
C3INF = 0.04177593184059834334    # coefficients/side24_v1 (merged), c_{3,24} = c_{3,inf}(1 + O(e^{-288}))
RS = ['0.003', '0.005', '0.007', '0.009', '0.011']
RS_B = ['0.002', '0.004', '0.006', '0.008']
RS_D1 = ['0.001', '0.002', '0.003', '0.004', '0.005']


def main():
    global MUTANT
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', default=None)
    args = ap.parse_args()
    if args.mutant is not None and args.mutant not in ('M1', 'M2', 'M3', 'M4'):
        sys.stderr.write('unknown mutant label\n')
        return 2
    MUTANT = args.mutant
    out = {'object': 'CL-THIRD-ORDER-COEFF-20261001-v1.2 controls', 'scientific_effect': 'NONE', 'mutant': MUTANT, 'checks': {}}
    ok_all = True
    for name, kern, K, nt in (('T1_d1_gauss', 'gauss', 8.0, 80), ('T2_d1_mixture', 'mix', 27.0, 120)):
        c, c2 = coefficients(1, kern, 12, RS_D1, nt=nt, K=K)
        C0, twoB2 = d1_closed(kern)
        ok = abs(c / C0 - 1) < 1e-10 and abs(c2 / twoB2 - 1) < 1e-8
        out['checks'][name] = {'c': '%.12f' % c, 'C0_closed': '%.12f' % C0, 'c2': '%.10f' % c2, '2B2_closed': '%.10f' % twoB2,
                               'passed': ok}
        ok_all &= ok
    c, c2 = coefficients(2, 'gauss', 10, RS)
    cb, c2b = coefficients(2, 'gauss', 10, RS_B)
    ok = abs(c / C2INF - 1) < 1e-10 and abs(c2b - c2) < 1e-8
    out['checks']['T3_d2_gauss'] = {'c': '%.12f' % c, 'c_2inf': '%.12f' % C2INF, 'c2': '%.10f' % c2, 'c2_second_rset': '%.10f' % c2b,
                                    'c2_over_c': '%.8f' % (c2 / c), 'passed': ok}
    ok_all &= ok
    c, c2 = coefficients(3, 'gauss', 8, RS, nb=56, nt=120, nq=48)
    c_g, c2_g = coefficients(3, 'gauss', 8, RS, nb=40, nt=80, nq=32)
    c_r, c2_r = coefficients(3, 'gauss', 8, RS_B, nb=40, nt=80, nq=32)
    ok = abs(c / C3INF - 1) < 1e-10 and abs(c2 - c2_g) < 1e-8 and abs(c2 - c2_r) < 1e-8
    out['checks']['T4_d3_gauss'] = {'c': '%.13f' % c, 'c_3inf': '%.13f' % C3INF, 'c2': '%.10f' % c2,
                                    'c2_grid_40_80_32': '%.10f' % c2_g, 'c2_second_rset': '%.10f' % c2_r,
                                    'c2_over_c': '%.8f' % (c2 / c),
                                    'grids': 'b 56, k 120, cone 48x48; comparisons b 40, k 80, cone 32x32 (both r-sets)',
                                    'passed': ok}
    ok_all &= ok
    # T5: the fold-scale expansion is even at first order (#191): interpolating A_r on (1, r, r^2, r^3, r^4) at the five
    # separations gives a negligible r^1 coefficient
    t5 = {}
    rf = [float(r) for r in RS]
    rmx5 = Decimal(max(RS, key=Decimal))
    Xb = [[Decimal(1), Decimal(r) / rmx5, (Decimal(r) / rmx5) ** 2, (Decimal(r) / rmx5) ** 3, (Decimal(r) / rmx5) ** 4] for r in RS]
    inv, _ = gauss_jordan_inv(Xb)
    ok5 = True
    for d, N in ((2, 10), (3, 8)):
        ks = [Kernel(d, N, r, 'gauss') for r in RS]
        for (b, k) in ((0.3, 0.7), (-1.0, 0.2), (1.5, 1.3)):
            mom = [kk.cone_moments(b, 0.0, 32) for kk in ks] if d == 3 else [None] * len(ks)
            vals = [kk.A(b, k, m) for kk, m in zip(ks, mom)]
            co = [math.fsum(float(inv[a][i]) * vals[i] for i in range(len(rf))) for a in range(5)]
            if MUTANT == 'M2':
                co[1] = co[2]
            rm = float(rmx5)
            rel1, rel2 = co[1] / rm / co[0], co[2] / rm ** 2 / co[0]
            t5['d%d_b%g_k%g' % (d, b, k)] = {'abs_r1_over_A0_below_1e-6': abs(rel1) < 1e-6, 'r2_over_A0': '%.4f' % rel2}
            ok5 &= abs(rel1) < 1e-6 and abs(rel2) > 1e-2
    t5['passed'] = bool(ok5)
    out['checks']['T5_no_r1_term'] = t5
    ok_all &= ok5
    # T6: the subtracted term is the cusp loss limit (0.1): A_2(b, 0) = -12 pi_0 E_0[Y^2 1{A<0} | b] in d = 2,
    # Y = f_xxxx a / 12 - gamma^2 / 4, a = f_yy(0), gamma = f_xxy(0)
    ks = [Kernel(2, 10, r, 'gauss') for r in RS]
    rmx = max(float(r) for r in RS)
    basis = [[1.0, (float(r) / rmx) ** 2, (float(r) / rmx) ** 3, (float(r) / rmx) ** 4] for r in RS]
    XtX = [[math.fsum(basis[i][a] * basis[i][b] for i in range(len(RS))) for b in range(4)] for a in range(4)]
    inv4, _ = gauss_jordan_inv([[Decimal(x) for x in row] for row in XtX])
    inv4 = [[float(x) for x in row] for row in inv4]
    W2 = [math.fsum(inv4[1][c] * basis[i][c] for c in range(4)) / rmx ** 2 for i in range(len(RS))]
    P0 = Pinned(2, 10, '0.000001', 'gauss', {'f4': ((4, 0), Decimal(0)), 'g': ((2, 1), Decimal(0)), 'a': ((0, 2), Decimal(0))})
    xg, wg = gauss_legendre(64)
    t6, ok6 = {}, True
    for b in (-1.2, 0.0, 0.7, 2.0):
        A20 = math.fsum(W2[i] * ks[i].A(b, 0.0) for i in range(len(RS)))
        v = P0.target(b, 0.0)
        mu = {u: P0.mean(u, v) for u in ('f4', 'g', 'a')}
        sa2 = P0.cov[('a', 'a')]
        s = math.sqrt(sa2)
        bf, bg = P0.cov[('f4', 'a')] / sa2, P0.cov[('g', 'a')] / sa2
        vf, vg = P0.cov[('f4', 'f4')] - bf * bf * sa2, P0.cov[('g', 'g')] - bg * bg * sa2
        cfg = P0.cov[('f4', 'g')] - bf * bg * sa2
        lo, hi = mu['a'] - 14 * s, min(0.0, mu['a'] + 14 * s)
        tot = 0.0
        for x, w in zip(xg, wg):
            a = lo + (hi - lo) * (x + 1) / 2
            dens = math.exp(-(a - mu['a']) ** 2 / (2 * sa2)) / (s * math.sqrt(2 * math.pi))
            mf, mg = mu['f4'] + bf * (a - mu['a']), mu['g'] + bg * (a - mu['a'])
            eg2 = vg + mg * mg
            ey2 = (a / 12) ** 2 * (vf + mf * mf) - (a / 24) * (mf * eg2 + 2 * cfg * mg) + (3 * vg * vg + 6 * vg * mg * mg + mg ** 4) / 16
            tot += w * (hi - lo) / 2 * dens * ey2
        pred = -12 * P0.pi(v) * tot
        rel = A20 / pred - 1
        if MUTANT == 'M1':
            rel = 1.0
        t6['b%g' % b] = {'A2_b0': '%.8e' % A20, 'loss_limit': '%.8e' % pred, 'agree_1e-6': abs(rel) < 1e-6}
        ok6 &= abs(rel) < 1e-6
    t6['passed'] = bool(ok6)
    out['checks']['T6_overlap_term_d2'] = t6
    ok_all &= ok6
    out['passed'] = bool(ok_all)
    sys.stdout.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main())
