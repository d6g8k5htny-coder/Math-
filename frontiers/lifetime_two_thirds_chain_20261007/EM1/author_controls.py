"""Exact controls for addendum EM.1 (CL-EM1-BAD-REGION-20261006-v1).

Standard library only; exact rational arithmetic; deterministic; output identical under -O.
Usage: python3 -B -S em1_exact.py [--mutant M1..M8]
On success: one JSON line on stdout, exit 0.
On a failed control: nothing on stdout, 'FAILED: <group>' on stderr, exit 1.
On invalid arguments: usage on stderr, exit 2.
"""
import json
import random
import sys
from fractions import Fraction as F

USAGE = "usage: em1_exact.py [--mutant M1..M8]\n"
MUTANTS = {"M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"}


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


def rat(lo, hi, den=12):
    return F(RNG.randint(lo * den, hi * den), den)


def matmul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))] for i in range(len(X))]


def transpose(X):
    return [list(r) for r in zip(*X)]


def rot(t):
    """a rational rotation of the plane (Pythagorean parametrization)."""
    c = (1 - t * t) / (1 + t * t)
    s = 2 * t / (1 + t * t)
    return [[c, -s], [s, c]]


def quad(v, M):
    return sum(v[i] * M[i][j] * v[j] for i in range(len(v)) for j in range(len(v)))


# ---------- B1: the shear on typed pairs: |tau|^2 <= q_D / mu < -a / mu ----------

def b1():
    n = 0
    abound = F(6) if MUT == "M1" else F(7)
    thr = F(1) if MUT == "M7" else F(7)                # (2.1): r |tau| <= 1 once mu >= 7 N r^2
    # |a~| <= 6 kappa + N/12 <= 7 N for kappa <= 1 <= N (#220 (H.1))
    for kap in (F(1), F(1, 2), F(1, 1000)):
        for NB in (F(1), F(3, 2), F(10)):
            need(6 * kap + NB / 12 <= abound * NB, "B1_tau")
            n += 1
    acc = 0
    for _ in range(3000):
        m = RNG.choice((1, 2))
        mus = sorted(F(RNG.randint(1, 400), 100) for _ in range(m))   # eigenvalues of -D
        if m == 1:
            R = [[F(1)]]
        else:
            R = rot(F(RNG.randint(-30, 30), 11))
        negD = matmul(matmul(R, [[mus[i] if i == j else F(0) for j in range(m)] for i in range(m)]), transpose(R))
        negDinv = matmul(matmul(R, [[1 / mus[i] if i == j else F(0) for j in range(m)] for i in range(m)]), transpose(R))
        bt = [rat(-3, 3) for _ in range(m)]
        at = rat(-8, 2)
        qD = quad(bt, negDinv)
        s = -at - qD                                   # s = b^T D^{-1} b - a~ = -q_D - a~
        if s <= 0:
            continue
        acc += 1
        tau = [sum(negDinv[i][j] * bt[j] for j in range(m)) for i in range(m)]   # tau = (-D)^{-1} b~
        tau2 = sum(x * x for x in tau)
        mu = mus[0]
        need(tau2 * mu <= qD and qD < -at, "B1_tau")
        # check (-D) tau = b~ exactly
        need(all(sum(negD[i][j] * tau[j] for j in range(m)) == bt[i] for i in range(m)), "B1_tau")
        # r |tau| <= 1 once mu >= 7 N r^2 and |a~| <= 7 N
        NB = max(F(1), abs(at) / 7)
        r = F(1, 10) * F(RNG.randint(1, 100), 100)
        if mu >= thr * NB * r * r:
            need(r * r * tau2 <= 1, "B1_tau")
            n += 1
        n += 2
    # boundary witnesses: m = 1, beta~ along the soft direction, s = 10^-6, |a~| = 7 N, mu = 7 N r^2 (N = 1)
    for i in range(1, 40):
        r = F(1, 10 * i)
        mu = thr * r * r
        qD = 7 - F(1, 10 ** 6)
        at = -qD - F(1, 10 ** 6)
        tau2 = qD / mu                              # m = 1: |tau|^2 = q_D / mu
        need(abs(at) <= 7 and r * r * tau2 <= 1 and r * r * tau2 > F(99, 100), "B1_tau")
        n += 1
    need(acc >= 1000, "B1_tau")
    return n + 1


