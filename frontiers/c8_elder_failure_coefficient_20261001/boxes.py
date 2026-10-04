"""Box enclosures of the failure integrands (certified engine; standard library only).

Jet coordinates.  (a, beta, c) ~ N(0, diag(2, 2, 6)) are the odd jets of [NUM] section 2.  For a gap mark k the scaled
coordinates a^ = a / sqrt k ~ N(0, 2/k), beta ~ N(0, 2), c^ = sqrt(k) c ~ N(0, 6k) give
    B = beta - a^2/12,   u = c^ + d,   d = -a^ beta/4 + a^3/72,   w = |u|,   T = 3 w^2  ( = 12 k D^2 of [NUM] section 3).
Roots.  P(x) = (x + B)^2 (2x - B).  The big root x(B, T) >= xm = max(-B, B/2) solves P(x) = T (P increasing and convex on
[xm, inf), P(xm) = 0).  For B < 0 and T <= |B|^3/2 the middle root solves P(x) = T in [|B|/2, |B|] (P decreasing there).
Integrands.  With r = B/x:
    H   = |B|^3 + 4x^3 - 3B^2 x = 2(B_-)^3 + 2T + V,   V = -3B(2x - B)(x + B)             (big root)
    H_2 = |B|^3 + 4x^3 - 3B^2 x = 2|B|^3 + 2T + V                                    (middle root, inside its support)
    V_B  = x^2 (-6 + 9r^2/2 - 3r^3/2),     V_w = -sigma sqrt3 x^(3/2) r (4 + r)(2 - r)^(1/2)
    V_BB = x p(r),  p(r) = 6 + 3r - 9r^2/2 - 3r^3/4 + 3r^4/4
    V_Bw = -sigma (sqrt3/2) x^(1/2) e(r),  e(r) = (2 - r)^(3/2)(4 + 2r + r^2)
    V_ww = g(r) = -r(4 - r + r^2)
with sigma = +1 on the big root and -1 on the middle root (derivatives in (B, w) at fixed w, resp. fixed B).
Per box:  I1 = Gaussian mass x pointwise range (monotonicity at the corners of the image rectangle), and, on one side of
u = 0, I2 = second-order Taylor expansion in (B, w) about a float point (B*, w*) of the rectangle with exact Gaussian
polynomial moments and the integral-form remainder, whose averaged Hessian entries lie in the interval ranges of the
second derivatives over the rectangle.  The box integral lies in I1 and in I2; the intersection is returned (an empty
intersection raises)."""
import math
from ia import (dn, up, add, sub, neg, mul, div, scal, divc, sqr, pw, isqrt, exp_neg, Q_point, SQRT2PI)

MUTANT = None                       # set by certificate.py --mutant (the certificate must then fail)
SQRT3 = isqrt((3.0, 3.0))
HSQRT3 = scal(0.5, SQRT3)
_U = 2.0 ** -53


# ================================================================ 1D Gaussian partial moments
def phis(x, s, s2):
    """phi_sigma(x) for a float x, sigma interval s, sigma^2 interval s2."""
    return div(exp_neg(div(sqr((x, x)), scal(2.0, s2))), mul(s, SQRT2PI))


def _Qiv(t):
    """Q = 1 - Phi over an interval t >= 0 (decreasing)."""
    return (Q_point(t[1])[0], Q_point(t[0])[1])


def cell_mass(x0, x1, s):
    """Gaussian mass of [x0, x1], computed on the side away from 0 as a difference of upper tails."""
    t0, t1 = div((x0, x0), s), div((x1, x1), s)
    if x0 >= 0.0:
        return sub(_Qiv(t0), _Qiv(t1))
    if x1 <= 0.0:
        return sub(_Qiv(neg(t1)), _Qiv(neg(t0)))
    return sub(sub((1.0, 1.0), _Qiv(t1)), _Qiv(neg(t0)))


def moments(x0, x1, s, s2, nmax):
    """M_n = int_{x0}^{x1} x^n phi_sigma(x) dx, n = 0..nmax:  M_1 = s^2 (phi(x0) - phi(x1)),
    M_n = (n - 1) s^2 M_{n-2} + s^2 (x0^(n-1) phi(x0) - x1^(n-1) phi(x1))."""
    p0, p1 = phis(x0, s, s2), phis(x1, s, s2)
    m0 = cell_mass(x0, x1, s)
    M = [(max(0.0, m0[0]), m0[1])]
    if nmax >= 1:
        M.append(mul(s2, sub(p0, p1)))
    x0i, x1i = (x0, x0), (x1, x1)
    for n in range(2, nmax + 1):
        t = sub(mul(pw(x0i, n - 1), p0), mul(pw(x1i, n - 1), p1))
        M.append(add(mul(scal(float(n - 1), s2), M[n - 2]), mul(s2, t)))
    return M


