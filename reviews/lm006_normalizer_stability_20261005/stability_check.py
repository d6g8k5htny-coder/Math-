#!/usr/bin/env python3
"""Exact finite controls for LM006 endpoint-weight stability (stdlib only).

These rational controls do not prove the continuum theorem or execute Lean.
"""
import argparse
from fractions import Fraction as F
import itertools
import json
import random
import sys


def rational(x):
    if type(x) not in (int,F):
        raise TypeError('expected an exact integer or Fraction, not bool/float')
    return F(x)


def vector(v):
    v=tuple(rational(x) for x in v)
    if len(v)!=6: raise ValueError('endpoint vector must have six entries')
    return v


def radius(r):
    r=rational(r)
    if not 0<=r<=1: raise ValueError('radius must lie in [0,1]')
    return r


def norm_sq(v):
    return sum((rational(x)**2 for x in v),F(0))


def pos(x): return max(x,F(0))


def weight(v,r,mutant=None):
    am,ap,bm,bp,cm,cp=vector(v); r=radius(r)
    rr=r*r if mutant=='M1' else r
    if mutant=='M2':
        fm=pos(pos(am)*pos(cm)-rr*bm*bm)
    else:
        fm=pos(pos(-am)*pos(-cm)-rr*bm*bm)
    fs=rr*bp*bp-ap*cp
    if mutant!='M3': fs=pos(fs)
    return fm*fs


def physical_weight(v,r):
    am,ap,bm,bp,cm,cp=vector(v); r=radius(r)
    if r==0: raise ValueError('physical normalized ratio requires r>0')
    dm=(r*am)*cm-(r*bm)**2
    ds=(r*ap)*cp-(r*bp)**2
    return abs(dm*ds)/(r*r) if r*am<0 and dm>0 and ds<0 else F(0)


def normal_norm_even(d,k,mutant=None):
    if type(d) is not int or type(k) is not int or d<=0 or k<0:
        raise ValueError('positive integer dimension and nonnegative integer order required')
    if mutant=='M4' and k==3: return 15
    ans=1
    for j in range(k): ans*=d+2*j
    return ans


def affine_gap_sq(m,A,n,B,mutant=None):
    m,n=vector(m),vector(n)
    A=tuple(tuple(rational(x) for x in row) for row in A)
    B=tuple(tuple(rational(x) for x in row) for row in B)
    if len(A)!=6 or len(B)!=6 or not A[0]: raise ValueError('six nonempty factor rows required')
    width=len(A[0])
    if any(len(row)!=width for row in A+B): raise ValueError('factor shapes differ')
    shift=F(0) if mutant=='M5' else norm_sq(tuple(x-y for x,y in zip(m,n)))
    return shift+sum(((x-y)**2 for row,col in zip(A,B) for x,y in zip(row,col)),F(0))


def check(condition,label):
    if not condition: raise ValueError(label)


def controls(mutant=None):
    counts={'physical_identity':0,'limit':0,'parameter':0,'vector_squared_envelope':0,'gaussian_moments':0,'mean_shift':0}
    for values in itertools.product((-1,0,1),repeat=6):
        v=tuple(map(F,values))
        for r in (F(1,4),F(1,2),F(1)):
            check(weight(v,r,mutant)==physical_weight(v,r),'PHYSICAL_TYPED_IDENTITY')
            counts['physical_identity']+=1
    for a,q in itertools.product((-3,0,4),(-2,-1,0,1,2)):
        v=(F(-1),F(1),-F(a)/2,F(a)/2,F(q),F(q))
        check(weight(v,0,mutant)==pos(-F(q))**2,'LIMIT_NEGATIVE_PART')
        counts['limit']+=1
    rng=random.Random(20261005)
    for _ in range(200):
        v=tuple(F(rng.randrange(-8,9),4) for _ in range(6))
        w=tuple(F(rng.randrange(-8,9),4) for _ in range(6))
        r,s=F(rng.randrange(9),8),F(rng.randrange(9),8)
        check(abs(weight(v,r,mutant)-weight(v,s,mutant))<=abs(r-s)*norm_sq(v)**2,'PARAMETER_ENVELOPE')
        counts['parameter']+=1
        excess=pos(abs(weight(v,r,mutant)-weight(w,s,mutant))-abs(r-s)*norm_sq(w)**2)
        check(excess**2<=8*(norm_sq(v)+norm_sq(w))**3*norm_sq(tuple(x-y for x,y in zip(v,w))),'VECTOR_ENVELOPE')
        counts['vector_squared_envelope']+=1
    for d,k,want in ((6,2,48),(6,3,480),(6,4,5760)):
        check(normal_norm_even(d,k,mutant)==want,'GAUSSIAN_NORM_MOMENT')
        counts['gaussian_moments']+=1
    a=tuple(map(F,(-1,1,0,0,-1,-1))); b=tuple(map(F,(-1,1,0,0,-2,-2)))
    zero=((F(0),),)*6
    check(affine_gap_sq(a,zero,b,zero,mutant)==2,'MEAN_SHIFT_NOT_COVARIANCE_ONLY')
    counts['mean_shift']+=1
    return {'scientific_effect':'NONE','exact_controls':counts,'total':sum(counts.values()),'meaning':'finite algebra diagnostics, not a continuum or Lean proof'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mutant',choices=['M1','M2','M3','M4','M5'])
    a=p.parse_args()
    try: result=controls(a.mutant)
    except (ValueError,TypeError) as e:
        print('STABILITY_FAIL: '+str(e),file=sys.stderr); return 1
    print(json.dumps(result,sort_keys=True)); return 0

if __name__=='__main__': sys.exit(main())
