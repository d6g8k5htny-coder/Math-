#!/usr/bin/env python3
"""Exact controls for CL-CANDIDATE-PARITY-RATE-20261001-v1 (Theorem P: the candidate density with remainder l^(3/5)).

Standard library only; exact rationals throughout; deterministic (a fixed linear congruential generator).
Output: RESULTS.json (sorted keys), byte-identical under -O.  Usage:
    python3 -B -S parity_check.py                 # exit 0, prints RESULTS.json
    python3 -B -S parity_check.py --mutant M3     # exit 1 (only its control fails)
    unknown mutant label                          -> exit 2

Controls
  Q1  the exponent ledger of section 5 at rho = l^(1/5): least exponent 3/5, attained by rho^3, l^2 rho^-7, l rho^-2;
      the split is optimal on a grid and is exactly the edge k = r^2 of Lemma U's range; the ledger without Lemma K
      (finite part l rho^-2) also gives 3/5; the closed form of the integral of r min(k, 1/k) (antiderivatives
      evaluated exactly) is (6/5) l^(2/3); 3/5 > 1/2 > 3/7 > 4/11
  Q2  Lemma R and the evenness of Lemma Pi on exactly pinned polynomial fields (d = 1, 2, 3, 4): in the
      birth-integrated (midpoint) coordinates every pinned jet is an even polynomial in r; Pi(r) =
      -det H(-r/2) det H(r/2) / r^2 is even in r; the new row of section 1 has target 0 (a consistency identity);
      point reflection maps the pins at k to the pins at -k and preserves Pi; det K_M and det K_S are affine in k
      (checked at d + 1 values of k, which determine a polynomial of degree <= d)
  Q3  Lemma Pi, (2.2), on the same fields: det K_(M,S) = -/+ 6 k Delta + r U -/+ r^2 V + O(r^3) and
      Pi = 36 k^2 Delta^2 + r^2 (12 k Delta V - U^2) + O(r^4), with U, V of (2.1) built from the general
      Delta_BB = d^2/dt^2 det(A + t B) and A#_B = d/dt adj(A + t B) at t = 0 (so d = 4 tests the m >= 3 terms);
      U is invariant and V changes sign under (k, odd jets) -> (-k, -odd jets)
  Q4  Lemma K (the k-parity of A_2) on an instance: for the reference kernel exp(-|z|^2/2) in d = 1, 2, 3 the
      A-integrand H(k, A) of the birth-integrated r^2 coefficient is h0 + h2 k^2 + h4 k^4 exactly (no odd powers),
      a = 12, and the d = 1, 2 polynomials are those of Math- #232 section 4
  Q5  the pointwise algebra of Lemma U, Step U2, on rational grids (including the Case 3 identity)
  Q6  the inequalities that collect Lemma U's error terms into C(r^2 + r min(k, 1/k)) for k >= r^2: (U.c) on a grid,
      and the identities (U.a), (U.b), (U.d), recorded as consistency checks (they cannot fail)
"""
import json
import sys
from fractions import Fraction as Fr
from itertools import product

MUTANTS = ('M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8')
MUT = None


# ----------------------------------------------------------------------------------------------- deterministic rationals
class LCG:
    def __init__(self, seed):
        self.s = seed % (2 ** 61 - 1)

    def nxt(self):
        self.s = (self.s * 437799614237992725 + 1) % (2 ** 61 - 1)
        return self.s

    def rat(self, num, den):
        return Fr(self.nxt() % (2 * num + 1) - num, 1 + self.nxt() % den)


