"""The SIDE24 cone moment D_3 in closed form: D_3 = 50/3 - 76/(3 pi) - (200/(9 pi)) arctan(1/2) = (50 pi + 200 arctan 2 - 228)/(9 pi).

Standard library only. Run from anywhere:  python -B -S closed_form_d3.py [--mutant NAME]

Object.  Math-#199 (coefficients/side24_d4_20260930) reduces the d = 4 cone moment D_3 = E[det(A)^2 1{A < 0}] of SIDE24's
reference law A = Q + sqrt(2/3) Z I_3 to the one-dimensional integral

    D_3 = (1/(32 pi)) [ sqrt(2 pi/3) int_0^inf e^{-s^2/24} erfc(s/(2 sqrt6)) sum_k e_k(s) J_k(s) ds
                        + int_0^inf e^{-s^2/12} sum_k r_k(s) J_k(s) ds ],      J_k(s) = int_0^s q^k e^{-q^2/8} dq,

with rational polynomials e_k, r_k produced by exact algebra from the ordered-sector integrand (the same code as #199), and
encloses it by certified quadrature.  Here the same integral is evaluated exactly.  Only odd k occur, so every J_k is
B_k + C_k(s) e^{-s^2/8} with a rational constant B_k and a rational polynomial C_k (no erf inside J_k), and every term of
D_3 is a moment  M_n(lam, f) = int_0^inf s^n e^{-lam s^2} f(s) ds  with f = 1 or f = erf(kappa s), kappa = 1/(2 sqrt6),
lam in {1/24, 1/12, 1/6, 5/24} (erfc = 1 - erf).  These are elementary:

    M_0(lam, 1) = (1/2) sqrt(pi/lam),   M_1(lam, 1) = 1/(2 lam),   M_0(lam, erf(kappa .)) = arctan(kappa/sqrt lam)/sqrt(pi lam),
    M_n(lam, f) = [ (n-1) M_{n-2}(lam, f) + (2 kappa/sqrt pi) M_{n-1}(lam + kappa^2, 1) ] / (2 lam)     (n >= 1, by parts),

and the arguments that occur are kappa/sqrt lam = 1 (lam = 1/24, arctan = pi/4) and 1/2 (lam = 1/6).  The computation is
carried out in exact arithmetic on the Q-span of  sqrt(r) pi^(k/2) A  (r squarefree, k an integer, A = 1 or an arctan atom),
so the output is an identity, not an approximation.  The same code gives D_1 = 4/3 and D_2 = 29/6 - sqrt6 exactly (rules),
and the interval evaluation of the closed form lies inside #199's certified enclosure of D_3 (47 common digits; rule).
Consequently c_{4,ref} = Gamma(7/6) (3/2)^(1/3) (50 pi + 200 arctan 2 - 228) / (72 sqrt3 pi^(7/2)).  Scientific effect NONE.
"""
import argparse
import json
import math
import sys
import time
from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN, setcontext
from fractions import Fraction as Fr
from functools import lru_cache

MUTANTS = ("shift-variance", "vandermonde", "erfc-sign", "jacobian", "mehta", "by-parts", "one-erf", "jk-init",
           "gauss-half", "boundary-term", "atom-pi")
MUT = None

PREC = 60
CF = Context(prec=PREC, rounding=ROUND_FLOOR, Emin=-9999999, Emax=9999999)
CC = Context(prec=PREC, rounding=ROUND_CEILING, Emin=-9999999, Emax=9999999)
CE = Context(prec=PREC, rounding=ROUND_HALF_EVEN, Emin=-9999999, Emax=9999999)
setcontext(Context(prec=2 * PREC + 20, rounding=ROUND_HALF_EVEN, Emin=-9999999, Emax=9999999))
ZERO, ONE, HALF = Decimal(0), Decimal(1), Decimal("0.5")
ROOT_DIGITS = 70

# Math-#199 v1.1 (coefficients/side24_d4_20260930/RESULTS.json at 4fc6d15): the certified enclosures this closed form must meet
CERTIFIED = {
    "D_3": ("5.32318026888989689492319873968726063578438852940845576405060", "5.32318026888989689492319873968726063578438852947338433618854"),
    "c_4_ref": ("0.0233216660029528350945211949528568851531013723630981034059901", "0.0233216660029528350945211949528568851531013723633825654059788"),
}
PINNED = {"D_3": "5.323180268889896894923198739687260635784388529",
          "c_4_ref": "0.023321666002952835094521194952856885153101372363",
          "pi": "3.14159265358979323846264338327950288419716939937510"}