# ---------- B2: the cubic coefficient along the shear in the bad region ----------

def b2():
    n = 0
    tconst = F(18) if MUT == "M2" else F(19)
    # constants: 12 + 1/2 N + (13/80) N / 10 <= 13 N for N >= 1; (7 sqrt 7)^2 = 343 <= 19^2; 13 N <= 19 N^{3/2}
    need(12 + F(1, 2) + F(13, 800) <= 13 and 49 * 7 <= 19 ** 2, "B2_cubic")
    n += 1
    # N = 7 j^2 with j rational: N runs from 28/25 to 112, so 1 <= N < 7 is sampled
    js = (F(2, 5), F(3, 7), F(1, 2), F(1), F(2), F(3), F(4))
    samples = []
    for _ in range(2000):
        j = RNG.choice(js)
        p, q = RNG.randint(1, 60), RNG.randint(1, 60)
        samples.append((j, F(p, q), F(1, 10) * F(RNG.randint(1, 100), 100)))
    # boundary samples: r |tau| = 1 exactly (mu = 7 N r^2 = (7 j r)^2), small r
    for i in range(1, 40):
        for j in (F(2, 5), F(1), F(2)):
            r = F(1, 10 * i)
            samples.append((j, 7 * j * r, r))
    for j, smu, r in samples:
        NB = 7 * j * j                                 # 7 N = (7 j)^2
        need(NB >= 1, "B2_cubic")
        mu = smu * smu
        kap = F(RNG.randint(1, 100), 100)
        f4 = NB * F(RNG.randint(-100, 100), 100)
        if mu < 7 * NB * r * r:
            continue
        tau = 7 * j / smu                              # |tau| at its bound (7 N / mu)^{1/2}
        need(r * tau <= 1, "B2_cubic")
        e30 = 12 * kap + abs(f4) / 2 + F(13, 80) * NB * r
        need(e30 <= 13 * NB, "B2_cubic")
        alpha = e30 + 3 * NB * tau + 3 * NB * r * tau ** 2 + NB * r * r * tau ** 3
        # T = 19 N^{3/2} (1 + mu^{-1/2}); compare exactly by squaring: alpha^2 <= 361 N^3 (1 + mu^{-1/2})^2
        need(alpha ** 2 <= tconst ** 2 * NB ** 3 * (1 + 1 / smu) ** 2, "B2_cubic")
        n += 3
    return n


# ---------- B3: the hypotheses and the threshold of Lemma X on the bad region ----------

