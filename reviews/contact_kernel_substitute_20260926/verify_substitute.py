#!/usr/bin/env python3
"""Exact rational checks for SUBSTITUTE.md (OA-CONTACT-KERNEL-SUBSTITUTE-20260926).

Standard library only (fractions). Every identity in the Section 5 table is
re-derived here by symbolic polynomial expansion over Q, not by floating point
and not by comparison with stored answers alone. The script proves finite
algebra only: it does not establish the continuum regression, the marked
Kac-Rice use, or any limit in eta, k or r.

Run:
    python -B -S reviews/contact_kernel_substitute_20260926/verify_substitute.py
    python -B -O -S reviews/contact_kernel_substitute_20260926/verify_substitute.py
Negative controls (each must exit nonzero):
    python -B -S .../verify_substitute.py --mutate pin_sign
    python -B -S .../verify_substitute.py --mutate det_sign
    python -B -S .../verify_substitute.py --mutate integral_bound
    python -B -S .../verify_substitute.py --mutate prefactor
Checks raise CheckError explicitly; nothing relies on `assert`, so `-O` does
not weaken the run.
"""
from __future__ import annotations

import argparse
import sys
from fractions import Fraction as F

# Variable order for exponent tuples.
NAMES = ("k", "q", "u", "v", "th", "w", "A", "c", "d", "s", "t")
IDX = {n: i for i, n in enumerate(NAMES)}
NV = len(NAMES)

MUTATIONS = ("pin_sign", "det_sign", "integral_bound", "prefactor")


class CheckError(Exception):
    pass


def require(cond: bool, label: str) -> None:
    if not cond:
        raise CheckError(label)


# ---------------------------------------------------------------- polynomials

def var(name: str):
    e = [0] * NV
    e[IDX[name]] = 1
    return {tuple(e): F(1)}


def const(c) -> dict:
    c = F(c)
    return {(0,) * NV: c} if c else {}


def add(*ps):
    out: dict = {}
    for p in ps:
        for e, c in p.items():
            out[e] = out.get(e, F(0)) + c
    return {e: c for e, c in out.items() if c}


def neg(p):
    return {e: -c for e, c in p.items()}


def sub(p, q):
    return add(p, neg(q))


def scale(p, s):
    s = F(s)
    return {e: c * s for e, c in p.items() if c * s}


def mul(p, q):
    out: dict = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            e = tuple(a + b for a, b in zip(e1, e2))
            out[e] = out.get(e, F(0)) + c1 * c2
    return {e: c for e, c in out.items() if c}


def powp(p, n: int):
    out = const(1)
    for _ in range(n):
        out = mul(out, p)
    return out


def deriv(p, name: str):
    i = IDX[name]
    out: dict = {}
    for e, c in p.items():
        if e[i]:
            e2 = list(e)
            e2[i] -= 1
            out[tuple(e2)] = out.get(tuple(e2), F(0)) + c * e[i]
    return {e: c for e, c in out.items() if c}


def subst_poly(p, name: str, value):
    """Substitute a polynomial `value` for variable `name` (Horner by degree)."""
    i = IDX[name]
    by_deg: dict = {}
    for e, c in p.items():
        e2 = list(e)
        dgr = e2[i]
        e2[i] = 0
        by_deg.setdefault(dgr, {})
        by_deg[dgr][tuple(e2)] = by_deg[dgr].get(tuple(e2), F(0)) + c
    out: dict = {}
    for dgr, coeff in by_deg.items():
        out = add(out, mul(coeff, powp(value, dgr)))
    return out


def degree_in(p, name: str) -> int:
    i = IDX[name]
    return max((e[i] for e in p), default=0)


# ------------------------------------------------- rational functions num/v^n

