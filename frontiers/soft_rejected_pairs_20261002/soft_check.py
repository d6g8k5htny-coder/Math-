#!/usr/bin/env python3
"""Exact controls for CL-SOFT-REJECTED-20261002-v1.2 (Theorem 1, Corollary 1', Lemmas 2, 3 and 5, Propositions 2' and 4;
PROOF.md).

Standard library only; exact rationals except control S8 (a deterministic floating-point implementation of Lemma 2 on
fixed cases). Output: RESULTS.json (sorted keys), byte-identical under -O. Usage:
    python3 -B -S soft_check.py                 # exit 0, prints RESULTS.json
    python3 -B -S soft_check.py --mutant M3     # exit 1 (only its control fails; M1..M14)
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
  S11 Theorem 1 in every d (m = d - 1 = 2, 3; rational eigenframes from Cayley rotations): z = f4 - 3 g^T A^{-1} g =
      3 g1^2/l1 + f4~, Y = (Delta/12) z, w = 36 kappa^2 Delta^2 (1 - phi^2), the substitution (1.1) with the factor
      Pi' = (l2...lm)^2, 69984/72^4 = 1/384, and the double-soft implication 3 sum_{i>=2} g_i^2/l_i >= kappa/2 =>
      l2 <= 6|g|^2/kappa
  S12 the Gaussian kernel in d = 3 (Hermite numbers in three coordinates): A = -b I + GOE and f4 ~ N(-3b, 24) given the
      even pins; the b-integrated law (t ~ N(0, 5/3), f4 | t ~ N(6t/5, 138/5); d = 2: [[8/3, 2], [2, 30]]); the odd
      jets along e = (3/5, 4/5) with variances (6, 2, 2, 6); the prefactor p_G(0) p_{V_u}(0) (2 pi)^{-1/2} tau_u^{-1} =
      (2 pi)^{-d}/(6 sqrt pi) from the exact covariances of grad f, V_u and tau_u; Corollary 1': 25 sqrt3/(48 pi^2) and
      125 sqrt30/(192 pi^3), in exact arithmetic of the form q pi^(e/2) sqrt(r) (floating-point values printed only)
  S13 Proposition 2': on two exactly pinned degree-6 fields in d = 3 with A = diag(-lt r/k, mu) at 0,
      (f(rX, rk zeta, r^(3/2) eta) - b)/(k r^3) = G_k + (mu/2k) eta^2 + r^(1/2) G_half + O(r), at r = 1e-6 and 1e-8
  S14 Lemma 2's exact (D') witness (OpenAI Codex, #242 comment 5946792240): G_(3/2,8/3,20/3)(X, z) =
      (1/9) G_(1/6,0,0)(X + 2z, 3z) on a 4 x 4 rational grid (unisolvent for bidegree <= (3, 3), hence an identity); the
      witness is typed with beta > 2, chi > 0; G_(1/6,0,0) has gradient zero at (+-1/2, 0) and (-3, 35/8), and
      d_X G(X, p/2) = (X^2 - 1/4)(3/2 + X/2) (so these are all its critical points); the witness's critical values
      0, -1/36 = L_S, -125/384; and the (D) certificate at (1/6, 0, 0): R = (X + 1/2)^2 (X^2 + 3X - 15/4)/8 < 0 off -1/2 on
      [-2, 1/2] (convexity, endpoint signs), R - L_S = (X - 1/2)^2 (X^2 + 5X + 17/4)/8 at six points (quartic identity),
      and the edge factor changes sign once on (-2, -1); and, for beta > 2, chi < 0 (rejected by Lemma 2), the slice at
      X = 1/beta is open: a = 0 and D = -chi p < 0, on three typed rational points
"""
import json
import math
import sys
from fractions import Fraction as Fr

MUTANTS = ('M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12', 'M13', 'M14')
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


# ------------------------------------------------------------------------------------- S11: Theorem 1 in every d (algebra)
def mmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def mT(A):
    return [list(r) for r in zip(*A)]


