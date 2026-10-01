#!/usr/bin/env python3
"""Exact controls for CL-D1-THIRD-ORDER-20261001-v1 (frontiers/d1_third_order_law_20261001/PROOF.md).
Standard library only. Run: python3 -B -S d1_check.py   (and with -O; output byte-identical).
Mutants: --mutant M1|M2|M3|M4|M5 must exit 1; an unknown label exits 2.

  C1 the constants: exponent bookkeeping over primes and symbols, rational exponents
       ((CU.2) of Math- #207 at d = 1 equals C1; the two printed forms of C1; C0 from the fold integral; I/C1; B2 prefactors)
  C2 Lemma 2.1: k_theta = 4 theta^(1/4) + (4/7) theta^(-7/4) exactly for theta = 1, 1/3, and a quadrature check
  C3 the model (3.1): polynomial identities in (X, phi); X3 and the critical values; the margins of Lemma 3.3 at rational
       phi; the decision by exact one-dimensional persistence of the quartic for 117 rational phi: elder iff |phi| < 1/3
  C4 Lemma 1.3: exact Laurent series in tau computed from the covariance, for exp(-x^2/2) and (exp(-x^2/2)+exp(-2x^2))/2
  C5 the B2 assembly: exact multivariate polynomial identities; Q/(120 l2 l4 D) = 3/4 for the Gaussian kernel
  C6 the two-point Rice integral (Decimal conditioning, float quadrature): fitted a, b against I/C0 and B2/(C0/2)
"""
import argparse
import json
import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

MUTANT = None


# ----------------------------------------------------------------------------------------------- C1: exponent bookkeeping
def factor_int(n):
    out = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


class Mono:
    """sign * prod base^exp with bases primes (int) or symbols (str) and Fraction exponents."""

    def __init__(self, sign=1, exps=None):
        self.sign = sign
        self.exps = {k: F(v) for k, v in (exps or {}).items() if F(v) != 0}

    @staticmethod
    def rat(q):
        q = F(q)
        if q == 0:
            raise ValueError('zero')
        e = {}
        for p, k in factor_int(abs(q.numerator)).items():
            e[p] = e.get(p, 0) + k
        for p, k in factor_int(q.denominator).items():
            e[p] = e.get(p, 0) - k
        return Mono(1 if q > 0 else -1, e)

    @staticmethod
    def sym(name, power=1):
        return Mono(1, {name: power})

    def __mul__(self, o):
        e = dict(self.exps)
        for k, v in o.exps.items():
            e[k] = e.get(k, 0) + v
        return Mono(self.sign*o.sign, e)

    def __pow__(self, r):
        r = F(r)
        if self.sign < 0 and r.denominator != 1:
            raise ValueError('negative base')
        return Mono(self.sign**int(r) if r.denominator == 1 else 1, {k: v*r for k, v in self.exps.items()})

    def __eq__(self, o):
        return self.sign == o.sign and self.exps == o.exps

    def __neg__(self):
        return Mono(-self.sign, self.exps)


def R(q):
    return Mono.rat(q)


