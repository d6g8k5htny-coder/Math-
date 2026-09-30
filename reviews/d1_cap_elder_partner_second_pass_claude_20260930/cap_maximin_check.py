"""Second-pass finite controls for the marked-cylinder cap theorem (D1 component III).

Standard library only.  Run from anywhere:  python -B -S cap_maximin_check.py [--mutant NAME]

Object checked: the deterministic theorem of imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md
(MARKED-CYLINDER-CAP-20260924-v1, sections 2-5) and its composition into D1 Theorem A through
UNIFORM_MATRIX_CAP_AND_LIFETIME.md sections 7-8 (the good event G_r and the Morse / distinct-value locus).
The implication under audit is

    G_r  (transverse depth  lambda > (4/(3 kappa)) r M_3^2  and  r M_4 <= 3 kappa / 10)
      =>  the maximin connection level from M to {f > f(M)} equals f(S) = f(M) - kappa r^3
      =>  S is the ordinary superlevel elder death partner of M  (Morse, distinct critical values).

Rules (all must hold; exit 1 otherwise):
  EXACT_CONSTANTS        every rational constant of sections 2-5, in order, in exact arithmetic (Fractions), including the
                         kappa-rescaled constants used by the parent's G_r;
  RIDGE_IDENTITY_M3      identity (11), F'' = f_xxx + 3 f_xxy[h'] + 3 f_xyy[h',h'] + f_yyy[h',h',h'], as an exact
                         polynomial identity for transverse dimension 3 with a curved ridge (h'' != 0), an x-dependent
                         transverse Hessian and cubic transverse terms (the h'' cancellation is exercised, not assumed);
  MAXIMIN_D2, MAXIMIN_D3 explicit polynomial landscapes on the cap cylinder D = [-2r, 2r] x B(0, 2r), d = 2 and d = 3,
                         whose hypotheses (1) hold with exactly computed M_3, M_4, lambda: the grid maximin level from M
                         to the older set {f > b} (union-find in decreasing height order) equals s = b - kappa r^3 to
                         grid tolerance, and the merge happens at the grid point S;
  HYPOTHESIS_LOAD_BEARING a landscape that violates the depth condition (a quartic transverse rim inside D): the same
                         computation finds a maximin level strictly above s and a merge point away from S, so the
                         conclusion genuinely depends on (1) and not on the pins alone.
Mutants (each must exit 1): kernel-mass (Hermite kernel mass r^3/3 in place of r^3/6, so the forced third derivative
drops and the chain of section 4 no longer yields F'' > 1/4), depth-four (depth constant 4 in place of 8 in (4)),
coefficient-two (2 f_xxy[h'] in (11)), drop-cross-terms ((11) read as F'' = f_xxx), no-depth (the rim landscape fed to
the MAXIMIN_D2 rule), gap-sign (S above M: the pins are not a younger/older pair).

Finite grids demonstrate the mechanism on explicit functions; they prove nothing about arbitrary C^4 fields.  The proof
is the written derivation in REVIEW.md.  Scientific effect: NONE.
"""
import argparse
import json
import sys
from fractions import Fraction as Fr

MUTANTS = ("kernel-mass", "depth-four", "coefficient-two", "drop-cross-terms", "no-depth", "gap-sign")
MUT = None
BETA_RIM = Fr(100000)          # quartic transverse rim: pass level b - 1/(16 beta) above s = b - r^3/6 for r = 1/50


