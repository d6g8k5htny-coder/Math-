"""Rigorous one-dimensional v-quadrature of F(tau, g, v) at a point (tau, g): adaptive cells, one-variable Taylor models.
H(tau, g) = (24 tau sqrt(pi))^{-1} int_0^{v1} F dv + E[g 1{v >= v1}], the tail bounded by ddbounds.vtail_bound.
vquad returns the enclosure of int_0^{v1} F dv; H_point assembles H.  Cells whose plain-interval (order-0) enclosure is
already negligible are accepted at that order."""
import heapq, decimal, math
from fractions import Fraction as Fr
from decimal import Decimal as Dec
import ddcore as C
from ddcore import require, add, width, ZERO, ONE, q, mul, smul, sq, isqrt, iexp
import ddint as D
import ddbounds as B

EXC = (ZeroDivisionError, ValueError, AssertionError, decimal.Overflow, decimal.InvalidOperation)

def _eval(tau_iv, g_iv, kind, c, h, order):
    """enclosure of the integral over one cell: kind 'v' (v-cell centred at c, half-width h), 'yl'/'yr' (y-cell:
    v = 1 -/+ e^y, y centred at c), 'sv' (a sliver v-cell whose exact extent is uncertain: the enclosure is hulled with 0,
    plain interval evaluation)."""
    try:
        if kind == 'v':
            return D.H_integrand_point(tau_iv, g_iv, c, h, order).integrate()
        if kind == 'sv':
            e = D.H_integrand_point(tau_iv, g_iv, c, h, 0).integrate()
            return (min(e[0], ZERO), max(e[1], ZERO))
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

GRID = Dec('0.000001')     # every cell boundary is a multiple of this (short decimals: centres, half-widths and halvings are exact)

def _short(x, mode):
    """round a float/Decimal to the GRID, downwards ('d') or upwards ('u')."""
    d = Dec(repr(float(x))) if not isinstance(x, Dec) else x
    qd = d.quantize(GRID, rounding=decimal.ROUND_FLOOR if mode == 'd' else decimal.ROUND_CEILING)
    return qd

def _vcell(a, b, kind='v'):
    """(kind, centre, half-width) for the decimal interval [a, b]; exact when a, b are short decimals (asserted for 'v')."""
    vc = C.CD.divide(C.CD.add(a, b), Dec(2)); hv = C.CU.divide(C.CU.subtract(b, a), Dec(2))
    if kind == 'v':
        require(C.CD.subtract(vc, hv) == a and C.CU.add(vc, hv) == b, 'inexact v-cell geometry')
    return (kind, vc, hv)

def initial_cells(st, sc, v1):
    """initial cells in [0, v1] as (kind, centre, half-width) with exact decimal geometry (every v- and y-cell boundary is
    a multiple of GRID, so centres, half-widths and halvings are exact):
    - a bump region around v = 2 of half-width w = min(1.5, 4 (sigma_t + sigma_chi/36)) in 8 cells (the small-sigma case),
    - in the narrow regime (sigma_chi/(12 sigma_t) < NARROW_SCALE, sigma_t > 0.1) a log region around v = 1: y-cells of
      width ~1 on y in [y_min, y_max] for both sides (v = 1 -/+ e^y, covering |v - 1| in [eps, delta] exactly, eps = e^{y_min},
      delta = e^{y_max}), the core |v - 1| <= eps_in (a short decimal <= eps) as one v-cell, plain v-cells up to
      1 - delta_out and from 1 + delta_out (short decimals, delta_out >= delta), and four sliver cells covering the gaps
      [1 - delta_out, 1 - delta], [1 - eps, 1 - eps_in], [1 + eps_in, 1 + eps], [1 + delta, 1 + delta_out], whose exact
      extents are unknown (transcendental endpoints): their contribution is enclosed by hull(0, (sliver length) x range F),
    - elsewhere v-cells of width ~ v_scale/3, v_scale = 2.06 sqrt(sigma_t) (the t < 0 branch has v ~ sqrt(3|t|)),
      at least 4 up to v1."""
    sigt = float(st[1]); sigc = float(sc[1])
    cells = []
    v1d = Dec(int(v1)); require(v1d == v1)
    narrow = sigc / (12 * sigt) < NARROW_SCALE and sigc > 0 and sigt > 0.1      # v = 1 carries mass only if t >= 2/3 is reachable
    segments = []            # decimal [a, b] intervals to be covered by plain v-cells
    v_scale = max(1.0, 2.06 * math.sqrt(sigt))
    if narrow:
        y_min = Dec(math.floor(math.log(1e-7 * sigc)))
        n = int(math.ceil(float(Dec(repr(math.log(LOG_DELTA))) - y_min)))
        hy = _short((math.log(LOG_DELTA) - float(y_min)) / (2 * n), 'u')
        y_max = C.CU.add(y_min, C.CU.multiply(hy, Dec(2 * n)))                 # exact (short decimals)
        require(C.CD.add(y_min, C.CD.multiply(hy, Dec(2 * n))) == y_max)
        delta = iexp((y_max, y_max)); eps = iexp((y_min, y_min))
        for k in range(n):
            yc = C.CD.add(y_min, C.CD.multiply(hy, Dec(2 * k + 1)))
            require(C.CD.subtract(yc, hy) == C.CD.add(y_min, C.CD.multiply(hy, Dec(2 * k))))
            cells.append(('yl', yc, hy)); cells.append(('yr', yc, hy))
        one = Dec(1)
        delta_out = _short(delta[1], 'u'); eps_in = _short(eps[0], 'd')
        require(delta_out >= delta[1] and 0 <= eps_in <= eps[0])
        cells.append(('v', one, eps_in))                                      # the core (certain part)
        for (a, b) in ((C.CD.subtract(one, delta_out), C.CU.subtract(one, delta[0])), (C.CD.subtract(one, eps[1]), C.CU.subtract(one, eps_in)),
                       (C.CD.add(one, eps_in), C.CU.add(one, eps[1])), (C.CD.add(one, delta[0]), C.CU.add(one, delta_out))):
            cells.append(_vcell(a, b, 'sv'))
        segments.append((Dec(0), C.CD.subtract(one, delta_out))); segments.append((C.CU.add(one, delta_out), v1d))
    else:
        segments.append((Dec(0), v1d))
    w = min(1.5, max(0.01, 4 * (sigt + sigc / 36)))
    bump = (w < 1.5)
    for (a, b) in segments:
        edges = [float(a)]
        if bump and float(a) <= 2 - w and 2 + w <= float(b):
            edges += [2 - w + 2 * w * k / 8 for k in range(9)]
        start = max(edges)
        m = max(4 if (a == 0 and not narrow) else 1, int(math.ceil((float(b) - start) / (v_scale / 3))))
        edges += [start + (float(b) - start) * k / m for k in range(1, m + 1)]
        edges = sorted(set(edges))
        ded = [a] + [_short(e, 'd') for e in edges[1:-1]] + [b]
        ded = [x for i, x in enumerate(ded) if i == 0 or x > ded[i - 1]]          # strictly increasing (interior edges clamped by the sort)
        ded = [x for x in ded if a <= x <= b]
        if ded[-1] != b: ded.append(b)
        for x, y in zip(ded[:-1], ded[1:]):
            if y > x: cells.append(_vcell(x, y))
    return cells

