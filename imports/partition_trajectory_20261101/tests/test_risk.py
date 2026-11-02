import unittest
from partition_trajectory.risk import conditional_entropy


class RiskTests(unittest.TestCase):
    def setUp(self):
        self.histories = [(x, y) for x in (0, 1) for y in (0, 1)]
        self.probs = {h: 0.25 for h in self.histories}

    def test_residual_entropy_boundaries(self):
        parity = {h: h[0] ^ h[1] for h in self.histories}
        x = {h: h[0] for h in self.histories}
        joint = {h: h for h in self.histories}
        self.assertEqual(conditional_entropy(self.histories, self.probs, parity, x), 1.0)
        self.assertEqual(conditional_entropy(self.histories, self.probs, parity, joint), 0.0)


if __name__ == "__main__":
    unittest.main()
