#!/usr/bin/env python3
"""Theorem L' (NOTE.md): the radial ledger of [LP] Theorem B on the C8 band with a VANISHING remainder, d = 2 and d = 3.

For the torus kernel (every side L >= 10, every frame) and for the reference kernel, b in [0, 1], k in [1/2, 2], 0 < r <= R:

    -(a_dn r^2 + beta_dn r)  <=  A_r(b, k, u) / A_0(b, k, u) - 1  <=  a_up r^2 + beta_up r,

where A_0 = lim_{r -> 0} A_r is the contact integrand of THE SAME kernel (for the torus: its own A_0^(L), not the Gaussian
A_0^ref).  Math-#215 (Theorem L) proved the same shape against A_0^ref with an additive, r-independent eps_d; here every
remainder carries a positive power of r.  The first-order coefficient beta collects the torus corrections only (about
1e-12); for the reference kernel it is exactly 0 (torus=False gives M1 = 0, and the computed beta is the rational 0: its
upward-rounded stored values are all 0).

Method (NOTE.md sections 2-5):
- Taylor models with INTERVAL coefficients and a remainder proportional to r^(N+1) (class TV): every rounding goes into a
  coefficient radius, every truncation into the r^(N+1) remainder.  The value at r = 0 is the constant coefficient, so
  t(r) - t(0) is controlled by the coefficients of r^1, r^2, ... only.
- The torus part of each covariance has the coefficient majorant |tau_p| <= T0 e^p (Cauchy estimates and
  g_x!/(g_x - A)! <= w^A e^(g_x - w), as in the engines of Math-#206/#212); it enters as radii T0 e^p on the coefficients
  p <= N and as T0 e^(N+1)/(1 - e R) r^(N+1).
- Increments against r = 0: the pin-density ratio pi_r/pi_0 (the kernel normalization Theta multiplies increments only),
  the main normalizer term by the derivative bound dF = 2 E[lambda_+] dmu + Phi(mu/sigma) d(sigma^2) (d = 2) and by a Gaussian
  gradient coupling with |grad det(B)^2 1{B > 0}| <= ||B||_F^3 (d = 3); first-order terms carry an explicit factor r; the
  thin set and the far set G_0^c by Markov at a high moment (r^2).
- The interval band laws, the second-order term bounds and the reference integrals are those of Math-#215's theorem_b.py and
  the engines of Math-#206/#212, as byte-identical pinned copies (SOURCE_MAP.json).

  python3 -B -S theorem_v.py --write        regenerate RESULTS.json
  python3 -B -S theorem_v.py --check        replay and compare with RESULTS.json (exact)
  python3 -B -S theorem_v.py --mutant NAME  a semantic mutation; the replay must then fail (exit 1)
"""
import argparse
import importlib.util
import json
import math
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OBJECT = 'CL-C8-TORUS-VANISHING-REMAINDER-20261001-v1'
MUTANTS = ('torus-const-only', 'exp-radius', 'no-lin', 'no-om-term', 'coupling-half')
MUT = None


def require(cond, msg):
    if not cond:
        raise SystemExit('FAIL: ' + msg)


def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


TB = _load('theorem_b', 'theorem_b.py')         # Math-#215, pinned byte-identical copy (loads engine_e2.py, engine_e3.py)
E2, E3, ENG = TB.E2, TB.E3, TB.ENG
R_STARS = TB.R_STARS
SUBBOXES, SUB_K = TB.SUBBOXES, TB.SUB_K
TM_S, TM_N, TM_P = TB.TM_S, TB.TM_N, TB.TM_P
TINY = TB.TINY
E_UP = Fr(27183, 10000)                          # > e
SQRT2_UP = Fr(14143, 10000)                      # > sqrt(2)
MARKOV_P = 64                                    # moment order of the far-set bound
dec_up, dec_down, cdiv = TB.dec_up, TB.dec_down, TB.cdiv


