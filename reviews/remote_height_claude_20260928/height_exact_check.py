"""Independent exact checks for the nonauthor review of Math-#120
(frontiers/remote_height_decoupling_20260928/PROOF.md, remote within-window height decoupling).

Python standard library only; exact rational arithmetic. Written after reading the author's check.py, but it
shares no code with it and tests different objects. Groups:

  REG  (H7)-(H10) in an exact finite-rank Gaussian model on the plane (monomial basis of degree <= 5 with
       positive coefficient variances). The regression direction g = Cov(F, V) Sigma^-1 e_h is computed
       exactly. Checks: V[g] = e_h, hence the ORIGINAL endpoint values and gradients of g vanish; g is the same
       whether the pins are written raw or through RM's U_r transform; the pathwise identity
       F_h - F_h' = (h - h') g; the vector zero-average identity behind (H10) at both endpoints; the bound
       |D^2 g(i) u| <= (r/2) sup |D^3 g|; and second-order convergence of g to its contact limit.
  CONG (H12) positive congruence: det H = r det K and equal inertia, so F_j(H) = r F_j(K), for d = 2, 3.
  FDET (H13) = RM (8) for the filtered determinant on random and index-changing pairs (Frobenius form, which
       the operator-norm statement implies).
  LIP  (H17) integral of |theta - t| is 1/3; mean deviation of Lipschitz densities is at most L/3.
  MIX  (H18)-(H20) singleton/mean mixture, a <= q, Bonferroni, epsilon, own-marginal factor two,
       configuration-level TV = epsilon, and deterministic and randomized selectors, on random exact laws.
  BAR  (H21) the abstract r^2 barrier: exactly flat mean, q = r^5, singleton TV = r^2/(2(1-r^2)).
  MOM  (H4) TV controls bounded moments; physical mean/variance power ledger.

Not a continuum or Gaussian proof: uniform covariance floors, conditional moments and Kac-Rice are argued in
REVIEW.md.
"""
import argparse
import json
import random
import sys
from fractions import Fraction as F
from math import comb, factorial

MUTANTS = ("no-endpoint-pins", "gradient-target", "unscaled-beta", "indicator-only", "lip-constant",
           "eps-over-2m", "a-as-probability", "p2-r6", "var-l")

# ----------------------------------------------------------------------------------------------------------
# Exact linear algebra and polynomials
# ----------------------------------------------------------------------------------------------------------


