"""Exploration (floats): size the 2-D midpoint rule in (u, w) = (ln tau, ln g) for D with error bounds obtained by
differentiating the Gaussian kernels (no derivatives of g = I - I_quad needed).

D = int du int dw rho(u, w) H(u, w),  rho(u, w) = A3 tau^{-8/3} g^{11/3} e^{-12 tau^2 g^4 - g^2/4} * (24 tau sqrt(pi))^{-1}... see below,
H(u, w) = E[g(sigma_t Z1, sigma_chi Z2)] with sigma_t = 12 sqrt2 tau, sigma_chi = 576 sqrt6 tau^2 g.
In terms of vform3: int dv F(tau, g, v) = int dt e^{-t^2/(576 tau^2)} E_chi[g] = 24 tau sqrt(pi) * H  (the t-Gaussian is unnormalized).
So D = int du int dw [A3 tau^{-11/3} g^{8/3} e^{-12 tau^2 g^4 - g^2/4} * tau * g] * [24 tau sqrt(pi) H]   (dtau = tau du, dg = g dw)
      =: int du int dw rho(u,w) H(u,w),   rho = 24 sqrt(pi) A3 tau^{-5/3} g^{11/3} e^{-12 tau^2 g^4 - g^2/4}.

Derivatives of H via the kernels (log-scale):  d/d(ln sigma) N_sigma(x) = N_sigma(x) (z^2 - 1), z = x/sigma;
  d^2/d(ln sigma)^2 N = N (z^4 - 4 z^2 + 1).   u enters ln sigma_t with factor 1 and ln sigma_chi with factor 2; w enters ln sigma_chi with 1.
  H_u = E[g (P1(Z1) + 2 P1(Z2))], H_w = E[g P1(Z2)], H_uu = E[g (P2(Z1) + 4 P1(Z1) P1(Z2) + 4 P2(Z2))],
  H_uw = E[g (P1(Z1) P1(Z2) + 2 P2(Z2))], H_ww = E[g P2(Z2)],  P1(z) = z^2 - 1, P2(z) = z^4 - 4 z^2 + 1.
Bounds: |E[g Q]| <= E[|g| |Q|] with |g| <= (10/3)|c'|^3 + 2*16^{-2/3}|c'||R|^{4/3} + R^2/12 + |Iquad|.
"""
import math, sys, time
import numpy as np
from scipy import integrate, special
sys.path.insert(0, '.')
import vform3 as V3

A3 = V3.A3

def rho(u, w):
    tau = math.exp(u); g = math.exp(w)
    return 24*math.sqrt(math.pi)*A3*tau**(-5/3)*g**(11/3)*math.exp(-12*tau*tau*g**4 - g*g/4)

def H_num(u, w):
    """H via vform3: (1/(24 tau sqrt pi)) int dv F."""
    tau = math.exp(u); g = math.exp(w)
    s = 576*math.sqrt(6)*tau*tau*g; sd_t = 12*tau*math.sqrt(2)
    R_max = 8 + 12*8*sd_t + 8*s
    v_hi = (R_max/4)**(1/3) + 1.0
    vs = np.linspace(0, v_hi, 20001)
    Fv = V3.F(tau, g, vs)
    return np.trapezoid(Fv, vs)/(24*tau*math.sqrt(math.pi))

# Monte Carlo-free bound pieces: E[|t|^i |chi|^j |Q(Z)|] with |Q| bounded by absolute monomials.
def absmom(p):
    """E|Z|^p for Z ~ N(0,1)."""
    return 2**(p/2)*special.gamma((p+1)/2)/math.sqrt(math.pi)

def g_bound_terms():
    """|g| <= sum c * |t|^a |chi|^b (with fractional b allowed): returns list of (c, a, b).
    c' = 1 - t, R = 8 - 12 t + chi.  |c'| <= 1 + |t|; |R| <= 8 + 12|t| + |chi|.
    (10/3)|c'|^3 <= (10/3)(1+|t|)^3; 2*16^{-2/3}|c'||R|^{4/3} <= 0.315 (1+|t|) * 2^{1/3} ((8+12|t|)^{4/3} + |chi|^{4/3}) ...
    we expand crudely with (a+b)^p <= 2^{p-1}(a^p + b^p)."""
    terms = []
    # (10/3)(1+|t|)^3
    for k, ck in enumerate([1, 3, 3, 1]): terms.append(((10/3)*ck, k, 0))
    # 0.315 (1+|t|) |R|^{4/3}, |R|^{4/3} <= 2^{1/3} [ (8+12|t|)^{4/3} + |chi|^{4/3} ], (8+12|t|)^{4/3} <= 2^{1/3}(8^{4/3} + (12|t|)^{4/3})
    c = 2*16**(-2/3)*2**(1/3)
    for (ct, a) in ((1, 0), (1, 1)):
        terms.append((c*ct*2**(1/3)*8**(4/3), a, 0)); terms.append((c*ct*2**(1/3)*12**(4/3), a + 4/3, 0)); terms.append((c*ct, a, 4/3))
    # R^2/12 <= (3/12)(64 + 144 t^2 + chi^2)
    terms += [(16.0, 0, 0), (36.0, 2, 0), (0.25, 0, 2)]
    # |Iquad| <= 20/3 + 20|t| + (8/9)|chi| + (52/3) t^2 + (4/3)|t||chi| + (13/486) chi^2
    terms += [(20/3, 0, 0), (20.0, 1, 0), (8/9, 0, 1), (52/3, 2, 0), (4/3, 1, 1), (13/486, 0, 2)]
    return terms

