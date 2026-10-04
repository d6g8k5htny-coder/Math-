#!/usr/bin/env python3
"""Exact controls for CL-ELDER-CUSP-PARITY-20261002-v1 (Lemma Q', Proposition CE++, Theorem N, Corollary N').

Standard library only; exact rationals throughout; deterministic (a fixed linear congruential generator).
Output: RESULTS.json (sorted keys), byte-identical under -O.  Usage:
    python3 -B -S ecp_check.py                 # exit 0, prints RESULTS.json
    python3 -B -S ecp_check.py --mutant M3     # exit 1 (only its control fails)
    unknown mutant label                       -> exit 2

Controls
  X1  Lemma Q' and Proposition CE++: the polynomial bounds for eps0, eps1, eps2 (units C1 N r, in Gamma~ with
      M~ = (35/8) Gamma~) and the constant 220; rho <= 4(1 + M~); the slack on |Xi| = R'; |q| >= lambda Gamma~^2 and
      |tr(A^-1 B)| <= m ||B|| / lambda on random negative definite rational matrices (m = 1, 2, 3); the constants of the
      sufficient conditions (2.3); kappa^2 r^(3/2) + kappa^3 r^2 <= 2r for kappa, r <= 1; the exponents of the 5/2-power step
  X2  the model ridge g = 2(X + 1/2)^2 (X - 1) + 3 phi (X^2 - 1/4)^2 (kappa = 1): (M1) and (3.3) as identities; the new
      cases phi > 1 and phi < -1 of Step Q6'; on J+- = {|phi -+ 1/3| <= 1/96} the constants c3 = 281/128 and c4, the
      bounds on g(-3), g(2), g(-3/2), g(X3) and the brackets, by exact monotonicity; the expansions (3.4) with
      |Psi2|, |Psi2^-| <= 90 and |omega_+-| <= 120 (exact Bernstein positivity on the interval)
  X3  pinned polynomial fields: in d = 2, 3 with k = kappa r, the window field is P + r Q + O(r^2) and every monomial
      r^a X^i Xi^j of F - P - r Q has a >= 2 and |j| <= a + 1; Math- #232's family (2.4) in window coordinates is
      P + r Q + (r^2/4) X^2 Xi^T C Xi; Lemma Omega (a) in d = 2, 3, 4 at fixed k: the coefficients of r^0..r^3 of
      det K_M, det K_S and -det K_M det K_S (odd coefficients of the product vanish)
  X4  Lemma Omega (b)-(c): Delta J_B = Delta_B J - J B J (m = 1, 2, 3, including singular A); (4.2); P1 = Delta^2 Q1;
      V_o = Delta Q1 + alpha4 Delta_B; Q(X, Xi*) = Q1 X (X^2 - 1/4)^2; the parities of Q1, P1, w0, q, z, Y'
  X5  the first-order bookkeeping: w0(+-24 kappa) = 32 kappa^2 Delta^2; 12 k P1 = (kappa Delta^2/3) 36 r Q1; the edge
      shift 36 r Q1 in z from r Q1/(2 kappa) in phi; the edge equations 12 kappa t -+ 6 r Q1 = 0; I'(0) = Psi/36 on
      polynomial test densities (exact antiderivatives); the candidate kink window half-width 24 r |Q1|
  X6  Corollary N' and the ledgers: the substitution r = l^(1/4) s; int_{r-}^{r+} r^2 dr <= kappa0^(-3/4) l^(3/4)/3;
      Math- #229's ledger with and without the elder-only rows (least exponent 3/7 at rho_f = l^(2/7) in both); the
      conditional ledger of Remark 1 (fold family balanced at 1/2, intermediate 4/9)
"""
import json
import sys
from fractions import Fraction as Fr
from itertools import product

MUTANTS = ('M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7')
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


# ----------------------------------------------------------------------------------------------- polynomials in one variable
class RP:
    """Polynomial in one variable (r, or t) with rational coefficients, ascending."""
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

    def __rsub__(self, o):
        return RP([o]) - self

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

    def __pow__(self, n):
        out = RP([1])
        for _ in range(n):
            out = out * self
        return out

    def co(self, n):
        return self.c[n] if n < len(self.c) else Fr(0)

    def div_r(self, n=1):
        if any(self.co(i) != 0 for i in range(n)):
            raise ArithmeticError('not divisible by r^%d' % n)
        return RP(self.c[n:])

    def ev(self, x):
        s = Fr(0)
        for a in reversed(self.c):
            s = s * x + a
        return s

    def deriv(self):
        return RP([i * self.c[i] for i in range(1, len(self.c))])

    def integ(self):
        return RP([0] + [self.c[i] / (i + 1) for i in range(len(self.c))])

    def compose(self, q):
        out = RP()
        for a in reversed(self.c):
            out = out * q + a
        return out

    def even(self):
        return all(self.co(i) == 0 for i in range(1, len(self.c), 2))


T = RP([0, 1])


def binom(n, k):
    out = 1
    for i in range(k):
        out = out * (n - i) // (i + 1)
    return out


def bernstein_positive(p, a, b, depth=14):
    """True if p > 0 on [a, b] is certified by positive Bernstein coefficients (with bisection)."""
    q = p.compose(RP([a, b - a]))
    n = max(len(q.c) - 1, 0)
    coeffs = [sum((Fr(binom(j, i), binom(n, i)) * q.co(i) for i in range(j + 1)), Fr(0)) for j in range(n + 1)]
    if all(x > 0 for x in coeffs):
        return True
    if coeffs[0] <= 0 or coeffs[-1] <= 0 or depth == 0:
        return False
    m = (a + b) / 2
    return bernstein_positive(p, a, m, depth - 1) and bernstein_positive(p, m, b, depth - 1)


def fact(n):
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


