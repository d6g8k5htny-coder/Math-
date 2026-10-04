#!/usr/bin/env python3
"""Certified lower bound z_* for the planar finite-r full normalizer Z_r / r^2 of [LP] section 1 (parent torus kernel).

Z_r = E_Q[|det H_M det H_S| 1{H_M < 0, index H_S = 1}], Q the Gaussian regression at the six pins
f(M) = b, f(S) = b - k r^3, grad f(M) = grad f(S) = 0, M = -(r/2) u, S = (r/2) u, d = 2.

Method (all arithmetic exact rational; transcendental constants bracketed by series with remainder bounds):
  * pins and Hessian targets are re-expressed through midpoint-jet combinations (p1, p2, p3', p4, q1, q2; T, v, w)
    whose covariance matrix has an O(1) nondegenerate limit as r -> 0, so that the Gaussian regression is a
    well-conditioned 6 x 6 interval solve; every raw covariance is an exact Laurent polynomial in r (Hermite
    polynomials times the Taylor polynomial of exp(-r^2/2)) plus a remainder interval;
  * the torus kernel K_L differs from the continuum Gaussian kernel by a periodization remainder bounded
    explicitly (any frame, L >= L_MIN);
  * E[W 1_cell] >= min_cell |det H_M| |det H_S| x P(cell) summed over a grid of disjoint cells, with P(cell)
    a rigorous lower bound from the block Cholesky factor (2 x 2 blocks; cross-block couplings absorbed by a
    box shrink on |z|_inf <= Z_MAX), each 2-d rectangle probability by a piecewise lower Riemann sum whose
    integrand min is attained at piece endpoints (unimodality of Phi(u(s)) - Phi(l(s)) for parallel affine u, l).
Standard library only; deterministic; outputs are exact rationals (printed as decimals rounded down).
"""
import argparse
import json
import math
import multiprocessing
import os
import random
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
MUTANTS = ('swap-minmax', 'drop-torus-error', 'sign-saddle')
MUT = None
PBITS = 160
N_EXP = 24          # Taylor order of exp(-r^2/2)
L_MIN = 10          # default torus side floor for the quick and point-band checks (the certified bands carry their own)
Z_MAX = 8           # |z|_inf clip for the cross-block coupling argument
# certified r-bands: name -> (r range, number of r-steps of width 1/512, declared torus side floor L >= L_min);
# the low band needs L >= 12 because the periodization remainder enters the preconditioned functionals with the
# factor r^-10 (see torus_epsilon and NOTE.md section 2)
BANDS = {
    'high': {'r': (Fr(1, 8), Fr(1, 2)), 'steps': 192, 'L_min': 10},
    'low': {'r': (Fr(1, 64), Fr(1, 8)), 'steps': 56, 'L_min': 12},
}
BAND_ORDER = ('low', 'high')
BAND_B = (Fr(0), Fr(1))
B_STEPS = 8
BAND_K = (Fr(1, 2), Fr(2))
K_STEPS = 6
GRID = {'n_w': 40, 'n_o': 40, 'n_v': 6, 'n_T': 8, 'c_T': Fr(4), 'c_v': Fr(7, 2), 'span_w': Fr(5), 'pieces_w': 10, 'pieces_T': 8, 'pieces_v': 8}


def require(cond, msg):
    if not cond:
        print(json.dumps({'check': 'FAIL', 'reason': msg, 'mutant': MUT}))
        sys.exit(1)


