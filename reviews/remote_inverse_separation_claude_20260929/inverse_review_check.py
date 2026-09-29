"""Independent nonauthor checks for OA-REMOTE-INVERSE-SEPARATION-20260928-v1 (Math-#128, PROOF.md).

Python standard library only; exact rational arithmetic throughout. Written from the markdown; the author's
inverse.py/test_inverse.py are replayed separately and not reused here. Groups:

  LEDGER    exact frame Jacobians: (grad f(x), grad f(x')) -> G_delta has det delta^(-d); the height-divided frame of
            RC (4.1) has det delta^(-d-3), and with dy' = delta^3 dt it reduces to the same delta^(-d); radial powers
            (d-1)-d+2 = 1 (fixed r, (I16)) and (d-1)-(d+3)+3+2 = 1 (blow-up); r-power 3 of J_r from both routes.
  ENVELOPE  (I10): the z-length/t-window algebra; exact dyadic shell ratios decide convergence of s^(p+1) at 0 and
            s^(p-2) at infinity for rational p, so the envelope is finite exactly on -2 < p < 1.
  OVERLAP   (I11) on exact instances (k/|t| a perfect power chosen so every rational power is rational), for
            negative and positive p, including p = 0 = (R10); the T-exponent (4-p)/3 lies in (1, 2).
  COEFF     (I8) constant 108 * 12^(-(4-p)/3) = (3/4) 12^((p+2)/3); the p = 0 reduction to RP (R3) (3/40); the
            normalization of (I20); the Tonelli identity A_p = A_0 * int s^p g_S; the slope (I21) 144/4 = 36; and an
            Abelian cross-check between (I8) and (I19): (p+2) A_p -> J_0 as p decreases to -2.
  PAIR      explicit polynomial fields in d = 2, 3, 4 with critical points at x and x + delta e: exact identity
            det H_x det H_x' = -delta^2[(T^2/4)(det A)^2 - delta^2 q^2], hence (I14) with an O(delta^2) error; the
            segment bound |H_x e| <= (delta/2)|D^3 f|; det(H)^2 <= |He|^2 ||H||_F^(2(d-1)); the height gap
            f(x') - f(x) = -T delta^3/12, so two windows differ on a y-set of measure exactly |T| delta^3/12.
  RANK      distinct-jet independence as exact rank over Q of derivative functionals on polynomial spaces: pins,
            grad f(x), H_x e, A, T, f(x), H_M, H_S at delta = 0 (the (I15) positivity list) and pins, grad f(x),
            grad f(x + delta e), f(x) at delta > 0; negative control: grad f(x + 0 e) duplicates grad f(x).
  CUTOFF    (I5)/(I6) on a model radial density delta(J + a delta): q = 3, 4 power asymptotics, the q = 2 log with a
            bounded rational remainder, and the CDF half.
  SCOPE     counterexamples recording why the scope limits are needed: a family with both iterated limits equal to
            J_0 but a coupled cutoff delta = r^10 seeing J_0 + 1/2; a TV-convergent family whose inverse moment
            diverges, so (I7) needs the weighted domination rather than TV alone.

Mutants (each must fail): height-jacobian, envelope-endpoint, overlap-three, contact-quarter, merge-rate,
jet-duplicate, cdf-half.
Not an analytic proof: the Gaussian conditioning, Kac-Rice, domination and translation steps are reviewed in REVIEW.md.
"""
import argparse
import itertools
import json
import random
import sys
from fractions import Fraction as F

MUTANTS = ("height-jacobian", "envelope-endpoint", "overlap-three", "contact-quarter", "merge-rate",
           "jet-duplicate", "cdf-half")
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


def rank(rows):
    M = [list(map(F, r)) for r in rows]
    rk, cols = 0, len(M[0]) if M else 0
    for c in range(cols):
        p = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c] / M[rk][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[rk])]
        rk += 1
    return rk


def ipow(x, n):
    """x^n for rational x and integer n (negative allowed)."""
    return F(x) ** n