GB = g_bound_terms()

def EgQ(u, w, Q):
    """E[|g| |Q(Z1,Z2)|] bound; Q given as list of (coef, i, j) absolute monomials |Z1|^i |Z2|^j."""
    tau = math.exp(u); g = math.exp(w)
    st = 12*math.sqrt(2)*tau; sc = 576*math.sqrt(6)*tau*tau*g
    tot = 0.0
    for (c, a, b) in GB:
        for (q, i, j) in Q:
            tot += c*q*st**a*sc**b*absmom(a + i)*absmom(b + j)
    return tot

P1abs = [(1, 2, 0), (1, 0, 0)]                     # |z^2 - 1| <= z^2 + 1  (in Z1)
def shift(Q, to2):
    return [(c, (0 if to2 else i), (i if to2 else 0)) for (c, i, j) in Q] if False else None
# explicit absolute-monomial bounds for the kernels
Q_uu = [(1, 4, 0), (4, 2, 0), (1, 0, 0),           # |P2(Z1)| <= z1^4 + 4 z1^2 + 1
        (4, 2, 2), (4, 2, 0), (4, 0, 2), (4, 0, 0),  # 4|P1(Z1)P1(Z2)| <= 4 (z1^2+1)(z2^2+1)
        (4, 0, 4), (16, 0, 2), (4, 0, 0)]           # 4|P2(Z2)|
Q_uw = [(1, 2, 2), (1, 2, 0), (1, 0, 2), (1, 0, 0), (2, 0, 4), (8, 0, 2), (2, 0, 0)]
Q_ww = [(1, 0, 4), (4, 0, 2), (1, 0, 0)]
Q_u = [(1, 2, 0), (1, 0, 0), (2, 0, 2), (2, 0, 0)]
Q_w = [(1, 0, 2), (1, 0, 0)]
Q_0 = [(1, 0, 0)]

def rho_derivs(u, w, e=1e-4):
    r0 = rho(u, w)
    ru = (rho(u+e, w) - rho(u-e, w))/(2*e); rw = (rho(u, w+e) - rho(u, w-e))/(2*e)
    ruu = (rho(u+e, w) - 2*r0 + rho(u-e, w))/e**2; rww = (rho(u, w+e) - 2*r0 + rho(u, w-e))/e**2
    ruw = (rho(u+e, w+e) - rho(u+e, w-e) - rho(u-e, w+e) + rho(u-e, w-e))/(4*e*e)
    return r0, ru, rw, ruu, ruw, rww

def second_deriv_bounds(u, w):
    """bounds on |d^2(rho H)| in uu, uw, ww via the kernel-derivative bounds."""
    r0, ru, rw, ruu, ruw, rww = rho_derivs(u, w)
    H0 = EgQ(u, w, Q_0); Hu = EgQ(u, w, Q_u); Hw = EgQ(u, w, Q_w)
    Huu = EgQ(u, w, Q_uu); Huw = EgQ(u, w, Q_uw); Hww = EgQ(u, w, Q_ww)
    Buu = abs(ruu)*H0 + 2*abs(ru)*Hu + abs(r0)*Huu
    Buw = abs(ruw)*H0 + abs(ru)*Hw + abs(rw)*Hu + abs(r0)*Huw
    Bww = abs(rww)*H0 + 2*abs(rw)*Hw + abs(r0)*Hww
    return Buu, Buw, Bww

if __name__ == '__main__':
    # grid in (u, w); compare the rigorous-style error bound with the actual midpoint error
    u_lo, u_hi = math.log(1e-3), math.log(1e3)
    w_lo, w_hi = math.log(0.05), math.log(6.0)
    t0 = time.time()
    for N in (30, 60):
        Nu, Nw = N, N//2
        hu = (u_hi - u_lo)/(2*Nu); hw = (w_hi - w_lo)/(2*Nw)
        tot = 0.0; err = 0.0
        for i in range(Nu):
            u = u_lo + (2*i + 1)*hu
            for j in range(Nw):
                w = w_lo + (2*j + 1)*hw
                vol = 4*hu*hw
                tot += vol*rho(u, w)*H_num(u, w)
                Buu, Buw, Bww = second_deriv_bounds(u, w)
                err += vol*(hu*hu*Buu/6 + hu*hw*Buw/4 + hw*hw*Bww/6)
        print('N=%d (hu=%.3f hw=%.3f): midpoint D = %.6f, rigorous-style error bound %.4e  [%.0fs]' % (N, hu, hw, tot, err, time.time()-t0)); sys.stdout.flush()
