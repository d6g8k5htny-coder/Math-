"""Exact checks for the PR28 all-height annulus interfaces.

Subject: frontiers/rn_annulus_bridge_20260925/PROOF.md
at dedc69e1b786f7ad148e6b66718277f4145c99cd,
blob 6f317515b3d417661f86e2fed09bc7d950899c2b.

Python standard library only. This file does not import the author
package. A passing run checks rational identities used by R1, R2, R4,
R5, and R7. It does not prove conditional Gaussian moments, weighted
Kac-Rice, or the continuum bound (2).
"""
from fractions import Fraction as Q
from math import factorial
import unittest


def dval(coeff, i, j, x=0, z=0):
    x, z = Q(x), Q(z)
    total = Q(0)
    for (px, pz), c in coeff.items():
        if px >= i and pz >= j:
            total += (
                Q(c)
                * Q(factorial(px), factorial(px - i))
                * Q(factorial(pz), factorial(pz - j))
                * x ** (px - i)
                * z ** (pz - j)
            )
    return total


def jets_to_coeff(jets):
    return {
        key: Q(val) / (factorial(key[0]) * factorial(key[1]))
        for key, val in jets.items()
    }


def solve(rows, rhs):
    matrix = [list(map(Q, row)) + [Q(y)] for row, y in zip(rows, rhs)]
    size = len(matrix)
    for col in range(size):
        pivot_row = next(i for i in range(col, size) if matrix[i][col])
        matrix[pivot_row], matrix[col] = matrix[col], matrix[pivot_row]
        pivot = matrix[col][col]
        matrix[col] = [entry / pivot for entry in matrix[col]]
        for row in range(size):
            if row != col and matrix[row][col]:
                factor = matrix[row][col]
                matrix[row] = [
                    entry - factor * other
                    for entry, other in zip(matrix[row], matrix[col])
                ]
    return [row[-1] for row in matrix]


def hermite_jet(g_minus, g_plus, gp_minus, gp_plus, h_minus, h_plus, radius):
    radius = Q(radius)
    s0 = (g_minus + g_plus) / 2
    d0 = (g_plus - g_minus) / (2 * radius)
    s1 = (gp_minus + gp_plus) / 2
    d1 = (gp_plus - gp_minus) / (2 * radius)
    return (
        s0 - radius * radius * d1 / 2,
        (3 * d0 - s1) / 2,
        d1,
        3 * (s1 - d0) / (radius * radius),
        (h_minus + h_plus) / 2,
        (h_plus - h_minus) / (2 * radius),
    )


def impose_pins(free, separation, birth, gap):
    """Solve the six pins for the midpoint jets of orders (0..3,0) and (0..1,1)."""
    half = separation / 2
    pivots = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1)]
    base = {key: Q(val) for key, val in free.items() if key not in pivots}
    base_coeff = jets_to_coeff(base)
    targets = {
        (-1, 0, 0): birth,
        (1, 0, 0): birth - gap * separation ** 3,
        (-1, 1, 0): Q(0),
        (1, 1, 0): Q(0),
        (-1, 0, 1): Q(0),
        (1, 0, 1): Q(0),
    }
    rows, rhs = [], []
    for sign, di, dj in (
        (-1, 0, 0),
        (1, 0, 0),
        (-1, 1, 0),
        (1, 1, 0),
        (-1, 0, 1),
        (1, 0, 1),
    ):
        x = sign * half
        rows.append([
            Q(0) if (i < di or j != dj) else x ** (i - di) / factorial(i - di)
            for i, j in pivots
        ])
        rhs.append(targets[(sign, di, dj)] - dval(base_coeff, di, dj, x, 0))
    jets = dict(base)
    for key, value in zip(pivots, solve(rows, rhs)):
        jets[key] = value
    return jets


def aspect_entries(u):
    u = Q(u)
    return u * (u * u - Q(1, 4)) / 6, (u * u - Q(1, 4)) / 2


def minors(u, alpha, beta):
    longitudinal, mixed = aspect_entries(u)
    alpha, beta = Q(alpha), Q(beta)
    return (
        longitudinal * mixed * alpha ** 2,
        longitudinal * alpha * beta,
        u * beta ** 2,
    )


def gram_det(u, alpha, beta):
    return sum(value * value for value in minors(u, alpha, beta))


