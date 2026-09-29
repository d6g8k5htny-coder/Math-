"""Independent nonauthor checks for OA-WINDOW-MULTIPLICITY-DISTANCE-20260928-v1 (Math-#116 C4, REMOTE_DISTANCE_MOMENTS.md).

Python standard library only; exact rational arithmetic throughout. Written from the markdown; the author's absent
algebra.py is neither run nor reconstructed. Groups:

  DET       (D6): the block identity det[[delta a, delta b^T], [delta b, A]] = delta a det A - delta^2 b^T adj(A) b on
            random rational matrices, singular A included; explicit axial fields g'(u) = (c0 + c1 u)(u^2 - delta u)
            with critical points at 0 and delta give the Peano target t and the axial entries exactly:
            alpha_x = 6t + (c1/2) delta, alpha_x' = -6t + (c1/2) delta, i.e. +-6t + O(delta K).
  ENVELOPE  (D7)->(D8): the height integral of (t^2 + delta^2) over the actual two-window region is exactly
            k r^3 (a^3/6 + delta^2 a), a = k r^3/delta^3; the radial density r^3 delta (a^3 + delta^2 a) is exactly
            k^3 r^12 delta^-8 + k r^6 in the exponents; the original RP envelope would give r^6 delta^-2, whose first
            moment is not summable on dyadic shells between A r and epsilon, so the sharper (D8) is needed at p = 1.
  DIAGONAL  (D9): delta^4 (two t = 0 determinants) * delta^(-d-3) (value-gradient density) * delta^(d-1) (polar) =
            delta^0 for every d; hence local integrability of dist^p Lambda_2 exactly for p > -1.
  REGIMES   (D5): exact small-distance bounds for p > 1 (the delta <= r part r^(p-1), the r^12 part for integer
            p != 7, the r^6 part epsilon^(p+1)); the p = 1 middle bound r^6 int_{Ar}^eps delta^-7 <= A^-6/6 and
            int delta d delta <= eps^2/2; A_1 prefactor k^2/(2 z0) from (D2); regime exponents 5+p vs 6.
  TAIL      (D13)-(D14): int_{-1}^1 v^2 (1 - |v|) dv = 1/6, the constants 6 and 6/7; an exact piecewise-polynomial
            model Psi(t) = (1 - t^2)_+ shows s^9 int t^2 (k - s^3|t|)_+ Psi dt -> k^4/6 with O(s^-6) error; moments of
            S are finite exactly for p < 7; the tail matches (D8): r^4 (delta/r)^-8 = r^12 delta^-8, and the two
            envelope terms cross at delta = r^(3/4).
  MOMENTS   (D15)-(D16): E[S_r] limit exceeds E[S] by B_1/A_0 > 0; E[S_r^p] ~ (B_p/A_0) r^(1-p); RMS exponent 1/2;
            (D2) at p = 0 and p = 1 against RP (R3) and the Tonelli identity A_p = A_0 E[S^p] for 0 <= p < 7.

Mutants (each must fail): block-det, peano-slope, envelope-power, middle-cutoff, tail-sixth, a1-constant,
diagonal-order.
Not an analytic proof: the Gaussian conditioning, (D10) and limiting steps are reviewed in REVIEW.md.
"""
import argparse
import json
import random
import sys
from fractions import Fraction as F

MUTANTS = ("block-det", "peano-slope", "envelope-power", "middle-cutoff", "tail-sixth", "a1-constant",
           "diagonal-order")
MUT = None


def det(A):
    n = len(A)
    if n == 0:
        return F(1)
    M = [list(map(F, r)) for r in A]
    d = F(1)
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c] != 0), None)
        if p is None:
            return F(0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d *= M[c][c]
        for i in range(c + 1, n):
            f = M[i][c] / M[c][c]
            M[i] = [x - f * y for x, y in zip(M[i], M[c])]
    return d


def adjugate(A):
    n = len(A)
    if n == 1:
        return [[F(1)]]
    adj = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j + 1:] for k, row in enumerate(A) if k != i]
            adj[j][i] = (-1) ** (i + j) * det(minor)
    return adj


# ---------------------------------------------------------------------------------------------------------------

