#!/usr/bin/env python3
"""Exact rational checks for OA-PIN-MICRO-COV-20260926-v1."""
from fractions import Fraction as F

def det2(a,b,c,d):
    return a*d-b*c

def minors(r,P,Q):
    a11=F(0)
    a12=Q*(r*P-F(1,2))
    a13=r*P*(2*r*P-1)*(r*P-1)/12
    a21=Q
    a22=r*P*(r*P-1)/2
    a23=F(0)
    return (
        det2(a11,a12,a21,a22),
        det2(a11,a13,a21,a23),
        det2(a12,a13,a22,a23),
    )

def main():
    samples=[
        (F(1,100),F(2),F(3,5)),
        (F(1,50),F(-3),F(1,7)),
        (F(1,20),F(1),F(-2,9)),
        (F(1,40),F(4),F(0)),
    ]
    for r,P,Q in samples:
        assert abs(r*P)<=F(1,4)
        m1,m2,m3=minors(r,P,Q)
        assert m1 == -Q*Q*(2*r*P-1)/2
        assert m2 == -r*P*Q*(r*P-1)*(2*r*P-1)/12
        assert m3 == -r*r*P*P*(r*P-1)**2*(2*r*P-1)/24
        h2=Q*Q+r*r*P*P
        gramdet=m1*m1+m2*m2+m3*m3
        assert gramdet >= h2*h2/F(20000)
    # Deliberately incomplete minor formulas are rejected.
    r,P,Q=F(1,100),F(2),F(3,5)
    m1,m2,m3=minors(r,P,Q)
    assert m1 != -Q*Q/2
    assert m3 != F(0)
    print("ok")

if __name__=="__main__":
    main()
