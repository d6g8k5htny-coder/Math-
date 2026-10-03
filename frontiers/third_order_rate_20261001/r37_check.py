#!/usr/bin/env python3
"""Exact controls for CL-THIRD-ORDER-RATE-20261001-v1 (frontiers/third_order_rate_20261001/PROOF.md).
Standard library only, exact rationals. Run: python3 -B -S r37_check.py   (and with -O; output byte-identical).
Mutants: --mutant M1|...|M8 must exit 1; an unknown label exits 2.

  R1 the exponent ledger of section 5 with rho_f = l^(2/7), rho_c = l^(2/9), a = l^(1/9). An error r^p kappa^q
     (kappa = l r^-4) on [rho_f, rho_c] integrates to l^q r^(p-4q+1) at the endpoint that dominates. Candidate: least
     exponent 3/7, attained exactly by rho_f^5/l (twice: Lemma F's layer and Lemma O's tail) and l rho_f^-2 (twice: the
     finite part and Lemma C+'s linear term). Elder: least 3/7, attained exactly by the same four terms, the rejected fold
     mass rho_f^5/l, and Lemma CE+'s l^2 rho_f^-11/2 and l^3 rho_f^-9. Every other term is >= 4/9, and the intermediate
     separations give exactly 4/9 (log). The hypotheses l^(1/3) < rho_f < l^(1/4) < rho_c < a and kappa <= 1 on
     [rho_c, r0*] hold. Optimality: 2/7, 2/9 and 1/9 maximize the respective minima over rational grids. Regression:
     #218's error r(1 + kappa)^2 at rho_f = l^(3/11) gives 4/11 (its T1), and #198 (W.1) with a = l^(2/15) gives 2/5
     on the intermediate separations (#220 X1). Remark 1's max-min over rho_f: without the rho_f^5/l family both
     densities reach 4/9; without only the linear pair (l rho_f^-2) the candidate reaches 4/9 and the elder stays 3/7.
  R2 Lemma L: |(c^2 - y^2)_+ - (c^2 - y'^2)_+| <= |y - y'| (|y| + |y'|) on random and edge rational instances, with
     equality instances; the old constant 2c also holds, and the new bound is smaller by a factor <= 1/100 on some
     instances with a nonzero difference.
  R3 the refined B_4 estimate (Lemma CE+, Step E2+): if A <= -lam I, |q| <= |gamma|^2/lam and
     |f4 - 3q| = 72 kappa |phi| with 1/6 <= |phi| <= 1/2, then |f4| >= 6 kappa or lam <= |gamma|^2/(2 kappa); on scalar
     instances and on matrix instances A = -O diag(mu) O^T (m = 1, 2, 3; O rational orthogonal by the Cayley
     transform), where q = gamma^T A^-1 gamma and |q| <= |gamma|^2/min(mu) are exact; and eps* <= kappa/4 with
     ||phi| - 1/3| <= 2 eps*/(3 kappa) puts |phi| in [1/6, 1/2].
  R4 Proposition W+: the typed sign pattern (-6kD + rY + R_M)(6kD + rY + R_S) < 0 forces |rY| <= 6k|D| + max|R_i| and
     |det K_M det K_S| <= r^2 (12 kappa |D| + 2 eta)^2, eta = max|R_i|/r; the f4-window
     {|(f4/12) D + c0| <= 6 kappa |D| + eta} has length exactly 144 kappa + 24 eta/|D|; and the splitting inequality
     (x + y)^2 min(1, a + b) <= 2 (x^2 + y^2)(a + min(1, b)) for x, y, a, b >= 0.
  R5 Proposition W+ bookkeeping: kappa^3 + kappa^2 r + kappa r^2 + r^3 L <= (kappa + r)^2 (kappa + r L)
     <= (1 + L)(kappa + r)^3 for L >= 0, and (kappa + r)^3 <= 4 (kappa^3 + r^3).
  R6 Lemma C+/CE+ bookkeeping, with r = s^2, kappa = t^2, kappa r <= 1, r <= 1: kappa^2 min(1, kappa) r^3 <= r;
     kappa^(1/2) min(1, kappa) r^(3/2) <= r; r^2 (1 + kappa)^2 <= 2 r (1 + kappa); kappa^2 r^2 <= kappa r; and the
     new elder error is <= the old one: kappa^2 r^(3/2) + kappa^3 r^2 <= 2 kappa^2 r.
"""
import argparse
import json
import random
import sys
from fractions import Fraction as Fr

