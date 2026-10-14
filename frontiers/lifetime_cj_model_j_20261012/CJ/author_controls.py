"""Note CJ controls: a certified two-sided enclosure of note C3's model number J (Python standard library only).

J = (16/45)(4 pi)^(-1/2) int_0^inf h(a) psi(a) da,  psi(a) = (432/a^2)^(2/3) K_{4/3}(2a/sqrt3),
h(a) = E[(a - W)_+^3], W ~ Gamma(1/2, 1)  (note CJ, Lemma 1).  The integral is enclosed by Simpson's rule on an
explicit partition, Simpson's remainder bounded through explicit bounds of the fourth derivative (Lemma 3), plus
closed-form tails (Lemma 4).  All arithmetic is outward-rounded decimal interval arithmetic.
Usage: python3 cj_exact.py [--mutant M1..M14]
"""
import decimal
import json
import math
import sys
from fractions import Fraction as Fr

USAGE = 'usage: cj_exact.py [--mutant M1..M14]'
MUTANTS = ['M%d' % i for i in range(1, 15)]
if len(sys.argv) == 1:
    MUT = None
elif len(sys.argv) == 3 and sys.argv[1] == '--mutant' and sys.argv[2] in MUTANTS:
    MUT = sys.argv[2]
else:
    sys.stderr.write(USAGE + '\n')
    sys.exit(2)

PREC = 50
CD = decimal.Context(prec=PREC, rounding=decimal.ROUND_FLOOR)
CU = decimal.Context(prec=PREC, rounding=decimal.ROUND_CEILING)
CN = decimal.Context(prec=PREC, rounding=decimal.ROUND_HALF_EVEN)
# Every rounding is explicit (CD, CU, CN).  The default context traps any operation that would round, so an operation
# written without a context (unary minus, abs, +, -, *, /) can only ever be exact.
decimal.setcontext(decimal.Context(prec=PREC, traps=[decimal.Inexact, decimal.Rounded, decimal.InvalidOperation,
                                                     decimal.DivisionByZero, decimal.Overflow]))
Dec = decimal.Decimal
Z = Dec(0)
COUNT = {}


class Fail(Exception):
    pass


def need(cond, group):
    COUNT[group] = COUNT.get(group, 0) + 1
    if not cond:
        raise Fail(group)


def _hook(kind, value, tb):
    if kind is Fail:
        sys.stderr.write('FAILED: %s\n' % value.args[0])
    else:
        sys.__excepthook__(kind, value, tb)


sys.excepthook = _hook       # any failed check: message on stderr, empty stdout, exit status 1


# ---------------------------------------------------------------- interval arithmetic (lo, hi)
def q(x):
    x = Fr(x)
    n, d = Dec(x.numerator), Dec(x.denominator)
    return (CD.divide(n, d), CU.divide(n, d))


def pt(x):
    return (x, x)


def add(a, b):
    return (CD.add(a[0], b[0]), CU.add(a[1], b[1]))


def sub(a, b):
    return (CD.subtract(a[0], b[1]), CU.subtract(a[1], b[0]))


def neg(a):
    return (a[1].copy_negate(), a[0].copy_negate())          # exact; unary minus would round in the context


def mul(a, b):
    lo = min(CD.multiply(x, y) for x in a for y in b)
    hi = max(CU.multiply(x, y) for x in a for y in b)
    return (lo, hi)


def div(a, b):
    if not (b[0] > 0 or b[1] < 0):
        raise Fail('interval_division')
    lo = min(CD.divide(x, y) for x in a for y in b)
    hi = max(CU.divide(x, y) for x in a for y in b)
    return (lo, hi)


def isqrt(a):
    if a[0] < 0:
        raise Fail('interval_sqrt')
    lo = Z if a[0] == 0 else max(Z, CD.next_minus(CN.sqrt(a[0])))
    hi = Z if a[1] == 0 else CU.next_plus(CN.sqrt(a[1]))
    if CU.multiply(lo, lo) > a[0] or CD.multiply(hi, hi) < a[1]:      # verified, not assumed
        raise Fail('interval_sqrt')
    return (lo, hi)


def iexp(a):
    # decimal's exp is correctly rounded (half-even); one ulp of widening makes it an enclosure
    return (max(Z, CD.next_minus(CN.exp(a[0]))), CU.next_plus(CN.exp(a[1])))


def iln(a):
    if a[0] <= 0:
        raise Fail('interval_ln')
    return (CD.next_minus(CN.ln(a[0])), CU.next_plus(CN.ln(a[1])))


