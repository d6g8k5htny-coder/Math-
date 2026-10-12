"""Exact controls for note C3 (CL-C3-CANDIDATE-TWO-THIRDS-20261006-v1).

Standard library only; exact rational arithmetic; deterministic; output identical under -O.
Usage: python3 -B -S c3_exact.py [--mutant M1..M10]
On success: one JSON line on stdout, exit 0.
On a failed control: nothing on stdout, 'FAILED: <group>' on stderr, exit 1.
On invalid arguments: usage on stderr, exit 2.
"""
import json
import random
import sys
from fractions import Fraction as F

USAGE = "usage: c3_exact.py [--mutant M1..M10]\n"
MUTANTS = {"M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"}


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


def rat(lo=-9, hi=9, den=4):
    return F(RNG.randint(lo, hi), RNG.randint(1, den))


# ---------- small exact linear algebra ----------

def mat_mul(X, Y):
    return [[sum(X[i][t] * Y[t][j] for t in range(len(Y))) for j in range(len(Y[0]))] for i in range(len(X))]


def transpose(X):
    return [list(row) for row in zip(*X)]


def ident(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def inverse(X):
    n = len(X)
    M = [list(X[i]) + ident(n)[i] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if M[i][c] != 0)
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [v / piv for v in M[c]]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return [row[n:] for row in M]


def det(X):
    n = len(X)
    if n == 1:
        return X[0][0]
    return sum((-1) ** j * X[0][j] * det([row[:j] + row[j + 1:] for row in X[1:]]) for j in range(n))


def adj(X):
    n = len(X)
    if n == 1:
        return [[F(1)]]
    cof = [[(-1) ** (i + j) * det([row[:j] + row[j + 1:] for k, row in enumerate(X) if k != i]) for j in range(n)]
           for i in range(n)]
    return transpose(cof)


def cayley(m):
    """rational orthogonal matrix (I - S)(I + S)^{-1}, S skew."""
    S = [[F(0)] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1, m):
            S[i][j] = rat(-5, 5, 3)
            S[j][i] = -S[i][j]
    I = ident(m)
    return mat_mul([[I[i][j] - S[i][j] for j in range(m)] for i in range(m)],
                   inverse([[I[i][j] + S[i][j] for j in range(m)] for i in range(m)]))


# ---------- E1: the adjugate at the edge, (I.1) and (1.2) ----------

def e1():
    n = 0
    for m in (1, 2, 3):
        for _ in range(40):
            lam = sorted({rat(-12, 12, 3) for _ in range(m + 3)})[:m]
            if len(lam) < m:
                continue
            O = cayley(m)
            need(mat_mul(transpose(O), O) == ident(m), "E1_edge")
            A = mat_mul(mat_mul(O, [[lam[i] if i == j else F(0) for j in range(m)] for i in range(m)]), transpose(O))
            cols = [[O[i][j] for i in range(m)] for j in range(m)]
            e = cols[m - 1]
            lm = lam[m - 1]
            P = F(1)
            for j in range(m - 1):
                P *= lam[j]
            R = [[F(0)] * m for _ in range(m)]
            for j in range(m - 1):
                c = F(1)
                for i in range(m - 1 if MUT != "M1" else m):
                    if i != j:
                        c *= lam[i]
                for a in range(m):
                    for b in range(m):
                        R[a][b] += c * cols[j][a] * cols[j][b]
            Ad = adj(A)
            need(det(A) == lm * P, "E1_edge")
            need(Ad == [[P * e[a] * e[b] + lm * R[a][b] for b in range(m)] for a in range(m)], "E1_edge")
            g = [rat() for _ in range(m)]
            Bm = [[F(0)] * m for _ in range(m)]
            for a in range(m):
                for b in range(a, m):
                    Bm[a][b] = Bm[b][a] = rat()
            f4, k = rat(), rat(0, 9, 4)
            ge = sum(g[a] * e[a] for a in range(m))
            Bee = sum(e[a] * Bm[a][b] * e[b] for a in range(m) for b in range(m))
            gAg = sum(g[a] * Ad[a][b] * g[b] for a in range(m) for b in range(m))
            gRg = sum(g[a] * R[a][b] * g[b] for a in range(m) for b in range(m))
            trAB = sum(Ad[a][b] * Bm[b][a] for a in range(m) for b in range(m))
            trRB = sum(R[a][b] * Bm[b][a] for a in range(m) for b in range(m))
            need(gAg == P * ge * ge + lm * gRg and trAB == P * Bee + lm * trRB, "E1_edge")
            Y = f4 / 12 * det(A) - gAg / 4
            W0 = P * f4 / 12 - gRg / 4
            need(Y == P * (-ge * ge / 4) + lm * W0, "E1_edge")
            U = Y + 3 * k * trAB
            Ured = 3 * k * Bee - ge * ge / 4
            need(U == P * Ured + lm * (W0 + 3 * k * trRB), "E1_edge")
            n += 5
    return n


# ---------- E2: the layer integral (I.2) ----------

def e2():
    n = 0
    c23 = F(1, 2) if MUT == "M2" else F(2, 3)
    for _ in range(500):
        a = F(RNG.randint(0, 60), RNG.randint(1, 7))
        beta = F(RNG.randint(1, 60), RNG.randint(1, 7))
        lo = -a / beta
        val = (a * a * 0 - beta * beta * 0 / 3) - (a * a * lo - beta * beta * lo ** 3 / 3)   # antiderivative a^2 x - b^2 x^3/3
        need(val == c23 * a ** 3 / beta, "E2_layer")
        P = rat(-9, 9, 3) or F(1)
        Ured, kap = rat(), F(RNG.randint(1, 50), RNG.randint(1, 5))
        need(c23 * (abs(P) * abs(Ured)) ** 3 / (6 * kap * abs(P)) == P * P * abs(Ured) ** 3 / (9 * kap), "E2_layer")
        n += 2
    return n


# ---------- E3: the Gaussian-kernel jet laws (G.1) ----------

def dfact(n):
    out = 1
    for j in range(n, 0, -2):
        out *= j
    return out


def dC(alpha):
    """d^alpha of exp(-|z|^2/2) at 0."""
    out = F(1)
    for a in alpha:
        if a % 2:
            return F(0)
        out *= (-1) ** (a // 2) * dfact(a - 1)
    return out


def cov(L1, L2):
    """L = {alpha: coef}; Cov(sum c d^alpha f(0), sum c' d^beta f(0)) = sum c c' (-1)^|beta| d^{alpha+beta} C(0)."""
    s = F(0)
    for a, c in L1.items():
        for b, cc in L2.items():
            s += c * cc * (-1) ** sum(b) * dC(tuple(x + y for x, y in zip(a, b)))
    return s


def unit(d, i, n=1):
    v = [0] * d
    v[i] += n
    return tuple(v)


def add(*idx):
    return tuple(sum(t) for t in zip(*idx))


def condition(X, pins):
    """regression coefficients of the functionals X on the pins, and the conditional covariance."""
    Sp = [[cov(p, q) for q in pins] for p in pins]
    Spi = inverse(Sp)
    coefs = []
    for x in X:
        c = [cov(x, p) for p in pins]
        coefs.append([sum(c[j] * Spi[j][i] for j in range(len(pins))) for i in range(len(pins))])
    Sc = [[cov(x, y) - sum(coefs[a][i] * cov(pins[i], y) for i in range(len(pins))) for b, y in enumerate(X)]
          for a, x in enumerate(X)]
    return coefs, Sc


def e3():
    n = 0
    for d in (2, 3, 4):
        u = 0
        dirs = [{1: F(1)}]
        if d >= 3:
            dirs.append({1: F(3, 5), 2: F(4, 5)})
        grad = [{unit(d, j): F(1)} for j in range(d)]
        dgrad = [{add(unit(d, u), unit(d, j)): F(1)} for j in range(d)]
        f3 = {unit(d, u, 3): F(1)}
        pins = grad + dgrad + [f3]
        for e in dirs:
            ge = {}
            Bee = {}
            for j, cj in e.items():
                key = add(unit(d, u, 2), unit(d, j))
                ge[key] = ge.get(key, F(0)) + cj
                for l, cl in e.items():
                    key = add(unit(d, u), unit(d, j), unit(d, l))
                    Bee[key] = Bee.get(key, F(0)) + cj * cl
            pins_used = pins if MUT != "M3" else [p for p in pins if p != grad[u]]
            coefs, Sc = condition([ge, Bee], pins_used)
            need(Sc == [[F(2), F(0)], [F(0), F(2)]], "E3_jets")
            i3 = pins_used.index(f3)
            need(coefs[0][i3] == 0 and coefs[1][i3] == 0, "E3_jets")       # no dependence on the target 12k
            n += 2
        cf, Sv = condition([f3], grad + dgrad)
        need(Sv == [[F(6)]], "E3_jets")                                   # v(k)^T Cov^{-1} v(k)/2 = (12k)^2/12 = 12k^2
        need(F(12) ** 2 / (2 * Sv[0][0]) == 12, "E3_jets")
        n += 2
    return n


# ---------- E4: moments and the Gamma identity (G.3) ----------

def e4():
    n = 0
    s2 = F(2)                                                     # variance of gamma and of B
    mom = {0: F(1), 1: F(0), 2: s2, 3: F(0), 4: 3 * s2 ** 2, 5: F(0), 6: 15 * s2 ** 3}
    # E[(g^2/4 - 3kB)^3] = sum_j C(3,j) E[(g^2/4)^{3-j}] (-3k)^j E[B^j]; polynomial in k: {power: coef}
    binom = [1, 3, 3, 1]
    poly = {}
    c27 = 24 if MUT == "M4" else 27
    for j in range(4):
        cg = mom[2 * (3 - j)] / F(4) ** (3 - j)
        cb = mom[j] * (-3) ** j
        poly[j] = poly.get(j, F(0)) + binom[j] * cg * cb
    if MUT == "M4":
        poly[2] = poly[2] * F(c27, 27)
    poly = {p: c for p, c in poly.items() if c != 0}
    g0 = mom[6] / 64
    need(g0 == F(15, 8) and poly == {0: F(15, 8), 2: F(27)}, "E4_moments")
    a = F(12) ** 2 / (2 * F(6))                                   # the density factor e^{-a k^2}; 6 = Var(d_u^3 f | pins)
    b = poly[2] / g0                                              # e^{-a k^2} E[X^3]/g(0) = e^{-a k^2}(1 + b k^2)
    need(a == 12 and b == F(72, 5) and b == 6 * a / 5, "E4_moments")
    n += 2
    # The Gamma identity's bookkeeping, from the substitution t = a k^2 in int (e^{-ak^2}(1 + bk^2) - 1) k^p dk:
    # k = a^{-1/2} t^{1/2}, dk = (1/2) a^{-1/2} t^{-1/2} dt, so k^q dk = (1/2) a^{-q/2 - 1/2} t^{q/2 - 1/2} dt.
    p = F(-5, 3) - 1                                              # (C3)'s k^{-5/3} times the 1/k of (G.2)
    need(p == F(-8, 3), "E4_moments")
    sarg, apow = [], []
    for q in (p, p + 2):                                          # term 0: (e^{-t} - 1) k^p; term 1: b k^2 e^{-t} k^p
        sarg.append(q / 2 - F(1, 2) + 1)                          # int e^{-t} t^{s-1} dt = Gamma(s)
        apow.append(-q / 2 - F(1, 2))
    need(sarg == [F(-5, 6), F(1, 6)], "E4_moments")
    need(-1 < sarg[0] < 0 < sarg[1], "E4_moments")                # int (e^{-t} - 1) t^{s-1} dt = Gamma(s) needs -1 < s < 0
    need(sarg[1] == sarg[0] + 1 and apow[0] - apow[1] == 1 and apow[1] == F(-1, 6), "E4_moments")
    rec = sarg[0] if MUT == "M10" else 1 / sarg[0]                # Gamma(s0) = Gamma(s0 + 1)/s0
    need(rec == F(-6, 5), "E4_moments")
    ca, cb = F(1, 2) * rec, F(1, 2)                               # coefficient of Gamma(1/6) a^{-1/6}: ca*a + cb*b
    need(ca == F(-3, 5) and cb == F(1, 2), "E4_moments")
    need(ca * a + cb * b == 0, "E4_moments")                      # the bracket integrates to 0
    n += 7
    return n


# ---------- E5: the constants of (3.2) and (G.3) ----------

def e5():
    c = F(12, 8) if MUT == "M5" else F(12, 9)
    need(c * F(1, 64) == F(1, 48), "E5_constant")
    need(F(1, 48) / F(5, 24) == F(1, 10), "E5_constant")
    need(F(15) * F(2) ** 3 == 120 and F(120, 64) == F(15, 8), "E5_constant")
    need(F(1, 3) * F(1, 10) == F(1, 30), "E5_constant")                 # c3 = (J/3) int a1 = (J/30) int int F0
    need(F(1, 30) * F(25, 48) == F(5, 288), "E5_constant")              # d = 2: int int F0 = 25 sqrt3/(48 pi^2)
    need(F(1, 30) * F(125, 192) == F(25, 1152), "E5_constant")          # d = 3: int int F0 = 125 sqrt30/(192 pi^3)
    return 6


# ---------- E6: the domination of section 4 ----------

def e6():
    n = 0
    ex = 2 if MUT == "M6" else 3
    need(1 - ex < -1, "E6_domination")                                  # s * s^{-ex} integrable at infinity
    need(F(-1, 3) + F(-4, 3) == F(-5, 3), "E6_domination")              # s ds = (1/3) k^{-5/3} dk, s = k^{-1/3}
    for _ in range(400):
        t = F(RNG.randint(1, 30), 100)                                   # l = t^3, l^{1/3} = t
        rho = F(RNG.randint(1, 100), 100)
        s = F(RNG.randint(1, 400), 20)
        if s > rho / t:
            continue
        r, k = t * s, 1 / s ** 3
        kap = k / r
        need(kap == 1 / (t * s ** 4) and k == t ** 3 / r ** 3, "E6_domination")
        lhs = min(r, r * kap) + min(k, 1 / k)
        need(lhs <= 2 * min(F(1), s ** -ex), "E6_domination")
        n += 1
    return n + 2


# ---------- E7: the strip (Step 4): Schur complement and sign ----------

def e7():
    n = 0
    signs = 0
    for m in (1, 2, 3):
        s = (-1) ** m
        for _ in range(80):
            O = cayley(m)
            eta = F(RNG.randint(1, 8), 8)
            lam = sorted(-(eta + F(RNG.randint(0, 40), 10)) for _ in range(m - 1)) + [F(RNG.randint(1, 30), RNG.randint(1, 9))]
            AM = mat_mul(mat_mul(O, [[lam[i] if i == j else F(0) for j in range(m)] for i in range(m)]), transpose(O))
            t = F(RNG.randint(1, 5), RNG.randint(20, 60))              # sqrt(r), so r is a rational square (r <= 1/16)
            r = t * t
            alpha = -F(RNG.randint(1, 60), 10) if RNG.randint(0, 3) else rat()
            beta = [rat(-3, 3, 4) for _ in range(m)]
            K = [[alpha] + [t * x for x in beta]] + [[t * beta[i]] + AM[i] for i in range(m)]
            Ai = inverse(AM)
            sigma = alpha - r * sum(beta[i] * Ai[i][j] * beta[j] for i in range(m) for j in range(m))
            need(det(K) == det(AM) * sigma, "E7_strip")                 # Schur: det K_M = det A_M * sigma_M
            need(det(AM) * s < 0, "E7_strip")                          # one positive eigenvalue: sign -s
            bound = alpha + (F(0) if MUT == "M7" else r * sum(x * x for x in beta) / eta)
            need(sigma <= bound, "E7_strip")
            n += 3
            if bound < 0:
                mM = det(K) / r
                need(s * mM > 0, "E7_strip")                            # frak a = s m_M > 0
                bb = rat()
                x, y = (s * mM + bb) / 2, (bb - s * mM) / 2
                need(abs(x) >= y, "E7_strip")                           # so |x| >= y: the strip is in the layer
                n += 2
                signs += 1
    need(signs >= 100, "E7_strip")
    return n + 1


# ---------- E8: the expansion (2.3) ----------

def e8():
    n = 0
    for s in (1, -1):
        for _ in range(150):
            P = -s * F(RNG.randint(1, 40), RNG.randint(1, 9))          # sign P = -s on the edge set
            lam = -F(RNG.randint(1, 40), RNG.randint(1, 9))            # lambda < 0
            U, W, V = rat(), rat(), rat()
            kap, r = F(RNG.randint(1, 50), RNG.randint(1, 5)), F(1, RNG.randint(2, 50))
            ep, em = rat(-3, 3, 9), rat(-3, 3, 9)
            x = s * (P * U + lam * W) + ep
            y = 6 * kap * s * lam * P + r * s * V + em
            a, beta = abs(P) * abs(U), 6 * kap * abs(P)
            need(s * lam * P == abs(lam) * abs(P), "E8_cross")
            cross = 2 * (s if MUT == "M8" else 1) * P * U * lam * W
            rho = (cross + lam * lam * W * W - 2 * beta * abs(lam) * (r * s * V + em) - (r * s * V + em) ** 2
                   + 2 * s * (P * U + lam * W) * ep + ep * ep)
            need(x * x - y * y == a * a - beta * beta * lam * lam + rho, "E8_cross")
            need(abs(2 * s * (P * U + lam * W) * ep + ep * ep) <= 2 * (a + abs(lam * W)) * abs(ep) + ep * ep, "E8_cross")
            n += 3
    return n


# ---------- E9: the bound on rho in section 3 ----------

def e9():
    n = 0
    for big in (False, True):
        for _ in range(150):
            P = rat(-9, 9, 3) * (F(10) ** 6 if big else 1)
            ge, W0 = rat(), rat()
            kap = F(RNG.randint(4, 400), 4)                            # kappa >= 1
            if ge == 0:
                continue
            lam = -ge * ge / (12 * kap) * F(RNG.randint(0, 12), 12)     # |lambda| <= ge^2/(12 kappa)
            Y = P * (-ge * ge / 4) + lam * W0
            a = abs(P) * ge * ge / 4
            rho = -P * ge * ge * lam * W0 / 2 + lam * lam * W0 * W0
            need(Y * Y == a * a + rho, "E9_tail")
            mid = abs(P) * ge ** 4 * abs(W0) / (24 * kap) + ge ** 4 * W0 * W0 / (144 * kap * kap)
            fac = F(1) if MUT == "M9" else 1 + abs(P)
            need(abs(rho) <= mid <= fac * (1 + ge * ge) ** 2 * (1 + abs(W0)) ** 2 / kap, "E9_tail")
            n += 2
    # the referee's instance: ge = W0 = 1, lambda = -1/(12 kappa), |P| = 10^6, kappa = 1
    P, ge, W0, kap = F(10) ** 6, F(1), F(1), F(1)
    lam = -F(1, 12)
    rho = -P * ge * ge * lam * W0 / 2 + lam * lam * W0 * W0
    fac = F(1) if MUT == "M9" else 1 + abs(P)
    need(abs(rho) <= fac * (1 + ge * ge) ** 2 * (1 + abs(W0)) ** 2 / kap, "E9_tail")
    return n + 1


def main():
    groups = [("E1_edge", e1), ("E2_layer", e2), ("E3_jets", e3), ("E4_moments", e4), ("E5_constant", e5),
              ("E6_domination", e6), ("E7_strip", e7), ("E8_cross", e8), ("E9_tail", e9)]
    counts = {}
    try:
        for name, fn in groups:
            counts[name] = fn()
    except Failed as ex:
        sys.stderr.write("FAILED: %s\n" % ex.args[0])
        sys.exit(1)
    out = {"object": "CL-C3-CANDIDATE-TWO-THIRDS-20261006-v1", "checks": counts, "total": sum(counts.values()),
           "passed": True}
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
