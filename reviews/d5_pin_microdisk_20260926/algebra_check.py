#!/usr/bin/env python3
"""Exact algebra for the pin microdisk frame and determinant factors.

Standard library only. These identities are finite jet checks. They are not
a continuum proof of the conditional Gaussian integral in NOTE.md.
"""

from fractions import Fraction as Q


def fact(n):
    out = 1
    for i in range(1, n + 1):
        out *= i
    return out


JETS = (
    "f", "fx", "fz",
    "fxx", "fxz", "fzz",
    "fxxx", "fxxz", "fxzz", "fzzz",
    "fxxxx", "fxxxz", "fxxzz", "fxzzz", "fzzzz",
)
MULTI = {
    "f": (0, 0),
    "fx": (1, 0), "fz": (0, 1),
    "fxx": (2, 0), "fxz": (1, 1), "fzz": (0, 2),
    "fxxx": (3, 0), "fxxz": (2, 1), "fxzz": (1, 2), "fzzz": (0, 3),
    "fxxxx": (4, 0), "fxxxz": (3, 1), "fxxzz": (2, 2), "fxzzz": (1, 3), "fzzzz": (0, 4),
}


def eval_deriv(jets, a, b, x, z):
    total = Q(0)
    for name, (px, pz) in MULTI.items():
        if px < a or pz < b:
            continue
        dx, dz = px - a, pz - b
        if dx + dz + a + b > 4:
            continue
        total += jets[name] * (x ** dx) * (z ** dz) / (fact(dx) * fact(dz))
    return total


def pinned_jets(r, k, free):
    jets = {name: Q(0) for name in JETS}
    jets["f"] = free["b"]
    jets["fxxxx"] = free["Q"]
    jets["fxxz"] = free["T"]
    jets["fxxxz"] = free["U"]
    jets["fzz"] = free["S"]
    jets["fxzz"] = free["C"]
    jets["fzzz"] = free["D"]
    jets["fxxzz"] = free["V"]
    jets["fxzzz"] = free["W"]
    jets["fzzzz"] = free["Z"]
    jets["fxxx"] = 12 * k - (r * free["Q"]) / 2
    jets["fxx"] = -6 * k * r + (r ** 2 * free["Q"]) / 12
    jets["fxz"] = -(r * free["T"]) / 2 - (r ** 2 * free["U"]) / 6
    return jets


def blank_free(**overrides):
    free = {
        "b": Q(0), "Q": Q(0), "T": Q(0), "U": Q(0), "S": Q(0),
        "C": Q(0), "D": Q(0), "V": Q(0), "W": Q(0), "Z": Q(0),
    }
    free.update(overrides)
    return free


def predicted_gradient(r, a, b, k, free):
    """Full degree-4 gradient at X=M+r^2(a,b)."""
    t, c, s = free["T"], free["C"], free["S"]
    quad, u, d = free["Q"], free["U"], free["D"]
    v, w, z = free["V"], free["W"], free["Z"]
    fx = (
        r ** 3 * (-6 * k * a - b * t / 2)
        + r ** 4 * (6 * k * a ** 2 + a * b * t + (b ** 2 * c) / 2 + (a * quad) / 12 - (b * u) / 6)
        + r ** 5 * (-(quad * a ** 2) / 4)
        + r ** 6 * ((quad * a ** 3) / 6 + (u * a ** 2 * b) / 2 + (v * a * b ** 2) / 2 + (w * b ** 3) / 6)
    )
    fz = (
        r ** 2 * (b * s)
        + r ** 3 * (-(a * t) / 2)
        + r ** 4 * ((a ** 2 * t) / 2 + a * b * c + (b ** 2 * d) / 2 - (a * u) / 6)
        + r ** 6 * ((u * a ** 3) / 6 + (v * a ** 2 * b) / 2 + (w * a * b ** 2) / 2 + (z * b ** 3) / 6)
    )
    return fx, fz


