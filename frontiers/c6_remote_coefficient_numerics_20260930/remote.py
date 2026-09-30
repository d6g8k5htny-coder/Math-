#!/usr/bin/env python3
"""Numerical evaluation of the remote contact kernel Lambda_j(x; b, k, u) of [RM] (13) for the
parent kernel K(z) = exp(-|z|^2/2) (and its L-periodization) in the plane d = 2, together with
its far-field value, the correlation-hole constant and the torus integral k * integral_X Lambda dx
that enters nu(1) = nu_near(1) + k integral_X Lambda ([CL] (1.4)).

Standard library only.  Deterministic nested Gauss quadrature; no random numbers except in the
optional Monte Carlo cross-check (fixed seed).  Nothing here is a proof or an enclosure.

    python -B -S remote.py            # full run, writes RESULTS.json (long: tens of minutes)
    python -B -S remote.py --check    # exact controls + replay of a small subset against RESULTS.json
    python -B -S remote.py --check --mutant NAME   # must exit 1

Conventions.  Coordinates x = (x1, z): x1 along the pin axis u, z transverse.  Jets are indexed by
derivative orders (a, c) = d^a/dx1^a d^c/dz^c.  Cov(d^alpha f(s), d^beta f(t)) = (-1)^|alpha|
(d^(alpha+beta) K)(t - s).  Contact observation U_0 = (f, f_x, f_z, f_xx, f_xz, f_xxx)(0) =
(b, 0, 0, 0, 0, 12k); A_0 = f_zz(0); Y_x = (f_x, f_z, f)(x) = (0, 0, b); H_x = (f_xx, f_xz, f_zz)(x).
w_0 = 36 k^2 A_0^2 1{A_0 < 0}; z_0 = E[w_0 | U_0] = 36 k^2 m_(2,b).
Lambda_j(x) = p_(Y_x | U_0)(0, 0, b) * E[w_0 F_j(H_x) | U_0, Y_x] / z_0,  F_j(H) = |det H| 1{index j}.
"""
import argparse
import json
import math
import os
import random
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50

HERE = os.path.dirname(os.path.abspath(__file__))
MUTANTS = ('hermite-sign', 'det-abs', 'weight-indicator')
MUT = None

SITE0 = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2), (3, 0)]   # f, f_x, f_z, f_xx, f_xz, f_zz, f_xxx at 0
SITEX = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]           # f, f_x, f_z, f_xx, f_xz, f_zz at x
OBS0 = [0, 1, 2, 3, 4, 6]        # U_0 within the 13-vector
OBSX = [8, 9, 7]                 # Y_x = (f_x, f_z, f)(x)
TARGETS = [5, 10, 11, 12]        # A_0 = f_zz(0), h1 = f_xx(x), h2 = f_xz(x), h3 = f_zz(x)


def require(cond, msg):
    if not cond:
        print('FAIL: ' + msg)
        sys.exit(1)


# ----------------------------------------------------------------------------- Hermite / kernel
def hermite(n, t):
    """Probabilists' Hermite polynomial He_n(t):  (d/dt)^n exp(-t^2/2) = (-1)^n He_n(t) exp(-t^2/2)."""
    h0, h1 = 1, t
    if n == 0:
        return h0
    for m in range(1, n):
        h0, h1 = h1, t * h1 - m * h0
    return h1


def _exp(t):
    return t.exp() if isinstance(t, Decimal) else math.exp(t)


def _sqrt(t):
    return t.sqrt() if isinstance(t, Decimal) else math.sqrt(t)


def _log(t):
    return t.ln() if isinstance(t, Decimal) else math.log(t)


def kernel_derivative(a, c, x1, z, L=None, images=2):
    """(d^a/dx1^a d^c/dz^c) K_L(x1, z) for K(z) = exp(-|z|^2/2), K_L its normalized L-periodization.
    L = None: continuum kernel (single image).  Works in float or Decimal arithmetic (type of x1)."""
    if L is None:
        return (-1) ** (a + c) * hermite(a, x1) * hermite(c, z) * _exp(-(x1 * x1 + z * z) / 2)
    tot = 0 * x1
    norm = 0 * x1
    for m1 in range(-images, images + 1):
        for m2 in range(-images, images + 1):
            s1, s2 = x1 + L * m1, z + L * m2
            tot += (-1) ** (a + c) * hermite(a, s1) * hermite(c, s2) * _exp(-(s1 * s1 + s2 * s2) / 2)
            norm += _exp(-(L * L) * (m1 * m1 + m2 * m2) / 2 + 0 * x1)
    return tot / norm


def cov_entry(alpha, beta, dx1, dz, L=None):
    """Cov(d^alpha f(s), d^beta f(t)) with t - s = (dx1, dz)."""
    sign = (-1) ** (alpha[0] + alpha[1])
    if MUT == 'hermite-sign':
        sign = (-1) ** (beta[0] + beta[1])
    return sign * kernel_derivative(alpha[0] + beta[0], alpha[1] + beta[1], dx1, dz, L)


