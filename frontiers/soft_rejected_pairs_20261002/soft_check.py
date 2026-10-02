#!/usr/bin/env python3
"""Exact controls for CL-SOFT-REJECTED-20261002-v1 (Theorem 1, Lemmas 2, 3 and 5, Proposition 4; PROOF.md).

Standard library only; exact rationals except control S8 (a deterministic floating-point implementation of Lemma 2 on
fixed cases). Output: RESULTS.json (sorted keys), byte-identical under -O. Usage:
    python3 -B -S soft_check.py                 # exit 0, prints RESULTS.json
    python3 -B -S soft_check.py --mutant M3     # exit 1 (only its control fails)
    unknown mutant label                        -> exit 2

Controls
  S1  Theorem 1: the change of variables in (1.1) (69984 kappa^3 / 72^4 = 1/384 per kappa), int_{1/3}^1 (phi^-4 - phi^-2)
      = 20/3, 12 (20/3)/384 = 5/24, and F0 = 25 pi0 pA(0|b) for E gamma^6 = 15 sigma^6, sigma^2 = 2; the soft window
      lambda in [gamma^2/(24 kappa), gamma^2/(8 kappa)] at f4 = 0
  S2  the algebra of the model (2.1)-(2.4): partial derivatives of G_k (exact 4-point stencils), the pins,
      det H_M = 6 lt + Y, det H_S = -6 lt + Y with Y = 3kB - gamma^2/4, the normalization G_k(X, (gamma/lt) z) =
      (gamma^2/lt) G(X, z), the weight 36 lt^2 - Y^2 = (gamma^4/16)(phi^-2 - c'^2), the measure, and the typed window (2.4),
      on random rationals
  S3  the Gaussian kernel exp(-|x|^2/2): covariances of (f, grad, Hessian, third and fourth jets) from Hermite numbers;
      given grad f = 0 the third-order jets (f_uuu, gamma, B, C3) are independent with variances (6, 2, 2, 6) and
      uncorrelated with every even jet; the pin factor exp(-144 k^2 / (2 * 6)) = exp(-12 k^2)   [(0.3)]
  S4  the elder edge (3.3): truncated power series in t (exact) for the tangency R = L_S, R' = 0 of the ridge
      2(X + 1/2)^2 (X - 1) + 3 phi (X^2 - 1/4)^2 / (1 - 2 t phi X) at X = -3/2 - t/3 - t^2/3, phi = 1/3 + t/3 + 10 t^2/27;
      the factorization at t = 0 and its nondegeneracy (Jacobian -96)
  S5  (3.4): I(t, 0) = 20/3 - 20 t + 52 t^2/3 + O(t^3) from (3.3) and the typed edge 1/(1 - t)
  S6  Proposition 4: E gamma^6 = 120, E[gamma^6 t^2] = 576 k^2, (52/3) 576 / 800 = 312/25, 312/25 - 12 = 12/25; the moment
      identities gamma^6 |t|^3 = 1728 |k|^3 |B|^3, gamma^6 chi0^2 = 331776 k^4 C3^2, gamma^6 |t chi0| = 6912 |k|^3 |B C3 gamma|
  S7  Lemma 3: every numerical inequality of its proof, with exact rational bounds (including s/a in [0.99, 1.01] and the
      critical-value formulas h(z_r) = p^2 (a + 2s)/(6 (a + s)^2), h(z_v) = (a + s)^2 (a - 2s)/(6 chi^2), checked as
      identities at rational points with s rational)
  S8  Lemma 2 (floating point, fixed cases): the decision on 16 parameter points with known answers (cusp edge 1/3,
      beta > 2 with and without C3, the valley at M, chi^2 = 16 phi, the open slice, the a priori region of Lemma 3)
  S9  Lemma 5: the exponent bookkeeping of its three error terms (all 3/4) and the convergence exponents of I~
  S10 the limit (2.1): on three exactly pinned degree-6 fields with A = -lt r/k, (f(rX, rk zeta) - b)/(k r^3) equals
      G_k + r G1 + O(r^2) at four points (G1 explicit), checked at r = 1/1000 and 1/10000 in exact arithmetic
"""
import json
import math
import sys
from fractions import Fraction as Fr

MUTANTS = ('M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10')
MUT = None


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


