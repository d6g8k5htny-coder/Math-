"""Exact controls for note C7 (CL-C7-ELDER-TWO-THIRDS-20261007-v1).

Standard library only; exact rational arithmetic; deterministic; output identical under -O.
Usage: python3 -B -S c7_exact.py [--mutant M1..M8]
On success: one JSON line on stdout, exit 0.
On a failed control: nothing on stdout, 'FAILED: <group>' on stderr, exit 1.
On invalid arguments: usage on stderr, exit 2.
"""
import json
import random
import sys
from fractions import Fraction as F

USAGE = "usage: c7_exact.py [--mutant M1..M8]\n"
MUTANTS = {"M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"}


def parse(argv):
    if len(argv) == 0:
        return None
    if len(argv) == 2 and argv[0] == "--mutant" and argv[1] in MUTANTS:
        return argv[1]
    sys.stderr.write(USAGE)
    sys.exit(2)


MUT = parse(sys.argv[1:])
RNG = random.Random(20261007)
HALF = F(1, 2)
QUARTER = F(1, 4)


class Failed(Exception):
    pass


def need(cond, group):
    if not cond:
        raise Failed(group)


def nonneg(hi=99, den=12):
    return F(RNG.randint(0, hi), RNG.randint(1, den))


# ---------- K1: the inequality behind (1.2), and its use ----------

def k1():
    g = "K1_minsum"
    n = 0
    for _ in range(3000):
        a, b, c, d = nonneg(), nonneg(), nonneg(), nonneg()
        rhs = min(a, d) + b + (0 if MUT == "M1" else c)
        need(min(a + b, c + d) <= rhs, g)
        n += 1
    for _ in range(300):
        # exact perfect powers: r = p^3, kappa = q^3 <= r, so r^{4/3} kappa^{2/3} = p^4 q^2
        p = F(1, RNG.randint(3, 12))
        q = p * F(RNG.randint(1, 9), 9)
        r, kap = p ** 3, q ** 3
        mu = F(RNG.randint(1, 200), 100)
        A = F(RNG.randint(1, 400), RNG.randint(1, 20))          # stands for C# Nbar^2
        R = p ** 4 * q ** 2
        need(kap <= r and R * R * R == r ** 4 * kap ** 2, g)
        # the expansion: mu (12 kappa + A r/mu)^2 = 144 mu kappa^2 + 24 A kappa r + A^2 r^2/mu
        lhs = mu * (12 * kap + A * r / mu) ** 2
        need(lhs == 144 * mu * kap ** 2 + 24 * A * kap * r + A * A * r * r / mu, g)
        need(lhs <= max(F(144), 24 * A, A * A) * (mu * kap ** 2 + kap * r + r * r / mu), g)
        # (1.2) with a = kappa, b = mu kappa^2 + R/mu, c = mu kappa^2 + kappa r, d = r^2/mu
        x1 = mu * kap ** 2 + kap + R / mu
        x2 = mu * kap ** 2 + kap * r + r * r / mu
        cterm = 0 if MUT == "M1" else mu * kap ** 2 + kap * r
        need(min(x1, x2) <= min(kap, r * r / mu) + mu * kap ** 2 + R / mu + cterm, g)
        n += 4
    return n


# ---------- K2: the shell sum (1.3) ----------

