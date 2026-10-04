"""Rational ball arithmetic and rational bounds for CL-C2-TORUS-TRANSFER-20261001 (NOTE.md section 2).  Standard library.

A ball B(c, r) is the set [c - r, c + r] with c, r rational, r >= 0.  Centers are carried EXACTLY: with every radius
zero the arithmetic is that of Fractions, so a ball pipeline reproduces the exact reference derivation in its centers.
Radii are rounded UP to dyadic rationals with RB significant bits after each operation, which only enlarges the ball.
Every operation returns a ball containing every result of the operation applied to members of the operand balls."""
from fractions import Fraction as Fr
import math

RB = 64


def rup(x):
    """smallest dyadic m / 2^e >= x with m < 2^RB (x >= 0 rational)"""
    x = Fr(x)
    if x <= 0:
        if x < 0:
            raise ValueError('negative radius')
        return Fr(0)
    e = RB - (x.numerator.bit_length() - x.denominator.bit_length())
    if e >= 0:
        m = -((-x.numerator << e) // x.denominator)
        return Fr(m, 1 << e)
    m = -((-x.numerator) // (x.denominator << -e))
    return Fr(m << -e)


class B:
    __slots__ = ('c', 'r')

    def __init__(self, c, r=0):
        self.c = Fr(c)
        self.r = rup(r)

    def __bool__(self):
        return bool(self.c) or bool(self.r)

    def __add__(self, o):
        if isinstance(o, B):
            return B(self.c + o.c, self.r + o.r)
        return B(self.c + o, self.r)
    __radd__ = __add__

    def __neg__(self):
        return B(-self.c, self.r)

    def __sub__(self, o):
        return self + (-o)

    def __rsub__(self, o):
        return (-self) + o

    def __mul__(self, o):
        if isinstance(o, B):
            return B(self.c * o.c, abs(self.c) * o.r + abs(o.c) * self.r + self.r * o.r)
        o = Fr(o)
        return B(self.c * o, abs(o) * self.r)
    __rmul__ = __mul__

    def inv(self):
        a = abs(self.c)
        if not a > self.r:
            raise ZeroDivisionError('ball contains 0')
        return B(1 / self.c, self.r / (a * (a - self.r)))

    def __truediv__(self, o):
        if isinstance(o, B):
            return self * o.inv()
        return self * (1 / Fr(o))

    def __rtruediv__(self, o):
        return self.inv() * o

    def mag(self):
        """upper bound of |x| on the ball"""
        return abs(self.c) + self.r

    def __repr__(self):
        return 'B(%s, %s)' % (float(self.c), float(self.r))


def center(x):
    return x.c if isinstance(x, B) else Fr(x)


def radius(x):
    return x.r if isinstance(x, B) else Fr(0)


def mag(x):
    return x.mag() if isinstance(x, B) else abs(Fr(x))


def nonzero_center(x):
    return center(x) != 0


# ---------------------------------------------------------------------------------------------- rational bounds
PI_UP = Fr(355, 113)            # pi < 355/113
PI_DN = Fr(333, 106)            # 333/106 < pi


def exp_up(x):
    """upper bound of e^x for rational x (exact partial sums: e^x >= sum_{j<=J} x^j/j! for x >= 0)"""
    x = Fr(x)
    if x <= 0:
        # e^-y = (e^(-y/n))^n, n = 2^m with y/n <= 1;  e^(-t) <= 1/sum_{j<=30} t^j/j!;  each squaring rounds up
        y = -x
        n, m = 1, 0
        while y / n > 1:
            n, m = 2 * n, m + 1
        t = y / n
        s, term = Fr(0), Fr(1)
        for j in range(31):
            s += term
            term = term * t / (j + 1)
        v = rup(1 / s)
        for _ in range(m):
            v = rup(v * v)
        return v
    # e^x = 1 / e^-x  <=  1 / (lower bound of e^-x);  e^-x >= alternating partial sum ending on a negative term ... use
    # e^x = (e^(x/n))^n with x/n <= 1/2 and e^t <= 1/(1 - t - t^2/2 ... ) avoided: e^t <= sum_{j<=J} t^j/j! + tail
    n = 1
    while x / n > Fr(1, 2):
        n *= 2
    t = x / n
    J = 30
    s, term = Fr(0), Fr(1)
    for j in range(J + 1):
        s += term
        term = term * t / (j + 1)
    s += 2 * term                  # tail sum_{j>J} t^j/j! <= 2 t^(J+1)/(J+1)! for t <= 1/2
    return rup(s ** n)


def exp_dn(x):
    """lower bound of e^x"""
    return 1 / exp_up(-Fr(x))


def isqrt_frac_up(x, bits=80):
    """upper bound of sqrt(x), x >= 0 rational"""
    x = Fr(x)
    if x == 0:
        return Fr(0)
    sc = 1 << (2 * bits)
    n = -((-x.numerator * sc) // x.denominator)
    s = math.isqrt(n)
    if s * s < n:
        s += 1
    return Fr(s, 1 << bits)


def isqrt_frac_dn(x, bits=80):
    x = Fr(x)
    sc = 1 << (2 * bits)
    n = (x.numerator * sc) // x.denominator
    return Fr(math.isqrt(n), 1 << bits)
