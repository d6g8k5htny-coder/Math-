"""Prototype (numpy floats) of the RIGOROUS cell scheme for the curvature term C, to size the grids.
The decimal version will compute the same bounds with directed rounding.

C = c0 * int_0^inf dsigma int_R dz sigma^{1/6} Kt(z, sigma) G(24 sqrt(sigma) z, 576 sqrt6 sigma),  c0 = 1990656/4800,
Kt(z, sigma) = (1/pi) int_0^inf w^9 exp(-z^2 w^2 - w^4/4 - 12 sigma w^6) dw,
G(t, s) = 13/243 - int f(1-t, 8-12t+sv) 2 theta(|v|) dv,  f = d^2 Phi / dR^2 = 1/24 + (2x+x^2+2x^3)/72, x = c'/psi_e.

Cell bounds:
  W_cell = int int sigma^{1/6} Kt dz dsigma = (1/(2 sqrt pi)) int_0^inf w^8 e^{-w^4/4} [erf(z1 w) - erf(z0 w)] Gam(w) dw,
           Gam(w) = (12 w^6)^{-7/6} [gamma(7/6, 12 sigma1 w^6) - gamma(7/6, 12 sigma0 w^6)]   (exact in z and sigma),
           the w-integral by product-of-monotone-factor bounds on w-cells (first order in the w-cell size).
  G over the cell: t in [t0,t1], s in [s0,s1]; for each v-cell, R-range and c'-range by corners, x-range by monotonicity,
           f-range, times the exact mass of 2 theta on the v-cell; crude [0, 13/243] when the c'-range contains 0.
"""
import sys, math, time
import numpy as np
from scipy import special

c0 = 1990656/4800
F13 = 13/243

def theta(a):
    return np.exp(-a*a/2)/math.sqrt(2*math.pi) - a*0.5*special.erfc(a/math.sqrt(2))

def theta_mass(a, b):
    """int_a^b 2 theta(|v|) dv for 0 <= a <= b, via the antiderivative of theta on v >= 0:
    int theta(v) dv = (1/2)[(v^2+1)Q(v) ... ] -- use numeric closed form: Theta(v) = -(v phi(v))/2 ... compute by quad-free formula:
    d/dv [ (1+v^2)/2 * Q(v) - v phi(v)/2 ] = v Q - (1+v^2) phi/2 - phi/2 + v^2 phi/2 = vQ - phi = -theta.  So int_a^b theta = H(a)-H(b),
    H(v) = (1+v^2)/2*Q(v) - v*phi(v)/2."""
    H = lambda v: (1+v*v)/2*0.5*special.erfc(v/math.sqrt(2)) - v*np.exp(-v*v/2)/math.sqrt(2*math.pi)/2
    return 2*(H(a) - H(b))

def psi_e(cp, R):
    """psi_e = c' + y, y the largest real root of y^3 - 3c'^2 y + 2c'^3 - R^2/16 = 0."""
    sig = np.abs(R)/8.0
    cp = np.asarray(cp, float); sig = np.broadcast_to(sig, cp.shape) if np.ndim(cp) else sig
    out = np.empty(np.broadcast(cp, sig).shape)
    cp_b = np.broadcast_to(cp, out.shape); sg_b = np.broadcast_to(sig, out.shape)
    trig = (cp_b > 0) & (sg_b**2 <= cp_b**3)
    with np.errstate(all='ignore'):
        c = cp_b[trig]; arg = np.clip(sg_b[trig]*c**-1.5, 0, 1)
        out[trig] = 2*c*np.cos((2/3)*np.arccos(arg))
        o = ~trig; c = cp_b[o]; sg = sg_b[o]
        A = sg + np.sqrt(np.maximum(sg**2 - c**3, 0)); A23 = np.cbrt(A)**2
        out[o] = np.where(A > 0, A23 + c**2/np.where(A23 > 0, A23, 1.0), 0.0)
    return cp_b + out

def f_of_x(x):
    return 1/24 + (2*x + x*x + 2*x**3)/72

def x_val(cp, R):
    return cp/psi_e(cp, R)

def G_bounds(t0, t1, s0, s1, vedges):
    """Rigorous-style bounds of G(t, s) over [t0,t1] x [s0,s1]: returns (Gmin, Gmax)."""
    cp0, cp1 = 1 - t1, 1 - t0              # c' range
    a0, a1 = 8 - 12*t1, 8 - 12*t0          # 8-12t range
    v0, v1 = vedges[:-1], vedges[1:]
    # R = (8-12t) + s v: range over the box by corners (bilinear in s and v)
    corners = [a0 + s0*v0, a0 + s0*v1, a0 + s1*v0, a0 + s1*v1, a1 + s0*v0, a1 + s0*v1, a1 + s1*v0, a1 + s1*v1]
    Rlo = np.minimum.reduce(corners); Rhi = np.maximum.reduce(corners)
    absR_lo = np.where((Rlo <= 0) & (Rhi >= 0), 0.0, np.minimum(np.abs(Rlo), np.abs(Rhi)))
    absR_hi = np.maximum(np.abs(Rlo), np.abs(Rhi))
    mass = theta_mass(np.minimum(np.abs(v0), np.abs(v1)), np.maximum(np.abs(v0), np.abs(v1)))  # cells do not straddle 0
    if cp0 <= 0 <= cp1:
        fmin = np.zeros_like(absR_lo); fmax = np.full_like(absR_lo, F13)
    elif cp0 > 0:
        # x decreasing in |R|, increasing in c': min at (cp0, |R|hi), max at (cp1, |R|lo)
        fmin = f_of_x(x_val(cp0, 8*absR_hi/8)); fmax = f_of_x(x_val(cp1, absR_lo))
    else:
        # c' < 0: x increasing in |R| and in c': min at (cp0, |R|lo), max at (cp1, |R|hi)
        fmin = f_of_x(x_val(cp0, absR_lo)); fmax = f_of_x(x_val(cp1, absR_hi))
    tail = 1.0 - mass.sum()          # mass outside the v-range: f in [0, 13/243]
    Psi_lo = (fmin*mass).sum(); Psi_hi = (fmax*mass).sum() + F13*tail
    return F13 - Psi_hi, F13 - Psi_lo

