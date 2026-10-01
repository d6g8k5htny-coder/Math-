"""Certificate for CL-C2-EXACT-20261001: the third-order coefficient c2 of Math-#216 / #218 (0.1) for the Gaussian kernel,
d = 1, 2, 3, in closed form and as interval enclosures; also the leading coefficient c by the same pipeline.

    python3 -B -S certificate.py --write     derive, check, write RESULTS.json
    python3 -B -S certificate.py --check     derive, check, compare with RESULTS.json (must be identical)
    python3 -B -S certificate.py --mutant N  a seeded defect; the exact checks must reject it (exit 1)

Standard library only.  The derivation is exact (Fractions; exact.py, pseries.py); only the final evaluation of the closed
forms uses outward-rounded binary64 intervals (ia.py, elem.py, gam.py)."""
import argparse
import json
import math
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

import pseries as P
import exact as X
from exact import Num
from ia import dn, up, mul, div, isqrt, from_frac, PI
import gam

PACKET = 'CL-C2-EXACT-20261001-v1'
MUTANTS = ('target', 'finite-part', 'cone-sign', 'truncation', 'sphere')
DIGITS = 16
MARGIN = 1e-14


def install_mutant(name):
    if name in ('target', 'finite-part', 'cone-sign'):
        X.MUTANT = name
    elif name == 'truncation':
        X.NR = 3
    elif name == 'sphere':
        X.SPHERE[2] = Num.pi_half(2)
    elif name is not None:
        raise SystemExit('unknown mutant: %s' % name)


# ------------------------------------------------------------------------------------------- derivation
def derive():
    out = {}
    for d in (1, 2, 3):
        data = X.kernel_data(d)
        for which, nm in ((0, 'c'), (2, 'c2')):
            val, atom, info = X.coefficient(d, which, data)
            out[(d, nm)] = (val, atom, info)
    return out


def side24_cref(d):
    """c_(d,ref) of coefficients/side24_v1 (1) in the atom Gamma(1/6) 12^(-1/6):
    c_(d,ref) = Gamma(7/6) (3/2)^(1/3) D_(d-1) / (2 sqrt3 pi^(d-1) sqrt(pi)),  D_1 = 4/3,  D_2 = 29/6 - sqrt6.
    With Gamma(7/6) = Gamma(1/6)/6 and (3/2)^(1/3) = sqrt3 12^(-1/6):  c_(d,ref) = atom * D_(d-1) / (12 pi^(d - 1/2))."""
    D = {2: Num.rat(Fr(4, 3)), 3: Num.rat(Fr(29, 6)) - Num.sqrt(6)}[d]
    return D * Fr(1, 12) * Num.pi_half(-(2 * d - 1))


def d1_closed():
    """Math-#214 (D1.2) for the Gaussian kernel: lambda_2, 4, 6, 8 = 1, 3, 15, 105, D = lambda_2 lambda_6 - lambda_4^2 = 6,
    sigma_3 = sqrt(D/lambda_2) = sqrt6, p_12 = 1/(2 pi sqrt(lambda_2 lambda_4)) = 1/(2 pi sqrt3),
    Q/(120 lambda_2 lambda_4 D) = 1620/2160 = 3/4.
      C_0 = 2 . 72^(-1/6) Gamma(7/6) (2 pi)^(-1/2) p_12 sigma_3^(4/3);  72^(-1/6) 6^(2/3) = sqrt6 . 12^(-1/6), so
      C_0 = atom_c . 2 (1/6) sqrt6 (2 pi)^(-1/2) / (2 pi sqrt3) = atom_c . (1/6) pi^(-3/2).
      2 B_2 = 2 . 2^(1/2) 3^(1/3) Gamma(5/6) (2 pi)^(-1/2) p_12 sigma_3^(2/3) . 3/4;  3^(1/3) 6^(1/3) = 12 sqrt3 . 12^(-5/6), so
      2 B_2 = atom_c2 . 2 sqrt2 12 sqrt3 (3/4) (2 pi)^(-1/2) / (2 pi sqrt3) = atom_c2 . 9 pi^(-3/2)."""
    return Num.rat(Fr(1, 6)) * Num.pi_half(-3), Num.rat(9) * Num.pi_half(-3)


