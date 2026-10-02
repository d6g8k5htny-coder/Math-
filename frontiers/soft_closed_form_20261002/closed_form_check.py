#!/usr/bin/env python3
"""Exact controls for CL-SOFT-CLOSED-FORM-20261002-v1 (Theorem A, Corollaries A.1-A.4, Lemmas B.1-B.2, Theorem B;
PROOF.md).

Standard library only. Exact rationals, except where a control says floating point: C2 (the explicit roots (2.6) against
bisection), C6 (the bound (4.4) at random points) and C7 (a Gauss-Legendre quadrature of (4.3)). Output: RESULTS.json
(sorted keys), byte-identical under -O. Usage:
    python3 -B -S closed_form_check.py                 # exit 0, prints RESULTS.json
    python3 -B -S closed_form_check.py --mutant M3     # exit 1 (only its control fails; M1..M9)
    unknown mutant label                               -> exit 2

Notation (PROOF (0.2)): psi = 1/phi, c' = 1 - t (written cp), R = chi0 + 8 - 12 t, sigma = R/8,
g(psi) = 16 (psi - 2 cp)^2 (psi + cp).

Controls
  C1  Lemma 1: G(X, z) = P_theta(X, 24 phi z)/(24 phi) as a polynomial identity in (X, z) at random rational (phi, t, chi0),
      theta = (-1/(24 phi), 1, t/12, chi0/576), k = 1; [CUB]'s B = -cp/12, D = R/1152, s = -psi/24; (2.3)-(2.4) exactly;
      typing s < -|B|/2 iff psi > |cp|
  C2  Theorem A: g' = 48 psi (psi - 2 cp) and g(c' + y)/16 = (y - cp)^2 (y + 2 cp) = y^3 - 3 cp^2 y + 2 cp^3 as polynomial
      identities; g(psi0) = 0; the discriminant -(4p^3 + 27q^2) = 432 sigma^2 (cp^3 - sigma^2); (2.6) against bisection in
      floating point on 600 points (both branches, cp = 0, sigma = 0), with psi_e >= psi0
  C3  Corollary A.1: (3.1) as a polynomial identity in (psi, t); (3.3) from (2.5) at rational S (t = 3(1 - S^2)/4); the
      ordering psi_+ >= t iff t <= 2/3; the values 20/3, 4/81, 1/3; the slopes -13/9, 5/9 and 1; strict monotonicity on a
      rational grid; the Catalan series (3.4) and the series of I(t, 0) to order 12 (exact power series)
  C4  Corollary A.2: I(1, chi0) = (chi0 - 4)^2/48; the minimum (4/3) cp^3 (cp > 0) and the zero set (cp <= 0) at R = 0;
      the identity (2.7) as a polynomial identity in (cp, y) given the cubic for y
  C5  Corollary A.4: g(t) = 16 (3t - 2)^2 when cp = 1 - t, and on 400 rational typed points with beta > 2, chi0 <= 0 the
      test (A) fails
  C6  Lemma B.2: (a) the derivative formula at rational points with rational square roots; (b) the reduction of
      d^2 Phi/dR^2 to (3p^3 + 2cp p^2 + cp^2 p + 2cp^3)/(72 p^3) as a polynomial identity in (rho, cp); the range [0, 1/16]
      and the monotonicity of 2x + x^2 + 2x^3; (c) the jump kappa = (3cp)^(3/2)/6 at rational squares; (d) the bound (4.4)
      at 300 random points (floating point)
  C7  Lemma B.1(b): F_-' and F_+' as polynomial identities after multiplying by tau^(9/2) S; the exact assembly of Lambda
      in Q(sqrt3, sqrt6) = 128/105 - (2888 sqrt3 + 907 sqrt6)/2835; a floating-point evaluation of (4.3) (exact series near 0,
      Gauss-Legendre elsewhere) within 1e-12; the two forms of h_{7/2} in (4.2) agree exactly in Q(sqrt2, sqrt6), and
      h_{7/2} = -10.1440440225148...
  C8  Theorem B's bookkeeping: E[gamma^6] = 120, E[gamma^6 t^2] = 576 k^2, 800 + 9984 k^2, 312/25 - 12 = 12/25, the
      constants 62208 and 27648 sqrt6/3200 = (216/25) sqrt6, E|B|^q = 2^q Gamma((q+1)/2)/sqrt(pi) at q = 2, 4 (exact), and the
      exponents 7/2, 4, 14/3, 25/6
  C9  Fixed points: #242's exact (D') witness (3/2, 8/3, 20/3) is elder; (0, 0) has psi_e = 3, I = 20/3; #242's 16 control-S8
      decisions; the PROOF section 5 examples
"""
import json
import math
import sys
from fractions import Fraction as Fr

MUTANTS = ('M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9')
MUT = None
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
    NV = 4

    def __init__(self, terms=None):
        self.t = {}
        for k, v in (terms or {}).items():
            if v != 0:
                self.t[k] = Fr(v)

    @classmethod
    def const(cls, c):
        return cls({(0,) * cls.NV: c})

    @classmethod
    def var(cls, i):
        e = [0] * cls.NV
        e[i] = 1
        return cls({tuple(e): 1})

    def __add__(self, o):
        o = o if isinstance(o, P) else P.const(o)
        r = dict(self.t)
        for k, v in o.t.items():
            r[k] = r.get(k, 0) + v
        return P(r)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.t.items()})

    def __sub__(self, o):
        return self + (-(o if isinstance(o, P) else P.const(o)))

    def __rsub__(self, o):
        return P.const(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, P) else P.const(o)
        r = {}
        for k1, v1 in self.t.items():
            for k2, v2 in o.t.items():
                k = tuple(a + b for a, b in zip(k1, k2))
                r[k] = r.get(k, 0) + v1 * v2
        return P(r)

    __rmul__ = __mul__

    def __pow__(self, n):
        r = P.const(1)
        for _ in range(n):
            r = r * self
        return r

    def is_zero(self):
        return not self.t

    def diff(self, i):
        r = {}
        for k, v in self.t.items():
            if k[i]:
                e = list(k)
                e[i] -= 1
                r[tuple(e)] = r.get(tuple(e), 0) + v * k[i]
        return P(r)

    def subs(self, i, val):
        """substitute variable i by the polynomial val"""
        r = P()
        for k, v in self.t.items():
            e = list(k)
            n = e[i]
            e[i] = 0
            r = r + P({tuple(e): v}) * (val ** n)
        return r


