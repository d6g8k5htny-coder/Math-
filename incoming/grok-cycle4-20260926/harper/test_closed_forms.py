"""Stdlib checks for incoming/grok-cycle4-20260926/harper/CLOSED_FORMS_FTS_FTT.md.

Scientific effect: NONE. These are finite-r evaluations of the closed forms
against their exact series prefixes. They are not a continuum proof.
"""
from __future__ import annotations

from fractions import Fraction
import math
import unittest

# Exact power series in x = r^2, truncated at x^ORDER (inclusive), as lists of
# Fractions indexed by the power of x.
ORDER = 11


def _series_exp() -> list[Fraction]:
    return [Fraction(1, math.factorial(k)) for k in range(ORDER + 1)]


def _series_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * (ORDER + 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if i + j > ORDER:
                break
            out[i + j] += ai * bj
    return out


def _series_add(*terms: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * (ORDER + 1)
    for t in terms:
        for k, c in enumerate(t):
            out[k] += c
    return out


def _series_scale(a: list[Fraction], c: Fraction | int) -> list[Fraction]:
    return [ai * c for ai in a]


def _series_mono(k: int, c: Fraction | int = 1) -> list[Fraction]:
    out = [Fraction(0)] * (ORDER + 1)
    out[k] = Fraction(c)
    return out


def _series_div(num: list[Fraction], den: list[Fraction]) -> tuple[int, list[Fraction]]:
    """Return (shift, q) with num/den = x^shift * sum q[k] x^k, exactly."""
    kn = next(k for k, c in enumerate(num) if c != 0)
    kd = next(k for k, c in enumerate(den) if c != 0)
    n = num[kn:] + [Fraction(0)] * kn
    d = den[kd:] + [Fraction(0)] * kd
    length = ORDER + 1 - max(kn, kd)
    q = [Fraction(0)] * length
    for i in range(length):
        q[i] = (n[i] - sum(q[j] * d[i - j] for j in range(i))) / d[0]
    return kn - kd, q


def tt_numerator_series() -> list[Fraction]:
    # r^6 E - r^4 E - r^4 + 4 r^2 E - 4 r^2 - 2 E^2 + 4 E - 2, with x = r^2.
    e = _series_exp()
    return _series_add(
        _series_mul(_series_mono(3), e),
        _series_scale(_series_mul(_series_mono(2), e), -1),
        _series_mono(2, -1),
        _series_scale(_series_mul(_series_mono(1), e), 4),
        _series_mono(1, -4),
        _series_scale(_series_mul(e, e), -2),
        _series_scale(e, 4),
        _series_mono(0, -2),
    )


def tt_denominator_series() -> list[Fraction]:
    # r^4 E - (E - 1)^2, with x = r^2.
    e = _series_exp()
    em1 = _series_add(e, _series_mono(0, -1))
    return _series_add(_series_mul(_series_mono(2), e), _series_scale(_series_mul(em1, em1), -1))


def ts_series() -> list[Fraction]:
    # (E - 1 - x) / (E - 1), with x = r^2.
    e = _series_exp()
    em1 = _series_add(e, _series_mono(0, -1))
    shift, q = _series_div(_series_add(em1, _series_mono(1, -1)), em1)
    assert shift == 1
    return [Fraction(0)] + q


def var_fts(r: float) -> float:
    e = math.exp(r * r)
    return (e - 1.0 - r * r) / (e - 1.0)


def var_fts_series(r: float) -> float:
    x = r * r
    # Exact series of Identity TS: r^2/2 - r^4/12 + r^8/720 + O(r^{12}).
    # The r^6 coefficient vanishes.
    return x / 2.0 - (x * x) / 12.0 + (x ** 4) / 720.0


def var_ftt(r: float) -> float:
    e = math.exp(r * r)
    e2 = e * e
    r2 = r * r
    r4 = r2 * r2
    r6 = r4 * r2
    num = r6 * e - r4 * e - r4 + 4.0 * r2 * e - 4.0 * r2 - 2.0 * e2 + 4.0 * e - 2.0
    den = r4 * e - (e - 1.0) ** 2
    return num / den


def var_ftt_series(r: float) -> float:
    r2 = r * r
    r4 = r2 * r2
    r6 = r4 * r2
    r8 = r4 * r4
    r10 = r8 * r2
    return r4 / 6.0 - r6 / 30.0 + r8 / 360.0 - r10 / 12600.0


class ClosedFormTests(unittest.TestCase):
    def test_fts_matches_series_on_moderate_r(self) -> None:
        for r in (0.2, 0.35, 0.5, 0.75):
            exact = var_fts(r)
            approx = var_fts_series(r)
            rel = abs(exact - approx) / exact
            self.assertLess(rel, 5e-3, msg=f"fts r={r}")

    def test_fts_limit_beta(self) -> None:
        # Var(beta) = Var(fts)/r^2 -> 1/2
        r = 0.05
        value = var_fts(r) / (r * r)
        self.assertAlmostEqual(value, 0.5, delta=2e-3)

    def test_ftt_matches_series_on_moderate_r(self) -> None:
        for r in (0.2, 0.35, 0.5, 0.75, 1.0):
            exact = var_ftt(r)
            approx = var_ftt_series(r)
            rel = abs(exact - approx) / exact
            self.assertLess(rel, 2e-2, msg=f"ftt r={r} exact={exact} series={approx}")

    def test_ftt_positive_and_less_than_unconditional(self) -> None:
        for r in (0.2, 0.5, 1.0, 1.5, 2.0):
            v = var_ftt(r)
            self.assertGreater(v, 0.0, msg=f"r={r}")
            self.assertLess(v, 3.0, msg=f"r={r}")

    def test_fts_positive_and_less_than_one(self) -> None:
        for r in (0.05, 0.2, 0.5, 1.0, 2.0):
            v = var_fts(r)
            self.assertGreater(v, 0.0, msg=f"r={r}")
            self.assertLess(v, 1.0, msg=f"r={r}")

    def test_ftt_leading_coefficient(self) -> None:
        r = 0.15
        leading = (r ** 4) / 6.0
        rel = abs(var_ftt(r) - leading) / leading
        self.assertLess(rel, 0.05)

    def test_fts_r6_coefficient_vanishes_numerically(self) -> None:
        # (var/r^2 - 1/2 + r^2/12) / r^4 must tend to 0 (the r^6 coefficient),
        # not to a nonzero constant such as 1/48. Normalize by r^4 and use
        # shrinking radii; the normalized residual is r^2/720 + O(r^6) and
        # must decrease with r. Float64 cancellation grows as r shrinks, so
        # the radii stay moderate and the ratio test carries the content.
        radii = (0.4, 0.3, 0.2, 0.15)
        normalized = []
        for r in radii:
            x = r * r
            residual = var_fts(r) / x - 0.5 + x / 12.0
            normalized.append(residual / (x * x))
        for value, r in zip(normalized, radii):
            expected = (r ** 2) / 720.0
            self.assertAlmostEqual(value, expected, delta=2e-2 * expected, msg=f"r={r}")
        for earlier, later in zip(normalized, normalized[1:]):
            self.assertLess(abs(later), abs(earlier))

    # Exact rational-series checks of the closed forms (no floating point).

    def test_ts_exact_series_coefficients(self) -> None:
        q = ts_series()
        expected = {1: Fraction(1, 2), 2: Fraction(-1, 12), 3: Fraction(0), 4: Fraction(1, 720), 5: Fraction(0)}
        for k, c in expected.items():
            self.assertEqual(q[k], c, msg=f"x^{k}")

    def test_tt_denominator_order_and_leading_coefficient(self) -> None:
        den = tt_denominator_series()
        # r^4 E - (E-1)^2 = -x^4/12 - x^5/12 - (2/45) x^6 + ...: first nonzero
        # order is r^8 (x^4), coefficient -1/12; there is no r^6 term.
        self.assertEqual(den[:4], [Fraction(0)] * 4)
        self.assertEqual(den[4], Fraction(-1, 12))
        self.assertEqual(den[5], Fraction(-1, 12))
        self.assertEqual(den[6], Fraction(-2, 45))

    def test_tt_numerator_order_and_leading_coefficient(self) -> None:
        num = tt_numerator_series()
        # Numerator vanishes to order r^12 (x^6) with coefficient -1/72.
        self.assertEqual(num[:6], [Fraction(0)] * 6)
        self.assertEqual(num[6], Fraction(-1, 72))
        self.assertEqual(num[7], Fraction(-1, 90))

    def test_tt_exact_series_coefficients(self) -> None:
        shift, q = _series_div(tt_numerator_series(), tt_denominator_series())
        self.assertEqual(shift, 2)
        # r^4/6 - r^6/30 + r^8/360 - r^10/12600 + O(r^12)
        self.assertEqual(q[0], Fraction(1, 6))
        self.assertEqual(q[1], Fraction(-1, 30))
        self.assertEqual(q[2], Fraction(1, 360))
        self.assertEqual(q[3], Fraction(-1, 12600))

    def test_tt_exact_series_negative_control(self) -> None:
        # A denominator with the wrong order (r^6/12, the superseded statement)
        # must not reproduce the displayed quotient.
        wrong_den = _series_mono(3, Fraction(1, 12))
        shift, q = _series_div(tt_numerator_series(), wrong_den)
        self.assertNotEqual((shift, q[0]), (2, Fraction(1, 6)))


if __name__ == "__main__":
    unittest.main()
