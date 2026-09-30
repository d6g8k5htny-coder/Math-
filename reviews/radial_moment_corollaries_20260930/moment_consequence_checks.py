"""Independent exact controls for the consequence of PR176 equation (17).

No author code is imported. These finite arithmetic/probability controls do not
prove the source Gaussian theorem, its remainder, or any original finite-r rate.
"""
from fractions import Fraction as F
import json
from math import factorial
import unittest


POWERS = [F(-100), F(-7), F(-1), F(-1, 2), F(0), F(1, 2),
          F(1), F(2), F(10), F(109, 10), F(10999, 1000)]


def integral(exponent):
    """Exact integral of q^exponent over [1,infinity), or divergent."""
    if exponent >= -1:
        raise ValueError('divergent power integral')
    return -1 / (exponent + 1)


def tail_moment(p):
    return (1 + p * integral(p - 12),
            p * (integral(p - 14) - integral(p - 12)))


def density_moment(p):
    return (11 * integral(p - 12),
            13 * integral(p - 14) - 11 * integral(p - 12))


def proposed_moment(p):
    return F(11) / (11 - p), -2 * p / ((13 - p) * (11 - p))


class MomentConsequenceTests(unittest.TestCase):
    def test_tail_and_density_derivations_agree_for_negative_zero_positive_p(self):
        for p in POWERS:
            with self.subTest(p=p):
                self.assertEqual(tail_moment(p), proposed_moment(p))
                self.assertEqual(density_moment(p), proposed_moment(p))

    def test_hand_checked_special_cases(self):
        for p, wanted in [(F(-1), (F(11, 12), F(1, 84))),
                          (F(0), (F(1), F(0))),
                          (F(1), (F(11, 10), F(-1, 60))),
                          (F(2), (F(11, 9), F(-4, 99)))]:
            self.assertEqual(tail_moment(p), wanted)

    def test_threshold_and_above_diverge(self):
        for p in (F(11), F(111, 10), F(12), F(100)):
            with self.assertRaises(ValueError):
                integral(p - 12)

    def test_direct_log_tail_integral(self):
        self.assertEqual(integral(F(-12)), F(1, 11))
        self.assertEqual(integral(F(-14)) - integral(F(-12)), F(-2, 143))

    def test_actual_probability_mixture_has_claimed_moment_remainder_bound(self):
        # A genuine mixture of Pareto(11), Pareto(13), Pareto(15): its tail
        # obeys (17) with c=1 and remainder (1/2)t^-4 q^-11(q^-4-1).
        for t in (4, 8, 16):
            delta, bound = F(1, t * t), F(1, 2)
            weights = [1 - delta - bound * delta**2, delta, bound * delta**2]
            self.assertEqual(sum(weights), 1)
            self.assertTrue(all(w > 0 for w in weights))
            for p in POWERS:
                exact = sum(w * F(alpha) / (alpha - p)
                            for w, alpha in zip(weights, (11, 13, 15)))
                leading, correction = proposed_moment(p)
                error = exact - leading - delta * correction
                self.assertLessEqual(abs(error), abs(p) * bound * delta**2 / (11 - p))
            exact_log = sum(w / alpha for w, alpha in zip(weights, (11, 13, 15)))
            self.assertLessEqual(abs(exact_log - F(1, 11) + F(2, 143) * delta),
                                 bound * delta**2 / 11)

    def test_uniform_in_p_remainder_overclaim_has_exact_counterexample(self):
        p, delta, bound = F(10999, 1000), F(1, 16), F(1, 2)
        actual_error = abs(bound * delta**2 * (F(15) / (15 - p) - F(11) / (11 - p)))
        self.assertGreater(actual_error, bound * delta**2)

    def test_wrong_normalizer_sign_and_missing_p_are_detected(self):
        cases = [
            ('missing denominator normalization', F(0), F(1)),
            ('reversed correction sign', F(1), F(1, 60)),
            ('omitted p factor', F(0), F(-2, 143)),
            ('omitted factor two', F(1), F(-1, 120)),
        ]
        for name, p, false_coefficient in cases:
            with self.subTest(mutant=name):
                self.assertNotEqual(tail_moment(p)[1], false_coefficient)
        self.assertNotEqual(integral(F(-14)) - integral(F(-12)), F(-1, 143))

    def test_all_order_finite_tail_matches_direct_pareto_mixture(self):
        # F(s)=sum C_j s^(-11-2j), s>=1, divided by F(1), is an actual
        # survival function. Conditioning at t gives component weights
        # proportional to C_j t^(-2j); its conditional moments are exact.
        coefficients = (F(2), F(3), F(5), F(7))
        for t in (3, 7, 13):
            pieces = [c / t**(2*j) for j, c in enumerate(coefficients)]
            normalizer = sum(pieces)
            weights = [part / normalizer for part in pieces]
            for p in POWERS:
                direct = sum(w * F(11+2*j) / (11+2*j-p)
                             for j, w in enumerate(weights))
                from_tail = 1 + p * sum(part * integral(p-12-2*j)
                                       for j, part in enumerate(pieces)) / normalizer
                numerator = sum((11+2*j) * part / (11+2*j-p)
                                for j, part in enumerate(pieces))
                self.assertEqual(direct, from_tail)
                self.assertEqual(direct, numerator / normalizer)
                self.assertNotEqual(direct, numerator)  # missing denominator

    def test_all_order_log_powers_and_normalization(self):
        for m in (1, 2, 3, 4):
            for alpha in (11, 13, 15, 17):
                # Integration by parts in y=log(q):
                # integral y^n exp(-alpha*y)dy = n/alpha times the n-1 integral.
                gamma_integral = F(1, alpha)
                for n in range(1, m):
                    gamma_integral *= F(n, alpha)
                tail_log_moment = m * gamma_integral
                exponential_log_moment = F(factorial(m), alpha**m)
                self.assertEqual(tail_log_moment, exponential_log_moment)
                if m > 1:
                    self.assertNotEqual(tail_log_moment, F(1, alpha**m))

    def test_quantile_expansion_brackets_an_actual_conditional_law_exactly(self):
        # The exact conditional tail q^-11(1+c t^-2 q^-2)/(1+c t^-2)
        # comes from F(s)=s^-11(1+c s^-2), with an irrelevant global normalizer.
        # Bracket the true quantile using only rational comparisons, avoiding
        # floating point root finding or differentiation of a remainder.
        for q0 in (F(5, 4), F(3, 2), F(2)):
            alpha = q0**-11
            for c in (F(1), F(2)):
                correction = c * (q0**-2 - 1) / 11
                for t in (8, 16, 32):
                    delta = F(1, t*t)
                    def survival(q):
                        return q**-11 * (1+c*delta*q**-2) / (1+c*delta)
                    qlo = q0*(1+correction*delta-delta**2)
                    qhi = q0*(1+correction*delta+delta**2)
                    self.assertGreater(qlo, 1)
                    self.assertGreater(survival(qlo), alpha)
                    self.assertLess(survival(qhi), alpha)
                    # Reversing the coefficient produces an O(delta) error
                    # that lies outside this O(delta^2) bracket.
                    wrong = q0*(1-correction*delta)
                    self.assertGreater(wrong, qhi)

    def test_offered_rational_coefficient_factors(self):
        integral_shape, u2, uabs = F(246528, 35), F(240192, 35), F(5898627, 880)
        self.assertEqual(11*u2/(2*integral_shape), F(4587, 856))
        self.assertEqual(11*uabs/(2*integral_shape), F(4587821, 876544))


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(MomentConsequenceTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print(json.dumps({'scope': 'PR176 equation17 conditional moment consequence only',
                      'exact_rational_powers': [str(p) for p in POWERS],
                      'moment_rows': [{'p': str(p), 'leading': str(tail_moment(p)[0]),
                                       'coefficient_of_c_t_minus_2': str(tail_moment(p)[1])}
                                      for p in POWERS],
                      'log_leading': '1/11', 'log_correction': '-2/143',
                      'quantile_controls': 'exact rational brackets for Pareto mixtures',
                      'all_order_controls': 'normalized finite Pareto mixtures',
                      'tests': result.testsRun, 'scientific_effect': 'NONE'}, sort_keys=True))