# ---------------------------------------------------------------------------------------------------------------

def check_ledger():
    out = {}
    ok_grad = ok_height = ok_consistent = True
    for d in range(2, 7):
        for delta in (F(1, 3), F(2, 7), F(1, 10)):
            # (g, g') -> (g, (g' - g)/delta), variables ordered g_1..g_d, g'_1..g'_d
            L = [[F(0)] * (2 * d) for _ in range(2 * d)]
            for i in range(d):
                L[i][i] = F(1)
                L[d + i][i] = -1 / delta
                L[d + i][d + i] = 1 / delta
            g_power = -(d + 3) if MUT == "height-jacobian" else -d
            ok_grad &= abs(det(L)) == delta ** g_power
            # RC (4.1): (g, g', y, y') -> (g, (g'-g)/delta, y, [y' - y - (delta/2) e.(g + g')]/delta^3), e = first axis
            n = 2 * d + 2
            V = [[F(0)] * n for _ in range(n)]
            for i in range(2 * d):
                V[i] = L[i] + [F(0), F(0)]
            V[2 * d][2 * d] = F(1)
            last = [F(0)] * n
            last[0] = -(delta / 2) / delta ** 3
            last[d] = -(delta / 2) / delta ** 3
            last[2 * d] = -1 / delta ** 3
            last[2 * d + 1] = 1 / delta ** 3
            V[2 * d + 1] = last
            ok_height &= abs(det(V)) == delta ** (-(d + 3))
            # dy' = delta^3 dt: the height-divided frame reduces to the gradient-only density power
            ok_consistent &= abs(det(V)) * delta ** 3 == delta ** (-d)
    out["gradient_only_frame_det_is_delta_minus_d"] = ok_grad
    out["height_divided_frame_det_is_delta_minus_d_minus_3"] = ok_height
    out["frames_agree_after_dy_prime_equals_delta3_dt"] = ok_consistent
    ok_fixed = ok_blow = True
    for d in range(2, 11):
        g_power = -(d + 3) if MUT == "height-jacobian" else -d
        ok_fixed &= (d - 1) + g_power + 2 == 1                 # (I16)
        ok_blow &= (d - 1) - (d + 3) + 3 + 2 == 1              # RP ledger, unchanged
    out["fixed_r_radial_power_is_one_all_d"] = ok_fixed
    out["blow_up_radial_power_is_one_all_d"] = ok_blow
    # r-power of J_r: (I18) window dh = k r^3 dtheta, and W_r / Z_r ~ r^2 / r^2  ->  3.
    # Iterated-limit route: j_r(r s) r ds = r^5 A_0 g_S(s) ds and g_S(s) ~ (J_0/A_0) s  ->  j_r(delta) ~ r^(5-1-1) J_0 delta.
    out["J_r_is_order_r_cubed_by_both_routes"] = (3 + 2 - 2 == 3) and (5 - 1 - 1 == 3)
    return out


