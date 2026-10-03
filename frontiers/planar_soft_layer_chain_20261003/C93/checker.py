#!/usr/bin/env python3
"""C93 nonauthor rational transcription controls; not a Gaussian proof.

Python standard library only. No author checker or inputs are used.
Run: python3 c93_independent_controls.py
"""
from fractions import Fraction as F
from math import comb

COUNTS = {}
NEGATIVE = []


def check(group, predicate):
    if not predicate:
        raise RuntimeError("positive control failed: " + group)
    COUNTS[group] = COUNTS.get(group, 0) + 1


def reject(name, false_claim):
    if false_claim:
        raise RuntimeError("negative fixture survived: " + name)
    NEGATIVE.append(name)


def det(h):
    return h[0] * h[2] - h[1] ** 2


def filtered(h, index):
    d = det(h)
    if d == 0:
        return F(0)
    actual = 1 if d < 0 else (2 if h[0] < 0 else 0)
    return abs(d) if actual == index else F(0)


def margins(lam, gamma, b):
    return 24 * lam - gamma ** 2 + 12 * b, 24 * lam + gamma ** 2 - 12 * b


grid = [F(-2), F(-1, 2), F(0), F(1, 3), F(1), F(3)]
for lam in grid:
    for gamma in grid:
        for b in grid:
            am, ass = margins(lam, gamma, b)
            hm = (F(-6), -gamma / 2, -lam - b / 2)
            hs = (F(6), gamma / 2, -lam + b / 2)
            expected = max(am, 0) * max(ass, 0) / 16
            check("weight_and_typing", filtered(hm, 2) * filtered(hs, 1) == expected)
            check("weight_and_typing", am + ass == 48 * lam)
            check("weight_and_typing", not (am > 0 and ass > 0) or lam > 0)

# Both substitutions, signed derivative and absolute Jacobian, including edges.
for lam in [F(1, 100), F(1, 4), F(1), F(2)]:
    for gamma in grid:
        for fraction in [F(0), F(1, 100), F(1, 4), F(1, 2), F(99, 100), F(1)]:
            s = 48 * lam * fraction
            for i in [0, 1]:
                b = (s - 24 * lam + gamma ** 2) / 12 if i == 0 else (24 * lam + gamma ** 2 - s) / 12
                pair = margins(lam, gamma, b)
                check("edge_change_of_variables", pair[i] == s and pair[1 - i] == 48 * lam - s)
                check("edge_change_of_variables", max(pair[0], 0) * max(pair[1], 0) / 16 == s * (48 * lam - s) / 16)
                ds = F(1, 7)
                next_b = (s + ds - 24 * lam + gamma ** 2) / 12 if i == 0 else (24 * lam + gamma ** 2 - s - ds) / 12
                check("edge_change_of_variables", abs((next_b - b) / ds) == F(1, 12))

# The multiplication precedes conditional moments; retain all four terms.
for p in range(5):
    for r in [F(1, 64), F(1, 5), F(1)]:
        for n in [F(1), F(3), F(17)]:
            for d in [F(1), F(5), F(11)]:
                direct = n ** p * r * n * (d + r * n) ** 3
                expanded = sum(F(comb(3, j)) * r ** (j + 1) * d ** (3 - j) * n ** (p + j + 1) for j in range(4))
                check("moment_product_expansion", direct == expanded)

# Exact polynomial norm domination supporting (not proving) Gaussian absorption.
for gamma in grid:
    for b in grid:
        for c3 in grid:
            pnorm = 1 + abs(gamma) + abs(b) + abs(c3)
            check("polynomial_domination", pnorm ** 2 <= 4 * (1 + gamma ** 2 + b ** 2 + c3 ** 2))

# Integrate the nonnegative edge skeleton analytically as rational polynomials.
for cap in [F(1, 4), F(1), F(4)]:
    for delta in [cap / 100, cap / 7, cap]:
        for r in [F(1, 64), F(1, 5)]:
            strip = delta ** 2 / 2 + r * delta
            check("strip_and_inverse_integrals", strip <= delta ** 2 + r * delta)
            for lam in [cap / 48, cap / 24]:
                upper = min(delta, 48 * lam)
                edge_weight_integral = (48 * lam * upper ** 2 / 2 - upper ** 3 / 3) / 16
                check("strip_and_inverse_integrals", 0 <= edge_weight_integral <= 48 * lam * upper ** 2 / 32)
            exact_v3 = 1 / delta - 1 / cap + r * (1 / delta ** 2 - 1 / cap ** 2) / 2
            check("strip_and_inverse_integrals", 0 <= exact_v3 <= 1 / delta + r / (2 * delta ** 2))
            epsilon = delta
            split = delta ** 2 + r * delta + epsilon ** 3 * (1 / delta + r / delta ** 2)
            check("strip_and_inverse_integrals", split == 2 * (epsilon ** 2 + r * epsilon))

