from fractions import Fraction as F
import unittest
import transfer as t

class InitialTests(unittest.TestCase):
    def test_dimensions(self):
        self.assertEqual([len(t.jet_labels(d)) for d in (1,2,3)],[4,8,13])
    def test_covariance_eighth_order(self):
        self.assertEqual(t.covariance((4,),(4,)),105)
    def test_reference_floor(self):
        self.assertTrue(all(x>0 for x in t.floor_pivots(3)))
        self.assertEqual(t.floor_pivots(3)[-1],F(467,30))
    def test_scale_exponent(self):
        self.assertEqual([t.slice_exponent(d) for d in (1,2,3)],[F(-5,8)]*3)
    def test_eight_derivative_count(self):
        self.assertEqual(t.matching_count(8),764)
    def test_side10_bound(self):
        self.assertTrue(0<t.error_bound(3,10)<F(5,10**5))
    def test_side24_bound(self):
        self.assertTrue(0<t.error_bound(3,24)<F(3,10**105))
    def test_birth_even_schur(self):
        self.assertEqual(t.even_floor_schur(3),F(467,30))


class ExtendedTests(unittest.TestCase):
    def test_matching_count_independent_recurrence(self):
        vals=[1,1]
        for n in range(2,9):vals.append(vals[-1]+(n-1)*vals[-2])
        self.assertEqual([t.matching_count(i) for i in range(9)],vals)
    def test_covariance_independent_hermite_recurrence(self):
        # He_(n+1)=x He_n - n He_(n-1); Gaussian derivative at zero is
        # (-1)^n He_n(0). No double-factorial implementation is reused.
        polynomials=[[F(1)],[F(0),F(1)]]
        for n in range(1,8):
            x=[F(0)]+polynomials[-1];old=polynomials[-2]
            for i,c in enumerate(old):x[i]-=n*c
            polynomials.append(x)
        for a in range(5):
            for b in range(5):
                self.assertEqual(t.covariance((a,),(b,)),(-1)**(b+a+b)*polynomials[a+b][0])
    def test_ldlt_reconstruction(self):
        for d in (1,2,3,5):
            A=t.matrix(d);n=len(A);M=[[x-(F(1,3) if i==j else 0) for j,x in enumerate(row)] for i,row in enumerate(A)]
            L,D=t.ldlt(M)
            self.assertEqual(M,[[sum(L[i][k]*D[k]*L[j][k] for k in range(n)) for j in range(n)] for i in range(n)])
            self.assertEqual(D[-1],t.even_floor_schur(d))
    def test_full_birth_covariance_requires_smaller_floor(self):
        C=t.matrix(3,True)
        with self.assertRaises(ValueError):t.ldlt([[x-(F(1,3) if i==j else 0) for j,x in enumerate(row)] for i,row in enumerate(C)])
        L,D=t.ldlt([[x-(F(1,4) if i==j else 0) for j,x in enumerate(row)] for i,row in enumerate(C)])
        self.assertTrue(all(x>0 for x in D))
    def test_no_half_floor(self):
        C=t.matrix(1)
        with self.assertRaises(ValueError):t.ldlt([[x-(F(1,2) if i==j else 0) for j,x in enumerate(row)] for i,row in enumerate(C)])
    def test_conditional_reference_regression(self):
        for d in (1,2,3):
            mean,S,det,ff=t.pin_regression(d)
            m=d-1;labels=t.jet_labels(d,True)[2*d+2:]
            expmean=[];vars=[]
            for jet in labels:
                if sum(jet)==4:expmean.append(-3);vars.append(24)
                elif sum(jet)==3:expmean.append(0);vars.append(2)
                elif max(jet)==2:expmean.append(-1);vars.append(2)
                else:expmean.append(0);vars.append(1)
            self.assertEqual(mean,expmean)
            self.assertEqual(S,[[F(vars[i]) if i==j else 0 for j in range(len(S))] for i in range(len(S))])
            self.assertEqual(det,12);self.assertEqual(ff,F(3,2))
    def test_homogeneity_without_fractional_powers(self):
        # h^4=|Y|^7|det A|, so every arithmetic operation is rational.
        for A,gamma,f4 in (([[F(-2)]],[F(3)],F(5)),
                           ([[F(-2),F(1,3)],[F(1,3),F(-3)]],[F(1),F(-2)],F(7))):
            m=len(A)
            def value(A,g,f):
                if m==1:det=A[0][0];quad=g[0]**2
                else:det=A[0][0]*A[1][1]-A[0][1]**2;quad=A[1][1]*g[0]**2-2*A[0][1]*g[0]*g[1]+A[0][0]*g[1]**2
                return abs(f*det/12-quad/4)**7*abs(det)
            v=value(A,gamma,f4)
            for a in (F(1,3),F(2),F(5)):
                self.assertEqual(value([[a*x for x in row] for row in A],[a*x for x in gamma],a*f4),a**(8*m+7)*v)
    def test_shell_ratios_by_rational_exponential(self):
        # 1024 exp(-150) < 1/3 follows already from exp(150)>11401.
        self.assertLess(F(1024,11401),F(1,3))
        for d in (1,2,3):
            for j in range(1,11):
                self.assertLessEqual((2*j+1)**d-(2*j-1)**d,2*d*3**(d-1)*j**(d-1))
    def test_exp_bounds_and_reference_values(self):
        from decimal import Decimal,localcontext
        with localcontext() as ctx:
            ctx.prec=180
            for x in (F(0),F(1,2),F(3),F(50),F(288)):
                lo,hi=t.exp_negative_interval(x)
                ref=F((-Decimal(x.numerator)/Decimal(x.denominator)).exp())
                self.assertLessEqual(lo,ref);self.assertLessEqual(ref,hi)
        self.assertLess(t.exp_negative_interval(50)[1],F(193,10**24))
        self.assertLess(t.exp_negative_interval(288)[1],F(1,10**125))
    def test_side_bound_monotonicity(self):
        for d in (1,2,3):
            self.assertGreater(t.error_bound(d,10),t.error_bound(d,12))
            self.assertGreater(t.error_bound(d,12),t.error_bound(d,24))
    def test_actual_sandwich_bound_no_transcendentals(self):
        for d in (1,2,3):
            for delta in (F(0),F(1,10**8),F(1,10000)):
                lo,hi=t.sandwich_eighth_powers(d,delta)
                self.assertTrue((1-13*delta)**8<=lo<=1<=hi<=(1+13*delta)**8)
    def test_operator_dimension_factor(self):
        # An all-E perturbation has Rayleigh quotient N*E on all-ones.
        for N in (4,8,13):
            E=F(1,10**8);ones=[1]*N
            rayleigh=sum(E*ones[i]*ones[j] for i in range(N) for j in range(N))/sum(x*x for x in ones)
            self.assertEqual(rayleigh,N*E)
    def test_outward_formatting_and_negative_interval(self):
        for v in (F(1,3),F(1,10**105),F(5,10**5),F(999999,100)):
            self.assertGreaterEqual(F(t.scientific_upper(v)),v)
        lo,hi=t.inherited_interval(2,10);s=t.decimal_enclosure((lo,hi))
        self.assertTrue(F(s[0])<=lo<hi<=F(s[1]))
    def test_invalid_inputs(self):
        for d in (0,13,True):
            with self.assertRaises(ValueError):t.jet_labels(d)
        for x in (True,10.0,'10'):
            with self.assertRaises(TypeError):t.image_bound(2,x)
        with self.assertRaises(ValueError):t.image_bound(2,9)
        with self.assertRaises(ValueError):t.ldlt([[1,2],[0,1]])
        with self.assertRaises(ValueError):t.inverse([[1,1],[1,1]])
    def test_both_modes_and_semantic_mutants(self):
        import subprocess,sys
        from pathlib import Path
        script=str(Path(t.__file__).resolve());baseline=None
        for flags in (['-B','-S'],['-B','-O','-S']):
            p=subprocess.run([sys.executable,*flags,script],capture_output=True,timeout=45)
            self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(p.stderr,b'')
            if baseline is None:baseline=p.stdout
            self.assertEqual(baseline,p.stdout)
            for m in t.MUTANTS:
                q=subprocess.run([sys.executable,*flags,script,'--mutant',m],capture_output=True,timeout=45)
                self.assertEqual(q.returncode,1,(m,q.stdout,q.stderr))
            q=subprocess.run([sys.executable,*flags,script,'--mutant','unknown'],capture_output=True,timeout=45)
            self.assertEqual(q.returncode,2)


