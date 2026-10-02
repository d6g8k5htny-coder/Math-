#!/usr/bin/env python3
"""Exact controls for CL-FOLD-LIMIT-20261002-v1 (Theorem FL, Corollaries FL.5-FL.6, Proposition FL.4, Lemmas FL.1-FL.3;
PROOF.md).

Standard library only; exact rationals except the floating-point margins printed by F4 (a fixed, deterministic
construction of the model certificates on three parameter points). Output:
RESULTS.json (sorted keys), byte-identical under -O. Usage:
    python3 -B -S fold_check.py                 # exit 0, prints RESULTS.json
    python3 -B -S fold_check.py --mutant M3     # exit 1 (only its control fails; M1..M7)
    unknown mutant label                        -> exit 2

Controls
  F1  the model at the pins and the weight identity (3.5): det Hess G_w(M) = (1 + beta/2 - phi)/(4 phi),
      d_z^2 G_w(M) = -(1 + beta/2), det Hess G_w(S) = -(1 - beta/2 + phi)/(4 phi) (exact central differences, exact for
      cubics); the typed region {phi > 0, |phi - beta/2| < 1} = (2.4) of #242; the unnormalized determinants 6 lt + Y and
      -6 lt + Y (Y = 3kB - gamma^2/4); the normalization (lt/gamma^2) G_k(X, (gamma/lt) z) = G_w(X, z); and the window
      determinant identity |det Hess f| = k^(m-1) r^2 |det Hess F| for f = b + k r^3 F(L^-1 .), L = diag(r, rk, r^(3/2), ...),
      m = 1, 2, 3, with r = t^2 (exact)
  F2  Lemma FL.2: det d_w(grad G, G) = z^4 (X + 1/2)/(96 phi^2) and det d_w(grad G, G - L_S) = z^4 (X - 1/2)/(96 phi^2) as
      polynomial identities (psi = 1/phi, derivatives by exact polynomial differentiation); the critical values
      -z^2 (2 + beta)/12 on X = -1/2 and -z^2 (2 - beta)/12 on X = 1/2; A0 - L_S = (X - 1/2)^2 (X + 1)/(12 phi) and
      A0(2) = 25/(48 phi) (the axial path of Lemma FL.2(c)); the double
      root z = a/chi and the inflection value A0 + a^3/(6 chi^2) on D = 0, and the phi-scaling of A0 - L_S; the asymptotic
      ridge coefficients kappa_+- (2.2) (leading-order slice equation, and R(X)/X^3 at X = +-10^6 in floating point);
      kappa_+ = 0 for the witness; the Jacobian k^3 gamma^2/(12 mu^4) of (gamma, B, C3) -> w (exact differentiation)
  F3  Lemma FL.1: the exponent table (1.2) for every monomial of degree <= 4 (d = 2, 3, 4), the pinned/exact list, and the
      order-5 remainder; on exactly pinned degree-6 fields (d = 2 and d = 3, rational coefficients, r = t^2) the C^2 error
      of the soft window against G_k^(d) at 4 points drops by about 100 (d = 2) and 10 (d = 3) when r drops by 100
  F4  Proposition FL.4: the exact D' witness G_(3/2, 8/3, 20/3)(X, z) = (1/9) G_(1/6, 0, 0)(X + 2z, 3z) (polynomial identity);
      the factorization showing that G_(1/6, 0, 0) has exactly the critical points (+-1/2, 0) and (-3, 35/8), hence the
      witness exactly three, with values 0, -1/36, -125/384; the crossing forms at S on rational points (case (D): vertical
      descending -a(1/2) < 0, ridge tangent ascending R''(1/2) = det/G_zz > 0; case (D'): vertical ascending, valley tangent
      descending); the two facts used in Lemma FL.2(c) (beta > 2, chi < 0: the slice at 1/beta is open; chi > 0:
      D > a^2 on |X| < 1/2), on rational points; and the floating-point certificate margins on three fixed points, one per
      case (R), (D), (D')
  F5  Theorem FL: the change of variables 36 mu^2 - Y^2 = (gamma^4/16)(phi^-2 - (1 - t)^2), dmu/dphi = -gamma^2/(24 phi^2),
      (384/gamma^6)(gamma^4/16)(gamma^2/24) = 1, and chi = k^2 C3 gamma/mu^2 = chi0 phi^2, on random rationals
  F6  Corollaries FL.5-FL.6: the factorization (4.2) R - L_S = (X - 1/2)^2 [2(X + 1) + 3 phi (X + 1/2)^2]/(24 phi) at
      w = (phi, 0, 0) and its discriminant 4 - 12 phi; the concave slice (G = R at z_r = p/2); for phi in {2/5, 1/2, 3/4, 9/10},
      exact Sturm counts showing R > L_S + 1/200 on [-3, -1/2] and R(-3) > 0 (the (R) certificate along the ridge); the
      pushforward ell^(-1/3) (ell/k^2)/(3 k^(2/3)) = ell^(2/3) k^(-8/3)/3, the cumulative factor 3/5 and the cusp-cutoff
      exponent 2/3 - 5/12 = 1/4
"""
import json
import math
import sys
from fractions import Fraction as Fr

MUTANTS = ('M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7')
MUT = None
FACT = [math.factorial(n) for n in range(16)]
H = Fr(1, 2)


class LCG:
    def __init__(self, seed):
        self.s = seed % (2 ** 61 - 1)

    def nxt(self):
        self.s = (self.s * 437799614237992725 + 1) % (2 ** 61 - 1)
        return self.s

    def rat(self, num, den, nonzero=False):
        while True:
            x = Fr(self.nxt() % (2 * num + 1) - num, 1 + self.nxt() % den)
            if x != 0 or not nonzero:
                return x