def solve(A, b):
    n = len(A)
    M = [list(row) + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = next(i for i in range(col, n) if M[i][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for i in range(n):
            if i != col and M[i][col] != 0:
                fac = M[i][col]
                M[i] = [x - fac * y for x, y in zip(M[i], M[col])]
    return [M[i][n] for i in range(n)]


def det(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    return sum((-1) ** j * A[0][j] * det([row[:j] + row[j + 1:] for row in A[1:]]) for j in range(n))


def charpoly(A):
    """Faddeev-LeVerrier: coefficients c[0..n] of det(t I - A), c[n] = 1."""
    n = len(A)
    c = [F(0)] * (n + 1)
    c[n] = F(1)
    Mk = [[F(0)] * n for _ in range(n)]
    for k in range(1, n + 1):
        AM = [[sum(A[i][l] * Mk[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        Mk = [[AM[i][j] + (c[n - k + 1] if i == j else 0) for j in range(n)] for i in range(n)]
        AMk = [[sum(A[i][l] * Mk[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        c[n - k] = -sum(AMk[i][i] for i in range(n)) / k
    return c


def inertia(A):
    """(negatives, zeros) for a symmetric rational matrix: Descartes' rule is exact for real-rooted polynomials."""
    c = charpoly(A)
    z = 0
    while c[z] == 0:
        z += 1
    q = [c[i] * (-1) ** i for i in range(z, len(c))]  # coefficients of p(-t)/t^z
    signs = [x > 0 for x in q if x != 0]
    return sum(1 for u, v in zip(signs, signs[1:]) if u != v), z


def Fj(A, j, mut=None):
    neg, z = inertia(A)
    if z or neg != j:
        return F(0)
    return F(1) if mut == "indicator-only" else abs(det(A))


def frob2(A):
    return sum(x * x for row in A for x in row)


DEG = 5
BASIS = [(a, b) for a in range(DEG + 1) for b in range(DEG + 1 - a)]
WEIGHT = [F(1, factorial(a) * factorial(b)) for a, b in BASIS]  # positive coefficient variances


def dmono(m, i, j, pt):
    a, b = m
    if i > a or j > b:
        return F(0)
    c = (factorial(a) // factorial(a - i)) * (factorial(b) // factorial(b - j))
    return c * pt[0] ** (a - i) * pt[1] ** (b - j)


def apply(func, coeffs):
    return sum(w * dmono(m, i, j, pt) * coeffs[k] for k, m in enumerate(BASIS) for (w, i, j, pt) in func)


def row(func):
    return [sum(w * dmono(m, i, j, pt) for (w, i, j, pt) in func) for m in BASIS]


def observations(r, x, kind):
    O = (F(0), F(0))
    Y = [[(1, 1, 0, x)], [(1, 0, 1, x)], [(1, 0, 0, x)]]
    if kind == "Y":
        return Y
    if kind == "U0":
        U0 = [[(1, 0, 0, O)], [(1, 1, 0, O)], [(1, 2, 0, O)], [(1, 3, 0, O)], [(1, 0, 1, O)], [(1, 1, 1, O)]]
        return U0 + Y
    M, S = (-r / 2, F(0)), (r / 2, F(0))
    raw = [[(1, 0, 0, M)], [(1, 1, 0, M)], [(1, 0, 1, M)], [(1, 0, 0, S)], [(1, 1, 0, S)], [(1, 0, 1, S)]]
    U = [[(F(1, 2), 0, 0, M), (F(1, 2), 0, 0, S)],
         [(-1 / r, 0, 0, M), (1 / r, 0, 0, S)],
         [(-1 / r, 1, 0, M), (1 / r, 1, 0, S)],
         [(6 / r ** 2, 1, 0, M), (6 / r ** 2, 1, 0, S), (12 / r ** 3, 0, 0, M), (-12 / r ** 3, 0, 0, S)],
         [(F(1, 2), 0, 1, M), (F(1, 2), 0, 1, S)],
         [(-1 / r, 0, 1, M), (1 / r, 0, 1, S)]]
    return {"raw": raw + Y, "U": U + Y}[kind]


def direction(V, e_index):
    """Coefficients of g = Cov(F(.), V) Sigma^-1 e and the observation matrix A."""
    A = [row(f) for f in V]
    n = len(V)
    Sig = [[sum(A[k][i] * WEIGHT[i] * A[l][i] for i in range(len(BASIS))) for l in range(n)] for k in range(n)]
    e = [F(0)] * n
    e[e_index] = F(1)
    y = solve(Sig, e)
    return [WEIGHT[i] * sum(A[k][i] * y[k] for k in range(n)) for i in range(len(BASIS))], A, Sig


def restrict_axis(coeffs, i, j, r):
    """Univariate coefficients in t of (d_x^i d_z^j g)(-r/2 + t, 0)."""
    out = [F(0)] * (DEG + 1)
    for k, (a, b) in enumerate(BASIS):
        if coeffs[k] == 0 or i > a or j != b:
            continue
        c = coeffs[k] * (factorial(a) // factorial(a - i)) * factorial(b)
        p = a - i  # (-r/2 + t)^p
        for s in range(p + 1):
            out[s] += c * comb(p, s) * (-r / 2) ** (p - s)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def uni_int(p, weight, r):
    """integral_0^r weight(t) p(t) dt for weight 'r-t' or 't'."""
    tot = F(0)
    for s, c in enumerate(p):
        if weight == "t":
            tot += c * r ** (s + 2) / (s + 2)
        else:
            tot += c * (r * r ** (s + 1) / (s + 1) - r ** (s + 2) / (s + 2))
    return tot


def uni_eval(p, t):
    return sum(c * t ** s for s, c in enumerate(p))


def uni_maxabs(p, r):
    assert len(p) <= 3
    pts = [F(0), r]
    if len(p) == 3 and p[2] != 0:
        v = -p[1] / (2 * p[2])
        if 0 < v < r:
            pts.append(v)
    return max(abs(uni_eval(p, t)) for t in pts)


# ----------------------------------------------------------------------------------------------------------
# Groups
# ----------------------------------------------------------------------------------------------------------


def check_reg(mut):
    out = {}
    x = (F(3, 5), F(2, 7))
    nopin = mut == "no-endpoint-pins"
    # V ends with (f_x(x), f_z(x), f(x)); the mutant conditions on the witness observations alone.
    e_idx = (7 if mut == "gradient-target" else 8) - (6 if nopin else 0)
    kind_r, kind_0 = ("Y", "Y") if nopin else ("U", "U0")
    ok_ev, ok_pins, ok_one, ok_inv, ok_path, ok_avg, ok_bound = True, True, True, True, True, True, True
    rng = random.Random(120)
    for r in (F(1, 3), F(1, 7), F(1, 19)):
        used = observations(r, x, "Y" if nopin else "raw")
        c, A, Sig = direction(used, e_idx)
        cU, _, _ = direction(observations(r, x, "U"), 8)
        ok_inv &= c == cU
        raw = observations(r, x, "raw")
        vals = [apply(f, c) for f in raw]
        target = [F(0)] * 9
        target[8] = F(1)
        ok_ev &= vals == target
        ok_pins &= all(v == 0 for v in vals[:6])
        ok_one &= vals[8] == 1 and vals[6] == 0 and vals[7] == 0
        # (H7): pathwise identity with one unconditioned coefficient vector xi; the conditioned copies must
        # also realize every ORIGINAL target.
        xi = [F(rng.randrange(-40, 41), rng.randrange(1, 9)) for _ in BASIS]
        Vxi = [sum(a * z for a, z in zip(Ar, xi)) for Ar in A]
        vt = [F(1, 3), F(0), F(0), F(1, 3) - F(2, 5) * r ** 3, F(0), F(0), F(0), F(0)]

        def cond(h):
            a_h = (vt[6:] if nopin else vt) + [h]
            y = solve(Sig, [ai - vi for ai, vi in zip(a_h, Vxi)])
            return [xi[i] + WEIGHT[i] * sum(A[k][i] * y[k] for k in range(len(A))) for i in range(len(BASIS))]

        h1, h2 = F(1, 3) - F(1, 10) * r ** 3, F(1, 3) - F(3, 10) * r ** 3
        f1, f2 = cond(h1), cond(h2)
        ok_path &= all(u - v == (h1 - h2) * gi for u, v, gi in zip(f1, f2, c))
        ok_path &= [apply(f, f1) for f in raw] == vt[:6] + [F(0), F(0), h1]
        # (H10): vector zero-average identity at both endpoints, for the u-column (xx and xz entries).
        for (i, j) in ((2, 0), (1, 1)):
            col = restrict_axis(c, i, j, r)
            third = restrict_axis(c, i + 1, j, r)
            at_M, at_S = uni_eval(col, F(0)), uni_eval(col, r)
            ok_avg &= at_M == -uni_int(third, "r-t", r) / r and at_S == uni_int(third, "t", r) / r
            bnd = r / 2 * uni_maxabs(third, r)
            ok_bound &= abs(at_M) <= bnd and abs(at_S) <= bnd
    out["V_g_equals_e_h_exact"] = ok_ev
    out["original_endpoint_values_and_gradients_vanish"] = ok_pins
    out["g_x_one_and_grad_g_x_zero"] = ok_one
    out["U_r_reexpression_gives_same_g"] = ok_inv
    out["pathwise_F_h_minus_F_h2_is_dh_times_g_and_targets_realized"] = ok_path
    out["zero_average_identity_both_endpoints"] = ok_avg
    out["column_bound_r_over_2_sup_D3"] = ok_bound
    # Second-order contact convergence of the direction: ||g_r - g_0|| shrinks by >= 8 per factor 4 in r.
    c0, _, _ = direction(observations(None, x, kind_0), e_idx)
    ds = []
    for r in (F(1, 4), F(1, 16), F(1, 64)):
        cr, _, _ = direction(observations(r, x, kind_r), e_idx)
        ds.append(max(abs(u - v) for u, v in zip(cr, c0)))
    out["contact_limit_second_order"] = ds[1] * 8 <= ds[0] and ds[2] * 8 <= ds[1] and ds[2] > 0
    return out


def check_cong(mut):
    rng = random.Random(1201)
    ok_det, ok_idx, ok_F = True, True, True
    for n in (2, 3):
        for _ in range(150):
            s = F(rng.randrange(1, 20), 20)
            r = s * s
            alpha = F(rng.randrange(-9, 10), rng.randrange(1, 4))
            beta = [F(rng.randrange(-9, 10), rng.randrange(1, 4)) for _ in range(n - 1)]
            Ab = [[F(0)] * (n - 1) for _ in range(n - 1)]
            for i in range(n - 1):
                for j in range(i, n - 1):
                    Ab[i][j] = Ab[j][i] = F(rng.randrange(-9, 10), rng.randrange(1, 4))
            sb = 1 if mut == "unscaled-beta" else s
            K = [[alpha] + [sb * b for b in beta]] + [[sb * beta[i]] + Ab[i] for i in range(n - 1)]
            H = [[r * alpha] + [r * b for b in beta]] + [[r * beta[i]] + Ab[i] for i in range(n - 1)]
            ok_det &= det(H) == r * det(K)
            ok_idx &= inertia(H) == inertia(K)
            ok_F &= all(Fj(H, j) == r * Fj(K, j) for j in range(n + 1))
    return {"det_H_equals_r_det_K": ok_det, "inertia_preserved": ok_idx, "F_j_H_equals_r_F_j_K": ok_F}


def check_fdet(mut):
    rng = random.Random(1202)
    ok, flips = True, 0
    pairs = []
    for n in (2, 3):
        for _ in range(150):
            X = [[F(0)] * n for _ in range(n)]
            E = [[F(0)] * n for _ in range(n)]
            for i in range(n):
                for j in range(i, n):
                    X[i][j] = X[j][i] = F(rng.randrange(-9, 10), rng.randrange(1, 5))
                    E[i][j] = E[j][i] = F(rng.randrange(-9, 10), rng.randrange(1, 5))
            t = F(1, rng.choice((1, 10, 1000)))
            pairs.append((X, [[X[i][j] + t * E[i][j] for j in range(n)] for i in range(n)]))
        for eps in (F(1, 10), F(1, 1000), F(1, 10 ** 6)):  # forced index change across a singular matrix
            D1 = [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]
            D2 = [list(rw) for rw in D1]
            D1[n - 1][n - 1], D2[n - 1][n - 1] = eps, -eps
            pairs.append((D1, D2))
    for X, Y in pairs:
        n = len(X)
        m2 = max(frob2(X), frob2(Y))
        d2 = frob2([[X[i][j] - Y[i][j] for j in range(n)] for i in range(n)])
        flips += inertia(X) != inertia(Y)
        for j in range(n + 1):
            diff = Fj(X, j, mut) - Fj(Y, j, mut)
            ok &= diff * diff <= n * n * m2 ** (n - 1) * d2
    return {"filtered_det_lipschitz_all_pairs": ok and flips >= 6}


def check_lip(mut):
    out = {}
    # integral_0^1 integral_0^1 |theta - t| dt dtheta = integral_0^1 (theta^2/2 + (1-theta)^2/2) dtheta
    out["double_integral_abs_diff_one_third"] = F(1, 6) + F(1, 6) == F(1, 3)
    const = F(1, 6) if mut == "lip-constant" else F(1, 3)
    rng = random.Random(1203)
    Lc = F(3)
    ok = True
    cases = [[Lc] * 8, [-Lc] * 8] + [[F(rng.randrange(-30, 31), 10) for _ in range(8)] for _ in range(300)]
    for slopes in cases:
        knots = [F(5)]
        for sl in slopes:
            knots.append(knots[-1] + sl / 8)
        mean = sum((knots[i] + knots[i + 1]) / 2 for i in range(8)) / 8
        dev = F(0)
        for i in range(8):
            u, v = knots[i] - mean, knots[i + 1] - mean  # linear on a piece of width 1/8
            if u * v >= 0:
                dev += abs(u + v) / 2 / 8
            else:
                dev += (u * u + v * v) / (2 * abs(v - u)) / 8
        ok &= dev <= Lc * const
    out["mean_deviation_le_L_over_3"] = ok
    return out


def tv(p, q):
    keys = set(p) | set(q)
    return sum(abs(p.get(k, F(0)) - q.get(k, F(0))) for k in keys) / 2


def law_stats(law):
    m = sum(P * len(c) for c, P in law.items())
    mu, sig = {}, {}
    for c, P in law.items():
        for pt in c:
            mu[pt] = mu.get(pt, F(0)) + P
        if len(c) == 1:
            sig[c[0]] = sig.get(c[0], F(0)) + P
    a = sum(mu.values()) - sum(sig.values())
    q = sum(P * len(c) * (len(c) - 1) for c, P in law.items())
    alpha = sum(P for c, P in law.items() if len(c) >= 2)
    P1 = sum(P for c, P in law.items() if len(c) >= 1)
    return m, mu, sig, a, q, alpha, P1


def ymarg(d):
    out = {}
    for (y, th), v in d.items():
        out[y] = out.get(y, F(0)) + v
    return out


def times_lambda(d):
    return {(y, th): v / 2 for y, v in d.items() for th in (0, 1)}


def check_mix(mut):
    rng = random.Random(1204)
    marks = [(y, th) for y in range(4) for th in (0, 1)]
    laws = []
    s, p = F(1, 10), F(1, 20)
    laws.append({(): 1 - s - p, ((0, 0),): s, ((1, 0), (2, 1)): p})  # extremal: equality in (H19), (H20)
    for _ in range(300):
        w = {(): F(rng.randrange(1000, 3000))}
        for mk in marks:
            w[(mk,)] = F(rng.randrange(0, 60))
        for _ in range(6):
            c = tuple(sorted(rng.sample(marks, 2)))
            w[c] = w.get(c, F(0)) + rng.randrange(0, 6)
        for _ in range(3):
            c = tuple(sorted(rng.sample(marks, 3)))
            w[c] = w.get(c, F(0)) + rng.randrange(0, 3)
        tot = sum(w.values())
        laws.append({c: v / tot for c, v in w.items() if v})
    res = dict.fromkeys(("mixture_tv_le_a_over_m", "a_le_q", "p1_ge_m_minus_q", "bonferroni_and_multiple",
                         "epsilon_le_q_over_2m_minus_q", "own_marginal_factor_two", "height_marginal_bound",
                         "configuration_tv_equals_epsilon", "selectors_within_epsilon"), True)
    for law in laws:
        m, mu, sig, a, q, alpha, P1 = law_stats(law)
        p1 = sum(sig.values())
        S = {k: v / p1 for k, v in sig.items()}
        mun = {k: v / m for k, v in mu.items()}
        abound = alpha if mut == "a-as-probability" else a
        res["mixture_tv_le_a_over_m"] &= tv(S, mun) <= abound / m
        res["a_le_q"] &= a <= q
        res["p1_ge_m_minus_q"] &= p1 == m - a and p1 >= m - q
        res["bonferroni_and_multiple"] &= P1 >= m - q / 2 and alpha <= q / 2
        eps = alpha / P1
        ebound = q / (2 * m) if mut == "eps-over-2m" else q / (2 * m - q)
        res["epsilon_le_q_over_2m_minus_q"] &= 2 * m > q and eps <= ebound
        base = tv(mun, times_lambda(ymarg(mun)))
        pi1 = ymarg(S)
        res["own_marginal_factor_two"] &= (tv(pi1, ymarg(mun)) <= tv(S, mun)
                                           and tv(S, times_lambda(pi1)) <= 2 * a / m + base)
        thS = {th: sum(v for (y, t), v in S.items() if t == th) for th in (0, 1)}
        res["height_marginal_bound"] &= tv(thS, {0: F(1, 2), 1: F(1, 2)}) <= a / m + base
        cond = {c: P / P1 for c, P in law.items() if c}
        emb = {(k,): v for k, v in S.items()}
        res["configuration_tv_equals_epsilon"] &= tv(cond, emb) == eps
        det_sel, rnd_sel = {}, {}
        for c, P in cond.items():
            k = min(c)
            det_sel[k] = det_sel.get(k, F(0)) + P
            for pt in c:
                rnd_sel[pt] = rnd_sel.get(pt, F(0)) + P / len(c)
        for sel in (det_sel, rnd_sel):
            res["selectors_within_epsilon"] &= (tv(sel, S) <= eps and
                                                tv(sel, times_lambda(ymarg(sel))) <= 2 * eps + tv(S, times_lambda(pi1)))
    return res


def check_bar(mut):
    ok_flat, ok_q, ok_tv, ok_nonneg, ok_beats = True, True, True, True, True
    for r in (F(1, 2), F(1, 3), F(1, 10), F(1, 50)):
        m = r ** 3
        p2 = r ** 6 / 2 if mut == "p2-r6" else r ** 5 / 2
        sig = {("A", 0): m / 4 - p2, ("A", 1): m / 4, ("B", 0): m / 4 - p2, ("B", 1): m / 4}
        law = {c: v for c, v in (((k,), v) for k, v in sig.items())}
        law[(("A", 0), ("B", 0))] = p2
        law[()] = 1 - sum(sig.values()) - p2
        mm, mu, sg, a, q, alpha, P1 = law_stats(law)
        ok_flat &= mm == m and all(v == m / 4 for v in mu.values())
        ok_q &= q == r ** 5 and a == q
        p1 = sum(sg.values())
        th = {t: sum(v for (y, tt), v in sg.items() if tt == t) / p1 for t in (0, 1)}
        val = tv(th, {0: F(1, 2), 1: F(1, 2)})
        ok_tv &= val == r * r / (2 * (1 - r * r)) and val <= a / m
        ok_nonneg &= all(v >= 0 for v in law.values())
        if r <= F(1, 10):
            ok_beats &= val > r ** 3
    return {"mean_exactly_flat": ok_flat, "q_equals_r5": ok_q, "singleton_tv_r2_over_2_1_minus_r2": ok_tv,
            "valid_law_r_le_half": ok_nonneg, "exceeds_r3": ok_beats}


def check_mom(mut):
    rng = random.Random(1205)
    grid = [F(i, 12) for i in range(13)]
    ok = True
    for _ in range(300):
        P = [F(rng.randrange(0, 20)) for _ in grid]
        Q = [F(rng.randrange(0, 20)) for _ in grid]
        if not sum(P) or not sum(Q):
            continue
        P = [v / sum(P) for v in P]
        Q = [v / sum(Q) for v in Q]
        d = sum(abs(u - v) for u, v in zip(P, Q)) / 2
        for phi in (lambda t: t, lambda t: t * t):
            ok &= abs(sum(u * phi(t) for u, t in zip(P, grid)) - sum(v * phi(t) for v, t in zip(Q, grid))) <= d
    # Var(theta) perturbation: E theta = 1/2 + d1, E theta^2 = 1/3 + d2, |d_i| <= delta <= 1 => |Var - 1/12| <= 3 delta
    ok_var = True
    for _ in range(300):
        delta = F(rng.randrange(1, 100), 100)
        d1 = delta * F(rng.randrange(-100, 101), 100)
        d2 = delta * F(rng.randrange(-100, 101), 100)
        var = F(1, 3) + d2 - (F(1, 2) + d1) ** 2
        ok_var &= abs(var - F(1, 12)) <= 3 * delta
    lpow = 3
    varpow = 1 if mut == "var-l" else 2
    return {"tv_controls_bounded_moments": ok, "variance_perturbation_3_delta": ok_var,
            "mean_error_power_r5": lpow + 2 == 5, "variance_error_power_r8": varpow * lpow + 2 == 8}


def flatten(d):
    for v in d.values():
        if isinstance(v, dict):
            yield from flatten(v)
        else:
            yield v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    mut = ap.parse_args().mutant
    checks = {"REG_regression_direction": check_reg(mut), "CONG_congruence": check_cong(mut),
              "FDET_filtered_determinant": check_fdet(mut), "LIP_window_variation": check_lip(mut),
              "MIX_singleton_mixture": check_mix(mut), "BAR_r2_barrier": check_bar(mut),
              "MOM_moments": check_mom(mut)}
    passed = all(flatten(checks))
    print(json.dumps({"checks": checks, "passed": passed, "scientific_effect": "NONE",
                      "scope": "exact identities and a finite-rank Gaussian regression model only; uniform "
                               "covariance floors, conditional moments and Kac-Rice are argued in REVIEW.md"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
