#!/usr/bin/env python3
"""Explicit constants for [LP] Theorem B on the C8 band, d = 2 and d = 3 (NOTE.md Theorem L and its corollaries).

For the radial ledger A_r = 12 pi_r(R; v_r) Z_r / r^2 of [LP] (10.2) the certificate proves, for 0 < r <= R, every frame,
every torus side L >= 10 and the reference kernel,

    -(a_dn r^2 + eps) <= A_r(b, k, u) / A_0^ref(b, k) - 1 <= a_up r^2 + eps         (b in [0, 1], k in [1/2, 2]),

with A_0^ref the closed-form contact integrand of the Gaussian kernel, and assembles from it two-sided second-order bounds for
nu_cand and nu_eld, the difference constant C_{B,K} of [LP] (1.2), and the constants of (12.1) and (12.3).

Standard library only; exact rational interval arithmetic throughout.
- Taylor models in r (fixed-point integer coefficients, every rounding carried in the remainder) for the pin covariance, its
  determinant, the pin energies and the law of the transverse Hessian and of Omega' (section 2 of NOTE.md).
- The interval band laws and the box-bound engines of Math-#206 (d = 2) and Math-#212 (d = 3), as byte-identical pinned
  copies engine_e2.py and engine_e3.py (section 2; SOURCE_MAP.json).

  python3 -B -S theorem_b.py --procs N              regenerate RESULTS.json
  python3 -B -S theorem_b.py --check --procs N      replay: Taylor models, rate sweep, reference integrals, a sample of
                                                    cap bands, and the assembled tables (exact comparison)
  python3 -B -S theorem_b.py --check-full --procs N replay every cap band as well
  python3 -B -S theorem_b.py --mutant NAME --check  a semantic mutation; the replay must then fail (exit 1)
  python3 -B -S theorem_b.py --controls             floating controls (not part of the certificate)
"""
import argparse
import importlib.util
import json
import math
import multiprocessing
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
MUTANTS = ('no-om-term', 'no-bad-set', 'no-det', 'no-torus', 'cap-half')
MUT = None

R_STARS = (Fr(1, 4096), Fr(1, 2048), Fr(1, 1024), Fr(1, 512), Fr(1, 256), Fr(1, 128), Fr(1, 64))
TM_S = 6                       # Taylor models on [0, 2^-TM_S] = [0, 1/64]
TM_N = 8                       # Taylor-model degree
TM_P = 288                     # fixed-point bits of the Taylor-model coefficients
R0C = Fr(12)                   # Loewner coupling radius (d = 3)
TINY = Fr(1, 10 ** 60)         # polynomial coefficients below this are rounding residue of exact zeros
SUB_B = tuple((Fr(i, 8), Fr(i + 1, 8)) for i in range(8))
SUB_K = tuple((Fr(1, 2) + Fr(j, 8), Fr(1, 2) + Fr(j + 1, 8)) for j in range(12))
SUBBOXES = tuple((bb, kb) for kb in SUB_K for bb in SUB_B)
NH = 4096                      # b-cells of the reference integrals
BLOCK = 16                     # cells per second-derivative block
CAP_B = tuple((Fr(i, 4), Fr(i + 1, 4)) for i in range(4))
CAP_K = tuple((Fr(1, 2) + Fr(i, 32), Fr(1, 2) + Fr(i + 1, 32)) for i in range(8)) \
    + tuple((Fr(3, 4) + Fr(i, 16), Fr(3, 4) + Fr(i + 1, 16)) for i in range(4)) + ((Fr(1), Fr(3, 2)), (Fr(3, 2), Fr(2)))
CAP_BOXES = tuple((bb, kb) for kb in CAP_K for bb in CAP_B)
C_REF_197 = Fr('0.0023869380211529483091019117')    # Math-#197, reference c_{B,K} in d = 2 (cross-check only)
C_REF_205 = Fr('0.0009743823660242504624710565')    # Math-#205, reference c_{B,K} in d = 3 (cross-check only)


def require(cond, msg):
    if not cond:
        raise SystemExit('FAIL: ' + msg)


