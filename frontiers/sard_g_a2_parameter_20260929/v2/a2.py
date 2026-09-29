"""Exact finite controls for a fixed-frame Lyapunov--Perron proof.

No numerical trajectory sampling and no Gaussian continuum acceptance.
"""
from fractions import Fraction as F
from math import comb

MUTANT=None

def _positive(*values):
    if any(F(x)<=0 for x in values):
        raise ValueError('positive spectral/radius data required')

def lp_constants(lam,mu,ell,beta):
    lam,mu,ell,beta=map(F,(lam,mu,ell,beta))
    _positive(lam,mu,ell,beta)
    if beta>=lam:
        raise ValueError('unstable weight must be below lambda')
    cu=1/(lam+beta) if MUTANT=='wrong-unstable-weight' else 1/(lam-beta)
    cs=1/(mu-beta) if MUTANT=='wrong-stable-weight' else 1/(mu+beta)
    return ell*(1/lam+1/mu),ell*(cu+cs)

def anchor_equilibrium(lam,mu,bu,bs):
    """Bounded constant path of x'=lambda*x+bu, y'=-mu*y+bs."""
    lam,mu,bu,bs=map(F,(lam,mu,bu,bs));_positive(lam,mu)
    if MUTANT=='drop-constant-forcing':
        return F(0),F(0)
    px=bu/lam if MUTANT=='reverse-unstable-integral' else -bu/lam
    return px,bs/mu

def unstable_polynomial(lam,mu,rho,c):
    """Triangular ILLUSTRATION x'=lambda*x+c, y'=-mu*y+rho*x^2.

Returns px and coefficients of y(s)=y0+y1*s+y2*s^2, s=x-px.
This illustrative vector field need not be a gradient and is labelled as such.
"""
    lam,mu,rho,c=map(F,(lam,mu,rho,c));_positive(lam,mu)
    px=anchor_equilibrium(lam,mu,c,0)[0]
    return px,rho*px*px/mu,2*rho*px/(mu+lam),rho/(mu+2*lam)

def fixed_anchor_derivative(lam,mu,rho,c,a):
    lam,mu,rho,c,a=map(F,(lam,mu,rho,c,a));_positive(lam,mu)
    p=-c/lam;s=a-p
    dp=-1/lam
    return dp*(2*rho*p/mu+2*rho*(a-2*p)/(mu+lam)-2*rho*s/(mu+2*lam))

def matrix_inverse2(A):
    a,b=A[0];c,d=A[1];det=a*d-b*c
    if not det:raise ValueError('singular matrix')
    return [[d/det,-b/det],[-c/det,a/det]]

def mm(A,B):
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*B)] for row in A]

def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))

def projection(v,n):
    v=list(map(F,v));n=list(map(F,n));den=dot(v,n)
    if den==0:raise ValueError('transverse normal denominator required')
    if MUTANT=='omit-hit-time-projection':
        return [[F(1),F(0)],[F(0),F(1)]]
    return [[F(int(i==j))-v[i]*n[j]/den for j in range(2)] for i in range(2)]

def adjoint_hit(v,n,tau):
    P=projection(v,n)
    return [sum(F(tau[i])*P[i][j] for i in range(2)) for j in range(2)]

def eigenline_quotient_bounds(n):
    """At t=n^-4: k=sqrt(t)=n^-2, 1<sqrt(1+t)<1+t/2.

Bounds for slope(t)/t, without approximating the square root.
"""
    if type(n) is not int or n<2:raise ValueError('integer n>=2 required')
    t=F(1,n**4);k=F(1,n**2)
    if MUTANT=='pretend-Lipschitz-eigenline':
        return F(0),F(1)
    return k/(t*(2+t/2)),k/(2*t)

def beta_polynomial_integral(n):
    """Integral_0^1 x^n (1-x)^n dx by finite rational expansion."""
    if type(n) is not int or n<0:raise ValueError('integer n>=0 required')
    return sum((F((-1)**j*comb(n,j),n+j+1) for j in range(n+1)),F(0))

def density_mesh_powers():
    """Probabilistic dimension ledger, not a continuum probability calculation."""
    morse=F(2)+F(1,2)-2
    distinct=F(5)-4
    if MUTANT=='omit-height-difference':distinct=F(4)-4
    if MUTANT=='ignore-singular-slab':morse=F(2)-2
    return morse,distinct

def gaussian_residual_covariances(weights,ell):
    weights=list(map(F,weights));ell=list(map(F,ell))
    v=sum(w*l*l for w,l in zip(weights,ell))
    if v<=0:raise ValueError('positive variance required')
    q=[w*l for w,l in zip(weights,ell)]
    scale=F(1) if MUTANT=='wrong-residual-scale' else 1/v
    # xi=ell(f), g=f-(Qell/v)*xi: unnormalised exact equivalent.
    return [a-a*scale*v for a in q]

def matrix_rank(rows):
    A=[list(map(F,row)) for row in rows]
    if not A:return 0
    r=0
    for j in range(len(A[0])):
        pivot=next((i for i in range(r,len(A)) if A[i][j]),None)
        if pivot is None:continue
        A[r],A[pivot]=A[pivot],A[r]
        for i in range(r+1,len(A)):
            if A[i][j]:
                q=A[i][j]/A[r][j]
                A[i]=[a-q*b for a,b in zip(A[i],A[r])]
        r+=1
        if r==len(A):break
    return r