# ============================================================================= 1. interval-coefficient Taylor models
class TV:
    """f(r) = sum_{j <= N} c_j r^j + rho(r) for 0 <= r <= 2^-s, with FIXED (r-independent) coefficients
    c_j in [(C_j - D_j)/2^P, (C_j + D_j)/2^P] and |rho(r)| <= (E/2^P) r^(N+1).  In particular f(0) = c_0.
    Preconditions (the reuse boundary; reviews C56, C63): C and D are integer lists of length N + 1 with every D_j >= 0;
    E is an integer >= 0; s >= 0 and N >= 0 are integers, with N >= 2 for the second-order readers (inc, absinc and
    their callers read coeff(2)); the operands of +, -, * share (s, N); powers are nonnegative integers; reader radii
    and scalars are exact rationals, with 0 < R <= 2^-s; the lists are not mutated after construction.  The certificate
    meets all of them (s = TM_S, N = TM_N = 8); inputs outside them are not covered."""
    __slots__ = ('C', 'D', 'E', 's', 'N')

    def __init__(self, C, D, E, s, N):
        self.C, self.D, self.E, self.s, self.N = C, D, E, s, N

    @classmethod
    def build(cls, centers, radii, e, s, N):
        """centers, radii: {power: rational}; e: rational coefficient of r^(N+1) in the remainder bound."""
        C, D = [0] * (N + 1), [0] * (N + 1)
        R = Fr(1, 2 ** s)
        E = Fr(e)
        for p, x in centers.items():
            x = Fr(x)
            if x == 0:
                continue
            if p <= N:
                v = round(x * (1 << TM_P))
                C[p] += v
                if x * (1 << TM_P) != v:
                    D[p] += 1
            else:
                E += abs(x) * R ** (p - N - 1)
        for p, x in radii.items():
            x = Fr(x)
            if p <= N:
                D[p] += cdiv((x * (1 << TM_P)).numerator, (x * (1 << TM_P)).denominator)
            else:
                E += x * R ** (p - N - 1)
        return cls(C, D, cdiv(E.numerator << TM_P, E.denominator), s, N)

    @classmethod
    def const(cls, x, s, N, rad=0):
        return cls.build({0: Fr(x)}, {0: Fr(rad)} if rad else {}, 0, s, N)

    def zero(self):
        return TV([0] * (self.N + 1), [0] * (self.N + 1), 0, self.s, self.N)

    def polybound(self):
        """Upper bound (units 2^-P) of |sum c_j r^j| on [0, 2^-s]."""
        return sum(cdiv(abs(c) + d, 1 << (self.s * j)) for j, (c, d) in enumerate(zip(self.C, self.D)) if c or d)

    def __add__(self, o):
        if not isinstance(o, TV):
            o = TV.const(o, self.s, self.N)
        return TV([a + b for a, b in zip(self.C, o.C)], [a + b for a, b in zip(self.D, o.D)], self.E + o.E, self.s, self.N)
    __radd__ = __add__

    def __neg__(self):
        return TV([-a for a in self.C], list(self.D), self.E, self.s, self.N)

    def __sub__(self, o):
        if not isinstance(o, TV):
            o = TV.const(o, self.s, self.N)
        return self + (-o)

    def scale(self, x):
        x = Fr(x)
        C, D = [], []
        for c, d in zip(self.C, self.D):
            v = c * x
            w = round(v)
            C.append(w)
            D.append(cdiv((d * abs(x)).numerator, (d * abs(x)).denominator) + (1 if v != w else 0))
        e = self.E * abs(x)
        return TV(C, D, cdiv(e.numerator, e.denominator), self.s, self.N)

    def __mul__(self, o):
        if not isinstance(o, TV):
            return self.scale(o)
        N, s = self.N, self.s
        S = [0] * (2 * N + 1)
        Rd = [0] * (2 * N + 1)
        for i, (a, da) in enumerate(zip(self.C, self.D)):
            if a or da:
                for j, (b, db) in enumerate(zip(o.C, o.D)):
                    if b or db:
                        S[i + j] += a * b
                        Rd[i + j] += abs(a) * db + da * abs(b) + da * db
        C, D, E = [], [], 0
        for k in range(N + 1):
            v = S[k] >> TM_P
            C.append(v)
            D.append(cdiv(Rd[k], 1 << TM_P) + (1 if S[k] - (v << TM_P) else 0))
        for k in range(N + 1, 2 * N + 1):
            if S[k] or Rd[k]:
                E += cdiv(abs(S[k]) + Rd[k], 1 << (TM_P + s * (k - N - 1)))
        E += cdiv(self.E * o.polybound() + o.E * self.polybound(), 1 << TM_P)
        E += cdiv(self.E * o.E, 1 << (TM_P + s * (N + 1)))
        return TV(C, D, E, s, N)
    __rmul__ = __mul__

    def c0(self):
        return Fr(self.C[0] - self.D[0], 1 << TM_P), Fr(self.C[0] + self.D[0], 1 << TM_P)

    def lin_bound(self):
        """G with |f(r) - f(0)| <= G r on [0, 2^-s] (exact rational)."""
        R = Fr(1, 2 ** self.s)
        g = sum(Fr(abs(c) + d, 1 << TM_P) * R ** (j - 1) for j, (c, d) in enumerate(zip(self.C, self.D)) if j >= 1)
        return g + Fr(self.E, 1 << TM_P) * R ** self.N

    def inv(self):
        lo, hi = self.c0()
        require(lo > 0 or hi < 0, 'TV inverse at a constant term containing 0')
        # centered at 1/C_0 (so that centers stay the reference values), radius covering [1/hi, 1/lo]
        uc = Fr(1 << TM_P, self.C[0])
        u = TV.build({0: uc}, {0: max(abs(1 / hi - uc), abs(1 / lo - uc))}, 0, self.s, self.N)
        h = TV([0] + self.C[1:], [0] + self.D[1:], self.E, self.s, self.N)
        g = h * u
        require(g.C[0] == 0 and g.D[0] == 0, 'TV inverse: g(0) = 0')
        G1 = g.lin_bound()
        R = Fr(1, 2 ** self.s)
        require(G1 * R < Fr(1, 2), 'TV inverse: |g| too large')
        acc = TV.const(1, self.s, self.N)
        p = TV.const(1, self.s, self.N)
        mg = -g
        for _ in range(self.N):
            p = p * mg
            acc = acc + p
        tail = G1 ** (self.N + 1) / (1 - G1 * R)
        acc = TV(acc.C, acc.D, acc.E + cdiv(tail.numerator << TM_P, tail.denominator), self.s, self.N)
        return acc * u

    # ----------------------------------------------------------------------------- readers
    def coeff(self, j):
        return Fr(self.C[j] - self.D[j], 1 << TM_P), Fr(self.C[j] + self.D[j], 1 << TM_P)

    def high(self, R):
        """H with |sum_{j >= 3} c_j r^j + rho(r)| <= H r^2 on (0, R]."""
        h = sum(Fr(abs(c) + d, 1 << TM_P) * R ** (j - 2) for j, (c, d) in enumerate(zip(self.C, self.D)) if j >= 3)
        return h + Fr(self.E, 1 << TM_P) * R ** (self.N - 1)

    def inc(self, R):
        """(l_lo, l_hi, q_lo, q_hi): f(r) - f(0) in [l_lo r + q_lo r^2, l_hi r + q_hi r^2] for 0 < r <= R."""
        l_lo, l_hi = self.coeff(1)
        q_lo, q_hi = self.coeff(2)
        H = self.high(R)
        if MUT == 'no-lin':
            l_lo = l_hi = Fr(0)
        return l_lo, l_hi, q_lo - H, q_hi + H

    def absinc(self, R):
        """(a, b): |f(r) - f(0)| <= a r^2 + b r."""
        l_lo, l_hi, q_lo, q_hi = self.inc(R)
        return max(abs(q_lo), abs(q_hi)), max(abs(l_lo), abs(l_hi))

    def absval(self, R):
        """(s, c): |f(r)| <= c + s r on [0, R], c = sup |c_0|."""
        lo, hi = self.c0()
        s = sum(Fr(abs(c) + d, 1 << TM_P) * R ** (j - 1) for j, (c, d) in enumerate(zip(self.C, self.D)) if j >= 1)
        return s + Fr(self.E, 1 << TM_P) * R ** self.N, max(abs(lo), abs(hi))

    def enclose(self, R):
        """Interval of f(r) over r in [0, R]."""
        lo, hi = self.c0()
        for j in range(1, self.N + 1):
            a, b = self.coeff(j)
            Rj = R ** j
            lo += min(a, 0) * Rj
            hi += max(b, 0) * Rj
        e = Fr(self.E, 1 << TM_P) * R ** (self.N + 1)
        return lo - e, hi + e

    def center(self, j):
        return Fr(self.C[j], 1 << TM_P)


