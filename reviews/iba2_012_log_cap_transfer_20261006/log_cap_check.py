"""Exact finite algebra for the log-cap transfer note; no numerical field constants.

MUTANT is a test-only switch. The tests, not these helpers, assign pass/fail.
Transcendental tail inversion and all infinite-family limits are proved in NOTE.md.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import prod

MUTANT: str | None = None


def beta(q: int) -> int:
    if type(q) is not int or q < 1:
        raise ValueError('positive integer q required')
    return q*(q+7)//2


def mixed_power(alphas) -> F:
    values=tuple(F(a) for a in alphas)
    if not values or any(a<=0 for a in values) or any(a<b for a,b in zip(values,values[1:])):
        raise ValueError('positive nonincreasing exponents required')
    return sum(((j+2)*min(a,F(1)) for j,a in enumerate(values,2)),F(0))


def ledger(d: int, alphas, s) -> tuple[F,F]:
    values=tuple(alphas);s=F(s)
    if type(d) is not int or d<3 or len(values)>d-2 or s<=0:
        raise ValueError('fixed d>=3, 1<=q<=d-2 and s>0 required')
    radial=(0 if MUTANT=='M3' else 3)+mixed_power(values)
    logarithmic=((d-1) if MUTANT=='M2' else d)*s
    return radial,logarithmic


def holder_powers() -> tuple[F,...]:
    return (F(1,4),)*4


def cutoff_constant(q: int, c) -> F:
    c=F(c)
    if c<=0:raise ValueError('positive tail constant required')
    factor=1 if MUTANT=='M1' else 4
    return max(F(1),F(factor*(beta(q)+4))/c)


def cutoff_powers(d: int) -> tuple[int,int]:
    if type(d) is not int or d<3:raise ValueError('integer d>=3 required')
    return d, -d


def spike(j: int, d: int) -> dict:
    if type(j) is not int or j<2 or type(d) is not int or d<3:
        raise ValueError('integers j>=2,d>=3 required')
    n=2**j
    v=n if MUTANT=='M4' else n//j
    r=F(1,2**n)
    ordinary=r**3;rare=r**7
    return dict(j=j,d=d,n=n,v=v,count=v**d,r=r,ordinary=ordinary,rare=rare,zero=1-ordinary-rare)


def spike_ratio(j:int,d:int,s:int) -> F:
    c=spike(j,d)
    return c['rare']*c['count']**s/(c['r']**3*(2*c['r'])**4)


def holder_finite(probs,densities,K,psi,a:int,s:int,T):
    rows=list(zip(probs,densities,K,psi,strict=True))
    lhs=sum((p*z*k**a*x**s for p,z,k,x in rows if x>T),F(0))
    rhs=(sum((p*z**4 for p,z,k,x in rows),F(0))
         *sum((p*k**(4*a) for p,z,k,x in rows),F(0))
         *sum((p*x**(4*s) for p,z,k,x in rows),F(0))
         *sum((p for p,z,k,x in rows if x>T),F(0)))
    return lhs,rhs


def truncation(probs,K,N,psi,E,a:int,s:int,T):
    rows=list(zip(probs,K,N,psi,E,strict=True))
    low=sum((p*k**a*n**s for p,k,n,x,e in rows if e and x<=T),F(0))
    bound=T**s*sum((p*k**a for p,k,n,x,e in rows if e),F(0))
    return low,bound


def normalized_weights(weights,Z) -> list[F]:
    Z=F(Z);weights=[F(w) for w in weights]
    if Z<=0 or any(w<0 for w in weights):raise ValueError('positive full normalizer and nonnegative weights required')
    return weights if MUTANT=='M5' else [w/Z for w in weights]


def xi(thresholds,r) -> F:
    values=[F(x) for x in thresholds];r=F(r)
    if not values or not 0<r<=F(1,2) or any(not 0<=x<=F(1,2) for x in values) or any(a>b for a,b in zip(values,values[1:])):
        raise ValueError('ordered thresholds in [0,1/2], 0<r<=1/2 required')
    return prod(((eta+r)**(j+2) for j,eta in enumerate(values,2)),start=F(1))


def local_event(local_count:int,soft,thresholds) -> bool:
    return local_count>0 and all(x<=eta for x,eta in zip(soft,thresholds,strict=True))


def falling(n:int,s:int) -> int:
    if type(n) is not int or type(s) is not int or n<0 or s<1:
        raise ValueError('integer n>=0 and integer s>=1 required')
    return 0 if n<s else prod(range(n-s+1,n+1))
