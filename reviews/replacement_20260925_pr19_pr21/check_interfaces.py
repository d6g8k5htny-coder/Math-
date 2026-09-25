"""Exact checks behind the replacement review. Standard library only.

Passing this file corroborates finite identities. It does not accept a theorem
and it does not read the author packages.
"""
from fractions import Fraction as Q
from math import factorial


def fact(n):
    return factorial(n)


def deriv(poly, dx, dz):
    out = {}
    for (i, j), coefficient in poly.items():
        if i >= dx and j >= dz:
            factor = (fact(i) // fact(i - dx)) * (fact(j) // fact(j - dz))
            key = (i - dx, j - dz)
            out[key] = out.get(key, Q(0)) + coefficient * factor
    return out


def evaluate(poly, x, z):
    total = Q(0)
    x, z = Q(x), Q(z)
    for (i, j), coefficient in poly.items():
        total += coefficient * x**i * z**j
    return total


def solve(augmented):
    matrix = [list(map(Q, row)) for row in augmented]
    size = len(matrix)
    for col in range(size):
        pivot = next(i for i in range(col, size) if matrix[i][col])
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        scale = matrix[col][col]
        matrix[col] = [value / scale for value in matrix[col]]
        for i in range(size):
            if i != col and matrix[i][col]:
                factor = matrix[i][col]
                matrix[i] = [v - factor * w for v, w in zip(matrix[i], matrix[col])]
    return [row[-1] for row in matrix]


PIVOTS = ((0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1))
PINS = ((0, 0, -1), (0, 0, 1), (1, 0, -1), (1, 0, 1), (0, 1, -1), (0, 1, 1))


def pin_polynomial(r, free, b=Q(2), k=Q(1)):
    r = Q(r)
    matrix, rhs = [], []
    targets = (b, b - k * r**3, 0, 0, 0, 0)
    for (dx, dz, sign), target in zip(PINS, targets):
        x = sign * r / 2
        matrix.append([evaluate(deriv({p: Q(1)}, dx, dz), x, 0) for p in PIVOTS])
        rhs.append(target - evaluate(deriv(dict(free), dx, dz), x, 0))
    coeffs = solve([row + [y] for row, y in zip(matrix, rhs)])
    poly = {p: Q(c) for p, c in free.items()}
    poly.update(zip(PIVOTS, coeffs))
    return {p: c for p, c in poly.items() if c}


def triangle_ceiling(poly, radius):
    radius = Q(radius)
    ceiling = Q(0)
    for order in range(7):
        for dx in range(order + 1):
            bound = sum(
                (abs(c) * radius ** (i + j) for (i, j), c in deriv(poly, dx, order - dx).items()),
                Q(0),
            )
            if bound > ceiling:
                ceiling = bound
    return ceiling


def hermite_closed(r, gm, gxm, gp, gxp, hm, hp):
    values = [Q(v) for v in (gm, gxm, gp, gxp, hm, hp)]
    gm, gxm, gp, gxp, hm, hp = values
    a = Q(r) / 2
    s0 = (gm + gp) / 2
    d0 = (gp - gm) / (2 * a)
    s1 = (gxm + gxp) / 2
    d1 = (gxp - gxm) / (2 * a)
    return (
        s0 - a * a * d1 / 2,
        (3 * d0 - s1) / 2,
        d1,
        3 * (s1 - d0) / (a * a),
        (hm + hp) / 2,
        (hp - hm) / (2 * a),
    )


def hermite_solved(r, gm, gxm, gp, gxp, hm, hp):
    gm, gxm, gp, gxp, hm, hp = (Q(v) for v in (gm, gxm, gp, gxp, hm, hp))
    a = Q(r) / 2
    rows = [
        [1, a, a * a / 2, a**3 / 6, gp],
        [1, -a, a * a / 2, -(a**3) / 6, gm],
        [0, 1, a, a * a / 2, gxp],
        [0, 1, -a, a * a / 2, gxm],
    ]
    p, q, s, t = solve(rows)
    return (p, q, s, t, (hm + hp) / 2, (hp - hm) / (2 * a))


def alpha(u):
    return u * (u * u - Q(1, 4)) / 6


def beta(u):
    return (u * u - Q(1, 4)) / 2


def monomial_Y(r, u, w, i, j):
    a = r / 2

    def value(x):
        return Q(x) ** i if j == 0 else Q(0)

    def grad(x, z):
        gx = i * Q(x) ** (i - 1) * Q(z) ** j if i else Q(0)
        gz = j * Q(x) ** i * Q(z) ** (j - 1) if j else Q(0)
        return gx, gz

    gm, gp = grad(-a, 0), grad(a, 0)
    jet = hermite_closed(r, value(-a), gm[0], value(a), gp[0], gm[1], gp[1])
    x = r * u
    h_prime = jet[1] + jet[2] * x + jet[3] * x * x / 2
    linear = jet[4] + jet[5] * x
    gx, gz = grad(x, r * r * w)
    return (gx - h_prime - r * r * w * jet[5]) / r**3, (gz - linear) / r**2


def extrapolate_limit(i, j, u, w, order=10):
    step = Q(1, 17)
    samples = [monomial_Y(n * step, u, w, i, j) for n in range(1, order + 1)]
    total = [Q(0), Q(0)]
    for n in range(1, order + 1):
        weight = Q(1)
        for m in range(1, order + 1):
            if m != n:
                weight *= Q(m, m - n)
        total[0] += weight * samples[n - 1][0]
        total[1] += weight * samples[n - 1][1]
    return tuple(total)


def expected_limit(i, j, u, w):
    quartic = Q(24 if (i, j) == (4, 0) else 0)
    mixed = Q(2 if (i, j) == (2, 1) else 0)
    transverse = Q(2 if (i, j) == (0, 2) else 0)
    return alpha(u) * quartic + u * w * mixed, beta(u) * mixed + w * transverse


def interface_ratios(poly, r, box, ceiling, k=Q(1), b=Q(2)):
    r, box, ceiling = Q(r), Q(box), Q(ceiling)

    def jet(dx, dz, x=0, z=0):
        return evaluate(deriv(poly, dx, dz), x, z)

    ratios = {}

    def keep(name, error, bound):
        ratio = abs(error) / bound
        if name not in ratios or ratio > ratios[name]:
            ratios[name] = ratio

    keep("M1", jet(1, 0) + r * r * jet(3, 0) / 8, ceiling * r**4 / 384)
    keep("M2", jet(2, 0) + r * r * jet(4, 0) / 24, ceiling * r**4 / 1920)
    keep("M3", jet(3, 0) - 12 * k, Q(3, 80) * ceiling * r * r)
    keep("M4", jet(0, 0) - b + k * r**3 / 2, Q(121, 15360) * ceiling * r**4)
    keep("M5", jet(1, 0) / r**2 + Q(3, 2) * k, Q(7, 960) * ceiling * r * r)
    keep("M6", jet(0, 1) + r * r * jet(2, 1) / 8, ceiling * r**4 / 384)
    keep("M7", jet(1, 1) + r * r * jet(3, 1) / 24, ceiling * r**4 / 1920)
    cx = Q(7, 960) + Q(27, 320) * box + Q(3, 160) * box**2 + Q(4, 3) * box**3
    cy = Q(49, 384) + Q(27, 640) * box + 2 * box**2
    ca = Q(1, 384) + Q(27, 640) * box + box**3 / 6
    ch = (
        Q(121, 15360)
        + Q(19, 1920) * box
        + Q(81, 1280) * box**2
        + box**3 / 160
        + Q(2, 3) * box**4
    )
    us = (Q(0), Q(1, 2), Q(1), Q(3, 2), Q(2), box, -box, -Q(1))
    vs = (Q(0), Q(1, 2), box, -box, -Q(1, 3), Q(1))
    for u in us:
        for v in vs:
            if abs(u) > box or abs(v) > box:
                continue
            x, z = r * u, r * v
            fx, fz, value = jet(1, 0, x, z), jet(0, 1, x, z), jet(0, 0, x, z)
            q, c, d, a = jet(2, 1), jet(1, 2), jet(0, 3), jet(0, 2)
            px = 6 * k * (u * u - Q(1, 4)) + q * u * v + c * v * v / 2
            height = (
                k * (2 * u**3 - Q(3, 2) * u - Q(1, 2))
                + q * (u * u - Q(1, 4)) * v / 2
                + c * u * v * v / 2
                + d * v**3 / 6
            )
            keep("S1", fx / r**2 - px, cx * ceiling * r)
            keep("S2", fz / r - a * v, cy * ceiling * r)
            keep("S4", (value - b) / r**2 - a * v * v / 2 - r * height, ch * ceiling * r * r)
            if v == 0:
                keep("S3", fz / r**2 - q * (u * u - Q(1, 4)) / 2, ca * ceiling * r)
    return ratios


def main():
    assert Q(3, 640) + Q(1, 384) == Q(7, 960)
    assert Q(1, 24) + Q(1, 1920) == Q(27, 640)
    assert Q(121, 960) / 16 == Q(121, 15360)
    assert Q(7, 960) + Q(1, 384) == Q(19, 1920)
    assert Q(27, 1280) + Q(27, 640) == Q(81, 1280)

    sample = (Q(2, 5), Q(3), Q(-1), Q(7), Q(4), Q(-2), Q(8))
    assert hermite_closed(*sample) == hermite_solved(*sample)

    r, b, k = Q(1, 6), Q(3), Q(4)
    spec = hermite_closed(r, b, 0, b - k * r**3, 0, 0, 0)
    assert spec == (b - k * r**3 / 2, -Q(3, 2) * k * r * r, 0, 12 * k, 0, 0)
    a = r / 2
    s0 = (b + (b - k * r**3)) / 2
    d0 = ((b - k * r**3) - b) / (2 * a)
    v3 = 3 * (0 - d0) / (a * a)
    assert spec[0] == s0 - r * r * 0 / 8
    assert spec[1] == d0 - r * r * v3 / 24

    for u in (Q(-3), Q(3, 2), Q(-5, 2)):
        assert alpha(u) * beta(u) == u * (u * u - Q(1, 4)) ** 2 / 12
        assert alpha(u) * beta(u) != 0
    assert Q(2, 7) ** 5 == Q(2, 7) ** 3 * Q(2, 7) ** 2

    quartic = pin_polynomial(Q(1, 7), {(4, 0): Q(1)})
    base = pin_polynomial(Q(1, 7), {})
    increment = evaluate(deriv(quartic, 1, 0), Q(2, 7), 0) - evaluate(deriv(base, 1, 0), Q(2, 7), 0)
    assert increment / Q(1, 7) ** 2 == 30 * Q(1, 7)

    sharp = pin_polynomial(1, {(5, 0): Q(1), (0, 2): Q(-1)})
    sharp_m = triangle_ceiling(sharp, 1)
    sharp_err = abs(evaluate(deriv(sharp, 1, 0), 0, 0) + evaluate(deriv(sharp, 3, 0), 0, 0) / 8)
    assert sharp_m == 120
    assert sharp_err == sharp_m / 384

    free_sets = []
    for order in range(7):
        for i in range(order + 1):
            j = order - i
            if (i, j) not in PIVOTS:
                free_sets.append({(i, j): Q(1), (0, 2): Q(-1)})
    free_sets.append(
        {
            (i, j): Q(((-1) ** (i + j)) * (1 + i), 3 + j)
            for order in range(7)
            for i in range(order + 1)
            for j in (order - i,)
            if (i, j) not in PIVOTS
        }
    )
    free_sets.append(
        {(4, 0): Q(1), (5, 0): Q(-2), (3, 2): Q(3), (0, 6): Q(1), (6, 0): Q(-1), (2, 3): Q(4)}
    )
    worst = {}
    cases = 0
    for radius in (Q(1), Q(4, 5), Q(1, 2), Q(1, 5), Q(1, 31)):
        for box in (Q(1), Q(2), Q(3)):
            for free in free_sets:
                poly = pin_polynomial(radius, free)
                for sign in (-1, 1):
                    height = 2 if sign < 0 else 2 - radius**3
                    assert evaluate(poly, sign * radius / 2, 0) == height
                    assert evaluate(deriv(poly, 1, 0), sign * radius / 2, 0) == 0
                    assert evaluate(deriv(poly, 0, 1), sign * radius / 2, 0) == 0
                ratios = interface_ratios(poly, radius, box, triangle_ceiling(poly, box * radius))
                cases += 1
                for name, ratio in ratios.items():
                    assert ratio <= 1, (name, ratio, radius, box)
                    if name not in worst or ratio > worst[name]:
                        worst[name] = ratio

    for i in range(7):
        for j in range(7 - i):
            for u in (Q(-2), Q(5, 3)):
                for w in (Q(0), Q(2, 3)):
                    assert extrapolate_limit(i, j, u, w) == expected_limit(i, j, u, w), (i, j, u, w)

    bare = monomial_Y(Q(1, 100), Q(2), Q(3), 1, 1)
    assert bare == (0, 0)
    # Rebuild the xz monomial without the L' subtraction.
    r, u, w = Q(1, 100), Q(2), Q(3)
    gx = r * r * w
    assert gx / r**3 == w / r

    names = ("M1", "M2", "M3", "M4", "M5", "M6", "M7", "S1", "S2", "S3", "S4")
    summary = ", ".join(f"{name}={worst[name]}" for name in names)
    print(f"cases={cases} {summary}")
    print("interfaces hold")


if __name__ == "__main__":
    main()