def cov_tv(M, F, G, key, s, N, M1):
    """TV on [0, 2^-s] of the covariance of F, G under the unnormalized torus kernel: the exact reference series (centers),
    the Taylor truncation tail (gx > NX, proportional to r^(NX+1-w)) and the torus part sum_p tau_p r^p with
    |tau_p| <= T0 e^p (radii T0 e^p for p <= N, remainder T0 e^(N+1)/(1 - e R) r^(N+1))."""
    R = Fr(1, 2 ** s)
    ser, w, absterms = M.pair_series(F, G, key)
    A = max((t[1] for t in absterms), default=0)
    tail = T0 = Fr(0)
    for t in absterms:
        acc, aa, gys = t[0], t[1], t[2:]
        hprod = fprod = 1
        for g in gys:
            hprod *= M.hcoef(g)
            fprod *= math.factorial(g)
        tail += acc * abs(hprod)
        T0 += acc * fprod * Fr(max(w, 1)) ** aa
    require(M.NX + 1 - w >= N + 1, 'truncation tail below the Taylor-model order')
    tail_e = 2 * Fr(M.NX + 1) ** A * tail * R ** (M.NX + 1 - w - (N + 1))
    T0 = T0 * M1
    eu = Fr(1) if MUT == 'exp-radius' else E_UP
    if MUT == 'torus-const-only':
        radii = {0: T0}
        tor_e = Fr(0)
    else:
        radii = {p: T0 * eu ** p for p in range(N + 1)}
        tor_e = T0 * eu ** (N + 1) / (1 - eu * R)
    return TV.build(ser, radii, tail_e + tor_e, s, N)


def solve_tv(A, B):
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


class Law:
    pass


def tv_law(d, torus=True, s=TM_S, N=TM_N, L=10):
    """The TV law over [0, 2^-s] of the targets TB.TM_NAMES[d]: as TB.tm_law, with interval-coefficient models."""
    M = ENG[d]
    names = TB.TM_NAMES[d]
    pins, targets = M.functionals()
    P = [pins[nm] for nm in M.PIN_NAMES]
    idx = [M.TARGET_NAMES.index(nm) for nm in names]
    T = [targets[nm] for nm in names]
    M1 = M.torus_M1(L) if torus else Fr(0)
    n, nt = len(P), len(T)
    Spp = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            Spp[i][j] = Spp[j][i] = cov_tv(M, P[i], P[j], ('p', i, j), s, N, M1)
    Stp = [[cov_tv(M, T[a], P[j], ('tp', idx[a], j), s, N, M1) for j in range(n)] for a in range(nt)]
    Stt = [[None] * nt for _ in range(nt)]
    for a in range(nt):
        for b in range(a, nt):
            i, j = idx[a], idx[b]
            if i <= j:
                Stt[a][b] = Stt[b][a] = cov_tv(M, T[a], T[b], ('tt', i, j), s, N, M1)
            else:
                Stt[a][b] = Stt[b][a] = cov_tv(M, T[b], T[a], ('tt', j, i), s, N, M1)
    zero = TV.const(0, s, N)
    kvec = [TV.build({3: Fr(-1, 2)}, {}, 0, s, N), TV.build({2: Fr(-1)}, {}, 0, s, N), TV.const(12, s, N)] + [zero] * (n - 3)
    e1 = [TV.const(1, s, N)] + [zero] * (n - 1)
    X, det = solve_tv(Spp, Stp + [e1, kvec])
    W, xs0, xs1 = X[:nt], X[nt], X[nt + 1]
    law = Law()
    law.d, law.M1, law.s, law.N = d, M1, s, N
    law.th1 = M.theta_minus_one(L) if torus else Fr(0)
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
        an = ('a11', 'a22', 'a12')
        Xg, _ = solve_tv([[law.Cu[(x, y)] for y in an] for x in an], [[law.Cu[(o, y)] for y in an] for o in ('o11', 'o22', 'o12')])
        law.G = {o: [-Xg[c][l] for l in range(3)] for c, o in enumerate(('o11', 'o22', 'o12'))}
    return law


def tv_summary(law):
    """Low-order centers and radii (decimal, 30 places) and remainder coefficients of the TV law, for the record."""
    def row(t):
        out = {'c': [], 'rad': []}
        for j in range(4):
            x = t.center(j)
            out['c'].append(dec_down(x, 30) if x >= 0 else dec_up(x, 30))
            out['rad'].append(dec_up(Fr(t.D[j], 1 << TM_P), 30))
        out['rem_r9'] = dec_up(Fr(t.E, 1 << TM_P), 30)
        return out
    out = {'det': row(law.det), 'e_bb': row(law.e_bb), 'e_bk': row(law.e_bk), 'e_kk': row(law.e_kk)}
    for nm in law.alpha:
        out['alpha_' + nm] = row(law.alpha[nm])
        out['beta_' + nm] = row(law.beta[nm])
    names = TB.TM_NAMES[law.d]
    for i, a in enumerate(names):
        for b in names[i:]:
            out['C_%s_%s' % (a, b)] = row(law.Cu[(a, b)])
    return out


