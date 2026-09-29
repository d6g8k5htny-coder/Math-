"""Finite companion for CL-C6-SHARPENED-20260929-v1 (PROOF.md). Standard library only.

  SQUARE      -s^2/4 + R s = R^2 - (s/2 - R)^2 exactly (Lemma G's completing the square).
  SHELL       the lattice sum sum_{n in Z^d} |n'|^k exp(-|n'|^2/4 + R|n'|) (n' = 2 pi n, T = 1) stays below
              (1+R)^(k+d) e^(R^2) times a fixed constant for R = 1..6, d = 2, 3 (Lemma G's growth rate).
  REMAINDER   a_m = 2 (2 eta'/sqrt m)^(m+1) <= m^(-m/2) exactly at perfect squares m = k^2, eta' = 1/8 (3.1).
  EXPONENTS   lambda_m = m^(m/(8d)): (lambda_m^(2d)) exponent m/4 and lambda_m^2 exponent m/(4d), exactly; the Markov
              term m^(-m/4) m log m and the truncation term e^(Cm) m^(-m/(4d)) both fall below exp(-m log m/(8d)) once
              log m >= 8dC (checked in logs for C = 1 at m = e^(8d+1), e^(8d+4), e^(8d+8)).
  LOGEPS      log(1/eps_m) <= m log m from the exact eps_m = 4 m^(m/(8d)) (2 eta'/sqrt m)^(m+1), for eta' = 1/8, 1/64
              and m >= max(3, e^(4 log(1/(2 eta')))) (the enlarged m_0 of (3.3)); d = 2, 3, 4.
  RADIAL      int_{|t|<=R} min(1, eps^(2d)/|t|^d) d^d t = |S^(d-1)| eps^(2d) (1/d + log(R/eps^2)), d = 2, 3, quadrature.
  LAMBDA      lambda = A^d [L/log L]^d satisfies lambda^(1/d) log lambda >= A L at r = 2^-k, L = log(1/r), d = 2, 3.
Mutants (each must fail): fixed-radius, wrong-cutoff, planar-cap, drop-loglog, small-m0.
"""
import argparse
import itertools
import json
import math
import sys
from fractions import Fraction as F

MUTANTS = ("fixed-radius", "wrong-cutoff", "planar-cap", "drop-loglog", "small-m0")
MUT = None


def check_square():
    ok = True
    for R in (F(1), F(5, 2), F(7)):
        for s in (F(0), F(1, 3), F(4), F(19, 2)):
            ok &= -s * s / 4 + R * s == R * R - (s / 2 - R) ** 2
    return ok


def shell_sum(R, d, k, cutoff):
    tot = 0.0
    rng = range(-cutoff, cutoff + 1)
    for n in itertools.product(rng, repeat=d):
        s = 2 * math.pi * math.sqrt(sum(x * x for x in n))
        tot += s ** k * math.exp(-s * s / 4 + R * s)
    return tot


def check_shell():
    ok = True
    for d, cutoff in ((2, 12), (3, 7)):
        ratios = []
        for R in (1, 2, 3, 4, 5, 6):
            val = shell_sum(R, d, 2, cutoff)
            ratios.append(val / ((1 + R) ** (2 + d) * math.exp(R * R)))
        ok &= max(ratios) < 50 and all(x > 0 for x in ratios)
    return ok


def check_remainder():
    ok = True
    eta = F(1, 8)
    for k in (4, 5, 6, 8, 10):
        m = k * k
        a_m = 2 * (2 * eta / k) ** (m + 1)                          # sqrt(m) = k exactly
        if MUT == "fixed-radius":
            a_m = 2 * (2 * eta / (4 * eta)) ** (m + 1)            # radius 4 eta': factor 2^-m only
        ok &= a_m <= F(1, k ** m)                                  # m^(-m/2) = k^(-m)
    return ok


def check_exponents():
    ok = True
    for d in (2, 3, 4):
        lam_exp = F(1, 8 * d) if MUT != "wrong-cutoff" else F(1, 4 * d)
        markov = 2 * d * lam_exp - F(1, 2)                       # exponent of m^(m*.) in lambda^(2d) a_m
        trunc = -2 * lam_exp                                     # exponent in the lambda^-2 truncation
        ok &= markov == -F(1, 4) and trunc == -F(1, 4 * d)
        for shift in (1, 4, 8):                                 # m >= e^(8d C) with C = 1: the regime m >= m_0
            m = math.exp(8 * d + shift)
            lm = math.log(m)
            target = -m * lm / (8 * d)
            ok &= float(markov) * m * lm + math.log(m * lm) <= target
            ok &= m + float(trunc) * m * lm <= target              # e^(Cm) with C = 1
    return ok


def log_inv_eps(m, eta, d):
    return (m + 1) * (0.5 * math.log(m) + math.log(1 / (2 * eta))) - m * math.log(m) / (8 * d) - math.log(4)


def check_logeps():
    ok = True
    for eta in (1 / 8, 1 / 64):                                      # eta_0 = eta = 1/8, eta_j = eta/8
        m0 = max(3.0, math.exp(4 * math.log(1 / (2 * eta))))
        if MUT == "small-m0":
            m0 = 16.0                                               # no enlargement of m_0
        for d in (2, 3, 4):
            for mult in (1, 2, 10, 1000):
                m = m0 * mult
                ok &= log_inv_eps(m, eta, d) <= m * math.log(m)
    return ok


def radial(eps, R, d, n=6000):
    a, b = math.log(eps * eps), math.log(R)
    h = (b - a) / n
    area = 2 * math.pi if d == 2 else 4 * math.pi                  # |S^(d-1)|
    g = lambda u: min(1.0, eps ** (2 * d) / math.exp(u * d)) * area * math.exp(u * d)
    s = g(a) + g(b) + sum((4 if i % 2 else 2) * g(a + i * h) for i in range(1, n))
    inner = area * eps ** (2 * d) / d                             # |t| <= eps^2, where min(...) = 1
    return inner + s * h / 3


def check_radial():
    ok = True
    for d in (2, 3):
        area = 2 * math.pi if d == 2 else 4 * math.pi
        for e in (1e-1, 1e-2, 1e-3):
            closed = area * e ** (2 * d) * (1 / d + math.log(1.0 / e ** 2))
            ok &= abs(radial(e, 1.0, d) - closed) <= 1e-6 * closed
    return ok


def check_lambda():
    ok = True
    A = 12.0
    for d in (2, 3):
        cap_d = 2 if MUT == "planar-cap" else d
        for k in (2 ** 10, 2 ** 20, 2 ** 40):
            L = k * math.log(2)
            base = L if MUT == "drop-loglog" else L / math.log(L)
            lam = (A * base) ** cap_d
            lhs = lam ** (1.0 / d) * math.log(lam)
            ok &= lhs >= A * L
            if MUT != "drop-loglog":
                ok &= lam <= (A * L / math.log(L)) ** d * 1.000001   # the claimed size, no larger
            else:
                ok &= lam <= (A * L / math.log(L)) ** d
    return ok


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    checks = {"SQUARE": check_square(), "SHELL": check_shell(), "REMAINDER": check_remainder(),
              "EXPONENTS": check_exponents(), "LOGEPS": check_logeps(), "RADIAL": check_radial(),
              "LAMBDA": check_lambda()}
    passed = all(checks.values()) and len(checks) == 7
    print(json.dumps({"object": "CL-C6-SHARPENED-20260929-v1", "checks": checks, "passed": passed,
                      "scope": "finite identities, exponent bookkeeping and quadratures only; the proof is PROOF.md"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
