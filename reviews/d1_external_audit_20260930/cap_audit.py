"""Exact finite controls for the D1 cap audit (not a continuum proof checker).

Standard-library rational polynomial calculations and two independent finite-graph
algorithms. Deterministic bounds and topology are reconstructed in AUDIT.md;
Gaussian interfaces are separate inputs, not established by executing this module.
"""
from fractions import Fraction as F
import json


def rational(x):
    if type(x) not in (int, F):
        raise TypeError('exact int or Fraction required')
    return F(x)


def clean(poly):
    return {tuple(i): rational(a) for i, a in poly.items() if a}


def variable(dim, axis):
    if type(dim) is not int or type(axis) is not int or not 0 <= axis < dim:
        raise ValueError('positive dimension and valid axis required')
    i = [0]*dim
    i[axis] = 1
    return {tuple(i): F(1)}


def add(*polys):
    out = {}
    for poly in polys:
        for i, a in poly.items():
            out[i] = out.get(i, F(0)) + a
    return clean(out)


def scale(poly, a):
    a = rational(a)
    return clean({i: a*b for i, b in poly.items()})


def multiply(left, right):
    out = {}
    for i, a in left.items():
        for j, b in right.items():
            if len(i) != len(j):
                raise ValueError('polynomial dimensions differ')
            k = tuple(x+y for x, y in zip(i, j))
            out[k] = out.get(k, F(0)) + a*b
    return clean(out)


def power(poly, n):
    if type(n) is not int or n < 0 or not poly:
        raise ValueError('nonempty polynomial and nonnegative integer power required')
    out = {tuple(0 for _ in next(iter(poly))): F(1)}
    for _ in range(n):
        out = multiply(out, poly)
    return out


def derivative(poly, axis):
    out = {}
    for i, a in poly.items():
        if type(axis) is not int or not 0 <= axis < len(i):
            raise ValueError('invalid derivative axis')
        if i[axis]:
            j = list(i)
            j[axis] -= 1
            out[tuple(j)] = a*i[axis]
    return clean(out)


def value(poly, point):
    point = tuple(map(rational, point))
    ans = F(0)
    for i, a in poly.items():
        if len(i) != len(point):
            raise ValueError('point dimension mismatch')
        term = a
        for degree, coordinate in zip(i, point):
            term *= coordinate**degree
        ans += term
    return ans


def integral(poly, lo, hi):
    lo, hi = map(rational, (lo, hi))
    if any(len(i) != 1 for i in poly):
        raise ValueError('one-variable polynomial required')
    return sum((a*(hi**(i[0]+1)-lo**(i[0]+1))/F(i[0]+1)
                for i, a in poly.items()), F(0))


def constants():
    k_min = F(11)
    slope = 2/k_min + 2/k_min**2
    m_slope = (1 + 6/k_min + 5/k_min**2)/4
    adverse = m_slope*(3 + 3*slope + slope*slope)
    quadratic = {(2,): F(1, 8), (0,): -F(1, 32)}
    drop = integral(quadratic, F(1, 2), F(2))
    delta_over_r = F(2)*k_min
    distance_over_r = 2 - 2/k_min
    return {
        'ridge_lower': F(7, 4)-adverse,
        'ridge_slope_upper': slope,
        'adverse_third_derivative': adverse,
        'axis_drop_normalized': drop,
        'axis_excess_normalized': drop-F(1, 6),
        'side_drop_normalized': delta_over_r*distance_over_r**2/2,
    }


def good_event(r, k, m3, m4, lam):
    """Check the displayed scalar sufficient inequalities, not bounds on a field."""
    r, k, m3, m4, lam = map(rational, (r, k, m3, m4, lam))
    if r <= 0 or k <= 0 or m3 < 0 or m4 < 0:
        raise ValueError('r,k positive and derivative bounds nonnegative required')
    return lam > F(4, 3)*r*m3*m3/k and r*m4 <= F(3, 10)*k


def diagonal_congruence(matrix, diag):
    n = len(diag)
    diag = list(map(rational, diag))
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError('square matrix/diagonal size mismatch')
    return [[diag[i]*rational(matrix[i][j])*diag[j] for j in range(n)] for i in range(n)]


def falsifier():
    f0 = {(3, 0): F(2), (1, 0): -F(3, 2), (0, 0): -F(1, 2),
          (0, 2): F(-128)}
    return f0, add(f0, {(0, 4): F(65536), (0, 5): F(1)})


def graph_data(weights, edges, start):
    if start not in weights:
        raise ValueError('missing start vertex')
    weights = {v: rational(w) for v, w in weights.items()}
    adj = {v: set() for v in weights}
    for a, b in edges:
        if a not in weights or b not in weights:
            raise ValueError('edge refers to absent vertex')
        adj[a].add(b)
        adj[b].add(a)
    return weights, adj


def graph_maximin(weights, edges, start):
    """Widest-path algorithm to any strictly older vertex; None means essential."""
    weights, adj = graph_data(weights, edges, start)
    score = {start: weights[start]}
    done = set()
    while True:
        candidates = [v for v in score if v not in done]
        if not candidates:
            return None
        v = max(candidates, key=lambda z: score[z])
        if weights[v] > weights[start]:
            return score[v]
        done.add(v)
        for w in adj[v]-done:
            bottleneck = min(score[v], weights[w])
            if w not in score or bottleneck > score[w]:
                score[w] = bottleneck


def graph_threshold_oracle(weights, edges, start):
    """Independent threshold-connectedness oracle; no widest-path labels."""
    weights, adj = graph_data(weights, edges, start)
    for threshold in sorted(set(weights.values()), reverse=True):
        if weights[start] < threshold:
            continue
        pending = [start]
        seen = {start}
        while pending:
            v = pending.pop()
            if weights[v] > weights[start]:
                return threshold
            for w in adj[v]:
                if w not in seen and weights[w] >= threshold:
                    seen.add(w)
                    pending.append(w)
    return None


def main():
    print(json.dumps({'scope': 'finite exact controls only; not D1 formal verification',
                      'scientific_effect': 'NONE',
                      'constants': {key: str(x) for key, x in constants().items()}},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
