#!/usr/bin/env python3
"""C124 finite exact arithmetic controls; no analytic or formal-proof claim.

No arguments: baseline (exit 0 on success). --mutant NAME: deliberately
incorrect candidate (exit 1 if rejected). Invalid arguments exit 2.
Only the Python standard library is used; no files or network are accessed.
"""

from fractions import Fraction as F
from math import comb, factorial, prod
import json
import sys


MUTANTS = (
    "WINDOW_H_OMITTED",
    "BAND_P_ONE",
    "DROP_BAND_FLOOR",
    "UNWEIGHTED_PROMOTION",
    "INDEPENDENT_COEFFICIENTS",
    "EXP_SCALE_TOO_LARGE",
    "DROP_SOFT_FACTOR",
    "DOUBLE_NORMALIZER",
    "DROP_SCALED_FAR",
    "GAUSSIAN_LAMBDA_SQUARED",
)


class Checks:
    def __init__(self):
        self.groups = {}
        self.failures = []

    def check(self, group, label, condition):
        counts = self.groups.setdefault(group, {"checks": 0, "failures": 0})
        counts["checks"] += 1
        if not condition:
            counts["failures"] += 1
            if len(self.failures) < 16:
                self.failures.append({"group": group, "label": label})

    def equal(self, group, label, got, want):
        self.check(group, label, got == want)

    def result(self, mutant):
        checks = sum(v["checks"] for v in self.groups.values())
        failures = sum(v["failures"] for v in self.groups.values())
        return {
            "object": "C124-EXACT-CONTROLS-v1",
            "candidate": mutant or "BASELINE",
            "passed": failures == 0,
            "checks": checks,
            "failure_count": failures,
            "failures_first_16": self.failures,
            "groups": self.groups,
            "scope": "finite rational controls; not analytic proof or source verification",
        }


def ledger(c, mutant):
    g = "G1_schedule_and_admissibility"
    # w=(r H^4)^(-1/12), retaining both exact powers.
    schedule = (F(-1, 12), F(-1, 3))
    if mutant == "WINDOW_H_OMITTED":
        schedule = (F(-1, 12), F(0))

    def substitute(r, h, w):
        return (F(r) + F(w) * schedule[0], F(h) + F(w) * schedule[1])

    # Input monomials (r,H,w) and independently hand-derived expected pairs.
    cases = (
        ("radius", (0, 0, -8), (F(2, 3), F(8, 3))),
        ("radius_actual", (1, 3, -4), (F(4, 3), F(13, 3))),
        ("selected_edge", (1, 4, 4), (F(2, 3), F(8, 3))),
        ("selected_edge_actual", (F(3, 2), 5, 2), (F(4, 3), F(13, 3))),
        ("endpoint", (1, 3, 2), (F(5, 6), F(7, 3))),
        ("endpoint_actual", (F(3, 2), 4, 1), (F(17, 12), F(11, 3))),
        ("joint_band", (1, 0, 4), (F(2, 3), F(-4, 3))),
        ("actual_band_floor", (1, 4, 0), (F(1), F(4))),
        ("large_N", (2, 3, 8), (F(4, 3), F(1, 3))),
        ("hessian_first", (2, 5, 4), (F(5, 3), F(11, 3))),
        ("hessian_second", (2, 7, 2), (F(11, 6), F(19, 3))),
        ("far_derivative", (1, 0, 0), (F(1), F(0))),
    )
    target = (F(2, 3), F(8, 3))
    values = {}
    for label, powers, want in cases:
        got = substitute(*powers)
        values[label] = got
        c.equal(g, label + ":exact_pair", got, want)
        c.check(g, label + ":log_dominance",
                got[0] > target[0] or
                (got[0] == target[0] and got[1] <= target[1]))
    c.equal(g, "balanced_leading_terms", values["radius"], values["selected_edge"])
    c.equal(g, "leading_target", values["radius"], target)
    for label, powers, want in (
        ("rH", (1, 1, 0), (F(1), F(1))),
        ("rw", (1, 0, 1), (F(11, 12), F(-1, 3))),
        ("e", (1, 0, 4), (F(2, 3), F(-4, 3))),
        ("H2e", (1, 2, 4), (F(2, 3), F(2, 3))),
        ("eta", (1, 0, 2), (F(5, 6), F(-2, 3))),
    ):
        got = substitute(*powers)
        c.equal(g, label + ":exact_admissibility", got, want)
        c.check(g, label + ":vanishes", got[0] > 0)
    c.check(g, "window_grows", schedule[0] < 0)
    # Fixed-Lambda schedule w=r^-1/12: H powers become constants.
    for label, powers, _ in cases:
        r, _, w = powers
        c.check(g, label + ":fixed_layer_at_least_two_thirds",
                F(r) - F(w, 12) >= F(2, 3))