class Moments:
    """Cache of the partial moments of one coordinate."""
    def __init__(self, sig, sig2, nmax):
        self.sig, self.sig2, self.nmax, self.c = sig, sig2, nmax, {}

    def get(self, x0, x1):
        key = (x0, x1)
        r = self.c.get(key)
        if r is None:
            r = moments(x0, x1, self.sig, self.sig2, self.nmax)
            self.c[key] = r
        return r


# ================================================================ verified roots
def _sgn_f(x, B, T):
    """Rigorous sign of P(x) - T at floats x, B, T >= 0 (+1, -1, or 0 if undecided).  The binary64 error of
    p = x + B, q = 2x - B (2x exact), p*p*q and the final subtraction is below 5u (p^2 |q|) + u |f|; the test uses
    8u (p^2 |q| + T) + 4u |f| + 1e-300."""
    p = x + B
    q = 2.0 * x - B
    r = p * p * q
    f = r - T
    e = 8.0 * _U * (abs(r) + T) + 4.0 * _U * abs(f) + 1e-300
    if f > e:
        return 1
    if f < -e:
        return -1
    return 0


def _guess_big(B, T):
    aB = abs(B)
    if B < 0 and T < aB ** 3:
        c = -1.0 + 2.0 * T / aB ** 3
        ph = math.acos(max(-1.0, min(1.0, c)))
        return aB * (math.cos(ph / 3.0) + 0.5)
    h = B ** 3 / 8.0 + T / 4.0
    sd = math.sqrt(max(0.0, T * (B ** 3 + T) / 16.0))
    A, C = h + sd, h - sd
    y = math.copysign(abs(A) ** (1.0 / 3.0), A) + math.copysign(abs(C) ** (1.0 / 3.0), C)
    return y - B / 2.0


def _guess_mid(B, T):
    aB = -B
    c = -1.0 + 2.0 * T / aB ** 3
    ph = math.acos(max(-1.0, min(1.0, c)))
    return aB * (math.cos((2.0 * math.pi - ph) / 3.0) + 0.5)


def _newton_big(B, T, xm):
    lo = xm
    hi = xm + 2.0 * (T / 2.0) ** (1.0 / 3.0) + abs(B) + 1.0      # starting bracket only (the result is verified)
    x = _guess_big(B, T)
    if not (lo < x < hi):
        x = 0.5 * (lo + hi)
    for _ in range(60):
        fx = (x + B) * (x + B) * (2 * x - B) - T
        d = 6 * x * (x + B)
        if fx > 0:
            hi = min(hi, x)
        else:
            lo = max(lo, x)
        nx = x - fx / d if d > 0 else 0.5 * (lo + hi)
        if not (lo < nx < hi):
            nx = 0.5 * (lo + hi)
        if abs(nx - x) <= 2e-15 * max(1.0, abs(x)):
            return nx
        x = nx
    return x


def xbig(B, Tlo, Thi=None):
    """Interval containing the big root x(B, T) for every T in [Tlo, Thi]: the lower end a has a = xm or P(a) < Tlo, the
    upper end b has P(b) > Thi (P increasing on [xm, inf))."""
    if Thi is None:
        Thi = Tlo
    xm = -B if B < 0 else B / 2.0
    if Thi <= 0.0:
        return (xm, xm)
    x = _newton_big(B, 0.5 * (Tlo + Thi), xm)
    delta = 8e-16 * max(1.0, abs(x))
    for _ in range(60):
        a, b = max(xm, x - delta), x + delta
        if (a <= xm or _sgn_f(a, B, Tlo) == -1) and _sgn_f(b, B, Thi) == 1:
            return (a, b)
        delta *= 4.0
    raise RuntimeError('big-root bracket failed: B=%r T=[%r, %r]' % (B, Tlo, Thi))


def xmid(B, Tlo, Thi=None):
    """Interval containing the middle root x(B, T) in [|B|/2, |B|] for every T in [Tlo, Thi] (B < 0,
    Thi <= |B|^3/2): lower end a = |B|/2 or P(a) > Thi, upper end b = |B| or P(b) < Tlo (P decreasing there)."""
    if Thi is None:
        Thi = Tlo
    aB = -B
    lo0, hi0 = aB / 2.0, aB
    if Thi <= 0.0:
        return (hi0, hi0)
    T = 0.5 * (Tlo + Thi)
    lo, hi = lo0, hi0
    x = _guess_mid(B, T)
    if not (lo < x < hi):
        x = 0.5 * (lo + hi)
    for _ in range(80):
        fx = (x + B) * (x + B) * (2 * x - B) - T
        if fx > 0:
            lo = x
        else:
            hi = x
        d = 6 * x * (x + B)
        nx = x - fx / d if d < 0 else 0.5 * (lo + hi)
        if not (lo < nx < hi):
            nx = 0.5 * (lo + hi)
        if abs(nx - x) <= 2e-15 * max(1.0, abs(x)):
            x = nx
            break
        x = nx
    delta = 8e-16 * max(1.0, abs(x))
    for _ in range(60):
        a, b = max(lo0, x - delta), min(hi0, x + delta)
        if (a <= lo0 or _sgn_f(a, B, Thi) == 1) and (b >= hi0 or _sgn_f(b, B, Tlo) == -1):
            return (a, b)
        delta *= 4.0
    raise RuntimeError('middle-root bracket failed: B=%r T=[%r, %r]' % (B, Tlo, Thi))


