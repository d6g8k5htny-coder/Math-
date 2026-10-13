"""Exploration (floats): adaptive 2-D midpoint rule in (u, w) = (ln tau, ln g) for D, with per-cell error bounds from
kernel derivatives and a hybrid bound on |g| (cubic near the origin, crude polynomial outside); counts the cells needed
for a target total error bound.  The near-origin cubic constant C3 is a placeholder (to be certified by the exact
region-S computation); here it is estimated numerically from g itself.
"""
import math, sys, time, heapq
import numpy as np
from scipy import integrate, special
sys.path.insert(0, '.')
import vform3 as V3
from stein_bounds import rho, H_num, absmom, GB, Q_uu, Q_uw, Q_ww, Q_u, Q_w, Q_0, rho_derivs

BOX = 0.25        # |t|, |chi| <= BOX: cubic bound region
C3 = 60.0         # |g| <= C3 (|t| + |chi|)^3 on the box (placeholder; measured below)

def measure_C3():
    import vform1 as V1
    worst = 0.0
    for t in np.linspace(-BOX, BOX, 41):
        for chi in np.linspace(-BOX, BOX, 41):
            r = abs(t) + abs(chi)
            if r < 1e-6: continue
            g = V1.Phi_R(1 - t, 8 - 12*t + chi) - V1.Iquad(t, chi)
            worst = max(worst, abs(g)/r**3)
    return worst

def inc_absmom(p, a, sigma):
    """E[|X|^p 1{|X| > a}] for X ~ N(0, sigma^2): numerical (floats) via quad."""
    if a <= 0: return sigma**p*absmom(p)
    # E[|X|^p 1{|X|>a}] = sigma^p 2^{p/2} Gamma((p+1)/2, a^2/(2 sigma^2)) / sqrt(pi)
    return sigma**p*2**(p/2)*special.gamma((p+1)/2)*special.gammaincc((p+1)/2, a*a/(2*sigma*sigma))/math.sqrt(math.pi)

def EgQ_hybrid(u, w, Q):
    """E[|g| |Q|] <= C3 E[(|t|+|chi|)^3 |Q| 1_box] + E[crude |Q| 1_outside]
       <= C3 sum_k C(3,k) E[|t|^k |chi|^{3-k} |Q|] (box dropped: upper bound) + sum over crude terms of
          c E[|t|^a|chi|^b |Q| 1{|t|>BOX or |chi|>BOX}]."""
    tau = math.exp(u); g = math.exp(w)
    st = 12*math.sqrt(2)*tau; sc = 576*math.sqrt(6)*tau*tau*g
    tot = 0.0
    for (q, i, j) in Q:
        for k in range(4):
            tot += C3*math.comb(3, k)*q*min(st**k*absmom(k+i), BOX**k*absmom(i))*min(sc**(3-k)*absmom(3-k+j), BOX**(3-k)*absmom(j))
        for (c, a, b) in GB:
            # 1{|t|>BOX or |chi|>BOX} <= 1{|t|>BOX} + 1{|chi|>BOX}
            tot += c*q*(inc_absmom(a + i, BOX, st)/st**i*sc**b*absmom(b+j) + st**a*absmom(a+i)*inc_absmom(b + j, BOX, sc)/sc**j)
    return tot

def second_deriv_bounds(u, w):
    r0, ru, rw, ruu, ruw, rww = rho_derivs(u, w)
    H0 = EgQ_hybrid(u, w, Q_0); Hu = EgQ_hybrid(u, w, Q_u); Hw = EgQ_hybrid(u, w, Q_w)
    Huu = EgQ_hybrid(u, w, Q_uu); Huw = EgQ_hybrid(u, w, Q_uw); Hww = EgQ_hybrid(u, w, Q_ww)
    Buu = abs(ruu)*H0 + 2*abs(ru)*Hu + abs(r0)*Huu
    Buw = abs(ruw)*H0 + abs(ru)*Hw + abs(rw)*Hu + abs(r0)*Huw
    Bww = abs(rww)*H0 + 2*abs(rw)*Hw + abs(r0)*Hww
    return Buu, Buw, Bww

def cell_bound(uc, hu, wc, hw):
    """error bound for the midpoint rule on the cell, using derivative bounds sampled at the corners/centre (float proxy
    for the interval evaluation)."""
    B = [0.0, 0.0, 0.0]
    for du in (-hu, 0, hu):
        for dw in (-hw, 0, hw):
            b = second_deriv_bounds(uc + du, wc + dw)
            B = [max(x, y) for x, y in zip(B, b)]
    vol = 4*hu*hw
    return vol*(hu*hu*B[0]/6 + hu*hw*B[1]/4 + hw*hw*B[2]/6)

if __name__ == '__main__':
    pass
    c3m = measure_C3(); print('measured C3 ~ %.3f on the box %.2f' % (c3m, BOX))
    globals()["C3"] = 1.5*c3m
    u_lo, u_hi = math.log(1e-3), math.log(1e3)
    target = float(sys.argv[1]) if len(sys.argv) > 1 else 2e-3
    max_cells = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    # initial cells: u-slabs with per-slab w-range
    cells = []
    Nu0 = 24
    for i in range(Nu0):
        hu = (u_hi - u_lo)/(2*Nu0); uc = u_lo + (2*i + 1)*hu
        tau = math.exp(uc)
        g_hi = min(9.0, (60/(12*tau*tau))**0.25 + 0.5); g_lo = 1e-3*g_hi
        w_lo, w_hi = math.log(g_lo), math.log(g_hi)
        Nw0 = 6
        for j in range(Nw0):
            hw = (w_hi - w_lo)/(2*Nw0); wc = w_lo + (2*j + 1)*hw
            cells.append((uc, hu, wc, hw))
    t0 = time.time()
    heap = []
    for (uc, hu, wc, hw) in cells:
        b = cell_bound(uc, hu, wc, hw)
        heapq.heappush(heap, (-b, uc, hu, wc, hw))
    n = len(heap)
    while True:
        total = sum(-x[0] for x in heap)
        if total <= target or n >= max_cells: break
        negb, uc, hu, wc, hw = heapq.heappop(heap)
        # split along the axis with larger scaled extent... use the larger of hu/scale_u, hw/scale_w; simple: alternate by size
        if hu >= hw:
            for s in (-1, 1):
                b = cell_bound(uc + s*hu/2, hu/2, wc, hw); heapq.heappush(heap, (-b, uc + s*hu/2, hu/2, wc, hw))
        else:
            for s in (-1, 1):
                b = cell_bound(uc, hu, wc + s*hw/2, hw/2); heapq.heappush(heap, (-b, uc, hu, wc + s*hw/2, hw/2))
        n += 1
        if n % 200 == 0:
            print('  cells %d total bound %.4e (%.0fs)' % (n, total, time.time()-t0)); sys.stdout.flush()
    print('cells %d, total error bound %.4e' % (n, sum(-x[0] for x in heap)))
    # midpoint value on the final cells
    D = sum(4*hu*hw*rho(uc, wc)*H_num(uc, wc) for (_, uc, hu, wc, hw) in heap)
    print('midpoint D on these cells = %.6f  [%.0fs]' % (D, time.time()-t0))