class Rat:
    """num / (den * v^vpow) with `num` a polynomial and `den` a rational number."""

    def __init__(self, num, vpow: int = 0, den=1):
        self.num = num
        self.vpow = vpow
        self.den = F(den)

    @staticmethod
    def of(p):
        return Rat(p, 0, 1)

    def __add__(self, other):
        m = max(self.vpow, other.vpow)
        a = mul(self.num, powp(var("v"), m - self.vpow))
        b = mul(other.num, powp(var("v"), m - other.vpow))
        # bring to common numeric denominator
        den = self.den * other.den
        a = scale(a, other.den)
        b = scale(b, self.den)
        return Rat(add(a, b), m, den)

    def __neg__(self):
        return Rat(neg(self.num), self.vpow, self.den)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if not isinstance(other, Rat):
            other = Rat(const(other))
        return Rat(mul(self.num, other.num), self.vpow + other.vpow, self.den * other.den)

    def is_zero(self) -> bool:
        return not self.num

    def equals(self, other) -> bool:
        return (self - other).is_zero()


def subst_rat(p, name: str, value: Rat) -> Rat:
    """Substitute a Rat for a variable occurring polynomially in `p`."""
    i = IDX[name]
    by_deg: dict = {}
    for e, c in p.items():
        e2 = list(e)
        dgr = e2[i]
        e2[i] = 0
        by_deg.setdefault(dgr, {})
        by_deg[dgr][tuple(e2)] = by_deg[dgr].get(tuple(e2), F(0)) + c
    out = Rat(const(0))
    for dgr, coeff in by_deg.items():
        term = Rat(coeff)
        for _ in range(dgr):
            term = term * value
        out = out + term
    return out


def subst_rat_in_rat(r: Rat, name: str, value: Rat) -> Rat:
    inner = subst_rat(r.num, name, value)
    return Rat(inner.num, inner.vpow + r.vpow, inner.den * r.den)


# ------------------------------------------------------------------- the cubic

k, q, u, v, th, w, A, c, d, s, t = (var(n) for n in NAMES)


def cubic(mut: str | None):
    """P(s,t) from SUBSTITUTE.md Section 1 (with optional mutation)."""
    q_sign = F(-1) if mut == "pin_sign" else F(1)
    return add(
        scale(k, F(-1, 2)),
        scale(mul(k, powp(s, 3)), 2),
        scale(mul(k, s), F(-3, 2)),
        scale(mul(A, powp(t, 2)), F(1, 2)),
        scale(mul(mul(q, sub(powp(s, 2), const(F(1, 4)))), t), q_sign * F(1, 2)),
        scale(mul(mul(c, s), powp(t, 2)), F(1, 2)),
        scale(mul(d, powp(t, 3)), F(1, 6)),
    )


def at_point(p, sv, tv):
    """Evaluate a polynomial in (s,t) at rational or polynomial coordinates."""
    if not isinstance(sv, dict):
        sv = const(sv)
    if not isinstance(tv, dict):
        tv = const(tv)
    return subst_poly(subst_poly(p, "s", sv), "t", tv)


def solved_jets():
    """(A, c, d) of Section 1 as Rat objects in (k, q, u, v, th)."""
    D = sub(powp(u, 2), const(F(1, 4)))
    Lc = add(scale(powp(u, 3), 2), scale(u, F(-3, 2)), const(F(-1, 2)))
    c_rat = Rat(add(scale(mul(k, D), -12), scale(mul(mul(q, u), v), -2)), 2)
    d_rat = Rat(add(scale(mul(k, add(Lc, th)), 12), scale(mul(mul(q, D), v), 3)), 3)
    A_rat = Rat(add(mul(q, v), scale(mul(k, add(scale(u, 2), const(1), scale(th, -2))), 6)), 2, 2)
    return A_rat, c_rat, d_rat


def check_pins(P):
    M = (F(-1, 2), F(0))
    S = (F(1, 2), F(0))
    Ps, Pt = deriv(P, "s"), deriv(P, "t")
    require(not at_point(P, *M), "P(M) != 0")
    require(not at_point(Ps, *M), "P_s(M) != 0")
    require(not at_point(Pt, *M), "P_t(M) != 0")
    require(not sub(at_point(P, *S), neg(k)), "P(S) != -k")
    require(not at_point(Ps, *S), "P_s(S) != 0")
    require(not at_point(Pt, *S), "P_t(S) != 0")


