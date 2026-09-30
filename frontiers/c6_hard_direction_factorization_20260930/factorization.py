#!/usr/bin/env python3
"""Hard-direction factorization of the near cluster coefficients for the Gaussian kernel (Math-, object
CL-C6-HARD-DIRECTION-FACTORIZATION-20260930-v1).  Standard library only.

    python -B -S factorization.py            # full run: writes RESULTS.json (about two minutes)
    python -B -S factorization.py --check    # exact lemma, closed forms and replay against RESULTS.json (rc 0)
    python -B -S factorization.py --check --mutant NAME   # must exit 1

Objects (see PROOF.md).  For the unit Gaussian kernel K(x) = exp(-|x|^2/2) in dimension d = m + 1, the [SC] (17)
measure factors through the hard directions: for every nonnegative measurable g of the soft cubic (s, a, beta, c),

    integral g dM^(d) = R_d(b) integral g dM^(2),      R_d(b) = N_d(b) m_(2,b) / m_(d,b),

    N_d(b)  = c_m (2 pi)^(-m(m-1)/4) integral_(0 < h_2 < ... < h_m) prod h_j^3 phi_2(h_j - b) prod_(i<j) (h_j - h_i) dh,
    m_(d,b) = E[(det A)^2 1{A negative definite}],  A = -b I_m + G_m  (GOE: diagonal variance 2, off-diagonal 1),
    m_(2,b) = E[A^2 1{A < 0}],  A ~ N(-b, 2),      phi_2 = N(0, 2) density,   c_m as in [SC] (8).

In particular a_j^(d) = R_d(b) alpha_j^(2) for the near coefficients [SC] (20), and R_3(0) = (32 + 28 sqrt2)/17.
Not a proof of any source theorem; scientific effect NONE.
"""
import argparse
import itertools
import json
import math
import os
import random
import sys
from fractions import Fraction as Fr
from math import erf, exp, factorial, gamma, pi, sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
MUTANTS = ('drop-vandermonde', 'hard-power-two', 'drop-spectral-constant')
MUT = None
REPLAY_TOL = 1e-9
DIMS = (2, 3, 4, 5)
BS = (0.0, 1.0)


def require(cond, msg):
    if not cond:
        print(json.dumps({'check': 'FAIL', 'what': msg, 'mutant': MUT}))
        sys.exit(1)


