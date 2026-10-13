"""Adaptive Taylor-model cubature of the D-integrand over a box in (u, w, v)."""
import heapq, time, sys, decimal
from decimal import Decimal as Dec
import ddcore as C
from ddcore import add, mul, width, mag, ZERO, ONE
import ddint as D

class Cell:
    __slots__ = ('c', 'h', 'enc', 'score', 'fail')
    def __init__(self, c, h):
        self.c = c; self.h = h; self.enc = None; self.score = None; self.fail = False

def evaluate(cell, order):
    try:
        enc, T = D.cell_integral(cell.c[0], cell.h[0], cell.c[1], cell.h[1], cell.c[2], cell.h[2], order)
    except (ZeroDivisionError, ValueError, AssertionError, decimal.Overflow, decimal.InvalidOperation) as e:
        cell.fail = True; cell.enc = None; cell.score = [ONE, ONE, ONE]
        return
    cell.enc = enc
    # per-axis sensitivity: total magnitude of polynomial terms involving each variable (times the box range)
    S = T.S
    score = [ZERO, ZERO, ZERO]
    for m, cm in T.c.items():
        if m == S.zero_m: continue
        contrib = C.CU.multiply(mag(cm), S.rng[m][1])
        for i in range(3):
            if m[i] > 0: score[i] = C.CU.add(score[i], contrib)
    # the remainder is attributed to every axis equally
    r = mag(T.r)
    cell.score = [C.CU.add(sc, r) for sc in score]

def split(cell):
    i = max(range(3), key=lambda k: (cell.score[k], -k))
    h = list(cell.h); h[i] = C.CD.divide(h[i], Dec(2))
    half = h[i]
    c1 = list(cell.c); c1[i] = C.CD.subtract(cell.c[i], half)
    c2 = list(cell.c); c2[i] = C.CU.add(cell.c[i], half)
    return Cell(c1, h), Cell(c2, h)

def integrate_box(u_lo, u_hi, w_lo, w_hi, v_lo, v_hi, n0=(1, 2, 2), order=3, tol=Dec('1e-5'), max_cells=20000, log=None):
    """returns (enclosure, ncells, total_width)."""
    cells = []
    def grid(lo, hi, n):
        lo = Dec(lo); hi = Dec(hi); n = int(n)
        h = C.CD.divide(C.CD.subtract(hi, lo), Dec(2 * n))
        return [(C.CD.add(lo, C.CD.multiply(h, Dec(2 * k + 1))), h) for k in range(n)]
    for (uc, hu) in grid(u_lo, u_hi, n0[0]):
        for (wc, hw) in grid(w_lo, w_hi, n0[1]):
            for (vc, hv) in grid(v_lo, v_hi, n0[2]):
                cells.append(Cell([uc, wc, vc], [hu, hw, hv]))
    heap = []; done = []
    counter = 0
    def push(cell):
        nonlocal counter
        evaluate(cell, order)
        if cell.fail:
            wdt = Dec('1e30')
        else:
            wdt = width(cell.enc)
        counter += 1
        heapq.heappush(heap, (-wdt, counter, cell))
    for cell in cells: push(cell)
    ncells = len(cells); t0 = time.time()
    while True:
        total_w = sum((-item[0] for item in heap), ZERO)
        if total_w <= tol or ncells >= max_cells:
            break
        negw, _, cell = heapq.heappop(heap)
        a, b = split(cell)
        push(a); push(b); ncells += 1
        if log and ncells % 200 == 0:
            print('  cells %d  total width %.3e  (%.0fs)' % (ncells, float(total_w), time.time() - t0), file=log); log.flush()
    tot = (ZERO, ZERO); fails = 0
    for negw, _, cell in heap:
        if cell.fail: fails += 1; continue
        tot = add(tot, cell.enc)
    return tot, ncells, total_w, fails