# ---------------------------------------------------------------- 1. exact constants of sections 2-5
def exact_constants():
    """Replays the constant chain of MARKED_CYLINDER_CAP_PROOF.md sections 2-5 in exact arithmetic (kappa = 1/6)."""
    out = {}
    r = Fr(1)                                                   # every constant below is homogeneous; r = 1 scales out
    # section 2: Hermite kernel (x + r/2)(r/2 - x) on [-r/2, r/2] has mass r^3/6; with the 1/2 in front,
    # f(S) - f(M) = -(1/2) mass . avg(f_xxx) = -r^3/6  =>  avg = 2
    mass = Fr(1, 3) if MUT == "kernel-mass" else Fr(1, 6)
    mass_exact = Fr(1, 4) - Fr(2, 3) * Fr(1, 8)                # int_{-1/2}^{1/2} (1/4 - x^2) dx
    avg = 2 * Fr(1, 6) / mass
    m_low = avg                                                 # sup |f_xxx| >= weighted average
    out["kernel_mass"] = str(mass_exact)
    out["forced_average_f_xxx"] = str(avg)
    # product distance from (x0, 0), x0 in [-r/2, r/2], to any point of D: <= 5r/2 + 2r = 9r/2 < 5r
    dist = Fr(5, 2) + 2
    ok = mass_exact == Fr(1, 6) and dist < 5
    # (5): f_xxx >= avg - 5 r n with r n <= 1/20; D_y^2 f <= -(lambda - 5 r m) I
    rn = Fr(1, 20)
    fxxx_low = avg - 5 * rn
    ok &= fxxx_low == Fr(7, 4) or MUT == "kernel-mass"
    depth = 4 if MUT == "depth-four" else 8                      # (4): lambda > depth . r m^2
    k = depth * m_low - 5                                        # delta > r m (depth m - 5) = r m k
    ok &= k >= 1
    out["k_min"] = str(k)
    delta_over_r = m_low * k                                     # delta/r > m k  (>= 22 in the source)
    # (6) sup_{|x|<=2r} |x^2 - r^2/4| = 15 r^2/4, so ||w|| <= (15/8) m r^2 < 2 m r^2
    ok &= (4 - Fr(1, 4)) == Fr(15, 4) and Fr(15, 8) < 2
    # (7) averaged kernel: sup_{|x|<=2r} int_{-r/2}^{r/2} |x - t| dt = 2 r^2  (attained at |x| = 2r)
    ok &= max(2 * Fr(1), Fr(1, 4) + Fr(1, 4)) == 2               # r|x| at |x| = 2r, x^2 + r^2/4 at |x| < r/2
    # (8)-(9): ||h|| < 2r/k, u = 2/k + 2/k^2, m u = (1 + 6/k + 5/k^2)/4 with m = (k + 5)/depth
    u = Fr(2, 1) / k + Fr(2, 1) / (k * k)
    m_of_k = (k + 5) / Fr(depth)
    mu = m_of_k * u
    out["u"] = str(u)
    out["m_u"] = str(mu)
    if depth == 8:
        ok &= mu == (1 + Fr(6, 1) / k + Fr(5, 1) / (k * k)) / 4
    # (12): adverse part <= m u (3 + 3u + u^2); F'' >= fxxx_low - adverse > 1/4
    adverse = mu * (3 + 3 * u + u * u)
    fpp = fxxx_low - adverse
    out["adverse"] = str(adverse)
    out["F_second_derivative_lower_bound"] = str(fpp)
    ok &= fpp > Fr(1, 4)
    if MUT is None:
        ok &= adverse == Fr(2554128, 1771561) and fpp == Fr(2184415, 7086244) and u == Fr(24, 121) and mu == Fr(48, 121)
    # (13): exterior integrals of (x - a)(x - c)/8 with a = -r/2, c = r/2 over [-2r, a] and [c, 2r] equal 9 r^3/32
    a, c = -Fr(1, 2), Fr(1, 2)
    def prim(x):                                                 # antiderivative of (x - a)(x - c)/8 = (x^2 - 1/4)/8
        return (x ** 3 / 3 - x / 4) / 8
    left = prim(a) - prim(-2)
    right = prim(2) - prim(c)
    ok &= left == Fr(9, 32) and right == Fr(9, 32)
    s_gap = Fr(1, 6)                                             # s = b - r^3/6
    ok &= Fr(9, 32) - s_gap == Fr(11, 96)
    out["exterior_integral"] = str(left)
    out["excess_over_gap"] = str(Fr(9, 32) - s_gap)
    # (14): transverse boundary: ||y - h|| > 2r - 2r/k >= 20r/11, delta > 22 r: drop > (22/2)(20/11)^2 r^3 = 4400/121 r^3
    ymh = 2 - Fr(2, 1) / k
    drop = (delta_over_r / 2) * ymh * ymh
    ok &= drop > s_gap
    if MUT is None:
        ok &= ymh == Fr(20, 11) and delta_over_r >= 22 and drop >= Fr(4400, 121)
    out["transverse_drop"] = str(drop)
    # kappa rescaling: apply the normalized theorem to f/(6 kappa)
    kappa = Fr(1, 7)                                             # a generic positive rational; every identity is linear in kappa
    cond_depth = Fr(depth) / (6 * kappa)                         # lambda > depth r m^2/(6 kappa)
    cond_fourth = 6 * kappa / 20
    ok &= (depth != 8) or (cond_depth == Fr(4, 3) / kappa and cond_fourth == 3 * kappa / 10)
    scaled = {"F_second_derivative": str(6 * kappa * Fr(1, 4)), "longitudinal_drop": str(6 * kappa * Fr(9, 32)),
              "excess": str(6 * kappa * Fr(11, 96)), "transverse_drop": str(6 * kappa * Fr(4400, 121))}
    ok &= scaled == {"F_second_derivative": str(3 * kappa / 2), "longitudinal_drop": str(27 * kappa / 16),
                     "excess": str(11 * kappa / 16), "transverse_drop": str(26400 * kappa / 121)}
    out["kappa_scaled_at_kappa_1_over_7"] = scaled
    return bool(ok), out


