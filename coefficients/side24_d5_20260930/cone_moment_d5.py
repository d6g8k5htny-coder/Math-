"""SIDE24's coefficient in d = 5: the birth-integrated cone moment D_4, certified, with c_{5,ref} and c_{5,24}.

Standard library only. Run from anywhere:  python -B -S cone_moment_d5.py [--mutant NAME]
Every printed interval [lo, hi] is a rigorous enclosure (interval arithmetic over `decimal` at 60 digits with directed
rounding; exact integer roots; series with explicit remainders; one-dimensional Taylor quadrature with the omitted tail
bounded by Cauchy's estimate at the cell centre and a geometric series).  Nothing is fitted, sampled or extrapolated.

Object.  For the reference law of coefficients/side24_v1 in dimension d = m + 1, A = Q + sqrt(2/3) Z I_m (Q the m x m GOE
of density proportional to exp(-tr Q^2/4)), D_m = E[det(A)^2 1{A < 0}], and (coefficients/side24_d4_20260930, NOTE
section 1)

    D_m = sqrt(3/(m+3)) / Z_m . int_{mu in (-inf,0)^m} prod mu_i^2 prod_{i<j} |mu_i - mu_j| exp(-|mu|^2/4 + S^2/(4(m+3))) dmu.

General decoupling (NOTE section 1).  In the ordered-sector coordinates mu_m = -a, mu_{m-j} = -(a + t_j),
t_j = p_1 + ... + p_j, with T = sum_j t_j and u = t - (T/(m-1)) 1, the a-integral has alpha = 3m/(4(m+3)),
beta = 3T/(2(m+3)), and after it the erfc branch carries exp(-T^2/(4m(m-1)) - |u|^2/4) with erfc(beta/(2 sqrt alpha)),
the polynomial branch exp(-T^2/((m-1)(m+3)) - |u|^2/4).  For m = 4 (this record) the u-integral runs over the triangle
p_2, p_3 > 0, 2 p_2 + p_3 < T with |u|^2/4 = (p_2^2 + p_2 p_3 + p_3^2)/6; in v = 2 p_2 + p_3 this is
(1/2) int_0^T dv e^{-v^2/24} int_0^v dp_3 (.) e^{-p_3^2/8}, the inner integral is exact through
J_k(v) = int_0^v q^k e^{-q^2/8} dq, and the v-integral is carried as the cumulative integrals
L_a(T) = int_0^T e^{-v^2/24} q_a(v) dv (section 2), certified cell by cell together with the outer T-integral (section 3).
Then D_4 = sqrt(3/7) . 4!/Z_4 . (1/6) I_4.  The same machinery evaluates Mehta's constant Z_4 = 1536 pi (a rule), and the
m = 2, 3 pipelines of the d = 4 record are re-run here (29/6 - sqrt6; the D_3 enclosure of Math-#199).

Coefficient.  [LP] (15.2): c_{d,ref} = Gamma(7/6) (3/2)^{1/3} |S^{d-1}| D_{d-1} / (sqrt3 sqrt pi (2 pi)^d); d = 5:
c_{5,ref} = Gamma(7/6) (3/2)^{1/3} D_4 / (12 sqrt3 pi^{7/2}) with |S^4| = 8 pi^2/3; c_{5,24} by the SIDE24 section 3-4
covariance sandwich with the d = 5 constants (NOTE section 4).  Scientific effect NONE.
"""
import argparse
import itertools
import json
import math
import sys
import time
from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN, setcontext
from fractions import Fraction as Fr

MUTANTS = ("shift-variance", "vandermonde", "erfc-branch", "remainder-dropped", "mehta", "sphere-area", "image-shells",
           "sandwich-exponent", "recurrence", "jacobian", "cumulative-half")
MUT = None

PREC = 60
CF = Context(prec=PREC, rounding=ROUND_FLOOR, Emin=-9999999, Emax=9999999)
CC = Context(prec=PREC, rounding=ROUND_CEILING, Emin=-9999999, Emax=9999999)
CE = Context(prec=PREC, rounding=ROUND_HALF_EVEN, Emin=-9999999, Emax=9999999)
# Every arithmetic step names one of the three contexts; operator syntax on Decimals would round to the current context
# (default 28 digits), so it is widened as a safety net and rule LIBRARY_EXACT checks exp, sqrt and the negation.
setcontext(Context(prec=2 * PREC + 20, rounding=ROUND_HALF_EVEN, Emin=-9999999, Emax=9999999))
ZERO, ONE, HALF = Decimal(0), Decimal(1), Decimal("0.5")
ROOT_DIGITS = 70
K_ORDER, RHO, CELL, T_CUT = 40, Fr(6), Fr(1, 2), Fr(60)
CELLS_M4 = [(Fr(i, 2), Fr(i + 1, 2)) for i in range(60)] + [(Fr(30 + i), Fr(31 + i)) for i in range(30)]
CELLS_Z4 = CELLS_M4 + [(Fr(60 + i), Fr(61 + i)) for i in range(30)]          # Z_4 decays only as e^{-T^2/48}
SIDE24 = {2: ("0.07340691930603427103", "0.07340691930603427104"), 3: ("0.04177593184059834334", "0.04177593184059834335")}
D3_PIN = ("5.32318026888989689492319873968726063578438852940845576405060", "5.32318026888989689492319873968726063578438852947338433618854")   # Math-#199 v1.1
PINNED = {"D_4": "14.2187634589773576013064656778740783173406",
          "c_5_ref": "0.0132193193800849680760334875146413965210528",
          "pi": "3.14159265358979323846264338327950288419716939937510"}


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
        return Iv(a.hi.copy_negate(), a.lo.copy_negate())

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

    def mag(a):
        return max(abs(a.lo), abs(a.hi))

    def contains(a, x):
        x = Iv.of(x)
        return a.lo <= x.lo and x.hi <= a.hi

    def intersects(a, b):
        return a.lo <= b.hi and b.lo <= a.hi

    def pair(a):
        return [str(a.lo), str(a.hi)]


def hull(a, b):
    return Iv(min(a.lo, b.lo), max(a.hi, b.hi))


def ipow(x, n):
    r = Iv(ONE)
    for _ in range(n):
        r = r * x
    return r


# ---------------- constants and special functions
def inroot(N, n):
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
    q = Fr(q)
    if q <= 0:
        raise ValueError("root of a nonpositive number")
    p, d = q.numerator, q.denominator
    scale = 10 ** ROOT_DIGITS
    r = inroot(p * d ** (n - 1) * scale ** n, n)
    den = d * scale
    return Iv(Iv.frac(Fr(r, den)).lo, Iv.frac(Fr(r + 1, den)).hi)


def pi_interval():
    def atan_inv(n, terms):
        x = Fr(1, n)
        partial, sums = Iv(ZERO), []
        for m in range(terms + 2):
            t = Iv.frac(x ** (2 * m + 1) / (2 * m + 1))
            partial = partial + t if m % 2 == 0 else partial - t
            sums.append(partial)
        return hull(sums[-1], sums[-2])
    return atan_inv(5, 44) * 16 - atan_inv(239, 22) * 4


