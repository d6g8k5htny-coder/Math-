"""Finite controls for the enclosure implementation; not nonauthor proof review."""
import unittest
from fractions import Fraction as Q
from math import factorial
import coefficient as c


class ExactArithmetic(unittest.TestCase):
    def test_reject_float(self):
        with self.assertRaises(TypeError): c.I(0.1)
    def test_reversed(self):
        with self.assertRaises(ValueError): c.I(2,1)
    def test_add(self):
        self.assertTrue((c.I(Q(1,3))+c.I(Q(2,3))).contains(1))
    def test_signed_multiplication(self):
        a=c.I(-2,3)*c.I(-4,5)
        self.assertEqual((a.lo,a.hi),(Q(-12),Q(15)))
    def test_division_zero(self):
        with self.assertRaises(ValueError): c.I(-1,1).inv()
    def test_inverse(self):
        self.assertTrue(c.I(Q(3,7)).inv().contains(Q(7,3)))
    def test_negative_inverse(self):
        a=c.I(-2,-1).inv()
        self.assertEqual((a.lo,a.hi),(Q(-1),Q(-1,2)))
    def test_roots(self):
        for n in (2,3,4):
            for a in range(101):
                r=c.integer_root(a,n)
                self.assertLessEqual(r**n,a)
                self.assertGreater((r+1)**n,a)
    def test_root_interval(self):
        a=c.root(c.I(2),2)
        self.assertLessEqual(a.lo*a.lo,2)
        self.assertGreaterEqual(a.hi*a.hi,2)
    def test_atan_remainder(self):
        a=c.atan_small(Q(1,5),2)
        self.assertEqual(a.lo,c.floor_grid(Q(1,5)-Q(1,375)))
        self.assertGreater(a.hi,a.lo)
    def test_pi_bracket(self):
        a=c.pi_interval()
        self.assertGreater(a.lo,Q('3.14159265358979323846264338327950288419716939937510'))
        self.assertLess(a.hi,Q('3.14159265358979323846264338327950288419716939937511'))
    def test_exp_zero(self):
        self.assertTrue(c.exp_point(Q(0)).contains(1))
    def test_log_one(self):
        self.assertTrue(c.log_point(Q(1)).contains(0))
    def test_log_exp(self):
        for q in (Q(1,7),Q(2),Q(17),Q(199,6)):
            self.assertTrue(c.exp_interval(c.log_point(q)).contains(q))
    def test_gamma_width(self):
        self.assertLess(c.gamma_seven_sixths().width,Q(1,10**28))
    def test_gamma_bracket(self):
        a=c.gamma_seven_sixths()
        self.assertGreater(a.lo,Q('0.92771933363003920070'))
        self.assertLess(a.hi,Q('0.92771933363003920071'))


class Mathematics(unittest.TestCase):
    def test_scalar_cone(self):
        self.assertTrue(c.cone_moment(2).contains(Q(4,3)))
    def test_matrix_cone(self):
        # Equivalent independent algebra: (3s^4-4s^2+8-8/sqrt(1+s^2))/2.
        v=c.I(Q(5,3))
        other=(3*v*v-4*v+8-8/c.root(1+v,2))/2
        direct=c.cone_moment(3)
        self.assertLessEqual(direct.lo,other.hi)
        self.assertLessEqual(other.lo,direct.hi)
    def test_transverse_covariance(self):
        var=Q(3)-Q(1,3)
        cov=Q(1)-Q(1,3)
        self.assertEqual((var+cov)/2,Q(5,3))
        self.assertEqual((var-cov)/2,1)
    def test_odd_block_minimum(self):
        # C - I/3 positive definite in the only nontrivial odd 2x2 block.
        self.assertEqual((1-Q(1,3))*(15-Q(1,3))-9,Q(7,9))
    def test_image_constant(self):
        self.assertEqual(c.image_ledger()['image_constant'],21175738586478)
    def test_image_exponential(self):
        self.assertTrue(c.image_ledger()['exp_lower_gt_10'])
        self.assertLess(Q(512,10**375),Q(1,2))
    def test_covariance_and_density_bounds(self):
        self.assertTrue(c.image_ledger()['relative_below_eps'])
        self.assertTrue(c.image_ledger()['density_comparison_below_reported'])
    def test_parameter_dimension_bounds(self):
        for d in (2,3):
            m=d-1; n=m*(m+1)//2
            a=Q(m)+Q(2,3)+Q(n,2); b=Q(d)+Q(n,2)
            self.assertLess(a+2*b,14)
            self.assertLess(2*a+b,13)
    def test_public_d2_interval(self):
        a=c.side24_coefficient(2)
        self.assertGreater(a.lo,Q('0.07340691930603427103'))
        self.assertLess(a.hi,Q('0.07340691930603427104'))
    def test_public_d3_interval(self):
        a=c.side24_coefficient(3)
        self.assertGreater(a.lo,Q('0.04177593184059834334'))
        self.assertLess(a.hi,Q('0.04177593184059834335'))
    def test_side_interval_contains_reference(self):
        for d in (2,3):
            a=c.side24_coefficient(d); b=c.reference_coefficient(d)
            self.assertLessEqual(a.lo,b.lo)
            self.assertGreaterEqual(a.hi,b.hi)
    def test_dimension_refusal(self):
        for d in (1,4):
            with self.assertRaises(ValueError): c.reference_coefficient(d)
    def test_report_no_acceptance(self):
        self.assertIs(c.report()['scientific_acceptance'],False)
    def test_decimal_outward(self):
        self.assertEqual(c.decimals(c.I(Q(1,3)),3),{'lower':'0.333','upper':'0.334'})


if __name__=='__main__':
    unittest.main()
