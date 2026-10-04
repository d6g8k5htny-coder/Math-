from fractions import Fraction as F
import unittest
import shape

class InitialTests(unittest.TestCase):
    def test_normalization(self): self.assertEqual(shape.shape_moment(0), F(888807,280))
    def test_first_moment(self): self.assertEqual(shape.shape_moment(1), F(3524743221,1361360))
    def test_shape_w_normalization(self): self.assertEqual(shape.limit_w_even_moment(0), 1)
    def test_companion_survival(self): self.assertEqual(shape.ratio_survival(1), 1)
    def test_companion_height_ratio(self): self.assertEqual(shape.height_ratio(2), F(32,5))
    def test_supercritical_four(self): self.assertEqual(shape.moment_blowup_constant(4), F(30,13))
    def test_supercritical_seven(self): self.assertEqual(shape.moment_blowup_constant(7), F(441,65))
    def test_supercritical_ten(self): self.assertEqual(shape.moment_blowup_constant(10), F(3270,91))



class GeometryTests(unittest.TestCase):
    def test_rational_classifier_grid(self):self.assertEqual(shape.checks(),589)
    def test_classifier_factor(self):
        for e in (F(1,1000),F(1,10),F(1,2),F(9,10)):
            for x in (F(-1,4),F(0),F(1,20),F(1,4),F(2,5)):
                p=x+F(1,2);a=12*p*p-3;v=6*(e+x)
                lhs=(v-a)**2*(2*v+a)-12*(v-a*p)**2
                self.assertEqual(lhs,432*(1-e)*(2*x**3+3*e*x*x-e*e))
    def test_no_finite_cutoff_doublet_certainty(self):
        for e in (F(1,10),F(1,10000),F(1,10**8)):
            self.assertTrue(shape.in_support(e,0))
            self.assertFalse(shape.doublet(e,0))
    def test_boundary_order_by_exact_brackets(self):
        for e in (F(1,1000),F(1,10),F(1,2),F(9,10)):
            c=shape.isolate(e*e,lambda x:2*x**3+3*e*x*x,F(0),F(1,2),100)
            b=shape.isolate(e,lambda x:3*x*x+2*x**3,F(0),F(1,2),100)
            self.assertTrue(0<c[0]<c[1]<b[0]<b[1])
    def test_exact_scaled_companion(self):
        cases=0
        for delta in (F(1,1000),F(1,10000)):
            for w in (F(1,5),F(1,3),F(1,2)):
                e,x=delta*delta,delta*w
                other=shape.companion(e,x)
                V,H=shape.exact_scaled_companion(delta,w)
                self.assertTrue(shape.doublet(e,x))
                self.assertEqual(V,-other[2]);self.assertEqual(H,other[0]/e)
                self.assertTrue(V>1 and H>1);cases+=1
        self.assertEqual(cases,6)
    def test_companion_limit_at_compact_shapes(self):
        for w in (F(1,5),F(1,3),F(1,2)):
            vals=[]
            for d in (F(1,1000),F(1,10000),F(1,100000)):
                v,h=shape.exact_scaled_companion(d,w)
                err=abs(v-shape.w_to_ratio(w))+abs(h-shape.height_ratio(shape.w_to_ratio(w)))
                vals.append(err)
            self.assertTrue(vals[0]>vals[1]>vals[2]>0)
    def test_scaled_kernel_identity(self):
        for d in (F(1,3),F(1,10),F(1,100)):
            for w in (F(-1,10),F(0),F(1,4),F(1,2)):
                self.assertEqual(shape.kernel(d*d,d*w)*d,F(10368)*d**6*shape.scaled_phi(d,w))
    def test_selection_support_is_the_two_polynomial_strips(self):
        for i in range(-19,10):
            x=F(i,20)
            for j in range(1,20):
                e=F(j,20)
                lower=-2*x-x*x if x<=0 else 3*x*x+2*x**3
                self.assertEqual(shape.in_support(e,x),lower<e<1)
                if shape.in_support(e,x):self.assertGreater(shape.kernel(e,x),0)


