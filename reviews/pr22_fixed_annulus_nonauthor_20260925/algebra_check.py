#!/usr/bin/env python3
"""Exact rational checks for FIXED_ANNULUS_CANDIDATE identities.

Standard library only. A passing run checks finite identities. It does not
replace the continuum argument in REVIEW.md.
"""

from fractions import Fraction


def det3(rows):
    (a, b, c), (d, e, f), (g, h, i) = rows
    return (
        a * (e * i - f * h)
        - b * (d * i - f * g)
        + c * (d * h - e * g)
    )


def check_pin_target():
    r = Fraction(2, 5)
    k = Fraction(3, 7)
    b = Fraction(11, 4)
    a = r / 2

    def height(x):
        return b - k * r**3 / 2 - Fraction(3, 2) * k * r**2 * x + 2 * k * x**3

    def slope(x):
        return -Fraction(3, 2) * k * r**2 + 6 * k * x**2

    assert height(-a) == b
    assert height(a) == b - k * r**3
    assert slope(-a) == 0
    assert slope(a) == 0
    # Second derivative of this cubic is 12*k*x, so f_xx(M)/r = -6k.
    assert (12 * k * (-a)) / r == -6 * k
    assert (12 * k * a) / r == 6 * k

    s0 = (height(-a) + height(a)) / 2
    d0 = (height(a) - height(-a)) / (2 * a)
    s1 = (slope(-a) + slope(a)) / 2
    d1 = (slope(a) - slope(-a)) / (2 * a)
    second = (3 * d0 - s1) / 2
    fourth = 3 * (s1 - d0) / a**2
    assert s0 - a**2 * d1 / 2 == b - k * r**3 / 2
    assert second == -Fraction(3, 2) * k * r**2
    assert d1 == 0
    assert fourth == 12 * k


def check_contact_matrix():
    r = Fraction(1, 3)
    u = Fraction(5, 2)
    t = Fraction(-2, 5)
    k = Fraction(4, 3)
    b = Fraction(1, 2)
    curvature = Fraction(7, 2)
    mixed = Fraction(-3, 5)
    cubic = Fraction(8, 7)
    pure = Fraction(-1, 6)
    value = b - k * r**3 / 2
    dx = -(r**2 / 8) * (12 * k)
    dxx = 0
    dxxx = 12 * k
    dz = -(r**2 / 8) * mixed
    dxz = 0
    dzz = curvature
    dxxz = mixed
    dxzz = cubic
    dzzz = pure
    x = r * u
    z = r * t
    field = (
        value
        + x * dx
        + z * dz
        + (x**2 / 2) * dxx
        + x * z * dxz
        + (z**2 / 2) * dzz
        + (x**3 / 6) * dxxx
        + (x**2 * z / 2) * dxxz
        + (x * z**2 / 2) * dxzz
        + (z**3 / 6) * dzzz
    )
    fx = (
        dx
        + x * dxx
        + z * dxz
        + (x**2 / 2) * dxxx
        + x * z * dxxz
        + (z**2 / 2) * dxzz
    )
    fz = (
        dz
        + x * dxz
        + z * dzz
        + (x**2 / 2) * dxxz
        + x * z * dxzz
        + (z**2 / 2) * dzzz
    )
    observed = (
        fx / r**2,
        fz / r,
        (field - b - (r * t / 2) * fz) / r**3,
    )
    second_remainder = r * (
        (u**2 - Fraction(1, 4)) * mixed / 2
        + u * t * cubic
        + (t**2 / 2) * pure
    )
    predicted = (
        6 * k * (u**2 - Fraction(1, 4)) + u * t * mixed + (t**2 / 2) * cubic,
        t * curvature + second_remainder,
        k * (2 * u**3 - Fraction(3, 2) * u - Fraction(1, 2))
        + ((u**2 - Fraction(1, 4)) * t / 4) * mixed
        - (t**3 / 12) * pure,
    )
    assert observed == predicted

    minor = [
        [0, t**2 / 2, 0],
        [t, 0, 0],
        [0, 0, -(t**3) / 12],
    ]
    assert det3(minor) == t**6 / 24

    # Affine map (f_x, f_z, f) -> J_r is triangular with determinant r^-6.
    # Row three also depends on f_z; that entry does not change the determinant.
    assert (1 / r**2) * (1 / r) * (1 / r**3) == r**-6


def check_cutoff_and_ledgers():
    q = Fraction(1, 24)
    assert 12 * q < 1
    assert 1 - 12 * q == Fraction(1, 2)
    assert 18 + 72 + 6 == 96
    assert -6 + 6 + 3 + -2 == 1
    assert 168 * Fraction(1, 12) == 14
    assert 14 - 13 == 1
    for i in range(21):
        alpha2 = Fraction(i, 20)
        beta2 = 1 - alpha2
        assert alpha2**2 + beta2**2 >= Fraction(1, 2)


def check_inner_chart():
    radius = Fraction(3, 2)
    inner = (radius + 1) / 2
    assert inner > 1
    assert inner**2 > Fraction(1, 4)
    gap = radius**2 - inner**2
    assert gap > 0
    transverse2 = gap / 2
    assert radius**2 - transverse2 > inner**2


def main():
    check_pin_target()
    check_contact_matrix()
    check_cutoff_and_ledgers()
    check_inner_chart()
    print("ok")


if __name__ == "__main__":
    main()