def check_C1():
    two, three = R(2), R(3)
    pi = Mono.sym('pi')
    mu74 = (two**F(7, 8))*Mono.sym('G(11/8)')*(pi**F(-1, 2))          # E|Z|^{7/4}
    p12 = (R(2)*pi)**-1*Mono.sym('l2l4', F(-1, 2))                     # (2 pi)^{-1}(l2 l4)^{-1/2}
    s3, s4 = Mono.sym('s3'), Mono.sym('s4')
    common = (R(2)*pi)**F(-1, 2)*p12*(s3**-1)*(s4**F(7, 4))*mu74        # (2 pi)^{-1/2} p12 s4^{7/4} mu / s3
    k1 = F(32, 7)
    if MUTANT == 'M2':
        k1 = F(4)
    # C1 as printed: -(8/21) 24^{1/4} * common
    C1_a = -(R(F(8, 21))*R(24)**F(1, 4)*common)
    # C1 second printed form: -(2^{25/8}/7) 3^{-3/4} pi^{-2} G(11/8) s4^{7/4} s3^{-1} (l2 l4)^{-1/2}
    C1_b = -(two**F(25, 8)*R(F(1, 7))*three**F(-3, 4)*pi**-2*Mono.sym('G(11/8)')*(s4**F(7, 4))*(s3**-1)
             * Mono.sym('l2l4', F(-1, 2)))
    # (CU.2) of #207 at d = 1: -(192/7) 2^{1/4} * 2 (two points of S^0) * p12 (2 pi)^{-1/2} s3^{-1} 12^{-7/4} s4^{7/4} mu
    C1_cu = -(R(F(192, 7))*two**F(1, 4)*R(2)*p12*(R(2)*pi)**F(-1, 2)*(s3**-1)*R(12)**F(-7, 4)*(s4**F(7, 4))*mu74)
    # cusp-coefficient assembly, Proposition 2.2(d): theta-coefficient/2 = -(s4^2/48)(72/s4)^{1/4} k mu p12 p3(0)
    p30 = (R(2)*pi)**F(-1, 2)*(s3**-1)
    def cusp(k):
        return -(s4**2*R(F(1, 48))*R(72)**F(1, 4)*(s4**F(-1, 4))*R(k)*mu74*p12*p30*R(2))
    C1_cusp = cusp(F(64, 7)*1)*three**F(-1, 4)          # k_{1/3} = (64/7) 3^{-1/4}
    I_cusp = cusp(k1)
    ratio_ok = (I_cusp*(C1_cusp**-1) == three**F(1, 4)*R(F(1, 2)))
    # C0: 2 * p12 12^{-1/3} sigma3^{4/3} 2^{1/6} G(7/6) (2 pi)^{-1/2} = 2 * 72^{-1/6} G(7/6) (2 pi)^{-1/2} p12 sigma3^{4/3}
    C0_fold = R(2)*p12*R(12)**F(-1, 3)*(s3**F(4, 3))*two**F(1, 6)*Mono.sym('G(7/6)')*(R(2)*pi)**F(-1, 2)
    C0_print = R(2)*R(72)**F(-1, 6)*Mono.sym('G(7/6)')*(R(2)*pi)**F(-1, 2)*p12*(s3**F(4, 3))
    # B2 prefactors: 12^{1/3} M = 2^{1/2} 3^{1/3} G(5/6)(2 pi)^{-1/2} s3^{2/3};  B2^(2) = 12^{1/3} p12 M s4^2/(12 s3^2)
    M = two**F(-1, 6)*Mono.sym('G(5/6)')*(R(2)*pi)**F(-1, 2)*(s3**F(2, 3))
    pref_ok = (R(12)**F(1, 3)*M == two**F(1, 2)*three**F(1, 3)*Mono.sym('G(5/6)')*(R(2)*pi)**F(-1, 2)*(s3**F(2, 3)))
    FP = (R(2)*pi)**F(-1, 2)*(s3**F(-4, 3))*R(-6)*two**F(-7, 6)*Mono.sym('G(5/6)')      # int (p3 - p3(0)) a^{-4/3}
    B2b_lhs = -(s4**2*p12*R(F(1, 36))*R(12)**F(1, 3)*FP)
    B2b_rhs = R(12)**F(1, 3)*p12*M*(s4**2)*R(F(1, 12))*(s3**-2)
    checks = {
        'C1_printed_forms_agree': C1_a == C1_b,
        'CU2_at_d1_equals_C1': C1_cu == C1_a,
        'cusp_assembly_gives_C1': C1_cusp == C1_a,
        'I_over_C1_is_3^(1/4)/2': ratio_ok,
        'C0_from_fold_integral': C0_fold == C0_print,
        'B2_prefactor_2^(1/2)3^(1/3)': pref_ok,
        'B2_part2_closed_form': B2b_lhs == B2b_rhs,
    }
    return all(checks.values()), {k: v for k, v in checks.items()}


# ----------------------------------------------------------------------------------------------- C2: Mellin integrals
def zeta(theta, s):
    a = theta*s
    P_in = math.erf(a/math.sqrt(2))
    phi = math.exp(-a*a/2)/math.sqrt(2*math.pi)
    return (P_in - 2*a*phi) + s*s*(1 - P_in)


def check_C2():
    # k_theta = 4 theta^{1/4} + (4/7) theta^{-7/4}; for theta = 1/3 both terms are rational multiples of 3^{-1/4}
    k1 = F(4) + F(4, 7)
    k13_coef = F(4) + F(4, 7)*9            # 4*3^{-1/4} + (4/7)*3^{7/4} = (4 + 36/7) 3^{-1/4}
    if MUTANT == 'M2':
        k1 = F(4)
    exact = (k1 == F(32, 7)) and (k13_coef == F(64, 7))
    mu = 2**(7/8)*math.gamma(11/8)/math.sqrt(math.pi)
    # quadrature in w = log s on [-60, W], W = log(60/theta) (beyond, zeta = 1 to double precision), plus the tail 4 e^{-W/4}
    num = {}
    for label, theta, k in (('1', 1.0, float(k1)), ('1/3', 1/3, float(k13_coef)*3**-0.25)):
        n, a, b = 60000, -60.0, math.log(60/theta)
        hstep = (b - a)/n
        tot = 0.0
        for i in range(n + 1):
            w = a + i*hstep
            c = 1 if i in (0, n) else (4 if i % 2 else 2)
            tot += c*zeta(theta, math.exp(w))*math.exp(-w/4)
        tot = tot*hstep/3 + 4*math.exp(-b/4)
        num[label] = round(tot/(k*mu), 9)
    quad_ok = all(abs(v - 1) < 1e-7 for v in num.values())
    return exact and quad_ok, {'k1': str(k1), 'k_(1/3)': '%s * 3^(-1/4)' % k13_coef,
                               'quadrature_ratio_to_k_mu': num}


