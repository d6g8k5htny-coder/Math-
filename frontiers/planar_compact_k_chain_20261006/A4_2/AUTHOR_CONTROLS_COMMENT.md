## QS addendum A4.2: author controls, exact executable and stdout

This is the standard-library script behind [A4.2 (5974565257)](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5974565257). It checks finite algebra, exact sums and exponent bookkeeping only. It does not prove C103's or C124's analytic inputs, C82 LB, the Gaussian moment bounds or any measure-theoretic step.

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`), A4.2's author. Scientific effect: NONE.

**Extraction rule.**
- The file is the exact text between the ```` ```python ```` fence under the `###` heading and the next ```` ``` ```` line, plus one final newline.
- The expected stdout is the text in the following ```` ```text ```` fence, plus one final newline.
- The byte counts below include those newlines.

**Run.**
- `python3 -B -S a42_exact.py`: exit 0, with exactly the stdout shown. A run takes about 2 seconds.
- `-O` mode and plain `python3`: byte-identical output.
- `python3 a42_exact.py BOGUS`: exit 2.
- Each of the six mutant labels exits 1 (table below). B5's quadrature uses deterministic IEEE floats against an exact closed form, with relative tolerance `10⁻⁶`.

The output was produced with Python 3.11.15.

**Mutants.** Each was actually run; each exits 1. `DB_HALF` changes the total, because a guarded branch then runs more often.

| label | change | failing group | failed checks |
|---|---|---|---:|
| `K2_UNIT` | `K₂(1)` for `K₂(K)` | B0 | 1 of 26300 |
| `DB_HALF` | `a = K₀(K)e` | B2 | 437 of 26303 |
| `PD_79` | density error `ℓ^{7/9}` | B5 | 2 of 26300 |
| `CUM_169` | cumulative error `t^{16/9}` | B5 | 1 of 26300 |
| `FRAC_109` | fraction error `ℓ^{10/9}` | B5 | 1 of 26300 |
| `LOG_ONE` | `log(k/ℓ) ≤ log(1/ℓ)` | B5 | 994 of 26300 |

### a42_exact.py

- **File:** 10859 bytes, SHA-256 `ea4945278f229f11e61872a4d1dfc51e754277175271b6945b28e9dd3af21af9`.
- **Stdout:** 442 bytes, SHA-256 `60a3711bbcd118b6250d349e8d3a56c6cb3a7faca604c6be2da8e9480f66f3e0`.

