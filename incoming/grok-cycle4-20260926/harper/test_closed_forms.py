"""Stdlib checks for incoming/grok-cycle4-20260926/harper/CLOSED_FORMS_FTS_FTT.md.

Scientific effect: NONE. These are finite-r evaluations of the closed forms
against their exact series prefixes. They are not a continuum proof.
"""
from __future__ import annotations

import math
import unittest


def var_fts(r: float) -> float:
    e = math.exp(r * r)
    return (e - 1.0 - r * r) / (e - 1.0)


def var_fts_series(r: float) -> float:
    x = r * r
    # r^2/2 - r^4/12 + r^6/48 - ... from expanding (E-1-r^2)/(E-1)
    # Use four terms of the known series of Identity TS.
    return x / 2.0 - (x * x) / 12.0 + (x ** 3) / 48.0 - (x ** 4) / 180.0


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


if __name__ == "__main__":
    unittest.main()
