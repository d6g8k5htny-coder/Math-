from fractions import Fraction as F
import unittest
import inverse as m

class InitialTests(unittest.TestCase):
    def test_schur_chart(self):
        H,e=m.soft_chart([[F(-2)]],[F(1,3)],F(1,10))
        self.assertEqual(H,[[F(-7,45),F(1,3)],[F(1,3),F(-2)]])
        self.assertEqual(e,[F(1),F(1,6)])
    def test_barrier(self):
        self.assertEqual(m.barrier(F(4),F(1,10),F(2)),(F(1,20),F(1,12000)))
    def test_path_constants(self):
        self.assertEqual(m.path_constants(F(1),F(4)),(F(6),F(1,24),F(36),F(9)))
    def test_spectral_split(self):
        self.assertEqual(m.upper_split(F(1,10)),F(7,500))
    def test_exact_cubic_gap(self):
        self.assertEqual(m.cubic_gap(F(1,10),F(2)),F(1,6000))
    def test_tilt_exponent(self):
        self.assertEqual(m.tail_exponent(1),F(2,3))
        self.assertEqual(m.tail_exponent(0),F(1,3))
    def test_threshold(self):
        self.assertEqual([m.inverse_finite(p) for p in (F(0),F(1,3),F(2,3),F(1))],[True,True,False,False])
    def test_critical_cap(self):
        self.assertEqual(m.critical_model(),(F(1),F(-2)))


class ExtendedTests(unittest.TestCase):
    def test_full_scalar_controls(self):
        r=m.check();self.assertEqual(r['path_parameter_cases'],36)
        self.assertEqual(r['path_grid_checks'],612)
    def test_schur_in_arbitrary_hard_dimensions(self):
        count=0
        for n in range(1,5):
            B=[[F((i+2*j)%5-2,7) for j in range(n)] for i in range(n)]
            C=[[-sum(B[k][i]*B[k][j] for k in range(n))-int(i==j) for j in range(n)] for i in range(n)]
            for numerator in (1,2,5):
                v=[F(numerator*(i+1),11) for i in range(n)]
                for lam in (F(1,100),F(1,10),F(1)):
                    H,e=m.soft_chart(C,v,lam)
                    He=[sum(H[i][j]*e[j] for j in range(n+1)) for i in range(n+1)]
                    self.assertEqual(He,[-lam]+[F(0)]*n)
                    self.assertEqual(m.determinant(H),-lam*m.determinant(C))
                    for x in (F(-1),F(2,3)):
                        y=[F(i-1,3) for i in range(n)];vec=[x]+y
                        q=sum(vec[i]*H[i][j]*vec[j] for i in range(n+1) for j in range(n+1))
                        cv=m.inverse(C);z=[y[i]+x*sum(cv[i][j]*v[j] for j in range(n)) for i in range(n)]
                        self.assertEqual(q,-lam*x*x+sum(z[i]*C[i][j]*z[j] for i in range(n) for j in range(n)))
                    count+=1
        self.assertEqual(count,36)
    def test_uniform_scalar_barrier_inequality(self):
        for L in (F(1,3),F(1),F(4),F(24)):
            for K in (F(1),F(3),F(20)):
                for ratio in (F(1,100),F(1,3),F(1)):
                    lam=K*ratio;R,gap=m.barrier(L,lam,K)
                    self.assertLess(R,L/2)
                    self.assertLessEqual(-lam*R**2/2+K*R**3/6,-gap)
                    for j in range(1,11):
                        t=R*F(j,10)
                        self.assertLess(-lam*t*t/2+K*t**3/6,0)
    def test_scalar_cubic_stationary_point(self):
        for lam in (F(1,100),F(1,7),F(1)):
            for g in (F(1,2),F(1),F(7)):
                t=2*lam/g
                self.assertEqual(-lam*t+g*t*t/2,0)
                self.assertGreater(-lam+g*t,0)
                self.assertEqual(-lam*t*t/2+g*t**3/6,-m.cubic_gap(lam,g))
    def test_lower_path_at_worst_fourth_derivative(self):
        for g0 in (F(1,3),F(1),F(3)):
            for M in (F(1),F(10),F(100)):
                B,cut,C,gain=m.path_constants(g0,M)
                for g in (g0,2*g0):
                    lam=cut/2
                    for h in (-M,F(0),M):
                        val=lambda t:-lam*t*t/2+g*t**3/6+h*t**4/24
                        self.assertGreaterEqual(val(B*lam),gain*lam**3)
                        self.assertTrue(all(val(B*lam*F(j,20))>=-C*lam**3 for j in range(21)))
    def test_weighted_split_by_independent_primitives(self):
        for s in (F(1,100),F(1,3),F(1)):
            direct=s*s/2+s**3*(1/s-1)
            self.assertEqual(direct,m.upper_split(s))
            self.assertLessEqual(direct,F(3,2)*s*s)
            self.assertGreaterEqual(direct,s*s/2)
    def test_random_norm_factor_can_be_absorbed(self):
        for A in (F(1),F(3,2),F(10)):
            for x in (F(1,100),F(1,3),F(1),F(5)):
                self.assertLessEqual(min(F(1),A*x),A*min(F(1),x))
    def test_capped_model_piecewise_integration(self):
        for s in (F(1,20),F(1,3),F(1)):
            for n in (0,1,3,4,5):
                direct=s**(2-n)+2*(1-s**(2-n))/F(2-n)
                self.assertEqual(m.cap_model(s,n),direct)
                self.assertGreaterEqual(direct,1)
    def test_critical_model_logarithm(self):
        # For p=2/3, the lower part is1 and the upper integral is -2log(s).
        self.assertEqual(m.critical_model(),(1,-2))
        self.assertEqual(F(2)/3,m.tail_exponent())
    def test_wrong_inputs_rejected(self):
        for val in (True,0.5,'1/2'):
            with self.assertRaises(TypeError):m.cubic_gap(val,1)
        for C,v,l in (([[1]],[0],1),([[-1,1],[0,-1]],[0,0],1),([[-1]],[0],0)):
            with self.assertRaises(ValueError):m.soft_chart(C,v,l)
        with self.assertRaises(ValueError):m.barrier(0,1,2)
        with self.assertRaises(ValueError):m.barrier(1,3,2)
        with self.assertRaises(ValueError):m.path_constants(0,1)
        with self.assertRaises(ValueError):m.upper_split(0)
    def test_cli_both_modes_and_mutants(self):
        import subprocess,sys
        from pathlib import Path
        path=str(Path(m.__file__).resolve());baseline=None
        for flags in (['-B','-S'],['-B','-O','-S']):
            run=subprocess.run([sys.executable,*flags,path],capture_output=True,timeout=25)
            self.assertEqual(run.returncode,0,run.stderr);self.assertEqual(run.stderr,b'')
            if baseline is None:baseline=run.stdout
            self.assertEqual(run.stdout,baseline)
            for mutant in m.MUTANTS:
                bad=subprocess.run([sys.executable,*flags,path,'--mutant',mutant],capture_output=True,timeout=25)
                self.assertEqual(bad.returncode,1,(mutant,bad.stdout,bad.stderr))
            bad=subprocess.run([sys.executable,*flags,path,'--mutant','unknown'],capture_output=True,timeout=25)
            self.assertEqual(bad.returncode,2)

if __name__=='__main__':unittest.main()
