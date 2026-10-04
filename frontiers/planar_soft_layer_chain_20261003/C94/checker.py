"""Independent C94 algebra/inference diagnostics; Python stdlib only.

No author checker is read. These finite controls do not establish uniform
Gaussian estimates, Borel measurability, or topology. No assert statement is
used: every check remains active with python -O. Fractions give exact arithmetic.
"""

from fractions import Fraction as F
from itertools import product


counts = {}
negative = []


def check(group, condition):
    if not condition:
        raise RuntimeError("failed control: " + group)
    counts[group] = counts.get(group, 0) + 1


def reject(name, false_claim):
    if false_claim:
        raise RuntimeError("adverse fixture did not reject: " + name)
    negative.append(name)


def con(value, n=2):
    return {(0,) * n: F(value)} if value else {}


def var(index, n=2):
    powers = [0] * n
    powers[index] = 1
    return {tuple(powers): F(1)}


def add(*polys):
    result = {}
    for poly in polys:
        for key, value in poly.items():
            result[key] = result.get(key, F(0)) + value
    return {key: value for key, value in result.items() if value}


def scale(poly, scalar):
    return {key: value * scalar for key, value in poly.items() if value * scalar}


def mul(left, right):
    result = {}
    for a, va in left.items():
        for b, vb in right.items():
            key = tuple(x + y for x, y in zip(a, b))
            result[key] = result.get(key, F(0)) + va * vb
    return {key: value for key, value in result.items() if value}


def power(poly, exponent, n=2):
    result = con(1, n)
    for _ in range(exponent):
        result = mul(result, poly)
    return result


def power_integral(exponent, low, high):
    if exponent == -1:
        raise ValueError("logarithmic integral is not a rational control")
    return (high ** (exponent + 1) - low ** (exponent + 1)) / F(exponent + 1)


def radius_integral(upper):
    # The inner s-integral is 1152 lambda^3, integrated in lambda.
    return F(1152) * power_integral(3, F(0), upper)


def gaussian_monomial(powers):
    moment = F(1)
    for exponent in powers:
        if exponent % 2:
            return F(0)
        for odd in range(1, exponent, 2):
            moment *= odd
    return moment


def gaussian_expectation(poly):
    return sum((value * gaussian_monomial(key) for key, value in poly.items()), F(0))


def rate_ledger(beta, band_power, moment):
    value_power = 1 - 4 * beta
    return (8 * beta, 1 + 4 * beta, value_power,
            1 + value_power / 2, band_power, F(1),
            moment * (value_power - band_power), 2 - 4 * beta)


