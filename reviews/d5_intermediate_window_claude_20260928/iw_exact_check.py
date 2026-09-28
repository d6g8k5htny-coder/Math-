"""Independent exact checks for the nonauthor review of OA-D5-INTERMEDIATE-WINDOW-20260928-v1 (Math-#107).

Python standard library only; exact rational Laurent-polynomial arithmetic. Written independently of the
author's algebra.py. Groups:

  H   epsilon-Hermite coefficient formulas, their divided-difference averages and the positive kernel of
      H'''(0) (the uniform remainder behind (I9));
  RK  nine-row rank at confluence epsilon=0: the -v^6 and u^10 witness minors on the kernel of the six
      contact functionals, and the degree-four collinear rank drop (negative control);
  EX  (I12)-(I16) for a GENERIC degree-six field with the six pins solved exactly: every stated order in r,
      the reduced vector Z has no negative power of s after r = epsilon*s, and its s^0 part is exactly
      mean + B J; also the physical Jacobian s^6;
  TR  the transverse matrix B: (C3,D3,S0) minor v^6/24 and Cauchy-Binet for det(BB^T);
  EU  the homogeneous Euler identity (I17) for a generic degree-six field;
  LG  (I21)-(I34) power and dyadic ledgers.

Not a continuum proof: covariance floors, Gaussian moments and Kac-Rice are argued in REVIEW.md.
"""
import argparse
import itertools
import json
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


def cf(e):
    return P.c(F(e))


def generic(deg, prefix="c"):
    x, z = P.v("x"), P.v("z")
    f = P()
    names = []
    for i in range(deg + 1):
        for j in range(deg + 1 - i):
            nm = "%s%d%d" % (prefix, i, j)
            names.append(nm)
            f = f + P.v(nm) * x ** i * z ** j
    return f, names


def at(p, X1, X2):
    return p.subs("x", X1).subs("z", X2)


def zero_orders(p, name):
    ex = p.exponents(name)
    return ex[0] if ex else 10 ** 6


def hermite(gm, gp, dgm, dgp, a, ainv):
    s0 = (gm + gp) * F(1, 2)
    d0 = (gp - gm) * ainv * F(1, 2)
    s1 = (dgm + dgp) * F(1, 2)
    d1 = (dgp - dgm) * ainv * F(1, 2)
    return s0 - a * a * d1 * F(1, 2), (3 * d0 - s1) * F(1, 2), d1, 3 * (s1 - d0) * ainv * ainv, (s0, d0, s1, d1)


# ---------------------------------------------------------------------------- H
def check_h(mut):
    out = {}
    t, a, ai = P.v("t"), P.v("a"), P.v("a", -1)
    g = sum((P.v("g%d" % i) * t ** i for i in range(10)), P())
    g1, g2, g3 = g.d("t"), g.d("t").d("t"), g.d("t").d("t").d("t")
    H0, H1, H2, H3, (s0, d0, s1, d1) = hermite(g.subs("t", -a), g.subs("t", a), g1.subs("t", -a), g1.subs("t", a), a, ai)
    # Reproduces every cubic exactly.
    cub = {"g%d" % i: P.c(0) for i in range(4, 10)}
    def trunc(p):
        for nm, val in cub.items():
            p = p.subs(nm, val)
        return p
    out["hermite_reproduces_cubics"] = all(
        (trunc(Hk) - want).is_zero() for Hk, want in
        ((H0, P.v("g0")), (H1, P.v("g1")), (H2, 2 * P.v("g2")), (H3, 6 * P.v("g3"))))
    kn = F(3, 2) if mut == "hermite-kernel" else F(3, 4)
    kern = (a * a - t * t)
    out["H3_is_positive_kernel_average_of_g3"] = (
        (H3 - kn * ai ** 3 * (kern * g3).integrate("t", -a, a)).is_zero()
        and (kn * ai ** 3 * kern.integrate("t", -a, a) - 1).is_zero())
    out["d0_d1_are_averages"] = (
        (d0 - ai * F(1, 2) * g1.integrate("t", -a, a)).is_zero()
        and (d1 - ai * F(1, 2) * g2.integrate("t", -a, a)).is_zero())
    # H0 = s0 - a^2 d1/2 has no inverse power of a: uniform as a -> 0.
    out["hermite_coefficients_have_no_inverse_powers_of_a"] = all(
        min(Hk.exponents("a") or [0]) >= 0 for Hk in (H0, H1, H2, H3))
    return out


