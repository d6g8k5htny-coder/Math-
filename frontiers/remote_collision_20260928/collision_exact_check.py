"""Exact finite controls for CL-D5-REMOTE-COLLISION-20260928-v1 (frontiers/remote_collision_20260928/PROOF.md).

Python standard library only; exact rational / Laurent-polynomial arithmetic. Checks:

  T   trapezoid identity (4.2): D3 = -(1/12) * positive mass-one average of g''', and G_delta as the average of g'';
  J   the Jacobian delta^(-d-3) of the divided-difference coordinates (4.3), d = 2, 3;
  S   surjectivity of H -> He on Sym_d for exact rational unit e (the delta = 0 rank of Lemma 1), d = 2, 3;
  DT  det(H)^2 <= |He|^2 ||H||_F^(2(d-1)) on exact random matrices (Lemma 4), with equality on a diagonal family;
  F   the fold example: two critical points at distance delta differ in height by exactly -(1/12) f''' delta^3;
  L   delta- and r-power ledgers, and the exact integral of delta*min(1, a/delta^3) = (3/2) a^(2/3) at a = q^3;
  B   Bonferroni inequalities N - N(N-1)/2 <= 1{N>=1} <= N and 1{N>=2} <= N(N-1)/2.

Not a continuum or Gaussian proof.
"""
import argparse
import itertools
import json
import random
import sys
from fractions import Fraction as F


def _mono_mul(a, b):
    d = dict(a)
    for v, e in b:
        n = d.get(v, 0) + e
        if n:
            d[v] = n
        else:
            d.pop(v, None)
    return tuple(sorted(d.items()))


class P:
    __slots__ = ("t",)

    def __init__(self, t=None):
        self.t = {m: c for m, c in (t or {}).items() if c != 0}

    @staticmethod
    def c(x):
        return P({(): F(x)})

    @staticmethod
    def v(name, e=1):
        return P({((name, e),): F(1)})

    @staticmethod
    def lift(o):
        return o if isinstance(o, P) else P.c(o)

    def __add__(self, o):
        o = P.lift(o)
        t = dict(self.t)
        for m, c in o.t.items():
            t[m] = t.get(m, 0) + c
        return P(t)

    __radd__ = __add__

    def __neg__(self):
        return P({m: -c for m, c in self.t.items()})

    def __sub__(self, o):
        return self + (-P.lift(o))

    def __rsub__(self, o):
        return P.lift(o) - self

    def __mul__(self, o):
        o = P.lift(o)
        t = {}
        for m1, c1 in self.t.items():
            for m2, c2 in o.t.items():
                m = _mono_mul(m1, m2)
                t[m] = t.get(m, 0) + c1 * c2
        return P(t)

    __rmul__ = __mul__

    def __pow__(self, n):
        out = P.c(1)
        for _ in range(n):
            out = out * self
        return out

    def is_zero(self):
        return not self.t

    def d(self, name):
        t = {}
        for m, c in self.t.items():
            dm = dict(m)
            e = dm.get(name, 0)
            if e == 0:
                continue
            if e == 1:
                dm.pop(name)
            else:
                dm[name] = e - 1
            key = tuple(sorted(dm.items()))
            t[key] = t.get(key, 0) + c * e
        return P(t)

    def antider(self, name):
        t = {}
        for m, c in self.t.items():
            dm = dict(m)
            e = dm.get(name, 0)
            if e == -1:
                raise ValueError("log term")
            dm[name] = e + 1
            key = tuple(sorted(dm.items()))
            t[key] = t.get(key, 0) + c / (e + 1)
        return P(t)

    def subs(self, name, q):
        q = P.lift(q)
        out = P()
        for m, c in self.t.items():
            dm = dict(m)
            e = dm.pop(name, 0)
            if e < 0:
                raise ValueError("negative power substitution")
            rest = P({tuple(sorted(dm.items())): c})
            out = out + rest * (q ** e)
        return out

    def integrate(self, name, lo, hi):
        a = self.antider(name)
        return a.subs(name, hi) - a.subs(name, lo)

    def coeff(self, name, e):
        """Coefficient of name^e (as a polynomial in the other variables)."""
        t = {}
        for m, c in self.t.items():
            dm = dict(m)
            if dm.get(name, 0) != e:
                continue
            dm.pop(name, None)
            key = tuple(sorted(dm.items()))
            t[key] = t.get(key, 0) + c
        return P(t)

    def exponents(self, name):
        return sorted({dict(m).get(name, 0) for m in self.t})


def det(M):
    n = len(M)
    total = P()
    for perm in itertools.permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])
        term = P.c(-1 if inv % 2 else 1)
        for i in range(n):
            term = term * M[i][perm[i]]
        total = total + term
    return total


