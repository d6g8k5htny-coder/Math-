from fractions import Fraction as F
import unittest
import elder

class InitialTests(unittest.TestCase):
    def test_selected_mass(self):
        self.assertEqual(elder.moment(0), F(888807,280))
    def test_selected_mean(self):
        self.assertEqual(elder.moment(1)/elder.moment(0), F(1174914407,1440459878))
    def test_selected_second(self):
        self.assertEqual(elder.moment(2)/elder.moment(0), F(63496935353,92189432192))
    def test_outer_not_elder(self):
        self.assertEqual(elder.selection(F(-1), F(6)), 0)
    def test_inner_is_elder(self):
        self.assertEqual(elder.selection(F(-13,23), F(294,529)), 1)
    def test_near_zero_density(self):
        self.assertEqual(elder.small_height_density_coefficient(),F(3328))
    def test_upper_density(self):
        lo,hi=elder.height_density_bounds(F(1))
        self.assertEqual((lo,hi),(F(1312200,296269),F(1312200,296269)))
    def test_new_ratio_exponent(self):
        self.assertEqual(elder.outer_over_elder_tail_exponent(),13)



class GeometryTests(unittest.TestCase):
    def test_full_shape_grid(self):
        self.assertEqual(elder.checks(),893)

    def test_selector_matches_cubic_boundary(self):
        for ip in range(-7,24):
            p=F(ip,16)
            for j in range(1,15):
                e=F(j,15); v=6*(e+p-F(1,2)); u=-p
                if not elder.shape(u,v):continue
                boundary=2*p**3-F(3,2)*p+F(1,2)
                expected=F(1) if p<=F(1,2) or e>boundary else F(1,2) if e==boundary else F(0)
                self.assertEqual(elder.selection(u,v),expected)

    def test_actual_cubic_gradient_height_and_type(self):
        # Directly differentiate the unsheared cubic, independently of selector.
        cases=0
        for p in (F(1,4),F(3,5),F(3,4),F(1),F(5,4)):
            u=-p; b=3-12*u*u;lo,hi=abs(b)/2,3-6*u
            for j in range(1,5):
                v=lo+(hi-lo)*F(j,5)
                for k,a,Z in ((F(1),F(-12),F(1)),(F(3,2),F(4),F(-2))):
                    s=-k*v/Z**2; B=k*b/Z**2; Dc=k*(v-b*u)/Z**3
                    beta=B+a*a/(12*k);c=2*Dc+a*B/(4*k)+a**3/(144*k*k)
                    roots=[(u,v,F(1))]
                    other=elder.companion(u,v)
                    if other and elder.shape(other[0],other[1]):roots.append(other)
                    es=[]
                    for uu,vv,t in roots:
                        z=t*Z;x=uu-a*z/(12*k)
                        gx=6*k*x*x-F(3,2)*k+a*x*z+beta*z*z/2
                        gz=s*z+a*(x*x-F(1,4))/2+beta*x*z+c*z*z/2
                        val=2*k*x**3-F(3,2)*k*x-k/2+s*z*z/2+a*(x*x-F(1,4))*z/2+beta*x*z*z/2+c*z**3/6
                        hxx=12*k*x+a*z;hzz=s+beta*x+c*z;hxz=a*x+beta*z
                        self.assertEqual((gx,gz),(0,0))
                        self.assertEqual(-val/k,elder.height(uu,vv))
                        self.assertTrue(-k<val<0)
                        self.assertLess(hxx*hzz-hxz*hxz,0)
                        es.append(-val/k)
                    if len(es)==2 and es[0]!=es[1]:
                        self.assertEqual(elder.selection(u,v),int(es[0]<es[1]))
                    cases+=1
        self.assertEqual(cases,40)

    def test_degree_drop(self):
        u,v=F(-5,8),F(27,16)
        self.assertTrue(elder.shape(u,v))
        self.assertIsNone(elder.companion(u,v))
        self.assertEqual(elder.selection(u,v),1)

    def test_height_tie_shared(self):
        self.assertEqual(elder.selection(F(-3,4),F(45,16)),F(1,2))

    def test_physical_radius_not_the_selector(self):
        # Existing source falsifier, computed from original coordinates.
        u,v,a,k=F(-3,4),F(14,5),F(-12),F(1)
        uc,vc,tc=elder.companion(u,v)
        r0=(u-a/(12*k))**2+1
        rc=(uc-a*tc/(12*k))**2+tc*tc
        self.assertEqual(r0,F(17,16))
        self.assertEqual(rc,F(3126268865,790959376))
        self.assertLess(abs(tc),1);self.assertGreater(rc,r0)
        self.assertEqual(elder.selection(u,v),0)
        self.assertEqual(elder.selection(uc,vc),1)

    def test_strict_endpoints(self):
        for u,v in ((F(-1),F(9)),(F(-1),F(9,2)),(F(-1,2),F(0))):
            self.assertFalse(elder.shape(u,v))
            with self.assertRaises(ValueError):elder.selection(u,v)


