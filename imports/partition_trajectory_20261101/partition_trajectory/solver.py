"""Causal section-or-obstruction solver."""
from itertools import product
from .refinement import (
    available_cells,
    mapping_partition,
    mapping_refines,
    obstruction_cell,
    refines,
)


def solve(histories, required, observations, capacity, options=None, max_solutions=10000):
    """Find causal memory trajectories or report a refinement obstruction.

    Args:
        histories: finite iterable of hashable histories.
        required: required suffix partition for each decision stage.
        observations: one function per stage; observation_t(h) returns the new
            observation available before the update at stage t.
        capacity: maximum number of memory states.
        options: optional {name: partition} future task partitions evaluated on
            the final memory partition.
        max_solutions: safety limit for returned trajectories.
    """
    histories = tuple(histories)
    options = options or {}
    solutions = []
    first_obstruction = None

    def recurse(stage, previous, maps):
        nonlocal first_obstruction
        if len(solutions) >= max_solutions:
            return
        available = available_cells(histories, previous, observations[stage])
        for assignment in product(range(capacity), repeat=len(available)):
            mapping = {
                history: value
                for cell, value in zip(available, assignment)
                for history in cell
            }
            if not mapping_refines(histories, mapping, required[stage]):
                continue
            new_maps = maps + [mapping]
            if stage + 1 == len(required):
                final_partition = mapping_partition(histories, mapping)
                flexibility = {
                    name: refines(final_partition, partition)
                    for name, partition in options.items()
                }
                solutions.append({"maps": new_maps, "flexibility": flexibility})
            else:
                recurse(stage + 1, mapping, new_maps)
        if not solutions and first_obstruction is None:
            cell = obstruction_cell(available, required[stage])
            if cell is not None:
                first_obstruction = {"stage": stage, "cell": cell}

    recurse(0, None, [])
    return {"solutions": solutions, "obstruction": first_obstruction}
