#!/usr/bin/env python3
"""Certificate for CL-C8-ELDER-FAILURE-COEFFICIENT-20261001-v1 (standard library only).

    python3 -B -S certificate.py --write [--procs N]     full run, writes RESULTS.json
    python3 -B -S certificate.py --check [--procs N]     self-test, then full replay; every replayed enclosure must lie
                                                         inside the published one (and the published one must not be
                                                         looser than the replay by more than the publication margin),
                                                         leaf counts must agree
    python3 -B -S certificate.py --check --mutant NAME   must exit 1
    python3 -B certificate.py --controls                 floating-point cross-checks (not part of the certificate)

Certified quantities (planar near cluster coefficients of [NUM], reference kernel):
    J_fail(k) = J_1 + J_2 = 3k^2 (E[2(B_-)^3] + E[2T] + E[V]),   J_2(k) = 3k^2 E[H_2]       (k = 1/2, 1, 2)
    I_k = int_{1/2}^{2} e^(-12k^2) k^(-5/3) J_fail(k) dk,   C_fail^{B,K} = const * I_b * I_k,
    const = 4 / (sqrt2 (2 pi)^(5/2) sqrt12),   I_b = int_0^1 e^(-b^2) db = sqrt(pi) (Phi(sqrt2) - 1/2)."""
import sys, os, json, time, math, argparse
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as Fr
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ia
from ia import (dn, up, add, sub, neg, mul, div, scal, divc, sqr, pw, isqrt, exp_neg, Phi, Phi_point, SQRT2PI,
                from_frac, PI)
import boxes as BX

PACKET = 'CL-C8-ELDER-FAILURE-COEFFICIENT-20261001-v1'
KS = (0.5, 1.0, 2.0)
TOL3 = {'V': 1e-8, 'H2': 1e-8}      # per-box width tolerance (unscaled expectations)
TOL4 = 2.5e-9
L_BOX = 8.0                         # boxes cover [-8 sigma, 8 sigma] in every jet coordinate
N0, NK0 = 8, 8                      # initial grid: 8 cells per jet coordinate, 8 dyadic k-cells
SK = 0.8                            # k-scale used only to choose the split direction
MAXDEPTH3, MAXDEPTH4 = 60, 80
MARGIN = 1e-7                       # publication: widen relatively by MARGIN, then round outward to 10 digits
DIGITS = 10
SQRT2 = isqrt((2.0, 2.0))


# ================================================================ drivers
def sig3(k):
    """Scaled-law standard deviations for k in KS (all variances exact floats)."""
    v = ((2.0 / k), 2.0, 6.0 * k)
    if v[0] * k != 2.0 or v[2] / k != 6.0:
        raise ValueError('k must make 2/k and 6k exact')
    return [(isqrt((x, x)), (x, x)) for x in v]


_ST = {}


def _init3(k):
    S = sig3(k)
    _ST['M'] = (BX.Moments(S[0][0], S[0][1], 6), BX.Moments(S[1][0], S[1][1], 2), BX.Moments(S[2][0], S[2][1], 2))
    _ST['sd'] = tuple(s[0][1] for s in S)


def _work3(args):
    which, tol, cells, mutant = args
    BX.MUTANT = mutant
    Ma, Mb, Mc = _ST['M']
    sd = _ST['sd']
    fn = BX.H2_box3 if which == 'H2' else (lambda b, x, y, z: BX.big_box3(b, x, y, z, with_H=(which == 'H')))
    lo = hi = 0.0
    nleaf = 0
    for cell in cells:
        stack = [(cell, 0)]
        while stack:
            box, dep = stack.pop()
            I = fn(box, Ma, Mb, Mc)
            if I[1] - I[0] > tol and dep < MAXDEPTH3:
                w = [(box[i][1] - box[i][0]) / sd[i] for i in range(3)]
                d = w.index(max(w))
                l_, h_ = box[d]
                mid = 0.5 * (l_ + h_)
                for half in ((l_, mid), (mid, h_)):
                    nb = list(box)
                    nb[d] = half
                    stack.append((tuple(nb), dep + 1))
            else:
                lo, hi = dn(lo + I[0]), up(hi + I[1])
                nleaf += 1
    return lo, hi, nleaf


