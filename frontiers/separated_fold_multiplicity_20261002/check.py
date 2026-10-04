"""Exact finite controls for the separated-fold manuscript.

These checks verify algebra and finite examples, not Gaussian support,
transversality, an implicit-function theorem, or a continuum persistence law.
Python standard library only. Numerical inputs must be exact integers/Fractions.
"""
from fractions import Fraction as F
import argparse
import json
import sys

MUTANT = None
MUTANTS = ('M1', 'M2', 'M3', 'M4', 'M5')


def rational(x):
    if type(x) not in (int, F):
        raise TypeError('an exact integer or Fraction is required')
    return F(x)


def fold_values(q, alpha=F(2)):
    q, alpha = rational(q), rational(alpha)
    if q <= 0 or not 1 <= alpha <= 3:
        raise ValueError('positive root and curvature in [1,3] required')
    mu = alpha*q*q/2
    birth = alpha*q**3/3
    gap = 2*birth if MUTANT != 'M1' else 2*alpha*q*q/3
    return mu, birth, -birth, gap


def cap_slack(a):
    a = rational(a)
    if not 0 < a <= F(1,8):
        raise ValueError('radius must be in (0,1/8]')
    delta, eta = a*a/100, a**3/100
    axial = (F(1,3)-F(1,24))*a**3-F(3,2)*delta*a-2*eta
    lateral = F(1,4)*(F(3,4)*a)**2
    return axial, lateral


def hessian(x, shear):
    x, shear = rational(x), rational(shear)
    return ((-2*x-shear*shear,shear),(shear,F(-1)))


def matrix(a):
    out = [[rational(x) for x in row] for row in a]
    if not out or any(len(row) != len(out) for row in out):
        raise ValueError('a nonempty square matrix is required')
    return out


def det(a):
    a=matrix(a); n=len(a); out=F(1)
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:
            return F(0)
        if pivot != j:
            a[j],a[pivot]=a[pivot],a[j]; out=-out
        p=a[j][j];out*=p
        for i in range(j+1,n):
            z=a[i][j]/p
            for k in range(j+1,n):a[i][k]-=z*a[j][k]
            a[i][j]=0
    return out


def solve(a,b):
    a=matrix(a);b=[rational(x) for x in b];n=len(a)
    if len(b)!=n:raise ValueError('incompatible right-hand side')
    a=[row+[z] for row,z in zip(a,b)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:raise ValueError('singular matrix')
        a[j],a[pivot]=a[pivot],a[j]
        p=a[j][j];a[j]=[v/p for v in a[j]]
        for i in range(n):
            if i!=j:
                z=a[i][j];a[i]=[x-z*y for x,y in zip(a[i],a[j])]
    return [row[-1] for row in a]


def row_error(a):
    a=matrix(a);n=len(a)
    if MUTANT=='M3':return max(abs(a[i][i]-1) for i in range(n))
    return max(sum(abs(a[i][j]-(i==j)) for j in range(n)) for i in range(n))


def lower_volume(n):
    if type(n) is not int:raise TypeError('integer multiplicity required')
    if n<1:raise ValueError('positive multiplicity required')
    return F(1,(4 if MUTANT=='M2' else 5)**n)


def exponent(n):
    lower_volume(n)
    return F(10,7) if MUTANT=='M5' and n==2 else F(2*n,3)


def measures(law):
    law=[(rational(p),tuple(marks)) for p,marks in law]
    if sum((p for p,_ in law),F(0))!=1 or any(p<0 for p,_ in law):
        raise ValueError('probability weights must sum to one')
    if any(type(x) is not str for _,marks in law for x in marks):
        raise TypeError('finite test marks must be strings')
    out={k:{} for k in ('I','J','R','R2')}
    out.update({k:F(0) for k in ('m','p','D','p1','p2','q2','tail')})
    for p,marks in law:
        n=len(marks)
        out['m']+=p*n
        out['p']+=p*(n>0)
        out['p1']+=p*(n==1);out['p2']+=p*(n==2)
        out['q2']+=p*(n>=2);out['D']+=p*n*(n>=2)
        out['tail']+=p*n*(n>=3)
        if not n:continue
        for x in marks:
            out['I'][x]=out['I'].get(x,F(0))+p
            weight=p/n if MUTANT!='M4' else p
            out['J'][x]=out['J'].get(x,F(0))+weight
            out['R'][x]=out['R'].get(x,F(0))+p-weight
            if n==2:out['R2'][x]=out['R2'].get(x,F(0))+p/2
    for name in ('I','J','R','R2'):
        out[name]={k:v for k,v in out[name].items() if v}
    return out


def tv(a,b):
    a={k:rational(v) for k,v in a.items()};b={k:rational(v) for k,v in b.items()}
    if sum(a.values())!=1 or sum(b.values())!=1 or any(x<0 for x in (*a.values(),*b.values())):
        raise ValueError('two probability measures are required')
    return sum((abs(a.get(k,0)-b.get(k,0)) for k in a.keys()|b.keys()),F(0))/2


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mutant')
    args=parser.parse_args()
    global MUTANT
    if args.mutant and args.mutant not in MUTANTS:
        parser.error('unknown mutant label')
    MUTANT=args.mutant
    # The tests import this exact running module, including the selected mutation.
    sys.modules['check']=sys.modules[__name__]
    import unittest
    suite=unittest.defaultTestLoader.loadTestsFromName('test_check')
    result=unittest.TextTestRunner(stream=sys.stderr,verbosity=0).run(suite)
    if not result.wasSuccessful():return 1
    print(json.dumps({'scientific_effect':'NONE','tests_passed':result.testsRun,
       'continuum_theorem_verified_by_tests':False,
       'fold_gap_squared_ratio_bounds':['32/27','32/9'],
       'axial_face_slack':'77/300 * a^3','lateral_face_drop':'9/64 * a^2',
       'parameter_volume_lower_constant':'5^(-n)',
       'multiplicity_exponent':'2n/3','two_bar_exponent':'4/3',
       'excess_vs_proposed_error_exponent':'4/3-10/7=-2/21',
       'mutants':list(MUTANTS)},sort_keys=True,indent=2))
    return 0

if __name__=='__main__':sys.exit(main())
