#!/usr/bin/env python3
"""Exact finite-Hilbert Gaussian regression controls; standard library only.

Rows are coefficients against an independent standard Gaussian vector. Their
inner products therefore are exact covariances. No random sampling or Lean.
"""
from fractions import Fraction as F
import argparse, json, math, sys


def exact(x):
    if type(x) not in (int,F): raise TypeError('exact int/Fraction required')
    return F(x)


def matrix(a):
    a=[list(map(exact,row)) for row in a]
    if not a or not a[0] or any(len(row)!=len(a[0]) for row in a):
        raise ValueError('nonempty rectangular matrix required')
    return a


def transpose(a): return [list(x) for x in zip(*matrix(a))]


def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]


def mul(a,b):
    a,b=matrix(a),matrix(b)
    if len(a[0])!=len(b): raise ValueError('matrix product shape mismatch')
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]


def sub(a,b):
    a,b=matrix(a),matrix(b)
    if len(a)!=len(b) or len(a[0])!=len(b[0]): raise ValueError('difference shape mismatch')
    return [[x-y for x,y in zip(row,col)] for row,col in zip(a,b)]


def frob2(a): return sum((x*x for row in matrix(a) for x in row),F(0))


def inverse(a):
    a=matrix(a); n=len(a)
    if len(a[0])!=n: raise ValueError('square matrix required')
    aug=[row+ident for row,ident in zip(a,eye(n))]
    for j in range(n):
        pivot=next((i for i in range(j,n) if aug[i][j]),None)
        if pivot is None: raise ValueError('singular matrix')
        aug[j],aug[pivot]=aug[pivot],aug[j]
        scale=aug[j][j]; aug[j]=[x/scale for x in aug[j]]
        for i in range(n):
            if i!=j:
                scale=aug[i][j]; aug[i]=[x-scale*y for x,y in zip(aug[i],aug[j])]
    return [row[n:] for row in aug]


def condition(p,v,d,mutant=None):
    p,v=matrix(p),matrix(v); d=list(map(exact,d))
    if len(p[0])!=len(v[0]) or len(p)!=len(d): raise ValueError('conditioning shape mismatch')
    B=mul(mul(v,transpose(p)),inverse(mul(p,transpose(p))))
    mean=[row[0] for row in mul(B,[[x] for x in d])]
    residual=sub(v,mul(B,p))
    if mutant=='M1': mean=[F(0)]*len(mean)
    if mutant=='M2': residual=v
    return mean,residual


def coupling_error_sq(left,right):
    m,a=left; n,b=right
    if len(m)!=len(n): raise ValueError('mean shape mismatch')
    return sum(((exact(x)-exact(y))**2 for x,y in zip(m,n)),F(0))+frob2(sub(a,b))


def frame(raw,r):
    raw=tuple(map(exact,raw)); r=exact(r)
    if len(raw)!=6 or r<=0: raise ValueError('six raw pins and positive radius required')
    fm,fxm,fym,fp,fxp,fyp=raw
    p0=(fm+fp)/2; p1=(fxm+fxp)/2
    return (p0,p1,(fym+fyp)/2,(fxp-fxm)/r,(fyp-fym)/r,12*(p1-(fp-fm)/r)/r**2)


def inverse_frame(p,r):
    p=tuple(map(exact,p)); r=exact(r)
    if len(p)!=6 or r<=0: raise ValueError('six frame pins and positive radius required')
    a,b,c,d,e,g=p
    return (a-r*b/2+r**3*g/24,b-r*d/2,c-r*e/2,a+r*b/2-r**3*g/24,b+r*d/2,c+r*e/2)


def kernel_constants():
    # Integrals of |u| times kernels over [-1/2,1/2], by exact antiderivatives.
    h=F(1,2)
    return (12*(h*h/8-h**4/4), h*h/2, h*h)


