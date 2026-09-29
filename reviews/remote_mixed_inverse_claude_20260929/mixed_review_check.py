"""Independent nonauthor checks for OA-REMOTE-MIXED-INVERSE-20260929-v1 (Math-#132, PROOF.md). Stdlib, exact rationals.

ENVELOPE  (M10)-(M11): for s >= 1 the t-window |t| < k/s^3 gives s^(1-q-3b) * s^(-3(1-b)) = s^(-2-q); dyadic-shell
          ratios decide the domain exactly: finite iff q + 3b < 2 (at 0) and q > -1 (at infinity).
OVERLAP   (M13) on exact instances (s_max a perfect power), lambda = q + 3b rational in [0, 2).
COEFF     (M14) T-exponent (4+q)/3 independent of b; (M15) 108 * 12^(-(4+q)/3) = (3/4) 12^((2-q)/3); k-exponent
          (5-q)/3 - b; (M4) D/A_{-q} = k^-b (2-q)(5-q)/((2-lambda)(5-lambda)).
HEIGHT    pushforward exponent alpha - 1, (M16), Beta(alpha, 2) mean/variance (M6), marginal mass, the correlation
          (M17) from the conditional-uniform smaller mark, and the RP values at alpha = 2/3 (1/4, 9/176, 2/7) and
          alpha = 1/3 (1/7, 7/11); the joint density alpha(alpha+1)|a-b|^(alpha-1)/2 has mass one.
FIXEDR    (M18) radial power 1 - 3b for every d; integrability iff q + 3b < 2; (M12) separated order r^(6-3b) and
          r^(1+q) after division; (M20) exponent bookkeeping for b >= b0 = 2/3.
RESIDUE   (M22): at q* = 2 - 3b the prefactor is 1/4, the 12-power b, the k-power 1, the T-power 2 - b, matching (M21).
Mutants (each must fail): beta-in-T, k-exponent, far-envelope, triangle-half, radial-ledger, residue-denominator.
"""
import argparse
import json
import sys
from fractions import Fraction as F

MUTANTS = ("beta-in-T", "k-exponent", "far-envelope", "triangle-half", "radial-ledger", "residue-denominator")
MUT = None
GRID = [(F(q), F(b)) for q in (0, F(1, 2), 1, F(3, 2)) for b in (0, F(1, 9), F(1, 6), F(1, 3), F(1, 2))]


def check_envelope():
    ok_far = ok_dom = True
    for q, b in GRID:
        far = (1 - q - 3 * b) + (-3 * (1 - b)) if MUT != "far-envelope" else (1 - q - 3 * b) - 3
        ok_far &= far == -2 - q
        lam = q + 3 * b
        n = lam.denominator * q.denominator
        near_ratio = F(2) ** (-int(n * (2 - lam))) if n * (2 - lam) >= 0 else F(2) ** int(-n * (2 - lam))
        finite = near_ratio < 1 and (-2 - q) < -1
        ok_dom &= finite == (lam < 2)
    return {"M11_far_exponent_is_minus2_minus_q": ok_far, "domain_exactly_lambda_lt_2": ok_dom}


def check_overlap():
    ok = True
    for q, b in GRID:
        lam = q + 3 * b
        if lam >= 2:
            continue
        den = lam.denominator
        for base in (2, 3):
            for tt in (F(1), F(3, 7)):
                m = F(base) ** den
                k = m ** 3 * tt
                m_2l = F(base) ** int(den * (2 - lam))                  # s_max^(2-lambda)
                lhs = k * m_2l / (2 - lam) - tt * m_2l * m ** 3 / (5 - lam)
                ok &= lhs == 3 * k * m_2l / ((2 - lam) * (5 - lam))
    return {"M13_exact": ok}


def check_coeff():
    out = {"M14_T_exponent_beta_free": all(
        (2 - b - (2 - q - 3 * b) / 3) == ((4 + q) / 3 - (b if MUT == "beta-in-T" else 0)) for q, b in GRID)}
    out["M14_T_exponent_beta_free"] &= all((2 - b - (2 - q - 3 * b) / 3) == (4 + q) / 3 for q, b in GRID)
    out["M15_constant"] = F(108) == F(3, 4) * 144 and all((2 - q) / 3 + (4 + q) / 3 == 2 for q, _ in GRID)
    kexp = lambda q, b: (5 - q - 3 * b) / 3
    out["M15_k_exponent"] = all(kexp(q, b) == (5 - q) / 3 - (0 if MUT == "k-exponent" else b) for q, b in GRID)
    # (M4): D's rational prefactor 3/(4(2-lam)(5-lam)) over RI's A_(-q) prefactor 3/(4(2-q)(5-q)), and k-exponents
    pref_D = lambda q, b: F(3) / (4 * (2 - q - 3 * b) * (5 - q - 3 * b))
    pref_A = lambda q: F(3) / (4 * (2 - q) * (5 - q))
    out["M4_ratio"] = all(pref_D(q, b) / pref_A(q) == (2 - q) * (5 - q) / ((2 - q - 3 * b) * (5 - q - 3 * b))
                          and kexp(q, b) - (5 - q) / 3 == -b for q, b in GRID if q + 3 * b < 2)
    return out


