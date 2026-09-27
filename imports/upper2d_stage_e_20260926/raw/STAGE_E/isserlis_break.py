#!/usr/bin/env python3
# isserlis_break.py — STAGE-E certified pointwise violation of named lemma
# H5-AXIS v1 (M-backward wedge flat envelope rho_w <= mbwd_C = 1.6522e-5,
# wedge {d_M < 0.074, theta_M > 170 deg}; machine cover skips the wedge
# interior, so the named lemma is the only cover).
#
# rho_w(y) = pgrad * I / Z,  I = int_{t in window} phi_std(t) g(t) dt,
# g(t) = E[ h_M h_S h_Y ; N(mu(t), S_H) ],  h_block = |det| 1{typed}.
#
# Certified lower bound on g over a t-interval V0:
#   P6(X) = (X0 X2 - X1^2)(X4^2 - X3 X5)(X7^2 - X6 X8)  (= h on typed set)
#   g = E[P6 1{typed}] = E[P6] - E[P6 1{not typed}]
#     >= E[P6] - sqrt( E[P6^2] * P(not typed) )
#   * E[P6](t): exact Isserlis degree-6 moment, interval means over V0.
#   * E[P6^2](t0): exact Isserlis degree-12 moment at t0 (mp, memoized
#     pairings); uniformity over V0 via E[P6(t)^2] <= 2 E[P6(t0)^2] +
#     2 E[Delta^2], Delta = P6(t)-P6(t0), E[Delta^2] bounded by crude
#     certified 1-dim raw-moment Holder (correction term only).
#   * P(not typed) <= P(X notin B) with B a kappa-sigma box certified
#     typed by interval determinant evaluation; tails via certified Mills.
# Station law recomputed at dps=120 and dps=160 and cross-agreed.
# Deterministic, fail-closed, python3 / -O byte-identical, no floats in
# the digest.
import hashlib
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "C1_alpha_intensity"))
sys.path.insert(0, os.path.join(ROOT, "H2_foundations"))

from mpmath import mp, mpf, pi, cos, sin, sqrt, exp
import mpmath

COV_EXACT_SHA256 = "f08c1c5f653f2ffd2e85d39e1112f80d15db04d15f932e5ee42db2ca3553e783"
MBWD_C = mpf("1.6522e-05")
Z_HI = mpf("1.3970321e-02")


def ck(cond, msg):
    if not cond:
        print("STAGE-E ISSERLIS CERTIFICATION FAILED:", msg)
        raise SystemExit(1)


