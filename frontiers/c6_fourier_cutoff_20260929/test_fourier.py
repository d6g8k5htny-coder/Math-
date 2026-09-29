"""Finite exact algebra, exponent and inference-boundary controls."""
import itertools
import unittest
from fractions import Fraction as F
from math import prod
import fourier as f

class FourierTests(unittest.TestCase):
    def test_clearing_keeps_laurent_values(self):
        for d in (2,3,4):
            m=2
            terms={tuple([m]*d):F(2),tuple([-m]*d):F(-3),tuple([0]*d):F(5)}
            w=[F(i+2,i+1) for i in range(d)]
            out=f.clear_laurent(terms,d,m)
            self.assertEqual(f.evaluate(out,w),prod(x**m for x in w)*f.evaluate(terms,w))
            self.assertTrue(all(min(n)>=0 for n in out))

    def test_total_degree_attains_2dm(self):
        for d in range(2,7):
            for m in range(1,5):
                out=f.clear_laurent({(m,)*d:F(1)},d,m)
                degree=max(map(sum,out))
                self.assertEqual(degree,2*d*m)
                self.assertEqual(f.bezout_cap(d,m),degree**d)

    def test_cap_dimension_not_always_planar(self):
        self.assertEqual(f.bezout_cap(3,2),1728)
        self.assertEqual(f.bezout_cap(2,2),64)

    def test_separable_cosine_attains_cutoff_order(self):
        # grad sum cos(m*x_i) has 2m independent zeros per coordinate on a 2pi torus.
        for d in range(2,6):
            for m in range(1,6):
                self.assertLessEqual((2*m)**d,f.bezout_cap(d,m))
                self.assertEqual(F((2*m)**d,m**d),2**d)

    def test_gaussian_square_completion(self):
        for a,b,x in itertools.product((F(1,4),F(1),F(3)),(F(0),F(2),F(5)),(F(-2),F(0),F(3))):
            self.assertEqual(f.square_margin(a,b,x),(a*x-b)**2/(2*a))
            self.assertGreaterEqual(f.square_margin(a,b,x),0)

    def test_conditional_mean_must_be_retained(self):
        self.assertEqual(f.regression_second_moment(1,F(1,2),3),3)
        self.assertGreater(f.regression_second_moment(1,F(1,2),3),1)

    def test_uniform_coefficient_second_moment_bound(self):
        for cov,y in itertools.product((F(-1),F(-1,2),F(0),F(1,2),F(1)),range(-5,6)):
            self.assertLessEqual(f.regression_second_moment(1,cov,y),1+y*y)

    def test_all_three_cutoff_terms_decay(self):
        for d in range(2,15):
            vals=f.decay_coefficients(d,F(3,7))
            self.assertTrue(all(x>0 for x in vals.values()))
            self.assertEqual(vals['sublevel'],F(3,7)*F(2*d+1,4*d))
            self.assertEqual(vals['lipschitz'],F(3,7)*F(1,2*d))

    def test_density_volume_powers(self):
        for d in range(2,12):
            # h^(2d)/(h/lambda)^(2d-1)=h*lambda^(2d-1).
            h,lam=F(1,128),F(4)
            self.assertEqual(h**(2*d)/(h/lam)**(2*d-1),h*lam**(2*d-1))
            self.assertEqual(d-1-d,-1)

    def test_measurable_degree_is_a_union(self):
        history={1:False,2:True,3:False,4:True}
        self.assertTrue(f.success_up_to(history,3))
        self.assertFalse(f.success_up_to(history,1))

    def test_count_tail_power(self):
        self.assertEqual(f.count_tail_power(2),1)
        self.assertEqual(f.count_tail_power(3),F(2,3))
        self.assertEqual(f.count_tail_power(4),F(1,2))

    def test_factorial_logarithm_exponents(self):
        for d,p in itertools.product(range(2,8),range(2,6)):
            self.assertEqual(f.mean_log_power(d,p),F(d*(p-1),2))
            self.assertEqual(f.mean_log_power(d,p)*f.count_tail_power(d),p-1)

    def test_original_tilt_keeps_square_root(self):
        for c in (F(1,8),F(1),F(3,2)):
            self.assertEqual(f.tail_after_tilt(c),c/2)

    def test_rare_example_exact_first_and_second_moments(self):
        for d,m in itertools.product(range(2,6),range(2,9)):
            z=f.rare_count(d,m)
            self.assertEqual(z['mean'],F(1,2**(3*m*m)))
            self.assertEqual(z['factorial']/z['mean'],m**d-1)

    def test_rare_example_uniform_stretched_tail(self):
        for d,m in itertools.product(range(2,6),range(2,9)):
            z=f.rare_count(d,m)
            for k in range(m+1):
                # Threshold x=k^d, so x^(2/d)=k^2 is exact.
                tail=z['probability'] if k<m else F(0)
                self.assertLessEqual(tail,F(1,2**(2*k*k)))
            expmoment=1-z['probability']+z['probability']*2**(m*m)
            self.assertLessEqual(expmoment,2)

    def test_rare_higher_factorial_size_bias(self):
        for p in range(2,7):
            z=f.rare_count(3,3,p)
            expected=prod(z['count']-j for j in range(1,p))
            self.assertEqual(z['factorial']/z['mean'],expected)
            self.assertGreater(expected,0)

    def test_lattice_cutoff_tail_split(self):
        # After completing the square, separate an exp(-A*m^2/4) factor.
        for m,n in itertools.product(range(1,8),range(1,10)):
            if n>m:
                self.assertGreaterEqual(F(n*n,2),F(m*m,4)+F(n*n,4))

    def test_invalid_arguments(self):
        with self.assertRaises(ValueError):f.clear_laurent({(-3,0):1},2,2)
        with self.assertRaises(ValueError):f.count_tail_power(1)
        with self.assertRaises(ValueError):f.regression_second_moment(1,2,0)
        with self.assertRaises(ValueError):f.mean_log_power(2,F(3,2))

if __name__=='__main__': unittest.main()
