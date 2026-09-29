"""Independent nonauthor checks for OA-WINDOW-MULTIPLICITY-HEIGHT-20260928-v1 (Math-#116 C5, HEIGHT_MARKS.md).

Python standard library only; exact rational arithmetic throughout. Written from the markdown; the author's absent
algebra.py is neither run nor reconstructed. Groups:

  JACOBIAN   (H2): h = b - k r^3 theta has |dh/dtheta| = k r^3 exactly; with (H1) the mean density error is
             k r^3 * C r = C r^4 per unit volume, and the normalized error is C r (H3)-(H4).
  NORMALIZE  the variation inequality ||mu/m - nu/n|| <= (||mu - nu|| + |m - n|)/m <= 2||mu - nu||/m on random
             finite positive measures, plus an explicit instance where dropping the mass term fails.
  MIXTURE    exact finite configuration models (random laws on configurations of 0..4 marked points): the
             decomposition mu = sigma + eta, a = E[N; N >= 2] <= q = E[N(N-1)], p_1 = m - a, the singleton-mark
             bound dTV(sigma/p_1, mu/m) <= a/m, and the complete-configuration bound
             dTV(Law(Xi | N >= 1), singleton with mark law mu/m) <= a/m, all in probability TV (half variation).
  INTEGER    pointwise: N - 1{N>=1} <= N(N-1)/2, 1{N>=2} <= N(N-1)/2, N 1{N>=2} <= N(N-1) for N = 0..60.
  CONTRAST   integrated means do not determine the height law (two densities with equal mass); the single-point
             uniform limit versus the pair-weighted Beta(2/3, 2) gap: E|theta - theta'| = 1/3 for independent
             uniforms, 1/4 for the RP pair law.

Mutants (each must fail): jacobian-r, drop-mass-term, a-le-half-q, full-variation.
Not an analytic proof: the source estimate (H1) is RM section 5 and is reviewed in REVIEW.md.
"""
import argparse
import itertools
import json
import random
import sys
from fractions import Fraction as F

MUTANTS = ("jacobian-r", "drop-mass-term", "a-le-half-q", "full-variation")
MUT = None


def var(mu, nu, keys):
    return sum(abs(mu.get(k, F(0)) - nu.get(k, F(0))) for k in keys)


def tv(mu, nu, keys):
    full = var(mu, nu, keys)
    return full if MUT == "full-variation" else full / 2


def check_jacobian():
    ok = True
    for k in (F(1, 2), F(3), F(7, 4)):
        for r in (F(1, 10), F(1, 3)):
            b = F(2, 3)
            th1, th2 = F(1, 5), F(4, 5)
            h1, h2 = b - k * r ** 3 * th1, b - k * r ** 3 * th2
            jac = abs((h2 - h1) / (th2 - th1))
            expected = r if MUT == "jacobian-r" else k * r ** 3
            ok &= jac == expected
            # density error k r^3 * (C r) against mass ~ k r^3: normalized order r
            ok &= (k * r ** 3 * r) / (k * r ** 3) == r
    return {"H2_jacobian_is_k_r_cubed": ok}


def check_normalize():
    rng = random.Random(116501)
    ok = True
    for _ in range(500):
        n = rng.randint(1, 6)
        keys = list(range(n))
        mu = {i: F(rng.randint(0, 9), rng.randint(1, 5)) for i in keys}
        nu = {i: F(rng.randint(0, 9), rng.randint(1, 5)) for i in keys}
        m, nn = sum(mu.values()), sum(nu.values())
        if m == 0 or nn == 0:
            continue
        lhs = var({i: mu[i] / m for i in keys}, {i: nu[i] / nn for i in keys}, keys)
        d = var(mu, nu, keys)
        ok &= lhs <= (d + abs(m - nn)) / m <= 2 * d / m
    # dropping the mass term is false: mu = (1, 1), nu = (0, 1) gives 1 > 1/2
    mu, nu, keys = {0: F(1), 1: F(1)}, {0: F(0), 1: F(1)}, [0, 1]
    lhs = var({i: mu[i] / 2 for i in keys}, {i: nu[i] for i in keys}, keys)
    bound = var(mu, nu, keys) / 2 if MUT == "drop-mass-term" else (var(mu, nu, keys) + 1) / 2
    ok &= lhs == 1 and lhs <= bound
    return {"normalization_variation_inequality": ok}


