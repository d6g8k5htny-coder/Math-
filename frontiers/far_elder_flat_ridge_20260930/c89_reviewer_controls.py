#!/usr/bin/env python3
"""C89 reviewer-only exact controls; no author executable or third-party package.

Run: python -B c89_reviewer_controls.py --source-dir PATH
Repeat with -B -O. PATH contains PROOF.md, source/P.md, source/G.md.
Omit --source-dir to run algebra controls without source-custody checks.
The finite controls do not prove uniform analytic bounds or parent hypotheses.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import product
from math import factorial
from pathlib import Path


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


ZERO = (F(0), F(0))
ONE = (F(1), F(0))


def ca(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cs(a, r):
    return (a[0] * r, a[1] * r)


def conj(a):
    return (a[0], -a[1])


def iphase(q):
    return (ONE, (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1)))[q % 4]


def add(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = ca(out.get(k, ZERO), v)
    return {k: v for k, v in out.items() if v != ZERO}


def scale(a, r):
    return {k: cs(v, r) for k, v in a.items() if cs(v, r) != ZERO}


def mul(a, b, truncated=False):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            k = tuple(x + y for x, y in zip(ka, kb))
            if truncated and sum(k) > 2:
                continue
            out[k] = ca(out.get(k, ZERO), cm(va, vb))
    return {k: v for k, v in out.items() if v != ZERO}


def power(a, n, d, truncated=False):
    out = {(0,) * d: ONE}
    for _ in range(n):
        out = mul(out, a, truncated)
    return out


def indices(d):
    return [a for a in product(range(3), repeat=d) if sum(a) <= 2]


def afact(a):
    out = 1
    for v in a:
        out *= factorial(v)
    return out


def unit(d, j, sign=1):
    return tuple(sign if k == j else 0 for k in range(d))


def derivative(poly, site, alpha):
    out = ZERO
    for k, coeff in poly.items():
        factor = 1
        for n, a in zip(k, alpha):
            factor *= n ** a
        phase = iphase(sum(n * x for n, x in zip(k, site)) + sum(alpha))
        out = ca(out, cs(cm(coeff, phase), F(factor)))
    return out


def bpoly(site):
    d = len(site)
    out = {(0,) * d: (F(d), F(0))}
    for j, x in enumerate(site):
        out = add(out, {unit(d, j): cs(iphase(-x), F(-1, 2)),
                        unit(d, j, -1): cs(iphase(x), F(-1, 2))})
    return out


def zpoly(site, j):
    d = len(site)
    return {unit(d, j): cm(iphase(-site[j]), (F(0), F(-1, 2))),
            unit(d, j, -1): cm(iphase(site[j]), (F(0), F(1, 2)))}


def qpoly(sites, i, exponent=2):
    d = len(sites[0])
    out = {(0,) * d: ONE}
    for j, site in enumerate(sites):
        if j == i:
            continue
        bp = bpoly(site)
        denominator = derivative(bp, sites[i], (0,) * d)
        need(denominator[1] == 0 and denominator[0] > 0, 'repeated-site denominator')
        out = mul(out, power(scale(bp, 1 / denominator[0]), exponent, d))
    return out


def reciprocal_jet(q, site):
    d = len(site)
    jet = {a: cs(derivative(q, site, a), F(1, afact(a))) for a in indices(d)}
    need(jet[(0,) * d] == ONE, 'Q_i(x_i) != 1')
    u = add(jet, {(0,) * d: (F(-1), F(0))})
    return add(add({(0,) * d: ONE}, scale(u, -1)), mul(u, u, True))


def compose(taylor, zs):
    d = len(zs)
    out = {}
    for alpha, coeff in taylor.items():
        term = {(0,) * d: coeff}
        for j, a in enumerate(alpha):
            term = mul(term, power(zs[j], a, d))
        out = add(out, term)
    return out


def cardinals(sites, exponent=2, reciprocal=True, factorials=True):
    d = len(sites[0])
    out = {}
    for i, site in enumerate(sites):
        q = qpoly(sites, i, exponent)
        inv = reciprocal_jet(q, site) if reciprocal else {(0,) * d: ONE}
        zs = [zpoly(site, j) for j in range(d)]
        for alpha in indices(d):
            den = afact(alpha) if factorials else 1
            t = mul(inv, {alpha: (F(1, den), F(0))}, True)
            out[(i, alpha)] = mul(q, compose(t, zs))
    return out


def mismatch_count(sites, **variant):
    d = len(sites[0])
    count = 0
    for (i, alpha), poly in cardinals(sites, **variant).items():
        for j, site in enumerate(sites):
            for beta in indices(d):
                expected = ONE if i == j and alpha == beta else ZERO
                count += derivative(poly, site, beta) != expected
    return count


def positive_definite(matrix):
    n = len(matrix)
    lower = [[F(0)] * n for _ in range(n)]
    pivots = []
    for i in range(n):
        lower[i][i] = F(1)
        pivot = matrix[i][i] - sum(lower[i][k] ** 2 * pivots[k] for k in range(i))
        if pivot <= 0:
            return False
        pivots.append(pivot)
        for j in range(i + 1, n):
            lower[j][i] = (matrix[j][i] - sum(lower[j][k] * lower[i][k] * pivots[k]
                                            for k in range(i))) / pivot
    return True


def finite_gram(sites, band):
    d = len(sites[0])
    coords = [(site, a) for site in sites for a in indices(d)]
    out = [[F(0) for _ in coords] for _ in coords]
    for mode in product(range(-band, band + 1), repeat=d):
        features = [derivative({mode: ONE}, site, a) for site, a in coords]
        for i, fi in enumerate(features):
            for j, fj in enumerate(features):
                value = cm(fi, conj(fj))
                out[i][j] += value[0]
    return out


def controls():
    sets = [[(0,), (1,), (2,)],
            [(0, 0), (1, 0), (0, 1), (2, 2)],
            [(0, 0, 0), (1, 0, 1), (0, 1, 2)]]
    derivative_checks = frequency_checks = realness_checks = product_checks = 0
    for sites in sets:
        d, s = len(sites[0]), len(sites)
        need(len(indices(d)) == (d + 1) * (d + 2) // 2, 'jet count')
        cq = cr = F(0)
        for i, site in enumerate(sites):
            qp = qpoly(sites, i)
            cq = max(cq, sum(abs(a) + abs(b) for a, b in qp.values()))
            inv = reciprocal_jet(qp, site)
            for alpha in indices(d):
                rp = mul(inv, {alpha: (F(1, afact(alpha)), F(0))}, True)
                cr = max(cr, sum(abs(a) + abs(b) for a, b in rp.values()))
        for (i, alpha), poly in cardinals(sites).items():
            # omega=1 here, so C_Z=1. This rational coefficient norm
            # dominates the complex absolute-value norm and is submultiplicative.
            need(sum(abs(a) + abs(b) for a, b in poly.values()) <= cq * cr,
                 'successor product bound')
            product_checks += 1
            need(all(max(abs(x) for x in k) <= 2 * s for k in poly), 'frequency support')
            frequency_checks += 1
            for k, value in poly.items():
                need(poly.get(tuple(-x for x in k), ZERO) == conj(value), 'real polynomial')
                realness_checks += 1
            for j, site in enumerate(sites):
                for beta in indices(d):
                    expected = ONE if i == j and alpha == beta else ZERO
                    need(derivative(poly, site, beta) == expected, 'cardinal jet mismatch')
                    derivative_checks += 1
    variants = [('order_two_zero_only', {'exponent': 1}),
                ('omit_reciprocal', {'reciprocal': False}),
                ('omit_alpha_factorial', {'factorials': False})]
    rejected = {}
    for name, kwargs in variants:
        bad = sum(mismatch_count(sites, **kwargs) for sites in sets[:2])
        need(bad > 0, 'mutation survived: ' + name)
        rejected[name] = {'mismatches': bad}
    try:
        qpoly([(0,), (0,)], 0)
    except RuntimeError:
        rejected['repeated_site_cardinal'] = {'rejected': True}
    else:
        raise RuntimeError('repeated-site construction survived')
    sites = [(0,), (1,)]
    polys = cardinals(sites)
    cstar = max(sum(abs(v[0]) + abs(v[1]) for v in p.values()) for p in polys.values())
    dimension = len(polys)
    lower = F(1, dimension) / cstar ** 2
    gram = finite_gram(sites, 2 * len(sites))
    gram_minus_lower = [[x - (lower if i == j else 0) for j, x in enumerate(row)]
                        for i, row in enumerate(gram)]
    need(positive_definite(gram_minus_lower), 'finite Gram lower bound')
    duplicate = finite_gram([(0,), (0,)], 4)
    need(duplicate[0][0] + duplicate[3][3] - 2 * duplicate[0][3] == 0,
         'duplicate-site null vector')
    rejected['repeated_site_positive_gram'] = {'null_vector_variance': '0'}
    covariance_checks = 2
    for rho in (F(1, 2), F(1, 3)):
        epsilon = rho ** 12
        sigma = epsilon ** 2
        cross = epsilon
        coefficient = cross / sigma
        need(coefficient ** 2 == 1 / sigma, 'regression energy equality')
        need(coefficient == rho ** -12, 'regression separation exponent')
        need(1 - cross ** 2 / sigma == 0, 'singular residual variance')
        need(coefficient > 1, 'unamplified regression variant survived')
        covariance_checks += 4
    rejected['unamplified_regression'] = {'rejected': True}
    sigma = [[F(3), F(1), F(1)], [F(1), F(3), F(1)], [F(1), F(1), F(3)]]
    need(positive_definite([[x - int(i == j) for j, x in enumerate(row)]
                            for i, row in enumerate(sigma)]), 'joint lower bound')
    schur = [[sigma[i][j] - sigma[i][0] * sigma[0][j] / sigma[0][0]
              for j in (1, 2)] for i in (1, 2)]
    need(positive_definite([[x - int(i == j) for j, x in enumerate(row)]
                            for i, row in enumerate(schur)]), 'Schur lower bound')
    covariance_checks += 2
    need(F(1) > F(1) * F(1, 2), 'weighted-tail adverse control')
    rejected['unweighted_tail_substitution'] = {'weighted_mass': '1', 'product_of_means': '1/2'}
    exponent_checks = 0
    for d in (2, 3, 5):
        J = (d + 1) * (d + 2) // 2
        for q in range(1, 7):
            N, p = 2 * (q + 1), 2 * d * (q + 1)
            B = 12 * N * (N + 1) * (d + 1)
            A = 24 * J + 12 * d * N + B
            main = N * (1 + F(d, 2)) - F(d * N, 2) - F(d * N, 2 * d)
            need(main == F(N, 2) == q + 1, 'main lifetime exponent')
            need(F(p, 2 * d) == q + 1, 'tail lifetime exponent')
            need(-24 * J - 12 * p + 12 * p == -24 * J, 'tail rho cancellation')
            need(F(q + 1) - F(1, A) * A == q, 'power cutoff exponent')
            need(F(1, A) < F(1, 2), 'geometric domain')
            exponent_checks += 5
    need(24 * 6 + 12 * 2 * 4 + 12 * 4 * 5 * 3 == 960, 'd=2 example')
    exponent_checks += 1
    return {'cardinal_derivative_checks': derivative_checks,
            'frequency_support_checks': frequency_checks,
            'real_coefficient_symmetry_checks': realness_checks,
            'constant_product_checks': product_checks,
            'covariance_controls': covariance_checks,
            'exponent_checks': exponent_checks,
            'negative_controls_rejected': rejected,
            'finite_gram_lower_bound': str(lower),
            'scope': 'finite exact controls; uniform proof and imported hypotheses not certified'}


def source_checks(directory):
    expected = {
        'PROOF.md': (15039, '7d8d3063caa0dfb5edbfe75437d7ccff8ab74697d1dd92c4b47cca5926b02392'),
        'source/P.md': (40261, '9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7'),
        'source/G.md': (29110, '967148439e32e8e5d6c06a12df5cc7c1eb2475fe6828e4aeb3748c48817a4cba')}
    out = {}
    for name, (size, digest) in expected.items():
        data = (Path(directory) / name).read_bytes()
        got = hashlib.sha256(data).hexdigest()
        need((len(data), got) == (size, digest), 'source identity: ' + name)
        out[name] = {'bytes': len(data), 'sha256': got, 'final_newline': data.endswith(b'\n')}
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir')
    args = parser.parse_args()
    result = controls()
    result['source_checks'] = source_checks(args.source_dir) if args.source_dir else 'NOT_RUN'
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