# ----------------------------------------------------------------------------------------------- polynomials in r
class RP:
    __slots__ = ('c',)

    def __init__(self, c=None):
        c = [Fr(x) for x in (c or [])]
        while c and c[-1] == 0:
            c.pop()
        self.c = c

    def __add__(self, o):
        o = o if isinstance(o, RP) else RP([o])
        n = max(len(self.c), len(o.c))
        return RP([(self.c[i] if i < len(self.c) else 0) + (o.c[i] if i < len(o.c) else 0) for i in range(n)])

    __radd__ = __add__

    def __neg__(self):
        return RP([-x for x in self.c])

    def __sub__(self, o):
        return self + (-(o if isinstance(o, RP) else RP([o])))

    def __mul__(self, o):
        if not isinstance(o, RP):
            return RP([x * o for x in self.c])
        if not self.c or not o.c:
            return RP()
        out = [Fr(0)] * (len(self.c) + len(o.c) - 1)
        for i, a in enumerate(self.c):
            if a:
                for j, b in enumerate(o.c):
                    out[i + j] += a * b
        return RP(out)

    __rmul__ = __mul__

    def co(self, n):
        return self.c[n] if n < len(self.c) else Fr(0)

    def div_r(self, n=1):
        if any(self.co(i) != 0 for i in range(n)):
            raise ArithmeticError('not divisible by r^%d' % n)
        return RP(self.c[n:])

    def even(self):
        return all(self.co(i) == 0 for i in range(1, len(self.c), 2))


def fact(n):
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


def monomials(m, D, tmax=None):
    """exponent tuples (a, b_1..b_m) of total degree <= D; with tmax, transverse degree b_1 + ... + b_m <= tmax
    (second derivatives on the axis y = 0 see only transverse degree <= 2)."""
    out = []
    for tot in range(D + 1):
        for a in range(tot + 1):
            for bs in product(range(tot - a + 1), repeat=m):
                if sum(bs) == tot - a and (tmax is None or sum(bs) <= tmax):
                    out.append((a,) + bs)
    return out


_POW = {}


def xpow(x, n):
    """x^n for an RP x, memoized (x is one of the fixed evaluation points HALF, MHALF, SADDLE_M8)."""
    key = (tuple(x.c), n)
    v = _POW.get(key)
    if v is None:
        v = RP([1]) if n == 0 else xpow(x, n - 1) * x
        _POW[key] = v
    return v


def dat(field, alpha, x):
    """partial^alpha f at (x, 0, ..., 0); x an RP in r."""
    m = len(alpha) - 1
    tot = RP()
    for mono, coef in field.items():
        if mono[0] < alpha[0] or any(mono[j] != alpha[j] for j in range(1, m + 1)):
            continue
        k = fact(mono[0]) // fact(mono[0] - alpha[0])
        for j in range(1, m + 1):
            k *= fact(mono[j])
        tot = tot + coef * k * xpow(x, mono[0] - alpha[0])
    return tot


HALF, MHALF = RP([0, Fr(1, 2)]), RP([0, Fr(-1, 2)])
SADDLE_M8 = RP([0, Fr(1, 2), 0, 0, 1])          # r/2 + r^4: an asymmetric displacement of the saddle (mutant M8)


def pinned(m):
    e = lambda j: tuple(1 if i == j else 0 for i in range(m))
    return [(0,) + (0,) * m, (1,) + (0,) * m, (2,) + (0,) * m, (3,) + (0,) * m] + [(0,) + e(j) for j in range(m)] + [(1,) + e(j) for j in range(m)]


def row(field, m, i):
    """the i-th centred pin row of [R] section 2 (0: midpoint height, 1: (f(+) - f(-))/r, 2: (f_x(+) - f_x(-))/r,
    3: T_r, then the m transverse averages and the m transverse differences), as an RP in r."""
    z = (0,) * m
    f = lambda al, x: dat(field, al, x)
    if i == 0:
        return (f((0,) + z, MHALF) + f((0,) + z, HALF)) * Fr(1, 2)
    if i in (1, 3):
        R2 = (f((0,) + z, HALF) - f((0,) + z, MHALF)).div_r(1)
        return R2 if i == 1 else ((f((1,) + z, MHALF) + f((1,) + z, HALF) - R2 * 2) * 6).div_r(2)
    if i == 2:
        return (f((1,) + z, HALF) - f((1,) + z, MHALF)).div_r(1)
    j = i - 4
    ej = tuple(1 if t == j % m else 0 for t in range(m))
    if j < m:
        return (f((0,) + ej, MHALF) + f((0,) + ej, HALF)) * Fr(1, 2)
    return (f((0,) + ej, HALF) - f((0,) + ej, MHALF)).div_r(1)


def rows(field, m):
    return [row(field, m, i) for i in range(4 + 2 * m)]