def monomials(m, D, tmax=None):
    out = []
    for tot in range(D + 1):
        for a in range(tot + 1):
            for bs in product(range(tot - a + 1), repeat=m):
                if sum(bs) == tot - a and (tmax is None or sum(bs) <= tmax):
                    out.append((a,) + bs)
    return out


_POW = {}


def xpow(x, n):
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
SADDLE_M6 = RP([0, Fr(1, 2), 0, 0, 1])          # r/2 + r^4: an asymmetric displacement of the saddle (mutant M6)


def pinned(m):
    e = lambda j: tuple(1 if i == j else 0 for i in range(m))
    return [(0,) + (0,) * m, (1,) + (0,) * m, (2,) + (0,) * m, (3,) + (0,) * m] + [(0,) + e(j) for j in range(m)] + [(1,) + e(j) for j in range(m)]


def row(field, m, i):
    """[R] section 2's centred pin rows (0: midpoint height, 1: (f(+) - f(-))/r, 2: (f_x(+) - f_x(-))/r, 3: T_r,
    then the m transverse averages and the m transverse differences), as RPs in r."""
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


def pin_field(free, m, tgt):
    """Solve the pinned monomials (as RPs in r) for the target RPs tgt of the 4 + 2m rows."""
    pins = pinned(m)
    field = {mo: RP([v]) for mo, v in free.items()}
    for mo in pins:
        field[mo] = RP()
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
    chk = [row(field, m, i) for i in range(4 + 2 * m)]
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


def dets_of(field, m):
    KM = rdet(hess(field, m, MHALF)).div_r(1)
    KS = rdet(hess(field, m, HALF if MUT != 'M6' else SADDLE_M6)).div_r(1)
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


def mmul(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), Fr(0)) for j in range(len(B[0]))] for i in range(len(A))]


def mvec(A, v):
    return [sum((A[i][k] * v[k] for k in range(len(v))), Fr(0)) for i in range(len(A))]


def dot(u, v):
    return sum((a * b for a, b in zip(u, v)), Fr(0))


def quad(u, M, v):
    return dot(u, mvec(M, v))


def minv(M):
    D = mdet(M)
    return [[x / D for x in row_] for row_ in madj(M)]


def jets_of(field, m):
    g = lambda mono: field[mono].co(0) if mono in field else Fr(0)
    e = lambda j: tuple(1 if i == j else 0 for i in range(m))

    def sym(xp, md, mo):
        return [[(md * g((xp,) + tuple(2 if t == i else 0 for t in range(m))) if i == j else
                  mo * g((xp,) + tuple(1 if t in (i, j) else 0 for t in range(m)))) for j in range(m)] for i in range(m)]
    return (sym(0, 2, 1), sym(1, 2, 1), sym(2, 4, 2), [2 * g((2,) + e(j)) for j in range(m)],
            [6 * g((3,) + e(j)) for j in range(m)], 24 * g((4,) + (0,) * m), 120 * g((5,) + (0,) * m))


def det_adj_t(A, B):
    """det(A + tB) and adj(A + tB) as RPs in t."""
    m = len(A)
    M = [[RP([A[i][j], B[i][j]]) for j in range(m)] for i in range(m)]
    if m == 1:
        return M[0][0], [[RP([1])]]
    adj = [[rdet([[M[a][b] for b in range(m) if b != i] for a in range(m) if a != j]) * (-1) ** (i + j)
            for j in range(m)] for i in range(m)]
    return rdet(M), adj


def UVparts(A, B, C, gam, eta, f4, f5, k):
    """Delta, Delta_B, Delta_C, Delta_BB, J, J_B, Y', U, V of Lemma Omega (#232 (2.2))."""
    dt, at = det_adj_t(A, B)
    D, DB, DBB = dt.co(0), dt.co(1), 2 * dt.co(2)
    J = [[x.co(0) for x in row_] for row_ in at]
    JB = [[x.co(1) for x in row_] for row_ in at]
    m = len(A)
    DC = sum((J[i][j] * C[j][i] for i in range(m) for j in range(m)), Fr(0))
    Yp = f4 / 12 * D - quad(gam, J, gam) / 4
    U = Yp + 3 * k * DB
    V = (Fr(3, 4) * k * (DC + DBB) + f4 / 24 * DB + f5 / 120 * D - quad(gam, J, eta) / 12 - quad(gam, JB, gam) / 8)
    return D, DB, DC, DBB, J, JB, Yp, U, V


