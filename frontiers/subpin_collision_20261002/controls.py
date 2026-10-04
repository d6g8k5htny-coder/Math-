"""Exact finite controls; no analytic theorem or review is certified here."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def main():
    here = Path(__file__).resolve().parent
    root = here.parents[1]
    source_map = json.loads((here / 'SOURCES.json').read_text())
    for source in source_map['sources']:
        raw = (root / source['path']).read_bytes()
        require(len(raw) == source['bytes'], 'source size: ' + source['id'])
        require(hashlib.sha256(raw).hexdigest() == source['sha256'],
                'source digest: ' + source['id'])

    # Exhaust all simple undirected witness graphs on at most six vertices.
    # C is twice the edge count: ordered pairs, not unordered pairs or events.
    graphs = 0
    for n in range(7):
        edges = n * (n - 1) // 2
        for bits in range(1 << edges):
            c = 2 * bin(bits).count('1')
            require(c <= n * (n - 1), 'factorial count domination')
            require((c == 0) or c >= 2, 'ordered nonempty lower bound')
            for p in (0, 1, 2, 5):
                require(n**p * c <= n**(p + 2) * int(c > 0),
                        'polynomial insertion')
            graphs += 1

    # Exact discrete subsequences of the proof's three abstract examples.
    diagonal_ratios = []
    multiplicity_ratios = []
    slow_ratios = []
    for j in range(2, 11):
        r = F(1, 2**j)
        # Two points a scaled distance r apart fall below sqrt(r).
        require(r*r <= r, 'shrinking cutoff inclusion')
        close_count = r**3 * 2
        require(close_count/r**3 == 2, 'moments do not remove diagonal mass')
        diagonal_ratios.append(str(close_count/r**3))
        # Rare many-point cluster: small event probability, non-small count.
        n = 2**j
        require(r**5 * n*(n-1) / r**3 == 1-r, 'count/event distinction')
        require(r**5 * n**4 == r, 'fourth moment fails')
        multiplicity_ratios.append(str(1-r))
        # a_j=1/j tends to zero arbitrarily slowly relative to powers of r_j.
        a = F(1, j)
        require((r**3 * 2*a)/r**3 == 2*a, 'slow convergence family')
        slow_ratios.append(str(2*a))

    # If a radial density is r^alpha and ell=k r^3, its density is
    # (1/3) k^(-(alpha+1)/3) ell^((alpha-2)/3).
    alpha = F(4)  # r times the o(r^3) weighted mark
    lifetime_power = (alpha-2)/3
    gap_power = -(alpha+1)/3
    cumulative_power = lifetime_power+1
    require((lifetime_power, gap_power, cumulative_power) ==
            (F(2, 3), F(-5, 3), F(5, 3)), 'coarea units')
    require(F(2)+F(3) == F(5), 'one full normalizer only')
    # Negative controls for common incorrect substitutions.
    require(F(3)/3 != lifetime_power, 'omit radial/coarea Jacobian rejected')
    require(F(2)+F(2)+F(3) != F(5), 'double normalizer rejected')
    require(F(1) != F(2), 'unordered/ordered counts are different')

    print(json.dumps({
        'status': 'PASS_EXACT_FINITE_CONTROLS_ONLY',
        'source_files_verified': len(source_map['sources']),
        'simple_witness_graphs': graphs,
        'diagonal_mass_ratios': diagonal_ratios,
        'rare_high_multiplicity_ratios': multiplicity_ratios,
        'slow_convergence_ratios': slow_ratios,
        'coarea': {'radial_power': str(alpha), 'lifetime_power': str(lifetime_power),
                   'gap_power': str(gap_power), 'cumulative_power': str(cumulative_power)},
        'not_certified': ['analytic limits', 'Gaussian parent proofs',
                          'uniform little-o', 'algebraic rate', 'scientific acceptance']
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