# ------------------------------------------------------------------------------------- truncated power series in t
class TS:
    """Power series in t truncated after degree N (exact rationals)."""
    N = 3

    def __init__(self, c):
        c = [Fr(x) for x in c][:TS.N + 1]
        self.c = c + [Fr(0)] * (TS.N + 1 - len(c))

    def __add__(self, o):
        o = o if isinstance(o, TS) else TS([o])
        return TS([a + b for a, b in zip(self.c, o.c)])

    __radd__ = __add__

    def __neg__(self):
        return TS([-a for a in self.c])

    def __sub__(self, o):
        return self + (-(o if isinstance(o, TS) else TS([o])))

    def __rsub__(self, o):
        return TS([o]) - self

    def __mul__(self, o):
        o = o if isinstance(o, TS) else TS([o])
        out = [Fr(0)] * (TS.N + 1)
        for i, a in enumerate(self.c):
            for j, b in enumerate(o.c):
                if i + j <= TS.N:
                    out[i + j] += a * b
        return TS(out)

    __rmul__ = __mul__

    def inv(self):
        a0 = self.c[0]
        out = [Fr(1) / a0] + [Fr(0)] * TS.N
        for n in range(1, TS.N + 1):
            out[n] = -sum(self.c[j] * out[n - j] for j in range(1, n + 1)) / a0
        return TS(out)

    def __pow__(self, n):
        r = TS([1])
        for _ in range(n):
            r = r * self
        return r


# ------------------------------------------------------------------------------------- S1: Theorem 1 algebra
def control_S1():
    ok = True
    const = Fr(9 * 5184 * 216, 144)                       # (9 gamma^4/144) * 5184 kappa^2 * 216 kappa gamma^2 / ...
    ok &= const == 69984
    c384 = Fr(69984, 72 ** 4) if MUT != 'M1' else Fr(69984, 72 ** 4) * Fr(385, 384)
    ok &= c384 == Fr(1, 384)
    # int_{1/3}^1 (phi^-4 - phi^-2) dphi with the antiderivative -phi^-3/3 + phi^-1
    F = lambda p: -Fr(1, 3) / p ** 3 + 1 / p
    I0 = F(Fr(1)) - F(Fr(1, 3))
    ok &= I0 == Fr(20, 3)
    ok &= 12 * I0 / 384 == Fr(5, 24)
    Eg6 = 15 * Fr(2) ** 3
    ok &= Eg6 == 120 and Fr(5, 24) * Eg6 == 25
    # the soft window at f4 = 0: lambda = 3 gamma^2 / (72 kappa phi), phi in [1/3, 1)
    for g2, kap in ((Fr(2), Fr(7)), (Fr(5, 3), Fr(100))):
        lam = lambda phi: 3 * g2 / (72 * kap * phi)
        ok &= lam(Fr(1, 3)) == g2 / (8 * kap) and lam(Fr(1)) == g2 / (24 * kap)
    # the bound |f4/(72 kappa phi)| <= 1/24 on |f4| < kappa, phi >= 1/3
    ok &= Fr(1) / (72 * Fr(1, 3)) == Fr(1, 24)
    return ok, {'change_of_variables_constant': str(c384), 'phi_integral': str(I0), 'F0_over_pi0_pA0': str(Fr(5, 24) * Eg6)}


# ------------------------------------------------------------------------------------- S2: the soft model
def Gk(X, ze, g, lt, k, B, C3):
    return (2 * (X + Fr(1, 2)) ** 2 * (X - 1) + Fr(1, 2) * (X * X - Fr(1, 4)) * g * ze - Fr(1, 2) * lt * ze * ze
            + Fr(1, 2) * k * B * X * ze * ze + k * k * C3 * ze ** 3 / 6)


def Gn(X, z, phi, beta, chi):
    return 2 * (X + Fr(1, 2)) ** 2 * (X - 1) / (24 * phi) + Fr(1, 2) * (X * X - Fr(1, 4)) * z - Fr(1, 2) * (1 - beta * X) * z * z + chi * z ** 3 / 6


def d1(f, x, h):
    return (-f(x + 2 * h) + 8 * f(x + h) - 8 * f(x - h) + f(x - 2 * h)) / (12 * h)


