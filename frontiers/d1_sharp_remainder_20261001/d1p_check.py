#!/usr/bin/env python3
"""Exact controls for Theorem 1D+ (CL-D1-SHARP-REMAINDER-20261001-v1.1).

Standard library only.  Exact rationals (fractions.Fraction) for C1-C4 and C7, Decimal at 60 digits for C5, and
float quadrature (reported to 6 significant digits) for C6.  Output: one JSON document on stdout, equal to RESULTS.json.

    python3 -B -S d1p_check.py                 # exit 0
    python3 -B -S d1p_check.py --mutant M3     # exit 1 (each mutant breaks its own control)
    python3 -B -S d1p_check.py --mutant XX     # exit 2 (unknown label)

Scientific effect: NONE.  The controls check exact algebra, margins and arithmetic; C5 and C6 are numerical
consistency checks, not proofs.
"""
import json
import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

MUTANTS = {
    'M1': 'C1: edge function Gamma_+ with (3 phi + 1) in place of (3 phi - 1)',
    'M2': 'C2: edge margin eta_0 = 1/50 in place of 1/100',
    'M3': 'C3: odd a5 profile with 1/60 in place of 1/120',
    'M4': 'C4: the even part treated as odd (no cancellation in the window length)',
    'M5': 'C5: first-order edge coefficient 1/6 in place of 1/12',
    'M6': 'C6: Lemma E bound v2 min(1, s)/4 in place of 2 v2 min(1, s)',
    'M7': 'C7: delta = 1/8 in place of 1/10',
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
                print('usage: d1p_check.py [--mutant M1..M7]', file=sys.stderr)
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

def padd(p, q):
    n = max(len(p), len(q))
    return trim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)])


def pscale(p, c):
    return trim([c * a for a in p])


def pmul(p, q):
    if not p or not q:
        return []
    out = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return trim(out)


def ppow(p, k):
    out = [Fr(1)]
    for _ in range(k):
        out = pmul(out, p)
    return out


def pder(p):
    return trim([i * p[i] for i in range(1, len(p))])


def peval(p, x):
    acc = 0
    for a in reversed(p):
        acc = acc * x + a
    return acc


def trim(p):
    p = [Fr(a) for a in p]
    while p and p[-1] == 0:
        p.pop()
    return p


def pcompose_scale(p, c):
    """p(c X)"""
    return trim([a * c ** i for i, a in enumerate(p)])


X = [Fr(0), Fr(1)]
HALF = Fr(1, 2)
Q2 = padd(pmul(X, X), [Fr(-1, 4)])          # X^2 - 1/4
Q2SQ = pmul(Q2, Q2)                          # (X^2 - 1/4)^2


def g_poly(phi):
    """[1D] (3.1): g_phi(X) = 2 (X + 1/2)^2 (X - 1) + 3 phi (X^2 - 1/4)^2."""
    return padd(pmul(pscale(ppow(padd(X, [HALF]), 2), 2), padd(X, [Fr(-1)])), pscale(Q2SQ, 3 * phi))


def rat_points(n):
    pts = []
    k = 1
    while len(pts) < n:
        for q in (Fr(k, 7), Fr(-k, 7), Fr(k, 13) + Fr(1, 101), Fr(-k, 11) - Fr(1, 97)):
            if q != 0 and q not in pts:
                pts.append(q)
        k += 1
    return pts[:n]


# ---------------------------------------------------------------- C1: the model's parity split and the edge functions