# --------------------------------------------------------------------------------- sparse polynomials over Q
class P:
    """Polynomial in NV variables: dict exponent-tuple -> Fraction."""
    NV = 5

    def __init__(self, terms=None):
        self.t = {}
        for e, c in (terms or {}).items():
            c = Fr(c)
            if c != 0:
                self.t[e] = self.t.get(e, Fr(0)) + c
        self.t = {e: c for e, c in self.t.items() if c != 0}

    @staticmethod
    def const(c):
        return P({(0,) * P.NV: c})

    @staticmethod
    def var(i):
        e = [0] * P.NV; e[i] = 1
        return P({tuple(e): 1})

    def __add__(self, o):
        o = o if isinstance(o, P) else P.const(o)
        d = dict(self.t)
        for e, c in o.t.items():
            d[e] = d.get(e, Fr(0)) + c
        return P(d)

    __radd__ = __add__

    def __neg__(self):
        return P({e: -c for e, c in self.t.items()})

    def __sub__(self, o):
        return self + (-(o if isinstance(o, P) else P.const(o)))

    def __rsub__(self, o):
        return P.const(o) - self

    def __mul__(self, o):
        if not isinstance(o, P):
            return P({e: c * Fr(o) for e, c in self.t.items()})
        d = {}
        for e1, c1 in self.t.items():
            for e2, c2 in o.t.items():
                e = tuple(a + b for a, b in zip(e1, e2))
                d[e] = d.get(e, Fr(0)) + c1 * c2
        return P(d)

    __rmul__ = __mul__

    def __pow__(self, n):
        out = P.const(1)
        for _ in range(n):
            out = out * self
        return out

    def d(self, i):
        d = {}
        for e, c in self.t.items():
            if e[i] > 0:
                f = list(e); f[i] -= 1
                d[tuple(f)] = d.get(tuple(f), Fr(0)) + c * e[i]
        return P(d)

    def __eq__(self, o):
        o = o if isinstance(o, P) else P.const(o)
        return (self - o).t == {}

    def __call__(self, *vals):
        out = Fr(0)
        for e, c in self.t.items():
            v = c
            for x, n in zip(vals, e):
                if n:
                    v *= Fr(x) ** n
            out += v
        return out


