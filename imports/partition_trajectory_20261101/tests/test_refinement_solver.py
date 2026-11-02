import unittest
from partition_trajectory.examples import (
    parity_reuse,
    x_then_z,
    greedy_retention,
    flexibility_frontier,
)


class RefinementSolverTests(unittest.TestCase):
    def test_parity_reuse(self):
        self.assertEqual(parity_reuse()["solution_count"], 4)

    def test_x_then_z_obstruction(self):
        result = x_then_z()
        self.assertEqual(result["solution_count"], 0)
        self.assertEqual(result["obstruction_stage"], 1)
        self.assertEqual(result["obstruction_cell"], [(0, 0), (0, 1)])

    def test_future_aware_retention(self):
        result = greedy_retention()
        self.assertEqual(result["solution_count"], 36)
        self.assertEqual(
            result["first_final_partition"],
            [[(0, 0)], [(0, 1)], [(1, 0), (1, 1)]],
        )

    def test_flexibility_patterns(self):
        self.assertEqual(
            flexibility_frontier(),
            {"empty": 108, "O0_only": 36, "O1_only": 36, "joint": 0},
        )


if __name__ == "__main__":
    unittest.main()