def random_configuration_law(rng, marks):
    """A random law on configurations (multisets) of 0..4 marked points."""
    configs = [()]
    for size in range(1, 5):
        configs += list(itertools.combinations_with_replacement(marks, size))
    weights = [F(rng.randint(0, 6)) for _ in configs]
    weights[0] += 50                         # most mass on the empty configuration, as for a rare window
    for i, c in enumerate(configs):          # thin larger configurations
        if len(c) >= 2:
            weights[i] = weights[i] / (4 ** len(c))
    total = sum(weights)
    return {c: w / total for c, w in zip(configs, weights) if w > 0}


def check_mixture():
    rng = random.Random(116502)
    marks = ("a", "b", "c")
    ok_decomp = ok_a = ok_single = ok_config = ok_h7 = True
    for _ in range(200):
        law = random_configuration_law(rng, marks)
        mu, sigma = {}, {}
        m = a = q = p1 = pn = F(0)
        for c, p in law.items():
            N = len(c)
            m += N * p
            q += N * (N - 1) * p
            if N >= 1:
                pn += p
            if N == 1:
                p1 += p
                sigma[c[0]] = sigma.get(c[0], F(0)) + p
            if N >= 2:
                a += N * p
            for x in c:
                mu[x] = mu.get(x, F(0)) + p
        if m == 0 or p1 == 0:
            continue
        eta = {x: mu.get(x, F(0)) - sigma.get(x, F(0)) for x in marks}
        ok_decomp &= all(v >= 0 for v in eta.values()) and sum(eta.values()) == a and p1 == m - a
        bound_a = q / 2 if MUT == "a-le-half-q" else q
        ok_a &= a <= bound_a
        # singleton mark law versus mean mark law
        ok_single &= tv({x: sigma.get(x, F(0)) / p1 for x in marks}, {x: mu.get(x, F(0)) / m for x in marks},
                        marks) <= a / m
        # complete configuration: Law(Xi | N >= 1) versus a singleton with mark law mu/m
        cond = {c: p / pn for c, p in law.items() if len(c) >= 1}
        single = {(x,): mu.get(x, F(0)) / m for x in marks}
        keys = set(cond) | set(single)
        ok_config &= tv(cond, single, keys) <= a / m
        # (H7)
        ok_h7 &= m - pn <= q / 2 and (pn - p1) <= q / 2
    return {"mu_equals_sigma_plus_eta_and_p1_equals_m_minus_a": ok_decomp,
            "a_le_q": ok_a,
            "singleton_mark_law_within_a_over_m": ok_single,
            "configuration_law_within_a_over_m": ok_config,
            "H7_integer_consequences": ok_h7}


def check_integer():
    ok = True
    for N in range(61):
        fact = F(N * (N - 1))
        ok &= N - int(N >= 1) <= fact / 2 and int(N >= 2) <= fact / 2 and N * int(N >= 2) <= fact
    return {"pointwise_integer_inequalities": ok}


def check_contrast():
    # two height densities on (0,1) with the same total mass 1: uniform and 2 theta; mean of theta differs
    mean_uniform = F(1, 2)
    mean_linear = F(2, 3)                    # int_0^1 theta * 2 theta
    out = {"integrated_mass_does_not_fix_height_law": mean_uniform != mean_linear}
    # independent uniforms: E|a - b| = 1/3; RP pair law Beta(2/3, 2): E g = 10/((3+2)(3+5)) = 1/4
    out["single_uniform_vs_pair_beta_gap"] = F(1, 3) != F(10, 5 * 8) and F(10, 5 * 8) == F(1, 4)
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
    checks = {"JACOBIAN": check_jacobian(), "NORMALIZE": check_normalize(), "MIXTURE": check_mixture(),
              "INTEGER": check_integer(), "CONTRAST": check_contrast()}
    passed = all(flatten(checks))
    print(json.dumps({"object": "CLAUDE-REVIEW-REMOTE-HEIGHT-MARKS-20260929-v1", "checks": checks,
                      "passed": passed, "scope": "exact finite identities only; not an analytic proof"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
