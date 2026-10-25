## QS addendum A3.5: author controls, exact executable and stdout

This publishes the standard-library control script that A3.5 ([6001191875](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6001191875)) cites, so anyone can replay it. It checks finite algebra and exactly pinned polynomial fields only; it does not prove the analytic statements.

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction rule.** The same as in [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189): the file is the exact text between the first ```` ```python ```` fence after its `###` heading and the next ```` ``` ```` line, plus a final newline. The expected stdout is the single JSON line in the following ```` ```json ```` fence, plus one newline.

**Run.** Each full run takes about 40 s.
- `python3 -B -S a35_exact.py`: exit 0, with exactly the stdout below.
- `python3 -B -O -S a35_exact.py`: byte-identical output. No check depends on an `assert`.
- `--mutant M1` … `M10`: each exits 1 in both modes and names its failing control on stderr:
  - M1 fails in F2's (FW.2), M2 and M8 in (FW.1), M9 in (FW.2), M10 in (FW.4);
  - M3 and M7 fail in D1;
  - M4 fails in T1's Frobenius identity, M5 in G1's inner bound, M6 in G2.
- `--bogus` and `--mutant M11`: exit 2.

The output was produced with Python 3.11.15. The script uses only `json`, `random`, `sys`, `fractions`, `itertools` and `math`.

### a35_exact.py

- **File:** 21719 bytes, SHA-256 `b017e11ac1e1a21051ab03b41d8701760fad7d88de6b2cb5bae1224329e6ec7d`.
- **Stdout:** 1180 bytes, SHA-256 `b30bc8ebe18f5a3d8fa0340035aec6ad5fd690f6abf469d2f1e38cbc52e93100`.

