"""Exact polynomial companion for CL-SARD-A2-REGULARITY-20260929-v1 (PROOF.md). Standard library, exact rationals.

INVARIANCE   for V_t(x,y) = (x, -y + x^2 + t1 x^3 + t2 x^4) the graph y = x^2/3 + t1 x^3/4 + t2 x^4/5 is invariant
             (coefficientwise polynomial identity), so the unstable-manifold graph is C1 in (x, t) and LINEAR in the
             perturbation coefficients.
LYAPUNOV     the t1-derivative x^3/4 equals the bounded backward solution z(0) = int_{-inf}^0 e^{s} (x e^{s})^3 ds,
             i.e. x^3 * 1/(3+1); the t2-derivative x^4/5 likewise with 1/(4+1).
SADDLE       V_t = (x - t, -y + x^2): p(t) = (t, t^2) and dp/dt = -DV(p)^{-1} d_tV = (1, 2t) exactly.
Mutants (each must fail): lp-exponent, nonlinear-superposition, saddle-sign.
"""
import argparse
import json
import sys
from fractions import Fraction as F

MUTANTS = ("lp-exponent", "nonlinear-superposition", "saddle-sign")
MUT = None


def poly_mul(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            out[i + j] = out.get(i + j, F(0)) + x * y
    return {k: v for k, v in out.items() if v != 0}


def poly_add(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, F(0)) + v
    return {k: v for k, v in out.items() if v != 0}


def deriv(p):
    return {k - 1: k * v for k, v in p.items() if k > 0}


def check_invariance():
    ok = True
    for t1 in (F(0), F(1), F(-3, 2)):
        for t2 in (F(0), F(2, 5), F(-1)):
            c4 = t2 / 5 if MUT != "nonlinear-superposition" else t2 / 5 + t1 * t2
            w = {2: F(1, 3), 3: t1 / 4, 4: c4}                  # y = w(x)
            xdot = {1: F(1)}                                  # xdot = x
            lhs = poly_mul(deriv(w), xdot)                    # d/dt w(x(t)) = w'(x) xdot
            rhs = poly_add({k: -v for k, v in w.items()}, {2: F(1), 3: t1, 4: t2})   # ydot on the graph
            ok &= lhs == rhs
    return {"graph_invariant_and_linear_in_perturbation": ok}


def check_lyapunov():
    # z' = -z + x(s)^n with x(s) = x e^{s}: bounded backward solution z(0) = x^n int_{-inf}^0 e^{(n+1)s} ds = x^n/(n+1)
    ok = True
    for n, coeff in ((3, F(1, 4)), (4, F(1, 5))):
        integral = F(1, n + (0 if MUT == "lp-exponent" else 1))
        ok &= integral == coeff
    return {"variation_equals_backward_integral": ok}


def check_saddle():
    ok = True
    for t in (F(0), F(1, 3), F(-2)):
        p = (t, t * t)
        ok &= p[0] - t == 0 and -p[1] + p[0] ** 2 == 0          # V_t(p) = 0
        DV = [[F(1), F(0)], [2 * p[0], F(-1)]]
        det = DV[0][0] * DV[1][1] - DV[0][1] * DV[1][0]
        inv = [[DV[1][1] / det, -DV[0][1] / det], [-DV[1][0] / det, DV[0][0] / det]]
        dtV = (F(-1), F(0))
        sign = 1 if MUT == "saddle-sign" else -1
        dp = tuple(sign * (inv[i][0] * dtV[0] + inv[i][1] * dtV[1]) for i in range(2))
        ok &= dp == (F(1), 2 * t)
    return {"saddle_displacement_formula": ok}


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    checks = {**check_invariance(), **check_lyapunov(), **check_saddle()}
    passed = all(checks.values())
    print(json.dumps({"object": "CL-SARD-A2-REGULARITY-20260929-v1", "checks": checks, "passed": passed,
                      "scope": "exact polynomial identities only; not the invariant-manifold theorems"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
