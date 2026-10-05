#!/usr/bin/env python3
"""Exact controls for Theorem 1D_R (CL-D1-LINE-20261004-v1): Theorems 1D and 1D+ on the line.

Standard library only.  Exact rationals (fractions.Fraction) for C1, C2, C4, C5 and C6.  C3 evaluates the closed-form
constants of [1D] section 0 in floating point and compares them with the printed 8-decimal values.  Output: one JSON
document on stdout, equal to RESULTS.json.

    python3 -B -S line_check.py                 # exit 0
    python3 -B -S line_check.py --mutant M3     # exit 1 (each mutant breaks its own control)
    python3 -B -S line_check.py --mutant XX     # exit 2 (unknown label)

Notation as in PROOF.md section 4: w is an interval (cell) length or a sample spacing, sigma_F the Lipschitz constant
of Lemma 4.4_R.

Scientific effect: NONE.  The controls check the elementary inequalities, constants and summations that the proof uses
(PROOF.md section 8).  They do not check the probabilistic steps.
"""
import json
import math
import sys
from fractions import Fraction as Fr

OBJECT = 'CL-D1-LINE-20261004-v1.1'

MUTANTS = {
    'M1': 'C1: the Landau bound without the term 2 osc/|Delta|',
    'M2': 'C4: the cell Sobolev constant 1 in place of 2',
    'M3': 'C2: the Gaussian sample spacing w = 1 in place of 2',
    'M4': 'C3: C0 without its factor 2',
    'M5': 'C5: the band exponent 23 A^2/(32 sigma_F^2) in place of 23 A^2/(16 sigma_F^2)',
    'M6': 'C6: the threshold R0 = 4 (M2^(1/2) + 1) in place of 5 (M2^(1/2) + 1)',
    'M7': 'C6: only r - 1 small eigenvalues allowed after a rank-r conditioning',
}


class ControlFailure(Exception):
    pass


def check(cond, msg):
    if not cond:
        raise ControlFailure(msg)


def parse_args(argv):
    mutant = None
    rest = list(argv)
    while rest:
        a = rest.pop(0)
        if a == '--mutant':
            if not rest:
                print('usage: line_check.py [--mutant M1..M7]', file=sys.stderr)
                sys.exit(2)
            mutant = rest.pop(0)
            if mutant not in MUTANTS:
                print('unknown mutant label: ' + mutant, file=sys.stderr)
                sys.exit(2)
        else:
            print('unknown argument: ' + a, file=sys.stderr)
            sys.exit(2)
    return mutant


# ---------------------------------------------------------------- polynomials (coefficients low -> high, Fractions)

def trim(p):
    p = [Fr(a) for a in p]
    while p and p[-1] == 0:
        p.pop()
    return p


def padd(p, q):
    n = max(len(p), len(q))
    return trim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)])


def pmul(p, q):
    if not p or not q:
        return []
    out = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return trim(out)


def pder(p):
    return trim([i * p[i] for i in range(1, len(p))])


def peval(p, x):
    acc = Fr(0)
    for a in reversed(p):
        acc = acc * x + a
    return acc


def pint(p, a, b):
    """exact integral of p over [a, b]"""
    anti = [Fr(0)] + [c / (i + 1) for i, c in enumerate(p)]
    return peval(anti, b) - peval(anti, a)


def show(p):
    return '[' + ', '.join(map(str, p)) + ']'


class Lcg:
    def __init__(self, seed):
        self.x = seed

    def nxt(self):
        self.x = (6364136223846793005 * self.x + 1442695040888963407) % (1 << 64)
        return self.x >> 33

    def frac(self, den):
        """a rational in [-1, 1] with denominator den"""
        return Fr(self.nxt() % (2 * den + 1) - den, den)


