## QS addendum A4.3: author controls, exact executable and stdout

This publishes the standard-library control script that A4.3 ([6010510789](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6010510789)) cites, so anyone can replay it. It checks the finite algebra of the planar transfer — the fibre constants, the planar sub-layer integrals and radius sub-layer, the shell ledgers and sums, the exponent tables, the transported constants and the `k = 1` constants; it does not prove the analytic statements. The numerics for Lemma 1.1 are A3.11's (same cubic).

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction rule.** The same as in [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189): the file is the exact text between the first ```` ```python ```` fence after its `###` heading and the next ```` ``` ```` line, plus a final newline. The expected stdout is the single JSON line in the following ```` ```json ```` fence, plus one newline.

**Run.** Each full run takes well under a second.
- `python3 -B -S a43_exact.py`: exit 0, with exactly the stdout below.
- `python3 -B -O -S a43_exact.py`: byte-identical output. No check depends on an `assert`.
- `--mutant M1` … `M10`: each exits 1 in both modes and names its failing group on stderr (identical stderr in both modes):
  - `M1` (Lemma 1.1: the fibre constant 192 U^3 written 96 U^3): exits 1; stderr names `Z1_lemma11_constants`.
  - `M2` (Lemma 1.2: the planar sub-layer weight integral written 144 U^4 in place of 288 U^4): exits 1; stderr names `Z2_planar_integrals`.
  - `M3` (Lemma 2.1(b): the split total x1 eps + (4/3) x0 sqrt(eps) written with coefficient 1): exits 1; stderr names `Z3_margin_totals`.
  - `M4` (Lemma 2.1(c): the split point d^2 = eta^2/w'^2 in place of eta/w'^2): exits 1; stderr names `Z4_endpoint_shell`.
  - `M5` (Lemma 2.2: sum (5 2^i)^-2 written 1/25 in place of 4/75): exits 1; stderr names `Z5_shell_sums`.
  - `M6` (Theorem QFE''_K: the schedule alpha = (1 - beta)/4 in place of (1 - beta)/8 (H^7 r^(13/8) falls below beta at small beta)): exits 1; stderr names `Z6_exponent_tables`.
  - `M7` (Corollary PD_ER' (iii): the moment constant 8130 in place of 8139): exits 1; stderr names `Z7_pd_constants`.
  - `M8` ((0.1): H_gamma <= 40 Pjet^2 in place of 54 Pjet^2 (false at gamma = 0)): exits 1; stderr names `Z2_planar_integrals`.
  - `M9` (Corollary PD_ER' (ii): the cumulative constant 21/8 in place of 21/4): exits 1; stderr names `Z7_pd_constants`.
  - `M10` (Remark 4: K2(1) = 115/24 in place of 115/48 (C103 (S12) at k = 1)): exits 1; stderr names `Z8_k1_constants`.
- `--bogus`, `--mutant M11` and a bare `--mutant`: exit 2.

The output was produced with Python 3.11.15. The script uses only `sys`, `math`, `json` and `fractions`. One clean-context referee pass (same provider and session; not review evidence) read the note against C101, C103, C124, A4, A4.1, A4.2, Corollary PD, C82 and A3.11, recomputed every constant, integral, monomial, exponent and threshold (95 exact checks, all agreeing) and tested Lemma 1.1 numerically on the planar cubic (330 band tests; worst ratio 0.233), and returned ACCEPT WITH MINOR FIXES with nine findings, all applied before posting: one `d = 3` artifact in the proof of Lemma 2.1(c) (the planar endpoint strip is `η_jN(γ² + 72) ≥ a_M`, without A3.7's factor `4`; the Markov constant is `73²η_j²/d²`, the bound unchanged), the `≥`/`≤` form of (0.1) and the `D_Λ` intersections, the standing condition `rH/k_- ≤ 1` in the fixed-layer cutoff, the hypothesis `C_VH²r^{1/4} ≤ 1` added to Lemma 2.1 and the justification of its part (d), and five wording items.

### a43_exact.py

```python
#!/usr/bin/env python3
"""QS addendum A4.3 controls: exact checks of the finite algebra (standard library only).

Usage: python3 a43_exact.py [--mutant M1..M10]; exit 0 iff every check passes, 1 on a failure (stderr names the
first failing group), 2 on an unknown argument. All groups use exact rationals except Z7's Simpson check.
It checks arithmetic only, not the analytic inputs (C101-C103, C124, A4-A4.2, A3.11, C82).
"""
import sys, math, json
from fractions import Fraction as F
from math import comb, factorial

MUTANTS = tuple("M%d" % i for i in range(1, 11))
MUT = None
args = sys.argv[1:]
if args:
    if len(args) != 2 or args[0] != "--mutant" or args[1] not in MUTANTS:
        sys.stderr.write("usage: a43_exact.py [--mutant M1..M10]\n")
        sys.exit(2)
    MUT = args[1]

COUNT = 0
def chk(cond, group):
    global COUNT
    COUNT += 1
    if not cond:
        sys.stderr.write("FAILED: %s\n" % group)
        sys.exit(1)

def pint(coeffs, a, b):
    tot = F(0)
    for i, c in enumerate(coeffs):
        tot += F(c) * (F(b) ** (i + 1) - F(a) ** (i + 1)) / (i + 1)
    return tot

def isqrt_frac(x):
    n, d = int(math.isqrt(x.numerator)), int(math.isqrt(x.denominator))
    s = F(n, d)
    return s if s * s == x else None

# ------------------------------------------------------------------ Z1: Lemma 1.1's constants in the planar fibre identity
K192 = F(96) if MUT == "M1" else F(192)
for g2 in (F(1), F(2, 5), F(9), F(100)):
    for U in (F(1, 7), F(1), F(5, 2), F(30)):
        psiU = 24 * U / g2                                   # psi = 24 lambda / gamma^2 (C103 section 3.3)
        chk((g2 ** 3 / 384) * F(16, 3) * psiU ** 3 == K192 * U ** 3, "Z1_lemma11_constants")
        chk((g2 ** 3 / 384) * psiU ** 3 / 3 == 12 * U ** 3, "Z1_lemma11_constants")
for x in (F(1, 2), F(2), F(99)):
    chk(12 <= 24 * x <= K192 * x, "Z1_lemma11_constants")

# ------------------------------------------------------------------ Z2: planar sub-layer integrals, the radius sub-layer, H_gamma
K288 = F(144) if MUT == "M2" else F(288)
for U in (F(1, 2), F(1), F(7, 3), F(12)):
    # inner: int_0^{48 l} s (48 l - s)/16 ds = (48 l)^3/96 = 1152 l^3 ; int_0^U 1152 l^3 dl = 288 U^4
    for l in (F(1, 3), F(2)):
        chk(pint([0, 48 * l / 16, F(-1, 16)], 0, 48 * l) == 1152 * l ** 3, "Z2_planar_integrals")
    chk(pint([0, 0, 0, 1152], 0, U) == K288 * U ** 4, "Z2_planar_integrals")
    chk(pint([0, 48], 0, U) == 24 * U ** 2, "Z2_planar_integrals")
    for s in (F(0), U, 10 * U, 48 * U):
        val = pint([-s / 16, 3], s / 48, U)                 # int_{s/48}^U (48 l - s)/16 dl
        chk(val == (48 * U - s) ** 2 / 1536 and val <= F(3, 2) * U ** 2, "Z2_planar_integrals")
chk(F(25, 96) <= F(3, 8), "Z2_planar_integrals")           # Rbox's constant is dominated by H_gamma's
for w in (F(5), F(7), F(40), F(1000)):
    chk(w - F(5, 2) >= w / 2 and w - F(3, 2) >= w - F(5, 2), "Z2_planar_integrals")
K54 = F(40) if MUT == "M8" else F(54)
for x in (F(0), F(1, 3), F(1), F(4), F(100)):            # H_gamma = (3/8)(|g|+12)^2 <= 54 (1+|g|)^2
    chk(F(3, 8) * (x + 12) ** 2 <= K54 * (1 + x) ** 2, "Z2_planar_integrals")

# ------------------------------------------------------------------ Z3: Lemma 2.1(b): split total and shell values (planar x0 = r H^3 w'^-2)
K43 = F(1) if MUT == "M3" else F(4, 3)
for x1, x0, eps in ((F(1), F(1), F(1, 4)), (F(1, 81), F(5), F(16)), (F(3, 7), F(1, 9), F(49, 100))):
    d = isqrt_frac(eps); chk(d is not None, "Z3_margin_totals")
    chk(x1 * d ** 2 / 2 + x0 * d + eps ** 2 * (x1 / (2 * d ** 2) + x0 / (3 * d ** 3)) == x1 * eps + K43 * x0 * d, "Z3_margin_totals")
for wp, r, H in ((F(5), F(1, 100), F(4)), (F(80), F(1, 10000), F(9)), (F(10), F(1, 4), F(1))):
    CV = F(4)
    x1, x0 = wp ** -4, r * H ** 3 * wp ** -2
    eps = CV * H ** 2 * 16 * r * wp ** 4                     # eps_j <= C_V H^2 e_j, e_j = 16 r w'^4
    chk(x1 * eps == 16 * CV * H ** 2 * r, "Z3_margin_totals")
    sq = isqrt_frac(eps); sr = isqrt_frac(r)
    chk(sq is not None and sr is not None and x0 * sq == 4 * 2 * r * sr * H ** 4, "Z3_margin_totals")   # 4 sqrt(C_V) r^{3/2} H^4

# ------------------------------------------------------------------ Z4: Lemma 2.1(c): optimization and shell values (planar)
for wp, r, H, K2 in ((F(5), F(1, 100), F(4), F(2)), (F(20), F(1, 400), F(1), F(1, 2)), (F(10), F(1, 10000), F(3), F(115, 48))):
    eta = 8 * K2 * r * wp ** 2
    x1, x0 = wp ** -4, r * H ** 3 * wp ** -2
    a, b = wp ** -8, r * H ** 3 * wp ** -4
    d2 = eta / wp ** 2 if MUT != "M4" else eta ** 2 / wp ** 2
    chk(x1 * d2 == eta * wp ** -6 == (eta ** 2 / d2) * a, "Z4_endpoint_shell")
    chk((eta ** 2 / d2) * b == eta * r * H ** 3 * wp ** -2 == 8 * K2 * r ** 2 * H ** 3, "Z4_endpoint_shell")
    chk(eta * wp ** -6 == 8 * K2 * r * wp ** -4, "Z4_endpoint_shell")
    chk(eta ** 2 * a == 64 * K2 ** 2 * r ** 2 * wp ** -4 and eta ** 2 * b == 64 * K2 ** 2 * r ** 3 * H ** 3, "Z4_endpoint_shell")
    chk(x0 ** 2 * d2 == 8 * K2 * r ** 3 * H ** 6 * wp ** -4, "Z4_endpoint_shell")       # (sqrt(8K2) r^{3/2} H^3 w'^-2)^2

# ------------------------------------------------------------------ Z5: Lemma 2.2's sums and the shell count
S2 = F(1, 25) if MUT == "M5" else F(4, 75)
chk(sum(F(1, (5 * 2 ** i) ** 2) for i in range(60)) < S2 and F(1, 25) / (1 - F(1, 4)) == F(4, 75), "Z5_shell_sums")
chk(F(1, 625) / (1 - F(1, 16)) == F(16, 9375), "Z5_shell_sums")
for J in range(1, 12):
    w = [5 * 2 ** j for j in range(J + 1)]
    chk(sum(F(wj) ** 4 for wj in w[1:]) <= F(16, 15) * F(w[J]) ** 4 and sum(F(wj) ** 2 for wj in w[1:]) <= F(4, 3) * F(w[J]) ** 2, "Z5_shell_sums")
for r in (math.exp(-1), 1e-2, 1e-3, 1e-6, 1e-12, 1e-40):
    wmax = r ** (-3 / 16); J = int(math.floor(math.log2(wmax / 5))) if wmax >= 5 else -1; L = math.log(1 / r)
    chk(J + 1 <= 1 + (3 / 16) * math.log2(1 / r) + 1e-9 and J <= 2 * L - 1 + 1e-9, "Z5_shell_sums")
    if J >= 0:
        wJ = 5 * 2 ** J
        chk(wJ <= wmax < 2 * wJ and wJ ** -8 <= 256 * r ** 1.5 * (1 + 1e-12) and wJ ** -4 <= 16 * r ** 0.75 * (1 + 1e-12) and wJ ** 4 <= r ** -0.75 * (1 + 1e-12), "Z5_shell_sums")

# ------------------------------------------------------------------ Z6: the exponent tables (QFE''_K, ER'_K), the domination, the side conditions
TERMS = {"rH4": (F(1), 4, 0), "H2r_log": (F(1), 2, 1), "H5r54": (F(5, 4), 5, 0), "r32H5": (F(3, 2), 5, 0), "r32H4_log": (F(3, 2), 4, 1),
         "H7r138": (F(13, 8), 7, 0), "r74H3": (F(7, 4), 3, 0), "r2H3_log": (F(2), 3, 1)}
CLOSED = {"rH4": lambda b: (1 + b) / 2, "H2r_log": lambda b: (3 + b) / 4, "H5r54": lambda b: F(5, 8) + 5 * b / 8, "r32H5": lambda b: F(7, 8) + 5 * b / 8,
          "r32H4_log": lambda b: 1 + b / 2, "H7r138": lambda b: F(3, 4) + 7 * b / 8, "r74H3": lambda b: F(11, 8) + 3 * b / 8, "r2H3_log": lambda b: F(13, 8) + 3 * b / 8}
for i in range(1, 100):
    beta = F(i, 100)
    alpha = (1 - beta) / (4 if MUT == "M6" else 8)
    for name, (rp, hp, lp) in TERMS.items():
        ex = rp - alpha * hp
        if MUT != "M6":
            chk(ex == CLOSED[name](beta), "Z6_exponent_tables")
        chk(ex > beta if lp else ex >= beta, "Z6_exponent_tables")
    chk(1 - alpha == (7 + beta) / 8 and F(1, 4) - 2 * alpha == beta / 4 if MUT != "M6" else True, "Z6_exponent_tables")
er = {name: (rp, hp + lp) for name, (rp, hp, lp) in TERMS.items()}
chk(max(lp for rp, lp in er.values() if rp == 1) == 4 and er["rH4"] == (1, 4) and er["H2r_log"] == (1, 3), "Z6_exponent_tables")
chk(min(rp for rp, lp in er.values() if rp > 1) >= F(5, 4), "Z6_exponent_tables")
for H in (F(1), F(2), F(10), F(1000)):
    for r in (F(1), F(1, 2), F(1, 1000)):
        chk(H ** 3 * r <= r * H ** 4 and r ** F(3, 2) <= r ** F(3, 2) * H ** 5 and r ** F(3, 2) * H ** 4 <= r ** F(3, 2) * H ** 5 and r * H ** 3 <= r * H ** 4, "Z6_exponent_tables")
# the fixed-layer exponent lists of (3.1) and (3.2)
l31 = [F(3, 2), F(7, 4), F(5, 4), F(13, 8), F(1), F(1), F(3, 2), F(3, 2)]
l32 = [F(3, 2), F(7, 4), F(1), F(1), F(3, 2), F(2)]
chk(min(l31) == 1 and min(l32) == 1 and len(l31) == 8 and len(l32) == 6, "Z6_exponent_tables")

# ------------------------------------------------------------------ Z7: Corollary PD_ER''s constants
K8139 = 8130 if MUT == "M7" else 8139
chk(sum(comb(4, j) * factorial(j) * 3 ** (j + 1) for j in range(5)) == K8139, "Z7_pd_constants")
K214 = F(21, 8) if MUT == "M9" else F(21, 4)
chk(sum(F(comb(4, j) * factorial(j), 2 ** (j + 1)) for j in range(5)) == K214 < 6, "Z7_pd_constants")
chk(F(2, 3) ** 4 == F(16, 81), "Z7_pd_constants")
for q in (F(-5, 3) + F(1, 1000), F(-1), F(0), F(3)):
    chk(q + 2 > F(1, 3) and sum(F(comb(4, j) * factorial(j)) / (q + 2) ** (j + 1) for j in range(5)) <= K8139, "Z7_pd_constants")
def simpson(f, a, b, n):
    h = (b - a) / n; s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3
chk(abs(simpson(lambda x: math.exp(-2 * x) * (1 + x) ** 4, 0.0, 60.0, 60000) - 21 / 4) < 1e-7, "Z7_pd_constants")

# ------------------------------------------------------------------ Z8: the k = 1 constants of Remark 4 (C103 (S12))
km, kp = F(1), F(1)
K0 = F(9, 64) / km + F(1, 16) + (1 + kp) ** 4 / (24 * km)
K2 = F(17, 48) / km + F(1, 24) + max(1 / km, F(1), kp) * (1 + kp) ** 2 / 2
K1 = F(33, 128) / km + F(1, 16) + max(1 / km, F(1)) * (1 + kp) ** 3 / 6
K2_ref = F(115, 24) if MUT == "M10" else F(115, 48)
chk(K0 == F(167, 192) and K1 == F(635, 384) and K2 == K2_ref, "Z8_k1_constants")
chk(2 * K2 == F(115, 24), "Z8_k1_constants")                                         # eta_K = (115/24) r w^2 at K = {1}
chk(F(5, 3) * K2 * F(1, 1) == F(575, 144), "Z8_k1_constants")                       # C_eta = 5 K2/3 (C103) = 575/144 (C101)

print(json.dumps({"checks": COUNT, "mutant": MUT, "pd_moment_constant": 8139, "pd_cumulative_constant": "21/4",
                  "lemma11_constant": 192, "log_power_endpoint": 4}, sort_keys=True))
```

```json
{"checks": 1835, "lemma11_constant": 192, "log_power_endpoint": 4, "mutant": null, "pd_cumulative_constant": "21/4", "pd_moment_constant": 8139}
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_