"""Exact controls for note LU (CL-LU-GAP-DIFFERENCE-20261006-v1).

Standard library only; exact rational arithmetic; deterministic; output identical under -O.
Usage: python3 -B -S lu_exact.py [--mutant M1..M7]
On success: one JSON line on stdout, exit 0.
On a failed control: nothing on stdout, 'FAILED: <group>' on stderr, exit 1.
On invalid arguments: usage on stderr, exit 2.
"""
import json
import random
import sys
from fractions import Fraction as F
from math import factorial

USAGE = "usage: lu_exact.py [--mutant M1..M7]\n"
MUTANTS = {"M1", "M2", "M3", "M4", "M5", "M6", "M7"}


def parse(argv):
    if len(argv) == 0:
        return None
    if len(argv) == 2 and argv[0] == "--mutant" and argv[1] in MUTANTS:
        return argv[1]
    sys.stderr.write(USAGE)
    sys.exit(2)


MUT = parse(sys.argv[1:])
RNG = random.Random(20261006)


class Failed(Exception):
    pass


def need(cond, group):
    if not cond:
        raise Failed(group)


# ---------- polynomials in (r, k): dict {(i, j): Fraction} for r^i k^j ----------

def padd(p, q, c=1):
    out = dict(p)
    for key, v in q.items():
        out[key] = out.get(key, 0) + c * v
        if out[key] == 0:
            del out[key]
    return out


def pmul(p, q):
    out = {}
    for (i1, j1), a in p.items():
        for (i2, j2), b in q.items():
            key = (i1 + i2, j1 + j2)
            out[key] = out.get(key, 0) + a * b
    return {key: v for key, v in out.items() if v != 0}


def pconst(c):
    return {(0, 0): F(c)} if c != 0 else {}


def rpow(n, c=1):
    return {(n, 0): F(c)} if c != 0 else {}


def pdiv_r(p):
    """divide by r; requires no r^0 term."""
    need(all(i >= 1 for (i, j) in p), "L1_shift")
    return {(i - 1, j): v for (i, j), v in p.items()}


def pdk(p):
    """derivative in k."""
    return {(i, j - 1): j * v for (i, j), v in p.items() if j >= 1}


def det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return padd(pmul(M[0][0], M[1][1]), pmul(M[0][1], M[1][0]), -1)
    out = {}
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        term = pmul(M[0][j], det(minor))
        out = padd(out, term, 1 if j % 2 == 0 else -1)
    return out


# ---------- pinned polynomial fields ----------
# A field of degree <= DEG in d variables (x, y_1, ..., y_m) is {alpha: P2}, alpha a d-tuple, coefficient = d^alpha g(0).

DEG = 6


def multi(d):
    out = []

    def rec(prefix, left, slots):
        if slots == 0:
            out.append(tuple(prefix))
            return
        for a in range(left + 1):
            rec(prefix + [a], left - a, slots - 1)
    rec([], DEG, d)
    return out


def e(d, i, n=1):
    v = [0] * d
    v[i] += n
    return tuple(v)


def add_idx(a, b):
    return tuple(x + y for x, y in zip(a, b))


def t_coef(j):
    """T_r = sum over odd j >= 3 of t_j r^(j-3) d_x^j f(0); t_j = (24 / 2^j) (j - 1) / j!."""
    return F(24, 2 ** j) * F(j - 1, factorial(j))


