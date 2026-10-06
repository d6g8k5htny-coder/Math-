#!/usr/bin/env python3
"""Exact finite controls; not Gaussian simulation or continuum verification."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import importlib.util
from itertools import permutations
import json
from math import factorial
from pathlib import Path
import sys
import unittest

module_path=Path(__file__).with_name('marked_entropy_check.py')
H=None
if module_path.exists():
    spec=importlib.util.spec_from_file_location('marked_entropy_check',module_path)
    H=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(H)

class TransferTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(H,'implementation missing; expected RED phase')

    def test_log_power(self):
        for d in range(3,9):
            for s in [F(1,2),F(1),F(3,2),F(2),F(4)]:
                self.assertEqual(H.log_power(d,s),F(d)*s/2)

    def test_single_rho_and_soft_power(self):
        for a in [F(0),F(1,2),F(3)]:
            for s in [F(1,2),F(1),F(3)]:
                row=H.ledger(a,s,5)
                self.assertEqual(row['rho'],1)
                self.assertEqual(row['Xi'],1)
                self.assertEqual(row['log'],F(5)*s/2)

    def test_derivative_moment(self):
        for a in [F(0),F(1,4),F(2),F(7,2)]:
            row=H.ledger(a,F(3,2),3)
            self.assertEqual(row['derivative_order'],2*a)
            self.assertEqual(row['scalar_order'],3)

    def test_polynomial_tail_envelope(self):
        # theta=log(2), gamma=2/d. 1/2<log(2) makes this bound rational.
        for d in range(2,7):
            for u in range(1,6):
                k=H.envelope_order(F(u),F(2,d))
                self.assertGreaterEqual(k*F(2,d),u-1)
                C=factorial(k)*4**k
                for j in range(1,9):
                    n=j**d; y=j*j
                    self.assertLessEqual(n**(2*(u-1)),C*C*2**y)
        self.assertEqual(H.envelope_order(F(1,2),F(2,3)),0)

    def test_restricted_tail_with_exact_exponent(self):
        for d in [2,3,4]:
            law=[(F(1,2),0),(F(1,4),1),(F(1,8),2**d),(F(1,8),4**d)]
            M=sum((p*n*2**(0 if n==0 else (1 if n==1 else (4 if n==2**d else 16))) for p,n in law),F())
            for u in [1,2,3]:
                k=H.envelope_order(F(u),F(2,d)); C=factorial(k)*4**k
                T=2**d
                tail=sum((p*n**u for p,n in law if n>T),F())
                self.assertLessEqual(tail**2,M**2*C**2*F(1,2**4))

    def test_correlated_weight_split(self):
        for d in [3,4]:
            law=[(F(1,2),0,1,False),(F(1,8),1,9,True),
                 (F(1,8),2**d,2,True),(F(1,8),3**d,1,True),
                 (F(1,8),4**d,20,False)]
            for a in [0,1,2]:
                for s in [1,2,3]:
                    lhs=sum((w*k**a*n**s for w,n,k,e in law if e),F())
                    derivative=sum((w*k**(2*a) for w,n,k,e in law if e),F())
                    count=sum((w*n**(2*s) for w,n,k,e in law if e),F())
                    self.assertLessEqual(lhs**2,derivative*count)

    def test_all_thresholds_in_spike(self):
        for d in [3,4,5]:
            for j in range(2,8):
                r,rho,rare,n=H.spike(d,j)
                self.assertEqual(n,j**d)
                self.assertLess(rho+rare,1)
                for eta in [F(0),r/2,r,2*r,F(1,2)]:
                    event=rare if eta>=r else F()
                    self.assertLessEqual(event,rho*(eta+r)**4)

    def test_marked_budget_uniform_bound(self):
        # Ordinary count 2 has 2^(2^(2/d))<=4 for d>=2.
        for d in range(3,8):
            C=8+factorial(d)*2**(d-1)
            for j in range(2,16):
                r,rho,rare,n=H.spike(d,j)
                rare_scaled=rare/rho*n*H.marked_exponential(d,j)
                self.assertLessEqual(8+rare_scaled,C)

    def test_gamma_not_ordinary_exponential(self):
        for d in [3,4,5]:
            for j in [2,3,5]:
                self.assertEqual(H.marked_exponential(d,j),2**(j*j))
                self.assertNotEqual(H.marked_exponential(d,j),2**(j**d))

    def test_log_comparison_for_spike(self):
        # L=1+(4j²-4)log2, 1/2<log2<1; hence j² <= L <=4j².
        for j in range(2,41):
            lo,hi=H.log_bounds(j)
            self.assertLessEqual(j*j,lo)
            self.assertLessEqual(lo,hi)
            self.assertLessEqual(hi,4*j*j)

    def test_sharp_ratio(self):
        for d in [3,4,5]:
            for j in range(2,9):
                r,rho,rare,n=H.spike(d,j)
                for s in [1,2,3]:
                    ratio=rare*n**s/(rho*(2*r)**4)
                    self.assertEqual(ratio,F(j**(d*s),16))
                    lo,hi=H.log_bounds(j)
                    # Squaring avoids half-integral powers.
                    self.assertLessEqual(lo**(d*s)/(256*4**(d*s)),ratio**2)
                    self.assertLessEqual(ratio**2,hi**(d*s)/256)

    def test_unmarked_normalization_guard(self):
        for j in range(2,7):
            r,rho,rare,n=H.spike(3,j)
            zero_mass=1-rho-rare
            self.assertGreater(zero_mass/rho,1)
            self.assertEqual(H.count_exponential_at_zero(),0)

    def test_remote_and_zero_power(self):
        N,NR,K=7,0,3
        soft=True; event=(NR>0 and soft)
        self.assertEqual(NR**2*int(soft),0)
        self.assertEqual(N**2*int(event),0)
        self.assertGreater(N**2*int(soft),0)
        self.assertNotEqual(int(soft),int(event))

    def test_tuple_mass(self):
        for n in range(0,7):
            for s in range(1,5):
                actual=sum(1 for _ in permutations(range(n),s))
                self.assertEqual(H.falling(n,s),actual)
                self.assertLessEqual(actual,n**s)

    def test_invalid_domains(self):
        for d,s in [(True,F(1)),(0,F(1)),(3,F(0)),(3,F(-1))]:
            with self.assertRaises((TypeError,ValueError)):H.log_power(d,s)
        for u,g in [(F(0),F(1)),(F(1),F(0))]:
            with self.assertRaises(ValueError):H.envelope_order(u,g)
        for d,j in [(3,0),(3,1),(True,3),(3,True)]:
            with self.assertRaises((TypeError,ValueError)):H.spike(d,j)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mutant',choices=['M1','M2','M3','M4','M5'])
    args=ap.parse_args()
    if H is not None:H.MUTANT=args.mutant
    result=unittest.TextTestRunner(stream=sys.stderr,verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(TransferTests))
    report={'ok':result.wasSuccessful(),'tests':result.testsRun,'mutant':args.mutant,
            'failures':sorted({t.id().split('.')[-1] for t,_ in result.failures}),
            'errors':sorted({t.id().split('.')[-1] for t,_ in result.errors}),
            'scope':'exact finite controls, not a continuum or field verdict'}
    print(json.dumps(report,sort_keys=True,separators=(',',':')))
    return 2 if result.errors else (0 if result.wasSuccessful() else 1)
if __name__=='__main__':sys.exit(main())