# ---------------------------------------------------------------------------- RK
def contact(p):
    z0 = lambda q: at(q, P.c(0), P.c(0))
    px, pz = p.d("x"), p.d("z")
    return [z0(p), z0(px), z0(px.d("x")), z0(px.d("x").d("x")), z0(pz), z0(pz.d("x"))]


def witness_rows(p, U, V):
    return [at(p, U, V), at(p.d("x"), U, V), at(p.d("z"), U, V)]


def check_rk(mut):
    out = {}
    x, z, u, v = P.v("x"), P.v("z"), P.v("u"), P.v("v")
    fam_v = [z ** 2, z ** 3, x * z ** 2]
    fam_u = [x ** 4, x ** 5, x ** 2 * z]
    out["families_annihilate_contact_functionals"] = all(
        all(c.is_zero() for c in contact(p)) for p in fam_v + fam_u)
    Mv = [witness_rows(p, u, v) for p in fam_v]
    Mu = [witness_rows(p, u, P.c(0)) for p in fam_u]
    out["witness_minor_v_ne_0_is_-v^6"] = (det(Mv) + v ** 6).is_zero()
    out["witness_minor_v_eq_0_is_u^10"] = (det(Mu) - u ** 10).is_zero()

    def kernel_rank_has_nonzero_minor(deg):
        f, names = generic(deg)
        kill = {"c00", "c10", "c20", "c30", "c01", "c11"}
        for nm in kill:
            f = f.subs(nm, P.c(0))
        free = [nm for nm in names if nm not in kill]
        rows = witness_rows(f, u, P.c(0))
        Mat = [[r.coeff(nm, 1) for nm in free] for r in rows]
        for cols in itertools.combinations(range(len(free)), 3):
            if not det([[Mat[i][c] for c in cols] for i in range(3)]).is_zero():
                return True
        return False
    deg_pos = 4 if mut == "degree-four" else 5
    out["degree_five_kernel_rank_three_on_axis"] = kernel_rank_has_nonzero_minor(deg_pos)
    out["degree_four_kernel_rank_drops_on_axis"] = not kernel_rank_has_nonzero_minor(4)
    return out


# ---------------------------------------------------------------------------- EX / TR
def pinned_field():
    f, names = generic(6)
    x = P.v("x")
    R, RI = P.v("r"), P.v("r", -1)
    a, ai = R * F(1, 2), 2 * RI
    b, k = P.v("b"), P.v("k")
    h = sum((P.v("c%d0" % i) * x ** i for i in range(4, 7)), P())
    q = sum((P.v("c%d1" % i) * x ** i for i in range(2, 6)), P())
    Ht = hermite(b, b - k * R ** 3, P.c(0), P.c(0), a, ai)
    hh = hermite(h.subs("x", -a), h.subs("x", a), h.d("x").subs("x", -a), h.d("x").subs("x", a), a, ai)
    sol = {
        "c00": Ht[0] - hh[0], "c10": Ht[1] - hh[1],
        "c20": (Ht[2] - hh[2]) * F(1, 2), "c30": (Ht[3] - hh[3]) * F(1, 6),
        "c01": -(q.subs("x", a) + q.subs("x", -a)) * F(1, 2),
        "c11": -(q.subs("x", a) - q.subs("x", -a)) * ai * F(1, 2),
    }
    for nm, val in sol.items():
        f = f.subs(nm, val)
    return f


