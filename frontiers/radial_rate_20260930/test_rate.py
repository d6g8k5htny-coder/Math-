from fractions import Fraction as F
import unittest
import rate

class InitialTests(unittest.TestCase):
    def test_shape_mass(self): self.assertEqual(rate.shape_integrals()['I'],F(246528,35))
    def test_shape_u2(self): self.assertEqual(rate.shape_integrals()['U2'],F(240192,35))
    def test_shape_b(self): self.assertEqual(rate.shape_integrals()['B'],F(-428544,7))
    def test_shape_abs_u(self): self.assertEqual(rate.shape_integrals()['ABS_U'],F(5898627,880))
    def test_leading_boundary(self):
        c=rate.tail_series(F(-3,4),F(3,4),F(5,4),{0:F(1)},4)
        self.assertEqual(c[0],2*F(5,4)**11/11)
    def test_second_boundary(self):
        u,A,g=F(-3,4),F(3,4),F(5,4)
        c=rate.tail_series(u,A,g,{0:F(1),2:F(2)},4)
        self.assertEqual(c[2],u*u*g**9*(1+12*A*A)+F(4,13)*g**13)
    def test_even_series(self):
        c=rate.tail_series(F(-3,4),F(3,4),F(5,4),{0:F(1),2:F(2),3:F(7)},6)
        self.assertEqual([c[i] for i in (1,3,5)],[0,0,0])
    def test_signed_first_coefficient(self):
        u,A,g=F(-3,4),F(3,4),F(5,4)
        c=rate.half_series(u,A,g,{0:F(1),2:F(2),3:F(7)},4,1)
        self.assertEqual(c[1],-u*A*g**10)


class ExtendedTests(unittest.TestCase):
    def test_endpoint_equation(self):
        for u in (F(-5,4),F(-1,2),F(1,4)):
            for p in (F(-1,2),F(0),F(1,3)):
                A=2*p/(1-p*p);g=(1+p*p)/(1-p*p);n=8
                for B in rate.endpoints(u,A,g,n):
                    square=rate.smul(B,B,n)
                    for j in range(n+1):
                        value=square[j]-(u*u*square[j-2] if j>=2 else 0)
                        value+=2*u*A*B[j-1] if j>=1 else 0
                        value-=g*g if j==0 else 0
                        self.assertEqual(value,0)
    def test_general_polynomial_parity(self):
        phi={0:F(1),1:F(3),2:F(-5),3:F(7),4:F(2),5:F(-1)}
        got=rate.tail_series(F(-4,3),F(3,4),F(5,4),phi,10)
        self.assertTrue(all(got[j]==0 for j in (1,3,5,7,9)))
    def test_half_reflection(self):
        u,A,g=F(-3,4),F(3,4),F(5,4);phi={0:F(2),2:F(-3),3:F(5)}
        plus=rate.half_series(u,A,g,phi,8,1);minus=rate.half_series(u,A,g,phi,8,-1)
        self.assertEqual(minus,[x*(-1)**j for j,x in enumerate(plus)])
    def test_cubic_density_term_first_enters_at_four(self):
        args=F(-3,4),F(3,4),F(5,4)
        x=rate.tail_series(*args,{0:F(1)},6);y=rate.tail_series(*args,{0:F(1),3:F(5)},6)
        self.assertEqual(x[:4],y[:4]);self.assertNotEqual(x[4],y[4])
    def test_shear_zero_removes_first_signed_bias(self):
        got=rate.half_series(F(-3,4),F(0),F(1),{0:F(1),2:F(3),3:F(5)},6,1)
        self.assertEqual(got[1],0);self.assertNotEqual(got[3],0)
    def test_density_multiplier(self):
        coeff=[F(2),0,F(3),0,F(5)]
        self.assertEqual(rate.density_series(coeff),[F(22),0,F(39),0,F(75)])
    def test_b_integral_relation(self):
        c=rate.shape_integrals();self.assertEqual(c['B'],3*c['I']-12*c['U2'])
    def test_constant_density_decimal_remainder(self):
        from decimal import Decimal,localcontext
        with localcontext() as ctx:
            ctx.prec=70;D=Decimal;u=D('-0.75');A=D('0.75');g=D('1.25')
            c0=2*g**11/11;c2=u*u*g**9*(1+12*A*A)
            vals=[]
            for t in (D(40),D(80),D(160)):
                delta=1/t;disc=(g*g-u*u*delta*delta).sqrt();den=1-u*u*delta*delta
                bp=(-u*A*delta+disc)/den;bm=(-u*A*delta-disc)/den
                J=(bp**11-bm**11)/11
                vals.append(abs((J-c0-c2*delta*delta)/delta**4))
            self.assertTrue(all(x<D(1000) for x in vals))
            self.assertLess(abs(vals[-1]-vals[-2]),D('0.2'))
    def test_tv_crossing_constant(self):
        # The positive density-difference integral up to sqrt(13/11)
        # equals the survival-difference maximum at the same point.
        from decimal import Decimal,localcontext
        with localcontext() as ctx:
            ctx.prec=50;D=Decimal;x=(D(13)/11).sqrt()
            kappa=D(2)/13*(D(11)/13)**(D(11)/2)
            self.assertLess(abs((x**-11-x**-13)-kappa),D('1e-45'))
    def test_invalid_inputs(self):
        for x in (True,0.5,'1/2'):
            with self.assertRaises(TypeError):rate.endpoints(x,F(0),F(1),4)
        for n in (-1,13,True):
            with self.assertRaises(ValueError):rate.endpoints(0,0,1,n)
        with self.assertRaises(ValueError):rate.endpoints(0,1,1,4)
        with self.assertRaises(ValueError):rate.half_series(0,0,1,{0:1},4,0)
        with self.assertRaises(ValueError):rate.tail_series(0,0,1,{-1:1},4)
    def test_cli_modes_and_mutants(self):
        import subprocess,sys
        from pathlib import Path
        script=str(Path(rate.__file__).resolve());reference=None
        for flags in (['-B','-S'],['-B','-O','-S']):
            run=subprocess.run([sys.executable,*flags,script],capture_output=True,timeout=40)
            self.assertEqual(run.returncode,0,run.stderr)
            if reference is None:reference=run.stdout
            self.assertEqual(reference,run.stdout)
            for mutant in rate.MUTANTS:
                bad=subprocess.run([sys.executable,*flags,script,'--mutant',mutant],capture_output=True,timeout=40)
                self.assertEqual(bad.returncode,1,(mutant,bad.stdout,bad.stderr))
            bad=subprocess.run([sys.executable,*flags,script,'--mutant','unknown'],capture_output=True,timeout=40)
            self.assertEqual(bad.returncode,2)