def gram_pieces(r, a, b):
    phi = b ** 4 / 4 + (r ** 2 * a ** 2 * b ** 2) / 144 + (r ** 4 * a ** 4) / 576
    psi = b ** 2 + r ** 2 * a ** 2
    gap = 576 * phi - psi ** 2
    claimed = 143 * b ** 4 + 2 * r ** 2 * a ** 2 * b ** 2
    return phi, psi, gap, claimed


def contact_scaled(t, q, c, dz, k):
    """det(H/r)=det(H)/r^2 in the Q=U=0 contact chart, p=t*q."""
    denom = 1 - 2 * t * q
    tee_num = (c + 12 * k * t ** 2) * q - 12 * k * t
    tee = tee_num / denom
    sigma = -tee * t * (t * q - 1) / 2 - t * q * c - q * dz / 2
    p = t * q
    ex = 6 * k * p * (p - 1) + q * (p - Q(1, 2)) * tee + (q ** 2 / 2) * c
    ez = q * sigma + tee * p * (p - 1) / 2 + p * q * c + (q ** 2 / 2) * dz
    if ex != 0 or ez != 0:
        raise AssertionError((ex, ez))
    det_m = -6 * k * sigma - tee ** 2 / 4
    xx = -6 * k + 12 * k * p + tee * q
    xz = -tee / 2 + tee * p + c * q
    zz = sigma + c * p + dz * q
    det_x = xx * zz - xz ** 2
    det_s = 6 * k * (sigma + c) - tee ** 2 / 4
    return det_m, det_x, det_s


def quartic_ratio_symbol(r, a, b, k):
    """(mean f_x)^2 / symbol variance on the (T,Q) chart."""
    mean = -6 * k * a * r ** 3
    var = (r ** 3 * b / 2) ** 2 + (r ** 4 * a / 12) ** 2
    return (mean ** 2) / var


def solve_st(r, k, p, q, free):
    base = dict(free)

    def grad(s, t):
        base["S"], base["T"] = s, t
        jets = pinned_jets(r, k, base)
        return (
            eval_deriv(jets, 1, 0, r * p, r * q),
            eval_deriv(jets, 0, 1, r * p, r * q),
        )

    fx00, fz00 = grad(Q(0), Q(0))
    fx01, fz01 = grad(Q(0), Q(1))
    fx10, fz10 = grad(Q(1), Q(0))
    at, bt, bs = fx01 - fx00, fz01 - fz00, fz10 - fz00
    if at == 0 or bs == 0:
        raise ZeroDivisionError("divided-difference rows dropped rank")
    tee = -fx00 / at
    ess = -(bt * tee + fz00) / bs
    fx, fz = grad(ess, tee)
    if fx != 0 or fz != 0:
        raise AssertionError((fx, fz))
    base["S"], base["T"] = ess, tee
    jets = pinned_jets(r, k, base)

    def det_at(x, z):
        xx = eval_deriv(jets, 2, 0, x, z)
        xz = eval_deriv(jets, 1, 1, x, z)
        zz = eval_deriv(jets, 0, 2, x, z)
        return xx * zz - xz * xz

    return ess, tee, det_at(Q(0), Q(0)), det_at(r * p, r * q), det_at(r, Q(0))


def check_rows_and_pins():
    free = blank_free(
        b=Q(1, 3), Q=Q(5), T=Q(-2), U=Q(4, 3), S=Q(7, 2),
        C=Q(-3, 5), D=Q(1, 6), V=Q(8), W=Q(-1, 4), Z=Q(9, 2),
    )
    k = Q(4, 3)
    for r in (Q(1, 5), Q(1, 12)):
        for a in (Q(0), Q(2), Q(-3, 2), Q(1, 7)):
            for b in (Q(0), Q(1), Q(-2, 3), Q(5)):
                jets = pinned_jets(r, k, free)
                assert eval_deriv(jets, 1, 0, 0, 0) == 0
                assert eval_deriv(jets, 0, 1, 0, 0) == 0
                assert eval_deriv(jets, 0, 0, r, 0) == free["b"] - k * r ** 3
                assert eval_deriv(jets, 1, 0, r, 0) == 0
                assert eval_deriv(jets, 0, 1, r, 0) == 0
                got = (
                    eval_deriv(jets, 1, 0, r * r * a, r * r * b),
                    eval_deriv(jets, 0, 1, r * r * a, r * r * b),
                )
                assert got == predicted_gradient(r, a, b, k, free)


