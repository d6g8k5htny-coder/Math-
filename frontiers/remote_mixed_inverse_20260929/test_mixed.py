"""Exact finite controls of exponents, normalization and limiting coefficients."""
from fractions import Fraction as F
import itertools
import unittest
import mixed as m

class MixedTests(unittest.TestCase):
    def test_cubic_gap_domain(self):
        self.assertFalse(m.finite(F(1),F(1,3)))
        self.assertTrue(m.finite(F(1),F(1,4)))
        self.assertTrue(m.finite(0,F(1,2)))
        self.assertFalse(m.finite(0,F(2,3)))

    def test_exact_domain_grid(self):
        for q,b in itertools.product([F(i,12) for i in range(30)],repeat=2):
            # Independent tests from the near-s and t-integrals.
            expected = (b<1 and 1-q-3*b>-1)
            self.assertEqual(m.finite(q,b),expected)

    def test_strict_endpoint(self):
        for b in (F(0),F(1,6),F(1,3),F(1,2),F(2,3)):
            self.assertFalse(m.finite(2-3*b,b))
            self.assertEqual(m.cutoff_regime(2-3*b,b),'logarithmic')

    def test_beta_shape(self):
        self.assertEqual(m.alpha(F(1,2),F(1,4)),F(1,4))
        self.assertEqual(m.alpha(1,0),F(1,3))
        self.assertEqual(m.alpha(0,F(1,3)),F(1,3))

    def test_beta_normalization_by_integer_substitution(self):
        for q,b in ((0,0),(1,0),(0,F(1,3)),(F(1,2),F(1,4)),(F(1,3),F(2,5))):
            a=(2-F(q)-3*F(b))/3
            n,k=a.denominator,a.numerator
            # g=u^n transforms g^(a-1)(1-g)dg to n*u^(k-1)(1-u^n)du.
            integral = n*(F(1,k)-F(1,k+n))
            self.assertEqual(2*m.square_density_factor(q,b)*integral,1)

    def test_beta_moments_and_old_law(self):
        self.assertEqual(m.gap_moment(0,0,1),F(1,4))
        self.assertEqual(m.gap_variance(0,0),F(9,176))
        self.assertEqual(m.gap_moment(1,0,1),F(1,7))
        self.assertEqual(m.square_density_factor(0,0),F(5,9))
        for q,b in ((0,0),(1,0),(0,F(1,2))):
            a=(2-F(q)-3*F(b))/3
            for j in range(7):
                self.assertEqual(m.gap_moment(q,b,j),a*(a+1)*(F(1)/(a+j)-F(1)/(a+j+1)))

    def test_coefficient_parts(self):
        c,p12,pk,pt=m.coefficient_parts(F(1,2),F(1,4))
        self.assertEqual((c,p12,pk,pt),(F(4,15),F(1,2),F(5,4),F(3,2)))
        self.assertEqual(m.coefficient_parts(0,0),(F(3,40),F(2,3),F(5,3),F(4,3)))

    def test_physical_gap_not_normalized_gap(self):
        q,b=F(1,2),F(1,4)
        self.assertEqual(m.coefficient_parts(q,b)[2],(5-q)/3-b)
        self.assertNotEqual(m.coefficient_parts(q,b)[2],(5-q)/3)

    def test_T_exponent_beta_cancels(self):
        for q in (F(0),F(1,3),F(1)):
            for b in (F(0),F(1,12),F(1,6)):
                if m.finite(q,b):
                    self.assertEqual(m.coefficient_parts(q,b)[3],2-b-(2-q-3*b)/3)

    def test_overlap_via_integer_substitution(self):
        for q,b in ((0,0),(1,0),(0,F(1,3)),(F(1,2),F(1,4))):
            q,b=F(q),F(b)
            exponent=2-q-3*b
            n,k=exponent.denominator,exponent.numerator
            # s=u^n, root=1 and |t|=k_window=1 gives elementary polynomial integral.
            integral=n*(F(1,k)-F(1,k+3*n))
            c,_,_=m.overlap_integral(q,b,1,1,1)
            self.assertEqual(c,integral)
            # Multiplying by 36 and converting t=-T/12 preserves the claimed prefactor.
            self.assertEqual(36*c/144,m.coefficient_parts(q,b)[0])

    def test_coefficient_relative_to_A_minus_q(self):
        for q,b in ((0,F(1,3)),(F(1,2),F(1,4)),(1,F(1,6))):
            q,b=F(q),F(b);lam=q+3*b
            c=m.coefficient_parts(q,b)[0];base=m.coefficient_parts(q,0)[0]
            self.assertEqual(c/base,(2-q)*(5-q)/((2-lam)*(5-lam)))
            self.assertEqual(m.coefficient_parts(q,b)[1],m.coefficient_parts(q,0)[1])

    def test_dimension_cancellation_and_fixed_r_boundary(self):
        for d in range(2,13):
            for b in (F(0),F(1,6),F(1,3),F(2,3),F(5,6)):
                self.assertEqual(m.radial_power(d,b),1-3*b)
        self.assertEqual(m.cutoff_regime(0,F(3,4)),'power')
        self.assertEqual(m.cutoff_regime(0,F(1,2)),'finite')

    def test_cutoff_constants_model_density(self):
        # j_beta=J delta^(1-3beta). Integer powers avoid approximate log computation.
        J=F(7,3);left,right=F(1,8),F(1,2)
        for q,b in ((3,0),(2,F(1,3)),(1,F(2,3))):
            power=F(1-q-3*b)
            self.assertEqual(power.denominator,1)
            power=int(power)
            self.assertEqual(J*m.integral_power_interval(power,left,right),
                             J*(left**(2-q-3*b)-right**(2-q-3*b))/(q+3*b-2))
        # At logarithmic threshold each geometric shell has the same log coefficient J.
        self.assertEqual(m.radial_power(4,F(1,3))-1,-1)

    def test_envelope_both_ends(self):
        for q,b in ((0,0),(F(1,2),F(1,4)),(1,F(1,6))):
            near,far=m.envelope_powers(q,b)
            self.assertGreater(near,-1);self.assertLess(far,-1)
            self.assertEqual(far,1-F(q)-3*F(b)-3*(1-F(b)))

    def test_abelian_boundary_residue(self):
        for b in (F(0),F(1,6),F(1,3),F(1,2)):
            c,p12,pk,pt=m.pole_parts(b)
            q0=2-3*b
            self.assertEqual((c,p12,pk,pt),(F(1,4),(2-q0)/3,(5-q0)/3-b,(4+q0)/3))
            for eps in (F(1,16),F(1,64)):
                q=q0-eps
                self.assertEqual(eps*m.coefficient_parts(q,b)[0],F(3,4)/(3+eps))

    def test_invalid_domains_rejected(self):
        with self.assertRaises(ValueError):m.finite(-1,0)
        with self.assertRaises(ValueError):m.alpha(2,0)
        with self.assertRaises(ValueError):m.cutoff_regime(0,1)
        with self.assertRaises(ValueError):m.overlap_integral(0,0,2,1,1)

    def test_height_correlation(self):
        self.assertEqual(m.height_correlation(0,0),F(2,7))
        self.assertEqual(m.height_correlation(1,0),F(7,11))
        for q,b in ((0,0),(1,0),(0,F(1,2))):
            a=(2-F(q)-3*F(b))/3
            self.assertEqual(m.height_correlation(q,b),(2-a-a*a)/(2+a+a*a))

    def test_boundary_gap_collapse(self):
        previous=F(1)
        for n in (4,16,64,256):
            q=2-F(3,n);b=0
            self.assertEqual(m.alpha(q,b),F(1,n))
            mean=m.gap_moment(q,b,1)
            self.assertLess(mean,previous)
            self.assertEqual(mean,F(1,2*n+1))
            previous=mean
        self.assertGreater(m.height_correlation(2-F(3,256),0),F(99,100))

if __name__=='__main__':unittest.main()
