"""Gap control for the note DD certificate: the four sliver v-cells of a narrow-regime node are formed by ddvq._vcell from
their decimal endpoints [a, b] with the centre rounded down and the half-width rounded up, so the cell [c - h, c + h]
always covers a on the left but may stop short of b on the right by at most a few units in the 30th digit.  The
v-quadrature therefore omits, at such a node, the integral of F over the gaps (c + h, b_true], where b_true <= b is the
true right end of the sliver (b itself for the slivers whose right end is a short decimal; an enclosure end otherwise).

This script encloses the omitted contribution rigorously, in the certificate's own arithmetic, for every node of the
certificate: for each gap G = [c + h, b] (a superset of the true gap) it evaluates F on a decimal cell that provably
contains G (checked with exact rationals), encloses int_G F dv in hull(0, |cell| x range F), applies the normalization
(24 tau sqrt pi)^{-1}, the density rho(node) and the node's Gauss weight h_u h_w w_i w_j, and sums over all nodes.  The
result is an interval Delta = [Delta_lo, Delta_hi] with Delta_lo <= 0 <= Delta_hi such that the true D lies in
[D_lo + Delta_lo, D_hi + Delta_hi], where [D_lo, D_hi] is the assembled enclosure.  Standard library only.

Usage: python3 -B -S dd_gapcheck.py cells_full.json [nproc]
"""
import sys, json, math
from decimal import Decimal as Dec
from fractions import Fraction as Fr
import ddcore as C
from ddcore import iexp, mul, add, smul, q, require, ZERO
import ddbounds as B
import ddint as D
import ddvq as V
import ddgauss as G


def sliver_gaps(st, sc):
    """replicates ddvq.initial_cells' sliver construction (and checks it against ddvq.initial_cells); returns the list of
    gaps (gap_lo = c + h as an exact Fraction, gap_hi = b as a Decimal), one per sliver whose cell stops short of b, and
    whether the node is in the narrow regime."""
    sigt = float(st[1]); sigc = float(sc[1])
    narrow = sigc / (12 * sigt) < V.NARROW_SCALE and sigc > 0 and sigt > 0.1
    if not narrow:
        return [], False
    y_min = Dec(math.floor(math.log(1e-7 * sigc)))
    n = int(math.ceil(float(Dec(repr(math.log(V.LOG_DELTA))) - y_min)))
    hy = V._short((math.log(V.LOG_DELTA) - float(y_min)) / (2 * n), 'u')
    y_max = C.CU.add(y_min, C.CU.multiply(hy, Dec(2 * n)))
    require(C.CD.add(y_min, C.CD.multiply(hy, Dec(2 * n))) == y_max)
    delta = iexp((y_max, y_max)); eps = iexp((y_min, y_min))
    one = Dec(1)
    delta_out = V._short(delta[1], 'u'); eps_in = V._short(eps[0], 'd')
    require(delta_out >= delta[1] and 0 <= eps_in <= eps[0])
    gaps = []; mine = []
    for (a, b) in ((C.CD.subtract(one, delta_out), C.CU.subtract(one, delta[0])), (C.CD.subtract(one, eps[1]), C.CU.subtract(one, eps_in)),
                   (C.CD.add(one, eps_in), C.CU.add(one, eps[1])), (C.CD.add(one, delta[0]), C.CU.add(one, delta_out))):
        kind, c, h = V._vcell(a, b, 'sv')
        mine.append((c, h))
        require(Fr(c) - Fr(h) <= Fr(a), 'sliver cell does not cover its left end')     # never fails (both roundings push left)
        hi = Fr(c) + Fr(h)
        if hi < Fr(b):
            gaps.append((hi, b))
    # the replication above must agree with the certificate's own cell construction at this node
    actual = [(c, h) for (kind, c, h) in V.initial_cells(st, sc, V.v1_choice(st, sc)) if kind == 'sv']
    require(actual == mine, 'sliver cells differ from ddvq.initial_cells')
    return gaps, True