def run3(k, which, tol, procs, mutant=None):
    """Sum of box enclosures of E[which] over [-L sigma, L sigma]^3 (which in V, H2, H)."""
    S = sig3(k)
    edges = [[-L_BOX * s[0][1] + 2 * L_BOX * s[0][1] * i / N0 for i in range(N0 + 1)] for s in S]
    cells = [((edges[0][i], edges[0][i + 1]), (edges[1][j], edges[1][j + 1]), (edges[2][l], edges[2][l + 1]))
             for i in range(N0) for j in range(N0) for l in range(N0)]
    chunks = [(which, tol, cells[p::procs], mutant) for p in range(procs)]
    with Pool(procs, initializer=_init3, initargs=(k,)) as pool:
        res = pool.map(_work3, chunks)
    lo = hi = 0.0
    n = 0
    for r in res:
        lo, hi, n = dn(lo + r[0]), up(hi + r[1]), n + r[2]
    return (lo, hi), n, edges


def _init4(elem):
    S = sig3(1.0)                                    # original jet law N(0, diag(2, 2, 6))
    _ST['M'] = (BX.Moments(S[0][0], S[0][1], 6), BX.Moments(S[1][0], S[1][1], 2), BX.Moments(S[2][0], S[2][1], 2))
    _ST['K'] = BX.KMoments(elem)
    _ST['sd'] = tuple(s[0][1] for s in S) + (SK,)


def _work4(args):
    tol, cells, mutant = args
    BX.MUTANT = mutant
    Ma, Mb, Mc = _ST['M']
    Km = _ST['K']
    sd = _ST['sd']
    lo = hi = 0.0
    nleaf = 0
    for cell in cells:
        stack = [(cell, 0)]
        while stack:
            box, dep = stack.pop()
            I = BX.H_box4(box, Ma, Mb, Mc, Km)
            if I[1] - I[0] > tol and dep < MAXDEPTH4:
                w = [(box[i][1] - box[i][0]) / sd[i] for i in range(4)]
                if box[3][1] - box[3][0] <= Km.width:
                    w[3] = -1.0
                d = w.index(max(w))
                l_, h_ = box[d]
                mid = 0.5 * (l_ + h_)
                for half in ((l_, mid), (mid, h_)):
                    nb = list(box)
                    nb[d] = half
                    stack.append((tuple(nb), dep + 1))
            else:
                lo, hi = dn(lo + I[0]), up(hi + I[1])
                nleaf += 1
    return lo, hi, nleaf


def run4(tol, procs, elem, mutant=None):
    S = sig3(1.0)
    edges = [[-L_BOX * s[0][1] + 2 * L_BOX * s[0][1] * i / N0 for i in range(N0 + 1)] for s in S]
    kw = (BX.K_HI - BX.K_LO) / NK0
    kedges = [BX.K_LO + kw * j for j in range(NK0 + 1)]
    cells = [((edges[0][i], edges[0][i + 1]), (edges[1][j], edges[1][j + 1]), (edges[2][l], edges[2][l + 1]),
              (kedges[q], kedges[q + 1])) for q in range(NK0) for i in range(N0) for j in range(N0) for l in range(N0)]
    chunks = [(tol, cells[p::procs], mutant) for p in range(procs)]
    with Pool(procs, initializer=_init4, initargs=(elem,)) as pool:
        res = pool.map(_work4, chunks)
    lo = hi = 0.0
    n = 0
    for r in res:
        lo, hi, n = dn(lo + r[0]), up(hi + r[1]), n + r[2]
    return (lo, hi), n


# ================================================================ exact and one-dimensional parts, tails
def E2T(k):
    """E[2T] = 6 E[u^2] = 6 (6k + 1/(4k) + 5/(216 k^3)) (exact rational)."""
    k = Fr(k)
    return 6 * (6 * k + Fr(1) / (4 * k) + Fr(5) / (216 * k ** 3))


