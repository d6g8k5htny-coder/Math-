#!/usr/bin/env python3
# first_variation_check.py — exact finite controls for the SIDE24 nearest-image
# first-variation candidate (object CL-SIDE24-PFV-20260929-v1).
#
# Python standard library only. Fail-closed via SystemExit (no `assert`, so
# `-O` output is byte-identical). Mutants: --mutant M1|M2|M3 -> exit 1.
#
# What this program proves is finite algebra: Hermite values, sphere-moment
# weights, the rotational projection of the six-image jet perturbation, the
# chain rule through the isotropic coefficient functional, the closed form
# P3(L), its value at L=24, and rigorous magnitude bounds. It does NOT prove
# the continuum Gaussian statements; those live in PROOF.md.

import json
import math
import sys
from fractions import Fraction as F

FAILURES = []


def check(name, cond):
    if not cond:
        FAILURES.append(name)
        print("FAIL " + name)
        raise SystemExit(1)


# ---------- exact polynomials in L (coefficient dict: degree -> Fraction) ----
def pzero():
    return {}


def padd(p, r):
    out = dict(p)
    for d, c in r.items():
        out[d] = out.get(d, F(0)) + c
        if out[d] == 0:
            del out[d]
    return out


def pscale(p, s):
    return {d: c * F(s) for d, c in p.items() if c * F(s) != 0}


def pmul(p, r):
    out = {}
    for d1, c1 in p.items():
        for d2, c2 in r.items():
            out[d1 + d2] = out.get(d1 + d2, F(0)) + c1 * c2
    return {d: c for d, c in out.items() if c != 0}


def peval(p, x):
    return sum(c * F(x) ** d for d, c in p.items())


def peq(p, r):
    return padd(p, pscale(r, -1)) == {}


# ---------- probabilists' Hermite polynomials He_k, exact ----------
def hermite(k):
    # He_0 = 1, He_1 = x, He_{n+1} = x He_n - n He_{n-1}
    hs = [{0: F(1)}, {1: F(1)}]
    while len(hs) <= k:
        n = len(hs) - 1
        hs.append(padd(pmul({1: F(1)}, hs[n]), pscale(hs[n - 1], -n)))
    return hs[k]


def dfact(n):  # double factorial of odd n (n!!), n >= -1
    out = 1
    while n > 1:
        out *= n
        n -= 2
    return out


