"""Exact finite first-contact and Gaussian-slicing illustrations.

Polyline controls are stricter than the smooth-arc theorem: a certified hit must
lie inside a single affine piece. This is not a numerical ODE or SARD-G verifier.
"""
from fractions import Fraction as F

MUTANT=None

def _data(path, section):
    pts=[tuple(F(v) for v in p) for p in path]
    lo,hi=map(F,section)
    if len(pts)<2 or any(len(p)!=3 for p in pts) or not lo<hi:
        raise ValueError('nondegenerate path and vertical section required')
    if pts[0][0]!=0 or any(p[0]>=q[0] for p,q in zip(pts,pts[1:])):
        raise ValueError('path times must start at zero and increase strictly')
    return pts,lo,hi

def closed_contacts(path,section):
    """All first-contact candidates with the CLOSED vertical segment x=0."""
    pts,lo,hi=_data(path,section);hits=[]
    for i,(p,q) in enumerate(zip(pts,pts[1:])):
        t0,x0,y0=p;t1,x1,y1=q
        if x1!=x0:
            u=-x0/(x1-x0)
            if 0<=u<=1 and lo<=y0+u*(y1-y0)<=hi:
                hits.append(dict(time=t0+u*(t1-t0),height=y0+u*(y1-y0),
                                 speed=(x1-x0)/(t1-t0),interior_piece=0<u<1,piece=i))
        elif x0==0:
            if y0==y1:
                u=F(0) if lo<=y0<=hi else None
            else:
                us=sorted(((lo-y0)/(y1-y0),(hi-y0)/(y1-y0)))
                left,right=max(F(0),us[0]),min(F(1),us[1])
                u=left if left<=right else None
            if u is not None:
                hits.append(dict(time=t0+u*(t1-t0),height=y0+u*(y1-y0),
                                 speed=F(0),interior_piece=False,piece=i))
    return sorted(hits,key=lambda h:(h['time'],h['speed']!=0))

def robust_hit(path,section,tube,margin=F(0)):
    pts,lo,hi=_data(path,section);margin=F(margin)
    if margin<0 or len(tube)!=4:
        raise ValueError('nonnegative strict margin and rectangle required')
    xmin,xmax,ymin,ymax=map(F,tube)
    if not xmin<0<xmax or not ymin<lo<hi<ymax:
        raise ValueError('closed section must lie in open tube')
    hits=closed_contacts(pts,(lo,hi))
    if MUTANT=='ignore-earlier-closed':
        hits=[h for h in hits if lo<h['height']<hi]
    if not hits:return False
    h=hits[0];tau=h['time'];height=h['height']
    if not tau>margin:return False
    if MUTANT!='allow-terminal' and not pts[-1][0]-tau>margin:return False
    endpoint_ok= min(height-lo,hi-height)>margin
    if MUTANT=='allow-endpoint':endpoint_ok=min(height-lo,hi-height)>=margin
    if not endpoint_ok:return False
    inside_piece=h['interior_piece']
    if MUTANT=='allow-terminal' and tau==pts[-1][0]:inside_piece=True
    if not inside_piece or not abs(h['speed'])>margin:return False
    prefix=[(p[1],p[2]) for p in pts if p[0]<tau]+[(F(0),height)]
    if MUTANT!='skip-tube':
        if not all(min(x-xmin,xmax-x,y-ymin,ymax-y)>margin for x,y in prefix):return False
    return True

def chart_hits(paths,section,tube):
    paths=list(paths)
    if not paths:raise ValueError('at least one declared hit required')
    if MUTANT=='skip-local':paths=paths[-1:]
    return all(robust_hit(p,section,tube) for p in paths)

def gradient_slack(minimum,eta):
    minimum,eta=F(minimum),F(eta)
    if eta<=0:raise ValueError('positive exclusion threshold required')
    return minimum>=eta if MUTANT=='nonstrict-gradient' else minimum>eta

def gaussian_split(Q,a):
    """Rational unstandardized form: xi=a.F, b=Qa/Var(xi), g=F-b xi."""
    a=list(map(F,a));Q=[list(map(F,row)) for row in Q];n=len(a)
    if n==0 or len(Q)!=n or any(len(row)!=n for row in Q):
        raise ValueError('matching square covariance and vector required')
    if any(Q[i][j]!=Q[j][i] for i in range(n) for j in range(n)):
        raise ValueError('symmetric covariance required')
    v=[sum((Q[i][j]*a[j] for j in range(n)),F(0)) for i in range(n)]
    var=sum((a[i]*v[i] for i in range(n)),F(0))
    if var<=0:raise ValueError('positive scalar variance required')
    b=[x/var for x in v]
    R=[[Q[i][j]-(0 if MUTANT=='leave-covariance' else v[i]*v[j]/var)
        for j in range(n)] for i in range(n)]
    return var,b,R

def rank(A):
    M=[list(map(F,row)) for row in A]
    if not M:return 0
    if any(len(row)!=len(M[0]) for row in M):raise ValueError('rectangular matrix required')
    k=0
    for j in range(len(M[0])):
        pivot=next((i for i in range(k,len(M)) if M[i][j]),None)
        if pivot is None:continue
        M[k],M[pivot]=M[pivot],M[k]
        z=M[k][j];M[k]=[v/z for v in M[k]]
        for i in range(k+1,len(M)):
            z=M[i][j];M[i]=[v-z*w for v,w in zip(M[i],M[k])]
        k+=1
        if k==len(M):break
    return k

def regular_zero(coefficients,x):
    coeff=list(map(F,coefficients));x=F(x)
    value=sum((a*x**i for i,a in enumerate(coeff)),F(0))
    deriv=sum((i*coeff[i]*x**(i-1) for i in range(1,len(coeff))),F(0))
    return value==0 and (True if MUTANT=='count-singular-zero' else deriv!=0)