def control_c1(mutant):
    res = {}
    # parity split: g_phi = (2X^3 - 3X/2) + (3 phi (X^2 - 1/4)^2 - 1/2); identity in (X, phi) of degree (4, 1)
    odd = [Fr(0), Fr(-3, 2), Fr(0), Fr(2)]
    for phi in rat_points(5):
        target = padd(padd(odd, pscale(Q2SQ, 3 * phi)), [Fr(-1, 2)])
        check(g_poly(phi) == target, 'C1 parity split fails at phi=%s' % phi)
        # g' = 12 phi (X^2 - 1/4)(X - X3) = 6 (X^2 - 1/4)(1 + 2 phi X)
        check(pder(g_poly(phi)) == pmul(pscale(Q2, 6), [Fr(1), 2 * phi]), "C1 g' factorization fails")
        # mirror symmetry g(-X, -phi) = -1 - g(X, phi)
        gm = pcompose_scale(g_poly(-phi), Fr(-1))
        check(gm == padd([Fr(-1)], pscale(g_poly(phi), -1)), 'C1 mirror symmetry fails')
    res['parity_split_and_gprime_factorization'] = True
    res['mirror_symmetry_g(-X,-phi)=-1-g(X,phi)'] = True
    # edge functions at X3 = -1/(2 phi): Gamma_+ = g(X3) + 1, Gamma_- = g(X3)
    Np = pmul(ppow([Fr(1), Fr(1)], 3), [Fr(-1), Fr(3)] if mutant != 'M1' else [Fr(1), Fr(3)])   # (phi+1)^3 (3phi-1)
    Nm = pmul(ppow([Fr(-1), Fr(1)], 3), [Fr(1), Fr(3)])                                          # (phi-1)^3 (3phi+1)
    D = [Fr(0), Fr(0), Fr(0), Fr(16)]                                                             # 16 phi^3
    pts = rat_points(200)
    for phi in pts:
        X3 = -1 / (2 * phi)
        gX3 = peval(g_poly(phi), X3)
        check(gX3 + 1 == peval(Np, phi) / peval(D, phi), 'C1 Gamma_+ identity fails at phi=%s' % phi)
        check(gX3 == peval(Nm, phi) / peval(D, phi), 'C1 Gamma_- identity fails at phi=%s' % phi)
        check(peval(Nm, phi) / peval(D, phi) == -peval(Np, -phi) / peval(D, -phi), 'C1 Gamma_-(phi) = -Gamma_+(-phi) fails')
        # g''(X3) = 3 (1 - phi^2)/phi
        check(peval(pder(pder(g_poly(phi))), X3) == 3 * (1 - phi * phi) / phi, "C1 g''(X3) fails")
    res['Gamma_identities_rational_points'] = len(pts)
    # Gamma_+' = (N'D - N D')/D^2 and N'D - N D' = 48 phi^2 (1 - phi^2)^2, i.e. Gamma' = 3 (1 - phi^2)^2/(16 phi^4)
    W = padd(pmul(pder(Np), D), pscale(pmul(Np, pder(D)), -1))
    target = pmul([Fr(0), Fr(0), Fr(48)], ppow([Fr(1), Fr(0), Fr(-1)], 2))
    check(W == target, "C1 Gamma_+' fails")
    Wm = padd(pmul(pder(Nm), D), pscale(pmul(Nm, pder(D)), -1))
    check(Wm == target, "C1 Gamma_-' fails")
    check(padd(Np, pscale(Nm, -1)) == D, 'C1 Gamma_+ - Gamma_- = 1 fails')
    third = Fr(1, 3)
    slope = Fr(3) * (1 - third ** 2) ** 2 / (16 * third ** 4)
    check(slope == 12 and peval(Np, third) == 0 and peval(Nm, -third) == 0, 'C1 slope 12 at +-1/3 fails')
    # second derivative of Gamma_+ at 1/3 (recorded): (W'D^2 - W 2 D D')/D^4 at 1/3
    Dv, D1v, Wv, W1v = peval(D, third), peval(pder(D), third), peval(W, third), peval(pder(W), third)
    second = (W1v * Dv ** 2 - Wv * 2 * Dv * D1v) / Dv ** 4
    res['Gamma_prime_numerator'] = '48 phi^2 (1 - phi^2)^2'
    res['Gamma_slope_at_pm_1/3'] = str(slope)
    res['Gamma_plus_second_derivative_at_1/3'] = str(second)
    check(second == -162, 'C1 Gamma_+ second derivative')
    return res


# ---------------------------------------------------------------- C2: the margins of Lemma W on J_+ and J_-