def pin_field(free, m, bp, k):
    """Solve the pinned monomials (as polynomials in r) for target (bp, -k r^2, 0, 12 k, 0...) of [R] section 2,
    written in the midpoint height bp; mutant M2 writes the height of M (bp + k r^3/2) in place of the midpoint."""
    pins = pinned(m)
    field = {mo: RP([v]) for mo, v in free.items()}
    for mo in pins:
        field[mo] = RP()
    h0 = RP([bp]) if MUT != 'M2' else RP([bp, 0, 0, k / 2])
    tgt = [h0, RP([0, 0, -k]), RP(), RP([12 * k])] + [RP()] * (2 * m)
    order = [2, 0, 3, 1] + [4 + j for j in range(m)] + [4 + m + j for j in range(m)]
    for _ in range(3):
        for ri in order:
            mo = pins[ri]
            field[mo] = RP()
            rest = row(field, m, ri)
            field[mo] = RP([1])
            unit = row(field, m, ri) - rest
            if len(unit.c) != 1 or unit.c[0] == 0:
                raise ArithmeticError('row %d not unit-triangular' % ri)
            field[mo] = (tgt[ri] - rest) * (1 / unit.c[0])
    chk = rows(field, m)
    if any((chk[i] - tgt[i]).c for i in range(len(chk))):
        raise ArithmeticError('pins not satisfied')
    return field


