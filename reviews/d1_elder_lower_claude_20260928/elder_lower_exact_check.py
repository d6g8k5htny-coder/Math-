"""Independent exact checks for the nonauthor review of Math-#116's direct elder lower bound
(ELDER_LOWER_AND_DENSITY_GAP.md) and local multiplicity module (LOCAL_MULTIPLICITY.md).

Python standard library only; exact rational / Laurent-polynomial arithmetic. Written without the
author's (unpublished) algebra.py. Groups:

  NF   (E7)/(L6)-(L7): a GENERIC degree-six planar field with the six actual pins solved exactly
       satisfies (f(rX,rZ)-b)/r^3 = P_{k,s,a,beta,c} + O(r) with s=f_zz(0)/r, including -aZ/8;
       P itself satisfies all six pins for arbitrary (s,a,beta,c); dropping -aZ/8 breaks them.
  G    G_k: pins, the four critical points, heights, Hessians, determinants, |P_pm|^2 = 39/16.
  PATH the three segment polynomials (E6), their monotonicity, min -7k/32, end +17k/64, the k/64
       margins, and containment in B(0,3).
  LED  weight 45k^4 and floor 45/4, box volume 16 eps^4 k^4 r, tilt ledger r*r^4/r^2 = r^3,
       radial Jacobian r dr = (1/3) l^(-1/3) k^(-2/3) dl and the loss exponent l^(2/3) k^(-5/3).
  TV   the exact Bernoulli-comparison total variation h on random exact laws, and the counting
       inequalities 1{N>=2} <= N/2, N(N-1) >= 2*1{N>=2}.

Not a continuum or Gaussian proof: the jet-box density floor, conditional C^4 control and the
normalizer bound are argued in REVIEW.md.
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


def at(p, X1, X2):
    return p.subs("x", X1).subs("z", X2)


def hermite(gm, gp, dgm, dgp, a, ainv):
    s0 = (gm + gp) * F(1, 2)
    d0 = (gp - gm) * ainv * F(1, 2)
    s1 = (dgm + dgp) * F(1, 2)
    d1 = (dgp - dgm) * ainv * F(1, 2)
    return s0 - a * a * d1 * F(1, 2), (3 * d0 - s1) * F(1, 2), d1, 3 * (s1 - d0) * ainv * ainv


def pinned_generic(deg=6):
    x, z = P.v("x"), P.v("z")
    f = P()
    for i in range(deg + 1):
        for j in range(deg + 1 - i):
            f = f + P.v("c%d%d" % (i, j)) * x ** i * z ** j
    R, RI = P.v("r"), P.v("r", -1)
    a, ai = R * F(1, 2), 2 * RI
    b, k = P.v("b"), P.v("k")
    h = sum((P.v("c%d0" % i) * x ** i for i in range(4, deg + 1)), P())
    q = sum((P.v("c%d1" % i) * x ** i for i in range(2, deg)), P())
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


def Ppoly(X, Z, k, s, a, beta, c, mut):
    lin = F(0) if mut == "drop-aZ-over-8" else F(1)
    return (2 * k * X ** 3 - F(3, 2) * k * X - k * F(1, 2) + s * F(1, 2) * Z * Z
            + a * F(1, 2) * (X * X - lin * F(1, 4)) * Z + beta * F(1, 2) * X * Z * Z + c * F(1, 6) * Z ** 3)


def check_nf(mut):
    out = {}
    R = P.v("r")
    f = pinned_generic()
    X, Z = P.v("X"), P.v("Z")
    b, k = P.v("b"), P.v("k")
    Fsc = (at(f, R * X, R * Z) - b) * P.v("r", -3)
    s = 2 * P.v("c02") * P.v("r", -1)
    a, beta, c = 2 * P.v("c21"), 2 * P.v("c12"), 6 * P.v("c03")
    Pp = Ppoly(X, Z, k, s, a, beta, c, mut)
    diff = Fsc - Pp
    ex = diff.exponents("r")
    out["F_minus_P_is_O_r_generic_degree6"] = (not ex) or min(ex) >= 1
    # P satisfies all six pins for arbitrary (s,a,beta,c) (scaled pins: F(-1/2,0)=0, F(1/2,0)=-k, grad=0).
    ss, aa, bb, cc = P.v("s"), P.v("a"), P.v("bt"), P.v("cc")
    Pg = Ppoly(X, Z, k, ss, aa, bb, cc, mut)
    ev = lambda p, u, w: p.subs("X", P.c(u)).subs("Z", P.c(w))
    pins = [ev(Pg, F(-1, 2), 0), ev(Pg, F(1, 2), 0) + k,
            ev(Pg.d("X"), F(-1, 2), 0), ev(Pg.d("X"), F(1, 2), 0),
            ev(Pg.d("Z"), F(-1, 2), 0), ev(Pg.d("Z"), F(1, 2), 0)]
    out["P_satisfies_all_six_pins_for_arbitrary_jets"] = all(p.is_zero() for p in pins)
    # Target jets give G_k.
    Gk = k * (2 * X ** 3 - F(3, 2) * X - F(1, 2) - F(3, 4) * Z * Z - X * Z * Z)
    Pt = Ppoly(X, Z, k, -F(3, 2) * k, P.c(0), -2 * k, P.c(0), mut)
    out["target_jets_give_G_k"] = (Pt - Gk).is_zero()
    return out


def check_g(mut):
    out = {}
    k = F(1)
    G = lambda X, Z: k * (2 * X ** 3 - F(3, 2) * X - F(1, 2) - F(3, 4) * Z * Z - X * Z * Z)
    GX = lambda X, Z: k * (6 * X * X - F(3, 2) - Z * Z)
    GZ = lambda X, Z: -k * (F(3, 2) + 2 * X) * Z
    hess = lambda X, Z: (12 * k * X, -2 * k * Z, k * (-F(3, 2) - 2 * X))
    out["pins_heights_0_and_minus_k"] = G(F(-1, 2), 0) == 0 and G(F(1, 2), 0) == -k
    out["pin_gradients_zero"] = all(GX(u, 0) == 0 and GZ(u, 0) == 0 for u in (F(-1, 2), F(1, 2)))
    hm, hs = hess(F(-1, 2), 0), hess(F(1, 2), 0)
    sgn = -1 if mut == "hessian-sign" else 1
    out["M_hessian_diag_-6k_-k_over_2_max"] = hm == (sgn * -6 * k, 0, -k / 2) and hm[0] < 0 and hm[2] < 0
    out["S_hessian_diag_6k_-5k_over_2_saddle"] = hs == (6 * k, 0, -F(5, 2) * k)
    # Extra critical points: X=-3/4, Z^2 = 15/8 (use z2 in place of Z^2; Z only enters via Z^2 or Z*Z).
    z2 = F(15, 8)
    Xp = F(-3, 4)
    out["extra_points_are_critical"] = (6 * Xp * Xp - F(3, 2) - z2 == 0) and (F(3, 2) + 2 * Xp == 0)
    height = 2 * Xp ** 3 - F(3, 2) * Xp - F(1, 2) - (F(3, 4) + Xp) * z2
    out["extra_height_-7_over_32"] = height == F(-7, 32) and -1 < height < 0
    det_extra = (12 * Xp) * (-F(3, 2) - 2 * Xp) - 4 * z2
    out["extra_det_-15_over_2_saddle"] = det_extra == F(-15, 2)
    out["extra_norm_sq_39_over_16_lt_4"] = Xp * Xp + z2 == F(39, 16) and Xp * Xp + z2 < 4
    out["weight_product_45k4"] = abs(hm[0] * hm[2]) * abs(hs[0] * hs[2]) == 45
    out["floor_45_over_4_from_3_over_2_and_15_over_2"] = F(3, 2) * F(15, 2) == F(45, 4)
    return out


def check_path(mut):
    out = {}
    v = P.v("v")
    k = F(1)
    Gp = lambda X, Z: (2 * X ** 3 - F(3, 2) * X - F(1, 2) - F(3, 4) * Z * Z - X * Z * Z) * k
    last = (F(-1), F(2)) if mut == "path-endpoint" else (F(-1), F(9, 4))
    V = [(F(-1, 2), F(0)), (F(-3, 4), F(0)), (F(-3, 4), F(9, 4)), last]
    segs = []
    for (x0, z0), (x1, z1) in zip(V, V[1:]):
        X = x0 + (x1 - x0) * v
        Z = z0 + (z1 - z0) * v
        segs.append(Gp(X, Z))
    want = [-F(3, 16) * v ** 2 - F(1, 32) * v ** 3, P.c(F(-7, 32)),
            F(-7, 32) + F(51, 64) * v - F(9, 32) * v ** 2 - F(1, 32) * v ** 3]
    out["segment_polynomials_E6"] = all((s - w).is_zero() for s, w in zip(segs, want))
    ev = lambda p, t: p.subs("v", P.c(t)).t.get((), F(0))
    g1p, g3p = segs[0].d("v"), segs[2].d("v")
    grid = [F(i, 400) for i in range(401)]
    out["g1_nonincreasing"] = all(ev(g1p, t) <= 0 for t in grid) and ev(segs[0].d("v").d("v"), F(0)) <= 0
    # g3' is a decreasing quadratic on [0,1] (g3'' = -9/16 - 3v/16 < 0), so its minimum is g3'(1).
    out["g3_prime_ge_9_over_64"] = ev(g3p, F(1)) == F(9, 64) and all(ev(g3p.d("v"), t) < 0 for t in grid)
    vals = [ev(s, t) for s in segs for t in grid]
    out["path_min_-7_over_32"] = min(vals) == F(-7, 32)
    out["path_end_17_over_64"] = ev(segs[2], F(1)) == F(17, 64)
    out["margin_path_above_minus_quarter"] = F(-7, 32) - F(1, 64) == F(-15, 64) and F(-15, 64) > F(-1, 4)
    out["margin_end_above_quarter"] = F(17, 64) - F(1, 64) == F(1, 4)
    out["path_in_B3"] = max(x * x + z * z for x, z in V) == F(97, 16) and F(97, 16) < 9
    return out


def check_led(mut):
    out = {}
    eps, k, r = P.v("eps"), P.v("k"), P.v("r")
    vol = (2 * eps * k * r) * (2 * eps * k) ** 3
    out["box_volume_16_eps4_k4_r"] = (vol - 16 * eps ** 4 * k ** 4 * r).is_zero()
    wpow = 3 if mut == "weight-power" else 4
    out["tilt_ledger_r_times_r4_over_r2_is_r3"] = 1 + wpow - 2 == 3
    # Radial Jacobian with k = t^3 and r = q (so l = k r^3 = t^3 q^3, l^(1/3) = t q):
    # r dr = q dq, dl = 3 t^3 q^2 dq  => r dr / dl = 1/(3 t^3 q);  (1/3) l^(-1/3) k^(-2/3) = 1/(3 t q t^2).
    t, q = P.v("t"), P.v("q")
    lhs = q * P.v("t", -3) * P.v("q", -2) * F(1, 3)  # r dr / dl = q / (3 t^3 q^2)
    rhs = F(1, 3) * P.v("t", -1) * P.v("q", -1) * P.v("t", -2)
    out["radial_jacobian_r_dr"] = (lhs - rhs).is_zero()
    # Loss: l^(-1/3) k^(-2/3) * (1-p ~ r^3 = l/k): exponents of (l, k) = (-1/3 + 1, -2/3 - 1).
    le, ke = F(-1, 3) + 1, F(-2, 3) - 1
    out["loss_exponent_l_2_3_k_minus_5_3"] = (le, ke) == (F(2, 3), F(-5, 3))
    return out


def check_tv(mut):
    rng = random.Random(116)
    ok_tv, ok_cnt = True, True
    nontrivial = 0
    for _ in range(2000):
        # A random law of the count N in {0..6} with mean m <= 1 (heavy mass at N = 0).
        pN = [F(rng.randrange(300, 1000))] + [F(rng.randrange(0, 30)) for _ in range(6)]
        tot = sum(pN)
        pN = [x / tot for x in pN]
        m = sum(n * pN[n] for n in range(7))
        if m > 1:
            continue
        s1 = pN[1]
        h = sum(n * pN[n] for n in range(2, 7))
        alpha = sum(pN[n] for n in range(2, 7))
        # Law minus Bernoulli(mean): empty (1-m) vs P(N=0); singleton mean mass s1+h vs s1; multiples alpha.
        diff_empty = pN[0] - (1 - m)
        diff_single = s1 - (s1 + h)
        diff_mult = alpha
        tv = (abs(diff_empty) + abs(diff_single) + abs(diff_mult)) / 2
        target = h if mut != "tv-half" else h / 2
        ok_tv &= tv == target and h >= 2 * alpha
        nontrivial += h > 0
    for N in range(40):
        ok_cnt &= F(int(N >= 2)) <= F(N, 2) and N * (N - 1) >= 2 * int(N >= 2)
    return {"bernoulli_tv_equals_h_random_exact": ok_tv and nontrivial >= 1000,
            "counting_inequalities": ok_cnt}


MUTANTS = ("drop-aZ-over-8", "hessian-sign", "path-endpoint", "weight-power", "tv-half")


def flatten(d):
    for v in d.values():
        if isinstance(v, dict):
            yield from flatten(v)
        else:
            yield v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    mut = ap.parse_args().mutant
    groups = {
        "NF_pinned_normal_form": check_nf(mut),
        "G_cubic_critical_data": check_g(mut),
        "PATH_elder_obstruction": check_path(mut),
        "LED_ledgers": check_led(mut),
        "TV_multiplicity": check_tv(mut),
    }
    passed = all(flatten(groups))
    res = {"checks": groups, "passed": passed, "scientific_effect": "NONE",
           "scope": "exact identities only; Gaussian jet-box, conditional C^4 and normalizer steps are argued in REVIEW.md"}
    sys.stdout.write(json.dumps(res, indent=2, sort_keys=True) + "\n")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
