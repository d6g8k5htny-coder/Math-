#!/usr/bin/env python3
"""Exact finite controls for the conditional IBA2 count-transfer note.

No network, third-party packages, field simulation or Lean execution.
Exit 0: every finite control passes. Exit 1: assertion rejection only.
Exit 2: invalid arguments or an unexpected test error, not a math rejection.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import permutations
import json
from math import factorial
import sys
import unittest

MUTANT = None


def falling(n: int, m: int) -> int:
    if n < m:
        return 0
    value = 1
    for i in range(m):
        value *= n - i
    return value


def beta(q: int) -> int:
    return sum(j + 2 for j in range(2, q + 2))


def theta(p: F, order: int) -> F:
    p = F(p)
    if p < 0 or order < 2 or order <= p:
        raise ValueError("need p >= 0 and integer order >= 2, order > p")
    return F(1) if MUTANT == "M2" else 1 - p / order


def common_radial_power(p: F, order: int) -> F:
    return F(3) * theta(p, order) if MUTANT == "M1" else F(3)


def mixed_power(alphas: tuple[F, ...]) -> F:
    weights = list(range(4, 4 + len(alphas)))
    if MUTANT == "M3":
        weights.reverse()
    return sum((w * min(F(a), F(1)) for w, a in zip(weights, alphas)), F(0))


def envelope(n: int, order: int) -> int:
    return order ** order * (falling(n, order) + (0 if MUTANT == "M4" else 1))


def spike(n: int, q: int = 1) -> tuple[F, F, F, int]:
    r = F(1, 2 ** n)
    ordinary = r ** 3
    rare = r ** (3 + beta(q))
    return r, ordinary, rare, n + 2


class CountTransferTests(unittest.TestCase):
    def test_beta(self):
        self.assertEqual([beta(q) for q in range(1, 5)], [4, 9, 15, 22])
        for q in range(1, 12):
            self.assertEqual(beta(q), q * (q + 7) // 2)

    def test_factorial_envelope(self):
        for order in range(2, 9):
            for n in range(0, 41):
                with self.subTest(order=order, n=n):
                    self.assertLessEqual(n ** order, envelope(n, order))

    def test_holder_exponents(self):
        for order in range(2, 9):
            for p in range(1, order):
                self.assertEqual(theta(F(p), order), F(order - p, order))
                self.assertEqual(F(p, order) + theta(F(p), order), 1)
        self.assertEqual(theta(F(3, 2), 4), F(5, 8))
        for p, order in [(2, 2), (3, 2), (-1, 2), (0, 1)]:
            with self.assertRaises(ValueError):
                theta(F(p), order)

    def test_radial_power(self):
        for order in range(2, 9):
            for p in range(1, order):
                self.assertEqual(common_radial_power(F(p), order), 3)
                self.assertEqual(3 * F(p, order) + 3 * F(order - p, order), 3)

    def test_weighted_holder_finite_laws(self):
        laws = [
            [(F(1, 2), 0, 1), (F(1, 8), 1, 2), (F(1, 8), 2, 3),
             (F(1, 8), 3, 5), (F(1, 8), 7, 7)],
            [(F(1, 3), 1, 9), (F(1, 3), 4, 2), (F(1, 3), 9, 1)],
        ]
        for law in laws:
            for cutoff in [1, 2, 5]:
                selected = [(w, n, k) for w, n, k in law if n >= cutoff]
                for order in range(2, 7):
                    for p in range(1, order):
                        lhs = sum((w * k ** (order-p) * n ** p for w,n,k in selected), F(0))
                        moment = sum((w * n ** order for w,n,k in selected), F(0))
                        weighted = sum((w * k ** order for w,n,k in selected), F(0))
                        self.assertLessEqual(lhs ** order, moment ** p * weighted ** (order-p))

    def test_event_restricted_moment(self):
        # A large count outside E does not justify removing the event from K.
        law = [(F(1, 2), 0, False), (F(1, 4), 1, True),
               (F(1, 8), 5, True), (F(1, 8), 19, False)]
        pe = sum((w for w,n,e in law if e), F(0))
        for order in range(2, 8):
            lhs = sum((w * n ** order for w,n,e in law if e), F(0))
            fm = sum((w * falling(n, order) for w,n,e in law), F(0))
            self.assertLessEqual(lhs, order ** order * (pe + fm))

    def test_mixed_diagonal(self):
        b = mixed_power((F(1, 2), F(1, 4)))
        self.assertEqual(b, F(13, 4))
        self.assertEqual(common_radial_power(F(1), 2) + b * theta(F(1), 2), F(37, 8))
        self.assertEqual(common_radial_power(F(2), 4) + 4 * theta(F(2), 4), 5)

    def test_saturation(self):
        self.assertEqual(mixed_power((F(2), F(1))), 9)
        self.assertEqual(mixed_power((F(1),)), 4)
        self.assertEqual(mixed_power((F(1, 2),)), 2)
        for n in range(1, 15):
            r = F(1, 2 ** n)
            self.assertLessEqual(r ** 2 + r, 2*r)
            self.assertGreaterEqual(r ** 2 + r, r)

    def test_spike_event_thresholds(self):
        for q in range(1, 5):
            for n in range(1, 13):
                r, ordinary, rare, count = spike(n, q)
                self.assertLess(ordinary + rare, 1)
                for eta in [F(0), r/2, r, min(2*r, F(1)), F(1)]:
                    mass = rare if eta >= r else F(0)
                    self.assertLessEqual(mass, r ** 3 * (eta+r) ** beta(q))

    def test_spike_fixed_moments(self):
        for order in range(2, 9):
            bound = 2 ** order + 6 ** order * factorial(order)
            for n in range(1, 65):
                r, ordinary, rare, count = spike(n)
                moment = ordinary * 2 ** order + rare * count ** order
                fm = ordinary * falling(2, order) + rare * falling(count, order)
                self.assertLessEqual(fm, moment)
                self.assertLessEqual(moment, bound * r ** 3)
                self.assertGreaterEqual(ordinary + rare, r ** 3)

    def test_lossfree_obstruction(self):
        for p in [1, 2, 3]:
            ratios = []
            for n in [2, 8, 32, 128]:
                r, ordinary, rare, count = spike(n)
                value = rare * count ** p / (r ** 3 * (2*r) ** 4)
                self.assertEqual(value, F((n+2) ** p, 16))
                ratios.append(value)
            self.assertEqual(ratios, sorted(ratios))
            self.assertGreater(ratios[-1], 1)
        # Finite checks only; divergence follows from (n+2)^p/16 -> infinity.

    def test_remote_only_exclusion(self):
        global_count, local_count, soft = 7, 0, True
        event = local_count > 0 and soft
        self.assertFalse(event)
        self.assertEqual(local_count ** 2 * int(soft), 0)
        self.assertGreater(global_count ** 2 * int(soft), 0)
        self.assertEqual(global_count ** 2 * int(event), 0)

    def test_factorial_intensity_mass(self):
        for n in range(0, 7):
            for degree in range(1, 5):
                ordered_tuples = sum(1 for _ in permutations(range(n), degree))
                self.assertEqual(ordered_tuples, falling(n, degree))
                self.assertLessEqual(falling(n, degree), n ** degree)


def main() -> int:
    global MUTANT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutant", choices=["M1", "M2", "M3", "M4"])
    args = parser.parse_args()
    MUTANT = args.mutant
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CountTransferTests)
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
    report = {"ok": result.wasSuccessful(), "tests": result.testsRun,
              "mutant": MUTANT,
              "failures": [str(t) for t, _ in result.failures],
              "errors": [str(t) for t, _ in result.errors],
              "scope": "finite arithmetic only; no continuum or kernel verdict"}
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 2 if result.errors else (0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    sys.exit(main())
