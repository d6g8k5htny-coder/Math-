"""Exploration (numpy/scipy, outside the repository): D by the (tau, g, v) reduction with the t-integral in closed form.

D = A3 int_0^inf dtau int_0^inf dg tau^{-11/3} g^{8/3} e^{-12 tau^2 g^4 - g^2/4} int_0^inf dv sum_{sg=+-}
      int_{1 - v^2/3}^inf dt e^{-t^2/(576 tau^2)} P_sg(t, v) e^{-(lam_sg t + mu_sg)^2/(2 s^2)} / (s sqrt(2 pi)),
  s = 576 sqrt6 tau^2 g,  R(v,t) = 4v^3 - 12v + 12 v t,  lam_sg = 12(1 + sg v),  mu_sg = sg(4v^3 - 12v) - 8,
  P_sg(t, v) = [PhiT(t, v) - Iquad(t, sg R - 8 + 12 t)] * 12 (v^2 - 1 + t),
  PhiT(t, v) = v^6/3 - (1-t) v^4 + (4/3)(1-t)^3 [t < 1].
The t-integral of (polynomial) x exp(-alpha (t - tc)^2) is done in closed form with erf/erfc.
Reference: D ~ 0.0767381 (note V24 Remark 1; note DC Remark 1 gives 0.07674).
"""
import math, sys, time
import numpy as np
from scipy import integrate, special

A3 = 1/(57600*math.pi)
SQ6 = math.sqrt(6)

