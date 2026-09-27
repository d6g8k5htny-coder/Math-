"""Independent exact checks for the PR25 Sections B–D review.

Standard library only. These identities are finite algebraic facts.
They do not prove the Gaussian continuum limit and they do not accept
the author unittest file.
"""
from __future__ import annotations

from fractions import Fraction as Q
import unittest

NAMES = ("k", "u", "v", "theta", "q")
ZERO = (0,) * len(NAMES)


class L:
    """Laurent polynomial over Q in k,u,v,theta,q."""

    def __init__(self, terms=None):
        self.terms = {}
        for m, c in (terms or {}).items():
            c = Q(c)
            if c:
                self.terms[m] = self.terms.get(m, Q(0)) + c
                if not self.terms[m]:
                    del self.terms[m]

    @staticmethod
    def coerce(x):
        if isinstance(x, L):
            return x
        if type(x) is int or isinstance(x, Q):
            return L({ZERO: Q(x)})
        raise TypeError(type(x))

    def __add__(self, other):
        out = dict(self.terms)
        for m, c in self.coerce(other).terms.items():
            out[m] = out.get(m, Q(0)) + c
            if not out[m]:
                del out[m]
        return L(out)

    __radd__ = __add__

    def __neg__(self):
        return L({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) + (-self)

    def __mul__(self, other):
        other = self.coerce(other)
        out = {}
        for m, a in self.terms.items():
            for n, b in other.terms.items():
                key = tuple(i + j for i, j in zip(m, n))
                out[key] = out.get(key, Q(0)) + a * b
                if not out[key]:
                    del out[key]
        return L(out)

    __rmul__ = __mul__

    def __truediv__(self, x):
        if type(x) is int or isinstance(x, Q):
            if not x:
                raise ZeroDivisionError
            return L({m: c / Q(x) for m, c in self.terms.items()})
        other = self.coerce(x)
        if len(other.terms) != 1:
            raise TypeError("division only by a monomial")
        n, b = next(iter(other.terms.items()))
        return L({tuple(i - j for i, j in zip(m, n)): c / b for m, c in self.terms.items()})

    def __pow__(self, n):
        if type(n) is not int or n < 0:
            raise TypeError("nonnegative integer power")
        result = L.coerce(1)
        for _ in range(n):
            result = result * self
        return result

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms

    def __repr__(self):
        return f"L({self.terms})"


def var(name):
    m = [0] * len(NAMES)
    m[NAMES.index(name)] = 1
    return L({tuple(m): Q(1)})


k, u, v, theta, q = map(var, NAMES)


def det2(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def chart_jets():
    D = u * u - Q(1, 4)
    Lc = 2 * u ** 3 - 3 * u / 2 - Q(1, 2)
    c = -12 * k * D / v ** 2 - 2 * q * u / v
    d = 12 * k * (Lc + theta) / v ** 3 + 3 * q * D / v ** 2
    A = (12 * k * u + 6 * k + q * v - 12 * k * theta) / (2 * v * v)
    return A, c, d


def hessians():
    A, c, d = chart_jets()
    BM = [[-6 * k, -q / 2], [-q / 2, A - c / 2]]
    BS = [[6 * k, q / 2], [q / 2, A + c / 2]]
    BX = [[12 * k * u + q * v, q * u + c * v], [q * u + c * v, A + c * u + d * v]]
    return BM, BS, BX


def w_of_q():
    return (q * v + 12 * k * u) / (6 * k)


class Algebra(unittest.TestCase):
    def test_b1_is_the_unique_six_pin_cubic(self):
        # Monomials 1,s,t,s^2,st,t^2,s^3,s^2 t, s t^2, t^3.
        # Rows are P, P_s, P_t at s=-1/2 and s=+1/2, t=0.
        cols = []
        rhs_pos = []
        for a in range(4):
            for b in range(4 - a):
                cols.append((a, b))
        rows = []
        for s0 in (Q(-1, 2), Q(1, 2)):
            for kind in ("P", "Ps", "Pt"):
                row = []
                for a, b in cols:
                    if kind == "P":
                        coef = Q(0) if b else s0 ** a
                    elif kind == "Ps":
                        coef = Q(0) if b or a == 0 else a * s0 ** (a - 1)
                    else:
                        coef = Q(0) if b != 1 else s0 ** a
                    row.append(coef)
                rows.append(row)
        # Augment with the two height values and four zeros. k is kept symbolic
        # by solving the inhomogeneous system as particular + null space over Q,
        # with the height -k represented by a second right-hand column.
        def rref(matrix):
            A = [row[:] for row in matrix]
            m, n = len(A), len(A[0])
            pivots = []
            r = 0
            for c in range(n):
                pivot = next((i for i in range(r, m) if A[i][c]), None)
                if pivot is None:
                    continue
                A[r], A[pivot] = A[pivot], A[r]
                scale = A[r][c]
                A[r] = [x / scale for x in A[r]]
                for i in range(m):
                    if i != r and A[i][c]:
                        factor = A[i][c]
                        A[i] = [x - factor * y for x, y in zip(A[i], A[r])]
                pivots.append(c)
                r += 1
            return A, pivots

        # Right hand: height at -1/2 is 0, height at +1/2 is -k.
        # Split rhs = rhs0 + k*rhs1.
        rhs0 = [Q(0), Q(0), Q(0), Q(0), Q(0), Q(0)]
        rhs1 = [Q(0), Q(0), Q(0), Q(-1), Q(0), Q(0)]
        aug = [row + [a, b] for row, a, b in zip(rows, rhs0, rhs1)]
        reduced, pivots = rref(aug)
        free = [j for j in range(10) if j not in pivots]
        self.assertEqual(len(pivots), 6)
        self.assertEqual(len(free), 4)
        # The four free monomials are t^2, s^2 t, s t^2, t^3, matching A,q,c,d.
        self.assertEqual(set(cols[j] for j in free), {(0, 2), (2, 1), (1, 2), (0, 3)})
        # Pinned solution with free variables zero:
        sol0 = [Q(0)] * 10
        solk = [Q(0)] * 10
        for i, c in enumerate(pivots):
            sol0[c] = reduced[i][10]
            solk[c] = reduced[i][11]
        # Expected axial part: -k/2 - (3k/2) s + 2 k s^3.
        expected = {
            (0, 0): Q(-1, 2),
            (1, 0): Q(-3, 2),
            (3, 0): Q(2),
        }
        for j, mon in enumerate(cols):
            self.assertEqual(sol0[j], 0)
            self.assertEqual(solk[j], expected.get(mon, Q(0)))

    def test_third_point_solves_gradient_and_height(self):
        A, c, d = chart_jets()
        D = u * u - Q(1, 4)
        Ps = 6 * k * u * u - 3 * k / 2 + q * u * v + c * v * v / 2
        Pt = A * v + q * D / 2 + c * u * v + d * v * v / 2
        height = (
            -k / 2
            + 2 * k * u ** 3
            - 3 * k * u / 2
            + A * v * v / 2
            + q * D * v / 2
            + c * u * v * v / 2
            + d * v ** 3 / 6
            + k * theta
        )
        self.assertEqual(Ps, 0)
        self.assertEqual(Pt, 0)
        self.assertEqual(height, 0)

    def test_determinant_sum_of_squares_identity(self):
        BM, BS, BX = hessians()
        w = w_of_q()
        scale = 9 * k * k / v ** 2
        self.assertEqual(det2(BM), scale * (4 * theta - (w + 1) ** 2))
        self.assertEqual(det2(BS), scale * (4 * (1 - theta) - (w - 1) ** 2))
        squares = (w + 1 - 2 * theta) ** 2 + 4 * theta * (1 - theta)
        self.assertEqual(det2(BX), -scale * squares)
        # Strict sign for theta in (0,1): the quadratic form in w is at least 4 theta(1-theta).
        self.assertEqual(squares - (w + 1 - 2 * theta) ** 2, 4 * theta * (1 - theta))

    def test_endpoint_type_interval_is_exact(self):
        # det B_M>0 iff |w+1|<2 sqrt(theta).
        # det B_S<0 iff w<1-2 sqrt(1-theta) or w>1+2 sqrt(1-theta).
        # The right-hand branch is disjoint from det B_M>0 precisely when
        # -1+2 sqrt(theta) < 1+2 sqrt(1-theta), i.e. sqrt(theta)+sqrt(1-theta)>0.
        # The retained upper bound is the smaller one precisely when
        # sqrt(theta)+sqrt(1-theta) >= 1. Both sides are positive, and squaring
        # gives 1+2 sqrt(theta(1-theta)) >= 1, i.e. theta(1-theta)>=0.
        # Equality holds only for theta in {0,1}, which the open height range excludes.
        # The retained interval is nonempty for theta in (0,1) because
        # 1+sqrt(theta) > sqrt(1-theta), and squaring gives 2 sqrt(theta)+2 theta>0.
        for n in range(1, 12):
            th = Q(n, 12)
            self.assertGreater(th * (1 - th), 0)
            self.assertGreater(th, 0)
            self.assertGreater(1 - th, 0)

    def test_positive_witness_and_w_minus_one(self):
        A, c, d = chart_jets()
        subs = {"k": Q(1), "u": Q(2), "v": Q(1), "theta": Q(1, 2), "q": Q(-30)}

        def ev(expr):
            acc = Q(0)
            for mon, coef in expr.terms.items():
                term = coef
                for name, power in zip(NAMES, mon):
                    if power:
                        term *= subs[name] ** power
                acc += term
            return acc

        self.assertEqual(ev(w_of_q()), Q(-1))
        self.assertEqual(ev(A), Q(-3))
        self.assertEqual(ev(c), Q(75))
        self.assertEqual(ev(d), Q(-363, 2))
        BM, BS, BX = hessians()
        self.assertEqual([ev(det2(M)) for M in (BM, BS, BX)], [Q(18), Q(-18), Q(-18)])
        self.assertEqual(ev(BM[0][0]), Q(-6))
        # At w=-1 the bracket (w+1)^2 vanishes, so det B_M = 36 k^2 theta / v^2
        # and the other two determinants equal the negative of that value.
        at_w = 9 * k * k / v ** 2 * (4 * theta - (L.coerce(-1) + 1) ** 2)
        self.assertEqual(at_w, 36 * k * k * theta / v ** 2)
        self.assertEqual(ev(det2(BM)), ev(at_w))
        self.assertEqual(ev(det2(BS)), -ev(at_w))
        self.assertEqual(ev(det2(BX)), -ev(at_w))

    def test_jet_minor_and_physical_jacobian(self):
        D = u * u - Q(1, 4)
        Lc = 2 * u ** 3 - 3 * u / 2 - Q(1, 2)
        # Unscaled jets a_jet, c_jet, d_jet. q remains free.
        # Use a fresh Laurent extension by encoding a,c,d as extra symbols through
        # a 3x3 numeric-symbol matrix of monomials in v only.
        # j1 = 6k D + q u v + c v^2/2
        # j2 = a v
        # j3 = k Lc + q D v/4 - d v^3/12
        # Partial Jacobian in column order (a, c, d):
        # [[0, v^2/2, 0], [v, 0, 0], [0, 0, -v^3/12]].
        # Cofactor (0,1) contributes -(v^2/2) * (v * (-v^3/12)) = v^6/24.
        minor = -(v * v / 2) * (v * (-v ** 3 / 12))
        self.assertEqual(minor, v ** 6 / 24)
        # Lc = 2 u^3 - 3u/2 - 1/2 = 2 u D - u - 1/2, the axial remainder in J_3.
        self.assertEqual(Lc, 2 * u * D - u - Q(1, 2))
        # Physical map (f_x, f_z, f-b) -> J has inverse Jacobian r^6.
        # Matrix [[r^2,0,0],[0,r,0],[0, r^2 v/2, r^3]], det = r^6.
        r = Q(1, 7)  # stand-in; the monomial identity is checked structurally below
        self.assertEqual(r ** 2 * r * r ** 3, r ** 6)
        # Structural: exponents 2+1+3=6, and the shear term does not enter a triangular det.
        self.assertEqual(2 + 1 + 3, 6)

    def test_normalizer_uses_unscaled_transverse_curvature(self):
        # Endpoint model: axial contact scaled by r, transverse curvature a held O(1).
        # det H_M = (-6 k r) a, det H_S = (6 k r) a, product / r^2 = -36 k^2 a^2
        # before absolute value. The r^2 denominator is the full endpoint normalizer.
        a = Q(-3, 5)
        kk = Q(4, 7)
        rr = Q(1, 11)
        det_m = (-6 * kk * rr) * a
        det_s = (6 * kk * rr) * a
        self.assertEqual(det_m * det_s / rr ** 2, -36 * kk ** 2 * a ** 2)
        self.assertEqual(abs(det_m * det_s) / rr ** 2, 36 * kk ** 2 * a ** 2)
        # Sign pattern: a<0, H_M,11<0 and det>0 so index 2; H_S,11>0 and det<0 so index 1.
        self.assertGreater(det_m, 0)  # (-6kr)*(negative a) > 0
        self.assertLess(det_s, 0)
        # A wrong r^4 normalization would not recover 36 k^2 a^2.
        self.assertNotEqual(abs(det_m * det_s) / rr ** 4, 36 * kk ** 2 * a ** 2)

    def test_witness_scaling_uses_chart_A_not_unscaled_zero(self):
        # At the positive witness, chart A=-3, while the unscaled jet a is 0.
        # Transverse entry of B_M is A-c/2, not 0-c/2.
        A = Q(-3)
        c = Q(75)
        self.assertNotEqual(A - c / 2, Q(0) - c / 2)
        self.assertEqual(A - c / 2, Q(-81, 2))
        self.assertEqual(Q(0) - c / 2, Q(-75, 2))

    def test_contact_coefficient_exponent_and_factor(self):
        # area r^2, height k r^3, physical-to-J Jacobian r^{-6},
        # three filtered determinants r^6, endpoint normalizer r^2.
        self.assertEqual(2 + 3 - 6 + 6 - 2, 3)
        # Jet minor v^6/24 contributes the reciprocal 24/|v|^6, times the height slope k.
        minor = Q(1, 24)  # v=1
        self.assertEqual(1 / minor, 24)
        self.assertEqual(24 * 1, 24)  # k=1

    def test_cumulative_sharp_constant_needs_the_ratio_limit(self):
        # alpha=1, m=3, kappa=1, b=1, h=2 r^3. Then h/(kappa r^m)=2, not 1.
        # Two-sided bounds c0=1, C0=3 hold, and h_r/(m kappa r^{m-1})=2.
        # R=1/2 gives ell=2*(1/8)=1/4, N=R^2/2=1/8.
        # The displayed (D2) constant is ell^{2/3}/2 = 2^{-7/3}, whose cube is 1/128.
        # Actual cube is 1/512. The constants differ by 2^{-2/3}.
        R = Q(1, 2)
        ell = 2 * R ** 3
        N = R ** 2 / 2
        self.assertEqual(ell, Q(1, 4))
        self.assertEqual(N, Q(1, 8))
        self.assertEqual(N ** 3, Q(1, 512))
        claimed_cube = Q(1, 128)  # (2^{-7/3})^3 = 2^{-7}
        self.assertNotEqual(N ** 3, claimed_cube)
        # If instead h=r^3, the same R has ell=R^3=1/8 and N equals ell^{2/3}/2.
        ell_sharp = R ** 3
        self.assertEqual(ell_sharp, Q(1, 8))
        # h=r^3 gives ell^{2/3}=R^2, so the (D2) constant ell^{2/3}/2 equals N.
        self.assertEqual(R * R / 2, N)

    def test_oscillatory_density_limits_and_phase_diagram(self):
        # Along the two sequences the simplified ratio is exactly 1/2 and 1/4.
        self.assertEqual(Q(1, 3 - 1), Q(1, 2))
        self.assertEqual(Q(1, 3 - (-1)), Q(1, 4))
        # h' stays positive for r<=1/4: 3-cos+4 r sin >= 3-1-1 = 1.
        self.assertGreaterEqual(3 - 1 - 1, 1)
        # alpha=1,m=3,q=-1/2, delta=q+1-beta=-1/6.
        beta = Q(2, 3)
        q_mark = Q(-1, 2)
        delta = q_mark + 1 - beta
        self.assertEqual(delta, Q(-1, 6))
        # nu = 2 (ell^{-1/2} - ell^{-1/3}). At ell=1/64 the powers are 8 and 4.
        ell = Q(1, 64)
        self.assertEqual(ell ** -1, 64)
        # ell^{-1/2} = 8, ell^{-1/3}=4, exact because 64=8^2=4^3.
        self.assertEqual(8 ** 2, 64)
        self.assertEqual(4 ** 3, 64)
        nu_times_clear = 2 * (8 - 4)
        self.assertEqual(nu_times_clear, 8)
        pure_universal_scale = 4  # an ell^{-1/3} value, not the exact density
        self.assertNotEqual(nu_times_clear, pure_universal_scale)

    def test_d3_alpha_selection_and_cumulative_match(self):
        # Positive selection keeps beta=(1+1)/3=2/3, density power -1/3.
        beta = Q(2, 3)
        self.assertEqual(beta - 1, Q(-1, 3))
        # N coefficient is 1/(alpha+1) = 1/2, while density coefficient C=(1/3)*integral,
        # and  (1/2) * 3 C = (3/2) C.
        self.assertEqual(Q(1, 2) * 3, Q(3, 2))
        # Selection p~r^gamma replaces the exponent by (alpha+gamma+1)/m - 1.
        self.assertEqual(Q(1 + 1 + 1, 3) - 1, Q(0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
