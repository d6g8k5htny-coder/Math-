"""Finite exact-algebra controls for the Cap I4 adapter note; not a continuum or Lean proof."""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from math import factorial
import json
import unittest


def gamma_half(twice_argument):
    """Gamma(t/2) as rational coefficient times pi**(pi_power_twice/2)."""
    if type(twice_argument) is not int or twice_argument <= 0:
        raise ValueError('positive integer twice-argument required')
    if twice_argument % 2 == 0:
        return F(factorial(twice_argument//2-1)), 0
    k=(twice_argument-1)//2
    return F(factorial(2*k),4**k*factorial(k)), 1


def chamber_gaussian(n,s):
    """Exact symbolic G(n,s,1): coefficient, twice its pi exponent."""
    if type(n) is not int or type(s) is not int or n < 1 or s < 0:
        raise ValueError('n>=1 and integer s>=0 required; n=0 is the separate scalar branch')
    numerator, en=gamma_half(n+s)
    denominator, ed=gamma_half(n)
    return numerator/denominator/F(2**n*factorial(n)), n+en-ed


def compositions(total,n):
    if n==1:
        yield (total,)
        return
    for first in range(total+1):
        for rest in compositions(total-first,n-1):
            yield (first,)+rest


def even_coordinate_moment(q):
    return F(factorial(2*q),4**q*factorial(q))


def cartesian_norm_moment(n,q):
    total=F(0)
    for ks in compositions(q,n):
        multinomial=F(factorial(q))
        for k in ks:
            multinomial=multinomial/factorial(k)*even_coordinate_moment(k)
        total+=multinomial
    return total


class AdapterAlgebra(unittest.TestCase):
    def test_chamber_base_and_scalar_exclusion(self):
        self.assertEqual(chamber_gaussian(1,0),(F(1,2),1))
        self.assertEqual(chamber_gaussian(1,1),(F(1,2),0))
        self.assertEqual(chamber_gaussian(2,0),(F(1,8),2))
        self.assertEqual(chamber_gaussian(3,0),(F(1,48),3))
        with self.assertRaises(ValueError):chamber_gaussian(0,0)
        with self.assertRaises(ValueError):chamber_gaussian(2,-1)
    def test_radial_gamma_recurrence(self):
        for n in range(1,9):
            for s in range(25):
                a,pa=chamber_gaussian(n,s)
                b,pb=chamber_gaussian(n,s+2)
                self.assertEqual(pa,pb)
                self.assertEqual(b,F(n+s,2)*a)
    def test_independent_cartesian_expansion(self):
        for n in range(1,6):
            for q in range(7):
                a,pa=chamber_gaussian(n,2*q)
                b,pb=chamber_gaussian(n,0)
                self.assertEqual(pa,pb)
                self.assertEqual(a/b,cartesian_norm_moment(n,q))
    def test_chamber_factor_cannot_be_omitted_or_squared(self):
        actual=chamber_gaussian(2,0)[0]
        self.assertEqual(actual,F(1,8))
        self.assertNotEqual(actual,F(1,4))
        self.assertNotEqual(actual,F(1,16))
    def test_j_plus_lambda_majorant(self):
        for p in range(1,19):
            for j,l in product((F(1),F(2),F(5)),(F(0),F(1,100),F(1),F(4))):
                self.assertLessEqual((j+l)**p,2**(p-1)*(j**p+l**p))
    def test_spectral_prefactor(self):
        for m in range(2,6):
            for k,r,j,l in product((F(1,2),F(2)),(F(1,100),F(1)),(F(1),F(3)),(F(0),F(1,10),F(2))):
                u=j+l;h=k*u
                actual=h*h/F(4)*(l*(l+r*h))**(m-1)
                upper=k*k*(1+k)**(m-1)/4*u**(2*m)
                self.assertLessEqual(actual,upper)
    def test_depth_cutoff_uniform_lower_mark(self):
        for kmin,k0,r,h,u in product((F(1,3),F(1)),(F(1),F(4)),(F(1,100),F(1)),(F(1),F(2)),(F(2),F(4))):
            k=kmin+k0;K=F(2)
            self.assertLessEqual(4/(3*k)*r*h*h,4*K*K/(3*kmin)*r*u*u)
    def test_exact_radius_kernel(self):
        for r,d,e,u in product((F(1,100),F(1,3),F(1)),(F(1),F(3)),(F(1,2),F(2)),(F(1),F(4))):
            a=d*r*u*u;b=e*r*u
            primitive=a**3/3+b*a*a/2
            self.assertEqual(primitive,r**3*(d**3*u**6/3+e*d*d*u**5/2))
            self.assertEqual(r*r*primitive,r**5*(d**3*u**6/3+e*d*d*u**5/2))
    def test_vandermonde_before_extension(self):
        for m in range(2,6):
            for xs in combinations_with_replacement((F(0),F(1,100),F(1,2),F(1)),m):
                delta=F(1)
                for i in range(m):
                    for j in range(i+1,m):delta*=xs[j]-xs[i]
                self.assertLessEqual(delta,xs[-1]**(m*(m-1)//2))
        # The bound need not hold on the enlarged first-coordinate interval.
        self.assertGreater(abs(F(3)-F(1)),F(1))
    def test_residual_marginals_do_not_imply_product_domination(self):
        joint=(F(1)*1+F(4)*4)/2
        product_marginals=((F(1)+4)/2)**2
        self.assertGreater(joint,product_marginals)
    def test_same_weight_and_typed_support(self):
        weights=(F(0),F(2),F(4));q=(F(1,2),F(1,4),F(1,4))
        # good->geometric can fail where the actual weight is zero.
        good=(True,True,False);geom=(False,True,False)
        z=sum(p*w for p,w in zip(q,weights))
        fail_geom=sum(p*w for p,w,g in zip(q,weights,geom) if not g)/z
        fail_good=sum(p*w for p,w,g in zip(q,weights,good) if not g)/z
        self.assertEqual(fail_geom,fail_good)
        self.assertFalse(all(not h or g for h,g in zip(good,geom)))
    def test_uniformity_and_scalar_far_negative_controls(self):
        ratios=[]
        for r in (F(1,2),F(1,4),F(1,8)):
            j=1/r;ratios.append(j**10)
        self.assertTrue(ratios[0]<ratios[1]<ratios[2])
        lam,j,d,r=F(8),F(1),F(1),F(1)
        self.assertLessEqual(lam,2*d*r*j*j+2*d*r*lam*lam)
        self.assertGreater(lam,4*d*r*j*j)
        self.assertGreater(lam,1/(4*d*r))


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(AdapterAlgebra))
    if not result.wasSuccessful():raise SystemExit(1)
    rows=[]
    for m in range(2,6):
        n=m-1;v=m*n//2;p=2*m+6
        rows.append({'m':m,'n':n,'vandermonde_degree':v,'residual_moment':p,
                     'G_n_v_c1':[str(chamber_gaussian(n,v)[0]),chamber_gaussian(n,v)[1]],
                     'G_n_v_plus_p_c1':[str(chamber_gaussian(n,v+p)[0]),chamber_gaussian(n,v+p)[1]]})
    print(json.dumps({'scope':'exact finite algebra; not continuum or Lean verification','methods':result.testsRun,'rows':rows},indent=2))