def _gs(mi):
    """g = E[(m - beta)_+^3], g' = 3 E[(m - beta)_+^2], g'' = 6 E[(m - beta)_+] for beta ~ N(0, 2), t = m/sqrt2:
    g = (m^3 + 6m) Phi(t) + sqrt2 (m^2 + 4) phi(t),  g' = 3 [(m^2 + 2) Phi(t) + sqrt2 m phi(t)],
    g'' = 6 [m Phi(t) + sqrt2 phi(t)]; all increasing in m."""
    t = div(mi, SQRT2)
    P = Phi(t)
    ph = div(exp_neg(divc(sqr(mi), 4.0)), SQRT2PI)
    g = add(mul(add(pw(mi, 3), scal(6.0, mi)), P), mul(mul(SQRT2, add(sqr(mi), (4.0, 4.0))), ph))
    g1 = scal(3.0, add(mul(add(sqr(mi), (2.0, 2.0)), P), mul(mul(SQRT2, mi), ph)))
    g2 = scal(6.0, add(mul(mi, P), mul(SQRT2, ph)))
    return g, g1, g2


def tail_moments(L, s, s2, nmax):
    """int_L^inf x^n phi_s(x) dx, n = 0..nmax, L >= 0."""
    pL = BX.phis(L, s, s2)
    q = BX._Qiv(div((L, L), s))
    M = [q, mul(s2, pL)]
    for n in range(2, nmax + 1):
        M.append(add(mul(scal(float(n - 1), s2), M[n - 2]), mul(s2, mul(pw((L, L), n - 1), pL))))
    return M


def E2B(k, L=12.0, N=4000):
    """E[2(B_-)^3] = 4 int_0^inf phi_sa(a) G(a) da with G(a) = g(a^2/12), sa^2 = 2/k: second-order Taylor expansion on each
    of N cells about the midpoint (G'' = g''(m) a^2/36 + g'(m)/6 is increasing in a >= 0, bounded by its values at the
    cell ends), plus the tail a > L sa with g(m) <= m^3 + 6m + sqrt2 (m^2 + 4)/sqrt(2 pi)."""
    s, s2 = sig3(k)[0]
    top = L * s[1]
    acc = (0.0, 0.0)
    for i in range(N):
        a0, a1 = top * i / N, top * (i + 1) / N
        M = BX.moments(a0, a1, s, s2, 2)
        ac = 0.5 * (a0 + a1)
        aci = (ac, ac)
        g, g1, _ = _gs(divc(sqr(aci), 12.0))
        _, g1l, g2l = _gs(divc(sqr((a0, a0)), 12.0))
        _, g1h, g2h = _gs(divc(sqr((a1, a1)), 12.0))
        G2lo = add(divc(mul(g2l, sqr((a0, a0))), 36.0), divc(g1l, 6.0))[0]
        G2hi = add(divc(mul(g2h, sqr((a1, a1))), 36.0), divc(g1h, 6.0))[1]
        M1c = sub(M[1], mul(aci, M[0]))
        M2c = BX._nonneg(add(sub(M[2], scal(2.0, mul(aci, M[1]))), mul(sqr(aci), M[0])))
        cell = add(add(mul(g, M[0]), mul(mul(g1, divc(aci, 6.0)), M1c)), scal(0.5, mul((G2lo, G2hi), M2c)))
        acc = add(acc, cell)
    T = tail_moments(top, s, s2, 6)
    tail = add(add(divc(T[6], 1728.0), divc(T[2], 2.0)),
               mul(div(SQRT2, SQRT2PI), add(divc(T[4], 144.0), scal(4.0, T[0]))))
    return (scal(4.0, acc)[0], scal(4.0, add(acc, (0.0, tail[1])))[1])


def abs_moments(s, s2, nmax):
    """E|X|^n, X ~ N(0, s^2): 1, 2 s^2 phi_s(0), then (n - 1) s^2 E|X|^(n-2)."""
    M = [(1.0, 1.0), scal(2.0, mul(s2, BX.phis(0.0, s, s2)))]
    for n in range(2, nmax + 1):
        M.append(mul(scal(float(n - 1), s2), M[n - 2]))
    return M


def _tail_union(S, L, terms):
    """Upper bound of E[sum_terms c |X1|^i |X2|^j |X3|^l 1{some |X_m| > L sigma_m}] (union bound over m; independence)."""
    full = [abs_moments(S[m][0], S[m][1], 6) for m in range(3)]
    tl = [[scal(2.0, t) for t in tail_moments(L * S[m][0][1], S[m][0], S[m][1], 6)] for m in range(3)]
    tot = (0.0, 0.0)
    for m in range(3):
        for cf, e in terms:
            v = cf
            for j in range(3):
                v = mul(v, tl[j][e[j]] if j == m else full[j][e[j]])
            tot = add(tot, v)
    return tot[1]