V0, V1, V2, V3 = (P.var(i) for i in range(4))


# --------------------------------------------------------------------------------- the closed form (PROOF Theorem A)
def g_of(psi, cp, c16=16):
    return c16 * (psi - 2 * cp) ** 2 * (psi + cp)


def elder_test(psi, cp, R):
    """(A): exact if the inputs are exact"""
    return psi >= 2 * cp and R * R <= g_of(psi, cp)


def psi_e_bisect(cp, R):
    lo = max(2 * cp, -cp)
    hi = lo + 1.0
    while g_of(hi, cp) < R * R:
        hi = lo + 2 * (hi - lo)
    for _ in range(200):
        m = 0.5 * (lo + hi)
        if g_of(m, cp) < R * R:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


def psi_e_formula(cp, R, mutate=False):
    s = R / 8.0
    if cp > 0 and s * s <= cp ** 3:
        return cp + 2 * cp * math.cos(2.0 / 3.0 * math.acos(min(1.0, abs(s) / cp ** 1.5)))
    A = abs(s) + math.sqrt(s * s - cp ** 3)
    if A == 0:
        return cp
    a23 = A ** (2.0 / 3.0)
    return cp + a23 + (-1 if mutate else 1) * cp * cp / a23


def Phi_float(cp, R):
    d = psi_e_bisect(cp, R) - abs(cp)
    return abs(cp) * d * d + d ** 3 / 3


# ======================================================================================= C1: Lemma 1
def control_C1():
    rng = LCG(4101)
    ok = True
    X, Z = V0, V1
    n_id = 0
    for _ in range(30):
        phi = abs(rng.rat(40, 17, True))
        t = rng.rat(60, 13)
        x0 = rng.rat(200, 7)
        beta, chi = 2 * t * phi, x0 * phi * phi
        G = (2 * (X + H) ** 2 * (X - 1) * Fr(1, 24) * (1 / phi) + H * (X * X - Fr(1, 4)) * Z - H * (1 - beta * X) * Z * Z
             + Fr(chi, 6) * Z ** 3)
        s, a, bp, c = -1 / (24 * phi), Fr(1), t / 12, x0 / 576
        Zs = 24 * phi * Z
        Pth = (2 * X ** 3 - Fr(3, 2) * X - H + s * Zs * Zs * H + (a * H) * (X * X - Fr(1, 4)) * Zs + (bp * H) * X * Zs * Zs
               + Fr(1, 6) * c * Zs ** 3)
        ok &= (G - Pth * (1 / (24 * phi))).is_zero()
        n_id += 1
        # [CUB] (C2), (C5)
        psi, cp, R = 1 / phi, 1 - t, x0 + 8 - 12 * t
        B = bp - a * a / 12
        D = (c - a * bp / 4 + a ** 3 / 72) / 2
        ok &= B == -cp / 12 and D == R / 1152 and s == -psi / 24
        T = -(s - B) ** 2 * (B + 2 * s) / 12
        c16 = 15 if MUT == 'M1' else 16
        ok &= T == (psi - 2 * cp) ** 2 * (psi + cp) / 82944
        ok &= 1327104 * (T - D * D) == g_of(psi, cp, c16) - R * R
        ok &= 12 * D * D + B ** 3 == (R * R - 64 * cp ** 3) / 110592
        ok &= 12 * D * D + (s - B) ** 2 * (B + 2 * s) == (R * R - g_of(psi, cp, c16)) / 110592
        ok &= (s < -abs(B) / 2) == (psi > abs(cp))
        ok &= (s <= B) == (psi >= 2 * cp)
    # typing at boundary values
    for cp in (Fr(1, 3), Fr(-2, 5), Fr(0)):
        for psi in (abs(cp), abs(cp) + Fr(1, 1000), 2 * cp if cp > 0 else abs(cp) + 1):
            s, B = -psi / 24, -cp / 12
            ok &= (s < -abs(B) / 2) == (psi > abs(cp))
    return ok, {'identities_G_eq_P': n_id, 'CUB_B': '-cp/12', 'CUB_D': 'R/1152', 'CUB_T': '(psi-2cp)^2(psi+cp)/82944',
                'Delta_1': 'sigma^2 = cp^3', 'Sigma_1': 'R^2 = g(psi)'}


