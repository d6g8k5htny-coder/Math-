"""Finite controls for contact-kernel tails and the small-gap contact law.

Exact quantities use Fraction and polynomial dictionaries. Gaussian moment and
axis-tail helpers use ordinary floating point and are diagnostics, NOT interval
or quadrature-error certificates. No scientific-status mutation is performed.
"""
from __future__ import annotations
from fractions import Fraction as Q
from math import comb, erf, erfc, exp, factorial, isfinite, pi, sqrt
import json

Poly = dict[tuple[int,int],Q]


def exact(value: int | Q) -> Q:
    if type(value) is int or isinstance(value,Q):
        return Q(value)
    raise TypeError('integer or Fraction required; floats/bools are refused')


def var(index: int) -> Poly:
    if type(index) is not int or index not in (0,1):raise ValueError('index 0 or 1')
    return {(1,0) if index==0 else (0,1):Q(1)}


def const(value: int | Q) -> Poly:
    value=exact(value)
    return {(0,0):value} if value else {}


def add(*polys: Poly) -> Poly:
    out={}
    for p in polys:
        for monomial,c in p.items():out[monomial]=out.get(monomial,Q(0))+c
    return {m:c for m,c in out.items() if c}


def scale(p: Poly, c: int | Q) -> Poly:
    c=exact(c)
    return {m:c*v for m,v in p.items() if c*v}


def mul(p: Poly, q: Poly) -> Poly:
    out={}
    for (i,j),a in p.items():
        for (k,l),b in q.items():
            m=(i+k,j+l);out[m]=out.get(m,Q(0))+a*b
    return {m:c for m,c in out.items() if c}


def powp(p: Poly, n: int) -> Poly:
    if type(n) is not int or not 0<=n<=32:raise ValueError('finite nonnegative integer power required')
    out=const(1)
    for _ in range(n):out=mul(out,p)
    return out


def diff(p: Poly, index: int) -> Poly:
    if type(index) is not int or index not in (0,1):raise ValueError('index 0 or 1')
    out={}
    for monomial,c in p.items():
        n=monomial[index]
        if n:
            key=list(monomial);key[index]-=1;out[tuple(key)]=n*c
    return out


def evaluate(p: Poly, w: int | Q, theta: int | Q) -> Q:
    w,t=exact(w),exact(theta)
    return sum((c*w**i*t**j for (i,j),c in p.items()),Q(0))


def type_polynomial() -> Poly:
    w,t=var(0),var(1)
    dm=add(scale(t,4),scale(powp(add(w,const(1)),2),-1))
    ds=add(powp(add(w,const(-1)),2),const(-4),scale(t,4))
    dx=add(powp(add(w,const(1),scale(t,-2)),2),scale(mul(t,add(const(1),scale(t,-1))),4))
    return mul(mul(dm,ds),dx)


def _integral_w(p: Poly, lo: int, hi: int) -> Q:
    out=Q(0)
    for (i,j),c in p.items():
        if j:raise ValueError('theta must have been eliminated')
        out+=c*Q(hi**(i+1)-lo**(i+1),i+1)
    return out


def integrate_type_pieces(p: Poly) -> tuple[Q,Q]:
    """Integrate over exactly the maximum/saddle type region in (w,theta)."""
    w=var(0)
    lower_left=scale(powp(add(w,const(1)),2),Q(1,4))
    lower_right=add(const(1),scale(powp(add(w,const(-1)),2),-Q(1,4)))
    out=[]
    for lower,lo,hi in ((lower_left,-3,-1),(lower_right,-1,1)):
        integrated={}
        for (i,j),c in p.items():
            term=mul({(i,0):c/Q(j+1)},add(const(1),scale(powp(lower,j+1),-1)))
            integrated=add(integrated,term)
        out.append(_integral_w(integrated,lo,hi))
    return out[0],out[1]


def integrate_type(p: Poly) -> Q:
    a,b=integrate_type_pieces(p)
    return a+b


def normalized_prefactor(k: int | Q) -> Q:
    k=exact(k)
    if k<=0:raise ValueError('positive gap mark required')
    # 24k from the contact Jacobian and height; 6k from dq/dw;
    # (9k^2)^3 from the determinants; 36k^2 from endpoint z0.
    return (24*k)*(6*k)*(9*k*k)**3/(36*k*k)


def contact_jets(u: int | Q,v: int | Q,k: int | Q,w: int | Q,theta: int | Q) -> tuple[Q,Q,Q]:
    u,v,k,w,t=map(exact,(u,v,k,w,theta))
    if not v or k<=0 or not 0<=t<=1:raise ValueError('nonzero v, positive k and height fraction in [0,1] required')
    q=6*k*(w-2*u)/v
    c=12*k*(u*u-u*w+Q(1,4))/v**2
    d=6*k*cubic_d_numerator(u,w,t)/v**3
    return q,c,d


