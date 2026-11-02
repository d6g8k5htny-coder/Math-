# Partition-Trajectory Possibility

A self-contained implementation of a finite, executable theory of possibility as causal information architecture.

The package studies which future task–loss structures an agent can keep actionable through memory, observation, and causal updates. It includes exact partition solvers, Bayes-risk frontiers, temporal memory search, randomized option games, and independent/correlated channel models.

## Requirements

- Python 3.11 or newer
- No third-party runtime dependencies

## Execute all model suites

From this directory:

```bash
python3 -m partition_trajectory
```

The command emits JSON for all built-in models:

- parity memory reuse;
- x-then-z causal infeasibility;
- greedy versus future-aware retention;
- flexibility frontiers;
- MI–risk divergence;
- temporal option games at capacities three and four;
- randomized minimax;
- asymmetric visibility;
- correlated-noise boundary.

## Run the exact tests

```bash
python3 -m unittest discover -s tests -v
```

The tests use only `unittest` and the package itself.

## Minimal custom analysis

```python
from itertools import product
from partition_trajectory.solver import solve

histories = list(product((0, 1), repeat=2))  # (x, y)
p_x = [frozenset({(0, 0), (0, 1)}), frozenset({(1, 0), (1, 1)})]
p_parity = [frozenset({(0, 0), (1, 1)}), frozenset({(0, 1), (1, 0)})]

result = solve(
    histories,
    required=[p_x, p_parity],
    observations=[lambda h: h[0], lambda h: h[1]],
    capacity=2,
)

print(len(result["solutions"]))  # 4
```

`observations[t](h)` returns the new information available before the update at stage `t`. Every returned memory map is constant on available-information cells and is therefore causal by construction.

## Package map

- `partition_trajectory/refinement.py` — partition and available-information primitives
- `partition_trajectory/solver.py` — causal section-or-obstruction search
- `partition_trajectory/risk.py` — Bayes error, mutual information, conditional entropy, information-loss defect
- `partition_trajectory/bottleneck.py` — static memory enumeration and Pareto frontiers
- `partition_trajectory/temporal.py` — temporal causal trajectories and task risks
- `partition_trajectory/channels.py` — independent asymmetric and correlated channel models
- `partition_trajectory/examples.py` — all built-in model suites
- `docs/theory.md` — canonical model, equations, and scope
- `docs/glossary.md` — definitions of provisional terms
- `docs/verification.md` — exact expected results
- `docs/research_status.md` — candidate status, tested and discarded paths
- `examples/` — additional execution notes and a custom-analysis template

## Scope

The package implements finite model validations, not a universal theory of agency or evidence about deployed AI systems. General partition search is combinatorial. Task losses, observation timing, memory capacity, and adversary visibility must be declared explicitly.

See `docs/theory.md` for the formal model and `docs/glossary.md` for terms.