_x, _w = np.polynomial.legendre.leggauss(400)
def W_exact(z0, z1, sig0, sig1):
    """Accurate W_cell (not a bound) by Gauss-Legendre on [0, 6] in w, for sizing the G-bounds error."""
    wn = 3.0*_x + 3.0; ww = 3.0*_w
    g = wn**8*np.exp(-wn**4/4)
    e = special.erf(z1*wn) - special.erf(z0*wn)
    gam = (12*wn**6)**(-7/6)*(special.gammainc(7/6, 12*sig1*wn**6) - special.gammainc(7/6, 12*sig0*wn**6))*special.gamma(7/6)
    return (ww*g*e*gam).sum()/(2*math.sqrt(math.pi))

def W_cell(z0, z1, sig0, sig1, wedges):
    """Bounds of int int sigma^{1/6} Kt dz dsigma over the cell, by product-of-monotone bounds on w-cells."""
    w0, w1 = wedges[:-1], wedges[1:]
    g = lambda w: w**8*np.exp(-w**4/4)                      # unimodal, mode w = 8^{1/4}
    gm = np.minimum(g(w0), g(w1)); gM = np.maximum(g(w0), g(w1))
    m = 8**0.25
    inside = (w0 < m) & (m < w1); gM = np.where(inside, g(m), gM)
    e = lambda w: special.erf(z1*w) - special.erf(z0*w)      # >= 0 (z1 > z0)
    e0, e1 = e(w0), e(w1)
    em = np.minimum(e0, e1); eM = np.maximum(e0, e1)
    # erf difference in w is unimodal; its max over the cell may be interior: bound by max of ends plus a crude cap
    # (prototype: sample interior; the decimal version will use the derivative sign change bracket)
    wm = (w0 + w1)/2; eM = np.maximum(eM, e(wm))
    gam = lambda w: (12*w**6)**(-7/6)*(special.gammainc(7/6, 12*sig1*w**6) - special.gammainc(7/6, 12*sig0*w**6))*special.gamma(7/6)
    G0, G1 = gam(w0), gam(w1)           # decreasing in w
    Gm, GM = np.minimum(G0, G1), np.maximum(G0, G1)
    lo = ((w1 - w0)*gm*em*Gm).sum()/(2*math.sqrt(math.pi))
    hi = ((w1 - w0)*gM*eM*GM).sum()/(2*math.sqrt(math.pi))
    return lo, hi

if __name__ == '__main__':
    ns, nz, nv, nw = [int(a) for a in sys.argv[1:5]]
    EXACTW = len(sys.argv) > 5 and sys.argv[5] == 'exactW'
    t0 = time.time()
    # sigma cells: geometric from 1e-9 to 1e17 (the tail beyond is bounded separately)
    sedges = np.exp(np.linspace(math.log(1e-9), math.log(1e17), ns + 1))
    vedges = np.concatenate([-np.exp(np.linspace(math.log(12), math.log(1e-4), nv//2 + 1)), [0.0], np.exp(np.linspace(math.log(1e-4), math.log(12), nv//2 + 1))])
    vedges = np.unique(vedges)
    wedges = np.exp(np.linspace(math.log(1e-5), math.log(6.0), nw + 1))
    Clo = Chi = 0.0; Wtot_lo = Wtot_hi = 0.0
    for i in range(ns):
        s0, s1 = sedges[i], sedges[i+1]
        Z = 9.0*max(1.0, 1.5*(8*s1)**(1/6))
        zedges = np.linspace(-Z, Z, nz + 1)
        for j in range(nz):
            z0, z1 = zedges[j], zedges[j+1]
            if EXACTW:
                wlo = whi = W_exact(z0, z1, s0, s1)
            else:
                wlo, whi = W_cell(z0, z1, s0, s1, wedges)
            if whi < 1e-16:
                continue
            tt = sorted([24*math.sqrt(s0)*z0, 24*math.sqrt(s0)*z1, 24*math.sqrt(s1)*z0, 24*math.sqrt(s1)*z1])
            glo, ghi = G_bounds(tt[0], tt[-1], 576*math.sqrt(6)*s0, 576*math.sqrt(6)*s1, vedges)
            Clo += wlo*glo; Chi += whi*ghi
            Wtot_lo += wlo; Wtot_hi += whi
    print('ns=%d nz=%d nv=%d nw=%d: W in [%.7f, %.7f] (target %.7f); C in [%.5f, %.5f] width %.5f  [%.0fs]' % (
        ns, nz, nv, nw, Wtot_lo, Wtot_hi, 0.5*12**(-7/6)*special.gamma(7/6), c0*Clo, c0*Chi, c0*(Chi - Clo), time.time()-t0))