def minv(A):
    n = len(A)
    M = [list(A[i]) + [Fr(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        piv = next(i for i in range(c, n) if M[i][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        M[c] = [x / M[c][c] for x in M[c]]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return [row[n:] for row in M]


def mdet(A):
    n = len(A)
    M = [list(r) for r in A]
    d = Fr(1)
    for c in range(n):
        piv = next((i for i in range(c, n) if M[i][c] != 0), None)
        if piv is None:
            return Fr(0)
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            d = -d
        d *= M[c][c]
        for i in range(c + 1, n):
            f = M[i][c] / M[c][c]
            M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return d


def cayley(K):
    """Rational orthogonal matrix (I - K)^{-1}(I + K) for skew K."""
    n = len(K)
    I = [[Fr(int(i == j)) for j in range(n)] for i in range(n)]
    return mmul(minv([[I[i][j] - K[i][j] for j in range(n)] for i in range(n)]), [[I[i][j] + K[i][j] for j in range(n)] for i in range(n)])


def control_S11():
    """Theorem 1 for m = d - 1 = 2, 3: in the eigenframe of Lambda = -A, z = f4 - 3 g^T A^{-1} g = 3 g1^2/l1 + f4~,
    Y = (Delta/12) z, w = 36 kappa^2 Delta^2 (1 - phi^2); the soft-window substitution with the factor l2^2...lm^2;
    and the double-soft implication 3 sum_{i>=2} g_i^2/l_i >= kappa/2  =>  l2 <= 6 |g|^2/kappa."""
    ok = True
    rng = LCG(31011)
    n = 0
    for m in (2, 3, 2, 3, 2, 3, 2, 3):
        K = [[Fr(0)] * m for _ in range(m)]
        for i in range(m):
            for j in range(i + 1, m):
                K[i][j] = rng.rat(5, 4); K[j][i] = -K[i][j]
        O = cayley(K)
        ok &= mmul(mT(O), O) == [[Fr(int(i == j)) for j in range(m)] for i in range(m)]
        lam = sorted({abs(rng.rat(9, 7, True)) for _ in range(m + 3)})[:m]
        if len(lam) < m:
            continue
        Lam = mmul(mmul(O, [[lam[i] if i == j else Fr(0) for j in range(m)] for i in range(m)]), mT(O))
        A = [[-x for x in row] for row in Lam]
        g = [rng.rat(9, 4) for _ in range(m)]
        f4 = rng.rat(19, 3); kap = abs(rng.rat(40, 3, True))
        gi = [sum(O[k][i] * g[k] for k in range(m)) for i in range(m)]          # g_i = g . e_i, e_i = O[:, i]
        Ainv = minv(A)
        q = -sum(g[i] * Ainv[i][j] * g[j] for i in range(m) for j in range(m))
        ok &= q == sum(gi[i] ** 2 / lam[i] for i in range(m))
        Delta = mdet(A)
        prod = Fr(1)
        for x in lam:
            prod *= x
        ok &= Delta == (-1) ** m * prod
        adj = [[Delta * x for x in row] for row in Ainv] if MUT != 'M11' else Ainv
        Y = f4 / 12 * Delta - sum(g[i] * adj[i][j] * g[j] for i in range(m) for j in range(m)) / 4
        z = f4 + 3 * q
        ok &= Y == Delta / 12 * z
        phi = z / (72 * kap)
        ok &= 36 * kap ** 2 * Delta ** 2 - Y * Y == 36 * kap ** 2 * Delta ** 2 * (1 - phi * phi)
        # the substitution: f4~ = f4 + 3 sum_{i>=2} g_i^2/l_i, l1(phi) = 3 g1^2/(72 kappa phi - f4~)
        f4t = f4 + 3 * sum(gi[i] ** 2 / lam[i] for i in range(1, m))
        Pp = Fr(1)
        for x in lam[1:]:
            Pp *= x * x
        for ph in (Fr(1, 3), Fr(1, 2), Fr(5, 7), Fr(99, 100)):
            den = 72 * kap * ph - f4t
            if den <= 0 or gi[0] == 0:
                continue
            l1 = 3 * gi[0] ** 2 / den
            ok &= f4t + 3 * gi[0] ** 2 / l1 == 72 * kap * ph
            jac = 216 * kap * gi[0] ** 2 / den ** 2
            ok &= 36 * kap ** 2 * l1 ** 2 * Pp * (1 - ph * ph) * jac == 69984 * kap ** 3 * gi[0] ** 6 * Pp * (1 - ph * ph) / den ** 4
        # double-soft implication
        if 3 * sum(gi[i] ** 2 / lam[i] for i in range(1, m)) >= kap / 2:
            ok &= lam[1] <= 6 * sum(x * x for x in g) / kap
        n += 1
    ok &= Fr(69984, 72 ** 4) == Fr(1, 384)
    return ok, {'instances': n}


# ------------------------------------------------------------------------------------- S12: the Gaussian kernel in d = 3
def cov3(a, b):
    out = Fr((-1) ** sum(b))
    for x, y in zip(a, b):
        out *= d0(x + y)
    return out


def covL(J1, J2):
    return sum(c1 * c2 * cov3(a, b) for a, c1 in J1.items() for b, c2 in J2.items())


def directional(order_u, e, n_e):
    """d_u^order_u d_e^n_e f for e = (e1, e2) in the transverse plane, as {multi-index (u, 1, 2): coefficient}."""
    out = {}
    for j in range(n_e + 1):
        c = Fr(math.comb(n_e, j)) * e[0] ** (n_e - j) * e[1] ** j
        key = (order_u, n_e - j, j)
        out[key] = out.get(key, Fr(0)) + c
    return out


def condition(Xs, Ps):
    """Conditional covariance of the jets Xs given Ps (lists of linear combinations), and regression coefficients."""
    SPP = [[covL(p, q) for q in Ps] for p in Ps]
    Pinv = minv(SPP)
    SXP = [[covL(x, p) for p in Ps] for x in Xs]
    coef = mmul(SXP, Pinv)
    C = [[covL(x, y) - sum(coef[i][k] * SXP[j][k] for k in range(len(Ps))) for j, y in enumerate(Xs)] for i, x in enumerate(Xs)]
    return C, coef


class Sym:
    """q * pi^(e/2) * sqrt(r), q and r rational, r squarefree-normalized lazily (comparison by square)."""
    def __init__(self, q, e, r):
        self.q, self.e, self.r = Fr(q), e, Fr(r)

    def __mul__(self, o):
        return Sym(self.q * o.q, self.e + o.e, self.r * o.r)

    def same(self, o):
        return self.e == o.e and self.q * self.q * self.r == o.q * o.q * o.r and (self.q >= 0) == (o.q >= 0)

    def value(self):
        return float(self.q) * math.pi ** (self.e / 2) * math.sqrt(float(self.r))


def control_S12():
    """The Gaussian kernel exp(-|x|^2/2) in d = 3, coordinates (u, theta_1, theta_2):
    (i) given (f, f_uu, f_u1, f_u2) = (b, 0, 0, 0): A = -b I + G with Var G_11 = Var G_22 = 2, Cov = 0, Var G_12 = 1
        (GOE), and f4 = -3b + N(0, 24) independent of A;
    (ii) b-integrated (f free): t = tr A/2 ~ N(0, 5/3), the traceless part has variance 1 per coordinate, and
        f4 | A ~ N((6/5) t, 138/5); d = 2: (f_TT, f4) ~ N(0, [[8/3, 2], [2, 30]]);
    (iii) given grad f = 0, along e = (3/5, 4/5): (f_uuu, gamma_e, B_ee, C_eee) are independent with variances
        (6, 2, 2, 6), as in d = 2 (rotation invariance), so the pin factor exp(-12 k^2) and H are unchanged;
    (iv) the constants int int F0 db dsigma = 25 K_d d_int: d = 2: 25 sqrt3/(48 pi^2), d = 3: 125 sqrt30/(192 pi^3)."""
    ok = True
    f, fuu = {(0, 0, 0): Fr(1)}, {(2, 0, 0): Fr(1)}
    fu1, fu2 = {(1, 1, 0): Fr(1)}, {(1, 0, 1): Fr(1)}
    A11, A22, A12, f4 = {(0, 2, 0): Fr(1)}, {(0, 0, 2): Fr(1)}, {(0, 1, 1): Fr(1)}, {(4, 0, 0): Fr(1)}
    C, coef = condition([A11, A22, A12, f4], [f, fuu, fu1, fu2])
    target = [[2, 0, 0, 0], [0, 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 24]]
    if MUT == 'M12':
        target[2][2] = 2
    ok &= C == [[Fr(x) for x in row] for row in target]
    ok &= [row[0] for row in coef] == [-1, -1, 0, -3]                    # mean coefficients on b
    t = {(0, 2, 0): Fr(1, 2), (0, 0, 2): Fr(1, 2)}
    h = {(0, 2, 0): Fr(1, 2), (0, 0, 2): Fr(-1, 2)}
    C2, _ = condition([t, h, A12, f4], [fuu, fu1, fu2])
    ok &= C2 == [[Fr(5, 3), 0, 0, 2], [0, 1, 0, 0], [0, 0, 1, 0], [2, 0, 0, 30]]
    reg = C2[0][3] / C2[0][0]; var = C2[3][3] - C2[0][3] ** 2 / C2[0][0]
    ok &= reg == Fr(6, 5) and var == Fr(138, 5)
    C1, _ = condition([A11, f4], [fuu, fu1])                          # d = 2 (theta_2 absent: its jets are uncorrelated)
    ok &= C1 == [[Fr(8, 3), 2], [2, 30]]
    e = (Fr(3, 5), Fr(4, 5))
    odd = [directional(3, e, 0), directional(2, e, 1), directional(1, e, 2), directional(0, e, 3)]
    grad = [{(1, 0, 0): Fr(1)}, {(0, 1, 0): Fr(1)}, {(0, 0, 1): Fr(1)}]
    C3, _ = condition(odd, grad)
    ok &= C3 == [[Fr(x) for x in row] for row in ([6, 0, 0, 0], [0, 2, 0, 0], [0, 0, 2, 0], [0, 0, 0, 6])]
    ok &= all(covL(o, ev) == 0 for o in odd for ev in (f, fuu, fu1, fu2, A11, A22, A12, f4))
    # (iv) the prefactor of #207's parity factorization, p_G(0) p_{V_u}(0) (2 pi)^{-1/2} tau_u^{-1}, from the exact
    # covariances: grad f ~ N(0, I_d); V_u = (f_uu, f_u1, f_u2) with variances (3, 1, 1), uncorrelated; tau_u^2 = 6.
    Gd3 = [{(1, 0, 0): Fr(1)}, {(0, 1, 0): Fr(1)}, {(0, 0, 1): Fr(1)}]
    ok &= [[covL(x, y) for y in Gd3] for x in Gd3] == [[Fr(int(i == j)) for j in range(3)] for i in range(3)]
    Vu = [fuu, fu1, fu2]
    CV = [[covL(x, y) for y in Vu] for x in Vu]
    ok &= CV == [[3, 0, 0], [0, 1, 0], [0, 0, 1]]
    tau2 = C3[0][0]
    ok &= tau2 == 6

    def gauss0(variances):          # density at 0 of independent centred normals: (2 pi)^{-n/2} prod v^{-1/2}
        prod = Fr(1)
        for v in variances:
            prod *= v
        n = len(variances)
        return Sym(Fr(1), -n, 1 / (Fr(2) ** n * prod))   # pi^{-n/2} sqrt(2^{-n} / prod v)

    pref3 = gauss0([Fr(1)] * 3) * gauss0([CV[i][i] for i in range(3)]) * gauss0([tau2])
    pref2 = gauss0([Fr(1)] * 2) * gauss0([CV[0][0], CV[1][1]]) * gauss0([tau2])
    ok &= pref3.same(Sym(Fr(1, 48), -7, 1)) and pref2.same(Sym(Fr(1, 24), -5, 1))      # (2 pi)^{-d} / (6 sqrt pi)
    K3 = Sym(4, 2, 1) * pref3                                            # |S^2| = 4 pi
    K2 = Sym(2, 2, 1) * pref2                                            # |S^1| = 2 pi
    ok &= K3.same(Sym(Fr(1, 12), -5, 1)) and K2.same(Sym(Fr(1, 12), -3, 1))
    # the weighted densities: d = 2, the density of A ~ N(0, 8/3) at 0; d = 3, E[(2 rho)^2 p_t(-rho)] with t ~ N(0, 5/3),
    # rho ~ Rayleigh(1): 4 (2 pi 5/3)^{-1/2} int rho^3 exp(-(1/2 + 3/10) rho^2) d rho = (25/8) (10 pi/3)^{-1/2}
    vt = C2[0][0]
    a = Fr(1, 2) + 1 / (2 * vt)
    ok &= vt == Fr(5, 3) and a == Fr(4, 5) and 4 * (1 / (2 * a * a)) == Fr(25, 8)
    d2 = gauss0([C1[0][0]])                                              # (2 pi 8/3)^{-1/2}
    d3 = Sym(4 * (1 / (2 * a * a)), 0, 1) * gauss0([vt])                 # (25/8) (2 pi 5/3)^{-1/2}
    F2 = Sym(25, 0, 1) * K2 * d2
    F3 = Sym(25, 0, 1) * K3 * d3
    ok &= F2.same(Sym(Fr(25, 48), -4, 3)) and F3.same(Sym(Fr(125, 192), -6, 30))
    return ok, {'A_given_b_d3': [[str(x) for x in row] for row in C], 'b_integrated_t_h_A12_f4': [[str(x) for x in row] for row in C2],
                'f4_regression_on_t': str(reg), 'f4_residual_variance': str(var), 'odd_jets_along_e': [[str(x) for x in row] for row in C3],
                'int_F0_d2': '25 sqrt(3)/(48 pi^2) = %.10f' % F2.value(), 'int_F0_d3': '125 sqrt(30)/(192 pi^3) = %.10f' % F3.value()}


# ------------------------------------------------------------------------------------- S13: the stiff directions (d = 3)
def control_S13():
    """Exactly pinned degree-6 fields in (x, y, w) with A = diag(-lt r/k, mu) at 0 (the eigenframe): at the fold scale
    y = rk zeta, w = r^(3/2) eta,
        (f - b)/(k r^3) = G_k(X, zeta) + (mu/(2k)) eta^2 + r^(1/2) G_half + O(r),
        G_half = (c201/(2k))(X^2 - 1/4) eta + c111 X zeta eta + (k c021/2) zeta^2 eta,
    checked at r = 10^-6 and 10^-8 (so r^(1/2) is rational) in exact arithmetic."""
    ok = True
    rng = LCG(313)
    pinned = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (1, 0, 1)]
    mono = [(i, j, l) for n in range(7) for i in range(n + 1) for j in range(n + 1 - i) for l in [n - i - j]]
    worst = Fr(0)

    def val(cc, x, y, w, dx=0, dy=0, dw=0):
        out = Fr(0)
        for (i, j, l), v in cc.items():
            if i >= dx and j >= dy and l >= dw:
                out += v * x ** (i - dx) * y ** (j - dy) * w ** (l - dw) / (FACT[i - dx] * FACT[j - dy] * FACT[l - dw])
        return out
    for trial in range(2):
        k = Fr(1 + rng.nxt() % 4, 1 + rng.nxt() % 3); lt = Fr(1 + rng.nxt() % 5, 1 + rng.nxt() % 4); b = rng.rat(3, 2)
        mu = -Fr(1 + rng.nxt() % 5, 1 + rng.nxt() % 3)
        free = {mm: rng.rat(5, 3) for mm in mono if mm not in pinned}
        free[(0, 1, 1)] = Fr(0); free[(0, 0, 2)] = mu
        errs = []
        for sr in (Fr(1, 10 ** 3), Fr(1, 10 ** 4)):
            r = sr * sr
            c = dict(free); c[(0, 2, 0)] = -lt * r / k
            rows, rhs = [], []
            for (x, target, kind) in ((-r / 2, b, (0, 0, 0)), (r / 2, b - k * r ** 3, (0, 0, 0)), (-r / 2, 0, (1, 0, 0)),
                                      (r / 2, 0, (1, 0, 0)), (-r / 2, 0, (0, 1, 0)), (r / 2, 0, (0, 1, 0)),
                                      (-r / 2, 0, (0, 0, 1)), (r / 2, 0, (0, 0, 1))):
                rows.append([val({mm: Fr(1)}, x, Fr(0), Fr(0), *kind) for mm in pinned])
                rhs.append(target - val(c, x, Fr(0), Fr(0), *kind))
            for mm, v in zip(pinned, solve(rows, rhs)):
                c[mm] = v
            g, B, C3 = c[(2, 1, 0)], c[(1, 2, 0)], c[(0, 3, 0)]
            e = []
            for X, ze, et in ((Fr(-3, 2), Fr(1, 3), Fr(1, 2)), (Fr(-1, 2), Fr(2), Fr(-1)), (Fr(1, 3), Fr(-1), Fr(2)), (Fr(2), Fr(1, 2), Fr(1, 3))):
                F = (val(c, r * X, r * k * ze, r * sr * et) - b) / (k * r ** 3)
                G = Gk(X, ze, g, lt, k, B, C3) + mu / (2 * k) * et * et
                Gh = (c[(2, 0, 1)] / (2 * k) * (X * X - Fr(1, 4)) * et + c[(1, 1, 1)] * X * ze * et + k * c[(0, 2, 1)] / 2 * ze * ze * et)
                if MUT == 'M13':
                    Gh = 0
                e.append(abs((F - G - sr * Gh) / r))
            errs.append(max(e))
        # remainder O(r): the scaled error stays bounded as r drops by 100
        ok &= errs[1] <= 2 * errs[0] + 1 and errs[1] <= 100
        worst = max(worst, errs[1])
    return ok, {'fields': 2, 'max_scaled_remainder_at_r_1e-8': str(float(worst))}


# ------------------------------------------------------------------------------------- S14: the exact (D') witness
def control_S14():
    ok = True
    H = Fr(1, 2)
    wit = (Fr(3, 2), Fr(8, 3), Fr(20, 3))
    base = (Fr(1, 6), Fr(0), Fr(0))
    scale = Fr(1, 9) if MUT != 'M14' else Fr(1, 8)
    grid = [Fr(j, 3) - 1 for j in range(4)]
    for X in grid:
        for z in grid:
            ok &= Gn(X, z, *wit) == scale * Gn(X + 2 * z, 3 * z, *base)
    phi, beta, chi = wit
    ok &= phi > 0 and abs(phi - beta / 2) < 1 and beta > 2 and chi > 0
    # critical points of G_(1/6,0,0): grad zero, and d_X G(X, p/2) = (X^2 - 1/4)(1/(4 phi) + X/2) with 1/(4 phi) = 3/2
    g = lambda X, z: Gn(X, z, *base)
    def grad(X, z):
        e = Fr(1, 10 ** 6)
        # exact derivatives of a cubic by the 4-point stencil (exact for degree <= 4)
        gx = (-g(X + 2 * e, z) + 8 * g(X + e, z) - 8 * g(X - e, z) + g(X - 2 * e, z)) / (12 * e)
        gz = (-g(X, z + 2 * e) + 8 * g(X, z + e) - 8 * g(X, z - e) + g(X, z - 2 * e)) / (12 * e)
        return gx, gz
    pts = [(-H, Fr(0)), (H, Fr(0)), (Fr(-3), Fr(35, 8))]
    for X, z in pts:
        ok &= grad(X, z) == (0, 0)
    for X in (Fr(-7, 2), Fr(-1), Fr(0), Fr(2, 3), Fr(5, 4)):
        p = X * X - Fr(1, 4)
        ok &= grad(X, p / 2)[0] == p * (Fr(3, 2) + X / 2)
        ok &= grad(X, p / 2)[1] == 0
    # the witness's critical points are the images under (X, z) -> (X - 2 z/3, z/3) of these, with values / 9
    vals = sorted(scale * g(X, z) for X, z in pts)
    ok &= vals == sorted([Fr(0), Fr(-1, 36), Fr(-125, 384)]) and Fr(-1, 24) / phi == Fr(-1, 36)
    for X, z in pts:
        Xw, zw = X - 2 * z / 3, z / 3
        ok &= Gn(Xw, zw, *wit) == scale * g(X, z)
    # the (D) certificate at (1/6, 0, 0): concave slices, R = (X + 1/2)^2 (X^2 + 3X - 15/4)/8
    for X in (Fr(-2), Fr(-3, 2), Fr(-1), Fr(0), H):
        R = g(X, (X * X - Fr(1, 4)) / 2)
        ok &= R == (X + H) ** 2 * (X * X + 3 * X - Fr(15, 4)) / 8
    q = lambda X: X * X + 3 * X - Fr(15, 4)
    ok &= q(Fr(-2)) < 0 and q(H) < 0                    # convex, so negative on [-2, 1/2]
    e2 = lambda X: X * X + 5 * X + Fr(17, 4)            # R - L_S = (X - 1/2)^2 e2(X)/8 at phi = 1/6 (L_S = -1/4)
    for X in (Fr(-3), Fr(-2), Fr(-1), Fr(0), Fr(1, 3), Fr(2)):
        R = g(X, (X * X - Fr(1, 4)) / 2)
        ok &= R + Fr(1, 4) == (X - H) ** 2 * e2(X) / 8
    ok &= e2(Fr(-2)) < 0 and e2(Fr(-1)) > 0 and e2(H) > 0
    # beta > 2, chi < 0: the slice at X = 1/beta is open, D = a^2 - chi p = -chi p(1/beta) < 0 (Lemma 2, Step 5)
    nopen = 0
    for (ph, be, ch) in ((Fr(1, 2), Fr(11, 5), Fr(-1, 2)), (Fr(3, 2), Fr(8, 3), Fr(-20, 3)), (Fr(2), Fr(5, 2), Fr(-1, 10))):
        ok &= ph > 0 and abs(ph - be / 2) < 1 and be > 2 and ch < 0
        X = 1 / be
        a = 1 - be * X; p = X * X - Fr(1, 4)
        ok &= a == 0 and p < 0 and a * a - ch * p < 0
        nopen += 1
    return ok, {'witness': [str(v) for v in wit], 'critical_values': [str(v) for v in vals], 'open_slice_cases_beta_gt_2_chi_lt_0': nopen}


def main(argv):
    global MUT
    if len(argv) == 2 and argv[0] == '--mutant':
        if argv[1] not in MUTANTS:
            print('unknown mutant label', file=sys.stderr)
            return 2
        MUT = argv[1]
    elif argv:
        print('usage: soft_check.py [--mutant M1..M14]', file=sys.stderr)
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
    s11, s11d = control_S11()
    s12, s12d = control_S12()
    s13, s13d = control_S13()
    s14, s14d = control_S14()
    res = {'object': 'CL-SOFT-REJECTED-20261002-v1.2', 'scientific_effect': 'NONE',
           'controls': {'S1_theorem_1': s1, 'S2_model_algebra': s2, 'S3_gaussian_kernel_jets': s3, 'S4_elder_edge': s4,
                        'S5_I_series': s5, 'S6_proposition_4': s6, 'S7_lemma_3': s7, 'S8_lemma_2_cases': s8,
                        'S9_lemma_5': s9, 'S10_limit_field': s10, 'S11_theorem_1_every_d': s11,
                        'S12_gaussian_kernel_d3': s12, 'S13_stiff_directions': s13, 'S14_exact_dprime_witness': s14},
           'S1': s1d, 'S2_instances': n2, 'S3': s3d, 'S4': s4d, 'S5': s5d, 'S6': s6d, 'S7': s7d, 'S8': s8d, 'S9': s9d, 'S10': s10d,
           'S11': s11d, 'S12': s12d, 'S13': s13d, 'S14': s14d}
    ok = all(res['controls'].values())
    if MUT is None:
        print(json.dumps(res, indent=1, sort_keys=True))
    else:
        print('mutant ' + MUT + ': failing controls ' + ', '.join(sorted(k for k, v in res['controls'].items() if not v)),
              file=sys.stderr)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
