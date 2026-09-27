"""Independent finite checks; analytic proofs are in NOTE.md, not in this suite."""
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import unittest
import angular_contact as m


def deriv(poly, axis):
    out={}
    for e,c in poly.items():
        if e[axis]:
            f=list(e);f[axis]-=1;out[tuple(f)]=c*e[axis]
    return out


def evaluate(poly,x,z):
    return sum((c*x**i*z**j for (i,j),c in poly.items()),Q(0))


def raw_poly(k,A,q,c,d):
    return {(0,0):-k/2,(3,0):2*k,(1,0):-3*k/2,(0,2):A/2,
            (2,1):q/2,(0,1):-q/8,(1,2):c/2,(0,3):d/6}


def simpson(f,a,b,n=1000):
    h=(b-a)/n
    return h/3*(f(a)+f(b)+sum((4 if i%2 else 2)*f(a+i*h) for i in range(1,n)))


class AngularContactTests(unittest.TestCase):
    def test_known_pin_compatible_point(self):
        self.assertEqual(m.contact_coordinates(1,2,1,-1,Q(1,2)),
                         {'q':Q(-30),'c':Q(75),'d':Q(-363,2),'A':Q(-3)})
    def test_reject_inexact_inputs(self):
        for bad in (True,0.5,'1',None):
            with self.assertRaises(TypeError):m.exact(bad)
    def test_reject_degenerate_domains(self):
        for args in ((0,2,1,0,Q(1,2)),(1,2,0,0,Q(1,2)),(1,2,1,0,2)):
            with self.assertRaises(ValueError):m.contact_coordinates(*args)
    def test_six_original_pins_and_third_point(self):
        for k in (Q(1,2),Q(2)):
            for u in (Q(-5,4),Q(2)):
                for v in (Q(-1,3),Q(2,5)):
                    for theta in (Q(1,4),Q(1,2),Q(3,4)):
                        params=m.contact_coordinates(k,u,v,-1,theta)
                        p=raw_poly(k,**params)
                        for x,z,height in ((Q(-1,2),0,0),(Q(1,2),0,-k),(u,v,-k*theta)):
                            self.assertEqual(evaluate(p,x,z),height)
                            for axis in (0,1):self.assertEqual(evaluate(deriv(p,axis),x,z),0)
    def test_original_hessians_match_factored_weights(self):
        k,u,v,w,t=Q(3,2),Q(-5,4),Q(1,3),Q(-1),Q(2,5)
        p=raw_poly(k,**m.contact_coordinates(k,u,v,w,t))
        actual=[]
        for x,z in ((Q(-1,2),0),(Q(1,2),0),(u,v)):
            a=evaluate(deriv(deriv(p,0),0),x,z)
            b=evaluate(deriv(deriv(p,0),1),x,z)
            c=evaluate(deriv(deriv(p,1),1),x,z)
            actual.append(a*c-b*b)
        f=m.type_factors(w,t)
        self.assertEqual(actual,[9*k*k/v**2*f[0],-9*k*k/v**2*f[1],-9*k*k/v**2*f[2]])
    def test_type_interval_and_zero_boundary(self):
        for t in (Q(1,10),Q(1,2),Q(9,10)):
            self.assertTrue(all(x>0 for x in m.type_factors(-1,t)))
        self.assertEqual(m.typed_scaled_product(1,1,1),0)
        self.assertEqual(m.typed_scaled_product(1,2,Q(1,2)),0)
    def test_degree_six_polynomial_identity(self):
        for t in (Q(0),Q(1,3),Q(1)):
            coeff=m.type_polynomial(t)
            self.assertEqual(len(coeff),7)
            self.assertEqual(coeff[-1],-1)
            for w in (Q(-3),Q(-4,3),Q(0),Q(1)):
                self.assertEqual(sum(c*w**j for j,c in enumerate(coeff)),math.prod(m.type_factors(w,t)))
    def test_height_parametrization(self):
        u,v,k,c,d=Q(-5,4),Q(2,7),Q(3,2),Q(5),Q(-7)
        q,w,t=m.cd_coordinates(k,u,v,c,d)
        params=m.contact_coordinates(k,u,v,w,t)
        self.assertEqual((params['q'],params['c'],params['d']),(q,c,d))
    def test_cd_change_of_variables_determinant(self):
        k,u,v=Q(2),Q(-5,4),Q(1,3)
        f0=m.cd_coordinates(k,u,v,0,0)
        fc=m.cd_coordinates(k,u,v,1,0)
        fd=m.cd_coordinates(k,u,v,0,1)
        jac=(fc[0]-f0[0])*(fd[2]-f0[2])-(fd[0]-f0[0])*(fc[2]-f0[2])
        self.assertEqual(jac,-v**4/(24*k*u))
    def test_left_channel_is_interior(self):
        for u in (Q(-11,10),Q(-5,4),Q(-7,5)):
            q0,w0,t0=m.left_channel(1,u)
            self.assertGreater(t0,0);self.assertLess(t0,1)
            self.assertTrue(all(z>0 for z in m.type_factors(w0,t0)))
            self.assertEqual(q0,-6*(u*u-Q(1,4))/u)
    def test_left_channel_range_is_not_silently_extended(self):
        for u in (-2,Q(-3,2),-1,1,0):
            with self.assertRaises(ValueError):m.left_channel(1,u)
    def test_left_scaled_triple_product(self):
        for u in (Q(-11,10),Q(-5,4),Q(-7,5)):
            for k in (Q(1,2),Q(2)):
                _,w,t=m.left_channel(k,u)
                D=u*u-Q(1,4)
                self.assertEqual(m.typed_scaled_product(k,w,t),5832*k**6*D**8/u**6)
    def test_right_cubic_jet_barrier(self):
        for u in (Q(3,5),Q(1),Q(2)):
            for t in (Q(0),Q(1,2),Q(1)):
                for w in (Q(-3),Q(-1),Q(1)):
                    p=m.contact_coordinates(1,u,Q(1,3),w,t)
                    self.assertLessEqual(p['d']*Q(1,3)**3,-12*(u-Q(1,2))**3)
    def test_right_barrier_attained_at_boundary(self):
        u=Q(2);p=m.contact_coordinates(1,u,1,1,1)
        self.assertEqual(p['d'],-12*(u-Q(1,2))**3)
        self.assertEqual(m.right_rate(1,u),12*(u-Q(1,2))**6)
    def test_left_rate_exact(self):
        self.assertEqual(m.left_rate(1,Q(-5,4)),Q(3969,400))
    def test_contact_density_power_ledger(self):
        self.assertEqual(m.ledger(),{'contact_prefactor_power':-13,'left_prefactor_power':-8,
                                    'change_to_cd_power':4,'cd_prefactor_power':-2})
    def test_gaussian_square_completion(self):
        u,v=Q(-5,4),Q(1,3);Q0,_,_=m.left_channel(1,u);K=1+v*v/(4*u*u)
        mean=Q0/(2*u*K)
        for c in (Q(-2),Q(0),Q(7)):
            q=Q0/v-c*v/(2*u)
            self.assertEqual(q*q/4+c*c/4,Q0*Q0/(4*v*v)-Q0*Q0/(16*u*u*K)+K*(c-mean)**2/4)
    def test_standard_gaussian_moments(self):
        moments=m.gaussian_moments(-1,1,6)
        self.assertEqual(moments[1],0);self.assertEqual(moments[3],0)
        for j in range(7):
            ref=simpson(lambda x:x**j*math.exp(-x*x/2),-1,1)
            self.assertAlmostEqual(moments[j],ref,places=9)
    def test_truncated_polynomial_reduction(self):
        for theta,precision,mean,lo,hi in ((.4,1.5,-.2,-2,.5),(.8,.7,.3,-2,-.1)):
            coeff=[float(c) for c in m.type_polynomial(Q(str(theta)))]
            value=m.gaussian_polynomial_integral(coeff,precision,mean,lo,hi)
            ref=simpson(lambda w:sum(c*w**j for j,c in enumerate(coeff))*math.exp(-precision*(w-mean)**2/2),lo,hi,2000)
            self.assertAlmostEqual(value,ref,places=8)
    def test_bf_normalizer(self):
        self.assertAlmostEqual(m.bf_z0(0,1),36.0,places=12)
        self.assertGreater(m.bf_z0(1,1),m.bf_z0(-1,1))
    def test_left_amplitude_matches_direct_gaussian_integral(self):
        u=-1.25;k=1;b=0
        q0,w0,t0=map(float,m.left_channel(1,Q(-5,4)))
        T0=float(m.typed_scaled_product(1,Q(w0),Q(t0)))
        self.assertGreater(T0,0, "the interior type weight must be strictly positive")
        direct=T0/(4*math.pi*m.bf_z0(b,k)*abs(u))*math.exp(-b*b/4+q0*q0/(16*u*u))
        self.assertAlmostEqual(math.log(m.left_amplitude(b,k,u)),math.log(direct),places=10)
    def test_correlated_left_gaussian_parameters(self):
        S=[[2,1,0,0],[1,3,1,0],[0,1,4,1],[0,0,1,5]]
        result=m.left_gaussian_parameters(S,[1,2,3,4],Q(-5,4),Q(1,5))
        self.assertEqual(result['variance_a'],2)
        self.assertEqual(result['mean_v_given_a0'],Q(63,50))
        self.assertEqual(result['variance_v_given_a0'],Q(2957,1250))
    def test_correlated_conditional_variances(self):
        S=[[2,1,0,0],[1,3,1,0],[0,1,4,1],[0,0,1,5]]
        self.assertEqual(m.conditional_variance(S,1,[0]),Q(5,2))
        self.assertEqual(m.conditional_variance(S,3,[0,1,2]),Q(85,18))
        self.assertNotEqual(m.conditional_variance(S,1,[0]),Q(S[1][1]))
    def test_covariance_rates_recover_bargmann_fock(self):
        S=[[2,0,0,0],[0,2,0,0],[0,0,2,0],[0,0,0,6]]
        k,u=Q(1),Q(-5,4);Q0,_,_=m.left_channel(k,u)
        self.assertEqual(Q0**2/(2*m.conditional_variance(S,1,[0])),m.left_rate(k,u))
        self.assertEqual(72*k*k*(Q(2)-Q(1,2))**6/m.conditional_variance(S,3,[0,1,2]),m.right_rate(k,2))
    def test_bad_covariance_is_rejected(self):
        for S in ([[1,2],[2,1]],[[1,1],[1,1]],[[1,2],[3,4]]):
            with self.assertRaises(ValueError):m.conditional_variance(S,1,[0])

    def test_nonclaims_preserved(self):
        flags=m.scope_record()
        self.assertFalse(flags['finite_r_axis_uniformity_proved'])
        self.assertFalse(flags['periodic_equals_bargmann_fock'])
        self.assertFalse(flags['independent_acceptance'])
        self.assertFalse(flags['global_elder_bound_proved'])

if __name__=='__main__':unittest.main(verbosity=2)