# ----------------------------------------------------------------------------------------------- X1
def control_X1():
    ok = True
    G = RP([0, 1])                                              # Gamma~
    Mt = G * Fr(35, 8)                                          # M~
    one = RP([1])
    gbar = one + Mt                                             # gbar / (C1 N r)
    eps0 = (one + Mt) * (one + Mt) * 4
    eps1 = (one + Mt) * (one + Mt) * 4 + G * gbar * 6
    beta = gbar * 2
    eps2 = (gbar * 2 + G * gbar * 2) + beta * G * 12 + beta * (one + Mt) * 2 + G * G * 18
    const = 220 if MUT != 'M5' else 200
    bound = (one + G) * (one + G) * const
    ok &= eps0.c == [4, 35, Fr(1225, 16)] and eps1.c == [4, 41, Fr(1645, 16)] and eps2.c == [6, Fr(279, 4), Fr(3333, 16)]
    ok &= all(bound.co(i) >= e.co(i) for e in (eps0, eps1, eps2) for i in range(3))
    # rho = max(1, 8 gbar/lambda) <= 4(1 + M~) when lambda >= 2 C1 N r; ball radius M~ + rho <= 5 M~ + 4; slack on |Xi| = R'
    ok &= 8 * Fr(1, 2) == 4                                      # 8 C1 N r (1 + M~) / (2 C1 N r) = 4 (1 + M~)
    for g in (Fr(0), Fr(1, 3), Fr(5), Fr(40)):
        m_ = Fr(35, 8) * g
        ok &= m_ + 4 * (1 + m_) == 5 * m_ + 4 and (5 * m_ + 4) - (2 * m_ + 1) >= 0 and 5 * m_ + 4 <= 5 * (1 + m_)
    # |q| >= lambda0 |A^-1 gamma|^2 and tr(A^-1 B)^2 lambda0^2 <= m^2 ||B||_F^2 for A = -(lambda0 I + M^T M)
    rng = LCG(20261002)
    for m in (1, 2, 3):
        for _ in range(6):
            lam0 = Fr(1 + rng.nxt() % 5, 1 + rng.nxt() % 4)
            Mm = [[rng.rat(5, 3) for _ in range(m)] for _ in range(m)]
            MtM = mmul([list(x) for x in zip(*Mm)], Mm)
            A = [[-(lam0 if i == j else 0) - MtM[i][j] for j in range(m)] for i in range(m)]
            B0 = [[rng.rat(5, 3) for _ in range(m)] for _ in range(m)]
            B = [[(B0[i][j] + B0[j][i]) / 2 for j in range(m)] for i in range(m)]
            gam = [rng.rat(6, 4) for _ in range(m)]
            Ai = minv(A)
            v = mvec(Ai, gam)
            q = dot(gam, v)
            ok &= -q >= lam0 * dot(v, v)
            tr = sum((mmul(Ai, B)[i][i] for i in range(m)), Fr(0))
            ok &= tr * tr * lam0 * lam0 <= m * m * sum((B[i][j] ** 2 for i in range(m) for j in range(m)), Fr(0))
    # constants of the sufficient conditions (2.3) and of (Q'3) in section 2
    ok &= 3 * 6 == 18 and 4 * 12 == 48 and 5 * Fr(35, 8) * 12 == Fr(525, 2)
    ok &= (18 ** 2) * 2 == 648                                   # (18^(2/3) 2^(1/3))^3 = 18^2 * 2 = (18 sqrt 2)^2
    ok &= 10 * Fr(35, 8) * 16 == 700 and 6 * 16 == 96 and 5 * Fr(35, 8) * 2 == Fr(175, 4)
    ok &= 220 * 2 * 8 == 3520 and Fr(7040, 3) <= 2347 and 12 * 7040 == 84480
    # kappa^2 r^(3/2) + kappa^3 r^2 <= 2 r for kappa, r <= 1 (r = s^2)
    for kap, s in product([Fr(i, 7) for i in range(0, 8)], [Fr(i, 9) for i in range(1, 10)]):
        r = s * s
        ok &= kap ** 2 * r * s + kap ** 3 * r * r <= 2 * r
    # the 5/2-power step: kappa^2 lambda^2 (t1 f4/(kappa lambda))^(5/2) = kappa^(-1/2) t1^(5/2) f4^(5/2) lambda^(-1/2)
    ok &= Fr(2) - Fr(5, 2) == Fr(-1, 2) and Fr(-1, 2) * Fr(3, 2) == Fr(-3, 4)
    return ok, {'eps0': [str(x) for x in eps0.c], 'eps1': [str(x) for x in eps1.c], 'eps2': [str(x) for x in eps2.c],
                'constant': const}


# ----------------------------------------------------------------------------------------------- X2
def g_model(phi, X):
    return 2 * (X + Fr(1, 2)) ** 2 * (X - 1) + 3 * phi * (X * X - Fr(1, 4)) ** 2


