"""Exact finite controls for the separate Poisson-coefficient addendum."""
import unittest
from fractions import Fraction as F
import cluster_check as c


def tv(left, right):
    return sum((abs(left.get(n, 0)-right.get(n, 0))
                for n in set(left) | set(right)), F(0))/2


def examples():
    for p in [F(1, 128), F(1, 32), F(1, 8)]:
        for single in [F(0), F(1, 3), F(2, 3)]:
            yield {0: 1-p, 1: p*single, 2: p*(1-single)/2, 4: p*(1-single)/2}


class SharpCoefficientTests(unittest.TestCase):
    def test_occurrence_bernoulli_identity(self):
        for law in examples():
            p = 1-law[0]
            beta = sum(mass for n, mass in law.items() if n >= 2)
            self.assertEqual(tv(law, {0: 1-p, 1: p}), beta)

    def test_mean_bernoulli_identity(self):
        for law in examples():
            mu = c.moment(law, 1)
            h = sum(n*mass for n, mass in law.items() if n >= 2)
            self.assertLessEqual(mu, 1)
            self.assertEqual(tv(law, {0: 1-mu, 1: mu}), h)

    def test_all_rate_lower_probes(self):
        for law in examples():
            p = 1-law[0]
            beta = sum(mass for n, mass in law.items() if n >= 2)
            for rate in [F(0), p/2, p, 2*p, 4*p, F(1), F(3)]:
                lo, hi = c.poisson_tv(law, rate)
                self.assertGreaterEqual(lo, beta-2*p*p)
                self.assertLessEqual(lo, hi)

    def test_occurrence_rate_upper(self):
        for law in examples():
            p = 1-law[0]
            beta = sum(mass for n, mass in law.items() if n >= 2)
            lo, hi = c.poisson_tv(law, p)
            self.assertLessEqual(hi, beta+p*p)

    def test_mean_rate_interval(self):
        for law in examples():
            mu = c.moment(law, 1)
            h = sum(n*mass for n, mass in law.items() if n >= 2)
            lo, hi = c.poisson_tv(law, mu)
            self.assertGreaterEqual(lo, h-mu*mu)
            self.assertLessEqual(hi, h+mu*mu)

    def test_minimizing_interval_and_mean_cost(self):
        one, multi, mass = F(2, 3), F(1, 3), F(1)
        def coefficient(rate):
            return (abs(mass-rate)+abs(one-rate)+multi)/2
        for rate in [one, F(5, 6), mass]:
            self.assertEqual(coefficient(rate), multi)
        for rate in [F(0), F(1, 3), F(4, 3), F(2)]:
            self.assertGreater(coefficient(rate), multi)
        self.assertEqual(coefficient(one+2*multi), 2*multi)


if __name__ == '__main__':
    unittest.main()
