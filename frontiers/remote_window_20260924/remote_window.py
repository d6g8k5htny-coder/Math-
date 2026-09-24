"""Exact finite controls for the fixed-remote height-window argument.

This module does not evaluate a Gaussian-field Kac-Rice integral or certify its
continuum estimates. Inputs are integers/Fractions, not sampled floating data.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from math import factorial
import json
from typing import Iterable

Matrix = tuple[tuple[Q, ...], ...]


def exact(value: int | Q) -> Q:
    if type(value) is int or isinstance(value, Q):
        return Q(value)
    raise TypeError('an integer or Fraction is required; floats/bools are refused')


def matrix(rows: Iterable[Iterable[int | Q]]) -> Matrix:
    result = tuple(tuple(exact(x) for x in row) for row in rows)
    if not 1 <= len(result) <= 12 or any(len(row) != len(result) for row in result):
        raise ValueError('a square matrix of order 1 through 12 is required')
    return result


def symmetric(rows: Iterable[Iterable[int | Q]]) -> Matrix:
    a = matrix(rows)
    if any(a[i][j] != a[j][i] for i in range(len(a)) for j in range(len(a))):
        raise ValueError('symmetric matrix required')
    return a


def determinant(rows: Iterable[Iterable[int | Q]]) -> Q:
    a = [list(row) for row in matrix(rows)]
    out = Q(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i]), None)
        if pivot is None:
            return Q(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            out = -out
        value = a[i][i]
        out *= value
        for j in range(i + 1, len(a)):
            scale = a[j][i] / value
            for k in range(i + 1, len(a)):
                a[j][k] -= scale * a[i][k]
    return out


def inertia(rows: Iterable[Iterable[int | Q]]) -> tuple[int, int, int]:
    """Return (negative, zero, positive) counts by exact symmetric congruences."""
    a = [list(row) for row in symmetric(rows)]
    neg = zero = pos = 0
    while a:
        n = len(a)
        pivot = next((i for i in range(n) if a[i][i]), None)
        if pivot is not None:
            order = [pivot] + [i for i in range(n) if i != pivot]
            a = [[a[i][j] for j in order] for i in order]
            v = a[0][0]
            neg += int(v < 0)
            pos += int(v > 0)
            a = [[a[i][j] - a[i][0] * a[0][j] / v
                  for j in range(1, n)] for i in range(1, n)]
            continue
        pair = next(((i, j) for i in range(n) for j in range(i + 1, n) if a[i][j]), None)
        if pair is None:
            zero += n
            break
        i, j = pair
        order = [i, j] + [k for k in range(n) if k not in (i, j)]
        a = [[a[i][j] for j in order] for i in order]
        v = a[0][1]  # the 2x2 block [[0,v],[v,0]] has one of each sign
        neg += 1
        pos += 1
        a = [[a[i][j] - (a[i][0] * a[1][j] + a[i][1] * a[0][j]) / v
              for j in range(2, n)] for i in range(2, n)]
    return neg, zero, pos


def typed_det(rows: Iterable[Iterable[int | Q]], index: int) -> Q:
    a = symmetric(rows)
    if type(index) is not int or not 0 <= index <= len(a):
        raise ValueError('invalid negative index')
    return abs(determinant(a)) if inertia(a)[0] == index else Q(0)


def block(alpha: int | Q, beta: Iterable[int | Q], a_rows: Iterable[Iterable[int | Q]], root_t: int | Q) -> Matrix:
    a = symmetric(a_rows)
    b = tuple(exact(x) for x in beta)
    s = exact(root_t)
    if len(b) != len(a) or s < 0:
        raise ValueError('wrong beta dimension or negative square root')
    return matrix(((exact(alpha), *(s*x for x in b)),
                   *((s*b[i], *a[i]) for i in range(len(a)))))


def quadratic_slope(a_rows: Iterable[Iterable[int | Q]], beta: Iterable[int | Q]) -> Q:
    # -det([[0,beta^T],[beta,A]])=beta^T adj(A) beta, even when A is singular.
    return -determinant(block(0, beta, a_rows, 1))


def block_bound(alpha: int | Q, beta: Iterable[int | Q], a: Iterable[Iterable[int | Q]], root_t: int | Q, index: int) -> dict[str, Q | bool]:
    aa = symmetric(a)
    bb = tuple(exact(x) for x in beta)
    s = exact(root_t)
    lhs = abs(typed_det(block(alpha, bb, aa, s), index) - typed_det(block(alpha, bb, aa, 0), index))
    rhs = s*s*abs(quadratic_slope(aa, bb))
    return {'lhs': lhs, 'rhs': rhs, 'holds': lhs <= rhs}


def inverse(rows: Iterable[Iterable[int | Q]]) -> Matrix:
    a0 = matrix(rows)
    n = len(a0)
    a = [list(row) + [Q(i == j) for j in range(n)] for i, row in enumerate(a0)]
    for i in range(n):
        p = next((j for j in range(i, n) if a[j][i]), None)
        if p is None:
            raise ValueError('singular covariance block')
        a[i], a[p] = a[p], a[i]
        v = a[i][i]
        a[i] = [x/v for x in a[i]]
        for j in range(n):
            if j != i:
                s = a[j][i]
                a[j] = [x-s*y for x, y in zip(a[j], a[i])]
    return matrix(row[n:] for row in a)


def conditional(covariance: Iterable[Iterable[int | Q]], target: Iterable[int | Q]) -> tuple[tuple[Q, ...], Matrix]:
    """Conditional mean/covariance of remaining centered coordinates given a prefix."""
    c = symmetric(covariance)
    v = tuple(exact(x) for x in target)
    k, n = len(v), len(c)
    if not 1 <= k < n or inertia(c) != (0, 0, n):
        raise ValueError('nonempty proper prefix and positive covariance required')
    inv = inverse(row[:k] for row in c[:k])
    b = [[sum(c[i][s]*inv[s][t] for s in range(k)) for t in range(k)] for i in range(k, n)]
    mu = tuple(sum(row[t]*v[t] for t in range(k)) for row in b)
    residual = symmetric([[c[i][j]-sum(b[i-k][t]*c[t][j] for t in range(k))
                           for j in range(k, n)] for i in range(k, n)])
    return mu, residual


def square_product_moment(var_x: int | Q, var_y: int | Q, covariance: int | Q) -> Q:
    x, y, c = map(exact, (var_x, var_y, covariance))
    if x < 0 or y < 0 or c*c > x*y:
        raise ValueError('invalid covariance')
    return x*y + 2*c*c


def pin_transform(dimension: int, radius: int | Q) -> Matrix:
    if type(dimension) is not int or not 2 <= dimension <= 5:
        raise ValueError('finite helper supports dimensions 2 through 5')
    r = exact(radius)
    if r <= 0:
        raise ValueError('positive radius required')
    n = 2*(dimension+1)
    t = [[Q(0) for _ in range(n)] for _ in range(n)]
    t[0][:4] = [Q(1,2),0,Q(1,2),0]
    t[1][:4] = [-1/r,0,1/r,0]
    t[2][:4] = [0,-1/r,0,1/r]
    t[3][:4] = [12/r**3,6/r**2,-12/r**3,6/r**2]
    for j in range(dimension-1):
        k = 4+2*j
        t[k][k:k+2] = [Q(1,2),Q(1,2)]
        t[k+1][k:k+2] = [-1/r,1/r]
    return matrix(t)


def transformed_target(dimension: int, radius: int | Q, birth: int | Q, gap_mark: int | Q) -> tuple[Q, ...]:
    r, b, k = map(exact, (radius, birth, gap_mark))
    if k <= 0:
        raise ValueError('positive gap mark required')
    v = (b, Q(0), b-k*r**3, Q(0), *(Q(0) for _ in range(2*(dimension-1))))
    return tuple(sum(x*y for x,y in zip(row,v)) for row in pin_transform(dimension,r))


def window_length(radius: int | Q, gap_mark: int | Q) -> Q:
    r, k = exact(radius), exact(gap_mark)
    if r <= 0 or k <= 0:
        raise ValueError('radius and gap mark must be positive')
    return k*r**3


def window_polynomial(coefficients: Iterable[int | Q], radius: int | Q, gap_mark: int | Q) -> Q:
    """Integrate a polynomial in depth below birth over the exact height window."""
    coeff = tuple(exact(x) for x in coefficients)
    if len(coeff) > 20:
        raise ValueError('polynomial degree exceeds finite helper limit')
    length = window_length(radius, gap_mark)
    return sum((c*length**(i+1)/Q(i+1) for i,c in enumerate(coeff)), Q(0))


def count_ledger(witnesses: int) -> dict[str, int]:
    if type(witnesses) is not int or not 1 <= witnesses <= 8:
        raise ValueError('finite ledger supports 1 through 8 witnesses')
    numerator_power = 2 + 3*witnesses
    normalizer_power = 2
    return {'witnesses': witnesses, 'determinant_factors': witnesses+2,
            'endpoint_weights': 1, 'normalizers': 1,
            'numerator_power': numerator_power,
            'mean_power': numerator_power-normalizer_power,
            'unordered_divisor': factorial(witnesses)}


@dataclass(frozen=True)
class FixedRemoteScope:
    dimension: int
    side: Q
    exclusion_radius: Q

    def __post_init__(self) -> None:
        if type(self.dimension) is not int or not 2 <= self.dimension <= 5:
            raise ValueError('finite helper dimension limit')
        side, rho = exact(self.side), exact(self.exclusion_radius)
        if not 0 < rho < side/4:
            raise ValueError('fixed 0<rho<L/4 required')
        object.__setattr__(self, 'side', side)
        object.__setattr__(self, 'exclusion_radius', rho)

    def check_radius(self, radius: int | Q) -> None:
        if not 0 < exact(radius) <= self.exclusion_radius:
            raise ValueError('radius lies outside this fixed exclusion contract')

    def distance_squared(self, x: Iterable[int | Q], y: Iterable[int | Q]) -> Q:
        xx, yy = tuple(map(exact,x)), tuple(map(exact,y))
        if len(xx) != self.dimension or len(yy) != self.dimension:
            raise ValueError('point dimension mismatch')
        return sum((min((a-b)%self.side, self.side-(a-b)%self.side)**2 for a,b in zip(xx,yy)), Q(0))

    def contains(self, x: Iterable[int | Q]) -> bool:
        return self.distance_squared(x, (0,)*self.dimension) >= self.exclusion_radius**2

    def tuple_allowed(self, points: Iterable[Iterable[int | Q]], separation: int | Q) -> bool:
        pts = tuple(tuple(p) for p in points)
        eta = exact(separation)
        if not 1 <= len(pts) <= 8 or eta <= 0:
            raise ValueError('finite tuple and positive fixed separation required')
        return (all(self.contains(p) for p in pts)
                and all(self.distance_squared(pts[i],pts[j]) >= eta**2
                        for i in range(len(pts)) for j in range(i)))


def result() -> dict:
    return {'object':'RN-FIXED-REMOTE-WINDOW-20260924-v1',
            'single_witness': count_ledger(1), 'separated_pair': count_ledger(2),
            'sample_exact_window':str(window_length(Q(1,10),Q(1,6))),
            'scope':'Fixed positive spatial exclusion; shrinking between-pin height window; compact birth and positive gap marks',
            'candidate_statement':'E_QW N_j(E)=k*r^3*integral_E Lambda_j + O(k*r^4*volume(E))',
            'separated_tuple_statement':'For fixed m and positive mutual separation, E ordered T_m=(k*r^3)^m*C_m+O(r^(3*m+1))',
            'gaussian_integral_numerically_evaluated':False,
            'legacy_RN_24jet_discharged':False, 'independent_analytic_acceptance':False}


if __name__ == '__main__':
    print(json.dumps(result(), indent=2, sort_keys=True))
