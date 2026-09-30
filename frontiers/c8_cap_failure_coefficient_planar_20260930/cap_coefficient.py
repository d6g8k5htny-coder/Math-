#!/usr/bin/env python3
"""Exact leading coefficient of the cap-failure probability of [LP] Theorem A in the plane.

G_r = {lambda_min(-A_M) > (4/(3k)) r M_3^2, r M_4 <= 3k/10} is the good event of [LP] section 7 / [CAP] (1), with M_3, M_4 the
partial-block derivative norms on the cylinder D = [-2r, 2r] x [-2r, 2r] and Q^W = W_r Q / Z_r the typed pair law.  NOTE.md
Theorem G:  Q^W(G_r^c) = c_G(b, k) r^3 + o(r^3),  c_G = R(b) J(k),

    R(b) = p_w(0) / E[w^2 1{w < 0}],  w ~ N(-b, 2)  (closed form in Phi, phi),
    J(k) = (216 k^3)^(-1) E[ integral_{max(a, c)}^{8 M^2} (s - a)(s - c) ds ],
    a = v^2,  c = 6k om - v^2,  M = max(12k, 2|v|, |om|, |Y|),  v ~ N(0, 1/2), om ~ N(0, 2), Y ~ N(0, 6) independent

(the contact jets -f_xxy/2, f_xyy, f_yyy at the pins' midpoint given the six pins, reference kernel).  By symmetry in om the
expectation reduces to three one-dimensional integrals (NOTE.md section 3):

    216 k^3 J(k) = (512/3) I1 - 8 I2 - I3,
    I1 = E[M^6],   I2 = E[v^4 M^2],   I3 = E[F(max(a, c))],   F(s) = s^3/3 - (a + c) s^2/2 + a c s.

Certification: exact rational interval arithmetic (outward rounding to 2^-160; exp by alternating series, pi by Machin,
Phi by a fixed-point series with an integer rounding budget); each one-dimensional integral by cells with the mean-value
enclosure  integral_cell f  in  h f(mid) +- (h^2/8) width(f'(cell)),  f' from forward-mode interval differentiation, and
closed-form Gaussian tails.  Standard library only; deterministic.  The interval toolkit is the one of
frontiers/c8_normalizer_floor_planar_20260930/floor.py (Math-#195).
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
MUTANTS = ('no-third-jet', 'sign-lo', 'variance-yyy')
MUT = None
PBITS = 160
K_GRID = (Fr(1, 6), Fr(1, 2), Fr(3, 4), Fr(1), Fr(3, 2), Fr(2))
B_GRID = (Fr(0), Fr(1, 4), Fr(1, 2), Fr(3, 4), Fr(1), Fr(6, 5))
CELL = Fr(1, 512)        # cell width of the certified quadratures
T_SPAN = Fr(30)          # integrate t on [12k, 12k + T_SPAN]; the rest is a closed-form tail
V_MAX = Fr(8)            # integrate v on [0, V_MAX]; the rest is a closed-form tail
LEAD = 2359296           # J(k) ~ LEAD k^3 = (512/3)(12k)^6 / (216 k^3): the pinned f_xxx forces M >= 12k


def require(cond, msg):
    if not cond:
        print(json.dumps({'check': 'FAIL', 'reason': msg, 'mutant': MUT}))
        sys.exit(1)


# ----------------------------------------------------------------------------- rational intervals (from floor.py, Math-#195)
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


def phi_iv(x):
    """Standard normal density on an interval (via exp(-x^2/2) monotone in x^2)."""
    return exp_neg(x.sq() * Fr(1, 2)) / SQRT2PI


# ----------------------------------------------------------------------------- forward-mode interval differentiation
class DV:
    """Pair (value interval, derivative interval) of a function of one real variable, both rigorous on a cell."""
    __slots__ = ('v', 'd')

    def __init__(self, v, d):
        self.v = v if isinstance(v, IV) else IV(v)
        self.d = d if isinstance(d, IV) else IV(d)

    @staticmethod
    def var(x):
        return DV(x, IV(1))

    @staticmethod
    def const(c):
        return DV(c, IV(0))

    def __add__(self, o):
        o = o if isinstance(o, DV) else DV.const(o)
        return DV(self.v + o.v, self.d + o.d)
    __radd__ = __add__

    def __neg__(self):
        return DV(-self.v, -self.d)

    def __sub__(self, o):
        return self + (-(o if isinstance(o, DV) else DV.const(o)))

    def __rsub__(self, o):
        return DV.const(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, DV) else DV.const(o)
        return DV(self.v * o.v, self.d * o.v + self.v * o.d)
    __rmul__ = __mul__

    def scale(self, c):
        c = Fr(c)
        return DV(self.v * c, self.d * c)

    def sq(self):
        return DV(self.v.sq(), self.d * self.v * 2)

    def pow(self, n):
        out = DV.const(1)
        for _ in range(n):
            out = out * self
        return out


def Phi_dv(x):
    """Phi(x) with derivative phi(x) x'."""
    return DV(Phi(x.v), phi_iv(x.v) * x.d)