def ipow(a, r):
    # a > 0, r rational
    return iexp(mul(iln(a), q(r)))


def ipow_int(a, n):
    out = (Dec(1), Dec(1))
    for _ in range(n):
        out = mul(out, a)
    return out


def absmax(a):
    return max(a[0].copy_abs(), a[1].copy_abs())            # exact; abs() would round in the context


def contains(a, x):
    return a[0] <= x <= a[1]


def width(a):
    return CU.subtract(a[1], a[0])


ONE = q(1)
HALF = q(Fr(1, 2))
TINY = Dec('1e-45')       # series are summed until the last term is below TINY times the partial sum

# neg and absmax are exact at full precision (they must not round in any context)
X50 = CN.divide(Dec(1), Dec(7))
need(neg(pt(X50)) == (X50.copy_negate(), X50.copy_negate()) and absmax(neg(pt(X50))) == X50, 'primitives')


# ---------------------------------------------------------------- pi (Machin), Gamma(1/3) and Gamma(2/3)
def atan_inv(n):
    """atan(1/n), n >= 2: alternating series with decreasing terms, enclosed by the next term."""
    s = (Z, Z)
    k = 0
    p = q(Fr(1, n))
    n2 = q(n * n)
    while True:
        t = div(p, q(2 * k + 1))
        s = add(s, t) if k % 2 == 0 else sub(s, t)
        p = div(p, n2)
        k += 1
        nxt = div(p, q(2 * k + 1))
        if nxt[1] < Dec('1e-55'):
            return (CD.subtract(s[0], nxt[1]), CU.add(s[1], nxt[1]))


PI = sub(mul(q(16), atan_inv(5)), mul(q(4), atan_inv(239)))
need(width(PI) < Dec('1e-45'), 'pi')
need(contains(PI, Dec('3.14159265358979323846264338327950288419716939937510')), 'pi')

GX = 130            # Gamma(a) = gamma(a, X) + Gamma(a, X) at X = 130


def gamma_small(a):
    """Gamma(a) for 0 < a <= 1: gamma(a, X) = X^a e^(-X) sum_n X^n / (a (a+1) ... (a+n)) (positive terms) and
    0 <= Gamma(a, X) <= X^(a-1) e^(-X)."""
    a = Fr(a)
    X = q(GX)
    t = div(ONE, q(a))
    s = t
    n = 0
    while True:
        n += 1
        t = mul(t, div(X, q(a + n)))
        s = add(s, t)
        if n > GX and t[1] < CU.multiply(s[0], TINY):
            break
    r = div(X, q(a + n + 1))                     # all later ratios are at most r < 1
    tail = div(mul(t, r), sub(ONE, r))
    s = (s[0], CU.add(s[1], tail[1]))
    pref = mul(iexp(mul(q(a), iln(X))), iexp(neg(X)))
    low = mul(pref, s)
    upper_tail = mul(iexp(mul(q(a - 1), iln(X))), iexp(neg(X)))
    if MUT == 'M1':
        upper_tail = mul(upper_tail, q(-10 ** 30))
    return (low[0], CU.add(low[1], upper_tail[1]))


G13 = gamma_small(Fr(1, 3))
G23 = gamma_small(Fr(2, 3))
SQ3 = isqrt(q(3))
need(contains(G13, Dec('2.6789385347077476336556929409746776441286893779573')), 'gamma')
need(contains(G23, Dec('1.3541179394264004169452880281545137855193272660568')), 'gamma')
refl = sub(mul(mul(G13, G23), SQ3), mul(q(2), PI))     # Gamma(1/3) Gamma(2/3) sqrt3 = 2 pi: two independent series
need(refl[0] <= 0 <= refl[1], 'gamma')
need(width(G13) < Dec('1e-40') and width(G23) < Dec('1e-40'), 'gamma')

# ---------------------------------------------------------------- modified Bessel functions
NU = Fr(4, 3)
GSHIFT = {Fr(4, 3): mul(q(Fr(4, 9)), G13),        # Gamma(7/3) = (4/3)(1/3) Gamma(1/3)
          Fr(-4, 3): mul(q(-3), G23),             # Gamma(-1/3) = Gamma(2/3)/(-1/3)
          Fr(7, 3): mul(q(Fr(28, 27)), G13),      # Gamma(10/3) = (7/3)(4/3)(1/3) Gamma(1/3)
          Fr(-7, 3): mul(q(Fr(9, 4)), G23)}       # Gamma(-4/3) = Gamma(-1/3)/(-4/3)


