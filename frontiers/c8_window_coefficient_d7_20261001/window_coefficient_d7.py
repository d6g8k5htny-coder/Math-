"""The compact-window coefficient c_{B,K} of [LP] Theorem B in d = 7: the cone moment D_6, c_{7,ref}, the reference window
coefficient, and the transfer to the torus for every L >= 10 and every frame.

Standard library only. Run from anywhere:  python -B -S window_coefficient_d7.py [--mutant NAME]   (about four minutes)
Every printed interval [lo, hi] is a rigorous enclosure: interval arithmetic over `decimal` (60 digits, directed rounding; exp
and sqrt widened by two units in the last place and checked against exact rational brackets by rule LIBRARY_EXACT), pi by
Machin, fractional powers by exact integer roots, erf and the lower incomplete gamma function by positive series with geometric
tails (and, for |x| >= 12, the enclosure 0 < erfc(x) < e^{-x^2}/(x sqrt(pi))), arctan and Owen's T by alternating series bracketed
by consecutive partial sums (the Math-#197 toolkit, unchanged), and one one-dimensional integral by an order-48 Taylor expansion
at each cell centre with a Cauchy remainder (Math-#199 section 3), carrying the Owen-type kinds as a certified cumulative layer
(Math-#204 section 3).

Object ([LP] = imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md, (11.3) with the section 15 factorization,
both stated for every d, for compact windows B = [b_-, b_+] and K = [k_-, k_+] of positive length, b_- < b_+ and
0 < k_- < k_+ < infinity; frame (u, w1, ..., w6), G = grad f, V = (f_uu, f_uw1, ..., f_uw6), A the 6 x 6 transverse Hessian,
t = f_uuu):

  c^(7)_{B,K} = 144 int_{S^6} p_G(0) p_V(0) I_B(u) J_K(u) dsigma(u),   I_B(u) = E[1{f in B} det(A)^2 1{A < 0} | V = 0],
  J_K(u) = int_K k^(4/3) phi_tau(12 k) dk,   tau^2 = Var(t | G = 0).

Reference kernel.  (f, A) | V = 0 is f ~ N(0, 2/3) and A = Q - f I with Q the 6 x 6 GOE (density ~ exp(-tr Q^2/4)) independent
of f.  On the ordered eigenvalue sector of A, with total trace -T and nested coordinates (w'', w', w, s, q) (Jacobian 1/720), the
exponent is T^2/72 + w''^2/120 + w'^2/80 + w^2/48 + s^2/24 + q^2/8, the birth window enters only through
W_B(T) = Phi((3/sqrt2) (b_+ - T/9)) - Phi((3/sqrt2) (b_- - T/9)), and only odd powers of q occur.  One exact layer recursion
integrates q, s, w, w' and w'' in closed form.  The w-layer cancellation of Math-#213 recurs; the w'-layer leaves the three
Owen-type kinds of Math-#222, K_{al,g}(y) = int_0^y e^{-al x^2} E_g(x) dx, E_g(x) = int_0^x e^{-g s^2} ds; the w''-layer
integrates them by parts, and the nested kinds int_0^T e^{-y^2/120} K_{al,g}(y) dy cancel identically, so that

  I^ref_B = (1/(sqrt3 Z_6)) int_0^inf exp(-T^2/72) F_6(T) W_B(T) dT,   Z_6 = 4423680 sqrt2 pi^(3/2) (Mehta),
  F_6 = polynomials times exp(-T^2/12), exp(-5T^2/24), exp(-al T^2) E_g(T), K_{1/48,1/16}(T) and exp(-T^2/120) K_{al,g}(T).

The K_{al,g} are Owen's T functions, K = (pi/sqrt(al g)) [arctan(a)/(2 pi) - T(sqrt(2 al) T, a)], a = sqrt(g/al); the quadrature
carries them as a certified cumulative layer, and rule OWEN_EXACT checks that layer against Owen's series.  The same layers with
the Vandermonde alone return Mehta's Z_6 through arctan(sqrt3) = pi/3 (rule MEHTA_Z6).  B = R gives the cone moment D_6 and
c_{7,ref} = Gamma(7/6) (3/2)^(1/3) D_6/(120 sqrt3 pi^(9/2)).  The same code at m = 2, ..., 5 returns 29/6 - sqrt6, Math-#197's
d = 3 window values, Math-#201's D_3, Math-#202's D_4, Math-#204's and Math-#222's D_5, and the band factors of Math-#209, #213
and #222.

Torus.  If (1-eps) C'_ref <= C' <= (1+eps) C'_ref for the covariance of the 22-vector (f, A) | V = 0, the density comparison and
the degree-12 homogeneity of det(A)^2 give (Lemma S of Math-#205 with n = 22, degree 12)

  (1-eps)^17/(1+eps)^11 I^ref_{B/sqrt(1-eps)}  <=  I'_B  <=  (1+eps)^17/(1-eps)^11 I^ref_{B/sqrt(1+eps)}.

lambda_min(C'_ref) = (10 - 2 sqrt22)/3 = 0.2064 (below the d = 6 floor 23/100): eps = ||C' - C'_ref||_F / (1/5) over the entry
box of the d = 7 image bound E^(7)_L = 1499596 (76 L^6 + 15) exp(-L^2/2); p_G(0), p_V(0) and tau^2 over the same box.  One
enclosure covers every frame and every L >= 10.  Windows touching k = 0 or infinity, unbounded B, and singleton windows
(b_- = b_+ or k_- = k_+, where the integral is zero) are evaluated as coefficient integrals only.
Scientific effect NONE.
"""
import argparse
import json
import math
import sys
import time
from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN, setcontext
from fractions import Fraction as Fr

MUTANTS = ("image-shells", "d6-floor", "sandwich-swap", "window-scale", "trace-slope", "moment-recurrence", "remainder-dropped",
           "parts-sign", "schur-sign", "tau-cross", "sphere", "tilt-gamma", "layer-dropped", "cumulative-shift", "owen-parts", "mehta")
MUT = None

PREC = 60
CF = Context(prec=PREC, rounding=ROUND_FLOOR, Emin=-9999999, Emax=9999999)
CC = Context(prec=PREC, rounding=ROUND_CEILING, Emin=-9999999, Emax=9999999)
CE = Context(prec=PREC, rounding=ROUND_HALF_EVEN, Emin=-9999999, Emax=9999999)
# Every arithmetic step below names one of the three contexts; operator syntax on Decimals would round to the thread's
# current context, which is widened as a safety net (rule LIBRARY_EXACT checks exp, sqrt and the negation).
setcontext(Context(prec=2 * PREC + 20, rounding=ROUND_HALF_EVEN, Emin=-9999999, Emax=9999999))
ZERO, ONE, HALF = Decimal(0), Decimal(1), Decimal("0.5")
INF = math.inf
ROOT_DIGITS = 70
K_ORDER, RHO, CELL, T_CUT = 48, Fr(6), Fr(1, 2), Fr(120)         # Taylor order, Cauchy radius, cell width, cut (Math-#199 section 3)
D5_222 = ("44.1306518750741327103620248954026331487822380630770420119935",   # Math-#222 RESULTS.json reference/D_5_quadrature
          "44.1306518750741327103620248954026331487822380630770420128758")
D5_204 = ("44.1306518750741327103620248954026331485852349159356435082422",   # Math-#204 RESULTS.json cone_moments/D_5 (certified)
          "44.1306518750741327103620248954026331489792412102184405166029")
F4B_209 = "0.1539033000676815392013091707812771979851002980"        # Math-#209 PINNED (F^(4)_[0,1], the d = 4 band birth factor)
F5B_213 = "0.04371743008362033053724245662643528133240074085"       # Math-#213 PINNED (F^(5)_[0,1], the d = 5 band birth factor)
F6B_222 = "0.008001944363618010329693943918504838262453904498"      # Math-#222 PINNED (F^(6)_[0,1], the d = 6 band birth factor)
PINNED = {"c_7_ref": "0.004612569916048218421172084741520436510290786583", "D_6": "155.8639107879976764976861204156889715840949755687", "F7|[0,1]": "0.000941412181332181837593997476121259426168575107", "c7|[0,1]x[1/2,2] ref": "2.925502659389580710639082688904335713337849031792", "pi": "3.141592653589793238462643383279502884197169399375"}


# ---------------- interval arithmetic and special functions (Math-#197 toolkit, unchanged)
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
C3_REF = GAMMA76 * CBRT32 * D2_EXACT / (2 * SQRT3 * PI * PI * SQRTPI)             # SIDE24 (1), d = 3


# ---------------- the Gaussian integrals int_{-inf}^x t^n phi(t) Phi(a t) dt, n <= 4 (Math-#197 section 2, unchanged)
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


def P_reg(s):
    """Regularized lower incomplete gamma P(7/6, s) (s an interval >= 0 or INF)."""
    a = SHAPE()
    return gamma_lower(s, a) / GAMMA76


def G_ref(K):
    lo, hi = K
    def s(k):
        return k if isinstance(k, float) else 12 * Iv.frac(k * k)
    return P_reg(s(hi)) - P_reg(s(lo))


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


# ---------------- the d = 3 reference birth integral with interval endpoints (Math-#197 (4.1) and its three primitives)
def endpoint(b):
    return b if isinstance(b, (float, Iv)) else Iv.frac(b)


def I3_ref(lo, hi):
    """int_lo^hi phi_{2/3}(b) m_{3,b} db, m_{3,b} = (b^3 + b) phi(b) + (b^4 + 2 b^2 + 7) Phi(b) - 4 sqrt2 exp(-b^2/4) Phi(b/sqrt2);
    lo, hi are rationals, intervals or +-INF."""
    sig = SIGMA_REF
    def term_i(b):
        if isinstance(b, float):
            return Iv(ZERO)
        return -(b.sq() * 2 / 5 + Iv.frac(Fr(18, 25))) * (-(b.sq()) * 5 / 4).exp() / (2 * PI * sig)
    def term_ii(b):
        G = G_at(b if isinstance(b, float) else b / sig, sig)
        return sig.sq().sq() * G[4] + 2 * sig.sq() * G[2] + 7 * G[0]
    def term_iii(b):
        G = G_at(b if isinstance(b, float) else b * SQRT2, Iv.frac(Fr(1, 2)))
        return 4 / sig * G[0]
    lo, hi = endpoint(lo), endpoint(hi)
    cross = Iv.frac(Fr(1, 2)) if MUT == "d3-cross" else Iv(ONE)
    return (term_i(hi) - term_i(lo)) + (term_ii(hi) - term_ii(lo)) - cross * (term_iii(hi) - term_iii(lo))