def control_S2():
    ok = True
    rng = LCG(20261002)
    n = 0
    for _ in range(60):
        g = rng.rat(9, 7, True); lt = abs(rng.rat(9, 7, True)); k = rng.rat(5, 7); B = rng.rat(9, 5); C3 = rng.rat(9, 5)
        X = rng.rat(9, 4); ze = rng.rat(9, 4); h = Fr(1, 3)
        f = lambda x, y: Gk(x, y, g, lt, k, B, C3)
        GX = d1(lambda x: f(x, ze), X, h)
        GZ = d1(lambda y: f(X, y), ze, h)
        GXX = d1(lambda x: d1(lambda xx: f(xx, ze), x, h), X, h)
        GZZ = d1(lambda y: d1(lambda yy: f(X, yy), y, h), ze, h)
        GXZ = d1(lambda y: d1(lambda x: f(x, y), X, h), ze, h)
        ok &= GX == 6 * (X * X - Fr(1, 4)) + X * g * ze + k * B * ze * ze / 2
        ok &= GZ == (X * X - Fr(1, 4)) * g / 2 - lt * ze + k * B * X * ze + k * k * C3 * ze * ze / 2
        ok &= GXX == 12 * X + g * ze and GZZ == -lt + k * B * X + k * k * C3 * ze and GXZ == X * g + k * B * ze
        Y = 3 * k * B - g * g / 4
        detM = (-6) * (-lt - k * B / 2) - (g / 2) ** 2
        detS = 6 * (-lt + k * B / 2) - (g / 2) ** 2
        ok &= detM == 6 * lt + Y and detS == -6 * lt + Y
        ok &= f(Fr(-1, 2), Fr(0)) == 0 and f(Fr(1, 2), Fr(0)) == -1
        # normalization (2.2)-(2.3), gamma > 0 branch and the reflection for gamma < 0
        gg, CC, sgn = (g, C3, 1) if g > 0 else (-g, -C3, -1)
        phi = gg * gg / (24 * lt); beta = k * B / lt; chi0 = 576 * (k * k) * CC / gg ** 3
        if MUT == 'M8':
            chi0 = chi0 / 2
        chi = chi0 * phi * phi
        t = 12 * k * B / (gg * gg)
        ok &= beta == 2 * t * phi
        z = rng.rat(9, 4)
        ok &= f(X, sgn * gg / lt * z) == gg * gg / lt * Gn(X, z, phi, beta, chi)
        # weight and measure
        cp = 1 - t
        ok &= 36 * lt * lt - Y * Y == gg ** 4 / 16 * (1 / phi ** 2 - cp * cp)
        ok &= gg ** 2 / (24 * phi ** 2) * gg ** 4 / 16 == gg ** 6 / 384 / phi ** 2
        # typed window (2.4): |Y| < 6 lt  <=>  phi < 1/|c'|
        ok &= (abs(Y) < 6 * lt) == (cp == 0 or phi < 1 / abs(cp))
        n += 1
    return ok, n


# ------------------------------------------------------------------------------------- S3: Gaussian kernel covariances
def dfac(n):
    out = 1
    for j in range(n - 1, 0, -2):
        out *= j
    return out


