#!/usr/bin/env python3
"""Outward rational enclosure of the coefficient in Math-#358.

All certified arithmetic is integer/Fraction. No floating arithmetic, quadrature
library, simulation, or Lean proof. Source theorem and scope remain prerequisites.
"""
import argparse
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt
import json

SCALE=10**36

def ceil_ratio(n,d):
    return -((-n)//d)

def fixed(x):
    x=F(x)
    return x.numerator*SCALE//x.denominator,ceil_ratio(x.numerator*SCALE,x.denominator)

def sqrt_bounds(x):
    x=F(x)
    if x<0:raise ValueError('nonnegative radicand required')
    a=isqrt(x.numerator*SCALE*SCALE//x.denominator)
    b=a if F(a*a,SCALE*SCALE)==x else a+1
    return F(a,SCALE),F(b,SCALE)

@lru_cache(maxsize=1)
def pi_bounds():
    def atan(z):
        # 81 terms ends positive, hence upper; preceding partial sum is lower.
        z=F(z);s=F(0)
        for k in range(81):
            term=(-1)**k*z**(2*k+1)/(2*k+1)
            s+=term
        return s-term,s
    a,b=atan(F(1,5));c,d=atan(F(1,239))
    return 16*a-4*d,16*b-4*c

def exp_neg(x):
    x=F(x)
    if x<0:raise ValueError('nonnegative argument required')
    if x==0:return F(1),F(1)
    shifts=0
    while x>F(1,8):x/=2;shifts+=1
    # Alternating series: even degree 22 upper; odd degree 23 lower.
    term=s=F(1)
    for k in range(1,24):
        term*=-x/k;s+=term
    lo=fixed(s)[0];hi=fixed(s-term)[1]
    for _ in range(shifts):
        lo=lo*lo//SCALE;hi=ceil_ratio(hi*hi,SCALE)
    return F(max(lo,0),SCALE),F(min(hi,SCALE),SCALE)

@lru_cache(maxsize=1)
def inv_sqrt_2pi():
    lo,hi=pi_bounds();a=sqrt_bounds(2*lo)[0];b=sqrt_bounds(2*hi)[1]
    return 1/b,1/a

def cdf_positive(z):
    z=F(z)
    if not 0<=z<=1:raise ValueError('CDF series interface requires 0<=z<=1')
    if z==0:return F(1,2),F(1,2)
    term=s=z
    # Integrate exp(-t²/2), alternating with decreasing terms on [0,1].
    for k in range(1,34):
        term*=-z*z*F(2*k-1,2*k*(2*k+1));s+=term
    c,d=inv_sqrt_2pi()
    return F(1,2)+c*s,F(1,2)+d*(s-term)

@lru_cache(maxsize=1)
def image_bounds():
    # Positive Taylor lower sum certifies e^288 > 10^125, no decimal log input.
    term=total=F(1)
    for k in range(1,401):term*=F(288,k);total+=term
    if total<=10**125:raise ArithmeticError('exponential image bound failed')
    q=F(1,10**125)
    s2=q*(1+q)/(1-q)**3
    s4=q*(1+11*q+11*q*q+q**3)/(1-q)**5
    # H>=1; drop the negative contribution -6 A2 for upper m4 error.
    return {'exp288_lower_gt_10pow125':True,
            'm2_error':2*24**2*s2,'m4_error':2*24**4*s4}

@lru_cache(maxsize=1)
def parameters():
    images=image_bounds();eps=F(1,10**24)
    if max(images['m2_error'],images['m4_error'])>=eps:
        raise ArithmeticError('periodic input enclosure not established')
    m2=(1-eps,F(1));m4=(F(3),3+eps)
    delta=(m4[0]-m2[1]**2,m4[1]-m2[0]**2)
    v=(m2[0]*delta[0],m2[1]*delta[1])
    # a=m2*b>0, z0=(a²+delta)Phi(a/sqrt(delta))+a sqrt(delta)phi(a/sqrt(delta)).
    a=(m2[0]*F(6,5),m2[1]*F(6,5))
    sigma=(sqrt_bounds(delta[0])[0],sqrt_bounds(delta[1])[1])
    z=(a[0]/sigma[1],a[1]/sigma[0])
    Phi=(cdf_positive(z[0])[0],cdf_positive(z[1])[1])
    inv=inv_sqrt_2pi()
    ex=(exp_neg(z[1]**2/2)[0],exp_neg(z[0]**2/2)[1])
    phi=(inv[0]*ex[0],inv[1]*ex[1])
    z0=((a[0]**2+delta[0])*Phi[0]+a[0]*sigma[0]*phi[0],
        (a[1]**2+delta[1])*Phi[1]+a[1]*sigma[1]*phi[1])
    p0=(phi[0]/sigma[1],phi[1]/sigma[0])
    return {'m2':m2,'m4':m4,'delta':delta,'variance_D':v,'z0':z0,'p0':p0}

def density(x,var):
    x=F(x);lo,hi=map(F,var)
    if x<0 or not 0<lo<=hi:raise ValueError('nonnegative coordinate, positive variance interval required')
    c,d=inv_sqrt_2pi()
    lower=c/sqrt_bounds(hi)[1]*exp_neg(x*x/(2*lo))[0]
    upper=d/sqrt_bounds(lo)[0]*exp_neg(x*x/(2*hi))[1]
    return F(fixed(lower)[0],SCALE),F(fixed(upper)[1],SCALE)

def j(d,u):
    d,u=F(d),F(u)
    if u<0:raise ValueError('nonnegative squared mixed coordinate required')
    if u==0 or d<=u:return F(0)
    ell=min(u,d-u);big=max(u,d-u)
    return ell*ell*(3*big-ell)/6

def cell_bounds(d0,d1,u0,u1):
    d0,d1,u0,u1=map(F,(d0,d1,u0,u1))
    if not 0<=d0<=d1 or not 0<=u0<=u1:raise ValueError('ordered positive rectangle required')
    return min(j(d0,u0),j(d0,u1)),j(d1,min(max(d1/2,u0),u1))

def _jnum(d,u):
    if u<=0 or d<=u:return 0
    ell=min(u,d-u);big=max(u,d-u)
    return ell*ell*(3*big-ell)

def enclosure(n=512):
    if type(n) is not int:raise TypeError('integer grid required')
    if not 2<=n<=2048:raise ValueError('grid must lie in [2,2048]')
    p=parameters();v=p['variance_D'];R=12;T=4
    d_pdf=[density(F(R*i,n),v) for i in range(n+1)]
    b_pdf=[density(F(T*i,n),(v[0]/4,v[1]/4)) for i in range(n+1)]
    dl=[fixed(t[0])[0] for t in d_pdf];du=[fixed(t[1])[1] for t in d_pdf]
    bl=[fixed(t[0])[0] for t in b_pdf];bu=[fixed(t[1])[1] for t in b_pdf]
    # Common coordinate denominator q=2n² includes the d/2 stationary point.
    q=2*n*n;lower=upper=0
    for i in range(n):
        d0=2*R*i*n;d1=d0+2*R*n
        for k in range(n):
            u0=2*T*T*k*k;u1=2*T*T*(k+1)*(k+1)
            jlo=min(_jnum(d0,u0),_jnum(d0,u1))
            jhi=_jnum(d1,min(max(d1//2,u0),u1))
            lower+=jlo*dl[i+1]*bl[k+1]
            upper+=jhi*du[i]*bu[k]
    factor=F(2*R*T, n*n*6*q**3*SCALE*SCALE)
    low=lower*factor;high=upper*factor
    # Union bound for omitted D>R and |B|>T; J<=D_+³/24.
    tail_d=(v[1]*R*R+2*v[1]**2)*d_pdf[-1][1]/24
    mean_d3=2*v[1]**2*d_pdf[0][1]
    tail_b=mean_d3/24*(v[1]/(2*T))*b_pdf[-1][1]
    tail=tail_d+tail_b
    gamma=(low,high+tail)
    coeff=(gamma[0]*p['p0'][0]/p['z0'][1],gamma[1]*p['p0'][1]/p['z0'][0])
    return {'grid':n,'gamma':gamma,'coefficient':coeff,'tail':tail,'parameters':p}

def decimal_bound(x,places=12,upper=False):
    scale=10**places;x=F(x)
    n=ceil_ratio(x.numerator*scale,x.denominator) if upper else x.numerator*scale//x.denominator
    return str(n//scale)+'.'+str(n%scale).zfill(places)

def output(n):
    r=enclosure(n)
    pairs=lambda a:[decimal_bound(a[0]),decimal_bound(a[1],upper=True)]
    return {'scientific_effect':'NONE','independently_reviewed':False,
            'meaning':'author-side outward rational enclosure conditional on the #358 coefficient formula',
            'source_commit':'64c0a203b94105f0fccbe6f8116a94e13431f84e',
            'grid':n,'coefficient':pairs(r['coefficient']),'gamma':pairs(r['gamma']),
            'tail_gamma_upper':decimal_bound(r['tail'],places=18,upper=True),
            'z0':pairs(r['parameters']['z0']),'p0':pairs(r['parameters']['p0']),
            'arithmetic':'integer/Fraction; outward fixed-point scale 10^36',
            'scope':'d2, L24, b6/5, original axes, six pins and gap r^3/6; no finite-r error bound'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--grid',type=int,default=512)
    args=parser.parse_args()
    try:result=output(args.grid)
    except (ValueError,TypeError,ArithmeticError) as exc:
        print('ENCLOSURE_FAIL: '+str(exc),file=__import__('sys').stderr);return 1
    print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
