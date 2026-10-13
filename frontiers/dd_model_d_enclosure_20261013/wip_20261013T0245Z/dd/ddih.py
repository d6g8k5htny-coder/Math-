"""Interval automatic differentiation to second order over a box ("interval Hessian"): each object carries
cell-wide interval enclosures of the value, the gradient (n components) and the Hessian (n(n+1)/2 components).
Rules are the pointwise identities, so cell-wide enclosures of the inputs give cell-wide enclosures of the outputs.
Same interface as the Taylor models of ddcore (so the integrand code is shared)."""
import math
from decimal import Decimal as Dec
from fractions import Fraction as Fr
import ddcore as C
from ddcore import q, add, sub, mul, div, neg, smul, sq, ipow, iexp, isqrt, ZERO, ONE, TWO

class IHSpace:
    def __init__(self, nvars, h):
        self.n = nvars
        self.h = [q(x) for x in h]
        self.pairs = [(i, j) for i in range(nvars) for j in range(i, nvars)]
        self.pidx = {p: k for k, p in enumerate(self.pairs)}
        self.zero = (ZERO, ZERO)
        self.cellwide = True; self.p = 2
    def var(self, i):
        g = [self.zero] * self.n; g[i] = (ONE, ONE)
        # value range over the box is [-h, h] about the centre; the caller adds the centre
        return IH(self, (neg(self.h[i])[0], self.h[i][1]), g, [self.zero] * len(self.pairs))
    def const(self, a):
        return IH(self, q(a), [self.zero] * self.n, [self.zero] * len(self.pairs))

class IH:
    __slots__ = ('S', 'v', 'g', 'H')
    def __init__(self, S, v, g, H):
        self.S = S; self.v = v; self.g = g; self.H = H
    # interface shims
    def range(self): return self.v
    def const_term(self): return self.v
    @property
    def r(self): return (ZERO, ZERO)
    def __add__(self, o):
        S = self.S
        if not isinstance(o, IH): o = S.const(o)
        return IH(S, add(self.v, o.v), [add(a, b) for a, b in zip(self.g, o.g)], [add(a, b) for a, b in zip(self.H, o.H)])
    __radd__ = __add__
    def __neg__(self):
        return IH(self.S, neg(self.v), [neg(a) for a in self.g], [neg(a) for a in self.H])
    def __sub__(self, o):
        return self.__add__(-(o if isinstance(o, IH) else self.S.const(o)))
    def __rsub__(self, o):
        return (-self).__add__(o)
    def scale(self, a):
        a = q(a)
        return IH(self.S, mul(a, self.v), [mul(a, x) for x in self.g], [mul(a, x) for x in self.H])
    def __mul__(self, o):
        S = self.S
        if not isinstance(o, IH): return self.scale(o)
        v = mul(self.v, o.v)
        g = [add(mul(self.g[i], o.v), mul(self.v, o.g[i])) for i in range(S.n)]
        H = []
        for (i, j) in S.pairs:
            k = S.pidx[(i, j)]
            t = add(mul(self.H[k], o.v), mul(self.v, o.H[k]))
            t = add(t, add(mul(self.g[i], o.g[j]), mul(self.g[j], o.g[i])))
            H.append(t)
        return IH(S, v, g, H)
    __rmul__ = __mul__
    def __truediv__(self, o):
        if isinstance(o, IH): return self * o.recip()
        return self.scale(C.recip(q(o)))
    def __rtruediv__(self, o):
        return self.recip().scale(q(o))
    def _compose(self, f0, f1, f2):
        """F(self) with F(v), F'(v), F''(v) given as intervals over the value range."""
        S = self.S
        v = f0
        g = [mul(f1, x) for x in self.g]
        H = []
        for (i, j) in S.pairs:
            k = S.pidx[(i, j)]
            H.append(add(mul(f1, self.H[k]), mul(f2, mul(self.g[i], self.g[j]))))
        return IH(S, v, g, H)
    def exp(self):
        e = iexp(self.v)
        return self._compose(e, e, e)
    def recip(self):
        inv = C.recip(self.v)
        return self._compose(inv, neg(sq(inv)), smul(TWO, mul(inv, sq(inv))))
    def sqrt(self):
        s = isqrt(self.v)
        inv_s = C.recip(s)
        return self._compose(s, smul(Dec('0.5'), inv_s), smul(Dec('-0.25'), mul(inv_s, C.recip(self.v))))
    def ln(self):
        inv = C.recip(self.v)
        return self._compose(C.iln(self.v), inv, neg(sq(inv)))
    def erf(self):
        e = iexp(neg(sq(self.v)))
        two_over_sqrtpi = div((TWO, TWO), C.SQRTPI)
        d1 = mul(two_over_sqrtpi, e)
        d2 = mul(d1, smul(Dec(-2), self.v))
        return self._compose(C.ierf(self.v), d1, d2)
    def erfc(self):
        return 1 - self.erf()
    def add_remainder(self, r):
        """PLACEHOLDER: value-only inflation (derivative bounds of the series remainder are added in ddmom)."""
        return IH(self.S, add(self.v, (-r, r)), self.g, self.H)
    def hess_bounds(self):
        """dict pair -> interval enclosure of the second partial derivative over the box."""
        return {p: self.H[self.S.pidx[p]] for p in self.S.pairs}
