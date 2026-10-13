"""Exploration (numpy, vectorized): the curvature term C by the (t, sigma)-kernel route.
C = (1990656/4800) int dt int dsigma K(t, sigma) G(t, 576 sqrt6 sigma),
K(t, sigma) = sigma^{14/3}/(24 pi) int_0^inf u^9 exp(-(t^2/576)u^2 - (sigma^2/4)u^4 - 12 sigma^4 u^6) du,
G(t, s) = 13/243 - E_V f(1-t, 8-12t+sV),  V ~ 2 theta(|v|)."""
import sys, math, time
import numpy as np
from scipy import special
sys.path.insert(0, '/tmp/claude-0/-home-claude/b41b316f-232c-5cf7-a0ee-80f0de603a6f/scratchpad/dcert/referee/sliceA')
from phi_impl import d2R_formula

def theta(a):
    a = np.asarray(a, float)
    return np.exp(-a*a/2)/math.sqrt(2*math.pi) - a*0.5*special.erfc(a/math.sqrt(2))

def gl(n, lo, hi):
    x, w = np.polynomial.legendre.leggauss(n)
    return (hi-lo)/2*x + (hi+lo)/2, (hi-lo)/2*w

_v1, _w1 = gl(400, -12.0, 0.0); _v2, _w2 = gl(400, 0.0, 12.0)
VN, VW = np.concatenate([_v1, _v2]), np.concatenate([_w1, _w2])
PV = 2*theta(np.abs(VN))*VW
# u-grid for K: the integrand u^9 exp(-a u^2 - b u^4 - c u^6) lives on u in (0, few); use log-spaced-ish fixed GL on [0, 40] split
_u1, _uw1 = gl(500, 0.0, 1.5); _u2, _uw2 = gl(500, 1.5, 3.0); _u3, _uw3 = gl(300, 3.0, 6.0)
UN, UW = np.concatenate([_u1, _u2, _u3]), np.concatenate([_uw1, _uw2, _uw3])   # w-grid after u = w / sqrt(sigma)

def K_row(t, sig):
    """K(t, sigma) for an array of sigma at fixed t."""
    # K = sigma^{-1/3}/(24 pi) int w^9 exp(-(t^2/(576 sigma)) w^2 - w^4/4 - 12 sigma w^6) dw
    E = -(t*t/(576*sig[:, None]))*UN[None, :]**2 - UN[None, :]**4/4 - 12*sig[:, None]*UN[None, :]**6
    return sig**(-1/3)/(24*math.pi)*((UN**9)[None, :]*np.exp(E)*UW[None, :]).sum(axis=1)

def G_row(t, sig):
    s = 576*math.sqrt(6)*sig
    cp = 1 - t
    R = (8 - 12*t) + s[:, None]*VN[None, :]
    f = d2R_formula(np.full_like(R, cp), R)
    return 13/243 - (f*PV[None, :]).sum(axis=1)

if __name__ == '__main__':
    t0 = time.time()
    nt, ns = int(sys.argv[1]), int(sys.argv[2])
    tn, tw = gl(nt, -6.0, 8.0)
    yn, yw = gl(ns, -18.0, 45.0)
    sn, sw = np.exp(yn), np.exp(yn)*yw      # sigma = e^y
    tot = 0.0; Kmass = 0.0; Gpos = 0.0
    for t, wt in zip(tn, tw):
        Kv = K_row(t, sn); Gv = G_row(t, sn)
        Kmass += wt*(Kv*sw).sum(); tot += wt*(Kv*Gv*sw).sum()
    print('nt=%d ns=%d: int K = %.7f (target int k^{4/3}e^{-12k^2}dk = %.7f); C = %.7f; D = T1+T3-C = %.7f  [%.0fs]' % (
        nt, ns, Kmass, 0.5*12**(-7/6)*special.gamma(7/6), 1990656/4800*tot, 0.043570680+0.155690564-1990656/4800*tot, time.time()-t0))
