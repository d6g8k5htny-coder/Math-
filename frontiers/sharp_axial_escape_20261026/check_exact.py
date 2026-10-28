#!/usr/bin/env python3
"""Author-side exact algebra controls; not a proof of the C4 theorem."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def add(a, b):
    return [(a[i] if i < len(a) else F(0))
            + (b[i] if i < len(b) else F(0))
            for i in range(max(len(a), len(b)))]


def mul(a, b):
    result = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return result


def scale(a, c):
    return [c * x for x in a]


def derivative(a):
    return [i * a[i] for i in range(1, len(a))]


def at(a, x):
    return sum(c * x ** i for i, c in enumerate(a))


def compose(a, b):
    result, power = [F(0)], [F(1)]
    for c in a:
        result = add(result, scale(power, c))
        power = mul(power, b)
    return result


counts = {}
source_checks = []
for source in json.loads((HERE / 'SOURCES.json').read_text())['sources']:
    raw = (ROOT / source['path']).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    blob = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
    require(len(raw) == source['bytes'], 'source byte count: ' + source['id'])
    require(digest == source['sha256'], 'source digest: ' + source['id'])
    require(blob == source['git_blob'], 'source blob: ' + source['id'])
    source_checks.append(source['id'])

polynomial_cases = 0
for rho in [F(0), F(1, 8), F(1, 2), F(99, 100), F(1), F(101, 100), F(2)]:
    # Normalized lower envelope, independently expanded from (4).
    p = [F(0), F(0), -3-rho, 2+2*rho, -rho]
    require(add(p, [F(1)]) == mul([F(1), F(-2), F(1)],
                                 [F(1), F(2), -rho]), 'minimum factorization')
    if rho == 1:
        require(p == scale(mul([F(0), F(0), F(1)],
                               [F(4), F(-4), F(1)]), -1), 'boundary square')
    if rho > 1:
        square = mul([-1-1/rho, F(1)], [-1-1/rho, F(1)])
        bracket = add(scale(square, rho), [1-1/rho])
        require(p == scale(mul([F(0), F(0), F(1)], bracket), -1),
                'strict obstruction square')
    for r, k, b in product([F(1, 8), F(1, 100)],
                           [F(1, 3), F(1), F(7, 2)], [F(-4), F(0), F(5)]):
        physical = add([b], scale(compose(p, [F(1, 2), 1/r]), k*r**3))
        first = derivative(physical)
        second = derivative(first)
        fourth = derivative(derivative(second))
        require(at(physical, -r/2) == b, 'birth pin')
        require(at(physical, r/2) == b-k*r**3, 'lower pin')
        require(at(first, -r/2) == at(first, r/2) == 0, 'derivative pins')
        require(fourth == [-24*rho*k/r], 'physical fourth derivative')
        require(at(second, -r/2) == -2*k*r*(3+rho), 'maximum Hessian')
        require(at(second, r/2) == 2*k*r*(3-rho), 'minimum Hessian')
        require(at(physical, 3*r/2)-b == 4*k*r**3*(1-rho), 'endpoint margin')
        polynomial_cases += 1
counts['physical_quartic_cases'] = polynomial_cases

require(add([F(-3), F(2)], [F(4), F(-4), F(1)])
        == [F(1), F(-2), F(1)], 'endpoint optimization polynomial identity')
counts['endpoint_optimization_identity'] = 1

# At the proposed weak threshold, there is no strict escape, while both types
# remain strict. This rejects changing rho<1 to rho<=1.
boundary = [F(0), F(0), F(-4), F(4), F(-1)]
require(at(boundary, 0) == at(boundary, 2) == 0, 'boundary has no endpoint margin')
require(at(derivative(derivative(boundary)), 0) < 0
        < at(derivative(derivative(boundary)), 1), 'boundary types')
counts['weak_threshold_counterexample'] = 1

exponent_cases = 0
for q, epsilon in product([F(1, 4), F(1, 2), F(1), F(7, 3)],
                          [F(1, 10), F(1), F(5)]):
    s = 4*q+3+epsilon
    require((s-q)-3*q-3 == epsilon, 'normalized finite-moment exponent')
    # Wrongly using s-3q-3 omits the norm factor in X^q.
    require(s-3*q-3 != epsilon, 'omitted norm power must change exponent')
    exponent_cases += 1
counts['exponent_cases'] = exponent_cases

moment_cases = 0
for q, n in product([1, 2, 3], [4, 8, 16, 32]):
    r, big_b = F(1, n), F(24)
    s_star = 4*q+3
    prob = [1-r**3-r**s_star, r**3, r**s_star]
    kval = [F(1), F(1), big_b/r]
    xval = [F(1), F(1, 2), r**-4]
    require(min(prob) > 0 and sum(prob) == 1, 'three-atom probability law')
    require(all(x <= 2*v/r**3 for x, v in zip(xval, kval)), 'lifetime size bound')
    require(xval[2] > 1 and kval[2] >= 24/r, 'bad-norm inclusion')
    for s in [1, s_star-1, s_star]:
        moment = sum(p*v**s for p, v in zip(prob, kval))
        require(moment <= 1+big_b**s, 'uniform norm moment bound')
    clipped = sum(prob[i]*min(xval[i], 1)**q for i in [1, 2])/r**3
    actual = sum(prob[i]*xval[i]**q for i in [1, 2])/r**3
    require(clipped == F(1, 2)**q+r**(4*q), 'clipped limit formula')
    require(actual == F(1, 2)**q+1, 'nonvanishing actual moment defect')
    require(actual-clipped == 1-r**(4*q), 'endpoint implication falsified')
    moment_cases += 1
counts['abstract_endpoint_moment_counterexamples'] = moment_cases

print(json.dumps({
    'status': 'PASS',
    'scope': 'Author-side exact finite algebra and source identities only; '
             'no independent scientific acceptance or formal verification.',
    'counts': counts,
    'source_checks': source_checks,
    'proof_sha256': hashlib.sha256((HERE / 'PROOF.md').read_bytes()).hexdigest(),
    'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'sources_sha256': hashlib.sha256((HERE / 'SOURCES.json').read_bytes()).hexdigest(),
}, indent=2, sort_keys=True))
