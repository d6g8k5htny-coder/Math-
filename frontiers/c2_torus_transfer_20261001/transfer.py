"""CL-C2-TORUS-TRANSFER-20261001: the third-order coefficient c2 on the finite torus, d = 1, 2, 3, every L >= L0 and
every orthonormal frame, against the closed form of frontiers/c2_exact_20261001 (NOTE.md).  Standard library only.

    python3 -B -S transfer.py                 print the bounds
    python3 -B -S transfer.py --write         write RESULTS.json
    python3 -B -S transfer.py --check         recompute everything and compare with RESULTS.json (exit 1 on mismatch)
    python3 -B -S transfer.py --mutant NAME   run --check with a seeded defect (must exit 1)

Pipeline (NOTE.md sections 1-4):
  1. jet covariances of the normalized periodic kernel K_L as balls around the Gaussian ones (Lemma J);
  2. the exact derivation of c2_exact (pin rows, conditioning, Isserlis, exp/det expansion) re-run in ball arithmetic,
     with the full transverse block T = (T11, T22, T12) in d = 3 (no rotation reduction): the r^4 coefficient
     H(b, k, x) of the integrand, the exponent E = (q0 + Q0)/2 and the determinants, as balls (Lemma P);
  3. the finite-part lemma and explicit Gaussian moment bounds for the difference of the two integrands (Lemmas F, G)."""
from fractions import Fraction as Fr
import itertools
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ball import (B, rup, center, radius, mag, exp_up, isqrt_frac_dn, PI_UP, PI_DN)    # noqa: E402
import pseries as P                                                                      # noqa: E402

P.R = 8                       # series exact through r^(R - 3) = r^5; the certificate needs r^4
NR = 4                        # polynomial truncation in r: the r^4 coefficient is the A_2 integrand
VARS = ('r', 'b', 'k', 'x1', 'x2', 'x3')
NV = len(VARS)
ONE = (0,) * NV
MUTANT = None
MUTANTS = ('no-image', 'no-theta', 'drop-ratio', 'eta-half', 'fp-const')
L0S = (10, 12, 16, 24)
HERE = os.path.dirname(os.path.abspath(__file__))


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


# ============================================================================== 1. jet covariances (Lemma J)
def rho_der(g):
    """d^g phi(0) for phi(z) = exp(-|z|^2/2) (exact integer)"""
    return P.rho_der(g)