# ======================================================================================= C2: Theorem A
def control_C2():
    ok = True
    psi, cp, y, sg = V0, V1, V2, V3
    g = 16 * (psi - 2 * cp) ** 2 * (psi + cp)
    ok &= (g.diff(0) - 48 * psi * (psi - 2 * cp)).is_zero()
    gy = g.subs(0, cp + y)
    ok &= (gy - 16 * ((y - cp) ** 2 * (y + 2 * cp))).is_zero()
    ok &= (gy - 16 * (y ** 3 - 3 * cp * cp * y + 2 * cp ** 3)).is_zero()
    p, q = -3 * cp * cp, 2 * cp ** 3 - 4 * sg * sg
    ok &= ((-(4 * p ** 3 + 27 * q * q)) - 432 * sg * sg * (cp ** 3 - sg * sg)).is_zero()
    for c in (Fr(2, 7), Fr(-3, 4), Fr(0)):
        ok &= g_of(max(2 * c, -c), c) == 0
    # explicit roots against bisection (floating point)
    rng = LCG(4202)
    worst = 0.0
    n = 0
    branches = {'trig': 0, 'cardano': 0}
    pts = [(0.0, 0.0), (0.0, 3.0), (0.0, -5.0), (-2.0, 0.0), (1.0, 8.0), (0.5, 0.0), (0.5, 2.8284271247461903)]
    while len(pts) < 600:
        cpv = float(rng.rat(300, 11))
        Rv = float(rng.rat(2000, 9))
        pts.append((cpv, Rv))
    for (cpv, Rv) in pts:
        a = psi_e_formula(cpv, Rv, mutate=(MUT == 'M2'))
        b = psi_e_bisect(cpv, Rv)
        worst = max(worst, abs(a - b) / max(1.0, abs(b)))
        p0 = max(2 * cpv, -cpv)
        ok &= a >= p0 - 1e-9 * max(1.0, abs(p0))
        # Remark 4 / (2.8): psi_e <= psi0 + (R^2/16)^(1/3) and Phi <= (16/3)|cp|^3 + R^2/3
        ok &= b <= p0 + (Rv * Rv / 16) ** (1.0 / 3.0) + 1e-9 * max(1.0, b)
        dd = b - abs(cpv)
        ok &= abs(cpv) * dd * dd + dd ** 3 / 3 <= (16.0 / 3.0) * abs(cpv) ** 3 + Rv * Rv / 3 + 1e-9 * (1 + Rv * Rv)
        branches['trig' if (cpv > 0 and (Rv / 8) ** 2 <= cpv ** 3) else 'cardano'] += 1
        n += 1
    ok &= worst < 1e-9
    # g >= 16 (psi - psi0)^3 on [psi0, inf): both factors dominate psi - psi0 (exact, random rationals)
    rng2 = LCG(4203)
    for _ in range(200):
        c = rng2.rat(40, 7)
        p0 = max(2 * c, -c)
        ps = p0 + abs(rng2.rat(60, 7))
        ok &= g_of(ps, c) >= 16 * (ps - p0) ** 3
    return ok, {'points': n, 'branches': branches, 'max_rel_dev_formula_vs_bisection_lt_1e-9': worst < 1e-9,
                'bound_2_8': '(16/3)|cp|^3 + R^2/3'}


# ======================================================================================= C3: Corollary A.1
def catalan(m):
    return math.comb(2 * m, m) // (m + 1)


def sqrt_series(coef_lin, order):
    """exact power series of sqrt(1 + coef_lin*x) to x^order"""
    out = []
    for n in range(order + 1):
        b = Fr(1)
        for j in range(n):
            b *= (H - j)
        b /= math.factorial(n)
        out.append(b * coef_lin ** n)
    return out


def ser_mul(a, b, order):
    return [sum(a[i] * b[n - i] for i in range(n + 1)) for n in range(order + 1)]


def I0_exact_at_S(S):
    """I(t, 0) at t = 3(1 - S^2)/4 with S >= 0 rational (t <= 3/4); returns (t, I) from (3.3)/(3.2)"""
    t = Fr(3, 4) * (1 - S * S)
    if t <= Fr(2, 3):
        cp = 1 - t
        d = H - t + Fr(3, 2) * S
        return t, cp * d * d + d ** 3 / 3
    return t, None