def k2():
    g = "K2_shells"
    n = 0
    many = 0
    for _ in range(500):
        r = F(RNG.randint(1, 100), 1000)                     # 0 < r <= 1/10
        kap = r * F(RNG.randint(1, 100), 100)                # 0 < kappa <= r
        j = RNG.randint(0, 6)
        y = F(2) ** (j + 1)                                  # y_j = C0 2^{j+1}, C0 = 1
        x = r * F(RNG.randint(1, 8), 8)                      # the lowest shell, of order r
        xs = []
        while x <= y:
            xs.append(x)
            x = 2 * x
        s = sum((min(x * kap, r * r) for x in xs), F(0))
        nplus = sum(1 for x in xs if x * kap > r * r)
        need(s <= 2 * y * kap, g)
        low = sum((x * kap for x in xs if x * kap <= r * r), F(0))
        need(low <= 2 * r * r, g)
        need(s <= r * r * (2 if MUT == "M2" else 2 + nplus), g)
        if nplus >= 1:
            need(F(2) ** (nplus - 1) * r * r < y * kap, g)    # n+ < log2(y kappa / r^2) + 1
            many += nplus >= 3
        m = 0                                                # least m with 2^m >= kappa / r^2
        while F(2) ** m < kap / (r * r):
            m += 1
        while F(2) ** (m - 1) >= kap / (r * r):
            m -= 1
        need(nplus <= j + 1 + max(m, 0), g)
        n += 5
    need(many >= 50, g)
    return n + 1


# ---------- K3: the substitution of section 2 and the integral 9/8 ----------

def deriv(fn):
    """fn = (P, Q) means P(t) + Q(t) log t, with P, Q Laurent polynomials {power: coefficient}."""
    p, q = fn
    out_p, out_q = {}, {}
    for e, c in p.items():
        if e != 0:
            out_p[e - 1] = out_p.get(e - 1, F(0)) + e * c
    for e, c in q.items():
        out_p[e - 1] = out_p.get(e - 1, F(0)) + c                # Q/t
        if e != 0:
            out_q[e - 1] = out_q.get(e - 1, F(0)) + e * c
    clean = lambda d: {e: c for e, c in d.items() if c != 0}
    return clean(out_p), clean(out_q)


def k3():
    g = "K3_integral"
    coef = 5 if MUT == "M3" else 6                            # the log coefficient of Upsilon~
    n = 0
    for _ in range(400):
        a = F(RNG.randint(1, 9), RNG.randint(10, 40))          # l = a^6
        lam = a ** 6
        t = F(RNG.randint(1, 60), RNG.randint(1, 20))
        if t == 1:
            t = F(3, 2)
        r = a * t                                               # r = l^{1/6} t
        kap = lam / r ** 4
        need(r * kap == lam / r ** 3 == a ** 3 * t ** -3, g)    # r kappa = l^{1/2} t^{-3}
        need(r ** 3 == a ** 3 * t ** 3, g)                      # r^3 = l^{1/2} t^3
        need(kap / r ** 2 == lam / r ** 6 == t ** -6, g)        # kappa / r^2 = t^{-6}
        need(r ** -3 * (r * kap) == t ** -6, g)                 # first entry of r^{-3} Upsilon
        need(kap / r ** 2 == (1 / t) ** coef, g)               # log(kappa/r^2) = coef log(1/t)
        s = F(RNG.randint(1, 9), RNG.randint(10, 20))           # r = s^3: r^2 kappa^{2/3} = l^{2/3} r^{-2/3}
        rr = s ** 3
        kk = lam / rr ** 4
        need(rr ** 2 * (a ** 4 / s ** 8) == a ** 4 * s ** -2 and (a ** 4 / s ** 8) ** 3 == kk ** 2, g)
        n += 6
    for _ in range(200):
        yv = F(RNG.randint(1, 1000), 1000)                      # y = t^6 in (0, 1]
        need(yv * (1 + (1 / yv - 1)) == 1, g)                   # the bound behind y(1 + log(1/y)) <= 1
        n += 1
    # int_0^1 t^3 (1 + c log(1/t)) dt, through an exact antiderivative (P, Q): P + Q log t
    integrand = ({3: F(1)}, {3: F(-coef)})                       # t^3 - c t^3 log t
    anti = ({4: F(1, 4) + F(coef, 16)}, {4: F(-coef, 4)})
    need(deriv(anti) == integrand, g)
    need(all(e > 0 for e in anti[0]) and all(e > 0 for e in anti[1]), g)   # vanishes at t -> 0
    low = anti[0][4]                                              # value at t = 1 (log 1 = 0)
    tail_anti = ({-2: F(-1, 2)}, {})                              # int_1^inf t^{-3} dt
    need(deriv(tail_anti) == ({-3: F(1)}, {}), g)
    tail = -tail_anti[0][-2]                                      # 0 - (-1/2)
    need(low == F(1, 4) + F(coef, 16), g)
    need(low + tail == F(9, 8), g)
    need(F(1, 4) + F(6, 16) == F(5, 8) and tail == HALF, g)
    return n + 6


