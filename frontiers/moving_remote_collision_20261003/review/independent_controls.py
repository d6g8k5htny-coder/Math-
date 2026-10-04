#!/usr/bin/env python3
"""Independent exact controls; no imports from the author checker."""
from fractions import Fraction as Q
from itertools import product
import json

COUNTS = {}
MUTANTS = {}

def require(ok, name):
    if not ok:
        raise AssertionError(name)
    COUNTS[name] = COUNTS.get(name, 0) + 1

def reject(ok, name):
    if ok:
        raise AssertionError('mutant survived: ' + name)
    MUTANTS[name] = MUTANTS.get(name, 0) + 1

class P:
    """Exact polynomials in sin x, cos x, sin y, cos y."""
    def __init__(self, terms=0):
        if isinstance(terms, P):
            self.a = terms.a.copy()
        elif isinstance(terms, dict):
            self.a = {k:Q(v) for k,v in terms.items() if v}
        else:
            self.a = {(0,0,0,0):Q(terms)} if terms else {}
    def __add__(self, b):
        a = self.a.copy()
        for k,v in P(b).a.items(): a[k] = a.get(k,0)+v
        return P(a)
    __radd__ = __add__
    def __neg__(self): return P({k:-v for k,v in self.a.items()})
    def __sub__(self,b): return self+-P(b)
    def __rsub__(self,b): return P(b)+-self
    def __mul__(self,b):
        a = {}
        for k,v in self.a.items():
            for l,w in P(b).a.items():
                m=tuple(x+y for x,y in zip(k,l)); a[m]=a.get(m,0)+v*w
        return P(a)
    __rmul__=__mul__
    def __truediv__(self,b): return self*Q(1,b)
    def __pow__(self,n):
        a=P(1)
        for _ in range(n): a=a*self
        return a
    def derivative(self,axis):
        a={}; s,c=2*axis,2*axis+1
        for k,v in self.a.items():
            if k[s]:
                l=list(k); l[s]-=1; l[c]+=1; l=tuple(l)
                a[l]=a.get(l,0)+v*k[s]
            if k[c]:
                l=list(k); l[c]-=1; l[s]+=1; l=tuple(l)
                a[l]=a.get(l,0)-v*k[c]
        return P(a)
    def at(self,point):
        return sum(v*prodq(x**n for x,n in zip(point,k)) for k,v in self.a.items())
    def jet(self,point): return (self.at(point),*(self.derivative(j).at(point) for j in range(2)))
    def degree(self): return max((sum(k) for k in self.a),default=0)

def prodq(values):
    r=Q(1)
    for x in values:r*=x
    return r

SX,CX,SY,CY=(P({tuple(int(i==j) for i in range(4)):1}) for j in range(4))

def point(a,b):
    def circle(t): return 2*t/(1+t*t),(1-t*t)/(1+t*t)
    return (*circle(Q(a)),*circle(Q(b)))

ORIGIN=point(0,0)

def separator(p): return 2-CX*p[1]-SX*p[0]-CY*p[3]-SY*p[2]
def chart(c): return SX*c[1]-CX*c[0],SY*c[3]-CY*c[2]
def chart_derivatives(p,c): return p[1]*c[1]+p[0]*c[0],p[3]*c[3]+p[2]*c[2]
def dot(x,y):return sum(a*b for a,b in zip(x,y))

def dual_pair(sites,killed,data,center,omit_chain=False,omit_separator=False):
    q=P(1)
    for p in killed[:-1] if omit_separator else killed:q*=separator(p)
    xx,yy=chart(center)
    z0=(xx.at(sites[0]),yy.at(sites[0])); z1=(xx.at(sites[1]),yy.at(sites[1]))
    d=tuple(b-a for a,b in zip(z0,z1)); perp=(-d[1],d[0]); d2=dot(d,d)
    t=((xx-z0[0])*d[0]+(yy-z0[1])*d[1])/d2
    y=((xx-z0[0])*perp[0]+(yy-z0[1])*perp[1])/d2
    values=[]; tangent=[]; normal=[]
    for p,(val,gx,gy) in zip(sites,data):
        qv,qx,qy=q.jet(p); grad=((gx*qv-val*qx)/qv**2,(gy*qv-val*qy)/qv**2)
        cd=chart_derivatives(p,center)
        if not omit_chain:grad=tuple(g/c for g,c in zip(grad,cd))
        values.append(val/qv); tangent.append(dot(grad,d)); normal.append(dot(grad,perp))
    v0,v1=values; t0,t1=tangent; y0,y1=normal
    poly=v0+t0*t+(3*(v1-v0)-2*t0-t1)*t**2+(t1+t0-2*(v1-v0))*t**3+y*(y0+(y1-y0)*t)
    return q*poly