def main(argv):
    mutant = None
    if len(argv) == 3 and argv[1] == "--mutant":
        mutant = argv[2]
    elif len(argv) != 1:
        print("usage: first_variation_check.py [--mutant M1|M2|M3]")
        raise SystemExit(2)

    results = {}

    # ---- H1: Hermite seeds and values ---------------------------------------
    seed = F(2) if mutant == "M3" else F(1)  # M3 corrupts He_1
    He = {k: hermite(k) for k in (0, 1, 2, 3, 4, 5, 6)}
    if mutant == "M3":
        He[1] = {1: seed}
        # rebuild upward with the corrupted seed
        hs = [He[0], He[1]]
        for n in range(1, 6):
            hs.append(padd(pmul({1: F(1)}, hs[n]), pscale(hs[n - 1], -n)))
        for k in range(7):
            He[k] = hs[k]
    he0 = {k: peval(He[k], 0) for k in (0, 2, 4, 6)}
    check("H1_he0", [he0[0], he0[2], he0[4], he0[6]] == [F(1), F(-1), F(3), F(-15)])
    check("H1_He2", peq(He[2], {2: F(1), 0: F(-1)}))
    check("H1_He4", peq(He[4], {4: F(1), 2: F(-6), 0: F(3)}))
    check("H1_He6", peq(He[6], {6: F(1), 4: F(-15), 2: F(45), 0: F(-15)}))
    # derivative identity spot check: (d/dz)^k e^{-z^2/2} = (-1)^k He_k(z) e^{-z^2/2}
    # verified structurally by the recurrence used; record the three values used
    results["H1_hermite"] = {"He2": "L^2-1", "He4": "L^4-6L^2+3",
                            "He6": "L^6-15L^4+45L^2-15", "at_zero": [1, -1, 3, -15]}

    # ---- H2: sphere moments on S^2 via the Gaussian factorization -----------
    # E[v1^{2a} v2^{2b} v3^{2c}] = (2a-1)!!(2b-1)!!(2c-1)!! / (2n+1)!!, n=a+b+c
    # (g = R v with R^2 ~ chi^2_3 independent of v; E chi^2_3-moments = (2n+1)!!/1)
    def smom(a, b, c):
        n = a + b + c
        return F(dfact(2 * a - 1) * dfact(2 * b - 1) * dfact(2 * c - 1),
                 dfact(2 * n + 1))

    # chi^2_3 moment recursion cross-check: E R^{2n} = prod_{j<n} (3+2j)
    for n in range(1, 4):
        prod = 1
        for j in range(n):
            prod *= (3 + 2 * j)
        check("H2_chisq_moment_n%d" % n, F(prod) == F(dfact(2 * n + 1)))
    check("H2_v2", smom(1, 0, 0) == F(1, 3))
    check("H2_v4", smom(2, 0, 0) == F(1, 5))
    check("H2_v2v2", smom(1, 1, 0) == F(1, 15))
    check("H2_v6", smom(3, 0, 0) == F(1, 7))
    check("H2_v4v2", smom(2, 1, 0) == F(1, 35))
    check("H2_v2v2v2", smom(1, 1, 1) == F(1, 105))
    # normalization: sum over |v|^2 = 1 identities
    check("H2_norm1", 3 * smom(1, 0, 0) == F(1))
    check("H2_norm2", 3 * smom(2, 0, 0) + 6 * smom(1, 1, 0) == F(1))
    check("H2_norm3", 3 * smom(3, 0, 0) + 6 * smom(2, 1, 0) * 3 + 6 * smom(1, 1, 1)
          == F(1))
    # (v1^2+v2^2+v3^2)^3: terms 3x v^6, 3*2=6 ordered pairs each multinomial 3 -> 3*smom6 + 18*smom42/... keep the
    # direct expansion: multinomial coefficients 1 (aaa), 3 (a^2b), 6 (abc):
    # 3*E v1^6 + 3*perm... expansion above verified: 3*(1/7) + 18*(1/35) + 6*(1/105) = 15/35+18/35+2/35 = 1
    results["H2_sphere_moments"] = {"v1^2": "1/3", "v1^4": "1/5", "v1^2v2^2": "1/15",
                                    "v1^6": "1/7", "v1^4v2^2": "1/35",
                                    "v1^2v2^2v3^2": "1/105"}

    # ---- H3: projection weights (directional-derivative averages) -----------
    # <d^4_v> = sum E[v_i v_j v_k v_l] d_ijkl: d_iiii weight 1/5;
    # d_iijj (i<j) has 4!/(2!2!) = 6 orderings, each E = 1/15 -> weight 6/15 = 2/5.
    w_iijj = F(1, 5) if mutant == "M1" else 6 * smom(1, 1, 0)
    check("H3_w4_iiii", smom(2, 0, 0) == F(1, 5))
    check("H3_w4_iijj", w_iijj == F(2, 5))
    # <d^6_v>: d_iiiiii weight 1/7; d_iiiijj (i!=j ordered) 6!/(4!2!) = 15 orderings,
    # each E = 1/35 -> 15/35 = 3/7; d_iijjkk 6!/(2!2!2!) = 90 orderings, E = 1/105 -> 6/7.
    check("H3_w6_i6", smom(3, 0, 0) == F(1, 7))
    check("H3_w6_i4j2", 15 * smom(2, 1, 0) == F(3, 7))
    check("H3_w6_112233", 90 * smom(1, 1, 1) == F(6, 7))
    results["H3_projection_weights"] = {"d4": ["1/5", "2/5"], "d6": ["1/7", "3/7", "6/7"]}

    # ---- H4: per-q first-order normalized 1-D moment perturbations ----------
    # dm_{2j}(L) = 2 (He_{2j}(L) - He_{2j}(0))   [coefficient of q; Z_L division included]
    dm = {2 * j: pscale(padd(He[2 * j] if 2 * j else {0: F(1)},
                             {0: -he0.get(2 * j, F(1))}), 2) for j in (1, 2, 3)}
    # ---- H5: assemble the projected radial-moment variations (per q) --------
    # per-axis / per-pair structure (six images +/- L e_i; only the matching
    # 1-D factor is perturbed at first order):
    # Per-axis perturbations of the summed (unnormalized-by-count) radial moments.
    # There are 3 axes i and, for the mixed terms, 3 unordered pairs {i,j}.
    # <d^2_v> = (1/3) sum_i d_ii ; only the axis-i image family perturbs d_ii.
    d_ii = dm[2]                                       # per axis i
    # <d^4_v> = (1/5) sum_i d_iiii + (2/5) sum_{i<j} d_iijj
    d_iiii = dm[4]                                     # per axis i
    d_iijj = pscale(pmul(dm[2], {0: he0[2]}), 2)       # per pair {i,j}: axis i OR axis j
    # <d^6_v> = (1/7) sum_i d_i^6 + (3/7) sum_{i<j, i!=j} d_i^4 d_j^2 + (6/7) d_112233
    d_i6 = dm[6]                                        # per axis i
    d_i4j2 = padd(pmul(dm[4], {0: he0[2]}),             # per ordered (i,j): axis i perturbs m4,
                  pmul({0: he0[4]}, dm[2]))             #                    axis j perturbs m2
    d_112233 = pscale(pmul(dm[2], {0: he0[2] * he0[2]}), 3)  # 3 axes each perturb one m2 factor
    avg_d2 = pscale(d_ii, F(1, 3) * 3)                            # 3 axes
    avg_d4 = padd(pscale(d_iiii, F(1, 5) * 3), pscale(d_iijj, w_iijj * 3))  # 3 axes, 3 pairs
    avg_d6 = padd(pscale(d_i6, F(1, 7) * 3),                      # 3 axes
                  padd(pscale(d_i4j2, F(3, 7) * 6),               # 6 ordered pairs
                       pscale(d_112233, F(6, 7))))                # single 112233 term
    da = pscale(avg_d2, -1)
    dm4 = avg_d4
    dchi = pscale(avg_d6, -1)
    check("H5_da", peq(da, {2: F(-2)}))                       # -2 L^2
    check("H5_dm4", peq(dm4, {4: F(6, 5), 2: F(-12)}))        # (6/5)L^4 - 12L^2
    check("H5_dchi", peq(dchi, {6: F(-6, 7), 4: F(18), 2: F(-90)}))
    results["H5_moment_variations_per_q"] = {
        "da": "-2L^2", "dm4": "(6/5)L^4-12L^2", "dchi": "-(6/7)L^6+18L^4-90L^2"}

    # ---- H6: isotropic functional exponents and the chain rule --------------
    # c proportional to Omega^{2/3} m4^{1/2} a^{-13/6}, Omega = a chi - m4^2:
    # from (15.2)-specialization factors p_G ~ a^{-3/2}, p_V ~ m4^{-3/2},
    # tau^{4/3} = (Omega/a)^{2/3}, D-scale ~ m4^2  (derivation in PROOF.md §4).
    ea = F(-3, 2) + F(-2, 3)               # a exponent  (-13/6)
    em = F(-3, 2) + F(2)                   # m4 exponent (1/2)
    eo = F(2, 3)                           # Omega exponent
    # M2 corrupts the target a-exponent to -11/6; the true value -13/6 then fails.
    target_a = F(-11, 6) if mutant == "M2" else F(-13, 6)
    check("H6_exp_a", ea == target_a)
    check("H6_exp_m4", em == F(1, 2))
    check("H6_exp_Omega", eo == F(2, 3))
    # chain at planar (a, m4, chi) = (1, 3, 15), Omega = 6:
    # dlog c = (2/3) dOmega/6 + (1/2) dm4/3 - (13/6) da = dOmega/9 + dm4/6 - (13/6) da
    check("H6_planar_weights", F(2, 3) / 6 == F(1, 9) and F(1, 2) / 3 == F(1, 6))
    dOmega = padd(padd(pscale(da, 15), dchi), pscale(dm4, -6))  # chi da + a dchi - 2 m4 dm4
    dlogc = padd(padd(pscale(dOmega, F(1, 9)), pscale(dm4, F(1, 6))),
                 pscale(da, F(-13, 6)))
    results["H6_chain"] = "dlogc = dOmega/9 + dm4/6 - (13/6) da at (1,3,15)"

    # ---- H7: the closed form P3(L) and its value at 24 -----------------------
    P3_stated = pscale(pmul({2: F(1)}, {4: F(10), 2: F(-147), 0: F(315)}), F(-1, 105))
    check("H7_P3_matches_derivation", peq(dlogc, P3_stated))
    P3_alt = {6: F(-2, 21), 4: F(7, 5), 2: F(-3)}
    check("H7_alt_form", peq(P3_stated, P3_alt))
    P324 = peval(P3_stated, 24)
    check("H7_P3_24", P324 == F(-620813376, 35))
    results["H7_P3"] = {"P3(L)": "-L^2(10L^4-147L^2+315)/105",
                       "P3(24)": "-620813376/35"}

    # ---- H8: rigorous magnitude bounds (exact big-integer arithmetic) -------
    # e > 27182818284/10^10, so e^288 > (27182818284/10^10)^288; compare 10^125.
    e_lo = F(27182818284, 10 ** 10)
    lhs = e_lo ** 288
    check("H8_exp_bound", lhs > F(10) ** 125)
    # hence e^{-288} < 10^{-125} and |P3(24)| e^{-288} < 1.8e7 * 1e-125 < 1e-117
    check("H8_linear_term_band", abs(P324) * F(10) ** -125 < F(1, 10 ** 117))
    check("H8_inside_coarse_band", F(1, 10 ** 117) < F(1, 10 ** 106))
    # informational float value of the linear term
    lin = abs(float(P324)) * math.exp(-288.0)
    check("H8_float_scale", 1.0e-118 < lin < 2.0e-118)
    results["H8_bounds"] = {"e^-288": "<1e-125 (exact rational)",
                           "|P3(24)|e^-288": "<1e-117 (exact); ~%.4e (float)" % lin,
                           "coarse_band": "1e-106 (side24_v1 (4)); linear term inside"}

    out = {
        "object": "CL-SIDE24-PFV-20260929-v1-CHECKS",
        "scope": ("finite exact controls for the nearest-image first-variation "
                  "candidate; not the Gaussian/analytic proof"),
        "results": results,
        "passed": True,
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv)
