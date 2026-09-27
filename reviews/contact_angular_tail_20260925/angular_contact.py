"""Exact contact algebra and floating-point diagnostic helpers.

Only Python standard library. The Gaussian helpers are not interval enclosures.
The proofs and dependency boundaries are in NOTE.md.
"""
from __future__ import annotations
from fractions import Fraction as Q
import math


def exact(value: int | Q) -> Q:
    if type(value) is int or isinstance(value,Q):
        return Q(value)
    raise TypeError('integer or Fraction required; floats and booleans are refused')


def contact_coordinates(k,u,v,w,theta):
    k,u,v,w,theta=map(exact,(k,u,v,w,theta))
    if k<=0 or v==0 or not 0<=theta<=1:
        raise ValueError('positive k, nonzero v, and theta in [0,1] required')
    D=u*u-Q(1,4)
    q=6*k*(w-2*u)/v
    c=12*k*(u*u+Q(1,4)-u*w)/(v*v)
    d=6*k*(-2*u**3-Q(3,2)*u-1+2*theta+3*w*D)/(v**3)
    A=(12*k*u+6*k+q*v-12*k*theta)/(2*v*v)
    return {'q':q,'c':c,'d':d,'A':A}


def type_factors(w,theta):
    w,theta=map(exact,(w,theta))
    return (4*theta-(w+1)**2,
            (w-1)**2-4*(1-theta),
            (w+1-2*theta)**2+4*theta*(1-theta))


def typed_scaled_product(k,w,theta):
    k=exact(k);theta=exact(theta)
    if k<=0:raise ValueError('positive k required')
    f=type_factors(w,theta)
    return (9*k*k)**3*math.prod(f) if 0<theta<1 and min(f)>0 else Q(0)


