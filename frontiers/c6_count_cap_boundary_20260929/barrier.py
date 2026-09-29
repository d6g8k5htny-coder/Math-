"""Exact finite rare-count and size-bias controls. No Gaussian model is implemented."""
from fractions import Fraction as F

MUTANT=None

def integer(n, minimum=0):
    if type(n) is not int or n<minimum:
        raise ValueError('integer parameter outside domain')
    return n

def falling(n,q):
    integer(n); integer(q)
    out=1
    for i in range(q):
        out*=max(n-i,0)
    return out

def rare_law(n,d):
    integer(n,3); integer(d,2)
    r=F(1,n**n)
    k=n**(2 if MUTANT=='planar-only-cap' else d)
    power=2 if MUTANT=='wrong-rarity' else 3
    return r,k,r**power/k

def rare_factorial(n,d,q):
    integer(q,1)
    _,k,p=rare_law(n,d)
    value=k**q if MUTANT=='ordinary-not-factorial' else falling(k,q)
    return p*value

def size_biased(law):
    if not isinstance(law,dict) or not law:
        raise ValueError('finite probability dictionary required')
    law={integer(n):F(p) for n,p in law.items()}
    if any(p<0 for p in law.values()) or sum(law.values())!=1:
        raise ValueError('probabilities must be nonnegative and sum to one')
    mean=sum(n*p for n,p in law.items())
    if mean<=0:
        raise ValueError('positive first moment required')
    if MUTANT=='nonempty-not-size-biased':
        mass=1-law.get(0,F(0))
        return {n:p/mass for n,p in law.items() if n and p}
    return {n:n*p/mean for n,p in law.items() if n and p}

def tilt_cost(weight_power,normalizer_power):
    w,z=F(weight_power),F(normalizer_power)
    return w if MUTANT=='drop-normalizer' else w-z

def count_cap(n,d):
    _,k,_=rare_law(n,d)
    return k+(0 if MUTANT=='omit-prescribed-pins' else 2)

def exact_tail(n,d,threshold):
    _,_,p=rare_law(n,d)
    x=F(threshold); cap=count_cap(n,d)
    if x<2:return F(1)
    return p if x<cap else F(0)