def control_X2():
    ok = True
    grid = [Fr(i, 7) for i in range(-25, 18)]
    phis = [Fr(i, 5) for i in range(-9, 10) if i != 0]
    for phi, X in product(phis, grid):
        g = g_model(phi, X)
        ok &= g + 1 == (X - Fr(1, 2)) ** 2 * (2 * (X + 1) + 3 * phi * (X + Fr(1, 2)) ** 2)
        ok &= g == (X + Fr(1, 2)) ** 2 * (2 * (X - 1) + 3 * phi * (X - Fr(1, 2)) ** 2)
    for phi in phis + [Fr(31, 96), Fr(33, 96), Fr(-31, 96), Fr(-33, 96)]:
        X3 = -1 / (2 * phi)
        ok &= g_model(phi, X3) + 1 == (phi + 1) ** 3 * (3 * phi - 1) / (16 * phi ** 3)
        ok &= g_model(phi, X3) == (phi - 1) ** 3 * (3 * phi + 1) / (16 * phi ** 3)
        ok &= 1 + 2 * phi * X3 == 0
    # derivative g' = 6 (X^2 - 1/4)(1 + 2 phi X) (as a polynomial identity in X at rational phi)
    for phi in phis:
        gp = (RP([Fr(1, 2), 1]) ** 2 * RP([-1, 1]) * 2 + RP([Fr(-1, 4), 0, 1]) ** 2 * (3 * phi)).deriv()
        ok &= not (gp - RP([Fr(-1, 4), 0, 1]) * RP([1, 2 * phi]) * 6).c
    # new cases of Step Q6'. phi > 1: on [-3, -1/2], X^2 - 1/4 >= 0 and 1 + 2 phi X <= 1 - phi < 0 (corners suffice:
    # 1 + 2 phi X is bilinear); g(-3) = -50 + (3675/16) phi > 179 at phi = 1 and increasing.
    for phi, X in product((Fr(1), Fr(5), Fr(10 ** 6)), (Fr(-3), Fr(-1, 2))):
        ok &= 1 + 2 * phi * X <= 1 - phi
    ok &= g_model(Fr(1), Fr(-3)) == -50 + Fr(3675, 16) and -50 + Fr(3675, 16) > 179
    # phi < -1: bracket 2(X + 1) + 3 phi (X + 1/2)^2 <= -(3X^2 + X - 5/4) <= 0 on [1/2, 2]
    brk = RP([Fr(-5, 4), 1, 3])
    ok &= brk.ev(Fr(1, 2)) == 0 and all(brk.deriv().ev(X) > 0 for X in (Fr(1, 2), Fr(2)))   # derivative 6X + 1, linear
    ok &= -5 + 12 * Fr(-1) == -17 and Fr(25, 2) + Fr(675, 16) * Fr(-1) < Fr(-29)
    # J+ = [31/96, 33/96]: c3, X3, g', c4, g(-3), the bracket beta <= -1/2 on [X3, 1/2], g(-5/4) <= -9/32
    Jp = (Fr(31, 96), Fr(33, 96))
    Jm = (Fr(-33, 96), Fr(-31, 96))
    c3 = Fr(281, 128)
    for phi, X in product(Jp, (Fr(-3), Fr(-5, 4))):
        ok &= 12 * phi * X + 2 < 0                               # g''/6 decreasing in X (bilinear: corners)
    ok &= 6 * Fr(-5, 4) ** 2 - Fr(1, 2) > 0                       # g''/6 increasing in phi for |X| >= 5/4
    v = 6 * Jp[0] * Fr(25, 16) + 2 * Fr(-5, 4) - Jp[0] / 2
    ok &= v == Fr(281, 768) and 6 * v == c3
    ok &= -1 / (2 * Jp[0]) == Fr(-48, 31) and -1 / (2 * Jp[1]) == Fr(-16, 11) and Fr(-3) < Fr(-48, 31) and Fr(-16, 11) < Fr(-5, 4)
    c4 = c3 / 2 * (Fr(16, 11) - Fr(5, 4)) ** 2
    ok &= Fr(16, 11) - Fr(5, 4) == Fr(9, 44) and c4 == c3 / 2 * Fr(81, 1936) and Fr(1, 200) < c4 / 2
    ok &= -50 + Fr(3675, 16) * Jp[0] >= 24
    for phi in Jp:
        X3 = -1 / (2 * phi)
        beta = 2 * (X3 - 1) + 3 * phi * (X3 - Fr(1, 2)) ** 2
        ok &= beta == (3 * phi + 1) * (phi - 1) / (4 * phi) and beta <= Fr(-1, 2) and 3 * phi * phi <= 1
    ok &= 2 * (Fr(1, 2) - 1) + 0 == -1                            # beta(1/2) = -1; beta convex in X (beta'' = 6 phi > 0)
    ok &= -Fr(1, 2) * (Fr(-5, 4) + Fr(1, 2)) ** 2 == Fr(-9, 32)
    ok &= Fr(25, 2) + Fr(675, 16) * Fr(-1, 4) >= Fr(125, 64)       # g(2) >= 125/64 for phi >= -1/4 (#220 (M5))
    # J- = [-33/96, -31/96]: mirror statements
    for phi, X in product(Jm, (Fr(5, 4), Fr(2))):
        ok &= 12 * phi * X + 2 < 0
    vm = 6 * Jm[1] * Fr(25, 16) + 2 * Fr(5, 4) - Jm[1] / 2
    ok &= vm == Fr(-281, 768)
    ok &= -1 / (2 * Jm[1]) == Fr(48, 31) and -1 / (2 * Jm[0]) == Fr(16, 11) and Fr(5, 4) < Fr(16, 11) and Fr(48, 31) < 2
    ok &= Fr(25, 2) + Fr(675, 16) * Jm[1] <= Fr(-112, 100)
    ok &= -5 + 12 * Jm[1] <= -7
    for phi in Jm:
        X3 = -1 / (2 * phi)
        bp = 2 * (X3 + 1) + 3 * phi * (X3 + Fr(1, 2)) ** 2
        ok &= bp == (3 * phi - 1) * (phi + 1) / (4 * phi) and bp >= Fr(1, 2) and 3 * phi * phi <= 1
        ok &= abs(g_model(phi, X3)) <= Fr(1, 7)
    # (3.4): Psi(1/3 + t) = 12 t + Psi2 t^2, Psi_-(-1/3 + t) = 12 t + Psi2^- t^2, X3 (X3^2 - 1/4)^2 = -+6 + omega t
    lo, hi = Fr(-1, 96), Fr(1, 96)
    cpsi = 90
    comg = 120 if MUT != 'M4' else 100
    fits = {}
    for sgn in (1, -1):
        a = RP([sgn * Fr(4, 3), 1])                              # phi + 1 = +-4/3 + t ... (for sgn = -1: phi - 1 = -4/3 + t)
        d = RP([sgn * Fr(1, 3), 1])                              # phi = +-1/3 + t
        M_ = a ** 3 * 3 - d ** 3 * 192                          # Psi - 12 t = t M_ / (16 d^3)
        M1 = M_.div_r(1)
        den = d ** 3 * 16
        s_ = 1 if sgn == 1 else -1                               # sign of den on the interval
        ok &= bernstein_positive(den * (s_ * cpsi) - M1, lo, hi) and bernstein_positive(den * (s_ * cpsi) + M1, lo, hi)
        # check the identity at sample points: Psi(+-1/3 + t) = 12 t + t^2 M1/den
        for t in (Fr(1, 200), Fr(-1, 150)):
            phi = sgn * Fr(1, 3) + t
            Psi = ((phi + 1) ** 3 * (3 * phi - 1) / (16 * phi ** 3)) if sgn == 1 else ((phi - 1) ** 3 * (3 * phi + 1) / (16 * phi ** 3))
            ok &= Psi == 12 * t + t * t * M1.ev(t) / den.ev(t)
        fits['Psi2_at_0' if sgn == 1 else 'Psi2m_at_0'] = str(M1.ev(Fr(0)) / den.ev(Fr(0)))
        # omega: X3 = -1/(2 phi) = -+3/(2 +- 6 t) ... computed as X3 = -sgn*3/(2 + sgn*6t)
        base = RP([2, sgn * 6])                                 # 2 + 6t (sgn = 1) or 2 - 6t (sgn = -1)
        inner = RP([8, -sgn * 6, -9])                            # 8 -+ 6t - 9t^2
        Nw = base ** 5 * 6 - inner ** 2 * 3                      # (sgn = 1): t omega (2 + 6t)^5 = 6 base^5 - 3 inner^2
        if sgn == -1:
            Nw = -Nw                                             # (sgn = -1): t omega (2 - 6t)^5 = 3 inner^2 - 6 base^5
        N1 = Nw.div_r(1)
        ok &= bernstein_positive(base ** 5 * comg - N1, lo, hi) and bernstein_positive(base ** 5 * comg + N1, lo, hi)
        for t in (Fr(1, 200), Fr(-1, 150)):
            phi = sgn * Fr(1, 3) + t
            X3 = -1 / (2 * phi)
            ok &= X3 * (X3 * X3 - Fr(1, 4)) ** 2 == -sgn * 6 + t * N1.ev(t) / base.ev(t) ** 5
        fits['omega_at_0' if sgn == 1 else 'omegam_at_0'] = str(N1.ev(Fr(0)) / base.ev(Fr(0)) ** 5)
    ok &= fits['Psi2_at_0'] == '-81' and fits['Psi2m_at_0'] == '81' and fits['omega_at_0'] == '99' and fits['omegam_at_0'] == '99'
    ok &= cpsi * Fr(1, 96) <= 1 and comg * Fr(1, 200) <= 1      # 90 kappa t^2 <= kappa |t|; 120 r |Q1| <= kappa
    return ok, {'c3': str(c3), 'c4': str(c4), 'delta_e': '1/96', 'c_e': '1/200', 'Psi2_bound': cpsi, 'omega_bound': comg,
                'second_order_coefficients': fits}