def check_envelope():
    out = {}
    # (I9)/(I10): for fixed s, z the t-window has length exactly k/s^3; the z-overlap is (k - s^3|t|)_+ (RP (R9)).
    rng = random.Random(128001)
    ok_len = ok_overlap = True
    for _ in range(300):
        k = F(rng.randint(1, 30), rng.randint(1, 7))
        s = F(rng.randint(1, 20), rng.randint(1, 7))
        z = k * F(rng.randint(1, 99), 100)
        t = F(rng.randint(-50, 50), rng.randint(1, 7))
        ok_len &= z / s ** 3 - (z - k) / s ** 3 == k / s ** 3
        lo, hi = max(F(0), s ** 3 * t), min(k, k + s ** 3 * t)
        ok_overlap &= max(F(0), hi - lo) == max(F(0), k - s ** 3 * abs(t))
    out["t_window_length_is_k_over_s_cubed"] = ok_len
    out["z_overlap_is_k_minus_s3_abs_t"] = ok_overlap
    # With the weight s^p the envelope is s^(p+1) near 0 and s^(p-2) near infinity.  On shells [lam^-(n+1), lam^-n]
    # (resp. [lam^n, lam^(n+1)]) with lam = 2^q, q = den(p), the shell integrals form exact geometric series with
    # ratios 2^(-q(p+2)) (resp. 2^(q(p-1))); a series converges iff its ratio is < 1.
    def finite(p):
        q = p.denominator
        near_ratio = ipow(2, -int(q * (p + 2)))
        far_ratio = ipow(2, int(q * (p - 1)))
        if MUT == "envelope-endpoint":
            return near_ratio <= 1 and far_ratio <= 1
        return near_ratio < 1 and far_ratio < 1
    inside = [F(-7, 4), F(-3, 2), F(-1), F(-1, 3), F(0), F(1, 2), F(5, 6)]
    outside = [F(-3), F(-2), F(1), F(3, 2), F(2)]
    out["envelope_finite_exactly_on_minus2_lt_p_lt_1"] = (all(finite(p) for p in inside)
                                                         and not any(finite(p) for p in outside))
    # Endpoint shells are not summable: at p = -2 each shell of s^-1 contributes >= 1/2 (min 2^n, width 2^-(n+1)),
    # and at p = 1 each far shell of s^-1 contributes >= 1/2 (min 2^-(n+1), width 2^n).
    near = sum(ipow(2, n) * ipow(2, -(n + 1)) for n in range(40))
    far = sum(ipow(2, -(n + 1)) * ipow(2, n) for n in range(40))
    out["endpoint_shell_sums_grow_linearly"] = near == 20 and far == 20
    return out


def check_overlap():
    out = {}
    ok = True
    for p in (F(-7, 4), F(-3, 2), F(-1), F(-1, 2), F(-1, 3), F(0), F(1, 3), F(1, 2), F(3, 4)):
        q = p.denominator
        for base in (2, 3):
            for tt in (F(1), F(2, 5), F(7, 3)):
                m = F(base) ** q                         # s_max = (k/|t|)^(1/3) = m, so k = m^3 |t|
                k = m ** 3 * tt
                m_p2 = F(base) ** int(q * (p + 2))       # m^(p+2), exact since q(p+2) is an integer
                m_p5 = m_p2 * m ** 3
                lhs = k * m_p2 / (p + 2) - tt * m_p5 / (p + 5)
                num = 1 if MUT == "overlap-three" else 3
                # 3 k^((p+5)/3) |t|^(-(p+2)/3) / ((p+2)(p+5)) = 3 k (k/|t|)^((p+2)/3) / (...) = 3 k m^(p+2) / (...)
                rhs = num * k * m_p2 / ((p + 2) * (p + 5))
                ok &= lhs == rhs
    out["I11_overlap_integral_exact_negative_and_positive_p"] = ok
    out["I11_at_p0_is_R10_three_tenths"] = F(3) / (F(2) * F(5)) == F(3, 10)
    out["T_exponent_in_1_2_on_domain"] = all(1 < (4 - p) / 3 < 2 for p in (F(-199, 100), F(-1), F(0), F(99, 100)))
    return out


