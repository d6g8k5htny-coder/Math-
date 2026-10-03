"""Exact controls for the extreme whole-cluster candidate; standard library only.

The rational identities and integral certificates are executable. Gaussian
conditioning, changes of variables and weak limits are analytic obligations,
not conclusions that this program certifies.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
from math import comb
from typing import Optional

Poly = dict[int, F]
AffineLog = tuple[F, F]  # a + b log(2)
Interval = tuple[F, F]
MUTANTS = ('drop-companion-sign', 'point-is-cluster', 'close-window',
           'drop-log2', 'double-count-inner', 'lose-height-jacobian',
           'wrong-tail-power', 'uniform-cluster-from-point')
_MUTANT: Optional[str] = None


def _r(x: F | int) -> F:
    if isinstance(x, bool) or not isinstance(x, (F, int)):
        raise TypeError('an integer or Fraction is required')
    return F(x)


def b0(u: F | int) -> F:
    u = _r(u)
    return 3 - 12*u*u


def height(u: F | int, v: F | int) -> F:
    return _r(u) + F(1, 2) + _r(v)/6


def in_shape(u: F | int, v: F | int) -> bool:
    u, v = _r(u), _r(v)
    if _MUTANT == 'close-window':
        return -F(3,2) <= u <= F(1,2) and abs(b0(u))/2 <= v <= 3-6*u
    return -F(3,2) < u < F(1,2) and abs(b0(u))/2 < v < 3-6*u


def shape_weight(u: F | int, v: F | int) -> F:
    u, v = _r(u), _r(v)
    b = b0(u)
    return (4*v*v-b*b)*(b-4*u*v)


def companion(u: F | int, v: F | int) -> Optional[tuple[F, F, F]]:
    """Other root's (u',v',Z'/Z); None is the linear degree-drop case.

    This algebraic map is defined even outside the strict shape region;
    membership must be checked separately. It is not a field root solver.
    """
    u, v = _r(u), _r(v)
    b = b0(u)
    den = 4*v*v - 8*b*u*v + b*b
    if den == 0:
        return None
    t = (4*v*v-b*b)/den
    up = (2*b*v-u*(4*v*v+b*b))/den
    vp = v*t*t
    if _MUTANT == 'drop-companion-sign':
        t = abs(t)
    return up, vp, t


def is_double(u: F | int, v: F | int) -> bool:
    if not in_shape(u,v):
        return False
    c = companion(u,v)
    return c is not None and in_shape(c[0], c[1])


def classifier_double(u: F | int, v: F | int) -> bool:
    """Independent CUB threshold read on an already counted root."""
    u, v = _r(u), _r(v)
    b = b0(u)
    return in_shape(u,v) and v < -b and 12*(v-b*u)**2 < (v+b)**2*(2*v-b)


def anchor_weight(u: F | int, v: F | int) -> F:
    """Asymptotic |Z|-maximum selector; ties have weight one half."""
    if not in_shape(u,v):
        raise ValueError('strictly typed in-window root required')
    if _MUTANT == 'point-is-cluster':
        return F(1)
    c = companion(u,v)
    if c is None or not in_shape(c[0], c[1]):
        return F(1)
    ratio = abs(c[2])
    return F(1) if ratio < 1 else F(1,2) if ratio == 1 else F(0)


def inner_double(u: F | int, v: F | int) -> bool:
    """Polynomial description; strict boundary, no square-root comparison."""
    u, v = _r(u), _r(v)
    p = -u
    a = 12*p*p-3
    f = -2*v*v+(36*p*p-12*p-3)*v-72*p**3+36*p*p+18*p-9
    return in_shape(u,v) and F(1,2)<p<1 and a*p<v and f>0


def outer_double(u: F | int, v: F | int) -> bool:
    u, v = _r(u), _r(v)
    p = -u
    a = 12*p*p-3
    return ((F(1,2)<p<1 and a/2<v<a*p) or
            (1<=p<F(3,2) and a/2<v<3+6*p))


# Sparse Laurent arithmetic. Exponents can be negative; powers are nonnegative.
def add(*polys: Poly) -> Poly:
    out: Poly = {}
    for poly in polys:
        for k, value in poly.items():
            out[k] = out.get(k,F(0)) + value
    return {k:v for k,v in out.items() if v}


def scale(poly: Poly, c: F | int) -> Poly:
    c = _r(c)
    return {k:v*c for k,v in poly.items() if v*c}


def multiply(left: Poly, right: Poly) -> Poly:
    out: Poly = {}
    for i,x in left.items():
        for j,y in right.items():
            out[i+j] = out.get(i+j,F(0)) + x*y
    return {k:v for k,v in out.items() if v}


def power(poly: Poly, n: int) -> Poly:
    if isinstance(n,bool) or not isinstance(n,int) or n<0:
        raise ValueError('nonnegative integer power required')
    result: Poly = {0:F(1)}
    base = dict(poly)
    while n:
        if n & 1:
            result = multiply(result,base)
        base = multiply(base,base)
        n //= 2
    return result


def evaluate(poly: Poly, x: F | int) -> F:
    x = _r(x)
    return sum((v*x**k for k,v in poly.items()),F(0))


def integrate_polynomial(poly: Poly, left: F, right: F) -> F:
    if any(k<0 for k in poly):
        raise ValueError('ordinary polynomial required')
    return sum((v*(right**(k+1)-left**(k+1))/F(k+1)
                for k,v in poly.items()),F(0))


def _moment_gap(u: Poly, b: Poly, hi: Poly, lo: Poly, j: int) -> Poly:
    """Integrate Q(u,v)*(u+1/2+v/6)^j in v between polynomial bounds."""
    if isinstance(j,bool) or not isinstance(j,int) or not 0<=j<=12:
        raise ValueError('moment order must be an integer between 0 and 12')
    q = {3:scale(u,-16), 2:scale(b,4),
         1:scale(multiply(u,power(b,2)),4), 0:scale(power(b,3),-1)}
    bias = add(u,{0:F(1,2)})
    total: Poly = {}
    for ell in range(j+1):
        eta = scale(power(bias,j-ell),F(comb(j,ell),6**ell))
        for order, coef in q.items():
            n = order+ell+1
            gap = add(power(hi,n),scale(power(lo,n),-1))
            total = add(total,scale(multiply(multiply(eta,coef),gap),F(1,n)))
    return total


def point_moment(j: int) -> F:
    u: Poly = {1:F(1)}
    b = add({0:F(3)},scale(power(u,2),-12))
    hi = add({0:F(3)},scale(u,-6))
    value = F(0)
    for left,right,sgn in ((F(-3,2),F(-1,2),-1),(F(-1,2),F(1,2),1)):
        poly = _moment_gap(u,b,hi,scale(b,F(sgn,2)),j)
        value += integrate_polynomial(poly,left,right)
    return value/6 if _MUTANT=='lose-height-jacobian' else value


def inner_certificate(j: int) -> Poly:
    """Laurent integrand on y in [1/4,1], after rationalizing V_+(p)."""
    p: Poly = {-1:F(2,9), 0:F(1,18), 1:F(2,9)}
    a = add(scale(power(p,2),12),{0:F(-3)})
    hi: Poly = {-2:F(8,9), -1:F(-4,3), 1:F(4,9)}
    lo = multiply(a,p)
    gap = _moment_gap(scale(p,-1),scale(a,-1),hi,lo,j)
    return multiply(gap,{-2:F(2,9),0:F(-2,9)})


def inner_moment(j: int) -> AffineLog:
    poly = inner_certificate(j)
    rat = sum((c*(1-F(1,4)**(k+1))/F(k+1)
               for k,c in poly.items() if k!=-1),F(0))
    log = 2*poly.get(-1,F(0))
    if _MUTANT=='drop-log2':
        log = F(0)
    if _MUTANT=='double-count-inner':
        rat,log = 2*rat,2*log
    return rat,log


def outer_double_mass() -> F:
    p: Poly = {1:F(1)}
    a = add(scale(power(p,2),12),{0:F(-3)})
    u,b,lo = scale(p,-1),scale(a,-1),scale(a,F(1,2))
    first = _moment_gap(u,b,multiply(a,p),lo,0)
    second = _moment_gap(u,b,add({0:F(3)},scale(p,6)),lo,0)
    return (integrate_polynomial(first,F(1,2),F(1)) +
            integrate_polynomial(second,F(1),F(3,2)))


def log_two_bounds(n: int=60) -> Interval:
    """Rational atanh(1/3) lower sum and a proved geometric upper remainder."""
    if isinstance(n,bool) or not isinstance(n,int) or n<1:
        raise ValueError('positive integer number of terms required')
    z,power_z = F(1,3), F(1,3)
    lower = F(0)
    for j in range(n):
        lower += 2*power_z/F(2*j+1)
        power_z *= z*z
    remainder = 2*power_z/(F(2*n+1)*(1-z*z))
    return lower,lower+remainder


def affine_bounds(value: AffineLog, log: Interval) -> Interval:
    a,b = value
    return (a+b*log[0],a+b*log[1]) if b>=0 else (a+b*log[1],a+b*log[0])


def divide_positive(numerator: Interval, denominator: Interval) -> Interval:
    if numerator[0]<0 or denominator[0]<=0:
        raise ValueError('positive interval division required')
    return numerator[0]/denominator[1],numerator[1]/denominator[0]


def subtract_fixed(x: F, interval: Interval) -> Interval:
    return x-interval[1],x-interval[0]


def certified_constants(n: int=60) -> dict[str,Interval]:
    log = log_two_bounds(n)
    I,J = point_moment(0),outer_double_mass()
    inner = affine_bounds(inner_moment(0),log)
    max_mass = subtract_fixed(I,inner)
    inner1 = affine_bounds(inner_moment(1),log)
    inner2 = affine_bounds(inner_moment(2),log)
    double_probability = divide_positive((J,J),max_mass)
    if _MUTANT=='uniform-cluster-from-point':
        double_probability = ((J+inner[0])/I,(J+inner[1])/I)
    return {
        'point_shape_mass':(I,I), 'inner_double_shape_mass':inner,
        'maximum_shape_mass':max_mass, 'outer_double_shape_mass':(J,J),
        'maximum_to_point_tail_ratio':(max_mass[0]/I,max_mass[1]/I),
        'double_cluster_given_extreme':double_probability,
        'two_exceedances_given_extreme':divide_positive(inner,max_mass),
        'mean_exceedance_count':divide_positive((I,I),max_mass),
        'companion_ratio_11th_moment_given_double':(inner[0]/J,inner[1]/J),
        'outer_height_mean':divide_positive(subtract_fixed(point_moment(1),inner1),max_mass),
        'outer_height_second_moment':divide_positive(subtract_fixed(point_moment(2),inner2),max_mass),
    }


def decimal_bounds(interval: Interval, digits: int=18) -> dict[str,str]:
    if not 1<=digits<=60:
        raise ValueError('digits must lie between 1 and 60')
    unit = 10**digits
    lo = interval[0]*unit
    hi = interval[1]*unit
    low = lo.numerator//lo.denominator
    high = -((-hi.numerator)//hi.denominator)
    def fmt(n: int) -> str:
        sign='-' if n<0 else ''
        n=abs(n)
        return f'{sign}{n//unit}.{n%unit:0{digits}d}'
    return {'lower':fmt(low),'upper':fmt(high)}


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def finite_checks() -> int:
    _need(not in_shape(F(-1),F(9)),'height endpoint must be open')
    _need(companion(F(-1),F(6))==(F(-13,23),F(294,529),F(-7,23)), 'signed companion')
    _need(anchor_weight(F(-3,4),F(3))==0,'one maximum anchor, not point counting')
    _need(point_moment(0)==F(246528,35),'point integral and height convention')
    _need(point_moment(1)/point_moment(0)==F(5771,7062),'point first moment')
    _need(inner_moment(0)==(F(27066286003,223205220),-F(79298560,4782969)), 'inner integral')
    _need(outer_double_mass()==F(1083417,280),'outer double integral')
    const = certified_constants(50)
    p2=const['double_cluster_given_extreme']
    _need(F(558,1000)<p2[0]<=p2[1]<F(559,1000),'cluster law must be unbiassed')
    tail_power = 10 if _MUTANT=='wrong-tail-power' else 11
    _need(tail_power==2+2+3+4,'cusp exponent ledger')
    cases=0
    for iu in range(-35,12):
        u=F(iu,24)
        b=b0(u)
        low,high=abs(b)/2,3-6*u
        if low>=high:continue
        for j in range(1,20):
            v=low+(high-low)*F(j,20)
            _need(in_shape(u,v) and shape_weight(u,v)>0,'open positive shape')
            c=companion(u,v)
            _need(is_double(u,v)==classifier_double(u,v),'companion/CUB disagreement')
            if c is not None:
                up,vp,t=c
                _need(b0(up)==b*t*t,'conic invariance')
                _need(b*up+(v-b*u)*t==v,'line invariance')
                back=companion(up,vp)
                _need(back is not None and back[0]==u and back[1]==v and back[2]*t==1,'involution')
                if in_shape(up,vp):
                    _need(t<0,'doublet transverse signs')
                    _need(anchor_weight(u,v)+anchor_weight(up,vp)==1,'once per cluster')
                    if abs(t)!=1:
                        _need(inner_double(u,v)==(abs(t)>1),'inner region')
                        _need(outer_double(u,v)==(abs(t)<1),'outer region')
                        _need((height(up,vp)-height(u,v))*(abs(t)-1)>0,'outer saddle is deeper')
            cases+=1
    return cases


def results() -> dict:
    cases=finite_checks()
    return {'passed':True,'scientific_effect':'NONE','mathematical_acceptance':False,
            'scope':'exact finite identities and rational/logarithmic integrals only',
            'rational_shape_cases':cases,'log2_terms':60,
            'tail_power':11,
            'inner_integrals':{str(j):[str(x) for x in inner_moment(j)] for j in range(3)},
            'constants':{k:decimal_bounds(v) for k,v in sorted(certified_constants().items())}}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant',choices=MUTANTS)
    args=parser.parse_args()
    global _MUTANT
    _MUTANT=args.mutant
    print(json.dumps(results(),indent=2,sort_keys=True))


if __name__=='__main__':main()
