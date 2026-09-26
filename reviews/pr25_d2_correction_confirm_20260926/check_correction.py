"""Exact arithmetic for the D2 cumulative correction. Not a theorem proof.

The identities below are the finite comparisons used in the review:
the sharp ratio-1 constant, the factor 2^{-beta} for h = 2*kappa*r^m,
the c0 domination inequality, the null-amplitude cubes, and the two
sin(1/r) = 0 density values.
"""
from fractions import Fraction as Q


def main():
    alpha, m = 1, 3
    beta = Q(alpha + 1, m)
    assert beta == Q(2, 3)
    # int_0^ell t^{beta-1} dt / m = ell^beta / (alpha+1).
    assert Q(1, m) * Q(1, beta) == Q(1, alpha + 1)

    radius = Q(1, 2)
    # B = 1, so int_0^R r dr = R^2/2.
    cumulative = radius**2 / 2
    assert cumulative == Q(1, 8)

    # h = kappa r^m with kappa = 1. Then ell^beta/(alpha+1) = N exactly.
    ell_sharp = radius**m
    assert ell_sharp == Q(1, 8)
    assert cumulative**3 == ell_sharp**2 / 8 == Q(1, 512)

    # h = 2*kappa*r^m. Ratio is 2, not 1. Candidate constant uses kappa as written.
    ell_twice = 2 * radius**m
    assert ell_twice == Q(1, 4)
    assert cumulative**3 == Q(1, 512)
    assert ell_twice**2 / 8 == Q(1, 128)
    # [N / (ell^beta/(alpha+1))]^3 = (2^{-beta})^3 = 1/4.
    assert cumulative**3 * 8 / ell_twice**2 == Q(1, 4)
    assert Q(1, 2) ** (3 * beta) == Q(1, 4)

    # c0 = 1 is a legal lower comparison: 2*kappa*r^m >= kappa*r^m.
    # R < (ell/(c0*kappa))^{1/m} iff R^m < ell.
    assert radius**m < ell_twice
    # The dominated bound is c0^{-beta}/(alpha+1) = 1/2, and N is strictly below it.
    assert cumulative**3 < ell_twice**2 / 8

    # B(r) = r, B0 = 0, h = r^3. Then int_0^R r^2 dr = R^3/3 and
    # N/ell^beta = R/3, so the normalized cubes decrease to 0.
    previous = None
    for radius_n in (Q(1, 2), Q(1, 4), Q(1, 8)):
        ell = radius_n**m
        integral = radius_n**3 / 3
        # (N/ell^beta)^3 = N^3/ell^2 = (R/3)^3.
        normalized_cube = integral**3 / ell**2
        assert normalized_cube == (radius_n / 3) ** 3
        if previous is not None:
            assert normalized_cube < previous
        previous = normalized_cube
    assert previous == (Q(1, 24)) ** 3

    # At sin(1/r) = 0 the cumulative factor is 1, while the density ratio splits.
    for cosine, density in ((1, Q(1, 2)), (-1, Q(1, 4))):
        sine = 0
        numerator = 1 + sine
        denominator = 3 - cosine + 4 * sine
        assert Q(numerator, denominator) == density
        assert numerator == 1
    print("d2 correction arithmetic holds")


if __name__ == "__main__":
    main()
