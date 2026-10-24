"""The Gauss region of the certified enclosure of D:
  D_G = int_{u_lo}^{u_hi} du int_{w_lo(u)}^{w_hi(u)} dw rho(u, w) H(u, w)   (u = ln tau, w = ln g),
by a tensor n-point Gauss-Legendre rule on adaptively refined cells, each cell's remainder bounded by ddbounds.cell_remainder
(derivative bounds of rho H), each node value rho(node) H(node) enclosed with ddvq.H_point (rigorous v-quadrature + tail).
Rows: the u-range is cut into rows of equal width; each row has its own w-range [w_lo, w_hi]; the parts of the row
outside the w-range are bounded (omega_tails).  All cell geometry is exact decimal (dyadic refinement of short decimals), so
the cells tile the rows exactly; the refinement order is deterministic.

Usage: python3 ddgauss.py build <out.json> [target] [u_lo] [u_hi]   -> cell list with remainder bounds
       python3 ddgauss.py eval  <cells.json> <out.json> [nproc]      -> node values (checkpointed), assembly
"""
import sys, os, json, math, heapq, time
from fractions import Fraction as Fr
from decimal import Decimal as Dec
import ddcore as C
from ddcore import require, q, add, sub, mul, div, smul, sq, ipow, iexp, iln, isqrt, ZERO, ONE, TWO
import ddbounds as B
import ddvq as VQ

NGAUSS = 4
TAYLOR = (11, Fr(3, 10), Fr(1))
ROW_WIDTH = Dec('0.4')          # 2 hu of the initial rows
NW0 = 8                          # initial cells per row in w
G_LO_FRAC = 0.002                # g_lo = G_LO_FRAC * g_hi (the lower omega tail is bounded; small g means a narrow chi-Gaussian and a slow v-quadrature)
_TP = None
def taylor_part():
    global _TP
    if _TP is None: _TP = B.TaylorPart(*TAYLOR)
    return _TP

HALF = Dec('0.5')
def half(x): return C.CD.multiply(x, HALF)      # exact for short decimals

# ---------------------------------------------------------------- Gauss-Legendre nodes and weights as intervals
def gauss_nodes(n):
    if n == 4:
        s30 = isqrt(q(30))
        x1 = isqrt(div(sub(q(15), smul(TWO, s30)), q(35))); x2 = isqrt(div(add(q(15), smul(TWO, s30)), q(35)))
        w1 = div(add(q(18), s30), q(36)); w2 = div(sub(q(18), s30), q(36))
        return [(C.neg(x2), w2), (C.neg(x1), w1), (x1, w1), (x2, w2)]
    if n == 3:
        x = isqrt(q(Fr(3, 5)))
        return [(C.neg(x), q(Fr(5, 9))), ((ZERO, ZERO), q(Fr(8, 9))), (x, q(Fr(5, 9)))]
    raise ValueError(n)

# ---------------------------------------------------------------- rows and w-ranges (short decimals)
def g_hi_of(tau_lo):
    """g_hi for a row whose smallest tau is tau_lo: e^{-12 tau^2 g^4} <= e^{-60} beyond (60/(12 tau_lo^2))^{1/4}; plus the
    e^{-g^2/4} scale when tau is small (float heuristic; the tails are bounded rigorously whatever the choice)."""
    base = (60.0 / (12.0 * tau_lo * tau_lo)) ** 0.25
    return min(9.0, base + min(0.5, 3.0 / tau_lo))

def rows_for(u_lo, n_rows):
    rows = []
    hu = half(ROW_WIDTH)
    for i in range(n_rows):
        uc = C.CD.add(u_lo, C.CD.multiply(ROW_WIDTH, Dec(i)) ) ; uc = C.CD.add(uc, hu)
        tau_lo = math.exp(float(uc - hu))
        g_hi = g_hi_of(tau_lo); g_lo = G_LO_FRAC * g_hi
        w_hi = Dec(math.ceil(math.log(g_hi) * 1000)).scaleb(-3)          # short decimals
        hw0 = Dec(math.ceil((math.log(g_hi) - math.log(g_lo)) / (2 * NW0) * 1000)).scaleb(-3)
        w_lo = C.CD.subtract(w_hi, C.CD.multiply(hw0, Dec(2 * NW0)))
        rows.append(dict(uc=uc, hu=hu, w_lo=w_lo, w_hi=w_hi, hw0=hw0))
    return rows