def pinned_field(d, target, odd_only, gd=0):
    """random rational free jets; pinned jets solved order by order, as polynomials in r.

    gd: the transverse gradient-difference target is gd * r (0 for every honest field; mutant M7 only)."""
    m = d - 1
    g = {}
    for a in multi(d):
        if odd_only and sum(a) % 2 == 0:
            continue
        g[a] = pconst(F(RNG.randint(-9, 9), RNG.randint(1, 4)))
    X = 0
    phi = lambda j: g.get(e(d, X, j), {})
    # T_r: phi_3 = 12 target - sum_{j odd >= 5} t_j r^(j-3) phi_j
    p3 = pconst(12 * target)
    for j in range(5, DEG + 1, 2):
        p3 = padd(p3, pmul(rpow(j - 3, t_coef(j)), phi(j)), -1)
    g[e(d, X, 3)] = p3
    # gradient difference, x-component: phi_2 = - sum_{j odd >= 3} (r/2)^(j-1)/j! phi_(j+1)
    p2 = {}
    for j in range(3, DEG, 2):
        p2 = padd(p2, pmul(rpow(j - 1, F(1, 2 ** (j - 1) * factorial(j))), phi(j + 1)), -1)
    if p2 or not odd_only:
        g[e(d, X, 2)] = p2
    elif e(d, X, 2) in g:
        del g[e(d, X, 2)]
    # average gradient, x-component: phi_1 = - sum_{j even >= 2} (r/2)^j/j! phi_(j+1)
    p1 = {}
    for j in range(2, DEG, 2):
        p1 = padd(p1, pmul(rpow(j, F(1, 2 ** j * factorial(j))), phi(j + 1)), -1)
    g[e(d, X, 1)] = p1
    for i in range(1, m + 1):
        psi = lambda j, i=i: g.get(add_idx(e(d, X, j), e(d, i)), {})
        # gradient difference, y_i-component: (d_i g(x_S) - d_i g(x_M)) / r = gd * r
        q1 = rpow(1, gd)
        for j in range(3, DEG, 2):
            q1 = padd(q1, pmul(rpow(j - 1, F(1, 2 ** (j - 1) * factorial(j))), psi(j)), -1)
        g[add_idx(e(d, X, 1), e(d, i))] = q1
        q0 = {}
        for j in range(2, DEG, 2):
            q0 = padd(q0, pmul(rpow(j, F(1, 2 ** j * factorial(j))), psi(j)), -1)
        g[e(d, i)] = q0
    return {a: v for a, v in g.items() if v}


def jet_at_axis(g, d, alpha_tail, sigma):
    """value at (sigma r/2, 0) of the derivative d^alpha_tail g: sum_a d_x^a d^tail g(0) (sigma r/2)^a / a!."""
    out = {}
    for a in range(DEG + 1):
        c = g.get(add_idx(e(d, 0, a), alpha_tail))
        if c:
            out = padd(out, pmul(rpow(a, F(sigma ** a, 2 ** a * factorial(a))), c))
    return out


def check_pins(g, d, target, gd=0):
    zero = tuple([0] * d)
    for v in range(d):
        tail = e(d, v)
        s_ = jet_at_axis(g, d, tail, 1)
        m_ = jet_at_axis(g, d, tail, -1)
        need(padd(s_, m_) == {}, "L1_shift")                     # average gradient 0
        need(padd(s_, m_, -1) == (rpow(2, gd) if v >= 1 else {}), "L1_shift")   # gradient difference 0 (gd r^2: M7)
    # T_r = (6/r^2)[f_x(x_M) + f_x(x_S) - 2 (f(x_S) - f(x_M))/r] = 12 target
    fx = padd(jet_at_axis(g, d, e(d, 0), 1), jet_at_axis(g, d, e(d, 0), -1))
    df = padd(jet_at_axis(g, d, zero, 1), jet_at_axis(g, d, zero, -1), -1)
    inner = padd(pmul(fx, rpow(1)), df, -2)                      # r [f_x + f_x] - 2 (f_S - f_M) = r^3 T_r / 6
    need(inner == pmul(rpow(3, F(12 * target, 6)), pconst(1)) if target else inner == {}, "L1_shift")


def hessian_at(g, d, sigma):
    return [[jet_at_axis(g, d, add_idx(e(d, p), e(d, q)), sigma) for q in range(d)] for p in range(d)]


def detK(g, d, sigma):
    return pdiv_r(det(hessian_at(g, d, sigma)))


def shift(f, mu, k_sign=1):
    g = {}
    for a in set(f) | set(mu):
        g[a] = padd(f.get(a, {}), pmul(mu.get(a, {}), {(0, 1): F(k_sign)}))
    return {a: v for a, v in g.items() if v}


def reflect(f):
    return {a: {key: (v if sum(a) % 2 == 0 else -v) for key, v in c.items()} for a, c in f.items()}


def num(p):
    """constant value of a P2 that must be a constant."""
    need(all(key == (0, 0) for key in p), "L1_shift")
    return p.get((0, 0), F(0))


def adj(M):
    n = len(M)
    if n == 1:
        return [[F(1)]]
    if n == 2:
        return [[M[1][1], -M[0][1]], [-M[1][0], M[0][0]]]
    raise ValueError


