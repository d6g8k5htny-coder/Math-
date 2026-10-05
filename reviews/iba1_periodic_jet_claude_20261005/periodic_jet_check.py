"""Exact-periodic contact-jet covariances for the SIDE24 family (main#252, IBA-20261003-P1, item 2).

Standard library only.  The field is centred, variance one, with covariance

    K_L(z) = prod_i q_L(z_i),   q_L(t) = theta_L(t) / theta_L(0),
    theta_L(t) = sum_{n in Z} exp(-(t + L n)^2 / 2),

so every derivative tensor at 0 is a polynomial in q2 = q_L''(0), q4 = q_L''''(0), q6 = q_L^(6)(0).
With spectral moments m2 = -q2, m4 = q4, m6 = -q6 of one coordinate and cumulants
k2 = m2, k4 = m4 - 3 m2^2, k6 = m6 - 15 m4 m2 + 30 m2^3, the moment E[prod <xi, v_k>] is the sum over
partitions into even blocks of k2 <v_a, v_b> (pairs) and k_{2j} sum_i prod v_{k,i} (blocks of size 4, 6).
Cov(d_A f, d_B f) = (-1)^|B| (-1)^((|A|+|B|)/2) E[prod_{A+B} <xi, v>] for |A|+|B| even, else 0.

Usage:  python3 -B -S periodic_jet_check.py [--mutant M1|M2|M3|M4]
Normal run prints RESULTS.json and exits 0.  A mutant must make a check fail (exit 1):
  M1  isotropic surrogate for the fourth- and sixth-order tensors (q4 = 3 q2^2, q6 = -15 (-q2)^3);
  M2  transverse Hessian block not conditioned on V = 0;
  M3  prefactor of (15.2) divided by 12;
  M4  raw upper-triangle trace of the transverse block (frame-dependent; finding PJ-A-001).
An unknown mutant label exits 2.
"""
import decimal
import fractions
import json
import sys
from decimal import Decimal as D

PREC = 270
decimal.getcontext().prec = PREC
MUTANT = None


def pi_dec():
    # Machin: pi = 16 atan(1/5) - 4 atan(1/239)
    def atan_inv(x):
        x = D(x)
        x2 = x * x
        term = D(1) / x
        total = term
        k = 1
        eps = D(10) ** (-(PREC + 5))
        while True:
            term /= -x2
            add = term / (2 * k + 1)
            if abs(add) < eps:
                break
            total += add
            k += 1
        return total
    return 16 * atan_inv(5) - 4 * atan_inv(239)


PI = pi_dec()


def cos_sin(theta):
    theta = D(theta)
    eps = D(10) ** (-(PREC + 5))
    c, s = D(1), theta
    tc, ts = D(1), theta
    k = 1
    while True:
        tc = -tc * theta * theta / ((2 * k - 1) * (2 * k))
        ts = -ts * theta * theta / ((2 * k) * (2 * k + 1))
        if abs(tc) < eps and abs(ts) < eps:
            break
        c += tc
        s += ts
        k += 1
    return c, s


def he(j, x):
    # probabilists' Hermite polynomials He_0, He_2, He_4, He_6
    x2 = x * x
    return {0: D(1), 2: x2 - 1, 4: x2 * x2 - 6 * x2 + 3, 6: x2 ** 3 - 15 * x2 * x2 + 45 * x2 - 15}[j]


