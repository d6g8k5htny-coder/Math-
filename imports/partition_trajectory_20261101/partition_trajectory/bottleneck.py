"""Static actionable-bottleneck enumeration and Pareto frontiers."""
from itertools import product


def enumerate_memories(histories, capacity):
    """Enumerate canonical memory maps up to memory-label permutation."""
    seen = set()
    memories = []
    for assignment in product(range(capacity), repeat=len(histories)):
        mapping = {history: assignment[i] for i, history in enumerate(histories)}
        groups = {}
        for history in histories:
            groups.setdefault(mapping[history], set()).add(history)
        key = tuple(sorted(tuple(sorted(cell)) for cell in groups.values()))
        if key not in seen:
            seen.add(key)
            memories.append(mapping)
    return memories


def pareto_front(points, maximize_index=None):
    """Nondominated points; lower is better except at `maximize_index`."""
    unique = list(dict.fromkeys(points))
    front = []
    for candidate in unique:
        dominated = False
        for other in unique:
            if other == candidate:
                continue
            no_worse = True
            strictly_better = False
            for i in range(len(candidate)):
                if i == maximize_index:
                    no_worse &= other[i] >= candidate[i] - 1e-12
                    strictly_better |= other[i] > candidate[i] + 1e-12
                else:
                    no_worse &= other[i] <= candidate[i] + 1e-12
                    strictly_better |= other[i] < candidate[i] - 1e-12
            if no_worse and strictly_better:
                dominated = True
                break
        if not dominated:
            front.append(candidate)
    return front