# ---------------- exact polynomial algebra (Math-#199 cone_moment_d4.py, unchanged)
def padd(u, v):
    w = dict(u)
    for k, c in v.items():
        w[k] = w.get(k, Fr(0)) + c
    return {k: c for k, c in w.items() if c != 0}


def pmul(u, v):
    w = {}
    for k1, c1 in u.items():
        for k2, c2 in v.items():
            k = tuple(a + b for a, b in zip(k1, k2))
            w[k] = w.get(k, Fr(0)) + c1 * c2
    return {k: c for k, c in w.items() if c != 0}


def pscale(u, c):
    return {k: v * c for k, v in u.items() if v * c != 0}


def pconst(c, nvars):
    return {(0,) * nvars: Fr(c)} if c != 0 else {}


def pvar(i, nvars):
    e = [0] * nvars
    e[i] = 1
    return {tuple(e): Fr(1)}


def plin(coeffs):
    """sum_i coeffs[i] * variable_i."""
    out = {}
    for i, c in enumerate(coeffs):
        if c:
            out = padd(out, pscale(pvar(i, len(coeffs)), Fr(c)))
    return out


def lpadd(u, v):
    n = max(len(u), len(v))
    return [(u[i] if i < len(u) else Fr(0)) + (v[i] if i < len(v) else Fr(0)) for i in range(n)]


def lpmul(u, v):
    if not u or not v:
        return []
    w = [Fr(0)] * (len(u) + len(v) - 1)
    for i, a in enumerate(u):
        for j, b in enumerate(v):
            w[i + j] += a * b
    return w


# ---------------- the reference birth integral as a one-dimensional integral in the total trace (NOTE section 2)
def Jk_closed(k):
    """J_k(s) = int_0^s q^k e^{-q^2/8} dq for odd k: J_k = B_k + C_k(s) e^{-s^2/8} with B_k rational and C_k a rational polynomial
    (list by power): J_1 = 4 - 4 e^{-s^2/8}, J_{k+2} = -4 s^{k+1} e^{-s^2/8} + 4 (k+1) J_k."""
    if k % 2 != 1:
        raise ValueError("even power of q")
    B, C, j = Fr(4), [Fr(-4)], 1
    while j < k:
        C2 = [4 * (j + 1) * c for c in C] + [Fr(0)] * (j + 2 - len(C))
        C2[j + 1] += -4
        B, C, j = 4 * (j + 1) * B, C2, j + 2
    return B, C


def moments(gamma, nmax):
    """M_j(T) = int_0^T s^j e^{-gamma s^2} ds = alpha_j + rho_j(T) e^{-gamma T^2} + beta_j E_gamma(T), E_gamma = (1/2) sqrt(pi/gamma)
    erf(sqrt(gamma) T): M_0 = E_gamma, M_1 = (1 - e^{-gamma T^2})/(2 gamma), M_{j+2} = ((j+1) M_j - T^{j+1} e^{-gamma T^2})/(2 gamma)."""
    g = Fr(gamma)
    M = [(Fr(0), [], Fr(1)), (1 / (2 * g), [-1 / (2 * g)], Fr(0))]
    for j in range(nmax - 1):
        a, r, b = M[j]
        f = Fr(j if MUT == "moment-recurrence" else j + 1)
        r2 = [x * f / (2 * g) for x in r] + [Fr(0)] * (j + 2 - len(r))
        r2[j + 1] += -1 / (2 * g)
        M.append((f * a / (2 * g), r2, f * b / (2 * g)))
    return M


F_MEMO = {}


def F_pieces(m, mehta=False):
    if (m, mehta) not in F_MEMO:
        F_MEMO[(m, mehta)] = F_pieces_build(m, mehta)
    return F_MEMO[(m, mehta)]


def F_pieces_build(m, mehta=False):
    """The inner integrals in closed form, for every m = 2, ..., 6 by one generic layer recursion (NOTE section 2).  On the ordered
    eigenvalue sector mu_m = -a, mu_{m-1} = -a - p_1, ..., mu_1 = -a - p_1 - ... - p_{m-1} put x_0 = T = m a + (m-1) p_1 + ... + p_{m-1}
    (minus the trace) and x_k = (m-k) p_k + ... + p_{m-1}, k = 1, ..., m-1 (Jacobian 1/m!, region T > x_1 > ... > x_{m-1} > 0); the
    integrand is P(x) e^{-sum_k x_k^2 c_k} with c_{m-1} = 1/8 and c_{m-2}, ..., c_{m-5} = 1/24, 1/48, 1/80, 1/120 (eight times the
    triangular numbers), P = prod mu_i^2 times the Vandermonde (mehta: the Vandermonde alone).  The q = x_{m-1} layer is exact
    (Math-#201 L1); every further layer integrates y^j e^{-c y^2} times a kind ('1', ('e', g), ('E', g), ('eE', al, g), ('K', al, g))
    from 0 to the next variable by moment_dict, L_dict and KL_dict; the kinds KL_dict creates (('eK', c, al, g) = e^{-cT^2} K_{al,g}(T)
    and the nested ('KK', c, al, g) = int_0^T e^{-cy^2} K_{al,g}(y) dy) entering a further layer are refused (ValueError).
    Returns ({kind: polynomial in T, list by power}, outer gamma 3/(4 m (m+3)), [(c, generated kinds that came out zero) per layer])."""
    nv = m
    xs = [pvar(i, nv) for i in range(nv)]

    def lin(i, j, den):
        co = [Fr(0)] * nv
        co[i] += Fr(1, den)
        if j is not None:
            co[j] -= Fr(1, den)
        return plin(co)
    a = lin(0, 1, m)
    ps = [lin(k, k + 1 if k + 1 < m else None, m - k) for k in range(1, m)]
    mus, run = [pscale(a, Fr(-1))], a
    for p in ps:
        run = padd(run, p)
        mus.append(pscale(run, Fr(-1)))
    P = {(0,) * nv: Fr(1)}
    if not mehta:
        for mu in mus:
            P = pmul(P, pmul(mu, mu))
    for i in range(m):
        for j in range(i + 1, m):
            P = pmul(P, padd(mus[i], pscale(mus[j], Fr(-1))))                 # mus[i] > mus[j]
    U, V = {}, {}
    for mono, c in P.items():
        Bk, Ck = Jk_closed(mono[-1])                                           # raises on an even power of q
        base = mono[:-1]
        U[base] = U.get(base, Fr(0)) + c * Bk
        for n, x in enumerate(Ck):
            if x:
                mm = list(base)
                mm[-1] += n
                mm = tuple(mm)
                V[mm] = V.get(mm, Fr(0)) + c * x
    pieces = {("1",): {k: v for k, v in U.items() if v}, ("e", Fr(1, 8)): {k: v for k, v in V.items() if v}}
    stages, nvc = [], nv - 1
    for c in (Fr(1, 24), Fr(1, 48), Fr(1, 80), Fr(1, 120))[:m - 2]:
        pieces = layer(pieces, nvc, c)
        nvc -= 1
        if MUT == "layer-dropped" and c == Fr(1, 48):
            pieces.pop(("E", Fr(3, 16)), None)                                # a cancelled layer silently not derived
        stages.append((c, sorted(("%s" % (k,)) for k, p in pieces.items() if not p)))
    out = {}
    for kind, poly in pieces.items():
        lst = []
        for mono, v in poly.items():
            n = mono[0]
            lst += [Fr(0)] * (n + 1 - len(lst))
            lst[n] += v
        out[kind] = lst
    return out, Fr(3, 4 * m * (m + 3)), stages


def layer(pieces, nv, c):
    """Integrate the last variable y of nv variables (T, x_1, ..., y) over (0, x_{nv-2}) against e^{-c y^2}, kind by kind."""
    out = {}
    for kind, poly in pieces.items():
        for mono, coef in poly.items():
            j = mono[-1]
            if kind[0] == "1":
                lay = moment_dict(c, j)
            elif kind[0] == "e":
                lay = moment_dict(c + kind[1], j)
            elif kind[0] == "E":
                lay = L_dict(c, kind[1], j)
            elif kind[0] == "eE":
                lay = L_dict(c + kind[1], kind[2], j)
            elif kind[0] == "K":
                lay = KL_dict(c, kind[1], kind[2], j)
            else:
                raise ValueError("a kind %r entered a further layer" % (kind,))
            base = mono[:-1]
            for k2, pl in lay.items():
                acc = out.setdefault(k2, {})
                for n, x in enumerate(pl):
                    if x:
                        mm = list(base)
                        mm[-1] += n
                        mm = tuple(mm)
                        acc[mm] = acc.get(mm, Fr(0)) + coef * x
    return {k: {mm: v for mm, v in p.items() if v} for k, p in out.items()}


def moment_dict(gamma, j):
    """M_j(gamma, T) = int_0^T w^j e^{-gamma w^2} dw by kind: ('1',) constant, ('e', gamma) e^{-gamma T^2}, ('E', gamma) E_gamma(T)."""
    a_, r_, b_ = moments(gamma, max(j, 1))[j]
    out = {}
    if a_:
        out[("1",)] = [a_]
    if any(r_):
        out[("e", gamma)] = list(r_)
    if b_:
        out[("E", gamma)] = [b_]
    return out


L_MEMO = {}


def L_dict(al, g, j):
    """L_j(T) = int_0^T w^j e^{-al w^2} E_g(w) dw, E_g(w) = (1/2) sqrt(pi/g) erf(sqrt(g) w): L_0 = Kfun_{al,g}(T) and, by parts,
    L_j = -(1/(2 al)) T^{j-1} e^{-al T^2} E_g(T) + ((j-1)/(2 al)) L_{j-2} + (1/(2 al)) M_{j-1}(al + g, T)
    (the last coefficient is (1/2) sqrt(pi/g) . sqrt(g)/(al sqrt(pi)) = 1/(2 al), rational)."""
    key = (al, g, j)
    if key in L_MEMO:
        return L_MEMO[key]
    if j == 0:
        res = {("K", al, g): [Fr(1)]}
    else:
        res = {}

        def add(kind, poly):
            res[kind] = lpadd(res.get(kind, []), poly)
        add(("eE", al, g), [Fr(0)] * (j - 1) + [(1 if MUT == "parts-sign" else -1) / (2 * al)])
        if j >= 2:
            for kind, pl in L_dict(al, g, j - 2).items():
                add(kind, [x * Fr(j - 1) / (2 * al) for x in pl])
        for kind, pl in moment_dict(al + g, j - 1).items():
            add(kind, [x / (2 * al) for x in pl])
    L_MEMO[key] = res
    return res


