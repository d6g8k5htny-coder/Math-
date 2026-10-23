"""Finite rational ledgers for the marked-Fourier sector transfer.

The arbitrary-law proof is NOTE.md. These helpers do not evaluate an infinite
covariance, certify unknown constants, or prove a statement about a field.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import ceil

MUTANT=None

def positive_integer(value:int,name:str)->int:
    if isinstance(value,bool) or not isinstance(value,int):
        raise TypeError(name+' must be an integer, not bool')
    if value<1:raise ValueError(name+' must be positive')
    return value

def log_power(d:int,s:F)->F:
    positive_integer(d,'dimension')
    s=F(s)
    if s<=0:raise ValueError('count power must be positive')
    return d*s if MUTANT=='M1' else d*s/2

def ledger(a:F,s:F,d:int)->dict:
    a=F(a);s=F(s)
    if a<0:raise ValueError('derivative power must be nonnegative')
    p=log_power(d,s)
    return {'rho':F(1,2) if MUTANT=='M2' else F(1),
            'Xi':F(1), 'log':p,
            'derivative_order':a if MUTANT=='M3' else 2*a,
            'scalar_order':2*s}

def envelope_order(u:F,gamma:F)->int:
    u=F(u);gamma=F(gamma)
    if u<=0 or gamma<=0:raise ValueError('positive power and gamma required')
    return max(0,ceil((u-1)/gamma))

def spike(d:int,j:int)->tuple[F,F,F,int]:
    positive_integer(d,'dimension');positive_integer(j,'index')
    if d<3 or j<2:raise ValueError('spike requires dimension>=3,index>=2')
    r=F(1,2**(j*j))
    return r,r**3,r**7,j**d

def marked_exponential(d:int,j:int)->int:
    spike(d,j) # domain validation
    return 2**(j**d if MUTANT=='M4' else j*j)

def log_bounds(j:int)->tuple[F,F]:
    positive_integer(j,'index')
    if j<2:raise ValueError('index>=2 required')
    coefficient=4*j*j-4
    return 1+F(coefficient,2),F(1+coefficient)

def count_exponential_at_zero()->int:
    return 1 if MUTANT=='M5' else 0

def falling(n:int,s:int)->int:
    if isinstance(n,bool) or not isinstance(n,int) or n<0:
        raise ValueError('nonnegative integer count required')
    positive_integer(s,'factorial degree')
    if n<s:return 0
    value=1
    for k in range(s):value*=n-k
    return value