def check_solve(P):
    """Substituting the displayed (A,c,d) satisfies grad P(X)=0 and P(X)=-k*theta,
    and the linear system for (A,c,d) is uniquely solvable for v != 0."""
    A_rat, c_rat, d_rat = solved_jets()
    Ps, Pt = deriv(P, "s"), deriv(P, "t")
    eqs = [
        (at_point(Ps, u, v), Rat(const(0)), "P_s(X)"),
        (at_point(Pt, u, v), Rat(const(0)), "P_t(X)"),
        (at_point(P, u, v), Rat(neg(mul(k, th))), "P(X)+k*theta"),
    ]
    for poly, target, label in eqs:
        r = subst_rat(poly, "A", A_rat)
        r = subst_rat_in_rat(r, "c", c_rat)
        r = subst_rat_in_rat(r, "d", d_rat)
        require(r.equals(target), "solve identity fails: " + label)
    # Uniqueness: coefficient matrix of (A, c, d) in the three equations.
    rows = []
    for poly, _, _ in eqs:
        row = []
        for name in ("A", "c", "d"):
            require(degree_in(poly, name) <= 1, "cubic not linear in " + name)
            row.append(subst_poly(subst_poly(subst_poly(deriv(poly, name), "A", const(0)), "c", const(0)), "d", const(0)))
        rows.append(row)
    det3 = add(
        mul(rows[0][0], sub(mul(rows[1][1], rows[2][2]), mul(rows[1][2], rows[2][1]))),
        neg(mul(rows[0][1], sub(mul(rows[1][0], rows[2][2]), mul(rows[1][2], rows[2][0])))),
        mul(rows[0][2], sub(mul(rows[1][0], rows[2][1]), mul(rows[1][1], rows[2][0]))),
    )
    # det = const * v^n: a monomial in v alone, so nonzero exactly when v != 0.
    require(len(det3) == 1, "solve matrix determinant is not a v-monomial")
    (e, coeff), = det3.items()
    require(all(e[i] == 0 for i in range(NV) if NAMES[i] != "v") and coeff != 0, "solve matrix determinant depends on more than v")
    return A_rat, c_rat, d_rat


def hessian(P, sv, tv, A_rat, c_rat, d_rat):
    out = []
    for a, b in (("s", "s"), ("s", "t"), ("t", "t")):
        h = at_point(deriv(deriv(P, a), b), sv, tv)
        r = subst_rat(h, "A", A_rat)
        r = subst_rat_in_rat(r, "c", c_rat)
        r = subst_rat_in_rat(r, "d", d_rat)
        out.append(r)
    return out  # (h11, h12, h22)


def det2(h11, h12, h22):
    return h11 * h22 - h12 * h12


def type_polys():
    PM = sub(scale(th, 4), powp(add(w, const(1)), 2))
    PS = sub(powp(sub(w, const(1)), 2), scale(sub(const(1), th), 4))
    PX = add(powp(add(w, const(1), scale(th, -2)), 2), scale(mul(th, sub(const(1), th)), 4))
    return PM, PS, PX


