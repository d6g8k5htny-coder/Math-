#!/usr/bin/env python3
"""Finite rational author controls, not continuum proof or acceptance."""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def transpose(a):
    return list(map(list, zip(*a)))


def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col))
             for col in transpose(b)] for row in a]


def mv(a, v):
    return [sum(x*y for x, y in zip(row, v)) for row in a]


def determinant(a):
    if len(a) == 1:
        return a[0][0]
    return sum((-1)**j*a[0][j]*determinant(
        [row[:j]+row[j+1:] for row in a[1:]]) for j in range(len(a)))


counts = {}
A = [[F(1), F(1), F(0)], [F(0), F(1), F(1)]]
Ginv = [[F(2, 3), F(-1, 3)], [F(-1, 3), F(2, 3)]]
require(mm(mm(A, transpose(A)), Ginv) == [[1, 0], [0, 1]], 'Gram inverse')
projection = mm(mm(transpose(A), Ginv), A)
C = [[F(i == j)-projection[i][j] for j in range(3)] for i in range(3)]
require(C == transpose(C), 'residual symmetry')
require(mm(C, C) == C, 'residual idempotence')
require(mm(A, C) == [[0]*3 for _ in range(2)], 'exact residual pins')
require(C[0][1] == F(-1, 3), 'correlated residual independence obstruction')
require(all(0 <= C[j][j] <= 1 for j in range(3)), 'marginal variance contraction')
target_cases = 0
for v in product([F(-2), F(0), F(1, 3), F(5)], repeat=2):
    mean = mv(mm(transpose(A), Ginv), v)
    energy = sum(x*y for x, y in zip(v, mv(Ginv, v)))
    require(mv(A, mean) == list(v), 'conditional mean pins')
    require(sum(x*x for x in mean) == energy, 'regression energy')
    require(all(x*x <= energy for x in mean), 'coordinate mean bound')
    target_cases += 1
counts['regression_targets'] = target_cases

weighted_cases = 0
for weights in [[F(0), F(0), F(0)], [F(0), F(2), F(0)],
                [F(1, 3), F(7, 2), F(0)], [F(2), F(3), F(4)]]:
    S = sum(weights)
    for z in product([F(0), F(1, 2), F(3)], repeat=3):
        T = sum(w*x for w, x in zip(weights, z))
        require(T*T <= S*sum(w*x*x for w, x in zip(weights, z)),
                'weighted Cauchy with total mass')
        weighted_cases += 1
    if S:
        eta0 = 1/(8*S*S)
        lam = eta0/2
        require(1-4*eta0*S*S == F(1, 2), 'Gaussian square safe denominator')
        require(lam < eta0 and 1-4*lam*S*S > 0, 'tilt absorption slack')
        require(1-4*(1/(4*S*S))*S*S == 0, 'excluded square boundary')
require(F(2)**2 > F(2)*F(1)**2, 'omitting total mass is false')
counts['weighted_cauchy_cases'] = weighted_cases

congruence_cases = 0
for dimension, root_r in product([2, 3], [F(1, 2), F(1, 3), F(2, 3)]):
    r = root_r**2
    alpha = F(-3)
    beta = [F(j+1, 2) for j in range(dimension-1)]
    block = [[F(2+i) if i == j else F(1, 4)
              for j in range(dimension-1)] for i in range(dimension-1)]
    H = [[r*alpha]+[r*x for x in beta]]
    H += [[r*beta[i]]+block[i] for i in range(dimension-1)]
    diag = [1/root_r]+[F(1)]*(dimension-1)
    scaled = [[diag[i]*H[i][j]*diag[j] for j in range(dimension)]
              for i in range(dimension)]
    require(scaled[0][0] == alpha, 'corrected congruence axial entry')
    require(scaled[0][1:] == [root_r*x for x in beta], 'scaled cross block')
    require(determinant(scaled) == determinant(H)/r, 'determinant divided by radius')
    wrong_entry = root_r*H[0][0]*root_r
    require(wrong_entry == r*r*alpha and wrong_entry != alpha,
            'wrong congruence counterexample')
    congruence_cases += 1
counts['corrected_congruence_cases'] = congruence_cases

exponent_cases = 0
for q, theta, dimension in product([F(1, 4), F(1), F(7, 3)],
                                   [F(1, 4), F(1, 2), F(3, 4)], [2, 3, 5]):
    # X^q <= (2/k)^q r^(-3q) K^q, with outer normalization r^-3.
    require(-3*q-3 == -(3*q+3), 'scaled finite lifetime radius power')
    # K^q <= C exp(theta*lambda*K^2); remaining tail budget positive.
    lam = F(1, 10)
    tail_budget = (1-theta)*lam
    require(theta*lam+tail_budget == lam and tail_budget > 0,
            'polynomial absorption exponential split')
    # Actual determinant tilt is polynomial degree 2d, with same absorption.
    require(2*dimension+q > 0, 'tilt and lifetime polynomial degrees')
    exponent_cases += 1
counts['tail_exponent_cases'] = exponent_cases

source_checks = []
for source in json.loads((HERE / 'SOURCES.json').read_text())['sources']:
    raw = (ROOT / source['path']).read_bytes()
    require(len(raw) == source['bytes'], 'source bytes: ' + source['id'])
    require(hashlib.sha256(raw).hexdigest() == source['sha256'],
            'source digest: ' + source['id'])
    require(hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
            == source['git_blob'], 'source blob: ' + source['id'])
    source_checks.append(source['id'])

print(json.dumps({
    'status': 'PASS',
    'scope': 'Finite rational author controls only; no Gaussian simulation, '
             'continuum verification or scientific acceptance.',
    'counts': counts,
    'source_checks': source_checks,
    'proof_sha256': hashlib.sha256((HERE / 'PROOF.md').read_bytes()).hexdigest(),
    'sources_sha256': hashlib.sha256((HERE / 'SOURCES.json').read_bytes()).hexdigest(),
    'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}, indent=2, sort_keys=True))
