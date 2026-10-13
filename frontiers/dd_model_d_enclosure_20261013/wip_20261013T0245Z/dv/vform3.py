"""Exploration (numpy, outside the repository): midpoint cubature of D in (u = ln tau, g, v) with the closed-form
t-integral, vectorized; convergence with the grid, to size a rigorous version.
F(tau, g, v) := sum_sg int_{1-v^2/3}^inf dt e^{-t^2/(576 tau^2)} P_sg(t,v) e^{-(lam t + mu)^2/(2 s^2)} / (s sqrt(2 pi)).
D = A3 int dtau int dg int dv tau^{-11/3} g^{8/3} e^{-12 tau^2 g^4 - g^2/4} F.
"""
import math, sys, time
import numpy as np
from scipy import special

A3 = 1/(57600*math.pi)
SQ6 = math.sqrt(6)
SQPI = math.sqrt(math.pi)

def P_coeffs(v, sg, branch):
    """Coefficients c[0..4] (arrays over v) of P_sg(t, v) in powers of t."""
    v = np.asarray(v, float)
    # PhiT in t
    if branch == 'A':
        ph = [v**6/3 - v**4 + 4/3, v**4 - 4.0, 4.0*np.ones_like(v), -4/3*np.ones_like(v)]
    else:
        ph = [v**6/3 - v**4, v**4, np.zeros_like(v), np.zeros_like(v)]
    chi0 = sg*(4*v**3 - 12*v) - 8.0
    chi1 = 12*sg*v + 12.0
    # Iquad = 20/3 - 20 t + (8/9) chi + (52/3) t^2 - (4/3) t chi + (13/486) chi^2
    iq = [20/3 + (8/9)*chi0 + (13/486)*chi0**2,
          -20.0 + (8/9)*chi1 - (4/3)*chi0 + (13/486)*2*chi0*chi1,
          52/3 - (4/3)*chi1 + (13/486)*chi1**2,
          np.zeros_like(v)]
    d = [ph[i] - iq[i] for i in range(4)]
    # times 12 (v^2 - 1) + 12 t
    r0 = 12*(v*v - 1); r1 = 12.0
    c = [d[0]*r0, d[1]*r0 + d[0]*r1, d[2]*r0 + d[1]*r1, d[3]*r0 + d[2]*r1, d[3]*r1]
    return c

def gauss_moments(alpha, u1, u2, nmax):
    """arrays: I_n = int_{u1}^{u2} u^n e^{-alpha u^2} du, u2 may be +inf (array with inf)."""
    sa = np.sqrt(alpha)
    e1 = np.exp(-alpha*u1*u1)
    fin = np.isfinite(u2)
    u2f = np.where(fin, u2, 0.0)
    e2 = np.where(fin, np.exp(-alpha*u2f*u2f), 0.0)
    # I0 = sqrt(pi)/(2 sa) * (erf(sa u2) - erf(sa u1)); use erfc for stability when both large
    I0 = (SQPI/(2*sa))*np.where(fin, special.erf(sa*u2f) - special.erf(sa*u1), special.erfc(sa*u1))
    I = [I0]
    if nmax >= 1:
        I.append((e1 - e2)/(2*alpha))
    for n in range(2, nmax+1):
        b1 = u1**(n-1)*e1; b2 = np.where(fin, u2f**(n-1)*e2, 0.0)
        I.append(((n-1)/(2*alpha))*I[n-2] - (b2 - b1)/(2*alpha))
    return I

def F(tau, g, v):
    """F(tau, g, v) on broadcast arrays g, v (tau scalar)."""
    g = np.asarray(g, float); v = np.asarray(v, float)
    g, v = np.broadcast_arrays(g, v)
    s = 576*SQ6*tau*tau*g
    a = 1/(576*tau*tau)
    out = np.zeros_like(v)
    for sg in (1, -1):
        lam = 12*(1 + sg*v); mu = sg*(4*v**3 - 12*v) - 8.0
        alpha = a + lam*lam/(2*s*s)
        beta = lam*mu/(s*s)
        const = mu*mu/(2*s*s)
        tc = -beta/(2*alpha)
        logpre = alpha*tc*tc - const
        pre = np.exp(np.maximum(logpre, -700.0))/(s*math.sqrt(2*math.pi))
        t1 = 1 - v*v/3
        for (lo, hi, branch) in ((t1, np.ones_like(v), 'A'), (np.ones_like(v), np.full_like(v, np.inf), 'B')):
            c = P_coeffs(v, sg, branch)
            # shift: q_j = sum_i c_i C(i,j) tc^(i-j)
            q = [np.zeros_like(v) for _ in range(5)]
            for i in range(5):
                for j in range(i+1):
                    q[j] = q[j] + c[i]*math.comb(i, j)*tc**(i-j)
            u1 = lo - tc; u2 = hi - tc
            mom = gauss_moments(alpha, u1, u2, 4)
            tot = sum(q[j]*mom[j] for j in range(5))
            tot = np.where(hi > lo, tot, 0.0)
            out = out + pre*tot
    return out

def weight(tau, g):
    return tau**(-11/3)*g**(8/3)*np.exp(-12*tau*tau*g**4 - g*g/4)

def midpoint_D(Nu, Ng, Nv, u_lo=math.log(1e-3), u_hi=math.log(30.0), g_hi=9.0, v_lo=0.0, v_hi=6.0, adapt=True):
    """Midpoint rule in u = ln tau (uniform), g (uniform), v (per-slab grid concentrated near v* = 2 when adapt)."""
    us = u_lo + (np.arange(Nu) + 0.5)*(u_hi - u_lo)/Nu; du = (u_hi - u_lo)/Nu
    gs = (np.arange(Ng) + 0.5)*g_hi/Ng; dg = g_hi/Ng
    total = 0.0
    for u in us:
        tau = math.exp(u)
        if adapt:
            # v-grid: dense near 2 with width w ~ max(3e-3, 60 tau), plus coarse elsewhere
            w = min(2.0, max(0.02, 150*tau))
            dense = np.linspace(2 - w, 2 + w, Nv + 1)
            coarse_lo = np.linspace(v_lo, 2 - w, max(2, Nv//3) + 1)[:-1]
            coarse_hi = np.linspace(2 + w, v_hi, max(2, Nv//3) + 1)[1:]
            edges = np.concatenate([coarse_lo, dense, coarse_hi])
        else:
            edges = np.linspace(v_lo, v_hi, Nv + 1)
        vm = 0.5*(edges[1:] + edges[:-1]); dv = np.diff(edges)
        G, V = np.meshgrid(gs, vm, indexing='ij')
        vals = F(tau, G, V)*weight(tau, G)*dv[None, :]
        total += vals.sum()*dg*du*tau     # dtau = tau du
    return A3*total

if __name__ == '__main__':
    t0 = time.time()
    for (Nu, Ng, Nv) in ((20, 12, 20), (40, 24, 40), (80, 48, 80), (160, 96, 160)):
        D = midpoint_D(Nu, Ng, Nv)
        print('Nu=%d Ng=%d Nv=%d: D = %.8f  [%.0fs]' % (Nu, Ng, Nv, D, time.time()-t0)); sys.stdout.flush()