class DensityAndMomentTests(unittest.TestCase):
    def test_second_parent_moment(self):self.assertEqual(shape.shape_moment(2),F(190490806059,87127040))
    def test_limit_shape_moments(self):
        for j in range(1,8):
            self.assertTrue(0<shape.limit_w_even_moment(j)<F(1,3)**j)
    def test_radius_change_of_variables(self):
        for w in (F(1,10),F(1,4),F(1,3),F(1,2)):
            v=shape.w_to_ratio(w)
            self.assertEqual(shape.w_density(w),shape.ratio_density(v)/w**3)
            self.assertEqual(shape.rho_density(1/v),shape.ratio_density(v)*v*v)
    def test_survival_positive_decreasing_and_tail(self):
        prev=F(1)
        for t in (2,3,10,100,10000):
            z=shape.ratio_survival(t)
            self.assertTrue(0<z<prev);prev=z
            self.assertLess(abs(t*z-F(81,52)),F(2,t))
    def test_survival_derivative(self):
        for t in (F(3,2),F(2),F(10)):
            q=2*t+1
            derivative=-F(81,13)/q**2+F(81,13)/q**4
            self.assertEqual(-derivative,shape.ratio_density(t))
    def test_lifetime_ratio_asymptotic(self):
        for t in (F(10),F(100),F(1000)):
            self.assertGreater(shape.height_ratio(t),t**3/2)
            self.assertLess(shape.height_ratio(t)/t**3-F(1,2),F(1,t))
    def test_interval_density_nesting(self):
        for e in (F(1,100),F(1,3),F(3,4)):
            lo=shape.density_intervals(e,80);hi=shape.density_intervals(e,128)
            for name in lo:
                self.assertTrue(0<lo[name][0]<=hi[name][0]<=hi[name][1]<=lo[name][1])
    def test_singleton_density_asymptotic(self):
        alpha=shape.isolate(F(1),lambda x:2*x**3,F(0),F(1),128)
        coeff=F(10368)*(alpha[0]+alpha[1])**2/4
        errors=[]
        for n in (10,30,100):
            e=F(1,n**6)
            bounds=shape.density_intervals(e,160)
            estimate=sum(bounds['singleton'],F(0))/2*n**20
            errors.append(abs(estimate-coeff))
            total=sum(bounds['total'],F(0))/2*n**18
            self.assertLess(abs(total-3328),F(10**6,n**3))
        self.assertTrue(errors[0]>errors[1]>errors[2]>0)
    def test_moment_constants_independent_binomial_integral(self):
        # Integrate small rational polynomials by hand, without production helpers.
        integrals={4:F(1,2)+F(1,3),7:F(1,4)+F(2,5)+F(1,6),
                   10:F(1,6)+F(3,7)+F(3,8)+F(1,9)}
        for p,val in integrals.items():
            k=F(2592,13*(13-p))*F(1,2)**((13-p)//3)*val
            self.assertEqual(shape.moment_blowup_constant(p),k)
    def test_uniform_square_comparisons_finite_grid(self):
        for r in (F(1,1000),F(1,10),F(1,2),F(9,10)):
            for z in (F(1,1000),F(1,10),F(1,2),F(9,10)):
                a=shape.square_lifetime(r,z)/(r**3*z*z)
                b=shape.square_density(r,z)/(165888*r**12*z**7)
                self.assertTrue(F(1,4)<=a<=8)
                self.assertTrue(F(1,2**23)<=b<=2**32)
    def test_square_boundary_coefficients(self):
        for r in (F(1,10),F(1,3),F(3,4)):
            z=F(1,10**8)
            kappa=r**3*(r+2)/(r+1)**2
            self.assertLess(abs(shape.square_lifetime(r,z)/(kappa*z*z)-1),10*z)
            dens=shape.square_density(r,z)/(165888*r**12*z**7/(r+1)**7)
            self.assertLess(abs(dens-1),100*z)
    def test_invalid_inputs(self):
        for val in (True,0.25,'1/2'):
            with self.assertRaises(TypeError):shape.ratio_survival(val)
        for j in (-1,9,True):
            with self.assertRaises(ValueError):shape.shape_moment(j)
        for p in (1,2,13,True):
            with self.assertRaises(ValueError):shape.moment_blowup_constant(p)
        with self.assertRaises(ValueError):shape.density_intervals(0)
        with self.assertRaises(ValueError):shape.density_intervals(1)
        with self.assertRaises(ValueError):shape.ratio_survival(F(1,2))
    def test_cli_both_modes_and_negative_controls(self):
        import subprocess,sys
        from pathlib import Path
        script=str(Path(shape.__file__).resolve());baseline=None
        for flags in (['-B','-S'],['-B','-O','-S']):
            run=subprocess.run([sys.executable,*flags,script],capture_output=True,timeout=30)
            self.assertEqual(run.returncode,0,run.stderr);self.assertEqual(run.stderr,b'')
            if baseline is None:baseline=run.stdout
            self.assertEqual(run.stdout,baseline)
            for mutant in shape.MUTANTS:
                bad=subprocess.run([sys.executable,*flags,script,'--mutant',mutant],capture_output=True,timeout=30)
                self.assertEqual(bad.returncode,1,(mutant,bad.stdout,bad.stderr))
            bad=subprocess.run([sys.executable,*flags,script,'--mutant','unknown'],capture_output=True,timeout=30)
            self.assertEqual(bad.returncode,2)

if __name__=='__main__':unittest.main()
