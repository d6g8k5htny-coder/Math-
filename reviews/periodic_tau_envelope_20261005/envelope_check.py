"""Exact rational consequences of REPORT.md, not a Lean or interval certificate.

Run with Python's standard library, normally or under -O. Exit codes:
0 = all finite controls pass, 1 = a named mathematical control fails,
2 = invalid arguments. M1--M4 intentionally corrupt the tested formulas.
"""
import argparse
from fractions import Fraction as F
import itertools
import json
from typing import Iterable


def exact(x: int | str | F) -> F:
    """Reject floats: a decimal string means its exact rational value only."""
    if isinstance(x, bool) or not isinstance(x, (int, str, F)):
        raise TypeError('use int, Fraction, or an exact rational string')
    return F(x)


def dimension(d: int) -> None:
    if isinstance(d, bool) or not isinstance(d, int):
        raise TypeError('dimension must be an integer')
    if d < 1:
        raise ValueError('dimension must be positive')


def simplex(x: Iterable[int | str | F]) -> tuple[F, ...]:
    values = tuple(exact(t) for t in x)
    if not values or any(t < 0 for t in values) or sum(values) != 1:
        raise ValueError('simplex coordinates must be nonnegative and sum to one')
    return values


def support_values(d: int, A: int | str | F, B: int | str | F,
                   mode: str | None = None) -> tuple[F, ...]:
    dimension(d)
    A, B = exact(A), exact(B)
    values = tuple(A/m + B/(m if mode == 'M4' else m*m) for m in range(1, d+1))
    if mode == 'M1' and d > 2:
        return values[0], values[-1]  # deliberately omits intermediate supports
    return values


def envelope(d: int, A: int | str | F, B: int | str | F,
             mode: str | None = None) -> tuple[F, F]:
    values = support_values(d, A, B, mode)
    return min(values), max(values)


def polynomial(x: Iterable[int | str | F], A: int | str | F,
               B: int | str | F) -> F:
    x, A, B = simplex(x), exact(A), exact(B)
    return A*sum(t*t for t in x) + B*sum(t*t*t for t in x)


def tau_coefficients(a: int | str | F, b: int | str | F,
                     c: int | str | F, mode: str | None = None) -> tuple[F, F]:
    a, b, c = exact(a), exact(b), exact(c)
    if a <= 0:
        raise ValueError('second spectral cumulant must be positive')
    return (15 if mode == 'M3' else 9)*a*b, c if mode == 'M2' else c-b*b/a


def tau_polynomial(x: Iterable[int | str | F], a: int | str | F,
                   b: int | str | F, c: int | str | F,
                   mode: str | None = None) -> F:
    a = exact(a)
    A, B = tau_coefficients(a, b, c, mode)
    return 6*a**3 + polynomial(x, A, B)


def tau_envelope(d: int, a: int | str | F, b: int | str | F,
                 c: int | str | F) -> tuple[F, F]:
    a = exact(a)
    A, B = tau_coefficients(a, b, c)
    lo, hi = envelope(d, A, B)
    return 6*a**3+lo, 6*a**3+hi


def test_cumulants() -> tuple[F, F, F]:
    atoms = (-2, -1, 1, 2)
    a, m4, m6 = (sum(F(t)**j for t in atoms)/len(atoms) for j in (2, 4, 6))
    return a, m4-3*a*a, m6-15*m4*a+30*a**3


def test_directions() -> tuple[tuple[F, ...], ...]:
    return ((F(1), F(0)), (F(3, 5), F(4, 5)),
            (F(1), F(0), F(0)), (F(1, 3), F(2, 3), F(2, 3)),
            (F(1, 2),)*4, (F(-1, 2), F(1, 2), F(-1, 2), F(1, 2)))


def direct_spectral_regression(u: tuple[F, ...]) -> F:
    """Independent finite-atom E[Y^6]-sum_i E[Y^3 xi_i]^2/a oracle."""
    if sum(t*t for t in u) != 1:
        raise ValueError('test direction must have unit length')
    atoms = tuple(itertools.product((-2, -1, 1, 2), repeat=len(u)))
    sixth = F(0)
    cross = [F(0)]*len(u)
    for xi in atoms:
        y = sum(t*s for t, s in zip(u, xi))
        sixth += y**6
        for i in range(len(u)):
            cross[i] += y**3*xi[i]
    sixth /= len(atoms)
    cross = [v/len(atoms) for v in cross]
    return sixth-sum(v*v for v in cross)/F(5, 2)


def diagnostics(mode: str | None = None) -> dict:
    if mode not in (None, 'M1', 'M2', 'M3', 'M4'):
        raise ValueError('unknown mutant')
    a, b, c = test_cumulants()
    A, B = tau_coefficients(a, b, c, mode)
    checks = {
        'intermediate_support': envelope(3, 1, -1, mode) == (F(0), F(1, 4)),
        'support_scaling': support_values(4, 2, -3, mode) == (F(-1), F(1, 4), F(1, 3), F(5, 16)),
        'conditioning': B == c-b*b/a,
        'fourth_cumulant_coefficient': A == 9*a*b,
        'finite_spectral_regression': all(
            tau_polynomial(tuple(t*t for t in u), a, b, c, mode) == direct_spectral_regression(u)
            for u in test_directions()),
        'flat_two_coordinate_edge': all(polynomial((F(j, 10), 1-F(j, 10)), -3, 2) == -1
                                        for j in range(11)),
    }
    values = support_values(4, 9*a*b, c-b*b/a)
    return {'object': 'PERIODIC-TAU-ENVELOPE-20261005', 'scientific_effect': 'NONE',
            'mutant': mode, 'checks': checks, 'passed': all(checks.values()),
            'finite_spectrum_cumulants': [str(a), str(b), str(c)],
            'tau_support_values_d4': [str(6*a**3+v) for v in values],
            'limits': 'Exact rational controls only; no Gaussian realization, image-sum or Lean certificate.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant', choices=('M1', 'M2', 'M3', 'M4'))
    args = parser.parse_args()
    result = diagnostics(args.mutant)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
