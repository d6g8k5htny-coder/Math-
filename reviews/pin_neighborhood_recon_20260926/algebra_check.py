#!/usr/bin/env python3
"""Exact checks for the pin-neighborhood ledger.

Standard library only. These identities do not replace the conditional
Gaussian argument in NOTE.md. Checks raise CheckError explicitly (not
`assert`), so `python -O` does not weaken them. `--mutate` injects a wrong
pin solve; that run must exit nonzero.
"""

import sys
from fractions import Fraction


class CheckError(Exception):
    pass


def check(cond, label):
    if not cond:
        raise CheckError(label)


MUTATE = False


def fact(n):
    out = 1
    for i in range(1, n + 1):
        out *= i
    return out


# Jets through order 4, centered at the endpoint under inspection.
JETS = (
    "f", "fx", "fz",
    "fxx", "fxz", "fzz",
    "fxxx", "fxxz", "fxzz", "fzzz",
    "fxxxx", "fxxxz", "fxxzz", "fxzzz", "fzzzz",
)
INDEX = {name: i for i, name in enumerate(JETS)}
MULTI = {
    "f": (0, 0),
    "fx": (1, 0), "fz": (0, 1),
    "fxx": (2, 0), "fxz": (1, 1), "fzz": (0, 2),
    "fxxx": (3, 0), "fxxz": (2, 1), "fxzz": (1, 2), "fzzz": (0, 3),
    "fxxxx": (4, 0), "fxxxz": (3, 1), "fxxzz": (2, 2), "fxzzz": (1, 3), "fzzzz": (0, 4),
}


def eval_deriv(jets, a, b, x, z):
    """Partial_x^a partial_z^b of the degree-4 Taylor polynomial at displacement (x, z)."""
    total = Fraction(0)
    for name, value in jets.items():
        px, pz = MULTI[name]
        if px < a or pz < b:
            continue
        dx, dz = px - a, pz - b
        if dx + dz + a + b > 4:
            continue
        total += value * (x ** dx) * (z ** dz) / (fact(dx) * fact(dz))
    return total


def pinned_jets(r, k, free):
    """Six pins at M and S, solved through the degree-4 jet."""
    jets = {name: Fraction(0) for name in JETS}
    jets["f"] = free["b"]
    jets["fx"] = Fraction(0)
    jets["fz"] = Fraction(0)
    q = free["Q"]
    t = free["T"]
    jets["fxxxx"] = q
    jets["fxxz"] = t
    jets["fxxxz"] = free["U"]
    jets["fzz"] = free["S"]
    jets["fxzz"] = free["C"]
    jets["fzzz"] = free["D"]
    jets["fxxzz"] = free["V"]
    jets["fxzzz"] = free["W"]
    jets["fzzzz"] = free["Z"]
    # fx(S)=0 and f(S)=b-k r^3 with fx(M)=0.
    jets["fxxx"] = 12 * k - (r / 2) * q
    jets["fxx"] = -6 * k * r + (r ** 2 / 12) * q
    if MUTATE:
        jets["fxx"] = -6 * k * r - (r ** 2 / 12) * q  # wrong sign: pins at S fail
    # fz(S)=0 with fz(M)=0.
    jets["fxz"] = -(r / 2) * t - (r ** 2 / 6) * free["U"]
    return jets


def assert_pins(r, k, jets):
    b = jets["f"]
    check(eval_deriv(jets, 1, 0, 0, 0) == 0, 'eval_deriv(jets, 1, 0, 0, 0) == 0')
    check(eval_deriv(jets, 0, 1, 0, 0) == 0, 'eval_deriv(jets, 0, 1, 0, 0) == 0')
    check(eval_deriv(jets, 0, 0, r, 0) == b - k * r ** 3, 'eval_deriv(jets, 0, 0, r, 0) == b - k * r ** 3')
    check(eval_deriv(jets, 1, 0, r, 0) == 0, 'eval_deriv(jets, 1, 0, r, 0) == 0')
    check(eval_deriv(jets, 0, 1, r, 0) == 0, 'eval_deriv(jets, 0, 1, r, 0) == 0')