# ----------------------------------------------------------------------------------------------- X3
def window_terms(field, m):
    """r^-4 (f(rX, r^2 Xi) - f(M)) as {(power of r, i, j-tuple): coefficient}; f(M) = f(-r/2, 0)."""
    out = {}
    for mono, coef in field.items():
        a, bs = mono[0], mono[1:]
        for n, c in enumerate(coef.c):
            if c:
                key = (n + a + 2 * sum(bs) - 4, a, bs)
                out[key] = out.get(key, 0) + c
    fM = dat(field, (0,) * (m + 1), MHALF)
    for n, c in enumerate(fM.c):
        if c:
            key = (n - 4, 0, (0,) * m)
            out[key] = out.get(key, 0) - c
    return {k: v for k, v in out.items() if v != 0}


def model_terms(m, kap, A, B, C, gam, eta, f4, f5, with_C=False, mutQ=False):
    """P + r Q (+ (r^2/4) X^2 Xi^T C Xi) as {(power of r, i, j-tuple): coefficient}."""
    z = (0,) * m
    e = lambda j: tuple(1 if t == j else 0 for t in range(m))
    ee = lambda i, j: tuple((1 if t == i else 0) + (1 if t == j else 0) for t in range(m))
    out = {}

    def add(key, v):
        if v:
            out[key] = out.get(key, 0) + v
    for (i, c) in ((3, 2 * kap), (1, -Fr(3, 2) * kap), (0, -kap / 2)):           # 2 kappa (X + 1/2)^2 (X - 1)
        add((0, i, z), c)
    for (i, c) in ((4, 1), (2, Fr(-1, 2)), (0, Fr(1, 16))):                      # (f4/24)(X^2 - 1/4)^2
        add((0, i, z), f4 / 24 * c)
    for j in range(m):
        add((0, 2, e(j)), gam[j] / 2)
        add((0, 0, e(j)), -gam[j] / 8)
        for jj in range(m):
            add((0, 0, ee(j, jj)), A[j][jj] / 2)
    q5 = f5 / 120 if not mutQ else f5 / 60
    for (i, c) in ((5, 1), (3, Fr(-1, 2)), (1, Fr(1, 16))):                      # (f5/120) X (X^2 - 1/4)^2
        add((1, i, z), q5 * c)
    for j in range(m):
        add((1, 3, e(j)), eta[j] / 6)
        add((1, 1, e(j)), -eta[j] / 24)
        for jj in range(m):
            add((1, 1, ee(j, jj)), B[j][jj] / 2)
            if with_C:
                add((2, 2, ee(j, jj)), C[j][jj] / 4)
    return {k: v for k, v in out.items() if v != 0}