# ---------------------------------------------------------------- 2. exact multivariate polynomials
def padd(p, q):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, 0) + v
        if r[k] == 0:
            del r[k]
    return r


def pscale(p, c):
    return {k: v * c for k, v in p.items()} if c != 0 else {}


def pmul(p, q):
    r = {}
    for k1, v1 in p.items():
        for k2, v2 in q.items():
            k = tuple(a + b for a, b in zip(k1, k2))
            r[k] = r.get(k, 0) + v1 * v2
    return {k: v for k, v in r.items() if v != 0}


def pdiff(p, i):
    r = {}
    for k, v in p.items():
        if k[i] > 0:
            kk = list(k)
            kk[i] -= 1
            r[tuple(kk)] = r.get(tuple(kk), 0) + v * k[i]
    return r


def pconst(c, n):
    return {(0,) * n: Fr(c)} if c != 0 else {}


def pvar(i, n):
    k = [0] * n
    k[i] = 1
    return {tuple(k): Fr(1)}


def psubst_y(p, Q):
    """Substitute y_i := Q_i(x) (univariate polynomials in x as dicts over 1-tuples) into a polynomial in (x, y_1..y_m)."""
    n = len(Q) + 1
    res = {}
    for k, v in p.items():
        term = {(k[0],): v}
        for i, qi in enumerate(Q):
            for _ in range(k[1 + i]):
                term = pmul(term, qi)
        res = padd(res, term)
    return res


