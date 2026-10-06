#!/usr/bin/env python3
"""Independent exact controls for comment6008747995 Part B (not a Lean proof).

Standard-library polynomial coefficient identities and rational test inputs.
No import from either mathematical packet. --mutant is a deliberately wrong
review-control formula, not a modification of a repository source.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import itertools
import json
import sys

NVAR = 5  # x, g, X, G, t
class P:
    def __init__(self, value=0):
        self.c = ({e: Q(a) for e, a in value.items() if a}
                  if isinstance(value, dict) else ({(0,)*NVAR: Q(value)} if value else {}))
    @staticmethod
    def var(index):
        e = [0]*NVAR; e[index] = 1
        return P({tuple(e): 1})
    def __add__(self, other):
        other = other if isinstance(other, P) else P(other)
        c = dict(self.c)
        for e, a in other.c.items(): c[e] = c.get(e, Q(0)) + a
        return P(c)
    __radd__ = __add__
    def __neg__(self): return P({e: -a for e, a in self.c.items()})
    def __sub__(self, other): return self + -(other if isinstance(other, P) else P(other))
    def __rsub__(self, other): return P(other) + -self
    def __mul__(self, other):
        other = other if isinstance(other, P) else P(other)
        c = {}
        for e, a in self.c.items():
            for f, b in other.c.items():
                ef = tuple(i+j for i,j in zip(e,f))
                c[ef] = c.get(ef, Q(0)) + a*b
        return P(c)
    __rmul__ = __mul__
    def __pow__(self, n):
        if type(n) is not int or n < 0: raise ValueError('nonnegative exponent required')
        out = P(1)
        for _ in range(n): out *= self
        return out

def f0(x,g): return g*(g+2*x)/(g+x)
def f1(x,g): return 4*x*(g+2*x)/(g+4*x)
def endpoints(x,g): return x*(g+x), g*(g+4*x)/4
def schur(x,g,t):
    d0,d1 = endpoints(x,g)
    return x*g*(g+2*x)/((1-4*t)*d0+4*t*d1)
def original_schur(x,g,t):
    a = g+x-2*(g-2*x)*t
    c = x+2*(g-2*x)*t
    d = x*(g+x)+(g-2*x)*(g+2*x)*t
    return a-(c**3+(2*c+a)*(g-2*x)**2*t*(1-4*t))/d

def run(mutant=None):
    failures=[]; counts={}
    def expect(ok,group):
        if not ok and group not in failures: failures.append(group)
    x,g,X,G,t = [P.var(i) for i in range(NVAR)]
    d0 = x*(g+x); d1 = Q(1,4)*g*(g+4*x); n=x*g*(g+2*x)
    d = x*(g+x)+(g-2*x)*(g+2*x)*t
    a = g+x-2*(g-2*x)*t; c=x+2*(g-2*x)*t
    sign = -1 if mutant=='flip_difference_sign' else 1
    factor = 2 if mutant=='omit_F1_factor_four' else 4
    identities = {
      'F0_x_difference':g*(g+2*X)*(g+x)-g*(g+2*x)*(g+X)-sign*g**2*(X-x),
      'F0_g_difference':G*(G+2*x)*(g+x)-g*(g+2*x)*(G+x)-(G-g)*(G+x)*(g+x)-x**2*(G-g),
      'F1_x_difference':4*X*(g+2*X)*(g+4*x)-4*x*(g+2*x)*(g+4*X)-2*(X-x)*(g+4*X)*(g+4*x)-2*g**2*(X-x),
      'F1_g_difference':4*x*(G+2*x)*(g+4*x)-4*x*(g+2*x)*(G+4*x)-8*x**2*(G-g),
      'determinant_interpolation':d-(1-4*t)*d0-4*t*d1,
      'original_schur_cancellation':a*d-c**3-(2*c+a)*(g-2*x)**2*t*(1-4*t)-n,
      'endpoint0':n*(g+x)-g*(g+2*x)*d0,
      'endpoint1':n*(g+4*x)-factor*x*(g+2*x)*d1,
      'dominance0':g*(g+2*x)-g*(g+x)-g*x,
      'dominance1':4*x*(g+2*x)-2*x*(g+4*x)-2*x*g,
    }
    for name, residual in identities.items(): expect(not residual.c,'symbolic:'+name)
    counts['polynomial_identities']=len(identities)
    values=[Q(1,64),Q(1,4),Q(1),Q(2),Q(9),Q(64)]
    inc=[Q(0),Q(1,7),Q(2),Q(19)]
    exact_count=0
    for x,g,dx,dg in itertools.product(values,values,inc,inc):
        X,G=x+dx,g+dg
        claims=[
          (f0(X,g)-f0(x,g),g*g*dx/((g+X)*(g+x))),
          (f0(x,G)-f0(x,g),dg+x*x*dg/((G+x)*(g+x))),
          (f1(X,g)-f1(x,g),2*dx+2*g*g*dx/((g+4*X)*(g+4*x))),
          (f1(x,G)-f1(x,g),8*x*x*dg/((G+4*x)*(g+4*x))),
        ]
        for left,right in claims:
            expect(left==right,'rational_differences'); exact_count+=1
            expect(left<=0 if mutant=='reverse_monotone_direction' else left>=0,'monotonicity')
    counts['rational_difference_equalities']=exact_count
    dirs=0; dominance=0; endpoint_min=0; original_equalities=0
    for s0,g0,dx,dg in itertools.product(
          [Q(1,8),Q(1,2),Q(1),Q(5,4),Q(3),Q(8)],
          [Q(1,16),Q(1,4),Q(9,8),Q(2),Q(7),Q(64)],
          [Q(0),Q(1,7),Q(3)],[Q(0),Q(1,5),Q(5)]):
        x0=s0*s0; x=x0+dx; g=g0+dg
        supplied_x=s0 if mutant=='square_input_missing' else x0
        choice=max if mutant=='max_for_min' else min
        h=choice(f0(supplied_x,g0),f1(supplied_x,g0))
        expect(h>=min(g0,2*x0),'dominance'); dominance+=1
        expect(min(schur(x,g,Q(0)),schur(x,g,Q(1,4)))==min(f0(x,g),f1(x,g)),'endpoint_min'); endpoint_min+=1
        for k in range(17):
            t=Q(k,64)
            d0,d1=endpoints(x,g)
            expect((1-4*t)*d0+4*t*d1>0,'denominator_positivity')
            expect(schur(x,g,t)>=h,'direction_floor'); dirs+=1
            expect(original_schur(x,g,t)==schur(x,g,t),'native_formula_correspondence'); original_equalities+=1
    counts.update(direction_inequalities=dirs,dominance_checks=dominance,
                  endpoint_minimum_checks=endpoint_min,native_formula_equalities=original_equalities)
    x0,g0=Q(25,16),Q(9,8)
    ex=min(f0(x0,g0),f1(x0,g0))
    target=Q(153,85 if mutant=='example_wrong_denominator' else 86)
    expect(ex==target and ex/Q(9,8)==Q(68,43),'example')
    # Deliberate excluded-direction inputs: denominator stays positive but claimed bound fails.
    outside=[(Q(1),Q(1),Q(-1)),(Q(1),Q(4),Q(1))]
    for x,g,t in outside:
        d0,d1=endpoints(x,g)
        expect((1-4*t)*d0+4*t*d1>0 and schur(x,g,t)<min(f0(x,g),f1(x,g)),'direction_scope_counterexample')
    # Boundary switch g=2x must retain equality of both endpoint expressions.
    for x in values:
        expect(f0(x,2*x)==f1(x,2*x)==Q(8,3)*x,'equal_endpoints')
    counts.update(example_checks=1,outside_direction_counterexamples=2,equal_endpoint_cases=len(values))
    return {'scope':'exact algebra and finite controls for comment6008747995 Part B; not a Lean or field verdict',
            'mutant':mutant,'counts':counts,'failures':sorted(failures),
            'errors':[],'ok':not failures,'example_floor':str(ex),'example_gain':str(ex/Q(9,8))}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mutant',choices=['flip_difference_sign','omit_F1_factor_four','max_for_min',
                                      'square_input_missing','reverse_monotone_direction','example_wrong_denominator'])
    args=p.parse_args()
    report=run(args.mutant)
    print(json.dumps(report,sort_keys=True,separators=(',',':')))
    return 0 if report['ok'] else 1
if __name__=='__main__': sys.exit(main())