def control_c2(mutant):
    res = {}
    eta0 = Fr(1, 100) if mutant != 'M2' else Fr(1, 50)
    lo, hi = Fr(1, 3) - eta0, Fr(1, 3) + eta0
    Gp = lambda p: (p + 1) ** 3 * (3 * p - 1) / (16 * p ** 3)
    # g(-2) = 675 phi/16 - 27/2 and g(2) + 1 = 675 phi/16 + 27/2, identities in phi (degree 1)
    for phi in (Fr(1, 5), Fr(2, 7), Fr(1, 3)):
        check(peval(g_poly(phi), Fr(-2)) == Fr(675, 16) * phi - Fr(27, 2), 'C2 g(-2) formula')
        check(peval(g_poly(phi), Fr(2)) + 1 == Fr(675, 16) * phi + Fr(27, 2), 'C2 g(2)+1 formula')
        check(peval(g_poly(phi), Fr(3, 2)) == 12 * phi + 4 and peval(g_poly(phi), Fr(-3, 2)) == 12 * phi - 5, 'C2 g(+-3/2)')
    gm2 = Fr(675, 16) * lo - Fr(27, 2)                       # increasing in phi: min on J_+ at lo
    res['g(-2)_min_on_J+'] = str(gm2)
    check(gm2 >= Fr(9, 64), 'C2 margin g(-2) >= 9/64 fails on J_+')
    check(Fr(675, 16) * (-lo) + Fr(27, 2) <= -Fr(9, 64), 'C2 margin g(2)+1 <= -9/64 fails on J_-')
    gpp = lambda p: 3 * (1 - p * p) / p                      # g''(X3), decreasing in phi > 0
    res['g2_at_X3_min_on_J+'] = '%.6f' % float(gpp(hi))
    check(gpp(hi) >= Fr(77, 10) and gpp(-hi) <= -Fr(77, 10), "C2 margin g''(X3) >= 7.7 fails")
    check(Gp(hi) <= Fr(3, 25) and Gp(lo) >= -Fr(13, 100), 'C2 Gamma_+ range on J_+ fails')
    res['Gamma_plus_on_J+'] = ['%.6f' % float(Gp(lo)), '%.6f' % float(Gp(hi))]
    X3lo, X3hi = -1 / (2 * lo), -1 / (2 * hi)                # X3 range on J_+
    check(X3lo >= -Fr(31, 20) and X3hi <= -Fr(29, 20), 'C2 X3 range [-1.55, -1.45] fails')
    check(12 * lo * (1 - Fr(1, 4)) >= Fr(29, 10), 'C2 12 phi (X^2 - 1/4) >= 2.9 on [-2,-1] fails')
    # |g'| >= 1.8 (1/2 - |X|) on (-1/2, 1/2): 12 phi (1/2 + |X|)(X - X3) >= 12 lo (1/2)(-1/2 - X3hi)
    check(12 * lo * HALF * (-HALF - X3hi) >= Fr(9, 5), "C2 |g'| >= 1.8 (1/2 - |X|) fails")
    # g' >= 1.7 |X + 1/2| on [-1, -1/2): 12 phi (|X| + 1/2)(X - X3) >= 12 lo (1)(-1 - X3hi)
    check(12 * lo * (-1 - X3hi) >= Fr(17, 10), "C2 g' >= 1.7 |X + 1/2| fails")
    # g''' = 12 + 72 phi X (identity); on [-1.6, -1.4]: |g'''| <= 12 + 72 hi (8/5) <= 52; within 1/20 of X3, g'' >= 5.1
    for phi in (lo, hi):
        check(pder(pder(pder(g_poly(phi)))) == [Fr(12), 72 * phi], "C2 g''' formula")
    g3 = 12 + 72 * hi * Fr(8, 5)
    check(g3 <= 52 and Fr(77, 10) - Fr(52, 20) >= Fr(51, 10), "C2 g'' >= 5.1 near X3 fails")
    res["g3_bound_on_[-1.6,-1.4]"] = '%.4f' % float(g3)
    # quadratic growth: g - g(X3) = (X - X3)^2 q(X), q = 3 phi X^2 - X + (1 - 6 phi^2)/(4 phi)  (identity in X)
    for phi in (lo, hi, Fr(1, 3), Fr(2, 7), Fr(-1, 5), Fr(3, 4), Fr(-5, 9), Fr(7, 3)):     # identity of degree <= 4 in phi after clearing
        X3 = -1 / (2 * phi)
        q = [(1 - 6 * phi * phi) / (4 * phi), Fr(-1), 3 * phi]
        lhs = padd(g_poly(phi), [-peval(g_poly(phi), X3)])
        check(lhs == pmul(ppow([-X3, Fr(1)], 2), q), 'C2 quadratic-growth identity fails')
    # on [-2,-1]: dq/dX = 6 phi X - 1 < 0, so the min is at X = -1: q(-1) = 3 phi/2 + 1 + 1/(4 phi);
    # d/dphi q(-1) = 3/2 - 1/(4 phi^2) < 0 on J_+ (phi^2 < 1/6), so the min over J_+ is at hi
    check(6 * hi * (-1) - 1 < 0 and hi * hi < Fr(1, 6), 'C2 quadratic-growth monotonicity fails')
    qmin = Fr(3, 2) * hi + 1 + 1 / (4 * hi)
    res['quadratic_growth_min_on_[-2,-1]xJ+'] = '%.6f' % float(qmin)
    check(qmin >= Fr(224, 100), 'C2 quadratic-growth factor >= 2.24 fails')
    # mirror on [1,2] x J_-: (g(X3) - g(X))/(X - X3)^2 = -q, minimal at X = 1, phi = -hi
    qm = -(3 * (-hi) * 1 - 1 + (1 - 6 * hi * hi) / (4 * (-hi)))
    check(qm == qmin, 'C2 mirror quadratic-growth factor fails')
    # right side: g + 1 = (X - 1/2)^2 [2(X + 1) + 3 phi (X + 1/2)^2]
    for phi in (lo, hi):
        rhs = pmul(ppow(padd(X, [-HALF]), 2), padd(pscale(padd(X, [Fr(1)]), 2), pscale(ppow(padd(X, [HALF]), 2), 3 * phi)))
        check(padd(g_poly(phi), [Fr(1)]) == rhs, 'C2 g + 1 factorization fails')
        check(12 * phi + 4 >= 7, 'C2 g(3/2) >= 7 fails')
    res['eta0'] = str(eta0)
    res['J_plus'] = [str(lo), str(hi)]
    return res


