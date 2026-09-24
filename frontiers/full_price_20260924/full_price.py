"""Exact finite controls for P15 full transformed-price hazard transfer.
Standard library only. No network, repository writes, or scientific acceptance.
"""
from __future__ import annotations
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import comb, factorial
import json


def rational(x):
    if type(x) is int or isinstance(x, Q):
        return Q(x)
    raise TypeError('exact integer or Fraction required')


def _terms(n):
    if type(n) is not int or not 4 <= n <= 256:
        raise ValueError('series length must be an integer in [4,256]')


@lru_cache(maxsize=4096, typed=True)
def log_bounds(value, terms=48):
    """Outward rational log bounds, with binary range reduction and atanh tail."""
    x = rational(value)
    _terms(terms)
    if x <= 0:
        raise ValueError('positive logarithm input required')
    if max(x.numerator.bit_length(), x.denominator.bit_length()) > 20000:
        raise ValueError('input exceeds arithmetic size limit')
    shift = 0
    while x >= 2:
        x /= 2
        shift += 1
    while x < 1:
        x *= 2
        shift -= 1
    def series(y):
        t = (y-1)/(y+1)
        total = 2*sum((t**(2*j+1)/Q(2*j+1) for j in range(terms)), Q(0))
        tail = 2*t**(2*terms+1)/(Q(2*terms+1)*(1-t*t))
        return total, total+tail
    lo, hi = series(x)
    a, b = series(Q(2))
    if shift >= 0:
        return lo+shift*a, hi+shift*b
    return lo+shift*b, hi+shift*a


def exp_one_bounds(terms=48):
    _terms(terms)
    lower = sum((Q(1, factorial(j)) for j in range(terms+1)), Q(0))
    upper = lower + Q(1, factorial(terms+1))/(1-Q(1, terms+2))
    return lower, upper


def phi_bounds(probability):
    p = rational(probability)
    if not 0 <= p <= 1:
        raise ValueError('probability outside [0,1]')
    if p == 1:
        return Q(1), Q(1)
    lo, hi = log_bounds(1/(1-p))
    return min(Q(1), lo), min(Q(1), hi)


def capacity_good(probabilities, capacity):
    ps = tuple(rational(p) for p in probabilities)
    if not 1 <= len(ps) <= 512 or type(capacity) is not int or not 0 <= capacity <= len(ps):
        raise ValueError('invalid finite capacity problem')
    if any(not 0 <= p <= 1 for p in ps):
        raise ValueError('probability outside [0,1]')
    state = [Q(1)]+[Q(0)]*capacity
    for p in ps:
        state = [(1-p)*state[j] + (p*state[j-1] if j else 0) for j in range(capacity+1)]
    return sum(state, Q(0))


def binomial_good(n, a, p):
    p = rational(p)
    if type(n) is not int or type(a) is not int or not 1 <= n <= 512 or not 0 <= a <= n or not 0 <= p <= 1:
        raise ValueError('invalid binomial parameters')
    return sum((Q(comb(n,j))*p**j*(1-p)**(n-j) for j in range(a+1)), Q(0))


@lru_cache(maxsize=128, typed=True)
def reference_bounds(n=3, a=1):
    """H=-log P(Bin(n,1-e^-1)<=a), and its inverse, enclosed rationally."""
    if type(n) is not int or type(a) is not int or not 1 <= n <= 64 or not 0 <= a < n:
        raise ValueError('reference evaluation limited to 1<=n<=64, 0<=a<n')
    el, eu = exp_one_bounds()
    pl, pu = 1-1/el, 1-1/eu
    ml, mu = binomial_good(n,a,pu), binomial_good(n,a,pl)
    hlow = -log_bounds(mu)[1]
    hhigh = -log_bounds(ml)[0]
    if hlow <= 0:
        raise ArithmeticError('insufficient positive hazard resolution')
    return (hlow,hhigh), (1/hhigh,1/hlow)


def coordinate_second_derivative(A,B,z):
    """For H(t)=-log(A+B exp(-t)), z=exp(-t); exact sign identity."""
    A,B,z = map(rational,(A,B,z))
    if min(A,B) < 0 or z <= 0 or A+B*z <= 0:
        raise ValueError('invalid decreasing-event slice')
    return -A*B*z/(A+B*z)**2


def realized_class(a,d):
    if type(a) is not int or type(d) is not int or a < 1 or d < 1:
        raise ValueError('positive integer capacity and demand required')
    return {'capacity':a,'demand':d,'block_size':a*d+1,
            'full_price_uniform_guarantee':d>=2,
            'scope':'specified realized capacity family, not arbitrary P15 inputs'}


def downset_good(n, masks, probabilities):
    """Bounded independent enumeration, used for control examples only."""
    if type(n) is not int or not 1 <= n <= 8:
        raise ValueError('explicit downset limited to eight coordinates')
    masks = set(masks)
    if 0 not in masks or any(type(m) is not int or not 0 <= m < 2**n for m in masks):
        raise ValueError('empty-admissible subset family required')
    for m in masks:
        for i in range(n):
            if m & (1<<i) and m ^ (1<<i) not in masks:
                raise ValueError('family is not decreasing')
    ps = tuple(map(rational, probabilities))
    if len(ps)!=n or any(not 0<=p<=1 for p in ps):
        raise ValueError('invalid probability vector')
    total = Q(0)
    for mask in masks:
        weight = Q(1)
        for i,p in enumerate(ps):
            weight *= p if mask & (1<<i) else 1-p
        total += weight
    return total


def local_budget_check(probabilities, a):
    """A finite interval diagnostic; its scope is not a universal theorem checker."""
    ps=tuple(map(rational, probabilities))
    good=capacity_good(ps,a)
    price_upper=Q(1)
    for p in ps:
        price_upper *= phi_bounds(p)[1]
    if good == 0:
        return True
    hlow=-log_bounds(good)[1]
    rho_upper=reference_bounds()[1][1]
    return price_upper <= rho_upper*hlow


def decimal_outward(bounds, digits=20):
    if type(digits) is not int or not 0 <= digits <= 60:
        raise ValueError('invalid output precision')
    lo,hi=map(rational,bounds)
    if lo>hi: raise ValueError('reversed interval')
    scale=10**digits
    a=(lo*scale).numerator//(lo*scale).denominator
    b=-((-hi*scale).numerator//(-hi*scale).denominator)
    def text(v):
        sign='-' if v<0 else ''; v=abs(v)
        return sign+str(v//scale)+('.'+str(v%scale).zfill(digits) if digits else '')
    return {'lower':text(a),'upper':text(b)}


def result():
    hazard,rho=reference_bounds()
    return {'object':'P15-FULL-TRANSFORMED-PRICE-20260924-v1',
            'hazard_reference':decimal_outward(hazard),
            'sharp_uniform_factor':decimal_outward(rho),
            'formula':'rho=1/(3-log(3e-2))',
            'rational_factor':'6/7',
            'factor_below_6_7':rho[1]<Q(6,7),
            'hazard_above_7_6':hazard[0]>Q(7,6),
            'probability_domain':'all independent p_v in [0,1]',
            'price_domain':'0<=c_v<=min(1,-log(1-p_v)); phi(1)=1',
            'hypotheses':'a_i>=1, d_i>=2, |X_i|=a_i*d_i+1; complete crossing clutter',
            'palette':'unchanged K>=K_H(d)',
            'scientific_acceptance':False,
            'scope':'exact constant evaluation; proof and nonauthor review are separate'}


if __name__=='__main__':
    print(json.dumps(result(),indent=2,sort_keys=True))
