"""Exact finite controls only: no MF1/SC validation or field simulation."""

from fractions import Fraction as F
from itertools import product
from math import factorial
import unittest

import finite_checks as fc


def coefficient_product(left, right):
    """Independent oracle: evaluate PGF products, then Newton-interpolate.

    This never forms pairs of measure atoms. Exact product evaluations at
    degree+1 distinct integers determine the polynomial coefficients.
    """
    degree = max(left, default=0) + max(right, default=0)
    values = [
        sum(q * x**n for n, q in left.items())
        * sum(q * x**n for n, q in right.items())
        for x in range(degree + 1)
    ]
    coefficients = [F(0)] * (degree + 1)
    basis = [F(1)]  # binomial(x, 0)
    for j in range(degree + 1):
        for n, q in enumerate(basis):
            coefficients[n] += values[0] * q
        values = [b - a for a, b in zip(values, values[1:])]
        next_basis = [F(0)] * (len(basis) + 1)
        for n, q in enumerate(basis):
            next_basis[n] -= F(j, j + 1) * q
            next_basis[n + 1] += F(1, j + 1) * q
        basis = next_basis
    return {n: q for n, q in enumerate(coefficients) if q}


class PositiveFiniteControls(unittest.TestCase):
    def test_original_probability_and_zero_centering(self):
        """An omitted negative atom at zero must fail this control."""
        for m in (3, 4, 8, 12):
            eta = F(1, m * 2**m)
            nu = {1: F(1), 2: F(1), m: eta}
            self.assertEqual(fc.escaping_intensity(m), nu)
            centered = fc.center(nu)
            self.assertEqual(sum(centered.values()), 0)
            delta = F(1, 128 * m)
            law = fc.probability_from_intensity(nu, delta)
            self.assertEqual(sum(law.values()), 1)
            self.assertGreater(law[0], 0)
            self.assertTrue(all(q >= 0 for q in law.values()))
            self.assertEqual(law[m], delta * eta)
            scaled = {n: q / delta for n, q in law.items()}
            scaled[0] -= 1 / delta
            self.assertEqual(scaled, centered)
            self.assertEqual(centered[0], -(2 + eta))

    def test_endpoint_errors_and_distinct_normalizers(self):
        """Omitting n in size bias, or equating its denominator with a, fails."""
        limit = {1: F(1), 2: F(1)}
        for m in (3, 4, 8, 12):
            nu = fc.escaping_intensity(m)
            eta = F(1, m * 2**m)
            a, z = sum(nu.values()), sum(n * q for n, q in nu.items())
            self.assertEqual(a, 2 + eta)
            self.assertEqual(z, 3 + F(1, 2**m))
            self.assertNotEqual(a, z)
            self.assertEqual(fc.weighted_norm(fc.subtract(nu, limit)), F(1, m))
            centered_error = fc.weighted_norm(
                fc.subtract(fc.center(nu), fc.center(limit))
            )
            self.assertEqual(centered_error, F(1, m) + eta)
            self.assertLessEqual(centered_error, F(2, m))
            ordinary, biased = fc.positive_conditioned(nu), fc.size_biased(nu)
            self.assertEqual(sum(ordinary.values()), 1)
            self.assertEqual(sum(biased.values()), 1)
            self.assertEqual(ordinary[1], 1 / a)
            self.assertEqual(biased[1], 1 / z)
            self.assertEqual(biased[2], 2 / z)
            self.assertEqual(2**m * ordinary[m], 1 / (m * a))
            self.assertEqual(2**m * biased[m], 1 / z)
            self.assertGreaterEqual(2**m * biased[m], F(1, 4))

    def test_retained_n_factor_certifies_endpoint_tail(self):
        """Replacing the first weighted moment by the zeroth breaks E6."""
        for m in (3, 4, 8, 12):
            nu = fc.escaping_intensity(m)
            first_moment = sum(n * 2**n * q for n, q in nu.items())
            self.assertEqual(first_moment, 11)
            for cutoff in (1, 2, m - 1, m, m + 1):
                tail = sum(2**n * q for n, q in nu.items() if n > cutoff)
                fc.check_upper(tail, F(11, cutoff + 1), "E6 endpoint tail")

    def test_signed_convolution_against_coefficient_product(self):
        """Lost signs, missed coefficients and a wrong weight fail the oracle."""
        measures = [
            {n: q for n, q in enumerate(entries) if q}
            for entries in product((F(-2, 3), F(0), F(1, 2)), repeat=3)
        ]
        for left, right in product(measures, repeat=2):
            convolution = fc.convolve(left, right)
            self.assertEqual(convolution, coefficient_product(left, right))
            fc.check_upper(
                fc.weighted_norm(convolution),
                fc.weighted_norm(left) * fc.weighted_norm(right),
                "E11 signed convolution",
            )
        cancellation = fc.convolve({0: F(1), 1: F(-1)}, {0: F(1), 1: F(1)})
        self.assertEqual(cancellation, {0: F(1), 2: F(-1)})
        self.assertEqual(fc.weighted_norm(cancellation), 5)

    def test_taylor_polynomial_remainder_and_mass_are_explicit(self):
        """Dropping the tail or treating every Taylor polynomial as a law fails."""
        generator = {0: F(-1), 1: F(1)}
        polynomial = fc.exp_polynomial(generator, F(1, 16), order=2)
        self.assertEqual(polynomial, {0: F(481, 512), 1: F(15, 256), 2: F(1, 512)})
        self.assertEqual(sum(polynomial.values()), 1)  # centered cancellation
        positive_polynomial = fc.exp_polynomial({1: F(1), 2: F(1)}, F(1, 128), 8)
        positive_mass = sum(positive_polynomial.values())
        expected_mass = sum(F(1, 64)**j / factorial(j) for j in range(9))
        self.assertEqual(positive_mass, expected_mass)
        self.assertNotEqual(positive_mass, 1)
        self.assertGreater(F(1, 64)**9 / factorial(9), 0)  # omitted CP-series mass
        for x in (F(0), F(1, 16), F(1, 4)):
            for order in (0, 2, 8):
                remainder = fc.scalar_tail_bound(x, order)
                tail_prefix = sum(x**j / factorial(j) for j in range(order + 1, order + 10))
                self.assertGreaterEqual(remainder, tail_prefix)
                self.assertEqual(fc.scalar_exp_prefix(x, order), sum(x**j / factorial(j) for j in range(order + 1)))

    def test_one_copy_euler_error_with_infinite_tail_allowance(self):
        """E13 comparison adds a rigorous remainder instead of truncating truth."""
        bound = F(22)  # B=2C, C=11 in these escaping-mass fixtures.
        for m in (3, 4, 8, 12):
            nu, delta = fc.escaping_intensity(m), F(1, 128 * m)
            generator = fc.center(nu)
            x = delta * fc.weighted_norm(generator)
            self.assertLessEqual(x, F(1, 4))
            law = fc.probability_from_intensity(nu, delta)
            polynomial = fc.exp_polynomial(generator, delta, 8)
            certified_error = fc.weighted_norm(fc.subtract(law, polynomial)) + fc.scalar_tail_bound(x, 8)
            # A lower scalar enclosure makes this a stronger finite check.
            e13_lower = delta**2 * bound**2 * fc.scalar_exp_prefix(delta * bound, 8) / 2
            fc.check_upper(certified_error, e13_lower, "E13 with Taylor remainder")

    def test_actual_replica_convolution_and_floor_ledger(self):
        """Wrong replica multiplication or omitting m=floor(t/delta) fails."""
        bound = F(22)
        for escape_m in (3, 4, 8, 12):
            nu = fc.escaping_intensity(escape_m)
            delta = F(1, 128 * escape_m)
            generator = fc.center(nu)
            for t in (F(0), delta / 2, 2 * delta, 7 * delta / 3):
                copies = t // delta
                law = fc.replica_law(nu, delta, t)
                one_copy = fc.probability_from_intensity(nu, delta)
                self.assertEqual(law, fc.convolution_power(one_copy, copies))
                self.assertEqual(sum(law.values()), 1)
                self.assertGreaterEqual(t - copies * delta, 0)
                self.assertLess(t - copies * delta, delta)
                s = copies * delta
                polynomial = fc.exp_polynomial(generator, s, 8)
                x = s * fc.weighted_norm(generator)
                self.assertLessEqual(x, F(1, 4))
                certified_error = fc.weighted_norm(fc.subtract(law, polynomial)) + fc.scalar_tail_bound(x, 8)
                e14_lower = copies * delta**2 * bound**2 * fc.scalar_exp_prefix(s * bound, 8) / 2
                fc.check_upper(certified_error, e14_lower, "E14 with Taylor remainder")
        bernoulli = {0: F(7, 8), 1: F(1, 8)}
        self.assertEqual(fc.convolution_power(bernoulli, 2), {0: F(49, 64), 1: F(7, 32), 2: F(1, 64)})
        self.assertEqual(fc.convolution_power(bernoulli, 0), {0: F(1)})

    def test_e12_actual_laws_against_limit_exponential_with_remainder(self):
        """Endpoint mark error, floor and infinite-series tail all enter E12."""
        limit = {1: F(1), 2: F(1)}
        generator = fc.center(limit)
        bound, horizon = F(22), F(1, 100)
        self.assertLessEqual(horizon * bound, F(1, 4))
        exponential_lower = fc.scalar_exp_prefix(horizon * bound, 8)
        for m in (3, 4, 8, 12):
            nu, delta = fc.escaping_intensity(m), F(1, 128 * m)
            epsilon = fc.weighted_norm(fc.subtract(nu, limit))
            self.assertEqual(epsilon, F(1, m))
            for t in (F(0), delta / 2, 2 * delta, 7 * delta / 3):
                self.assertLessEqual(t, horizon)
                actual = fc.replica_law(nu, delta, t)
                polynomial = fc.exp_polynomial(generator, t, 8)
                x = t * fc.weighted_norm(generator)
                certified_error = fc.weighted_norm(fc.subtract(actual, polynomial)) + fc.scalar_tail_bound(x, 8)
                e12_lower = exponential_lower * (
                    delta * (horizon * bound**2 / 2 + bound) + 2 * horizon * epsilon
                )
                fc.check_upper(certified_error, e12_lower, "E12 with Taylor remainder")