def det2(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def mdet(A):
    A = [row[:] for row in A]
    n = len(A); s = Fr(1)
    for c in range(n):
        piv = next((i for i in range(c, n) if A[i][c] != 0), None)
        if piv is None:
            return Fr(0)
        if piv != c:
            A[c], A[piv] = A[piv], A[c]; s = -s
        s *= A[c][c]
        for i in range(c + 1, n):
            f = A[i][c] / A[c][c]
            A[i] = [a - f * b for a, b in zip(A[i], A[c])]
    return s


def solve(M, v):
    n = len(v)
    A = [row[:] + [v[i]] for i, row in enumerate(M)]
    for c in range(n):
        piv = next(i for i in range(c, n) if A[i][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c] / A[c][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[c])]
    return [A[i][n] / A[i][i] for i in range(n)]


# variables for F2: X, z, psi (= 1/phi), beta, chi
VX, VZ, VPSI, VB, VC = (P.var(i) for i in range(5))


def model_poly():
    A0 = (VX + H) ** 2 * (VX - 1) * VPSI * Fr(1, 12)
    G = A0 + H * (VX * VX - Fr(1, 4)) * VZ - H * (1 - VB * VX) * VZ * VZ + VC * VZ ** 3 * Fr(1, 6)
    return A0, G


def Gw(X, z, phi, beta, chi):
    X, z, phi, beta, chi = (Fr(v) for v in (X, z, phi, beta, chi))
    return ((X + H) ** 2 * (X - 1) / (12 * phi) + H * (X * X - Fr(1, 4)) * z - H * (1 - beta * X) * z * z
            + chi * z ** 3 / 6)


def Gk(X, ze, g, lt, k, B, C3):
    return (2 * (X + H) ** 2 * (X - 1) + H * (X * X - Fr(1, 4)) * g * ze - H * lt * ze * ze + H * k * B * X * ze * ze
            + k * k * C3 * ze ** 3 / 6)


def hess_num(f, x, y, h=Fr(1, 7)):
    """exact Hessian of a polynomial of degree <= 3 by central differences"""
    fxx = (f(x + h, y) - 2 * f(x, y) + f(x - h, y)) / (h * h)
    fyy = (f(x, y + h) - 2 * f(x, y) + f(x, y - h)) / (h * h)
    fxy = (f(x + h, y + h) - f(x + h, y - h) - f(x - h, y + h) + f(x - h, y - h)) / (4 * h * h)
    return [[fxx, fxy], [fxy, fyy]]


# ------------------------------------------------------------------------------------------------ F1
def control_F1():
    ok = True
    rng = LCG(901)
    n = 0
    for _ in range(40):
        phi = Fr(1 + rng.nxt() % 50, 1 + rng.nxt() % 20); beta = rng.rat(9, 4); chi = rng.rat(9, 4)
        f = lambda X, z: Gw(X, z, phi, beta, chi)
        HM = hess_num(f, -H, Fr(0)); HS = hess_num(f, H, Fr(0))
        detS_expected = -(1 - beta / 2 + phi) / (4 * phi)
        if MUT == 'M1':
            detS_expected = (1 - beta / 2 + phi) / (4 * phi)
        ok &= det2(HM) == (1 + beta / 2 - phi) / (4 * phi) and HM[1][1] == -(1 + beta / 2)
        ok &= det2(HS) == detS_expected
        typed = phi > 0 and abs(phi - beta / 2) < 1
        ok &= typed == (det2(HM) > 0 and HM[1][1] < 0 and det2(HS) < 0)
        # unnormalized blocks and the normalization
        k = Fr(1 + rng.nxt() % 9, 1 + rng.nxt() % 5); g = rng.rat(7, 3, nonzero=True); lt = Fr(1 + rng.nxt() % 9, 1 + rng.nxt() % 4)
        B = rng.rat(7, 3); C3 = rng.rat(7, 3); Y = 3 * k * B - g * g / 4
        fk = lambda X, ze: Gk(X, ze, g, lt, k, B, C3)
        ok &= det2(hess_num(fk, -H, Fr(0))) == 6 * lt + Y and det2(hess_num(fk, H, Fr(0))) == -6 * lt + Y
        ph, be, ch = g * g / (24 * lt), k * B / lt, k * k * C3 * g / lt ** 2
        for X, z in ((Fr(-3, 2), Fr(1, 3)), (Fr(1, 5), Fr(-2)), (Fr(2), Fr(5, 7))):
            ok &= lt / g ** 2 * Gk(X, g / lt * z, g, lt, k, B, C3) == Gw(X, z, ph, be, ch)
        n += 1
    # the window determinant identity: f = b + k r^3 F(L^-1 x), L = diag(r, r k, r^(3/2), ...), r = t^2
    wd = []
    for m in (1, 2, 3):
        for t in (Fr(1, 3), Fr(2, 7)):
            r = t * t; k = Fr(5, 4)
            L = [r, r * k] + [t ** 3] * (m - 1)
            HF = [[rng.rat(5, 3) for _ in range(m + 1)] for _ in range(m + 1)]
            HF = [[(HF[i][j] + HF[j][i]) / 2 for j in range(m + 1)] for i in range(m + 1)]
            # Hess f = k r^3 L^-1 HF L^-1 (L diagonal)
            Hf = [[k * r ** 3 * HF[i][j] / (L[i] * L[j]) for j in range(m + 1)] for i in range(m + 1)]
            ok &= mdet(Hf) == k ** (m - 1) * r ** 2 * mdet(HF)
            wd.append(m)
    return ok, {'random_parameter_points': n, 'window_identity_dims_checked': sorted(set(wd))}


# ------------------------------------------------------------------------------------------------ F2
def control_F2():
    ok = True
    A0, G = model_poly()
    GX, Gz = G.d(0), G.d(1)
    LS = VPSI * Fr(-1, 24)
    dphi = lambda F: -(VPSI * VPSI) * F.d(2)          # d/dphi = -psi^2 d/dpsi
    dbeta = lambda F: F.d(3)
    dchi = lambda F: F.d(4)
    # (b) the level conditions
    rows0 = [[dphi(F), dbeta(F), dchi(F)] for F in (GX, Gz, G)]
    rowsS = [[dphi(F), dbeta(F), dchi(F)] for F in (GX, Gz, G - LS)]
    c96 = Fr(1, 96) if MUT != 'M2' else Fr(1, 95)
    ok &= det3(rows0) == VZ ** 4 * (VX + H) * VPSI ** 2 * c96
    ok &= det3(rowsS) == VZ ** 4 * (VX - H) * VPSI ** 2 * c96
    # (c) the lines X = -1/2 and X = 1/2
    rng = LCG(902)
    for _ in range(12):
        beta = rng.rat(9, 4, nonzero=True); phi = Fr(1 + rng.nxt() % 30, 1 + rng.nxt() % 9)
        z = 1 / beta; chi = beta * (2 + beta)                        # X = -1/2: z = (2 + beta)/chi = 1/beta
        vals = (-H, z, 1 / phi, beta, chi)
        ok &= GX(*vals) == 0 and Gz(*vals) == 0 and G(*vals) == -z * z * (2 + beta) / 12
        z = -1 / beta; chi = beta * beta - 2 * beta                   # X = 1/2: z = (2 - beta)/chi = -1/beta
        if chi != 0:
            vals = (H, z, 1 / phi, beta, chi)
            ok &= GX(*vals) == 0 and Gz(*vals) == 0 and G(*vals) - LS(*vals) == -z * z * (2 - beta) / 12
    # (d) A0 - L_S, and the end of the axial path: A0(2) = 25/(48 phi)
    ok &= A0 - LS == (VX - H) ** 2 * (VX + 1) * VPSI * Fr(1, 12)
    for phi in (Fr(1, 7), Fr(2, 3), Fr(5, 2)):
        ok &= A0(Fr(2), Fr(0), 1 / phi, Fr(0), Fr(0)) == Fr(25, 48) / phi
    # (e) the inflection value on D = 0 and its phi-derivative
    for _ in range(12):
        X = rng.rat(9, 4); beta = rng.rat(5, 3); phi = Fr(1 + rng.nxt() % 30, 1 + rng.nxt() % 9)
        p = X * X - Fr(1, 4); a = 1 - beta * X
        if p == 0 or a == 0:
            continue
        chi = a * a / p                                               # D = a^2 - chi p = 0
        zi = a / chi
        vals = (X, zi, 1 / phi, beta, chi)
        ok &= Gz(*vals) == 0 and Gz.d(1)(*vals) == 0                   # double critical point of the slice
        ok &= G(*vals) == A0(*vals) + a ** 3 / (6 * chi * chi)
    # d/dphi (A0 + a^3/(6 chi^2) - L_S) = -(A0 - L_S)/phi: A0 - L_S is phi^-1 times a function of X alone
    for _ in range(6):
        X = rng.rat(9, 4); ph1 = Fr(1 + rng.nxt() % 30, 1 + rng.nxt() % 9); ph2 = ph1 + Fr(1, 3)
        AL = lambda ph: (X + H) ** 2 * (X - 1) / (12 * ph) + Fr(1, 24) / ph
        ok &= AL(ph1) * ph1 == AL(ph2) * ph2
    # (f) kappa_+- : series of z_r and float check of R(X)/X^3
    kap = []
    for (phi, beta, chi) in ((Fr(1, 2), Fr(1, 3), Fr(-2)), (Fr(3, 2), Fr(8, 3), Fr(20, 3)), (Fr(1, 5), Fr(-2), Fr(3)),
                             (Fr(2, 3), Fr(5, 2), Fr(-1, 4))):
        om2 = beta * beta - chi
        if om2 <= 0:
            continue
        omf = math.sqrt(float(om2))
        kp = 1 / (12 * float(phi)) + (2 * omf - float(beta)) / (6 * (omf - float(beta)) ** 2)
        km = 1 / (12 * float(phi)) - (2 * omf + float(beta)) / (6 * (omf + float(beta)) ** 2)
        # zeta0 = 1/(omega - beta) solves (chi/2) z^2 + beta z + 1/2 = 0 (leading order of the slice equation)
        z0 = 1 / (omf - float(beta))
        ok &= abs(float(chi) / 2 * z0 * z0 + float(beta) * z0 + 0.5) < 1e-12
        ok &= abs(kp - (1 / (12 * float(phi)) + z0 / 3 + float(beta) * z0 * z0 / 6)) < 1e-12
        for X, kexp in ((1e6, kp), (-1e6, km)):
            p = X * X - 0.25; a = 1 - float(beta) * X; Dd = a * a - float(chi) * p
            sq = math.sqrt(Dd)
            zr = p / (a + sq) if a >= 0 else (a - sq) / float(chi)
            R = (X + 0.5) ** 2 * (X - 1) / (12 * float(phi)) + p * zr / 3 - a * zr * zr / 6
            ok &= abs(R / X ** 3 - kexp) < 1e-5 * (1 + abs(kexp))
        kap.append([str(phi), str(beta), str(chi), round(kp, 9), round(km, 9)])
    # the D' witness has kappa_+ = 0 exactly (beta^2 - chi = 4/9, omega = 2/3): R = O(X^2) on the right
    om = Fr(2, 3); phi, beta = Fr(3, 2), Fr(8, 3)
    ok &= 1 / (12 * phi) + (2 * om - beta) / (6 * (om - beta) ** 2) == 0
    # (g) the Jacobian of (gamma, B, C3) -> (phi, beta, chi) at fixed mu, k, by exact differentiation
    VG, VBB, VC3 = P.var(0), P.var(1), P.var(2)
    for _ in range(8):
        mu = Fr(1 + rng.nxt() % 9, 1 + rng.nxt() % 4); k = Fr(1 + rng.nxt() % 9, 1 + rng.nxt() % 4)
        w = [VG * VG * (1 / (24 * mu)), VBB * (k / mu), VC3 * VG * (k * k / mu ** 2)]
        J = [[w[i].d(j) for j in range(3)] for i in range(3)]
        ok &= det3(J) == VG * VG * (k ** 3 / (12 * mu ** 4))
    return ok, {'kappa_pm_float': kap, 'witness_kappa_plus': '0'}


# ------------------------------------------------------------------------------------------------ F3
def control_F3():
    ok = True
    table = {}
    for d in (2, 3, 4):
        mdim = d - 1
        listed = 0; checked = 0
        for i in range(5):
            for j in range(5 - i):
                for L in range(5 - i - j):
                    if mdim == 1 and L > 0:
                        continue
                    e = Fr(i + j) + Fr(3 * L, 2) - 3
                    if MUT == 'M3':
                        e = Fr(i + j + L) - 3
                    deg = i + j + L
                    pinned_or_exact = ((L == 0 and i + j <= 3) or (L == 2 and i == j == 0) or (L == 1 and i + j <= 1))
                    if pinned_or_exact:
                        listed += 1
                        continue
                    checked += 1
                    bound = Fr(1, 2) if L == 1 else Fr(1)
                    ok &= e >= bound and deg >= 3
        # Taylor remainder of order 5: e >= 2 for every (i, j, L) with i + j + L = 5
        for i in range(6):
            for j in range(6 - i):
                L = 5 - i - j
                if mdim == 1 and L > 0:
                    continue
                ok &= Fr(i + j) + Fr(3 * L, 2) - 3 >= 2
        table[str(d)] = {'listed_pinned_or_exact': listed, 'checked_monomials': checked}
    # exactly pinned degree-6 fields: d = 2 and d = 3
    rates = {}
    for d in (2, 3):
        rng = LCG(903 + d)
        if d == 2:
            mono = [(i, n - i, 0) for n in range(7) for i in range(n, -1, -1)]
            pinned = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 1, 0), (1, 1, 0)]
        else:
            mono = [(i, j, n - i - j) for n in range(7) for i in range(n + 1) for j in range(n + 1 - i)]
            pinned = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (1, 0, 1)]

        def val(cc, x, y, w, dx=0, dy=0, dw=0):
            out = Fr(0)
            for (i, j, l), v in cc.items():
                if i >= dx and j >= dy and l >= dw:
                    out += v * x ** (i - dx) * y ** (j - dy) * w ** (l - dw) / (FACT[i - dx] * FACT[j - dy] * FACT[l - dw])
            return out
        k = Fr(2, 3); lt = Fr(3, 2); b = Fr(1, 5); mu = Fr(-5, 4)          # stiff A_22 = mu < 0
        free = {mm: rng.rat(5, 3) for mm in mono if mm not in pinned}
        if d == 3:
            free[(0, 1, 1)] = Fr(0); free[(0, 0, 2)] = mu
        errs = []
        ts = (Fr(1, 10), Fr(1, 100)) if d == 2 else (Fr(1, 100), Fr(1, 1000))
        for t in ts:
            r = t * t
            c = dict(free); c[(0, 2, 0)] = -lt * r / k
            rows, rhs = [], []
            pins = [((-r / 2), b, (0, 0, 0)), (r / 2, b - k * r ** 3, (0, 0, 0)), (-r / 2, 0, (1, 0, 0)), (r / 2, 0, (1, 0, 0)),
                    (-r / 2, 0, (0, 1, 0)), (r / 2, 0, (0, 1, 0))]
            if d == 3:
                pins += [(-r / 2, 0, (0, 0, 1)), (r / 2, 0, (0, 0, 1))]
            for (x, target, kind) in pins:
                rows.append([val({mm: Fr(1)}, x, Fr(0), Fr(0), *kind) for mm in pinned])
                rhs.append(target - val(c, x, Fr(0), Fr(0), *kind))
            for mm, v in zip(pinned, solve(rows, rhs)):
                c[mm] = v
            g, B, C3 = c[(2, 1, 0)], c[(1, 2, 0)], c[(0, 3, 0)]
            sx, sy, sw = r, r * k, t ** 3                                  # x = r X, y = r k zeta, w = r^(3/2) eta
            e = []
            for X, ze, et in ((Fr(-3, 2), Fr(1, 3), Fr(1, 2)), (Fr(-1, 2), Fr(2), Fr(-1)), (Fr(1, 3), Fr(-1), Fr(2)),
                              (Fr(2), Fr(1, 2), Fr(1, 3))):
                if d == 2:
                    et = Fr(0)
                x, y, w = sx * X, sy * ze, sw * et
                s = k * r ** 3
                # window field and its derivatives (chain rule), minus the model G_k - (1/(2k)) lambda_2 eta^2
                F0 = (val(c, x, y, w) - b) / s
                lam2 = -mu
                Gm = Gk(X, ze, g, lt, k, B, C3) - lam2 * et * et / (2 * k)
                err = [abs(F0 - Gm)]
                # first and second derivatives of the model (exact, by hand)
                GX = 2 * (2 * (X + H) * (X - 1) + (X + H) ** 2) + X * g * ze + H * k * B * ze * ze
                Gz = H * (X * X - Fr(1, 4)) * g - lt * ze + k * B * X * ze + k * k * C3 * ze * ze / 2
                Ge = -lam2 * et / k
                GXX = 2 * (2 * (X - 1) + 4 * (X + H)) + g * ze
                GXz = X * g + k * B * ze
                Gzz = -lt + k * B * X + k * k * C3 * ze
                Gee = -lam2 / k
                derivs = [((1, 0, 0), sx, GX), ((0, 1, 0), sy, Gz), ((2, 0, 0), sx * sx, GXX), ((1, 1, 0), sx * sy, GXz),
                          ((0, 2, 0), sy * sy, Gzz)]
                if d == 3:
                    derivs += [((0, 0, 1), sw, Ge), ((0, 0, 2), sw * sw, Gee), ((1, 0, 1), sx * sw, Fr(0)),
                               ((0, 1, 1), sy * sw, Fr(0))]
                for (dx, dy, dw), fac, gm in derivs:
                    err.append(abs(val(c, x, y, w, dx, dy, dw) * fac / s - gm))
                e.append(max(err))
            errs.append(max(e))
        ratio = errs[0] / errs[1]
        expected = Fr(100) if d == 2 else Fr(10)                           # r drops by 100: rate r (d=2), r^(1/2) (d=3)
        ok &= expected / 3 <= ratio <= 3 * expected
        rates[str(d)] = {'C2_error_at_two_r': [str(float(v)) for v in errs], 'ratio': str(float(ratio)),
                         'expected_ratio': str(expected)}
    return ok, {'exponent_table': table, 'pinned_fields': rates}


