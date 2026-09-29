#!/usr/bin/env python3
# coefficient_review_check.py — exact finite controls for the nonauthor review
# CL-SIDE24-V1-REVIEW-20260929-v1 of coefficients/side24_v1 (OpenAI/ChatGPT).
# Python stdlib only; fail-closed via SystemExit; -O byte-identical.
# Mutants: --mutant M1|M2|M3 -> exit 1.
#   M1 = image constant with coefficient sum 75 instead of 76
#   M2 = claim the reference covariance floor is 1/2 (it is 8 - sqrt(58) ~ 0.384)
#   M3 = the untruncated half-moment 29/6 used as D_2 (truncation dropped)
# These verify finite identities in the note and its program (R1-R6, R8) and give an
# independent standard-library decimal evaluation of formula (1) (R7); they do not
# replace the by-hand arguments recorded in REVIEW.md. Unknown mutant labels exit 2.

import json
import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F
from math import factorial


def check(name, cond):
    if not cond:
        print("FAIL " + name)
        raise SystemExit(1)


def bernoulli_list(nmax):
    """B_0..B_nmax by the Akiyama-Tanigawa algorithm (exact; B_1 = +1/2 convention)."""
    A = [F(0)] * (nmax + 1)
    out = []
    for mm in range(nmax + 1):
        A[mm] = F(1, mm + 1)
        for j in range(mm, 0, -1):
            A[j - 1] = j * (A[j - 1] - A[j])
        out.append(A[0])
    return out


def dfact(n):
    out = 1
    while n > 1:
        out *= n
        n -= 2
    return out


