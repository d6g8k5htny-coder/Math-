## QS addendum A3.8: author controls, exact executable and stdout

This publishes the standard-library control script that A3.8 ([6007704303](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6007704303)) cites, so anyone can replay it. It checks finite algebra, exponent ledgers, coverings, elementary integrals and the `P_QS` facts at exact saddles only; it does not prove the analytic statements.

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction rule.** The same as in [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189): the file is the exact text between the first ```` ```python ```` fence after its `###` heading and the next ```` ``` ```` line, plus a final newline. The expected stdout is the single JSON line in the following ```` ```json ```` fence, plus one newline.

**Run.** Each full run takes about 2 s.
- `python3 -B -S a38_exact.py`: exit 0, with exactly the stdout below (the JSON also reports the branch counts of the Lemma 3.2 coverings).
- `python3 -B -O -S a38_exact.py`: byte-identical output. No check depends on an `assert`.
- `--mutant M1` … `M13`: each exits 1 in both modes and names its failing group on stderr (identical stderr in both modes):
  - `M1` (QFE3 schedule alpha = (2 - 3 beta)/4 in place of /16 (H^4 e falls below beta at every beta < 2/3)): exits 1; stderr names `Z1_QFE3_ledger`.
  - `M2` (QFE3 ledger: rH^7 exponent written 1 - 6 alpha (H^6 in place of H^7)): exits 1; stderr names `Z1_QFE3_ledger`.
  - `M3` (ER3 window w = (r H^3)^(-1/12) in place of (r H^4)^(-1/12) (H^4 e no longer balances w^-8)): exits 1; stderr names `Z2_ER3_monomials`.
  - `M4` (MB3 (3.1): the wide-shell tail with 4 delta^2 N^2 in place of 16 delta^2 N^2): exits 1; stderr names `Z3_MB3_coverings`.
  - `M5` (MB3 (3.2): hard-gap strip {lam2 <= 4 delta N^2} in place of {lam2 <= 8 delta N^2}): exits 1; stderr names `Z3_MB3_coverings`.
  - `M6` (Lemma 2.3: (1/4) H^4 delta^4 in place of (5/4) H^4 delta^4): exits 1; stderr names `Z4_H_integrals`.
  - `M7` (Lemma 2.4: C_4 = 4 Lambda + 1/3 + 12 bounded by 4 H in place of 17 H): exits 1; stderr names `Z4_H_integrals`.
  - `M8` (Lemma 5.2: the fibre bound written (64|D|^3 + 2 J^2)/576 in place of /1152): exits 1; stderr names `Z5_PQS_facts`.
  - `M9` (Lemma 5.2: (sigma - 1)^2 < 2 h in place of 4 h): exits 1; stderr names `Z5_PQS_facts`.
  - `M10` (Lemma 5.1: lam-tilde <= k(D U^2 + K0 U/2) in place of K0 U/sqrt 2 (the mean-value constant)): exits 1; stderr names `Z6_tails_algebra`.
  - `M11` (Lemma 5.4: eps_0 = 1/(4 (1+S)^2) in place of 1/(12 (1+S)^2) (the series exceeds 2)): exits 1; stderr names `Z6_tails_algebra`.
  - `M12` (fixed-Lambda reduction: A3.7's rejected ledger read with eta_LE exponent 1 - omega in place of 1 - 2 omega): exits 1; stderr names `Z7_fixed_Lambda`.
  - `M13` (Lemma 5.1: D = 4 K0^2/(3 k) in place of 8 K0^2/(3 k) (the sqrt 2 of [P] (4.3) dropped)): exits 1; stderr names `Z6_tails_algebra`.
- `--bogus`, `--mutant M14` and a bare `--mutant`: exit 2.

The output was produced with Python 3.11.15. The script uses only `json`, `random`, `sys` and `fractions`. Two clean-context referee passes (same session; not review evidence) audited the groups, traced every mutant's failing checks to the stated reason, and found two pins that held only for the fixed seed; both were fixed before this posting (A3.8 §8).

### a38_exact.py

- **File:** 28557 bytes, SHA-256 `f5b32f603bbb4a0847d8299d02a0a49a6e7930b5eb93b4dc02761666e24d4faf`.
- **Stdout:** 525 bytes, SHA-256 `11f3b6a37d0dd2cb7a1f741f9cd2091066cb4fa01454a864551a95b45ca22c6a`.

```python
"""QS addendum A3.8: author controls (exact rational arithmetic, standard library only).

Finite algebra behind A3.8 (the d = 3 failure-measure rate on the growing soft layer): exponent
ledgers for both schedules, the shell coverings of Lemma 3.2, the H-carrying integrals of sections 2
and 4, the P_QS facts of Lemma 5.2 at exact rational saddles, and the elementary steps of Lemmas 5.1
and 5.4. It does not prove the Gaussian estimates of A3.4-A3.7, [P]'s cap integration, C82's Theorem
LB, or any topology.

Usage:
  python3 -B -S a38_exact.py                 exit 0, one JSON line on stdout
  python3 -B -S a38_exact.py --mutant Mj     j = 1..13: exit 1, the failing control named on stderr
  any other argument                         exit 2
"""
import json
import random
import sys
from fractions import Fraction as F

MUTANTS = {
    "M1": "QFE3 schedule alpha = (2 - 3 beta)/4 in place of /16 (H^4 e falls below beta at every beta < 2/3)",
    "M2": "QFE3 ledger: rH^7 exponent written 1 - 6 alpha (H^6 in place of H^7)",
    "M3": "ER3 window w = (r H^3)^(-1/12) in place of (r H^4)^(-1/12) (H^4 e no longer balances w^-8)",
    "M4": "MB3 (3.1): the wide-shell tail with 4 delta^2 N^2 in place of 16 delta^2 N^2",
    "M5": "MB3 (3.2): hard-gap strip {lam2 <= 4 delta N^2} in place of {lam2 <= 8 delta N^2}",
    "M6": "Lemma 2.3: (1/4) H^4 delta^4 in place of (5/4) H^4 delta^4",
    "M7": "Lemma 2.4: C_4 = 4 Lambda + 1/3 + 12 bounded by 4 H in place of 17 H",
    "M8": "Lemma 5.2: the fibre bound written (64|D|^3 + 2 J^2)/576 in place of /1152",
    "M9": "Lemma 5.2: (sigma - 1)^2 < 2 h in place of 4 h",
    "M10": "Lemma 5.1: lam-tilde <= k(D U^2 + K0 U/2) in place of K0 U/sqrt 2 (the mean-value constant)",
    "M11": "Lemma 5.4: eps_0 = 1/(4 (1+S)^2) in place of 1/(12 (1+S)^2) (the series exceeds 2)",
    "M12": "fixed-Lambda reduction: A3.7's rejected ledger read with eta_LE exponent 1 - omega in place of 1 - 2 omega",
    "M13": "Lemma 5.1: D = 4 K0^2/(3 k) in place of 8 K0^2/(3 k) (the sqrt 2 of [P] (4.3) dropped)",
}


def usage_exit():
    sys.stderr.write("usage: a38_exact.py [--mutant M1..M13]\n")
    sys.exit(2)


MUT = None
if len(sys.argv) == 1:
    pass
elif len(sys.argv) == 3 and sys.argv[1] == "--mutant" and sys.argv[2] in MUTANTS:
    MUT = sys.argv[2]
else:
    usage_exit()

RNG = random.Random(2026100638)
GROUPS = []
FAILED = []


class Group:
    def __init__(self, name):
        self.name, self.n, self.bad = name, 0, 0
        GROUPS.append(self)

    def check(self, ok):
        self.n += 1
        if not ok:
            self.bad += 1
            if self.name not in FAILED:
                FAILED.append(self.name)


def rq(lo, hi, den=89):
    a, b = int(F(lo) * den), int(F(hi) * den)
    return F(RNG.randint(a, b), den)


def rq_nz(lo, hi, den=89):
    while True:
        x = rq(lo, hi, den)
        if x != 0:
            return x


def simpson(f, a, b):
    """Exact for polynomials of degree <= 3."""
    return (b - a) / 6 * (f(a) + 4 * f((a + b) / 2) + f(b))


def pint(coeffs, a, b):
    """Exact integral over [a, b] of sum_i coeffs[i] x^i."""
    return sum(c_ * (b ** (i + 1) - a ** (i + 1)) / (i + 1) for i, c_ in enumerate(coeffs))


# --------------------------------------------------------------------------- the cubic (A3.6 section 0)
def PQS(psi, c, R, u, Z):
    return 2 * u ** 3 - F(3, 2) * u - F(1, 2) - (psi + 2 * c * u) * Z ** 2 / 48 + R * Z ** 3 / 3456


def gradPQS(psi, c, R, u, Z):
    return (6 * u * u - F(3, 2) - c * Z * Z / 24, -(psi + 2 * c * u) * Z / 24 + R * Z * Z / 1152)


def hessdet(psi, c, R, u, Z):
    puu, puz, pzz = 12 * u, -c * Z / 12, -(psi + 2 * c * u) / 24 + R * Z / 576
    return puu * pzz - puz * puz


# =========================================================================== Z1 QFE3 ledger
g = Group("Z1_QFE3_ledger")


def qfe3_terms(beta, alpha):
    e = 1 - beta / 2                        # e = r w^4 with w = r^(-beta/8)
    eta = 1 - beta / 4                      # eta_LE = 2 K2 r w^2
    return {
        "w^-8": beta,
        "r H^6 w^-4": 1 - 6 * alpha + beta / 2,
        "H^4 e": e - 4 * alpha,
        "r H^8 e^(1/2)": 1 - 8 * alpha + e / 2,
        "e": e,
        "r H^7": 1 - 7 * alpha if MUT != "M2" else 1 - 6 * alpha,
        "H^3 e^2": 2 * e - 3 * alpha,
        "H^4 e^4": 4 * e - 4 * alpha,
        "r H^8 e^2": 1 + 2 * e - 8 * alpha,
        "H^4 r^2 w^4": 2 - beta / 2 - 4 * alpha,
        "H^8 r^2 w^2": 2 - beta / 4 - 8 * alpha,
        "H^3 eta_LE": eta - 3 * alpha,
        "r H^7 eta_LE^(1/2)": 1 - 7 * alpha + eta / 2,
    }


def closed_forms(beta):
    return {
        "w^-8": beta,
        "r H^6 w^-4": (2 + 13 * beta) / 8,
        "H^4 e": F(1, 2) + beta / 4,
        "r H^8 e^(1/2)": F(1, 2) + 5 * beta / 4,
        "e": 1 - beta / 2,
        "r H^7": (2 + 21 * beta) / 16,
        "H^3 e^2": (26 - 7 * beta) / 16,
        "H^4 e^4": (14 - 5 * beta) / 4,
        "r H^8 e^2": 2 + beta / 2,
        "H^4 r^2 w^4": F(3, 2) + beta / 4,
        "H^8 r^2 w^2": 1 + 5 * beta / 4,
        "H^3 eta_LE": (10 + 5 * beta) / 16,
        "r H^7 eta_LE^(1/2)": (10 + 19 * beta) / 16,
    }


def alpha_max(beta):
    """The largest alpha each H-carrying term allows (its exponent is affine in alpha: value at 0 minus slope * alpha)."""
    t0, t1 = qfe3_terms(beta, F(0)), qfe3_terms(beta, F(1))
    out = {}
    for key in t0:
        slope = t0[key] - t1[key]
        if slope > 0:
            out[key] = (t0[key] - beta) / slope
    return out


for n in range(1, 61):
    beta = F(2, 3) * F(n, 61)                            # beta in (0, 2/3)
    alpha = (2 - 3 * beta) / (4 if MUT == "M1" else 16)
    terms = qfe3_terms(beta, alpha)
    cf = closed_forms(beta)
    for key, val in terms.items():
        if MUT != "M1":
            g.check(val == cf[key])                          # the table's closed forms (alpha = (2 - 3 beta)/16)
        g.check(val >= beta)                                 # each term is at least beta
    # the minimum of the ledger is exactly beta (from w^-8)
    g.check(min(terms.values()) == beta)
    # every term's constraint on alpha is met; near beta = 2/3 the tightest is H^4 e's (2 - 3 beta)/8, for beta < 6/13 it is rH^7's (1 - beta)/7
    amax = alpha_max(beta)
    g.check(all(alpha <= a_ for a_ in amax.values()))
    g.check(amax["H^4 e"] == (2 - 3 * beta) / 8 and (amax["r H^7"] == (1 - beta) / 7 or MUT == "M2"))
    tight = min(amax, key=lambda k_: (amax[k_], k_))
    if beta < F(6, 13):
        g.check(tight == "r H^7" or MUT == "M2")
    elif beta > F(6, 13):
        g.check(tight == "H^4 e")
    # tails: the least admissible m
    m = 1
    while m * alpha < beta:
        m += 1
    g.check(m * alpha >= beta and (m - 1) * alpha < beta)
    g.check(m >= 16 * beta / (2 - 3 * beta) and m - 1 < 16 * beta / (2 - 3 * beta))
    # admissibility powers, all positive
    powers = [1 - alpha, 1 - 4 * alpha, beta / 8, F(1, 2) - beta / 8, 1 - beta / 2, 1 - beta / 4]
    g.check(all(p_ > 0 for p_ in powers))
    g.check(1 - 4 * alpha == (2 + 3 * beta) / 4 or MUT == "M1")
# the obstruction at beta = 2/3: w^-8, e and H^4 e (at alpha = 0) are exactly beta there; H^4 e falls below beta for alpha > 0
beta = F(2, 3)
for a_ in (F(1, 100), F(1, 1000)):
    g.check(qfe3_terms(beta, a_)["H^4 e"] < beta)
t0 = qfe3_terms(beta, F(0))
g.check(t0["H^4 e"] == beta == t0["w^-8"] == t0["e"])
g.check(sorted(k_ for k_, v_ in t0.items() if v_ == beta) == ["H^4 e", "e", "w^-8"])
g.check(alpha_max(F(6, 13))["H^4 e"] == alpha_max(F(6, 13))["r H^7"] == F(1, 13) or MUT == "M2")

# =========================================================================== Z2 ER3 monomials
g = Group("Z2_ER3_monomials")
# w = (r H^4)^(-1/12): exponents (r, H) of each term of (6.1); e = r w^4 = r^(2/3) H^(-4/3)
wexp = (F(-1, 12), F(-1, 4)) if MUT == "M3" else (F(-1, 12), F(-4, 12))   # (r, H) exponents of w
rw, hw = wexp
e_r, e_h = 1 + 4 * rw, 4 * hw
eta_r, eta_h = 1 + 2 * rw, 2 * hw
mono = {
    "w^-8": (-8 * rw, -8 * hw),
    "r H^6 w^-4": (1 - 4 * rw, 6 - 4 * hw),
    "H^4 e": (e_r, 4 + e_h),
    "r H^8 e^(1/2)": (1 + e_r / 2, 8 + e_h / 2),
    "e": (e_r, e_h),
    "r H^7": (F(1), F(7)),
    "H^3 e^2": (2 * e_r, 3 + 2 * e_h),
    "H^4 e^4": (4 * e_r, 4 + 4 * e_h),
    "r H^8 e^2": (1 + 2 * e_r, 8 + 2 * e_h),
    "H^4 r^2 w^4": (2 + 4 * rw, 4 + 4 * hw),
    "H^8 r^2 w^2": (2 + 2 * rw, 8 + 2 * hw),
    "H^3 eta_LE": (eta_r, 3 + eta_h),
    "r H^7 eta_LE^(1/2)": (1 + eta_r / 2, 7 + eta_h / 2),
}
expected = {
    "w^-8": (F(2, 3), F(8, 3)), "r H^6 w^-4": (F(4, 3), F(22, 3)), "H^4 e": (F(2, 3), F(8, 3)),
    "r H^8 e^(1/2)": (F(4, 3), F(22, 3)), "e": (F(2, 3), F(-4, 3)), "r H^7": (F(1), F(7)),
    "H^3 e^2": (F(4, 3), F(1, 3)), "H^4 e^4": (F(8, 3), F(-4, 3)), "r H^8 e^2": (F(7, 3), F(16, 3)),
    "H^4 r^2 w^4": (F(5, 3), F(8, 3)), "H^8 r^2 w^2": (F(11, 6), F(22, 3)), "H^3 eta_LE": (F(5, 6), F(7, 3)),
    "r H^7 eta_LE^(1/2)": (F(17, 12), F(20, 3)),
}
for key, val in mono.items():
    g.check(val == expected[key])
g.check(mono["w^-8"] == mono["H^4 e"])                           # the balanced pair
for key, (re_, he_) in mono.items():
    if key not in ("w^-8", "H^4 e"):
        # every other term is O(r^(2/3) H^(8/3)): either its r-exponent exceeds 2/3, or (the term e) it equals 2/3 with a smaller H-power
        g.check(re_ > F(2, 3) or (re_ == F(2, 3) and he_ <= F(8, 3)))
g.check(mono["e"] == (F(2, 3), F(-4, 3)))
# side conditions as (r, H) exponents: r^(1/2) w, e, eta_LE, r H, r H^4 all vanish (positive r-exponent)
for re_ in (F(1, 2) + rw, e_r, eta_r, F(1), F(1)):
    g.check(re_ > 0)

# =========================================================================== Z3 shell coverings of Lemma 3.2
g = Group("Z3_MB3_coverings")
tail16 = 4 if MUT == "M4" else 16
strip8 = 4 if MUT == "M5" else 8
BR = {"3.1 trivial range": 0, "3.1 inner band": 0, "3.1 shell": 0, "3.1 wide tail": 0, "3.1 outside": 0,
      "3.2 first band": 0, "3.2 band shells": 0, "3.2 strip": 0, "3.2 outside": 0}


def jstar_of(dl):
    """The first j >= 0 with 2^(j+1) delta > 1/2 (so j0 = jstar - 1 is the last shell index of Lemma 3.2)."""
    j = 0
    while 2 ** (j + 1) * dl <= F(1, 2):
        j += 1
    return j


def cover31(mu, N, dl):
    """Right side of the pointwise covering of (3.1) for delta < 1/4: inner band, dyadic shells, wide tail."""
    js = jstar_of(dl)
    rhs = F(1 if abs(mu) <= dl else 0)
    for j in range(js):
        rhs += N * N / F(4 ** j) * (1 if abs(mu) <= 2 ** (j + 1) * dl else 0)
    wide = abs(mu) <= dl * N and abs(mu) > 2 ** js * dl
    if wide:
        g.check(N > 2 ** js > 1 / (4 * dl))                   # the wide tail forces N > 2^(j0 + 1) > 1/(4 delta)
    rhs += (tail16 * dl * dl * N * N if wide else 0)
    return rhs, wide, js


def cover32(mu, lam2, N, dl):
    """Right side of the pointwise covering of (3.2): first band, weighted band shells, the hard-gap strip."""
    q = lam2 * abs(mu)
    first = lam2 >= 2 * dl and q <= dl
    rhs = F(1 if first else 0)
    shells = 0
    j = 0
    while 4 ** j * dl < q and j < 400:
        if 4 ** j * dl < q <= 4 ** (j + 1) * dl and lam2 >= 2 * 4 ** (j + 1) * dl:
            rhs += N ** 4 / F(16 ** j)
            shells += 1
            g.check(4 ** (j + 1) * dl / lam2 <= F(1, 2))      # consistency pin: the band's fibre width is at most 1/2
        j += 1
    strip = lam2 <= strip8 * dl * N * N
    rhs += 1 if strip else 0
    return rhs, first, shells, strip


# (3.1), stratified: delta in [2^-13, 1/4] (dyadic exponent uniform), then the branch picks N and |mu|: the inner band,
# a dyadic shell, the wide tail with N in (2^(j0+1), 1/(2 delta)) where the constant 16 is needed, or outside the event
for _ in range(3000):
    jd = RNG.randint(2, 12)
    dl = rq(F(1, 2), 1, den=997) / 2 ** jd                   # delta in [2^-(jd+1), 2^-jd]
    if dl >= F(1, 4):
        BR["3.1 trivial range"] += 1
        g.check(tail16 * dl * dl >= 1)
        continue
    js = jstar_of(dl)
    g.check(js >= 1 and 2 ** js * dl <= F(1, 2) < 2 ** (js + 1) * dl)
    branch = RNG.random()
    if branch < F(1, 2):
        N = max(F(1), F(1) / (4 * dl) * (1 + rq(F(-1, 10), F(1, 10), den=1009))) if RNG.random() < F(1, 2) else rq(1, F(2) / dl, den=7)
        if branch < F(1, 4):
            mu = rq_nz(-1, 1, den=1013) * dl                                               # inner band |mu| <= delta
        else:
            j = RNG.randint(0, js - 1)
            mu = rq_nz(-1, 1, den=1013) * 2 ** j * dl * (1 + rq(F(1, 1000), 1, den=1019))  # shell 2^j delta < |mu| <= 2^(j+1) delta
    elif branch < F(3, 4):
        lo_N, hi_N = F(2 ** js), F(1) / (2 * dl)
        N = lo_N + rq(F(1, 1000), 1, den=1019) * ((hi_N - lo_N) if hi_N > lo_N else lo_N)   # N in (2^(j0+1), 1/(2 delta)) when nonempty
        lo = 2 ** js * dl
        mu = (lo + rq(F(1, 1000), 1, den=1019) * (dl * N - lo)) * RNG.choice((-1, 1))      # the wide tail 2^(j0+1) delta < |mu| <= delta N
    else:
        N = rq(1, F(2) / dl, den=7)
        mu = dl * N * (1 + rq(F(1, 1000), 3, den=1019)) * RNG.choice((-1, 1))              # outside: |mu| > delta N
    lhs = 1 if abs(mu) <= dl * N else 0
    rhs, wide, _js = cover31(mu, N, dl)
    g.check(lhs <= rhs)
    if not lhs:
        BR["3.1 outside"] += 1
    elif abs(mu) <= dl:
        BR["3.1 inner band"] += 1
    elif wide:
        BR["3.1 wide tail"] += 1
    else:
        BR["3.1 shell"] += 1
# the trivial range delta >= 1/4 by itself (16 delta^2 >= 1 at the cut)
for _ in range(400):
    dl = rq(F(1, 4), 3, den=1020)                              # the lower end is exactly 1/4 (1020 is divisible by 4)
    BR["3.1 trivial range"] += 1
    g.check(tail16 * dl * dl >= 1)
# (3.2), stratified: q = lam2 |mu| in (0, delta] or in a shell (4^j delta, 4^(j+1) delta]; lam2 in the band regime, above the
# strip with q <= delta N^2 (so the band terms must carry the covering), or inside the strip
for _ in range(3000):
    jd = RNG.randint(0, 12)
    dl = rq(F(1, 2), 1, den=997) / 2 ** jd
    j = RNG.randint(-1, 8)
    if j < 0:
        q = rq(F(1, 1000), 1, den=1019) * dl
    else:
        q = 4 ** j * dl * (1 + rq(F(1, 1000), 3, den=1019))
    regime = RNG.random()
    if regime < F(1, 3):
        lam2 = 2 * 4 ** (j + 1) * dl * (1 + rq(0, 3, den=7))                           # the band regime
        N = rq(1, 200, den=3)
    elif regime < F(2, 3):
        N = max(F(1), q / dl) * rq(1, 4, den=5)                                         # N^2 >= q/delta, so q <= delta N^2
        lam2 = 8 * dl * N * N * (1 + rq(F(1, 1000), 2, den=1019))                       # above the strip: the band terms must cover
    else:
        N = rq(1, 50, den=3)
        lam2 = rq(F(1, 1000), 1, den=1019) * min(2 * 4 ** (j + 1) * dl, 8 * dl * N * N)  # inside the strip, below the band's lambda_2 threshold
    mu = q / lam2
    lhs = 1 if q <= dl * N * N else 0
    rhs, first, shells, strip = cover32(mu, lam2, N, dl)
    g.check(lhs <= rhs)
    if not lhs:
        BR["3.2 outside"] += 1
    elif first:
        BR["3.2 first band"] += 1
    elif shells:
        BR["3.2 band shells"] += 1
    else:
        BR["3.2 strip"] += 1
# targeted cases for the strip constant: N^2 just above 4^j, q just above 4^j delta, and lam2 between 4 delta N^2 and 8 delta 4^j
for j in range(1, 12):
    for _ in range(20):
        dl = rq(F(1, 89), 1)
        N2 = 4 ** j * (1 + rq(F(1, 1000), F(1, 10), den=10 ** 4))
        q = 4 ** j * dl * (1 + rq(F(1, 1000), F(1, 100), den=10 ** 5))
        if not q <= dl * N2:
            continue
        lam2 = 4 * dl * N2 + rq(F(1, 1000), 1, den=10 ** 4) * (8 * dl * 4 ** j - 4 * dl * N2)
        if not (4 * dl * N2 < lam2 < 2 * 4 ** (j + 1) * dl):
            continue
        covered = (lam2 >= 2 * dl and q <= dl) or (lam2 >= 2 * 4 ** (j + 1) * dl) or (lam2 <= strip8 * dl * N2)
        g.check(covered)
# two explicit witnesses for the constants 16 and 8
mu, N, dl = F(21, 50), F(9, 2), F(1, 10)                                                  # j0 + 1 = 2: the wide tail (2/5, 9/20]
g.check(abs(mu) <= dl * N and abs(mu) > 2 ** jstar_of(dl) * dl and 2 ** jstar_of(dl) < N < 1 / (2 * dl))
g.check(tail16 * dl * dl * N * N >= 1)                                                    # 16 delta^2 N^2 = 81/25; with 4 it is 81/100
dl, N2 = F(1, 10), F(9, 2)
lam2 = 20 * dl
q = F(9, 2) * dl
g.check(q <= dl * N2 and not (lam2 >= 2 * dl and q <= dl) and not (lam2 >= 2 * 16 * dl) and lam2 <= strip8 * dl * N2)
# every branch of both coverings was exercised
g.check(BR["3.1 inner band"] >= 300 and BR["3.1 shell"] >= 300 and BR["3.1 wide tail"] >= 300 and BR["3.1 outside"] >= 100)
g.check(BR["3.2 first band"] >= 100 and BR["3.2 band shells"] >= 300 and BR["3.2 strip"] >= 300 and BR["3.2 outside"] >= 100)
# the finite series and the totals (consistency pins)
for n in range(0, 40):
    g.check(sum(F(2 ** (jj + 1), 4 ** jj) for jj in range(n + 1)) <= 4)
    g.check(sum(F(1, 4 ** jj) for jj in range(n + 1)) <= F(4, 3))
    g.check(sum(F(4 ** (jj + 1), 16 ** jj) for jj in range(n + 1)) <= F(16, 3))
    g.check(sum(F(1, 16 ** jj) for jj in range(n + 1)) <= F(16, 15))
g.check(1 + 4 == 5 and 1 + F(4, 3) == F(7, 3) and 1 + F(16, 3) == F(19, 3) and 1 + F(16, 15) == F(31, 15))

# =========================================================================== Z4 the H-carrying integrals
g = Group("Z4_H_integrals")


def hardgap_integral(x1, x0, dl):
    """int_0^inf min(1, (delta/l)^5) l (x1 l^2 + x0) dl, computed from its two pieces: Simpson on [0, delta] (a cubic),
    and the tail with l = delta/x, which is int_0^1 (x1 delta^4 + x0 delta^2 x^2) dx."""
    return simpson(lambda l: l * (x1 * l * l + x0), F(0), dl) + pint([x1 * dl ** 4, F(0), x0 * dl ** 2], F(0), F(1))


for _ in range(300):
    Lam = rq(1, 9)
    H = 1 + Lam
    Astar = 12 * Lam
    g.check(simpson(lambda y: y, F(0), Astar) == 72 * Lam ** 2 and simpson(lambda y: F(1), F(0), Astar) == 12 * Lam)
    g.check(72 * Lam ** 2 <= 72 * H ** 2 and 12 * Lam <= 12 * H)
    r = rq(F(1, 1000), F(1, 10), den=10 ** 4)
    # Lemma 2.1 at phi = 1: int_0^{12 l} s(12 l - s) ds = 288 l^3 and int_0^Lam 288 l^3 dl = 72 Lam^4 (Simpson, exact);
    # int_0^Lam 12 l r H^6 dl = 6 Lam^2 r H^6; and int_0^{A_*} (H^2 s + r H^7) ds dominates both
    l_ = rq(F(1, 89), 5)
    g.check(simpson(lambda s_: s_ * (12 * l_ - s_), F(0), 12 * l_) == 288 * l_ ** 3)
    g.check(simpson(lambda l: 288 * l ** 3, F(0), Lam) == 72 * Lam ** 4)
    lhs = 72 * Lam ** 4 + 6 * Lam ** 2 * r * H ** 6
    rhs = H ** 2 * Astar ** 2 / 2 + r * H ** 7 * Astar
    g.check(lhs <= rhs)
    # Lemma 2.3's inner integral, computed independently of its closed form (5/4) x1 delta^4 + (5/6) x0 delta^2, at (x1, x0) = (H^4, r H^8)
    dl = rq(F(1, 89), 2)
    x1, x0 = H ** 4, r * H ** 8
    c54 = F(1, 4) if MUT == "M6" else F(5, 4)
    g.check(hardgap_integral(x1, x0, dl) == c54 * x1 * dl ** 4 + F(5, 6) * x0 * dl ** 2)
    # Lemma 4.1: the two totals at d1 = sqrt(eps) (eps a square), computed from the pieces; the strip integral is exact, the
    # proof's bound H^2 d1^2 + r H^7 d1 for it gives the cruder totals (3/2) H^2 eps + (4/3) r H^7 sqrt eps and (29/24) H^2 eps + (23/18) r H^7 sqrt eps
    s_ = rq(F(1, 89), 1)
    eps = s_ * s_
    strip = simpson(lambda y: H ** 2 * y + r * H ** 7, F(0), s_)
    g.check(strip <= H ** 2 * eps + r * H ** 7 * s_)
    away1 = eps ** 2 * pint([F(0), H ** 2 / s_ ** 2, r * H ** 7 / s_ ** 3], F(0), F(1))   # int_{d1}^inf s^-4 (H^2 s + r H^7) ds with s = d1/x
    g.check(strip + away1 == H ** 2 * eps + F(4, 3) * r * H ** 7 * s_ <= F(3, 2) * H ** 2 * eps + F(4, 3) * r * H ** 7 * s_)
    y_ = s_ * (1 + rq(0, 4))
    inner = hardgap_integral(H ** 2 * y_, r * H ** 7, eps / y_ ** 2)                      # the inner integral at this y, independently
    g.check(inner == F(5, 4) * H ** 2 * eps ** 4 / y_ ** 7 + F(5, 6) * r * H ** 7 * eps ** 2 / y_ ** 4)
    away2 = F(5, 4) * H ** 2 * eps ** 4 * pint([0, 0, 0, 0, 0, F(1)], F(0), F(1)) / s_ ** 6 \
        + F(5, 6) * r * H ** 7 * eps ** 2 * pint([0, 0, F(1)], F(0), F(1)) / s_ ** 3          # y = d1/x: int y^-7 = d1^-6/6, int y^-4 = d1^-3/3
    g.check(strip + away2 == F(17, 24) * H ** 2 * eps + F(23, 18) * r * H ** 7 * s_ <= F(29, 24) * H ** 2 * eps + F(23, 18) * r * H ** 7 * s_)
    # eps_V, eps'_V <= C_V H^2 e with c_* = 1/(12000 Lambda^2)
    cstar = 1 / (12000 * Lam ** 2)
    K0, Ce, kp, e_ = rq(F(1, 2), 9), rq(1, 99), rq(1, 3), rq(F(1, 1000), 1, den=10 ** 4)
    CV = 48000 * max(K0, Ce * kp)
    g.check(4 * K0 * e_ / cstar <= CV * H ** 2 * e_ and 4 * Ce * kp * e_ / cstar <= CV * H ** 2 * e_)
    # Lemma 2.4: a_i L_i = a_i/3 + (gamma^2 + 144)/12 <= (4 Lambda + 1/3 + 12) P^2 on T (a_i <= 12 Lambda, gamma^2 <= 4 P^2), C_4 <= 17 H
    c17 = 4 if MUT == "M7" else 17
    a_i, P_ = rq(F(1, 89), 12 * Lam), rq(1, 20)
    gam2 = rq(0, 4) * P_ * P_
    g.check(a_i / 3 + (gam2 + 144) / 12 <= (4 * Lam + F(1, 3) + 12) * P_ * P_)
    g.check(4 * Lam + F(1, 3) + 12 <= c17 * H)
    # the (3/2) bound int_0^A min(1,(sigma/y)^3)(x1 y + x0) dy <= (3/2)(x1 sigma^2 + x0 sigma), both pieces computed
    sig, A_ = rq(F(1, 89), 2), rq(1, 30)
    x1, x0 = rq(0, 5), rq(0, 5)
    if sig <= A_:
        # tail with y = sigma/x, x from sigma/A to 1: sigma^3 int (x1 y^-2 + x0 y^-3) dy = int (x1 sigma^2 + x0 sigma x) dx
        val = simpson(lambda y: x1 * y + x0, F(0), sig) + pint([x1 * sig ** 2, x0 * sig], sig / A_, F(1))
    else:
        val = simpson(lambda y: x1 * y + x0, F(0), A_)
    g.check(val <= F(3, 2) * (x1 * sig ** 2 + x0 * sig))
    # Lemma 4.2: the strip integral and 73 P^2
    g.check(strip == H ** 2 * eps / 2 + r * H ** 7 * s_)
    gam2_42 = rq(0, 1) * P_ * P_                                 # Lemma 4.2 uses gamma^2 <= P^2 (|gamma| <= |t| <= P)
    g.check(gam2_42 + 72 <= 73 * P_ * P_)

# =========================================================================== Z5 Lemma 5.2 at exact saddles
g = Group("Z5_PQS_facts")
c2 = F(2)
q14 = F(1, 4)
den1152 = 576 if MUT == "M8" else 1152
c4h = 2 if MUT == "M9" else 4
cnt = 0
big = 0
while cnt < 600 or big < 200:
    sg = F(RNG.randint(-199, 399), 100)                      # wider than (-1, 3); the saddle facts cut it down
    Zs = rq_nz(-4, 4, den=97)
    if sg * sg == 1:
        continue
    c = 36 * (sg * sg - 1) / (Zs * Zs)
    psi = (4 * abs(c) if RNG.random() < F(1, 2) else abs(c)) + rq(F(1, 37), 11)        # half of the saddles on the branch psi >= 4|c|
    R = 48 * (psi - c * sg) / Zs
    if not (c - sg * psi < 0):
        continue
    u = -sg / 2
    g.check(gradPQS(psi, c, R, u, Zs) == (0, 0) and hessdet(psi, c, R, u, Zs) < 0)
    h = -PQS(psi, c, R, u, Zs)
    if not (0 < h < 1):
        continue
    cnt += 1
    v = 1 - h
    rho = c / psi
    x = psi * Zs * Zs / 144
    g.check(sg == 2 * (v + x) - 1)                                   # C82 (5) in C82's variables
    g.check((sg - 1) ** 2 < c4h * h)                                 # the display before C82 (15), for h < 1
    g.check(x == h + (sg - 1) / 2 and x < 2 and -1 < sg < 3)         # consequences: x < h + sqrt h < 2, |sigma - 1| < 2
    g.check(R * R * x == 16 * psi ** 3 * (1 - rho * sg) ** 2)       # C82 (16), the squared line equation
    if psi >= 4 * abs(c):
        big += 1
        g.check(abs(rho) <= F(1, 4) and abs(1 - rho * sg) > q14)
        g.check(sg * sg < 3 and abs(1 - rho * sg) > F(1, 2))          # in fact x < 2 forces sigma^2 < 1 + 8 rho <= 3 (not used)
    g.check(psi ** 3 <= 64 * abs(c) ** 3 + c2 * R * R)
    # the conversion to (64|D|^3 + 2 J^2)/1152 for a jet with these (psi, c, R)
    gam = rq_nz(-3, 3)
    D, J = c * gam ** 2, R * gam ** 3
    g.check(gam ** 6 / 384 * (64 * abs(c) ** 3 + 2 * R * R) / 3 == (64 * abs(D) ** 3 + 2 * J * J) / den1152)
    lamt = gam * gam * psi / 24
    g.check((24 * lamt) ** 3 <= 64 * abs(D) ** 3 + c2 * J * J)
    # (4|D| + t)^3 >= 64|D|^3 + t^3 for t >= 0, so with t^3 = 2 J^2: 24 lamt <= 4|D| + t, and t = 2^(1/3)|J|^(2/3) <= (13/10)|J|^(2/3)
    # since 2 <= (13/10)^3; hence lamt <= |D|/6 + (13/240)|J|^(2/3) <= (|D| + |J|^(2/3))/6
    g.check(2 <= F(13, 10) ** 3 and F(13, 240) <= F(1, 6))
    tt = rq(0, 5)
    g.check((4 * abs(D) + tt) ** 3 >= 64 * abs(D) ** 3 + tt ** 3)
g.check(cnt >= 600 and big >= 200)                                    # at least 600 saddles, at least 200 on the branch psi >= 4|c|

# =========================================================================== Z6 Lemmas 5.1 and 5.4
g = Group("Z6_tails_algebra")
SQ2_LO, SQ2_HI = F(14142, 10000), F(14143, 10000)   # brackets of sqrt 2
coef = F(1, 2) if MUT == "M10" else SQ2_HI / 2        # the mean-value constant: (1/2) sqrt 2 = 1/sqrt 2, bracketed above
dnum = 4 if MUT == "M13" else 8                       # D = 8 K0^2/(3 k): [P]'s 4 K^2/(3 k) with K = sqrt 2 K0
g.check(4 * (SQ2_LO ** 2) <= dnum and dnum <= 4 * (SQ2_HI ** 2) + F(1, 1000))   # consistency pin for the constant 8
for _ in range(2000):
    k, K0 = rq(F(1, 4), 3), rq(F(1, 2), 9)
    D_ = dnum * K0 * K0 / (3 * k)
    Jr, lmax = rq(1, 40), rq(0, 40)
    U = Jr + lmax
    r = rq(F(1, 10 ** 4), F(1, 10), den=10 ** 5)
    # the transverse 2 x 2 Hessian: ||A||_F^2 = l1^2 + l2^2 <= 2 lmax^2 for 0 < l1 <= l2 = lmax (the sqrt 2 of M3 <= sqrt 2 K0 U)
    l1 = rq(0, 1) * lmax
    g.check(l1 * l1 + lmax * lmax <= 2 * lmax * lmax and K0 * (Jr + SQ2_LO * lmax) <= SQ2_LO * K0 * U)
    # M3 <= sqrt 2 K0 U (sampled below the lower bracket, so the sample satisfies the true bound); at the top a quarter of the time
    top = RNG.random() < F(1, 4)
    M3 = K0 * U * SQ2_LO if top else rq(0, 1) * K0 * U * SQ2_LO
    # [P] (7.1): depth failure means lam_min <= (4/(3k)) r M3^2 <= D r U^2
    g.check(4 * r * M3 * M3 / (3 * k) <= D_ * r * U * U)
    xi = F(1) if top else rq(0, 1)
    lam_min = xi * D_ * r * U * U                        # depth failure: lam_min <= D r U^2 (equality a quarter of the time)
    lam1_mid = lam_min + r * M3 / 2                      # Weyl + mean value (worst case)
    lamt = k * lam1_mid / r
    g.check(lamt <= k * (D_ * U * U + K0 * U * coef))
    CU = k * (D_ + K0)
    g.check(k * (D_ * U * U + K0 * U * SQ2_HI / 2) <= CU * U * U)            # U >= 1 and 1/sqrt2 < 1
    # the lam-tilde < -Lambda case: (r/2) M3 > r Lambda/k gives M3 > 2 Lambda/k, U > sqrt2 Lambda/(k K0), and U^2 >= Lambda/C_U (via U >= 1)
    Lam = rq(1, 50)
    if r * M3 / 2 > r * Lam / k:
        g.check(M3 > 2 * Lam / k and U >= M3 / (K0 * SQ2_HI) and U * U >= Lam / CU)
        g.check(CU >= k * K0 and k * k * K0 * K0 / (2 * CU) <= CU / 2)      # the two inequalities the proof uses
# Lemma 5.4: (2n)^n/n! <= (2e)^n with e in [27182/10000, 27183/10000]; the geometric series at eps_0 = 1/(12(1+S)^2)
e_lo, e_hi = F(27182, 10000), F(27183, 10000)
fact = 1
for n in range(1, 61):
    fact *= n
    g.check(F((2 * n) ** n, fact) <= (2 * e_hi) ** n)
for S in (F(0), F(1, 2), F(1), F(10), F(1000)):
    eps0 = 1 / ((4 if MUT == "M11" else 12) * (1 + S) ** 2)
    ratio = 2 * e_hi * eps0 * (1 + S) ** 2
    g.check(ratio < 1)
    g.check(1 + ratio / (1 - ratio) <= 2)                            # sum_{n>=0} ratio^n <= 2

# =========================================================================== Z7 the fixed-Lambda reduction
g = Group("Z7_fixed_Lambda")
om = F(1, 12)
e = 1 - 4 * om
eta = 1 - (1 if MUT == "M12" else 2) * om
fixed = {"w^-8": 8 * om, "r w^-4": 1 + 4 * om, "e": e, "r e^(1/2)": 1 + e / 2, "r": F(1), "e^2": 2 * e, "e^4": 4 * e,
         "r e^2": 1 + 2 * e, "r^2 w^4": 2 - 4 * om, "r^2 w^2": 2 - 2 * om, "eta_LE": eta, "r eta_LE^(1/2)": 1 + eta / 2}
g.check(min(fixed.values()) == F(2, 3))
g.check(sorted(k_ for k_, v_ in fixed.items() if v_ == F(2, 3)) == ["e", "w^-8"])
g.check(fixed["eta_LE"] == F(5, 6) and fixed["r eta_LE^(1/2)"] == F(17, 12))
# A3.7's two ledgers are the H = 1 specializations of (6.1)
a37_elder = [F(2, 3), F(4, 3), F(2, 3), F(4, 3), F(1), F(8, 3), F(7, 3), F(5, 3)]
a37_rejected = [F(2, 3), F(4, 3), F(2, 3), F(1), F(5, 6), F(17, 12)]
g.check(min(a37_elder) == F(2, 3) and min(a37_rejected) == F(2, 3))
g.check(fixed["e^2"] == F(4, 3) and fixed["e^4"] == F(8, 3) and fixed["r e^2"] == F(7, 3))

# --------------------------------------------------------------------------- report
out = {"object": "CL-QS-A3-8-CONTROLS-20261006-v1",
       "groups": {gr.name: [gr.n - gr.bad, gr.n] for gr in GROUPS},
       "total": sum(gr.n for gr in GROUPS),
       "z3_branches": BR,
       "passed": not FAILED}
if FAILED:
    sys.stderr.write("FAILED: %s\n" % ", ".join(FAILED))
    if MUT:
        sys.stderr.write("mutant %s: %s\n" % (MUT, MUTANTS[MUT]))
    sys.exit(1)
sys.stdout.write(json.dumps(out, sort_keys=True) + "\n")
```

```json
{"groups": {"Z1_QFE3_ledger": [2045, 2045], "Z2_ER3_monomials": [31, 31], "Z3_MB3_coverings": [12249, 12249], "Z4_H_integrals": [4800, 4800], "Z5_PQS_facts": [8992, 8992], "Z6_tails_algebra": [11183, 11183], "Z7_fixed_Lambda": [5, 5]}, "object": "CL-QS-A3-8-CONTROLS-20261006-v1", "passed": true, "total": 39305, "z3_branches": {"3.1 inner band": 994, "3.1 outside": 787, "3.1 shell": 504, "3.1 trivial range": 400, "3.1 wide tail": 715, "3.2 band shells": 1483, "3.2 first band": 211, "3.2 outside": 804, "3.2 strip": 502}}
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_