def cell_bound(uc, hu, wc, hw):
    E, Eu, Ew = B.cell_remainder(uc, hu, wc, hw, NGAUSS, taylor_part())
    return E, Eu, Ew

def build(target, u_lo, u_hi, max_cells=30000, log=None):
    """adaptive cell list: split the cell with the largest remainder bound (in the direction of its larger part) until the
    total bound <= target.  Returns (cells, rows, total) with cells = [(uc, hu, wc, hw, E, Eu, Ew)] (Decimals) in a
    deterministic order."""
    n_rows = int(math.ceil(float((u_hi - u_lo) / ROW_WIDTH)))
    rows = rows_for(u_lo, n_rows)
    heap = []; cells = {}; nid = 0
    t0 = time.time()
    for r in rows:
        for j in range(NW0):
            hw = r['hw0']; wc = C.CD.add(r['w_lo'], C.CD.multiply(hw, Dec(2 * j + 1)))
            E, Eu, Ew = cell_bound(r['uc'], r['hu'], wc, hw)
            cells[nid] = (r['uc'], r['hu'], wc, hw, E, Eu, Ew)
            heapq.heappush(heap, (-E, nid)); nid += 1
    def total_of():
        t = ZERO
        for c in cells.values(): t = C.CU.add(t, c[4])
        return t
    total = total_of()
    while total > target and len(cells) < max_cells:
        negE, i = heapq.heappop(heap)
        uc, hu, wc, hw, E, Eu, Ew = cells.pop(i)
        if Eu >= Ew:
            h2 = half(hu); kids = [(C.CD.subtract(uc, h2), h2, wc, hw), (C.CD.add(uc, h2), h2, wc, hw)]
        else:
            h2 = half(hw); kids = [(uc, hu, C.CD.subtract(wc, h2), h2), (uc, hu, C.CD.add(wc, h2), h2)]
        for (a, b, c_, d) in kids:
            E2, Eu2, Ew2 = cell_bound(a, b, c_, d)
            cells[nid] = (a, b, c_, d, E2, Eu2, Ew2); heapq.heappush(heap, (-E2, nid)); nid += 1
        total = C.CU.add(C.CU.add(C.CU.add(total, -E), cells[nid - 2][4]), cells[nid - 1][4])
        if log and len(cells) % 200 == 0:
            print('  cells %d total bound %.4e [%.0fs]' % (len(cells), float(total), time.time() - t0), file=log, flush=True)
    out = [cells[k] for k in sorted(cells)]
    return out, rows, total_of()

def omega_tails(rows):
    """upper bound of int_row du [int_{w > w_hi} + int_{w < w_lo}] rho |H| dw, summed over rows:
       w > w_hi: term-wise with E[g~] = sum c m_a m_b sigma_t^a sigma_chi^b and
                 int_{g_hi}^inf g^{8/3+b} e^{-12 tau^2 g^4 - g^2/4} dg <= min( e^{-g_hi^2/4} Gamma(p/4, 12 tau^2 g_hi^4) / (4 (12 tau^2)^{p/4}),
                                                                       (1/2) 4^{p/2} Gamma(p/2, g_hi^2/4) ),  p = b + 11/3;
       w < w_lo: sup|H| (ddbounds.H_sup over sigma_chi in [0, sigma_chi(g_lo)]) times int_0^{g_lo} g^{8/3} dg = g_lo^{11/3}/(11/3);
       the u-integral of the row by sup over the row's tau-interval times the row width (2 hu)."""
    tot = ZERO
    K = smul(Dec(576), isqrt(q(6)))
    for r in rows:
        u_iv = (C.CD.subtract(r['uc'], r['hu']), C.CU.add(r['uc'], r['hu'])); tau = iexp(u_iv)
        st = smul(Dec(12), mul(isqrt(q(2)), tau))
        g_hi = iexp(q(r['w_hi'])); g_lo = iexp(q(r['w_lo']))
        pre = mul(B.RHO_C0, iexp(smul(Dec(-5), div(u_iv, q(3)))))     # c0 tau^{-5/3}
        width_u = C.CU.multiply(TWO, r['hu'])
        # upper tail
        x = mul(smul(Dec(12), sq(tau)), ipow(g_hi, 4))
        eg = iexp(C.neg(div(sq(g_hi), q(4))))
        up = ZERO
        for (c, a, b) in B.SHARPER:
            p = b + Fr(11, 3)
            G = B.upper_incomplete_gamma_bound(p / 4, x)
            den = smul(Dec(4), B.sigma_pow(smul(Dec(12), sq(tau)), p / 4))
            gint = C.CU.multiply(C.CU.multiply(eg[1], G[1]), C.recip(den)[1])
            # alternative (drop e^{-12 tau^2 g^4} <= 1): int_{g_hi}^inf g^{p-1} e^{-g^2/4} dg = (1/2) 4^{p/2} Gamma(p/2, g_hi^2/4)
            G2 = B.upper_incomplete_gamma_bound(p / 2, div(sq(g_hi), q(4)))
            gint2 = C.CU.multiply(C.CU.multiply(HALF, B.sigma_pow(q(4), p / 2)[1]), G2[1])
            gint = min(gint, gint2)
            kt = B.sigma_pow(mul(K, sq(tau)), b)[1]                      # (K tau^2)^b; the g^b is inside the g-integral
            term = C.CU.multiply(C.CU.multiply(c[1], C.CU.multiply(B.absmom(a)[1], B.absmom(b)[1])), C.CU.multiply(B.sigma_pow(st, a)[1], C.CU.multiply(kt, gint)))
            up = C.CU.add(up, term)
        up = C.CU.multiply(C.CU.multiply(pre[1], up), width_u)
        # lower tail
        sc_lo = mul(K, mul(sq(tau), g_lo))
        Hs = B.H_sup(st, (ZERO, sc_lo[1]), taylor_part())
        gint = C.CU.multiply(B.sigma_pow(g_lo, Fr(11, 3))[1], C.recip(q(Fr(11, 3)))[1])
        low = C.CU.multiply(C.CU.multiply(C.CU.multiply(pre[1], Hs), gint), width_u)
        tot = C.CU.add(tot, C.CU.add(up, low))
    return tot

