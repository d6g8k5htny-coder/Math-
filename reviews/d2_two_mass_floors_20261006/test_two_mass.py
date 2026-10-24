#!/usr/bin/env python3
"""Exact finite controls; not continuum proof or a Lean execution."""
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

SIDE = Path(__file__).resolve().parent

class TwoMassTests(unittest.TestCase):
    def module(self):
        path = SIDE / 'two_mass.py'
        self.assertTrue(path.is_file(), 'two_mass.py implementation is missing')
        spec = importlib.util.spec_from_file_location('two_mass_control', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_weighted_completion(self):
        m = self.module()
        for u in (F(1,7), F(1), F(4)):
            for v in (F(1,9), F(2), F(7)):
                for a,b,c in ((F(-3),F(2),F(1)),(F(1),F(4),F(0)),(F(1),F(4),(u+4*v)/(u+v))):
                    self.assertEqual(u*(a-c)**2+v*(b-c)**2,
                        m.harmonic(u,v)*(a-b)**2+(u+v)*(c-(u*a+v*b)/(u+v))**2)

    def test_probability_mass_domain(self):
        m = self.module()
        for args in ((F(0),F(1,2),F(1),F(4)),(F(1),F(1),F(1),F(4)),
                     (F(1,4),F(1,4),F(-1),F(4)),(F(1,4),F(1,4),F(1),F(1))):
            with self.assertRaises(ValueError): m.floors(*args)
        with self.assertRaises(TypeError): m.floors(0.25,F(1,4),F(1),F(4))

    def test_distinct_sharp_extremizers(self):
        m = self.module(); p,r,s,t = F(1,5),F(2,5),F(1),F(9)
        f = m.floors(p,r,s,t); d = (p*s+r*t)/(p+r)
        a2,a4,a6 = m.moments([(s,p),(t,r),(F(0),1-p-r)])
        self.assertEqual(a6-a4*a4/a2, f['delta'])
        self.assertGreater(a4-a2*a2, f['gap'])
        b2,b4,b6 = m.moments([(s,p),(t,r),(d,1-p-r)])
        self.assertEqual(b4-b2*b2, f['gap'])
        self.assertGreater(b6-b4*b4/b2, f['delta'])

    def test_zero_radius_is_not_strict_delta(self):
        m = self.module(); f=m.floors(F(1,2),F(1,2),F(0),F(1))
        self.assertEqual(f['gap'],F(1,4)); self.assertEqual(f['delta'],0)
        self.assertEqual(m.moments([(F(0),F(1,2)),(F(1),F(1,2))]),(F(1,2),)*3)

    def test_mass_and_radius_lower_bounds(self):
        m = self.module()
        for u,v in ((F(1,10),F(2,5)),(F(2),F(3))):
            self.assertLessEqual(m.harmonic(u,v),m.harmonic(2*u,3*v))
        p,r,s,t=F(1,5),F(1,3),F(1,4),F(4)
        lower=m.floors(p/2,r/3,s,t); actual=m.floors(p,r,s,t)
        for key in lower: self.assertLessEqual(lower[key],actual[key])

    def test_lattice_floor_dominates_old_pair_floor(self):
        m=self.module(); p,r,h=F(1,6),F(1,9),F(1,3)
        s,t=h*h,4*h*h
        m2,m4,m6=m.moments([(s,p),(t,r),(9*h*h,1-p-r)])
        f=m.floors(p,r,s,t)
        self.assertGreater(f['gap'],9*h**4*p*r)
        self.assertGreater(f['delta'],36*h**8*p*r/m2)
        self.assertLessEqual(f['delta'],m6-m4*m4/m2)

    def test_directional_endpoint_floors(self):
        m=self.module()
        for p,r,s,t,law in m.laws():
            m2,m4,m6=m.moments(law)
            for u2,u4 in ((m2,m4),(2*m2,2*m4)):
                f=m.directional(p,r,s,t,u2,u4)
                for q in (F(0),F(1,64),F(1,8),F(1,4)):
                    d,schur,tau=m.direct(m2,m4,m6,q)
                    self.assertLessEqual(f['det'],d)
                    self.assertLessEqual(f['schur'],schur)
                    self.assertLessEqual(f['tau'],tau)

    def test_no_probability_normalization_for_general_measure(self):
        m=self.module(); a2,a4,_=m.moments([(F(1),F(2))])
        residual=2*(1-a2)**2
        self.assertNotEqual(residual,a4-a2*a2)
        self.assertEqual(residual,a4-2*a2*a2+2*a2*a2)

    def test_homogeneous_scaling(self):
        m=self.module(); p,r,s,t=F(1,5),F(1,3),F(1),F(4)
        f=m.floors(p,r,s,t)
        for scale in (F(1,9),F(4),F(16)):
            g=m.floors(p,r,scale*s,scale*t)
            for key,power in (('m2',1),('gap',2),('delta',3)):
                self.assertEqual(g[key],f[key]*scale**power)

    def test_cli_baseline_and_each_exact_mutant(self):
        m=self.module()
        def run(*args):
            flags=['-B','-S'] if not sys.flags.optimize else ['-B','-O','-S']
            return subprocess.run([sys.executable,*flags,str(SIDE/'two_mass.py'),*args],capture_output=True,text=True,timeout=15)
        good=run(); self.assertEqual(good.returncode,0,good.stderr); self.assertEqual(good.stderr,'')
        j=json.loads(good.stdout);self.assertTrue(j['ok']);self.assertEqual(j['scientific_effect'],'NONE')
        for label,reason in m.MUTANTS.items():
            bad=run('--mutant',label)
            self.assertEqual(bad.returncode,1,(label,bad.stdout,bad.stderr));self.assertEqual(bad.stderr,'')
            self.assertEqual(json.loads(bad.stdout)['failed'],[reason])
        bad=run('--mutant','M9');self.assertEqual((bad.returncode,bad.stdout,bad.stderr),(2,'unknown mutant\n',''))

if __name__=='__main__': unittest.main(verbosity=2)