def control_C3():
    ok = True
    psi, t = V0, V1
    cp = 1 - t
    lhs = (psi - 2 * cp) ** 2 * (psi + cp) - (2 - 3 * t) ** 2
    rhs = (psi - t) * (psi * psi + (4 * t - 3) * psi + 4 * t * t - 3 * t)
    ok &= (lhs - rhs).is_zero()
    # (3.3) on t <= 2/3 from (2.5), at rational S
    n33 = 0
    for k in range(1, 61):
        S = Fr(k, 20)                        # S in (0, 3]; t = 3(1 - S^2)/4 in [-6, 3/4)
        tt = Fr(3, 4) * (1 - S * S)
        if tt > Fr(2, 3):
            # psi_+ < t on (2/3, 3/4]
            ok &= Fr(3, 2) - 2 * tt + Fr(3, 2) * S < tt
            continue
        ok &= Fr(3, 2) - 2 * tt + Fr(3, 2) * S >= tt          # psi_+ >= t
        _, I = I0_exact_at_S(S)
        form = (Fr(11, 3) - Fr(21, 2) * tt + Fr(17, 2) * tt ** 2 - Fr(4, 3) * tt ** 3
                + Fr(3, 2) * (1 - tt) * (2 - 3 * tt) * S)
        ok &= I == form
        n33 += 1
    # the values and slopes
    _, I00 = I0_exact_at_S(Fr(1))
    ok &= I00 == Fr(20, 3)
    _, I23 = I0_exact_at_S(Fr(1, 3))
    mid = lambda u: (2 * u - 1) ** 2 * (2 - u) / 3
    ok &= I23 == Fr(4, 81) == mid(Fr(2, 3))
    ok &= mid(Fr(1)) == Fr(1, 3) == Fr(1) - Fr(2, 3)
    # I0' = -delta [2 psi_e + (psi_e + cp)/S] against the exact derivative of (3.3) at rational S (t <= 2/3):
    #   d/dt [P0 + P1 S] = P0' + P1' S + P1 S',  S' = -(2/3)/S
    nder = 0
    for k in range(7, 61):
        S = Fr(k, 20)
        tt = Fr(3, 4) * (1 - S * S)
        if tt > Fr(2, 3):
            continue
        P0p = Fr(-21, 2) + 17 * tt - 4 * tt * tt
        P1 = Fr(3, 2) * (1 - tt) * (2 - 3 * tt)
        P1p = Fr(3, 2) * (-(2 - 3 * tt) - 3 * (1 - tt))
        exact = P0p + P1p * S + P1 * (Fr(-2, 3) / S)
        d, pe, c_ = H - tt + Fr(3, 2) * S, Fr(3, 2) - 2 * tt + Fr(3, 2) * S, 1 - tt
        ok &= exact == -d * (2 * pe + (pe + c_) / S) and exact < 0
        nder += 1
    d, pe, c_, S = Fr(1, 3), Fr(2, 3), Fr(1, 3), Fr(1, 3)
    ok &= -d * (2 * pe + (pe + c_) / S) == Fr(-13, 9)
    dmid = lambda u: (2 * u - 1) * (3 - 2 * u)
    ok &= dmid(Fr(2, 3)) == Fr(5, 9) and dmid(Fr(1)) == 1
    # derivatives of the middle piece; C^2 but not C^3 at t = 1 (the right piece t - 2/3 has I'' = I''' = 0)
    u = V1
    midp = (2 * u - 1) ** 2 * (2 - u) * Fr(1, 3)
    ok &= (midp.diff(1) - (2 * u - 1) * (3 - 2 * u)).is_zero()
    ev1 = lambda poly: sum(v * Fr(1) ** k[1] for k, v in poly.t.items())
    ok &= ev1(midp.diff(1).diff(1)) == 0 and ev1(midp.diff(1).diff(1).diff(1)) == -8
    # strict monotonicity on a rational grid: decreasing for t <= 2/3, increasing on [2/3, 1] and beyond
    vals = []
    for k in range(60, 6, -1):
        S = Fr(k, 20)
        tt, I = I0_exact_at_S(S)
        if I is not None:
            vals.append((tt, I))
    vals.sort()
    ok &= all(vals[i][1] > vals[i + 1][1] for i in range(len(vals) - 1))
    grid = [Fr(2, 3) + Fr(j, 90) for j in range(31)]
    mids = [mid(x) for x in grid]
    ok &= all(mids[i] < mids[i + 1] for i in range(len(mids) - 1))
    # the Catalan series of psi_e(t, 0) = 3/2 - 2t + (3/2) sqrt(1 - 4t/3), and the series of I(t, 0)
    N = 12
    sq = sqrt_series(Fr(-4, 3), N)
    pe_ser = [Fr(3, 2) * c for c in sq]
    pe_ser[0] += Fr(3, 2)
    pe_ser[1] += -2
    cat_ser = [Fr(3), Fr(-3)] + [Fr(-(catalan(m) + (1 if (MUT == 'M3' and m == 3) else 0)), 3 ** m) for m in range(1, N)]
    ok &= pe_ser == cat_ser
    # the quadratic factor vanishes as a power series: psi^2 + (4t - 3) psi + 4t^2 - 3t
    sq_pe = ser_mul(pe_ser, pe_ser, N)
    lin = [Fr(0)] * (N + 1)
    for n in range(N + 1):
        lin[n] += -3 * pe_ser[n] + (4 * pe_ser[n - 1] if n >= 1 else 0)
    quad = [sq_pe[n] + lin[n] + (-3 if n == 1 else 0) + (4 if n == 2 else 0) for n in range(N + 1)]
    ok &= all(q == 0 for q in quad)
    # I(t, 0) series: cp = 1 - t, delta = psi_e - cp
    cp_ser = [Fr(1), Fr(-1)] + [Fr(0)] * (N - 1)
    dl = [a - b for a, b in zip(pe_ser, cp_ser)]
    d2 = ser_mul(dl, dl, N)
    I_ser = [a + b / 3 for a, b in zip(ser_mul(cp_ser, d2, N), ser_mul(d2, dl, N))]
    ok &= I_ser[:6] == [Fr(20, 3), Fr(-20), Fr(52, 3), Fr(-28, 9), Fr(-7, 27), Fr(-7, 81)]
    # phi_e = 1/psi_e = 1/3 + t/3 + 10 t^2/27 + ...
    inv = [Fr(1, 3)]
    for n in range(1, 4):
        inv.append(-sum(pe_ser[i] * inv[n - i] for i in range(1, n + 1)) / pe_ser[0])
    ok &= inv[:3] == [Fr(1, 3), Fr(1, 3), Fr(10, 27)]
    return ok, {'identity_3_1': True, 'points_3_3': n33, 'points_derivative': nder, 't_star': '2/3', 'I(0,0)': str(I00), 'I(2/3,0)': str(I23),
                'slopes_at_2/3': ['-13/9', '5/9'], 'catalan_terms': N, 'I_series': [str(x) for x in I_ser[:6]],
                'phi_e_series': [str(x) for x in inv[:3]]}


# ======================================================================================= C4: Corollary A.2
def control_C4():
    ok = True
    rng = LCG(4404)
    den = 47 if MUT == 'M4' else 48
    psi = V0
    ok &= (16 * (psi - 0) ** 2 * (psi + 0) - 16 * psi ** 3).is_zero()          # g_0(psi) = 16 psi^3
    for _ in range(40):
        x0 = rng.rat(400, 9)
        R = float(x0 - 4)                # t = 1, cp = 0
        pe = psi_e_bisect(0.0, R)        # found independently
        I1 = pe ** 3 / 3
        ok &= abs(I1 - float((x0 - 4) ** 2) / den) <= 1e-9 * (1 + I1)
    for _ in range(40):
        c = rng.rat(50, 7, True)
        pe = max(2 * c, -c)              # R = 0: psi_e = psi0
        ok &= g_of(pe, c) == 0
        d = pe - abs(c)
        I = abs(c) * d * d + d ** 3 / 3
        ok &= I == (Fr(4, 3) * c ** 3 if c > 0 else 0)
        if c > 0:                        # the rejected strip (c', 2c') alone carries (4/3) c'^3 (used on Delta)
            ok &= (8 * c ** 3 / 3 - c * c * 2 * c) - (c ** 3 / 3 - c ** 3) == Fr(4, 3) * c ** 3
    # the zero set, both directions: I = 0 on {t > 1, chi0 = 12t - 8}; I > 0 off it (floating point, bisection)
    nz = 0
    for _ in range(200):
        tt = float(rng.rat(300, 11))
        x0 = float(rng.rat(300, 7))
        if tt > 1 and abs(x0 + 8 - 12 * tt) < 1e-9:
            continue
        cpv, Rv = 1 - tt, x0 + 8 - 12 * tt
        dd = psi_e_bisect(cpv, Rv) - abs(cpv)
        ok &= abs(cpv) * dd * dd + dd ** 3 / 3 > 0
        nz += 1
    for _ in range(20):
        tt = 1 + abs(rng.rat(300, 11, True))
        c = 1 - tt
        ok &= g_of(-c, c) == 0 and (lambda d: abs(c) * d * d + d ** 3 / 3)(-c - abs(c)) == 0
    # (2.7): with R^2 := 16 (y^3 - 3cp^2 y + 2cp^3) and psi_e = cp + y,
    #   psi_e^3/3 - cp^2 psi_e  ==  R^2/48 + cp y (y + cp) - (4/3) cp^3       (the (2/3)|cp|^3 terms agree on both sides)
    cp, y = V0, V1
    R2 = 16 * (y ** 3 - 3 * cp * cp * y + 2 * cp ** 3)
    lhs = (cp + y) ** 3 * Fr(1, 3) - cp * cp * (cp + y)
    rhs = R2 * Fr(1, 48) + cp * y * (y + cp) - Fr(4, 3) * cp ** 3
    ok &= (lhs - rhs).is_zero()
    # and the equivalence of (2.5) with psi_e^3/3 - cp^2 psi_e + (2/3)|cp|^3:  |cp| d^2 + d^3/3, d = psi_e - |cp|
    for _ in range(30):
        c = rng.rat(30, 7)
        pe = abs(c) + abs(rng.rat(30, 7))
        d = pe - abs(c)
        ok &= abs(c) * d * d + d ** 3 / 3 == pe ** 3 / 3 - c * c * pe + Fr(2, 3) * abs(c) ** 3
    return ok, {'I(1,chi0)': '(chi0 - 4)^2/48', 'min_over_chi0': '(4/3)(1-t)_+^3', 'identity_2_7': True,
                'zero_set_positive_points': nz}


