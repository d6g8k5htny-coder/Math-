"""Exact algebra controls; these tests do not certify the Gaussian arguments."""
from fractions import Fraction as F
import unittest
import extremes as e

class InitialTests(unittest.TestCase):
    def test_strict_shape(self):
        self.assertTrue(e.in_shape(F(-3,4),F(3)))
    def test_companion_exact(self):
        self.assertEqual(e.companion(F(-1),F(6)),(F(-13,23),F(294,529),F(-7,23)))
    def test_outer_double_mass(self):
        self.assertEqual(e.outer_double_mass(),F(1083417,280))
    def test_point_mass(self):
        self.assertEqual(e.point_moment(0),F(246528,35))
    def test_point_mean(self):
        self.assertEqual(e.point_moment(1)/F(246528,35),F(5771,7062))
    def test_inner_mass(self):
        self.assertEqual(e.inner_moment(0),(F(27066286003,223205220),-F(79298560,4782969)))
    def test_inner_first_moment(self):
        self.assertEqual(e.inner_moment(1),(F(1259212131941593,15982386572880),-F(3186360320,387420489)))
    def test_inner_second_moment(self):
        self.assertEqual(e.inner_moment(2),(F(72706616008642669,1315122095139840),-F(15686696960,3486784401)))
    def test_log_two_lower(self):
        lo,hi=e.log_two_bounds(30)
        self.assertGreater(lo,F(6931471805599453,10**16))
    def test_log_two_upper(self):
        lo,hi=e.log_two_bounds(30)
        self.assertLess(hi,F(6931471805599454,10**16))
        self.assertGreater(hi,lo)


class GeometryTests(unittest.TestCase):
    def test_full_rational_grid(self):
        self.assertEqual(e.finite_checks(),893)
    def test_degree_drop(self):
        self.assertTrue(e.in_shape(F(-5,8),F(27,16)))
        self.assertIsNone(e.companion(F(-5,8),F(27,16)))
        self.assertEqual(e.anchor_weight(F(-5,8),F(27,16)),1)
    def test_equal_radius_doublet(self):
        u,v=F(-3,4),F(45,16)
        self.assertEqual(e.companion(u,v),(u,v,F(-1)))
        self.assertEqual(e.anchor_weight(u,v),F(1,2))
    def test_zero_B_finite_companion_outside_window(self):
        c=e.companion(F(-1,2),F(3))
        self.assertEqual(c,(F(1,2),F(3),F(1)))
        self.assertFalse(e.is_double(F(-1,2),F(3)))
        self.assertEqual(e.anchor_weight(F(-1,2),F(3)),1)
    def test_height_and_type_boundaries_are_open(self):
        for u,v in ((F(-1),F(9)),(F(-1),F(9,2)),(F(-1,2),F(0))):
            self.assertFalse(e.in_shape(u,v))
    def test_invalid_numeric_types(self):
        for x in (True,0.5,'1/2'):
            with self.subTest(x=x),self.assertRaises(TypeError):e.b0(x)
    def test_anchor_rejects_outside_shape(self):
        with self.assertRaises(ValueError):e.anchor_weight(2,1)
    def test_other_root_via_independent_line_conic(self):
        for iu in range(-21,7):
            u=F(iu,16);b=3-12*u*u
            if not -F(3,2)<u<F(1,2) or b==0:continue
            low,high=abs(b)/2,3-6*u
            for j in range(1,8):
                v=low+(high-low)*F(j,8)
                d=v-b*u
                intercept,slope=v/b,-d/b
                lead=6*slope*slope+b/2
                constant=6*intercept*intercept-F(3,2)
                c=e.companion(u,v)
                if lead==0:
                    self.assertIsNone(c)
                else:
                    t=constant/lead
                    self.assertEqual(c,(intercept+slope*t,v*t*t,t))
    def test_height_order_formula(self):
        for p in (F(3,5),F(3,4),F(1),F(5,4)):
            A=12*p*p-3
            high=min(A*p,3+6*p)
            for j in range(1,8):
                v=A/2+(high-A/2)*F(j,8)
                uc,vc,t=e.companion(-p,v)
                ell=v/A
                rhs=2*(ell-p)*(4*p*ell-1)**3/(4*ell*ell-8*p*ell+1)**2
                self.assertEqual(e.height(uc,vc)-e.height(-p,v),rhs)
                self.assertLess(rhs,0)
                self.assertTrue(-1<t<0)
    def test_once_per_cluster_contrasts_uniform_point(self):
        u,v=F(-1),F(6); uc,vc,t=e.companion(u,v)
        self.assertEqual(e.anchor_weight(u,v),1)
        self.assertEqual(e.anchor_weight(uc,vc),0)
        self.assertNotEqual(e.height(u,v),e.height(uc,vc))