def ceil_dec(x, digits):
    """decimal string of the rational x rounded up (towards +infinity) at the given number of digits"""
    scale = 10 ** digits
    n = -((-x.numerator * scale) // x.denominator)
    sign = '-' if n < 0 else ''
    n = abs(n)
    return '%s%d.%0*d' % (sign, n // scale, digits, n % scale)


def floor_dec(x, digits):
    """decimal string of the rational x >= 0 rounded down at the given number of digits"""
    scale = 10 ** digits
    n = (x.numerator * scale) // x.denominator
    return '%d.%0*d' % (n // scale, digits, n % scale)


# ---------------------------------------------------------------- C1: Landau's inequality on an interval (Lemma 4.2_R)

def landau_case(c, w, grid=64, steps=40):
    """g(s) = sum c[k] s^k on Delta = [-w/2, w/2], midpoint 0, |Delta| = w.
    Returns |g'(0)|, a lower and an upper bound for osc_Delta g, S = sup_Delta |g''| (exact), and the Taylor-step
    verdict.  Upper bound: every point is within w/(2 grid) of a grid point, and |g'| <= sum k |c_k| (w/2)^(k-1)."""
    g = trim(c)
    g1 = pder(g)
    g2 = pder(g1)
    half = w / 2
    cands = [-half, half]
    if len(g2) == 3:
        v = -g2[1] / (2 * g2[2])
        if -half < v < half:
            cands.append(v)
    S = max(abs(peval(g2, x)) for x in cands)
    pts = [-half + w * Fr(k, grid) for k in range(grid + 1)]
    vals = [peval(g, x) for x in pts]
    for k in range(grid):
        lo, hi = pts[k], pts[k + 1]
        flo, fhi = peval(g1, lo), peval(g1, hi)
        if flo != 0 and fhi != 0 and (flo > 0) != (fhi > 0):
            for _ in range(steps):
                mid = (lo + hi) / 2
                fm = peval(g1, mid)
                if (fm > 0) == (flo > 0):
                    lo, flo = mid, fm
                else:
                    hi = mid
            vals.append(peval(g, lo))
            vals.append(peval(g, hi))
    osc = max(vals) - min(vals)
    slope = sum(k * abs(ck) * half ** (k - 1) for k, ck in enumerate(g) if k >= 1)
    osc_up = osc + (w / grid) * slope
    a = abs(peval(g1, Fr(0)))
    taylor = True
    for u in (half, half / 2, half / 4, half / 8):
        taylor = taylor and abs(2 * u * peval(g1, Fr(0))) <= abs(peval(g, u) - peval(g, -u)) + u * u * S
    return a, osc, osc_up, S, taylor


def landau_holds(a, osc, S, w, mutant):
    """|g'(y)| <= (osc S)^(1/2) + 2 osc/|Delta|, decided exactly:
    with b = 2 osc/|Delta|, either a <= b or (a - b)^2 <= osc S"""
    b = Fr(0) if mutant == 'M1' else 2 * osc / w
    return a <= b or (a - b) ** 2 <= osc * S


def control_c1(mutant):
    rng = Lcg(20261004)
    lengths = [Fr(1, 2), Fr(1), Fr(2), Fr(3), Fr(4), Fr(25, 2)]
    n = 0
    sqrt_needed = 0
    for w in lengths:
        cases = []
        for _ in range(40):
            # degree <= 4, scaled to the interval: g(s) = sum c_k (2 s/w)^k
            cases.append([rng.frac(9) * (2 / w) ** k for k in range(5)])
        for _ in range(10):
            # S-shaped cubics g = A s (1 - (2s/w)^2) + small terms: |g'(y)| exceeds 2 osc/|Delta|
            A = 1 + abs(rng.frac(9))
            cases.append([rng.frac(9) / 50, A, rng.frac(9) / (50 * w), -4 * A / w ** 2])
        for c in cases:
            a, osc, osc_up, S, taylor = landau_case(c, w)
            check(taylor, 'C1 Taylor step fails (|Delta|=%s, g=%s)' % (w, show(c)))
            check(landau_holds(a, osc, S, w, mutant), 'C1 Landau bound fails (|Delta|=%s, g=%s)' % (w, show(c)))
            if a > 2 * osc_up / w:
                sqrt_needed += 1
            n += 1
    check(sqrt_needed >= len(lengths) * 10, 'C1 the S-shaped cubics should need the term (osc S)^(1/2)')
    # the nearly affine family g = s + eps s^2 on a unit interval: |g'(0)| = 1, osc = 1, S = 2 eps
    affine = {}
    for eps in (Fr(1, 10), Fr(1, 100), Fr(1, 1000), Fr(1, 10 ** 6)):
        a, osc, osc_up, S, taylor = landau_case([Fr(0), Fr(1), eps], Fr(1))
        check(a == 1 and osc == 1 and S == 2 * eps and taylor, 'C1 nearly affine family: exact values')
        check(landau_holds(a, osc, S, Fr(1), mutant),
              'C1 Landau bound fails on the nearly affine family (eps=%s)' % eps)
        check(osc * S < a * a, "C1 nearly affine family: (osc S)^(1/2) < |g'(0)|")
        affine[str(eps)] = {"|g'(0)|": '1', 'osc': '1', 'S': str(S), 'osc*S': str(osc * S)}
    return {'interval_lengths': [str(w) for w in lengths], 'polynomials_tested': n,
            "cases_with_|g'(y)|>2osc/|Delta|_(osc_bounded_above)": sqrt_needed,
            'nearly_affine_g=s+eps*s^2_unit_interval': affine,
            'reading': "both terms are needed: the S-shaped cubics have |g'(y)| > 2 osc/|Delta|, and on the nearly "
                       "affine family |g'(y)|^2 = 1 > osc*S = 2 eps"}


# ---------------------------------------------------------------- C2: Gaussian f'-samples, diagonal dominance

def exp_neg_upper(x, n=40):
    """e^(-x) <= 1/sum_{j<=n} x^j/j! for rational x >= 0"""
    s, term = Fr(0), Fr(1)
    for j in range(n + 1):
        s += term
        term = term * x / (j + 1)
    return 1 / s


def rowsum_upper(w, m=6):
    """an upper bound for 2 sum_{k>=1} |1 - k^2 w^2| e^(-k^2 w^2/2) (requires w >= 1)"""
    tot = Fr(0)
    for k in range(1, m):
        x = k * k * w * w
        tot += abs(1 - x) * exp_neg_upper(x / 2)
    # k >= m: |1 - k^2 w^2| <= k^2 w^2 and e^(-k^2 w^2/2) <= q^k with q = e^(-m w^2/2);
    # sum_{k>=m} k^2 q^k <= m^2 q^m sum_{j>=0} (1+j)^2 q^j = m^2 q^m (1+q)/(1-q)^3
    q = exp_neg_upper(m * w * w / 2)
    check(0 < q < 1, 'C2 tail ratio')
    tail = w * w * m * m * q ** m * (1 + q) / (1 - q) ** 3
    return 2 * (tot + tail)


def control_c2(mutant):
    res = {}
    bound = Fr(5, 6)
    spacings = [Fr(2), Fr(3), Fr(4)] if mutant != 'M3' else [Fr(1), Fr(3), Fr(4)]
    for w in spacings:
        u = rowsum_upper(w)
        check(u <= bound, 'C2 row sum bound %s exceeds 5/6 at w=%s' % (ceil_dec(u, 8), w))
        res['w=%s' % w] = {'row_sum_upper': ceil_dec(u, 8), 'lambda_min_lower': floor_dec(1 - u, 8)}
    # monotonicity for w >= 2: d/dx (x^2 - 1) e^(-x^2/2) = x (3 - x^2) e^(-x^2/2), negative once x^2 > 3
    lhs = padd(pder([Fr(-1), Fr(0), Fr(1)]), pmul([Fr(-1), Fr(0), Fr(1)], [Fr(0), Fr(-1)]))
    check(lhs == [Fr(0), Fr(3), Fr(0), Fr(-1)], 'C2 derivative identity')
    check(Fr(2) ** 2 > 3, 'C2 k w >= 2 > sqrt(3)')
    res['monotone_for_w>=2'] = "((x^2-1) e^(-x^2/2))' = x (3 - x^2) e^(-x^2/2) < 0 for x >= 2"
    res['conclusion'] = 'lambda_min >= 1 - 5/6 = 1/6 for every spacing w >= 2 and every N (Gershgorin)'
    return res


# ---------------------------------------------------------------- C3: the constants of [1D] section 0, Gaussian kernel

def control_c3(mutant):
    lam = {2: Fr(1), 4: Fr(3), 6: Fr(15), 8: Fr(105)}            # (2j - 1)!!
    l2, l4, l6, l8 = lam[2], lam[4], lam[6], lam[8]
    D = l2 * l6 - l4 ** 2
    s3sq, s4sq = D / l2, l8 - l6 ** 2 / l4
    Q = 4 * l2 ** 2 * l4 * l8 + 26 * l2 * l4 ** 2 * l6 - 5 * l2 ** 2 * l6 ** 2 - 25 * l4 ** 4
    check(D == 6 and s3sq == 6 and s4sq == 30 and Q == 1620, 'C3 Gaussian moments')
    check(Q / (120 * l2 * l4 * D) == Fr(3, 4), 'C3 Q/(120 l2 l4 D) = 3/4')
    check(Q == 4 * l2 ** 2 * (l4 * l8 - l6 ** 2) + D * (25 * l4 ** 2 - l2 * l6)
          and Q == 4 * l2 ** 2 * l4 * s4sq + D * (24 * l4 ** 2 - D), 'C3 decomposition of Q at the Gaussian moments')
    check(l2 * l6 <= 25 * l4 ** 2, 'C3 sufficient condition for B2 > 0')
    s3, s4 = math.sqrt(float(s3sq)), math.sqrt(float(s4sq))
    p12 = 1 / (2 * math.pi * math.sqrt(float(l2 * l4)))
    pref = 2.0 if mutant != 'M4' else 1.0
    C0 = pref * 72 ** (-1 / 6) * math.gamma(7 / 6) * (2 * math.pi) ** -0.5 * p12 * s3 ** (4 / 3)
    mu = 2 ** (7 / 8) * math.gamma(11 / 8) / math.sqrt(math.pi)
    C1 = -(8 / 21) * 24 ** 0.25 * mu * (2 * math.pi) ** -0.5 * p12 * s4 ** 1.75 / s3
    C1b = (-(2 ** (25 / 8) / 7) * 3 ** -0.75 * math.pi ** -2 * math.gamma(11 / 8) * s4 ** 1.75 / s3
           * float(l2 * l4) ** -0.5)
    check(abs(C1 - C1b) <= 1e-12 * abs(C1), 'C3 the two printed forms of C1')
    I = 3 ** 0.25 / 2 * C1
    B2 = 2 ** 0.5 * 3 ** (1 / 3) * math.gamma(5 / 6) * (2 * math.pi) ** -0.5 * p12 * s3 ** (2 / 3) * float(Fr(3, 4))
    rate = math.sqrt(float(l4 / l2)) / (2 * math.pi)
    got = {'C0': '%.8f' % C0, 'C1': '%.8f' % C1, 'I': '%.8f' % I, 'B2': '%.8f' % B2,
           'per_crest_h^(-1/3)': '%.8f' % (C0 / 2 / rate), 'per_crest_h^(1/4)': '%.8f' % (I / 2 / rate),
           'per_crest_h^(1/3)': '%.8f' % (B2 / rate)}
    printed = {'C0': '0.11011038', 'C1': '-0.22760636', 'I': '-0.14977341', 'B2': '0.11502229',
               'per_crest_h^(-1/3)': '0.19971814', 'per_crest_h^(1/4)': '-0.27165891',
               'per_crest_h^(1/3)': '0.41725471'}
    for k in sorted(printed):
        check(got[k] == printed[k], 'C3 %s = %s, printed %s' % (k, got[k], printed[k]))
    check('%.5f' % (B2 / rate) == '0.41725', 'C3 [1D] prints the h^(1/3) per-crest coefficient as 0.41725')
    check('%.8f' % rate == '%.8f' % (math.sqrt(3) / (2 * math.pi)), 'C3 rate of maxima sqrt(3)/(2 pi)')
    return {'lambda_2j': ['1', '3', '15', '105'], 'D': str(D), 'sigma3^2': str(s3sq), 'sigma4^2': str(s4sq),
            'Q': str(Q), 'Q/(120 l2 l4 D)': '3/4', 'values_8_decimals': got, 'rate_of_maxima': '%.8f' % rate}


# ---------------------------------------------------------------- C4: the cell Sobolev bound

def sobolev_case(c, w, grid=256):
    """u(s) = sum c[k] (s/w)^k on [0, w]: an exact lower bound and a rigorous upper bound for sup|u|, and the base
    w^-1 int u^2 + w int u'^2"""
    u = trim([ck / w ** k for k, ck in enumerate(c)])
    du = pder(u)
    I0 = pint(pmul(u, u), Fr(0), w)
    I1 = pint(pmul(du, du), Fr(0), w)
    M1 = sum(k * abs(ck) for k, ck in enumerate(c)) / w              # >= sup |u'| on [0, w]
    eta = w / grid
    lo = max(abs(peval(u, w * Fr(j, grid))) for j in range(grid + 1))
    up = lo + eta / 2 * M1
    return lo, up, I0 / w + w * I1


def control_c4(mutant):
    rng = Lcg(4102026)
    const = Fr(2) if mutant != 'M2' else Fr(1)
    lengths = [Fr(1, 2), Fr(1), Fr(2), Fr(4), Fr(25, 2)]
    n = 0
    worst = Fr(0)
    witness = {}
    for w in lengths:
        cases = [[Fr(1), Fr(0), Fr(1, 2)]]                            # the witness 1 + (s/w)^2/2
        cases += [[rng.frac(9) for _ in range(6)] for _ in range(30)]
        for c in cases:
            lo, up, base = sobolev_case(c, w)
            check(up * up <= const * base, 'C4 Sobolev bound fails (w=%s, u=%s)' % (w, show(c)))
            if base > 0:
                worst = max(worst, lo * lo / base)
            n += 1
        lo, up, base = sobolev_case(cases[0], w)
        check(lo * lo == Fr(9, 4) and base == Fr(103, 60), 'C4 the witness is scale invariant')
        witness['w=%s' % w] = {'sup_u^2': str(lo * lo), "w^-1 int u^2 + w int u'^2": str(base)}
    check(Fr(9, 4) > Fr(103, 60), 'C4 the constant 1 is false')
    return {'polynomials_tested': n, 'interval_lengths': [str(w) for w in lengths],
            "max_sup^2/(w^-1 int u^2 + w int u'^2)": ceil_dec(worst, 6),
            'witness_u=1+(s/w)^2/2': witness,
            'sharp_constant_coth(1)_float': '%.6f' % (math.cosh(1.0) / math.sinh(1.0)),
            'reading': 'the bound holds with constant 2; constant 1 fails on the witness (9/4 > 103/60)'}


# ---------------------------------------------------------------- C5: the summation of Lemma F_R, at sample values

def control_c5(mutant):
    res = {}
    for x in (Fr(1, 2), Fr(1, 3), Fr(1, 10), Fr(1, 1000)):
        for M in (23, 30, 50):
            s = sum(x ** n for n in range(23, M + 1))
            check(s == (x ** 23 - x ** (M + 1)) / (1 - x), 'C5 geometric partial sum')
        check(x ** 23 / (1 - x) <= 2 * x ** 23, 'C5 x^23/(1-x) <= 2 x^23')
    check(Fr(1, 2) ** 4 == Fr(1, 16), 'C5 q^(1/4) <= 1/2 iff q <= 1/16')
    res['geometric'] = ('sum_{n=23}^{M} x^n = (x^23 - x^(M+1))/(1-x) and x^23/(1-x) <= 2 x^23 for x in '
                        '{1/2, 1/3, 1/10, 1/1000}; the ratios are <= 1/2 when q <= 1/16 and '
                        'h^(A^2/(16 sigma_F^2)) <= 1/2')
    for r in (Fr(1, 3), Fr(2, 7), Fr(1, 100)):
        q = 4 * r * r                                                  # q = 4 r^2, so q/4 = r^2 and q^(1/2) = 2 r
        for N in range(23, 61, 2):                                     # odd N: N/2 - 3 = (N - 6)/2, half-integer
            lhs = 2 ** N * (r * r) ** ((N - 7) // 2) * r              # (q/4)^(N/2 - 3) = r^(N - 6)
            rhs = 64 * q ** ((N - 7) // 2) * (2 * r)                  # 64 q^(N/2 - 3) = 64 q^((N-7)/2) q^(1/2)
            check(lhs == rhs, 'C5 2^N (q/4)^(N/2-3) = 64 q^(N/2-3)')
        for N in range(24, 61, 2):
            check(2 ** N * (r * r) ** ((N - 6) // 2) == 64 * q ** ((N - 6) // 2), 'C5 2^N (q/4)^(N/2-3) = 64 q^(N/2-3)')
    res['union_bound_step'] = '2^N (q/4)^(N/2-3) = 64 q^(N/2-3) with q/4 = eps (2e/lambda_*)^(1/2)'
    w = Fr(5, 2)
    T0 = 24 * w
    for t in (T0, T0 + Fr(1, 7), T0 + 3 * w, T0 + 100):
        N = (t - 2 * w) // w + 1
        check(N >= 23, 'C5 N >= 23')
        check(-t / 2 + w + (N - 1) * w <= t / 2 - w, 'C5 the last point lies in [-tau + w, tau - w]')
        check((N + 1) // 2 >= 12, 'C5 |G| = ceil(N/2) >= 12 >= 6')
    res['N(t)'] = 'N = floor((t - 2w)/w) + 1 >= 23 for t >= 24 w, y_(N-1) <= tau - w, and ceil(N/2) >= 12 (at w = 5/2)'
    A2_over_sigma2 = Fr(2)                                             # the smallest admissible A^2/sigma_F^2
    exp_h = (Fr(23, 32) if mutant == 'M5' else Fr(23, 16)) * A2_over_sigma2
    check(exp_h > 2, 'C5 band exponent %s not > 2' % exp_h)
    exp_q = (Fr(23, 4) - Fr(3, 2)) * Fr(1, 2)                         # q^(23/4 - 3/2) = q^(17/4), q ~ h^(1/2)
    log_q = (Fr(23, 4) - Fr(3, 2)) * Fr(1, 4)
    check(exp_q == Fr(17, 8) and exp_q > 2 and log_q == Fr(17, 16), 'C5 q-exponents')
    res['exponents'] = {'h^(23 A^2/(16 sigma_F^2)) at A^2 = 2 sigma_F^2': str(exp_h),
                        'q^(N/4 - 3/2) at N = 23, with q = O(h^(1/2) log^(1/4))': 'h^(%s) log^(%s)' % (exp_q, log_q),
                        'margin over h^2': str(min(exp_h, exp_q) - 2)}
    check(Fr(1, 2) * Fr(1, 8) == Fr(1, 16), 'C5 square root of the banded probability')
    res['square_root'] = 'P^(1/2) <= exp(-N R^2/(16 sigma_F^2)) + 8 q^(N/4 - 3/2)'
    return res


# ---------------------------------------------------------------- C6: the ingredients of Lemmas 4.3_R and 4.4_R

def negative_pivots(S):
    """number of negative eigenvalues of the symmetric rational matrix S, by exact LDL^T without pivoting
    (Sylvester's law of inertia); returns None if a zero pivot occurs"""
    n = len(S)
    M = [row[:] for row in S]
    neg = 0
    for i in range(n):
        piv = M[i][i]
        if piv == 0:
            return None
        if piv < 0:
            neg += 1
        for r in range(i + 1, n):
            f = M[r][i] / piv
            if f:
                for c in range(i, n):
                    M[r][c] -= f * M[i][c]
    return neg


def e_bounds():
    lo, t = Fr(0), Fr(1)
    for j in range(30):
        lo += t
        t = t / (j + 1)
    return lo, lo + 2 * t                    # the tail after 30 terms is below twice the next term


def control_c6(mutant):
    res = {}
    rng = Lcg(97531)
    lam = Fr(1, 3)
    cases = attained = 0
    for k in (4, 5, 6, 8, 10):
        for r in (1, 2, 3):
            for _ in range(6):
                Mx = [[rng.frac(5) for _ in range(k)] for _ in range(k)]
                MMt = [[sum(Mx[i][l] * Mx[j][l] for l in range(k)) for j in range(k)] for i in range(k)]
                us = [[rng.frac(7) for _ in range(k)] for _ in range(r)]
                S = [[MMt[i][j] - sum(u[i] * u[j] for u in us) for j in range(k)] for i in range(k)]
                neg = negative_pivots(S)                                # A - P - lam Id = M M^T - P
                if neg is None:
                    continue
                check(neg <= r, 'C6 interlacing: %d negative eigenvalues after a rank-%d downdate' % (neg, r))
                cases += 1
            # a family that attains r: P = c sum_{s<=r} e_s e_s^T with c > trace(M M^T)
            Mx = [[rng.frac(5) for _ in range(k)] for _ in range(k)]
            MMt = [[sum(Mx[i][l] * Mx[j][l] for l in range(k)) for j in range(k)] for i in range(k)]
            c = sum(MMt[i][i] for i in range(k)) + 1
            S = [[MMt[i][j] - (c if i == j and i < r else 0) for j in range(k)] for i in range(k)]
            neg = negative_pivots(S)
            check(neg is not None and neg == r, 'C6 the attaining family')
            allowed = r - 1 if mutant == 'M7' else r
            check(neg <= allowed,
                  'C6 interlacing allows only %d small eigenvalues after a rank-%d conditioning' % (allowed, r))
            attained += 1
    res['interlacing'] = {'random_cases': cases, 'attaining_cases': attained,
                          'statement': 'A - P - lam Id has at most rank(P) negative eigenvalues when A - lam Id >= 0'}
    elo, ehi = e_bounds()
    sqrtpi_lo = Fr(17724, 10000)                                       # sqrt(pi) = 1.77245...
    check(sqrtpi_lo ** 2 < Fr(314159, 100000), 'C6 sqrt(pi) lower bound')
    for m in range(3, 301):
        # Gamma(m/2 + 1) >= (m/(2e))^(m/2), i.e. Gamma(m/2 + 1)^2 >= (m/(2e))^m; use e >= elo
        if m % 2 == 0:
            n = m // 2
            g2 = Fr(1)
            for i in range(2, n + 1):
                g2 *= i
            g2 = g2 * g2
        else:
            # Gamma(n + 3/2) = (2n+2)! sqrt(pi)/(4^(n+1) (n+1)!)
            n = (m - 1) // 2
            num, den = 1, 1
            for i in range(2, 2 * n + 3):
                num *= i
            for i in range(2, n + 2):
                den *= i
            g2 = (Fr(num, 4 ** (n + 1) * den) * sqrtpi_lo) ** 2
        check(g2 >= (Fr(m, 2) / elo) ** m, 'C6 Stirling lower bound fails at m=%d' % m)
    for k in range(6, 200):
        check(Fr(k, k - 3) <= 2, 'C6 k/(k-3) <= 2')
    res['stirling'] = 'Gamma(m/2 + 1) >= (m/(2e))^(m/2) for 3 <= m <= 300; k/(k-3) <= 2 for k >= 6'
    c = Fr(4) if mutant == 'M6' else Fr(5)
    check((Fr(1, 2) + 1 / c) ** 2 <= Fr(1, 2),
          'C6 threshold R0 = %s (M2^(1/2) + 1) does not give R/sqrt(2) - R/%s >= R/2' % (c, c))
    res['R0_threshold'] = {'R0': '%s (M2^(1/2) + 1)' % c, '(1/2 + 1/%s)^2' % c: str((Fr(1, 2) + 1 / c) ** 2),
                           'needed': '<= 1/2'}
    check((Fr(1, 2) + Fr(1, 4)) ** 2 > Fr(1, 2), 'C6 the factor 4 fails')
    res['factor_4_fails'] = '(1/2 + 1/4)^2 = 9/16 > 1/2'
    return res


def main():
    mutant = parse_args(sys.argv[1:])
    controls = [('C1', control_c1), ('C2', control_c2), ('C3', control_c3), ('C4', control_c4),
                ('C5', control_c5), ('C6', control_c6)]
    out = {'object': OBJECT, 'scientific_effect': 'NONE', 'mutants': MUTANTS, 'controls': {}}
    try:
        for name, fn in controls:
            out['controls'][name] = fn(mutant)
    except ControlFailure as exc:
        print(json.dumps({'mutant': mutant, 'failed': str(exc)}), file=sys.stderr)
        sys.exit(1)
    if mutant is not None:
        print('mutant %s was not detected' % mutant, file=sys.stderr)
        sys.exit(3)
    sys.stdout.write(json.dumps(out, indent=1, sort_keys=True, ensure_ascii=True) + '\n')


if __name__ == '__main__':
    main()
