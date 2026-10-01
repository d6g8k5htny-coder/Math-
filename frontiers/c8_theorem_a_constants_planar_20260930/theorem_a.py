#!/usr/bin/env python3
"""Explicit constants for Theorem A of [LP] in the plane (d = 2), for the torus kernel K_L with L >= 10 in every frame:
for 0 < r <= r_*, b in [0, 1], k in [1/2, 2],

    1 - p_r(b, k, R)  <=  Q^W(G_r^c)  <=  C(r_*) r^3,

with G_r the good event of [LP] section 7 / [CAP] (1) and C(r_*) certified here (NOTE.md Theorem E).  The proof bounds
Q^W(G_r^c) = E_Q[W_r 1{G_r^c}] / Z_r from above by an exact Gaussian regression near r = 0:

  * covariances of the preconditioned pin and target functionals are exact power series in r, obtained from the Taylor
    coefficients of the kernel at 0 (every negative power cancels identically, checked); the torus remainder is bounded
    uniformly in r and in the frame by Cauchy estimates on a polydisc;
  * the failure event is reduced to {lambda <= (4/(3k)) r M_3^2} u {r M_4 > 3k/10}; M_3 is bounded through exact averaging
    identities of the pinned jets and M_4 through the Taylor series at the midpoint;
  * the main term is integrated in lambda = -f_yy(M) against its Gaussian density after an exact regression on w = f_yy(M);
    the remaining expectations are closed-form incomplete Gaussian moments plus Hoelder-controlled perturbations;
  * the normalizer Z_r is bounded below in closed form; the rare branches are Gaussian tails.
All arithmetic is exact rational interval arithmetic (outward rounding to 2^-160); standard library only.
"""
import argparse
import json
import math
import multiprocessing
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
MUTANTS = ('no-delta', 'cap-half', 'no-zfloor-correction', 'no-om-term')
MUT = None
PBITS = 160
L_MIN = 10
NX = 60                    # Taylor order in x of the covariance series (exact); the rest is a bounded tail
NB = 24                    # truncation order of the Taylor tails of the 4-jets at the midpoint (the rest is bounded)
X0 = Fr(1, 64)             # threshold for the quadratic near-branch analysis
THETA = Fr(1, 32)          # splitting parameter in the max-moment lemma
THETA_E = Fr(1, 16)        # splitting parameter for the (r nu + v)^2 factor
R_STARS = (Fr(1, 4096), Fr(1, 2048), Fr(1, 1024), Fr(1, 512), Fr(1, 256), Fr(1, 128), Fr(1, 64))
BAND_B = (Fr(0), Fr(1))
BAND_K = (Fr(1, 2), Fr(2))


def require(cond, msg):
    if not cond:
        print(json.dumps({'check': 'FAIL', 'reason': msg, 'mutant': MUT}))
        sys.exit(1)


# ----------------------------------------------------------------------------- rational intervals (from Math-#195 / #203)
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




def phi_pt(x):
    """phi(x) for rational x (interval)."""
    x = Fr(x)
    return exp_neg_point(x * x / 2) / SQRT2PI


def Phibar_pt(x):
    """1 - Phi(x) for rational x (interval)."""
    p = phi_point(Fr(x)) if abs(Fr(x)) <= 12 else None
    if p is None:
        if x > 0:
            # Mills: Phibar(x) <= phi(x)/x
            return IV(0, (phi_pt(x) / x).hi)
        return IV(1 - (phi_pt(-x) / (-x)).hi, 1)
    return IV(1 - p.hi, 1 - p.lo)


def upper_moments(x, J):
    """[M_0(x), ..., M_J(x)], M_j(x) = integral_x^inf t^j phi(t) dt, for rational x >= 0 (intervals)."""
    x = Fr(x)
    require(x >= 0, 'upper moment at negative point')
    ph = phi_pt(x)
    M = [Phibar_pt(x), ph]
    for j in range(2, J + 1):
        M.append(ph * x ** (j - 1) + M[j - 2] * (j - 1))
    return M


def dfact(n):
    """(n)!! for n >= -1."""
    return math.prod(range(n, 0, -2)) if n > 0 else 1