class Dual:
    """Independent exact two-variable automatic differentiation for Jacobian tests."""
    def __init__(self,value,du=0,dv=0):self.x,self.du,self.dv=F(value),F(du),F(dv)
    @staticmethod
    def cast(x):return x if isinstance(x,Dual) else Dual(x)
    def __add__(self,other):
        o=self.cast(other);return Dual(self.x+o.x,self.du+o.du,self.dv+o.dv)
    __radd__=__add__
    def __neg__(self):return Dual(-self.x,-self.du,-self.dv)
    def __sub__(self,o):return self+-self.cast(o)
    def __rsub__(self,o):return self.cast(o)+-self
    def __mul__(self,other):
        o=self.cast(other)
        return Dual(self.x*o.x,self.du*o.x+self.x*o.du,self.dv*o.x+self.x*o.dv)
    __rmul__=__mul__
    def __truediv__(self,other):
        o=self.cast(other)
        return Dual(self.x/o.x,(self.du*o.x-self.x*o.du)/o.x**2,(self.dv*o.x-self.x*o.dv)/o.x**2)
    def __pow__(self,n):
        out=Dual(1)
        for _ in range(n):out=out*self
        return out


class JacobianTests(unittest.TestCase):
    def test_weighted_involution_jacobian(self):
        cases=0
        for p in (F(3,5),F(3,4),F(1),F(5,4)):
            A=12*p*p-3
            for j in range(1,9):
                val=A/2+(min(A*p,3+6*p)-A/2)*F(j,10)
                u,v=Dual(-p,1,0),Dual(val,0,1)
                b=3-12*u*u;den=4*v*v-8*b*u*v+b*b
                t=(4*v*v-b*b)/den
                uc=(2*b*v-u*(4*v*v+b*b))/den;vc=v*t*t
                jac=uc.du*vc.dv-uc.dv*vc.du
                self.assertEqual(e.shape_weight(uc.x,vc.x)*abs(jac),e.shape_weight(u.x,v.x)*abs(t.x)**11)
                cases+=1
        self.assertEqual(cases,32)


def lagrange_integral(xs,ys,left,right):
    """Independent small dense polynomial interpolation, no production helpers."""
    total=F(0)
    for i,(x,y) in enumerate(zip(xs,ys)):
        pol=[F(1)];den=F(1)
        for j,z in enumerate(xs):
            if i==j:continue
            new=[F(0)]*(len(pol)+1)
            for k,c in enumerate(pol):new[k]-=z*c;new[k+1]+=c
            pol=new;den*=x-z
        integ=sum((c*(right**(k+1)-left**(k+1))/F(k+1) for k,c in enumerate(pol)),F(0))
        total+=y*integ/den
    return total


