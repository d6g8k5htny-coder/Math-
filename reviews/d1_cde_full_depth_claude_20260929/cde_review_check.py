#!/usr/bin/env python3
# cde_review_check.py — finite exact/numerical controls for the full-depth
# review of D1-C (parent Section 10), D1-D (Sections 13-14), D1-E (Section 15)
# of UNIFORM-MATRIX-CAP-LIFETIME-20260924-v1 (read with E1/E2/W1).
#
# Python standard library only. Fail-closed: any failed check raises
# SystemExit(1) via check(); no `assert` statements are used, so `-O`
# output is byte-identical. Mutants: run with --mutant M1|M2|M3 -> exit 1.
#
# These are finite algebra/implementation controls. They do NOT prove the
# continuum Gaussian estimates; the analytic review lives in REVIEW.md.

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


def det_fraction(mat):
    """Exact determinant of a square Fraction matrix by fraction-free
    Gaussian elimination with partial pivoting (exact over Q)."""
    n = len(mat)
    m = [row[:] for row in mat]
    det = F(1)
    for col in range(n):
        piv = None
        for row in range(col, n):
            if m[row][col] != 0:
                piv = row
                break
        if piv is None:
            return F(0)
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det = -det
        det *= m[col][col]
        inv = F(1) / m[col][col]
        for row in range(col + 1, n):
            factor = m[row][col] * inv
            if factor != 0:
                for k in range(col, n):
                    m[row][k] -= factor * m[col][k]
    return det


def build_T(r, d, u3_coeff=F(6)):
    """Exact matrix of the Section 3 transformation U_r = T_r O_r.
    Ordering of O_r: (f(a), f_x(a), f(c), f_x(c),
                      f_y1(a), f_y1(c), ..., f_ym(a), f_ym(c)).
    u3_coeff is 6 in the parent display (3.1); mutant M1 uses 3."""
    m = d - 1
    n = 4 + 2 * m
    T = [[F(0)] * n for _ in range(n)]
    # U0 = (f(a)+f(c))/2
    T[0][0] = F(1, 2)
    T[0][2] = F(1, 2)
    # U1 = (f(c)-f(a))/r
    T[1][0] = -F(1) / r
    T[1][2] = F(1) / r
    # U2 = (f_x(c)-f_x(a))/r
    T[2][1] = -F(1) / r
    T[2][3] = F(1) / r
    # U3 = (c6/r^2)[f_x(a)+f_x(c) - 2(f(c)-f(a))/r]
    c6 = u3_coeff / (r * r)
    T[3][0] = c6 * F(2) / r
    T[3][1] = c6
    T[3][2] = -c6 * F(2) / r
    T[3][3] = c6
    # per transverse j: Vj0=(f_yj(a)+f_yj(c))/2, Vj1=(f_yj(c)-f_yj(a))/r
    for j in range(m):
        i0 = 4 + 2 * j
        T[i0][i0] = F(1, 2)
        T[i0][i0 + 1] = F(1, 2)
        T[i0 + 1][i0] = -F(1) / r
        T[i0 + 1][i0 + 1] = F(1) / r
    return T


