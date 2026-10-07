"""Note DC controls: a certified upper bound for the model number D (Python standard library only).

D <= T1 + T2 + T3 (note DC, Proposition 1).  This script encloses each term by outward-rounded decimal
interval arithmetic on explicit partitions, with analytic tails; it checks the note's main polynomial
identities, its constants, and the cell factors that the production loops actually use (sampled, after the run).  Usage: python3 dc_exact.py [--mutant M1..M18]
"""
import decimal
import json
import sys
from fractions import Fraction as Fr

USAGE = 'usage: dc_exact.py [--mutant M1..M18]'
MUTANTS = ['M%d' % i for i in range(1, 19)]
if len(sys.argv) == 1:
    MUT = None
elif len(sys.argv) == 3 and sys.argv[1] == '--mutant' and sys.argv[2] in MUTANTS:
    MUT = sys.argv[2]
else:
    sys.stderr.write(USAGE + '\n')
    sys.exit(2)

PREC = 24
CD = decimal.Context(prec=PREC, rounding=decimal.ROUND_FLOOR)
CU = decimal.Context(prec=PREC, rounding=decimal.ROUND_CEILING)
CN = decimal.Context(prec=PREC, rounding=decimal.ROUND_HALF_EVEN)
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
    return (-a[1], -a[0])


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


# monotone table for e^{-x}, x >= 0: U[k] >= e^{-k/EXP_H} >= L[k]
EXP_H, EXP_N = 1024, 60 * 1024
EXP_U = [CU.next_plus(CN.exp(CN.divide(Dec(-k), Dec(EXP_H)))) for k in range(EXP_N + 1)]
EXP_L = [max(Z, CD.next_minus(CN.exp(CN.divide(Dec(-k), Dec(EXP_H))))) for k in range(EXP_N + 1)]
EXP_HD = Dec(EXP_H)


def upx(x_lo):
    """Upper bound of e^{-x} for every x >= x_lo >= 0."""
    k = int(CD.multiply(x_lo, EXP_HD).to_integral_value(rounding=decimal.ROUND_FLOOR))
    return EXP_U[min(max(k, 0), EXP_N)]


def lox(x_hi):
    """Lower bound of e^{-x} for every 0 <= x <= x_hi."""
    k = int(CU.multiply(x_hi, EXP_HD).to_integral_value(rounding=decimal.ROUND_CEILING))
    return EXP_L[k] if k <= EXP_N else Z


def contains(a, x):
    return a[0] <= x <= a[1]


# ---------------------------------------------------------------- polynomials over Q (lists, low degree first)
def padd(p, r):
    n = max(len(p), len(r))
    return [(p[i] if i < len(p) else 0) + (r[i] if i < len(r) else 0) for i in range(n)]