KL_MEMO = {}


def KL_dict(c, al, g, j):
    """KL_j(T) = int_0^T y^j e^{-c y^2} K_{al,g}(y) dy: KL_0 is the nested kind ('KK', c, al, g) and, by parts with K' = e^{-al y^2} E_g,
    KL_j = -(1/(2c)) T^{j-1} e^{-cT^2} K_{al,g}(T) + ((j-1)/(2c)) KL_{j-2} + (1/(2c)) L_{j-1}(c + al, g, T)."""
    key = (c, al, g, j)
    if key in KL_MEMO:
        return KL_MEMO[key]
    res = {}

    def add(kind, poly):
        res[kind] = lpadd(res.get(kind, []), poly)
    if j == 0:
        add(("KK", c, al, g), [Fr(1)])
    else:
        add(("eK", c, al, g), [Fr(0)] * (j - 1) + [Fr(-1) / (2 * c)])
        if j >= 2:
            f = Fr(j if MUT == "owen-parts" else j - 1)
            for kind, pl in KL_dict(c, al, g, j - 2).items():
                add(kind, [x * f / (2 * c) for x in pl])
        for kind, pl in L_dict(c + al, g, j - 1).items():
            add(kind, [x / (2 * c) for x in pl])
    KL_MEMO[key] = res
    return res


def trim(poly):
    poly = list(poly)
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def g_terms(m, gamma_out=None):
    """g_m(T) = e^{-gamma_out T^2} F_m(T) as terms (const, polynomial, gamma, kappa, K): const * poly(T) e^{-gamma T^2} [erf(kappa T)]
    [K_{al,g}(T)], with K_{al,g}(T) = int_0^T e^{-al w^2} E_g(w) dw the Owen-type kinds (certified cumulative layer, NOTE section 3);
    ('eK', c, al, g) is e^{-cT^2} K_{al,g}(T).  A surviving nested kind is refused (ValueError)."""
    pieces, g_ref, _ = F_pieces(m)
    gout = g_ref if gamma_out is None else gamma_out
    terms = []
    for key, poly in sorted(pieces.items(), key=lambda kv: str(kv[0])):
        poly = trim(poly)
        if not poly:
            continue
        if key[0] == "1":
            terms.append((Iv(ONE), poly, Iv.frac(gout), None, None))
        elif key[0] == "e":
            terms.append((Iv(ONE), poly, Iv.frac(gout + key[1]), None, None))
        elif key[0] == "E":
            terms.append(((PI / Iv.frac(key[1])).sqrt() / 2, poly, Iv.frac(gout), Iv.frac(key[1]).sqrt(), None))
        elif key[0] == "eE":
            terms.append(((PI / Iv.frac(key[2])).sqrt() / 2, poly, Iv.frac(gout + key[1]), Iv.frac(key[2]).sqrt(), None))
        elif key[0] == "K":
            terms.append((Iv(ONE), poly, Iv.frac(gout), None, (key[1], key[2])))
        elif key[0] == "eK":
            terms.append((Iv(ONE), poly, Iv.frac(gout + key[1]), None, (key[2], key[3])))
        else:
            raise ValueError("a nested Owen-type kind %r survived" % (key,))
    return terms


def K_float(al, g, T, n=4000):
    """Float control of K_{al,g}(T) by Simpson's rule."""
    if T == 0:
        return 0.0
    h = T / n
    f = [math.exp(-al * (i * h) ** 2) * 0.5 * math.sqrt(math.pi / g) * math.erf(math.sqrt(g) * i * h) for i in range(n + 1)]
    return h / 3 * (f[0] + f[-1] + 4 * sum(f[1:-1:2]) + 2 * sum(f[2:-1:2]))


def F_float(pieces, T):
    tot = 0.0
    for key, poly in pieces.items():
        pv = sum(float(c) * T ** i for i, c in enumerate(poly))
        if key[0] == "1":
            tot += pv
        elif key[0] == "e":
            tot += pv * math.exp(-float(key[1]) * T * T)
        elif key[0] == "E":
            g = float(key[1])
            tot += pv * 0.5 * math.sqrt(math.pi / g) * math.erf(math.sqrt(g) * T)
        elif key[0] == "eE":
            al, g = float(key[1]), float(key[2])
            tot += pv * math.exp(-al * T * T) * 0.5 * math.sqrt(math.pi / g) * math.erf(math.sqrt(g) * T)
        elif key[0] == "K":
            tot += pv * K_float(float(key[1]), float(key[2]), T)
        elif key[0] == "eK":
            tot += pv * math.exp(-float(key[1]) * T * T) * K_float(float(key[2]), float(key[3]), T)
        elif any(poly):
            raise ValueError(key)
    return tot


# ---------------- Taylor quadrature with Cauchy remainders (Math-#199 section 3; factors as functions, plus Phi(alpha - beta T))
def ipow(x, n):
    r = Iv(ONE)
    for _ in range(n):
        r = r * x
    return r


ERF_FAST = Decimal(12)


def erf_point_fast(x):
    """erf at a Decimal point: the toolkit series for |x| < 12; for |x| >= 12 the enclosure [1 - e^{-x^2}/(x sqrt(pi)), 1] (with sign),
    since 0 < erfc(x) < e^{-x^2}/(x sqrt(pi)) for x > 0 (here below 1.5e-64)."""
    if abs(x) < ERF_FAST:
        return erf_point(x)
    X = Iv(abs(x))
    t = (-(X.sq())).exp() / (X * SQRTPI)
    v = Iv((1 - t).lo, ONE)
    return v if x > 0 else -v


def erf_fast(x):
    return Iv(erf_point_fast(x.lo).lo, erf_point_fast(x.hi).hi)


def Phi_fast(x):
    return (1 + erf_fast(x / SQRT2)) / 2


CACHE = {}


def gauss_coeffs(g, s0, K):
    """Taylor coefficients of exp(-g s^2) at s0: (n+1) y_{n+1} = -2 g (s0 y_n + y_{n-1})."""
    key = ("g", g.lo, g.hi, s0, K)
    if key in CACHE:
        return CACHE[key]
    S0 = Iv.frac(s0)
    y = [(-(g * S0.sq())).exp()]
    prev = Iv(ZERO)
    for n in range(K):
        nxt = -(2 * g) * (S0 * y[n] + prev) / (n + 1)
        prev = y[n]
        y.append(nxt)
    CACHE[key] = y
    return y


def gauss_bound(g, s0, rho):
    inner = max(Fr(0), abs(Fr(s0)) - Fr(rho))
    return (g * Iv.frac(rho * rho) - g * Iv.frac(inner * inner)).exp()   # |e^{-g z^2}| = e^{-g(x^2 - y^2)}, |y| <= rho


def erf_coeffs(kappa, s0, K):
    """erf(kappa s): value at s0, then (2 kappa/sqrt pi) times the Gaussian's coefficients divided by n + 1."""
    key = ("e", kappa.lo, kappa.hi, s0, K)
    if key in CACHE:
        return CACHE[key]
    y = gauss_coeffs(kappa.sq(), s0, K)
    pref = 2 * kappa / SQRTPI
    out = [erf_fast(kappa * Iv.frac(s0))] + [pref * y[n] / (n + 1) for n in range(K)]
    CACHE[key] = out
    return out


def erf_bound(kappa, s0, rho):
    return 2 * kappa / SQRTPI * Iv.frac(abs(Fr(s0)) + Fr(rho)) * (kappa.sq() * Iv.frac(Fr(rho) ** 2)).exp()


def poly_coeffs(c, s0, K):
    out = []
    for n in range(K + 1):
        v = Fr(0)
        for j, cj in enumerate(c):
            if j >= n:
                v += cj * math.comb(j, n) * Fr(s0) ** (j - n)
        out.append(Iv.frac(v))
    return out


def poly_bound(c, s0, rho):
    r = abs(Fr(s0)) + Fr(rho)
    return Iv.frac(sum(abs(cj) * r ** j for j, cj in enumerate(c)))


def t_mul(u, v):
    K = len(u) - 1
    out = []
    for n in range(K + 1):
        acc = Iv(ZERO)
        for i in range(n + 1):
            acc = acc + u[i] * v[n - i]
        out.append(acc)
    return out


def phi_aff_coeffs(alpha, beta, s0, K):
    """Phi(alpha - beta T) at T = s0 + x (alpha, beta real intervals, beta > 0): c_0 = Phi(w0), w0 = alpha - beta s0, and
    c_{n+1} = -(beta/sqrt(2 pi)) y_n/(n+1) with y the coefficients of exp(-(w0 - beta x)^2/2), (n+1) y_{n+1} = beta w0 y_n - beta^2 y_{n-1}."""
    w0 = alpha - beta * Iv.frac(s0)
    y = [(-(w0.sq()) / 2).exp()]
    prev = Iv(ZERO)
    b2 = beta.sq()
    for n in range(K):
        nxt = (beta * w0 * y[n] - b2 * prev) / (n + 1)
        prev = y[n]
        y.append(nxt)
    pref = beta / SQRT2PI
    return [Phi_fast(w0)] + [-(pref * y[n] / (n + 1)) for n in range(K)]


def phi_aff_bound(beta, rho):
    """|Phi(alpha - beta z)| <= Phi(w0) + |int_{w0}^{w} phi| <= 1 + beta rho e^{beta^2 rho^2/2}/sqrt(2 pi) on |z - s0| <= rho
    (the segment from the real point w0 has |Im t| <= beta rho, and |phi(t)| <= e^{(Im t)^2/2}/sqrt(2 pi))."""
    br = beta * Iv.frac(rho)
    return 1 + br * (br.sq() / 2).exp() / SQRT2PI