def b3():
    n = 0
    # Section 2 (c), last two hypothesis bullets. mu >= c4 N r^{4/3} kappa^{1/3} gives mu^3 >= c4^3 N^3 r^4 kappa, which is
    # >= (256/9) N^2 r^4 kappa as N >= 1; mu >= 7 N r^2 gives mu^2 >= 49 N^2 r^4 >= (64/3) N r^4 kappa as kappa <= 1 <= N
    c4 = F(3) if MUT == "M8" else F(4)
    need(c4 ** 3 >= F(256, 9) and 7 ** 2 >= F(64, 3), "B3_threshold")
    n += 1
    # the same at mu = mu0(N) = 7 N r^2 + c4 N r^{4/3} kappa^{1/3}, exactly: r = a^3, kappa = c^3 <= r, r^{4/3} kappa^{1/3} = a^4 c
    for _ in range(600):
        a = F(RNG.randint(1, 46), 100) / 10 ** RNG.randint(0, 4)    # r = a^3 <= 0.0974 < 1/10
        c = a * F(RNG.randint(1, 100), 100)                          # kappa = c^3 <= r
        NB = RNG.choice((F(1), F(RNG.randint(100, 1000), 100)))
        r, kap = a ** 3, c ** 3
        mu = 7 * NB * r * r + c4 * NB * a ** 4 * c
        need(mu ** 3 >= F(256, 9) * NB ** 2 * r ** 4 * kap, "B3_threshold")
        need(mu ** 2 >= F(64, 3) * NB * r ** 4 * kap, "B3_threshold")
        # the embedding bullet: r + 2 r^2 (kappa / mu)^{1/2} <= r + r^{3/2}, squared: 4 r kappa <= mu
        need(4 * r * kap <= mu, "B3_threshold")
        n += 3
    # ((256/9) kappa T^2)^{1/3} <= 22 N kappa^{1/3} (1 + mu^{-1/3}) for T = 19 N^{3/2}(1 + mu^{-1/2}):
    # (256/9) 19^2 <= 22^3, and (1 + y)^{2/3} <= 1 + y^{2/3}
    need(F(256, 9) * 19 ** 2 <= 22 ** 3, "B3_threshold")
    need(F(1024, 3) <= F(37, 2) ** 2, "B3_threshold")     # ((1024/3) N kappa)^{1/2} <= 18.5 N^{1/2} kappa^{1/2}
    n += 2
    for _ in range(500):
        u = F(RNG.randint(0, 60), RNG.randint(1, 30))
        # (1 + u^3)^{2/3} <= 1 + u^2  <=>  (1 + u^3)^2 <= (1 + u^2)^3
        need((1 + u ** 3) ** 2 <= (1 + u * u) ** 3, "B3_threshold")
        n += 1
    # exact check of the cubed inequality on perfect powers: N = n^2 (N^{3/2} = n^3), kappa = c^3, mu = m^6
    for _ in range(1000):
        nn = F(RNG.randint(1, 3))
        cc = F(RNG.randint(1, 40), 40)
        mm = F(RNG.randint(1, 60), 60)
        NB, kap, mu = nn ** 2, cc ** 3, mm ** 6
        T = 19 * nn ** 3 * (1 + 1 / mm ** 3)
        need(F(256, 9) * kap * T * T <= (22 * NB * cc * (1 + 1 / mm ** 2)) ** 3, "B3_threshold")
        if mu <= NB:
            # (b) <= 18.5 N (kappa / mu)^{1/2} as mu <= ||D|| <= N; squared
            need(F(1024, 3) * NB * kap <= (F(37, 2) * NB) ** 2 * kap / mu, "B3_threshold")
            n += 1
        n += 1
    # every threshold of (X.0) is at most 1024 N^2 times one term of eps_B (22, 18.5, 64, 1024, 16 <= 1024)
    need(max(22, F(37, 2), 64, 1024, 16) == 1024, "B3_threshold")
    return n + 1


# ---------- B4: the shell sums of the bad region and their domination ----------

def mono_le(m1, m2):
    """r^a kappa^b <= r^a' kappa^b' on 0 < kappa <= r <= 1 when b >= b' and a + b >= a' + b'."""
    (a, b), (a2, b2_) = m1, m2
    return b >= b2_ and a + b >= a2 + b2_


def b4():
    n = 0
    w = F(3, 2) if MUT == "M3" else F(5, 2)          # (V.4): eps^2 x^{5/2}
    # eps_B(kappa, mu)^2 terms as (power of x, power of kappa, power of r)
    terms = [(F(0), F(2), F(0)), (F(-1), F(1), F(0)), (F(0), F(2, 3), F(0)), (F(-2, 3), F(2, 3), F(0)),
             (F(-4), F(2), F(4))]
    out = []
    for px, pk, pr in terms:
        ex = w + px
        if ex > 0:
            # geometric sum dominated by the top shell x ~ t ~ r
            out.append((pr + ex, pk))
        else:
            # dominated by the bottom shell x ~ mu0 >= r^{4/3} kappa^{1/3}: x^{ex} <= (r^{4/3} kappa^{1/3})^{ex}
            need(ex < 0, "B4_shells")
            out.append((pr + F(4, 3) * ex, pk + F(1, 3) * ex))
        n += 1
    # multiply by r^2 (kappa + r) <= 2 r^3 and divide by the prefactor r^2: one more power of r
    final = [(a + 1, b) for a, b in out]
    targets = [(F(1), F(1)), (F(2), F(2, 3))]           # r kappa and r^2 kappa^{2/3}
    for mono in final:
        need(any(mono_le(mono, t) for t in targets), "B4_shells")
        n += 1
    # B0: r^2 (kappa + r) kappa^{2/3} mu0(1)^{1/2}, mu0(1)^{1/2} <= C (r + r^{2/3} kappa^{1/6}), divided by r^2
    half = F(1, 2) if MUT == "M4" else F(2, 3)
    b0 = [(F(1) + F(1), F(2, 3)), (F(1) + half, F(2, 3) + F(1, 6))]
    need(mono_le(b0[0], targets[1]), "B4_shells")
    # AM-GM: r^{5/3} kappa^{5/6} = (r kappa)^{1/2} (r^{7/3} kappa^{2/3})^{1/2}
    am = ((F(1) + F(7, 3)) / 2, (F(1) + F(2, 3)) / 2)
    need(am == b0[1], "B4_shells")
    need(mono_le((F(7, 3), F(2, 3)), targets[1]), "B4_shells")
    # (V.4) on B_R: K-measure x, beta_1 x^{1/2}, weight mu <= 2x; this x-exponent is the one used in the shells
    need(F(1) + F(1, 2) + 1 == w, "B4_shells")
    return n + 5


