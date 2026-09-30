import unittest
from fractions import Fraction as F
import cubic

class CubicTests(unittest.TestCase):
    def test_known_two_saddle_model(self):
        self.assertEqual(cubic.window_count(1,F(-3,2),-2,0), 2)
    def test_single_saddle_sector(self):
        self.assertEqual(cubic.window_count(1,-1,0,1), 1)
    def test_zero_saddle_sector(self):
        self.assertEqual(cubic.window_count(1,-1,1,0), 0)
    def test_shear(self):
        self.assertEqual(cubic.canonical(1,6,1,F(-3,2)), (F(-2),F(0)))
    def test_two_sector_boundary_is_one(self):
        self.assertEqual(cubic.window_count(F(5,48),F(-3,2),-2,1), 1)
    def test_zero_sector_boundary_is_zero(self):
        self.assertEqual(cubic.window_count(F(5,12),-2,-1,1), 0)
    def test_scalar_boundary(self):
        self.assertEqual(cubic.window_count(F(1,6),-1,0,1), 0)
    def test_typed_weight(self):
        self.assertEqual(cubic.weight(1,F(-3,2),-2),45)
    def test_slice_integrals(self):
        self.assertEqual(cubic.integrated_weight(1,-2,-2,-1),48)
    def test_exponent_ledger(self):
        self.assertEqual(cubic.rare_exponent(),3)


class ExtendedTests(unittest.TestCase):
    def test_sign_reflection(self):
        for D in (F(0),F(1,10),F(1),F(3)):
            self.assertEqual(cubic.window_count(1,F(-3,2),-2,D),
                             cubic.window_count(1,F(-3,2),-2,-D))
    def test_typed_boundary_rejected(self):
        with self.assertRaises(ValueError): cubic.window_count(1,-1,-2,0)
    def test_float_rejected(self):
        with self.assertRaises(ValueError): cubic.window_count(1.0,-1,0,1)
    def test_bool_rejected(self):
        with self.assertRaises(ValueError): cubic.canonical(True,0,0,0)
    def test_nonpositive_k(self):
        with self.assertRaises(ValueError): cubic.canonical(0,0,0,0)
    def test_linear_conic(self):
        self.assertEqual(cubic.conic_oracle(F(1,12),-1,-1,1),1)
    def test_tangent_below_window(self):
        self.assertEqual(cubic.conic_oracle(F(1,4),-1,1,1),0)
    def test_s_equals_B(self):
        self.assertEqual(cubic.window_count(1,-1,-1,0),0)
        self.assertEqual(cubic.window_count(1,-1,-1,1),1)
    def test_B_D_zero(self):
        self.assertEqual(cubic.conic_oracle(1,-1,0,0),0)
    def test_surd_exact_equality(self):
        self.assertEqual(cubic.surd_sign(-2,1,4),0)
    def test_surd_both_signs(self):
        self.assertEqual(cubic.surd_sign(-1,1,2),1)
        self.assertEqual(cubic.surd_sign(1,-1,2),-1)
    def test_open_root_endpoints(self):
        self.assertEqual(cubic.roots_in_open_interval(1,0,-1,-1,1),0)
        self.assertEqual(cubic.roots_in_open_interval(1,0,-1,-2,2),2)
    def test_double_root(self):
        self.assertEqual(cubic.roots_in_open_interval(1,-2,1,0,2),1)
    def test_linear_root(self):
        self.assertEqual(cubic.roots_in_open_interval(0,2,-1,0,1),1)
    def test_no_real_roots(self):
        self.assertEqual(cubic.roots_in_open_interval(1,0,1,-3,3),0)
    def test_zero_polynomial_rejected(self):
        with self.assertRaises(ValueError): cubic.roots_in_open_interval(0,0,0,-1,1)
    def test_closed_form_D_zero_integral(self):
        for k in (F(1,2),F(1),F(3)):
            for B in (F(-1),F(-2),F(-5)):
                self.assertEqual(cubic.integrated_weight(k,B,B,B/2),-6*k*k*B**3)
    def test_scalar_sector_integral(self):
        # k=1/6, D=1 gives lower s=-1 and integral 72*k^3*D^2=1/3.
        self.assertEqual(cubic.integrated_weight(F(1,6),0,-1,0),F(1,3))
    def test_conic_discriminant_grid(self):
        self.assertEqual(cubic.run_checks()['rational_classifier_cases'],600)
    def test_shear_polynomial_identity(self):
        for k in (F(1,2),F(1),F(2)):
            for a in (F(-3),F(0),F(6)):
                beta,c,s=F(2,3),F(-5,2),F(-7,3)
                B,D=cubic.canonical(k,a,beta,c)
                for u,z in ((F(0),F(1)),(F(2,3),F(-3,2)),(F(-1,2),F(0))):
                    X=u-a*z/(12*k)
                    original=2*k*X**3-F(3,2)*k*X-k/2+s*z*z/2+a*(X*X-F(1,4))*z/2+beta*X*z*z/2+c*z**3/6
                    canonical=2*k*u**3-F(3,2)*k*u-k/2+s*z*z/2+B*u*z*z/2+D*z**3/3
                    self.assertEqual(original,canonical)
    def test_stationary_height_and_det(self):
        # Construct exact critical points rather than taking a floating square root.
        for u in (F(-3,4),F(-1),F(1,4),F(3,4)):
            k,z=F(1),F(2)
            B=-12*k*(u*u-F(1,4))/(z*z)
            s=-2-abs(B)
            D=(-s-B*u)/z
            h=2*k*u**3-F(3,2)*k*u-k/2+s*z*z/2+B*u*z*z/2+D*z**3/3
            det=12*k*u*(s+B*u+2*D*z)-(B*z)**2
            self.assertEqual(h,-k*(u+F(1,2))+s*z*z/6)
            self.assertEqual(det,-3*k*(B+4*s*u))
    def test_cli_modes_and_mutants(self):
        import subprocess,sys
        from pathlib import Path
        script=str(Path(cubic.__file__).resolve())
        reference=None
        for flags in (['-B','-S'],['-B','-O','-S']):
            run=subprocess.run([sys.executable,*flags,script],capture_output=True,timeout=30)
            self.assertEqual(run.returncode,0,run.stderr)
            if reference is None: reference=run.stdout
            self.assertEqual(run.stdout,reference)
            for name in cubic.MUTANTS:
                run=subprocess.run([sys.executable,*flags,script,'--mutant',name],capture_output=True,timeout=30)
                self.assertEqual(run.returncode,1,(name,run.stdout,run.stderr))
            run=subprocess.run([sys.executable,*flags,script,'--mutant','unknown'],capture_output=True,timeout=30)
            self.assertEqual(run.returncode,2)

if __name__=='__main__': unittest.main()