def bessel_i(mu, x):
    """I_mu(x) = (x/2)^mu sum_m (x^2/4)^m / (m! Gamma(m + mu + 1)), x > 0 an interval."""
    y = mul(mul(x, x), q(Fr(1, 4)))
    term = div(ONE, GSHIFT[mu])
    s = term
    m = 0
    while True:
        term = div(mul(term, y), mul(q(m + 1), q(m + 1 + mu)))
        m += 1
        s = add(s, term)
        ratio = div(y, mul(q(m + 1), q(m + 1 + mu)))       # the next ratio; m + 1 + mu > 0 once m >= 2
        if m >= 2 and ratio[1] <= HALF[0] and absmax(term) < CD.multiply(s[0].copy_abs(), TINY):
            break
    tail = absmax(term)          # later terms keep one sign, with ratios at most 1/2: their sum is at most the last term
    s = (CD.subtract(s[0], tail), CU.add(s[1], tail))
    return mul(ipow(mul(x, HALF), mu), s)


PI_SQ3 = div(PI, SQ3)


def bessel_k_ladder(x):
    """[K_{4/3}, K_{7/3}, K_{10/3}, K_{13/3}, K_{16/3}] at x > 0 (an interval).
    K_mu = (pi/(2 sin(mu pi))) (I_{-mu} - I_mu); sin(4 pi/3) = -sqrt3/2, sin(7 pi/3) = sqrt3/2."""
    k43 = mul(PI_SQ3, sub(bessel_i(Fr(4, 3), x), bessel_i(Fr(-4, 3), x)))
    k73 = mul(PI_SQ3, sub(bessel_i(Fr(-7, 3), x), bessel_i(Fr(7, 3), x)))
    if MUT == 'M2':
        k43 = mul(k43, q(Fr(101, 100)))
    ks = [k43, k73]
    for j in range(3):                       # K_{mu+1} = K_{mu-1} + (2 mu / x) K_mu, for mu = 7/3, 10/3, 13/3
        mu = NU + 1 + j
        ks.append(add(ks[-2], mul(div(q(2 * mu), x), ks[-1])))
    need(all(k[0] > 0 for k in ks), 'bessel')
    return ks


# ---------------------------------------------------------------- h and its derivatives
def lower_gammas(a):
    """gamma(s, a) for s = 1/2, 3/2, 5/2, 7/2: a^s e^(-a) sum_n a^n / (s (s+1) ... (s+n)), positive terms."""
    out = []
    ea = iexp(neg(a))
    svals = [Fr(1, 2), Fr(3, 2), Fr(5, 2), Fr(7, 2)]
    if MUT == 'M10':
        svals[1] = Fr(5, 2)
    for s in svals:
        t = div(ONE, q(s))
        tot = t
        n = 0
        while True:
            n += 1
            t = mul(t, div(a, q(s + n)))
            tot = add(tot, t)
            if div(a, q(s + n + 1))[1] <= HALF[0] and t[1] < CU.multiply(tot[0], TINY):
                break
        tot = (tot[0], CU.add(tot[1], t[1]))        # later ratios are at most 1/2: the tail is at most the last term
        out.append(mul(mul(ipow(a, s), ea), tot))
    return out


SQPI = isqrt(PI)
H_CACHE = {}


def h_derivs(a):
    """[h, h', h'', h''', h''''] at a > 0 (an interval); W ~ Gamma(1/2, 1) has density pi^(-1/2) w^(-1/2) e^(-w).
    E[(a - W)_+^n] = pi^(-1/2) sum_k C(n, k) a^(n-k) (-1)^k gamma(k + 1/2, a);  h = E3, h' = 3 E2, h'' = 6 E1,
    h''' = 6 P(W <= a), h'''' = 6 times the density of W."""
    if a in H_CACHE:
        return H_CACHE[a]
    g = lower_gammas(a)

    def em(n):
        s = (Z, Z)
        coeffs = {3: [1, 3, 3, 1], 2: [1, 2, 1], 1: [1, 1]}[n]
        for k in range(n + 1):
            term = mul(mul(q(coeffs[k]), ipow_int(a, n - k)), g[k])
            s = add(s, term) if k % 2 == 0 else sub(s, term)
        return div(s, SQPI)

    h0 = em(3)
    if MUT == 'M3':
        h0 = em(2)
    out = [h0, mul(q(3), em(2)), mul(q(6), em(1)), div(mul(q(6), g[0]), SQPI),
           div(mul(q(6), mul(ipow(a, Fr(-1, 2)), iexp(neg(a)))), SQPI)]
    H_CACHE[a] = out
    return out


