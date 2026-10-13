"""Core for the certified two-sided enclosure of D: decimal interval arithmetic with directed rounding, rigorous
elementary functions (exp, ln, sqrt via the correctly rounded decimal functions widened by one ulp; erf and pi by
series with explicit remainders; Gamma by Stirling with the first-omitted-term bound), and Taylor models in n
variables over a centred box.  Python standard library only.
"""
import math
from decimal import Decimal as Dec, Context, ROUND_FLOOR, ROUND_CEILING, InvalidOperation, DivisionByZero, Overflow, localcontext
from fractions import Fraction as Fr

PREC = 30
TRAPS = [InvalidOperation, DivisionByZero, Overflow]
# the default (thread) context is used by operations without an explicit context (unary minus, abs, comparisons with
# rounding...); give it a precision above every working precision so that such operations are exact on our values
import decimal as _decimal
_decimal.getcontext().prec = 60
CD = Context(prec=PREC, rounding=ROUND_FLOOR, traps=TRAPS)
CU = Context(prec=PREC, rounding=ROUND_CEILING, traps=TRAPS)
CX = Context(prec=PREC + 25, rounding=ROUND_FLOOR, traps=TRAPS)   # extra precision for series
ZERO = Dec(0); ONE = Dec(1); TWO = Dec(2)

def set_precision(p):
    global PREC, CD, CU, CX
    PREC = p
    CD = Context(prec=p, rounding=ROUND_FLOOR, traps=TRAPS)
    CU = Context(prec=p, rounding=ROUND_CEILING, traps=TRAPS)
    CX = Context(prec=p + 25, rounding=ROUND_FLOOR, traps=TRAPS)

# ---------------------------------------------------------------- intervals: pairs (lo, hi) of Decimal
def q(x):
    """exact rational/int/str -> enclosing interval."""
    if isinstance(x, tuple): return x
    if isinstance(x, Fr):
        n, d = Dec(x.numerator), Dec(x.denominator)
        return (CD.divide(n, d), CU.divide(n, d))
    if isinstance(x, int): d = Dec(x); return (d, d)
    if isinstance(x, Dec): return (x, x)
    if isinstance(x, str): d = Dec(x); return (d, d)
    raise TypeError(type(x))

def add(a, b): return (CD.add(a[0], b[0]), CU.add(a[1], b[1]))
def sub(a, b): return (CD.subtract(a[0], b[1]), CU.subtract(a[1], b[0]))
def neg(a): return (a[1].copy_negate(), a[0].copy_negate())      # copy_negate: exact (unary minus would round in the default context)
def mul(a, b):
    al, ah = a; bl, bh = b
    if al >= 0:
        if bl >= 0: return (CD.multiply(al, bl), CU.multiply(ah, bh))
        if bh <= 0: return (CD.multiply(ah, bl), CU.multiply(al, bh))
        return (CD.multiply(ah, bl), CU.multiply(ah, bh))
    if ah <= 0:
        if bl >= 0: return (CD.multiply(al, bh), CU.multiply(ah, bl))
        if bh <= 0: return (CD.multiply(ah, bh), CU.multiply(al, bl))
        return (CD.multiply(al, bh), CU.multiply(al, bl))
    if bl >= 0: return (CD.multiply(al, bh), CU.multiply(ah, bh))
    if bh <= 0: return (CD.multiply(ah, bl), CU.multiply(al, bl))
    return (min(CD.multiply(al, bh), CD.multiply(ah, bl)), max(CU.multiply(al, bl), CU.multiply(ah, bh)))
def recip(a):
    al, ah = a
    if al <= 0 <= ah: raise ZeroDivisionError('interval contains zero')
    return (CD.divide(ONE, ah), CU.divide(ONE, al))
def div(a, b): return mul(a, recip(b))
def smul(c, a):
    """exact Decimal scalar times interval."""
    if c >= 0: return (CD.multiply(c, a[0]), CU.multiply(c, a[1]))
    return (CD.multiply(c, a[1]), CU.multiply(c, a[0]))
def sq(a):
    al, ah = a
    if al >= 0: return (CD.multiply(al, al), CU.multiply(ah, ah))
    if ah <= 0: return (CD.multiply(ah, ah), CU.multiply(al, al))
    m = max(-al, ah); return (ZERO, CU.multiply(m, m))
