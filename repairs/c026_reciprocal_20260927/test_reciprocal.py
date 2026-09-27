"""Exact behavior tests; no archived engine or external packages are imported."""
from fractions import Fraction as F
import importlib.util
from pathlib import Path
import unittest

class ReciprocalTests(unittest.TestCase):
    def reciprocal(self, coefficients, offset=0, through_power=5):
        path = Path(__file__).with_name('reciprocal.py')
        self.assertTrue(path.is_file(), 'finite-polynomial reciprocal implementation missing')
        spec = importlib.util.spec_from_file_location('reciprocal_under_test', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.reciprocal_finite_polynomial(coefficients, offset, through_power)

    def test_geometric_inverse_has_negative_linear_coefficient(self):
        self.assertEqual(self.reciprocal([1, 1]), (0, tuple(F((-1)**k) for k in range(6))))

    def test_positive_offset_needs_more_coefficients(self):
        self.assertEqual(self.reciprocal([1, 1], 3, 5), (-3, tuple(F((-1)**k) for k in range(9))))

    def test_negative_offset(self):
        self.assertEqual(self.reciprocal([1, 1], -2, 3), (2, (F(1), F(-1))))

    def test_cutoff_before_leading_power_is_empty(self):
        self.assertEqual(self.reciprocal([1, 1], -5, 3), (5, ()))

    def test_constant_polynomial(self):
        self.assertEqual(self.reciprocal([2], 2, 1), (-2, (F(1, 2), F(0), F(0), F(0))))

    def test_rational_coefficients(self):
        self.assertEqual(self.reciprocal([F(1, 2), 1], 0, 4), (0, tuple(F(2*(-2)**k) for k in range(5))))

    def test_product_coefficients_independently_cancel(self):
        for a0 in (-2, -1, 1, 2):
            for a1 in (-3, 0, 3):
                coefficients = [F(a0), F(a1), F(4, 3)]
                for offset in (-2, 0, 3):
                    with self.subTest(coefficients=coefficients, offset=offset):
                        inv_offset, b = self.reciprocal(coefficients, offset, 8)
                        self.assertEqual(inv_offset, -offset)
                        self.assertEqual(len(b), 9+offset)
                        for k in range(len(b)):
                            coefficient = sum(coefficients[j]*b[k-j] for j in range(min(k, 2)+1))
                            self.assertEqual(coefficient, F(k == 0))

    def test_empty_polynomial_is_rejected(self):
        with self.assertRaises(ValueError):
            self.reciprocal([])

    def test_zero_leading_coefficient_is_rejected(self):
        with self.assertRaises(ValueError):
            self.reciprocal([0, 1])

    def test_inexact_and_boolean_coefficients_are_rejected(self):
        for coefficients in ([1.0, 1], [True, 1], ['1', 1]):
            with self.subTest(coefficients=coefficients):
                with self.assertRaises(TypeError):
                    self.reciprocal(coefficients)

    def test_noninteger_powers_are_rejected(self):
        for offset, through in ((True, 5), (0, 2.5), (0.5, 5), (0, False)):
            with self.subTest(offset=offset, through=through):
                with self.assertRaises(TypeError):
                    self.reciprocal([1, 1], offset, through)

    def test_input_is_not_mutated(self):
        coefficients = [F(2), F(3), F(4)]
        original = list(coefficients)
        self.reciprocal(coefficients)
        self.assertEqual(coefficients, original)

if __name__ == '__main__':
    unittest.main()