def check_ex_tr(mut):
    out = {}
    R = P.v("r")
    b, k = P.v("b"), P.v("k")
    f = pinned_field()
    fx, fz = f.d("x"), f.d("z")
    a = R * F(1, 2)
    zero = P.c(0)
    out["six_pins_hold_exactly"] = (
        (at(f, -a, zero) - b).is_zero() and (at(f, a, zero) - b + k * R ** 3).is_zero()
        and all(at(g, s_, zero).is_zero() for g in (fx, fz) for s_ in (-a, a)))
    o = lambda p: at(p, zero, zero)
    bbar = b - k * R ** 3 * F(1, 2)
    T3, C3, D3, S0 = 2 * P.v("c21"), 2 * P.v("c12"), 6 * P.v("c03"), 2 * P.v("c02")
    orders = {
        "f0_minus_bbar": (o(f) - bbar, 4),
        "fx0_plus_3kr2_over_2": (o(fx) + k * R ** 2 * F(3, 2), 4),
        "fz0_plus_r2T3_over_8": (o(fz) + R ** 2 * T3 * F(1, 8), 4),
        "fxx0": (o(fx.d("x")), 2),
        "fxz0": (o(fx.d("z")), 2),
        "fxxx0_minus_12k": (o(fx.d("x").d("x")) - 12 * k, 2),
    }
    out["I12_orders_in_r"] = {nm: zero_orders(p, "r") >= e for nm, (p, e) in orders.items()}
    # Reduced vector Z at X = s(u,v) with r = e s.
    s, u, v, e = P.v("s"), P.v("u"), P.v("v"), P.v("e")
    X1, X2 = s * u, s * v
    sub = lambda p: at(p, X1, X2).subs("r", e * s)
    fX, fxX, fzX = sub(f), sub(fx), sub(fz)
    bb = bbar.subs("r", e * s)
    Z1 = fxX * P.v("s", -2)
    Z2 = fzX * P.v("s", -1)
    if mut == "no-row-operation":
        Z3 = (fX - bb) * P.v("s", -3)
    else:
        Z3 = (fX - bb - s * v * F(1, 2) * fzX) * P.v("s", -3)
    de = u * u - e * e * F(1, 4)
    d3c = F(-1, 4) if mut == "d3-coefficient" else F(-1, 12)
    E1 = 6 * k * de + u * v * T3 + v * v * F(1, 2) * C3
    E2 = v * S0
    E3 = k * (2 * u ** 3 - F(3, 2) * e * e * u) + v * de * F(1, 4) * T3 + d3c * v ** 3 * D3
    Zs = (Z1, Z2, Z3)
    out["Z_has_no_negative_power_of_s"] = all(zero_orders(Zi, "s") >= 0 for Zi in Zs)
    ok = all(zero_orders(Zi, "s") >= 0 for Zi in Zs)
    out["Z_s^0_part_equals_mean_plus_BJ"] = ok and all(
        (Zi.coeff("s", 0) - Ei).is_zero() for Zi, Ei in zip(Zs, (E1, E2, E3)))
    # Physical Jacobian of (Z1,Z2,Z3) -> (f_x, f_z, f - bbar).
    Jm = [[s ** 2, zero, zero], [zero, s, zero], [zero, s * s * v * F(1, 2), s ** 3]]
    out["physical_jacobian_s^6"] = (det(Jm) - s ** 6).is_zero()
    # TR: B derived from the actual s^0 part, columns (T3, C3, D3, S0).
    if ok:
        base = [Zi.coeff("s", 0) for Zi in Zs]
        B = [[bi.coeff("c21", 1) * F(1, 2), bi.coeff("c12", 1) * F(1, 2),
              bi.coeff("c03", 1) * F(1, 6), bi.coeff("c02", 1) * F(1, 2)] for bi in base]
        minor_const = F(1, 12) if mut == "minor-constant" else F(1, 24)
        m_cds = det([[B[i][c] for c in (1, 2, 3)] for i in range(3)])
        out["minor_C3_D3_S0_is_v^6_over_24"] = (m_cds - minor_const * v ** 6).is_zero()
        BBt = [[sum((B[i][l] * B[j][l] for l in range(4)), P()) for j in range(3)] for i in range(3)]
        cb = sum((det([[B[i][c] for c in cols] for i in range(3)]) ** 2
                  for cols in itertools.combinations(range(4), 3)), P())
        out["cauchy_binet_det_BBt"] = (det(BBt) - cb).is_zero()
        out["B_entries_are_O_of_v"] = all(
            (B[i][j].is_zero() or min(B[i][j].exponents("v")) >= 1) for i in range(3) for j in range(4))
    else:
        out["minor_C3_D3_S0_is_v^6_over_24"] = False
        out["cauchy_binet_det_BBt"] = False
        out["B_entries_are_O_of_v"] = False
    return out


