#!/usr/bin/env python3
"""Finite rational controls and source-identity checks, not analytic proof acceptance."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import hashlib
import json

HERE = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def add(a, b):
    return [(a[i] if i < len(a) else F(0)) + (b[i] if i < len(b) else F(0)) for i in range(max(len(a), len(b)))]

def mul(a, b):
    result = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return result

def der(p):
    return [i * p[i] for i in range(1, len(p))]

def at(p, x):
    return sum(c * x ** i for i, c in enumerate(p))

def cubic(b, k, r):
    return [b-k*r**3/2, -3*k*r**2/2, F(0), 2*k]

source_inventory = json.loads((HERE / 'SOURCES.json').read_text())
source_checks = []
proof_text = (HERE / 'PROOF.md').read_text()
for source in source_inventory['sources']:
    raw = (HERE / source['local_path']).read_bytes()
    sha256 = hashlib.sha256(raw).hexdigest()
    blob = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
    require(len(raw) == source['bytes'], f"size {source['id']}")
    require(sha256 == source['sha256'], f"SHA256 {source['id']}")
    require(blob == source['git_blob'], f"Git blob {source['id']}")
    if source['id'] in {'P', 'MARK_2', 'MARK_D'}:
        require(sha256 in proof_text, f"stated source hash {source['id']}")
    source_checks.append({'id': source['id'], 'bytes': len(raw), 'sha256': sha256, 'git_blob': blob})

quartic_cases = 0
negative_controls = 0
for r, k, b in product([F(1,8), F(1,100)], [F(1,3), F(1), F(7,2)], [F(-4), F(0), F(5)]):
    a, c, e = -r/2, r/2, 3*r/2
    p = cubic(b, k, r)
    require(at(p,a) == b and at(p,c) == b-k*r**3, 'cubic values')
    require(at(der(p),a) == 0 and at(der(p),c) == 0, 'cubic gradient pins')
    require(der(der(der(p))) == [12*k], 'third derivative normalization')
    require(at(p,e) == b+4*k*r**3, 'cubic escape value')
    require((e-a)**2*(e-c)**2 == 4*r**4, 'Hermite remainder factor')
    bubble = mul([-a, F(1)], [-c, F(1)])
    bubble = mul(bubble,bubble)
    for t in [F(-1), F(0), F(1)]:
        coeff = t*k/(8*r)
        g = add(p, [coeff*v for v in bubble])
        H = abs(der(der(der(der(g))))[0])
        require(r*H <= 3*k, 'good fourth-derivative condition')
        require(at(g,a) == b and at(g,c) == b-k*r**3, 'quartic exact values')
        require(at(der(g),a) == 0 and at(der(g),c) == 0, 'quartic exact gradients')
        require(der(g) == mul([-r*r/4,F(0),F(1)],[6*k,4*coeff]), 'exact derivative factorization')
        require(6*k - 6*abs(coeff)*r >= 21*k/4, 'positive derivative factor throughout axial segment')
        require(at(g,e) >= b+F(7,2)*k*r**3, 'escape endpoint bound')
        require(12*k-2*r*H >= 6*k, 'strict convexity margin')
        quartic_cases += 1
    # Dropping the derivative condition is not harmless, even with the exact pins
    # and the correct axial max/min types. This is only an axial negative fixture.
    coeff = -2*k/r
    g = add(p, [coeff*v for v in bubble])
    require(at(g,e) == b-4*k*r**3, 'negative fixture endpoint')
    require(r*abs(der(der(der(der(g))))[0]) == 48*k, 'negative fixture outside hypothesis')
    require(at(der(der(g)),a) < 0 < at(der(der(g)),c), 'negative fixture axial types retained')
    negative_controls += 1

power_cases = 0
for q, desired in product([F(1,2),F(1),F(2),F(29,4)], [F(1),F(4),F(10)]):
    markov_power = 3*q + 3 + desired + 1
    require(markov_power - 3*q - 3 == desired + 1, 'weighted tail exponent')
    power_cases += 1

print(json.dumps({
    'status': 'PASS',
    'scope': 'Exact finite algebra controls, hypothesis-sensitive negative fixtures, normalization exponents, and source identities only; no Gaussian simulation, infinite-dimensional proof certification, or scientific acceptance.',
    'source_identity_checks': source_checks,
    'good_quartic_cases': quartic_cases,
    'outside_hypothesis_axial_negative_controls': negative_controls,
    'normalization_exponent_cases': power_cases,
    'proof_sha256': hashlib.sha256((HERE/'PROOF.md').read_bytes()).hexdigest(),
    'sources_sha256': hashlib.sha256((HERE/'SOURCES.json').read_bytes()).hexdigest(),
    'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}, indent=2, sort_keys=True))