def tail3(k):
    """Outside the box, |V|, H and H_2 are at most 17|B|^3 + 8T <= 68|beta|^3 + (68/1728 + 96/5184) a^6 + 48 c^2
    + 6 a^2 beta^2 (scaled coordinates; x <= |B| + (T/2)^(1/3), |B|^3 <= 4(|beta|^3 + a^6/1728), T <= 6c^2 + 6d^2,
    d^2 <= 2(a^2 beta^2/16 + a^6/5184))."""
    c6 = add(divc((68.0, 68.0), 1728.0), divc((96.0, 96.0), 5184.0))
    terms = [((68.0, 68.0), (0, 3, 0)), (c6, (6, 0, 0)), ((48.0, 48.0), (0, 0, 2)), ((6.0, 6.0), (2, 2, 0))]
    return _tail_union(sig3(k), L_BOX, terms)


def tail4(Ktot):
    """Outside the jet box, for every k in [1/2, 2] (original coordinates): H <= 17|B|^3 + 8T <= 68|beta|^3 + 68 a^6/216
    + 576 a^6/5184 + 144 c^2 + 9 a^2 beta^2 (|B| <= |beta| + a^2/6; u^2 <= 6c^2 + 3a^2 beta^2/8 + 24 a^6/5184); times
    int W(k) dk = K_0([1/2, 2])."""
    c6 = add(divc((68.0, 68.0), 216.0), divc((576.0, 576.0), 5184.0))
    terms = [((68.0, 68.0), (0, 3, 0)), (c6, (6, 0, 0)), ((144.0, 144.0), (0, 0, 2)), ((9.0, 9.0), (2, 2, 0))]
    return up(_tail_union(sig3(1.0), L_BOX, terms) * Ktot[1] * (1.0 + 4e-16))


# ================================================================ assembly
def m2(b):
    """m_(2,b) = (b^2 + 2) Phi(b/sqrt2) + sqrt2 b phi(b/sqrt2) (b a float >= 0)."""
    bi = (b, b)
    t = div(bi, SQRT2)
    ph = div(exp_neg(divc(sqr(t), 2.0)), SQRT2PI)
    return add(mul(add(sqr(bi), (2.0, 2.0)), Phi(t)), mul(mul(SQRT2, bi), ph))


def prefactor(b, k):
    """p_b(0)/z_0 = phi(b/sqrt2) / (sqrt2 36 k^2 m_(2,b))."""
    t = div((b, b), SQRT2)
    ph = div(exp_neg(divc(sqr(t), 2.0)), SQRT2PI)
    return div(ph, mul(mul(SQRT2, (36.0 * k * k, 36.0 * k * k)), m2(b)))


def constants():
    sqrt_pi = isqrt(PI)
    two_pi = scal(2.0, PI)
    const = div((4.0, 4.0), mul(mul(SQRT2, mul(sqr(two_pi), isqrt(two_pi))), isqrt((12.0, 12.0))))
    Ib = mul(sqrt_pi, sub(Phi(SQRT2), (0.5, 0.5)))
    return const, Ib


def iv_frac(q):
    return from_frac(q)


