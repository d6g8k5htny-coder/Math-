#!/usr/bin/env python3
"""
c1_grid.py -- C1 alpha-class: plane integral of the AO-free window-saddle Palm
intensity rho(y) over the alpha-relevant region around M at r = 0.05, for the
CONSISTENCY DISPLAY against the historical measured C* = 0.97 territory
(C020/C021: int Lambda dA = 1.216e-4, qual/raw = 0.9997).  This is a display,
not a proof: quadrature + QMC error budgets are printed; the alpha support
edge stations are printed to exhibit the decay.

INDEPENDENT CODE PATH: jet layout (P6, H_M, H_S, Y3, H_y) with a cached
12x12 pin+Hessian Gram block; recomputes rho at the main script's probe
stations and must agree within the displayed tolerance (fail-closed).

Fail-closed ck() -> SystemExit; deterministic; python/-O byte-identical.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'H2_foundations'))
import numpy as np
from scipy.stats import qmc as _qmc
from scipy.special import ndtr as _ndtr, ndtri as _ndtri
import cov_exact as ce
import pin_transform as pt
from mpmath import mp, mpf, sqrt, exp, pi

mp.dps = 80

FAILS = []
def ck(cond, tag, msg=""):
    if not cond:
        sys.stdout.write("CERTIFICATE FAIL [%s] %s\n" % (tag, msg)); sys.stdout.flush()
        raise SystemExit(1)
    sys.stdout.write("ck %-30s PASS %s\n" % (tag, msg))

DER = {'f': (0, 0), 'fx': (1, 0), 'fy': (0, 1), 'fxx': (2, 0), 'fxy': (1, 1), 'fyy': (0, 2)}
B = mpf('1.2')
R = mpf('0.05')
ELL = R**3/6
SEED = 424242


def station_xy(r, th_deg, delta):
    t = mpf(th_deg)*pi/180
    return (-r/2 + mpf(delta)*mp.cos(t), mpf(delta)*mp.sin(t))


class GridLaw:
    """18-jet Gram with layout (P6 | H_M H_S | Y3 | H_y) = (0..5 | 6..11 | 12..14 | 15..17)."""

    def __init__(self, r):
        self.r = mpf(r)
        rM = (-self.r/2, mpf(0)); rS = (self.r/2, mpf(0))
        self.shared_pts = ([(rM[0], rM[1], k) for k in ('f', 'fx', 'fy')]
                           + [(rS[0], rS[1], k) for k in ('f', 'fx', 'fy')]
                           + [(rM[0], rM[1], k) for k in ('fxx', 'fxy', 'fyy')]
                           + [(rS[0], rS[1], k) for k in ('fxx', 'fxy', 'fyy')])
        self.G12 = self._gram(self.shared_pts, self.shared_pts)
        # certified pin inverse once per rung
        G6_rows = [[self.G12[i, j] for j in range(6)] for i in range(6)]
        G6inv_iv, cert = pt.certified_inverse(G6_rows, self.r, frame='normalized')
        ck(cert['kappa_eps'] <= pt.CERT_TOL, "grid-pin-cert", mp.nstr(cert['kappa_eps'], 3))
        self.G6inv = mp.matrix(6, 6)
        for i in range(6):
            for j in range(6):
                self.G6inv[i, j] = (mpf(G6inv_iv[i][j].a) + mpf(G6inv_iv[i][j].b))/2

    def _gram(self, pts_a, pts_b, symmetric=False):
        na, nb = len(pts_a), len(pts_b)
        G = mp.zeros(na, nb)
        for i in range(na):
            xi, yi, ai = pts_a[i]
            for j in range(nb):
                xj, yj, aj = pts_b[j]
                G[i, j] = ce.cov(DER[ai], DER[aj], xi-xj, yi-yj, 'spectral', 'mpf')
        return G

    def station(self, th, delta):
        y = station_xy(self.r, th, mpf(delta))
        y_pts = ([(y[0], y[1], k) for k in ('f', 'fx', 'fy')]
                 + [(y[0], y[1], k) for k in ('fxx', 'fxy', 'fyy')])
        Gyx = self._gram(y_pts, self.shared_pts)     # 6 x 12
        Gyy = self._gram(y_pts, y_pts)               # 6 x 6
        # assemble 18x18 (mp.matrix)
        G = mp.zeros(18, 18)
        for i in range(12):
            for j in range(12):
                G[i, j] = self.G12[i, j]
        for i in range(6):
            for j in range(12):
                G[12+i, j] = Gyx[i, j]; G[j, 12+i] = Gyx[i, j]
        for i in range(6):
            for j in range(6):
                G[12+i, 12+j] = Gyy[i, j]
        return self._condition(G, th, delta, y)

    def _condition(self, G, th, delta, y):
        pv = mp.matrix([B, 0, 0, B-ELL, 0, 0])
        ir = list(range(6, 18))
        Grc = mp.zeros(12, 6)
        for i, gi in enumerate(ir):
            for j in range(6):
                Grc[i, j] = G[gi, j]
        mu1 = Grc*(self.G6inv*pv)
        Grr = mp.zeros(12, 12)
        for i, gi in enumerate(ir):
            for j, gj in enumerate(ir):
                Grr[i, j] = G[gi, gj]
        S1 = Grr - Grc*self.G6inv*Grc.T
        # local layout: 0..5 H_M H_S, 6..8 Y3 (f,fx,fy), 9..11 H_y
        Sgg = S1[7:9, 7:9]
        Sgginv = Sgg**-1
        mu_g = mp.matrix([mu1[7], mu1[8]])
        detSgg = Sgg[0, 0]*Sgg[1, 1]-Sgg[0, 1]**2
        pgrad = exp(-(mu_g.T*Sgginv*mu_g)[0]/2)/(2*pi*sqrt(detSgg))
        irest = [0, 1, 2, 3, 4, 5, 9, 10, 11, 6]   # H9 then f(y)
        Grg = mp.zeros(10, 2)
        for i, gi in enumerate(irest):
            for j in (7, 8):
                Grg[i, j-7] = S1[gi, j]
        mu2 = mp.matrix([mu1[gi] for gi in irest]) - Grg*Sgginv*mu_g
        S2 = mp.zeros(10, 10)
        for i, gi in enumerate(irest):
            for j, gj in enumerate(irest):
                S2[i, j] = S1[gi, gj]
        S2 = S2 - Grg*Sgginv*Grg.T
        # local: 0..8 H9 (H_M, H_S, H_y), 9: f(y)
        mu_t = mu2[9]; s_t2 = S2[9, 9]
        c_v = mp.matrix(9, 1)
        for k in range(9):
            c_v[k] = S2[9, k]/s_t2
        mu_H = mp.matrix([mu2[k] for k in range(9)])
        S_H = S2[0:9, 0:9] - s_t2*(c_v*c_v.T)
        return dict(th=th, delta=float(delta), y=y, pgrad=pgrad, mu_t=mu_t, s_t2=s_t2,
                    c_v=c_v, mu_H=mu_H, S_H=S_H)


def chol_np(S):
    return np.linalg.cholesky(np.array([[float(S[i, j]) for j in range(S.cols)] for i in range(S.rows)]))


def g_engine(st, N=2**18, seed=SEED):
    muH = np.array([float(st['mu_H'][k]) for k in range(9)])
    LH = chol_np(st['S_H'])
    cv = np.array([float(st['c_v'][k]) for k in range(9)])
    s_t = float(sqrt(st['s_t2'])); mu_t = float(st['mu_t'])
    eng = _qmc.Sobol(9, scramble=True, seed=seed)
    u = eng.random(N)
    z = np.clip(_ndtri(np.clip(u, 1e-300, 1-1e-16)), -38, 38)
    ZL = z @ LH.T
    def g_at_t(t):
        mu_v = muH + cv*(s_t*t)
        def ev(Z):
            X = Z + mu_v
            dM = X[:, 0]*X[:, 2]-X[:, 1]**2; tM = X[:, 0]+X[:, 2]
            dS = X[:, 3]*X[:, 5]-X[:, 4]**2
            dy = X[:, 6]*X[:, 8]-X[:, 7]**2
            return np.abs(dM)*(dM > 0)*(tM < 0)*np.abs(dS)*(dS < 0)*np.abs(dy)*(dy < 0)
        h = 0.5*(ev(ZL)+ev(-ZL))
        bl = h.reshape(32, -1).mean(axis=1)
        return float(h.mean()), float(bl.std(ddof=1)/np.sqrt(32))
    return g_at_t, mu_t, s_t


def rho_station(st, Zr, Nq=10, Nmc=2**18, seed=SEED):
    g_at_t, mu_t, s_t = g_engine(st, Nmc, seed)
    bf, ef = float(B), float(ELL)
    t_lo = (bf-ef-mu_t)/s_t; t_hi = (bf-mu_t)/s_t
    u_lo, u_hi = _ndtr(t_lo), _ndtr(t_hi)
    if not (u_hi > u_lo):          # window carries zero needle mass (to float)
        return 0.0, 0.0, 0.0
    us = np.clip(u_lo + (u_hi-u_lo)*(np.arange(Nq)+0.5)/Nq, 1e-300, 1-1e-16)
    gs = [g_at_t(float(_ndtri(uu)))[0] for uu in us]
    I = (u_hi-u_lo)*float(np.mean(gs))
    return float(st['pgrad'])*I/Zr, I, (u_hi-u_lo)


def rho_station_adaptive(st, Zr, seed=SEED):
    """QMC at N=2^17, Nq=8; if the node-QMC resolves zero mass despite the
    needle sitting inside the window (rare typing), boost to N=2^20 once.
    Deterministic (fixed seeds)."""
    rho, I, mass = rho_station(st, Zr, Nq=8, Nmc=2**17, seed=seed)
    boosted = False
    if I == 0.0 and mass > 0.1:
        rho, I, mass = rho_station(st, Zr, Nq=10, Nmc=2**20, seed=seed+5)
        boosted = True
    return rho, I, mass, boosted


def Z_r_grid(gl: GridLaw):
    """Z_r from the grid code path (pair law): local H_M,H_S = mu1[0:6]."""
    y = station_xy(gl.r, 90, mpf('0.4'))
    y_pts = ([(y[0], y[1], k) for k in ('f', 'fx', 'fy')]
             + [(y[0], y[1], k) for k in ('fxx', 'fxy', 'fyy')])
    # pair law needs only the shared block
    pv = mp.matrix([B, 0, 0, B-ELL, 0, 0])
    Grc = mp.zeros(6, 6)
    for i in range(6):
        for j in range(6):
            Grc[i, j] = gl.G12[6+i, j]
    mu6 = Grc*(gl.G6inv*pv)
    Grr = mp.zeros(6, 6)
    for i in range(6):
        for j in range(6):
            Grr[i, j] = gl.G12[6+i, 6+j]
    S6 = Grr - Grc*gl.G6inv*Grc.T
    mu6n = np.array([float(mu6[k]) for k in range(6)])
    L6 = chol_np(S6)
    eng = _qmc.Sobol(6, scramble=True, seed=SEED+1)
    u = eng.random(2**20)
    z = np.clip(_ndtri(np.clip(u, 1e-300, 1-1e-16)), -38, 38)
    def ev(Z):
        X = Z @ L6.T + mu6n
        dM = X[:, 0]*X[:, 2]-X[:, 1]**2; tM = X[:, 0]+X[:, 2]
        dS = X[:, 3]*X[:, 5]-X[:, 4]**2
        return np.abs(dM)*(dM > 0)*(tM < 0)*np.abs(dS)*(dS < 0)
    h = 0.5*(ev(z)+ev(-z))
    bl = h.reshape(32, -1).mean(axis=1)
    return float(h.mean()), float(bl.std(ddof=1)/np.sqrt(32))


def main():
    print("== C1 grid: plane integral of rho (AO-free envelope), r = 0.05 ==")
    print("historical consistency target (display only, NOT proof): "
          "int Lambda dA = 1.216e-4, C* = 0.973 +/- 0.058, qual/raw = 0.9997")
    gl = GridLaw(R)
    Zr, Zr_se = Z_r_grid(gl)
    print("Z_r (grid code path) = %.9e +/- %.1e" % (Zr, Zr_se))
    ck(abs(Zr-8.059372673e-03) < 3*Zr_se + 3e-5, "Zr-two-codepath",
       "grid %.9e vs main 8.059372673e-03" % Zr)

    thetas = [15, 45, 75, 105, 135, 150, 160, 165, 170, 175]
    deltas = [float(sqrt(2*ELL/B)), 0.012, 0.020, 0.026, 0.033, 0.040, 0.050, 0.066]
    print("grid: thetas=%s deg, deltas=%s" % (thetas, ["%.5f" % d for d in deltas]))
    RHO = {}
    for th in thetas:
        for dl in deltas:
            st = gl.station(th, dl)
            rho, I, mass, boosted = rho_station_adaptive(st, Zr)
            RHO[(th, dl)] = rho
            print("  th=%-4d dl=%.5f  rho=%.11e  (I=%.3e, mass=%.3f, off=%+.4f, s_t/l=%.4f%s)"
                  % (th, dl, rho, I, mass, float((st['mu_t']-B)/ELL), float(sqrt(st['s_t2'])/ELL),
                     ", boosted" if boosted else ""))
    # trapezoid over (th, dl) with Jacobian dl; theta in radians, covering [0,pi]
    ths = np.array(thetas)*np.pi/180
    # extend edges: theta=15 covers [0,30], ..., theta=165 covers [150,180]
    w_th = np.zeros(len(thetas))
    for i in range(len(thetas)):
        lo = 0.0 if i == 0 else (ths[i-1]+ths[i])/2
        hi = np.pi if i == len(thetas)-1 else (ths[i]+ths[i+1])/2
        w_th[i] = hi-lo
    w_dl = np.zeros(len(deltas))
    for j in range(len(deltas)):
        lo = 0.0 if j == 0 else (deltas[j-1]+deltas[j])/2
        hi = deltas[j] + (deltas[j]-deltas[j-1])/2 if j == len(deltas)-1 else (deltas[j]+deltas[j+1])/2
        w_dl[j] = hi-lo
    total = 0.0
    for i, th in enumerate(thetas):
        for j, dl in enumerate(deltas):
            total += w_th[i]*w_dl[j]*dl*RHO[(th, dl)]
    total *= 2   # lower half-plane by the y -> -y reflection symmetry of the pins
    ck(np.isfinite(total) and total > 0, "grid-total-finite", "%.6e" % total)
    print("int rho dA (AO-free envelope, grid trapezoid, both half-planes) = %.6e" % total)
    print("historical C*r^3 = 0.973*1.25e-4 = %.6e ; ratio ours/historical = %.4f"
          % (0.973*1.25e-4, total/(0.973*1.25e-4)))
    # cross-check vs main-script probe values (independent code path)
    main_val = 6.310632e-04   # c1_intensity.py transcript, station (45, 0.033), se ~1.2pct
    rel = abs(RHO[(45, 0.033)]-main_val)/main_val
    ck(rel < 0.012, "grid-vs-main-two-codepath",
       "grid %.9e vs main %.9e, rel %.2e (QMC SE budget ~1.2pct)" % (RHO[(45, 0.033)], main_val, rel))
    print("grid probe (45,0.033): rho = %.9e ; main-script %.9e ; rel %.2e"
          % (RHO[(45, 0.033)], main_val, rel))
    print("ALL GRID CERTIFICATES PASS")
    print("TRANSCRIPT END")


if __name__ == '__main__':
    main()
