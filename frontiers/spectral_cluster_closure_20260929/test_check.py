import unittest
from fractions import Fraction as F
import check as c

class InitialTests(unittest.TestCase):
    def test_absorption_near(self):
        self.assertEqual(c.absorption(1,1,F(1,10),1),'near')
    def test_absorption_far(self):
        self.assertEqual(c.absorption(200,1,F(1,10),1),'far')
    def test_absorption_invalid(self):
        with self.assertRaises(ValueError): c.absorption(5,1,F(1,10),1)
    def test_vandermonde(self):
        self.assertEqual(c.vandermonde([1,3,5]),16)
    def test_spectral_factor(self):
        self.assertEqual(c.spectral_factor(F(1,10),-1,[2,4]),F(741,500))
    def test_empty_hard_factor(self):
        self.assertEqual(c.spectral_factor(F(1,10),-1,[]),F(1,10))
    def test_limit_hard_factor(self):
        self.assertEqual(c.limit_hard_factor([2,4]),1024)
    def test_weight(self):
        self.assertEqual(c.typed_weight(1,F(-3,2),0,-2),45)
    def test_zero_filtered(self):
        self.assertEqual(c.nonempty_intensity({0:F(7,8),1:F(1,16),2:F(1,16)},F(1,8)),{1:F(1,2),2:F(1,2)})
    def test_reduced_derivative(self):
        self.assertEqual(c.reduced_third(1,2,3,4),20)
    def test_majorant_degree(self):
        self.assertEqual(c.majorant_degree(3),14)
    def test_bad_cutoff(self):
        self.assertFalse(c.invalid_cutoff_bound(F(1,10),F(1,100),F(1,10)))


class AlgebraTests(unittest.TestCase):
    def test_absorption_grid(self):
        count=0
        for a in (F(1),F(3)):
            for u in (F(1),F(2),F(5)):
                for r in (F(1,100),F(1,10),F(1,2)):
                    for x in map(F,(0,1,2,5,10,20,100,200,1000,20000)):
                        if x<=a*u*u+a*r*r*x*x:
                            branch=c.absorption(x,u,r,a)
                            self.assertTrue(x<=2*a*u*u if branch=='near' else x>=1/(2*a*r*r))
                            count+=1
        self.assertGreater(count,80)
    def test_float_rejected(self):
        with self.assertRaises(ValueError): c.absorption(1.0,1,F(1,10),1)
    def test_bad_dimension(self):
        with self.assertRaises(ValueError): c.majorant_degree(1)
    def test_bool_dimension(self):
        with self.assertRaises(ValueError): c.majorant_degree(True)
    def test_unordered_spectrum(self):
        with self.assertRaises(ValueError): c.spectral_factor(F(1,10),-30,[1,2])
    def test_hard_zero_rejected(self):
        with self.assertRaises(ValueError): c.limit_hard_factor([0,1])
    def test_weight_boundary_zero(self):
        self.assertEqual(c.typed_weight(1,-1,0,-2),0)
    def test_weight_shear(self):
        self.assertEqual(c.typed_weight(1,F(-3,2),6,1),45)
    def test_bad_probability(self):
        with self.assertRaises(ValueError): c.nonempty_intensity({0:F(1,2)},F(1,10))
    def test_zero_mass_diverges(self):
        for j in (10,100,1000):
            e=F(1,j)
            self.assertEqual((1-e)/e,j-1)
            self.assertNotIn(0,c.nonempty_intensity({0:1-e,2:e},e))
    def test_full_mixed_third_identity(self):
        for g in (F(1),F(12),F(24)):
            for vd in (F(2),F(5)):
                for tensor in (F(3),F(7)):
                    terms=(g-3*vd-tensor,vd+tensor,-tensor,tensor)
                    self.assertEqual(c.reduced_third(*terms),g)
                    for index in (1,2,3):
                        changed=list(terms); changed[index]=F(0)
                        self.assertNotEqual(c.reduced_third(*changed),g)
    def test_determinant(self):
        self.assertEqual(c.det([[2,1],[1,3]]),5)
        self.assertEqual(c.det([]),1)
    def test_weyl_local_jacobian_2(self):
        for co,si in ((F(1),F(0)),(F(3,5),F(4,5)),(F(5,13),F(12,13))):
            for l1,l2 in ((F(-2),F(3)),(F(1,3),F(7))):
                gap=l2-l1
                jac=[[co*co,si*si,2*co*si*gap],
                     [co*si,-co*si,-(co*co-si*si)*gap],
                     [si*si,co*co,-2*co*si*gap]]
                self.assertEqual(abs(c.det(jac)),gap)
    def test_two_soft_column_determinant(self):
        # Exact d=3 Schur expansion, keeping the r^3 mixed correction.
        for r in (F(1,100),F(1,10),F(1),F(2)):
            matrix=[[-6*r,-r,2*r],[-r,-2*r,3*r],[2*r,3*r,-5]]
            expected=-55*r*r+50*r**3
            self.assertEqual(c.det(matrix),expected)
    def test_orthogonal_norms(self):
        for co,si in ((F(3,5),F(4,5)),(F(5,13),F(12,13))):
            l1,l2=F(-2),F(7)
            a=co*co*l1+si*si*l2; b=co*si*(l1-l2); d=si*si*l1+co*co*l2
            self.assertEqual(a*a+2*b*b+d*d,l1*l1+l2*l2)
    def test_unbounded_shear_counterexample(self):
        # D=-1,v=t,A00=-t^2, raw T_www=1, transformed tau_zzz=t^3.
        for t in (10,100,1000):
            raw_norm_upper=F(t*t+2*t+2)
            self.assertGreater(F(t**3)/raw_norm_upper,F(t,2))
    def test_deep_constants(self):
        for R in (F(1),F(3)):
            for K in (F(1),F(12)):
                for k in (F(1,10),F(1),F(3)):
                    r=k/(4*R*K); lam=2*(8*R*K+56*R*K*K/k)*r
                    rho=4*R*R*K*r*r/lam; slope=4*R*K*r/lam
                    self.assertLess(rho,R*r/2)
                    self.assertLess(slope,F(1,2))
                    self.assertLess(28*R*K*K*r/lam,k/2)
                    self.assertEqual(2*R*K*r,k/2)
    def test_near_far_scaling(self):
        self.assertEqual(F(3)+F(3,2),F(9,2))
    def test_higher_factorials_vanish_in_limit(self):
        from math import prod
        for q in range(3,9):
            for n in (1,2): self.assertEqual(prod(n-j for j in range(q)),0)

class ExecutionTests(unittest.TestCase):
    def test_both_modes_and_semantic_controls(self):
        import subprocess,sys
        from pathlib import Path
        command=str(Path(c.__file__).resolve())
        reference=None
        for flags in (['-B','-S'],['-B','-O','-S']):
            run=subprocess.run([sys.executable,*flags,command],capture_output=True,timeout=30)
            self.assertEqual(run.returncode,0,run.stderr)
            if reference is None: reference=run.stdout
            self.assertEqual(run.stdout,reference)
            for label in c.MUTANTS:
                run=subprocess.run([sys.executable,*flags,command,'--mutant',label],capture_output=True,timeout=30)
                self.assertEqual(run.returncode,1,(label,run.stdout,run.stderr))
                self.assertEqual(run.stderr,b'')
            run=subprocess.run([sys.executable,*flags,command,'--mutant','unknown'],capture_output=True,timeout=30)
            self.assertEqual(run.returncode,2)

if __name__=='__main__': unittest.main()