def main(argv):
    mutant = None
    if len(argv) == 3 and argv[1] == "--mutant":
        mutant = argv[2]
        if mutant not in ("M1", "M2", "M3"):
            print("FAIL unknown mutant " + mutant)
            raise SystemExit(2)
    elif len(argv) != 1:
        raise SystemExit(2)
    res = {}

    # ---- R1: Hermite/pairing coefficient sums for q <= 6 -------------------------
    # |d^q phi| <= phi * sum_j q!/(2^j j! (q-2j)!) |x|^{q-2j}; sums and zero values
    sums = {}
    for q in range(7):
        sums[q] = sum(factorial(q) // (2 ** j * factorial(j) * factorial(q - 2 * j)) for j in range(q // 2 + 1))
    check("R1_sum_q6_is_76", sums[6] == (75 if mutant == "M1" else 76) and sums[6] == 1 + 15 + 45 + 15)
    check("R1_sums_le_76", all(sums[q] <= 76 for q in range(7)))
    check("R1_zero_value_le_15", all(dfact(q - 1) <= 15 for q in range(0, 7, 2)))  # (q-1)!! at x=0
    res["R1_hermite_sums"] = {str(q): sums[q] for q in range(7)}

    # ---- R2: lattice counting and the geometric ratio ---------------------------
    for j in range(1, 60):
        shell = (2 * j + 1) ** 3 - (2 * j - 1) ** 3          # points with max-coordinate exactly j
        check("R2_shell_count", shell == 24 * j * j + 2 and shell <= 27 * j ** 3)
        check("R2_norm6_bound", (3 * j * j) ** 3 == 27 * j ** 6)
    # successive-term ratio of j^9 e^{-288 j^2}: ((j+1)/j)^9 e^{-288(2j+1)} <= 2^9 e^{-864} < 1/2
    # since e^{864} > 2^{864} > 2^{10}
    check("R2_ratio", 2 ** 9 * 2 ** -864 < F(1, 2) and 2 ** 864 > 1024)
    res["R2_lattice"] = "shell count 24j^2+2 <= 27j^3; |n|^6 <= 27 j^6; term ratio <= 512 e^-864 < 1/2 -> sum <= 1458 e^-288"

    # ---- R3: image ledger arithmetic -------------------------------------------
    exp_lower = sum((F(288, 125) ** k / factorial(k) for k in range(21)), F(0))
    check("R3_exp_288_over_125_gt_10", exp_lower > 10)
    ic = 1458 * (76 * 24 ** 6 + 15)
    check("R3_image_constant", ic == 21175738586478 and 24 ** 6 == 191102976)
    E = F(ic, 10 ** 125)
    check("R3_60E_below_eps", 60 * E < F(1, 10 ** 108))
    check("R3_32eps_below_1e-106", 32 * F(1, 10 ** 108) < F(1, 10 ** 106))
    # e^{-288} < 10^{-125} follows from e^{288/125} > 10 (125th power)
    check("R3_e288_bound_logic", exp_lower ** 125 > 10 ** 125)
    res["R3_image_ledger"] = {"E": "21175738586478e-125", "60E": "<1e-108", "32eps": "<1e-106"}

    # ---- R4: reference covariance eigenvalue floor ------------------------------
    # svec Hessian block at d=3: Cov = 2 I_6 + J on the 3 diagonal entries -> eigenvalues 5 (once), 2 (five)
    n = 6
    C = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        C[i][i] = F(2)
    for i in range(3):
        for j in range(3):
            C[i][j] += 1                     # Cov(H_ii, H_jj) = 1 + 2 delta_ij
    def matvec(M, v):
        return [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]
    v_trace = [F(1), F(1), F(1), F(0), F(0), F(0)]
    check("R4_trace_eigen_d+2", matvec(C, v_trace) == [5 * x for x in v_trace])
    for v in ([F(1), F(-1), F(0), F(0), F(0), F(0)], [F(1), F(1), F(-2), F(0), F(0), F(0)],
              [F(0), F(0), F(0), F(1), F(0), F(0)], [F(0), F(0), F(0), F(0), F(1), F(0)], [F(0)] * 5 + [F(1)]):
        check("R4_traceless_eigen_2", matvec(C, v) == [2 * x for x in v])
    # odd block [[1,-3],[-3,15]]: eigenvalues 8 +/- sqrt(58); smaller > 1/3 (shift by 1/3 -> PD)
    floor = F(1, 2) if mutant == "M2" else F(1, 3)
    a11, a12, a22 = F(1) - floor, F(-3), F(15) - floor
    check("R4_odd_block_floor", a11 > 0 and a11 * a22 - a12 * a12 > 0)
    check("R4_odd_block_exact_minors", (F(2, 3), F(7, 9)) == (F(1) - F(1, 3), (F(2, 3)) * (F(44, 3)) - 9))
    # numeric: 8 - sqrt(58) ~ 0.3844 > 1/3
    check("R4_numeric_floor", 8 - math.sqrt(58) > 1 / 3)
    res["R4_covariance_floor"] = "Hessian block eigen {5, 2,2,2,2,2}; odd block min eigen 8-sqrt(58)=0.384 > 1/3; gradients 1 -> C_ref >= I/3"

    # ---- R5: density-comparison exponents and the 1 +/- 32 eps bracket ---------
    eps = F(1, 10 ** 108)
    for d in (2, 3):
        m = d - 1
        nn = m * (m + 1) // 2
        a = F(m) + F(2, 3) + F(nn, 2)
        b = F(d) + F(nn, 2)
        check("R5_exponent_sums_d%d" % d, a + 2 * b < 14 and 2 * a + b < 13 and a <= 5 and b <= 5)
    up = (1 + eps) ** 5 / (1 - eps) ** 5
    lo = (1 - eps) ** 5 / (1 + eps) ** 5
    check("R5_upper_bracket", up <= 1 + 32 * eps)
    check("R5_lower_bracket", lo >= 1 - 32 * eps)
    res["R5_density_comparison"] = "a=m+2/3+n/2, b=d+n/2 (<=5 for d=2,3); (1+eps)^5/(1-eps)^5 <= 1+32eps exactly at eps=1e-108"

    # ---- R6: cone moments --------------------------------------------------------
    # s ~ N(0,5/3): E s^2 = 5/3, E s^4 = 3 (5/3)^2 = 25/3 ; R^2 ~ Exp(1/2): E=2, E^2=8
    Es2, Es4 = F(5, 3), 3 * F(5, 3) ** 2
    check("R6_s_moments", Es2 == F(5, 3) and Es4 == F(25, 3))
    ER2, ER4 = F(2), F(8)
    untrunc_half = (Es4 - 2 * Es2 * ER2 + ER4) / 2
    check("R6_untruncated_half_29_6", untrunc_half == F(29, 6))
    # kernel identity int_0^a (a-z)^2 e^{-z/2} dz/2 = a^2 - 4a + 8 - 8 X, X = e^{-a/2}, by formal
    # differentiation (X' = -X/2): RHS'' = 2 - 2X = LHS'' ; RHS(0)=0, RHS'(0)=0
    # represent as (poly coeffs in a, coefficient of X): RHS = (a^2 - 4a + 8) + (-8) X
    poly, cX = [F(8), F(-4), F(1)], F(-8)                # poly[k] = coeff of a^k
    d1_poly = [poly[1], 2 * poly[2]]; d1_X = cX * F(-1, 2)    # (-4 + 2a) + 4X
    d2_poly = [d1_poly[1]]; d2_X = d1_X * F(-1, 2)            # 2 + (-2)X
    check("R6_kernel_second_derivative", d2_poly == [F(2)] and d2_X == F(-2))
    check("R6_kernel_initial_values", poly[0] + cX == 0 and d1_poly[0] + d1_X == 0)
    # E e^{-s^2/2} = (1 + 5/3)^{-1/2} = sqrt(3/8): (sqrt(3/8))^2 = 3/8 = 1/(8/3)
    check("R6_gauss_expectation", F(3, 8) == 1 / (1 + F(5, 3)))
    # D_2 = (1/2)[25/3 - 20/3 + 8] - 8 * (1/2) * sqrt(3/8) = 29/6 - 4 sqrt(3/8) ; (4 sqrt(3/8))^2 = 6
    D2_rational_part = (F(25, 3) - F(20, 3) + 8) / 2
    check("R6_D2_rational_part", D2_rational_part == F(29, 6))
    check("R6_D2_sqrt_part", 16 * F(3, 8) == 6)
    D2_num = 29 / 6 - math.sqrt(6)
    if mutant == "M3":
        D2_num = 29 / 6
    check("R6_D2_numeric", abs(D2_num - 2.383843590550155) < 1e-12)
    # D_1 = E[A^2 1{A<0}] for A ~ N(0, 8/3) = (1/2)(8/3) = 4/3
    check("R6_D1", F(1, 2) * F(8, 3) == F(4, 3))
    res["R6_cone_moments"] = {"D_1": "4/3", "D_2": "29/6 - sqrt(6)", "untruncated_half": "29/6 (control)"}

    # ---- R7: eq. (1) is the closed form of the parent specialization; independent numerics -
    check("R7_cube_identity", F(36, 24) == F(3, 2))                    # (3/2)^{1/3} = 6^{2/3}/24^{1/3}
    check("R7_gamma_prefactor", F(144 ** 3, 12 ** 7 * 2) == F(1, 24))   # (144 12^{-7/3} 2^{-1/3})^3 = 1/24
    g76 = math.gamma(7 / 6)
    c3 = g76 * 1.5 ** (1 / 3) * D2_num / (2 * math.sqrt(3) * math.pi ** 2.5)
    c2 = g76 * 1.5 ** (1 / 3) * (4 / 3) / (2 * math.sqrt(3) * math.pi ** 1.5)
    check("R7_c3_inside_enclosure", 0.04177593184059834334 - 2e-16 < c3 < 0.04177593184059834335 + 2e-16)
    check("R7_c2_inside_enclosure", 0.07340691930603427103 - 2e-16 < c2 < 0.07340691930603427104 + 2e-16)
    # Independent evaluation of (1) with the standard-library decimal module: Stirling for
    # log Gamma at z = 7/6 + 120 with B_2..B_40 (remainder < 1e-70 by DLMF 5.11(ii)), own Machin pi.
    # This is a different shift (120 vs the package's 32) and a different arithmetic (decimal vs
    # rational intervals). Digits beyond the remainder bound are not claimed.
    getcontext().prec = 90
    Bn = bernoulli_list(42)
    def atan_inv(n):
        x = Decimal(1) / Decimal(n); x2 = x * x; term = x; tot = Decimal(0); k = 0
        while abs(term) > Decimal(10) ** -95:
            tot += term / (2 * k + 1) * (-1) ** k; term *= x2; k += 1
        return tot
    pi_d = 16 * atan_inv(5) - 4 * atan_inv(239)
    z0 = Decimal(7) / 6; shift = 120; K = 20; z = z0 + shift
    lg = (z - Decimal(1) / 2) * z.ln() - z + (2 * pi_d).ln() / 2
    for k in range(1, K + 1):
        b = Bn[2 * k]
        lg += Decimal(b.numerator) / Decimal(b.denominator) / (Decimal(2 * k * (2 * k - 1)) * z ** (2 * k - 1))
    b = Bn[2 * K + 2]
    rem = abs(Decimal(b.numerator) / Decimal(b.denominator) / (Decimal((2 * K + 2) * (2 * K + 1)) * z ** (2 * K + 1)))
    check("R7_stirling_remainder_tiny", rem < Decimal(10) ** -70)
    for j in range(shift):
        lg -= (z0 + j).ln()
    g_d = lg.exp()
    c2_d = g_d * (Decimal(3) / 2) ** (Decimal(1) / 3) * (Decimal(4) / 3) / (2 * Decimal(3).sqrt() * pi_d * pi_d.sqrt())
    c3_d = g_d * (Decimal(3) / 2) ** (Decimal(1) / 3) * (Decimal(29) / 6 - Decimal(6).sqrt()) / (2 * Decimal(3).sqrt() * pi_d ** 2 * pi_d.sqrt())
    check("R7_decimal_c2_in_published_endpoints", Decimal("0.07340691930603427103") < c2_d < Decimal("0.07340691930603427104"))
    check("R7_decimal_c3_in_published_endpoints", Decimal("0.04177593184059834334") < c3_d < Decimal("0.04177593184059834335"))
    # earlier clean-context 45-digit re-derivation of c_3 (2026-09-29), compared here, not just recorded
    c3_45 = Decimal("0.0417759318405983433429366654285755564666815197")
    check("R7_decimal_c3_matches_45_digit_rederivation", abs(c3_d - c3_45) < Decimal(10) ** -45)
    def trunc(x, n):
        t = str(x); i = t.index("."); return t[:i + 1 + n]
    res["R7_closed_form"] = {"c3_float": "%.17g" % c3, "c2_float": "%.17g" % c2,
                            "gamma_7_6_decimal_60": trunc(g_d, 60), "c2_decimal_60": trunc(c2_d, 60),
                            "c3_decimal_60": trunc(c3_d, 60),
                            "independent_45_digit": str(c3_45) + " (clean-context re-derivation, 2026-09-29; matched to 1e-45)"}

    # ---- R8: Bernoulli numbers used in the Stirling expansion --------------------
    B = [F(1, 6), F(-1, 30), F(1, 42), F(-1, 30), F(5, 66), F(-691, 2730), F(7, 6), F(-3617, 510),
         F(43867, 798), F(-174611, 330), F(854513, 138)]
    # recompute B_{2k} from the Akiyama-Tanigawa algorithm (exact)
    Bt = bernoulli_list(22)
    check("R8_bernoulli_2_to_22", [Bt[2 * k] for k in range(1, 12)] == B)
    check("R8_B22_positive_first_omitted", B[10] > 0)
    res["R8_stirling"] = "B_2..B_22 exact; first omitted term positive (DLMF 5.11(ii) sign)"

    print(json.dumps({"object": "CL-SIDE24-V1-REVIEW-20260929-v1-CHECKS",
                      "scope": "finite identities of the coefficient note and its program; by-hand items in REVIEW.md",
                      "results": res, "passed": True}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv)