def load_engine(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


E2 = load_engine('engine_e2', 'engine_e2.py')
E3 = load_engine('engine_e3', 'engine_e3.py')
ENG = {2: E2, 3: E3}


def exp_minus(M, t):
    """Enclosure of exp(-t) for rational t of either sign."""
    t = Fr(t)
    return M.exp_neg_point(t) if t >= 0 else M.exp_neg_point(-t).inv()


def grid_up(x, g=2 ** 40):
    return Fr(math.ceil(Fr(x) * g), g)


def grid_dn(x, g=2 ** 40):
    return Fr(math.floor(Fr(x) * g), g)


def dec_up(x, places):
    x = Fr(x)
    n = -((-x.numerator * 10 ** places) // x.denominator)
    s = str(abs(n)).rjust(places + 1, '0')
    return ('-' if n < 0 else '') + s[:-places] + '.' + s[-places:]


def dec_down(x, places):
    x = Fr(x)
    n = (x.numerator * 10 ** places) // x.denominator
    s = str(abs(n)).rjust(places + 1, '0')
    return ('-' if n < 0 else '') + s[:-places] + '.' + s[-places:]


# ============================================================================= 1. Taylor models in r
def cdiv(a, b):
    return -((-a) // b)


class TM:
    """f(r) = sum_{j <= N} (C_j / 2^P) r^j + theta (E / 2^P), |theta| <= 1, for every r in [0, 2^-s]."""
    __slots__ = ('C', 'E', 's', 'N')

    def __init__(self, C, E, s, N):
        self.C, self.E, self.s, self.N = C, E, s, N

    @classmethod
    def from_fracs(cls, coeffs, e, s, N):
        items = coeffs.items() if isinstance(coeffs, dict) else enumerate(coeffs)
        C = [0] * (N + 1)
        E = Fr(e)
        for p, x in items:
            x = Fr(x)
            if x == 0:
                continue
            if p <= N:
                v = round(x * (1 << TM_P))
                C[p] += v
                E += abs(x - Fr(v, 1 << TM_P)) / Fr(2) ** (s * p)
            else:
                E += abs(x) / Fr(2) ** (s * p)
        return cls(C, cdiv(E.numerator << TM_P, E.denominator), s, N)

    @classmethod
    def const(cls, x, s, N):
        return cls.from_fracs({0: Fr(x)}, 0, s, N)

    def polybound(self):
        return sum(cdiv(abs(c), 1 << (self.s * j)) for j, c in enumerate(self.C) if c)

    def bound(self):
        return self.polybound() + self.E

    def frac_coeffs(self):
        return [Fr(c, 1 << TM_P) for c in self.C]

    def frac_e(self):
        return Fr(self.E, 1 << TM_P)

    def __add__(self, o):
        if not isinstance(o, TM):
            o = TM.const(o, self.s, self.N)
        return TM([a + b for a, b in zip(self.C, o.C)], self.E + o.E, self.s, self.N)
    __radd__ = __add__

    def __neg__(self):
        return TM([-a for a in self.C], self.E, self.s, self.N)

    def __sub__(self, o):
        if not isinstance(o, TM):
            o = TM.const(o, self.s, self.N)
        return self + (-o)

    def scale(self, x):
        x = Fr(x)
        C = []
        E = Fr(self.E, 1 << TM_P) * abs(x)
        for j, c in enumerate(self.C):
            v = Fr(c, 1 << TM_P) * x
            w = round(v * (1 << TM_P))
            C.append(w)
            E += abs(v - Fr(w, 1 << TM_P)) / Fr(2) ** (self.s * j)
        return TM(C, cdiv(E.numerator << TM_P, E.denominator), self.s, self.N)

    def __mul__(self, o):
        if not isinstance(o, TM):
            return self.scale(o)
        N, s = self.N, self.s
        S = [0] * (2 * N + 1)
        for i, a in enumerate(self.C):
            if a:
                for j, b in enumerate(o.C):
                    if b:
                        S[i + j] += a * b
        C, E = [], 0
        for k in range(N + 1):
            v = S[k] >> TM_P                                  # floor: error below one unit, times r^k <= 1
            C.append(v)
            if S[k] - (v << TM_P):
                E += 1
        for k in range(N + 1, 2 * N + 1):
            if S[k]:
                E += cdiv(abs(S[k]), 1 << (TM_P + s * k))
        E += cdiv(self.E * o.polybound() + o.E * self.polybound() + self.E * o.E, 1 << TM_P)
        return TM(C, E, s, N)
    __rmul__ = __mul__

    def inv(self):
        c0 = Fr(self.C[0], 1 << TM_P)
        require(c0 != 0, 'Taylor-model inverse at a zero constant term')
        h = (self - TM([self.C[0]] + [0] * self.N, 0, self.s, self.N)).scale(1 / c0)
        H = Fr(h.bound(), 1 << TM_P)
        require(H < Fr(1, 2), 'Taylor-model inverse: |h| too large')
        acc = TM.const(1, self.s, self.N)
        p = TM.const(1, self.s, self.N)
        mh = -h
        for _ in range(self.N):
            p = p * mh
            acc = acc + p
        tail = H ** (self.N + 1) / (1 - H)
        acc = TM(acc.C, acc.E + cdiv(tail.numerator << TM_P, tail.denominator), self.s, self.N)
        return acc.scale(1 / c0)

    def enclose(self, r0, r1):
        lo = hi = Fr(0)
        for j, c in enumerate(self.C):
            if c:
                x = Fr(c, 1 << TM_P)
                a, b = Fr(r0) ** j, Fr(r1) ** j
                lo += x * (a if x >= 0 else b)
                hi += x * (b if x >= 0 else a)
        e = self.frac_e()
        return lo - e, hi + e


def cov_tm(M, F, G, key, s, N, M1):
    """Taylor model on [0, 2^-s] of the covariance of F, G under the unnormalized torus kernel: the engine's exact series,
    its truncation tail and its torus remainder (as in the engines' cov_band, at r1 = 2^-s)."""
    R = Fr(1, 2 ** s)
    ser, w, absterms = M.pair_series(F, G, key)
    A = max((t[1] for t in absterms), default=0)
    tail = tor = Fr(0)
    for t in absterms:
        acc, aa, gys = t[0], t[1], t[2:]
        hprod = fprod = 1
        for g in gys:
            hprod *= M.hcoef(g)
            fprod *= math.factorial(g)
        tail += acc * abs(hprod)
        tor += acc * fprod * Fr(max(w, 1)) ** aa
    tail *= 2 * Fr(M.NX + 1) ** A * R ** (M.NX + 1 - w)
    tor = tor * M1 / (1 - Fr(27183, 10000) * R)
    return TM.from_fracs(ser, tail + tor, s, N)


def solve_tm(A, B):
    """Gaussian elimination without pivoting (A(0) is positive definite): X[c] solves A X[c] = B[c]; also det A."""
    n = len(A)
    Mx = [[A[i][j] for j in range(n)] + [B[c][i] for c in range(len(B))] for i in range(n)]
    det, invs = None, []
    for col in range(n):
        piv = Mx[col][col]
        det = piv if det is None else det * piv
        ip = piv.inv()
        invs.append(ip)
        for i in range(col + 1, n):
            f = Mx[i][col] * ip
            for j in range(col, len(Mx[i])):
                Mx[i][j] = Mx[i][j] - f * Mx[col][j]
    X = []
    for c in range(len(B)):
        x = [None] * n
        for i in reversed(range(n)):
            acc = Mx[i][n + c]
            for j in range(i + 1, n):
                acc = acc - Mx[i][j] * x[j]
            x[i] = acc * invs[i]
        X.append(x)
    return X, det


class TMLaw:
    pass


TM_NAMES = {2: ('w', 'om'), 3: ('a11', 'a22', 'a12', 'o11', 'o22', 'o12')}


def tm_law(d, s=TM_S, N=TM_N, L=10):
    """Taylor-model law over r in [0, 2^-s] of the targets TM_NAMES[d] (every frame, every torus side >= L, the reference
    kernel): alpha, beta (mean = b alpha + k beta), the unnormalized covariance block, the unnormalized pin energies, det."""
    M = ENG[d]
    names = TM_NAMES[d]
    pins, targets = M.functionals()
    P = [pins[nm] for nm in M.PIN_NAMES]
    idx = [M.TARGET_NAMES.index(nm) for nm in names]
    T = [targets[nm] for nm in names]
    M1 = Fr(0) if MUT == 'no-torus' else M.torus_M1(L)
    n, nt = len(P), len(T)
    Spp = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            Spp[i][j] = Spp[j][i] = cov_tm(M, P[i], P[j], ('p', i, j), s, N, M1)
    Stp = [[cov_tm(M, T[a], P[j], ('tp', idx[a], j), s, N, M1) for j in range(n)] for a in range(nt)]
    Stt = [[None] * nt for _ in range(nt)]
    for a in range(nt):
        for b in range(a, nt):
            i, j = idx[a], idx[b]
            if i <= j:
                Stt[a][b] = Stt[b][a] = cov_tm(M, T[a], T[b], ('tt', i, j), s, N, M1)
            else:
                Stt[a][b] = Stt[b][a] = cov_tm(M, T[b], T[a], ('tt', j, i), s, N, M1)
    zero = TM.const(0, s, N)
    kvec = [TM.from_fracs({3: Fr(-1, 2)}, 0, s, N), TM.from_fracs({2: Fr(-1)}, 0, s, N), TM.const(12, s, N)] + [zero] * (n - 3)
    e1 = [TM.const(1, s, N)] + [zero] * (n - 1)
    X, det = solve_tm(Spp, Stp + [e1, kvec])
    W, xs0, xs1 = X[:nt], X[nt], X[nt + 1]
    law = TMLaw()
    law.d, law.M1, law.th1, law.s, law.N = d, M1, (Fr(0) if MUT == 'no-torus' else M.theta_minus_one(L)), s, N
    law.alpha = {nm: W[a][0] for a, nm in enumerate(names)}
    law.beta = {nm: sum((W[a][j] * kvec[j] for j in range(n)), zero) for a, nm in enumerate(names)}
    law.Cu = {}
    for a, na in enumerate(names):
        for b, nb in enumerate(names):
            law.Cu[(na, nb)] = Stt[a][b] - sum((W[a][l] * Stp[b][l] for l in range(n)), zero)
    law.e_bb = xs0[0]
    law.e_bk = sum((kvec[j] * xs0[j] for j in range(n)), zero)
    law.e_kk = sum((kvec[j] * xs1[j] for j in range(n)), zero)
    law.det = det
    if d == 3:
        # E[O - mu_O | B] = sum_l G[O][l] (B_l - mu_B_l) in natural coordinates (B11, B22, B12), B = -A:
        # G = -Cu(O, A) Cu(A, A)^-1
        an = ('a11', 'a22', 'a12')
        Xg, _ = solve_tm([[law.Cu[(x, y)] for y in an] for x in an], [[law.Cu[(o, y)] for y in an] for o in ('o11', 'o22', 'o12')])
        law.G = {o: [-Xg[c][l] for l in range(3)] for c, o in enumerate(('o11', 'o22', 'o12'))}
    return law


def tm_summary(law):
    """Exact low-order coefficients (decimal, 30 places) and remainders of the Taylor models, for the record."""
    def row(t):
        c = t.frac_coeffs()
        return {'c': [dec_down(x, 30) if x >= 0 else dec_up(x, 30) for x in c[:5]], 'rem': dec_up(t.frac_e(), 30)}
    out = {'det': row(law.det), 'e_bb': row(law.e_bb), 'e_bk': row(law.e_bk), 'e_kk': row(law.e_kk)}
    for nm in law.alpha:
        out['alpha_' + nm] = row(law.alpha[nm])
        out['beta_' + nm] = row(law.beta[nm])
    names = TM_NAMES[law.d]
    for i, a in enumerate(names):
        for b in names[i:]:
            out['C_%s_%s' % (a, b)] = row(law.Cu[(a, b)])
    return out


# ============================================================================= 2. (a, eps) forms and Taylor-model readers
def ae_add(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def ae_mul(x, c):
    return (x[0] * c, x[1] * c)


def ae_at(x, R):
    return x[0] * R * R + x[1]


def exp_up(M, x, R):
    """exp(a0 r^2 + e0) - 1 <= (a0 r^2 + e0) exp(a0 R^2 + e0) on (0, R]."""
    f = exp_minus(M, -ae_at(x, R)).hi
    return (x[0] * f, x[1] * f)


def tm_dev(t, ref, R):
    """(a, eps): |t(r) - ref| <= a r^2 + eps for 0 <= r <= R."""
    c = t.frac_coeffs()
    eps = abs(c[0] - ref) + abs(c[1]) * R + t.frac_e()
    a, Rp = Fr(0), Fr(1)
    for x in c[2:]:
        a += abs(x) * Rp
        Rp *= R
    return (a, eps)


def tm_lin(t, R):
    """(s, eps): |t(r)| <= s r + eps for 0 <= r <= R."""
    c = t.frac_coeffs()
    s, Rp = Fr(0), Fr(1)
    for x in c[1:]:
        s += abs(x) * Rp
        Rp *= R
    return (s, abs(c[0]) + t.frac_e())


def tm_shift(t, ref, R):
    """(lo, hi, eps): t(r) - ref in [lo r^2 - eps, hi r^2 + eps] for 0 <= r <= R."""
    c = t.frac_coeffs()
    eps = abs(c[0] - ref) + abs(c[1]) * R + t.frac_e()
    lo = hi = c[2]
    Rp = R
    for x in c[3:]:
        v = x * Rp
        lo += min(v, 0)
        hi += max(v, 0)
        Rp *= R
    return (lo, hi, eps)


def assert_flat(t, ref, what):
    c = t.frac_coeffs()
    require(abs(c[0] - ref) <= TINY and all(abs(x) <= TINY for x in c[1:]),
            'the reference law of %s is not the contact law for every r' % what)


def gersh_min(C):
    n = len(C)
    return min(C[i][i].lo - sum(max(abs(C[i][j].lo), abs(C[i][j].hi)) for j in range(n) if j != i) for i in range(n))


def wq_bound(M, Cg, rows, vecs):
    """Upper bound of ||V' Cg^-1 V|| (rows of V given as magnitude lists).  With D the lower endpoints of the diagonal,
    Cg = D^(1/2)(I + H + E)D^(1/2) exactly, where H >= 0 is diagonal (the actual diagonal's surplus over D) and E has zero
    diagonal with ||E||_F <= Ef; so Cg >= (1 - Ef) D and Cg^-1 <= D^-1/(1 - Ef) (review C58: the surplus H only helps)."""
    n = len(rows)
    D = [Cg[(rows[i], rows[i])].lo for i in range(n)]
    Ef2 = Fr(0)
    for i in range(n):
        for j in range(n):
            if i != j:
                c = max(abs(Cg[(rows[i], rows[j])].lo), abs(Cg[(rows[i], rows[j])].hi))
                Ef2 += c * c / (D[i] * D[j])
    Ef = M.sqrt_up(Ef2)
    require(Ef < Fr(1, 2), 'diagonal scaling of the conditional covariance')
    return sum(sum(x * x for x in vecs[i]) / D[i] for i in range(n)) / (1 - Ef)


def half_moments(M, c):
    """H_j = int_0^inf u^j exp(-u^2/(2c)) du, j = 0..3: sqrt(pi c/2), c, c sqrt(pi c/2), 2 c^2 (upper bounds)."""
    s = M.isqrt_iv(M.PI * c / 2).hi
    return [s, Fr(c), c * s, 2 * Fr(c) ** 2]


# ============================================================================= 3. the ratio A_r / A_0^ref on a (b, k) box
def pi_ratio(M, tml, n, Q, R):
    """log(pi_r / pi_0^ref) in [-dn, up], with dn, up in (a, eps) form; pi_0^ref has det 12 and energy 3b^2/2 + 24k^2."""
    b0, b1, k0, k1 = Q
    th1 = tml.th1
    dlo, dhi, de = tm_shift(tml.det, 12, R)
    if MUT == 'no-det':
        dlo = dhi = de = Fr(0)
    xm = (max(abs(dlo), abs(dhi)) * R * R + de) / 12
    require(xm < Fr(1, 2), 'pin determinant deviation')
    half_log_up = (max(Fr(0), -dlo) / (24 * (1 - xm)), de / (24 * (1 - xm)))
    half_log_dn = (max(Fr(0), dhi) / 24, de / 24)
    parts = ((tml.e_bb, Fr(3, 2), (b0 * b0, b1 * b1)), (tml.e_bk, Fr(0), (2 * b0 * k0, 2 * b1 * k1)),
             (tml.e_kk, Fr(24), (k0 * k0, k1 * k1)))
    Elo = Ehi = Ee = Eu = Fr(0)
    for t, ref, (wlo, whi) in parts:
        lo, hi, e = tm_shift(t, ref, R)
        Elo += min(wlo * lo, whi * lo)
        Ehi += max(wlo * hi, whi * hi)
        Ee += whi * e
        Eu += whi * (abs(ref) + max(abs(lo), abs(hi)) * R * R + e)
    up = ae_add(half_log_up, (max(Fr(0), -Elo / 2), Ee / 2 + n * th1 / 2))
    dn = ae_add(half_log_dn, (max(Fr(0), Ehi / 2), (Ee + th1 * Eu) / 2))
    return up, dn


def combine(M, p_up, p_dn, z_up, z_dn, R):
    pu = exp_up(M, p_up, R)
    zR = ae_at(z_up, R)
    up = (pu[0] + z_up[0] + pu[0] * zR, pu[1] + z_up[1] + pu[1] * zR)
    return up, ae_add(p_dn, z_dn)


def bounds_d2(Q, R, tml, il):
    """(up, dn): A_r/A_0^ref - 1 <= up(r), 1 - A_r/A_0^ref <= dn(r) on the box, for 0 < r <= R (NOTE sections 3-5)."""
    M = E2
    b0, b1, k0, k1 = Q
    th1 = tml.th1
    assert_flat(tml.alpha['w'], -1, 'alpha_w')
    assert_flat(tml.beta['w'], 0, 'beta_w')
    assert_flat(tml.Cu[('w', 'w')], 2, 'Var w')
    # the law of lambda = -w: mean b + D, variance 2 + S (remainder only)
    Dae = ae_add(ae_mul(tm_dev(tml.alpha['w'], -1, R), b1), ae_mul(tm_dev(tml.beta['w'], 0, R), k1))
    aC = tm_dev(tml.Cu[('w', 'w')], 2, R)
    Sae = (aC[0], aC[1] + (2 + ae_at(aC, R)) * th1)
    Dm, Sm = ae_at(Dae, R), ae_at(Sae, R)
    r2 = M.isqrt_iv(M.IV(2))
    s_lo, s_hi = M.isqrt_iv(M.IV(2 - Sm)).lo, M.isqrt_iv(M.IV(2 + Sm)).hi
    sa, sb = min(s_lo, r2.lo), max(s_hi, r2.hi)
    m_lo, m_hi = b0 - Dm, b1 + Dm
    mmax = max(abs(m_lo), abs(m_hi))
    Fmin = M.elam2_pos(m_lo, sa).lo
    Fmax = M.elam2_pos(m_hi, sb).hi
    F1max = M.elam_pos(m_hi, sb).hi
    # the variance multiplier (3/4) 2 sb = (3/2) sb only needs to be >= 1 (dF/d(sigma^2) = Phi(mu/sigma) <= 1); it is not
    # a claim that Phi <= 3/4, which fails at mu = 1, sigma^2 = 2 (review C60)
    Fae = ae_add(ae_mul(Dae, 2 * F1max / Fmin), ae_mul(Sae, 2 * sb / Fmin * Fr(3, 4)))
    Fref = M.elam2_pos(b0, r2.lo).lo
    # secondary law: the engine's interval law over [0, R]
    b, k = M.IV(b0, b1), M.IV(k0, k1)
    ma = {nm: M.absup(b * il.alpha[nm] + k * il.beta[nm]) for nm in M.TARGET_NAMES}
    gn = lambda nm, p: M.gauss_norm(ma[nm], il.sdQ[nm].hi, p)
    lam = lambda p: M.gauss_norm(mmax, s_hi, p)
    T, tau, om, v, nu = (lambda p, x=x: gn(x, p) for x in ('T', 'tau', 'om', 'v', 'nu'))
    kap = lambda p: 6 * k1 * tau(p) + T(2 * p) ** 2 + R * T(2 * p) * tau(2 * p)
    norm36 = 36 * k0 * k0 * Fref
    # first order: r E[lambda_+ om] = r [mu_om F_1 - bw_om (F - m F_1)], with mu_om, bw_om = O(r) (Taylor models)
    sa_, ea_ = tm_lin(tml.alpha['om'], R)
    sb_, eb_ = tm_lin(tml.beta['om'], R)
    sc_, ec_ = tm_lin(tml.Cu[('om', 'w')], R)
    cwlo = 2 - ae_at(aC, R)
    T2 = (((b1 * sa_ + k1 * sb_) * F1max + sc_ / cwlo * (Fmax + mmax * F1max)) / Fref,
          R * ((b1 * ea_ + k1 * eb_) * F1max + ec_ / cwlo * (Fmax + mmax * F1max)) / Fref)
    if MUT == 'no-om-term':
        T2 = (Fr(0), Fr(0))
    # second order (explicit r^2). kappa = 6k tau - T^2 - r T tau with E[tau | w] = mu_tau + bw_tau (w - mu_w):
    # 6k mu_tau F + 6k bw_tau E[(w - mu_w) lambda_+^2] - E[T^2 lambda_+^2] - r E[T tau lambda_+^2] (signed in the leading part)
    mt = M.IV(6 * k0, 6 * k1) * (b * il.alpha['tau'] + k * il.beta['tau']) * M.IV(Fmin, Fmax)
    side = 6 * k1 * M.absup(il.bw['tau']) * s_hi * lam(4) ** 2 + R * T(4) * tau(4) * lam(4) ** 2
    T3_up = max(Fr(0), mt.hi + side) / norm36
    T3_dn = max(Fr(0), -mt.lo + side + T(4) ** 2 * lam(4) ** 2) / norm36
    if MUT == 'no-om-term':
        T3_up = T3_dn = Fr(0)
    T4 = R * kap(4) * lam(4) * om(2)
    xi2 = 6 * k1 * (R * nu(4) ** 2 + 2 * nu(4) * v(4)) + T(4) * (R * R * nu(8) ** 2 + 2 * R * nu(8) * v(8) + 2 * v(8) ** 2) \
        + R * tau(4) * v(8) ** 2
    T5 = lam(2) * xi2
    T6 = v(8) ** 2 * (6 * k1 + R * T(4) + R * R * tau(4)) * om(4) + v(4) ** 2 * (R * nu(4) + v(4)) ** 2
    # the thin set {0 < lambda <= r h} on G_0 (conditional density of lambda given (v, om, nu))
    Yn = ('v', 'om', 'nu')
    prec = 1 / (2 - Sm) + wq_bound(M, il.Cg, Yn, [[M.absup(il.bw[nm])] for nm in Yn])
    pbar = Fr(2, 5) * M.sqrt_up(prec)
    h = lambda p: Fr(2) / (9 * k0) * v(2 * p) ** 2 + om(p)
    bad = R * pbar * h(2) * (Fr(15, 2) * k1 * h(4) + v(8) ** 2) * (9 * k1 * (h(4) + om(4)) + (R * nu(8) + v(8)) ** 2)
    if MUT == 'no-bad-set':
        bad = Fr(0)
    # G_0^c (not r^2-scaled; astronomically small)
    q = M.gauss_tail2(ma['T'], il.sdQ['T'].hi, 3 * k0 / (2 * R)) + M.gauss_tail2(ma['tau'], il.sdQ['tau'].hi, 3 * k0 / (2 * R * R))
    P1n = (6 * k1 + R * T(8)) * lam(8) + R * v(8) ** 2
    P2n = (6 * k1 + R * T(8) + R * R * tau(8)) * (lam(8) + R * om(8)) + R * (R * nu(8) + v(8)) ** 2
    g0c = P1n * P2n * M.sqrt_up(q) if q > 0 else Fr(0)
    X = ae_add(T2, ((T4 + T5 + T6 + bad) / norm36, g0c / norm36))
    p_up, p_dn = pi_ratio(M, tml, 6, Q, R)
    return combine(M, p_up, p_dn, ae_add(exp_up(M, Fae, R), X, (T3_up, Fr(0))), ae_add(Fae, X, (T3_dn, Fr(0))), R)


def bounds_d3(Q, R, tml, il):
    """(up, dn) in d = 3 (NOTE sections 3-5)."""
    M = E3
    b0, b1, k0, k1 = Q
    th1 = tml.th1
    names = ('a11', 'a22', 'a12')
    for nm, ref in (('a11', -1), ('a22', -1), ('a12', 0)):
        assert_flat(tml.alpha[nm], ref, 'alpha_' + nm)
        assert_flat(tml.beta[nm], 0, 'beta_' + nm)
    for (x, y), ref in ((('a11', 'a11'), 2), (('a22', 'a22'), 2), (('a12', 'a12'), 1), (('a11', 'a22'), 0),
                        (('a11', 'a12'), 0), (('a22', 'a12'), 0)):
        assert_flat(tml.Cu[(x, y)], ref, 'Cov(%s, %s)' % (x, y))
    # Loewner coupling with the contact law at the same b: eps = sup ||mu_B - b I||_F, eta = ||chol(Cb) - sqrt2 I||
    comps = []
    for nm, ref, f in (('a11', -1, 1), ('a22', -1, 1), ('a12', 0, 2)):
        comps.append(ae_at(ae_add(ae_mul(tm_dev(tml.alpha[nm], ref, R), b1), ae_mul(tm_dev(tml.beta[nm], 0, R), k1)), R) * f)
    eps = M.sqrt_up(sum(x * x for x in comps))
    Fw = (Fr(1), Fr(1), M.SQRT2)
    Cb = []
    for i in range(3):
        row = []
        for j in range(3):
            lo, hi = tml.Cu[(names[i], names[j])].enclose(0, R)
            row.append(M.IV(lo, hi) * Fw[i] * Fw[j] * M.IV(1 / (1 + th1), 1))
        Cb.append(row)
    Lb = M.cholesky(Cb)
    eta = M.sqrt_up(sum(M.absup(Lb[i][j] - (M.SQRT2 if i == j else 0)) ** 2 for i in range(3) for j in range(i + 1)))
    Dl = M.rup_rel(eps + eta * R0C)
    cm = M.contact_moment
    bA, bB = grid_dn(b0 - Dl), grid_up(b1 + Dl)
    m3b0 = cm(2, 0, b0).lo
    L3up = 2 * cm(1, 1, bB).hi / m3b0
    L3dn = 2 * cm(1, 1, b1).hi / cm(2, 0, bA).lo
    pR0 = M.chi_tail(3, R0C)
    muB = M.rup_rel(b1 * M.sqrt_up(Fr(2)) + eps)
    sig = M.sqrt_up(max(x.hi for x in (Cb[0][0], Cb[1][1], Cb[2][2]))
                    + 2 * max(M.absup(Cb[i][j]) for i in range(3) for j in range(3) if i != j))
    U = M.chi_upper_moments(3, R0C, 4)
    out_D2 = sum((U[i] * (M.binom(4, i) * muB ** (4 - i) * sig ** i) for i in range(5)), M.IV(0)).hi / 4
    tail_c = M.sqrt_up(cm(4, 0, b1).hi) * M.sqrt_up(pR0)
    nBF16 = M.rup_rel(muB + sig * M.chi_norm(3, 16))
    out_ball = M.sqrt_up(pR0)

    def up_moment(a, c):
        return M.rup_rel(cm(a, c, bB).hi + 2 ** c * M.rup_rel(nBF16 ** (2 * a + c)) * out_ball)
    ED2, ED4, ED2T2, ET4, DT = up_moment(2, 0), up_moment(4, 0), up_moment(2, 2), up_moment(0, 4), up_moment(1, 1)
    trCb = sum(x.hi for x in (Cb[0][0], Cb[1][1], Cb[2][2]))
    BF = lambda p: M.frob_norm(muB, trCb, p)
    # secondary law (engine interval law over [0, R])
    b, k = M.IV(b0, b1), M.IV(k0, k1)
    ma = {nm: M.absup(b * il.alpha[nm] + k * il.beta[nm]) for nm in M.TARGET_NAMES}
    T = lambda p: M.gauss_norm(ma['T'], il.sdQ['T'], p)
    tau = lambda p: M.gauss_norm(ma['tau'], il.sdQ['tau'], p)
    mu_o = M.sqrt_up(ma['o11'] ** 2 + ma['o22'] ** 2 + 2 * ma['o12'] ** 2)
    trO = sum(m * il.C[(nm, nm)].hi for nm, m in zip(M.ONAMES, (1, 1, 2)))
    Om = lambda p: M.frob_norm(mu_o, trO, p)
    mu_v = M.sqrt_up(ma['v1'] ** 2 + ma['v2'] ** 2)
    v = lambda p: M.frob_norm(mu_v, il.C[('v1', 'v1')].hi + il.C[('v2', 'v2')].hi, p)
    mu_nu = M.sqrt_up(ma['nu1'] ** 2 + ma['nu2'] ** 2)
    nu = lambda p: M.frob_norm(mu_nu, il.C[('nu1', 'nu1')].hi + il.C[('nu2', 'nu2')].hi, p)
    e = lambda p: R * nu(p) + v(p)
    kap = lambda p: 6 * k1 * tau(p) + T(2 * p) ** 2 + R * T(2 * p) * tau(2 * p)
    c1 = lambda p: 6 * k1 + R * T(p)
    c2 = lambda p: 6 * k1 + R * T(p) + R * R * tau(p)
    norm36 = 36 * k0 * k0 * m3b0
    # the mean of Omega': ||mu_Omega'||_F <= s_mu r + e_mu (Taylor models; beta_O = r^2 on the diagonal)
    s_mu2 = e_mu2 = Fr(0)
    for nm, mult in zip(M.ONAMES, (1, 1, 2)):
        sa_, ea_ = tm_lin(tml.alpha[nm], R)
        sb_, eb_ = tm_lin(tml.beta[nm], R)
        s_mu2 += mult * (b1 * sa_ + k1 * sb_) ** 2
        e_mu2 += mult * (b1 * ea_ + k1 * eb_) ** 2
    muO = M.sqrt_up(s_mu2) * R + M.sqrt_up(e_mu2)                      # sup over (0, R] (it multiplies r^2 or more)
    # the regression of Omega' on B: E[Omega' - mu | B] = beta (B - mu_B) + DY, beta = (r - r^3/4)/2 + ..., DY remainder-only
    G = tml.G
    beta_t = G['o11'][0]
    bc = beta_t.frac_coeffs()
    require(abs(bc[0]) <= TINY, 'regression of Omega on B at r = 0')
    for (o, l) in (('o22', 1), ('o12', 2)):
        assert_flat(G[o][l] - beta_t, 0, 'regression of %s on B' % o)
    for o, ls in (('o11', (1, 2)), ('o22', (0, 2)), ('o12', (0, 1))):
        for l in ls:
            assert_flat(G[o][l], 0, 'off-diagonal regression of %s on B' % o)
    dG2 = Fr(0)
    for o, mult in zip(('o11', 'o22', 'o12'), (1, 1, 2)):
        for l in range(3):
            t = G[o][l] - beta_t if (o, l) in (('o11', 0), ('o22', 1), ('o12', 2)) else G[o][l]
            dG2 += mult * Fr(t.bound(), 1 << TM_P) ** 2
    dGn = M.sqrt_up(dG2)
    b1c = bc[1]                                                         # = 1/2
    require(b1c > 0, 'sign of the first-order regression coefficient of Omega on B')
    sb_beta = sum(abs(x) * R ** (j - 2) for j, x in enumerate(bc) if j >= 2)
    e_beta = beta_t.frac_e()
    # E[D tr(A* Omega') 1] = beta (2 E[D^2 1] - E[D tr(A* mu_B) 1]) + R1, tr(A* mu_B) = b tr B + tr(A* dmu), ||dmu||_F <= eps
    DTlo = cm(1, 1, bA).lo - M.sqrt_up(cm(2, 2, b1).hi) * M.sqrt_up(pR0)
    m3up = cm(2, 0, b1).hi
    rho_lo = exp_minus(M, Dl * L3dn).lo - tail_c / m3b0                 # m3_r / m3(b)
    rho_hi = exp_minus(M, -(Dl * L3up)).hi + out_D2 / m3b0
    tau_lo = b0 * max(DTlo, Fr(0)) / m3up                               # b E[D tr B 1] / m3(b)
    tau_hi = b1 * DT / m3b0
    X3lo = 2 * rho_lo - tau_hi - eps * DT / m3b0
    X3hi = 2 * rho_hi - tau_lo + eps * DT / m3b0
    X3m = max(abs(X3lo), abs(X3hi))
    # |R1|/m3(b) <= (s_mu r + e_mu) DT/m3 + ||DG|| sqrt(E[D^2 tr^2 1]) sqrt(tr Cb)/m3, so r |R1|/m3 <= r^2 s_mu DT/m3 + R (...)
    R1a = M.sqrt_up(s_mu2) * DT / m3b0
    R1e = (M.sqrt_up(e_mu2) * DT + dGn * M.sqrt_up(ED2T2) * M.sqrt_up(trCb)) / m3b0
    # -r E[D tr(A* Omega') 1]/m3(b) = -(b1c r^2 + (r beta - b1c r^2)) X3 - r R1/m3(b), |r beta - b1c r^2| <= sb_beta R r^2 + e_beta r
    U3_up = (max(Fr(0), -b1c * X3lo) + sb_beta * R * X3m + R1a, R * (e_beta * X3m + R1e))
    U3_dn = (max(Fr(0), b1c * X3hi) + sb_beta * R * X3m + R1a, R * (e_beta * X3m + R1e))
    if MUT == 'no-om-term':
        U3_up = U3_dn = (Fr(0), Fr(0))
    # explained parts of Omega' by B (for U4) and by zeta = (B, v, nu) (for U6, U7): traces of C_Oz C_zz^-1 C_zO
    zB = ('a11', 'a22', 'a12')
    zA = zB + tuple(M.VNAMES) + ('nu1', 'nu2')
    def cov_Oz(o, z):
        if z in zB:
            s_, e_ = tm_lin(tml.Cu[(o, z)], R)
            return s_ * R + e_
        return M.absup(il.C[(o, z)])
    def explained(zs):
        rows = []
        for o, mult in zip(M.ONAMES, (1, 1, 2)):
            rows.append([cov_Oz(o, z) for z in zs])
        D = [il.C[(z, z)].lo for z in zs]
        Ef2 = Fr(0)
        for i in range(len(zs)):
            for j in range(len(zs)):
                if i != j:
                    c = M.absup(il.C[(zs[i], zs[j])])
                    Ef2 += c * c / (D[i] * D[j])
        Ef = M.sqrt_up(Ef2)
        require(Ef < Fr(1, 2), 'diagonal scaling (explained part of Omega)')
        return sum(mult * sum(x * x / Dz for x, Dz in zip(row, D)) for row, mult in zip(rows, (1, 1, 2))) / (1 - Ef)
    tB, tK = explained(zB), explained(zA)
    YB4, YK4 = M.frob_norm(0, tB, 4), M.frob_norm(0, tK, 4)
    detX = M.absup(il.Cg[('o11', 'o22')] - il.Cg[('o12', 'o12')])     # |E[det(Omega' - E[Omega' | B])]|
    E1 = up_moment(1, 0)
    # second order (explicit r^2)
    # signed kappa term: 6k mu_tau E[D^2 1] + 6k E[(tau - mu_tau) D^2 1] - E[T^2 D^2 1] - r E[T tau D^2 1]
    ED2lo = max(Fr(0), cm(2, 0, bA).lo - tail_c)
    mt = M.IV(6 * k0, 6 * k1) * (b * il.alpha['tau'] + k * il.beta['tau']) * M.IV(ED2lo, ED2)
    side = 6 * k1 * il.bnorm['tau'] * M.sqrt_up(trCb) * M.sqrt_up(ED4) + R * T(4) * tau(4) * M.sqrt_up(ED4)
    U2_up = max(Fr(0), mt.hi + side) / norm36
    U2_dn = max(Fr(0), -mt.lo + side + T(4) ** 2 * M.sqrt_up(ED4)) / norm36
    if MUT == 'no-om-term':
        U2_up = U2_dn = Fr(0)
    U2 = Fr(0)
    U3r = R * kap(4) * M.sqrt_up(ED2T2) * Om(4)
    # U4 = r^2 E[c1 c2 D det Omega' 1]: E[det Omega' | B] = det(mu + Y_B) + E[det X'] (36 k^2 cancels; relative)
    U4rel = (detX * E1 + M.sqrt_up(ED2) * (muO + YB4) ** 2 / 2) / m3b0
    U4 = R * R * kap(4) * M.sqrt_up(ED2) * Om(8) ** 2 / 2
    U5 = M.sqrt_up(ED2T2) * ((2 * T(4) + R * tau(4)) * v(8) ** 2 + 2 * c1(4) * nu(8) * v(8) + R * c1(4) * nu(8) ** 2)
    # U6, U7: the 6k parts through E[Omega' | B, v, nu] = mu + Y_K (Omega' - E[Omega' | zeta] has conditional mean 0)
    U67rel = (M.sqrt_up(ED2) * (muO * e(4) ** 2 + e(8) ** 2 * YK4) + M.sqrt_up(ET4) * (muO * v(4) ** 2 + v(8) ** 2 * YK4)) / (6 * k0 * m3b0)
    U6 = R * T(8) * M.sqrt_up(ED2) * Om(8) * e(8) ** 2
    U7 = R * (T(8) + R * tau(8)) * M.sqrt_up(ET4) * Om(8) * v(8) ** 2
    U8 = R * c2(8) * Om(16) ** 2 / 2 * M.iroot(ET4, 4) * v(16) ** 2
    U9 = M.sqrt_up(ET4) * v(8) ** 2 * e(8) ** 2
    U10 = R * M.iroot(ET4, 4) * v(8) ** 2 * Om(4) * e(8) ** 2
    # the thin set {0 < lambda_1 <= r h} on G_0: conditional law of B given Y = (v, Omega', nu), eigenvalue coordinates
    Yn = tuple(M.VNAMES) + tuple(M.ONAMES) + ('nu1', 'nu2')
    lmB = gersh_min(Cb)
    rows = []
    for nm in Yn:
        if nm in M.ONAMES:
            cov = [(tm_lin(tml.Cu[(nm, an)], R)[0] * R + tm_lin(tml.Cu[(nm, an)], R)[1]) * f for an, f in zip(names, (1, 1, 2))]
            rows.append([M.sqrt_up(sum(x * x for x in cov)) / lmB])
        else:
            rows.append([M.absup(x) for x in il.bt[nm]])
    Wt = wq_bound(M, il.Cg, Yn, rows)
    c_hi = sig * sig
    cl = 1 / (1 / lmB + Wt)
    KBp = M.rup_rel((M.PI * M.SQRT2 / (2 * M.PI * M.SQRT2PI)).hi / (cl * M.sqrt_down(cl)))
    m1 = muB + c_hi * M.sqrt_up(Wt) * M.chi_norm(7, 8)
    Hs = half_moments(M, c_hi)
    Ja = m1 ** 4 / 4 + sum(M.binom(3, i) * m1 ** (3 - i) * Hs[i] for i in range(4))
    Jb = m1 ** 3 / 3 + sum(M.binom(2, i) * m1 ** (2 - i) * Hs[i] for i in range(3))
    h = lambda p: Fr(2) / (9 * k0) * v(2 * p) ** 2 + Om(p)
    nhg = h(4) * (Fr(15, 2) * k1 * h(8) + v(16) ** 2) * (9 * k1 * (h(8) + Om(8)) + e(16) ** 2)
    nhgO = h(8) * (Fr(15, 2) * k1 * h(16) + v(32) ** 2) * (9 * k1 * (h(16) + Om(16)) + e(32) ** 2) * Om(8)
    bad = R * KBp * (Ja * nhg + R * Jb * nhgO)
    if MUT == 'no-bad-set':
        bad = Fr(0)
    q = M.gauss_tail2(ma['T'], il.sdQ['T'], 3 * k0 / (2 * R)) + M.gauss_tail2(ma['tau'], il.sdQ['tau'], 3 * k0 / (2 * R * R))
    P1n = c1(8) * BF(16) ** 2 + R * BF(8) * v(16) ** 2
    P2n = c2(8) * (BF(16) + R * Om(16)) ** 2 + R * (BF(8) + R * Om(8)) * e(16) ** 2
    g0c = P1n * P2n * M.sqrt_up(q) if q > 0 else Fr(0)
    X = ((U2 + U3r + U4 + U5 + U6 + U7 + U8 + U9 + U10 + bad) / norm36 + U4rel + U67rel, g0c / norm36)
    z_up = ae_add(exp_up(M, (Fr(0), Dl * L3up), R), (Fr(0), out_D2 / m3b0), U3_up, X, (U2_up, Fr(0)))
    z_dn = ae_add((Fr(0), Dl * L3dn), (Fr(0), tail_c / m3b0), U3_dn, X, (U2_dn, Fr(0)))
    p_up, p_dn = pi_ratio(M, tml, 8, Q, R)
    return combine(M, p_up, p_dn, z_up, z_dn, R)


def rate_sweep(d, tml):
    """For every R in R_STARS and every sub-box: (a_up, eps_up, a_dn, eps_dn) as decimal strings (rounded up)."""
    M = ENG[d]
    fn = bounds_d2 if d == 2 else bounds_d3
    out = {}
    for R in R_STARS:
        il = M.band_law(Fr(0), R)
        rows = []
        for bb, kb in SUBBOXES:
            up, dn = fn((bb[0], bb[1], kb[0], kb[1]), R, tml, il)
            rows.append([dec_up(up[0], 6), dec_up(up[1], 20), dec_up(dn[0], 6), dec_up(dn[1], 20)])
        out[str(R)] = {'boxes': rows,
                       'a_up': max((r[0] for r in rows), key=Fr), 'eps_up': max((r[1] for r in rows), key=Fr),
                       'a_dn': max((r[2] for r in rows), key=Fr), 'eps_dn': max((r[3] for r in rows), key=Fr)}
    return out


# ============================================================================= 4. certified reference integrals
PREC = 240


def iroot_int(N, p):
    """Largest y >= 0 with y^p <= N."""
    if N < 2:
        return N
    y = 1 << ((N.bit_length() + p - 1) // p)
    while True:
        z = ((p - 1) * y + N // y ** (p - 1)) // p
        if z >= y:
            break
        y = z
    while y ** p > N:
        y -= 1
    while (y + 1) ** p <= N:
        y += 1
    return y


def pow_frac(M, x, num, den):
    """Enclosure of x^(num/den), rational x > 0."""
    x = Fr(x) ** num
    S = 1 << (den * PREC)
    lo_n = (x.numerator * S) // x.denominator
    hi_n = -((-x.numerator * S) // x.denominator)
    ylo, yhi = iroot_int(lo_n, den), iroot_int(hi_n, den)
    if yhi ** den < hi_n:
        yhi += 1
    return M.IV(Fr(ylo, 1 << PREC), Fr(yhi, 1 << PREC))


def lower_gamma(M, an, ad, x):
    """gamma(a, x) = x^a e^-x sum_n x^n / (a (a+1) ... (a+n)), a = an/ad > 0, rational x > 0 (series with a geometric tail)."""
    a, x = Fr(an, ad), Fr(x)
    term = s = 1 / a
    n = 0
    while True:
        n += 1
        term = term * x / (a + n)
        s += term
        if a + n + 1 > 2 * x and term < Fr(1, 10 ** 70) * s:
            break
    rho = x / (a + n + 1)
    return pow_frac(M, x, an, ad) * M.exp_neg_point(x) * M.IV(s, s + term * rho / (1 - rho))


def k_integral(M, qn, qd, k0, k1):
    """int_{k0}^{k1} k^q exp(-12 k^2) dk = (1/2) 12^(-a) [gamma(a, 12 k1^2) - gamma(a, 12 k0^2)], a = (q + 1)/2."""
    an, ad = qn + qd, 2 * qd
    g = math.gcd(an, ad)
    an, ad = an // g, ad // g
    pre = pow_frac(M, Fr(1, 12), an, ad) * Fr(1, 2)
    return pre * (lower_gamma(M, an, ad, 12 * Fr(k1) ** 2) - lower_gamma(M, an, ad, 12 * Fr(k0) ** 2))


def m_ref(d, b):
    """The reference contact moment: F(b, sqrt2) = E[(b + sqrt2 z)_+^2] (d = 2), m_3(b) = E[det(B)^2 1{B > 0}] (d = 3)."""
    if d == 2:
        s = E2.isqrt_iv(E2.IV(2))
        return E2.IV(E2.elam2_pos(Fr(b), s.lo).lo, E2.elam2_pos(Fr(b), s.hi).hi)
    return E3.contact_moment(2, 0, Fr(b))


def m_ref_derivs(d, b):
    """Upper bounds of m, m', m'' at b (each increasing in b)."""
    if d == 2:
        s = E2.isqrt_iv(E2.IV(2)).hi
        return E2.elam2_pos(Fr(b), s).hi, 2 * E2.elam_pos(Fr(b), s).hi, Fr(2)
    cm = E3.contact_moment
    return cm(2, 0, Fr(b)).hi, 2 * cm(1, 1, Fr(b)).hi, 2 * cm(0, 2, Fr(b)).hi + 4 * cm(1, 0, Fr(b)).hi


def b_cells(d):
    """Enclosures of int over [j h, (j+1) h] of exp(-3b^2/4) m(b) db, h = 1/NH (midpoint rule, |g''| bounded per block)."""
    M = ENG[d]
    h = Fr(1, NH)
    out = []
    for blk in range(NH // BLOCK):
        x0, x1 = blk * BLOCK * h, (blk + 1) * BLOCK * h
        m, m1, m2 = m_ref_derivs(d, x1)
        g2 = M.exp_neg_point(3 * x0 * x0 / 4).hi * ((Fr(9, 4) * x1 * x1 + Fr(3, 2)) * m + 3 * x1 * m1 + m2)
        err = h ** 3 / 24 * g2
        for j in range(BLOCK):
            c = x0 + (j + Fr(1, 2)) * h
            out.append(M.exp_neg_point(3 * c * c / 4) * m_ref(d, c) * h + M.IV(-err, err))
    return out


def b_integral(M, cells, b0, b1):
    i0, i1 = Fr(b0) * NH, Fr(b1) * NH
    require(i0.denominator == 1 and i1.denominator == 1, 'b-box off the cell grid')
    return sum((cells[j] for j in range(int(i0), int(i1))), M.IV(0))


def K_const(d):
    """|S^(d-1)| 144 (2 pi)^(-(d+1)) / sqrt12: A_0^ref/(3 k^p) = K k^(2-p) e^(-12 k^2) e^(-3 b^2/4) m(b)."""
    M = ENG[d]
    tp = 2 * M.PI
    pw = M.IV(1)
    for _ in range(d + 1):
        pw = pw * tp
    return (tp if d == 2 else 2 * tp) * 144 / pw / M.isqrt_iv(M.IV(12))


def reference(d):
    M = ENG[d]
    cells = b_cells(d)
    K = K_const(d)
    Ib = b_integral(M, cells, 0, 1)
    c_ref = K * Ib * k_integral(M, 4, 3, Fr(1, 2), Fr(2))
    J23, J43, J13 = {}, {}, {}
    for kb in SUB_K:
        J23[kb] = k_integral(M, 2, 3, kb[0], kb[1])
        J43[kb] = k_integral(M, 4, 3, kb[0], kb[1])
    for kb in CAP_K:
        J13[kb] = k_integral(M, 1, 3, kb[0], kb[1])
    Ibs = {bb: b_integral(M, cells, bb[0], bb[1]) for bb in set(SUB_B) | set(CAP_B)}
    return {'c_ref': [dec_down(c_ref.lo, 24), dec_up(c_ref.hi, 24)],
            'w_c': [dec_up((K * Ibs[bb] * J43[kb]).hi, 24) for bb, kb in SUBBOXES],          # int A_0/(3 k^(2/3))
            'w_2': [dec_up((K * Ibs[bb] * J23[kb]).hi, 24) for bb, kb in SUBBOXES],          # int A_0/(3 k^(4/3))
            'w_cap': [dec_up((K * Ibs[bb] * J13[kb]).hi, 24) for bb, kb in CAP_BOXES]}       # int A_0/(3 k^(5/3))


# ============================================================================= 5. the refined cap sweep (engines of #206, #212)
CAPM = {}


def cap_init(d):
    CAPM['M'] = ENG[d]
    CAPM['d'] = d
    if MUT == 'cap-half':
        CAPM['M'].MUT = 'cap-half'


def cap_band(args):
    """Certified bound of sup over the band of Q^W(G_r^c)/r^3 on every refined box (rounded up, 4 places)."""
    d, r0, r1 = args
    M = ENG[d]
    if MUT == 'cap-half':
        M.MUT = 'cap-half'
    law = M.band_law(r0, r1)
    x0, th = (M.COMBOS[0] if d == 2 else M.COMBO)
    return {'r': [str(r0), str(r1)],
            'bound': [M.dec_up(M.box_bound(law, bb, kb, r0, r1, last_band=(r0 == 0), x0=x0, theta=th)['total'])
                      for bb, kb in CAP_BOXES]}


def cap_sweep(d, procs, which=None):
    bl = ENG[d].bands()
    idx = range(len(bl)) if which is None else which
    jobs = [(d, bl[i][0], bl[i][1]) for i in idx]
    if procs <= 1:
        return [cap_band(j) for j in jobs]
    with multiprocessing.Pool(procs, initializer=cap_init, initargs=(d,)) as pool:
        return pool.map(cap_band, jobs, chunksize=1)


def cap_sample(d):
    """Band indices replayed by --check: the band ending at each r_*, the band ending at 2^-20 and the last band."""
    bl = ENG[d].bands()
    ends = set(R_STARS) | {Fr(1, 2 ** 20)}
    return sorted({i for i, (r0, r1) in enumerate(bl) if r1 in ends} | {0})


# ============================================================================= 6. assembly
def assemble(d, rate, ref, cap):
    """The C_{B,K}(r_*) table, the second-order density constants, and the (12.1), (12.3) constants."""
    c_lo, c_hi = Fr(ref['c_ref'][0]), Fr(ref['c_ref'][1])
    wc = [Fr(x) for x in ref['w_c']]
    w2 = [Fr(x) for x in ref['w_2']]
    wcap = [Fr(x) for x in ref['w_cap']]
    out = {}
    for R in R_STARS:
        rr = rate[str(R)]
        a_up, e_up, a_dn, e_dn = Fr(rr['a_up']), Fr(rr['eps_up']), Fr(rr['a_dn']), Fr(rr['eps_dn'])
        c2_up = sum(Fr(row[0]) * w for row, w in zip(rr['boxes'], w2))
        c2_dn = sum(Fr(row[2]) * w for row, w in zip(rr['boxes'], w2))
        e_c_up = sum(Fr(row[1]) * w for row, w in zip(rr['boxes'], wc))
        e_c_dn = sum(Fr(row[3]) * w for row, w in zip(rr['boxes'], wc))
        Cbox = [Fr(0)] * len(CAP_BOXES)
        for rec in cap:
            if Fr(rec['r'][1]) <= R:
                for i, x in enumerate(rec['bound']):
                    Cbox[i] = max(Cbox[i], Fr(x))
        S = sum(c * w for c, w in zip(Cbox, wcap))
        CBK = (1 + a_up * R * R + e_up) * S
        out[str(R)] = {'C_BK': dec_up(CBK, 4), 'C_121': dec_up(Fr(3, 5) * CBK, 4),
                       'c2_up': dec_up(c2_up, 12), 'c2_dn': dec_up(c2_dn, 12),
                       'epsc_up': dec_up(e_c_up, 30), 'epsc_dn': dec_up(e_c_dn, 30),
                       'rel2_up': dec_up(c2_up / c_lo, 6), 'rel2_dn': dec_up(c2_dn / c_lo, 6),
                       'ell_max': '%s' % (R ** 3 / 2)}
    return out


def params():
    return {'R_STARS': [str(x) for x in R_STARS], 'TM': {'s': TM_S, 'N': TM_N, 'P': TM_P}, 'R0_COUPLING': str(R0C),
            'SUB_B': [[str(a), str(b)] for a, b in SUB_B], 'SUB_K': [[str(a), str(b)] for a, b in SUB_K],
            'NH': NH, 'BLOCK': BLOCK, 'CAP_B': [[str(a), str(b)] for a, b in CAP_B], 'CAP_K': [[str(a), str(b)] for a, b in CAP_K],
            'band': {'b': ['0', '1'], 'k': ['1/2', '2']}, 'L_min': 10}


def compute_core(d):
    tml = tm_law(d)
    return tm_summary(tml), rate_sweep(d, tml), reference(d)


def full_run(procs):
    res = {'schema': 1, 'object': 'CL-C8-LIFETIME-DIFFERENCE-CONSTANT-20261001-v1', 'scientific_effect': 'NONE',
           'certified': True, 'mutant': None, 'parameters': params(), 'dims': {}}
    for d in (2, 3):
        summ, rate, ref = compute_core(d)
        cap = cap_sweep(d, procs)
        res['dims'][str(d)] = {'tm_law': summ, 'rate': rate, 'reference': ref, 'table': assemble(d, rate, ref, cap),
                               'cap_boxes': [[str(bb[0]), str(bb[1]), str(kb[0]), str(kb[1])] for bb, kb in CAP_BOXES],
                               'cap_bands': cap}
    return res


def results_text(res):
    """Canonical layout: everything indented except the cap-band records, one line each."""
    caps = {d: res['dims'][d].pop('cap_bands') for d in res['dims']}
    head = json.dumps(res, indent=1, sort_keys=True)
    for d in res['dims']:
        res['dims'][d]['cap_bands'] = caps[d]
    tail = ',\n "cap_bands": {\n' + ',\n'.join(
        '  "%s": [\n' % d + ',\n'.join('   ' + json.dumps(rec, sort_keys=True) for rec in caps[d]) + '\n  ]'
        for d in sorted(caps)) + '\n }\n}\n'
    return head[:-2] + tail


def load_results():
    with open(os.path.join(HERE, 'RESULTS.json')) as fh:
        res = json.load(fh)
    for d, recs in res.pop('cap_bands').items():
        res['dims'][d]['cap_bands'] = recs
    return res


def check_run(procs, full=False):
    res = load_results()
    with open(os.path.join(HERE, 'RESULTS.json')) as fh:
        require(fh.read() == results_text(res), 'RESULTS.json is not in canonical layout')
    require(res['parameters'] == params(), 'parameters differ')
    require(res['mutant'] is None and res['certified'] is True, 'header')
    for d in (2, 3):
        rd = res['dims'][str(d)]
        tml = tm_law(d)
        require(tm_summary(tml) == rd['tm_law'], 'Taylor-model law differs (d = %d)' % d)
        rate = rate_sweep(d, tml)
        require(rate == rd['rate'], 'rate sweep differs (d = %d)' % d)
        ref = reference(d)
        require(ref == rd['reference'], 'reference integrals differ (d = %d)' % d)
        c_lo, c_hi = Fr(ref['c_ref'][0]), Fr(ref['c_ref'][1])
        cx = C_REF_197 if d == 2 else C_REF_205
        require(c_lo <= cx <= c_hi, 'reference c_{B,K} does not contain the value of Math-#197/#205 (d = %d)' % d)
        require(rd['cap_boxes'] == [[str(bb[0]), str(bb[1]), str(kb[0]), str(kb[1])] for bb, kb in CAP_BOXES], 'cap boxes')
        bl = ENG[d].bands()
        require([rec['r'] for rec in rd['cap_bands']] == [[str(a), str(b)] for a, b in bl], 'cap band layout (d = %d)' % d)
        which = None if full else cap_sample(d)
        recs = cap_sweep(d, procs, which)
        for i, rec in zip(range(len(bl)) if which is None else which, recs):
            require(rec == rd['cap_bands'][i], 'cap band %d differs (d = %d)' % (i, d))
        require(assemble(d, rate, ref, rd['cap_bands']) == rd['table'], 'assembled table differs (d = %d)' % d)
    print('CHECK PASSED (%s)' % ('full' if full else 'sample'))


# ============================================================================= 7. floating controls (not part of the certificate)
def controls():
    """Floating estimates of the reference-kernel cap-route benchmarks Gamma_{B,K} = |S| int A_0^ref c_G / (3 k^(5/3)) for comparison with C_{B,K}:
    planar c_G = R(b) J(k) of Math-#203 with J(k) = 2359296 k^3 (1 + delta(k)), delta(1/2) = 0.0232, delta(3/4) = 1.3e-4;
    d = 3 from the floating R_3(b) R(b) and J^(3)/J ratios of Math-#208."""
    from math import exp, pi, sqrt, erf
    out = {}
    K2 = 2 * pi * 144 / (2 * pi) ** 3 / sqrt(12)
    Ib2 = sqrt(pi) / 2 * erf(1) / (2 * sqrt(pi))                 # int_0^1 e^{-b^2} db / (2 sqrt(pi)) (m R = p_w(0))
    def J2(k):
        dl = 0.0232 + (k - 0.5) / 0.25 * (1.3e-4 - 0.0232) if k < 0.75 else 1.3e-4 * max(0.0, (1 - k) / 0.25)
        return 2359296 * k ** 3 * (1 + dl)
    n = 200000
    Ik2 = sum(((0.5 + (i + 0.5) * 1.5 / n) ** (1 / 3)) * exp(-12 * (0.5 + (i + 0.5) * 1.5 / n) ** 2) * J2(0.5 + (i + 0.5) * 1.5 / n)
              * 1.5 / n for i in range(n))
    out['Gamma_2'] = K2 * Ib2 * Ik2
    bs = [0, 0.25, 0.5, 0.75, 1.0]
    m3 = [0.6715728752625627, 1.195532362807149, 2.05794812257308, 3.43079921823, 5.54806027367761]
    r3r = [1.1880833639847637, 0.9085531055205767, 0.6853903187865128, 0.5096151204445851, 0.37314989157732215]
    f = [exp(-0.75 * b * b) * m * r for b, m, r in zip(bs, m3, r3r)]
    Ib3 = 0.25 / 3 * (f[0] + 4 * f[1] + 2 * f[2] + 4 * f[3] + f[4])
    K3 = 4 * pi * 144 / (2 * pi) ** 4 / sqrt(12)
    def J3(k):
        dl = 0.1617 + (k - 0.5) / 0.25 * (0.0012 - 0.1617) if k < 0.75 else 0.0012 * max(0.0, (1 - k) / 0.25)
        return 2359296 * k ** 3 * (1 + dl)
    Ik3 = sum(((0.5 + (i + 0.5) * 1.5 / n) ** (1 / 3)) * exp(-12 * (0.5 + (i + 0.5) * 1.5 / n) ** 2) * J3(0.5 + (i + 0.5) * 1.5 / n)
              * 1.5 / n for i in range(n))
    out['Gamma_3'] = K3 * Ib3 * Ik3
    return out


def mc_ratio(d, n, seed=20261001):
    """Floating Monte Carlo of (A_r/A_0^ref - 1)/r^2 for the reference kernel at r = 1/8, 1/16: the exact law at r from the
    series (all r, not only r <= 1/64), Z_r/r^2 by sampling W_r/r^2 = P1 P2 1{typed}, and the exact pin ratio."""
    import random
    M = ENG[d]
    names = ('w', 'v', 'om', 'T', 'tau', 'nu') if d == 2 else \
        ('a11', 'a22', 'a12', 'v1', 'v2', 'o11', 'o22', 'o12', 'T', 'tau', 'nu1', 'nu2')
    pins, targets = M.functionals()
    P = [pins[x] for x in M.PIN_NAMES]
    idx = [M.TARGET_NAMES.index(x) for x in names]
    Tf = [targets[x] for x in names]
    tml = tm_law(d)
    def cov(F, G, key, r):
        ser, w, _ = M.pair_series(F, G, key)
        return sum(c * r ** p for p, c in ser.items())
    def law(r, b, k):
        n_ = len(P)
        S = [[None] * n_ for _ in range(n_)]
        for i in range(n_):
            for j in range(i, n_):
                S[i][j] = S[j][i] = cov(P[i], P[j], ('p', i, j), r)
        Stp = [[cov(Tf[a], P[j], ('tp', idx[a], j), r) for j in range(n_)] for a in range(len(Tf))]
        Mx = [list(S[i]) + [Stp[a][i] for a in range(len(Tf))] for i in range(n_)]
        for col in range(n_):
            for i in range(col + 1, n_):
                f = Mx[i][col] / Mx[col][col]
                for j in range(col, len(Mx[i])):
                    Mx[i][j] -= f * Mx[col][j]
        W = []
        for a in range(len(Tf)):
            x = [None] * n_
            for i in reversed(range(n_)):
                x[i] = (Mx[i][n_ + a] - sum(Mx[i][j] * x[j] for j in range(i + 1, n_))) / Mx[i][i]
            W.append(x)
        kv = [-r ** 3 / 2, -r ** 2, Fr(12)] + [Fr(0)] * (n_ - 3)
        mu = [float(b * W[a][0] + k * sum(W[a][j] * kv[j] for j in range(n_))) for a in range(len(Tf))]
        def stt(a, c):
            i, j = idx[a], idx[c]
            return cov(Tf[a], Tf[c], ('tt', i, j), r) if i <= j else cov(Tf[c], Tf[a], ('tt', j, i), r)
        C = [[float(stt(a, c) - sum(W[a][l] * Stp[c][l] for l in range(n_))) for c in range(len(Tf))] for a in range(len(Tf))]
        L = [[0.0] * len(C) for _ in C]
        for i in range(len(C)):
            for j in range(i + 1):
                s = C[i][j] - sum(L[i][l] * L[j][l] for l in range(j))
                L[i][j] = math.sqrt(max(s, 0.0)) if i == j else (s / L[j][j] if L[j][j] > 0 else 0.0)
        return mu, L
    rng = random.Random(seed)
    out = []
    for r in (Fr(1, 8), Fr(1, 16)):
        rf = float(r)
        for b, k in ((Fr(0), Fr(1, 2)), (Fr(0), Fr(2)), (Fr(1), Fr(1, 2)), (Fr(1), Fr(2))):
            mu, L = law(r, b, k)
            kf = float(k)
            tot = tot2 = 0.0
            for _ in range(n):
                z = [rng.gauss(0.0, 1.0) for _ in mu]
                x = [mu[i] + sum(L[i][j] * z[j] for j in range(i + 1)) for i in range(len(mu))]
                if d == 2:
                    w, v, om, T, tau, nu = x
                    lam = -w
                    c1, c2 = 6 * kf - rf * T, 6 * kf + rf * T + rf * rf * tau
                    P1 = c1 * lam - rf * v * v
                    P2 = c2 * (lam - rf * om) + rf * (rf * nu - v) ** 2
                    Wv = P1 * P2 if (c1 > 0 and P1 > 0 and P2 > 0) else 0.0
                else:
                    a11, a22, a12, v1, v2, o11, o22, o12, T, tau, nu1, nu2 = x
                    B = (-a11, -a22, -a12)
                    S_ = (B[0] - rf * o11, B[1] - rf * o22, B[2] - rf * o12)
                    detB, detS = B[0] * B[1] - B[2] ** 2, S_[0] * S_[1] - S_[2] ** 2
                    c1, c2 = 6 * kf - rf * T, 6 * kf + rf * T + rf * rf * tau
                    e1, e2 = rf * nu1 - v1, rf * nu2 - v2
                    P1 = c1 * detB - rf * (B[1] * v1 * v1 - 2 * B[2] * v1 * v2 + B[0] * v2 * v2)
                    P2 = c2 * detS + rf * (S_[1] * e1 * e1 - 2 * S_[2] * e1 * e2 + S_[0] * e2 * e2)
                    Wv = 0.0
                    if B[0] > 0 and detB > 0 and P1 > 0 and P2 > 0:
                        # index(H_S) = 2: sign changes of the leading minors (-S_11, det S, r P2) of H_S reordered (y1, y2, x)
                        m1, m2, m3 = -S_[0], detS, rf * P2
                        if m1 != 0 and m2 != 0:
                            neg = (m1 < 0) + (m2 / m1 < 0) + (m3 / m2 < 0)
                            Wv = P1 * P2 if neg == 2 else 0.0
                tot += Wv
                tot2 += Wv * Wv
            mean = tot / n
            se = math.sqrt(max(tot2 / n - mean * mean, 0.0) / n)
            mref = float(m_ref(d, b).mid())
            zr, zse = mean / (36 * kf * kf * mref), se / (36 * kf * kf * mref)
            ev = lambda t: sum(float(c) * rf ** j for j, c in enumerate(t.frac_coeffs()))
            E = ev(tml.e_bb) * float(b) ** 2 + 2 * ev(tml.e_bk) * float(b) * kf + ev(tml.e_kk) * kf * kf
            pr = math.sqrt(12 / ev(tml.det)) * math.exp(-(E - (1.5 * float(b) ** 2 + 24 * kf * kf)) / 2)
            out.append({'d': d, 'r': str(r), 'b': str(b), 'k': str(k), 'n': n, 'Z_ratio': round(zr, 5), 'Z_se': round(zse, 5),
                        'pin_ratio': round(pr, 6), 'coef': round((pr * zr - 1) / rf ** 2, 3), 'coef_se': round(pr * zse / rf ** 2, 3)})
    return out


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--check-full', action='store_true')
    ap.add_argument('--mutant', choices=MUTANTS)
    ap.add_argument('--procs', type=int, default=4)
    ap.add_argument('--controls', action='store_true')
    args = ap.parse_args()
    MUT = args.mutant
    if args.controls:
        out = controls()
        out['mc'] = mc_ratio(2, 200000) + mc_ratio(3, 100000)
        print(json.dumps(out, indent=1))
        return
    if args.check or args.check_full:
        check_run(args.procs, full=args.check_full)
        return
    require(MUT is None, 'a mutant cannot regenerate RESULTS.json')
    res = full_run(args.procs)
    with open(os.path.join(HERE, 'RESULTS.json'), 'w') as fh:
        fh.write(results_text(res))
    print(json.dumps({d: {R: row['C_BK'] for R, row in res['dims'][d]['table'].items()} for d in res['dims']}))


if __name__ == '__main__':
    main()
