"""Exact tests for the two-coordinate transformed-price counterexample."""
from fractions import Fraction as Q
import unittest
import frontier_math as f

class PriceBoundary(unittest.TestCase):
    def test_exact_good_probability(self):
        m=f.Model((1,),(1,),())
        self.assertEqual(f.probability_of(m,(Q(1,2),Q(1,2)),m.good),Q(3,4))
    def test_every_generator_family(self):
        # Four possible generators. A family covers the unique obstruction X
        # exactly when it is nonempty, since every generator is contained in X.
        costs=(Q(1),Q(2,3),Q(2,3),Q(4,9))
        minimum=min(sum((costs[j] for j in range(4) if family>>j&1),Q(0)) for family in range(1,16))
        self.assertEqual(minimum,Q(4,9))
        self.assertGreater(minimum,Q(1,3))
        self.assertEqual(2*Q(1,3),Q(2,3))
    def test_two_colors_do_not_inherit_counterexample(self):
        m=f.Model((1,),(1,),())
        self.assertEqual(m.chromatic_table()[m.full],2)
        with self.assertRaises(ValueError):
            f.budget_certificate(m,(Q(1,2),)*2,(Q(2,3),)*2)

if __name__=='__main__': unittest.main()