def predicted(r, p, q, k, free):
    t = free["T"]
    c = free["C"]
    s = free["S"]
    quad = free["Q"]
    fx = r ** 2 * (
        6 * k * p * (p - 1)
        + q * (p - Fraction(1, 2)) * t
        + (q ** 2 / 2) * c
    )
    fx += r ** 3 * quad * p * (2 * p - 1) * (p - 1) / 12
    fx += r ** 3 * free["U"] * q * (p ** 2 / 2 - Fraction(1, 6))
    fx += r ** 3 * free["V"] * (p * q ** 2 / 2)
    fx += r ** 3 * free["W"] * (q ** 3 / 6)
    fz = r * q * s
    fz += r ** 2 * (
        t * p * (p - 1) / 2
        + p * q * c
        + (q ** 2 / 2) * free["D"]
    )
    fz += r ** 3 * free["U"] * p * (p ** 2 - 1) / 6
    fz += r ** 3 * free["V"] * (p ** 2 * q / 2)
    fz += r ** 3 * free["W"] * (p * q ** 2 / 2)
    fz += r ** 3 * free["Z"] * (q ** 3 / 6)
    return fx, fz


def check_expansion():
    samples = []
    for r in (Fraction(1, 3), Fraction(2, 5)):
        for p in (Fraction(0), Fraction(1, 4), Fraction(-1, 5), Fraction(1)):
            for q in (Fraction(0), Fraction(1, 7), Fraction(-2, 3)):
                samples.append((r, p, q))
    free = {
        "b": Fraction(3, 2),
        "Q": Fraction(5, 1),
        "T": Fraction(-2, 1),
        "U": Fraction(4, 3),
        "S": Fraction(7, 2),
        "C": Fraction(-3, 5),
        "D": Fraction(1, 6),
        "V": Fraction(8, 1),
        "W": Fraction(-1, 4),
        "Z": Fraction(9, 2),
    }
    k = Fraction(4, 3)
    for r, p, q in samples:
        jets = pinned_jets(r, k, free)
        assert_pins(r, k, jets)
        got = (
            eval_deriv(jets, 1, 0, r * p, r * q),
            eval_deriv(jets, 0, 1, r * p, r * q),
        )
        check(got == predicted(r, p, q, k, free), 'got == predicted(r, p, q, k, free)')


def check_s_drift():
    # X = S + r (p', 0) on the cubic mean. Drift of f_x / r^2 is 6k p'(p'+1).
    r = Fraction(1, 5)
    k = Fraction(3, 7)
    b = Fraction(2, 1)
    def height(x):
        return b - k * r ** 3 / 2 - Fraction(3, 2) * k * r ** 2 * x + 2 * k * x ** 3
    def slope(x):
        return -Fraction(3, 2) * k * r ** 2 + 6 * k * x ** 2
    check(height(-r / 2) == b, 'height(-r / 2) == b')
    check(height(r / 2) == b - k * r ** 3, 'height(r / 2) == b - k * r ** 3')
    check(slope(-r / 2) == 0, 'slope(-r / 2) == 0')
    check(slope(r / 2) == 0, 'slope(r / 2) == 0')
    for p in (Fraction(-1, 3), Fraction(1, 4), Fraction(2, 1), Fraction(0)):
        x = -r / 2 + r * p
        check(slope(x) / r ** 2 == 6 * k * p * (p - 1), 'slope(x) / r ** 2 == 6 * k * p * (p - 1)')
        y = r / 2 + r * p
        check(slope(y) / r ** 2 == 6 * k * p * (p + 1), 'slope(y) / r ** 2 == 6 * k * p * (p + 1)')


def minor_sum(p, q):
    # 2x3 map (S, T, C) -> (q(p-1/2) T + q^2 C/2, q S)
    rows = (
        (Fraction(0), q * (p - Fraction(1, 2)), q ** 2 / 2),
        (q, Fraction(0), Fraction(0)),
    )
    minors = []
    pairs = ((0, 1), (0, 2), (1, 2))
    for i, j in pairs:
        minors.append(rows[0][i] * rows[1][j] - rows[0][j] * rows[1][i])
    return sum(m ** 2 for m in minors)


def check_rank():
    for p in (Fraction(0), Fraction(1, 4), Fraction(-2), Fraction(1, 2)):
        for q in (Fraction(0), Fraction(1, 3), Fraction(-3, 2), Fraction(2)):
            got = minor_sum(p, q)
            expect = q ** 4 * ((p - Fraction(1, 2)) ** 2 + q ** 2 / 4)
            check(got == expect, 'got == expect')
    # Transverse blow-up: divide by q. Leading (S, T) minor is 1/2.
    # Y1 = (p-1/2) T + (q/2) C, Y2 = S, then p=α q and q->0 gives -T/2.
    minor = Fraction(0) * Fraction(0) - Fraction(-1, 2) * Fraction(1)
    check(minor == Fraction(1, 2), 'minor == Fraction(1, 2)')