def covering_cell(lo_fr, b):
    """a decimal (centre, half-width) whose cell provably contains [lo_fr, b] (lo_fr a Fraction, b a Decimal)."""
    lo = C.CD.divide(C.CD.create_decimal(lo_fr.numerator), C.CD.create_decimal(lo_fr.denominator))   # rounded down: lo <= lo_fr
    h = C.CU.divide(C.CU.subtract(b, lo), Dec(2))
    c = C.CD.divide(C.CD.add(lo, b), Dec(2))
    bump = Dec('1e-40')
    for _ in range(200):
        if Fr(c) - Fr(h) <= lo_fr and Fr(c) + Fr(h) >= Fr(b):
            return c, h
        h = C.CU.add(h, bump); bump = C.CU.multiply(bump, Dec(10))
    raise AssertionError('no covering cell')


def node_gap_contribution(u_iv, w_iv):
    """hull(0, sum over gaps of |cell| x range F) x (24 tau sqrt pi)^{-1} x rho(node): an enclosure of the omitted part of
    rho H at the node (zero when the node has no gap)."""
    tau = iexp(u_iv); g = iexp(w_iv)
    st, sc = V.sigmas(tau, g)
    gaps, narrow = sliver_gaps(st, sc)
    if not gaps:
        return (ZERO, ZERO), 0, ZERO, narrow
    tot = (ZERO, ZERO); glen = ZERO
    for (lo_fr, b) in gaps:
        c, h = covering_cell(lo_fr, b)
        e = D.H_integrand_point(tau, g, c, h, 0).integrate()        # 2h x range(F on the cell)
        tot = add(tot, (min(e[0], ZERO), max(e[1], ZERO)))
        glen = C.CU.add(glen, C.CU.multiply(h, Dec(2)))
    norm = C.recip(mul(smul(Dec(24), tau), C.SQRTPI))
    rho, X, Y = B.rho_cell(u_iv, w_iv)
    val = mul(mul(tot, norm), rho)
    return (min(val[0], ZERO), max(val[1], ZERO)), len(gaps), glen, narrow


def work(args):
    i, uc, hu, wc, hw = args
    out = []
    for (u_iv, w_iv, wij) in G.cell_nodes(uc, hu, wc, hw):
        corr, ng, glen, narrow = node_gap_contribution(u_iv, w_iv)
        out.append((str(corr[0]), str(corr[1]), ng, str(glen), str(wij[0]), str(wij[1]), narrow))
    return i, out


def main(cells_path, nproc=2):
    import multiprocessing as mp
    spec, cells = G.load_cells(cells_path)
    tasks = [(i, c[0], c[1], c[2], c[3]) for i, c in enumerate(cells)]
    results = {}
    with mp.Pool(nproc) as pool:
        for k, (i, out) in enumerate(pool.imap_unordered(work, tasks, chunksize=4)):
            results[i] = out
            if (k + 1) % 400 == 0:
                print('  %d/%d cells' % (k + 1, len(cells)), flush=True)
    total = (ZERO, ZERO); n_gap_nodes = 0; n_gaps = 0; max_glen = ZERO; max_node = ZERO
    for i, c in enumerate(cells):
        uc, hu, wc, hw = c[0], c[1], c[2], c[3]
        s = (ZERO, ZERO)
        for (lo, hi, ng, glen, wlo, whi, narrow) in results[i]:
            corr = (Dec(lo), Dec(hi)); wij = (Dec(wlo), Dec(whi))
            if ng:
                n_gap_nodes += 1; n_gaps += ng
                max_glen = max(max_glen, Dec(glen)); max_node = max(max_node, abs(corr[0]), abs(corr[1]))
            s = add(s, mul(wij, corr))
        s = mul(s, mul(q(hu), q(hw)))
        total = add(total, s)
    n_narrow = sum(1 for i in results for o in results[i] if o[6])
    print('narrow-regime nodes: %d of %d; nodes with a sliver gap: %d (%d gaps; every sliver cell covers its left end and the replicated '
          'sliver geometry equals ddvq.initial_cells at every narrow node); largest total gap length at a node: %s; largest |rho H| '
          'omission at a node: %s' % (n_narrow, 16 * len(cells), n_gap_nodes, n_gaps, max_glen, max_node))
    print('Delta (the omitted contribution to D lies in this interval): [%s, %s]' % (total[0], total[1]))
    return total


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 2)