def phi_dv(x):
    """phi(x) with derivative -x phi(x) x'."""
    p = phi_iv(x.v)
    return DV(p, -(x.v * p) * x.d)


def upper_moment(j, x):
    """M_j(x) = integral_x^infinity u^j phi(u) du (x >= 0), as DV in x (derivative -x^j phi(x) x'); by the recursion
    M_0 = 1 - Phi, M_1 = phi, M_j = x^(j-1) phi(x) + (j - 1) M_(j-2)."""
    p = phi_iv(x.v)
    P = Phi(x.v)
    vals = [IV(1) - P, p]
    for m in range(2, j + 1):
        xp = IV(x.v.lo ** (m - 1), x.v.hi ** (m - 1))
        vals.append(xp * p + vals[m - 2] * (m - 1))
    xj = IV(x.v.lo ** j, x.v.hi ** j) if j > 0 else IV(1)
    return DV(vals[j], -(xj * p) * x.d)


def abs_moment_between(j, sigma2, lo, hi):
    """E[|X|^j 1{lo < |X| < hi}] for X ~ N(0, sigma2), lo, hi DV in the integration variable (0 <= lo <= hi)."""
    sig = isqrt_iv(IV(sigma2))
    sigj = IV(sig.lo ** j, sig.hi ** j)
    inv = sig.inv()
    a = DV(lo.v * inv, lo.d * inv)
    b = DV(hi.v * inv, hi.d * inv)
    return (upper_moment(j, a) - upper_moment(j, b)) * DV.const(sigj * 2)


def abs_moment_tail(j, sigma2, lo):
    """E[|X|^j 1{|X| > lo}] for X ~ N(0, sigma2), lo rational >= 0 (interval)."""
    sig = isqrt_iv(IV(sigma2))
    sigj = IV(sig.lo ** j, sig.hi ** j)
    return upper_moment(j, DV.const(IV(lo) * sig.inv())).v * sigj * 2


# ----------------------------------------------------------------------------- certified one-dimensional quadrature
def integrate(f, a, b, h, nf=1):
    """Enclosures of integral_a^b f_i for f: DV -> (DV, ..., DV) (nf components, rigorous on intervals), by cells of
    width h with the mean-value enclosure  integral_cell f_i in h f_i(mid) +- (h^2 / 8) width(f_i'(cell))  (pair t and
    2 mid - t: f(t) + f(2 mid - t) - 2 f(mid) = (t - mid)(f'(xi_1) - f'(xi_2)) is bounded by |t - mid| width(f'(cell)))."""
    a, b, h = Fr(a), Fr(b), Fr(h)
    n = int(math.ceil((b - a) / h))
    tot = [IV(0) for _ in range(nf)]
    t0 = a
    for i in range(n):
        t1 = min(b, a + (i + 1) * h)
        w = t1 - t0
        mid = (t0 + t1) / 2
        fm = f(DV.var(IV(mid)))
        cell = f(DV.var(IV(t0, t1)))
        for j in range(nf):
            err = cell[j].d.width() * w * w / 8
            tot[j] = tot[j] + fm[j].v * w + IV(-err, err)
        t0 = t1
    return tot