def adj(M):
    n = len(M)
    out = [[P() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [[M[a][b] for b in range(n) if b != j] for a in range(n) if a != i]
            cof = det(minor) if minor else P.c(1)
            out[j][i] = cof if (i + j) % 2 == 0 else -cof
    return out


def check_t(mut):
    t, dl, dli = P.v("t"), P.v("dl"), P.v("dl", -1)
    g = sum((P.v("g%d" % i) * t ** i for i in range(10)), P())
    g1, g2, g3 = g.d("t"), g.d("t").d("t"), g.d("t").d("t").d("t")
    at = lambda p, v: p.subs("t", v)
    D3 = (at(g, dl) - at(g, P.c(0))) * dli ** 3 - (at(g1, P.c(0)) + at(g1, dl)) * dli ** 2 * F(1, 2)
    const = F(-1, 6) if mut == "trapezoid-constant" else F(-1, 12)
    w = 6 * t * (dl - t) * dli ** 3
    avg3 = (w * g3).integrate("t", P.c(0), dl)
    Gd = (at(g1, dl) - at(g1, P.c(0))) * dli
    return {
        "D3_is_minus_one_twelfth_average_of_g3": (D3 - const * avg3).is_zero(),
        "trapezoid_weight_mass_one": (w.integrate("t", P.c(0), dl) - 1).is_zero(),
        "G_delta_is_average_of_g2": (Gd - dli * g2.integrate("t", P.c(0), dl)).is_zero(),
        "D3_has_no_negative_power_of_delta": min(D3.exponents("dl") or [0]) >= 0,
    }


def check_j(mut):
    out = {}
    dl, dli = P.v("dl"), P.v("dl", -1)
    for d in (2, 3):
        n = 2 * d + 2
        # Rows: grad f(x) (d), G (d), f(x), D3 ; columns: grad f(x) (d), grad f(x') (d), f(x), f(x').
        M = [[P() for _ in range(n)] for _ in range(n)]
        e = [P.v("e%d" % i) for i in range(d)]
        for i in range(d):
            M[i][i] = P.c(1)
            M[d + i][i] = -dli
            M[d + i][d + i] = dli
        M[2 * d][2 * d] = P.c(1)
        # D3 = (f' - f)/dl^3 - (1/(2 dl^2)) e.(grad f + grad f')
        M[2 * d + 1][2 * d] = -dli ** 3
        M[2 * d + 1][2 * d + 1] = dli ** 3
        for i in range(d):
            M[2 * d + 1][i] = -e[i] * dli ** 2 * F(1, 2)
            M[2 * d + 1][d + i] = -e[i] * dli ** 2 * F(1, 2)
        expo = -(d + 2) if mut == "jacobian-exponent" else -(d + 3)
        out["jacobian_delta^-(d+3)_d%d" % d] = (det(M) - P.v("dl", expo)).is_zero()
    return out


def rational_unit(rng, d):
    if d == 2:
        q = F(rng.randrange(-30, 31), rng.randrange(1, 11))
        n = 1 + q * q
        return [(1 - q * q) / n, 2 * q / n]
    u = F(rng.randrange(-30, 31), rng.randrange(1, 11))
    w = F(rng.randrange(-30, 31), rng.randrange(1, 11))
    n = 1 + u * u + w * w
    return [2 * u / n, 2 * w / n, (1 - u * u - w * w) / n]


def fdet(A):
    n = len(A)
    M = [list(r) for r in A]
    dv = F(1)
    for c in range(n):
        piv = next((i for i in range(c, n) if M[i][c] != 0), None)
        if piv is None:
            return F(0)
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            dv = -dv
        dv *= M[c][c]
        for i in range(c + 1, n):
            fac = M[i][c] / M[c][c]
            M[i] = [a - fac * b for a, b in zip(M[i], M[c])]
    return dv


def rank(A):
    M = [list(r) for r in A]
    rk, rows, cols = 0, len(M), len(M[0])
    for c in range(cols):
        piv = next((i for i in range(rk, rows) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        for i in range(rows):
            if i != rk and M[i][c] != 0:
                fac = M[i][c] / M[rk][c]
                M[i] = [a - fac * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk


def check_s(mut):
    rng = random.Random(28)
    ok = True
    for d in (2, 3):
        basis = [(i, j) for i in range(d) for j in range(i, d)]
        for _ in range(200):
            e = rational_unit(rng, d)
            # Linear map Sym_d -> R^d, H -> He, in the basis E_ij (+E_ji).
            cols = []
            for (i, j) in basis:
                v = [F(0)] * d
                if i == j:
                    v[i] += e[i]
                else:
                    v[i] += e[j]
                    v[j] += e[i]
                cols.append(v)
            A = [[cols[c][rr] for c in range(len(basis))] for rr in range(d)]
            ok &= rank(A) == d
    return {"H_to_He_is_onto_for_rational_unit_e_d2_d3": ok}


def check_dt(mut):
    rng = random.Random(4)
    ok, eq = True, True
    for d in (2, 3):
        for _ in range(1500):
            H = [[F(0)] * d for _ in range(d)]
            for i in range(d):
                for j in range(i, d):
                    v = F(rng.randrange(-50, 51), rng.randrange(1, 8))
                    H[i][j] = H[j][i] = v
            e = rational_unit(rng, d)
            He = [sum(H[i][j] * e[j] for j in range(d)) for i in range(d)]
            he2 = sum(v * v for v in He)
            fro2 = sum(H[i][j] ** 2 for i in range(d) for j in range(d))
            ok &= fdet(H) ** 2 <= he2 * fro2 ** (d - 1)
        # Equality family: H = diag(lam, big, ..., big) with 0 < lam <= big and e = e_1 gives
        # |det H| = |He| ||H||_op^(d-1) exactly (||H||_op = big).
        for _ in range(50):
            lam = F(rng.randrange(1, 40), rng.randrange(1, 5))
            big = lam + F(rng.randrange(0, 40), rng.randrange(1, 5))
            H = [[F(0)] * d for _ in range(d)]
            H[0][0] = lam
            for i in range(1, d):
                H[i][i] = big
            He = [H[i][0] for i in range(d)]
            he2 = sum(v * v for v in He)
            eq &= fdet(H) ** 2 == he2 * big ** (2 * (d - 1))
    return {"det_squared_le_He2_times_Frobenius_power": ok, "equality_with_operator_norm_on_diagonal_family_d2_d3": eq}


def check_f(mut):
    t, eps = P.v("t"), P.v("eps")
    # f(t) = t^3/3 - eps t, critical points -+ sqrt(eps); write sqrt(eps) = q.
    q = P.v("q")
    f = t ** 3 * F(1, 3) - q * q * t
    dfp = (f.subs("t", q) - f.subs("t", -q))
    delta = 2 * q
    f3 = f.d("t").d("t").d("t")
    const = F(-1, 6) if mut == "trapezoid-constant" else F(-1, 12)
    return {
        "fold_critical_points": (f.d("t").subs("t", q)).is_zero() and (f.d("t").subs("t", -q)).is_zero(),
        "fold_height_gap_is_minus_f3_delta3_over_12": (dfp - const * f3 * delta ** 3).is_zero(),
    }


def check_l(mut):
    out = {}
    ok = True
    for d in range(2, 9):
        dets = 1 if mut == "one-determinant" else 2
        ok &= (d - 1) - (d + 3) + 3 + dets == 1
    out["delta_exponent_is_1_for_all_d"] = ok
    # r ledger: W r^2, first window r^3, divide Z r^2, delta integral r^2 -> r^5 ; separated r^2 r^6 / r^2 -> r^6
    win = 2 if mut == "window-factor" else 3
    out["near_r_exponent_5"] = 2 + win - 2 + 2 == 5
    out["separated_r_exponent_6"] = 2 + 2 * win - 2 == 6
    # integral_0^inf delta*min(1, a/delta^3) with a = q^3: split at q.
    q, dl = P.v("q"), P.v("dl")
    first = dl.integrate("dl", P.c(0), q)
    # integral_q^inf q^3 dl^-2 d dl = [-q^3/dl]_q^inf = q^3 / q = q^2 (antiderivative evaluated by hand)
    second_val = q ** 3 * P.v("q", -1)
    out["exact_integral_three_halves_a_two_thirds"] = ((first + second_val) - q * q * F(3, 2)).is_zero()
    return out


def check_b(mut):
    ok1 = ok2 = True
    for N in range(61):
        ind1 = 1 if N >= 1 else 0
        lower = N - F(N * (N - 1), 2) if mut != "bonferroni-sign" else N + F(N * (N - 1), 2)
        ok1 &= lower <= ind1 <= N
        ok2 &= (1 if N >= 2 else 0) <= F(N * (N - 1), 2)
    return {"bonferroni_first_order": ok1, "two_or_more_le_half_factorial_moment": ok2}


MUTANTS = ("jacobian-exponent", "trapezoid-constant", "one-determinant", "window-factor", "bonferroni-sign")


def flatten(dd):
    for v in dd.values():
        if isinstance(v, dict):
            yield from flatten(v)
        else:
            yield v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    mut = ap.parse_args().mutant
    groups = {
        "T_trapezoid_and_divided_difference": check_t(mut),
        "J_jacobian": check_j(mut),
        "S_rank_at_collision": check_s(mut),
        "DT_determinant_inequality": check_dt(mut),
        "F_fold_example": check_f(mut),
        "L_ledgers": check_l(mut),
        "B_bonferroni": check_b(mut),
    }
    passed = all(flatten(groups))
    res = {"checks": groups, "passed": passed, "scientific_effect": "NONE",
           "scope": "exact identities and ledgers only; Gaussian and Kac-Rice steps are argued in PROOF.md"}
    sys.stdout.write(json.dumps(res, indent=2, sort_keys=True) + "\n")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
