"""Exact controls for note SL (CL-SL-SOFT-LAYER-TWO-THIRDS-20261007-v1).

Standard library only; exact rational arithmetic; deterministic; output identical under -O.
Usage: python3 -B -S sl_exact.py [--mutant M1..M4]
On success: one JSON line on stdout, exit 0.
On a failed control: nothing on stdout, 'FAILED: <group>' on stderr, exit 1.
On invalid arguments: usage on stderr, exit 2.
"""
import json
import random
import sys
from fractions import Fraction as F

USAGE = "usage: sl_exact.py [--mutant M1..M4]\n"
MUTANTS = {"M1", "M2", "M3", "M4"}


def parse(argv):
    if len(argv) == 0:
        return None
    if len(argv) == 2 and argv[0] == "--mutant" and argv[1] in MUTANTS:
        return argv[1]
    sys.stderr.write(USAGE)
    sys.exit(2)


MUT = parse(sys.argv[1:])
RNG = random.Random(20261007)


class Failed(Exception):
    pass


def need(cond, group):
    if not cond:
        raise Failed(group)


def pos(lo=1, hi=60, den=12):
    return F(RNG.randint(lo, hi), RNG.randint(1, den))


# ---------- S1: the substitutions on exact perfect powers l = t^12 ----------

def s1():
    n = 0
    for _ in range(400):
        t = F(RNG.randint(1, 9), RNG.randint(2, 12))            # l^{1/12} = t, l^{1/4} = t^3, l^{1/3} = t^4
        l = t ** 12
        s = pos()
        r = t ** 3 * s                                           # r = l^{1/4} s
        need(l / r ** 4 == s ** -4, "S1_substitution")
        v = pos()
        r = (t ** 3 if MUT == "M1" else t ** 4) * v              # r = l^{1/3} v
        k = l / r ** 3
        kap = k / r
        need(k == v ** -3, "S1_substitution")
        need(kap == t ** -4 * v ** -4, "S1_substitution")        # kappa = l^{-1/3} v^{-4}
        need((r <= t ** 3) == (v <= 1 / t) == (kap >= 1), "S1_substitution")
        need((v <= 1) == (k >= 1), "S1_substitution")
        n += 5
    return n


# ---------- S2: the identities behind (1.2) and (1.4) ----------

def s2():
    n = 0
    for _ in range(400):
        t = F(RNG.randint(1, 9), RNG.randint(2, 12))
        l = t ** 12
        v = pos()
        r = t ** 4 * v
        k = l / r ** 3
        kap = k / r
        D = F(RNG.randint(-99, 99), RNG.randint(1, 30))
        need(kap * r ** 2 == r * k and kap ** 2 * r ** 2 == k ** 2, "S2_identities")
        need(D / r == (1 / k) * kap * D, "S2_identities")
        jac = t ** 4 * (t ** 4 if MUT != "M2" else 1)            # dr = l^{1/3} dv, and D_r = r (D_r/r) = l^{1/3} v (D_r/r)
        need(jac == t ** 8, "S2_identities")                     # l^{1/3} l^{1/3} = l^{2/3} = t^8
        # int D_r dr = l^{1/3} int D dv = l^{1/3} int r (D/r) dv = l^{2/3} int v (D/r) dv
        need(t ** 4 * (r * (D / r)) == jac * (v * (D / r)), "S2_identities")
        need(v * (1 / k) == v ** 4, "S2_identities")              # the weight of the limit: v (1/k) = v^4
        n += 5
    return n


# ---------- S3: the domination on the soft layer v <= l^{-1/12} ----------

def s3():
    n = 0
    low = high = 0
    for _ in range(600):
        t = F(1, RNG.randint(2, 12))                            # l^{-1/12} = 1/t in [2, 12]
        l = t ** 12
        top = (2 if MUT == "M3" else 1) / t                     # M3: beyond the soft layer
        v = top * F(RNG.randint(1, 1000), 1000)
        r = t ** 4 * v
        k = l / r ** 3
        kap = k / r
        if MUT != "M3":
            need(kap >= 1 and r <= k, "S3_domination")           # the soft layer: kappa >= 1, r <= k
        if v <= 1:
            need(2 * v / (kap * r) == 2 * v ** 4 and 2 * v ** 4 <= 2, "S3_domination")    # |D| <= 2C/kappa
            low += 1
        else:
            need(v * (r ** 2 + r * k) / r <= 2 * v * k and 2 * v * k == 2 * v ** -2, "S3_domination")   # (TL), r <= k
            high += 1
        n += 1
    need(low >= 20 and high >= 20, "S3_domination")             # both ranges are exercised
    return n + 1


# ---------- S4: the integrability of the limit, and (SL1) ----------

def s4():
    n = 0
    w = 3 if MUT == "M4" else 4                                 # the weight v^w of R_{2/3}
    # v -> 0: |v^w (Phi - Phi0)| <= C v^w, integrable at 0 iff w > -1
    need(w > -1, "S4_integrability")
    # v -> infinity: |Phi(v^{-3}) - Phi0| <= C k^2 = C v^{-6}, so v^w v^{-6} must be integrable at infinity: w - 6 < -1
    need(w - 6 == -2 and w - 6 < -1, "S4_integrability")
    # the limit of the domination at v >= 1 is C v^{-2}, matching v^w v^{-6}
    need(w - 6 == -2, "S4_integrability")
    for _ in range(200):
        k = F(RNG.randint(1, 60), RNG.randint(60, 120))          # 0 < k <= 1
        r = F(RNG.randint(1, 50), RNG.randint(50, 5000))
        if r > k:
            continue
        kap = k / r
        need(kap * r ** 2 * (1 + kap) == r * k + k ** 2, "S4_integrability")   # kappa * C r^2 (1 + kappa) = C(rk + k^2)
        n += 1
    return n + 3


def main():
    groups = [("S1_substitution", s1), ("S2_identities", s2), ("S3_domination", s3), ("S4_integrability", s4)]
    counts = {}
    try:
        for name, fn in groups:
            counts[name] = fn()
    except Failed as ex:
        sys.stderr.write("FAILED: %s\n" % ex.args[0])
        sys.exit(1)
    out = {"object": "CL-SL-SOFT-LAYER-TWO-THIRDS-20261007-v1", "checks": counts, "total": sum(counts.values()),
           "passed": True}
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