# ----------------------------------------------------------------------------------------------- C3: the model
def pmul(a, b):
    out = {}
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            out[(i + k, j + l)] = out.get((i + k, j + l), 0) + x*y
    return {k: v for k, v in out.items() if v != 0}


def padd(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v != 0}


def pc(c, p):
    return {k: c*v for k, v in p.items() if c*v != 0}


X = {(1, 0): F(1)}       # variables: (power of X, power of phi)
PHI = {(0, 1): F(1)}
ONE = {(0, 0): F(1)}


def lin(c0, c1):          # c0 + c1 X
    return padd({(0, 0): F(c0)}, {(1, 0): F(c1)})


def g_poly():
    xp, xm = lin(F(1, 2), 1), lin(F(-1, 2), 1)
    t1 = pc(2, pmul(pmul(xp, xp), lin(-1, 1)))
    t2 = pc(3, pmul(PHI, pmul(pmul(xp, xm), pmul(xp, xm))))
    return padd(t1, t2)


def pderiv_X(p):
    return {(i - 1, j): v*i for (i, j), v in p.items() if i > 0}


def peval(p, x, ph):
    return sum(v*F(x)**i*F(ph)**j for (i, j), v in p.items())


def gval(x, ph):
    return 2*(x + F(1, 2))**2*(x - 1) + 3*ph*(x*x - F(1, 4))**2


def decide(ph):
    """Exact 1-D persistence of the model g at M = -1/2: returns (typed&adjacent, elder)."""
    gpp_M = 6*(-1)*(1 - ph)          # g''(-1/2) = -6(1 - phi)
    gpp_S = 6*(1 + ph)
    crit = [F(-1, 2), F(1, 2)]
    if ph != 0:
        crit.append(F(-1, 1)/(2*ph))
    crit = sorted(set(crit))
    adjacent = not any(F(-1, 2) < c < F(1, 2) for c in crit)
    typed = gpp_M < 0 < gpp_S and adjacent
    vals = {c: gval(c, ph) for c in crit}
    gM, gS = vals[F(-1, 2)], vals[F(1, 2)]
    # behaviour at -inf / +inf
    if ph > 0:
        end_left, end_right = 1, 1
    elif ph < 0:
        end_left, end_right = -1, -1
    else:
        end_left, end_right = -1, 1
    iM = crit.index(F(-1, 2))

    def excursion(direction):
        mn = gM
        i = iM + direction
        while 0 <= i < len(crit):
            v = vals[crit[i]]
            if v > gM:
                return mn
            mn = min(mn, v)
            i += direction
        end = end_left if direction < 0 else end_right
        return mn if end > 0 else None      # None = -infinity
    mL, mR = excursion(-1), excursion(+1)
    vals_d = [m for m in (mL, mR) if m is not None]
    if not vals_d:
        return typed, False
    d = max(vals_d)
    return typed, typed and d == gS


