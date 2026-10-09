## QS addendum A3.11: author controls, exact executable and stdout

This publishes the standard-library control script that A3.11 ([6009956838](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6009956838)) cites, so anyone can replay it. It checks the finite algebra of the note — the constants of the localized band lemma, the sub-layer integrals, the shell ledgers and their sums, the exponent tables and the transported constants — and runs one numeric sanity check of Lemma 1.1 on sampled cubics; it does not prove the analytic statements, and it does not replace C82.

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction rule.** The same as in [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189): the file is the exact text between the first ```` ```python ```` fence after its `###` heading and the next ```` ``` ```` line, plus a final newline. The expected stdout is the single JSON line in the following ```` ```json ```` fence, plus one newline.

**Run.** Each full run takes about 1 s.
- `python3 -B -S a311_exact.py`: exit 0, with exactly the stdout below.
- `python3 -B -O -S a311_exact.py`: byte-identical output. No check depends on an `assert`.
- `--mutant M1` … `M12`: each exits 1 in both modes and names its failing group on stderr (identical stderr in both modes):
  - `M1` (Lemma 1.1: the fibre constant 192 U^3 written 96 U^3): exits 1; stderr names `Z1_lemma11_constants`.
  - `M2` (Z2: the critical value written (sigma + 1)/2 - psi Z^2/144 in place of (sigma - 1)/2 - psi Z^2/144): exits 1; stderr names `Z2_cubic_identities`.
  - `M3` (Lemma 1.2: the sub-layer weight integral written 36 U^4 in place of 72 U^4): exits 1; stderr names `Z3_sublayer_integrals`.
  - `M4` (Lemma 2.1(b): the split total x1 eps + (4/3) x0 sqrt(eps) written with coefficient 1 in place of 4/3): exits 1; stderr names `Z4_margin_totals`.
  - `M5` (Lemma 2.1(c): the split point d^2 = eta^2/w'^2 in place of eta/w'^2 (the strip and the Markov term no longer balance)): exits 1; stderr names `Z5_endpoint_shell`.
  - `M6` (Lemma 2.2: sum_{i>=0} (5 2^i)^-2 written 1/25 in place of 4/75): exits 1; stderr names `Z6_shell_sums`.
  - `M7` (Theorem QFE3': the schedule alpha = (1 - beta)/4 in place of (1 - beta)/8 (r H^7 falls below beta)): exits 1; stderr names `Z7_exponent_tables`.
  - `M8` (Corollary PD3' (iii): the moment constant 46149300 in place of 46149330): exits 1; stderr names `Z8_pd3_constants`.
  - `M9` (Z9: the band bound (16/3) x psi_U^3 replaced by (1/2) x psi_U^3 (violated by the sampled cubics)): exits 1; stderr names `Z9_numeric_band`.
  - `M10` (Z2: det Hess = -(c - sigma psi)/4 in place of (c - sigma psi)/4 (C82 (5))): exits 1; stderr names `Z2_cubic_identities`.
  - `M11` (Corollary PD3' (ii): the cumulative constant 2325/8 in place of 2325/16): exits 1; stderr names `Z8_pd3_constants`.
  - `M12` (Lemma 1.2: Theta_bullet(gamma) <= 40 P^2 in place of 49 P^2 (false at gamma = t = 0)): exits 1; stderr names `Z3_sublayer_integrals`.
- `--bogus`, `--mutant M13` and a bare `--mutant`: exit 2.

The output was produced with Python 3.11.15. The script uses only `sys`, `math`, `json` and `fractions`. Z9's `saddles()` types the critical points by C82 (5), `det Hess = (c − σψ)/4`; the first draft of this script carried a wrong mixed partial there (`−cZ/24` for `−cZ/12`), which the clean-context referee caught — it affected only the controls and the exploration's density figure, not the note's proof, which cites C82 §2 (A3.11 §7). One clean-context referee pass (same provider and session; not review evidence) read the note against A3.4–A3.10 and C82, recomputed every displayed constant and exponent independently (sympy; all matched), ran its own branch-wise numerics for Lemma 1.1, and returned ACCEPT WITH MINOR FIXES with eight findings, all applied before posting: the Hessian identity above; the conditionality sentence; the labels (9.4), C82 (12)–(14) and C82 (4); the hard-gap strips of the λ₂-bands, which the localized Lemma 1.3 makes unnecessary (the referee's point led to the simplification of Lemmas 1.3–1.4 and of (3.1)–(3.2)); the exact inner integral of (1.3); Z7's derived powers; Z9's branch-wise form. A delta re-check confirmed the revised Lemmas 1.3–1.4, the ledgers and the script.

### a311_exact.py

```python
#!/usr/bin/env python3
"""QS addendum A3.11 controls: exact checks of the finite algebra (standard library only).

Usage: python3 a311_exact.py [--mutant M1..M12]; exit 0 iff every check passes, 1 on a failure (stderr names the
first failing group), 2 on an unknown argument. Groups Z1-Z8 use exact rationals (fractions.Fraction); Z9 is a
floating-point sanity check of Lemma 1.1 on a deterministic sample (it is not a proof and does not replace C82).
It checks arithmetic only, not the analytic inputs (A3.4-A3.10, C82, [P], [R]).
"""
import sys, math, json
from fractions import Fraction as F
from math import comb, factorial

MUTANTS = tuple("M%d" % i for i in range(1, 13))
MUT = None
args = sys.argv[1:]
if args:
    if len(args) != 2 or args[0] != "--mutant" or args[1] not in MUTANTS:
        sys.stderr.write("usage: a311_exact.py [--mutant M1..M12]\n")
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
    """Exact integral over [a, b] of the polynomial with rational coefficients coeffs[i] x^i."""
    tot = F(0)
    for i, c in enumerate(coeffs):
        tot += F(c) * (F(b) ** (i + 1) - F(a) ** (i + 1)) / (i + 1)
    return tot

# ------------------------------------------------------------------ Z1: Lemma 1.1's constants
K192 = F(96) if MUT == "M1" else F(192)
for g2 in (F(1), F(1, 3), F(7, 2), F(25)):          # gamma^2
    for U in (F(1, 10), F(1), F(13, 4), F(50)):
        psiU = 24 * U / g2
        band = (g2 ** 3 / 384) * F(16, 3) * psiU ** 3          # two branches x 2x x (4/3) psi_U^3, per unit x
        chk(band == K192 * U ** 3, "Z1_lemma11_constants")
        whole = (g2 ** 3 / 384) * psiU ** 3 / 3
        chk(whole == 12 * U ** 3, "Z1_lemma11_constants")
for x in (F(1, 2), F(3, 4), F(5), F(1000)):
    chk(12 <= 24 * x <= K192 * x, "Z1_lemma11_constants")

# ------------------------------------------------------------------ Z2: the sheared cubic's critical identities (exact)
def P_val(u, Z, c, R, psi):
    return 2 * u ** 3 - F(3, 2) * u - F(1, 2) - (psi + 2 * c * u) * Z ** 2 / 48 + R * Z ** 3 / 3456
SIGN = F(1) if MUT == "M2" else F(-1)
pts = [(F(3, 2), F(2), F(5, 4)), (F(-1, 3), F(7, 3), F(2)), (F(5, 2), F(-3, 5), F(11, 2)), (F(1, 7), F(9), F(1, 3)),
       (F(-4, 3), F(1, 2), F(10)), (F(2), F(4), F(2))]
for sigma, Z, psi in pts:
    c = 36 * (sigma ** 2 - 1) / Z ** 2                 # sigma^2 - 1 = c Z^2/36
    R = 48 * (psi - c * sigma) / Z                     # R Z = 48 (psi - c sigma)
    u = -sigma / 2
    dPu = 6 * u ** 2 - F(3, 2) - c * Z ** 2 / 24
    dPZ = -(psi + 2 * c * u) * Z / 24 + R * Z ** 2 / 1152
    chk(dPu == 0 and dPZ == 0, "Z2_cubic_identities")
    chk(P_val(u, Z, c, R, psi) == (sigma + SIGN) / 2 - psi * Z ** 2 / 144, "Z2_cubic_identities")
    # explicit psi-derivative at fixed (u, Z): -Z^2/48
    dpsi = F(1, 1000)
    chk((P_val(u, Z, c, R, psi + dpsi) - P_val(u, Z, c, R, psi)) / dpsi == -Z ** 2 / 48, "Z2_cubic_identities")
    Puu = 12 * u
    PZZ = -(psi + 2 * c * u) / 24 + R * Z / 576
    PuZ = -c * Z / 12
    det = Puu * PZZ - PuZ ** 2
    DS = F(-1) if MUT == "M10" else F(1)
    chk(det == -sigma * (psi - c * sigma) / 4 - c ** 2 * Z ** 2 / 144 == DS * (c - sigma * psi) / 4, "Z2_cubic_identities")

# ------------------------------------------------------------------ Z3: Lemma 1.2's sub-layer integrals and bounds
K72 = F(36) if MUT == "M3" else F(72)
for U in (F(1, 3), F(1), F(9, 2), F(20)):
    # int_0^U int_0^{12 l} s (12 l - s) ds dl = 72 U^4 ;  int_0^U int_0^{12 l} ds dl = 6 U^2
    # inner: int_0^{12l} s(12 l - s) ds = 12 l (12 l)^2/2 - (12 l)^3/3 = 288 l^3 ; then int_0^U 288 l^3 dl = 72 U^4
    for l in (F(1, 2), F(3)):
        chk(pint([0, 12 * l, -1], 0, 12 * l) == 288 * l ** 3, "Z3_sublayer_integrals")
    chk(pint([0, 0, 0, 288], 0, U) == K72 * U ** 4, "Z3_sublayer_integrals")
    chk(pint([0, 12], 0, U) == 6 * U ** 2, "Z3_sublayer_integrals")
    for s in (F(0), U / 2, 3 * U, 12 * U):
        # int_{s/12}^{U} (12 l - s) dl <= 12 U^2 for 0 <= s <= 12 U
        val = pint([-s, 12], s / 12, U)
        chk(0 <= val <= 12 * U ** 2, "Z3_sublayer_integrals")
# U <= 4 Theta / w^2 from Theta/(w - 5/2)^2 and (w - 5/2)^2 >= w^2/4 for w >= 5; (w - 3/2)^2 >= w^2/4 for w >= 3
for w in (F(5), F(6), F(10), F(80), F(1000)):
    chk((w - F(5, 2)) ** 2 >= w ** 2 / 4 and (w - F(3, 2)) ** 2 >= w ** 2 / 4, "Z3_sublayer_integrals")
# Theta_R(g) = (289/864)(|g|+12)^2 <= 49 (1+|t|)^2 when |g| <= |t|: the ratio (x+12)^2/(1+x)^2 decreases in x
for x in (F(0), F(1, 2), F(1), F(3), F(10), F(100)):
    chk(F(289, 864) * (x + 12) ** 2 <= 49 * (1 + x) ** 2 and F(25, 96) * (x + 12) ** 2 <= 49 * (1 + x) ** 2, "Z3_sublayer_integrals")
K49 = F(40) if MUT == "M12" else F(49)
chk((F(0) + 12) ** 2 * F(289, 864) <= K49 and (F(0) + 12) ** 2 * F(25, 96) <= K49, "Z3_sublayer_integrals")

# ------------------------------------------------------------------ Z4: Lemma 2.1(b)'s split totals and shell values
K43 = F(1) if MUT == "M4" else F(4, 3)
for x1, x0, eps in ((F(1), F(1), F(1, 4)), (F(1, 16), F(3), F(9)), (F(7, 3), F(1, 5), F(25, 36)), (F(1, 625), F(2), F(1, 100))):
    d = F(int(math.isqrt(eps.numerator)), int(math.isqrt(eps.denominator)))
    chk(d * d == eps, "Z4_margin_totals")
    strip = x1 * d ** 2 / 2 + x0 * d
    away = eps ** 2 * (x1 / (2 * d ** 2) + x0 / (3 * d ** 3))
    chk(strip + away == x1 * eps + K43 * x0 * d, "Z4_margin_totals")
    # the hard-gap margin: (x1 d^2 + x0 d) + (5/24) x1 eps^4 d^-6 + (5/18) x0 eps^2 d^-3 at d = sqrt(eps)
    tot2 = (x1 * d ** 2 + x0 * d) + F(5, 24) * x1 * eps ** 4 / d ** 6 + F(5, 18) * x0 * eps ** 2 / d ** 3
    chk(tot2 == F(29, 24) * x1 * eps + F(23, 18) * x0 * d, "Z4_margin_totals")
# shell values: x1 = w'^-4, x0 = r H^6 w'^-2, eps = C_V H^2 * 16 r w'^4 (C_V = 4, r, H perfect squares for exactness)
for wp, r, H in ((F(5), F(1, 100), F(4)), (F(40), F(1, 10000), F(9)), (F(5, 1), F(1, 4), F(1))):
    CV = F(4)
    x1, x0 = wp ** -4, r * H ** 6 * wp ** -2
    eps = CV * H ** 2 * 16 * r * wp ** 4
    chk(x1 * eps == 16 * CV * H ** 2 * r, "Z4_margin_totals")
    sq = F(int(math.isqrt(eps.numerator)), int(math.isqrt(eps.denominator)))
    chk(sq * sq == eps and x0 * sq == 4 * F(2) * r * F(int(math.isqrt((r).numerator)), int(math.isqrt((r).denominator))) * H ** 7, "Z4_margin_totals")

# ------------------------------------------------------------------ Z5: Lemma 2.1(c)'s optimization and shell values
for wp, r, H, K2 in ((F(5), F(1, 100), F(4), F(2)), (F(20), F(1, 400), F(1), F(1, 2)), (F(10), F(1, 10000), F(3), F(8))):
    eta = 8 * K2 * r * wp ** 2
    x1, x0 = wp ** -4, r * H ** 6 * wp ** -2
    a, b = wp ** -8, r * H ** 6 * wp ** -4
    d2 = eta / wp ** 2 if MUT != "M5" else eta ** 2 / wp ** 2          # d^2 = eta / w'^2
    chk(x1 * d2 == eta * wp ** -6 and (eta ** 2 / d2) * a == eta * wp ** -6, "Z5_endpoint_shell")   # equalized
    chk((eta ** 2 / d2) * b == eta * r * H ** 6 * wp ** -2, "Z5_endpoint_shell")
    chk(eta * wp ** -6 == 8 * K2 * r * wp ** -4, "Z5_endpoint_shell")
    chk(eta * r * H ** 6 * wp ** -2 == 8 * K2 * r ** 2 * H ** 6, "Z5_endpoint_shell")
    chk(eta ** 2 * a == 64 * K2 ** 2 * r ** 2 * wp ** -4 and eta ** 2 * b == 64 * K2 ** 2 * r ** 3 * H ** 6, "Z5_endpoint_shell")
    # x0 d = r H^6 w'^-3 sqrt(eta): squared identity (x0 d)^2 = r^2 H^12 w'^-6 eta
    chk((x0 ** 2) * d2 == r ** 2 * H ** 12 * wp ** -6 * eta, "Z5_endpoint_shell")
    chk(r ** 2 * H ** 12 * wp ** -6 * eta == 8 * K2 * r ** 3 * H ** 12 * wp ** -4, "Z5_endpoint_shell")   # = (sqrt(8K2) r^{3/2} H^6 w'^-2)^2

# ------------------------------------------------------------------ Z6: Lemma 2.2's shell sums and the count J
S2 = F(1, 25) if MUT == "M6" else F(4, 75)
chk(sum(F(1, (5 * 2 ** i) ** 2) for i in range(60)) < S2 and F(1, 25) / (1 - F(1, 4)) == F(4, 75), "Z6_shell_sums")
chk(F(1, 625) / (1 - F(1, 16)) == F(16, 9375), "Z6_shell_sums")
for J in range(1, 12):
    w = [5 * 2 ** j for j in range(J + 1)]
    chk(sum(F(wj) ** 4 for wj in w[:-1]) <= F(16, 15) * F(w[J - 1]) ** 4 and F(16, 15) * F(w[J - 1]) ** 4 == F(1, 15) * F(w[J]) ** 4, "Z6_shell_sums")
    chk(sum(F(wj) ** 4 for wj in w[:-1]) <= F(1, 15) * F(w[J]) ** 4, "Z6_shell_sums")
    chk(sum(F(wj) ** 4 for wj in w[1:]) <= F(16, 15) * F(w[J]) ** 4, "Z6_shell_sums")
    chk(sum(F(wj) ** 2 for wj in w[1:]) <= F(4, 3) * F(w[J]) ** 2, "Z6_shell_sums")
for r in (math.exp(-1), 1e-2, 1e-3, 1e-6, 1e-12, 1e-40):
    wmax = r ** (-3 / 16)
    J = int(math.floor(math.log2(wmax / 5))) if wmax >= 5 else -1
    L = math.log(1 / r)
    chk(J + 1 <= 1 + (3 / 16) * math.log2(1 / r) + 1e-9 and J <= 2 * L - 1 + 1e-9, "Z6_shell_sums")
    if J >= 0:
        wJ = 5 * 2 ** J
        chk(wJ <= wmax < 2 * wJ and wJ ** -8 <= 256 * r ** 1.5 * (1 + 1e-12) and wJ ** -4 <= 16 * r ** 0.75 * (1 + 1e-12), "Z6_shell_sums")

# ------------------------------------------------------------------ Z7: the exponent tables of Theorems QFE3' and ER3'
def exps(beta, alpha):
    # (exponent of r, strict?) for each term of (4.1) with H = r^-alpha, plus tails
    return [("rH7", 1 - 7 * alpha, False), ("H2r_log", 1 - 2 * alpha, True), ("H4r54", F(5, 4) - 4 * alpha, False),
            ("r32H8", F(3, 2) - 8 * alpha, False), ("r32H7_log", F(3, 2) - 7 * alpha, True), ("H8r138", F(13, 8) - 8 * alpha, False),
            ("r74H6", F(7, 4) - 6 * alpha, False), ("r2H6_log", 2 - 6 * alpha, True), ("far", F(1), False)]
for i in range(1, 100):
    beta = F(i, 100)
    alpha = (1 - beta) / (4 if MUT == "M7" else 8)
    for name, ex, strict in exps(beta, alpha):
        chk(ex > beta if strict else ex >= beta, "Z7_exponent_tables")
    m = -(-(8 * beta) // (1 - beta))                  # ceiling of 8 beta/(1 - beta)
    chk(m * alpha >= beta, "Z7_exponent_tables")
    chk(1 - 4 * alpha == (1 + beta) / 2 > 0, "Z7_exponent_tables")      # r H^4 <= 16 r^{(1+beta)/2}
# the terms of (4.1) as (r-power, H-power, explicit log-power); with H = (1 + D) log(1/r) the log-power is H-power + log-power
TERMS = {"rH7": (F(1), 7, 0), "H2r_log": (F(1), 2, 1), "H4r54": (F(5, 4), 4, 0), "r32H8": (F(3, 2), 8, 0), "r32H7_log": (F(3, 2), 7, 1),
         "H8r138": (F(13, 8), 8, 0), "r74H6": (F(7, 4), 6, 0), "r2H6_log": (F(2), 6, 1)}
# consistency of the QFE table above with the term list: exponent = r-power - alpha * H-power, strict iff a logarithm is present
for i in range(1, 100):
    beta = F(i, 100); alpha = (1 - beta) / 8
    table = {name: (ex, strict) for name, ex, strict in exps(beta, alpha) if name != "far"}
    for name, (rp, hp, lp) in TERMS.items():
        chk(table[name] == (rp - alpha * hp, lp > 0), "Z7_exponent_tables")
er = {name: (rp, hp + lp) for name, (rp, hp, lp) in TERMS.items()}
chk(max(lp for rp, lp in er.values() if rp == 1) == 7 and er["rH7"] == (1, 7) and er["H2r_log"] == (1, 3), "Z7_exponent_tables")
chk(min(rp for rp, lp in er.values() if rp > 1) >= F(5, 4), "Z7_exponent_tables")
# dominated terms of (3.1)-(3.2) by (4.1) for H >= 1, r <= 1
for H in (F(1), F(2), F(10), F(1000)):
    for r in (F(1), F(1, 2), F(1, 1000)):
        chk(H ** 4 * r <= r * H ** 7 and H ** 3 * r <= r * H ** 7 and r ** F(3, 2) <= r ** F(3, 2) * H ** 8 and r ** F(3, 2) * H ** 7 <= r ** F(3, 2) * H ** 8 and r * H ** 6 <= r * H ** 7, "Z7_exponent_tables")

# ------------------------------------------------------------------ Z8: Corollary PD3''s constants
K46 = 46149300 if MUT == "M8" else 46149330
chk(sum(comb(7, j) * factorial(j) * 3 ** (j + 1) for j in range(8)) == K46, "Z8_pd3_constants")
K2325 = F(2325, 8) if MUT == "M11" else F(2325, 16)
chk(sum(F(comb(7, j) * factorial(j), 2 ** (j + 1)) for j in range(8)) == K2325 < 146, "Z8_pd3_constants")
chk(F(2, 3) ** 7 == F(128, 2187), "Z8_pd3_constants")
for q in (F(-5, 3) + F(1, 1000), F(-1), F(0), F(2), F(10)):
    chk(q + 2 > F(1, 3), "Z8_pd3_constants")
    chk(sum(F(comb(7, j) * factorial(j)) / (q + 2) ** (j + 1) for j in range(8)) <= K46, "Z8_pd3_constants")
# the identity int_0^1 s^{q+1} (1 + log(1/s))^7 ds = sum_j C(7,j) j!/(q+2)^{j+1}: numerical check at q = 0 (Simpson on x = log(1/s))
def simpson(f, a, b, n):
    h = (b - a) / n; s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3
num = simpson(lambda x: math.exp(-2 * x) * (1 + x) ** 7, 0.0, 60.0, 60000)
chk(abs(num - 2325 / 16) < 1e-6, "Z8_pd3_constants")

# ------------------------------------------------------------------ Z9: numeric sanity check of Lemma 1.1 (floating point)
def saddles(c, R, psi):
    out = []
    if R == 0.0:
        if c == 0.0:
            return out
        s = psi / c; z2 = 36.0 * (s * s - 1.0) / c
        if z2 <= 0:
            return out
        for Z in (math.sqrt(z2), -math.sqrt(z2)):
            det = (c - s * psi) / 4.0                      # C82 (5)
            v = (s - 1.0) / 2.0 - psi * Z * Z / 144.0 + 1.0
            if det < 0:
                out.append((s, Z, v))
        return out
    k = 64.0 * c / (R * R)
    A = 1.0 - k * c * c; B = 2.0 * k * c * psi; C = -1.0 - k * psi * psi
    if abs(A) < 1e-14:
        roots = [-C / B] if abs(B) >= 1e-14 else []
    else:
        disc = B * B - 4 * A * C
        if disc < 0:
            return out
        sd = math.sqrt(disc); roots = [(-B + sd) / (2 * A), (-B - sd) / (2 * A)]
    for s in roots:
        Z = 48.0 * (psi - c * s) / R
        if Z == 0.0 or abs(s * s - 1.0 - c * Z * Z / 36.0) > 1e-7 * (1 + s * s + abs(c) * Z * Z / 36.0):
            continue
        det = (c - s * psi) / 4.0                          # C82 (5)
        v = (s - 1.0) / 2.0 - psi * Z * Z / 144.0 + 1.0
        if det < 0:
            out.append((s, Z, v))
    return out

def branches(c, R, lo, hi):
    """Saddle branches on (lo, hi]: for each root index of C82's quadratic, the sub-interval where that root is a saddle
    (type is constant along a branch; a branch is cut where the root leaves the saddle type or ceases to exist)."""
    n = 4000
    grid = [lo + (hi - lo) * i / n for i in range(1, n + 1)]
    out = []
    for idx in (0, 1):
        cur = None
        for p in grid:
            S = saddles_indexed(c, R, p)
            ok = idx in S
            if ok and cur is None:
                cur = [p, p]
            elif ok:
                cur[1] = p
            elif cur is not None:
                out.append((idx, cur[0], cur[1])); cur = None
        if cur is not None:
            out.append((idx, cur[0], cur[1]))
    return out

def saddles_indexed(c, R, psi):
    """{root index: v} for the saddles at psi, with a stable root ordering (by sigma)."""
    res = {}
    if R == 0.0:
        S = saddles(c, R, psi)
        for i, (s, Z, v) in enumerate(sorted(S)):
            res[i] = v
        return res
    k = 64.0 * c / (R * R)
    A = 1.0 - k * c * c; B = 2.0 * k * c * psi; C = -1.0 - k * psi * psi
    if abs(A) < 1e-14:
        roots = [-C / B] if abs(B) >= 1e-14 else []
    else:
        disc = B * B - 4 * A * C
        if disc < 0:
            return res
        sd = math.sqrt(disc); roots = sorted([(-B + sd) / (2 * A), (-B - sd) / (2 * A)])
    for i, s in enumerate(roots):
        Z = 48.0 * (psi - c * s) / R
        if Z == 0.0 or abs(s * s - 1.0 - c * Z * Z / 36.0) > 1e-7 * (1 + s * s + abs(c) * Z * Z / 36.0):
            continue
        if (c - s * psi) / 4.0 < 0:
            res[i] = (s - 1.0) / 2.0 - psi * Z * Z / 144.0 + 1.0
    return res

def v_on(c, R, idx, psi):
    return saddles_indexed(c, R, psi).get(idx, None)

def band_interval(c, R, idx, a, b, x):
    """The psi-interval of the branch (idx on [a, b]) where |v| <= x, by bisection (v is monotone decreasing on a branch)."""
    va, vb = v_on(c, R, idx, a), v_on(c, R, idx, b)
    if va is None or vb is None:
        return None
    if va < -x or vb > x:          # v decreasing: the band needs va >= -x and vb <= x somewhere
        if va < -x or vb > x:
            pass
    # v decreasing in psi: {v <= x} = [psi_x, b], {v >= -x} = [a, psi_{-x}]
    def solve(target):             # largest psi with v(psi) >= target  (v decreasing)
        if va < target:
            return a - 1.0           # empty
        if vb >= target:
            return b
        lo_, hi_ = a, b
        for _ in range(60):
            mid = 0.5 * (lo_ + hi_)
            vm = v_on(c, R, idx, mid)
            if vm is None or vm < target:
                hi_ = mid
            else:
                lo_ = mid
        return lo_
    hi_end = solve(-x)             # v >= -x up to here
    lo_end = solve(x)              # v >= x up to here, so v <= x from here on
    L, Rr = max(a, lo_end), min(b, hi_end)
    return (L, Rr) if Rr > L else None

def union_measure(intervals, c, psiU):
    """integral of (psi^2 - c^2) over the union of the intervals, cut at psiU."""
    ivs = sorted([(a, min(b, psiU)) for (a, b) in intervals if a < psiU])
    tot, cur = 0.0, None
    def meas(a, b):
        return (b ** 3 - a ** 3) / 3.0 - c * c * (b - a)
    for a, b in ivs:
        if cur is None:
            cur = [a, b]
        elif a <= cur[1]:
            cur[1] = max(cur[1], b)
        else:
            tot += meas(*cur); cur = [a, b]
    if cur is not None:
        tot += meas(*cur)
    return tot

K163 = 0.5 if MUT == "M9" else 16.0 / 3.0
K43f = 4.0 / 3.0
state = 20261006
def lcg():
    global state
    state = (1103515245 * state + 12345) % (2 ** 31)
    return state / 2 ** 31
cases = [(-0.548276, -17.811837), (-0.417044, -12.641051), (-0.692364, -22.181068), (-0.911235, 30.299460), (0.0, 16.0), (0.3, 0.0), (0.0, 0.0)]
for _ in range(50):
    u1, u2, u3, u4 = lcg(), lcg(), lcg(), lcg()
    c = math.sqrt(-2 * math.log(1 - u1 + 1e-12)) * math.cos(2 * math.pi * u2) * 2.0
    R = math.sqrt(-2 * math.log(1 - u3 + 1e-12)) * math.cos(2 * math.pi * u4) * 20.0
    cases.append((c, R))
ntests = 0
for c, R in cases:
    lo = abs(c) + 1e-9
    hi = max(4.0 * abs(c), 2.0 * abs(R) ** (2.0 / 3.0) + 1.0, 2.0) * 1.5
    brs = branches(c, R, lo, hi)
    chk(len(brs) <= 2, "Z9_numeric_band")
    # density bound along the branches at v <= 1/2
    for (idx, a, b) in brs:
        for t in range(1, 60):
            p = a + (b - a) * t / 60.0
            S = saddles(c, R, p)
            for (sg, Z, v) in S:
                if v <= 0.5:
                    chk(48.0 * (p * p - c * c) / (Z * Z) <= K43f * p ** 3 * (1 + 1e-9), "Z9_numeric_band")
    for x in (0.5, 0.25, 0.1, 0.02, 0.001):
        ivs = []
        for (idx, a, b) in brs:
            iv = band_interval(c, R, idx, a, b, x)
            if iv is not None:
                ivs.append(iv)
        tops = [lo + frac * (hi - lo) for frac in (0.1, 0.3, 0.6, 1.0)] + [b for (a, b) in ivs] + [a + 1e-6 for (a, b) in ivs]
        for psiU in tops:
            if psiU <= lo:
                continue
            Jint = union_measure(ivs, c, psiU)
            chk(Jint <= K163 * x * psiU ** 3 * (1 + 1e-9) + 1e-12, "Z9_numeric_band")
            ntests += 1
print(json.dumps({"checks": COUNT, "mutant": MUT, "z9_band_tests": ntests, "pd3_moment_constant": 46149330,
                  "pd3_cumulative_constant": "2325/16", "lemma11_constant": 192}, sort_keys=True))
```

```json
{"checks": 8569, "lemma11_constant": 192, "mutant": null, "pd3_cumulative_constant": "2325/16", "pd3_moment_constant": 46149330, "z9_band_tests": 1770}
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_