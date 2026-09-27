"""Exact reciprocal of a declared finite polynomial times an integer power.

This is not an automatic replacement for unknown-tail truncated Laurent series.
No legacy engine is imported or modified.
"""
from fractions import Fraction
from typing import Sequence


def reciprocal_finite_polynomial(
    coefficients: Sequence[int | Fraction], offset: int = 0, through_power: int = 5
) -> tuple[int, tuple[Fraction, ...]]:
    """Return r**(-offset) coefficients of 1/(r**offset * P(r)).

    P is the COMPLETE finite polynomial with the supplied ascending coefficients.
    Its constant coefficient must be nonzero. Output contains exactly the terms
    with Laurent exponent <= through_power. Integers and Fractions only; no
    floating-point rounding or error-bound claim is introduced.
    """
    if type(offset) is not int or type(through_power) is not int:
        raise TypeError('offset and through_power must be integers, not booleans')
    if any(type(value) is not int and not isinstance(value, Fraction) for value in coefficients):
        raise TypeError('coefficients must be integers or Fractions')
    a = tuple(Fraction(value) for value in coefficients)
    if not a or a[0] == 0:
        raise ValueError('a normalized nonzero leading coefficient is required')
    n = max(0, through_power + offset + 1)
    if n == 0:
        return -offset, ()
    b = [1 / a[0]]
    m = len(a) - 1
    for k in range(1, n):
        convolution = sum(a[j] * b[k - j] for j in range(1, min(k, m) + 1))
        b.append(-convolution / a[0])
    return -offset, tuple(b)