def d1_float():
    """the same two numbers directly from #214's formulas in floating point (a check of the reductions above)"""
    l2, l4, l6, l8 = 1.0, 3.0, 15.0, 105.0
    D = l2 * l6 - l4 * l4
    s3 = math.sqrt(D / l2)
    p12 = 1 / (2 * math.pi * math.sqrt(l2 * l4))
    C0 = 2 * 72 ** (-1 / 6) * math.gamma(7 / 6) * (2 * math.pi) ** -0.5 * p12 * s3 ** (4 / 3)
    Q = 4 * l2 ** 2 * l4 * l8 + 26 * l2 * l4 ** 2 * l6 - 5 * l2 ** 2 * l6 ** 2 - 25 * l4 ** 4
    B2 = 2 ** 0.5 * 3 ** (1 / 3) * math.gamma(5 / 6) * (2 * math.pi) ** -0.5 * p12 * s3 ** (2 / 3) * Q / (120 * l2 * l4 * D)
    return C0, 2 * B2


def checks(res):
    """Exact checks.  Returns a list of failure strings."""
    fails = []
    for key, (val, atom, info) in res.items():
        if any(e for (_, _, e) in val.t):
            fails.append('%s: the cone atom theta does not cancel' % (key,))
    for d in (2, 3):
        if not res[(d, 'c')][0] == side24_cref(d):
            fails.append('d = %d: c differs from side24_v1 (1): %s' % (d, res[(d, 'c')][0].text()))
    C0, B2x2 = d1_closed()
    if not res[(1, 'c')][0] == C0:
        fails.append('d = 1: c differs from Math-#214 C_0')
    if not res[(1, 'c2')][0] == B2x2:
        fails.append('d = 1: c2 differs from Math-#214 2 B_2')
    fc, fb = d1_float()
    if not (abs(fc - num_float(C0, 'c')) < 1e-14 and abs(fb - num_float(B2x2, 'c2')) < 1e-14):
        fails.append('d = 1: the reductions of #214 closed forms disagree in floating point')
    return fails


def stability(res):
    """recompute with higher truncation orders; the exact results must be identical"""
    oldR, oldNR = P.R, X.NR
    try:
        P.R, X.NR = 12, 8
        res2 = derive()
    finally:
        P.R, X.NR = oldR, oldNR
    return [('%s changes with the truncation order' % (key,)) for key in res if not res[key][0] == res2[key][0]]


# ------------------------------------------------------------------------------------------- evaluation
ATOMS = {'c': (Fr(1, 6), Fr(-1, 6)), 'c2': (Fr(5, 6), Fr(-5, 6))}


def num_float(n, which):
    g, e = ATOMS[which]
    a = math.gamma(float(g)) * 12.0 ** float(e)
    return a * math.fsum(float(v) * math.pi ** (h / 2) * math.sqrt(m) for (h, m, _), v in n.t.items())


def ipow(x, n):
    out = (1.0, 1.0)
    for _ in range(abs(n)):
        out = mul(out, x)
    return out if n >= 0 else div((1.0, 1.0), out)


