import unittest
from partition_trajectory.examples import (
    single_task_divergence,
    temporal_option_game,
    randomized_minimax,
)


class FrontierTests(unittest.TestCase):
    def test_single_task_divergence(self):
        result = single_task_divergence()
        self.assertAlmostEqual(result["fully_informed_floor"], 0.12)
        frontier = result["pareto_frontier"]
        self.assertEqual(len(frontier), 2)
        self.assertAlmostEqual(frontier[0][0], 0.12)
        self.assertAlmostEqual(frontier[0][1], 0.28191725917176846)
        self.assertAlmostEqual(frontier[1][0], 0.25)
        self.assertAlmostEqual(frontier[1][1], 0.31127812445913283)

    def test_temporal_frontier_and_capacity(self):
        three = temporal_option_game(3)
        four = temporal_option_game(4)
        self.assertEqual(
            three["frontier"],
            [(0.0, 0.0, 0.25), (0.0, 0.25, 0.0), (0.25, 0.0, 0.0)],
        )
        self.assertFalse(three["all_zero"])
        self.assertEqual(three["uncertainty_premium"], 0.25)
        self.assertTrue(four["all_zero"])
        self.assertEqual(four["uncertainty_premium"], 0.0)

    def test_randomized_minimax(self):
        result = randomized_minimax()
        self.assertEqual(result["distribution_level_minimax"], 0.125)
        self.assertEqual(result["realization_level_risk"], 0.25)
        self.assertEqual(result["balanced_option_risks"], [0.125, 0.125])


if __name__ == "__main__":
    unittest.main()
