"""Partition and memory-map primitives.

Partitions are collections of nonempty frozensets. A memory map assigns each
history a memory state; its induced partition must be constant within cells of
available information.
"""

def refines(partition, required):
    """Return True when every cell of `partition` lies in a cell of `required`."""
    return all(any(cell <= target for target in required) for cell in partition)


def mapping_partition(histories, mapping):
    """Induce a partition on histories from a memory map."""
    cells = {}
    for history in histories:
        cells.setdefault(mapping[history], set()).add(history)
    return [frozenset(cell) for cell in cells.values()]


def mapping_refines(histories, mapping, required):
    return refines(mapping_partition(histories, mapping), required)


def available_cells(histories, previous_memory, observation):
    """Cells distinguishable by previous memory and the current observation."""
    groups = {}
    for history in histories:
        key = (
            None if previous_memory is None else previous_memory[history],
            observation(history),
        )
        groups.setdefault(key, set()).add(history)
    return [frozenset(cell) for cell in groups.values()]


def obstruction_cell(available, required):
    """Find a cell that cannot be split to refine `required`, or return None."""
    for cell in available:
        hits = [target for target in required if cell & target]
        if len(hits) > 1:
            return cell
    return None
