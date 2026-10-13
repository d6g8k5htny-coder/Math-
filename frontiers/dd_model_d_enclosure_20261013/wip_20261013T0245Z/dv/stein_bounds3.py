"""Exploration (floats): cell count for the 2-D midpoint rule in (u, w) with the corrected error bounds
|E[g Q]| <= |E[T_N Q]| + E[|T_N| |Q| 1_out] + C_{N+1} E[rho^{N+1} |Q| 1_box] + E[crude |Q| 1_out],  N = 7.
T_7 is the exact Taylor polynomial of g at the origin (from the sympy/Fraction computation); C_8 is measured numerically here
(to be certified in the exact region-S computation)."""
import math, sys, time, heapq
import numpy as np
from scipy import special
sys.path.insert(0, '.')
from stein_bounds import rho, H_num, absmom, GB, rho_derivs
from fractions import Fraction as Fr

T7 = {(0,3): Fr(-5,52488), (2,1): Fr(14,81), (3,0): Fr(-28,9),
      (0,4): Fr(43,15116544), (1,3): Fr(-5,34992), (2,2): Fr(5,5832), (3,1): Fr(7,243), (4,0): Fr(-7,27),
      (0,5): Fr(-131,1224440064), (1,4): Fr(43,5038848), (2,3): Fr(-67,314928), (3,2): Fr(25,17496), (4,1): Fr(2,243), (5,0): Fr(-7,81),
      (0,6): Fr(2405,528958107648), (1,5): Fr(-131,272097792), (2,4): Fr(7621,408146688), (3,3): Fr(-299,944784), (4,2): Fr(71,34992), (5,1): Fr(1,1458), (6,0): Fr(-1,27),
      (0,7): Fr(-31,148769467776), (1,6): Fr(2405,88159684608), (2,5): Fr(-1291,918330048), (3,4): Fr(1375,38263752), (4,3): Fr(-995,2125764), (5,2): Fr(145,52488), (6,1): Fr(-8,2187), (7,0): Fr(-4,243)}
T7f = {k: float(v) for k, v in T7.items()}
BOX = 0.3
C8 = None

def measure_C8():
    import vform1 as V1
    worst = 0.0
    for t in np.linspace(-BOX, BOX, 61):
        for chi in np.linspace(-BOX, BOX, 61):
            r = abs(t) + abs(chi)
            if r < 1e-3: continue
            g = V1.Phi_R(1 - t, 8 - 12*t + chi) - V1.Iquad(t, chi)
            T = sum(c*t**a*chi**b for (a, b), c in T7f.items())
            worst = max(worst, abs(g - T)/r**8)
    return worst

def mom(n):           # E[Z^n]
    return 0.0 if n % 2 else float(math.prod(range(n - 1, 0, -2))) if n > 0 else 1.0
def inc_absmom(p, a, sigma):
    if a <= 0: return sigma**p*absmom(p)
    return sigma**p*2**(p/2)*special.gamma((p+1)/2)*special.gammaincc((p+1)/2, a*a/(2*sigma*sigma))/math.sqrt(math.pi)
def trunc_absmom(p, a, sigma):
    """E[|X|^p 1{|X| <= a}] <= min(sigma^p absmom(p), a^p)."""
    return min(sigma**p*absmom(p), a**p)

# kernel polynomials as signed dicts {(i, j): coef} in (Z1, Z2)
def P1(idx):
    return {(2 if idx == 1 else 0, 2 if idx == 2 else 0): 1.0, (0, 0): -1.0}
def P2(idx):
    return {(4 if idx == 1 else 0, 4 if idx == 2 else 0): 1.0, (2 if idx == 1 else 0, 2 if idx == 2 else 0): -4.0, (0, 0): 1.0}
def padd(*ps):
    out = {}
    for s, p in ps:
        for k, v in p.items(): out[k] = out.get(k, 0.0) + s*v
    return out
def pmul(p, q):
    out = {}
    for (i, j), a in p.items():
        for (k, l), b in q.items():
            out[(i+k, j+l)] = out.get((i+k, j+l), 0.0) + a*b
    return out
Q_0 = {(0, 0): 1.0}
Q_u = padd((1, P1(1)), (2, P1(2))); Q_w = P1(2)
Q_uu = padd((1, P2(1)), (4, pmul(P1(1), P1(2))), (4, P2(2)))
Q_uw = padd((1, pmul(P1(1), P1(2))), (2, P2(2)))
Q_ww = P2(2)

