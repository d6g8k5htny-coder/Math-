"""Exact controls for the small-lifetime crossover in a limiting elder law.

Only the Python standard library is used. These identities and interval checks
are not a proof of the source Gaussian/elder interfaces or uniform field limits.
"""
import argparse
from fractions import Fraction as F
import json
from math import comb

MUTANTS=('all-doublets-finite','wrong-shape-normalization','retain-exponent13',
         'lose-ratio-jacobian','wrong-height-ratio','lose-moment-crossover')
_MUTANT=None


def rat(x):
    if type(x) not in (int,F): raise TypeError('exact int or Fraction required')
    return F(x)


def add(*polys):
    out={}
    for pol in polys:
        for ij,c in pol.items(): out[ij]=out.get(ij,F(0))+c
    return {ij:c for ij,c in out.items() if c}


def scale(pol,c): return {ij:a*c for ij,a in pol.items() if a*c}


def mul(a,b):
    out={}
    for (i,j),c in a.items():
        for (k,l),d in b.items(): out[i+k,j+l]=out.get((i+k,j+l),F(0))+c*d
    return {ij:c for ij,c in out.items() if c}


def power(pol,n):
    out={(0,0):F(1)}
    for _ in range(n): out=mul(out,pol)
    return out


def kernel_poly():
    # Coordinates are (e,x). This includes the original dv=6 de Jacobian.
    return scale(mul(mul({(1,0):F(1),(0,2):F(-1)},
                         {(1,0):F(1),(0,2):F(1),(0,1):F(2)}),
                     {(1,0):F(1),(1,1):F(2),(0,2):F(1)}),F(10368))


def kernel(e,x):
    e,x=rat(e),rat(x)
    return F(10368)*(e-x*x)*(e+x*x+2*x)*(e+2*e*x+x*x)


def shape_moment(j):
    """Exact unnormalized moment, integrating e first on two polynomial strips."""
    if type(j) is not int or not 0<=j<=8: raise ValueError('integer order 0..8 required')
    pol={(i+j,k):v for (i,k),v in kernel_poly().items()}
    total=F(0)
    for left,right,low in ((F(-1),F(0),{(0,1):F(-2),(0,2):F(-1)}),
                           (F(0),F(1,2),{(0,2):F(3),(0,3):F(2)})):
        integ={}
        for (i,k),v in pol.items():
            part=add({(0,0):F(1)},scale(power(low,i+1),-1))
            integ=add(integ,scale(mul({(0,k):F(1)},part),v/F(i+1)))
        total+=sum((v*(right**(k+1)-left**(k+1))/F(k+1)
                    for (i,k),v in integ.items()),F(0))
    if _MUTANT=='wrong-shape-normalization': total/=6
    return total


def in_support(e,x):
    e,x=rat(e),rat(x)
    return (0<e<1 and -1<x<F(1,2) and e>-2*x-x*x
            and (x<=0 or e>3*x*x+2*x**3))


def doublet(e,x):
    if not in_support(e,x): raise ValueError('point outside strict elder shape')
    if _MUTANT=='all-doublets-finite': return True
    return x>0 and 2*x**3+3*e*x*x-e*e>0


def companion(e,x):
    """Other exact cubic root in (e_comp,x_comp,Z_comp/Z); not necessarily counted."""
    e,x=rat(e),rat(x)
    u=-F(1,2)-x;v=6*(e+x);b=3-12*u*u
    den=4*v*v-8*b*u*v+b*b
    if den==0: return None
    t=(4*v*v-b*b)/den
    uc=(2*b*v-u*(4*v*v+b*b))/den;vc=v*t*t
    return uc+F(1,2)+vc/6,-uc-F(1,2),t


def scaled_phi(delta,w):
    delta,w=rat(delta),rat(w)
    return (1-w*w)*(2*w+delta*(1+w*w))*(1+w*w+2*delta*w)


def w_density(w):
    w=rat(w)
    if not (w>0 and 3*w*w<1): return F(0)
    return F(81,13)*w*(1-w**4)


def limit_w_even_moment(j):
    if type(j) is not int or j<0: raise ValueError('nonnegative integer required')
    return F(81,13)*(F(1,3**(j+1)*(2*j+2))-F(1,3**(j+3)*(2*j+6)))


def w_to_ratio(w):
    w=rat(w)
    if not (w>0 and 3*w*w<1): raise ValueError('0<w<1/sqrt(3) required')
    return (1-w*w)/(2*w*w)


def ratio_density(v):
    v=rat(v)
    if v<=1:return F(0)
    q=2*v+1
    ans=F(81,13)*(1/q**2-1/q**4)
    return ans*q if _MUTANT=='lose-ratio-jacobian' else ans


def ratio_survival(t):
    t=rat(t)
    if t<1:raise ValueError('threshold at least one required')
    if _MUTANT=='retain-exponent13':return t**-13
    q=2*t+1
    return F(81,26)/q-F(27,26)/q**3


def rho_density(r):
    r=rat(r)
    if not 0<r<1:return F(0)
    return F(324,13)*(1+r)/(2+r)**4


def height_ratio(v):
    v=rat(v)
    if v<1:raise ValueError('companion ratio at least one required')
    return v**3 if _MUTANT=='wrong-height-ratio' else v**3*(v+2)/(2*v+1)