def check_row_symbols():
    r, k = Q(1, 9), Q(1)
    a, b = Q(2, 3), Q(-1, 5)
    free = blank_free()
    jets0 = pinned_jets(r, k, free)
    fx0 = eval_deriv(jets0, 1, 0, r * r * a, r * r * b)
    fz0 = eval_deriv(jets0, 0, 1, r * r * a, r * r * b)
    assert fx0 == r ** 3 * (-6 * k * a) + r ** 4 * (6 * k * a * a)
    assert fz0 == 0

    def coef(name):
        bumped = blank_free(**{name: Q(1)})
        jets = pinned_jets(r, k, bumped)
        fx = eval_deriv(jets, 1, 0, r * r * a, r * r * b) - fx0
        fz = eval_deriv(jets, 0, 1, r * r * a, r * r * b) - fz0
        return fx, fz

    sx, sz = coef("S")
    tx, tz = coef("T")
    qx, qz = coef("Q")
    assert sx == 0 and qz == 0
    assert sz == r ** 2 * b
    assert tx == r ** 3 * (-b / 2) + r ** 4 * (a * b)
    assert tz == r ** 3 * (-a / 2) + r ** 4 * (a * a / 2)
    assert qx == r ** 4 * (a / 12) + r ** 5 * (-(a * a) / 4) + r ** 6 * (a ** 3 / 6)
    st = sx * tz - tx * sz
    assert st == r ** 5 * b ** 2 * (Q(1, 2) - r * a)
    # Axial (T,Q) minor at this same alpha, beta set to 0.
    jets_axis = pinned_jets(r, k, free)
    fx_axis = eval_deriv(jets_axis, 1, 0, r * r * a, 0)
    assert fx_axis == r ** 3 * (-6 * k * a) + r ** 4 * (6 * k * a * a)
    t_in_z = r ** 3 * (-a / 2) + r ** 4 * (a * a / 2)
    q_in_x = r ** 4 * (a / 12) + r ** 5 * (-(a * a) / 4) + r ** 6 * (a ** 3 / 6)
    tq = q_in_x * t_in_z
    poly = 1 - 4 * r * a + 5 * r * r * a * a - 2 * r ** 3 * a ** 3
    # f_z coefficient of T starts at -a/2, so the product carries that sign.
    # The 2x2 minor (T,Q) is the negative of this product and starts at +r^7 a^2/24.
    assert tq == -(r ** 7 * a * a / 24) * poly
    assert -tq == (r ** 7 * a * a / 24) * poly


def check_gram():
    for r in (Q(0), Q(1, 100), Q(1, 7)):
        for a in (Q(0), Q(1), Q(-3, 2), Q(4)):
            for b in (Q(0), Q(1, 3), Q(-2), Q(5, 2)):
                phi, psi, gap, claimed = gram_pieces(r, a, b)
                assert gap == claimed
                if psi != 0:
                    assert phi / psi ** 2 >= Q(1, 576)
                if b == 0 and a != 0 and r != 0:
                    assert phi / psi ** 2 == Q(1, 576)


