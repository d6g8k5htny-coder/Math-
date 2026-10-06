#!/usr/bin/env python3
"""Exact finite controls for the conditional cubic saddle-sign bound.

Standard library only. These controls are not a continuum proof or Lean run.
"""
import argparse
from fractions import Fraction as F
import itertools
import json
from math import factorial, comb
import sys


def exact(value):
    if type(value) not in (int,F):
        raise TypeError('exact int or Fraction required')
    return F(value)


def radius(value):
    value=exact(value)
    if not 0<=value<=1:
        raise ValueError('radius must lie in [0,1]')
    return value


def positive(value):
    return max(F(0),value)


def weight(v,r):
    v=tuple(map(exact,v)); r=radius(r)
    if len(v)!=6:
        raise ValueError('six endpoint coordinates required')
    am,ap,bm,bp,cm,cp=v
    return positive(positive(-am)*positive(-cm)-r*bm*bm)*positive(r*bp*bp-ap*cp)


def band_integral(am,ap,bm,bp,g,r):
    """Exact Lebesgue integral of T_r over c_plus>=0 at fixed other coordinates."""
    am,ap,bm,bp,g=map(exact,(am,ap,bm,bp,g)); r=radius(r)
    a=positive(-am)
    if a==0 or g<=0:
        return F(0)
    f0=a*g-r*bm*bm
    upper=positive(f0/a)
    if ap>0:
        upper=min(upper,r*bp*bp/ap)
    # (f0-a*t)*(r*bp^2-ap*t) integrated to the first positive-part zero.
    return f0*r*bp*bp*upper-(a*r*bp*bp+f0*ap)*upper**2/2+a*ap*upper**3/3


def band_bound(am,ap,bp,g,r,mutant=None):
    am,ap,bp,g=map(exact,(am,ap,bp,g)); r=radius(r)
    a=abs(am); g=positive(g)
    c2=4 if mutant=='M1' else 2
    c3=12 if mutant=='M2' else 6
    return a*(r*bp*bp*g*g/c2+positive(-ap)*g**3/c3)


def identity(n):
    return [[F(int(i==j)) for j in range(n)] for i in range(n)]


def matrix(a):
    a=[list(map(exact,row)) for row in a]
    if not a or not a[0] or any(len(row)!=len(a[0]) for row in a):
        raise ValueError('nonempty rectangular matrix required')
    return a


def matmul(a,b):
    a,b=matrix(a),matrix(b)
    if len(a[0])!=len(b):
        raise ValueError('matrix shapes do not compose')
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]


def inverse(a):
    a=matrix(a); n=len(a)
    if len(a[0])!=n:
        raise ValueError('square matrix required')
    a=[row+unit for row,unit in zip(a,identity(n))]
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None: raise ValueError('singular matrix')
        a[j],a[pivot]=a[pivot],a[j]
        t=a[j][j]; a[j]=[x/t for x in a[j]]
        for i in range(n):
            if i!=j:
                t=a[i][j]; a[i]=[x-t*y for x,y in zip(a[i],a[j])]
    return [row[n:] for row in a]


def determinant(a):
    a=matrix(a); n=len(a); ans=F(1)
    if len(a[0])!=n: raise ValueError('square matrix required')
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None: return F(0)
        if pivot!=j: a[j],a[pivot]=a[pivot],a[j]; ans=-ans
        t=a[j][j]; ans*=t
        for i in range(j+1,n):
            s=a[i][j]/t
            a[i]=[x-s*y for x,y in zip(a[i],a[j])]
    return ans


