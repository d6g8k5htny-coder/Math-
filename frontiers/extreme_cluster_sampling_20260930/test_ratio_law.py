"""Exact unit-square controls; no Gaussian limit or exact sampling is asserted by tests."""
from fractions import Fraction as F
from math import comb
import unittest
import random
import extremes as e
import ratio_law as r
from test_extremes import Dual

class RatioTests(unittest.TestCase):
    def test_coordinate_companion_ratio(self):
        for rho in (F(1,1000),F(1,4),F(1,2),F(3,4),F(999,1000)):
            for z in (F(1,9),F(1,4),F(1,2),F(3,4),F(8,9)):
                u,v=r.coordinates(rho,z)
                self.assertTrue(e.outer_double(u,v))
                uc,vc,t=e.companion(u,v)
                self.assertEqual(t,-rho)
                self.assertEqual((e.height(u,v),e.height(uc,vc)),r.heights(rho,z))
    def test_jacobian_against_independent_dual_calculation(self):
        count=0
        for i in range(1,9):
            for j in range(1,10):
                rho,z=Dual(F(i,9),1,0),Dual(F(j,10),0,1)
                p=(2*rho*z*z+2*rho*z+rho+2*z+1)/(2*(2*rho*z+rho+1))
                ell=(1+2*rho*z/(1+rho))/2
                u=-p;v=(12*p*p-3)*ell
                jac=u.du*v.dv-u.dv*v.du
                actual=e.shape_weight(u.x,v.x)*abs(jac)
                self.assertEqual(r.density(rho.x,z.x),actual)
                self.assertGreater(actual,0)
                count+=1
        self.assertEqual(count,72)
    def test_small_ratio_integral(self):
        h=sum((F(comb(4,j),8+j) for j in range(5)),F(0))
        self.assertEqual(r.z_normalizer(),h)
        self.assertEqual(h,F(6401,3960))
        self.assertEqual(r.small_ratio_constant(),F(137647104,3972529))
    def test_sampler_acceptance_bounds_and_factorization(self):
        for i in range(1,10):
            for j in range(1,10):
                rho,z=F(i,10),F(j,10)
                a=r.acceptance(rho,z)
                self.assertTrue(0<a<1)
                proposal=2*rho*z**7*(z+1)**4/r.z_normalizer()
                self.assertEqual(proposal*a*r.proposal_mean(),r.density(rho,z)/e.outer_double_mass())
    def test_sampler_mean_matches_tail_coefficient(self):
        self.assertEqual(r.proposal_mean(),r.small_ratio_constant())
    def test_endpoint_density_integral(self):
        # At rho=1 put x=z+1; (z(z+2))^7=(x^2-1)^7.
        rational=F(0)
        for j in range(1,8):
            rational+=F(comb(7,j)*(-1)**(7-j),2*j)*(2**(2*j)-1)
        J=e.outer_double_mass()
        expected=F(81,8)*rational/J, -F(81,8)/J
        self.assertEqual(r.endpoint_density(),expected)
        self.assertEqual(expected,(F(857223,2889112),-F(945,361139)))
    def test_small_ratio_height_mean(self):
        val=sum((F(comb(4,j),10+j) for j in range(5)),F(0))/F(6401,3960)
        self.assertEqual(r.small_ratio_height_mean(),val)
        self.assertEqual(val,F(483876,582491))
    def test_square_boundary_extensions(self):
        self.assertEqual(r.density(0,F(1,2)),0)
        self.assertEqual(r.density(F(1,2),0),0)
        self.assertGreater(r.density(1,F(1,2)),0)
        self.assertEqual(r.heights(F(1,2),1)[0],1)
        self.assertEqual(r.acceptance(0,F(1,2)),1)
    def test_heights_strictly_ordered(self):
        for i in range(1,10):
            for j in range(1,10):
                big,small=r.heights(F(i,10),F(j,10))
                self.assertTrue(0<small<big<1)
                rho,z=F(i,10),F(j,10)
                den=2*rho*z+rho+1
                self.assertEqual(big-small,z*z*(1-rho)*(rho*z+rho+1)**2/den)
                self.assertEqual(1-big,(1-z*z)*(rho*z+rho+1)**2/((rho+1)*den))
    def test_physical_order_is_not_finite_Z_order(self):
        # Exact support example from PR169 comment5902401772, recomputed here.
        u,v,a,k,Z=F(-3,4),F(14,5),F(-12),F(1),F(1)
        uc,vc,t=e.companion(u,v)
        self.assertEqual((uc,vc,t),(F(-20907,28124),F(670215854,247174805),F(-6919,7031)))
        self.assertTrue(e.in_shape(u,v) and e.in_shape(uc,vc))
        x=u-a*Z/(12*k); zc=t*Z; xc=uc-a*zc/(12*k)
        self.assertLess(abs(zc),abs(Z))
        self.assertEqual(x*x+Z*Z,F(17,16))
        self.assertEqual(xc*xc+zc*zc,F(3126268865,790959376))
        self.assertGreater(xc*xc+zc*zc,x*x+Z*Z)
        self.assertEqual(e.height(u,v),F(13,60))
        self.assertEqual(e.height(uc,vc),F(618523783,2966097660))
        self.assertLess(e.height(uc,vc),e.height(u,v))
    def test_invalid_inputs(self):
        for rho,z in ((-1,F(1,2)),(2,F(1,2)),(F(1,2),2),(True,F(1,2)),(0.5,F(1,2))):
            with self.subTest(rho=rho,z=z),self.assertRaises((ValueError,TypeError)):
                r.density(rho,z)
    def test_missing_jacobian_and_wrong_rho_power_reject(self):
        rho,z=F(1,2),F(1,3)
        a=r.acceptance(rho,z)
        density=r.density(rho,z)
        self.assertNotEqual(density,density*(1+rho)/(2*rho))
        self.assertNotEqual(density,165888*rho**2*z**7*(1+z)**4*a)
    def test_positive_near_zero_coefficient(self):
        for z in (F(1,4),F(1,2),F(3,4)):
            # continuous extension of density/rho at rho=0
            coefficient=165888*z**7*(1+z)**4*r.acceptance(0,z)
            self.assertGreater(coefficient,0)
            self.assertEqual(coefficient,165888*z**7*(1+z)**4)

class SamplerTests(unittest.TestCase):
    def test_seeded_reproducibility_and_ranges(self):
        a,b=random.Random(20260930),random.Random(20260930)
        for _ in range(25):
            x,y=r.sample_doublet(a),r.sample_doublet(b)
            self.assertEqual(x,y)
            self.assertTrue(0<x['radius_ratio']<1)
            self.assertTrue(0<x['height_companion']<x['height_maximum']<1)
    def test_exhausted_budget(self):
        class Reject(random.Random):
            def random(self): return 0.999
            def randrange(self,*args): return 0
        with self.assertRaises(RuntimeError):r.sample_doublet(Reject(),max_trials=2)
    def test_bad_budget(self):
        for n in (0,-1,True,0.5):
            with self.subTest(n=n),self.assertRaises(ValueError):r.sample_doublet(max_trials=n)

if __name__=='__main__':unittest.main()