# ---------------------------------------------------------------- psi(a) = 432^(2/3) a^(-4/3) K_{4/3}(b a), b = 2/sqrt3
B = div(q(2), SQ3)
C432 = ipow(q(432), Fr(2, 3))
PSI_CACHE = {}


def psi_derivs(a):
    """[psi, psi', ..., psi''''] at a > 0: psi^(j)(a) = C432 b^(4/3 + j) u^(j)(b a) with u(x) = x^(-4/3) K_{4/3}(x),
    u' = -x^(-nu) K_{nu+1},  u'' = x^(-nu) K_{nu+2} - x^(-nu-1) K_{nu+1},  u''' = 3 x^(-nu-1) K_{nu+2} - x^(-nu) K_{nu+3},
    u'''' = 3 x^(-nu-2) K_{nu+2} - 6 x^(-nu-1) K_{nu+3} + x^(-nu) K_{nu+4}."""
    if a in PSI_CACHE:
        return PSI_CACHE[a]
    x = mul(B, a)
    if MUT == 'M6':
        x = mul(q(Fr(11, 10)), x)
    k = bessel_k_ladder(x)
    xm = ipow(x, -NU)
    ix = div(ONE, x)
    c6 = 5 if MUT == 'M4' else 6
    u = [mul(xm, k[0]),
         neg(mul(xm, k[1])),
         sub(mul(xm, k[2]), mul(mul(xm, ix), k[1])),
         sub(mul(q(3), mul(mul(xm, ix), k[2])), mul(xm, k[3])),
         add(sub(mul(q(3), mul(mul(xm, mul(ix, ix)), k[2])), mul(q(c6), mul(mul(xm, ix), k[3]))), mul(xm, k[4]))]
    out = [mul(mul(C432, ipow(B, NU + j)), u[j]) for j in range(5)]
    PSI_CACHE[a] = out
    return out


# ---------------------------------------------------------------- Simpson cells with a fourth-derivative remainder
def simpson(grid, hfun, label):
    """Enclose the integral over the grid of h(a) psi(a), h = hfun(a)[0], by Simpson's rule plus a remainder of
    absolute value at most D^5 M / 2880 per cell, where M bounds |(h psi)''''| on the cell: h^(j) (j <= 3) are
    nonnegative and nondecreasing, h'''' is nonnegative and nonincreasing, and |psi^(j)| are nonincreasing
    (psi is completely monotone)."""
    total = (Z, Z)
    err = Z
    err2 = Fr(0)                 # the same remainder sum in exact rational arithmetic (a control on the rounding of err)
    binom4 = [1, 1, 1, 1, 1] if MUT == 'M12' else [1, 4, 6, 4, 1]
    w4 = 3 if MUT == 'M5' else 4
    for a0, a1 in zip(grid, grid[1:]):
        dlt = CU.subtract(a1, a0)
        need(CD.subtract(a1, a0) == dlt, label)                       # cell widths are exact
        s = CD.add(a0, a1)
        need(s == CU.add(a0, a1), label)                               # a0 + a1 is exact
        m = CD.divide(s, Dec(2))
        need(m == CU.divide(s, Dec(2)), label)                         # the midpoint is exact
        h0, p0 = hfun(pt(a0)), psi_derivs(pt(a0))
        h1, p1 = hfun(pt(a1)), psi_derivs(pt(a1))
        hm, pm = hfun(pt(m)), psi_derivs(pt(m))
        f = add(add(mul(h0[0], p0[0]), mul(q(w4), mul(hm[0], pm[0]))), mul(h1[0], p1[0]))
        total = add(total, mul(f, div(pt(dlt), q(6))))
        mbound = Z
        for j in range(5):
            hb = h1[j][1] if j <= 3 else h0[4][1]
            pb = absmax(p0[4 - j])
            mbound = CU.add(mbound, CU.multiply(Dec(binom4[j]), CU.multiply(hb, pb)))
        # (3.1)'s majorant M dominates the Leibniz majorant sum_j C(4, j) h^(j) |psi^(4-j)| at a0, m and a1 (Lemma 2's
        # monotonicity); the Leibniz majorant is taken from the lower ends of the enclosures, with its own binomials
        for xh, xp in ((h0, p0), (hm, pm), (h1, p1)):
            lead = Z
            for j in range(5):
                v = xp[4 - j]
                lo_p = min(v[0].copy_abs(), v[1].copy_abs()) if (v[0] > 0 or v[1] < 0) else Z
                lead = CD.add(lead, CD.multiply(Dec(math.comb(4, j)), CD.multiply(max(Z, xh[j][0]), lo_p)))
            need(mbound >= lead, 'remainder')
        d5 = CU.multiply(CU.multiply(CU.multiply(dlt, dlt), CU.multiply(dlt, dlt)), dlt)
        err = CU.add(err, CU.divide(CU.multiply(d5, mbound), Dec(2880000 if MUT == 'M11' else 2880)))
        err2 += (Fr(a1) - Fr(a0)) ** 5 * Fr(mbound) / 2880
    need(err >= q(err2)[0], label)           # every rounding in err is upward, so err is at least the exact sum
    return total, err


