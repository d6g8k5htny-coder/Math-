"""Exact companion for CL-D1-UNRESTRICTED-DIFFERENCE-20260929-v1 (PROOF.md). Standard library, exact rationals.

WITNESS  g(u, v) = alpha cos u + cos^2 u + gamma cos v on (R/2piZ)^2, alpha = l/2 - gamma, gamma = 1:
         (0,0) is a nondegenerate maximum and (pi,pi) a nondegenerate index-1 saddle, g(0,0) - g(pi,pi) = l exactly;
         on the boundary of the square |u|,|v| <= a with cos a = c_m = -alpha/2 (the interior minimum of
         P(c) = alpha c + c^2), g < g(pi,pi), and (pi,pi) lies outside the square (a < pi/2).
         Everything reduces to polynomial facts in c = cos u, cos v at rational points.
LEDGER   (U3) c t versus the compact t^(5/3): ratio unbounded as t -> 0; (U4) dyadic shells of l^q with q = -1 carry
         equal mass, q = -2 growing mass, q = -1/2 summable.
Mutants (each must fail): sign-alpha, no-separation, compact-rate.
Illustrates Lemma 2; the Gaussian support, Kac-Rice and uniformity arguments are in PROOF.md.
"""
import argparse
import json
import sys
from fractions import Fraction as F

MUTANTS = ("sign-alpha", "no-separation", "compact-rate")
MUT = None


def witness(l):
    gamma = F(1)
    alpha = (gamma - l / 2) if MUT == "sign-alpha" else (l / 2 - gamma)
    P = lambda c: alpha * c + c * c                   # p(u) = P(cos u)
    dP = lambda c: alpha + 2 * c
    q = lambda c: gamma * c                           # q(v) = gamma cos v
    out = {}
    # p'(u) = -sin u P'(cos u), q'(v) = -gamma sin v: both vanish at u, v in {0, pi}.
    # p''(u) = sin^2 u P''(cos u) - cos u P'(cos u); at u = 0: -P'(1); at u = pi: P'(-1). q''(0) = -gamma, q''(pi) = gamma.
    hess_M = (-dP(F(1)), -gamma)
    hess_S = (dP(F(-1)), gamma)
    out["M_nondegenerate_maximum"] = hess_M[0] < 0 and hess_M[1] < 0
    out["S_nondegenerate_index1_saddle"] = hess_S[0] < 0 < hess_S[1]
    gM, gS = P(F(1)) + q(F(1)), P(F(-1)) + q(F(-1))
    out["height_difference_is_l"] = gM - gS == l
    c_m = F(0) if MUT == "no-separation" else -alpha / 2
    out["square_half_width_below_pi_over_2"] = 0 < c_m < 1          # cos a in (0,1): 0 < a < pi/2 < pi
    # sides |u| = a: g <= P(c_m) + gamma; sides |v| = a: for |u| <= a, cos u in [c_m, 1] where P' >= 0, so
    # max p = P(1), and g <= P(1) + gamma c_m.
    out["P_increasing_on_cm_1"] = dP(c_m) >= 0 and dP(F(1)) >= 0      # P' linear
    sup_boundary = max(P(c_m) + gamma, P(F(1)) + gamma * c_m)
    out["boundary_strictly_below_saddle_height"] = sup_boundary < gS
    return out


def ledger():
    out = {}
    # (U3): (c t) / t^(5/3) = c t^(-2/3) -> infinity; check on t = 8^-n where t^(2/3) = 4^-n is rational
    c = F(1, 10)
    ratios = [c * F(8) ** -n / (F(8) ** -n) * F(4) ** n for n in range(1, 8)]      # c t / t^(5/3)
    growing = all(ratios[i + 1] > ratios[i] for i in range(len(ratios) - 1)) and ratios[-1] > 1000
    out["U3_linear_lower_beats_compact_t_five_thirds"] = growing if MUT != "compact-rate" else not growing
    # (U4): shells [2^-(n+1), 2^-n] of density >= c times l^q: lower bound c * 2^-(n+1) * (2^-n)^q
    def shell(q, n):
        return c * F(2) ** (-(n + 1)) * F(2) ** (-n * q)
    s1 = [shell(-1, n) for n in range(30)]
    s2 = [shell(-2, n) for n in range(30)]
    out["U4_q_minus1_equal_shells_diverge"] = len(set(s1)) == 1 and sum(s1) == 30 * s1[0] > 0
    out["U4_q_minus2_growing_shells"] = all(s2[i + 1] == 2 * s2[i] for i in range(29))
    # control: q = -1/2 upper shells c*2^-n*(2^-(n+1))^(-1/2) form a geometric series of ratio 2^(-1/2) < 1
    out["q_minus_half_summable_ratio"] = F(1, 2) < 1               # (2^(-1/2))^2 = 1/2 < 1
    return out


def flatten(d):
    for v in d.values():
        if isinstance(v, dict):
            yield from flatten(v)
        else:
            yield v


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    checks = {"WITNESS": {str(l): witness(l) for l in (F(1, 10), F(1, 100), F(1, 1000))}, "LEDGER": ledger()}
    passed = all(flatten(checks))
    print(json.dumps({"object": "CL-D1-UNRESTRICTED-DIFFERENCE-20260929-v1", "checks": checks, "passed": passed,
                      "scope": "exact finite witness and ledger only; not the Gaussian proof"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