def dyadic(c, mutant):
    g = "G2_joint_band_dyadic_sums"
    p = 1 if mutant == "BAND_P_ONE" else 2
    for m in range(2, 33):
        for scale in (F(1), F(3, 4), F(5, 7)):
            a = scale / 2**m
            b = F(3, 17)
            endpoint = 2 * a
            last = 0
            while 2 * endpoint <= F(1, 2):
                last += 1
                endpoint *= 2
            c.check(g, f"m{m}:{scale}:stopping_interval",
                    F(1, 4) < endpoint <= F(1, 2))
            shell_a = sum((2 * a * F(2) ** ((1 - p) * j)
                           for j in range(last + 1)), F(0))
            shell_b = sum((b * F(2) ** (-p * j)
                           for j in range(last + 1)), F(0))
            c.equal(g, f"m{m}:{scale}:linear_geometric_sum", shell_a,
                    4 * a * (1 - F(1, 2) ** (last + 1)))
            c.equal(g, f"m{m}:{scale}:floor_geometric_sum", shell_b,
                    F(4, 3) * b * (1 - F(1, 4) ** (last + 1)))
            c.check(g, f"m{m}:{scale}:uniform_shell_bound",
                    shell_a + shell_b <= 4 * a + F(4, 3) * b)
            c.check(g, f"m{m}:{scale}:large_N_threshold",
                    endpoint / a > 1 / (4 * a))
            c.check(g, f"m{m}:{scale}:tail_markov_coefficient",
                    (a / endpoint)**2 < 16 * a**2)
            c.check(g, f"m{m}:{scale}:combined_low_and_shells",
                    a + b + shell_a + shell_b <= 5 * a + F(7, 3) * b)
    # Abstract continuous band fixture: measure of total mass B, N=1,
    # uniform in mu on (0,delta]. It obeys mass{|mu|<=s} <= s+B for
    # every s>0, with no atom at the neutral level. It is not asserted
    # to be a realizable pinned Gaussian field. The bound alone cannot
    # discard B; choosing delta=B/2^m defeats a delta-only unit bound.
    for m in range(1, 33):
        b = F(1, 64)
        delta = b / 2**m
        offered = delta if mutant == "DROP_BAND_FLOOR" else delta + b
        c.check(g, f"continuous:m{m}:retain_band_error_floor", b <= offered)


def counterexample(c, mutant):
    g = "G3_unweighted_band_counterexample"
    # The geometric-distribution recurrence is compared with literal moments.
    moments = [1]
    for p in range(1, 9):
        moments.append(2 + sum(comb(p, j) * moments[j] for j in range(1, p)))
    c.equal(g, "geometric_moments_zero_through_eight", moments,
            [1, 2, 6, 26, 150, 1082, 9366, 94586, 1091670])
    for p in range(9):
        partial = sum((F(n**p, 2**n) for n in range(1, 129)), F(0))
        c.check(g, f"p{p}:partial_moment_below_exact", partial <= moments[p])
    for m in range(2, 65):
        delta = F(1, 2**m)
        e = delta / m
        c.equal(g, f"m{m}:event_lower_bound_over_e", delta / e, F(m))
        c.check(g, f"m{m}:event_containment_at_right_endpoint", delta <= e * m)
        # Exact partition into U-intervals with N=m+j, including the tail.
        finite = sum((F((m + j)**2, 2**(m + j)) for j in range(1, 17)), F(0))
        tail = F((m + 16)**2 + 4 * (m + 16) + 6, 2**(m + 16))
        joint = delta * (m*m + 4*m + 6)
        c.equal(g, f"m{m}:joint_second_moment", finite + tail, joint)
        c.equal(g, f"m{m}:joint_band_ratio", joint / delta, F(m*m + 4*m + 6))
        proposed_bound = 8 * e if mutant == "UNWEIGHTED_PROMOTION" else delta
        c.check(g, f"m{m}:unweighted_Oe_claim_not_inferred", delta <= proposed_bound)


