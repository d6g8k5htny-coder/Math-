"""Exact finite-algebra controls, not a Gaussian-model or Lean proof."""
from fractions import Fraction as F
import importlib.util
import json
from math import factorial
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent

class AdapterChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = HERE / 'algebra.py'
        cls.alg = None
        if path.is_file():
            spec = importlib.util.spec_from_file_location('cap_d3_algebra', path)
            cls.alg = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.alg)

    def call(self, name, *args):
        fn = getattr(self.alg, name, None)
        self.assertTrue(callable(fn), f'missing implementation: {name}')
        return fn(*args)

    def test_jacobian_from_three_by_three_derivative(self):
        for c,s in [(F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),(F(-5,13),F(12,13))]:
            for rho in [F(0),F(1,1000),F(1,3),F(7)]:
                rows = [[(1-c)/2,(1+c)/2,-rho*s],[-s/2,s/2,rho*c],[(1+c)/2,(1-c)/2,rho*s]]
                self.assertEqual(self.call('det3',rows),rho)

    def test_spectral_trace_determinant_and_frobenius(self):
        for lam in [F(-2),F(0),F(1,100),F(3)]:
            for gap in [F(0),F(1,1000),F(2),F(7)]:
                top=lam+gap
                for c,s in [(F(1),F(0)),(F(3,5),F(4,5)),(F(-5,13),F(12,13))]:
                    a,b,d=self.call('spectral_entries',lam,top,c,s)
                    self.assertEqual(a+d,lam+top)
                    self.assertEqual(a*d-b*b,lam*top)
                    self.assertEqual(a*a+2*b*b+d*d,lam*lam+top*top)

    def test_angle_and_volume_normalizations(self):
        data=self.call('normalization_ledger')
        # Relative to pi times the gap, entry measure has coefficient one.
        self.assertEqual(data['entry_angular_over_pi'],F(1))
        self.assertEqual(data['cartesian_to_trace_absdet'],F(2))
        self.assertEqual(data['spectral_to_trace_absdet'],F(1,2))
        # Frobenius volume differs by sqrt(2), so its squared ratio is two.
        self.assertEqual(data['frobenius_over_entry_squared'],F(2))
        # Whole-space radial Gaussian: 4 * integral_0^inf rho exp(-2rho^2) = 1.
        self.assertEqual(data['entry_angular_over_pi']*4*F(1,4),1)

    def test_soft_primitive_retains_mixed_term(self):
        for r in [F(1,100),F(1,3),F(1)]:
            for D in [F(1,4),F(2)]:
                for E in [F(0),F(3,2)]:
                    for U in [F(1),F(7,3),F(10)]:
                        actual=self.call('soft_primitive',D*r*U*U,E*r*U)
                        self.assertEqual(actual,r**3*(D**3*U**6/3+E*D**2*U**5/2))

    def test_typed_determinant_hard_factor_retained(self):
        for r in [F(1,100),F(1,2),F(1)]:
            for K in [F(1,3),F(1),F(3)]:
                for J in [F(1),F(5)]:
                    for top in [F(1,10000),F(1,2),F(8)]:
                        for frac in [F(1,7),F(1)]:
                            lam=frac*top; U=J+top; h=K*U
                            source=r*r*h*h/4*lam*(lam+F(3,2)*r*h)*top*(top+r*h)
                            major=self.call('weight_majorant',lam,top,J,r,K)
                            self.assertLessEqual(source,major)

    def test_order_bound_precedes_interval_extension(self):
        for top in [F(1,10),F(1),F(4)]:
            for upper in [top/10,top,10*top]:
                for shift in [F(0),F(1,3),F(5)]:
                    a=min(top,upper)
                    # Integral t(t+b)(top-t), on the ORIGINAL nonnegative interval.
                    actual=top*a**3/3+top*shift*a*a/2-a**4/4-shift*a**3/3
                    widened=top*self.call('soft_primitive',upper,shift)
                    self.assertGreaterEqual(actual,0)
                    self.assertLessEqual(actual,widened)
        self.assertLess(F(1)-F(2),0)  # Do not retain the signed gap after widening.

    def test_ninth_moment_radius_factorization(self):
        for r in [F(1,100),F(1,2),F(1)]:
            for K in [F(1,3),F(2)]:
                for k in [F(1,5),F(3)]:
                    D=4*K*K/(3*k); E=3*K/2; A=K*K*(1+K)/4
                    for J,top in [(F(1),F(1,10)),(F(3),F(4)),(F(10),F(1,1000))]:
                        U=J+top
                        integrated=A*r*r*top*top*U**3*self.call('soft_primitive',D*r*U*U,E*r*U)
                        exact=A*r**5*top*top*(D**3*U**9/3+E*D*D*U**8/2)
                        self.assertEqual(integrated,exact)
                        upper=self.call('post_soft_majorant',top,J,r,K,k)
                        self.assertLessEqual(exact,upper)

    def test_power_envelope_and_gaussian_moments(self):
        for J in [F(1),F(3,2),F(9)]:
            for top in [F(0),F(1,10000),F(2),F(7)]:
                self.assertLessEqual((J+top)**9,self.call('ninth_power_envelope',J,top))
        # Recurrence: even coefficients multiply sqrt(pi), odd are rational.
        for scale in [F(1,3),F(1),F(2)]:
            c=scale*scale
            self.assertEqual(self.call('gaussian_half_moment',2,scale),(F(1,4)/scale**3,True))
            self.assertEqual(self.call('gaussian_half_moment',11,scale),(F(60)/c**6,False))
            for n in range(10):
                a,pa=self.call('gaussian_half_moment',n,scale)
                b,pb=self.call('gaussian_half_moment',n+2,scale)
                self.assertEqual(pa,pb)
                self.assertEqual(b,F(n+1,2)/c*a)

    def test_gaussian_mean_majorant(self):
        for z in [(F(0),F(0),F(0)),(F(2),F(-1),F(3)),(F(1,7),F(1),F(-2))]:
            for mean in [(F(0),F(0),F(0)),(F(1),F(-2),F(1,3))]:
                gap=self.call('gaussian_square_gap',z,mean)
                expected=sum((a-b)**2 for a,b in zip(z,mean))-sum(a*a for a in z)/2+sum(b*b for b in mean)
                self.assertEqual(gap,expected)
                self.assertGreaterEqual(gap,0)

    def test_full_normalizer_once(self):
        for r in [F(1,100),F(1,2),F(1)]:
            for C,z in [(F(3),F(1,7)),(F(1,5),F(4))]:
                self.assertEqual(self.call('normalized_depth',C,z,r),(C/z)*r**3)

    def test_dependent_marginals_not_product_domination(self):
        joint=self.call('diagonal_bernoulli')
        self.assertEqual(sum(joint.values()),1)
        self.assertEqual(sum(p for (x,y),p in joint.items() if x==1),F(1,2))
        self.assertEqual(sum(p for (x,y),p in joint.items() if y==1),F(1,2))
        self.assertGreater(joint[(1,1)],F(1,2)*F(1,2))

    def test_weighted_support_not_global_implication(self):
        # good=>G fails at the zero-weight atom, but the weighted transfer is exact.
        atoms=[(F(0),True,False),(F(2),True,True),(F(3),False,False)]
        left,right=self.call('support_transfer_sums',atoms)
        self.assertEqual((left,right),(F(3),F(3)))
        self.assertTrue(any(good and not G for W,good,G in atoms))

    def test_no_claim_eighth_moment_controls_ninth(self):
        ratios=[]
        for T in [F(2),F(4),F(8),F(16)]:
            m8,m9=self.call('two_atom_moments',T)
            self.assertLessEqual(m8,2)
            self.assertGreaterEqual(m9,T)
            ratios.append(m9/m8)
        self.assertTrue(all(a<b for a,b in zip(ratios,ratios[1:])))

    def test_all_soft_neighborhoods_and_boundaries(self):
        # Positive mass polynomial bounds remain valid for arbitrarily small top.
        for denominator in [10,100,10000,10**8]:
            top=F(1,denominator); lam=top/2
            self.assertGreater(self.call('weight_majorant',lam,top,F(1),F(1,10),F(1)),0)
            self.assertEqual(self.call('soft_primitive',0,top),0)
        with self.assertRaises(ValueError): self.call('spectral_entries',F(2),F(1),F(1),F(0))
        with self.assertRaises(ValueError): self.call('gaussian_half_moment',2,F(0))

if __name__ == '__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(AdapterChecks)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    summary={'scope':'exact finite algebra only; not analytic or Lean acceptance','tests':result.testsRun,
             'failures':[test.id().split('.')[-1] for test,_ in result.failures],
             'errors':[test.id().split('.')[-1] for test,_ in result.errors],
             'success':result.wasSuccessful()}
    print(json.dumps(summary,sort_keys=True,indent=2))
    raise SystemExit(0 if result.wasSuccessful() else 1)