PI = pi_interval()
SQRTPI = PI.sqrt()
SQRT2 = Iv.frac(2).sqrt()
SQRT3 = Iv.frac(3).sqrt()
SQRT6 = Iv.frac(6).sqrt()
SQRT2PI = (2 * PI).sqrt()
TINY = Decimal(10) ** (-PREC - 8)


def erf_point(x):
    """erf(x) at a Decimal point by the positive series (2/sqrt pi) e^{-x^2} sum 2^n x^{2n+1}/(2n+1)!!; once the term ratio
    2x^2/(2n+3) is at most 1/2 the omitted tail is at most twice the first omitted term."""
    if x < 0:
        return -erf_point(-x)
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
        if ratio.hi <= HALF and t.hi < S.lo * TINY:
            break
        if n > 200000:
            raise RuntimeError("erf series did not converge")
    return (S + Iv(ZERO, CC.multiply(Decimal(2), t.hi))) * (-x2).exp() * 2 / SQRTPI


def erf_iv(x):
    return Iv(erf_point(x.lo).lo, erf_point(x.hi).hi)


def gamma_lower_point(x, a):
    """gamma(a, x) by the positive series x^a e^-x sum_n x^n/(a (a+1) ... (a+n)); a = 7/6, x a Decimal > 0."""
    X = Iv(x)
    t, S, n = Iv.frac(1 / a), Iv(ZERO), 0
    while True:
        S = S + t
        n += 1
        ratio = X / Iv.frac(a + n)
        t = t * ratio
        if ratio.hi <= HALF and t.hi < S.lo * TINY:
            break
    xa = X * root_frac(Fr(x), 6)
    return xa * (-X).exp() * (S + Iv(ZERO, CC.multiply(Decimal(2), t.hi)))


def gamma_complete(a, X=Decimal(120)):
    """Gamma(a) = gamma(a, X) + Gamma(a, X), 1 < a < 2, X^(a-1) e^-X <= Gamma(a, X) <= X^(a-1) e^-X / (1 - (a-1)/X)."""
    low = gamma_lower_point(X, a)
    up = root_frac(Fr(X), 6) * (-Iv(X)).exp()
    return low + Iv(up.lo, (up / (1 - Iv.frac(a - 1) / Iv(X))).hi)


GAMMA76 = gamma_complete(Fr(7, 6))
CBRT32 = root_frac(Fr(12), 3) / 2                       # (3/2)^(1/3)