# ----------------------------------------------------------------------------- exact one-site jet law
def c_even(n):
    """d^n/dx^n exp(-x^2/2) at 0 = (-1)^(n/2) (n-1)!! for even n, 0 for odd n."""
    if n % 2:
        return Fr(0)
    v = Fr(1)
    for j in range(1, n, 2):
        v *= j
    return v * (-1) ** (n // 2)


def cov_point(al, be):
    """Cov(d^al f(0), d^be f(0)) = (-1)^|al| d^(al+be) K(0), exact rational."""
    v = Fr((-1) ** sum(al))
    for a, b in zip(al, be):
        v *= c_even(a + b)
    return v


def unit(d, i, n=1):
    v = [0] * d
    v[i] = n
    return tuple(v)


def add(*vs):
    return tuple(sum(v[i] for v in vs) for i in range(len(vs[0])))


def mat_inv(M):
    n = len(M)
    A = [row[:] + [Fr(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]


def conditional(targets, obs):
    """Regression matrix and conditional covariance of the targets given the observations (exact)."""
    Soo = [[cov_point(a, b) for b in obs] for a in obs]
    Sto = [[cov_point(a, b) for b in obs] for a in targets]
    Stt = [[cov_point(a, b) for b in targets] for a in targets]
    inv = mat_inv(Soo)
    reg = [[sum(Sto[i][k] * inv[k][j] for k in range(len(obs))) for j in range(len(obs))] for i in range(len(targets))]
    cc = [[Stt[i][j] - sum(reg[i][k] * Sto[j][k] for k in range(len(obs))) for j in range(len(targets))] for i in range(len(targets))]
    return reg, cc


def contact_frame(d):
    """U_0 of [SC] section 2: f, all first derivatives, f_xx, f_x y_i, f_xxx (values b, 0, ..., 0, 12k)."""
    zero = (0,) * d
    x = unit(d, 0)
    return [zero] + [unit(d, i) for i in range(d)] + [unit(d, 0, 2)] + [add(x, unit(d, i)) for i in range(1, d)] + [unit(d, 0, 3)]


def lemma_one(d):
    """The conditional law of (A, T) given U_0 (Lemma 1 of PROOF.md), checked exactly in dimension d."""
    obs = contact_frame(d)
    even = [add(unit(d, i), unit(d, j)) for i in range(1, d) for j in range(i, d)]
    odd = [al for al in itertools.product(range(4), repeat=d) if sum(al) == 3 and al != unit(d, 0, 3)]
    reg_e, cc_e = conditional(even, obs)
    reg_o, cc_o = conditional(odd, obs)
    # even part: mean -b on the diagonal entries (coefficient -1 on f, 0 on everything else), covariance diag(2 on
    # diagonal entries, 1 on off-diagonal entries), no dependence on f_xxx
    for i, al in enumerate(even):
        diag = max(al) == 2
        require(reg_e[i][0] == (Fr(-1) if diag else Fr(0)) and all(reg_e[i][j] == 0 for j in range(1, len(obs))),
                'even mean coefficients d=%d %r' % (d, al))
        for j, be in enumerate(even):
            want = Fr(0) if i != j else (Fr(2) if diag else Fr(1))
            require(cc_e[i][j] == want, 'even conditional covariance d=%d %r %r' % (d, al, be))
    # odd part: centered (no dependence on b or on f_xxx = 12k), independent, variances 6 / 2 / 1 by multiplicity
    for i, al in enumerate(odd):
        # only f (= b) and f_xxx (= 12k) are nonzero in U_0; the odd mean must not depend on either
        require(reg_o[i][0] == 0 and reg_o[i][-1] == 0, 'odd conditional mean zero d=%d %r' % (d, al))
        mult = sorted(al, reverse=True)
        want = Fr(6) if mult[0] == 3 else (Fr(2) if mult[0] == 2 else Fr(1))
        for j, be in enumerate(odd):
            require(cc_o[i][j] == (want if i == j else Fr(0)), 'odd conditional covariance d=%d %r %r' % (d, al, be))
    # even/odd independence: cross covariances vanish identically by parity
    require(all(cov_point(a, b) == 0 for a in even for b in odd), 'even/odd cross covariance d=%d' % d)
    # the planar one-site table of Math-#168 (exact structure) is the d = 2 case
    return {'d': d, 'observations': len(obs), 'even_jets': len(even), 'odd_jets': len(odd),
            'even_law': 'A | U_0 = -b I + GOE(diag 2, off 1)', 'odd_law': 'centered, independent, var 6/2/1 by multiplicity'}


# ----------------------------------------------------------------------------- quadrature and special functions
def phi(x):
    return exp(-x * x / 2) / sqrt(2 * pi)


def Phi(x):
    return 0.5 * (1 + erf(x / sqrt(2)))


def phi2(x):
    return phi(x / sqrt(2)) / sqrt(2)


def gauss_legendre(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for m in range(2, n + 1):
                p0, p1 = p1, ((2 * m - 1) * x * p1 - (m - 1) * p0) / m
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-15:
                break
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


def gl(f, lo, hi, rule):
    mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
    return half * sum(w * f(mid + half * x) for x, w in zip(*rule))


def c_m(m):
    """[SC] (8) through Mehta's integral: H_m = (2 pi)^(m/2) prod_(j<=m) Gamma(1 + j/2) / (Gamma(3/2)^m m!)."""
    if MUT == 'drop-spectral-constant':
        return 1.0
    return pi ** (m * (m - 1) / 4) * factorial(m) * gamma(1.5) ** m / math.prod(gamma(1 + j / 2) for j in range(1, m + 1))


def m2(b):
    """E[A^2 1{A < 0}], A ~ N(-b, 2) (Math-#168's m_(2,b))."""
    mu, s = -b, sqrt(2)
    t = mu / s
    return (mu * mu + s * s) * Phi(-t) - mu * s * phi(t)


def ordered_integral(m, weight, lo, hi, rule):
    """c_m (2 pi)^(-m(m-1)/4) integral over lo < l_1 < ... < l_m < hi of prod weight(l_i) times the Vandermonde."""
    pref = c_m(m) * (2 * pi) ** (-m * (m - 1) / 4)

    def rec(prev, depth):
        if depth == m:
            return 1.0

        def f(l):
            v = weight(l)
            if MUT != 'drop-vandermonde':
                for p in prev:
                    v *= (l - p)
            return v * rec(prev + [l], depth + 1)
        return gl(f, prev[-1] if prev else lo, hi, rule)
    return pref * rec([], 0)


_CACHE = {}


def default_order(d):
    return 40 if d >= 5 else 60


def N_d(d, b, n=None, L=14.0):
    """Hard-direction factor: the m - 1 hard eigenvalues h > 0 with weight h^3 phi_2(h - b) and their Vandermonde,
    times c_m (2 pi)^(-m(m-1)/4); the soft eigenvalue sits at 0 and contributes phi_2(b) on both sides of the ratio."""
    m = d - 1
    n = n or default_order(d)
    key = ('N', d, b, n, L, MUT)
    if key in _CACHE:
        return _CACHE[key]
    pref = c_m(m) * (2 * pi) ** (-m * (m - 1) / 4)
    if m == 1:
        _CACHE[key] = pref
        return pref
    power = 2 if MUT == 'hard-power-two' else 3
    rule = gauss_legendre(n)
    k = m - 1

    def rec(prev, depth):
        if depth == k:
            return 1.0

        def f(h):
            v = h ** power * phi2(h - b)
            if MUT != 'drop-vandermonde':
                for p in prev:
                    v *= (h - p)
            return v * rec(prev + [h], depth + 1)
        return gl(f, prev[-1] if prev else 0.0, L, rule)
    _CACHE[key] = pref * rec([], 0)
    return _CACHE[key]


def m_d(d, b, n=None, L=14.0):
    """E[(det A)^2 1{A negative definite}] for A = -b I_m + GOE_m, by the ordered eigenvalue density."""
    m = d - 1
    if m == 1:
        return m2(b)
    n = n or default_order(d)
    key = ('m', d, b, n, L, MUT)
    if key not in _CACHE:
        _CACHE[key] = ordered_integral(m, lambda l: l * l * phi2(l + b), -L, 0.0, gauss_legendre(n))
    return _CACHE[key]


def normalization(d, b, n=None, L=14.0):
    """Total mass of the eigenvalue density: must be 1 (tests c_m, the (2 pi) power and the quadrature)."""
    m = d - 1
    n = n or default_order(d)
    return ordered_integral(m, lambda l: phi2(l + b), -L - abs(b), L + abs(b), gauss_legendre(n))


def R_d(d, b, n=None):
    return N_d(d, b, n) * m2(b) / m_d(d, b, n)


def closed_forms():
    """b = 0, d = 3: m_(3,0) = (7 - 4 sqrt2)/2, N_3(0) = 2 sqrt2, R_3(0) = (32 + 28 sqrt2)/17; d = 2: R_2 = 1."""
    return {'m_3_0': (7 - 4 * sqrt(2)) / 2, 'N_3_0': 2 * sqrt(2), 'R_3_0': (32 + 28 * sqrt(2)) / 17,
            'E_absA3_negative_b0': 4 / sqrt(pi)}


# ----------------------------------------------------------------------------- Monte Carlo controls
def det(M):
    n = len(M)
    A = [r[:] for r in M]
    dt = 1.0
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        if A[p][c] == 0:
            return 0.0
        if p != c:
            A[c], A[p] = A[p], A[c]
            dt = -dt
        dt *= A[c][c]
        for r in range(c + 1, n):
            f = A[r][c] / A[c][c]
            for j in range(c, n):
                A[r][j] -= f * A[c][j]
    return dt


def n_negative(M):
    """Negative eigenvalues of a symmetric matrix from the signs of its leading principal minors (generic case)."""
    n = len(M)
    seq = [1.0] + [det([row[:k] for row in M[:k]]) for k in range(1, n + 1)]
    return sum(1 for i in range(n) if seq[i] * seq[i + 1] < 0)


def mc_m_d(d, b, n, seed):
    rng = random.Random(seed)
    m = d - 1
    acc = acc2 = 0.0
    for _ in range(n):
        A = [[0.0] * m for _ in range(m)]
        for i in range(m):
            A[i][i] = -b + sqrt(2) * rng.gauss(0, 1)
            for j in range(i + 1, m):
                A[i][j] = A[j][i] = rng.gauss(0, 1)
        v = det(A) ** 2 if n_negative(A) == m else 0.0
        acc += v
        acc2 += v * v
    mu = acc / n
    return {'value': mu, 'se': sqrt(max(acc2 / n - mu * mu, 0.0) / n), 'samples': n}


def mc_N_3(b, n, seed, eps=0.05):
    """N_3(b) phi_2(b) = lim E[l_other^2 1{|l_max| < eps}]/(2 eps) for A = -b I_2 + GOE_2 (density of the largest
    eigenvalue at 0 times the conditional second moment of the other one)."""
    rng = random.Random(seed)
    acc = acc2 = 0.0
    for _ in range(n):
        p = -b + sqrt(2) * rng.gauss(0, 1)
        q = -b + sqrt(2) * rng.gauss(0, 1)
        g = rng.gauss(0, 1)
        mid, rad = 0.5 * (p + q), sqrt(0.25 * (p - q) ** 2 + g * g)
        lmax, lother = mid + rad, mid - rad
        v = lother * lother / (2 * eps) if abs(lmax) < eps else 0.0
        acc += v
        acc2 += v * v
    mu = acc / n
    return {'value': mu / phi2(b), 'se': sqrt(max(acc2 / n - mu * mu, 0.0) / n) / phi2(b), 'samples': n, 'eps': eps}


# ----------------------------------------------------------------------------- finite-r normalizer Z_r / r^2 (Monte Carlo)
def hermite(n, x):
    if n == 0:
        return 1.0
    h0, h1 = 1.0, x
    for k in range(1, n):
        h0, h1 = h1, x * h1 - k * h0
    return h1


def kernel_derivative(gam, y):
    """d^gam K(y) for K(y) = exp(-|y|^2/2): prod (-1)^gam_i He_gam_i(y_i) exp(-y_i^2/2)."""
    v = 1.0
    for g, yi in zip(gam, y):
        v *= (-1) ** g * hermite(g, yi) * exp(-yi * yi / 2)
    return v


def cov_two_point(al, s, be, t):
    """Cov(d^al f(s), d^be f(t)) = (-1)^|al| d^(al+be) K(t - s)."""
    return (-1) ** sum(al) * kernel_derivative(add(al, be), [ti - si for si, ti in zip(s, t)])


def cholesky(S):
    n = len(S)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = S[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                if s <= 0:
                    raise ValueError('not positive definite')
                L[i][i] = sqrt(s)
            else:
                L[i][j] = s / L[j][j]
    return L


def jacobi_eigen(S, sweeps=100):
    """Eigen decomposition of a small symmetric matrix by cyclic Jacobi rotations: returns (eigenvalues, V) with S = V diag V^T."""
    n = len(S)
    A = [row[:] for row in S]
    V = [[float(i == j) for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-30:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(A[p][q]) < 1e-300:
                    continue
                theta = 0.5 * math.atan2(2 * A[p][q], A[q][q] - A[p][p])
                c, s_ = math.cos(theta), math.sin(theta)
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p], A[k][q] = c * akp - s_ * akq, s_ * akp + c * akq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k], A[q][k] = c * apk - s_ * aqk, s_ * apk + c * aqk
                for k in range(n):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p], V[k][q] = c * vkp - s_ * vkq, s_ * vkp + c * vkq
    return [A[i][i] for i in range(n)], V


def sym_sqrt(S):
    """Symmetric square root with negative rounding eigenvalues clipped to zero (S = L L^T)."""
    lam, V = jacobi_eigen(S)
    scale = max(abs(l) for l in lam)
    for l in lam:
        if l < -1e-9 * scale:
            raise ValueError('conditional covariance has a genuinely negative eigenvalue: %r' % l)
    root = [sqrt(max(l, 0.0)) for l in lam]
    n = len(S)
    return [[sum(V[i][k] * root[k] * V[j][k] for k in range(n)) for j in range(n)] for i in range(n)]


def solve_spd(S, B):
    """Solve S X = B (S symmetric positive definite, B a list of columns) by Cholesky."""
    L = cholesky(S)
    n = len(S)
    out = []
    for col in B:
        y = [0.0] * n
        for i in range(n):
            y[i] = (col[i] - sum(L[i][k] * y[k] for k in range(i))) / L[i][i]
        x = [0.0] * n
        for i in reversed(range(n)):
            x[i] = (y[i] - sum(L[k][i] * x[k] for k in range(i + 1, n))) / L[i][i]
        out.append(x)
    return out


def finite_r_normalizer(d, r, b, k, n, seed):
    """Monte Carlo E_Q[F_d(H_M) F_(d-1)(H_S)] / r^2 under the endpoint regression Q_r (pins f, grad f at M and S),
    compared with 36 k^2 m_(d,b) = lim Z_r / r^2 (Lemma 2 of PROOF.md)."""
    M = [-r / 2] + [0.0] * (d - 1)
    S = [r / 2] + [0.0] * (d - 1)
    zero = (0,) * d
    obs = [(zero, M)] + [(unit(d, i), M) for i in range(d)] + [(zero, S)] + [(unit(d, i), S) for i in range(d)]
    vals = [b] + [0.0] * d + [b - k * r ** 3] + [0.0] * d
    pairs = [(i, j) for i in range(d) for j in range(i, d)]
    targets = [(add(unit(d, i), unit(d, j)), M) for i, j in pairs] + [(add(unit(d, i), unit(d, j)), S) for i, j in pairs]
    Soo = [[cov_two_point(a, s, c, t) for (c, t) in obs] for (a, s) in obs]
    Sto = [[cov_two_point(a, s, c, t) for (c, t) in obs] for (a, s) in targets]
    Stt = [[cov_two_point(a, s, c, t) for (c, t) in targets] for (a, s) in targets]
    W = solve_spd(Soo, Sto)                       # W[i] = Soo^{-1} Sto[i]
    mean = [sum(W[i][j] * vals[j] for j in range(len(obs))) for i in range(len(targets))]
    cc = [[Stt[i][j] - sum(W[i][l] * Sto[j][l] for l in range(len(obs))) for j in range(len(targets))] for i in range(len(targets))]
    # the conditional covariance is nearly singular at small r (f_xx at the two pins is pinned to O(r^2) precision),
    # so sample through a symmetric square root with the tiny negative rounding eigenvalues clipped to zero
    L = sym_sqrt(cc)
    rng = random.Random(seed)
    nt = len(targets)
    acc = acc2 = 0.0
    for _ in range(n):
        z = [rng.gauss(0, 1) for _ in range(nt)]
        x = [mean[i] + sum(L[i][j] * z[j] for j in range(nt)) for i in range(nt)]
        HM = [[0.0] * d for _ in range(d)]
        HS = [[0.0] * d for _ in range(d)]
        for idx, (i, j) in enumerate(pairs):
            HM[i][j] = HM[j][i] = x[idx]
            HS[i][j] = HS[j][i] = x[len(pairs) + idx]
        v = abs(det(HM)) * abs(det(HS)) if (n_negative(HM) == d and n_negative(HS) == d - 1) else 0.0
        acc += v
        acc2 += v * v
    mu = acc / n
    return {'d': d, 'r': r, 'b': b, 'k': k, 'Z_r_over_r2': mu / r ** 2, 'se': sqrt(max(acc2 / n - mu * mu, 0.0) / n) / r ** 2,
            'limit_36k2_m_d': 36 * k * k * m_d(d, b), 'samples': n}


# ----------------------------------------------------------------------------- assembly with Math-#168's planar values
def planar_values():
    path = os.path.join(HERE, '..', 'c6_cluster_coefficients_numerics_20260930', 'RESULTS.json')
    with open(path) as fh:
        ref = json.load(fh)
    return ref['prefactor']


def assemble(table):
    pre = planar_values()
    out = {}
    for key, row in pre.items():
        kstr, bstr = key.split(',')
        b = float(bstr.split('=')[1])
        for d in DIMS:
            R = table['R_d']['d=%d' % d]['b=%s' % b]
            out['%s,d=%d' % (key, d)] = {'a1': R * row['alpha1_gh60'], 'a2': R * row['alpha2_gh60'],
                                         'a1_plus_a2': R * (row['alpha1_gh60'] + row['alpha2_gh60']),
                                         'a2_over_a1': row['alpha2_gh60'] / row['alpha1_gh60'], 'R_d': R,
                                         'z0_d': 36 * float(Fr(kstr.split('=')[1])) ** 2 * m_d(d, b),
                                         'planar_source': 'Math-#168 RESULTS.json prefactor/%s (GH60, not certified)' % key}
    return out


def full_run(fast=False):
    res = {'schema': 1, 'object': 'CL-C6-HARD-DIRECTION-FACTORIZATION-20260930-v1', 'scientific_effect': 'NONE', 'certified': False,
           'kernel': 'exp(-|x|^2/2), continuum (torus images neglected; see PROOF.md section 6)', 'mutant': MUT,
           'python_requirement': '>= 3.11'}
    res['lemma_one'] = {'d=%d' % d: lemma_one(d) for d in (2, 3, 4, 5)}
    res['c_m'] = {'m=%d' % m: c_m(m) for m in (1, 2, 3, 4)}
    res['closed_forms'] = closed_forms()
    tab = {'N_d': {}, 'm_d': {}, 'R_d': {}, 'normalization': {}, 'm_2': {'b=%s' % b: m2(b) for b in BS}}
    for d in DIMS:
        for key in ('N_d', 'm_d', 'R_d', 'normalization'):
            tab[key].setdefault('d=%d' % d, {})
        for b in BS:
            tab['N_d']['d=%d' % d]['b=%s' % b] = N_d(d, b)
            tab['m_d']['d=%d' % d]['b=%s' % b] = m_d(d, b)
            tab['R_d']['d=%d' % d]['b=%s' % b] = R_d(d, b)
            tab['normalization']['d=%d' % d]['b=%s' % b] = normalization(d, b)
    res['table'] = tab
    res['quadrature_orders'] = {'d=%d,b=0.0' % d: {'n=%d' % n: {'N_d': N_d(d, 0.0, n), 'm_d': m_d(d, 0.0, n)} for n in ((30, 40, 50) if d == 5 else (40, 60, 80))} for d in (3, 4, 5)}
    nmc = 20000 if fast else 200000
    res['monte_carlo'] = {'m_d': {'d=%d,b=%s' % (d, b): mc_m_d(d, b, nmc if d < 5 else nmc // 2, 100 + d) for d in (3, 4, 5) for b in BS},
                          'N_3': {'b=%s' % b: mc_N_3(b, 5 * nmc, 200) for b in BS}}
    nz = 4000 if fast else 400000
    res['finite_r_normalizer'] = {'d=%d,r=%s,b=%s' % (d, r, b): finite_r_normalizer(d, r, b, 1.0, nz, 300 + int(100 * r))
                                  for d in (2, 3) for r in (0.1, 0.05) for b in BS}
    res['assembled_near_coefficients'] = assemble(res['table'])
    return res


def check_run():
    for d in (2, 3, 4, 5):
        lemma_one(d)
    cf = closed_forms()
    require(abs(c_m(1) - 1) < 1e-14 and abs(c_m(2) - pi) < 1e-13, 'c_1 = 1, c_2 = pi')
    require(abs(m2(0.0) - 1) < 1e-14 and abs(m2(1.0) - 2.7201411062) < 1e-9, 'm_(2,0) = 1, m_(2,1) = 2.72014')
    require(abs(N_d(3, 0.0) - cf['N_3_0']) < 1e-10, 'N_3(0) = 2 sqrt2')
    require(abs(m_d(3, 0.0) - cf['m_3_0']) < 1e-10, 'm_(3,0) = (7 - 4 sqrt2)/2')
    require(abs(R_d(3, 0.0) - cf['R_3_0']) < 1e-9, 'R_3(0) = (32 + 28 sqrt2)/17')
    require(abs(R_d(2, 0.0) - 1) < 1e-12 and abs(R_d(2, 1.0) - 1) < 1e-12, 'R_2 = 1 (planar case reproduces itself)')
    for d in DIMS:
        for b in BS:
            # the full-line normalization integral is the least well resolved piece at order 40 in four dimensions
            tol = 1e-5 if d >= 5 else 1e-9
            require(abs(normalization(d, b) - 1) < tol, 'eigenvalue density normalizes to 1 (d=%d, b=%s)' % (d, b))
    require(N_d(4, 0.0) > N_d(3, 0.0) and m_d(4, 0.0) < m_d(3, 0.0), 'monotonicity sanity d = 3 -> 4 at b = 0')
    path = os.path.join(HERE, 'RESULTS.json')
    require(os.path.exists(path), 'RESULTS.json present')
    with open(path) as fh:
        ref = json.load(fh)
    for d in DIMS:
        for b in BS:
            for key, fn in (('N_d', N_d), ('m_d', m_d), ('R_d', R_d)):
                want = ref['table'][key]['d=%d' % d]['b=%s' % b]
                require(abs(fn(d, b) - want) <= REPLAY_TOL * max(abs(want), 1.0), 'replay %s d=%d b=%s' % (key, d, b))
    for key, row in ref['monte_carlo']['m_d'].items():
        d = int(key.split(',')[0][2:])
        b = float(key.split('=')[-1])
        require(abs(row['value'] - m_d(d, b)) <= 4 * row['se'] + 1e-12, 'Monte Carlo m_d within 4 s.e. (%s)' % key)
    for key, row in ref['monte_carlo']['N_3'].items():
        b = float(key.split('=')[-1])
        require(abs(row['value'] - N_d(3, b)) <= 4 * row['se'] + 0.02 * N_d(3, b), 'Monte Carlo N_3 within 4 s.e. + 2%% bin bias (%s)' % key)
    for key, row in ref['finite_r_normalizer'].items():
        require(abs(row['Z_r_over_r2'] - row['limit_36k2_m_d']) <= 4 * row['se'] + 0.15 * row['r'] * row['limit_36k2_m_d'] + 1e-9,
                'finite-r normalizer within 4 s.e. + O(r) of 36 k^2 m_d (%s)' % key)
    for key, row in ref['assembled_near_coefficients'].items():
        d = int(key.split('d=')[1])
        b = float(key.split('b=')[1].split(',')[0])
        require(abs(row['R_d'] - R_d(d, b)) <= REPLAY_TOL * row['R_d'], 'assembled R_d replay (%s)' % key)
    print(json.dumps({'check': 'ok', 'R_3_0': R_d(3, 0.0), 'closed_form': cf['R_3_0'], 'mutant': MUT}))


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--fast', action='store_true', help='fewer Monte Carlo samples (development only)')
    ap.add_argument('--mutant', choices=MUTANTS)
    args = ap.parse_args()
    MUT = args.mutant
    if args.check:
        check_run()
        return
    res = full_run(fast=args.fast)
    with open(os.path.join(HERE, 'RESULTS.json'), 'w') as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print('wrote RESULTS.json')


if __name__ == '__main__':
    main()
