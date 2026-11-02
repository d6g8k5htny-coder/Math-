import unittest
from partition_trajectory.channels import (
    specialized_risks,
    robust_risks,
    visibility_premia,
    robust_expected_loss_comparison,
    correlated_visibility,
)


class ChannelTests(unittest.TestCase):
    def test_symmetric_specialization(self):
        a = 0.4
        b = 0.05
        self.assertEqual(specialized_risks(a, b), (0.4, 0.115, 0.16))
        self.assertEqual(robust_risks(a, b), (0.45, 0.025, 0.025))

    def test_factorized_visibility_gap(self):
        for alpha, beta in [(0, 0.1), (0.2, 0.3), (0.4, 0.05), (0.5, 0.5)]:
            premia = visibility_premia(alpha, beta)
            expected = 0.125 * (1 - 2 * alpha) * (1 - 2 * beta)
            self.assertAlmostEqual(premia["gap"], expected)

    def test_robust_regime(self):
        result = robust_expected_loss_comparison(0.4, 0.05)
        self.assertAlmostEqual(result["specialized_mixture"], 0.5375)
        self.assertAlmostEqual(result["robust"], 0.475)
        self.assertTrue(result["robust_preferred"])

    def test_correlated_boundary(self):
        expected = {0.0: 0.0, 0.06: 0.03, 0.10: 0.05, 0.20: 0.05}
        for kappa, gap in expected.items():
            result = correlated_visibility(0.2, 0.3, kappa)
            self.assertAlmostEqual(result["gap"], gap)


if __name__ == "__main__":
    unittest.main()