# ---------- K4: Lemma D's case analysis on a discrete model ----------

GRID = [F(-3) + F(i, 8) for i in range(41)]                      # -3 .. 2, step 1/8
I_M = 20                                                         # X = -1/2
I_S = 28                                                         # X = 1/2


def escape(vals, kap):
    """(ii): a grid point X1 in [-3, 1/2) with g > 0 and g > -kappa on the closed interval between -1/2 and X1."""
    for step, stop in ((1, I_S), (-1, -1)):
        low = vals[I_M]
        i = I_M + step
        while i != stop:
            low = min(low, vals[i])
            if low <= -kap:
                break
            if vals[i] > 0:
                return True
            i += step
    return False


def trap(vals, kap):
    """(iii): X_L in [-3, -1/2), X_R in (-1/2, 2] with g < -kappa at both and g <= 0 between."""
    lo = I_M
    while lo - 1 >= 0 and vals[lo - 1] <= 0:
        lo -= 1
    hi = I_M
    while hi + 1 <= 40 and vals[hi + 1] <= 0:
        hi += 1
    left = any(vals[i] < -kap for i in range(lo, I_M))
    right = any(vals[i] < -kap for i in range(I_M + 1, hi + 1))
    return left and right


def k4():
    g = "K4_dichotomy"
    seen = {"escape": 0, "trap": 0, "alt1": 0, "alt2_only": 0}
    n = 0
    ties = MUT == "M8"                                           # M8: ties with 0 and -kappa allowed, i.e. (G) dropped
    for _ in range(4000):
        K = RNG.randint(3, 9)
        kap = F(RNG.randint(1, 20), RNG.randint(1, 20))
        inside = RNG.choice([60, 90, 97])                       # percent of grid values in the band
        vals = []
        for i in range(41):
            if i == I_M:
                vals.append(F(0))
                continue
            if i == I_S:
                vals.append(-kap)
                continue
            if abs(i - I_M) == 1:
                m = RNG.randint(-K, -1)                          # in (-kappa, 0): a local maximum at -1/2
            elif RNG.randint(1, 100) <= inside:
                m = RNG.randint(-K, 0 if ties else -1)           # in the band
            elif RNG.randint(0, 1):
                m = RNG.randint(0, 2 * K)                        # above 0
            else:
                m = RNG.randint(-3 * K, -K - 1)                  # below -kappa
            vals.append(kap * (m if ties else m + HALF) / K)     # without M8 never 0 or -kappa: ties excluded
        band = [(-kap <= v <= 0) for v in vals]
        if not ties:
            need(all(v != 0 and v != -kap for i, v in enumerate(vals) if i not in (I_M, I_S)), g)
        esc = escape(vals, kap)
        trp = False if MUT == "M4" else trap(vals, kap)
        alt1 = all(band[I_M:I_S + 1])
        alt2 = all(band[0:I_M + 1])
        if esc:
            seen["escape"] += 1
        elif trp:
            seen["trap"] += 1
        else:
            need(alt1 or alt2, g)
            if alt1:
                seen["alt1"] += 1
            else:
                seen["alt2_only"] += 1
        n += 1
    need(min(seen.values()) >= 25, g)
    # the tie witness: (G) cannot be dropped. kappa = 1; g(0) = -1 is a local minimum at the level of S,
    # g(1/8) = 1/2, g = -1/2 at the other grid points of (-1/2, 2] and at -5/8, g = -2 left of -5/8.
    one = F(1)
    wit = []
    for i, x in enumerate(GRID):
        if i == I_M:
            wit.append(F(0))
        elif i == I_S:
            wit.append(-one)
        elif x == 0:
            wit.append(-one)
        elif x == F(1, 8):
            wit.append(HALF)
        elif x > -HALF or x == F(-5, 8):
            wit.append(-HALF)
        else:
            wit.append(F(-2))
    need(not escape(wit, one) and not trap(wit, one), g)
    wband = [(-one <= v <= 0) for v in wit]
    need(not all(wband[I_M:I_S + 1]) and not all(wband[0:I_M + 1]), g)
    return n + 3