MUTANT = None


def cusp_integral_exponent(p, q, ef, ec):
    """l^q r^(p-4q+1) at the dominating endpoint of [rho_f, rho_c] (rho_f = l^ef, rho_c = l^ec); g = 0 is a log."""
    g = p - 4 * q + 1
    if g < 0:
        return q + ef * g, 'rho_f'
    if g > 0:
        return q + ec * g, 'rho_c'
    return q, 'log'


# ----------------------------------------------------------------------------------------------- R1 exponents
def ledger(ef, ec, ea, cand_forms, eld_forms):
    one = Fr(1)
    cand = {'F: rho_f^2': 2 * ef, 'F: rho_f^5/l (Lemma F layer)': 5 * ef - one,
            'F: l rho_f^-2 (finite part)': one - 2 * ef,
            'K: rho_f^5/l (Lemma O tail)': 5 * ef - one, 'K: l^2 rho_c^-7 (upper tail)': 2 - 7 * ec,
            'J2: rho_c^3': 3 * ec, 'J3: l^2 rho_c^-7': 2 - 7 * ec, 'J3: l rho_c^-2': one - 2 * ec,
            'J4: l^2 rho_c^-7': 2 - 7 * ec, 'J5: l': one}
    for (p, q) in cand_forms:
        e, _ = cusp_integral_exponent(p, q, ef, ec)
        cand['K: Lemma C+ r^%s kappa^%s' % (p, q)] = e
    eld = {'F: rho_f^2': 2 * ef, 'F: rho_f^5/l (Lemma F layer)': 5 * ef - one,
           'F: l rho_f^-2 (finite part)': one - 2 * ef, 'F: rho_f^5/l (rejected fold mass, [C7-K] (K2))': 5 * ef - one,
           'K: rho_f^5/l (Lemma O/O\' tail)': 5 * ef - one, 'K: l^2 rho_c^-7 (upper tail)': 2 - 7 * ec,
           'J4: l^2 rho_c^-7': 2 - 7 * ec,
           'I: [rho_c,a] l^3 rho_c^-11 (log)': 3 - 11 * ec, 'I: [rho_c,a] a^4 (log)': 4 * ea,
           'I: [a,r0*] l^(5/3) a^-7': Fr(5, 3) - 7 * ea, 'I: [a,r0*] l^(2/3) a^-2': Fr(2, 3) - 2 * ea,
           'far: #187 Theorem F': Fr(2, 3)}
    for (p, q) in eld_forms:
        e, _ = cusp_integral_exponent(p, q, ef, ec)
        eld['K: Lemma CE+ r^%s kappa^%s' % (p, q)] = e
    return cand, eld


