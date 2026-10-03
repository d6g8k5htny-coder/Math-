#!/usr/bin/env python3
"""Exact controls for CL-CANDIDATE-THIRD-ORDER-20261001-v1 (frontiers/candidate_third_order_20261001/PROOF.md).
Standard library only, exact rationals. Run: python3 -B -S thmT_check.py   (and with -O; output byte-identical).
Mutants: --mutant M1|M2|M3|M4 must exit 1; an unknown label exits 2.

  T1 the exponent ledger of section 4 (rho_f = l^(1/4+1/44), rho_c = l^(1/4-1/36)): every exponent >= 4/11, equality
     exactly for rho_f^5/l and l^2 rho_f^-6, 4/11 > 1/3; rho_f < l^(1/4) < rho_c and l rho_f^-3 <= 1 for l <= 1
  T2 Lemma C, Step C1: the pathwise case analysis on random rational data (Case 1 weights and bounds; the sign window)
  T3 Lemma C, Step C2: the Lipschitz constant 12 kappa |Delta| of w_kappa in Y, and (36k^2D^2 - Y^2)_+ - 36k^2D^2 = -min
  T4 Lemma D: the Vandermonde inequality prod_{j != i*} |l_i* - l_j| <= 2^(m-1) prod_{j != i*} |l_j|, m = 1..5
  T5 (2.2) on exactly pinned polynomial fields of degree 7 in d = 2 and d = 3 (pinned jets solved symbolically as
     polynomials in r): det K_i = det H_i / r has constant term -+6k Delta and common r^1 coefficient
     Y = (f4/12) Delta + 3k tr(adj(A) B) - gamma^T adj(A) gamma / 4; the product has constant term -36 k^2 Delta^2, no
     r^1 term, and r^2 coefficient Y^2 at k = 0
"""
import argparse
import json
import random
import sys
from fractions import Fraction as Fr
from math import factorial

MUTANT = None


# ----------------------------------------------------------------------------------------------- T1 exponents
def t1():
    q = Fr(1, 4)
    af, ac = Fr(1, 44), Fr(1, 36)
    if MUTANT == 'M1':
        af = Fr(1, 40)
    ef, ec = q + af, q - ac                     # rho_f = l^ef, rho_c = l^ec
    terms = {'rho_f^2': 2 * ef, 'rho_f^5/l': 5 * ef - 1, 'l rho_f^-2': 1 - 2 * ef, 'l^2 rho_f^-6': 2 - 6 * ef,
             'rho_c^2': 2 * ec, 'rho_c^3': 3 * ec, 'l^2 rho_c^-7': 2 - 7 * ec, 'l rho_c^-2': 1 - 2 * ec, 'l': Fr(1)}
    least = min(terms.values())
    ok = (least == Fr(4, 11) and sorted(k for k, v in terms.items() if v == least) == ['l^2 rho_f^-6', 'rho_f^5/l']
          and Fr(4, 11) > Fr(1, 3) and ef > q > ec and 1 - 3 * ef >= 0)
    return {'exponents': {k: str(v) for k, v in sorted(terms.items())}, 'least': str(least), 'margin_over_1/3': str(least - Fr(1, 3)),
            'passed': bool(ok)}


# ----------------------------------------------------------------------------------------------- T2, T3 Lemma C
def rnd(rng, lo=-3, hi=3, den=97):
    return Fr(rng.randint(lo * den, hi * den), den)


def w_kappa(kap, D, Y):
    v = 36 * kap * kap * D * D - Y * Y
    return v if v > 0 else Fr(0)


