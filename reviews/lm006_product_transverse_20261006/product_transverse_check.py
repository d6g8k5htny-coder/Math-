#!/usr/bin/env python3
"""Exact finite product-spectrum checks, not a periodic-field certificate or Lean."""
import argparse
from fractions import Fraction as F
from functools import lru_cache
import json
import sys


def cmul(a,b):
    return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])


def cpow(a,n):
    if n<0: return cpow((a[0],-a[1]),-n)
    out=(F(1),F(0))
    while n:
        if n&1: out=cmul(out,a)
        a=cmul(a,a); n//=2
    return out


def spectrum(correlated=False,yvalues=(-2,-1,0,1,2)):
    p={(x,y):F(1)+F(x*x*y*y,100)*correlated for x in range(-5,6) for y in yvalues}
    total=sum(p.values()); return {k:w/total for k,w in p.items()}


def moments(p):
    m2=sum(w*y*y for (x,y),w in p.items())
    m4=sum(w*y**4 for (x,y),w in p.items())
    return m2,m4,m4-m2*m2


@lru_cache(maxsize=4096)
def primitive(items,z,a,b):
    sa,xa,ya=a; sb,xb,yb=b
    if z[0]*z[0]+z[1]*z[1]!=1: raise ValueError('unit-circle rational phase required')
    ip=cpow((F(0),F(1)),xa+ya-xb-yb)
    re=im=F(0)
    for (x,y),w in items:
        u=cmul(ip,cpow(z,(sa-sb)*x)); scale=w*x**(xa+xb)*y**(ya+yb)
        re+=scale*u[0]; im+=scale*u[1]
    if im: raise ValueError('covariance is not real')
    return re


def cov(p,z,a,b):
    items=tuple(sorted(p.items())); z=tuple(map(F,z))
    return sum(c*d*primitive(items,z,(s,x,y),(t,u,v))
               for c,s,x,y in a for d,t,u,v in b)


def row(site,dx=0,dy=0): return [(F(1),site,dx,dy)]


def rho(p,z): return cov(p,z,row(1),row(0))


def residual_cross(p,z,derivative,wrong_sign=False):
    m2,_,_=moments(p)
    r=row(1,0,2)+[(m2*(-1 if wrong_sign else 1),1,0,0)]
    return cov(p,z,r,row(0,*derivative))


def residual_covariance(p,z):
    m2,_,_=moments(p)
    return cov(p,z,row(1,0,2)+[(m2,1,0,0)],row(0,0,2)+[(m2,0,0,0)])


def observations():
    obs=[row(s,j,0) for s in (0,1) for j in range(3)]
    obs += [row(s,j,1) for s in (0,1) for j in range(2)]
    obs += [[(F(1),1,0,2),(F(-1),0,0,2)]]
    return obs,row(1,0,2)


def solve(a,b):
    n=len(a)
    if not n or len(b)!=n or any(len(v)!=n for v in a): raise ValueError('square system required')
    a=[list(map(F,v))+[F(w)] for v,w in zip(a,b)]
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]),None)
        if k is None: raise ValueError('singular observations')
        a[j],a[k]=a[k],a[j]; t=a[j][j]; a[j]=[v/t for v in a[j]]
        for k in range(n):
            if k!=j:
                t=a[k][j]; a[k]=[v-t*w for v,w in zip(a[k],a[j])]
    return [v[-1] for v in a]


def regress(p,z,observed,target):
    gram=[[cov(p,z,a,b) for b in observed] for a in observed]
    cross=[cov(p,z,a,target) for a in observed]
    coefficients=solve(gram,cross)
    return cov(p,z,target,target)-sum(a*b for a,b in zip(coefficients,cross)),coefficients


def require(ok,label):
    if not ok: raise ValueError(label)


def controls(mutant=None):
    p=spectrum(); m2,_,g=moments(p); z=(F(3,5),F(4,5)); obs,q=observations()
    v,co=regress(p,z,obs,q); correlation=rho(p,z)
    require(residual_cross(p,z,(0,0),mutant=='M1')==0,'RESIDUAL_SIGN')
    require(v==g*(1+correlation)/(1 if mutant=='M2' else 2),'VARIANCE_FACTOR')
    values=list(map(F,(6,0,1,5,0,-1,0,2,0,-3,1)))
    mean=sum(a*b for a,b in zip(co,values))
    require(mean==F(1,2)-(0 if mutant=='M3' else m2*F(11,2)),'MEAN_SHIFT')
    pins=[obs[j] for j in (0,1,6,3,4,8)]
    variance,_=regress(p,z,pins,obs[-1])
    require(variance==(1 if mutant=='M4' else 2)*g*(1-correlation),'DIFFERENCE_VARIANCE')
    wrong=residual_cross(spectrum(correlated=True),(F(1),F(0)),(2,0))
    require(wrong==0 if mutant=='M5' else wrong!=0,'PRODUCT_REQUIRED')
    low=g*(1+rho(p,(F(-1),F(0))))/2
    require(low>=g/2 if mutant=='M6' else low<g/2,'DENSITY_SIGN_PREMISE')
    count=6
    for phase in (z,(F(5,13),F(12,13)),(F(-1),F(0))):
        for derivative in ((0,0),(1,0),(2,0),(0,1),(1,1)):
            require(residual_cross(p,phase,derivative)==0,'ORTHOGONALITY'); count+=1
        require(residual_covariance(p,phase)==g*rho(p,phase),'RESIDUAL_COVARIANCE'); count+=1
        vr,cr=regress(p,phase,obs,q)
        require(vr==g*(1+rho(p,phase))/2,'FULL_SCHUR'); count+=1
        require(sum(a*b for a,b in zip(cr,values))==F(1,2)-m2*F(11,2),'FULL_MEAN'); count+=1
    return {'controls':count,'arithmetic':'Fraction','scope':'finite spectral Gaussian models; no continuum or Lean execution','scientific_effect':'NONE'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mutant',choices=['M'+str(i) for i in range(1,7)])
    args=ap.parse_args()
    try: result=controls(args.mutant)
    except ValueError as exc:
        print('PRODUCT_FAIL: '+str(exc),file=sys.stderr); return 1
    print(json.dumps(result,sort_keys=True)); return 0

if __name__=='__main__': sys.exit(main())