def check_det():
    rng = random.Random(116401)
    ok_block = True
    for n in (1, 2, 3, 4):
        for trial in range(25):
            A = [[F(0)] * n for _ in range(n)]
            for i in range(n):
                for j in range(i, n):
                    A[i][j] = A[j][i] = F(rng.randint(-4, 4), rng.randint(1, 3))
            if trial % 5 == 0:                       # force a singular transverse block
                for j in range(n):
                    A[n - 1][j] = A[0][j] if n > 1 else F(0)
                for i in range(n):
                    A[i][n - 1] = A[i][0] if n > 1 else F(0)
            a = F(rng.randint(-9, 9), 4)
            b = [F(rng.randint(-5, 5), 3) for _ in range(n)]
            delta = F(1, rng.randint(2, 50))
            H = [[delta * a] + [delta * bi for bi in b]] + [[delta * b[i]] + list(A[i]) for i in range(n)]
            adj = adjugate(A)
            quad = sum(b[i] * adj[i][j] * b[j] for i in range(n) for j in range(n))
            sign = 1 if MUT == "block-det" else -1
            ok_block &= det(H) == delta * a * det(A) + sign * delta ** 2 * quad
    # Axial Peano check: g'(u) = (c0 + c1 u)(u^2 - delta u) has g'(0) = g'(delta) = 0.
    ok_axial = True
    for c0, c1 in ((F(3), F(2)), (F(-5, 2), F(7, 3)), (F(1, 4), F(-9))):
        for delta in (F(1, 10), F(1, 100), F(2, 7)):
            gdiff = c0 * (delta ** 3 / 3 - delta ** 3 / 2) + c1 * (delta ** 4 / 4 - delta ** 4 / 3)
            t = gdiff / delta ** 3                  # D3_delta with zero endpoint gradients
            alpha_x = (-c0 * delta) / delta          # g''(0)/delta
            alpha_xp = (c0 * delta + c1 * delta ** 2) / delta   # g''(delta)/delta
            slope = F(0) if MUT == "peano-slope" else c1 / 2
            ok_axial &= alpha_x == 6 * t + slope * delta and alpha_xp == -6 * t + slope * delta
            ok_axial &= t == -c0 / 6 - c1 * delta / 12
    return {"D6_block_determinant_identity_incl_singular_A": ok_block,
            "D6_axial_entries_plus_minus_6t_plus_O_delta": ok_axial}


def check_envelope():
    out = {}
    ok_exact = True
    for k in (F(1), F(3, 2), F(7, 5)):
        for r in (F(1, 10), F(1, 7)):
            for delta in (r, 2 * r, F(1, 3), F(1, 2)):
                a = k * r ** 3 / delta ** 3
                # region {y in I_r, y + delta^3 t in I_r} has t-section length (k r^3 - delta^3 |t|)_+ on |t| <= a
                # int_{-a}^{a} (t^2 + delta^2)(k r^3 - delta^3 |t|) dt, evaluated by exact antiderivatives
                kr3 = k * r ** 3
                integral = 2 * (kr3 * (a ** 3 / 3 + delta ** 2 * a) - delta ** 3 * (a ** 4 / 4 + delta ** 2 * a ** 2 / 2))
                ok_exact &= integral == kr3 * (a ** 3 / 6 + delta ** 2 * a)
                ok_exact &= integral <= kr3 * (2 * a ** 3 / 3 + 2 * delta ** 2 * a)      # the note's cruder bound
    out["height_integral_exact_kr3_a3_over_6_plus_delta2_a"] = ok_exact
    # radial density r^3 * delta^(d-1) * delta^-d * delta^2 * (a^3 + delta^2 a): r and delta exponents of both terms
    first = (3 + 9, 1 - 9) if MUT != "envelope-power" else (3 + 9, 1 - 10)
    second = (3 + 3, 1 + 2 - 3)
    out["D8_terms_are_r12_delta_minus8_and_r6"] = first == (12, -8) and second == (6, 0)
    # delta <= r: the t-integral is bounded, so the radial density is r^3 * delta^(d-1-d+2) = r^3 delta
    out["D8_inner_is_r3_delta_all_d"] = all((d - 1) - d + 2 == 1 for d in range(2, 11))
    # Original RP envelope r^4 s min(1, s^-3) with s = delta/r is r^6 delta^-2 for delta >= r; its first moment
    # r^6 int delta^-1 has equal mass on every dyadic shell, so the p = 1 middle region would not vanish.
    shells = [F(2) ** n * F(1, 2) * F(2) ** (-n) for n in range(30)]   # min of delta^-1 times shell width
    out["original_envelope_first_moment_not_summable"] = all(s == F(1, 2) for s in shells) and sum(shells) == 15
    return out


