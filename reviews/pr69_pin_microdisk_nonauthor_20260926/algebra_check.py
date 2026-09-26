#!/usr/bin/env python3
"""Independent finite checks for the PR69 pin-microdisk review.

Standard library only. These identities certify the degree-4 symbol,
the q=0 determinant values, and the ledger arithmetic. They are not a
continuum proof of the conditional Gaussian integral.
"""

from fractions import Fraction as Q


def fact(n):
    out = 1
    for i in range(1, n + 1):
        out *= i
    return out


JETS = (
    "f", "fx", "fz", "fxx", "fxz", "fzz", "fxxx", "fxxz", "fxzz", "fzzz",
    "fxxxx", "fxxxz", "fxxzz", "fxzzz", "fzzzz",
)
MULTI = {
    "f": (0, 0),
    "fx": (1, 0), "fz": (0, 1),
    "fxx": (2, 0), "fxz": (1, 1), "fzz": (0, 2),
    "fxxx": (3, 0), "fxxz": (2, 1), "fxzz": (1, 2), "fzzz": (0, 3),
    "fxxxx": (4, 0), "fxxxz": (3, 1), "fxxzz": (2, 2), "fxzzz": (1, 3), "fzzzz": (0, 4),
}


def ev(jets, a, b, x, z):
    total = Q(0)
    for name, (px, pz) in MULTI.items():
        if px < a or pz < b:
            continue
        dx, dz = px - a, pz - b
        if dx + dz + a + b > 4:
            continue
        total += jets[name] * (x ** dx) * (z ** dz) / Q(fact(dx) * fact(dz))
    return total


def pins(r, k, free):
    jets = {name: Q(0) for name in JETS}
    jets["f"] = free.get("b", Q(0))
    jets["fxxxx"] = free.get("Q", Q(0))
    jets["fxxz"] = free.get("T", Q(0))
    jets["fxxxz"] = free.get("U", Q(0))
    jets["fzz"] = free.get("S", Q(0))
    jets["fxzz"] = free.get("C", Q(0))
    jets["fzzz"] = free.get("D", Q(0))
    jets["fxxzz"] = free.get("V", Q(0))
    jets["fxzzz"] = free.get("W", Q(0))
    jets["fzzzz"] = free.get("Z", Q(0))
    jets["fxxx"] = 12 * k - (r * jets["fxxxx"]) / 2
    jets["fxx"] = -6 * k * r + (r ** 2 * jets["fxxxx"]) / 12
    jets["fxz"] = -(r * jets["fxxz"]) / 2 - (r ** 2 * jets["fxxxz"]) / 6
    return jets


def column(r, k, a, b, name):
    zero = pins(r, k, {})
    bumped = pins(r, k, {name: Q(1)})
    x, z = r * r * a, r * r * b
    return (
        ev(bumped, 1, 0, x, z) - ev(zero, 1, 0, x, z),
        ev(bumped, 0, 1, x, z) - ev(zero, 0, 1, x, z),
    )


def minor(u, v):
    return u[0] * v[1] - v[0] * u[1]


def gram(r, a, b):
    cs, ct, cq = column(r, Q(1), a, b, "S"), column(r, Q(1), a, b, "T"), column(r, Q(1), a, b, "Q")
    return minor(cs, ct) ** 2 + minor(cs, cq) ** 2 + minor(ct, cq) ** 2


def closed_gram(r, a, b):
    """Exact degree-4 (S,T,Q) Gram determinant of (f_x, f_z)."""
    x = r * a
    brace = (
        (b ** 4) * (Q(1, 2) - x) ** 2
        + (r ** 2) * (a ** 2) * (b ** 2) * ((1 - x) ** 2) * ((1 - 2 * x) ** 2) / 144
        + (r ** 4) * (a ** 4) * ((1 - x) ** 4) * ((1 - 2 * x) ** 2) / 576
    )
    return (r ** 10) * brace


def leading_phi(r, a, b):
    return b ** 4 / 4 + (r ** 2) * (a ** 2) * (b ** 2) / 144 + (r ** 4) * (a ** 4) / 576


def contact(t, q, c, dz, k):
    denom = 1 - 2 * t * q
    tee = ((c + 12 * k * t * t) * q - 12 * k * t) / denom
    sigma = -tee * t * (t * q - 1) / 2 - t * q * c - q * dz / 2
    p = t * q
    det_m = -6 * k * sigma - tee ** 2 / 4
    xx = -6 * k + 12 * k * p + tee * q
    xz = -tee / 2 + tee * p + c * q
    zz = sigma + c * p + dz * q
    det_x = xx * zz - xz ** 2
    det_s = 6 * k * (sigma + c) - tee ** 2 / 4
    return det_m, det_x, det_s


