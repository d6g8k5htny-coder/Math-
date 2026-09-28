"""Independent finite controls. These do not certify the continuum hazard proof."""
import itertools
import unittest
from fractions import Fraction as F
from math import factorial
import overlap as m


def exact_chromatic_table(blocks, capacities):
    vertices = sorted(set().union(*blocks))
    n = len(vertices)
    sets = [{vertices[j] for j in range(n) if mask >> j & 1} for mask in range(1 << n)]
    good = [all(len(s & b) <= a for b, a in zip(blocks, capacities)) for s in sets]
    dp = [0] + [n + 1] * ((1 << n) - 1)
    for mask in range(1, 1 << n):
        first = mask & -mask
        sub = mask
        while sub:
            if sub & first and good[sub]:
                dp[mask] = min(dp[mask], 1 + dp[mask ^ sub])
            sub = (sub - 1) & mask
    return sets, dp


def check_coloring(test, vertices, blocks, capacities, colors):
    test.assertEqual(set(colors), set(vertices))
    for color in set(colors.values()):
        test.assertTrue(all(sum(colors.get(v, -1) == color for v in block & set(vertices)) <= a
                            for block, a in zip(blocks, capacities)))


class OverlapTests(unittest.TestCase):
    def test_minimum_palette(self):
        self.assertEqual(m.capacity_bound(set(range(4)), [{0, 1, 2, 3, 4}], [1]), 4)

    def test_empty_configuration(self):
        self.assertEqual(m.capacity_bound(set(), [{0, 1}], [1]), 0)
        self.assertEqual(m.color_capacity(set(), [{0, 1}], [1], [0]), {})

    def test_exact_coloring_against_partition_oracle(self):
        instances = [([{0, 1, 2}, {2, 3, 4}], [1, 1], [0, 1]),
                     ([{0, 1, 2, 3}, {2, 3, 4}], [2, 1], [0, 1]),
                     ([{0, 1}, {2, 3}, {0, 2}, {1, 3}], [1]*4, [0, 0, 1, 1])]
        for blocks, capacities, sides in instances:
            sets, oracle = exact_chromatic_table(blocks, capacities)
            for vertices, expected in zip(sets, oracle):
                self.assertEqual(m.capacity_bound(vertices, blocks, capacities), expected)
                colors = m.color_capacity(vertices, blocks, capacities, sides)
                check_coloring(self, vertices, blocks, capacities, colors)
                self.assertEqual(len(set(colors.values())), expected)

    def test_parallel_edges(self):
        vertices = set(range(5)); blocks = [vertices, vertices]
        colors = m.color_capacity(vertices, blocks, [1, 1], [0, 1])
        self.assertEqual(len(set(colors.values())), 5)
        check_coloring(self, vertices, blocks, [1, 1], colors)

    def test_nonunit_capacities(self):
        vertices = set(range(8)); blocks = [set(range(6)), set(range(3, 8))]
        colors = m.color_capacity(vertices, blocks, [2, 3], [0, 1])
        check_coloring(self, vertices, blocks, [2, 3], colors)
        self.assertEqual(len(set(colors.values())), 3)

    def test_one_original_coordinate_one_color(self):
        blocks = [{0, 1, 2, 3}, {2, 3, 4, 5}]
        colors = m.color_capacity(set(range(6)), blocks, [2, 2], [0, 1])
        self.assertEqual(len(colors), 6)
        check_coloring(self, set(range(6)), blocks, [2, 2], colors)

    def test_bipartition_validation(self):
        with self.assertRaises(ValueError):
            m.color_capacity({0, 1, 2}, [{0, 1}, {1, 2}], [1, 1], [0, 0])

    def test_read_two_is_not_enough(self):
        # Triangle with two parallel edges per side; one private coordinate per block.
        blocks = [{0, 1, 4, 5, 6}, {0, 1, 2, 3, 7}, {2, 3, 4, 5, 8}]
        vertices = set(range(6))
        _, oracle = exact_chromatic_table([b & vertices for b in blocks], [1]*3)
        self.assertEqual(oracle[-1], 6)
        self.assertEqual(m.capacity_bound(vertices, blocks, [1]*3), 4)
        self.assertTrue(all(not b <= vertices for b in blocks))
        with self.assertRaises(ValueError):
            m.color_capacity(vertices, blocks, [1]*3, [0, 1, 0])

    def test_complete_active_block_needs_extra_color(self):
        blocks = [set(range(5)), set(range(4, 9))]
        self.assertEqual(m.capacity_bound(blocks[0], blocks, [1, 1]), 5)
        self.assertEqual(m.active_generators(blocks, [1, 1], [4, 4]), blocks)

    def test_inactive_demand_one_is_not_a_generator(self):
        blocks = [set(range(5)), {4, 5}]
        self.assertEqual(m.active_generators(blocks, [1, 1], [4, 1]), [blocks[0]])
        self.assertEqual(m.capacity_bound({4, 5}, blocks, [1, 1]), 2)

    def test_exact_obstruction_all_subsets(self):
        blocks = [set(range(5)), set(range(4, 9))]
        generators = m.active_generators(blocks, [1, 1], [4, 4])
        for bits in itertools.product((False, True), repeat=9):
            vertices = {i for i, bit in enumerate(bits) if bit}
            self.assertEqual(m.capacity_bound(vertices, blocks, [1, 1]) > 4,
                             any(g <= vertices for g in generators))

    def test_shape_validation(self):
        with self.assertRaises(ValueError):
            m.active_generators([{0, 1, 2}], [1], [4])
        with self.assertRaises(ValueError):
            m.color_capacity({9}, [{0, 1}], [1], [0])
        with self.assertRaises(ValueError):
            m.color_capacity({0}, [{0}], [0], [0])

    def test_overlap_destroys_local_independence(self):
        blocks = [{0, 1}, {1, 2}]; p = {i: F(1, 2) for i in range(3)}
        joint = m.good_probability(blocks, [1, 1], p)
        marg = [m.good_probability([b], [1], p) for b in blocks]
        self.assertEqual(joint, F(5, 8))
        self.assertGreater(joint, marg[0]*marg[1])
        self.assertTrue(m.cs_probability_bound(joint, marg[0], marg[1]))

    def test_cauchy_schwarz_on_heterogeneous_grid(self):
        blocks = [{0, 1}, {1, 2}]
        for values in itertools.product((F(0), F(1, 4), F(1, 2), F(3, 4), F(1)), repeat=3):
            p = dict(enumerate(values))
            q = m.good_probability(blocks, [1, 1], p)
            q0 = m.good_probability([blocks[0]], [1], p)
            q1 = m.good_probability([blocks[1]], [1], p)
            self.assertTrue(m.cs_probability_bound(q, q0, q1))

    def test_probability_boundaries(self):
        blocks = [{0, 1}, {1, 2}]
        self.assertEqual(m.good_probability(blocks, [1, 1], {i: F(0) for i in range(3)}), 1)
        self.assertEqual(m.good_probability(blocks, [1, 1], {i: F(1) for i in range(3)}), 0)

    def test_same_side_independence_exact(self):
        p = {i: F(i+1, 7) for i in range(5)}
        self.assertEqual(m.good_probability([{0, 1}, {2, 3, 4}], [1, 2], p),
                         m.good_probability([{0, 1}], [1], p)*m.good_probability([{2, 3, 4}], [2], p))

    def test_binomial_five_tail_identity(self):
        for q in (F(1, 4), F(1, 3), F(1, 2), F(3, 4)):
            p = {i: 1-q for i in range(5)}
            self.assertEqual(m.good_probability([set(range(5))], [1], p), 5*q**4-4*q**5)

    def test_exp_rational_enclosure(self):
        lo, hi = m.exp_one_interval(6)
        self.assertEqual(lo, F(1957, 720))
        self.assertEqual(hi, F(31967, 11760))
        self.assertGreater(lo, F(8, 3))
        self.assertLess(hi, F(87, 32))

    def test_tail_and_constant_certificates(self):
        cert = m.small_certificates()
        self.assertTrue(all(v > 0 for v in cert.values()))
        self.assertEqual(cert['exp_seven_thirds_margin'], F(129055, 209952))
        self.assertEqual(cert['a_ge_two_tail_margin'], F(2601239, 247374336))

    def test_overlap_constant(self):
        lo, hi = m.overlap_constant_interval()
        self.assertGreater(lo, F(73015826409534942932, 10**20))
        self.assertLess(hi, F(73015826409534942934, 10**20))
        self.assertLess(hi, F(3, 4))

    def test_demand_one_obstruction_preserved(self):
        # At reference p*=1-1/e the two-point capacity-one good probability exceeds e^-1.
        lo, hi = m.exp_one_interval(6)
        # e>2 implies 2/e-1/e^2>1/e, i.e. e-1>0.
        self.assertGreater(lo-1, 0)
        self.assertEqual(m.capacity_bound({0, 1}, [{0, 1}], [1]), 2)

    def test_log_interval_contains_known_identity(self):
        lo, hi = m.log_interval(F(1))
        self.assertEqual((lo, hi), (0, 0))
        l2, u2 = m.log_interval(F(2))
        l4, u4 = m.log_interval(F(4))
        self.assertEqual((l4, u4), (2*l2, 2*u2))

    def test_even_triangle_same_palette(self):
        blocks = [set(range(4)) | set(range(8, 12)) | {12},
                  set(range(8)) | {13},
                  set(range(4, 12)) | {14}]
        vertices = set(range(12))
        colors = m.color_even_capacity(vertices, blocks, [2, 2, 2])
        check_coloring(self, vertices, blocks, [2, 2, 2], colors)
        self.assertEqual(len(set(colors.values())), 4)
        whole = set(range(15))
        colors = m.color_even_capacity(whole, blocks, [2, 2, 2])
        check_coloring(self, whole, blocks, [2, 2, 2], colors)
        self.assertEqual(len(set(colors.values())), 5)

    def test_even_capacity_partition_oracle(self):
        blocks = [{0, 1, 4, 5}, {0, 1, 2, 3}, {2, 3, 4, 5}]
        for caps in ([2, 2, 2], [2, 4, 2]):
            sets, oracle = exact_chromatic_table(blocks, caps)
            for vertices, expected in zip(sets, oracle):
                colors = m.color_even_capacity(vertices, blocks, caps)
                check_coloring(self, vertices, blocks, caps, colors)
                self.assertEqual(len(set(colors.values())), expected)

    def test_even_capacity_requires_even(self):
        with self.assertRaises(ValueError):
            m.color_even_capacity(set(range(4)), [set(range(4))], [3])

    def test_even_capacity_rejects_read_three(self):
        with self.assertRaises(ValueError):
            m.color_even_capacity({0, 1, 2}, [{0, 1}, {0, 2}, {0}], [2, 2, 2])

    def test_even_empty(self):
        self.assertEqual(m.color_even_capacity(set(), [{0, 1}], [2]), {})

    def test_nonbipartite_read_two_probability(self):
        blocks = [{0, 1}, {1, 2}, {2, 0}]
        for values in itertools.product((F(1, 4), F(1, 2), F(3, 4)), repeat=3):
            p = dict(enumerate(values))
            q = m.good_probability(blocks, [1, 1, 1], p)
            product_marginals = F(1)
            for block in blocks:
                product_marginals *= m.good_probability([block], [1], p)
            self.assertLessEqual(q*q, product_marginals)

    def test_even_hazard_rational_certificate(self):
        self.assertEqual(F(512, 25)-F(87, 32)**3, F(314641, 819200))
        self.assertGreater(F(512, 25)-F(87, 32)**3, 0)
        lo, hi = m.log_interval(F(512, 25))
        self.assertGreater(lo, 3)
        self.assertLess(2/lo, F(2, 3))

if __name__ == '__main__':
    unittest.main()