def check_diagonal():
    ok = True
    for d in range(2, 11):
        dets = 2 if MUT == "diagonal-order" else 4
        ok &= dets + (-(d + 3)) + (d - 1) == 0
    # local integrability of delta^p * (bounded radial density) at 0 iff p > -1; B_p needs only p >= 0
    return {"D9_radial_density_order_delta0_all_d": ok,
            "B_p_locally_integrable_for_p_gt_minus1": all(p + 1 > 0 for p in (F(-1, 2), F(0), F(1), F(9)))
            and not F(-1) + 1 > 0}


def check_regimes():
    out = {}
    # p > 1, delta <= r: int_0^r delta^p r^3 delta d delta / r^6 = r^(p-1)/(p+2)
    ok = True
    for p in (F(3, 2), F(2), F(5), F(9)):
        for r in (F(1, 10), F(1, 100)):
            if p.denominator == 1:
                ok &= r ** 3 * r ** int(p + 2) / (p + 2) / r ** 6 == r ** int(p - 1) / (p + 2)
    # r^12 part on [r, eps] after / r^6: r^6 (eps^(p-7) - r^(p-7))/(p-7) for integer p != 7; decreasing to 0 in r
    for p in (2, 3, 4, 6, 8, 10):
        eps = F(1, 4)
        rs = (F(1, 10), F(1, 100), F(1, 1000))
        vals = [r ** 6 * (eps ** (p - 7) - r ** (p - 7)) / (p - 7) for r in rs]
        ok &= all(v > 0 for v in vals) and vals[0] > vals[1] > vals[2]
        # O(r^(p-1)) for p < 7 and O(r^6 eps^(p-7)) for p > 7, as stated in the note
        bounds = [r ** (p - 1) / (7 - p) if p < 7 else r ** 6 * eps ** (p - 7) / (p - 7) for r in rs]
        ok &= all(v <= b for v, b in zip(vals, bounds))
    out["p_gt_1_small_distance_parts_vanish"] = ok
    # p = 1: middle bounds
    ok = True
    power = 5 if MUT == "middle-cutoff" else 6
    for A in (F(1), F(4), F(10)):
        for r in (F(1, 100), F(1, 1000)):
            eps = F(1, 5)
            mid = r ** 6 * ((A * r) ** -6 - eps ** -6) / 6          # r^6 int_{Ar}^eps delta^-7 d delta
            ok &= mid == A ** -power / 6 - r ** 6 * eps ** -6 / 6 and 0 <= mid <= A ** -power / 6
            ok &= (eps ** 2 - (A * r) ** 2) / 2 <= eps ** 2 / 2       # int_{Ar}^eps delta d delta
    out["p1_middle_bounded_by_A_minus6_plus_eps2"] = ok
    # A_1 from (D2): 3 * 12^((p+2)/3) k^((p+5)/3) / (4 (p+2)(p+5) z0) at p = 1 is 36 k^2 / (72 z0) = k^2/(2 z0)
    pref = F(3 * 12) / (4 * 3 * 6)
    target = F(1, 4) if MUT == "a1-constant" else F(1, 2)
    out["A1_prefactor_k2_over_2z0"] = pref == target
    # regime exponents: microscopic r^(5+p) vs macroscopic r^6
    out["regime_exponents"] = all((5 + p < 6) == (p < 1) and (5 + p == 6) == (p == 1)
                                  for p in (F(0), F(1, 2), F(1), F(3, 2), F(4)))
    return out


