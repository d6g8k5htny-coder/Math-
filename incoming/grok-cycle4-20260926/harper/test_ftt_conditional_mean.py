"""Exact series for E[f_tt | six pins] on planar BF.

Scientific effect: NONE. Stdlib reproduction of the conditional-mean series
displayed in D5_OBSTRUCTION_LEDGER.md. Not a uniform estimate and not a
count lemma.

Pins: f(M)=b, f_t(M)=0, f_s(M)=0, f(S)=b-k r^3, f_t(S)=0, f_s(S)=0.
Transverse pins drop out by s-parity. The four-pin Gram and the cross vector
of f_tt(M) are those of CLOSED_FORMS_FTS_FTT.md / the six-pin Hessian note.
"""
from __future__ import annotations

from fractions import Fraction
import itertools
import math
import unittest

ORDER = 24


def _z() -> list[Fraction]:
    return [Fraction(0)] * (ORDER + 1)


def _mono(k: int, c: Fraction | int = 1) -> list[Fraction]:
    a = _z()
    if 0 <= k <= ORDER:
        a[k] = Fraction(c)
    return a


def _add(*terms: list[Fraction]) -> list[Fraction]:
    out = _z()
    for t in terms:
        for i, c in enumerate(t):
            out[i] += c
    return out


def _scale(a: list[Fraction], c: Fraction | int) -> list[Fraction]:
    return [x * Fraction(c) for x in a]


def _mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = _z()
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if i + j > ORDER:
                break
            out[i + j] += ai * bj
    return out


def _c() -> list[Fraction]:
    """exp(-r^2/2) through r^ORDER."""
    out = _z()
    n = 0
    while 2 * n <= ORDER:
        out[2 * n] = Fraction((-1) ** n, (2**n) * math.factorial(n))
        n += 1
    return out


def _det(rows: list[list[list[Fraction]]]) -> list[Fraction]:
    n = len(rows)
    out = _z()
    for perm in itertools.permutations(range(n)):
        inv = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = _mono(0, 1 if inv % 2 == 0 else -1)
        for i in range(n):
            term = _mul(term, rows[i][perm[i]])
        out = _add(out, term)
    return out


def _minor(rows: list[list[list[Fraction]]], i: int, j: int) -> list[list[list[Fraction]]]:
    return [[rows[a][b] for b in range(4) if b != j] for a in range(4) if a != i]


def _gram() -> list[list[list[Fraction]]]:
    c = _c()
    r = _mono(1)
    r2 = _mul(r, r)
    one = _mono(0)
    rc = _mul(r, c)
    one_m_r2_c = _mul(_add(one, _scale(r2, -1)), c)
    z = _z()
    return [
        [one, z, c, _scale(rc, -1)],
        [z, one, rc, one_m_r2_c],
        [c, rc, one, z],
        [_scale(rc, -1), one_m_r2_c, z, one],
    ]


def _cross_m() -> list[list[Fraction]]:
    """Cov(f_tt(M), (f(M), f_t(M), f(S), f_t(S)))."""
    c = _c()
    r = _mono(1)
    r2 = _mul(r, r)
    one = _mono(0)
    return [
        _scale(one, -1),
        _z(),
        _mul(_add(r2, _scale(one, -1)), c),
        _mul(_mul(r, _add(_mono(0, 3), _scale(r2, -1))), c),
    ]


def _cross_s() -> list[list[Fraction]]:
    """Cov(f_tt(S), (f(M), f_t(M), f(S), f_t(S))).

    With z = S - M = (r, 0) and K = exp(-r^2/2),
    Cov(f_tt(S), f(M)) = (r^2 - 1) K,
    Cov(f_tt(S), f_t(M)) = r (r^2 - 3) K.
    """
    c = _c()
    r = _mono(1)
    r2 = _mul(r, r)
    one = _mono(0)
    return [
        _mul(_add(r2, _scale(one, -1)), c),
        _mul(_mul(r, _add(r2, _scale(_mono(0, 3), -1))), c),
        _scale(one, -1),
        _z(),
    ]


def _apply_adj(g: list[list[list[Fraction]]], v: list[list[Fraction]]) -> list[list[Fraction]]:
    w: list[list[Fraction]] = []
    for i in range(4):
        acc = _z()
        for j in range(4):
            sign = 1 if (i + j) % 2 == 0 else -1
            acc = _add(acc, _scale(_mul(_det(_minor(g, j, i)), v[j]), sign))
        w.append(acc)
    return w


