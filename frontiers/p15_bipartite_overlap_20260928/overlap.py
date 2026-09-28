"""Finite exact helpers for the bipartite-overlap capacity theorem.

Standard library only. Original coordinates are graph EDGES, never independent
clones. The analytic probability/hazard theorem is proved in PROOF.md.
"""
from fractions import Fraction
from itertools import product
from math import factorial

F = Fraction


def _validate(blocks, capacities):
    if not blocks or len(blocks) != len(capacities):
        raise ValueError('nonempty blocks and one capacity per block required')
    if any(not b for b in blocks):
        raise ValueError('blocks must be nonempty')
    if any(type(a) is not int or a < 1 for a in capacities):
        raise ValueError('capacities must be positive integers')


def capacity_bound(vertices, blocks, capacities):
    """Lower bound, exact when the block intersection graph is bipartite."""
    _validate(blocks, capacities)
    vertices = set(vertices)
    if not vertices <= set().union(*blocks):
        raise ValueError('all coordinates must belong to a block')
    return max((len(vertices & b) + a - 1) // a for b, a in zip(blocks, capacities))


def color_capacity(vertices, blocks, capacities, sides):
    """Construct an optimal coloring of ORIGINAL coordinates under bipartite overlap.

sides[i] is 0 or 1. Blocks on the same side must be disjoint. Vertex
splitting is an auxiliary incidence-graph construction, not a change to the
probability space. Returns one integer color per original coordinate.
    """
    _validate(blocks, capacities)
    if len(sides) != len(blocks) or any(s not in (0, 1) for s in sides):
        raise ValueError('one bipartition side per block required')
    for i, b in enumerate(blocks):
        for j in range(i):
            if sides[i] == sides[j] and b & blocks[j]:
                raise ValueError('same-side blocks intersect')
    vertices = set(vertices)
    k = capacity_bound(vertices, blocks, capacities)
    if not vertices:
        return {}
    # Incidence slots: each block has a_i auxiliary vertices of degree <= k.
    slots = {}
    for i, (b, a) in enumerate(zip(blocks, capacities)):
        for j, v in enumerate(sorted(b & vertices)):
            slots[i, v] = (0, i, j % a)
    edges = []
    for v in sorted(vertices):
        incidence = [i for i, b in enumerate(blocks) if v in b]
        left = next((slots[i, v] for i in incidence if sides[i] == 0), (1, v, 0))
        right = next((slots[i, v] for i in incidence if sides[i] == 1), (1, v, 0))
        edges.append((left, right, v))
    left_nodes = sorted({e[0] for e in edges})
    right_nodes = sorted({e[1] for e in edges})
    n = max(len(left_nodes), len(right_nodes))
    left_nodes += [(2, i, 0) for i in range(n-len(left_nodes))]
    right_nodes += [(2, i, 0) for i in range(n-len(right_nodes))]
    # Regularize by adding auxiliary edges between deficits; keep original tags.
    dl = {v: k for v in left_nodes}; dr = {v: k for v in right_nodes}
    for l, r, _ in edges:
        dl[l] -= 1; dr[r] -= 1
    if min((*dl.values(), *dr.values())) < 0:
        raise RuntimeError('capacity splitting exceeded palette')
    for l in left_nodes:
        for r in right_nodes:
            count = min(dl[l], dr[r])
            edges.extend((l, r, None) for _ in range(count))
            dl[l] -= count; dr[r] -= count
    if any(dl.values()) or any(dr.values()):
        raise RuntimeError('regularization deficits did not balance')
    colors = {}
    # A k-regular bipartite multigraph has a perfect matching by Hall; repeat.
    for color in range(k):
        adjacency = {l: [] for l in left_nodes}
        for index, (l, r, _) in enumerate(edges):
            adjacency[l].append((r, index))
        match = {}

        def augment(l, seen):
            for r, index in adjacency[l]:
                if r in seen:
                    continue
                seen.add(r)
                if r not in match or augment(match[r][0], seen):
                    match[r] = (l, index)
                    return True
            return False

        for l in left_nodes:
            if not augment(l, set()):
                raise RuntimeError('Hall matching failed')
        chosen = {index for _, index in match.values()}
        for index in chosen:
            original = edges[index][2]
            if original is not None:
                if original in colors:
                    raise RuntimeError('original coordinate colored twice')
                colors[original] = color
        edges = [e for index, e in enumerate(edges) if index not in chosen]
    if edges or set(colors) != vertices:
        raise RuntimeError('incomplete original-coordinate coloring')
    return colors


def active_generators(blocks, capacities, demands):
    """Full blocks at maximal demand; remove duplicates, not zero prices."""
    _validate(blocks, capacities)
    if len(demands) != len(blocks) or any(type(d) is not int or d < 1 for d in demands):
        raise ValueError('one positive integer demand per block required')
    if any(len(b) != a*d+1 for b, a, d in zip(blocks, capacities, demands)):
        raise ValueError('block size must be a_i d_i + 1')
    k = max(demands)
    answer = []
    for b, d in zip(blocks, demands):
        if d == k and b not in answer:
            answer.append(b)
    return answer


def good_probability(blocks, capacities, probabilities):
    """Exact small-instance Bernoulli enumeration, NOT a large-instance algorithm."""
    _validate(blocks, capacities)
    vertices = sorted(set().union(*blocks))
    if len(vertices) > 20:
        raise ValueError('finite enumeration is limited to 20 coordinates')
    if any(v not in probabilities or not F(0) <= probabilities[v] <= F(1) for v in vertices):
        raise ValueError('probabilities in [0,1] required')
    total = F(0)
    for bits in product((0, 1), repeat=len(vertices)):
        selected = {v for v, bit in zip(vertices, bits) if bit}
        if not all(len(selected & b) <= a for b, a in zip(blocks, capacities)):
            continue
        weight = F(1)
        for v, bit in zip(vertices, bits):
            weight *= probabilities[v] if bit else 1-probabilities[v]
        total += weight
    return total


def cs_probability_bound(joint, left, right):
    return joint**2 <= left*right


def exp_one_interval(n=40):
    if type(n) is not int or n < 1:
        raise ValueError('positive series length required')
    lo = sum((F(1, factorial(j)) for j in range(n+1)), F(0))
    tail = F(1, factorial(n+1))/(1-F(1, n+2))
    return lo, lo+tail


def _log_unit_interval(x, terms):
    t = (x-1)/(x+1)
    lo = 2*sum((t**(2*j+1)/(2*j+1) for j in range(terms)), F(0))
    error = 2*t**(2*terms+1)/((2*terms+1)*(1-t*t))
    return lo, lo+error


def log_interval(x, terms=55):
    x = F(x)
    if x <= 0 or type(terms) is not int or terms < 1:
        raise ValueError('positive logarithm argument and series length required')
    if x < 1:
        lo, hi = log_interval(1/x, terms)
        return -hi, -lo
    exponent = 0
    while x >= 2:
        x /= 2; exponent += 1
    lo, hi = _log_unit_interval(x, terms)
    l2, u2 = _log_unit_interval(F(2), terms)
    return lo+exponent*l2, hi+exponent*u2


def overlap_constant_interval():
    elo, ehi = exp_one_interval()
    llo, _ = log_interval(5*elo-4)
    _, lhi = log_interval(5*ehi-4)
    hlo, hhi = 5-lhi, 5-llo
    return 2/hhi, 2/hlo


def small_certificates():
    return {
        'exp_seven_thirds_margin': sum((F(7, 3)**j/factorial(j) for j in range(7)), F(0))-F(307, 32),
        'a_ge_two_tail_margin': F(28, 3)*F(4, 11)**5-F(25, 512),
        'e_upper_margin': F(87, 32)-exp_one_interval(6)[1],
        'chernoff_geometric_margin': 1-F(5, 16),
    }


def color_even_capacity(vertices, blocks, capacities):
    """Optimal original-coordinate coloring for read-two blocks with EVEN capacities.

The incidence graph need not be bipartite. Split into capacity-two vertices,
Euler-orient after pairing odd vertices, then edge-color the bipartite
outgoing/incoming incidence graph. Auxiliary edges are discarded at the end.
    """
    _validate(blocks, capacities)
    if any(a % 2 for a in capacities):
        raise ValueError('all capacities must be even')
    ground = set().union(*blocks)
    if any(sum(v in b for b in blocks) > 2 for v in ground):
        raise ValueError('a coordinate may belong to at most two blocks')
    vertices = set(vertices)
    capacity_bound(vertices, blocks, capacities)
    if not vertices:
        return {}
    slots = {}
    for i, (block, capacity) in enumerate(zip(blocks, capacities)):
        half_capacity = capacity // 2
        for j, v in enumerate(sorted(block & vertices)):
            slots[i, v] = (0, i, j % half_capacity)
    edges = []
    for v in sorted(vertices):
        incident = [i for i, b in enumerate(blocks) if v in b]
        left = slots[incident[0], v]
        right = slots[incident[1], v] if len(incident) == 2 else (1, v, 0)
        edges.append((left, right, v))
    adjacency = {}
    for index, (left, right, _) in enumerate(edges):
        adjacency.setdefault(left, []).append(index)
        adjacency.setdefault(right, []).append(index)
    odd = sorted(v for v, incident in adjacency.items() if len(incident) % 2)
    for left, right in zip(odd[::2], odd[1::2]):
        index = len(edges)
        edges.append((left, right, None))
        adjacency[left].append(index)
        adjacency[right].append(index)
    unused = set(range(len(edges)))
    oriented = {}
    while unused:
        start = edges[min(unused)][0]
        current = start
        while True:
            while adjacency[current] and adjacency[current][-1] not in unused:
                adjacency[current].pop()
            if not adjacency[current]:
                if current != start:
                    raise RuntimeError('Euler trail did not close')
                break
            index = adjacency[current].pop()
            unused.remove(index)
            left, right, _ = edges[index]
            nxt = right if current == left else left
            oriented[index] = (current, nxt)
            current = nxt
    out_blocks = {}; in_blocks = {}
    for index, (tail, head) in oriented.items():
        out_blocks.setdefault(tail, set()).add(index)
        in_blocks.setdefault(head, set()).add(index)
    auxiliary_blocks = list(out_blocks.values()) + list(in_blocks.values())
    colors = color_capacity(set(range(len(edges))), auxiliary_blocks,
                            [1]*len(auxiliary_blocks),
                            [0]*len(out_blocks) + [1]*len(in_blocks))
    return {original: colors[index] for index, (_, _, original) in enumerate(edges)
            if original is not None}