# ---------- K5: the window of section 4 (c) ----------

def quart(x):
    return (x * x - QUARTER) ** 2


def cub(x):
    return 2 * (x + HALF) ** 2 * (x - 1)


def ridge(x, kap, z):
    return kap * cub(x) + z / 24 * quart(x)


def ridge_d(x, kap, z):
    return 2 * kap * (2 * (x + HALF) * (x - 1) + (x + HALF) ** 2) + z / 24 * 4 * x * (x * x - QUARTER)


def k5():
    g = "K5_window"
    c0 = F(192) if MUT == "M5" else F(384)                     # 24 / (X^2 - 1/4)^2 at X = 0
    c1 = F(128, 3)                                               # 24 / (X^2 - 1/4)^2 at X = -1, over 9
    need(quart(F(0)) == F(1, 16) and quart(F(-1)) == F(9, 16), g)
    need(cub(F(0)) == -HALF and cub(F(-1)) == -1, g)
    need(F(-1) * quart(F(-1)) == F(-9, 16), g)
    n = 3
    hits = [0, 0]
    for _ in range(3000):
        kap = F(RNG.randint(1, 100), RNG.randint(1, 100))
        e2 = F(RNG.randint(0, 100), RNG.randint(1, 100))
        rq = F(RNG.randint(-100, 100), RNG.randint(1, 100))     # r Q_1
        z = F(RNG.randint(-2000, 2000), RNG.randint(1, 10)) * kap
        x = F(RNG.randint(-30, 30), 7)
        phi = z / (72 * kap)
        need(kap * (cub(x) + 3 * phi * quart(x)) == ridge(x, kap, z), g)
        need(ridge(-HALF, kap, z) == 0 and ridge(HALF, kap, z) == -kap, g)
        need(ridge_d(-HALF, kap, z) == 0 and ridge_d(HALF, kap, z) == 0, g)
        for delta in (-e2, F(0), e2, e2 * F(RNG.randint(-10, 10), 10)):
            g0 = ridge(F(0), kap, z) + delta                     # g_F(0)
            if -kap <= g0 <= 0:
                need(c0 * (-kap / 2 - e2) <= z <= c0 * (kap / 2 + e2), g)
                hits[0] += 1
            g1 = ridge(F(-1), kap, z) + rq * F(-1) * quart(F(-1)) + delta   # g_F(-1)
            if -kap <= g1 <= 0:
                need(c1 * (F(9, 16) * rq - e2) <= z <= c1 * (F(9, 16) * rq + kap + e2), g)
                hits[1] += 1
        # sharpness: the endpoints are attained at delta = -e2 (upper) and delta = +e2 (lower), at X = 0 and at X = -1
        zt = 384 * (kap / 2 + e2)
        need(ridge(F(0), kap, zt) - e2 == 0 and zt <= c0 * (kap / 2 + e2), g)
        zb = 384 * (-kap / 2 - e2)
        need(ridge(F(0), kap, zb) + e2 == -kap and zb >= c0 * (-kap / 2 - e2), g)
        zu = F(128, 3) * (F(9, 16) * rq + kap + e2)
        need(ridge(F(-1), kap, zu) + rq * F(-1) * quart(F(-1)) - e2 == 0 and zu <= c1 * (F(9, 16) * rq + kap + e2), g)
        zl = F(128, 3) * (F(9, 16) * rq - e2)
        need(ridge(F(-1), kap, zl) + rq * F(-1) * quart(F(-1)) + e2 == -kap and zl >= c1 * (F(9, 16) * rq - e2), g)
        need((c0 + c1) * (kap + 2 * e2) <= 427 * (kap + 2 * e2), g)
        n += 8
    need(min(hits) >= 200, g)
    need(F(384) + F(128, 3) <= 427 and F(1280, 3) == F(384) + F(128, 3), g)
    return n + 2