def quartic_ratio(r, a, b, k):
    mean = -6 * k * a * r ** 3
    var = (r ** 3 * b / 2) ** 2 + (r ** 4 * a / 12) ** 2
    return (mean ** 2) / var


def check_gram_factor():
    samples = []
    for r in (Q(0), Q(1, 20), Q(1, 7), Q(2, 9)):
        for a in (Q(-4), Q(-1, 3), Q(0), Q(1), Q(3)):
            for b in (Q(-2), Q(0), Q(1, 5), Q(4)):
                got = gram(r, a, b)
                expect = closed_gram(r, a, b)
                assert got == expect
                samples.append((r, a, b, got))
                if b == 0 and a != 0:
                    x = r * a
                    axis = (r ** 14) * (a ** 4) * ((1 - x) ** 4) * ((1 - 2 * x) ** 2) / 576
                    assert got == axis
    # Leading symbol identity used by the note.
    for r, a, b, _got in samples:
        phi = leading_phi(r, a, b)
        psi = b * b + r * r * a * a
        assert 576 * phi - psi ** 2 == 143 * b ** 4 + 2 * r * r * a * a * b * b
        if b == 0 and a != 0 and r != 0:
            assert phi * 576 == psi ** 2
    # Positive floor on the square once |r alpha| <= 1/4.
    floor = Q(9, 131072)
    for r, a, b, got in samples:
        if abs(r * a) > Q(1, 4):
            continue
        if a == 0 and b == 0:
            continue
        psi = b * b + r * r * a * a
        assert got * 131072 >= (r ** 10) * psi * psi * 9
        assert got >= (r ** 10) * psi * psi * floor


def check_soft_factors():
    for t in (Q(0), Q(1), Q(-3, 2), Q(2, 7)):
        for c in (Q(0), Q(3), Q(-1, 4)):
            for dz in (Q(0), Q(1, 5), Q(9)):
                for k in (Q(1), Q(4, 3)):
                    det_m, det_x, det_s = contact(t, Q(0), c, dz, k)
                    assert det_m == 0 and det_x == 0
                    assert det_s == 6 * k * c - 72 * k * k * t * t
    closed = contact(Q(1), Q(1, 5), Q(1), Q(2), Q(1))
    assert closed == (Q(-769, 36), Q(3031, 180), Q(-3433, 36))


def check_quartic_and_ledgers():
    r = Q(1, 20)
    for n in range(1, 9):
        a = Q(n, 8)
        for m in range(0, n + 1):
            b = r * a * Q(m, n)
            assert quartic_ratio(r, a, b, Q(1)) >= Q(5184, 37) / r ** 2
        assert quartic_ratio(r, a, Q(0), Q(1)) == Q(5184) / r ** 2
    assert quartic_ratio(r, Q(1), r, Q(1)) == Q(5184, 37) / r ** 2
    # Microdisk: Z^{-1} r^{-2}, Jacobian r^{-5}, determinant r^{8}, area r^{4}.
    assert -2 - 5 + 8 + 4 == 5
    # Cone: Z^{-1} r^{-2}, Jacobian r^{-3}, determinant r^{6}, area r^{2}.
    assert -2 - 3 + 6 + 2 == 3
    assert Q(1, 4) + Q(1, 4) < 1
    assert Q(1, 2) + Q(1, 4) == Q(3, 4)
    assert Q(3, 4) < 1


def mutants():
    caught = []
    phi = leading_phi(Q(1, 20), Q(1), Q(0))
    psi = (Q(1, 20) ** 2)
    if phi / psi ** 2 == Q(1, 288):
        raise AssertionError("axis floor mutant agrees")
    caught.append("axis-floor-288")
    if contact(Q(1), Q(0), Q(0), Q(0), Q(1))[2] == -36:
        raise AssertionError("detS mutant agrees")
    caught.append("detS-36")
    if quartic_ratio(Q(1, 20), Q(1), Q(1, 20), Q(1)) >= Q(5184, 36) / Q(1, 20) ** 2:
        raise AssertionError("quartic mutant still holds")
    caught.append("quartic-36")
    if -2 - 3 + 5 + 2 == 3:
        raise AssertionError("cone power mutant still cubic")
    caught.append("cone-power")
    if Q(1, 2) + Q(1, 4) < Q(1, 2):
        raise AssertionError("collar mutant still separates")
    caught.append("collar")
    return caught


def main():
    check_gram_factor()
    check_soft_factors()
    check_quartic_and_ledgers()
    caught = mutants()
    if caught != ["axis-floor-288", "detS-36", "quartic-36", "cone-power", "collar"]:
        raise SystemExit(caught)
    print("ok")
    print("mutants", ",".join(caught))


if __name__ == "__main__":
    main()