def r1():
    ef = Fr(3, 11) if MUTANT == 'M1' else Fr(2, 7)
    ec = Fr(1, 4) if MUTANT == 'M8' else Fr(2, 9)
    ea = Fr(2, 15) if MUTANT == 'M6' else Fr(1, 9)
    cand_forms = [(Fr(1), Fr(0)), (Fr(1), Fr(2) if MUTANT == 'M2' else Fr(1))]
    eld_forms = [(Fr(1), Fr(0)), (Fr(1), Fr(1)), (Fr(3, 2), Fr(2)), (Fr(2), Fr(3))]
    cand, eld = ledger(ef, ec, ea, cand_forms, eld_forms)
    target = Fr(3, 7)
    ok = min(cand.values()) == target and min(eld.values()) == target
    want_c = sorted(['F: rho_f^5/l (Lemma F layer)', 'F: l rho_f^-2 (finite part)', 'K: rho_f^5/l (Lemma O tail)',
                     'K: Lemma C+ r^1 kappa^1'])
    want_e = sorted(['F: rho_f^5/l (Lemma F layer)', 'F: l rho_f^-2 (finite part)',
                     'F: rho_f^5/l (rejected fold mass, [C7-K] (K2))', 'K: rho_f^5/l (Lemma O/O\' tail)',
                     'K: Lemma CE+ r^1 kappa^1', 'K: Lemma CE+ r^3/2 kappa^2', 'K: Lemma CE+ r^2 kappa^3'])
    ok &= sorted(k for k, v in cand.items() if v == target) == want_c
    ok &= sorted(k for k, v in eld.items() if v == target) == want_e
    ok &= all(v >= Fr(4, 9) for k, v in cand.items() if v != target)
    ok &= all(v >= Fr(4, 9) for k, v in eld.items() if v != target)
    inter = [v for k, v in eld.items() if k.startswith('I:')]
    ok &= min(inter) == Fr(4, 9)
    # hypotheses: l^(1/3) < rho_f < l^(1/4) < rho_c < a < 1 (exponents reversed); kappa <= 1 on [rho_c, r0*]
    q = Fr(1, 4)
    hyp = Fr(1, 3) > ef > q > ec > ea > 0 and 1 - 4 * ec >= 0 and 1 - 4 * ea >= 0 and 1 - 3 * ef >= 0
    ok &= hyp
    # optimality on rational grids: rho_f, rho_c and a maximize the minima of the terms that depend on them
    grid = sorted({Fr(i, n) for n in range(2, 241) for i in range(1, n)})
    fdep = lambda f: min(5 * f - 1, 1 - 2 * f, cusp_integral_exponent(Fr(3, 2), Fr(2), f, ec)[0],
                         cusp_integral_exponent(Fr(2), Fr(3), f, ec)[0])
    fbest = max((g for g in grid if q < g < Fr(1, 3)), key=fdep)
    cbest = max((g for g in grid if Fr(1, 9) < g < q), key=lambda c: min(2 * c, 2 - 7 * c, 3 - 11 * c))
    abest = max((g for g in grid if 0 < g < Fr(2, 9)), key=lambda a: min(4 * a, Fr(2, 3) - 2 * a))
    ok &= fbest == Fr(2, 7) and fdep(fbest) == target and cbest == Fr(2, 9) and abest == Fr(1, 9)
    # regression: #218 (error r(1 + kappa)^2, rho_f = l^(3/11)) and #220's intermediate split (W.1, a = l^(2/15))
    old_c, _ = ledger(Fr(3, 11), Fr(2, 9), Fr(1, 9), [(Fr(1), Fr(0)), (Fr(1), Fr(1)), (Fr(1), Fr(2))], [])
    reg218 = min(old_c.values())
    reg220 = min(2 - 7 * Fr(2, 9), 3 * Fr(2, 15), Fr(5, 3) - 7 * Fr(2, 15), Fr(2, 3) - 2 * Fr(2, 15))
    ok &= reg218 == Fr(4, 11) and reg220 == Fr(2, 5)
    # the old linear-in-kappa^2 term at the new split would be l^(2/7): the improvement of Lemma C+ is needed
    ok &= cusp_integral_exponent(Fr(1), Fr(2), Fr(2, 7), Fr(2, 9))[0] == Fr(2, 7)
    # Remark 1: max over rho_f = l^f (1/4 < f < 1/3, rational grid) of the least exponent, with a family removed
    def best(drop, elder):
        vals = []
        for f in (g for g in grid if q < g < Fr(1, 3)):
            c_, e_ = ledger(f, Fr(2, 9), Fr(1, 9), cand_forms, eld_forms)
            terms = e_ if elder else c_
            keep = [v for k, v in terms.items() if not any(dd in k for dd in drop)]
            vals.append(min(keep))
        return max(vals)
    layer = ('rho_f^5/l',)
    linear = ('l rho_f^-2', 'r^1 kappa^1')
    pair = {'drop_layer_cand': best(layer, False), 'drop_layer_eld': best(layer, True),
            'drop_linear_cand': best(linear, False), 'drop_linear_eld': best(linear, True)}
    ok &= pair == {'drop_layer_cand': Fr(4, 9), 'drop_layer_eld': Fr(4, 9), 'drop_linear_cand': Fr(4, 9),
                   'drop_linear_eld': Fr(3, 7)}
    return {'rho_f': 'l^' + str(ef), 'rho_c': 'l^' + str(ec), 'a': 'l^' + str(ea),
            'candidate_least': str(min(cand.values())), 'elder_least': str(min(eld.values())),
            'intermediate_least': str(min(inter)), 'hypotheses': bool(hyp),
            'regression_218': str(reg218), 'regression_220_intermediate': str(reg220),
            'remark1_maxmin': {k: str(v) for k, v in sorted(pair.items())},
            'candidate_terms': {k: str(v) for k, v in sorted(cand.items())},
            'elder_terms': {k: str(v) for k, v in sorted(eld.items())}, 'passed': bool(ok)}


