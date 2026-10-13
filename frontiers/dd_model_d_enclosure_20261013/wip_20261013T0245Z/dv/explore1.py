"""Exploration (numpy): the curvature term of note DC's Remark 1 identity, split by the sign of c' = 1 - t.
A(k) = E[f(1-t, 8-12t+sV)], f = d^2Phi/dR^2 (Lemma B.2(b)), t = 12kB/gamma^2, s = 576 sqrt6 k^2/|gamma|^3,
(gamma, B) ~ N(0,2) x N(0,2), V ~ density 2 theta(|v|), theta(a) = phi(a) - a Q(a).
D = T1 + T3 - (1990656/4800) int k^{4/3} e^{-12k^2} (13/243 - A(k)) dk, T1 = 0.043570680, T3 = 0.155690564 (referee)."""
import sys, math
import numpy as np
from scipy import integrate, special
sys.path.insert(0, '/tmp/claude-0/-home-claude/b41b316f-232c-5cf7-a0ee-80f0de603a6f/scratchpad/dcert/referee/sliceA')
from phi_impl import d2R_formula

def theta(a):
    a = np.asarray(a, float)
    return np.exp(-a*a/2)/math.sqrt(2*math.pi) - a*0.5*special.erfc(a/math.sqrt(2))

# Gauss-Hermite style nodes for gamma (density p(g)=e^{-g^2/4}/sqrt(4pi), even -> 2*int_0^inf) and B (same law)
def gauss_nodes(n, lo, hi):
    x, w = np.polynomial.legendre.leggauss(n)
    return (hi-lo)/2*x + (hi+lo)/2, (hi-lo)/2*w

def A_split(k, ng=400, nb=400, nv=400):
    # gamma > 0 on (0, 12], B on [-12, 12], v on [-10, 10]
    G, WG = gauss_nodes(ng, 1e-6, 12.0)
    Bn, WB = gauss_nodes(nb, -12.0, 12.0)
    Vn, WV = gauss_nodes(nv, -10.0, 10.0)
    pg = 2*np.exp(-G*G/4)/math.sqrt(4*math.pi)
    pb = np.exp(-Bn*Bn/4)/math.sqrt(4*math.pi)
    pv = 2*theta(np.abs(Vn))
    pos = neg = 0.0; Ppos = 0.0
    for g, wg in zip(G, WG):
        t = 12*k*Bn/(g*g)                       # shape (nb,)
        s = 576*math.sqrt(6)*k*k/g**3
        cp = (1 - t)[:, None]
        R = (8 - 12*t)[:, None] + s*Vn[None, :]
        f = d2R_formula(np.broadcast_to(cp, R.shape), R)
        inner = (f*pv[None, :]*WV[None, :]).sum(axis=1)   # E_V f for each B
        wb = pb*WB
        m = t < 1
        pos += wg*pg[list(G).index(g)] * (inner[m]*wb[m]).sum() if False else wg*(2*math.exp(-g*g/4)/math.sqrt(4*math.pi))*(inner[m]*wb[m]).sum()
        neg += wg*(2*math.exp(-g*g/4)/math.sqrt(4*math.pi))*(inner[~m]*wb[~m]).sum()
        Ppos += wg*(2*math.exp(-g*g/4)/math.sqrt(4*math.pi))*(wb[m]).sum()
    return pos, neg, Ppos

if __name__ == '__main__':
    for k in (0.05, 0.1, 0.2, 0.3, 0.45, 0.6, 0.8, 1.0):
        pos, neg, P = A_split(k)
        print('k=%.2f  A=%.7f  (t<1: %.7f, t>1: %.7f)  P(t<1)=%.5f  13/243-A=%.7f  weight k^{4/3}e^{-12k^2}=%.5f' % (
            k, pos+neg, pos, neg, P, 13/243-(pos+neg), k**(4/3)*math.exp(-12*k*k)), flush=True)
