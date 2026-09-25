"""Finite exact controls; these do not verify the Gaussian continuum application."""
from fractions import Fraction as Q
import math
import unittest
import contact_tools as m

class ContactTests(unittest.TestCase):
    def test_exact_input_contract(self):
        for bad in (True, False, 0.5, '1/2', None):
            with self.assertRaises(TypeError): m.exact(bad)
        self.assertEqual(m.exact(2), Q(2))

    def test_polynomial_arithmetic(self):
        w=m.var(0); t=m.var(1)
        self.assertEqual(m.mul(m.add(w,t),m.add(w,t)),m.add(m.powp(w,2),m.scale(m.mul(w,t),2),m.powp(t,2)))
        self.assertEqual(m.evaluate(m.mul(w,t),Q(2),Q(3)),6)

    def test_type_factor_from_three_shapes(self):
        p=m.type_polynomial()
        for theta in (Q(1,8),Q(1,4),Q(1,2),Q(3,4),Q(7,8)):
            self.assertEqual(m.evaluate(p,-1,theta),64*theta**3)
            self.assertGreater(m.evaluate(p,-1,theta),0)

    def test_type_area(self):
        self.assertEqual(m.integrate_type({(0,0):Q(1)}),Q(2))

    def test_exact_shape_integral(self):
        self.assertEqual(m.integrate_type(m.type_polynomial()),Q(27392,315))

    def test_two_pieces(self):
        a,b=m.integrate_type_pieces(m.type_polynomial())
        self.assertEqual(a,Q(77248,945));self.assertEqual(b,Q(704,135))

    def test_polynomial_differentiation(self):
        w=m.var(0); t=m.var(1)
        self.assertEqual(m.diff(m.powp(w,3),0),m.scale(m.powp(w,2),3))
        self.assertEqual(m.diff(m.mul(w,t),1),w)

    def test_w_jacobian_is_counted_once(self):
        self.assertEqual(m.normalized_prefactor(Q(2)),2916*Q(2)**6)
        self.assertNotEqual(m.normalized_prefactor(Q(2)),2916*Q(2)**8)

    def test_universal_rational_coefficient(self):
        self.assertEqual(m.normalized_prefactor(1)*m.integrate_type(m.type_polynomial()),Q(8875008,35))

    def test_exact_contact_fixture(self):
        q,c,d=m.contact_jets(2,1,1,-1,Q(1,2))
        self.assertEqual((q,c,d),(Q(-30),Q(75),-Q(363,2)))

    def test_critical_constraints(self):
        for u,v,k,w,t in [(2,1,1,-1,Q(1,2)),(-2,Q(-1,2),2,-1,Q(1,3)),(Q(3,2),Q(1,4),Q(1,7),-2,Q(3,4))]:
            q,c,d=m.contact_jets(u,v,k,w,t)
            A=m.transverse_hessian(u,v,k,w,t)
            self.assertEqual(6*k*(u*u-Q(1,4))+q*u*v+c*v*v/2,0)
            self.assertEqual(A*v+q*(u*u-Q(1,4))/2+c*u*v+d*v*v/2,0)
            h=k*(2*u**3-Q(3,2)*u-Q(1,2))+A*v*v/2+q*(u*u-Q(1,4))*v/2+c*u*v*v/2+d*v**3/6
            self.assertEqual(h,-k*t)

    def test_typed_determinant_forms(self):
        u,v,k,w,t=Q(2),Q(1),Q(1),Q(-1),Q(1,2)
        q,c,d=m.contact_jets(u,v,k,w,t);A=m.transverse_hessian(u,v,k,w,t)
        raw=(-6*k*(A-c/2)-q*q/4,6*k*(A+c/2)-q*q/4,(12*k*u+q*v)*(A+c*u+d*v)-(q*u+c*v)**2)
        self.assertEqual(raw,m.contact_determinants(u,v,k,w,t))
        self.assertEqual(raw,(18,-18,-18))

    def test_saddle_side_remainder_identity(self):
        for u,w,t in [(Q(2),Q(-1),Q(1,2)),(Q(3,2),Q(1,2),Q(3,4)),(Q(4),Q(-2),Q(1,4))]:
            R=m.cubic_d_numerator(u,w,t)
            rhs=-2*(u-Q(1,2))**3+3*(u*u-Q(1,4))*(w-1)-2*(1-t)
            self.assertEqual(R,rhs)
            self.assertLessEqual(R,-2*(u-Q(1,2))**3)

    def test_saddle_side_d_lower_bound(self):
        u,v,k,w,t=Q(2),Q(1,10),Q(3,2),Q(-1),Q(1,2)
        d=m.contact_jets(u,v,k,w,t)[2]
        self.assertGreaterEqual(abs(d),12*k*(u-Q(1,2))**3/abs(v)**3)

    def test_directional_inequality_not_exported_to_left(self):
        u=Q(-2);t=Q(1,2);w=Q(-76,45)
        self.assertEqual(m.cubic_d_numerator(u,w,t),0)
        self.assertGreater(m.evaluate(m.type_polynomial(),w,t),0)

    def test_gradient_coercivity(self):
        u,v,k=Q(2),Q(1,5),Q(3,2)
        q,c,_=m.contact_jets(u,v,k,-1,Q(1,2))
        lower=36*k*k*(u*u-Q(1,4))**2/(v*v*(u*u+v*v/4))
        self.assertGreaterEqual(q*q+c*c,lower)

    def test_odd_even_gaussian_jet_covariances(self):
        for even in [(0,0),(2,0),(1,1),(0,2)]:
            for odd in [(1,0),(0,1),(3,0),(2,1),(1,2),(0,3)]:
                self.assertEqual(m.bf_cov(even,odd),0)

    def test_tail_gamma_polynomial_identity(self):
        # (d/dx - 1) sum_{j=0}^5 x^j/j! = -x^5/5!
        p={(i,0):Q(1,math.factorial(i)) for i in range(6)}
        self.assertEqual(m.add(m.diff(p,0),m.scale(p,-1)),{(5,0):-Q(1,120)})

    def test_tail_values(self):
        self.assertGreater(m.axis_tail_integral(1.0,0.5),0)
        self.assertLess(m.axis_tail_integral(1.0,0.2),m.axis_tail_integral(1.0,0.5))
        for c,e in ((0,1),(1,0),(-1,1)):
            with self.assertRaises(ValueError):m.axis_tail_integral(c,e)

    def test_gaussian_moments_symmetric(self):
        moments=m.gaussian_moments(0.7,-1.5,1.5,6)
        for n in (1,3,5):self.assertAlmostEqual(moments[n],0,places=14)
        self.assertGreater(moments[0],moments[2])
        self.assertGreater(moments[2],0)

    def test_gaussian_polynomial_reduction_against_simpson(self):
        coeff=[1.2,-0.7,2.0,0.3,0.4,-0.1,0.02]
        a,mu,lo,hi=0.7,-0.2,-1.3,0.8
        actual=m.gaussian_polynomial_integral(coeff,a,mu,lo,hi)
        def f(x):return sum(c*x**i for i,c in enumerate(coeff))*math.exp(-a*(x-mu)**2)
        n=4000;h=(hi-lo)/n
        expected=h/3*(f(lo)+f(hi)+4*sum(f(lo+h*i) for i in range(1,n,2))+2*sum(f(lo+h*i) for i in range(2,n,2)))
        self.assertAlmostEqual(actual,expected,places=10)

    def test_zero_precision_integral(self):
        self.assertAlmostEqual(m.gaussian_polynomial_integral([1,2,3],0,7,-1,2),15.0,places=12)

    def test_exact_scoped_power_bookkeeping(self):
        self.assertEqual(2+3-6+6-2,3)
        self.assertEqual(-13-1,-14)
        self.assertEqual(6-Q(2,3)+1,Q(19,3))

    def test_claim_scope_metadata(self):
        data=m.results()
        self.assertEqual(data['typed_shape_integral'],'27392/315')
        self.assertFalse(data['independent_analytic_acceptance'])
        self.assertFalse(data['global_rn_closed'])
        self.assertFalse(data['finite_r_small_k_uniformity'])

if __name__=='__main__':unittest.main(verbosity=2)