# ----------------------------------------------------------------------------------------------- R2 Lemma L
def wplus(c, y):
    v = c * c - y * y
    return v if v > 0 else Fr(0)


def r2(rng):
    ok = True
    eq = small = 0
    insts = []
    for _ in range(6000):
        c = Fr(rng.randint(0, 60), rng.randint(1, 12))
        y = Fr(rng.randint(-90, 90), rng.randint(1, 12))
        yp = Fr(rng.randint(-90, 90), rng.randint(1, 12))
        insts.append((c, y, yp))
    for c in (Fr(0), Fr(1), Fr(7, 3)):
        for y in (-c, c, Fr(0), c / 2, -c / 2, 2 * c + 1):
            for yp in (-c, c, Fr(0), c / 3, 3 * c, -3 * c - 1):
                insts.append((c, y, yp))
    for (c, y, yp) in insts:
        lhs = abs(wplus(c, y) - wplus(c, yp))
        fac = max(abs(y), abs(yp)) if MUTANT == 'M3' else abs(y) + abs(yp)
        rhs = abs(y - yp) * fac
        ok &= lhs <= rhs
        ok &= lhs <= 2 * c * abs(y - yp)                      # the old constant, also valid
        if lhs == rhs and lhs > 0:
            eq += 1
        if lhs > 0 and 100 * rhs <= 2 * c * abs(y - yp):
            small += 1
    ok &= eq > 0 and small > 0
    return {'instances': len(insts), 'equality_instances': eq, 'improvement_factor_le_1/100_instances': small,
            'passed': bool(ok)}


# ----------------------------------------------------------------------------------------------- R3 refined B_4
def matmul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))] for i in range(len(X))]


