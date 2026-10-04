#!/usr/bin/env python3
"""The cap-failure coefficient of [LP] Theorem A's proof route in every dimension: certified values in d = 3.

Theorem G_d (NOTE.md): for the d-dimensional six-pin law of [LP] and the good event G_r of [LP] section 7 / [CAP] (1)
(partial-block operator norms), Q^W(G_r^c) = c_G^(d)(b, k) r^3 + o(r^3), and for the reference kernel

    c_G^(d)(b, k) = R_d(b) R(b) J^(d)(k),

R_d the hard-direction factor of Math-#184, R the planar factor of Math-#203, J^(d)(k) = (216 k^3)^-1 E[ int_{max(a,c)}^{8M^2}
(s - a)(s - c) ds ] with M = max(12k, 2|v|, ||Omega||_op, ||Y||_op) over the full transverse blocks.

This script (standard library, exact rational interval arithmetic):
  * checks the d = 3 contact law of the jets exactly (rational covariances of the reference kernel);
  * certifies R_3(0) = (32 + 28 sqrt2)/17 and R(0) = 1/(2 sqrt(pi));
  * brackets J^(d)(k) for d = 2, 3 from Gaussian moments and chi-square tails (self-contained), checks that the d = 2
    bracket contains the certified planar J(k) of [G] = Math-#203, and encloses J^(3)(k) by the monotone coupling
    J^(2) <= J^(3) <= J^(2) + tail;
  * evaluates c_G^(3)(0, k); floating R_3(b) R(b) and Monte Carlo J^(3)(k) are recorded as controls.
"""
import argparse
import json
import math
import os
import random
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
MUTANTS = ('no-y-tail', 'r3-one', 'no-bp', 'frob-omega-off')
MUT = None
PBITS = 160
K_GRID = (Fr(1, 2), Fr(3, 4), Fr(1), Fr(3, 2), Fr(2))
# [G] Math-#203 at a388580, RESULTS.json (git blob e3a8e25a49fb572f0e3fb95c88f070ef9fa9d731): certified planar J(k)
JG = {Fr(1, 2): ('301744.4364470241', '301744.4616663935'),
      Fr(3, 4): ('995454.6123240485', '995454.6129283207'),
      Fr(1): ('2359292.9611053703', '2359292.9611122569'),
      Fr(3, 2): ('7962621.6645357431', '7962621.6645378716'),
      Fr(2): ('18874366.3403946311', '18874366.3403964820')}


def require(cond, msg):
    if not cond:
        print(json.dumps({'check': 'FAIL', 'reason': msg, 'mutant': MUT}))
        sys.exit(1)


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
    """Enclosure of exp(-t) for a rational t >= 0: halve t to t <= 1/2, evaluate the alternating series in fixed point
    (ulp = 2^-(PBITS+40)) with an integer bound on the accumulated rounding error, then square back."""
    t = Fr(t)
    m = 0
    while t > Fr(1, 2):
        t /= 2
        m += 1
    P2 = PBITS + 40
    ONE = 1 << P2
    X = t.numerator * ONE // t.denominator            # X / ONE <= t < (X + 1) / ONE
    # series at x_lo = X / ONE: exp(-x_lo) = sum (-1)^n x_lo^n / n!  (alternating, terms decreasing for x_lo <= 1/2)
    S = ONE
    T = ONE
    E = 0                                             # error bound of T in ulps
    Etot = 0
    n = 0
    while T > 0:
        n += 1
        T = (T * X) // (ONE * n)
        E = (E * X) // (ONE * n) + 2
        S += (-1) ** n * T
        Etot += E
    Etot += E + 1                                     # first omitted exact term is below (T_n + E) <= E + 1 ulps
    # exp(-t) in [exp(-(X + 1)/ONE), exp(-X/ONE)] and exp(-(X + 1)/ONE) >= exp(-X/ONE) - 1/ONE (Lipschitz 1)
    v = IV(Fr(S - Etot - 1, ONE), Fr(S + Etot, ONE))
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
    """Phi on an interval (monotone); arguments clipped to [-12, 12] (clipping only widens)."""
    lo = min(max(x.lo, Fr(-12)), Fr(12))
    hi = max(min(x.hi, Fr(12)), Fr(-12))
    if x.lo < -12:
        plo = Fr(0)
    else:
        plo = phi_point(lo).lo
    if x.hi > 12:
        phi_ = Fr(1)
    else:
        phi_ = phi_point(hi).hi
    return IV(plo, phi_)


