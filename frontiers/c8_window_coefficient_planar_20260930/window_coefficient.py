"""Compact-window coefficient c_{B,K} of [LP] Theorem B in the plane: exact factorization, closed forms, certified values.

Standard library only. Run from anywhere:  python -B -S window_coefficient.py [--mutant NAME]
Every printed interval [lo, hi] is a rigorous enclosure: interval arithmetic over `decimal` with directed rounding (exp and
sqrt are correctly rounded by the decimal module and widened by two units in the last place), pi from Machin's formula
with the alternating-series bracket, fractional powers from exact integer roots, erf and the lower incomplete gamma
function from their positive series with a geometric tail bound, Owen's T and arctan from alternating series bracketed by
consecutive partial sums. Nothing is fitted, sampled or extrapolated.

Object certified ([LP] = imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md, (11.3) with the section 15
factorization, at d = 2):

  c_{B,K} = 144 int_{S^1} p_G(0) p_V(0) [ int_B p_{f|V=0}(b) E[A^2 1{A<0} | f=b, V=0] db ] [ int_K k^(4/3) phi_tau(12k) dk ] dsigma(u),

with G = grad f, V = (f_uu, f_uw), A = f_ww, tau^2 = Var(f_uuu | G=0), all in the frame (u, w), w = u^perp.  For the
Euclidean reference kernel exp(-|z|^2/2): p_G(0) = 1/(2 pi), p_V(0) = 1/(2 pi sqrt3), f | V=0 ~ N(0, 2/3),
A | f=b, V=0 ~ N(-b, 2) (derived in NOTE section 2 from the jet covariances; it is the contact law [LP] (5.4)
as quoted in Math-#195 section 1), tau^2 = 6, and the coefficient factorizes exactly:

  c_{B,K} = c_{2,ref} F_B G_K,   c_{2,ref} = 2 Gamma(7/6) (3/2)^(1/3) / (3 sqrt3 pi^(3/2))      (SIDE24 (1), d = 2)
  G_K = P(7/6, 12 k_+^2) - P(7/6, 12 k_-^2)                       (regularized lower incomplete gamma)
  F_B = Psi(b_+ sqrt(3/2)) - Psi(b_- sqrt(3/2)),
  Psi(x) = Phi(x) - 2 T(x, 1/sqrt3) - (1/2) x phi(x) Phi(x/sqrt3) - (sqrt3/(4 pi)) exp(-2x^2/3)   (T = Owen's function).

For the torus kernel K_L (side L >= 10) every covariance entry of the 3-jet in any frame lies within
E_L = 128 (76 L^6 + 15) exp(-L^2/2) of its reference value (NOTE section 3); the same formulas are evaluated over those
entry intervals, so one enclosure covers every frame and every L >= 10, and a sharper one L = 24.  The reference expression
in d = 3 (SIDE24 reference law A = -b I + Q, Q the 2x2 GOE with diagonal variance 2) is enclosed through the closed form

  m_{3,b} = (b^3 + b) phi(b) + (b^4 + 2b^2 + 7) Phi(b) - 4 sqrt2 exp(-b^2/4) Phi(b/sqrt2),

whose Gaussian mean over b ~ N(0, 2/3) is D_2 = 29/6 - sqrt6 (SIDE24 section 1), a rule below.
The theorems behind (11.3) are consumed at their stated scopes; this script certifies arithmetic. Scientific effect: NONE.
"""
import argparse
import json
import math
import sys
import time
from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN, setcontext
from fractions import Fraction as Fr

MUTANTS = ("no-owen", "mean-sign", "slope", "gamma-shape", "image-dropped", "shell-count", "tail-dropped", "prefactor",
           "d3-cross", "window-swap")
MUT = None

PREC = 60
CF = Context(prec=PREC, rounding=ROUND_FLOOR, Emin=-9999999, Emax=9999999)
CC = Context(prec=PREC, rounding=ROUND_CEILING, Emin=-9999999, Emax=9999999)
CE = Context(prec=PREC, rounding=ROUND_HALF_EVEN, Emin=-9999999, Emax=9999999)
# Every arithmetic step below names one of the three contexts.  Operator syntax on Decimals (unary minus, int * Decimal,
# Decimal - Decimal) rounds to the thread's current context, whose default precision is 28: that would silently shorten a
# 60-digit endpoint.  The current context is therefore widened as a safety net, and rule LIBRARY_EXACT compares exp and
# sqrt of the decimal module, and the negation, against exact rational brackets.
setcontext(Context(prec=2 * PREC + 20, rounding=ROUND_HALF_EVEN, Emin=-9999999, Emax=9999999))
ZERO, ONE, HALF = Decimal(0), Decimal(1), Decimal("0.5")
INF = math.inf
ROOT_DIGITS = 70
SIDE24_D2 = ("0.07340691930603427103", "0.07340691930603427104")   # coefficients/side24_v1/ENCLOSURE.json, dimensions.2
PINNED = {
    "c_2_ref": "0.0734069193060342710301359629577740500176642446843",
    "F|[0,1]": "0.4826434564192741302043420464555699272914090372616",
    "G|[1/2,2]": "0.0673717334256416673488444184744027734315404221598",
    "Gamma(7/6)": "0.9277193336300392007083494825346210185664665191454",
    "pi": "3.14159265358979323846264338327950288419716939937510",
}


def ulp(x):
    if x == 0:
        return Decimal(1).scaleb(-PREC - 30)
    return Decimal(1).scaleb(x.adjusted() - PREC + 1)


