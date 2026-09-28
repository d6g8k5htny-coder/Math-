"""Exact symbolic checks for the nonauthor review of OA-PIN-MICRO-COV-20260926-v1.

Python standard library only. A minimal sparse multivariate Laurent-polynomial
class over Fractions verifies, as exact polynomial identities in (r, P, Q) and
the free jets:

  1. the degree-four pin solution for f_xx, f_xxx, f_xz satisfies all six pins;
  2. the coefficients of (S0, T, R4) in G_r are exactly the matrix B_r;
  3. the three 2x2 minors of B_r;
  4. every random-jet column of G_r (all nine free jets through degree four)
     is a polynomial in (r, s=rP, Q) with no negative power of r and no
     constant term, so it is O(|Q| + r|P|) = O(h) on bounded (r, s, Q);
     each monomial r^a s^b Q^c also has a >= c-1, so the O(h) bound holds
     uniformly on the whole pin chart |rP|, |rQ| <= 1/4;
  5. the deterministic mean is exactly 6kP(rP-1) in G_r1 and 0 in G_r2;
  6. the rational constants in the Cauchy-Binet and trace bounds.

Not a continuum proof: the Gaussian Schur-complement floor, the Taylor
remainder and the density bound are argued in REVIEW.md, not checked here.
"""
import argparse
import json
import sys
from fractions import Fraction as F

VARS = ("r", "P", "Q", "s", "k", "S0", "T", "R4", "C", "D", "E1", "E2", "E3", "F4")
IDX = {v: i for i, v in enumerate(VARS)}
RANDOM_JETS = ("S0", "T", "R4", "C", "D", "E1", "E2", "E3", "F4")


class Poly:
    __slots__ = ("t",)

    def __init__(self, terms=None):
        self.t = {m: c for m, c in (terms or {}).items() if c != 0}

    @staticmethod
    def const(c):
        return Poly({(0,) * len(VARS): F(c)})

    @staticmethod
    def var(name, power=1):
        m = [0] * len(VARS)
        m[IDX[name]] = power
        return Poly({tuple(m): F(1)})

    def __add__(self, o):
        o = o if isinstance(o, Poly) else Poly.const(o)
        t = dict(self.t)
        for m, c in o.t.items():
            t[m] = t.get(m, 0) + c
        return Poly(t)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.t.items()})

    def __sub__(self, o):
        return self + (-(o if isinstance(o, Poly) else Poly.const(o)))

    def __rsub__(self, o):
        return Poly.const(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, Poly) else Poly.const(o)
        t = {}
        for m1, c1 in self.t.items():
            for m2, c2 in o.t.items():
                m = tuple(a + b for a, b in zip(m1, m2))
                t[m] = t.get(m, 0) + c1 * c2
        return Poly(t)

    __rmul__ = __mul__

    def __pow__(self, n):
        out = Poly.const(1)
        for _ in range(n):
            out = out * self
        return out

    def is_zero(self):
        return not self.t

    def coeff(self, name):
        """Coefficient of a variable that occurs at most linearly."""
        i = IDX[name]
        t = {}
        for m, c in self.t.items():
            if m[i] > 1:
                raise ValueError(f"{name} occurs nonlinearly")
            if m[i] == 1:
                mm = list(m)
                mm[i] = 0
                t[tuple(mm)] = c
        return Poly(t)

    def without(self, names):
        idx = [IDX[n] for n in names]
        return Poly({m: c for m, c in self.t.items() if all(m[i] == 0 for i in idx)})

    def subs_P_by_s_over_r(self):
        t = {}
        for m, c in self.t.items():
            mm = list(m)
            p = mm[IDX["P"]]
            mm[IDX["P"]] = 0
            mm[IDX["s"]] += p
            mm[IDX["r"]] -= p
            key = tuple(mm)
            t[key] = t.get(key, 0) + c
        return Poly(t)


def V(name, power=1):
    return Poly.var(name, power)


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def build(mutant=None):
    r, P, Q, k = V("r"), V("P"), V("Q"), V("k")
    S0, T, R4, C, D = V("S0"), V("T"), V("R4"), V("C"), V("D")
    E1, E2, E3, F4 = V("E1"), V("E2"), V("E3"), V("F4")
    # Degree-four pin solution claimed in Section 2 of the author note.
    fxx = -6 * k * r + F(1, 12) * r ** 2 * R4
    fxxx = 12 * k - F(1, 2) * r * R4
    fxz = -F(1, 2) * r * T - F(1, 6) * r ** 2 * E1
    if mutant == "pin-sign":
        fxxx = 12 * k + F(1, 2) * r * R4

    def grad(x, z):
        fx = (fxx * x + fxz * z
              + F(1, 2) * (fxxx * x ** 2 + 2 * T * x * z + C * z ** 2)
              + F(1, 6) * (R4 * x ** 3 + 3 * E1 * x ** 2 * z + 3 * E2 * x * z ** 2 + E3 * z ** 3))
        fz = (fxz * x + S0 * z
              + F(1, 2) * (T * x ** 2 + 2 * C * x * z + D * z ** 2)
              + F(1, 6) * (E1 * x ** 3 + 3 * E2 * x ** 2 * z + 3 * E3 * x * z ** 2 + F4 * z ** 3))
        return fx, fz

    def height(x, z):  # f - f(M), degree-four Taylor polynomial
        return (F(1, 2) * (fxx * x ** 2 + 2 * fxz * x * z + S0 * z ** 2)
                + F(1, 6) * (fxxx * x ** 3 + 3 * T * x ** 2 * z + 3 * C * x * z ** 2 + D * z ** 3)
                + F(1, 24) * (R4 * x ** 4 + 4 * E1 * x ** 3 * z + 6 * E2 * x ** 2 * z ** 2
                              + 4 * E3 * x * z ** 3 + F4 * z ** 4))

    zero = Poly()
    fxS, fzS = grad(r, zero)
    pins = {"f_x(S)=0": fxS, "f_z(S)=0": fzS, "f(S)-f(M)=-k r^3": height(r, zero) + k * r ** 3}
    fx, fz = grad(r ** 2 * P, r ** 2 * Q)
    rinv3 = Poly({tuple(-3 if v == "r" else 0 for v in VARS): F(1)})
    rinv2 = Poly({tuple(-2 if v == "r" else 0 for v in VARS): F(1)})
    G1, G2 = fx * rinv3, fz * rinv2
    return pins, G1, G2