def certify(procs, mutant=None, log=print, only=None):
    """Run everything; returns the raw results (floats) and leaf counts."""
    out = {'J': {}, 'leaves': {}}
    t0 = time.time()
    for k in KS:
        if only is not None and k not in only:
            continue
        s = 3.0 * k * k
        EV, nV, _ = run3(k, 'V', TOL3['V'], procs, mutant)
        EH2, nH2, _ = run3(k, 'H2', TOL3['H2'], procs, mutant)
        e2b = E2B(k)
        e2t = iv_frac(E2T(k))
        tl = tail3(k)
        EVt = (dn(EV[0] - tl), up(EV[1] + tl))
        EH2t = (EH2[0], up(EH2[1] + tl))
        Jf = scal(s, add(add(e2b, e2t), EVt))
        J2 = scal(s, EH2t)
        out['J'][k] = {'J_fail': Jf, 'J_2': J2, 'E2B': e2b, 'E2T': e2t, 'EV_boxes': EV, 'EH2_boxes': EH2, 'tail': tl}
        out['leaves']['V k=%g' % k] = nV
        out['leaves']['H2 k=%g' % k] = nH2
        log('k=%g  J_fail in [%.10f, %.10f]  J_2 in [%.10f, %.10f]  (leaves %d, %d; %.0fs)' %
            (k, Jf[0], Jf[1], J2[0], J2[1], nV, nH2, time.time() - t0))
    if only is None:
        elem = BX.elementary_kmoments()
        Km = BX.KMoments(elem)
        Ktot = Km.get(BX.K_LO, BX.K_HI)[0]
        Ik_boxes, n4 = run4(TOL4, procs, elem, mutant)
        t4 = tail4(Ktot)
        Ik = (Ik_boxes[0], up(Ik_boxes[1] + t4))
        const, Ib = constants()
        C = mul(mul(const, Ib), Ik)
        out['Ik'] = {'Ik': Ik, 'boxes': Ik_boxes, 'tail': t4, 'const': const, 'Ib': Ib, 'C_fail': C, 'Wtot': Ktot}
        out['leaves']['I_k 4D'] = n4
        log('I_k in [%.10f, %.10f]  C_fail in [%.12f, %.12f]  (leaves %d; %.0fs)' % (Ik[0], Ik[1], C[0], C[1], n4,
                                                                                    time.time() - t0))
    return out


# ================================================================ publication rounding and the result document
def pub(iv_):
    """Outward publication of an enclosure: widen by MARGIN relatively, round outward to DIGITS significant digits."""
    lo, hi = Decimal(iv_[0]), Decimal(iv_[1])
    lo = lo - abs(lo) * Decimal(MARGIN)
    hi = hi + abs(hi) * Decimal(MARGIN)

    def rnd(x, mode):
        if x == 0:
            return Decimal(0)
        e = x.adjusted() - (DIGITS - 1)
        return x.quantize(Decimal(1).scaleb(e), rounding=mode)
    return [str(rnd(lo, ROUND_FLOOR)), str(rnd(hi, ROUND_CEILING))]


def contains_pub(pub_iv, iv_):
    return Decimal(pub_iv[0]) <= Decimal(iv_[0]) and Decimal(iv_[1]) <= Decimal(pub_iv[1])


def not_looser(pub_iv, iv_):
    """The published interval is within 2 MARGIN + one unit of the last digit of the replayed one."""
    lo, hi = Decimal(iv_[0]), Decimal(iv_[1])
    unit = lambda x: Decimal(1).scaleb(x.adjusted() - (DIGITS - 1)) if x != 0 else Decimal(0)
    lo_min = lo - abs(lo) * Decimal(2 * MARGIN) - unit(lo)
    hi_max = hi + abs(hi) * Decimal(2 * MARGIN) + unit(hi)
    return Decimal(pub_iv[0]) >= lo_min and Decimal(pub_iv[1]) <= hi_max


def derived(raw):
    """Published quantities derived from the raw enclosures."""
    res = {}
    for k in KS:
        J = raw['J'][k]
        Jf, J2 = J['J_fail'], J['J_2']
        J1 = sub(Jf, J2)
        share = div(J2, Jf)
        palm = div(scal(2.0, J2), add(Jf, J2))
        row = {'J_fail': Jf, 'J_1': J1, 'J_2': J2, 'share_J2_over_Jfail': share, 'near_palm_excess': palm,
               'E[2T] exact': str(E2T(k)),
               'parts': {'E[2(B_-)^3]': J['E2B'], 'E[2T]': J['E2T'], 'E[V] boxes': J['EV_boxes'],
                         'E[H_2] boxes': J['EH2_boxes'], 'tail bound': (0.0, J['tail'])}}
        coeffs = {}
        for b in (0.0, 1.0):
            P = prefactor(b, k)
            coeffs['b=%g' % b] = {'p_b(0)/z_0': P, 'alpha_1': mul(P, J1), 'alpha_2': mul(P, J2),
                                 'a_fail = alpha_1 + alpha_2': mul(P, Jf)}
        row['coefficients'] = coeffs
        res['k=%g' % k] = row
    if 'Ik' in raw:
        I = raw['Ik']
        res['C_fail'] = {'I_k': I['Ik'], 'I_k boxes': I['boxes'], 'I_k tail bound': (0.0, I['tail']),
                         'int_K W(k) dk': I['Wtot'], 'const': I['const'], 'I_b': I['Ib'], 'C_fail^{B,K}': I['C_fail']}
    return res