class Model:
    """int_0^inf g(T) Phi(alpha - beta T) dT for g = sum const * poly(T) e^{-gamma T^2} [erf(kappa T)] [K_{al,g}(T)] (entire).  On each
    cell of width CELL the point Taylor coefficients of g at the centre are computed once and contracted with the cell moments, so
    that an evaluation for given (alpha, beta) costs one product of coefficient vectors per cell.  The remainder of the order-K
    Taylor polynomial of the product is bounded by Cauchy's estimate at the centre, |c_n| <= M_g M_Phi / rho^n, summed geometrically;
    beyond T_CUT the integrand is bounded by |g| (0 <= Phi <= 1, |erf| <= 1, |K_{al,g}| <= pi/(4 sqrt(al g))) and incomplete gamma
    bounds.  K_{al,g} is a certified cumulative layer (Math-#204 section 3): its value at a centre is the certified integral of
    k = e^{-al w^2} E_g(w) over the full cells before plus the left half of the current cell, its higher Taylor coefficients are those
    of k divided by n, and its disc bound is |K(s0)| + rho M_k."""

    def __init__(self, terms, K=K_ORDER, cell=CELL, T=T_CUT, rho=RHO):
        self.K, self.rho = K, rho
        half = cell / 2
        ncell = int(T / cell)
        if ncell * cell != T or Fr(half) >= Fr(rho):
            raise ValueError("bad quadrature parameters")
        mom = [Iv.frac(2 * half ** (n + 1) / (n + 1)) if n % 2 == 0 else Iv(ZERO) for n in range(K + 1)]
        left = [Iv.frac((-1) ** n * half ** (n + 1) / (n + 1)) for n in range(K + 1)]   # int_{-h}^0 x^n dx
        rem_moment = Iv.frac(2 * half ** (K + 2) / (K + 2) / (1 - Fr(half) / Fr(rho)))
        rho_pow = Iv.frac(Fr(rho) ** (K + 1))
        kinds = sorted({kk for *_, kk in terms if kk is not None})
        Kacc = {kk: Iv(ZERO) for kk in kinds}
        self.Kvals = {kk: [] for kk in kinds}
        self.cells, Rsum = [], Iv(ZERO)
        for c in range(ncell):
            s0 = (2 * c + 1) * half
            Kco, Kbd = {}, {}
            for al, g in kinds:
                Ec = (PI / Iv.frac(g)).sqrt() / 2
                kc = [Ec * x for x in t_mul(gauss_coeffs(Iv.frac(al), s0, K), erf_coeffs(Iv.frac(g).sqrt(), s0, K))]
                Mk = Ec * gauss_bound(Iv.frac(al), s0, rho) * erf_bound(Iv.frac(g).sqrt(), s0, rho)
                Rk = (Mk / rho_pow * rem_moment / 2).hi                          # one-sided Cauchy remainder
                if MUT == "remainder-dropped":
                    Rk = ZERO
                lefti = sum((kc[n] * left[n] for n in range(K + 1)), Iv(ZERO))
                full = sum((kc[n] * mom[n] for n in range(0, K + 1, 2)), Iv(ZERO))
                Ks0 = Kacc[(al, g)] + (Iv(ZERO) if MUT == "cumulative-shift" else lefti) + Iv(Rk.copy_negate(), Rk)
                Kacc[(al, g)] = Kacc[(al, g)] + full + Iv(CC.multiply(Decimal(-2), Rk), CC.multiply(Decimal(2), Rk))
                Kco[(al, g)] = [Ks0] + [kc[n] / (n + 1) for n in range(K)]
                Kbd[(al, g)] = Iv(Ks0.mag()) + Iv.frac(rho) * Mk
                self.Kvals[(al, g)].append((s0, Ks0))
            G, M = [Iv(ZERO)] * (K + 1), Iv(ZERO)
            for const, poly, gam, kap, kk in terms:
                pc = t_mul(poly_coeffs(poly, s0, K), gauss_coeffs(gam, s0, K))
                Mb = poly_bound(poly, s0, rho) * gauss_bound(gam, s0, rho)
                if kap is not None:
                    pc = t_mul(pc, erf_coeffs(kap, s0, K))
                    Mb = Mb * erf_bound(kap, s0, rho)
                if kk is not None:
                    pc = t_mul(pc, Kco[kk])
                    Mb = Mb * Kbd[kk]
                G = [x + const * y for x, y in zip(G, pc)]
                M = M + Iv(const.mag()) * Mb
            Gm = []
            for j in range(K + 1):
                acc = Iv(ZERO)
                for i in range(j % 2, K + 1 - j, 2):
                    acc = acc + G[i] * mom[i + j]
                Gm.append(acc)
            self.cells.append((s0, Gm))
            Rsum = Rsum + M / rho_pow * rem_moment
        self.Rsum = Rsum.hi
        self.K_at_cut = Kacc
        tail = Iv(ZERO)
        for const, poly, gam, kap, kk in terms:              # int_T^inf t^j e^{-g t^2} dt = (1/2) g^{-(j+1)/2} Gamma((j+1)/2, g T^2)
            kfac = Iv(ONE) if kk is None else PI / (4 * (Iv.frac(kk[0]) * Iv.frac(kk[1])).sqrt())
            x = gam * Iv.frac(T * T)
            for j, cj in enumerate(poly):
                if cj == 0:
                    continue
                a = Fr(j + 1, 2)
                if a.denominator == 2:
                    xa1, gpow = ipow(x, int(a - Fr(1, 2))) * x.sqrt() / x, ipow(gam, int(a)) * gam.sqrt()
                else:
                    xa1, gpow = ipow(x, int(a) - 1), ipow(gam, int(a))
                up = xa1 * (-x).exp()                          # Gamma(a, x) <= x^(a-1) e^-x (a <= 1), / (1 - (a-1)/x) (a > 1)
                if a > 1:
                    up = up / (1 - Iv.frac(a - 1) / x)
                tail = tail + Iv(const.mag()) * kfac * Iv.frac(abs(cj)) * up / gpow / 2
        self.tail = tail.hi

    def integral(self, alpha=None, beta=None):
        tot = Iv(ZERO)
        if alpha is None:
            for _, Gm in self.cells:
                tot = tot + Gm[0]
            R = self.Rsum
        else:
            for s0, Gm in self.cells:
                Wc = phi_aff_coeffs(alpha, beta, s0, self.K)
                for j in range(self.K + 1):
                    tot = tot + Wc[j] * Gm[j]
            R = (Iv(self.Rsum) * phi_aff_bound(beta, self.rho)).hi
        if MUT == "remainder-dropped":
            R = ZERO
        R = CC.add(R, self.tail)
        return tot + Iv(R.copy_negate(), R)


MODELS = {}


def model(m, gamma_out=None):
    key = (m, gamma_out)
    if key not in MODELS:
        MODELS[key] = Model(g_terms(m, gamma_out))
    return MODELS[key]


Z_MEHTA = {2: 8 * SQRT2PI, 3: 48 * SQRT2 * PI, 4: 1536 * PI, 5: 46080 * PI * SQRTPI,     # Mehta's integral (Math-#199 section 1; Z_4, Z_5: Math-#202, #204)
           6: 4423680 * PI * SQRTPI * (ONE if MUT == "mehta" else SQRT2)}           # Z_6 = 4423680 sqrt2 pi^(3/2) (rule MEHTA_Z6)


class Birth:
    """I_B = kappa0/Z_m int_0^inf e^{-gamma_out T^2} F_m(T) [Phi(sl (b_+ - c T)) - Phi(sl (b_- - c T))] dT for the Gaussian pair
    f ~ N(0, v), g = mu f + sigma Z (A = Q - g I): conditioning on f = b and integrating the GOE shift exactly (NOTE section 2).
    Reference: v = 2/3, mu = 1, sigma = 0, i.e. kappa0 = sqrt(3/(m+3)), gamma_out = 3/(4m(m+3)), sl = sqrt((m+3)/2), c = 1/(m+3)."""

    def __init__(self, m, v=Fr(2, 3), mu=Fr(1), sig2=Fr(0)):
        D = 1 + m * sig2 / 2
        A = 1 / (2 * v) + m * mu * mu / (4 * D)
        Bc = mu / (2 * D)
        g0 = Bc * Bc / (4 * A) + (Fr(0) if MUT == "tilt-gamma" else sig2 / (8 * D))
        self.m = m
        self.gamma_out = Fr(1, 4 * m) - g0
        c = Bc / (2 * A)
        if MUT == "trace-slope" and sig2 == 0:
            c = Fr(1, m + 2)
        self.sl = Iv.frac(2 * A).sqrt()
        self.beta = self.sl * Iv.frac(c)
        self.pref = 1 / Iv.frac(2 * v * A * D).sqrt() / Z_MEHTA[m]
        self.M = model(m, None if self.gamma_out == F_pieces(m)[1] else self.gamma_out)
        self.cache = {}

    def lam(self, b):
        if isinstance(b, float):
            return self.M.integral() if b > 0 else Iv(ZERO)
        key = (b.lo, b.hi)
        if key not in self.cache:
            self.cache[key] = self.M.integral(self.sl * b, self.beta)
        return self.cache[key]

    def I(self, B):
        lo, hi = (x if isinstance(x, (float, Iv)) else Iv.frac(x) for x in B)
        return self.pref * (self.lam(hi) - self.lam(lo))


def gl_nodes(n):
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
            if abs(dx) < 1e-15:
                break
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


def Fm_direct_float(m, T, n=12):
    """int_{T > x_1 > ... > x_{m-1} > 0} P e^{-sum_k c_k x_k^2} by nested Gauss-Legendre with n nodes per layer (float control of the exact
    layers and of the cumulative K layer; P = prod mu_i^2 times the Vandermonde, mu from the gaps p_k = (x_k - x_{k+1})/(m - k))."""
    xs, ws = gl_nodes(n)
    cs = [None] + [float((Fr(1, 120), Fr(1, 80), Fr(1, 48), Fr(1, 24), Fr(1, 8))[k + 5 - m]) for k in range(1, m)]   # c of x_k

    def rec(k, x, upper, weight, acc):
        if k == m:
            a = (T - x[1]) / m
            ps = [(x[i] - (x[i + 1] if i + 1 < m else 0.0)) / (m - i) for i in range(1, m)]
            mus, run = [a], a
            for p_ in ps:
                run += p_
                mus.append(run)
            val = 1.0
            for mu in mus:
                val *= mu * mu
            for i in range(m):
                for j in range(i + 1, m):
                    val *= mus[j] - mus[i]
            return weight * val
        tot = 0.0
        for xi, wi in zip(xs, ws):
            y = upper * (xi + 1) / 2
            tot += rec(k + 1, x + [y], y, weight * wi * upper / 2 * math.exp(-cs[k] * y * y), acc)
        return tot
    return rec(1, [T], T, 1.0, None)


