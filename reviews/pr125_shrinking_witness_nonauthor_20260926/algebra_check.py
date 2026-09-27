"""Independent certificates for the main PR125 shrinking-witness review.

Rational arithmetic only. These checks rederive the note's displayed
identities. They do not sample a Gaussian field, do not evaluate the
periodized pinned kernel, and do not install a sharper radius exponent.
"""
from __future__ import annotations

from fractions import Fraction


def det(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    total = 0
    for col, entry in enumerate(matrix[0]):
        minor = [row[:col] + row[col + 1 :] for row in matrix[1:]]
        total += ((-1) ** col) * entry * det(minor)
    return total


def jacobian_matrix(dim, delta):
    """Columns (G0, G1), rows (G0, G0 + delta G1)."""
    size = 2 * dim
    matrix = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for i in range(dim):
        matrix[i][i] = Fraction(1)
        matrix[dim + i][i] = Fraction(1)
        matrix[dim + i][dim + i] = delta
    return matrix


def axial_jets(delta, mu, nu, rho):
    """Solve h(delta)=0 for the axial derivative h(0)=0, h'(0) unknown.

    h(s) = alpha*s + mu*s**2/2 + nu*s**3/6 + rho*s**4/24.
    The field gap is the integral of h. alpha_far is h'(delta).
    """
    alpha = -(mu * delta / 2 + nu * delta**2 / 6 + rho * delta**3 / 24)
    alpha_far = alpha + mu * delta + nu * delta**2 / 2 + rho * delta**3 / 6
    gap = (
        alpha * delta**2 / 2
        + mu * delta**3 / 6
        + nu * delta**4 / 24
        + rho * delta**5 / 120
    )
    residual = alpha * delta + mu * delta**2 / 2 + nu * delta**3 / 6 + rho * delta**4 / 24
    return alpha, alpha_far, gap, residual


def det3(h11, h12, h13, h22, h23, h33):
    return (
        h11 * (h22 * h33 - h23**2)
        - h12 * (h12 * h33 - h13 * h23)
        + h13 * (h12 * h23 - h13 * h22)
    )


def check_jacobian():
    for dim in (2, 3, 4):
        for delta in (Fraction(1, 3), Fraction(2, 5), Fraction(1), Fraction(1, 8)):
            if det(jacobian_matrix(dim, delta)) != delta**dim:
                raise SystemExit(f"jacobian failed dim={dim} delta={delta}")


def check_singular_values():
    for alpha, beta, gamma in (
        (Fraction(1, 7), Fraction(1, 7), Fraction(3)),
        (Fraction(-2, 5), Fraction(1, 4), Fraction(-6)),
        (Fraction(0), Fraction(0), Fraction(4)),
    ):
        determinant = alpha * gamma - beta**2
        hu2 = alpha**2 + beta**2
        frobenius2 = alpha**2 + 2 * beta**2 + gamma**2
        if determinant**2 > hu2 * frobenius2:
            raise SystemExit("d=2 singular-value comparison failed")
    samples = (
        (Fraction(1, 3), Fraction(-1, 5), Fraction(2, 7), Fraction(4), Fraction(1, 2), Fraction(-3)),
        (Fraction(1, 8), Fraction(0), Fraction(0), Fraction(5), Fraction(1, 9), Fraction(2)),
        (Fraction(-1, 2), Fraction(1, 3), Fraction(-1, 4), Fraction(1), Fraction(0), Fraction(6)),
    )
    for h11, h12, h13, h22, h23, h33 in samples:
        determinant = det3(h11, h12, h13, h22, h23, h33)
        hu2 = h11**2 + h12**2 + h13**2
        frobenius2 = (
            h11**2 + h22**2 + h33**2 + 2 * (h12**2 + h13**2 + h23**2)
        )
        # |det| <= ||Hu|| ||H||_F^{2} squares to det**2 <= hu2 * (||H||_F^2)**2.
        if determinant**2 > hu2 * frobenius2**2:
            raise SystemExit("d=3 singular-value comparison failed")


def check_height_gap():
    delta, mu, nu, rho = Fraction(2, 7), Fraction(3), Fraction(-5), Fraction(11)
    alpha, alpha_far, gap, residual = axial_jets(delta, mu, nu, rho)
    if residual != 0:
        raise SystemExit("axial derivative was not pinned at distance delta")
    if alpha != -(delta / 2) * mu - (delta**2 / 6) * nu - (delta**3 / 24) * rho:
        raise SystemExit("near axial coefficient mismatch")
    if alpha_far != (delta / 2) * mu + (delta**2 / 3) * nu + (delta**3 / 8) * rho:
        raise SystemExit("far axial coefficient mismatch")
    if gap != -(mu * delta**3) / 12 - (nu * delta**4) / 24 - (rho * delta**5) / 80:
        raise SystemExit("height-gap coefficient mismatch")
    alpha, alpha_far, _gap, _residual = axial_jets(Fraction(1, 5), Fraction(4), 0, 0)
    if alpha * alpha_far >= 0:
        raise SystemExit("pure third derivative did not force opposite signs")
    delta = Fraction(1, 4)
    alpha, alpha_far, _gap, _residual = axial_jets(delta, delta * Fraction(-3), Fraction(6), 0)
    if alpha / delta**2 != Fraction(1, 2) or alpha_far / delta**2 != Fraction(1, 2):
        raise SystemExit("fourth-derivative same-sign window failed")
    alpha, alpha_far, _gap, _residual = axial_jets(delta, 0, Fraction(6), 0)
    if alpha * alpha_far >= 0:
        raise SystemExit("pure fourth derivative did not force opposite signs")


def check_radial_integral():
    for dim in (2, 3, 5, 8):
        if (2 - dim) + (dim - 1) != 1:
            raise SystemExit(f"radial exponent failed in dimension {dim}")
    eta, radius = Fraction(1, 10**8), Fraction(1, 8)
    integral = (radius**2 - eta**2) / 2
    if not (0 < integral < radius**2 / 2):
        raise SystemExit("radial integral left the expected range")
    if radius**2 / 2 - integral != eta**2 / 2:
        raise SystemExit("radial limit identity failed")


def check_bargmann_contact_scale():
    # Var(d^3 f / dx^3) = 15, Cov(df/dx, d^3 f/dx^3) = -3, Var(df/dx) = 1.
    variance = 15 - ((-3) ** 2) // 1
    if variance != 6:
        raise SystemExit("third-derivative residual variance failed")
    # (sqrt(6)/12)^2 = 1/24. The printed diagnostic 0.204 is 51/250.
    printed = Fraction(51, 250)
    difference = Fraction(1, 24) - printed**2
    if difference != Fraction(19, 375000):
        raise SystemExit("diagnostic square comparison failed")
    if difference <= 0:
        raise SystemExit("printed 0.204 is not below sqrt(6)/12")


def check_split_majorant_arithmetic():
    """Arithmetic of a height-split ledger. Not a field theorem.

    Integrate w * min(s, w/(kappa s**2)) from 0 to R. The kink is
    t = (w/kappa)**(1/3). For w = kappa t**3 the integral equals
    (3/2) kappa t**5 - kappa t**6 / R, which is the expanded form of
    (3/2) kappa**(-2/3) w**(5/3) - w**2 / (kappa R).
    """
    radius = Fraction(1)
    kappa = Fraction(1)
    for denominator in (2, 8, 100):
        split_point = Fraction(1, denominator)
        window = kappa * split_point**3
        if split_point >= radius:
            raise SystemExit("ledger split point is outside the radius")
        integrated = (window * split_point**2) / 2 + (window**2 / kappa) * (
            1 / split_point - 1 / radius
        )
        expected = (
            Fraction(3, 2) * kappa * split_point**5
            - kappa * split_point**6 / radius
        )
        if integrated != expected:
            raise SystemExit(
                f"split ledger mismatch integrated={integrated} expected={expected}"
            )
        crude = window * radius**2 / 2
        if crude <= integrated:
            raise SystemExit("crude one-window majorant did not exceed the split")


def main():
    check_jacobian()
    check_singular_values()
    check_height_gap()
    check_radial_integral()
    check_bargmann_contact_scale()
    check_split_majorant_arithmetic()
    print("all certificates passed")


if __name__ == "__main__":
    main()
