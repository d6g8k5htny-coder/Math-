"""Exact finite controls; no Gaussian-field simulation or theorem certification."""
from fractions import Fraction as F
import unittest
import barrier as b

class BarrierTests(unittest.TestCase):
    def test_rare_first_moment(self):
        for d in (2,3,4):
            for n in (3,5):
                r,k,p=b.rare_law(n,d)
                self.assertEqual(p*k,r**3)
    def test_size_bias_differs_from_nonempty_conditioning(self):
        law={0:F(1,3),1:F(1,2),3:F(1,6)}
        self.assertEqual(b.size_biased(law),{1:F(1,2),3:F(1,2)})



    def test_arbitrary_fixed_dimension(self):
        for d in range(2,7):
            r,k,p=b.rare_law(3,d)
            self.assertEqual(k,3**d)
            self.assertEqual(p,F(1,3**(9+d)))
    def test_second_factorial_exact(self):
        for d in (2,3,5):
            for n in (3,4,7):
                r,k,_=b.rare_law(n,d)
                self.assertEqual(b.rare_factorial(n,d,2),r**3*(k-1))
    def test_every_integer_factorial_order(self):
        for d in (2,3,4):
            for n in (3,5):
                r,k,_=b.rare_law(n,d)
                prod=1
                for q in range(1,9):
                    if q>1:prod*=k-q+1
                    self.assertEqual(b.rare_factorial(n,d,q),r**3*prod)
    def test_orders_above_count_are_zero(self):
        self.assertEqual(b.rare_factorial(3,2,10),0)
        self.assertEqual(b.falling(0,0),1)
    def test_probability_normalization(self):
        for n in (3,5,9):
            for d in (2,3):
                r,k,p=b.rare_law(n,d)
                self.assertGreater(p,0);self.assertLess(p,1)
                self.assertEqual((1-p)+p,1)
    def test_prescribed_pin_offset(self):
        for n in (3,7):
            for d in (2,3,4):
                _,k,_=b.rare_law(n,d)
                self.assertEqual(b.count_cap(n,d),k+2)
    def test_tail_steps(self):
        n,d=3,2;_,k,p=b.rare_law(n,d)
        self.assertEqual(b.exact_tail(n,d,1),1)
        self.assertEqual(b.exact_tail(n,d,2),p)
        self.assertEqual(b.exact_tail(n,d,k+1),p)
        self.assertEqual(b.exact_tail(n,d,k+2),0)
    def test_tail_comparison_algebra(self):
        # Ingredients of the analytic phi_d(k+2)<=2(d+1)n log n comparison.
        for d in range(2,8):
            for n in range(3,12):
                self.assertLessEqual(n**d+2,(2*n)**d)
                self.assertLessEqual(n**d+4,n**(d+1))
                self.assertGreaterEqual(3*n+d,n)
    def test_exact_size_bias_identity(self):
        law={0:F(1,3),1:F(1,2),3:F(1,6)}
        mean=sum(n*p for n,p in law.items())
        biased=b.size_biased(law)
        for q in (2,3,4):
            lhs=sum(b.falling(n,q)*p for n,p in law.items())
            rhs=mean*sum(b.falling(n-1,q-1)*p for n,p in biased.items())
            self.assertEqual(lhs,rhs)
    def test_rare_size_bias_concentrates_on_large_count(self):
        r,k,p=b.rare_law(5,3)
        biased=b.size_biased({0:1-p,k:p})
        self.assertEqual(biased,{k:F(1)})
        self.assertEqual(sum((n+2)*v for n,v in biased.items()),k+2)
    def test_cap_truncation_pathwise(self):
        for N in range(12):
            for cap in (N,N+2,N+7):
                for cutoff in (F(1,2),F(3),F(11)):
                    for q in (2,3,4):
                        rhs=cutoff**(q-1)*N+(cap**q if cap>cutoff else 0)
                        self.assertLessEqual(b.falling(N,q),rhs)
    def test_full_normalizer_once(self):
        self.assertEqual(b.tilt_cost(2,2),0)
        self.assertEqual(b.tilt_cost(3,2),1)
    def test_domains(self):
        with self.assertRaises(ValueError):b.rare_law(2,2)
        with self.assertRaises(ValueError):b.rare_law(3,1)
        with self.assertRaises(ValueError):b.rare_law(True,2)
        with self.assertRaises(ValueError):b.size_biased({0:1})
        with self.assertRaises(ValueError):b.size_biased({0:F(1,3)})
        with self.assertRaises(ValueError):b.falling(2,-1)

if __name__=='__main__': unittest.main()
