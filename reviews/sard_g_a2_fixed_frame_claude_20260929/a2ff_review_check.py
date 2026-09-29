"""Independent exact checks for OA-SARD-A2-FIXED-FRAME-20260929-v2 (Math-#137 v2/A2_FIXED_FRAME.md), counterexample F1-F3.

f_t = (x^2-y^2)/2 + g(x,y) - t x - (2/3) t |t|^(1/2) y,  g = (2/3) x y (x^2+y^2)^(1/4).
On the axis y = 0 the needed derivatives of g are exact: g_x(x,0) = 0, g_xx(x,0) = 0, g_yy(x,0) = 0,
g_y(x,0) = (2/3) x |x|^(1/2), g_xy(x,0) = |x|^(1/2). Take t = s^2 with s = (k^2-1)/(2k), k rational > 1, so that
sqrt(t) = s and sqrt(1+t) = (k^2+1)/(2k) are rational.
  CRITICAL   grad f_t(t,0) = 0 exactly.
  HESSIAN    H(p_t) = [[1, s], [s, -1]]; eigenvalue sqrt(1+t) with eigenvector (1, m), m = s/(1+sqrt(1+t)) (F3).
  NONDIFF    m(t)/t >= 1/(3 sqrt t) and m(t)/t is unbounded along t -> 0 (F3 claim): the slope is not differentiable.
Mutants (each must fail): wrong-slope, bounded-quotient, nonzero-gradient.
"""
import argparse
import json
import sys
from fractions import Fraction as F

MUTANTS = ("wrong-slope", "bounded-quotient", "nonzero-gradient")
MUT = None


def instance(k):
    s = (k * k - 1) / (2 * k)
    root = (k * k + 1) / (2 * k)             # sqrt(1 + s^2)
    t = s * s
    return s, root, t


def check():
    out = {"CRITICAL": True, "HESSIAN": True, "NONDIFF": True}
    quotients = []
    for k in (F(2), F(3, 2), F(5, 4), F(11, 10), F(101, 100), F(1001, 1000)):
        s, root, t = instance(k)
        assert root * root == 1 + t
        x = t
        gx, gy = F(0), F(2, 3) * x * s          # |x|^(1/2) = s since x = t = s^2 > 0
        pin_y = -F(2, 3) * t * s                 # -(2/3) t |t|^(1/2)
        fx = x - t + gx
        fy = -F(0) + gy + pin_y + (F(1, 1000) if MUT == "nonzero-gradient" else F(0))
        out["CRITICAL"] &= fx == 0 and fy == 0
        H = [[1 + F(0), s], [s, -1 + F(0)]]      # g_xx = g_yy = 0 on the axis, g_xy = |x|^(1/2) = s
        m = s / (1 + root) if MUT != "wrong-slope" else s / (2 + root)
        lam = root
        out["HESSIAN"] &= H[0][0] + H[0][1] * m == lam and H[1][0] + H[1][1] * m == lam * m
        q = m / t
        out["NONDIFF"] &= q >= 1 / (3 * s)
        quotients.append(q)
    grows = all(quotients[i + 1] > quotients[i] for i in range(len(quotients) - 1)) and quotients[-1] > 100
    out["NONDIFF"] &= (not grows) if MUT == "bounded-quotient" else grows
    return out


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    checks = check()
    passed = all(checks.values())
    print(json.dumps({"object": "CLAUDE-REVIEW-SARD-A2-FIXED-FRAME-20260929-v1", "checks": checks, "passed": passed,
                      "scope": "exact checks of the counterexample only; the Banach-space proof is reviewed in REVIEW.md"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