class Iv:
    """Closed interval [lo, hi] of Decimals; every operation encloses the exact result."""
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        if hi is None:
            hi = lo
        if lo > hi:
            raise ValueError("empty interval")
        self.lo, self.hi = lo, hi

    @staticmethod
    def frac(q):
        q = Fr(q)
        n, d = Decimal(q.numerator), Decimal(q.denominator)
        return Iv(CF.divide(n, d), CC.divide(n, d))

    @staticmethod
    def of(x):
        return x if isinstance(x, Iv) else Iv.frac(x)

    def __add__(a, b):
        b = Iv.of(b)
        return Iv(CF.add(a.lo, b.lo), CC.add(a.hi, b.hi))
    __radd__ = __add__

    def __neg__(a):
        return Iv(a.hi.copy_negate(), a.lo.copy_negate())          # exact: unary minus would round to the default context

    def __sub__(a, b):
        b = Iv.of(b)
        return Iv(CF.subtract(a.lo, b.hi), CC.subtract(a.hi, b.lo))

    def __rsub__(a, b):
        return Iv.of(b) - a

    def __mul__(a, b):
        b = Iv.of(b)
        c = [(x, y) for x in (a.lo, a.hi) for y in (b.lo, b.hi)]
        return Iv(min(CF.multiply(x, y) for x, y in c), max(CC.multiply(x, y) for x, y in c))
    __rmul__ = __mul__

    def __truediv__(a, b):
        b = Iv.of(b)
        if b.lo <= 0 <= b.hi:
            raise ZeroDivisionError("interval division by an interval containing 0")
        c = [(x, y) for x in (a.lo, a.hi) for y in (b.lo, b.hi)]
        return Iv(min(CF.divide(x, y) for x, y in c), max(CC.divide(x, y) for x, y in c))

    def __rtruediv__(a, b):
        return Iv.of(b) / a

    def sq(a):
        if a.lo <= 0 <= a.hi:
            return Iv(ZERO, max(CC.multiply(a.lo, a.lo), CC.multiply(a.hi, a.hi)))
        return a * a

    def exp(a):
        lo, hi = CE.exp(a.lo), CE.exp(a.hi)
        return Iv(max(ZERO, CF.subtract(lo, CC.multiply(Decimal(2), ulp(lo)))), CC.add(hi, CC.multiply(Decimal(2), ulp(hi))))

    def sqrt(a):
        if a.lo < 0:
            raise ValueError("sqrt of an interval with negative part")
        lo, hi = CE.sqrt(a.lo), CE.sqrt(a.hi)
        return Iv(max(ZERO, CF.subtract(lo, CC.multiply(Decimal(2), ulp(lo)))), CC.add(hi, CC.multiply(Decimal(2), ulp(hi))))

    def width(a):
        return CC.subtract(a.hi, a.lo)

    def contains(a, x):
        x = Iv.of(x)
        return a.lo <= x.lo and x.hi <= a.hi

    def intersects(a, b):
        return a.lo <= b.hi and b.lo <= a.hi

    def mag(a):
        return max(abs(a.lo), abs(a.hi))

    def mid_float(a):
        return float((a.lo + a.hi) / 2)

    def pair(a):
        return [str(a.lo), str(a.hi)]


def hull(a, b):
    return Iv(min(a.lo, b.lo), max(a.hi, b.hi))


