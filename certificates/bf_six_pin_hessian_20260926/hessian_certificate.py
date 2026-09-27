"""Exact finite regression and arithmetic checks. Read PROOF.md for analysis.

No floating point, network, third-party packages, or scientific-status writes.
The executable does not kernel-check infinite series or Gaussian conditioning.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
from math import factorial
from pathlib import Path
import sys

class Poly:
    """Small integer polynomial in formal variables r,c (not numerical samples)."""
    def __init__(self, terms=0):
        if type(terms) is int: terms={(0,0):terms}
        self.terms={k:v for k,v in terms.items() if v}
    @staticmethod
    def cast(x): return x if isinstance(x,Poly) else Poly(x)
    def __add__(self,other):
        other=self.cast(other);out=dict(self.terms)
        for k,v in other.terms.items():out[k]=out.get(k,0)+v
        return Poly(out)
    __radd__=__add__
    def __neg__(self):return Poly({k:-v for k,v in self.terms.items()})
    def __sub__(self,other):return self+-self.cast(other)
    def __rsub__(self,other):return self.cast(other)+-self
    def __mul__(self,other):
        out={}
        for (i,j),v in self.terms.items():
            for (k,l),w in self.cast(other).terms.items():out[i+k,j+l]=out.get((i+k,j+l),0)+v*w
        return Poly(out)
    __rmul__=__mul__
    def __pow__(self,n):
        if type(n) is not int or n<0:raise ValueError('nonnegative integer power required')
        out=Poly(1)
        for _ in range(n):out=out*self
        return out
    def __eq__(self,other):return self.terms==self.cast(other).terms

R=Poly({(1,0):1});C=Poly({(0,1):1})

def determinant(A):
    if not A:return Poly(1)
    return sum(((-1)**j*A[0][j]*determinant([row[:j]+row[j+1:] for row in A[1:]]) for j in range(len(A))),Poly(0))

def adjugate(A):
    n=len(A)
    return [[(-1)**(i+j)*determinant([row[:i]+row[i+1:] for k,row in enumerate(A) if k!=j]) for j in range(n)] for i in range(n)]

def regression_inputs():
    r,c=R,C
    G=[[Poly(1),Poly(0),c,-r*c],
       [Poly(0),Poly(1),r*c,(1-r**2)*c],
       [c,r*c,Poly(1),Poly(0)],
       [-r*c,(1-r**2)*c,Poly(0),Poly(1)]]
    return G,[Poly(-1),Poly(0),(r**2-1)*c,r*(3-r**2)*c]

def regression_check(G=None,b=None):
    if G is None and b is None:G,b=regression_inputs()
    if G is None or b is None:raise ValueError('both matrix and vector required')
    det=determinant(G);adj=adjugate(G)
    expected=1-(2+R**4)*C**2+C**4
    numerator=3*det-sum((b[i]*adj[i][j]*b[j] for i in range(4) for j in range(4)),Poly(0))
    expected_num=2+(-R**6+R**4-4*R**2-4)*C**2+(R**4+4*R**2+2)*C**4
    checks={'gram_determinant':det==expected,'schur_numerator':numerator==expected_num,
        'inverse_identity':all(sum((G[i][k]*adj[k][j] for k in range(4)),Poly(0))==(det if i==j else Poly(0)) for i in range(4) for j in range(4))}
    if not all(checks.values()):raise ValueError('regression polynomial identity failed')
    return checks

def ecoeff(n):return F(1,factorial(n)) if n>=0 else F(0)

def d_coeff(n):
    return (2**n-2)*ecoeff(n)+int(n==0)-ecoeff(n-2)

def a_coeff(n):
    return (2**(n+1)-4)*ecoeff(n)-4*ecoeff(n-1)+ecoeff(n-2)-ecoeff(n-3)+2*int(n==0)+4*int(n==1)+int(n==2)

def positivity_seeds():
    def seeds(fn,start,order):
        row=[int(fn(n)*factorial(n)) for n in range(start,start+order)];out=[]
        while row:
            out.append(row[0]);row=[b-a for a,b in zip(row,row[1:])]
        return out
    return {'D':seeds(d_coeff,4,3),'A':seeds(a_coeff,6,4)}

def axial_bounds(radius:F):
    if type(radius) is not F:raise TypeError('exact Fraction radius required')
    if not 0<radius<=F(1,40):raise ValueError('proved radius domain is 0<R<=1/40')
    x=radius**2
    D_upper=F(1,12)+F(4,15)*x/(1-x/3)
    A_upper=F(1,72)+F(16,315)*x/(1-x/4)
    return F(1,72)/D_upper,12*A_upper

def build_report():
    identities=regression_check();lo,hi=axial_bounds(F(1,40))
    if not F(1,7)<lo<=hi<F(1,5):raise ValueError('endpoint interval does not imply declared axial bounds')
    return {
      'object_id':'OA-BF-SIX-PIN-HESSIAN-20260926-v1','dimension':2,
      'model':'unperiodized planar Bargmann-Fock, K=exp(-|x-y|^2/2)',
      'conditioning':'six linear endpoint pins; no determinant or type reweighting',
      'coordinates':['f_tt(M)/r^2','f_ts(M)/r','f_ss(M)'],
      'r_domain':'0<r<=1/40','covariance_lower':'1/7','covariance_upper':'2',
      'diagonal_intervals':[['1/7','1/5'],['1599/3200','1/2'],['2','2']],
      'axial_internal_interval':[str(lo),str(hi)],'positivity_seeds':positivity_seeds(),
      'regression_polynomials':identities,
      'centered_residual_determinant_second_moment_upper':'23/20 * r^4',
      'moment_boundary':'H-E[H|P] only; not H, not Palm weight, not a normalizer',
      'scientific_status_authority':False,'scientific_effect':'NONE',
      'review_status':'REVIEW_REQUIRED','kernel_checked':False,
      'coverage':'finite polynomial identities and rational endpoint checks; analytic all-order proof separate'
    }

def validate_report(report):
    expected=build_report()
    # Canonical serialization distinguishes bool from int (Python dict equality does not).
    if json.dumps(report,sort_keys=True,allow_nan=False)!=json.dumps(expected,sort_keys=True,allow_nan=False):
        raise ValueError('certificate differs from complete generated scope or arithmetic')
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',type=Path);args=p.parse_args()
    if args.check:
        raw=args.check.read_bytes()
        if len(raw)>65536:raise ValueError('certificate too large')
        def pairs(items):
            out={}
            for k,v in items:
                if k in out:raise ValueError('duplicate JSON key')
                out[k]=v
            return out
        validate_report(json.loads(raw,object_pairs_hook=pairs))
    print(json.dumps(build_report(),indent=2,sort_keys=True))

if __name__=='__main__':
    try:main()
    except (ValueError,TypeError,OSError) as exc:
        print('REFUSED: '+str(exc),file=sys.stderr);sys.exit(1)