def mdet(M):
    if len(M) == 1:
        return M[0][0]
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def l1_l3():
    n1 = n3 = 0
    coef12 = F(11) if MUT == "M1" else F(12)
    db_coef = F(4) if MUT == "M3" else F(6)
    gd = 1 if MUT == "M7" else 0
    for d, trials in ((2, 3), (3, 2)):
        m = d - 1
        for _ in range(trials):
            f = pinned_field(d, 0, False, gd)
            mu = pinned_field(d, 1, True)
            check_pins(f, d, 0, gd)
            check_pins(mu, d, 1)
            need(all(sum(a) % 2 == 1 for a in mu), "L1_shift")
            g = shift(f, mu)
            KS, KM = detK(g, d, 1), detK(g, d, -1)
            A = [[num(f.get(add_idx(e(d, i), e(d, j)), {})) for j in range(1, d)] for i in range(1, d)]
            Delta = mdet(A)
            diff_k = padd(pdk(padd(KS, KM, -1)), pconst(coef12 * Delta), -1)
            need(all(v == 0 for (i, j), v in diff_k.items() if i <= 1), "L1_shift")
            sum_k = pdk(padd(KS, KM))
            need(all(v == 0 for (i, j), v in sum_k.items() if i == 0), "L1_shift")
            # reflection: det K_M(f~ - k mu) = det K_S(f + k mu)
            gt = shift(reflect(f), mu, 1 if MUT == "M2" else -1)
            need(detK(gt, d, -1) == KS, "L1_shift")
            n1 += 4
            # L3: r^1 coefficient of d/dk (det K_S + det K_M) at k = 0 equals 6 Delta_B - gamma^T A# gamma_mu
            B = [[num(f.get(add_idx(e(d, 0), add_idx(e(d, i), e(d, j))), {})) for j in range(1, d)] for i in range(1, d)]
            Ad = adj(A)
            DB = sum(Ad[i][j] * B[j][i] for i in range(m) for j in range(m))
            gam = [num(f.get(add_idx(e(d, 0, 2), e(d, i)), {})) for i in range(1, d)]
            gmu = [num(mu.get(add_idx(e(d, 0, 2), e(d, i)), {})) for i in range(1, d)]
            quad = sum(gam[i] * Ad[i][j] * gmu[j] for i in range(m) for j in range(m))
            c1 = sum(v for (i, j), v in sum_k.items() if i == 1 and j == 0)
            need(c1 == db_coef * DB - quad, "L3_drift")
            n3 += 1
    return n1, n3


# ---------- L2: (1.1) on rational samples ----------

def l2():
    n = 0
    for _ in range(4000):
        a = F(RNG.randint(-50, 50), RNG.randint(1, 9))
        b = F(RNG.randint(-50, 50), RNG.randint(1, 9))
        W = (-a) * b if (a < 0 < b) else F(0)
        x, y = (a + b) / 2, (b - a) / 2
        yp = y if y > 0 else F(0)
        G = yp * yp - x * x
        G = G if G > 0 else F(0)
        need(W == G, "L2_typed")
        n += 1
    return n


# ---------- L4: the ledgers ----------

def l4():
    n = 0
    # Theorem P+ at fixed rho: l^{3/4} (r^2 min(1,kappa)), l^{2/3} (fold scale), l (J3, J5), l^2 (J4, A2 finite part, cusp tail)
    rows = {"r2min": F(3, 4), "fold": F(2, 3), "J3": F(1), "J5": F(1), "J4": F(2), "A2": F(2), "tail": F(2)}
    least = min(rows.values())
    need(least == F(2, 3) and [k for k, v in rows.items() if v == least] == ["fold"], "L4_ledger")
    n += len(rows)
    lo = F(41, 200) if MUT == "M4" else F(5, 24)
    for s_ in (lo, F(7, 33), (lo + F(7, 33)) / 2):
        need(F(1, 5) < s_ < F(1, 4), "L4_ledger")
        theta = (1 - 4 * s_) / s_
        need(0 < theta < 1, "L4_ledger")
        r2 = {"fold etc.": F(2, 3), "EM.1 log": F(2, 3), "rho^8/l": 8 * s_ - 1, "U= r2min": F(3, 4), "TL- kappa r^2": F(3, 4),
              "l^2 rho^-6 log": 2 - 6 * s_, "l^3 rho^-11": 3 - 11 * s_, "rho^4 log (W+.3)": 4 * s_,
              "l^2 rho^-5": 2 - 5 * s_, "l^4 rho^-13": 4 - 13 * s_}
        need(min(r2.values()) == F(2, 3), "L4_ledger")
        n += len(r2)
    need(F(5, 7) == (1 - 4 * F(7, 33)) / F(7, 33) and F(4, 5) == (1 - 4 * F(5, 24)) / F(5, 24), "L4_ledger")
    need(F(2, 3) + F(1, 3) == 1, "L4_ledger")                       # SIDE24 relative remainder
    return n + 2