def ridge_identity_m3():
    """Identity (11) with transverse dimension 3: f = p(x) - 1/2 (y-Q)^T A(x) (y-Q) + cubic(y-Q), ridge y = Q(x)."""
    n = 4                                                        # variables x, y1, y2, y3
    x = pvar(0, n)
    y = [pvar(1 + i, n) for i in range(3)]
    Qx = [padd(pscale(pmul(x, x), Fr(1, 3)), pscale(x, Fr(-1, 5))),            # y1 = x^2/3 - x/5   (curved: h'' != 0)
          padd(pscale(pmul(pmul(x, x), x), Fr(2, 7)), pconst(Fr(1, 4), n)),     # y2 = 2x^3/7 + 1/4
          pscale(pmul(x, x), Fr(-3, 11))]                                       # y3 = -3x^2/11
    Q1 = [{(k[0],): v for k, v in q.items()} for q in Qx]                       # univariate copies for substitution
    z = [padd(y[i], pscale(Qx[i], -1)) for i in range(3)]                      # z = y - Q(x)
    A0 = [[Fr(2), Fr(1, 3), Fr(-1, 4)], [Fr(1, 3), Fr(3), Fr(1, 5)], [Fr(-1, 4), Fr(1, 5), Fr(5, 2)]]
    A1 = [[Fr(1, 2), Fr(-1, 6), Fr(1, 7)], [Fr(-1, 6), Fr(1, 3), Fr(0)], [Fr(1, 7), Fr(0), Fr(-1, 8)]]
    p = padd(padd(padd(pscale(pmul(pmul(x, x), x), Fr(5, 3)), pscale(pmul(x, x), Fr(-7, 2))), pscale(x, Fr(9, 4))),
             pscale(pmul(pmul(x, x), pmul(x, x)), Fr(1, 5)))
    f = dict(p)
    for i in range(3):
        for j in range(3):
            Aij = padd(pconst(A0[i][j], n), pscale(x, A1[i][j]))
            f = padd(f, pscale(pmul(pmul(Aij, z[i]), z[j]), Fr(-1, 2)))
    cubic = {(0, 1, 2): Fr(3, 5), (1, 0, 2): Fr(-2, 3), (0, 0, 3): Fr(1, 9), (1, 1, 1): Fr(4, 7), (2, 1, 0): Fr(-1, 2)}
    for (i, j, k), cval in cubic.items():                        # sum c z_i^? ... encoded as exponents of (z1, z2, z3)
        term = pconst(cval, n)
        for idx, e in enumerate((i, j, k)):
            for _ in range(e):
                term = pmul(term, z[idx])
        term = pmul(term, padd(pconst(1, n), pscale(x, Fr(1, 6))))          # x-dependent cubic coefficients
        f = padd(f, term)
    # gradient in y vanishes on the ridge (quadratic and cubic parts vanish to first order at z = 0)
    grad_ok = all(psubst_y(pdiff(f, 1 + i), Q1) == {} for i in range(3))
    # left side: g(x) = f(x, Q(x)) = p(x), F = g', F'' = g'''
    g = psubst_y(f, Q1)
    p1 = {(k[0],): v for k, v in p.items()}
    lhs = pdiff(pdiff(pdiff(g, 0), 0), 0)
    # right side: f_xxx + 3 f_xxy[Q'] + 3 f_xyy[Q',Q'] + f_yyy[Q',Q',Q'] on the ridge
    dQ = [pdiff(q, 0) for q in Q1]
    c1 = 2 if MUT == "coefficient-two" else 3
    fx = pdiff(f, 0)
    fxx = pdiff(fx, 0)
    rhs = psubst_y(pdiff(fxx, 0), Q1)
    if MUT != "drop-cross-terms":
        for i in range(3):
            rhs = padd(rhs, pscale(pmul(psubst_y(pdiff(fxx, 1 + i), Q1), dQ[i]), c1))
            for j in range(3):
                rhs = padd(rhs, pscale(pmul(pmul(psubst_y(pdiff(pdiff(fx, 1 + i), 1 + j), Q1), dQ[i]), dQ[j]), 3))
                for k in range(3):
                    rhs = padd(rhs, pmul(pmul(pmul(psubst_y(pdiff(pdiff(pdiff(f, 1 + i), 1 + j), 1 + k), Q1), dQ[i]), dQ[j]), dQ[k]))
    naive = psubst_y(pdiff(fxx, 0), Q1)                          # F'' = f_xxx would be wrong on this family
    ok = grad_ok and g == p1 and lhs == rhs and lhs != naive
    return bool(ok), {"ridge_gradient_vanishes": grad_ok, "g_equals_p": g == p1, "identity_holds": lhs == rhs,
                      "correction_terms_live": lhs != naive, "lhs_degree": max((k[0] for k in lhs), default=0)}