# ---------- B5: the ledger with the bad region at 2/3 ----------

def b5():
    n = 0
    sig = F(3, 14)
    # the bad-region row from its monomial r^2 kappa^{2/3} = l^{pk} r^{pr - 4 pk} (kappa = l / r^4): integrable at 0
    pr, pk = F(2), F(2, 3)
    bad = F(3, 5) if MUT == "M5" else F(2, 3)
    need(pr - 4 * pk > -1 and bad == pk, "B5_ledger")
    rows = {"rho^3": 3 * sig, "l^3 rho^-11": 3 - 11 * sig, "l^2 rho^-6 log": 2 - 6 * sig, "rho^8/l": 8 * sig - 1,
            "l^3/4": F(3, 4), "l^2/3 rows": F(2, 3), "l^2 rho^-5": 2 - 5 * sig, "l^4 rho^-13": 4 - 13 * sig,
            "both regions min(r^3 log, r kappa)": F(2, 3), "bad region r^2 kappa^2/3": bad}
    least = min(rows.values())
    need(least == F(9, 14), "B5_ledger")
    need(sorted(k for k, v in rows.items() if v == least) == ["l^3 rho^-11", "rho^3"], "B5_ledger")
    n += len(rows) + 3
    # the error r^2 min(1, kappa) over [0, rho]: r^2 on [0, l^{1/4}], and l r^{-2} above (decreasing, so its lower end)
    e_low = (F(2) + 1) / 4
    qr, qk = F(2), F(1)
    e_high = qk + (qr - 4 * qk + 1) / 4
    need(qr - 4 * qk + 1 < 0 and e_low == F(3, 4) and e_high == F(3, 4), "B5_ledger")
    # if the rho^3 row were l^{3/4} (Lemma U for differences) and int_0^rho T_r(0) is bounded by (W+.3)'s rho^4 log:
    # least 2/3 exactly on [5/24, 7/33], with theta = (1 - 4 sigma) / sigma < 1
    lo = F(1, 5) if MUT == "M6" else F(5, 24)
    for s_ in (lo, F(7, 33), (lo + F(7, 33)) / 2):
        rows2 = dict(rows)
        rows2["rho^3"] = e_low
        rows2["rho^4 log (W+.3)"] = 4 * s_
        rows2["l^3 rho^-11"] = 3 - 11 * s_
        rows2["l^2 rho^-6 log"] = 2 - 6 * s_
        rows2["rho^8/l"] = 8 * s_ - 1
        rows2["l^2 rho^-5"] = 2 - 5 * s_
        rows2["l^4 rho^-13"] = 4 - 13 * s_
        need(min(rows2.values()) == F(2, 3) and (1 - 4 * s_) / s_ < 1, "B5_ledger")
        n += 1
    return n + 1


def main():
    groups = [("B1_tau", b1), ("B2_cubic", b2), ("B3_threshold", b3), ("B4_shells", b4), ("B5_ledger", b5)]
    counts = {}
    try:
        for name, fn in groups:
            counts[name] = fn()
    except Failed as e:
        sys.stderr.write("FAILED: %s\n" % e.args[0])
        sys.exit(1)
    out = {"object": "CL-EM1-BAD-REGION-20261006-v1", "checks": counts, "total": sum(counts.values()), "passed": True}
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