def q_derivatives(L):
    """(q2, q4, q6, tail): image sums with a rigorous tail bound `tail` on every theta_j."""
    if L is None:
        return D(-1), D(3), D(-15), D(0)
    L = D(L)
    target = D(PREC + 30) * D(10).ln()
    N = 1
    while (L * N) ** 2 / 2 < target:
        N += 1
    x = L * (N + 1)
    assert x >= 10
    # for x >= 10: |He_j(x)| <= 2 x^j (j <= 6) and x^6 e^{-x^2/2} decreases with ratio <= 1/2 per
    # step n -> n+1, so the two-sided tail is at most 2 * 2 * (2 x^6 e^{-x^2/2}).
    tail = 8 * x ** 6 * (-(x * x) / 2).exp()
    th = {}
    for j in (0, 2, 4, 6):
        s = he(j, D(0))
        for n in range(1, N + 1):
            y = L * n
            s += 2 * he(j, y) * (-(y * y) / 2).exp()
        th[j] = s
    q2, q4, q6 = th[2] / th[0], th[4] / th[0], th[6] / th[0]
    if MUTANT == 'M1':
        q4 = 3 * q2 * q2          # isotropic surrogate for the fourth-order tensor
        q6 = -15 * (-q2) ** 3      # and for the sixth-order tensor
    return q2, q4, q6, tail


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def even_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    n = len(rest)
    for size in (1, 3, 5):
        if size > n:
            break
        for combo in _combinations(range(n), size):
            block = [first] + [rest[i] for i in combo]
            remaining = [rest[i] for i in range(n) if i not in combo]
            for p in even_partitions(remaining):
                yield [block] + p


def _combinations(seq, r):
    seq = list(seq)
    if r == 0:
        yield ()
        return
    for i in range(len(seq)):
        for tail in _combinations(seq[i + 1:], r - 1):
            yield (seq[i],) + tail


def moment(vs, k):
    """E[prod <xi, v>] for the product spectral law with cumulants k = {2: k2, 4: k4, 6: k6}."""
    if len(vs) % 2:
        return D(0)
    total = D(0)
    for part in even_partitions(list(range(len(vs)))):
        term = D(1)
        for block in part:
            if len(block) == 2:
                term *= k[2] * dot(vs[block[0]], vs[block[1]])
            else:
                s = D(0)
                for i in range(len(vs[0])):
                    pr = D(1)
                    for b in block:
                        pr *= vs[b][i]
                    s += pr
                term *= k[len(block)] * s
            if term == 0:
                break
        total += term
    return total