def _walk(d, f):
    if isinstance(d, dict):
        return {k: _walk(v, f) for k, v in d.items()}
    if isinstance(d, str):
        return d
    return f(d)


def document(raw):
    der = derived(raw)
    return {
        'object': PACKET,
        'scientific_effect': 'NONE',
        'certified': True,
        'arithmetic': 'binary64 interval arithmetic, outward one-ulp widening after every operation; published '
                      'intervals widened by %g relatively and rounded outward to %d significant digits' % (MARGIN, DIGITS),
        'parameters': {'k': list(KS), 'tol3': TOL3, 'tol4': TOL4, 'box_half_width_sigma': L_BOX, 'initial_cells': N0,
                       'initial_k_cells': NK0, 'k_split_scale': SK, 'k_elementary_level': BX.KLEVEL},
        'leaves': raw['leaves'],
        'results': _walk(der, pub),
    }


def compare(doc, raw):
    """Replay check: every replayed interval inside the published one, not looser by more than the margin."""
    der = derived(raw)
    bad = []

    def rec(p, r, path):
        if isinstance(r, dict):
            if sorted(p) != sorted(r):
                bad.append(('/'.join(path), 'keys', sorted(p), sorted(r)))
                return
            for key in r:
                rec(p[key], r[key], path + [key])
        elif isinstance(r, str):
            if p != r:
                bad.append(('/'.join(path), p, r))
        else:
            if not contains_pub(p, r) or not not_looser(p, r):
                bad.append(('/'.join(path), p, r))
    rec(doc['results'], der, [])
    if doc['leaves'] != raw['leaves']:
        bad.append(('leaves', doc['leaves'], raw['leaves']))
    return bad


