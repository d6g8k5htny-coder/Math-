"""Exact controls for elder-selected microscopic extreme laws.

Standard library only. This is finite algebra and interval arithmetic, not a
proof of the actual Gaussian elder-selector interface or the limiting theorem.
"""
import argparse
from fractions import Fraction as F
import json
from math import comb

MUTANTS=('choose-outer','count-both','drop-half','wrong-lifetime-sign',
         'forget-radius-bias','wrong-height-power')
_MUTANT=None


def rational(x):
    if type(x) not in (int,F): raise TypeError('exact int/Fraction required')
    return F(x)


def b0(u): return 3-12*u*u

def height(u,v): return u+F(1,2)+v/6

def shape(u,v):
    return -F(3,2)<u<F(1,2) and abs(b0(u))/2<v<3-6*u

def weight(u,v):
    b=b0(u)
    return (4*v*v-b*b)*(b-4*u*v)


def companion(u,v):
    u,v=map(rational,(u,v));b=b0(u)
    den=4*v*v-8*b*u*v+b*b
    if den==0:return None
    ratio=(4*v*v-b*b)/den
    return ((2*b*v-u*(4*v*v+b*b))/den,v*ratio**2,ratio)


def outer(u,v):
    p=-u;a=12*p*p-3
    return (F(1,2)<p<1 and a/2<v<a*p) or (1<=p<F(3,2) and a/2<v<3+6*p)


def selection(u,v):
    """Select minimum downward height, not maximum radius; ties get half."""
    u,v=map(rational,(u,v))
    if not shape(u,v):raise ValueError('strict shape point required')
    pair=companion(u,v)
    if pair is None or not shape(pair[0],pair[1]):return F(1)
    if _MUTANT=='count-both':return F(1)
    eta,eta_c=height(u,v),height(pair[0],pair[1])
    if _MUTANT=='wrong-lifetime-sign':eta,eta_c=-eta,-eta_c
    if eta==eta_c:return F(1) if _MUTANT=='drop-half' else F(1,2)
    answer=int(eta<eta_c)
    return F(1-answer if _MUTANT=='choose-outer' else answer)


# Exact two-variable polynomials, indexed by powers of the first variable and v.
def add(*polys):
    out={}
    for pol in polys:
        for ij,c in pol.items():out[ij]=out.get(ij,F(0))+c
    return {ij:c for ij,c in out.items() if c}

def scale(pol,a):return {ij:c*a for ij,c in pol.items() if c*a}

def multiply(left,right):
    out={}
    for (i,j),c in left.items():
        for (k,l),d in right.items():out[i+k,j+l]=out.get((i+k,j+l),F(0))+c*d
    return {ij:c for ij,c in out.items() if c}

def power(pol,n):
    out={(0,0):F(1)}
    for _ in range(n):out=multiply(out,pol)
    return out

def strip(pol,left,right,low,high):
    """Integral in first coordinate, then between polynomial v bounds."""
    total={}
    for (i,j),c in pol.items():
        bounds=add(power(high,j+1),scale(power(low,j+1),-1))
        total=add(total,scale(multiply({(i,0):F(1)},bounds),c/F(j+1)))
    if any(j for i,j in total):raise ValueError('bounds must be univariate')
    return sum((c*(right**(i+1)-left**(i+1))/F(i+1) for (i,j),c in total.items()),F(0))


def integrand(n):
    if type(n) is not int or not 0<=n<=8:raise ValueError('integer moment order 0..8 required')
    b={(0,0):F(3),(2,0):F(-12)};v={(0,1):F(1)};u={(1,0):F(1)}
    q=multiply(add(scale(power(v,2),4),scale(power(b,2),-1)),add(b,scale(multiply(u,v),-4)))
    eta={(1,0):F(1),(0,0):F(1,2),(0,1):F(1,6)}
    return multiply(q,power(eta,n))


def point_moment(n):
    poly=integrand(n);b={(0,0):F(3),(2,0):F(-12)};hi={(0,0):F(3),(1,0):F(-6)}
    return (strip(poly,F(-3,2),F(-1,2),scale(b,F(-1,2)),hi)+
            strip(poly,F(-1,2),F(1,2),scale(b,F(1,2)),hi))


def outer_moment(n):
    poly={(i,j):c*(-1)**i for (i,j),c in integrand(n).items()}
    a={(2,0):F(12),(0,0):F(-3)};p={(1,0):F(1)};hi={(0,0):F(3),(1,0):F(6)}
    return (strip(poly,F(1,2),F(1),scale(a,F(1,2)),multiply(a,p))+
            strip(poly,F(1),F(3,2),scale(a,F(1,2)),hi))


def moment(n):return point_moment(n)-outer_moment(n)


def small_height_density_coefficient():
    # eta^-3 H(eta) -> 10368 int_0^(1/sqrt(3)) 2z(1-z^4) dz.
    return F(0) if _MUTANT=='wrong-height-power' else F(10368)*(F(1,3)-F(1,81))


def outer_over_elder_tail_exponent():
    return 2 if _MUTANT=='forget-radius-bias' else 1+11+1


def imul(a,b):
    vals=[x*y for x in a for y in b]
    return min(vals),max(vals)

def iadd(a,b):return a[0]+b[0],a[1]+b[1]

def ipoly(coefs,x):
    ans=(F(0),F(0))
    for j in range(max(coefs),-1,-1):
        c=coefs.get(j,F(0));ans=iadd(imul(ans,x),(c,c))
    return ans


def _isolate(target,func,left,right,bits):
    for _ in range(bits):
        mid=(left+right)/2;value=func(mid)
        if value==target:return mid,mid
        if value<target:left=mid
        else:right=mid
    return left,right


