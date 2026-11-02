"""Built-in executable model suites."""
from itertools import product
from .solver import solve
from .risk import bayes_error, mutual_information, conditional_entropy
from .bottleneck import enumerate_memories, pareto_front
from .temporal import temporal_risk_solver
from .channels import (
    MEMORY_A,
    MEMORY_B,
    MEMORY_C,
    specialized_risks,
    robust_risks,
    visibility_premia,
    robust_expected_loss_comparison,
    correlated_visibility,
)


def _histories():
    return list(product((0, 1), repeat=2))


def _partitions():
    p_x = [frozenset({(0, 0), (0, 1)}), frozenset({(1, 0), (1, 1)})]
    p_z = [frozenset({(0, 0), (1, 0)}), frozenset({(0, 1), (1, 1)})]
    p_parity = [frozenset({(0, 0), (1, 1)}), frozenset({(0, 1), (1, 0)})]
    p2 = [frozenset({(0, 0)}), frozenset({(0, 1)}), frozenset({(1, 0), (1, 1)})]
    mb = [frozenset({(0, 0), (0, 1)}), frozenset({(1, 0)}), frozenset({(1, 1)})]
    return p_x, p_z, p_parity, p2, mb


def parity_reuse():
    histories = _histories()
    p_x, _, p_parity, _, _ = _partitions()
    result = solve(histories, [p_x, p_parity], [lambda h: h[0], lambda h: h[1]], 2)
    return {"solution_count": len(result["solutions"])}


def x_then_z():
    histories = _histories()
    p_x, p_z, _, _, _ = _partitions()
    result = solve(histories, [p_x, p_z], [lambda h: h, lambda h: None], 2)
    obstruction = result["obstruction"]
    return {
        "solution_count": len(result["solutions"]),
        "obstruction_stage": obstruction["stage"],
        "obstruction_cell": sorted(obstruction["cell"]),
    }


def greedy_retention():
    histories = _histories()
    p_x, _, _, p2, _ = _partitions()
    result = solve(histories, [p_x, p2], [lambda h: h, lambda h: None], 3)
    return {
        "solution_count": len(result["solutions"]),
        "first_final_partition": [
            sorted(cell) for cell in _partition_of_last(histories, result["solutions"][0])
        ],
    }


def _partition_of_last(histories, solution):
    from .refinement import mapping_partition
    return mapping_partition(histories, solution["maps"][-1])


def flexibility_frontier():
    histories = _histories()
    p_x, _, _, p2, mb = _partitions()
    result = solve(
        histories,
        [p_x, p_x],
        [lambda h: h, lambda h: None],
        3,
        options={"O0": p2, "O1": mb},
        max_solutions=100000,
    )
    patterns = {}
    for solution in result["solutions"]:
        key = tuple(sorted(k for k, v in solution["flexibility"].items() if v))
        patterns[key] = patterns.get(key, 0) + 1
    return {
        "empty": patterns.get((), 0),
        "O0_only": patterns.get(("O0",), 0),
        "O1_only": patterns.get(("O1",), 0),
        "joint": patterns.get(("O0", "O1"), 0),
    }


def single_task_divergence():
    observations = ("a", "b", "c")
    weights = {"a": 0.5, "b": 13 / 76, "c": 25 / 76}
    posteriors = {"a": 0.0, "b": 22 / 25, "c": 189 / 625}
    histories = [(a, r) for a in observations for r in (0, 1)]
    probs = {
        (a, r): weights[a] * (posteriors[a] if r else 1 - posteriors[a])
        for a in observations
        for r in (0, 1)
    }
    task = {h: h[1] for h in histories}
    points = []
    for memory_a in enumerate_memories(observations, 2):
        memory = {h: memory_a[h[0]] for h in histories}
        points.append((
            bayes_error(histories, probs, task, memory),
            mutual_information(histories, probs, task, memory),
        ))
    return {
        "fully_informed_floor": bayes_error(
            histories, probs, task, {h: h[0] for h in histories}
        ),
        "pareto_frontier": sorted(pareto_front(points, maximize_index=1)),
    }


def temporal_option_game(capacity=3):
    histories = _histories()
    probs = {h: 0.25 for h in histories}
    task_x = {h: h[0] for h in histories}
    task_z = {h: h[1] for h in histories}
    relevant_0 = {h: int(h[0] == 0) for h in histories}
    relevant_1 = {h: int(h[0] == 1) for h in histories}
    tasks = [
        ("current_x", 0, task_x, None),
        ("O0", 1, task_z, relevant_0),
        ("O1", 1, task_z, relevant_1),
    ]
    result = temporal_risk_solver(histories, probs, [lambda h: h, lambda h: None], capacity, tasks)
    current_exact = [v for v in result["vectors"] if v[0] == 0]
    premium = min((max(v[1], v[2]) for v in current_exact), default=None)
    return {
        "capacity": capacity,
        "frontier": result["frontier"],
        "all_zero": (0, 0, 0) in result["vectors"],
        "uncertainty_premium": premium,
    }


def randomized_minimax():
    # Exact analytic optimum over current-exact deterministic risk vectors.
    balanced = 0.5 * 0.25
    return {
        "mix_A": 0.5,
        "mix_B": 0.5,
        "distribution_level_minimax": balanced,
        "realization_level_risk": 0.25,
        "balanced_option_risks": [balanced, balanced],
    }


def asymmetric_visibility(alpha=0.4, beta=0.05):
    a = specialized_risks(alpha, beta)
    return {
        "alpha": alpha,
        "beta": beta,
        "specialized_A": a,
        "specialized_B": (a[0], a[2], a[1]),
        "robust_C": robust_risks(alpha, beta),
        "premia": visibility_premia(alpha, beta),
        "expected_loss": robust_expected_loss_comparison(alpha, beta),
    }


def correlated_boundary(alpha=0.2, beta=0.3):
    rows = {}
    for kappa in (0.0, 0.06, 0.10, 0.20):
        result = correlated_visibility(alpha, beta, kappa)
        rows[str(kappa)] = {
            "distribution": result["distribution"],
            "realization": result["realization"],
            "gap": result["gap"],
        }
    return {"alpha": alpha, "beta": beta, "rows": rows}


def run_all():
    return {
        "parity_reuse": parity_reuse(),
        "x_then_z": x_then_z(),
        "greedy_retention": greedy_retention(),
        "flexibility_frontier": flexibility_frontier(),
        "single_task_divergence": single_task_divergence(),
        "temporal_option_game_3": temporal_option_game(3),
        "temporal_option_game_4": temporal_option_game(4),
        "randomized_minimax": randomized_minimax(),
        "asymmetric_visibility": asymmetric_visibility(),
        "correlated_boundary": correlated_boundary(),
    }