# ---------------------------------------------------------------- 3. grid maximin (union-find in decreasing height)
def landscape(kind, r, lam, eps, beta):
    """Explicit landscapes on the cylinder; pins M = (-r/2, 0), S = (r/2, 0), f(M) = b, f(S) = b - r^3/6 (kappa = 1/6).
    p(x) = x^3/3 - r^2 x/4 + const so that p' = x^2 - r^2/4 vanishes at the pins and p(-r/2) - p(r/2) = r^3/6."""
    b = Fr(6, 5)
    r = Fr(r)
    lam, eps, beta = Fr(lam), Fr(eps), Fr(beta)
    c0 = b - ((-r / 2) ** 3 / 3 - r * r * (-r / 2) / 4)
    sign = -1 if MUT == "gap-sign" else 1

    def f(x, ys):
        val = c0 + sign * (Fr(x) ** 3 / 3 - r * r * Fr(x) / 4)
        if sign < 0:
            val = b - (val - b)                                  # mirror so that f(M) = b still holds and f(S) = b + r^3/6
        y1 = Fr(ys[0])
        ny2 = sum(Fr(yy) ** 2 for yy in ys)
        val += -(lam / 2) * ny2 + eps * (Fr(x) ** 2 - r * r / 4) * y1
        if kind == "rim":
            val += beta * ny2 * ny2
        return val

    # exact hypothesis data for the "good" landscapes: third-order blocks are constants
    if kind == "good":
        M3 = max(Fr(2), 2 * eps)
        M4 = Fr(0)
        lam_min = lam
        hyp = lam_min > 8 * r * M3 * M3 and r * M4 <= Fr(1, 20)
    else:
        # rim: f_yyy contains 24 beta y (norm up to 48 beta r on D) so M3 >= 48 beta r; M4 >= 24 beta
        M3 = max(Fr(2), 2 * eps, 48 * beta * r)
        M4 = 24 * beta
        lam_min = lam                                            # at M (y = 0) the transverse Hessian is -lam I
        hyp = lam_min > 8 * r * M3 * M3 and r * M4 <= Fr(1, 20)
    return f, b, b - r ** 3 / 6, hyp, {"M3": str(M3), "M4": str(M4), "lambda": str(lam_min), "depth_rhs_8rM3sq": str(8 * r * M3 * M3),
                                       "rM4": str(r * M4)}


def grid_maximin(f, b, r, dim, n):
    """Grid maximin level from M to {f > b} on D = [-2r, 2r] x [-2r, 2r]^(dim-1), spacing r/n (n even so that the
    pins and 0 are grid points). Cells are activated in decreasing height; the first height at which the component of M
    contains an older cell is the grid maximin level; the activating cell is the merge point."""
    r = Fr(r)
    h = r / n
    N = 4 * n + 1
    import itertools
    coords = [(-2 * r + i * h) for i in range(N)]
    shape = (N,) * dim
    idx_M = (int(Fr(3, 2) * n),) + (2 * n,) * (dim - 1)
    idx_S = (int(Fr(5, 2) * n),) + (2 * n,) * (dim - 1)
    vals = {}
    for idx in itertools.product(range(N), repeat=dim):
        vals[idx] = float(f(coords[idx[0]], [coords[i] for i in idx[1:]]))
    bf = float(b)
    order = sorted(vals, key=lambda t: -vals[t])
    parent = {}
    older = {}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, c):
        ra, rc = find(a), find(c)
        if ra == rc:
            return
        parent[rc] = ra
        older[ra] = older[ra] or older[rc]

    nbrs = [d for d in itertools.product((-1, 0, 1), repeat=dim) if any(d)]
    level, merge_cell, steps = None, None, 0
    for cell in order:
        parent[cell] = cell
        older[cell] = vals[cell] > bf
        for d in nbrs:
            nb = tuple(c + dd for c, dd in zip(cell, d))
            if nb in parent:
                union(cell, nb)
        steps += 1
        if idx_M in parent and older[find(idx_M)]:
            level, merge_cell = vals[cell], cell
            break
    dist_S = max(abs(a - c) for a, c in zip(merge_cell, idx_S)) if merge_cell else None
    return level, {"grid_maximin_level": "%.12g" % level if level is not None else None, "merge_cell_offset_from_S_in_steps": dist_S,
                   "cells": len(vals), "activated_before_merge": steps, "f_at_M": "%.12g" % vals[idx_M], "f_at_S": "%.12g" % vals[idx_S]}