def gamma_half_integer(twice):
    """Gamma(twice/2) for a positive integer `twice`, exactly in terms of sqrt pi."""
    if twice % 2 == 0:
        return Iv.frac(math.factorial(twice // 2 - 1))
    k = (twice - 1) // 2                                   # Gamma(k + 1/2) = (2k)! sqrt pi / (4^k k!)
    return Iv.frac(Fr(math.factorial(2 * k), 4 ** k * math.factorial(k))) * SQRTPI


def mehta_Z(m):
    """Z_m = int_{R^m} prod_{i<j} |l_i - l_j| e^{-|l|^2/4} dl (unordered); Mehta's integral at beta = 1 after l = sqrt2 x."""
    if MUT == "mehta":
        m_eff = m + 1 if m == 4 else m
    else:
        m_eff = m
    prod = Iv(ONE)
    for j in range(1, m_eff + 1):
        prod = prod * gamma_half_integer(j + 2)             # Gamma(1 + j/2)
    pw = Fr(m_eff, 2) + Fr(m_eff * (m_eff - 1), 4)         # exponent of 2
    two_pow = Iv.frac(2 ** int(pw)) * (SQRT2 if pw.denominator == 2 else Iv(ONE))
    twopi_pow = ipow(2 * PI, m_eff // 2) * (SQRT2PI if m_eff % 2 else Iv(ONE))
    return two_pow * twopi_pow * prod / ipow(gamma_half_integer(3), m_eff)


def sphere_area(d):
    """|S^{d-1}| = 2 pi^{d/2} / Gamma(d/2)."""
    if MUT == "sphere-area" and d == 5:
        return 4 * PI * PI
    pi_pow = ipow(PI, d // 2) * (SQRTPI if d % 2 else Iv(ONE))
    return 2 * pi_pow / gamma_half_integer(d)


# ---------------- exact polynomial algebra (dict of exponent tuples -> Fraction)
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


def ppow(u, n, nvars):
    r = pconst(1, nvars)
    for _ in range(n):
        r = pmul(r, u)
    return r


def psubst(u, images, nvars_out):
    """Substitute variable i -> images[i] (polynomials in nvars_out variables)."""
    out = {}
    for k, c in u.items():
        term = pconst(c, nvars_out)
        for i, e in enumerate(k):
            if e:
                term = pmul(term, ppow(images[i], e, nvars_out))
        out = padd(out, term)
    return out


def univariate(u):
    """dict {(n,): c} -> list of Fractions by power."""
    if not u:
        return [Fr(0)]
    deg = max(k[0] for k in u)
    return [u.get((n,), Fr(0)) for n in range(deg + 1)]


def reduce_sector(m):
    """The m-dimensional sector integrand in (a, p_1, ..., p_{m-1}) with mu_m = -a, mu_{m-1} = -a - p_1, ...:
    returns (polynomial, quadratic form) with polynomial = prod mu_i^2 prod_{i<j} (mu_j - mu_i) and
    quadratic form = |mu|^2/4 - S^2/(4(m+3)) as dicts in m variables (a first)."""
    nv = m
    a = pvar(0, nv)
    mus = []                                               # mu_m, mu_{m-1}, ..., mu_1 (each = -(a + p_1 + ...))
    acc = a
    for i in range(m):
        if i > 0:
            acc = padd(acc, pvar(i, nv))
        mus.append(pscale(acc, Fr(-1)))
    poly = pconst(1, nv)
    for mu in mus:
        poly = pmul(poly, pmul(mu, mu))
    if MUT != "vandermonde":
        for i in range(m):
            for j in range(i + 1, m):
                poly = pmul(poly, padd(mus[i], pscale(mus[j], Fr(-1))))      # mu_(later index) is larger: mus[i] - mus[j] > 0
    S = {}
    norm2 = {}
    for mu in mus:
        S = padd(S, mu)
        norm2 = padd(norm2, pmul(mu, mu))
    shift = Fr(1, 4 * (m + 3)) if MUT != "shift-variance" or m != 4 else Fr(1, 24)
    quad = padd(pscale(norm2, Fr(1, 4)), pscale(pmul(S, S), -shift))
    return poly, quad


# ---------------- Taylor-model quadrature with Cauchy remainders
class Factor:
    """An entire factor g(s): point Taylor coefficients at a rational centre s0 (list of K+1 intervals) and a bound M on
    |g(z)| for |z - s0| <= rho."""

    def coefficients(self, s0, K):
        raise NotImplementedError

    def disc_bound(self, s0, rho):
        raise NotImplementedError


class Gauss(Factor):
    """exp(-gamma s^2)."""

    def __init__(self, gamma):
        self.gamma = Fr(gamma)

    def coefficients(self, s0, K):
        g = Iv.frac(self.gamma)
        S0 = Iv.frac(s0)
        y = [(-(g * S0.sq())).exp()]
        prev = Iv(ZERO)
        for n in range(K):
            nxt = -(2 * g) * (S0 * y[n] + prev) / (n + 1)   # (n+1) y_{n+1} = -2 gamma (s0 y_n + y_{n-1})
            prev = y[n]
            y.append(nxt)
        return y

    def disc_bound(self, s0, rho):
        g = Iv.frac(self.gamma)
        inner = max(Fr(0), abs(Fr(s0)) - Fr(rho))
        return (g * Iv.frac(rho * rho) - g * Iv.frac(inner * inner)).exp()   # |e^{-g z^2}| = e^{-g(x^2 - y^2)}


class ErfLin(Factor):
    """erf(kappa s) (sign +1) or erfc(kappa s) (sign -1); kappa an interval."""

    def __init__(self, kappa, sign):
        self.kappa, self.sign = kappa, sign

    def coefficients(self, s0, K):
        k = self.kappa
        S0 = Iv.frac(s0)
        e = erf_iv(k * S0)
        c0 = e if self.sign > 0 else 1 - e
        # derivative of erf(kappa s) is (2 kappa/sqrt pi) exp(-kappa^2 s^2): coefficients of the Gaussian in s
        k2 = k.sq()
        y = [(-(k2 * S0.sq())).exp()]
        prev = Iv(ZERO)
        for n in range(K):
            nxt = -(2 * k2) * (S0 * y[n] + prev) / (n + 1)
            prev = y[n]
            y.append(nxt)
        pref = 2 * k / SQRTPI * self.sign
        return [c0] + [pref * y[n] / (n + 1) for n in range(K)]

    def disc_bound(self, s0, rho):
        k = self.kappa
        seg = 2 * k / SQRTPI * Iv.frac(abs(Fr(s0)) + Fr(rho)) * (k.sq() * Iv.frac(Fr(rho) ** 2)).exp()
        return seg if self.sign > 0 else 1 + seg


class Poly(Factor):
    """Polynomial with rational coefficients (list by power)."""

    def __init__(self, coeffs):
        self.c = list(coeffs)

    def coefficients(self, s0, K):
        # Taylor coefficients at s0: sum_j c_j C(j, n) s0^(j-n)
        out = []
        for n in range(K + 1):
            v = Fr(0)
            for j, cj in enumerate(self.c):
                if j >= n:
                    v += cj * math.comb(j, n) * Fr(s0) ** (j - n)
            out.append(Iv.frac(v))
        return out

    def disc_bound(self, s0, rho):
        r = abs(Fr(s0)) + Fr(rho)
        return Iv.frac(sum(abs(cj) * r ** j for j, cj in enumerate(self.c)))


class Jk(Factor):
    """J_k(s) = int_0^s q^k e^{-q^2/8} dq: J_0 = sqrt(2 pi) erf(s/(2 sqrt2)), J_1 = 4 (1 - e^{-s^2/8}),
    J_{k+2}(s) = -4 s^{k+1} e^{-s^2/8} + 4 (k+1) J_k(s)."""

    def __init__(self, k):
        self.k = k

    _cache = {}

    def coefficients(self, s0, K):
        key = (s0, K)
        chain = Jk._cache.get(key)
        if chain is None or len(chain) <= self.k:
            E3 = Gauss(Fr(1, 8)).coefficients(s0, K)
            J0 = [c * SQRT2PI for c in ErfLin(1 / (2 * SQRT2), +1).coefficients(s0, K)]
            J1 = [Iv.frac(4) - 4 * E3[0]] + [-4 * c for c in E3[1:]]
            chain = [J0, J1]
            for k in range(max(self.k, 9) - 1):
                sp = Poly([Fr(0)] * (k + 1) + [Fr(1)]).coefficients(s0, K)     # s^{k+1}
                chain.append(t_add(t_scale(t_mul(sp, E3), Fr(-4)), t_scale(chain[k], Fr(4 * (k + 1)))))
            Jk._cache = {key: chain}
        return chain[self.k]

    def infinity(self):
        """J_k(inf) = (1/2) 8^{(k+1)/2} Gamma((k+1)/2), as an interval."""
        k = self.k
        eight = Iv.frac(8 ** ((k + 1) // 2)) * (SQRT2 * 2 if (k + 1) % 2 else Iv(ONE))
        return eight * gamma_half_integer(k + 1) / 2

    def disc_bound(self, s0, rho):
        r = Iv.frac(abs(Fr(s0)) + Fr(rho))
        return ipow(r, self.k + 1) * (Iv.frac(Fr(rho) ** 2 / 8)).exp() / (self.k + 1)


def t_mul(u, v):
    K = len(u) - 1
    out = []
    for n in range(K + 1):
        acc = Iv(ZERO)
        for i in range(n + 1):
            acc = acc + u[i] * v[n - i]
        out.append(acc)
    return out


def t_add(u, v):
    return [x + y for x, y in zip(u, v)]


def t_scale(u, c):
    return [x * c for x in u]


def enclose_integral(branches, K=None, cell=None, T=None, rho=None, remainder=True):
    """int_0^T of sum over branches of const * prod(prefactors) * sum_pairs poly * J, plus the tail bound.  A branch is
    (const Iv, [prefactor factors], [(Poly, Jk or None)], tail_poly, gamma): for s >= T the branch is bounded in absolute
    value by |const| tail_poly(s) e^{-gamma s^2} (tail_poly a rational polynomial by power).  On each cell the point Taylor
    coefficients of the product are integrated exactly; the tail sum_{n > K} c_n x^n of the (everywhere convergent) Taylor
    series at the centre is bounded through Cauchy's estimate at the centre, |c_n| <= M_F(rho)/rho^n, M_F the product/sum of
    the factors' disc bounds, and the geometric series in |x|/rho <= h/(2 rho) (v1.1: the v1.0 text applied the estimate
    off-centre without shrinking the radius; Codex 4148001628)."""
    K = K_ORDER if K is None else K
    cell = CELL if cell is None else cell
    T = T_CUT if T is None else T
    rho = RHO if rho is None else rho
    ncell = int(T / cell)
    if ncell * cell != T:
        raise ValueError("cell does not divide T")
    half = cell / 2
    total = Iv(ZERO)
    even_moments = [Iv.frac(2 * half ** (n + 1) / (n + 1)) if n % 2 == 0 else None for n in range(K + 1)]
    # int_{-h/2}^{h/2} sum_{n>K} |c_n| |x|^n dx <= M_F sum_{n>K} rho^-n 2 (h/2)^(n+1)/(n+1)
    #                                          <= M_F rho^-(K+1) 2 (h/2)^(K+2)/(K+2) . 1/(1 - h/(2 rho))
    if Fr(half) >= Fr(rho):
        raise ValueError("cell half-width must be below the Cauchy radius")
    rem_moment = Iv.frac(2 * half ** (K + 2) / (K + 2) / (1 - Fr(half) / Fr(rho)))
    rho_pow = Iv.frac(Fr(rho) ** (K + 1))
    for c in range(ncell):
        s0 = (2 * c + 1) * half
        cell_val = Iv(ZERO)
        M_F = Iv(ZERO)
        for const, prefactors, pairs, _, _ in branches:
            acc, M_acc = None, Iv(ZERO)
            for poly, jk in pairs:
                pc = poly.coefficients(s0, K)
                M_pair = poly.disc_bound(s0, rho)
                if jk is not None:
                    pc = t_mul(pc, jk.coefficients(s0, K))
                    M_pair = M_pair * jk.disc_bound(s0, rho)
                acc = pc if acc is None else t_add(acc, pc)
                M_acc = M_acc + M_pair
            M = M_acc
            for f in prefactors:
                acc = t_mul(acc, f.coefficients(s0, K))
                M = M * f.disc_bound(s0, rho)
            for n in range(0, K + 1, 2):
                cell_val = cell_val + const * acc[n] * even_moments[n]
            M_F = M_F + Iv(const.mag()) * M
        if remainder:
            R = (M_F / rho_pow * rem_moment).hi
            cell_val = cell_val + Iv(-R, R)
        total = total + cell_val
    # tail: int_T^inf s^j e^{-gamma s^2} ds = (1/2) gamma^{-(j+1)/2} Gamma((j+1)/2, gamma T^2),
    # Gamma(a, x) <= x^(a-1) e^-x / (1 - (a-1)/x) for a > 1, <= x^(a-1) e^-x for a <= 1
    tail = Iv(ZERO)
    for const, _, _, tail_poly, gamma in branches:
        g = Iv.of(gamma)
        x = g * Iv.frac(T * T)
        for j, cj in enumerate(tail_poly):
            if cj == 0:
                continue
            a = Fr(j + 1, 2)
            if a.denominator == 2:
                xa1 = ipow(x, int(a - Fr(1, 2))) * x.sqrt() / x
                gpow = ipow(g, int(a)) * g.sqrt()
            else:
                xa1 = ipow(x, int(a) - 1)
                gpow = ipow(g, int(a))
            up = xa1 * (-x).exp()
            if a > 1:
                up = up / (1 - Iv.frac(a - 1) / x)
            tail = tail + Iv(const.mag()) * Iv.frac(abs(cj)) * up / gpow / 2
    return total + Iv(-tail.hi, tail.hi)


# ---------------- the reductions (m = 2, 3 as in coefficients/side24_d4_20260930)
def a_integrated_terms(m):
    """For m = 2 and m = 3: integrate the sector polynomial times e^{-Q} over a in (0, inf) exactly; returns the erfc-branch
    and polynomial-branch integrands as polynomials in the remaining variables with their (decoupled) exponents."""
    poly, quad = reduce_sector(m)
    nv = m
    # quad = alpha a^2 + a * beta(p) + rest(p)
    alpha = quad.get((2,) + (0,) * (nv - 1), Fr(0))
    beta = {k[1:]: c for k, c in quad.items() if k[0] == 1}
    rest = {k[1:]: c for k, c in quad.items() if k[0] == 0}
    # G_n = P_n(beta) G_0 + R_n(beta), G_0 = (1/2) sqrt(pi/alpha) e^{beta^2/(4 alpha)} erfc(beta/(2 sqrt alpha))
    nvr = nv - 1
    P = [pconst(1, nvr), pscale(beta, Fr(-1, 2) / alpha)]
    R = [{}, pconst(Fr(1, 2) / alpha, nvr)]
    deg_a = max(k[0] for k in poly)
    for n in range(1, deg_a):
        P.append(pscale(padd(pscale(P[n - 1], Fr(n)), pscale(pmul(beta, P[n]), Fr(-1))), Fr(1, 2) / alpha))
        R.append(pscale(padd(pscale(R[n - 1], Fr(n)), pscale(pmul(beta, R[n]), Fr(-1))), Fr(1, 2) / alpha))
    if MUT == "recurrence":
        P[3] = pscale(P[3], Fr(101, 100))
    PE, PR = {}, {}
    for k, c in poly.items():
        n = k[0]
        w = {k[1:]: c}
        PE = padd(PE, pmul(w, P[n]))
        PR = padd(PR, pmul(w, R[n]))
    # exponents: erfc branch  -(rest - beta^2/(4 alpha)),  polynomial branch  -rest
    expE = padd(rest, pscale(pmul(beta, beta), Fr(-1, 4) / alpha))
    return alpha, beta, PE, PR, expE, rest


def d2_terms():
    """m = 2: one remaining variable p; erfc branch e^{-p^2/8} erfc(p sqrt30/20), polynomial branch e^{-p^2/5}."""
    alpha, beta, PE, PR, expE, rest = a_integrated_terms(2)
    if set(expE) - {(2,)} or set(rest) - {(2,)} or set(beta) - {(1,)}:
        raise ValueError("m = 2 structure")
    gE, gR, b1 = expE[(2,)], rest[(2,)], beta[(1,)]
    kappa = Iv.frac(b1) / (2 * Iv.frac(alpha).sqrt())                            # erfc argument slope
    constE = Iv.frac(Fr(1, 2)) * (PI / Iv.frac(alpha)).sqrt()
    pref = (Iv.frac(Fr(3, 5))).sqrt() / mehta_Z(2) * 2                           # sqrt(3/(m+3)) . (m! sectors) / Z_m
    pe, pr = univariate(PE), univariate(PR)
    tE = (pref * constE, [Gauss(gE), ErfLin(kappa, -1)], [(Poly(pe), None)], [2 * abs(c) for c in pe], gE)
    tR = (pref, [Gauss(gR)], [(Poly(pr), None)], [abs(c) for c in pr], gR)
    return [tE, tR]


def d3_terms():
    """m = 3: remaining (p, q); substitute p = (s - q)/2 (Jacobian 1/2), integrate q over (0, s) exactly through J_k."""
    alpha, beta, PE, PR, expE, rest = a_integrated_terms(3)
    s, q = pvar(0, 2), pvar(1, 2)
    p_img = pscale(padd(s, pscale(q, Fr(-1))), Fr(1, 2))
    images = [p_img, q]
    PEs, PRs = psubst(PE, images, 2), psubst(PR, images, 2)
    eE, eR, bs = psubst(expE, images, 2), psubst(rest, images, 2), psubst(beta, images, 2)
    # the decoupling: exponents must be diagonal in (s, q) with q^2 coefficient 1/8, and beta must be a multiple of s
    if set(eE) != {(2, 0), (0, 2)} or set(eR) != {(2, 0), (0, 2)} or eE[(0, 2)] != Fr(1, 8) or eR[(0, 2)] != Fr(1, 8) or set(bs) != {(1, 0)}:
        raise ValueError("decoupling failed: " + repr((eE, eR, bs)))
    gE, gR = eE[(2, 0)], eR[(2, 0)]
    kappa = Iv.frac(bs[(1, 0)]) / (2 * Iv.frac(alpha).sqrt())
    constE = Iv.frac(Fr(1, 2)) * (PI / Iv.frac(alpha)).sqrt()
    pref = (Iv.frac(Fr(1, 2))).sqrt() / mehta_Z(3) * 6 / 2                     # sqrt(3/6) . 3! / Z_3 . Jacobian 1/2
    branches = []
    def by_q_power(Pxy):
        out = {}
        for (i, j), c in Pxy.items():
            out.setdefault(j, {})[(i,)] = c
        return out
    for branch, Pxy, g, const, extra in (("E", PEs, gE, pref * constE, [ErfLin(kappa, -1)]), ("R", PRs, gR, pref, [])):
        pairs, tail_poly = [], {}
        for k, coef_poly in sorted(by_q_power(Pxy).items()):
            ek = univariate(coef_poly)
            jk = Jk(k)
            pairs.append((Poly(ek), jk))
            # tail bound for s >= T: |J_k(s)| <= J_k(inf), erfc <= 2; rational upper bound of J_k(inf) from its interval
            jk_bound = Fr(jk.infinity().hi) * (2 if branch == "E" else 1)
            for j, c in enumerate(ek):
                tail_poly[j] = tail_poly.get(j, Fr(0)) + abs(c) * jk_bound
        tp = [tail_poly.get(j, Fr(0)) for j in range(max(tail_poly) + 1)]
        branches.append((const, [Gauss(g)] + extra, pairs, tp, g))
    return branches


# ---------------- m = 4
def t_mul_poly(pc, tm):
    """Product of a short coefficient list pc (a polynomial's Taylor coefficients) with a full Taylor list tm."""
    K = len(tm) - 1
    out = []
    for n in range(K + 1):
        acc = Iv(ZERO)
        for i in range(min(n, len(pc) - 1) + 1):
            acc = acc + pc[i] * tm[n - i]
        out.append(acc)
    return out


def poly_taylor_short(coeffs, s0):
    """Taylor coefficients at s0 of sum_j coeffs[j] s^j, all degrees (exact rationals as intervals)."""
    deg = len(coeffs) - 1
    out = []
    for n in range(deg + 1):
        v = Fr(0)
        for j in range(n, deg + 1):
            v += coeffs[j] * math.comb(j, n) * Fr(s0) ** (j - n)
        out.append(Iv.frac(v))
    return out


def gauss_moment(j, gamma):
    """int_0^inf v^j e^{-gamma v^2} dv = (1/2) gamma^{-(j+1)/2} Gamma((j+1)/2), as an interval."""
    g = Iv.frac(gamma)
    a2 = j + 1
    gpow = ipow(g, a2 // 2) * (g.sqrt() if a2 % 2 else Iv(ONE))
    return gamma_half_integer(a2) / gpow / 2


def organize_tvp(P):
    """Polynomial dict in (T, v, p3) -> {a: {k: [coefficients in v by power]}} (a = T power, k = p3 power)."""
    out = {}
    for (i, j, k), c in P.items():
        out.setdefault(i, {}).setdefault(k, {})[j] = c
    return {a: {k: [d.get(j, Fr(0)) for j in range(max(d) + 1)] for k, d in ks.items()} for a, ks in out.items()}


def m4_setup():
    """The two branches of I_4 after the exact a- and p3-integrations, organised for the (T, L_a) quadrature."""
    m = 4
    alpha, beta, PE, PR, expE, rest = a_integrated_terms(m)
    # p1 = (T - 2 p2 - p3)/3 -> variables (T, p2, p3)
    T, p2, p3 = pvar(0, 3), pvar(1, 3), pvar(2, 3)
    p1 = pscale(padd(T, padd(pscale(p2, Fr(-2)), pscale(p3, Fr(-1)))), Fr(1, 3))
    img1 = [p1, p2, p3]
    PE1, PR1 = psubst(PE, img1, 3), psubst(PR, img1, 3)
    eE1, eR1, b1 = psubst(expE, img1, 3), psubst(rest, img1, 3), psubst(beta, img1, 3)
    # p2 = (v - p3)/2 -> variables (T, v, p3)
    T2, v, q = pvar(0, 3), pvar(1, 3), pvar(2, 3)
    img2 = [T2, pscale(padd(v, pscale(q, Fr(-1))), Fr(1, 2)), q]
    PE2, PR2 = psubst(PE1, img2, 3), psubst(PR1, img2, 3)
    eE2, eR2, b2 = psubst(eE1, img2, 3), psubst(eR1, img2, 3), psubst(b1, img2, 3)
    diag = {(2, 0, 0), (0, 2, 0), (0, 0, 2)}
    for e in (eE2, eR2):
        if set(e) != diag or e[(0, 2, 0)] != Fr(1, 24) or e[(0, 0, 2)] != Fr(1, 8):
            raise ValueError("m = 4 decoupling failed: " + repr(e))
    if set(b2) != {(1, 0, 0)}:
        raise ValueError("beta is not a multiple of T: " + repr(b2))
    gE, gR = eE2[(2, 0, 0)], eR2[(2, 0, 0)]
    bT = b2[(1, 0, 0)]
    kappa = Iv.frac(bT) / (2 * Iv.frac(alpha).sqrt())
    kappa2 = bT * bT / (4 * alpha)                                                 # rational: erfc(kappa T) <= e^{-kappa2 T^2}
    constE = Iv.frac(Fr(1, 2)) * (PI / Iv.frac(alpha)).sqrt()
    if MUT == "erfc-branch":
        constE = constE * Iv.frac(Fr(1, 2))
    jac = Fr(1, 6) if MUT != "jacobian" else Fr(1, 2)                              # dp1 dp2 dp3 = (1/3)(1/2) dT dv dp3
    pref = (Iv.frac(Fr(3, m + 3))).sqrt() / mehta_Z(m) * math.factorial(m) * Iv.frac(jac)
    branches = []
    for name, P, g, const, extra, gtail in (("E", PE2, gE, pref * constE, [ErfLin(kappa, -1)], gE + kappa2),
                                            ("R", PR2, gR, pref, [], gR)):
        inner = organize_tvp(P)
        # tail: |sum_a T^a L_a(T)| <= sum_a T^a Lbar_a, Lbar_a = sum_k sum_j |e_{a,k,j}| J_k(inf) int_0^inf v^j e^{-v^2/24} dv
        tail = {}
        for a, ks in inner.items():
            lb = Iv(ZERO)
            for k, ek in ks.items():
                jinf = Jk(k).infinity()
                for j, c in enumerate(ek):
                    if c:
                        lb = lb + Iv.frac(abs(c)) * jinf * gauss_moment(j, Fr(1, 24))
            tail[a] = Fr(lb.hi)
        tail_poly = [tail.get(a, Fr(0)) for a in range(max(tail) + 1)]
        branches.append({"name": name, "const": const, "prefactors": [Gauss(g)] + extra, "inner": inner,
                         "tail_poly": tail_poly, "gamma": gtail})
    return branches


def z4_setup():
    """Mehta's Z_4 through the same triangle machinery: Z_4 = 4! sqrt pi (1/6) int dT e^{-T^2/48} int_0^T dv e^{-v^2/24}
    int_0^v dp3 V e^{-p3^2/8}, V the Vandermonde p1 p2 p3 (p1+p2)(p2+p3)(p1+p2+p3) with p1 = (T - v)/3, p2 = (v - p3)/2."""
    T, v, q = pvar(0, 3), pvar(1, 3), pvar(2, 3)
    p1 = pscale(padd(T, pscale(v, Fr(-1))), Fr(1, 3))
    p2 = pscale(padd(v, pscale(q, Fr(-1))), Fr(1, 2))
    p3 = q
    V = pconst(1, 3)
    for f in (p1, p2, p3, padd(p1, p2), padd(p2, p3), padd(padd(p1, p2), p3)):
        V = pmul(V, f)
    jac = Fr(1, 6) if MUT != "jacobian" else Fr(1, 2)
    const = Iv.frac(24 * jac) * SQRTPI
    inner = organize_tvp(V)
    tail = {}
    for a, ks in inner.items():
        lb = Iv(ZERO)
        for k, ek in ks.items():
            jinf = Jk(k).infinity()
            for j, c in enumerate(ek):
                if c:
                    lb = lb + Iv.frac(abs(c)) * jinf * gauss_moment(j, Fr(1, 24))
        tail[a] = Fr(lb.hi)
    tail_poly = [tail.get(a, Fr(0)) for a in range(max(tail) + 1)]
    return [{"name": "Z4", "const": const, "prefactors": [Gauss(Fr(1, 48))], "inner": inner, "tail_poly": tail_poly,
             "gamma": Fr(1, 48)}]


def enclose_m4(branches, K=None, rho=None, cells=None, remainder=True):
    """int_0^{T_max} sum_branches const . prod(prefactors)(T) . sum_a T^a L_a(T) dT + tail, with
    L_a(T) = int_0^T e^{-v^2/24} q_a(v) dv, q_a = sum_k e_{a,k}(v) J_k(v), carried as Taylor factors: at each cell centre
    s_0 the value L_a(s_0) is the accumulated certified integral over [0, s_0] (full cells so far plus the left half of
    this cell) and the higher coefficients are those of the integrand divided by n.  Remainders as in enclose_integral
    (Cauchy at the centre, geometric factor); the disc bound of L_a is |L_a(s_0)| + rho . M_g."""
    K = K_ORDER if K is None else K
    rho = RHO if rho is None else rho
    cells = CELLS_M4 if cells is None else cells
    rho_pow = Iv.frac(Fr(rho) ** (K + 1))
    G24 = Gauss(Fr(1, 24))
    L = {(bi, a): Iv(ZERO) for bi, br in enumerate(branches) for a in br["inner"]}
    total = Iv(ZERO)
    for lo, hi in cells:
        h = Fr(hi) - Fr(lo)
        half = h / 2
        s0 = Fr(lo) + half
        if half >= Fr(rho):
            raise ValueError("cell half-width must be below the Cauchy radius")
        geom = 1 / (1 - half / Fr(rho))
        full_even = {n: Iv.frac(2 * half ** (n + 1) / (n + 1)) for n in range(0, K + 1, 2)}
        left = [Iv.frac((-1) ** n * half ** (n + 1) / (n + 1)) for n in range(K + 1)]      # int_{-h/2}^0 x^n dx
        rem_half = Iv.frac(half ** (K + 2) / (K + 2) * geom)
        rem_full = rem_half * 2
        g24 = G24.coefficients(s0, K)
        M24 = G24.disc_bound(s0, rho)
        outer_val, M_outer = Iv(ZERO), Iv(ZERO)
        for bi, br in enumerate(branches):
            acc, M_acc = None, Iv(ZERO)
            for a, ks in br["inner"].items():
                qsum, M_q = None, Iv(ZERO)
                for k, ek in ks.items():
                    jk = Jk(k)
                    prod = t_mul_poly(poly_taylor_short(ek, s0), jk.coefficients(s0, K))
                    qsum = prod if qsum is None else t_add(qsum, prod)
                    M_q = M_q + Poly(ek).disc_bound(s0, rho) * jk.disc_bound(s0, rho)
                g = t_mul(qsum, g24)
                M_g = M_q * M24
                Ihalf, Ifull = Iv(ZERO), Iv(ZERO)
                for n in range(K + 1):
                    Ihalf = Ihalf + g[n] * left[n]
                    if n % 2 == 0:
                        Ifull = Ifull + g[n] * full_even[n]
                if remainder:
                    Rh = (M_g / rho_pow * rem_half).hi
                    Ihalf = Ihalf + Iv(-Rh, Rh)
                    Ifull = Ifull + Iv(-2 * Rh, 2 * Rh)
                Lc = L[(bi, a)] + (Ihalf if MUT != "cumulative-half" else Iv(ZERO))
                L[(bi, a)] = L[(bi, a)] + Ifull
                cum = [Lc] + [g[n - 1] / n for n in range(1, K + 1)]
                M_cum = Iv(Lc.mag()) + Iv.frac(rho) * M_g
                ta = poly_taylor_short([Fr(0)] * a + [Fr(1)], s0)
                term = t_mul_poly(ta, cum)
                M_term = Poly([Fr(0)] * a + [Fr(1)]).disc_bound(s0, rho) * M_cum
                acc = term if acc is None else t_add(acc, term)
                M_acc = M_acc + M_term
            M = M_acc
            for f in br["prefactors"]:
                acc = t_mul(acc, f.coefficients(s0, K))
                M = M * f.disc_bound(s0, rho)
            for n in range(0, K + 1, 2):
                outer_val = outer_val + br["const"] * acc[n] * full_even[n]
            M_outer = M_outer + Iv(br["const"].mag()) * M
        if remainder:
            R = (M_outer / rho_pow * rem_full).hi
            outer_val = outer_val + Iv(-R, R)
        total = total + outer_val
    Tmax = Fr(cells[-1][1])
    tail = Iv(ZERO)
    for br in branches:
        g = Iv.of(br["gamma"])
        x = g * Iv.frac(Tmax * Tmax)
        for j, cj in enumerate(br["tail_poly"]):
            if cj == 0:
                continue
            a = Fr(j + 1, 2)
            if a.denominator == 2:
                xa1 = ipow(x, int(a - Fr(1, 2))) * x.sqrt() / x
                gpow = ipow(g, int(a)) * g.sqrt()
            else:
                xa1 = ipow(x, int(a) - 1)
                gpow = ipow(g, int(a))
            up = xa1 * (-x).exp()
            if a > 1:
                up = up / (1 - Iv.frac(a - 1) / x)
            tail = tail + Iv(br["const"].mag()) * Iv.frac(abs(cj)) * up / gpow / 2
    return total + Iv(-tail.hi, tail.hi)


# ---------------- floating controls
def mehta_Z_float(m):
    return 2 ** (m / 2 + m * (m - 1) / 4) * (2 * math.pi) ** (m / 2) * math.prod(math.gamma(1 + j / 2) for j in range(1, m + 1)) / math.gamma(1.5) ** m


def float_orthant(m, T, n):
    coef = math.sqrt(3 / (m + 3)) / mehta_Z_float(m)
    h = T / n
    grid = [-(i + 0.5) * h for i in range(n)]
    total = 0.0
    for mu in itertools.product(grid, repeat=m):
        S = sum(mu)
        w = 1.0
        for x in mu:
            w *= x * x
        for i in range(m):
            for j in range(i + 1, m):
                w *= abs(mu[i] - mu[j])
        total += w * math.exp(-sum(x * x for x in mu) / 4 + S * S / (4 * (m + 3)))
    return coef * total * h ** m


def float_D4_aint(T=26.0, n=56):
    """m = 4 after the exact a-integral only: 3-D midpoint quadrature over (p1, p2, p3); independent of the (T, v)
    substitutions, the J_k and the cumulative integrals."""
    m = 4
    alpha = 3 * m / (4 * (m + 3))
    def G_list(beta, nmax=8):
        G0 = 0.5 * math.sqrt(math.pi / alpha) * math.exp(beta * beta / (4 * alpha)) * math.erfc(beta / (2 * math.sqrt(alpha)))
        G = [G0, (1 - beta * G0) / (2 * alpha)]
        for k in range(1, nmax):
            G.append((k * G[k - 1] - beta * G[k]) / (2 * alpha))
        return G
    def pm(u, v):
        out = [0.0] * (len(u) + len(v) - 1)
        for i, x in enumerate(u):
            for j, y in enumerate(v):
                out[i + j] += x * y
        return out
    h = T / n
    tot = 0.0
    for i in range(n):
        p1 = (i + 0.5) * h
        for j in range(n):
            p2 = (j + 0.5) * h
            for k in range(n):
                p3 = (k + 0.5) * h
                t1, t2, t3 = p1, p1 + p2, p1 + p2 + p3
                Tsum = t1 + t2 + t3
                beta = 3 * Tsum / (2 * (m + 3))
                rest = (t1 * t1 + t2 * t2 + t3 * t3) / 4 - Tsum * Tsum / (4 * (m + 3))
                G = G_list(beta)
                poly = pm(pm(pm([0, 0, 1.0], [t1 * t1, 2 * t1, 1.0]), [t2 * t2, 2 * t2, 1.0]), [t3 * t3, 2 * t3, 1.0])
                val = sum(poly[q] * G[q] for q in range(9))
                vand = p1 * p2 * p3 * (p1 + p2) * (p2 + p3) * (p1 + p2 + p3)
                tot += val * vand * math.exp(-rest)
    return math.sqrt(3 / 7) * 24 / mehta_Z_float(4) * tot * h ** 3


# ---------------- main
def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    args = ap.parse_args()
    MUT = args.mutant
    t0 = time.time()
    checks = {}

    D2 = enclose_integral(d2_terms(), T=Fr(40))
    D3 = enclose_integral(d3_terms())
    B4 = m4_setup()
    D4 = enclose_m4(B4)
    if MUT == "remainder-dropped":
        D4 = enclose_m4(B4, K=6, cells=[(Fr(i), Fr(i + 1)) for i in range(60)], remainder=False)
    D4_coarse = enclose_m4(B4, K=K_ORDER // 2, cells=[(Fr(i), Fr(i + 1)) for i in range(60)],
                           remainder=MUT != "remainder-dropped")
    Z4 = enclose_m4(z4_setup(), cells=CELLS_Z4)
    D2_exact = Iv.frac(Fr(29, 6)) - SQRT6
    D3_pin = Iv(Decimal(D3_PIN[0]), Decimal(D3_PIN[1]))

    def c_ref(d, D):
        return GAMMA76 * CBRT32 * sphere_area(d) * D / (SQRT3 * SQRTPI * ipow(2 * PI, d))
    c2, c3, c4, c5 = c_ref(2, Iv.frac(Fr(4, 3))), c_ref(3, D2), c_ref(4, D3), c_ref(5, D4)
    c5_closed = GAMMA76 * CBRT32 * D4 / (12 * SQRT3 * PI * PI * PI * SQRTPI)

    # torus transfer d = 5, L = 24: shells (2j+1)^5 - (2j-1)^5 <= 242 j^4, |n|^6 <= 125 j^6, ratio < 1/2
    shells = 30250 if MUT != "image-shells" else 15125
    E5 = Iv.frac(2 * shells * (76 * 24 ** 6 + 15)) * (-Iv.frac(288)).exp()
    n_jet = 5 + 1 + 15
    eps = Iv.frac(6 * n_jet) * E5
    b_exp = 10 if MUT != "sandwich-exponent" else 8                            # d + n_A/2, n_A = 10; a = 29/3 <= 10
    num = Iv(ZERO)
    for k in range(1, 11):
        num = num + Iv.frac(math.comb(10, k) - (-1) ** k * math.comb(b_exp, k)) * ipow(eps, k)
    delta = num / ipow(1 - eps, b_exp)
    ratio = Iv((1 / (1 + delta)).lo, (1 + delta).hi)
    c5_torus = c5 * ratio

    # ---- rules
    f2, f3 = float_orthant(2, 16.0, 400), float_orthant(3, 14.0, 90)
    f4, f4a = float_orthant(4, 14.0, 28), float_D4_aint()
    def near(iv, fv, tol):
        f, t = Decimal(repr(fv)), Decimal(repr(tol))
        return CE.subtract(iv.lo, f) <= t and CE.subtract(f, iv.hi) <= t
    checks["FLOAT_INSIDE"] = bool(near(D2, f2, 2e-3) and near(D3, f3, 2e-2) and near(D4, f4, 1.5) and near(D4, f4a, 0.4))
    checks["D2_EXACT"] = bool(D2.intersects(D2_exact))
    checks["D3_CONSISTENT"] = bool(D3.intersects(D3_pin) and D3.width() < Decimal("1e-40"))
    checks["MEHTA_Z4"] = bool(Z4.intersects(mehta_Z(4)) and Z4.intersects(1536 * PI) and Z4.width() < Decimal("1e-40"))
    checks["WIDTHS"] = bool(D2.width() < Decimal("1e-40") and D4.width() < Decimal("1e-28") and c5.width() < Decimal("1e-28"))
    side = {d: Iv(Decimal(a), Decimal(b)) for d, (a, b) in SIDE24.items()}
    checks["SIDE24_CONSISTENT"] = bool(all(c.intersects(side[d] + Iv(-side[d].hi * Decimal("1e-106"), side[d].hi * Decimal("1e-106")))
                                           for d, c in ((2, c2), (3, c3))))
    checks["CLOSED_FORM_D5"] = bool(c5.intersects(c5_closed))
    checks["TRUNCATION_NESTING"] = bool(D4_coarse.intersects(D4) and D4_coarse.width() >= D4.width())
    checks["MONOTONE"] = bool(Iv.frac(Fr(4, 3)).hi < D2.lo < D2.hi < D3.lo < D3.hi < D4.lo
                              and c2.lo > c3.hi > c3.lo > c4.hi > c4.lo > c5.hi and c5.lo > 0)
    checks["IMAGE_BOUND"] = bool(Decimal("7e-111") < E5.lo and E5.hi < Decimal("8e-111"))
    # proving direction (v1.1, Codex 4148778791): 19 eps <= delta <= 21 eps for every represented value; the enclosures of
    # delta and 20 eps intersect (delta - 20 eps ~ 200 eps^2 is far below the interval resolution, so it is recorded, not certified)
    checks["TRANSFER_BOUND"] = bool(delta.lo >= CC.multiply(Decimal(19), eps.hi) and delta.hi <= CF.multiply(Decimal(21), eps.lo)
                                    and delta.hi >= CF.multiply(Decimal(20), eps.lo) and delta.lo <= CC.multiply(Decimal(20), eps.hi)
                                    and c5_torus.contains(c5))
    checks["LIBRARY_EXACT"] = bool(library_exact())
    pinned = {"D_4": D4, "c_5_ref": c5, "pi": PI}
    checks["PINNED"] = bool(all(str(pinned[k].lo).startswith(p) and str(pinned[k].hi).startswith(p) for k, p in PINNED.items()))
    if len(checks) != 13:
        raise ValueError("rule count changed")
    passed = all(checks.values())

    out = {
        "object": "CL-SIDE24-D5-COEFFICIENT-20260930-v1",
        "scientific_effect": "NONE",
        "certified": True,
        "mutant": MUT,
        "passed": passed,
        "checks": checks,
        "cone_moments": {"D_2": D2.pair(), "D_2_exact_29/6-sqrt6": D2_exact.pair(), "D_3": D3.pair(), "D_3_Math-199": list(D3_PIN),
                         "D_4": D4.pair(), "D_4_coarse": D4_coarse.pair()},
        "coefficients": {"c_2_ref": c2.pair(), "c_3_ref": c3.pair(), "c_4_ref": c4.pair(), "c_5_ref": c5.pair(),
                         "c_5_ref_closed": c5_closed.pair(), "c_5_24": c5_torus.pair()},
        "transfer": {"E_5": E5.pair(), "epsilon": eps.pair(), "delta": delta.pair(), "n_jet": n_jet,
                     "exponents": {"a": "29/3 (<= 10 used)", "b": 10}},
        "constants": {"pi": PI.pair(), "Gamma(7/6)": GAMMA76.pair(), "(3/2)^(1/3)": CBRT32.pair(),
                      "Z_4": mehta_Z(4).pair(), "Z_4_quadrature": Z4.pair(), "1536pi": (1536 * PI).pair(),
                      "|S^4|": sphere_area(5).pair()},
        "quadrature": {"K": K_ORDER, "cells": "width 1/2 on [0, 30], width 1 on [30, 60]", "rho": str(RHO)},
        "float_reference_10sig": {"D_2_orthant": "%.10g" % f2, "D_3_orthant": "%.10g" % f3, "D_4_orthant": "%.10g" % f4,
                                  "D_4_a_integrated_3D": "%.10g" % f4a},
        "exact_relations": {
            "D_m": "sqrt(3/(m+3)) Z_m^-1 int_{mu<0} prod mu_i^2 |Delta(mu)| exp(-|mu|^2/4 + (sum mu)^2/(4(m+3))) dmu",
            "decoupling": "alpha = 3m/(4(m+3)), beta = 3T/(2(m+3)); erfc branch exp(-T^2/(4m(m-1)) - |u|^2/4), polynomial branch exp(-T^2/((m-1)(m+3)) - |u|^2/4), u = t - (T/(m-1)) 1",
            "m=4": "p1 = (T - 2 p2 - p3)/3, v = 2 p2 + p3, p2 = (v - p3)/2; |u|^2/4 = v^2/24 + p3^2/8; dp1 dp2 dp3 = dT dv dp3/6; region 0 < p3 < v < T",
            "erfc argument": "beta/(2 sqrt alpha) = T sqrt21/28; erfc(x) <= e^{-x^2} in the tail",
            "L_a": "L_a(T) = int_0^T e^{-v^2/24} sum_k e_{a,k}(v) J_k(v) dv, accumulated cell by cell",
            "D_4": "sqrt(3/7) . 24/Z_4 . (1/6) I_4",
            "Z_4": "4! sqrt pi (1/6) int dT e^{-T^2/48} int_0^T dv e^{-v^2/24} int_0^v V e^{-p3^2/8} dp3 = 1536 pi",
            "c_d_ref": "Gamma(7/6) (3/2)^(1/3) |S^{d-1}| D_{d-1} / (sqrt3 sqrt pi (2 pi)^d); d = 5: Gamma(7/6) (3/2)^(1/3) D_4 / (12 sqrt3 pi^(7/2))",
            "transfer": "E_5 = 60500 (76 24^6 + 15) e^-288; eps = 126 E_5; c_{5,24}/c_{5,ref} in [1/(1+delta), 1+delta], delta = (1+eps)^10/(1-eps)^10 - 1",
        },
    }
    sys.stdout.write(json.dumps(out, indent=1) + "\n")
    sys.stderr.write("seconds %.1f\n" % (time.time() - t0))
    sys.exit(0 if passed else 1)


def library_exact():
    ok = True
    for q in (Fr(3), Fr(120), Fr(1, 2), Fr(288), Fr(5, 7), Fr(48) - Fr(51035039649098175696, 10 ** 29)):
        g = -q / 64
        parts, term, ssum = [], Fr(1), Fr(0)
        for k in range(0, 60):
            ssum += term
            parts.append(ssum)
            term = term * g / (k + 1)
        lo, hi = min(parts[-1], parts[-2]), max(parts[-1], parts[-2])
        exact = Iv(Iv.frac(lo ** 64).lo, Iv.frac(hi ** 64).hi)
        X = Iv.frac(q)
        got = (-X).exp()
        ok &= got.intersects(exact) and CC.divide(got.width(), got.lo) < Decimal(10) ** (-PREC + 3)
        r = root_frac(q, 2)
        ok &= X.sqrt().intersects(r) and CC.divide(X.sqrt().width(), r.lo) < Decimal(10) ** (-PREC + 3)
        ok &= (-X).lo == X.hi.copy_negate() and (-X).hi == X.lo.copy_negate()
    return ok




if __name__ == "__main__":
    main()
