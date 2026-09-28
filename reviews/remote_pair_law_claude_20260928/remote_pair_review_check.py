"""Independent nonauthor checks for OA-WINDOW-MULTIPLICITY-REMOTE-20260928-v1 (Math-#116, REMOTE_PAIR_LAW.md).

Python standard library only; exact rational arithmetic throughout. Written from the markdown; the author's absent
algebra.py is neither run nor reconstructed. Groups:

  LEDGER     radial and r-power ledgers of the blown-up pair Kac-Rice integral: (d-1)-(d+3)+3+2 = 1 and r^5, d = 2..10.
  WINDOW     (R9): for rational (z-range, s, t) the admissible z-length is exactly (k - s^3|t|)_+.
  OVERLAP    (R10) on exact instances with k/|t| a rational cube; the envelope integral of s*min(1, s^-3) is 3/2.
  COEFF      36*(3/10) = 54/5 and (54/5)*12^(-4/3) = (3/40)*12^(2/3), i.e. 54/5 = (3/40)*144.
  PAIR       explicit polynomial fields in d = 2, 3, 4 with critical points at x and x + delta*e: exact congruence limits
             F_i(H_x)/delta -> F_i(diag(-T/2, A)), F_j(H_x')/delta -> F_j(diag(T/2, A)) with O(delta) error, the
             orientation rule (R2) for both signs of T and every index of A, the e -> -e exchange, and the negative
             control: T = 0 with a mixed cubic gives two same-index points with determinants of order delta^2.
  HEIGHT     the pushforward Jacobian s ds = (1/3)(k/|t|)^(2/3) g^(-1/3) dg; the Beta(2/3, 2) normalization 9/10; h
             integrates to 1; the index-resolved triangle density (10/9)(b-a)^(-1/3); moments (R15) and Corr = 2/7.

Mutants (each must fail): exponent-d, chi-orientation, coefficient-power, beta-normalizer, overlap-exponent.
Not an analytic proof: the Gaussian limit, domination and translation steps are reviewed in REVIEW.md.
"""
import argparse
import json
import random
import sys
from fractions import Fraction as F

MUTANTS = ("exponent-d", "chi-orientation", "coefficient-power", "beta-normalizer", "overlap-exponent")
MUT = None


def det(A):
    n = len(A)
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


def negatives(A):
    """Number of negative eigenvalues of a symmetric rational matrix (sign changes of leading minors, generic)."""
    n = len(A)
    minors = [F(1)] + [det([row[:k] for row in A[:k]]) for k in range(1, n + 1)]
    if any(m == 0 for m in minors):
        return None
    return sum(1 for a, b in zip(minors, minors[1:]) if (a > 0) != (b > 0))


def chi(i, j, neg_a, T):
    """(R2): orientation of the adjacent pair; zero on T = 0."""
    if T == 0:
        return 0
    sign = 1 if (T > 0) != (MUT == "chi-orientation") else -1
    return int((i, j) == ((neg_a + 1, neg_a) if sign > 0 else (neg_a, neg_a + 1)))


# ---------------------------------------------------------------------------------------------------------------

def check_ledger():
    ok_delta = ok_r = True
    for d in range(2, 11):
        polar, density, second_height, dets = d - 1, -(d + 3), 3, 2
        if MUT == "exponent-d":
            polar = d
        ok_delta &= polar + density + second_height + dets == 1
        # r-powers with delta = r s, y = b - r^3 z: polar r^d, dy r^3, dy' = r^3 s^3 dt, density r^(-d-3), dets r^2,
        # W/Z -> w0/z0 (r^2 / r^2).
        ok_r &= d + 3 + 3 - (d + 3) + 2 == 5
    return {"delta_exponent_is_one_all_d": ok_delta, "r_power_is_five_all_d": ok_r}


def check_window():
    rng = random.Random(116301)
    ok = True
    for _ in range(400):
        k = F(rng.randint(1, 40), rng.randint(1, 9))
        s = F(rng.randint(1, 30), rng.randint(1, 9))
        t = F(rng.randint(-60, 60), rng.randint(1, 9))
        # z in (0,k) and (z-k)/s^3 < t < z/s^3  <=>  s^3 t < z < k + s^3 t
        lo, hi = max(F(0), s ** 3 * t), min(k, k + s ** 3 * t)
        length = max(F(0), hi - lo)
        ok &= length == max(F(0), k - s ** 3 * abs(t))
    return {"R9_z_length_is_k_minus_s3_abs_t": ok}


