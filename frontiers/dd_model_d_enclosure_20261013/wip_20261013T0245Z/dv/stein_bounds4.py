"""Exploration (floats): cell count for the CORRECTED midpoint rule (midpoint + exact second-derivative correction at the
centre) in (u, w), with the remainder bounded through 4th-derivative bounds of rho*H built from the sharper |g| bound
and the kernel polynomials p_n (L^n N = N p_n, L = d/dln sigma, p_{n+1} = p_1 p_n - z p_n').
Remainder per cell <= vol [h_u^4 B_uuuu/120 + h_u^2 h_w^2 B_uuww/36 + h_w^4 B_wwww/120]."""
import math, sys, time, heapq
import numpy as np
from scipy import special
sys.path.insert(0, '.')
from stein_bounds import rho, H_num, absmom

# ---- sharper |g| bound terms (c, a, b): |g| <= sum c |t|^a |chi|^b   (identity (2.7); see the measurement script)
def sharper_terms():
    T = [(23/3888, 0, 2), (5/9, 0, 1), (5/6, 1, 1), (16/3, 0, 0), (16, 1, 0), (43/3, 2, 0)]
    for k, ck in enumerate([1, 3, 3, 1]): T.append((8*ck, k, 0))
    r23 = [(8**(2/3)/16**(1/3), 0, 0), (12**(2/3)/16**(1/3), 2/3, 0), (1/16**(1/3), 0, 2/3)]
    r43 = [(3**(1/3)*8**(4/3)/16**(2/3), 0, 0), (3**(1/3)*12**(4/3)/16**(2/3), 4/3, 0), (3**(1/3)/16**(2/3), 0, 4/3)]
    for (ct, a) in ((1, 0), (2, 1), (1, 2)):
        for (c, p, q) in r23: T.append((5*ct*c, a + p, q))
    for (ct, a) in ((1, 0), (1, 1)):
        for (c, p, q) in r43: T.append((ct*c, a + p, q))
    return T
ST = sharper_terms()

# ---- kernel polynomials in one variable as {power: coef}
def p_next(p):
    # p_{n+1} = (z^2 - 1) p - z p'
    out = {}
    for k, c in p.items():
        out[k + 2] = out.get(k + 2, 0.0) + c
        out[k] = out.get(k, 0.0) - c
        if k > 0: out[k] = out.get(k, 0.0) - k*c
    return out
P = [{0: 1.0}]
for n in range(6): P.append(p_next(P[-1]))
def kern2(a, b):
    """polynomial in (Z1, Z2): p_a(Z1) p_b(Z2) as {(i, j): coef}."""
    return {(i, j): ci*cj for i, ci in P[a].items() for j, cj in P[b].items()}
def padd(*ps):
    out = {}
    for s, p in ps:
        for k, v in p.items(): out[k] = out.get(k, 0.0) + s*v
    return out
# d/du = L1 + 2 L2, d/dw = L2 (L_i acts on sigma_i); the kernel for d_u^a d_w^b is sum over binomial expansion
def kernel(a, b):
    out = {}
    for k in range(a + 1):
        c = math.comb(a, k)*2**(a - k)
        out = padd((1, out), (c, kern2(k, a - k + b)))
    return out

def Ebound(st, sc, Q):
    tot = 0.0
    for (c, a, b) in ST:
        for (i, j), q in Q.items():
            tot += c*abs(q)*st**a*sc**b*absmom(a + i)*absmom(b + j)
    return tot

def rho_derivs4(u, w, e=2e-3):
    """finite-difference derivatives of rho up to order 4 in u and w (float proxy)."""
    f = lambda du, dw: rho(u + du, w + dw)
    d = {}
    for a in range(5):
        for b in range(5 - a):
            # central differences via binomial stencils
            val = 0.0
            for i in range(a + 1):
                for j in range(b + 1):
                    val += (-1)**(i + j)*math.comb(a, i)*math.comb(b, j)*f((a/2 - i)*e, (b/2 - j)*e)
            d[(a, b)] = val/e**(a + b)
    return d

def fourth_bounds(u, w):
    tau = math.exp(u); g = math.exp(w)
    st = 12*math.sqrt(2)*tau; sc = 576*math.sqrt(6)*tau*tau*g
    rd = rho_derivs4(u, w)
    Hb = {(a, b): Ebound(st, sc, kernel(a, b)) for a in range(5) for b in range(5 - a)}
    def B(a, b):   # bound on |d_u^a d_w^b (rho H)|
        tot = 0.0
        for i in range(a + 1):
            for j in range(b + 1):
                tot += math.comb(a, i)*math.comb(b, j)*abs(rd[(i, j)])*Hb[(a - i, b - j)]
        return tot
    return B(4, 0), B(2, 2), B(0, 4)

def cell_bound(uc, hu, wc, hw):
    B = [0.0, 0.0, 0.0]
    for du in (-hu, 0, hu):
        for dw in (-hw, 0, hw):
            b = fourth_bounds(uc + du, wc + dw)
            B = [max(x, y) for x, y in zip(B, b)]
    vol = 4*hu*hw
    return vol*(hu**4*B[0]/120 + hu*hu*hw*hw*B[1]/36 + hw**4*B[2]/120)

if __name__ == '__main__':
    u_lo, u_hi = math.log(float(sys.argv[3]) if len(sys.argv) > 3 else 1e-2), math.log(1e3)
    target = float(sys.argv[1]) if len(sys.argv) > 1 else 2e-3
    max_cells = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    cells = []
    Nu0 = 30
    for i in range(Nu0):
        hu = (u_hi - u_lo)/(2*Nu0); uc = u_lo + (2*i + 1)*hu
        tau = math.exp(uc)
        g_hi = min(9.0, (60/(12*tau*tau))**0.25 + 0.5); g_lo = 1e-3*g_hi
        w_lo, w_hi = math.log(g_lo), math.log(g_hi)
        for j in range(8):
            hw = (w_hi - w_lo)/16; wc = w_lo + (2*j + 1)*hw
            cells.append((uc, hu, wc, hw))
    t0 = time.time(); heap = []
    for (uc, hu, wc, hw) in cells:
        heapq.heappush(heap, (-cell_bound(uc, hu, wc, hw), uc, hu, wc, hw))
    n = len(heap)
    while True:
        total = sum(-x[0] for x in heap)
        if total <= target or n >= max_cells: break
        negb, uc, hu, wc, hw = heapq.heappop(heap)
        if hu >= hw:
            for s in (-1, 1): heapq.heappush(heap, (-cell_bound(uc + s*hu/2, hu/2, wc, hw), uc + s*hu/2, hu/2, wc, hw))
        else:
            for s in (-1, 1): heapq.heappush(heap, (-cell_bound(uc, hu, wc + s*hw/2, hw/2), uc, hu, wc + s*hw/2, hw/2))
        n += 1
        if n % 500 == 0:
            print('  cells %d total bound %.4e (%.0fs)' % (n, total, time.time()-t0)); sys.stdout.flush()
    tot = sum(-x[0] for x in heap)
    print('cells %d, total 4th-order remainder bound %.4e [%.0fs]' % (n, tot, time.time()-t0))
    for negb, uc, hu, wc, hw in sorted(heap)[:5]:
        print('  worst cell bound %.3e at tau=%.3g g=%.3g hu=%.3f hw=%.3f' % (-negb, math.exp(uc), math.exp(wc), hu, hw))