# ----------------------------------------------------------------------------- exact contact law in d = 3 (reference kernel)
def _h(n):
    return 0 if n % 2 else (-1) ** (n // 2) * math.prod(range(n - 1, 0, -2))


def _cov(a, b):
    """E[d^a f(0) d^b f(0)] = (-1)^|b| d^(a+b) exp(-|z|^2/2) at 0."""
    return Fr((-1) ** sum(b) * math.prod(_h(x + y) for x, y in zip(a, b)))


PINS3 = ((0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (1, 0, 1))   # contact jet [LP] (3.4)
JETS3 = {'f_xxy1': (2, 1, 0), 'f_xxy2': (2, 0, 1), 'O11': (1, 2, 0), 'O12': (1, 1, 1), 'O22': (1, 0, 2),
         'T111': (0, 3, 0), 'T112': (0, 2, 1), 'T122': (0, 1, 2), 'T222': (0, 0, 3),
         'A11': (0, 2, 0), 'A12': (0, 1, 1), 'A22': (0, 0, 2)}
CLAIM3 = {'f_xxy1': 2, 'f_xxy2': 2, 'O11': 2, 'O12': 1, 'O22': 2, 'T111': 6, 'T112': 2, 'T122': 2, 'T222': 6,
          'A11': 2, 'A12': 1, 'A22': 2}


def _solve(M, rhs):
    n = len(M)
    A = [row[:] + [x] for row, x in zip(M, rhs)]
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c] != 0)
        A[c], A[p] = A[p], A[c]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c] / A[c][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [A[i][n] / A[i][i] for i in range(n)]


def contact_law_3():
    """Conditional law of the jets at 0 given the contact pins (f, f_x, f_xx, f_xxx, f_y1, f_xy1, f_y2, f_xy2) = (b, 0, 0,
    12k, 0, 0, 0, 0): returns (means as linear forms in (b, k), conditional covariance), exact rationals."""
    S = [[_cov(p, q) for q in PINS3] for p in PINS3]
    names = list(JETS3)
    W = {n: _solve(S, [_cov(JETS3[n], q) for q in PINS3]) for n in names}
    mean = {n: (W[n][0], 12 * W[n][3]) for n in names}          # coefficient of b and of k
    C = {(m, n): _cov(JETS3[m], JETS3[n]) - sum(W[m][i] * _cov(JETS3[n], PINS3[i]) for i in range(len(PINS3)))
         for m in names for n in names}
    return mean, C


def check_contact_law():
    mean, C = contact_law_3()
    for n in JETS3:
        want_b = Fr(-1) if n in ('A11', 'A22') else Fr(0)
        require(mean[n] == (want_b, Fr(0)), 'contact mean of ' + n)
        require(C[(n, n)] == CLAIM3[n], 'contact variance of ' + n)
    for m in JETS3:
        for n in JETS3:
            require(m == n or C[(m, n)] == 0, 'contact covariance %s, %s' % (m, n))
    return True


# ----------------------------------------------------------------------------- Gaussian and chi-square moments (intervals)
SQRTPI = isqrt_iv(PI)


def dfact(n):
    return math.prod(range(n, 0, -2)) if n > 0 else 1


def e_abs_std(n):
    """E|Z|^n, Z ~ N(0,1)."""
    if n % 2 == 0:
        return IV(dfact(n - 1))
    return IV(dfact(n - 1)) * SQRT2 / SQRTPI


def e_v1(j):
    """E[v1^(2j)], v1 ~ N(0, 1/2)."""
    return Fr(dfact(2 * j - 1), 2 ** j)


def e_om(n):
    """E|Omega11|^n, Omega11 ~ N(0, 2)."""
    s = IV(2 ** (n // 2)) * (SQRT2 if n % 2 else IV(1))
    return s * e_abs_std(n)


def e_Q(j, k):
    """E[Q^j], Q = 2 v1^2 + 6k |Omega11| (independent factors)."""
    tot = IV(0)
    for l in range(j + 1):
        tot = tot + IV(math.comb(j, l) * 2 ** l * e_v1(l) * (6 * k) ** (j - l)) * e_om(j - l)
    return tot


def gamma_half(two_s):
    """Gamma(s) for s = two_s / 2 > 0 an integer or half-integer, as (rational, uses_sqrt_pi)."""
    if two_s % 2 == 0:
        return Fr(math.factorial(two_s // 2 - 1)), False
    n = two_s // 2                                         # s = n + 1/2
    return Fr(math.factorial(2 * n), 4 ** n * math.factorial(n)), True


def chi_tail(nu, sigma2, p, t):
    """Upper bound (interval) of E[Z^p 1{Z > t}] for Z^2 = sigma2 * chi2_nu, t > 0 rational, p >= 0 integer."""
    t = Fr(t)
    y0 = t * t / sigma2                                   # Y = chi2_nu > y0
    x = y0 / 2
    two_s = nu + p                                         # s = nu/2 + p/2
    g_s, pi_s = gamma_half(two_s)
    g_n, pi_n = gamma_half(nu)
    ratio = IV(g_s / g_n)
    if pi_s and not pi_n:
        ratio = ratio * SQRTPI
    elif pi_n and not pi_s:
        ratio = ratio / SQRTPI
    # regularized upper incomplete gamma Q(s, x)
    if two_s % 2 == 0:
        n = two_s // 2
        Q = exp_neg(IV(x)) * IV(sum(x ** j / math.factorial(j) for j in range(n)))
    else:
        n = two_s // 2                                     # s = n + 1/2
        sx = isqrt_iv(IV(x)) if x > 0 else IV(0)
        erfc = 2 * (1 - Phi(IV(t) / isqrt_iv(IV(sigma2))))   # erfc(sqrt x) = 2 Phibar(t / sigma)
        acc = IV(0)
        for j in range(n):
            g, _ = gamma_half(2 * j + 3)                   # Gamma(j + 3/2) = g sqrt(pi)
            acc = acc + IV(x ** j) * sx / (IV(g) * SQRTPI)
        Q = erfc + exp_neg(IV(x)) * acc
    sig_p = IV(sigma2 ** (p // 2)) * (isqrt_iv(IV(sigma2)) if p % 2 else IV(1))
    two_q = IV(2 ** (p // 2)) * (SQRT2 if p % 2 else IV(1))     # 2^(p/2)
    val = sig_p * two_q * ratio * Q
    return IV(0, val.hi)


# ----------------------------------------------------------------------------- the bracket of J^(d)(k)
LAWS = {2: {'v': (1, 2), 'om': (1, 2), 'Y': (1, 6)},      # (nu, sigma2): Z_v = 2|v1|, Z_Om = |Omega11|, Z_Y = |T111|
        3: {'v': (2, 2), 'om': (3, 2), 'Y': (4, 6)}}      # Z_v = 2||v||, Z_Om = ||Omega||_F, Z_Y = weighted Frobenius


def tail_hi(d, k):
    """Upper bound of T^(d)(k) = E[(P(8M^2) - P(1152 k^2)) 1{X > 12k}] (NOTE section 3), via
    E[(512/3 Zbar^6 + 64 Q Zbar^4 + 8 Q^2 Zbar^2) 1{Zbar > t}] <= sum over the three blocks."""
    t = 12 * k
    law = LAWS[d]
    tot = IV(0)
    coef = {0: Fr(512, 3), 1: Fr(64), 2: Fr(8)}           # coefficient of Q^j Z^(6 - 2j)
    for j in (0, 1, 2):
        p = 6 - 2 * j
        # block Y: independent of Q
        if MUT != 'no-y-tail':
            nu, s2 = law['Y']
            tot = tot + IV(coef[j]) * e_Q(j, k) * chi_tail(nu, s2, p, t)
        # block Omega: Q <= 2 v1^2 + 6k Z_Om
        nu, s2 = law['om']
        if MUT == 'frob-omega-off' and d == 3:
            nu = 1                                         # wrong: |Omega11| does not dominate ||Omega||_op
        for l in range(j + 1):
            tot = tot + IV(coef[j] * math.comb(j, l) * 2 ** l * e_v1(l) * (6 * k) ** (j - l)) * chi_tail(nu, s2, p + j - l, t)
        # block v: Q <= Z_v^2 / 2 + 6k |Omega11|
        nu, s2 = law['v']
        for l in range(j + 1):
            tot = tot + IV(coef[j] * math.comb(j, l) * Fr(1, 2 ** l) * (6 * k) ** (j - l)) * e_om(j - l) * chi_tail(nu, s2, p + 2 * l, t)
    return tot.hi


def J_bracket(d, k):
    """Self-contained bracket of J^(d)(k):  216 k^3 J = 512 t^6/3 - 6 t^2 - E[P(m0)] + T,  t = 12k,
    |E[P(m0)]| <= B_P = 2 E[Q^3],  -2 E[Q^6] / (8 t^2)^3 <= T <= tail_hi."""
    k = Fr(k)
    t = 12 * k
    base = Fr(512) * t ** 6 / 3 - 6 * t ** 2
    bp = (2 * e_Q(3, k)).hi
    if MUT == 'no-bp':
        bp = Fr(0)
    tlo = (2 * e_Q(6, k)).hi / (8 * t * t) ** 3
    thi = tail_hi(d, k)
    den = 216 * k ** 3
    return IV((base - bp - tlo) / den, (base + bp + thi) / den), {'B_P': bp, 'T_lo': tlo, 'T_hi': thi}


def J3_from_G(k):
    """Monotone coupling: J^(2)(k) <= J^(3)(k) <= J^(2)(k) + tail_hi(3, k) / (216 k^3), with J^(2) from [G]."""
    lo, hi = (Fr(x) for x in JG[k])
    return IV(lo, hi + tail_hi(3, k) / (216 * k ** 3))


def R3_0():
    """R_3(0) = N_3(0) m_(2,0) / m_(3,0) = 2 sqrt2 / ((7 - 4 sqrt2)/2) = (32 + 28 sqrt2)/17 (NOTE section 2)."""
    if MUT == 'r3-one':
        return IV(1)
    return (32 + 28 * SQRT2) / 17


R_0 = 1 / (2 * SQRTPI)                                     # R(0) = phi_2(0) / m_(2,0) = (1/(2 sqrt pi)) / 1


def m3_0_polar():
    """m_(3,0) = (1/(4 sqrt(2 pi))) * int rho^6 e^(-rho^2/4) drho * int_{pi/4}^{pi/2} c^2 s^2 (s - c) dtheta
    = (30/sqrt2) * (7/(30 sqrt2) - 2/15) = (7 - 4 sqrt2)/2 (NOTE section 2): returns both sides."""
    lhs = IV(30) / SQRT2 * (IV(7) / (30 * SQRT2) - Fr(2, 15))
    rhs = (7 - 4 * SQRT2) / 2
    return lhs, rhs


# ----------------------------------------------------------------------------- floating controls (not part of the certificate)
def _Phi_f(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _phi_f(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def r3r_float(b, n=4000, top=14.0):
    """Floating R_3(b) R(b) = phi_2(b) N_3(b) / m_(3,b), and R_3(b) = N_3(b) m_(2,b) / m_(3,b):
    N_3(b) = sqrt(pi/2) E[X_+^3], X ~ N(b, 2); m_(3,b) = E[((b + t)^2 - rho^2)^2 1{b + t > rho}], t ~ N(0,1), rho Rayleigh(1)."""
    s = math.sqrt(2)
    mu = b
    ex3 = (mu ** 3 + 3 * mu * s * s) * _Phi_f(mu / s) + s * (mu * mu + 2 * s * s) * _phi_f(mu / s)
    N3 = math.sqrt(math.pi / 2) * ex3
    m2 = (2 + b * b) * _Phi_f(b / s) + s * b * _phi_f(b / s)

    def inner(rho):                                         # int_rho^inf (u^2 - rho^2)^2 phi(u - b) du
        z = rho - b
        P0 = 1 - _Phi_f(z)
        ph = _phi_f(z)
        # moments of u = b + x over x > z: E[x^j 1{x > z}] for x ~ N(0,1)
        m = [P0, ph]
        for j in range(2, 5):
            m.append(z ** (j - 1) * ph + (j - 1) * m[j - 2])
        U = lambda p: sum(math.comb(p, j) * b ** (p - j) * m[j] for j in range(p + 1))
        return U(4) - 2 * rho * rho * U(2) + rho ** 4 * U(0)
    h = top / n
    acc = 0.0
    for i in range(n + 1):
        rho = i * h
        w = 1 if i in (0, n) else (4 if i % 2 else 2)
        acc += w * rho * math.exp(-rho * rho / 2) * inner(rho)
    m3 = acc * h / 3
    phi2 = math.exp(-b * b / 4) / (2 * math.sqrt(math.pi))
    return {'b': b, 'N3': N3, 'm2': m2, 'm3': m3, 'R3': N3 * m2 / m3, 'R': phi2 / m2, 'R3R': phi2 * N3 / m3}


def _ynorm(T111, T112, T122, T222, n=64):
    best, bt = 0.0, 0.0
    for i in range(n):
        th = math.pi * i / n
        c, s = math.cos(th), math.sin(th)
        y = abs(T111 * c ** 3 + 3 * T112 * c * c * s + 3 * T122 * c * s * s + T222 * s ** 3)
        if y > best:
            best, bt = y, th
    f = lambda th: abs(T111 * math.cos(th) ** 3 + 3 * T112 * math.cos(th) ** 2 * math.sin(th)
                       + 3 * T122 * math.cos(th) * math.sin(th) ** 2 + T222 * math.sin(th) ** 3)
    lo, hi = bt - math.pi / n, bt + math.pi / n
    g = (math.sqrt(5) - 1) / 2
    for _ in range(40):
        a, c = hi - g * (hi - lo), lo + g * (hi - lo)
        if f(a) > f(c):
            hi = c
        else:
            lo = a
    return max(best, f((lo + hi) / 2))


def mc_J(d, k, n, seed):
    """Monte Carlo of J^(d)(k) (floating): v ~ N(0, I/2), Omega GOE(1), Y with T111, T222 ~ N(0,6), T112, T122 ~ N(0,2);
    for d = 2 only the first components enter M."""
    rng = random.Random(seed)
    tot = tot2 = 0.0
    k = float(k)
    for _ in range(n):
        v1, v2 = rng.gauss(0, math.sqrt(0.5)), rng.gauss(0, math.sqrt(0.5))
        o11, o22, o12 = rng.gauss(0, math.sqrt(2)), rng.gauss(0, math.sqrt(2)), rng.gauss(0, 1)
        T111, T222 = rng.gauss(0, math.sqrt(6)), rng.gauss(0, math.sqrt(6))
        T112, T122 = rng.gauss(0, math.sqrt(2)), rng.gauss(0, math.sqrt(2))
        if d == 3:
            vn = math.hypot(v1, v2)
            tr, df = (o11 + o22) / 2, math.hypot((o11 - o22) / 2, o12)
            on = max(abs(tr + df), abs(tr - df))
            yn = _ynorm(T111, T112, T122, T222)
        else:
            vn, on, yn = abs(v1), abs(o11), abs(T111)
        M = max(12 * k, 2 * vn, on, yn)
        a, c = v1 * v1, 6 * k * o11 - v1 * v1
        m0, S = max(a, c), 8 * M * M
        P = lambda s: s ** 3 / 3 - (a + c) * s * s / 2 + a * c * s
        x = (P(S) - P(m0)) / (216 * k ** 3)
        tot += x
        tot2 += x * x
    m = tot / n
    return {'d': d, 'k': str(Fr(k).limit_denominator(64)), 'n': n, 'seed': seed, 'J': m, 'se': math.sqrt(max(tot2 / n - m * m, 0) / n),
            'J_over_2359296k3': m / (2359296 * k ** 3)}


# ----------------------------------------------------------------------------- certified record, check, main
def dec_down(x, places):
    x = Fr(x)
    n = (x.numerator * 10 ** places) // x.denominator
    s = str(abs(n)).rjust(places + 1, '0')
    return ('-' if n < 0 else '') + s[:-places] + '.' + s[-places:]


def dec_up(x, places):
    x = Fr(x)
    n = -((-x.numerator * 10 ** places) // x.denominator)
    s = str(abs(n)).rjust(places + 1, '0')
    return ('-' if n < 0 else '') + s[:-places] + '.' + s[-places:]


def iv_str(x, places=10):
    return [dec_down(x.lo, places), dec_up(x.hi, places)]


def certified():
    check_contact_law()
    lhs, rhs = m3_0_polar()
    require(abs(lhs.mid() - rhs.mid()) < Fr(1, 10 ** 40), 'm_(3,0) closed form')
    r3 = R3_0()
    out = {'contact_law_d3': 'verified exactly (rational covariances)', 'm3_0': iv_str(rhs, 20), 'R3_0': iv_str(r3, 20),
           'R_0': iv_str(R_0, 20), 'J': {}, 'J3_from_G': {}, 'cG3_0': {}, 'G_containment': {}}
    for d in (2, 3):
        out['J'][str(d)] = {}
        for k in K_GRID:
            br, parts = J_bracket(d, k)
            out['J'][str(d)][str(k)] = {'bracket': iv_str(br, 6), 'B_P': dec_up(parts['B_P'], 6),
                                        'T_hi': dec_up(parts['T_hi'], 6), 'T_lo': dec_up(parts['T_lo'], 12)}
            if d == 2:
                g_lo, g_hi = (Fr(x) for x in JG[k])
                ok = br.lo <= g_lo and g_hi <= br.hi
                require(ok or MUT is not None, 'planar bracket does not contain [G] at k = %s' % k)
                out['G_containment'][str(k)] = ok
    for k in K_GRID:
        j3 = J3_from_G(k)
        out['J3_from_G'][str(k)] = iv_str(j3, 10)
        out['cG3_0'][str(k)] = iv_str(R3_0() * R_0 * j3, 6)
    return out


def write_results(res):
    with open(os.path.join(HERE, 'RESULTS.json'), 'w') as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
        fh.write('\n')


def load_results():
    with open(os.path.join(HERE, 'RESULTS.json')) as fh:
        return json.load(fh)


MC_PLAN = [(d, k, 200000, seed) for d in (2, 3) for k in (Fr(1, 6), Fr(1, 2), Fr(3, 4)) for seed in (1, 2)]


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--mutant', choices=MUTANTS)
    ap.add_argument('--controls', action='store_true', help='recompute the floating controls (slow)')
    ap.add_argument('--procs', type=int, default=4)
    args = ap.parse_args()
    MUT = args.mutant
    if args.check:
        ref = load_results()
        cur = certified()
        require(cur == ref['certified'], 'certified values differ from RESULTS.json')
        require(ref['mutant'] is None, 'RESULTS.json produced under a mutant')
        # floating controls recorded: d = 3 Monte Carlo inside the certified enclosures where they are informative
        for row in ref['controls']['mc']:
            k = Fr(row['k'])
            if row['d'] == 3 and k in (Fr(3, 4),):
                lo, hi = (float(Fr(x)) for x in ref['certified']['J3_from_G'][str(k)])
                require(lo - 5 * row['se'] <= row['J'] <= hi + 5 * row['se'], 'MC control outside the enclosure')
        print(json.dumps({'check': 'ok', 'cG3_0': cur['cG3_0'], 'mutant': MUT}))
        return
    res = {'schema': 1, 'object': 'CL-C8-CAP-FAILURE-COEFFICIENT-DIMS-20261001-v1', 'scientific_effect': 'NONE',
           'certified': certified(), 'mutant': MUT}
    if args.controls:
        import multiprocessing
        with multiprocessing.Pool(args.procs) as pool:
            mc = pool.starmap(mc_J, MC_PLAN)
        res['controls'] = {'r3r_float': [r3r_float(b) for b in (0.0, 0.25, 0.5, 0.75, 1.0)], 'mc': mc}
    else:
        res['controls'] = load_results()['controls']
    write_results(res)
    print(json.dumps(res['certified']['cG3_0']))


if __name__ == '__main__':
    main()
