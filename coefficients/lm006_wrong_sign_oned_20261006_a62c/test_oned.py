"""Exact/algebraic and numerical sanity controls; not a Lean or field proof."""
from fractions import Fraction as F
from pathlib import Path
import hashlib, importlib.util, math, subprocess, sys, unittest

P = Path(__file__).with_name('oned.py')

class OneDimensionalTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(P.is_file(), 'one-dimensional implementation not supplied')
        spec=importlib.util.spec_from_file_location('oned',P)
        self.m=importlib.util.module_from_spec(spec); spec.loader.exec_module(self.m)

    def test_interval_arithmetic(self):
        m=self.m
        for a,b,c,d in [(-2,1,3,4),(-3,-1,-4,-2),(0,2,1,3)]:
            x,y=m.iv(a,b),m.iv(c,d)
            for u in (F(a),F(a+b,2),F(b)):
                for v in (F(c),F(c+d,2),F(d)):
                    for z,val in [(m.add(x,y),u+v),(m.sub(x,y),u-v),(m.mul(x,y),u*v)]:
                        self.assertLessEqual(z[0],val); self.assertLessEqual(val,z[1])
        for v in (F(1,7),F(-1,7),F(2,3),F(-13,17)):
            z=m.iv(v)
            self.assertLessEqual(z[0],v); self.assertLessEqual(v,z[1])
            self.assertLessEqual(z[1]-z[0],F(1,m.SCALE))
        with self.assertRaises(ValueError): m.div(m.iv(1),m.iv(-1,1))
        with self.assertRaises(TypeError): m.iv(True)

    def test_parent_authentication(self):
        raw=self.m.parent_bytes()
        self.assertEqual(len(raw),7215)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),self.m.PARENT_SHA)
        with self.assertRaises(ValueError): self.m.authenticate(raw+b'\n')
        self.assertEqual(self.m.parent().j(3,1),F(5,6))

    def test_tail_exact_series(self):
        # Independently sum unrounded terms. These narrower exact partial sums
        # must fit inside the wider fixed-point implementation enclosure.
        m=self.m
        c=m.parent().inv_sqrt_2pi()
        for x in (F(0),F(1,2),F(1),F(4),F(8),F(13)):
            term=total=x
            for k in range(1,336):
                term *= -x*x*F(2*k-1,2*k*(2*k+1)); total += term
            lower=F(1,2)-c[1]*(total-term)
            upper=F(1,2)-c[0]*total
            got=m.normal_tail_point(x)
            self.assertLessEqual(got[0],max(0,lower))
            self.assertGreaterEqual(got[1],min(F(1,2),upper))
            self.assertLessEqual(got[1]-got[0],F(1,10**28))

    def test_tail_sanity_and_domain(self):
        for x in (0,F(1,4),1,2,4,8,13):
            lo,hi=self.m.normal_tail_point(F(x)); expected=math.erfc(float(x)/math.sqrt(2))/2
            self.assertLessEqual(float(lo)-1e-15,expected)
            self.assertLessEqual(expected,float(hi)+1e-15)
        for x in (-1,14):
            with self.assertRaises(ValueError): self.m.normal_tail_point(F(x))

    def test_exact_fourth_derivative_algebra(self):
        # Polynomial coefficient maps for h(a), in basis phi(a),phi(2a),T(a),T(2a).
        def trim(p): return {k:v for k,v in p.items() if v}
        def add(p,q):
            r=dict(p)
            for k,v in q.items(): r[k]=r.get(k,F(0))+v
            return trim(r)
        def scale(p,s,shift=0): return trim({k+shift:v*s for k,v in p.items()})
        def derivative(p): return {k-1:k*v for k,v in p.items() if k}
        h=[{0:-F(1,3),2:-F(2,3)},{0:F(1,3),2:F(2,3)},
           {1:F(1),3:F(2,3)},{1:-F(1),3:-F(4,3)}]
        def step(a):
            out=[derivative(p) for p in a]
            out[0]=add(add(out[0],scale(a[0],-1,1)),scale(a[2],-1))
            out[1]=add(add(out[1],scale(a[1],-4,1)),scale(a[3],-2))
            return out
        for _ in range(3): h=step(h)
        self.assertEqual(h,[{1:F(-1)}, {}, {0:F(4)}, {0:F(-8)}])
        h=step(h)
        self.assertEqual(h,[{0:F(-5),2:F(1)},{0:F(16)}, {}, {}])
        self.assertEqual(self.m.derivative_bound(),F(1100))
        self.assertLess(F(4,3)*(F(832,45)+40+135+297+261),1100)

    def test_conditional_formula_against_positive_integral(self):
        # Binary64 midpoint integration is a SANITY SCREEN, not certification.
        m=self.m
        for u in (F(1,8),F(1,2),1,2,4,8):
            got=m.conditional_integral(F(u),m.iv(2))
            s=math.sqrt(2); n=4000; dx=float(u)/n
            h=lambda a:s*math.exp(-a*a/4)/math.sqrt(2*math.pi)-a*math.erfc(a/2)/2
            approx=sum((float(u)-((i+0.5)*dx))*h(float(u)+(i+0.5)*dx) for i in range(n))*dx
            self.assertLessEqual(abs((float(got[0])+float(got[1]))/2-approx),1e-8)
        self.assertEqual(m.conditional_integral(F(0),m.iv(2)),m.iv(0))

    def test_reduction_from_truncated_moments(self):
        # Independent expression: integrate the two polynomial branches of J
        # against moments M0..M3 on [u,2u] and [2u,infinity).
        m=self.m;v=m.iv(2);sd=m.sqrt_iv(v)
        def moments(t):
            x=m.div(t,sd);ph=m.phi(x);tail=m.normal_tail(x)
            return [tail,m.mul(sd,ph),m.mul(v,m.add(m.mul(x,ph),tail)),
                    m.mul(m.mul(v,sd),m.mul(m.add(m.mul(x,x),2),ph))]
        for u in (F(1,4),F(1),F(2),F(4),F(8)):
            a,b=moments(u),moments(2*u);d=[m.sub(x,y) for x,y in zip(a,b)]
            first=m.div(m.add(m.sub(m.mul(6*u,d[2]),d[3]),
                             m.sub(m.mul(4*u**3,d[0]),m.mul(9*u*u,d[1]))),6)
            second=m.sub(m.mul(u*u/2,b[1]),m.mul(2*u**3/3,b[0]))
            separate=m.add(first,second);direct=m.conditional_integral(u,v)
            self.assertLessEqual(max(separate[0],direct[0]),min(separate[1],direct[1]))

    def test_simpson_weights_and_error(self):
        m=self.m
        for n in (2,4,8,16):
            for degree in range(4):
                z=m.simpson(lambda x:m.iv(x**degree),F(3),n)
                target=F(3**(degree+1),degree+1)
                self.assertLessEqual(z[0],target);self.assertLessEqual(target,z[1])
            z=m.simpson(lambda x:m.iv(x**4),F(3),n)
            error=abs(z[1]-F(3**5,5))
            self.assertLessEqual(error,24*3*F(3,n)**4/180+F(1,10**30))
            self.assertEqual(m.simpson_error(n),F(1485,n**4))

    def test_tail_is_present_and_small(self):
        p=self.m.parent().parameters();tail=self.m.omitted_tail(p['variance_D'])
        self.assertGreater(tail,0); self.assertLess(tail,F(1,10**12))
        # It is stricter than ignoring the support condition D>B^2.
        v=p['variance_D'][1]; pdfD=self.m.parent().density(9,p['variance_D'])[1]
        pdfB=self.m.parent().density(3,(p['variance_D'][0]/4,v/4))[1]
        self.assertEqual(tail,(81*v+2*v*v)*pdfD/24 *v*pdfB/6)

    def test_nonzero_integrand_and_scaling(self):
        m=self.m
        for b in (F(1,4),F(1,2),1,F(3,2)):
            z=m.integrand(b,m.iv(2)); self.assertGreater(z[0],0)
            density=m.iv(*m.parent().density(b,(F(1,2),F(1,2))))
            expected=m.mul(2,m.mul(density,m.conditional_integral(b*b,m.iv(2))))
            self.assertEqual(z,expected)
        self.assertEqual(m.integrand(0,m.iv(2)),m.iv(0))
        self.assertGreater(m.conditional_integral(F(1),m.iv(2))[0],F(1,100))

    def test_low_resolution_is_genuine_enclosure(self):
        m=self.m;result=m.enclosure(32)
        self.assertLessEqual(result['coefficient'][0],F(1322,10**6))
        self.assertGreaterEqual(result['coefficient'][1],F(1322,10**6))
        self.assertGreater(result['quadrature_error'],0)
        self.assertLessEqual(result['gamma'][0],result['gamma'][1])

    def test_error_tail_and_quotient_attachment(self):
        m=self.m; r=m.enclosure(8);p=r['parameters']
        self.assertEqual(r['gamma'][0],max(F(0),r['simpson_sum'][0]-r['quadrature_error']))
        self.assertEqual(r['gamma'][1],r['simpson_sum'][1]+r['quadrature_error']+r['tail'])
        self.assertEqual(r['coefficient'],(r['gamma'][0]*p['p0'][0]/p['z0'][1],r['gamma'][1]*p['p0'][1]/p['z0'][0]))
        lower_j=m.parent().cell_bounds(12,13,9,F(169,16))[0]
        lower_tail=F(1,2)*lower_j*m.parent().density(13,p['variance_D'])[0]*m.parent().density(F(13,4),(p['variance_D'][0]/4,p['variance_D'][1]/4))[0]
        self.assertGreater(lower_tail,0);self.assertLess(lower_tail,r['tail'])
        for u,v in [(10,m.iv(2)),(1,m.iv(F(3,2))),(1,m.iv(4))]:
            with self.assertRaises(ValueError):m.conditional_integral(u,v)

    def test_product_derivative_identity(self):
        # d/db(exp(-alpha*b²) * g(b²)); symbolic polynomial coefficients.
        terms={(0,0,0):F(1)}
        for _ in range(4):
            new={}
            def acc(key,value):new[key]=new.get(key,F(0))+value
            for (k,a,j),c in terms.items():
                if k:acc((k-1,a,j),k*c)
                acc((k+1,a,j+1),2*c)
                acc((k+1,a+1,j),-2*c)
            terms={k:v for k,v in new.items() if v}
        expected={(4,4,0):16,(2,3,0):-48,(0,2,0):12,
                  (2,2,1):144,(4,3,1):-64,(0,1,1):-24,
                  (4,2,2):96,(2,1,2):-144,(0,0,2):12,
                  (4,1,3):-64,(2,0,3):48,(4,0,4):16}
        self.assertEqual(terms,expected)

    def test_invalid_resolution(self):
        for n in (True,0,1,3,5000):
            with self.assertRaises((TypeError,ValueError)): self.m.enclosure(n)

    def test_cli(self):
        for flags in (['-B','-S'],['-B','-O','-S']):
            p=subprocess.run([sys.executable,*flags,str(P),'--panels','16'],capture_output=True,timeout=40)
            self.assertEqual(p.returncode,0,p.stderr); self.assertEqual(p.stderr,b'')
        for args in (['--panels','3'],['--bogus']):
            p=subprocess.run([sys.executable,'-B','-S',str(P),*args],capture_output=True,timeout=20)
            self.assertEqual(p.returncode,1 if args[0]=='--panels' else 2)
            if args[0]=='--panels':
                self.assertEqual(p.stderr,b'ONED_FAIL: even panels in [2,2048] required\n')

if __name__=='__main__':unittest.main()