def ipow(a, n):
    if n == 0: return (ONE, ONE)
    if n == 1: return a
    if n % 2 == 0: return sq(ipow(a, n // 2))
    return mul(a, ipow(a, n - 1))
def mag(a): return max(a[0].copy_abs(), a[1].copy_abs())          # max |x| (exact)
def mig(a):                                   # min |x|
    if a[0] <= 0 <= a[1]: return ZERO
    return min(a[0].copy_abs(), a[1].copy_abs())
def hull(a, b): return (min(a[0], b[0]), max(a[1], b[1]))
def width(a): return CU.subtract(a[1], a[0])
def contains(a, x): return a[0] <= x <= a[1]
def iabs(a):
    if a[0] >= 0: return a
    if a[1] <= 0: return (a[1].copy_negate(), a[0].copy_negate())
    return (ZERO, mag(a))
def imax(a, b): return (max(a[0], b[0]), max(a[1], b[1]))
def imin(a, b): return (min(a[0], b[0]), min(a[1], b[1]))

def ulp(x):
    """one unit in the last place of x at precision PREC (x != 0)."""
    if x == 0: return Dec(1).scaleb(-PREC - 5)
    return Dec(1).scaleb(x.adjusted() - PREC + 1)

def widen(x):
    """enclose a correctly rounded (half-even) result by one ulp on each side."""
    u = ulp(x)
    return (CD.subtract(x, u), CU.add(x, u))

def iexp(a):
    lo = CD.exp(a[0]); hi = CU.exp(a[1])
    return (CD.subtract(lo, ulp(lo)), CU.add(hi, ulp(hi)))
def iln(a):
    if a[0] <= 0: raise ValueError('ln of non-positive interval')
    lo = CD.ln(a[0]); hi = CU.ln(a[1])
    return (CD.subtract(lo, ulp(lo)), CU.add(hi, ulp(hi)))
def isqrt(a):
    if a[0] < 0: raise ValueError('sqrt of negative interval')
    lo = CD.sqrt(a[0]); hi = CU.sqrt(a[1])
    lo = CD.subtract(lo, ulp(lo)) if lo != 0 else ZERO
    hi = CU.add(hi, ulp(hi))
    # verify by squaring (correctly rounded sqrt is guaranteed, this is a second check)
    assert CU.multiply(lo, lo) <= a[0] or lo == 0, 'sqrt lower bound'
    assert CD.multiply(hi, hi) >= a[1], 'sqrt upper bound'
    return (max(lo, ZERO), hi)
def fpow(a, p):
    """a^p for interval a > 0 and exact rational p, via exp(p ln a)."""
    pq = q(p)
    return iexp(mul(pq, iln(a)))

# ---------------------------------------------------------------- pi by Machin, with remainder
def _arctan_inv(n, terms_prec):
    """interval enclosure of arctan(1/n) by the alternating series, n >= 2."""
    with localcontext(CX) as c:
        x = Dec(1) / Dec(n)
        x2 = x * x
        s = Dec(0); term = x; k = 0
        sign = 1
        while True:
            t = term / Dec(2 * k + 1)
            if t < Dec(1).scaleb(-terms_prec):
                break
            s += t if sign > 0 else -t
            sign = -sign; term = term * x2; k += 1
        # alternating series with decreasing terms: |remainder| <= next term t
        err = t + Dec(1).scaleb(-terms_prec + 2)   # rounding slack (generous)
    return (CD.subtract(s, err), CU.add(s, err))

def compute_pi():
    a = _arctan_inv(5, PREC + 20); b = _arctan_inv(239, PREC + 20)
    return sub(smul(Dec(16), a), smul(Dec(4), b))

PI = compute_pi()
SQRTPI = isqrt(PI)
SQRT2PI = isqrt(smul(TWO, PI))

# ---------------------------------------------------------------- erf
def erf_point(x):
    """enclosure of erf(x) for a Decimal x (any sign)."""
    if x < 0:
        r = erf_point(-x); return (-r[1], -r[0])
    if x == 0: return (ZERO, ZERO)
    if x > 7:
        # 1 - erf(x) = erfc(x) <= exp(-x^2)/(x sqrt(pi)) < 1e-21; return [1 - that, 1]
        b = div(iexp(neg(sq((x, x)))), mul((x, x), SQRTPI))
        return (CD.subtract(ONE, b[1]), ONE)
    # Taylor series: erf(x) = 2/sqrt(pi) sum (-1)^n x^(2n+1)/(n! (2n+1)); alternating with decreasing terms once n >= x^2.
    with localcontext(Context(prec=PREC + 40, rounding=ROUND_FLOOR, traps=TRAPS)) as c:
        x2 = x * x
        s = Dec(0); term = x; n = 0
        nmin = int(x2) + 2
        while True:
            t = term / Dec(2 * n + 1)
            if n >= nmin and t < Dec(1).scaleb(-PREC - 12):
                break
            s += t if n % 2 == 0 else -t
            n += 1
            term = term * x2 / Dec(n)
        err = t + Dec(1).scaleb(-PREC - 10)
    lo = CD.subtract(s, err); hi = CU.add(s, err)
    r = mul((lo, hi), div((TWO, TWO), SQRTPI))
    return (max(r[0], Dec(-1)), min(r[1], ONE))

def ierf(a):
    """erf is increasing."""
    return (erf_point(a[0])[0], erf_point(a[1])[1])
def ierfc(a):
    """erfc(x) = 1 - erf(x), decreasing; for large x use the bound directly for accuracy."""
    lo_x, hi_x = a
    def erfc_pt(x, side):
        if x > 7:
            b = div(iexp(neg(sq((x, x)))), mul((x, x), SQRTPI))   # erfc(x) in [0, b]: use Mills ratio bound... lower bound 0
            # sharper lower bound: erfc(x) >= exp(-x^2) * 2/(sqrt(pi) (x + sqrt(x^2+2)))  (Birnbaum-type); use it
            xx = (x, x)
            lo = div(mul(smul(TWO, iexp(neg(sq(xx)))), (ONE, ONE)), mul(SQRTPI, add(xx, isqrt(add(sq(xx), (TWO, TWO))))))
            return (lo[0], b[1])
        e = erf_point(x)
        return (CD.subtract(ONE, e[1]), CU.subtract(ONE, e[0]))
    return (erfc_pt(hi_x, 0)[0], erfc_pt(lo_x, 1)[1])

# ---------------------------------------------------------------- Gamma(x), x > 0, by Stirling at x + N
def _bernoulli_coeffs():
    # B_{2k}/(2k(2k-1)) for k = 1..8 as Fractions
    B = [Fr(1, 6), Fr(-1, 30), Fr(1, 42), Fr(-1, 30), Fr(5, 66), Fr(-691, 2730), Fr(7, 6), Fr(-3617, 510)]
    return [B[k - 1] / (2 * k * (2 * k - 1)) for k in range(1, 9)]
_STIR = _bernoulli_coeffs()

def igamma(x):
    """enclosure of Gamma(x) for interval x with x > 0 (x of moderate size); Stirling series at z = x + N with the
    remainder bounded by the first omitted term (valid for real z > 0)."""
    N = 40
    z = add(x, q(N))
    # ln Gamma(z) = (z - 1/2) ln z - z + ln(2 pi)/2 + sum_{k=1}^{K} c_k / z^(2k-1) + R, |R| <= |c_{K+1}| / z^(2K+1)
    K = 7
    lnz = iln(z)
    s = add(mul(sub(z, q(Fr(1, 2))), lnz), neg(z))
    s = add(s, smul(Dec('0.5'), iln(smul(TWO, PI))))
    zinv = recip(z); zp = zinv
    for k in range(1, K + 1):
        s = add(s, mul(q(_STIR[k - 1]), zp))
        zp = mul(zp, sq(zinv))
    rem = mag(mul(q(_STIR[K]), zp))
    s = (CD.subtract(s[0], rem), CU.add(s[1], rem))
    g = iexp(s)
    # Gamma(x) = Gamma(x+N) / (x (x+1) ... (x+N-1))
    p = (ONE, ONE)
    for j in range(N):
        p = mul(p, add(x, q(j)))
    return div(g, p)

# ---------------------------------------------------------------- Taylor models
# Variables delta_i in [-h_i, h_i]; polynomial part: dict {exponent tuple: interval}; remainder: interval.
class TMSpace:
    def __init__(self, nvars, order, h, cellwide=False):
        self.n = nvars; self.p = order; self.cellwide = cellwide
        self.h = [q(x) for x in h]                 # half-widths as intervals (exact decimals)
        self.monos = [m for m in self._all_monos()]
        self.deg = {m: sum(m) for m in self.monos}
        # range of each monomial over the box and its exact integral over the box
        self.rng = {}; self.integ = {}
        for m in self.monos:
            r = (ONE, ONE); it = (ONE, ONE); even = True
            for i, e in enumerate(m):
                hi_e = ipow(self.h[i], e)
                r = mul(r, hi_e)
                if e % 2 == 1:
                    even = False
                # integral of delta^e over [-h, h]: 2 h^(e+1)/(e+1) for even e, else 0
                if e % 2 == 0:
                    it = mul(it, div(smul(TWO, ipow(self.h[i], e + 1)), q(e + 1)))
                else:
                    it = (ZERO, ZERO)
            self.rng[m] = (ZERO, r[1]) if even else (-r[1], r[1])
            self.integ[m] = it
        vol = (ONE, ONE)
        for i in range(self.n): vol = mul(vol, smul(TWO, self.h[i]))
        self.vol = vol
        self.zero_m = tuple([0] * self.n)
    def _all_monos(self):
        def rec(i, left):
            if i == self.n - 1:
                for e in range(left + 1): yield (e,)
                return
            for e in range(left + 1):
                for rest in rec(i + 1, left - e): yield (e,) + rest
        return sorted(rec(0, self.p), key=lambda m: (sum(m), m))
    def var(self, i):
        c = {self.zero_m: (ZERO, ZERO)}
        m = tuple(1 if j == i else 0 for j in range(self.n))
        c[m] = (ONE, ONE)
        return TM(self, c, (ZERO, ZERO))
    def const(self, a):
        return TM(self, {self.zero_m: q(a)}, (ZERO, ZERO))

class TM:
    __slots__ = ('S', 'c', 'r')
    def __init__(self, S, c, r):
        self.S = S; self.c = c; self.r = r
    # --- helpers
    def range(self):
        """interval enclosure of the TM over the box."""
        S = self.S; tot = self.r
        for m, cm in self.c.items():
            if m == S.zero_m: tot = add(tot, cm)
            else: tot = add(tot, mul(cm, S.rng[m]))
        return tot
    def const_term(self):
        return self.c.get(self.S.zero_m, (ZERO, ZERO))
    def __add__(self, o):
        S = self.S
        if not isinstance(o, TM): o = S.const(o)
        c = dict(self.c)
        for m, v in o.c.items():
            c[m] = add(c[m], v) if m in c else v
        return TM(S, c, add(self.r, o.r))
    __radd__ = __add__
    def __neg__(self):
        return TM(self.S, {m: neg(v) for m, v in self.c.items()}, neg(self.r))
    def __sub__(self, o):
        return self.__add__(-(o if isinstance(o, TM) else self.S.const(o)))
    def __rsub__(self, o):
        return (-self).__add__(o)
    def scale(self, a):
        """multiply by an interval/exact scalar."""
        a = q(a)
        return TM(self.S, {m: mul(a, v) for m, v in self.c.items()}, mul(a, self.r))
    def __mul__(self, o):
        S = self.S
        if not isinstance(o, TM): return self.scale(o)
        p = S.p; deg = S.deg
        c = {}; rem = (ZERO, ZERO)
        for ma, va in self.c.items():
            da = deg[ma]
            for mb, vb in o.c.items():
                prod = mul(va, vb)
                if da + deg[mb] <= p:
                    m = tuple(x + y for x, y in zip(ma, mb))
                    c[m] = add(c[m], prod) if m in c else prod
                else:
                    # range of the monomial product over the box
                    m = tuple(x + y for x, y in zip(ma, mb))
                    rng = S.rng.get(m)
                    if rng is None:
                        r = (ONE, ONE); even = True
                        for i, e in enumerate(m):
                            r = mul(r, ipow(S.h[i], e))
                            if e % 2: even = False
                        rng = (ZERO, r[1]) if even else (-r[1], r[1])
                        S.rng[m] = rng
                    rem = add(rem, mul(prod, rng))
        # cross terms with remainders
        ra = self.r; rb = o.r
        if ra != (ZERO, ZERO) or rb != (ZERO, ZERO):
            rem = add(rem, mul(ra, o.range()))
            rem = add(rem, mul(rb, TM(S, self.c, (ZERO, ZERO)).range()))
            rem = add(rem, mul(ra, rb))
        return TM(S, c, rem)
    __rmul__ = __mul__
    def __truediv__(self, o):
        if isinstance(o, TM): return self * o.recip()
        return self.scale(recip(q(o)))
    def __rtruediv__(self, o):
        return self.recip().scale(q(o))
    # --- elementary functions by Taylor expansion about the constant term with a Lagrange remainder
    def _apply(self, derivs, frange=None):
        """derivs(c0, B, p) -> (list a_0..a_p of f^(k)(c0)/k! as intervals, bound of f^(p+1)(xi)/(p+1)! for xi in c0+B).
        frange(z) -> an interval enclosing f over the argument interval z (monotone functions); when the Taylor model's own
        range is wider than f(c0 + B), the constant model with that range is returned instead (both enclose f on the
        cell; the second is tighter when the cell is too wide for the expansion)."""
        S = self.S; p = S.p
        c0 = self.const_term()
        That = TM(S, {m: v for m, v in self.c.items() if m != S.zero_m}, self.r)
        B = That.range()
        if S.cellwide:
            # cell-wide Taylor coefficients: every derivative is taken over the value range c0 + B
            a, rb = derivs(add(c0, B), B, p)
        else:
            a, rb = derivs(c0, B, p)
        # Horner: f = a0 + That (a1 + That (a2 + ...))
        res = S.const(a[p])
        for k in range(p - 1, -1, -1):
            res = res * That + a[k]
        # Lagrange remainder: rb * That^(p+1), bounded by rb * B^(p+1)
        Bp = ipow(B, p + 1)
        res.r = add(res.r, mul(rb, Bp))
        if frange is not None:
            fr = frange(add(c0, B))
            if width(res.range()) > CU.multiply(Dec(4), width(fr)):
                return S.const(fr)
        return res
    def exp(self, upper=None):
        """exp of the TM; `upper` (a Decimal) is an a-priori upper bound of the argument on the cell, used to cap the
        value range at which the Lagrange remainder's e^xi is evaluated (the true range is a subset of the TM range
        intersected with (-inf, upper]); the Taylor coefficients at the centre are unchanged."""
        def derivs(c0, B, p):
            e0 = iexp(c0)
            a = [e0]; f = ONE
            for k in range(1, p + 1):
                f = CU.multiply(f, Dec(k))
                a.append(div(e0, (f, f)))
            f = CU.multiply(f, Dec(p + 1))
            z = add(c0, B)
            if upper is not None:
                # the Lagrange point lies between a representative of c0 and the true argument (<= upper): cap the range at
                # max(upper, c0's upper end)
                cap = max(upper, c0[1])
                if z[1] > cap: z = (min(z[0], cap), cap)
            rb = div(iexp(z), (f, f))
            return a, rb
        def frange(z):
            if upper is not None and z[1] > upper:
                z = (min(z[0], upper), upper)
            return iexp(z)
        return self._apply(derivs, frange)
    def ln(self):
        def derivs(c0, B, p):
            a = [iln(c0)]
            inv = recip(c0); powk = inv
            for k in range(1, p + 1):
                # f^(k)(x)/k! = (-1)^(k-1) / (k x^k)
                t = div(powk, q(k))
                a.append(t if k % 2 == 1 else neg(t))
                powk = mul(powk, inv)
            z = add(c0, B)
            t = div(ipow(recip(z), p + 1), q(p + 1))
            rb = t if (p + 1) % 2 == 1 else neg(t)
            return a, rb
        return self._apply(derivs, iln)
    def sqrt(self):
        def derivs(c0, B, p):
            s0 = isqrt(c0)
            a = [s0]
            # f^(k)(x)/k! = binom(1/2, k) x^(1/2 - k)
            binom = Fr(1); inv = recip(c0); powk = (ONE, ONE)
            for k in range(1, p + 1):
                binom = binom * (Fr(1, 2) - (k - 1)) / k
                powk = mul(powk, inv)
                a.append(mul(q(binom), mul(s0, powk)))
            binom = binom * (Fr(1, 2) - p) / (p + 1)
            z = add(c0, B)
            rb = mul(q(binom), mul(isqrt(z), ipow(recip(z), p + 1)))
            return a, rb
        return self._apply(derivs, isqrt)
    def recip(self):
        def derivs(c0, B, p):
            inv = recip(c0)
            a = [inv]; powk = inv
            for k in range(1, p + 1):
                powk = mul(powk, inv)
                a.append(powk if k % 2 == 0 else neg(powk))
            z = add(c0, B)
            t = ipow(recip(z), p + 2)
            rb = t if (p + 1) % 2 == 0 else neg(t)
            return a, rb
        return self._apply(derivs, recip)
    def erf(self):
        def derivs(c0, B, p):
            a = [ierf(c0)]
            # f^(k)(x) = 2/sqrt(pi) (-1)^(k-1) H_{k-1}(x) exp(-x^2), H physicists' Hermite
            two_over_sqrtpi = div((TWO, TWO), SQRTPI)
            e0 = iexp(neg(sq(c0)))
            def dk_over_kfact(x, k, ex):
                # evaluate H_{k-1}(x) at interval x
                Hs = [(ONE, ONE), smul(TWO, x)]
                for n in range(1, k - 1):
                    Hs.append(sub(smul(TWO, mul(x, Hs[n])), smul(Dec(2 * n), Hs[n - 1])))
                val = mul(two_over_sqrtpi, mul(Hs[k - 1], ex))
                if (k - 1) % 2 == 1: val = neg(val)
                kf = Dec(math.factorial(k))
                return div(val, (kf, kf))
            for k in range(1, p + 1):
                a.append(dk_over_kfact(c0, k, e0))
            z = add(c0, B)
            rb = dk_over_kfact(z, p + 1, iexp(neg(sq(z))))
            return a, rb
        return self._apply(derivs, ierf)
    def erfc(self):
        return 1 - self.erf()
    def add_remainder(self, r):
        """return the TM with [-r, r] added to its remainder."""
        return TM(self.S, self.c, add(self.r, (-r, r)))
    def integrate(self):
        """enclosure of the integral of the TM over the box."""
        S = self.S
        tot = mul(self.r, S.vol)
        for m, cm in self.c.items():
            it = S.integ[m]
            if it != (ZERO, ZERO):
                tot = add(tot, mul(cm, it))
        return tot

def tm_const(S, a): return S.const(a)


# ---------------------------------------------------------------- fast one-variable Taylor models (list-based)
class TM1Space:
    """One variable delta in [-h, h]; polynomial coefficients as a list of intervals; same interface as TMSpace/TM."""
    def __init__(self, order, h):
        self.n = 1; self.p = order; self.cellwide = False
        self.h = [q(h)]
        hh = self.h[0]
        self.hp = [(ONE, ONE)]
        for k in range(1, 2 * order + 3):
            self.hp.append(mul(self.hp[-1], hh))
        # monomial ranges and integrals
        self.rng1 = [(ZERO, self.hp[k][1]) if k % 2 == 0 else (-self.hp[k][1], self.hp[k][1]) for k in range(2 * order + 3)]
        self.integ1 = [div(smul(TWO, self.hp[k + 1]), q(k + 1)) if k % 2 == 0 else (ZERO, ZERO) for k in range(order + 1)]
        self.vol = smul(TWO, hh)
        self.zero_m = (0,)
    def var(self, i=0):
        if self.p == 0:
            return TM1(self, [(ZERO, ZERO)], (neg(self.h[0])[0], self.h[0][1]))
        c = [(ZERO, ZERO)] * (self.p + 1); c[1] = (ONE, ONE)
        return TM1(self, c, (ZERO, ZERO))
    def const(self, a):
        c = [(ZERO, ZERO)] * (self.p + 1); c[0] = q(a)
        return TM1(self, c, (ZERO, ZERO))

class TM1:
    __slots__ = ('S', 'c', 'r')
    def __init__(self, S, c, r):
        self.S = S; self.c = c; self.r = r
    def range(self):
        S = self.S; c = self.c
        lo, hi = c[0]
        lo = CD.add(lo, self.r[0]); hi = CU.add(hi, self.r[1])
        for k in range(1, S.p + 1):
            ck = c[k]
            if ck[0] == 0 and ck[1] == 0: continue
            rk = S.rng1[k]
            m = mul(ck, rk)
            lo = CD.add(lo, m[0]); hi = CU.add(hi, m[1])
        return (lo, hi)
    def const_term(self): return self.c[0]
    def __add__(self, o):
        S = self.S
        if not isinstance(o, TM1):
            oq = q(o); c = list(self.c); c[0] = add(c[0], oq)
            return TM1(S, c, self.r)
        return TM1(S, [add(a, b) for a, b in zip(self.c, o.c)], add(self.r, o.r))
    __radd__ = __add__
    def __neg__(self): return TM1(self.S, [neg(a) for a in self.c], neg(self.r))
    def __sub__(self, o): return self.__add__(-(o if isinstance(o, TM1) else self.S.const(o)))
    def __rsub__(self, o): return (-self).__add__(o)
    def scale(self, a):
        a = q(a)
        return TM1(self.S, [mul(a, x) for x in self.c], mul(a, self.r))
    def __mul__(self, o):
        S = self.S
        if not isinstance(o, TM1): return self.scale(o)
        p = S.p; a = self.c; b = o.c
        c = [(ZERO, ZERO)] * (p + 1)
        rlo = ZERO; rhi = ZERO
        nz_a = [i for i in range(p + 1) if a[i][0] != 0 or a[i][1] != 0]
        nz_b = [j for j in range(p + 1) if b[j][0] != 0 or b[j][1] != 0]
        for i in nz_a:
            ai = a[i]
            for j in nz_b:
                pr = mul(ai, b[j])
                k = i + j
                if k <= p:
                    ck = c[k]; c[k] = (CD.add(ck[0], pr[0]), CU.add(ck[1], pr[1]))
                else:
                    m = mul(pr, S.rng1[k]); rlo = CD.add(rlo, m[0]); rhi = CU.add(rhi, m[1])
        ra = self.r; rb = o.r
        if ra[0] != 0 or ra[1] != 0 or rb[0] != 0 or rb[1] != 0:
            if ra[0] != 0 or ra[1] != 0:
                m = mul(ra, o.range()); rlo = CD.add(rlo, m[0]); rhi = CU.add(rhi, m[1])
            if rb[0] != 0 or rb[1] != 0:
                m = mul(rb, TM1(S, self.c, (ZERO, ZERO)).range()); rlo = CD.add(rlo, m[0]); rhi = CU.add(rhi, m[1])
            m = mul(ra, rb); rlo = CD.add(rlo, m[0]); rhi = CU.add(rhi, m[1])
        return TM1(S, c, (rlo, rhi))
    __rmul__ = __mul__
    def __truediv__(self, o):
        if isinstance(o, TM1): return self * o.recip()
        return self.scale(recip(q(o)))
    def __rtruediv__(self, o): return self.recip().scale(q(o))
    def add_remainder(self, r): return TM1(self.S, self.c, add(self.r, (-r, r)))
    def integrate(self):
        S = self.S
        tot = mul(self.r, S.vol)
        for k in range(0, S.p + 1, 2):
            tot = add(tot, mul(self.c[k], S.integ1[k]))
        return tot
    def _apply(self, derivs, frange=None):
        S = self.S; p = S.p
        c0 = self.c[0]
        That = TM1(S, [(ZERO, ZERO)] + list(self.c[1:]), self.r)
        B = That.range()
        a, rb = derivs(c0, B, p)
        res = S.const(a[p])
        for k in range(p - 1, -1, -1):
            res = res * That + a[k]
        res.r = add(res.r, mul(rb, ipow(B, p + 1)))
        if frange is not None:
            fr = frange(add(c0, B))
            if width(res.range()) > CU.multiply(Dec(4), width(fr)):
                return S.const(fr)
        return res
    exp = TM.exp; ln = TM.ln; sqrt = TM.sqrt; recip = TM.recip; erf = TM.erf; erfc = TM.erfc
