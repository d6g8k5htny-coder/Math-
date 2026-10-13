"""Assembly of the certified enclosure of D and the corollary.
   D = D_S + D_G + (omega tails) + (tau tail), with
   D_S from ddS.region_S (closed form), D_G from ddgauss (cells + node values + remainder bounds), the omega tails from
   ddgauss.omega_tails, the tau tail from ddS.tau_tail.
Usage: python3 dd_exact.py <cells.json> <nodes.json>"""
import sys, json, math
from fractions import Fraction as Fr
from decimal import Decimal as Dec
import ddcore as C
from ddcore import q, add, sub, mul, div, smul, ZERO, ONE
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

def main(cells_path, *nodes_paths):
    spec, cells = G.load_cells(cells_path)
    done = {}
    for np_ in nodes_paths:
        done.update({int(k): v for k, v in json.load(open(np_)).items()})
    assert len(done) == len(cells), 'incomplete node values: %d of %d cells' % (len(done), len(cells))
    encG, totG, remG = G.assemble(cells, done)
    rows = [{k: Dec(v) for k, v in r.items()} for r in spec['rows']]
    ot = G.omega_tails(rows)                      # recomputed from the rows (not read from the file)
    tp = B.TaylorPart(int(spec['taylor'][0]), Fr(spec['taylor'][1]), Fr(spec['taylor'][2]))
    u_lo = Dec(spec['u_lo']); u_hi = Dec(spec['u_hi'])
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
    main(sys.argv[1], *sys.argv[2:])