def inverse(X):
    n = len(X)
    M = [list(X[i]) + [Fr(int(i == j)) for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = next(i for i in range(col, n) if M[i][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [v / pv for v in M[col]]
        for i in range(n):
            if i != col and M[i][col] != 0:
                fac = M[i][col]
                M[i] = [a - fac * b for a, b in zip(M[i], M[col])]
    return [row[n:] for row in M]


def cayley(K):
    n = len(K)
    I = [[Fr(int(i == j)) for j in range(n)] for i in range(n)]
    return matmul([[I[i][j] - K[i][j] for j in range(n)] for i in range(n)],
                  inverse([[I[i][j] + K[i][j] for j in range(n)] for i in range(n)]))


def r3(rng):
    ok = True
    insts = []
    for _ in range(4000):
        kap = Fr(rng.randint(1, 400), rng.randint(1, 20))
        lam = Fr(rng.randint(1, 300), rng.randint(1, 30))
        g2 = Fr(rng.randint(0, 900), rng.randint(1, 30))           # |gamma|^2
        q = (g2 / lam) * Fr(rng.randint(-1000, 1000), 1000)        # |q| <= |gamma|^2 / lam
        phi = Fr(rng.choice((-1, 1))) * (Fr(1, 6) + Fr(rng.randint(0, 600), 1800))   # 1/6 <= |phi| <= 1/2
        insts.append((kap, lam, g2, q, phi))
    insts.append((Fr(1), Fr(1), Fr(1), Fr(1, 2), Fr(-1, 6)))      # |f4| = 21/2: separates 6 kappa from 12 kappa
    nmat = second = 0
    for m in (1, 2, 3):                                              # matrix instances: A = -O diag(mu) O^T
        for _ in range(300):
            K = [[Fr(0)] * m for _ in range(m)]
            for i in range(m):
                for j in range(i + 1, m):
                    v = Fr(rng.randint(-9, 9), rng.randint(1, 5))
                    K[i][j], K[j][i] = v, -v
            O = cayley(K)
            mu = [Fr(rng.randint(1, 400), rng.randint(1, 40)) for _ in range(m)]
            gam = [Fr(rng.randint(-60, 60), rng.randint(1, 6)) for _ in range(m)]
            Og = [sum(O[i][j] * gam[i] for i in range(m)) for j in range(m)]          # O^T gamma
            q = -sum(Og[j] * Og[j] / mu[j] for j in range(m))                         # gamma^T A^-1 gamma
            Ainv = [[-sum(O[i][l] * O[j][l] / mu[l] for l in range(m)) for j in range(m)] for i in range(m)]
            ok &= q == sum(gam[i] * Ainv[i][j] * gam[j] for i in range(m) for j in range(m))
            A = [[-sum(O[i][l] * O[j][l] * mu[l] for l in range(m)) for j in range(m)] for i in range(m)]
            ok &= matmul(A, Ainv) == [[Fr(int(i == j)) for j in range(m)] for i in range(m)]
            lam, g2 = min(mu), sum(g * g for g in gam)
            ok &= abs(q) <= g2 / lam
            kap = Fr(rng.randint(1, 400), rng.randint(1, 20))
            phi = Fr(rng.choice((-1, 1))) * (Fr(1, 6) + Fr(rng.randint(0, 600), 1800))
            insts.append((kap, lam, g2, q, phi))
            nmat += 1
    for (kap, lam, g2, q, phi) in insts:
        f4 = 3 * q + 72 * kap * phi
        thr = 12 * kap if MUTANT == 'M4' else 6 * kap
        ok &= abs(f4) >= thr or lam <= g2 / (2 * kap)
        if abs(f4) < 6 * kap:
            second += 1
    for _ in range(2000):                                             # (Q3) puts |phi| in [1/6, 1/2] on B_4
        kap = Fr(rng.randint(1, 400), rng.randint(1, 20))
        eps = kap / 4 * Fr(rng.randint(0, 1000), 1000)
        dev = 2 * eps / (3 * kap) * Fr(rng.randint(-1000, 1000), 1000)
        aphi = Fr(1, 3) + dev
        ok &= Fr(1, 6) <= aphi <= Fr(1, 2)
    ok &= second > 0
    return {'instances': len(insts) + 2000, 'matrix_instances': nmat, 'second_alternative_only': second,
            'passed': bool(ok)}


# ----------------------------------------------------------------------------------------------- R4 typed window
def r4(rng):
    ok = True
    typed = 0
    for _ in range(6000):
        k = Fr(rng.randint(0, 40), rng.randint(1, 20))
        r = Fr(rng.randint(1, 20), 20)
        D = Fr(rng.choice((-1, 1)) * rng.randint(1, 80), rng.randint(1, 20))
        Y = Fr(rng.randint(-200, 200), rng.randint(1, 20))
        RM = Fr(rng.randint(-50, 50), rng.randint(1, 40))
        RS = Fr(rng.randint(-50, 50), rng.randint(1, 40))
        kM, kS = -6 * k * D + r * Y + RM, 6 * k * D + r * Y + RS
        if kM * kS < 0:
            typed += 1
            Rb = max(abs(RM), abs(RS))
            eta, kap = Rb / r, k / r
            ok &= abs(r * Y) <= 6 * k * abs(D) + Rb
            ok &= abs(kM * kS) <= r * r * (12 * kap * abs(D) + 2 * eta) ** 2
            ok &= abs(Y) <= 6 * kap * abs(D) + eta
    for _ in range(3000):
        D = Fr(rng.choice((-1, 1)) * rng.randint(1, 80), rng.randint(1, 20))
        c0 = Fr(rng.randint(-200, 200), rng.randint(1, 20))
        kap = Fr(rng.randint(0, 60), rng.randint(1, 20))
        eta = Fr(rng.randint(0, 60), rng.randint(1, 20))
        half = 6 * kap * abs(D) + eta
        x1, x2 = (-c0 - half) * 12 / D, (-c0 + half) * 12 / D
        length = abs(x2 - x1)
        claimed = 144 * kap + (12 if MUTANT == 'M5' else 24) * eta / abs(D)
        ok &= length == claimed
        lo, hi = min(x1, x2), max(x1, x2)
        for x in (lo, hi, (lo + hi) / 2):
            ok &= abs(x / 12 * D + c0) <= half
        for x in (lo - 1, hi + 1):
            ok &= abs(x / 12 * D + c0) > half
    for _ in range(3000):                                             # (x + y)^2 min(1, a + b) <= 2(x^2 + y^2)(a + min(1, b))
        x, y = Fr(rng.randint(0, 90), rng.randint(1, 9)), Fr(rng.randint(0, 90), rng.randint(1, 9))
        a, b = Fr(rng.randint(0, 40), rng.randint(1, 40)), Fr(rng.randint(0, 40), rng.randint(1, 40))
        ok &= (x + y) ** 2 * min(Fr(1), a + b) <= 2 * (x * x + y * y) * (a + min(Fr(1), b))
    ok &= typed > 500
    return {'typed_instances': typed, 'window_instances': 3000, 'splitting_instances': 3000, 'passed': bool(ok)}


# ----------------------------------------------------------------------------------------------- R5 W+ bookkeeping
def r5(rng):
    ok = True
    for _ in range(5000):
        kap = Fr(rng.randint(0, 100), rng.randint(1, 100))
        r = Fr(rng.randint(1, 100), 100)
        L = Fr(rng.randint(0, 400), 20)
        lhs = kap ** 3 + kap * kap * r + kap * r * r + r ** 3 * L
        mid = (kap + r) ** 2 * (kap + r * L)
        ok &= lhs <= mid <= (1 + L) * (kap + r) ** 3 and (kap + r) ** 3 <= 4 * (kap ** 3 + r ** 3)
    return {'instances': 5000, 'passed': bool(ok)}


# ----------------------------------------------------------------------------------------------- R6 C+/CE+ bookkeeping
def r6(rng):
    ok = True
    n = 0
    for _ in range(8000):
        s = Fr(rng.randint(1, 60), 60)                                  # r = s^2 in (0, 1]
        t = Fr(rng.randint(1, 1000), 1000) / s                          # kappa = t^2, kappa r = (t s)^2 <= 1
        r, kap = s * s, t * t
        n += 1
        mn = min(Fr(1), kap)
        ok &= kap * kap * mn * r ** 3 <= r
        ok &= t * mn * s ** 3 <= r                                      # kappa^(1/2) min(1, kappa) r^(3/2) <= r
        bound = r if MUTANT == 'M7' else 2 * r * (1 + kap)
        ok &= r * r * (1 + kap) ** 2 <= bound
        ok &= kap * kap * r * r <= kap * r
        ok &= kap * kap * s ** 3 + kap ** 3 * r * r <= 2 * kap * kap * r   # new elder error <= old r (1 + kappa)^2 part
    ok &= n == 8000
    return {'instances': n, 'passed': bool(ok)}


def main():
    global MUTANT
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', default=None)
    args = ap.parse_args()
    if args.mutant is not None and args.mutant not in ('M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'):
        sys.stderr.write('unknown mutant label\n')
        return 2
    MUTANT = args.mutant
    rng = random.Random(20261001)
    out = {'object': 'CL-THIRD-ORDER-RATE-20261001-v1 controls', 'scientific_effect': 'NONE', 'mutant': MUTANT,
           'checks': {'R1_exponent_ledger': r1(), 'R2_lemma_L': r2(rng), 'R3_refined_B4': r3(rng),
                      'R4_typed_window': r4(rng), 'R5_W_plus_bookkeeping': r5(rng),
                      'R6_C_plus_CE_plus_bookkeeping': r6(rng)}}
    out['passed'] = all(v['passed'] for v in out['checks'].values())
    sys.stdout.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
    return 0 if out['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