# ======================================================================================= C5: Corollary A.4
def control_C5():
    ok = True
    t = V0
    ok &= (16 * (t - 2 * (1 - t)) ** 2 * (t + (1 - t)) - 16 * (3 * t - 2) ** 2).is_zero()
    rng = LCG(4505)
    n = 0
    while n < 400:
        tt = rng.rat(400, 13)
        x0 = -abs(rng.rat(300, 11))
        if MUT == 'M5':
            x0 = abs(x0) + 40
        cp = 1 - tt
        if tt <= 0:
            continue
        # typed with beta > 2: |cp| < psi < t
        lo, hi = abs(cp), tt
        if not lo < hi:
            continue
        psi = lo + (hi - lo) * Fr(1 + rng.nxt() % 998, 1000)
        R = x0 + 8 - 12 * tt
        if tt >= Fr(2, 3):
            ok &= g_of(tt, cp) == 16 * (3 * tt - 2) ** 2
            ok &= R * R >= g_of(tt, cp) and (psi < max(2 * cp, -cp) or g_of(psi, cp) < g_of(tt, cp))
        else:
            ok &= psi < 2 * cp
        ok &= not elder_test(psi, cp, R)
        n += 1
    return ok, {'points_beta_gt_2_chi_le_0': n, 'all_rejected': ok}


# ======================================================================================= C6: Lemma B.2
def control_C6():
    ok = True
    # (a) at rational points with rho + 3cp = q^2: R = 4 rho q, psi_e = rho + 2cp;
    #     dPhi/dR = (psi_e^2 - cp^2) * 2R / g'(psi_e)  ==  (rho + cp) q^3 / (6 (rho + 2 cp))
    rng = LCG(4606)
    na = 0
    for _ in range(60):
        cp = rng.rat(20, 7)
        q = abs(rng.rat(20, 5, True))
        rho = q * q - 3 * cp
        if rho <= 0 or rho + 2 * cp <= 0:
            continue
        R = 4 * rho * q
        pe = rho + 2 * cp
        ok &= g_of(pe, cp) == R * R
        gp = 48 * pe * (pe - 2 * cp)
        ok &= (pe * pe - cp * cp) * 2 * R / gp == (rho + cp) * q ** 3 / (6 * (rho + 2 * cp))
        na += 1
    # (b) d2Phi/dR2 = F'(rho) sqrt(rho+3cp)/(6p), with F = (rho+cp)(rho+3cp)^(3/2)/(6p), p = rho + 2cp:
    #     = [(rho+3cp)^2 + (3/2)(rho+cp)(rho+3cp)]/(36 p^2) - (rho+cp)(rho+3cp)^2/(36 p^3)
    rho, cp = V0, V1
    p = rho + 2 * cp
    cub = 2 if MUT != 'M6' else 3
    lhs = 2 * ((rho + 3 * cp) ** 2 + Fr(3, 2) * (rho + cp) * (rho + 3 * cp)) * p - 2 * (rho + cp) * (rho + 3 * cp) ** 2
    rhs = 3 * p ** 3 + 2 * cp * p * p + cp * cp * p + cub * cp ** 3
    ok &= (lhs - rhs).is_zero()                      # both sides times 72 p^3
    # the range: x = cp/p in [-1, 1/2]; 1/24 + (2x + x^2 + 2x^3)/72 in [0, 1/16]
    f = lambda x: Fr(1, 24) + (2 * x + x * x + 2 * x ** 3) / 72
    ok &= f(Fr(-1)) == 0 and f(H) == Fr(1, 16)
    xv = V0
    dpoly = (2 * xv + xv * xv + 2 * xv ** 3).diff(0)          # 2 + 2x + 6x^2
    co = {k[0]: v for k, v in dpoly.t.items()}
    ok &= co.get(1, 0) ** 2 - 4 * co.get(2, 0) * co.get(0, 0) < 0
    ok &= f(Fr(1, 3)) == Fr(13, 243)                           # d2Phi(1, 8): psi_e = 3, x = 1/3
    ok &= (3 * 3 ** 3 + 2 * 1 * 3 ** 2 + 1 * 3 + 2) * Fr(1, 72 * 27) == Fr(13, 243)
    xs = [Fr(-1) + Fr(k, 40) for k in range(61)]
    ok &= all(f(xs[i]) < f(xs[i + 1]) for i in range(len(xs) - 1))
    # (c) the one-sided limits as exact values of F(rho) = (rho + cp)(rho + 3cp)^(3/2)/(6(rho + 2cp)) at rho0:
    #     cp > 0: rho0 = 0, F = (3cp)^(3/2)/12 (jump 2F = kappa); cp < 0: rho0 = 3|cp|, F = 0; cp = 0: F = rho^(3/2)/6 -> 0
    def Fexact(rho, cp, q):              # q = sqrt(rho + 3cp), rational
        return (rho + cp) * q ** 3 / (6 * (rho + 2 * cp))
    for qq in (Fr(1), Fr(3, 2), Fr(2, 5)):
        c = qq * qq / 3
        ok &= Fexact(Fr(0), c, qq) == qq ** 3 / 12 and 2 * Fexact(Fr(0), c, qq) == qq ** 3 / 6
    for c in (Fr(-1), Fr(-2, 7)):
        ok &= Fexact(3 * abs(c), c, Fr(0)) == 0
    ok &= all(Fexact(Fr(1, n * n), Fr(0), Fr(1, n)) == Fr(1, 6 * n ** 3) for n in (10, 100, 1000))
    # (d) the bound (4.4) at random points (floating point)
    worst = -1.0
    for _ in range(300):
        c = float(rng.rat(30, 7))
        r = float(rng.rat(300, 7))
        h = float(rng.rat(300, 7))
        d2 = 0.5 * (Phi_float(c, r + h) + Phi_float(c, r - h)) - Phi_float(c, r)
        kap = (3 * max(c, 0.0)) ** 1.5 / 6
        bound = h * h / 32 + (kap / 2) * abs(h) * (1.0 if abs(r) < abs(h) else 0.0)
        scale = 1e-9 * (1 + abs(Phi_float(c, r)) + bound)
        ok &= -scale <= d2 <= bound + scale
        worst = max(worst, (d2 - bound) / (1 + bound))
    return ok, {'points_a': na, 'phi_RR_reduction': True, 'range': '[0, 1/16]', 'bound_4_4_points': 300}