def _sha256(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


ck(_sha256(os.path.join(ROOT, "H2_foundations", "cov_exact.py"))
   == COV_EXACT_SHA256, "cov_exact.py hash drift")

import c1_grid as CG


def station_at(gl, x, y):
    yp = (mpf(x), mpf(y))
    y_pts = ([(yp[0], yp[1], k) for k in ("f", "fx", "fy")]
             + [(yp[0], yp[1], k) for k in ("fxx", "fxy", "fyy")])
    Gyx = gl._gram(y_pts, gl.shared_pts)
    Gyy = gl._gram(y_pts, y_pts)
    G = mp.zeros(18, 18)
    for i in range(12):
        for j in range(12):
            G[i, j] = gl.G12[i, j]
    for i in range(6):
        for j in range(12):
            G[12 + i, j] = Gyx[i, j]
            G[j, 12 + i] = Gyx[i, j]
    for i in range(6):
        for j in range(6):
            G[12 + i, 12 + j] = Gyy[i, j]
    return gl._condition(G, 0, mpf(0), yp)


# ---------------- Isserlis engine (mean/cov, any backend) ------------------
class Isserlis:
    """Mixed moments E[prod X_i] for X ~ N(mu, Sigma); works with mp or iv."""

    def __init__(self, mu, Sigma):
        self.mu = list(mu)
        self.S = [[Sigma[i, j] for j in range(len(mu))] for i in range(len(mu))]
        self.cache = {}

    def moment(self, idx):
        idx = tuple(sorted(idx))
        if not idx:
            return self.mu[0]*0 + 1
        if idx in self.cache:
            return self.cache[idx]
        # pair first element with another, or leave as singleton (mean)
        i0 = idx[0]
        rest = idx[1:]
        tot = self.mu[i0]*self.moment(rest) if False else None
        # recurrence: E[X_i0 * prod rest] = mu_i0 E[prod rest]
        #     + sum_{j in rest} S_i0j E[prod rest\{j}]
        tot = self.mu[i0]*self.moment(rest)
        for k, j in enumerate(rest):
            tot = tot + self.S[i0][j]*self.moment(rest[:k] + rest[k + 1:])
        self.cache[idx] = tot
        return tot


# P6 = sum sign * monomial(6 indices)
BLOCKS = ((0, 1, 2), (3, 4, 5), (6, 7, 8))
# dM = X0 X2 - X1^2 ; -dS = X4^2 - X3 X5 ; -dy = X7^2 - X6 X8
QUAD = [((0, 2), (1, 1)), ((4, 4), (3, 5)), ((7, 7), (6, 8))]
MONOS = []
for sgn_bits in itertools.product((0, 1), repeat=3):
    sgn = (-1)**sum(sgn_bits)
    m = tuple(sorted(QUAD[b][sgn_bits[b]] for b in range(3)))
    MONOS.append((sgn, tuple(sorted(sum((list(t) for t in m), [])))))


def E_P6(iser):
    return sum(s*iser.moment(m) for s, m in MONOS)


def E_P6sq(iser):
    tot = 0
    for s1, m1 in MONOS:
        for s2, m2 in MONOS:
            tot = tot + s1*s2*iser.moment(tuple(sorted(m1 + m2)))
    return tot


def raw_moment_bound(mu_k, sg_k, pw):
    """E[X^pw] for X ~ N(mu, sg^2), exact closed form (pw even)."""
    tot = mpf(0)
    for kk in range(pw//2 + 1):
        tot += mpf(mp.binomial(pw, 2*kk)) * mpf(mp.faculty2(2*kk - 1)) \
            * abs(mu_k)**(pw - 2*kk) * sg_k**(2*kk)
    return tot


def certify_point(gl, xs, ys, t0, w, kappa, tag):
    st = station_at(gl, xs, ys)
    mu_H = [st["mu_H"][k] for k in range(9)]
    c_v = [st["c_v"][k] for k in range(9)]
    s_t = sqrt(st["s_t2"])
    S_H = st["S_H"]
    sig = [sqrt(S_H[k, k]) for k in range(9)]
    B, ELL = CG.B, CG.ELL
    mu_t = st["mu_t"]
    t_lo = (B - ELL - mu_t)/s_t
    t_hi = (B - mu_t)/s_t
    tA, tB = max(t_lo, t0 - w), min(t_hi, t0 + w)
    ck(tA < t0 < tB, "%s: V0 outside window" % tag)

    # --- E[P6] over V0 with interval means ----------------------------------
    iv = mpmath.iv
    iv.dps = 90
    t_iv = iv.mpf([float(tA), float(tB)])
    mu_iv = [iv.mpf(mu_H[k]) + iv.mpf(c_v[k]*s_t)*t_iv for k in range(9)]
    S_iv = [[iv.mpf(S_H[i, j]) for j in range(9)] for i in range(9)]
    iser_iv = Isserlis(mu_iv, S_iv)
    e6_iv = E_P6(iser_iv)
    ck(e6_iv.a > 0, "%s: E[P6] interval not positive" % tag)
    e6_lo = mpf(e6_iv.a)

    # --- E[P6^2] at t0 (exact mp) + Delta^2 crude bound ---------------------
    mu0 = [mu_H[k] + c_v[k]*s_t*t0 for k in range(9)]
    iser0 = Isserlis(mu0, S_H)
    e6sq0 = E_P6sq(iser0)
    ck(e6sq0 > 0, "%s: E[P6^2] <= 0" % tag)
    # Delta bound: E[(P6(t)-P6(t0))^2] <= (sum_j w^j sqrt(E[A_j^2]))^2,
    # E[A_j^2] bounded crudely (correction only) via 1-dim raw moments.
    gam = [c_v[k]*s_t for k in range(9)]
    sq_sum = mpf(0)
    for j in (1, 2, 3):
        a_j = mpf(0)
        for s, m in MONOS:
            for T in itertools.combinations(range(6), j):
                gt = mpf(1)
                rem = []
                for k in range(6):
                    if k in T:
                        gt *= abs(gam[m[k]])
                    else:
                        rem.append(m[k])
                # E[(prod rem)^2] <= prod (E X^{2*|rem|})^{1/|rem|}
                if rem:
                    pw = 2*len(rem)
                    bnd = mpf(1)
                    for k in rem:
                        bnd *= raw_moment_bound(mu0[k], sig[k], pw)**(mpf(1)/len(rem))
                else:
                    bnd = mpf(1)
                a_j += gt*sqrt(bnd)
        sq_sum += w**j * a_j
    e6sq_hi = 2*e6sq0 + 2*sq_sum**2 * mpf("4")  # x4 safety on correction

    # --- P(not typed) <= P(not in kappa-box), tails over V0 -----------------
    ivt = mpmath.iv
    half = [kappa*sig[k] for k in range(9)]
    X = [ivt.mpf([float(mu0[k] - half[k]), float(mu0[k] + half[k])])
         for k in range(9)]
    dM = X[0]*X[2] - X[1]*X[1]
    tM = X[0] + X[2]
    dS = X[3]*X[5] - X[4]*X[4]
    dy = X[6]*X[8] - X[7]*X[7]
    ck(dM.a > 0 and tM.b < 0 and dS.b < 0 and dy.b < 0,
       "%s: kappa-box not certified typed" % tag)
    dev_max = [abs(c_v[k])*s_t*max(abs(tA - t0), abs(tB - t0)) for k in range(9)]
    Pnt = mpf(0)
    for k in range(9):
        marg = (half[k] - dev_max[k])/sig[k]
        ck(marg > 3, "%s: box margin under 3 sigma" % tag)
        x = ivt.mpf(mp.nstr(marg, 30))
        Pnt += 2*mpf((ivt.exp(-x*x/2)/(x*ivt.sqrt(2*ivt.pi))).b)
    CS = sqrt(e6sq_hi*Pnt)

    g_lo = e6_lo - CS
    ck(g_lo > 0, "%s: g_lo not positive" % tag)
    t_end = max(abs(tA), abs(tB))
    phi_lo = exp(-t_end**2/2)/sqrt(2*pi)
    I_lo = (tB - tA)*phi_lo*g_lo
    pgrad_lo = st["pgrad"]*mpf("0.999999")
    rho_lo = pgrad_lo*I_lo/Z_HI*mpf("0.999")
    print("  [%s] e6_lo=%s  sqrt(E[P6^2]*Pnt)=%s  g_lo=%s"
          % (tag, mp.nstr(e6_lo, 6), mp.nstr(CS, 4), mp.nstr(g_lo, 6)))
    print("  [%s] I_lo=%s  rho_lo=%s  vs C=%s  ratio=%s"
          % (tag, mp.nstr(I_lo, 6), mp.nstr(rho_lo, 6), mp.nstr(MBWD_C, 4),
             mp.nstr(rho_lo/MBWD_C, 4)))
    return rho_lo, g_lo, e6_lo, CS, e6sq0, Pnt


def main():
    stats = {}
    for dps in (120, 160):
        mp.dps = dps
        gl = CG.GridLaw(CG.R)
        stats[dps] = gl
    mp.dps = 120
    gl = stats[120]
    R = CG.R

    # cross-precision agreement of station law at both attack points
    pts = [("170.2", "0.05"), ("170.5", "0.045")]
    for ths, dls in pts:
        th, dl = mpf(ths), mpf(dls)
        x = -R/2 + dl*cos(th*pi/180)
        y = dl*sin(th*pi/180)
        s1 = station_at(stats[120], x, y)
        s2 = station_at(stats[160], x, y)
        for key in ("pgrad", "mu_t", "s_t2"):
            d = abs(s1[key] - s2[key])
            ck(d <= mpf("1e-25")*abs(s1[key]) + mpf("1e-60"),
               "station disagreement %s at %s" % (key, ths))

    best = None
    for ths, dls, t0, w, kap in [("170.2", "0.05", "0.0", "0.55", "5.5"),
                                 ("170.5", "0.045", "0.0", "0.55", "5.5")]:
        th, dl = mpf(ths), mpf(dls)
        x = -R/2 + dl*cos(th*pi/180)
        y = dl*sin(th*pi/180)
        out = certify_point(gl, x, y, mpf(t0), mpf(w), mpf(kap),
                            "%s/%s" % (ths, dls))
        if best is None or out[0] > best[0]:
            best = (out[0], ths, dls) + out[1:]
    rho_lo = best[0]
    ck(rho_lo > MBWD_C, "certified rho_lo does not exceed envelope constant")
    print("BEST: point (th_M=%s deg, d_M=%s): certified rho_lo=%s > mbwd_C=%s"
          % (best[1], best[2], mp.nstr(rho_lo, 6), mp.nstr(MBWD_C, 4)))
    print("ratio =", mp.nstr(rho_lo/MBWD_C, 6))
    DIG = hashlib.sha256()
    for s in ["pt=%s/%s" % (best[1], best[2]),
                      "rho_lo=%s" % mp.nstr(rho_lo, 20),
                      "C=%s" % mp.nstr(MBWD_C, 10),
                      "VERDICT=H5-AXIS-v1-pointwise-FALSE"]:
        DIG.update(s.encode())
    print("STAGE-E H5-AXIS BREAK CERTIFIED digest=%s" % DIG.hexdigest())


main()
