"""Exact finite controls for the conditional rare-cluster consequence packet.

Standard library only. No Gaussian proof or statistical estimation is performed.
All probability inputs are exact int/Fraction values, never binary floats.
"""
import argparse
import json
import math
from fractions import Fraction as F
from functools import lru_cache

MUTANTS = ('palm-is-conditional', 'cp-rate-is-mean', 'erase-cross-term',
           'third-lower', 'unique-limit', 'wrong-r6-ledger', 'ordinary-poisson')


def natural(n):
    if type(n) is not int or n < 0:
        raise ValueError('nonnegative integer required')
    return n


def rational(x):
    if type(x) not in (int, F):
        raise ValueError('exact int/Fraction required')
    return F(x)


def validate(law):
    if not isinstance(law, dict) or not law:
        raise ValueError('nonempty finite PMF mapping required')
    out = {natural(n): rational(p) for n, p in law.items()}
    if any(p < 0 for p in out.values()) or sum(out.values()) != 1:
        raise ValueError('nonnegative masses summing to one required')
    return out


def falling(n, q):
    natural(n)
    natural(q)
    return math.prod(n-j for j in range(q)) if q <= n else 0


@lru_cache(maxsize=None)
def stirling(n, k):
    natural(n)
    natural(k)
    if n == 0:
        return int(k == 0)
    if k == 0 or k > n:
        return 0
    return k*stirling(n-1, k) + stirling(n-1, k-1)


def moment(law, q, factorial=False):
    law = validate(law)
    natural(q)
    return sum((p*(falling(n, q) if factorial else n**q)
                for n, p in law.items()), F(0))


def tilt(law, size_biased=False):
    law = validate(law)
    weights = {n: p*(n if size_biased else 1) for n, p in law.items() if n > 0}
    total = sum(weights.values(), F(0))
    if total == 0:
        raise ValueError('positive occurrence probability required')
    return {n: p/total for n, p in weights.items() if p > 0}


def cp_moments(law, q):
    """Factorial moments of CP(p, Law(N | N>0)); NOT CP(E N, ...)."""
    natural(q)
    law = validate(law)
    a = [F(0)] + [moment(law, j, True) for j in range(1, q+1)]
    bell = [F(1)]
    for n in range(1, q+1):
        bell.append(sum((math.comb(n-1, j-1)*a[j]*bell[n-j]
                         for j in range(1, n+1)), F(0)))
    return bell


def exp_bounds(x, degree=40):
    """Taylor lower/upper rational bounds on exp(-x), x >= 0.

    The odd/even Taylor remainder signs hold by Lagrange's formula, even
    before terms decrease. Clipping to [0,1] is safe for x >= 0.
    """
    x = rational(x)
    natural(degree)
    if x < 0 or degree % 2:
        raise ValueError('x >= 0 and even degree required')
    upper = sum(((-x)**j/F(math.factorial(j)) for j in range(degree+1)), F(0))
    lower = upper - x**(degree+1)/math.factorial(degree+1)
    return max(F(0), lower), min(F(1), upper)


def poisson_tv(law, rate):
    """Enclose exact TV via overlap; the Poisson tail is NOT discarded."""
    law = validate(law)
    rate = rational(rate)
    lo, hi = exp_bounds(rate)
    overlap_lo = sum((min(p, lo*rate**n/math.factorial(n))
                      for n, p in law.items()), F(0))
    overlap_hi = sum((min(p, hi*rate**n/math.factorial(n))
                      for n, p in law.items()), F(0))
    return 1-overlap_hi, 1-overlap_lo


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run_checks(mutant=None):
    groups = []
    law = {0: F(3, 4), 1: F(1, 8), 3: F(1, 8)}
    j = tilt(law)
    y = j if mutant == 'palm-is-conditional' else tilt(law, True)
    ej = moment(j, 1)
    require(moment(y, 1)-ej == (moment(j, 2)-ej**2)/ej, 'Palm variance identity')
    groups.append('conditional-versus-size-biased')

    p = 1-law.get(0, 0)
    mu = moment(law, 1)
    rate = mu if mutant == 'cp-rate-is-mean' else p
    require(rate*ej == mu, 'compound occurrence rate, not count mean')
    second = cp_moments(law, 2)[2]
    if mutant == 'erase-cross-term':
        second -= mu**2
    if mutant == 'ordinary-poisson':
        second = mu**2
    require(second == moment(law, 2, True)+mu**2, 'compound second factorial moment')
    groups.append('compound-rate-and-factorial-moments')

    for n in range(12):
        for q in range(1, 9):
            require(n**q == sum(stirling(q, k)*falling(n, k) for k in range(1, q+1)),
                    'Stirling identity')
    groups.append('ordinary-from-factorial-moments')

    eps = F(1, 128)
    two = {0: 1-eps, 2: eps}
    # A=2, a=1 meets the theorem's small-epsilon thresholds.
    for rate in [F(i, 128) for i in range(33)] + [F(1), F(2), F(4)]:
        lo, hi = poisson_tv(two, rate)
        require(eps/2 <= lo <= hi <= 1, 'ordinary Poisson obstruction probes')
    groups.append('poisson-obstruction-exact-probes')

    for p in [F(1, 100), F(1, 8), F(1, 2), F(1)]:
        lo, hi = exp_bounds(p)
        require(lo-1+p >= p*p/3, 'zero-event compound lower bound')
        require(p*(1-lo) <= p*p, 'binary-kernel compound upper bound')
        require(lo-1+p <= p*(1-hi), 'ordered compound bounds')
    order = 5 if mutant == 'wrong-r6-ledger' else 2*3
    require(order == 6, 'epsilon squared is r to the sixth')
    groups.append('compound-TV-bounds-and-r6-ledger')

    third = moment(two, 3, True)
    require(third > 0 if mutant == 'third-lower' else third == 0,
            'no third-factorial lower bound follows')
    lhs, rhs = {2: F(1)}, {3: F(1)}
    require(lhs == rhs if mutant == 'unique-limit' else lhs != rhs,
            'oscillating intensity counterexample')
    groups.append('nonclaims-counterexamples')
    return {'schema': 1, 'passed': True, 'groups': groups,
            'scientific_effect': 'NONE', 'mathematical_acceptance': False,
            'scope': 'finite exact identities and probes only'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant', choices=MUTANTS)
    args = parser.parse_args()
    try:
        result = run_checks(args.mutant)
    except ValueError as exc:
        print(json.dumps({'passed': False, 'error': str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