def grid_from(spec):
    g = []
    for kind, a0, a1, n in spec:
        a0, a1 = Dec(a0), Dec(a1)
        if kind == 'u':
            pts = [CN.add(a0, CN.divide(CN.multiply(CN.subtract(a1, a0), Dec(i)), Dec(n))) for i in range(n + 1)]
        else:        # geometric, rounded to 12 significant digits (any increasing exact decimals partition the range)
            r = CN.power(CN.divide(a1, a0), CN.divide(Dec(1), Dec(n)))
            pts = [CN.multiply(a0, CN.power(r, Dec(i))) for i in range(n + 1)]
        pts = [a0] + [Dec(format(p, '.11e')) for p in pts[1:-1]] + [a1]
        if g:
            need(g[-1] == pts[0], 'partition')
            pts = pts[1:]
        g += pts
    need(all(x < y for x, y in zip(g, g[1:])), 'partition')
    return g


A_MIN, A_MAX = Dec('1e-6'), Dec(30)
SPEC = [('g', '1e-6', '0.05', 300), ('u', '0.05', '1', 400), ('u', '1', '4', 300), ('u', '4', '12', 300),
        ('u', '12', '30', 200)]
if MUT == 'M7':
    SPEC[1] = ('u', '0.06', '1', 400)
GRID = grid_from(SPEC)
need(GRID[0] == A_MIN and GRID[-1] == A_MAX, 'partition')


# ---------------------------------------------------------------- tails
def tail_low(coef_h, power_h):
    """int_0^A_MIN of coef_h a^power_h psi(a): psi(a) <= C432 2^(1/3) Gamma(4/3) b^(-4/3) a^(-8/3), because x^nu K_nu(x)
    is nonincreasing with limit 2^(nu - 1) Gamma(nu) at 0."""
    g43 = div(G13, q(3))
    cpsi = mul(mul(C432, mul(ipow(q(2), Fr(1, 3)), g43)), ipow(B, -NU))
    expo = Fr(power_h) - Fr(5, 3)                # int_0^A a^(p - 8/3) da = A^(p - 5/3)/(p - 5/3)
    need(expo > 0, 'tails')
    val = mul(mul(coef_h, cpsi), div(ipow(pt(A_MIN), expo), q(expo)))
    return (Z, val[1])


def tail_high():
    """int_A_MAX^inf h(a) psi(a) with h(a) <= a^3: a^(-4/3) <= A_MAX^(-4/3) and K_nu(x) <= K_nu(x0) e^(-(x - x0)) for
    x >= x0 (from K_nu(x) = int_0^inf e^(-x cosh t) cosh(nu t) dt)."""
    k0 = bessel_k_ladder(mul(B, pt(A_MAX)))[0]
    pre = mul(mul(C432, ipow(pt(A_MAX), -NU)), k0)
    A = pt(A_MAX)
    b2 = mul(B, B)
    s = add(add(div(mul(mul(A, A), A), B), div(mul(q(3), mul(A, A)), b2)),
            add(div(mul(q(6), A), mul(b2, B)), div(q(6), mul(b2, b2))))       # int_A^inf a^3 e^(-b(a - A)) da
    return (Z, mul(pre, s)[1])


# ---------------------------------------------------------------- checks of the special functions
for xs in ('0.3', '1.7', '6.5', '20', '34'):
    x = pt(Dec(xs))
    ks = bessel_k_ladder(x)
    w = add(mul(bessel_i(Fr(4, 3), x), ks[1]), mul(bessel_i(Fr(7, 3), x), ks[0]))   # Wronskian: = 1/x
    lhs = sub(w, div(ONE, x))
    need(lhs[0] <= 0 <= lhs[1] and width(w) < Dec('1e-15'), 'bessel')
