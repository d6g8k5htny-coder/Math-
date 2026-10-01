"""Floating controls for CL-C2-EXACT-20261001.  These are not part of the certificate.

1. Finite-r kernel, pointwise.  The fixed-cone surrogate A~_r(b, k) (NOTE.md section 1) is computed at finite r
   directly from the closed-form kernel derivatives at the displaced points M = -r e1/2, S = r e1/2, 0, without Taylor
   jets or series: D^g K(z) = prod_i (-1)^(g_i) He_(g_i)(z_i) e^(-z_i^2/2), conditioning in Decimal (60 digits), then
   floating Isserlis and quadrature.  The Richardson combination
   2 D(r) - D(2r), D(r) = (A~_r - A_0)/r^2, must approach the exact A_2(b, k) of exact.py at the rate O(r^2)
   (error ratio 4 per halving of r).
2. Math-#216's floating values (head 4f0927f, NOTE.md section 0 table and README) against the closed forms.

Run: python3 -B controls.py (pure Python, a few seconds)."""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import exact as X

getcontext().prec = 60
DEC = Decimal


# ------------------------------------------------------------------------------------------- finite-r kernel
def he(n, x):
    a, b = DEC(1), x
    if n == 0:
        return a
    for k in range(1, n):
        a, b = b, x * b - k * a
    return b


def dK(g, z):
    out = DEC(1)
    for gi, zi in zip(g, z):
        out *= (-1) ** gi * he(gi, zi) * (-(zi * zi) / 2).exp()
    return out


def cov(u, w):
    """u, w: lists of (coef, point, alpha)"""
    tot = DEC(0)
    for cu, xu, au in u:
        for cw, xw, aw in w:
            z = tuple(p - q for p, q in zip(xu, xw))
            tot += cu * cw * (-1) ** sum(aw) * dK(tuple(p + q for p, q in zip(au, aw)), z)
    return tot


def solve(A, B):
    """A^-1 B (Decimal Gauss-Jordan), B a list of columns"""
    n = len(A)
    M = [A[i][:] + [col[i] for col in B] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(M[i][c]))
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [x / piv for x in M[c]]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[c])]
    return [[M[i][n + j] for i in range(n)] for j in range(len(B))]


def det(A):
    n = len(A)
    M = [row[:] for row in A]
    out = DEC(1)
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(M[i][c]))
        if p != c:
            M[c], M[p] = M[p], M[c]
            out = -out
        out *= M[c][c]
        for i in range(c + 1, n):
            f = M[i][c] / M[c][c]
            M[i] = [x - f * y for x, y in zip(M[i], M[c])]
    return out


def unit(d, *idx):
    e = [0] * d
    for i in idx:
        e[i] += 1
    return tuple(e)


def structure(d, r):
    r = DEC(r)
    Mp = (-r / 2,) + (DEC(0),) * (d - 1)
    Sp = (r / 2,) + (DEC(0),) * (d - 1)
    O = (DEC(0),) * d
    e0, ex = (0,) * d, unit(d, 0)
    rows = [[(DEC('0.5'), Mp, e0), (DEC('0.5'), Sp, e0)],
            [(-1 / r, Mp, e0), (1 / r, Sp, e0)],
            [(-1 / r, Mp, ex), (1 / r, Sp, ex)],
            [(6 / r ** 2, Mp, ex), (6 / r ** 2, Sp, ex), (12 / r ** 3, Mp, e0), (-12 / r ** 3, Sp, e0)]]
    for t in range(1, d):
        ey = unit(d, t)
        rows += [[(DEC('0.5'), Mp, ey), (DEC('0.5'), Sp, ey)], [(-1 / r, Mp, ey), (1 / r, Sp, ey)]]
    forms = {}
    for nm, pt in (('M', Mp), ('S', Sp)):
        for i in range(d):
            for j in range(i, d):
                forms[(nm, i, j)] = [(DEC(1), pt, unit(d, i, j))]
    trans = []
    for i in range(1, d):
        for j in range(i, d):
            forms[('T', i, j)] = [(DEC(1), O, unit(d, i, j))]
            trans.append(('T', i, j))
    p = len(rows)
    Sm = [[cov(a, b) for b in rows] for a in rows]
    names = list(forms)
    CFP = {u: [cov(forms[u], row) for row in rows] for u in names}
    G = {u: col for u, col in zip(names, solve(Sm, [CFP[u] for u in names]))}     # S^-1 C_PF -> mean coefficients
    C = {(u, w): cov(forms[u], forms[w]) - sum(G[u][q] * CFP[w][q] for q in range(p)) for u in names for w in names}
    Sinv_cols = solve(Sm, [[DEC(int(i == j)) for i in range(p)] for j in range(p)])
    return {'p': p, 'G': G, 'C': C, 'Sinv': Sinv_cols, 'detS': det(Sm), 'names': names, 'trans': trans, 'r': r}


