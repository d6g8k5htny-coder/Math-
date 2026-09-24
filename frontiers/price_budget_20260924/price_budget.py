"""Exact sufficient local budgets for the realized P15 family. No float/log calls.
A refusal is NOT a proof of infeasibility. Analytical premises are in PROOF.md.
"""
from __future__ import annotations
from fractions import Fraction as Q
from collections.abc import Sequence
import json
import math

LOW_PROBABILITY = Q(1, 4)
BUDGET_FACTOR = Q(16, 27)


def probability(x: Q | int) -> Q:
    if isinstance(x, bool) or not isinstance(x, (int, Q)):
        raise TypeError("exact integer/Fraction probability required")
    x = Q(x)
    if not 0 <= x <= 1:
        raise ValueError("probability outside [0,1]")
    return x


def positive_integer(x: int) -> int:
    if type(x) is not int or x < 1:
        raise ValueError("positive integer required")
    return x


def inputs(values: Sequence[Q | int], capacity: int, demand: int) -> tuple[Q, ...]:
    a, d = positive_integer(capacity), positive_integer(demand)
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        raise TypeError("a finite probability sequence is required")
    n = len(values)
    if n != a * d + 1:
        raise ValueError("actual block size must equal capacity*demand+1")
    if n > 4096 or n * (a + 1) > 1_000_000:
        raise ValueError("declared exact-computation limit exceeded")
    return tuple(probability(p) for p in values)


def phi_upper(p: Q | int) -> Q:
    """min(1,p/(1-p)) >= min(1,-log(1-p)); endpoint p=1 is one."""
    p = probability(p)
    return Q(1) if p == 1 else min(Q(1), p / (1 - p))


def tail_probability(values: Sequence[Q | int], capacity: int) -> Q:
    """Exact Poisson-binomial P(number selected > capacity), no subset enumeration."""
    a = positive_integer(capacity)
    ps = tuple(probability(p) for p in values)
    if not ps or len(ps) > 4096 or len(ps) * (a + 1) > 1_000_000:
        raise ValueError("empty or oversized exact problem")
    if a >= len(ps):
        return Q(0)
    row = [Q(1)] + [Q(0)] * a
    for p in ps:
        row = [row[j] * (1 - p) + (row[j-1] * p if j else 0)
               for j in range(a + 1)]
    return 1 - sum(row)


def low_probability_conditions(values: Sequence[Q | int], capacity: int, demand: int) -> bool:
    ps = inputs(values, capacity, demand)
    return demand >= 2 and max(ps) <= LOW_PROBABILITY


def uniform_ratio_bound(pmax: Q | int, capacity: int, demand: int) -> Q:
    """Upper price / one (a+1)-selection event; pmax must be strictly below 1."""
    p = probability(pmax)
    a, d = positive_integer(capacity), positive_integer(demand)
    if p == 1:
        raise ValueError("uniform ratio needs pmax < 1")
    n = a * d + 1
    return p ** (n - a - 1) / (1 - p) ** n


def audit_block(values: Sequence[Q | int], capacity: int, demand: int) -> dict:
    ps = inputs(values, capacity, demand)
    q = tail_probability(ps, capacity)
    upper = math.prod(phi_upper(p) for p in ps)
    low = low_probability_conditions(ps, capacity, demand)
    if low:
        # Finite consistency check supplements, but does not replace, the proof.
        if upper > BUDGET_FACTOR * q:
            raise ArithmeticError("analytical low-probability inequality violated")
        certified, reason = True, "low-probability-factor-16/27"
    elif upper <= q:
        certified, reason = True, "price-upper-at-most-local-failure"
    elif q >= Q(2, 3):
        # -log(1-q) >= log(3) > 1, so phi(q)=1; each price is <=1.
        certified, reason = True, "local-hazard-cap-is-one"
    else:
        certified, reason = False, "not-certified-by-these-sufficient-tests"
    return {"certified_sufficient_budget": certified, "reason": reason,
            "local_failure": q, "all_transformed_prices_product_upper": upper,
            "low_probability_hypotheses": low,
            "meaning": "sufficient local budget, not theorem acceptance or optimal cover search"}


def positive_inflated_price(p: Q | int) -> Q:
    """For 0<p<=1/4: p < p+p^2/2 < phi(p), by an elementary integral bound."""
    p = probability(p)
    if not 0 < p <= LOW_PROBABILITY:
        raise ValueError("this example requires 0<p<=1/4")
    return p + p*p/2


def demo() -> dict:
    p = Q(1, 40900)
    audit = audit_block([p] * 409, 1, 408)
    failure = audit_block([Q(1,2)] * 2, 1, 1)
    return {
        "object": "P15-TRANSFORMED-PRICE-BUDGET-20260924-v1",
        "analytical_scope": "realized family; every d_i>=2 and every p_v<=1/4",
        "all_prices": "0<=c_v<=min(1,-log(1-p_v))",
        "global_cover_bound": "min(1,(16/27)*[-log(mu_p(D))])",
        "local_factor": str(BUDGET_FACTOR),
        "six_block_example": {
            "coordinates": 6*409, "unchanged_palette": max(408, (6*408+2)//3),
            "block_budget_certified": audit["certified_sufficient_budget"],
            "probability": str(p), "strictly_larger_admissible_price": str(positive_inflated_price(p)),
            "cover_cost_at_maximal_prices": "6*log(40900/40899)^409",
            "rational_cover_cost_upper": "6/(40899^409)"},
        "previous_two_coordinate_counterexample": {
            "covered_by_new_hypotheses": failure["low_probability_hypotheses"],
            "sufficient_checker_accepts": failure["certified_sufficient_budget"],
            "status": "unchanged: unrestricted same-palette extension is false"},
        "scientific_acceptance": False}


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, sort_keys=True))