def cubic_d_numerator(u: int | Q,w: int | Q,theta: int | Q) -> Q:
    u,w,t=map(exact,(u,w,theta))
    return -2*u**3-Q(3,2)*u-1+2*t+3*w*(u*u-Q(1,4))


def transverse_hessian(u: int | Q,v: int | Q,k: int | Q,w: int | Q,theta: int | Q) -> Q:
    u,v,k,w,t=map(exact,(u,v,k,w,theta))
    q,_,_=contact_jets(u,v,k,w,t)
    return (12*k*u+6*k+q*v-12*k*t)/(2*v*v)


def contact_determinants(u: int | Q,v: int | Q,k: int | Q,w: int | Q,theta: int | Q) -> tuple[Q,Q,Q]:
    u,v,k,w,t=map(exact,(u,v,k,w,theta))
    if not v:raise ValueError('nonzero transverse coordinate required')
    factor=9*k*k/v**2
    return (factor*(4*t-(w+1)**2),factor*(4*(1-t)-(w-1)**2),
            -factor*((w+1-2*t)**2+4*t*(1-t)))


def _deriv_zero(n: int) -> Q:
    if n%2:return Q(0)
    t=n//2
    return Q((-1)**t*factorial(2*t),2**t*factorial(t))


def bf_cov(alpha: tuple[int,int],beta: tuple[int,int]) -> Q:
    return (-1)**sum(beta)*_deriv_zero(alpha[0]+beta[0])*_deriv_zero(alpha[1]+beta[1])


def axis_tail_integral(c: float, epsilon: float) -> float:
    """Diagnostic value of integral_0^epsilon v^-13 exp(-c/v^2) dv."""
    if not isfinite(c) or not isfinite(epsilon) or c<=0 or epsilon<=0:raise ValueError('finite positive c and epsilon')
    x=c/epsilon**2
    if x>700:return 0.0  # floating underflow; not a rigorous zero bound
    return factorial(5)*exp(-x)*sum(x**j/factorial(j) for j in range(6))/(2*c**6)


def _erf_difference(a:float,b:float)->float:
    if a>=0:return erfc(a)-erfc(b)
    if b<=0:return erfc(-b)-erfc(-a)
    return erf(b)-erf(a)


def gaussian_moments(a:float,lo:float,hi:float,degree:int=6)->list[float]:
    """Diagnostic centered moments integral_lo^hi x^n exp(-a*x^2) dx.

    No outward rounding. Higher moments can lose relative precision when the
    interval is short or the tails are extreme. Do not use as a certificate.
    """
    if not all(isfinite(x) for x in (a,lo,hi)) or a<=0 or hi<lo or type(degree) is not int or not 0<=degree<=16:
        raise ValueError('positive precision, ordered finite interval, degree <=16')
    sa=sqrt(a);el=exp(-a*lo*lo);eh=exp(-a*hi*hi)
    out=[sqrt(pi)/(2*sa)*_erf_difference(sa*lo,sa*hi)]
    if degree:out.append((el-eh)/(2*a))
    for n in range(2,degree+1):
        out.append((lo**(n-1)*el-hi**(n-1)*eh)/(2*a)+(n-1)*out[n-2]/(2*a))
    return out


def gaussian_polynomial_integral(coefficients:list[float],a:float,mu:float,lo:float,hi:float)->float:
    if not coefficients or len(coefficients)>17 or not all(isfinite(x) for x in [a,mu,lo,hi,*coefficients]) or a<0 or hi<lo:
        raise ValueError('finite polynomial, nonnegative precision, ordered interval')
    if a==0:return sum(c*(hi**(i+1)-lo**(i+1))/(i+1) for i,c in enumerate(coefficients))
    centered=[sum(coefficients[i]*comb(i,j)*mu**(i-j) for i in range(j,len(coefficients))) for j in range(len(coefficients))]
    moments=gaussian_moments(a,lo-mu,hi-mu,len(coefficients)-1)
    return sum(c*m for c,m in zip(centered,moments))


def results()->dict:
    j=integrate_type(type_polynomial())
    return {'object':'OA-CONTACT-KERNEL-TAILS-20260925-v1','typed_shape_integral':str(j),
            'small_gap_rational_multiplier':str(normalized_prefactor(1)*j),
            'contact_small_gap_power':6,'transverse_coordinate_power':-13,
            'right_axis_penalty_power':6,'general_axis_penalty_power':2,
            'whole_annulus_asymptotic':'conditional on the exact PR22/PR25 analytic interfaces',
            'finite_r_small_k_uniformity':False,'global_rn_closed':False,
            'independent_analytic_acceptance':False,'diagnostic_quadrature_certified':False}

if __name__=='__main__':print(json.dumps(results(),indent=2,sort_keys=True))