```python
#!/usr/bin/env python3
"""QS addendum A4.2 (compact-K endpoint rate) and Corollary PD_ER: exact rational checks, standard library only.

Author-side controls (Anthropic Claude, session_01NMeKEismAyeqgdB4sy2NJU, for Dylan Roy; delegated AI work).
They check finite algebra, exact sums and exponent bookkeeping only. They do not prove C103's or C124's
analytic inputs, C82 LB, the Gaussian moment bounds or any measure-theoretic step.

Usage: python3 a42_exact.py [MUTANT]   (exit 0 pass, 1 fail, 2 unknown label)
Mutants (each must exit 1):
  K2_UNIT     eta_K computed with K2(1) = 115/48 for every K
  DB_HALF     the decision constant a = K0(K) e in place of 2 K0(K) e
  PD_79       the PD_ER density error l^(7/9) in place of l^(8/9)
  CUM_169     the cumulative error t^(16/9) in place of t^(17/9)
  FRAC_109    the nonselected-fraction error l^(10/9) in place of l^(11/9)
  LOG_ONE     the conversion log(k/l) <= log(1/l) in place of log(k/l) <= 2 log(1/l)
"""
import math
import random
import sys
from fractions import Fraction as F

MUTANTS = ("K2_UNIT", "DB_HALF", "PD_79", "CUM_169", "FRAC_109", "LOG_ONE")
MUT = None
if len(sys.argv) > 1:
    MUT = sys.argv[1]
    if len(sys.argv) > 2 or MUT not in MUTANTS:
        print("unknown mutant label: %s" % " ".join(sys.argv[1:]))
        sys.exit(2)

RNG = random.Random(42_5974351360)
RESULTS, FAILS = [], []


class Group:
    def __init__(self, name):
        self.name, self.n, self.bad = name, 0, 0

    def check(self, ok, msg=""):
        self.n += 1
        if not ok:
            self.bad += 1
            if len(FAILS) < 12:
                FAILS.append("%s: %s" % (self.name, msg))

    def close(self):
        RESULTS.append((self.name, self.n - self.bad, self.n))


def rq(lo, hi, den=97):
    a, b = int(math.floor(F(lo) * den)), int(math.floor(F(hi) * den))
    return F(RNG.randint(a, b), den)


def rq_pos(lo, hi, den=97):
    while True:
        x = rq(lo, hi, den)
        if x > 0:
            return x


def K0(km, kp):
    return F(9, 64) / km + F(1, 16) + (1 + kp)**4 / (24 * km)


def K2(km, kp):
    if MUT == "K2_UNIT":
        return F(115, 48)
    return F(17, 48) / km + F(1, 24) + max(1 / km, F(1), kp) * (1 + kp)**2 / 2


# =====================================================================
# B0  the compact-K constants (C103 (S12)) and eta_K
# =====================================================================
g = Group("B0 compact-K constants")
g.check(K0(F(1), F(1)) == F(167, 192) and (MUT == "K2_UNIT" or K2(F(1), F(1)) == F(115, 48)), "K = {1}: 167/192 and 115/48")
g.check(K0(F(1, 2), F(2)) == F(227, 32), "K = [1/2, 2]: K0 = 227/32")
g.check(K2(F(1, 2), F(2)) == F(39, 4), "K = [1/2, 2]: K2 = 39/4")
for _ in range(2000):
    km = rq_pos(F(1, 10), 3)
    kp = km + rq(0, 4)
    r, w = rq_pos(F(1, 10**4), F(1, 10), 10**4), rq(5, 50)
    etaK = 2 * K2(km, kp) * r * w**2
    g.check((5 * K2(km, kp) / 3) * r * w**2 == F(5, 6) * etaK, "C_eta r w^2 = (5/6) eta_K")
    g.check(K2(km, kp) >= F(115, 48) or km > 1, "K2(K) >= K2({1}) whenever k_- <= 1")
g.close()

# =====================================================================
# B1  Lemma JB_K: the Jacobian chain and the chart
# =====================================================================
g = Group("B1 Lemma JB_K Jacobian and chart")
for _ in range(3000):
    r, k = rq_pos(F(1, 1000), F(1, 2), 1000), rq_pos(F(1, 10), 5)
    jac = (r / k) * (1 / k) * (1 / k**2)                # A = -r lam/k, B_phys = B/k, C_phys = C/k^2
    g.check(jac == r / k**4 and r**-5 * r**4 * jac == 1 / k**4, "r/k^4 Jacobian and the k^-4 prefactor")
    gam, B, C = rq(-4, 4), rq(-4, 4), rq(-4, 4)
    if gam == 0:
        continue
    D, J = gam**2 - 12 * B, 8 * gam**3 - 144 * B * gam + 576 * C
    lam = rq_pos(0, 3)
    psi, c, R = 24 * lam / gam**2, D / gam**2, J / gam**3
    g.check((24 * lam - D) * (24 * lam + D) / 16 * gam**2 / 24 == gam**6 * (psi**2 - c**2) / 384, "w d lambda = (gamma^6/384)(psi^2 - c^2) d psi")
    g.check(gam**6 * abs(c)**3 == abs(D)**3 and gam**6 * R**2 == J**2, "pole cancellation")
g.close()

# =====================================================================
# B2  Lemma DB_K: the decision constant and the shell sums
# =====================================================================
g = Group("B2 Lemma DB_K")
for _ in range(3000):
    km = rq_pos(F(1, 10), 3)
    kp = km + rq(0, 4)
    N, e = rq_pos(1, 50), rq_pos(F(1, 10**6), F(1, 10**3), 10**7)
    a = (K0(km, kp) if MUT == "DB_HALF" else 2 * K0(km, kp)) * e
    E0 = K0(km, kp) * N * e * rq(0, 1, 1000)        # E0 <= K0(K) N e
    mu = 2 * E0 * rq(0, 1, 1000)                       # a decision error: |mu| <= 2 E0
    g.check(mu <= a * N, "|mu| <= 2 E0 <= 2 K0(K) N e = a N")
    if a <= F(1, 4):
        m = 0
        while not (F(1, 4) <= 2**m * a < F(1, 2)):
            m += 1
        b = rq_pos(0, 1, 1000)
        g.check(sum(2 * a / 2**j + b / 4**j for j in range(m)) <= 4 * a + F(4, 3) * b, "shell sums <= 4a + (4/3) b")
g.close()

# =====================================================================
# B3  Lemma ES_K (gap-independent constants) and Lemma FT_K
# =====================================================================
g = Group("B3 Lemmas ES_K and FT_K")
for n in range(1, 80):
    g.check(F((2 * n)**n, 12**n * math.factorial(n)) <= F(1, 2**n), "series term <= 2^-n at eps0 = 1/(12 (1 + S)^2)")
for _ in range(2000):
    r, Jr, CK = rq_pos(F(1, 1000), F(1, 2), 1000), rq_pos(1, 9), rq_pos(F(1, 10), 6)
    Lt = CK * r * Jr**2
    integral = Lt**3 / 3 + Lt * Lt**2 / 2             # int_0^Lt l (l + C_K r J^2) dl with the same C_K
    g.check(integral == F(5, 6) * CK**3 * r**3 * Jr**6, "(S29): int_0^(C_K r J^2) l (l + C_K r J^2) dl = (5/6) C_K^3 r^3 J^6")
    g.check(r**2 * Jr**4 * integral == F(5, 6) * CK**3 * r**5 * Jr**10, "near weight C r^5 J^10")
g.close()

# =====================================================================
# B4  Theorem ER_K: the fixed-layer exponents and the exhaustion table
# =====================================================================
g = Group("B4 Theorem ER_K ledger")
bw = F(1, 12)
e_ = 1 - 4 * bw
eta_ = 1 - 2 * bw                                       # eta_K ~ r w^2
fixed = [8 * bw, 1 + 4 * bw, e_, 1 + e_ / 2, eta_, 1 + eta_ / 2, e_, F(1), 2 * e_, 2 - 4 * bw, 2 - 2 * bw]
g.check(fixed == [F(2, 3), F(4, 3), F(2, 3), F(4, 3), F(5, 6), F(17, 12), F(2, 3), F(1), F(4, 3), F(5, 3), F(11, 6)], "fixed-Lambda exponents")
g.check(3 + min(fixed) == F(11, 3), "Q_r^W(D_Lambda, H_r Delta E) = O(r^(11/3))")
w_, ee, r_, H_ = (F(-1, 12), F(-1, 3)), (F(2, 3), F(-4, 3)), (F(1), F(0)), (F(0), F(1))
eta = (F(1) + 2 * w_[0], 2 * w_[1])                    # eta_K ~ r w^2


def mono(*parts):
    return (sum(p[0] * k for p, k in parts), sum(p[1] * k for p, k in parts))


rows = [mono((w_, -8)), mono((r_, 1), (H_, 3), (w_, -4)), mono((H_, 4), (ee, 1)), mono((r_, 1), (H_, 5), (ee, F(1, 2))),
        mono((H_, 3), (eta, 1)), mono((r_, 1), (H_, 4), (eta, F(1, 2))), ee, mono((r_, 1), (H_, 4)), mono((H_, 3), (ee, 2)),
        mono((H_, 5), (r_, 2), (w_, 4)), mono((H_, 7), (r_, 2), (w_, 2))]
for (x, y) in rows:
    g.check(x > F(2, 3) or (x == F(2, 3) and y <= F(8, 3)), "every term is O(r^(2/3) H^(8/3))")
g.check(max(y for (x, y) in rows if x == F(2, 3)) == F(8, 3), "the leading terms carry exactly H^(8/3)")
for name, (x, y) in {"rH": mono((r_, 1), (H_, 1)), "r w": mono((r_, 1), (w_, 1)), "e": ee, "H^2 e": mono((H_, 2), (ee, 1)), "eta_K": eta}.items():
    g.check(x > 0, "admissibility: %s -> 0" % name)
g.close()

# =====================================================================
# B5  Corollary PD_ER: exponents, the log conversions and the moment integral
# =====================================================================
g = Group("B5 Corollary PD_ER")
rel = F(2, 3) / 3                                      # r^(2/3) with r = (l/k)^(1/3)
dens = F(7, 9) if MUT == "PD_79" else F(2, 3) + rel
g.check(dens == F(8, 9) and dens == (2 + F(2, 3)) / 3, "(i): density error l^(8/9) = l^((2+2/3)/3), PD (v)'s supremum")
g.check(min(rel, F(1, 3)) == rel, "the A_r - A_0 = O(l^(1/3)) term is dominated by l^(2/9)")
cum = F(16, 9) if MUT == "CUM_169" else 1 + dens
g.check(cum == F(17, 9), "(ii): cumulative error t^(17/9)")
frac = F(10, 9) if MUT == "FRAC_109" else 1 + rel
g.check(frac == F(11, 9), "(iv): fraction error l^(11/9)")
def moment_const(a1):
    """int_0^1 s^(a1 - 1) (1 + log(1/s))^3 ds = sum_j C(3, j) j!/a1^(j+1)  (s = e^-x)"""
    return sum(math.comb(3, j) * math.factorial(j) / a1**(j + 1) for j in range(4))


def quad(a1, X=80.0, n=200000):
    """Simpson's rule for int_0^X exp(-a1 x)(1 + x)^3 dx (deterministic floats)."""
    h = X / n
    tot = 0.0
    for i in range(n + 1):
        x = i * h
        wgt = 1 if i in (0, n) else (4 if i % 2 else 2)
        tot += wgt * math.exp(-a1 * x) * (1 + x)**3
    return tot * h / 3


for a1 in (F(2, 9) + F(1, 10), F(1, 2), F(17, 9), F(4)):
    exact = moment_const(a1)
    g.check(abs(quad(float(a1)) - float(exact)) <= 1e-6 * float(exact), "moment closed form = quadrature of exp(-a x)(1 + x)^3")
g.check(sum(math.comb(3, j) * math.factorial(j) * F(9, 2)**(j + 1) for j in range(4)) == F(24579, 8) < 3073, "sup over q > -5/3: 24579/8 < 3073")
g.check(moment_const(F(17, 9)) < 3, "q = 0: the constant is < 3 (statement (ii))")
for _ in range(400):
    q = rq(F(-5, 3) + F(1, 97), 4)
    a1 = q + F(17, 9)                                  # (q + 8/9) + 1
    g.check(a1 > F(2, 9) and moment_const(a1) <= F(24579, 8), "q > -5/3: q + 17/9 > 2/9 and the constant <= 24579/8")
    A, Bv = rq(1, 20), rq(0, 20)                       # A = log(1/t) >= 1, Bv = log(1/s) >= 0
    g.check(A + Bv <= A * (1 + Bv), "log(1/l) = log(1/t) + log(1/s) <= log(1/t)(1 + log(1/s))")
    x = rq(0, 30)
    g.check((1 + x)**8 <= (1 + x)**9, "(1 + x)^(8/3) <= (1 + x)^3 for x >= 0 (cubes: (1 + x)^8 <= (1 + x)^9)")
# the conversion: for l <= 1/k_+ and k in K, (l/k)^(2/9) <= (l/k_-)^(2/9) and log(k/l) <= 2 log(1/l)
cfac = 1 if MUT == "LOG_ONE" else 2
for _ in range(1000):
    km = rq_pos(F(1, 10), 20)
    kp = km + rq(0, 20)
    k = km + (kp - km) * rq(0, 1, 1000)
    l = rq_pos(F(1, 10**6), F(1, 1) / kp, 10**6)
    if l <= 1 / kp and l < 1:
        g.check(l / k <= l / km, "r^(2/3) = (l/k)^(2/9) <= k_-^(-2/9) l^(2/9)")
        g.check(k / l <= (1 / l)**cfac, "log(k/l) <= 2 log(1/l), i.e. k/l <= l^-2 (k <= 1/l)")
g.close()

# ---------------------------------------------------------------------
total = sum(t for _, _, t in RESULTS)
passed = sum(p for _, p, _ in RESULTS)
for name, p, t in RESULTS:
    print("%-46s %6d/%-6d %s" % (name, p, t, "PASS" if p == t else "FAIL"))
print("mutant: %s" % (MUT if MUT else "none"))
print("total checks: %d; failures: %d" % (total, total - passed))
for f_ in FAILS:
    print("  FAIL " + f_)
sys.exit(0 if passed == total else 1)
```

```text
B0 compact-K constants                           4003/4003   PASS
B1 Lemma JB_K Jacobian and chart                 8992/8992   PASS
B2 Lemma DB_K                                    5997/5997   PASS
B3 Lemmas ES_K and FT_K                          4079/4079   PASS
B4 Theorem ER_K ledger                             19/19     PASS
B5 Corollary PD_ER                               3210/3210   PASS
mutant: none
total checks: 26300; failures: 0
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_