def rup_rel(x, bits=200):
    """Round a rational x >= 0 up to a dyadic with `bits` significant bits (upper bounds stay upper bounds)."""
    x = Fr(x)
    if x <= 0:
        return x
    e = x.numerator.bit_length() - x.denominator.bit_length()
    sh = bits - e
    if sh >= 0:
        return Fr(-((-x.numerator << sh) // x.denominator), 1 << sh)
    return Fr(-((-x.numerator) // (x.denominator << -sh)) << -sh)


def sqrt_up(x):
    """Rational upper bound of sqrt(x), x >= 0 rational, relative error below 2^-200 (no absolute rounding floor)."""
    x = Fr(x)
    if x == 0:
        return Fr(0)
    n, d = x.numerator, x.denominator
    nd = n * d
    m = max(0, (420 - nd.bit_length()) // 2 + 1)
    return rup_rel(Fr(math.isqrt(nd << (2 * m)) + 1, d << m))


def iroot(x, p):
    """Upper bound (rational) of x^(1/p) for rational x >= 0 and p a power of two."""
    v = Fr(x)
    while p > 1:
        v = sqrt_up(v)
        p //= 2
    return v


def pow2(p):
    q = 1
    while q < p:
        q *= 2
    return q


ZN = {}


def znorm(p):
    """Upper bound of ||N(0,1)||_p for p a power of two (p = 1 uses sqrt(2/pi) < 4/5)."""
    if p == 1:
        return Fr(4, 5)
    if p not in ZN:
        ZN[p] = iroot(Fr(dfact(p - 1)), p)
    return ZN[p]


def habs_moment(j):
    """E|zeta|^j (interval)."""
    if j % 2 == 0:
        return IV(dfact(j - 1))
    return SQRT2 / isqrt_iv(PI) * (2 ** ((j - 1) // 2) * math.factorial((j - 1) // 2))


# ----------------------------------------------------------------------------- functionals and exact covariance series
HALF = Fr(1, 2)
XM, XS, X0PT = -HALF, HALF, Fr(0)


def term(c, p, a, b, x0):
    """c r^p d_x^a d_y^b f(x0 r, 0)."""
    return (Fr(c), p, a, b, Fr(x0))


def functionals():
    pins = {
        'p1': [term(HALF, 0, 0, 0, XM), term(HALF, 0, 0, 0, XS)],
        'p2': [term(-1, -1, 0, 0, XM), term(1, -1, 0, 0, XS)],
        'p3p': [term(6, -2, 1, 0, XM), term(6, -2, 1, 0, XS), term(12, -3, 0, 0, XM), term(-12, -3, 0, 0, XS)],
        'p4': [term(-1, -1, 1, 0, XM), term(1, -1, 1, 0, XS)],
        'q1': [term(HALF, 0, 0, 1, XM), term(HALF, 0, 0, 1, XS)],
        'q2': [term(-1, -1, 0, 1, XM), term(1, -1, 0, 1, XS)],
    }
    targets = {
        'w': [term(1, 0, 0, 2, XM)],
        'v': [term(1, -1, 1, 1, XM), term(1, -2, 0, 1, XM), term(-1, -2, 0, 1, XS)],
        'om': [term(1, -1, 0, 2, XS), term(-1, -1, 0, 2, XM)],
        'Y': [term(1, 0, 0, 3, X0PT)],
        'T': [term(1, -2, 2, 0, XM), term(4, -3, 1, 0, XM), term(2, -3, 1, 0, XS), term(6, -4, 0, 0, XM), term(-6, -4, 0, 0, XS)],
        'tau': [term(1, -3, 2, 0, XS), term(-1, -3, 2, 0, XM), term(-6, -4, 1, 0, XM), term(-6, -4, 1, 0, XS),
                term(-12, -5, 0, 0, XM), term(12, -5, 0, 0, XS)],
        'nu': [term(1, -2, 1, 1, XM), term(1, -2, 1, 1, XS), term(2, -3, 0, 1, XM), term(-2, -3, 0, 1, XS)],
        'X40': [term(1, 0, 4, 0, X0PT)], 'X31': [term(1, 0, 3, 1, X0PT)], 'X22': [term(1, 0, 2, 2, X0PT)],
        'X13': [term(1, 0, 1, 3, X0PT)], 'X04': [term(1, 0, 0, 4, X0PT)],
    }
    return pins, targets


PIN_NAMES = ('p1', 'p2', 'p3p', 'p4', 'q1', 'q2')
TARGET_NAMES = ('w', 'v', 'om', 'Y', 'T', 'tau', 'nu', 'X40', 'X31', 'X22', 'X13', 'X04')
JET4 = ('X40', 'X31', 'X22', 'X13', 'X04')
JET4_IDX = {'X40': (4, 0), 'X31': (3, 1), 'X22': (2, 2), 'X13': (1, 3), 'X04': (0, 4)}


def weight(F):
    """Scaling weight a - (power of r), common to all terms of a preconditioned functional."""
    ws = {t[2] - t[1] for t in F}
    require(len(ws) == 1, 'functional not homogeneous')
    return ws.pop()


def hcoef(n):
    """d^n/dx^n exp(-x^2/2) at 0."""
    if n % 2:
        return 0
    return (-1) ** (n // 2) * dfact(n - 1)


PAIR_CACHE = {}


def pair_series(F, G, key):
    """Exact data of Cov_K(F, G) = sum_gamma kappa_gamma pi_gamma r^(gx - wF - wG):
    returns (reference series {power: rational}, weight w, list of (|c c'|, a+a', b+b') for the remainder bounds)."""
    if key in PAIR_CACHE:
        return PAIR_CACHE[key]
    wF, wG = weight(F), weight(G)
    w = wF + wG
    pi = {}
    absterms = []
    for (cf, pf, af, bf, xf) in F:
        for (cg, pg, ag, bg, xg) in G:
            gy = bf + bg
            sgn = (-1) ** (ag + bg)
            d = xf - xg
            absterms.append((abs(cf * cg), af + ag, gy))
            for gx in range(af + ag, NX + 1):
                m = gx - af - ag
                val = cf * cg * sgn * d ** m / math.factorial(m)
                if val != 0:
                    pi[(gx, gy)] = pi.get((gx, gy), Fr(0)) + val
    for (gx, gy), v in pi.items():
        require(v == 0 or gx - w >= 0, 'negative power of r in a covariance (regularity fails)')
    ser = {}
    for (gx, gy), v in pi.items():
        kap = hcoef(gx) * hcoef(gy)
        if kap and v:
            ser[gx - w] = ser.get(gx - w, Fr(0)) + kap * v
    out = ({p: c for p, c in ser.items() if c != 0}, w, absterms)
    PAIR_CACHE[key] = out
    return out


def torus_M1(L):
    """Bound of |sum_{n != 0} G(z + p_n)| on the polydisc |z_1|, |z_2| <= 1 (every frame, |p_n| = |n| L):
    exp(1) * sum_{j >= 1} 8 j exp(-(j L - 3/2)^2 / 2)."""
    L = Fr(L)
    tot = Fr(0)
    for j in range(1, 6):
        tot += 8 * j * exp_neg_point((j * L - Fr(3, 2)) ** 2 / 2).hi
    tail = 8 * 7 * exp_neg_point((6 * L - Fr(3, 2)) ** 2 / 2).hi * 4      # j >= 6, very crude
    return Fr(27183, 10000) * (tot + tail)


def theta_minus_one(L):
    L = Fr(L)
    tot = Fr(0)
    for j in range(1, 6):
        tot += 8 * j * exp_neg_point((j * L) ** 2 / 2).hi
    return tot + 8 * 7 * exp_neg_point((6 * L) ** 2 / 2).hi * 4


def cov_band(F, G, key, r0, r1, M1):
    """Enclosure of the covariance (unnormalized torus kernel sum_n G(z + p_n)) of F and G, for r in [r0, r1]."""
    ser, w, absterms = pair_series(F, G, key)
    val = IV(0)
    for p, c in ser.items():
        val = val + IV(r0 ** p, r1 ** p) * c
    A = max((t[1] for t in absterms), default=0)
    # Taylor truncation tail of the reference kernel (orders gx > NX)
    tail = Fr(0)
    for (acc, aa, gy) in absterms:
        tail += acc * abs(hcoef(gy))
    tail *= 2 * Fr(NX + 1) ** A * r1 ** (NX + 1 - w)
    # torus remainder: Cauchy estimates |rho_gamma| <= gx! gy! M1 on the unit polydisc
    tor = Fr(0)
    if True:
        for (acc, aa, gy) in absterms:
            tor += acc * math.factorial(gy) * Fr(max(w, 1)) ** aa
        tor = tor * M1 / (1 - Fr(27183, 10000) * r1)
    err = tail + tor
    return val + IV(-err, err)


# ----------------------------------------------------------------------------- interval linear algebra
def solve_iv(A, B):
    """Interval Gaussian elimination with partial pivoting on midpoints: X[c] solves A X[c] = B[c]."""
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


def cholesky3(C):
    """Interval Cholesky of a 3 x 3 SPD interval matrix."""
    L = [[IV(0)] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(i + 1):
            s = C[i][j] - sum((L[i][l] * L[j][l] for l in range(j)), IV(0))
            if i == j:
                require(s.lo > 0, 'Cholesky pivot not positive')
                L[i][j] = isqrt_iv(s)
            else:
                L[i][j] = s / L[j][j]
    return L


def absup(x):
    return max(abs(x.lo), abs(x.hi))


# ----------------------------------------------------------------------------- the conditional law on an r-band
class Law:
    pass


def band_law(r0, r1, L=L_MIN):
    """Interval enclosures, uniform over r in [r0, r1], every frame and every torus side >= L, of the Q-law of the
    targets: mean = b alpha + k beta, covariance C (normalized kernel), and the pin energy coefficients."""
    pins, targets = functionals()
    P = [pins[n] for n in PIN_NAMES]
    T = [targets[n] for n in TARGET_NAMES]
    M1 = torus_M1(L)
    th1 = theta_minus_one(L)
    nt = len(T)
    Spp = [[cov_band(P[i], P[j], ('p', i, j), r0, r1, M1) for j in range(6)] for i in range(6)]
    Stp = [[cov_band(T[i], P[j], ('tp', i, j), r0, r1, M1) for j in range(6)] for i in range(nt)]
    Stt = [[cov_band(T[i], T[j], ('tt', i, j), r0, r1, M1) for j in range(nt)] for i in range(nt)]
    r = IV(r0, r1)
    kvec = [-(r * r * r) * HALF, -(r * r), IV(12), IV(0), IV(0), IV(0)]
    e1 = [IV(1), IV(0), IV(0), IV(0), IV(0), IV(0)]
    W = solve_iv(Spp, Stp)
    xs = solve_iv(Spp, [e1, kvec])
    law = Law()
    law.r0, law.r1, law.L, law.M1, law.th1 = r0, r1, L, M1, th1
    law.alpha = {n: W[i][0] for i, n in enumerate(TARGET_NAMES)}
    law.beta = {n: sum((W[i][j] * kvec[j] for j in range(6)), IV(0)) for i, n in enumerate(TARGET_NAMES)}
    scale = IV(1 / (1 + th1), 1)          # K_L = (unnormalized) / Theta, Theta in [1, 1 + th1]
    C = {}
    for i, a in enumerate(TARGET_NAMES):
        for j, c in enumerate(TARGET_NAMES):
            if j < i:
                continue
            v = Stt[i][j] - sum((W[i][l] * Stp[j][l] for l in range(6)), IV(0))
            if i != j:
                v2 = Stt[j][i] - sum((W[j][l] * Stp[i][l] for l in range(6)), IV(0))
                v = v.meet(v2)
            C[(a, c)] = C[(c, a)] = v * scale
    law.C = C
    escale = IV(1, 1 + th1)
    law.e_bb = xs[0][0] * escale
    law.e_bk = sum((kvec[j] * xs[0][j] for j in range(6)), IV(0)) * escale
    law.e_kk = sum((kvec[j] * xs[1][j] for j in range(6)), IV(0)) * escale
    # regression on w and the g-parts
    sw2 = C[('w', 'w')]
    require(sw2.lo > 0, 'Var w not positive')
    law.sw2 = sw2
    law.sw = isqrt_iv(sw2)
    law.bw = {n: C[(n, 'w')] / sw2 for n in TARGET_NAMES if n != 'w'}
    Cg = {}
    for a in TARGET_NAMES:
        for c in TARGET_NAMES:
            if a != 'w' and c != 'w':
                Cg[(a, c)] = C[(a, c)] - C[(a, 'w')] * C[(c, 'w')] / sw2
    law.Cg = Cg
    law.L3 = cholesky3([[Cg[(a, c)] for c in ('v', 'om', 'Y')] for a in ('v', 'om', 'Y')])
    law.sdg = {n: isqrt_iv(IV(max(Cg[(n, n)].lo, Fr(0)), Cg[(n, n)].hi)) if Cg[(n, n)].lo > 0 else IV(0, isqrt_iv(IV(Cg[(n, n)].hi)).hi)
               for n in TARGET_NAMES if n != 'w'}
    law.sdQ = {n: isqrt_iv(C[(n, n)]) for n in TARGET_NAMES}
    # crude higher jets: Taylor-tail coefficients S_alpha(r1) = sum_{beta != 0} sd0_{alpha+beta} (2 r1)^{|beta|} / beta!
    law.S = {n: taylor_tail_coefficient(JET4_IDX[n], r1, M1) for n in JET4}
    return law


def sd0_bound(gx, gy, M1):
    """Upper bound of sqrt(Var d^gamma f(0)) = sqrt(|d^{2 gamma} K_L(0)|) (normalized, every frame, L >= L_MIN)."""
    v = dfact(2 * gx - 1) * dfact(2 * gy - 1) + math.factorial(2 * gx) * math.factorial(2 * gy) * M1
    return isqrt_iv(IV(v)).hi


def taylor_tail_coefficient(alpha, r1, M1):
    ax, ay = alpha
    tot = Fr(0)
    for n in range(1, NB + 1):
        for bx in range(n + 1):
            by = n - bx
            tot += sd0_bound(ax + bx, ay + by, M1) * (2 * r1) ** n / (math.factorial(bx) * math.factorial(by))
    # tail |beta| > NB: sd0_gamma <= 2^|gamma| gx! gy! sqrt(1 + M1) (binom(2m, m) <= 4^m), so a term is at most
    # 2^|alpha| (4 + n)^4 (4 r1)^n 2 per multi-index; n + 1 multi-indices of order n
    q = 4 * r1
    require(q <= Fr(1, 16), 'Taylor tail ratio too large')
    tail = Fr(0)
    base = 2 ** (ax + ay) * 2
    n = NB + 1
    # sum_{n > NB} (n + 1)(n + 4)^8 q^n <= (NB + 2)(NB + 5)^8 q^(NB+1) / (1 - 2 q)   (consecutive ratio <= 2q for these n)
    tail = base * (NB + 2) * Fr(NB + 5) ** 8 * q ** (NB + 1) / (1 - 2 * q)
    return tot + tail


# ----------------------------------------------------------------------------- moment calculus (normalized by K = 12 k)
def binom(n, k):
    return math.comb(n, k)


def gauss_norm(mu_abs, sd, p):
    """Upper bound of ||X||_p for X Gaussian with |mean| <= mu_abs and sd <= sd."""
    return rup_rel(mu_abs + sd * znorm(pow2(p)))


def pos_part_moments(s, c, nmax, extra_max):
    """P[n][e] = upper bound of E[u^e (u^n - c^n)_+], u = s |zeta|, for 1 <= n <= nmax, 0 <= e <= extra_max."""
    x = c / s
    M = upper_moments(x, nmax + extra_max)
    out = {}
    for n in range(1, nmax + 1):
        for e in range(extra_max + 1):
            out[(n, e)] = rup_rel(((M[n + e] * s ** (n + e) - M[e] * c ** n * s ** e) * 2).hi)
    return out


def normalized_moments(q, nmax):
    """Component moments, normalized by K = 12 k (K >= Klo), for n <= nmax:
      E1[n], E1o[n], E1v[n] : upper bounds of E[y1^n], E[o0 y1^n], E[v0^2 y1^n], y1 = 1 + cmu1/K + (r1/K) Delta1;
      Tn[n], To[n], Tv[n]   : upper bounds of sum_{i=2,3,4} E[(y_i^n - c^n)_+] (and with the factors o0, v0^2),
                              y_i <= u_i + delta_i (u_i = s_i |zeta| independent half-normals), threshold c = q['c'].
    o0 = s3 |z2| and v0^2 = s2^2 z1^2 / 4 are unnormalized."""
    th = THETA
    cp = q['c'] * (1 - th)                  # <= c (1 + th)^{-(n-1)/n} for every n (Bernoulli)
    PP = {i: pos_part_moments(q['s'][i], cp, nmax, 2) for i in (2, 3, 4)}
    Eu3 = (habs_moment(1) * q['s3']).hi
    Eu2sq = (habs_moment(2) * q['s2'] * q['s2']).hi
    n_o0_2 = q['s3'] * znorm(2)
    n_u2sq_2 = q['s2'] * q['s2'] * znorm(4) ** 2
    r3 = q['s3'] / q['s'][3]
    r2sq = (q['s2'] / q['s'][2]) ** 2
    E1, E1o, E1v, Tn, To, Tv = {}, {}, {}, {}, {}, {}
    base = 1 + q['cmt1']
    for n in range(0, nmax + 1):
        ey = base ** n
        eo = base ** n * Eu3
        ev = base ** n * Eu2sq
        for j in range(1, n + 1):
            coef = binom(n, j) * base ** (n - j) * q['rK'] ** j
            ey += coef * q['nD1'](pow2(j)) ** j
            eo += coef * n_o0_2 * q['nD1'](pow2(2 * j)) ** j
            ev += coef * n_u2sq_2 * q['nD1'](pow2(2 * j)) ** j
        E1[n], E1o[n], E1v[n] = rup_rel(ey), rup_rel(eo), rup_rel(ev / 4)
        if n == 0:
            continue
        f1 = (1 + th) ** (n - 1)
        f2 = (1 + 1 / th) ** (n - 1)
        tn = to = tv = Fr(0)
        for i in (2, 3, 4):
            P = PP[i]
            dn = q['nd'](i, pow2(n)) ** n
            dn2 = q['nd'](i, pow2(2 * n)) ** n
            tn += f1 * P[(n, 0)] + f2 * dn
            to += (f1 * r3 * P[(n, 1)] if i == 3 else f1 * Eu3 * P[(n, 0)]) + f2 * n_o0_2 * dn2
            tv += (f1 * r2sq * P[(n, 2)] if i == 2 else f1 * Eu2sq * P[(n, 0)]) + f2 * n_u2sq_2 * dn2
        Tn[n], To[n], Tv[n] = rup_rel(tn), rup_rel(to), rup_rel(tv / 4)
    return E1, E1o, E1v, Tn, To, Tv


def elam_pos(m, s):
    """E[(s z + m)_+] at a point (rational m, s > 0)."""
    x = Fr(m) / s
    return m * Phi(IV(x)) + phi_pt(x) * s


def elam2_pos(m, s):
    """E[(s z + m)_+^2] at a point."""
    x = Fr(m) / s
    return (m * m + s * s) * Phi(IV(x)) + phi_pt(x) * (m * s)


def box_bound(law, bb, kb, r0, r1, last_band=False):
    """Certified upper bound of sup_{r in [r0, r1]} Q^W(G_r^c) / r^3 over b in bb, k in kb, with its pieces."""
    b = IV(bb[0], bb[1])
    k = IV(kb[0], kb[1])
    klo, khi = kb[0], kb[1]
    Klo = 12 * klo
    mu = {n: b * law.alpha[n] + k * law.beta[n] for n in TARGET_NAMES}
    mabs = {n: absup(mu[n]) for n in TARGET_NAMES}
    E = b * b * law.e_bb + b * k * law.e_bk * 2 + k * k * law.e_kk
    require(E.hi > 0, 'energy')
    sqE = isqrt_iv(IV(E.hi)).hi
    sw_lo, sw_hi = law.sw.lo, law.sw.hi
    muw_abs = mabs['w']
    bw = {n: absup(law.bw[n]) for n in law.bw}
    t = {n: law.S[n] / sw_lo for n in JET4}
    a_fac = Fr(1, 2) if MUT == 'cap-half' else Fr(1)      # the cap constant 4/(3k) (mutant: halved)
    B = lambda n: bw[n] + t[n]
    bbars = {1: r1 * (Fr(5, 2) * B('X40') + 2 * B('X31')),
             2: 2 * bw['v'] + r1 * (Fr(5, 2) * B('X31') + 2 * B('X22')),
             3: bw['om'] + r1 * (Fr(5, 2) * B('X22') + 2 * B('X13')),
             4: bw['Y'] + r1 * (2 * B('X13') + 2 * B('X04'))}
    bbars = {i: rup_rel(v) for i, v in bbars.items()}
    bbar = max(bbars.values())
    L3 = law.L3
    s2, s3, s4 = 2 * L3[0][0].hi, L3[1][1].hi, L3[2][2].hi
    l21, l31, l32 = absup(L3[1][0]), absup(L3[2][0]), absup(L3[2][1])

    memo = {}

    def nA(n, p):     # ||A_alpha^g||_p, A_alpha^g = |X_alpha,g| + T_alpha^g
        key = ('A', n, p)
        if key not in memo:
            memo[key] = rup_rel(gauss_norm(mabs[n], law.sdg[n].hi, p) + law.S[n] * (sqE + znorm(pow2(p))))
        return memo[key]

    def nDelta(i, p):
        key = ('D', i, p)
        if key not in memo:
            memo[key] = rup_rel(nDelta0(i, p))
        return memo[key]

    def nDelta0(i, p):
        if MUT == 'no-delta':
            return Fr(0)
        if i == 1:
            return Fr(5, 2) * nA('X40', p) + 2 * nA('X31', p)
        if i == 2:
            return Fr(5, 2) * nA('X31', p) + 2 * nA('X22', p)
        if i == 3:
            return Fr(5, 2) * nA('X22', p) + 2 * nA('X13', p)
        return 2 * nA('X13', p) + 2 * nA('X04', p)

    def nd(i, p):
        key = ('d', i, p)
        if key not in memo:
            memo[key] = rup_rel(nd0(i, p))
        return memo[key]

    def nd0(i, p):     # ||delta_i||_p / Klo, delta_i including beta_i |mu_w|
        zp = znorm(pow2(p))
        cm = bbars[i] * muw_abs
        if i == 2:
            v = 2 * mabs['v'] + cm + r1 * nDelta(2, p)
        elif i == 3:
            v = mabs['om'] + l21 * zp + cm + r1 * nDelta(3, p)
        else:
            v = mabs['Y'] + (l31 + l32) * zp + cm + r1 * nDelta(4, p)
        return v / Klo

    kappa = 3 / (1 - 3 * X0)
    Fk = 1 + kappa * X0                      # (1 + kappa x_i) <= Fk on the event {x_i <= X0}
    cth = 1 - kappa * X0 / 2                 # <= Fk^{-1/2}
    NMAX = 18
    q = {'cmt1': bbars[1] * muw_abs / Klo, 'rK': r1 / Klo, 'nD1': lambda p: nDelta(1, p),
         's': {2: s2 / Klo, 3: s3 / Klo, 4: s4 / Klo}, 'nd': nd, 's3': s3, 's2': s2, 'c': cth}
    E1, E1o, E1v, Tn, To, Tv = normalized_moments(q, NMAX)
    et1 = rup_rel(16 * kappa * r1 * bbars[1] * a_fac)     # eta_1 K, k-free
    aK2_hi = 192 * khi * a_fac                    # a K^2 = 192 k

    # moments of Ut = U / (a K^2) <= max(Z1, Fk y_i^2), Z1 = y1^2 (1 + et1 y1)
    def EUt(p):                                   # upper bound of E[Ut^p]
        key = ('U', p)
        if key not in memo:
            memo[key] = rup_rel(sum(binom(p, l) * et1 ** l * E1[2 * p + l] for l in range(p + 1)) + Fk ** p * Tn[2 * p])
        return memo[key]

    def EoUt2():
        return sum(binom(2, l) * et1 ** l * E1o[4 + l] for l in range(3)) + Fk ** 2 * To[4]

    def EvUt2():
        return sum(binom(2, l) * et1 ** l * E1v[4 + l] for l in range(3)) + Fk ** 2 * Tv[4]

    def sq(x):
        return isqrt_iv(IV(x)).hi

    U3_2 = sq(EUt(6))                              # ||Ut^3||_2
    U2_2 = sq(EUt(4))                              # ||Ut^2||_2

    def nU(p):                                     # ||U||_p <= a K^2 Fk ||max_i y_i||_2p^2 (on the event x_i <= X0)
        require(2 * p <= NMAX and pow2(p) == p, 'norm order')
        key = ('nU', p)
        if key not in memo:
            memo[key] = rup_rel(aK2_hi * Fk * iroot(E1[2 * p] + Tn[2 * p], p))
        return memo[key]

    def nbar(n, p):                                # ||F_bar||_p, F_bar = |F_g| + |beta_F| (|mu_w| + r1 U)
        return gauss_norm(mabs[n], law.sdg[n].hi, p) + bw[n] * (muw_abs + r1 * nU(p))

    six_klo = 6 * klo
    nT2, nT4, nt2, nt4 = nbar('T', 2), nbar('T', 4), nbar('tau', 2), nbar('tau', 4)
    epsc2 = (2 * r1 * nT2 + r1 * r1 * nt2) / six_klo + (r1 * nT4) * (r1 * nT4 + r1 * r1 * nt4) / six_klo ** 2
    nT8, nt8 = nbar('T', 8), nbar('tau', 8)
    epsc4 = (2 * r1 * nT4 + r1 * r1 * nt4) / six_klo + (r1 * nT8) * (r1 * nT8 + r1 * r1 * nt8) / six_klo ** 2
    # Term A / (36 k^2)
    A_n = EUt(3) + epsc2 * U3_2
    termA = aK2_hi ** 3 / 3 * A_n
    # Term B / (36 k^2)
    ndo = lambda p: l21 * znorm(pow2(p)) + mabs['om'] + bw['om'] * (muw_abs + r1 * nU(p))
    no4 = s3 * znorm(4) + ndo(4)
    B_n = EoUt2() + (ndo(2) + epsc4 * no4) * U2_2
    termB = aK2_hi ** 2 / 2 * B_n
    if MUT == 'no-om-term':
        termB = Fr(0)
    # Term C / (36 k^2) = (a K^2)^2 / (12 k) * E[(1 + r T/(6k)) e Ut^2]
    th = THETA_E
    dv = lambda p: mabs['v'] + bw['v'] * (muw_abs + r1 * nU(p))
    ebar4 = (r1 * nbar('nu', 8) + L3[0][0].hi * znorm(8) + dv(8)) ** 2
    C_n = ((1 + th) ** 2 * EvUt2()
           + ((1 + th) * (1 + 1 / th) * dv(4) ** 2 + (1 + 1 / th) * r1 * r1 * nbar('nu', 4) ** 2) * U2_2
           + r1 * nT4 / six_klo * ebar4 * U2_2)
    termC = aK2_hi ** 2 / (12 * klo) * C_n
    # density of lambda = -w on [0, inf)
    mlo = max(Fr(0), mu['w'].lo)
    pbar = (phi_pt(mlo / sw_hi) / sw_lo).hi
    # ---- normalizer floor Z_r / (36 k^2 r^2) >= El2 - corr
    m_lam = -mu['w']
    El2 = elam2_pos(m_lam.lo, sw_lo).lo
    Elp = elam_pos(m_lam.hi, sw_hi).hi
    lam_n = lambda p: muw_abs + sw_hi * znorm(pow2(p))
    sdT, sdtau = law.sdQ['T'].hi, law.sdQ['tau'].hi
    q_bad = gauss_tail2(mabs['T'], sdT, 3 * klo / (2 * r1)) + gauss_tail2(mabs['tau'], sdtau, 3 * klo / (2 * r1 * r1))
    Eom_g = mabs['om'] + law.sdg['om'].hi * Fr(4, 5)
    Evg2 = mabs['v'] ** 2 + law.sdg['v'].hi ** 2
    E_om_lam = Eom_g * Elp + bw['om'] * (muw_abs * lam_n(1) + lam_n(2) ** 2)
    E_v2_lam = 2 * Evg2 * Elp + 2 * bw['v'] ** 2 * (sw_hi * znorm(4)) ** 2 * lam_n(2)
    corr = (lam_n(4) ** 2 * iroot(q_bad, 2) if q_bad > 0 else Fr(0)) \
        + (2 * r1 * gauss_norm(mabs['T'], sdT, 2) + r1 * r1 * gauss_norm(mabs['tau'], sdtau, 2)) * lam_n(4) ** 2 / six_klo \
        + r1 * (E_v2_lam / (3 * klo) + E_om_lam)
    if MUT == 'no-zfloor-correction':
        corr = Fr(0)
    zt = El2 - corr
    require(zt > 0, 'normalizer floor not positive')
    main = pbar * (termA + termB + termC) / zt
    # ---- rare branches at the band top: ||W||_2 / r^2 and probabilities
    six_khi = 6 * khi
    nT8Q = gauss_norm(mabs['T'], sdT, 8)
    ntau8Q = gauss_norm(mabs['tau'], sdtau, 8)
    g1 = (six_khi + r1 * nT8Q) * lam_n(8)
    g2 = (six_khi + r1 * nT8Q + r1 * r1 * ntau8Q) * (lam_n(8) + r1 * gauss_norm(mabs['om'], law.sdQ['om'].hi, 8)) \
        + r1 * (r1 * gauss_norm(mabs['nu'], law.sdQ['nu'].hi, 8) + gauss_norm(mabs['v'], law.sdQ['v'].hi, 8)) ** 2
    w2 = g1 * g2
    thr = 3 * klo / (10 * r1)
    qA2 = Fr(0)
    args = []
    for n in JET4:
        args.append((thr * Fr(7, 8) - mabs[n]) / law.sdQ[n].hi)
        qA2 += gauss_tail2(mabs[n], law.sdQ[n].hi, thr * Fr(7, 8))
        qA2 += (law.S[n] * (sqE + znorm(32)) / (thr / 8)) ** 32
    a_hi = Fr(4, 3) / klo * a_fac
    qfar = Fr(0)
    qx = Fr(0)
    if bbar > 0:
        lam_far = 1 / (4 * a_hi * r1 * bbar * bbar)
        args.append((lam_far - muw_abs) / sw_hi)
        qfar = gauss_tail1(muw_abs, sw_hi, lam_far)
    for i in (1, 2, 3, 4):                         # x_i > X0  <=>  y_i' > X0 / (a r1 beta_i)
        if bbars[i] == 0:
            continue
        tx = X0 / (a_hi * r1 * bbars[i])
        if i == 1:
            cb = 12 * khi + bbars[1] * muw_abs
            qx += Fr(1) if tx <= cb else (r1 * nDelta(1, 32) / (tx - cb)) ** 32
        else:
            s_i = {2: s2, 3: s3, 4: s4}[i]
            args.append(tx / (2 * s_i))
            qx += gauss_tail2(0, s_i, tx / 2) + (nd(i, 32) * Klo / (tx / 2)) ** 32
    qs = [min(Fr(1), x) for x in (qA2, qfar, qx)]
    tail_num = w2 * sum((iroot(x, 2) if x > 0 else Fr(0)) for x in qs)
    if last_band:
        # (0, R] is the union of [R 2^-(j+1), R 2^-j]; every Gaussian tail argument scales at least like 1/r and is >= 3 at R,
        # every Markov piece is a power r^q with q >= 16 after the square root, so each halving of r divides every tail
        # piece by more than 8 and the supremum of tail / r^3 over (0, R] is attained on [R/2, R]
        require(min(args) >= 3, 'last-band tail arguments')
        # no piece is capped at 1, so the factor-64 decrease of every piece per halving carries over to each sum
        require(max(qA2, qfar, qx) < 1, 'last-band tail pieces')
        rdiv = r1 / 2
    else:
        rdiv = r0
    tail = tail_num / (36 * klo * klo * zt * rdiv ** 3)
    total = main + tail
    return {'total': total, 'main': main, 'tail': tail, 'zt': zt, 'pbar': pbar, 'termA': termA, 'termB': termB,
            'termC': termC, 'qA2': qA2, 'qfar': qfar, 'qx': qx, 'El2': El2, 'corr': corr, 'min_arg': min(args)}


def phibar_upper(x):
    """Rational upper bound of 1 - Phi(x) for rational x >= 0: the series value for x <= 12, and for x > 12 the Mills bound
    phi(x)/x with exp(-y) <= m!/y^m (m = 40), which stays exact far below the 2^-160 rounding floor."""
    x = Fr(x)
    if x <= 12:
        return Phibar_pt(x).hi
    y = x * x / 2
    m = 40
    return Fr(math.factorial(m)) / y ** m / (x * Fr(5, 2))      # sqrt(2 pi) > 5/2


def gauss_tail2(mu_abs, sd, t):
    """Upper bound of P(|X| > t) for X Gaussian with |mean| <= mu_abs, sd <= sd."""
    if t <= mu_abs:
        return Fr(1)
    return min(Fr(1), 2 * phibar_upper((t - mu_abs) / sd))


def gauss_tail1(mu_abs, sd, t):
    if t <= mu_abs:
        return Fr(1)
    return min(Fr(1), phibar_upper((t - mu_abs) / sd))


# ----------------------------------------------------------------------------- bands, boxes, runs
B_BOXES = ((Fr(0), Fr(1, 64)), (Fr(1, 64), Fr(1, 16)), (Fr(1, 16), Fr(1, 4)), (Fr(1, 4), Fr(1)))
K_BOXES = ((Fr(1, 2), Fr(1)), (Fr(1), Fr(3, 2)), (Fr(3, 2), Fr(7, 4)), (Fr(7, 4), Fr(15, 8)), (Fr(15, 8), Fr(31, 16)),
           (Fr(31, 16), Fr(63, 32)), (Fr(63, 32), Fr(2)))
HIGH_OCTAVES = 3           # octaves [2^-(j+1), 2^-j], j = 6..8 (r up to 1/64), split into 8 sub-bands
TOP_OCTAVES = 4            # octaves j = 9..12, split into 16 sub-bands
LOW_OCTAVES = 16           # octaves j = 13..28, split into 4 sub-bands
R_LAST = Fr(1, 2 ** 29)    # last band [0, 2^-29]


def bands():
    """Sub-bands [r0, r1] covering (0, 1/64]; each octave split into equal sub-bands; the last band is [0, R_LAST]."""
    out = []
    for j in range(6, 9 + TOP_OCTAVES + LOW_OCTAVES):
        hi = Fr(1, 2 ** j)
        lo = hi / 2
        m = 8 if j < 9 else (16 if j < 9 + TOP_OCTAVES else 4)
        for i in range(m):
            out.append((lo + (hi - lo) * i / m, lo + (hi - lo) * (i + 1) / m))
    out.append((Fr(0), R_LAST))
    require(min(b[0] for b in out) == 0 and max(b[1] for b in out) == Fr(1, 64), 'band cover')
    return sorted(out)


def up(x, digits=6):
    """Decimal string of a rational rounded UP to `digits` significant digits (as a string float)."""
    x = Fr(x)
    if x <= 0:
        return '0'
    e = len(str(x.numerator // x.denominator)) if x >= 1 else -len(str(x.denominator // x.numerator))
    scale = Fr(10) ** (digits - e)
    n = -((-x.numerator * scale.numerator) // (x.denominator * scale.denominator))
    return str(Fr(n) / scale) if scale.denominator == 1 else '%s' % (Fr(n) / scale)


def dec_down(x, places=4):
    x = Fr(x)
    n = (x.numerator * 10 ** places) // x.denominator
    s = str(abs(n)).rjust(places + 1, '0')
    return ('-' if n < 0 else '') + s[:-places] + '.' + s[-places:]


def dec_up(x, places=4):
    x = Fr(x)
    n = -((-x.numerator * 10 ** places) // x.denominator)
    s = str(abs(n)).rjust(places + 1, '0')
    return ('-' if n < 0 else '') + s[:-places] + '.' + s[-places:]


BOXES = tuple((bb, kb) for bb in B_BOXES for kb in K_BOXES)      # the order of the per-box lists in a band record


def band_record(args):
    """Per band: the certified bound of sup Q^W(G_r^c)/r^3 (rounded up, 4 places) and the floor of Z_r/r^2 (rounded down,
    6 places) for each of the 28 boxes in BOXES order, and the largest tail part (rounded up, 12 places)."""
    r0, r1 = args
    law = band_law(r0, r1)
    last = (r0 == 0)
    bound, zfloor, tails = [], [], []
    for bb, kb in BOXES:
        res = box_bound(law, bb, kb, r0, r1, last_band=last)
        bound.append(dec_up(res['total']))
        zfloor.append(dec_down(36 * kb[0] * kb[0] * res['zt'], 6))
        tails.append(res['tail'])
    return {'r': [str(r0), str(r1)], 'bound': bound, 'zfloor': zfloor, 'tail_max': dec_up(max(tails), 12)}


def full_run(procs):
    bl = bands()
    with multiprocessing.Pool(procs) as pool:
        recs = pool.map(band_record, bl)
    return assemble(recs)


def assemble(recs):
    table = {}
    for rs in R_STARS:
        mx, arg, zmin = Fr(0), None, None
        for rec in recs:
            if Fr(rec['r'][1]) <= rs:
                for (bb, kb), bs, zs in zip(BOXES, rec['bound'], rec['zfloor']):
                    v = Fr(bs)
                    if v > mx:
                        mx, arg = v, {'r': rec['r'], 'b': [str(bb[0]), str(bb[1])], 'k': [str(kb[0]), str(kb[1])]}
                    z = Fr(zs)
                    zmin = z if zmin is None or z < zmin else zmin
        table[str(rs)] = {'C': str(mx), 'argmax': arg, 'C_over_cG02': dec_up(mx / Fr('5324360.4426'), 6),
                          'C_rstar3': dec_up(mx * rs ** 3, 10), 'z_star': str(zmin)}
    return {'schema': 1, 'object': 'CL-C8-THEOREM-A-CONSTANTS-PLANAR-20260930-v1', 'scientific_effect': 'NONE',
            'certified': True, 'mutant': MUT, 'L_min': L_MIN,
            'band': {'b': [str(BAND_B[0]), str(BAND_B[1])], 'k': [str(BAND_K[0]), str(BAND_K[1])]},
            'parameters': params(), 'C_table': table, 'bands': recs}


def params():
    return {'PBITS': PBITS, 'NX': NX, 'NB': NB, 'X0': str(X0), 'THETA': str(THETA), 'THETA_E': str(THETA_E),
            'R_STARS': [str(x) for x in R_STARS], 'HIGH_OCTAVES': HIGH_OCTAVES, 'TOP_OCTAVES': TOP_OCTAVES,
            'LOW_OCTAVES': LOW_OCTAVES, 'R_LAST': str(R_LAST),
            'B_BOXES': [[str(a), str(b)] for a, b in B_BOXES], 'K_BOXES': [[str(a), str(b)] for a, b in K_BOXES]}


def results_text(res):
    """RESULTS.json layout: the summary indented, then one line per band record."""
    head = json.dumps({key: val for key, val in res.items() if key != 'bands'}, indent=1, sort_keys=True)
    lines = ',\n'.join('  ' + json.dumps(rec, sort_keys=True) for rec in res['bands'])
    return head[:-2] + ',\n "bands": [\n' + lines + '\n ]\n}\n'


def write_results(res):
    with open(os.path.join(HERE, 'RESULTS.json'), 'w') as fh:
        fh.write(results_text(res))


def load_results():
    with open(os.path.join(HERE, 'RESULTS.json')) as fh:
        return json.load(fh)


def replay_sample():
    """Band indices replayed by --check: the band ending at each r_*, the bands ending at 2^-14, 2^-20, 2^-26, the last band."""
    bl = bands()
    idx = []
    for rs in R_STARS:
        j = max(i for i, b in enumerate(bl) if b[1] == rs)
        idx.append(j)
    idx += [i for i, b in enumerate(bl) if b[1] in (Fr(1, 2 ** 14), Fr(1, 2 ** 20), Fr(1, 2 ** 26))]
    idx.append(0)
    return sorted(set(idx))


def check_run(procs, full=False):
    ref = load_results()
    with open(os.path.join(HERE, 'RESULTS.json')) as fh:
        require(fh.read() == results_text(ref), 'RESULTS.json is not in the canonical layout')
    require(ref['parameters'] == params(), 'parameters differ from RESULTS.json')
    require(ref['mutant'] is None, 'RESULTS.json produced under a mutant')
    require(abs(PI.mid() - Fr('3.14159265358979323846')) < Fr(1, 10 ** 19) and PI.width() < Fr(1, 10 ** 30), 'pi enclosure')
    require(abs(Phi(IV(1)).mid() - Fr('0.841344746068542948585')) < Fr(1, 10 ** 19), 'Phi(1) enclosure')
    bl = bands()
    require([rec['r'] for rec in ref['bands']] == [[str(a), str(b)] for a, b in bl], 'band list differs')
    idx = list(range(len(bl))) if full else replay_sample()
    with multiprocessing.Pool(procs) as pool:
        recs = pool.map(band_record, [bl[i] for i in idx])
    for i, rec in zip(idx, recs):
        require(rec == ref['bands'][i], 'band %d (%s) differs from RESULTS.json' % (i, rec['r']))
    # the table is the maximum over the stored records
    require(assemble(ref['bands'])['C_table'] == ref['C_table'], 'C table is not the maximum of the stored bounds')
    # sanity: every C exceeds the sharp reference-kernel cap coefficient c_G(0, 2) of Math-#203 (a lower bound for every
    # cap-route constant valid for all L >= 10, since c_G^{L,R} -> c_G^{ref} as L -> infinity)
    for rs, row in ref['C_table'].items():
        require(Fr(row['C']) > Fr('5324360.4426'), 'C below the sharp cap coefficient')
    print(json.dumps({'check': 'ok', 'bands_replayed': len(idx), 'C_table': {rs: row['C'] for rs, row in ref['C_table'].items()}, 'mutant': MUT}))


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--check-full', action='store_true')
    ap.add_argument('--mutant', choices=MUTANTS)
    ap.add_argument('--procs', type=int, default=4)
    ap.add_argument('--mc', nargs=5, metavar=('R', 'B', 'K', 'N', 'SEED'), help='floating end-to-end control')
    args = ap.parse_args()
    MUT = args.mutant
    if args.mc:
        rr, bb, kk, nn, sd = args.mc
        print(json.dumps(mc_event(float(Fr(rr)), float(Fr(bb)), float(Fr(kk)), int(nn), int(sd))))
        return
    if args.check or args.check_full:
        check_run(args.procs, full=args.check_full)
        return
    res = full_run(args.procs)
    write_results(res)
    print(json.dumps({rs: row['C'] for rs, row in res['C_table'].items()}))



# ----------------------------------------------------------------------------- floating control (not part of the certificate)
def mc_event(r, b, k, n, seed, deg=8, grid=9):
    """End-to-end Monte Carlo of Q^W(G_r^c) / r^3 and Z_r / r^2 for the reference kernel (floating point): the Taylor jet of
    order deg at the midpoint is sampled under Q, the field near D is rebuilt from it, W_r and G_r (M_3, M_4 on a grid of D)
    are evaluated directly from the definitions."""
    import random
    pins, _ = functionals()
    P = [pins[nm] for nm in PIN_NAMES]
    jets = [(i, m - i) for m in range(deg + 1) for i in range(m, -1, -1)]
    J = [[term(1, 0, a, bb, X0PT)] for (a, bb) in jets]

    def ev(F, G, key):
        ser, w, _ = pair_series(F, G, key)
        return sum(float(c) * r ** p for p, c in ser.items())
    Spp = [[ev(P[i], P[j], ('p', i, j)) for j in range(6)] for i in range(6)]
    Sjp = [[ev(J[i], P[j], ('jp', deg, i, j)) for j in range(6)] for i in range(len(J))]
    Sjj = [[ev(J[i], J[j], ('jj', deg, i, j)) for j in range(len(J))] for i in range(len(J))]

    def solve(A, bv):
        m = len(A)
        M = [A[i][:] + [bv[i]] for i in range(m)]
        for c in range(m):
            p = max(range(c, m), key=lambda i: abs(M[i][c]))
            M[c], M[p] = M[p], M[c]
            for i in range(c + 1, m):
                f = M[i][c] / M[c][c]
                for j in range(c, m + 1):
                    M[i][j] -= f * M[c][j]
        x = [0.0] * m
        for i in reversed(range(m)):
            x[i] = (M[i][m] - sum(M[i][j] * x[j] for j in range(i + 1, m))) / M[i][i]
        return x
    vr = [b - k * r ** 3 / 2, -k * r * r, 12 * k, 0, 0, 0]
    Wt = [solve(Spp, Sjp[i]) for i in range(len(J))]
    mu = [sum(Wt[i][j] * vr[j] for j in range(6)) for i in range(len(J))]
    C = [[Sjj[i][j] - sum(Wt[i][l] * Sjp[j][l] for l in range(6)) for j in range(len(J))] for i in range(len(J))]
    # symmetric square root (Jacobi)
    m = len(J)
    A = [row[:] for row in C]
    V = [[float(i == j) for j in range(m)] for i in range(m)]
    for _ in range(100):
        off = sum(A[p][q] ** 2 for p in range(m) for q in range(p + 1, m))
        if off < 1e-26:
            break
        for p in range(m - 1):
            for q in range(p + 1, m):
                if abs(A[p][q]) < 1e-300:
                    continue
                th = 0.5 * math.atan2(2 * A[p][q], A[q][q] - A[p][p])
                c, s = math.cos(th), math.sin(th)
                for kk in range(m):
                    akp, akq = A[kk][p], A[kk][q]
                    A[kk][p], A[kk][q] = c * akp - s * akq, s * akp + c * akq
                for kk in range(m):
                    apk, aqk = A[p][kk], A[q][kk]
                    A[p][kk], A[q][kk] = c * apk - s * aqk, s * apk + c * aqk
                for kk in range(m):
                    vkp, vkq = V[kk][p], V[kk][q]
                    V[kk][p], V[kk][q] = c * vkp - s * vkq, s * vkp + c * vkq
    lam = [max(A[i][i], 0.0) for i in range(m)]
    S = [[sum(V[i][kk] * math.sqrt(lam[kk]) * V[j][kk] for kk in range(m)) for j in range(m)] for i in range(m)]
    fact = [math.factorial(i) for i in range(deg + 2)]
    pts = [(-2 * r + 4 * r * i / (grid - 1), -2 * r + 4 * r * j / (grid - 1)) for i in range(grid) for j in range(grid)]

    def deriv(cf, a0, b0, x, y):
        tot = 0.0
        for idx, (a, bb) in enumerate(jets):
            if a >= a0 and bb >= b0:
                tot += cf[idx] * x ** (a - a0) * y ** (bb - b0) / (fact[a - a0] * fact[bb - b0])
        return tot
    rng = random.Random(seed)
    num = den = 0.0
    acap = 4 / (3 * k)
    for _ in range(n):
        z = [rng.gauss(0, 1) for _ in jets]
        cf = [mu[i] + sum(S[i][j] * z[j] for j in range(m)) for i in range(m)]
        hM = [deriv(cf, 2, 0, -r / 2, 0.0), deriv(cf, 1, 1, -r / 2, 0.0), deriv(cf, 0, 2, -r / 2, 0.0)]
        hS = [deriv(cf, 2, 0, r / 2, 0.0), deriv(cf, 1, 1, r / 2, 0.0), deriv(cf, 0, 2, r / 2, 0.0)]
        dM = hM[0] * hM[2] - hM[1] ** 2
        dS = hS[0] * hS[2] - hS[1] ** 2
        if not (hM[0] < 0 and dM > 0 and dS < 0):
            continue
        Wv = abs(dM * dS)
        den += Wv
        lamv = -hM[2]
        M3 = max(abs(deriv(cf, a, 3 - a, x, y)) for (x, y) in pts for a in range(4))
        M4 = max(abs(deriv(cf, a, 4 - a, x, y)) for (x, y) in pts for a in range(5))
        if not (lamv > acap * r * M3 * M3 and r * M4 <= 3 * k / 10):
            num += Wv
    return {'r': r, 'b': b, 'k': k, 'n': n, 'seed': seed, 'QW_Gc_over_r3': num / den / r ** 3, 'Z_over_r2': den / n / r ** 2}


if __name__ == '__main__':
    main()
