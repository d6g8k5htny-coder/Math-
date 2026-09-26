#!/usr/bin/env python3
"""Exact checks for the pin-neighborhood ledger.

Standard library only. These identities do not replace the conditional
Gaussian argument in NOTE.md.
"""

from fractions import Fraction


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
    # fz(S)=0 with fz(M)=0.
    jets["fxz"] = -(r / 2) * t - (r ** 2 / 6) * free["U"]
    return jets


def assert_pins(r, k, jets):
    b = jets["f"]
    assert eval_deriv(jets, 1, 0, 0, 0) == 0
    assert eval_deriv(jets, 0, 1, 0, 0) == 0
    assert eval_deriv(jets, 0, 0, r, 0) == b - k * r ** 3
    assert eval_deriv(jets, 1, 0, r, 0) == 0
    assert eval_deriv(jets, 0, 1, r, 0) == 0


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
        assert got == predicted(r, p, q, k, free)


def check_s_drift():
    # X = S + r (p', 0) on the cubic mean. Drift of f_x / r^2 is 6k p'(p'+1).
    r = Fraction(1, 5)
    k = Fraction(3, 7)
    b = Fraction(2, 1)
    def height(x):
        return b - k * r ** 3 / 2 - Fraction(3, 2) * k * r ** 2 * x + 2 * k * x ** 3
    def slope(x):
        return -Fraction(3, 2) * k * r ** 2 + 6 * k * x ** 2
    assert height(-r / 2) == b
    assert height(r / 2) == b - k * r ** 3
    assert slope(-r / 2) == 0
    assert slope(r / 2) == 0
    for p in (Fraction(-1, 3), Fraction(1, 4), Fraction(2, 1), Fraction(0)):
        x = -r / 2 + r * p
        assert slope(x) / r ** 2 == 6 * k * p * (p - 1)
        y = r / 2 + r * p
        assert slope(y) / r ** 2 == 6 * k * p * (p + 1)


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
            assert got == expect
    # Transverse blow-up: divide by q. Leading (S, T) minor is 1/2.
    # Y1 = (p-1/2) T + (q/2) C, Y2 = S, then p=α q and q->0 gives -T/2.
    minor = Fraction(0) * Fraction(0) - Fraction(-1, 2) * Fraction(1)
    assert minor == Fraction(1, 2)


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
        assert ratio == 5184 * k ** 2 / ((2 * p - 1) ** 2 * var)
        assert ratio >= 2304 * k ** 2 / var


def check_ledger_and_overlap():
    assert -2 - 3 + 5 == 0
    # Cone: physical element r^2 |q| dq times intensity 1/q^2.
    assert 2 + 1 - 2 == 1  # power of |q| in the integrand before 1/|q| from dq/q
    radius = Fraction(3, 2)
    assert radius > 1
    assert radius - Fraction(1, 2) > Fraction(1, 2)
    # |s|<=1/4 lies inside the open disk ρ<1, hence inside every annulus hole ρ<A.
    assert Fraction(1, 2) + Fraction(1, 4) < 1


def main():
    check_expansion()
    check_s_drift()
    check_rank()
    check_axis_ratio()
    check_ledger_and_overlap()
    print("ok")


if __name__ == "__main__":
    main()