# ---------------------------------------------------------------- C3: the pin algebra of Lemma Phi

def control_c3(mutant):
    res = {}
    for tau in (Fr(1, 7), Fr(2, 13), Fr(3, 41)):
        t = 2 * tau
        h = Fr(5, 17) * t ** 4
        # odd cubic H0(x) = h (2 (x/t)^3 - (3/2)(x/t)): H0'(tau) = 0, H0(tau) = -h/2
        H0 = [Fr(0), -Fr(3, 2) * h / t, Fr(0), 2 * h / t ** 3]
        check(peval(pder(H0), tau) == 0 and peval(H0, tau) == -h / 2, 'C3 H0 pins')
        # odd Hermite basis at tau
        p1 = [Fr(0), Fr(3, 2) / tau, Fr(0), -Fr(1, 2) / tau ** 3]
        p2 = [Fr(0), -tau / 2 / tau, Fr(0), tau / 2 / tau ** 3]
        check(peval(p1, tau) == 1 and peval(pder(p1), tau) == 0 and peval(p2, tau) == 0 and peval(pder(p2), tau) == 1,
              'C3 Hermite basis')
        # odd profiles: R_o = x^5/120 -> R~_o(tX) = (t^5/120) X (X^2-1/4)^2 ; R_o = x^7/5040 -> (t^7/10080) X (X^2-1/4)^2 (2X^2+1)
        for deg, prof, const in ((5, pmul(X, Q2SQ), Fr(1, 120) if mutant != 'M3' else Fr(1, 60)),
                                 (7, pmul(pmul(X, Q2SQ), [Fr(1), Fr(0), Fr(2)]), Fr(1, 10080))):
            Ro = [Fr(0)] * deg + [Fr(1, math.factorial(deg))]
            Rt = padd(Ro, padd(pscale(p1, -peval(Ro, tau)), pscale(p2, -peval(pder(Ro), tau))))
            check(pcompose_scale(Rt, t) == pscale(prof, const * t ** deg), 'C3 odd profile degree %d' % deg)
        # even pins: f_e = a2 x^2/2 + a4 x^4/24 + R, a2 = -a4 tau^2/6 - R'(tau)/tau
        for a4, R in ((Fr(1), [Fr(0)] * 6 + [Fr(1, 720)]), (Fr(0), [Fr(0)] * 8 + [Fr(1, 40320)]), (Fr(3, 5), [Fr(0)] * 6 + [Fr(2, 7)])):
            a2 = -a4 * tau ** 2 / 6 - peval(pder(R), tau) / tau
            fe = padd([Fr(0), Fr(0), a2 / 2, Fr(0), a4 / 24], R)
            lhs = padd(fe, [-peval(fe, tau)])
            Rt = padd(padd(R, [-peval(R, tau)]), pscale(padd(pmul(X, X), [-tau ** 2]), -peval(pder(R), tau) / (2 * tau)))
            rhs = padd(pscale(ppow(padd(pmul(X, X), [-tau ** 2]), 2), a4 / 24), Rt)
            check(lhs == rhs, 'C3 even pin identity')
            check(peval(pder(fe), tau) == 0, 'C3 even pin')
            E1 = peval(pder(pder(fe)), tau)
            check(E1 == a4 * tau ** 2 / 3 + peval(pder(pder(R)), tau) - peval(pder(R), tau) / tau, 'C3 E1 identity')
        # even profiles: a4 -> (t^4/24)(X^2-1/4)^2 ; R = x^6/720 -> (t^6/720)(X^2-1/4)^2 (X^2+1/2)
        R6 = [Fr(0)] * 6 + [Fr(1, 720)]
        Rt6 = padd(padd(R6, [-peval(R6, tau)]), pscale(padd(pmul(X, X), [-tau ** 2]), -peval(pder(R6), tau) / (2 * tau)))
        check(pcompose_scale(Rt6, t) == pscale(pmul(Q2SQ, [HALF, Fr(0), Fr(1)]), t ** 6 / 720), 'C3 even sextic profile')
        check(pcompose_scale(ppow(padd(pmul(X, X), [-tau ** 2]), 2), t) == pscale(Q2SQ, t ** 4), 'C3 even quartic profile')
        # regression constant: (m/h)(t^4/24)(tau^2 V/3)/((tau^4/9) V) with m/h = 6/t^2 equals 3
        check(Fr(6) / t ** 2 * t ** 4 / 24 * tau ** 2 / 3 * 9 / tau ** 4 == 3, 'C3 regression constant')
    res['odd_profiles'] = ['X (X^2-1/4)^2 t^5/120', 'X (X^2-1/4)^2 (2X^2+1) t^7/10080']
    res['even_profiles'] = ['(X^2-1/4)^2 t^4/24', '(X^2-1/4)^2 (X^2+1/2) t^6/720']
    # second derivative of the odd cubic at 1/2, and the odd profile value at 3/2
    check(peval(pder(pder([Fr(0), -Fr(3, 2), Fr(0), Fr(2)])), HALF) == 6, 'C3 (2X^3 - 3X/2)\'\'(1/2) = 6')
    v32 = peval(pmul(X, Q2SQ), Fr(3, 2))
    check(v32 == 6, 'C3 X (X^2 - 1/4)^2 at 3/2')
    # Gaussian kernel: lambda_{2k} = (2k-1)!!; E[a5 | a1 = 0, a3 = alpha] = alpha (l4 l6 - l2 l8)/D = -10 alpha
    lam = {2: Fr(1), 4: Fr(3), 6: Fr(15), 8: Fr(105)}
    Dg = lam[2] * lam[6] - lam[4] ** 2
    r5 = (lam[4] * lam[6] - lam[2] * lam[8]) / Dg
    check(Dg == 6 and r5 == -10, 'C3 Gaussian regression coefficient')
    # E_Q O(3/2) leading term: r5 alpha t^5/(120 h) * 6 with alpha = 12 h/t^3 -> 6 r5 t^2 * 12/120 = -6 t^2
    lead = r5 * 12 * v32 / 120
    check(lead == -6, 'C3 E_Q O(3/2)/t^2 -> -6')
    res['Gaussian_E[a5|a1=0,a3=alpha]/alpha'] = str(r5)
    res['Gaussian_E_QO(3/2)/t^2_leading'] = str(lead)
    return res