# ======================================================================================= C7: Lambda and h_{7/2}
class Q3:
    """a + b sqrt3 + c sqrt6 with rational a, b, c"""

    def __init__(self, a=0, b=0, c=0):
        self.v = (Fr(a), Fr(b), Fr(c))

    def __add__(self, o):
        return Q3(*(x + y for x, y in zip(self.v, o.v)))

    def scale(self, k):
        return Q3(*(k * x for x in self.v))


def poly_from(coeffs):
    """univariate (variable 0) polynomial from a coefficient list"""
    r = P()
    for n, c in enumerate(coeffs):
        r = r + P({(n, 0, 0, 0): c})
    return r


def gauss_legendre(n):
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
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


def control_C7():
    ok = True
    tau = V0
    P1 = lambda u: Fr(3, 2) * (1 - u) * (2 - 3 * u)
    # F_- = S_- Qm tau^(-7/2)/945 with S_-^2 = 1 - 4tau/3:  tau^(9/2) S_- F_-' = [ (S^2)'/2 tau Q + S^2 (tau Q' - 7/2 Q) ]/945
    Qm = poly_from([-810, 3051, -3711, 1444])
    Qp = poly_from([810, 3051, 3711, 1444])
    for sgn, Q, K in ((-1, Qm, Fr(1, 945)), (1, Qp, Fr(-1, 945))):
        S2 = 1 + sgn * Fr(4, 3) * tau
        lhs = K * (S2.diff(0) * Fr(1, 2) * tau * Q + S2 * (tau * Q.diff(0) - Fr(7, 2) * Q))
        p1 = Fr(3, 2) * (1 - tau) * (2 - 3 * tau) if sgn == -1 else Fr(3, 2) * (1 + tau) * (2 + 3 * tau)
        ok &= (lhs - p1 * S2).is_zero()
    # exact assembly of Lambda in Q(sqrt3, sqrt6)
    P0 = {0: Fr(11, 3), 1: Fr(-21, 2), 2: Fr(17, 2), 3: Fr(-4, 3)}
    T2 = {0: Fr(20, 3), 1: Fr(-20), 2: Fr(52, 3)}
    Imid = {0: Fr(2, 3), 1: Fr(-3), 2: Fr(4), 3: Fr(-4, 3)}           # (2t - 1)^2 (2 - t)/3
    lin = {0: Fr(-2, 3), 1: Fr(1)}
    sub = lambda a, b: {k: a.get(k, 0) - b.get(k, 0) for k in set(a) | set(b)}

    def A_at(p, where):
        tot = Q3()
        for n, c in p.items():
            e = Fr(n) - Fr(7, 2)
            v = Q3(0, 0, Fr(2, 3) ** n * Fr(27, 16)) if where == '2/3' else Q3(1)
            tot = tot + v.scale(c / e)
        return tot

    t23 = Fr(2, 3)
    Fm_23 = Q3(0, 0, Fr(1, 3) * (1444 * t23 ** 3 - 3711 * t23 ** 2 + 3051 * t23 - 810) / 945 * Fr(27, 16))
    Fp_inf = Q3(0, Fr(-2888, 2835))
    Lam = (Fm_23 + Fp_inf + A_at(sub(P0, T2), '2/3') + A_at(sub(Imid, T2), '1') + A_at(sub(Imid, T2), '2/3').scale(-1)
           + A_at(sub(lin, T2), '1').scale(-1))
    claim = (Fr(128, 105), Fr(-2887 if MUT == 'M7' else -2888, 2835), Fr(-907, 2835))
    ok &= Lam.v == claim
    lam_f = float(Lam.v[0]) + float(Lam.v[1]) * math.sqrt(3) + float(Lam.v[2]) * math.sqrt(6)
    # floating-point evaluation of (4.3): exact even series below tau0, Gauss-Legendre above
    N = 60
    sm = sqrt_series(Fr(-4, 3), N)
    sp = sqrt_series(Fr(4, 3), N)
    P1m = [Fr(3), Fr(-15, 2), Fr(9, 2)]                     # P1(tau)
    P1p = [Fr(3), Fr(15, 2), Fr(9, 2)]                      # P1(-tau)
    ev = [Fr(0)] * (N + 1)
    ev[0] += -6
    ev[2] += Fr(-53, 3)
    for n in range(N + 1):
        for i, c in enumerate(P1m):
            if n - i >= 0:
                ev[n] += c * sm[n - i]
        for i, c in enumerate(P1p):
            if n - i >= 0:
                ev[n] += c * sp[n - i]
    ok &= all(ev[n] == 0 for n in range(4)) and ev[4] == Fr(-14, 27) and ev[6] == Fr(-2, 27)
    tau0 = 0.2
    head = sum(float(ev[n]) * tau0 ** (n - 3.5) / (n - 3.5) for n in range(4, N + 1))

    def Ifun(u):
        if u <= 2.0 / 3.0:
            S = math.sqrt(1 - 4 * u / 3)
            return 11 / 3 - 21 * u / 2 + 17 * u * u / 2 - 4 * u ** 3 / 3 + 1.5 * (1 - u) * (2 - 3 * u) * S
        if u <= 1.0:
            return (2 * u - 1) ** 2 * (2 - u) / 3
        return u - 2.0 / 3.0

    def Ineg(u):                                           # I(-u, 0), u > 0
        S = math.sqrt(1 + 4 * u / 3)
        return 11 / 3 + 21 * u / 2 + 17 * u * u / 2 + 4 * u ** 3 / 3 + 1.5 * (1 + u) * (2 + 3 * u) * S

    T2f = lambda u: 20 / 3 - 20 * u + 52 / 3 * u * u
    f = lambda u: u ** -4.5 * (Ifun(u) - T2f(u) + Ineg(u) - T2f(-u))
    xs, ws = gauss_legendre(40)
    body = 0.0
    for a, b in ((tau0, 0.4), (0.4, 2.0 / 3.0), (2.0 / 3.0, 1.0)):
        body += sum(w * f(0.5 * (b - a) * x + 0.5 * (a + b)) for x, w in zip(xs, ws)) * 0.5 * (b - a)
    # [1, inf): tau = 1/v^2, d tau = -2 v^-3 dv
    body += sum(w * 2 * (0.5 * x + 0.5) ** -3 * f((0.5 * x + 0.5) ** -2) for x, w in zip(xs, ws)) * 0.5
    lam_q = head + body
    ok &= abs(lam_q - lam_f) < 1e-12
    # h_{7/2}: (216/25) sqrt6 Lambda == (16/2625)(1728 sqrt6 - 4332 sqrt2 - 2721) exactly, in the basis (1, sqrt2, sqrt6)
    a, b, c = Lam.v                                       # sqrt6*(a + b sqrt3 + c sqrt6) = 6c + 3b sqrt2 + a sqrt6
    left = (Fr(216, 25) * 6 * c, Fr(216, 25) * 3 * b, Fr(216, 25) * a)
    right = (Fr(16, 2625) * -2721, Fr(16, 2625) * -4332, Fr(16, 2625) * 1728)
    ok &= left == right
    h72 = 16 * math.gamma(2.25) * (1728 * math.sqrt(6) - 4332 * math.sqrt(2) - 2721) / (2625 * math.pi)
    ok &= abs(h72 - (-10.144044022514828)) < 1e-12
    return ok, {'Lambda': [str(x) for x in Lam.v], 'Lambda_float_12dp': round(lam_f, 12),
                'quadrature_agrees_1e-12': abs(lam_q - lam_f) < 1e-12, 'h72_10dp': round(h72, 10),
                'even_series_first_terms': [str(ev[4]), str(ev[6])]}