# ------------------------------------------------------------------------------------------------ F4
def slice_crit(X, phi, beta, chi):
    """float: (z_r, z_v, R, V) of the slice, or None if open"""
    p = X * X - 0.25; a = 1 - beta * X; Dd = a * a - chi * p
    if Dd <= 0:
        return None
    sq = math.sqrt(Dd)
    if a >= 0:
        zr = p / (a + sq); zv = (a + sq) / chi
    else:
        zr = (a - sq) / chi; zv = p / (a - sq)
    A0 = (X + 0.5) ** 2 * (X - 1) / (12 * phi)
    crit = lambda z: A0 + p * z / 3 - a * z * z / 6
    return zr, zv, crit(zr), crit(zv)


def gw_f(X, z, phi, beta, chi):
    return ((X + 0.5) ** 2 * (X - 1) / (12 * phi) + 0.5 * (X * X - 0.25) * z - 0.5 * (1 - beta * X) * z * z + chi * z ** 3 / 6)


def certificate_margins(case, phi, beta, chi, n=4000):
    """float margins of the constructions of Proposition FL.4, Step 3, on the model (fixed grids)."""
    LS = -1.0 / (24 * phi)
    sgn = 1.0 if chi > 0 else -1.0
    out = {}
    if case == 'R':
        # path: the ridge from -1/2 leftwards until R > 0 (for this point M dies on the left ridge)
        vals = []
        for i in range(n + 1):
            X = -0.5 - 6.0 * i / n
            c = slice_crit(X, phi, beta, chi)
            vals.append(c[2])
            if c[2] > 0.05:
                break
        out['path_min_minus_LS'] = min(vals) - LS
        out['endpoint_value'] = vals[-1]
        return out

    def scan(direction, stop_at_half):
        X = -0.5
        while True:
            Xn = X + direction * 1e-3
            c = slice_crit(Xn, phi, beta, chi)
            if c is None or c[2] <= LS:
                return Xn
            if stop_at_half and Xn >= 0.5:
                return 0.5
            X = Xn
    XL = scan(-1, False)
    XR = scan(+1, case == 'D')
    tau = 0.02
    while any(slice_crit(XL - tau * i / 20, phi, beta, chi) is None for i in range(21)) or (
            case != 'D' and any(slice_crit(XR + tau * i / 20, phi, beta, chi) is None for i in range(21))):
        tau /= 2
    J = (XL - tau, (0.5 if case == 'D' else XR + tau))
    Z = 30.0
    bmax = -1e9; imax_off = -1e9
    rho = 0.08
    for i in range(n + 1):
        X = J[0] + (J[1] - J[0]) * i / n
        zr, zv, R, V = slice_crit(X, phi, beta, chi)
        zd = zr - Z * sgn
        if not (case == "D'" and abs(X - 0.5) < rho):
            bmax = max(bmax, V - LS)                       # the valley boundary (off the crossing arc)
        bmax = max(bmax, gw_f(X, zd, phi, beta, chi) - LS)  # the dead-end boundary
        if abs(X + 0.5) > rho:
            imax_off = max(imax_off, R)                    # interior: G <= R(X) on each closed slice segment
        if i == 0 or (i == n and case != 'D'):
            bmax = max(bmax, R - LS)                       # vertical sides
    out['I_M'] = [round(XL, 3), round(XR, 3)]
    out['tau'] = tau
    out['boundary_max_minus_LS'] = bmax
    out['interior_max_off_M'] = imax_off
    if case == 'D':
        # the right side: the slice at 1/2 between z_d and z_v, off |z| < rho; and the ridge path margins
        zr, zv, R, V = slice_crit(0.5, phi, beta, chi)
        zs = [zr - Z * sgn + (zv - zr + Z * sgn) * i / n for i in range(n + 1)]
        out['right_side_max_minus_LS_off_S'] = max(gw_f(0.5, z, phi, beta, chi) - LS for z in zs if abs(z) > rho)
        out['ridge_path_min_minus_LS_off_S'] = min(slice_crit(-0.5 + (1 - rho) * i / n, phi, beta, chi)[2] - LS
                                                     for i in range(n + 1))
        X1 = 0.5 + rho
        out['A0_minus_LS_at_X1'] = (X1 + 0.5) ** 2 * (X1 - 1) / (12 * phi) - LS
    if case == "D'":
        zr, zv, R, V = slice_crit(0.5, phi, beta, chi)
        far = -1.0 if zr > 0 else 1.0
        zs = [zr + (far * 40 - zr) * i / n for i in range(n + 1)]
        vs = [gw_f(0.5, z, phi, beta, chi) for z in zs]
        out['slice_path_min_minus_LS_off_S'] = min(v - LS for z, v in zip(zs, vs) if abs(z) > rho)
        out['slice_path_end_value'] = max(vs)
        out['ridge_path_min_minus_LS'] = min(slice_crit(-0.5 + i / n, phi, beta, chi)[2] - LS for i in range(n + 1))
    return out