class IntendedNegativeControls(unittest.TestCase):
    NEGATIVE_CONTROL = True

    def test_reject_omitted_zero_centering(self):
        """Deliberately wrong generator nu must be rejected as noncentered."""
        wrong_generator = fc.escaping_intensity(8)
        with self.assertRaisesRegex(fc.ControlFailure, "zero-centering"):
            fc.check_zero_mass(wrong_generator, "omitted-zero-centering")

    def test_reject_omitted_n_factor(self):
        """A bounded zeroth weighted moment cannot justify the endpoint tail."""
        m = 16
        wrong_intensity = {1: F(1), 2: F(1), m: F(1, 2**m)}
        wrong_constant = fc.weighted_norm(wrong_intensity)
        self.assertEqual(wrong_constant, 7)
        self.assertEqual(sum(n * 2**n * q for n, q in wrong_intensity.items()), 26)
        with self.assertRaisesRegex(fc.ControlFailure, "omitted-n-factor"):
            fc.check_upper(F(1), wrong_constant / m, "omitted-n-factor")

    def test_reject_endpoint_size_bias_convergence_inference(self):
        """The false extension of the intensity's 2/m bound is rejected."""
        limit_biased = {1: F(1, 3), 2: F(2, 3)}
        for m in (16, 32, 64):
            biased = fc.size_biased(fc.escaping_intensity(m))
            error = fc.weighted_norm(fc.subtract(biased, limit_biased))
            self.assertGreaterEqual(error, F(1, 4))
            with self.assertRaisesRegex(fc.ControlFailure, "endpoint-size-bias"):
                fc.check_upper(error, F(2, m), "endpoint-size-bias")

    def test_reject_coupled_replicas_as_independent(self):
        """Perfectly coupled Bernoulli copies omit the positive middle atom."""
        coupled_sum = {0: F(7, 8), 2: F(1, 8)}
        independent_sum = {0: F(49, 64), 1: F(7, 32), 2: F(1, 64)}
        self.assertEqual(fc.weighted_norm(fc.subtract(coupled_sum, independent_sum)), F(63, 64))
        with self.assertRaisesRegex(fc.ControlFailure, "coupled-replicas"):
            fc.check_equal(coupled_sum, independent_sum, "coupled-replicas")


if __name__ == "__main__":
    unittest.main()