# ----------------------------------------------------------------------------- the model
SIG2_V = Fr(1, 2)       # v = -f_xxy(0)/2
SIG2_OM = Fr(2)         # om = f_xyy(0)
SIG2_Y = Fr(6)          # Y = f_yyy(0)
SIG2_2V = Fr(2)         # 2|v| has the law of |N(0, 2)|, as |om|


def sig2_y():
    return Fr(2) if MUT == 'variance-yyy' else SIG2_Y


def F_abs(t, sigma2):
    """P(|N(0, sigma2)| <= t) = 2 Phi(t / sigma) - 1 as DV."""
    inv = isqrt_iv(IV(sigma2)).inv()
    return Phi_dv(DV(t.v * inv, t.d * inv)).scale(2) - 1


def F3(t):
    if MUT == 'no-third-jet':
        return DV.const(1)
    return F_abs(t, sig2_y())


def tail_t5(T):
    """integral_T^infinity 6 t^5 (1 - F1(t)^2 F3(t)) dt <= sum over the union bound 2(1 - F1) + (1 - F3), each
    integral_T^inf 6 t^5 2(1 - Phi(t/sigma)) dt <= 12 (sigma^6 / 6) M_6(T / sigma)."""
    tot = IV(0)
    for mult, s2 in ((2, SIG2_2V), (1, sig2_y())):
        if MUT == 'no-third-jet' and s2 == sig2_y():
            continue
        sig = isqrt_iv(IV(s2))
        tot = tot + upper_moment(6, DV.const(IV(T) * sig.inv())).v * IV(sig.lo ** 6, sig.hi ** 6) * (2 * mult)
    return IV(0, tot.hi)


def tail_t1(T):
    """integral_T^infinity 2 t (1 - F1(t) F3(t)) dt <= sum_i integral_T^inf 2 t 2(1 - Phi(t/sigma_i)) dt <= sum_i 2 sigma_i^2 M_2(T/sigma_i)."""
    tot = IV(0)
    for s2 in (SIG2_2V, sig2_y()):
        if MUT == 'no-third-jet' and s2 == sig2_y():
            continue
        sig = isqrt_iv(IV(s2))
        tot = tot + upper_moment(2, DV.const(IV(T) * sig.inv())).v * sig.sq() * 2
    return IV(0, tot.hi)


