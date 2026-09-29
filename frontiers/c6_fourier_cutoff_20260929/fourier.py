"""Exact finite companions for C6 Fourier cutoff. Not a Gaussian proof checker."""
from fractions import Fraction as F
from math import prod

MUTANT = None

def dimension(d):
    if type(d) is not int or d < 2:
        raise ValueError('fixed integer dimension at least two required')
    return d

def clear_laurent(terms, d, m):
    dimension(d)
    if type(m) is not int or m < 1:
        raise ValueError('positive integer cutoff required')
    out={}
    shift = 0 if MUTANT == 'omit-monomial' else m
    for n, c in terms.items():
        if len(n)!=d or any(type(k) is not int or abs(k)>m for k in n):
            raise ValueError('exponent outside integer Fourier box')
        key=tuple(k+shift for k in n)
        out[key]=out.get(key,F(0))+F(c)
    return {n:c for n,c in out.items() if c}

def evaluate(terms, w):
    if any(F(x)==0 for x in w):
        raise ValueError('nonzero Laurent coordinates required')
    return sum((F(c)*prod(F(x)**n for x,n in zip(w,ns)) for ns,c in terms.items()),F(0))

def bezout_cap(d,m):
    dimension(d)
    if type(m) is not int or m<1: raise ValueError('positive cutoff required')
    degree=2*m if MUTANT=='degree-without-dimension' else 2*d*m
    power=2 if MUTANT=='planar-cap-everywhere' else d
    return degree**power

def count_tail_power(d):
    dimension(d)
    return F(1) if MUTANT=='exponential-all-dimensions' else F(2,d)

def decay_coefficients(d,a=F(1)):
    dimension(d);a=F(a)
    if a<=0: raise ValueError('positive rate required')
    cut=a/d if MUTANT=='oversized-lipschitz-cutoff' else a/(4*d)
    # Coefficients of m^2 in the three NEGATIVE exponential bounds.
    return {'remainder':2*a,'sublevel':a-(2*d-1)*cut,'lipschitz':2*cut}

def mean_log_power(d,p):
    dimension(d)
    if type(p) is not int or p<2: raise ValueError('integer factorial order >=2 required')
    return F(p-1) if MUTANT=='planar-log-everywhere' else F(d*(p-1),2)

def success_up_to(success,m):
    if m<1: return False
    return bool(success.get(m,False)) if MUTANT=='single-cutoff-event' else any(success.get(n,False) for n in range(1,m+1))

def regression_second_moment(var,cov,target):
    """One standardized observation. Full conditional second moment includes mean."""
    var,cov,target=map(F,(var,cov,target))
    if var<0 or cov*cov>var: raise ValueError('joint covariance must be positive semidefinite')
    mean=cov*target
    return var-cov*cov+(0 if MUTANT=='drop-conditional-mean' else mean*mean)

def rare_count(d,m,p=2):
    dimension(d)
    if type(m) is not int or m<2 or type(p) is not int or p<1: raise ValueError('invalid example indices')
    n=m**d; mean=F(1,2**(3*m*m));prob=mean/n
    factorial=prod(n-j for j in range(p)) if n>=p else 0
    return {'count':n,'probability':prob,'mean':prob*n,'factorial':prob*factorial}

def tail_after_tilt(c):
    c=F(c)
    if c<=0: raise ValueError('positive rate required')
    return c if MUTANT=='drop-cauchy-square-root' else c/2

def square_margin(a,b,x):
    a,b,x=map(F,(a,b,x))
    if a<=0: raise ValueError('positive Gaussian rate required')
    return a*x*x/2+b*b/(2*a)-b*x
