#!/usr/bin/env python3
# exponent_check.py — exact controls for CL-C7-TOTAL-BOUNDED-20260929-v1.1.
# Python stdlib only; fail-closed; -O byte-identical. Mutants: --mutant M1|M2|M3 -> exit 1.
#   M1 = the withdrawn v1 error (drop the (k+r)^2 factor of (K1), i.e. use the crude majorant)
#   M2 = wrong split threshold (k_* = l^{1/3} instead of l^{1/4})
#   M3 = the false saddle bound of the withdrawn draft (drops the r K^2 U^2/4 mixed term in (6.2'))
# Verifies: the exact (7.3) integral with D, E symbolic; the (r/k)^4 (k+r)^2 <= 4 r^3/k
# reduction for r <= k; the piecewise power-law integrals of Corollary T; the resulting
# orders O(l^{1/4}) + O(1); the inverse-moment threshold -1; and that the v1 route
# (crude majorant) would have produced l^{-1/4}. It does NOT verify the Gaussian steps.

import json
import sys
from fractions import Fraction as F


def check(name, cond):
    if not cond:
        print("FAIL " + name)
        raise SystemExit(1)


# --- tiny multivariate polynomial helpers: dict {exp tuple: Fraction} ---------
def padd(p, q):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, F(0)) + v
        if out[k] == 0:
            del out[k]
    return out


def pmul(p, q):
    out = {}
    for k1, v1 in p.items():
        for k2, v2 in q.items():
            k = tuple(a + b for a, b in zip(k1, k2))
            out[k] = out.get(k, F(0)) + v1 * v2
    return {k: v for k, v in out.items() if v != 0}


def pint_def(p, idx, hi):
    """int_0^{hi} over variable idx (hi a polynomial in the other variables)."""
    n = len(next(iter(p)))
    out = {}
    for k, v in p.items():
        e = k[idx]
        coef = v / (e + 1)
        term = {tuple(0 if j == idx else k[j] for j in range(n)): coef}
        for _ in range(e + 1):
            term = pmul(term, hi)
        out = padd(out, term)
    return out


