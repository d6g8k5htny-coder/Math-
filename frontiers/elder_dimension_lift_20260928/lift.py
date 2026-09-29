"""Exact finite helpers for the one-soft-transverse-direction construction.

No Gaussian continuum claim follows from these computations. Standard library only.
"""
from fractions import Fraction as F
from itertools import product
from math import factorial

MUTANT=None

def eye(n): return [[F(int(i==j)) for j in range(n)] for i in range(n)]
def tr(A): return [list(c) for c in zip(*A)]
def mm(A,B):
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*B)] for row in A]

def solve(A,b):
    n=len(A)
    if n==0 or len(b)!=n or any(len(row)!=n for row in A):
        raise ValueError('nonempty square linear system required')
    W=[[F(x) for x in row]+[F(b[i])] for i,row in enumerate(A)]
    for j in range(n):
        p=next((i for i in range(j,n) if W[i][j]),None)
        if p is None: raise ValueError('singular matrix')
        W[j],W[p]=W[p],W[j]
        pivot=W[j][j]; W[j]=[x/pivot for x in W[j]]
        for i in range(n):
            if i!=j:
                v=W[i][j]; W[i]=[x-v*y for x,y in zip(W[i],W[j])]
    return [row[-1] for row in W]

def det(A):
    n=len(A)
    if not n:return F(1)
    W=[[F(x) for x in row] for row in A]; out=F(1)
    for j in range(n):
        p=next((i for i in range(j,n) if W[i][j]),None)
        if p is None:return F(0)
        if p!=j:W[j],W[p]=W[p],W[j];out=-out
        pivot=W[j][j];out*=pivot
        for i in range(j+1,n):
            z=W[i][j]/pivot
            for k in range(j+1,n):W[i][k]-=z*W[j][k]
    return out

def rank(A):
    W=[[F(x) for x in row] for row in A]
    if not W:return 0
    h=0
    for j in range(len(W[0])):
        p=next((i for i in range(h,len(W)) if W[i][j]),None)
        if p is None:continue
        W[h],W[p]=W[p],W[h];pivot=W[h][j]
        for i in range(h+1,len(W)):
            z=W[i][j]/pivot
            if z:
                for k in range(j,len(W[0])):W[i][k]-=z*W[h][k]
        h+=1
        if h==len(W):break
    return h

def chart(D,v,sigma):
    q=solve(D,v);n=len(D)
    sign=-1 if MUTANT=='wrong-schur-sign' else 1
    a=F(sigma)+sign*sum((x*y for x,y in zip(v,q)),F(0))
    A=[[a,*v]]+[[v[i],*D[i]] for i in range(n)]
    S=eye(n+1)
    for i in range(n):S[i+1][0]=F(0) if MUTANT=='omit-shear' else -q[i]
    return A,S

def multiindices(d,degree,upto=False):
    return [a for a in product(range(degree+1),repeat=d) if sum(a)<=degree] if upto else [a for a in product(range(degree+1),repeat=d) if sum(a)==degree]

def monomial(x,a):
    out=1
    for u,p in zip(x,a):out*=u**p
    return out

def jet_labels(d):
    zero=(0,)*d; e=[tuple(int(i==j) for j in range(d)) for i in range(d)]
    plus=lambda a,b:tuple(x+y for x,y in zip(a,b))
    ex=e[0]; two=plus(ex,ex);three=plus(two,ex)
    U=[zero,ex,two,three]
    for j in range(1,d):U += [e[j],plus(ex,e[j])]
    J=[a for a in multiindices(d,3,upto=True) if a not in U]
    if MUTANT=='duplicate-cubic-pin':J[-1]=three
    return U,J

def _pmul(P,Q):
    R={}
    for a,c in P.items():
        for b,e in Q.items():
            k=tuple(x+y for x,y in zip(a,b));R[k]=R.get(k,F(0))+c*e
    return {a:c for a,c in R.items() if c}

def cubic_change(d,q):
    """Map third-derivative coordinates by f -> f(x,z,w-q z); pure xxx stays fixed."""
    labels=multiindices(d,3);M=[[F(0) for _ in labels] for _ in labels]
    unit=[tuple(int(i==j) for j in range(d)) for i in range(d)]
    substitutions=[{u:F(1)} for u in unit]
    for j,v in enumerate(q):substitutions[j+2][unit[1]]=-v
    def mf(a):
        out=1
        for x in a:out*=factorial(x)
        return out
    for j,a in enumerate(labels):
        P={(0,)*d:F(1,mf(a))}
        for i,power in enumerate(a):
            for _ in range(power):P=_pmul(P,substitutions[i])
        for i,b in enumerate(labels):M[i][j]=P.get(b,F(0))*mf(b)
    return labels,M

def rare_power(d):return d-1 if MUTANT=='rare-every-direction' else 1
def weight_power(d):return 2*d if MUTANT=='all-directions-soft' else 4
def band_width(r,k,epsilon):return 2*epsilon*k*(1 if MUTANT=='drop-band-jacobian' else r)

def plane(X,Z,k,s,a,beta,c):
    lin=0 if MUTANT=='drop-transverse-linear' else F(1,4)
    value=2*k*X**3-F(3,2)*k*X-k/2+s*Z*Z/2+a*(X*X-lin)*Z/2+beta*X*Z*Z/2+c*Z**3/6
    dx=6*k*X*X-F(3,2)*k+a*X*Z+beta*Z*Z/2
    dz=s*Z+a*(X*X-lin)/2+beta*X*Z+c*Z*Z/2
    return value,[dx,dz]

def blocks(A,C,D):
    return [list(A[i])+list(C[i]) for i in range(len(A))]+[list(row)+list(D[i]) for i,row in enumerate(tr(C))]

def schur(A,C,D):
    invC=tr([solve(D,row) for row in C]);Q=mm(C,invC)
    if MUTANT=='ignore-cross-schur':Q=[[F(0) for _ in A] for _ in A]
    return [[A[i][j]-Q[i][j] for j in range(len(A))] for i in range(len(A))]

def endpoint_model(d,r,k):
    stable=1 if MUTANT=='positive-stiff' else -1
    def diag(vals):return [[v if i==j else F(0) for j in range(d)] for i,v in enumerate(vals)]
    return diag([-6*k*r,-k*r/2]+[F(stable)]*(d-2)),diag([6*k*r,-5*k*r/2]+[F(stable)]*(d-2))

def inertia(A):
    """Exact Descartes signs for a real-rooted characteristic polynomial of a symmetric matrix."""
    n=len(A);coef=[F(1)];B=eye(n)
    for k in range(1,n+1):
        AB=mm(A,B);c=-sum(AB[i][i] for i in range(n))/k
        coef.append(c);B=[[AB[i][j]+(c if i==j else 0) for j in range(n)] for i in range(n)]
    asc=list(reversed(coef));z=0
    while z<n and asc[z]==0:z+=1
    signs=[v*(-1)**i>0 for i,v in enumerate(asc) if v]
    neg=sum(a!=b for a,b in zip(signs,signs[1:]))
    return neg,z

def loss_powers():
    return (F(-1,3)+(0 if MUTANT=='omit-loss-factor' else 1),F(-2,3)-1)