def check_C3():
    g = g_poly()
    xp, xm = lin(F(1, 2), 1), lin(F(-1, 2), 1)
    f1 = pmul(pmul(xp, xp), padd(pc(2, lin(-1, 1)), pc(3, pmul(PHI, pmul(xm, xm)))))
    f2 = pmul(pmul(xm, xm), padd(pc(2, lin(1, 1)), pc(3, pmul(PHI, pmul(xp, xp)))))
    gp_expected = pc(6, pmul(pmul(xp, xm), padd(ONE, pc(2, pmul(PHI, X)))))
    ident = {
        'g = (X+1/2)^2[2(X-1) + 3 phi (X-1/2)^2]': padd(g, pc(-1, f1)) == {},
        'g + 1 = (X-1/2)^2[2(X+1) + 3 phi (X+1/2)^2]': padd(g, ONE, pc(-1, f2)) == {},
        "g' = 6(X+1/2)(X-1/2)(1 + 2 phi X)": padd(pderiv_X(g), pc(-1, gp_expected)) == {},
    }
    window = F(1, 2) if MUTANT == 'M1' else F(1, 3)
    phis = [F(k, 59) for k in range(-58, 59) if k != 0]   # 116 values in (-1, 1)
    phis.append(F(1, 1000))
    crit_ok, margin_ok, decision_ok = True, True, True
    eta = F(1, 30)
    for ph in phis:
        x3 = F(-1)/(2*ph)
        if gval(x3, ph) != (ph - 1)**3*(3*ph + 1)/(16*ph**3) or gval(x3, ph) + 1 != (ph + 1)**3*(3*ph - 1)/(16*ph**3):
            crit_ok = False
        typed, elder = decide(ph)
        if typed != (abs(ph) < 1):
            decision_ok = False
        if typed and elder != (abs(ph) < window):
            decision_ok = False
        # margins of Lemma 3.3
        if abs(ph) <= F(1, 3) - eta:
            if not (gval(F(-3, 2), ph) <= -1 - 12*eta and gval(F(3, 2), ph) >= 12*eta):
                margin_ok = False
            for i in range(0, 41):
                xl = F(-3, 2) + F(i, 40)            # [-3/2, -1/2]
                if not gval(xl, ph) <= -(xl + F(1, 2))**2:
                    margin_ok = False
                xr = F(1, 2) + F(i, 40)             # [1/2, 3/2]
                if not gval(xr, ph) + 1 >= (xr - F(1, 2))**2:
                    margin_ok = False
        if F(1, 3) + eta <= ph < 1:
            if not (F(-3, 2) < x3 < F(-1, 2) and gval(F(-2), ph) >= F(9, 16)
                    and gval(x3, ph) + 1 >= F(1, 2)*(3*ph - 1)):
                margin_ok = False
        if -1 < ph <= -F(1, 3) - eta:
            if not (F(1, 2) < x3 < F(3, 2) and gval(F(2), ph) + 1 <= -F(9, 16)
                    and gval(x3, ph) <= F(1, 2)*(3*ph + 1)):
                margin_ok = False
    # extension of (R) to 1 <= |phi| <= 6/5 (typed pairs with |phi| < 1 + eps/6)
    ext_ok = True
    for ph in (F(1), F(21, 20), F(11, 10), F(6, 5)):
        if not gval(F(-2), ph) >= F(9, 16):
            ext_ok = False
        for i in range(0, 60):
            xl = F(-2) + F(i, 40)                    # [-2, -1/2)
            if not (gval(xl, ph) >= 0 and peval(pderiv_X(g), xl, ph) < 0):
                ext_ok = False
        for i in range(1, 61):
            xr = F(1, 2) + F(i, 40)                  # (1/2, 2]
            if not gval(xr, -ph) + 1 < 0:
                ext_ok = False
    ok = all(ident.values()) and crit_ok and margin_ok and decision_ok and ext_ok
    return ok, {'identities': ident, 'critical_values_(3.1)': crit_ok, 'lemma_3.3_margins': margin_ok,
                'lemma_3.3_extension_|phi|>=1': ext_ok, 'decision_elder_iff_|phi|<1/3': decision_ok, 'n_phi': len(phis)}


# ----------------------------------------------------------------------------------------------- C4: pinned-law series
NS = 16


