"""Gauss-Legendre rules with rigorous node and weight enclosures, and the Bernstein-ellipse error bound used by
certificate.py (CL-CU-CUSP-COEFFICIENT-20261001).

Nodes.  P_n is evaluated exactly in rational arithmetic by (k+1) P_(k+1) = (2k+1) x P_k - k P_(k-1).  A floating
Newton root is refined by exact Newton steps on the grid 2^-200 to a rational r, and accepted only when P_n has
strictly opposite signs at r - 2^-150 and r + 2^-150.  The n enclosing intervals are
disjoint, so they contain all n roots, one each.  The rule is symmetric, so only the roots in (0, 1) are verified; the
others are their negatives (and 0 itself when n is odd).

Weights.  At a root, (1 - x^2) P_n'(x) = n P_(n-1)(x), so w = 2 (1 - x^2)/(n P_(n-1)(x))^2.  It is enclosed over the
node interval by its exact midpoint value plus a Lipschitz bound (_weight).

Error bound (Lemma Q of NOTE.md).  Let f be analytic in the open Bernstein ellipse E_rho of [-1, 1] and bounded by M
there.  Then its Chebyshev coefficients satisfy |a_k| <= 2 M rho^(-k).  The n-point rule is exact up to degree 2n - 1
and is exact on odd T_k by symmetry.  For even k, |int T_k| <= 2/(k^2 - 1) and |Q_n(T_k)| <= sum w = 2.  Hence
    |int f - Q_n f| <= 4 M (1 + 1/(4n^2 - 1)) rho^(-2n) / (1 - rho^(-2)),
and on [a, b] the right side is multiplied by h = (b - a)/2, for the ellipse c + h E_rho."""
import math
from fractions import Fraction as Fr
from ia import dn, up, add, sub, mul, div, scal, divc, sqr, from_frac

_CACHE = {}


def _legendre_exact(x, n):
    """(P_(n-1)(x), P_n(x)) in exact rational arithmetic at a rational x, n >= 1."""
    p0 = Fr(1)
    p1 = x
    for k in range(1, n):
        p0, p1 = p1, ((2 * k + 1) * x * p1 - k * p0) / (k + 1)
    return p0, p1


def _legendre_float(x, n):
    p0, p1 = 1.0, x
    for k in range(1, n):
        p0, p1 = p1, ((2 * k + 1) * x * p1 - k * p0) / (k + 1)
    return p0, p1


def _weight(lo, hi, n):
    """Enclosure of w(x) = 2 (1 - x^2)/(n P_(n-1)(x))^2 over the rational interval [lo, hi]: exact value at the
    midpoint plus a Lipschitz bound.  On [-1, 1], |P_(n-1)'| <= P_(n-1)'(1) = n (n - 1)/2, so |P_(n-1)| >= m on
    [lo, hi] with m = min(|P_(n-1)(lo)|, |P_(n-1)(hi)|) - n (n - 1)/2 (hi - lo), and |w'| <= (4/n^2)(1/m^2 + (n (n - 1)/2)/m^3)."""
    D1 = Fr(n * (n - 1), 2)
    M0 = (lo + hi) / 2
    plo = abs(_legendre_exact(lo, n)[0])
    phi = abs(_legendre_exact(hi, n)[0])
    m = min(plo, phi) - D1 * (hi - lo)
    if m <= 0:
        raise RuntimeError('Gauss-Legendre weight: P_(n-1) not bounded away from 0')
    pm = _legendre_exact(M0, n)[0]
    wm = 2 * (1 - M0 * M0) / (n * n * pm * pm)
    lip = Fr(4, n * n) * (1 / (m * m) + D1 / (m * m * m))
    err = lip * (hi - lo) / 2
    return (from_frac(wm - err)[0], from_frac(wm + err)[1])


_GRID = Fr(1, 2 ** 200)
_EPS = Fr(1, 2 ** 150)


def _snap(r):
    """Round the rational r to the grid 2^-200 (keeps the exact Newton iterates small)."""
    return Fr(round(r / _GRID)) * _GRID


