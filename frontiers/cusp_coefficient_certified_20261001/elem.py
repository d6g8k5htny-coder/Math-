"""Real-interval elementary functions for CL-CU-CUSP-COEFFICIENT-20261001, built on ia.py (its conventions apply: an
interval is a pair (lo, hi) of floats, every operation is rounded outward).

Point enclosures come from series with explicit remainder bounds; the only constants are pi and ln 2 of ia.py.
Interval extensions use the monotonicity stated with each function; sin and cos take their endpoint values and +-1
at every critical point that may lie inside the interval.

    exp, log (t > 0), log1p (t > -1), atan, sin, cos, sinh, cosh,
    E1(x) = (e^x - 1)/x,   L(x) = log(1 + x)/x,   A(x) = atan(x)/x,   Sinc(x) = sin(x)/x   (each = 1 at x = 0).

E1 is increasing on R, L is decreasing on (-1, oo), A is even and decreasing in |x|, Sinc is even and decreasing on
[0, pi].  The four kernels are analytic, so the integrands of certificate.py never divide by a small quantity."""
import math
from ia import (dn, up, add, sub, neg, mul, div, scal, divc, sqr, isqrt, hull, absmax, PI, LN2, exp_neg)

ONE = (1.0, 1.0)
HALF_PI = scal(0.5, PI)


def _with_err(s, e):
    """s widened by the nonnegative error bound e."""
    return (dn(s[0] - e), up(s[1] + e))


# ---------------------------------------------------------------- exp
def exp_pt(t):
    """Enclosure of e^t for a float t with t <= 700."""
    if t <= 0.0:
        return exp_neg((-t, -t))
    if t > 700.0:
        raise OverflowError('exp argument too large: %r' % t)
    return div(ONE, exp_neg((t, t)))


def exp_iv(x):
    return (exp_pt(x[0])[0], exp_pt(x[1])[1])


# ---------------------------------------------------------------- log, log1p via atanh
def _atanh_series(u, K=26):
    """atanh(u) = sum_k u^(2k+1)/(2k+1) for an interval u with |u| <= 1/3.  The tail after K terms is at most
    m^(2K+3)/((2K+3)(1 - m^2)) with m = max|u|; it is added with a safety factor 2."""
    m = absmax(u)
    if m > 0.34:
        raise ValueError('atanh series outside its range')
    u2 = sqr(u)
    term = u
    s = u
    for k in range(1, K + 1):
        term = mul(term, u2)
        s = add(s, divc(term, float(2 * k + 1)))
    tail = 2.0 * m ** (2 * K + 3) / ((2 * K + 3) * (1.0 - m * m))
    return _with_err(s, tail)


def log_pt(t):
    """Enclosure of log t for a float t > 0: t = m 2^e with m in [1/sqrt2, sqrt2), log m = 2 atanh((m-1)/(m+1))."""
    if not t > 0.0:
        raise ValueError('log of a nonpositive number')
    m, e = math.frexp(t)
    if m < 0.7071067811865476:
        m *= 2.0
        e -= 1
    M = (m, m)
    u = div(sub(M, ONE), add(M, ONE))
    r = scal(2.0, _atanh_series(u))
    return add(r, mul((float(e), float(e)), LN2))


def log_iv(x):
    return (log_pt(x[0])[0], log_pt(x[1])[1])


def log1p_pt(t):
    """Enclosure of log(1 + t) for a float t > -1, with full relative accuracy near 0 (2 atanh(t/(2 + t)))."""
    if not t > -1.0:
        raise ValueError('log1p argument <= -1')
    if abs(t) <= 0.5:
        T = (t, t)
        u = div(T, add((2.0, 2.0), T))
        return scal(2.0, _atanh_series(u))
    return log_iv((dn(1.0 + t), up(1.0 + t)))


def log1p_iv(x):
    return (log1p_pt(x[0])[0], log1p_pt(x[1])[1])