def pmul(p, r):
    out = [Fr(0)] * (len(p) + len(r) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(r):
            out[i + j] += a * b
    return out


def pscale(p, c):
    return [c * a for a in p]


def ptrim(p):
    p = [Fr(a) for a in p]
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def pcompose(p, r):
    # p(r(x))
    out = [Fr(0)]
    for a in reversed(p):
        out = padd(pmul(out, r), [a])
    return ptrim(out)


def peval(p, x):
    s = Fr(0)
    for a in reversed(p):
        s = s * x + a
    return s


def pderiv(p):
    return ptrim([i * p[i] for i in range(1, len(p))] or [0])


# ---------------------------------------------------------------- constants: pi (Machin) and Gamma (series)
def atan_inv(n, terms):
    s = Fr(0)
    for k in range(terms):
        s += Fr((-1) ** k, (2 * k + 1) * n ** (2 * k + 1))
    nxt = Fr((-1) ** terms, (2 * terms + 1) * n ** (2 * terms + 1))
    return (min(s, s + nxt), max(s, s + nxt))


def rat_iv(lo, hi):
    return (CD.divide(Dec(lo.numerator), Dec(lo.denominator)), CU.divide(Dec(hi.numerator), Dec(hi.denominator)))


a5, a239 = atan_inv(5, 40), atan_inv(239, 12)
PI = rat_iv(16 * a5[0] - 4 * a239[1], 16 * a5[1] - 4 * a239[0])
need(contains(PI, Dec('3.141592653589793238462643383279502884')), 'pi')
need(PI[1] - PI[0] < Dec('1e-20'), 'pi')

GX, GN = 50, (20 if MUT == 'M8' else 220)


def gamma_iv(a):
    """Gamma(a), a rational in (0, 3]: gamma(a, X) by its alternating series, plus Gamma(a, X) >= 0 bounded above."""
    a = Fr(a)
    need(GN > GX + 1, 'gamma')
    s, term = Fr(0), Fr(1)
    for n in range(GN):
        s += term / (n + a)
        term = term * (-GX) / (n + 1)
    tail = abs(term) / (GN + a)           # first omitted term; terms decrease for n >= X
    xa = ipow(pt(Dec(GX)), a)
    lo = mul(xa, rat_iv(s - tail, s - tail))[0]
    hi = mul(xa, rat_iv(s + tail, s + tail))[1]
    # Gamma(a, X) <= X^{a-1} e^{-X} / (1 - (a-1)/X) for 1 <= a < X; <= X^{a-1} e^{-X} for a <= 1
    c = Fr(1) if a <= 1 else 1 / (1 - (a - 1) / GX)
    up = mul(mul(ipow(pt(Dec(GX)), a - 1), iexp(pt(Dec(-GX)))), q(c))[1]
    return (lo, CU.add(hi, up))


G1, G2, GH = gamma_iv(1), gamma_iv(2), gamma_iv(Fr(1, 2))
need(contains(G1, Dec(1)) and contains(G2, Dec(1)), 'gamma')
need(mul(GH, GH)[0] <= PI[1] and mul(GH, GH)[1] >= PI[0], 'gamma')
need(G1[1] - G1[0] < Dec('1e-18'), 'gamma')
GAM = {r: gamma_iv(r) for r in (Fr(1, 6), Fr(7, 6), Fr(11, 6), Fr(11, 12), Fr(5, 4), Fr(3, 4), Fr(7, 3), Fr(1, 2),
                                 Fr(7, 4), Fr(3, 2))}
# crude bounds used in the tails (log-convexity: Gamma <= 1 on [1, 2]; Gamma(x) = Gamma(1 + x)/x)
for r, b in ((Fr(7, 6), 1), (Fr(11, 6), 1), (Fr(5, 4), 1), (Fr(11, 12), Fr(12, 11)), (Fr(3, 4), Fr(4, 3)),
             (Fr(7, 3), Fr(4, 3)), (Fr(7, 4), 1), (Fr(3, 2), 1)):
    need(GAM[r][1] <= q(b)[0], 'gamma')

SQRT_PI = isqrt(PI)
SQ3 = isqrt(q(3))
SQ6 = isqrt(q(6))
SQ4PI = isqrt(mul(q(4), PI))
SQ2PI = isqrt(mul(q(2), PI))
PHI0 = div(q(1), SQ4PI if MUT == 'M18' else SQ2PI)     # phi(0) = 1/sqrt(2 pi)
C6 = mul(q(576), SQ3 if MUT == 'M11' else SQ6)          # s = C6 tau^2 g, C6 = 576 sqrt6
# Lemma 4: k = tau gamma^2; gamma^6 k^{-8/3} dk = tau^{-8/3} |gamma|^{8/3} dtau; the t-density adds tau^{-1};
# s = 576 sqrt6 k^2/|gamma|^3 = 576 sqrt6 tau^2 |gamma|.  Constants: (1/2400) (t-density 1/(12 sqrt(4 pi))) (2: evenness)
need(6 - 2 * Fr(8, 3) + 2 == Fr(8, 3) and Fr(-8, 3) - 1 == Fr(-11, 3) and 2 * 2 - 3 == 1, 'lemma4')
C1_RAT = Fr(1, 2400) * 2 / (6 if MUT == 'M15' else 12)       # C1 sqrt(4 pi)
C3_RAT = Fr(1, 2400) * 2 / 12 / 4                             # C3 pi, since (4 pi)^{-1/2} (4 pi)^{-1/2} = 1/(4 pi)
need(C1_RAT == Fr(1, 14400) and C3_RAT == Fr(1, 57600), 'lemma4')
C1 = div(q(C1_RAT), SQ4PI)       # T1 weight constant 1/(14400 sqrt(4 pi))
C3 = div(q(C3_RAT), PI)          # T3 weight constant 1/(57600 pi)
# the defining identities, written independently of the lines above
need(contains(mul(mul(mul(C1, C1), q(14400 ** 2)), mul(q(4), PI)), Dec(1)), 'lemma4')
need(contains(mul(mul(C3, q(57600)), PI), Dec(1)), 'lemma4')
need(contains(mul(C6, C6), Dec(576 ** 2 * 6)), 'lemma4')
need(contains(mul(mul(PHI0, PHI0), mul(q(2), PI)), Dec(1)), 'lemma4')
if MUT == 'M4':
    C1 = mul(C1, q(2))
if MUT == 'M5':
    C3 = mul(C3, q(2))


# ---------------------------------------------------------------- R2 = I0 - T2 (#244 (3.3)) and its exact facts
def T2poly(t):
    return add(sub(q(Fr(20, 3)), mul(q(20), t)), mul(q(Fr(52, 3)), mul(t, t)))


P0C = [Fr(11, 3), Fr(-21, 2), Fr(16 if MUT == 'M6' else 17, 2), Fr(-4, 3)]
P1C = [Fr(3), Fr(-15, 2), Fr(9, 2)]                # (3/2)(1 - t)(2 - 3t)
T2C = [Fr(20, 3), Fr(-20), Fr(52, 3)]


def polyiv(c, t):
    s = q(c[-1])
    for a in reversed(c[:-1]):
        s = add(mul(s, t), q(a))
    return s


def R2iv(x):
    """Enclosure of R2(x) for an exact Decimal x."""
    t = pt(x)
    if 3 * Fr(x) <= 2:
        S = isqrt(sub(q(1), mul(q(Fr(4, 3)), t)))
        return sub(add(polyiv(P0C, t), mul(polyiv(P1C, t), S)), polyiv(T2C, t))
    if x <= 1:
        u = sub(mul(q(2), t), q(1))
        return sub(mul(mul(u, u), div(sub(q(2), t), q(3))), polyiv(T2C, t))
    return sub(sub(t, q(Fr(2, 3))), polyiv(T2C, t))


# (a) the pieces of (3.3) agree at t = 2/3 (S = 1/3) and t = 1; R2(0) = 0
need(peval(P0C, Fr(2, 3)) + peval(P1C, Fr(2, 3)) * Fr(1, 3) == Fr(4, 81), 'R2_formula')
need((2 * Fr(2, 3) - 1) ** 2 * (2 - Fr(2, 3)) / 3 == Fr(4, 81), 'R2_formula')
need(peval(P0C, 0) + peval(P1C, 0) - peval(T2C, 0) == 0, 'R2_formula')
need(Fr(1) ** 2 * (2 - 1) / 3 == 1 - Fr(2, 3), 'R2_formula')                       # the pieces agree at t = 1
for xs in ('0.001', '0.01'):
    x = Dec(xs)
    ratio = div(R2iv(x), q(Fr(x) ** 3))
    need(Dec('-3.2') < ratio[0] and ratio[1] < Dec('-3.0'), 'R2_formula')   # R2(t)/t^3 -> -28/9
# (b) monotonicity: with t = 3(1 - S^2)/4, 16 S R2'(t) = (S - 1)^2 W(S) on t < 2/3
tS = [Fr(3, 4), Fr(0), Fr(-3, 4)]
dP0, dP1, dT2 = pderiv(P0C), pderiv(P1C), pderiv(T2C)
# 16 S (P0' + P1' S + P1 S' - T2') with S' = -2/(3S):  16 S P0' + 16 S^2 P1' - (32/3) P1 - 16 S T2'
lhs = padd(padd(pmul([0, 16], pcompose(dP0, tS)), pmul([0, 0, 16], pcompose(dP1, tS))),
           padd(pscale(pcompose(P1C, tS), Fr(-32, 3)), pmul([0, -16], pcompose(dT2, tS))))
QC = [Fr(1), Fr(-94), Fr(-206 if MUT == 'M1' else -207), Fr(-36)]     # the note's W(S)
need(ptrim(lhs) == ptrim(pmul(pmul([-1, 1], [-1, 1]), QC)), 'R2_monotone')
need(peval(QC, Fr(1, 3)) < 0 and all(c <= 0 for c in pderiv(QC)), 'R2_monotone')   # W < 0 on S >= 1/3
# t in [2/3, 1]: R2' = (2t - 1)(3 - 2t) + 20 - (104/3) t <= 1 + 20 - (104/3)(2/3) < 0; t >= 1: 21 - 104/3 < 0
need(1 + 20 - Fr(104, 3) * Fr(2, 3) < 0 and 21 - Fr(104, 3) < 0, 'R2_monotone')
need(ptrim([Fr(-3), Fr(8), Fr(-4)]) == ptrim(padd([1], pscale(pmul([-1, 1], [-1, 1]), -4))), 'R2_monotone')  # = 1 - 4(t-1)^2
MIDC = [Fr(2, 3), Fr(-3), Fr(4), Fr(-4, 3)]                                          # (2t - 1)^2 (2 - t)/3
need(ptrim(pmul(pmul([-1, 2], [-1, 2]), [Fr(2, 3), Fr(-1, 3)])) == MIDC, 'R2_monotone')
need(pderiv(padd(MIDC, pscale(T2C, -1))) ==
     ptrim(padd([Fr(21), Fr(-104, 3)], pscale(pmul([-1, 1], [-1, 1]), -4))), 'R2_monotone')  # 21 - 4(t-1)^2 - (104/3)t
need(pderiv(padd([Fr(-2, 3), Fr(1)], pscale(T2C, -1))) == [Fr(21), Fr(-104, 3)], 'R2_monotone')
# (c) majorant: R2(-t) = -3 - 19t/2 - 53t^2/6 + 4t^3/3 + (3/2)(1 + t)(2 + 3t) S+ ; P1(-t) = (3/2)(1 + t)(2 + 3t)
m1 = [Fr(0), Fr(-1)]
R2m_poly = padd(pcompose(P0C, m1), pscale(pcompose(T2C, m1), -1))
need(ptrim(R2m_poly) == ptrim([Fr(-3), Fr(-19, 2), Fr(-53, 6), Fr(4, 3)]), 'R2_majorant')
need(ptrim(pcompose(P1C, m1)) == ptrim(pscale(pmul([1, 1], [2, 3]), Fr(3, 2))), 'R2_majorant')
# with S+ <= 1 + (2/sqrt3) sqrt t:  R2(-t) <= (4/3)t^3 + 3 sqrt3 t^{5/2} - (13/3)t^2 + 5 sqrt3 t^{3/2} - 2t + 2 sqrt3 t^{1/2}
poly_part = padd(R2m_poly, pscale(pmul([1, 1], [2, 3]), Fr(3, 2)))
need(ptrim(poly_part) == ptrim([Fr(0), Fr(-2), Fr(-13, 3), Fr(4, 3)]), 'R2_majorant')
need(ptrim(pmul([1, 1], [2, 3])) == [2, 5, 3], 'R2_majorant')
# |W(S)| <= 755 on [1, sqrt(7/3)] (W decreasing, W(sqrt(7/3)) = -(36 (7/3) + 94) sqrt(7/3) - 207 (7/3) + 1)
qv = add(neg(mul(add(q(Fr(36 * 7, 3)), q(94)), isqrt(q(Fr(7, 3))))), q(Fr(-207 * 7, 3) + 1))
need(qv[0] >= -755, 'R2_majorant')
# so R2(-t) <= int_0^t (2u/3)^2 755/16 du = (755/108) t^3 <= 7 t^3 on [0, 1]; for t >= 1, U(t) <= (2/3 + 5 sqrt3) t^3
need(Fr(755, 108) <= 7 and add(q(Fr(2, 3)), mul(q(5), SQ3))[1] <= 10, 'R2_majorant')
need(ptrim(padd(pmul([1, Fr(2, 3)], [1, Fr(2, 3)]), [-1, Fr(-4, 3)])) == [0, 0, Fr(4, 9)], 'R2_majorant')   # (1 + 2u/3)^2 - (1 + 4u/3)
need(Fr(4, 9) * Fr(755, 16) / 3 == Fr(755, 108), 'R2_majorant')                    # int_0^t (2u/3)^2 (755/16) du

# ---------------------------------------------------------------- Birnbaum's Mills-ratio bound (note DC, Lemma 3)
X2 = [0, 0, 1]  # x^2
bir = 3 if MUT == 'M2' else 4
need(ptrim(padd(pmul(pmul(padd(X2, [1]), padd(X2, [1])), padd(X2, [bir])),
                pscale(pmul(X2, pmul(padd(X2, [3]), padd(X2, [3]))), -1))) == [4], 'mills')
need(ptrim(padd(pmul(padd(X2, [2]), padd(X2, [2])), pscale(pmul(X2, padd(X2, [4])), -1))) == [4], 'mills')
# Lemma 3's reductions in Q[x][w]/(w^2 - x^2 - 4), elements (P, R) = P + R w:
#   2w(-1 + x b - b') with b = (w - x)/2, b' = (x/w - 1)/2 equals -2w + (x w^2 - x^2 w) - (x - w) = x^3 + 3x - (x^2 + 1) w
W2 = padd(X2, [4])
red = (padd(pmul([0, 1], W2), [0, -1]), [-2, 0, -1, 0])
red = (ptrim(red[0]), ptrim(padd(red[1], [1])))
need(red == (ptrim([0, 3, 0, 1]), ptrim([-1, 0, -1])), 'mills')
#   1 - a b(a) = 1 - a (w - a)/2 = (2 + a^2)/2 - (a/2) w
need((ptrim(padd([1], pscale(pmul([0, 1], [0, 1]), Fr(1, 2)))), [0, Fr(-1, 2)]) ==
     (ptrim([1, 0, Fr(1, 2)]), [0, Fr(-1, 2)]), 'mills')


def thetap_iv(a):
    """theta+(a) = 2 phi(a) / (2 + a^2 + a sqrt(a^2 + 4)) for an exact Decimal a >= 0."""
    A = pt(a)
    num = mul(q(2), mul(PHI0, iexp(neg(div(mul(A, A), q(2))))))
    den = add(add(q(2), mul(A, A)), mul(A, isqrt(add(mul(A, A), q(4)))))
    return div(num, den)


TH_STEP, TH_N = 200, 8000          # table at a = k/200, k <= 8000 (a <= 40)
THTAB = [thetap_iv(CN.divide(Dec(k), Dec(TH_STEP)))[1] for k in range(TH_N + 1)]


def th_idx_scaled(x):
    # x is a lower bound of TH_STEP * a; the table entry at floor(x) / TH_STEP <= a bounds theta+(a) above
    if MUT == 'M9':
        return min(max(int(x.to_integral_value(rounding=decimal.ROUND_CEILING)), 0), TH_N)
    return min(max(int(x.to_integral_value(rounding=decimal.ROUND_FLOOR)), 0), TH_N)


def th_index(a_lo):
    return th_idx_scaled(CD.multiply(a_lo, TH_STEP))


for s_ in ('0', '0.0049', '0.5', '0.731', '1.0001', '2.5', '3.14159', '7.777', '12.3456', '39.999', '55'):
    a = Dec(s_)
    need(thetap_iv(a)[1] <= THTAB[th_index(a)], 'theta_table')
need(all(THTAB[k + 1] <= THTAB[k] for k in range(TH_N)), 'theta_table')
need(thetap_iv(Z)[1] >= PHI0[0] and thetap_iv(Z)[0] <= PHI0[1], 'theta_table')

# ---------------------------------------------------------------- T2 (closed form)
need((Fr(1, 32) - Fr(13, 480 if MUT == 'M3' else 486)) * 576 * 576 * 6 / (2 * 2400) == Fr(28, 15), 'T2')
T2 = mul(mul(q(Fr(28, 15)), ipow(pt(Dec(12)), Fr(-7, 6))), GAM[Fr(7, 6)])
need(T2[0] >= Dec('0.0953758') and T2[1] <= Dec('0.0953759'), 'T2')

# ---------------------------------------------------------------- grids (exact decimals)
CEIL3 = decimal.Context(prec=3, rounding=decimal.ROUND_CEILING)
CEIL2 = decimal.Context(prec=2, rounding=decimal.ROUND_CEILING)
CEIL6 = decimal.Context(prec=6, rounding=decimal.ROUND_CEILING)


def geo_grid(a, b, ratio):
    pts, r = [Dec(a)], Dec(ratio)
    while pts[-1] < Dec(b):
        pts.append(CEIL6.multiply(pts[-1], r))
    return pts


def t1_grid(tmax, hrel='0.01', t0='1e-7'):
    """0, then geometric points from t0 with ratio 1 + hrel (rounded up to 6 significant digits), up to >= tmax."""
    pts, r = [Z, Dec(t0)], CN.add(Dec(1), Dec(hrel))
    while pts[-1] < tmax:
        pts.append(CEIL6.multiply(pts[-1], r))
    return pts


def t3_grid(tmax, hk='0.005', hrel='0.02', sym=False):
    """Increasing exact points: fine step hk on [-1, 1], relative step hrel beyond; from <= -tmax to 1 (or to >= tmax)."""
    neg_pts = [Dec(1)]
    while neg_pts[-1] > -tmax:
        x = neg_pts[-1]
        h = Dec(hk) if x > -1 else max(Dec(hk), CEIL3.multiply(-x, Dec(hrel)))
        neg_pts.append(CN.subtract(x, h))
    pts = neg_pts[::-1]
    if sym:
        while pts[-1] < tmax:
            x = pts[-1]
            h = Dec(hk) if x < 1 else max(Dec(hk), CEIL3.multiply(x, Dec(hrel)))
            pts.append(CN.add(x, h))
    return pts


def increasing(pts):
    return all(pts[i] < pts[i + 1] for i in range(len(pts) - 1))


# ---------------------------------------------------------------- the g-direction: m_p(g) = g^p e^{-g^2/4}
M_CACHE = {}


def m_iv(g, p):
    if g == 0:
        return (Z, Z)
    G = pt(g)
    return iexp(sub(mul(q(p), iln(G)), div(mul(G, G), q(4))))


def m_peak(p):
    # maximum of m_p at g^2 = 2p:  exp((p/2) ln(2p) - p/2)
    return iexp(sub(mul(q(p / 2), iln(q(2 * p))), q(p / 2)))


PEAK = {Fr(8, 3): m_peak(Fr(8, 3)), Fr(11, 3): m_peak(Fr(11, 3))}
need(Fr(8, 3) * 2 == Fr(16, 3), 'gstar')        # d/dg log m_{8/3} = (8/3)/g - g/2 vanishes at g^2 = 16/3
need(Fr(11, 3) * 2 == Fr(22, 3), 'gstar')


def g_cells(dg, n, p):
    """Per cell j = [j dg, (j+1) dg]: (upper bound of sup m_p, lower bound of inf m_p); m_p is log-concave."""
    key = (dg, n, p)
    if key not in M_CACHE:
        vals = [m_iv(CN.multiply(dg, Dec(j)), p) for j in range(n + 1)]
        out = []
        for j in range(n):
            ga, gb = Fr(dg) * j, Fr(dg) * (j + 1)
            if gb * gb <= 2 * p:
                sup = vals[j + 1][1]
            elif ga * ga >= 2 * p:
                sup = vals[j][1]
            else:
                sup = PEAK[p][1]
            out.append((sup, min(vals[j][0], vals[j + 1][0])))
        M_CACHE[key] = out
    return M_CACHE[key]


def g_step(tau, scale, n):
    """dg (2 significant digits, rounded up) with n dg >= min(14, scale (12 tau^2)^{-1/4})."""
    greq = min(Fr(14), Fr(scale) * Fr(ipow(mul(q(12), pt(CN.multiply(tau, tau))), Fr(-1, 4))[1]))
    return CEIL2.divide(Dec(greq.numerator), Dec(greq.denominator) * n)


def g_tail(tau, G, p):
    """Upper bound of int_G^inf m_p(g) e^{-12 tau^2 g^4} dg (Gamma factors bounded crudely)."""
    gam2 = {Fr(8, 3): Fr(1), Fr(11, 3): Fr(4, 3)}[p]           # Gamma((p+1)/2) <= .
    gam4 = {Fr(8, 3): Fr(12, 11), Fr(11, 3): Fr(1)}[p]          # Gamma((p+1)/4) <= .
    Gi = pt(G)
    b1 = mul(mul(iexp(neg(div(mul(Gi, Gi), q(8)))), q(gam2 / 2)), ipow(q(8), (p + 1) / 2))
    t6 = mul(q(6), pt(CN.multiply(tau, tau)))
    b2 = mul(mul(iexp(neg(mul(t6, mul(mul(Gi, Gi), mul(Gi, Gi))))), q(gam4 / 4)), ipow(t6, -(p + 1) / 4))
    return min(b1[1], b2[1])


def g_integral(tau, p, n, scale=6, want_lower=True):
    """Enclosure of int_0^inf m_p(g) e^{-12 tau^2 g^4} dg."""
    dg = g_step(tau, scale, n)
    cells = g_cells(dg, n, p)
    t12 = CN.multiply(Dec(12), CN.multiply(tau, tau))
    up, lo = Z, Z
    for j in range(n):
        ga = CN.multiply(dg, Dec(j))
        gb = CN.add(ga, dg)
        e_up = upx(CD.multiply(t12, CD.multiply(CD.multiply(ga, ga), CD.multiply(ga, ga))))
        up = CU.add(up, CU.multiply(CU.multiply(dg, cells[j][0]), e_up))
        if want_lower:
            e_lo = lox(CU.multiply(t12, CU.multiply(CU.multiply(gb, gb), CU.multiply(gb, gb))))
            lo = CD.add(lo, CD.multiply(CD.multiply(dg, cells[j][1]), e_lo))
    up = CU.add(up, g_tail(tau, CN.multiply(dg, Dec(n)), p))
    return (lo, up)


MFAC = div(q(2), SQ4PI)       # M(tau) = (2/sqrt(4 pi)) int m_{8/3} e^{-12 tau^2 g^4} dg
if MUT == 'M10':
    MFAC = div(q(2), mul(q(4), PI))


def M_enc(tau, n=280):
    return mul(MFAC, g_integral(tau, Fr(8, 3), n))


# M(0) and N(0) in closed form, compared with the g-cell enclosures at tau = 0+ (a check of the g machinery)
M0 = mul(div(ipow(q(2), Fr(8, 3)), SQRT_PI), GAM[Fr(11, 6)])               # E|g|^{8/3} = 2^{8/3} Gamma(11/6)/sqrt(pi)
need(M_enc(Dec('1e-9'))[0] <= M0[1] and M0[0] <= M_enc(Dec('1e-9'))[1], 'g_machinery')
N0 = mul(mul(q(Fr(1, 2)), ipow(q(4), Fr(7, 3))), GAM[Fr(7, 3)])            # int g^{11/3} e^{-g^2/4} = (1/2) 4^{7/3} Gamma(7/3)
need(g_integral(Dec('1e-9'), Fr(11, 3), 200)[0] <= N0[1] <= CU.multiply(g_integral(Dec('1e-9'), Fr(11, 3), 200)[1], Dec(2)), 'g_machinery')
need(g_integral(Dec('1e-9'), Fr(11, 3), 200)[1] >= N0[0], 'g_machinery')

# ---------------------------------------------------------------- T1 = int dtau int_0^inf dt C1 tau^{-11/3} M(tau) e^{-t^2/(576 tau^2)} R2e(t)
BETA_H = Dec(9)
E_BH = iexp(q(Fr(-81, 8)))                     # e^{-beta_H^2/8}
U_TERMS = [(Fr(3), q(Fr(2, 3))), (Fr(5, 2), mul(q(Fr(3, 2)), SQ3)), (Fr(3, 2), mul(q(Fr(5, 2)), SQ3)), (Fr(1, 2), SQ3)]
GUP = {Fr(2): Fr(1), Fr(7, 4): Fr(1), Fr(5, 4): Fr(1), Fr(3, 4): Fr(4, 3), Fr(3, 2): Fr(1)}   # Gamma(.) <= .


def tpow(x, r):
    return ipow(pt(x), r)


def half_moment(V, n):
    """Upper bound of int_0^inf e^{-t^2/V} t^n dt = (1/2) V^{(n+1)/2} Gamma((n+1)/2)."""
    return mul(mul(q(Fr(1, 2)), ipow(V, (n + 1) / 2)), q(GUP[(n + 1) / 2]))


def t1_cell(ta, tb, m_a, m_b):
    """T1 on the tau-cell [ta, tb]: pa >= dtau sup C1 tau^{-11/3} M(tau), pb <= dtau inf C1 tau^{-11/3} M(tau)
    (M decreasing; m_a, m_b enclose M(ta), M(tb)); and the exact denominators 576 ta^2, 576 tb^2."""
    dtau = CN.subtract(tb, ta)
    ts, ms = (tb, m_b) if MUT == 'M16' else (ta, m_a)
    pa = CU.multiply(CU.multiply(C1[1], tpow(ts, Fr(-11, 3))[1]), CU.multiply(ms[1], dtau))
    pb = CD.multiply(CD.multiply(C1[0], tpow(tb, Fr(-11, 3))[0]), CD.multiply(m_b[0], dtau))
    return pa, pb, CN.multiply(Dec(576), CN.multiply(ta, ta)), CN.multiply(Dec(576), CN.multiply(tb, tb))


def gauss_up(u0, den):
    """Upper bound of e^{-t^2/(576 tau^2)} for t >= u0 >= 0 and 576 tau^2 <= den."""
    return upx(CD.divide(CD.multiply(u0, u0), den))


def gauss_lo(u1, den):
    """Lower bound of e^{-t^2/(576 tau^2)} for 0 <= t <= u1 and 576 tau^2 >= den."""
    return lox(CU.divide(CU.multiply(u1, u1), den))


def t1_gauss(u0, u1, den_a, den_b):
    """(Upper bound of the sup, lower bound of the inf) of e^{-t^2/(576 tau^2)} on [u0, u1] x [ta, tb]."""
    return gauss_up(u0, den_b), gauss_lo(u1, den_a)


def rho_up(u0, u1):
    """Upper bound of sup R2e on [u0, u1], 0 <= u0 <= u1: (R2(u0) + R2(-u1))/2, since R2 decreases (Lemma 2(a))."""
    return CU.multiply(Dec('0.5'), CU.add(R2iv(u0)[1], R2iv(-u1)[1]))


LOG = {'T1': [], 'T3': [], 'SEP': [], 'K': []}      # factors used by the production loops on sampled cells


def T1_bound(tau_pts, tg, mode, log_cells=()):
    """mode 'R2': (cell sum, tail sum) upper bounds of T1 on [tau_0, tau_N];  mode 'mom': (lower, upper) for t^2."""
    need(increasing(tau_pts) and increasing(tg) and tg[0] == 0, 'partition')
    rho = None
    if mode == 'R2':
        rho = [rho_up(tg[j], tg[j + 1]) for j in range(len(tg) - 1)]
        need(R2iv(Z)[0] <= 0 <= R2iv(Z)[1], 'R2_formula')      # R2(0) = 0, so R2(t) <= 0 for t >= 0
    menc = [M_enc(x) for x in tau_pts]
    up, lo, tails = Z, Z, Z
    prev = tau_pts[0]
    for i in range(len(tau_pts) - 1):
        if MUT == 'M7' and i == 400:
            continue
        ta, tb = tau_pts[i], tau_pts[i + 1]
        need(ta == prev, 'partition')
        prev = tb
        pa, pb, den_a, den_b = t1_cell(ta, tb, menc[i], menc[i + 1])
        tmax = CN.multiply(Dec(12), CN.multiply(tb, BETA_H))
        if MUT == 'M12':
            tmax = CN.divide(tmax, Dec(2))
        J = 0
        while tg[J] < tmax:
            J += 1
        need(tg[J] >= CN.multiply(Dec(12), CN.multiply(tb, BETA_H)), 'partition')
        # cells [0, tg[j0]] (merged) and [tg[j], tg[j+1]] for j0 <= j < J, with tg[j0] <= 12 ta / 1000
        tlo = CN.multiply(Dec('0.012'), ta)
        j0 = 0
        while j0 + 1 < J and tg[j0 + 1] <= tlo:
            j0 += 1
        cells_t = ([(Z, tg[j0], rho_up(Z, tg[j0]) if mode == 'R2' else None)] if j0 > 0 else []) + \
            [(tg[j], tg[j + 1], rho[j] if mode == 'R2' else None) for j in range(j0, J)]
        nct = len(cells_t)
        sample = {0, 1, nct // 4, nct // 2, (3 * nct) // 4, nct - 1} if i in log_cells else ()
        for c, (u0, u1, rj) in enumerate(cells_t):
            dt = CN.subtract(u1, u0)
            eu, el = t1_gauss(u0, u1, den_a, den_b)
            if mode == 'R2':
                dr = CU.multiply(dt, rj)          # an upper bound of dt * rho for either sign of rho
                if rj >= 0:
                    wu, ew = pa, eu
                    up = CU.add(up, CU.multiply(CU.multiply(wu, ew), dr))
                else:
                    wu, ew = pb, el
                    up = CU.add(up, CU.multiply(CD.multiply(wu, ew), dr))
                if c in sample:
                    LOG['T1'].append((ta, tb, u0, u1, wu, ew, rj))
            else:
                up = CU.add(up, CU.multiply(CU.multiply(pa, eu), CU.multiply(dt, CU.multiply(u1, u1))))
                lo = CD.add(lo, CD.multiply(CD.multiply(pb, el), CD.multiply(dt, CD.multiply(u0, u0))))
        # t-tail beyond tg[J] >= 12 tb beta_H:  int_T^inf e^{-t^2/(576 tau^2)} t^n <= e^{-beta_H^2/8} (1/2) V^{(n+1)/2} Gamma
        V = q(1152 * Fr(tb) ** 2)
        if mode == 'R2':
            # R2e <= U(t) and R2e <= 10 t^3: use the smaller tail integral
            tt = Z
            for n, a in U_TERMS:
                tt = CU.add(tt, mul(a, half_moment(V, n))[1])
            tt = min(tt, mul(q(10), half_moment(V, Fr(3)))[1])
        else:
            tt = half_moment(V, Fr(2))[1]
        tails = CU.add(tails, CU.multiply(CU.multiply(pa, E_BH[1]), tt))
    if mode == 'R2':
        return up, tails
    return lo, CU.add(up, tails)


def T1_tau_tails(tau0, tauN, mode):
    """Upper bounds of the T1 contributions from tau < tau0 and tau > tauN."""
    Minf = mul(mul(MFAC, q(Fr(1, 4))), mul(ipow(q(12), Fr(-11, 12)), q(Fr(12, 11))))   # M(tau) <= Minf tau^{-11/6}
    low_terms = [(Fr(3), q(10))] if mode == 'R2' else [(Fr(2), q(1))]                  # R2e(t) <= 10 t^3
    high_terms = U_TERMS if mode == 'R2' else [(Fr(2), q(1))]
    low = Z
    for n, a in low_terms:
        # int_0^tau0 C1 tau^{-11/3} M(0) a (1/2)(24 tau)^{n+1} Gamma((n+1)/2) dtau
        c = mul(mul(C1, M0), mul(a, half_moment(q(576), n)))
        low = CU.add(low, mul(c, div(tpow(tau0, n - Fr(5, 3)), q(n - Fr(5, 3))))[1])
    high = Z
    for n, a in high_terms:
        c = mul(mul(C1, Minf), mul(a, half_moment(q(576), n)))
        high = CU.add(high, mul(c, div(tpow(tauN, n - Fr(7, 2)), q(Fr(7, 2) - n)))[1])
    return low, high


# ---------------------------------------------------------------- T3:  C3 tau^{-11/3} m(g) e^{-12 tau^2 g^4} e^{-t^2/(576 tau^2)} kappa(1-t) s theta(|8-12t|/s)
def kappa_iv(v):
    x = mul(q(3), sub(q(1), pt(v)))
    if x[1] <= 0:
        return (Z, Z)
    return div(mul(x, isqrt(x)), q(6))


TAU_L3, TAU_M, TAU_H = '0.002', '2', '1000'
T3G = t3_grid(CN.multiply(Dec(12 * 9), CN.multiply(Dec(TAU_H), Dec('1.05'))))
need(increasing(T3G) and T3G[-1] == 1, 'partition')
KAP = [kappa_iv(v) for v in T3G]
TABS = []
RMIN = []
for k in range(len(T3G) - 1):
    fa, fb = Fr(T3G[k]), Fr(T3G[k + 1])
    ta_ = Fr(0) if fa <= 0 <= fb else min(abs(fa), abs(fb))
    ra_ = Fr(0) if 3 * fa <= 2 <= 3 * fb else min(abs(8 - 12 * fa), abs(8 - 12 * fb))
    TABS.append(q(ta_)[0])                     # lower bounds (exact here): larger Gaussian factor, larger theta+
    RMIN.append(q(ra_)[0])
CC = mul(mul(C3, PHI0), C6)                    # constant of the unsuppressed bound


def t3_start(tb):
    T = CN.multiply(Dec(12), CN.multiply(tb, BETA_H))
    k0 = len(T3G) - 1
    while k0 > 0 and T3G[k0] > -T:
        k0 -= 1
    need(T3G[k0] <= -T, 'partition')
    return k0


def K_tail(tb, k0):
    """Upper bound of int_{-inf}^{T3G[k0]} e^{-t^2/(576 tau^2)} kappa(1-t) dt for tau <= tb (T3G[k0] <= -12 tb beta_H)."""
    V = q(1152 * Fr(tb) ** 2)
    br = add(half_moment(V, Fr(3, 2)), mul(q(Fr(3, 2)), add(mul(q(Fr(1, 2)), mul(ipow(V, Fr(1, 2)), SQRT_PI)),
                                                            half_moment(V, Fr(1, 2)))))
    return mul(mul(E_BH, div(ipow(q(3), Fr(3, 2)), q(6))), br)[1]


def t3_tw(k, tb):
    """Upper bound of dt * sup e^{-t^2/(576 tau^2)} kappa(1 - t) over the t-cell k and tau <= tb."""
    den = CN.multiply(Dec(576), CN.multiply(tb, tb))
    kap = KAP[k + 1][1] if MUT == 'M14' else KAP[k][1]
    return CU.multiply(CU.multiply(gauss_up(TABS[k], den), kap), CN.subtract(T3G[k + 1], T3G[k]))


def K_up(tb, log=False):
    """Upper bound of K(tau) = int_{-inf}^1 e^{-t^2/(576 tau^2)} kappa(1-t) dt for tau <= tb (K is increasing in tau)."""
    k0 = t3_start(tb)
    nk = len(T3G) - 1 - k0
    sample = {k0, k0 + nk // 3, k0 + (2 * nk) // 3, len(T3G) - 2} if log else ()
    s = Z
    for k in range(k0, len(T3G) - 1):
        tw = t3_tw(k, tb)
        s = CU.add(s, tw)
        if k in sample:
            LOG['K'].append((tb, k, tw))
    return CU.add(s, K_tail(tb, k0))


def t3_cell(ta, tb, n3=48, gscale=3):
    """The tau-cell [ta, tb] of the 3-d part: A >= dtau sup C3 tau^{-11/3}; per g-cell j (width dg):
    w[j] >= dg sup m(g) e^{-12 tau^2 g^4}, s[j] >= sup s = 576 sqrt6 tau^2 g, inv[j] <= 200/s[j]."""
    dtau = CN.subtract(tb, ta)
    A = CU.multiply(CU.multiply(C3[1], tpow(ta, Fr(-11, 3))[1]), dtau)
    dg = g_step(ta, gscale, n3)
    cells = g_cells(dg, n3, Fr(8, 3))
    t12a = CN.multiply(Dec(12), CN.multiply(ta, ta))
    tsq = CN.multiply(ta, ta) if MUT == 'M13' else CN.multiply(tb, tb)
    c6t2 = CU.multiply(C6[1], tsq)
    w, sv, inv = [], [], []
    for j in range(n3):
        ga = CN.multiply(dg, Dec(j))
        w.append(CU.multiply(CU.multiply(dg, cells[j][0]),
                             upx(CD.multiply(t12a, CD.multiply(CD.multiply(ga, ga), CD.multiply(ga, ga))))))
        sv.append(CU.multiply(c6t2, CN.add(ga, dg)))
        inv.append(CD.divide(Dec(TH_STEP), sv[-1]))
    return A, dg, w, sv, inv


TH_LIM = Dec(TH_STEP * 40)


def th_up(r, invj):
    """Table bound of theta+(r'/s) for r' >= r and s <= s_j, with invj <= 200/s_j (Lemma 3)."""
    return THTAB[th_idx_scaled(CD.multiply(r, invj))]


def lam_terms(r, gw, inv, GS):
    """sum_j gw[j] th_j, with th_j >= theta+(r/s_j) from the table, and the list of the th_j used."""
    n = len(gw)
    if r == 0:
        return CU.multiply(THTAB[0], GS), [THTAB[0]] * n
    if CD.multiply(r, inv[-1]) >= TH_LIM:              # every a >= 40: the last table entry
        return CU.multiply(THTAB[TH_N], GS), [THTAB[TH_N]] * n
    ths = [th_up(r, inv[j]) for j in range(n)]
    lam = Z
    for j in range(n):
        lam = CU.add(lam, CU.multiply(gw[j], ths[j]))
    return lam, ths


def T3_3d(tau_pts, n3=48, gscale=3, log_cells=()):
    need(increasing(tau_pts), 'partition')
    total, tails = Z, Z
    for i in range(len(tau_pts) - 1):
        ta, tb = tau_pts[i], tau_pts[i + 1]
        dtau = CN.subtract(tb, ta)
        ta113 = tpow(ta, Fr(-11, 3))[1]
        A, dg, w, sv, inv = t3_cell(ta, tb, n3, gscale)
        gw = [CU.multiply(w[j], sv[j]) for j in range(n3)]
        GS = Z
        for x in gw:
            GS = CU.add(GS, x)
        k0 = t3_start(tb)
        ksample = ()
        if i in log_cells:
            ksample = {k0, (k0 + len(T3G) - 2) // 2, len(T3G) - 2}
            ksample |= {k for k in range(k0, len(T3G) - 1) if T3G[k] <= Dec('0.6667') <= T3G[k + 1]}
            ksample |= {k for k in range(k0, len(T3G) - 1) if T3G[k] <= Dec('-0.3') <= T3G[k + 1]}
        invx = inv[::-1] if MUT == 'M17' else inv
        acc = Z
        for k in range(k0, len(T3G) - 1):
            tw = t3_tw(k, tb)
            lam, ths = lam_terms(RMIN[k], gw, invx, GS)
            acc = CU.add(acc, CU.multiply(tw, lam))
            if k in ksample:
                LOG['T3'].append((ta, tb, dtau, A, dg, gw, k, tw, ths))
        total = CU.add(total, CU.multiply(A, acc))
        # tails of this tau-cell: g > G (unsuppressed) and t below the grid (unsuppressed)
        base = CU.multiply(CU.multiply(CC[1], ta113), CU.multiply(dtau, CN.multiply(tb, tb)))
        gt = CU.multiply(g_tail(ta, CN.multiply(dg, Dec(n3)), Fr(11, 3)), Kcrude(tb)[1])
        nt = CU.multiply(g_integral(ta, Fr(11, 3), 200, want_lower=False)[1], K_tail(tb, k0))
        tails = CU.add(tails, CU.multiply(base, CU.add(gt, nt)))
    return total, tails


def sep_fac(ta, tb):
    """Upper bound of dtau sup_{[ta, tb]} C3 phi(0) 576 sqrt6 tau^{-5/3} N(tau) (N decreasing)."""
    nn = g_integral(ta, Fr(11, 3), 200, want_lower=False)[1]
    return CU.multiply(CU.multiply(CC[1], tpow(ta, Fr(-5, 3))[1]), CU.multiply(CN.subtract(tb, ta), nn))


def T3_sep(tau_pts, log_cells=()):
    """tau in [tau_M, tau_H]: theta <= phi(0); bound CC dtau ta^{-5/3} N+(ta) K+(tb)."""
    need(increasing(tau_pts), 'partition')
    total = Z
    for i in range(len(tau_pts) - 1):
        ta, tb = tau_pts[i], tau_pts[i + 1]
        sf = sep_fac(ta, tb)
        total = CU.add(total, CU.multiply(sf, K_up(tb, log=(i in log_cells))))
        if i in log_cells:
            LOG['SEP'].append((ta, tb, sf))
    return total


def check_logs():
    """Group corners: every factor that a production loop used on a sampled cell dominates (or, for the infimum
    weight of a negative T1 cell, is dominated by) an independent enclosure of the matching factor of the integrand,
    at the corners, edge midpoints and centre of that cell.  The comparisons are one-sided and cannot fail for
    correct code."""
    def at(a, b, u):
        return CN.add(a, CN.multiply(CN.subtract(b, a), u))
    U3 = [Dec(0), Dec('0.5'), Dec(1)]
    need(len(LOG['T1']) >= 20 and len(LOG['T3']) >= 20 and len(LOG['SEP']) >= 3 and len(LOG['K']) >= 9, 'corners')
    mc = {}
    for (ta, tb, u0, u1, wu, ew, rj) in LOG['T1']:
        dtau = CN.subtract(tb, ta)
        for u in U3:
            x = at(ta, tb, u)
            if x not in mc:
                mc[x] = M_enc(x)
            v = mul(mul(C1, tpow(x, Fr(-11, 3))), mul(mc[x], pt(dtau)))
            need(v[0] <= wu if rj >= 0 else v[1] >= wu, 'corners')
            for ut in U3:
                t = at(u0, u1, ut)
                e = iexp(neg(div(mul(pt(t), pt(t)), mul(q(576), mul(pt(x), pt(x))))))
                need(e[0] <= ew if rj >= 0 else e[1] >= ew, 'corners')
        for ut in U3:
            t = at(u0, u1, ut)
            need(mul(q(Fr(1, 2)), add(R2iv(t), R2iv(-t)))[0] <= rj, 'corners')
    for (ta, tb, dtau, A, dg, gw, k, tw, ths) in LOG['T3']:
        va, vb = T3G[k], T3G[k + 1]
        for u in U3:
            x = at(ta, tb, u)
            need(mul(C3, mul(tpow(x, Fr(-11, 3)), pt(dtau)))[0] <= A, 'corners')
            for ut in U3:
                t = at(va, vb, ut)
                e = iexp(neg(div(mul(pt(t), pt(t)), mul(q(576), mul(pt(x), pt(x))))))
                need(mul(mul(e, kappa_iv(t)), pt(CN.subtract(vb, va)))[0] <= tw, 'corners')
        for j in (0, 7, 23, len(gw) - 1):
            ga = CN.multiply(dg, Dec(j))
            gb = CN.add(ga, dg)
            used = CU.multiply(gw[j], ths[j])
            for ug in U3:
                g = at(ga, gb, ug)
                if g == 0:
                    continue
                for u in U3:
                    x = at(ta, tb, u)
                    wv = mul(pt(dg), mul(m_iv(g, Fr(8, 3)), iexp(neg(mul(mul(q(12), mul(pt(x), pt(x))),
                                                                     mul(mul(pt(g), pt(g)), mul(pt(g), pt(g))))))))
                    sx = mul(C6, mul(mul(pt(x), pt(x)), pt(g)))
                    for ut in U3:
                        t = at(va, vb, ut)
                        r = abs(CN.subtract(Dec(8), CN.multiply(Dec(12), t)))
                        th = thetap_iv(CU.divide(r, sx[0]))[0]
                        need(CD.multiply(CD.multiply(wv[0], sx[0]), th) <= used, 'corners')
    for (ta, tb, sf) in LOG['SEP']:
        for u in U3:
            x = at(ta, tb, u)
            nx = g_integral(x, Fr(11, 3), 200)[0]
            need(mul(mul(CC, tpow(x, Fr(-5, 3))), mul(pt(nx), pt(CN.subtract(tb, ta))))[0] <= sf, 'corners')
    for (tb, k, tw) in LOG['K']:
        va, vb = T3G[k], T3G[k + 1]
        for x in (tb, CN.multiply(tb, Dec('0.5'))):
            for ut in U3:
                t = at(va, vb, ut)
                e = iexp(neg(div(mul(pt(t), pt(t)), mul(q(576), mul(pt(x), pt(x))))))
                need(mul(mul(e, kappa_iv(t)), pt(CN.subtract(vb, va)))[0] <= tw, 'corners')


def Kcrude(tau):
    """Upper bound of K(tau) for every tau' <= tau: (3^{3/2}/6)[1 + (1/2)(24 tau)^{5/2} G(5/4) + (3/4)(24 tau sqrt(pi) + (24 tau)^{3/2} G(3/4))]."""
    x = mul(q(24), pt(tau))
    br = add(add(q(1), mul(q(Fr(1, 2)), ipow(x, Fr(5, 2)))),
             mul(q(Fr(3, 4)), add(mul(x, SQRT_PI), mul(ipow(x, Fr(3, 2)), q(Fr(4, 3))))))
    return mul(div(ipow(q(3), Fr(3, 2)), q(6)), br)


def T3_low(tauL):
    """tau < tauL: (a) t in (1/3, 1] and (b) t <= 1/3, as in note DC, section 6 (the tails)."""
    tL = pt(Dec(tauL))
    pre = mul(CC, mul(N0, ipow(tL, Fr(-2, 3))))
    a_part = mul(mul(pre, mul(q(Fr(2, 3)), div(ipow(q(2), Fr(3, 2)), q(6)))),
                 iexp(neg(div(q(1), mul(q(5184), mul(tL, tL))))))
    nb = mul(mul(q(Fr(1, 2)), ipow(q(8), Fr(7, 3))), q(Fr(4, 3)))                     # int g^{11/3} e^{-g^2/8}
    b_part = mul(mul(mul(CC, nb), mul(Kcrude(Dec(tauL)), ipow(tL, Fr(-2, 3)))),
                 iexp(neg(div(q(2), mul(C6, mul(tL, tL))))))
    need(Fr(tauL) ** 2 < Fr(6, 5 * 5184), 'tails')            # monotone factor on (0, tauL]
    need(Fr(tauL) ** 2 * 5 * Fr(C6[1]) < 12, 'tails')
    return add(a_part, b_part)[1]


def T3_high(tauH):
    """tau > tauH: N(tau) <= (1/4)(12 tau^2)^{-7/6}, K(tau) <= Kcrude(tau)."""
    tH = pt(Dec(tauH))
    c = mul(CC, mul(q(Fr(1, 4)), ipow(q(12), Fr(-7, 6))))
    x24 = q(24)
    s = Z
    # terms of tau^{-4} Kcrude(tau): exponents -4, -3/2, -3, -5/2
    k6 = div(ipow(q(3), Fr(3, 2)), q(6))
    for coef, ex in ((q(1), Fr(-4)), (mul(q(Fr(1, 2)), ipow(x24, Fr(5, 2))), Fr(-3, 2)),
                     (mul(q(Fr(3, 4)), mul(x24, SQRT_PI)), Fr(-3)),
                     (mul(q(Fr(3, 4)), mul(ipow(x24, Fr(3, 2)), q(Fr(4, 3)))), Fr(-5, 2))):
        s = CU.add(s, mul(mul(c, mul(k6, coef)), div(ipow(tH, ex + 1), q(-(ex + 1))))[1])
    return s


# ---------------------------------------------------------------- normalization checks against closed forms
G16 = GAM[Fr(1, 6)]
# (1/2400) int k^{-8/3} e^{-12 k^2} E[g^6 t^2] dk = (576/2400)(1/2) 12^{-1/6} Gamma(1/6)
TGT1 = mul(mul(q(Fr(576, 4800)), ipow(q(12), Fr(-1, 6))), G16)
# (1/2400) int k^{-8/3} e^{-12 k^2} E[g^6 s] dk, s = 576 sqrt6 k^2/|g|^3, E|g|^3 = 8/sqrt(pi)
TGT3 = mul(mul(mul(q(Fr(576, 2400)), SQ6), div(q(8), SQRT_PI)), mul(q(Fr(1, 2)), mul(ipow(q(12), Fr(-1, 6)), G16)))
C36 = mul(C3, C6)
GAUSS_R = mul(q(24), SQRT_PI)                  # int_R e^{-t^2/(576 tau^2)} dt = 24 tau sqrt(pi)


def check_tau_tails(tau0, tauN):
    low = mul(mul(C36, mul(GAUSS_R, N0)), mul(q(3), tpow(tau0, Fr(1, 3))))
    high = mul(mul(C36, mul(GAUSS_R, mul(q(Fr(1, 4)), ipow(q(12), Fr(-7, 6))))), div(tpow(tauN, Fr(-2)), q(2)))
    return CU.add(low[1], high[1])


def T3_check_3d(tau_pts):
    """kappa = 1, K_sigma = s, t over R integrated exactly: (lower, upper) by the 3-d code's g- and tau-cells."""
    lo, up = Z, Z
    n3 = 40
    for i in range(len(tau_pts) - 1):
        ta, tb = tau_pts[i], tau_pts[i + 1]
        dtau = CN.subtract(tb, ta)
        A_up = CU.multiply(CU.multiply(C3[1], tpow(ta, Fr(-11, 3))[1]), dtau)
        A_lo = CD.multiply(CD.multiply(C3[0], tpow(tb, Fr(-11, 3))[0]), dtau)
        dg = g_step(ta, 5, n3)
        cells = g_cells(dg, n3, Fr(8, 3))
        GS_up, GS_lo = Z, Z
        t12a = CN.multiply(Dec(12), CN.multiply(ta, ta))
        t12b = CN.multiply(Dec(12), CN.multiply(tb, tb))
        for j in range(n3):
            ga = CN.multiply(dg, Dec(j))
            gb = CN.add(ga, dg)
            wu = CU.multiply(CU.multiply(dg, cells[j][0]),
                             upx(CD.multiply(t12a, CD.multiply(CD.multiply(ga, ga), CD.multiply(ga, ga)))))
            wl = CD.multiply(CD.multiply(dg, cells[j][1]),
                             lox(CU.multiply(t12b, CU.multiply(CU.multiply(gb, gb), CU.multiply(gb, gb)))))
            GS_up = CU.add(GS_up, CU.multiply(wu, CU.multiply(C6[1], CN.multiply(CN.multiply(tb, tb), gb))))
            GS_lo = CD.add(GS_lo, CD.multiply(wl, CD.multiply(C6[0], CN.multiply(CN.multiply(ta, ta), ga))))
        up = CU.add(up, CU.multiply(A_up, CU.multiply(GS_up, CU.multiply(GAUSS_R[1], tb))))
        lo = CD.add(lo, CD.multiply(A_lo, CD.multiply(GS_lo, CD.multiply(GAUSS_R[0], ta))))
        base = CU.multiply(CU.multiply(C36[1], tpow(ta, Fr(-11, 3))[1]), CU.multiply(dtau, CN.multiply(tb, tb)))
        gt = CU.multiply(g_tail(ta, CN.multiply(dg, Dec(n3)), Fr(11, 3)), CU.multiply(GAUSS_R[1], tb))
        up = CU.add(up, CU.multiply(base, gt))
    return lo, up


def t_machinery(tau):
    """The 3-d code's t-cells on the symmetric grid built like T3G: bracket int_R e^{-t^2/(576 tau^2)} dt = 24 tau sqrt(pi)."""
    tgs = t3_grid(CN.multiply(Dec(108), tau), sym=True)
    den = CN.multiply(Dec(576), CN.multiply(tau, tau))
    lo, up = Z, Z
    for k in range(len(tgs) - 1):
        va, vb = tgs[k], tgs[k + 1]
        tabs = Z if va <= 0 <= vb else min(abs(va), abs(vb))
        tmx = max(abs(va), abs(vb))
        dt = CN.subtract(vb, va)
        up = CU.add(up, CU.multiply(upx(CD.divide(CD.multiply(tabs, tabs), den)), dt))
        lo = CD.add(lo, CD.multiply(lox(CU.divide(CU.multiply(tmx, tmx), den)), dt))
    # Gaussian tails beyond |t| >= 12 tau beta_H:  2 e^{-beta_H^2/8} (1/2) sqrt(1152 tau^2) sqrt(pi)
    up = CU.add(up, mul(mul(q(2), E_BH), mul(q(Fr(1, 2)), mul(ipow(q(1152 * Fr(tau) ** 2), Fr(1, 2)), SQRT_PI)))[1])
    exact = mul(GAUSS_R, pt(tau))
    need(lo <= exact[1] and exact[0] <= up and up <= CU.multiply(lo, Dec('1.2')), 't_machinery')
    return lo, up


def T3_check_sep(tau_pts):
    lo, up = Z, Z
    for i in range(len(tau_pts) - 1):
        ta, tb = tau_pts[i], tau_pts[i + 1]
        dtau = CN.subtract(tb, ta)
        nlo = g_integral(tb, Fr(11, 3), 100)[0]
        nup = g_integral(ta, Fr(11, 3), 100, want_lower=False)[1]
        up = CU.add(up, CU.multiply(CU.multiply(C36[1], tpow(ta, Fr(-5, 3))[1]), CU.multiply(dtau, CU.multiply(nup, CU.multiply(GAUSS_R[1], tb)))))
        lo = CD.add(lo, CD.multiply(CD.multiply(C36[0], tpow(tb, Fr(-5, 3))[0]), CD.multiply(dtau, CD.multiply(nlo, CD.multiply(GAUSS_R[0], ta)))))
    return lo, up


def run():
    # T1 moment check (validates C1, M, the t-cells and the tails)
    tc = geo_grid('1e-4', '1e4', '1.05')
    lo, up = T1_bound(tc, t1_grid(CN.multiply(Dec(108), tc[-1]), '0.05'), 'mom')
    l_, h_ = T1_tau_tails(tc[0], tc[-1], 'mom')
    up = CU.add(up, CU.add(l_, h_))
    need(lo <= TGT1[1] and TGT1[0] <= up and up <= CU.multiply(lo, Dec(3)), 'T1_moment')
    mom1 = (lo, up)
    # T3 moment checks (validate C3 C6, the g-cells, both tau-paths and the tails)
    tc3 = geo_grid('1e-4', '1e4', '1.05')
    lo3, up3 = T3_check_3d(tc3)
    up3 = CU.add(up3, check_tau_tails(tc3[0], tc3[-1]))
    need(lo3 <= TGT3[1] and TGT3[0] <= up3 and up3 <= CU.multiply(lo3, Dec(3)), 'T3_moment')
    los, ups = T3_check_sep(tc3)
    ups = CU.add(ups, check_tau_tails(tc3[0], tc3[-1]))
    need(los <= TGT3[1] and TGT3[0] <= ups and ups <= CU.multiply(los, Dec(3)), 'T3_moment')
    tmach = [t_machinery(Dec(x)) for x in ('0.002', '0.05', '1', '30', '1000')]

    # grids
    tau1 = geo_grid('1e-4', TAU_H, '1.02')
    tg1 = t1_grid(CN.multiply(Dec(108), tau1[-1]))
    tau3 = geo_grid(TAU_L3, TAU_M, '1.02')
    taus = geo_grid(tau3[-1], TAU_H, '1.02')
    # T1 (the loops log the factors they use on sampled cells; check_logs verifies them below)
    t1c, t1t = T1_bound(tau1, tg1, 'R2', log_cells={40, 200, 400, 600, len(tau1) - 2})
    t1l, t1h = T1_tau_tails(tau1[0], tau1[-1], 'R2')
    T1_UP = CU.add(CU.add(t1c, t1t), CU.add(t1l, t1h))
    # T3
    t3c, t3t = T3_3d(tau3, log_cells={10, 100, 200, 300, len(tau3) - 2})
    need(taus[0] == tau3[-1], 'partition')
    t3s = T3_sep(taus, log_cells={0, 100, len(taus) - 2})
    check_logs()
    t3l = T3_low(TAU_L3)
    t3h = T3_high(taus[-1])
    T3_UP = CU.add(CU.add(CU.add(t3c, t3t), t3s), CU.add(t3l, t3h))
    D_UP = CU.add(CU.add(T1_UP, T2[1]), T3_UP)
    need(D_UP <= Dec('0.61'), 'assembly')
    need(T1_UP <= Dec('0.0951690') and T3_UP <= Dec('0.248277') and D_UP <= Dec('0.438822'), 'assembly')
    # corollaries: I~ = I~_quad + D (note V24, (5.3)), -I~_quad = (112/675) Gamma(1/6) 12^{-1/6}; J >= 1/2000 (V24 Lemma J)
    IQ = mul(mul(q(Fr(112, 675)), G16), ipow(q(12), Fr(-1, 6)))
    need(IQ[0] >= Dec('0.6104056') and IQ[1] <= Dec('0.6104057'), 'corollary')
    ITILDE_UP = CU.add(-IQ[0], D_UP)
    COEF_LO = CD.subtract(CD.add(q(Fr(1, 60000))[0], IQ[0]), D_UP)          # J/30 - I~ >= this
    need(ITILDE_UP <= Dec('-0.17158') and COEF_LO >= Dec('0.17160'), 'corollary')
    # note V24, Theorem V at L >= 10: eta_c + eta_R (d = 3: 1.97e-7 + 4.97e-4; d = 2: 5.88e-9 + 7.81e-6)
    ETA = {3: (Dec('1.97e-7'), Dec('4.97e-4')), 2: (Dec('5.88e-9'), Dec('7.81e-6'))}
    TORUS = {}
    for d_, (ec, er) in ETA.items():
        lo_coef = CD.subtract(COEF_LO, CU.add(ec, er))
        up_r = CU.add(ITILDE_UP, er)
        need(lo_coef >= Dec('0.1711') and up_r <= Dec('-0.1710'), 'corollary')
        TORUS['d%d_coef_lo' % d_] = lo_coef
        TORUS['d%d_R_up' % d_] = up_r
    return {'T1_up': T1_UP, 'T1_cells': t1c, 'T1_tails': CU.add(CU.add(t1t, t1l), t1h),
            'Itilde_quad_neg': IQ, 'Itilde_up': ITILDE_UP, 'model_coef_lo': str(R6D.plus(COEF_LO)),
            'torus_L10': {k: str(R6D.plus(v)) if 'coef' in k else str(R6.plus(v)) for k, v in TORUS.items()},
            'T2': T2, 'T3_up': T3_UP, 'T3_cells_3d': t3c, 'T3_sep': t3s,
            'T3_tails': CU.add(CU.add(t3t, t3l), t3h), 'D_up': D_UP,
            'moment_T1': mom1, 'moment_T1_target': TGT1, 'moment_T3_3d': (lo3, up3), 'moment_T3_sep': (los, ups),
            'moment_T3_target': TGT3,
            'cells': {'tau_T1': len(tau1) - 1, 't_T1': len(t1_grid(CN.multiply(Dec(108), tau1[-1]))) - 1,
                      'tau_T3_3d': len(tau3) - 1, 'tau_T3_sep': len(taus) - 1, 't_T3': len(T3G) - 1}}


R6 = decimal.Context(prec=6, rounding=decimal.ROUND_CEILING)
R6D = decimal.Context(prec=6, rounding=decimal.ROUND_FLOOR)


def fmt(x):
    if isinstance(x, str):
        return x
    if isinstance(x, tuple):
        return [str(R6D.plus(x[0])), str(R6.plus(x[1]))]
    if isinstance(x, dict):
        return x
    return str(R6.plus(x))


try:
    res = run()
except Fail as e:
    sys.stderr.write('FAILED: %s\n' % e.args[0])
    sys.exit(1)
out = {'note': 'DC', 'result': 'D <= D_up <= 0.438822', 'values': {k: fmt(v) for k, v in res.items()},
       'checks': COUNT, 'precision': PREC}
print(json.dumps(out, sort_keys=True, ensure_ascii=True))