def t2(rng):
    n_both = n_one = n_none = n_win = 0
    ok = True
    for _ in range(4000):
        s = rng.choice((1, -1))                       # s = (-1)^m = sign(Delta) when A_0 < 0
        kap = Fr(rng.randint(1, 400), 100)
        D = s * Fr(rng.randint(1, 300), 100)
        eta = Fr(rng.randint(0, 60), 100)
        rM, rS = Fr(rng.randint(-100, 100), 100) * eta, Fr(rng.randint(-100, 100), 100) * eta    # |rho_i| <= eta
        # put Y near the window edges half the time, to exercise the disagreement case
        if rng.random() < 0.5:
            Y = rng.choice((1, -1)) * 6 * kap * abs(D) + Fr(rng.randint(-100, 100), 100) * eta
        else:
            Y = rnd(rng) * 6 * kap * abs(D) / 2
        mM, mS = Y - 6 * kap * D + rM, Y + 6 * kap * D + rS
        typed = s * mM < 0 < s * mS
        lim = abs(Y) < 6 * kap * abs(D)
        a = abs(mM * mS) if typed else Fr(0)
        w = w_kappa(kap, D, Y)
        if lim != (w > 0):
            ok = False
        if typed and lim:
            n_both += 1
            ok &= abs(a - w) <= 24 * eta * kap * abs(D) + eta * eta
        elif typed or lim:
            n_one += 1
            b = 2 * eta * (12 * kap * abs(D) + 3 * eta)
            ok &= a <= b and w <= b
        else:
            n_none += 1
            ok &= a == 0 and w == 0
        # the sign window (#198 section 3): opposite signs force |m_i| <= 12 kappa |Delta| + 2 eta
        if mM * mS < 0:
            n_win += 1
            ok &= abs(mM) <= 12 * kap * abs(D) + 2 * eta and abs(mS) <= 12 * kap * abs(D) + 2 * eta
    return {'cases_both': n_both, 'cases_exactly_one': n_one, 'cases_neither': n_none, 'sign_window_cases': n_win,
            'passed': bool(ok and n_both > 100 and n_one > 100 and n_none > 100)}


def t3(rng):
    ok = True
    lip = 6 if MUTANT == 'M3' else 12
    for _ in range(4000):
        kap = Fr(rng.randint(1, 400), 100)
        D = rnd(rng)
        Y, Y2 = rnd(rng, -9, 9), rnd(rng, -9, 9)
        if rng.random() < 0.5:
            Y2 = Y + Fr(rng.randint(-20, 20), 1000)
        ok &= abs(w_kappa(kap, D, Y) - w_kappa(kap, D, Y2)) <= lip * kap * abs(D) * abs(Y - Y2)
        ok &= w_kappa(kap, D, Y) - 36 * kap * kap * D * D == -min(Y * Y, 36 * kap * kap * D * D)
    return {'trials': 4000, 'passed': bool(ok)}


# ----------------------------------------------------------------------------------------------- T4 Lemma D
def t4(rng):
    ok = True
    for m in range(1, 6):
        for _ in range(800):
            lam = [rnd(rng, -5, 5, 31) for _ in range(m)]
            if any(x == 0 for x in lam):
                continue
            i = min(range(m), key=lambda j: abs(lam[j]))
            lhs = Fr(1)
            rhs = Fr(2 ** (m - 1)) if MUTANT != 'M2' else Fr(1)
            for j in range(m):
                if j != i:
                    lhs *= abs(lam[i] - lam[j])
                    rhs *= abs(lam[j])
            ok &= lhs <= rhs
    return {'m': [1, 2, 3, 4, 5], 'trials_per_m': 800, 'passed': bool(ok)}


# ----------------------------------------------------------------------------------------------- T5 pinned polynomials
def padd(p, q):
    out = list(p) + [Fr(0)] * max(0, len(q) - len(p))
    for i, c in enumerate(q):
        out[i] += c
    return out


def pmul(p, q):
    out = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                out[i + j] += a * b
    return out


def pscale(p, c):
    return [c * x for x in p]


def trim(p):
    while len(p) > 1 and p[-1] == 0:
        p = p[:-1]
    return p


def rpow(n):                                            # the monomial r^n as a polynomial in r
    return [Fr(0)] * n + [Fr(1)]


def axis_odd_sum(c, D, h, shift, skip):
    """sum_{i odd} c[(i+shift,0..)] h^(i-1) r^(i-1) / i!  over available coefficients, skipping index `skip`"""
    out = [Fr(0)]
    for i in range(1, D + 2, 2):
        key = c.get(i + shift)
        if key is None or i + shift == skip:
            continue
        out = padd(out, pmul(pscale(rpow(i - 1), h ** (i - 1) / factorial(i)), key))
    return out


