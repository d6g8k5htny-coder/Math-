#!/usr/bin/env python3
# remainder_check.py — exact finite controls for CL-SIDE24-PERIODIZATION-REMAINDER-20260929-v1.
# Python stdlib only; fail-closed via SystemExit; -O byte-identical. Mutants: --mutant M1|M2|M3 -> exit 1.
#   M1 = wrong section-scaling exponent (forgets the free t coordinate: n_free = 3 instead of 4)  [code: 0 + 3]
#   M2 = wrong sign of the y^T Delta C^{-1} Delta y term in the second Gaussian derivative
#   M3 = wrong calculus majorant sup x^k e^{-x/4} = (2k/e)^k instead of (4k/e)^k
# Unknown mutant labels exit 2. These verify the finite identities and the numerical constants of
# PROOF.md; the Gaussian/analytic steps are recorded there and are not "verified" by this script.

import json
import math
import sys
from fractions import Fraction as F


def check(name, cond):
    if not cond:
        print("FAIL " + name)
        raise SystemExit(1)


# ---------- tiny exact polynomial-in-t helpers (lists of Fractions, index = power) ----------
def padd(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else F(0)) + (q[i] if i < len(q) else F(0)) for i in range(n)]


def pmul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def pscale(p, c):
    return [c * a for a in p]


def det3(M):  # M: 3x3 of polynomials
    def m(i, j):
        return M[i][j]
    t1 = pmul(m(0, 0), padd(pmul(m(1, 1), m(2, 2)), pscale(pmul(m(1, 2), m(2, 1)), F(-1))))
    t2 = pmul(m(0, 1), padd(pmul(m(1, 0), m(2, 2)), pscale(pmul(m(1, 2), m(2, 0)), F(-1))))
    t3 = pmul(m(0, 2), padd(pmul(m(1, 0), m(2, 1)), pscale(pmul(m(1, 1), m(2, 0)), F(-1))))
    return padd(padd(t1, pscale(t2, F(-1))), t3)