# ---------------------------------------------------------------- atan
def _atan_small(y, K=14):
    """Alternating series for atan on an interval y within [0, 0.21]: the error after K terms is at most the next
    term."""
    y2 = sqr(y)
    term = y
    s = y
    for k in range(1, K + 1):
        term = mul(term, y2)
        t = divc(term, float(2 * k + 1))
        s = sub(s, t) if k % 2 else add(s, t)
    m = absmax(y)
    nxt = m ** (2 * K + 3) / (2 * K + 3)
    return _with_err(s, 2.0 * nxt)


def atan_pt(t):
    """Enclosure of atan t for a float t: odd symmetry, atan t = pi/2 - atan(1/t) for t > 1, and two halvings
    atan x = 2 atan(x/(1 + sqrt(1 + x^2))) bringing the argument below tan(pi/16) < 0.199."""
    if t < 0.0:
        return neg(atan_pt(-t))
    if t == 0.0:
        return (0.0, 0.0)
    if t > 1.0:
        x = div(ONE, (t, t))
        return sub(HALF_PI, _atan_reduced(x))
    return _atan_reduced((t, t))


def _atan_reduced(x):
    y = x
    for _ in range(2):
        y = div(y, add(ONE, isqrt(add(ONE, sqr(y)))))
    if y[1] > 0.21:
        raise ValueError('atan reduction failed')
    return scal(4.0, _atan_small(y))


def atan_iv(x):
    return (atan_pt(x[0])[0], atan_pt(x[1])[1])


# ---------------------------------------------------------------- sin, cos
def _sincos_small(r, K=12):
    """sin and cos on an interval r within [-0.8, 0.8] by their alternating Taylor series; the error after K terms is
    at most the next term."""
    r2 = sqr(r)
    s = r
    c = ONE
    ts = r
    tc = ONE
    for k in range(1, K + 1):
        ts = divc(mul(ts, r2), float((2 * k) * (2 * k + 1)))
        tc = divc(mul(tc, r2), float((2 * k - 1) * (2 * k)))
        if k % 2:
            s = sub(s, ts)
            c = sub(c, tc)
        else:
            s = add(s, ts)
            c = add(c, tc)
    m = absmax(r)
    es = m ** (2 * K + 3) / math.factorial(2 * K + 3)
    ec = m ** (2 * K + 2) / math.factorial(2 * K + 2)
    return _with_err(s, 2.0 * es), _with_err(c, 2.0 * ec)


def sincos_pt(t):
    """Enclosures of (sin t, cos t) for a float t with |t| <= 1e6: t = k pi/2 + r with |r| <= pi/4 + 1e-9."""
    if abs(t) > 1e6:
        raise ValueError('sin/cos argument too large')
    k = round(t / 1.5707963267948966)
    r = sub((t, t), mul((float(k), float(k)), HALF_PI))
    if absmax(r) > 0.8:
        raise ValueError('sin/cos reduction failed')
    s, c = _sincos_small(r)
    q = k % 4
    if q == 0:
        return s, c
    if q == 1:
        return c, neg(s)
    if q == 2:
        return neg(s), neg(c)
    return neg(c), s


def _clip1(x):
    return (max(-1.0, x[0]), min(1.0, x[1]))


def _crit_inside(x, offset):
    """Integers k such that the enclosure of offset + k pi meets [x0, x1] (offset 0 or pi/2), with their parity."""
    out = []
    k0 = math.floor(x[0] / 3.141592653589793) - 2
    k1 = math.ceil(x[1] / 3.141592653589793) + 2
    for k in range(k0, k1 + 1):
        c = add(offset, mul((float(k), float(k)), PI))
        if c[0] <= x[1] and c[1] >= x[0]:
            out.append(k)
    return out


def sin_iv(x):
    """Range of sin over an interval: the endpoint values, together with +-1 at every pi/2 + k pi that may lie
    inside (decided against the interval enclosure of pi)."""
    if x[1] - x[0] >= 6.3:
        return (-1.0, 1.0)
    a, b = sincos_pt(x[0])[0], sincos_pt(x[1])[0]
    lo, hi = min(a[0], b[0]), max(a[1], b[1])
    for k in _crit_inside(x, HALF_PI):
        if k % 2 == 0:
            hi = 1.0
        else:
            lo = -1.0
    return _clip1((lo, hi))


