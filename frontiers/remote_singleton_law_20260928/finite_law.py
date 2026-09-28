"""Exact finite probability algebra. Not a Gaussian or continuum verifier."""
from fractions import Fraction as F


def exact(x):
    if isinstance(x,bool) or not isinstance(x,(int,F)):
        raise TypeError('int or Fraction required')
    return F(x)


def validate(p):
    if not isinstance(p,dict):raise TypeError('finite law must be a dictionary')
    if any(not isinstance(c,tuple) or any(type(x) is not int or x<0 for x in c)
           or tuple(sorted(c))!=c for c in p):
        raise ValueError('sorted tuples of nonnegative integer atoms required')
    vals=[exact(v) for v in p.values()]
    if any(v<0 for v in vals) or sum(vals)!=1:
        raise ValueError('probabilities must be nonnegative and sum to one')


def mean_measure(p):
    validate(p); mu={}
    for c,w in p.items():
        for x in c:
            mu[x]=mu.get(x,F(0))+w
    return mu


def multiple_point_mass(p):
    validate(p)
    return sum((len(c)*w for c,w in p.items() if len(c)>=2),F(0))


def factorial(p):
    validate(p)
    return sum((len(c)*(len(c)-1)*w for c,w in p.items()),F(0))


def bernoulli(mu):
    if not isinstance(mu,dict):raise TypeError('measure must be a dictionary')
    vals={x:exact(v) for x,v in mu.items()}
    if any(type(x) is not int or x<0 for x in vals) or any(v<0 for v in vals.values()):
        raise ValueError('nonnegative measure on integer atoms required')
    m=sum(vals.values(),F(0))
    if m>1:raise ValueError('Bernoulli mean cannot exceed one')
    return {():1-m,**{(x,):v for x,v in vals.items()}}


def tv(p,q):
    """Half total mass norm; inputs used as probabilities in the tests."""
    return sum((abs(exact(p.get(c,0))-exact(q.get(c,0))) for c in set(p)|set(q)),F(0))/2


def nonempty(p):
    validate(p)
    mass=sum((w for c,w in p.items() if c),F(0))
    if mass==0:raise ValueError('nonempty event has zero probability')
    return {c:w/mass for c,w in p.items() if c}


def unique(p):
    validate(p); mass=sum((w for c,w in p.items() if len(c)==1),F(0))
    if mass==0:raise ValueError('singleton event has zero probability')
    return {c:w/mass for c,w in p.items() if len(c)==1}


def conditional_multiple_bound(q,p):
    q,p=map(exact,(q,p))
    if q<0 or not 0<p<=1:raise ValueError('nonnegative factorial moment, positive event probability required')
    return q/(2*p)
