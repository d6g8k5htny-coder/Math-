"""Exact finite ledgers for GD1. They do not prove conditional Gaussian bounds."""
from fractions import Fraction as F
from math import ceil, factorial
import unittest


class DerivativeWeightTests(unittest.TestCase):
    def test_one_full_normalizer(self):
        # Remote normalized moment: endpoint short columns, normalizer, height.
        self.assertEqual(2-2+3,3)
        self.assertNotEqual(2+3,3)
        self.assertNotEqual(2-2-2+3,3)

    def test_pin_and_collar_spatial_powers(self):
        for d in range(2,10):
            self.assertEqual((3-d)+d,3)

    def test_exponential_absorption_budgets(self):
        # These overestimate by retaining the older source's cap costs as well.
        for d in range(2,9):
            for p in range(10):
                for alpha,cost in ((F(2),F(6+3*d+p)),
                                   (F(2,3),F(15+39*d+10*p)),
                                   (F(1,4),F(40*d+5+10*p))):
                    n=ceil(cost/alpha)
                    self.assertGreaterEqual(alpha*n,cost)
                    self.assertLess(alpha*(n-1),cost)

    def test_inverse_angle_budgets(self):
        for d in range(2,9):
            for p in range(10):
                for cost in (16*d+10+4*p,22*d+15+6*p):
                    n=ceil(F(cost,2))
                    self.assertGreaterEqual(2*n,cost)
                    self.assertLess(2*(n-1),cost)

    def test_positive_exponential_series_term(self):
        # exp(y)>=y^n/n!: retain the n-th term of a strictly positive polynomial.
        for y in (F(1,2),F(1),F(3),F(10)):
            for n in (1,2,5,9):
                partial=sum((y**j/F(factorial(j)) for j in range(n+1)),F(0))
                self.assertGreater(partial,y**n/F(factorial(n)))

    def test_shell_cross_term(self):
        for r in (F(1,100),F(1,20),F(1,10)):
            for s in (4*r,F(1,2),F(1)):
                if r>s/4: continue
                value=(r+s*s)**2/(s*s)
                self.assertEqual(value,r*r/(s*s)+2*r+s*s)
                self.assertLessEqual(value,2*(r*r/(s*s)+s*s))

    def test_full_strip_volume(self):
        for d in range(2,10):
            for s in (F(1,100),F(1,3),F(1,2),F(1)):
                self.assertLessEqual(s**d,s*s)

    def test_dyadic_sums(self):
        for levels in range(1,13):
            r=F(1,2**(levels+3))
            scales=[4*r*2**j for j in range(levels)]
            self.assertLess(sum((r/s)**2 for s in scales),F(1,12))
            self.assertLess(sum(s*s for s in scales),F(4,3)*scales[-1]**2)

    def test_count_weighted_tail_is_pointwise(self):
        for count in (0,1,2,9):
            for norm in (F(1),F(3),F(10)):
                for threshold in (F(1),F(2),F(5)):
                    for p in range(5):
                        left=count if norm>threshold else 0
                        self.assertLessEqual(left,count*norm**p/threshold**p)


if __name__=='__main__': unittest.main()