def _cbrt_lo(y):
    """A float c >= 0 with c^3 <= y (y >= 0)."""
    if y <= 0:
        return 0.0
    c = y ** (1.0 / 3.0)
    while pw((c, c), 3)[1] > y:
        c = dn(c)
    return c


# ================================================================ pointwise pieces
def _nonneg(a):
    return (max(0.0, a[0]), max(0.0, a[1]))


def _hull0(a):
    return (min(0.0, a[0]), max(0.0, a[1]))


def V_iv(Bi, xi):
    """V = -3B(2x - B)(x + B)."""
    return mul(scal(-3.0, Bi), mul(sub(scal(2.0, xi), Bi), add(xi, Bi)))


def VB_iv(Bi, xi):
    """V_B = -6x^2 + 9B^2/2 - 3B^3/(2x) (either root, x > 0)."""
    return add(add(scal(-6.0, sqr(xi)), scal(4.5, sqr(Bi))), neg(div(scal(1.5, pw(Bi, 3)), xi)))


def Vw_big_iv(Bi, xi):
    """V_w on the big root: -sqrt3 B (4x + B)(2x - B)^(1/2)/x  (the middle root has the opposite sign)."""
    q = _nonneg(sub(scal(2.0, xi), Bi))
    v = neg(div(mul(mul(SQRT3, mul(Bi, add(scal(4.0, xi), Bi))), isqrt(q)), xi))
    return neg(v) if MUTANT == 'vw-sign' else v


_P = (6.0, 3.0, -4.5, -0.75, 0.75)          # p(r), increasing degree
_DP = (3.0, -9.0, -2.25, 3.0)               # p'(r)


def _horner(coef, R):
    acc = (coef[-1], coef[-1])
    for c in reversed(coef[:-1]):
        acc = add(mul(acc, R), (c, c))
    return acc


def p_range(R):
    """Mean-value enclosure of p over the interval R."""
    rc = 0.5 * (R[0] + R[1])
    return add(_horner(_P, (rc, rc)), mul(_horner(_DP, R), sub(R, (rc, rc))))


def _g_pt(r):
    ri = (r, r)
    return neg(mul(ri, add(sub((4.0, 4.0), ri), sqr(ri))))


def g_range(R):
    """g(r) = -r(4 - r + r^2) is strictly decreasing (g' = -4 + 2r - 3r^2 < 0)."""
    if MUTANT == 'ww-drop':
        return (0.0, 0.0)
    return (_g_pt(R[1])[0], _g_pt(R[0])[1])


def _e_pt(r):
    t = _nonneg(sub((2.0, 2.0), (r, r)))
    ri = (r, r)
    return mul(mul(t, isqrt(t)), add(add((4.0, 4.0), scal(2.0, ri)), sqr(ri)))


def e_range(R):
    """e(r) = (2 - r)^(3/2)(4 + 2r + r^2) is decreasing on r <= 2 (e' = (2 - r)^(1/2)(-2 - r - 7r^2/2) < 0)."""
    return (_e_pt(R[1])[0], _e_pt(R[0])[1])


# ================================================================ image rectangles
def d_iv(ai, bi):
    return add(divc(neg(mul(ai, bi)), 4.0), divc(pw(ai, 3), 72.0))


def d_range(a0, a1, b0, b1):
    """Range of d = -a beta/4 + a^3/72 over a rectangle: linear in beta (extremes at beta = b0, b1); for fixed beta
    the a-extremes are at a0, a1 or at a = +-sqrt(6 beta) (beta > 0), where d = -+ beta^(3/2)/sqrt6."""
    cands = []
    for b in (b0, b1):
        bi = (b, b)
        for a in (a0, a1):
            cands.append(d_iv((a, a), bi))
        if b > 0:
            r = isqrt(scal(6.0, bi))
            val = div(mul(bi, isqrt(bi)), isqrt((6.0, 6.0)))
            if r[0] < a1 and a0 < r[1]:
                cands.append(neg(val))
            if -r[1] < a1 and a0 < -r[0]:
                cands.append(val)
    return (min(c[0] for c in cands), max(c[1] for c in cands))


def box_geometry(box):
    """(Bl, Bh, ul, uh): ranges of B and u over a box of scaled coordinates."""
    (a0, a1), (b0, b1), (c0, c1) = box
    A2 = sqr((a0, a1))
    Bl = dn(b0 - up(A2[1] / 12.0))
    Bh = up(b1 - dn(A2[0] / 12.0))
    dl, dh = d_range(a0, a1, b0, b1)
    return Bl, Bh, dn(c0 + dl), up(c1 + dh)


