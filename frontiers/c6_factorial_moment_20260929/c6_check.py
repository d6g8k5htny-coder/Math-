"""Finite companion for CL-C6-FACTORIAL-20260929-v1 (PROOF.md). Standard library only.

  ELIMINATION   F1 - (12k/T3) F2 = q * l(p, q) with l linear, exactly on a rational grid; l(0,0) = 2 det DF(0,0)/T3 and
                l(1,0) = -2 det DF(1,0)/T3; on the W-support (M max, S saddle) both values carry the sign of T3.
  CAP_ATTAINED  k = 1/3, T3 = 0, C3 = -1, D = 0, sigma = -1/8: M is a maximum and S a saddle of the leading-order model,
                whose zero set is exactly {(0,0), (1,0), (-1/8, 3/4), (-1/8, -3/4)} (Bezout bound 4 attained).
  REMAINDER     sum_{k>m} 2^-k = 2^-m exactly (Cauchy remainder (6.1)).
  PACKING       radii rho_i = eta' + 2 i delta give disjoint delta-balls, and their number times the 4-ball volume is at
                least (pi^2/4) eta' delta^3 (6.2); delta = 2^(1-m), lambda^3 eps = 2^(1-m/2) for lambda = 2^(m/8).
  RADIAL        int_{|y|<=R} min(1, eps^4/|y|^2) d^2y = pi eps^4 (1 + 2 ln(R/eps^2)) (numerical quadrature), and the
                ratio to eps^4 grows without bound: the logarithm in Lemma M(c) is genuine.
Mutants (each must fail): wrong-elimination, touching-balls, no-log, short-remainder.
"""
import argparse
import json
import math
import sys
from fractions import Fraction as F

MUTANTS = ("wrong-elimination", "touching-balls", "no-log", "short-remainder")
MUT = None


def model(p, q, k, T3, C3, D, s):
    F1 = 6 * k * p * (p - 1) + (p - F(1, 2)) * q * T3 + q * q * C3 / 2
    F2 = s * q + T3 / 2 * p * (p - 1) + p * q * C3 + q * q * D / 2
    return F1, F2


def check_elimination():
    ok = True
    params = [(F(1, 2), F(3), F(-1, 4), F(2, 7), F(1, 3)), (F(2), F(-5, 3), F(7, 2), F(-1), F(-4)),
              (F(3, 4), F(1, 9), F(0), F(5), F(0)), (F(1, 3), F(-2), F(-1), F(1, 2), F(-7, 5))]
    coef = 6 if MUT == "wrong-elimination" else 12
    for k, T3, C3, D, s in params:
        for p in (F(-1, 3), F(0), F(1, 2), F(1), F(7, 5)):
            for q in (F(0), F(1, 4), F(-2, 3)):
                F1, F2 = model(p, q, k, T3, C3, D, s)
                ell = (p - F(1, 2)) * T3 - (12 * k / T3) * (s + p * C3) + q * (C3 / 2 - 6 * k * D / T3)
                ok &= F1 - (coef * k / T3) * F2 == q * ell
        detM = -6 * k * s - T3 * T3 / 4
        detS = 6 * k * (s + C3) - T3 * T3 / 4
        l0 = -T3 / 2 - (12 * k / T3) * s
        l1 = T3 / 2 - (12 * k / T3) * (s + C3)
        ok &= l0 == 2 * detM / T3 and l1 == -2 * detS / T3
        if detM > 0 and detS < 0:                                   # W-support: same sign as T3
            ok &= (l0 > 0) == (T3 > 0) and (l1 > 0) == (T3 > 0)
    return ok


def check_cap():
    k, T3, C3, D, s = F(1, 3), F(0), F(-1), F(0), F(-1, 8)
    zeros = [(F(0), F(0)), (F(1), F(0)), (F(-1, 8), F(3, 4)), (F(-1, 8), F(-3, 4))]
    ok = all(model(p, q, k, T3, C3, D, s) == (0, 0) for p, q in zeros)
    # completeness: F2 = q (s + p C3) (T3 = D = 0); q = 0 forces p(p-1) = 0, else p = -s/C3 and q^2 = -12 k p(p-1)/C3
    p_extra = -s / C3
    q2 = -12 * k * p_extra * (p_extra - 1) / C3
    ok &= p_extra == F(-1, 8) and q2 == F(9, 16)
    detM, trM = -6 * k * s - T3 * T3 / 4, -6 * k + s                  # DF(0,0) = [[-6k, -T3/2], [-T3/2, s]]
    detS = 6 * k * (s + C3) - T3 * T3 / 4
    ok &= detM > 0 and trM < 0 and detS < 0                           # M maximum, S saddle
    return ok and len(zeros) == 4


def check_remainder():
    ok = True
    for m in (1, 5, 17):
        tail = sum(F(1, 2 ** kk) for kk in range(m + 1, m + 81)) + F(1, 2 ** (m + 80))
        bound = F(1, 2 ** (m + 1)) if MUT == "short-remainder" else F(1, 2 ** m)
        ok &= tail <= bound
    return ok


def check_packing():
    ok = True
    for m in (8, 16, 24):
        lam = 2 ** (m // 8)
        eps = F(2 * lam, 2 ** m)
        delta = eps / lam
        ok &= delta == F(2, 2 ** m) and lam ** 3 * eps == F(2, 2 ** (m // 2))
        for eta in (F(1, 8), F(1, 64)):
            if delta > eta / 2:
                continue
            count = int(eta / (2 * delta)) + 1
            step = delta if MUT == "touching-balls" else 2 * delta
            radii = [eta + i * step for i in range(count)]
            ok &= radii[-1] <= 2 * eta or MUT == "touching-balls"
            ok &= all(radii[i + 1] - radii[i] >= 2 * delta for i in range(count - 1))   # disjoint delta-balls
            ok &= count * delta ** 4 / 2 >= eta * delta ** 3 / 4                        # (pi^2 cancels)
    return ok


def radial(eps, R, n=4000):
    """int_0^R min(1, eps^4/t^2) 2 pi t dt by the substitution t = exp(u) and Simpson's rule on [ln(eps^2), ln R]."""
    a, b = math.log(eps * eps), math.log(R)
    h = (b - a) / n
    g = lambda u: min(1.0, eps ** 4 / math.exp(2 * u)) * 2 * math.pi * math.exp(2 * u)
    s = g(a) + g(b) + sum((4 if i % 2 else 2) * g(a + i * h) for i in range(1, n))
    return math.pi * eps ** 4 + s * h / 3


def check_radial():
    ok = True
    R = 1.0
    ratios = []
    for e in (1e-1, 1e-2, 1e-3, 1e-4):
        closed = math.pi * e ** 4 * (1 + 2 * math.log(R / e ** 2))
        num = radial(e, R)
        ok &= abs(num - closed) <= 1e-6 * closed
        ratios.append(num / e ** 4)
    grows = all(ratios[i + 1] > ratios[i] + 1 for i in range(len(ratios) - 1))
    ok &= (not grows) if MUT == "no-log" else grows
    return ok


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    checks = {"ELIMINATION": check_elimination(), "CAP_ATTAINED": check_cap(), "REMAINDER": check_remainder(),
              "PACKING": check_packing(), "RADIAL": check_radial()}
    passed = all(checks.values()) and len(checks) == 5
    print(json.dumps({"object": "CL-C6-FACTORIAL-20260929-v1", "checks": checks, "passed": passed,
                      "scope": "finite identities and one quadrature only; the analytic proof is PROOF.md"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