def check_axis_ratio():
    # (mean ξ)^2 / (r^2 Q-coefficient squared) = 5184 k^2 / ((2p-1)^2 Var).
    # On |p|<=1/4 the minimum is 2304 k^2/Var, at p=-1/4.
    k = Fraction(1)
    var = Fraction(1)
    for n in range(-8, 9):
        p = Fraction(n, 32)  # |p|<=1/4
        if p == 0:
            continue
        mean = 6 * k * p * (p - 1)
        noise = p * (2 * p - 1) * (p - 1) / 12
        ratio = (mean ** 2) / (noise ** 2 * var)
        check(ratio == 5184 * k ** 2 / ((2 * p - 1) ** 2 * var), 'ratio == 5184 * k ** 2 / ((2 * p - 1) ** 2 * var)')
        check(ratio >= 2304 * k ** 2 / var, 'ratio >= 2304 * k ** 2 / var')


def check_ledger_and_overlap():
    # Overlap: |s| <= 1/4 lies inside rho <= 3/4 < 1 < A for every annulus radius A > 1,
    # and the pin-to-annulus distance A - 1/2 exceeds 1/2. Checked on a rational grid of A.
    check(Fraction(1, 2) + Fraction(1, 4) < 1, "disk inside unit circle")
    for n in range(1, 41):
        A = 1 + Fraction(n, 20)
        check(Fraction(3, 4) < A, "disk misses annulus hole A=%s" % A)
        check(A - Fraction(1, 2) > Fraction(1, 2), "collar separation A=%s" % A)


def solve_contact(r, p, q, k, free):
    """Impose f_x(X)=f_z(X)=0 at X=M+r(p,q) on the degree-4 pinned jet and solve
    the two equations, which are linear in (T, S), for those jets."""
    def grad(T, S):
        fr = dict(free)
        fr["T"] = T
        fr["S"] = S
        jets = pinned_jets(r, k, fr)
        return eval_deriv(jets, 1, 0, r * p, r * q), eval_deriv(jets, 0, 1, r * p, r * q), jets
    gx0, gz0, _ = grad(Fraction(0), Fraction(0))
    gxT, gzT, _ = grad(Fraction(1), Fraction(0))
    gxS, gzS, _ = grad(Fraction(0), Fraction(1))
    a, b = gxT - gx0, gxS - gx0
    c, d = gzT - gz0, gzS - gz0
    det = a * d - b * c
    check(det != 0, "contact solve is singular")
    T = (-gx0 * d + gz0 * b) / det
    S = (-a * gz0 + c * gx0) / det
    gx, gz, jets = grad(T, S)
    check(gx == 0 and gz == 0, "contact solve does not annihilate the gradient")
    return T, S, jets


def hessian_det(jets, x, z):
    fxx = eval_deriv(jets, 2, 0, x, z)
    fxz = eval_deriv(jets, 1, 1, x, z)
    fzz = eval_deriv(jets, 0, 2, x, z)
    return fxx * fzz - fxz ** 2


