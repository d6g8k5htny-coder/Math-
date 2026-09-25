"""Exact, independent polynomial fixtures; not a stochastic proof checker."""
from fractions import Fraction as F
from math import comb, factorial
import unittest
import contact as c


def monomial_gradient(i, j, x, z):
    return ((i * x**(i-1) * z**j) if i else F(0),
            (j * x**i * z**(j-1)) if j else F(0))


def monomial_pins(i, j, r):
    a = r / 2
    def value(x):
        return x**i if j == 0 else F(0)
    gm = monomial_gradient(i, j, -a, F(0))
    gp = monomial_gradient(i, j, a, F(0))
    return value(-a), gm[0], value(a), gp[0], gm[1], gp[1]


def fixture_value_gradient(x, z, r, b=F(3), k=F(2), q=F(5)):
    # Construct the original function, independently of the transformed formulas.
    value = b-k*r**3/2+2*k*x**3-F(3,2)*k*r*r*x-z*z + q*(x*x-r*r/4)*z/2
    gx = 6*k*x*x-F(3,2)*k*r*r+q*x*z
    gz = -2*z+q*(x*x-r*r/4)/2
    return value, gx, gz


class ContactTests(unittest.TestCase):
    def test_arbitrary_cubic_and_linear_interpolation(self):
        r = F(2,3)
        h = lambda x: 1+2*x+F(3,2)*x*x+F(2,3)*x**3
        hp = lambda x: 2+3*x+2*x*x
        a = r/2
        pins = (h(-a),hp(-a),h(a),hp(a),5-6*a,5+6*a)
        self.assertEqual(c.hermite(r,pins),(F(1),F(2),F(3),F(4),F(5),F(6)))

    def test_original_six_pins(self):
        r=F(1,10); b=F(3); k=F(2)
        self.assertEqual(fixture_value_gradient(-r/2,F(0),r,b,k),(b,F(0),F(0)))
        self.assertEqual(fixture_value_gradient(r/2,F(0),r,b,k),(b-k*r**3,F(0),F(0)))

    def test_actual_hermite_target(self):
        r=F(1,7); b=F(3); k=F(2)
        pins=(b,F(0),b-k*r**3,F(0),F(0),F(0))
        self.assertEqual(c.hermite(r,pins),(b-k*r**3/2,-F(3,2)*k*r*r,F(0),12*k,F(0),F(0)))

    def test_constant_removed(self):
        r=F(1,3)
        self.assertEqual(c.normalized(r,F(2),F(1),monomial_pins(0,0,r),(F(0),F(0))),(F(0),F(0)))

    def test_unconditioned_xz_counterterm_is_essential(self):
        r=F(1,13);u=F(2);w=F(3,5)
        gx,gz=monomial_gradient(1,1,r*u,r*r*w)
        self.assertEqual(c.normalized(r,u,w,monomial_pins(1,1,r),(gx,gz)),(F(0),F(0)))

    def test_axial_quartic_residual(self):
        for r in (F(1,10),F(2,7)):
            for u in (F(-2),F(3,2)):
                gx,gz=monomial_gradient(4,0,r*u,F(0))
                self.assertEqual(c.normalized(r,u,F(0),monomial_pins(4,0,r),(gx,gz)),(4*u*(u*u-F(1,4)),F(0)))

    def test_mixed_cubic_residual(self):
        r=F(1,11);u=F(7,4);w=F(-2,3)
        raw=monomial_gradient(2,1,r*u,r*r*w)
        self.assertEqual(c.normalized(r,u,w,monomial_pins(2,1,r),raw),(2*u*w,u*u-F(1,4)))

    def test_transverse_quadratic_residual(self):
        r=F(1,11);u=F(7,4);w=F(-2,3)
        raw=monomial_gradient(0,2,r*u,r*r*w)
        self.assertEqual(c.normalized(r,u,w,monomial_pins(0,2,r),raw),(F(0),2*w))

    def test_all_degree_six_basis_limits(self):
        # At most degree 12 is enough for exact finite-polynomial extrapolation.
        # The fixtures derive raw gradients directly; they never call limit_rows.
        for i in range(7):
            for j in range(7-i):
                Q=F(24 if (i,j)==(4,0) else 0)
                T=F(2 if (i,j)==(2,1) else 0)
                S=F(2 if (i,j)==(0,2) else 0)
                for u in (F(-2),F(3,2)):
                    for w in (F(0),F(1,3),F(-1,3)):
                        total=[F(0),F(0)]
                        for n in range(1,14):
                            r=F(n,31)
                            raw=monomial_gradient(i,j,r*u,r*r*w)
                            z=c.normalized(r,u,w,monomial_pins(i,j,r),raw)
                            weight=(-1)**(n-1)*comb(13,n)
                            total=[total[t]+weight*z[t] for t in (0,1)]
                        self.assertEqual(tuple(total),c.limit_rows(u,w,Q,T,S),(i,j,u,w))

    def test_contact_minor_uses_random_Q_and_T(self):
        for u in (F(-3),F(-3,2),F(3,2),F(3)):
            rowQ=c.limit_rows(u,F(2,3),F(1),F(0),F(0))
            rowT=c.limit_rows(u,F(2,3),F(0),F(1),F(0))
            determinant=rowQ[0]*rowT[1]-rowT[0]*rowQ[1]
            self.assertEqual(determinant,u*(u*u-F(1,4))**2/12)
            self.assertNotEqual(determinant,0)

    def test_scaled_pin_boundaries_are_excluded(self):
        for u in (F(-1,2),F(1,2),F(0)):
            rowQ=c.limit_rows(u,F(0),F(1),F(0),F(0))
            rowT=c.limit_rows(u,F(0),F(0),F(1),F(0))
            self.assertEqual(rowQ[0]*rowT[1]-rowT[0]*rowQ[1],0)

    def test_density_jacobian_is_five_not_four(self):
        r=F(2,7)
        self.assertEqual(c.density_jacobian(r),r**3*r**2)
        self.assertNotEqual(c.density_jacobian(r),r**4)

    def test_old_unshifted_drift_is_falsified(self):
        r=F(1,10);u=F(2);k=F(1)
        _,gx,_=fixture_value_gradient(r*u,F(0),r,k=k)
        self.assertEqual(gx/r**2,F(45,2))
        self.assertNotEqual(gx/r**2,6*k*u*u)

    def test_bad_radius_rejected(self):
        for r in (F(0),F(-1),True,0.1):
            with self.assertRaises((TypeError,ValueError)):
                c.hermite(r,(F(0),)*6)

    def test_pin_arity_rejected(self):
        with self.assertRaises(ValueError):
            c.hermite(F(1),(F(0),)*5)


if __name__=='__main__':
    unittest.main()