# ---------------------------------------------------------------------------- EU
def check_eu(mut):
    f, _ = generic(6)
    x, z = P.v("x"), P.v("z")
    o = lambda p: at(p, P.c(0), P.c(0))
    fx, fz = f.d("x"), f.d("z")
    lhs = 3 * (f - o(f)) - (x * fx + z * fz)
    low = 2 * (o(fx) * x + o(fz) * z) + F(1, 2) * (
        o(fx.d("x")) * x * x + 2 * o(fx.d("z")) * x * z + o(fz.d("z")) * z * z)
    diff = lhs - low
    ok = True
    for mono, c in diff.t.items():
        dm = dict(mono)
        deg = dm.get("x", 0) + dm.get("z", 0)
        ok &= deg >= 4
    # And the degree-j part is exactly (3-j) P_j.
    parts = P()
    for mono, c in f.t.items():
        dm = dict(mono)
        deg = dm.get("x", 0) + dm.get("z", 0)
        if deg >= 4:
            parts = parts + P({mono: c * (3 - deg)})
    return {"euler_cubic_terms_cancel": ok, "euler_remainder_is_sum_(3-j)P_j": (diff - parts).is_zero()}


# ---------------------------------------------------------------------------- LG
def check_lg(mut):
    out = {}
    K, s, v, r = P.v("K"), P.v("s"), P.v("v"), P.v("r")
    A = K * (r + s * s) * P.v("v", -2)
    W = r * r * K * K * A * A
    detHX = s * s * K * K * P.v("v", -2)
    ratio = W * detHX * P.v("r", -2)
    out["I21_ledger"] = (ratio - K ** 6 * s * s * (r + s * s) ** 2 * P.v("v", -6)).is_zero()
    lam = P.v("s", -6) * P.v("v", -6) * (ratio * P.v("K", -6)) * P.v("v", -48)
    out["I31_ledger"] = (lam - P.v("s", -4) * (r + s * s) ** 2 * P.v("v", -60)).is_zero()
    shell = lam * P.v("v", 60) * s * s * r ** 3
    bound = 2 * r ** 3 * (r * r * P.v("s", -2) + s ** 4 * P.v("s", -2) * 1)
    # 2 r^3 [(r/s)^2 + s^2] - r^3 (r+s^2)^2/s^2 = r^3 (r/s - s)^2 >= 0
    gap = 2 * r ** 3 * (r * r * P.v("s", -2) + s * s) - shell
    out["I32_shell_bound_gap_is_square"] = (gap - r ** 3 * (r * P.v("s", -1) - s) ** 2).is_zero()
    out["I34_geometric_sums_below_4_over_3"] = all(
        sum(F(1, 4 ** j) for j in range(n + 1)) < F(4, 3) for n in range(80))
    import random
    rng = random.Random(107)
    okr = True
    for _ in range(3000):
        sq = F(rng.randrange(1, 1000), 1000)
        rq = sq * F(rng.randrange(1, 251), 1000)  # r <= s/4
        okr &= rq ** 3 <= rq * rq * sq and rq * rq * sq * sq <= rq * rq * sq and rq * rq / sq <= rq / 4
    out["I18_I21_order_comparisons_exact_random"] = okr
    return out


MUTANTS = ("hermite-kernel", "degree-four", "d3-coefficient", "no-row-operation", "minor-constant")


def flatten(d):
    for k_, v_ in d.items():
        if isinstance(v_, dict):
            yield from flatten(v_)
        else:
            yield v_


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    mut = ap.parse_args().mutant
    groups = {
        "H_hermite_uniform_remainder": check_h(mut),
        "RK_confluent_rank": check_rk(mut),
        "EX_TR_pinned_expansion_and_transverse_block": check_ex_tr(mut),
        "EU_euler_identity": check_eu(mut),
        "LG_ledgers": check_lg(mut),
    }
    passed = all(flatten(groups))
    res = {"checks": groups, "passed": passed, "scientific_effect": "NONE",
           "scope": "exact identities only; covariance floors, Gaussian moments and Kac-Rice are argued in REVIEW.md"}
    sys.stdout.write(json.dumps(res, indent=2, sort_keys=True) + "\n")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
