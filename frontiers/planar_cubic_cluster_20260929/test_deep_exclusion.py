"""Finite algebra checks for the separate deterministic exclusion addendum."""
import unittest
from fractions import Fraction as F


class DeepExclusionTests(unittest.TestCase):
    def test_rational_constant_grid(self):
        for R in map(F, (1, 2, 5)):
            for K in map(F, (1, 3, 12)):
                for k in (F(1, 10), F(1), F(3)):
                    r=k/(8*R*K)
                    lam=2*(8*R*K+56*R*K*K/k)*r
                    rho=4*R*R*K*r*r/lam
                    t=4*R*K*r/lam
                    self.assertLess(2*R*K*r,lam/2)
                    self.assertLess(rho,R*r/2)
                    self.assertLess(t,F(1,2))
                    self.assertLess(28*R*K*K*r/lam,k/2)
                    self.assertLessEqual(2*R*K*r,k/2)
                    self.assertGreater(12*k-2*R*K*r-7*K*t,11*k)
    def test_vertical_sign_bracket(self):
        # At +/-rho the guaranteed vertical variation is twice the axis bound.
        for R,K,r,lam in ((F(2),F(3),F(1,100),F(2)),
                          (F(1),F(1),F(1,1000),F(1))):
            gmax=K*R*R*r*r; rho=4*R*R*K*r*r/lam
            self.assertEqual(lam*rho/2,2*gmax)
            self.assertGreater(lam*rho/2-gmax,0)
    def test_reduced_third_polynomial_identity(self):
        # f=g(x)+h(x)z-lambda*z^2/2, zeta=h/lambda,
        # g'''=12k, h=1+2x+3x^2+4x^3. Compute both formulas independently.
        for x in (F(-2),F(-1,2),F(0),F(3,4)):
            for lam in (F(1),F(3),F(7)):
                k=F(2); h=1+2*x+3*x*x+4*x**3
                hp=2+6*x+12*x*x; hpp=6+24*x; hppp=F(24)
                direct=12*k+(3*hp*hpp+h*hppp)/lam
                fxxx=12*k+hppp*h/lam
                t=-hp/lam
                reduced=fxxx-3*hpp*t
                self.assertEqual(direct,reduced)
    def test_mixed_term_is_load_bearing(self):
        k,lam,h,hp,hpp,hppp=map(F,(1,2,1,2,6,24))
        direct=12*k+(3*hp*hpp+h*hppp)/lam
        omitted=12*k+hppp*h/lam
        self.assertNotEqual(direct,omitted)
    def test_convexity_margin(self):
        for k in (F(1,100),F(1),F(100)):
            self.assertEqual(12*k-k/2-k/2,11*k)
            self.assertGreater(11*k,0)


if __name__=='__main__': unittest.main()