def check_coeff():
    out = {}
    ps = (F(-7, 4), F(-1), F(-1, 2), F(0), F(1, 2), F(9, 10))
    # 36 t^2 times the numerator 3 of (I11) is 108; 12^((p+2)/3) * 12^((4-p)/3) = 12^2, so
    # 108 * 12^(-(4-p)/3) = (3/4) 12^((p+2)/3)  <=>  108 = (3/4) * 144.
    out["I8_constant_108_equals_three_quarters_144"] = (36 * 3 == 108 and F(3, 4) * 144 == 108
                                                       and all((p + 2) / 3 + (4 - p) / 3 == 2 for p in ps))
    # p = 0: 3 / (4 (p+2)(p+5)) = 3/40, the RP (R3) all-index constant.
    out["I8_at_p0_reduces_to_R3_three_fortieths"] = F(3) / (4 * 2 * 5) == F(3, 40)
    # Normalization of (I20): 36 * (3/10) = 54/5 = (3/40) 12^(2/3) 12^(4/3) = (3/40) * 144.
    out["I20_normalizes_to_one"] = 36 * F(3, 10) == F(54, 5) == F(3, 40) * 144
    # Tonelli: A_0 int s^p g_S ds = (36/z0) int t^2 Psi * 3 k^((p+5)/3) |t|^(-(p+2)/3)/((p+2)(p+5)); (I8) after
    # t = -T/12 gives (3/4) 12^((p+2)/3) 12^((4-p)/3) / ((p+2)(p+5)) = 108/((p+2)(p+5)); both prefactors agree.
    out["A_p_equals_A_0_times_S_moment"] = all(F(36 * 3) / ((p + 2) * (p + 5)) == F(3, 4) * 144 / ((p + 2) * (p + 5))
                                               for p in ps)
    # (I21): J_0 = (k/(4 z0)) * 144 int t^2 Psi (T^2 = 144 t^2), slope of g_S = (36 k/(z0 A0)) int t^2 Psi.
    quarter = F(1, 2) if MUT == "contact-quarter" else F(1, 4)
    out["I21_slope_equals_J0_over_A0"] = quarter * 144 == 36
    # Abelian cross-check: (p+2) A_p -> J_0 as p decreases to -2.  Rational prefactor of (p+2) A_p is
    # 3 / (4 (p+5)) -> 3/(4*3) = 1/4 = (I19) prefactor; k-power (p+5)/3 -> 1; T-power (4-p)/3 -> 2.
    seq = [F(-2) + F(1, 10 ** n) for n in range(1, 8)]
    pref = [F(3) / (4 * (p + 5)) for p in seq]
    converging = all(abs(pref[i + 1] - quarter) < abs(pref[i] - quarter) for i in range(len(pref) - 1))
    out["abelian_limit_of_I8_matches_I19"] = (converging and F(3) / (4 * 3) == quarter
                                              and (F(-2) + 5) / 3 == 1 and (4 - F(-2)) / 3 == 2)
    return out


def pair_field(T, A, c, delta):
    """f(u, v) = (T/6)u^3 - (T/4)delta u^2 + (1/2) v^T A v + (u^2 - delta u) c.v on R x R^(d-1)."""
    n = len(A)

    def hess(u):
        Huu = T * u - T * delta / 2
        Huv = [(2 * u - delta) * ci for ci in c]
        return [[Huu] + Huv] + [[Huv[i]] + list(A[i]) for i in range(n)]

    def grad(u):
        return [T / 2 * u * u - T / 2 * delta * u] + [(u * u - delta * u) * ci for ci in c]

    def value(u):
        gap = T * u ** 3 / 6 - T * delta * u * u / 4
        return gap

    return hess, grad, value


def adj_quadratic(A, c):
    """c^T adj(A) c = det(A) - det(A - c c^T) (matrix determinant lemma, exact)."""
    n = len(A)
    return det(A) - det([[A[i][j] - c[i] * c[j] for j in range(n)] for i in range(n)])


