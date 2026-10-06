"""Exact finite diagnostics, not a proof of the infinite-field limit."""
from fractions import Fraction as F
import itertools
import unittest

try:
    import sign_coefficient as sc
except ModuleNotFoundError:
    sc = None


def integrate_clipped_lines(d, u):
    """Independent piecewise integration; split at both actual zeros."""
    end = max(d, F(0))
    knots = sorted({F(0), end, *[x for x in (d-u, u) if 0 < x < end]})
    total = F(0)
    for lo, hi in zip(knots, knots[1:]):
        mid = (lo+hi)/2
        if d-u-mid > 0 and u-mid > 0:
            total += u*(d-u)*(hi-lo)-d*(hi**2-lo**2)/2+(hi**3-lo**3)/3
    return total


class CoefficientTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(sc, 'implementation has not been supplied')

    def test_integral_against_piecewise_reference(self):
        for d in map(F, range(-3, 8)):
            for u in (F(i, 4) for i in range(21)):
                with self.subTest(d=d, u=u):
                    self.assertEqual(sc.band_integral(d, u), integrate_clipped_lines(d, u))

    def test_exact_examples_and_boundaries(self):
        examples = [(2, 1, F(1,3)), (3,1,F(5,6)), (1,1,0), (0,1,0),
                    (-1,1,0), (1,0,0), (F(3,2),F(1,2),F(5,48))]
        for d,u,value in examples:
            self.assertEqual(sc.band_integral(F(d),F(u)), F(value))
        with self.assertRaises(ValueError):
            sc.band_integral(F(1),F(-1))

    def test_symmetry_and_homogeneity(self):
        for d in (F(1,2),F(1),F(2),F(5)):
            for ratio in (F(0),F(1,5),F(1,2),F(4,5),F(1)):
                u=d*ratio
                self.assertEqual(sc.band_integral(d,u),sc.band_integral(d,d-u))
                for c in (F(1,3),F(2),F(7,2)):
                    self.assertEqual(sc.band_integral(c*d,c*u),c**3*sc.band_integral(d,u))

    def test_positive_box_witness(self):
        for b,d,t in itertools.product((F(1,2),F(5,8),F(3,4)),
                                      (F(1),F(9,8),F(5,4)),
                                      (F(0),F(1,16),F(1,8))):
            self.assertGreaterEqual(d-b*b-t,F(5,16))
            self.assertGreaterEqual(b*b-t,F(1,8))
            self.assertGreaterEqual(sc.band_integral(d,b*b),F(5,1024))

    def test_full_physical_scaling(self):
        values=(F(-2),F(-1),F(0),F(1),F(2))
        for r in (F(1,2),F(1,5)):
            for am,ap,bm,bp,d,t in itertools.product(values,values,(F(0),F(1)),
                                                   (F(0),F(1)),values,
                                                   (F(-1,2),F(0),F(1,2),F(1))):
                w=sc.physical_weight(r,am,ap,bm,bp,r*(t-d),r*t)
                actual = w/r**4 if t>=0 else F(0)
                self.assertEqual(actual,sc.layer_weight(am,ap,bm,bp,d,t))

    def test_layer_support(self):
        for d in (F(-2),F(0),F(1),F(3)):
            for t in (F(-1),F(0),F(1),F(2),F(4)):
                if t<0 or t>max(d,F(0)):
                    self.assertEqual(sc.layer_weight(-1,1,-1,1,d,t),0)

    def test_endpoint_average_difference(self):
        delta=F(13,7)
        for correlation,r in itertools.product((F(-1,2),F(0),F(3,4),F(1)),
                                                (F(1,3),F(2,5))):
            covariance=[[delta,delta*correlation],[delta*correlation,delta]]
            transform=[[F(1,2),F(1,2)],[-1/r,1/r]]
            out=sc.matmul(sc.matmul(transform,covariance),sc.transpose(transform))
            self.assertEqual(out,[[delta*(1+correlation)/2,F(0)],
                                  [F(0),2*delta*(1-correlation)/r**2]])

    def test_exact_pin_drift(self):
        for r,m2,b in itertools.product((F(1,2),F(1,5)),(F(1),F(5,3)),(F(6,5),F(-2))):
            mean_u,mean_d=sc.transverse_means(m2,b,r)
            self.assertEqual(mean_u-r*mean_d/2,-m2*b)
            self.assertEqual(mean_u+r*mean_d/2,-m2*(b-r**3/6))

    def test_actual_contact_regression_in_finite_product_models(self):
        for weights in sc.diagnostic_spectra():
            moments=sc.moments(weights,10)
            for b in (F(6,5),F(-1),F(0)):
                mean,covariance=sc.contact_regression(moments,b)
                m2,m4=moments[2],moments[4];delta=m4-m2*m2
                self.assertGreater(delta,0)
                self.assertEqual(mean,[-m2*b,F(0),F(0)])
                self.assertEqual(covariance,[[delta,0,0],[0,m2*delta,0],[0,0,m2*delta]])

    def test_mixed_derivative_factor_and_width_laws(self):
        for weights in sc.diagnostic_spectra():
            m=sc.moments(weights,10);delta=m[4]-m[2]**2
            laws=sc.contact_laws(m[2],m[4],F(6,5))
            self.assertEqual(laws['variance_q'],delta)
            self.assertEqual(laws['variance_B'],m[2]*delta/4)
            self.assertEqual(laws['variance_D'],4*laws['variance_B'])

    def test_nonproduct_obstruction(self):
        joint={(sx*a,sy*a):F(1,8) for a in (1,2) for sx in (-1,1) for sy in (-1,1)}
        self.assertEqual(sc.residual_cross(joint),F(9,4))
        weights=sc.diagnostic_spectra()[0]
        product={(x,y):p*q for x,p in weights.items() for y,q in weights.items()}
        self.assertEqual(sc.residual_cross(product),0)

    def test_normalizer_power_ledger(self):
        self.assertEqual(sc.power_ledger(),{'transverse_factors':2,'density_variable':1,
            'normalized_numerator':3,'physical_numerator':5,'physical_normalizer':2,
            'probability':3})


if __name__=='__main__':
    unittest.main(verbosity=2)