class Dual:
    """Exact independent two-variable differentiation for the square map."""
    def __init__(self,x,dr=0,dz=0):self.x,self.dr,self.dz=F(x),F(dr),F(dz)
    @staticmethod
    def cv(x):return x if isinstance(x,Dual) else Dual(x)
    def __add__(self,o):
        o=self.cv(o);return Dual(self.x+o.x,self.dr+o.dr,self.dz+o.dz)
    __radd__=__add__
    def __neg__(self):return Dual(-self.x,-self.dr,-self.dz)
    def __sub__(self,o):return self+-self.cv(o)
    def __rsub__(self,o):return self.cv(o)+-self
    def __mul__(self,o):
        o=self.cv(o);return Dual(self.x*o.x,self.dr*o.x+self.x*o.dr,self.dz*o.x+self.x*o.dz)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=self.cv(o);return Dual(self.x/o.x,(self.dr*o.x-self.x*o.dr)/o.x**2,(self.dz*o.x-self.x*o.dz)/o.x**2)
    def __pow__(self,n):
        z=Dual(1)
        for _ in range(n):z=z*self
        return z


class SquareTests(unittest.TestCase):
    def test_direct_inner_jacobian(self):
        # Bypass the source's outer density and involution. Differentiate the
        # direct inner root coordinates against the square coordinates.
        for rr in (F(1,5),F(1,3),F(1,2),F(4,5)):
            for zz in (F(1,7),F(2,5),F(3,4)):
                r,z=Dual(rr,1,0),Dual(zz,0,1)
                w=1+2*r*z/(1+r)
                pc=((1+r)*w*w+(1-r))/(4*w)
                u=-pc
                # Derive v_inner = rho^2 v_outer from the shared soft curvature.
                po=((1+r)*w*w-(1-r))/(4*r*w)
                v=r*r*(12*po*po-3)*w/2
                det=u.dr*v.dz-u.dz*v.dr
                self.assertTrue(elder.shape(u.x,v.x))
                self.assertEqual(elder.selection(u.x,v.x),1)
                self.assertEqual(elder.weight(u.x,v.x)*abs(det),elder.square_density(rr,zz))
                eta_elder,eta_other=elder.square_heights(rr,zz)
                self.assertEqual(eta_elder,elder.height(u.x,v.x))
                self.assertTrue(0<eta_elder<eta_other<1)

    def test_radius_bias_is_not_optional(self):
        r,z=F(1,2),F(1,3)
        base=165888*r*z**7*(z+1)**4*(r*z+1)**4*(r*z+r+1)**7/((r+1)**5*(2*r*z+r+1)**9)
        self.assertEqual(elder.square_density(r,z),r**11*base)
        self.assertNotEqual(elder.square_density(r,z),base)

    def test_small_ratio_uniform_corner_controls(self):
        for z in (F(1,100),F(1,3),F(1,2),F(99,100)):
            for r in (F(1,1000),F(1,10000)):
                rat=elder.square_density(r,z)/(165888*r**12*z**7*(z+1)**4)
                self.assertLess(abs(rat-1),20*r)
                inner,outer=elder.square_heights(r,z)
                self.assertLess(abs(inner/r**3-2*z*z*(z+1)),50*r)
                self.assertLess(abs(outer-z*z),20*r)

    def test_tail_constant_positive(self):
        c=elder.constants()['outer_over_elder_ratio_tail_constant']
        self.assertTrue(0<c[0]<c[1])
        self.assertEqual(F(1,13),F(1)/(12+1))


