## Lifetime note TS: author controls, exact executable and stdout

This publishes the standard-library control script that note TS ([6020794123](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6020794123)) cites in §7, so anyone can replay it. It checks the finite algebra of the note: the pin relation (1.1) on pinned polynomial profiles, the window-coordinate rescaling and the barrier algebra of Lemma S″, the constants of Lemmas W⁻, GE⁻ and Δ⁻, Lemma Δ⁻'s edge mechanism on exact polynomial models, the ledger of Corollary TS with every exponent derived from its integral, and the domination of every error monomial of §§2–4 by `κr² + r³/κ`. It does not prove the analytic statements; §7 of the note lists what no control covers.

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction rule.** The same as in [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189): the file is the exact text between the first ```` ```python ```` fence after its `###` heading and the next ```` ``` ```` line, plus a final newline. The expected stdout is the single JSON line in the following ```` ```json ```` fence, plus one newline.

**Identities.** `ts_exact.py`: 20,043 B, SHA-256 `0337e78c58a975e9049550347f2c0e5901f1fae022afcf5abb4da948b55eba59`. Stdout: 185 B, SHA-256 `f5d11868721c23382ae0a961843ef6ad34c7cf79200108c78d65a5c9e1e17b71`.

**Run.** A full run takes about 0.3 s.
- `python3 -B -S ts_exact.py`: exit 0, with exactly the stdout below.
- `python3 -B -O -S ts_exact.py`: byte-identical output. No check depends on an `assert`.
- `--mutant M1` … `M10`: each exits 1 in both modes, with empty stdout and `FAILED: <group>` on stderr:
  - `M1` (S1: `|g‴(0) − 12k| ≤ (1/4)r sup|g⁗|`): `S1_pins`.
  - `M2` (S2: `δ = min(1, 3λ/(C₅𝒩))`): `S2_barrier`.
  - `M3` (S2: `(4/9)C₅²𝒩²κ` in place of `(16/9)C₅²𝒩²κ`): `S2_barrier`.
  - `M4` (S3: `130³` in place of `131³`): `S3_constants`.
  - `M5` (S5: `a = ℓ^{1/8}`, so the least exponent becomes `1/2`): `S5_ledger`.
  - `M6` (S5: the contact row left at `ℓ²ρ^{−7}`, so the least exponent becomes `1/2`): `S5_ledger`.
  - `M7` (S5: SIDE24's shift `1/4` in place of `1/3`): `S5_ledger`.
  - `M8` (S6: the monomial `r³/κ` replaced by `r²/κ`): `S6_monomials`.
  - `M9` (S4: the bound `a²sup|F′|/2`): `S4_edge_model`.
  - `M10` (S2: `D = diag(r, r, …, r)`): `S2_barrier`.
- An unknown label (`--mutant M11`), a bare `--mutant`, or any other argument: exit 2, with `usage: ts_exact.py [--mutant M1..M10]` on stderr.

The output was produced with Python 3.11.15. The script uses only `json`, `random` (with a fixed seed), `sys` and `fractions`.

**Author-side referee (not review evidence).** Before posting, three clean-context referee passes read the note in three slices against the consumed sources: §1, §2, and §§3–5. They ran in the same provider and session, so they carry organizational-independence credit 0 and are not review evidence. All three returned PASS WITH NITS, with no blocker and no needed correction. Their nits are applied above:
- §1: the norm constant `C₀` (orders `≤ 9`, gradients of orders `≤ 8`); the exponent `N₃` of Step 4 (renamed from `N₂`); the sharp constant `1/2` in (1.1), noted; one bound `|x − M| ≤ r`; `E` as a topological ball; `a ≥ ℓ^{1/4}` in the comparison;
- §2: the slack of (W1) renamed `ϱ` (it clashed with the jet `η`); (1.1) of TL by interpolation at `j = 1/2, 3/2`; (W1)'s window used only with the bounded density of `f₄`; the law of `A` given `J‴`; the term `8r²`; the layer value in `𝔅_b`;
- §§3–5: parity stated in Step 4; the collection of Steps 1–6; both branches in (Δ.1⁻) and the mirror map; (5.0) for every `k ≥ 0`, through #218 Step C3; the range `σ ≤ 10/49` without (5.0), now checked in S5; the logarithm's power `1/7`, noted.

The §§3–5 referee also tested Lemma Δ⁻ numerically with a Gaussian `p₄` over 1296 configurations (`κ` from `0.01` to `1`): both differences stayed within the note's bounds (ratios at most `0.99` and `0.87`), and the scaled ratios stayed bounded down to `κ = 0.001`.

### ts_exact.py

```python
"""Exact controls for lifetime note TS (CL-TS-SMALL-KAPPA-20261006-v1).

Standard library only; exact rational arithmetic; deterministic; output identical under -O.
Usage: python3 -B -S ts_exact.py [--mutant M1..M10]
On success: one JSON line on stdout, exit 0.
On a failed control: nothing on stdout, 'FAILED: <group>' on stderr, exit 1.
On invalid arguments: usage on stderr, exit 2.
"""
import json
import random
import sys
from fractions import Fraction as F

USAGE = "usage: ts_exact.py [--mutant M1..M10]\n"
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


def rat(lo, hi, den=12):
    return F(RNG.randint(lo * den, hi * den), den)


# ---------- S1: the pins at third order, (1.1) ----------

def quad_sup_abs(c0, c1, c2, lo, hi):
    """exact max of |c0 + c1 t + c2 t^2| over [lo, hi]."""
    pts = [lo, hi]
    if c2 != 0:
        ts = -c1 / (2 * c2)
        if lo < ts < hi:
            pts.append(ts)
    return max(abs(c0 + c1 * t + c2 * t * t) for t in pts)


def pinned_profile(r, k, b, g4, g5, g6):
    """g(t) = b + al t^2 + be t^3 + g4 t^4 + g5 t^5 + g6 t^6 with g(r) = b - k r^3, g'(r) = 0 (and g'(0) = 0)."""
    # al r^2 + be r^3 = -k r^3 - g4 r^4 - g5 r^5 - g6 r^6
    # 2 al r + 3 be r^2 = -4 g4 r^3 - 5 g5 r^4 - 6 g6 r^5
    a11, a12, b1 = r ** 2, r ** 3, -k * r ** 3 - g4 * r ** 4 - g5 * r ** 5 - g6 * r ** 6
    a21, a22, b2 = 2 * r, 3 * r ** 2, -4 * g4 * r ** 3 - 5 * g5 * r ** 4 - 6 * g6 * r ** 5
    det = a11 * a22 - a12 * a21
    al = (b1 * a22 - a12 * b2) / det
    be = (a11 * b2 - a21 * b1) / det
    return [b, F(0), al, be, g4, g5, g6]


def peval(c, t):
    return sum((ci * t ** i for i, ci in enumerate(c)), F(0))


def pder(c):
    return [i * c[i] for i in range(1, len(c))]


def s1():
    n = 0
    factor = F(1, 4) if MUT == "M1" else F(3, 2)
    cases = []
    for _ in range(150):
        r = F(RNG.randint(1, 60), 60)
        k = r * F(RNG.randint(0, 24), 24)
        cases.append((r, k, rat(-3, 3), rat(-20, 20), rat(-20, 20), rat(-40, 40)))
    for r in (F(1, 2), F(1, 10), F(1)):
        cases.append((r, r / 3, F(0), F(5), F(0), F(0)))           # constant g'''' (ratio exactly 1/2)
        cases.append((r, F(0), F(1), F(-7), F(3) / r, F(0)))
    for (r, k, b, g4, g5, g6) in cases:
        g = pinned_profile(r, k, b, g4, g5, g6)
        g1, g2, g3, g4d = pder(g), pder(pder(g)), pder(pder(pder(g))), pder(pder(pder(pder(g))))
        need(peval(g, r) == b - k * r ** 3 and peval(g1, r) == 0 and peval(g1, F(0)) == 0 and peval(g, F(0)) == b, "S1_pins")
        g20, g30 = peval(g2, F(0)), peval(g3, F(0))
        R4 = peval(g, r) - (b + g20 * r ** 2 / 2 + g30 * r ** 3 / 6)
        R3 = peval(g1, r) - (g20 * r + g30 * r ** 2 / 2)
        need(g30 - 12 * k == 12 * (R4 - r * R3 / 2) / r ** 3, "S1_pins")
        sup4 = quad_sup_abs(g4d[0], g4d[1], g4d[2], F(0), r)
        need(abs(R4) <= sup4 * r ** 4 / 24 and abs(R3) <= sup4 * r ** 3 / 6, "S1_pins")
        need(abs(g30 - 12 * k) <= factor * r * sup4, "S1_pins")
        n += 4
    return n


# ---------- S2: the barrier in window coordinates ----------

def matmul(a, b):
    return [[sum((a[i][t] * b[t][j] for t in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def diag(v):
    return [[v[i] if i == j else F(0) for j in range(len(v))] for i in range(len(v))]


def s2():
    n = 0
    # (a) scaling exponents a + 2|beta| - 4 of the window coordinates
    third = {(3, 0): -1, (2, 1): 0, (1, 2): 1, (0, 3): 2}
    second = {(2, 0): -2, (1, 1): -1, (0, 2): 0}
    for (a, bb), e in list(third.items()) + list(second.items()):
        need(a + 2 * bb - 4 == e, "S2_barrier")
        n += 1
    # (b) D^2 F at M-hat equals H-tilde: r^{-4} D H D = Lambda^{-1} H Lambda^{-1}
    for d in (2, 3, 4):
        for _ in range(10):
            r = F(RNG.randint(1, 30), 31)
            h = [[F(0)] * d for _ in range(d)]
            for i in range(d):
                for j in range(i, d):
                    h[i][j] = h[j][i] = rat(-5, 5)
            dv = [r] + [r * r if MUT != "M10" else r] * (d - 1)
            lhs = matmul(matmul(diag(dv), h), diag(dv))
            lhs = [[x / r ** 4 for x in row] for row in lhs]
            lam_inv = [1 / r] + [F(1)] * (d - 1)
            rhs = matmul(matmul(diag(lam_inv), h), diag(lam_inv))
            need(lhs == rhs, "S2_barrier")
            n += 1
    # (c) the barrier algebra: delta = min(1, 3 lam/(2K)); on [0, delta], -(lam/2)t^2 + (K/6)t^3 <= -(lam/4)t^2;
    #     kappa >= lam delta^2/4 forces lam^3 <= max(64 kappa^3, (16/9) K^2 kappa); then lam^3 <= C6^3 N^2 kappa.
    ccube = F(4, 9) if MUT == "M3" else F(16, 9)
    for _ in range(120):
        lam = F(RNG.randint(1, 400), RNG.randint(1, 40))
        c5 = F(RNG.randint(1, 50), RNG.randint(1, 5))
        nn = F(RNG.randint(1, 30), RNG.randint(1, 3))
        if nn < 1:
            nn = F(1)
        K = c5 * nn
        delta = min(F(1), F(3) * lam / K) if MUT == "M2" else min(F(1), F(3) * lam / (2 * K))
        for j in range(9):
            t = delta * j / 8
            need(-lam / 2 * t ** 2 + K / 6 * t ** 3 <= -lam / 4 * t ** 2, "S2_barrier")
        kap_min = lam * delta ** 2 / 4          # extremal: kappa = lam delta^2 / 4
        for kap in (kap_min, kap_min * 2, kap_min * 7):
            if kap > 1:
                continue
            need(lam ** 3 <= max(64 * kap ** 3, ccube * K ** 2 * kap), "S2_barrier")
            c6cube = max(F(64), F(16, 9) * c5 ** 2)
            need(lam ** 3 <= c6cube * nn ** 2 * kap, "S2_barrier")
            n += 2
        n += 9
    # (d) the comparison with Lemma S' (exponents of r at fixed kappa, the common factor kappa + r removed):
    #     (S''.1): r^2 kappa^{2/3};  (S'.1): l^{2/3} r^{-2} = kappa^{2/3} r^{8/3 - 2}.
    s2pp = (F(2), F(2, 3))
    s2p = (F(2, 3) * 4 - 2, F(2, 3))
    need(s2pp[1] == s2p[1] and s2pp[0] - s2p[0] == F(4, 3), "S2_barrier")
    n += 1
    return n


# ---------- S3: the constants of sections 1-3 ----------

def s3():
    ce, de = F(1, 200), F(1, 96)
    c4 = F(130) if MUT == "M4" else F(131)
    checks = [
        c4 ** 3 >= 175 ** 2 * 72,                          # Lemma GE-: (175/8) N r^2 Gamma <= lam/8
        576 * 2 == 1152 and F(1152) <= c4 ** 3,            # 3 N r^2 ((k+1)/lam)^{1/2} <= lam/8, kappa + 1 <= 2
        440 * 72 == 31680,
        F(175, 4) <= 44 and 6 + 44 + 1 + 6 == 57,           # 6r + 2r^2 R' <= 57 r <= L/4 for r <= L/228
        36 * ce < 72 * de and 2 * ce / 3 < de,              # Lemma Q' off J+-, and the edge shift inside J+-
        36 + 12 * ce <= 37,                                 # TL (2.2)
        5184 + 1728 * ce < 73 ** 2,                         # |z| < 73 kappa on the support of G_r
        3 * 72 == 216,                                      # typed pairs: |z| = 72 kappa |phi| < 216 kappa
        (5184 - 48 ** 2) == 20 * 144 and 12 * ce < 20,      # w0 >= 20 kappa^2 Delta^2 on [e+, 48 kappa], > |s beta|
        24 + 36 * ce <= F(242, 10),                         # edges inside |z| <= 24.2 kappa
        F(242, 10) / 72 <= F(1, 2),                         # |w0'| <= kappa Delta^2 / 2 there
        1728 * ce == F(864, 100),                           # kink: 1728 kappa r|Q1| <= 8.64 kappa^2
        F(719, 10) ** 2 <= 5184 - F(864, 100),              # so z >= 71.9 kappa at the kink
        F(1728) / F(1439, 10) <= F(121, 10),                # |z - 72 kappa| <= 12.1 r|Q1|
        12 * F(242, 10) <= 291 and 12 * 72 == 864,          # kink 291, second term 864
        72 * 37 == 2664 and 2 * 12 * 50 == 1200,            # (Delta.1-)
        2 * 50 == 100 and 2 * 144 == 288 and 2 * 216 == 432,  # window lengths
        48 * 1 - 72 * ce >= 47,                             # e+(s) - e-(s) >= 47 kappa
    ]
    # Lemma W-: |x| >= 3|q| - 216 on the window; for |q| >= 216, 3|q| - 216 >= 2|q|; for |q| <= 216, 1 + |q| <= 217
    for q in (F(0), F(1), F(100), F(216), F(217), F(1000)):
        if q >= 216:
            checks.append(3 * q - 216 >= 2 * q)
        else:
            checks.append(1 + q <= 217)
    # |phi_r| < 7/6 + kappa m / (2 C12) < 3 for C12 >= m and kappa <= 1
    for m in range(1, 9):
        checks.append(F(7, 6) + F(m, 2 * m) < 3)
    for c in checks:
        need(c, "S3_constants")
    return len(checks)


# ---------- S4: the edge mechanism of Lemma Delta- on explicit models ----------

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
    return [x * s for x in a]


def poly_int(a, lo, hi):
    return sum((ci * (hi ** (i + 1) - lo ** (i + 1)) / (i + 1) for i, ci in enumerate(a)), F(0))


def shift(a, z0):
    out = [F(0)] * len(a)
    for i, ci in enumerate(a):
        term = [F(1)]
        for _ in range(i):
            term = poly_mul(term, [z0, F(1)])
        out = poly_add(out, poly_scale(term, ci))
    return out


def sup_abs(a, z0, h):
    s = shift(a, z0)
    return sum((abs(ci) * h ** i for i, ci in enumerate(s)), F(0))


def s4():
    n = 0
    ce = F(1, 200)
    half = F(1, 2) if MUT == "M9" else F(1)
    # (a) the second difference of Phi for linear F is exactly F' a^2
    for c0, c1 in ((F(1), F(2)), (F(-3), F(5, 7)), (F(2), F(-1, 3))):
        for a in (F(1, 10), F(-1, 7), F(2, 3)):
            phi = lambda x: c0 * x + c1 * x * x / 2
            need(phi(a) + phi(-a) == c1 * a * a, "S4_edge_model")
            need(abs(phi(a) + phi(-a)) <= half * a * a * abs(c1), "S4_edge_model")
            n += 2
    # (b) the w0-model: f4 is the variable; z = f4 + 3|q|; rho a positive quadratic stand-in for p4
    for kap in (F(1, 10), F(1, 3), F(1)):
        for q3 in (F(0), F(1), F(5)):                       # 3|q|
            for d2 in (F(1), F(1, 4)):
                for Q1 in (F(1, 3), F(-2), F(5, 2)):
                    for frac in (F(1), F(1, 2), F(1, 5)):
                        r = frac * ce * kap / abs(Q1)       # r|Q1| <= c_e kappa
                        z_of = [q3, F(1)]                   # z = f4 + 3|q|
                        w0 = poly_scale(poly_add([5184 * kap ** 2], poly_scale(poly_mul(z_of, z_of), F(-1))), d2 / 144)
                        rho = [F(3), F(1, 5), F(1, 40)]     # positive on the relevant range
                        beta = 12 * kap * d2 * Q1
                        e0 = 24 * kap - q3
                        a = 36 * r * Q1
                        zp = 48 * kap - q3

                        def S(s):
                            integrand = poly_add(w0, [s * beta])
                            return poly_int(poly_mul(integrand, rho), e0 + 36 * s * Q1, zp)

                        Fp = poly_mul(w0, rho)

                        def Phi(x):
                            return poly_int(Fp, e0, e0 + x)

                        lhs = S(r) + S(-r) - 2 * S(F(0))
                        rhs = -(Phi(a) + Phi(-a)) + r * beta * poly_int(rho, e0 + a, e0 - a)
                        need(lhs == rhs, "S4_edge_model")
                        fprime = [i * Fp[i] for i in range(1, len(Fp))]
                        bound = half * a * a * sup_abs(fprime, e0, abs(a))
                        need(abs(Phi(a) + Phi(-a)) <= bound, "S4_edge_model")
                        # |w0'| <= kappa Delta^2 / 2 on |z| <= 24.2 kappa (w0' = -(Delta^2/72) z)
                        need(d2 / 72 * F(242, 10) * kap <= kap * d2 / 2, "S4_edge_model")
                        # w0 >= 20 kappa^2 Delta^2 >= |r beta| on [e0 - |a|, 48 kappa - 3|q|]
                        need(peval(w0, zp) == 20 * kap ** 2 * d2 and abs(r * beta) <= 12 * ce * kap ** 2 * d2, "S4_edge_model")
                        # the kink: |w0| >= r|beta| at z = 72 kappa -+ 12.1 r|Q1|, so the kink lies inside that window
                        for sgn in (1, -1):
                            zz = 72 * kap + sgn * F(121, 10) * r * abs(Q1)
                            need(abs(peval(w0, zz - q3)) >= r * abs(beta), "S4_edge_model")
                        n += 6
    # (c) the kink integrand (w + h)_+ + (w - h)_+ - 2 w_+ is in [0, |h|] and vanishes for |w| >= |h|
    pos = lambda y: y if y > 0 else F(0)
    for h in (F(1, 3), F(2)):
        for j in range(-12, 13):
            w = h * F(j, 4)
            kink = pos(w + h) + pos(w - h) - 2 * pos(w)
            need(0 <= kink <= abs(h), "S4_edge_model")
            if abs(w) >= abs(h):
                need(kink == 0, "S4_edge_model")
            n += 1
    return n


# ---------- S5: the ledger of (TS.1) ----------

def int_exp(p, lo, hi):
    """l-exponent of the integral of r^p over [l^lo, l^hi] (lo > hi >= 0) as l -> 0;
    lo = None means the lower limit 0 (needs p > -1), hi = None means the upper limit +infinity (needs p < -1)."""
    if p > -1:
        need(hi is not None, "S5_ledger")
        return hi * (p + 1)
    need(p < -1 and lo is not None, "S5_ledger")
    return lo * (p + 1)


def ledger(sig, aexp, cancel=True):
    """rows of (TS.1) at rho = l^sig, a = l^aexp, each exponent derived from its integral (kappa = l r^{-4})."""
    q5 = F(1, 5)
    rows = {
        "W+ typed mass on [l^{1/5}, a] (log)": int_exp(F(3), q5, aexp),          # r^3 log
        "S'' r kappa^{2/3} on [a, r0]": F(2, 3) + int_exp(F(-5, 3), aexp, None),
        "S'' kappa^{5/3} on [a, r0]": F(5, 3) + int_exp(F(-20, 3), aexp, None),
        "Lemma U r^2": int_exp(F(2), None, sig),
        "elder cusp tail / W+ kappa^3": F(3) + int_exp(F(-12), sig, None),
        "W+ kappa^2 r log on [rho, l^{1/5}]": F(2) + int_exp(F(-7), sig, q5),
        "TL- r^3/kappa": F(-1) + int_exp(F(7), F(1, 4), sig),
        "TL- kappa r^2": F(1) + int_exp(F(-2), F(1, 4), sig),
        "Lemma U fold / TL1": F(2, 3),                                           # recorded (#237 section 5; TL1)
        "A2 finite part": 2 - 5 * sig,                                           # recorded (#237 section 5)
        "contact difference (5.0)": F(4) + int_exp(F(-14), sig, None),
    }
    if not cancel:
        rows["contact difference (5.0)"] = F(2) + int_exp(F(-8), sig, None)      # TL's separate bounds l^2 rho^{-7}
    return rows


def s5():
    n = 0
    sig = F(3, 14)
    aexp = F(1, 8) if MUT == "M5" else F(1, 7)
    rows = ledger(sig, aexp, cancel=(MUT != "M6"))
    need(rows["Lemma U r^2"] == 3 * sig and rows["elder cusp tail / W+ kappa^3"] == 3 - 11 * sig, "S5_ledger")
    need(rows["TL- r^3/kappa"] == 8 * sig - 1 and rows["contact difference (5.0)"] in (4 - 13 * sig, 2 - 7 * sig), "S5_ledger")
    need(min(rows.values()) == F(4, 7), "S5_ledger")
    bold = sorted(k for k, v in rows.items() if v == F(4, 7))
    need(bold == ["S'' r kappa^{2/3} on [a, r0]", "W+ typed mass on [l^{1/5}, a] (log)"], "S5_ledger")
    expect = {"Lemma U r^2": F(9, 14), "elder cusp tail / W+ kappa^3": F(9, 14), "W+ kappa^2 r log on [rho, l^{1/5}]": F(5, 7),
              "TL- r^3/kappa": F(5, 7), "TL- kappa r^2": F(3, 4), "S'' kappa^{5/3} on [a, r0]": F(6, 7),
              "A2 finite part": F(13, 14), "contact difference (5.0)": F(17, 14)}
    for k_, v in expect.items():
        need(rows[k_] == v, "S5_ledger")
    n += 4 + len(expect)
    # the split: theta = (1 - 4 sigma)/sigma = 2/3 at sigma = 3/14; the admissible range (1/5, 17/77]
    need((1 - 4 * sig) / sig == F(2, 3), "S5_ledger")
    for s in (F(1, 5) + F(1, 1000), F(21, 100), F(3, 14), F(17, 77)):
        need(min(ledger(s, F(1, 7)).values()) == F(4, 7) and (1 - 4 * s) / s < 1 and s <= F(1, 4), "S5_ledger")
        n += 1
    need(min(ledger(F(17, 77) + F(1, 1000), F(1, 7)).values()) < F(4, 7), "S5_ledger")
    need((1 - 4 * F(1, 5)) / F(1, 5) == 1, "S5_ledger")                    # sigma = 1/5 is the edge kappa = r
    n += 2
    # a = l^{1/7} balances the two bold rows: 4a = 2/3 - (2/3)a
    need(4 * F(1, 7) == F(2, 3) - F(2, 3) * F(1, 7), "S5_ledger")
    # kappa^2 k^2 with kappa = l r^{-4}, k = l r^{-3}: (l, r) exponents (4, -14)
    need((2 * 1 + 2 * 1, 2 * (-4) + 2 * (-3)) == (4, -14), "S5_ledger")
    n += 2
    # how each improvement contributes
    # (i) TL inputs (#229: W+ below a, S' above): a^4 against l^{2/3} a^{-2} at a = l^{1/9}
    need(4 * F(1, 9) == F(2, 3) - 2 * F(1, 9) == F(4, 9), "S5_ledger")
    # (ii) S'' without TL-: rho^2 against l^3 rho^{-11} at rho = l^{3/13}
    need(2 * F(3, 13) == 3 - 11 * F(3, 13) == F(6, 13) and F(6, 13) < F(1, 2) < F(4, 7), "S5_ledger")
    # (iii) without (5.0): the row l^2 rho^{-7} keeps the least exponent at 4/7 exactly for sigma <= 10/49 (theta >= 9/10)
    need(min(ledger(F(10, 49), F(1, 7), cancel=False).values()) == F(4, 7), "S5_ledger")
    need(min(ledger(F(10, 49) + F(1, 1000), F(1, 7), cancel=False).values()) < F(4, 7), "S5_ledger")
    need((1 - 4 * F(10, 49)) / F(10, 49) == F(9, 10) and 2 - 7 * F(10, 49) == F(4, 7), "S5_ledger")
    # SIDE24 and the comparison with TL and #229
    shift_ = F(1, 4) if MUT == "M7" else F(1, 3)
    need(F(4, 7) + shift_ == F(19, 21) and F(19, 21) > F(7, 9) > F(16, 21), "S5_ledger")
    # (TS.2): #237 (P.1) has remainder l^{3/5}, and 3/5 > 4/7
    need(F(3, 5) > F(4, 7), "S5_ledger")
    n += 7
    return n


# ---------- S6: every error monomial of sections 2-4 is at most kappa r^2 + r^3/kappa on r <= kappa <= 1 ----------

def dominated(a, b):
    """r^a kappa^b <= max(kappa r^2, r^3/kappa) for all r <= kappa <= 1 (small r). In x = log kappa in [log r, 0] the
    right side is the max of two linear functions, crossing at kappa = r^{1/2}; the left side is linear. So it
    suffices to check kappa = r, kappa = r^{1/2} and kappa = 1: a + b >= 2, a + b/2 >= 5/2 and a >= 2."""
    return a + b >= 2 and a + b / 2 >= F(5, 2) and a >= 2


def s6():
    rows = [
        ("eps_omega: r^2 kappa", F(2), F(1)), ("eps_omega: k^2 kappa = kappa^3 r^2", F(2), F(3)),
        ("B_a: r^3", F(3), F(0)), ("B_b: kappa^3 r^3", F(3), F(3)), ("B_b: r^3", F(3), F(0)),
        ("B_b: kappa r^2", F(2), F(1)), ("B_b: r^3 log via 2 r^{5/2}", F(5, 2), F(0)), ("B_b: r^3/kappa", F(3), F(-1)),
        ("B_d: r^3", F(3), F(0)), ("B_d: r^3 log(2/kappa) via r^3/kappa", F(3), F(-1)),
        ("edge set: kappa r^2", F(2), F(1)), ("edge set: kappa^2 r^2", F(2), F(2)),
        ("Delta-: r^2 kappa", F(2), F(1)), ("step 2: k^2 kappa^3", F(2), F(5)), ("step 3: kappa^3 r^2", F(2), F(3)),
        ("step 5: r^2 kappa^3", F(2), F(3)), ("step 6: (r^2 + k^2) kappa^3", F(2), F(3)),
    ]
    if MUT == "M8":
        rows[7] = ("B_b: r^3/kappa", F(2), F(-1))
    for _, a, b in rows:
        need(dominated(a, b), "S6_monomials")
    # the target itself, and a monomial that is not dominated
    need(dominated(F(2), F(1)) and dominated(F(3), F(-1)) and not dominated(F(2), F(0)), "S6_monomials")
    # (r/kappa)^p <= r^3 <= r^3/kappa for kappa >= r^theta, p = ceil(3/(1 - theta))
    for th in (F(1, 2), F(2, 3), F(3, 4), F(9, 10)):
        x = F(3) / (1 - th)
        p = x.numerator // x.denominator + (1 if x.denominator != 1 else 0)
        need(p >= x and (1 - th) * p >= 3, "S6_monomials")
    return len(rows) + 1 + 4


def main():
    groups = [("S1_pins", s1), ("S2_barrier", s2), ("S3_constants", s3), ("S4_edge_model", s4),
              ("S5_ledger", s5), ("S6_monomials", s6)]
    counts = {}
    try:
        for name, fn in groups:
            counts[name] = fn()
    except Failed as e:
        sys.stderr.write("FAILED: %s\n" % e.args[0])
        sys.exit(1)
    out = {"object": "CL-TS-SMALL-KAPPA-20261006-v1", "checks": counts, "total": sum(counts.values()), "passed": True}
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
```

```json
{"checks":{"S1_pins":624,"S2_barrier":1514,"S3_constants":32,"S4_edge_model":1040,"S5_ledger":27,"S6_monomials":22},"object":"CL-TS-SMALL-KAPPA-20261006-v1","passed":true,"total":3259}
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_