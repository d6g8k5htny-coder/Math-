"""Exact algebra and envelope constants for a conditional saddle-kernel theorem.

Returned rational tail pairs mean prefactor*exp(-decay_argument). No floating
point enclosure or independent Gaussian theorem acceptance is claimed.
"""
from fractions import Fraction as Q
from math import factorial
import json


def exact(value):
    if isinstance(value,bool) or not isinstance(value,(int,Q)):
        raise TypeError('exact int/Fraction required')
    return Q(value)


def jets(k,u,v,w,theta):
    k,u,v,w,theta=map(exact,(k,u,v,w,theta))
    if k<=0 or v==0 or not 0<=theta<=1:
        raise ValueError('k>0, v!=0 and 0<=theta<=1 required')
    q=6*k*(w-2*u)/v
    c=12*k*(u*u+Q(1,4)-u*w)/v**2
    d=12*k*(2*u**3-Q(3,2)*u-Q(1,2)+theta)/v**3+3*q*(u*u-Q(1,4))/v**2
    A=3*k*(w+1-2*theta)/v**2
    return A,q,c,d


def determinant_factors(theta,w):
    theta,w=map(exact,(theta,w))
    if not 0<=theta<=1:
        raise ValueError('height fraction outside [0,1]')
    return (4*theta-(w+1)**2,
            4*(1-theta)-(w-1)**2,
            -((w+1-2*theta)**2+4*theta*(1-theta)))


def typed(theta,w):
    dm,ds,dx=determinant_factors(theta,w)
    return dm>0 and ds<0 and dx<0


def q_jacobian(k,v):
    k,v=map(exact,(k,v))
    if k<=0 or v==0:raise ValueError('k>0, v!=0 required')
    return 6*k/abs(v)


def kernel_prefactor(k,v,z0):
    k,v,z0=map(exact,(k,v,z0))
    if k<=0 or v==0 or z0<=0:raise ValueError('positive k,z0 and nonzero v required')
    return 104976*k**8/(z0*abs(v)**13)


def coercivity(k,u,v):
    k,u,v=map(exact,(k,u,v))
    if k<=0 or v==0:raise ValueError('k>0, v!=0 required')
    return 36*k*k*(u*u-Q(1,4))**2/(v*v*(u*u+v*v/4))


def gamma6_coefficients():
    # Gamma(6,x)=exp(-x)*P(x); coefficients in increasing powers.
    return [Q(factorial(5),factorial(j)) for j in range(6)]


def axis_tail(B,C,c,eps):
    """Rectangle-envelope integral, exact pair (prefactor, decay_argument).

    Assumes Lambda<=C |v|^-13 exp(-c/v²) on |u|<=B, |v|<=eps.
    Constants B,C,c,eps must be supplied; they are not certified here.
    """
    B,C,c,eps=map(exact,(B,C,c,eps))
    if min(B,C,c,eps)<=0:raise ValueError('positive envelope inputs required')
    x=c/eps**2
    P=sum((a*x**j for j,a in enumerate(gamma6_coefficients())),Q(0))
    return 2*B*C/c**6*P,x


def absorption(p,n,c):
    if type(p) is not int or type(n) is not int or p<0 or n<0:
        raise ValueError('nonnegative integer powers required')
    c=exact(c)
    if c<=0:raise ValueError('positive decay required')
    order=(p+n+1)//2
    return order,Q(factorial(order))/c**order


def monotone_radius_squared(p,c):
    if type(p) is not int or p<=0:raise ValueError('positive integer power required')
    c=exact(c)
    if c<=0:raise ValueError('positive decay required')
    return 2*c/p


def scope():
    return {
        'object':'D5-CONTACT-KERNEL-TAIL-20260925-v1',
        'kernel_prefactor_integer':104976,
        'kernel_inverse_transverse_power':13,
        'kernel_gap_power':8,
        'upper_gamma_order':6,
        'required_gluing_inputs':['PR25_C1_fixed_transverse_uniform_limit','PR28_normalized_finite_r_strip_envelope'],
        'full_annulus_asymptotic_accepted':False,
        'probability_lower_bound':False,
        'global_RN_closed':False,
        'scientific_effect':'NONE',
        'meaning':'finite algebra checks and conditional composition, not scientific acceptance',
    }

if __name__=='__main__':print(json.dumps(scope(),indent=2,sort_keys=True))
