"""Exact controls for lifetime note TL (CL-TL-SOFT-LAYER-20261006-v1).

Standard library only; exact rational arithmetic; deterministic; output identical under -O.
Usage: python3 -B -S tl_exact.py [--mutant M1..M10]
On success: one JSON line on stdout, exit 0.
On a failed control: nothing on stdout, 'FAILED: <group>' on stderr, exit 1.
On invalid arguments: usage on stderr, exit 2.
"""
import json
import random
import sys
from fractions import Fraction as F

USAGE = "usage: tl_exact.py [--mutant M1..M10]\n"
MUTANTS = {"M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"}


def parse(argv):
    if len(argv) == 0:
        return None
    if len(argv) == 2 and argv[0] == "--mutant" and argv[1] in MUTANTS:
        return argv[1]
    sys.stderr.write(USAGE)
    sys.exit(2)


MUT = parse(sys.argv[1:])


class Failed(Exception):
    pass


def need(cond, group):
    if not cond:
        raise Failed(group)


# ---------- small exact linear algebra ----------

def zeros(n, m):
    return [[F(0)] * m for _ in range(n)]


def eye(n):
    a = zeros(n, n)
    for i in range(n):
        a[i][i] = F(1)
    return a


def matmul(a, b):
    n, k, m = len(a), len(b), len(b[0])
    return [[sum((a[i][t] * b[t][j] for t in range(k)), F(0)) for j in range(m)] for i in range(n)]


def transpose(a):
    return [list(r) for r in zip(*a)]


def matvec(a, v):
    return [sum((a[i][j] * v[j] for j in range(len(v))), F(0)) for i in range(len(a))]


def dot(u, v):
    return sum((x * y for x, y in zip(u, v)), F(0))