class PR28Algebra(unittest.TestCase):
    def test_hermite_closed_form_matches_the_linear_solve(self):
        radius = Q(1, 7)
        values = (Q(3), Q(-5), Q(2), Q(-4))
        rows = []
        for x, deriv in ((-radius, 0), (radius, 0), (-radius, 1), (radius, 1)):
            rows.append(
                [Q(1), x, x * x, x ** 3]
                if deriv == 0
                else [Q(0), Q(1), 2 * x, 3 * x * x]
            )
        p, q, r, s = solve(rows, values)
        self.assertEqual(
            hermite_jet(*values, Q(0), Q(0), radius)[:4],
            (p, q, 2 * r, 6 * s),
        )

    def test_six_pin_midpoint_target(self):
        separation, gap, birth = Q(1, 5), Q(4, 3), Q(2)
        jet = hermite_jet(
            birth,
            birth - gap * separation ** 3,
            Q(0),
            Q(0),
            Q(0),
            Q(0),
            separation / 2,
        )
        self.assertEqual(
            jet,
            (
                birth - gap * separation ** 3 / 2,
                -3 * gap * separation ** 2 / 2,
                Q(0),
                12 * gap,
                Q(0),
                Q(0),
            ),
        )

    def test_axial_quartic_and_transverse_affine_coefficients(self):
        samples = (
            (Q(-3), Q(1, 4), Q(24), Q(6)),
            (Q(3, 2), Q(1, 6), Q(-12), Q(5, 2)),
            (Q(4), Q(2, 9), Q(0), Q(-7)),
        )
        for u, separation, fourth, mixed in samples:
            jets = {
                (0, 0): Q(1, 3),
                (1, 0): Q(-2),
                (2, 0): Q(5),
                (3, 0): Q(-7),
                (4, 0): fourth,
                (0, 1): Q(3),
                (1, 1): Q(-5),
                (2, 1): mixed,
            }
            coeff = jets_to_coeff(jets)
            half = separation / 2
            longitudinal, transverse = aspect_entries(u)
            value_jet = hermite_jet(
                dval(coeff, 0, 0, -half, 0),
                dval(coeff, 0, 0, half, 0),
                dval(coeff, 1, 0, -half, 0),
                dval(coeff, 1, 0, half, 0),
                dval(coeff, 0, 1, -half, 0),
                dval(coeff, 0, 1, half, 0),
                half,
            )
            predicted_slope = (
                value_jet[1]
                + value_jet[2] * separation * u
                + value_jet[3] * (separation * u) ** 2 / 2
            )
            self.assertEqual(
                dval(coeff, 1, 0, separation * u, 0) - predicted_slope,
                separation ** 3 * longitudinal * fourth,
            )
            level = value_jet[4] + value_jet[5] * separation * u
            self.assertEqual(
                dval(coeff, 0, 1, separation * u, 0) - level,
                separation ** 2 * transverse * mixed,
            )
            self.assertEqual(
                dval(coeff, 1, 1, separation * u, 0) - value_jet[5],
                separation * u * mixed,
            )

    def test_normalized_numerators_keep_only_the_displayed_jets(self):
        separation, u, v = Q(1, 7), Q(2), Q(1, 3)
        fourth, mixed, transverse, cross = Q(24), Q(6), Q(-3), Q(10)
        jets = impose_pins(
            {(4, 0): fourth, (2, 1): mixed, (0, 2): transverse, (1, 2): cross},
            separation,
            Q(1),
            Q(2),
        )
        coeff = jets_to_coeff(jets)
        half = separation / 2
        jet = hermite_jet(
            dval(coeff, 0, 0, -half, 0),
            dval(coeff, 0, 0, half, 0),
            dval(coeff, 1, 0, -half, 0),
            dval(coeff, 1, 0, half, 0),
            dval(coeff, 0, 1, -half, 0),
            dval(coeff, 0, 1, half, 0),
            half,
        )
        slope = jet[1] + jet[2] * separation * u + jet[3] * (separation * u) ** 2 / 2
        level = jet[4] + jet[5] * separation * u
        num1 = dval(coeff, 1, 0, separation * u, separation * v) - slope - separation * v * jet[5]
        num2 = dval(coeff, 0, 1, separation * u, separation * v) - level
        longitudinal, transverse_poly = aspect_entries(u)
        self.assertEqual(
            num1,
            separation ** 2 * (longitudinal * separation * fourth + u * v * mixed)
            + (separation * v) ** 2 * cross / 2,
        )
        self.assertEqual(
            num2,
            separation * (transverse_poly * separation * mixed + v * transverse)
            + separation ** 2 * u * v * cross,
        )

    def test_three_minors_and_compact_rank_floor(self):
        units = (
            (Q(1), Q(0)),
            (Q(0), Q(1)),
            (Q(0), Q(-1)),
            (Q(3, 5), Q(4, 5)),
            (Q(3, 5), Q(-4, 5)),
            (Q(5, 13), Q(12, 13)),
            (Q(8, 17), Q(15, 17)),
            (Q(9, 41), Q(40, 41)),
            (Q(11, 61), Q(-60, 61)),
        )
        for u in (Q(-4), Q(-3, 2), Q(-6, 5), Q(6, 5), Q(3, 2), Q(2), Q(10)):
            longitudinal, mixed = aspect_entries(u)
            floor = min(longitudinal ** 2 * mixed ** 2, u * u) / 2
            self.assertGreater(floor, 0)
            for alpha, beta in units:
                self.assertGreaterEqual(alpha ** 4 + beta ** 4, Q(1, 2))
                values = minors(u, alpha, beta)
                matrix = [
                    [longitudinal * alpha, u * beta, Q(0)],
                    [Q(0), mixed * alpha, beta],
                ]
                actual = []
                for i, j in ((0, 1), (0, 2), (1, 2)):
                    actual.append(matrix[0][i] * matrix[1][j] - matrix[0][j] * matrix[1][i])
                self.assertEqual(tuple(actual), values)
                self.assertGreaterEqual(gram_det(u, alpha, beta), floor)

    def test_endpoint_determinant_leading_term_and_linear_error(self):
        gap, transverse = Q(2), Q(-3, 2)
        for separation in (Q(1, 5), Q(1, 25), Q(1, 100)):
            cubic = impose_pins({(0, 2): transverse}, separation, Q(1), gap)
            coeff = jets_to_coeff(cubic)
            half = separation / 2
            for sign, prediction in ((-1, -6 * gap * transverse), (1, 6 * gap * transverse)):
                xx = dval(coeff, 2, 0, sign * half, 0)
                xz = dval(coeff, 1, 1, sign * half, 0)
                zz = dval(coeff, 0, 2, sign * half, 0)
                self.assertEqual((xx * zz - xz * xz) / separation, prediction)
                self.assertEqual(xx / separation, 6 * gap * sign)
            quartic = impose_pins(
                {(0, 2): transverse, (4, 0): Q(24)},
                separation,
                Q(1),
                gap,
            )
            coeff = jets_to_coeff(quartic)
            self.assertEqual(quartic[(2, 0)], -(separation ** 2 / 24) * 24)
            self.assertEqual(quartic[(3, 0)], 12 * gap)
            xx = dval(coeff, 2, 0, -half, 0)
            xz = dval(coeff, 1, 1, -half, 0)
            zz = dval(coeff, 0, 2, -half, 0)
            error = (xx * zz - xz * xz) / separation - (-6 * gap * transverse)
            self.assertEqual(error / separation, Q(-3, 1))

    def test_off_axis_minor_and_scaled_row(self):
        for u, v in ((Q(0), Q(2)), (Q(-2), Q(-1, 3)), (Q(3, 2), Q(4))):
            minor = Q(0) * Q(0) - v * (v * v / 2)
            self.assertEqual(minor, -(v ** 3) / 2)
        separation, u, v = Q(1, 9), Q(-2), Q(1, 2)
        gap, transverse, mixed, cross = Q(3), Q(-5, 2), Q(4), Q(-3)
        jets = impose_pins(
            {(0, 2): transverse, (2, 1): mixed, (1, 2): cross},
            separation,
            Q(1),
            gap,
        )
        coeff = jets_to_coeff(jets)
        observed_x = dval(coeff, 1, 0, separation * u, separation * v) / separation ** 2
        observed_z = dval(coeff, 0, 1, separation * u, separation * v) / separation
        predicted_x = 6 * gap * (u * u - Q(1, 4)) + mixed * u * v + cross * v * v / 2
        self.assertEqual(observed_x, predicted_x)
        # The transverse row differs from a*v by the pinned on-axis remainder and the c1 transport.
        self.assertEqual(
            observed_z - transverse * v,
            separation * u * v * cross
            + dval(coeff, 0, 1, separation * u, 0) / separation,
        )

    def test_crossover_powers_need_the_seventh_series_term(self):
        gradient_r, normalizer_r = -3, -2
        gradient_delta, moment_delta = -2, -6
        geometric_r, geometric_v = 6, -6
        inner = gradient_r + normalizer_r + gradient_delta + moment_delta
        outer_v = gradient_delta + moment_delta + geometric_v
        self.assertEqual(inner, -13)
        self.assertEqual(outer_v, -14)
        self.assertEqual(gradient_r + normalizer_r + geometric_r, 1)
        self.assertEqual(inner + 2 * 7, 1)
        self.assertEqual(outer_v + 2 * 7, 0)
        self.assertEqual(inner + 2 * 6, -1)
        self.assertEqual(factorial(7), 5040)

    def test_fixed_annulus_chart_has_room_and_hessian_constant_closes(self):
        inner, outer = Q(3, 2), Q(4)
        midpoint = (inner + 1) / 2
        self.assertGreater(midpoint, 1)
        self.assertLess(midpoint, outer)
        self.assertGreater(inner * inner - midpoint * midpoint, 0)
        for radius in (Q(1), Q(2), Q(5), Q(20)):
            transported = 3 * radius ** 2 + 2 * radius + 1
            self.assertLessEqual(transported, 16 * (radius + 1) ** 2)


if __name__ == "__main__":
    unittest.main()
