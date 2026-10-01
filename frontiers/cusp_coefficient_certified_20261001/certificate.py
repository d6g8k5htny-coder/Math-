"""Certificate for CL-CU-CUSP-COEFFICIENT-20261001: rigorous enclosures of the cusp coefficient c1 of Theorem CU
(Math-#207, (CU.2)) for the Gaussian kernel in d = 1, 2, 3, of I^cand = (3^(1/4)/2) c1, and of the ratios c1/c_(d,ref);
by Lemma S (side24.py) also for the [P] torus field of every side L >= 24 in d = 2, 3, with the ratios c1/c_(d,24).

    python3 -B -S certificate.py --write [--procs N]     compute and write RESULTS.json
    python3 -B -S certificate.py --check [--procs N]     self-test, recompute, compare with RESULTS.json
    python3 -B -S certificate.py --check --mutant NAME   a seeded defect; the self-test must reject it (exit 1)

Standard library only.  All arithmetic is outward-rounded binary64 interval arithmetic (ia.py, elem.py, cx.py).
NOTE.md states the reduction and the error bounds."""
import argparse
import json
import math
import os
import sys
import time
from fractions import Fraction as Fr
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

import ia
from ia import dn, up, add, sub, mul, div, scal, from_frac
import elem as EL
import gauss as G
import cusp as CU
import cx as CX
import consts as K
import d3
import side24 as S24

PACKET = 'CL-CU-CUSP-COEFFICIENT-20261001-v1'
U_EDGES = (0.0, 0.4, 0.7, 0.9, 1.0, 1.1, 1.3, 1.6, 2.0, 2.6, 3.4, 4.5, 6.0, 8.0, 11.0, 15.0)
U_MAX = U_EDGES[-1]
TOL2 = 5e-16            # per u-panel, d = 2
TOL3 = 1e-11            # per (s, t) box, d = 3
RHOS2 = (4.0, 3.0, 2.4, 2.0, 1.7, 1.5, 1.35, 1.25, 1.18, 1.12)
MARGIN = 1e-12          # relative widening before publication
DIGITS = 16             # significant digits of the published decimals
MUTANTS = ('kernel-A', 'gl-weight', 'bound-scale', 'phase-sign', 'tail-drop', 'image-order6')
MUTANT = None


# ---------------------------------------------------------------- mutants (seeded defects for the workflow)
def install_mutant(name):
    global MUTANT
    MUTANT = name
    if name == 'kernel-A':
        orig = EL.A_pt

        def A_pt(t):
            return orig(t * 1.0000001)
        EL.A_pt = A_pt
    elif name == 'gl-weight':
        orig_rule = G.rule

        def rule(n):
            xs, ws = orig_rule(n)
            return xs, [scal(1.0 + 1e-9, w) for w in ws]
        G.rule = rule
    elif name == 'bound-scale':
        orig_eb = G.error_bound

        def error_bound(n, rho, M, h):
            return orig_eb(n, rho, M, h) * 1e-6
        G.error_bound = error_bound
    elif name == 'phase-sign':
        CU.MUTANT = 'phase-sign'
    elif name == 'tail-drop':
        d3.tail_t = lambda: (0.0, 0.0)
    elif name == 'image-order6':
        S24.IMAGE_ORDER = 6
    elif name is not None:
        raise SystemExit('unknown mutant: %s' % name)


# ---------------------------------------------------------------- independent floating references (self-test only)
def _g2_float(u):
    w = u ** 4
    H = (1 + 1j * w) ** -0.5 * (1 - 1j * w / 3 + 19 * w * w / 36) ** -0.625
    return (1 - H.real) / (w * w)