def inverse(a):
    n = len(a)
    m = [list(a[i]) + list(eye(n)[i]) for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [x / piv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [row[n:] for row in m]


def det(a):
    n = len(a)
    m = [list(r) for r in a]
    d = F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            return F(0)
        if p != c:
            m[c], m[p] = m[p], m[c]
            d = -d
        d *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return d


def positive_definite(a):
    """Sylvester's criterion (exact)."""
    n = len(a)
    return all(det([row[:i] for row in a[:i]]) > 0 for i in range(1, n + 1))


def cayley(s):
    """Rational orthogonal matrix (I - S)(I + S)^{-1} for skew-symmetric S."""
    n = len(s)
    i = eye(n)
    return matmul([[i[r][c] - s[r][c] for c in range(n)] for r in range(n)],
                  inverse([[i[r][c] + s[r][c] for c in range(n)] for r in range(n)]))


RNG = random.Random(20261006)


def rat(lo, hi, den=12):
    return F(RNG.randint(lo * den, hi * den), den)


def random_case(m):
    s = zeros(m, m)
    for i in range(m):
        for j in range(i + 1, m):
            x = rat(-2, 2)
            s[i][j], s[j][i] = x, -x
    o = cayley(s)
    lam = sorted(F(RNG.randint(1, 40), RNG.randint(1, 9)) for _ in range(m))
    d = [[lam[i] if i == j else F(0) for j in range(m)] for i in range(m)]
    a = matmul(matmul(o, d), transpose(o))
    a = [[-x for x in row] for row in a]          # A = -O diag(lam) O^T < 0
    gamma = [rat(-3, 3) for _ in range(m)]
    if all(x == 0 for x in gamma):
        gamma[0] = F(1)
    eta = [rat(-3, 3) for _ in range(m)]
    bsym = zeros(m, m)
    for i in range(m):
        for j in range(i, m):
            x = rat(-3, 3)
            bsym[i][j] = bsym[j][i] = x
    return o, lam, a, gamma, eta, bsym


def opnorm_at_least(lam_val, b):
    """True iff lam_val <= ||B||_op, tested exactly: lam_val > ||B|| iff lam I -+ B are both PD."""
    n = len(b)
    plus = [[(lam_val if i == j else F(0)) - b[i][j] for j in range(n)] for i in range(n)]
    minus = [[(lam_val if i == j else F(0)) + b[i][j] for j in range(n)] for i in range(n)]
    return not (positive_definite(plus) and positive_definite(minus))


# ---------- T1: (1.1) ----------

def t1():
    n = 0
    for m in (1, 2, 3):
        for _ in range(40):
            o, lam, a, gamma, eta, bsym = random_case(m)
            ainv = inverse(a)
            lmin, lmax = lam[0], lam[-1]
            q = dot(gamma, matvec(ainv, gamma))
            absq = -q
            need(absq > 0, "T1_matrix_bounds")
            v = matvec(ainv, gamma)
            g2 = dot(v, v)                        # Gamma-tilde squared
            delta = det(a)
            need(absq <= dot(gamma, gamma) / lmin, "T1_matrix_bounds")
            if MUT == "M2":
                need(g2 <= absq * lmin, "T1_matrix_bounds")
            else:
                need(g2 <= absq / lmin, "T1_matrix_bounds")
            a2 = lmax ** (2 * m - 2)
            need(delta ** 2 <= lmin ** 2 * a2, "T1_matrix_bounds")
            need(delta ** 2 * g2 <= lmin * absq * a2, "T1_matrix_bounds")
            need(delta ** 2 * g2 ** 2 <= absq ** 2 * a2, "T1_matrix_bounds")
            n += 5
    return n


# ---------- T2: the radial parametrization ----------

def t2():
    n = 0
    # polynomial identity: z = f4 + 3 rho^2 mu, dz/drho * rho = 2 (z - f4), coefficients in rho
    for mu in (F(1, 3), F(5, 2), F(7)):
        z_minus_f4 = [F(0), F(0), 3 * mu]               # coefficients of rho^0, rho^1, rho^2
        dz = [F(0), 6 * mu]                             # d/drho
        if MUT == "M1":
            lhs = [F(0)] + [x / 2 for x in dz]          # (z - f4)/rho version of the derivative
        else:
            lhs = [F(0)] + dz                           # rho * dz/drho
        rhs = [2 * x for x in z_minus_f4]
        need(lhs == rhs, "T2_radial")
        n += 1
    for m in (1, 2, 3):
        for _ in range(30):
            o, lam, a, gamma, eta, bsym = random_case(m)
            ainv = inverse(a)
            omega = [rat(-2, 2) for _ in range(m)]
            if all(x == 0 for x in omega):
                omega[0] = F(1)
            rho = F(RNG.randint(1, 30), 7)
            f5 = rat(-3, 3)
            g = [rho * x for x in omega]
            q1 = f5 / 120 - dot(eta, matvec(ainv, g)) / 12 + dot(g, matvec(ainv, matvec(bsym, matvec(ainv, g)))) / 8
            c0 = f5 / 120
            c1 = -dot(eta, matvec(ainv, omega)) / 12
            c2 = dot(omega, matvec(ainv, matvec(bsym, matvec(ainv, omega)))) / 8
            need(q1 == c0 + c1 * rho + c2 * rho ** 2, "T2_radial")
            v = matvec(ainv, g)
            g2 = dot(v, v)
            need((c1 * rho) ** 2 <= dot(eta, eta) * g2 / 144, "T2_radial")
            # |c2| rho^2 <= ||B|| Gamma^2 / 8, i.e. 8|c2 rho^2| / Gamma^2 <= ||B||_op (exact test)
            if g2 > 0 and c2 != 0:
                need(opnorm_at_least(8 * abs(c2) * rho ** 2 / g2, bsym), "T2_radial")
            # (3.2): dQ1/dz = (c1 + 2 c2 rho) / (6 rho mu) = (c1 rho + 2 c2 rho^2) / (2 (z - f4))
            mu = dot(omega, matvec([[-x for x in row] for row in ainv], omega))
            need(mu > 0, "T2_radial")
            zf = 3 * rho ** 2 * mu
            need((c1 + 2 * c2 * rho) / (6 * rho * mu) == (c1 * rho + 2 * c2 * rho ** 2) / (2 * zf), "T2_radial")
            # mu <= |omega|^2 / lambda
            need(mu <= dot(omega, omega) / lam[0], "T2_radial")
            n += 6
    return n


# ---------- T3: Lemma W2's slab constants (kappa = 1 by scaling) ----------

def t3():
    n = 0
    bound_f4 = F(17) if MUT == "M6" else F(13)
    for x0 in (F(24), F(72)):
        for i in range(-26, 27):
            f4 = bound_f4 * F(i, 26)
            lo, hi = x0 - 4 - f4, x0 + 4 - f4
            need(lo >= 7, "T3_slab")
            need(hi / lo <= F(41, 7), "T3_slab")
            need(hi / lo <= F(15, 7), "T3_slab")
            n += 3
    return n


# ---------- T4: constants of sections 2 and 3 ----------

def pl_ge(a, b, c):
    """max(a, 3x - b) >= (1 + x)/c for every x >= 0 (exact): the difference is convex and piecewise linear,
    decreasing before the kink x* = (a + b)/3, so it suffices to check x = 0, x = x* and the final slope."""
    g = lambda x: max(a, 3 * x - b) - (1 + x) / c
    xs = (a + b) / 3
    return g(F(0)) >= 0 and (xs <= 0 or g(xs) >= 0) and 3 - 1 / c >= 0

def t4():
    ce = F(1, 200)
    checks = []
    checks.append(1 - 36 * ce / 11 > F(49, 50))
    checks.append(36 * ce < F(1, 5))                                  # edge in (23.8, 24.2)
    checks.append(F(36 * 72, 11) <= 236)
    checks.append((F(5184) - F(48) ** 2) / 144 == 20 and 12 * ce < 20)
    kink = F(1728, 72)
    if MUT == "M8":
        kink = F(12)
    checks.append(kink == 24 and kink * ce <= F(12, 100))
    checks.append(F(242, 10) / 72 <= F(1, 2))                         # |w0'| <= kappa Delta^2 / 2
    checks.append(F(5184) + 1728 * ce < F(73) ** 2)                   # support |z| < 73 kappa
    checks.append(F(73 + 12, 3) == F(85, 3) and F(28 + 13, 3) == F(41, 3))
    lower_edge = F(11) if MUT != "M3" else F(12)
    checks.append(F(23) - 12 >= lower_edge)                           # z - f4 >= 11 kappa on the edge range
    checks.append(440 * 72 == 31680 and F(175, 4) <= 44)
    checks.append(131 ** 3 >= 175 ** 2 * 72)
    checks.append(36 + 12 * ce <= 37)                                # the constant 37 of (2.2)
    # piecewise-linear tail bounds (kappa = 1): max(a, 3x - b) >= (1 + x)/c for all x >= 0
    window_a = F(9) if MUT == "M10" else F(11)
    checks.append(pl_ge(window_a, F(73), F(3)))                      # Part F, the whole window
    checks.append(pl_ge(F(11), F(25), F(3)))                         # Part F, near the edges
    checks.append(pl_ge(F(13), F(25), F(2)))                         # Proposition RW, edge set, |f4| > 13 kappa
    for c in checks:
        need(c, "T4_constants")
    return len(checks)


# ---------- T5: exponent ledgers ----------

def t5():
    n = 0
    # Lemma W2 rows, kappa^a lambda^s -> kappa^(a-2-s); second differences need <= kappa^1
    w2_second = [
        (1, 2), (2, 1), (3, 0),                 # RW edge table: zeta^2 row; also (3.6) with (3.4)
        (2, 2), (F(7, 2), F(1, 2)),             # RW edge table: r^2 (1 + Gamma)^3 / kappa row
        (2, 1), (3, 0),                         # RW edge table: r^2 (1 + Gamma)^2 / (lambda kappa) row
        (1, 2), (3, 0),                         # RW edge table: eps^2 / kappa^2 row
    ]
    for a, s in w2_second:
        need(F(a) - 2 - F(s) <= 1, "T5_exponent_tables")
        n += 1
    # Lemma W2 rows for the first difference (3.7), first term: kappa^2 Delta^2 Qhat with (3.4); need <= kappa^0
    w2_first = [(2, 2), (F(5, 2), F(3, 2)), (3, 1)]
    if MUT == "M9":
        w2_first = [(2, 2), (F(5, 2), F(3, 2)), (3, 0)]
    for a, s in w2_first:
        need(F(a) - 2 - F(s) <= 0, "T5_exponent_tables")
        n += 1
    # Lemma W1 rows, kappa^a lambda^s -> kappa^(a-1-s)
    w1_second = [(0, 2), (1, 1), (2, 0)]                 # Delta^2 Qhat^2 terms (r^2 factor): need <= kappa^1
    for a, s in w1_second:
        need(F(a) - 1 - F(s) <= 1, "T5_exponent_tables")
        n += 1
    w1_first = [(1, 2), (F(3, 2), F(3, 2)), (2, 1)]      # kappa Delta^2 Qhat terms (r factor): need <= kappa^0
    for a, s in w1_first:
        need(F(a) - 1 - F(s) <= 0, "T5_exponent_tables")
        n += 1
    # bad-event terms r^a kappa^b must be <= r^2 max(1, kappa) on 1 <= kappa <= 1/r
    bad = [(3, 2), (F(5, 2), F(-1, 2)), (2, 0), (2, 1), (3, 0), (3, 2), (4, 2), (2, -1)]
    for a, b in bad:
        need(F(a) >= 2 and F(b) <= F(a) - 1, "T5_exponent_tables")
        n += 1
    # brute-force confirmation on a grid of (r, kappa), for the integral exponents
    for a, b in bad:
        if F(a).denominator != 1 or F(b).denominator != 1:
            continue
        for r in (F(1, 10), F(1, 100), F(1, 1000)):
            for kap in (F(1), F(1) / (7 * r), F(1) / r):
                val = r ** int(F(a)) * kap ** int(F(b))
                need(val <= r ** 2 * max(F(1), kap), "T5_exponent_tables")
                n += 1
    return n


# ---------- T6: the corollaries ----------

def int_exp(p, lo, hi):
    """l-exponent of the integral of r^p over [l^lo, l^hi] (lo > hi >= 0, so l^lo < l^hi) as l -> 0;
    lo = None means the lower limit 0 (needs p > -1), hi = None means the upper limit +infinity (needs p < -1)."""
    if p > -1:
        need(hi is not None, "T6_corollaries")
        return hi * (p + 1)
    need(p < -1 and lo is not None, "T6_corollaries")
    return lo * (p + 1)


def t6():
    n = 0
    # TL1: k >= 1 part, int_0^{l^{1/3}} C r^4 / l dr
    need(-1 + int_exp(F(4), None, F(1, 3)) == F(2, 3), "T6_corollaries")
    # TL1: the error of (TL) on [l^{1/3}, l^{1/4}]: r^2 and l r^{-2}
    need(int_exp(F(2), F(1, 3), F(1, 4)) == F(3, 4), "T6_corollaries")
    need(1 + int_exp(F(-2), F(1, 3), F(1, 4)) == F(2, 3), "T6_corollaries")
    # TL1: the missing piece l^{1/4} int_0^{l^{1/12}} s^4 ds
    need(F(1, 4) + int_exp(F(4), None, F(1, 12)) == F(2, 3), "T6_corollaries")
    n += 4
    # the #296 tail: l^{-1/4} int |E_l| kappa^{-5/4}; |E_l| <= (l/kappa)^{1/2}(1 + kappa) or C/kappa.
    # Work with kappa = l^{-x}: the cut kappa = l^{-1/3}.
    pre = F(-1, 4)
    near1 = (pre + F(1, 2), F(-1, 2) - F(5, 4))          # (l-exponent, kappa-exponent) = (1/4, -7/4)
    near2 = (pre + F(1, 2), F(1, 2) - F(5, 4))           # (1/4, -3/4)
    far = (pre, F(-1) - F(5, 4))                         # (-1/4, -9/4)
    need(near1 == (F(1, 4), F(-7, 4)) and near2 == (F(1, 4), F(-3, 4)) and far == (F(-1, 4), F(-9, 4)), "T6_corollaries")
    # kappa^{-7/4} from kbar: kbar^{-3/4} (lower endpoint), times l^{1/4}
    # kappa^{-3/4} up to l^{-1/3}: (l^{-1/3})^{1/4}, times l^{1/4}; kappa^{-9/4} from l^{-1/3}: (l^{-1/3})^{-5/4}, times l^{-1/4}
    t2 = near2[0] + F(-1, 3) * (near2[1] + 1)
    t3 = far[0] + F(-1, 3) * (far[1] + 1)
    need(near1[1] + 1 == F(-3, 4) and t2 == F(1, 6) and t3 == F(1, 6), "T6_corollaries")
    n += 2
    # TL2: r = l^{3/10} y^{-1/10}, k = l^{1/10} y^{3/10}; exponents as (l, y)
    r = (F(3, 10), F(-1, 10))
    k = (F(1, 10), F(3, 10))
    kap = (k[0] - r[0], k[1] - r[1])
    if MUT == "M5":
        kap = (F(-1, 5), F(-2, 5))
    need(kap == (F(-1, 5), F(2, 5)), "T6_corollaries")
    need((kap[0] + r[0], kap[1] + r[1]) == k, "T6_corollaries")
    need((k[0] + 3 * r[0], k[1] + 3 * r[1]) == (F(1), F(0)), "T6_corollaries")      # l = k r^3
    need((3 * k[0] - r[0], 3 * k[1] - r[1]) == (F(0), F(1)), "T6_corollaries")      # y = k^3 / r
    need((2 * k[0], 2 * k[1]) == (F(1, 5), F(3, 5)) and (-kap[0], -kap[1]) == (F(1, 5), F(-2, 5)), "T6_corollaries")
    need(F(1, 2) + 2 * k[0] == F(7, 10) and F(1, 2) - kap[0] == F(7, 10), "T6_corollaries")      # band remainder
    n += 6
    # TL3 ledger at rho = l^theta; rows derived from their integrals, and three rows recorded from cited sources
    theta = F(1, 5) if MUT == "M4" else F(2, 9)
    rows = {
        "cusp tail / J4": 2 + int_exp(F(-8), theta, None),                   # int_rho^inf (l/r^4)^2 dr
        "CE++ and C+": int_exp(F(1), F(1, 4), theta),                        # int_{l^{1/4}}^rho r dr
        "I_eld": F(4, 9),                                                    # recorded: #229 section 5
        "tail of A_rej": F(1, 4) + int_exp(F(-12), theta - F(1, 4), None),  # l^{1/4} int_{rho l^{-1/4}}^inf s^{-12} ds
        "Lemma U / TL1": min(3 * theta, F(2, 3)),                            # recorded rho^3 (#237 section 5); TL1 above
        "TL r^2": int_exp(F(2), F(1, 3), F(1, 4)),
        "A2 finite part": 2 - 5 * theta,                                     # recorded: #237 section 5
    }
    need(rows["cusp tail / J4"] == 2 - 7 * theta and rows["tail of A_rej"] == 3 - 11 * theta, "T6_corollaries")
    need(min(rows.values()) == F(4, 9), "T6_corollaries")
    need(sorted(k for k, v in rows.items() if v == F(4, 9)) == ["CE++ and C+", "I_eld", "cusp tail / J4"], "T6_corollaries")
    need(F(1, 5) <= theta <= F(1, 4), "T6_corollaries")
    need(2 * F(2, 9) == 2 - 7 * F(2, 9), "T6_corollaries")
    n += 5
    # SIDE24 relative remainders
    need(F(4, 9) + F(1, 3) == F(7, 9) and F(3, 7) + F(1, 3) == F(16, 21) and F(7, 9) > F(16, 21), "T6_corollaries")
    n += 1
    return n


# ---------- T7: Lemma Delta's mechanism on explicit models ----------

def poly_eval(c, x):
    return sum((ci * x ** i for i, ci in enumerate(c)), F(0))


def poly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def poly_add(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else F(0)) + (b[i] if i < len(b) else F(0)) for i in range(n)]


def poly_scale(a, s):
    return [s * x for x in a]


def poly_deriv(a):
    return [i * a[i] for i in range(1, len(a))] or [F(0)]


def poly_int(a, lo, hi):
    return sum((ci * (hi ** (i + 1) - lo ** (i + 1)) / (i + 1) for i, ci in enumerate(a)), F(0))


def shift(a, z0):
    """coefficients of p(z0 + h) in h."""
    out = [F(0)] * len(a)
    for i, ci in enumerate(a):
        # (z0 + h)^i
        term = [F(1)]
        for _ in range(i):
            term = poly_mul(term, [z0, F(1)])
        out = poly_add(out, poly_scale(term, ci))
    return out


def sup_abs(a, z0, h):
    """exact upper bound of |p| on [z0 - h, z0 + h]."""
    s = shift(a, z0)
    return sum((abs(ci) * h ** i for i, ci in enumerate(s)), F(0))


def t7():
    n = 0
    ce = F(1, 200)
    for kap in (F(1), F(3), F(10)):
        for f4 in (F(-12) * kap, F(0), F(12) * kap):
            for d2 in (F(1, 3), F(2)):
                for c0, c2p in ((F(1, 5), F(1, 50)), (F(-2, 7), F(1, 30)), (F(0), F(-1, 40))):
                    # Q1(z) = c0 + c2p (z - f4); Qhat = max |Q1| on [23k, 73k]
                    qend = [abs(c0 + c2p * (z - f4)) for z in (23 * kap, 73 * kap)]
                    qhat = max(qend)
                    if qhat == 0:
                        continue
                    lip = abs(c2p)
                    # density: positive polynomial on [23k, 73k]
                    rz = [F(3), F(1, 7) / kap, F(1, 50) / kap ** 2]
                    rz = [rz[0] - rz[1] * 24 * kap + rz[2] * (24 * kap) ** 2,
                          rz[1] - 2 * rz[2] * 24 * kap, rz[2]]               # 3 + (z-24k)/(7k) + (z-24k)^2/(50k^2)
                    w0 = [d2 * 5184 * kap ** 2 / 144, F(0), -d2 / 144]
                    beta = poly_scale([c0 - c2p * f4, c2p], 12 * kap * d2)
                    Fp = poly_mul(w0, rz)
                    r = ce * kap / qhat / 2
                    if r > 1 / kap:
                        r = 1 / kap

                    def ze(s):
                        return (24 * kap + 36 * s * (c0 - c2p * f4)) / (1 - 36 * s * c2p)

                    def s1(s):
                        integrand = poly_add(w0, poly_scale(beta, s))
                        return poly_int(poly_mul(integrand, rz), ze(s), 48 * kap)

                    for rr in (r, r / 2, r / 4):
                        dp, dm = ze(rr) - 24 * kap, ze(-rr) - 24 * kap
                        need(abs(dp) <= 36 * rr * qhat and abs(dm) <= 36 * rr * qhat, "T7_edge_model")
                        need(abs(dp) < kap / 5 and abs(dm) < kap / 5, "T7_edge_model")
                        q_at = lambda z: c0 + c2p * (z - f4)
                        if MUT == "M7":
                            s_pm = 36 * rr * (q_at(ze(rr)) + q_at(ze(-rr)))
                        else:
                            s_pm = 36 * rr * (q_at(ze(rr)) - q_at(ze(-rr)))
                        need(s_pm == dp + dm, "T7_edge_model")
                        need(abs(dp + dm) <= 36 * rr * lip * abs(dp - dm), "T7_edge_model")
                        second = s1(rr) + s1(-rr) - 2 * s1(F(0))
                        h = kap / 5
                        f_at = poly_eval(Fp, 24 * kap)
                        fprime_sup = sup_abs(poly_deriv(Fp), 24 * kap, h)
                        brz_sup = sup_abs(poly_mul(beta, rz), 24 * kap, h)
                        bound = f_at * abs(dp + dm) + (dp ** 2 + dm ** 2) / 2 * fprime_sup + rr * abs(dp - dm) * brz_sup
                        need(abs(second) <= bound, "T7_edge_model")
                        first = s1(rr) - s1(-rr)
                        w_sup = sup_abs(poly_add(w0, poly_scale(beta, rr)), 24 * kap, h)
                        rz_sup = sup_abs(rz, 24 * kap, h)
                        bint = poly_int(poly_scale(rz, 12 * kap * d2 * qhat), 23 * kap, 48 * kap)
                        need(abs(first) <= abs(dp - dm) * w_sup * rz_sup + 2 * rr * bint, "T7_edge_model")
                        n += 7
    return n


def main():
    groups = [("T1_matrix_bounds", t1), ("T2_radial", t2), ("T3_slab", t3), ("T4_constants", t4),
              ("T5_exponent_tables", t5), ("T6_corollaries", t6), ("T7_edge_model", t7)]
    counts = {}
    try:
        for name, fn in groups:
            counts[name] = fn()
    except Failed as e:
        sys.stderr.write("FAILED: %s\n" % e.args[0])
        sys.exit(1)
    out = {"object": "CL-TL-SOFT-LAYER-20261006-v1", "checks": counts, "total": sum(counts.values()), "passed": True}
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
