#!/usr/bin/env python3
# hunt_rim.py — STAGE-E hunt: interior points of the H5-RIM flat envelope.
# H5-RIM (named lemma, H5_CLOSURE.md §1): rho_w(y) <= C_flat(col) for
# delta_M <= 0.00895, C_flat = 2x certified probe-box rho_hi (probes at
# delta in [0.004, 0.008]).  The interior delta < 0.004 is covered ONLY by
# the flatness hypothesis.  This program point-evaluates rho_w at interior
# depths with the campaign's own exact-law grid engine (c1_grid.py, dps=80,
# deterministic QMC) and compares against the merged C_flat constants.
# Hunt-grade (QMC evidence); any exceedance is then certified separately.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
C1DIR = os.path.join(os.path.dirname(HERE), "C1_alpha_intensity")
sys.path.insert(0, C1DIR)

from mpmath import mp, mpf
mp.dps = 80
import numpy as np
import c1_grid as CG


def chol_robust(S):
    A = np.array([[float(S[i, j]) for j in range(S.cols)] for i in range(S.rows)])
    try:
        return np.linalg.cholesky(A)
    except np.linalg.LinAlgError:
        w, Vq = np.linalg.eigh(0.5 * (A + A.T))
        floor = max(w.max(), 1.0) * 1e-13
        wc = np.clip(w, floor, None)
        return Vq @ np.diag(np.sqrt(wc))


CG.chol_np = chol_robust

# merged rim constants (last-wins across h5_results_*.jsonl; verified)
RHO_HI = {15: '0.00060348387741551686', 45: '2.59435032960078375662',
          75: '0.03528240856247915931', 105: '0.03624768324222395018',
          135: '0.62900067915038803690', 150: '1.32125917691204831142',
          160: '0.02949289930718605979', 165: '0.00119344716565773927',
          170: '0.00000001327705651495', 175: '1.72865592536977723981'}
CFLAT = {t: 2 * mpf(v) for t, v in RHO_HI.items()}


def col_of(th):
    return min(range(0, 180, 15), key=lambda c: abs(c - th) if abs(c - th) <= 90 else 180 - abs(c - th)) or 15


def main():
    gl = CG.GridLaw(CG.R)
    Zr, zse = CG.Z_r_grid(gl)
    print("Z_r(0.05) = %.10e (se %.1e)" % (Zr, zse))
    print("hunt: interior rim depths, columns 135..175 (envelope-tight side)")
    worst = []
    for th in [135, 150, 160, 165, 170, 175]:
        cf = CFLAT[min(CFLAT, key=lambda c: abs(c - th))]
        for dl in ['0.0035', '0.003', '0.0025', '0.002', '0.0015', '0.001', '0.0005']:
            st = gl.station(mpf(th), mpf(dl))
            rho, I, mass, boosted = CG.rho_station_adaptive(st, Zr)
            ratio = mpf(rho) / cf if cf > 0 else mpf('inf')
            flag = "  <<< EXCEEDS C_flat" if ratio > 1 else ""
            worst.append((float(ratio), th, dl, rho))
            print("th=%3d dl=%7s rho=%12.5e  C_flat=%9.3e  ratio=%9.3e mass=%8.2e%s"
                  % (th, dl, rho, float(cf), float(ratio), mass, flag))
    worst.sort(reverse=True)
    print("worst ratio:", worst[0])


main()