def control_X3():
    ok = True
    nwin = 0
    rng = LCG(20261003)
    # (i) window fields of pinned polynomial fields with k = kappa r (d = 2, 3)
    for m, deg, trials in ((1, 9, 3), (2, 8, 2)):
        pins = set(pinned(m))
        for _ in range(trials):
            free = {mo: rng.rat(9, 5) for mo in monomials(m, deg) if mo not in pins}
            kap = Fr(1 + rng.nxt() % 7, 1 + rng.nxt() % 3)
            bp = rng.rat(5, 3)
            tgt = [RP([bp]), RP([0, 0, 0, -kap]), RP(), RP([0, 12 * kap])] + [RP()] * (2 * m)
            fld = pin_field(free, m, tgt)
            A, B, C, gam, eta, f4, f5 = jets_of(fld, m)
            W = window_terms(fld, m)
            ok &= all(k[0] >= 0 for k in W)
            Mdl = model_terms(m, kap, A, B, C, gam, eta, f4, f5, mutQ=(MUT == 'M1'))
            for k_, v in Mdl.items():
                if W.get(k_, 0) != v:
                    ok = False
            for k_, v in W.items():
                if k_[0] <= 1 and Mdl.get(k_, 0) != v:
                    ok = False
                if k_[0] >= 2:
                    ok &= sum(k_[2]) <= k_[0] + 1
            nwin += 1
    # (ii) Math- #232's family (2.4) in window coordinates (d = 2, 3), and its pins
    for m in (1, 2):
        for _ in range(2):
            kap = Fr(1 + rng.nxt() % 5, 2)
            f4, f5 = rng.rat(7, 3), rng.rat(7, 3)
            gam = [rng.rat(5, 3) for _ in range(m)]
            eta = [rng.rat(5, 3) for _ in range(m)]
            sym = lambda: (lambda M0: [[(M0[i][j] + M0[j][i]) / 2 for j in range(m)] for i in range(m)])([[rng.rat(5, 3) for _ in range(m)] for _ in range(m)])
            A, B, C = sym(), sym(), sym()
            # f(x, y) = 2k(x - r)(x + r/2)^2 + (f4/24)(x^2 - r^2/4)^2 + (f5/120) x (x^2 - r^2/4)^2
            #           + sum_i y_i [(gam_i/2)(x^2 - r^2/4) + (eta_i/6) x (x^2 - r^2/4)] + (1/2) y^T [A + x B + (x^2/2) C] y
            fld = {}
            z = (0,) * m
            e = lambda j: tuple(1 if t == j else 0 for t in range(m))
            ee = lambda i, j: tuple((1 if t == i else 0) + (1 if t == j else 0) for t in range(m))

            def add(mono, rp):
                fld[mono] = fld.get(mono, RP()) + rp
            k = RP([0, kap])                                     # k = kappa r
            # 2k (x - r)(x + r/2)^2 = 2k (x^3 - (3/4) r^2 x - r^3/4)
            add((3,) + z, k * 2)
            add((1,) + z, k * RP([0, 0, Fr(-3, 2)]))
            add((0,) + z, k * RP([0, 0, 0, Fr(-1, 2)]))
            add((4,) + z, RP([f4 / 24]))
            add((2,) + z, RP([0, 0, -f4 / 48]))
            add((0,) + z, RP([0, 0, 0, 0, f4 / 384]))
            add((5,) + z, RP([f5 / 120]))
            add((3,) + z, RP([0, 0, -f5 / 240]))
            add((1,) + z, RP([0, 0, 0, 0, f5 / 1920]))
            for j in range(m):
                add((2,) + e(j), RP([gam[j] / 2]))
                add((0,) + e(j), RP([0, 0, -gam[j] / 8]))
                add((3,) + e(j), RP([eta[j] / 6]))
                add((1,) + e(j), RP([0, 0, -eta[j] / 24]))
                for jj in range(m):
                    mult = Fr(1, 2)
                    add((0,) + ee(j, jj), RP([A[j][jj] * mult]))
                    add((1,) + ee(j, jj), RP([B[j][jj] * mult]))
                    add((2,) + ee(j, jj), RP([C[j][jj] * mult / 2]))
            # pins: f(M) = 0, f(S) = -k r^3, gradients zero at both
            ok &= not dat(fld, (0,) * (m + 1), MHALF).c
            ok &= not (dat(fld, (0,) * (m + 1), HALF) + RP([0, kap]) * RP([0, 0, 0, 1])).c
            for i in range(m + 1):
                al = tuple(1 if t == i else 0 for t in range(m + 1))
                ok &= not dat(fld, al, MHALF).c and not dat(fld, al, HALF).c
            W = window_terms(fld, m)
            Mdl = model_terms(m, kap, A, B, C, gam, eta, f4, f5, with_C=True, mutQ=(MUT == 'M1'))
            ok &= W == Mdl
            nwin += 1
    # (iii) Lemma Omega (a) at fixed k (d = 2, 3, 4)
    nom = 0
    for m, deg, trials, tmax in ((1, 9, 3, None), (2, 8, 2, None), (3, 9, 1, 2)):
        pins = set(pinned(m))
        for _ in range(trials):
            free = {mo: rng.rat(9, 5) for mo in monomials(m, deg, tmax) if mo not in pins}
            k = rng.rat(6, 4)
            if k == 0:
                k = Fr(1, 3)
            bp = rng.rat(5, 3)
            tgt = [RP([bp]), RP([0, 0, -k]), RP(), RP([12 * k])] + [RP()] * (2 * m)
            fld = pin_field(free, m, tgt)
            Pi, KM, KS = dets_of(fld, m)
            A, B, C, gam, eta, f4, f5 = jets_of(fld, m)
            D, DB, DC, DBB, J, JB, Yp, U, V = UVparts(A, B, C, gam, eta, f4, f5, k)
            ok &= KM.co(0) == -6 * k * D and KS.co(0) == 6 * k * D
            ok &= KM.co(1) == U and KS.co(1) == U and KM.co(2) == -V and KS.co(2) == V
            ok &= Pi.co(0) == 36 * k * k * D * D and Pi.co(1) == 0 and Pi.co(2) == 12 * k * D * V - U * U and Pi.co(3) == 0
            ok &= Pi.even()
            nom += 1
    return ok, nwin, nom