def _f3_float(s, v, t):
    a1 = s ** 4
    a2 = a1 * v ** 4
    w = t ** 4 / a1
    Phi = ((1 - 1j * w * a1) ** -0.5 * (1 - 1j * w * a2) ** -0.5
           * complex(math.e) ** (-1j * w * a1 * a2 * (a1 + a2) / 20 - 23 * w * w * (a1 * a2) ** 2 / 240))
    Gt = (1 - Phi.real) / (w * a1) ** 2
    return s ** 20 * v ** 4 * (1 - v ** 4) * math.exp(-s ** 8 * (2 * v ** 8 - v ** 4 + 2) / 10) * Gt


def _E1f(x):
    return math.expm1(x) / x if x != 0.0 else 1.0


def _Lf(x):
    return math.log1p(x) / x if x != 0.0 else 1.0


def _Af(x):
    return math.atan(x) / x if x != 0.0 else 1.0


def _Sf(x):
    return math.sin(x) / x if x != 0.0 else 1.0


def _Gf(Rt, It, R, I):
    return -_E1f(R) * Rt + math.exp(R) * _Sf(I / 2) ** 2 * It * It / 2


def _g2_safe_float(u):
    """g2 by the safe formulation in plain floating point (libm), for the assembly check."""
    w = u ** 4
    w2 = w * w
    q = 7 / 6 + 361 * w2 / 1296
    Rt = -0.25 * _Lf(w2) - 5 / 16 * q * _Lf(w2 * q)
    v = 3 + 19 * w2 / 12
    It = -0.5 * _Af(w) + 5 / 8 * _Af(w / v) / v
    return _Gf(Rt, It, w2 * Rt, w * It)


def _f3_safe_float(s, v, t):
    a1sq = s ** 8
    v4, t4 = v ** 4, t ** 4
    v8, t8 = v4 * v4, t4 * t4
    Rt = -0.25 * (_Lf(t8) + v8 * _Lf(t8 * v8)) - 23 / 240 * a1sq * v8
    It = 0.5 * (_Af(t4) + v4 * _Af(t4 * v4)) - a1sq * v4 * (1 + v4) / 20
    G = _Gf(Rt, It, t8 * Rt, t4 * It)
    return s ** 20 * v4 * (1 - v4) * math.exp(-a1sq * (2 * v8 - v4 + 2) / 10) * G


def _gl_float(f, a, b, n=40):
    xs, ws = G.rule(n)
    c, h = 0.5 * (a + b), 0.5 * (b - a)
    return sum(0.5 * (w[0] + w[1]) * h * f(c + h * 0.5 * (x[0] + x[1])) for x, w in zip(xs, ws))


