"""Assembly of the certified enclosure of D and the corollary.
   D = D_S + D_G + (omega tails) + (tau tail), with
   D_S from ddS.region_S (closed form), D_G from ddgauss (cells + node values + remainder bounds), the omega tails from
   ddgauss.omega_tails, the tau tail from ddS.tau_tail.
Usage: python3 dd_exact.py <cells.json> <nodes.json>"""
import sys, json, math
from fractions import Fraction as Fr
from decimal import Decimal as Dec
import ddcore as C
from ddcore import require, q, add, sub, mul, div, smul, ZERO, ONE
import ddbounds as B
import ddgauss as G
import ddS as S

def corollary(D):
    """q = J/30 - I~_quad - D and the elder coefficient (c3 - R_{2/3})(L) = q S_d - allowances, note CJ's constants."""
    J = (Dec('4.1977819534'), Dec('4.1977820097'))
    mIq = (Dec('0.6104056'), Dec('0.6104057'))            # -I~_quad
    qv = add(add(div(J, q(30)), mIq), C.neg(D))
    PI = C.PI
    S2 = div(smul(Dec(25), C.isqrt(q(3))), smul(Dec(48), C.sq(PI)))
    S3 = div(smul(Dec(125), C.isqrt(q(30))), smul(Dec(192), C.ipow(PI, 3)))
    out = {'q': qv}
    for d, Sd, etas in ((2, S2, {'L>=10': (Dec('5.88e-9'), Dec('7.81e-6')), 'L>=24': (Dec('4.88e-110'), Dec('6.48e-107'))}),
                        (3, S3, {'L>=10': (Dec('1.97e-7'), Dec('4.97e-4')), 'L>=24': (Dec('1.64e-108'), Dec('4.13e-105'))})):
        for key, (eta_c, eta_R) in etas.items():
            eta = C.CU.add(eta_c, eta_R)
            coef = mul((C.CD.subtract(qv[0], eta), C.CU.add(qv[1], eta)), Sd)
            out[(d, key)] = coef
    return out

def main(cells_path, *nodes_paths, recheck=True, sample=24):
    spec, cells = G.load_cells(cells_path)
    done = {}
    for np_ in nodes_paths:
        done.update({int(k): v for k, v in json.load(open(np_)).items()})
    require(len(done) == len(cells), 'incomplete node values: %d of %d cells' % (len(done), len(cells)))
    rows = [{k: Dec(v) for k, v in r.items()} for r in spec['rows']]
    u_lo = Dec(spec['u_lo']); u_hi = Dec(spec['u_hi'])
    require(G.TAYLOR[0] == int(spec['taylor'][0]) and str(G.TAYLOR[1]) == spec['taylor'][1] and str(G.TAYLOR[2]) == spec['taylor'][2])
    require(G.NGAUSS == spec['ngauss'] and Dec(spec['row_width']) == G.ROW_WIDTH and spec['nw0'] == G.NW0)
    require(C.CU.add(u_lo, C.CU.multiply(G.ROW_WIDTH, Dec(len(rows)))) == u_hi, 'rows do not end at u_hi')
    # the rows and the cells tile: every cell lies in one row's rectangle; the cells of each row tile its rectangle (exact decimals)
    tile = {}
    for c in cells:
        uc, hu, wc, hw = c[:4]
        row = [r for r in rows if r['uc'] - r['hu'] <= uc - hu and uc + hu <= r['uc'] + r['hu'] and r['w_lo'] <= wc - hw and wc + hw <= r['w_hi']]
        require(len(row) == 1, 'cell outside the rows')
        tile.setdefault(id(row[0]), []).append((uc - hu, uc + hu, wc - hw, wc + hw))
    for r in rows:
        area = sum((b - a) * (d - c_) for (a, b, c_, d) in tile.get(id(r), []))
        require(area == (2 * r['hu']) * (r['w_hi'] - r['w_lo']), 'the cells of a row do not fill it')
        # pairwise disjointness (open interiors): cells are dyadic; check no overlap by sorting
        segs = sorted(tile.get(id(r), []))
        for i in range(len(segs)):
            for j in range(i + 1, len(segs)):
                a1, b1, c1, d1 = segs[i]; a2, b2, c2, d2 = segs[j]
                require(not (a1 < b2 and a2 < b1 and c1 < d2 and c2 < d1), 'overlapping cells')
    remainders = None
    if recheck:      # C9a: recompute every cell's Gauss remainder bound independently of the stored values
        remainders = []
        for i, c in enumerate(cells):
            E, Eu, Ew = B.cell_remainder(c[0], c[1], c[2], c[3], G.NGAUSS, G.taylor_part())
            require(E == c[4], 'cell %d: stored remainder %s differs from the recomputation %s' % (i, c[4], E))
            remainders.append(E)
        print('C9a: the %d cell remainders recomputed and equal to the stored values' % len(cells))
    if sample:       # C9b: recompute a deterministic sample of node values and require equality
        import random
        rng = random.Random(20261013); idx = sorted(rng.sample(range(len(cells)), min(sample, len(cells))))
        for i in idx:
            k = rng.randrange(G.NGAUSS * G.NGAUSS)
            node = G.cell_nodes(*cells[i][:4])[k]
            res = G.eval_node((node[0], node[1]))
            require(res[:2] == tuple(done[i][k][:2]), 'cell %d node %d: recomputed value differs' % (i, k))
        print('C9b: %d sampled node values recomputed and equal to the stored values' % len(idx))
    encG, totG, remG = G.assemble(cells, done, remainders)
    ot = G.omega_tails(rows)                      # recomputed from the rows (not read from the file)
    tp = G.taylor_part()
    encS, dS = S.region_S(u_lo, tp)
    tt = S.tau_tail(u_hi)
    lo = C.CD.subtract(C.CD.subtract(C.CD.add(encG[0], encS[0]), ot), tt)
    hi = C.CU.add(C.CU.add(C.CU.add(encG[1], encS[1]), ot), tt)
    D = (lo, hi)
    print('Gauss region: sum [%s, %s] (node-width %s), remainder %s' % (totG[0], totG[1], C.width(totG), remG))
    print('region S: [%s, %s]; omega tails %s; tau tail %s' % (encS[0], encS[1], ot, tt))
    print('D in [%s, %s]  width %s' % (lo, hi, C.width(D)))
    co = corollary(D)
    print('q = J/30 - I~_quad - D in [%s, %s]' % (co['q'][0], co['q'][1]))
    for k in ((2, 'L>=10'), (2, 'L>=24'), (3, 'L>=10'), (3, 'L>=24')):
        print('(c3 - R_{2/3})(L), d=%d, %s: [%s, %s]' % (k[0], k[1], co[k][0], co[k][1]))
    return D

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    main(args[0], *args[1:], recheck='--no-recheck' not in sys.argv, sample=0 if '--no-sample' in sys.argv else 24)