def check_contact_determinants():
    """On the transverse cone p = t q, |q| >= kappa r: after both witness-gradient
    equations, det(H_M)/r^2 and det(H_X)/r^2 are O(|q| + r) and det(H_S)/r^2 = O(1).
    The leading rank-one cancellation -6k(S/r) - T^2/4 -> 36k^2t^2 - 36k^2t^2 = 0 is
    exact in the limit q -> 0, r -> 0."""
    free = {
        "b": Fraction(3, 2), "Q": Fraction(5), "U": Fraction(4, 3), "C": Fraction(-3, 5),
        "D": Fraction(1, 6), "V": Fraction(8), "W": Fraction(-1, 4), "Z": Fraction(9, 2),
        "T": None, "S": None,
    }
    k = Fraction(4, 3)
    t = Fraction(1, 3)
    # Exact limit identity for every k, t.
    for kk in (Fraction(1), Fraction(4, 3), Fraction(7, 2)):
        for tt in (Fraction(1, 3), Fraction(-2, 5), Fraction(1)):
            T_lim = -12 * kk * tt
            S_over_r_lim = -6 * kk * tt ** 2
            check(-6 * kk * S_over_r_lim - T_lim ** 2 / 4 == 0, "leading det(H_M)/r^2 does not cancel")
    bound = 10  # |det(H_M)/r^2| <= bound * (|q| + r) on the sampled jet
    for r in (Fraction(1, 100), Fraction(1, 1000), Fraction(1, 10000)):
        for q in (Fraction(1, 10), Fraction(1, 100), Fraction(1, 1000)):
            p = t * q
            T, S, jets = solve_contact(r, p, q, k, free)
            dM = hessian_det(jets, 0, 0) / r ** 2
            dX = hessian_det(jets, r * p, r * q) / r ** 2
            dS = hessian_det(jets, r, 0) / r ** 2
            check(abs(dM) <= bound * (abs(q) + r), "det(H_M)/r^2 not O(|q|+r) at r=%s q=%s" % (r, q))
            check(abs(dX) <= bound * (abs(q) + r), "det(H_X)/r^2 not O(|q|+r) at r=%s q=%s" % (r, q))
            check(10 <= abs(dS) <= 25, "det(H_S)/r^2 not order one at r=%s q=%s" % (r, q))
            # T and S/r approach their contact limits.
            check(abs(T + 12 * k * t) <= 3 * (abs(q) + r), "T contact limit")
            check(abs(S / r + 6 * k * t ** 2) <= 2 * (abs(q) + r), "S/r contact limit")
    # Every Hessian entry at M and S is O(r) on the cone: check |f_zz(S)| <= c r.
    r, q = Fraction(1, 1000), Fraction(1, 100)
    _, _, jets = solve_contact(r, t * q, q, k, free)
    check(abs(eval_deriv(jets, 0, 2, r, 0)) <= 5 * r, "f_zz(S) not O(r) on the cone")
    check(abs(eval_deriv(jets, 0, 2, 0, 0)) <= 5 * r, "f_zz(M) not O(r) on the cone")


def check_inner_axis_coefficients():
    """Inner disk, axis Q=0: with p = r P the T-coefficient of f_z/r^2 is -T r P/2 + O(r^2)
    and the Q-coefficient of f_x/r^3 is P(2rP-1)(rP-1)/12 * r: both vanish linearly in r P,
    so the normalized gradient has no order-one noise on the axis (NOTE, "Inner disk")."""
    r = Fraction(1, 100)
    k = Fraction(4, 3)
    base = {n: Fraction(0) for n in ("b", "Q", "T", "U", "S", "C", "D", "V", "W", "Z")}
    for P in (Fraction(1, 2), Fraction(1, 10), Fraction(1, 100)):
        p = r * P
        drift_x, drift_z = predicted(r, p, Fraction(0), k, base)
        fr = dict(base)
        fr["T"] = Fraction(1)
        fz_T = (predicted(r, p, Fraction(0), k, fr)[1] - drift_z) / r ** 2
        check(fz_T == p * (p - 1) / 2, "T-coefficient of f_z/r^2 on the axis")
        check(abs(fz_T) <= abs(p), "T-coefficient not O(rP)")
        fr = dict(base)
        fr["Q"] = Fraction(1)
        fx_Q = (predicted(r, p, Fraction(0), k, fr)[0] - drift_x) / r ** 3
        check(fx_Q == p * (2 * p - 1) * (p - 1) / 12, "Q-coefficient of f_x/r^3 on the axis")
        check(abs(fx_Q) <= abs(p), "Q-coefficient not O(rP)")


def main(argv=None):
    global MUTATE
    argv = sys.argv[1:] if argv is None else argv
    MUTATE = "--mutate" in argv
    try:
        check_expansion()
        check_s_drift()
        check_rank()
        check_axis_ratio()
        check_ledger_and_overlap()
        check_contact_determinants()
        check_inner_axis_coefficients()
    except CheckError as exc:
        print("FAIL: " + str(exc) + (" (mutation)" if MUTATE else ""))
        return 1
    if MUTATE:
        print("FAIL: mutation was not detected")
        return 2
    print("ok: pins, drifts, rank minor, axis Q-ratio, overlap, contact determinant cancellation, inner-axis coefficients")
    return 0


if __name__ == "__main__":
    sys.exit(main())