def smul(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            k = i + j
            if k < NS:
                out[k] = out.get(k, 0) + x*y
    return {k: v for k, v in out.items() if v != 0}


def sadd(a, b, cb=1):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + cb*v
    return {k: v for k, v in out.items() if v != 0}


def sscale(a, c):
    return {k: c*v for k, v in a.items() if c*v != 0}


def sinv(a):
    m = min(a)
    a0 = a[m]
    u = {k - m: v/a0 for k, v in a.items() if k != m}
    out, term = {0: F(1)}, {0: F(1)}
    for _ in range(NS + 8):
        term = smul(term, sscale(u, -1))
        if not term:
            break
        out = sadd(out, term)
    return {k - m: v/a0 for k, v in out.items() if k - m < NS}


def rho_der_series(rc, n, d):
    """Series in tau of rho^{(n)}(x) at x = d * 2 tau, d in {-1, 0, 1}; rho(x) = sum_k rc[k] x^{2k}."""
    out = {}
    for k, r in enumerate(rc):
        p = 2*k - n
        if p < 0:
            continue
        c = r*F(math.factorial(2*k), math.factorial(p))
        if d == 0:
            if p == 0:
                out[0] = out.get(0, 0) + c
        elif p < NS:
            out[p] = out.get(p, 0) + c*F(2*d)**p
    return {k: v for k, v in out.items() if v != 0}


def pinned_series(rc):
    pts = [(1, -1), (1, 1), (0, -1), (0, 1), (2, -1), (2, 1)]    # f'(-t/2), f'(t/2), f(-t/2), f(t/2), f''(-t/2), f''(t/2)

    def cov(a, b):
        (i, si), (j, sj) = pts[a], pts[b]
        return sscale(rho_der_series(rc, i + j, (si - sj)//2), (-1)**j)
    C = [[cov(a, b) for b in range(6)] for a in range(6)]
    ti, ti2, ti3 = {-1: F(1, 2)}, {-2: F(1, 4)}, {-3: F(1, 8)}
    U1 = {0: {0: F(1, 2)}, 1: {0: F(1, 2)}}
    U2 = {0: sscale(ti, -1), 1: ti}
    U3 = {0: sscale(ti2, 6), 1: sscale(ti2, 6), 2: sscale(ti3, 12), 3: sscale(ti3, -12)}
    O = {4: {0: F(-1, 2)}, 5: {0: F(1, 2)}}
    E1 = {4: {0: F(1, 2)}, 5: {0: F(1, 2)}}

    def V(A, B):
        out = {}
        for a, ca in A.items():
            for b, cb in B.items():
                out = sadd(out, smul(smul(ca, cb), C[a][b]))
        return out
    zero_blocks = all(not V(A, B) for A, B in ((U1, U2), (U2, U3), (O, U2), (E1, U1), (E1, U3), (O, E1)))
    v11, v13, v33, v22 = V(U1, U1), V(U1, U3), V(U3, U3), V(U2, U2)
    det2 = sadd(smul(v11, v33), smul(v13, v13), -1)
    idet = sinv(det2)
    o1, o3 = V(O, U1), V(O, U3)
    b3 = smul(sadd(smul(o3, v11), smul(o1, v13), -1), idet)
    b1 = smul(sadd(smul(o1, v33), smul(o3, v13), -1), idet)
    e2 = V(E1, U2)
    return {'zero_blocks': zero_blocks, 'det': smul(det2, v22), 'inv33': smul(v11, idet), 'c': b3,
            'v1': sadd(V(E1, E1), smul(smul(e2, e2), sinv(v22)), -1),
            'v2': sadd(V(O, O), sadd(smul(b1, o1), smul(b3, o3)), -1)}


def kernels():
    K = 14
    gauss = [F((-1)**k, 2**k*math.factorial(k)) for k in range(K)]
    mix = [(F((-1)**k, 2**k*math.factorial(k)) + F((-2)**k, math.factorial(k)))/2 for k in range(K)]
    return {'exp(-x^2/2)': gauss, '(exp(-x^2/2)+exp(-2x^2))/2': mix}


def lambdas(rc):
    return {2*j: (-1)**j*rc[j]*math.factorial(2*j) for j in range(1, 7)}


def formulas(lam):
    l2, l4, l6, l8, l10 = (lam[i] for i in (2, 4, 6, 8, 10))
    Dd = l2*l6 - l4**2
    c2 = -(l2*l8 - l4*l6)/(15*Dd)
    if MUTANT == 'M3':
        c2 = -c2
    return {'D': Dd, 'c2': c2,
            'd2': (8*l4**2*l6 - 3*l2*l4*l8 - 5*l2*l6**2)/(15*l4*Dd),
            'q2': (l2**2*l8 - 6*l2*l4*l6 + 5*l4**3)/(5*l2*Dd),
            'v1_4': (l8 - l6**2/l4)/9,
            'v2_6': (l10 - (l6**3 - 2*l4*l6*l8 + l2*l8**2)/Dd)/225}


def check_C4():
    info, ok = {}, True
    for name, rc in kernels().items():
        lam = lambdas(rc)
        fm = formulas(lam)
        s = pinned_series(rc)
        l2, l4 = lam[2], lam[4]
        Dd = fm['D']
        parity = (all(k % 2 == 0 for k in s['det']) and all(k % 2 == 0 for k in s['inv33'])
                  and all(k % 2 == 1 for k in s['c']) and all(k % 2 == 0 for k in s['v1']) and all(k % 2 == 0 for k in s['v2']))
        res = {
            'zero_blocks': s['zero_blocks'],
            'parity': parity,
            'c = tau(1 + c2 tau^2 + ...)': s['c'].get(1) == 1 and s['c'].get(3) == fm['c2'],
            'det = l4 D (1 + d2 tau^2 + ...)': s['det'].get(0) == l4*Dd and s['det'].get(2) == l4*Dd*fm['d2'],
            'inv33 = (l2/D)(1 + q2 tau^2 + ...)': s['inv33'].get(0) == l2/Dd and s['inv33'].get(2) == l2/Dd*fm['q2'],
            'v1 = sigma4^2 tau^4/9 + ...': min(s['v1']) == 4 and s['v1'][4] == fm['v1_4'],
            'v2 = (tau^6/225) Var(a5|a1,a3) + ...': min(s['v2']) == 6 and s['v2'][6] == fm['v2_6'],
        }
        ok = ok and all(res.values())
        info[name] = {'checks': res, 'lambda': {str(k): str(v) for k, v in lam.items()},
                      'c2': str(fm['c2']), 'd2': str(fm['d2']), 'q2': str(fm['q2'])}
    return ok, info


# ----------------------------------------------------------------------------------------------- C5: B2 assembly
VARS = ('l2', 'l4', 'l6', 'l8')


def mono(**kw):
    return {tuple(kw.get(v, 0) for v in VARS): F(1)}


def mpoly_mul(a, b):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            k = tuple(x + y for x, y in zip(ka, kb))
            out[k] = out.get(k, 0) + va*vb
    return {k: v for k, v in out.items() if v != 0}


def mpoly_add(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v != 0}


def mpc(c, p):
    return {k: c*v for k, v in p.items() if c*v != 0}


def check_C5():
    l2, l4, l6, l8 = (mono(**{v: 1}) for v in VARS)
    D = mpoly_add(mpoly_mul(l2, l6), mpc(-1, mpoly_mul(l4, l4)))
    sgn = -1 if MUTANT == 'M3' else 1
    # 30 l2 l4 D * 2 c2      = -4 l2 l4 (l2 l8 - l4 l6)
    t_c = mpc(-4*sgn, mpoly_mul(mpoly_mul(l2, l4), mpoly_add(mpoly_mul(l2, l8), mpc(-1, mpoly_mul(l4, l6)))))
    # 30 l2 l4 D * (-d2/2)  = -l2 (8 l4^2 l6 - 3 l2 l4 l8 - 5 l2 l6^2)
    t_d = mpc(-1, mpoly_mul(l2, mpoly_add(mpc(8, mpoly_mul(mpoly_mul(l4, l4), l6)), mpc(-3, mpoly_mul(mpoly_mul(l2, l4), l8)),
                                          mpc(-5, mpoly_mul(mpoly_mul(l2, l6), l6)))))
    # 30 l2 l4 D * (-5 q2/6) = -5 l4 (l2^2 l8 - 6 l2 l4 l6 + 5 l4^3)
    t_q = mpc(-5, mpoly_mul(l4, mpoly_add(mpoly_mul(mpoly_mul(l2, l2), l8), mpc(-6, mpoly_mul(mpoly_mul(l2, l4), l6)),
                                          mpc(5, mpoly_mul(mpoly_mul(l4, l4), l4)))))
    lhs1 = mpoly_add(t_c, t_d, t_q)
    rhs1 = mpoly_add(mpc(-6, mono(l2=2, l4=1, l8=1)), mpc(26, mono(l2=1, l4=2, l6=1)), mpc(5, mono(l2=2, l6=2)),
                     mpc(-25, mono(l4=4)))
    # 120 l2 l4 D * s4^2/(12 s3^2) = 10 l2^2 (l4 l8 - l6^2)
    t_s = mpc(10, mpoly_mul(mpoly_mul(l2, l2), mpoly_add(mpoly_mul(l4, l8), mpc(-1, mpoly_mul(l6, l6)))))
    c26 = 25 if MUTANT == 'M4' else 26
    Q = mpoly_add(mpc(4, mono(l2=2, l4=1, l8=1)), mpc(c26, mono(l2=1, l4=2, l6=1)), mpc(-5, mono(l2=2, l6=2)),
                  mpc(-25, mono(l4=4)))
    id1 = mpoly_add(lhs1, mpc(-1, rhs1)) == {}
    id2 = mpoly_add(lhs1, t_s, mpc(-1, Q)) == {}
    # individual coefficient formulas against the exact rational values of C4 (Gaussian kernel and mixture)
    vals = {}
    for name, rc in kernels().items():
        lam = lambdas(rc)
        fm = formulas(lam)
        L2, L4, L6, L8 = (lam[i] for i in (2, 4, 6, 8))
        Dd = fm['D']
        s3sq, s4sq = Dd/L2, L8 - L6**2/L4
        bracket = (2*fm['c2'] - fm['d2']/2 - 5*fm['q2']/6)/4 + s4sq/(12*s3sq)
        Qv = 4*L2**2*L4*L8 + c26*L2*L4**2*L6 - 5*L2**2*L6**2 - 25*L4**4
        vals[name] = {'bracket': str(bracket), 'Q/(120 l2 l4 D)': str(Qv/(120*L2*L4*Dd)),
                      'agree': bracket == Qv/(120*L2*L4*Dd)}
    gauss_34 = vals['exp(-x^2/2)']['Q/(120 l2 l4 D)'] == '3/4'
    ok = id1 and id2 and gauss_34 and all(v['agree'] for v in vals.values())
    return ok, {'identity_30l2l4D(2c2-d2/2-5q2/6)': id1, 'identity_sum_equals_Q': id2, 'values': vals,
                'gauss_Q_over_120l2l4D_is_3/4': gauss_34}


# ----------------------------------------------------------------------------------------------- C6: two-point Rice
getcontext().prec = 60
D_ = Decimal


def He(n, x):
    h0, h1 = D_(1), x
    if n == 0:
        return h0
    for k in range(1, n):
        h0, h1 = h1, x*h1 - k*h0
    return h1


def rder(kernel, n, x):
    g = (-1)**n*He(n, x)*(-(x*x)/2).exp()
    if kernel == 'gauss':
        return g
    return (g + (-1)**n*D_(2)**n*He(n, 2*x)*(-2*x*x).exp())/2


def solve(M, b):
    n = len(M)
    A = [M[i][:] + [b[i]] for i in range(n)]
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[p] = A[p], A[i]
        for r in range(n):
            if r != i:
                f = A[r][i]/A[i][i]
                A[r] = [x - f*y for x, y in zip(A[r], A[i])]
    return [A[i][n]/A[i][i] for i in range(n)]


def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2] - M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2] - M[1][2]*M[2][0])
            + M[0][2]*(M[1][0]*M[2][1] - M[1][1]*M[2][0]))