def check_tail():
    out = {}
    sixth = F(1, 3) if MUT == "tail-sixth" else F(1, 6)
    # int_{-1}^{1} v^2 (1 - |v|) dv = 2 (1/3 - 1/4)
    out["v2_one_minus_abs_v_integral_is_one_sixth"] = 2 * (F(1, 3) - F(1, 4)) == sixth
    # constants: 36 * (1/6) = 6 in g_S tail, and the survival tail divides by 7
    out["tail_constants_6_and_6_over_7"] = 36 * sixth == 6 and F(6) / 7 == F(6, 7)
    # model Psi(t) = (1 - t^2)_+: for s^3 > k, J(s) = 2 int_0^{k/s^3} t^2 (k - s^3 t)(1 - t^2) dt exactly
    ok = True
    k = F(3, 2)
    errs = []
    for s in (F(2), F(4), F(8), F(16)):
        m = k / s ** 3
        J = 2 * (k * m ** 3 / 3 - s ** 3 * m ** 4 / 4 - k * m ** 5 / 5 + s ** 3 * m ** 6 / 6)
        err = s ** 9 * J - k ** 4 * sixth
        errs.append(err)
        ok &= abs(err) <= k ** 6 * s ** -6
    ok &= all(abs(errs[i + 1]) < abs(errs[i]) for i in range(len(errs) - 1))
    out["model_tail_s9_integral_to_k4_over_6"] = ok
    # finiteness of E[S^p]: s^(p-8) integrable at infinity iff p < 7; near 0 g_S = O(s)
    out["S_moments_finite_iff_p_lt_7"] = all(((p - 8) < -1) == (p < 7) for p in (F(0), F(6), F(7), F(15, 2)))
    # matching with (D8): r^4 g_S(delta/r) with g_S ~ s^-8 gives r^12 delta^-8; crossover r^12 d^-8 = r^6 at d = r^(3/4)
    out["tail_matches_D8_and_crossover_three_quarters"] = (4 + 8 == 12) and (F(12) - 8 * F(3, 4) == 6)
    return out


def check_moments():
    out = {}
    # E[S_r^p] = r^-p M_p / M_0: exponent -p + 6 - 5 = 1 - p for p >= 1; p = 1 limit (A_1 + B_1)/A_0 > A_1/A_0
    out["D15_D16_exponents"] = all(-p + 6 - 5 == 1 - p for p in (F(1), F(3, 2), F(3)))
    A1, B1, A0 = F(2), F(1, 3), F(5)
    out["D15_limit_exceeds_TV_limit_by_B1_over_A0"] = (A1 + B1) / A0 - A1 / A0 == B1 / A0 > 0
    # RMS: sqrt(M_2 / M_0) = sqrt(r^6 B_2 / (r^5 A_0)) -> exponent of r inside the root is 1
    out["rms_distance_exponent"] = 6 - 5 == 1
    # (D2) at p = 0 is RP's 3/40; Tonelli: 36 * 3/((p+2)(p+5)) = (3/4) 144 /((p+2)(p+5)) for 0 <= p < 7
    out["D2_at_p0_is_R3"] = F(3) / (4 * 2 * 5) == F(3, 40)
    out["A_p_is_A0_E_S_p"] = all(F(108) / ((p + 2) * (p + 5)) == F(3, 4) * 144 / ((p + 2) * (p + 5))
                                 for p in (F(0), F(1), F(3), F(13, 2)))
    # T-exponent (4-p)/3 > -1 exactly for p < 7
    out["D2_T_exponent_integrable_iff_p_lt_7"] = all(((4 - p) / 3 > -1) == (p < 7) for p in (F(0), F(5), F(7), F(8)))
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
    checks = {"DET": check_det(), "ENVELOPE": check_envelope(), "DIAGONAL": check_diagonal(),
              "REGIMES": check_regimes(), "TAIL": check_tail(), "MOMENTS": check_moments()}
    passed = all(flatten(checks))
    print(json.dumps({"object": "CLAUDE-REVIEW-REMOTE-DISTANCE-MOMENTS-20260929-v1", "checks": checks,
                      "passed": passed, "scope": "exact finite identities only; not an analytic proof"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
