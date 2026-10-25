## Lifetime note EM: author controls, exact executable and stdout

This publishes the standard-library control script that note EM ([6023010944](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6023010944)) cites in §7, so anyone can replay it. It checks the finite algebra of the note: Lemma P on exactly pinned polynomial profiles, the shear and the box conditions of Lemma X, the cusp polynomial along the shear and the typed window, the secular equation and interval characterization behind Lemma V, the constants of §4.1, and the ledger of Corollary EM. It does not test the analytic estimates (§7 of the note lists them).

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction rule.** The same as in [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189): the file is the exact text between the first ```` ```python ```` fence after its `###` heading and the next ```` ``` ```` line, plus a final newline. The expected stdout is the single JSON line in the following ```` ```json ```` fence, plus one newline.

**Identities.** `em_exact.py`: 21,773 B, SHA-256 `feea3c3c004ba5b6bc5dbcefc60bc684f0abc91808e6cf092eeac16a81cd9189`. Stdout: 202 B, SHA-256 `c4c2a636ea378587d4c3e629c2fc05aa0d72aad2f260e2327f493cb8259c5740`.

**Run.** A full run takes about 1.6 s.
- `python3 -B -S em_exact.py`: exit 0, with exactly the stdout below (19,972 checks in seven groups).
- `python3 -B -O -S em_exact.py`: byte-identical output. No check depends on an `assert`.
- `--mutant M1` … `M11`: each exits 1 in both modes, with empty stdout and `FAILED: <group>` on stderr:
  - `M1` ((P.1)'s constant `3/80 → 1/50`): `E1_pins`.
  - `M2` ((P.2)'s constant `13/80 → 1/20`): `E1_pins`.
  - `M3` (the shear's sign, `τ = +D^{−1}β̃`): `E2_shear`.
  - `M4` (`3γ·τ → 2γ·τ` in the cubic coefficient along the shear): `E3_model`.
  - `M5` (box condition (a)'s threshold `256/9 → 128/9`; two boundary samples sit between the two): `E4_box`.
  - `M6` (`δ_t² = 4κ/s → 2κ/s`, so the faces only reach `−(5/8)κ`): `E4_box`.
  - `M7` (`σ = 3/14 → 1/5`): `E6_ledger`.
  - `M8` (the bad region's typed exponent `7/2 → 3`): `E6_ledger`.
  - `M9` (the `β₁`-exponent `1/2 → 1` in E5's exponent self-check): `E5_volume`.
  - `M10` (the factor `2` in the bound on `a(ε) − a(0)` `→ 1`): `E5_volume`.
  - `M11` ((P.3)'s constant `5/12 → 1/16`; the worst sampled ratio is about `0.083`): `E1_pins`.
- An unknown label (`--mutant M12`), a bare `--mutant`, extra arguments, or any other argument: exit 2, with `usage: em_exact.py [--mutant M1..M11]` on stderr.

The output was produced with Python 3.11.15. The script uses only `json`, `random` (with a fixed seed), `sys` and `fractions`.

**Author-side referee (not review evidence).** Before posting, three clean-context referee passes read the note in the three slices of its §8, against the consumed sources at Math- `main` `665f744a` and note TS with its successor text. They ran in the same provider and session, so they carry organizational-independence credit 0 and are not review evidence. Every finding is applied in the posted note; no statement, exponent or constant changed.
- *Slice A (§§1–2): AMEND.* One sentence of §2 Step 3 paired the error terms of (2.2) with `s` and `μ` by position, and the pairing was wrong; it now names each term with its condition. NITs applied: "equivalent" restated with the direction E4 checks; Lemma X's bound `c` renamed `𝒩̄` and its setting stated for a general `f ∈ C⁴`; the box `𝒬` and the set `𝓔` renamed, with the projection explicit; `⊗3` in §1; §7's list of what the controls do not test; and a new mutant M11 for (P.3), whose check no mutant exercised. The reader also tested Lemmas P and X end to end in exact arithmetic on independently built fields (40 pinned fields of degree 6–7; 109 quartic parameter sets, 15,369 points): every bound held, the worst ratio being `−1.43` against the required `≤ −1` in (2.3).
- *Slice B (§§3–4): PASS*, with NITs applied: `C_G` fixed in one place; "it suffices that" for (Q′1); which facts come from Lemma Q′'s proof (Steps Q1, Q2′, Q4); the `ã`-integration's weight written out; `ε″_j` renamed; shells `(x, 2x]`; `s_S`'s sign stated in §0; and M9 described as a self-check. The reader's own Monte Carlo (numpy, `−Y = I + GOE`, 4·10⁶ samples) and sympy checks of (L2), (4.3), the `δτ` identity and the determinant scalings agreed.
- *Slice C (§0, §§5–6, header): AMEND*, wording only. Remark 3 misdescribed the bottleneck: the intermediate mass was a limiting term in notes TL and TS, but not in #229, where it sat at `4/9` behind the rows at `3/7`, and the bad region now ties at `9/14`. Remark 1 claimed all three improvements were needed (only the third and one of the first two are), misattributed #237's `3/5` and mislabelled the row `ρ³`. The header now names #237 Lemmas D′ and D″ as the nearest prior small-ball estimates and lists (S″.2) among the consumed statements. NITs applied: Remark 2's description of TS Remark 1; #198 among the same session's packets; the SIDE24 constant; "proven remainder"; the Monte Carlo wording. The reader recomputed both ledgers exactly, reran `smallball.py` byte for byte, and checked every cited blob.

**Exploration (not part of the controls).** Remark 4's Monte Carlo is `smallball.py` (996 B, SHA-256 `33a45d8d80678d1675d3d6f1ea9c99ce64f881dcd3eb930ae707e7f1001b259e`; numpy, outside the repository), with output 1,103 B, SHA-256 `bbf333ec21554250bb7ac629ef98c898a1d6e3bea659652a233c4f0cc8797a90`. Both are kept in the project archive.

### em_exact.py

```python
"""Exact controls for lifetime note EM (CL-EM-INTERMEDIATE-ELDER-20261006-v1).

Standard library only; exact rational arithmetic; deterministic; output identical under -O.
Usage: python3 -B -S em_exact.py [--mutant M1..M11]
On success: one JSON line on stdout, exit 0.
On a failed control: nothing on stdout, 'FAILED: <group>' on stderr, exit 1.
On invalid arguments: usage on stderr, exit 2.
"""
import json
import random
import sys
from fractions import Fraction as F

USAGE = "usage: em_exact.py [--mutant M1..M11]\n"
MUTANTS = {"M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11"}


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


# ---------- polynomial helpers (coefficient lists, lowest degree first) ----------

def padd(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else F(0)) + (q[i] if i < len(q) else F(0)) for i in range(n)]


def pmul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def pscale(p, c):
    return [c * a for a in p]


def peval(p, x):
    return sum((a * x ** i for i, a in enumerate(p)), F(0))


def pder(p, n=1):
    for _ in range(n):
        p = [i * p[i] for i in range(1, len(p))] or [F(0)]
    return p


def sup_abs_quadratic(p, lo, hi):
    """exact max of |p| on [lo, hi] for a polynomial p of degree <= 2."""
    p = (p + [F(0)] * 3)[:3]
    pts = [lo, hi]
    if p[2] != 0:
        v = -p[1] / (2 * p[2])
        if lo < v < hi:
            pts.append(v)
    return max(abs(peval(p, t)) for t in pts)


# ---------- linear algebra over Q ----------

def solve(Amat, b):
    n = len(Amat)
    M = [list(Amat[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = next(i for i in range(c, n) if M[i][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c] / M[c][c]
                M[i] = [M[i][j] - f * M[c][j] for j in range(n + 1)]
    return [M[i][n] / M[i][i] for i in range(n)]


def det(Amat):
    n = len(Amat)
    M = [list(r) for r in Amat]
    d = F(1)
    for c in range(n):
        piv = next((i for i in range(c, n) if M[i][c] != 0), None)
        if piv is None:
            return F(0)
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            d = -d
        d *= M[c][c]
        for i in range(c + 1, n):
            f = M[i][c] / M[c][c]
            M[i] = [M[i][j] - f * M[c][j] for j in range(n)]
    return d


def matmul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))] for i in range(len(X))]


def transpose(X):
    return [list(r) for r in zip(*X)]


def neg_def(m):
    """a random negative definite rational m x m matrix: -(L L^T + I/4)."""
    L = [[rat(-2, 2) if j <= i else F(0) for j in range(m)] for i in range(m)]
    LLt = matmul(L, transpose(L))
    return [[-(LLt[i][j] + (F(1, 4) if i == j else F(0))) for j in range(m)] for i in range(m)]


def dot(u, v):
    return sum((a * b for a, b in zip(u, v)), F(0))


# ---------- E1: third-order pin relations at M (Lemma P) ----------

def e1():
    n = 0
    c1 = F(1, 50) if MUT == "M1" else F(3, 80)
    c2 = F(1, 20) if MUT == "M2" else F(13, 80)
    c3t = F(1, 16) if MUT == "M11" else F(5, 12)
    worst1 = worst2 = F(0)
    for _ in range(300):
        h = F(RNG.randint(1, 40), 400)              # r = 2h <= 1/5
        r = 2 * h
        c0, c3, c4, c5, c6, c7 = (rat(-3, 3) for _ in range(6))
        if RNG.random() < 0.5:
            c7 = F(0)
        a1 = -3 * c3 * h ** 2 - 5 * c5 * h ** 4 - 7 * c7 * h ** 6
        a2 = -2 * c4 * h ** 2 - 3 * c6 * h ** 4
        G = [c0, a1, a2, c3, c4, c5, c6, c7]
        G1 = pder(G)
        need(peval(G1, h) == 0 and peval(G1, -h) == 0, "E1_pins")
        k = (peval(G, -h) - peval(G, h)) / (8 * h ** 3)
        kap = k / r
        G3, G4, G5 = pder(G, 3), pder(G, 4), pder(G, 5)
        S5 = sup_abs_quadratic(G5, -h, h)
        e_mid = peval(G3, 0) - 12 * k
        need(e_mid == -12 * c5 * h ** 2 - 18 * c7 * h ** 4, "E1_pins")          # the exact error
        need(abs(e_mid) <= c1 * r ** 2 * S5, "E1_pins")                      # (P.1)
        e_M = peval(G3, -h) / r - 12 * kap + peval(G4, 0) / 2
        need(abs(e_M) <= c2 * r * S5, "E1_pins")                             # (P.2)
        if S5 != 0:
            worst1 = max(worst1, abs(e_mid) / (r ** 2 * S5))
            worst2 = max(worst2, abs(e_M) / (r * S5))
        n += 4
        # the transverse pin (P.3): psi(+-h) = 0
        q = [rat(-3, 3) for _ in range(4)]
        psi = pmul([-h * h, F(0), F(1)], q)
        need(peval(psi, h) == 0 and peval(psi, -h) == 0, "E1_pins")
        S3 = sup_abs_quadratic(pder(psi, 3), -h, h)
        e_t = peval(pder(psi), -h) / r + peval(pder(psi, 2), 0) / 2
        need(abs(e_t) <= c3t * r * S3, "E1_pins")
        n += 2
    need(worst1 <= c1 and worst2 <= c2, "E1_pins")
    # sharpness on quintic profiles (G^(5) constant): the ratio in (P.1) is exactly 1/40, in (P.2) exactly 1/10
    for h in (F(1, 10), F(1, 20), F(3, 70)):
        r = 2 * h
        c5 = F(7, 3)
        G = [F(0), -5 * c5 * h ** 4, F(0), F(0), F(0), c5]
        k = (peval(G, -h) - peval(G, h)) / (8 * h ** 3)
        S5 = 120 * abs(c5)
        e_mid = peval(pder(G, 3), 0) - 12 * k
        e_M = peval(pder(G, 3), -h) / r - 12 * k / r + peval(pder(G, 4), 0) / 2
        need(abs(e_mid) == F(1, 40) * r ** 2 * S5 and abs(e_M) == F(1, 10) * r * S5, "E1_pins")
        need(abs(e_mid) <= c1 * r ** 2 * S5 and abs(e_M) <= c2 * r * S5, "E1_pins")
    # D^3 E at M_hat: (13/80)|v|^3 + (3/2)|v|^2|w| + 3|v||w|^2 + r|w|^3 <= (|v| + |w|)^3 coefficientwise, for r <= 1
    for r in (F(1), F(1, 2), F(1, 10)):
        need(all(a <= b for a, b in zip((F(13, 80), F(3, 2), F(3), r), (F(1), F(3), F(3), F(1)))), "E1_pins")
    return n + 10


# ---------- E2: the shear at M_hat (Lemma X, step 1) ----------

def e2():
    n = 0
    for _ in range(120):
        m = RNG.choice((1, 2))
        D = neg_def(m)
        bt = [rat(-3, 3) for _ in range(m)]
        at = rat(-3, 3)
        Dinv_b = solve(D, bt)
        tau = [-x for x in Dinv_b]
        if MUT == "M3":
            tau = list(Dinv_b)
        H = [[at] + bt] + [[bt[i]] + D[i] for i in range(m)]
        J = [[F(1)] + [F(0)] * m] + [[tau[i]] + [F(1) if i == j else F(0) for j in range(m)] for i in range(m)]
        HG = matmul(transpose(J), matmul(H, J))
        schur = at - dot(bt, Dinv_b)
        need(HG[0][0] == schur, "E2_shear")
        need(all(HG[0][j] == 0 and HG[j][0] == 0 for j in range(1, m + 1)), "E2_shear")
        need(all(HG[i + 1][j + 1] == D[i][j] for i in range(m) for j in range(m)), "E2_shear")
        need(det(H) == det(D) * schur and det(J) == 1, "E2_shear")
        n += 4
    return n


# ---------- E3: the cusp polynomial along the shear, and the typed window ----------

def e3():
    n = 0
    for _ in range(120):
        m = RNG.choice((1, 2))
        kap = F(RNG.randint(1, 60), 60)
        f4 = rat(-4, 4)
        gam = [rat(-3, 3) for _ in range(m)]
        A = neg_def(m)
        Ainv_g = solve(A, gam)
        q = dot(gam, Ainv_g)
        z = f4 - 3 * q
        dtau = [rat(-1, 1) for _ in range(m)]
        tau = [Ainv_g[i] / 2 + dtau[i] for i in range(m)]
        gt = dot(gam, tau)
        tAt = dot(tau, [dot(A[i], tau) for i in range(m)])
        # P(-1/2 + t, tau t) as a polynomial in t
        poly = padd([F(0), F(0), -3 * kap, 2 * kap],
                    pscale(pmul([F(0), F(0), F(1)], [F(1), F(-2), F(1)]), f4 / 24))
        poly = padd(poly, pscale([F(0), F(0), F(-1), F(1)], gt / 2))
        poly = padd(poly, [F(0), F(0), tAt / 2])
        third = 6 * (poly[3] if len(poly) > 3 else F(0))
        coeff = F(2) if MUT == "M4" else F(3)
        need(third == 12 * kap - f4 / 2 + coeff * gt, "E3_model")
        need(third == 12 * kap - z / 2 + 3 * dot(gam, dtau), "E3_model")
        # the value, gradient and Hessian at t = 0 (the shear keeps M_hat critical with value 0)
        need(poly[0] == 0 and poly[1] == 0, "E3_model")
        # model Schur complements at M_hat and S_hat: -6 kappa + z/12 and 6 kappa + z/12
        sM = (-6 * kap + f4 / 12) - dot([-g / 2 for g in gam], solve(A, [-g / 2 for g in gam]))
        sS = (6 * kap + f4 / 12) - dot([g / 2 for g in gam], solve(A, [g / 2 for g in gam]))
        phi = z / (72 * kap)
        need(sM == -6 * kap + z / 12 == -6 * kap * (1 - phi), "E3_model")
        need(sS == 6 * kap + z / 12 == 6 * kap * (1 + phi), "E3_model")
        # the second derivative of P along the shear at t = 0 is the Schur value when tau = A^{-1} gam / 2
        tau0 = [x / 2 for x in Ainv_g]
        p2 = 2 * (-3 * kap + f4 / 24 + (-dot(gam, tau0)) / 2 + dot(tau0, [dot(A[i], tau0) for i in range(m)]) / 2)
        need(p2 == sM, "E3_model")
        n += 6
    # the typed window: s, s_S > 0 with |h_+-| <= eps imply |z| < 72 kappa + 12 eps and s + s_S <= 12 kappa + 2 eps
    acc = 0
    for _ in range(4000):
        kap = F(RNG.randint(1, 40), 40)
        eps = F(RNG.randint(0, 40), 40)
        z = rat(-150, 150)
        hm, hp = (F(RNG.randint(-40, 40), 40) * eps for _ in range(2))
        s = 6 * kap - z / 12 - hm
        sS = 6 * kap + z / 12 + hp
        if s > 0 and sS > 0:
            acc += 1
            need(abs(z) < 72 * kap + 12 * eps, "E3_model")
            need(s + sS <= 12 * kap + 2 * eps, "E3_model")
    need(acc >= 300, "E3_model")
    return n + acc + 1


# ---------- E4: the box barrier (Lemma X, steps 2-4) ----------

def bound(s, mu, T, nb, r, t, zz):
    """the right side of (2.2) at |zeta| = zz (nb is the bound N-bar on the third and fourth derivatives)."""
    return (-s * t * t / 2 - mu * zz * zz / 2 + T * t ** 3 / 6 + 2 * nb * t * t * zz + nb * r * t * zz * zz
            + nb * r * r * zz ** 3 / 6 + 16 * nb * t ** 4 / 3 + nb * r ** 4 * zz ** 4 / 3)


def e4():
    n = 0
    acc = 0
    tconst = F(128, 9) if MUT == "M5" else F(256, 9)
    samples = [(F(RNG.randint(1, 400), 4000), F(RNG.randint(1, 50), 100), F(RNG.randint(1, 400), 100),
                F(RNG.randint(1, 8)), F(RNG.randint(1, 100), 10000), F(RNG.randint(0, 600), 100)) for _ in range(6000)]
    # boundary samples: (128/9) kappa T^2 <= s^3 < (256/9) kappa T^2, all other thresholds satisfied
    samples += [(F(1, 1000), F(1, 2), F(1, 1000), F(1, 2000), F(1, 10 ** 6), F(1, 60)),
                (F(1, 2000), F(1, 2), F(1, 1000), F(1, 4000), F(1, 10 ** 6), F(1, 125))]
    for kap, dt, dz, nb, r, T in samples:
        two = F(2) if MUT == "M6" else F(4)
        s = two * kap / dt ** 2
        mu = 4 * kap / dz ** 2
        thresholds = [s ** 3 >= tconst * kap * T * T, s * s >= F(1024, 3) * nb * kap, s * s >= 4096 * nb * nb * kap / mu,
                      s >= 1024 * nb * nb * r * r * kap / mu ** 2, s >= 16 * kap,
                      mu ** 3 >= F(256, 9) * nb * nb * r ** 4 * kap, mu * mu >= F(64, 3) * nb * r ** 4 * kap]
        if not all(thresholds):
            continue
        acc += 1
        # the box conditions (a)-(g), as squared inequalities
        conds = [dt * dt <= 9 * s * s / (64 * T * T) if T else True, dt * dt <= 3 * s / (256 * nb),
                 dz * dz <= s * s / (1024 * nb * nb), dt * dt <= mu * mu / (256 * nb * nb * r * r),
                 dz * dz <= 9 * mu * mu / (64 * nb * nb * r ** 4), dz * dz <= 3 * mu / (16 * nb * r ** 4), dt <= F(1, 2)]
        need(all(conds), "E4_box")
        # the bound on a grid of the box, and the faces
        for i in range(5):
            for j in range(5):
                t, zz = dt * i / 4, dz * j / 4
                need(bound(s, mu, T, nb, r, t, zz) <= -F(5, 16) * (s * t * t + mu * zz * zz), "E4_box")
                n += 1
        need(-F(5, 16) * s * dt * dt < -kap and -F(5, 16) * mu * dz * dz < -kap, "E4_box")
        need(F(5, 16) * s * dt * dt == F(5, 4) * kap or MUT == "M6", "E4_box")
    need(acc >= 200, "E4_box")
    # (x + y)^4 <= 8 (x^4 + y^4), and the quartic remainder constant (1/24) * 8 * (16 t^4 + r^4 z^4) = (1/3)(16 t^4 + r^4 z^4)
    for _ in range(300):
        x, y = F(RNG.randint(0, 100), 37), F(RNG.randint(0, 100), 41)
        need((x + y) ** 4 <= 8 * (x ** 4 + y ** 4) and (2 * x + y) ** 4 <= 8 * (16 * x ** 4 + y ** 4), "E4_box")
    need(F(1, 24) * 8 == F(1, 3), "E4_box")
    return n + acc + 302


# ---------- E5: the small-ball lemma (Lemma V): the secular equation and the a-interval ----------

def e5():
    n = 0
    for _ in range(200):
        m = RNG.choice((1, 2, 3))
        mus = [F(RNG.randint(1, 60), 20) for _ in range(m)]
        b = [rat(-3, 3) for _ in range(m)]
        mmin = min(mus)

        def a_of(lam):
            return lam + sum(b[i] ** 2 / (mus[i] - lam) for i in range(m))
        lam = mmin * F(RNG.randint(0, 99), 100)
        a = a_of(lam)
        P = [[a - lam] + b] + [[b[i]] + [(mus[i] - lam) if i == j else F(0) for j in range(m)] for i in range(m)]
        need(det(P) == 0, "E5_volume")                                  # lam is an eigenvalue of [[a, b^T], [b, D]]
        eps = mmin / 2 * F(RNG.randint(1, 100), 100)
        da = a_of(eps) - a_of(F(0))
        factor = F(1) if MUT == "M10" else F(2)
        need(da <= eps * (1 + factor * sum(b[i] ** 2 / mus[i] ** 2 for i in range(m))), "E5_volume")
        R = a_of(F(0))
        need(all(b[i] ** 2 <= R * mus[i] for i in range(m)), "E5_volume")
        need(eps * sum(b[i] ** 2 / mus[i] ** 2 for i in range(m)) <= eps * R * sum(1 / mus[i] for i in range(m)), "E5_volume")
        n += 4
        # the a-interval: with K - eps I > 0, -Y - eps I > 0 exactly when a > a(eps) (Sylvester, K block first),
        # and det(-Y - eps I) = det(K - eps I)(a - a(eps)); the same at eps = 0
        for lev in (eps, F(0)):
            for _ in range(3):
                a_t = a_of(F(0)) - 1 + (a_of(eps) - a_of(F(0)) + 2) * F(RNG.randint(0, 100), 100)
                Ms = [[(mus[i] - lev) if i == j else F(0) for j in range(m)] + [b[i]] for i in range(m)]
                Ms.append(list(b) + [a_t - lev])
                minors = [det([row[:k] for row in Ms[:k]]) for k in range(1, m + 2)]
                dK = F(1)
                for i in range(m):
                    dK *= mus[i] - lev
                need(minors[-1] == dK * (a_t - a_of(lev)), "E5_volume")
                need(all(x > 0 for x in minors) == (a_t > a_of(lev)), "E5_volume")
                n += 2
    # the small shells of (V.1): min(2 eps, t)^{3/2} <= 2 eps t^{1/2}; squared, min(2 eps, t)^3 <= 4 eps^2 t
    for _ in range(200):
        eps, t = F(RNG.randint(1, 1000), 997), F(RNG.randint(1, 1000), 991)
        need(min(2 * eps, t) ** 3 <= 4 * eps ** 2 * t, "E5_volume")
        n += 1
    # dyadic sums: sum_k 2^{-k/2} <= 4, since 1 - 2^{-1/2} >= 1/4 (2^{-1/2} <= 3/4 iff 1/2 <= 9/16)
    need(F(1, 2) <= F(9, 16), "E5_volume")
    # exponents: (V.1) eps * x * x^{1/2} * eps / x = eps^2 x^{1/2}; (V.2) t (weight) * t (mu) * t^{1/2} (b) = t^{5/2}
    half = F(1) if MUT == "M9" else F(1, 2)
    need(F(1) + half - 1 == F(1, 2) and 1 + 1 + half == F(5, 2), "E5_volume")
    return n + 2


# ---------- E6: the ledger of Corollary EM ----------

def e6():
    n = 0
    sig = F(1, 5) if MUT == "M7" else F(3, 14)
    rows = {
        "rho^3 (Lemma U)": 3 * sig,
        "l^3 rho^-11 (elder cusp tail; (W+.2) on [rho, l^1/5])": 3 - 11 * sig,
        "l^2 rho^-6 log ((W+.2))": 2 - 6 * sig,
        "rho^8 / l (TL-)": 8 * sig - 1,
        "l^3/4 (TL-)": F(3, 4),
        "l^2/3 (Lemma U fold scale; TL1; S''' r^7/3 term; S'' on [r*, r0*]; far)": F(2, 3),
        "l^2 rho^-5 (A2 finite part)": 2 - 5 * sig,
        "l^4 rho^-13 ((5.0))": 4 - 13 * sig,
    }
    # S''' on [l^1/5, r*]: min(r^3 log, r kappa) -> crossover r = l^{1/6}, mass l^{2/3} log
    cross1 = F(1, 6)                                   # r^3 = l r^{-3}
    need(3 * cross1 == 1 - 3 * cross1 and 4 * cross1 == F(2, 3), "E6_ledger")
    rows["min(r^3 log, r kappa) mass, with log"] = 4 * cross1
    # the r^{7/3} kappa^{2/3} log term: l^{2/3} r^{-1/3} log, integrable at 0
    need(F(7, 3) - F(8, 3) == F(-1, 3) and F(-1, 3) > -1, "E6_ledger")
    # the bad region: min(r^{p_typ}, r^{3/2} kappa^{2/3}) with kappa = l r^{-4}, so r^{3/2} kappa^{2/3} = l^{2/3} r^{e_bad}
    p_typ = F(3) if MUT == "M8" else F(7, 2)
    e_bad = F(3, 2) - F(2, 3) * 4
    need(e_bad == F(-7, 6) and e_bad + 1 < 0, "E6_ledger")      # the upper piece converges at infinity
    cross2 = F(2, 3) / (p_typ - e_bad)                  # r^{p_typ} = l^{2/3} r^{e_bad} at r = l^{cross2}
    need(cross2 * p_typ == F(2, 3) + cross2 * e_bad, "E6_ledger")
    m1 = (p_typ + 1) * cross2                           # int_0^{l^c} r^{p_typ} dr = l^{(p_typ + 1)c} / (p_typ + 1)
    m2 = F(2, 3) + (e_bad + 1) * cross2                 # int_{l^c} l^{2/3} r^{e_bad} dr = l^{2/3 + (e_bad + 1)c} / (-(e_bad + 1))
    need(m1 == m2, "E6_ledger")
    need(1 / (p_typ + 1) + 1 / (-(e_bad + 1)) == F(56, 9), "E6_ledger")   # the constant 2/9 + 6 = 56/9 of section 5
    rows["min(r^7/2, r^3/2 kappa^2/3) mass (bad region)"] = m1
    least = min(rows.values())
    need(least == F(9, 14), "E6_ledger")
    need(sorted(k for k, v in rows.items() if v == least) == sorted(
        ["rho^3 (Lemma U)", "l^3 rho^-11 (elder cusp tail; (W+.2) on [rho, l^1/5])", "min(r^7/2, r^3/2 kappa^2/3) mass (bad region)"]),
        "E6_ledger")
    n += len(rows) + 6
    # sigma = 3/14 maximizes min(3 sigma, 3 - 11 sigma); theta = (1 - 4 sigma)/sigma = 2/3 < 1
    grid = [F(i, 1000) for i in range(201, 260)]
    best = max(grid + [F(3, 14)], key=lambda x: min(3 * x, 3 - 11 * x))
    need(best == F(3, 14) and (1 - 4 * F(3, 14)) / F(3, 14) == F(2, 3), "E6_ledger")
    # SIDE24, rho_rej and the counterfactuals
    need(F(9, 14) + F(1, 3) == F(41, 42), "E6_ledger")
    need(min(F(3, 5), F(9, 14)) == F(3, 5) and F(3, 5) > F(4, 7), "E6_ledger")
    need(F(2, 3) > F(9, 14), "E6_ledger")                                     # the far term is absorbed
    # without (V.2): min(r^3, r^{3/2} kappa^{2/3}) gives kappa = r^{9/4}, r = l^{4/25}, mass l^{16/25} < l^{9/14}
    c3 = F(1) / (4 + F(9, 4))
    need(c3 == F(4, 25) and 4 * c3 == F(16, 25) and F(16, 25) < F(9, 14), "E6_ledger")
    # note TS: a^4 log against l^{2/3} a^{-2/3} at a = l^{1/7}: 4/7
    need(4 * F(1, 7) == F(2, 3) - F(2, 3) * F(1, 7) == F(4, 7), "E6_ledger")
    return n + 7


# ---------- E7: the constants of the good region ----------

def e7():
    n = 0
    for _ in range(400):
        C1 = F(RNG.randint(1, 20))
        NB = F(RNG.randint(1, 50))                     # N-bar = C0 N, with |f4|, |gamma|, lambda <= N-bar and 1 <= N-bar
        r = F(RNG.randint(1, 100), 10 ** 6)
        lam = 3520 * C1 * NB * r * F(RNG.randint(100, 400), 100)
        kap = F(RNG.randint(1, 100), 100)              # kappa <= 1
        # (4.2): from 3 lam G2 <= N-bar + 72 kappa + 12 eps~ with eps~ <= 440 C1 N-bar r (1 + G2), the largest admissible G2
        G2max = (NB + 72 * kap + 5280 * C1 * NB * r) / (3 * lam - 5280 * C1 * NB * r)
        CGam = F(2, 3) * (73 + 5280 * C1)
        need(3 * lam - 5280 * C1 * NB * r >= F(3, 2) * lam, "E7_constants")
        need(G2max <= CGam * NB / lam, "E7_constants")
        # (4.4): N-bar^2 r / lam <= N-bar^{5/2} r lam^{-3/2} whenever lam <= N-bar (squared)
        lam2 = NB * F(RNG.randint(1, 100), 100)
        need((NB ** 2 * r / lam2) ** 2 <= NB ** 5 * r ** 2 / lam2 ** 3, "E7_constants")
        # |delta tau| <= (C0 N r / mu)(G/4 + 5/12) <= G/4 + 1/2 once mu >= C0 N r, and then |tau| <= G/2 + |delta tau| <= G + 1
        C0 = F(RNG.randint(1, 20))
        NN = F(RNG.randint(1, 50))
        G = F(RNG.randint(0, 100), 10)
        mu = C0 * NN * r * F(RNG.randint(100, 1000), 100)
        need((C0 * NN * r / mu) * (G / 4 + F(5, 12)) <= G / 4 + F(1, 2), "E7_constants")
        need(G / 2 + G / 4 + F(1, 2) <= G + 1, "E7_constants")
        n += 5
    # the barrier thresholds collapse to C [kappa + N kappa^{1/2} mu^{-1/2} + kappa^{1/3} T^{2/3}] once mu >= C_G N r / 2:
    # 1024 C0^2 N^2 r^2 kappa / mu^2 <= 4096 C0^2 kappa / C_G^2 <= kappa for C_G >= 64 C0
    for _ in range(200):
        C0 = F(RNG.randint(1, 20))
        CG = 64 * C0 * F(RNG.randint(1, 5))
        NN = F(RNG.randint(1, 50))
        r = F(RNG.randint(1, 1000), 10 ** 5)
        mu = CG * NN * r / 2 * F(RNG.randint(1, 50))
        kap = F(RNG.randint(1, 100), 100) * r
        need(1024 * C0 ** 2 * NN ** 2 * r ** 2 * kap / mu ** 2 <= kap, "E7_constants")
        n += 1
    # exponents of the good-region integrand: r^3 mu * kappa^{2/3} (r mu^{-3/2})^{4/3} = r^2 * r^{7/3} kappa^{2/3} mu^{-1},
    # and r^3 mu * (kappa / mu) = r^2 * r kappa
    e_r, e_mu = 3 + F(4, 3), 1 - F(3, 2) * F(4, 3)
    need(e_r - 2 == F(7, 3) and e_mu == -1 and F(3) - 2 == 1, "E7_constants")
    return n + 1


def main():
    groups = [("E1_pins", e1), ("E2_shear", e2), ("E3_model", e3), ("E4_box", e4),
              ("E5_volume", e5), ("E6_ledger", e6), ("E7_constants", e7)]
    counts = {}
    try:
        for name, fn in groups:
            counts[name] = fn()
    except Failed as e:
        sys.stderr.write("FAILED: %s\n" % e.args[0])
        sys.exit(1)
    out = {"object": "CL-EM-INTERMEDIATE-ELDER-20261006-v1", "checks": counts, "total": sum(counts.values()), "passed": True}
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
```

```json
{"checks":{"E1_pins":1810,"E2_shear":480,"E3_model":1692,"E4_box":10364,"E5_volume":3402,"E6_ledger":23,"E7_constants":2201},"object":"CL-EM-INTERMEDIATE-ELDER-20261006-v1","passed":true,"total":19972}
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_