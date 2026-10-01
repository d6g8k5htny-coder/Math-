"""Exact finite controls for the birth-marginalized c2 representation.

This is not a continuum proof checker or a finite-L numerical enclosure. Only
integers/Fractions are used. A polynomial is a list of coefficients in increasing
order; matrices in det/adj have polynomial entries. No external package is used.
"""
from fractions import Fraction as F
from itertools import permutations
from functools import lru_cache
import json


def exact(x):
    if type(x) not in (int,F):raise TypeError('exact int or Fraction required')
    return F(x)


def trim(p):
    p=list(map(exact,p))
    while len(p)>1 and p[-1]==0:p.pop()
    return p or [F(0)]


def coef(p,n):return p[n] if n<len(p) else F(0)


def add(*ps):
    out=[F(0)]*max((len(p) for p in ps),default=1)
    for p in ps:
        for j,x in enumerate(p):out[j]+=exact(x)
    return trim(out)


def scale(p,x):return trim([exact(x)*exact(y) for y in p])


def mul(p,q):
    out=[F(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]+=exact(x)*exact(y)
    return trim(out)


def det(a):
    n=len(a)
    if any(len(row)!=n for row in a):raise ValueError('square matrix required')
    ans=[F(0)]
    for perm in permutations(range(n)):
        parity=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        term=[F((-1)**parity)]
        for i,j in enumerate(perm):term=mul(term,a[i][j])
        ans=add(ans,term)
    return ans


def adj(a):
    n=len(a)
    return [[scale(det([[a[ii][jj] for jj in range(n) if jj!=i]
                        for ii in range(n) if ii!=j]),(-1)**(i+j))
             for j in range(n)] for i in range(n)]


def det_data(a,b,cc):
    m=len(a)
    for matrix in (a,b,cc):
        if len(matrix)!=m or any(len(row)!=m for row in matrix):raise ValueError('matrix size mismatch')
    ab=[[[exact(a[i][j]),exact(b[i][j])] for j in range(m)] for i in range(m)]
    ac=[[[exact(a[i][j]),exact(cc[i][j])] for j in range(m)] for i in range(m)]
    db=det(ab);dc=det(ac)
    return coef(db,0),coef(db,1),coef(dc,1),2*coef(db,2),[[coef(v,1) for v in row] for row in adj(ab)]


def bilinear(x,a,y):
    return sum((exact(x[i])*exact(a[i][j])*exact(y[j])
                for i in range(len(x)) for j in range(len(y))),F(0))


def weight2(a,b,cc,g,h,f4,f5,k):
    f4,f5,k=map(exact,(f4,f5,k))
    D,DB,DC,DBB,JB=det_data(a,b,cc)
    J=[[coef(v,0) for v in row] for row in adj([[[exact(x)] for x in row] for row in a])]
    y=f4*D/12-bilinear(g,J,g)/4
    common=y+3*k*DB
    second=3*k*(DC+DBB)/4+f4*DB/24+f5*D/120-bilinear(g,J,h)/12-bilinear(g,JB,g)/8
    return 12*k*D*second-common*common


def endpoint_product(a,b,cc,g,h,f4,f5,k):
    """Independent full-Hessian determinant of an exactly pinned polynomial."""
    m=len(a);ds=[]
    f4,f5,k=map(exact,(f4,f5,k))
    for sign in (-1,1):
        H=[[[F(0)] for _ in range(m+1)] for _ in range(m+1)]
        H[0][0]=[F(0),sign*6*k,f4/12,sign*f5/120]
        for i in range(m):
            H[0][i+1]=H[i+1][0]=[F(0),sign*exact(g[i])/2,exact(h[i])/12]
            for j in range(m):
                H[i+1][j+1]=[exact(a[i][j]),sign*exact(b[i][j])/2,exact(cc[i][j])/8]
        p=det(H)
        if coef(p,0)!=0:raise ArithmeticError('pin division not exact')
        ds.append(p[1:] or [F(0)])
    return scale(mul(ds[0],ds[1]),-1)


def inverse(a):
    n=len(a)
    if any(len(row)!=n for row in a):raise ValueError('square matrix required')
    b=[[exact(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        p=next((i for i in range(j,n) if b[i][j]),None)
        if p is None:raise ValueError('singular matrix')
        b[j],b[p]=b[p],b[j];v=b[j][j];b[j]=[x/v for x in b[j]]
        for i in range(n):
            if i!=j:
                v=b[i][j];b[i]=[x-v*y for x,y in zip(b[i],b[j])]
    return [row[n:] for row in b]


def jet_cov(a,b,q):
    """Derivative covariance for exp(-x^T q x/2), rejecting unused order ten."""
    if len(a)!=len(q) or len(b)!=len(q):raise ValueError('dimension mismatch')
    n=sum(a)+sum(b)
    if n>8:raise ValueError('order above eight is not part of the coefficient')
    if n%2:return F(0)
    indices=tuple(i for i in range(len(a)) for _ in range(a[i]+b[i]))
    @lru_cache(None)
    def moment(ix):
        if not ix:return F(1)
        first=ix[0]
        return sum((exact(q[first][ix[j]])*moment(ix[1:j]+ix[j+1:])
                    for j in range(1,len(ix))),F(0))
    return (-1)**(sum(b)+n//2)*moment(indices)


def blocks(d,q):
    def mi(*axes):
        out=[0]*d
        for axis in axes:out[axis]+=1
        return tuple(out)
    odd=[mi(i) for i in range(d)]+[mi(0,0,0)]
    odd2=[(mi(i,0,0),F(1,8)) for i in range(d)]+[(mi(0,0,0,0,0),F(1,40))]
    even=[mi(0,i) for i in range(d)]+[mi(i,j) for i in range(1,d) for j in range(i,d)]
    even2=[(mi(0,i,0,0),F(1,24)) for i in range(d)]+[(x,F(0)) for x in even[d:]]
    seen=[]
    def cov(a,b):
        seen.append(sum(a)+sum(b));return jet_cov(a,b,q)
    def pair(z,z2):
        c0=[[cov(a,b) for b in z] for a in z]
        c2=[]
        for i,a in enumerate(z):
            row=[]
            for j,b in enumerate(z):
                ai,wa=z2[i];bj,wb=z2[j]
                row.append((wa*cov(ai,b) if wa else F(0))+(wb*cov(a,bj) if wb else F(0)))
            c2.append(row)
        return c0,c2
    so,so2=pair(odd,odd2);ce,ce2=pair(even,even2)
    parity=all(cov(a,b)==0 for a in odd for b in even)
    return {'odd0':so,'odd2':so2,'even0':ce,'even2':ce2,
            'parity_zero':parity,'maximum_order':max(seen)}


def d1(moments):
    """Unnormalized polynomial and pin normalization in the one-dimensional case."""
    if len(moments)!=4:raise ValueError('moments m2,m4,m6,m8 required')
    m2,m4,m6,m8=map(exact,moments)
    detso=m2*m6-m4*m4
    if m2<=0 or m4<=0 or detso<=0 or m8-m6*m6/m4<0:raise ValueError('invalid covariance data')
    so=[[m2,-m4],[-m4,m6]]
    so2=[[-m4/4,3*m6/20],[3*m6/20,-m8/20]]
    si=inverse(so)
    score0=-sum((si[i][j]*so2[j][i] for i,j in product2(2)),F(0))/2+m6/(24*m4)
    score2=72*sum((si[1][i]*so2[i][j]*si[j][1] for i,j in product2(2)),F(0))
    mean5=12*(m6*si[0][1]-m8*si[1][1])
    p=[-(m8-m6*m6/m4)/144,mean5/10+36*score0,36*score2]
    return {'a':72*si[1][1],'p':p,'den2':detso*m4}


def product2(n):return ((i,j) for i in range(n) for j in range(n))


def mellin_factor(a,p):
    a=exact(a)
    if a<=0 or len(p)!=3:raise ValueError('positive rate and three polynomial coefficients required')
    p0,p2,p4=map(exact,p)
    return -3*p0+p2/(2*a)+5*p4/(12*a*a)


def cubature():return [(F(-3),F(1,72)),(F(-1),F(3,8)),(F(0),F(2,9)),(F(1),F(3,8)),(F(3),F(1,72))]


REFERENCE_C2={
    '1':('0.2300445802661503','0.2300445802661998'),
    '2':('0.2215244106266632','0.2215244106267110'),
    '3':('0.1612340491269447','0.1612340491269810'),
}


def exp_partial(t,n):
    t=exact(t)
    if t<0 or type(n) is not int or n<0:raise ValueError('nonnegative argument and integer order required')
    term=out=F(1)
    for j in range(1,n+1):
        term*=t/j;out+=term
    return out


def image_polynomial(d,L):
    L=exact(L)
    if type(d) is not int or d not in (1,2,3) or L<10:raise ValueError('d=1,2,3 and L>=10 required')
    return 2*(3**d-1)*(d**4*L**8+28*d**3*L**6+210*d*d*L**4+420*d*L**2+210)


def bound_budget():
    return {
        'weight_l1':F(151,6)**2+48*F(781,60),
        'moment8_integral':6*128*(1+105*318**4),
        'H_bound':2000*10*20000**4+36*4*4*10**6*5,
        'H_derivative_bound':2000*4000*20000**4+36*4*4*10**8*5,
        'p_bound':12*9*10**23*10**15,
        'p_derivative_bound':12*(10**3*10**23+9*10**26+9*100*10**23)*10**15,
        'final_bound':16*(12*10**44+11*10**4*10**41),
    }


def decimal_exact(x,places):
    x=exact(x);z=x*10**places
    if z.denominator!=1:raise ValueError('requested exact decimal is not terminating at this precision')
    v=z.numerator;return ('-' if v<0 else '')+str(abs(v)//10**places)+'.'+str(abs(v)%10**places).zfill(places)


def results():
    out=d1((1,3,15,105))
    enclosures={}
    for d in ('1','2','3'):
        lo,hi=map(F,REFERENCE_C2[d]);bound=F(10**50)*image_polynomial(int(d),F(24))/10**125
        if bound>=F(1,10**60):raise ArithmeticError('SIDE24 error bound failed')
        enclosures[d]={'additive_error_upper_rational':str(bound),
            'reference_interval':list(REFERENCE_C2[d]),
            'torus_L_at_least_24_outward_interval':[
                decimal_exact(lo-F(1,10**16),16),decimal_exact(hi+F(1,10**16),16)]}
    return {'scientific_effect':'NONE','status':'author-side proof candidate; nonauthor review required',
            'scope':'signed fixed-cone c2 functional; actual persistence identification is an imported premise',
            'reference_d1':{'a':str(out['a']),'polynomial':[str(x) for x in out['p']],
                            'pin_determinant_product':str(out['den2']),
                            'Mellin_factor':str(mellin_factor(out['a'],out['p'])),
                            'c2_over_12pow1over6_Gamma5over6_pi_minus3over2':'3/4'},
            'maximum_covariance_derivative_order':8,
            'Lipschitz_constant_upper':'1e50','jet_box_radius':'1e-4',
            'SIDE24_uniform_additive_error_upper':'1e-60',
            'budget':{k:str(v) for k,v in bound_budget().items()},
            'torus_expression_enclosures':enclosures,
            'actual_elder_identification_proved_here':False,
            'finite_lifetime_remainder_bound_proved_here':False}

if __name__=='__main__':print(json.dumps(results(),indent=2,sort_keys=True))
