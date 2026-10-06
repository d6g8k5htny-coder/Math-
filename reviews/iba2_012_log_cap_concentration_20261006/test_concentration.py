#!/usr/bin/env python3
"""Exact finite controls only; no field simulation or continuum/formal verdict."""
from fractions import Fraction as F
import argparse
import json
import sys
import unittest
try:
    import concentration_check as core
except ModuleNotFoundError:
    core = None


class ConcentrationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(core, 'missing concentration_check implementation')

    def test_half_tail_and_normalization(self):
        self.assertEqual(core.tail_power(), F(1, 2))
        for beta in [4, 9, 15, 22]:
            for c in [F(1, 7), F(1, 3), F(2)]:
                for u in [8, 16, 128]:
                    y0 = core.shift(c, beta)
                    for y in [y0, y0+1, 2*y0]:
                        self.assertEqual(core.raw_exponent(c,beta,u,y), (beta+3-c*y/2)*u)
                        self.assertLessEqual(core.raw_exponent(c,beta,u,y), -c*u*y/4)

    def test_shifted_tail(self):
        for beta in [4, 9, 15]:
            c = F(1,3); y0 = core.shift(c,beta)
            self.assertGreaterEqual(y0, 1)
            self.assertGreaterEqual(c*y0/4,beta+3)
            for u in [8, 32, 1024]:
                for z in [F(0), F(1,7), F(1), F(10)]:
                    self.assertLessEqual(core.raw_exponent(c,beta,u,y0+z), -c*u*(y0+z)/4)

    def test_exponential_gap(self):
        for c in [F(1, 9), F(1,3), F(1)]:
            for u in [8, 16, 64]:
                self.assertEqual(core.kappa(c,u), c*u/8)
                self.assertEqual(core.layer_ratio(c,u), 1)
                self.assertGreater(c*u/4-core.kappa(c,u),0)

    def test_uniform_order_condition(self):
        c=F(1,3); beta=4; u=64; d=3
        upper=core.kappa(c,u)*core.shift(c,beta)/d
        self.assertTrue(core.eligible(upper,c,beta,u,d))
        self.assertFalse(core.eligible(upper+1,c,beta,u,d))
        for s in [F(1,2), F(1), F(4), F(12)]:
            self.assertEqual(core.eligible(s,c,beta,u,d), d*s<=core.kappa(c,u)*core.shift(c,beta))

    def test_growing_threshold(self):
        for d,B in [(3,F(4)),(4,F(9)),(5,F(15)),(3,F(13,4))]:
            self.assertEqual(core.critical_order(B,d),B/d)
            self.assertEqual(core.limiting_rate(B,F(1,2),d),-B+d*F(1,2))
            self.assertLess(core.limiting_rate(B,B/(2*d),d),0)
            self.assertGreater(core.limiting_rate(B,2*B/d,d),0)
            self.assertEqual(core.classify(B,B/d,d),'leading-order-zero')

    def test_critical_boundary(self):
        self.assertTrue(hasattr(core, 'boundary_exponent'), 'missing critical-boundary ledger')
        for B in [F(4),F(9),F(13,4)]:
            for u,lu,llu,ly in [(128,7,3,1),(1024,10,4,2),(4096,12,5,3)]:
                expected=B*u*(ly-llu)/lu
                self.assertEqual(core.boundary_exponent(B,u,lu,llu,ly),expected)
                self.assertLess(expected,0)

    def test_factorial_bracket(self):
        for N in range(1,35):
            for s in range(1,N+1):
                val=core.falling(N,s)
                lo,hi=core.log2_bracket(N,s,8)
                numer=val; denom=2**32
                self.assertLessEqual(F(2)**lo,F(numer,denom))
                self.assertLessEqual(F(numer,denom),F(2)**hi)
                if s<=N//2:
                    self.assertGreaterEqual(F(val,N**s),1-F(s*(s-1),2*N))
        with self.assertRaises(ValueError):
            core.log2_bracket(3,4,8)

    def test_dyadic_strict_sides(self):
        # Log-free integer brackets for theta*n/j, asymptotic to theta*Lambda.
        # No enormous probability or factorial is constructed for large j.
        for d in [3,4,5]:
            theta_lo=F(2,d); theta_hi=F(8,d)
            for j in [32,64,128]:
                for theta,side in [(theta_lo,-1),(theta_hi,1)]:
                    n,N,s=core.dyadic(j,d,theta)
                    lo,hi=core.log2_bracket(N,s,n)
                    if side<0: self.assertLess(hi,0)
                    else: self.assertGreater(lo,0)
                    self.assertLess(s*s,N)
                    target=-4+d*theta
                    self.assertLessEqual(F(lo,n),target)
                    self.assertGreater(target, F(lo,n)-1)

    def test_no_conditional_denominator(self):
        budget=F(1,8); actual=F(1,1024)
        self.assertEqual(core.budget_mass(actual,budget),F(1,128))
        self.assertNotEqual(core.budget_mass(actual,budget),1)
        # A probability on E divides by actual mass, which is NOT our finite measure.
        self.assertEqual(actual/actual,1)
        with self.assertRaises(ValueError): core.budget_mass(actual,F(0))

    def test_finite_mark_dependence(self):
        # Same-space Cauchy-Schwarz with correlated D,K and count event.
        law=[(F(1,2),F(1,2),1,0),(F(1,4),1,3,2),(F(1,4),2,7,11)]
        self.assertEqual(sum(w*D for w,D,K,N in law),1)
        for cutoff in [0,1,5,20]:
            lhs=sum((w*D*K for w,D,K,N in law if N>cutoff),F(0))
            tail=sum((w for w,D,K,N in law if N>cutoff),F(0))
            second=sum((w*D*D*K*K for w,D,K,N in law),F(0))
            self.assertLessEqual(lhs*lhs,second*tail)

    def test_domain_guards(self):
        for args in [(F(0),4),(F(-1),4),(F(1),-1)]:
            with self.assertRaises(ValueError): core.shift(*args)
        for d in [0,1,2]:
            with self.assertRaises(ValueError): core.critical_order(F(4),d)
        with self.assertRaises(ValueError): core.dyadic(1,3,F(1))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant',choices=['M1','M2','M3','M4','M5','M6'])
    args=parser.parse_args()
    if core is not None: core.MUTANT=args.mutant
    result=unittest.TextTestRunner(stream=sys.stderr,verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(ConcentrationTests))
    print(json.dumps({'ok':result.wasSuccessful(),'tests':result.testsRun,
        'failures':sorted({t.id().split('.')[-1] for t,_ in result.failures}),
        'errors':sorted({t.id().split('.')[-1] for t,_ in result.errors}),
        'mutant':args.mutant,'scope':'exact finite controls; no field or Lean verdict'},sort_keys=True,separators=(',',':')))
    return 2 if result.errors else (0 if result.wasSuccessful() else 1)


if __name__=='__main__': sys.exit(main())
