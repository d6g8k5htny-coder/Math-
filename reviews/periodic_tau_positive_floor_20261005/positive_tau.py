"""Exact controls: orthogonal decomposition and direction/dimension-uniform variance band.

python -B -S positive_tau.py [--mutant M1|M2|M3|M4]
M1 omits gradient regression; M2 uses 3 instead of 9 for the mixed terms;
M3 uses 6 instead of 36 for the triple terms; M4 uses Delta alone as a
purported dimension-free lower bound. Tests are not the general proof.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
from math import factorial
import sys
MUTANT=None


def exact(x):
    if isinstance(x,bool) or isinstance(x,float):
        raise TypeError('use exact integers, Fraction, or rational/decimal strings')
    return F(x)


def moments(a,b,c):
    a,b,c=map(exact,(a,b,c))
    if a<=0 or b<a*a or c<b*b/a:
        raise ValueError('positive m2 and necessary moment inequalities required')
    return a,b,c


def simplex(t):
    t=tuple(map(exact,t))
    if not t or min(t)<0 or sum(t)!=1:
        raise ValueError('nonnegative nonempty simplex point of sum one required')
    return t


def monomial_weights(t):
    t=simplex(t)
    diagonal=sum(x**3 for x in t)
    mixed=3*sum(t[i]**2*t[j] for i in range(len(t)) for j in range(len(t)) if i!=j)
    triple=6*sum(t[i]*t[j]*t[k] for i,j,k in combinations(range(len(t)),3))
    return diagonal,mixed,triple


def variance_band(a,b,c):
    a,b,c=moments(a,b,c)
    delta=c-b*b/a
    coeff=(delta,3*a*(b-a*a),6*a**3)
    lower=delta if MUTANT=='M4' else min(coeff)
    return lower,max(coeff),delta


def decomposed_variance(a,b,c,t):
    a,b,c=moments(a,b,c)
    w=monomial_weights(t)
    mixed=a*(b-a*a) if MUTANT=='M2' else 3*a*(b-a*a)
    triple=a**3 if MUTANT=='M3' else 6*a**3
    return (c-b*b/a)*w[0]+mixed*w[1]+triple*w[2]


def compositions(n,d):
    if d==1:
        yield (n,)
        return
    for first in range(n+1):
        for rest in compositions(n-first,d-1):
            yield (first,)+rest


def simplex_grid(d,denominator):
    if type(d) is not int or d<1 or type(denominator) is not int or denominator<1:
        raise ValueError('positive integer dimension and denominator required')
    for ns in compositions(denominator,d):
        yield tuple(F(n,denominator) for n in ns)


def direct_schur(a,b,c,v):
    """Independent multinomial oracle; v need not be normalized.

    Dividing by (sum v_i^2)^3 avoids introducing irrational coordinates.
    The field covariance sign cancels in the regression norm squared.
    """
    a,b,c=moments(a,b,c);v=tuple(map(exact,v));norm2=sum(x*x for x in v)
    if norm2<=0:raise ValueError('nonzero direction required')
    table={0:F(1),2:a,4:b,6:c}
    def expectation(power,extra=None):
        total=F(0)
        for ns in compositions(power,len(v)):
            coefficient=factorial(power);term=F(1)
            for i,n in enumerate(ns):
                coefficient//=factorial(n)
                term*=v[i]**n*table.get(n+(i==extra),F(0))
            total+=coefficient*term
        return total
    variance=expectation(6)
    if MUTANT!='M1':variance-=sum(expectation(3,i)**2 for i in range(len(v)))/a
    return variance/norm2**3


def controls():
    counts={'schur_identities':0,'convex_weight_identities':0,'band_checks':0,
            'dimension_dependent_floor_checks':0,'positive_law_checks':0}
    def require(ok,label):
        if not ok:raise RuntimeError('POSITIVE_TAU_FAIL: '+label)
    laws=[(1,3,15),(F(5,2),F(17,2),F(65,2)),(1,1,1),
          (F(199,100),F(10099,100),F(1000099,100))]
    for d in range(1,6):
        for v in [(1,)*d,tuple(range(1,d+1)),tuple((-1)**i*(i+1) for i in range(d))]:
            norm2=sum(x*x for x in v);t=tuple(F(x*x,norm2) for x in v)
            for law in laws:
                require(decomposed_variance(*law,t)==direct_schur(*law,v),
                        'orthogonal decomposition versus full-gradient Schur oracle')
                counts['schur_identities']+=1
    for d in range(1,7):
        for t in simplex_grid(d,5):
            w=monomial_weights(t)
            require(sum(w)==1 and min(w)>=0,'convex monomial weights')
            counts['convex_weight_identities']+=1
            for law in laws:
                lo,hi,delta=variance_band(*law)
                value=decomposed_variance(*law,t)
                require(lo<=value<=hi,'dimension-free variance band')
                counts['band_checks']+=1
                require(value>=delta/d**2,'simplex floor')
                counts['dimension_dependent_floor_checks']+=1
                if delta>0:
                    require(lo>0,'positive moment-law floor')
                    counts['positive_law_checks']+=1
    require(variance_band(1,3,15)==(6,6,6),'Gaussian reference exact band')
    require(variance_band(1,1,1)[0]==0,'degenerate law not declared strictly positive')
    return {'object':'PERIODIC-TAU-POSITIVE-FLOOR-20261005-v1','passed':True,
            'counts':counts,'arithmetic':'exact rational','scientific_acceptance':False,
            'meaning':'finite controls; analytic proof and scope in NOTE.md'}


def main():
    global MUTANT
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mutant',choices=['M1','M2','M3','M4'])
    MUTANT=p.parse_args().mutant
    try:out=controls()
    except RuntimeError as error:
        print(str(error),file=sys.stderr);return 1
    print(json.dumps(out,sort_keys=True));return 0

if __name__=='__main__':sys.exit(main())