def check_overlap():
    ok = True
    for m in (1, 2, 3, 5):
        for tt in (F(1), F(2), F(1, 3), F(7, 5)):
            k = F(m) ** 3 * tt           # then s_max = (k/|t|)^(1/3) = m
            smax = F(m)
            integral = k * smax ** 2 / 2 - tt * smax ** 5 / 5
            expo = F(1, 3) if MUT == "overlap-exponent" else F(2, 3)
            # (3/10) k^(5/3) |t|^(-2/3) = (3/10) k (k/|t|)^(2/3) = (3/10) k smax^(3*expo)
            ok &= integral == F(3, 10) * k * smax ** (3 * expo)
    envelope = F(1, 2) + F(1)            # int_0^1 s ds + int_1^inf s^-2 ds
    return {"R10_overlap_integral_exact": ok, "envelope_s_min_1_s_minus3_is_3_over_2": envelope == F(3, 2)}


def check_coeff():
    # (54/5) 12^(-4/3) = c 12^(2/3)  <=>  54/5 = c 12^2 ; mutant uses 12^(-2/3) on the right, i.e. 54/5 = c 12^(2/3+2/3)
    power = F(2) if MUT != "coefficient-power" else F(4, 3)
    c = F(3, 40)
    ok = F(36) * F(3, 10) == F(54, 5) and (power.denominator == 1 and F(54, 5) == c * 12 ** int(power))
    return {"coefficient_54_over_5_times_12_minus_4_3_is_3_40_12_2_3": ok}


def pair_field_hessians(T, A, c, delta):
    """f(u, v) = (T/6)u^3 - (T/4)delta u^2 + (1/2) v^T A v + (u^2 - delta u) c.v on R x R^(d-1).
    grad f vanishes at (0,0) and (delta,0); returns the two Hessians and the gradients there."""
    n = len(A)
    def hess(u):
        Huu = T * u - T * delta / 2
        Huv = [(2 * u - delta) * ci for ci in c]
        return [[Huu] + Huv] + [[Huv[i]] + list(A[i]) for i in range(n)]
    def grad(u):
        return [T / 2 * u * u - T / 2 * delta * u] + [(u * u - delta * u) * ci for ci in c]
    return hess(F(0)), hess(delta), grad(F(0)), grad(delta)


def check_pair():
    rng = random.Random(116302)
    ok_crit = ok_limit = ok_orient = ok_swap = True
    for d in (2, 3, 4):
        n = d - 1
        for trial in range(12):
            # A diagonal-dominant with a chosen number of negative eigenvalues
            a_neg = trial % (n + 1)
            A = [[F(0)] * n for _ in range(n)]
            for i in range(n):
                A[i][i] = F(-(i + 2)) if i < a_neg else F(i + 2)
                for j in range(i):
                    A[i][j] = A[j][i] = F(rng.randint(-2, 2), 10)
            if negatives(A) != a_neg:
                continue
            c = [F(rng.randint(-9, 9), 7) for _ in range(n)]
            T = F(rng.choice([-1, 1]) * rng.randint(1, 20), 3)
            detA = det(A)
            errs = []
            for delta in (F(1, 10), F(1, 100), F(1, 1000)):
                Hx, Hy, gx, gy = pair_field_hessians(T, A, c, delta)
                ok_crit &= all(v == 0 for v in gx + gy)
                # exact: det H / delta -/+ (T/2) det A = -delta c^T adj(A) c, so (error / delta) is delta-independent
                errs.append(((det(Hx) / delta - (-T / 2) * detA) / delta, (det(Hy) / delta - (T / 2) * detA) / delta))
                nx, ny = negatives(Hx), negatives(Hy)
                if nx is not None and ny is not None:
                    ok_orient &= all(chi(i, j, a_neg, T) == int((i, j) == (nx, ny))
                                     for i in range(d + 1) for j in range(d + 1))
            # the limit error is exactly linear in delta, with the same slope at both witnesses
            ok_limit &= len(set(errs)) == 1 and errs[0][0] == errs[0][1]
            # e -> -e flips T and exchanges the ordered indices
            ok_swap &= all(chi(i, j, a_neg, -T) == chi(j, i, a_neg, T) for i in range(d + 1) for j in range(d + 1))
    # Negative control: T = 0 and a mixed cubic give two same-index points with det of order delta^2.
    ok_neg = True
    for lam, cc in ((F(3), F(2)), (F(-5, 2), F(1, 3))):
        for delta in (F(1, 10), F(1, 100)):
            H0 = [[F(0), -cc * delta], [-cc * delta, lam]]
            H1 = [[F(0), cc * delta], [cc * delta, lam]]
            ok_neg &= det(H0) == det(H1) == -(cc * delta) ** 2
            ok_neg &= det(H0) / delta ** 2 == -cc * cc   # order delta^2, so zero at the delta^1 scale of (R8)
    return {"pair_fields_have_both_critical_points": ok_crit,
            "R8_congruence_limits_with_O_delta_error": ok_limit,
            "R2_orientation_matches_exact_inertia": ok_orient,
            "e_to_minus_e_exchanges_ordered_indices": ok_swap,
            "same_index_pairs_only_at_order_delta_squared": ok_neg}