def d0(n):
    return 0 if n % 2 else (-1) ** (n // 2) * dfac(n)


def cov(a, b):
    return Fr((-1) ** (b[0] + b[1]) * d0(a[0] + b[0]) * d0(a[1] + b[1]))


def control_S3():
    ok = True
    first = [(1, 0), (0, 1)]
    third = [(3, 0), (2, 1), (1, 2), (0, 3)]                # f_uuu, gamma = f_uuT, B = f_uTT, C3 = f_TTT
    S11 = [[cov(a, b) for b in first] for a in first]
    ok &= S11 == [[1, 0], [0, 1]]
    C = [[cov(a, b) - sum(cov(a, first[i]) * cov(first[i], b) / S11[i][i] for i in range(2)) for b in third] for a in third]
    target = [[6, 0, 0, 0], [0, 2, 0, 0], [0, 0, 2, 0], [0, 0, 0, 6]]
    if MUT == 'M2':
        target[2][2] = 3
    ok &= C == [[Fr(x) for x in row] for row in target]
    even = [(0, 0), (2, 0), (1, 1), (0, 2), (4, 0), (2, 2), (0, 4)]
    ok &= all(cov(e, o) == 0 for e in even for o in third + first)
    var3 = C[0][0]
    ok &= Fr(144) / (2 * var3) == 12                         # exp(-(12k)^2/(2*6)) = exp(-12 k^2)
    return ok, {'conditional_covariance_third_jets': [[str(x) for x in row] for row in C], 'pin_exponent_a_prime': str(Fr(144) / (2 * var3))}


# ------------------------------------------------------------------------------------- S4, S5: the edge (3.3) and I(t, 0) (3.4)
def ridge_series(Xs, Ps, t):
    beta = 2 * t * Ps
    p = Xs * Xs - Fr(1, 4)
    a = 1 - beta * Xs
    g = 2 * (Xs + Fr(1, 2)) ** 2 * (Xs - 1) + 3 * Ps * p * p * a.inv()
    # derivative in X of the same expression at fixed phi, beta: d/dX[2(X+1/2)^2(X-1)] = 6(X^2 - 1/4),
    # d/dX[p^2/a] = (4 X p a + beta p^2)/a^2
    gx = 6 * p + 3 * Ps * (4 * Xs * p * a + beta * p * p) * (a * a).inv()
    return g, gx


def control_S4():
    ok = True
    t = TS([0, 1])
    p2 = Fr(10, 27) if MUT != 'M3' else Fr(1, 3)
    Xs = TS([Fr(-3, 2), Fr(-1, 3), Fr(-1, 3)])
    Ps = TS([Fr(1, 3), Fr(1, 3), p2])
    g, gx = ridge_series(Xs, Ps, t)
    ok &= (g + 1).c[:3] == [0, 0, 0] and gx.c[:3] == [0, 0, 0]
    # t = 0: g + 1 = ((X - 1/2)(X + 3/2))^2 at phi = 1/3 (identity at rational points)
    for X in (Fr(-7, 3), Fr(-3, 2), Fr(1, 5), Fr(9, 4)):
        ok &= 2 * (X + Fr(1, 2)) ** 2 * (X - 1) + (X * X - Fr(1, 4)) ** 2 + 1 == ((X - Fr(1, 2)) * (X + Fr(3, 2))) ** 2
    # Jacobian of (g + 1, g_X) in (X, phi) at (-3/2, 1/3, t = 0): [[g_X, g_phi], [g_XX, g_Xphi]] = [[0, 12], [g_XX, -36]]
    X0 = Fr(-3, 2)
    gphi = 3 * (X0 * X0 - Fr(1, 4)) ** 2
    gXX = 12 * X0 + Fr(1, 3) * 3 * (12 * X0 * X0 - 1)          # d2/dX2 [2(X+1/2)^2(X-1) + 3 phi (X^2-1/4)^2] at phi = 1/3
    gXphi = 3 * 4 * X0 * (X0 * X0 - Fr(1, 4))
    jac = 0 * gXphi - gphi * gXX
    ok &= gphi == 12 and gXX == 8 and jac != 0
    return ok, {'X_e': ['-3/2', '-1/3', '-1/3'], 'phi_e': ['1/3', '1/3', str(p2)], 'jacobian': str(jac)}


def control_S5():
    ok = True
    t = TS([0, 1])
    pe = TS([Fr(1, 3), Fr(1, 3), Fr(10, 27)])
    cp = 1 - t if MUT != 'M4' else 1 + t
    I = Fr(1, 3) * (pe.inv() ** 3) - cp * cp * pe.inv() + Fr(2, 3) * cp ** 3
    ok &= I.c[:3] == [Fr(20, 3), Fr(-20), Fr(52, 3)]
    # the general antiderivative: int_a^b phi^-2 (phi^-2 - c^2) = (a^-3 - b^-3)/3 - c^2 (a^-1 - b^-1), b = 1/c
    for a, c in ((Fr(1, 3), Fr(1)), (Fr(2, 7), Fr(5, 4))):
        b = 1 / c
        lhs = (a ** -3 - b ** -3) / 3 - c * c * (1 / a - 1 / b)
        ok &= lhs == a ** -3 / 3 - c * c / a + Fr(2, 3) * c ** 3
    return ok, {'I_t_series': [str(x) for x in I.c[:3]]}


# ------------------------------------------------------------------------------------- S6: Proposition 4 constants
def control_S6():
    ok = True
    m = lambda n, s2: dfac(n) * Fr(s2) ** (n // 2) if n % 2 == 0 else Fr(0)       # E X^n, X ~ N(0, s2)
    EB2, Eg2, Eg6 = m(2, 2), m(2, 2), m(6, 2)
    ok &= Eg6 == 120 and EB2 == 2 and Eg2 == 2
    Eg6t2 = 144 * EB2 * Eg2 if MUT != 'M9' else 144 * EB2 * Eg2 * Fr(3, 2)   # gamma^6 t^2 = 144 k^2 B^2 gamma^2
    ok &= Eg6t2 == 576
    h2 = Fr(52, 3) * Eg6t2 / (Eg6 * Fr(20, 3))
    ok &= h2 == Fr(312, 25) and h2 - 12 == Fr(12, 25)
    # pointwise identities at rational (k, B, C3, gamma)
    rng = LCG(7)
    for _ in range(20):
        k, B, C3, g = rng.rat(5, 3), rng.rat(5, 3), rng.rat(5, 3), rng.rat(5, 3, True)
        t = 12 * k * B / (g * g); c0 = 576 * k * k * C3 / g ** 3
        ok &= g ** 6 * abs(t) ** 3 == 1728 * abs(k) ** 3 * abs(B) ** 3 and g ** 6 * c0 ** 2 == 331776 * k ** 4 * C3 ** 2
        ok &= g ** 6 * abs(t) * abs(c0) == 6912 * abs(k) ** 3 * abs(B) * abs(C3) * abs(g)
    return ok, {'h2': str(h2), 'H_k2_coefficient': str(h2 - 12)}


# ------------------------------------------------------------------------------------- S7: Lemma 3
def control_S7():
    ok = True
    phimax = Fr(1, 20) if MUT != 'M5' else Fr(1, 5)
    betamax, chimax = Fr(1, 10), Fr(1, 400)
    # |beta| = 2|t| phi <= 1/10 when phi <= |t|^-1/20; |chi| = |chi0| phi^2 <= 1/400; chi^2 <= phi/8000
    ok &= 2 * Fr(1, 20) == betamax and Fr(1, 20) ** 2 == chimax
    ok &= Fr(1, 20) ** 3 * 8000 == 1                         # phi^3 <= |chi0|^-2/8000  =>  chi^2 = chi0^2 phi^4 <= phi/8000
    # a = 1 - beta X on [-2, 1/2] lies in [4/5, 6/5]; on [-1/2, 1/2] in [19/20, 21/20]
    ok &= 1 - betamax * 2 == Fr(4, 5) and 1 + betamax * 2 == Fr(6, 5) and 1 - betamax / 2 == Fr(19, 20)
    # D > 0 on [-2, 1/2]: a^2 - |chi| |p| >= 16/25 - (1/400)(15/4) > 0
    ok &= Fr(16, 25) - chimax * Fr(15, 4) > 0
    # s/a in [0.99, 1.01]: |chi p| / a^2 <= (1/400)(15/4)/(16/25) = 375/25600 < 1/64
    ok &= chimax * Fr(15, 4) / Fr(16, 25) <= Fr(1, 64)
    ok &= Fr(99, 100) ** 2 <= 1 - Fr(1, 64) and Fr(101, 100) ** 2 >= 1 + Fr(1, 64)
    # critical values of h(z) = p z/2 - a z^2/2 + chi z^3/6 at z_r = p/(a+s), z_v = (a+s)/chi, s^2 = a^2 - chi p
    rng = LCG(11)
    for _ in range(30):
        a, s, chi = rng.rat(9, 5, True), rng.rat(9, 5, True), rng.rat(9, 5, True)
        p = (a * a - s * s) / chi
        h = lambda z: p * z / 2 - a * z * z / 2 + chi * z ** 3 / 6
        ok &= h(p / (a + s)) == p * p * (a + 2 * s) / (6 * (a + s) ** 2) if a + s != 0 else True
        ok &= h((a + s) / chi) == (a + s) ** 2 * (a - 2 * s) / (6 * chi * chi)
    # R - A0 <= p^2 (a + 2s)/(6 (a + s)^2) <= (a + 2.02 a)/(6 (1.99 a)^2) p^2 = c_R p^2 / a with c_R <= 0.128
    cR = (1 + Fr(202, 100)) / (6 * Fr(199, 100) ** 2)
    ok &= cR <= Fr(128, 1000)
    # left dip at X = -2: p = 15/4, a >= 4/5: R - A0 <= cR (225/16)/(4/5) <= 2.3; A0(-2) = 13.5 L_S; 12.5/(24 phi) > 2.3
    ok &= cR * Fr(225, 16) / Fr(4, 5) <= Fr(23, 10)
    ok &= 2 * Fr(9, 4) * (-3) == Fr(-27, 2)
    ok &= Fr(25, 2) / (24 * phimax) > Fr(23, 10)
    # on [-2, -1/2): bracket 2(X - 1)/(24 phi) + (cR/a)(X - 1/2)^2 <= -1/(8 phi) + (cR/(4/5)) (25/4) < 0
    ok &= -1 / (8 * phimax) + cR / Fr(4, 5) * Fr(25, 4) < 0 and -1 / (8 * Fr(1, 20)) == Fr(-5, 2)
    # middle (-1/2, 1/2): 2(X - 1) <= -1 and (X - 1/2)^2 <= 1: bracket <= -1/(24 phi) + cR/(19/20) < 0
    ok &= -1 / (24 * phimax) + cR / Fr(19, 20) < 0
    # valley: (a + s)^2 (2s - a) >= (1.99 a)^2 (0.98 a) >= 3.88 * 0.512 = 1.98 -> V - A0 <= -0.33/chi^2; vs L_S: chi^2 < 7.92 phi
    low = Fr(199, 100) ** 2 * Fr(98, 100) * Fr(4, 5) ** 3
    ok &= low >= Fr(198, 100) and low / 6 >= Fr(33, 100)
    ok &= Fr(33, 100) * 24 > Fr(1, 8000)                      # 0.33/chi^2 > 1/(24 phi) when chi^2 <= phi/8000
    # the resulting bound: I <= int_{phi*}^inf phi^-4 = phi*^-3/3 = (20^3/3) max(1, |t|^3, chi0^2)
    ok &= Fr(20) ** 3 / 3 == Fr(8000, 3)
    return ok, {'phi_star_factor': str(phimax), 'c_R': str(cR), 'I_bound_constant': '8000/3'}


# ------------------------------------------------------------------------------------- S8: Lemma 2 (floating point)
def slice_vals(X, phi, beta, chi):
    """(open, R, V) of z -> G(X, z) for the normalized model (2.3)."""
    p = X * X - 0.25
    a = 1.0 - beta * X
    A0 = 2 * (X + 0.5) ** 2 * (X - 1) / (24 * phi)
    if chi == 0.0:
        if a <= 0:
            return True, None, None
        return False, A0 + p * p / (8 * a), -math.inf
    D = a * a - chi * p
    if D <= 0:
        return True, None, None
    s = math.sqrt(D)
    # stable roots of (chi/2) z^2 - a z + p/2 = 0 (product p/chi): no cancellation in either branch
    if a >= 0:
        zr = p / (a + s); zv = (a + s) / chi
    else:
        zr = (a - s) / chi; zv = p / (a - s)
    crit = lambda z: A0 + p * z / 3 - a * z * z / 6             # the value of G at a critical point of the slice
    R = crit(zr)
    V = crit(zv) if MUT != 'M6' else -math.inf
    return False, R, V


def decide(phi, beta, chi, n_mid=2001, n_side=6000, Xside=40.0):
    """Lemma 2: 1 = elder, 0 = rejected."""
    LS = -1.0 / (24 * phi)
    aS = 1 - beta / 2
    if aS <= 0 and chi == 0.0:
        return 0                                              # the ridge blows up at X = 1/beta < 1/2
    q = (Xside - 0.5) / 1e-6
    side = [1e-6 * q ** (i / (n_side - 1)) for i in range(n_side)]
    mid = [-0.5 + i / (n_mid - 1) for i in range(1, n_mid - 1)]

    def walk(xs, at_half_is_S):
        """Follow M's ridge interval along xs: 'closed' at the first X with R <= L_S, 'trigger' or 'open-ended'."""
        for X in xs:
            op, R, V = slice_vals(X, phi, beta, chi)
            if op:
                return 'trigger', X
            if R <= LS:
                return 'closed', X
            if R > 0:
                return 'trigger', X
            if V > LS and not (at_half_is_S and abs(X - 0.5) < 2e-3):
                return 'trigger', X
        return 'open-ended', None

    if aS > 0:                                                # S on the ridge: M's interval must reach S
        st, X = walk(mid, False)
        if st == 'trigger' or (st == 'closed' and X < 0.5 - 1e-3):
            return 0
    else:                                                     # S is the valley point at X = 1/2: the interval must contain 1/2
        st, X = walk(mid + [0.5] + [0.5 + d for d in side], True)
        if st != 'closed' or X <= 0.5:
            return 0
    st, X = walk([-0.5 - d for d in side], False)
    return 1 if st == 'closed' else 0


def control_S8():
    cases = [((0.30, 0.0, 0.0), 1), ((0.36, 0.0, 0.0), 0), ((0.3333, 0.0, 0.0), 1), ((0.3334, 0.0, 0.0), 0),
             ((0.95, 0.0, 0.0), 0), ((0.5, 2.2, 0.0), 0), ((0.04, 0.09, 0.002), 1),
             ((0.30, 0.0, 3.0), 0), ((0.20, 0.0, 1.0), 0), ((0.20, 0.0, 0.5), 1), ((0.05, 0.0, 0.5), 1),
             ((0.05, 0.0, 0.85), 0), ((0.03, -0.1, 0.0), 1),
             ((0.2401, 2.1425, 0.5536), 1), ((0.6267, 2.3645, 2.8796), 1), ((0.5, 2.2, 0.01), 0)]
    # (0.05, 0, chi): the valley at M reaches L_S when chi^2 = 16 phi = 0.8, chi = 0.894, and slightly left of M earlier;
    # (0.2, 0, 1): the slice opens (D = 0) at p = 1 before the left ridge falls below L_S
    res = [decide(*c) for c, _ in cases]
    ok = all(r == e for r, (_, e) in zip(res, cases))
    return ok, {'cases': [[list(c), e, r] for (c, e), r in zip(cases, res)]}


# ------------------------------------------------------------------------------------- S9: Lemma 5 bookkeeping
def control_S9():
    ok = True
    e1 = 4 + Fr(-13, 4) if MUT != 'M7' else 4 + Fr(-12, 4)     # l^4 * l^(-13/4): r > l^(1/4), kappa^2 * k^2
    e2 = Fr(2, 3) + Fr(1, 12)                                 # l^(2/3) * l^(1/12): the tail of I~ beyond u = l^(-1/12)
    e3 = Fr(8, 3) - 2 + Fr(1, 3) - Fr(3, 12)                  # l^(8/3 - 2 + 1/3) * l^(-3/12): the O(kappa^-2) part
    ok &= e1 == e2 == e3 == Fr(3, 4)
    # int_{l^(1/4)}^inf r^-14 dr = l^(-13/4)/13 ; the integrand of I~: u^4 * u^-6 = u^-2 at infinity, u^4 at 0
    ok &= Fr(-14) + 1 == -13 and 4 - 6 == -2
    ok &= Fr(3, 4) > Fr(2, 3) > Fr(1, 4)
    return ok, {'error_exponents': [str(e1), str(e2), str(e3)]}



# ------------------------------------------------------------------------------------- S10: the limit (2.1)
FACT = [1, 1, 2, 6, 24, 120, 720, 5040]


def solve(M, v):
    """Exact Gaussian elimination."""
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


def control_S10():
    """Exactly pinned degree-6 fields with A = -lt r/k: (f(rX, rk zeta) - b)/(k r^3) = G_k + r G1 + O(r^2), with
    G1 = (f4/(24k))(X^2 - 1/4)^2 + (k/4) c22 X^2 zeta^2 + (k^2/6) c13 X zeta^3 + (k^3/24) c04 zeta^4 + (1/6) c31 X (X^2 - 1/4) zeta."""
    ok = True
    rng = LCG(240)
    pinned = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1)]
    mono = [(i, n - i) for n in range(7) for i in range(n, -1, -1)]
    worst = Fr(0)
    for trial in range(3):
        k = Fr(1 + rng.nxt() % 4, 1 + rng.nxt() % 3); lt = Fr(1 + rng.nxt() % 5, 1 + rng.nxt() % 4); b = rng.rat(3, 2)
        free = {m: rng.rat(5, 3) for m in mono if m not in pinned}
        errs = []
        for r in (Fr(1, 10 ** 3), Fr(1, 10 ** 4)):
            c = dict(free); c[(0, 2)] = -lt * r / k
            def val(cc, x, y, dx=0, dy=0):
                out = Fr(0)
                for (i, j), v in cc.items():
                    if i >= dx and j >= dy:
                        out += v * x ** (i - dx) * y ** (j - dy) / (FACT[i - dx] * FACT[j - dy])
                return out
            rows, rhs = [], []
            for (x, target, kind) in ((-r / 2, b, 'f'), (r / 2, b - k * r ** 3, 'f'), (-r / 2, 0, 'fx'), (r / 2, 0, 'fx'),
                                      (-r / 2, 0, 'fy'), (r / 2, 0, 'fy')):
                dx, dy = {'f': (0, 0), 'fx': (1, 0), 'fy': (0, 1)}[kind]
                rows.append([val({m: Fr(1)}, x, Fr(0), dx, dy) for m in pinned])
                rhs.append(target - val(c, x, Fr(0), dx, dy))
            sol = solve(rows, rhs)
            for m, v in zip(pinned, sol):
                c[m] = v
            g, B, C3, f4 = c[(2, 1)], c[(1, 2)], c[(0, 3)], c[(4, 0)]
            e = []
            for X, ze in ((Fr(-3, 2), Fr(1, 3)), (Fr(-1, 2), Fr(2)), (Fr(1, 3), Fr(-1)), (Fr(2), Fr(1, 2))):
                F = (val(c, r * X, r * k * ze) - b) / (k * r ** 3)
                C3m = C3 if MUT != 'M10' else 0
                G = Gk(X, ze, g, lt, k, B, C3m)
                p4 = (X * X - Fr(1, 4))
                G1 = (f4 / (24 * k) * p4 ** 2 + k / 4 * c[(2, 2)] * X * X * ze * ze + k * k / 6 * c[(1, 3)] * X * ze ** 3
                      + k ** 3 / 24 * c[(0, 4)] * ze ** 4 + c[(3, 1)] / 6 * X * p4 * ze)
                e.append(abs((F - G) / r - G1))
            errs.append(max(e))
        # O(r^2) remainder: the r^1-corrected error must scale like r (factor 10 between r = 1e-3 and 1e-4)
        ok &= errs[1] * 5 <= errs[0] and errs[1] <= Fr(1, 10)
        worst = max(worst, errs[1])
    return ok, {'fields': 3, 'max_error_after_r1_term_at_r_1e-4': str(float(worst))}


