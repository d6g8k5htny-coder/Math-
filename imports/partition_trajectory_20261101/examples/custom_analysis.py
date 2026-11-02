"""Minimal custom finite-model analysis."""
import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from partition_trajectory.solver import solve


def main():
    histories = list(product((0, 1), repeat=2))
    p_x = [frozenset({(0, 0), (0, 1)}), frozenset({(1, 0), (1, 1)})]
    p_parity = [frozenset({(0, 0), (1, 1)}), frozenset({(0, 1), (1, 0)})]

    result = solve(
        histories,
        required=[p_x, p_parity],
        observations=[lambda h: h[0], lambda h: h[1]],
        capacity=2,
    )
    print(f"Causal trajectories found: {len(result['solutions'])}")
    print(f"Obstruction: {result['obstruction']}")


if __name__ == "__main__":
    main()