def maximin_rule(dim, n, kind_override=None):
    r = Fr(1, 50)
    kind = kind_override or "good"
    f, b, s, hyp, data = landscape(kind, r, lam=1, eps=Fr(1, 2), beta=0 if kind == "good" else BETA_RIM)
    level, res = grid_maximin(f, b, r, dim, n)
    gap = float(r ** 3 / 6)
    tol = 1e-3 * gap
    ok = hyp and (float(s) - tol <= level <= float(s) + 1e-12) and res["merge_cell_offset_from_S_in_steps"] == 0
    res.update({"hypotheses_hold": hyp, "hypothesis_data": data, "s": "%.12g" % float(s), "tolerance": "%.3g" % tol, "kind": kind})
    return bool(ok), res


def load_bearing_rule(n):
    """The rim landscape violates (1) inside D and its elder partner is not S."""
    r = Fr(1, 50)
    f, b, s, hyp, data = landscape("rim", r, lam=1, eps=Fr(1, 2), beta=BETA_RIM)
    level, res = grid_maximin(f, b, r, 2, n)
    gap = float(r ** 3 / 6)
    # analytic rim pass: along x = -r/2 the profile b - lam y^2/2 + beta y^4 has its minimum b - lam^2/(16 beta) at y^2 = lam/(4 beta);
    # it lies inside D and above s exactly when lam^2/(16 beta) < r^3/6
    rim_level = float(b - Fr(1) / (16 * BETA_RIM))
    inside_D = Fr(1, 4 * BETA_RIM) < (2 * r) ** 2
    above_s = Fr(1) / (16 * BETA_RIM) < r ** 3 / 6
    ok = (not hyp) and inside_D and above_s and level > float(s) + 0.25 * gap and res["merge_cell_offset_from_S_in_steps"] > 2 \
        and abs(level - rim_level) < 0.5 * gap
    res.update({"hypotheses_hold": hyp, "hypothesis_data": data, "s": "%.12g" % float(s), "analytic_rim_pass_level": "%.12g" % rim_level,
                "rim_inside_D": bool(inside_D), "rim_pass_above_s": bool(above_s), "gap_kappa_r3": "%.6g" % gap})
    return bool(ok), res


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    args = ap.parse_args()
    MUT = args.mutant
    checks, detail = {}, {}
    checks["EXACT_CONSTANTS"], detail["EXACT_CONSTANTS"] = exact_constants()
    checks["RIDGE_IDENTITY_M3"], detail["RIDGE_IDENTITY_M3"] = ridge_identity_m3()
    checks["MAXIMIN_D2"], detail["MAXIMIN_D2"] = maximin_rule(2, 20, "rim" if MUT == "no-depth" else None)
    checks["MAXIMIN_D3"], detail["MAXIMIN_D3"] = maximin_rule(3, 12)
    checks["HYPOTHESIS_LOAD_BEARING"], detail["HYPOTHESIS_LOAD_BEARING"] = load_bearing_rule(40)
    out = {"object": "D1-CAP-ELDER-PARTNER-SECOND-PASS-20260930-v1", "checks": checks, "detail": detail,
           "passed": all(checks.values()) and len(checks) == 5,
           "scope": ("finite controls for the deterministic cap theorem and identity (11); the theorem itself is the written "
                     "derivation in REVIEW.md; not a proof about random fields; scientific effect NONE")}
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