def main(argv):
    mutant = None
    if len(argv) == 3 and argv[1] == "--mutant":
        mutant = argv[2]
    elif len(argv) != 1:
        print("usage: cde_review_check.py [--mutant M1|M2|M3]")
        raise SystemExit(2)

    results = {}

    # ---- C1: |det T_r| = 12 r^-(d+3) exactly (parent (3.2), used in (10.1))
    u3 = F(3) if mutant == "M1" else F(6)
    c1 = []
    for d in (2, 3):
        for r in (F(1, 7), F(3, 5), F(1), F(9, 4)):
            got = abs(det_fraction(build_T(r, d, u3)))
            want = F(12) * r ** (-(d + 3))
            check("C1_detTr_d%d_r%s" % (d, r), got == want)
            c1.append([d, str(r), str(got)])
    results["C1_detTr_exact_12_r_minus_d_plus_3"] = c1

    # ---- C2: Section 10 radial power ledger sums to exactly 1 for every d
    # spatial (d-1) + height-mark 3 + pin -(d+3) + determinant-normalizer 2
    height_power = 0 if mutant == "M2" else 3
    for d in range(2, 11):
        total = (d - 1) + height_power - (d + 3) + 2
        check("C2_ledger_power_d%d" % d, total == 1)
    results["C2_radial_ledger_power"] = 1

    # ---- C3: (13.1) coercivity on an exact rational grid, r <= 1
    grid_b = [F(-3), F(-1), F(0), F(1, 2), F(2), F(5)]
    grid_k = [F(1, 10), F(1), F(3), F(10)]
    grid_r = [F(1, 10), F(1, 2), F(1)]
    for b in grid_b:
        for k in grid_k:
            for r in grid_r:
                x = b - k * r ** 3 / 2
                check("C3a", b * b <= 2 * x * x + k * k / 2)
                check("C3b", x * x + 144 * k * k >= (b * b + k * k) / 2)
    results["C3_target_coercivity_13_1"] = "grid %dx%dx%d exact" % (
        len(grid_b), len(grid_k), len(grid_r))

    # ---- C4: (11.1) lifetime pushforward, checked exactly via cubes:
    # with ell = k r^3, [r dr/d ell]^3 = 1/(27 k^2 ell)
    for r in (F(1, 5), F(2, 3), F(7, 4)):
        for k in (F(1, 3), F(1), F(8)):
            ell = k * r ** 3
            lhs_cubed = (F(1) / (3 * k * r)) ** 3
            rhs_cubed = F(1) / (27 * k * k * ell)
            check("C4_pushforward", lhs_cubed == rhs_cubed)
    results["C4_pushforward_11_1_cubed_identity"] = "exact"

    # ---- C5/C6: the (15.2) gamma factor, numerically (Simpson)
    # 144 * int_0^inf k^(4/3) phi_tau(12k) dk = Gamma(7/6) tau^(4/3) / (24^(1/3) sqrt(pi))
    def simpson(f, a, b, n):
        if n % 2:
            n += 1
        h = (b - a) / n
        s = f(a) + f(b)
        for i in range(1, n):
            s += f(a + i * h) * (4 if i % 2 else 2)
        return s * h / 3

    exponent = 5.0 / 6.0 if mutant == "M3" else 7.0 / 6.0
    for tau in (1.0, 2.5):
        def integrand(k, tau=tau):
            if k <= 0.0:
                return 0.0
            return 144.0 * k ** (4.0 / 3.0) * math.exp(
                -(12.0 * k) ** 2 / (2.0 * tau * tau)) / (
                tau * math.sqrt(2.0 * math.pi))
        got = simpson(integrand, 0.0, 4.0 * tau, 400000)
        want = math.gamma(exponent) * tau ** (4.0 / 3.0) / (
            24.0 ** (1.0 / 3.0) * math.sqrt(math.pi))
        rel = abs(got - want) / want
        check("C5_gamma_factor_tau%s" % tau, rel < 1e-9)
    results["C5_gamma_factor_15_2"] = "rel<1e-9 at tau=1,2.5"

    # C6: the underlying half-Gaussian moment
    # int_0^inf t^(4/3) phi_tau(t) dt = tau^(4/3) 2^(-1/3) Gamma(7/6)/sqrt(pi)
    tau = 1.7
    got = simpson(lambda t: 0.0 if t <= 0 else t ** (4.0 / 3.0) * math.exp(
        -t * t / (2 * tau * tau)) / (tau * math.sqrt(2 * math.pi)),
        0.0, 12.0 * tau, 400000)
    want = tau ** (4.0 / 3.0) * 2.0 ** (-1.0 / 3.0) * math.gamma(
        7.0 / 6.0) / math.sqrt(math.pi)
    check("C6_half_gaussian_moment", abs(got - want) / want < 1e-9)
    results["C6_half_gaussian_moment"] = "rel<1e-9"

    # ---- C7: amplitude-scaling exponent of (15.2): a^(-2/3) for every d
    for d in range(2, 11):
        total = F(-d) + F(-d) + F(4, 3) + F(2) * (d - 1)
        check("C7_amplitude_d%d" % d, total == F(-2, 3))
    results["C7_amplitude_scaling_exponent"] = "-2/3 all d in 2..10"

    # ---- C8: specialization concordance ((15.2) -> side24_v1 eq (1) -> value)
    check("C8_cube_identity", F(36, 24) == F(3, 2))  # (6^(2/3)/24^(1/3))^3
    D2 = 29.0 / 6.0 - math.sqrt(6.0)
    g76 = math.gamma(7.0 / 6.0)
    c3_spec = (g76 / (24.0 ** (1.0 / 3.0) * math.sqrt(math.pi))) * \
        4.0 * math.pi * (2.0 * math.pi) ** -3.0 * 3.0 ** -0.5 * \
        6.0 ** (2.0 / 3.0) * D2
    c3_formula1 = g76 * (1.5) ** (1.0 / 3.0) * D2 / (
        2.0 * math.sqrt(3.0) * math.pi ** 2.5)
    check("C8_spec_eq_formula1",
          abs(c3_spec - c3_formula1) / c3_formula1 < 1e-12)
    check("C8_value_d3", abs(c3_formula1 - 0.041775931840598343) < 1e-15)
    c2_formula1 = g76 * (1.5) ** (1.0 / 3.0) * (4.0 / 3.0) / (
        2.0 * math.sqrt(3.0) * math.pi ** 1.5)
    check("C8_value_d2", abs(c2_formula1 - 0.073406919306034271) < 1e-15)
    results["C8_specialization_concordance"] = {
        "c3": "%.18f" % c3_formula1, "c2": "%.18f" % c2_formula1}

    # ---- C9: E1 congruence D_r = diag(r^(-1/2), I): det(D H D) = det(H)/r,
    # exact over Q for m=1 (the sqrt(r) entries only ever appear squared)
    for r in (F(1, 4), F(2, 3), F(5)):
        for (al, be, A) in ((F(3), F(1, 2), F(-2)), (F(-1), F(4), F(7, 3))):
            detH = (r * al) * A - (r * be) * (r * be)
            det_scaled_correct = al * A - r * be * be        # diag(r^-1/2, 1)
            det_scaled_wrong = (r * r * al) * A - (r ** 3) * be * be  # diag(r^1/2,1)
            check("C9_E1_identity", det_scaled_correct == detH / r)
            if r != 1:
                check("C9_E1_mutant_differs", det_scaled_wrong != detH / r)
    results["C9_E1_congruence"] = "det(DHD)=det(H)/r exact; sqrt-r mutant differs"

    out = {
        "object": "CL-D1-CDE-FULLDEPTH-20260929-v1-CHECKS",
        "scope": ("finite exact/numerical controls for parent Sections 10, "
                  "13-14, 15 as read with E1/E2/W1; not the Gaussian proof"),
        "results": results,
        "passed": True,
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv)