def vquad(tau_iv, g_iv, v1, order=8, rel_tol=Dec('1e-2'), abs_tol=Dec('1e-30'), max_cells=4000):
    """enclosure of int_0^{v1} F(tau, g, v) dv; returns (enclosure, ncells, total_width, fails)."""
    st, sc = sigmas(tau_iv, g_iv)
    init = initial_cells(st, sc, float(v1))
    cells = []   # [kind, c, h, enc, order_used]
    for (kind, c, h) in init:
        od = 0 if (kind in ('v', 'sv') and h < Dec('1e-4')) else order
        cells.append([kind, c, h, _eval(tau_iv, g_iv, kind, c, h, od), od])
    def total():
        tot = (ZERO, ZERO); tw = ZERO
        for kind, c, h, enc, od in cells:
            if enc is None: tw = C.CU.add(tw, Dec('1e40')); continue
            tot = add(tot, enc); tw = C.CU.add(tw, width(enc))
        return tot, tw
    heap = [(-(width(c[3]) if c[3] is not None else Dec('1e40')), i) for i, c in enumerate(cells) if c[0] != 'sv']
    heapq.heapify(heap)
    ncells = len(cells)
    while True:
        tot, tw = total()
        mag = max(C.mag(tot), abs_tol)
        tol = C.CU.add(C.CU.multiply(rel_tol, mag), abs_tol)
        if tw <= tol or ncells >= max_cells or not heap:
            break
        cheap_tol = C.CD.divide(tol, Dec(20 * max(ncells, 1)))
        negw, i = heapq.heappop(heap)
        kind, c, h, enc, od = cells[i]
        h2 = C.CD.divide(h, Dec(2))
        require(C.CU.multiply(h2, Dec(2)) == h and C.CD.subtract(c, h2) == C.CU.subtract(c, h2), 'inexact halving')
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

def H_point(tau_iv, g_iv, order=8, rel_tol=Dec('5e-3'), v1_override=None):
    """enclosure of H(tau, g) = E[g(sigma_t Z1, sigma_chi Z2)] at a point given as (thin) intervals; also returns diagnostics.
    v1_override (an integer >= 3) replaces the automatic v1 (used by the controls: any v1 gives a valid enclosure)."""
    st, sc = sigmas(tau_iv, g_iv)
    v1 = v1_choice(st, sc) if v1_override is None else int(v1_override)
    enc, n, tw, fails = vquad(tau_iv, g_iv, v1, order, rel_tol)
    if fails: raise RuntimeError('v-quadrature failure')
    tail = B.vtail_bound(st, sc, Fr(v1))                       # a bound on |E[g 1{v >= v1}]|, in the units of H
    norm = C.recip(mul(smul(Dec(24), tau_iv), C.SQRTPI))
    H = mul(enc, norm)                                        # (24 tau sqrt pi)^{-1} int_0^{v1} F dv
    H = (C.CD.subtract(H[0], tail), C.CU.add(H[1], tail))
    return H, dict(v1=v1, ncells=n, width=tw, tail=tail)
