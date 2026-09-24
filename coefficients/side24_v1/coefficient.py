"""Outward rational enclosure of the coefficient in main issue63, Eq.(15.2).

Only standard-library integer/Fraction arithmetic contributes to the enclosure.
No Monte Carlo, external floating-point special function, or theorem acceptance.
Run: python -B -S coefficient.py
Stirling remainder: NIST DLMF 5.11(i), 5.11(ii), positive real argument.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import lru_cache
from math import factorial, isqrt
import json

SCALE = 10**80
EPS = Q(1, 10**108)
RELATIVE_BOUND = Q(1, 10**106)


def rational(x):
    if isinstance(x, (int, str, Q)) and not isinstance(x, bool):
        return Q(x)
    raise TypeError('only exact int, str or Fraction inputs are allowed')


def floor_grid(x):
    return Q((x.numerator*SCALE)//x.denominator, SCALE)


def ceil_grid(x):
    return -floor_grid(-x)


@dataclass(frozen=True)
class I:
    lo: Q
    hi: Q | None = None

    def __post_init__(self):
        lo = rational(self.lo)
        hi = lo if self.hi is None else rational(self.hi)
        if lo > hi:
            raise ValueError('reversed interval')
        object.__setattr__(self, 'lo', floor_grid(lo))
        object.__setattr__(self, 'hi', ceil_grid(hi))

    def __add__(self, other):
        b = other if isinstance(other, I) else I(other)
        return I(self.lo+b.lo, self.hi+b.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -(other if isinstance(other, I) else I(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        b = other if isinstance(other, I) else I(other)
        ends = [x*y for x in (self.lo,self.hi) for y in (b.lo,b.hi)]
        return I(min(ends), max(ends))

    __rmul__ = __mul__

    def inv(self):
        if self.lo <= 0 <= self.hi:
            raise ValueError('division across zero')
        return I(1/self.hi, 1/self.lo)

    def __truediv__(self, other):
        return self*(other if isinstance(other,I) else I(other)).inv()

    def __rtruediv__(self, other):
        return self.inv()*other

    def __pow__(self, n):
        if type(n) is not int or n < 0:
            raise ValueError('nonnegative integer powers only')
        out = I(1)
        for _ in range(n):
            out = out*self
        return out

    def contains(self, x):
        return self.lo <= rational(x) <= self.hi

    @property
    def width(self):
        return self.hi-self.lo


def integer_root(a, n):
    if a < 0 or n < 1:
        raise ValueError('invalid integer root')
    if n == 2:
        return isqrt(a)
    low, high = 0, 1 << ((a.bit_length()+n-1)//n)
    while low+1 < high:
        mid = (low+high)//2
        if mid**n <= a:
            low=mid
        else:
            high=mid
    return high if high**n <= a else low


def root(x: I, n: int):
    if x.lo < 0 or type(n) is not int or n < 1:
        raise ValueError('positive real root required')
    def lower(v):
        return Q(integer_root((v.numerator*SCALE**n)//v.denominator,n),SCALE)
    lo, hi = lower(x.lo), lower(x.hi)
    if hi**n < x.hi:
        hi += Q(1,SCALE)
    return I(lo,hi)


def atan_small(x: Q, terms=100):
    if not 0 <= x <= 1:
        raise ValueError('atan bound requires 0<=x<=1')
    total = sum(((-1)**j*x**(2*j+1)/Q(2*j+1) for j in range(terms)),Q(0))
    nxt = (-1)**terms*x**(2*terms+1)/Q(2*terms+1)
    return I(min(total,total+nxt),max(total,total+nxt))


@lru_cache(None)
def pi_interval():
    return 16*atan_small(Q(1,5))-4*atan_small(Q(1,239))


def log_unit(x: Q):
    if not 1 <= x <= 2:
        raise ValueError('log unit requires [1,2]')
    y=(x-1)/(x+1)
    total=I(0)
    power=I(y)
    y2=I(y*y)
    for j in range(120):
        total += 2*power/Q(2*j+1)
        power *= y2
    rem=2*y**241/(Q(241)*(1-y*y))
    return I(total.lo,total.hi+rem)


@lru_cache(None)
def log_two():
    return log_unit(Q(2))


def log_point(x: Q):
    if x <= 0:
        raise ValueError('log requires positive input')
    k=0
    while x > 2:
        x /= 2
        k += 1
    while x < 1:
        x *= 2
        k -= 1
    return log_unit(x)+k*log_two()


def log_interval(x: I):
    return I(log_point(x.lo).lo,log_point(x.hi).hi)


def exp_point(x: Q):
    if x < 0:
        return exp_point(-x).inv()
    squarings=0
    while x > Q(1,4):
        x /= 2
        squarings += 1
    total=I(1)
    term=I(1)
    for k in range(1,71):
        term=term*x/k
        total += term
    first=x**71/Q(factorial(71))
    rem=first/(1-x/Q(72))
    out=I(total.lo,total.hi+rem)
    for _ in range(squarings):
        out=out*out
    return out


def exp_interval(x: I):
    return I(exp_point(x.lo).lo,exp_point(x.hi).hi)


# B_2 through B_22, the last coefficient bounds the omitted term.
BERNOULLI = [Q(1,6),Q(-1,30),Q(1,42),Q(-1,30),Q(5,66),
             Q(-691,2730),Q(7,6),Q(-3617,510),Q(43867,798),
             Q(-174611,330),Q(854513,138)]


@lru_cache(None)
def gamma_seven_sixths():
    z=Q(7,6)+32
    approx=(z-Q(1,2))*log_interval(I(z))-z+log_interval(2*pi_interval())/2
    for k,b in enumerate(BERNOULLI[:10],1):
        approx += b/(2*k*(2*k-1)*z**(2*k-1))
    omitted=BERNOULLI[10]/(22*21*z**21)
    # First omitted term is positive. This is a real analytic remainder bound.
    approx=I(approx.lo,approx.hi+omitted)
    for j in range(32):
        approx -= log_interval(I(Q(7,6)+j))
    return exp_interval(approx)


def cone_moment(d: int):
    if d == 2:
        return I(Q(4,3))
    if d == 3:
        return I(Q(29,6))-root(I(6),2)
    raise ValueError('only dimensions2 and3 are enclosed')


def reference_coefficient(d: int):
    if d not in (2,3):
        raise ValueError('only dimensions2 and3 are enclosed')
    pi=pi_interval()
    common=gamma_seven_sixths()*root(I(Q(3,2)),3)
    return common*cone_moment(d)/(2*root(I(3),2)*pi**(d-1)*root(pi,2))


def image_ledger():
    # e^(288/125)>10 by a positive rational Taylor partial sum.
    exp_lower=sum((Q(288,125)**k/Q(factorial(k)) for k in range(21)),Q(0))
    image_constant=1458*(76*24**6+15)
    derivative_bound=Q(image_constant,10**125)
    # At most10 coordinates; sqrt(2) factors cost<=2; lambda_min(C_BF)>1/3.
    covariance_relative_bound=60*derivative_bound
    return {'exp_lower_gt_10':exp_lower>10,
            'image_constant':image_constant,
            'derivative_bound':derivative_bound,
            'covariance_relative_bound':covariance_relative_bound,
            'relative_below_eps':covariance_relative_bound<EPS,
            'density_comparison_below_reported':32*EPS<RELATIVE_BOUND}


def side24_coefficient(d: int):
    ledger=image_ledger()
    if not all(ledger[k] for k in ('exp_lower_gt_10','relative_below_eps','density_comparison_below_reported')):
        raise ArithmeticError('analytic image ledger failed')
    ref=reference_coefficient(d)
    # Apply the symbolic 1e-106 perturbation BEFORE outward 80-digit rounding.
    return I(ref.lo*(1-RELATIVE_BOUND),ref.hi*(1+RELATIVE_BOUND))


def decimals(x: I, digits=20):
    scale=10**digits
    low=(x.lo.numerator*scale)//x.lo.denominator
    high=-((-x.hi.numerator*scale)//x.hi.denominator)
    def fmt(a):
        sign='-' if a<0 else ''
        a=abs(a)
        return f'{sign}{a//scale}.{a%scale:0{digits}d}'
    return {'lower':fmt(low),'upper':fmt(high)}


def report():
    return {'object':'SIDE24-COEFFICIENT-D23-20260924-v1',
            'scope':'coefficient of issue63 Eq15.2; parent theorem unreviewed',
            'method':'outward rational arithmetic; analytic image and Stirling remainder bounds',
            'relative_periodization_bound':'1e-106',
            'dimensions':{str(d):decimals(side24_coefficient(d)) for d in (2,3)},
            'cone_moments':{'2':'4/3','3':'29/6-sqrt(6)'},
            'image_ledger':{k:str(v) if isinstance(v,Q) else v for k,v in image_ledger().items()},
            'scientific_acceptance':False}


if __name__=='__main__':
    print(json.dumps(report(),indent=2,sort_keys=True))