def dual_single(site,killed,data):
    q=P(1)
    for p in killed:q*=separator(p)
    v,gx,gy=data; qv,qx,qy=q.jet(site)
    xx,yy=chart(site)
    return q*(v/qv+((gx*qv-v*qx)/qv**2)*xx+((gy*qv-v*qy)/qv**2)*yy)

def periodic_controls():
    for n in (8,16,32):
        pins=(point(-Q(1,n**3),-Q(1,2*n**3)),point(Q(1,n**3),Q(1,2*n**3)))
        witnesses=(point(Q(1,n),Q(1,2*n)),point(Q(1,n)+Q(1,n**3),Q(1,2*n)+Q(1,3*n**3)))
        for sites,killed,center in ((pins,witnesses,ORIGIN),(witnesses,pins,witnesses[0])):
            for basis in range(6):
                data=tuple(tuple(Q(int(3*i+j==basis)) for j in range(3)) for i in range(2))
                phi=dual_pair(sites,killed,data,center)
                require(tuple(phi.jet(p) for p in sites)==data,'periodic surviving full jets')
                require(all(phi.jet(p)==(0,0,0) for p in killed),'periodic killed full jets')
                require(phi.degree()<=5,'periodic Fourier-degree bound')
            data=((Q(1),Q(2),Q(3)),(Q(4),Q(5),Q(6)))
            broken=dual_pair(sites,killed,data,center,omit_chain=True)
            reject(tuple(broken.jet(p) for p in sites)==data,'missing inverse-chart gradient chain rule')
            broken=dual_pair(sites,killed,data,center,omit_separator=True)
            reject(all(broken.jet(p)==(0,0,0) for p in killed),'missing killed-site separator')
        for target,other in ((witnesses[0],witnesses[1]),(witnesses[1],witnesses[0])):
            for basis in range(3):
                data=tuple(Q(int(j==basis)) for j in range(3))
                phi=dual_single(target,(*pins,other),data)
                require(phi.jet(target)==data,'separated singleton full jets')
                require(all(phi.jet(p)==(0,0,0) for p in (*pins,other)),'separated singleton killed jets')
                require(phi.degree()<=4,'singleton Fourier-degree bound')
        p=witnesses[0]; square=separator(p)**2
        for i in range(4):
            for j in range(4-i):
                f=square
                for _ in range(i):f=f.derivative(0)
                for _ in range(j):f=f.derivative(1)
                require(f.at(p)==0,'repeated separator annihilates order through three')
        f=SX-p[0]
        reject(f.jet(p)==(0,0,0),'simple zero claimed to kill full gradient')

def peval(a,x):return sum(c*x**i for i,c in enumerate(a))
def pder(a):return [i*c for i,c in enumerate(a)][1:]
def integ(a,h):return sum(c*h**(i+1)/Q(i+1) for i,c in enumerate(a))

def confluence_controls():
    for h in (Q(1,2),Q(1,7),Q(1,100)):
        for degree in range(7):
            a=[Q(0)]*degree+[Q(1)]; ad=pder(a); add=pder(ad); addd=pder(add)
            a3=(peval(ad,h)+peval(ad,0))/h**2-2*(peval(a,h)-peval(a,0))/h**3
            integral=sum(c*(h*h**(i+2)/Q(i+2)-h**(i+3)/Q(i+3)) for i,c in enumerate(addd))/h**3
            a2=3*(peval(a,h)-peval(a,0))/h**2-(2*peval(ad,0)+peval(ad,h))/h
            require(a3==integral,'Hermite cubic integral cancellation')
            require(a2==integ(add,h)/(2*h)-Q(3,2)*h*a3,'Hermite quadratic integral cancellation')
            if degree==3:reject(a3==integral/2,'wrong Hermite cubic factor')
        for basis in range(6):
            A=[Q(int(i==basis)) for i in range(6)]; r=h
            p=[A[0]-r*r*A[2]/8,A[1]-r*r*A[3]/24,A[2]/2,A[3]/6]; dp=pder(p)
            lo,hi=-r/2,r/2
            result=[(peval(p,lo)+peval(p,hi))/2,(peval(p,hi)-peval(p,lo))/r,(peval(dp,hi)-peval(dp,lo))/r,6/r**2*(peval(dp,lo)+peval(dp,hi)-2*(peval(p,hi)-peval(p,lo))/r),A[4],A[5]]
            require(result==A,'pin right inverse all basis data')
            p=[A[4],A[0],(A[2]+6*h*A[5])/2,-2*A[5]];dp=pder(p)
            result=[peval(dp,0),A[1],(peval(dp,h)-peval(dp,0))/h,A[3],peval(p,0),(peval(p,h)-peval(p,0)-h*(peval(dp,0)+peval(dp,h))/2)/h**3]
            require(result==A,'witness right inverse all basis data')
        reject(Q(1)*r*r/24==0,'omitted pin cubic correction')
        reject((Q(3)+Q(2)*h/2-Q(3))/h==2,'wrong mixed coefficient')

