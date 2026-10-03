"""Exact finite controls for the inverse-radius asymptotic candidate.

Standard library only. Series calculations are formal algebra, not authentication
of Gaussian premises or a proof of domination/total-variation convergence.
"""
import argparse
from fractions import Fraction as F
import json
from math import comb

MUTANTS=('omit-shift','omit-density-term','drop-a-shear','odd-term-survives',
         'unsigned-is-signed','wrong-b-integral','wrong-density-factor','wrong-tv-root')


def rational(x):
    if type(x) not in (int,F): raise TypeError('exact int/Fraction required')
    return F(x)


def add(a,b):
    out=dict(a)
    for i,x in b.items():out[i]=out.get(i,F(0))+x
    return {i:x for i,x in out.items() if x}


def scale(a,c): return {i:x*c for i,x in a.items() if x*c}


def mul(a,b):
    out={}
    for i,x in a.items():
        for j,y in b.items():out[i+j]=out.get(i+j,F(0))+x*y
    return {i:x for i,x in out.items() if x}


def power(a,n):
    out={0:F(1)}
    for _ in range(n):out=mul(out,a)
    return out


def integral(a,lo,hi):
    return sum((x*(hi**(i+1)-lo**(i+1))/F(i+1) for i,x in a.items()),F(0))


def shape_integrals():
    b={0:F(3),2:F(-12)};u={1:F(1)};hi={0:F(3),1:F(-6)}
    # Q=(4v^2-b^2)(b-4uv); dictionary index is v power.
    Q={3:scale(u,-16),2:scale(b,4),1:scale(mul(u,power(b,2)),4),0:scale(power(b,3),-1)}
    ans={key:F(0) for key in ('I','U2','B','ABS_U')}
    for lo_u,hi_u,sgn_b,sgn_u in ((F(-3,2),F(-1,2),-1,-1),(F(-1,2),F(0),1,-1),(F(0),F(1,2),1,1)):
        low=scale(b,F(sgn_b,2));vint={}
        for j,c in Q.items():
            difference=add(power(hi,j+1),scale(power(low,j+1),-1))
            vint=add(vint,scale(mul(c,difference),F(1,j+1)))
        for key,weight in [('I',{0:F(1)}),('U2',{2:F(1)}),('B',b),('ABS_U',{1:F(sgn_u)})]:
            ans[key]+=integral(mul(vint,weight),lo_u,hi_u)
    return ans


def smul(a,b,n):
    out=[F(0)]*(n+1)
    for i,x in enumerate(a[:n+1]):
        for j,y in enumerate(b[:n+1-i]):out[i+j]+=x*y
    return out


def spow(a,m,n):
    out=[F(1)]+[F(0)]*n
    for _ in range(m):out=smul(out,a,n)
    return out


