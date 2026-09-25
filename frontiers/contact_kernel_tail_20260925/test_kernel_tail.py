"""Finite exact tests; no Gaussian continuum proof or acceptance is inferred."""
from fractions import Fraction as Q
from math import factorial
import unittest
import kernel_tail as m


def polynomial(k,A,q,c,d):
    return {(0,0):-k/2,(3,0):2*k,(1,0):-3*k/2,(0,2):A/2,
            (2,1):q/2,(0,1):-q/8,(1,2):c/2,(0,3):d/6}


def value(p,x,z,dx=0,dz=0):
    return sum((c*Q(factorial(i),factorial(i-dx))*Q(factorial(j),factorial(j-dz))
                *x**(i-dx)*z**(j-dz) for (i,j),c in p.items() if i>=dx and j>=dz),Q(0))


def det_at(p,x,z):
    return value(p,x,z,2,0)*value(p,x,z,0,2)-value(p,x,z,1,1)**2


class TailControls(unittest.TestCase):
    def test_all_original_pins_and_witness_constraints(self):
        for k in (Q(1,2),Q(1),Q(3)):
            for u in (Q(-2),Q(0),Q(2)):
                for v in (Q(-2),Q(-1,3),Q(1,5),Q(2)):
                    for theta,w in ((Q(1,4),Q(-1)),(Q(1,2),Q(-1)),(Q(3,4),Q(-3,2))):
                        A,q,c,d=m.jets(k,u,v,w,theta)
                        p=polynomial(k,A,q,c,d)
                        self.assertEqual(value(p,Q(-1,2),Q(0)),0)
                        self.assertEqual(value(p,Q(1,2),Q(0)),-k)
                        for x,z in ((Q(-1,2),Q(0)),(Q(1,2),Q(0)),(u,v)):
                            self.assertEqual(value(p,x,z,1,0),0)
                            self.assertEqual(value(p,x,z,0,1),0)
                        self.assertEqual(value(p,u,v),-k*theta)

    def test_three_determinants_from_raw_polynomial(self):
        k,u,v,w,theta=Q(2),Q(-2),Q(-1,3),Q(-1),Q(1,3)
        A,q,c,d=m.jets(k,u,v,w,theta);p=polynomial(k,A,q,c,d)
        expected=m.determinant_factors(theta,w)
        for (x,z),f in zip(((Q(-1,2),Q(0)),(Q(1,2),Q(0)),(u,v)),expected):
            self.assertEqual(det_at(p,x,z),9*k*k/v**2*f)

    def test_known_three_hessian_witness(self):
        A,q,c,d=m.jets(1,2,1,-1,Q(1,2))
        self.assertEqual((A,q,c,d),(Q(-3),Q(-30),Q(75),Q(-363,2)))

    def test_saddle_sign_strict_interior(self):
        for t in (Q(1,100),Q(1,4),Q(1,2),Q(99,100)):
            for w in (Q(-4),Q(-1),Q(0),Q(3)):
                self.assertLess(m.determinant_factors(t,w)[2],0)

    def test_endpoint_strictness_not_claimed_at_theta_zero(self):
        self.assertEqual(m.determinant_factors(0,-1)[2],0)

    def test_typing_uses_maximum_and_saddle_both(self):
        self.assertTrue(m.typed( Q(1,2), Q(-1)))
        self.assertFalse(m.typed(Q(1,2),Q(0)))
        self.assertFalse(m.typed(Q(1,2),Q(4)))

    def test_type_rectangle_bounds(self):
        for it in range(1,20):
            t=Q(it,20)
            for iw in range(-80,41):
                w=Q(iw,20)
                if m.typed(t,w):
                    self.assertGreater(w,-3);self.assertLess(w,1)
                    a,b,c=m.determinant_factors(t,w)
                    self.assertLessEqual(a,4);self.assertLessEqual(abs(b),16);self.assertLessEqual(abs(c),17)
                    self.assertLessEqual(a*abs(b*c),1088)

    def test_exact_q_to_w_jacobian_both_signs(self):
        for v in (Q(-2),Q(-1,7),Q(1,3),Q(3)):
            k=Q(3,2);u=Q(2);h=Q(1,17)
            q0=m.jets(k,u,v,-1,Q(1,2))[1]
            q1=m.jets(k,u,v,-1+h,Q(1,2))[1]
            self.assertEqual(abs((q1-q0)/h),m.q_jacobian(k,v))

    def test_combined_kernel_prefactor(self):
        k,v,z0=Q(3,2),Q(-2,3),Q(7)
        derived=24*k/(z0*abs(v)**6)*(9*k*k/v**2)**3*(6*k/abs(v))
        self.assertEqual(m.kernel_prefactor(k,v,z0),derived)
        self.assertEqual(m.kernel_prefactor(1,1,1),104976)

    def test_kernel_prefactor_v_scaling(self):
        self.assertEqual(m.kernel_prefactor(1,Q(1,2),1)/m.kernel_prefactor(1,1,1),2**13)

    def test_kernel_prefactor_k_scaling(self):
        self.assertEqual(m.kernel_prefactor(2,1,1)/m.kernel_prefactor(1,1,1),2**8)

    def test_contact_coercivity_including_c_when_q_zero(self):
        for u in (Q(-2),Q(2)):
            for v in (Q(1,10),Q(-1,7)):
                A,q,c,d=m.jets(1,u,v,2*u,Q(1,2))
                self.assertEqual(q,0)
                self.assertGreater(c*c,0)
                self.assertGreaterEqual(q*q+c*c,m.coercivity(1,u,v))

    def test_general_contact_coercivity(self):
        for u in (Q(-2),Q(3,2),Q(2)):
            for v in (Q(-1,3),Q(1,5),Q(1)):
                for w in (Q(-3),Q(-1),Q(1)):
                    _,q,c,_=m.jets(1,u,v,w,Q(1,2))
                    self.assertGreaterEqual(q*q+c*c,m.coercivity(1,u,v))

    def test_gamma6_polynomial_differential_identity(self):
        coeff=m.gamma6_coefficients()
        # (d/dx - 1) P(x) = -x^5, so d[e^-x P(x)]/dx=-x^5 e^-x.
        observed=[(j+1)*coeff[j+1]-coeff[j] if j<5 else -coeff[j] for j in range(6)]
        self.assertEqual(observed,[0,0,0,0,0,-1])
        self.assertEqual(coeff[0],factorial(5))

    def test_axis_integral_two_sides_and_longitudinal_width(self):
        B,C,c,eps=Q(3),Q(2),Q(5),Q(1,4)
        pref,x=m.axis_tail(B,C,c,eps)
        expected=2*B*C/c**6*sum(Q(factorial(5),factorial(j))*x**j for j in range(6))
        self.assertEqual(pref,expected);self.assertEqual(x,c/eps**2)

    def test_one_side_integral_has_correct_antiderivative(self):
        # Symbolically differentiate (1/(2c^6))exp(-c/e²)P(c/e²).
        for c in (Q(1),Q(3)):
            coeff=m.gamma6_coefficients()
            for eps in (Q(1,5),Q(1,2),Q(2)):
                x=c/eps**2
                P=sum(coeff[j]*x**j for j in range(6))
                dP=sum(j*coeff[j]*x**(j-1) for j in range(1,6))
                derivative_pref=(dP-P)*(-2*c/eps**3)/(2*c**6)
                self.assertEqual(derivative_pref,eps**-13)

    def test_superpolynomial_absorption_order(self):
        for p in (13,14):
            for n in range(10):
                order,C=m.absorption(p,n,Q(2))
                self.assertGreaterEqual(2*order-p,n)
                self.assertEqual(C,Q(factorial(order),2**order))

    def test_monotonicity_radius_for_envelope(self):
        for p in (13,14):
            self.assertEqual(m.monotone_radius_squared(p,Q(3)),Q(6,p))

    def test_invalid_domain_fails(self):
        for args in ((0,2,1,-1,Q(1,2)),(1,2,0,-1,Q(1,2)),(1,2,1,-1,2)):
            with self.assertRaises(ValueError):m.jets(*args)
        with self.assertRaises(ValueError):m.kernel_prefactor(1,1,0)
        with self.assertRaises(TypeError):m.jets(True,2,1,-1,Q(1,2))
        with self.assertRaises(TypeError):m.jets(1.0,2,1,-1,Q(1,2))

    def test_absent_gluing_premise_never_promoted(self):
        report=m.scope()
        self.assertFalse(report['full_annulus_asymptotic_accepted'])
        self.assertFalse(report['probability_lower_bound'])
        self.assertFalse(report['global_RN_closed'])
        self.assertEqual(len(report['required_gluing_inputs']),2)

    def test_count_lower_bound_not_existence_lower_bound(self):
        # N=m^2 with probability m^-5, else0: E N=m^-3, P(N>0)=m^-5.
        for n in (2,4,8,16):
            self.assertEqual(Q(n*n,n**5),Q(1,n**3))
            self.assertLess(Q(1,n**5),Q(1,n**3))

    def test_fixed_cutoff_convergence_is_not_uniform_gluing(self):
        # f_r(v)=1_{r<v<2r}/r: zero eventually at every fixed v>0,
        # yet integral over v is1. This violates the required tail control.
        for r in (Q(1,5),Q(1,11),Q(1,31)):
            self.assertEqual((2*r-r)/r,1)

if __name__=='__main__':unittest.main()