```python
#!/usr/bin/env python3
"""A3.5 controls: exact rational checks of the deterministic algebra of QS addendum A3.5 (d = 3).

Usage:  python3 -B -S a35_exact.py             -> JSON summary on stdout, exit 0 iff every check passes
        python3 -B -S a35_exact.py --mutant Mk  -> runs with mutant Mk (k = 1..10); must exit 1 (failure on stderr)
Standard library only; exact Fractions; seeded; no check depends on an assert. Output is byte-identical under -O.

  F1  Lemma FW3 (i), the cube: |E|_j <= K_j^(3) N r w^(4-j), j = 0, 1, 2.
  F2  Lemma FW3 (ii), the barrel box |eta| <= v with r^(1/2) v <= w: (FW.0) for j = 0, 1, 2, and (FW.1)-(FW.4).
  F3  Lemma FW3 (iii): |a2| <= c0 N w^2, |d_X a2| + |d_zeta a2| <= c1 N w, ||D^2 a2|| <= c2 N.
      F1-F3 run on exactly pinned rational fields of degree 6 (pins by an exact linear solve), with k in [k-, k+],
      and on three near-extremal families: (Nc/6)(x+y1)^3 y2 for (FW.1); (Nc/2)(x+y1) y2^2 + (Nc/6) y2^3 on the
      longest box for (FW.2)-(FW.3); Nc (x+y1+y2)^4/24 on the longest box for (FW.4). N is a rigorous upper bound
      1 + sum |coef| * (box monomial) over every partial of order 3 or 4 on the physical box.
  D1  Proposition D3: from the FW3 budgets and the barrel event (B_r), the claims (a) and (b), exactly, with k in
      [k-, k+] and lambda2 from just above the threshold to 10^6 times it (lambda2 = k v^2, v rational).
  T1  Lemma T3: QS's identity G_k = P o phi; D^2 P at both pins by exact differentiation; gamma^2 kappa_i = a_i/12;
      the Frobenius identity ||T_i||_F^2 = 1/3 + (gamma^2 + 144)/(12 a_i); the chain rule for phi.
  G1  Theorem G3's one-dimensional integrals: the closed forms, each sandwiched by exact Riemann sums on monotone
      pieces (with an exact tail bound), and the sharpness of the constant 3/2.
  G2  Theorem G3's exponent bookkeeping for w = r^(-beta).
Mutants: M1 (FW.2) without the factor w; M2 (FW.1) with r^2 for r^(3/2); M3 C_e = c0^2; M4 L_i with 24 a_i;
M5 inner-integral constant 1 for 3/2; M6 the O(r^4) range beta <= 1/4; M7 barrel half-width 2 sqrt(k/lambda2);
M8 A1/2; M9 A2/2; M10 A4 = 0.
"""
import json
import random
import sys
from fractions import Fraction as Fr
from itertools import product

MUTANTS = ['M%d' % i for i in range(1, 11)]
MUT = None
if len(sys.argv) == 3 and sys.argv[1] == '--mutant' and sys.argv[2] in MUTANTS:
    MUT = sys.argv[2]
elif len(sys.argv) != 1:
    sys.stderr.write('usage: a35_exact.py [--mutant M1|...|M10]\n')
    sys.exit(2)

FAIL = []
COUNT = {}
WORST = {}


def record(name, ok, detail=''):
    COUNT[name] = COUNT.get(name, 0) + 1
    if not ok and len(FAIL) < 20:
        FAIL.append('%s: %s' % (name, detail))


def ratio(name, num, den):
    rat = num / den
    WORST[name] = max(WORST.get(name, Fr(0)), rat)
    record(name, rat <= 1, 'ratio %s' % float(rat))


# ---------------------------------------------------------------- polynomials in three variables
def padd(p, q, c=1):
    out = dict(p)
    for e, v in q.items():
        out[e] = out.get(e, 0) + c * v
    return {e: v for e, v in out.items() if v != 0}


def pdiff(p, a, b, c):
    out = {}
    for (i, j, l), v in p.items():
        if i >= a and j >= b and l >= c:
            f = 1
            for n, m in ((i, a), (j, b), (l, c)):
                for t in range(m):
                    f *= (n - t)
            out[(i - a, j - b, l - c)] = out.get((i - a, j - b, l - c), 0) + f * v
    return {e: v for e, v in out.items() if v != 0}


def peval(p, x, y, z):
    s = Fr(0)
    for (i, j, l), v in p.items():
        s += v * x ** i * y ** j * z ** l
    return s


def fact(n):
    f = 1
    for t in range(2, n + 1):
        f *= t
    return f


def binom(n, m):
    return fact(n) // (fact(m) * fact(n - m))


def solve_lin(A, b):
    n = len(A)
    M = [list(row) + [bb] for row, bb in zip(A, b)]
    for c in range(n):
        piv = next(i for i in range(c, n) if M[i][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c] / M[c][c]
                M[i] = [a - f * bb for a, bb in zip(M[i], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


# ---------------------------------------------------------------- constants for k in [km, kp]
def consts(km, kp):
    one = Fr(1)
    M1 = max(1 / km, one)
    M2 = max(1 / km, one, kp)
    H3 = 2 + kp
    C = {}
    C['K0'] = Fr(9, 64) / km + Fr(1, 16) + (1 + kp) ** 4 / (24 * km)             # C91 (W3), H = 1 + k+
    C['K1'] = Fr(33, 128) / km + Fr(1, 16) + M1 * (1 + kp) ** 3 / 6
    C['K2'] = Fr(17, 48) / km + Fr(1, 24) + M2 * (1 + kp) ** 2 / 2
    C['K0_3'] = Fr(9, 64) / km + Fr(1, 16) + Fr(35, 48) / km + Fr(1, 2) + H3 ** 4 / (24 * km)
    C['K1_3'] = Fr(33, 128) / km + Fr(1, 16) + Fr(25, 16) / km + 1 + M1 * H3 ** 3 / 6
    C['K2_3'] = Fr(17, 48) / km + Fr(1, 24) + Fr(49, 24) / km + 1 + M2 * H3 ** 2 / 2
    C['A1'] = (Fr(1, 48) + Fr(1, 24) + (1 + kp) ** 3 / 6) / km
    C['A2'] = 1 + 2 / km
    C['A3'] = Fr(1, 24) / km + (1 + 1 / km) * H3 ** 2 / 2
    C['A4'] = max(1 + 2 / km, H3 * max(one, kp))
    if MUT == 'M8':
        C['A1'] /= 2
    if MUT == 'M9':
        C['A2'] /= 2
    if MUT == 'M10':
        C['A4'] = Fr(0)
    C['c0'] = Fr(5, 8) / km + 1 + kp / 2
    C['c1'] = 2 + 1 / km + kp
    C['c2'] = 1 + max(1 / km, kp)
    C['c3'] = C['c1'] + 1 + 1 / km + C['A3']
    C['CB'] = max(Fr(16), 2 * C['A2'], (C['c0'] + C['A1']) ** 2)
    C['Ce'] = (C['c0'] + C['A1']) ** 2 if MUT != 'M3' else C['c0'] ** 2
    C['Dh'] = 2 * (C['K2'] + C['A4'])
    C['Ch'] = 2 * C['c2'] * (C['c0'] + C['A1']) + 2 * C['c3'] ** 2
    return C


# ---------------------------------------------------------------- exactly pinned rational fields of degree <= 6
def pinned_field(rnd, s, k, lam_t, lam2, deg=6, special=None):
    """b = 0, r = s^2, eigenframe (x, y1, y2) = (u, e1, e2); the 8 pin equations solved exactly."""
    r = s * s
    h = r / 2
    c = {}
    if special is None:
        for e in product(range(deg + 1), repeat=3):
            if 3 <= sum(e) <= deg:
                c[e] = Fr(rnd.randint(-6, 6), rnd.choice([1, 2, 3, 4])) / (fact(e[0]) * fact(e[1]) * fact(e[2]))
    else:
        c.update(special)
    c[(0, 2, 0)] = -(r * lam_t / k) / 2
    c[(0, 0, 2)] = -lam2 / 2
    c[(0, 1, 1)] = Fr(0)
    hi = {n: c.get((n, 0, 0), Fr(0)) for n in range(4, deg + 1)}
    rows, rhs = [], []
    for xv, kind, target in ((-h, 0, Fr(0)), (h, 0, -k * r ** 3), (-h, 1, Fr(0)), (h, 1, Fr(0))):
        rows.append([xv ** n if kind == 0 else (n * xv ** (n - 1) if n else Fr(0)) for n in range(4)])
        rhs.append(target - sum(v * (xv ** n if kind == 0 else n * xv ** (n - 1)) for n, v in hi.items()))
    sol = solve_lin(rows, rhs)
    for n in range(4):
        c[(n, 0, 0)] = sol[n]
    for e1, e2 in ((1, 0), (0, 1)):
        hi2 = {n: c.get((n, e1, e2), Fr(0)) for n in range(2, deg)}
        sol2 = solve_lin([[Fr(1), -h], [Fr(1), h]], [-sum(v * (-h) ** n for n, v in hi2.items()),
                                                     -sum(v * h ** n for n, v in hi2.items())])
        c[(0, e1, e2)], c[(1, e1, e2)] = sol2
    return {e: v for e, v in c.items() if v != 0}


def pin_residual(f, r, k):
    h = r / 2
    res = [peval(f, -h, 0, 0), peval(f, h, 0, 0) + k * r ** 3]
    for d in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        g = pdiff(f, *d)
        res += [peval(g, -h, 0, 0), peval(g, h, 0, 0)]
    return max(abs(x) for x in res)


def N_upper(f, box):
    """A rigorous upper bound for 1 + sup over the box of every partial of order 3 or 4 (all the proof uses)."""
    m = Fr(0)
    for e in product(range(5), repeat=3):
        if sum(e) in (3, 4):
            g = pdiff(f, *e)
            m = max(m, sum(abs(v) * box[0] ** i * box[1] ** j * box[2] ** l for (i, j, l), v in g.items()))
    return 1 + m


def error_poly(f, s, k, lam_t, lam2):
    r = s * s
    F = {(i, j, l): v * r ** i * (r * k) ** j * s ** (3 * l) / (k * r ** 3) for (i, j, l), v in f.items()}
    J = lambda e: peval(pdiff(f, *e), 0, 0, 0)
    gam, B, C3 = J((2, 1, 0)), J((1, 2, 0)), J((0, 3, 0))
    g2, b2, n2 = J((2, 0, 1)), J((1, 1, 1)), J((0, 2, 1))
    Gk = {(3, 0, 0): Fr(2), (1, 0, 0): Fr(-3, 2), (0, 0, 0): Fr(-1, 2), (2, 1, 0): gam / 2, (0, 1, 0): -gam / 8,
          (0, 2, 0): -lam_t / 2, (1, 2, 0): k * B / 2, (0, 3, 0): k * k * C3 / 6}
    a2 = {(2, 0, 0): g2 / (2 * k), (0, 0, 0): -g2 / (8 * k), (1, 1, 0): b2, (0, 2, 0): k * n2 / 2}
    E = padd(F, {e: v for e, v in Gk.items() if v != 0}, -1)
    E = padd(E, {(0, 0, 2): lam2 / (2 * k)})
    E = padd(E, {(i, j, 1): s * v for (i, j, _), v in a2.items() if v != 0}, -1)
    return E, {e: v for e, v in a2.items() if v != 0}, (g2, b2, n2)


ORD = {j: [e for e in product(range(3), repeat=3) if sum(e) == j] for j in (0, 1, 2)}


def check_fields(f, s, k, km, kp, lam_t, lam2, w, v):
    r = s * s
    record('F0_pins_exact', pin_residual(f, r, k) == 0, 'pin residual')
    C = consts(km, kp)
    E, a2, (g2, b2, n2) = error_poly(f, s, k, lam_t, lam2)
    D = {e: pdiff(E, *e) for j in (0, 1, 2) for e in ORD[j]}
    grid = [-w, -w / 2, -w / 5, 0, w / 3, 2 * w / 3, w]
    # F1: the cube
    NI = N_upper(f, (r * w, r * k * w, s ** 3 * w))
    pts = list(product(grid, repeat=3))
    for j, key in ((0, 'K0_3'), (1, 'K1_3'), (2, 'K2_3')):
        m = max(abs(peval(D[e], *p)) for e in ORD[j] for p in pts)
        ratio('F1_cube_j%d' % j, m, C[key] * NI * r * w ** (4 - j))
    # F2: the barrel box
    NB = N_upper(f, (r * w, r * k * w, s ** 3 * max(w, v)))
    pp = list(product(grid, repeat=2))
    pb = [(x, y, z) for (x, y) in pp for z in (-v, -v / 2, 0, v / 3, v)]
    for j, key in ((0, 'K0'), (1, 'K1'), (2, 'K2')):
        m = max(abs(peval(D[e], x, y, 0)) for e in ORD[j] if e[2] == 0 for x, y in pp)
        ratio('F2_FW0_j%d' % j, m, C[key] * NB * r * w ** (4 - j))
    r32 = s ** 3 if MUT != 'M2' else r * r
    ratio('F2_FW1', max(abs(peval(D[(0, 0, 1)], x, y, 0)) for x, y in pp), C['A1'] * NB * r32 * w ** 3)
    wf = w if MUT != 'M1' else Fr(1)
    ratio('F2_FW2', max(abs(peval(D[(0, 0, 2)], *p)) for p in pb), C['A2'] * NB * r * wf)
    ratio('F2_FW3', max(abs(peval(D[(1, 0, 1)], *p)) + abs(peval(D[(0, 1, 1)], *p)) for p in pb),
          NB * r * ((1 + 1 / km) * v + C['A3'] * s * w ** 2))
    ratio('F2_FW4', max(abs(peval(D[e], *p)) for e in ((2, 0, 0), (1, 1, 0), (0, 2, 0)) for p in pb),
          (C['K2'] + C['A4']) * NB * r * w ** 2)
    # F3: the hard coefficient
    Da = (pdiff(a2, 1, 0, 0), pdiff(a2, 0, 1, 0))
    ratio('F3_a2', max(abs(peval(a2, x, y, 0)) for x, y in pp), C['c0'] * NB * w ** 2)
    ratio('F3_Da2', max(abs(peval(Da[0], x, y, 0)) + abs(peval(Da[1], x, y, 0)) for x, y in pp), C['c1'] * NB * w)
    ratio('F3_D2a2', max(abs(g2 / k) + abs(b2), abs(b2) + abs(k * n2)), C['c2'] * NB)


def check_F(rnd):
    n = 0
    for trial in range(24):
        km = rnd.choice([Fr(1, 2), Fr(1), Fr(3, 2)])
        kp = km * rnd.choice([Fr(1), Fr(2)])
        k = rnd.choice([km, kp, (km + kp) / 2])
        s = rnd.choice([Fr(1, 2), Fr(1, 3), Fr(1, 5)])
        w = rnd.choice([Fr(1), Fr(2), 1 / s])
        v = w / s if trial % 2 else w
        lam_t = Fr(rnd.randint(-8, 16), 4)
        lam2 = Fr(rnd.randint(1, 16), 4)
        f = pinned_field(rnd, s, k, lam_t, lam2)
        check_fields(f, s, k, km, kp, lam_t, lam2, w, v)
        n += 1
    for Nc in (Fr(100), Fr(1000)):
        for k in (Fr(1, 2), Fr(1), Fr(2)):
            s, w = Fr(1, 10), Fr(3)
            sp1 = {(a, 3 - a, 1): Nc / 6 * binom(3, a) for a in range(4)}               # (Nc/6)(x + y1)^3 y2
            check_fields(pinned_field(rnd, s, k, Fr(1), Fr(2), special=sp1), s, k, k, k, Fr(1), Fr(2), w, w)
            sp2 = {(1, 0, 2): Nc / 2, (0, 1, 2): Nc / 2, (0, 0, 3): Nc / 6}            # (Nc/2)(x + y1) y2^2 + (Nc/6) y2^3
            check_fields(pinned_field(rnd, s, k, Fr(1), Fr(2), special=sp2), s, k, k, k, Fr(1), Fr(2), w, w / s)
            sp4 = {(a, b, 4 - a - b): Nc / 24 * (fact(4) // (fact(a) * fact(b) * fact(4 - a - b)))
                   for a in range(5) for b in range(5 - a)}                           # Nc (x + y1 + y2)^4 / 24
            check_fields(pinned_field(rnd, s, k, Fr(1), Fr(2), special=sp4), s, k, k, k, Fr(1), Fr(2), w, w / s)
            n += 3
    return n


# ---------------------------------------------------------------- D1: Proposition D3's algebra
def sqrt_hi(q, prec=10 ** 30):
    import math
    return Fr(math.isqrt(q.numerator * prec * prec // q.denominator) + 1, prec)


def check_D1(rnd):
    n = 0
    for trial in range(4000):
        km = rnd.choice([Fr(1, 4), Fr(1, 2), Fr(1), Fr(3, 2)])
        kp = km * rnd.choice([Fr(1), Fr(3, 2), Fr(2)])
        k = km + (kp - km) * Fr(rnd.randint(0, 4), 4)
        C = consts(km, kp)
        if trial % 5 == 0:
            s, w = Fr(1), Fr(1)                                    # the extreme r = w = 1
        else:
            s = Fr(1, rnd.randint(2, 60))
            w = Fr(rnd.randint(1, max(1, int(1 / s))), 1)
        r = s * s
        N = Fr(rnd.randint(1, 12), rnd.choice([1, 2])) + 1
        thr = C['CB'] * k * N * N * r * w ** 4
        v = sqrt_hi(thr / k) * rnd.choice([Fr(1), Fr(1001, 1000), Fr(11, 10), Fr(10), Fr(1000)])
        lam2 = k * v * v
        if not lam2 > thr:
            continue
        eps = 4 / v if MUT != 'M7' else 2 / v                     # eps = 4 sqrt(k/lambda2)
        xi = k * N / lam2
        d0 = C['K0'] * N * r * w ** 4
        d1 = C['A1'] * N * s ** 3 * w ** 3
        dzz = C['A2'] * N * r * w
        dxz = N * r * ((1 + 1 / km) * eps + s * w ** 2 * C['A3'])
        dxx = 2 * (C['K2'] + C['A4']) * N * r * w ** 2
        al0, al1, al2 = C['c0'] * N * w ** 2, C['c1'] * N * w, C['c2'] * N
        Lb = lam2 / k - dzz
        q0 = s * al0 + d1
        ok = s * eps < w and Lb > lam2 / (2 * k) and q0 < Lb * eps / 2 and Lb * eps * eps > 8
        ok = ok and d0 + q0 * q0 / (2 * Lb) <= N * r * w ** 4 * (C['K0'] + C['Ce'] * xi)
        ok = ok and dxx + s * al2 * q0 / Lb + (s * al1 + dxz) ** 2 / Lb <= N * r * w ** 2 * (C['Dh'] + C['Ch'] * xi)
        record('D1_prop_D3', ok, 'km=%s kp=%s k=%s s=%s w=%s N=%s' % (km, kp, k, s, w, N))
        n += 1
    return n


# ---------------------------------------------------------------- T1: QS identity, pin Hessians, transfer
def check_T1(rnd):
    for trial in range(300):
        k = rnd.choice([Fr(1, 2), Fr(1), Fr(3, 2), Fr(2)])
        gam = Fr(rnd.choice([-1, 1]) * rnd.randint(1, 30), rnd.randint(1, 6))
        lam_t = Fr(rnd.randint(1, 40), rnd.randint(1, 8))
        B = Fr(rnd.randint(-30, 30), rnd.randint(1, 8))
        C3 = Fr(rnd.randint(-30, 30), rnd.randint(1, 8))
        psi = 24 * lam_t / gam ** 2
        c = 1 - 12 * k * B / gam ** 2
        R = 8 - 144 * k * B / gam ** 2 + 576 * k * k * C3 / gam ** 3
        # P(u, Z) = 2(u + 1/2)^2 (u - 1) - (psi + 2 c u) Z^2/48 + R Z^3/3456, as a polynomial in (u, Z)
        P = {(3, 0, 0): Fr(2), (1, 0, 0): Fr(-3, 2), (0, 0, 0): Fr(-1, 2), (0, 2, 0): -psi / 48,
             (1, 2, 0): -2 * c / 48, (0, 3, 0): R / 3456}
        Gk = {(3, 0, 0): Fr(2), (1, 0, 0): Fr(-3, 2), (0, 0, 0): Fr(-1, 2), (2, 1, 0): gam / 2, (0, 1, 0): -gam / 8,
              (0, 2, 0): -lam_t / 2, (1, 2, 0): k * B / 2, (0, 3, 0): k * k * C3 / 6}
        ok = True
        for _ in range(5):
            u = Fr(rnd.randint(-40, 40), rnd.randint(1, 9))
            Z = Fr(rnd.randint(-40, 40), rnd.randint(1, 9))
            ok = ok and peval(Gk, u - Z / 12, Z / gam, 0) == peval(P, u, Z, 0)
        record('T1_qs_identity', ok, 'G_k o phi != P')
        Y = 3 * k * B - gam ** 2 / 4
        aM, aS = 6 * lam_t + Y, 6 * lam_t - Y
        kS, kM = (psi + c) / 48, (psi - c) / 48
        H = lambda pt: [[peval(pdiff(P, 2, 0, 0), *pt), peval(pdiff(P, 1, 1, 0), *pt)],
                        [peval(pdiff(P, 1, 1, 0), *pt), peval(pdiff(P, 0, 2, 0), *pt)]]
        ok = H((Fr(1, 2), 0, 0)) == [[6, 0], [0, -2 * kS]] and H((Fr(-1, 2), 0, 0)) == [[-6, 0], [0, -2 * kM]]
        ok = ok and gam ** 2 * kS == aS / 12 and gam ** 2 * kM == aM / 12
        record('T1_pin_hessians', ok, 'D^2 P at the pins')
        for ai, ki in ((aM, kM), (aS, kS)):
            if ai <= 0:
                continue
            Mm = [[Fr(1), Fr(-1, 12)], [Fr(0), 1 / gam]]
            J2 = [Fr(1, 3), 1 / ki]
            frob = sum(Mm[p][q] ** 2 * J2[q] for p in range(2) for q in range(2))
            den = 12 if MUT != 'M4' else 24
            record('T1_frobenius', frob == Fr(1, 3) + (gam ** 2 + 144) / (den * ai), 'frobenius')
        e = {(i, j, 0): Fr(rnd.randint(-9, 9), rnd.randint(1, 5)) for i in range(4) for j in range(4 - i)}
        u = Fr(rnd.randint(-9, 9), 7)
        Z = Fr(rnd.randint(-9, 9), 5)
        X, ze = u - Z / 12, Z / gam
        Hraw = [[peval(pdiff(e, 2, 0, 0), X, ze, 0), peval(pdiff(e, 1, 1, 0), X, ze, 0)],
                [peval(pdiff(e, 1, 1, 0), X, ze, 0), peval(pdiff(e, 0, 2, 0), X, ze, 0)]]
        comp = {}
        for (i, j, _), val in e.items():
            for t in range(i + 1):
                key = (t, i - t + j, 0)
                comp[key] = comp.get(key, 0) + val * binom(i, t) * Fr(-1, 12) ** (i - t) / gam ** j
        Huz = [[peval(pdiff(comp, 2, 0, 0), u, Z, 0), peval(pdiff(comp, 1, 1, 0), u, Z, 0)],
               [peval(pdiff(comp, 1, 1, 0), u, Z, 0), peval(pdiff(comp, 0, 2, 0), u, Z, 0)]]
        Mm = [[Fr(1), Fr(-1, 12)], [Fr(0), 1 / gam]]
        MtHM = [[sum(Mm[a][p] * Hraw[a][b] * Mm[b][q] for a in range(2) for b in range(2)) for q in range(2)]
                for p in range(2)]
        record('T1_chain_rule', MtHM == Huz, 'chain rule')


# ---------------------------------------------------------------- G1: one-dimensional integrals
def inner_I(x1, x0, sig, A):
    """int_0^A min(1, (sig/y)^3)(x1 y + x0) dy, exact closed form."""
    if sig >= A:
        return x1 * A * A / 2 + x0 * A
    return x1 * sig * sig / 2 + x0 * sig + sig ** 3 * (x1 * (1 / sig - 1 / A) + x0 * (1 / sig ** 2 - 1 / A ** 2) / 2)


def riemann(fn, lo, hi, n, increasing):
    """Exact lower and upper Riemann sums of a monotone function on [lo, hi]."""
    hstep = (hi - lo) / n
    left = sum(fn(lo + i * hstep) for i in range(n)) * hstep
    right = sum(fn(lo + (i + 1) * hstep) for i in range(n)) * hstep
    return (left, right) if increasing else (right, left)


def check_G1(rnd):
    cst = Fr(3, 2) if MUT != 'M5' else Fr(1)
    for _ in range(1500):
        x1 = Fr(rnd.randint(0, 50), rnd.randint(1, 9))
        x0 = Fr(rnd.randint(0, 50), rnd.randint(1, 9))
        sig = Fr(rnd.randint(1, 200), rnd.randint(1, 400))
        A = Fr(rnd.randint(1, 10 ** 6), rnd.randint(1, 50))
        record('G1a_inner_bound', inner_I(x1, x0, sig, A) <= cst * (x1 * sig * sig + x0 * sig), 'inner')
    # the closed form against exact Riemann sums: increasing on [0, min(sig, A)], decreasing on [sig, A]
    for _ in range(40):
        x1 = Fr(rnd.randint(0, 9), rnd.randint(1, 5))
        x0 = Fr(rnd.randint(0, 9), rnd.randint(1, 5))
        sig = Fr(rnd.randint(1, 20), rnd.randint(1, 10))
        A = Fr(rnd.randint(1, 40), rnd.randint(1, 5))
        m = min(sig, A)
        lo1, hi1 = riemann(lambda y: x1 * y + x0, Fr(0), m, 64, True)
        lo2 = hi2 = Fr(0)
        if sig < A:
            lo2, hi2 = riemann(lambda y: sig ** 3 * (x1 / y ** 2 + x0 / y ** 3), sig, A, 64, False)
        I = inner_I(x1, x0, sig, A)
        record('G1a_closed_form', lo1 + lo2 <= I <= hi1 + hi2, 'Riemann sandwich')
    x1, x0, sig = Fr(1), Fr(1), Fr(1, 10)
    rat = inner_I(x1, x0, sig, Fr(10 ** 9)) / (Fr(3, 2) * (x1 * sig * sig + x0 * sig))
    record('G1a_sharp', Fr(999, 1000) < rat <= 1, 'sharpness')
    # the hard-gap integral int_0^inf min(1,(t/l)^5) l (l^2 + r) dl = (5/4) t^4 + (5/6) r t^2
    for _ in range(40):
        t = Fr(rnd.randint(1, 30), rnd.randint(1, 20))
        r = Fr(rnd.randint(0, 30), rnd.randint(1, 20))
        U = 50 * t
        lo1, hi1 = riemann(lambda l: l * (l * l + r), Fr(0), t, 64, True)
        lo2, hi2 = riemann(lambda l: t ** 5 * (1 / l ** 2 + r / l ** 4), t, U, 256, False)
        tail = t ** 5 * (1 / U + r / (3 * U ** 3))                 # exact integral of the decreasing tail on [U, inf)
        closed = Fr(5, 4) * t ** 4 + Fr(5, 6) * r * t ** 2
        record('G1b_gap', lo1 + lo2 + tail <= closed <= hi1 + hi2 + tail, 'gap integral')


# ---------------------------------------------------------------- G2: exponent bookkeeping
def check_G2():
    top = Fr(3, 16) if MUT != 'M6' else Fr(1, 4)
    for num in range(0, 64):
        beta = Fr(num, 256)
        p = max(Fr(4), 1 / (1 - 4 * beta))
        expo = [Fr(4), 5 - 4 * beta, 6 - 8 * beta, 7 - 16 * beta, 3 + p * (1 - 4 * beta)]
        record('G2_exponents', (min(expo) >= 4) == (beta <= top), 'beta=%s' % beta)
        if beta > Fr(3, 16):
            record('G2_dominant', min(expo) == 7 - 16 * beta, 'dominant')


def main():
    rnd = random.Random(20261005)
    nF = check_F(rnd)
    nD = check_D1(rnd)
    check_T1(rnd)
    check_G1(rnd)
    check_G2()
    C = consts(Fr(1), Fr(1))
    summary = {
        'passed': not FAIL,
        'counts': dict(sorted(COUNT.items())),
        'fields_F': nF,
        'cases_D1': nD,
        'largest_ratios': {key: str(val.limit_denominator(10 ** 6)) for key, val in sorted(WORST.items())},
        'constants_k1': {key: str(C[key]) for key in ('K0', 'K2', 'K0_3', 'K1_3', 'K2_3', 'A1', 'A2', 'A3', 'A4',
                                                     'c0', 'c1', 'c2', 'c3', 'CB', 'Ce', 'Dh', 'Ch')},
    }
    out = json.dumps(summary, sort_keys=True) + '\n'
    if FAIL:
        sys.stderr.write('FAILED:\n' + '\n'.join(FAIL) + '\n')
        sys.stdout.write(out)
        sys.exit(1)
    sys.stdout.write(out)
    sys.exit(0)


if __name__ == '__main__':
    main()
```