def adj3(M):  # adjugate of a 3x3 polynomial matrix
    def minor(i, j):
        rows = [r for r in range(3) if r != i]
        cols = [c for c in range(3) if c != j]
        a, b = rows
        c, d = cols
        return padd(pmul(M[a][c], M[b][d]), pscale(pmul(M[a][d], M[b][c]), F(-1)))
    A = [[None] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            A[j][i] = pscale(minor(i, j), F((-1) ** (i + j)))   # transpose of cofactors
    return A


def coef(p, k):
    return p[k] if k < len(p) else F(0)


def matvec(M, v):
    return [sum(M[i][j] * v[j] for j in range(3)) for i in range(3)]


def inv3(C):
    D = det3([[[c] for c in row] for row in C])[0]
    A = adj3([[[c] for c in row] for row in C])
    return [[A[i][j][0] / D for j in range(3)] for i in range(3)]


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

    # ---- C1: section-scaling exponent  int w phi_{sC}(0,z_free) = s^{(p + n_free - n)/2} int w phi_C
    d, m = 3, 2
    n = d + 1 + d * (d + 1) // 2                       # 10 jet coordinates (G, t, H)
    n_free = (0 if mutant == "M1" else 1) + m * (m + 1) // 2   # t and the transverse Hessian entries
    p = F(4, 3) + 2 * m                                # degree of w = |t|^{4/3} det(A)^2 1{A<0}
    expo = (p + n_free - n) / 2
    check("C1_scaling_exponent_minus_1_3", expo == F(-1, 3) and n == 10 and n_free == 4)
    # the same exponent in d = 2 (n = 6, n_free = 2, p = 10/3)
    check("C1_scaling_exponent_d2", (F(4, 3) + 2 + 2 - 6) / 2 == F(-1, 3))
    # Euler homogeneity: d/ds F(sC)|_{s=1} = -F/3 and dF[C](C) = (1/2) int w phi (q - n)  ->  int w phi q = (n - 2/3) F = (p + n_free) F
    check("C1_first_section_moment_28_3", n - F(2, 3) == p + n_free == F(28, 3))
    res["C1"] = "int w phi_{sC} = s^{-1/3} int w phi_C for d = 3 (and d = 2); exact first section moment int w phi q = (28/3) F"

    # ---- C2: c = 96^{-1/3} int_{S^2} F(C_u) dsigma, and the reference value is formula (1)
    check("C2_kappa_prefactor", 4 * 24 == 96)          # kappa Gamma(7/6)/(24^{1/3} sqrt pi) = 2^{-2/3} 24^{-1/3}
    check("C2_reference_recovers_eq1", F(144, 96) == F(3, 2))   # 96^{-1/3} 6^{2/3} 2^{2/3} = (3/2)^{1/3}
    g76 = math.gamma(7 / 6)
    kappa = math.sqrt(math.pi) / (2 ** (2 / 3) * g76)
    check("C2_kappa_times_prefactor_numeric", abs(kappa * g76 / (24 ** (1 / 3) * math.sqrt(math.pi)) - 96 ** (-1 / 3)) < 1e-15)
    # E|N(0,1)|^{4/3} = 2^{2/3} Gamma(7/6)/sqrt(pi): Simpson quadrature of 2 int_0^40 x^{4/3} phi(x) dx
    N = 400000
    h = 40 / N
    tot = 0.0
    for i in range(N + 1):
        x = i * h
        wgt = 1 if i in (0, N) else (4 if i % 2 else 2)
        tot += wgt * x ** (4 / 3) * math.exp(-x * x / 2)
    quad = 2 * tot * h / 3 / math.sqrt(2 * math.pi)
    check("C2_abs_moment_4_3_numeric", abs(quad - 2 ** (2 / 3) * g76 / math.sqrt(math.pi)) < 1e-9)
    res["C2"] = "c_d = 96^{-1/3} int F(C_u) dsigma (kappa identity and E|N|^{4/3} checked numerically); at C_ref this is coefficients/side24_v1 eq. (1)"

    # ---- C3: Gaussian directional derivatives, exact rational check on a 3x3 example
    # log phi_{C_t}(z) = const - (1/2) log det C_t - (1/2) q_t,  C_t = C + t Delta,  q_t = z^T C_t^{-1} z,  y = C^{-1} z
    # claims:  (log det)' = tr(C^{-1} Delta),  (log det)'' = -tr(C^{-1} Delta C^{-1} Delta),
    #          q' = -y^T Delta y,               q'' = +2 y^T Delta C^{-1} Delta y      (all at t = 0)
    C = [[F(3), F(1), F(0)], [F(1), F(2), F(1, 2)], [F(0), F(1, 2), F(4)]]          # SPD
    Dl = [[F(1, 3), F(-1), F(2)], [F(-1), F(0), F(1, 5)], [F(2), F(1, 5), F(-1)]]  # symmetric
    z = [F(1), F(-2), F(3, 2)]
    Ct = [[[C[i][j], Dl[i][j]] for j in range(3)] for i in range(3)]                # polynomials in t
    Dp = det3(Ct)
    Ap = adj3(Ct)
    d0, d1, d2 = coef(Dp, 0), coef(Dp, 1), 2 * coef(Dp, 2)
    Ci = inv3(C)
    CiD = [[sum(Ci[i][k] * Dl[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    trCiD = sum(CiD[i][i] for i in range(3))
    check("C3_logdet_first", d1 / d0 == trCiD)
    CiDCiD = [[sum(CiD[i][k] * CiD[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    tr2 = sum(CiDCiD[i][i] for i in range(3))
    check("C3_logdet_second", (d2 * d0 - d1 * d1) / (d0 * d0) == -tr2)
    # q_t = z^T adj(C_t) z / det(C_t): numerator polynomial N(t)
    Nz = [F(0)]
    for i in range(3):
        for j in range(3):
            Nz = padd(Nz, pscale(Ap[i][j], z[i] * z[j]))
    n0, n1, n2 = coef(Nz, 0), coef(Nz, 1), 2 * coef(Nz, 2)
    y = matvec(Ci, z)
    yDy = sum(y[i] * Dl[i][j] * y[j] for i in range(3) for j in range(3))
    Dy = matvec(Dl, y)
    CiDy = matvec(Ci, Dy)
    yDCiDy = sum(Dy[i] * CiDy[i] for i in range(3))
    q1 = (n1 * d0 - n0 * d1) / (d0 * d0)
    q2 = (n2 * d0 * d0 - n0 * d2 * d0 - 2 * n1 * d1 * d0 + 2 * n0 * d1 * d1) / (d0 ** 3)
    check("C3_q_first", q1 == -yDy)
    sign = F(-1) if mutant == "M2" else F(1)
    check("C3_q_second", q2 == sign * 2 * yDCiDy)
    # hence (log phi)' = a/2 with a = y^T Delta y - tr(C^{-1} Delta) and
    #       phi''/phi = a^2/4 - y^T Delta C^{-1} Delta y + tr(C^{-1} Delta C^{-1} Delta)/2
    res["C3"] = "phi''/phi = a^2/4 - y'Delta C^-1 Delta y + tr(C^-1 Delta C^-1 Delta)/2, a = y'Delta y - tr(C^-1 Delta); exact 3x3 check"

    # ---- C4: sup_{x>=0} x^k e^{-x/4} = (4k/e)^k, attained at x = 4k (rational e bounds)
    e_lo, e_hi = F(27182, 10000), F(27183, 10000)
    factor = 2 if mutant == "M3" else 4
    for k in (1, 2):
        sup_claim_upper = F(factor * k) ** k / e_lo ** k          # rational upper bound for (4k/e)^k
        # grid sanity: x^k e^{-x/4} <= claimed sup on a grid, using e^{x/4} >= sum of the Taylor series (lower bound)
        for xi in range(0, 400):
            x = F(xi, 10)
            ex_lower = sum((x / 4) ** j / math.factorial(j) for j in range(40))   # Taylor partial sum < e^{x/4}
            # x^k e^{-x/4} < x^k / ex_lower; the latter must stay below the claimed sup (1e-6 grid tolerance)
            check("C4_grid_k%d" % k, x ** k <= sup_claim_upper * ex_lower * (1 + F(1, 10 ** 6)))
        # the value at x = 4k is (4k/e)^k: the sup is attained there (derivative (k - x/4) x^{k-1} e^{-x/4} vanishes)
        check("C4_attained_at_4k", F(4 * k) ** k / e_hi ** k <= sup_claim_upper)
    res["C4"] = "x^k e^{-x/4} <= (4k/e)^k, k = 1, 2; hence int w phi_C q^k <= (4k/e)^k 2^{n/2} int w phi_{2C}"

    # ---- C5: lambda_min(C_ref) in raw coordinates: odd block [[1,-3],[-3,15]] (+) I_2, even block (2I+J on the
    #      three diagonal Hessian entries; variance 1 on the three off-diagonal entries): minimum 8 - sqrt(58) > 1/3
    check("C5_odd_block_minors", F(1) - F(1, 3) > 0 and (F(1) - F(1, 3)) * (F(15) - F(1, 3)) - 9 > 0)
    check("C5_8_minus_sqrt58_gt_1_3_exact", F(23, 3) ** 2 > 58 and 529 > 522)        # 8 - sqrt(58) > 1/3  <=>  (23/3)^2 > 58
    check("C5_8_minus_sqrt58_lt_1_exact", F(7) ** 2 < 58)                            # 8 - sqrt(58) < 1
    # even block: 2I_3 + J_3 on the diagonal Hessian entries (eigenvalues 5, 2, 2), I_3 on the off-diagonal ones
    Jm = [[F(2) + 1 if i == j else F(1) for j in range(3)] for i in range(3)]
    mv = lambda M, v: [sum(M[i][j] * v[j] for j in range(3)) for i in range(3)]
    check("C5_even_block_trace_eigen_5", mv(Jm, [F(1)] * 3) == [F(5)] * 3)
    check("C5_even_block_traceless_eigen_2", mv(Jm, [F(1), F(-1), F(0)]) == [F(2), F(-2), F(0)] and mv(Jm, [F(1), F(1), F(-2)]) == [F(2), F(2), F(-4)])
    # the remaining eigenvalues (1 on G_2, G_3 and on the three off-diagonal Hessian entries) exceed 8 - sqrt(58) < 1
    check("C5_lambda_min_numeric", 8 - math.sqrt(58) > 1 / 3 and 8 - math.sqrt(58) < 1)
    res["C5"] = "raw C_ref spectrum: {8 +/- sqrt(58), 1, 1} (odd) and {5, 2, 2, 1, 1, 1} (even); lambda_min = 8 - sqrt(58) > 1/3 (exact: 529 > 522)"

    # ---- C6: the constants of the second-order bound
    E = F(21175738586478, 10 ** 125)                       # side24_v1 image bound, per entry, every frame
    delta = 10 * E                                          # ||Delta||_F <= 10 E for a 10x10 matrix with entries < E
    A_up = F(253985, 10000)                                 # 2^{14/3} < 25.3985
    check("C6_two_pow_14_3", A_up ** 3 > 2 ** 14)
    M1 = F(4) / e_lo * A_up                                 # (4/e) 2^{14/3}
    M2 = (F(8) / e_lo) ** 2 * A_up                          # (8/e)^2 2^{14/3}
    bracket = (M2 + 2 * n * M1 + n * n) / 4 + M1 + F(n, 2)
    check("C6_bracket_below_310", bracket < F(310))
    lam_inv2 = 1 / (F(1, 3) - delta) ** 2
    Ft_ratio = 1 + 32 * 3 * delta                           # F(C_t) <= (1 + 32 eps') F_ref, eps' = 3 delta
    K = bracket * lam_inv2 * Ft_ratio / 2
    check("C6_K_below_1393", K < F(1393))
    second = K * delta * delta
    check("C6_second_order_below_6_3e-219", second < F(63, 10 ** 220))
    res["C6"] = {"bracket": "%.4f" % float(bracket), "K": "%.2f" % float(K), "delta": "10 E = %.4e" % float(delta),
                 "second_order_relative": "< %.3e" % float(F(63, 10 ** 220))}

    # ---- C7: first-order rest (normalizer q^2 terms of the first shell, deeper shells) is negligible
    ten_m125 = F(1, 10 ** 125)                             # e^{-288} < 10^{-125}  (side24_v1, e^{288/125} > 10)
    e_576 = ten_m125 ** 2                                   # e^{-576} < 10^{-250}
    c76 = 76 * 24 ** 6 + 15
    first_shell_norm = 42 * c76 * e_576                     # |6-sum - 6q D^q phi(0)| (1/S - 1) <= 6 q c76 * 7 q  (S - 1 <= 7q)
    shell2 = 20 * 76 * (24 ** 6) * 27 * e_576 + 20 * 15 * e_576   # |n|^2 in {2,3}: 20 points, |n|^6 <= 27, e^{-288|n|^2} <= e^{-576}
    tail = 729 * c76 * 2 * (2 ** 9) * ten_m125 ** 4        # j >= 2 shells: <= 729 c76 sum_{j>=2} j^9 e^{-288 j^2} <= 729 c76 * 2 * 512 e^{-1152}
    entry_rest = first_shell_norm + shell2 + tail
    delta_rest = 10 * entry_rest
    dF_norm = F(3, 2) * (M1 + n)                            # ||dF[C_ref]|| <= (1/2) lambda^{-1} (M1 + n) F_ref, lambda >= 1/3
    first_rest = dF_norm * delta_rest
    check("C7_first_order_rest_below_1e-234", first_rest < F(1, 10 ** 234))
    total = second + first_rest
    check("C7_total_below_1e-218", total < F(1, 10 ** 218))
    res["C7"] = {"entry_rest": "< %.3e" % float(entry_rest), "first_order_rest_relative": "< %.3e" % float(first_rest),
                 "total_epsilon": "< 1e-218"}

    # ---- C8: the leading term dominates the remainder by more than 10^99
    P3 = lambda L: -F(L * L) * (10 * L ** 4 - 147 * L * L + 315) / 105
    check("C8_P3_24", P3(24) == F(-620813376, 35))
    q_lower = 1 / e_hi ** 288                               # e^{-288} > (27183/10000)^{-288}
    check("C8_q_lower_above_1e-126", q_lower > F(1, 10 ** 126))
    check("C8_leading_over_remainder", abs(P3(24)) * q_lower > F(1, 10 ** 118) and F(1, 10 ** 118) == 10 ** 100 * F(1, 10 ** 218))
    res["C8"] = "P_3(24) = -620813376/35; |P_3(24)| e^{-288} > 1e-118 = 1e100 * 1e-218: the leading term exceeds the remainder bound by > 10^100"

    print(json.dumps({"object": "CL-SIDE24-PERIODIZATION-REMAINDER-20260929-v1-CHECKS",
                      "scope": "finite identities and constants of the second-order remainder bound; analytic steps in PROOF.md",
                      "results": res, "passed": True}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv)
