"""Rigorous one-dimensional v-quadrature of F(tau, g, v) at a point (tau, g): adaptive cells, one-variable Taylor models.
H(tau, g) = (24 tau sqrt(pi))^{-1} [int_0^{v1} F dv + E[g 1{v >= v1}]], the tail bounded by ddbounds.vtail_bound.
vquad returns the enclosure of int_0^{v1} F dv; H_point assembles H.  Cells whose plain-interval (order-0) enclosure is
already negligible are accepted at that order."""
import heapq, decimal, math
from fractions import Fraction as Fr
from decimal import Decimal as Dec
import ddcore as C
from ddcore import add, width, ZERO, ONE, q, mul, smul, sq, isqrt
import ddint as D
import ddbounds as B

EXC = (ZeroDivisionError, ValueError, AssertionError, decimal.Overflow, decimal.InvalidOperation)

def _eval(tau_iv, g_iv, kind, c, h, order):
    """enclosure of the integral over one cell: kind 'v' (v-cell centred at c, half-width h), 'yl'/'yr' (y-cell:
    v = 1 -/+ e^y, y centred at c)."""
    try:
        if kind == 'v':
            return D.H_integrand_point(tau_iv, g_iv, c, h, order).integrate()
        return D.H_integrand_point_log(tau_iv, g_iv, c, h, -1 if kind == 'yl' else 1, order).integrate()
    except EXC:
        return None

def sigmas(tau_iv, g_iv):
    st = smul(Dec(12), mul(isqrt(q(2)), tau_iv)); sc = mul(smul(Dec(576), isqrt(q(6))), mul(sq(tau_iv), g_iv))
    return st, sc

def v1_choice(st, sc, k=9):
    """v1 (an integer >= 8) with T1 = v1^2/6 - 1 >= k sigma_t and X1 = 2 v1^3 - 8 - 12 T1 >= k sigma_chi."""
    sigt = float(st[1]); sigc = float(sc[1])
    v1 = max(8.0, math.sqrt(6 * (1 + k * sigt)))
    while 2 * v1 ** 3 - 8 - 12 * (v1 * v1 / 6 - 1) < k * sigc:
        v1 *= 1.2
    return int(math.ceil(v1))

NARROW_SCALE = 0.1      # use the log substitution around v = 1 when sigma_chi/(12 sigma_t) < this
LOG_DELTA = 0.5         # half-width of the log region around v = 1

def initial_cells(st, sc, v1):
    """initial cells in [0, v1] as (kind, centre, half-width) with exact decimal geometry:
    - a bump region around v = 2 of half-width w = min(1.5, 4 (sigma_t + sigma_chi/36)) in 8 cells (the small-sigma case),
    - in the narrow regime (sigma_chi/(12 sigma_t) < NARROW_SCALE) a log region |v - 1| in [eps, LOG_DELTA], eps = 1e-7 sigma_chi,
      in y-cells of width 1 on both sides plus the core [1 - eps, 1 + eps] as one v-cell,
    - elsewhere v-cells of width ~ v_scale/3, v_scale = 2.06 sqrt(sigma_t) (the t < 0 branch has v ~ sqrt(3|t|)), at least 4 up to v1."""
    sigt = float(st[1]); sigc = float(sc[1])
    cells = []
    edges = [0.0]
    narrow = sigc / (12 * sigt) < NARROW_SCALE and sigc > 0 and sigt > 0.1      # v = 1 carries mass only if t >= 2/3 is reachable
    if narrow:
        eps = Dec('1e-7') * Dec(repr(sigc)); eps = Dec(repr(float(eps)))
        y_max = Dec(repr(math.log(LOG_DELTA))); y_min = Dec(repr(math.floor(math.log(float(eps)))))
        n = int((y_max - y_min) / Dec(1)) + 1
        hy = C.CU.divide(C.CU.subtract(y_max, y_min), Dec(2 * n))
        for k in range(n):
            yc = C.CD.add(y_min, C.CD.multiply(hy, Dec(2 * k + 1)))
            cells.append(('yl', yc, hy)); cells.append(('yr', yc, hy))
        cells.append(('v', Dec(1), eps))
        edges += [1 - LOG_DELTA, 1 + LOG_DELTA]
    w = min(1.5, max(0.01, 4 * (sigt + sigc / 36)))
    if w < 1.5 and 2 - w > (1 + LOG_DELTA if narrow else 0):
        edges += [max(0.0, 2 - w + 2 * w * k / 8) for k in range(9)]
    start = max(edges)
    v_scale = max(1.0, 2.06 * math.sqrt(sigt))
    n = max(4, int(math.ceil((v1 - start) / (v_scale / 3))))
    edges += [start + (v1 - start) * k / n for k in range(1, n + 1)]
    edges = sorted(set(e for e in edges if 0.0 <= e <= v1))
    for a, b in zip(edges[:-1], edges[1:]):
        if b - a < 1e-12: continue
        if narrow and a >= 1 - LOG_DELTA - 1e-12 and b <= 1 + LOG_DELTA + 1e-12: continue      # covered by the log region
        ad = Dec(repr(a)); bd = Dec(repr(b))
        vc = C.CD.divide(C.CD.add(ad, bd), Dec(2)); hv = C.CU.divide(C.CU.subtract(bd, ad), Dec(2))
        cells.append(('v', vc, hv))
    return cells