def model(r,mutant=None):
    r=exact(r)
    if not 0<=r<=1: raise ValueError('radius must lie in [0,1]')
    # f=Z0+Z1*x+Z2*y+Z3*x²/2+Z4*x*y+Z5*x³/6+Z6*x²*y/2
    #   +Z7*y²/2+Z8*x⁴/24+Z9*x³*y/6+Z10*x*y²/2.
    f={0:(0,F(1)),1:(1,F(1)),2:(3,F(1,2)),3:(5,F(1,6)),4:(8,F(1,24))}
    hy={0:(2,F(1)),1:(4,F(1)),2:(6,F(1,2)),3:(9,F(1,6))}
    q={0:(7,F(1)),1:(10,F(1))}
    def derivative(poly,x,order):
        row=[F(0)]*11
        for degree,(index,c) in poly.items():
            if degree>=order: row[index]=c*F(math.factorial(degree),math.factorial(degree-order))*x**(degree-order)
        return row
    zero=F(0); h=r/2
    if not r:
        p=[derivative(f,zero,0),derivative(f,zero,1),derivative(hy,zero,0),derivative(f,zero,2),derivative(hy,zero,1),derivative(f,zero,3)]
        f3=derivative(f,zero,3); h2=derivative(hy,zero,2)
        v=[[-x/2 for x in f3],[x/2 for x in f3],[-x/2 for x in h2],[x/2 for x in h2],derivative(q,zero,0),derivative(q,zero,0)]
    else:
        raw=[derivative(f,-h,0),derivative(f,-h,1),derivative(hy,-h,0),derivative(f,h,0),derivative(f,h,1),derivative(hy,h,0)]
        p=transpose([frame(col,r) for col in zip(*raw)])
        v=[[(x-y)/r for x,y in zip(derivative(f,-h,2),p[3])],[(x-y)/r for x,y in zip(derivative(f,h,2),p[3])],[(x-y)/r for x,y in zip(derivative(hy,-h,1),p[4])],[(x-y)/r for x,y in zip(derivative(hy,h,1),p[4])],derivative(q,-h,0),derivative(q,h,0)]
    d=[F(6,5)-r**3/12,F(0),F(0),F(0),F(0),F(1) if mutant=='M3' else F(2)]
    return p,v,d


def rough_model(n):
    """C3-not-C4 example: replace Z8*x^4/24 by Z8*|x|^(7/2)."""
    if type(n) is not int or n<2: raise ValueError('integer n>=2 required')
    p,v,d=model(F(2,n*n))
    p[0][8]=F(1,n**7); p[1][8]=F(0); p[3][8]=F(7,2*n**3); p[5][8]=F(0)
    v[0][8]=v[1][8]=F(21,8*n)
    return p,v,d


def require(ok,reason):
    if not ok: raise ValueError(reason)


def controls(mutant=None):
    count=0
    m,res=condition(eye(2),eye(2),[F(1),F(2)],mutant)
    require(m==[F(1),F(2)],'CONDITIONAL_MEAN'); count+=1
    require(res==[[F(0)]*2 for _ in range(2)],'RESIDUAL_ORTHOGONALITY'); count+=1
    mean,_=condition(*model(F(0),mutant))
    require(mean[:2]==[F(-1),F(1)],'CUBIC_PIN_TARGET'); count+=1
    k=F(3,32) if mutant=='M4' else kernel_constants()[0]
    require(k==F(3,16),'KERNEL_LIPSCHITZ_MASS'); count+=1
    for n in (2,4,8,16,32):
        r=F(1,n)
        require(r<= (r*r if mutant=='M5' else r),'NO_SQRT_LIPSCHITZ'); count+=1
        ratio=F(21*n,16)
        require(ratio<=(F(25) if mutant=='M6' else F(21*n,16)),'EXTRA_REGULARITY_REQUIRED'); count+=1
    for r in (F(1),F(1,2),F(1,8)):
        for j in range(12):
            raw=tuple(F((j+3*i)%11-5,3) for i in range(6))
            require(inverse_frame(frame(raw,r),r)==raw,'FRAME_INVERSE'); count+=1
    p0,v0,d0=model(F(0)); y=condition(p0,v0,d0)
    for j in range(1,15):
        r=F(1,2**j); p,v,d=model(r); x=condition(p,v,d)
        require(mul(x[1],transpose(p))==[[F(0)]*6 for _ in range(6)],'RESIDUAL_ORTHOGONALITY'); count+=1
        require(frob2(sub(p,p0))<=4*r*r and frob2(sub(v,v0))<=4*r*r,'ROW_RATES'); count+=1
        if r<=F(1,40):
            e2=coupling_error_sq(x,y)
            require(F(1,2)*r*r<=e2<=(F(10042,3)**2+2590**2)*r*r,'QUANTIFIED_RATE'); count+=1
    return {'controls':count,'scientific_effect':'NONE','meaning':'finite exact regression and countermodels; not Lean or an infinite-field realization'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant',choices=['M'+str(i) for i in range(1,7)])
    args=parser.parse_args()
    try: result=controls(args.mutant)
    except (ValueError,TypeError) as exc:
        print('REGRESSION_FAIL: '+str(exc),file=sys.stderr); return 1
    print(json.dumps(result,sort_keys=True)); return 0
if __name__=='__main__': sys.exit(main())