def exact_scaled_companion(delta,w):
    """Return positive radius ratio and companion/elder height ratio on a doublet."""
    delta,w=rat(delta),rat(w)
    e,x=delta*delta,delta*w
    if not doublet(e,x):raise ValueError('counted doublet required')
    den=4*w**3+delta*(3*w**4+6*w*w-1)+4*delta*delta*w**3
    V=(1-w*w)*(2*w+delta*(1+w*w))/den
    H=(1-w*w)**3*(1+3*w*w+delta*(6*w+2*w**3)+delta*delta*(1+3*w*w))/den**2
    return V,H


def square_density(r,z):
    """Unnormalized doublet shape density; total is D, not E0."""
    r,z=rat(r),rat(z)
    return F(165888)*r**12*z**7*(1+z)**4*(1+r*z)**4*(1+r*z+r)**7/((1+r)**5*(1+2*r*z+r)**9)


def square_lifetime(r,z):
    r,z=rat(r),rat(z)
    return r**3*z*z*(z+1)*(r*z+r+2)/((r+1)*(2*r*z+r+1))


def moment_blowup_constant(p):
    """Exact constants at p=4,7,10; the general real-p integral is in PROOF.md."""
    if p not in (4,7,10) or type(p) is not int:raise ValueError('exact cases: p=4,7,10')
    j=(p-1)//3
    integ=sum((F(comb(j,k),2*j+k) for k in range(j+1)),F(0))
    ans=F(2592,13*(13-p))*F(1,2**((13-p)//3))*integ
    return ans*3 if _MUTANT=='lose-moment-crossover' else ans


def isolate(target,func,left,right,bits=100):
    if type(bits) is not int or not 16<=bits<=256:raise ValueError('bits16..256 required')
    for _ in range(bits):
        mid=(left+right)/2;f=func(mid)
        if f==target:return mid,mid
        if f<target:left=mid
        else:right=mid
    return left,right


def iadd(a,b):return a[0]+b[0],a[1]+b[1]

def imul(a,b):
    z=[x*y for x in a for y in b];return min(z),max(z)

def ipoly(poly,x):
    out=(F(0),F(0))
    for i in range(max(poly),-1,-1):
        c=poly.get(i,F(0));out=iadd(imul(out,x),(c,c))
    return out


def density_intervals(e,bits=100):
    """Rational enclosures of total and singleton lifetime-density numerators."""
    e=rat(e)
    if not 0<e<1:raise ValueError('strict lifetime e in(0,1) required')
    sq=isolate(1-e,lambda x:x*x,F(0),F(1),bits)
    low=(sq[0]-1,sq[1]-1)
    high=isolate(e,lambda x:3*x*x+2*x**3,F(0),F(1,2),bits)
    split=isolate(e*e,lambda x:2*x**3+3*e*x*x,F(0),F(1,2),bits)
    poly={}
    for (i,j),v in kernel_poly().items():poly[j+1]=poly.get(j+1,F(0))+v*e**i/F(j+1)
    A=ipoly(poly,low);B=ipoly(poly,high);C=ipoly(poly,split)
    return {'total':(max(F(0),B[0]-A[1]),B[1]-A[0]),
            'singleton':(max(F(0),C[0]-A[1]),C[1]-A[0])}


def checks():
    if shape_moment(0)!=F(888807,280):raise ValueError('source density normalization')
    if doublet(F(1,100),F(0)):raise ValueError('finite cutoff has singleton mass')
    if ratio_survival(2)!=F(999,1625):raise ValueError('small-lifetime ratio tail, not exponent13')
    v=w_to_ratio(F(1,3))
    if w_density(F(1,3))!=ratio_density(v)/F(1,3)**3:raise ValueError('ratio Jacobian')
    if height_ratio(2)!=F(32,5):raise ValueError('companion height map')
    if moment_blowup_constant(4)!=F(30,13):raise ValueError('singular moment coefficient')
    cases=0
    for ne in range(1,30):
        e=F(ne,30)
        for nx in range(-29,15):
            x=F(nx,30)
            if not in_support(e,x):continue
            pair=companion(e,x)
            counted=pair is not None and 0<pair[0]<1
            if doublet(e,x)!=counted:raise ValueError('companion boundary disagreement')
            if counted and pair[0]!=e and not pair[0]>e:raise ValueError('elder height ordering')
            cases+=1
    return cases


def result():
    cases=checks()
    return {'passed':True,'scientific_effect':'NONE','mathematical_acceptance':False,
            'scope':'finite algebra and interval checks only',
            'rational_classifier_cases':cases,
            'source_shape_moments':{str(j):str(shape_moment(j)) for j in range(3)},
            'small_lifetime_y_density':'4 y^3 on (0,1)',
            'small_lifetime_w_density':'(81/13) w (1-w^4) on (0,1/sqrt(3))',
            'singleton_probability_coefficient':'(486/169)*2^(-2/3)',
            'singleton_probability_exponent':'1/3',
            'limiting_companion_tail_coefficient':str(F(81,52)),
            'limiting_companion_moment_threshold':1,
            'finite_epsilon_companion_moment_threshold':13,
            'critical_mean_log_coefficient':str(F(27,52)),
            'moment_blowup_constants':{str(p):str(moment_blowup_constant(p)) for p in (4,7,10)}}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--mutant',choices=MUTANTS)
    args=parser.parse_args();global _MUTANT;_MUTANT=args.mutant
    try:data=result()
    except ValueError as exc:
        print(json.dumps({'passed':False,'error':str(exc)},sort_keys=True));raise SystemExit(1)
    print(json.dumps(data,sort_keys=True,indent=2))

if __name__=='__main__':main()