def selftest():
    """Returns a list of failure strings (empty when all checks pass)."""
    fails = []
    # (1) Gauss-Legendre exactness on even monomials, for every n the certificate may use.
    for n in (4, 6, 8, 12, 16, 20, 24, 32, 40, 48):
        xs, ws = G.rule(n)
        for k in range(0, n, max(1, n // 6)):
            s = (0.0, 0.0)
            for x, w in zip(xs, ws):
                s = add(s, mul(w, ia.pw(x, 2 * k)))
            if not (Fr(s[0]) <= Fr(2, 2 * k + 1) <= Fr(s[1])):
                fails.append('GL n=%d exactness at degree %d' % (n, 2 * k))
                break
    # (2) the safe-form integrands against the direct complex-power formulas (floating), at moderate arguments
    for u in (0.3, 0.7, 1.0, 1.4, 2.2):
        iv = CU.g2(CU.RealOps, (u, u))
        ref = _g2_float(u)
        if not abs(0.5 * (iv[0] + iv[1]) - ref) <= 1e-10 * abs(ref):
            fails.append('g2(%g): %r vs %r' % (u, iv, ref))
    for s, v, t in ((1.2, 0.6, 0.5), (1.4, 0.9, 1.2), (0.9, 0.3, 2.0), (1.6, 0.8, 0.8), (1.3, 0.5, 3.0)):
        iv = CU.f3(CU.RealOps, (s, s), (v, v), (t, t))
        ref = _f3_float(s, v, t)
        if not abs(0.5 * (iv[0] + iv[1]) - ref) <= 1e-9 * abs(ref):
            fails.append('f3(%g, %g, %g): %r vs %r' % (s, v, t, iv, ref))
    # (3) a deliberately coarse rule: the certified enclosure must contain a 40-point floating reference.
    iv, n, rho, M, e = panel2(0.85, 1.15, 1e-9, nmin=6)
    ref = _gl_float(_g2_float, 0.85, 1.15)
    if not (iv[0] <= ref <= iv[1]):
        fails.append('coarse d = 2 panel: %r does not contain %r' % (iv, ref))
    # (4) the t-tail against its floating formula
    T = d3.T_MAX
    tt = d3.tail_t()
    W = math.gamma(21 / 8) / 8 * _gl_float(lambda v: v ** 4 * (1 - v ** 4) * ((2 * v ** 8 - v ** 4 + 2) / 10) ** (-21 / 8), 0.0, 1.0)
    ref = W * T ** -7 / 7
    if not (tt[0] <= ref <= tt[1]) or not tt[1] - tt[0] < 1e-2 * ref:
        fails.append('t-tail: %r vs %r' % (tt, ref))
    # (5) Lemma S: the exact jet covariance C_0 reproduces Lemma R.1 (regression, det C_P = 12, (C_P^-1)_ff = 3/2), and
    # the premises of the transfer hold (image bound order, matchings count, positive definiteness of C_0 - mu I)
    for d in (2, 3):
        fails.extend(S24.lemma_r_check(d))
        try:
            S24.transfer(d)
        except ValueError as e:
            fails.append('Lemma S, d = %d: %s' % (d, e))
    if S24.matchings(8) != 764:
        fails.append('T_8 != 764')
    enc = S24.enclosure_check(HERE)
    if enc:
        fails.extend(enc)
    return fails


# ---------------------------------------------------------------- assembly cross-checks (floating, coarse)
def assembly_check(name, iv, ref, rel):
    """The certified enclosure must agree with an independent coarse floating quadrature of the same integral to the
    relative tolerance rel.  This guards the assembly (normalizations, factors, tails) and is not part of the bound."""
    mid = 0.5 * (iv[0] + iv[1])
    if not abs(mid - ref) <= rel * abs(ref):
        raise RuntimeError('assembly check failed for %s: certified mid %r vs floating %r' % (name, mid, ref))


def float_int_g2():
    """int_0^oo g2 by floating Gauss-Legendre (40 nodes per u-panel, safe formulation in libm floating point) plus the
    main tail term."""
    return sum(_gl_float(_g2_safe_float, a, b) for a, b in zip(U_EDGES, U_EDGES[1:])) + U_MAX ** -7 / 7


def float_T3():
    """T3 = 64 int int int f3 by coarse floating Gauss-Legendre with the safe formulation in libm floating point."""
    tot = 0.0
    xs, ws = G.rule(24)
    def nodes(a, b):
        c, h = 0.5 * (a + b), 0.5 * (b - a)
        return [(c + h * 0.5 * (x[0] + x[1]), h * 0.5 * (w[0] + w[1])) for x, w in zip(xs, ws)]
    s_nodes = [q for a, b in ((0.3, 1.0), (1.0, 1.4), (1.4, 1.8), (1.8, 2.4)) for q in nodes(a, b)]
    v_nodes = [q for a, b in ((0.0, 0.5), (0.5, 0.8), (0.8, 1.0)) for q in nodes(a, b)]
    t_nodes = [q for a, b in ((0.0, 0.7), (0.7, 1.2), (1.2, 2.5), (2.5, 6.0), (6.0, 15.0)) for q in nodes(a, b)]
    for s, w1 in s_nodes:
        for v, w2 in v_nodes:
            inner = sum(w3 * _f3_safe_float(s, v, t) for t, w3 in t_nodes)
            wgt = s ** 20 * v ** 4 * (1 - v ** 4) * math.exp(-s ** 8 * (2 * v ** 8 - v ** 4 + 2) / 10)
            inner += wgt * 15.0 ** -7 / 7
            tot += w1 * w2 * inner
    return 64.0 * tot


# ---------------------------------------------------------------- d = 2
def _g2_safe_bound(box):
    return CX.cabs_up(CU.g2(CU.CplxOps, box))


def panel2(a, b, tol, nmin=4, m=24, nmax=60):
    """Certified int_a^b g2 with the smallest admissible Gauss-Legendre rule (n >= nmin); returns (enclosure, n, rho,
    M, err).  For each rho the bound M is the smaller of the two representations' maxima over the slabs; a
    representation counts only if it succeeds on every slab (NOTE.md, Lemma Q)."""
    h = 0.5 * (b - a)
    best = None
    for rho in RHOS2:
        slabs = G.ellipse_slabs(a, b, rho, m)
        Ms = []
        for bf in (_g2_safe_bound, CU.g2_bound_direct):
            try:
                Ms.append(max(bf(bx) for bx in slabs))
            except d3.FAIL:
                pass
        if not Ms:
            continue
        M = min(Ms)
        for n in range(nmin, nmax + 1):
            e = G.error_bound(n, rho, M, h)
            if e <= tol:
                if best is None or (n, e) < (best[0], best[1]):
                    best = (n, e, rho, M)
                break
        if nmin > 4 and best is not None:
            break
    if best is None:
        raise RuntimeError('d = 2 panel [%g, %g]: no admissible rule' % (a, b))
    n, e, rho, M = best
    if nmin > 4:
        n = nmin
        e = G.error_bound(n, rho, M, h)
    xs, ws = G.panel(n, a, b)
    Q = (0.0, 0.0)
    for x, w in zip(xs, ws):
        Q = add(Q, mul(w, CU.g2(CU.RealOps, x)))
    return (dn(Q[0] - e), up(Q[1] + e)), n, rho, M, e


def run_d2(log=print):
    tot = (0.0, 0.0)
    rules = []
    for a, b in zip(U_EDGES, U_EDGES[1:]):
        iv, n, rho, M, e = panel2(a, b, TOL2)
        tot = add(tot, iv)
        rules.append([a, b, n, rho])
    # tail u > U_MAX: int g2 = U^-7/7 - int u^-8 Re H, |Re H(u^4)| <= (36/19)^(5/8) u^-7 < 1.5 u^-7
    U = U_MAX
    main = div((1.0, 1.0), (7.0 * U ** 7, 7.0 * U ** 7))
    err = up(1.5 * U ** -14 / 14.0 * (1 + 1e-12))
    tail = (dn(main[0] - err), up(main[1] + err))
    tot = add(tot, tail)
    log('d = 2: int g2 in [%.17g, %.17g]' % tot)
    assembly_check('d = 2: int g2', tot, float_int_g2(), 1e-9)
    return {'int_g2': tot, 'tail': tail, 'rules': rules}


# ---------------------------------------------------------------- d = 3
def _box_job(b):
    S, T = b
    iv, info = d3.box(S, T, TOL3)
    return iv, info


def run_d3(procs, log=print):
    bx = d3.boxes()
    t0 = time.time()
    if procs > 1:
        with Pool(procs) as pool:
            res = pool.map(_box_job, bx, chunksize=1)
    else:
        res = [_box_job(b) for b in bx]
    tot = (0.0, 0.0)
    crude = gl = nodes = 0
    for iv, info in res:
        tot = add(tot, iv)
        if info.get('crude'):
            crude += 1
        else:
            gl += 1
            nodes += info['ns'] * info['nt'] * sum(info['nv'])
    tt = d3.tail_t()
    ts = d3.tail_s_bound()
    T3 = scal(64.0, add(add(tot, tt), (0.0, ts)))
    log('d = 3: T3 in [%.17g, %.17g]  (%d boxes: %d crude, %d Gauss-Legendre, %d nodes; %.0fs)' % (
        T3[0], T3[1], len(bx), crude, gl, nodes, time.time() - t0))
    assembly_check('d = 3: T3', T3, float_T3(), 1e-6)
    return {'T3': T3, 'boxes': scal(64.0, tot), 'tail_t': scal(64.0, tt), 'tail_s': (0.0, 64.0 * ts),
            'n_boxes': len(bx), 'n_crude': crude,
            'n_gl': gl, 'n_nodes': nodes}


# ---------------------------------------------------------------- assembly and publication
def certify(procs, log=print):
    out = {}
    out['d2'] = run_d2(log)
    out['d3'] = run_d3(procs, log)
    out['P2'] = K.prefactor_d2()
    out['P3'] = K.prefactor_d3()
    out['c1'] = {1: K.c1_d1(), 2: mul(out['P2'], out['d2']['int_g2']), 3: mul(out['P3'], out['d3']['T3'])}
    out['cref'] = {2: K.c_ref(2), 3: K.c_ref(3)}
    out['side24'] = {d: S24.transfer(d) for d in (2, 3)}
    out['K_p'] = K.K_p()
    out['Gamma'] = {'5/8': K.gamma(Fr(5, 8)), '11/4': K.gamma(Fr(11, 4)), '11/8': K.gamma(Fr(11, 8)),
                    '7/6': K.gamma(Fr(7, 6))}
    return out


def _round_out(x, digits, upward):
    if x == 0.0:
        return '0'
    from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING
    d = Decimal(x)
    q = Decimal(1).scaleb(d.adjusted() - digits + 1)
    return str(d.quantize(q, rounding=ROUND_CEILING if upward else ROUND_FLOOR))


def pub(iv, digits=DIGITS):
    lo = iv[0] - MARGIN * abs(iv[0])
    hi = iv[1] + MARGIN * abs(iv[1])
    return [_round_out(dn(lo), digits, False), _round_out(up(hi), digits, True)]


def derived(raw):
    from decimal import Decimal
    res = {}
    for d in (1, 2, 3):
        c1 = raw['c1'][d]
        Ic = mul(K.I_CAND_FACTOR, c1)
        res['d=%d' % d] = {'c1': c1, 'I_cand = (3^(1/4)/2) c1': Ic, 'I_cand - c1': sub(Ic, c1)}
        if d in (2, 3):
            res['d=%d' % d]['c_(d,ref)'] = raw['cref'][d]
            res['d=%d' % d]['c1 / c_(d,ref)'] = div(c1, raw['cref'][d])
    sec = res['[P] field, every L >= 24 (Lemma S)'] = {}
    for d in (2, 3):
        eta = raw['side24'][d]['eta']
        fac = (from_frac(1 - eta)[0], from_frac(1 + eta)[1])
        c1L = mul(raw['c1'][d], fac)
        IcL = mul(K.I_CAND_FACTOR, c1L)
        lo, hi = S24.C_24[d]
        c24 = (from_frac(Fr(lo))[0], from_frac(Fr(hi))[1])
        sec['d=%d: c1' % d] = c1L
        sec['d=%d: I_cand' % d] = IcL
        sec['d=%d: I_cand - c1' % d] = sub(IcL, c1L)
        sec['d=%d: c_(d,24) (side24_v1, consumed)' % d] = c24
        sec['d=%d: c1 / c_(d,24), L = 24' % d] = div(c1L, c24)
    res['parts'] = {
        'd=2: int_0^oo g2(u) du': raw['d2']['int_g2'],
        'd=2: tail u > %g' % U_MAX: raw['d2']['tail'],
        'd=2: P2': raw['P2'],
        'd=3: T3': raw['d3']['T3'],
        'd=3: boxes': raw['d3']['boxes'],
        'd=3: tail t > %g' % d3.T_MAX: raw['d3']['tail_t'],
        'd=3: tail s > %g' % d3.S_MAX: raw['d3']['tail_s'],
        'd=3: P3': raw['P3'],
        'K = pi/(2 Gamma(11/4) sin(7 pi/8))': raw['K_p'],
    }
    for k, v in raw['Gamma'].items():
        res['parts']['Gamma(%s)' % k] = v
    return res


def document(raw):
    der = derived(raw)
    vals = {}
    for sec, items in der.items():
        vals[sec] = {k: pub(v) for k, v in items.items()}
    return {
        'object': PACKET,
        'scientific_effect': 'NONE',
        'statement': 'interval enclosures (outward decimals) of the cusp coefficient c1 of Math-#207 (CU.2) for the '
                     'Gaussian kernel, d = 1, 2, 3; see NOTE.md',
        'values': vals,
        'rules': {
            'd=2 panels [a, b, n, rho]': raw['d2']['rules'],
            'd=3': {'boxes': raw['d3']['n_boxes'], 'crude': raw['d3']['n_crude'], 'gauss_legendre': raw['d3']['n_gl'],
                    'nodes': raw['d3']['n_nodes'], 'T_MAX': d3.T_MAX, 'S_MAX': d3.S_MAX},
            'Lemma S (exact rationals)': {
                'd=%d' % d: {k: str(v) for k, v in raw['side24'][d].items()} for d in (2, 3)},
        },
        'publication': {'margin_relative': MARGIN, 'digits': DIGITS},
    }


def compare(doc, raw):
    bad = []
    new = document(raw)
    if new['rules'] != doc['rules']:
        bad.append('rule data differ: %r vs %r' % (new['rules']['d=3'], doc['rules']['d=3']))
    der = derived(raw)
    from decimal import Decimal
    for sec, items in der.items():
        for k, v in items.items():
            p = doc['values'].get(sec, {}).get(k)
            if p is None:
                bad.append('missing %s / %s' % (sec, k))
                continue
            lo, hi = Decimal(p[0]), Decimal(p[1])
            if not (lo <= Decimal(v[0]) and Decimal(v[1]) <= hi):
                bad.append('%s / %s: raw [%r, %r] not inside published %r' % (sec, k, v[0], v[1], p))
            slack = Decimal(3 * MARGIN)
            if (Decimal(v[0]) - lo) > slack * abs(Decimal(v[0])) + Decimal('1e-300') or \
                    (hi - Decimal(v[1])) > slack * abs(Decimal(v[1])) + Decimal('1e-300'):
                bad.append('%s / %s: published %r looser than the replay [%r, %r]' % (sec, k, p, v[0], v[1]))
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--mutant', default=None)
    ap.add_argument('--procs', type=int, default=os.cpu_count() or 2)
    a = ap.parse_args()
    if a.mutant is not None and a.mutant not in MUTANTS:
        print('unknown mutant', a.mutant)
        return 2
    install_mutant(a.mutant)
    fails = selftest()
    print('self-test: %d failures' % len(fails))
    if fails:
        for f in fails[:10]:
            print('SELF-TEST FAILURE', f)
        return 1
    if not (a.write or a.check):
        return 0
    raw = certify(a.procs)
    path = os.path.join(HERE, 'RESULTS.json')
    if a.write:
        with open(path, 'w') as fh:
            json.dump(document(raw), fh, indent=1, sort_keys=False)
            fh.write('\n')
        print('wrote', path)
        return 0
    with open(path) as fh:
        doc = json.load(fh)
    bad = compare(doc, raw)
    if bad:
        for b in bad[:20]:
            print('MISMATCH', b)
        return 1
    print(json.dumps({'object': PACKET, 'check': 'passed', 'scientific_effect': 'NONE'}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
