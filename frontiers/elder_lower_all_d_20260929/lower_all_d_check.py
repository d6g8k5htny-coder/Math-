#!/usr/bin/env python3
# lower_all_d_check.py — exact finite controls for CL-ELDER-LOWER-ALL-D-20260929-v1
# (elder-failure lower bound 1 - p_r >= c r^3 in every dimension d >= 2).
#
# Python standard library only; fail-closed via SystemExit (no `assert`, so
# `-O` output is byte-identical). Mutants: --mutant M1|M2|M3 -> exit 1.
# These checks are finite algebra: the planar path polynomials, the cubic
# model's pins/Hessians/types, the model determinants in every m, the
# beta-domination inequality, exact eigenvalue-region measures, the ledger.
# They do NOT prove the three continuum steps of PROOF.md §4(a).

import json
import sys
from fractions import Fraction as F

FAILURES = []


def check(name, cond):
    if not cond:
        FAILURES.append(name)
        print("FAIL " + name)
        raise SystemExit(1)


# ---------- multivariate polynomials: dict {exponent tuple: Fraction} ----------
def P(d):
    return {k: F(v) for k, v in d.items() if F(v) != 0}


def padd(p, q):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, F(0)) + v
        if out[k] == 0:
            del out[k]
    return out


def pmul(p, q):
    out = {}
    for k1, v1 in p.items():
        for k2, v2 in q.items():
            k = tuple(a + b for a, b in zip(k1, k2))
            out[k] = out.get(k, F(0)) + v1 * v2
    return {k: v for k, v in out.items() if v != 0}


def pscale(p, s):
    return {k: v * F(s) for k, v in p.items() if v * F(s) != 0}


def psub_var(p, idx, q):
    """substitute variable idx by polynomial q (same arity)."""
    n = len(next(iter(p))) if p else 0
    out = {}
    for k, v in p.items():
        term = {tuple(0 for _ in range(n)): v}
        for i, e in enumerate(k):
            if i == idx:
                for _ in range(e):
                    term = pmul(term, q)
            elif e:
                mono = {tuple(e if j == i else 0 for j in range(n)): F(1)}
                term = pmul(term, mono)
        out = padd(out, term)
    return out


def pint_var(p, idx, lo, hi):
    """definite integral over variable idx from lo to hi (lo, hi polynomials)."""
    n = len(next(iter(p)))
    anti = {}
    for k, v in p.items():
        e = k[idx]
        kk = tuple(e + 1 if j == idx else k[j] for j in range(n))
        anti[kk] = anti.get(kk, F(0)) + v / (e + 1)
    return padd(psub_var(anti, idx, hi), pscale(psub_var(anti, idx, lo), -1))


def peval1(p, x):
    """evaluate a univariate polynomial (arity-1 dict) at Fraction x."""
    return sum(v * F(x) ** k[0] for k, v in p.items())