def Im_float(m, B, n=48, R=96.0):
    """Float control of the outer T layer: Gauss-Legendre in T (four panels) of e^{-gamma_out T^2} F_m(T) W_B(T) with F_m from the
    float evaluation of the exact pieces (math.erf and Simpson's K), independent of the certified Taylor/Cauchy quadrature and of
    the cumulative layer."""
    xs, ws = gl_nodes(n)
    pieces, g_out, _ = F_pieces(m)
    lo, hi = float(B[0]), float(B[1])
    sl, cc = math.sqrt((m + 3) / 2), 1.0 / (m + 3)

    def Phi_f(x):
        return 0.5 * math.erfc(-x / math.sqrt(2))
    tot = 0.0
    for k in range(4):
        a0 = k * R / 4
        for x, w in zip(xs, ws):
            T = a0 + R / 8 * (x + 1)
            W = Phi_f(sl * (hi - cc * T)) - Phi_f(sl * (lo - cc * T))
            tot += w * R / 8 * math.exp(-float(g_out) * T * T) * F_float(pieces, T) * W
    return math.sqrt(3 / (m + 3)) / Z_MEHTA[m].mid_float() * tot


# ---------------- the d = 7 jet of the reference kernel exp(-|z|^2/2), frame (u, w1, ..., w6)
def _e(*idx):
    v = [0] * 7
    for i in idx:
        v[i] += 1
    return tuple(v)


A_PAIRS = [(i, j) for i in range(1, 7) for j in range(i, 7)]                          # A11 A12 ... A66 (21 entries)
EVEN = [_e(), _e(0, 0)] + [_e(0, i) for i in range(1, 7)] + [_e(i, j) for i, j in A_PAIRS]   # f, f_uu, f_uw1..6, A (29 entries)
ODD = [_e(0)] + [_e(i) for i in range(1, 7)] + [_e(0, 0, 0)]                                  # f_u, f_w1..6, t = f_uuu
IDX_X, IDX_V = [0] + list(range(8, 29)), [1, 2, 3, 4, 5, 6, 7]
DIAG_A = [1 + k for k, (i, j) in enumerate(A_PAIRS) if i == j]                         # positions of A11, ..., A66 in IDX_X
OFF_A = [1 + k for k, (i, j) in enumerate(A_PAIRS) if i != j]
N_VEC, DEGREE = 22, 12                                                                 # Lemma S: dimension of (f, A), degree of det(A)^2


def dfact2(n):
    r = 1
    while n > 1:
        r *= n
        n -= 2
    return r