def gauss_legendre(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi*(i - 0.25)/(n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2*k - 1)*x*p1 - (k - 1)*p0)/k
            dp = n*(x*p1 - p0)/(x*x - 1)
            dx = p1/dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(x)
        ws.append(2/((1 - x*x)*dp*dp))
    return xs, ws


GX, GW = gauss_legendre(20)
XO, WO = gauss_legendre(24)


def Phi(x):
    return 0.5*math.erfc(-x/math.sqrt(2))


def phi_(x):
    return math.exp(-x*x/2)/math.sqrt(2*math.pi)


def Epos(mx, my, sx, sy, rho):
    """E[X^+ Y^+] for (X, Y) ~ N((mx, my), [[sx^2, rho sx sy], [., sy^2]]) (closed form when both means are far)."""
    a, b = mx/sx, my/sy
    if a > 30 and b > 30:
        return sx*sy*(a*b + rho)
    if a < -30 or b < -30:
        return 0.0
    s = sy*math.sqrt(max(1 - rho*rho, 0.0))
    beta = rho*sy/sx
    lo, hi = max(0.0, mx - 13*sx), mx + 13*sx
    if hi <= 0:
        return 0.0
    cuts = {lo, hi}
    cuts.update(mx + k*sx for k in range(-12, 13) if lo < mx + k*sx < hi)
    if beta != 0:
        xk = mx - my/beta
        if lo < xk < hi:
            cuts.add(xk)
            wk = s/abs(beta)
            for j in (0.5, 1, 2, 4, 8, 16, 32, 64):
                for sg in (-1, 1):
                    if lo < xk + sg*j*wk < hi:
                        cuts.add(xk + sg*j*wk)
    cuts = sorted(cuts)
    tot = 0.0
    for u, v in zip(cuts[:-1], cuts[1:]):
        for x, w in zip(GX, GW):
            xx = u + (v - u)*(x + 1)/2
            m2 = my + beta*(xx - mx)
            inner = m2*Phi(m2/s) + s*phi_(m2/s) if s > 0 else max(m2, 0.0)
            tot += w*(v - u)/2*xx*phi_((xx - mx)/sx)/sx*inner
    return tot