def poly_mul(a, b):
    out = [0.0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out
def poly_add(a, b):
    n = max(len(a), len(b)); out = [0.0]*n
    for i, x in enumerate(a): out[i] += x
    for i, x in enumerate(b): out[i] += x
    return out
def poly_scale(a, c): return [c*x for x in a]
def poly_shift(a, c):
    """coefficients of p(u + c) in powers of u, given p in powers of t (t = u + c)."""
    n = len(a); out = [0.0]*n
    for i, x in enumerate(a):
        # x * (u + c)^i
        for j in range(i+1):
            out[j] += x*math.comb(i, j)*c**(i-j)
    return out

def P_poly(v, sg, branch):
    """P_sg(t, v) as polynomial in t.  branch 'A': t < 1 (c' > 0), 'B': t >= 1."""
    cp = [1.0, -1.0]                       # c' = 1 - t
    cp3 = poly_mul(cp, poly_mul(cp, cp))
    phi = poly_add([v**6/3], poly_scale(cp, -v**4))
    if branch == 'A':
        phi = poly_add(phi, poly_scale(cp3, 4/3))
    R = [4*v**3 - 12*v, 12*v]              # R(v, t)
    chi = poly_add(poly_scale(R, sg), [-8.0, 12.0])   # sg R - 8 + 12 t
    t = [0.0, 1.0]
    iq = poly_add([20/3], poly_scale(t, -20.0))
    iq = poly_add(iq, poly_scale(chi, 8/9))
    iq = poly_add(iq, poly_scale(poly_mul(t, t), 52/3))
    iq = poly_add(iq, poly_scale(poly_mul(t, chi), -4/3))
    iq = poly_add(iq, poly_scale(poly_mul(chi, chi), 13/486))
    diff = poly_add(phi, poly_scale(iq, -1.0))
    Rp = [12*(v*v - 1), 12.0]
    return poly_mul(diff, Rp)

def gauss_moments(alpha, u1, u2, nmax):
    """I_n = int_{u1}^{u2} u^n e^{-alpha u^2} du for n = 0..nmax (u2 may be inf)."""
    sa = math.sqrt(alpha)
    e1 = math.exp(-alpha*u1*u1); e2 = 0.0 if u2 == math.inf else math.exp(-alpha*u2*u2)
    # I0 via erfc for accuracy
    if u2 == math.inf:
        I0 = (math.sqrt(math.pi)/(2*sa))*special.erfc(sa*u1)
    else:
        I0 = (math.sqrt(math.pi)/(2*sa))*(special.erf(sa*u2) - special.erf(sa*u1))
    I = [I0]
    if nmax >= 1:
        I.append((e1 - e2)/(2*alpha))
    for n in range(2, nmax+1):
        b1 = u1**(n-1)*e1; b2 = 0.0 if u2 == math.inf else u2**(n-1)*e2
        I.append(((n-1)/(2*alpha))*I[n-2] - (b2 - b1)/(2*alpha))
    return I

def t_integral(tau, g, v, sg):
    """int_{1-v^2/3}^inf dt e^{-t^2/(576 tau^2)} P_sg(t,v) e^{-(lam t + mu)^2/(2 s^2)}/(s sqrt(2pi)), split at t = 1."""
    s = 576*SQ6*tau*tau*g
    a = 1/(576*tau*tau)
    lam = 12*(1 + sg*v); mu = sg*(4*v**3 - 12*v) - 8
    alpha = a + lam*lam/(2*s*s)
    beta = lam*mu/(s*s)              # coefficient of t
    const = mu*mu/(2*s*s)
    tc = -beta/(2*alpha)
    # exponent: -alpha t^2 - beta t - const = -alpha (t - tc)^2 + alpha tc^2 - const
    logpre = alpha*tc*tc - const
    if logpre < -700: return 0.0
    pre = math.exp(logpre)/(s*math.sqrt(2*math.pi))
    total = 0.0
    t1 = 1 - v*v/3
    for (lo, hi, branch) in ((t1, 1.0, 'A'), (1.0, math.inf, 'B')):
        if hi <= lo: continue
        p = P_poly(v, sg, branch)
        q = poly_shift(p, tc)        # in u = t - tc
        u1, u2 = lo - tc, (math.inf if hi == math.inf else hi - tc)
        mom = gauss_moments(alpha, u1, u2, len(q)-1)
        total += sum(c*m for c, m in zip(q, mom))
    return pre*total

def inner_v(tau, g):
    f = lambda v: t_integral(tau, g, v, 1) + t_integral(tau, g, v, -1)
    # v where R ~ 8 at t ~ 0: 4v^3 - 12 v = 8 -> v = 2; the mass concentrates near v = 2 for small tau
    s = 576*SQ6*tau*tau*g
    width = max(1e-3, min(1.0, 5*s/36 + 60*tau))
    pts = [p for p in (2 - width, 2.0, 2 + width) if 0 < p < 12]
    val, err = integrate.quad(f, 0.0, 12.0, points=pts, limit=400)
    return val

def D_value(tau_lo=1e-7, tau_hi=40.0, eps=1e-7):
    def inner_g(tau):
        f = lambda g: g**(8/3)*math.exp(-12*tau*tau*g**4 - g*g/4)*inner_v(tau, g)
        val, err = integrate.quad(f, 0.0, 9.0, limit=200)
        return tau**(-11/3)*val
    val, err = integrate.quad(inner_g, tau_lo, tau_hi, limit=400, epsrel=eps, epsabs=0)
    return A3*val, A3*err

if __name__ == '__main__':
    t0 = time.time()
    # the inner t-integral against brute force for a few points
    def brute(tau, g, v, sg):
        s = 576*SQ6*tau*tau*g
        def f(t):
            branch = 'A' if t < 1 else 'B'
            p = P_poly(v, sg, branch); pt = sum(c*t**i for i, c in enumerate(p))
            lam = 12*(1+sg*v); mu = sg*(4*v**3-12*v) - 8
            return math.exp(-t*t/(576*tau*tau))*pt*math.exp(-(lam*t+mu)**2/(2*s*s))/(s*math.sqrt(2*math.pi))
        lo = 1 - v*v/3
        val, err = integrate.quad(f, lo, lo + 60, points=[1.0] if lo < 1 else None, limit=400)
        return val
    for (tau, g, v, sg) in ((0.05, 1.0, 2.0, 1), (0.05, 1.0, 2.0, -1), (0.3, 2.0, 1.5, 1), (0.01, 0.5, 2.1, 1), (1.0, 1.0, 0.5, -1)):
        print('t-integral tau=%g g=%g v=%g sg=%+d: closed %.12g  brute %.12g' % (tau, g, v, sg, t_integral(tau, g, v, sg), brute(tau, g, v, sg)))
    if len(sys.argv) > 1 and sys.argv[1] == 'D':
        for tau_lo in (1e-4, 1e-6):
            D, err = D_value(tau_lo=tau_lo)
            print('tau_lo=%g: D = %.8f (quad err %.1e)  [%.0fs]' % (tau_lo, D, err, time.time()-t0))
    if len(sys.argv) > 1 and sys.argv[1] == 'small':
        # the small-tau behaviour of the tau-integrand: should be ~ C tau^{-2/3}
        for tau in (1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 1e-5, 1e-6):
            f = lambda g: g**(8/3)*math.exp(-12*tau*tau*g**4 - g*g/4)*inner_v(tau, g)
            val, err = integrate.quad(f, 0.0, 9.0, limit=200)
            print('tau=%g: integrand*tau^{2/3} = %.6g' % (tau, A3*tau**(-11/3)*val*tau**(2/3)))