def control_F4():
    ok = True
    # (a) the exact D' witness
    A0, G = model_poly()
    Xp, zp = VX + 2 * VZ, 3 * VZ
    def subst(F, phi, beta, chi, Xs, zs):
        out = P.const(0)
        for e, c in F.t.items():
            out = out + (Xs ** e[0]) * (zs ** e[1]) * (c * (1 / Fr(phi)) ** e[2] * Fr(beta) ** e[3] * Fr(chi) ** e[4])
        return out
    lhs = subst(G, Fr(3, 2), Fr(8, 3), Fr(20, 3), VX, VZ)
    rhs = subst(G, Fr(1, 6), Fr(0), Fr(0), Xp, zp) * Fr(1, 9)
    ok &= lhs == rhs
    # critical points of G_(1/6,0,0): (+-1/2, 0) and (-3, 35/8); images under the inverse shear (X, z) = (x - 2w/3, w/3)
    g0 = lambda x, w: Gw(x, w, Fr(1, 6), 0, 0)
    crit0 = [(-H, Fr(0)), (H, Fr(0)), (Fr(-3), Fr(35, 8))]
    vals = []
    GXp, Gzp = G.d(0), G.d(1)
    for x, w in crit0:
        X, z = x - 2 * w / 3, w / 3
        args = (X, z, Fr(2, 3), Fr(8, 3), Fr(20, 3))                 # psi = 1/phi = 2/3
        ok &= GXp(*args) == 0 and Gzp(*args) == 0
        vals.append(G(*args))
        ok &= vals[-1] == g0(x, w) / 9
    ok &= vals == [Fr(0), Fr(-1, 36), Fr(-125, 384)]
    # exactly three critical points of G_(1/6,0,0): d_z G = (x^2 - 1/4)/2 - z vanishes iff z = (x^2 - 1/4)/2, and then
    # d_x G(x, (x^2 - 1/4)/2) = (x^2 - 1/4)(3/2 + x/2) = (x + 1/2)(x - 1/2)(x + 3)/2 as a polynomial in x
    G0 = subst(G, Fr(1, 6), Fr(0), Fr(0), VX, VZ)
    ok &= G0.d(1) == (VX * VX - Fr(1, 4)) * H - VZ
    zr0 = (VX * VX - Fr(1, 4)) * H
    gx_on = subst(G0.d(0), Fr(1), Fr(0), Fr(0), VX, zr0)
    ok &= gx_on == (VX + H) * (VX - H) * (VX + 3) * H
    # (b) crossing forms at S on rational points
    rng = LCG(904)
    nD = nDp = 0
    for _ in range(60):
        phi = Fr(1 + rng.nxt() % 40, 1 + rng.nxt() % 20); beta = rng.rat(12, 3); chi = rng.rat(9, 4, nonzero=True)
        if not (abs(phi - beta / 2) < 1) or beta == 2:
            continue
        HS = hess_num(lambda X, z: Gw(X, z, phi, beta, chi), H, Fr(0))
        a_half = 1 - beta / 2
        ok &= HS[1][1] == -a_half
        schur = det2(HS) / HS[1][1]                                   # R''(1/2) in (D), V''(1/2) in (D')
        tangent = (Fr(1), -HS[0][1] / HS[1][1])
        form = (HS[0][0] * tangent[0] ** 2 + 2 * HS[0][1] * tangent[0] * tangent[1] + HS[1][1] * tangent[1] ** 2)
        ok &= form == schur
        if MUT == 'M4':
            schur = -schur
        if a_half > 0:
            ok &= HS[1][1] < 0 and schur > 0                          # (D): vertical descending, ridge tangent ascending
            nD += 1
        else:
            ok &= HS[1][1] > 0 and schur < 0                          # (D'): vertical ascending, valley tangent descending
            nDp += 1
    # the witness: (D') forms
    HSw = hess_num(lambda X, z: Gw(X, z, Fr(3, 2), Fr(8, 3), Fr(20, 3)), H, Fr(0))
    ok &= HSw[1][1] == Fr(1, 3) and det2(HSw) / HSw[1][1] < 0
    # (c) float certificate margins on four fixed points
    pts = {'R': (0.5, 0.0, 0.001), 'D': (0.2, 0.2, 0.1), "D'": (1.5, 8 / 3, 20 / 3)}
    marg = {}
    for case, (phi, beta, chi) in pts.items():
        m = certificate_margins(case, phi, beta, chi)
        marg[case] = {k: (round(v, 6) if isinstance(v, float) else v) for k, v in m.items()}
        if case == 'R':
            ok &= m['path_min_minus_LS'] > 0 and m['endpoint_value'] > 0
        else:
            ok &= m['boundary_max_minus_LS'] < 0 and m['interior_max_off_M'] < 0
            if case == 'D':
                ok &= (m['right_side_max_minus_LS_off_S'] < 0 and m['ridge_path_min_minus_LS_off_S'] > 0
                       and m['A0_minus_LS_at_X1'] > 0)
            if case == "D'":
                ok &= (m['slice_path_min_minus_LS_off_S'] > 0 and m['slice_path_end_value'] > 0
                       and m['ridge_path_min_minus_LS'] > 0)
    # Lemma FL.2(c): the inequalities behind the trichotomy, exactly on rational points
    tri = {'beta>2,chi<0 open at 1/beta': 0, 'chi>0: D > a^2 on |X| < 1/2': 0}
    for _ in range(40):
        beta = 2 + Fr(1 + rng.nxt() % 40, 1 + rng.nxt() % 9); chi = -Fr(1 + rng.nxt() % 50, 1 + rng.nxt() % 9)
        X = 1 / beta; p = X * X - Fr(1, 4); a = 1 - beta * X
        ok &= a == 0 and p < 0 and a * a - chi * p < 0
        tri['beta>2,chi<0 open at 1/beta'] += 1
        chi2 = -chi; X2 = rng.rat(9, 20)
        if abs(X2) < H:
            p2 = X2 * X2 - Fr(1, 4); a2 = 1 - beta * X2; D2 = a2 * a2 - chi2 * p2
            ok &= (D2 > a2 * a2) if MUT != 'M7' else (D2 < a2 * a2)       # so sqrt(D) > |a|: z_r < 0 < z_v
            tri['chi>0: D > a^2 on |X| < 1/2'] += 1
    return ok, {'witness_critical_values': [str(v) for v in vals], 'crossing_forms_points': {'D': nD, "D'": nDp},
                'certificate_margins_float': marg, 'trichotomy_points': tri}