def g_rice(kernel, t, h):
    t, h, z = D_(repr(t)), D_(repr(h)), D_(0)
    pts = [(0, z), (1, z), (2, z), (0, t), (1, t), (2, t)]
    C = [[(-1)**j*rder(kernel, i + j, si - sj) for (j, sj) in pts] for (i, si) in pts]
    U = [[z, D_('0.5'), z, z, D_('0.5'), z], [z, -1/t, z, z, 1/t, z], [12/t**3, 6/t**2, z, -12/t**3, 6/t**2, z]]
    T = [[z, z, -1, z, z, z], [z, z, z, z, z, D_(1)]]

    def cv(a, b):
        return sum(a[i]*C[i][j]*b[j] for i in range(6) for j in range(6) if a[i] and b[j])
    CUU = [[cv(a, b) for b in U] for a in U]
    u = [z, z, 12*h/t**3]
    x = solve(CUU, u)
    y = [solve(CUU, [cv(Tk, a) for a in U]) for Tk in T]
    m = [sum(cv(Tk, U[k])*x[k] for k in range(3)) for Tk in T]
    S = [[cv(T[i], T[j]) - sum(cv(T[i], U[k])*y[j][k] for k in range(3)) for j in range(2)] for i in range(2)]
    q = sum(u[k]*x[k] for k in range(3))
    pU = float((-q/2).exp()/((2*D_(math.pi))**3*det3(CUU)).sqrt())
    sx, sy = float(S[0][0].sqrt()), float(S[1][1].sqrt())
    rho = float(S[0][1]/(S[0][0]*S[1][1]).sqrt())
    jac = 1.0 if MUTANT == 'M5' else 12.0
    return pU*jac/float(t)**4*Epos(float(m[0]), float(m[1]), sx, sy, rho)


