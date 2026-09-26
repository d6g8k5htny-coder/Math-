"""Exact checks for the pin-neighborhood review. Not a proof of the Gaussian integral."""
from fractions import Fraction as Q


def minor_sum(p, q):
    rows = (
        (Q(0), q * (p - Q(1, 2)), q ** 2 / 2),
        (q, Q(0), Q(0)),
    )
    pairs = ((0, 1), (0, 2), (1, 2))
    total = Q(0)
    for i, j in pairs:
        det = rows[0][i] * rows[1][j] - rows[0][j] * rows[1][i]
        total += det ** 2
    return total


def drifts():
    # H'(x)/r^2 at x=-r/2+r p equals 6 p(p-1). The r^2 terms cancel.
    for p in (Q(-1, 4), Q(0), Q(1, 5), Q(1, 4), Q(1)):
        expanded = -Q(3, 2) + 6 * (p - Q(1, 2)) ** 2
        assert expanded == 6 * p * (p - 1)
        right = -Q(3, 2) + 6 * (p + Q(1, 2)) ** 2
        assert right == 6 * p * (p + 1)
        assert right - expanded == 12 * p
    assert 6 * Q(-1, 4) * Q(-5, 4) == Q(15, 8)


def axis_ratio():
    best = None
    for n in range(-8, 9):
        p = Q(n, 32)
        if p == 0:
            continue
        mean = 6 * p * (p - 1)
        noise = p * (2 * p - 1) * (p - 1) / 12
        ratio = (mean / noise) ** 2
        assert ratio == 5184 / (2 * p - 1) ** 2
        if best is None or ratio < best:
            best = ratio
    assert best == 2304


def cone_powers():
    # Z^{-1} is r^{-2}, gradient Jacobian r^3 q^2, determinant product r^5.
    assert -2 - 3 + 5 == 0
    # Physical area r^2, cone width |q|, intensity 1/q^2: integrand r^2 / |q|.
    assert 2 + 1 - 2 == 1


def overlap():
    # |s|<=1/4 around M=(-1/2,0) reaches rho=3/4 < 1 < A.
    assert Q(1, 2) + Q(1, 4) == Q(3, 4)
    assert Q(3, 4) < 1
    # Distance from either pin to rho=A is A-1/2 > 1/2 whenever A>1.
    radius = Q(3, 2)
    assert radius - Q(1, 2) > Q(1, 2)


def inner_disk_density_not_uniform():
    """Leading (S,T) model at p=0. The r^5 normalization is not uniformly O(1)."""
    # Var(f_x)=(r^2 |q|/2)^2, Var(f_z)=(r|q|)^2, independent, mean zero.
    # sqrt(det Sigma) = r^3 q^2 / 2.
    # Density prefactor ratio against 1/r^5 is 2 r^2 / q^2, up to the constant 1/(2π).
    r = Q(1, 100)
    kappa = 20
    for q_over in (Q(1, 1), Q(1, 10), Q(1, 100)):
        q = kappa * r * q_over
        ratio = 2 * r ** 2 / q ** 2
        # Claimed uniform factor is order 1/kappa^2. The model exceeds it by 1/q_over^2.
        assert ratio == 2 / (kappa ** 2 * q_over ** 2)
    assert 2 * r ** 2 / (kappa * r / 100) ** 2 == 2 * 100 ** 2 / kappa ** 2
    # At the inner edge |q|=kappa*r the ratio is 2/kappa^2.
    # One decade closer it is 100 times larger. Not a uniform O(1/kappa^2) bound.


def determinant_power_in_cone():
    # |q|>=kappa*r turns r^2/|q| into at most r/kappa.
    # Three factors: r^2, r^2/|q|, r^2. Product <= r^5 / kappa.
    kappa = 20
    q = kappa  # in units of r, so |q|=kappa*r
    product_over_r5 = Q(1) / q
    assert product_over_r5 == Q(1, kappa)


def main():
    for p in (Q(0), Q(1, 4), Q(-1, 5), Q(1, 2)):
        for q in (Q(0), Q(1, 3), Q(-1, 7)):
            assert minor_sum(p, q) == q ** 4 * ((p - Q(1, 2)) ** 2 + q ** 2 / 4)
    # Limit map (T,S) -> (-T/2, S) has minor 1/2.
    assert -(Q(-1, 2)) == Q(1, 2)
    drifts()
    axis_ratio()
    cone_powers()
    overlap()
    inner_disk_density_not_uniform()
    determinant_power_in_cone()
    print("pin-chart arithmetic holds")


if __name__ == "__main__":
    main()