def check_contact_and_soft_factors():
    for t in (Q(0), Q(1), Q(-3, 2), Q(2, 7)):
        for c in (Q(0), Q(3), Q(-1, 4)):
            for k in (Q(1), Q(4, 3)):
                det_m, det_x, det_s = contact_scaled(t, Q(0), c, Q(1, 5), k)
                assert det_m == 0 and det_x == 0
                assert det_s == 6 * k * c - 72 * k * k * t * t
                # Transverse jet Dz does not enter the q=0 value of det(H_S/r).
                other = contact_scaled(t, Q(0), c, Q(9), k)[2]
                assert other == det_s
    # Checksum against the solved degree-4 jet. p=q=1/5, C=1, Dz=2, k=1, Q=U=0.
    closed = contact_scaled(Q(1), Q(1, 5), Q(1), Q(2), Q(1))
    assert closed == (Q(-769, 36), Q(3031, 180), Q(-3433, 36))
    free = blank_free(C=Q(1), D=Q(2))
    for n in (10, 25):
        _, _, det_m, det_x, det_s = solve_st(Q(1, n), Q(1), Q(1, 5), Q(1, 5), free)
        assert (det_m / Q(1, n) ** 2, det_x / Q(1, n) ** 2, det_s / Q(1, n) ** 2) == closed
    # Both M and X carry a factor q; S does not. Numerator 4(1-2p)^2 det.
    t, q, c, dz, k = Q(1, 3), Q(1, 5), Q(3), Q(1, 4), Q(4, 3)
    det_m, det_x, det_s = contact_scaled(t, q, c, dz, k)
    denom = 4 * (1 - 2 * t * q) ** 2
    num_m, num_x, num_s = denom * det_m, denom * det_x, denom * det_s
    assert num_m != 0 and num_x != 0 and num_s != 0
    # Polynomial vanishing: the q=0 numerator is 0 for M and X, not for S.
    det_m0, det_x0, det_s0 = contact_scaled(t, Q(0), c, dz, k)
    assert det_m0 == 0 and det_x0 == 0 and det_s0 == Q(88, 9)
    assert num_m != det_s * denom and num_x != det_s * denom


def check_quartic_powers_overlap():
    r = Q(1, 20)
    for n in range(1, 9):
        a = Q(n, 8)
        for m in range(0, n + 1):
            b = r * a * Q(m, n)
            ratio = quartic_ratio_symbol(r, a, b, Q(1))
            assert ratio >= (Q(5184, 37)) / r ** 2
        assert quartic_ratio_symbol(r, a, Q(0), Q(1)) == Q(5184) / r ** 2
    assert quartic_ratio_symbol(r, Q(1), r, Q(1)) == Q(5184, 37) / r ** 2
    assert -2 - 5 + 8 + 4 == 5
    assert -2 - 3 + 6 + 2 == 3
    assert -2 + 2 == 0
    assert Q(1, 4) + Q(1, 4) < 1
    assert Q(1, 2) + Q(1, 4) == Q(3, 4) < 1


def mutants():
    caught = []
    phi, psi, _, _ = gram_pieces(Q(1, 20), Q(1), Q(0))
    if phi / psi ** 2 == Q(1, 288):
        raise AssertionError("axis floor mutant agrees")
    caught.append("axis-floor-288")
    if contact_scaled(Q(1), Q(0), Q(0), Q(0), Q(1))[2] == -36:
        raise AssertionError("detS mutant agrees")
    caught.append("detS-36")
    if Q(-1, 2) == Q(-1):
        raise AssertionError("row half mutant agrees")
    caught.append("row-half")
    boundary = quartic_ratio_symbol(Q(1, 20), Q(1), Q(1, 20), Q(1))
    if boundary >= Q(5184, 36) / Q(1, 20) ** 2:
        raise AssertionError("quartic mutant still holds")
    caught.append("quartic-36")
    if -2 - 3 + 5 + 2 == 3:
        raise AssertionError("crude cone power accidentally cubic")
    caught.append("crude-cone-power")
    if Q(1, 2) + Q(1, 2) < 1:
        raise AssertionError("radius mutant still separates the pins")
    caught.append("pin-radius")
    return caught


def main():
    check_rows_and_pins()
    check_row_symbols()
    check_gram()
    check_contact_and_soft_factors()
    check_quartic_powers_overlap()
    caught = mutants()
    if caught != [
        "axis-floor-288", "detS-36", "row-half",
        "quartic-36", "crude-cone-power", "pin-radius",
    ]:
        raise SystemExit(caught)
    print("ok")
    print("mutants", ",".join(caught))


if __name__ == "__main__":
    main()