def gl(n, a, b):
    """Gauss-Legendre nodes (floating, Newton) on [a, b]"""
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(0.5 * (a + b) + 0.5 * (b - a) * x)
        ws.append(0.5 * (b - a) * 2 / ((1 - x * x) * dp * dp))
    return list(zip(xs, ws))


# small float polynomials in the cone variables: dict (i, j) -> coefficient
def pmul(a, b):
    out = {}
    for e1, c1 in a.items():
        for e2, c2 in b.items():
            e = (e1[0] + e2[0], e1[1] + e2[1])
            out[e] = out.get(e, 0.0) + c1 * c2
    return out


def detdet_poly(d, aff, cp):
    """E[det H_M det H_S | T] as a float polynomial in the cone variables, by Isserlis"""
    import itertools
    tot = {}
    for pp in itertools.permutations(range(d)):
        for qq in itertools.permutations(range(d)):
            fac = [('M', min(i, pp[i]), max(i, pp[i])) for i in range(d)] + \
                  [('S', min(i, qq[i]), max(i, qq[i])) for i in range(d)]
            sg = X.perm_sign(pp) * X.perm_sign(qq)
            for mt in X.matchings(list(range(2 * d))):
                used = set(i for pr in mt for i in pr)
                c = float(sg)
                for (i, j) in mt:
                    c *= cp[(fac[i], fac[j])]
                if c == 0.0:
                    continue
                poly = {(0, 0): c}
                for i in range(2 * d):
                    if i not in used:
                        poly = pmul(poly, aff[fac[i]])
                for e, v in poly.items():
                    tot[e] = tot.get(e, 0.0) + v
    return tot


def A_finite(d, st, b, k, nq=40):
    """A~_r(b, k) = -12 pi_r(v) E[det H_M det H_S 1{T < 0} | U_r = v] / r^2 at finite r (the fixed-cone surrogate)"""
    r = st['r']
    p = st['p']
    v = [DEC(b) - DEC(k) * r ** 3 / 2, -DEC(k) * r * r, DEC(0), 12 * DEC(k)] + [DEC(0)] * (p - 4)
    q = sum(v[i] * st['Sinv'][j][i] * v[j] for i in range(p) for j in range(p))
    pi_r = float((2 * DEC(math.pi)) ** (-DEC(p) / 2) / st['detS'].sqrt() * (-q / 2).exp())
    names, trans = st['names'], st['trans']
    mean = {u: sum(st['G'][u][j] * v[j] for j in range(p)) for u in names}
    hn = [u for u in names if u not in trans]
    if d == 1:
        cp = {(u, w): float(st['C'][(u, w)]) for u in hn for w in hn}
        aff = {u: {(0, 0): float(mean[u])} for u in hn}
        Z = detdet_poly(d, aff, cp)[(0, 0)]
        return -12 * pi_r * Z / float(r) ** 2
    CTT = [[st['C'][(x, y)] for y in trans] for x in trans]
    nt = len(trans)
    Bc = solve(CTT, [[st['C'][(u, trans[i])] for i in range(nt)] for u in hn])     # columns: C_TT^-1 C_Tu
    B = {u: col for u, col in zip(hn, Bc)}
    cp = {(u, w): float(st['C'][(u, w)] - sum(B[u][i] * st['C'][(trans[i], w)] for i in range(nt))) for u in hn for w in hn}
    mT = [mean[t] for t in trans]
    # cone variables (x1, x2): d = 2: a = x1; d = 3: diag(x1, x2)
    aff = {}
    for u in hn:
        base = mean[u] - sum(B[u][i] * mT[i] for i in range(nt))
        if d == 2:
            aff[u] = {(0, 0): float(base), (1, 0): float(B[u][0])}
        else:
            aff[u] = {(0, 0): float(base), (1, 0): float(B[u][0]), (0, 1): float(B[u][2])}
    poly = detdet_poly(d, aff, cp)
    CTTinv = solve(CTT, [[DEC(int(i == j)) for i in range(nt)] for j in range(nt)])
    Ci = [[float(CTTinv[j][i]) for j in range(nt)] for i in range(nt)]
    dT = float(det(CTT))
    mTf = [float(x) for x in mT]
    norm = (2 * math.pi) ** (-nt / 2) / math.sqrt(dT)

    def dens(z):
        qq = sum(z[i] * Ci[i][j] * z[j] for i in range(nt) for j in range(nt))
        return norm * math.exp(-qq / 2)
    tot = 0.0
    if d == 2:
        L = 14.0 + abs(b)
        for x, w in gl(nq, -L, 0.0):
            val = sum(c * x ** e[0] for e, c in poly.items())
            tot += w * val * dens([x - mTf[0]])
    else:
        L = 14.0 + abs(b)
        nodes = gl(nq, 0.0, L)
        for s, ws in nodes:
            for t, wt in nodes:
                x1, x2 = -s, -s - t
                val = sum(c * x1 ** e[0] * x2 ** e[1] for e, c in poly.items())
                tot += ws * wt * val * dens([x1 - mTf[0], -mTf[1], x2 - mTf[2]]) * math.pi * t
    return -12 * pi_r * tot / float(r) ** 2


