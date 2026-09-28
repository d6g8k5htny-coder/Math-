"""Rational controls for a tighter reference tail and weighted coordinate loads.

Standard library only; no network or repository writes. Finite calculations are
not a continuum theorem checker. See PROOF.md for the analytic argument.
"""
from fractions import Fraction as F
from itertools import product
from math import factorial


def exact(value):
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise TypeError('integer or Fraction required; floats are not certificates')
    return F(value)


def positive_integer(value):
    if type(value) is not int or value < 1:
        raise ValueError('positive integer required')
    return value


def tail_polynomial(z):
    z = exact(z)
    if z < 1:
        raise ValueError('z >= 1 required')
    return 36*z*z - 63*z + 28


def tail_nine(z):
    """P(Bin(9,1-1/z)<=2) for rational z>=1; not an approximation to e."""
    z = exact(z)
    return tail_polynomial(z)/z**9


def exp_one_interval(n=40):
    positive_integer(n)
    lower = sum((F(1, factorial(j)) for j in range(n+1)), F(0))
    remainder = F(1, factorial(n+1))/(1-F(1, n+2))
    return lower, lower + remainder


def _unit_log(x, terms):
    t = (x-1)/(x+1)
    lower = 2*sum((t**(2*j+1)/(2*j+1) for j in range(terms)), F(0))
    remainder = 2*t**(2*terms+1)/((2*terms+1)*(1-t*t))
    return lower, lower+remainder


def log_interval(x, terms=50):
    x = exact(x)
    positive_integer(terms)
    if x <= 0:
        raise ValueError('positive logarithm argument required')
    if x < 1:
        lower, upper = log_interval(1/x, terms)
        return -upper, -lower
    exponent = 0
    while x >= 2:
        x /= 2
        exponent += 1
    lower, upper = _unit_log(x, terms)
    l2, u2 = _unit_log(F(2), terms)
    return lower + exponent*l2, upper + exponent*u2


def coarse_tail_interval():
    """Outward bounds from 1957/720<e<87/32 and increasing P on this interval."""
    lower_e, upper_e = F(1957, 720), F(87, 32)
    return (tail_polynomial(lower_e)/upper_e**9,
            tail_polynomial(upper_e)/lower_e**9)


def even_large_tail_bound(a):
    if type(a) is not int or a < 4 or a % 2:
        raise ValueError('even capacity >=4 required')
    return F(1, 2)*F(5, 16)**a


def factor_interval():
    """Outward bounds for 2/[9-log(36e^2-63e+28)], using rational series."""
    lower_e, upper_e = exp_one_interval()
    lower_log, _ = log_interval(tail_polynomial(lower_e))
    _, upper_log = log_interval(tail_polynomial(upper_e))
    lower_h, upper_h = 9-upper_log, 9-lower_log
    if lower_h <= 0:
        raise ValueError('nonpositive certified hazard floor')
    return 2/upper_h, 2/lower_h


def _blocks(blocks):
    if any(not isinstance(b, (set, frozenset)) or not b or
           any(type(v) is not int or v < 0 for v in b) for b in blocks):
        raise ValueError('nonempty sets of nonnegative integer coordinates required')


def coordinate_load(blocks, weights):
    """Maximum SUM of nonnegative weights over blocks sharing a coordinate."""
    _blocks(blocks)
    if len(blocks) != len(weights):
        raise ValueError('one weight per block required')
    weights = [exact(w) for w in weights]
    if any(w < 0 for w in weights):
        raise ValueError('nonnegative weights required')
    ground = set().union(*blocks)
    return max((sum((w for b, w in zip(blocks, weights) if v in b), F(0))
                for v in ground), default=F(0))


def minimal_active_indices(blocks, capacities, demands):
    """Deduplicate and remove redundant supersets from maximal-demand blocks.

This only constructs a proposed full-block cover. Its eligibility still requires
an exact palette theorem; it does not certify coloring of an arbitrary downset.
    """
    _blocks(blocks)
    if not blocks or len(blocks) != len(capacities) or len(blocks) != len(demands):
        raise ValueError('one capacity and demand for each nonempty block required')
    for a, d in zip(capacities, demands):
        positive_integer(a)
        positive_integer(d)
    if any(len(b) != a*d+1 for b, a, d in zip(blocks, capacities, demands)):
        raise ValueError('block size must equal a*d+1')
    active = [i for i, d in enumerate(demands) if d == max(demands)]
    return [i for i in active if not any(
        blocks[j] < blocks[i] or (j < i and blocks[j] == blocks[i])
        for j in active if j != i)]


def good_probability(blocks, capacities, probabilities):
    """Exact finite product enumeration, limited to 12 coordinates."""
    _blocks(blocks)
    if len(blocks) != len(capacities) or any(type(a) is not int or a < 0 for a in capacities):
        raise ValueError('nonnegative integer capacity per block required')
    ground = sorted(set().union(*blocks))
    if len(ground) > 12:
        raise ValueError('enumeration limit is 12 coordinates')
    if any(v not in probabilities for v in ground):
        raise ValueError('missing original-coordinate probability')
    p = {v: exact(probabilities[v]) for v in ground}
    if any(value < 0 or value > 1 for value in p.values()):
        raise ValueError('probabilities must be in [0,1]')
    total = F(0)
    for bits in product((0, 1), repeat=len(ground)):
        chosen = {v for v, bit in zip(ground, bits) if bit}
        if not all(len(chosen & block) <= a for block, a in zip(blocks, capacities)):
            continue
        mass = F(1)
        for v, bit in zip(ground, bits):
            mass *= p[v] if bit else 1-p[v]
        total += mass
    return total
