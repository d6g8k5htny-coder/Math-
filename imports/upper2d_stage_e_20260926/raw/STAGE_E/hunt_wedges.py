#!/usr/bin/env python3
# hunt_wedges.py — STAGE-E hunt part 2: interior points of the H5-AXIS
# v1/v2 wedge/S-disk flat envelopes (named lemmas, H5_CLOSURE.md §1).
# Envelopes (merged constants, last-wins ledger):
#   scone_C = 2*max scone probes; mfwd_C, mbwd_C likewise; sdisk_C =
#   2*max(sdisk+sring+scone probes).
# Interiors are machine-uncoverable (det S_gg ~ 1e-15 by collinearity);
# only the flatness hypothesis covers them.  Hunt-grade point evaluations
# with the exact-law engine (dps=80 station algebra + deterministic QMC).
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
C1DIR = os.path.join(ROOT, "C1_alpha_intensity")
H5DIR = os.path.join(ROOT, "H5_closure")
sys.path.insert(0, C1DIR)

from mpmath import mp, mpf, pi, cos, sin, sqrt
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
        return Vq @ np.diag(np.sqrt(np.clip(w, floor, None)))


CG.chol_np = chol_robust


def merged_constants():
    probe_sites = {}
    for fn in sorted(glob.glob(os.path.join(H5DIR, "h5_results_*.jsonl"))):
        for line in open(fn):
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            p = d.get('part')
            if p == 'sconeprobe':
                probe_sites[('scone', d['thS'], d['dS'])] = mpf(d['rho_hi'])
            elif p == 'sdiskprobe':
                probe_sites[('sdisk', d['thS'])] = mpf(d['rho_hi'])
            elif p == 'sringprobe':
                probe_sites[('sring', d['thS'], d['dS'])] = mpf(d['rho_hi'])
            elif p == 'mbackprobe':
                key = 'mfwd' if int(d['thM']) < 90 else 'mbwd'
                probe_sites[(key, d['thM'], d['dl'])] = mpf(d['rho_hi'])
    srim = {}
    for k3, v in probe_sites.items():
        srim[k3[0]] = max(srim.get(k3[0], mpf(0)), v)
    scone_C = 2 * srim['scone']
    mfwd_C = 2 * srim['mfwd']
    mbwd_C = 2 * srim['mbwd']
    sdisk_C = 2 * max([v for k3, v in probe_sites.items()
                       if k3[0] in ('sdisk', 'sring', 'scone')])
    return scone_C, mfwd_C, mbwd_C, sdisk_C


def station_at(gl, yx, yy):
    y = (mpf(yx), mpf(yy))
    y_pts = ([(y[0], y[1], k) for k in ('f', 'fx', 'fy')]
             + [(y[0], y[1], k) for k in ('fxx', 'fxy', 'fyy')])
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
    return gl._condition(G, 0, mpf(0), y)


def main():
    scone_C, mfwd_C, mbwd_C, sdisk_C = merged_constants()
    print("envelope constants: scone_C=%.6e mfwd_C=%.6e mbwd_C=%.6e sdisk_C=%.6e"
          % (scone_C, mfwd_C, mbwd_C, sdisk_C))
    gl = CG.GridLaw(CG.R)
    Zr, zse = CG.Z_r_grid(gl)
    r = CG.R
    print("Z_r = %.10e" % Zr)

    hunts = []
    # M-forward wedge interior: th_M in [0,12), d_M < 0.10 ; constant mfwd_C
    for thM in [0, 2, 4, 6, 8, 10]:
        for dM in ['0.006', '0.012', '0.02', '0.03', '0.05', '0.075', '0.095']:
            hunts.append(("M-fwd", mfwd_C, -r/2 + mpf(dM)*cos(mpf(thM)*pi/180),
                          mpf(dM)*sin(mpf(thM)*pi/180), thM, dM))
    # M-backward wedge interior: th_M in (168,180], d_M < 0.10 ; mbwd_C
    for thM in [170, 172, 174, 176, 178, 180]:
        for dM in ['0.006', '0.012', '0.02', '0.03', '0.05', '0.075', '0.095']:
            hunts.append(("M-bwd", mbwd_C, -r/2 + mpf(dM)*cos(mpf(thM)*pi/180),
                          mpf(dM)*sin(mpf(thM)*pi/180), thM, dM))
    # S-cone interior: th_S in [0,12) measured from M-ward axis (toward M),
    # d_S < 0.105 ; scone_C.  theta_S=0 means toward M (negative x).
    for thS in [0, 2, 4, 6, 8, 10]:
        for dS in ['0.01', '0.02', '0.03', '0.05', '0.075', '0.10']:
            hunts.append(("S-cone", scone_C, r/2 - mpf(dS)*cos(mpf(thS)*pi/180),
                          mpf(dS)*sin(mpf(thS)*pi/180), thS, dS))
    # S-disk interior: d_S < 0.03, off-cone directions ; sdisk_C
    for thS in [30, 45, 60, 90, 120, 150]:
        for dS in ['0.005', '0.01', '0.02', '0.028']:
            hunts.append(("S-disk", sdisk_C, r/2 - mpf(dS)*cos(mpf(thS)*pi/180),
                          mpf(dS)*sin(mpf(thS)*pi/180), thS, dS))

    worst = []
    for name, C, x, y, th, dl in hunts:
        st = station_at(gl, x, y)
        rho, I, mass, boosted = CG.rho_station_adaptive(st, Zr)
        ratio = mpf(rho)/C if C > 0 else mpf('inf')
        flag = "  <<< EXCEEDS" if ratio > 1 else ""
        if ratio > mpf('0.5') or flag:
            print("%6s th=%3d dl=%6s rho=%11.4e C=%9.3e ratio=%9.3e mass=%7.1e%s"
                  % (name, th, dl, rho, float(C), float(ratio), mass, flag))
        worst.append((float(ratio), name, th, dl, rho, float(mass)))
    worst.sort(reverse=True)
    print("TOP 12 ratios:")
    for w in worst[:12]:
        print("  ratio=%9.3e %-6s th=%3d dl=%6s rho=%11.4e mass=%7.1e" % w)


main()
