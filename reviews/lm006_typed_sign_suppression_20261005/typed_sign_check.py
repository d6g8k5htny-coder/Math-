#!/usr/bin/env python3
"""Rational controls for a typed saddle-sign estimate; no Lean execution."""
from fractions import Fraction as F
from math import comb
import argparse,itertools,json,sys

def exact(x):
    if type(x) not in (int,F):raise TypeError("exact int/Fraction required")
    return F(x)

def vector(v):
    v=tuple(map(exact,v))
    if len(v)!=6:raise ValueError("six endpoint coordinates required")
    return v

def radius(r):
    r=exact(r)
    if not 0<=r<=1:raise ValueError("r must be in [0,1]")
    return r

def weight(v,r):
    am,ap,bm,bp,cm,cp=vector(v);r=radius(r)
    return max(max(-am,F(0))*max(-cm,F(0))-r*bm*bm,F(0))*max(r*bp*bp-ap*cp,F(0))

def physical(v,r):
    am,ap,bm,bp,cm,cp=vector(v);r=radius(r)
    if not r:raise ValueError("physical normalization needs r>0")
    dm=r*am*cm-r*r*bm*bm;ds=r*ap*cp-r*r*bp*bp
    return abs(dm*ds)/(r*r) if r*am<0 and dm>0 and ds<0 else F(0)

def terms(v,r,mutant=None):
    am,ap,bm,bp,cm,cp=vector(v);r=radius(r);g=cp-cm
    rr=r*r if mutant=="M1" else r
    den=32 if mutant=="M2" else 16
    return rr*abs(am)*bp*bp*abs(g),abs(am)*(ap-1)**2*g*g/den

def centered_even(k):
    value=1
    for n in range(1,2*k,2):value*=n
    return value

def normal_even(m,s2,k,mutant=None):
    m,s2=exact(m),exact(s2)
    if type(k) is not int or k<0 or s2<0:raise ValueError("invalid normal moment parameters")
    if mutant=="M5":m=F(0)
    return sum((F(comb(2*k,2*j)*centered_even(j))*m**(2*k-2*j)*s2**j
                for j in range(k+1)),F(0))

def mixed_fourth(m,s,n,t):
    m,s,n,t=map(exact,(m,s,n,t));value=F(0)
    for i,j in itertools.product(range(5),repeat=2):
        if (i+j)%2:continue
        value+=comb(4,i)*comb(4,j)*m**(4-i)*s**i*n**(4-j)*t**j*centered_even((i+j)//2)
    return value

def need(ok,reason):
    if not ok:raise ValueError(reason)

def controls(mutant=None):
    counts={"isolated_witnesses":0,"physical":0,"pointwise":0,"eighth":0,"mixed":0}
    v=(-1,1,0,1,-1,0);r=F(1,4)
    need(weight(v,r)<=sum(terms(v,r,mutant)),"RADIAL_SCALE");counts["isolated_witnesses"]+=1
    v=(-1,-1,0,0,-1,1)
    need(weight(v,0)<=sum(terms(v,0,mutant)),"QUARTIC_CONSTANT");counts["isolated_witnesses"]+=1
    v=(-1,1,0,0,-1,-1)
    lhs=weight(v,0) if mutant=="M3" else F(0)
    need(lhs<=sum(terms(v,0)),"EVENT_RESTRICTION");counts["isolated_witnesses"]+=1
    need(normal_even(0,1,4)<=(15 if mutant=="M4" else 105),"GAUSSIAN_EIGHTH");counts["isolated_witnesses"]+=1
    need(normal_even(2,0,4,mutant)==256,"GAUSSIAN_MEAN");counts["isolated_witnesses"]+=1
    p=F(1,1000);e2=8*p;false_bound=p*p<=F(105,64)*e2**4
    need(false_bound if mutant=="M6" else not false_bound,"GAUSSIAN_PREMISE_ESSENTIAL");counts["isolated_witnesses"]+=1
    n=weight((-1,-1,0,0,F(-1,2),F(1,2)),0)
    need((n if mutant=="M7" else n/n)==1,"NORMALIZER");counts["isolated_witnesses"]+=1

    for v in itertools.product((-1,0,1),repeat=6):
        for r in (F(1,4),F(1)):
            need(weight(v,r)==physical(v,r),"BASE_PHYSICAL");counts["physical"]+=1
        for r in (F(0),F(1,4),F(1)):
            lhs=weight(v,r) if v[5]>=0 else F(0)
            need(lhs<=sum(terms(v,r)),"BASE_MAJORANT");counts["pointwise"]+=1
    for m,s2 in itertools.product((-2,-1,0,1,2),(F(0),F(1,4),F(1),F(4))):
        need(normal_even(m,s2,4)<=105*(m*m+s2)**4,"BASE_EIGHTH");counts["eighth"]+=1
    for m,s,n,t in itertools.product((-1,0,1),repeat=4):
        need(mixed_fourth(m,s,n,t)<=105*(m*m+s*s)**2*(n*n+t*t)**2,"BASE_MIXED");counts["mixed"]+=1
    return {"scientific_effect":"NONE","counts":counts,"total":sum(counts.values()),
            "scope":"exact finite diagnostics; not continuum proof or Lean"}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mutant",choices=[f"M{i}" for i in range(1,8)])
    a=p.parse_args()
    try:result=controls(a.mutant)
    except (ValueError,TypeError) as exc:
        print("SIGN_FAIL: "+str(exc),file=sys.stderr);return 1
    print(json.dumps(result,sort_keys=True));return 0
if __name__=="__main__":sys.exit(main())