# ---------- L5: the two integrals of section 4 ----------

def l5():
    n = 0
    c43 = F(1) if MUT == "M5" else F(4, 3)
    for _ in range(300):
        a = F(RNG.randint(1, 40), 100)                  # l = a^4, l^{1/4} = a
        rho = a * F(RNG.randint(100, 900), 100)         # rho >= l^{1/4}
        # int_0^rho r^2 min(1, l/r^4) dr = a^3/3 + l (1/a - 1/rho)
        val = a ** 3 / 3 + a ** 4 * (1 / a - 1 / rho)
        need(val <= c43 * a ** 3, "L5_integrals")
        b = F(RNG.randint(1, 40), 100)                  # l = b^3, l^{1/3} = b, l^{2/3} = b^2
        # int_0^b r^4/l dr + int_b^inf l/r^2 dr = b^5/(5 b^3) + b^3 / b
        need(b ** 5 / (5 * b ** 3) + b ** 3 / b == F(6, 5) * b ** 2, "L5_integrals")
        n += 2
    return n


# ---------- L6: Step 2's exponents ----------

def l6():
    n = 0
    eexp = F(1, 2) if MUT == "M6" else F(3, 4)
    # (kappa eps0 + k)(kappa eps0 + r) <= 4 kappa r^{2e}; times P(C3) <= C eps0: kappa r^{3e} <= kappa r^2 needs 3e >= 2
    need(3 * eexp >= 2, "L6_exponents")
    # main term on C3: kappa^2 eps0^3 <= kappa r^2 (kappa <= 1)
    need(3 * eexp >= 2, "L6_exponents")
    # off the bad event: r * T <= r^{1 - 1/8} < eps0 / 2 for small r: 7/8 > e
    need(F(7, 8) > eexp, "L6_exponents")
    # exact spot checks on perfect powers: r = q^8, eps0 = q^{8e}
    for _ in range(200):
        q = F(RNG.randint(1, 30), 100)
        r = q ** 8
        eps0 = q ** int(8 * eexp)
        kap = F(RNG.randint(1, 100), 100)
        k = kap * r
        need((kap * eps0 + k) * (kap * eps0 + r) * eps0 <= 4 * kap * r ** 2, "L6_exponents")
        need(r * q ** -1 < eps0 / 2 or q > F(1, 2), "L6_exponents")
        n += 2
    # the slope condition on S = {|Delta| >= r(1 + |Delta_B|)}: |Delta|/12 - r|Delta_B|/24 >= |Delta|/24
    for _ in range(200):
        r = F(RNG.randint(1, 100), 1000)
        DB = F(RNG.randint(-50, 50), 7)
        Dl = r * (1 + abs(DB)) * F(RNG.randint(100, 500), 100)
        need(Dl / 12 - r * abs(DB) / 24 >= Dl / 24 and r * abs(DB) / (2 * Dl) <= F(1, 2), "L6_exponents")
        n += 1
    return n + 3


def main():
    counts = {}
    try:
        n1, n3 = l1_l3()
        counts["L1_shift"] = n1
        counts["L2_typed"] = l2()
        counts["L3_drift"] = n3
        counts["L4_ledger"] = l4()
        counts["L5_integrals"] = l5()
        counts["L6_exponents"] = l6()
    except Failed as ex:
        sys.stderr.write("FAILED: %s\n" % ex.args[0])
        sys.exit(1)
    out = {"object": "CL-LU-GAP-DIFFERENCE-20261006-v1", "checks": counts, "total": sum(counts.values()), "passed": True}
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