class IntegralTests(unittest.TestCase):
    def test_point_second_moment(self):
        self.assertEqual(e.point_moment(2)/e.point_moment(0),F(2440,3531))
    def test_laurent_certificate_against_interpolation(self):
        for y in (F(1,3),F(1,2),F(2,3),F(3,4)):
            p=(4*y*y+y+4)/(18*y);A=12*p*p-3
            lo=A*p;hi=4*(1-y)**2*(y+2)/(9*y*y)
            self.assertLess(lo,hi)
            H=lambda v:-2*v*v+(36*p*p-12*p-3)*v-72*p**3+36*p*p+18*p-9
            self.assertEqual(H(hi),0)
            for moment in range(4):
                n=moment+4
                xs=[lo+(hi-lo)*F(i,n-1) for i in range(n)]
                ys=[e.shape_weight(-p,v)*e.height(-p,v)**moment for v in xs]
                expected=lagrange_integral(xs,ys,lo,hi)*F(2,9)*(1/y**2-1)
                self.assertEqual(e.evaluate(e.inner_certificate(moment),y),expected)
    def test_theta_exact_affine_form(self):
        a,b=e.inner_moment(0);I=e.point_moment(0)
        self.assertEqual(1-a/I,F(1545114756173,1572181042176))
        self.assertEqual(-b/I,F(10841600,4605999147))
    def test_height_moment_order_rejected(self):
        for n in (-1,13,True):
            with self.assertRaises(ValueError):e.inner_moment(n)
    def test_laurent_operations(self):
        a={-1:F(2),1:F(3)};b={0:F(4),2:F(5)}
        for x in (F(1,3),F(2),F(5)):
            self.assertEqual(e.evaluate(e.multiply(a,b),x),e.evaluate(a,x)*e.evaluate(b,x))
            self.assertEqual(e.evaluate(e.power(a,4),x),e.evaluate(a,x)**4)
    def test_negative_laurent_not_ordinary_integral(self):
        with self.assertRaises(ValueError):e.integrate_polynomial({-1:F(1)},F(1),F(2))
    def test_no_extra_normalizer_in_ratios(self):
        I=e.point_moment(0);d=e.affine_bounds(e.inner_moment(0),e.log_two_bounds())[0]
        for c in (F(1,100),F(1),F(17)):
            self.assertEqual(c*(I-d)/(c*I),(I-d)/I)


class IntervalTests(unittest.TestCase):
    def test_log_nested(self):
        for n in range(1,12):
            lo,hi=e.log_two_bounds(n);lo2,hi2=e.log_two_bounds(n+1)
            self.assertLess(lo,lo2);self.assertLess(hi2,hi);self.assertLess(lo2,hi2)
    def test_log_bad_order(self):
        for n in (0,-1,True,F(3,2)):
            with self.assertRaises(ValueError):e.log_two_bounds(n)
    def test_certified_ratios(self):
        c=e.certified_constants()
        checks={'maximum_to_point_tail_ratio':(F(984415773209943375,10**18),F(984415773209943376,10**18)),
                'double_cluster_given_extreme':(F(558034234065747870,10**18),F(558034234065747871,10**18)),
                'two_exceedances_given_extreme':(F(15830939745347846,10**18),F(15830939745347847,10**18))}
        for key,(lo,hi) in checks.items():
            self.assertLess(lo,c[key][0]);self.assertLess(c[key][1],hi)
    def test_outward_decimal_rounding(self):
        for low,high in ((F(1,3),F(2,3)),(F(-2,3),F(-1,3))):
            d=e.decimal_bounds((low,high),12)
            self.assertLessEqual(F(d['lower']),low)
            self.assertGreaterEqual(F(d['upper']),high)
    def test_positive_division_rejects_zero(self):
        with self.assertRaises(ValueError):e.divide_positive((F(1),F(2)),(F(0),F(1)))
    def test_affine_negative_log_coefficient(self):
        lo,hi=e.affine_bounds((F(1),F(-2)),(F(1,2),F(3,4)))
        self.assertEqual((lo,hi),(F(-1,2),F(0)))
    def test_exceedance_identity_enclosed(self):
        c=e.certified_constants();mean=c['mean_exceedance_count'];p=c['two_exceedances_given_extreme']
        self.assertLessEqual(mean[0],1+p[1]);self.assertGreaterEqual(mean[1],1+p[0])

if __name__=='__main__':unittest.main()
