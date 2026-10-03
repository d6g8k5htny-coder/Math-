"""Gamma at rationals and rational powers, as outward-rounded intervals.  These are the functions lngamma, gamma and rpow
of frontiers/cusp_coefficient_certified_20261001/consts.py (Math-#219); their code lines are unchanged.

log Gamma(y) for y = q + N >= 10 uses Stirling's series with the remainder bounded by the first omitted term (real y > 0),
and log Gamma(q) = log Gamma(q + N) - log prod_(j<N) (q + j), the product taken exactly."""
from fractions import Fraction as Fr
from ia import add, sub, mul, scal, from_frac, PI
from elem import exp_iv, log_iv

BERN = [Fr(1, 6), Fr(-1, 30), Fr(1, 42), Fr(-1, 30), Fr(5, 66), Fr(-691, 2730), Fr(7, 6), Fr(-3617, 510),
        Fr(43867, 798), Fr(-174611, 330), Fr(854513, 138)]          # B_2, B_4, ..., B_22
TWO_PI = scal(2.0, PI)
LOG_2PI = log_iv(TWO_PI)


def _log_rat(q):
    return log_iv(from_frac(Fr(q)))


def lngamma(q, N=10, K=10):
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
    """base^expo for a positive interval base and a rational exponent"""
    return exp_iv(mul(from_frac(Fr(expo)), log_iv(base)))