# ------------------------------------------------------------------------------------------------ F5
def control_F5():
    ok = True
    rng = LCG(905)
    for _ in range(30):
        g = rng.rat(9, 4, nonzero=True); k = Fr(1 + rng.nxt() % 9, 1 + rng.nxt() % 4); B = rng.rat(9, 4)
        C3 = rng.rat(9, 4); phi = Fr(1 + rng.nxt() % 50, 1 + rng.nxt() % 20)
        mu = g * g / (24 * phi); t = 12 * k * B / g ** 2; Y = 3 * k * B - g * g / 4
        ok &= 36 * mu * mu - Y * Y == g ** 4 / 16 * (phi ** -2 - (1 - t) ** 2)
        # dmu/dphi exactly via the difference quotient of the rational function g^2/(24 phi)
        e = Fr(1, 10 ** 5)
        ok &= ((g * g / (24 * (phi + e))) - mu) / e == -g * g / (24 * phi * (phi + e))
        ok &= k * k * C3 * g / mu ** 2 == 576 * k * k * C3 / g ** 3 * phi ** 2
    c384 = Fr(384) if MUT != 'M5' else Fr(385)
    ok &= c384 * Fr(1, 16) * Fr(1, 24) == 1
    return ok, {'random_points': 30}


# ------------------------------------------------------------------------------------------------ F6
def sturm_count(poly, lo, hi):
    """number of distinct real roots of poly (list of Fraction coefficients, low to high) in (lo, hi]"""
    def trim(p):
        while len(p) > 1 and p[-1] == 0:
            p = p[:-1]
        return p
    def deriv(p):
        return [i * p[i] for i in range(1, len(p))] or [Fr(0)]
    def rem(a, b):
        a = a[:]
        while len(a) >= len(b) and any(a):
            f = a[-1] / b[-1]; s = len(a) - len(b)
            for i in range(len(b)):
                a[s + i] -= f * b[i]
            a = trim(a[:-1]) if a[-1] == 0 else trim(a)
            if len(a) < len(b):
                break
        return trim(a)
    seq = [trim(poly), trim(deriv(poly))]
    while len(seq[-1]) > 1 or seq[-1][0] != 0:
        r = rem(seq[-2], seq[-1])
        if r == [Fr(0)] or not any(r):
            break
        seq.append([-c for c in r])
    def ev(p, x):
        out = Fr(0)
        for c in reversed(p):
            out = out * x + c
        return out
    def changes(x):
        vals = [ev(p, x) for p in seq]
        vals = [v for v in vals if v != 0]
        return sum(1 for u, v in zip(vals, vals[1:]) if (u > 0) != (v > 0))
    return changes(lo) - changes(hi)