def wT(ul, uh):
    """(s, wl, wh, Tl, Th): s = sign of u on the box (0 if the u-range meets 0), ranges of w = |u| and T = 3w^2."""
    if ul > 0.0:
        s, wl, wh = 1, ul, uh
    elif uh < 0.0:
        s, wl, wh = -1, -uh, -ul
    else:
        s, wl, wh = 0, 0.0, max(-ul, uh)
    Tl = max(0.0, dn(3.0 * max(0.0, dn(wl * wl)))) if wl > 0.0 else 0.0
    Th = up(3.0 * up(wh * wh))
    return s, wl, wh, Tl, Th


def half_cube(B):
    """|B|^3/2 for a float B < 0."""
    return scal(0.5, pw((-B, -B), 3))


# ================================================================ second-order pieces
def taylor_moments3(A, Bm, C, Bs, us):
    """(m, int dB, int du, int dB^2, int du^2, int dB du) over a 3D box, dB = B - Bs, du = u - us (exact polynomial
    moments; A to order 6, Bm and C to order 2)."""
    ab = lambda i, j: mul(A[i], Bm[j])
    ab00, ab01, ab02 = ab(0, 0), ab(0, 1), ab(0, 2)
    ab11, ab12 = ab(1, 1), ab(1, 2)
    ab20, ab21, ab22 = ab(2, 0), ab(2, 1), ab(2, 2)
    ab30, ab31 = ab(3, 0), ab(3, 1)
    ab40, ab41 = ab(4, 0), ab(4, 1)
    ab50, ab60 = ab(5, 0), ab(6, 0)
    Bsi, usi = (Bs, Bs), (us, us)
    gB0 = sub(sub(ab01, divc(ab20, 12.0)), mul(Bsi, ab00))                       # int (B - Bs) over (a, beta)
    gBB = add(add(add(ab02, divc(ab40, 144.0)), mul(sqr(Bsi), ab00)),
              add(sub(divc(mul(Bsi, ab20), 6.0), divc(ab21, 6.0)), scal(-2.0, mul(Bsi, ab01))))
    Id1 = add(divc(neg(ab11), 4.0), divc(ab30, 72.0))                            # int d
    Id2 = add(add(divc(ab22, 16.0), divc(neg(ab41), 144.0)), divc(ab60, 5184.0))   # int d^2
    IBd = sub(add(add(divc(neg(ab12), 4.0), divc(scal(5.0, ab31), 144.0)), divc(neg(ab50), 864.0)), mul(Bsi, Id1))
    C0, C1, C2 = C[0], C[1], C[2]
    Cs1 = sub(C1, mul(usi, C0))                                                  # int (c - us)
    Cs2 = add(sub(C2, scal(2.0, mul(usi, C1))), mul(sqr(usi), C0))                # int (c - us)^2
    m = mul(ab00, C0)
    E1B = mul(gB0, C0)
    E1u = add(mul(ab00, Cs1), mul(Id1, C0))
    QB = mul(gBB, C0)
    Qu = add(add(mul(ab00, Cs2), scal(2.0, mul(Id1, Cs1))), mul(Id2, C0))
    QBu = add(mul(gB0, Cs1), mul(IBd, C0))
    return m, E1B, E1u, _nonneg(QB), _nonneg(Qu), QBu


def _quad(SBB, SBw, Sww, QB, Qu, QBu, s):
    """Remainder integral 1/2 int (h_BB dB^2 + 2 h_Bw dB dw + h_ww dw^2) with averaged Hessian entries h in the ranges
    S: in 1/2 (SBB QB + Sww Qu) + s c QBu +- d sqrt(QB Qu), c = centre and d = radius of SBw (dw = s du)."""
    c = 0.5 * (SBw[0] + SBw[1])
    dBw = up(max(up(SBw[1] - c), up(c - SBw[0])))
    cross = scal(float(s), mul((c, c), QBu))
    rad = up(dBw * up(math.sqrt(up(QB[1] * Qu[1]))) * (1.0 + 4 * _U))
    q = add(add(scal(0.5, mul(SBB, QB)), scal(0.5, mul(Sww, Qu))), cross)
    return (dn(q[0] - rad), up(q[1] + rad))


def _expansion_point(ac, bc, cc, Bl, Bh, s, wl, wh):
    """Float point (B*, w*) of the image rectangle near the image of the box centre (a^, beta, c^) = (ac, bc, cc)."""
    Bs = min(max(bc - ac * ac / 12.0, Bl), Bh)
    ws = min(max(s * (cc - ac * bc / 4.0 + ac ** 3 / 72.0), wl), wh)
    return Bs, ws


def _intersect(I1, I2, what):
    lo, hi = max(I1[0], I2[0]), min(I1[1], I2[1])
    if lo > hi:
        raise RuntimeError('inconsistent %s enclosures: %r vs %r' % (what, I1, I2))
    return (lo, hi)


