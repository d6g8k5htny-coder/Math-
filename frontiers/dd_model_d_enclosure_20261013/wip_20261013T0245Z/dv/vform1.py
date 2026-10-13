"""Exploration (numpy/scipy, outside the repository): the v-parametrization of Phi (see vform2.py for the formulas)."""
import math, sys, time
import numpy as np
from scipy import integrate, special

def y_root(cp, R):
    sig = abs(R)/8.0
    if cp > 0 and sig*sig <= cp**3:
        return 2*cp*math.cos((2/3)*math.acos(min(1.0, sig*cp**-1.5)))
    A = sig + math.sqrt(max(sig*sig - cp**3, 0.0))
    if A == 0: return 0.0
    A23 = A**(2/3)
    return A23 + cp*cp/A23

def Phi_R(cp, R):
    y = y_root(cp, R); psi = cp + y; d = psi - abs(cp)
    return abs(cp)*d*d + d**3/3

def Phi_v(cp, v):
    if cp > 0: return v**6/3 - cp*v**4 + (4/3)*cp**3
    return -cp*v**4 + v**6/3

def R_of_v(cp, v): return 4*v**3 - 12*cp*v
def Rp_of_v(cp, v): return 12*(v*v - cp)

def Iquad(t, chi): return 20/3 - 20*t + (8/9)*chi + (52/3)*t*t - (4/3)*t*chi + (13/486)*chi*chi

def E_direct(cp, r, s, t):
    f = lambda R: (Phi_R(cp, R) - Iquad(t, R - r))*math.exp(-(R-r)**2/(2*s*s))/(s*math.sqrt(2*math.pi))
    pts = sorted(set([0.0, r]))
    val, err = integrate.quad(f, r - 12*s, r + 12*s, points=[p for p in pts if r-12*s < p < r+12*s], limit=400)
    return val

def E_vform(cp, r, s, t):
    v0 = math.sqrt(3*cp) if cp > 0 else 0.0
    def g(v):
        R = R_of_v(cp, v); Rp = Rp_of_v(cp, v); P = Phi_v(cp, v)
        out = 0.0
        for sg in (1, -1):
            Rs = sg*R
            out += (P - Iquad(t, Rs - r))*math.exp(-(Rs-r)**2/(2*s*s))/(s*math.sqrt(2*math.pi))*Rp
        return out
    Rmax = abs(r) + 12*s
    vmax = max(v0 + 1.0, (Rmax/4)**(1/3) + math.sqrt(3*abs(cp)) + 1)
    pts = []
    if abs(r) > 0:
        roots = np.roots([4.0, 0.0, -12*cp, -abs(r)])
        for z in roots:
            if abs(z.imag) < 1e-9 and z.real >= v0:
                vs = z.real; Rp = max(Rp_of_v(cp, vs), 1e-12)
                for kk in (-6, -3, -1, 0, 1, 3, 6):
                    p = vs + kk*s/Rp
                    if v0 < p < vmax: pts.append(p)
    val, err = integrate.quad(g, v0, vmax, points=sorted(set(pts)) or None, limit=400)
    return val

if __name__ == '__main__':
    worst = 0.0
    for cp in (2.0, 1.0, 0.3, 0.01, 0.0, -0.01, -0.5, -2.0):
        v0 = math.sqrt(3*cp) if cp > 0 else 0.0
        for v in v0 + np.array([0.0, 1e-6, 1e-3, 0.1, 0.5, 1.0, 3.0, 10.0]):
            R = R_of_v(cp, v)
            a, b = Phi_R(cp, R), Phi_v(cp, v)
            worst = max(worst, abs(a-b)/(1+abs(b)))
    print('check1 worst relative discrepancy', worst)
    for (t, s) in ((0.1, 0.5), (0.5, 2.0), (0.9, 0.1), (1.0, 1.0), (1.3, 3.0), (-0.4, 0.05), (2.5, 20.0), (0.05, 0.01)):
        cp = 1 - t; r = 8 - 12*t
        a = E_direct(cp, r, s, t); b = E_vform(cp, r, s, t)
        print('  t=%5.2f s=%6.3f  direct %.12g  vform %.12g  diff %.2e' % (t, s, a, b, a-b))
