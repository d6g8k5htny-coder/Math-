"""Exact finite regression tests; not a Gaussian-field proof."""
import subprocess
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path
import cluster_check as c


class ClusterTests(unittest.TestCase):
    def setUp(self):
        self.law = {0: F(3, 4), 1: F(1, 8), 3: F(1, 8)}

    def test_validate(self):
        self.assertEqual(c.validate(self.law), self.law)

    def test_negative_mass(self):
        with self.assertRaises(ValueError):
            c.validate({0: F(2), 1: F(-1)})

    def test_float_rejected(self):
        with self.assertRaises(ValueError):
            c.validate({0: 1.0})

    def test_bool_key_rejected(self):
        with self.assertRaises(ValueError):
            c.validate({True: F(1)})

    def test_bad_mass(self):
        with self.assertRaises(ValueError):
            c.validate({0: F(1, 2)})

    def test_negative_key(self):
        with self.assertRaises(ValueError):
            c.validate({-1: F(1)})

    def test_positive_law(self):
        self.assertEqual(c.tilt(self.law, False), {1: F(1, 2), 3: F(1, 2)})

    def test_size_bias(self):
        self.assertEqual(c.tilt(self.law, True), {1: F(1, 4), 3: F(3, 4)})

    def test_empty_condition(self):
        with self.assertRaises(ValueError):
            c.tilt({0: F(1)}, False)

    def test_empty_size_bias(self):
        with self.assertRaises(ValueError):
            c.tilt({0: F(1)}, True)

    def test_zero_moment(self):
        self.assertEqual(c.moment(self.law, 0), 1)

    def test_first_moment(self):
        self.assertEqual(c.moment(self.law, 1), F(1, 2))

    def test_factorial_second(self):
        self.assertEqual(c.moment(self.law, 2, True), F(3, 4))

    def test_falling_above_support(self):
        self.assertEqual(c.falling(2, 3), 0)

    def test_invalid_order(self):
        with self.assertRaises(ValueError):
            c.moment(self.law, -1)

    def test_stirling_identity(self):
        for n in range(8):
            for q in range(1, 8):
                self.assertEqual(n**q, sum(c.stirling(q, j) * c.falling(n, j)
                                          for j in range(1, q + 1)))

    def test_palm_variance_identity(self):
        j, y = c.tilt(self.law, False), c.tilt(self.law, True)
        mean = c.moment(j, 1)
        self.assertEqual(c.moment(y, 1) - mean,
                         (c.moment(j, 2) - mean**2) / mean)

    def test_bell_two(self):
        self.assertEqual(c.cp_moments(self.law, 2)[2], F(1))

    def test_bell_three(self):
        a = [c.moment(self.law, j, True) for j in range(1, 4)]
        self.assertEqual(c.cp_moments(self.law, 3)[3], a[2]+3*a[1]*a[0]+a[0]**3)

    def test_bell_vs_partitions(self):
        def partitions(xs):
            if not xs:
                yield []
                return
            for p in partitions(xs[1:]):
                yield [[xs[0]]] + p
                for i in range(len(p)):
                    yield p[:i] + [[xs[0]] + p[i]] + p[i+1:]
        for q in range(1, 7):
            total = F(0)
            for p in partitions(list(range(q))):
                term = F(1)
                for block in p:
                    term *= c.moment(self.law, len(block), True)
                total += term
            self.assertEqual(c.cp_moments(self.law, q)[q], total)

    def test_exp_zero(self):
        self.assertEqual(c.exp_bounds(F(0)), (F(1), F(1)))

    def test_exp_nested(self):
        for x in [F(1, 10), F(1), F(3)]:
            lo, hi = c.exp_bounds(x, 20)
            lo2, hi2 = c.exp_bounds(x, 40)
            self.assertLessEqual(lo, lo2)
            self.assertLessEqual(hi2, hi)
            self.assertLessEqual(lo2, hi2)

    def test_exp_negative_rejected(self):
        with self.assertRaises(ValueError):
            c.exp_bounds(F(-1))

    def test_poisson_zero_rate(self):
        self.assertEqual(c.poisson_tv(self.law, F(0)), (F(1, 4), F(1, 4)))

    def test_poisson_zero_law(self):
        lo, hi = c.poisson_tv({0: F(1)}, F(1, 2))
        elo, ehi = c.exp_bounds(F(1, 2))
        self.assertEqual((lo, hi), (1-ehi, 1-elo))

    def test_nonunique_intensities(self):
        self.assertNotEqual({2: F(1)}, {3: F(1)})

    def test_no_third_lower_bound(self):
        self.assertEqual(c.moment({0: F(7, 8), 2: F(1, 8)}, 3, True), 0)

    def test_main_and_mutants(self):
        script = str(Path(c.__file__).resolve())
        reference = None
        for flags in (['-B', '-S'], ['-B', '-O', '-S']):
            run = subprocess.run([sys.executable, *flags, script], capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            if reference is None:
                reference = run.stdout
            self.assertEqual(run.stdout, reference)
            for name in c.MUTANTS:
                run = subprocess.run([sys.executable, *flags, script, '--mutant', name],
                                     capture_output=True)
                self.assertEqual(run.returncode, 1, (name, run.stdout, run.stderr))
            run = subprocess.run([sys.executable, *flags, script, '--mutant', 'unknown'],
                                 capture_output=True)
            self.assertEqual(run.returncode, 2)


if __name__ == '__main__':
    unittest.main()