def num_iv(n, which):
    g, e = ATOMS[which]
    atom = mul(gam.gamma(g), gam.rpow((12.0, 12.0), e))
    tot = (0.0, 0.0)
    for (h, m, _), v in sorted(n.t.items()):
        term = from_frac(v)
        term = mul(term, ipow(PI, h // 2))
        if h % 2:
            term = mul(term, isqrt(PI))
        if m != 1:
            term = mul(term, isqrt(from_frac(Fr(m))))
        tot = (dn(tot[0] + term[0]), up(tot[1] + term[1]))
    return mul(atom, tot)


def _round_out(x, upward):
    from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING
    dd = Decimal(x)
    q = Decimal(1).scaleb(dd.adjusted() - DIGITS + 1)
    return str(dd.quantize(q, rounding=ROUND_CEILING if upward else ROUND_FLOOR))


def pub(iv):
    lo, hi = iv[0] - MARGIN * abs(iv[0]), iv[1] + MARGIN * abs(iv[1])
    return [_round_out(dn(lo), False), _round_out(up(hi), True)]


RATIO_TEXT = {1: '54', 2: '78', 3: '18 (141 - sqrt6)/25'}


def document(res):
    vals, exact = {}, {}
    for d in (1, 2, 3):
        c, c2 = num_iv(res[(d, 'c')][0], 'c'), num_iv(res[(d, 'c2')][0], 'c2')
        vals['d=%d' % d] = {'c': pub(c), 'c2': pub(c2), 'c2 / c': pub(div(c2, c))}
        exact['d=%d' % d] = {'c': '[%s] * %s' % (res[(d, 'c')][0].text(), res[(d, 'c')][1]),
                             'c2': '[%s] * %s' % (res[(d, 'c2')][0].text(), res[(d, 'c2')][1]),
                             'c2 / c': '%s * Gamma(5/6)/(12^(2/3) Gamma(1/6))' % RATIO_TEXT[d]}
    info3 = res[(3, 'c2')][2]
    return {
        'object': PACKET,
        'scientific_effect': 'NONE',
        'statement': 'closed forms and interval enclosures (outward decimals) of the leading coefficient c and the '
                     'third-order coefficient c2 of the short-lifetime law, Gaussian kernel, d = 1, 2, 3 (Math-#216, '
                     '#218 (0.1)); see NOTE.md',
        'exact': exact,
        'values': vals,
        'derivation': {'series_order_R': P.R, 'polynomial_order_NR': X.NR, 'stability_orders': [12, 8],
                       'd=3 cone exponent [alpha, beta, gamma, D]': [str(info3[k]) for k in ('alpha', 'beta', 'gamma',
                                                                                              'D')],
                       'd=2 cone exponent gamma_a': str(res[(2, 'c2')][2]['gamma_a'])},
        'publication': {'margin_relative': MARGIN, 'digits': DIGITS},
    }


def ratio_check(res):
    """c2/c in closed form against the interval quotient"""
    fails = []
    base = div(mul(gam.gamma(Fr(5, 6)), (1.0, 1.0)), mul(gam.rpow((12.0, 12.0), Fr(2, 3)), gam.gamma(Fr(1, 6))))
    k = {1: from_frac(Fr(54)), 2: from_frac(Fr(78)),
         3: mul(from_frac(Fr(18, 25)), (dn(141 - isqrt((6.0, 6.0))[1]), up(141 - isqrt((6.0, 6.0))[0])))}
    for d in (1, 2, 3):
        a = mul(k[d], base)
        q = div(num_iv(res[(d, 'c2')][0], 'c2'), num_iv(res[(d, 'c')][0], 'c'))
        if a[1] < q[0] or q[1] < a[0]:
            fails.append('d = %d: closed-form ratio %r disjoint from the quotient %r' % (d, a, q))
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--mutant', default=None)
    a = ap.parse_args()
    if a.mutant is not None and a.mutant not in MUTANTS:
        print('unknown mutant', a.mutant)
        return 2
    install_mutant(a.mutant)
    try:
        res = derive()
    except (ArithmeticError, ValueError) as e:
        print('DERIVATION FAILURE', e)
        return 1
    fails = checks(res) + ratio_check(res)
    if not fails and a.mutant is None:
        fails += stability(res)
    print('exact checks: %d failures' % len(fails))
    for f in fails:
        print('CHECK FAILURE', f)
    if fails:
        return 1
    for d in (1, 2, 3):
        print('d = %d: c = %s ; c2 = %s' % (d, res[(d, 'c')][0].text() + ' * ' + res[(d, 'c')][1],
                                           res[(d, 'c2')][0].text() + ' * ' + res[(d, 'c2')][1]))
    if not (a.write or a.check):
        return 0
    doc = document(res)
    path = os.path.join(HERE, 'RESULTS.json')
    if a.write:
        with open(path, 'w') as fh:
            json.dump(doc, fh, indent=1)
            fh.write('\n')
        print('wrote', path)
        return 0
    with open(path) as fh:
        old = json.load(fh)
    if old != json.loads(json.dumps(doc)):
        print('MISMATCH: the recomputed document differs from RESULTS.json')
        return 1
    print(json.dumps({'object': PACKET, 'check': 'passed', 'scientific_effect': 'NONE'}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