def height_density_bounds(e,bits=100):
    """Rigorous rational interval for the normalized limiting density at e.

    Bounds use root isolation and interval evaluation of a polynomial primitive;
    no floating quadrature or transcendental library is needed.
    """
    e=rational(e)
    if not 0<=e<=1:raise ValueError('height fraction must be in [0,1]')
    if type(bits) is not int or not 8<=bits<=256:raise ValueError('bits must lie in 8..256')
    if e==0:return F(0),F(0)
    if e==1:
        val=F(98415,7)/moment(0);return val,val
    sq=_isolate(1-e,lambda z:z*z,F(0),F(1),bits)
    lower=(sq[0]-1,sq[1]-1)
    upper=_isolate(e,lambda z:3*z*z+2*z**3,F(0),F(1,2),bits)
    pol={(0,0):F(10368)}
    for factor in ({(0,0):e,(2,0):F(-1)},
                   {(0,0):e,(2,0):F(1),(1,0):F(2)},
                   {(0,0):e,(1,0):2*e,(2,0):F(1)}):pol=multiply(pol,factor)
    primitive={i+1:c/F(i+1) for (i,j),c in pol.items()}
    at_hi,at_lo=ipoly(primitive,upper),ipoly(primitive,lower)
    mass=moment(0)
    return max(F(0),(at_hi[0]-at_lo[1])/mass),(at_hi[1]-at_lo[0])/mass


def square_density(r,z):
    r,z=map(rational,(r,z))
    if not (0<r<1 and 0<z<1):raise ValueError('open square required')
    base=165888*r*z**7*(z+1)**4*(r*z+1)**4*(r*z+r+1)**7/((r+1)**5*(2*r*z+r+1)**9)
    return base if _MUTANT=='forget-radius-bias' else r**11*base


def square_heights(r,z):
    r,z=map(rational,(r,z));den=(r+1)*(2*r*z+r+1)
    return (r**3*z*z*(z+1)*(r*z+r+2)/den,
            z*z*(r*z+1)*(r*z+2*r+1)/den)


def log2_bounds(n=70):
    lo=2*sum((F(1,3**(2*j+1)*(2*j+1)) for j in range(n)),F(0))
    return lo,lo+2*F(1,3**(2*n+1))/((2*n+1)*(1-F(1,9)))


def constants():
    ell=log2_bounds();a=F(27066286003,223205220);b=-F(79298560,4782969)
    d=(a+b*ell[1],a+b*ell[0]);I=point_moment(0);E=moment(0);H0=F(6401,3960)
    return {'elder_to_point_tail_ratio':(E/I,E/I),
            'double_given_extreme_elder':(d[0]/E,d[1]/E),
            'elder_to_maximum_tail_ratio':(E/(I-d[0]),E/(I-d[1])),
            'outer_over_elder_ratio_tail_constant':(165888*H0/(13*d[1]),165888*H0/(13*d[0])),
            'mean_lifetime_fraction':(moment(1)/E,moment(1)/E),
            'second_lifetime_fraction_moment':(moment(2)/E,moment(2)/E)}


def decimal_interval(iv,digits=18):
    unit=10**digits;out=[]
    for i,val in enumerate(iv):
        q=val*unit;n=q.numerator//q.denominator if i==0 else -((-q.numerator)//q.denominator)
        sign='-' if n<0 else '';n=abs(n);out.append(f'{sign}{n//unit}.{n%unit:0{digits}d}')
    return dict(lower=out[0],upper=out[1])


def checks():
    if selection(F(-1),F(6))!=0:raise ValueError('elder is the higher, not outer saddle')
    if selection(F(-13,23),F(294,529))!=1:raise ValueError('inner partner selection')
    if selection(F(-3,4),F(45,16))!=F(1,2):raise ValueError('tie multiplicity')
    if moment(0)!=F(888807,280):raise ValueError('selected root mass')
    if small_height_density_coefficient()!=3328:raise ValueError('fourth-power small-lifetime law')
    if outer_over_elder_tail_exponent()!=13:raise ValueError('elder radius bias exponent')
    n=0
    for i in range(-35,12):
        u=F(i,24);lo,hi=abs(b0(u))/2,3-6*u
        if lo>=hi:continue
        for j in range(1,20):
            v=lo+(hi-lo)*F(j,20);sel=selection(u,v);pair=companion(u,v)
            if pair and shape(pair[0],pair[1]):
                if sel+selection(pair[0],pair[1])!=1:raise ValueError('one partner per configuration')
                if sel in (0,1) and sel!=1-int(outer(u,v)):raise ValueError('height/strip selector mismatch')
            elif sel!=1:raise ValueError('singleton must select its one root')
            n+=1
    return n


def result():
    n=checks()
    return {'scientific_effect':'NONE','mathematical_acceptance':False,
            'scope':'finite algebra, not validation of Gaussian or elder premises',
            'rational_shape_cases':n,
            'selected_shape_moments':{str(j):str(moment(j)) for j in range(3)},
            'small_lifetime_cdf_coefficient':str(F(832)/moment(0)),
            'inverse_lifetime_moment_threshold':4,
            'companion_over_elder_moment_threshold':13,
            'constants':{key:decimal_interval(val) for key,val in constants().items()},
            'height_density_values':{str(e):decimal_interval(height_density_bounds(e)) for e in (F(1,100),F(1,4),F(1,2),F(3,4),F(99,100))}}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--mutant',choices=MUTANTS);args=parser.parse_args()
    global _MUTANT
    _MUTANT=args.mutant
    try:ans=result()
    except ValueError as exc:
        print(json.dumps({'passed':False,'error':str(exc)},sort_keys=True));raise SystemExit(1)
    print(json.dumps(ans,indent=2,sort_keys=True))

if __name__=='__main__':main()