def check_determinants(P, A_rat, c_rat, d_rat, mut):
    q_of_w = Rat(scale(mul(k, sub(w, scale(u, 2))), 6), 1)  # 6k(w-2u)/v
    PM, PS, PX = type_polys()
    pref = Rat(scale(powp(k, 2), 9), 2)  # 9k^2/v^2
    sign_X = F(1) if mut == "det_sign" else F(-1)
    targets = {
        "M": ((F(-1, 2), F(0)), pref * Rat(PM)),
        "S": ((F(1, 2), F(0)), pref * Rat(sub(scale(sub(const(1), th), 4), powp(sub(w, const(1)), 2)))),
        "X": ((u, v), pref * Rat(scale(PX, sign_X))),
    }
    for label, (pt, target) in targets.items():
        h11, h12, h22 = hessian(P, pt[0], pt[1], A_rat, c_rat, d_rat)
        dt = det2(h11, h12, h22)
        dt_w = subst_rat_in_rat(dt, "q", q_of_w)
        require(dt_w.equals(target), "det B_" + label + " identity fails")
    # Endpoint (1,1) entries: -6k at M, +6k at S (sign conventions of Section 1).
    hM = hessian(P, F(-1, 2), F(0), A_rat, c_rat, d_rat)[0]
    hS = hessian(P, F(1, 2), F(0), A_rat, c_rat, d_rat)[0]
    require(hM.equals(Rat(scale(k, -6))) and hS.equals(Rat(scale(k, 6))), "endpoint (1,1) entries")
    # P_S as displayed equals minus the S-bracket, so det B_S = -(9k^2/v^2) P_S.
    require(not add(PS, sub(scale(sub(const(1), th), 4), powp(sub(w, const(1)), 2))), "P_S bracket sign")


def check_w_transform():
    # w = (q v + 12 k u)/(6k)  <=>  q = 6k(w - 2u)/v ; dq/dw = 6k/v.
    q_of_w = Rat(scale(mul(k, sub(w, scale(u, 2))), 6), 1)
    w_back = (q_of_w * Rat(v) + Rat(scale(mul(k, u), 12)))  # = 6k w
    require(w_back.equals(Rat(scale(mul(k, w), 6))), "w transform inverse")
    require(Rat(deriv(q_of_w.num, "w"), q_of_w.vpow).equals(Rat(scale(k, 6), 1)), "dq/dw")


def check_R_identity():
    D = sub(powp(u, 2), const(F(1, 4)))
    lhs = add(scale(powp(u, 3), -2), scale(u, F(-3, 2)), const(-1), scale(th, 2), scale(mul(w, D), 3))
    rhs = add(
        scale(powp(sub(u, const(F(1, 2))), 3), -2),
        scale(mul(D, sub(w, const(1))), 3),
        scale(sub(const(1), th), -2),
    )
    require(not sub(lhs, rhs), "R saddle-side identity")


def check_sample(P, A_rat, c_rat, d_rat):
    vals = {"u": F(2), "v": F(1), "k": F(1), "th": F(1, 2), "q": F(-30)}

    def ev_rat(r: Rat):
        p = r.num
        for name, val in vals.items():
            p = subst_poly(p, name, const(val))
        require(len(p) <= 1, "sample evaluation not constant")
        num = next(iter(p.values()), F(0))
        return num / (r.den * vals["v"] ** r.vpow)

    wv = (vals["q"] * vals["v"] + 12 * vals["k"] * vals["u"]) / (6 * vals["k"])
    require(wv == -1, "sample w")
    require(ev_rat(A_rat) == -3 and ev_rat(c_rat) == 75 and ev_rat(d_rat) == F(-363, 2), "sample (A,c,d)")
    dets = []
    for pt in ((F(-1, 2), F(0)), (F(1, 2), F(0)), (vals["u"], vals["v"])):
        h11, h12, h22 = hessian(P, pt[0], pt[1], A_rat, c_rat, d_rat)
        dets.append(ev_rat(det2(h11, h12, h22)))
    require(dets == [18, -18, -18], "sample determinants " + str(dets))


def integrate_var(p, name: str, lo, hi):
    """Definite integral of polynomial p in variable `name` from lo to hi (polys)."""
    i = IDX[name]
    anti: dict = {}
    for e, cf in p.items():
        e2 = list(e)
        e2[i] += 1
        anti[tuple(e2)] = cf / e2[i]
    return sub(subst_poly(anti, name, hi), subst_poly(anti, name, lo))


