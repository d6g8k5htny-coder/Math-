#!/usr/bin/env python3
"""One-dimensional outward enclosure of the pinned LM006 leading coefficient.

Integer/Fraction arithmetic only. Conditional on the exact #358 coefficient;
not a finite-radius probability or a Lean proof. Parent arithmetic is hash-bound.
"""
import argparse
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import types

PARENT_SHA='157e02ee22699b4fa2efdde1894824b92b962900dbb8da9bd65acee41ae91e88'
SCALE=10**36
SERIES_SCALE=10**100
SERIES_LAST=331  # Odd partial sum lower; preceding even partial sum upper.


def exact(x):
    if type(x) not in (int,F):
        raise TypeError('exact int or Fraction required')
    return F(x)


def ceildiv(a,b):
    return -((-a)//b)


def iv(lo,hi=None):
    lo=exact(lo); hi=lo if hi is None else exact(hi)
    if lo>hi: raise ValueError('interval endpoints reversed')
    return (F(lo.numerator*SCALE//lo.denominator,SCALE),
            F(ceildiv(hi.numerator*SCALE,hi.denominator),SCALE))


def as_iv(x):
    if isinstance(x,tuple) and len(x)==2: return iv(*x)
    return iv(x)


def add(x,y):
    x,y=as_iv(x),as_iv(y); return iv(x[0]+y[0],x[1]+y[1])


def sub(x,y):
    x,y=as_iv(x),as_iv(y); return iv(x[0]-y[1],x[1]-y[0])


def mul(x,y):
    x,y=as_iv(x),as_iv(y); z=[a*b for a in x for b in y]
    return iv(min(z),max(z))


def div(x,y):
    x,y=as_iv(x),as_iv(y)
    if y[0]<=0<=y[1]: raise ValueError('interval denominator contains zero')
    z=[a/b for a in x for b in y]
    return iv(min(z),max(z))


def authenticate(raw):
    if len(raw)!=7215 or hashlib.sha256(raw).hexdigest()!=PARENT_SHA:
        raise ValueError('parent source identity mismatch')
    return raw


def parent_bytes():
    path=Path(__file__).resolve().parent.parent/'lm006_wrong_sign_20261006_r20'/'enclose.py'
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb') as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError('parent must be a regular file')
        raw=stream.read(7217)
    return authenticate(raw)


@lru_cache(maxsize=1)
def parent():
    raw=parent_bytes(); module=types.ModuleType('verified_lm006_parent')
    exec(compile(raw,'<sha256:'+PARENT_SHA+'>','exec'),module.__dict__)
    return module


def sqrt_iv(x):
    x=as_iv(x)
    if x[0]<0: raise ValueError('nonnegative square-root interval required')
    return iv(parent().sqrt_bounds(x[0])[0],parent().sqrt_bounds(x[1])[1])


def phi(x):
    x=as_iv(x)
    if x[0]<0: raise ValueError('nonnegative normal coordinate required')
    p=parent(); c=iv(*p.inv_sqrt_2pi())
    return mul(c,iv(p.exp_neg(x[1]**2/2)[0],p.exp_neg(x[0]**2/2)[1]))


@lru_cache(maxsize=8192)
def normal_tail_point(x):
    """Enclose P(Z>x), 0<=x<=13, using signed integral-Taylor remainders."""
    x=exact(x)
    if not 0<=x<=13: raise ValueError('normal tail interface requires [0,13]')
    if x==0: return iv(F(1,2))
    S=SERIES_SCALE
    lo=x.numerator*S//x.denominator; hi=ceildiv(x.numerator*S,x.denominator)
    low,high=lo,hi
    x2=x*x
    even_high=None
    for k in range(1,SERIES_LAST+1):
        ratio=x2*F(2*k-1,2*k*(2*k+1))
        lo=lo*ratio.numerator//ratio.denominator
        hi=ceildiv(hi*ratio.numerator,ratio.denominator)
        if k%2: low-=hi; high-=lo
        else: low+=lo; high+=hi
        if k==SERIES_LAST-1: even_high=high
    if even_high is None or SERIES_LAST%2!=1:
        raise ArithmeticError('odd/even Taylor contract violated')
    # Odd-degree exp Taylor integrates below; even-degree integrates above.
    integral=(max(F(0),F(low,S)),F(even_high,S))
    if integral[1]<integral[0]: raise ArithmeticError('integral enclosure reversed')
    c,d=parent().inv_sqrt_2pi()
    lower=F(1,2)-d*integral[1]
    upper=F(1,2)-c*integral[0]
    if upper<0 or lower>F(1,2): raise ArithmeticError('tail enclosure outside probability range')
    return iv(max(F(0),lower),min(F(1,2),upper))


def normal_tail(x):
    x=as_iv(x)
    return iv(normal_tail_point(x[1])[0],normal_tail_point(x[0])[1])


def conditional_integral(u,v):
    """g_v(u)=E_D J(D,u); implementation domain u in [0,9], v in [199/100,3]."""
    u=exact(u); v=as_iv(v)
    if not 0<=u<=9 or not F(199,100)<=v[0]<=v[1]<=3:
        raise ValueError('u in [0,9] and variance in [199/100,3] required')
    if u==0: return iv(0)
    s=sqrt_iv(v); a=div(u,s); a2=mul(a,a); a3=mul(a2,a)
    first=mul(add(mul(4,a2),2),sub(phi(mul(2,a)),phi(a)))
    second=mul(add(mul(6,a),mul(4,a3)),normal_tail(a))
    third=mul(add(mul(6,a),mul(8,a3)),normal_tail(mul(2,a)))
    out=div(mul(mul(v,s),sub(add(first,second),third)),6)
    if out[1]<0: raise ArithmeticError('nonnegative conditional integral excluded')
    return iv(max(F(0),out[0]),min(F(1,5),out[1]))


def integrand(b,v):
    b=exact(b); v=as_iv(v)
    if not 0<=b<=3: raise ValueError('compact integral coordinate requires [0,3]')
    pdf=iv(*parent().density(b,(v[0]/4,v[1]/4)))
    return mul(2,mul(pdf,conditional_integral(b*b,v)))


def simpson(function,end,n):
    end=exact(end)
    if type(n) is not int or n<2 or n%2 or end<=0:
        raise ValueError('positive endpoint and positive even panel count required')
    total=add(function(F(0)),function(end))
    for k in range(1,n):
        total=add(total,mul(4 if k%2 else 2,function(end*k/n)))
    return mul(end/F(3*n),total)


def derivative_bound():
    # Proof gives <1002 uniformly on b>=0, variance [3/2,3]; use 1100.
    return F(1100)


def simpson_error(n):
    if type(n) is not int or n<2 or n%2:
        raise ValueError('positive even panel count required')
    return derivative_bound()*3*F(3,n)**4/180


def omitted_tail(v):
    p=parent();lo,hi=map(exact,v)
    if not 0<lo<=hi: raise ValueError('positive variance interval required')
    # |B|>3 and J>0 implies D>B²>9. Independence gives a product bound.
    d_tail=(81*hi+2*hi*hi)*p.density(9,(lo,hi))[1]/24
    b_tail=hi*p.density(3,(lo/4,hi/4))[1]/6
    return d_tail*b_tail


def enclosure(n=1024):
    if type(n) is not int: raise TypeError('integer panel count required')
    if not 2<=n<=2048 or n%2: raise ValueError('even panels in [2,2048] required')
    p=parent().parameters(); v=iv(*p['variance_D'])
    raw=simpson(lambda b:integrand(b,v),F(3),n)
    err=simpson_error(n);tail=omitted_tail(p['variance_D'])
    gamma=(max(F(0),raw[0]-err),raw[1]+err+tail)
    coefficient=(gamma[0]*p['p0'][0]/p['z0'][1],gamma[1]*p['p0'][1]/p['z0'][0])
    return {'panels':n,'evaluations':n+1,'gamma':gamma,'coefficient':coefficient,
            'quadrature_error':err,'tail':tail,'simpson_sum':raw,'parameters':p}


def output(n):
    value=enclosure(n); p=parent()
    pair=lambda z:[p.decimal_bound(z[0],15),p.decimal_bound(z[1],15,True)]
    return {'scientific_effect':'NONE','independently_reviewed':False,
            'panels':n,'evaluations':n+1,'coefficient':pair(value['coefficient']),
            'gamma':pair(value['gamma']),
            'quadrature_error_gamma_upper':p.decimal_bound(value['quadrature_error'],20,True),
            'omitted_tail_gamma_upper':p.decimal_bound(value['tail'],20,True),
            'source_commit':'64c0a203b94105f0fccbe6f8116a94e13431f84e',
            'method':'analytic D integration; composite Simpson with proved |f4|<=1100; rational outward arithmetic',
            'scope':'leading coefficient only; d2 L24 b6/5 original axes and pins; no finite-r remainder or radius'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--panels',type=int,default=1024)
    args=parser.parse_args()
    try: result=output(args.panels)
    except (ValueError,TypeError,ArithmeticError,OSError) as exc:
        print('ONED_FAIL: '+str(exc),file=sys.stderr);return 1
    print(json.dumps(result,sort_keys=True));return 0

if __name__=='__main__':sys.exit(main())
