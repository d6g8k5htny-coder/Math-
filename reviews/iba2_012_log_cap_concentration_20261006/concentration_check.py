"""Finite rational ledgers for the conditional log-cap concentration note.

This module does not evaluate field constants or certify logarithms. The
logarithmic comparisons and infinite-family limits are written proofs.
"""
from fractions import Fraction as F

MUTANT = None


def tail_power():
    return F(1) if MUTANT == 'M1' else F(1, 2)


def shift(c, beta):
    c=F(c)
    if c<=0 or beta<0:
        raise ValueError('need c>0 and beta>=0')
    offset=2 if MUTANT=='M2' else 3
    return max(F(1),4*(F(beta)+offset)/c)


def raw_exponent(c,beta,u,y):
    return (F(beta)+3-F(c)*tail_power()*F(y))*F(u)


def kappa(c,u):
    if F(c)<=0 or F(u)<=0:
        raise ValueError('positive tail constant and logarithmic scale required')
    return F(c)*F(u)/(16 if MUTANT=='M3' else 8)


def layer_ratio(c,u):
    k=kappa(c,u)
    return k/(F(c)*F(u)/4-k)


def eligible(s,c,beta,u,d):
    if F(s)<=0 or not isinstance(d,int) or isinstance(d,bool) or d<3:
        raise ValueError('need s>0 and integer d>=3')
    v=F(s) if MUTANT=='M4' else d*F(s)
    return v<=kappa(c,u)*shift(c,beta)


def critical_order(B,d):
    if F(B)<=0 or not isinstance(d,int) or isinstance(d,bool) or d<3:
        raise ValueError('need B>0 and integer d>=3')
    return F(B)/((2*d) if MUTANT=='M5' else d)


def limiting_rate(B,theta,d):
    critical_order(B,d)
    return -F(B)+(2*d if MUTANT=='M5' else d)*F(theta)


def classify(B,theta,d):
    rate=limiting_rate(B,theta,d)
    return 'decays' if rate<0 else ('grows' if rate>0 else 'leading-order-zero')


def falling(N,s):
    if not isinstance(N,int) or not isinstance(s,int) or N<0 or s<0:
        raise ValueError('nonnegative integer count and degree required')
    ans=1
    for i in range(s): ans*=max(0,N-i)
    return ans


def log2_bracket(N,s,n):
    if not 1<=s<=N or n<1:
        raise ValueError('need 1<=s<=N and n>=1')
    lower=(N-s+1).bit_length()-1
    upper=(N-1).bit_length()
    return (s*lower-4*n,s*upper-4*n)


def dyadic(j,d,theta):
    if not isinstance(j,int) or j<2 or d<3 or F(theta)<=0:
        raise ValueError('need integer j>=2,d>=3 and theta>0')
    n=2**j
    v=n//j
    s=(F(theta)*n/j).__floor__()
    return n,v**d,s


def budget_mass(actual,budget):
    actual,budget=F(actual),F(budget)
    if actual<0 or budget<=0:
        raise ValueError('need nonnegative actual mass and positive budget')
    if MUTANT=='M6': return F(1) if actual else F(0)
    return actual/budget


def boundary_exponent(B,u,log_u,log_log_u,log_y0):
    """Algebraic exponent at theta=B/d; logarithms are supplied symbolic values."""
    if F(B)<=0 or F(u)<=0 or F(log_u)<=0:
        raise ValueError('positive B,u,log_u required')
    return F(B)*F(u)*(F(log_y0)-F(log_log_u))/F(log_u)
