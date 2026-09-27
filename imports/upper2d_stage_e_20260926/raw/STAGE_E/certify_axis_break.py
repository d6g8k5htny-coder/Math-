#!/usr/bin/env python3
# certify_axis_break.py — STAGE-E certified point violation of the named
# lemma H5-AXIS v1 (M-backward wedge flat envelope), H5_CLOSURE.md §1:
#   "Envelope rho_w <= C over each wedge, C = 2x edge probes ..."
#   M-backward wedge: {d_M < 0.074, theta_M > 170 deg}; merged constant
#   mbwd_C = 1.6522e-05 (2x max probe rho_hi, probes at thM in {171,176} x
#   dl in {0.012,0.03,0.06}).
# The machine cover SKIPS patches entirely inside the wedge
# (h5_run.in_axis_envelope: dM<0.074 & thM>170), so the named lemma is the
# ONLY cover there.  We certify rho_w(y0) > mbwd_C at an interior point
# y0 = M + 0.05*(cos 170.5 deg, sin 170.5 deg).
#
# Method (fully certified, no Monte Carlo):
#   rho_w(y) = pgrad * I / Z,  I = s_t * int_{window} phi_std(t) g(t) dt
#   g(t) = E[ |dM| 1{dM>0,tM<0} |dS| 1{dS<0} |dy| 1{dy<0} ; N(mu(t), S_H) ]
#   Lower bound: pick t0 in-window, an axis-aligned 9-box B = mu(t0) +- k*sig
#   on which interval evaluation certifies the typing AND determinant floors
#   m_M, m_S, m_y; over t in [t0-tau, t0+tau] the box keeps margin >= kap'
#   in sigma units; union-bound Mills gives P(B|t) >= P_lo; then
#   I >= s_t * 2*tau * phi_lo * m_M*m_S*m_y * P_lo,  and
#   rho_lo = pgrad_lo * I_lo / Z_hi  (Z_hi = 1.3970321e-2, H5 certified hi).
# Station law: recomputed twice at dps=120 and dps=160 from the campaign's
# frozen exact kernel (cov_exact.py, hash-pinned) and cross-agreed to 1e-25
# relative; scalars then treated with +-1e-20 relative safety intervals.
# Discipline: fail-closed ck; deterministic; no floats in digest;
# python3 / python3 -O byte-identical.
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
C1DIR = os.path.join(ROOT, "C1_alpha_intensity")
H2DIR = os.path.join(ROOT, "H2_foundations")
sys.path.insert(0, C1DIR)
sys.path.insert(0, H2DIR)

from mpmath import mp, mpf, pi, cos, sin, sqrt, exp
import mpmath

COV_EXACT_SHA256 = "f08c1c5f653f2ffd2e85d39e1112f80d15db04d15f932e5ee42db2ca3553e783"
MBWD_C = mpf("1.6522e-05")   # merged envelope constant (>= true last-wins)
Z_HI = mpf("1.3970321e-02")  # H5 certified Z upper (h5_totals / D1 quotes)


def ck(cond, msg):
    if not cond:
        print("STAGE-E AXIS CERTIFICATION FAILED:", msg)
        raise SystemExit(1)


def _sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


ck(_sha256(os.path.join(H2DIR, "cov_exact.py")) == COV_EXACT_SHA256,
   "cov_exact.py hash drift")


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


# --- exact station, cross-computed at two precisions -----------------------
TH = mpf("170.5")
DL = mpf("0.05")
import c1_grid as CG
R = CG.R
xs = -R/2 + DL*cos(TH*pi/180)
ys = DL*sin(TH*pi/180)

stats = []
for dps in (120, 160):
    mp.dps = dps
    gl = CG.GridLaw(CG.R)
    st = station_at(gl, xs, ys)
    stats.append(st)
mp.dps = 120
st = stats[0]
REL = mpf("1e-25")
for key in ("pgrad", "mu_t", "s_t2"):
    d = abs(stats[0][key] - stats[1][key])
    ck(d <= REL*abs(stats[0][key]) + mpf("1e-60"),
       "station cross-precision disagreement in %s: %s" % (key, mp.nstr(d, 3)))
for k in range(9):
    d = abs(stats[0]["mu_H"][k] - stats[1]["mu_H"][k])
    ck(d <= REL*(abs(stats[0]["mu_H"][k]) + 1) + mpf("1e-60"),
       "station mu_H disagreement")
    d = abs(stats[0]["c_v"][k] - stats[1]["c_v"][k])
    ck(d <= REL*(abs(stats[0]["c_v"][k]) + 1) + mpf("1e-60"),
       "station c_v disagreement")
    d = abs(stats[0]["S_H"][k, k] - stats[1]["S_H"][k, k])
    ck(d <= REL*(abs(stats[0]["S_H"][k, k]) + 1) + mpf("1e-60"),
       "station S_H diag disagreement")

iv = mpmath.iv
iv.dps = 100
SAFE = mpf("1.0000000001")   # generous relative safety on station scalars