def cos_iv(x):
    """Range of cos over an interval: the endpoint values, together with +-1 at every k pi that may lie inside."""
    if x[1] - x[0] >= 6.3:
        return (-1.0, 1.0)
    a, b = sincos_pt(x[0])[1], sincos_pt(x[1])[1]
    lo, hi = min(a[0], b[0]), max(a[1], b[1])
    for k in _crit_inside(x, (0.0, 0.0)):
        if k % 2 == 0:
            hi = 1.0
        else:
            lo = -1.0
    return _clip1((lo, hi))


# ---------------------------------------------------------------- sinh, cosh (used only in complex bounds)
def cosh_iv(x):
    """cosh is even and increasing in |x|."""
    lo = 0.0 if x[0] <= 0.0 <= x[1] else min(abs(x[0]), abs(x[1]))
    hi = max(abs(x[0]), abs(x[1]))
    def ch(t):
        return scal(0.5, add(exp_pt(t), exp_pt(-t)))
    return (ch(lo)[0], ch(hi)[1])


def sinh_iv(x):
    """sinh is odd and increasing."""
    def sh(t):
        return scal(0.5, sub(exp_pt(t), exp_pt(-t)))
    return (sh(x[0])[0], sh(x[1])[1])


# ---------------------------------------------------------------- the four analytic kernels
def E1_pt(t):
    """(e^t - 1)/t: series sum t^k/(k+1)! for |t| <= 1/2 (tail <= 2|t|^(K+1)/(K+2)!), else (e^t - 1)/t."""
    if abs(t) <= 0.5:
        T = (t, t)
        s = ONE
        term = ONE
        K = 18
        for k in range(1, K + 1):
            term = divc(mul(term, T), float(k + 1))
            s = add(s, term)
        err = 2.0 * abs(t) ** (K + 1) / math.factorial(K + 2)
        return _with_err(s, err)
    return div(sub(exp_pt(t), ONE), (t, t))


def E1_iv(x):
    """E1 is increasing."""
    return (E1_pt(x[0])[0], E1_pt(x[1])[1])


def L_pt(t):
    """log(1 + t)/t for t > -1 (1 at t = 0)."""
    if t == 0.0:
        return ONE
    return div(log1p_pt(t), (t, t))


def L_iv(x):
    """L is decreasing on (-1, oo)."""
    return (L_pt(x[1])[0], L_pt(x[0])[1])


def A_pt(t):
    """atan(t)/t (1 at t = 0)."""
    if t == 0.0:
        return ONE
    return div(atan_pt(t), (t, t))


def A_iv(x):
    """A is even and decreasing in |x|."""
    lo = 0.0 if x[0] <= 0.0 <= x[1] else min(abs(x[0]), abs(x[1]))
    hi = max(abs(x[0]), abs(x[1]))
    return (A_pt(hi)[0], A_pt(lo)[1])


def Sinc_pt(t):
    """sin(t)/t: alternating series for |t| <= 1/2, else sin(t)/t."""
    if abs(t) <= 0.5:
        T = (t, t)
        t2 = sqr(T)
        s = ONE
        term = ONE
        K = 10
        for k in range(1, K + 1):
            term = divc(mul(term, t2), float((2 * k) * (2 * k + 1)))
            s = sub(s, term) if k % 2 else add(s, term)
        err = 2.0 * abs(t) ** (2 * K + 2) / math.factorial(2 * K + 3)
        return _with_err(s, err)
    return div(sincos_pt(t)[0], (t, t))


def Sinc_iv(x):
    """Sinc is even and decreasing on [0, pi]; outside [-3, 3] it is sin(x)/x, and |Sinc| <= 1 everywhere with
    Sinc >= -0.2173 (its global minimum is -0.21723... at |x| = 4.4934...)."""
    hi = max(abs(x[0]), abs(x[1]))
    if hi <= 3.0:
        lo = 0.0 if x[0] <= 0.0 <= x[1] else min(abs(x[0]), abs(x[1]))
        return (Sinc_pt(hi)[0], Sinc_pt(lo)[1])
    if x[0] > 0.0 or x[1] < 0.0:
        return div(sin_iv(x), x)
    return (-0.2173, 1.0)