# ----------------------------------------------------------------------------------------------- X4
def control_X4():
    ok = True
    rng = LCG(20261004)
    n = 0
    for m in (1, 2, 3):
        for trial in range(8):
            sym = lambda: (lambda M0: [[(M0[i][j] + M0[j][i]) / 2 for j in range(m)] for i in range(m)])([[rng.rat(6, 4) for _ in range(m)] for _ in range(m)])
            A, B, C = sym(), sym(), sym()
            if trial == 0 and m >= 2:                            # a singular A
                A[0] = [Fr(0)] * m
                for i in range(m):
                    A[i][0] = Fr(0)
            gam = [rng.rat(6, 4) for _ in range(m)]
            eta = [rng.rat(6, 4) for _ in range(m)]
            f4, f5, k, kap = rng.rat(9, 4), rng.rat(9, 4), rng.rat(5, 4), rng.rat(5, 2)
            D, DB, DC, DBB, J, JB, Yp, U, V = UVparts(A, B, C, gam, eta, f4, f5, k)
            JBJ = mmul(mmul(J, B), J)
            ok &= all(D * JB[i][j] == DB * J[i][j] - JBJ[i][j] for i in range(m) for j in range(m))
            P1 = D * D / 120 * f5 - D / 12 * quad(gam, J, eta) + quad(gam, JBJ, gam) / 8
            w0 = 36 * kap * kap * D * D - Yp * Yp
            ok &= 36 * kap * kap * D * D + 12 * k * D * V - U * U == w0 + 12 * k * P1 + 9 * k * k * (D * (DC + DBB) - DB * DB)
            Vo = V - Fr(3, 4) * k * (DC + DBB)
            ok &= 12 * D * Vo - 6 * Yp * DB == 12 * P1
            if D != 0:
                Ai = minv(A)
                sgnQ = 1 if MUT != 'M2' else -1
                Q1 = f5 / 120 - sgnQ * quad(eta, Ai, gam) / 12 + quad(gam, mmul(mmul(Ai, B), Ai), gam) / 8
                ok &= P1 == D * D * Q1
                q = quad(gam, Ai, gam)
                alpha4 = (f4 - 3 * q) / 24
                ok &= Vo == D * Q1 + alpha4 * DB and Yp == 2 * D * alpha4
                # Q(X, Xi*) = Q1 X (X^2 - 1/4)^2 with Xi* = -(1/2)(X^2 - 1/4) A^-1 gamma
                for X in (Fr(-3), Fr(-3, 2), Fr(1, 3), Fr(2)):
                    s = X * X - Fr(1, 4)
                    xi = [-s / 2 * x for x in mvec(Ai, gam)]
                    Qv = f5 / 120 * X * s * s + X * s / 6 * dot(eta, xi) + X / 2 * quad(xi, B, xi)
                    ok &= Qv == Q1 * X * s * s
                # parities: (gamma, B, f5) -> -(...), (A, C, eta, f4) fixed
                nB = [[-x for x in row_] for row_ in B]
                D2, DB2, DC2, DBB2, J2, JB2, Yp2, U2, V2 = UVparts(A, nB, C, [-x for x in gam], eta, f4, -f5, k)
                Q1n = -f5 / 120 - sgnQ * quad(eta, Ai, [-x for x in gam]) / 12 + quad([-x for x in gam], mmul(mmul(Ai, nB), Ai), [-x for x in gam]) / 8
                P1n = D2 * D2 / 120 * (-f5) - D2 / 12 * quad([-x for x in gam], J2, eta) + quad([-x for x in gam], mmul(mmul(J2, nB), J2), [-x for x in gam]) / 8
                qn = quad([-x for x in gam], Ai, [-x for x in gam])
                ok &= Q1n == -Q1 and P1n == -P1 and qn == q and Yp2 == Yp and D2 == D
            n += 1
    return ok, n


# ----------------------------------------------------------------------------------------------- X5
def control_X5():
    ok = True
    rng = LCG(20261005)
    shift = 36 if MUT != 'M3' else 18
    for _ in range(6):
        kap, D, r, Q1 = Fr(1 + rng.nxt() % 9, 1 + rng.nxt() % 4), rng.rat(7, 3), Fr(1, 1 + rng.nxt() % 50), rng.rat(9, 4)
        if D == 0:
            D = Fr(2, 3)
        k = kap * r
        w0 = lambda z: D * D / 144 * (5184 * kap * kap - z * z)
        ok &= w0(24 * kap) == 32 * kap * kap * D * D and w0(-24 * kap) == 32 * kap * kap * D * D
        ok &= 12 * k * (D * D * Q1) == kap * D * D / 3 * (36 * r * Q1)
        # edge shift: phi = 1/3 + r Q1/(2 kappa)  <=>  z = 72 kappa phi = 24 kappa + shift r Q1
        ok &= 72 * kap * (Fr(1, 3) + r * Q1 / (2 * kap)) == 24 * kap + shift * r * Q1
        # edge equations 12 kappa t + Psi... linear parts: 12 kappa t - 6 r Q1 = 0 (J+) and 12 kappa t + 6 r Q1 = 0 (J-)
        ok &= 12 * kap * (r * Q1 / (2 * kap)) - 6 * r * Q1 == 0 and 12 * kap * (-r * Q1 / (2 * kap)) + 6 * r * Q1 == 0
        # I'(0) = Psi/36 on a polynomial test density p (exact antiderivatives)
        p = RP([rng.rat(5, 3) for _ in range(5)])
        S = RP([0, 1])                                           # s
        upper = RP([24 * kap, 1])                                # 24 kappa + s
        integrand = (RP([5184 * kap * kap, 0, -1]) * (D * D / 144)) * p   # w0(z) p(z) as a polynomial in z
        F1 = integrand.integ()
        F0 = p.integ()
        I = (F1.compose(upper) - F1.compose(-upper)) + S * (kap * D * D / 3) * (F0.compose(upper) - F0.compose(-upper))
        Ip0 = I.co(1)
        Psi = 1152 * kap * kap * D * D * (p.ev(24 * kap) + p.ev(-24 * kap)) + 12 * kap * D * D * (F0.ev(24 * kap) - F0.ev(-24 * kap))
        ok &= Ip0 == Psi / 36
        # candidate kink: |w0| <= 12 k |P1|  =>  |72 kappa - |z|| <= 24 r |Q1| (since 72 kappa + |z| >= 72 kappa)
        ok &= Fr(1728) / 72 == 24 and 12 * 144 == 1728
    return ok