def vquad(tau_iv, g_iv, v1, order=8, rel_tol=Dec('1e-2'), abs_tol=Dec('1e-30'), max_cells=4000):
    """enclosure of int_0^{v1} F(tau, g, v) dv; returns (enclosure, ncells, total_width, fails)."""
    st, sc = sigmas(tau_iv, g_iv)
    init = initial_cells(st, sc, float(v1))
    cells = []   # [kind, c, h, enc, order_used]
    for (kind, c, h) in init:
        od = 0 if (kind == 'v' and h < Dec('1e-4')) else order
        cells.append([kind, c, h, _eval(tau_iv, g_iv, kind, c, h, od), od])
    def total():
        tot = (ZERO, ZERO); tw = ZERO
        for kind, c, h, enc, od in cells:
            if enc is None: tw = C.CU.add(tw, Dec('1e40')); continue
            tot = add(tot, enc); tw = C.CU.add(tw, width(enc))
        return tot, tw
    heap = [(-(width(c[3]) if c[3] is not None else Dec('1e40')), i) for i, c in enumerate(cells)]
    heapq.heapify(heap)
    ncells = len(cells)
    while True:
        tot, tw = total()
        mag = max(C.mag(tot), abs_tol)
        tol = C.CU.add(C.CU.multiply(rel_tol, mag), abs_tol)
        if tw <= tol or ncells >= max_cells:
            break
        cheap_tol = C.CD.divide(tol, Dec(20 * max(ncells, 1)))
        negw, i = heapq.heappop(heap)
        kind, c, h, enc, od = cells[i]
        h2 = C.CD.divide(h, Dec(2))
        children = []
        for cc in (C.CD.subtract(c, h2), C.CU.add(c, h2)):
            e0 = _eval(tau_iv, g_iv, kind, cc, h2, 0)
            if e0 is not None and width(e0) <= cheap_tol:
                children.append([kind, cc, h2, e0, 0])
            else:
                children.append([kind, cc, h2, _eval(tau_iv, g_iv, kind, cc, h2, order), order])
        cells[i] = children[0]; cells.append(children[1]); ncells += 1
        for j in (i, len(cells) - 1):
            e = cells[j][3]
            heapq.heappush(heap, (-(width(e) if e is not None else Dec('1e40')), j))
    tot, tw = total()
    fails = sum(1 for c in cells if c[3] is None)
    return tot, ncells, tw, fails

def H_point(tau_iv, g_iv, order=8, rel_tol=Dec('1e-2')):
    """enclosure of H(tau, g) = E[g(sigma_t Z1, sigma_chi Z2)] at a point given as (thin) intervals; also returns diagnostics."""
    st, sc = sigmas(tau_iv, g_iv)
    v1 = v1_choice(st, sc)
    enc, n, tw, fails = vquad(tau_iv, g_iv, v1, order, rel_tol)
    if fails: raise RuntimeError('v-quadrature failure')
    tail = B.vtail_bound(st, sc, Fr(v1))
    enc = (C.CD.subtract(enc[0], tail), C.CU.add(enc[1], tail))
    norm = C.recip(mul(smul(Dec(24), tau_iv), C.SQRTPI))
    return mul(enc, norm), dict(v1=v1, ncells=n, width=tw, tail=tail)