for xs in ('0.5', '3', '12'):
    x0 = pt(Dec(xs))
    x1 = pt(Dec(xs) + 1)
    need(bessel_k_ladder(x1)[0][1] <= mul(bessel_k_ladder(x0)[0], iexp(q(-1)))[0], 'bessel')

EPS = Dec('1e-6')
for xs in ('0.000001', '0.01', '0.5', '2', '9', '30'):
    a = pt(Dec(xs))
    a2 = pt(Dec(xs) + EPS)
    d, d2 = h_derivs(a), h_derivs(a2)
    p, p2 = psi_derivs(a), psi_derivs(a2)
    need(all(v[0] >= 0 for v in d), 'h_function')
    need(d[0][1] <= mul(div(q(Fr(32, 35)), SQPI), ipow(a, Fr(7, 2)))[0], 'h_function')   # used in tail_low
    need(d[0][1] <= ipow_int(a, 3)[0], 'h_function')                                     # used in tail_high
    # each derivative's increment over [a, a + eps] lies between eps times the next derivative at the two ends
    for j in range(4):
        inc = sub(d2[j], d[j])
        lo_ = min(CD.multiply(EPS, d[j + 1][0]), CD.multiply(EPS, d2[j + 1][0]))
        hi_ = max(CU.multiply(EPS, d[j + 1][1]), CU.multiply(EPS, d2[j + 1][1]))
        need(lo_ <= inc[1] and inc[0] <= hi_, 'h_function')
        inc = sub(p2[j], p[j])
        lo_ = min(CD.multiply(EPS, p[j + 1][0]), CD.multiply(EPS, p2[j + 1][0]))
        hi_ = max(CU.multiply(EPS, p[j + 1][1]), CU.multiply(EPS, p2[j + 1][1]))
        need(lo_ <= inc[1] and inc[0] <= hi_, 'psi_function')
    need(all((v[0] > 0 if j % 2 == 0 else v[1] < 0) for j, v in enumerate(p)), 'psi_function')
    if Dec(xs) <= Dec('0.01'):
        # small a: h(a) = pi^(-1/2) sum_n (-1)^n a^(n + 7/2) B(n + 1/2, 4) / n!, alternating with decreasing terms
        s = (Z, Z)
        tn = None
        fact = 1
        for n in range(8):
            if n:
                fact *= n
            bn = Fr(6) / (Fr(2 * n + 1, 2) * Fr(2 * n + 3, 2) * Fr(2 * n + 5, 2) * Fr(2 * n + 7, 2))
            tn = mul(q(bn / fact), ipow(a, Fr(2 * n + 7, 2)))
            s = add(s, tn) if n % 2 == 0 else sub(s, tn)
        s = div((CD.subtract(s[0], tn[1]), CU.add(s[1], tn[1])), SQPI)
        need(s[0] <= d[0][1] and d[0][0] <= s[1], 'h_function')

# ---------------------------------------------------------------- Lemma 1's k-integral, checked by a separate bracket
# int_0^inf k^(-11/3) e^(-12 k^2 - a^2/(36 k^2)) dk = (432/a^2)^(2/3) K_{4/3}(2a/sqrt3) at three values of a, against
# monotone cell bounds of the left side (k^(-11/3) and e^(-12 k^2) decrease, e^(-c/k^2) increases).
for a_s in ('0.5', '2', '5'):
    a = pt(Dec(a_s))
    c = div(mul(a, a), q(36))
    rhs = mul(ipow(div(q(432), mul(a, a)), Fr(2, 3)), bessel_k_ladder(mul(B, a))[0])
    kmin, kmax, n = Dec("0.004"), Dec("4"), 10000
    r = CN.power(CN.divide(kmax, kmin), CN.divide(Dec(1), Dec(n)))
    ks = [kmin] + [Dec(format(CN.multiply(kmin, CN.power(r, Dec(i))), '.11e')) for i in range(1, n)] + [kmax]
    lo_s, hi_s = Z, Z
    for k0, k1 in zip(ks, ks[1:]):
        dk = CU.subtract(k1, k0)
        f_hi = mul(mul(ipow(pt(k0), Fr(-11, 3)), iexp(mul(q(-12), pt(CD.multiply(k0, k0))))),
                   iexp(neg(div(c, pt(CU.multiply(k1, k1))))))
        f_lo = mul(mul(ipow(pt(k1), Fr(-11, 3)), iexp(mul(q(-12), pt(CU.multiply(k1, k1))))),
                   iexp(neg(div(c, pt(CD.multiply(k0, k0))))))
        hi_s = CU.add(hi_s, CU.multiply(f_hi[1], dk))
        lo_s = CD.add(lo_s, CD.multiply(f_lo[0], CD.subtract(k1, k0)))
    # outside [kmin, kmax]: k^(-11/3) e^(-c/k^2) <= kmin^(-11/3) e^(-c/kmin^2) is increasing on (0, kmin] when
    # kmin^2 < 6c/11, and e^(-12 k^2) k^(-11/3) <= e^(-12 k^2) kmax^(-11/3) above kmax
    need(CU.multiply(kmin, kmin) < CD.multiply(div(q(6), q(11))[0], c[0]), 'representation')
    low_part = mul(mul(ipow(pt(kmin), Fr(-11, 3)), iexp(neg(div(c, pt(CD.multiply(kmin, kmin)))))), pt(kmin))
    high_part = mul(mul(ipow(pt(kmax), Fr(-11, 3)), iexp(mul(q(-12), pt(CD.multiply(kmax, kmax))))),
                    div(ONE, mul(q(24), pt(kmax))))                      # int_K^inf e^(-12k^2) dk <= e^(-12K^2)/(24K)
    hi_s = CU.add(CU.add(hi_s, low_part[1]), high_part[1])
    need(lo_s <= rhs[1] and rhs[0] <= hi_s, 'representation')
    need(CU.subtract(hi_s, lo_s) < CD.multiply(Dec('0.02'), rhs[0]), 'representation')

