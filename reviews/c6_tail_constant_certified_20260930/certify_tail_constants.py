"""Certified enclosures of the planar microscopic radius-tail constants (Math-#178's table) for the parent kernel.

Standard library only. Run from anywhere:  python -B -S certify_tail_constants.py [--mutant NAME]
Every printed interval [lo, hi] is a rigorous enclosure: interval arithmetic over `decimal` with directed rounding
(exp and sqrt are correctly rounded by the decimal module and widened by two units in the last place), pi from Machin's
formula with the alternating-series bracket, log 2 and erf(1/2) from their series with explicit tails, and every
one-dimensional integral enclosed cell by cell with order-K Taylor arithmetic: the point expansion at the cell centre
supplies the even coefficients, and the K-th coefficient of the expansion over the whole cell (which contains
f^(K)(xi)/K! for every xi in the cell) supplies the remainder; beyond the truncation point T an exact Gaussian tail bound
is added. Nothing is fitted, sampled or extrapolated.

Inputs certified (from Math-#178 NOTE section 1-2 at head 48407d4, planar reduction of [R] (R12)-(R13) and [Q]):
  G0(a) = p_odd(a, a^2/(12k), a^3/(144 k^2)),  p_odd = N(0, diag(2, 2, 6)),  gamma(a) = sqrt(1 + (a/(12k))^2),  A = a/(12k)
  J_cusp = int gamma^11 G0,  T1 = int gamma^9 (1 + 12 A^2) G0,  T2 = int gamma^13 D_a G0,  Tb = int |A| gamma^10 G0,
  D_a G0 = -(a^2/24 + a^4/(3456 k^2)) G0;  all integrals over the real line (even integrands).
  p_b(0)/z_0 = phi(b/sqrt2) / (sqrt2 . 36 k^2 m_(2,b)),  m_(2,b) = (b^2 + 2) Phi(b/sqrt2) + b sqrt2 phi(b/sqrt2)
  K_0 = 108 k^7 p_b(0)/z_0;  C_0 = (216/11) k^7 [p_b(0)/z_0] J_cusp;  C_* = C_0 I;  C_2 = K_0 [U_2 T1 + (2B/13) T2];
  c = C_2/C_*;  d_TV coefficient kappa c with kappa = (2/13)(11/13)^(11/2);  B_sign = (K_0/C_*) U_abs Tb;
  G_max = C_0 (I - D),  G_2 = C_0 J,  B_2 = C_0 D,  singleton = C_0 (I - D - J);
  I = 246528/35, U_2 = 240192/35, B = -428544/7, U_abs = 5898627/880, J = 1083417/280 (exact, Math-#169/#176/#178),
  D = 27066286003/223205220 - (79298560/4782969) log 2 (Math-#169 E21).
The reductions are consumed at those records' stated scopes; this script certifies the arithmetic of the constants, not
the theorems. Scientific effect: NONE.

Twelve rules must hold (FLOAT_INSIDE, NESTING, TRUNCATION_NESTING, WIDTHS, PINNED, MONOTONE_IN_K, CONSTANTS_RIGOROUS,
TB_EXACT, T2_IDENTITY, C_BOUNDS, K_BOUNDS, LIBRARY_EXACT; README section 2) and eleven mutants must exit 1. The floating-point control enters the
pinned output only rounded to 10 significant digits, so the output is byte-identical across CPython versions. TB_EXACT and T2_IDENTITY are the exact
identities of README section 3: G_0 = exp(-12 k^2 (gamma^6 - 1)), Tb(k) = (12 k^2 + 1)/(36 k^3), T2 = -T1/12, whence
c = (66451/11128) T1/J_hat and B_sign = (4587821/876544) Tb/J_hat; C_BOUNDS is their consequence
66451/11128 < c(k) < 199353/2782 (T1/J_hat = 12 - 11 I_9/I_11 with 0 < I_9 < I_11); K_BOUNDS the all-k two-sided
bounds 2 sqrt(pi) < J_hat(k) <= 2 sqrt(pi)(1 + 1/(16k^2) + 1/(512k^4)) and their consequences for I_9, B_sign and c.
"""
import argparse
import json
import math
import sys
import time
from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN, setcontext
from fractions import Fraction as Fr
from math import comb, factorial

