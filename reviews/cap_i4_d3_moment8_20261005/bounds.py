"""Exact algebra for a source-bound d3 eighth-moment sufficiency proposal.

These functions are finite controls only. They do not construct Gaussian fields,
perform spectral change of variables, or invoke a theorem prover.
"""
from fractions import Fraction as F
from math import comb, factorial

def low_region(s: F, J: F) -> bool:
    if not (0 < s <= 1 and J >= 1):
        raise ValueError('require 0<s<=1 and J>=1')
    return s*s*J*J <= 1

def hard_low(L: F, K: F) -> F:
    if L < 0 or K <= 0:
        raise ValueError('require L>=0, K>0')
    return K + (1+K)*L

def low_integrated(r: F, J: F, L: F, K: F, k: F) -> F:
    if not (0 < r <= 1 and J >= 1 and L >= 0 and K > 0 and k > 0):
        raise ValueError('outside coefficient domain')
    U=J+L; D=4*K*K/(3*k); E=3*K/2
    return (K*K/4)*r**5*L*L*hard_low(L,K)*(D**3*U**8/3+E*D*D*U**7/2)

def power8(J: F, L: F) -> F:
    if J < 0 or L < 0:
        raise ValueError('nonnegative power inputs required')
    return 128*(J**8+L**8)

def high_polynomial(r: F, J: F, L: F, K: F) -> F:
    if not (0 < r <= 1 and J >= 1 and L >= 0 and K > 0):
        raise ValueError('outside weight domain')
    U=J+L
    return (K*K/4)*(r**2*U**2*L**4+(5*K/2)*r**3*U**3*L**3+(3*K*K/2)*r**4*U**4*L**2)

def tail8(s: F, J: F, q: int) -> F:
    if not (0 < s <= 1 and J >= 1 and s*J >= 1 and q in (2,3,4)):
        raise ValueError('requires high residual sector and q in {2,3,4}')
    return s**(8-q)*J**8

def half_gaussian(n: int, sqrt_c: F) -> tuple[F,bool]:
    """Integral_0^infty x^n exp(-c*x^2): coefficient and sqrt(pi) flag."""
    if type(n) is not int or n < 0 or sqrt_c <= 0:
        raise ValueError('invalid Gaussian moment arguments')
    if n % 2:
        j=(n-1)//2
        return F(factorial(j),2)/sqrt_c**(n+1),False
    value=F(1,2)
    for j in range(1,n//2+1):
        value*=F(2*j-1,2)
    return value/sqrt_c**(n+1),True

def tail_gaussian_polynomial(q: int) -> dict[int,F]:
    if q not in (2,3,4):
        raise ValueError('q must be 2,3,4')
    return {8-q+j:F(comb(q,j),2) for j in range(q+1)}

def tail_radius(s: F, q: int) -> F:
    if not (0 < s <= 1 and q in (2,3,4)):
        raise ValueError('invalid radius ledger input')
    return s**(2*q)*s**(8-q)

def dyadic_moment(q: int) -> F:
    if type(q) is not int or q >= 8:
        raise ValueError('finite dyadic moment requires integer q<8')
    return F(255,256)/(1-F(2)**(q-8))

def truncated_eighth(N: int) -> F:
    if type(N) is not int or N < 0:
        raise ValueError('nonnegative integer cutoff required')
    return sum((F(255,256)*F(2)**(-8*n)*F(2)**(8*n) for n in range(N+1)),F(0))

def counter_lower_scaled(N: int) -> F:
    return truncated_eighth(N)/12

def normalized_bounds(r: F, C: F, cZ: F, M4: F, k: F) -> tuple[F,F]:
    if not (0 < r <= 1 and C >= 0 and cZ > 0 and M4 >= 0 and k > 0):
        raise ValueError('invalid full-normalizer inputs')
    return C*r**5/(cZ*r**2), r**2*M4*(10*r/(3*k))**4/(cZ*r**2)