# ---------- K6: Proposition G0's exponents at kappa = c r^2 ----------

def k6():
    g = "K6_scale"
    bad = F(3) if MUT == "M6" else F(7, 2)                       # (kappa + r) r^{5/2} <= 2 r^{7/2}
    rows = {"bad": bad, "small_mu_log": F(7, 3) + F(2, 3) * 2, "large_mu": F(4)}
    need(rows["small_mu_log"] == F(11, 3), g)                    # r^{7/3} kappa^{2/3} = c^{2/3} r^{11/3}
    for e in rows.values():
        need(e - 3 > 0, g)                                       # o(r^3)
    need(F(1) + F(2) - 3 == 0, g)                                # eps r kappa = eps c r^3: the surviving term
    n = 5
    for _ in range(400):
        c = F(RNG.randint(1, 60), RNG.randint(1, 12))
        s = F(1, RNG.randint(2, 60))
        r = s * s                                                # r = s^2, so r^{5/2} = s^5
        if c * r > 1:
            continue
        kap = c * r * r
        k = c * r ** 3
        need(k == kap * r and k <= r * r and kap <= r, g)
        need((kap + r) * s ** 5 <= 2 * s ** 7, g)
        need(r * kap == c * r ** 3, g)
        need(r * r * (kap + r * r) == (c + 1) * r ** 4, g)
        n += 4
    return n


# ---------- K7: the ledgers ----------

def row_exp(spec, sig, g):
    """The exponent of l of one ledger row, derived from its integrand.

    spec = (p_kappa, p_k, p_r, side): the integrand kappa^p_kappa k^p_k r^p_r, with kappa = l r^{-4} and k = l r^{-3},
    integrated over [rho, inf) ('up'), [0, rho] ('down') or [l^{1/4}, inf) ('up4'), with rho = l^sigma.
    """
    p_kap, p_k, p_r, side = spec
    a = F(p_kap + p_k)                                           # the power of l in the integrand
    b = F(p_r - 4 * p_kap - 3 * p_k)                             # the power of r in the integrand
    if side == "down":
        need(b > -1, g)
        return a + (b + 1) * sig
    need(b < -1, g)
    if side == "up":
        return a + (b + 1) * sig
    need(side == "up4", g)
    return a + (b + 1) / 4


