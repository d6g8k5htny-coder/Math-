"""Exact checks for the two-scale addendum review. Standard library only.

These identities corroborate finite algebra in TWO_SCALE_ADDENDUM.md at blob
89cae3a9734f2ec7172cd0b6b0b3af3ddd355d73. They do not accept the analytic bound.
"""
from fractions import Fraction as Q


def main():
    u = Q(2)
    gap = u * u - Q(1, 4)
    a = u * gap / 6
    b = gap / 2
    assert 6 * gap == Q(45, 2)

    delta, alpha, beta = Q(1, 9), Q(3, 5), Q(4, 5)
    r, t = delta * alpha, delta * beta
    assert (r**3 * a + r**2 * t * u) / (r**2 * delta) == alpha * a + beta * u
    assert (r**2 * b + r * t) / (r * delta) == alpha * b + beta
    assert (r * r * delta) * (r * delta) == r**3 * delta**2

    for alpha2 in (Q(0), Q(1), Q(1, 2), Q(1, 3), Q(3, 4)):
        beta2 = 1 - alpha2
        assert alpha2**2 + beta2**2 >= Q(1, 2)
    assert Q(1, 2) ** 2 + Q(1, 2) ** 2 == Q(1, 2)

    assert -3 - 2 + 2 == -3
    assert -2 - 6 == -8
    assert -3 - 7 * Q(1) == -10
    assert -3 - 7 * Q(1, 2) == Q(-13, 2)

    # D_N^2 = c / (2(N+4)) makes the r exponent at least N+1.
    for n in range(0, 8):
        assert (n + 4) - 3 == n + 1

    # Leading pin curvature: f_xxx = 12k evaluated at distance r/2.
    k = Q(1)
    assert 12 * k * (r / 2) == 6 * k * r
    print("two-scale algebra holds")


if __name__ == "__main__":
    main()
