"""Exploration (numpy): C by the (z, sigma) route, t = 24 sqrt(sigma) z, s = 576 sqrt6 sigma.
C = c0 int dsigma sigma^{1/6} int dz Kz(z, sigma) G(24 sqrt(sigma) z, 576 sqrt6 sigma),
Kz(z, sigma) = (1/pi) int_0^inf w^9 exp(-z^2 w^2 - w^4/4 - 12 sigma w^6) dw,  c0 = 1990656/4800."""
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
_x1, _xw1 = gl(900, -16.0, 1.9)
WN, WW = np.exp(_x1), np.exp(_x1)*_xw1      # w = e^x, log grid

def Kz_row(zn, sig):
    E = -(zn[:, None]**2)*WN[None, :]**2 - WN[None, :]**4/4 - 12*sig*WN[None, :]**6
    return ((WN**9)[None, :]*np.exp(E)*WW[None, :]).sum(axis=1)/math.pi

def G_row(tn, s):
    cp = 1 - tn
    R = (8 - 12*tn)[:, None] + s*VN[None, :]
    f = d2R_formula(np.broadcast_to(cp[:, None], R.shape), R)
    return 13/243 - (f*PV[None, :]).sum(axis=1)

if __name__ == '__main__':
    t0 = time.time()
    nz, ns = int(sys.argv[1]), int(sys.argv[2])
    yn, yw = gl(ns, -20.0, 40.0)
    sn, sw = np.exp(yn), np.exp(yn)*yw
    tot = 0.0; mass = 0.0
    for sg, ws in zip(sn, sw):
        Z = 9.0*max(1.0, 1.5*(8*sg)**(1/6))
        zn, zw = gl(nz, -Z, Z)
        Kv = Kz_row(zn, sg)
        Gv = G_row(24*math.sqrt(sg)*zn, 576*math.sqrt(6)*sg)
        mass += ws*sg**(1/6)*(Kv*zw).sum()
        tot += ws*sg**(1/6)*(Kv*Gv*zw).sum()
    c0 = 1990656/4800
    print('nz=%d ns=%d: mass = %.7f (target %.7f); C = %.7f; D = T1+T3-C = %.7f  [%.0fs]' % (
        nz, ns, mass, 0.5*12**(-7/6)*special.gamma(7/6), c0*tot, 0.043570680+0.155690564-c0*tot, time.time()-t0))