# Threshold v=2: every dyadic shell contributes >=1/2 to integral ds/s.
# A finite total mass or an L1 rate cannot supply an inverse-moment bound.
for k in range(1, 21):
    lo, hi = F(1, 2 ** k), F(1, 2 ** (k - 1))
    check("inverse_threshold_shells", (hi - lo) / hi == F(1, 2))
    check("inverse_threshold_shells", 1 / lo - 1 / hi == 1 / (2 * lo))
    check("inverse_threshold_shells", (hi ** 2 - lo ** 2) / 2 > 0)

# Rationalized transformed directions: v=(sqrt(3)*x,y) has norm^2=3x^2+y^2.
# kappa=u^2 and a=48 gamma^2 u^2, so its raw image is rational.
for gamma in [F(-3), F(-1, 100), F(1, 1000), F(1, 2), F(2)]:
    for u in [F(1, 100), F(1, 3), F(1), F(5)]:
        a = 48 * gamma ** 2 * u ** 2
        frob = F(1, 3) + F(1, 144) / u ** 2 + 1 / (gamma ** 2 * u ** 2)
        loss = 1 + (gamma ** 2 + 144) / a
        check("hessian_transfer", frob == loss / 3)
        for x, y in [(F(0), F(1)), (F(1), F(0)), (F(1), F(1)), (F(-2), F(3))]:
            rx, rz = x - y / (12 * u), y / (gamma * u)
            length = 3 * x ** 2 + y ** 2
            for hxx in [F(-1), F(0), F(1)]:
                for hxz in [F(-1), F(1)]:
                    for hzz in [F(-1), F(0), F(1)]:
                        quadratic = hxx * rx ** 2 + 2 * hxz * rx * rz + hzz * rz ** 2
                        check("hessian_transfer", abs(quadratic) <= 2 * frob * length)
check("hessian_transfer", F(115, 48) * F(2, 3) == F(115, 72))

# Exact normalization and radius ledger; constants may depend on fixed p,beta.
for r in [F(1, 64), F(1, 8), F(1, 2)]:
    for z in [F(1, 3), F(2), F(7)]:
        mass = F(5, 7)
        check("normalization_and_exponents", r ** 4 * r * mass / (r ** 2 * z) == r ** 3 * mass / z)
for beta in [F(0), F(1, 20), F(1, 8), F(1, 5), F(6, 25), F(249, 1000)]:
    minimum = 1 / (1 - 4 * beta)
    for p in [minimum, minimum + 1, 2 * minimum]:
        check("normalization_and_exponents", 3 + p * (1 - 4 * beta) >= 4)
        check("normalization_and_exponents", 5 - 4 * beta >= 4)
        check("normalization_and_exponents", 1 - 2 * beta > 0 and 1 - beta > 0)

# Deliberately false claims. Each fixture must reject its named inference.
reject("missing_B1_jacobian", F(12, 12) == F(1, 12))
lam, gamma, s = F(1), F(2), F(7)
wrong_b = (s - 24 * lam + gamma ** 2) / 12
reject("reuse_M_substitution_for_S", margins(lam, gamma, wrong_b)[1] == s)
r, delta = F(1, 16), F(1, 4096)
reject("discard_actual_r_delta", delta ** 2 / 2 + r * delta <= 2 * delta ** 2)
# With the same fixed r, the dyadic lower bound grows without limit.
reject("L1_implies_actual_inverse_integrability", 100 * r / 2 <= r)
reject("model_second_inverse_is_finite", F(100, 2) <= 1)
# A second-moment split contributes epsilon^2 * int_delta^1 ds/s.
reject("second_moment_gives_uniform_log_free_split", F(100, 2) <= 2)
# E[D N] differs from E[D]E[N] for the correlated two-atom example (1,1),(3,3).
reject("factor_conditional_weight_and_norm", F(1 + 9, 2) == F(1 + 3, 2) ** 2)
reject("omit_full_r2_normalizer", F(1, 8) ** 5 == F(1, 8) ** 3)
reject("omit_typing_denominator", 1 + (F(1) + 144) / F(1, 100) <= 1 + F(1) + 144)
reject("allow_beta_one_quarter", 3 + 100 * (1 - 4 * F(1, 4)) >= 4)
reject("underpowered_fixed_moment", 3 + 4 * (1 - 4 * F(1, 5)) >= 4)
reject("arbitrary_random_budget_is_covered", F(115, 72) * F(1, 100) / F(1, 100) ** 2 <= 1)
try:
    F(1) / F(0)
except ZeroDivisionError:
    NEGATIVE.append("gamma_zero_is_not_a_chart")
else:
    raise RuntimeError("negative fixture survived: gamma_zero_is_not_a_chart")

print("C93 independent rational controls")
for name in sorted(COUNTS):
    print(name + ": " + str(COUNTS[name]))
print("positive_total: " + str(sum(COUNTS.values())))
print("negative_fixtures_rejected: " + str(len(NEGATIVE)))
print("negative_names: " + ", ".join(NEGATIVE))
print("PASS transcription/scaling controls only; analytic Gaussian inputs reviewed separately.")