def gaussian(c, mutant):
    g = "G4_correlated_gaussian_and_exp_square"
    for index, weights in enumerate(((F(1), F(1)), (F(1, 3), F(2, 3)),
                                     (F(2), F(3), F(5)),
                                     (F(1, 2), F(1, 3), F(1, 7)))):
        s = sum(weights)
        variance = sum(a*a for a in weights) if mutant == "INDEPENDENT_COEFFICIENTS" else s*s
        c.equal(g, f"fixture{index}:fully_correlated_variance", variance, s*s)
        c.check(g, f"fixture{index}:quadrature_is_too_small", sum(a*a for a in weights) < s*s)
        for m in range(1, 17):
            normal_moment = prod(range(1, 2*m, 2))
            candidate_moment = variance**m * normal_moment
            c.equal(g, f"fixture{index}:m{m}:actual_even_moment",
                    candidate_moment, s**(2*m) * normal_moment)
            c.check(g, f"fixture{index}:m{m}:Minkowski_majorant",
                    s**(2*m) * normal_moment <= s**(2*m) * (2*m)**m)
    # Rational coefficient check: if ||J||_p <= C sqrt(p), use
    # epsilon=1/(12 C^2), m! >= (m/3)^m, and sum 2^-m=2.
    # The assumed moment inequality and infinite-series step are analytic.
    for const in (F(1), F(3, 2), F(4), F(17, 3)):
        epsilon = 1 / (const*const * (1 if mutant == "EXP_SCALE_TOO_LARGE" else 12))
        for m in range(1, 49):
            c.check(g, f"C{const}:m{m}:factorial_majorant", m**m <= 3**m * factorial(m))
            coefficient = epsilon**m * const**(2*m) * (2*m)**m / factorial(m)
            c.check(g, f"C{const}:m{m}:geometric_exp_coefficient", coefficient <= F(1, 2**m))
    for m in range(1, 25):
        c.equal(g, f"exp_partial{m}", sum((F(1, 2**j) for j in range(m + 1)), F(0)),
                2 - F(1, 2**m))


def rare_scalar(c, mutant):
    g = "G5_rare_scalar_and_full_normalization"
    for r in (F(1, 2), F(1, 7), F(1, 64), F(3, 100)):
        for j in (F(1), F(3, 2), F(4)):
            for d, s in ((F(1), F(1)), (F(2), F(3, 4)), (F(1, 3), F(5))):
                top = d * r * j*j
                integral = top*top / 2 if mutant == "DROP_SOFT_FACTOR" else top**3/3 + s*r*j*j*top*top/2
                numerator = r*r*j**4 * integral
                coefficient = d**3/3 + s*d*d/2
                want = r**5*j**10*coefficient
                label = f"r{r}:J{j}:D{d}:C{s}"
                c.equal(g, label + ":scalar_integral", numerator, want)
                z = F(5, 3) * r*r
                normalized = numerator / (z*z if mutant == "DOUBLE_NORMALIZER" else z)
                c.equal(g, label + ":probability_scaling", normalized,
                        r**3*j**10*coefficient/F(5, 3))
                c.equal(g, label + ":scaled_measure", normalized/r**3,
                        j**10*coefficient/F(5, 3))
    # The documented input is E[(W/r^2) 1_exception] <= C r^4.
    c.equal(g, "near_radius_exponents", 5 - 2 - 3, 0)
    c.equal(g, "far_numerator_radius_exponent", 2 + 4, 6)
    far = F(0) if mutant == "DROP_SCALED_FAR" else F(1, 8)
    c.check(g, "retain_permitted_far_mass", F(1, 8) <= far)
    c.equal(g, "far_scaled_radius_exponent", 2 + 4 - 2 - 3, 1)


def exponential_tail(c, mutant):
    g = "G6_exponential_tail_threshold"
    for lam in (F(1), F(4), F(9), F(25), F(64), F(100)):
        for const in (F(1), F(4), F(9)):
            threshold_squared = lam*lam/const if mutant == "GAUSSIAN_LAMBDA_SQUARED" else lam/const
            c.equal(g, f"Lambda{lam}:C{const}:threshold_square", threshold_squared, lam/const)
    c.equal(g, "square_of_square_root_degree", F(1, 2)*2, 1)
    for decay in (F(1, 10), F(1, 3), F(1), F(7, 2)):
        D = F(2, 3)/decay
        c.equal(g, f"c{decay}:minimum_log_cutoff", decay*D, F(2, 3))
        c.check(g, f"c{decay}:larger_log_cutoff", decay*(D + 1) > F(2, 3))


def main(argv):
    if argv == ["--list-mutants"]:
        print(json.dumps(list(MUTANTS), separators=(",", ":")))
        return 0
    mutant = None
    if argv:
        if len(argv) != 2 or argv[0] != "--mutant" or argv[1] not in MUTANTS:
            print(json.dumps({"error": "expected no arguments, --list-mutants, or --mutant NAME",
                              "passed": False}, sort_keys=True, separators=(",", ":")))
            return 2
        mutant = argv[1]
    checks = Checks()
    for group in (ledger, dyadic, counterexample, gaussian, rare_scalar, exponential_tail):
        group(checks, mutant)
    result = checks.result(mutant)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