def _dot(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[Fraction]:
    return _add(*[_mul(x, y) for x, y in zip(a, b)])


def _div(num: list[Fraction], den: list[Fraction]) -> list[Fraction]:
    kd = next(i for i, c in enumerate(den) if c != 0)
    q = _z()
    for p in range(ORDER + 1):
        s = num[p]
        for j in range(kd + 1, p + 1):
            pj = p - j
            if 0 <= pj <= ORDER:
                s -= den[j] * q[pj]
        idx = p - kd
        if idx < 0:
            if s != 0:
                raise AssertionError(f"numerator has a term below det order at r^{p}")
            continue
        q[idx] = s / den[kd]
    return q


def _regression(cross: list[list[Fraction]]) -> tuple[list[Fraction], list[Fraction], list[Fraction]]:
    """Return (b-coefficients, k-coefficients, variance series) of the regression."""
    g = _gram()
    det = _det(g)
    r3 = _mul(_mul(_mono(1), _mono(1)), _mono(1))
    vb = [_mono(0), _z(), _mono(0), _z()]
    vk = [_z(), _z(), _scale(r3, -1), _z()]
    mb = _div(_dot(cross, _apply_adj(g, vb)), det)
    mk = _div(_dot(cross, _apply_adj(g, vk)), det)
    # Var = 3 - cross · G^{-1} cross.
    quad = _div(_dot(cross, _apply_adj(g, cross)), det)
    var = _add(_mono(0, 3), _scale(quad, -1))
    return mb, mk, var


_MB, _MK, _VAR_M = _regression(_cross_m())
_SB, _SK, _VAR_S = _regression(_cross_s())


class ConditionalMeanFtt(unittest.TestCase):
    def test_mean_at_m_matches_ledger(self) -> None:
        expect_b = {
            2: Fraction(-1, 4),
            4: Fraction(1, 24),
            6: Fraction(-1, 192),
            8: Fraction(1, 5760),
        }
        expect_k = {
            1: Fraction(-6),
            3: Fraction(1),
            5: Fraction(-1, 20),
            7: Fraction(-1, 120),
        }
        for p in range(0, 9):
            self.assertEqual(_MB[p], expect_b.get(p, Fraction(0)), f"b r^{p}")
            self.assertEqual(_MK[p], expect_k.get(p, Fraction(0)), f"k r^{p}")

    def test_mean_at_s_matches_ledger(self) -> None:
        expect_b = {
            2: Fraction(-1, 4),
            4: Fraction(1, 24),
            6: Fraction(-1, 192),
            8: Fraction(1, 5760),
        }
        expect_k = {
            1: Fraction(6),
            3: Fraction(-1),
            5: Fraction(3, 10),
            7: Fraction(-1, 30),
        }
        for p in range(0, 9):
            self.assertEqual(_SB[p], expect_b.get(p, Fraction(0)), f"b r^{p}")
            self.assertEqual(_SK[p], expect_k.get(p, Fraction(0)), f"k r^{p}")

    def test_variance_matches_identity_tt_and_agrees_at_s(self) -> None:
        expect = {
            4: Fraction(1, 6),
            6: Fraction(-1, 30),
            8: Fraction(1, 360),
            10: Fraction(-1, 12600),
        }
        for p in range(0, 11):
            self.assertEqual(_VAR_M[p], expect.get(p, Fraction(0)), f"Var_M r^{p}")
            self.assertEqual(_VAR_S[p], _VAR_M[p], f"Var_S r^{p}")

    def test_second_moment_through_r5(self) -> None:
        # E[(f_tt(M)+6kr)^2 | pins] = (mu + 6kr)^2 + Var.
        # Leading terms: (b^2/16 + 1/6) r^4 - (b k / 2) r^5.
        # (b^2/16 + 1/6, -b k / 2)
        cases = {
            (1, 0): (Fraction(11, 48), Fraction(0)),
            (0, 1): (Fraction(1, 6), Fraction(0)),
            (1, 1): (Fraction(11, 48), Fraction(-1, 2)),
            (2, 3): (Fraction(1, 4) + Fraction(1, 6), Fraction(-3)),
        }
        for (b, k), (c4, c5) in cases.items():
            rem = _add(_scale(_MB, b), _scale(_MK, k), _mono(1, 6 * k))
            square = _mul(rem, rem)
            moment = _add(square, _VAR_M)
            self.assertEqual(moment[4], c4, f"(b,k)={(b, k)} r^4")
            self.assertEqual(moment[5], c5, f"(b,k)={(b, k)} r^5")

    def test_float_regression_at_one_radius(self) -> None:
        r = 0.35
        c = math.exp(-r * r / 2)
        g = [
            [1.0, 0.0, c, -r * c],
            [0.0, 1.0, r * c, (1 - r * r) * c],
            [c, r * c, 1.0, 0.0],
            [-r * c, (1 - r * r) * c, 0.0, 1.0],
        ]
        u_m = [-1.0, 0.0, (r * r - 1) * c, r * (3 - r * r) * c]
        u_s = [(r * r - 1) * c, r * (r * r - 3) * c, -1.0, 0.0]

        def solve(u: list[float], v: list[float]) -> float:
            a = [g[i][:] + [v[i]] for i in range(4)]
            for col in range(4):
                piv = a[col][col]
                for j in range(col, 5):
                    a[col][j] /= piv
                for row in range(4):
                    if row == col:
                        continue
                    factor = a[row][col]
                    for j in range(col, 5):
                        a[row][j] -= factor * a[col][j]
            return sum(u[i] * a[i][4] for i in range(4))

        def series(bcoef: list[Fraction], kcoef: list[Fraction], b: int, k: int) -> float:
            return sum(float(bcoef[i]) * b * r**i + float(kcoef[i]) * k * r**i for i in range(ORDER + 1))

        for b, k in ((1, 0), (0, 1), (1, 1)):
            v = [float(b), 0.0, float(b) - k * r**3, 0.0]
            self.assertAlmostEqual(solve(u_m, v), series(_MB, _MK, b, k), delta=1e-11)
            self.assertAlmostEqual(solve(u_s, v), series(_SB, _SK, b, k), delta=1e-11)


if __name__ == "__main__":
    unittest.main()
