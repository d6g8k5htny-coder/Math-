"""Exact finite identities for local rare-intensity tightness. No Gaussian checker."""
from fractions import Fraction as F
from math import ceil, prod

MUTANT=None

def positive(*xs):
    if any(F(x)<=0 for x in xs): raise ValueError('positive parameters required')

def reduced_third(A,U,V,W,q):
    A,U,V,W,q=map(F,(A,U,V,W,q))
    return A-(2 if MUTANT=='wrong-schur-derivative' else 3)*q*U+3*q*q*V-q**3*W

def hermite_constant(r,k):
    positive(r,k)
    return (6 if MUTANT=='half-hermite' else 12)*F(k)

def soft_threshold(R,r,K,k):
    positive(R,r,K,k);R,r,K,k=map(F,(R,r,K,k))
    if R<1 or K<k: raise ValueError('R>=1 and K>=k required')
    return 64*(R+1)**2*r*K**(1 if MUTANT=='linear-norm-threshold' else 2)/k

def model_extra_x(k,lam,a):
    positive(k,lam)
    if not a: raise ValueError('nonzero mixed coefficient required')
    return -12*F(k)*F(lam)/F(a)**2

def norm_tail(r,C,p,M):
    positive(r,C,M)
    if type(p) is not int or p<1: raise ValueError('positive integer moment required')
    return F(C)*F(r)**(0 if MUTANT=='lose-rare-scale' else 3)/F(M)**p

def mixed_power():
    return 4+1+3-(4 if MUTANT=='normalizer-twice' else 2)

def boundary_volume(J,eps):
    positive(J,eps)
    return 2*F(eps)*(2*F(J))**3

def global_rates(a1,a2,remote):
    positive(a1,a2,remote)
    return {1:F(a1)+(0 if MUTANT=='omit-remote-singletons' else F(remote)),2:F(a2)}

def factorial_coefficient(rates,p):
    if type(p) is not int or p<1: raise ValueError('positive integer order required')
    return sum((mass*prod(n-j for j in range(p)) for n,mass in rates.items() if n>=p),F(0))

def decomposition_error(middle,mixed):
    if min(F(middle),F(mixed))<0: raise ValueError('nonnegative errors required')
    return 3*((0 if MUTANT=='ignore-middle-region' else F(middle))+F(mixed))

def nonempty_double(rates):
    return F(rates[2])/sum(rates.values())

def palm_excess(rates):
    denom=sum(rates.values()) if MUTANT=='palm-equals-nonempty' else sum(n*p for n,p in rates.items())
    return sum(n*(n-1)*p for n,p in rates.items())/denom

def absorption_order(loss,target,a):
    positive(a)
    return max(0,ceil((F(loss)+F(target))/F(a)))