# ---------------------------------------------------------------- C4: the window length (3.3), parity cancellation

class Lcg:
    def __init__(self, seed):
        self.x = seed

    def frac(self, den):
        self.x = (6364136223846793005 * self.x + 1442695040888963407) % (1 << 64)
        return Fr((self.x >> 33) % (2 * den + 1) - den, den)


def control_c4(mutant):
    rng = Lcg(20261001)
    n = 0
    for _ in range(50):
        o = pmul(pmul(X, Q2SQ), [rng.frac(9), Fr(0), rng.frac(9)])         # odd, double zeros at +-1/2
        b = pmul(Q2SQ, [rng.frac(9), Fr(0), rng.frac(9)])                  # even
        e = pmul(Q2SQ, [rng.frac(9), Fr(0), rng.frac(9)])                  # even (E-hat)
        eta = lambda phi, x: peval(o, x) + peval(b, x) + phi * peval(e, x)
        third, x32 = Fr(1, 3), Fr(3, 2)
        length = (eta(-third, x32) - eta(third, -x32)) / 12
        pred = peval(o, x32) / 6 - peval(e, x32) / 18
        if mutant == 'M4':
            pred += peval(b, x32) / 6
        check(length == pred, 'C4 window-length identity (3.3) fails')
        # the even part B moves both edges by the same amount -B(3/2)/12
        check(-eta(third, -x32) / 12 - (-(eta(third, -x32) - peval(b, -x32)) / 12) == -peval(b, x32) / 12, 'C4 translation')
        n += 1
    return {'random_triples': n, 'identity': 'phi+ - phi- - 2/3 = O(3/2)/6 - Ehat(3/2)/18 + O(eps^2) (Ehat even); B cancels'}