```json
{"cases_D1": 4000, "constants_k1": {"A1": "67/48", "A2": "3", "A3": "217/24", "A4": "3", "CB": "16", "Ce": "28561/2304", "Ch": "134377/288", "Dh": "259/24", "K0": "167/192", "K0_3": "923/192", "K1_3": "945/128", "K2": "115/48", "K2_3": "127/16", "c0": "17/8", "c1": "4", "c2": "2", "c3": "361/24"}, "counts": {"D1_prop_D3": 4000, "F0_pins_exact": 42, "F1_cube_j0": 42, "F1_cube_j1": 42, "F1_cube_j2": 42, "F2_FW0_j0": 42, "F2_FW0_j1": 42, "F2_FW0_j2": 42, "F2_FW1": 42, "F2_FW2": 42, "F2_FW3": 42, "F2_FW4": 42, "F3_D2a2": 42, "F3_Da2": 42, "F3_a2": 42, "G1a_closed_form": 40, "G1a_inner_bound": 1500, "G1a_sharp": 1, "G1b_gap": 40, "G2_dominant": 15, "G2_exponents": 64, "T1_chain_rule": 300, "T1_frobenius": 475, "T1_pin_hessians": 300, "T1_qs_identity": 300}, "fields_F": 42, "largest_ratios": {"F1_cube_j0": "91380/301919", "F1_cube_j1": "288128/734877", "F1_cube_j2": "244111/463781", "F2_FW0_j0": "224500/243243", "F2_FW0_j1": "498925/521203", "F2_FW0_j2": "57600/59059", "F2_FW1": "920931/935618", "F2_FW2": "1000/1001", "F2_FW3": "639437/700617", "F2_FW4": "512000/551551", "F3_D2a2": "218700/321733", "F3_Da2": "153090/321733", "F3_a2": "273485/763036"}, "passed": true}
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_