# ---------------------------------------------------------------- node evaluation
def cell_nodes(uc, hu, wc, hw):
    """the n x n node coordinates (thin intervals) and weight products (intervals) of a cell, in a fixed order."""
    GN = gauss_nodes(NGAUSS)
    out = []
    for (xi, wi) in GN:
        for (xj, wj) in GN:
            u_iv = add(q(uc), smul(hu, xi)); w_iv = add(q(wc), smul(hw, xj))
            out.append((u_iv, w_iv, mul(wi, wj)))
    return out

def eval_node(args):
    """rho(node) H(node) enclosure for a node given as thin intervals (u_iv, w_iv); returns (lo, hi, v1, ncells) as
    strings/ints, or ('FAIL', message, 0, 0) if the v-quadrature did not succeed (the assembly refuses such a node)."""
    u_iv, w_iv = args
    try:
        rho, X, Y = B.rho_cell(u_iv, w_iv)
        tau = iexp(u_iv); g = iexp(w_iv)
        H, d = VQ.H_point(tau, g)
        val = mul(rho, H)
        return (str(val[0]), str(val[1]), d['v1'], d['ncells'], str(u_iv[0]), str(w_iv[0]))
    except Exception as ex:
        return ('FAIL', '%s: %s' % (type(ex).__name__, ex), 0, 0, str(u_iv[0]), str(w_iv[0]))

def eval_cells(cells, out_path, nproc=2, log=None, shard=(0, 1)):
    """evaluate the node values of the cells with index % shard[1] == shard[0], with multiprocessing; checkpoint to
    out_path (JSON: cell index -> list of n*n node results)."""
    import multiprocessing as mp
    done = {}
    if os.path.exists(out_path):
        done = {int(k): v for k, v in json.load(open(out_path)).items()}
    todo = [i for i in range(len(cells)) if i not in done and i % shard[1] == shard[0]]
    t0 = time.time()
    tasks = []
    for i in todo:
        uc, hu, wc, hw = cells[i][:4]
        for (u_iv, w_iv, wij) in cell_nodes(uc, hu, wc, hw):
            tasks.append((i, (u_iv, w_iv)))
    results = {}
    with mp.Pool(nproc) as pool:
        it = pool.imap(eval_node, [t[1] for t in tasks], chunksize=1)
        for k, res in enumerate(it):
            i = tasks[k][0]
            results.setdefault(i, []).append(res)
            if len(results[i]) == NGAUSS * NGAUSS:
                done[i] = results.pop(i)
            if (k + 1) % 50 == 0 or k + 1 == len(tasks):
                json.dump({str(a): b for a, b in done.items()}, open(out_path + '.tmp', 'w')); os.replace(out_path + '.tmp', out_path)
                if log: print('  nodes %d/%d, cells done %d [%.0fs]' % (k + 1, len(tasks), len(done), time.time() - t0), file=log, flush=True)
    return done