def ref_cov(a, b):
    """Cov(d^a f, d^b f) = (-1)^|a| d^(a+b) exp(-|z|^2/2) at 0 = (-1)^|a| prod_i (-1)^(al_i/2) (al_i - 1)!! (all al_i even)."""
    al = [x + y for x, y in zip(a, b)]
    if any(x % 2 for x in al):
        return Fr(0)
    v = Fr((-1) ** sum(a))
    for x in al:
        v *= (-1) ** (x // 2) * dfact2(x - 1)
    if MUT == "tau-cross" and sorted([a, b]) == sorted([_e(0, 0, 0), _e(0)]):
        return Fr(0)
    return v


def ref_matrix(idx):
    return [[ref_cov(a, b) for b in idx] for a in idx]


def det_n(M):
    """Determinant by Laplace expansion along the first row (n <= 7); Fractions or intervals."""
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    tot = None
    for j in range(n):
        minor = [[M[i][k] for k in range(n) if k != j] for i in range(1, n)]
        t = M[0][j] * det_n(minor)
        tot = t if tot is None else (tot + t if j % 2 == 0 else tot - t)
    return tot


def inv_n(M):
    """Inverse by the adjugate (n <= 7); works for Fractions and for intervals."""
    n = len(M)
    d = det_n(M)
    cof = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [[M[r][c] for c in range(n) if c != j] for r in range(n) if r != i]
            v = det_n(minor)
            cof[i][j] = v if (i + j) % 2 == 0 else -v
    return [[cof[j][i] / d for j in range(n)] for i in range(n)], d


def schur(C, X, V):
    """Cov(X | V) = C_XX - C_XV C_VV^-1 C_VX for index lists into C (Fractions or intervals)."""
    Vinv, detV = inv_n([[C[i][j] for j in V] for i in V])
    out = []
    for i in X:
        row = []
        for j in X:
            s = None
            for p in range(len(V)):
                for q in range(len(V)):
                    t = C[i][V[p]] * Vinv[p][q] * C[V[q]][j]
                    s = t if s is None else s + t
            row.append(C[i][j] + s if MUT == "schur-sign" else C[i][j] - s)
        out.append(row)
    return out, detV


def sylvester_pd(M):
    """Exact positive definiteness of a symmetric rational matrix (Gaussian elimination; all pivots positive)."""
    n = len(M)
    A = [list(map(Fr, r)) for r in M]
    for k in range(n):
        if A[k][k] <= 0:
            return False
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= f * A[k][j]
    return True


C_EVEN_REF = ref_matrix(EVEN)
C_ODD_REF = ref_matrix(ODD)
CPRIME_REF, DETV_REF = schur(C_EVEN_REF, IDX_X, IDX_V)
LAMBDA0 = Fr(1, 5)


def shifted(M, lam):
    return [[M[i][j] - (lam if i == j else 0) for j in range(len(M))] for i in range(len(M))]


# ---------------- image bound for the torus kernel in d = 7
def image_bound7(L):
    """E^(7)_L = 1499596 (76 L^6 + 15) exp(-L^2/2): the shell |n|_inf = j carries (2j+1)^7 - (2j-1)^7 = 896 j^6 + 1120 j^4 + 168 j^2 + 2
    <= 2186 j^6 points with |n|^2 <= 7 j^2, so sum_{n != 0} |n|^6 exp(-L^2 |n|^2/2) <= 749798 sum_j j^12 exp(-L^2 j^2/2)
    <= 1499596 exp(-L^2/2) (successive terms ratio at most 2^12 exp(-3L^2/2) < 1/2 for L >= 10); the contraction bound 76|x|^6 phi(x)
    (q <= 6, |x| >= 1), |D^q phi(0)| <= 15 and the normalization S >= 1 are those of Math-#197 section 3 (dimension-free)."""
    shells = 896 if MUT == "image-shells" else 2186
    L = Fr(L)
    return Iv.frac(2 * shells * 343 * (76 * L ** 6 + 15)) * (-Iv.frac(L * L / 2)).exp()


def half_power(x, twice):
    r = ipow(x, twice // 2)
    return r * x.sqrt() if twice % 2 else r


SANDWICH_VIOLATIONS = []


def scaled(b, s):
    if isinstance(b, float):
        return b
    b = b if isinstance(b, Iv) else Iv.frac(b)
    return b * s if MUT == "window-scale" else b / s


def sandwich(birth, B, eps):
    """Lemma S with n = 22, degree 12: (1-eps)^17/(1+eps)^11 I^ref_{B/sqrt(1-eps)} <= I'_B <= (1+eps)^17/(1-eps)^11
    I^ref_{B/sqrt(1+eps)}."""
    e = Iv(eps) if isinstance(eps, Decimal) else Iv.of(eps)
    if e.hi >= 1:
        raise ValueError("eps must be below 1")
    up, dn = 1 + e, 1 - e
    s_up, s_dn = up.sqrt(), dn.sqrt()
    su, sd = (s_dn, s_up) if MUT == "sandwich-swap" else (s_up, s_dn)
    lo, hi = B
    upper = half_power(up, N_VEC + DEGREE) / half_power(dn, N_VEC) * birth.I((scaled(lo, su), scaled(hi, su)))
    lower = half_power(dn, N_VEC + DEGREE) / half_power(up, N_VEC) * birth.I((scaled(lo, sd), scaled(hi, sd)))
    if lower.lo > upper.hi:                       # impossible for a correct bracket; recorded and reported by rule SANDWICH_ORDERED
        SANDWICH_VIOLATIONS.append(str(B))
        return Iv(upper.lo, lower.hi)
    return Iv(lower.lo, upper.hi)


def scaled_exact(birth, B, eta):
    """Exact I'_B for C' = (1 + eta) C'_ref: (1 + eta)^6 I^ref_{B/sqrt(1+eta)} (degree-12 homogeneity of det(A)^2)."""
    s = (1 + Iv.frac(eta)).sqrt()
    lo, hi = B
    return ipow(1 + Iv.frac(eta), DEGREE // 2) * birth.I((scaled(lo, s), scaled(hi, s)))


def frob_eps(Cp, Cref):
    """eps = ||C' - C'_ref||_F / lambda0, entrywise supremum of the deviation over each interval entry."""
    dev2 = Iv(ZERO)
    n = len(Cref)
    for i in range(n):
        for j in range(n):
            r = Iv.frac(Cref[i][j])
            c = Cp[i][j] if isinstance(Cp[i][j], Iv) else Iv.frac(Cp[i][j])
            d = max(abs(CC.subtract(c.hi, r.lo)), abs(CF.subtract(c.lo, r.hi)))
            dev2 = dev2 + Iv(d).sq()
    return (dev2.sqrt() / Iv.frac(LAMBDA0)).hi


class Space7:
    """Every covariance entry of the 7-jet (other than Var f = 1, exact by the normalization) in [ref - E, ref + E]; the odd block
    (G, t) is independent of the even block (f, V, A) for any even kernel ([LP] section 15)."""

    def __init__(self, E, birth):
        E = Iv.of(E)
        self.birth = birth

        def box(M):
            n = len(M)
            Bx = [[None] * n for _ in range(n)]
            for i in range(n):
                for j in range(i, n):
                    Bx[i][j] = Bx[j][i] = Iv.frac(M[i][j]) + Iv(E.hi.copy_negate(), E.hi)
            return Bx
        CE_ = box(C_EVEN_REF)
        CE_[0][0] = Iv(ONE)
        CO = box(C_ODD_REF)
        G = [[CO[i][j] for j in range(7)] for i in range(7)]
        Ginv, detG = inv_n(G)
        c = [CO[7][j] for j in range(7)]
        self.tau2 = CO[7][7] - sum((c[i] * Ginv[i][j] * c[j] for i in range(7) for j in range(7)), Iv(ZERO))
        self.pG = 1 / (8 * PI.sq() * PI * SQRT2PI * detG.sqrt())         # (2 pi)^(-7/2) det(Cov G)^(-1/2)
        self.Cp, detV = schur(CE_, IDX_X, IDX_V)
        self.pV = 1 / (8 * PI.sq() * PI * SQRT2PI * detV.sqrt())
        self.tau43 = root_iv(self.tau2.sq(), 3)
        self.eps = frob_eps(self.Cp, CPRIME_REF)

    def k_integral(self, K):
        lo, hi = K

        def s(k):
            return k if isinstance(k, float) else 72 * Iv.frac(k * k) / self.tau2
        a = SHAPE()
        return self.tau43 * C72 * (gamma_lower(s(hi), a) - gamma_lower(s(lo), a)) / (2 * SQRT2PI)

    def coefficient(self, B, K):
        sphere = PI.sq() * PI if MUT == "sphere" else 16 * PI.sq() * PI / 15   # |S^6| = 16 pi^3/15
        return 144 * sphere * self.pG * self.pV * sandwich(self.birth, B, self.eps) * self.k_integral(K)


# ---------------- a non-scalar exact test of Lemma S: the tilted pair (f, g)
TILT = (Fr(17, 25), Fr(33, 34), Fr(2261, 86700))                      # v = Var f, mu, sigma^2 with mu^2 v + sigma^2 = 2/3


def tilted_cprime(v, mu, sig2):
    """Covariance of (f, A11, A12, ..., A55) for A = Q - (mu f + sigma Z) I."""
    s = mu * mu * v + sig2
    C = [[Fr(0)] * 22 for _ in range(22)]
    C[0][0] = v
    for i in DIAG_A:
        C[0][i] = C[i][0] = -mu * v
        for j in DIAG_A:
            C[i][j] = s + (2 if i == j else 0)
    for i in OFF_A:
        C[i][i] = Fr(1)
    return C


# ---------------- Owen's T closed form of the Owen-type kinds, and the interval value of F_5 (rules OWEN_EXACT, INNER_LAYERS)
def K_owen(al, g, T):
    """K_{al,g}(T) = int_0^T e^{-al w^2} E_g(w) dw = (pi/sqrt(al g)) [arctan(a)/(2 pi) - T_Owen(sqrt(2 al) T, a)], a = sqrt(g/al) > 1,
    through the reflection T(h, a) = (Phi(h) + Phi(a h))/2 - Phi(h) Phi(a h) - T(a h, 1/a) (h >= 0) and arctan a = pi/2 - arctan(1/a);
    Owen's series of the Math-#197 toolkit with N = 1400 terms (independent of the cumulative Taylor layer)."""
    A = (Iv.frac(g) / Iv.frac(al)).sqrt()
    h = (2 * Iv.frac(al)).sqrt() * Iv.frac(T)
    ah = A * h
    Th = (Phi(h) + Phi(ah)) / 2 - Phi(h) * Phi(ah) - owen_T(ah, 1 / A, N=1400)
    return PI / (Iv.frac(al) * Iv.frac(g)).sqrt() * ((PI / 2 - atan_iv(1 / A, N=400)) / (2 * PI) - Th)


def F_iv(pieces, T):
    """Interval value of F_m(T) from its closed-form pieces (the Owen-type kinds by K_owen); exact rational T."""
    tot = Iv(ZERO)
    Ti = Iv.frac(T)
    for key, poly in pieces.items():
        poly = trim(poly)
        if not poly:
            continue
        pv = Iv.frac(sum(c * Fr(T) ** i for i, c in enumerate(poly)))
        if key[0] == "1":
            tot = tot + pv
        elif key[0] == "e":
            tot = tot + pv * (-(Iv.frac(key[1]) * Ti.sq())).exp()
        elif key[0] == "E":
            tot = tot + pv * (PI / Iv.frac(key[1])).sqrt() / 2 * erf_iv(Iv.frac(key[1]).sqrt() * Ti)
        elif key[0] == "eE":
            al, g = key[1], key[2]
            tot = tot + pv * (-(Iv.frac(al) * Ti.sq())).exp() * (PI / Iv.frac(g)).sqrt() / 2 * erf_iv(Iv.frac(g).sqrt() * Ti)
        elif key[0] == "K":
            tot = tot + pv * K_owen(key[1], key[2], T)
        elif key[0] == "eK":
            tot = tot + pv * (-(Iv.frac(key[1]) * Ti.sq())).exp() * K_owen(key[2], key[3], T)
        else:
            raise ValueError(key)
    return tot


# ---------------- main
S6, S21, S14 = Iv.frac(6).sqrt(), Iv.frac(21).sqrt(), Iv.frac(14).sqrt()
ATAN2 = PI / 2 - atan_iv(Iv.frac(Fr(1, 2)))
D3_CF = (50 * PI + 200 * ATAN2 - 228) / (9 * PI)                  # Math-#201
D4_CF = (Iv.frac(Fr(6695, 54)) - Iv.frac(Fr(405, 32)) * S6        # Math-#202
         - (Iv.frac(Fr(1375, 72)) * S21 + Iv.frac(Fr(6695, 27)) * atan_iv(S21 / 7) + Iv.frac(Fr(405, 16)) * S6 * atan_iv(S14 / 14)) / PI)
R8 = [Fr(3, 1024) * x for x in (11243520, 0, -522240, 0, 28800, 0, -288, 0, 1)]
R6 = [Fr(-256, 729) * x for x in (405, 0, 405, 0, 45, 0, 1)]
STATED_F4 = {("e", Fr(1, 16)): [Fr(1, 31104) * x for x in (0, -991830528, 0, 18489408, 0, -346856, 0, 729)],   # Math-#213, verbatim
             ("E", Fr(1, 16)): R8,
             ("eE", Fr(1, 48), Fr(1, 24)): R6, ("eE", Fr(1, 48), Fr(1, 6)): [2 * x for x in R6],
             ("e", Fr(3, 16)): [Fr(512, 243) * x for x in (0, -297, 0, -42, 0, -1)]}
R10 = (7189875000, 0, 554203125, 0, -14962500, 0, 176750, 0, -700, 0, 1)
R9 = (0, -349281450000, 0, -34608500625, 0, 39341075, 0, -521235, 0, 729)
STATED_F5 = {("e", Fr(1, 5)): [Fr(256, 10546875) * x for x in (-131412150000, 0, -13096721250, 0, 7502375, 0, -174960, 0, 243)],
             ("e", Fr(3, 40)): [Fr(-1, 337500000) * x for x in (-1076528332800000, 0, 241731011520000, 0, -113418584000, 0,
                                                                    4666529880, 0, 150240501)],
             ("eE", Fr(1, 30), Fr(1, 24)): [Fr(256, 158203125) * x for x in R9],
             ("eE", Fr(1, 30), Fr(1, 6)): [Fr(512, 158203125) * x for x in R9],
             ("eE", Fr(1, 80), Fr(1, 16)): [Fr(-3, 500000000) * x for x in (0, -211803379200000, 0, 4362224640000, 0, -26148412800, 0,
                                                                           290979840, 0, 9372409)],
             ("K", Fr(1, 80), Fr(1, 16)): [Fr(576, 9765625) * x for x in R10],
             ("K", Fr(1, 30), Fr(1, 24)): [Fr(768, 9765625) * x for x in R10],
             ("K", Fr(1, 30), Fr(1, 6)): [Fr(1536, 9765625) * x for x in R10]}
R12 = (17156269670400, 0, -361184624640, 0, 17244057600, 0, -174182400, 0, 777600, 0, -1440, 0, 1)
S12 = (2392508671875, 0, -66431531250, 0, 898734375, 0, -7822500, 0, 49125, 0, -210, 0, 1)
Q11 = (0, -4306515046875, 0, 23876996875, 0, -236297250, 0, 1429650, 0, -6075, 0, 27)
STATED_F6 = {("K", Fr(1, 48), Fr(1, 16)): [Fr(5, 39366) * x for x in R12],
             ("eK", Fr(1, 120), Fr(1, 80), Fr(1, 16)): [Fr(-55296, 244140625) * x for x in S12],
             ("eK", Fr(1, 120), Fr(1, 30), Fr(1, 24)): [Fr(-73728, 244140625) * x for x in S12],
             ("eK", Fr(1, 120), Fr(1, 30), Fr(1, 6)): [Fr(-147456, 244140625) * x for x in S12],
             ("e", Fr(1, 12)): [Fr(-1, 170859375000) * x for x in (696502101362688000000, 0, -19424726020382400000, 0,
                                                                     1543288909140360000, 0, 4490688495364200, 0, 15081527796345, 0,
                                                                     12354341056)],
             ("e", Fr(5, 24)): [Fr(-24576, 9765625) * x for x in (-1619841281250, 0, 8110196875, 0, -81472500, 0, 487800, 0, -2070, 0, 9)],
             ("eE", Fr(1, 24), Fr(1, 24)): [Fr(-8192, 48828125) * x for x in Q11],
             ("eE", Fr(1, 24), Fr(1, 6)): [Fr(-16384, 48828125) * x for x in Q11],
             ("eE", Fr(1, 48), Fr(1, 16)): [Fr(-1, 20503125000000) * x for x in (0, 30469360222513728000000, 0, -451869635195452800000, 0,
                                                                               26977353149594304000, 0, 54126362457032400, 0,
                                                                               261305873316375, 0, 123252092672)]}
STAGES_F6 = [(Fr(1, 24), ["('1',)"]),
             (Fr(1, 48), ["('1',)", "('E', Fraction(3, 16))", "('K', Fraction(1, 48), Fraction(1, 24))",
                          "('K', Fraction(1, 48), Fraction(1, 6))"]),
             (Fr(1, 80), ["('1',)", "('E', Fraction(1, 5))", "('E', Fraction(3, 40))"]),
             (Fr(1, 120), ["('1',)", "('E', Fraction(1, 12))", "('E', Fraction(5, 24))", "('K', Fraction(1, 24), Fraction(1, 24))",
                           "('K', Fraction(1, 24), Fraction(1, 6))", "('KK', Fraction(1, 120), Fraction(1, 30), Fraction(1, 24))",
                           "('KK', Fraction(1, 120), Fraction(1, 30), Fraction(1, 6))",
                           "('KK', Fraction(1, 120), Fraction(1, 80), Fraction(1, 16))"])]   # generated by the derivation and zero
MEHTA_F6 = {("K", Fr(1, 48), Fr(1, 16)): [Fr(276480)]}   # the only kind of the Vandermonde-alone layers that survives T -> infinity
OWEN_KINDS = ((Fr(1, 48), Fr(1, 16)), (Fr(1, 80), Fr(1, 16)), (Fr(1, 30), Fr(1, 24)), (Fr(1, 30), Fr(1, 6)))


def K_limit(al, g):
    """K_{al,g}(infinity) = arctan(a)/(2 sqrt(al g)), a = sqrt(g/al), through arctan a = pi/2 - arctan(1/a) for a > 1."""
    A = (Iv.frac(g) / Iv.frac(al)).sqrt()
    at = PI / 2 - atan_iv(1 / A, N=400) if g > al else atan_iv(A, N=400)
    return at / (2 * (Iv.frac(al) * Iv.frac(g)).sqrt())


def label(W):
    def f(x):
        return ("inf" if x > 0 else "-inf") if isinstance(x, float) else str(x)
    return "[%s,%s]" % (f(W[0]), f(W[1]))


def within(iv, fv, tol):
    f, t = Decimal(repr(fv)), Decimal(repr(tol))
    return CE.subtract(iv.lo, f) <= t and CE.subtract(f, iv.hi) <= t


def common_prefix(iv):
    lo, hi = str(iv.lo), str(iv.hi)
    i = 0
    while i < min(len(lo), len(hi)) and lo[i] == hi[i]:
        i += 1
    return lo[:i]


def rel_width(iv):
    return CC.divide(iv.width(), CC.multiply(Decimal(2), iv.lo))


def main():
    global MUT, C_EVEN_REF, C_ODD_REF, CPRIME_REF, DETV_REF, LAMBDA0
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    C_EVEN_REF, C_ODD_REF = ref_matrix(EVEN), ref_matrix(ODD)            # rebuilt: they depend on the mutant
    CPRIME_REF, DETV_REF = schur(C_EVEN_REF, IDX_X, IDX_V)
    LAMBDA0 = Fr(23, 100) if MUT == "d6-floor" else Fr(1, 5)
    Z_MEHTA[6] = 4423680 * PI * SQRTPI * (ONE if MUT == "mehta" else SQRT2)
    t0 = time.time()
    checks = {}
    full, fullK = (-INF, INF), (Fr(0), INF)
    band, bandK = (Fr(0), Fr(1)), (Fr(1, 2), Fr(2))

    # the reference law, exactly
    stated = [[Fr(0)] * 22 for _ in range(22)]
    stated[0][0] = Fr(2, 3)
    for i in DIAG_A:
        stated[0][i] = stated[i][0] = Fr(-2, 3)
        for j in DIAG_A:
            stated[i][j] = Fr(8, 3) if i == j else Fr(2, 3)
    for i in OFF_A:
        stated[i][i] = Fr(1)
    s2 = CPRIME_REF[0][0]
    mean = [CPRIME_REF[i][0] / s2 for i in range(1, 22)]
    condA = [[CPRIME_REF[i][j] - CPRIME_REF[i][0] * CPRIME_REF[0][j] / s2 for j in range(1, 22)] for i in range(1, 22)]
    goe = [[(Fr(2) if i + 1 in DIAG_A else Fr(1)) if i == j else Fr(0) for j in range(21)] for i in range(21)]
    Ginv, detG = inv_n([[C_ODD_REF[i][j] for j in range(7)] for i in range(7)])
    tau2_ref = C_ODD_REF[7][7] - sum(C_ODD_REF[7][i] * Ginv[i][j] * C_ODD_REF[7][j] for i in range(7) for j in range(7))
    checks["REFERENCE_EXACT"] = bool(CPRIME_REF == stated and mean == [-1 if i + 1 in DIAG_A else 0 for i in range(21)]
                                     and condA == goe and DETV_REF == 3 and detG == 1 and tau2_ref == 6
                                     and tilted_cprime(Fr(2, 3), Fr(1), Fr(0)) == CPRIME_REF)
    checks["LAMBDA_FLOOR"] = bool(LAMBDA0 == Fr(1, 5) and sylvester_pd(shifted(CPRIME_REF, LAMBDA0))
                                  and sylvester_pd(shifted(CPRIME_REF, Fr(2063, 10000)))
                                  and not sylvester_pd(shifted(CPRIME_REF, Fr(2064, 10000)))
                                  and not sylvester_pd(shifted(CPRIME_REF, Fr(23, 100))))

    # the exact inner layers: the generated cancellations, the stated closed form, m = 4 and m = 5 against Math-#213 and #222, and the
    # interval value of F_6 (Owen's T for the Owen-type kinds) against a direct float quintuple integral
    pieces6, gamma6, stages6 = F_pieces(6)
    nonzero = {k: trim(v) for k, v in pieces6.items() if trim(v)}
    cancelled = sorted("%s" % (k,) for k, v in pieces6.items() if not trim(v))
    layer_ctrl = {}
    for T in (3, 6, 10):
        fi = F_iv(pieces6, Fr(T))
        layer_ctrl[str(T)] = {"F6_interval": fi.pair(), "F6_direct_float_n16": "%.15g" % Fm_direct_float(6, float(T), 16)}
    checks["INNER_LAYERS"] = bool(nonzero == STATED_F6 and stages6 == STAGES_F6 and gamma6 == Fr(1, 72)
                                  and cancelled == STAGES_F6[-1][1]
                                  and {k: trim(v) for k, v in F_pieces(5)[0].items() if trim(v)} == STATED_F5
                                  and {k: trim(v) for k, v in F_pieces(4)[0].items() if trim(v)} == STATED_F4
                                  and all(within(Iv(Decimal(v["F6_interval"][0]), Decimal(v["F6_interval"][1])),
                                                 float(v["F6_direct_float_n16"]), 1e-10 * abs(float(v["F6_direct_float_n16"])))
                                          for v in layer_ctrl.values()))

    # Mehta's Z_6 through the same layers (the Vandermonde alone): Z_6 = sqrt(24 pi) lim_{T -> infinity} F_6^Vandermonde(T)
    mehta_pieces = {k: trim(v) for k, v in F_pieces(6, mehta=True)[0].items() if trim(v)}
    surviving = {k: v for k, v in mehta_pieces.items() if k[0] in ("1", "E", "K")}
    Zlim = Iv(ZERO)
    for k, v in surviving.items():
        lim = Iv(ONE) if k[0] == "1" else ((PI / Iv.frac(k[1])).sqrt() / 2 if k[0] == "E" else K_limit(k[1], k[2]))
        Zlim = Zlim + Iv.frac(v[0]) * lim
    Zlim = (24 * PI).sqrt() * Zlim
    checks["MEHTA_Z6"] = bool(surviving == MEHTA_F6 and all(len(v) == 1 for v in surviving.values())
                              and all(k[0] in ("e", "eE", "eK") for k in mehta_pieces if k not in surviving)
                              and Zlim.intersects(Z_MEHTA[6]) and Zlim.width() < Zlim.lo * Decimal("1e-55")
                              and Fr(276480) * Fr(8, 3) * 6 == 4423680)       # sqrt(24 pi) (pi/3) 8 sqrt3 = 6 sqrt2 (8/3) pi^(3/2)

    # the reference birth integral: the cumulative layer against Owen's T, D_6, coarse quadrature, m = 2, ..., 5, float control
    ref6 = Birth(6)
    owen = {}
    ok = True
    for kk in OWEN_KINDS:
        rows = {}
        for s0, v in [ref6.M.Kvals[kk][0], ref6.M.Kvals[kk][40]] + [(T_CUT, ref6.M.K_at_cut[kk])]:
            w = K_owen(kk[0], kk[1], s0)
            ok &= v.intersects(w) and v.width() < Decimal("1e-50") and w.width() < Decimal("1e-50")
            rows[str(s0)] = {"cumulative_layer": v.pair(), "owen_T": w.pair()}
        owen["K_%s_%s" % kk] = rows
    checks["OWEN_EXACT"] = bool(ok)
    I_full = ref6.I(full)
    checks["D6_CERTIFIED"] = bool(I_full.width() < Decimal("1e-50") and I_full.lo > 0 and ref6.M.Rsum < Decimal("1e-50")
                                  and ref6.M.tail < Decimal("1e-60"))
    coarse = ref6.pref * Model(g_terms(6), K=8, cell=Fr(2), T=Fr(96), rho=Fr(6)).integral()
    checks["QUAD_COARSE"] = bool(coarse.contains(I_full))
    ref2 = Birth(2)
    cross = {}
    ok = ref2.I(full).intersects(D2_EXACT) and ref2.I(full).width() < Decimal("1e-45")
    for B in ((Fr(0), Fr(1)), (Fr(3), Fr(7, 2)), (-INF, Fr(0))):
        x, y = ref2.I(B), I3_ref(*B)
        ok &= x.intersects(y) and x.width() < Decimal("1e-45")
        cross["m2 " + label(B)] = {"T_quadrature": x.pair(), "Math197_closed_form": y.pair()}
    ref3 = Birth(3)
    F4band = ref3.I(band) / D3_CF
    ok &= ref3.I(full).intersects(D3_CF) and str(F4band.lo).startswith(F4B_209) and str(F4band.hi).startswith(F4B_209)
    cross["m3 full"] = ref3.I(full).pair()
    cross["m3 F^(4)_[0,1]"] = F4band.pair()
    ref4 = Birth(4)
    F5band = ref4.I(band) / D4_CF
    ok &= ref4.I(full).intersects(D4_CF) and str(F5band.lo).startswith(F5B_213) and str(F5band.hi).startswith(F5B_213)
    cross["m4 full"] = ref4.I(full).pair()
    cross["m4 F^(5)_[0,1]"] = F5band.pair()
    ref5 = Birth(5)
    D5_full = ref5.I(full)
    F6band = ref5.I(band) / D5_full
    ok &= (D5_full.intersects(Iv(Decimal(D5_222[0]), Decimal(D5_222[1]))) and D5_full.intersects(Iv(Decimal(D5_204[0]), Decimal(D5_204[1])))
           and str(F6band.lo).startswith(F6B_222) and str(F6band.hi).startswith(F6B_222))
    cross["m5 full"] = D5_full.pair()
    cross["m5 F^(6)_[0,1]"] = F6band.pair()
    checks["CROSSCHECK_M2_M5"] = bool(ok)
    fctrl = {}
    ok = True
    for B in (full, (Fr(0), Fr(1)), (Fr(1), Fr(2))):
        fv, cv = Im_float(6, B), ref6.I(B)
        ok &= within(cv, fv, 1e-9 * fv)
        fctrl[label(B)] = {"float_outer_quadrature": "%.12g" % fv, "certified": cv.pair()}
    checks["FLOAT_CONTROL"] = bool(ok)

    # image bound and epsilon
    E10, E12, E24 = image_bound7(10), image_bound7(12), image_bound7(24)
    checks["IMAGE_BOUND"] = bool(Decimal("2.19e-8") < E10.lo and E10.hi < Decimal("2.20e-8")
                                 and Decimal("1.82e-109") < E24.lo and E24.hi < Decimal("1.83e-109")
                                 and (Iv.frac(4096) * (-Iv.frac(150)).exp()).hi < HALF)
    S0, S10, S12, S24 = Space7(0, ref6), Space7(E10, ref6), Space7(E12, ref6), Space7(E24, ref6)
    checks["EPSILON"] = bool(S0.eps < Decimal("1e-55") and S10.eps < Decimal("6e-6") and S12.eps < Decimal("5e-15")
                             and S24.eps < Decimal("1e-54"))

    # Lemma S against exact scalar perturbations and an exact non-scalar (tilted) covariance
    ok = True
    for eta in (Fr(1, 50), Fr(-1, 50)):
        for B in ((Fr(0), Fr(1)), (Fr(3), Fr(7, 2)), (Fr(-7, 2), Fr(-3))):
            ok &= sandwich(ref6, B, Iv.frac(abs(eta))).contains(scaled_exact(ref6, B, eta))
    checks["SANDWICH_EXACT_SCALING"] = bool(ok)
    tb = Birth(6, *TILT)
    eps_t = frob_eps(tilted_cprime(*TILT), CPRIME_REF)
    full_t = tb.I(full)
    tilt = {"v_mu_sigma2": [str(x) for x in TILT], "eps": str(eps_t), "full_window": full_t.pair(), "windows": {}}
    ok = full_t.intersects(I_full) and Decimal("0.133") < eps_t < Decimal("0.134")
    for B in ((Fr(0), Fr(1)), (Fr(1), Fr(2))):
        if not ok:                                                     # eps outside its certified range: no bracket is formed
            break
        ex, sw, rf = tb.I(B), sandwich(ref6, B, eps_t), ref6.I(B)
        ok &= sw.contains(ex) and not ex.intersects(rf)
        tilt["windows"][label(B)] = {"tilted_exact": ex.pair(), "sandwich": sw.pair(), "reference": rf.pair()}
    checks["TILTED_EXACT"] = bool(ok)

    # the coefficient: reference, every L >= 10, L = 24
    C7_REF = GAMMA76 * CBRT32 * I_full / (120 * SQRT3 * PI.sq().sq() * SQRTPI)   # c_{7,ref} = Gamma(7/6) (3/2)^(1/3) D_6/(120 sqrt3 pi^(9/2))
    C7_GEN = GAMMA76 * CBRT32 * (16 * PI.sq() * PI / 15) * I_full / (SQRT3 * SQRTPI * ipow(2 * PI, 7))   # |S^6| D_6/(sqrt3 sqrt(pi) (2 pi)^7)
    b_windows = [(Fr(0), Fr(1)), (Fr(-1), Fr(1)), (Fr(-2), Fr(2)), (Fr(0), INF), (-INF, Fr(0)), full]
    table = {}
    for B in b_windows:
        F7 = ref6.I(B) / I_full
        for K in (bandK, fullK):
            GK = G_ref(K)
            table["B=%s K=%s" % (label(B), label(K))] = {
                "F7_B": F7.pair(), "G_K": GK.pair(), "c7_ref": (C7_REF * F7 * GK).pair(),
                "c7_torus_L_ge_10": S10.coefficient(B, K).pair(), "c7_torus_L_24": S24.coefficient(B, K).pair()}
    F7_band = ref6.I(band) / I_full
    c_band_ref = C7_REF * F7_band * G_ref(bandK)
    c_band_0, c_band_10, c_band_24 = S0.coefficient(band, bandK), S10.coefficient(band, bandK), S24.coefficient(band, bandK)
    c_full_0, c_full_10, c_full_24 = S0.coefficient(full, fullK), S10.coefficient(full, fullK), S24.coefficient(full, fullK)
    checks["FACTORIZATION"] = bool(c_band_0.intersects(c_band_ref) and c_full_0.intersects(C7_REF))
    checks["C7_CONSISTENT"] = bool(C7_REF.intersects(C7_GEN) and c_full_24.intersects(C7_REF) and c_full_10.contains(C7_REF)
                                   and C7_REF.width() < Decimal("1e-50"))
    checks["NESTING"] = bool(c_band_10.contains(c_band_ref) and c_band_10.intersects(c_band_24)
                             and c_band_10.width() > c_band_24.width() * Decimal(10) ** 30
                             and all(Iv(Decimal(v["c7_torus_L_ge_10"][0]), Decimal(v["c7_torus_L_ge_10"][1])).contains(
                                 Iv(Decimal(v["c7_ref"][0]), Decimal(v["c7_ref"][1]))) for v in table.values()))
    rel10 = rel_width(c_band_10)
    worst = max(rel_width(Iv(Decimal(v["c7_torus_L_ge_10"][0]), Decimal(v["c7_torus_L_ge_10"][1]))) for v in table.values())
    checks["WIDTHS"] = bool(worst < Decimal("2e-4") and c_band_24.width() < c_band_24.lo * Decimal("1e-40"))
    checks["SANDWICH_ORDERED"] = bool(not SANDWICH_VIOLATIONS)
    checks["LIBRARY_EXACT"] = bool(library_exact())
    pinned = {"c_7_ref": C7_REF, "D_6": I_full, "F7|[0,1]": F7_band, "c7|[0,1]x[1/2,2] ref": c_band_ref, "pi": PI}
    checks["PINNED"] = bool(all(str(pinned[k].lo).startswith(p) and str(pinned[k].hi).startswith(p) for k, p in PINNED.items()))
    if len(checks) != 20:
        raise ValueError("rule count changed")
    passed = all(checks.values())

    out = {
        "object": "CL-C8-WINDOW-COEFFICIENT-D7-20261001-v1",
        "scientific_effect": "NONE",
        "certified": True,
        "mutant": MUT,
        "passed": passed,
        "checks": checks,
        "c8_band": {"B": "[0,1]", "K": "[1/2,2]",
                    "c7_reference": c_band_ref.pair(), "c7_reference_digits": common_prefix(c_band_ref),
                    "F7_B": F7_band.pair(), "c7_torus_every_L_ge_10_every_frame": c_band_10.pair(),
                    "c7_torus_L_24": c_band_24.pair(), "relative_half_width_L_ge_10": str(rel10)},
        "full_window": {"D_6": I_full.pair(), "D_6_digits": common_prefix(I_full), "c_7_ref": C7_REF.pair(),
                        "c_7_ref_digits": common_prefix(C7_REF), "c_7_ref_general_formula": C7_GEN.pair(),
                        "c7_torus_every_L_ge_10": c_full_10.pair(), "c7_torus_L_24": c_full_24.pair()},
        "windows": table,
        "worst_relative_half_width_L_ge_10": str(worst),
        "transfer": {"E7_10": E10.pair(), "E7_12": E12.pair(), "E7_24": E24.pair(),
                     "eps_L_ge_10": str(S10.eps), "eps_L_ge_12": str(S12.eps), "eps_L_24": str(S24.eps), "eps_E0": str(S0.eps),
                     "lambda_floor": str(LAMBDA0), "lambda_min_exact": "(10 - 2 sqrt22)/3",
                     "tau2_L_ge_10": S10.tau2.pair(), "pG_pV_L_ge_10": (S10.pG * S10.pV).pair()},
        "reference": {"C_prime": [[str(x) for x in r] for r in CPRIME_REF], "A_given_f_mean": [str(x) for x in mean],
                      "tau2": str(tau2_ref), "det_Cov_V": str(DETV_REF), "coarse_quadrature": coarse.pair(),
                      "F_6_pieces": {"%s" % (k,): [str(x) for x in v] for k, v in sorted(nonzero.items(), key=lambda kv: str(kv[0]))},
                      "layer_cancellations": [[str(c), z] for c, z in stages6],
                      "quadrature_remainder_sum": str(ref6.M.Rsum), "quadrature_tail": str(ref6.M.tail),
                      "Z_6_layers": Zlim.pair(), "Z_6_closed_form": Z_MEHTA[6].pair(),
                      "Z_6_surviving_kinds": {"%s" % (k,): [str(x) for x in v] for k, v in surviving.items()}},
        "owen_type_layer": owen,
        "layers_interval_vs_float": layer_ctrl,
        "crosschecks": cross,
        "float_control": fctrl,
        "tilted": tilt,
        "constants": {"pi": PI.pair(), "Gamma(7/6)": GAMMA76.pair(), "(3/2)^(1/3)": CBRT32.pair()},
        "exact_relations": {
            "window coefficient": "c^(7)_{B,K} = 144 int_{S^6} p_G(0) p_V(0) I_B(u) J_K(u) dsigma(u), I_B = E[1{f in B} det(A)^2 1{A<0} | V=0] ([LP] (11.3), section 15)",
            "reference": "(f, A) | V=0: f ~ N(0, 2/3), A = Q - f I, Q the 6x6 GOE; I^ref_B = (1/(sqrt3 Z_6)) int_0^inf e^{-T^2/72} F_6(T) [Phi((3/sqrt2)(b_+ - T/9)) - Phi((3/sqrt2)(b_- - T/9))] dT",
            "Z_6": "Mehta's integral int |Delta| e^{-|mu|^2/4} over R^6 = 4423680 sqrt2 pi^(3/2) = sqrt(24 pi) * 276480 * K_{1/48,1/16}(infinity), K(infinity) = arctan(sqrt3)/(2 sqrt(1/768)) = 8 sqrt3 pi/3",
            "Owen-type kinds": "K_{al,g}(T) = int_0^T e^{-al w^2} E_g(w) dw = (pi/sqrt(al g)) [arctan(a)/(2 pi) - T_Owen(sqrt(2 al) T, a)], a = sqrt(g/al); eK = e^{-T^2/120} K",
            "sandwich": "(1-eps) C'_ref <= C' <= (1+eps) C'_ref  =>  (1-eps)^17/(1+eps)^11 I^ref_{B/sqrt(1-eps)} <= I'_B <= (1+eps)^17/(1-eps)^11 I^ref_{B/sqrt(1+eps)}",
            "epsilon": "eps = ||C' - C'_ref||_F / lambda0, lambda0 = 1/5 <= lambda_min(C'_ref) = (10 - 2 sqrt22)/3",
            "image bound": "E^(7)_L = 1499596 (76 L^6 + 15) exp(-L^2/2)",
            "c_7_ref": "Gamma(7/6) (3/2)^(1/3) |S^6| D_6 / (sqrt3 sqrt(pi) (2 pi)^7) = Gamma(7/6) (3/2)^(1/3) D_6 / (120 sqrt3 pi^(9/2)), |S^6| = 16 pi^3/15",
        },
    }
    sys.stdout.write(json.dumps(out, indent=1) + "\n")
    sys.stderr.write("seconds %.1f\n" % (time.time() - t0))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