def k7():
    g = "K7_ledger"
    sig = F(5, 24) if MUT == "M7" else F(4, 19)
    # section 5's rows: (name, integrand, with a logarithm, stated exponent at sigma = 4/19)
    rows = [("U_on_rho_rhof_r2kappa", (1, 0, 2, "up"), False, F(15, 19)),     # Theorem U= on [rho, rho_f]: r^2 kappa
            ("U_on_rho_rhof_rk", (0, 1, 1, "up"), False, F(15, 19)),          # and r k
            ("TLm_kappa_r2", (1, 0, 2, "up4"), False, F(3, 4)),               # (TL-): kappa r^2 on [l^{1/4}, rho]
            ("TLm_r3_over_kappa", (-1, 0, 3, "down"), False, F(13, 19)),      # (TL-): r^3/kappa
            ("elder_cusp_tail", (3, 0, 0, "up"), False, F(13, 19)),          # A^eld <= C kappa^3 on [rho, inf)
            ("contact_5_0", (2, 2, 0, "up"), False, F(24, 19)),              # (5.0): kappa^2 k^2
            ("T_r0", (0, 0, 3, "down"), True, F(16, 19)),                    # (W+.3): r^3 log(2/r) on [0, rho]
            ("A2_finite_part", (0, 2, 0, "up"), False, F(18, 19)),           # the finite part of A_2: k^2
            ("Weld_rho_l15", (2, 0, 1, "up"), True, F(14, 19))]              # (W+.2) on [rho, l^{1/5}]: kappa^2 r log
    exps = [(name, row_exp(spec, sig, g), want) for name, spec, _lg, want in rows]
    n = len(rows)
    for _name, e, _want in exps:
        need(e > F(2, 3), g)                                     # every row of section 5 is o(l^{2/3})
        n += 1
    for _name, e, want in exps:
        need(e == want, g)
        n += 1
    th = (1 - 4 * sig) / sig
    need(th == F(3, 4) and 0 < th < 1, g)                        # Theorem TL- at theta = 3/4
    need(1 - 4 * sig == sig * F(3, 4), g)                        # kappa >= l rho^{-4} = rho^theta on [l^{1/4}, rho]
    need(F(1, 5) < sig < F(1, 4) and F(5, 24) < sig < F(7, 33), g)
    need(8 * sig - 1 == 3 - 11 * sig == F(13, 19), g)            # sigma = 4/19 balances rho^8/l and l^3 rho^{-11}
    need(F(9, 44) < F(7, 32), g)                                 # no sigma puts both at 3/4 or above
    n += 5
    # Corollary E1: note LU's ledger at sigma = 5/24, with the new row l^{2/3} in place of EM.1's l^{2/3} log(1/l)
    s5 = F(5, 24)
    lu = [("l23_fold_TL1_S2_187", None, False), ("new_row_theorem_E", None, False),
          ("TLm_r3_over_kappa", (-1, 0, 3, "down"), False), ("l34_U_TLm", (1, 0, 2, "up4"), False),
          ("Weld_rho_l15", (2, 0, 1, "up"), True), ("elder_cusp_tail", (3, 0, 0, "up"), False),
          ("T_r0", (0, 0, 3, "down"), True), ("A2_finite_part", (0, 2, 0, "up"), False),
          ("contact_5_0", (2, 2, 0, "up"), False)]
    ex = [(F(2, 3) if spec is None else row_exp(spec, s5, g), lg) for _name, spec, lg in lu]
    lu_table = [F(2, 3), F(2, 3), F(2, 3), F(3, 4), F(3, 4), F(17, 24), F(5, 6), F(23, 24), F(31, 24)]
    need(sorted(e for e, _ in ex) == sorted(lu_table), g)        # note LU's stated ledger, row by row
    need(min(e for e, _ in ex) == F(2, 3), g)
    need(all(e > F(2, 3) for e, lg in ex if lg), g)              # the least exponent carries no logarithm
    need(sorted(e for e, lg in ex if lg) == [F(3, 4), F(5, 6)], g)
    need(F(2, 3) + F(1, 3) == 1, g)                              # SIDE24's relative remainder O(l)
    return n + 5


def main():
    groups = [("K1_minsum", k1), ("K2_shells", k2), ("K3_integral", k3), ("K4_dichotomy", k4), ("K5_window", k5),
              ("K6_scale", k6), ("K7_ledger", k7)]
    counts = {}
    try:
        for name, fn in groups:
            counts[name] = fn()
    except Failed as ex:
        sys.stderr.write("FAILED: %s\n" % ex.args[0])
        sys.exit(1)
    out = {"object": "CL-C7-ELDER-TWO-THIRDS-20261007-v1", "checks": counts, "total": sum(counts.values()),
           "passed": True}
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