# ======================================================================================= C8: Theorem B bookkeeping
def control_C8():
    ok = True
    # Gaussian moments of N(0, 2): E[x^2] = 2, E[x^4] = 12, E[x^6] = 120
    m = {2: Fr(2), 4: Fr(12), 6: Fr(120)}
    ok &= m[6] == 15 * 2 ** 3 and m[4] == 3 * 2 ** 2
    Eg6t2 = 144 * m[2] * m[2] if MUT != 'M8' else 575
    ok &= Eg6t2 == 576
    ok &= m[6] * Fr(20, 3) == 800 and Fr(52, 3) * Eg6t2 == 9984
    ok &= Fr(9984, 800) == Fr(312, 25) and Fr(312, 25) - 12 == Fr(12, 25)
    ok &= Fr(331776 * 6, 32) == 62208 and 576 ** 2 == 331776
    ok &= 24 ** 3 * 2 == 27648 and Fr(27648, 3200) == Fr(216, 25)       # 24^(7/2) = 24^3 sqrt24 = 27648 sqrt6
    # E|B|^q = 2^q Gamma((q+1)/2)/sqrt(pi) for N(0, 2): q = 2 -> 2, q = 4 -> 12 (Gamma(3/2) = sqrt(pi)/2, Gamma(5/2) = 3 sqrt(pi)/4)
    ok &= Fr(2 ** 2, 2) == m[2] and Fr(2 ** 4 * 3, 4) == m[4]
    # exponents: gamma = sqrt(k) g gives gamma^6 d gamma = k^(7/2); the error terms
    ok &= Fr(6, 2) + Fr(1, 2) == Fr(7, 2) and Fr(7, 2) + Fr(1, 2) == 4
    ok &= 2 + Fr(8, 3) == Fr(14, 3) and 2 + Fr(3, 2) + Fr(2, 3) == Fr(25, 6) and Fr(25, 6) > 4
    # E|B|^(7/2) = 2^(7/2) Gamma(9/4)/sqrt(pi) for B ~ N(0, 2), against Gauss-Legendre (floating point)
    xs, ws = gauss_legendre(40)
    def quad(f, a, b):
        return sum(w * f(0.5 * (b - a) * x + 0.5 * (a + b)) for x, w in zip(xs, ws)) * 0.5 * (b - a)
    dens = lambda x: math.exp(-x * x / 4) / math.sqrt(4 * math.pi)
    m72 = 2 * sum(quad(lambda x: x ** 3.5 * dens(x), a, b) for a, b in ((0, 1), (1, 4), (4, 10), (10, 20), (20, 40)))
    ok &= abs(m72 - 2 ** 3.5 * math.gamma(2.25) / math.sqrt(math.pi)) < 1e-10
    # the k^4 constants: 64512 = (7/27) 12^4 E[B^4]; int (p(w) - p(0)) w^-2 dw = -1/2; 32256; 53248; h4 = 728/25
    ok &= Fr(7, 27) * 12 ** 4 * m[4] == 64512
    pw = lambda w: (math.exp(-w * w / 4) - 1) / (w * w) / math.sqrt(4 * math.pi) if w > 1e-6 else -0.25 / math.sqrt(4 * math.pi)
    ipw = 2 * (sum(quad(pw, a, b) for a, b in ((0, 1), (1, 4), (4, 10), (10, 30), (30, 100))) - 1 / (100 * math.sqrt(4 * math.pi)))
    ok &= abs(ipw + 0.5) < 1e-10
    A4 = Fr(64512, 2)
    B4 = Fr(331776, 2) * Fr(13, 243) * 6
    ok &= A4 == 32256 and B4 == 53248
    h4 = (A4 + B4) / 800 + 72 - 12 * Fr(312, 25)
    ok &= h4 == Fr(728, 25)
    ok &= Fr(7, 2) + 1 == Fr(9, 2)
    return ok, {'E_gamma6': '120', 'E_gamma6_t2': '576 k^2', 'H_k2': '12/25', 'E_absB_7/2_quadrature': True,
                'k4_constants': ['32256', '53248'], 'h4': str(h4), 'h72_constant': '(216/25) sqrt6 Gamma(9/4) Lambda / pi'}


