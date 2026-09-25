"""Exact arithmetic for the D2 correction's constant mismatch. Not a theorem check."""
from fractions import Fraction as Q


def main():
    alpha, m, kappa = 1, 3, 1
    beta = Q(alpha + 1, m)
    assert beta == Q(2, 3)
    radius = Q(1, 2)
    # h = 2*kappa*r^m at this radius; B = 1; inner integral of r^alpha.
    ell = 2 * kappa * radius**m
    assert ell == Q(1, 4)
    # int_0^R r dr = R^2/2
    cumulative = radius**2 / 2
    assert cumulative == Q(1, 8)
    assert cumulative**3 == Q(1, 512)
    # (ell^{2/3}/2)^3 = ell^2 / 8. Cubing keeps the comparison in Q.
    assert ell**2 / 8 == Q(1, 128)
    # [N / (ell^beta/(alpha+1))]^3 = N^3 / (ell^2/8) = (2^{-beta})^3.
    assert cumulative**3 / (ell**2 / 8) == Q(1, 2) ** 2
    print("correction arithmetic holds")


if __name__ == "__main__":
    main()