CLOSED_FORM = {"1": Fr(50, 3), "1/pi": Fr(-76, 3), "arctan(1/2)/pi": Fr(-200, 9)}


# ---------------- interval arithmetic over decimal (the #199 toolkit, unchanged)
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
SQRT3 = Iv.frac(3).sqrt()
TINY = Decimal(10) ** (-PREC - 8)


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


def atan_iv(a, N=90):
    """arctan(a) for an interval 0 <= a <= 1: halve the argument, then the alternating series bracketed by consecutive
    partial sums (for each fixed argument the terms decrease, so the value lies between them)."""
    if a.lo < 0 or a.hi > 1:
        raise ValueError("atan_iv needs 0 <= a <= 1")
    a1 = a / (1 + (1 + a.sq()).sqrt())
    a1sq, p, S, prev = a1.sq(), a1, Iv(ZERO), None
    for n in range(N + 1):
        t = p / (2 * n + 1)
        prev = S
        S = S + t if n % 2 == 0 else S - t
        p = p * a1sq
    return 2 * hull(prev, S)


# ---------------- exact arithmetic: surds, and the Q-span of sqrt(r) pi^(k/2) ATOM
def sqf(n):
    """n a positive integer -> (k, r) with sqrt(n) = k sqrt(r), r squarefree."""
    k, r, p, m = 1, 1, 2, n
    while p * p <= m:
        while m % (p * p) == 0:
            m //= p * p
            k *= p
        if m % p == 0:
            m //= p
            r *= p
        p += 1
    return k, r * m


def surd_mul(u, v):
    """(c1, r1) (c2, r2) with (c, r) = c sqrt r."""
    k, r = sqf(u[1] * v[1])
    return (u[0] * v[0] * k, r)


def surd_sqrt(q):
    """sqrt of a positive rational as a surd."""
    q = Fr(q)
    if q <= 0:
        raise ValueError("sqrt of a nonpositive rational")
    k, r = sqf(q.numerator * q.denominator)
    return (Fr(k, q.denominator), r)


def surd_inv(u):
    return (1 / (u[0] * u[1]), u[1])


def surd_sq(u):
    return u[0] * u[0] * u[1]


ATOMS = [None]                      # index 0 is the number 1; index i > 0 is arctan(c sqrt r) for ATOMS[i] = (c, r), c sqrt r <= 1


def E(c=1, r=1, twok=0, atom=0):
    """The element c sqrt(r) pi^(twok/2) ATOMS[atom]."""
    return {(r, twok, atom): Fr(c)} if c != 0 else {}


def add(u, v):
    w = dict(u)
    for k, c in v.items():
        w[k] = w.get(k, Fr(0)) + c
    return {k: c for k, c in w.items() if c != 0}


def scale(u, c):
    c = Fr(c)
    return {k: v * c for k, v in u.items() if v * c != 0}


def mul_surd(u, s):
    out = {}
    for (r, twok, atom), c in u.items():
        k, r2 = sqf(r * s[1])
        key = (r2, twok, atom)
        out[key] = out.get(key, Fr(0)) + c * s[0] * k
    return {k: c for k, c in out.items() if c != 0}


def mul_pi_half(u, j):
    """multiply by pi^(j/2)."""
    return {(r, twok + j, atom): c for (r, twok, atom), c in u.items()}


def mul(u, v):
    out = {}
    for (r1, k1, a1), c1 in u.items():
        for (r2, k2, a2), c2 in v.items():
            if a1 and a2:
                raise ValueError("product of two arctan atoms is outside the span")
            k, r = sqf(r1 * r2)
            key = (r, k1 + k2, a1 or a2)
            out[key] = out.get(key, Fr(0)) + c1 * c2 * k
    return {k: c for k, c in out.items() if c != 0}


def inv_monomial(u):
    (r, twok, atom), c = next(iter(u.items()))
    if len(u) != 1 or atom:
        raise ValueError("only monomials without atoms are inverted")
    return E(1 / (c * r), r, -twok)


