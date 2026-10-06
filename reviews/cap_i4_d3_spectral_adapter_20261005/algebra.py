"""Rational identities used by the d=3 spectral-adapter checks.

No random field, Gaussian distribution, integral evaluator, or Lean kernel is
implemented here. Irrational Gaussian-moment constants are tracked symbolically.
"""
from fractions import Fraction as F
from math import factorial


def det3(a):
    if len(a) != 3 or any(len(row) != 3 for row in a):
        raise ValueError('expected a 3 by 3 matrix')
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def spectral_entries(lam, top, cosine, sine):
    if lam > top or cosine*cosine+sine*sine != 1:
        raise ValueError('ordered eigenvalues and a unit-circle point required')
    t=(lam+top)/2; rho=(top-lam)/2
    return t+rho*cosine, rho*sine, t-rho*cosine


def normalization_ledger():
    return {'entry_angular_over_pi': F(1),
            'cartesian_to_trace_absdet': F(2),
            'spectral_to_trace_absdet': F(1,2),
            'frobenius_over_entry_squared': F(2)}


def soft_primitive(upper, shift):
    return upper**3/3 + shift*upper**2/2


def weight_majorant(lam, top, J, r, K):
    if not (0 <= lam <= top and J >= 1 and 0 < r <= 1 and K > 0):
        raise ValueError('outside positive ordered compact-radius domain')
    U=J+top; A=K*K*(1+K)/4; E=3*K/2
    return A*r*r*top*U**3*lam*(lam+E*r*U)


def post_soft_majorant(top, J, r, K, k_floor):
    if not (top >= 0 and J >= 1 and 0 < r <= 1 and K > 0 and k_floor > 0):
        raise ValueError('positive radius, moments and mark floor required')
    D=4*K*K/(3*k_floor); E=3*K/2; A=K*K*(1+K)/4
    return A*(D**3/3+E*D*D/2)*r**5*top*top*(J+top)**9


def ninth_power_envelope(J, top):
    if J < 0 or top < 0:
        raise ValueError('nonnegative inputs required')
    return 256*(J**9+top**9)


def gaussian_half_moment(n, sqrt_c):
    """Return (rational coefficient, multiply_by_sqrt_pi) for c=sqrt_c**2."""
    if type(n) is not int or n < 0 or sqrt_c <= 0:
        raise ValueError('nonnegative integer degree and positive sqrt(c) required')
    if n % 2:
        k=(n-1)//2
        return F(factorial(k),2)/sqrt_c**(2*k+2), False
    k=n//2
    coeff=F(1,2)
    for j in range(1,k+1):
        coeff*=F(2*j-1,2)
    return coeff/sqrt_c**(2*k+1), True


def gaussian_square_gap(z, mean):
    if len(z) != len(mean):
        raise ValueError('incompatible vectors')
    return sum(((a-2*b)**2/2 for a,b in zip(z,mean)),F(0))


def normalized_depth(C, z_floor, r):
    if C < 0 or z_floor <= 0 or r <= 0:
        raise ValueError('invalid full-normalizer inputs')
    return (C*r**5)/(z_floor*r**2)


def diagonal_bernoulli():
    return {(0,0):F(1,2),(1,1):F(1,2)}


def support_transfer_sums(atoms):
    if any(W < 0 or (W > 0 and good and not G) for W,good,G in atoms):
        raise ValueError('weighted-support implication not supplied')
    return (sum((W for W,good,G in atoms if not G),F(0)),
            sum((W for W,good,G in atoms if not good),F(0)))


def two_atom_moments(T):
    if T <= 1:
        raise ValueError('T must exceed one')
    p=1/T**8
    return (1-p)+p*T**8, (1-p)+p*T**9
