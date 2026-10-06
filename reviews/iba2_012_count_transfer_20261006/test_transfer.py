"""Exact finite controls for PROOF.md; not a Gaussian-field or Lean replay."""
from __future__ import annotations
import importlib.util
import json
import subprocess
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class TransferTests(unittest.TestCase):
    def load(self):
        path = ROOT / 'transfer_check.py'
        self.assertTrue(path.is_file(), 'implementation file is absent')
        spec = importlib.util.spec_from_file_location('transfer_check', path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_beta_and_codimension(self):
        m=self.load()
        for q in range(1,8):
            self.assertEqual(m.beta(q), q*(q+7)//2)
            self.assertEqual(m.beta(q),sum(j+2 for j in range(2,q+2)))
        with self.assertRaises(ValueError): m.beta(0)

    def test_mixed_cutoffs_saturate(self):
        m=self.load()
        self.assertEqual(m.radial_exponent([F(1,2),F(1,4)],1,4),F(87,16))
        self.assertEqual(m.radial_exponent([F(2)],1,4),F(6))
        self.assertEqual(m.radial_exponent([F(1)],1,2),F(5))
        with self.assertRaises(ValueError):m.radial_exponent([F(1,4),F(1,2)],1,4)

    def test_holder_domain(self):
        m=self.load()
        self.assertEqual(m.theta(1,2),F(1,2))
        for s,p in [(2,2),(3,2),(0,2),(-1,3)]:
            with self.assertRaises(ValueError):m.theta(s,p)

    def test_stirling_factorial_identity(self):
        m=self.load()
        for p in range(1,10):
            for n in range(21):
                self.assertEqual(n**p,sum(m.stirling(p,j)*m.falling(n,j) for j in range(1,p+1)))

    def test_exact_holder_finite_laws(self):
        m=self.load()
        cases=0
        for atoms in m.fixtures():
            for p in range(2,7):
                for s in range(1,p):
                    for t in [0,1]:
                        lhs,rhs=m.holder_sides(atoms,s,p,t)
                        self.assertLessEqual(lhs,rhs)
                        cases+=1
        self.assertEqual(cases,360)

    def test_empty_event(self):
        m=self.load()
        self.assertEqual(m.holder_sides([(F(1),2,3,False)],1,3,1),(0,0))

    def test_positive_count_intensity_deletion(self):
        m=self.load()
        atoms=[(F(1,2),0,1,False),(F(1,4),2,1,False),(F(1,4),5,2,True)]
        for s in range(4):
            self.assertEqual(m.positive_mass_removed(atoms,s),F(5**s,4))

    def test_rare_spike_probability_and_moments(self):
        m=self.load()
        for n in range(1,21):
            atoms=m.spike(n,4)
            self.assertEqual(sum(row[0] for row in atoms),1)
            self.assertTrue(all(row[0]>=0 for row in atoms))
            r=F(1,2**n)
            for p in range(1,7):
                self.assertEqual(m.expect(atoms,p), r**3*(2**p+(n+3)**p*r**4))

    def test_no_loss_countermodel(self):
        m=self.load()
        for s in [1,2,3]:
            vals=[]
            for n in [1,2,4,8,16,32]:
                atoms=m.spike(n,4);r=F(1,2**n)
                ratio=m.positive_mass_removed(atoms,s)/(r**3*(2*r)**4)
                self.assertEqual(ratio,F((n+3)**s,16));vals.append(ratio)
            self.assertEqual(vals,sorted(vals))
            self.assertGreater(vals[-1],vals[0])

    def test_no_third_factorial_lower_bound(self):
        m=self.load()
        for n in range(1,8):
            r=F(1,2**n)
            atoms=[(1-r**3,0,1,False),(r**3,2,1,False)]
            self.assertEqual(sum(w*m.falling(x,2) for w,x,_,_ in atoms),2*r**3)
            self.assertEqual(sum(w*m.falling(x,3) for w,x,_,_ in atoms),0)

    def test_cli_baseline_and_determinism(self):
        self.load(); outputs=[]
        for flags in [[],['-O']]:
            p=subprocess.run([sys.executable,'-B','-S',*flags,str(ROOT/'transfer_check.py')],capture_output=True,text=True,timeout=15)
            self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(p.stderr,'')
            out=json.loads(p.stdout);self.assertIs(out['ok'],True)
            self.assertFalse(out['scientific_acceptance']);outputs.append(p.stdout)
        self.assertEqual(*outputs)

    def test_named_wrong_formulas_and_unknown_label(self):
        self.load()
        for label,failed in [('M1','mixed_scale'),('M2','rare_radial_scale'),('M3','stirling'),('M4','no_loss'),('M5','third_factorial')]:
            p=subprocess.run([sys.executable,'-B','-S',str(ROOT/'transfer_check.py'),'--mutant',label],capture_output=True,text=True,timeout=15)
            self.assertEqual(p.returncode,1,p.stderr);self.assertEqual(p.stderr,'')
            self.assertEqual(json.loads(p.stdout)['failed'],[failed])
        p=subprocess.run([sys.executable,'-B','-S',str(ROOT/'transfer_check.py'),'--mutant','M9'],capture_output=True,text=True,timeout=15)
        self.assertEqual(p.returncode,2);self.assertEqual(p.stdout,'unknown mutant\n');self.assertEqual(p.stderr,'')

if __name__=='__main__':
    unittest.main(verbosity=2)