class Rect:
    """Image rectangle of a box with its corner roots (big root)."""
    def __init__(self, Bl, Bh, ul, uh):
        self.Bl, self.Bh, self.ul, self.uh = Bl, Bh, ul, uh
        self.s, self.wl, self.wh, self.Tl, self.Th = wT(ul, uh)
        self._c = None

    def corners(self):
        if self._c is None:
            Bl, Bh, Tl, Th = self.Bl, self.Bh, self.Tl, self.Th
            self._c = (xbig(Bl, Tl), xbig(Bl, Th), xbig(Bh, Tl), xbig(Bh, Th))
        return self._c


def V_range(R):
    """[min V, max V] over the rectangle: V non-increasing in B; in T non-increasing for B > 0, non-decreasing for
    B < 0; V(0, T) = 0."""
    xLL, xLH, xHL, xHH = R.corners()
    Bl, Bh = R.Bl, R.Bh
    if MUTANT == 'corner-swap':
        xHH, xHL = xHL, xHH
    vmin = V_iv((Bh, Bh), xHH)[0] if Bh > 0 else (V_iv((Bh, Bh), xHL)[0] if Bh < 0 else 0.0)
    vmax = V_iv((Bl, Bl), xLH)[1] if Bl < 0 else (V_iv((Bl, Bl), xLL)[1] if Bl > 0 else 0.0)
    return (vmin, vmax)


def _Bneg3(Bi):
    lo = pw((max(0.0, -Bi[1]),) * 2, 3)[0]
    hi = pw((max(0.0, -Bi[0]),) * 2, 3)[1]
    return (max(0.0, lo), hi)


def _Bneg(Bi):
    return (max(0.0, -Bi[1]), max(0.0, -Bi[0]))


def _H_at(B, T, xi):
    return add(add(scal(2.0, _Bneg3((B, B))), (dn(2.0 * T), up(2.0 * T))), V_iv((B, B), xi))


def H_range(R):
    """[min H, max H]: H is non-increasing in B and non-decreasing in T."""
    xLL, xLH, xHL, xHH = R.corners()
    return (max(0.0, _H_at(R.Bh, R.Tl, xHL)[0]), _H_at(R.Bl, R.Th, xLH)[1])


def big_hessian(R, with_H):
    """Interval ranges (S_BB, S_Bw, S_ww) of the (B, w)-Hessian of V (or of H if with_H) over the rectangle (one side of
    u = 0).  x is increasing in T and, for fixed T, unimodal in B with minimum x = B at B = (T/4)^(1/3); r = B/x is
    non-decreasing in B, increasing in T for B < 0 and decreasing for B > 0; r in [-1, 2]."""
    xLL, xLH, xHL, xHH = R.corners()
    Bl, Bh, Tl = R.Bl, R.Bh, R.Tl
    XL, XH = min(xLL[0], xHL[0]), max(xLH[1], xHH[1])
    if Bh > 0:
        XL = min(XL, _cbrt_lo(max(0.0, dn(Tl / 4.0))))
    if XL <= 0.0:
        Rr = (-1.0, 2.0)
        XL = 0.0
    else:
        rmin = div((Bl, Bl), xLL)[0] if Bl < 0 else (div((Bl, Bl), xLH)[0] if Bl > 0 else 0.0)
        rmax = div((Bh, Bh), xHL)[1] if Bh > 0 else (div((Bh, Bh), xHH)[1] if Bh < 0 else 0.0)
        Rr = (max(-1.0, rmin), min(2.0, rmax))
    X = (XL, XH)
    SBB = mul(X, p_range(Rr))
    if with_H:
        SBB = add(SBB, scal(12.0, _Bneg((Bl, Bh))))
    SBw = neg(mul(HSQRT3, mul(isqrt(X), e_range(Rr))))
    Sww = g_range(Rr)
    if with_H:
        Sww = add(Sww, (12.0, 12.0))
    return SBB, SBw, Sww


def big_center(Bs, ws, with_H):
    """(value, d/dB, d/dw) of V (or H) at the float point (B*, w*), w* >= 0."""
    w2 = (max(0.0, dn(ws * ws)), up(ws * ws))
    T2 = (dn(3.0 * w2[0]), up(3.0 * w2[1]))
    xs = xbig(Bs, T2[0], T2[1])
    if xs[0] <= 0.0:
        return None
    Bsi = (Bs, Bs)
    v0, vB, vw = V_iv(Bsi, xs), VB_iv(Bsi, xs), Vw_big_iv(Bsi, xs)
    if with_H:
        v0 = add(add(scal(2.0, _Bneg3(Bsi)), scal(2.0, T2)), v0)
        vB = sub(vB, scal(6.0, sqr(_Bneg(Bsi))))
        vw = add(vw, scal(12.0, (ws, ws)))
    return v0, vB, vw


def second_order(R, Bs, ws, mom, with_H):
    """Second-order enclosure (None if the expansion point has x = 0)."""
    c = big_center(Bs, ws, with_H)
    if c is None:
        return None
    v0, vB, vw = c
    SBB, SBw, Sww = big_hessian(R, with_H)
    m, E1B, E1u, QB, Qu, QBu = mom
    lin = add(add(mul(v0, m), mul(vB, E1B)), scal(float(R.s), mul(vw, E1u)))
    return add(lin, _quad(SBB, SBw, Sww, QB, Qu, QBu, R.s))