# ---------------------------------------------------------------- C5: Lemma W numerically (Decimal, 60 digits)

def control_c5(mutant):
    getcontext().prec = 60
    D = Decimal
    coef = D(1) / D(12) if mutant != 'M5' else D(1) / D(6)

    def to_dec(p):
        return [D(a.numerator) / D(a.denominator) for a in p]

    def ev(p, x):
        acc = D(0)
        for a in reversed(p):
            acc = acc * x + a
        return acc

    shapes = {
        'odd X(X^2-1/4)^2': (pmul(X, Q2SQ), [], []),
        'even (X^2-1/4)^2(X^2+1/2)': ([], pmul(Q2SQ, [HALF, Fr(0), Fr(1)]), []),
        'mixed with phi-profile': (pmul(X, Q2SQ), pmul(Q2SQ, [HALF, Fr(0), Fr(1)]), pmul(Q2SQ, [Fr(0), Fr(0), Fr(1)])),
        'generic (X^2-1/4)^2(1+2X-X^2)/2': (pmul(Q2SQ, [Fr(0), Fr(1)]), pmul(Q2SQ, [HALF, Fr(0), -HALF]), []),
    }
    out = {}
    for name, (o, b, e) in shapes.items():
        ratios = []
        for eps in (Fr(1, 1000), Fr(1, 10000), Fr(1, 100000)):
            base0 = padd(pscale(o, eps), pscale(b, eps))
            prof = pscale(e, eps)

            def field(phi):
                # F_phi = g_phi + eta0 + phi * Ehat  (polynomial with Decimal coefficients)
                gp = to_dec(g_poly(Fr(0)))
                q = to_dec(Q2SQ)
                b0 = to_dec(base0)
                pr = to_dec(prof)
                n = max(len(gp), len(q), len(b0), len(pr))
                get = lambda p, i: p[i] if i < len(p) else D(0)
                return [get(gp, i) + 3 * phi * get(q, i) + get(b0, i) + phi * get(pr, i) for i in range(n)]

            def crit_value(phi, x0, sign):
                p = field(phi)
                d1 = [i * p[i] for i in range(1, len(p))]
                d2 = [i * d1[i] for i in range(1, len(d1))]
                x = x0
                for _ in range(60):
                    step = ev(d1, x) / ev(d2, x)
                    x -= step
                    if abs(step) < D(10) ** -50:
                        break
                check(sign * ev(d2, x) > 0, 'C5 critical point not nondegenerate')
                check(D('1.4') <= abs(x) <= D('1.6'), 'C5 critical point outside [1.4, 1.6]')
                return ev(p, x)

            def root(fun, lo, hi):
                flo = fun(lo)
                for _ in range(120):
                    mid = (lo + hi) / 2
                    fm = fun(mid)
                    if (fm > 0) == (flo > 0):
                        lo, flo = mid, fm
                    else:
                        hi = mid
                return (lo + hi) / 2

            third = D(1) / D(3)
            R = root(lambda ph: crit_value(ph, -1 / (2 * ph), 1) + 1, third - D('0.01'), third + D('0.01'))
            L = root(lambda ph: crit_value(ph, -1 / (2 * ph), -1), -third - D('0.01'), -third + D('0.01'))
            eta = lambda phi, x: ev(to_dec(base0), x) + phi * ev(to_dec(prof), x)
            dp = -coef * eta(third, D('-1.5'))
            dm = -coef * eta(-third, D('1.5'))
            ed = D(eps.numerator) / D(eps.denominator)
            rp = (R - third - dp) / ed ** 2
            rm = (L + third - dm) / ed ** 2
            pred_len = ev(to_dec(pscale(o, eps)), D('1.5')) / 6 - ev(to_dec(prof), D('1.5')) / 18
            rl = (R - L - 2 * third - pred_len) / ed ** 2
            check(abs(rp) <= 10 and abs(rm) <= 10 and abs(rl) <= 20, 'C5 first-order edge formula fails (%s)' % name)
            ratios.append(['%.6g' % float(rp), '%.6g' % float(rm), '%.6g' % float(rl)])
        # stabilization: the eps^-2 ratios at the two smallest eps agree to 2%
        for k in range(3):
            a, b2 = float(ratios[1][k]), float(ratios[2][k])
            check(abs(a - b2) <= 0.02 * max(1.0, abs(b2)), 'C5 ratio does not stabilize (%s)' % name)
        out[name] = {'eps (shape coefficient)': ['1e-3', '1e-4', '1e-5'],
                     '(phi+ - 1/3 - d+)/eps^2, (phi- + 1/3 - d-)/eps^2, (length - pred)/eps^2': ratios}
    return out


