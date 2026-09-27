"""Exact polynomial checks for a thin-tube candidate, not an analytic verifier.

Five variables are (r,x,z,u,v). Arithmetic is Fraction only; no external packages.
"""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import permutations
import json
import math

ZERO = (0, 0, 0, 0, 0)

def constant(c=0):
    c=Q(c)
    return {ZERO:c} if c else {}

def monomial(exponents, c=1):
    if len(exponents)!=5 or any(type(e) is not int or e<0 for e in exponents):
        raise ValueError('five nonnegative integer exponents required')
    return {tuple(exponents):Q(c)} if c else {}

def add(*ps):
    out={}
    for p in ps:
        for e,c in p.items(): out[e]=out.get(e,Q(0))+c
    return {e:c for e,c in out.items() if c}

def scale(p,c): return {e:a*Q(c) for e,a in p.items() if a*Q(c)}

def mul(p,q):
    out={}
    for e,c in p.items():
        for f,d in q.items():
            ef=tuple(a+b for a,b in zip(e,f))
            out[ef]=out.get(ef,Q(0))+c*d
    return {e:c for e,c in out.items() if c}

def power(p,n):
    if type(n) is not int or n<0: raise ValueError('nonnegative integer power required')
    out=constant(1)
    for _ in range(n): out=mul(out,p)
    return out

def variable(i):
    e=list(ZERO); e[i]=1
    return monomial(e)

r,x,z,u,v=map(variable,range(5))

def derivative(p,i,n=1):
    for _ in range(n):
        out={}
        for e,c in p.items():
            if e[i]:
                f=list(e); f[i]-=1; out[tuple(f)]=c*e[i]
        p=out
    return p

def substitute(p,replacements):
    out={}
    for e,c in p.items():
        term=constant(c)
        for i,n in enumerate(e): term=mul(term,power(replacements.get(i,variable(i)),n))
        out=add(out,term)
    return out

def coefficient_r(p,n):
    return {tuple([0,*e[1:]]):c for e,c in p.items() if e[0]==n}

def midpoint_contact(p,dx,dz):
    p=derivative(derivative(p,1,dx),2,dz)
    return substitute(p,{0:{},1:{},2:{}})

def thin_substitute(p): return substitute(p,{1:mul(r,u),2:mul(power(r,2),v)})

def completed_monomial(i,j):
    """Subtract cubic Hermite axis data and linear transverse-gradient data."""
    if any(type(n) is not int or n<0 for n in (i,j)): raise ValueError('invalid degree')
    p=mul(power(x,i),power(z,j)); h=scale(r,Q(1,2))
    if j==0:
        if i<4: return {}
        if i%2==0:
            hpoly=add(scale(power(h,i),1-Q(i,2)),
                      scale(mul(power(h,i-2),power(x,2)),Q(i,2)))
        else:
            hpoly=add(scale(mul(power(h,i-1),x),Q(3-i,2)),
                      scale(mul(power(h,i-3),power(x,3)),Q(i-1,2)))
        return add(p,scale(hpoly,-1))
    if j==1:
        interp=power(h,i) if i%2==0 else mul(power(h,i-1),x)
        return add(p,scale(mul(interp,z),-1))
    return p

def target_cubic():
    # b=0,k=1; the finite-r two-height/two-slope Hermite interpolant.
    return add(scale(power(x,3),2),scale(mul(power(r,2),x),Q(-3,2)),
               scale(power(r,3),Q(-1,2)))

def completed_axial_quartic(radius,point):
    p=substitute(completed_monomial(4,0),{0:constant(radius),1:constant(point)})
    return p.get(ZERO,Q(0))

def contact_rows():
    gap=add(power(u,2),constant(Q(-1,4)))
    a=scale(mul(u,gap),Q(1,6)); b=scale(gap,Q(1,2))
    return [[a,mul(u,v),{}],[{},b,v]]

def determinant(matrix):
    n=len(matrix)
    if any(len(row)!=n for row in matrix): raise ValueError('square matrix required')
    out={}
    for p in permutations(range(n)):
        inversions=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=constant((-1)**inversions)
        for i in range(n): term=mul(term,matrix[i][p[i]])
        out=add(out,term)
    return out

def reference_cov(a,b):
    out=Q((-1)**sum(b))
    for n in (a[0]+b[0],a[1]+b[1]):
        if n%2: return Q(0)
        out*=(-1)**(n//2)*math.prod(range(1,n,2))
    return out

def inverse(a):
    n=len(a); m=[[Q(x) for x in row]+[Q(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if m[i][j]),None)
        if pivot is None: raise ValueError('singular matrix')
        m[j],m[pivot]=m[pivot],m[j]; q=m[j][j]; m[j]=[x/q for x in m[j]]
        for i in range(n):
            if i!=j:
                q=m[i][j]; m[i]=[x-q*y for x,y in zip(m[i],m[j])]
    return [row[n:] for row in m]

def reference_schur():
    # NONPERIODIC reference diagnostic only. The proof uses exact periodic positivity.
    pins=[(0,0),(1,0),(2,0),(3,0),(0,1),(1,1)]
    free=[(4,0),(2,1),(0,2)]
    gi=inverse([[reference_cov(a,b) for b in pins] for a in pins])
    cross=[[reference_cov(a,b) for b in pins] for a in free]
    return [[reference_cov(a,b)-sum(cross[i][s]*gi[s][t]*cross[j][t]
                for s in range(6) for t in range(6))
             for j,b in enumerate(free)] for i,a in enumerate(free)]

def report():
    return {'object':'D5-THIN-TUBE-20260925-v1',
            'polynomial_degree_checked':8,'monomial_basis_size':45,
            'physical_coordinates':['r*u','r^2*v'],
            'normalized_centered_gradient_powers':[3,2],
            'contact_jets':['R0_xxxx','R0_xxz','R0_zz'],
            'contact_rows':[['u*(u^2-1/4)/6','u*v','0'],['0','(u^2-1/4)/2','v']],
            'minor':'u*(u^2-1/4)^2/12',
            'reference_schur':[[str(q) for q in row] for row in reference_schur()],
            'reference_is_periodic_covariance':False,
            'power_ledger':{'area':3,'gradient_density':-5,'triple_hessian_cost':-6,
                            'full_normalizer_division':-2,'total':-10},
            'candidate_count_bound':'C*r^-10*exp(-c/r^2)',
            'analytic_proof_checked_by_code':False,'independent_review':False,
            'full_annulus_closed':False,'scientific_effect':'NONE'}

if __name__=='__main__': print(json.dumps(report(),indent=2,sort_keys=True))