# ================================================================ 3D box integrals (scaled coordinates, fixed k)
def _box3_common(box, Ma, Mb, Mc):
    (a0, a1), (b0, b1), (c0, c1) = box
    A, Bm, C = Ma.get(a0, a1), Mb.get(b0, b1), Mc.get(c0, c1)
    R = Rect(*box_geometry(box))
    return A, Bm, C, R


def big_box3(box, Ma, Mb, Mc, with_H=False, second=True, parts=False):
    """Enclosure of int_box V dmu (with_H: of H) over a 3D box of scaled coordinates."""
    A, Bm, C, R = _box3_common(box, Ma, Mb, Mc)
    m0 = mul(mul(A[0], Bm[0]), C[0])
    I1 = mul(m0, H_range(R) if with_H else V_range(R))
    I2 = None
    if second and R.s != 0:
        (a0, a1), (b0, b1), (c0, c1) = box
        Bs, ws = _expansion_point(0.5 * (a0 + a1), 0.5 * (b0 + b1), 0.5 * (c0 + c1), R.Bl, R.Bh, R.s, R.wl, R.wh)
        I2 = second_order(R, Bs, ws, taylor_moments3(A, Bm, C, Bs, R.s * ws), with_H)
    I = I1 if I2 is None else _intersect(I1, I2, 'H' if with_H else 'V')
    return (I, I1, I2) if parts else I


def H2_point(B, T):
    """H_2(B, T) = 2|B|^3 + 2T + V(B, T; middle root) on {B < 0, T < |B|^3/2}, 0 outside; near the boundary
    0 <= H_2(B, T) <= H_2(B, T') for T' <= T inside (H_2 is non-increasing in T)."""
    if B >= 0.0:
        return (0.0, 0.0)
    half = half_cube(B)
    if T >= half[1]:
        return (0.0, 0.0)
    if T > half[0]:
        return (0.0, H2_point(B, dn(dn(half[0]) * (1.0 - 1e-12)))[1])
    v = add(add(scal(2.0, pw((-B, -B), 3)), (dn(2 * T), up(2 * T))), V_iv((B, B), xmid(B, T)))
    return (max(0.0, v[0]), max(0.0, v[1]))


def _H2_center(Bs, ws, A, Bm, C, s):
    w2 = (max(0.0, dn(ws * ws)), up(ws * ws))
    T2 = (dn(3.0 * w2[0]), up(3.0 * w2[1]))
    if Bs < 0.0 and T2[1] < half_cube(Bs)[0]:
        xs = xmid(Bs, T2[0], T2[1])
        Bsi = (Bs, Bs)
        h0 = add(add(scal(-2.0, pw(Bsi, 3)), scal(2.0, T2)), V_iv(Bsi, xs))
        hB = add(scal(-6.0, sqr(Bsi)), VB_iv(Bsi, xs))
        vw = neg(Vw_big_iv(Bsi, xs))                     # middle root: opposite sign
        if MUTANT == 'mid-branch':
            vw = neg(vw)
        hw = add(scal(12.0, (ws, ws)), vw)
        return h0, hB, hw
    if Bs >= 0.0 or T2[0] > half_cube(Bs)[1]:
        return (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)        # outside the support: value and gradient 0
    return None