# ---------------------------------------------------------------- C6: Lemma E numerically (float, reported to 6 digits)

def control_c6(mutant):
    Phi = lambda x: 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    phi = lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi)

    def gam1(S):                    # E[(S^2 - Z^2) 1{|Z| < S}], S >= 0
        if S <= 0:
            return 0.0
        return (S * S - 1) * (2 * Phi(S) - 1) + 2 * S * phi(S)

    def part(S, c):                 # E[(S^2 - Z^2) 1{|Z| < min(S, c)}], S > 0
        if S <= 0:
            return 0.0
        a = min(S, c)
        P = 2 * Phi(a) - 1
        return S * S * P - (P - 2 * a * phi(a))

    def expect(fun, n=2000, zmax=10.0):     # composite Simpson for E f(Z)
        hstep = 2 * zmax / n
        tot = 0.0
        for i in range(n + 1):
            z = -zmax + i * hstep
            w = 1 if i in (0, n) else (4 if i % 2 else 2)
            tot += w * fun(z) * phi(z)
        return tot * hstep / 3

    bound = 2.0 if mutant != 'M6' else 0.25
    rows = []
    worst = [0.0, 0.0]
    for s in (0.02, 0.1, 0.3, 1.0, 2.0, 3.0, 5.0, 8.0):
        for rr in (s / 8, s / 32):
            d1 = (expect(lambda z: gam1(s + rr * z)) - gam1(s)) / rr ** 2
            d3 = (expect(lambda z: part(s + rr * z, s / 3)) - part(s, s / 3)) / rr ** 2
            q1, q3 = d1 / min(1.0, s), d3 / min(1.0, s)
            check(d1 > -1e-6 and d3 > -1e-6, 'C6 lower bound fails at s=%g' % s)
            check(q1 <= bound and q3 <= bound, 'C6 Lemma E bound fails at s=%g: %g %g' % (s, q1, q3))
            worst = [max(worst[0], q1), max(worst[1], q3)]
            if rr == s / 32:
                lim1 = 2 * Phi(s) - 1 + 2 * s * phi(s)
                lim3 = 2 * Phi(s / 3) - 1
                check(abs(d1 - lim1) <= 0.05 * lim1 and abs(d3 - lim3) <= 0.05 * lim3, 'C6 small-v2 limit fails at s=%g' % s)
                rows.append(['%.6g' % s, '%.6g' % d1, '%.6g' % lim1, '%.6g' % d3, '%.6g' % lim3])
    return {'bound_checked': '0 <= (G - g)/v2 <= 2 min(1, s) on the 16-point grid s in {0.02,...,8}, sqrt(v2/v1) in {s/8, s/32}',
            'sup_ratio_theta1': '%.4g' % worst[0], 'sup_ratio_theta1/3': '%.4g' % worst[1],
            's, D1, limit1, D1/3, limit1/3 (v2/v1 = s^2/1024)': rows}