# ======================================================================================= C9: fixed points
def control_C9():
    ok = True
    res = []
    # #242's exact (D') witness (phi, beta, chi) = (3/2, 8/3, 20/3)
    phi, beta, chi = Fr(3, 2), Fr(8, 3), Fr(20, 3)
    t, x0 = beta / (2 * phi), chi / phi ** 2
    psi, cp, R = 1 / phi, 1 - t, x0 + 8 - 12 * t
    w = elder_test(psi, cp, R)
    ok &= w == (MUT != 'M9')
    res.append(['witness', [str(phi), str(beta), str(chi)], [str(t), str(x0)], w])
    # (0, 0): psi_e = 3, I = 20/3
    ok &= g_of(Fr(3), Fr(1)) == 64 == (0 + 8 - 0) ** 2
    d = Fr(3) - 1
    ok &= 1 * d * d + d ** 3 / 3 == Fr(20, 3)
    # #242 control S8 (floating point, its 16 cases)
    cases = [((0.30, 0.0, 0.0), 1), ((0.36, 0.0, 0.0), 0), ((0.3333, 0.0, 0.0), 1), ((0.3334, 0.0, 0.0), 0),
             ((0.95, 0.0, 0.0), 0), ((0.5, 2.2, 0.0), 0), ((0.04, 0.09, 0.002), 1),
             ((0.30, 0.0, 3.0), 0), ((0.20, 0.0, 1.0), 0), ((0.20, 0.0, 0.5), 1), ((0.05, 0.0, 0.5), 1),
             ((0.05, 0.0, 0.85), 0), ((0.03, -0.1, 0.0), 1),
             ((0.2401, 2.1425, 0.5536), 1), ((0.6267, 2.3645, 2.8796), 1), ((0.5, 2.2, 0.01), 0)]
    agree = 0
    at_origin = 0
    for (ph, be, ch), e in cases:
        tt, xx = be / (2 * ph), ch / ph ** 2
        dec = int(elder_test(1 / ph, 1 - tt, xx + 8 - 12 * tt))
        agree += dec == e
        at_origin += (be == 0.0 and ch == 0.0)          # (t, chi0) = (0, 0) lies on Delta: Remark 2, not Theorem A
    ok &= agree == len(cases)
    # section 5 examples: t = 9.005434, chi0 = 193.926947
    tt, xx = 9.005434, 193.926947
    ex = [(0.1112, 1), (0.1124, 1), (0.1126, 0), (0.113, 0)]
    ex_ok = all(int(elder_test(1 / ph, 1 - tt, xx + 8 - 12 * tt)) == e for ph, e in ex)
    # example 2 (a table node): Theorem A's edge 0.0871797..., the scanner's 0.0871798 (falsely accepted there)
    tt, xx = 11.464348642908552, -0.426511285632118
    edge = 1 / psi_e_bisect(1 - tt, xx + 8 - 12 * tt)
    ex2 = [(0.08717970, 1), (0.08717976, 0), (0.0871798, 0)]
    ex_ok &= abs(edge - 0.0871797) < 1e-7 and all(int(elder_test(1 / ph, 1 - tt, xx + 8 - 12 * tt)) == e for ph, e in ex2)
    ok &= ex_ok
    return ok, {'witness_elder': w, 'S8_agree': agree, 'S8_cases': len(cases), 'S8_at_origin_on_Delta': at_origin,
                'section5_examples': ex_ok}


def main(argv):
    global MUT
    if len(argv) == 2 and argv[0] == '--mutant':
        if argv[1] not in MUTANTS:
            print('unknown mutant label', file=sys.stderr)
            return 2
        MUT = argv[1]
    elif argv:
        print('usage: closed_form_check.py [--mutant M1..M9]', file=sys.stderr)
        return 2
    out = {}
    controls = {}
    for name, fn in (('C1_lemma1_identification', control_C1), ('C2_theorem_A', control_C2),
                     ('C3_corollary_A1_chi0_zero', control_C3), ('C4_corollary_A2', control_C4),
                     ('C5_corollary_A4', control_C5), ('C6_lemma_B2_Phi', control_C6),
                     ('C7_lemma_B1_Lambda_h72', control_C7), ('C8_theorem_B_bookkeeping', control_C8),
                     ('C9_fixed_points', control_C9)):
        ok, detail = fn()
        controls[name] = bool(ok)
        out[name.split('_')[0]] = detail
    res = {'object': 'CL-SOFT-CLOSED-FORM-20261002-v1', 'scientific_effect': 'NONE', 'controls': controls}
    res.update(out)
    ok = all(controls.values())
    if MUT is None:
        print(json.dumps(res, indent=1, sort_keys=True))
    else:
        print('mutant ' + MUT + ': failing controls ' + ', '.join(sorted(k for k, v in controls.items() if not v)),
              file=sys.stderr)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