def endpoints(u,A,g,n):
    u,A,g=map(rational,(u,A,g))
    if type(n) is not int or not 0<=n<=12: raise ValueError('series order 0..12 required')
    if g<=0 or g*g!=1+A*A: raise ValueError('positive exact gamma^2=1+A^2 required')
    inv=[F(0)]*(n+1);root=[F(0)]*(n+1)
    binom=F(1)
    for j in range(n//2+1):
        inv[2*j]=u**(2*j)
        if j:binom*= (F(1,2)-(j-1))/j
        root[2*j]=g*binom*(-u*u/(g*g))**j
    d=smul(inv,root,n)
    m=[F(0)]+[-u*A*x for x in inv[:n]]
    plus=[x+y for x,y in zip(m,d)];minus=[x-y for x,y in zip(m,d)]
    return plus,minus


def validate_phi(phi,n):
    if not isinstance(phi,dict) or any(type(j) is not int or j<0 for j in phi):
        raise ValueError('nonnegative polynomial orders required')
    return {j:rational(x) for j,x in phi.items() if j<=n}


def tail_series(u,A,g,phi,n):
    plus,minus=endpoints(u,A,g,n);phi=validate_phi(phi,n)
    out=[F(0)]*(n+1)
    for j,c in phi.items():
        p=spow(plus,11+j,n-j);m=spow(minus,11+j,n-j)
        for i in range(n-j+1):out[i+j]+=c*(p[i]-m[i])/F(11+j)
    return out


def half_series(u,A,g,phi,n,sign):
    if type(sign) is not int or sign not in (-1,1): raise ValueError('sign must be +/-1')
    plus,minus=endpoints(u,A,g,n);phi=validate_phi(phi,n)
    endpoint=plus if sign==1 else [-x for x in minus]
    out=[F(0)]*(n+1)
    for j,c in phi.items():
        p=spow(endpoint,11+j,n-j)
        for i in range(n-j+1):out[i+j]+=c*sign**j*p[i]/F(11+j)
    return out


def density_series(coeffs):return [(11+j)*x for j,x in enumerate(coeffs)]


def predicted_second(u,A,g,phi0,phi2):
    return u*u*g**9*(1+12*A*A)*phi0+F(2,13)*g**13*phi2


def check(mutant=None):
    vals=shape_integrals()
    expected={'I':F(246528,35),'U2':F(240192,35),'B':F(-428544,7),'ABS_U':F(5898627,880)}
    if mutant=='wrong-b-integral': vals['B']=-vals['B']
    if vals!=expected: raise ValueError('shape integral mismatch')
    cases=0
    for u in (F(-5,4),F(-3,4),F(-1,4),F(1,4)):
        for p in (F(-1,2),F(0),F(1,3)):
            A=2*p/(1-p*p);g=(1+p*p)/(1-p*p)
            phi={0:F(2),2:F(-3),3:F(5),4:F(7)}
            got=tail_series(u,A,g,phi,6)
            if got[0]!=2*g**11*phi[0]/11:raise ValueError('leading coefficient')
            guess=predicted_second(u,A,g,phi[0],phi[2])
            if mutant=='omit-shift':guess-=10*u*u*A*A*g**9*phi[0]
            if mutant=='omit-density-term':guess-=F(2,13)*g**13*phi[2]
            if mutant=='drop-a-shear':guess=predicted_second(u,F(0),F(1),phi[0],phi[2])
            if got[2]!=guess:raise ValueError('second coefficient mismatch')
            odd=[got[i] for i in (1,3,5)]
            if mutant=='odd-term-survives':odd[0]=1
            if any(odd):raise ValueError('odd inverse powers do not cancel')
            hplus=half_series(u,A,g,phi,6,1);hminus=half_series(u,A,g,phi,6,-1)
            if [a+b for a,b in zip(hplus,hminus)]!=got:raise ValueError('half sum')
            h1=-u*A*g**10*phi[0]
            if mutant=='unsigned-is-signed':h1=F(0)
            if hplus[1]!=h1:raise ValueError('signed first-order bias')
            den=density_series(got)
            expected_den=13*got[2]
            if mutant=='wrong-density-factor':expected_den=11*got[2]
            if den[2]!=expected_den:raise ValueError('radial density coefficient')
            cases+=1
    crossing2=F(13,11) if mutant!='wrong-tv-root' else F(11,13)
    if F(13,11)/crossing2!=1:raise ValueError('TV crossing root')
    return {'passed':True,'mathematical_acceptance':False,'scientific_effect':'NONE',
            'scope':'finite rational coefficient and parity controls only',
            'shape_integrals':{k:str(v) for k,v in expected.items()},
            'series_cases':cases,'tail_exponents':[11,13,15],
            'unsigned_radial_rate':2,'signed_joint_rate':1,'tv_crossing_squared':str(crossing2)}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--mutant',choices=MUTANTS)
    args=parser.parse_args()
    try:result=check(args.mutant)
    except ValueError as exc:
        print(json.dumps({'passed':False,'error':str(exc)},sort_keys=True));raise SystemExit(1)
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()