def inv(matrix):
    n=len(matrix);a=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for j in range(n):
        p=next(i for i in range(j,n) if a[i][j]);a[j],a[p]=a[p],a[j]
        pivot=a[j][j];a[j]=[x/pivot for x in a[j]]
        for i in range(n):
            if i!=j:
                val=a[i][j];a[i]=[x-val*y for x,y in zip(a[i],a[j])]
    return [row[n:] for row in a]

class GaussianControlTests(unittest.TestCase):
    def test_exact_aligned_schur_blocks(self):
        for m2,m4,m6 in ((F(1),F(3),F(15)),(F(14,3),F(98,3),F(794,3))):
            moments={0:F(1),2:m2,4:m4,6:m6}
            def cov(a,b):
                c=tuple(x+y for x,y in zip(a,b))
                if any(x%2 for x in c):return F(0)
                return (-1)**(sum(b)+sum(c)//2)*moments[c[0]]*moments[c[1]]
            pins=[(1,0),(0,1),(3,0)];jets=[(2,1),(1,2),(0,3)]
            S=[[cov(x,y) for y in pins] for x in pins];Si=inv(S)
            V=[[cov(x,y) for y in pins] for x in jets]
            R=[[sum(V[i][l]*Si[l][j] for l in range(3)) for j in range(3)] for i in range(3)]
            C=[[cov(jets[i],jets[j])-sum(R[i][l]*V[j][l] for l in range(3)) for j in range(3)] for i in range(3)]
            expected=[m2*(m4-m2*m2),m2*(m4-m2*m2),m6-m4*m4/m2]
            self.assertEqual(C,[[expected[i] if i==j else 0 for j in range(3)] for i in range(3)])
            self.assertEqual([row[2] for row in R],[0,0,0])
            self.assertTrue(all(x>0 for x in expected))
    def test_second_correction_positive_in_aligned_case(self):
        vals=rate.shape_integrals()
        for a in (F(0),F(1),F(-3)):
            for k in (F(1,2),F(1),F(2)):
                vbeta,vc=F(2),F(6);da=-(a*a/(12*vbeta)+a**4/(576*k*k*vc))
                self.assertGreater(vals['U2'],0)
                self.assertGreaterEqual(vals['B']*da,0)

if __name__=='__main__':unittest.main()