# ================================================================ self-test (pure-Python Gauss-Legendre references)
def _gl(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for j in range(2, n + 1):
                p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(x)
        ws.append(2.0 / ((1 - x * x) * dp * dp))
    return xs, ws


def _xb_f(B, T):
    xm = -B if B < 0 else B / 2.0
    return xm if T <= 0 else BX._newton_big(B, T, xm)


def _xm_f(B, T):
    b = BX.xmid(B, T)
    return 0.5 * (b[0] + b[1])


def _H_f(B, T):
    x = _xb_f(B, T)
    return abs(B) ** 3 + 4 * x ** 3 - 3 * B * B * x


def _V_f(B, T):
    x = _xb_f(B, T)
    return -3 * B * (2 * x - B) * (x + B)


def _H2_f(B, T):
    if B >= 0 or T >= abs(B) ** 3 / 2:
        return 0.0
    x = _xm_f(B, T)
    return abs(B) ** 3 + 4 * x ** 3 - 3 * B * B * x


def _ref3(box, k, f, n=12):
    xs, ws = _gl(n)
    var = (2.0 / k, 2.0, 6.0 * k)
    pts = []
    for (l, h), v in zip(box, var):
        pts.append([(0.5 * (h - l) * x + 0.5 * (h + l),
                     0.5 * (h - l) * w * math.exp(-(0.5 * (h - l) * x + 0.5 * (h + l)) ** 2 / (2 * v)) / math.sqrt(2 * math.pi * v))
                    for x, w in zip(xs, ws)])
    tot = 0.0
    for a, wa in pts[0]:
        for be, wb in pts[1]:
            B = be - a * a / 12.0
            d = -a * be / 4.0 + a ** 3 / 72.0
            for c, wc in pts[2]:
                u = c + d
                tot += wa * wb * wc * f(B, 3 * u * u)
    return tot


def _ref4(box, n=10):
    xs, ws = _gl(n)
    var = (2.0, 2.0, 6.0)
    pts = []
    for (l, h), v in zip(box[:3], var):
        pts.append([(0.5 * (h - l) * x + 0.5 * (h + l),
                     0.5 * (h - l) * w * math.exp(-(0.5 * (h - l) * x + 0.5 * (h + l)) ** 2 / (2 * v)) / math.sqrt(2 * math.pi * v))
                    for x, w in zip(xs, ws)])
    l, h = box[3]
    kp = [(0.5 * (h - l) * x + 0.5 * (h + l), 0.5 * (h - l) * w) for x, w in zip(xs, ws)]
    tot = 0.0
    for k, wk in kp:
        Wk = wk * 3 * k ** (1.0 / 3.0) * math.exp(-12 * k * k)
        sk = math.sqrt(k)
        for a, wa in pts[0]:
            for be, wb in pts[1]:
                B = be - a * a / (12 * k)
                for c, wc in pts[2]:
                    u = sk * c - a * be / (4 * sk) + a ** 3 / (72 * k * sk)
                    tot += Wk * wa * wb * wc * _H_f(B, 3 * u * u)
    return tot


SELFTEST3 = [   # (k, integrand, box in scaled coordinates (a, beta, c)); boxes on one side of u = 0
    (0.5, 'V', ((0.30, 0.55), (-1.20, -0.95), (0.80, 1.10))),
    (0.5, 'V', ((-2.10, -1.80), (0.40, 0.70), (-1.60, -1.30))),
    (0.5, 'V', ((0.05, 0.25), (0.90, 1.20), (2.00, 2.30))),
    (0.5, 'H', ((1.00, 1.30), (-0.60, -0.30), (0.30, 0.60))),
    (1.0, 'V', ((0.10, 0.35), (-2.00, -1.70), (0.20, 0.45))),
    (1.0, 'H', ((-0.80, -0.55), (0.10, 0.40), (-2.60, -2.30))),
    (2.0, 'V', ((0.40, 0.60), (-0.90, -0.60), (3.00, 3.40))),
    (0.5, 'H2', ((0.20, 0.40), (-2.40, -2.15), (0.60, 0.80))),      # inside the support
    (1.0, 'H2', ((-0.30, -0.10), (-3.00, -2.70), (-1.20, -0.95))),   # inside the support
    (0.5, 'H2', ((0.10, 0.30), (-1.30, -1.10), (0.60, 0.85))),      # meets the support boundary
    (0.5, 'V', ((0.30, 0.32), (-1.00, -0.98), (0.50, 1.50))),       # elongated in c: the w-curvature dominates
    (1.0, 'H', ((0.30, 0.32), (0.40, 0.42), (1.00, 2.00))),
    (0.5, 'H2', ((0.20, 0.22), (-2.40, -2.38), (0.20, 0.90))),
]
SELFTEST4 = [
    ((0.40, 0.70), (-1.20, -0.90), (1.00, 1.40), (0.5, 0.5 + 3 * 2.0 ** -7)),
    ((-1.50, -1.20), (0.50, 0.80), (-2.00, -1.60), (0.5 + 3 * 2.0 ** -6, 0.5 + 3 * 2.0 ** -5)),
]


def selftest(mutant=None, log=print):
    """Every box enclosure (and its first- and second-order parts separately) must contain a high-order floating-point
    Gauss-Legendre value; the k-moments must contain Gauss-Legendre values.  Returns a list of failures."""
    BX.MUTANT = mutant
    fails = []
    for k, which, box in SELFTEST3:
        S = sig3(k)
        Ma, Mb, Mc = BX.Moments(S[0][0], S[0][1], 6), BX.Moments(S[1][0], S[1][1], 2), BX.Moments(S[2][0], S[2][1], 2)
        if which == 'H2':
            I, I1, I2 = BX.H2_box3(box, Ma, Mb, Mc, parts=True)
            ref = _ref3(box, k, _H2_f, 16)
            slack = 1e-6 * abs(ref) + 1e-15        # the zero extension is only C^1 at the support boundary
        else:
            try:
                I, I1, I2 = BX.big_box3(box, Ma, Mb, Mc, with_H=(which == 'H'), parts=True)
            except RuntimeError as e:
                fails.append((which, k, box, 'raised: %s' % e))
                continue
            ref = _ref3(box, k, _H_f if which == 'H' else _V_f)
            slack = 1e-9 * abs(ref) + 1e-15
        for name, J in (('I', I), ('I1', I1), ('I2', I2)):
            if J is not None and not (J[0] - slack <= ref <= J[1] + slack):
                fails.append((which, k, box, name, J, ref))
        if I2 is None:
            fails.append((which, k, box, 'no second-order enclosure'))
    S = sig3(1.0)
    Ma, Mb, Mc = BX.Moments(S[0][0], S[0][1], 6), BX.Moments(S[1][0], S[1][1], 2), BX.Moments(S[2][0], S[2][1], 2)
    elem = {}
    for box in SELFTEST4:
        k0, k1 = box[3]
        w = (BX.K_HI - BX.K_LO) / 2 ** BX.KLEVEL
        i0, i1 = round((k0 - BX.K_LO) / w), round((k1 - BX.K_LO) / w)
        Km = _partial_kmoments(i0, i1)              # elementary k-moments of the needed cells only
        try:
            I, I1, I2 = BX.H_box4(box, Ma, Mb, Mc, Km, parts=True)
        except RuntimeError as e:
            fails.append(('H4', box, 'raised: %s' % e))
            continue
        ref = _ref4(box)
        slack = 1e-9 * abs(ref) + 1e-15
        for name, J in (('I', I), ('I1', I1), ('I2', I2)):
            if J is not None and not (J[0] - slack <= ref <= J[1] + slack):
                fails.append(('H4', box, name, J, ref))
        if I2 is None:
            fails.append(('H4', box, 'no second-order enclosure'))
        xs, ws = _gl(20)
        K = Km.get(k0, k1)
        for p in (BX.PMIN, 0, BX.PMAX):
            refk = sum(0.5 * (k1 - k0) * wq * 3 * kk ** (1 / 3 + p / 2) * math.exp(-12 * kk * kk)
                       for kk, wq in ((0.5 * (k1 - k0) * x + 0.5 * (k1 + k0), wq) for x, wq in zip(xs, ws)))
            if not (K[p][0] * (1 - 1e-12) <= refk <= K[p][1] * (1 + 1e-12)):
                fails.append(('K', box[3], p, K[p], refk))
    log('self-test: %d boxes, %d failures' % (len(SELFTEST3) + len(SELFTEST4), len(fails)))
    return fails


def _partial_kmoments(i0, i1, nsub=24):
    """KMoments object whose elementary cells i0..i1-1 are computed (others are never touched)."""
    n = 2 ** BX.KLEVEL
    width = (BX.K_HI - BX.K_LO) / n
    elem = [None] * n
    for i in range(i0, i1):
        k0 = BX.K_LO + width * i
        acc = {p: (0.0, 0.0) for p in range(BX.PMIN, BX.PMAX + 1)}
        prev = BX.kweights(k0)
        for j in range(nsub):
            l = k0 + width * j / nsub
            r = k0 + width * (j + 1) / nsub
            h = (dn(r - l), up(r - l))
            mid = BX.kweights(0.5 * (l + r))
            fr = BX.kweights(r)
            for p in acc:
                lo = mul(h, mid[p])[0]
                hi = mul(h, scal(0.5, add(prev[p], fr[p])))[1]
                acc[p] = (dn(acc[p][0] + lo), up(acc[p][1] + hi))
            prev = fr
        elem[i] = acc
    return BX.KMoments(elem)


# ================================================================ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--controls', action='store_true')
    ap.add_argument('--mutant', default=None)
    ap.add_argument('--procs', type=int, default=os.cpu_count() or 2)
    a = ap.parse_args()
    path = os.path.join(HERE, 'RESULTS.json')
    if a.controls:
        import controls
        controls.main()
        return 0
    fails = selftest(a.mutant)
    if fails:
        for f in fails[:10]:
            print('SELF-TEST FAILURE', f)
        return 1
    try:
        raw = certify(a.procs, a.mutant)
    except RuntimeError as e:
        print('CERTIFICATE FAILURE', e)
        return 1
    if a.write:
        doc = document(raw)
        with open(path, 'w') as fh:
            json.dump(doc, fh, indent=1, sort_keys=False)
            fh.write('\n')
        print('wrote', path)
        return 0
    if a.check:
        with open(path) as fh:
            doc = json.load(fh)
        bad = compare(doc, raw)
        if bad:
            for b in bad[:20]:
                print('MISMATCH', b)
            return 1
        print(json.dumps({'object': PACKET, 'check': 'passed', 'scientific_effect': 'NONE'}))
        return 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
