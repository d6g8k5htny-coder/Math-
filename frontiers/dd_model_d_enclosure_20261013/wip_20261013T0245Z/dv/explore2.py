"""Exploration (numpy): the curvature term C by the (t, sigma)-kernel route versus the A(k) route.
C = (1990656/4800) int k^{4/3} e^{-12k^2} (13/243 - A(k)) dk
  = (1990656/4800) int dt int dsigma K(t, sigma) G(t, 576 sqrt6 sigma),
K(t, sigma) = sigma^{14/3}/(24 pi) int_0^inf u^9 exp(-(t^2/576)u^2 - (sigma^2/4)u^4 - 12 sigma^4 u^6) du,
G(t, s) = 13/243 - Psi~(t, s),  Psi~(t, s) = E_V f(1-t, 8-12t+sV),  V ~ 2 theta(|v|)."""
import sys, math, time
import numpy as np
from scipy import integrate, special
sys.path.insert(0, '/tmp/claude-0/-home-claude/b41b316f-232c-5cf7-a0ee-80f0de603a6f/scratchpad/dcert/referee/sliceA')
from phi_impl import d2R_formula

def theta(a):
    a = np.asarray(a, float)
    return np.exp(-a*a/2)/math.sqrt(2*math.pi) - a*0.5*special.erfc(a/math.sqrt(2))

def gl(n, lo, hi):
    x, w = np.polynomial.legendre.leggauss(n)
    return (hi-lo)/2*x + (hi+lo)/2, (hi-lo)/2*w

_v1, _w1 = gl(300, -12.0, 0.0); _v2, _w2 = gl(300, 0.0, 12.0)
VN, VW = np.concatenate([_v1, _v2]), np.concatenate([_w1, _w2])
PV = 2*theta(np.abs(VN))*VW          # weights of the V-law (mass 1 - tail)
print('V mass', PV.sum())

def Psi(t, s):
    cp = 1 - t
    R = 8 - 12*t + s*VN
    f = d2R_formula(np.full_like(R, cp), R)
    return (f*PV).sum()

def K(t, sigma, nu=2000):
    # integrand in u: u^9 exp(-a u^2 - b u^4 - c u^6); locate scale and integrate on [0, U]
    a, b, c = t*t/576, sigma*sigma/4, 12*sigma**4
    # crude upper limit: where exponent < -60 beyond the mode
    f = lambda u: u**9*np.exp(-a*u*u - b*u**4 - c*u**6)
    # scale by sigma: typical u ~ (1/(12 sigma^4))^(1/6)
    U = 6.0*(1.0/(12*sigma**4))**(1/6) + 40.0/(1+abs(t))
    un, uw = gl(nu, 0.0, U)
    return sigma**(14/3)/(24*math.pi)*(f(un)*uw).sum()

def A_direct(k, ng=300, nb=300):
    G, WG = gl(ng, 1e-6, 12.0)
    Bn, WB = gl(nb, -12.0, 12.0)
    pg = 2*np.exp(-G*G/4)/math.sqrt(4*math.pi)*WG
    pb = np.exp(-Bn*Bn/4)/math.sqrt(4*math.pi)*WB
    acc = 0.0
    for g, wg in zip(G, pg):
        t = 12*k*Bn/(g*g); s = 576*math.sqrt(6)*k*k/g**3
        cp = (1 - t)[:, None]
        R = (8 - 12*t)[:, None] + s*VN[None, :]
        f = d2R_formula(np.broadcast_to(cp, R.shape), R)
        acc += wg*((f*PV[None, :]).sum(axis=1)*pb).sum()
    return acc

if __name__ == '__main__':
    t0 = time.time()
    C_A = 0.1225552
    # kernel route
    t0 = time.time()
    tn, tw = gl(240, -6.0, 8.0)
    sn, sw = gl(160, 1e-6, 2.5)
    tot = 0.0; Kmass = 0.0
    for t, wt in zip(tn, tw):
        for sg, ws in zip(sn, sw):
            Kv = K(t, sg, 800)
            Kmass += wt*ws*Kv
            tot += wt*ws*Kv*(13/243 - Psi(t, 576*math.sqrt(6)*sg))
    C_K = 1990656/4800*tot
    print('kernel mass int K = %.7f  (should equal int k^{4/3}e^{-12k^2}dk = %.7f)' % (Kmass, 0.5*12**(-7/6)*special.gamma(7/6)))
    print('C via kernel route = %.7f   [%.0fs]' % (C_K, time.time()-t0))
    T1, T3 = 0.043570680, 0.155690564
    print('D = T1 + T3 - C = %.7f (A route), %.7f (kernel route); reference 0.0767381/0.0767382' % (T1+T3-C_A, T1+T3-C_K))
