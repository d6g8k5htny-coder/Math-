"""Rigorous constants for CL-CU-CUSP-COEFFICIENT-20261001: Gamma at rationals, the prefactors of c1 in d = 1, 2, 3
(NOTE.md sections 2-4) and the reference leading coefficients c_(d,ref) of coefficients/side24_v1 (1).

log Gamma(y) at y = q + N >= 10 (the shift used by lgamma_iv; the bound below holds for every real y > 0) uses Stirling's series
    (y - 1/2) log y - y + log(2 pi)/2 + sum_(k=1..K) B_(2k)/(2k (2k-1) y^(2k-1)) + R_K,
    |R_K| <= |B_(2K+2)|/((2K+2)(2K+1) y^(2K+1))      (real y > 0: the remainder is bounded by the first omitted term),
and the recurrence log Gamma(q) = log Gamma(q + N) - log prod_(j<N) (q + j), the product taken exactly."""
from fractions import Fraction as Fr
from ia import dn, up, add, sub, neg, mul, div, scal, sqr, isqrt, from_frac, PI, LN2
from elem import exp_iv, log_iv, log_pt

BERN = [Fr(1, 6), Fr(-1, 30), Fr(1, 42), Fr(-1, 30), Fr(5, 66), Fr(-691, 2730), Fr(7, 6), Fr(-3617, 510),
        Fr(43867, 798), Fr(-174611, 330), Fr(854513, 138)]          # B_2, B_4, ..., B_22
TWO_PI = scal(2.0, PI)
LOG_2PI = log_iv(TWO_PI)


def _log_rat(q):
    """log of a positive rational q (exact float if possible, else its outward float hull)."""
    a = from_frac(Fr(q))
    return log_iv(a)


def lngamma(q, N=10, K=10):
    """Enclosure of log Gamma(q) for a rational q > 0 (Stirling at y = q + N >= 10; remainder below 1e-20)."""
    q = Fr(q)
    y = q + N
    ly = _log_rat(y)
    Y = from_frac(y)
    s = sub(mul(sub(Y, (0.5, 0.5)), ly), Y)
    s = add(s, scal(0.5, LOG_2PI))
    corr = Fr(0)
    for k in range(1, K + 1):
        corr += BERN[k - 1] / (2 * k * (2 * k - 1) * y ** (2 * k - 1))
    rem = abs(BERN[K]) / ((2 * K + 2) * (2 * K + 1) * y ** (2 * K + 1))
    s = add(s, (from_frac(corr - rem)[0], from_frac(corr + rem)[1]))
    prod = Fr(1)
    for j in range(N):
        prod *= q + j
    return sub(s, _log_rat(prod))


def gamma(q):
    return exp_iv(lngamma(q))


def rpow(base, expo):
    """base^expo for a positive interval base and a rational exponent, via exp(expo log base)."""
    return exp_iv(mul(from_frac(Fr(expo)), log_iv(base)))


def ipow(base, n):
    out = (1.0, 1.0)
    for _ in range(abs(n)):
        out = mul(out, base)
    return out if n >= 0 else div((1.0, 1.0), out)


def c(q):
    return from_frac(Fr(q))


SIN_PI_8 = scal(0.5, isqrt(sub((2.0, 2.0), isqrt((2.0, 2.0)))))      # sin(7 pi/8) = sin(pi/8) = sqrt(2 - sqrt2)/2


def K_p():
    """K = int_0^oo (1 - cos u) u^(-11/4) du = pi/(2 Gamma(11/4) sin(7 pi/8))."""
    return div(PI, mul((2.0, 2.0), mul(gamma(Fr(11, 4)), SIN_PI_8)))


def prefactor_d2():
    """c1^(2) = P2 * int_0^oo g2(u) du with P2 = -(96/7) 2^(1/4) (2 pi)^-2 12^(-1/2) Gamma(5/8) Gamma(11/4) sin(7 pi/8)/pi
    * 4 C0, C0 = (3/16)^(-5/8)."""
    P = mul(c(Fr(-96, 7)), rpow((2.0, 2.0), Fr(1, 4)))
    P = mul(P, div((1.0, 1.0), sqr(TWO_PI)))
    P = mul(P, rpow((12.0, 12.0), Fr(-1, 2)))
    P = mul(P, mul(gamma(Fr(5, 8)), gamma(Fr(11, 4))))
    P = mul(P, div(SIN_PI_8, PI))
    C0 = rpow(c(Fr(3, 16)), Fr(-5, 8))
    return mul(P, scal(4.0, C0))


def prefactor_d3():
    """c1^(3) = P3 * T3 with P3 = -(1536/7) 2^(1/4) pi C_A Gamma(11/4) sin(7 pi/8),
    C_A = (2 pi)^(-11/2) 12^(-1/2) sqrt(pi/5)."""
    CA = mul(rpow(TWO_PI, Fr(-11, 2)), rpow((12.0, 12.0), Fr(-1, 2)))
    CA = mul(CA, isqrt(div(PI, (5.0, 5.0))))
    P = mul(c(Fr(-1536, 7)), rpow((2.0, 2.0), Fr(1, 4)))
    P = mul(P, mul(PI, CA))
    return mul(P, mul(gamma(Fr(11, 4)), SIN_PI_8))


def c1_d1():
    """c1^(1) = -(192/7) 2^(1/4) * 2 * 12^(-7/4) (2 pi)^-2 12^(-1/2) sqrt(4 pi/3) 30^(7/8) 2^(7/8) Gamma(11/8)/sqrt(pi)."""
    v = mul(c(Fr(-384, 7)), rpow((2.0, 2.0), Fr(1, 4)))
    v = mul(v, rpow((12.0, 12.0), Fr(-9, 4)))
    v = mul(v, div((1.0, 1.0), sqr(TWO_PI)))
    v = mul(v, isqrt(div(scal(4.0, PI), (3.0, 3.0))))
    v = mul(v, rpow((30.0, 30.0), Fr(7, 8)))
    v = mul(v, rpow((2.0, 2.0), Fr(7, 8)))
    v = mul(v, div(gamma(Fr(11, 8)), isqrt(PI)))
    return v


def c_ref(d):
    """c_(d,ref) = Gamma(7/6) (3/2)^(1/3) D_(d-1)/(2 sqrt3 pi^(d-1) sqrt(pi)), D_1 = 4/3, D_2 = 29/6 - sqrt6
    (coefficients/side24_v1/PROOF.md (1))."""
    D = c(Fr(4, 3)) if d == 2 else sub(c(Fr(29, 6)), isqrt((6.0, 6.0)))
    v = mul(gamma(Fr(7, 6)), rpow(c(Fr(3, 2)), Fr(1, 3)))
    v = mul(v, D)
    den = mul(scal(2.0, isqrt((3.0, 3.0))), mul(ipow(PI, d - 1), isqrt(PI)))
    return div(v, den)


I_CAND_FACTOR = scal(0.5, rpow((3.0, 3.0), Fr(1, 4)))       # I^cand = (3^(1/4)/2) c1
