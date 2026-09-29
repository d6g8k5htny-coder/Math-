"""Exact scalar/finite-measure controls, not a Gaussian theorem checker."""
from fractions import Fraction as F
from itertools import product
from math import prod
import unittest
import controls as m

class Controls(unittest.TestCase):
    def test_reduced_third_derivative(self):
        for B,C,A,U,V,W in product([F(-2),F(1,3)], [F(-3),F(2)], [F(12)], [F(3)], [F(-2)], [F(5)]):
            q=B/C; hp=-q
            by_chain=A+U*hp-2*q*(U+V*hp)+q*q*(V+W*hp)
            self.assertEqual(m.reduced_third(A,U,V,W,q),by_chain)
    def test_hermite_integral_normalization(self):
        for r,k in product([F(1,2),F(1,7)], [F(1,3),F(2)]):
            h=r/2
            # Integral (h^2-x^2)*12k = 2*k*r^3.
            self.assertEqual(m.hermite_constant(r,k)*F(4,3)*h**3,2*k*r**3)
    def test_deep_constants_uniform(self):
        for R,k,K,j in product([F(1),F(2),F(5)],[F(1,5),F(1)],[F(13),F(37)],[1,4,16]):
            r=k/(2*(R+1)*K*j);lam=m.soft_threshold(R,r,K,k)
            q=2*(R+1)*r*K/lam
            lower=12*k-(R+1)*r*K-K*(3*q+3*q*q+q**3)
            self.assertGreater(lower,10*k)
            self.assertLessEqual((R+1)**2*K*r*r/lam,r/8)
            self.assertGreaterEqual(lam,4*R*r*K)
    def test_threshold_quadratic_norm(self):
        self.assertEqual(m.soft_threshold(2,F(1,100),20,1),64*9*F(1,100)*400)
        self.assertEqual(m.soft_threshold(2,F(1,100),40,1)/m.soft_threshold(2,F(1,100),20,1),4)
    def test_explicit_graph_extra_zero(self):
        # f=2kx^3-3kr^2*x/2-kr^3/2-lam*z^2/2 + a*(x^2-r^2/4)*z/2.
        for k,lam,a in product([F(1),F(2)],[F(1),F(3)],[F(1),F(2)]):
            r=F(1,10);x=m.model_extra_x(k,lam,a);z=a*(x*x-r*r/4)/(2*lam)
            self.assertEqual(6*k*(x*x-r*r/4)+a*x*z,0)
            self.assertEqual(-lam*z+a*(x*x-r*r/4)/2,0)
    def test_rare_norm_tail_keeps_scale(self):
        for r in [F(1,4),F(1,16)]:
            self.assertEqual(m.norm_tail(r,7,3,5),7*r**3/F(125))
    def test_mixed_local_remote_ledger(self):
        self.assertEqual(m.mixed_power(),6)
        for r in [F(1,4),F(1,16)]:
            self.assertEqual(r**4*r*r**3/r**2,r**m.mixed_power())
    def test_boundary_tube_volume(self):
        self.assertEqual(m.boundary_volume(3,F(1,10)),F(1,5)*6**3)
    def test_global_rates_and_factorials(self):
        rates=m.global_rates(F(2,3),F(5,7),F(11,13))
        self.assertEqual(rates,{1:F(2,3)+F(11,13),2:F(5,7)})
        self.assertEqual(m.factorial_coefficient(rates,2),F(10,7))
        for q in range(3,8):self.assertEqual(m.factorial_coefficient(rates,q),0)
    def test_missing_middle_is_not_automatic(self):
        self.assertGreater(m.decomposition_error(F(1,10),0),0)
        # For deterministic A=B=C=1, l1(delta_3-2delta_1)=3.
        self.assertGreaterEqual(m.decomposition_error(1,1),3)
    def test_nonempty_and_sizebiased_differ(self):
        rates={1:F(3),2:F(2)}
        self.assertEqual(m.nonempty_double(rates),F(2,5))
        self.assertEqual(m.palm_excess(rates),F(4,7))
        self.assertNotEqual(m.nonempty_double(rates),m.palm_excess(rates))
    def test_exponential_absorption_for_each_fixed_power(self):
        # e^{-c/u^a} <= n! (u^a/c)^n; choose an integer n to absorb a fixed loss.
        for loss,target,a in product(range(3,17),[2,5],[F(1,4),F(2,3),F(2)]):
            n=m.absorption_order(loss,target,a)
            self.assertGreaterEqual(a*n-loss,target)

if __name__=='__main__': unittest.main()