def dense_product(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out


def dense_integral_interpolated(xs,ys,left,right):
    """Independent dense Lagrange integration, used on polynomial strips."""
    out=F(0)
    for i,(x,y) in enumerate(zip(xs,ys)):
        pol=[F(1)];den=F(1)
        for j,z in enumerate(xs):
            if i==j:continue
            pol=dense_product(pol,[-z,F(1)]);den*=x-z
        out+=(y/den)*sum((c*(right**(j+1)-left**(j+1))/F(j+1) for j,c in enumerate(pol)),F(0))
    return out


class DensityTests(unittest.TestCase):
    def test_polynomial_primitive_moments_independent(self):
        # The v integral is degree <=3+j and the resulting p polynomial is
        # degree <=13+3j on an outer strip. Use enough rational interpolation
        # nodes rather than production sparse polynomial arithmetic.
        for moment in range(2):
            total=F(0)
            for left,right,hi_fn,lo_fn in (
                    (F(-1,2),F(1,2),lambda p:3+6*p,lambda p:(3-12*p*p)/2),
                    (F(1,2),F(3,2),lambda p:3+6*p,lambda p:(12*p*p-3)/2)):
                nodes=[left+(right-left)*F(i,13+3*moment) for i in range(14+3*moment)]
                vals=[]
                for p in nodes:
                    lo,hi=lo_fn(p),hi_fn(p);nv=4+moment
                    vs=[lo+(hi-lo)*F(j,nv-1) for j in range(nv)]
                    if lo==hi:vals.append(F(0));continue
                    vals.append(dense_integral_interpolated(vs,[(4*v*v-(3-12*p*p)**2)*((3-12*p*p)+4*p*v)*(F(1,2)-p+v/6)**moment for v in vs],lo,hi))
                total+=dense_integral_interpolated(nodes,vals,left,right)
            self.assertEqual(total,elder.point_moment(moment))

    def test_eta_integrand_factorization(self):
        for x in (F(-2,5),F(-1,7),F(0),F(1,3)):
            for e in (F(1,5),F(2,3),F(4,5)):
                p=x+F(1,2);v=6*(e+x)
                lhs=6*(4*v*v-(3-12*p*p)**2)*((3-12*p*p)+4*p*v)
                rhs=10368*(e-x*x)*(e+x*x+2*x)*(e+2*e*x+x*x)
                self.assertEqual(lhs,rhs)

    def test_density_bounds_are_nested_and_positive(self):
        for e in (F(1,1000),F(1,10),F(1,2),F(9,10)):
            lo,hi=elder.height_density_bounds(e,64)
            l2,h2=elder.height_density_bounds(e,128)
            self.assertTrue(0<lo<=l2<=h2<=hi)
            self.assertLess(hi-lo,F(1,10**12))

    def test_small_height_cubic_density_limit(self):
        expected=F(3328)/elder.moment(0)
        errors=[]
        for e in (F(1,10**4),F(1,10**6),F(1,10**8)):
            lo,hi=elder.height_density_bounds(e,180)
            val=(lo+hi)/(2*e**3)
            errors.append(abs(val-expected))
            self.assertLess(abs(val-expected),100*F(1,10**(len(str(e.denominator))//2)))
        self.assertGreater(errors[0],errors[1]);self.assertGreater(errors[1],errors[2])
        self.assertLess(errors[-1],F(1,1000))

    def test_upper_endpoint(self):
        endpoint=F(1312200,296269)
        lo,hi=elder.height_density_bounds(F(999999,1000000),160)
        self.assertLess(abs((lo+hi)/2-endpoint),F(1,1000))

    def test_unnormalized_moments(self):
        self.assertEqual(elder.moment(1),F(3524743221,1361360))
        self.assertEqual(elder.moment(2),F(190490806059,87127040))
        self.assertTrue(0<elder.moment(2)<elder.moment(1)<elder.moment(0))

    def test_log_interval_constants(self):
        c=elder.constants()
        self.assertEqual(c['elder_to_point_tail_ratio'],(F(296269,657408),)*2)
        lo,hi=c['double_given_extreme_elder']
        self.assertTrue(F(3458,100000)<lo<hi<F(3459,100000))

    def test_density_invalid_inputs(self):
        for e in (True,0.5,'1/2'):
            with self.assertRaises(TypeError):elder.height_density_bounds(e)
        for e in (F(-1),F(2)):
            with self.assertRaises(ValueError):elder.height_density_bounds(e)
        for bits in (1,300,True):
            with self.assertRaises(ValueError):elder.height_density_bounds(F(1,2),bits)

    def test_cli_modes_and_mutants(self):
        import subprocess,sys
        from pathlib import Path
        script=str(Path(elder.__file__).resolve());reference=None
        for flags in (['-B','-S'],['-B','-O','-S']):
            run=subprocess.run([sys.executable,*flags,script],capture_output=True,timeout=35)
            self.assertEqual(run.returncode,0,run.stderr)
            if reference is None:reference=run.stdout
            self.assertEqual(run.stdout,reference);self.assertEqual(run.stderr,b'')
            for name in elder.MUTANTS:
                bad=subprocess.run([sys.executable,*flags,script,'--mutant',name],capture_output=True,timeout=35)
                self.assertEqual(bad.returncode,1,(name,bad.stdout,bad.stderr))
            unknown=subprocess.run([sys.executable,*flags,script,'--mutant','unknown'],capture_output=True,timeout=35)
            self.assertEqual(unknown.returncode,2)

if __name__=='__main__':unittest.main()