def beta_moments(a):
    m1 = a / (a + 2)
    m2 = a * (a + 1) / ((a + 2) * (a + 3))
    return m1, m2


def check_height():
    out = {}
    ok_push = ok_norm = ok_mom = ok_corr = ok_joint = True
    for q, b in GRID:
        lam = q + 3 * b
        if lam >= 2:
            continue
        a = (2 - lam) / 3
        ok_push &= (1 - lam) / 3 - F(2, 3) == a - 1                 # s^(1-lam) ds -> g^(alpha-1) dg
        ok_norm &= F(1) / a - F(1) / (a + 1) == F(1) / (a * (a + 1))  # (M16)
        m1, m2 = beta_moments(a)
        ok_mom &= m2 - m1 ** 2 == 2 * a / ((a + 2) ** 2 * (a + 3))
        E2 = F(1, 3) - m1 / 6 + m2 / 3
        Ex = F(1, 3) - m1 / 6 - m2 / 6
        corr = (Ex - F(1, 4)) / (E2 - F(1, 4))
        ok_corr &= corr == (2 - a - a * a) / (2 + a + a * a)
        # joint density alpha(alpha+1)|a-b|^(alpha-1)/2: mass = alpha(alpha+1)/2 * 2 * int_0^1 int_0^y u^(alpha-1) du dy
        half = F(1) if MUT == "triangle-half" else F(1, 2)
        ok_joint &= a * (a + 1) * half * 2 * (F(1) / (a * (a + 1))) == 1
        # marginal (alpha+1)(a^alpha+(1-a)^alpha)/2 has mass (alpha+1)/2 * 2/(alpha+1) = 1
        ok_joint &= (a + 1) / 2 * 2 / (a + 1) == 1
    m1, m2 = beta_moments(F(2, 3))
    rp = (m1 == F(1, 4) and m2 - m1 ** 2 == F(9, 176)
          and (F(1, 3) - m1 / 6 - m2 / 6 - F(1, 4)) / (F(1, 3) - m1 / 6 + m2 / 3 - F(1, 4)) == F(2, 7))
    m1b, m2b = beta_moments(F(1, 3))
    q1 = m1b == F(1, 7) and (F(1, 3) - m1b / 6 - m2b / 6 - F(1, 4)) / (F(1, 3) - m1b / 6 + m2b / 3 - F(1, 4)) == F(7, 11)
    out.update({"pushforward_exponent": ok_push, "M16_normalizer": ok_norm, "M6_variance": ok_mom,
                "M17_correlation": ok_corr, "M5_joint_and_marginal_mass_one": ok_joint,
                "RP_alpha_two_thirds_and_q1_alpha_one_third": rp and q1})
    # boundary: E G = alpha/(alpha+2) decreases to 0 as alpha -> 0
    seq = [beta_moments(F(1, 10 ** n))[0] for n in range(1, 6)]
    out["boundary_mean_gap_to_zero"] = all(seq[i + 1] < seq[i] for i in range(4)) and seq[-1] < F(1, 10 ** 5)
    return out


def check_fixedr():
    out = {}
    ok = True
    for d in range(2, 11):
        for _, b in GRID:
            extra = 0 if MUT == "radial-ledger" else -3 * b
            ok &= (d - 1) - (d + 3) + 3 + 2 + extra == 1 - 3 * b
    out["M18_radial_power_1_minus_3beta_all_d"] = ok
    out["integrable_iff_lambda_lt_2"] = all(((1 - 3 * b - q) > -1) == (q + 3 * b < 2) for q, b in GRID)
    out["M12_separated_order"] = all((6 - 3 * b) - (5 - q - 3 * b) == 1 + q for q, b in GRID)
    # (M20): for b >= b0 = 2/3 and 0 < Delta < l, Delta^-(b-b0) >= l^-(b-b0) (monotone, exponent >= 0);
    # checked on integer exponents b - b0 in {0, 1, 2}
    ok = True
    for e in (0, 1, 2):
        for Dl, l in ((F(1, 4), F(1, 2)), (F(1, 100), F(1, 3))):
            ok &= Dl < l and Dl ** -e >= l ** -e
    out["M20_monotone_comparison"] = ok
    return out


def check_residue():
    ok = True
    den = 5 if MUT == "residue-denominator" else 3
    for b in (F(0), F(1, 9), F(1, 6), F(1, 3), F(1, 2)):
        qs = 2 - 3 * b
        ok &= (5 - qs - 3 * b) == den and F(3) / (4 * den) == F(1, 4)
        ok &= (2 - qs) / 3 == b and (5 - qs) / 3 - b == 1 and (4 + qs) / 3 == 2 - b
    return {"M22_matches_M21": ok}


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
    checks = {"ENVELOPE": check_envelope(), "OVERLAP": check_overlap(), "COEFF": check_coeff(),
              "HEIGHT": check_height(), "FIXEDR": check_fixedr(), "RESIDUE": check_residue()}
    passed = all(flatten(checks))
    print(json.dumps({"object": "CLAUDE-REVIEW-REMOTE-MIXED-INVERSE-20260929-v1", "checks": checks, "passed": passed,
                      "scope": "exact finite identities only; not an analytic proof"}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