# ----------------------------------------------------------------------------------------------- X6
def control_X6():
    ok = True
    # substitution r = l^(1/4) s: l/r^4 = s^-4; r- = (l/kappa1)^(1/4) <-> s = kappa1^(-1/4); dr = l^(1/4) ds
    ok &= Fr(1, 4) * 4 == 1
    # int_{r-}^{r+} r^2 dr = (r+^3 - r-^3)/3 <= r+^3/3 = kappa0^(-3/4) l^(3/4)/3 (checked at l = c^4, kappa = d^4)
    for c, d0, d1 in ((Fr(1, 10), Fr(1, 2), Fr(2)), (Fr(1, 3), Fr(1), Fr(3))):
        l = c ** 4
        rp, rm = c / d0, c / d1                                  # (l/kappa0)^(1/4), (l/kappa1)^(1/4)
        ok &= (rp ** 3 - rm ** 3) / 3 <= rp ** 3 / 3 and rp ** 3 == (c ** 3) / d0 ** 3
    # Math- #229's ledger at rho_f = l^(2/7), rho_c = l^(2/9), a = l^(1/9)
    sf = Fr(2, 7) if MUT != 'M7' else Fr(1, 4)
    sc, sa = Fr(2, 9), Fr(1, 9)
    rows_ = {'rho_f^5/l': 5 * sf - 1, 'l rho_f^-2': 1 - 2 * sf, 'l^2 rho_f^-11/2 (elder only)': 2 - Fr(11, 2) * sf,
             'l^3 rho_f^-9 (elder only)': 3 - 9 * sf, 'rho_f^2': 2 * sf, 'rho_c^2': 2 * sc, 'l^2 rho_c^-7': 2 - 7 * sc,
             'a^4 log': 4 * sa, 'l^(2/3) a^-2': Fr(2, 3) - 2 * sa, 'l^3 rho_c^-11 log': 3 - 11 * sc, 'l rho_c^-2': 1 - 2 * sc,
             'rho_c^3': 3 * sc, 'l^(5/3) a^-7': Fr(5, 3) - 7 * sa, 'l': Fr(1)}
    least_with = min(rows_.values())
    without = {k: v for k, v in rows_.items() if 'elder only' not in k}
    least_without = min(without.values())
    ok &= least_with == Fr(3, 7) and least_without == Fr(3, 7)
    ok &= sorted(k for k, v in without.items() if v == least_without) == ['l rho_f^-2', 'rho_f^5/l']
    # the conditional ledger of Remark 1: uniform (r^2 + k^2) on r <= kappa <= 1/r, rho_c = l^(1/5), Lemma K
    tf, tc = Fr(3, 10), Fr(1, 5)
    cond = {'rho_f^5/l': 5 * tf - 1, 'l^2 rho_f^-5': 2 - 5 * tf, 'rho_f^2': 2 * tf, 'rho_c^3': 3 * tc,
            'l^2 rho_c^-7': 2 - 7 * tc, 'l^3 rho_c^-11 log': 3 - 11 * tc, 'l rho_c^-2': 1 - 2 * tc,
            'a^4 log (intermediate)': 4 * sa, 'l^(2/3) a^-2 (intermediate)': Fr(2, 3) - 2 * sa}
    ok &= cond['rho_f^5/l'] == cond['l^2 rho_f^-5'] == Fr(1, 2)
    ok &= min(cond.values()) == Fr(4, 9) and Fr(1) / 5 == tc
    # the fold-family pair alone cannot exceed 1/2: max over sigma of min(5 sigma - 1, 2 - 5 sigma) is 1/2
    grid = [Fr(i, 600) for i in range(120, 241)]
    ok &= max(min(5 * s - 1, 2 - 5 * s) for s in grid) == Fr(1, 2)
    ok &= Fr(3, 5) > Fr(1, 2) > Fr(4, 9) > Fr(3, 7)
    return ok, {'ledger_229': {k: str(v) for k, v in rows_.items()}, 'least_with_elder_rows': str(least_with),
                'least_without_elder_rows': str(least_without),
                'conditional_ledger_remark_1': {k: str(v) for k, v in cond.items()}, 'conditional_least': str(min(cond.values()))}


def main(argv):
    global MUT
    if len(argv) == 2 and argv[0] == '--mutant':
        if argv[1] not in MUTANTS:
            print('unknown mutant label', file=sys.stderr)
            return 2
        MUT = argv[1]
    elif argv:
        print('usage: ecp_check.py [--mutant M1..M7]', file=sys.stderr)
        return 2
    x1, x1d = control_X1()
    x2, x2d = control_X2()
    x3, nwin, nom = control_X3()
    x4, n4 = control_X4()
    x5 = control_X5()
    x6, x6d = control_X6()
    res = {'object': 'CL-ELDER-CUSP-PARITY-20261002-v1', 'scientific_effect': 'NONE',
           'controls': {'X1_lemma_Q_prime_and_CE': x1, 'X2_model_ridge_and_edges': x2, 'X3_pinned_fields_and_Omega_a': x3,
                        'X4_Q1_identities_and_parity': x4, 'X5_first_order_bookkeeping': x5, 'X6_corollary_and_ledgers': x6},
           'X1': x1d, 'X2': x2d, 'X3_window_fields_checked': nwin, 'X3_Omega_fields_checked': nom,
           'X4_instances_checked': n4, 'X6': x6d}
    ok = all(res['controls'].values())
    if MUT is None:
        print(json.dumps(res, indent=1, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