def check_pair():
    rng = random.Random(128002)
    ok_crit = ok_product = ok_segment = ok_hadamard = ok_gap = ok_merge = True
    for d in (2, 3, 4):
        n = d - 1
        for trial in range(10):
            A = [[F(0)] * n for _ in range(n)]
            for i in range(n):
                A[i][i] = F((-1) ** (i + trial) * (i + 2))
                for j in range(i):
                    A[i][j] = A[j][i] = F(rng.randint(-2, 2), 10)
            c = [F(rng.randint(-9, 9), 7) for _ in range(n)]
            T = F(rng.choice([-1, 1]) * rng.randint(1, 20), 3)
            D, q = det(A), adj_quadratic(A, c)
            for delta in (F(1, 10), F(1, 100), F(1, 1000)):
                hess, grad, value = pair_field(T, A, c, delta)
                Hx, Hy = hess(F(0)), hess(delta)
                ok_crit &= all(v == 0 for v in grad(F(0)) + grad(delta))
                # exact: det H_x det H_x' = -delta^2 [(T^2/4) D^2 - delta^2 q^2]
                prod = det(Hx) * det(Hy)
                ok_product &= prod == -delta ** 2 * (T * T / 4 * D * D - delta ** 2 * q * q)
                # segment identity: H_x e = (-T delta/2, -delta c) and D^3 f has entries T, 2 c_j
                He = [row[0] for row in Hx]
                d3 = max([abs(T)] + [abs(2 * ci) for ci in c])
                ok_segment &= max(abs(v) for v in He) == delta / 2 * d3
                for H in (Hx, Hy):
                    col = [row[0] for row in H]
                    frob = sum(x * x for row in H for x in row)
                    ok_hadamard &= det(H) ** 2 <= sum(x * x for x in col) * frob ** (d - 1)
                gap = value(delta) - value(F(0))
                expected = -T * delta ** (2 if MUT == "merge-rate" else 3) / 12
                ok_gap &= gap == expected
                # two windows: {y in (a, b): y + gap not in (a, b)} has measure min(|gap|, b - a)
                a, b = F(-1, 3), F(2, 5)
                lo, hi = max(a, a - gap), min(b, b - gap)
                kept = max(F(0), hi - lo)
                ok_merge &= (b - a) - kept == min(abs(gap), b - a)
    # (I14) limit with O(delta^2) error: |prod|/delta^2 - (T^2/4) D^2 = -delta^2 q^2 when delta is small.
    T, A, c = F(7, 3), [[F(2), F(1, 10)], [F(1, 10), F(-3)]], [F(4, 7), F(-1, 7)]
    D, q = det(A), adj_quadratic(A, c)
    errs = []
    for delta in (F(1, 10), F(1, 100), F(1, 1000)):
        hess, _, _ = pair_field(T, A, c, delta)
        errs.append(abs(det(hess(F(0))) * det(hess(delta))) / delta ** 2 - T * T / 4 * D * D)
    ok_limit = all(e == -(dl ** 2) * q * q for e, dl in zip(errs, (F(1, 10), F(1, 100), F(1, 1000))))
    # Same-index control (RP): T = 0 with a mixed cubic gives a determinant product of order delta^4, so the
    # delta^2 coefficient that makes J_r > 0 comes only from adjacent-index pairs of the all-index sum.
    ok_same = True
    for lam, cc in ((F(3), F(2)), (F(-5, 2), F(1, 3))):
        for delta in (F(1, 10), F(1, 100)):
            H0 = [[F(0), -cc * delta], [-cc * delta, lam]]
            H1 = [[F(0), cc * delta], [cc * delta, lam]]
            ok_same &= det(H0) * det(H1) == (cc * delta) ** 4
    return {"pair_fields_have_both_critical_points": ok_crit,
            "determinant_product_exact_identity": ok_product,
            "I14_limit_with_order_delta_squared_error": ok_limit,
            "segment_bound_He_le_half_delta_D3": ok_segment,
            "det_squared_le_He_squared_times_frobenius": ok_hadamard,
            "height_gap_is_minus_T_delta_cubed_over_12": ok_gap,
            "two_windows_differ_on_measure_abs_gap": ok_merge,
            "same_index_product_is_order_delta_four": ok_same}


# ---- distinct-jet rank over Q -----------------------------------------------------------------------------------

def monomials(d, D):
    return [a for k in range(D + 1) for a in itertools.product(range(k + 1), repeat=d) if sum(a) == k]