def rice_F(kernel, h, t0, sig3):
    lh = math.log(h)
    main = [math.log(12*h/(m*sig3))/3 for m in (40, 20, 10, 6, 4, 2.5, 1.5, 1, 0.5, 0.25)]
    cuts = sorted(c for c in main + [lh/4 - 1, lh/4 - 0.5, lh/4, lh/4 + 0.5, lh/4 + 1, lh/4 + 2, math.log(t0)]
                  if c <= math.log(t0))
    tot = 0.0
    for a, b in zip(cuts[:-1], cuts[1:]):
        for x, w in zip(XO, WO):
            ww = a + (b - a)*(x + 1)/2
            tt = math.exp(ww)
            tot += w*(b - a)/2*tt*g_rice(kernel, tt, h)
    return tot


def lstsq3(rows, ys):
    A = [[sum(r[i]*r[j] for r in rows) for j in range(3)] for i in range(3)]
    b = [sum(r[i]*y for r, y in zip(rows, ys)) for i in range(3)]
    M = [A[i][:] + [b[i]] for i in range(3)]
    for i in range(3):
        p = max(range(i, 3), key=lambda r: abs(M[r][i]))
        M[i], M[p] = M[p], M[i]
        for r in range(3):
            if r != i:
                f = M[r][i]/M[i][i]
                M[r] = [x - f*y for x, y in zip(M[r], M[i])]
    return [M[i][3]/M[i][i] for i in range(3)]


def constants_float(lam):
    l2, l4, l6, l8 = (float(lam[i]) for i in (2, 4, 6, 8))
    Dd = l2*l6 - l4**2
    s3, s4 = math.sqrt(Dd/l2), math.sqrt(l8 - l6**2/l4)
    p12 = 1/(2*math.pi*math.sqrt(l2*l4))
    C0 = 2*72**(-1/6)*math.gamma(7/6)*(2*math.pi)**-0.5*p12*s3**(4/3)
    mu = 2**(7/8)*math.gamma(11/8)/math.sqrt(math.pi)
    C1 = -(8/21)*24**0.25*mu*(2*math.pi)**-0.5*p12*s4**1.75/s3
    Icand = 3**0.25/2*C1
    Q = 4*l2**2*l4*l8 + 26*l2*l4**2*l6 - 5*l2**2*l6**2 - 25*l4**4
    B2 = 2**0.5*3**(1/3)*math.gamma(5/6)*(2*math.pi)**-0.5*p12*s3**(2/3)*Q/(120*l2*l4*Dd)
    return {'C0': C0, 'C1': C1, 'I': Icand, 'B2': B2, 'sigma3': s3}


def check_C6():
    out, ok = {}, True
    ks = kernels()
    for kname, kernel, t0 in (('exp(-x^2/2)', 'gauss', 0.04), ('(exp(-x^2/2)+exp(-2x^2))/2', 'mix', 0.01)):
        cst = constants_float(lambdas(ks[kname]))
        a_pred, b_pred = cst['I']/cst['C0'], cst['B2']/(cst['C0']/2)
        rows, ys, pts = [], [], {}
        for e in (11, 12, 13, 14, 15, 16):
            h = 10.0**(-e)
            dev = h**(1/3)*rice_F(kernel, h, t0, cst['sigma3'])/(cst['C0']/2) - 1
            y = dev/h**(7/12)
            rows.append([1.0, h**(1/12), h**-0.25])
            ys.append(y)
            pts['1e-%d' % e] = float('%.6f' % y)
        fa, fb, fr = lstsq3(rows, ys)
        good = abs(fa - a_pred) < 2e-4 and abs(fb - b_pred) < 3e-3
        ok = ok and good
        out[kname] = {'t0': t0, 'C0': float('%.8f' % cst['C0']), 'C1': float('%.8f' % cst['C1']),
                      'I': float('%.8f' % cst['I']), 'B2': float('%.8f' % cst['B2']),
                      'a_pred_I/C0': float('%.7f' % a_pred), 'b_pred_B2/(C0/2)': float('%.7f' % b_pred),
                      'dev/h^(7/12)': pts, 'fit_a': float('%.4f' % fa), 'fit_b': float('%.3f' % fb), 'within_tolerance': good}
    return ok, out


# ----------------------------------------------------------------------------------------------- main
def main():
    global MUTANT
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', default=None)
    args = ap.parse_args()
    if args.mutant is not None and args.mutant not in ('M1', 'M2', 'M3', 'M4', 'M5'):
        sys.stderr.write('unknown mutant label\n')
        return 2
    MUTANT = args.mutant
    results = {}
    for name, fn in (('C1_constants', check_C1), ('C2_mellin', check_C2), ('C3_model_window', check_C3),
                     ('C4_pinned_series', check_C4), ('C5_B2_assembly', check_C5), ('C6_rice_integral', check_C6)):
        ok, info = fn()
        results[name] = {'passed': bool(ok), 'info': info}
    out = {'object': 'CL-D1-THIRD-ORDER-20261001-v1 exact controls', 'scientific_effect': 'NONE',
           'mutant': MUTANT, 'passed': all(r['passed'] for r in results.values()), 'checks': results}
    sys.stdout.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
    return 0 if out['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