# ----------------------------------------------------------------------------- rational intervals
def rdown(x):
    return Fr(x.numerator * (1 << PBITS) // x.denominator, 1 << PBITS)


def rup(x):
    return Fr(-((-x.numerator) * (1 << PBITS) // x.denominator), 1 << PBITS)


class IV:
    __slots__ = ('lo', 'hi')

    def __init__(self, lo, hi=None):
        lo = Fr(lo)
        hi = lo if hi is None else Fr(hi)
        if hi < lo:
            raise ValueError('empty interval')
        self.lo, self.hi = rdown(lo), rup(hi)

    def __repr__(self):
        return 'IV(%s, %s)' % (float(self.lo), float(self.hi))

    def __add__(self, o):
        o = o if isinstance(o, IV) else IV(o)
        return IV(self.lo + o.lo, self.hi + o.hi)
    __radd__ = __add__

    def __neg__(self):
        return IV(-self.hi, -self.lo)

    def __sub__(self, o):
        return self + (-(o if isinstance(o, IV) else IV(o)))

    def __rsub__(self, o):
        return IV(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, IV) else IV(o)
        c = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return IV(min(c), max(c))
    __rmul__ = __mul__

    def inv(self):
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError('interval contains zero')
        return IV(1 / self.hi, 1 / self.lo)

    def __truediv__(self, o):
        o = o if isinstance(o, IV) else IV(o)
        return self * o.inv()

    def __rtruediv__(self, o):
        return IV(o) * self.inv()

    def sq(self):
        if self.lo >= 0:
            return IV(self.lo * self.lo, self.hi * self.hi)
        if self.hi <= 0:
            return IV(self.hi * self.hi, self.lo * self.lo)
        return IV(0, max(self.lo * self.lo, self.hi * self.hi))

    def meet(self, o):
        lo, hi = max(self.lo, o.lo), min(self.hi, o.hi)
        if hi < lo:
            raise ValueError('inconsistent enclosures')
        return IV(lo, hi)

    def width(self):
        return self.hi - self.lo

    def mid(self):
        return (self.lo + self.hi) / 2

    def contains(self, x):
        return self.lo <= x <= self.hi


def isqrt_iv(x):
    """Enclosure of sqrt(x) for an interval x with x.lo > 0."""
    if x.lo <= 0:
        raise ValueError('sqrt of interval reaching zero: %r' % x)

    def lo_root(v):
        n = v.numerator * (1 << (2 * PBITS)) // v.denominator
        s = math.isqrt(n)
        return Fr(s, 1 << PBITS)

    def hi_root(v):
        n = -((-v.numerator * (1 << (2 * PBITS))) // v.denominator)
        s = math.isqrt(n) + 1
        return Fr(s, 1 << PBITS)
    return IV(lo_root(x.lo), hi_root(x.hi))


def exp_neg_point(t):
    """Enclosure of exp(-t) for a rational t >= 0 (halving to t <= 1/2, then the alternating series)."""
    t = Fr(t)
    m = 0
    while t > Fr(1, 2):
        t /= 2
        m += 1
    s = Fr(1)
    term = Fr(1)
    n = 0
    while True:
        n += 1
        term = term * (-t) / n
        if abs(term) < Fr(1, 1 << (PBITS + 8)):
            break
        s += term
    v = IV(s - abs(term), s + abs(term))
    for _ in range(m):
        v = v.sq()
    return v


def exp_neg(t):
    """exp(-t) on an interval t with t.lo >= 0 (monotone decreasing)."""
    return IV(exp_neg_point(t.hi).lo, exp_neg_point(t.lo).hi)


def _atan_inv(n):
    """Enclosure of arctan(1/n), n >= 2, alternating series."""
    x = Fr(1, n)
    s = Fr(0)
    term = x
    k = 0
    while True:
        s += term / (2 * k + 1)
        k += 1
        term = term * (-x * x)
        if abs(term) / (2 * k + 1) < Fr(1, 1 << (PBITS + 8)):
            break
    return IV(s - abs(term), s + abs(term))


PI = 4 * (4 * _atan_inv(5) - _atan_inv(239))
SQRT2 = isqrt_iv(IV(2))
SQRT2PI = isqrt_iv(2 * PI)


def phi_point(x):
    """Enclosure of Phi(x) = P(N(0,1) <= x) for a rational x with |x| <= 12, from the series
    Phi(x) = 1/2 + (1/sqrt(2 pi)) sum_n (-1)^n x^(2n+1) / (2^n n! (2n+1)), evaluated in fixed point (ulp = 2^-(PBITS+40))
    with an explicit integer bound E on the accumulated rounding error (in ulps) and the alternating-tail bound."""
    x = Fr(x)
    if x < 0:
        p = phi_point(-x)
        return IV(1 - p.hi, 1 - p.lo)
    if x > 12:
        raise ValueError('phi_point range')
    P2 = PBITS + 40
    ONE = 1 << P2
    X = x.numerator * ONE // x.denominator          # x_lo = X / ONE <= x < (X + 1) / ONE ; |Phi(x) - Phi(x_lo)| <= 1 ulp
    if X == 0:                                       # 0 <= x < 1 ulp: Phi(x) in [1/2, 1/2 + ulp]
        return IV(Fr(1, 2), Fr(1, 2) + Fr(1, ONE))
    X2u = (X + 1) * (X + 1)                          # upper bound of x^2 ONE^2
    S = 0
    T = X                                            # T_n ~ x^(2n+1) / (2^n n!) in ulps
    E = 1                                            # error bound of T_n in ulps
    Etot = 1                                         # error of S in ulps (starts with the x rounding)
    n = 0
    while T > 0:
        S += (-1) ** n * (T // (2 * n + 1))
        Etot += E + 1
        n += 1
        T = (T * X * X) // (ONE * ONE * 2 * n)
        E = (E * X2u) // (ONE * ONE * 2 * n) + 2
    # once T == 0 in fixed point the remaining terms are each below 1 ulp; if x^2 >= 2 n they are still growing in
    # exact arithmetic, so continue counting until they decrease: bound the tail by the first omitted exact term
    # <= (T_n + E) ulps <= (E + 1) ulps when T_n == 0 ... but growth may resume; require the decreasing regime.
    if x * x > 2 * n:
        raise ValueError('series terminated before the decreasing regime')
    Etot += E + 1
    core = IV(Fr(S - Etot, ONE), Fr(S + Etot, ONE)) / SQRT2PI
    return IV(Fr(1, 2) + core.lo, Fr(1, 2) + core.hi)


def Phi(x):
    """Phi on an interval (monotone); arguments clipped to [-Z_MAX - 4, Z_MAX + 4] (clipping only widens)."""
    lo = max(x.lo, Fr(-12))
    hi = min(x.hi, Fr(12))
    if x.lo < -12:
        plo = Fr(0)
    else:
        plo = phi_point(lo).lo
    if x.hi > 12:
        phi_ = Fr(1)
    else:
        phi_ = phi_point(hi).hi
    return IV(plo, phi_)


# ----------------------------------------------------------------------------- Laurent polynomials in r
class LP:
    """Laurent polynomial in r with rational coefficients: {power: coeff}."""
    __slots__ = ('c',)

    def __init__(self, c=None):
        self.c = {k: v for k, v in (c or {}).items() if v != 0}

    @staticmethod
    def const(a):
        return LP({0: Fr(a)})

    @staticmethod
    def mono(a, p):
        return LP({p: Fr(a)})

    def __add__(self, o):
        c = dict(self.c)
        for k, v in o.c.items():
            c[k] = c.get(k, Fr(0)) + v
        return LP(c)

    def __neg__(self):
        return LP({k: -v for k, v in self.c.items()})

    def __sub__(self, o):
        return self + (-o)

    def __mul__(self, o):
        if not isinstance(o, LP):
            return LP({k: v * Fr(o) for k, v in self.c.items()})
        c = {}
        for k1, v1 in self.c.items():
            for k2, v2 in o.c.items():
                c[k1 + k2] = c.get(k1 + k2, Fr(0)) + v1 * v2
        return LP(c)
    __rmul__ = __mul__

    def minpow(self):
        return min(self.c) if self.c else 0

    def eval(self, r):
        """Enclosure on the band r (IV with r.lo > 0)."""
        tot = IV(0)
        for k, v in self.c.items():
            if k >= 0:
                pk = IV(r.lo ** k, r.hi ** k)
            else:
                pk = IV(r.hi ** k, r.lo ** k)
            tot = tot + pk * v
        return tot

    def maxabs(self, r):
        return sum(abs(v) * max(r.lo ** k, r.hi ** k) for k, v in self.c.items()) if self.c else Fr(0)


def hermite_poly(n, sign):
    """He_n(sign * r) as an LP (probabilists' Hermite)."""
    a, b = LP.const(1), LP.mono(sign, 1)
    if n == 0:
        return a
    for k in range(1, n):
        a, b = b, LP.mono(sign, 1) * b - a * k
    return b


def hermite0(n):
    if n % 2:
        return Fr(0)
    return Fr((-1) ** (n // 2) * math.prod(range(1, n, 2)))


def exp_taylor():
    """Taylor polynomial of exp(-r^2/2) to order 2 N_EXP."""
    c = {}
    for j in range(N_EXP + 1):
        c[2 * j] = Fr((-1) ** j, 2 ** j * math.factorial(j))
    return LP(c)


EXP_TAYLOR = exp_taylor()


def exp_remainder(rhi):
    """|exp(-r^2/2) - Taylor| <= (r^2/2)^(N+1) / (N+1)! on 0 <= r <= rhi (alternating series)."""
    return (rhi * rhi / 2) ** (N_EXP + 1) / math.factorial(N_EXP + 1)


def torus_epsilon(L, rhi):
    """Bound on |sum_{n != 0} d^gamma G(w + R^T n L)| for |w| <= rhi, |gamma| <= 4, G = exp(-|y|^2/2), d = 2:
    m = 1 shell (8 points, |y| >= L - r, (s+3)^4 e^{-s^2/2} decreasing for s > 1) plus the m >= 2 tail."""
    L = Fr(L)
    s1 = L - rhi
    e1 = exp_neg_point(s1 * s1 / 2).hi
    first = 8 * (s1 + 3) ** 4 * e1
    e2 = exp_neg_point((2 * L - rhi) ** 2 / 2).hi
    eL = exp_neg_point(L * L / 2).hi
    tail = 128 * 32 * (L + 3) ** 4 * e2 / (1 - 32 * eL)
    return first + tail


# ----------------------------------------------------------------------------- functionals and covariances
# a functional is a list of (LP coefficient, x-order, y-order, point) with point in {'M', 'S'}
def functionals():
    f = lambda pt: (0, 0, pt)
    fx = lambda pt: (1, 0, pt)
    fy = lambda pt: (0, 1, pt)
    fxx = lambda pt: (2, 0, pt)
    fxy = lambda pt: (1, 1, pt)
    fyy = lambda pt: (0, 2, pt)
    h = Fr(1, 2)
    pins = {
        'p1': [(LP.const(h), f('M')), (LP.const(h), f('S'))],
        'p2': [(LP.mono(-1, -1), f('M')), (LP.mono(1, -1), f('S'))],
        'p3p': [(LP.mono(6, -2), fx('M')), (LP.mono(6, -2), fx('S')), (LP.mono(12, -3), f('M')), (LP.mono(-12, -3), f('S'))],
        'p4': [(LP.mono(-1, -1), fx('M')), (LP.mono(1, -1), fx('S'))],
        'q1': [(LP.const(h), fy('M')), (LP.const(h), fy('S'))],
        'q2': [(LP.mono(-1, -1), fy('M')), (LP.mono(1, -1), fy('S'))],
    }
    targets = {
        'TM': [(LP.mono(1, -2), fxx('M')), (LP.mono(4, -3), fx('M')), (LP.mono(2, -3), fx('S')), (LP.mono(6, -4), f('M')), (LP.mono(-6, -4), f('S'))],
        'tau': [(LP.mono(1, -3), fxx('S')), (LP.mono(-1, -3), fxx('M')), (LP.mono(-6, -4), fx('M')), (LP.mono(-6, -4), fx('S')), (LP.mono(-12, -5), f('M')), (LP.mono(12, -5), f('S'))],
        'vM': [(LP.mono(1, -1), fxy('M')), (LP.mono(1, -2), fy('M')), (LP.mono(-1, -2), fy('S'))],
        'nu': [(LP.mono(1, -2), fxy('M')), (LP.mono(1, -2), fxy('S')), (LP.mono(2, -3), fy('M')), (LP.mono(-2, -3), fy('S'))],
        'wM': [(LP.const(1), fyy('M'))],
        'om': [(LP.mono(1, -1), fyy('S')), (LP.mono(-1, -1), fyy('M'))],
    }
    # T_S = T_M + r tau ; v_S = r nu - v_M ; w_S = w_M + r om
    return pins, targets


PIN_NAMES = ('p1', 'p2', 'p3p', 'p4', 'q1', 'q2')
TARGET_NAMES = ('wM', 'om', 'TM', 'tau', 'vM', 'nu')     # block order: yy, xx, xy (difference coordinates)


def raw_cov(u, v):
    """Cov(d^u f(s), d^v f(t)) for the continuum kernel as (LP in r, hermite max-abs LP for the E-remainder), with
    u = (a, b, s), v = (c, d, t): X = (-1)^c He_{a+c}(Delta) g(Delta), Y = (-1)^d He_{b+d}(0), Delta = t - s in {0, +-r}."""
    a, b, s = u
    c, d, t = v
    Y = (-1) ** d * hermite0(b + d)
    if Y == 0:
        return None
    if s == t:
        X = LP.const((-1) ** c * hermite0(a + c))
        return X * Y, LP()
    sign = 1 if (s, t) == ('M', 'S') else -1
    He = hermite_poly(a + c, sign) * ((-1) ** c)
    return He * EXP_TAYLOR * Y, He * Y


def cov_functional(F, G, rband, eps_torus):
    """Enclosure of Cov(F, G) on the band (both F, G lists of (LP coeff, jet)); returns (LP exact part, IV)."""
    poly = LP()
    err = Fr(0)
    rhi = rband.hi
    rem = exp_remainder(rhi)
    for cf, jf in F:
        for cg, jg in G:
            coef = cf * cg
            rc = raw_cov(jf, jg)
            if rc is not None:
                p, he = rc
                poly = poly + coef * p
                err += coef.maxabs(rband) * he.maxabs(rband) * rem
            # torus periodization remainder on every raw entry (before normalization)
            err += coef.maxabs(rband) * eps_torus
    return poly, poly.eval(rband) + IV(-err, err)


def matrices(rband, L):
    pins, targets = functionals()
    eps = Fr(0) if MUT == 'drop-torus-error' else torus_epsilon(L, rband.hi)
    P = [pins[n] for n in PIN_NAMES]
    T = [targets[n] for n in TARGET_NAMES]
    Spp = [[None] * 6 for _ in range(6)]
    Stp = [[None] * 6 for _ in range(6)]
    Stt = [[None] * 6 for _ in range(6)]
    for i in range(6):
        for j in range(6):
            pol, Spp[i][j] = cov_functional(P[i], P[j], rband, eps)
            require(pol.minpow() >= 0, 'pin covariance has a negative Laurent power: %s %s' % (PIN_NAMES[i], PIN_NAMES[j]))
            pol, Stp[i][j] = cov_functional(T[i], P[j], rband, eps)
            require(pol.minpow() >= 0, 'target-pin covariance has a negative Laurent power')
            pol, Stt[i][j] = cov_functional(T[i], T[j], rband, eps)
            require(pol.minpow() >= 0, 'target covariance has a negative Laurent power')
    return Spp, Stp, Stt, eps


def solve_iv(A, B):
    """Interval Gaussian elimination with partial pivoting on midpoints: returns X with A X_i = B_i for each column B_i."""
    n = len(A)
    M = [[A[i][j] for j in range(n)] + [B[c][i] for c in range(len(B))] for i in range(n)]
    for col in range(n):
        p = max(range(col, n), key=lambda i: abs(M[i][col].mid()))
        M[col], M[p] = M[p], M[col]
        piv = M[col][col]
        for i in range(col + 1, n):
            f = M[i][col] / piv
            for j in range(col, len(M[i])):
                M[i][j] = M[i][j] - f * M[col][j]
    X = []
    for c in range(len(B)):
        x = [None] * n
        for i in reversed(range(n)):
            s = M[i][n + c]
            for j in range(i + 1, n):
                s = s - M[i][j] * x[j]
            x[i] = s / M[i][i]
        X.append(x)
    return X


def regression(rband, L, mats=None):
    """Interval regression of the preconditioned targets on the pins over an r-band: the conditional mean is exactly
    b * alpha + k * beta (the pin values are b (1, 0, 0, 0, 0, 0) + k (-r^3/2, -r^2, 12, 0, 0, 0)); alpha, beta and the
    conditional covariance C depend on r only."""
    Spp, Stp, Stt, eps = mats if mats is not None else matrices(rband, L)
    W = solve_iv(Spp, Stp)        # W[i] = Spp^{-1} Stp[i]
    r = rband
    kvec = [-r * r * r / 2, -r * r, IV(12), IV(0), IV(0), IV(0)]
    alpha = [W[i][0] for i in range(6)]
    beta = [sum((W[i][j] * kvec[j] for j in range(6)), IV(0)) for i in range(6)]
    C = [[Stt[i][j] - sum((W[i][l] * Stp[j][l] for l in range(6)), IV(0)) for j in range(6)] for i in range(6)]
    for i in range(6):
        for j in range(i + 1, 6):
            C[i][j] = C[j][i] = C[i][j].meet(C[j][i])
    # torus normalizer K_L(0) = 1: the whole covariance is divided by sum_n exp(-|nL|^2/2) in [1, 1 + eps0]
    eps0 = Fr(0) if MUT == 'drop-torus-error' else torus_epsilon(L, Fr(0))
    scale = IV(1 / (1 + eps0), 1)
    C = [[C[i][j] * scale for j in range(6)] for i in range(6)]
    return alpha, beta, C


def conditional(rband, bband, kband, L, mats=None):
    alpha, beta, C = regression(rband, L, mats)
    mu = [bband * alpha[i] + kband * beta[i] for i in range(6)]
    return mu, C


def cholesky_iv(C):
    n = len(C)
    Lm = [[IV(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = C[i][j]
            for k in range(j):
                s = s - Lm[i][k] * Lm[j][k]
            if i == j:
                Lm[i][i] = isqrt_iv(s)
            else:
                Lm[i][j] = s / Lm[j][j]
    return Lm


# ----------------------------------------------------------------------------- cell bounds
BLOCKS = ((0, 1), (2, 3), (4, 5))     # (wM, om), (TM, tau), (vM, nu) in TARGET_NAMES order


def block_prob(mu_p, mu_q, Lpp, Lqp, Lqq, lp, hp, lq, hq, pieces):
    """Lower bound of P(mu_p + Lpp z_a in [lp, hp], mu_q + Lqp z_a + Lqq z_b in [lq, hq]) for independent standard
    normals z_a, z_b, valid for every realization inside the interval data. The inner integrand
    g(s) = Phi((hq - mu_q - Lqp s)/Lqq) - Phi((lq - mu_q - Lqp s)/Lqq) is unimodal in s (its derivative is
    -Lqp/Lqq (phi(u) - phi(l)) with u > l, which changes sign once, where u + l = 0), so its minimum over a piece is
    attained at an endpoint."""
    A = ((IV(lp) - mu_p) / Lpp).hi
    B = ((IV(hp) - mu_p) / Lpp).lo
    A = max(A, Fr(-Z_MAX))
    B = min(B, Fr(Z_MAX))
    if B <= A:
        return IV(0)
    total = IV(0)
    edges = [A + (B - A) * i / pieces for i in range(pieces + 1)]
    gvals = []
    for s in edges:
        u = (IV(hq) - mu_q - Lqp * s) / Lqq
        l = (IV(lq) - mu_q - Lqp * s) / Lqq
        g = Phi(u) - Phi(l)
        gvals.append(g)
    for i in range(pieces):
        g0, g1 = gvals[i], gvals[i + 1]
        if MUT == 'swap-minmax':
            gmin = max(g0.lo, g1.lo)
        else:
            gmin = min(g0.lo, g1.lo)
        if gmin <= 0:
            continue
        pw = Phi(IV(edges[i + 1])).lo - Phi(IV(edges[i])).hi
        if pw <= 0:
            continue
        total = total + IV(gmin) * IV(pw)
    return total


def band_data(rband, L, grid=GRID, mats=None):
    """Everything that depends on r only: the regression, the block Cholesky factor, and the cell probabilities in the
    centred coordinates y = x - b alpha - k beta (conditional mean exactly zero for every b, k)."""
    alpha, beta, C = regression(rband, L, mats)
    Lm = cholesky_iv(C)
    zero = [IV(0)] * 6
    eta = []
    for i in range(6):
        blk = [bb for bb in BLOCKS if i in bb][0]
        eta.append(sum(max(abs(Lm[i][j].lo), abs(Lm[i][j].hi)) for j in range(i) if j not in blk) * Z_MAX)
    sd = [isqrt_iv(C[i][i]).hi for i in range(6)]

    def bp(blk, lo_p, hi_p, lo_q, hi_q, pieces):
        p, q = blk
        return block_prob(zero[p], zero[q], Lm[p][p], Lm[q][p], Lm[q][q], lo_p + eta[p], hi_p - eta[p], lo_q + eta[q], hi_q - eta[q], pieces)

    cT, cv, nv, nw, span, nT = grid['c_T'], grid['c_v'], grid['n_v'], grid['n_w'], grid['span_w'], grid['n_T']
    # xx block: y_TM slabs times a y_tau box
    Tedges = [-cT * sd[2] + 2 * cT * sd[2] * i / nT for i in range(nT + 1)]
    taubox = (-cT * sd[3], cT * sd[3])
    P_T = [bp(BLOCKS[1], Tedges[t], Tedges[t + 1], taubox[0], taubox[1], grid['pieces_T']) for t in range(nT)]
    # xy block: |y_vM| slabs times a y_nu box
    vedges = [cv * sd[4] * i / nv for i in range(nv + 1)]
    P_v = []
    for l in range(nv):
        a, c = vedges[l], vedges[l + 1]
        P_v.append(bp(BLOCKS[2], a, c, -cv * sd[5], cv * sd[5], grid['pieces_v']) + bp(BLOCKS[2], -c, -a, -cv * sd[5], cv * sd[5], grid['pieces_v']))
    # yy block: cells in (y_wM, y_om); w_M = y_wM + b alpha_0 + ... < 0 needs y_wM below about b, so the y_wM grid
    # stops at the top of the b band (alpha_0 is -1 up to the torus remainder)
    no = grid['n_o']
    ytop = BAND_B[1] + Fr(1, 8)
    eM = [-span * sd[0] + (ytop + span * sd[0]) * i / nw for i in range(nw + 1)]
    eO = [-span * sd[1] + 2 * span * sd[1] * j / no for j in range(no + 1)]
    P_w = [[bp(BLOCKS[0], eM[i], eM[i + 1], eO[j], eO[j + 1], grid['pieces_w']) for j in range(no)] for i in range(nw)]
    tail = 12 * (1 - Phi(IV(Z_MAX)).lo)
    return {'alpha': alpha, 'beta': beta, 'C': C, 'sd': sd, 'Tedges': Tedges, 'taubox': taubox, 'P_T': P_T, 'vedges': vedges, 'P_v': P_v,
            'eM': eM, 'eO': eO, 'P_w': P_w, 'tail': tail, 'rband': rband}


def subbox_floor(data, bband, kband):
    """Certified lower bound of Z_r on the (r-band) x bband x kband box from the band data; returns (Z_lower, floor for Z_r / r^2).
    The sum over cells factorizes: sum_{i,t} P_T[t] [sum_l detM(i,l,t) P_v[l]] [sum_j detS(i,j,t) P_w[i][j]], every factor a
    nonnegative lower bound; the |z|_inf > Z_MAX tail is subtracted once through sum_cells detM detS."""
    r, b, k = data['rband'], bband, kband
    al, be = data['alpha'], data['beta']
    mu = [b * al[i] + k * be[i] for i in range(6)]          # x = y + mu, mu an interval over the sub-box
    Tedges, (talo, tahi), P_T = data['Tedges'], data['taubox'], data['P_T']
    ta = IV(talo, tahi) + mu[3]
    nT = len(P_T)
    nv = len(data['P_v'])
    xy2 = []
    for l in range(nv):
        c = data['vedges'][l + 1]
        vmax = max(abs(-c + mu[4].lo), abs(c + mu[4].hi))
        xy2.append((r * IV(vmax * vmax) / k).hi)             # H_xy(M)^2 / (r k) on the slab
    eM, eO, P_w, tail = data['eM'], data['eO'], data['P_w'], data['tail']
    nw, no = len(P_w), len(P_w[0])
    total = Fr(0)
    detsum = Fr(0)
    for t in range(nT):
        TM = IV(Tedges[t], Tedges[t + 1]) + mu[2]
        hxxM = r * TM / k - 6                                # H_xx(M) / (r k)
        hxxS = r * (TM + r * ta) / k + 6                     # H_xx(S) / (r k)
        if hxxM.hi >= 0 or hxxS.lo <= 0:
            continue
        for i in range(nw):
            wM = IV(eM[i], eM[i + 1]) + mu[0]
            if wM.hi >= 0:
                continue
            prodM = (hxxM * wM).lo
            sM = Fr(0)
            dM = Fr(0)
            for l in range(nv):
                detM = prodM - xy2[l]                        # det H_M / (r k) >= detM on the cell
                if detM <= 0:
                    continue
                sM += detM * data['P_v'][l].lo
                dM += detM
            if sM <= 0:
                continue
            sS = Fr(0)
            dS = Fr(0)
            for j in range(no):
                wS = wM + r * (IV(eO[j], eO[j + 1]) + mu[1])
                if wS.hi >= 0:
                    continue
                detS = -(hxxS * wS).hi                       # |det H_S| / (r k) >= detS (H_xy(S)^2 >= 0 dropped)
                if MUT == 'sign-saddle':
                    detS = (hxxS * wS).hi
                if detS <= 0:
                    continue
                sS += detS * P_w[i][j].lo
                dS += detS
            total += P_T[t].lo * sM * sS
            detsum += dM * dS
    q = rdown(total - tail * detsum)    # Z_r / (r^2 k^2) >= q on the box
    if q <= 0:
        return Fr(0), Fr(0)
    fl = q * k.lo * k.lo
    fl = Fr(fl.numerator * (1 << 64) // fl.denominator, 1 << 64)      # rounded down to 2^-64 for storage
    return fl * r.lo * r.lo, fl


def band_floor(rband, bband, kband, L, grid=GRID, mats=None):
    data = band_data(rband, L, grid, mats)
    zlo, fl = subbox_floor(data, bband, kband)
    return zlo, fl, {'P_T': [float(p.lo) for p in data['P_T']], 'P_v': [float(p.lo) for p in data['P_v']]}


# ----------------------------------------------------------------------------- floating controls (not certified)
def float_conditional(r, b, k):
    """Direct floating regression of the six Hessian entries on the six raw pins (continuum kernel), for comparison."""
    def he(n, x):
        a, bb = 1.0, x
        if n == 0:
            return a
        for kk in range(1, n):
            a, bb = bb, x * bb - kk * a
        return bb

    def cov(al, s, be, t):
        g = (al[0] + be[0], al[1] + be[1])
        y = (t[0] - s[0], t[1] - s[1])
        v = 1.0
        for gi, yi in zip(g, y):
            v *= (-1) ** gi * he(gi, yi) * math.exp(-yi * yi / 2)
        return (-1) ** (al[0] + al[1]) * v
    M = (-r / 2, 0.0)
    S = (r / 2, 0.0)
    obs = [((0, 0), M), ((1, 0), M), ((0, 1), M), ((0, 0), S), ((1, 0), S), ((0, 1), S)]
    vals = [b, 0, 0, b - k * r ** 3, 0, 0]
    tg = [((0, 2), M), ((0, 2), S), ((2, 0), M), ((2, 0), S), ((1, 1), M), ((1, 1), S)]
    Soo = [[cov(a, s, c, t) for (c, t) in obs] for (a, s) in obs]
    Sto = [[cov(a, s, c, t) for (c, t) in obs] for (a, s) in tg]
    Stt = [[cov(a, s, c, t) for (c, t) in tg] for (a, s) in tg]
    n = 6
    A = [row[:] + [Sto[c][i] for c in range(6)] for i, row in enumerate(Soo)]
    for col in range(n):
        p = max(range(col, n), key=lambda i: abs(A[i][col]))
        A[col], A[p] = A[p], A[col]
        for i in range(col + 1, n):
            f = A[i][col] / A[col][col]
            for j in range(col, 2 * n):
                A[i][j] -= f * A[col][j]
    W = []
    for c in range(6):
        x = [0.0] * n
        for i in reversed(range(n)):
            x[i] = (A[i][n + c] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        W.append(x)
    mu = [sum(W[i][j] * vals[j] for j in range(6)) for i in range(6)]
    C = [[Stt[i][j] - sum(W[i][l] * Sto[j][l] for l in range(6)) for j in range(6)] for i in range(6)]
    return mu, C


def float_mc(r, b, k, n, seed):
    """Monte Carlo of Z_r / r^2 (continuum kernel, floating point)."""
    mu, C = float_conditional(r, b, k)
    # symmetric square root by Jacobi
    A = [row[:] for row in C]
    V = [[float(i == j) for j in range(6)] for i in range(6)]
    for _ in range(60):
        for p in range(5):
            for q in range(p + 1, 6):
                if abs(A[p][q]) < 1e-300:
                    continue
                th = 0.5 * math.atan2(2 * A[p][q], A[q][q] - A[p][p])
                c, s_ = math.cos(th), math.sin(th)
                for kk in range(6):
                    akp, akq = A[kk][p], A[kk][q]
                    A[kk][p], A[kk][q] = c * akp - s_ * akq, s_ * akp + c * akq
                for kk in range(6):
                    apk, aqk = A[p][kk], A[q][kk]
                    A[p][kk], A[q][kk] = c * apk - s_ * aqk, s_ * apk + c * aqk
                for kk in range(6):
                    vkp, vkq = V[kk][p], V[kk][q]
                    V[kk][p], V[kk][q] = c * vkp - s_ * vkq, s_ * vkp + c * vkq
    root = [math.sqrt(max(A[i][i], 0.0)) for i in range(6)]
    Lm = [[sum(V[i][kk] * root[kk] * V[j][kk] for kk in range(6)) for j in range(6)] for i in range(6)]
    rng = random.Random(seed)
    acc = acc2 = 0.0
    for _ in range(n):
        z = [rng.gauss(0, 1) for _ in range(6)]
        h = [mu[i] + sum(Lm[i][j] * z[j] for j in range(6)) for i in range(6)]
        wM, wS, xxM, xxS, xyM, xyS = h
        dM = xxM * wM - xyM ** 2
        dS = xxS * wS - xyS ** 2
        v = abs(dM) * abs(dS) if (xxM < 0 and dM > 0 and dS < 0) else 0.0
        acc += v
        acc2 += v * v
    m = acc / n
    return m / r ** 2, math.sqrt(max(acc2 / n - m * m, 0.0) / n) / r ** 2


def z0_limit(b, k):
    """36 k^2 E[A^2 1{A < 0}], A ~ N(-b, 2) ([LP] (5.4) with the planar contact law A_0 ~ N(-b, 2))."""
    s = math.sqrt(2)
    m = -b
    a = -m / s
    Ph = 0.5 * (1 + math.erf(a / math.sqrt(2)))
    ph = math.exp(-a * a / 2) / math.sqrt(2 * math.pi)
    e = m * m * Ph - 2 * m * s * ph + s * s * (Ph - a * ph)
    return 36 * k * k * e


# ----------------------------------------------------------------------------- driver
def subboxes(band):
    spec = BANDS[band]
    r0, r1 = spec['r']
    n = spec['steps']
    rs = [r0 + (r1 - r0) * i / n for i in range(n + 1)]
    bs = [BAND_B[0] + (BAND_B[1] - BAND_B[0]) * i / B_STEPS for i in range(B_STEPS + 1)]
    ks = [BAND_K[0] + (BAND_K[1] - BAND_K[0]) * i / K_STEPS for i in range(K_STEPS + 1)]
    return rs, bs, ks


def key(r0, r1, b0, b1, k0, k1):
    return 'r=[%s,%s],b=[%s,%s],k=[%s,%s]' % (r0, r1, b0, b1, k0, k1)


def parse_key(kk):
    parts_ = kk.replace('r=[', '').replace('],b=[', ',').replace('],k=[', ',').replace(']', '').split(',')
    return [Fr(x) for x in parts_]


def certify_rband(args):
    band, ir = args
    rs, bs, ks = subboxes(band)
    rband = IV(rs[ir], rs[ir + 1])
    data = band_data(rband, BANDS[band]['L_min'])
    out = {}
    for ib in range(B_STEPS):
        for ik in range(K_STEPS):
            zlo, fl = subbox_floor(data, IV(bs[ib], bs[ib + 1]), IV(ks[ik], ks[ik + 1]))
            out[key(rs[ir], rs[ir + 1], bs[ib], bs[ib + 1], ks[ik], ks[ik + 1])] = {'floor': str(fl), 'floor_float': float(fl)}
    return out


def control_keys(band, table):
    """Deterministic choice of the sub-boxes that receive floating Monte Carlo controls: the band's argmin, a grid of
    (r, b, k) corners, and for each (b, k) corner box in {low, middle, high}^2 the box attaining the minimum floor
    among r <= r_top / 2 and among the whole band (the boxes quoted in NOTE.md section 3)."""
    rs, bs, ks = subboxes(band)
    n = BANDS[band]['steps']
    fl = {kk: Fr(v['floor']) for kk, v in table.items()}
    chosen = {min(fl, key=fl.get)}
    for ir in (0, n // 4, n // 2, 3 * n // 4, n - 1):
        for (ib, ik) in ((0, 0), (B_STEPS - 1, K_STEPS - 1), (B_STEPS // 2, K_STEPS // 2), (0, K_STEPS - 1), (B_STEPS - 1, 0)):
            chosen.add(key(rs[ir], rs[ir + 1], bs[ib], bs[ib + 1], ks[ik], ks[ik + 1]))
    r_top = BANDS[band]['r'][1]
    for b0 in (bs[0], bs[B_STEPS // 2], bs[B_STEPS - 1]):
        for k0 in (ks[0], ks[K_STEPS // 2], ks[K_STEPS - 1]):
            for rmax in (r_top / 2, r_top):
                cand = [kk for kk in fl if (lambda p_: p_[1] <= rmax and p_[2] == b0 and p_[4] == k0)(parse_key(kk))]
                chosen.add(min(cand, key=fl.get))
    return sorted(chosen)


def float_controls(band, table):
    controls = {}
    for kk in control_keys(band, table):
        r0, r1, b0, b1, k0, k1 = parse_key(kk)
        row = {}
        for (r, b, k, tag) in ((r1, b0, k0, 'r1,b0,k0'), (r0, b1, k1, 'r0,b1,k1')):
            m, se = float_mc(float(r), float(b), float(k), 40000, 2026)
            row[tag] = {'r': float(r), 'b': float(b), 'k': float(k), 'mc': m, 'se': se, 'z0': z0_limit(float(b), float(k))}
        controls[kk] = row
    return controls


def replay_sample(band):
    """Sub-boxes replayed exactly by --check: one r-band per 32 (high) or per 18 (low), (b, k) indices stepping."""
    rs, bs, ks = subboxes(band)
    n = BANDS[band]['steps']
    irs = (0, 38, 76, 114, 152, 191) if band == 'high' else (0, 18, 37, 55)
    assert all(ir < n for ir in irs)
    return [key(rs[ir], rs[ir + 1], bs[ib], bs[ib + 1], ks[ik], ks[ik + 1])
            for j, ir in enumerate(irs)
            for (ib, ik) in [((3 * j) % B_STEPS, (5 * j + 2) % K_STEPS)]]


def dec(x, digits=10):
    """Decimal string rounded down."""
    x = Fr(x)
    n = x.numerator * 10 ** digits // x.denominator
    s_ = str(abs(n)).rjust(digits + 1, '0')
    return ('-' if n < 0 else '') + s_[:-digits] + '.' + s_[-digits:]


def band_record(band, table):
    zstar = min(Fr(v['floor']) for v in table.values())
    argmin = min(table, key=lambda kk: Fr(table[kk]['floor']))
    spec = BANDS[band]
    return {'r_range': [str(spec['r'][0]), str(spec['r'][1])], 'r_steps': spec['steps'], 'L_min': spec['L_min'],
            'statement': 'For d = 2, every frame, every torus side L >= %d, every r in [%s, %s], b in [%s, %s], k in [%s, %s]: Z_r / r^2 >= z_star.' % (
                spec['L_min'], spec['r'][0], spec['r'][1], BAND_B[0], BAND_B[1], BAND_K[0], BAND_K[1]),
            'z_star': str(zstar), 'z_star_decimal': dec(zstar), 'argmin': argmin,
            'torus_epsilon_at_rmax': float(torus_epsilon(spec['L_min'], spec['r'][1])), 'torus_epsilon0': float(torus_epsilon(spec['L_min'], Fr(0))),
            'table': table, 'float_controls': float_controls(band, table)}


def combined(res):
    """The combined statement: the weaker L floor of the two bands, the whole r range, the smaller z_star."""
    lo, hi = res['bands']['low'], res['bands']['high']
    z = min(Fr(lo['z_star']), Fr(hi['z_star']))
    return {'L_min': max(lo['L_min'], hi['L_min']), 'r_range': [lo['r_range'][0], hi['r_range'][1]], 'z_star': str(z), 'z_star_decimal': dec(z),
            'statement': 'For d = 2, every frame, every torus side L >= %d, every r in [%s, %s], b in [%s, %s], k in [%s, %s]: Z_r / r^2 >= %s (the high band alone holds for L >= %d).' % (
                max(lo['L_min'], hi['L_min']), lo['r_range'][0], hi['r_range'][1], BAND_B[0], BAND_B[1], BAND_K[0], BAND_K[1], dec(z), hi['L_min'])}


def full_run(procs, bands=None):
    """Certify the listed bands (default: all) and merge them into RESULTS.json (other bands kept)."""
    path = os.path.join(HERE, 'RESULTS.json')
    res = {}
    if os.path.exists(path):
        with open(path) as fh:
            res = json.load(fh)
    res.setdefault('bands', {})
    for band in (bands or BAND_ORDER):
        n = BANDS[band]['steps']
        with multiprocessing.Pool(procs) as pool:
            parts = pool.map(certify_rband, [(band, ir) for ir in range(n)])
        table = {}
        for part in parts:
            table.update(part)
        res['bands'][band] = band_record(band, table)
    res.update({
        'object': 'CL-C8-NORMALIZER-FLOOR-PLANAR-20260930-v1',
        'scientific_effect': 'NONE', 'certified': True, 'kind': 'certified lower bound (exact rational interval arithmetic)',
        'parameters': {'PBITS': PBITS, 'N_EXP': N_EXP, 'Z_MAX': Z_MAX, 'B_STEPS': B_STEPS, 'K_STEPS': K_STEPS,
                       'grid': {k_: (str(v_) if isinstance(v_, Fr) else v_) for k_, v_ in GRID.items()},
                       'bands': {name: {'r_range': [str(v['r'][0]), str(v['r'][1])], 'r_steps': v['steps'], 'L_min': v['L_min']} for name, v in BANDS.items()}},
        'table_note': 'floor = certified lower bound of Z_r / r^2 on the box (exact rational, rounded down to 2^-64); Z_r >= floor * r_lo^2 on the box',
        'mutant': MUT,
    })
    if all(b in res['bands'] for b in BANDS):
        res['combined'] = combined(res)
    return res


def write_results(res):
    with open(os.path.join(HERE, 'RESULTS.json'), 'w') as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
        fh.write('\n')


def load_results():
    path = os.path.join(HERE, 'RESULTS.json')
    require(os.path.exists(path), 'RESULTS.json present')
    with open(path) as fh:
        return json.load(fh)


def check_full(procs, bands=None, rbands=None):
    """Regenerate every sub-box floor of the listed bands (or the r-band indices listed) and compare exactly with
    RESULTS.json; the floating controls are recomputed and compared to 1e-9 relative (platform libm)."""
    ref = load_results()
    n_total = 0
    for band in (bands or BAND_ORDER):
        rec = ref['bands'][band]
        sel = list(range(BANDS[band]['steps'])) if rbands is None else rbands
        with multiprocessing.Pool(procs) as pool:
            parts = pool.map(certify_rband, [(band, ir) for ir in sel])
        n = 0
        for part in parts:
            for kk, v in part.items():
                require(kk in rec['table'], 'sub-box present: %s %s' % (band, kk))
                require(v['floor'] == rec['table'][kk]['floor'], 'exact regeneration of %s %s' % (band, kk))
                n += 1
        n_total += n
        if rbands is None:
            require(n == len(rec['table']) == BANDS[band]['steps'] * B_STEPS * K_STEPS, 'table complete: ' + band)
            zs = min(Fr(v['floor']) for v in rec['table'].values())
            require(str(zs) == rec['z_star'], 'z_star is the minimum of the regenerated table: ' + band)
            controls = float_controls(band, rec['table'])
            require(sorted(controls) == sorted(rec['float_controls']), 'control set: ' + band)
            for kk, row in controls.items():
                for tag, c in row.items():
                    r0 = rec['float_controls'][kk][tag]
                    for name in ('mc', 'se', 'z0'):
                        require(abs(c[name] - r0[name]) <= 1e-9 * max(abs(r0[name]), 1e-300), 'control %s %s %s %s' % (band, kk, tag, name))
    print(json.dumps({'check_full': 'ok', 'sub_boxes_regenerated': n_total, 'bands': bands or list(BAND_ORDER), 'z_star_combined': ref.get('combined', {}).get('z_star_decimal'), 'mutant': MUT}))


def check_run():
    ref = load_results()
    require(sorted(ref['bands']) == sorted(BANDS), 'both bands present')
    for band in BAND_ORDER:
        rec = ref['bands'][band]
        spec = BANDS[band]
        require(rec['L_min'] == spec['L_min'] and rec['r_steps'] == spec['steps'] and rec['r_range'] == [str(spec['r'][0]), str(spec['r'][1])], 'band record matches the code: ' + band)
        require(len(rec['table']) == spec['steps'] * B_STEPS * K_STEPS, 'table size: ' + band)
        # 1. the stored floor is the minimum of the table
        zs = min(Fr(v['floor']) for v in rec['table'].values())
        require(str(zs) == rec['z_star'] and dec(zs) == rec['z_star_decimal'], 'z_star is the minimum of the table: ' + band)
        # 2. exact replay of the argmin sub-box and of sub-boxes spread over the band; the complete regeneration is --check-full
        for kk in [rec['argmin']] + replay_sample(band):
            r0, r1, b0, b1, k0, k1 = parse_key(kk)
            zlo, fl, _ = band_floor(IV(r0, r1), IV(b0, b1), IV(k0, k1), spec['L_min'])
            require(str(fl) == rec['table'][kk]['floor'], 'exact replay of %s %s' % (band, kk))
        # 3. every certified floor lies below its floating Monte Carlo controls (sanity, not proof)
        require(sorted(rec['float_controls']) == control_keys(band, rec['table']), 'control boxes are the deterministic choice: ' + band)
        for kk, row in rec['float_controls'].items():
            v = rec['table'][kk]
            for tag, c in row.items():
                require(Fr(v['floor']) <= Fr(c['mc']) + 5 * Fr(c['se']), 'floor below MC + 5 se at %s %s %s' % (band, kk, tag))
                require(Fr(v['floor']) <= Fr(c['z0']) * Fr(101, 100), 'floor below the r -> 0 limit z_0 at %s %s %s' % (band, kk, tag))
    comb = combined(ref)
    require(comb == ref['combined'], 'combined statement')
    # 4. the preconditioned regression agrees with the direct floating regression at a point band
    # the direct floating regression on the raw pins is ill conditioned (condition number ~ r^-6), so its tolerance
    # is loosened at r = 1/32; the exact preconditioned regression keeps its 1e-6 enclosure width everywhere
    for (r, b, k, tol) in ((Fr(1, 4), Fr(1, 2), Fr(1), 1e-9), (Fr(3, 8), Fr(0), Fr(2), 1e-9), (Fr(1, 32), Fr(1), Fr(1, 2), 1e-5)):
        mu, C = conditional(IV(r), IV(b), IV(k), 12)
        fmu, fC = float_conditional(float(r), float(b), float(k))
        rr = float(r)
        kk_ = float(k)
        # H = A x + shift with x = (wM, om, TM, tau, vM, nu): wS = wM + r om, xxM = r^2 TM - 6 k r, xxS = r^2 TM + r^3 tau + 6 k r, xyM = r vM, xyS = r^2 nu - r vM
        A = [[1, 0, 0, 0, 0, 0], [1, rr, 0, 0, 0, 0], [0, 0, rr * rr, 0, 0, 0], [0, 0, rr * rr, rr ** 3, 0, 0], [0, 0, 0, 0, rr, 0], [0, 0, 0, 0, -rr, rr * rr]]
        shift = [0.0, 0.0, -6 * kk_ * rr, 6 * kk_ * rr, 0.0, 0.0]
        m = [float(v.mid()) for v in mu]
        c = [[float(C[i][j].mid()) for j in range(6)] for i in range(6)]
        hm = [sum(A[i][j] * m[j] for j in range(6)) + shift[i] for i in range(6)]
        hc = [[sum(A[i][a] * c[a][bb] * A[j][bb] for a in range(6) for bb in range(6)) for j in range(6)] for i in range(6)]
        for i in range(6):
            require(abs(hm[i] - fmu[i]) < tol * (1 + abs(fmu[i])), 'mean agreement %d at r=%s' % (i, r))
            for j in range(6):
                require(abs(hc[i][j] - fC[i][j]) < tol * (1 + abs(fC[i][j])), 'covariance agreement %d %d at r=%s' % (i, j, r))
            require(mu[i].width() < Fr(1, 10 ** 6) and C[i][i].width() < Fr(1, 10 ** 6), 'point-band enclosure width')
    # 5. constants
    require(abs(PI.mid() - Fr(3141592653589793, 10 ** 15)) < Fr(1, 10 ** 15) and PI.width() < Fr(1, 10 ** 30), 'pi enclosure')
    require(phi_point(Fr(0)).contains(Fr(1, 2)) and abs(Phi(IV(1)).mid() - Fr(8413447460685429, 10 ** 16)) < Fr(1, 10 ** 15) and Phi(IV(1)).width() < Fr(1, 10 ** 30), 'Phi enclosure')
    require(abs(exp_neg_point(Fr(1)).mid() - Fr(36787944117144233, 10 ** 17)) < Fr(1, 10 ** 15) and exp_neg_point(Fr(1)).width() < Fr(1, 10 ** 30), 'exp enclosure')
    require(abs(SQRT2.mid() * SQRT2.mid() - 2) < Fr(1, 10 ** 40), 'sqrt enclosure')
    print(json.dumps({'check': 'ok', 'z_star_combined': ref['combined']['z_star_decimal'], 'z_star_high': ref['bands']['high']['z_star_decimal'], 'z_star_low': ref['bands']['low']['z_star_decimal'], 'mutant': MUT}))


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--mutant', choices=MUTANTS)
    ap.add_argument('--procs', type=int, default=4)
    ap.add_argument('--quick', action='store_true', help='one sub-box of the high band, print the floor and a Monte Carlo control')
    ap.add_argument('--controls', action='store_true', help='recompute only the floating controls of an existing RESULTS.json')
    ap.add_argument('--check-full', action='store_true', help='regenerate every sub-box of the listed bands and compare exactly with RESULTS.json')
    ap.add_argument('--band', type=str, default=None, help='comma-separated band names (low, high); default all')
    ap.add_argument('--rbands', type=str, default=None, help='with --check-full: comma-separated r-band indices to regenerate instead of all')
    args = ap.parse_args()
    MUT = args.mutant
    bands = None if args.band is None else args.band.split(',')
    if args.check_full:
        check_full(args.procs, bands, None if args.rbands is None else [int(x) for x in args.rbands.split(',')])
        return
    if args.check:
        check_run()
        return
    if args.quick:
        rs, bs, ks = subboxes('high')
        import time
        t0 = time.time()
        zlo, fl, diag = band_floor(IV(rs[0], rs[1]), IV(bs[0], bs[1]), IV(ks[0], ks[1]), BANDS['high']['L_min'])
        print('floor', float(fl), diag, 'time', time.time() - t0)
        print('mc at r1,b0,k0', float_mc(float(rs[1]), float(bs[0]), float(ks[0]), 20000, 1), 'z0', z0_limit(float(bs[0]), float(ks[0])))
        return
    if args.controls:
        res = load_results()
        for band in (bands or BAND_ORDER):
            res['bands'][band]['float_controls'] = float_controls(band, res['bands'][band]['table'])
        write_results(res)
        print(json.dumps({'controls': {band: len(res['bands'][band]['float_controls']) for band in res['bands']}}))
        return
    res = full_run(args.procs, bands)
    write_results(res)
    print(json.dumps({band: (res['bands'][band]['z_star_decimal'], res['bands'][band]['argmin']) for band in res['bands']}))


if __name__ == '__main__':
    main()