def main(argv):
    global MUT
    if len(argv) == 2 and argv[0] == '--mutant':
        if argv[1] not in MUTANTS:
            print('unknown mutant label', file=sys.stderr)
            return 2
        MUT = argv[1]
    elif argv:
        print('usage: soft_check.py [--mutant M1..M10]', file=sys.stderr)
        return 2
    s1, s1d = control_S1()
    s2, n2 = control_S2()
    s3, s3d = control_S3()
    s4, s4d = control_S4()
    s5, s5d = control_S5()
    s6, s6d = control_S6()
    s7, s7d = control_S7()
    s8, s8d = control_S8()
    s9, s9d = control_S9()
    s10, s10d = control_S10()
    res = {'object': 'CL-SOFT-REJECTED-20261002-v1', 'scientific_effect': 'NONE',
           'controls': {'S1_theorem_S': s1, 'S2_model_algebra': s2, 'S3_gaussian_kernel_jets': s3, 'S4_elder_edge': s4,
                        'S5_I_series': s5, 'S6_proposition_H': s6, 'S7_lemma_B': s7, 'S8_lemma_D_cases': s8,
                        'S9_lemma_M': s9, 'S10_limit_field': s10},
           'S1': s1d, 'S2_instances': n2, 'S3': s3d, 'S4': s4d, 'S5': s5d, 'S6': s6d, 'S7': s7d, 'S8': s8d, 'S9': s9d, 'S10': s10d}
    ok = all(res['controls'].values())
    if MUT is None:
        print(json.dumps(res, indent=1, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