def assemble(cells, done, remainders=None):
    """sum over cells of hu hw sum_ij w_i w_j rho H(node_ij), plus/minus the remainder bounds (the stored E of each cell, or
    `remainders[i]` when given, e.g. recomputed).  Every node record must carry the node coordinates of the cell's k-th node
    (checked) and a valid enclosure lo <= hi."""
    tot = (ZERO, ZERO); rem = ZERO
    GN = gauss_nodes(NGAUSS)
    wprod = [mul(wi, wj) for (xi, wi) in GN for (xj, wj) in GN]
    for i, c in enumerate(cells):
        uc, hu, wc, hw, E = c[0], c[1], c[2], c[3], c[4]
        vals = done[i]
        require(len(vals) == NGAUSS * NGAUSS and all(v[0] != 'FAIL' for v in vals), 'cell %d: incomplete or failed node values' % i)
        nodes = cell_nodes(uc, hu, wc, hw)
        s = (ZERO, ZERO)
        for k, v in enumerate(vals):
            lo, hi = Dec(v[0]), Dec(v[1])
            require(lo <= hi and lo.is_finite() and hi.is_finite(), 'cell %d node %d: invalid enclosure' % (i, k))
            if len(v) >= 6:
                require(Dec(v[4]) == nodes[k][0][0] and Dec(v[5]) == nodes[k][1][0], 'cell %d node %d: coordinates differ' % (i, k))
            s = add(s, mul(wprod[k], (lo, hi)))
        s = mul(s, mul(q(hu), q(hw)))
        tot = add(tot, s); rem = C.CU.add(rem, Dec(E) if remainders is None else remainders[i])
    return (C.CD.subtract(tot[0], rem), C.CU.add(tot[1], rem)), tot, rem

def load_cells(path):
    spec = json.load(open(path))
    cells = [tuple(Dec(x) for x in c) for c in spec['cells']]
    return spec, cells

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'build':
        out = sys.argv[2]; target = Dec(sys.argv[3]) if len(sys.argv) > 3 else Dec('7e-4')
        u_lo = Dec(sys.argv[4]) if len(sys.argv) > 4 else Dec('-6.2')      # tau_s = e^{-6.2} = 0.002029
        u_hi = Dec(sys.argv[5]) if len(sys.argv) > 5 else Dec('18.6')      # tau_1 = e^{18.6} = 1.2e8
        t0 = time.time()
        cells, rows, total = build(target, u_lo, u_hi, log=sys.stdout)
        print('cells %d, total remainder bound %s [%.0fs]' % (len(cells), total, time.time() - t0))
        ot = omega_tails(rows)
        print('omega tails bound %s' % ot)
        json.dump(dict(target=str(target), u_lo=str(u_lo), u_hi=str(u_hi), row_width=str(ROW_WIDTH), nw0=NW0, ngauss=NGAUSS,
                       taylor=[TAYLOR[0], str(TAYLOR[1]), str(TAYLOR[2])],
                       rows=[{k: str(v) for k, v in r.items()} for r in rows], omega_tails=str(ot), total_remainder=str(total),
                       cells=[tuple(str(x) for x in c) for c in cells]), open(out, 'w'))
        import collections
        dec = collections.Counter(int(math.floor(float(c[0]) / math.log(10))) for c in cells)
        print('cells per decade of tau:', sorted(dec.items()))
    elif mode == 'eval':
        spec, cells = load_cells(sys.argv[2]); out = sys.argv[3]; nproc = int(sys.argv[4]) if len(sys.argv) > 4 else 2
        shard = tuple(int(x) for x in sys.argv[5].split('/')) if len(sys.argv) > 5 else (0, 1)
        done = eval_cells(cells, out, nproc, log=sys.stdout, shard=shard)
        if shard == (0, 1):
            enc, tot, rem = assemble(cells, done)
            print('Gauss region: sum = [%s, %s], remainder %s -> D_G in [%s, %s]' % (tot[0], tot[1], rem, enc[0], enc[1]))
        else:
            print('shard %d/%d: %d cells done' % (shard[0], shard[1], len(done)))