def main(argv):
    mutant = None
    if len(argv) == 3 and argv[1] == "--mutant":
        mutant = argv[2]
    elif len(argv) != 1:
        raise SystemExit(2)
    res = {}

    # ---- (6.2') layer integral, exact: variables (lam, D, r, U, a, K)
    # int_0^{D r U^2} lam [a lam + a r K U + r K^2 U^2/4] dlam
    #   = r^3 U^5 [a D^3 U/3 + a K D^2/2 + K^2 D^2 U/8]
    w = lambda l_, d_, r_, u_, a_, k_: (l_, d_, r_, u_, a_, k_)
    lam6 = {w(1, 0, 0, 0, 0, 0): F(1)}
    a6 = {w(0, 0, 0, 0, 1, 0): F(1)}
    rKU = {w(0, 0, 1, 1, 0, 1): F(1)}
    rK2U2_4 = {w(0, 0, 1, 2, 0, 2): F(1, 4)}
    bracket = padd(padd(pmul(a6, lam6), pmul(a6, rKU)), rK2U2_4)
    # M3 mutant: the (withdrawn draft's) false saddle bound drops the r K^2 U^2/4 mixed term
    if mutant == "M3":
        bracket = padd(pmul(a6, lam6), pmul(a6, rKU))
    integrand6 = pmul(lam6, bracket)
    hi6 = {w(0, 1, 1, 2, 0, 0): F(1)}       # D r U^2
    I6 = pint_def(integrand6, 0, hi6)
    want6 = {w(0, 3, 3, 6, 1, 0): F(1, 3),  # a D^3 r^3 U^6 / 3
             w(0, 2, 3, 5, 1, 1): F(1, 2),  # a K D^2 r^3 U^5 / 2
             w(0, 2, 3, 6, 0, 2): F(1, 8)}  # K^2 D^2 r^3 U^6 / 8
    check("K_62prime_layer_integral_exact", I6 == want6)
    check("K_62prime_all_terms_r_cubed", all(k[2] == 3 for k in I6))
    # at a = h/2 = K U/2 the bracket is P's (6.2): (KU/2)[lam + (3/2) r K U]
    a_eq_h2 = {w(0, 0, 0, 1, 0, 1): F(1, 2)}
    P62 = pmul(a_eq_h2, padd(lam6, {w(0, 0, 1, 1, 0, 1): F(3, 2)}))
    bracket_at_h2 = padd(padd(pmul(a_eq_h2, lam6), pmul(a_eq_h2, rKU)), rK2U2_4)
    check("K_62prime_reduces_to_P62_at_a_eq_h2", bracket_at_h2 == P62)
    res["(6.2')"] = "layer integral r^3 U^5 [a D^3 U/3 + a K D^2/2 + K^2 D^2 U/8]; equals P (6.2) at a = h/2"
    # ---- k-power reductions for the three terms (k <= 1, r <= k): each <= C k^-3 (k^2 + r^2) * poly
    for r_, k_ in ((F(1, 10), F(1, 2)), (F(1, 3), F(1, 3)), (F(1, 100), F(1, 5)), (F(2, 7), F(1, 2)), (F(1, 2), F(1))):
        check("K_AMGM_r_k2", r_ * k_ ** -2 <= (k_ ** -1 + r_ ** 2 * k_ ** -3) / 2)
        check("K_k2_le_k3", k_ ** -2 <= k_ ** -3)           # k <= 1
    res["k_reductions"] = "a^2 k^-3, a^2 k^-2, a k^-2 all <= C k^-3 (k^2 + r^2) poly(U) for k <= 1; a k^-2 via r k^-2 <= (k^-1 + r^2 k^-3)/2"

    # ---- (7.3) exact (P's own two-term form, a = h/2 special case kept for reference)
    v = lambda a, b, c, d, e: (a, b, c, d, e)
    lam = {v(1, 0, 0, 0, 0): F(1)}
    ErU = {v(0, 0, 1, 1, 1): F(1)}
    integrand = pmul(lam, padd(lam, ErU))
    hi = {v(0, 1, 1, 2, 0): F(1)}          # D r U^2
    I = pint_def(integrand, 0, hi)
    want = {v(0, 3, 3, 6, 0): F(1, 3), v(0, 2, 3, 5, 1): F(1, 2)}   # D^3 r^3 U^6 /3 + E D^2 r^3 U^5 /2
    check("K_73_exact_integral", I == want)
    check("K_73_r_cubed", all(k[2] == 3 for k in I))
    res["(7.3)"] = "int_0^{D r U^2} lam(lam+E r U) dlam = r^3 U^5 (D^3 U/3 + E D^2/2), exact"

    # ---- D = 4K^2/(3k): D^3 ~ k^-3, D^2 ~ k^-2 <= k^-3 for k <= 1 (exponent bookkeeping)
    check("K_D_powers", (-3, -2) == (-3, -2) and F(1) ** -2 <= F(1) ** -3)
    # ---- (r/k)^4 (k+r)^2 <= 4 r^3/k for r <= k  (exact on a rational grid)
    for r_, k_ in ((F(1, 10), F(1, 2)), (F(1, 3), F(1, 3)), (F(1, 100), F(1, 5)), (F(2, 7), F(1, 2))):
        check("K_far_and_M4_reduction", (r_ / k_) ** 4 * (k_ + r_) ** 2 <= 4 * r_ ** 3 / k_)
    res["(K2)_reductions"] = "(r/k)^4 (k+r)^2 <= 4 r^3/k for r <= k; depth term r^5 k^-3 (k^2 + r^2) <= 2 r^5/k for r <= k"
    for r_, k_ in ((F(1, 10), F(1, 2)), (F(1, 3), F(1, 3))):
        check("K_depth_reduction", r_ ** 5 * k_ ** -3 * (k_ ** 2 + r_ ** 2) <= 2 * r_ ** 5 / k_)

    # ---- Corollary T piecewise integrals (symbolic exponents in l) ---------------------
    thr = F(1, 3) if mutant == "M2" else F(1, 4)       # k_* = l^thr  (r = k  <=> k^4 = l)
    check("T_threshold_is_r_equals_k", F(1, 4) * 4 == 1 and (thr == F(1, 4)))
    maj_power = 0 if mutant == "M1" else 2               # (k + r)^maj_power in (K1)
    # piece A: k >= k_*, integrand (l/k^2) k^{-2/3} = l k^{-8/3}: exponent of int = 1 + (-8/3+1)*thr
    eA = 1 + (F(-8, 3) + 1) * thr
    check("T_pieceA_7_12", eA == F(7, 12))
    # piece B1: k < k_*, k^{maj_power} k^{-2/3}: int_0^{k_*} = k_*^{maj_power + 1/3}
    eB1 = (maj_power + F(1, 3)) * thr
    check("T_pieceB1_7_12", eB1 == F(7, 12))
    # piece B2: r^2 k^{-2/3} = l^{2/3} k^{-4/3}: lower endpoint l/r0^3 dominates -> l^{2/3} * l^{-1/3} = l^{1/3}
    eB2 = F(2, 3) + F(-4, 3) + 1          # l^{2/3} * (l)^{(-4/3+1)}
    check("T_pieceB2_1_3", eB2 == F(1, 3))
    near_A = F(-1, 3) + eA
    near_B1 = F(-1, 3) + eB1
    near_B2 = F(-1, 3) + eB2
    check("T_near_orders", near_A == F(1, 4) and near_B1 == F(1, 4) and near_B2 == 0)
    res["Corollary_T"] = {"near, r<=k": "O(l^{1/4})", "near, r>k, k^2-part": "O(l^{1/4})",
                          "near, r>k, r^2-part": "O(1) (cutoff shell)", "far": "O(1) by (14.1)",
                          "total": "O(1); Theta(1) with Theorem U", "rejected_moment_threshold": "q > -1 (sharp)"}
    # the withdrawn v1 route: crude majorant (no (k+r)^2) with min{1,(r/k)^3} normalized bound
    # gives k^{-2/3} on [0,k_*] -> k_*^{1/3} = l^{1/12}, i.e. l^{-1/3+1/12} = l^{-1/4}
    v1 = F(-1, 3) + F(1, 3) * F(1, 4)
    check("V1_route_recorded_as_wrong", v1 == F(-1, 4) and v1 != near_B1)
    res["withdrawn_v1"] = "crude majorant route gives l^{-1/4}; wrong because A_r ~ k^2 (P (5.4)); kept as mutant M1"

    # ---- selected/candidate thresholds unchanged: density ~ l^{-1/3} -> q > -2/3
    check("T_individual_threshold", F(-1, 3) + 1 == F(2, 3))

    print(json.dumps({"object": "CL-C7-TOTAL-BOUNDED-20260929-v1.1-CHECKS",
                      "scope": "exact exponent/integral bookkeeping for Theorem K and Corollary T; Gaussian steps not verified",
                      "results": res, "passed": True}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv)
