"""Rational certificates for the P15 full-price analytic review.

Subject: frontiers/full_price_20260924/PROOF.md
blob 582180e41dca0ad815ad0f18574df42040912149,
SHA256 87521901ca8e5405b4d1e47f1deb1cd0326affbd6f5967b53c4178590da993f9.

Python standard library only. This file does not import the author package.
A passing run checks algebraic identities and rational enclosures used by
the six-slice review. It does not replace the continuum argument in PROOF.md.
"""

from fractions import Fraction as Q
from math import comb


def fail(message):
    raise SystemExit(message)


def poly_mul(left, right):
    out = [Q(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return out


def poly_pow(base, exponent):
    out = [Q(1)]
    for _ in range(exponent):
        out = poly_mul(out, base)
    return out


def poly_scale(poly, scalar):
    return [scalar * coeff for coeff in poly]


def poly_eq(left, right):
    width = max(len(left), len(right))
    left = left + [Q(0)] * (width - len(left))
    right = right + [Q(0)] * (width - len(right))
    return left == right


def exp_series_upper(n_terms):
    """Return sum_{k=0}^{n} 1/k! + 1/(n! n), with n = n_terms."""
    total = Q(0)
    fact = 1
    for k in range(n_terms + 1):
        if k:
            fact *= k
        total += Q(1, fact)
    return total + Q(1, fact * n_terms)


def exp_bounds(n_terms):
    total = Q(0)
    fact = 1
    for k in range(n_terms + 1):
        if k:
            fact *= k
        total += Q(1, fact)
    return total, total + Q(1, fact * n_terms)


def log_series_bounds(x_lo, x_hi, terms):
    """Enclose log on an interval inside [1, 2]."""
    if not (Q(1) <= x_lo <= x_hi <= Q(2)):
        fail("logarithm reduction left [1, 2]")

    def lower(x):
        t = (x - 1) / (x + 1)
        total = Q(0)
        power = t
        for j in range(terms):
            total += power / (2 * j + 1)
            power *= t * t
        return 2 * total

    def upper(x):
        t = (x - 1) / (x + 1)
        total = Q(0)
        power = t
        for j in range(terms):
            total += power / (2 * j + 1)
            power *= t * t
        remainder = 2 * power / ((2 * terms + 1) * (1 - t * t))
        return 2 * total + remainder

    return lower(x_lo), upper(x_hi)


def rho_enclosure(exp_terms, log_terms):
    e_lo, e_hi = exp_bounds(exp_terms)
    log2_lo, log2_hi = log_series_bounds(Q(2), Q(2), log_terms)
    y_lo = (3 * e_lo - 2) / 4
    y_hi = (3 * e_hi - 2) / 4
    logy_lo, logy_hi = log_series_bounds(y_lo, y_hi, log_terms)
    h_lo = 3 - (2 * log2_hi + logy_hi)
    h_hi = 3 - (2 * log2_lo + logy_lo)
    return 1 / h_hi, 1 / h_lo


def f10_polynomials(a):
    """Unnormalized (F10) difference and target, as polynomials in p."""
    n = 2 * a + 1
    one_minus = [Q(1), Q(-1)]
    p_poly = [Q(0), Q(1)]
    first = poly_scale(
        poly_mul(
            poly_pow(one_minus, 2),
            poly_mul(
                poly_pow(p_poly, a + 1),
                poly_pow(one_minus, n - (a + 1)),
            ),
        ),
        Q(comb(n, a + 1)),
    )
    second = poly_scale(
        poly_mul(
            poly_pow(p_poly, 2),
            poly_mul(poly_pow(p_poly, a), poly_pow(one_minus, n - a)),
        ),
        Q(comb(n, a)),
    )
    width = max(len(first), len(second))
    left = first + [Q(0)] * (width - len(first))
    second = second + [Q(0)] * (width - len(second))
    left = [x - y for x, y in zip(left, second)]
    right = poly_scale(
        poly_mul(
            poly_mul([Q(0), Q(1), Q(-2)], poly_pow(p_poly, a)),
            poly_pow(one_minus, n - a),
        ),
        Q(comb(n, a)),
    )
    return left, right


def evaluate(poly, value):
    total = Q(0)
    power = Q(1)
    for coeff in poly:
        total += coeff * power
        power *= value
    return total


def monomial_mul(left, right):
    out = {}
    for (i, j, k), coeff in left.items():
        for (i2, j2, k2), other in right.items():
            key = (i + i2, j + j2, k + k2)
            out[key] = out.get(key, Q(0)) + coeff * other
    return {key: coeff for key, coeff in out.items() if coeff}


def monomial_add(left, right, scale=Q(1)):
    out = dict(left)
    for key, coeff in right.items():
        out[key] = out.get(key, Q(0)) + scale * coeff
    return {key: coeff for key, coeff in out.items() if coeff}


def main():
    # d/dt [B u / (A + B u)] with u = exp(-t), so u' = -u.
    # The numerator of that derivative is (-B u)(A + B u) - (B u)(-B u).
    A = {(1, 0, 0): Q(1)}
    B = {(0, 1, 0): Q(1)}
    u = {(0, 0, 1): Q(1)}
    Bu = monomial_mul(B, u)
    den = monomial_add(A, Bu)
    cross = monomial_add(
        monomial_mul({(0, 0, 0): Q(-1)}, monomial_mul(Bu, den)),
        monomial_mul(Bu, Bu),
    )
    target = {(1, 1, 1): Q(-1)}
    if cross != target:
        fail("separate second-derivative numerator")
    print("F5 cross-difference numerator -A B exp(-t)")

    for a in range(0, 21):
        n = 2 * a + 1
        if comb(n, a) != comb(n, a + 1):
            fail("odd binomial symmetry")
        left, right = f10_polynomials(a)
        if not poly_eq(left, right):
            fail(f"F10 polynomial identity at a={a}")
        for value, sign in (
            (Q(1, 2), 0),
            (Q(1), 0),
            (Q(3, 5), -1),
            (Q(4, 5), -1),
            (Q(2, 5), 1),
        ):
            got = evaluate(left, value)
            if sign == 0 and got != 0:
                fail(f"F10 endpoint a={a} p={value}")
            if sign < 0 and not got < 0:
                fail(f"F10 interior negativity a={a} p={value}")
            if sign > 0 and not got > 0:
                fail(f"F10 below one half a={a} p={value}")
    print("F10 identity and sign: zero at 1/2 and 1, negative on (1/2, 1)")

    # One added trial does not raise a fixed threshold.
    # P(Bin(n+1)<=a) - P(Bin(n)<=a) = -p P(Bin(n)=a).
    for n, a, p in ((3, 1, Q(3, 5)), (5, 2, Q(2, 3)), (4, 1, Q(4, 5))):
        def bin_cdf(trials, threshold):
            total = Q(0)
            for k in range(threshold + 1):
                total += Q(comb(trials, k)) * p**k * (1 - p) ** (trials - k)
            return total

        def bin_pmf(trials, k):
            return Q(comb(trials, k)) * p**k * (1 - p) ** (trials - k)

        gap = bin_cdf(n + 1, a) - bin_cdf(n, a)
        if gap != -p * bin_pmf(n, a) or not gap < 0:
            fail("trial-augmentation identity")
    print("fixed-threshold augmentation decreases the good probability")

    upper7 = exp_series_upper(7)
    if upper7 != Q(31967, 11760):
        fail("degree-7 exponential upper bound")
    if not (upper7 < Q(87, 32)):
        fail("31967/11760 < 87/32")
    if Q(87, 32) - upper7 != Q(11, 23520):
        fail("exponential gap 11/23520")
    e_lo, e_hi = exp_bounds(40)
    if not (Q(2) < e_lo < e_hi < upper7):
        fail("e enclosure")
    partial = Q(0)
    fact = 1
    base = Q(11, 6)
    for j in range(6):
        if j:
            fact *= j
        partial += base**j / fact
    if partial - Q(197, 32) != Q(26081, 933120):
        fail("degree-5 Taylor gap")
    if not (3 * Q(87, 32) - 2 == Q(197, 32) < partial):
        fail("3e-2 < 197/32 < exp(11/6)")
    if not (Q(7, 6) > 0 and Q(1) / (Q(7, 6)) == Q(6, 7)):
        fail("reciprocal of 7/6")
    print("e < 31967/11760 < 87/32 and rho_star < 6/7")

    # h_star > 1 because e > 2 rearranges to (e-1)(e-2) > 0.
    if not ((e_lo - 1) * (e_lo - 2) > 0):
        fail("h_star > 1")
    p_lo = 1 - 1 / e_lo
    p_hi = 1 - 1 / e_hi
    # e_lo < e < e_hi implies 1-1/e_lo < 1-1/e < 1-1/e_hi.
    if not (Q(1, 2) < p_lo < p_hi < 1):
        fail("p_star is not interior to (1/2, 1)")
    print("p_star = 1-exp(-1) lies in (1/2, 1)")

    claimed_lo = Q(84547981724898672067, 10**20)
    claimed_hi = Q(84547981724898672068, 10**20)
    rho_lo, rho_hi = rho_enclosure(40, 80)
    if not (claimed_lo < rho_lo <= rho_hi < claimed_hi):
        fail("F3 decimal enclosure")
    if not (rho_hi < Q(6, 7)):
        fail("decimal upper bound exceeds 6/7")
    print("F3 20-decimal enclosure of rho_star holds")

    # Demand one, a=1: hazard 2-log(2e-1) < 1 iff e > 1.
    if not (e_lo > 1):
        fail("demand-one hazard comparison")
    print("demand-one reference hazard is strictly less than one")
    print("all certificates passed")


if __name__ == "__main__":
    main()