def derivative_of_monomial(alpha, directions, point):
    """Apply d_{v_1} ... d_{v_m} to x^alpha and evaluate at point, exactly."""
    poly = {tuple(alpha): F(1)}
    for v in directions:
        new = {}
        for exps, coef in poly.items():
            for i, vi in enumerate(v):
                if vi == 0 or exps[i] == 0:
                    continue
                e2 = list(exps)
                e2[i] -= 1
                key = tuple(e2)
                new[key] = new.get(key, F(0)) + coef * exps[i] * vi
        poly = new
    total = F(0)
    for exps, coef in poly.items():
        term = coef
        for xi, k in zip(point, exps):
            term *= F(xi) ** k
        total += term
    return total


def functional_rows(funcs, d, D):
    mons = monomials(d, D)
    return [[derivative_of_monomial(a, dirs, pt) for a in mons] for pt, dirs in funcs]


def jet_lists(d, delta):
    basis = [tuple(F(int(i == j)) for j in range(d)) for i in range(d)]
    if d == 2:
        e, perp = (F(3, 5), F(4, 5)), [(F(-4, 5), F(3, 5))]
        x = (F(3, 2), F(1, 3))
    else:
        e = (F(1, 3), F(2, 3), F(2, 3))
        perp = [(F(2, 3), F(1, 3), F(-2, 3)), (F(2, 3), F(-2, 3), F(1, 3))]
        x = (F(3, 2), F(1, 3), F(-2, 5))
    r = F(1, 5)
    M = tuple(-r / 2 * u for u in basis[0])
    S = tuple(r / 2 * u for u in basis[0])
    xp = tuple(xi + delta * ei for xi, ei in zip(x, e))
    pins = [(M, []), (S, [])] + [(P, [b]) for P in (M, S) for b in basis]
    grad_x = [(x, [b]) for b in basis]
    hess_pairs = [(basis[i], basis[j]) for i in range(d) for j in range(i, d)]
    return dict(e=e, perp=perp, x=x, M=M, S=S, xp=xp, pins=pins, grad_x=grad_x, hess_pairs=hess_pairs, basis=basis)


def check_rank():
    out = {}
    ok_zero = ok_pos = ok_neg = True
    for d, D in ((2, 7), (3, 6)):
        J = jet_lists(d, F(0))
        He = [(J["x"], [J["e"], b]) for b in J["basis"]]
        if MUT == "jet-duplicate":
            He = [(J["xp"], [b]) for b in J["basis"]]      # grad f(x + 0 e) in place of H_x e
        A = [(J["x"], [J["perp"][i], J["perp"][j]]) for i in range(d - 1) for j in range(i, d - 1)]
        T = [(J["x"], [J["e"]] * 3)]
        val = [(J["x"], [])]
        HM = [(J["M"], list(p)) for p in J["hess_pairs"]]
        HS = [(J["S"], list(p)) for p in J["hess_pairs"]]
        # (I15) positivity list at delta = 0: pins, G_0 = (grad f(x), H_x e), A, T, f(x), H_M, H_S
        funcs = J["pins"] + J["grad_x"] + He + A + T + val + HM + HS
        expected = 2 * (d + 1) + d + d + (d - 1) * d // 2 + 1 + 1 + d * (d + 1)
        ok_zero &= len(funcs) == expected and rank(functional_rows(funcs, d, D)) == expected
        # delta > 0: pins, grad f(x), grad f(x + delta e), f(x) (G_delta is an invertible transform of these)
        for delta in (F(1, 7), F(2, 3)):
            Jd = jet_lists(d, delta)
            funcs_d = Jd["pins"] + Jd["grad_x"] + [(Jd["xp"], [b]) for b in Jd["basis"]] + [(Jd["x"], [])]
            ok_pos &= rank(functional_rows(funcs_d, d, D)) == 2 * (d + 1) + 2 * d + 1
        # negative control: at delta = 0, grad f(x + 0 e) duplicates grad f(x); rank drops by exactly d
        dup = J["pins"] + J["grad_x"] + [(J["xp"], [b]) for b in J["basis"]]
        ok_neg &= rank(functional_rows(dup, d, D)) == 2 * (d + 1) + d
    out["delta0_positivity_list_full_rank_d2_d3"] = ok_zero
    out["delta_positive_frame_full_rank_d2_d3"] = ok_pos
    out["undivided_gradient_frame_degenerates_at_delta0"] = ok_neg
    return out