def A_exact(d, data, which, b, k, nq=40):
    """A_which(b, k) from exact.py's polynomial data, evaluated by floating quadrature over the cone"""
    H = data['G'].rcoef(which + 2)
    E = (data['q0'] + data['Q0']) * X.Fr(1, 2)
    const = sum(float(v) * math.pi ** (h / 2) * math.sqrt(m) for (h, m, _), v in data['const'].t.items())

    def ev(poly, x1, x2):
        return sum(float(c) * b ** e[1] * k ** e[2] * x1 ** e[3] * x2 ** e[4] for e, c in poly.t.items())
    if d == 1:
        return const * math.exp(-ev(E, 0, 0)) * ev(H, 0, 0)
    tot = 0.0
    L = 14.0 + abs(b)
    if d == 2:
        for x, w in gl(nq, -L, 0.0):
            tot += w * math.exp(-ev(E, x, 0)) * ev(H, x, 0)
    else:
        nodes = gl(nq, 0.0, L)
        for s, ws in nodes:
            for t, wt in nodes:
                x1, x2 = -s, -s - t
                tot += ws * wt * math.exp(-ev(E, x1, x2)) * ev(H, x1, x2) * t
    return const * tot


QUOTED_216 = {   # Math-#216 head 4f0927f, NOTE.md section 0 table
    1: {'c': '0.110110378959', 'c2': '0.23004458', 'c2/c': '2.089218'},
    2: {'c': '0.073406919306', 'c2': '0.22152441', 'c2/c': '3.017759'},
    3: {'c': '0.041775931841', 'c2': '0.16123405', 'c2/c': '3.859496'},
}


def main():
    res = json.load(open(os.path.join(HERE, 'RESULTS.json')))['values']
    print('1. finite-r kernel against the exact A_2: relative error of 2 D(r) - D(2r) at r = 0.01, 0.005, 0.0025')
    out, bad = [], []
    for d, pts in ((1, [(0.3, 0.7)]), (2, [(0.5, 0.4), (-0.8, 0.9)]), (3, [(0.6, 0.5), (-0.4, 0.3)])):
        data = X.kernel_data(d)
        for b, k in pts:
            A0, A2 = A_exact(d, data, 0, b, k), A_exact(d, data, 2, b, k)
            errs = []
            for r in ('0.01', '0.005', '0.0025'):
                D1 = (A_finite(d, structure(d, r), b, k) - A0) / float(r) ** 2
                D2 = (A_finite(d, structure(d, str(2 * float(r))), b, k) - A0) / (2 * float(r)) ** 2
                errs.append(abs(2 * D1 - D2 - A2) / abs(A2))
            print('   d = %d, (b, k) = (%4.1f, %3.1f): A_2 = %+.10f; errors %.1e, %.1e, %.1e (ratios %.2f, %.2f)'
                  % (d, b, k, A2, errs[0], errs[1], errs[2], errs[0] / errs[1], errs[1] / errs[2]))
            out.append(errs)
            if not (errs[2] < 1e-4 and all(3.0 < errs[i] / errs[i + 1] < 5.0 for i in range(2))):
                bad.append('finite-r control, d = %d, (b, k) = (%g, %g)' % (d, b, k))
    print('2. Math-#216 floating values against the certified enclosures:')
    for d in (1, 2, 3):
        for key, rk in (('c', 'c'), ('c2', 'c2'), ('c2/c', 'c2 / c')):
            q = QUOTED_216[d][key]
            lo, hi = (float(x) for x in res['d=%d' % d][rk])
            mid = 0.5 * (lo + hi)
            half = 0.5 * 10 ** -len(q.split('.')[1])
            print('   d = %d %-5s quoted %-15s certified mid %.13f  |difference| %.1e  (half-unit %.0e)%s'
                  % (d, key, q, mid, abs(float(q) - mid), half, '' if abs(float(q) - mid) < half else '  NOT A ROUNDING'))
            if not abs(float(q) - mid) < half:
                bad.append('#216 value d = %d %s' % (d, key))
    print('controls: %d failures' % len(bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
