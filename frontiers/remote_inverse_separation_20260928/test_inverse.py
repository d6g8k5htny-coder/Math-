"""Exact finite controls; the continuum argument is in PROOF.md."""
from fractions import Fraction as F
import unittest
import inverse as m

class InverseTests(unittest.TestCase):
    def test_gradient_only_density_jacobian(self):
        for d in range(2,10):
            self.assertEqual(m.gradient_density_power(d),-d)

    def test_radial_power_independent_of_dimension(self):
        for d in range(2,10):
            self.assertEqual(m.radial_power(d),1)

    def test_microscopic_envelope_domain(self):
        for p in (F(-7,4), F(-1), F(0), F(1,2)):
            self.assertEqual(m.envelope_integral(p),1/(p+2)+1/(1-p))
        for p in (F(-3),F(-2),F(1),F(2)):
            with self.assertRaises(ValueError):m.envelope_integral(p)

    def test_integrated_overlap_coefficient(self):
        for p in (F(-7,4),F(-1),F(0),F(1,2),F(2)):
            self.assertEqual(m.overlap_coefficient(p),1/(p+2)-1/(p+5))
        self.assertEqual(m.overlap_coefficient(F(0)),F(3,10))
        with self.assertRaises(ValueError):m.overlap_coefficient(F(-2))

    def test_inverse_endpoint_is_not_finite(self):
        for q in (F(0),F(1),F(199,100)):
            self.assertTrue(m.moment_finite(-q))
        for q in (F(2),F(3),F(10)):
            self.assertFalse(m.moment_finite(-q))

    def test_fixed_r_cutoff_logarithm(self):
        self.assertEqual(m.inverse_cutoff(2,F(1,100),F(1,2)),
                         {'kind':'log','ratio':F(50),'coefficient':F(1)})

    def test_fixed_r_cutoff_powers(self):
        lo,hi=F(1,100),F(1,2)
        self.assertEqual(m.inverse_cutoff(0,lo,hi),(hi*hi-lo*lo)/2)
        self.assertEqual(m.inverse_cutoff(1,lo,hi),hi-lo)
        self.assertEqual(m.inverse_cutoff(3,lo,hi),1/lo-1/hi)
        self.assertEqual(m.inverse_cutoff(4,lo,hi),(lo**-2-hi**-2)/2)
        with self.assertRaises(ValueError):m.inverse_cutoff(3,F(0),hi)

    def test_small_separation_cdf_has_half(self):
        self.assertEqual(m.small_cdf_coefficient(F(7),F(3)),F(7,6))

    def test_exact_polynomial_fold_data(self):
        for d in (2,3,4):
            for delta in (F(1,3),F(1,11)):
                for T in (F(-5),F(7,3)):
                    transverse=[F((-1)**i*(i+1)) for i in range(d-1)]
                    detA=F(1)
                    for a in transverse:detA*=a
                    result=m.fold_data(delta,T,transverse)
                    self.assertEqual(result['gradients'],([F(0)]*d,[F(0)]*d))
                    self.assertEqual(result['height_difference'],-T*delta**3/12)
                    self.assertEqual(result['determinants'],(-T*delta*detA/2,T*delta*detA/2))
                    self.assertEqual(result['absolute_product'],delta**2*T**2*detA**2/4)

    def test_t_to_T_and_coefficient_conversion(self):
        self.assertEqual(36*F(1,12)**2,F(1,4))
        self.assertEqual(108/F(12)**2,F(3,4))
        self.assertEqual(m.height_width_power(),3)

    def test_negative_moment_scaling(self):
        for q in (F(1,2),F(1),F(3,2)):
            self.assertEqual(m.microscopic_power(-q),5-q)
            self.assertEqual(q+m.microscopic_power(-q)-m.microscopic_power(0),0)
            self.assertGreater(6-m.microscopic_power(-q),0)

    def test_probability_size_bias_not_event_sampling(self):
        # P(N=2)=1/4, P(N=3)=1/4: pair weighting differs from event weighting.
        self.assertEqual(m.pair_weight(2),2)
        self.assertEqual(m.pair_weight(3),6)
        self.assertEqual(F(1,4)*m.pair_weight(2)/(F(1,4)*m.pair_weight(2)+F(1,4)*m.pair_weight(3)),F(1,4))
        self.assertNotEqual(F(1,4),F(1,2))

if __name__=='__main__':unittest.main()
