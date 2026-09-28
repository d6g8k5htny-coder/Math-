"""Exact finite controls, not a proof of a continuum probability theorem."""
from fractions import Fraction as F
from itertools import product
from math import comb
import unittest
import certificate as c


class CertificateTests(unittest.TestCase):
    def test_exact_nine_tail_identity(self):
        for z in (F(2), F(5, 2), F(87, 32), F(3)):
            q = 1/z
            direct = sum(F(comb(9, j))*(1-q)**j*q**(9-j) for j in range(3))
            self.assertEqual(c.tail_nine(z), direct)

    def test_tail_domain(self):
        for z in (F(0), F(1, 2), True, 2.7):
            with self.assertRaises((ValueError, TypeError)):
                c.tail_nine(z)

    def test_exponential_bracket(self):
        lo, hi = c.exp_one_interval(6)
        self.assertEqual(lo, F(1957, 720))
        self.assertEqual(hi, F(31967, 11760))
        self.assertLess(hi, F(87, 32))
        self.assertGreater(lo, F(8, 3))

    def test_log_brackets_and_reciprocals(self):
        self.assertEqual(c.log_interval(F(1)), (0, 0))
        lo, hi = c.log_interval(F(2))
        self.assertGreater(lo, F(2, 3))
        self.assertLess(hi, F(7, 10))
        self.assertEqual(c.log_interval(F(4)), (2*lo, 2*hi))
        self.assertEqual(c.log_interval(F(1, 2)), (-hi, -lo))

    def test_logarithm_remainder_is_retained(self):
        self.assertEqual(c.log_interval(F(2), 1), (F(2, 3), F(25, 36)))

    def test_exact_rational_tail_separation(self):
        lo, hi = c.coarse_tail_interval()
        self.assertEqual(lo, c.tail_polynomial(F(1957, 720))/F(87, 32)**9)
        self.assertEqual(hi, c.tail_polynomial(F(87, 32))/F(1957, 720)**9)
        self.assertGreater(lo, F(625, 131072))
        self.assertLess(hi, F(1, 64))
        self.assertGreater(F(8)-F(11, 4)**2, 0)

    def test_even_chernoff_envelope(self):
        self.assertEqual(c.even_large_tail_bound(4), F(625, 131072))
        for a in range(4, 34, 2):
            self.assertLessEqual(c.even_large_tail_bound(a), c.even_large_tail_bound(4))
        for a in (2, 3, 5, 0, True):
            with self.assertRaises((ValueError, TypeError)):
                c.even_large_tail_bound(a)

    def test_tight_factor_enclosure(self):
        lo, hi = c.factor_interval()
        self.assertGreater(lo, F(47734798895766998533, 10**20))
        self.assertLess(hi, F(47734798895766998534, 10**20))
        self.assertLess(hi, F(1, 2))
        self.assertGreater(hi, lo)

    def test_invalid_interval_arguments(self):
        for n in (0, True, 1.5):
            with self.assertRaises((ValueError, TypeError)):
                c.exp_one_interval(n)
        for x in (0, -1, True, 0.5):
            with self.assertRaises((ValueError, TypeError)):
                c.log_interval(x)

    def test_weighted_overlap_load_is_sum(self):
        blocks = [{0, 1}, {1, 2}]
        self.assertEqual(c.coordinate_load(blocks, [F(1, 3), F(1, 5)]), F(8, 15))
        self.assertEqual(c.coordinate_load([{0}, {1}], [F(1, 3), F(1, 5)]), F(1, 3))
        self.assertEqual(c.coordinate_load([{0}, {0}], [F(1, 3), F(1, 5)]), F(8, 15))

    def test_active_minimal_cover_unchanged_scope(self):
        blocks = [{0, 1, 2, 3, 4}, {0, 1, 2, 3, 4}, set(range(9)), {9, 10}]
        self.assertEqual(c.minimal_active_indices(blocks, [1, 1, 2, 1], [4, 4, 4, 1]), [0])
        # Inactive demand-one is not charged, although it remains a constraint of D.
        self.assertEqual(c.minimal_active_indices([set(range(5)), {4, 5}], [1, 1], [4, 1]), [0])

    def test_cover_input_validation(self):
        with self.assertRaises(ValueError):
            c.minimal_active_indices([{0, 1}], [1], [4])
        with self.assertRaises(ValueError):
            c.coordinate_load([{0}], [F(-1)])
        with self.assertRaises(ValueError):
            c.coordinate_load([{0}], [])

    def test_integer_weighted_entropy_probability_form(self):
        blocks = [{0, 1}, {1, 2}, {2, 0}]
        weights = [1, 2, 3]
        exponent = int(c.coordinate_load(blocks, list(map(F, weights))))
        self.assertEqual(exponent, 5)
        for vals in product((F(0), F(1, 3), F(2, 3), F(1)), repeat=3):
            p = dict(enumerate(vals))
            joint = c.good_probability(blocks, [1, 1, 1], p)
            rhs = F(1)
            for block, weight in zip(blocks, weights):
                rhs *= c.good_probability([block], [1], p)**weight
            self.assertLessEqual(joint**exponent, rhs)

    def test_shared_coordinate_max_instead_of_sum_is_false(self):
        p = {0: F(1, 2)}
        joint = c.good_probability([{0}], [0], p)
        self.assertEqual(joint, F(1, 2))
        # Two identical local events, each with weight one, need load TWO.
        self.assertGreater(joint, joint*joint)
        self.assertEqual(joint**2, joint*joint)

    def test_exact_enumeration_endpoints(self):
        blocks = [{0, 1}, {1, 2}]
        self.assertEqual(c.good_probability(blocks, [1, 1], {v: F(0) for v in range(3)}), 1)
        self.assertEqual(c.good_probability(blocks, [1, 1], {v: F(1) for v in range(3)}), 0)
        self.assertEqual(c.good_probability(blocks, [1, 1], {v: F(1, 2) for v in range(3)}), F(5, 8))


if __name__ == '__main__':
    unittest.main(verbosity=2)