# the constant of Lemma 1, built from its derivation: 16/15 from (0.1), 1/3 from dB = da/(3k), (4 pi)^(-1/2) from the
# density of B; checked against Lemma 1's literal 16/45, and by the identity KJ * sqrt(4 pi) * 45/16 = 1
KJ = mul(mul(q(Fr(16, 15)), q(1 if MUT == 'M8' else Fr(1, 3))), div(ONE, isqrt(mul(q(4), PI))))
KJ_LIT = div(q(Fr(16, 45)), isqrt(mul(q(4), PI)))
need(KJ[0] <= KJ_LIT[1] and KJ_LIT[0] <= KJ[1], 'representation')
need(contains(mul(mul(KJ, isqrt(mul(q(4), PI))), q(Fr(45, 16))), Dec(1)), 'representation')

# ---------------------------------------------------------------- the quadrature machinery against a closed form
# With h replaced by a^3: int_0^inf a^3 psi(a) da = C432 int_0^inf a^(5/3) K_{4/3}(b a) da = C432 2^(2/3) b^(-8/3)
# Gamma(2/3) Gamma(2), by int_0^inf a^(mu-1) K_nu(b a) da = 2^(mu-2) b^(-mu) Gamma((mu-nu)/2) Gamma((mu+nu)/2).


def cube_derivs(a):
    return [ipow_int(a, 3), mul(q(3), mul(a, a)), mul(q(6), a), q(6), (Z, Z)]


TGT_CUBE = mul(mul(C432, ipow(q(2), Fr(2, 3))), mul(ipow(B, Fr(-8, 3)), G23))
cube, cube_err = simpson(GRID, cube_derivs, 'moment')
cube_lo = CD.subtract(cube[0], cube_err)
cube_hi = CU.add(CU.add(CU.add(cube[1], cube_err), tail_low(ONE, 3)[1]), tail_high()[1])
need(cube_lo <= TGT_CUBE[1] and TGT_CUBE[0] <= cube_hi, 'moment')
need(CU.subtract(cube_hi, cube_lo) < Dec('1e-5'), 'moment')

# ---------------------------------------------------------------- J
core, core_err = simpson(GRID, h_derivs, 'J_cells')
lowtail = tail_low(div(q(Fr(32, 35)), SQPI), Fr(7, 2))
hightail = tail_high()
need(lowtail[1] < Dec('1e-9') and hightail[1] < Dec('1e-9'), 'tails')
I_lo = CD.subtract(core[0], core_err)
I_hi = CU.add(CU.add(CU.add(core[1], core_err), lowtail[1]), hightail[1])
if MUT == 'M13':
    I_hi = CU.add(core[1], core_err)
J = mul(KJ, (I_lo, I_hi))
need(J[0] > 0 and width(J) < Dec('1e-7'), 'J_cells')
# the enclosure is at least as wide as its remainder and tail allowances (KJ > 0, I_lo > 0): none of them was dropped
need(width(J) >= CD.multiply(KJ[0], CD.add(CD.multiply(Dec(2), core_err), CD.add(lowtail[1], hightail[1]))), 'J_cells')
# two independent floating-point evaluations (note C3's Slice C referee: 4.1977819815839; mpmath: 4.1977819815839038)
need(contains(J, Dec('4.1977819815839038')), 'assembly')

