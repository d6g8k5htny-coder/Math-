"""Tests of ddbounds: (1) the pointwise bound |g| <= g~ against the float evaluation of g (vform1), (2) the exact Bell
polynomials of rho against finite differences, (3) cell_remainder on sample cells against the float estimate of
stein_bounds5 (NGAUSS=4), with timing."""
import sys, os, math, time, random
from fractions import Fraction as Fr
from decimal import Decimal as Dec
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'dv'))
import ddbounds as B
import ddcore as C
import vform1 as V1

def gtilde(t, chi):
    tot = 0.0
    for (c, a, b) in B.SHARPER:
        tot += float(c[1]) * abs(t) ** float(a) * abs(chi) ** float(b)
    return tot

def test_sharper():
    random.seed(1)
    worst = 0.0; n = 0
    pts = [(t, chi) for t in [-30, -5, -1, -0.5, 0, 0.3, 0.9, 1, 1.1, 2, 5, 30] for chi in [-3000, -100, -8, -1, 0, 1, 8, 100, 3000]]
    for _ in range(4000):
        pts.append((random.uniform(-40, 40), random.uniform(-5000, 5000)))
    for _ in range(2000):
        pts.append((random.uniform(-2, 2), random.uniform(-20, 20)))
    for (t, chi) in pts:
        g = V1.Phi_R(1 - t, 8 - 12 * t + chi) - V1.Iquad(t, chi)
        gt = gtilde(t, chi)
        assert abs(g) <= gt * (1 + 1e-9), (t, chi, g, gt)
        worst = max(worst, abs(g) / gt); n += 1
    print('sharper bound holds at %d points; max |g|/g~ = %.4f' % (n, worst))

def test_bell():
    # d^k/du^k rho at (u, w) by finite differences vs rho * B_k(X, Y)
    import ddtaylor as TT
    u, w = math.log(0.37), math.log(1.3)
    c0 = float(B.RHO_C0[0])
    def rho(uu, ww):
        tau = math.exp(uu); g = math.exp(ww)
        return c0 * tau ** (-5 / 3) * g ** (11 / 3) * math.exp(-12 * tau * tau * g ** 4 - g * g / 4)
    X = math.exp(2 * u + 4 * w); Y = math.exp(2 * w)
    for direction in ('u', 'w'):
        Bs = B.bell_polys(direction, 4)
        for k in range(1, 5):
            e = 1e-2
            val = 0.0
            for i in range(k + 1):
                d = (k / 2 - i) * e
                val += (-1) ** i * math.comb(k, i) * (rho(u + d, w) if direction == 'u' else rho(u, w + d))
            fd = val / e ** k
            ex = rho(u, w) * sum(float(c) * X ** i * Y ** j for (i, j), c in Bs[k].items())
            rel = abs(fd - ex) / max(abs(ex), 1e-300)
            print('  d_%s^%d rho: FD %.6e  Bell %.6e  rel %.1e' % (direction, k, fd, ex, rel))
            assert rel < 2e-2, (direction, k, fd, ex)
    print('Bell polynomials agree with finite differences')

def test_cells():
    os.environ['NGAUSS'] = '4'
    import stein_bounds5 as S5
    tp = B.TaylorPart(11, Fr(1, 2), Fr(1, 10))
    print('TaylorPart: C_12 = %s' % tp.C[1])
    cells = [(0.4, 0.1, 1.0, 0.1), (0.02, 0.05, 0.5, 0.2), (3.0, 0.1, 0.3, 0.1), (30.0, 0.2, 0.1, 0.2), (0.005, 0.05, 2.0, 0.3), (300.0, 0.3, 0.05, 0.3)]
    for (tau, hu, g, hw) in cells:
        uc = math.log(tau); wc = math.log(g)
        t0 = time.time()
        E = B.cell_remainder(Dec(repr(uc)), Dec(repr(hu)), Dec(repr(wc)), Dec(repr(hw)), 4, tp)[0]
        t1 = time.time()
        Ep = B.cell_remainder(Dec(repr(uc)), Dec(repr(hu)), Dec(repr(wc)), Dec(repr(hw)), 4, None)[0]
        t2 = time.time()
        f = S5.cell_bound(uc, hu, wc, hw)
        print('cell tau=%g hu=%g g=%g hw=%g: rigorous %.4e (%.1fs; plain-only %.4e, %.1fs) float-estimate %.4e' % (tau, hu, g, hw, float(E), t1 - t0, float(Ep), t2 - t1, f))

if __name__ == '__main__':
    which = sys.argv[1:] or ['sharper', 'bell', 'cells']
    if 'sharper' in which: test_sharper()
    if 'bell' in which: test_bell()
    if 'cells' in which: test_cells()
