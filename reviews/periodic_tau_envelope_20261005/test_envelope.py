"""Exact finite falsification controls; the arbitrary-real proof is in REPORT.md."""
from fractions import Fraction as F
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('envelope_check', ROOT / 'envelope_check.py')
MOD = None
if (ROOT / 'envelope_check.py').is_file():
    MOD = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(MOD)


def compositions(n, d):
    if d == 1:
        yield (n,)
    else:
        for j in range(n + 1):
            for tail in compositions(n - j, d - 1):
                yield (j,) + tail


class EnvelopeTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(MOD, 'exact envelope implementation is not supplied')

    def test_dimension_one(self):
        self.assertEqual(MOD.envelope(1, F(7, 3), F(-4, 3)), (F(1), F(1)))

    def test_zero_and_single_terms(self):
        for d in range(1, 9):
            self.assertEqual(MOD.envelope(d, 0, 0), (F(0), F(0)))
            self.assertEqual(MOD.envelope(d, 1, 0), (F(1, d), F(1)))
            self.assertEqual(MOD.envelope(d, 0, -1), (F(-1), -F(1, d*d)))

    def test_intermediate_support_is_essential(self):
        self.assertEqual(MOD.envelope(3, 1, -1), (F(0), F(1, 4)))
        self.assertGreater(F(1, 4), max(F(0), F(2, 9)))

    def test_equal_support_values_and_attainment(self):
        expected = (F(-1), F(1, 4), F(1, 3), F(5, 16))
        self.assertEqual(MOD.support_values(4, 2, -3), expected)
        for m in range(1, 5):
            x = (F(1, m),)*m + (F(0),)*(4-m)
            self.assertEqual(MOD.polynomial(x, 2, -3), expected[m-1])

    def test_rational_simplex_grid(self):
        count = 0
        for d in range(2, 6):
            for A, B in itertools.product((-3, -1, 0, 1, 3), repeat=2):
                lo, hi = MOD.envelope(d, A, B)
                for ns in compositions(8, d):
                    x = tuple(F(n, 8) for n in ns)
                    value = A*sum(t*t for t in x) + B*sum(t*t*t for t in x)
                    self.assertLessEqual(lo, value)
                    self.assertLessEqual(value, hi)
                    count += 1
        self.assertEqual(count, 17850)

    def test_all_two_level_stationary_candidates(self):
        for d in range(2, 7):
            for A, B in itertools.product(range(-3, 4), repeat=2):
                if B == 0:
                    continue
                lo, hi = MOD.envelope(d, A, B)
                S = -F(2*A, 3*B)
                for m in range(2, d+1):
                    for p in range(1, m):
                        q = m-p
                        if p == q:
                            continue
                        s = (1-q*S)/(p-q)
                        t = S-s
                        if s > 0 and t > 0:
                            value = A*(p*s*s+q*t*t)+B*(p*s**3+q*t**3)
                            self.assertLessEqual(lo, value)
                            self.assertLessEqual(value, hi)

    def test_flat_two_coordinate_degeneracy(self):
        for B in (-4, -1, 1, 4):
            A = -F(3, 2)*B
            for j in range(11):
                s = F(j, 10)
                self.assertEqual(MOD.polynomial((s, 1-s), A, B), A+B)
            self.assertEqual(MOD.envelope(2, A, B), (A+B, A+B))

    def test_equal_multiplicity_degeneracy(self):
        for p in range(1, 5):
            B, A = F(2), -F(3, p)
            S = F(1, p)
            target = A*F(1, 2*p)+B*F(1, (2*p)**2)
            for j in range(1, 10):
                s = S*F(j, 10)
                t = S-s
                value = A*(p*s*s+p*t*t)+B*(p*s**3+p*t**3)
                self.assertEqual(value, target)

    def test_spectral_regression_direct(self):
        for u in MOD.test_directions():
            direct = MOD.direct_spectral_regression(u)
            a, b, c = MOD.test_cumulants()
            x = tuple(t*t for t in u)
            self.assertEqual(MOD.tau_polynomial(x, a, b, c), direct)

    def test_tau_bounds_and_sign_permutation(self):
        a, b, c = MOD.test_cumulants()
        for u in MOD.test_directions():
            x = tuple(t*t for t in u)
            lo, hi = MOD.tau_envelope(len(u), a, b, c)
            value = MOD.tau_polynomial(x, a, b, c)
            self.assertLessEqual(lo, value)
            self.assertLessEqual(value, hi)
            self.assertEqual(MOD.tau_polynomial(tuple(reversed(x)), a, b, c), value)

    def test_adjacent_support_difference(self):
        for A, B in itertools.product((-3, 0, 4), repeat=2):
            values = MOD.support_values(8, A, B)
            for m in range(1, 8):
                rhs = F(A*m*(m+1)+B*(2*m+1), m*m*(m+1)*(m+1))
                self.assertEqual(values[m-1]-values[m], rhs)

    def test_invalid_exact_inputs(self):
        for d in (0, -1, True, 2.0):
            with self.assertRaises((ValueError, TypeError)):
                MOD.envelope(d, 1, -1)
        for x in ((), (F(-1), F(2)), (F(1), F(1))):
            with self.assertRaises(ValueError):
                MOD.polynomial(x, 1, 1)
        with self.assertRaises(TypeError):
            MOD.envelope(2, 0.1, 1)
        with self.assertRaises(ValueError):
            MOD.tau_envelope(2, 0, 1, 1)

    def test_mutants_have_named_failures(self):
        expected = {'M1': 'intermediate_support', 'M2': 'conditioning',
                    'M3': 'fourth_cumulant_coefficient', 'M4': 'support_scaling'}
        self.assertTrue(MOD.diagnostics()['passed'])
        for label, name in expected.items():
            result = MOD.diagnostics(label)
            self.assertFalse(result['passed'])
            self.assertFalse(result['checks'][name])

    def test_cli_exit_codes(self):
        flags = ['-B', '-S'] + ([] if __debug__ else ['-O'])
        for label in (None, 'M1', 'M2', 'M3', 'M4', 'BAD'):
            args = [sys.executable] + flags + [str(ROOT/'envelope_check.py')]
            if label is not None:
                args += ['--mutant', label]
            p = subprocess.run(args, capture_output=True, timeout=20)
            self.assertEqual(p.returncode, 0 if label is None else 2 if label == 'BAD' else 1)
            if label is None:
                self.assertTrue(json.loads(p.stdout)['passed'])


if __name__ == '__main__':
    unittest.main()