def check_cutoff():
    out = {}
    J, a, d0 = F(5, 2), F(-3, 4), F(1, 2)
    # j(delta) = delta (J + a delta); I_q(eps) = int_eps^d0 delta^-q j(delta) d delta
    ok = True
    for n in range(2, 9):
        eps = F(1, 10 ** n)
        I3 = J * (1 / eps - 1 / d0) + a * (d0 - eps)                       # q = 3
        I4 = J * (1 / eps ** 2 - 1 / d0 ** 2) / 2 + a * (1 / eps - 1 / d0)  # q = 4
        ok &= abs(I3 / (J / eps) - 1) <= 4 * eps
        ok &= abs(I4 / (J / (2 * eps ** 2)) - 1) <= 4 * eps
    out["q3_q4_leading_terms_J_eps_power_over_q_minus_2"] = ok
    # q = 2: I_2 = J log(d0/eps) + a (d0 - eps); the rational remainder is bounded, so I_2 ~ J log(d0/eps).
    out["q2_log_with_bounded_remainder"] = all(abs(a * (d0 - F(1, 10 ** n))) <= abs(a) * d0 for n in range(2, 9))
    # (I6): P(S <= eps) = int_0^eps (J0/A0) s (1 + b s) ds ~ (J0/(2 A0)) eps^2
    J0, A0, b = F(7), F(3), F(11, 5)
    half = F(1) if MUT == "cdf-half" else F(1, 2)
    ok = True
    for n in range(2, 9):
        eps = F(1, 10 ** n)
        cdf = J0 / A0 * (eps ** 2 / 2 + b * eps ** 3 / 3)
        ok &= abs(cdf / (half * J0 / A0 * eps ** 2) - 1) <= 2 * b * eps
    out["small_cdf_has_factor_one_half"] = ok
    return out


def check_scope():
    out = {}
    J0 = F(3)
    h = lambda u: u / (1 + u * u)
    ok_fixed_r = ok_fixed_s = True
    for rn in (1, 2):
        r = F(1, 10 ** rn)
        # fixed r, delta -> 0: u = delta / r^10 -> 0 and 0 <= h(u) <= u
        for m in range(1, 6):
            delta = r ** 10 * F(1, 10 ** m)
            u = delta / r ** 10
            ok_fixed_r &= 0 <= h(u) <= u
        # fixed s, delta = r s: u = s r^-9 -> infinity and 0 <= h(u) <= 1/u
        for s in (F(1, 2), F(1), F(3)):
            u = r * s / r ** 10
            ok_fixed_s &= 0 <= h(u) <= 1 / u
    out["iterated_limits_both_J0_but_coupled_cutoff_sees_J0_plus_half"] = (ok_fixed_r and ok_fixed_s
                                                                          and J0 + h(F(1)) == J0 + F(1, 2))
    # TV alone does not move unbounded inverse moments: mu_n = (1 - 1/n) mu + (1/n) delta_{n^-2} has TV <= 1/n,
    # but the added q = 1 inverse moment is (1/n) n^2 = n.
    out["tv_convergence_does_not_control_inverse_moments"] = all(
        F(1, n) <= F(1, 10) and F(1, n) * F(n) ** 2 == n for n in (10, 100, 1000))
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
    checks = {"LEDGER": check_ledger(), "ENVELOPE": check_envelope(), "OVERLAP": check_overlap(),
              "COEFF": check_coeff(), "PAIR": check_pair(), "RANK": check_rank(), "CUTOFF": check_cutoff(),
              "SCOPE": check_scope()}
    passed = all(flatten(checks))
    print(json.dumps({"object": "CLAUDE-REVIEW-REMOTE-INVERSE-SEPARATION-20260929-v1", "checks": checks,
                      "passed": passed, "scope": "exact finite identities only; not an analytic proof"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