# ---------------- rigorous constants and special functions
def inroot(N, n):
    """floor(N ** (1/n)) for integers N >= 0, n >= 1: integer Newton iteration started above the root."""
    if N < 2:
        return N
    x = 1 << ((N.bit_length() + n - 1) // n)
    while True:
        y = ((n - 1) * x + N // pow(x, n - 1)) // n
        if y >= x:
            break
        x = y
    if not (pow(x, n) <= N < pow(x + 1, n)):
        raise ValueError("integer root failed")
    return x


def root_frac(q, n):
    """Rigorous bracket of q ** (1/n) for a positive rational q, width 10^-ROOT_DIGITS."""
    q = Fr(q)
    if q <= 0:
        raise ValueError("root of a nonpositive number")
    p, d = q.numerator, q.denominator
    scale = 10 ** ROOT_DIGITS
    r = inroot(p * d ** (n - 1) * scale ** n, n)
    den = d * scale
    return Iv(Iv.frac(Fr(r, den)).lo, Iv.frac(Fr(r + 1, den)).hi)


def root_iv(x, n):
    """x ** (1/n) for an interval x > 0 (monotone: endpoint brackets)."""
    return Iv(root_frac(Fr(x.lo), n).lo, root_frac(Fr(x.hi), n).hi)


def pi_interval():
    def atan_inv(n, terms):
        x = Fr(1, n)
        partial, sums = Iv(ZERO), []
        for m in range(terms + 2):
            t = Iv.frac(x ** (2 * m + 1) / (2 * m + 1))
            partial = partial + t if m % 2 == 0 else partial - t
            sums.append(partial)
        return hull(sums[-1], sums[-2])              # alternating series with decreasing terms
    return atan_inv(5, 44) * 16 - atan_inv(239, 22) * 4


PI = pi_interval()
SQRT2 = Iv.frac(2).sqrt()
SQRT3 = Iv.frac(3).sqrt()
SQRT2PI = (2 * PI).sqrt()
SQRTPI = PI.sqrt()
TINY = Decimal(10) ** (-PREC - 8)


def erf_point(x, coarse=False):
    """erf(x) at a Decimal point: (2/sqrt pi) exp(-x^2) sum_n 2^n x^(2n+1)/(2n+1)!!, positive terms; once the term ratio
    2x^2/(2n+3) is at most 1/2 the omitted tail is at most twice the first omitted term.  coarse=True stops at that point
    (a valid, wider enclosure used by TRUNCATION_NESTING); the production run continues until the tail is negligible."""
    tail = MUT != "tail-dropped"
    coarse = coarse or not tail
    if x < 0:
        return -erf_point(-x, coarse)
    if x == 0:
        return Iv(ZERO)
    X = Iv(x)
    x2 = X * X
    t, S, n = X, Iv(ZERO), 0
    while True:
        S = S + t
        ratio = x2 * 2 / (2 * n + 3)
        t = t * ratio
        n += 1
        if ratio.hi <= HALF and (coarse or t.hi < S.lo * TINY):
            break
        if n > 200000:
            raise RuntimeError("erf series did not converge")
    rest = Iv(ZERO, CC.multiply(Decimal(2), t.hi)) if tail else Iv(ZERO)
    return (S + rest) * (-x2).exp() * 2 / SQRTPI


def erf_iv(x, coarse=False):
    return Iv(erf_point(x.lo, coarse).lo, erf_point(x.hi, coarse).hi)


def Phi(x):
    return (1 + erf_iv(x / SQRT2)) / 2


def Phi_bar(x):
    return (1 - erf_iv(x / SQRT2)) / 2


def phi(x):
    return (-(x.sq()) / 2).exp() / SQRT2PI


def atan_iv(a, N=90):
    """arctan(a) for an interval 0 <= a <= 1: halve the argument, then the alternating series bracketed by consecutive
    partial sums (for each fixed argument the terms decrease, so the value lies between them)."""
    a1 = a / (1 + (1 + a.sq()).sqrt())
    a1sq, p, S, prev = a1.sq(), a1, Iv(ZERO), None
    for n in range(N + 1):
        t = p / (2 * n + 1)
        prev = S
        S = S + t if n % 2 == 0 else S - t
        p = p * a1sq
    return 2 * hull(prev, S)


def owen_T(h, a, N=160, bracket=True):
    """Owen's T(h, a) = (1/2 pi) int_0^a exp(-h^2 (1+x^2)/2)/(1+x^2) dx for 0 <= a <= 1, by Owen's series
    T = (1/2 pi)[arctan a - sum_j c_j a^(2j+1)],  c_j = (-1)^j/(2j+1) [1 - exp(-h^2/2) sum_{i<=j} (h^2/2)^i/i!].
    The bracket is P(Poisson(h^2/2) > j), decreasing in j, so for fixed (h, a) the terms alternate with decreasing size and
    the sum lies between consecutive partial sums; interval evaluation of both encloses it for every point of the intervals."""
    if MUT == "no-owen":
        return Iv(ZERO)
    h2 = h.sq() / 2
    e = (-h2).exp()
    pois, term, apow, a2 = Iv(ONE), Iv(ONE), a, a.sq()
    S, prev = Iv(ZERO), None
    for j in range(N + 1):
        if j > 0:
            term = term * h2 / j
            pois = pois + term
        cj = apow / (2 * j + 1) * (1 - e * pois)
        prev = S
        S = S + cj if j % 2 == 0 else S - cj
        apow = apow * a2
    val = hull(prev, S) if bracket else S
    return (atan_iv(a) - val) / (2 * PI)


def owen_T_eval(h, a):
    if MUT == "tail-dropped":
        return owen_T(h, a, N=6, bracket=False)
    return owen_T(h, a)


def SHAPE():
    """Shape parameter of the gap-window incomplete gamma factor (mutant gamma-shape perturbs it)."""
    return Fr(4, 3) if MUT == "gamma-shape" else Fr(7, 6)


def gamma_lower_point(x, a, coarse=False):
    """gamma(a, x) = int_0^x s^(a-1) e^-s ds = x^a e^-x sum_n x^n/(a (a+1) ... (a+n)), positive terms; once the term ratio
    x/(a+n) is at most 1/2 the omitted tail is at most twice the first omitted term. x a Decimal point >= 0, a = 7/6 or 4/3."""
    tail = MUT != "tail-dropped"
    coarse = coarse or not tail
    if x == 0:
        return Iv(ZERO)
    X = Iv(x)
    t, S, n = Iv.frac(1 / a), Iv(ZERO), 0
    while True:
        S = S + t
        n += 1
        ratio = X / Iv.frac(a + n)
        t = t * ratio
        if ratio.hi <= HALF and (coarse or t.hi < S.lo * TINY):
            break
        if n > 200000:
            raise RuntimeError("incomplete gamma series did not converge")
    rest = Iv(ZERO, CC.multiply(Decimal(2), t.hi)) if tail else Iv(ZERO)
    xa = X * root_frac(Fr(x), 6) if a == Fr(7, 6) else X * root_frac(Fr(x), 3)      # x^a
    return xa * (-X).exp() * (S + rest)


def gamma_lower(x, a, coarse=False):
    """gamma(a, x) for an interval x >= 0 or x = INF (monotone in x)."""
    if isinstance(x, float):
        return GAMMA[a]
    return Iv(gamma_lower_point(x.lo, a, coarse).lo, gamma_lower_point(x.hi, a, coarse).hi)


def gamma_complete(a, X=Decimal(120)):
    """Gamma(a) = gamma(a, X) + Gamma(a, X), 1 < a < 2, with X^(a-1) e^-X <= Gamma(a, X) <= X^(a-1) e^-X / (1 - (a-1)/X)."""
    low = gamma_lower_point(X, a)
    xa1 = root_frac(Fr(X), 6) if a == Fr(7, 6) else root_frac(Fr(X), 3)
    up = xa1 * (-Iv(X)).exp()
    return low + Iv(up.lo, (up / (1 - Iv.frac(a - 1) / Iv(X))).hi)


GAMMA = {Fr(7, 6): gamma_complete(Fr(7, 6)), Fr(4, 3): gamma_complete(Fr(4, 3))}
GAMMA76 = GAMMA[Fr(7, 6)]
CBRT32 = root_frac(Fr(12), 3) / 2                       # (3/2)^(1/3) = 12^(1/3)/2
C72 = 1 / (72 * root_frac(Fr(72), 6))                   # 72^(-7/6)
SIGMA_REF = Iv.frac(Fr(2, 3)).sqrt()                    # sd of f | V=0 for the reference kernel
D2_EXACT = Iv.frac(Fr(29, 6)) - Iv.frac(6).sqrt()        # SIDE24 cone moment m = 2
C2_REF = 2 * GAMMA76 * CBRT32 / (3 * SQRT3 * PI * SQRTPI)                       # SIDE24 (1), d = 2, D_1 = 4/3
C3_REF = GAMMA76 * CBRT32 * D2_EXACT / (2 * SQRT3 * PI * PI * SQRTPI)             # SIDE24 (1), d = 3


# ---------------- the Gaussian integrals int_{-inf}^x t^n phi(t) Phi(a t) dt, n <= 4, and their limits
def G_finite(x, a):
    rho2 = 1 + a.sq()
    rho = rho2.sqrt()
    Phx, phx, Phax = Phi(x), phi(x), Phi(a * x)
    T = owen_T_eval(x, a)
    Erho = (-(rho2 * x.sq()) / 2).exp()
    Phrx = Phi(rho * x)
    x2 = x.sq()
    G0 = Phx / 2 - T
    G1 = -phx * Phax + a / (rho * SQRT2PI) * Phrx
    G2 = G0 - x * phx * Phax - a / (2 * PI * rho2) * Erho
    G3 = -x2 * phx * Phax + a / (2 * PI) * (-(x / rho2) * Erho + SQRT2PI / (rho2 * rho) * Phrx) + 2 * G1
    G4 = -x * x2 * phx * Phax - a / (2 * PI) * (x2 / rho2 + 2 / rho2.sq()) * Erho + 3 * G2
    return [G0, G1, G2, G3, G4]


def G_limit(a, sign):
    if sign < 0:
        return [Iv(ZERO)] * 5
    rho2 = 1 + a.sq()
    rho = rho2.sqrt()
    g1 = a / (rho * SQRT2PI)
    return [Iv.frac(Fr(1, 2)), g1, Iv.frac(Fr(1, 2)), a / (rho2 * rho * SQRT2PI) + 2 * g1, Iv.frac(Fr(3, 2))]


def G_at(x, a):
    """x an interval or +-INF."""
    if isinstance(x, float):
        return G_limit(a, 1 if x > 0 else -1)
    return G_finite(x, a)


# ---------------- planar 3-jet pipeline for a covariance whose entries are within E of the reference values
class Planar:
    """Frame (u, w): odd block (f_u, f_w, f_uuu) independent of the even block (f, f_uu, f_uw, f_ww) for any even kernel.
    Reference entries: Var f = 1; Var f_u = Var f_w = 1; Var f_uuu = 15, Cov(f_uuu, f_u) = -3; Cov(f, f_uu) = Cov(f, f_ww) = -1;
    Var f_uu = Var f_ww = 3, Cov(f_uu, f_ww) = 1, Var f_uw = 1; all other entries 0.  Each entry other than Var f = 1 is
    widened by +-E (E = 0: the reference kernel itself)."""

    def __init__(self, E):
        E = Iv.of(E)
        def ent(v):
            return Iv.frac(v) + Iv(-E.hi, E.hi)
        g11, g22, g12 = ent(1), ent(1), ent(0)
        detG = g11 * g22 - g12.sq()
        self.pG = 1 / (2 * PI * detG.sqrt())
        c1, c2, t66 = ent(-3), ent(0), ent(15)
        self.tau2 = t66 - (c1.sq() * g22 - 2 * c1 * c2 * g12 + c2.sq() * g11) / detG
        v11, v22, v12 = ent(3), ent(1), ent(0)                      # Sigma_V for V = (f_uu, f_uw)
        detV = v11 * v22 - v12.sq()
        self.pV = 1 / (2 * PI * detV.sqrt())
        def q(x, y):                                               # x^T Sigma_V^{-1} y
            return (x[0] * y[0] * v22 - (x[0] * y[1] + x[1] * y[0]) * v12 + x[1] * y[1] * v11) / detV
        cf = (ent(-1), ent(0))                                     # Cov(f, V)
        cA = (ent(1), ent(0))                                      # Cov(f_ww, V)
        self.sig2 = 1 - q(cf, cf)                                  # Var(f | V=0)
        covfA = ent(-1) - q(cf, cA)                                # Cov(f, A | V=0)
        varA = ent(3) - q(cA, cA)                                  # Var(A | V=0)
        self.alpha = covfA / self.sig2                             # A | f=b, V=0 has mean alpha b
        if MUT == "mean-sign":
            self.alpha = -self.alpha
        self.s2 = varA - covfA.sq() / self.sig2                    # and variance s^2
        self.sig = self.sig2.sqrt()
        self.s = self.s2.sqrt()
        self.a = -self.alpha * self.sig / self.s                   # slope of Phi in the b-integral after b = sig x
        if MUT == "slope":
            self.a = self.a * Iv.frac(Fr(11, 10))
        self.D1 = (self.s2 + self.alpha.sq() * self.sig2) / 2     # E[A^2 1{A<0} | V=0] = Var(A|V=0)/2
        self.tau43 = root_iv(self.tau2.sq(), 3)                    # tau^(4/3)
        self.rho2 = 1 + self.a.sq()

    def psi(self, x):
        """int_{-inf}^x phi(t) [(1 + a^2 t^2) Phi(a t) + a t phi(a t)] dt  (b-integral kernel after b = sig x, divided by s^2)."""
        if isinstance(x, float):
            return self.rho2 / 2 if x > 0 else Iv(ZERO)
        G = G_finite(x, self.a)
        return G[0] + self.a.sq() * G[2] - self.a / (2 * PI * self.rho2) * (-(self.rho2 * x.sq()) / 2).exp()

    def xval(self, b):
        return b if isinstance(b, float) else Iv.frac(b) / self.sig

    def b_integral(self, B):
        """int_B p_{f|V=0}(b) E[A^2 1{A<0} | f=b, V=0] db."""
        lo, hi = B
        if MUT == "window-swap":
            lo, hi = hi, lo
        return self.s2 * (self.psi(self.xval(hi)) - self.psi(self.xval(lo)))

    def k_integral(self, K):
        """int_K k^(4/3) phi_tau(12 k) dk = tau^(4/3) 72^(-7/6) [gamma(7/6, 72 k_+^2/tau^2) - gamma(7/6, 72 k_-^2/tau^2)] / (2 sqrt(2 pi))."""
        lo, hi = K
        def s(k):
            return k if isinstance(k, float) else 72 * Iv.frac(k * k) / self.tau2
        a = SHAPE()
        return self.tau43 * C72 * (gamma_lower(s(hi), a) - gamma_lower(s(lo), a)) / (2 * SQRT2PI)

    def coefficient(self, B, K):
        pref = 72 if MUT == "prefactor" else 144
        return pref * 2 * PI * self.pG * self.pV * self.b_integral(B) * self.k_integral(K)


# ---------------- reference closed forms (independent code path)
def Psi_ref(x):
    """Psi(x) = Phi(x) - 2 T(x, 1/sqrt3) - x phi(x) Phi(x/sqrt3)/2 - sqrt3/(4 pi) exp(-2x^2/3); Psi(-inf) = 0, Psi(inf) = 1."""
    if isinstance(x, float):
        return Iv(ONE) if x > 0 else Iv(ZERO)
    a = 1 / SQRT3
    return Phi(x) - 2 * owen_T_eval(x, a) - x * phi(x) * Phi(x / SQRT3) / 2 - SQRT3 / (4 * PI) * (-(x.sq()) * 2 / 3).exp()


def x_ref(b):
    return b if isinstance(b, float) else Iv.frac(b) / SIGMA_REF


def F_ref(B):
    lo, hi = B
    if MUT == "window-swap":
        lo, hi = hi, lo
    return Psi_ref(x_ref(hi)) - Psi_ref(x_ref(lo))


def F_ref_symmetric(beta):
    """Symmetric window B = [-beta, beta]: F = erf(beta sqrt3/2) - beta sqrt3 exp(-3 beta^2/4)/(4 sqrt pi)."""
    beta = Iv.frac(beta)
    return erf_iv(beta * SQRT3 / 2) - beta * SQRT3 * (-(beta.sq()) * 3 / 4).exp() / (4 * SQRTPI)


def P_reg(s):
    """Regularized lower incomplete gamma P(7/6, s) (s an interval >= 0 or INF)."""
    a = SHAPE()
    return gamma_lower(s, a) / GAMMA76


def G_ref(K):
    lo, hi = K
    def s(k):
        return k if isinstance(k, float) else 12 * Iv.frac(k * k)
    return P_reg(s(hi)) - P_reg(s(lo))


def F3_ref(B):
    """d = 3 reference window factor: int_B phi_{2/3}(b) m_{3,b} db / D_2 with
    m_{3,b} = (b^3 + b) phi(b) + (b^4 + 2 b^2 + 7) Phi(b) - 4 sqrt2 exp(-b^2/4) Phi(b/sqrt2)."""
    lo, hi = B
    if MUT == "window-swap":
        lo, hi = hi, lo
    sig = SIGMA_REF
    def term_i(b):                                # int phi_{2/3}(b) (b^3 + b) phi(b) db = -(2b^2/5 + 18/25) exp(-5b^2/4) / (2 pi sig)
        if isinstance(b, float):
            return Iv(ZERO)
        b = Iv.frac(b)
        return -(b.sq() * 2 / 5 + Iv.frac(Fr(18, 25))) * (-(b.sq()) * 5 / 4).exp() / (2 * PI * sig)
    def term_ii(b):                               # int phi_{2/3}(b) (b^4 + 2 b^2 + 7) Phi(b) db, b = sig x
        G = G_at(b if isinstance(b, float) else Iv.frac(b) / sig, sig)
        return sig.sq().sq() * G[4] + 2 * sig.sq() * G[2] + 7 * G[0]
    def term_iii(b):                              # int phi_{2/3}(b) 4 sqrt2 exp(-b^2/4) Phi(b/sqrt2) db = (4/sig) G_0(sqrt2 b; 1/2)
        G = G_at(b if isinstance(b, float) else Iv.frac(b) * SQRT2, Iv.frac(Fr(1, 2)))
        return 4 / sig * G[0]
    cross = Iv.frac(Fr(1, 2)) if MUT == "d3-cross" else Iv(ONE)
    total = (term_i(hi) - term_i(lo)) + (term_ii(hi) - term_ii(lo)) - cross * (term_iii(hi) - term_iii(lo))
    return total / D2_EXACT


# ---------------- image bound for the torus kernel (NOTE section 3)
def image_bound(L):
    """E_L = 128 (76 L^6 + 15) exp(-L^2/2): every unit-direction contraction of D^q K_L(0) - D^q phi(0), q <= 6, in absolute
    value (d = 2, L >= 10; shells |n|_inf = j carry 8 j points, |n|^6 <= 8 j^6, successive shell terms ratio < 1/2)."""
    if MUT == "image-dropped":
        return Iv(ZERO)
    shells = 64 if MUT == "shell-count" else 128
    L = Fr(L)
    return Iv.frac(shells * (76 * L ** 6 + 15)) * (-Iv.frac(L * L / 2)).exp()


# ---------------- floating-point controls (independent formulas; not part of the certificate)
def simpson(f, lo, hi, n=4000):
    h = (hi - lo) / n
    s = f(lo) + f(hi)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(lo + i * h)
    return s * h / 3


def fPhi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def fphi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def fclip(b, sign):
    return (12.0 * sign) if isinstance(b, float) else float(b)


def F2_float(B):
    def m2(b):                                    # Math-#178/#195: m_{2,b} = (b^2 + 2) Phi(b/sqrt2) + b sqrt2 phi(b/sqrt2)
        return (b * b + 2) * fPhi(b / math.sqrt(2)) + b * math.sqrt(2) * fphi(b / math.sqrt(2))
    sig = math.sqrt(2 / 3)
    lo, hi = fclip(B[0], -1), fclip(B[1], 1)
    return 0.75 * simpson(lambda b: math.exp(-b * b / (2 * sig * sig)) / (sig * math.sqrt(2 * math.pi)) * m2(b), lo, hi)


def m3_float(b):                                  # direct double integral: int_0^inf g(v^2) phi(v - b) dv, g from the Rayleigh integral
    def g(w):
        return w * w - 4 * w + 8 - 8 * math.exp(-w / 2)
    return simpson(lambda v: g(v * v) * fphi(v - b), 0.0, 14.0 + abs(b), 1200)


def F3_float(B):
    sig = math.sqrt(2 / 3)
    lo, hi = fclip(B[0], -1), fclip(B[1], 1)
    D2 = 29 / 6 - math.sqrt(6)
    return simpson(lambda b: math.exp(-b * b / (2 * sig * sig)) / (sig * math.sqrt(2 * math.pi)) * m3_float(b), lo, hi, 1600) / D2


def G_float(K):
    lo = float(K[0]) ** (1 / 3)
    hi = (6.0 if isinstance(K[1], float) else float(K[1])) ** (1 / 3)
    full = 0.5 * 12 ** (-7 / 6) * math.gamma(7 / 6)
    return simpson(lambda u: 3 * u ** 6 * math.exp(-12 * u ** 6), lo, hi) / full           # k = u^3


def owen_float(h, a):
    return simpson(lambda x: math.exp(-h * h * (1 + x * x) / 2) / (1 + x * x), 0.0, a) / (2 * math.pi)


# ---------------- main
def fmt10(x):
    return "%.10g" % x


def within(iv, fv, tol):
    """The float control fv lies within tol of the enclosure iv (exact comparisons through CE)."""
    f, t = Decimal(repr(fv)), Decimal(repr(tol))
    return CE.subtract(iv.lo, f) <= t and CE.subtract(f, iv.hi) <= t


def library_exact():
    """exp and sqrt of the decimal module, and the interval negation, against exact rational brackets: e^-q by the
    rational series of e^(-q/64) raised to the 64th power (alternating tail below the last term), sqrt by an integer root."""
    ok = True
    args = [Fr(48) - Fr(51035039649098175696, 10 ** 29), Fr(3), Fr(120), Fr(1, 2), Fr(288), Fr(5, 7)]
    for q in args:
        g = -q / 64
        parts = []
        term, ssum = Fr(1), Fr(0)
        for k in range(0, 60):
            ssum += term
            parts.append(ssum)
            term = term * g / (k + 1)
        lo, hi = min(parts[-1], parts[-2]), max(parts[-1], parts[-2])           # alternating series with decreasing terms
        exact = Iv(Iv.frac(lo ** 64).lo, Iv.frac(hi ** 64).hi)                  # e^-q = (e^(-q/64))^64, both endpoints positive
        X = Iv.frac(q)
        got = (-X).exp()
        ok &= got.intersects(exact) and CC.divide(got.width(), got.lo) < Decimal(10) ** (-PREC + 3)
        r = root_frac(q, 2)
        ok &= X.sqrt().intersects(r) and CC.divide(X.sqrt().width(), r.lo) < Decimal(10) ** (-PREC + 3)
        ok &= (-X).lo == X.hi.copy_negate() and (-X).hi == X.lo.copy_negate()
    return ok


def window_label(B, K):
    def e(v):
        return "inf" if isinstance(v, float) and v > 0 else ("-inf" if isinstance(v, float) else str(Fr(v)))
    return "B=[%s,%s] K=[%s,%s]" % (e(B[0]), e(B[1]), e(K[0]), e(K[1]))


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    args = ap.parse_args()
    MUT = args.mutant
    t0 = time.time()
    if MUT:
        globals()["GAMMA"] = {Fr(7, 6): gamma_complete(Fr(7, 6)), Fr(4, 3): gamma_complete(Fr(4, 3))}

    checks, notes = {}, {}
    ref = Planar(0)
    E10, E24 = image_bound(10), image_bound(24)
    tor10, tor24 = Planar(E10), Planar(E24)

    windows = [
        ("W1 (Math-#195 C8 band)", (Fr(0), Fr(1)), (Fr(1, 2), Fr(2))),
        ("W2", (Fr(-1), Fr(1)), (Fr(1, 2), Fr(2))),
        ("W3", (Fr(-2), Fr(2)), (Fr(1, 4), Fr(4))),
        ("W4", (Fr(-3), Fr(3)), (Fr(1, 10), Fr(10))),
        ("W5", (Fr(-1, 2), Fr(1, 2)), (Fr(1), Fr(3, 2))),
        ("FULL", (-INF, INF), (Fr(0), INF)),
    ]
    b_windows = [(Fr(0), Fr(1)), (Fr(-1), Fr(1)), (Fr(-2), Fr(2)), (Fr(-3), Fr(3)), (Fr(-1, 2), Fr(1, 2)), (Fr(0), INF),
                 (-INF, Fr(0)), (-INF, INF)]
    k_windows = [(Fr(1, 2), Fr(2)), (Fr(1, 4), Fr(4)), (Fr(1, 10), Fr(10)), (Fr(1), Fr(3, 2)), (Fr(1, 2), INF), (Fr(1), INF),
                 (Fr(0), INF)]

    # --- factor tables
    F2 = {window_label(B, (Fr(0), INF)): F_ref(B) for B in b_windows}
    F3 = {window_label(B, (Fr(0), INF)): F3_ref(B) for B in b_windows}
    GK = {window_label((-INF, INF), K): G_ref(K) for K in k_windows}
    F2f = {window_label(B, (Fr(0), INF)): F2_float(B) for B in b_windows}
    F3f = {window_label(B, (Fr(0), INF)): F3_float(B) for B in b_windows}
    GKf = {window_label((-INF, INF), K): G_float(K) for K in k_windows}

    # --- coefficient table
    rows = []
    for name, B, K in windows:
        c_closed = C2_REF * F_ref(B) * G_ref(K)
        rows.append({
            "window": name, "label": window_label(B, K),
            "c_ref_closed_form": c_closed.pair(),
            "c_ref_pipeline": ref.coefficient(B, K).pair(),
            "c_torus_L_ge_10": tor10.coefficient(B, K).pair(),
            "c_torus_L_24": tor24.coefficient(B, K).pair(),
            "fraction_of_c_2_ref": (F_ref(B) * G_ref(K)).pair(),
            "c3_ref_closed_form": (C3_REF * F3_ref(B) * G_ref(K)).pair(),
            "fraction_of_c_3_ref": (F3_ref(B) * G_ref(K)).pair(),
        })

    # --- rules
    tol = 1e-9
    ok = True
    for key in F2:
        for tab, ftab in ((F2, F2f), (F3, F3f)):
            iv, fv = tab[key], ftab[key]
            ok &= within(iv, fv, tol)
    for key in GK:
        iv, fv = GK[key], GKf[key]
        ok &= within(iv, fv, tol)
    owen_pts = [(Fr(0), Fr(1, 2)), (Fr(1), Fr(1, 2)), (Fr(3, 2), Fr(1, 2)), (Fr(2), Fr(4, 5)), (Fr(5, 2), Fr(1))]
    for hq, aq in owen_pts:
        iv, fv = owen_T_eval(Iv.frac(hq), Iv.frac(aq)), owen_float(float(hq), float(aq))
        ok &= within(iv, fv, tol)
    gf = math.gamma(7 / 6)
    ok &= within(GAMMA76, gf, 1e-13)
    checks["FLOAT_INSIDE"] = bool(ok)

    checks["WIDTHS"] = bool(
        all(F2[k].width() < Decimal("1e-40") and F3[k].width() < Decimal("1e-40") for k in F2)
        and all(GK[k].width() < Decimal("1e-40") for k in GK)
        and all(Iv(Decimal(r["c_ref_closed_form"][0]), Decimal(r["c_ref_closed_form"][1])).width() < Decimal("1e-40") for r in rows)
        and all(Iv(Decimal(r["c_torus_L_24"][0]), Decimal(r["c_torus_L_24"][1])).width() < Decimal("1e-40") for r in rows)
        and all(Iv(Decimal(r["c_torus_L_ge_10"][0]), Decimal(r["c_torus_L_ge_10"][1])).width() < Decimal("1e-10") for r in rows))

    fullB, fullK = (-INF, INF), (Fr(0), INF)
    checks["D1_EXACT"] = bool(ref.b_integral(fullB).contains(Fr(4, 3)) and ref.D1.contains(Fr(4, 3))
                              and F_ref(fullB).contains(1) and G_ref(fullK).contains(1))
    checks["D2_EXACT"] = bool(F3_ref(fullB).contains(1))          # the closed form of m_{3,b} integrates to 29/6 - sqrt6
    half = F_ref((Fr(0), INF))
    checks["HALF_LINE_EXACT"] = bool(half.contains(Iv.frac(Fr(2, 3)) + SQRT3 / (4 * PI)))   # T(0, 1/sqrt3) = 1/12
    checks["SYMMETRIC_CLOSED_FORM"] = bool(all(F_ref((-beta, beta)).intersects(F_ref_symmetric(beta))
                                               for beta in (Fr(1, 2), Fr(1), Fr(2), Fr(3))))

    fact = True
    for r in rows:
        a = Iv(Decimal(r["c_ref_closed_form"][0]), Decimal(r["c_ref_closed_form"][1]))
        b = Iv(Decimal(r["c_ref_pipeline"][0]), Decimal(r["c_ref_pipeline"][1]))
        t10 = Iv(Decimal(r["c_torus_L_ge_10"][0]), Decimal(r["c_torus_L_ge_10"][1]))
        t24 = Iv(Decimal(r["c_torus_L_24"][0]), Decimal(r["c_torus_L_24"][1]))
        fact &= a.intersects(b) and t10.contains(b) and t24.intersects(b) and t10.width() > 10 * b.width()
    checks["FACTORIZATION_AND_TRANSFER"] = bool(fact)

    side = Iv(Decimal(SIDE24_D2[0]), Decimal(SIDE24_D2[1]))
    full24 = tor24.coefficient(fullB, fullK)
    checks["SIDE24_CONSISTENT"] = bool(full24.intersects(side) and C2_REF.intersects(side + Iv(-side.hi * Decimal("1e-106"), side.hi * Decimal("1e-106"))))

    checks["IMAGE_BOUND"] = bool(Decimal("1.8e-12") < E10.hi < Decimal("1.95e-12") and E24.hi < Decimal("1e-112") and E24.lo > 0)

    mono = True
    seq = [F_ref((Fr(-1, 2), Fr(1, 2))), F_ref((Fr(-1), Fr(1))), F_ref((Fr(-2), Fr(2))), F_ref((Fr(-3), Fr(3))), F_ref(fullB)]
    mono &= all(seq[i].hi < seq[i + 1].lo for i in range(4)) and seq[0].lo > 0
    seqk = [G_ref((Fr(1), Fr(3, 2))), G_ref((Fr(1, 2), Fr(2))), G_ref((Fr(1, 4), Fr(4))), G_ref((Fr(1, 10), Fr(10))), G_ref(fullK)]
    mono &= all(seqk[i].hi < seqk[i + 1].lo for i in range(4)) and seqk[0].lo > 0
    mono &= F_ref((Fr(0), Fr(1))).lo > 0 and F3_ref((Fr(0), Fr(1))).lo > 0 and F_ref((-INF, Fr(0))).lo > 0
    checks["MONOTONE"] = bool(mono)

    # exhaustion: two-sided incomplete-gamma bounds and the elementary birth-tail bounds (NOTE section 5)
    exh = True
    a76 = Fr(7, 6)
    for klo, khi in ((Fr(1, 2), Fr(2)), (Fr(1, 4), Fr(4)), (Fr(1, 10), Fr(10))):
        s_lo, s_hi = 12 * Iv.frac(klo * klo), 12 * Iv.frac(khi * khi)
        Plo = P_reg(s_lo)
        s76 = s_lo * root_iv(s_lo, 6)
        g13 = Iv.frac(a76) * GAMMA76                                 # Gamma(13/6)
        exh &= Plo.intersects(Iv(((-s_lo).exp() * s76 / g13).lo, (s76 / g13).hi))
        Qhi = 1 - P_reg(s_hi)
        s16 = root_iv(s_hi, 6) * (-s_hi).exp()                       # s^(a-1) e^-s
        exh &= Qhi.intersects(Iv((s16 / GAMMA76).lo, (s16 / (GAMMA76 * (1 - Iv.frac(Fr(1, 6)) / s_hi))).hi))
    for bhi in (Fr(1), Fr(2), Fr(3)):                                 # 1 - Psi(x) <= 2 Phi_bar(x) + x phi(x)/2, x = b sqrt(3/2)
        x = x_ref(bhi)
        exh &= (1 - Psi_ref(x)).hi <= (2 * Phi_bar(x) + x * phi(x) / 2).lo
    for blo in (Fr(0), Fr(-1), Fr(-2), Fr(-3)):                       # Psi(x) <= (3/2) Phi(x) for b <= 0
        x = x_ref(blo)
        exh &= Psi_ref(x).hi <= (Iv.frac(Fr(3, 2)) * Phi(x)).lo
    checks["EXHAUSTION_BOUNDS"] = bool(exh)

    # truncation nesting: half the Owen terms, and erf / incomplete gamma without the tail must be caught by the tail rule
    nest = True
    for hq, aq in owen_pts:
        nest &= owen_T(Iv.frac(hq), Iv.frac(aq), N=80).intersects(owen_T_eval(Iv.frac(hq), Iv.frac(aq)))
    for xq in (Fr(1, 2), Fr(3, 2), Fr(3), Fr(5), Fr(48)):
        e_full, e_coarse = erf_iv(Iv.frac(xq)), erf_iv(Iv.frac(xq), coarse=True)
        nest &= e_coarse.intersects(e_full) and e_coarse.width() >= e_full.width()
        gl, gc = gamma_lower(Iv.frac(xq), Fr(7, 6)), gamma_lower(Iv.frac(xq), Fr(7, 6), coarse=True)
        nest &= gc.intersects(gl) and gc.width() >= gl.width()
    nest &= gamma_complete(Fr(7, 6), Decimal(90)).intersects(GAMMA76)
    checks["TRUNCATION_NESTING"] = bool(nest)

    pinned_vals = {"c_2_ref": C2_REF, "F|[0,1]": F_ref((Fr(0), Fr(1))), "G|[1/2,2]": G_ref((Fr(1, 2), Fr(2))),
                   "Gamma(7/6)": GAMMA76, "pi": PI}
    checks["LIBRARY_EXACT"] = bool(library_exact())
    checks["PINNED"] = bool(all(str(v.lo).startswith(p) and str(v.hi).startswith(p) for (k, p), v in
                                zip(PINNED.items(), (pinned_vals[k] for k in PINNED))))

    if len(checks) != 14:
        raise ValueError("rule count changed")
    passed = all(checks.values())

    out = {
        "object": "CL-C8-WINDOW-COEFFICIENT-PLANAR-20260930-v1",
        "scientific_effect": "NONE",
        "certified": True,
        "mutant": MUT,
        "passed": passed,
        "checks": checks,
        "constants": {
            "pi": PI.pair(), "Gamma(7/6)": GAMMA76.pair(), "(3/2)^(1/3)": CBRT32.pair(),
            "c_2_ref": C2_REF.pair(), "c_3_ref": C3_REF.pair(), "D_2": D2_EXACT.pair(),
            "E_10": E10.pair(), "E_24": E24.pair(),
            "reference_pipeline": {"p_G(0)": ref.pG.pair(), "p_V(0)": ref.pV.pair(), "tau^2": ref.tau2.pair(),
                                   "Var(f|V=0)": ref.sig2.pair(), "alpha": ref.alpha.pair(), "s^2": ref.s2.pair(),
                                   "a": ref.a.pair(), "D_1": ref.D1.pair()},
            "torus_L_ge_10_pipeline": {"tau^2": tor10.tau2.pair(), "Var(f|V=0)": tor10.sig2.pair(),
                                       "alpha": tor10.alpha.pair(), "s^2": tor10.s2.pair(), "a": tor10.a.pair()},
        },
        "birth_factor_d2": {k: v.pair() for k, v in F2.items()},
        "birth_factor_d3_reference": {k: v.pair() for k, v in F3.items()},
        "gap_factor": {k: v.pair() for k, v in GK.items()},
        "windows": rows,
        "float_reference_10sig": {
            "birth_factor_d2": {k: fmt10(v) for k, v in F2f.items()},
            "birth_factor_d3_reference": {k: fmt10(v) for k, v in F3f.items()},
            "gap_factor": {k: fmt10(v) for k, v in GKf.items()},
            "Gamma(7/6)": fmt10(gf),
            "owen_T": {"h=%s a=%s" % (hq, aq): fmt10(owen_float(float(hq), float(aq))) for hq, aq in owen_pts},
        },
        "exact_relations": {
            "factorization": "c_{B,K} = c_{2,ref} F_B G_K for the reference kernel; c_{2,ref} = 2 Gamma(7/6) (3/2)^(1/3) / (3 sqrt3 pi^(3/2))",
            "G_K": "P(7/6, 12 k_+^2) - P(7/6, 12 k_-^2)",
            "F_B": "Psi(b_+ sqrt(3/2)) - Psi(b_- sqrt(3/2)); Psi(x) = Phi(x) - 2 T(x, 1/sqrt3) - x phi(x) Phi(x/sqrt3)/2 - sqrt3 exp(-2x^2/3)/(4 pi)",
            "F_symmetric": "F_{[-beta,beta]} = erf(beta sqrt3/2) - beta sqrt3 exp(-3 beta^2/4)/(4 sqrt pi)",
            "F_half_line": "F_{[0,inf)} = 2/3 + sqrt3/(4 pi)",
            "m_3_b": "(b^3 + b) phi(b) + (b^4 + 2 b^2 + 7) Phi(b) - 4 sqrt2 exp(-b^2/4) Phi(b/sqrt2); E_b m_{3,b} = 29/6 - sqrt6",
            "image_bound": "E_L = 128 (76 L^6 + 15) exp(-L^2/2), d = 2, L >= 10",
            "exhaustion": "1 - G_K = P(7/6, 12 k_-^2) + Q(7/6, 12 k_+^2) with exp(-s) s^(7/6)/Gamma(13/6) <= P(7/6, s) <= s^(7/6)/Gamma(13/6) and "
                          "s^(1/6) e^-s/Gamma(7/6) <= Q(7/6, s) <= s^(1/6) e^-s/(Gamma(7/6)(1 - 1/(6s))); 1 - Psi(x) <= 2 Phi_bar(x) + x phi(x)/2 (x > 0); Psi(x) <= (3/2) Phi(x) (x <= 0)",
        },
    }
    sys.stdout.write(json.dumps(out, indent=1) + "\n")
    sys.stderr.write("seconds %.1f\n" % (time.time() - t0))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