def hermite(m,mutant=None):
    if type(m) is not int or m not in (2,3): raise ValueError('m must be 2 or 3')
    return [[F(0) if j<ell else F((1 if mutant=='M3' else factorial(j)//factorial(j-ell))*sign**(j-ell))
             for j in range(2*m)] for sign in (-1,1) for ell in range(m)]


def recover(coefficients,m,h):
    h=exact(h)
    if h<=0: raise ValueError('positive half-separation required')
    coefficients=list(map(exact,coefficients))
    values=[]
    for sign in (-1,1):
        for ell in range(m):
            values.append(sum((c*F(factorial(j),factorial(j-ell))*(sign*h)**(j-ell)*h**ell
                               for j,c in enumerate(coefficients) if j>=ell),F(0)))
    scaled=matmul(inverse(hermite(m)),[[x] for x in values])
    return [F(factorial(j))*row[0]/h**j for j,row in enumerate(scaled)]


def gram(rows):
    return matmul(rows,list(map(list,zip(*rows))))


def observation_rows(h,drop_q=False):
    """A finite independent-coefficient polynomial Gaussian, not a periodic field."""
    h=exact(h)
    if h<=0: raise ValueError('positive half-separation required')
    powers=[(j,0) for j in range(6)]+[(j,1) for j in range(4)]+[(1,2),(0,2),(6,0),(4,1),(2,2)]
    if drop_q: powers.remove((0,2))
    def row(x,dx,dy):
        return [x**(p-dx)/factorial(p-dx) if q==dy and p>=dx else F(0) for p,q in powers]
    rows=[row(sign*h,ell,0) for sign in (-1,1) for ell in range(3)]
    rows += [row(sign*h,ell,1) for sign in (-1,1) for ell in range(2)]
    plus,minus=row(h,0,2),row(-h,0,2)
    rows.append([(x-y)/(2*h) for x,y in zip(plus,minus)])
    return rows,plus


def residual_variance(rows,target,mutant=None):
    target=list(map(exact,target)); raw=sum((x*x for x in target),F(0))
    if mutant=='M5': return raw
    k=matmul(rows,[[x] for x in target])
    return raw-matmul(list(map(list,zip(*k))),matmul(inverse(gram(rows)),k))[0][0]


def centered_even(k,mutant=None):
    if type(k) is not int or k<0: raise ValueError('nonnegative integer moment index required')
    if mutant=='M4' and k==6: return 945
    value=1
    for j in range(1,2*k,2): value*=j
    return value


def noncentral_even(m,s,k):
    m,s=exact(m),exact(s)
    if s<0: raise ValueError('standard deviation must be nonnegative')
    return sum((F(comb(2*k,2*j))*m**(2*k-2*j)*s**(2*j)*centered_even(j) for j in range(k+1)),F(0))


def marginal_counterexample():
    # Q uniform[0,1], G=3Q/2, a_minus=a_plus=-1, b_minus=b_plus=0.
    # T=Q^2/2; the invalid use of marginal density cap1 gives E[G^3]/6.
    return F(1,2)*F(1,3),F(3,2)**3*F(1,4)/6


def require(ok,label):
    if not ok: raise ValueError(label)


def controls(mutant=None):
    require(band_integral(-1,0,0,1,2,F(1,2))<=band_bound(-1,0,1,2,F(1,2),mutant),'BAND_R_COEFFICIENT')
    require(band_integral(-1,-1,0,0,1,0)<=band_bound(-1,-1,0,1,0,mutant),'BAND_CUBIC_COEFFICIENT')
    require(hermite(3,mutant)[2][2]==2,'HERMITE_DERIVATIVE_SCALE')
    require(centered_even(6,mutant)==10395,'GAUSSIAN_TWELFTH')
    rows,q=observation_rows(F(1,2))
    require(residual_variance(rows,q,mutant)==F(65,64),'CONDITIONAL_NOT_MARGINAL')
    actual,bad=marginal_counterexample()
    require(actual<=bad if mutant=='M6' else actual>bad,'MARGINAL_DENSITY_NOT_SUFFICIENT')
    counts={'isolated_witnesses':6,'band':0,'hermite_monomials':0,'variance':0,'sharp_cubic':0}
    for am,ap,bm,bp,g,r in itertools.product((-2,-1,0,1),(-2,-1,0,1,2),(0,1,2),(0,1,2),(-1,0,1,2),(F(0),F(1,4),F(1))):
        value=band_integral(am,ap,bm,bp,g,r)
        require(0<=value<=band_bound(am,ap,bp,g,r),'BAND_GRID')
        counts['band']+=1
    for m in (2,3):
        for h in (F(1,2),F(1,4),F(1,8),F(1,16)):
            for j in range(2*m):
                require(recover([int(i==j) for i in range(2*m)],m,h)==[F(factorial(i) if i==j else 0) for i in range(2*m)],'HERMITE_RECOVERY')
                counts['hermite_monomials']+=1
    for h in (F(1,2),F(1,4),F(1,8),F(1,16)):
        rows,q=observation_rows(h)
        require(residual_variance(rows,q)==1+h**4/4,'CONDITIONAL_VARIANCE')
        counts['variance']+=1
        r=2*h
        require(band_integral(-1,1,-1,1,3*r,r)==F(5,6)*r**3,'CUBIC_SHARPNESS')
        counts['sharp_cubic']+=1
    return {'scientific_effect':'NONE','controls':counts,'total':sum(counts.values()),'scope':'finite rational diagnostics; no continuum or Lean execution'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant',choices=['M'+str(i) for i in range(1,7)])
    args=parser.parse_args()
    try: result=controls(args.mutant)
    except (ValueError,TypeError) as exc:
        print('CUBIC_BAND_FAIL: '+str(exc),file=sys.stderr)
        return 1
    print(json.dumps(result,sort_keys=True))
    return 0

if __name__=='__main__': sys.exit(main())