def certify_k(k):
    """Enclosures of I1, I2, I3 and J(k) at a rational k > 0."""
    k = Fr(k)
    m = 12 * k
    T = m + T_SPAN
    six_k = 6 * k

    def F1(t):
        return F_abs(t, SIG2_2V)

    # one pass over t in [m, T] for the three t-integrands
    #   f1 = 6 t^5 (1 - F1^2 F3)                   -> I1 = E[M^6] = m^6 + integral_m^inf f1
    #   h1 = 2 t (1 - F1 F3)                       -> H = E[max(m, |om|, |Y|)^2] = m^2 + integral_m^inf h1
    #   f2 = h1 E[v^4 1{6k < |v| < t/2}]           -> the t-integral in I2 = E[v^4 M^2]
    def fv(t):
        a1 = F1(t)
        a3 = F3(t)
        f1 = t.pow(5).scale(6) * (1 - a1.sq() * a3)
        h1 = t.scale(2) * (1 - a1 * a3)
        B = abs_moment_between(4, SIG2_V, DV.const(six_k), t.scale(Fr(1, 2)))
        return (f1, h1, h1 * B)
    q1, qh, q2 = integrate(fv, m, T, CELL, 3)
    I1 = IV(m ** 6) + q1 + tail_t5(T)
    H = IV(m * m) + qh + tail_t1(T)
    # I2 = E[v^4 M^2] = H E[v^4 1{|v| <= 6k}] + 4 E[v^6 1{|v| > 6k}] + integral_m^inf 2t (1 - F1 F3) E[v^4 1{6k < |v| < t/2}] dt
    Ev4_in = abs_moment_between(4, SIG2_V, DV.const(0), DV.const(six_k)).v
    Ev6_out = abs_moment_tail(6, SIG2_V, six_k)
    Ev4 = IV(3 * SIG2_V * SIG2_V)     # E v^4 = 3 sigma^4 = 3/4
    I2 = H * Ev4_in + Ev6_out * 4 + q2 + tail_t1(T) * Ev4

    # I3 = E[F(max(a, c))], F(max) = -a^3/6 + a^2 c/2 on {c <= a} (om <= v^2/(3k)), = -c^3/6 + a c^2/2 on {c > a}
    sig_om = isqrt_iv(IV(SIG2_OM))
    sig_v = isqrt_iv(IV(SIG2_V))
    inv_sv = sig_v.inv()

    def G(v):
        # om-expectations at threshold theta = v^2/(3k): u = theta / sigma_om
        theta = v.sq().scale(1 / (3 * k))
        u = DV(theta.v * sig_om.inv(), theta.d * sig_om.inv())
        P = Phi_dv(u)
        p = phi_dv(u)
        E0le = P
        E1le = -(p * DV.const(sig_om))
        E0gt = 1 - P
        E1gt = p * DV.const(sig_om)
        E2gt = (u * p + 1 - P) * DV.const(sig_om.sq())
        E3gt = (u.sq() * p + p.scale(2)) * DV.const(sig_om.sq() * sig_om)
        v2 = v.sq()
        v4 = v2.sq()
        v6 = v4 * v2
        piece1 = -(v6 * E0le).scale(Fr(2, 3)) + (v4 * E1le).scale(3 * k)
        # c = 6k om - v^2:  c^2 = 36k^2 om^2 - 12k v^2 om + v^4 ;  c^3 = 216k^3 om^3 - 108k^2 v^2 om^2 + 18k v^4 om - v^6
        c2 = E2gt.scale(36 * k * k) - (v2 * E1gt).scale(12 * k) + v4 * E0gt
        c3 = E3gt.scale(216 * k ** 3) - (v2 * E2gt).scale(108 * k * k) + (v4 * E1gt).scale(18 * k) - v6 * E0gt
        piece2 = ((v2 * c2).scale(3) - c3).scale(Fr(1, 6))
        return piece1 + piece2

    def f3(v):
        rho = phi_dv(DV(v.v * inv_sv, v.d * inv_sv)) * DV.const(inv_sv)
        return G(v) * rho
    # tail |v| > V: |F(max)| <= (2/3) v^6 + 3k v^4 E|om| + [3 v^2 E c^2 + E|c|^3] / 6 with |c| <= 6k|om| + v^2,
    # E|om| <= sqrt(2), E om^2 = 2, E|om|^3 <= sqrt(E om^6) = sqrt(120) < 11
    Eom1, Eom2, Eom3 = IV(SQRT2.hi), IV(2), IV(11)
    coef = {6: Fr(2, 3) + Fr(1, 6), 4: 3 * k * Eom1.hi + Fr(1, 6) * (3 * 6 * k * Eom1.hi + 3 * 6 * k * Eom1.hi),
            2: Fr(1, 6) * (3 * 36 * k * k * Eom2.hi + 3 * 36 * k * k * Eom2.hi), 0: Fr(1, 6) * 216 * k ** 3 * Eom3.hi}
    tail3 = IV(0)
    for j, cj in coef.items():
        tail3 = tail3 + abs_moment_tail(j, SIG2_V, V_MAX) * cj
    I3 = integrate(lambda v: (f3(v),), 0, V_MAX, CELL)[0] * 2 + IV(-tail3.hi, tail3.hi)

    sign = 1 if MUT == 'sign-lo' else -1
    J = (I1 * Fr(512, 3) - I2 * 8 + I3 * sign) / (216 * k ** 3)
    return {'k': str(k), 'I1': I1, 'I2': I2, 'I3': I3, 'J': J}


def R_of_b(b):
    """R(b) = [phi(beta) / sqrt(2)] / [(2 + b^2) Phi(beta) + sqrt(2) b phi(beta)], beta = b / sqrt(2)."""
    b = Fr(b)
    beta = IV(b) / SQRT2
    ph = phi_iv(beta)
    P = Phi(beta)
    num = ph / SQRT2
    den = P * (2 + b * b) + ph * SQRT2 * b
    return num / den