def joint_covariance(x1, z, L=None):
    """13 x 13 covariance of the two-site jet vector (SITE0 at 0, SITEX at x); float or Decimal."""
    jets = [(0, a) for a in SITE0] + [(1, a) for a in SITEX]
    n = len(jets)
    zero = 0 * x1
    if L is not None and isinstance(x1, Decimal):
        L = Decimal(L)
    C = [[zero] * n for _ in range(n)]
    for i in range(n):
        si, ai = jets[i]
        for j in range(n):
            sj, aj = jets[j]
            d1 = (x1 if sj == 1 else zero) - (x1 if si == 1 else zero)
            d2 = (z if sj == 1 else zero) - (z if si == 1 else zero)
            C[i][j] = cov_entry(ai, aj, d1, d2, L)
    return C


# ----------------------------------------------------------------------------- exact one-site table
def hermite_zero_exact(n):
    """He_n(0) exactly: 0 for odd n, (-1)^(n/2) (n-1)!! for even n."""
    if n % 2:
        return Fraction(0)
    v = Fraction(1)
    for m in range(1, n, 2):
        v *= m
    return v * (-1) ** (n // 2)


def exact_one_site_cov(alpha, beta):
    return (-1) ** (alpha[0] + alpha[1]) * hermite_zero_exact(alpha[0] + beta[0]) * hermite_zero_exact(alpha[1] + beta[1])


# ----------------------------------------------------------------------------- linear algebra
def cholesky(A):
    n = len(A)
    zero = 0 * A[0][0]
    Lm = [[zero] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = A[i][j] - sum((Lm[i][k] * Lm[j][k] for k in range(j)), zero)
            if i == j:
                if s <= 0:
                    raise ValueError('matrix not positive definite (pivot %r at %d)' % (s, i))
                Lm[i][j] = _sqrt(s)
            else:
                Lm[i][j] = s / Lm[j][j]
    return Lm


def chol_solve(Lm, b):
    n = len(Lm)
    zero = 0 * Lm[0][0]
    y = [zero] * n
    for i in range(n):
        y[i] = (b[i] - sum((Lm[i][k] * y[k] for k in range(i)), zero)) / Lm[i][i]
    x = [zero] * n
    for i in reversed(range(n)):
        x[i] = (y[i] - sum((Lm[k][i] * x[k] for k in range(i + 1, n)), zero)) / Lm[i][i]
    return x


def submatrix(C, rows, cols):
    return [[C[i][j] for j in cols] for i in rows]


def condition(C, obs, values, targets):
    """Gaussian regression: law of C[targets] given C[obs] = values (zero prior means).
    Returns (mean, cov, obs_logdensity_at_values)."""
    Coo = submatrix(C, obs, obs)
    zero = 0 * C[0][0]
    values = [v + zero for v in values]
    Lm = cholesky(Coo)
    alpha = chol_solve(Lm, values)
    logdet = 2 * sum((_log(Lm[i][i]) for i in range(len(obs))), zero)
    quad = sum((values[i] * alpha[i] for i in range(len(obs))), zero)
    logdens = float(-quad / 2 - logdet / 2) - 0.5 * len(obs) * math.log(2 * math.pi)
    mean = []
    cov = []
    Cto = submatrix(C, targets, obs)
    for r, t in enumerate(targets):
        mean.append(sum((Cto[r][i] * alpha[i] for i in range(len(obs))), zero))
    solved = [chol_solve(Lm, Cto[r]) for r in range(len(targets))]
    for r, t in enumerate(targets):
        row = []
        for s, u in enumerate(targets):
            row.append(C[t][u] - sum((Cto[r][i] * solved[s][i] for i in range(len(obs))), zero))
        cov.append(row)
    return mean, cov, logdens


# ----------------------------------------------------------------------------- quadrature rules
def gauss_legendre(n):
    nodes, weights = [], []
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
        p0, p1 = 1.0, x
        for m in range(2, n + 1):
            p0, p1 = p1, ((2 * m - 1) * x * p1 - (m - 1) * p0) / m
        dp = n * (x * p1 - p0) / (x * x - 1.0)
        nodes.append(x)
        weights.append(2.0 / ((1.0 - x * x) * dp * dp))
    return nodes, weights


def gauss_hermite(n):  # retained for the Monte Carlo-free control of the normalization; unused in the main integral
    """Probabilists' Gauss-Hermite: sum w_i g(t_i) ~ E g(T), T ~ N(0, 1)."""
    nodes, weights = [], []
    for i in range(1, n + 1):
        if i == 1:
            x = math.sqrt(2 * n + 1) - 1.85575 * (2 * n + 1) ** (-1.0 / 6.0)
        elif i == 2:
            x = nodes[-1] - 1.14 * n ** 0.426 / nodes[-1]
        elif i == 3:
            x = 1.86 * nodes[-1] - 0.86 * nodes[0]
        elif i == 4:
            x = 1.91 * nodes[-1] - 0.91 * nodes[-2]
        else:
            x = 2.0 * nodes[-1] - nodes[-2]
        for _ in range(200):
            h0, h1 = 1.0, x
            for m in range(1, n):
                h0, h1 = h1, x * h1 - m * h0
            dh = n * h0
            dx = h1 / dh
            x -= dx
            if abs(dx) < 1e-14:
                break
        h0, h1 = 1.0, x
        for m in range(1, n):
            h0, h1 = h1, x * h1 - m * h0
        nodes.append(x)
        weights.append(math.factorial(n) / (n * n * h0 * h0))
    return nodes, weights


SQRT2PI = math.sqrt(2 * math.pi)


def phi(t):
    return math.exp(-t * t / 2) / SQRT2PI


def Phi(t):
    return 0.5 * math.erfc(-t / math.sqrt(2))


def m2_negative(m, s):
    """E[A^2 1{A < 0}] for A ~ N(m, s^2)."""
    if MUT == 'weight-indicator':
        return m * m + s * s
    if s <= 0.0:
        return m * m if m < 0 else 0.0
    t = m / s
    return (m * m + s * s) * Phi(-t) - m * s * phi(t)


class Rules:
    """Quadrature orders: n_a Gauss-Legendre nodes on each side of a = 0, n_theta trapezoid nodes on the circle,
    n_rho Gauss-Legendre nodes on each of [0, |a|] and [|a|, rho_max]; Gaussian ranges cut at cut standard deviations."""

    def __init__(self, n_a=24, n_theta=32, n_rho=24, cut=9.0):
        self.gl_a = gauss_legendre(n_a)
        self.n_theta = n_theta
        self.gl_rho = gauss_legendre(n_rho)
        self.cut = cut
        self.orders = [n_a, n_theta, n_rho]


def weighted_determinant_integrals(mu, S, rules):
    """(A, h1, h2, h3) ~ N(mu, S).  Returns dict with
       G[j] = E[ A^2 1{A<0} |det H| 1{index H = j} ],   F[j] = E[ |det H| 1{index H = j} ],   D = E det H (control).
    Coordinates: a = (h1 + h3)/2, c = (h1 - h3)/2, so det H = a^2 - c^2 - h2^2 = a^2 - rho^2 with (c, h2) =
    rho (cos theta, sin theta).  The cone det H = 0 is the coordinate surface rho = |a|; the a-range is split at 0
    (index by the sign of the trace) and the rho-range at |a|, so every piece of the integrand is smooth and the
    nested Gauss-Legendre / trapezoid rule converges geometrically.  The general (non-isotropic) Gaussian density
    of (a, c, h2) is evaluated directly at the nodes; A is integrated out in closed form through m2_negative."""
    # linear map (h1, h2, h3) -> w = (a, c, h2)
    T = [[0.5, 0.0, 0.5], [0.5, 0.0, -0.5], [0.0, 1.0, 0.0]]
    SHH = [[S[i][j] for j in (1, 2, 3)] for i in (1, 2, 3)]
    muH = [mu[1], mu[2], mu[3]]
    muw = [sum(T[i][k] * muH[k] for k in range(3)) for i in range(3)]
    TS = [[sum(T[i][k] * SHH[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    Sw = [[sum(TS[i][k] * T[j][k] for k in range(3)) for j in range(3)] for i in range(3)]
    Lw = cholesky(Sw)
    logdet = 2.0 * sum(math.log(Lw[i][i]) for i in range(3))
    norm = math.exp(-0.5 * logdet) / (2 * math.pi) ** 1.5
    # A | w regression: A = muA + wA . (w - muw), residual sd sA
    SAH = [S[0][j] for j in (1, 2, 3)]
    SAw = [sum(T[i][k] * SAH[k] for k in range(3)) for i in range(3)]
    wA = chol_solve(Lw, SAw)
    sA = math.sqrt(max(S[0][0] - sum(SAw[i] * wA[i] for i in range(3)), 0.0))
    muA = mu[0]
    # inverse via Cholesky for the quadratic form
    Linv = [[0.0] * 3 for _ in range(3)]
    for j in range(3):
        e = [1.0 if i == j else 0.0 for i in range(3)]
        col = chol_solve(Lw, e)
        for i in range(3):
            Linv[i][j] = col[i]
    P = Linv  # S_w^{-1}
    cut = rules.cut
    sa = math.sqrt(Sw[0][0])
    sc, s2 = math.sqrt(Sw[1][1]), math.sqrt(Sw[2][2])
    rho_max = math.hypot(muw[1], muw[2]) + cut * max(sc, s2)
    G = [0.0, 0.0, 0.0]
    F = [0.0, 0.0, 0.0]
    # theta nodes: periodic trapezoid rule in u, theta = theta0 + u - beta sin u, concentrated at the angular
    # position theta0 of the (c, h2) mean when the Gaussian is offset and narrow (analytic periodic map: the
    # trapezoid rule keeps its geometric convergence; the Jacobian 1 - beta cos u is included in the weights)
    rmu = math.hypot(muw[1], muw[2])
    smax = max(sc, s2)
    width = min(1.0, smax / max(rmu, 1e-300))
    beta = max(0.0, 1.0 - rules.n_theta * width / (8 * math.pi))
    theta0 = math.atan2(muw[2], muw[1]) if rmu > 0 else 0.0
    cs = []
    for i in range(rules.n_theta):
        u = -math.pi + 2 * math.pi * (i + 0.5) / rules.n_theta
        th = theta0 + u - beta * math.sin(u)
        cs.append((math.cos(th), math.sin(th), 1.0 - beta * math.cos(u)))
    wtheta = 2 * math.pi / rules.n_theta
    a_lo, a_hi = muw[0] - cut * sa, muw[0] + cut * sa
    for lo, hi in ((a_lo, min(0.0, a_hi)), (max(0.0, a_lo), a_hi)):
        if hi <= lo:
            continue
        mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
        for ta, wa in zip(*rules.gl_a):
            a = mid + half * ta
            wt_a = wa * half
            aa = abs(a)
            jpos = 0 if a > 0 else 2      # det > 0: sign of the trace decides minimum (0) / maximum (2)
            segs = []
            if aa < rho_max:
                segs.append((0.0, aa, jpos))
                segs.append((aa, rho_max, 1))
            else:
                segs.append((0.0, rho_max, jpos))
            da = a - muw[0]
            for lo_r, hi_r, j in segs:
                if hi_r <= lo_r:
                    continue
                mid_r, half_r = 0.5 * (lo_r + hi_r), 0.5 * (hi_r - lo_r)
                accG = accF = 0.0
                for tr, wr in zip(*rules.gl_rho):
                    rho = mid_r + half_r * tr
                    adet = a * a - rho * rho
                    if MUT != 'det-abs':
                        adet = abs(adet)
                    base = wr * rho * adet
                    for cth, sth, jac in cs:
                        c = rho * cth
                        h2 = rho * sth
                        dc = c - muw[1]
                        d2 = h2 - muw[2]
                        q = (P[0][0] * da * da + P[1][1] * dc * dc + P[2][2] * d2 * d2
                             + 2 * (P[0][1] * da * dc + P[0][2] * da * d2 + P[1][2] * dc * d2))
                        if q > 2 * cut * cut:
                            continue
                        dens = math.exp(-0.5 * q) * jac
                        mA = muA + wA[0] * da + wA[1] * dc + wA[2] * d2
                        accF += base * dens
                        accG += base * dens * m2_negative(mA, sA)
                G[j] += wt_a * half_r * accG
                F[j] += wt_a * half_r * accF
    scale = norm * wtheta
    G = [g * scale for g in G]
    F = [f * scale for f in F]
    D = (muw[0] ** 2 + Sw[0][0]) - (muw[1] ** 2 + Sw[1][1]) - (muw[2] ** 2 + Sw[2][2])
    return {'G': G, 'F': F, 'D': D}


# ----------------------------------------------------------------------------- Lambda
def m2b(b):
    return m2_negative(-b, math.sqrt(2.0))


def _conditioning(x1, z, b, k, L, exact):
    """Density of Y_x at (0, 0, b) given U_0 (log) and the conditional law (mu, S) of (A_0, H_x) given
    U_0 and Y_x.  exact = True recomputes the Gaussian regression in 50-digit decimal arithmetic (used
    automatically where the double-precision regression loses positivity; the near-axis points, where
    Lambda is exponentially small)."""
    if exact:
        x1, z, bb, kk = Decimal(repr(x1)), Decimal(repr(z)), Decimal(repr(b)), Decimal(repr(k))
    else:
        bb, kk = b, k
    C = joint_covariance(x1, z, L)
    u0 = [bb, 0 * bb, 0 * bb, 0 * bb, 0 * bb, 12 * kk]
    meanY, covY, _ = condition(C, OBS0, u0, OBSX)
    LY = cholesky(covY)
    dev = [0 - meanY[0], 0 - meanY[1], bb - meanY[2]]
    a = chol_solve(LY, dev)
    logp = float(-sum((dev[i] * a[i] for i in range(3)), 0 * bb) / 2 - sum((_log(LY[i][i]) for i in range(3)), 0 * bb)) - 1.5 * math.log(2 * math.pi)
    obs = OBS0 + OBSX
    vals = u0 + [0 * bb, 0 * bb, bb]
    mu, S, _ = condition(C, obs, vals, TARGETS)
    mu = [float(v) for v in mu]
    S = [[float(v) for v in row] for row in S]
    # positivity of the (h1, h2, h3) block is needed by the quadrature
    cholesky([[S[i][j] for j in (1, 2, 3)] for i in (1, 2, 3)])
    return logp, mu, S


def lambda_at(x1, z, b, k, rules, L=None):
    """Returns dict: Lambda_j (j = 0, 1, 2), Lambda (sum), the unweighted remote density rho_j =
    p * E[F_j | obs] (what the same point would carry without the pin weight), logp, coupling."""
    try:
        logp, mu, S = _conditioning(x1, z, b, k, L, False)
        exact = False
    except ValueError:
        logp, mu, S = _conditioning(x1, z, b, k, L, True)
        exact = True
        EXACT_COUNT[0] += 1
    p = math.exp(logp)
    W = weighted_determinant_integrals(mu, S, rules)
    mm = m2b(b)
    lam = [p * W['G'][j] / mm for j in range(3)]
    rho = [p * W['F'][j] for j in range(3)]
    fsum = W['F'][0] + W['F'][1] + W['F'][2]
    coupling = (W['G'][0] + W['G'][1] + W['G'][2]) / (mm * fsum) if fsum > 0 else None
    return {'lambda_j': lam, 'lambda': sum(lam), 'rho_j': rho, 'rho': sum(rho), 'logp': logp, 'exact_regression': exact,
            'coupling': coupling}


def lambda_far(b, rules):
    """Far-field value: p = phi(b)/(2 pi), H | (f = b, grad f = 0): h1, h3 ~ N(-b, 2) independent,
    h2 ~ N(0, 1); A_0 independent of H.  Lambda_inf,j = phi(b)/(2 pi) E[F_j(H)]."""
    mu = [-b, -b, 0.0, -b]
    S = [[2.0, 0.0, 0.0, 0.0], [0.0, 2.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 2.0]]
    W = weighted_determinant_integrals(mu, S, rules)
    p = phi(b) / (2 * math.pi)
    lam = [p * W['G'][j] / m2b(b) for j in range(3)]
    return {'lambda_j': lam, 'lambda': sum(lam), 'rho_j': [p * W['F'][j] for j in range(3)], 'E_F_j': W['F']}


def unconditional_hessian_controls(rules):
    """H unconditional: Var f_xx = Var f_zz = 3, Cov = 1, Var f_xz = 1.  With h1 = a + c, h3 = a - c
    (a ~ N(0, 2), c ~ N(0, 1) independent) det H = a^2 - (c^2 + h2^2) = a^2 - rho^2 with rho^2 ~ Exp(mean 2),
    so E|det H| = 2 E[(rho^2 - a^2)_+] = 4 E exp(-a^2/2) = 4/sqrt3, E F_1 = 2/sqrt3, E F_0 = E F_2 = 1/sqrt3,
    E det H = 0.  Total critical density 2/(pi sqrt3), maxima 1/(2 pi sqrt3) (Longuet-Higgins)."""
    mu = [0.0, 0.0, 0.0, 0.0]
    S = [[2.0, 0.0, 0.0, 0.0], [0.0, 3.0, 0.0, 1.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 3.0]]
    W = weighted_determinant_integrals(mu, S, rules)
    return {'E_absdet': sum(W['F']), 'E_F_j': W['F'], 'E_det': W['D']}


def mc_absdet(n, seed=2026):
    """Monte Carlo cross-check of E|det H| for the unconditional Hessian (fixed seed)."""
    rng = random.Random(seed)
    acc = acc2 = 0.0
    for _ in range(n):
        g1, g2, g3 = rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)
        h1 = math.sqrt(2.0) * g1 + g3          # Var 3
        h3 = math.sqrt(2.0) * g2 + g3          # Var 3, Cov(h1, h3) = 1
        h2 = rng.gauss(0, 1)
        v = abs(h1 * h3 - h2 * h2)
        acc += v
        acc2 += v * v
    mean = acc / n
    var = acc2 / n - mean * mean
    return mean, math.sqrt(var / n)


# ----------------------------------------------------------------------------- grids
def hole_integral(b, k, rules, Rc=5.0, h=0.2, lam_inf=None):
    """2 * sum over the midpoint grid on [-Rc, Rc] x (0, Rc] of (Lambda(x) - Lambda_inf) h^2, by index.
    Continuum kernel."""
    n1 = int(round(2 * Rc / h))
    n2 = int(round(Rc / h))
    tot = [0.0, 0.0, 0.0]
    tot_rho = [0.0, 0.0, 0.0]
    minlam, maxlam = float('inf'), float('-inf')
    for i in range(n1):
        x1 = -Rc + (i + 0.5) * h
        for j in range(n2):
            z = (j + 0.5) * h
            r = lambda_at(x1, z, b, k, rules)
            for q in range(3):
                tot[q] += r['lambda_j'][q] - lam_inf['lambda_j'][q]
                tot_rho[q] += r['rho_j'][q] - lam_inf['rho_j'][q]
            minlam = min(minlam, r['lambda'])
            maxlam = max(maxlam, r['lambda'])
    scale = 2.0 * h * h
    return {'hole_j': [scale * t for t in tot], 'hole': scale * sum(tot),
            'hole_unweighted_j': [scale * t for t in tot_rho], 'hole_unweighted': scale * sum(tot_rho),
            'grid': {'Rc': Rc, 'h': h, 'points': n1 * n2, 'symmetry': 'z -> -z'},
            'lambda_min_on_grid': minlam, 'lambda_max_on_grid': maxlam}


def torus_integral(b, k, rules, L, h=0.2):
    """integral over the fundamental domain [-L/2, L/2]^2 of Lambda_L(x) dx (periodized kernel), by index."""
    n1 = int(round(L / h))
    n2 = int(round(L / (2 * h)))
    tot = [0.0, 0.0, 0.0]
    for i in range(n1):
        x1 = -L / 2 + (i + 0.5) * h
        for j in range(n2):
            z = (j + 0.5) * h
            r = lambda_at(x1, z, b, k, rules, L)
            for q in range(3):
                tot[q] += r['lambda_j'][q]
    scale = 2.0 * h * h
    return {'integral_j': [scale * t for t in tot], 'integral': scale * sum(tot),
            'grid': {'L': L, 'h': h, 'points': n1 * n2, 'symmetry': 'z -> -z'}}


# ----------------------------------------------------------------------------- controls
EXACT_COUNT = [0]
SAMPLE_POINTS = [(0.15, 0.15), (0.5, 0.3), (-0.7, 0.9), (1.0, 0.0), (0.0, 1.0), (2.0, 1.5), (-1.5, 0.5), (3.0, 3.0)]


def controls(rules):
    out = {}
    # (a) exact one-site Hermite table versus the floating kernel derivatives at 0 (continuum and L = 24, 12)
    table = {}
    maxdev = {'continuum': 0.0, 'L24': 0.0, 'L12': 0.0, 'L6': 0.0}
    for a in SITE0:
        for c in SITE0:
            ex = exact_one_site_cov(a, c)
            table['%d%d,%d%d' % (a + c)] = str(ex)
            fl = cov_entry(a, c, 0.0, 0.0)
            maxdev['continuum'] = max(maxdev['continuum'], abs(fl - float(ex)))
            for L, key in ((24.0, 'L24'), (12.0, 'L12'), (6.0, 'L6')):
                maxdev[key] = max(maxdev[key], abs(cov_entry(a, c, 0.0, 0.0, L) - float(ex)))
    require(table['20,20'] == '3' and table['30,30'] == '15' and table['10,30'] == '-3' and table['00,20'] == '-1'
            and table['20,02'] == '1' and table['11,11'] == '1' and table['00,00'] == '1', 'exact Hermite one-site table')
    require(maxdev['continuum'] < 1e-12 and maxdev['L24'] < 1e-9 and maxdev['L12'] < 1e-9, 'lattice one-site covariances at L = 24, 12')
    require(1e-4 < maxdev['L6'] < 2e-3, 'L = 6 one-site deviation is of the expected size')
    out['one_site_exact'] = {'Var_fxx': table['20,20'], 'Var_fxxx': table['30,30'], 'Cov_fx_fxxx': table['10,30'],
                             'Cov_f_fxx': table['00,20'], 'Cov_fxx_fzz': table['20,02'], 'Var_fxz': table['11,11']}
    out['one_site_lattice_max_dev'] = maxdev
    # (b) unconditional Hessian: E|det H| = sqrt3, E F_2 = sqrt3/4, E F_1 = sqrt3/2, E det = 0
    U = unconditional_hessian_controls(rules)
    require(abs(U['E_absdet'] - 4 / math.sqrt(3)) < 1e-9, 'E|det H| = 4/sqrt(3) (exact: a^2 - rho^2 decomposition)')
    require(abs(U['E_F_j'][2] - 1 / math.sqrt(3)) < 1e-9 and abs(U['E_F_j'][0] - 1 / math.sqrt(3)) < 1e-9
            and abs(U['E_F_j'][1] - 2 / math.sqrt(3)) < 1e-9, 'index split 1/sqrt3, 2/sqrt3, 1/sqrt3')
    require(abs(U['E_det']) < 1e-12, 'E det H = 0 (Euler characteristic of the torus)')
    out['unconditional_hessian'] = U
    # (c) far field: E[w_0 | U_0] / z_0 = 1 and Lambda_inf = phi(b) E|det H_b| / (2 pi)
    far = {}
    for b in (0.0, 1.0):
        r = lambda_far(b, rules)
        far[str(b)] = r
        rr = lambda_at(8.0, 0.0, b, 1.0, rules)
        require(abs(rr['lambda'] - r['lambda']) < 1e-9 * r['lambda'], 'Lambda(8, 0) equals the far-field value, b = %r' % b)
        require(abs(rr['coupling'] - 1.0) < 1e-9, 'pin weight decouples at |x| = 8')
    out['far_field'] = far
    # (d) z -> -z symmetry and a few sample values
    sym = 0.0
    for (x1, z) in SAMPLE_POINTS[:4]:
        r1 = lambda_at(x1, z, 0.0, 1.0, rules)
        r2 = lambda_at(x1, -z, 0.0, 1.0, rules)
        sym = max(sym, abs(r1['lambda'] - r2['lambda']) / r1['lambda'])
    require(sym < 1e-10, 'reflection symmetry z -> -z')
    out['reflection_symmetry_max_rel_dev'] = sym
    # (e) k-dependence enters only through the f_xxx = 12k conditioning: at |x| = 8 Lambda is k-free
    a1 = lambda_at(8.0, 0.0, 0.0, 0.5, rules)['lambda']
    a2 = lambda_at(8.0, 0.0, 0.0, 2.0, rules)['lambda']
    require(abs(a1 - a2) < 1e-9 * a1, 'far field is k-free')
    return out


def sample_table(b, k, rules, L=None):
    rows = []
    for (x1, z) in SAMPLE_POINTS:
        r = lambda_at(x1, z, b, k, rules, L)
        rows.append({'x': [x1, z], 'lambda': r['lambda'], 'lambda_j': r['lambda_j'], 'rho': r['rho'], 'coupling': r['coupling'], 'exact_regression': r['exact_regression']})
    return rows


def ray_profile(b, k, rules):
    """Lambda(x)/Lambda_inf along rays from the pin at angles 90 (transverse), 60, 45, 30, 0 degrees."""
    far = lambda_far(b, rules)['lambda']
    rows = []
    for ang_deg in (90, 60, 45, 30, 0):
        th = math.radians(ang_deg)
        for rad in (0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0):
            x1, z = rad * math.cos(th), rad * math.sin(th)
            if ang_deg == 0:
                z = 0.0
            r = lambda_at(x1, z, b, k, rules)
            rows.append({'angle_deg': ang_deg, 'r': rad, 'ratio': r['lambda'] / far, 'ratio_unweighted': r['rho'] / far})
    return rows


def near_zero_profile(b, k, rules):
    rows = []
    for rad in (0.05, 0.1, 0.2, 0.4):
        for ang_deg in (0, 30, 60, 90, 120, 150, 180):
            th = math.radians(ang_deg)
            x1, z = rad * math.cos(th), rad * math.sin(th)
            if ang_deg in (0, 180):
                z = 0.0
            r = lambda_at(x1, z, b, k, rules)
            rows.append({'r': rad, 'angle_deg': ang_deg, 'lambda': r['lambda'], 'lambda_j': r['lambda_j'], 'exact_regression': r['exact_regression']})
    return rows


# ----------------------------------------------------------------------------- main
def full_run(fast=False):
    rules = Rules()
    hi_rules = Rules(32, 48, 32)
    res = {'object': 'CL-C6-REMOTE-COEFF-NUMERICS-20260930-v1', 'scientific_effect': 'NONE', 'certified': False,
           'quadrature': {'coordinates': 'a = tr H / 2, (c, h2) polar; splits at a = 0 and rho = |a|',
                          'a_gauss_legendre_per_side': 24, 'theta_trapezoid': 32, 'rho_gauss_legendre_per_side': 24, 'cut_sd': 9.0,
                          'high_order_check': [32, 48, 32]}}
    res['controls'] = controls(rules)
    mc = mc_absdet(200000)
    res['controls']['mc_absdet_unconditional'] = {'mean': mc[0], 'se': mc[1], 'n': 200000, 'seed': 2026}
    # quadrature-order check at the sample points
    qdev = 0.0
    for (x1, z) in SAMPLE_POINTS:
        a = lambda_at(x1, z, 0.0, 1.0, rules)['lambda']
        c = lambda_at(x1, z, 0.0, 1.0, hi_rules)['lambda']
        qdev = max(qdev, abs(a - c) / c)
    res['quadrature']['max_rel_dev_vs_high_order_at_samples'] = qdev
    res['samples'] = {}
    res['samples_L6'] = {}
    res['near_zero_profile'] = {}
    res['ray_profile'] = {}
    res['far_field'] = {}
    res['hole'] = {}
    res['torus'] = {}
    res['remote_total'] = {}
    ks = (0.5, 1.0, 2.0)
    bs = (0.0, 1.0)
    grid_h = 0.4 if fast else 0.15
    for b in bs:
        far = lambda_far(b, rules)
        res['far_field'][str(b)] = {'lambda_inf': far['lambda'], 'lambda_inf_j': far['lambda_j'], 'E_F_j_given_level': far['E_F_j'],
                                    'p_inf': phi(b) / (2 * math.pi)}
        for k in ks:
            key = 'k=%s,b=%s' % (k, b)
            res['samples'][key] = sample_table(b, k, rules)
            res['samples_L6'][key] = sample_table(b, k, rules, 6.0)
            res['near_zero_profile'][key] = near_zero_profile(b, k, rules)
            res['ray_profile'][key] = ray_profile(b, k, rules)
            H = hole_integral(b, k, rules, Rc=6.0, h=grid_h, lam_inf=far)
            res['hole'][key] = H
            T6 = torus_integral(b, k, rules, 6.0, h=grid_h)
            res['torus'][key] = {'L=6': T6}
            rt = {}
            for L in (6.0, 12.0, 24.0):
                approx = L * L * far['lambda'] + H['hole']
                rt['L=%g' % L] = {'integral_X_Lambda_approx': approx, 'k_integral': k * approx}
            rt['L=6']['integral_X_Lambda_periodized_direct'] = T6['integral']
            rt['L=6']['k_integral_direct'] = k * T6['integral']
            res['remote_total'][key] = rt
            print('done', key, 'hole', H['hole'], 'L6 direct', T6['integral'], 'approx', 36 * far['lambda'] + H['hole'], flush=True)
    # grid-convergence, quadrature-order and tail checks for one parameter set; direct periodized L = 12 integral
    far0 = lambda_far(0.0, rules)
    far0_hi = lambda_far(0.0, hi_rules)
    Hc = hole_integral(0.0, 1.0, rules, Rc=6.0, h=0.3, lam_inf=far0)
    Hc_hi = hole_integral(0.0, 1.0, hi_rules, Rc=6.0, h=0.3, lam_inf=far0_hi)
    Hf = hole_integral(0.0, 1.0, rules, Rc=6.0, h=0.1, lam_inf=far0) if not fast else Hc
    Ht = hole_integral(0.0, 1.0, rules, Rc=5.0, h=0.3, lam_inf=far0)
    T12 = torus_integral(0.0, 1.0, rules, 12.0, h=0.2)
    res['grid_convergence'] = {'k=1.0,b=0.0': {'hole_h=0.3,Rc=6': Hc['hole'], 'hole_h=0.3,Rc=6,high_order': Hc_hi['hole'],
                                              'hole_h=0.3,Rc=5': Ht['hole'], 'hole_h=0.1,Rc=6': Hf['hole'],
                                              'hole_h=%s,Rc=6' % grid_h: res['hole']['k=1.0,b=0.0']['hole'],
                                              'hole_j_h=0.1,Rc=6': Hf['hole_j'],
                                              'torus_L=12_direct_h=0.2': T12['integral'],
                                              'torus_L=12_approx': 144 * far0['lambda'] + res['hole']['k=1.0,b=0.0']['hole'],
                                              'lambda_inf_high_order': far0_hi['lambda']}}
    res['exact_regression_points'] = EXACT_COUNT[0]
    return res


def check_run():
    rules = Rules()
    ctl = controls(rules)
    path = os.path.join(HERE, 'RESULTS.json')
    require(os.path.exists(path), 'RESULTS.json present')
    with open(path) as fh:
        ref = json.load(fh)
    for b in (0.0, 1.0):
        far = lambda_far(b, rules)
        require(abs(far['lambda'] - ref['far_field'][str(b)]['lambda_inf']) < 1e-10, 'far-field replay b = %r' % b)
    for key, k in (('k=1.0,b=0.0', 1.0), ('k=0.5,b=1.0', 0.5)):
        b = 0.0 if key.endswith('0.0') else 1.0
        rows = sample_table(b, k, rules)
        for r, rr in zip(rows, ref['samples'][key]):
            require(abs(r['lambda'] - rr['lambda']) <= 1e-9 * max(abs(rr['lambda']), 1e-6), 'sample replay %s at %r' % (key, r['x']))
        rows6 = sample_table(b, k, rules, 6.0)
        for r, rr in zip(rows6, ref['samples_L6'][key]):
            require(abs(r['lambda'] - rr['lambda']) <= 1e-9 * max(abs(rr['lambda']), 1e-6), 'L = 6 sample replay %s at %r' % (key, r['x']))
    # a near-axis point that needs the decimal regression
    r = lambda_at(0.1, 0.0, 0.0, 1.0, rules)
    require(r['exact_regression'] and r['lambda'] < 1e-20, 'near-axis point handled by the decimal regression and exponentially small')
    for row in ref['near_zero_profile']['k=1.0,b=0.0']:
        if row['r'] == 0.1 and row['angle_deg'] == 0:
            require(abs(row['lambda'] - r['lambda']) <= 1e-9 * max(abs(r['lambda']), 1e-30), 'near-zero replay')
    print(json.dumps({'check': 'ok', 'controls': list(ctl.keys()), 'mutant': MUT}))


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--fast', action='store_true', help='coarser grid (development only)')
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