# ---------------------------------------------------------------- C7: the ledger

def control_c7(mutant):
    res = {}
    # int_0^infty t^2 min(1, h/t^4) dt: substitute t = h^{1/4} u, giving h^{3/4} [int_0^1 u^2 du + int_1^infty u^{-2} du];
    # both pieces integrated exactly (antiderivatives u^3/3 and -1/u)
    piece1 = peval([Fr(0), Fr(0), Fr(0), Fr(1, 3)], Fr(1)) - peval([Fr(0), Fr(0), Fr(0), Fr(1, 3)], Fr(0))
    piece2 = Fr(0) - (-Fr(1) / Fr(1))
    check(piece1 + piece2 == Fr(4, 3), 'C7 the (4/3) h^(3/4) integral fails')
    res['int_t2_min(1,h/t4)/h^(3/4)'] = str(piece1 + piece2)
    delta = Fr(1, 10) if mutant != 'M7' else Fr(1, 8)
    band = 3 - Fr(11) / (5 - delta)
    res['band_tail_exponent_3-11/(5-delta)'] = str(band)
    check(band >= Fr(3, 4), 'C7 band-tail exponent below 3/4')
    check(3 - Fr(11) / (5 - Fr(1, 9)) == Fr(3, 4), 'C7 threshold delta = 1/9')
    res['recorded_1D_exponents_at_delta_1/10'] = {'2-7/(5-delta)': str(2 - Fr(7) / (5 - delta)), '3/(5-delta)': str(Fr(3) / (5 - delta))}
    # Proposition M: t = (h/u)^{1/4}, t^2 dt = (1/4) h^{3/4} u^{-7/4} du; the integrand t^2 s with s ~ u gives u^{-3/4}
    exp_u = 1 + Fr(-1, 2) - Fr(5, 4)
    check(exp_u == Fr(-3, 4) and exp_u > -1, 'C7 integrability at u -> 0')
    res['PropM_integrand_exponent_at_u->0'] = str(exp_u)
    # exponent sets: fold {-1/3 + 2k/3}, cusp {1/4 + j/2}; disjoint (8k = 7 + 6j has no solution); quintic scale 4/5
    fold = {Fr(-1, 3) + Fr(2 * k, 3) for k in range(200)}
    cusp = {Fr(1, 4) + Fr(j, 2) for j in range(200)}
    check(not (fold & cusp), 'C7 exponent sets intersect')
    nxt = sorted(e for e in (fold | cusp) if e > Fr(1, 3))[:2]
    check(nxt == [Fr(3, 4), Fr(1)], 'C7 next fold/cusp exponents')
    res['next_fold_cusp_exponents_after_1/3'] = [str(e) for e in nxt]
    check(Fr(4, 5) not in fold and Fr(4, 5) not in cusp, 'C7 4/5 in a set')
    res['recorded_heuristic_quintic_scale_exponent'] = '4/5 (Remark 5.1; not derived here)'
    res['recorded_remainder_improvement'] = {'1D_(1D.2)': '1/2', 'here': '3/4'}
    return res


def main():
    mutant = parse_args(sys.argv[1:])
    controls = [('C1', control_c1), ('C2', control_c2), ('C3', control_c3), ('C4', control_c4),
                ('C5', control_c5), ('C6', control_c6), ('C7', control_c7)]
    out = {'object': 'CL-D1-SHARP-REMAINDER-20261001-v1.1', 'scientific_effect': 'NONE',
           'mutants': MUTANTS, 'controls': {}}
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