def rdet(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    s = RP()
    for j in range(n):
        minor = [[M[i][jj] for jj in range(n) if jj != j] for i in range(1, n)]
        t = M[0][j] * rdet(minor)
        s = s + (t if j % 2 == 0 else -t)
    return s


def hess(field, m, x):
    d = m + 1
    H = [[None] * d for _ in range(d)]
    for i in range(d):
        for j in range(d):
            al = [0] * d
            al[i] += 1
            al[j] += 1
            H[i][j] = dat(field, tuple(al), x)
    return H


def Pi_of(field, m):
    KM = rdet(hess(field, m, MHALF)).div_r(1)
    KS = rdet(hess(field, m, HALF if MUT != 'M8' else SADDLE_M8)).div_r(1)
    return -(KM * KS), KM, KS


# ----------------------------------------------------------------------------------------------- matrices over Q
def mdet(M):
    n = len(M)
    if n == 0:
        return Fr(1)
    if n == 1:
        return M[0][0]
    s = Fr(0)
    for j in range(n):
        minor = [[M[i][jj] for jj in range(n) if jj != j] for i in range(1, n)]
        s += (-1) ** j * M[0][j] * mdet(minor)
    return s


def madj(M):
    n = len(M)
    if n == 1:
        return [[Fr(1)]]
    return [[(-1) ** (i + j) * mdet([[M[a][b] for b in range(n) if b != i] for a in range(n) if a != j]) for j in range(n)] for i in range(n)]


def quad(u, M, v):
    return sum((u[i] * M[i][j] * v[j] for i in range(len(u)) for j in range(len(v))), Fr(0))


def jets_of(field, m):
    g = lambda mono: field[mono].co(0) if mono in field else Fr(0)
    e = lambda j: tuple(1 if i == j else 0 for i in range(m))

    def sym(xp, md, mo):
        return [[(md * g((xp,) + tuple(2 if t == i else 0 for t in range(m))) if i == j else
                  mo * g((xp,) + tuple(1 if t in (i, j) else 0 for t in range(m)))) for j in range(m)] for i in range(m)]
    return (sym(0, 2, 1), sym(1, 2, 1), sym(2, 4, 2), [2 * g((2,) + e(j)) for j in range(m)],
            [6 * g((3,) + e(j)) for j in range(m)], 24 * g((4,) + (0,) * m), 120 * g((5,) + (0,) * m))


def det_adj_t(A, B):
    """det(A + tB) and adj(A + tB) as polynomials in t (the RP class, with t in place of r)."""
    m = len(A)
    M = [[RP([A[i][j], B[i][j]]) for j in range(m)] for i in range(m)]
    if m == 1:
        return M[0][0], [[RP([1])]]
    adj = [[rdet([[M[a][b] for b in range(m) if b != i] for a in range(m) if a != j]) * (-1) ** (i + j)
            for j in range(m)] for i in range(m)]
    return rdet(M), adj


def UV(A, B, C, gam, eta, f4, f5, k):
    """U, V of (2.1); Delta_B = D det(A)[B], Delta_BB = D^2 det(A)[B, B], A#_B = D adj(A)[B] in general form."""
    m = len(A)
    if m == 0:
        D, J, DB, DC, DBB, JB = Fr(1), [], Fr(0), Fr(0), Fr(0), []
    else:
        dt, at = det_adj_t(A, B)
        D, DB, DBB = dt.co(0), dt.co(1), 2 * dt.co(2)
        J = [[x.co(0) for x in row] for row in at]
        JB = [[x.co(1) for x in row] for row in at]
        DC = sum((J[i][j] * C[j][i] for i in range(m) for j in range(m)), Fr(0))
    U = f4 / 12 * D - quad(gam, J, gam) / 4 + (3 * k * DB if MUT != 'M3' else 0)
    V = (Fr(3, 4) * k * (DC + DBB) + f4 / 24 * DB + (f5 / 120 * D if MUT != 'M4' else 0) - quad(gam, J, eta) / 12
         - (quad(gam, JB, gam) / 8 if m >= 2 else 0))
    return D, U, V


def control_Q2_Q3():
    q2 = True
    q3 = True
    n = 0
    by_d = {}
    rng = LCG(20261001)
    for m, deg, trials, tmax in ((0, 9, 4, None), (1, 9, 4, None), (2, 8, 2, None), (2, 8, 2, None), (3, 9, 2, 2)):
        pins = set(pinned(m))
        for _ in range(trials):
            free = {mo: rng.rat(9, 5) for mo in monomials(m, deg, tmax) if mo not in pins}
            k = rng.rat(6, 4)
            if k == 0:
                k = Fr(1, 3)
            bp = rng.rat(5, 3)
            fld = pin_field(free, m, bp, k)
            q2 &= all(fld[mo].even() for mo in pinned(m))
            Pi, KM, KS = Pi_of(fld, m)
            q2 &= Pi.even()
            # the new row of section 1: (f_x(-) + f_x(+))/2 = R2 + r^2 R4 / 12 has target -k r^2 + k r^2 = 0
            z = (0,) * m
            avg = (dat(fld, (1,) + z, MHALF) + dat(fld, (1,) + z, HALF)) * Fr(1, 2)
            R = rows(fld, m)
            q2 &= not (avg - (R[1] + RP([0, 0, Fr(1, 12)]) * R[3])).c and not avg.c
            # point reflection f(-z): coefficients times (-1)^{|alpha|}; it satisfies the pins with -k, same Pi
            refl = {mo: c * (-1) ** sum(mo) for mo, c in fld.items()}
            Rr = rows(refl, m)
            tgt = [RP([bp]), RP([0, 0, k]), RP(), RP([-12 * k])] + [RP()] * (2 * m)
            q2 &= all(not (Rr[i] - tgt[i]).c for i in range(len(Rr)))
            Pr, _, _ = Pi_of(refl, m)
            q2 &= not (Pr - Pi).c
            # det K_M and det K_S affine in k: both are polynomials of degree <= d in k (the pinned coefficients are
            # affine in k), so d + 1 values t k, t = 1..d+1, decide; all second differences must vanish
            KK = [Pi_of(pin_field(free, m, bp, t * k), m) for t in range(1, m + 3)]
            for idx in (1, 2):
                vals = [x[idx] for x in KK]
                q2 &= all(not (vals[i] - vals[i + 1] * 2 + vals[i + 2]).c for i in range(len(vals) - 2))
            # Q3: the coefficients of Pi and the parity of U, V
            A, B, C, gam, eta, f4, f5 = jets_of(fld, m)
            D, U, V = UV(A, B, C, gam, eta, f4, f5, k)
            q3 &= Pi.co(0) == 36 * k * k * D * D and KM.co(0) == -6 * k * D and KS.co(0) == 6 * k * D
            q3 &= Pi.co(2) == 12 * k * D * V - U * U
            q3 &= KM.co(1) == U and KS.co(1) == U and KM.co(2) == -V and KS.co(2) == V
            neg = lambda M: [[-x for x in row] for row in M]
            D2, U2, V2 = UV(A, neg(B), C, [-x for x in gam], eta, f4, -f5, -k)
            q3 &= U2 == U and V2 == -V and D2 == D
            n += 1
            by_d[str(m + 1)] = by_d.get(str(m + 1), 0) + 1
    return q2, q3, n, by_d


# ----------------------------------------------------------------------------------------------- Q4: reference kernel
class MP:
    def __init__(self, n, t=None):
        self.n = n
        self.t = {e: Fr(c) for e, c in (t or {}).items() if c != 0}

    @staticmethod
    def var(n, i):
        e = [0] * n
        e[i] = 1
        return MP(n, {tuple(e): 1})

    @staticmethod
    def cst(n, c):
        return MP(n, {(0,) * n: c})

    def __add__(self, o):
        o = o if isinstance(o, MP) else MP.cst(self.n, o)
        out = dict(self.t)
        for e, c in o.t.items():
            out[e] = out.get(e, 0) + c
        return MP(self.n, out)

    __radd__ = __add__

    def __neg__(self):
        return MP(self.n, {e: -c for e, c in self.t.items()})

    def __sub__(self, o):
        return self + (-(o if isinstance(o, MP) else MP.cst(self.n, o)))

    def __mul__(self, o):
        if not isinstance(o, MP):
            return MP(self.n, {e: c * o for e, c in self.t.items()})
        out = {}
        for e1, c1 in self.t.items():
            for e2, c2 in o.t.items():
                e = tuple(a + b for a, b in zip(e1, e2))
                out[e] = out.get(e, 0) + c1 * c2
        return MP(self.n, out)

    __rmul__ = __mul__


def He0(n):
    if n % 2:
        return 0
    v = 1
    for j in range(1, n, 2):
        v *= j
    return (-1) ** (n // 2) * v


def kcov(a, b):
    s = (-1) ** sum(a)
    for x, y in zip(a, b):
        s *= He0(x + y)
    return Fr(s)


def inv(M):
    n = len(M)
    A = [[Fr(x) for x in row] + [Fr(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c] != 0)
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [row[n:] for row in A]


def isserlis(poly, ns, S):
    memo = {}

    def mom(ex):
        if ex in memo:
            return memo[ex]
        idx = [i for i, p in enumerate(ex) for _ in range(p)]
        if len(idx) % 2:
            memo[ex] = Fr(0)
            return Fr(0)

        def pr(lst):
            if not lst:
                return Fr(1)
            tot = Fr(0)
            for j in range(1, len(lst)):
                c = S[lst[0]][lst[j]]
                if c:
                    tot += c * pr(lst[1:j] + lst[j + 1:])
            return tot
        memo[ex] = pr(idx)
        return memo[ex]
    out = {}
    for e, c in poly.t.items():
        v = mom(e[ns:])
        if v:
            out[e[:ns]] = out.get(e[:ns], 0) + c * v
    return MP(ns, out)


def ref_H(d):
    """H(k, A) of the birth-integrated r^2 coefficient for exp(-|z|^2/2), as a polynomial in (k, A_upper)."""
    m = d - 1

    def mi(xo, ys):
        al = [0] * d
        al[0] = xo
        for j in ys:
            al[1 + j] += 1
        return tuple(al)
    G = [mi(1, [])] + [mi(0, [j]) for j in range(m)]
    T3 = mi(3, [])
    Hu = [mi(2, [])] + [mi(1, [j]) for j in range(m)]
    Aidx = [(i, j) for i in range(m) for j in range(i, m)]
    Aj = [mi(0, [i, j]) for (i, j) in Aidx]
    O = G + [T3]
    E0 = Hu + Aj
    C = O + E0
    F = [mi(4, []), mi(5, [])] + [mi(1, [i, j]) for (i, j) in Aidx] + [mi(2, [i, j]) for (i, j) in Aidx] \
        + [mi(2, [j]) for j in range(m)] + [mi(3, [j]) for j in range(m)]
    SCi = inv([[kcov(a, b) for b in C] for a in C])
    SFC = [[kcov(a, b) for b in C] for a in F]
    K = [[sum((SFC[i][t] * SCi[t][j] for t in range(len(C))), Fr(0)) for j in range(len(C))] for i in range(len(F))]
    Sc = [[kcov(F[i], F[j]) - sum((K[i][t] * SFC[j][t] for t in range(len(C))), Fr(0)) for j in range(len(F))] for i in range(len(F))]
    ns = 1 + len(Aidx)
    nv = ns + len(F)
    kv = MP.var(nv, 0)
    Av = [MP.var(nv, 1 + i) for i in range(len(Aidx))]
    t3 = 12 * kv + (1 if MUT == 'M5' else 0)
    cv = [MP.cst(nv, 0)] * len(G) + [t3] + [MP.cst(nv, 0)] * len(Hu) + Av
    jet = []
    for i in range(len(F)):
        mu = MP.cst(nv, 0)
        for t in range(len(C)):
            if K[i][t]:
                mu = mu + cv[t] * K[i][t]
        jet.append(mu + MP.var(nv, ns + i))
    f4, f5 = jet[0], jet[1]
    nA = len(Aidx)
    Bv, Cv = jet[2:2 + nA], jet[2 + nA:2 + 2 * nA]
    gm, et = jet[2 + 2 * nA:2 + 2 * nA + m], jet[2 + 2 * nA + m:]

    def sy(vals):
        M = [[None] * m for _ in range(m)]
        for t, (i, j) in enumerate(Aidx):
            M[i][j] = vals[t]
            M[j][i] = vals[t]
        return M
    Am, Bm, Cm = sy(Av), sy(Bv), sy(Cv)
    one, zero = MP.cst(nv, 1), MP.cst(nv, 0)
    if m == 0:
        D, DB, DC, DBB, J, JB = one, zero, zero, zero, [], []
    elif m == 1:
        D, DB, DC, DBB, J, JB = Am[0][0], Bm[0][0], Cm[0][0], zero, [[one]], [[zero]]
    else:
        D = Am[0][0] * Am[1][1] - Am[0][1] * Am[0][1]
        J = [[Am[1][1], -Am[0][1]], [-Am[0][1], Am[0][0]]]
        DB = Am[1][1] * Bm[0][0] + Am[0][0] * Bm[1][1] - 2 * Am[0][1] * Bm[0][1]
        DC = Am[1][1] * Cm[0][0] + Am[0][0] * Cm[1][1] - 2 * Am[0][1] * Cm[0][1]
        DBB = 2 * (Bm[0][0] * Bm[1][1] - Bm[0][1] * Bm[0][1])
        JB = [[Bm[1][1], -Bm[0][1]], [-Bm[0][1], Bm[0][0]]]

    def qd(u, M, v):
        s = zero
        for i in range(len(u)):
            for j in range(len(v)):
                s = s + u[i] * M[i][j] * v[j]
        return s
    U = f4 * Fr(1, 12) * D - qd(gm, J, gm) * Fr(1, 4) + 3 * kv * DB
    V = Fr(3, 4) * kv * (DC + DBB) + f4 * Fr(1, 24) * DB + f5 * Fr(1, 120) * D - qd(gm, J, et) * Fr(1, 12) - qd(gm, JB, gm) * Fr(1, 8)
    EW2 = isserlis(12 * kv * D * V - U * U, ns, Sc)

    def shift(al):
        return (al[0] + 2,) + al[1:]
    dO = [(shift(a), Fr(1, 8)) for a in G] + [(shift(T3), Fr(1, 40))]
    dE = [(shift(a), Fr(1, 24)) for a in Hu] + [(None, 0) for _ in Aj]

    def S2(base, dl):
        n = len(base)
        return [[(dl[i][1] * kcov(dl[i][0], base[j]) if dl[i][0] else 0) + (dl[j][1] * kcov(base[i], dl[j][0]) if dl[j][0] else 0)
                 for j in range(n)] for i in range(n)]
    Si = inv([[kcov(a, b) for b in O] for a in O])
    Ti = inv([[kcov(a, b) for b in E0] for a in E0])
    S2m, T2m = S2(O, dO), S2(E0, dE)

    def mm(X, Y):
        return [[sum((X[i][t] * Y[t][j] for t in range(len(Y))), Fr(0)) for j in range(len(Y[0]))] for i in range(len(X))]
    SS, TT = mm(Si, S2m), mm(Ti, T2m)
    SSS, TTT = mm(SS, Si), mm(TT, Ti)
    nO = len(O)
    score0 = -sum((SS[i][i] for i in range(nO)), Fr(0)) / 2 - sum((TT[i][i] for i in range(len(E0))), Fr(0)) / 2
    k2 = 72 * SSS[nO - 1][nO - 1]
    kvs = MP.var(ns, 0)
    Avs = [MP.var(ns, 1 + i) for i in range(len(Aidx))]
    xA = [MP.cst(ns, 0)] * len(Hu) + Avs
    sq = MP.cst(ns, 0)
    for i in range(len(E0)):
        for j in range(len(E0)):
            if TTT[i][j]:
                sq = sq + xA[i] * xA[j] * TTT[i][j]
    score = MP.cst(ns, score0) + kvs * kvs * k2 + sq * Fr(1, 2)
    Ds = MP.cst(ns, 1) if m == 0 else (Avs[0] if m == 1 else Avs[0] * Avs[2] - Avs[1] * Avs[1])
    return EW2 + 36 * kvs * kvs * Ds * Ds * score, 72 * Si[nO - 1][nO - 1]


def control_Q4():
    ok = True
    polys = {}
    for d in (1, 2, 3):
        H, a = ref_H(d)
        powers = sorted({e[0] for e in H.t})
        ok &= set(powers) <= {0, 2, 4} and a == 12
        polys[d] = {str(p): sorted([[list(e[1:]), str(c)] for e, c in H.t.items() if e[0] == p]) for p in (0, 2, 4)}
    # the d = 1 and d = 2 polynomials (Math- #232 (4.1) and the planar recovery; derived here independently)
    ok &= polys[1] == {'0': [[[], '-5/24']], '2': [[[], '9/2']], '4': [[[], '108']]}
    ok &= polys[2]['0'] == sorted([[[0], '-3/4'], [[2], '-13/96'], [[4], '-1/256']])
    ok &= polys[2]['2'] == sorted([[[0], '-18'], [[2], '57/8'], [[4], '-9/64']])
    ok &= polys[2]['4'] == [[[2], '108']]
    return ok, {'d1': polys[1], 'd2': polys[2]}


# ----------------------------------------------------------------------------------------------- Q1, Q5, Q6
def control_Q1():
    s = Fr(1, 5) if MUT != 'M1' else Fr(1, 6)
    terms = {'rho^3 (Lemma U, r^2 part; J2)': 3 * s, 'l^(2/3) (Lemma U, r min(k,1/k) part)': Fr(2, 3),
             'l^2 rho^-5 (A_2 finite part)': 2 - 5 * s, 'l^2 rho^-7 (cusp tail; J3; J4)': 2 - 7 * s,
             'l rho^-2 (J3)': 1 - 2 * s, 'l (J5)': Fr(1)}
    least = min(terms.values())
    attained = sorted(t for t, e in terms.items() if e == least)

    def worst(sig):
        return min(3 * sig, Fr(2, 3), 2 - 5 * sig, 2 - 7 * sig, 1 - 2 * sig, Fr(1))
    grid = [Fr(i, 1200) for i in range(150, 301)]
    best = max(grid, key=worst)
    ok = least == Fr(3, 5) and best == Fr(1, 5) and worst(Fr(1, 5)) == Fr(3, 5)
    # Lemma U is applied for r <= rho with k = l / r^3 >= r^2, i.e. r <= l^(1/5): the split is the boundary
    ok &= s >= Fr(1, 5)
    # without Lemma K (only the C^1 bound A_2(k) - A_2(0) = O(k)) the finite part is l rho^-2: still 3/5
    no_k = dict(terms)
    no_k['l^2 rho^-5 (A_2 finite part)'] = 1 - 2 * s
    least_no_k = min(no_k.values())
    ok &= least_no_k == Fr(3, 5)
    # closed form of int_0^inf r min(k, 1/k) dr, k = l/r^3, l = q^3 (crossover r = q):
    # antiderivatives r^5/(5 q^3) on [0, q] and -q^3/r on [q, inf), evaluated exactly
    for q in (Fr(1, 10), Fr(7, 3), Fr(5)):
        ok &= (q ** 5 / (5 * q ** 3) - 0) + (0 - (-(q ** 3) / q)) == Fr(6, 5) * q ** 2
    ok &= Fr(3, 5) > Fr(1, 2) > Fr(3, 7) > Fr(4, 11)
    return ok, {'split': str(s), 'terms': {t: str(e) for t, e in terms.items()}, 'least': str(least), 'attained_by': attained,
                'optimal_split': str(best), 'least_without_lemma_K': str(least_no_k)}


def control_Q5():
    ok = True
    grid = [Fr(i, 3) for i in range(-7, 8)]
    for y, c in product(grid, grid):
        if c >= 0:
            ok &= y * y - min(y * y, c * c) == max(y * y - c * c, 0)
    for x, e in product(grid, grid):
        lhs = abs(max(x + e, 0) - max(x, 0) - (e if x > 0 else 0))
        ok &= lhs <= (abs(e) if abs(x) <= abs(e) else 0)
    nz = [g for g in grid if g != 0]
    for mM, mS, s in product(nz, nz, (1, -1)):
        typed = s * mM < 0 < s * mS
        anti = s * mM > 0 > s * mS
        lhs = -mM * mS * ((1 if typed else 0) - 1)
        rhs = max(mM * mS, 0) - (abs(mM * mS) if (anti and MUT != 'M6') else 0)
        ok &= lhs == rhs
    # Case 3 on {A < 0}: with P := r^-2 Pi and eps := -P - X, P (1_typed - 1) - X_+ = P 1_typed - (-X)_+ + eps
    for P, X, t in product(grid, grid, (0, 1)):
        eps = -P - X
        ok &= P * (t - 1) - max(X, 0) == P * t - max(-X, 0) + eps
    return ok


def control_Q6():
    ok = True
    rs = [Fr(1, 2 ** i) for i in range(1, 9)] + [Fr(3, 5), Fr(1)]
    ks = [Fr(1, 10 ** 4), Fr(1, 300), Fr(1, 17), Fr(1, 3), Fr(1), Fr(5, 2), Fr(9), Fr(40)]
    for r, k in product(rs, ks):
        if k < r * r:
            continue
        kap = k / r
        mk = min(k, 1 / k)
        ok &= k * k / (1 + kap) ** 2 <= r * r                                      # (U.a): identity, k/(1 + kap) = kr/(k + r) <= r
        ok &= r ** 3 / kap <= r * r                                                # (U.b): identity, equivalent to k >= r^2
        lhs = (r * r + min(Fr(1), k * k)) / (1 + kap)
        ok &= lhs <= 2 * (r * r + r * mk)                                          # (U.c)
        if MUT == 'M7':
            ok &= k * k / (1 + kap) <= r * r
        if k <= 1:
            ok &= k * r <= r * mk                                                  # (U.d): identity, kr = r min(k, 1/k)
    return ok


def main(argv):
    global MUT
    if len(argv) == 2 and argv[0] == '--mutant':
        if argv[1] not in MUTANTS:
            print('unknown mutant label', file=sys.stderr)
            return 2
        MUT = argv[1]
    elif argv:
        print('usage: parity_check.py [--mutant M1..M8]', file=sys.stderr)
        return 2
    q1, ledger = control_Q1()
    q2, q3, nfields, by_d = control_Q2_Q3()
    q4, polys = control_Q4()
    q5 = control_Q5()
    q6 = control_Q6()
    res = {'object': 'CL-CANDIDATE-PARITY-RATE-20261001-v1', 'scientific_effect': 'NONE',
           'controls': {'Q1_ledger': q1, 'Q2_reflection_evenness': q2, 'Q3_second_coefficient': q3,
                        'Q4_k_parity_reference': q4, 'Q5_layer_algebra': q5, 'Q6_bookkeeping': q6},
           'ledger': ledger, 'pinned_fields_checked': nfields, 'pinned_fields_by_d': by_d,
           'reference_H_polynomials': polys}
    ok = all(res['controls'].values())
    if MUT is None:
        print(json.dumps(res, indent=1, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