# ============================================================================= 2. (a, b) forms: a r^2 + b r
def ab_add(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def ab_mul(x, c):
    return (x[0] * c, x[1] * c)


def ab_at(x, R):
    return x[0] * R * R + x[1] * R


def ab_norm(xs):
    """Minkowski: || (a_i r^2 + b_i r)_i ||_2 <= sqrt(sum a_i^2) r^2 + sqrt(sum b_i^2) r."""
    return (E3.sqrt_up(sum(x[0] * x[0] for x in xs)), E3.sqrt_up(sum(x[1] * x[1] for x in xs)))


def exp_up_ab(M, x, R):
    """exp(a r^2 + b r) - 1 <= (a r^2 + b r) exp(a R^2 + b R) on (0, R]."""
    f = TB.exp_minus(M, -ab_at(x, R)).hi
    return (x[0] * f, x[1] * f)


def flat(t, ref, what):
    """The reference part (centers) of t is the constant ref for every r (Lemma 1 of Math-#215)."""
    require(abs(t.center(0) - ref) <= TINY and all(abs(t.center(j)) <= TINY for j in range(1, t.N + 1)),
            'the reference law of %s is not flat in r' % what)


def mean_inc(law, nm, b1, k1, R):
    """|mu(r) - mu(0)| for mu = b alpha + k beta (b <= b1, k <= k1), in (a, b) form."""
    return ab_add(ab_mul(law.alpha[nm].absinc(R), b1), ab_mul(law.beta[nm].absinc(R), k1))


def pi_ratio_v(law, Q, R):
    """log(pi_r / pi_0) in [-dn, up] for the SAME kernel: pi_r ~ det(S_r/Theta)^(-1/2) exp(-Theta E_r/2), so
    log(pi_r/pi_0) = -(1/2) log(det S_r/det S_0) - Theta (E_r - E_0)/2; Theta in [1, 1 + th1] multiplies increments only."""
    b0, b1, k0, k1 = Q
    th1 = law.th1
    l_lo, l_hi, q_lo, q_hi = law.det.inc(R)
    d0lo = law.det.c0()[0]
    require(d0lo > 0, 'pin determinant at r = 0')
    xm = (max(abs(q_lo), abs(q_hi)) * R * R + max(abs(l_lo), abs(l_hi)) * R) / d0lo
    require(xm < Fr(1, 2), 'pin determinant increment')
    up = (max(Fr(0), -q_lo) / (2 * d0lo * (1 - xm)), max(Fr(0), -l_lo) / (2 * d0lo * (1 - xm)))
    dn = (max(Fr(0), q_hi) / (2 * d0lo), max(Fr(0), l_hi) / (2 * d0lo))
    parts = ((law.e_bb, (b0 * b0, b1 * b1)), (law.e_bk, (2 * b0 * k0, 2 * b1 * k1)), (law.e_kk, (k0 * k0, k1 * k1)))
    EL = EH = EQ = EP = Fr(0)
    for t, (wlo, whi) in parts:
        a_lo, a_hi, c_lo, c_hi = t.inc(R)
        EL += min(wlo * a_lo, whi * a_lo)
        EH += max(wlo * a_hi, whi * a_hi)
        EQ += min(wlo * c_lo, whi * c_lo)
        EP += max(wlo * c_hi, whi * c_hi)
    f = (1 + th1) / 2
    up = ab_add(up, (f * max(Fr(0), -EQ), f * max(Fr(0), -EL)))
    dn = ab_add(dn, (f * max(Fr(0), EP), f * max(Fr(0), EH)))
    return up, dn


def combine_v(M, p_up, p_dn, z_up, z_dn, R):
    """A_r/A_0 = (pi_r/pi_0) (z_r/z_0): (1 + pu)(1 + zu) - 1 <= pu + zu + pu zu(R); 1 - (1 - pd)(1 - zd) <= pd + zd.
    The lower sum is valid even when one lower estimate exceeds 1 (review C58): if pd + zd >= 1 it holds because both ratios
    are positive; otherwise 0 <= 1 - pd, 1 - zd and the two lower factors may be multiplied."""
    pu = exp_up_ab(M, p_up, R)
    zR = ab_at(z_up, R)
    up = (pu[0] + z_up[0] + pu[0] * zR, pu[1] + z_up[1] + pu[1] * zR)
    return up, ab_add(p_dn, z_dn)


def far_set(M, ma_T, sd_T, ma_tau, sd_tau, k0, R):
    """q4 with P(G_0^c) <= q4 r^4 on (0, R]: G_0^c = {|T| > 3k/(2r)} u {|tau| > 3k/(2r^2)}, Markov at order p = MARKOV_P:
    P(|X| > t) <= (||X||_p / t)^p, and r^p <= R^(p-4) r^4, r^(2p) <= R^(2p-4) r^4."""
    p = MARKOV_P
    nT = M.gauss_norm(ma_T, sd_T, p)
    nt = M.gauss_norm(ma_tau, sd_tau, p)
    c = Fr(2) / (3 * k0)
    q4 = (nT * c) ** p * R ** (p - 4) + (nt * c) ** p * R ** (2 * p - 4)
    return q4


# ============================================================================= 3. the ratio A_r / A_0 on a (b, k) box
def bounds_d2_v(Q, R, law, il):
    """(up, dn) in (a, b) form: A_r/A_0 - 1 <= up(r), 1 - A_r/A_0 <= dn(r) on the box, 0 < r <= R (NOTE sections 3-4)."""
    M = E2
    b0, b1, k0, k1 = Q
    th1 = law.th1
    flat(law.alpha['w'], -1, 'alpha_w')
    flat(law.beta['w'], 0, 'beta_w')
    flat(law.Cu[('w', 'w')], 2, 'Var w')
    # law of lambda = -w at r and at 0: mean mu = -(b alpha_w + k beta_w), variance Cu_ww / Theta
    sA, cA = (law.alpha['w'] + 1).absval(R)
    sB, cB = law.beta['w'].absval(R)
    Dm = b1 * (cA + sA * R) + k1 * (cB + sB * R)                      # sup |mu - b| over [0, R]
    sC, cC = (law.Cu[('w', 'w')] - 2).absval(R)
    Sm = cC + sC * R
    s_lo = M.isqrt_iv(M.IV((2 - Sm) / (1 + th1))).lo
    s_hi = M.isqrt_iv(M.IV(2 + Sm)).hi
    m_lo, m_hi = b0 - Dm, b1 + Dm
    mmax = max(abs(m_lo), abs(m_hi))
    Fmin = M.elam2_pos(m_lo, s_lo).lo                               # <= F_r and <= F_0
    Fmax = M.elam2_pos(m_hi, s_hi).hi
    F1max = M.elam_pos(m_hi, s_hi).hi
    # main term: |F(mu_r, s_r) - F(mu_0, s_0)| <= 2 E[lambda_+] |dmu| + Phi(mu/s) |d(s^2)| along the segment (both <= sup)
    dmu = mean_inc(law, 'w', b1, k1, R)
    dS = law.Cu[('w', 'w')].absinc(R)                               # |d(s^2)| <= |dCu| / Theta, Theta >= 1
    Fae = ab_mul(ab_add(ab_mul(dmu, 2 * F1max), dS), 1 / Fmin)
    norm = 36 * k0 * k0 * Fmin                                      # 36 k^2 F_0 >= norm
    b, k = M.IV(b0, b1), M.IV(k0, k1)
    ma = {nm: M.absup(b * il.alpha[nm] + k * il.beta[nm]) for nm in M.TARGET_NAMES}
    gn = lambda nm, p: M.gauss_norm(ma[nm], il.sdQ[nm].hi, p)
    lam = lambda p: M.gauss_norm(mmax, s_hi, p)
    T, tau, om, v, nu = (lambda p, x=x: gn(x, p) for x in ('T', 'tau', 'om', 'v', 'nu'))
    kap = lambda p: 6 * k1 * tau(p) + T(2 * p) ** 2 + R * T(2 * p) * tau(2 * p)
    # first order: r E[lambda_+ om] = r [mu_om F_1 - bw_om (F - m F_1)], |mu_om| <= c + s r, |bw_om| <= |Cu_om,w| / Cu_ww
    sa_, ca_ = law.alpha['om'].absval(R)
    sb_, cb_ = law.beta['om'].absval(R)
    sc_, cc_ = law.Cu[('om', 'w')].absval(R)
    cwlo = (2 - Sm) / (1 + th1)                                    # Var w = Cu_ww / Theta >= cwlo
    # the regression coefficient Cu_om,w / Cu_ww is free of Theta (it cancels exactly); dividing |Cu_om,w| by the
    # normalized floor cwlo is deliberately conservative (review C58)
    # relative to 36 k^2 r^2 F_0: the 36 k^2 cancels, so the normalizer is F_0 >= Fmin
    T2 = (((b1 * sa_ + k1 * sb_) * F1max + sc_ / cwlo * (Fmax + mmax * F1max)) / Fmin,
          ((b1 * ca_ + k1 * cb_) * F1max + cc_ / cwlo * (Fmax + mmax * F1max)) / Fmin)
    if MUT == 'no-om-term':
        T2 = (Fr(0), Fr(0))
    # second order (explicit r^2), as in Math-#215
    mt = M.IV(6 * k0, 6 * k1) * (b * il.alpha['tau'] + k * il.beta['tau']) * M.IV(Fmin, Fmax)
    side = 6 * k1 * M.absup(il.bw['tau']) * s_hi * lam(4) ** 2 + R * T(4) * tau(4) * lam(4) ** 2
    T3_up = max(Fr(0), mt.hi + side) / norm
    T3_dn = max(Fr(0), -mt.lo + side + T(4) ** 2 * lam(4) ** 2) / norm
    T4 = R * kap(4) * lam(4) * om(2)
    xi2 = 6 * k1 * (R * nu(4) ** 2 + 2 * nu(4) * v(4)) + T(4) * (R * R * nu(8) ** 2 + 2 * R * nu(8) * v(8) + 2 * v(8) ** 2) \
        + R * tau(4) * v(8) ** 2
    T5 = lam(2) * xi2
    T6 = v(8) ** 2 * (6 * k1 + R * T(4) + R * R * tau(4)) * om(4) + v(4) ** 2 * (R * nu(4) + v(4)) ** 2
    Yn = ('v', 'om', 'nu')
    prec = 1 / cwlo + TB.wq_bound(M, il.Cg, Yn, [[M.absup(il.bw[nm])] for nm in Yn])
    pbar = Fr(2, 5) * M.sqrt_up(prec)
    h = lambda p: Fr(2) / (9 * k0) * v(2 * p) ** 2 + om(p)
    bad = R * pbar * h(2) * (Fr(15, 2) * k1 * h(4) + v(8) ** 2) * (9 * k1 * (h(4) + om(4)) + (R * nu(8) + v(8)) ** 2)
    # G_0^c: E[W 1{G_0^c}]/r^2 <= P1n P2n P(G_0^c)^(1/2) <= P1n P2n sqrt(q4) r^2
    q4 = far_set(M, ma['T'], il.sdQ['T'].hi, ma['tau'], il.sdQ['tau'].hi, k0, R)
    P1n = (6 * k1 + R * T(8)) * lam(8) + R * v(8) ** 2
    P2n = (6 * k1 + R * T(8) + R * R * tau(8)) * (lam(8) + R * om(8)) + R * (R * nu(8) + v(8)) ** 2
    g0c = P1n * P2n * M.sqrt_up(q4)
    X = ab_add(T2, ((T4 + T5 + T6 + bad + g0c) / norm, Fr(0)))
    p_up, p_dn = pi_ratio_v(law, Q, R)
    z_up = ab_add(Fae, X, (T3_up, Fr(0)))
    z_dn = ab_add(Fae, X, (T3_dn, Fr(0)))
    return combine_v(M, p_up, p_dn, z_up, z_dn, R)


def bounds_d3_v(Q, R, law, il):
    """(up, dn) in (a, b) form in d = 3 (NOTE sections 3-4)."""
    M = E3
    b0, b1, k0, k1 = Q
    th1 = law.th1
    names = ('a11', 'a22', 'a12')
    for nm, ref in (('a11', -1), ('a22', -1), ('a12', 0)):
        flat(law.alpha[nm], ref, 'alpha_' + nm)
        flat(law.beta[nm], 0, 'beta_' + nm)
    for (x, y), ref in ((('a11', 'a11'), 2), (('a22', 'a22'), 2), (('a12', 'a12'), 1), (('a11', 'a22'), 0),
                        (('a11', 'a12'), 0), (('a22', 'a12'), 0)):
        flat(law.Cu[(x, y)], ref, 'Cov(%s, %s)' % (x, y))
    Fw = (Fr(1), Fr(1), M.SQRT2)
    # Loewner coupling with the contact law over the whole band [0, R] (as in Math-#215): moment bounds and m_0 >= m0lo
    comps = []
    for nm, ref, f in (('a11', -1, 1), ('a22', -1, 1), ('a12', 0, 2)):
        sA, cA = (law.alpha[nm] - ref).absval(R)
        sB, cB = law.beta[nm].absval(R)
        comps.append((b1 * (cA + sA * R) + k1 * (cB + sB * R)) * f)
    eps = M.sqrt_up(sum(x * x for x in comps))
    Cb = []
    for i in range(3):
        row = []
        for j in range(3):
            lo, hi = law.Cu[(names[i], names[j])].enclose(R)
            row.append(M.IV(lo, hi) * Fw[i] * Fw[j] * M.IV(1 / (1 + th1), 1))
        Cb.append(row)
    Lb = M.cholesky(Cb)
    eta = M.sqrt_up(sum(M.absup(Lb[i][j] - (M.SQRT2 if i == j else 0)) ** 2 for i in range(3) for j in range(i + 1)))
    Dl = M.rup_rel(eps + eta * TB.R0C)
    cm = M.contact_moment
    bA, bB = TB.grid_dn(b0 - Dl), TB.grid_up(b1 + Dl)
    m3b0 = cm(2, 0, b0).lo
    L3up = 2 * cm(1, 1, bB).hi / m3b0
    L3dn = 2 * cm(1, 1, b1).hi / cm(2, 0, bA).lo
    pR0 = M.chi_tail(3, TB.R0C)
    muB = M.rup_rel(b1 * M.sqrt_up(Fr(2)) + eps)
    sig = M.sqrt_up(max(x.hi for x in (Cb[0][0], Cb[1][1], Cb[2][2]))
                    + 2 * max(M.absup(Cb[i][j]) for i in range(3) for j in range(3) if i != j))
    U = M.chi_upper_moments(3, TB.R0C, 4)
    out_D2 = sum((U[i] * (M.binom(4, i) * muB ** (4 - i) * sig ** i) for i in range(5)), M.IV(0)).hi / 4
    tail_c = M.sqrt_up(cm(4, 0, b1).hi) * M.sqrt_up(pR0)
    nBF16 = M.rup_rel(muB + sig * M.chi_norm(3, 16))
    out_ball = M.sqrt_up(pR0)

    def up_moment(a, c):
        return M.rup_rel(cm(a, c, bB).hi + 2 ** c * M.rup_rel(nBF16 ** (2 * a + c)) * out_ball)
    ED2, ED4, ED2T2, ET4, DT = up_moment(2, 0), up_moment(4, 0), up_moment(2, 2), up_moment(0, 4), up_moment(1, 1)
    trCb = sum(x.hi for x in (Cb[0][0], Cb[1][1], Cb[2][2]))
    BF = lambda p: M.frob_norm(muB, trCb, p)
    rho_lo = TB.exp_minus(M, Dl * L3dn).lo - tail_c / m3b0               # m3_r / m3(b) over [0, R], r = 0 included
    rho_hi = TB.exp_minus(M, -(Dl * L3up)).hi + out_D2 / m3b0
    require(rho_lo > 0, 'contact moment floor')
    m0lo = m3b0 * rho_lo                                                 # m_0 = E_0[D^2 1{B > 0}] >= m0lo
    rel = 1 / rho_lo                                                     # bounds relative to m3(b) -> relative to m_0
    # main term: gradient coupling B_r = mu_r + C_r^(1/2) Z, B_0 = mu_0 + C_0^(1/2) Z (natural coordinates),
    # |g(B_r) - g(B_0)| <= max(||B_r||, ||B_0||)^3 ||B_r - B_0||, g = det(B)^2 1{B > 0};
    # ||C_r^(1/2) - C_0^(1/2)||_F <= ||C_r - C_0||_F / (2 sqrt(lmB)) (Sylvester equation in the eigenbases)
    Fu = (Fr(1), Fr(1), SQRT2_UP)                                       # rational upper bounds of the weights Fw
    dmuB = ab_norm([ab_mul(mean_inc(law, nm, b1, k1, R), f) for nm, f in zip(names, Fu)])
    dC = ab_norm([ab_mul(law.Cu[(names[i], names[j])].absinc(R), Fu[i] * Fu[j]) for i in range(3) for j in range(3)])
    lmB = TB.gersh_min(Cb)
    require(lmB > 0, 'Gershgorin floor of the transverse covariance')
    dS = ab_mul(dC, 1 / (2 * M.sqrt_down(lmB)))
    K3 = M.sqrt_up(Fr(2)) * BF(8) ** 3 / m0lo
    if MUT == 'coupling-half':
        K3 = K3 / 2
    main = ab_mul(ab_add(dmuB, dS), K3)
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
    # mean of Omega': ||mu_Omega'(r)||_F <= c_mu + s_mu r
    s_mu2 = c_mu2 = Fr(0)
    for nm, mult in zip(M.ONAMES, (1, 1, 2)):
        sa_, ca_ = law.alpha[nm].absval(R)
        sb_, cb_ = law.beta[nm].absval(R)
        s_mu2 += mult * (b1 * sa_ + k1 * sb_) ** 2
        c_mu2 += mult * (b1 * ca_ + k1 * cb_) ** 2
    s_mu, c_mu = M.sqrt_up(s_mu2), M.sqrt_up(c_mu2)
    muO = s_mu * R + c_mu
    # regression of Omega' on B: E[Omega' - mu | B] = beta (B - mu_B) + DY
    G = law.G
    beta_t = G['o11'][0]
    for (o, l) in (('o22', 1), ('o12', 2)):
        flat(G[o][l] - beta_t, 0, 'regression of %s on B' % o)
    for o, ls in (('o11', (1, 2)), ('o22', (0, 2)), ('o12', (0, 1))):
        for l in ls:
            flat(G[o][l], 0, 'off-diagonal regression of %s on B' % o)
    require(abs(beta_t.center(0)) <= TINY, 'regression of Omega on B at r = 0 (reference part)')
    dGs2 = dGc2 = Fr(0)
    for o, mult in zip(('o11', 'o22', 'o12'), (1, 1, 2)):
        for l in range(3):
            t = G[o][l] - beta_t if (o, l) in (('o11', 0), ('o22', 1), ('o12', 2)) else G[o][l]
            s_, c_ = t.absval(R)
            dGs2 += mult * s_ ** 2
            dGc2 += mult * c_ ** 2
    dGs, dGc = M.sqrt_up(dGs2), M.sqrt_up(dGc2)
    b1c = beta_t.center(1)                                               # = 1/2
    require(b1c > 0, 'sign of the first-order regression coefficient of Omega on B')
    # r beta(r) - b1c r^2 = c0 r + (c1 - b1c) r^2 + ...: |.| <= e_beta r + sb_beta r^2
    b0lo, b0hi = beta_t.c0()
    e_beta = max(abs(b0lo), abs(b0hi))
    c1lo, c1hi = beta_t.coeff(1)
    sb_beta = max(abs(c1lo - b1c), abs(c1hi - b1c)) + (max(abs(x) for x in beta_t.coeff(2)) + beta_t.high(R)) * R
    DTlo = cm(1, 1, bA).lo - M.sqrt_up(cm(2, 2, b1).hi) * M.sqrt_up(pR0)
    m3up = cm(2, 0, b1).hi
    tau_lo = b0 * max(DTlo, Fr(0)) / m3up
    tau_hi = b1 * DT / m3b0
    X3lo = 2 * rho_lo - tau_hi - eps * DT / m3b0
    X3hi = 2 * rho_hi - tau_lo + eps * DT / m3b0
    X3m = max(abs(X3lo), abs(X3hi))
    # r |R1|/m3(b) <= r (c_mu + s_mu r) DT/m3 + r (dGc + dGs r) sqrt(E[D^2 tr^2 1]) sqrt(tr Cb)/m3
    R1a = (s_mu * DT + dGs * M.sqrt_up(ED2T2) * M.sqrt_up(trCb)) / m3b0
    R1b = (c_mu * DT + dGc * M.sqrt_up(ED2T2) * M.sqrt_up(trCb)) / m3b0
    U3_up = (max(Fr(0), -b1c * X3lo) + sb_beta * X3m + R1a, e_beta * X3m + R1b)
    U3_dn = (max(Fr(0), b1c * X3hi) + sb_beta * X3m + R1a, e_beta * X3m + R1b)
    if MUT == 'no-om-term':
        U3_up = U3_dn = (Fr(0), Fr(0))

    def cov_Oz(o, z):
        if z in names:
            s_, c_ = law.Cu[(o, z)].absval(R)
            return s_ * R + c_
        return M.absup(il.C[(o, z)])

    def explained(zs):
        # with D the lower diagonal endpoints, C_zz = D^(1/2)(I + H + E)D^(1/2): H >= 0 diagonal (surplus), E zero-diagonal
        # with ||E||_F <= Ef, so C_zz >= (1 - Ef) D; the surplus H only helps (review C58)
        rows = [[cov_Oz(o, z) for z in zs] for o in M.ONAMES]
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
    zA = names + tuple(M.VNAMES) + ('nu1', 'nu2')
    tB, tK = explained(names), explained(zA)
    YB4, YK4 = M.frob_norm(0, tB, 4), M.frob_norm(0, tK, 4)
    detX = M.absup(il.Cg[('o11', 'o22')] - il.Cg[('o12', 'o12')])
    E1 = up_moment(1, 0)
    ED2lo = max(Fr(0), cm(2, 0, bA).lo - tail_c)
    mt = M.IV(6 * k0, 6 * k1) * (b * il.alpha['tau'] + k * il.beta['tau']) * M.IV(ED2lo, ED2)
    side = 6 * k1 * il.bnorm['tau'] * M.sqrt_up(trCb) * M.sqrt_up(ED4) + R * T(4) * tau(4) * M.sqrt_up(ED4)
    U2_up = max(Fr(0), mt.hi + side) / norm36
    U2_dn = max(Fr(0), -mt.lo + side + T(4) ** 2 * M.sqrt_up(ED4)) / norm36
    U3r = R * kap(4) * M.sqrt_up(ED2T2) * Om(4)
    U4rel = (detX * E1 + M.sqrt_up(ED2) * (muO + YB4) ** 2 / 2) / m3b0
    U4 = R * R * kap(4) * M.sqrt_up(ED2) * Om(8) ** 2 / 2
    U5 = M.sqrt_up(ED2T2) * ((2 * T(4) + R * tau(4)) * v(8) ** 2 + 2 * c1(4) * nu(8) * v(8) + R * c1(4) * nu(8) ** 2)
    U67rel = (M.sqrt_up(ED2) * (muO * e(4) ** 2 + e(8) ** 2 * YK4) + M.sqrt_up(ET4) * (muO * v(4) ** 2 + v(8) ** 2 * YK4)) / (6 * k0 * m3b0)
    U6 = R * T(8) * M.sqrt_up(ED2) * Om(8) * e(8) ** 2
    U7 = R * (T(8) + R * tau(8)) * M.sqrt_up(ET4) * Om(8) * v(8) ** 2
    U8 = R * c2(8) * Om(16) ** 2 / 2 * M.iroot(ET4, 4) * v(16) ** 2
    U9 = M.sqrt_up(ET4) * v(8) ** 2 * e(8) ** 2
    U10 = R * M.iroot(ET4, 4) * v(8) ** 2 * Om(4) * e(8) ** 2
    Yn = tuple(M.VNAMES) + tuple(M.ONAMES) + ('nu1', 'nu2')
    rows = []
    for nm in Yn:
        if nm in M.ONAMES:
            cov = []
            for an, f in zip(names, (1, 1, 2)):
                s_, c_ = law.Cu[(nm, an)].absval(R)
                cov.append((s_ * R + c_) * f)
            rows.append([M.sqrt_up(sum(x * x for x in cov)) / lmB])
        else:
            rows.append([M.absup(x) for x in il.bt[nm]])
    Wt = TB.wq_bound(M, il.Cg, Yn, rows)
    c_hi = sig * sig
    cl = 1 / (1 / lmB + Wt)
    KBp = M.rup_rel((M.PI * M.SQRT2 / (2 * M.PI * M.SQRT2PI)).hi / (cl * M.sqrt_down(cl)))
    m1 = muB + c_hi * M.sqrt_up(Wt) * M.chi_norm(7, 8)
    Hs = TB.half_moments(M, c_hi)
    Ja = m1 ** 4 / 4 + sum(M.binom(3, i) * m1 ** (3 - i) * Hs[i] for i in range(4))
    Jb = m1 ** 3 / 3 + sum(M.binom(2, i) * m1 ** (2 - i) * Hs[i] for i in range(3))
    h = lambda p: Fr(2) / (9 * k0) * v(2 * p) ** 2 + Om(p)
    nhg = h(4) * (Fr(15, 2) * k1 * h(8) + v(16) ** 2) * (9 * k1 * (h(8) + Om(8)) + e(16) ** 2)
    nhgO = h(8) * (Fr(15, 2) * k1 * h(16) + v(32) ** 2) * (9 * k1 * (h(16) + Om(16)) + e(32) ** 2) * Om(8)
    bad = R * KBp * (Ja * nhg + R * Jb * nhgO)
    q4 = far_set(M, ma['T'], il.sdQ['T'], ma['tau'], il.sdQ['tau'], k0, R)
    P1n = c1(8) * BF(16) ** 2 + R * BF(8) * v(16) ** 2
    P2n = c2(8) * (BF(16) + R * Om(16)) ** 2 + R * (BF(8) + R * Om(8)) * e(16) ** 2
    g0c = P1n * P2n * M.sqrt_up(q4)
    Xa = (U3r + U4 + U5 + U6 + U7 + U8 + U9 + U10 + bad + g0c) / norm36 + U4rel + U67rel
    # everything above except `main` is relative to m3(b); m3(b)/m_0 <= 1/rho_lo
    z_up = ab_add(main, ab_mul(ab_add(U3_up, (Xa, Fr(0)), (U2_up, Fr(0))), rel))
    z_dn = ab_add(main, ab_mul(ab_add(U3_dn, (Xa, Fr(0)), (U2_dn, Fr(0))), rel))
    p_up, p_dn = pi_ratio_v(law, Q, R)
    return combine_v(M, p_up, p_dn, z_up, z_dn, R)


def rate_sweep_v(d, law):
    """For every R and every sub-box: (a_up, beta_up, a_dn, beta_dn), decimal strings rounded up."""
    M = ENG[d]
    fn = bounds_d2_v if d == 2 else bounds_d3_v
    out = {}
    for R in R_STARS:
        il = M.band_law(Fr(0), R)
        rows = []
        for bb, kb in SUBBOXES:
            up, dn = fn((bb[0], bb[1], kb[0], kb[1]), R, law, il)
            rows.append([dec_up(up[0], 6), dec_up(up[1], 24), dec_up(dn[0], 6), dec_up(dn[1], 24)])
        out[str(R)] = {'boxes': rows,
                       'a_up': max((r[0] for r in rows), key=Fr), 'beta_up': max((r[1] for r in rows), key=Fr),
                       'a_dn': max((r[2] for r in rows), key=Fr), 'beta_dn': max((r[3] for r in rows), key=Fr)}
    return out


# ============================================================================= 4. reference integrals and the corollary
def k_weights(d):
    """int_box A_0^ref/(3k) on every sub-box (the r^1 weight), as decimal upper bounds."""
    M = ENG[d]
    cells = TB.b_cells(d)
    K = TB.K_const(d)
    J11 = {kb: TB.k_integral(M, 1, 1, kb[0], kb[1]) for kb in SUB_K}
    Ibs = {bb: TB.b_integral(M, cells, bb[0], bb[1]) for bb in set(bb for bb, _ in SUBBOXES)}
    return [dec_up((K * Ibs[bb] * J11[kb]).hi, 24) for bb, kb in SUBBOXES]


def assemble_v(d, rate, ref, w1, eps0):
    """Corollary L'1: for 0 < ell < R^3/2,
        ell^(1/3) nu_cand(ell) - c_{B,K}  in  [-(c2_dn ell^(2/3) + c1_dn ell^(1/3)), c2_up ell^(2/3) + c1_up ell^(1/3)],
    c_{B,K} = int_{B x K x S^(d-1)} A_0(b, k, u)/(3 k^(2/3)) db dk dsigma(u) of the same kernel; the weights are
    int_{box x S^(d-1)} A_0/(3k^(4/3)) and int_{box x S^(d-1)} A_0/(3k), bounded by (1 + eps0) times the reference
    weights (eps0 = Math-#215's |A_0/A_0^ref - 1| bound).  The reference weights w_2, w_1 are full angular integrals
    (theorem_b's K_const includes |S^(d-1)|); Theorem L' is uniform in u, and no isotropy is assumed."""
    c_lo = Fr(ref['c_ref'][0])
    w2 = [Fr(x) for x in ref['w_2']]
    w1 = [Fr(x) for x in w1]
    f = 1 + eps0
    out = {}
    for R in R_STARS:
        rr = rate[str(R)]
        c2_up = f * sum(Fr(row[0]) * w for row, w in zip(rr['boxes'], w2))
        c2_dn = f * sum(Fr(row[2]) * w for row, w in zip(rr['boxes'], w2))
        c1_up = f * sum(Fr(row[1]) * w for row, w in zip(rr['boxes'], w1))
        c1_dn = f * sum(Fr(row[3]) * w for row, w in zip(rr['boxes'], w1))
        cl = c_lo * (1 - eps0)
        out[str(R)] = {'c2_up': dec_up(c2_up, 12), 'c2_dn': dec_up(c2_dn, 12),
                       'c1_up': dec_up(c1_up, 30), 'c1_dn': dec_up(c1_dn, 30),
                       'rel2_up': dec_up(c2_up / cl, 6), 'rel2_dn': dec_up(c2_dn / cl, 6),
                       'rel1_up': dec_up(c1_up / cl, 30), 'rel1_dn': dec_up(c1_dn / cl, 30),
                       'ell_max': '%s' % (R ** 3 / 2)}
    return out


def params():
    return {'R_STARS': [str(x) for x in R_STARS], 'TV': {'s': TM_S, 'N': TM_N, 'P': TM_P}, 'E_UP': str(E_UP),
            'MARKOV_P': MARKOV_P, 'R0_COUPLING': str(TB.R0C), 'L_min': 10,
            'SUB_B': [[str(a), str(b)] for a, b in TB.SUB_B], 'SUB_K': [[str(a), str(b)] for a, b in SUB_K],
            'band': {'b': ['0', '1'], 'k': ['1/2', '2']}}


def eps0_215(d):
    """Math-#215 Theorem L at r -> 0: |A_0/A_0^ref - 1| <= max(eps_up, eps_dn) over R (pinned RESULTS.json of #215,
    recomputed here by TB.rate_sweep for R = 1/4096 and compared)."""
    tml = TB.tm_law(d)
    M = ENG[d]
    R = R_STARS[0]
    il = M.band_law(Fr(0), R)
    fn = TB.bounds_d2 if d == 2 else TB.bounds_d3
    e = Fr(0)
    for bb, kb in SUBBOXES:
        up, dn = fn((bb[0], bb[1], kb[0], kb[1]), R, tml, il)
        e = max(e, up[1], dn[1])
    return e


def compute(d):
    law_t = tv_law(d, torus=True)
    law_r = tv_law(d, torus=False)
    rate_t = rate_sweep_v(d, law_t)
    rate_r = rate_sweep_v(d, law_r)
    ref = TB.reference(d)
    w1 = k_weights(d)
    e0 = eps0_215(d)
    return {'tv_law_torus': tv_summary(law_t), 'rate_torus': rate_t, 'rate_reference_kernel': rate_r,
            'reference': {'c_ref': ref['c_ref'], 'w_c': ref['w_c'], 'w_2': ref['w_2'], 'w_1': w1},
            'eps0_215': dec_up(e0, 24),
            'corollary_torus': assemble_v(d, rate_t, ref, w1, Fr(dec_up(e0, 24))),
            'corollary_reference_kernel': assemble_v(d, rate_r, ref, w1, Fr(0))}


def full_run():
    res = {'schema': 1, 'object': OBJECT, 'scientific_effect': 'NONE', 'certified': True, 'mutant': MUT,
           'parameters': params(), 'dims': {}}
    for d in (2, 3):
        res['dims'][str(d)] = compute(d)
    return res


def text(res):
    return json.dumps(res, indent=1, sort_keys=True) + '\n'


def main():
    global MUT
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--mutant', choices=MUTANTS)
    a = ap.parse_args()
    MUT = a.mutant
    res = full_run()
    path = os.path.join(HERE, 'RESULTS.json')
    if a.write:
        require(MUT is None, 'no --write under a mutant')
        with open(path, 'w') as fh:
            fh.write(text(res))
        print('RESULTS.json written')
        return
    with open(path) as fh:
        stored = fh.read()
    if MUT is not None:
        res['mutant'] = None
    require(text(res) == stored, 'replay differs from RESULTS.json')
    print(json.dumps({'object': OBJECT, 'check': 'passed', 'scientific_effect': 'NONE'}))


if __name__ == '__main__':
    main()
