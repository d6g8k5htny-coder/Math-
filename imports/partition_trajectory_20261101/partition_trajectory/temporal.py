"""Temporal causal memory and task-risk enumeration."""
from itertools import product
from .bottleneck import pareto_front
from .refinement import available_cells
from .risk import bayes_error


def temporal_trajectories(histories, capacity, observations):
    histories = tuple(histories)

    def recurse(stage, previous, maps):
        if stage == len(observations):
            yield maps
            return
        cells = available_cells(histories, previous, observations[stage])
        for assignment in product(range(capacity), repeat=len(cells)):
            mapping = {
                history: value
                for cell, value in zip(cells, assignment)
                for history in cell
            }
            yield from recurse(stage + 1, mapping, maps + [mapping])

    yield from recurse(0, None, [])


def temporal_risk_solver(histories, probs, observations, capacity, tasks):
    """Evaluate task risks at their stages on all causal trajectories.

    Each task is `(name, stage, task_dict, relevance_dict_or_None)`.
    """
    histories = tuple(histories)
    rows = []
    for maps in temporal_trajectories(histories, capacity, observations):
        vector = tuple(
            bayes_error(histories, probs, task, maps[stage], relevance)
            for _, stage, task, relevance in tasks
        )
        rows.append((vector, maps))
    vectors = sorted({vector for vector, _ in rows})
    exemplars = {}
    for vector, maps in rows:
        exemplars.setdefault(vector, maps)
    return {
        "vectors": vectors,
        "frontier": pareto_front(vectors),
        "exemplars": exemplars,
    }