def run():
    # Literal independently integrated RED fixture, now GREEN.
    check("radius-integrals", radius_integral(F(1, 2)) == 18)
    x, z = var(0), var(1)
    axial = add(scale(power(x, 3), 2), scale(x, -F(3, 2)), con(-F(1, 2)))
    gammas = (F(-3, 2), F(-1, 2), F(1, 2), F(3, 2))
    lambdas = (F(1, 16), F(1, 3), F(2))
    bjets = (F(-1, 2), F(0), F(2, 3))
    cjets = (F(-1, 3), F(0), F(5, 4))
    for gamma, lam, bjet, cjet in product(gammas, lambdas, bjets, cjets):
        psi = 24 * lam / gamma ** 2
        disc = gamma ** 2 - 12 * bjet
        jpoly = 8 * gamma ** 3 - 144 * bjet * gamma + 576 * cjet
        c, rjet = disc / gamma ** 2, jpoly / gamma ** 3
        u, zz = add(x, scale(z, gamma / 12)), scale(z, gamma)
        transformed = add(scale(power(u, 3), 2), scale(u, -F(3, 2)),
                          con(-F(1, 2)),
                          scale(mul(add(con(psi), scale(u, 2 * c)), power(zz, 2)), -F(1, 48)),
                          scale(power(zz, 3), rjet / 3456))
        raw = add(axial, scale(mul(add(power(x, 2), con(-F(1, 4))), z), gamma / 2),
                  scale(power(z, 2), -lam / 2),
                  scale(mul(x, power(z, 2)), bjet / 2), scale(power(z, 3), cjet / 6))
        check("raw-polynomial", transformed == raw)
        a_m, a_s = 24 * lam - disc, 24 * lam + disc
        check("jacobians-poles", a_m == gamma ** 2 * (psi - c))
        check("jacobians-poles", a_s == gamma ** 2 * (psi + c))
        weight = a_m * a_s / 16
        check("jacobians-poles", weight * gamma ** 2 / 24 ==
              gamma ** 6 * (psi ** 2 - c ** 2) / 384)
        check("jacobians-poles", gamma ** 6 * abs(c) ** 3 == abs(disc) ** 3)
        check("jacobians-poles", gamma ** 6 * rjet ** 2 == jpoly ** 2)
        step = F(1, 7)
        check("jacobians-poles", (24 * lam + gamma ** 2 - 12 * (bjet - step / 12)) - a_s == step)
        check("jacobians-poles", (24 * lam - gamma ** 2 + 12 * (bjet + step / 12)) - a_m == step)

    for gamma, sqrtpsi, u, fraction in product(
            (F(-3), F(-1, 2), F(1, 4), F(2)),
            (F(1, 3), F(1), F(2)),
            (F(-5, 4), F(-1, 2), F(1, 2), F(3, 2)),
            (F(-1), F(-1, 2), F(0), F(1, 2), F(1))):
        zz = 30 * fraction / sqrtpsi
        raw_x, raw_z = u - zz / 12, zz / gamma
        radius = F(3, 2) + F(5, 2) * (abs(gamma) + 12) / (abs(gamma) * sqrtpsi)
        check("raw-box-radius", raw_x ** 2 + raw_z ** 2 <= radius ** 2)
        lam = gamma ** 2 * sqrtpsi ** 2 / 24
        h = F(25, 96) * (abs(gamma) + 12) ** 2
        check("raw-box-radius", (radius - F(3, 2)) ** 2 * lam == h)

    for upper, r in product((F(1, 2 ** j) for j in range(1, 10)), (F(1, 1000), F(1, 10), F(1, 2))):
        check("radius-integrals", radius_integral(upper) == 288 * upper ** 4)
        residual = 48 * r * power_integral(1, F(0), upper)
        check("radius-integrals", residual == 24 * r * upper ** 2)
        check("radius-integrals", radius_integral(upper) / 12 == 24 * upper ** 4)
        check("radius-integrals", residual / 12 == 2 * r * upper ** 2)
        inner = ((48 * upper) * power_integral(1, F(0), 48 * upper)
                 - power_integral(2, F(0), 48 * upper)) / 16
        check("radius-integrals", inner == 1152 * upper ** 3)

    a_squared = F(4, 27)
    omega_values = (F(-99, 100), F(-3, 4), F(-1, 2), F(-1, 4), F(0), F(1, 4), F(1, 2))
    for cap, relative_lam, omega, relative_r in product(
            (F(1, 20), F(1, 3), F(1), F(5)),
            (F(1, 10), F(1, 2), F(1)), omega_values, (F(0), F(1, 2), F(1))):
        lam, edge_cap = cap * relative_lam, 48 * cap
        s = 24 * lam * (1 + omega)
        tau_s_over_a = 1 + 3 * abs(omega) / (1 + omega) + relative_r * (1 - 2 * omega) / (1 + omega)
        check("A1-tolerance", tau_s_over_a <= (2 - omega + 3 * abs(omega)) / (1 + omega))
        check("A1-tolerance", tau_s_over_a <= 3 * edge_cap / s)
        remaining = 3 - 3 * abs(omega) / (1 - omega)
        f_squared = (1 - 2 * omega) ** 2 * (1 + omega) / (1 - omega) ** 3
        check("A1-tolerance", remaining >= 0 and relative_r ** 2 * f_squared <= remaining ** 2)
        m_lower = 2 / (125 * a_squared * tau_s_over_a ** 2)
        c_star = F(3, 250) / edge_cap ** 2
        check("A1-tolerance", m_lower >= c_star * s ** 2)
        check("A1-tolerance", F(27, 512) >= c_star * s ** 2)
        check("A1-tolerance", c_star * edge_cap ** 2 == F(3, 250))

    for cutoff, cap, r in product((F(1, 2 ** j) for j in range(1, 8)),
                                  (F(1), F(2), F(4)), (F(1, 1000), F(1, 10), F(1, 2))):
        epsilon = cutoff ** 2
        exact_away = power_integral(-3, cutoff, cap) + r * power_integral(-4, cutoff, cap)
        dropped = 1 / (2 * cutoff ** 2) + r / (3 * cutoff ** 3)
        check("value-truncation", 0 <= exact_away <= dropped)
        cost = cutoff ** 2 + r * cutoff + epsilon ** 2 * exact_away
        check("value-truncation", cost <= F(3, 2) * epsilon + F(4, 3) * r * cutoff)
        check("value-truncation", cutoff ** 2 + r * cutoff + epsilon ** 2 * dropped ==
              F(3, 2) * epsilon + F(4, 3) * r * cutoff)
        check("value-truncation", power_integral(-3, cap, cap) + r * power_integral(-4, cap, cap) == 0)
    for epsilon, norm, s in product((F(1, 128), F(1, 8), F(1, 2)),
                                    (F(1), F(2), F(8)), (F(1, 64), F(1, 4), F(1, 2), F(1))):
        bad = int(epsilon * norm >= s ** 2)
        check("value-truncation", bad <= epsilon ** 2 * norm ** 2 / s ** 4)

    for v, mu, error, band in product((F(1, 16), F(1, 4), F(1)),
                                      (None, -F(1, 64), -F(1, 4), -F(2)),
                                      (F(0), F(1, 128), F(1, 8), F(1)),
                                      (F(1, 128), F(1, 16), F(1, 4))):
        eta = v / 2 if mu is None else min(v, -mu) / 2
        level_bad = mu is not None and error >= -mu / 2
        check("random-margin-union", (error >= eta) == (error >= v / 2 or level_bad))
        near = mu is not None and -2 * band <= mu < 0
        check("random-margin-union", not level_bad or near or error >= band)
        check("random-margin-union", eta > 0 and eta < v and (mu is None or eta < -mu))

    for cap in (F(1, 100), F(1, 10), F(1, 3), F(1), F(10)):
        lam, gamma = cap / 2, F(1)
        bjet, cjet = (1 + 6 * cap) / 12, (1 + 18 * cap) / 144
        psi, c = 24 * lam, 1 - 12 * bjet
        j = 8 - 144 * bjet + 576 * cjet
        a_m, a_s = 24 * lam - 1 + 12 * bjet, 24 * lam + 1 - 12 * bjet
        check("positive-sector", 0 < lam < cap and a_m == 18 * cap and a_s == 6 * cap)
        check("positive-sector", a_m * a_s / 16 == F(27, 4) * cap ** 2)
        check("positive-sector", j == 0 and psi > abs(c) and psi > 2 * c)
        discriminant = j ** 2 + 64 * c * (psi ** 2 - c ** 2)
        check("positive-sector", discriminant == -41472 * cap ** 3 and discriminant < 0)
        check("positive-sector", 0 < 16 * (psi - 2 * c) ** 2 * (psi + c))

    expected = (F(1, 2), F(5, 4), F(3, 4), F(11, 8), F(1, 2), F(1), F(1, 2), F(7, 4))
    ledger = rate_ledger(F(1, 16), F(1, 2), F(2))
    for got, want in zip(ledger, expected):
        check("rates-normalization", got == want and 3 + got >= F(7, 2))
    check("rates-normalization", min(ledger) == F(1, 2))
    check("rates-normalization", 1 - F(1, 16) > 0 and 1 - 4 * F(1, 16) > 0)
    for r, mass, z in product((F(1, 16), F(1, 64), F(1, 256)),
                               (F(1, 2), F(2)), (F(3), F(5))):
        check("rates-normalization", r ** 5 * mass / (r ** 2 * z) == r ** 3 * mass / z)
        # Difference of reciprocals with a positive floor, not a layer normalizer.
        check("rates-normalization", abs(1 / (z + r) - 1 / z) <= r / z ** 2)

    # Adverse inference fixtures are explicit mathematical counterexamples,
    # not Gaussian claims about this field. The Gaussian fixture below IS
    # a nonsingular centered correlated Gaussian, but not the actual jet law.
    reject("lost-B1-Jacobian", F(1) == F(1, 12))
    reject("lost-gamma6-Jacobian", F(2) ** 6 / 384 == F(2) ** 4 / 384)
    reject("wrong-radius-integration-power", radius_integral(F(1, 2)) == 288 * F(1, 2) ** 3)
    r, upper = F(1, 8), F(1, 64)
    actual = 288 * upper ** 4 + 24 * r * upper ** 2
    reject("omitted-radius-residual", actual <= 2 * 288 * upper ** 4)
    r, edge = F(1, 16), F(1, 4096)
    reject("omitted-value-strip-residual", edge ** 2 + r * edge <= 10 * edge ** 2)
    # A small L1 perturbation moved to a small margin does not bound inverses.
    tv_error, small_margin = F(1, 100), F(1, 10000)
    reject("TV-times-unbounded-inverse", tv_error / small_margin <= 10 * tv_error)
    cutoff = F(1, 4096)
    actual_inverse = power_integral(-2, cutoff, F(1)) + F(1, 16) * power_integral(-3, cutoff, F(1))
    reject("model-inverse-only-at-finite-r", actual_inverse <= 2 * power_integral(-2, cutoff, F(1)))
    # Two equiprobable atoms, W=(0,1), N=(1,4).
    e_wn2, e_w, e_n2 = F(8), F(1, 2), F(17, 2)
    reject("factorized-weighted-norm", e_wn2 == e_w * e_n2)
    reject("unweighted-bad-probability", F(1, 2) == e_w * F(1, 2))
    # X,Y,Z independent N(0,1); gamma=X, B=Y, C=X+Z has covariance det=1.
    xx, yy, zz = (var(i, 3) for i in range(3))
    j = add(scale(power(xx, 3, 3), 8), scale(mul(xx, yy), -144), scale(add(xx, zz), 576))
    actual_j2 = gaussian_expectation(power(j, 2, 3))
    check("correlated-Gaussian", actual_j2 == 712896)
    check("correlated-Gaussian", gaussian_expectation(mul(power(xx, 3, 3), add(xx, zz))) == 3)
    reject("independent-reference-cross-terms", actual_j2 == 685248)
    # C82 c=0,R=1 has exact coarea density 1/48 in v. On |v|<=1/8,
    # width(v)=1/128+2|v| stays <=1/2 and includes the whole interval.
    variable_band_mass = F(1, 4) / 48
    fixed_central_width_mass = F(1, 128) / 24
    reject("psi-dependent-band-width", variable_band_mass <= fixed_central_width_mass)
    reject("dropped-joint-slice-density", F(2) * F(3, 7) == F(3, 7))
    r, mass, z = F(1, 16), F(2), F(3)
    reject("soft-layer-as-full-normalizer", r ** 5 * mass / (r ** 5 * mass) == r ** 3 * mass / z)
    reject("global-Good-probability-one", r ** 3 * mass / z == 1)
    reject("overclaimed-rate-r4", min(ledger) + 3 >= 4)
    reject("unrestricted-window-growth", min(rate_ledger(F(1, 8), F(1, 2), F(2))) > 0)
    gamma = F(0)
    try:
        _ = F(1) / gamma ** 2
    except ZeroDivisionError:
        negative.append("pointwise-gamma-zero-chart")
    else:
        raise RuntimeError("adverse gamma-zero chart did not reject")

    print("C94 independent exact diagnostics")
    for group, count in counts.items():
        print(group + ": " + str(count) + " PASS")
    print("positive controls: " + str(sum(counts.values())))
    print("false-inference fixtures: " + str(len(negative)) + " REJECTED")
    print("negative names: " + ", ".join(negative))
    print("Scope: algebra/inference controls only; Gaussian bounds and conditional G require analytic review.")


if __name__ == "__main__":
    run()