def polymul(a, b):
    out = [Fr(0)] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            out[i + j] += u * v
    return out


def control_F6():
    ok = True
    # the factorization (4.2): with psi = 1/phi, 24 (R - L_S) = psi (X - 1/2)^2 2 (X + 1) + 3 (X - 1/2)^2 (X + 1/2)^2,
    # i.e. R - L_S = (X - 1/2)^2 [2 (X + 1) + 3 phi (X + 1/2)^2]/(24 phi); discriminant of the bracket in X: 4 - 12 phi
    Rpoly = (VX + H) ** 2 * (VX - 1) * VPSI * Fr(1, 12) + (VX * VX - Fr(1, 4)) ** 2 * Fr(1, 8)
    LSp = VPSI * Fr(-1, 24)
    rhs = (VX - H) ** 2 * ((VX + 1) * 2 * VPSI + (VX + H) ** 2 * 3) * Fr(1, 24)
    ok &= Rpoly - LSp == rhs
    for phi in (Fr(1, 5), Fr(1, 3), Fr(2, 5), Fr(7, 9)):
        a2, a1, a0 = 3 * phi, 3 * phi + 2, 3 * phi / 4 + 2           # 2(X + 1) + 3 phi (X + 1/2)^2 = a2 X^2 + a1 X + a0
        ok &= a1 * a1 - 4 * a2 * a0 == 4 - 12 * phi
    # R(X) at w = (phi, 0, 0) equals g/(24 phi kappa), g = kappa [2 (X+1/2)^2 (X-1) + 3 phi (X^2-1/4)^2]
    rng = LCG(906)
    for _ in range(10):
        phi = Fr(1 + rng.nxt() % 50, 1 + rng.nxt() % 20); X = rng.rat(9, 4)
        R = (X + H) ** 2 * ((X - 1) / (12 * phi) + (X - H) ** 2 / 8)
        g_over_kappa = 2 * (X + H) ** 2 * (X - 1) + 3 * phi * (X * X - Fr(1, 4)) ** 2
        ok &= R == g_over_kappa / (24 * phi)
        # the concave slice: G(X, z) <= R(X) with equality at z_r = p/2 (a = 1)
        zr = (X * X - Fr(1, 4)) / 2
        ok &= Gw(X, zr, phi, 0, 0) == R and Gw(X, zr + Fr(1, 3), phi, 0, 0) < R
    # (R) certificates on the concave ridge, exactly: R - L_S - delta has no root on [-3, -1/2] and R(-3) > 0
    cert = {}
    for phi in (Fr(2, 5), Fr(1, 2), Fr(3, 4), Fr(9, 10)):
        LS = Fr(-1, 24) / phi
        # R(X) = (X + 1/2)^2 [(X - 1)/(12 phi) + (X - 1/2)^2 / 8] as coefficients in X (low to high)
        sq = [Fr(1, 4), Fr(1), Fr(1)]                                        # (X + 1/2)^2
        inner = [Fr(-1) / (12 * phi) + Fr(1, 32), Fr(1) / (12 * phi) - Fr(1, 8), Fr(1, 8)]
        Rc = polymul(sq, inner)
        delta = Fr(1, 200) if MUT != 'M6' else Fr(10)
        poly = Rc[:]; poly[0] -= LS + delta
        roots = sturm_count(poly, Fr(-3), -H)
        Rm3 = sum(c * Fr(-3) ** i for i, c in enumerate(Rc))
        ok &= roots == 0 and Rm3 > 0
        ok &= sum(c * (-H) ** i for i, c in enumerate(poly)) > 0            # sign at -1/2 (then on all of [-3, -1/2])
        cert[str(phi)] = {'roots_of_R_minus_LS_minus_delta_on_[-3,-1/2]': roots, 'R(-3)': str(Rm3)}
    # corollary bookkeeping
    for _ in range(6):
        k = Fr(1 + rng.nxt() % 9, 1 + rng.nxt() % 4); s = Fr(1 + rng.nxt() % 9, 1 + rng.nxt() % 7)
        ell = k * s ** 3; r = s                                              # r = (ell/k)^(1/3)
        ok &= r ** 3 == ell / k
        # r dr/dell = (1/3) k^(-2/3) ell^(-1/3): with r = (ell/k)^(1/3), dr/dell = r/(3 ell)
        ok &= r * (r / (3 * ell)) == Fr(1, 3) * (r * r / ell)               # = (1/3) k^(-2/3) ell^(-1/3)
        ok &= (r * r / ell) ** 3 == 1 / (k * k * ell)
    e7 = Fr(-1, 3) + 1 - Fr(2, 3)                                            # ell^(-1/3) * ell * k^-2 * k^(-2/3)
    ok &= e7 == 0 and Fr(-1, 3) + 1 == Fr(2, 3) and -2 - Fr(2, 3) == Fr(-8, 3)
    ok &= Fr(2, 3) + 1 == Fr(5, 3) and 1 / Fr(5, 3) == Fr(3, 5)
    ok &= Fr(-8, 3) + 1 == Fr(-5, 3) and Fr(1, 4) * Fr(-5, 3) == Fr(-5, 12) and Fr(2, 3) - Fr(5, 12) == Fr(1, 4)
    return ok, {'R_certificates_phi_0_0': cert}