# ---------------------------------------------------------------- the consequences
S2 = div(mul(q(25), SQ3), mul(q(48), mul(PI, PI)))                         # 25 sqrt3 / (48 pi^2)
S3 = div(mul(q(125), isqrt(q(30))), mul(q(192), mul(PI, mul(PI, PI))))     # 125 sqrt30 / (192 pi^3)
ETA = {(2, 10): (Fr(588, 10 ** 11), Fr(781, 10 ** 8)), (3, 10): (Fr(197, 10 ** 9), Fr(497, 10 ** 6)),
       (2, 24): (Fr(488, 10 ** 112), Fr(648, 10 ** 109)), (3, 24): (Fr(164, 10 ** 110), Fr(413, 10 ** 107))}
J30 = div(J, q(30))
NEG_IQ_LO, D_UP = q(Fr(6104056, 10 ** 7)), q(Fr(438822, 10 ** 6))          # note DC: -I~_quad >= 0.6104056, D <= 0.438822
if MUT == 'M9':
    D_UP = q(Fr(338822, 10 ** 6))
model = sub(add(J30, NEG_IQ_LO), D_UP)              # its lower end bounds J/30 - I~ from below
need(Dec('0.31150') <= model[0] <= Dec('0.31151'), 'corollary')
values = {}
for (d, L), (ec, er) in sorted(ETA.items()):
    S = S2 if d == 2 else S3
    c3_lo = mul(J30 if MUT == 'M14' else sub(J30, q(ec)), S)[0]
    c3_hi = mul(add(J30, q(ec)), S)[1]
    coef_lo = mul(sub(sub(model, q(ec)), q(er)), S)[0]
    need(c3_lo > 0 and coef_lo > 0, 'corollary')
    values['d%d_L%d' % (d, L)] = {'c3': [str(CD.quantize(c3_lo, Dec('1e-9'))), str(CU.quantize(c3_hi, Dec('1e-9')))],
                                  'coef_lo': str(CD.quantize(coef_lo, Dec('1e-6')))}

# ---------------------------------------------------------------- the certified printed strings, pinned to the note's text
J_STR = [str(CD.quantize(J[0], Dec('1e-10'))), str(CU.quantize(J[1], Dec('1e-10')))]
REM_STR = str(CU.quantize(CU.multiply(KJ[1], core_err), Dec('1e-12')))
TAILS_STR = str(CU.quantize(CU.multiply(KJ[1], CU.add(lowtail[1], hightail[1])), Dec('1e-15')))
MODEL_STR = str(CD.quantize(model[0], Dec('1e-6')))
PINNED = {
    'J': ['4.1977819534', '4.1977820097'],
    'J_simpson_remainder': '2.8099E-8',
    'J_tails': '1.5287E-11',
    'model_coef_lo': '0.311509',
    'values': {'d2_L10': {'c3': ['0.012789638', '0.012789640'], 'coef_lo': '0.028472'},
               'd2_L24': {'c3': ['0.012789638', '0.012789639'], 'coef_lo': '0.028472'},
               'd3_L10': {'c3': ['0.016092288', '0.016092334'], 'coef_lo': '0.035768'},
               'd3_L24': {'c3': ['0.016092310', '0.016092312'], 'coef_lo': '0.035825'}},
}
need(J_STR == PINNED['J'], 'pinned')
need(REM_STR == PINNED['J_simpson_remainder'], 'pinned')
need(TAILS_STR == PINNED['J_tails'], 'pinned')
need(MODEL_STR == PINNED['model_coef_lo'], 'pinned')
for key in sorted(PINNED['values']):
    need(values[key] == PINNED['values'][key], 'pinned')

out = {
    'note': 'CJ',
    'precision': PREC,
    'cells': len(GRID) - 1,
    'J': J_STR,
    'J_simpson_remainder': REM_STR,
    'J_tails': TAILS_STR,
    'moment_check': [str(CD.quantize(cube_lo, Dec('1e-9'))), str(CU.quantize(cube_hi, Dec('1e-9'))),
                     str(CN.quantize(TGT_CUBE[0], Dec('1e-9')))],
    'model_coef_lo': MODEL_STR,
    'values': values,
    'checks': dict(sorted(COUNT.items())),
    'result': 'J in the printed interval',
}
print(json.dumps(out, sort_keys=True))
