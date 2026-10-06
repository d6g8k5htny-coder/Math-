#!/usr/bin/env python3
"""Finite exact controls, not a continuum proof or a field simulation."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import sys
import unittest

source = Path(__file__).with_name('log_cap_check.py')
mod = None
if source.exists():
    spec = importlib.util.spec_from_file_location('log_cap_check', source)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

class LogCapTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(mod, 'missing log_cap_check.py implementation')

    def test_beta_and_mixed(self):
        self.assertEqual([mod.beta(q) for q in range(1,5)], [4,9,15,22])
        self.assertEqual(mod.mixed_power((F(1,2),F(1,4))), F(13,4))
        self.assertEqual(mod.mixed_power((F(2),F(1))), 9)

    def test_transfer_ledger(self):
        self.assertEqual(mod.ledger(3,(F(1),),F(1)), (F(7),F(3)))
        self.assertEqual(mod.ledger(3,(F(1),),F(2)), (F(7),F(6)))
        self.assertEqual(mod.ledger(4,(F(1),F(1)),F(1)), (F(12),F(4)))
        self.assertEqual(mod.ledger(4,(F(1,2),F(1,4)),F(3,2)),(F(25,4),F(6)))

    def test_tail_quarter(self):
        self.assertEqual(mod.holder_powers(), (F(1,4),)*4)
        self.assertEqual(sum(mod.holder_powers()), 1)
        for q in range(1,7):
            for c in [F(1,3),F(1),F(2),F(19)]:
                A=mod.cutoff_constant(q,c)
                self.assertGreaterEqual(A,1)
                self.assertGreaterEqual(c*A/4,mod.beta(q)+4)

    def test_cutoff_shape_and_scale(self):
        # These are exact coefficient controls for T=A^d*(u/log u)^d.
        for d in range(3,9):
            self.assertEqual(mod.cutoff_powers(d), (d,-d))
        for j in range(2,12):
            n=2**j
            for d in [3,4,6]:
                case=mod.spike(j,d)
                self.assertEqual(case['v'],n//j)
                self.assertEqual(case['count'],(n//j)**d)
                self.assertEqual(case['r'],F(1,2**n))

    def test_spike_probabilities_and_thresholds(self):
        for j in range(2,10):
            for d in [3,4,5]:
                c=mod.spike(j,d);r=c['r']
                self.assertGreater(c['zero'],0)
                self.assertEqual(c['zero']+c['ordinary']+c['rare'],1)
                for eta in [F(0),r/2,r,2*r,F(1,2)]:
                    mass=c['rare'] if eta>=r else F(0)
                    self.assertLessEqual(mass,r**3*(eta+r)**4)

    def test_abstract_tail_majorant(self):
        # Bounds phi(t)/log2 <= 3*d*n on the only nonzero t>=4 tail interval.
        for j in range(2,12):
            for d in range(3,8):
                c=mod.spike(j,d);n=c['n'];v=c['v'];M=c['count']
                self.assertLessEqual(M+2,(v+1)**d)
                self.assertLessEqual(v+1,F(3,2)*v)
                self.assertLessEqual(v+1,2**(j+1))
                self.assertLessEqual(F(3,2)*v*d*(j+1),3*d*n)
                self.assertLessEqual(F(3*d*n,d),7*n)

    def test_fixed_moments_and_sharp_ratio(self):
        for j in range(2,10):
            c=mod.spike(j,3);r=c['r'];M=c['count']
            for s in range(1,6):
                moment=2**s*c['ordinary']+M**s*c['rare']
                self.assertEqual(moment/r**3,2**s+r**4*M**s)
                ratio=mod.spike_ratio(j,3,s)
                self.assertEqual(ratio,F(M**s,16))
                self.assertLessEqual(c['v'],F(c['n'],j))
                self.assertGreaterEqual(c['v'],F(c['n'],2*j))

    def test_four_factor_holder_correlated(self):
        probs=[F(1,3)]*3
        densities=[F(1,2),F(1),F(3,2)]
        K=[1,3,2];N=[1,2,5];psi=[x+2 for x in N]
        self.assertEqual(sum(p*z for p,z in zip(probs,densities)),1)
        for a in range(0,4):
            for s in range(1,4):
                for T in [1,3,4,6,9]:
                    lhs,rhs=mod.holder_finite(probs,densities,K,psi,a,s,T)
                    self.assertLessEqual(lhs**4,rhs)

    def test_truncation_keeps_event(self):
        probs=[F(1,2),F(1,4),F(1,4)]
        K=[2,1,3];N=[0,2,7];psi=[n+2 for n in N];E=[False,True,True]
        for T in [1,4,9]:
            for s in [1,2,3]:
                low,bound=mod.truncation(probs,K,N,psi,E,2,s,T)
                self.assertLessEqual(low,bound)
                true_low=sum((p*k**2*n**s for p,k,n,z,e in zip(probs,K,N,psi,E) if e and z<=T),F(0))
                self.assertEqual(low,true_low)

    def test_single_full_normalizer(self):
        for r in [F(1,2),F(1,8),F(1,32)]:
            W=[r*r,3*r*r];probs=[F(1,2),F(1,2)]
            Z=sum(p*w for p,w in zip(probs,W))
            densities=mod.normalized_weights(W,Z)
            self.assertEqual(densities,[F(1,2),F(3,2)])
            self.assertEqual(sum(p*x for p,x in zip(probs,densities)),1)

    def test_zero_threshold_and_remote_guard(self):
        for q in range(1,6):
            for r in [F(1,2),F(1,8)]:
                Xi=mod.xi([F(0)]*q,r)
                self.assertEqual(Xi,r**mod.beta(q))
                self.assertLessEqual(r**(mod.beta(q)+4),r**3*Xi)
        self.assertFalse(mod.local_event(0,[F(0)],[F(1,2)]))
        self.assertTrue(mod.local_event(1,[F(0)],[F(0)]))

    def test_input_rejection_and_factorial_mass(self):
        for call in [lambda:mod.beta(0),lambda:mod.cutoff_constant(1,0),
                     lambda:mod.spike(1,3),lambda:mod.spike(3,1),
                     lambda:mod.ledger(3,(F(1),F(1)),1),
                     lambda:mod.mixed_power((F(1,4),F(1,2))),
                     lambda:mod.normalized_weights([1],0)]:
            with self.assertRaises(ValueError):call()
        for n in range(0,12):
            for s in range(1,6):
                self.assertLessEqual(mod.falling(n,s),n**s)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant',choices=['M1','M2','M3','M4','M5'])
    args=parser.parse_args()
    if mod is not None:mod.MUTANT=args.mutant
    result=unittest.TextTestRunner(stream=sys.stderr,verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(LogCapTests))
    print(json.dumps({'ok':result.wasSuccessful(),'tests':result.testsRun,'mutant':args.mutant,
                     'failures':[str(x) for x,_ in result.failures],
                     'errors':[str(x) for x,_ in result.errors],
                     'scope':'exact finite controls; not a continuum or kernel proof'},sort_keys=True,separators=(',',':')))
    return 2 if result.errors else (0 if result.wasSuccessful() else 1)
if __name__=='__main__':sys.exit(main())