def cov(A, B, k):
    p, q = len(A), len(B)
    if (p + q) % 2:
        return D(0)
    sign = (-1) ** q * (-1) ** ((p + q) // 2)
    return sign * moment(list(A) + list(B), k)


def cholesky_pivots(M):
    n = len(M)
    Lm = [[D(0)] * n for _ in range(n)]
    piv = []
    for i in range(n):
        for j in range(i + 1):
            s = M[i][j] - sum(Lm[i][t] * Lm[j][t] for t in range(j))
            if i == j:
                piv.append(s)
                if s <= 0:
                    return piv, None
                Lm[i][i] = s.sqrt()
            else:
                Lm[i][j] = s / Lm[j][j]
    return piv, Lm


def det_pd(M):
    piv, Lm = cholesky_pivots(M)
    assert Lm is not None, 'not positive definite'
    out = D(1)
    for p in piv:
        out *= p
    return out


def solve(M, b):
    n = len(M)
    a = [row[:] + [b[i]] for i, row in enumerate(M)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(a[r][c]))
        a[c], a[piv] = a[piv], a[c]
        for r in range(n):
            if r != c:
                f = a[r][c] / a[c][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [a[i][n] / a[i][i] for i in range(n)]


def schur(Saa, Sav, Svv):
    # Saa - Sav Svv^{-1} Sva
    cols = [solve(Svv, [Sav[i][j] for j in range(len(Svv))]) for i in range(len(Saa))]
    return [[Saa[i][j] - dot(Sav[i], cols[j]) for j in range(len(Saa))] for i in range(len(Saa))]


def frobenius_trace(S, idx):
    # trace of the conditional covariance of A as a symmetric matrix (Frobenius inner product): an
    # off-diagonal entry counts twice, so the value does not depend on the transverse frame; the raw
    # upper-triangle sum would (main#252 / Math-#297 finding PJ-A-001)
    if MUTANT == 'M4':
        return sum(S[a][a] for a in range(len(idx)))      # raw upper-triangle trace
    return sum(S[a][a] * (1 if i == j else 2) for a, (i, j) in enumerate(idx))


def frame(u):
    d = len(u)
    basis = [u]
    for e in range(d):
        v = [D(1) if i == e else D(0) for i in range(d)]
        for b in basis:
            c = dot(v, b)
            v = [x - c * y for x, y in zip(v, b)]
        nv = dot(v, v)
        if nv > D('1e-20'):
            nn = nv.sqrt()
            basis.append([x / nn for x in v])
        if len(basis) == d:
            break
    return basis


def normalize(v):
    v = [D(x) for x in v]
    n = dot(v, v).sqrt()
    return [x / n for x in v]


def jet_data(u, k, w=None):
    fr = frame(u)
    if w is None:
        w = fr[1:]
    fr = [u] + list(w)
    m = len(w)
    G = [[x] for x in fr]
    t = [u, u, u]
    V = [[u, u]] + [[u, wj] for wj in w]
    idx = [(i, j) for i in range(m) for j in range(i, m)]
    A = [[w[i], w[j]] for i, j in idx]
    S_GG = [[cov(a, b, k) for b in G] for a in G]
    c_tG = [cov(t, b, k) for b in G]
    var_t = cov(t, t, k)
    tau2 = var_t - dot(c_tG, solve(S_GG, c_tG))
    S_VV = [[cov(a, b, k) for b in V] for a in V]
    S_AA = [[cov(a, b, k) for b in A] for a in A]
    S_AV = [[cov(a, b, k) for b in V] for a in A]
    S_AgV = schur(S_AA, S_AV, S_VV)
    if MUTANT == 'M2':
        S_AgV = S_AA                # transverse block not conditioned on V = 0
    even = [[]] + V + A
    odd = G + [t]
    S_even = [[cov(a, b, k) for b in even] for a in even]
    S_odd = [[cov(a, b, k) for b in odd] for a in odd]
    pe, _ = cholesky_pivots(S_even)
    po, _ = cholesky_pivots(S_odd)
    pa, _ = cholesky_pivots(S_AgV)
    return {
        'det_G': det_pd(S_GG), 'det_V': det_pd(S_VV), 'tau2': tau2,
        'det_AgV': det_pd(S_AgV), 'tr_AgV': frobenius_trace(S_AgV, idx),
        'S_AgV': S_AgV, 'min_pivot': min(pe + po + pa),
    }


def directions(d):
    if d == 2:
        out = []
        for j in range(16):
            c, s = cos_sin(2 * PI * j / 16)
            out.append([c, s])
        return out
    raw = {
        3: [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1),
            (1, 2, 3), (3, -1, 2), (2, 5, -7)],
        4: [(1, 0, 0, 0), (0, 0, 0, 1), (1, 1, 0, 0), (1, 1, 1, 0), (1, 1, 1, 1),
            (1, 2, 3, 4), (4, -3, 2, -1), (2, 7, -1, 5)],
    }[d]
    return [normalize(v) for v in raw]


def fmt(x, digits=25):
    return format(x, '.%de' % (digits - 1)) if x != 0 else '0'


def stirling_gamma(z):
    # Gamma(z) for real z > 0 by shifting to z + S and the Stirling series with Bernoulli terms.
    S = 200
    B = bernoulli(60)
    zz = z + S
    lng = (zz - D('0.5')) * zz.ln() - zz + (2 * PI).ln() / 2
    for n in range(1, 31):
        b = B[2 * n]
        lng += D(b.numerator) / D(b.denominator) / (2 * n * (2 * n - 1) * zz ** (2 * n - 1))
    g = lng.exp()
    for i in range(S):
        g /= (z + i)
    return g


def bernoulli(n):
    A = [fractions.Fraction(0)] * (n + 1)
    Bs = []
    for m in range(n + 1):
        A[m] = fractions.Fraction(1, m + 1)
        for j in range(m, 0, -1):
            A[j - 1] = j * (A[j - 1] - A[j])
        Bs.append(A[0])
    return Bs


def coefficient_d2(k, N):
    """(15.2) for d = 2 by the trapezoid rule on N equally spaced directions."""
    pref = stirling_gamma(D(7) / 6) / (D(24) ** (D(1) / 3) * PI.sqrt())
    if MUTANT == 'M3':
        pref = pref / 12           # a lost factor 12 in the gamma/Jacobian prefactor
    total = D(0)
    for j in range(N):
        c, s = cos_sin(2 * PI * j / N)
        jd = jet_data([c, s], k)
        pG = 1 / (2 * PI * jd['det_G'].sqrt())
        pV = 1 / (2 * PI * jd['det_V'].sqrt())
        Du = jd['S_AgV'][0][0] / 2
        total += pG * pV * jd['tau2'] ** (D(2) / 3) * Du
    return pref * total * (2 * PI / N)


def main():
    global MUTANT
    if len(sys.argv) == 3 and sys.argv[1] == '--mutant':
        if sys.argv[2] not in ('M1', 'M2', 'M3', 'M4'):
            print('unknown mutant'); sys.exit(2)
        MUTANT = sys.argv[2]
    elif len(sys.argv) != 1:
        print(__doc__); sys.exit(2)

    checks = {}
    out = {'object': 'CL-IBA1-ITEM2-PERIODIC-JET-20261005-v1', 'precision_digits': PREC,
           'scientific_effect': 'NONE', 'cases': {}}

    # R1: the nonperiodic reference reproduces the published reference jet (side24_v1 section 1).
    q2, q4, q6, _ = q_derivatives(None)
    kref = {2: -q2, 4: q4 - 3 * q2 * q2, 6: -q6 - 15 * q4 * (-q2) + 30 * (-q2) ** 3}
    jr = jet_data([D(1), D(0)], kref)
    checks['R1_reference_jet'] = (jr['det_G'] == 1 and jr['det_V'] == 3 and jr['tau2'] == 6
                                  and abs(jr['S_AgV'][0][0] - D(8) / 3) < D('1e-250'))
    jr3 = jet_data(normalize((1, 2, 3)), kref)
    checks['R1_reference_d3_trace_frobenius'] = abs(jr3['tr_AgV'] - D(22) / 3) < D('1e-250')

    Ls = [('24', D(24)), ('8', D(8)), ('2pi', 2 * PI), ('4', D(4)), ('3', D(3))]
    aniso = {}
    for name, L in Ls:
        q2, q4, q6, tail = q_derivatives(L)
        m2, m4, m6 = -q2, q4, -q6
        k = {2: m2, 4: m4 - 3 * m2 * m2, 6: m6 - 15 * m4 * m2 + 30 * m2 ** 3}
        case = {'q2': fmt(q2), 'q4': fmt(q4), 'q6': fmt(q6), 'theta_tail_bound': fmt(tail, 3),
                'k4_over_k2sq': fmt(k[4] / (k[2] * k[2]), 6), 'dims': {}}
        for d in (2, 3, 4):
            dirs = directions(d)
            data = [jet_data(u, k) for u in dirs]
            minpiv = min(x['min_pivot'] for x in data)
            dev = D(0)
            for key in ('det_G', 'det_V', 'tau2', 'det_AgV', 'tr_AgV'):
                vals = [x[key] for x in data]
                base = vals[0]
                dev = max(dev, max(abs(v / base - 1) for v in vals))
            case['dims'][str(d)] = {'directions': len(dirs), 'min_cholesky_pivot': fmt(minpiv, 8),
                                    'max_relative_anisotropy': fmt(dev, 6)}
            checks['R2_positive_L%s_d%d' % (name, d)] = minpiv > 0
            aniso[(name, d)] = dev
        out['cases'][name] = case

    # R3: anisotropy at L = 24 is nonzero but far below side24_v1's periodization bound 1e-106;
    # at L = 4 it is of order one-tenth and must be seen (an isotropic surrogate is rejected).
    checks['R3_L24_anisotropy_measured'] = all(D('1e-130') < aniso[('24', d)] < D('1e-106') for d in (2, 3, 4))
    checks['R3_L4_anisotropy_visible'] = all(aniso[('4', d)] > D('1e-3') for d in (2, 3, 4))

    # R6: at fixed u = e_1, rotating the transverse frame by (cos, sin) = (3/5, 4/5) leaves every invariant
    # unchanged (L = 4, d = 3 and d = 4), including the Frobenius trace.
    q2, q4, q6, _ = q_derivatives(D(4))
    m2, m4, m6 = -q2, q4, -q6
    k4L = {2: m2, 4: m4 - 3 * m2 * m2, 6: m6 - 15 * m4 * m2 + 30 * m2 ** 3}
    rot = {}
    for d in (3, 4):
        u = [D(1)] + [D(0)] * (d - 1)
        base = jet_data(u, k4L)
        e = [[D(1) if i == j else D(0) for i in range(d)] for j in range(1, d)]
        cs, sn = D(3) / 5, D(4) / 5
        w = [[cs * a - sn * b for a, b in zip(e[0], e[1])], [sn * a + cs * b for a, b in zip(e[0], e[1])]] + e[2:]
        turned = jet_data(u, k4L, w)
        dev = max(abs(turned[key] - base[key]) for key in ('det_G', 'det_V', 'tau2', 'det_AgV', 'tr_AgV'))
        rot[str(d)] = fmt(dev, 3)
        checks['R6_transverse_frame_invariance_d%d' % d] = dev < D('1e-250')
    out['transverse_rotation_max_abs_change_L4'] = rot

    # R4: c_{2,24} by directional quadrature lies in side24_v1's published interval and equals the
    # reference closed form to far below that interval's width.
    q2, q4, q6, _ = q_derivatives(D(24))
    m2, m4, m6 = -q2, q4, -q6
    k24 = {2: m2, 4: m4 - 3 * m2 * m2, 6: m6 - 15 * m4 * m2 + 30 * m2 ** 3}
    c24_8 = coefficient_d2(k24, 8)
    c24_16 = coefficient_d2(k24, 16)
    lo, hi = D('0.07340691930603427103'), D('0.07340691930603427104')
    cref = coefficient_d2(kref, 4)
    checks['R4_c224_in_side24_interval'] = lo < c24_8 < hi and lo < c24_16 < hi
    checks['R4_c224_equals_reference'] = abs(c24_16 / cref - 1) < D('1e-100')
    out['c_2'] = {'reference': fmt(cref, 40), 'L24_N8': fmt(c24_8, 40), 'L24_N16': fmt(c24_16, 40),
                  'L24_relative_to_reference': fmt(c24_16 / cref - 1, 6),
                  'side24_v1_interval': [str(lo), str(hi)]}

    # R5 (diagnostic): c_{2,L} for smaller L, trapezoid on 256 and 512 directions.
    diag = {}
    for name, L in Ls[1:]:
        q2, q4, q6, _ = q_derivatives(L)
        m2, m4, m6 = -q2, q4, -q6
        kk = {2: m2, 4: m4 - 3 * m2 * m2, 6: m6 - 15 * m4 * m2 + 30 * m2 ** 3}
        a, b = coefficient_d2(kk, 256), coefficient_d2(kk, 512)
        diag[name] = {'N256': fmt(a, 20), 'N512': fmt(b, 20), 'abs_diff': fmt(abs(a - b), 3),
                      'ratio_to_reference': fmt(b / cref, 12)}
        checks['R5_quadrature_settled_L%s' % name] = abs(a - b) < D('1e-12') * b
    out['c_2_diagnostic_small_L'] = diag
    out['checks'] = {key: bool(v) for key, v in sorted(checks.items())}
    out['passed'] = all(checks.values())
    print(json.dumps(out, indent=1, sort_keys=True))
    sys.exit(0 if out['passed'] else 1)


if __name__ == '__main__':
    main()