def EgQ_bound(st, sc, Q):
    # exact E[T7 Q]
    exact = 0.0
    for (a, b), c in T7f.items():
        for (i, j), q in Q.items():
            exact += c*q*st**a*sc**b*mom(a + i)*mom(b + j)
    # T7 part on the box: min of (a) |E[T7 Q]| + E[|T7||Q| 1_out] and (b) sup_box|T7| * E[|Q|]
    ta = abs(exact); tb = 0.0
    supT = sum(abs(c)*BOX**(a + b) for (a, b), c in T7f.items())
    for (i, j), q in Q.items():
        qa = abs(q)
        for (a, b), c in T7f.items():
            ta += abs(c)*qa*(inc_absmom(a + i, BOX, st)/st**i*sc**b*absmom(b + j) + st**a*absmom(a + i)*inc_absmom(b + j, BOX, sc)/sc**j)
        tb += supT*qa*absmom(i)*absmom(j)
    tot = min(ta, tb)
    for (i, j), q in Q.items():
        qa = abs(q)
        # C8 E[rho^8 |Q| 1_box], rho = |t| + |chi|
        for k in range(9):
            tot += C8*math.comb(8, k)*qa*min(st**k*absmom(k + i), BOX**k*absmom(i))*min(sc**(8-k)*absmom(8-k+j), BOX**(8-k)*absmom(j))
        # crude outside
        for (c, a, b) in GB:
            tot += c*qa*(inc_absmom(a + i, BOX, st)/st**i*sc**b*absmom(b+j) + st**a*absmom(a+i)*inc_absmom(b + j, BOX, sc)/sc**j)
    return tot

def second_deriv_bounds(u, w):
    tau = math.exp(u); g = math.exp(w)
    st = 12*math.sqrt(2)*tau; sc = 576*math.sqrt(6)*tau*tau*g
    r0, ru, rw, ruu, ruw, rww = rho_derivs(u, w)
    H0 = EgQ_bound(st, sc, Q_0); Hu = EgQ_bound(st, sc, Q_u); Hw = EgQ_bound(st, sc, Q_w)
    Huu = EgQ_bound(st, sc, Q_uu); Huw = EgQ_bound(st, sc, Q_uw); Hww = EgQ_bound(st, sc, Q_ww)
    Buu = abs(ruu)*H0 + 2*abs(ru)*Hu + abs(r0)*Huu
    Buw = abs(ruw)*H0 + abs(ru)*Hw + abs(rw)*Hu + abs(r0)*Huw
    Bww = abs(rww)*H0 + 2*abs(rw)*Hw + abs(r0)*Hww
    return Buu, Buw, Bww

def cell_bound(uc, hu, wc, hw):
    B = [0.0, 0.0, 0.0]
    for du in (-hu, 0, hu):
        for dw in (-hw, 0, hw):
            b = second_deriv_bounds(uc + du, wc + dw)
            B = [max(x, y) for x, y in zip(B, b)]
    vol = 4*hu*hw
    return vol*(hu*hu*B[0]/6 + hu*hw*B[1]/4 + hw*hw*B[2]/6)

if __name__ == '__main__':
    C8 = 1.5*measure_C8(); print('C8 ~ %.4g (x1.5 margin) on the box %.2f' % (C8, BOX))
    u_lo, u_hi = math.log(float(sys.argv[3]) if len(sys.argv) > 3 else 1e-3), math.log(1e3)
    target = float(sys.argv[1]) if len(sys.argv) > 1 else 2e-3
    max_cells = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    cells = []
    Nu0 = 30
    for i in range(Nu0):
        hu = (u_hi - u_lo)/(2*Nu0); uc = u_lo + (2*i + 1)*hu
        tau = math.exp(uc)
        g_hi = min(9.0, (60/(12*tau*tau))**0.25 + 0.5); g_lo = 1e-3*g_hi
        w_lo, w_hi = math.log(g_lo), math.log(g_hi)
        Nw0 = 8
        for j in range(Nw0):
            hw = (w_hi - w_lo)/(2*Nw0); wc = w_lo + (2*j + 1)*hw
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
    print('cells %d, total error bound %.4e [%.0fs]' % (n, tot, time.time()-t0))
    worst = sorted(heap)[:5]
    for negb, uc, hu, wc, hw in worst:
        print('  worst cell bound %.3e at tau=%.3g g=%.3g hu=%.3f hw=%.3f' % (-negb, math.exp(uc), math.exp(wc), hu, hw))
    D = sum(4*hu*hw*rho(uc, wc)*H_num(uc, wc) for (_, uc, hu, wc, hw) in heap)
    print('midpoint D on these cells = %.6f  [%.0fs]' % (D, time.time()-t0))