def check_height():
    out = {}
    # pushforward Jacobian on rational points: s ds/dg = k/(3 s |t|) equals (1/3)(k/|t|)^(2/3) g^(-1/3), g = s^3|t|/k.
    ok = True
    for s, tt, k in ((F(2), F(1), F(8)), (F(3, 2), F(4, 3), F(9, 4)), (F(1, 2), F(5), F(5, 8))):
        g = s ** 3 * tt / k
        lhs = s / (3 * s * s * tt / k)              # s / (dg/ds)
        # (k/|t|)^(2/3) g^(-1/3) = (k/|t|)^(2/3) (k/(s^3 |t|))^(1/3) = (k/|t|) / s
        rhs = F(1, 3) * (k / tt) / s
        ok &= lhs == rhs
    out["pushforward_jacobian"] = ok
    # int_0^1 g^(-1/3) (1-g) dg = 3/2 - 3/5 = 9/10
    norm = F(3, 2) - F(3, 5)
    target = F(1) if MUT == "beta-normalizer" else F(9, 10)
    out["beta_normalizer_9_over_10"] = norm == F(9, 10) and norm == target
    # h(a,b) = (5/9)|a-b|^(-1/3) integrates to 1: 2 * int_0^1 int_0^b (b-a)^(-1/3) da db = 2 * (3/2)(3/5)
    out["h_integrates_to_one"] = F(5, 9) * 2 * F(3, 2) * F(3, 5) == 1
    # index-resolved triangle density (10/9)(b-a)^(-1/3) on a<b integrates to 1
    out["triangle_density_integrates_to_one"] = F(10, 9) * F(3, 2) * F(3, 5) == 1
    # moments of g ~ Beta(2/3, 2): E g^n = (10/9) [1/(n+2/3) - 1/(n+5/3)] = 10/((3n+2)(3n+5))
    mom = {n: F(10, 9) * (1 / (n + F(2, 3)) - 1 / (n + F(5, 3))) for n in range(6)}
    ok = all(mom[n] == F(10, (3 * n + 2) * (3 * n + 5)) for n in mom)
    ok &= mom[0] == 1 and mom[1] == F(1, 4) and mom[2] == F(5, 44) and mom[2] - mom[1] ** 2 == F(9, 176)
    out["gap_moments_R15"] = ok
    # marginal (5/6)(a^(2/3) + (1-a)^(2/3)): mass 1, E a = 1/2, E a^2 = 29/88; E ab = 3/11; Corr = 2/7
    beta = lambda p, q: _beta_rational(p, q)
    mass = F(5, 6) * 2 * (1 / F(5, 3))
    Ea = F(5, 6) * (1 / F(8, 3) + beta(F(2), F(5, 3)))
    Ea2 = F(5, 6) * (1 / F(11, 3) + beta(F(3), F(5, 3)))
    Eab = Ea2 - mom[2] / 2
    var = Ea2 - Ea ** 2
    out["marginal_and_correlation_R15"] = (mass == 1 and Ea == F(1, 2) and Ea2 == F(29, 88) and Eab == F(3, 11)
                                           and (Eab - Ea ** 2) / var == F(2, 7))
    out["independent_uniform_mean_gap_is_one_third"] = F(1, 3) != mom[1]
    return out


def _beta_rational(p, q):
    """B(p, q) for integer p >= 1 and rational q > 0: B(p,q) = (p-1)! / (q (q+1) ... (q+p-1))."""
    assert p.denominator == 1 and p >= 1
    out = F(1)
    for i in range(int(p) - 1):
        out *= F(i + 1)
    den = F(1)
    for i in range(int(p)):
        den *= (q + i)
    return out / den


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
    checks = {"LEDGER": check_ledger(), "WINDOW": check_window(), "OVERLAP": check_overlap(), "COEFF": check_coeff(),
              "PAIR": check_pair(), "HEIGHT": check_height()}
    passed = all(flatten(checks))
    print(json.dumps({"object": "CLAUDE-REVIEW-REMOTE-PAIR-LAW-20260928-v1", "checks": checks, "passed": passed,
                      "scope": "exact finite identities only; not an analytic proof"}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
