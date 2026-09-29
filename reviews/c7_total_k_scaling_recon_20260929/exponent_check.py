#!/usr/bin/env python3
# exponent_check.py — exact exponent bookkeeping for CL-C7-TOTAL-K-SCALING-RECON-20260929-v1.
# Python stdlib only; fail-closed; -O byte-identical. Mutants: --mutant M1|M2 -> exit 1.
# Verifies only the piecewise power-law integrals of RECONNAISSANCE.md §4 (symbolic
# exponent arithmetic in Fractions) — NOT the heuristic (H) and NOT any theorem.

import json
import sys
from fractions import Fraction as F


def check(name, cond):
    if not cond:
        print("FAIL " + name)
        raise SystemExit(1)


def power_integral_exponent(p, lo_exp, hi_exp):
    """For int_{c1 l^lo_exp}^{c2 l^hi_exp} k^p dk with p != -1: the l-exponent of the
    dominant endpoint contribution. Returns (exponent, which_end)."""
    q = p + 1
    if q > 0:      # dominated by the upper limit
        return (q * hi_exp if hi_exp is not None else None), "upper"
    else:          # dominated by the lower limit
        return q * lo_exp, "lower"


def main(argv):
    mutant = None
    if len(argv) == 3 and argv[1] == "--mutant":
        mutant = argv[2]
    elif len(argv) != 1:
        raise SystemExit(2)
    res = {}

    # Scenario (H): 1 - p_r <= C min{1, (r/k)^3}, r^3 = l/k  ->  (r/k)^3 = l / k^4
    # threshold k_* : l / k^4 = 1  ->  k_* = l^{1/4}
    thr = F(1, 4) if mutant != "M1" else F(1, 3)
    check("T_threshold", F(1, 4) == thr)
    # piece 1: k in [l/r0^3, k_*], integrand k^{-2/3}: int ~ k_*^{1/3} = l^{1/12} (upper end dominates)
    e1, end1 = power_integral_exponent(F(-2, 3), 1, thr)
    check("P1_exponent", e1 == F(1, 12) and end1 == "upper")
    # piece 2: k in [k_*, inf), integrand l * k^{-4} * k^{-2/3} = l k^{-14/3}: int ~ l * k_*^{-11/3} = l^{1/12}
    e2, end2 = power_integral_exponent(F(-14, 3), thr, None)
    check("P2_exponent", F(1) + e2 == F(1, 12) and end2 == "lower")
    total = F(-1, 3) + F(1, 12)
    check("RHO_near_exponent_minus_1_4", total == F(-1, 4))
    # inverse-moment threshold for a density ~ l^{-1/4}: int_0 l^{q - 1/4} finite iff q > -3/4
    check("MOMENT_threshold_minus_3_4", F(-1, 4) + 1 == F(3, 4))
    res["scenario_H"] = {"threshold_k*": "l^(1/4)", "piece1": "l^(1/12)", "piece2": "l^(1/12)",
                         "rho_rej_near": "l^(-1/3) * l^(1/12) = l^(-1/4)", "moment_threshold": "q > -3/4"}

    # Contrast scenario: k-uniform C r^3 = C l / k  ->  integrand l * k^{-1} * k^{-2/3} = l k^{-5/3}
    # on [l/r0^3, inf): int ~ l * (l/r0^3)^{-2/3} = l^{1/3}  ->  rho ~ l^{-1/3} * l^{1/3} = O(1)
    e3, end3 = power_integral_exponent(F(-5, 3), 1, None)
    check("CONTRAST_O1", F(1) + e3 == F(1, 3) and F(-1, 3) + F(1, 3) == 0 and end3 == "lower")
    check("CONTRAST_moment_threshold_minus_1", F(0) + 1 == 1)   # density O(1): finite iff q > -1
    res["scenario_uniform"] = {"rho_rej_near": "O(1)", "moment_threshold": "q > -1"}

    # ledgers of the two candidate lower-bound events (§5)
    # planar/#149-type event: mass k^4 r, weight k^4 r^4, normalizer k^2 r^2 -> k^6 r^3
    check("LEDGER_cubic_event", (4 + 4 - 2, 1 + 4 - 2) == (6, 3))
    # conjectured dominant layer: mass r/k, weight r^4 (k cancels), normalizer k^2 r^2 -> r^3 k^{-3}
    kexp = (-1) + 0 - 2
    check("LEDGER_conjectured_layer", (kexp, 1 + 4 - 2) == (-3, 3))
    if mutant == "M2":
        check("LEDGER_conjectured_layer_mutant", kexp == -2)
    res["ledgers"] = {"cubic_event": "k^6 r^3", "conjectured_layer": "(r/k)^3"}

    # compact-window consistency: k in [k-, k+] fixed -> min{1,(r/k)^3} = C r^3 = C l/k -> loss O(l^{2/3})
    check("COMPACT_consistency", F(-1, 3) + 1 == F(2, 3))
    res["compact_window"] = "O(l^(2/3)) recovered"

    print(json.dumps({"object": "CL-C7-TOTAL-K-SCALING-RECON-20260929-v1-CHECKS",
                      "scope": "exponent bookkeeping only; the heuristic (H) is not verified here",
                      "results": res, "passed": True}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv)