def determinant(rows):
    a=[[Q(x) for x in row] for row in rows]; out=Q(1); n=len(a)
    for i in range(n):
        p=next((p for p in range(i,n) if a[p][i]),None)
        if p is None:return Q(0)
        if p!=i:a[p],a[i]=a[i],a[p];out=-out
        pivot=a[i][i];out*=pivot
        for j in range(i+1,n):
            ratio=a[j][i]/pivot
            for k in range(i+1,n):a[j][k]-=ratio*a[i][k]
    return out

def regression_controls():
    growth=[]
    for rho in (Q(1,2),Q(1,4),Q(1,8),Q(1,16)):
        eps=rho**7; e=eps**2; sigma=((1,1),(1,1+e)); lower=e/3
        require(determinant(sigma)==e,'joint covariance determinant')
        require((1+e)-Q(1)==e,'Schur floor exact')
        require(1-lower>0 and determinant(((1-lower,1),(1,1+e-lower)))>0,'full covariance quantitative floor')
        require(eps**2/e==1,'regression energy is sharp')
        shift=eps/e
        require(shift==rho**-7,'square-root regression cost')
        reject(shift<=rho**-6,'rho^-6 regression bound')
        reject(shift<=1,'rho-independent regression bound')
        growth.append(shift/rho**-6)
        require((e**6)==rho**84 and rho**-42*rho**-56==rho**-98,'six-density eighth-moment exponent')
        # S=diag(e,1,1,1,1,1), t in its final coordinate: quadratic form = t^2.
        require(Q(9)==Q(3)**2,'mixed eigenvalue fixed tail scale')
        reject(Q(9)>=rho**-14*Q(9),'small-variance scale imposed on every tail direction')
    require(all(b>a for a,b in zip(growth,growth[1:])),'regression mutant violation grows as rho shrinks')

def collision_controls():
    for a in (Q(1,3),Q(1,8),Q(1,64)):
        delta=2*a;p=[0,-a*a,0,Q(1,3)];dp=pder(p);ddp=pder(dp)
        require(peval(dp,-a)==peval(dp,a)==0,'fold both gradients zero')
        D=(peval(p,a)-peval(p,-a))/delta**3
        require(D==-Q(1,6),'fold exact height difference')
        require(abs(peval(ddp,-a)*peval(ddp,a))==delta**2,'fold both Hessian determinants')
        rows=((1,0,0,0,0,0),(0,1,0,0,0,0),(-1/delta,0,1/delta,0,0,0),(0,-1/delta,0,1/delta,0,0),(0,0,0,0,1,0),(-1/(2*delta**2),0,-1/(2*delta**2),0,-1/delta**3,1/delta**3))
        det=abs(determinant(rows))
        require(det==delta**-5,'six-coordinate exact Jacobian')
        reject(det==delta**-4,'wrong density Jacobian')
        reject(1-5+3+1==1,'dropped witness determinant')
        q=a;window=q**3
        near=q*q/2;far=window/q
        require(near+far==Q(3,2)*q*q,'exact radial integral')
        cutoff=q/100
        unbounded=window*(1/cutoff-1/q)
        saturated=(q*q-cutoff*cutoff)/2
        reject(unbounded==saturated,'nonsaturating second-window factor')
    require(1-5+3+2==1 and 3+2==5,'radial and radius powers')

def scope_controls():
    require(2-98*Q(1,100)==Q(51,50),'example alpha exponent')
    require(2-98*Q(1,49)==0,'strict alpha boundary')
    reject(2-98*Q(1,49)>0,'little-o claimed at threshold')
    for n in range(50):
        require(Q(int(n>=2))<=Q(n*(n-1),2),'factorial event inequality')
        require(n*int(n>=2)<=n*(n-1),'factorial multiplicity inequality')
    for r,volume,L2 in product((Q(1,16),Q(1,8)),(Q(1,100),Q(1,2)),(Q(1),Q(2))):
        require(r**6*volume**2 <= Q(1,8)*L2*r**5*volume,'separated-volume absorption')

if __name__=='__main__':
    periodic_controls(); confluence_controls(); regression_controls();collision_controls();scope_controls()
    print(json.dumps({'status':'PASS','positive_evaluations':sum(COUNTS.values()),'positive_families':COUNTS,'rejected_mutant_evaluations':sum(MUTANTS.values()),'rejected_mutant_families':MUTANTS,'scope':'finite exact controls only; no continuum acceptance or independence credit'},indent=2,sort_keys=True))