def H2_box3(box, Ma, Mb, Mc, second=True, parts=False):
    """Enclosure of int_box H_2 dmu.  Inside the support the middle root x and r = B/x are non-increasing in B and T,
    r in [-2, -1]; on boxes meeting the support boundary the zero extension of H_2 is C^1 with zero value and gradient
    on {T = |B|^3/2} and piecewise C^2, so the Taylor remainder holds with Hessian ranges hulled with 0, the ranges being
    taken over rectangle and support, where |B|/2 <= x <= x(Bl, Tl) and r in [-2, r(Bl, Tl)]."""
    (a0, a1), (b0, b1), (c0, c1) = box
    Bl, Bh, ul, uh = box_geometry(box)
    zero = ((0.0, 0.0),) * 3
    if Bl >= 0.0:
        return zero if parts else (0.0, 0.0)
    s, wl, wh, Tl, Th = wT(ul, uh)
    if Tl >= half_cube(Bl)[1]:
        return zero if parts else (0.0, 0.0)
    A, Bm, C = Ma.get(a0, a1), Mb.get(b0, b1), Mc.get(c0, c1)
    m0 = mul(mul(A[0], Bm[0]), C[0])
    inside = Bh < 0.0 and Th < half_cube(Bh)[0]
    I2 = None
    if inside:
        xLL, xHH = xmid(Bl, Tl), xmid(Bh, Th)
        hmin = add(add(scal(2.0, pw((-Bh, -Bh), 3)), (dn(2 * Th), up(2 * Th))), V_iv((Bh, Bh), xHH))[0]
        hmax = add(add(scal(2.0, pw((-Bl, -Bl), 3)), (dn(2 * Tl), up(2 * Tl))), V_iv((Bl, Bl), xLL))[1]
        I1 = mul(m0, (max(0.0, hmin), max(0.0, hmax)))
        X = (xHH[0], xLL[1])
        Rr = (max(-2.0, div((Bh, Bh), xHH)[0]), min(-1.0, div((Bl, Bl), xLL)[1]))
        Bhe = Bh
    else:
        I1 = mul(m0, (H2_point(Bh, Th)[0], H2_point(Bl, Tl)[1]))
        if Tl < half_cube(Bl)[0]:
            Bhe = min(Bh, 0.0)
            xLL = xmid(Bl, Tl)
            X = (max(0.0, -Bhe / 2.0), xLL[1])
            Rr = (-2.0, min(-1.0, div((Bl, Bl), xLL)[1]))
        else:
            X = None
    if second and s != 0 and X is not None:
        SBB = add(scal(-12.0, (Bl, Bhe)), mul(X, p_range(Rr)))
        SBw = mul(HSQRT3, mul(isqrt(X), e_range(Rr)))
        Sww = add((12.0, 12.0), g_range(Rr))
        if not inside:
            SBB, SBw, Sww = _hull0(SBB), _hull0(SBw), _hull0(Sww)
        Bs, ws = _expansion_point(0.5 * (a0 + a1), 0.5 * (b0 + b1), 0.5 * (c0 + c1), Bl, Bh, s, wl, wh)
        cen = _H2_center(Bs, ws, A, Bm, C, s)
        if cen is not None:
            h0, hB, hw = cen
            m, E1B, E1u, QB, Qu, QBu = taylor_moments3(A, Bm, C, Bs, s * ws)
            lin = add(add(mul(h0, m), mul(hB, E1B)), scal(float(s), mul(hw, E1u)))
            I2 = add(lin, _quad(SBB, SBw, Sww, QB, Qu, QBu, s))
    I = I1 if I2 is None else _intersect(I1, I2, 'H2')
    return (I, I1, I2) if parts else I


# ================================================================ 4D: the gap mark k as a box coordinate
K_LO, K_HI = 0.5, 2.0
PMIN, PMAX = -6, 2
KLEVEL = 12                          # elementary dyadic cells of [1/2, 2]: width 3 * 2^-13


def _cbrt_iv(x):
    """Enclosure of x^(1/3) for a float x > 0."""
    c = x ** (1.0 / 3.0)
    lo, hi = c, c
    while pw((lo, lo), 3)[1] > x:
        lo = dn(lo)
    while pw((hi, hi), 3)[0] < x:
        hi = up(hi)
    return (lo, hi)


def kweights(k):
    """f_p(k) = 3 k^(1/3) k^(p/2) e^(-12 k^2), p = PMIN..PMAX, at a float k > 0  (3k^2 x e^(-12k^2) k^(-5/3) x k^(p/2))."""
    third = _cbrt_iv(k)
    if MUTANT == 'k-weight':
        third = (1.0, 1.0)
    base = mul(scal(3.0, third), exp_neg((dn(12.0 * dn(k * k)), up(12.0 * up(k * k)))))
    sk = isqrt((k, k))
    isk = div((1.0, 1.0), sk)
    out = {}
    v = base
    for p in range(0, PMAX + 1):
        out[p] = v
        v = mul(v, sk)
    v = mul(base, isk)
    for p in range(-1, PMIN - 1, -1):
        out[p] = v
        v = mul(v, isk)
    return out


def elementary_kmoments(nsub=24):
    """K_p = int f_p over each elementary cell.  Every f_p is convex on [1/2, 2]: f''/f = (24k - q/k)^2 - q/k^2 - 24 with
    q = 1/3 + p/2 in [-8/3, 4/3] is >= 87 - 16/3 - 24 > 0 (q >= 0) and >= 144 - 24 > 0 (q < 0).  Hence on every sub-cell
    h f(mid) <= int f <= h (f(l) + f(r))/2.  All cell and sub-cell ends are exact dyadic floats."""
    n = 2 ** KLEVEL
    width = (K_HI - K_LO) / n
    cells = []
    prev = kweights(K_LO)
    for i in range(n):
        k0 = K_LO + width * i
        acc = {p: (0.0, 0.0) for p in range(PMIN, PMAX + 1)}
        for j in range(nsub):
            l = k0 + width * j / nsub
            r = k0 + width * (j + 1) / nsub
            h = (dn(r - l), up(r - l))
            mid = kweights(0.5 * (l + r))
            fr = kweights(r)
            for p in acc:
                lo = mul(h, mid[p])[0]
                hi = mul(h, scal(0.5, add(prev[p], fr[p])))[1]
                acc[p] = (dn(acc[p][0] + lo), up(acc[p][1] + hi))
            prev = fr
        cells.append(acc)
    return cells