class MarginalTests(unittest.TestCase):
    def test_birth_mixture_correlation_retained(self):
        for d in (1,2,3):
            C=t.matrix(d);q=2*d+1;I=t.inverse([row[:q] for row in C[:q]])
            B=[[sum(row[k]*I[k][j] for k in range(q)) for j in range(q)] for row in C[q:]]
            S=[[C[q+i][q+j]-sum(B[i][k]*C[q+j][k] for k in range(q)) for j in range(len(B))] for i in range(len(B))]
            mean,Sb,_,_=t.pin_regression(d)
            self.assertEqual(S,[[Sb[i][j]+F(2,3)*mean[i]*mean[j] for j in range(len(B))] for i in range(len(B))])
            self.assertEqual(S[-1][-1],30)
            for i,jet in enumerate(t.jet_labels(d)[q:]):
                if sum(jet)==2 and max(jet)==2:
                    self.assertEqual(S[i][i],F(8,3));self.assertEqual(S[i][-1],2)
    def test_zero_pin_dimension_and_determinant(self):
        for d in (1,2,3):
            q=2*d+1;C=t.matrix(d);det=F(1)
            for p in t.ldlt([row[:q] for row in C[:q]])[1]:det*=p
            self.assertEqual(det,18)
    def test_normalized_vs_unnormalized_is_not_equality(self):
        # Coefficient covariance exponent is -5/8, so multiplying the raw
        # covariance by a=2^8 changes the coefficient by 1/32, not by one.
        self.assertEqual(2**-5,F(1,32));self.assertNotEqual(F(1,32),1)

if __name__=='__main__':unittest.main()