def main(argv):
    global MUT
    if len(argv) == 2 and argv[0] == '--mutant':
        if argv[1] not in MUTANTS:
            print('unknown mutant label', file=sys.stderr)
            return 2
        MUT = argv[1]
    elif argv:
        print('usage: fold_check.py [--mutant M1..M7]', file=sys.stderr)
        return 2
    f1, f1d = control_F1()
    f2, f2d = control_F2()
    f3, f3d = control_F3()
    f4, f4d = control_F4()
    f5, f5d = control_F5()
    f6, f6d = control_F6()
    res = {'object': 'CL-FOLD-LIMIT-20261002-v1', 'scientific_effect': 'NONE',
           'controls': {'F1_model_pins_and_weight': f1, 'F2_lemma_FL2_generic': f2, 'F3_lemma_FL1_window': f3,
                        'F4_proposition_FL4_certificates': f4, 'F5_theorem_FL_bookkeeping': f5, 'F6_corollaries': f6},
           'F1': f1d, 'F2': f2d, 'F3': f3d, 'F4': f4d, 'F5': f5d, 'F6': f6d}
    ok = all(res['controls'].values())
    if MUT is None:
        print(json.dumps(res, indent=1, sort_keys=True))
    else:
        print('mutant ' + MUT + ': failing controls ' + ', '.join(sorted(k for k, v in res['controls'].items() if not v)),
              file=sys.stderr)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