MUTANTS = ("gamma-power", "cusp-shift", "prefactor", "pi-truncated", "log2-truncated", "tail-dropped", "tb-power", "t2-weight",
           "t1t2-scale", "j-scale", "context-neg")
MUT = None


def T2_WEIGHT():
    """Coefficient multiplier of the a^4 term of D_a G0 (mutant t2-weight perturbs it on both evaluation paths)."""
    return Fr(1001, 1000) if MUT == "t2-weight" else Fr(1)


def T1T2_SCALE():
    """Common factor on the T1 and T2 integrands, both evaluation paths (mutant t1t2-scale halves them: T2 = -T1/12
    survives, the float control survives, only the universal bounds on c catch it)."""
    return Fr(1, 2) if MUT == "t1t2-scale" else Fr(1)


def J_SCALE():
    """Factor on the J integrand, both evaluation paths (mutant j-scale multiplies it by 101/100, which leaves the
    float control and the identities intact and is caught by the all-k bounds K_BOUNDS, as well as by PINNED)."""
    return Fr(101, 100) if MUT == "j-scale" else Fr(1)


def TB_POWER():
    """Power of gamma^2 in the Tb integrand (mutant tb-power lowers it on both evaluation paths)."""
    return 4 if MUT == "tb-power" else 5
PREC = 48
CF = Context(prec=PREC, rounding=ROUND_FLOOR, Emin=-9999999, Emax=9999999)
CC = Context(prec=PREC, rounding=ROUND_CEILING, Emin=-9999999, Emax=9999999)
CE = Context(prec=PREC, rounding=ROUND_HALF_EVEN, Emin=-9999999, Emax=9999999)
# Every arithmetic step names one of the three contexts.  Operator syntax on Decimals (unary minus, int * Decimal) rounds to
# the thread's current context, whose default precision is 28 and would silently shorten a 48-digit endpoint (v1.2 negated
# endpoints that way; repaired in v1.3).  The current context is widened as a safety net, negation is the exact copy_negate,
# and rule LIBRARY_EXACT compares exp, sqrt and the negation against exact rational brackets.
setcontext(Context(prec=2 * PREC + 20, rounding=ROUND_HALF_EVEN, Emin=-9999999, Emax=9999999))
ZERO, ONE = Decimal(0), Decimal(1)
KS = (Fr(1, 2), Fr(1), Fr(2))
BS = (Fr(0), Fr(1))
I_SHAPE, U2, BSH, UABS, JOUT = Fr(246528, 35), Fr(240192, 35), Fr(-428544, 7), Fr(5898627, 880), Fr(1083417, 280)
# exact prefactors of the two reduced formulas (README section 3): c = C_PREF . T1/J_hat,  B_sign = B_PREF . Tb/J_hat
C_PREF = Fr(11) * (U2 - BSH / 78) / (2 * I_SHAPE)
B_PREF = Fr(11) * UABS / (2 * I_SHAPE)
# universal bounds (README section 3, consequence): T1/J_hat = 12 - 11 I_9/I_11 lies strictly in (1, 12) for every k > 0
C_LOWER, C_UPPER = C_PREF, 12 * C_PREF                 # 66451/11128 < c(k) < 199353/2782
# first significant digits of the certified values (pinned by this record; PINNED check): key -> string prefix
PINNED = {
    "J_hat|1/2": "4.396080052560", "J_hat|1": "3.746141728365734", "J_hat|2": "3.594417805731787",
    "C_star|1/2|0": "1.929709931071", "C_star|1|0": "52.6211847645885", "C_star|2|0": "1615.67852743513",
    "D": "109.76995034568", "log2": "0.69314718055994530941", "pi": "3.14159265358979323846",
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
        if MUT == "context-neg":                                   # v1.2 behaviour: rounds to the current context
            return Iv(-a.hi, -a.lo)
        return Iv(a.hi.copy_negate(), a.lo.copy_negate())          # exact

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

    def mid_float(a):
        return float((a.lo + a.hi) / 2)

    def pair(a):
        return [str(a.lo), str(a.hi)]


# ---------------- rigorous constants
def pi_interval():
    def atan_inv(n, terms):
        x = Fr(1, n)
        partial, sums = Iv(ZERO), []
        for m in range(terms + 2):
            t = Iv.frac(x ** (2 * m + 1) / (2 * m + 1))
            partial = partial + t if m % 2 == 0 else partial - t
            sums.append(partial)
        a, b = sums[-1], sums[-2]                      # alternating series with decreasing terms
        return Iv(min(a.lo, b.lo), max(a.hi, b.hi))
    if MUT == "pi-truncated":
        return Iv.frac(Fr(314159, 100000))
    return atan_inv(5, 40) * 16 - atan_inv(239, 20) * 4


def log2_interval():
    # log 2 = sum_{n>=1} 1/(n 2^n); tail after N terms <= 1/((N+1) 2^N); N = 160 puts the tail below 1e-50
    N = 160 if MUT != "log2-truncated" else 8
    s = sum(Fr(1, n * 2 ** n) for n in range(1, N + 1))
    lo = Iv.frac(s)
    hi = Iv.frac(s + Fr(1, (N + 1) * 2 ** N))
    return Iv(lo.lo, hi.hi)


def erf_interval(x):
    """erf(x) for rational 0 <= x <= 1: (2/sqrt pi) sum (-1)^n x^(2n+1)/(n! (2n+1)), alternating with decreasing terms."""
    x = Fr(x)
    partial, sums = Fr(0), []
    for n in range(60):
        t = x ** (2 * n + 1) / (factorial(n) * (2 * n + 1))
        partial = partial + t if n % 2 == 0 else partial - t
        sums.append(partial)
    S = Iv(Iv.frac(min(sums[-1], sums[-2])).lo, Iv.frac(max(sums[-1], sums[-2])).hi)
    return S * 2 / pi_interval().sqrt()


def library_exact():
    """exp and sqrt of the decimal module, and the interval negation, against exact rational brackets: e^-q by the rational
    series of e^(-q/64) raised to the 64th power (alternating, bracketed by consecutive partial sums), sqrt by an integer root.
    Catches an argument shortened to the default 28-digit context (mutant context-neg) at the 1e-28 level."""
    ok = True
    for q in (Fr(48) - Fr(51035039649098175696, 10 ** 29), Fr(3), Fr(1, 2), Fr(288), Fr(5, 7), Fr(1234567, 10 ** 6)):
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
        m = 60
        r = math.isqrt(q.numerator * q.denominator * 10 ** (2 * m))
        root = Iv(Iv.frac(Fr(r, q.denominator * 10 ** m)).lo, Iv.frac(Fr(r + 1, q.denominator * 10 ** m)).hi)
        ok &= X.sqrt().intersects(root) and CC.divide(X.sqrt().width(), root.lo) < Decimal(10) ** (-PREC + 3)
        ok &= (-X).lo == X.hi.copy_negate() and (-X).hi == X.lo.copy_negate()
    return ok


# ---------------- Taylor arithmetic over intervals
def t_const(c, K):
    return [Iv.of(c)] + [Iv(ZERO)] * K


def t_var(c, K):
    s = t_const(c, K)
    s[1] = Iv(ONE)
    return s


def t_add(u, v):
    return [x + y for x, y in zip(u, v)]


def t_scale(u, c):
    return [x * c for x in u]


def t_mul(u, v):
    K = len(u) - 1
    out = []
    for k in range(K + 1):
        acc = Iv(ZERO)
        for j in range(k + 1):
            acc = acc + u[j] * v[k - j]
        out.append(acc)
    return out


def t_exp(u):
    K = len(u) - 1
    e = [u[0].exp()]
    for k in range(1, K + 1):
        acc = Iv(ZERO)
        for j in range(1, k + 1):
            acc = acc + (u[j] * j) * e[k - j]
        e.append(acc / k)
    return e


def t_sqrt(u):
    K = len(u) - 1
    s = [u[0].sqrt()]
    two_s0 = s[0] * 2
    for k in range(1, K + 1):
        acc = u[k]
        for j in range(1, k):
            acc = acc - s[j] * s[k - j]
        s.append(acc / two_s0)
    return s


def t_ipow(u, n):
    out = t_const(1, len(u) - 1)
    for _ in range(n):
        out = t_mul(out, u)
    return out


def integrand_series(name, centre, K, k):
    """Taylor series at a = centre + t of the raw (unnormalised) integrand of J_hat, T1, T2 or Tb:
    gamma^p . poly(a) . exp(-(a^2/4 + beta_0^2/4 + c_0^2/12)) with beta_0 = a^2/(12k), c_0 = a^3/(144k^2)."""
    s = Fr(1, 144 * k * k)
    a = t_var(centre, K)
    a2 = t_mul(a, a)
    a4 = t_mul(a2, a2)
    a6 = t_mul(a4, a2)
    g = t_add(t_const(1, K), t_scale(a2, s))                          # gamma^2 = 1 + s a^2
    c_term = Fr(0) if MUT == "cusp-shift" else Fr(1, 248832 * k ** 4)
    P = t_add(t_add(t_scale(a2, Fr(-1, 4)), t_scale(a4, -Fr(1, 576 * k * k))), t_scale(a6, -c_term))
    E = t_exp(P)
    root = t_sqrt(g)
    if name == "J":          # gamma^11 = g^5 sqrt(g)   (mutant gamma-power: gamma^10 = g^5)
        core = t_ipow(g, 5) if MUT == "gamma-power" else t_mul(t_ipow(g, 5), root)
        return t_scale(t_mul(core, E), J_SCALE())
    if name == "T1":         # gamma^9 (1 + 12 A^2) = g^4 sqrt(g) (1 + 12 s a^2)
        w = t_add(t_const(1, K), t_scale(a2, 12 * s))
        return t_scale(t_mul(t_mul(t_mul(t_ipow(g, 4), root), w), E), T1T2_SCALE())
    if name == "T2":         # gamma^13 . (-(a^2/24 + a^4/(3456 k^2)))
        w = t_add(t_scale(a2, Fr(-1, 24)), t_scale(a4, -Fr(1, 3456 * k * k) * T2_WEIGHT()))
        return t_scale(t_mul(t_mul(t_mul(t_ipow(g, 6), root), w), E), T1T2_SCALE())
    if name == "Tb":         # |A| gamma^10 = (a/(12k)) g^5 on a >= 0
        w = t_scale(a, Fr(1, 12 * k))
        return t_mul(t_mul(t_ipow(g, TB_POWER()), w), E)
    raise ValueError(name)


def enclose_half_line(name, k, T, cells, K):
    """int_0^T (raw integrand) as an interval, with the per-cell Taylor remainder; K even."""
    h = Fr(T, cells)
    if cells % 2 or K % 2:
        raise ValueError("cells and K must be even")
    total, max_rem, partial = Iv(ZERO), Decimal(0), None
    for i in range(cells):
        if i == cells // 2:
            partial = total                                   # int_0^{T/2}: the truncation-nesting witness
        lo, hi = h * i, h * (i + 1)
        c = (lo + hi) / 2
        r = Iv.frac(h / 2)
        p = integrand_series(name, Iv.frac(c), K, k)
        q = integrand_series(name, Iv(Iv.frac(lo).lo, Iv.frac(hi).hi), K, k)
        cell, rpow = Iv(ZERO), r
        for j in range(K):
            if j % 2 == 0:
                cell = cell + p[j] * (rpow * Fr(2, j + 1))
            rpow = rpow * r
        rem = q[K] * (rpow * Fr(2, K + 1))
        max_rem = max(max_rem, rem.width())
        total = total + cell + rem
    return total, max_rem, partial


def tail_bound(name, k, T):
    """Upper bound of int_T^inf of the raw integrand: gamma^p |poly| <= (1 + s a^2)^7 (1 + a^2)^2 in every case (T >= 1,
    a >= T: 1 + 12 s a^2 <= (1 + s a^2)(1 + a^2)... crude but rigorous), times e^{-a^2/4}; the Gaussian moments
    int_T^inf a^{2j} e^{-a^2/4} <= T^{-1} 2 4^j j! e^{-T^2/4} sum_{i<=j} (T^2/4)^i/i!."""
    if MUT == "tail-dropped":
        return Iv(ZERO)
    s = Fr(1, 144 * k * k)
    T = Fr(T)
    x = T * T / 4
    e = Iv.frac(-x).exp()
    # envelope polynomial in a^2: (1 + s a^2)^7 * (1 + a^2)^2  (covers gamma^13, (1+12A^2), |A| <= a and a^2/24 + a^4/(3456k^2) <= (1+a^2)^2)
    env = {}
    for j in range(8):
        for i in range(3):
            env[i + j] = env.get(i + j, 0) + comb(7, j) * s ** j * comb(2, i)
    tot = Iv(ZERO)
    for j, cj in env.items():
        poly = sum(x ** i / factorial(i) for i in range(j + 1))
        tot = tot + e * Iv.frac(Fr(cj) * 2 * 4 ** j * factorial(j) * poly / T)
    return Iv(ZERO, tot.hi)


def float_reference(name, k):
    """Independent floating-point estimate (96-point Gauss-Legendre on [0, 14], doubled) of the raw integral."""
    xs, ws = [], []
    n = 96
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for m in range(2, n + 1):
                p0, p1 = p1, ((2 * m - 1) * x * p1 - (m - 1) * p0) / m
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    kf = float(k)
    def raw(a):
        g = 1 + (a / (12 * kf)) ** 2
        E = math.exp(-a * a / 4 - a ** 4 / (576 * kf * kf) - a ** 6 / (248832 * kf ** 4))
        if name == "J":
            return float(J_SCALE()) * g ** 5.5 * E
        if name == "T1":
            return float(T1T2_SCALE()) * g ** 4.5 * (1 + 12 * (a / (12 * kf)) ** 2) * E
        if name == "T2":
            return -float(T1T2_SCALE()) * g ** 6.5 * (a * a / 24 + float(T2_WEIGHT()) * a ** 4 / (3456 * kf * kf)) * E
        return (a / (12 * kf)) * g ** TB_POWER() * E
    return 2 * sum(w * raw(7 * t + 7) for t, w in zip(xs, ws)) * 7


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    ap.add_argument("--T", type=int, default=16)
    ap.add_argument("--cells", type=int, default=160)
    ap.add_argument("--K", type=int, default=12)
    args = ap.parse_args()
    MUT = args.mutant
    if MUT == "context-neg":
        setcontext(Context(prec=28, rounding=ROUND_HALF_EVEN, Emin=-9999999, Emax=9999999))
    t0 = time.time()
    PI = pi_interval()
    LOG2 = log2_interval()
    SQRT2, SQRT3 = Iv.frac(2).sqrt(), Iv.frac(3).sqrt()
    NORM = 1 / (PI * PI * PI * 192).sqrt()                          # (2 pi)^(-3/2) 24^(-1/2)
    KAPPA = (Iv.frac(Fr(11, 13)).sqrt() * Iv.frac(Fr(11, 13) ** 5)) * Fr(2, 13)   # (2/13)(11/13)^(11/2)
    D_INNER = Iv.frac(Fr(27066286003, 223205220)) - LOG2 * Fr(79298560, 4782969)
    ERF_HALF = erf_interval(Fr(1, 2))
    checks = {}
    ok_float, ok_nest, ok_pinned, ok_width, ok_trunc = True, True, True, True, True
    out = {"object": "C6-TAIL-CONSTANT-CERTIFIED-20260930-v1", "precision_digits": PREC, "taylor_order": args.K,
           "truncation": args.T, "cells": args.cells, "pi": PI.pair(), "log2": LOG2.pair(), "erf_half": ERF_HALF.pair(),
           "kappa": KAPPA.pair(), "D_inner": D_INNER.pair(), "raw_integrals": {}, "constants": {}}
    raw = {}
    for k in KS:
        raw[k] = {}
        for name in ("J", "T1", "T2", "Tb"):
            half, rem, half_T2 = enclose_half_line(name, k, args.T, args.cells, args.K)
            sgn = -1 if name == "T2" else 1                      # T2's integrand is negative: the tail is subtracted
            tail_T, tail_T2 = tail_bound(name, k, args.T), tail_bound(name, k, Fr(args.T, 2))
            val = (half + tail_T * sgn) * 2
            val_T2 = (half_T2 + tail_T2 * sgn) * 2                # enclosure at truncation T/2 (same cells, same K)
            coarse_half, _, _ = enclose_half_line(name, k, args.T, max(8, args.cells // 4), max(6, args.K - 4))
            coarse = (coarse_half + tail_T * sgn) * 2
            ok_trunc &= val.lo <= val_T2.hi and val_T2.lo <= val.hi
            ref = float_reference(name, k)
            tol = abs(Decimal(repr(ref))) * Decimal("1e-11")
            ok_float &= val.lo <= Decimal(repr(ref)) + tol and val.hi >= Decimal(repr(ref)) - tol
            ok_nest &= coarse.contains(val)
            ok_width &= val.width() <= abs(Decimal(repr(ref))) * Decimal("1e-11")
            raw[k][name] = val
            out["raw_integrals"]["%s|%s" % (name, k)] = {"interval": val.pair(), "width": str(val.width()),
                                                          "float_reference_10sig": "%.10g" % ref, "max_cell_remainder_width": str(rem),
                                                          "coarse_enclosure": coarse.pair(), "tail_bound_at_T": str(tail_T.hi),
                                                          "enclosure_at_half_T": val_T2.pair()}
    # exact identities (derived in README section 3): Tb(k) = (12 k^2 + 1)/(36 k^3) and T2 = -T1/12
    ok_tb, ok_t2 = True, True
    out["exact_relations"] = {"G0": "exp(-12 k^2 (gamma^6 - 1))", "Tb": "(12 k^2 + 1)/(36 k^3)", "T2": "-T1/12",
                              "c_prefactor": str(C_PREF), "B_sign_prefactor": str(B_PREF), "per_k": {}}
    for k in KS:
        tb_exact = Fr(12 * k * k + 1, 36 * k ** 3)
        ok_tb &= raw[k]["Tb"].contains(Iv.frac(tb_exact))
        minus_t1_over_12 = raw[k]["T1"] * Fr(-1, 12)
        ok_t2 &= raw[k]["T2"].lo <= minus_t1_over_12.hi and minus_t1_over_12.lo <= raw[k]["T2"].hi
        out["exact_relations"]["per_k"][str(k)] = {"Tb_exact": str(tb_exact), "Tb_enclosure": raw[k]["Tb"].pair(),
                                                   "minus_T1_over_12": minus_t1_over_12.pair(), "T2_enclosure": raw[k]["T2"].pair()}
    # universal bounds on c = C_PREF . T1/J_hat: strict containment in (C_LOWER, C_UPPER) at every k
    ok_cb = True
    for k in KS:
        c_iv = raw[k]["T1"] * C_PREF / raw[k]["J"]
        ok_cb &= Iv.frac(C_LOWER).hi < c_iv.lo and c_iv.hi < Iv.frac(C_UPPER).lo
    out["exact_relations"]["c_bounds"] = {"lower": str(C_LOWER), "upper": str(C_UPPER),
                                          "note": "T1/J_hat = 12 - 11 I_9/I_11 with 0 < I_9 < I_11; both ends are limits (k -> inf, k -> 0)"}
    # all-k bounds (README section 3, consequence 3): with s = 4 sqrt3 k sqrt(gamma^6 - 1), J_hat = int F(gamma) e^{-s^2/4} ds
    # with 1 <= F = gamma^7 sqrt((gamma^4 + gamma^2 + 1)/3) <= gamma^9 = (1 + s^2/(48 k^2))^{3/2}; likewise I_9 with
    # 1 <= F_9 = gamma^5 sqrt(...) <= gamma^7.  Hence  2 sqrt(pi) < J_hat(k) <= 2 sqrt(pi)(1 + 1/(16k^2) + 1/(512k^4)),
    # 2 sqrt(pi) < I_9(k) <= 2 sqrt(pi)(1 + 7/(144k^2) + 7/(13824k^4)), and the derived bounds on B_sign and c.
    ok_kb = True
    two_sqrt_pi = PI.sqrt() * 2
    kb = {}
    for k in KS:
        J_iv = raw[k]["J"]
        I9_iv = (J_iv * 12 - raw[k]["T1"]) / 11
        upJ = two_sqrt_pi * (1 + Fr(1, 16 * k * k) + Fr(1, 512 * k ** 4))
        upI9 = two_sqrt_pi * (1 + Fr(7, 144 * k * k) + Fr(7, 13824 * k ** 4))
        tb = Fr(12 * k * k + 1, 36 * k ** 3)
        b_lo = Iv.frac(tb) * B_PREF / upJ
        b_hi = Iv.frac(tb) * B_PREF / two_sqrt_pi
        c_hi = (Iv.frac(12) - two_sqrt_pi * 11 / upJ) * C_PREF
        b_iv = Iv.frac(tb) * B_PREF / J_iv
        c_iv = raw[k]["T1"] * C_PREF / J_iv
        ok_kb &= two_sqrt_pi.hi < J_iv.lo and J_iv.hi < upJ.lo
        ok_kb &= two_sqrt_pi.hi < I9_iv.lo and I9_iv.hi < upI9.lo
        ok_kb &= b_lo.hi < b_iv.lo and b_iv.hi < b_hi.lo
        ok_kb &= c_iv.hi < c_hi.lo
        kb[str(k)] = {"J_hat": J_iv.pair(), "J_hat_bounds": [two_sqrt_pi.pair(), upJ.pair()], "I_9": I9_iv.pair(),
                      "I_9_bounds": [two_sqrt_pi.pair(), upI9.pair()], "B_sign": b_iv.pair(), "B_sign_bounds": [b_lo.pair(), b_hi.pair()],
                      "c": c_iv.pair(), "c_upper": c_hi.pair()}
    out["exact_relations"]["k_dependent_bounds"] = {
        "J_hat": "2 sqrt(pi) < J_hat(k) <= 2 sqrt(pi) (1 + 1/(16 k^2) + 1/(512 k^4))",
        "I_9": "2 sqrt(pi) < I_9(k) <= 2 sqrt(pi) (1 + 7/(144 k^2) + 7/(13824 k^4))",
        "B_sign": "B_PREF (12k^2+1)/(36 k^3) / upJ < B_sign(k) < B_PREF (12k^2+1)/(72 sqrt(pi) k^3)",
        "c": "c(k) <= C_PREF (12 - 11 . 2 sqrt(pi)/upJ)",
        "asymptotic_series_not_certified": {"J_hat/(2 sqrt pi)": "1 + 1/(18 k^2) + 13/(10368 k^4) - 35/(746496 k^6) + O(k^-8)",
                                            "I_9/(2 sqrt pi)": "1 + 1/(24 k^2) + 1/(10368 k^4) + 0 k^-6 + O(k^-8)",
                                            "c/C_PREF": "1 + 11/(72 k^2) + O(k^-4)"},
        "per_k": kb}
    # pinned digits
    for key, prefix in PINNED.items():
        if key.startswith("J_hat|"):
            v = raw[Fr(key.split("|")[1])]["J"]
        elif key == "D":
            v = D_INNER
        elif key == "log2":
            v = LOG2
        elif key == "pi":
            v = PI
        else:
            continue
        ok_pinned &= str(v.lo).startswith(prefix) and str(v.hi).startswith(prefix)
    # constants per (k, b)
    for k in KS:
        J, T1, T2, Tb = (raw[k][n] * NORM for n in ("J", "T1", "T2", "Tb"))
        for b in BS:
            phi_b = Iv.frac(-b * b / 4).exp() / (PI * 2).sqrt()                           # phi(b/sqrt2)
            Phi_b = (ERF_HALF + 1) / 2 if b == 1 else Iv.frac(Fr(1, 2))                    # Phi(b/sqrt2), b in {0,1}
            m2b = Phi_b * (b * b + 2) + phi_b * SQRT2 * b
            pref = phi_b / (SQRT2 * m2b * (36 * k * k))                                   # p_b(0)/z_0
            if MUT == "prefactor":
                pref = pref * Fr(385, 384)
            K0 = pref * (108 * k ** 7)
            C0 = pref * J * Fr(216 * k ** 7, 11)
            Cstar = C0 * I_SHAPE
            C2 = K0 * (T1 * U2 + T2 * Fr(2, 13) * BSH)
            c_ratio = C2 / Cstar
            Bsign = (K0 / Cstar) * Tb * UABS
            key = "k=%s,b=%s" % (k, b)
            out["constants"][key] = {
                "K0": K0.pair(), "C0_per_shape": C0.pair(), "C_star": Cstar.pair(), "C_star_width": str(Cstar.width()),
                "G_max": (C0 * (I_SHAPE - D_INNER)).pair(), "G2": (C0 * JOUT).pair(), "B2": (C0 * D_INNER).pair(),
                "singleton": (C0 * (I_SHAPE - JOUT - D_INNER)).pair(),
                "C2": C2.pair(), "c_C2_over_Cstar": c_ratio.pair(), "dTV_coefficient_kappa_c": (KAPPA * c_ratio).pair(),
                "B_sign": Bsign.pair(), "J_cusp": J.pair(), "T1": T1.pair(), "T2": T2.pair(), "Tb": Tb.pair(),
                "c_reduced": (raw[k]["T1"] * C_PREF / raw[k]["J"]).pair(),
                "B_sign_reduced": (Iv.frac(Fr(12 * k * k + 1, 36 * k ** 3)) * B_PREF / raw[k]["J"]).pair()}
            pk = "C_star|%s|%s" % (k, b)
            if pk in PINNED:
                ok_pinned &= str(Cstar.lo).startswith(PINNED[pk]) and str(Cstar.hi).startswith(PINNED[pk])
    ok_mono = raw[KS[0]]["J"].lo > raw[KS[1]]["J"].hi > raw[KS[2]]["J"].hi and raw[KS[1]]["J"].lo > raw[KS[2]]["J"].hi
    ok_pi = ok_pinned and all(v.width() < Decimal("1e-40") for v in (PI, LOG2, ERF_HALF, KAPPA, D_INNER))
    checks = {"FLOAT_INSIDE": bool(ok_float), "NESTING": bool(ok_nest), "WIDTHS": bool(ok_width), "PINNED": bool(ok_pinned),
              "MONOTONE_IN_K": bool(ok_mono), "CONSTANTS_RIGOROUS": bool(ok_pi), "TB_EXACT": bool(ok_tb), "T2_IDENTITY": bool(ok_t2),
              "TRUNCATION_NESTING": bool(ok_trunc), "C_BOUNDS": bool(ok_cb), "K_BOUNDS": bool(ok_kb),
              "LIBRARY_EXACT": bool(library_exact())}
    out["checks"] = checks
    out["passed"] = all(checks.values()) and len(checks) == 12
    print("elapsed seconds %.1f" % (time.time() - t0), file=sys.stderr)      # timing stays out of the pinned output
    out["scope"] = ("rigorous enclosures of the one-dimensional cusp integrals and of the assembled constants; the planar "
                    "reductions and the exact shape integrals are consumed at their records' scopes; not a proof of any "
                    "theorem; scientific effect NONE")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