def axis_even_sum(c, D, h, skip):
    out = [Fr(0)]
    for i in range(0, D + 2, 2):
        key = c.get(i)
        if key is None or i == skip:
            continue
        out = padd(out, pmul(pscale(rpow(i), h ** i / factorial(i)), key))
    return out


def pinned_field(free, b, k, D, m):
    """free: dict multi-index (i, j_1..j_m) -> Fr, the free Taylor coefficients of f = sum c_a x^i y^j / (i! j!).
    Returns dict multi-index -> polynomial in r: the pinned coefficients solved exactly from the pin rows of [R] section 2."""
    c = {key: [val] for key, val in free.items()}
    h = Fr(1, 2)
    z = (0,) * m
    ax = {i: c[(i,) + z] for i in range(D + 1) if (i,) + z in c}
    # row 3: (f_x(S) - f_x(M))/r = sum_{i odd} c_{i+1} h^(i-1) r^(i-1)/i! = 0
    ax[2] = pscale(axis_odd_sum(ax, D, h, 1, 2), Fr(-1))
    # row 4: (6/r^2)[f_x(M) + f_x(S) - 2(f(S) - f(M))/r] = c_3 + sum_{j odd >= 5} 12 (j-1) h^(j-1) / j! r^(j-3) c_j = 12k
    rest = [Fr(0)]
    for j in range(5, D + 1, 2):
        if j in ax:
            rest = padd(rest, pmul(pscale(rpow(j - 3), Fr(12 * (j - 1)) * h ** (j - 1) / factorial(j)), ax[j]))
    if MUTANT == 'M4':                                  # a one-sided axial row: an odd-order perturbation of c_3
        rest = padd(rest, pmul(pscale(rpow(1), Fr(1, 2)), ax[4]))
    ax[3] = padd([12 * k], pscale(rest, Fr(-1)))
    # row 2: (f(S) - f(M))/r = sum_{i odd} c_i h^(i-1) r^(i-1)/i! = -k r^2
    ax[1] = padd(pscale(rpow(2), -k), pscale(axis_odd_sum(ax, D, h, 0, 1), Fr(-1)))
    # row 1: (f(M) + f(S))/2 = sum_{i even} c_i (h r)^i / i! = b - k r^3 / 2
    ax[0] = padd(padd([b], pscale(rpow(3), -k / 2)), pscale(axis_even_sum(ax, D, h, 0), Fr(-1)))
    for i in range(4):
        c[(i,) + z] = ax[i]
    # transverse rows, one pair per transverse direction l
    for l in range(m):
        e = tuple(1 if t == l else 0 for t in range(m))
        tr = {i: c[(i,) + e] for i in range(D) if (i,) + e in c}
        c[(0,) + e] = pscale(axis_even_sum(tr, D, h, 0), Fr(-1))     # (f_yl(M) + f_yl(S))/2 = 0
        c[(1,) + e] = pscale(axis_odd_sum(tr, D, h, 0, 1), Fr(-1))   # (f_yl(S) - f_yl(M))/r = 0
    return c


def deriv_at(c, alpha, sign, D):
    """d^alpha f at (sign h r, 0, ..., 0) as a polynomial in r; alpha = (a_x, a_y1, ..., a_ym)"""
    h = Fr(1, 2) * sign
    out = [Fr(0)]
    for i in range(0, D + 1):
        key = c.get((alpha[0] + i,) + tuple(alpha[1:]))
        if key is None:
            continue
        out = padd(out, pmul(pscale(rpow(i), h ** i / factorial(i)), key))
    return out


