"""Deterministic exact finite algebra controls for the conditional EW packet.

All arithmetic is rational at alpha=1 and theta=log(2), so w(n)=2**n.
These controls validate selected finite identities and inequalities only.
They do not prove MF1, SC, a coefficient rate, or any field independence.
No source-cache content is read or exported by this module.

Run ``python finite_checks.py`` (also with ``-O``) for one small JSON result.
The only intended failures are the four named variants in the test module.
"""

from fractions import Fraction
from io import StringIO
import json
from math import factorial
import sys
import unittest


class ControlFailure(ValueError):
    """An explicit finite invariant failed; never relies on Python assert."""


def require(condition, label):
    if not condition:
        raise ControlFailure(label)


def rational(value):
    require(isinstance(value, (int, Fraction)), "exact rational required")
    return Fraction(value)


def canonical(measure):
    result = {}
    for n, coefficient in measure.items():
        require(isinstance(n, int) and n >= 0, "nonnegative integer atom required")
        coefficient = rational(coefficient)
        if coefficient:
            result[n] = coefficient
    return result


def add(left, right):
    result = canonical(left)
    for n, q in canonical(right).items():
        result[n] = result.get(n, Fraction(0)) + q
    return canonical(result)


def scale(measure, scalar):
    scalar = rational(scalar)
    return canonical({n: scalar * q for n, q in canonical(measure).items()})


def subtract(left, right):
    return add(left, scale(right, -1))


def weighted_norm(measure):
    return sum((2**n * abs(q) for n, q in canonical(measure).items()), Fraction(0))


def positive_intensity(intensity):
    intensity = canonical(intensity)
    require(all(n >= 1 and q >= 0 for n, q in intensity.items()), "positive intensity required")
    return intensity


def center(intensity):
    intensity = positive_intensity(intensity)
    return add(intensity, {0: -sum(intensity.values(), Fraction(0))})


def probability_from_intensity(intensity, delta):
    delta = rational(delta)
    require(delta > 0, "delta must be positive")
    law = add({0: Fraction(1)}, scale(center(intensity), delta))
    require(all(q >= 0 for q in law.values()), "one-copy law must be nonnegative")
    check_equal(sum(law.values(), Fraction(0)), Fraction(1), "one-copy probability mass")
    return law


def escaping_intensity(m):
    require(isinstance(m, int) and m >= 3, "escaping atom m must be at least 3")
    return {1: Fraction(1), 2: Fraction(1), m: Fraction(1, m * 2**m)}


def positive_conditioned(intensity):
    intensity = positive_intensity(intensity)
    normalizer = sum(intensity.values(), Fraction(0))
    require(normalizer > 0, "positive-conditioned normalizer")
    return scale(intensity, 1 / normalizer)


def size_biased(intensity):
    intensity = positive_intensity(intensity)
    biased = {n: n * q for n, q in intensity.items()}
    normalizer = sum(biased.values(), Fraction(0))
    require(normalizer > 0, "size-biased normalizer")
    return scale(biased, 1 / normalizer)


def convolve(left, right):
    result = {}
    for n, q in canonical(left).items():
        for k, p in canonical(right).items():
            result[n + k] = result.get(n + k, Fraction(0)) + q * p
    return canonical(result)


def convolution_power(measure, exponent):
    require(isinstance(exponent, int) and exponent >= 0, "nonnegative replica count required")
    result, base = {0: Fraction(1)}, canonical(measure)
    while exponent:
        if exponent % 2:
            result = convolve(result, base)
        exponent //= 2
        if exponent:
            base = convolve(base, base)
    return result


def replica_law(intensity, delta, t):
    delta, t = rational(delta), rational(t)
    require(delta > 0 and t >= 0, "replica time and delta")
    # This operation encodes deliberately independent replicas only.
    return convolution_power(probability_from_intensity(intensity, delta), t // delta)


def exp_polynomial(generator, t, order=8):
    """Signed convolution Taylor polynomial, not an infinite CP law.

    Its mass is exactly 1 when the generator has total mass zero, by
    cancellation. For an uncentered positive generator even this mass
    statement fails. The remainder must be added to every comparison
    with exp_*(t*generator).
    """
    t = rational(t)
    require(t >= 0 and isinstance(order, int) and order >= 0, "Taylor time and order")
    argument = scale(generator, t)
    total = term = {0: Fraction(1)}
    for j in range(1, order + 1):
        term = scale(convolve(term, argument), Fraction(1, j))
        total = add(total, term)
    return total


def scalar_exp_prefix(x, order=8):
    x = rational(x)
    require(x >= 0 and isinstance(order, int) and order >= 0, "scalar Taylor argument and order")
    return sum((x**j / factorial(j) for j in range(order + 1)), Fraction(0))


def scalar_tail_bound(x, order=8):
    """Rigorous rational upper bound for sum_(j>order) x**j/j!.

    The first omitted term is x**(order+1)/(order+1)!. Each subsequent
    ratio is at most x/(order+2), so a geometric series bounds the entire
    infinite scalar tail when that ratio is below 1. Submultiplicativity
    then bounds the omitted convolution tail at x=||t*generator||_w.
    Fixtures keep x<=1/4 and use the fixed order 8 for replica comparisons;
    no floating-point exponential or adaptive digit refinement is used.
    """
    x = rational(x)
    require(x >= 0 and isinstance(order, int) and order >= 0, "scalar remainder argument and order")
    ratio = x / (order + 2)
    require(ratio < 1, "geometric scalar remainder requires ratio below 1")
    return x**(order + 1) / factorial(order + 1) / (1 - ratio)


def check_zero_mass(measure, label):
    require(sum(canonical(measure).values(), Fraction(0)) == 0, label)


def check_upper(actual, upper, label):
    require(actual <= upper, label)


def check_equal(actual, expected, label):
    require(actual == expected, label)


def run_controls():
    import test_finite_checks

    suite = unittest.defaultTestLoader.loadTestsFromModule(test_finite_checks)

    def flatten(tests):
        for test in tests:
            if isinstance(test, unittest.TestSuite):
                yield from flatten(test)
            else:
                yield test

    tests = list(flatten(suite))
    negative_ids = {test.id() for test in tests if getattr(test, "NEGATIVE_CONTROL", False)}
    diagnostics = StringIO()
    result = unittest.TextTestRunner(stream=diagnostics, verbosity=0).run(suite)
    failed_ids = {test.id() for test, _ in result.failures + result.errors}
    summary = {
        "all_passed": result.wasSuccessful(),
        "checks": result.testsRun,
        "failed": len(failed_ids),
        "positive_controls": len(tests) - len(negative_ids),
        "intended_negative_controls": len(negative_ids),
        "intended_negative_controls_rejected": len(negative_ids - failed_ids),
        "scientific_effect": "NONE",
        "scope": "finite_algebra_only",
    }
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
    if not result.wasSuccessful():
        sys.stderr.write(diagnostics.getvalue())
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_controls())
