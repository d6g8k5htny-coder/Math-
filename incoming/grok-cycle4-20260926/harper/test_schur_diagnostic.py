"""Stdlib checks for incoming/grok-cycle4-20260926/harper/schur_diagnostic.py.

Run from the repository root:
    python -B -S -m unittest discover -s incoming/grok-cycle4-20260926/harper -p 'test_*.py' -v
"""
from __future__ import annotations

import os
import sys
import unittest
from decimal import Decimal as D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import schur_diagnostic as sd  # noqa: E402


class SchurDiagnosticTests(unittest.TestCase):
    def setUp(self) -> None:
        sd.MUTATE = False

    def tearDown(self) -> None:
        sd.MUTATE = False

    def test_unconditional_covariances(self) -> None:
        z = (D(0), D(0))
        self.assertEqual(sd.cov(((0, 0), z), ((0, 0), z)), 1)
        self.assertEqual(sd.cov(((1, 0), z), ((1, 0), z)), 1)
        self.assertEqual(sd.cov(((2, 0), z), ((2, 0), z)), 3)
        self.assertEqual(sd.cov(((2, 0), z), ((0, 0), z)), -1)
        self.assertEqual(sd.cov(((1, 1), z), ((1, 1), z)), 1)
        self.assertEqual(sd.cov(((0, 3), z), ((0, 1), z)), -3)

    def test_direct_schur_matches_closed_forms(self) -> None:
        for rs in ('0.3', '0.1', '0.02'):
            r = D(rs)
            six = sd.conditional(r, D(1), D(1), D(1) / 5, False)
            self.assertLess(abs(six['f_tt(M)'][1] - sd.closed_form_var_ftt(r)), D(10) ** -60)
            self.assertLess(abs(six['f_ts(M)'][1] - sd.closed_form_var_fts(r)), D(10) ** -60)

    def test_ftt_fluctuation_is_order_r_squared(self) -> None:
        r = D('0.05')
        mean, var = sd.conditional(r, D(1), D(6) / 5, D(1) / 5, False)['f_tt(M)']
        self.assertLess(abs(var / r ** 4 - D(1) / 6), D(1) / 1000)
        # mean correction beyond -6kr is order r^2, not r^3
        corr = (mean + 6 * (D(6) / 5) * r) / r ** 2
        self.assertLess(abs(corr + D(1) / 4), D(1) / 10)

    def test_eight_pin_far_endpoint_is_slaved(self) -> None:
        r = D('0.025')
        eight = sd.conditional(r, D(1), D(6) / 5, D(1) / 5, True)
        six = sd.conditional(r, D(1), D(6) / 5, D(1) / 5, False)
        self.assertLess(abs(six['f_ss(S)'][1] - 2), D(1) / 100)            # order one without the witness
        self.assertLess(abs(eight['f_ss(S)'][1] / r ** 2 - 2), D(1) / 20)    # O_p(r) with the witness
        self.assertLess(abs(eight['f_ss(M)'][1] / (r * r * (D(1) / 5) ** 2) - D(3) / 2), D(1) / 1000)

    def test_full_run_passes(self) -> None:
        self.assertEqual(sd.main([]), 0)

    def test_mutation_is_detected(self) -> None:
        self.assertEqual(sd.main(['--mutate']), 1)


if __name__ == '__main__':
    unittest.main()
