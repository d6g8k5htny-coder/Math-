"""Exact finite spectral regressions; not a continuum proof or Lean run."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import itertools
import json
import subprocess
import sys
import unittest

P = Path(__file__).with_name('product_transverse_check.py')
PHASES = [(F(3,5),F(4,5)),(F(5,13),F(12,13)),(F(-1),F(0))]

class ProductTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(P.is_file(), 'product-transverse implementation missing')
        spec=importlib.util.spec_from_file_location('product_check',P)
        self.m=importlib.util.module_from_spec(spec); spec.loader.exec_module(self.m)
        self.p=self.m.spectrum()

    def test_moments(self):
        m2,m4,g=self.m.moments(self.p)
        self.assertEqual((m2,m4,g),(F(2),F(34,5),F(14,5)))

    def test_residual_orthogonality(self):
        for z in PHASES:
            for target in ((0,0),(1,0),(2,0),(0,1),(1,1)):
                self.assertEqual(self.m.residual_cross(self.p,z,target),0)

    def test_residual_kernel(self):
        _,_,g=self.m.moments(self.p)
        for z in PHASES:
            self.assertEqual(self.m.residual_covariance(self.p,z),g*self.m.rho(self.p,z))

    def test_full_eleven_observation_variance(self):
        _,_,g=self.m.moments(self.p)
        for z in PHASES:
            obs,q=self.m.observations()
            variance,coeff=self.m.regress(self.p,z,obs,q)
            self.assertEqual(len(coeff),11)
            self.assertEqual(variance,g*(1+self.m.rho(self.p,z))/2)

    def test_mean_independent_of_nuisance_values(self):
        m2,_,_=self.m.moments(self.p)
        for z in PHASES:
            obs,q=self.m.observations(); _,co=self.m.regress(self.p,z,obs,q)
            for shift in (-3,0,4):
                values=list(map(F,(6,0,shift,5,0,-shift,0,shift,0,2*shift,1)))
                self.assertEqual(sum(a*b for a,b in zip(co,values)),F(1,2)-m2*F(11,2))

    def test_difference_under_only_six_pins(self):
        m2,_,g=self.m.moments(self.p)
        for z in PHASES:
            obs,q=self.m.observations(); pins=[obs[j] for j in (0,1,6,3,4,8)]
            diff=obs[-1]; variance,co=self.m.regress(self.p,z,pins,diff)
            self.assertEqual(variance,2*g*(1-self.m.rho(self.p,z)))
            self.assertEqual(sum(a*b for a,b in zip(co,map(F,(6,0,0,5,0,0)))),m2)

    def test_contact_eleven_jet_residual(self):
        obs=[[(F(1),0,j,0)] for j in range(6)]
        obs += [[(F(1),0,j,1)] for j in range(4)]
        obs += [[(F(1),0,1,2)]]
        v,co=self.m.regress(self.p,PHASES[0],obs,[(F(1),0,0,2)])
        m2,_,g=self.m.moments(self.p)
        self.assertEqual(v,g)
        self.assertEqual(co,[-m2]+[F(0)]*10)

    def test_nonproduct_countercontrol(self):
        p=self.m.spectrum(correlated=True)
        self.assertNotEqual(self.m.residual_cross(p,(F(1),F(0)),(2,0)),0)

    def test_negative_correlation_not_positive_kernel(self):
        _,_,g=self.m.moments(self.p)
        rho=self.m.rho(self.p,PHASES[-1])
        self.assertLess(rho,0)
        self.assertLess(g*(1+rho)/2,g/2)

    def test_zero_gap_and_collision_rejected(self):
        p=self.m.spectrum(yvalues=(-1,1))
        self.assertEqual(self.m.moments(p)[2],0)
        obs,q=self.m.observations()
        with self.assertRaises(ValueError): self.m.regress(p,PHASES[0],obs,q)
        with self.assertRaises(ValueError): self.m.regress(self.p,(F(1),F(0)),obs,q)

    def test_moment_positivity_and_symmetry(self):
        self.assertEqual(sum(self.p.values()),1)
        for (x,y),mass in self.p.items():
            self.assertGreater(mass,0); self.assertEqual(self.p[-x,-y],mass)
        for z in PHASES:
            self.assertEqual(self.m.rho(self.p,z),self.m.rho(self.p,(z[0],-z[1])))

    def test_cli_contract(self):
        reasons=['RESIDUAL_SIGN','VARIANCE_FACTOR','MEAN_SHIFT','DIFFERENCE_VARIANCE','PRODUCT_REQUIRED','DENSITY_SIGN_PREMISE']
        baseline=[]
        for flags in (['-B','-S'],['-B','-O','-S']):
            p=subprocess.run([sys.executable,*flags,str(P)],capture_output=True,timeout=30)
            self.assertEqual((p.returncode,p.stderr),(0,b'')); json.loads(p.stdout); baseline.append(p.stdout)
            for j,reason in enumerate(reasons,1):
                p=subprocess.run([sys.executable,*flags,str(P),'--mutant','M'+str(j)],capture_output=True,timeout=30)
                self.assertEqual((p.returncode,p.stdout,p.stderr),(1,b'',('PRODUCT_FAIL: '+reason+'\n').encode()))
            p=subprocess.run([sys.executable,*flags,str(P),'--mutant','M9'],capture_output=True,timeout=30)
            self.assertEqual(p.returncode,2)
        self.assertEqual(*baseline)

if __name__=='__main__': unittest.main()
