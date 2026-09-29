"""Exact finite helpers for mixed distance/height-gap powers.

These scalar identities do not verify the Gaussian proof. Standard library only.
"""
from fractions import Fraction as F

MUTANT = None

def parameters(q, beta):
    q, beta = F(q), F(beta)
    if q < 0 or beta < 0:
        raise ValueError('nonnegative inverse powers required')
    return q, beta

def combined(q, beta):
    q, beta = parameters(q,beta)
    return q + (beta if MUTANT == 'lose-cubic-gap' else 3*beta)

def finite(q, beta):
    lam = combined(q,beta)
    return lam <= 2 if MUTANT == 'include-boundary' else lam < 2

def alpha(q, beta):
    if not finite(q,beta):
        raise ValueError('positive finite mixed measure required')
    return (2-combined(q,beta))/3

def gap_moment(q,beta,n):
    a = alpha(q,beta)
    if type(n) is not int or n < 0:
        raise ValueError('nonnegative integer moment required')
    return a*(a+1)/((a+n)*(a+n+1))

def gap_variance(q,beta):
    return gap_moment(q,beta,2)-gap_moment(q,beta,1)**2

def square_density_factor(q,beta):
    a = alpha(q,beta)
    return a*(a+1)/(1 if MUTANT == 'omit-triangle-half' else 2)

def coefficient_parts(q,beta):
    """C, exponent of 12, k exponent, |T| exponent; omits 1/z0 and common integral."""
    q,beta = parameters(q,beta)
    if not finite(q,beta):
        raise ValueError('outside finite domain')
    lam = combined(q,beta)
    second = 5-q if MUTANT == 'uncoupled-denominator' else 5-lam
    factor = F(3,4)/((2-lam)*second)
    kp = (5-q)/3 - (0 if MUTANT == 'normalized-not-physical-gap' else beta)
    tp = (4+q)/3 - (beta if MUTANT == 'retain-beta-in-T' else 0)
    return factor, (2-q)/3, kp, tp

def overlap_integral(q,beta,k,t,smax):
    """Exact integral when smax=1, plus a rational scaling for integral powers.

Integral s^(1-q-3beta)|t|^-beta (k-s^3|t|)_+ ds.
This helper returns the dimensionless coefficient times k*smax^(2-q-3beta)
and the separate |t| exponent -beta rather than evaluating fractional powers.
    """
    q,beta=parameters(q,beta);k,t,smax=F(k),F(t),F(smax)
    if not finite(q,beta) or min(k,abs(t),smax)<=0 or k!=abs(t)*smax**3:
        raise ValueError('positive exact overlap root required')
    lam=combined(q,beta)
    return 3*k/((2-lam)*(5-lam)),2-lam,-beta

def envelope_powers(q,beta):
    return 1-combined(q,beta),-2-F(q)

def radial_power(d,beta):
    if type(d) is not int or d<2:
        raise ValueError('fixed dimension at least two required')
    beta=F(beta)
    if beta<0 or beta>=1:
        raise ValueError('weighted diagonal proof requires 0<=beta<1')
    # Polar + value-gradient density + dh' + determinant product + gap weight.
    jac = -d if MUTANT == 'wrong-height-frame' else -d-3
    return (d-1)+jac+3+2-3*beta

def cutoff_regime(q,beta):
    parameters(q,beta)
    if F(beta)>=1:
        raise ValueError('distance cutoff need not regularize height gap for beta>=1')
    lam=combined(q,beta)
    return 'finite' if lam<2 else ('logarithmic' if lam==2 else 'power')

def pole_parts(beta):
    """Limit of (2-q-3beta)D_qb as q increases to 2-3beta; beta<2/3."""
    beta=F(beta)
    if beta<0 or beta>=F(2,3):
        raise ValueError('fixed beta in [0,2/3) required')
    # Coefficient is 12^beta*k/(4*z0), T power 2-beta.
    return F(1,4),beta,F(1),2-beta

def integral_power_interval(power,left,right):
    """Finite exact integral for integer powers other than -1; endpoints positive."""
    if type(power) is not int or power==-1:
        raise ValueError('integer power other than logarithmic case required')
    left,right=F(left),F(right)
    if not 0<left<right:
        raise ValueError('ordered positive endpoints required')
    return (right**(power+1)-left**(power+1))/(power+1)

def height_correlation(q,beta):
    if MUTANT == 'independent-heights':
        return F(0)
    g1,g2=gap_moment(q,beta,1),gap_moment(q,beta,2)
    variance=F(1,12)-g1/6+g2/3
    covariance=F(1,12)-g1/6-g2/6
    return covariance/variance
