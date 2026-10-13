"""Prototype 2 (numpy floats) of the rigorous cell scheme for C, with improved G bounds:
  style A: exact f-integral over R-cells (via dPhi/dR at the c'-ends; f increasing in c') times the kernel's range;
  style C: f-range over the widened R-range times (1 - tail), for small s;
  the intersection of the two.  W_cell taken as exact (sizing the G-error only).
f = d^2Phi/dR^2 = 1/24 + (2x+x^2+2x^3)/72, x = c'/psi_e, psi_e = c' + y, y = largest root of y^3 - 3c'^2 y + 2c'^3 - R^2/16.
dPhi/dR = d (2|c'| + d) R / (24 (y^2 - c'^2)), d = psi_e - |c'|; at R = 0+ with c' > 0 it is kappa/2 = (sqrt3/4) c'^{3/2}.
"""
import sys, math, time
import numpy as np
from scipy import special

c0 = 1990656/4800
F13 = 13/243
SQ3 = math.sqrt(3)

def y_root(cp, R):
    cp = np.asarray(cp, float); R = np.asarray(R, float)
    cp, R = np.broadcast_arrays(cp, R)
    sig = np.abs(R)/8.0
    out = np.empty(cp.shape)
    trig = (cp > 0) & (sig**2 <= cp**3)
    with np.errstate(all='ignore'):
        c = cp[trig]; arg = np.clip(sig[trig]*c**-1.5, 0, 1)
        out[trig] = 2*c*np.cos((2/3)*np.arccos(arg))
        o = ~trig; c = cp[o]; sg = sig[o]
        A = sg + np.sqrt(np.maximum(sg**2 - c**3, 0)); A23 = np.cbrt(A)**2
        out[o] = np.where(A > 0, A23 + c**2/np.where(A23 > 0, A23, 1.0), 0.0)
    return out

def f_val(cp, R):
    y = y_root(cp, R); x = cp/(cp + y)
    return 1/24 + (2*x + x*x + 2*x**3)/72

def dPhi(cp, R):
    """dPhi/dR at (c', R), R != 0 (vectorized); the limit kappa/2 at R=0+ for c'>0."""
    cp = np.asarray(cp, float); R = np.asarray(R, float)
    cp, R = np.broadcast_arrays(cp, R)
    y = y_root(cp, R); d = y + cp - np.abs(cp)
    with np.errstate(all='ignore'):
        val = d*(2*np.abs(cp) + d)*R/(24*(y*y - cp*cp))
    small = (np.abs(R) < 1e-12)
    val = np.where(small, np.where(cp > 0, np.sign(R + 0.0)*SQ3/4*np.abs(cp)**1.5, 0.0), val)
    return val

def theta(a):
    return np.exp(-a*a/2)/math.sqrt(2*math.pi) - a*0.5*special.erfc(a/math.sqrt(2))

def Hth(v):   # antiderivative: int_a^b theta = Hth(a) - Hth(b), v >= 0
    return (1+v*v)/2*0.5*special.erfc(v/math.sqrt(2)) - v*np.exp(-v*v/2)/math.sqrt(2*math.pi)/2

def tail_mass(U):   # mass of 2 theta(|v|) beyond |v| > U
    return 2*2*Hth(U)   # 2 * int_U^inf theta = 2*(Hth(U) - 0)

def f_range_box(cp0, cp1, Rlo, Rhi):
    """range of f over c' in [cp0,cp1], |R| in [Rlo,Rhi] (0<=Rlo<=Rhi), using monotonicity; crude if c' straddles 0."""
    if cp0 <= 0 <= cp1:
        return 0.0, 1/16
    if cp0 > 0:
        return f_val(cp0, Rhi), f_val(cp1, Rlo)
    return f_val(cp0, Rlo), f_val(cp1, Rhi)