def _mul(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out


def type_polynomial(theta):
    theta=exact(theta)
    # P_theta(w) = positive determinant-factor product on the typed interval.
    a=[4*theta-1,Q(-2),Q(-1)]
    b=[4*theta-3,Q(-2),Q(1)]
    c=[Q(1),2-4*theta,Q(1)]
    return _mul(_mul(a,b),c)


def left_channel(k,u):
    k,u=map(exact,(k,u))
    if k<=0 or not -Q(3,2)<u<-1:
        raise ValueError('left-channel theorem requires k>0 and -3/2<u<-1')
    D=u*u-Q(1,4)
    return (-6*k*D/u,u+Q(1,4)/u,-(2*u-3)*(2*u+1)**3/(32*u))


def cd_coordinates(k,u,v,c,d):
    k,u,v,c,d=map(exact,(k,u,v,c,d))
    if k<=0 or u==0 or v==0:raise ValueError('positive k and nonzero u,v required')
    D=u*u-Q(1,4)
    Q0=-6*k*D/u
    w0=u+Q(1,4)/u
    theta0=-(2*u-3)*(2*u+1)**3/(32*u)
    q=Q0/v-c*v/(2*u)
    w=w0-c*v*v/(12*k*u)
    theta=theta0+c*D*v*v/(8*k*u)+d*v**3/(12*k)
    return q,w,theta


def left_rate(k,u):
    Q0,_,_=left_channel(k,u)
    return Q0*Q0/4


def right_rate(k,u):
    k,u=map(exact,(k,u))
    if k<=0 or u<=Q(1,2):raise ValueError('requires k>0 and u>1/2')
    return 12*k*k*(u-Q(1,2))**6


def ledger():
    return {'contact_prefactor_power':-13,'left_prefactor_power':-8,
            'change_to_cd_power':4,'cd_prefactor_power':-2}


def gaussian_moments(a:float,b:float,degree:int=6):
    """Integral z^j exp(-z^2/2) dz, j=0..degree, moderate finite endpoints.

    Floating-point evaluation only. Extreme-tail subtraction may lose accuracy;
    do not use as a certified quadrature or a probability lower bound.
    """
    a,b=float(a),float(b)
    if not math.isfinite(a+b) or b<a or type(degree) is not int or not 0<=degree<=6:
        raise ValueError('finite ordered endpoints and degree 0..6 required')
    e_a,e_b=math.exp(-a*a/2),math.exp(-b*b/2)
    i0=math.sqrt(math.pi/2)*(math.erf(b/math.sqrt(2))-math.erf(a/math.sqrt(2)))
    out=[i0]
    if degree:out.append(e_a-e_b)
    for j in range(2,degree+1):out.append((j-1)*out[j-2]+a**(j-1)*e_a-b**(j-1)*e_b)
    return out


def gaussian_polynomial_integral(coeff,precision,mean,lo,hi):
    """Closed recurrence for a polynomial times exp(-precision*(w-mean)^2/2)."""
    precision,mean,lo,hi=map(float,(precision,mean,lo,hi))
    coeff=list(map(float,coeff))
    if not 1<=len(coeff)<=7 or precision<=0 or not math.isfinite(precision+mean):
        raise ValueError('degree<=6 and finite positive precision required')
    root=math.sqrt(precision)
    moments=gaussian_moments(root*(lo-mean),root*(hi-mean),len(coeff)-1)
    return sum(p*sum(math.comb(j,i)*mean**(j-i)*moments[i]/root**(i+1)
                     for i in range(j+1)) for j,p in enumerate(coeff))


def bf_z0(b:float,k:float):
    """Full endpoint contact normalizer for unperiodized exp(-|h|^2/2)."""
    b,k=float(b),float(k)
    if k<=0 or not math.isfinite(b+k):raise ValueError('finite b and positive k required')
    x=b/math.sqrt(2)
    phi=math.exp(-x*x/2)/math.sqrt(2*math.pi)
    Phi=(1+math.erf(x/math.sqrt(2)))/2
    moment=(b*b+2)*Phi+b*math.sqrt(2)*phi
    if moment<=0:raise ArithmeticError('normalizer underflow/cancellation; use higher precision')
    return 36*k*k*moment


def left_amplitude(b:float,k:float,u:float):
    b,k,u=float(b),float(k),float(u)
    if not -1.5<u<-1 or k<=0:raise ValueError('requires -3/2<u<-1 and k>0')
    D=u*u-.25;Q0=-6*k*D/u
    T0=5832*k**6*D**8/u**6
    return T0/(4*math.pi*bf_z0(b,k)*abs(u))*math.exp(-b*b/4+Q0*Q0/(16*u*u))


def scope_record():
    return {'object':'OA-CONTACT-ANGULAR-TAIL-20260925-v1',
            'contact_kernel_only':True,'finite_r_axis_uniformity_proved':False,
            'periodic_equals_bargmann_fock':False,'independent_acceptance':False,
            'global_elder_bound_proved':False,
            'whole_annulus_limit':'conditional on PR25 fixed-angle asymptotic and PR28 domination'}



def _positive_covariance(cov):
    S=[list(map(exact,row)) for row in cov]
    n=len(S)
    if not 1<=n<=8 or any(len(row)!=n for row in S):
        raise ValueError('a square covariance of order 1..8 is required')
    if any(S[i][j]!=S[j][i] for i in range(n) for j in range(n)):
        raise ValueError('symmetric covariance required')
    residual=[row[:] for row in S]
    while residual:
        p=residual[0][0]
        if p<=0:raise ValueError('strictly positive covariance required')
        residual=[[residual[i][j]-residual[i][0]*residual[0][j]/p
                   for j in range(1,len(residual))] for i in range(1,len(residual))]
    return S


def conditional_variance(cov,index,given):
    """Exact Schur variance; not a replacement for the actual model covariance."""
    S=_positive_covariance(cov);n=len(S);given=list(given)
    if type(index) is not int or not 0<=index<n or any(type(i) is not int or not 0<=i<n for i in given):
        raise ValueError('invalid coordinate index')
    if index in given or len(set(given))!=len(given):
        raise ValueError('conditioning indices must be distinct and exclude target')
    order=given+[index]
    R=[[S[i][j] for j in order]for i in order]
    for _ in given:
        p=R[0][0]
        R=[[R[i][j]-R[i][0]*R[0][j]/p for j in range(1,len(R))]for i in range(1,len(R))]
    return R[0][0]


def left_gaussian_parameters(cov,mean,u,v):
    """Law of V_v=q+v*c/(2u) given a=0, retaining full covariance."""
    S=_positive_covariance(cov);mu=list(map(exact,mean));u,v=map(exact,(u,v))
    if len(S)!=4 or len(mu)!=4 or u==0:
        raise ValueError('four jet coordinates and nonzero u required')
    t=v/(2*u)
    mean_v=mu[1]+t*mu[2]
    cov_av=S[0][1]+t*S[0][2]
    variance_v=S[1][1]+2*t*S[1][2]+t*t*S[2][2]
    variance_v-=cov_av*cov_av/S[0][0]
    return {'variance_a':S[0][0], 'mean_a':mu[0],
            'mean_v_given_a0':mean_v-cov_av*mu[0]/S[0][0],
            'variance_v_given_a0':variance_v}