class KMoments:
    """K_p on dyadic k-cells (unions of elementary cells), cached."""
    def __init__(self, elem):
        self.elem, self.c = elem, {}
        self.width = (K_HI - K_LO) / len(elem)

    def get(self, k0, k1):
        key = (k0, k1)
        r = self.c.get(key)
        if r is None:
            i0 = round((k0 - K_LO) / self.width)
            i1 = round((k1 - K_LO) / self.width)
            if K_LO + i0 * self.width != k0 or K_LO + i1 * self.width != k1:
                raise ValueError('k-cell is not a union of elementary cells: %r' % (key,))
            r = {}
            for p in range(PMIN, PMAX + 1):
                lo = hi = 0.0
                for i in range(i0, i1):
                    e = self.elem[i][p]
                    lo, hi = dn(lo + e[0]), up(hi + e[1])
                r[p] = (lo, hi)
            self.c[key] = r
        return r


def _integrate4(terms, A, Bm, C, K):
    acc = (0.0, 0.0)
    for (cf, i, j, l, p) in terms:
        acc = add(acc, mul(cf, mul(mul(A[i], Bm[j]), mul(C[l], K[p]))))
    return acc


def _prod4(t1, t2):
    out = {}
    for (c1, i1, j1, l1, p1) in t1:
        for (c2, i2, j2, l2, p2) in t2:
            key = (i1 + i2, j1 + j2, l1 + l2, p1 + p2)
            c = mul(c1, c2)
            out[key] = add(out[key], c) if key in out else c
    return [(c,) + key for key, c in sorted(out.items())]


_C12 = div((1.0, 1.0), (12.0, 12.0))
_C72 = div((1.0, 1.0), (72.0, 72.0))


def taylor_moments4(A, Bm, C, K, Bs, us):
    """The six Taylor moments over a 4D box against W(k) dk x Gaussian, in the original coordinates:
    dB = beta - a^2 k^-1/12 - Bs,  du = c k^(1/2) - a beta k^(-1/2)/4 + a^3 k^(-3/2)/72 - us
    (terms: coefficient, powers of a, beta, c, and p for k^(p/2))."""
    dB = [((1.0, 1.0), 0, 1, 0, 0), (neg(_C12), 2, 0, 0, -2), ((-Bs, -Bs), 0, 0, 0, 0)]
    du = [((1.0, 1.0), 0, 0, 1, 1), ((-0.25, -0.25), 1, 1, 0, -1), (_C72, 3, 0, 0, -3), ((-us, -us), 0, 0, 0, 0)]
    m = _integrate4([((1.0, 1.0), 0, 0, 0, 0)], A, Bm, C, K)
    E1B = _integrate4(dB, A, Bm, C, K)
    E1u = _integrate4(du, A, Bm, C, K)
    QB = _integrate4(_prod4(dB, dB), A, Bm, C, K)
    Qu = _integrate4(_prod4(du, du), A, Bm, C, K)
    QBu = _integrate4(_prod4(dB, du), A, Bm, C, K)
    return m, E1B, E1u, _nonneg(QB), _nonneg(Qu), QBu


def _scaled_range(x0, x1, f0, f1):
    p = (x0 * f0, x0 * f1, x1 * f0, x1 * f1)
    return dn(min(p)), up(max(p))


def scaled_box(box):
    """Outer box of the scaled coordinates (a/sqrt k, beta, sqrt(k) c) over a 4D box (a, beta, c, k)."""
    (a0, a1), (b0, b1), (c0, c1), (k0, k1) = box
    sk0, sk1 = isqrt((k0, k0)), isqrt((k1, k1))
    isk = (div((1.0, 1.0), sk1)[0], div((1.0, 1.0), sk0)[1])
    sk = (sk0[0], sk1[1])
    return (_scaled_range(a0, a1, isk[0], isk[1]), (b0, b1), _scaled_range(c0, c1, sk[0], sk[1]))


def H_box4(box, Ma, Mb, Mc, Km, second=True, parts=False):
    """Enclosure of int_box W(k) H dmu dk over a 4D box (a, beta, c, k), W(k) = 3 k^(1/3) e^(-12k^2)."""
    (a0, a1), (b0, b1), (c0, c1), (k0, k1) = box
    A, Bm, C, K = Ma.get(a0, a1), Mb.get(b0, b1), Mc.get(c0, c1), Km.get(k0, k1)
    R = Rect(*box_geometry(scaled_box(box)))
    m0 = mul(mul(A[0], Bm[0]), mul(C[0], K[0]))
    I1 = mul(m0, H_range(R))
    I2 = None
    if second and R.s != 0:
        ac, bc, cc, kc = 0.5 * (a0 + a1), 0.5 * (b0 + b1), 0.5 * (c0 + c1), 0.5 * (k0 + k1)
        skc = math.sqrt(kc)
        Bs, ws = _expansion_point(ac / skc, bc, cc * skc, R.Bl, R.Bh, R.s, R.wl, R.wh)
        I2 = second_order(R, Bs, ws, taylor_moments4(A, Bm, C, K, Bs, R.s * ws), True)
    I = I1 if I2 is None else _intersect(I1, I2, 'H (4D)')
    return (I, I1, I2) if parts else I