def check(mutant=None):
    r, P, Q = V("r"), V("P"), V("Q")
    pins, G1, G2 = build(mutant)
    for name, expr in pins.items():
        require(expr.is_zero(), f"pin equation fails: {name}")

    B = [[Poly(), Q * (r * P - F(1, 2)), F(1, 12) * r * P * (2 * r * P - 1) * (r * P - 1)],
         [Q, F(1, 2) * r * P * (r * P - 1), Poly()]]
    if mutant == "B-entry":
        B[1][1] = F(1, 2) * r * P * (r * P + 1)
    cols = ("S0", "T", "R4")
    for i, G in enumerate((G1, G2)):
        for j, name in enumerate(cols):
            require((G.coeff(name) - B[i][j]).is_zero(), f"B_r[{i}][{j}] mismatch")

    m_ST = B[0][0] * B[1][1] - B[0][1] * B[1][0]
    m_SR = B[0][0] * B[1][2] - B[0][2] * B[1][0]
    m_TR = B[0][1] * B[1][2] - B[0][2] * B[1][1]
    require((m_ST - (-F(1, 2) * Q ** 2 * (2 * r * P - 1))).is_zero(), "m_ST")
    require((m_SR - (-F(1, 12) * r * P * Q * (r * P - 1) * (2 * r * P - 1))).is_zero(), "m_SR")
    require((m_TR - (-F(1, 24) * r ** 2 * P ** 2 * (r * P - 1) ** 2 * (2 * r * P - 1))).is_zero(), "m_TR")

    # Every random column is O(h): polynomial in (r, s, Q), no r^-1, no constant term.
    # Whole pin chart |s|=|rP|<=1/4, |rQ|<=1/4 (Q unbounded): each monomial
    # r^a s^b Q^c also needs a >= c-1, so that r^a Q^(c-1) = r^(a-c+1) (rQ)^(c-1)
    # stays bounded and the monomial is O(|s|+|Q|) = O(h) uniformly.
    whole_chart = True
    for G in (G1, G2):
        for name in RANDOM_JETS:
            col = G.coeff(name).subs_P_by_s_over_r()
            if mutant == "column-r-power" and name == "C":
                col = col * Poly({tuple(-1 if v == "r" else 0 for v in VARS): F(1)})
            for m in col.t:
                a, b, c = m[IDX["r"]], m[IDX["s"]], m[IDX["Q"]]
                require(a >= 0, f"column {name} has a negative power of r")
                require(b + c >= 1, f"column {name} is not O(h)")
                require(a >= c - 1, f"column {name} not O(h) on the whole pin chart")

    mean1 = G1.without(RANDOM_JETS)
    mean2 = G2.without(RANDOM_JETS)
    require((mean1 - 6 * V("k") * P * (r * P - 1)).is_zero(), "longitudinal mean")
    require(mean2.is_zero(), "transverse mean")

    # Rational constants for |rP| <= 1/4.
    lo_2rp1, lo_rp1 = F(1, 2), F(3, 4)
    require(lo_2rp1 * lo_rp1 ** 2 / 24 == F(3, 256), "m_TR floor constant")
    c0 = min(F(1, 16), F(3, 256) ** 2) / 2
    require(c0 == F(9, 131072), "Cauchy-Binet floor c0")
    # trace: a^2 <= (3/4)^2 Q^2, Q^2, e^2 <= (1/4)^2(5/4)^2/4... bounded by C0 h^2
    C0 = max(1 + F(3, 4) ** 2, F(3, 2) ** 2 * F(5, 4) ** 2 / 144 + F(5, 4) ** 2 / 4)
    require(C0 == F(25, 16), "trace constant C0")
    smin2 = c0 / C0
    return {
        "B_r_entries_verified": 6,
        "minors_verified": 3,
        "pin_equations_verified": len(pins),
        "random_columns_O_h": 2 * len(RANDOM_JETS),
        "random_columns_O_h_on_whole_pin_chart": whole_chart,
        "longitudinal_mean": "6kP(rP-1) exact in the degree-four model",
        "cauchy_binet_c0": str(c0),
        "trace_C0": str(C0),
        "sigma_min_squared_over_h2_floor": str(smin2),
        "scope": "exact polynomial identities only; Gaussian Schur floor, remainder and density are argued in REVIEW.md",
        "scientific_effect": "NONE",
        "passed": True,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=["pin-sign", "B-entry", "column-r-power"])
    args = ap.parse_args(argv)
    try:
        out = check(args.mutant)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