def det_poly(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return padd(pmul(M[0][0], M[1][1]), pscale(pmul(M[0][1], M[1][0]), Fr(-1)))
    out = [Fr(0)]
    for j in range(n):
        minor = [[M[i][t] for t in range(n) if t != j] for i in range(1, n)]
        out = padd(out, pscale(pmul(M[0][j], det_poly(minor)), Fr((-1) ** j)))
    return out


def det_num(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    return sum(((-1) ** j) * M[0][j] * det_num([[M[i][t] for t in range(n) if t != j] for i in range(1, n)]) for j in range(n))


def adj_num(M):
    n = len(M)
    if n == 1:
        return [[Fr(1)]]
    return [[((-1) ** (i + j)) * det_num([[M[a][b] for b in range(n) if b != i] for a in range(n) if a != j]) for j in range(n)]
            for i in range(n)]


def multi_indices(d, D):
    out = []
    def rec(prefix, left, slots):
        if slots == 0:
            out.append(tuple(prefix))
            return
        for v in range(left + 1):
            rec(prefix + [v], left - v, slots - 1)
    rec([], D, d)
    return out


def t5(rng):
    D = 7
    ok = True
    rows = []
    for d in (2, 3):
        m = d - 1
        pinned = {(i,) + (0,) * m for i in range(4)}
        for l in range(m):
            e = tuple(1 if t == l else 0 for t in range(m))
            pinned |= {(0,) + e, (1,) + e}
        for trial in range(4):
            k = Fr(0) if trial % 2 == 0 else Fr(rng.randint(1, 300), 100)
            b = rnd(rng)
            free = {a: rnd(rng, -2, 2, 13) for a in multi_indices(d, D) if a not in pinned}
            c = pinned_field(free, b, k, D, m)
            det = {}
            k1 = {}
            unit = lambda t: tuple(1 if s == t else 0 for s in range(d))
            # transverse jets at 0
            A = [[free[(0,) + tuple(unit(1 + l)[1:][s] + unit(1 + q)[1:][s] for s in range(m))] for q in range(m)] for l in range(m)]
            B = [[free[(1,) + tuple(unit(1 + l)[1:][s] + unit(1 + q)[1:][s] for s in range(m))] for q in range(m)] for l in range(m)]
            gam = [free[(2,) + unit(1 + l)[1:]] for l in range(m)]
            f4 = free[(4,) + (0,) * m]
            Dl = det_num(A)
            adjA = adj_num(A)
            trAB = sum(adjA[i][j] * B[j][i] for i in range(m) for j in range(m))
            q = sum(gam[i] * adjA[i][j] * gam[j] for i in range(m) for j in range(m)) / 4
            Y = f4 / 12 * Dl + 3 * k * trAB - q
            for name, sg in (('M', -1), ('S', 1)):
                H = [[deriv_at(c, tuple(unit(a)[t] + unit(bb)[t] for t in range(d)), sg, D) for bb in range(d)] for a in range(d)]
                dh = trim(det_poly(H))
                if dh[0] != 0:
                    ok = False
                dk = trim(dh[1:])
                det[name] = dk
                k1[name] = dk[1] if len(dk) > 1 else Fr(0)
                if dk[0] != sg * 6 * k * Dl:          # det K_M = -6k Delta + ..., det K_S = +6k Delta + ...
                    ok = False
            prod = trim(pmul(det['M'], det['S']))
            c0 = prod[0]
            c1 = prod[1] if len(prod) > 1 else Fr(0)
            c2 = prod[2] if len(prod) > 2 else Fr(0)
            good = (c0 == -36 * k * k * Dl ** 2 and c1 == 0 and k1['M'] == Y and k1['S'] == Y and (k != 0 or c2 == Y * Y))
            ok &= good
            rows.append({'d': d, 'k': str(k), 'deg_product': len(prod) - 1, 'const_ok': c0 == -36 * k * k * Dl ** 2,
                         'r1_zero': c1 == 0, 'common_Y': k1['M'] == Y and k1['S'] == Y,
                         'r2_is_Y2_at_k0': (c2 == Y * Y) if k == 0 else None})
    return {'trials': rows, 'passed': bool(ok)}


def main():
    global MUTANT
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', default=None)
    args = ap.parse_args()
    if args.mutant is not None and args.mutant not in ('M1', 'M2', 'M3', 'M4'):
        sys.stderr.write('unknown mutant label\n')
        return 2
    MUTANT = args.mutant
    rng = random.Random(20261001)
    out = {'object': 'CL-CANDIDATE-THIRD-ORDER-20261001-v1 controls', 'scientific_effect': 'NONE', 'mutant': MUTANT,
           'checks': {'T1_exponent_ledger': t1(), 'T2_lemma_C_cases': t2(rng), 'T3_lipschitz': t3(rng),
                      'T4_vandermonde': t4(rng), 'T5_pinned_product_d2_d3': t5(rng)}}
    out['passed'] = all(v['passed'] for v in out['checks'].values())
    sys.stdout.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
    return 0 if out['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
