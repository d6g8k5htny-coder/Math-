"""Exploration (floats): cell count for a tensor 3-point Gauss-Legendre rule in (u, w) with the remainder bounded through
6th-derivative bounds of rho*H (kernel polynomials p_6; sharper |g| bound).  1-D 3-point Gauss error on [c-h, c+h]:
|E| <= (2h)^7 (3!)^4 / (7 (6!)^3) sup|f^(6)| = 128 h^7 * 1296/(7*373248000) sup|f^(6)|.
For the tensor rule the error is bounded by the sum over the two variables of the 1-D errors integrated over the other.
"""
import math, sys, time, heapq
sys.path.insert(0, '.')
from stein_bounds import rho, absmom
from stein_bounds4 import ST, P, p_next, kern2, padd, Ebound

NG = int(__import__('os').environ.get('NGAUSS', '3')); DER = 2*NG
while len(P) < DER + 1: P.append(p_next(P[-1]))
def kernel(a, b):
    out = {}
    for k in range(a + 1):
        c = math.comb(a, k)*2**(a - k)
        out = padd((1, out), (c, kern2(k, a - k + b)))
    return out

def rho_derivs6(u, w, e=4e-3):
    f = lambda du, dw: rho(u + du, w + dw)
    d = {}
    for a in range(DER + 1):
        for b in (0,) if a > 0 else range(DER + 1):
            val = 0.0
            for i in range(a + 1):
                for j in range(b + 1):
                    val += (-1)**(i + j)*math.comb(a, i)*math.comb(b, j)*f((a/2 - i)*e, (b/2 - j)*e)
            d[(a, b)] = val/e**(a + b)
    return d

# 1-D n-point Gauss error on [c-h, c+h]: (2h)^(2n+1) (n!)^4 / ((2n+1) ((2n)!)^3) sup|f^(2n)|
KCONST = (2**(2*NG + 1))*(math.factorial(NG)**4)/((2*NG + 1)*(math.factorial(2*NG)**3))

def sixth_bounds(u, w):
    tau = math.exp(u); g = math.exp(w)
    st = 12*math.sqrt(2)*tau; sc = 576*math.sqrt(6)*tau*tau*g
    rd = rho_derivs6(u, w)
    Hu = [Ebound(st, sc, kernel(a, 0)) for a in range(DER + 1)]
    Hw = [Ebound(st, sc, kernel(0, b)) for b in range(DER + 1)]
    Bu = sum(math.comb(DER, i)*abs(rd[(i, 0)])*Hu[DER - i] for i in range(DER + 1))
    Bw = sum(math.comb(DER, j)*abs(rd[(0, j)])*Hw[DER - j] for j in range(DER + 1))
    return Bu, Bw

def cell_bound(uc, hu, wc, hw):
    B = [0.0, 0.0]
    for du in (-hu, 0, hu):
        for dw in (-hw, 0, hw):
            b = sixth_bounds(uc + du, wc + dw)
            B = [max(x, y) for x, y in zip(B, b)]
    return KCONST*(hu**(DER + 1)*B[0]*2*hw + hw**(DER + 1)*B[1]*2*hu)

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
    print('cells %d, total Gauss-3 remainder bound %.4e [%.0fs]' % (n, tot, time.time()-t0))
    for negb, uc, hu, wc, hw in sorted(heap)[:5]:
        print('  worst cell bound %.3e at tau=%.3g g=%.3g hu=%.3f hw=%.3f' % (-negb, math.exp(uc), math.exp(wc), hu, hw))