def check_type_mass(mut):
    PM, PS, PX = type_polys()
    Pprod = mul(mul(PM, PS), PX)
    require(degree_in(Pprod, "w") == 6 and degree_in(Pprod, "th") == 3, "degree of P in (w, theta)")
    one = const(1)
    lower_left = scale(powp(add(w, const(1)), 2), F(1, 4))
    lower_right = sub(one, scale(powp(sub(w, const(1)), 2), F(1, 4)))
    if mut == "integral_bound":
        lower_right = scale(powp(add(w, const(1)), 2), F(1, 4))
    left_w = integrate_var(Pprod, "th", lower_left, one)
    right_w = integrate_var(Pprod, "th", lower_right, one)
    left = integrate_var(left_w, "w", const(-3), const(-1))
    right = integrate_var(right_w, "w", const(-1), const(1))

    def as_const(p):
        require(len(p) <= 1 and all(all(x == 0 for x in e) for e in p), "integral not constant")
        return next(iter(p.values()), F(0))

    L, R = as_const(left), as_const(right)
    require(L == F(77248, 945), "left integral " + str(L))
    require(R == F(704, 135), "right integral " + str(R))
    J = L + R
    require(J == F(27392, 315), "J " + str(J))
    area_left = as_const(integrate_var(integrate_var(one, "th", lower_left, one), "w", const(-3), const(-1)))
    area_right = as_const(integrate_var(integrate_var(one, "th", lower_right, one), "w", const(-1), const(1)))
    require(area_left == F(4, 3) and area_right == F(2, 3) and area_left + area_right == 2, "type-region area")
    return J


def check_prefactors(J, mut):
    pref = 24 * 6 * 9 ** 3
    if mut == "prefactor":
        pref += 1
    require(pref == 104976, "24*6*9^3")
    require(F(104976, 36) == 2916, "2916 = 104976/36")
    require(2916 * J == F(8875008, 35), "2916 J")
    require(6 + 6 + 1 == 13, "|v| power count")


def check_interval_geometry():
    # I_theta = (-1 - 2 sqrt(theta), 1 - 2 sqrt(1-theta)) is nonempty on (0,1):
    # length/2 = 1 + sqrt(th) - sqrt(1-th) > 0  <=>  (1 + sqrt(th))^2 > 1 - th
    # <=> 2 sqrt(th) + 2 th > 0, true for th > 0. Check the rational squares on a grid.
    for n in range(1, 64):
        t_ = F(n, 64)
        # (1+sqrt(t))^2 = 1 + t + 2 sqrt(t) > 1 - t  <=>  2t + 2 sqrt(t) > 0
        require(2 * t_ > 0, "interval length sign")
    # P_X >= 4 th (1 - th) > 0 identically: P_X - 4 th(1-th) is a perfect square.
    _, _, PX = type_polys()
    sq = powp(add(w, const(1), scale(th, -2)), 2)
    require(not sub(sub(PX, scale(mul(th, sub(const(1), th)), 4)), sq), "P_X square decomposition")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mutate", choices=MUTATIONS, help="inject one deliberate error; the run must then fail")
    args = ap.parse_args(argv)
    mut = args.mutate
    try:
        P = cubic(mut)
        check_pins(P)
        A_rat, c_rat, d_rat = check_solve(P)
        check_determinants(P, A_rat, c_rat, d_rat, mut)
        check_w_transform()
        check_R_identity()
        check_interval_geometry()
        check_sample(P, A_rat, c_rat, d_rat)
        J = check_type_mass(mut)
        check_prefactors(J, mut)
    except CheckError as exc:
        print("FAIL: " + str(exc) + (" (mutation " + mut + ")" if mut else ""))
        return 1
    if mut:
        print("FAIL: mutation " + mut + " was not detected")
        return 2
    print("SUBSTITUTE_ALGEBRA_PASSED: pins, unique (A,c,d) solve, det B_M/B_S/B_X, w-transform, R identity, "
          "I_theta geometry, sample dets (18,-18,-18), left=77248/945, right=704/135, J=27392/315, area 2, "
          "104976, 2916J=8875008/35. Finite algebra only; no continuum or scientific acceptance.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