# ----------------------------------------------------------------------------- floating controls (not part of the certificate)
def _Phi_f(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _phi_f(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def float_I(k, v, om, Y):
    a = v * v
    c = 6 * k * om - v * v
    M = max(12 * k, 2 * abs(v), abs(om), abs(Y))
    top = 8 * M * M
    lo = max(a, c)

    def F(s):
        return s ** 3 / 3 - (a + c) * s * s / 2 + a * c * s
    return (F(top) - F(lo)) / (6 * k)


def float_mc(k, n, seed):
    rng = random.Random(seed)
    s = s2 = 0.0
    for _ in range(n):
        v = rng.gauss(0, math.sqrt(0.5))
        om = rng.gauss(0, math.sqrt(2))
        Y = rng.gauss(0, math.sqrt(6))
        x = float_I(k, v, om, Y) / (36 * k * k)
        s += x
        s2 += x * x
    mean = s / n
    return mean, math.sqrt(max(s2 / n - mean * mean, 0.0) / n)


def float_quad2d(k, n=240, V=7.0, O=11.0):
    """Midpoint rule in (v, om) with the Y-expectation in closed form."""
    sig_y = math.sqrt(6)
    tot = 0.0
    sv, so = math.sqrt(0.5), math.sqrt(2)
    for i in range(n):
        v = -V + (i + 0.5) * (2 * V / n)
        wv = _phi_f(v / sv) / sv * (2 * V / n)
        for j in range(n):
            om = -O + (j + 0.5) * (2 * O / n)
            wo = _phi_f(om / so) / so * (2 * O / n)
            a = v * v
            c = 6 * k * om - a
            lo = max(a, c)
            m0 = max(12 * k, 2 * abs(v), abs(om))
            coeffs = [-(lo ** 3 / 3 - (a + c) * lo * lo / 2 + a * c * lo), 8 * a * c, -(a + c) * 32, 512 / 3]
            t = m0 / sig_y
            A = [1 - _Phi_f(t)]
            for jj in range(1, 4):
                A.append(t ** (2 * jj - 1) * _phi_f(t) + (2 * jj - 1) * A[jj - 1])
            P_in = 2 * _Phi_f(t) - 1
            ey = sum(cj * (m0 ** (2 * jj) * P_in + 2 * sig_y ** (2 * jj) * A[jj]) for jj, cj in enumerate(coeffs))
            tot += wv * wo * ey / (6 * k)
    return tot / (36 * k * k)


def float_R(b):
    be = b / math.sqrt(2)
    return (_phi_f(be) / math.sqrt(2)) / ((2 + b * b) * _Phi_f(be) + math.sqrt(2) * b * _phi_f(be))


# ----------------------------------------------------------------------------- records
def dec_down(x, digits=10):
    x = Fr(x)
    n = x.numerator * 10 ** digits // x.denominator
    s_ = str(abs(n)).rjust(digits + 1, '0')
    return ('-' if n < 0 else '') + s_[:-digits] + '.' + s_[-digits:]


def dec_up(x, digits=10):
    x = Fr(x)
    n = -((-x.numerator * 10 ** digits) // x.denominator)
    s_ = str(abs(n)).rjust(digits + 1, '0')
    return ('-' if n < 0 else '') + s_[:-digits] + '.' + s_[-digits:]


def enclosure(iv, digits=10):
    return [dec_down(iv.lo, digits), dec_up(iv.hi, digits)]


def k_record(k):
    rec = certify_k(k)
    lead = LEAD * Fr(k) ** 3
    out = {'k': str(Fr(k)), 'J': enclosure(rec['J']), 'J_width': dec_up(rec['J'].width(), 12),
           'I1_E_M6': enclosure(rec['I1']), 'I2_E_v4M2': enclosure(rec['I2']), 'I3_E_F_lo': enclosure(rec['I3']),
           'lead_2359296_k3': str(lead), 'J_over_lead': enclosure(rec['J'] / lead, 8)}
    return out, rec


def controls_k(k):
    kf = float(Fr(k))
    mc, se = float_mc(kf, 200000, 2026)
    q = float_quad2d(kf)
    return {'k': str(Fr(k)), 'J_mc': mc, 'J_mc_se': se, 'J_quad2d': q}


def worker(k):
    out, rec = k_record(k)
    return out


def full_run(procs):
    with multiprocessing.Pool(procs) as pool:
        recs = pool.map(worker, list(K_GRID))
        ctrls = pool.map(controls_k, list(K_GRID))
    Rs = {str(b): enclosure(R_of_b(b), 12) for b in B_GRID}
    cg = {}
    for b in B_GRID:
        for rec in recs:
            J = IV(Fr(rec['J'][0]), Fr(rec['J'][1]))
            cg['b=%s,k=%s' % (b, rec['k'])] = enclosure(R_of_b(b) * J, 4)
    res = {
        'schema': 1,
        'object': 'CL-C8-CAP-FAILURE-COEFFICIENT-PLANAR-20260930-v1',
        'scientific_effect': 'NONE',
        'certified': True,
        'kind': 'certified enclosures of the limit coefficient c_G(b, k) = R(b) J(k) of Theorem G (NOTE.md); the limit theorem itself is author-side',
        'statement': 'Q^W(G_r^c) = c_G(b, k) r^3 + o(r^3) as r -> 0 for the planar six-pin law of [LP] with the good event G_r of [LP] section 7 / [CAP] (1); reference-kernel jet law',
        'parameters': {'PBITS': PBITS, 'CELL': str(CELL), 'T_SPAN': str(T_SPAN), 'V_MAX': str(V_MAX), 'LEAD': LEAD,
                       'k_grid': [str(k) for k in K_GRID], 'b_grid': [str(b) for b in B_GRID]},
        'J': recs,
        'R': Rs,
        'c_G': cg,
        'float_controls': ctrls,
        'mutant': MUT,
    }
    return res


def write_results(res):
    with open(os.path.join(HERE, 'RESULTS.json'), 'w') as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
        fh.write('\n')


def load_results():
    with open(os.path.join(HERE, 'RESULTS.json')) as fh:
        return json.load(fh)


def check_run(procs):
    ref = load_results()
    require(ref['parameters'] == {'PBITS': PBITS, 'CELL': str(CELL), 'T_SPAN': str(T_SPAN), 'V_MAX': str(V_MAX), 'LEAD': LEAD,
                                  'k_grid': [str(k) for k in K_GRID], 'b_grid': [str(b) for b in B_GRID]}, 'parameters differ from RESULTS.json')
    require(ref['mutant'] is None, 'RESULTS.json was produced under a mutant')
    # constants
    require(abs(PI.mid() - Fr('3.14159265358979323846')) < Fr(1, 10 ** 19) and PI.width() < Fr(1, 10 ** 30), 'pi enclosure')
    require(abs(Phi(IV(1)).mid() - Fr('0.841344746068542948585')) < Fr(1, 10 ** 19) and Phi(IV(1)).width() < Fr(1, 10 ** 30), 'Phi(1) enclosure')
    require(abs(exp_neg(IV(1)).mid() - Fr('0.367879441171442321595')) < Fr(1, 10 ** 19) and exp_neg(IV(1)).width() < Fr(1, 10 ** 30), 'exp(-1) enclosure')
    # the six certified values, recomputed and compared exactly with the stored decimal strings
    stored = {rec['k']: rec for rec in ref['J']}
    recs = {}

    def take(k, out):
        require(out == stored[str(k)], 'certified record for k = %s differs from RESULTS.json' % k)
        J = IV(Fr(out['J'][0]), Fr(out['J'][1]))
        lead = LEAD * Fr(k) ** 3
        # J(k) = LEAD k^3 (1 + delta(k)): delta positive and large for small k (the free third derivatives exceed 12k),
        # within 2e-6 of zero for k >= 1 (both signs occur: the -8 E[v^4 M^2] term is negative)
        if Fr(k) <= Fr(3, 4):
            require(J.lo >= lead, 'J(k) below %s k^3 at k = %s' % (LEAD, k))
        else:
            require(abs(J.mid() / lead - 1) < Fr(2, 10 ** 6), 'J(k) not within 2e-6 of %s k^3 at k = %s' % (LEAD, k))
        require(J.width() / J.lo < Fr(1, 10 ** 5), 'J(k) enclosure wider than 1e-5 relative at k = %s' % k)
        ctrl = [c for c in ref['float_controls'] if c['k'] == str(k)][0]
        Jf = float(J.mid())
        require(abs(ctrl['J_mc'] - Jf) <= 4 * ctrl['J_mc_se'] + 1e-9 * Jf, 'Monte Carlo control off by more than four standard errors at k = %s' % k)
        require(abs(ctrl['J_quad2d'] / Jf - 1) < 3e-4, 'two-dimensional quadrature control off by more than 3e-4 at k = %s' % k)
        recs[str(k)] = out
    take(K_GRID[0], worker(K_GRID[0]))          # first value sequentially: a mutant fails here
    with multiprocessing.Pool(procs) as pool:
        for k, out in zip(K_GRID[1:], pool.map(worker, list(K_GRID[1:]))):
            take(k, out)
    for b in B_GRID:
        Rb = R_of_b(b)
        require(enclosure(Rb, 12) == ref['R'][str(b)], 'R(b) differs at b = %s' % b)
        require(abs(float_R(float(b)) - float(Rb.mid())) < 1e-12, 'R(b) float control at b = %s' % b)
        for k in K_GRID:
            J = IV(Fr(stored[str(k)]['J'][0]), Fr(stored[str(k)]['J'][1]))
            require(enclosure(Rb * J, 4) == ref['c_G']['b=%s,k=%s' % (b, k)], 'c_G differs at (%s, %s)' % (b, k))
    # monotonicity of R on the grid and the two headline numbers
    Rvals = [Fr(ref['R'][str(b)][0]) for b in B_GRID]
    require(all(Fr(ref['R'][str(B_GRID[i])][1]) > Fr(ref['R'][str(B_GRID[i + 1])][0]) for i in range(len(B_GRID) - 1)), 'R not decreasing on the grid')
    require(Fr(ref['c_G']['b=0,k=2'][0]) > 5300000, 'c_G(0, 2) headline')
    require(Fr(ref['c_G']['b=6/5,k=1/6'][0]) > 35000, 'c_G(6/5, 1/6) headline')
    # [CAP] (3): C3_new + C4_new / 20 < 2.4e23, exact; and the recorded constant is at least 6e18 times c_G(6/5, 1/6)
    C3 = Fr(10, 51) * (Fr(32 ** 3, 3) * 320 ** 8 + Fr(3 * 32 ** 2, 2) * 320 ** 7)
    C4 = Fr(23, 5) * (10240 ** 4 + 6800 ** 4)
    require(C3 + C4 / 20 < Fr(24, 10) * 10 ** 23, '[CAP] (3) arithmetic')
    require(C3 / Fr(ref['c_G']['b=6/5,k=1/6'][1]) > 6 * 10 ** 18, 'ratio of the recorded constant to c_G(6/5, 1/6)')
    print(json.dumps({'check': 'ok', 'k_values': len(K_GRID), 'c_G(0,2)': ref['c_G']['b=0,k=2'], 'c_G(6/5,1/6)': ref['c_G']['b=6/5,k=1/6'], 'mutant': MUT}))


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--mutant', choices=MUTANTS)
    ap.add_argument('--procs', type=int, default=4)
    ap.add_argument('--quick', type=str, default=None, help='certify one k (rational) and print the record')
    args = ap.parse_args()
    MUT = args.mutant
    if args.quick:
        import time
        t0 = time.time()
        out, rec = k_record(Fr(args.quick))
        print(json.dumps(out), 'time', round(time.time() - t0, 1))
        print('mc', float_mc(float(Fr(args.quick)), 100000, 1), 'quad2d', float_quad2d(float(Fr(args.quick)), 160))
        return
    if args.check:
        check_run(args.procs)
        return
    res = full_run(args.procs)
    write_results(res)
    print(json.dumps({r['k']: r['J'] for r in res['J']}))


if __name__ == '__main__':
    main()