def rule(n):
    """Nodes and weights on [-1, 1] as lists of intervals, ascending.  Each root is refined by exact rational Newton
    steps on the grid 2^-200, then certified by a strict sign change of P_n at r -+ 2^-150 (exact arithmetic); the
    node interval is the outward float hull of [r - 2^-150, r + 2^-150]."""
    if n in _CACHE:
        return _CACHE[n]
    pos = []
    for i in range(1, n // 2 + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            pm1, pn = _legendre_float(x, n)
            dp = n * (x * pn - pm1) / (x * x - 1.0)
            dx = pn / dp
            x -= dx
            if abs(dx) < 1e-17:
                break
        r = _snap(Fr(x))
        for _ in range(4):
            pm1, pn = _legendre_exact(r, n)
            dp = n * (r * pn - pm1) / (r * r - 1)
            r = _snap(r - pn / dp)
        lo, hi = r - _EPS, r + _EPS
        if not _legendre_exact(lo, n)[1] * _legendre_exact(hi, n)[1] < 0:
            raise RuntimeError('Gauss-Legendre node %d of %d not verified' % (i, n))
        pos.append(((from_frac(lo)[0], from_frac(hi)[1]), _weight(lo, hi, n)))
    pos.sort(key=lambda e: e[0][0])
    for j in range(1, len(pos)):
        if not pos[j - 1][0][1] < pos[j][0][0]:
            raise RuntimeError('Gauss-Legendre node enclosures overlap')
    if pos and not pos[0][0][0] > 0.0:
        raise RuntimeError('Gauss-Legendre positive node enclosure meets 0')
    nodes, weights = [], []
    for X, w in reversed(pos):
        nodes.append((-X[1], -X[0]))
        weights.append(w)
    if n % 2:
        pm1 = _legendre_exact(Fr(0), n)[0]
        w0 = Fr(2, n * n) / (pm1 * pm1)
        nodes.append((0.0, 0.0))
        weights.append(from_frac(w0))
    for X, w in pos:
        nodes.append(X)
        weights.append(w)
    _CACHE[n] = (nodes, weights)
    return nodes, weights


def panel(n, a, b):
    """Rule on [a, b] (floats): nodes c + h x, weights h w, as intervals."""
    nodes, weights = rule(n)
    A, B = (a, a), (b, b)
    c = scal(0.5, add(A, B))
    h = scal(0.5, sub(B, A))
    return [add(c, mul(h, x)) for x in nodes], [mul(h, w) for w in weights]


def error_bound(n, rho, M, h):
    """Upper bound of |int_[a,b] f - Q_n f| for |f| <= M on the ellipse c + h E_rho (h = (b - a)/2, rho > 1)."""
    num = 4.0 * M * (1.0 + 1.0 / (4 * n * n - 1)) * rho ** (-2 * n)
    return up(up(num / (1.0 - rho ** -2)) * h * (1.0 + 1e-12))


def ellipse_slabs(a, b, rho, m):
    """m complex boxes (re, im) covering the closed ellipse c + h E_rho of [a, b]: the real extent
    c +- h (rho + 1/rho)/2 is cut into m slabs, and over each slab the imaginary half-height is the ellipse's at the slab
    point nearest to c."""
    c = 0.5 * (a + b)
    h = 0.5 * (b - a)
    ax = h * (rho + 1.0 / rho) / 2.0 * (1.0 + 1e-12)
    by = h * (rho - 1.0 / rho) / 2.0 * (1.0 + 1e-12)
    out = []
    for j in range(m):
        x0 = c - ax + 2.0 * ax * j / m
        x1 = c - ax + 2.0 * ax * (j + 1) / m
        x0, x1 = dn(x0), up(x1)
        near = 0.0 if x0 <= c <= x1 else min(abs(x0 - c), abs(x1 - c))
        frac = max(0.0, 1.0 - (near / ax) ** 2)
        yh = up(by * math.sqrt(frac) * (1.0 + 1e-12))
        out.append(((x0, x1), (-yh, yh)))
    return out
