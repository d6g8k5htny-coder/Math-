"""Midpoint cubature of D in (u = ln tau, g, v) with per-slab adaptive (g, v) ranges; convergence study."""
import math, sys, time
import numpy as np
from vform3 import F, weight, A3, SQ6

def slab_grids(tau, Ng, Nv):
    g_hi = min(9.0, (60/(12*tau*tau))**0.25 + 0.5)          # e^{-12 tau^2 g^4} < e^{-60} beyond
    gs_edges = np.linspace(0.0, g_hi, Ng + 1)
    sd_t = 12*tau*math.sqrt(2)
    s_max = 576*SQ6*tau*tau*g_hi
    R_max = 8 + 12*8*sd_t + 8*s_max
    v_hi = (R_max/4)**(1/3) + 1.0
    if tau < 0.3:
        w = min(2.0, max(0.02, 150*tau))
        dense = np.linspace(2 - w, 2 + w, Nv + 1)
        lo = np.linspace(0.0, 2 - w, max(2, Nv//3) + 1)[:-1]
        hi = np.linspace(2 + w, v_hi, max(2, Nv//3) + 1)[1:]
        v_edges = np.concatenate([lo, dense, hi])
    else:
        v_edges = np.linspace(0.0, v_hi, Nv + 1)
    return gs_edges, v_edges

def midpoint_D(Nu, Ng, Nv, tau_lo=1e-3, tau_hi=1e3):
    u_lo, u_hi = math.log(tau_lo), math.log(tau_hi)
    us = u_lo + (np.arange(Nu) + 0.5)*(u_hi - u_lo)/Nu; du = (u_hi - u_lo)/Nu
    total = 0.0; slabs = []
    for u in us:
        tau = math.exp(u)
        ge, ve = slab_grids(tau, Ng, Nv)
        gm = 0.5*(ge[1:] + ge[:-1]); dg = np.diff(ge)
        vm = 0.5*(ve[1:] + ve[:-1]); dv = np.diff(ve)
        G, V = np.meshgrid(gm, vm, indexing='ij')
        vals = F(tau, G, V)*weight(tau, G)*dv[None, :]*dg[:, None]
        slab = vals.sum()*du*tau*A3
        slabs.append((tau, slab)); total += slab
    return total, slabs

if __name__ == '__main__':
    t0 = time.time()
    for (Nu, Ng, Nv) in ((30, 12, 24), (60, 24, 48), (120, 48, 96), (240, 96, 192)):
        D, slabs = midpoint_D(Nu, Ng, Nv)
        print('Nu=%d Ng=%d Nv=%d: D = %.8f  [%.0fs]' % (Nu, Ng, Nv, D, time.time()-t0)); sys.stdout.flush()
    cum = 0.0
    for tau, slab in slabs:
        cum += slab
        if abs(math.log10(tau) - round(math.log10(tau))) < 0.03 or tau > 300:
            print('  tau=%9.4g slab=%+.3e cum=%.6f' % (tau, slab, cum))