def he_major(m):
    """coefficients of the majorant He*_m(s) = sum_j m!/(j! (m-2j)! 2^j) s^(m-2j) of the Hermite polynomial He_m:
    |He_m(t)| <= He*_m(|t|), He* nondecreasing on [0, oo)"""
    return {m - 2 * j: Fr(math.factorial(m), math.factorial(j) * math.factorial(m - 2 * j) * 2 ** j)
            for j in range(m // 2 + 1)}


def he_major_at(m, s):
    return sum((c * s ** p for p, c in he_major(m).items()), Fr(0))


def shells(d, S=4):
    """{s: #{n in Z^d : |n|^2 = s}} for 1 <= s <= S (every such n has |n_i| <= 2)"""
    cnt = {}
    for n in itertools.product(range(-2, 3), repeat=d):
        s = sum(x * x for x in n)
        if 1 <= s <= S:
            cnt[s] = cnt.get(s, 0) + 1
    return cnt


class Images:
    """Image sums of the periodization, bounded for every real L >= L0 and every orthonormal frame (Lemma J)."""

    def __init__(self, d, L0):
        self.d, self.L0 = d, Fr(L0)
        self.sh = shells(d)
        self.cache = {}
        self.theta1 = self.image(0)

    def image(self, m_tot, g=None):
        """upper bound of sum_{n != 0} prod_i |He_{g_i}(p_i)| phi(p),  p = L R n  (|p| = L |n|, any rotation R)"""
        d, L = self.d, self.L0
        g = g if g is not None else (0,) * d
        key = tuple(sorted(g))
        if key in self.cache:
            return self.cache[key]
        n = sum(g)
        require(n * n <= 5 * L * L and n <= L * L, 'jet order outside the range of Lemma J')
        tot = Fr(0)
        for s, c in sorted(self.sh.items()):
            sq = L * L * s
            t = Fr(c) * exp_up(-sq / 2)
            from ball import isqrt_frac_up
            hs = isqrt_frac_up(sq)
            for gi in g:
                t *= he_major_at(gi, hs)
            tot += t
        a2 = d + n                            # 2a, a = (d + |g|)/2 <= 20
        require(a2 <= 40, 'tail exponent')
        tail = Fr(3) ** d * (2 * L) ** n * 2 * Fr(5) ** ((a2 + 1) // 2) * exp_up(-5 * L * L / 2)
        val = rup(tot + tail)
        self.cache[key] = val
        return val

    def jetcov(self, g):
        """d^g K_L(0) as a ball around d^g phi(0)"""
        ref = rho_der(g)
        if sum(g) % 2:
            return B(0)                      # K_L is even: every odd total order vanishes exactly
        if MUTANT == 'no-image':
            return B(ref, self.theta1 * abs(ref))
        if MUTANT == 'no-theta':
            return B(ref, self.image(sum(g), g))
        return B(ref, self.image(sum(g), g) + self.theta1 * abs(ref))


# ============================================================================== 2. series and polynomials over balls
class S:
    """power series c_0 + ... + c_R r^R with Fraction or ball coefficients"""
    __slots__ = ('c',)

    def __init__(self, c=None):
        c = list(c or [])
        self.c = (c + [Fr(0)] * (P.R + 1))[:P.R + 1]

    @staticmethod
    def const(x):
        return S([x])

    def __add__(self, o):
        if not isinstance(o, S):
            o = S.const(o)
        return S([a + b for a, b in zip(self.c, o.c)])
    __radd__ = __add__

    def __neg__(self):
        return S([-a for a in self.c])

    def __sub__(self, o):
        return self + (-o)

    def __mul__(self, o):
        if not isinstance(o, S):
            return S([a * o for a in self.c])
        out = [Fr(0)] * (P.R + 1)
        for i, a in enumerate(self.c):
            if a:
                for j in range(P.R + 1 - i):
                    if o.c[j]:
                        out[i + j] = out[i + j] + a * o.c[j]
        return S(out)
    __rmul__ = __mul__

    def inv(self):
        a0 = self.c[0]
        ia = a0.inv() if isinstance(a0, B) else 1 / Fr(a0)
        out = [Fr(0)] * (P.R + 1)
        out[0] = ia
        for n in range(1, P.R + 1):
            acc = Fr(0)
            for k in range(1, n + 1):
                if self.c[k] and out[n - k]:
                    acc = acc + self.c[k] * out[n - k]
            out[n] = -(acc * ia)
        return S(out)

    def is_zero(self):
        return not any(self.c)


def from_pseries(s):
    return S(list(s.c))


def cov(u, w, jetcov):
    tot = S()
    for a, sa in u.items():
        for b, sb in w.items():
            g = tuple(x + y for x, y in zip(a, b))
            v = jetcov(g)
            if v:
                tot = tot + from_pseries(sa * sb) * (v * (-1) ** sum(b))
    return tot


def mat_inv(M):
    n = len(M)
    A = [row[:] + [S.const(Fr(int(i == j))) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(i for i in range(c, n) if center(A[i][c].c[0]) != 0)
        A[c], A[p] = A[p], A[c]
        iv = A[c][c].inv()
        A[c] = [x * iv for x in A[c]]
        for i in range(n):
            if i != c and not A[i][c].is_zero():
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [row[n:] for row in A]


def mat_det(M):
    n = len(M)
    A = [row[:] for row in M]
    det = S.const(Fr(1))
    for c in range(n):
        p = next(i for i in range(c, n) if center(A[i][c].c[0]) != 0)
        if p != c:
            A[c], A[p] = A[p], A[c]
            det = -det
        det = det * A[c][c]
        iv = A[c][c].inv()
        for i in range(c + 1, n):
            if not A[i][c].is_zero():
                f = A[i][c] * iv
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return det


class Poly:
    """polynomial in (r, b, k, x1, x2, x3), truncated at r^NR, Fraction or ball coefficients"""
    __slots__ = ('t',)

    def __init__(self, t=None):
        self.t = {e: c for e, c in (t or {}).items() if c}

    @staticmethod
    def var(name, power=1):
        e = [0] * NV
        e[VARS.index(name)] = power
        return Poly({tuple(e): Fr(1)})

    @staticmethod
    def const(c):
        return Poly({ONE: c})

    def __add__(self, o):
        if not isinstance(o, Poly):
            o = Poly.const(o)
        t = dict(self.t)
        for e, c in o.t.items():
            t[e] = t[e] + c if e in t else c
        return Poly(t)
    __radd__ = __add__

    def __neg__(self):
        return Poly({e: -c for e, c in self.t.items()})

    def __sub__(self, o):
        return self + (-o if isinstance(o, Poly) else Poly.const(-o))

    def __mul__(self, o):
        if not isinstance(o, Poly):
            return Poly({e: c * o for e, c in self.t.items()})
        t = {}
        for e1, c1 in self.t.items():
            for e2, c2 in o.t.items():
                if e1[0] + e2[0] > NR:
                    continue
                e = tuple(a + b for a, b in zip(e1, e2))
                v = c1 * c2
                t[e] = t[e] + v if e in t else v
        return Poly(t)
    __rmul__ = __mul__

    def rcoef(self, n):
        return Poly({(0,) + e[1:]: c for e, c in self.t.items() if e[0] == n})

    def r_positive(self):
        """the part with r-degree >= 1 (removes the r^0 terms; no subtraction of equal balls)"""
        return Poly({e: c for e, c in self.t.items() if e[0] >= 1})

    def deriv(self, name):
        i = VARS.index(name)
        return Poly({e[:i] + (e[i] - 1,) + e[i + 1:]: c * e[i] for e, c in self.t.items() if e[i]})

    def subs_zero(self, name):
        i = VARS.index(name)
        return Poly({e: c for e, c in self.t.items() if e[i] == 0})

    def centers(self):
        return Poly({e: center(c) for e, c in self.t.items()})

    def is_zero(self):
        return not self.t


def from_series(s):
    return Poly({(i,) + (0,) * (NV - 1): c for i, c in enumerate(s.c[:NR + 1]) if c})


def series_pow(x, alpha):
    """(1 + x)^alpha for a Poly x with no r^0 part (exact through r^NR)"""
    require(all(e[0] >= 1 for e in x.t), 'series_pow: r^0 part')
    out, term, coef = Poly.const(Fr(1)), Poly.const(Fr(1)), Fr(1)
    for n in range(1, NR + 1):
        coef = coef * (Fr(alpha) - (n - 1)) / n
        term = term * x
        out = out + term * coef
    return out


def series_exp(x):
    require(all(e[0] >= 1 for e in x.t), 'series_exp: r^0 part')
    out, term = Poly.const(Fr(1)), Poly.const(Fr(1))
    for n in range(1, NR + 1):
        term = term * x * Fr(1, n)
        out = out + term
    return out


# ============================================================================== 3. the kernel (Lemma P)
def forms_for(d):
    forms = {}
    for nm, sg in (('M', -1), ('S', 1)):
        for i in range(d):
            for j in range(i, d):
                be = [0] * d
                be[i] += 1
                be[j] += 1
                forms[(nm, i, j)] = P.deriv_at(tuple(be), sg, d)
    trans = []
    for i in range(1, d):
        for j in range(i, d):
            be = [0] * d
            be[i] += 1
            be[j] += 1
            forms[('T', i, j)] = {tuple(be): P.S.const(1)}
            trans.append(('T', i, j))
    return forms, trans


def matchings(lst):
    if not lst:
        yield []
        return
    f, rest = lst[0], lst[1:]
    for mm in matchings(rest):
        yield mm
    for i, y in enumerate(rest):
        for mm in matchings(rest[:i] + rest[i + 1:]):
            yield [(f, y)] + mm


def perm_sign(p):
    return -1 if sum(1 for i in range(len(p)) for j in range(i + 1, len(p)) if p[i] > p[j]) % 2 else 1


TVAL = {('T', 1, 1): 'x1', ('T', 2, 2): 'x2', ('T', 1, 2): 'x3'}


def kernel(d, jetcov):
    """A~_r(b, k) = kappa * integral over the cone {T < 0} (x-coordinates, Lebesgue) of exp(-E) G / r^2, with
    E = (q0 + Q0)/2 and kappa = -12 (2 pi)^(-(p + nT)/2) (det S0 det T0)^(-1/2) (NOTE.md 1.3; c2_exact NOTE 2.3)."""
    forms, trans = forms_for(d)
    rows = P.pin_rows(d)
    p, nt = len(rows), len(trans)
    Sm = [[cov(a, b_, jetcov) for b_ in rows] for a in rows]
    Sinv, detS = mat_inv(Sm), mat_det(Sm)
    names = list(forms)
    CF = {u: [cov(forms[u], row, jetcov) for row in rows] for u in names}
    G = {u: [sum((CF[u][q] * Sinv[q][j] for q in range(p)), S()) for j in range(p)] for u in names}
    C = {}
    for i, u in enumerate(names):
        for w in names[i:]:
            val = cov(forms[u], forms[w], jetcov) - sum((G[u][q] * CF[w][q] for q in range(p)), S())
            C[(u, w)] = C[(w, u)] = val
    r, b, k = Poly.var('r'), Poly.var('b'), Poly.var('k')
    v = [b - k * r * r * r * Fr(1, 2), -(k * r * r), Poly(), k * 12] + [Poly()] * (p - 4)
    mean = {u: sum((from_series(G[u][j]) * v[j] for j in range(p)), Poly()) for u in names}
    hn = [u for u in names if u not in trans]
    if nt:
        CTT = [[C[(x, y)] for y in trans] for x in trans]
        CTTinv, detT = mat_inv(CTT), mat_det(CTT)
        Bc = {u: [sum((C[(u, trans[j])] * CTTinv[j][i] for j in range(nt)), S()) for i in range(nt)] for u in hn}
        cp = {(u, w): from_series(C[(u, w)] - sum((Bc[u][i] * C[(trans[i], w)] for i in range(nt)), S()))
              for u in hn for w in hn}
        zT = [Poly.var(TVAL[nm]) - mean[nm] for nm in trans]
        aff = {u: mean[u] + sum((from_series(Bc[u][i]) * zT[i] for i in range(nt)), Poly()) for u in hn}
    else:
        CTTinv, detT, zT = [], S.const(Fr(1)), []
        cp = {(u, w): from_series(C[(u, w)]) for u in hn for w in hn}
        aff = dict((u, mean[u]) for u in hn)
    F = Poly()
    for pp in itertools.permutations(range(d)):
        for qq in itertools.permutations(range(d)):
            fac = [('M', min(i, pp[i]), max(i, pp[i])) for i in range(d)] + \
                  [('S', min(i, qq[i]), max(i, qq[i])) for i in range(d)]
            sg = perm_sign(pp) * perm_sign(qq)
            for mt in matchings(list(range(2 * d))):
                used = set(i for pr in mt for i in pr)
                c = Poly.const(Fr(sg))
                for (i, j) in mt:
                    c = c * cp[(fac[i], fac[j])]
                for i in range(2 * d):
                    if i not in used:
                        c = c * aff[fac[i]]
                F = F + c
    q = sum((v[i] * from_series(Sinv[i][j]) * v[j] for i in range(p) for j in range(p)), Poly())
    Q = sum((zT[i] * from_series(CTTinv[i][j]) * zT[j] for i in range(nt) for j in range(nt)), Poly())
    q0, Q0 = q.rcoef(0), Q.rcoef(0)
    detS0, detT0 = detS.c[0], detT.c[0]
    # (det S_r / det S_0)(det T_r / det T_0) - 1 from the r >= 1 coefficients only (its r^0 part is exactly 0)
    rS = Poly({(i,) + (0,) * (NV - 1): detS.c[i] * (1 / detS0 if not isinstance(detS0, B) else detS0.inv())
               for i in range(1, NR + 1) if detS.c[i]})
    i0 = (1 / detT0) if not isinstance(detT0, B) else detT0.inv()
    rT = Poly({(i,) + (0,) * (NV - 1): detT.c[i] * i0 for i in range(1, NR + 1) if detT.c[i]})
    ratio = rS + rT + (rS * rT)
    if MUTANT == 'drop-ratio':
        ratio = rS
    dqQ = (q.r_positive() + Q.r_positive()) * Fr(-1, 2)
    Gint = series_pow(ratio, Fr(-1, 2)) * series_exp(dqQ) * F
    return {'G': Gint, 'E': (q0 + Q0) * Fr(1, 2), 'p': p, 'nt': nt, 'detS0': detS0, 'detT0': detT0}


# ============================================================================== 4. bounds (Lemmas F, G)
WV = ('b', 'k', 'x1', 'x2', 'x3')


def strip_r(poly):
    out = {}
    for e, c in poly.t.items():
        require(e[0] == 0, 'strip_r: r-dependent term')
        out[e[1:]] = c
    return out


def quad_matrix(Ec, nv):
    """symmetric matrix M with E(w) = w^T M w for the homogeneous quadratic E (centers)"""
    M = [[Fr(0)] * nv for _ in range(nv)]
    for e, c in Ec.items():
        require(sum(e) == 2, 'exponent not homogeneous quadratic')
        idx = [i for i in range(nv) for _ in range(e[i])]
        i, j = idx
        if i == j:
            M[i][i] += c
        else:
            M[i][j] += c / 2
            M[j][i] += c / 2
    return M


def is_pd(M):
    n = len(M)
    A = [row[:] for row in M]
    for c in range(n):
        if A[c][c] <= 0:
            return False
        for i in range(c + 1, n):
            f = A[i][c] / A[c][c]
            for j in range(c, n):
                A[i][j] -= f * A[c][j]
    return True


def diag_scale_lower(M):
    """a rational t in (0, 1] with M - t diag(M) positive semidefinite (exact LDL checks, bisection to 2^-30), so that
    w^T M w >= t sum_i M_ii w_i^2"""
    n = len(M)
    require(is_pd(M), 'reference exponent not positive definite')

    def ok(t):
        return t == 0 or is_pd([[M[i][j] * (1 - t if i == j else 1) for j in range(n)] for i in range(n)]) or \
            (t == 1 and all(M[i][j] == 0 for i in range(n) for j in range(n) if i != j))
    if ok(Fr(1)):
        return Fr(1)
    lo, hi = Fr(0), Fr(1)
    for _ in range(30):
        mid = (lo + hi) / 2
        if ok(mid):
            lo = mid
        else:
            hi = mid
    require(lo > 0, 'diagonal scaling')
    return lo


def gamma_half_up(n):
    """upper bound of Gamma(n/2), n >= 1"""
    if n % 2 == 0:
        return Fr(math.factorial(n // 2 - 1))
    m = (n - 1) // 2                                  # Gamma(m + 1/2) = (2m-1)!! sqrt(pi) / 2^m
    df = 1
    for i in range(1, 2 * m, 2):
        df *= i
    from ball import isqrt_frac_up
    return Fr(df, 2 ** m) * isqrt_frac_up(PI_UP)


def pow_neg_half_up(a, n):
    """upper bound of a^(-n/2), a > 0 rational"""
    if n % 2 == 0:
        return 1 / a ** (n // 2)
    return 1 / (a ** (n // 2) * isqrt_frac_dn(a))


def moment_up(n, a, half=False):
    """upper bound of int_R |t|^n e^(-a t^2) dt = Gamma((n+1)/2) a^(-(n+1)/2)  (half: over [0, oo), one half)"""
    v = gamma_half_up(n + 1) * pow_neg_half_up(a, n + 1)
    return v / 2 if half else v


def maj_poly(H, which):
    """nonnegative majorant coefficients: which = 'mag' -> |c| + rad, 'rad' -> rad"""
    out = {}
    for e, c in H.items():
        v = mag(c) if which == 'mag' else radius(c)
        if v:
            out[e] = out.get(e, Fr(0)) + v
    return out


def mono_mul(P1, P2):
    out = {}
    for e1, c1 in P1.items():
        for e2, c2 in P2.items():
            e = tuple(a + b for a, b in zip(e1, e2))
            out[e] = out.get(e, Fr(0)) + c1 * c2
    return out


def gauss_bound(Pm, a, mode, nx):
    """upper bound of the integral of sum_e Pm[e] |w^e| e^(-sum_i a_i w_i^2) over b in R, x in R^nx, with k:
    'k0' k = 0;  'kw' integral over k in [0, 1] against k^(-1/3) (k^(j - 1/3) <= k^(j-1) for j >= 1, extended to
    [0, oo);  for j = 0, e^(-a k^2) <= 1 and int_0^1 k^(-1/3) dk = 3/2);  'kint' integral over k in [0, oo)."""
    tot = Fr(0)
    for e, c in Pm.items():
        eb, ek, ex = e[0], e[1], e[2:2 + nx]
        require(all(v == 0 for v in e[2 + nx:]), 'unused transverse variable')
        if mode == 'k0' and ek:
            continue
        t = c * moment_up(eb, a[0])
        for i, v in enumerate(ex):
            t *= moment_up(v, a[2 + i])
        if mode == 'kint':
            t *= moment_up(ek, a[1], half=True)
        elif mode == 'kw':
            t *= moment_up(ek - 1, a[1], half=True) if ek else Fr(3, 2)
        tot += t
    return tot


def eta_of(dE, nv):
    """eta_i with |dE(w)| <= sum_i eta_i w_i^2 from the coefficient radii of the quadratic dE
    (|w_i w_j| <= (w_i^2 + w_j^2)/2)"""
    acc = [Fr(0)] * nv
    for e, c in dE.items():
        rad = radius(c)
        if not rad:
            continue
        require(sum(e) == 2, 'exponent radius on a non-quadratic monomial')
        idx = [i for i in range(nv) for _ in range(e[i])]
        i, j = idx
        if i == j:
            acc[i] += rad
        else:
            acc[i] += rad / 2
            acc[j] += rad / 2
    return [x / 2 for x in acc] if MUTANT == 'eta-half' else acc


SPHERE_UP = {1: Fr(2), 2: 2 * PI_UP, 3: 4 * PI_UP}
C2_REF_LO = {1: Fr('0.2300445802661503'), 2: Fr('0.2215244106266632'), 3: Fr('0.1612340491269447')}   # c2_exact


def bound_core(d, D):
    """Lemmas F and G: an upper bound of sup_u |c2[K, u] - c2[phi]| from the ball kernel data D of K (NOTE.md 4)."""
    nx = D['nt']
    nv = 2 + nx
    H = strip_r(D['G'].rcoef(4))
    E = strip_r(D['E'])
    M = quad_matrix({e: center(c) for e, c in E.items()}, nv)
    t = diag_scale_lower(M)                  # E_ref(w) >= t sum_i M_ii w_i^2
    eta = eta_of(E, nv)                      # |E_K(w) - E_ref(w)| <= sum_i eta_i w_i^2
    a = [t * M[i][i] - eta[i] for i in range(nv)]
    require(all(x > 0 for x in a), 'exponent perturbation too large')
    # kappa_K / kappa_ref = (D_K / D_ref)^(-1/2),  D = det S0 det T0
    DK = D['detS0'] * D['detT0']
    Dref = center(DK)
    require(Dref > 0, 'reference determinant')
    rho = radius(DK) / Dref
    require(rho < Fr(1, 2), 'determinant radius')
    e_kappa = rho / (1 - rho)                # |kappa_K/kappa_ref - 1| <= (1 - rho)^(-1/2) - 1 <= rho/(1 - rho)
    nn = D['p'] + nx
    kap = 12 / isqrt_frac_dn(Dref)           # kappa_ref <= kap
    two_pi = 2 * PI_DN
    kap = kap / two_pi ** (nn // 2)
    if nn % 2:
        kap = kap / isqrt_frac_dn(two_pi)
    # H' = dH/dk - (dE/dk) H:  d/dk [exp(-E) H] = exp(-E) H'
    Hp = Poly({(0,) + e: c for e, c in H.items()})
    Ep = Poly({(0,) + e: c for e, c in E.items()})
    Hd = strip_r(Hp.deriv('k') - Ep.deriv('k') * Hp)
    fac = {(0,) * 5: e_kappa}                # |e_kappa| + sum_i eta_i w_i^2
    for i in range(nv):
        e = [0] * 5
        e[i] = 2
        fac[tuple(e)] = eta[i]

    def bound(Hx, mode):
        return kap * gauss_bound(dict_add(mono_mul(fac, maj_poly(Hx, 'mag')), maj_poly(Hx, 'rad')), a, mode, nx)
    fp_const = 3 if MUTANT != 'fp-const' else 1
    b0, b1, b2 = bound(H, 'k0'), bound(Hd, 'kw'), bound(H, 'kint')
    T_bound = fp_const * b0 + 3 * b1 + b2
    eps = rup(SPHERE_UP[d] / 3 * T_bound)
    return {'d': d, 't_diag': t, 'a_min': min(a), 'eta_max': max(eta), 'e_kappa': e_kappa, 'kappa_up': kap, 'Delta0': b0, 'dDelta_w': b1,
            'Delta_int': b2, 'eps': eps, 'max_radius_H': max((radius(c) for c in H.values()), default=Fr(0)),
            'n_monomials_H': len(H)}


def transfer_bound(d, L0):
    img = Images(d, L0)
    out = bound_core(d, kernel(d, img.jetcov))
    out.update({'L0': L0, 'theta1': img.theta1, 'rel': rup(out['eps'] / C2_REF_LO[d]),
                'max_jet_order': max((sum(g) for g in img.cache), default=0)})
    return out


def dict_add(A, Bd):
    out = dict(A)
    for e, c in Bd.items():
        out[e] = out.get(e, Fr(0)) + c
    return out


# ============================================================================== 5. reference checks
def reference_checks():
    """With every radius zero the pipeline is exact; it must reproduce c2_exact's kernel_data (d = 1, 2 identically;
    d = 3 on the slice x3 = T12 = 0, which is the diagonal slice c2_exact evaluates)."""
    import exact as X
    out = {}
    for d in (1, 2, 3):
        ref = X.kernel_data(d)
        mine = kernel(d, lambda g: Fr(rho_der(g)))
        Gm = mine['G'].subs_zero('x3') if d == 3 else mine['G']
        Em = mine['E'].subs_zero('x3') if d == 3 else mine['E']
        ok = True
        for n in range(NR + 1):
            a = {e[:5]: c for e, c in Gm.rcoef(n).t.items()}
            bb = {e: c for e, c in ref['G'].rcoef(n).t.items()}
            ok = ok and a == bb
        Eref = (ref['q0'] + ref['Q0']) * Fr(1, 2)
        ok = ok and {e[:5]: c for e, c in Em.t.items()} == dict(Eref.t)
        ok = ok and mine['detS0'] == ref['detS0']
        if d < 3:
            ok = ok and mine['detT0'] == ref['detT0']
        out[d] = ok
        require(ok, 'reference pipeline mismatch in d = %d' % d)
    return out


# ============================================================================== 6. driver
def dec_up(x, digits=6):
    """decimal string >= x (x >= 0 rational) with `digits` significant digits"""
    x = Fr(x)
    if x == 0:
        return '0'
    e = 0
    while x >= 10 ** (e + 1):
        e += 1
    while x < 10 ** e:
        e -= 1
    scale = Fr(10) ** (digits - 1 - e)
    m = -((-x.numerator * scale.numerator) // (x.denominator * scale.denominator))
    if m >= 10 ** digits:
        m, e = m // 10 + (m % 10 > 0), e + 1
    s = str(m)
    return '%s.%se%+d' % (s[0], s[1:], e)


def fmt(x):
    return dec_up(abs(x)) if x >= 0 else '-' + dec_up(-x)


def compute():
    res = {'object': 'CL-C2-TORUS-TRANSFER-20261001-v1', 'reference_checks': {}, 'bounds': {}}
    res['reference_checks'] = {str(k): v for k, v in reference_checks().items()}
    for d in (1, 2, 3):
        for L0 in L0S:
            t = transfer_bound(d, L0)
            res['bounds']['d%d_L%d' % (d, L0)] = {k: (fmt(v) if isinstance(v, Fr) else v) for k, v in t.items()}
    return res


def main():
    global MUTANT
    args = sys.argv[1:]
    if '--mutant' in args:
        MUTANT = args[args.index('--mutant') + 1]
        require(MUTANT in MUTANTS, 'unknown mutant')
        args = ['--check']
    res = compute()
    path = os.path.join(HERE, 'RESULTS.json')
    if '--write' in args:
        with open(path, 'w') as f:
            json.dump(res, f, indent=1, sort_keys=True)
            f.write('\n')
    elif '--check' in args:
        with open(path) as f:
            stored = json.load(f)
        if stored != res:
            print('MISMATCH against RESULTS.json')
            sys.exit(1)
        print('check passed')
    else:
        print(json.dumps(res, indent=1, sort_keys=True))


if __name__ == '__main__':
    main()