def G_bounds(t0, t1, s0, s1, nR=400, U=8.0):
    cp0, cp1 = 1 - t1, 1 - t0
    r0, r1 = 8 - 12*t1, 8 - 12*t0
    # ---- style C: f-range over R in [r0 - U s1, r1 + U s1], times (1 - tail)
    Rlo_, Rhi_ = r0 - U*s1, r1 + U*s1
    aRlo = 0.0 if Rlo_ <= 0 <= Rhi_ else min(abs(Rlo_), abs(Rhi_)); aRhi = max(abs(Rlo_), abs(Rhi_))
    fl, fh = f_range_box(cp0, cp1, aRlo, aRhi)
    tl = tail_mass(U)
    PsiC = (fl*(1 - tl), fh*(1 - tl) + tl/16)
    # ---- style A: R-cells on [r0 - U s1, r1 + U s1], exact f-integral per cell at c' ends, kernel range
    edges = np.linspace(Rlo_, Rhi_, nR + 1)
    if Rlo_ < 0 < Rhi_:
        edges = np.unique(np.concatenate([edges, [0.0]]))
    a, b = edges[:-1], edges[1:]
    # exact integral of f over [a,b] at c' = cp0 (min) and cp1 (max): dPhi(b) - dPhi(a), with the jump handled by splitting at 0
    def Fint(cp):
        if cp == 0:
            return (b - a)/24
        va = dPhi(cp, np.where(a == 0, 1e-300, a)); vb = dPhi(cp, np.where(b == 0, -1e-300, b))
        return vb - va
    if cp0 <= 0 <= cp1:
        F_lo = np.zeros_like(a); F_hi = (b - a)/16
    else:
        F_lo = Fint(cp0); F_hi = Fint(cp1)
    # kernel k(R) = (2/s) theta(|R - r|/s), r in [r0,r1], s in [s0,s1]: max <= (2/s0) theta(dmin/s1), min >= (2/s1) theta(dmax/s0)
    dmin = np.maximum(0.0, np.maximum(r0 - b, a - r1))
    dmax = np.maximum(np.abs(a - r0), np.abs(b - r1)); dmax = np.maximum(dmax, np.maximum(np.abs(a - r1), np.abs(b - r0)))
    kmax = (2/s0)*theta(dmin/s1); kmin = (2/s1)*theta(dmax/s0)
    PsiA = ((np.maximum(F_lo, 0)*kmin).sum(), (F_hi*kmax).sum() + tl/16)
    lo = max(PsiA[0], PsiC[0]); hi = min(PsiA[1], PsiC[1])
    return F13 - hi, F13 - lo

_x, _w = np.polynomial.legendre.leggauss(300)
def W_exact(z0, z1, sig0, sig1):
    wn = 3.0*_x + 3.0; ww = 3.0*_w
    g = wn**8*np.exp(-wn**4/4)
    e = special.erf(z1*wn) - special.erf(z0*wn)
    gam = (12*wn**6)**(-7/6)*(special.gammainc(7/6, 12*sig1*wn**6) - special.gammainc(7/6, 12*sig0*wn**6))*special.gamma(7/6)
    return (ww*g*e*gam).sum()/(2*math.sqrt(math.pi))

if __name__ == '__main__':
    ns, nz, nR = [int(a) for a in sys.argv[1:4]]
    t0 = time.time()
    sedges = np.exp(np.linspace(math.log(1e-9), math.log(1e17), ns + 1))
    Clo = Chi = 0.0; Wtot = 0.0
    for i in range(ns):
        s0, s1 = sedges[i], sedges[i+1]
        Z = 9.0*max(1.0, 1.5*(8*s1)**(1/6))
        zedges = np.linspace(-Z, Z, nz + 1)
        for j in range(nz):
            z0, z1 = zedges[j], zedges[j+1]
            W = W_exact(z0, z1, s0, s1)
            if W < 1e-16:
                continue
            tt = sorted([24*math.sqrt(s0)*z0, 24*math.sqrt(s0)*z1, 24*math.sqrt(s1)*z0, 24*math.sqrt(s1)*z1])
            glo, ghi = G_bounds(tt[0], tt[-1], 576*math.sqrt(6)*s0, 576*math.sqrt(6)*s1, nR)
            Clo += W*glo; Chi += W*ghi; Wtot += W
    print('ns=%d nz=%d nR=%d: W=%.7f (target %.7f); C in [%.5f, %.5f] width %.5f  [%.0fs]' % (
        ns, nz, nR, Wtot, 0.5*12**(-7/6)*special.gamma(7/6), c0*Clo, c0*Chi, c0*(Chi - Clo), time.time()-t0))