pgrad_lo = st["pgrad"]/SAFE
s_t_lo = sqrt(st["s_t2"])/SAFE
mu_H = [st["mu_H"][k] for k in range(9)]
c_v = [st["c_v"][k] for k in range(9)]
sig = [sqrt(st["S_H"][k, k])*SAFE for k in range(9)]
mu_t = st["mu_t"]
s_t = sqrt(st["s_t2"])
B, ELL = CG.B, CG.ELL
t_lo = (B - ELL - mu_t)/s_t
t_hi = (B - mu_t)/s_t
ck(t_lo < 0 < t_hi, "window does not straddle the needle center")

# --- certified box bound ----------------------------------------------------
def mills_hi(x):  # certified upper on Phibar(x), x > 0, interval arithmetic
    x = iv.mpf(x)
    return iv.exp(-x*x/2)/(x*iv.sqrt(2*iv.pi))


best = None
for t0s in ["0.0", "0.2", "-0.2", "0.4", "-0.4"]:
    t0 = mpf(t0s)
    if not (t_lo < t0 < t_hi):
        continue
    mu0 = [mu_H[k] + c_v[k]*s_t*t0 for k in range(9)]
    for kap in ["2", "2.5", "3", "3.5", "4", "4.5", "5", "6"]:
        kappa = mpf(kap)
        half = [kappa*sig[k] for k in range(9)]
        # interval typing + determinant floors over B
        X = [iv.mpf([float(mu0[k]-half[k]), float(mu0[k]+half[k])])
             for k in range(9)]
        dM = X[0]*X[2] - X[1]*X[1]
        tM = X[0] + X[2]
        dS = X[3]*X[5] - X[4]*X[4]
        dy = X[6]*X[8] - X[7]*X[7]
        if not (dM.a > 0 and tM.b < 0 and dS.b < 0 and dy.b < 0):
            continue
        m0 = dM.a*(-dS.b)*(-dy.b)   # |dM| |dS| |dy| floor on B
        # tau range keeping margins >= kap2 sigma
        for kap2 in ["1.5", "2", "2.5", "3", "3.5", "4"]:
            k2 = mpf(kap2)
            if k2 >= kappa - mpf("0.25"):
                continue
            # |c_v_k| s_t tau <= (kappa - k2) sig_k
            taus = []
            for k in range(9):
                if abs(c_v[k])*s_t > 0:
                    taus.append((kappa - k2)*sig[k]/(abs(c_v[k])*s_t))
            tau = mpf("0.9")*min(taus)
            if tau <= 0:
                continue
            tA = max(t0 - tau, t_lo)
            tB = min(t0 + tau, t_hi)
            if not (tA < t0 < tB):
                continue
            # worst margins over [tA, tB]
            P_lo = mpf(1)
            ok = True
            for k in range(9):
                dev = abs(c_v[k])*s_t*max(abs(tA - t0), abs(tB - t0))
                marg = (half[k] - dev)/sig[k]
                if marg <= k2:
                    ok = False
                    break
                P_lo -= 2*mills_hi(mp.nstr(marg, 30)).b
            if not ok or P_lo <= 0:
                continue
            # phi floor on [tA, tB]
            t_end = max(abs(tA), abs(tB))
            phi_lo = exp(-t_end**2/2)/sqrt(2*pi)/SAFE
            I_lo = s_t_lo*(tB - tA)*phi_lo*m0*P_lo/SAFE
            rho_lo = pgrad_lo*I_lo/Z_HI/SAFE
            if best is None or rho_lo > best[0]:
                best = (rho_lo, t0s, kap, kap2, tA, tB, m0, P_lo, phi_lo)

ck(best is not None, "no certified box configuration found")
rho_lo, t0s, kap, kap2, tA, tB, m0, P_lo, phi_lo = best
print("certified point lower bound at (th_M=170.5 deg, d_M=0.05):")
print("  t0=%s kappa=%s margin>=%s sigma" % (t0s, kap, kap2))
print("  determinant floor m0 =", mp.nstr(m0, 6))
print("  P_lo =", mp.nstr(P_lo, 6), " phi_lo =", mp.nstr(phi_lo, 6))
print("  window sub-interval width =", mp.nstr(tB - tA, 6))
print("  rho_lo =", mp.nstr(rho_lo, 8))
print("  envelope constant mbwd_C =", mp.nstr(MBWD_C, 8))
print("  ratio =", mp.nstr(rho_lo/MBWD_C, 8))
ck(rho_lo > MBWD_C, "certified lower bound does not exceed the envelope")
ck(rho_lo > 2*MBWD_C, "margin under 2x")

DIG = hashlib.sha256()
for s in ["point=170.5/0.05", "t0=%s" % t0s, "kap=%s/%s" % (kap, kap2),
          "rho_lo=%s" % mp.nstr(rho_lo, 20), "mbwd_C=%s" % mp.nstr(MBWD_C, 10),
          "VERDICT=H5-AXIS-v1-pointwise-FALSE"]:
    DIG.update(s.encode())
print("STAGE-E H5-AXIS BREAK CERTIFIED digest=%s" % DIG.hexdigest())
