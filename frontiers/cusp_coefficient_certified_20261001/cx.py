"""Complex boxes for the analytic-continuation bounds of CL-CU-CUSP-COEFFICIENT-20261001.

A complex box is a pair (re, im) of real intervals (ia.py conventions) and stands for {x + iy : x in re, y in im}.
Every operation returns a box containing all results.  These boxes are used only to bound |f| on Bernstein ellipses;
the quadrature sums themselves are real-interval computations.

The four kernels have integral representations over tau in [0, 1]:

    E1(z) = int e^(tau z),   L(z) = int 1/(1 + tau z),   A(z) = int 1/(1 + tau^2 z^2),   Sinc(z) = int cos(tau z).

So each value lies in the convex hull of the integrand's range.  The box of the integrand with tau replaced by the
interval [0, 1] contains that range, and boxes are convex.  L and A are analytic where 1 + tau z or 1 + tau^2 z^2
stays away from 0 for all tau; cdiv raises if a denominator box meets 0.

For larger |z| these hulls are needlessly wide, so the closed forms are used instead:
- L(z) = Log(1 + z)/z when Re(1 + z) > 0 (principal Log, Arg(1 + z) = atan(Im/Re));
- A(z) = (pi/2 - A(1/z)/z)/z when Re z > 0, since atan z = pi/2 - atan(1/z) there;
- E1(z) = (e^z - 1)/z;
- Sinc(z) = sin z/z.
Each is analytic on the boxes where it is used.  Both forms enclose the same analytic function, so either is a valid
bound; the closed form is chosen when min |z| >= 1."""
from ia import dn, up, add, sub, neg, mul, div, scal, sqr, isqrt, PI
from elem import exp_iv, sin_iv, cos_iv, sinh_iv, cosh_iv, log_iv, atan_iv

ZERO = (0.0, 0.0)
ONE = (1.0, 1.0)
TAU = (0.0, 1.0)


def creal(x):
    return (x, ZERO)


def cadd(a, b):
    return (add(a[0], b[0]), add(a[1], b[1]))


def csub(a, b):
    return (sub(a[0], b[0]), sub(a[1], b[1]))


def cmul(a, b):
    return (sub(mul(a[0], b[0]), mul(a[1], b[1])), add(mul(a[0], b[1]), mul(a[1], b[0])))


def cscal(r, a):
    """real interval r times complex box a."""
    return (mul(r, a[0]), mul(r, a[1]))


def cabs2(a):
    return add(sqr(a[0]), sqr(a[1]))


def cdiv(a, b):
    d = cabs2(b)
    if d[0] <= 0.0:
        raise ZeroDivisionError('complex box division by a box that may contain 0')
    num = cmul(a, (b[0], neg(b[1])))
    return (div(num[0], d), div(num[1], d))


def cexp(a):
    m = exp_iv(a[0])
    return (mul(m, cos_iv(a[1])), mul(m, sin_iv(a[1])))


def ccos(a):
    """cos(x + iy) = cos x cosh y - i sin x sinh y."""
    return (mul(cos_iv(a[0]), cosh_iv(a[1])), neg(mul(sin_iv(a[0]), sinh_iv(a[1]))))


def _abs2_clamped(a):
    d = cabs2(a)
    return (max(0.0, d[0]), d[1])


def cabs_up(a):
    """An upper bound of |z| over the box."""
    return isqrt(_abs2_clamped(a))[1]


def cabs_dn(a):
    """A lower bound of |z| over the box."""
    return isqrt(_abs2_clamped(a))[0]


def cpow(a, n):
    """z^n for an integer n >= 1.  On a box in the right half-plane Re > 0, the polar form r^n (cos n theta,
    sin n theta) is used: r over [min |z|, max |z|], and theta = atan(y/x) over the box, which is the interval atan of
    the interval quotient.  This avoids the wrapping of repeated box products.  Elsewhere it uses repeated products."""
    if a[0][0] > 0.0:
        r = (cabs_dn(a), cabs_up(a))
        th = atan_iv(div(a[1], a[0]))
        rn = _pow_iv(r, n)
        nth = (dn(n * th[0]), up(n * th[1]))
        return (mul(rn, cos_iv(nth)), mul(rn, sin_iv(nth)))
    out = a
    for _ in range(n - 1):
        out = cmul(out, a)
    return out


def _pow_iv(r, n):
    """[r0^n, r1^n] for 0 <= r0 <= r1, outward."""
    lo = 1.0
    hi = 1.0
    for _ in range(n):
        lo = dn(lo * r[0])
        hi = up(hi * r[1])
    return (max(0.0, lo), hi)


def csin(a):
    """sin(x + iy) = sin x cosh y + i cos x sinh y."""
    return (mul(sin_iv(a[0]), cosh_iv(a[1])), mul(cos_iv(a[0]), sinh_iv(a[1])))


def clog_right(a):
    """Principal Log over a box in the right half-plane Re > 0."""
    if not a[0][0] > 0.0:
        raise ValueError('clog_right needs Re > 0')
    mod = scal(0.5, log_iv(cabs2(a)))
    ratio = div(a[1], a[0])
    return (mod, atan_iv(ratio))


def _big(z):
    return cabs_dn(z) >= 1.0


def E1c(z):
    if _big(z):
        return cdiv(csub(cexp(z), creal(ONE)), z)
    return cexp(cscal(TAU, z))


def Lc(z):
    if _big(z) and z[0][0] > -0.5:
        return cdiv(clog_right(cadd(creal(ONE), z)), z)
    return cdiv(creal(ONE), cadd(creal(ONE), cscal(TAU, z)))


def _Ac_hull(z):
    return cdiv(creal(ONE), cadd(creal(ONE), cscal(TAU, cmul(z, z))))


def Ac(z):
    if _big(z) and z[0][0] > 0.0:
        w = cdiv(creal(ONE), z)
        atan_w = cmul(w, _Ac_hull(w))
        return cdiv(csub(creal(scal(0.5, PI)), atan_w), z)
    return _Ac_hull(z)


def Sincc(z):
    if _big(z):
        return cdiv(csin(z), z)
    return ccos(cscal(TAU, z))