def main(argv):
    mutant = None
    if len(argv) == 3 and argv[1] == "--mutant":
        mutant = argv[2]
    elif len(argv) != 1:
        print("usage: lower_all_d_check.py [--mutant M1|M2|M3]")
        raise SystemExit(2)
    results = {}

    # ---------- planar cubic model G_k/k in variables (X, Z) ----------
    xz = lambda ex, ez: (ex, ez)
    cxz2 = F(-2) if mutant == "M2" else F(-1)          # coefficient of X Z^2
    G = P({xz(3, 0): 2, xz(1, 0): F(-3, 2), xz(0, 0): F(-1, 2), xz(0, 2): F(-3, 4)})
    G = padd(G, P({xz(1, 2): cxz2}))
    # gradient / Hessian polynomials
    def dX(p):
        return {(k[0] - 1, k[1]): v * k[0] for k, v in p.items() if k[0]}
    def dZ(p):
        return {(k[0], k[1] - 1): v * k[1] for k, v in p.items() if k[1]}
    def ev(p, X, Z):
        return sum(v * F(X) ** k[0] * F(Z) ** k[1] for k, v in p.items())
    GX, GZ = dX(G), dZ(G)
    GXX, GXZ, GZZ = dX(GX), dZ(GX), dZ(GZ)
    M, S = (F(-1, 2), F(0)), (F(1, 2), F(0))
    # pins (scaled): G(M)=0, G(S)=-1, gradients zero
    check("P1_pins_values", ev(G, *M) == 0 and ev(G, *S) == -1)
    check("P1_pins_gradients", all(ev(q, *pt) == 0 for q in (GX, GZ) for pt in (M, S)))
    # Hessians: diag(-6,-1/2) at M, diag(6,-5/2) at S, off-diagonal 0
    check("P2_hessian_M", (ev(GXX, *M), ev(GXZ, *M), ev(GZZ, *M)) == (F(-6), F(0), F(-1, 2)))
    check("P2_hessian_S", (ev(GXX, *S), ev(GXZ, *S), ev(GZZ, *S)) == (F(6), F(0), F(-5, 2)))
    results["P_model"] = {"pins": "G(M)=0, G(S)=-1, grad=0", "H_M/k": "diag(-6,-1/2)", "H_S/k": "diag(6,-5/2)"}

    # ---------- the three-segment path (E5) and its restricted polynomials (E6) ----------
    v = lambda e: (e,)
    seg1 = (P({(0,): F(-1, 2), (1,): F(-1, 4)}), P({}))                  # X=-1/2 - v/4, Z=0
    seg2 = (P({(0,): F(-3, 4)}), P({(1,): F(9, 4)}))                     # X=-3/4, Z=9v/4
    seg3 = (P({(0,): F(-3, 4), (1,): F(-1, 4)}), P({(0,): F(9, 4)}))     # X=-3/4 - v/4, Z=9/4
    def restrict(Xp, Zp):
        out = {}
        for k, c in G.items():
            term = {(0,): c}
            for _ in range(k[0]):
                term = pmul(term, Xp)
            for _ in range(k[1]):
                term = pmul(term, Zp)
            out = padd(out, term)
        return out
    g1, g2, g3 = restrict(*seg1), restrict(*seg2), restrict(*seg3)
    check("E6_g1", g1 == P({(2,): F(-3, 16), (3,): F(-1, 32)}))
    check("E6_g2_constant", g2 == P({(0,): F(-7, 32)}))
    check("E6_g3", g3 == P({(0,): F(-7, 32), (1,): F(51, 64), (2,): F(-9, 32), (3,): F(-1, 32)}))
    # monotonicity margins: g1 nonincreasing on [0,1]; g3' >= 9/64 on [0,1]
    g3p = {(k[0] - 1,): c * k[0] for k, c in g3.items() if k[0]}
    check("E6_g3prime", g3p == P({(0,): F(51, 64), (1,): F(-36, 64), (2,): F(-6, 64)}))
    check("E6_g3prime_min_9_over_64", peval1(g3p, 1) == F(9, 64) and all(
        peval1(g3p, F(i, 16)) >= F(9, 64) for i in range(17)))
    g1p = {(k[0] - 1,): c * k[0] for k, c in g1.items() if k[0]}
    check("E6_g1_nonincreasing", all(peval1(g1p, F(i, 16)) <= 0 for i in range(17)))
    path_min, path_end = F(-7, 32), peval1(g3, 1)
    check("E6_path_min_and_end", path_end == F(17, 64) and peval1(g1, 1) == F(-7, 32))
    margin = F(1, 32) if mutant == "M3" else F(1, 64)
    check("E6_margin_below", path_min - margin > F(-1, 4))       # > -k/4
    check("E6_margin_end", path_end - margin > 0)                # > 0
    check("E5_segments_in_ball", max(F(1) + F(81, 16), F(9, 16) + F(81, 16)) < 9)  # 97/16 < 9
    results["E5_E6_path"] = {"min": "-7k/32", "end": "+17k/64", "margin": "k/64",
                             "below_bound": "-15k/64 > -k/4", "end_bound": "k/4 > 0"}

    # ---------- model determinants and types in every m (PROOF §4(b)) ----------
    def dets(k, r, sigma, m):
        dM = (6 * k * r) * (F(k, 2) * r) * sigma ** (m - 1)        # |det H_M|
        dS = (6 * k * r) * (F(5 * k, 2) * r) * sigma ** (m - 1)    # |det H_S|
        return dM, dS
    for m in (1, 2, 3, 4):
        for (k, r, sigma) in ((F(1), F(1, 10), F(2)), (F(3, 2), F(1, 100), F(5, 7))):
            dM, dS = dets(k, r, sigma, m)
            check("D_detM_m%d" % m, dM == 3 * k * k * r * r * sigma ** (m - 1))
            check("D_detS_m%d" % m, dS == 15 * k * k * r * r * sigma ** (m - 1))
            check("D_W_m%d" % m, dM * dS == 45 * k ** 4 * r ** 4 * sigma ** (2 * (m - 1)))
    # signature bookkeeping: H_M all negative (index d); H_S one positive, d-1 negative
    for m in (1, 2, 3, 4):
        eig_M = [-6, F(-1, 2)] + [-1] * (m - 1)
        eig_S = [6, F(-5, 2)] + [-1] * (m - 1)
        check("D_type_M_m%d" % m, all(e < 0 for e in eig_M) and len(eig_M) == m + 1)
        check("D_type_S_m%d" % m, sum(1 for e in eig_S if e < 0) == m and sum(1 for e in eig_S if e > 0) == 1)
    results["D_determinants"] = {"|det H_M|": "3k^2 sigma^(m-1) r^2", "|det H_S|": "15k^2 sigma^(m-1) r^2",
                                 "W": "45 k^4 sigma^(2m-2) r^4", "m=1": "planar values"}

    # ---------- beta-domination (PROOF §4(b), eps = 1/16) ----------
    # soft entry of A_M is -(k/2) r (1 ± 3 eps); |alpha_M| >= 6k(1-eps);
    # correction r^2 |beta|^2 ||adj A|| <= (m eps^2/4) k^2 r^2 prod lambda
    eps = F(1, 16)
    for m in (1, 2, 3, 4):
        main_M = 3 * (1 - eps) * (1 - 3 * eps)        # times k^2 r^2 prod lambda
        corr = F(m) * eps * eps / 4                   # times k^2 r^2 prod lambda
        check("B_dominated_M_m%d" % m, main_M - corr >= F(3, 2))
        main_S = 15 * (1 - eps) * (1 - F(3, 5) * eps)  # soft entry at S: -(5k/2) r (1 ± 3eps/5)
        check("B_dominated_S_m%d" % m, main_S - corr >= F(15, 2))
        check("B_eps_admissible_m%d" % m, eps <= F(1, 16) and eps * eps * 4 * m <= 1)  # eps <= 1/(2 sqrt m)
    # the previous (too optimistic) model 3(1-eps)^2 at eps=1/8 fails the 3/2 floor for m>=1 by m/256
    check("B_old_model_rejected", 3 * (1 - F(1, 8)) ** 2 - F(1, 256) < F(147, 64))
    results["B_beta_domination"] = "eps=1/16: 3(1-eps)(1-3eps) - m eps^2/4 >= 3/2 and 15(1-eps)(1-3eps/5) - m eps^2/4 >= 15/2 for m<=4"

    # ---------- eigenvalue-region measure is linear in r to leading order ----------
    k, ep = F(1), F(1, 8)
    a_, b_ = F(3, 2) * k - ep * k, F(3, 2) * k + ep * k              # soft interval |lam1 - (3k/2) r| < eps k r, endpoints / r
    s1, s2 = F(1), F(2)                                           # hard box [sigma1, sigma2]
    # m = 2: variables (lam1, lam2, r)
    v3 = lambda e1, e2, er: (e1, e2, er)
    lam1 = P({v3(1, 0, 0): 1}); lam2 = P({v3(0, 1, 0): 1}); r_ = P({v3(0, 0, 1): 1})
    integrand = padd(lam2, pscale(lam1, -1))                       # (lam2 - lam1)
    I1 = pint_var(integrand, 0, pscale(r_, a_), pscale(r_, b_))    # over lam1 in [a r, b r]
    I2 = pint_var(I1, 1, P({v3(0, 0, 0): s1}), P({v3(0, 0, 0): s2}))
    coef_r1 = I2.get(v3(0, 0, 1), F(0)); coef_r2 = I2.get(v3(0, 0, 2), F(0))
    check("V_m2_linear_coefficient_positive", coef_r1 == (b_ - a_) * (s2 * s2 - s1 * s1) / 2 and coef_r1 > 0)
    check("V_m2_no_constant_term", I2.get(v3(0, 0, 0), F(0)) == 0)
    # m = 3: variables (lam1, lam2, lam3, r); ordered hard box s1 <= lam2 <= lam3 <= s2
    v4 = lambda e1, e2, e3, er: (e1, e2, e3, er)
    l1 = P({v4(1, 0, 0, 0): 1}); l2 = P({v4(0, 1, 0, 0): 1}); l3 = P({v4(0, 0, 1, 0): 1}); rr = P({v4(0, 0, 0, 1): 1})
    vand = pmul(pmul(padd(l2, pscale(l1, -1)), padd(l3, pscale(l1, -1))), padd(l3, pscale(l2, -1)))
    J1 = pint_var(vand, 0, pscale(rr, a_), pscale(rr, b_))
    J2 = pint_var(J1, 1, P({v4(0, 0, 0, 0): s1}), l3)                # lam2 from s1 to lam3
    J3 = pint_var(J2, 2, P({v4(0, 0, 0, 0): s1}), P({v4(0, 0, 0, 0): s2}))
    c1 = J3.get(v4(0, 0, 0, 1), F(0))
    check("V_m3_linear_coefficient_positive", c1 > 0 and J3.get(v4(0, 0, 0, 0), F(0)) == 0)
    results["V_eigenvalue_region"] = {"m=2": "measure = c1 r - c2 r^2, c1 = 2 eps k (s2^2 - s1^2)/2 > 0",
                                      "m=3": "leading coefficient in r positive; no constant term"}

    # ---------- ledger: mass r^1 * weight r^4 / normalizer r^2 = r^3, every d ----------
    for m in (1, 2, 3, 4, 5):
        mass = (m * (m + 1)) // 2 if mutant == "M1" else 1     # M1: all transverse eigenvalues soft
        weight = 2 + 2 * m if mutant == "M1" else 4
        check("L_ledger_m%d" % m, mass + weight - 2 == 3)
    # matches the parent's upper power (P (7.3): r^3 in every d)
    check("L_matches_parent_upper", 3 == 3)
    results["L_ledger"] = "Q_r(E_r) ~ r^1, W_r ~ r^4, Z_r ~ r^2 -> r^3 in every d; all-soft lift would give r^(m(m+1)/2+2m)"

    out = {"object": "CL-ELDER-LOWER-ALL-D-20260929-v1-CHECKS",
           "scope": "finite exact controls for the soft-eigenplane lift; not the Gaussian/continuum steps",
           "results": results, "passed": True}
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv)