def atan_elem(t):
    """arctan(c sqrt r) as an element: rational multiples of pi are recognised (arguments 1, sqrt3, 1/sqrt3), an argument
    above 1 is reflected (arctan t = pi/2 - arctan(1/t)), anything else becomes an atom with argument in (0, 1]."""
    c, r = t
    if c == 0:
        return {}
    if c < 0:
        return scale(atan_elem((-c, r)), -1)
    if surd_sq(t) > 1:
        return add(E(Fr(1, 2), 1, 2), scale(atan_elem(surd_inv(t)), -1))
    if (c, r) == (1, 1):
        return E(Fr(1, 4) if MUT != "atom-pi" else Fr(1, 3), 1, 2)
    if r == 3 and c == Fr(1, 3):
        return E(Fr(1, 6), 1, 2)
    for i, a in enumerate(ATOMS):
        if a == (c, r):
            return E(1, 1, 0, i)
    ATOMS.append((c, r))
    return E(1, 1, 0, len(ATOMS) - 1)


def iv_eval(u):
    """Interval evaluation of an element (60 digits)."""
    total = Iv(ZERO)
    for (r, twok, atom), c in u.items():
        term = Iv.frac(c)
        if r != 1:
            term = term * root_frac(Fr(r), 2)
        if twok:
            pp = ipow(PI, abs(twok) // 2) * (SQRTPI if twok % 2 else Iv(ONE))
            term = term * pp if twok > 0 else term / pp
        if atom:
            ca, ra = ATOMS[atom]
            arg = Iv.frac(ca) * (root_frac(Fr(ra), 2) if ra != 1 else Iv(ONE))
            term = term * atan_iv(arg)
        total = total + term
    return total


def fl_eval(u):
    """Float evaluation of an element (controls only)."""
    v = 0.0
    for (r, twok, atom), c in u.items():
        t = float(c) * math.sqrt(r) * math.pi ** (twok / 2)
        if atom:
            ca, ra = ATOMS[atom]
            t *= math.atan(float(ca) * math.sqrt(ra))
        v += t
    return v


def show(u):
    parts = []
    for (r, twok, atom) in sorted(u, key=lambda k: (k[2], -k[1], k[0])):
        c = u[(r, twok, atom)]
        s = str(c)
        if r != 1:
            s += " sqrt(%d)" % r
        if twok:
            s += " pi^(%s)" % Fr(twok, 2)
        if atom:
            ca, ra = ATOMS[atom]
            s += " arctan(%s%s)" % (ca, "" if ra == 1 else " sqrt(%d)" % ra)
        parts.append(s)
    return "  +  ".join(parts) if parts else "0"


# ---------------- the moments  M(n, lam, slopes) = int_0^inf s^n e^{-lam s^2} prod_u erf(u s) ds
@lru_cache(maxsize=None)
def M(n, lam, slopes):
    lam = Fr(lam)
    if n == 0:
        inv_sqrt_lam = surd_sqrt(1 / lam)
        if not slopes:                                                             # (1/2) sqrt(pi/lam)
            return mul_pi_half(mul_surd(E(Fr(1, 2) if MUT != "gauss-half" else Fr(1)), inv_sqrt_lam), 1)
        if len(slopes) == 1:                                                       # arctan(u/sqrt lam)/sqrt(pi lam)
            u = slopes[0]
            t = surd_mul(u, inv_sqrt_lam) if MUT != "one-erf" else (u[0] / lam, u[1])
            return mul_pi_half(mul_surd(atan_elem(t), inv_sqrt_lam), -1)
        if len(slopes) == 2:                                                       # arctan(uv/sqrt(lam(lam+u^2+v^2)))/sqrt(pi lam)
            u, v = slopes
            den = surd_sqrt(lam * (lam + surd_sq(u) + surd_sq(v)))
            t = surd_mul(surd_mul(u, v), surd_inv(den))
            return mul_pi_half(mul_surd(atan_elem(t), inv_sqrt_lam), -1)
        raise ValueError("at most two erf factors")
    if n == 1 and not slopes:
        return E(1 / (2 * lam) if MUT != "boundary-term" else 1 / lam)
    # by parts: s^n e^{-lam s^2} f = s^{n-1} f . s e^{-lam s^2};  the boundary term vanishes (n >= 2, or f(0) = 0)
    out = {}
    if n >= 2:
        out = add(out, scale(M(n - 2, lam, slopes), n - 1 if MUT != "by-parts" else n))
    for i, u in enumerate(slopes):
        rest = slopes[:i] + slopes[i + 1:]
        term = M(n - 1, lam + surd_sq(u), rest)                                   # f' contributes (2u/sqrt pi) e^{-u^2 s^2}
        out = add(out, mul_pi_half(mul_surd(term, (2 * u[0], u[1])), -1))
    return scale(out, 1 / (2 * lam))


def gauss_moment_closed(n, lam):
    """(1/2) Gamma((n+1)/2) lam^{-(n+1)/2} as an element (the direct closed form, used only by rule GAUSS_MOMENTS)."""
    lam = Fr(lam)
    g = gamma_half(n + 1)
    if (n + 1) % 2 == 0:
        return scale(mul(g, E(Fr(1) / lam ** ((n + 1) // 2))), Fr(1, 2))
    return scale(mul_surd(mul(g, E(Fr(1) / lam ** (n // 2))), surd_sqrt(1 / lam)), Fr(1, 2))


# ---------------- exact polynomial algebra and the sector reduction (as in #199)
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
    out = {}
    for k, c in u.items():
        term = pconst(c, nvars_out)
        for i, e in enumerate(k):
            if e:
                term = pmul(term, ppow(images[i], e, nvars_out))
        out = padd(out, term)
    return out


def univariate(u):
    if not u:
        return [Fr(0)]
    deg = max(k[0] for k in u)
    return [u.get((n,), Fr(0)) for n in range(deg + 1)]


def reduce_sector(m):
    """Ordered sector mu_m = -a, mu_{m-1} = -a - p_1, ...: (prod mu_i^2 prod_{i<j} (mu_j - mu_i), |mu|^2/4 - S^2/(4(m+3)))."""
    nv = m
    a = pvar(0, nv)
    mus, acc = [], a
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
                poly = pmul(poly, padd(mus[i], pscale(mus[j], Fr(-1))))
    S, norm2 = {}, {}
    for mu in mus:
        S = padd(S, mu)
        norm2 = padd(norm2, pmul(mu, mu))
    shift = Fr(1, 4 * (m + 3)) if MUT != "shift-variance" or m != 3 else Fr(1, 20)
    quad = padd(pscale(norm2, Fr(1, 4)), pscale(pmul(S, S), -shift))
    return poly, quad


def a_integrated_terms(m):
    """Exact a-integral: erfc branch PE (times G_0) and polynomial branch PR, with exponents expE and rest."""
    poly, quad = reduce_sector(m)
    nv = m
    alpha = quad.get((2,) + (0,) * (nv - 1), Fr(0))
    beta = {k[1:]: c for k, c in quad.items() if k[0] == 1}
    rest = {k[1:]: c for k, c in quad.items() if k[0] == 0}
    nvr = nv - 1
    P = [pconst(1, nvr), pscale(beta, Fr(-1, 2) / alpha)]
    R = [{}, pconst(Fr(1, 2) / alpha, nvr)]
    deg_a = max(k[0] for k in poly)
    for n in range(1, deg_a):
        P.append(pscale(padd(pscale(P[n - 1], Fr(n)), pscale(pmul(beta, P[n]), Fr(-1))), Fr(1, 2) / alpha))
        R.append(pscale(padd(pscale(R[n - 1], Fr(n)), pscale(pmul(beta, R[n]), Fr(-1))), Fr(1, 2) / alpha))
    PE, PR = {}, {}
    for k, c in poly.items():
        n = k[0]
        w = {k[1:]: c}
        PE = padd(PE, pmul(w, P[n]))
        PR = padd(PR, pmul(w, R[n]))
    expE = padd(rest, pscale(pmul(beta, beta), Fr(-1, 4) / alpha))
    return alpha, beta, PE, PR, expE, rest


def gamma_half(twice):
    """Gamma(twice/2) as an element."""
    if twice % 2 == 0:
        return E(math.factorial(twice // 2 - 1))
    k = (twice - 1) // 2
    return E(Fr(math.factorial(2 * k), 4 ** k * math.factorial(k)), 1, 1)


def mehta_Z(m):
    """Z_m = 2^(m/2 + m(m-1)/4) (2 pi)^(m/2) prod_{j<=m} Gamma(1 + j/2) / Gamma(3/2)^m as an element."""
    m_eff = m + 1 if (MUT == "mehta" and m == 3) else m
    prod = E(1)
    for j in range(1, m_eff + 1):
        prod = mul(prod, gamma_half(j + 2))
    pw = Fr(m_eff, 2) + Fr(m_eff * (m_eff - 1), 4)
    two_pow = E(2 ** int(pw), 2 if pw.denominator == 2 else 1)
    twopi_pow = mul_pi_half(E(2 ** (m_eff // 2), 2 if m_eff % 2 else 1), m_eff)
    g = E(1)
    for _ in range(m_eff):
        g = mul(g, gamma_half(3))
    return mul(mul(mul(two_pow, twopi_pow), prod), inv_monomial(g))


def prefactor(m, jac):
    """sqrt(3/(m+3)) m! / Z_m times the Jacobian of the final substitution."""
    return mul_surd(scale(inv_monomial(mehta_Z(m)), math.factorial(m) * jac), surd_sqrt(Fr(3, m + 3)))


def jk_exact(kmax):
    """J_k(s) = A_k sqrt(2 pi) erf(s/(2 sqrt2)) + B_k + C_k(s) e^{-s^2/8}: (A_k, B_k, C_k by power) from J_0, J_1 and
    J_{k+2} = -4 s^{k+1} e^{-s^2/8} + 4(k+1) J_k."""
    J = [(Fr(1), Fr(0), []), (Fr(0), Fr(4), [Fr(-4)])]
    if MUT == "jk-init":
        J[1] = (Fr(0), Fr(2), [Fr(-2)])
    for k in range(kmax - 1):
        A, B, C = J[k]
        Cn = [4 * (k + 1) * c for c in C] + [Fr(0)] * max(0, k + 2 - len(C))
        Cn[k + 1] += Fr(-4)
        J.append((4 * (k + 1) * A, 4 * (k + 1) * B, Cn))
    return J


def jk_identities(JK):
    """J_k(0) = 0,  J_k'(s) = s^k e^{-s^2/8}  (A_k + C_k' - (s/4) C_k = s^k),  J_k(inf) = (1/2) 8^{(k+1)/2} Gamma((k+1)/2)."""
    ok = True
    for k, (A, B, C) in enumerate(JK):
        ok &= B + (C[0] if C else 0) == 0
        deriv = {}
        for i, c in enumerate(C):
            if i:
                deriv[i - 1] = deriv.get(i - 1, Fr(0)) + i * c
            deriv[i + 1] = deriv.get(i + 1, Fr(0)) - c / 4
        deriv[0] = deriv.get(0, Fr(0)) + A
        ok &= {i: c for i, c in deriv.items() if c} == {k: Fr(1)}
        at_inf = add(mul_pi_half(E(A, 2), 1), E(B))
        eight = E(8 ** ((k + 1) // 2), 2 if (k + 1) % 2 else 1)
        if (k + 1) % 2:
            eight = scale(eight, 2)                                    # 8^(1/2) = 2 sqrt2
        ok &= at_inf == scale(mul(eight, gamma_half(k + 1)), Fr(1, 2))
    return ok


# ---------------- D_1, D_2, D_3 exactly
def D1_exact():
    """D_1 = (sqrt3/2) (1/(2 sqrt pi)) int_0^inf mu^2 e^{-3 mu^2/16} dmu."""
    return mul_pi_half(mul_surd(scale(M(2, Fr(3, 16), ()), Fr(1, 4)), (Fr(1), 3)), -1)


def erfc_moment(n, lam, kappa):
    """int_0^inf s^n e^{-lam s^2} erfc(kappa s) ds = M_n(lam, 1) - M_n(lam, erf(kappa .))."""
    sign = -1 if MUT != "erfc-sign" else 1
    return add(M(n, lam, ()), scale(M(n, lam, (kappa,)), sign))


def D2_exact():
    """m = 2: one remaining variable p; erfc branch e^{-p^2/8} erfc(p sqrt30/20), polynomial branch e^{-p^2/5}."""
    alpha, beta, PE, PR, expE, rest = a_integrated_terms(2)
    if set(expE) - {(2,)} or set(rest) - {(2,)} or set(beta) - {(1,)}:
        raise ValueError("m = 2 structure")
    gE, gR, b1 = expE[(2,)], rest[(2,)], beta[(1,)]
    kappa = surd_mul((b1 / 2, 1), surd_sqrt(1 / alpha))
    constE = mul_pi_half(mul_surd(E(Fr(1, 2)), surd_sqrt(1 / alpha)), 1)          # (1/2) sqrt(pi/alpha)
    eb, rb = {}, {}
    for n, c in enumerate(univariate(PE)):
        eb = add(eb, scale(erfc_moment(n, gE, kappa), c))
    for n, c in enumerate(univariate(PR)):
        rb = add(rb, scale(M(n, gR, ()), c))
    return mul(prefactor(2, 1), add(mul(constE, eb), rb)), {"kappa": kappa, "lambda_erfc": gE, "lambda_poly": gR}


def D3_exact():
    """m = 3: p = (s - q)/2 (Jacobian 1/2), q over (0, s) through J_k, then the s-moments exactly."""
    alpha, beta, PE, PR, expE, rest = a_integrated_terms(3)
    s, q = pvar(0, 2), pvar(1, 2)
    images = [pscale(padd(s, pscale(q, Fr(-1))), Fr(1, 2)), q]
    PEs, PRs = psubst(PE, images, 2), psubst(PR, images, 2)
    eE, eR, bs = psubst(expE, images, 2), psubst(rest, images, 2), psubst(beta, images, 2)
    if set(eE) != {(2, 0), (0, 2)} or set(eR) != {(2, 0), (0, 2)} or eE[(0, 2)] != Fr(1, 8) or eR[(0, 2)] != Fr(1, 8) or set(bs) != {(1, 0)}:
        raise ValueError("decoupling failed: " + repr((eE, eR, bs)))
    gE, gR = eE[(2, 0)], eR[(2, 0)]
    kappa = surd_mul((bs[(1, 0)] / 2, 1), surd_sqrt(1 / alpha))
    b = (Fr(1, 4), 2)                                                              # 1/(2 sqrt2), the erf slope inside J_even
    constE = mul_pi_half(mul_surd(E(Fr(1, 2)), surd_sqrt(1 / alpha)), 1)

    def by_q_power(Pxy):
        out = {}
        for (i, j), c in Pxy.items():
            out.setdefault(j, {})[(i,)] = c
        return out
    qE, qR = by_q_power(PEs), by_q_power(PRs)
    kmax = max(max(qE), max(qR))
    JK = jk_exact(kmax)
    sqrt2pi = mul_pi_half(E(1, 2), 1)
    polys = {"e": {k: univariate(v) for k, v in sorted(qE.items())}, "r": {k: univariate(v) for k, v in sorted(qR.items())}}

    def branch(Pq, lam, erfc):
        tot = {}
        for k, coef_poly in sorted(Pq.items()):
            A, B, C = JK[k]
            for j, c in enumerate(univariate(coef_poly)):
                if c == 0:
                    continue
                term = {}
                if A:                                                             # A_k sqrt(2 pi) erf(s/(2 sqrt2))
                    x = M(j, lam, (b,))
                    if erfc:
                        x = add(x, scale(M(j, lam, (kappa, b)), -1 if MUT != "erfc-sign" else 1))
                    term = add(term, scale(mul(sqrt2pi, x), A))
                if B:                                                             # the constant B_k
                    term = add(term, scale(erfc_moment(j, lam, kappa) if erfc else M(j, lam, ()), B))
                for i, ci in enumerate(C):                                        # C_k(s) e^{-s^2/8}
                    if ci:
                        term = add(term, scale(erfc_moment(j + i, lam + Fr(1, 8), kappa) if erfc else M(j + i, lam + Fr(1, 8), ()), ci))
                tot = add(tot, scale(term, c))
        return tot
    jac = Fr(1, 2) if MUT != "jacobian" else Fr(1)
    pref = prefactor(3, jac)
    eb = mul(mul(pref, constE), branch(qE, gE, True))
    rb = mul(pref, branch(qR, gR, False))
    info = {"alpha": alpha, "kappa": kappa, "lambda_erfc": gE, "lambda_poly": gR, "kmax": kmax,
            "q_powers_erfc": sorted(qE), "q_powers_poly": sorted(qR), "polys": polys, "JK": JK,
            "erfc_branch": eb, "poly_branch": rb, "prefactor": pref, "constE": constE}
    return add(eb, rb), info


# ---------------- float controls (not part of the certificate)
def simpson(f, a, b, n=4000):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


def float_moment(n, lam, slopes):
    lam = float(lam)
    us = [float(c) * math.sqrt(r) for c, r in slopes]
    T = math.sqrt(140 / lam)
    def f(s):
        v = s ** n * math.exp(-lam * s * s)
        for u in us:
            v *= math.erf(u * s)
        return v
    return simpson(f, 0.0, T, 20000)


# ---------------- main
def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    args = ap.parse_args()
    MUT = args.mutant
    t0 = time.time()
    checks = {}

    d1 = D1_exact()
    d2, info2 = D2_exact()
    d3, info3 = D3_exact()
    atoms_used = list(ATOMS)                                   # the atoms created by the derivation itself (controls below may add more)
    D2_target = add(E(Fr(29, 6)), E(-1, 6))
    D3_target = add(add(E(CLOSED_FORM["1"]), E(CLOSED_FORM["1/pi"], 1, -2)),
                    mul_pi_half(scale(atan_elem((Fr(1, 2), 1)), CLOSED_FORM["arctan(1/2)/pi"]), -2))

    # STRUCTURE: the decoupled exponents (checked inside D3_exact), erfc slope kappa = 1/(2 sqrt6), only odd q-powers, arguments 1 and 1/2
    checks["STRUCTURE"] = bool(info3["kappa"] == (Fr(1, 12), 6) and info3["lambda_erfc"] == Fr(1, 24) and info3["lambda_poly"] == Fr(1, 12)
                               and all(k % 2 == 1 for k in info3["q_powers_erfc"] + info3["q_powers_poly"]) and info3["kmax"] == 7
                               and atoms_used[-1] == (Fr(1, 2), 1) and len(atoms_used) == 3)
    # GAUSS_MOMENTS: the by-parts recurrence at f = 1 reproduces (1/2) Gamma((n+1)/2) lam^{-(n+1)/2} exactly
    lams = (Fr(1, 24), Fr(1, 12), Fr(1, 6), Fr(5, 24), Fr(1, 8), Fr(1, 5), Fr(3, 16))
    checks["GAUSS_MOMENTS"] = bool(all(M(n, lam, ()) == gauss_moment_closed(n, lam) for n in range(13) for lam in lams))
    checks["JK_EXACT"] = bool(jk_identities(info3["JK"]))
    checks["D1_EXACT"] = bool(d1 == E(Fr(4, 3)))
    checks["D2_EXACT"] = bool(d2 == D2_target)
    checks["D3_FORM"] = bool(d3 == D3_target)
    # float controls of the base integrals and of sampled moments (Simpson on [0, sqrt(140/lam)]; erf from math)
    b1 = [(Fr(1, 24), (Fr(1, 12), 6)), (Fr(1, 6), (Fr(1, 12), 6)), (Fr(1, 8), (Fr(1, 20), 30)), (Fr(1, 7), (Fr(2, 3), 1))]
    ok = True
    for lam, u in b1:
        got = float_moment(0, lam, (u,))
        want = math.atan(float(u[0]) * math.sqrt(u[1]) / math.sqrt(lam)) / math.sqrt(math.pi * lam)
        ok &= abs(got - want) < 1e-9
    for lam, u, v in ((Fr(1, 24), (Fr(1, 12), 6), (Fr(1, 4), 2)), (Fr(1, 3), (Fr(1, 2), 1), (Fr(1, 3), 5))):
        got = float_moment(0, lam, (u, v))
        uu, vv = float(u[0]) * math.sqrt(u[1]), float(v[0]) * math.sqrt(v[1])
        want = math.atan(uu * vv / math.sqrt(lam * (lam + uu * uu + vv * vv))) / math.sqrt(math.pi * lam)
        ok &= abs(got - want) < 1e-9
    checks["BASE_INTEGRALS_FLOAT"] = bool(ok)
    ok = True
    for n in range(7):
        for lam, slopes in ((Fr(1, 24), ((Fr(1, 12), 6),)), (Fr(1, 6), ((Fr(1, 12), 6),)), (Fr(1, 12), ()), (Fr(1, 8), ((Fr(1, 20), 30),)),
                            (Fr(1, 24), ((Fr(1, 12), 6), (Fr(1, 4), 2)))):
            ex, fl = fl_eval(M(n, lam, slopes)), float_moment(n, lam, slopes)
            ok &= abs(ex - fl) <= 1e-8 * max(1.0, abs(fl))
    checks["MOMENTS_FLOAT"] = bool(ok)
    # interval evaluation of the closed form against #199's certified enclosure
    D3_iv = iv_eval(d3)
    cert = Iv(Decimal(CERTIFIED["D_3"][0]), Decimal(CERTIFIED["D_3"][1]))
    checks["D3_INSIDE_CERTIFIED"] = bool(cert.contains(D3_iv) and D3_iv.width() < Decimal("1e-55"))
    c4 = GAMMA76 * CBRT32 * D3_iv / (8 * SQRT3 * PI * PI * SQRTPI)
    cert4 = Iv(Decimal(CERTIFIED["c_4_ref"][0]), Decimal(CERTIFIED["c_4_ref"][1]))
    checks["C4_CLOSED"] = bool(cert4.contains(c4) and c4.width() < Decimal("1e-55"))
    checks["LIBRARY_EXACT"] = bool(library_exact())
    pinned = {"D_3": D3_iv, "c_4_ref": c4, "pi": PI}
    checks["PINNED"] = bool(all(str(pinned[k].lo).startswith(p) and str(pinned[k].hi).startswith(p) for k, p in PINNED.items()))
    if len(checks) != 12:
        raise ValueError("rule count changed")
    passed = all(checks.values())

    def fr(x):
        return str(x)
    out = {
        "object": "CL-SIDE24-D3-CLOSED-FORM-20260930-v1",
        "scientific_effect": "NONE",
        "certified": True,
        "mutant": MUT,
        "passed": passed,
        "checks": checks,
        "closed_forms": {
            "D_1": show(d1),
            "D_2": show(d2),
            "D_3": show(d3),
            "D_3_equivalent": "(50 pi + 200 arctan 2 - 228) / (9 pi)  =  50/3 - 76/(3 pi) - (100/(9 pi)) arccos(3/5)",
            "c_4_ref": "Gamma(7/6) (3/2)^(1/3) (50 pi + 200 arctan 2 - 228) / (72 sqrt3 pi^(7/2))",
            "erfc_branch_of_D_3": show(info3["erfc_branch"]),
            "polynomial_branch_of_D_3": show(info3["poly_branch"]),
        },
        "interval_evaluation": {"D_3": D3_iv.pair(), "c_4_ref": c4.pair(), "arctan(1/2)": atan_iv(Iv.frac(Fr(1, 2))).pair(),
                                "pi": PI.pair(), "Gamma(7/6)": GAMMA76.pair(), "(3/2)^(1/3)": CBRT32.pair()},
        "certified_enclosures_math_199": {"D_3": list(CERTIFIED["D_3"]), "c_4_ref": list(CERTIFIED["c_4_ref"])},
        "reduction_data": {
            "m=3": {"alpha": fr(info3["alpha"]), "kappa": "%s sqrt(%d)" % info3["kappa"], "lambda_erfc": fr(info3["lambda_erfc"]),
                    "lambda_poly": fr(info3["lambda_poly"]), "prefactor": show(info3["prefactor"]), "G_0_constant": show(info3["constE"]),
                    "e_k(s) by power, erfc branch": {str(k): [fr(c) for c in v] for k, v in info3["polys"]["e"].items()},
                    "r_k(s) by power, polynomial branch": {str(k): [fr(c) for c in v] for k, v in info3["polys"]["r"].items()},
                    "J_k = A_k sqrt(2 pi) erf(s/(2 sqrt2)) + B_k + C_k(s) e^{-s^2/8}": {
                        str(k): {"A": fr(A), "B": fr(B), "C": [fr(c) for c in C]} for k, (A, B, C) in enumerate(info3["JK"])}},
            "m=2": {"kappa": "%s sqrt(%d)" % info2["kappa"], "lambda_erfc": fr(info2["lambda_erfc"]), "lambda_poly": fr(info2["lambda_poly"])},
            "atoms_created_by_the_derivation": ["1"] + ["arctan(%s sqrt(%d))" % a for a in atoms_used[1:]],
            "note": "arctan(sqrt15/5) arises in the m = 2 erfc branch (kappa = sqrt30/20 against e^{-p^2/8}) and cancels exactly in D_2",
        },
        "exact_relations": {
            "M_0(lam, 1)": "(1/2) sqrt(pi/lam)", "M_1(lam, 1)": "1/(2 lam)",
            "M_0(lam, erf(u .))": "arctan(u/sqrt lam)/sqrt(pi lam)",
            "M_0(lam, erf(u .) erf(v .))": "arctan(u v/sqrt(lam (lam + u^2 + v^2)))/sqrt(pi lam)  (present in the code; not on the path of D_3)",
            "M_n(lam, f), n >= 1": "[(n-1) M_{n-2}(lam, f) + sum_{u in f} (2u/sqrt pi) M_{n-1}(lam + u^2, f minus u)]/(2 lam)",
            "D_3 integral": "(1/(32 pi)) [sqrt(2 pi/3) int e^{-s^2/24} erfc(s/(2 sqrt6)) sum_k e_k J_k + int e^{-s^2/12} sum_k r_k J_k]",
            "arguments": "kappa/sqrt(1/24) = 1 (arctan = pi/4), kappa/sqrt(1/6) = 1/2",
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
