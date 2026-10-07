## Lifetime note LU: author controls, exact executable and stdout, and the exploration script of Remark 3

This publishes the standard-library control script that note LU ([6025486512](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6025486512)) cites in §7, so anyone can replay it. The controls check the finite algebra of the note: Lemma E's coefficient identities and the reflection of (S.3) on exact pinned polynomial fields (L1), the identity (1.1) (L2), the drift formula in (2.1) (L3), the two ledgers (L4), the two integrals of §4 (L5), and Step 2's exponents with the slope bounds on `𝔖` (L6). They do not test the analytic estimates; §7 of the note lists what they leave out. An appendix publishes the exploration script and output of the note's Remark 3, which are not controls.

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction rule.** The same as in [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189): the file is the exact text between the first ```` ```python ```` fence after its `###` heading and the next ```` ``` ```` line, plus a final newline. The expected stdout is the single JSON line in the following ```` ```json ```` fence, plus one newline. In the appendix, `toy_diff_out.txt` is the exact text between the ```` ```text ```` fence after its heading and the next ```` ``` ```` line, plus a final newline.

**Identities.**
- `lu_exact.py`: 13,287 B, SHA-256 `c5bf756c5a6f417da58ab50c20f838d445a51c45b8a50a10244520d017e76c0a`. Stdout: 180 B, SHA-256 `8f47c8f039173bfd17f0bd8b4793a941127c93de7ffc413ca5fd6f64b738832e`.
- Appendix: `toy_diff.py`, 5,402 B, SHA-256 `1f9653b8b5ab7acec756c16226da61caca7b037a751a2bd44ba665f9525cd9cd` (the hash quoted in Remark 3); `toy_diff_out.txt`, 972 B, SHA-256 `5d86c7ad2d04dc4f8becfce283cfa277d05c3a5538807aed78ae7f8384dc198d`.

**Run.** A full run takes about 0.15 s.
- `python3 -B -S lu_exact.py`: exit 0, with exactly the stdout below (5,267 checks in six groups).
- `python3 -B -O -S lu_exact.py`: byte-identical output. No check depends on an `assert`.
- `--mutant M1` … `M7`: each exits 1 in both modes, with empty stdout and `FAILED: <group>` on stderr:
  - `M1` ((E.1)'s coefficient `12 → 11`): `L1_shift`.
  - `M2` (the reflection with `f̃ + kμ` in place of `f̃ − kμ`): `L1_shift`.
  - `M3` (`ξ̂`'s coefficient `3Δ_B → 2Δ_B`, that is L3's `6Δ_B → 4Δ_B`): `L3_drift`.
  - `M4` (the scenario's `σ = 5/24 → 41/200`; it passes the range guard `1/5 < σ < 1/4` and `θ = 36/41 < 1`, and the ledger minimum rejects it, since the row `ρ⁸/ℓ` drops to `16/25`): `L4_ledger`.
  - `M5` (the constant `4/3 → 1`): `L5_integrals`.
  - `M6` (`ε₀ = r^{3/4} → r^{1/2}`): `L6_exponents`.
  - `M7` (`f`'s transverse gradient-difference target `0 → r`, with `f`'s pins checked against that target): `L1_shift`. The pins pass, and the assertion that fails is the vanishing of the `r¹` coefficient of `∂_k(det K_S − det K_M) − 12Δ`. That coefficient becomes `−2·1ᵀA^♯γ_μ`. In Lemma E's proof it comes from the term `−rA^♯(β_S + β_M)·γ_μ`: the honest pins make `β_S + β_M = O(r)`, and M7 makes it `2·1 + O(r)`.
- An unknown label (`--mutant M8`), a bare `--mutant`, extra arguments, or any other argument: exit 2, with `usage: lu_exact.py [--mutant M1..M7]` on stderr.

The output was produced with Python 3.11.15. The script uses only `json`, `random` (with a fixed seed), `sys`, `fractions` and `math.factorial`.

**Author-side referee (not review evidence).** Before posting, three clean-context referee passes read the note in the three slices of its §8, against the consumed packets at Math- `main` `665f744a` and the cited notes on this issue. They ran in the same provider and session, so they carry organizational-independence credit 0 and are not review evidence. All three returned AMEND with no blocking finding. Every finding is applied in the posted note; no statement, exponent or constant changed.
- *Slice A (§§0–2): AMEND.*
  - Two displays in Lemma E's "sum" bullet were stated for `|k| ≤ 1` with `f`'s jets `Δ_B`, `γ`. They hold with the jets of `g = f + kμ` (`Δ_B(g)`, `γ(g)`), and only their `k = 0` values are used. Fixed.
  - The reason given for "`𝔗` dominates Lemma Π" misdescribed Lemma Π's statement, whose `T` (#218's) contains [R]'s coupling terms. The paragraph now uses the deterministic form given by #237's proof through #218 Step F1.
  - NITs applied: the converse in (S.4)'s proof; the nondegeneracy citation (#237 (R.4)); the ball renamed `𝔅` and `(a, b)` renamed `(𝔞, 𝔟)`; consumed displays prefixed with their packet; `D_r` defined; (0.2)'s density factor derived inline; the parities behind the oddness of `V_o`; L1 described as a randomized identity test in exact arithmetic; `Λ_κ = ∫𝒜^{cand}db`; "an odd number of odd factors" for `V_o`.
  - The referee showed that no mutant exercised L1's `r¹` assertion. The new mutant M7 does.
  - The referee's independent sympy check pinned by solving #237 (1.1) exactly. Fully symbolic in `d = 2, 3` and at random rational jets in `d = 4, 5`, it confirmed (E.1)–(E.2), (2.1) and the reflection, and found the sharper `x₀′ = ξ̂ + O(r²𝔗^N)`, which the note does not need.
- *Slice B (§3): AMEND.*
  - One load-bearing step had an inadequate reason: the claim that the Gaussian factor absorbs the powers of `|f₄^±|` near `x̂ = ±c_τ`. Closeness in `x̂` does not give closeness in `f₄` (on `𝔖`, `|ϑ|` can approach `1/2`), and without the absorption `E[η²1_{C₁∩𝔖}] ≫ r²`. The referee supplied the correct argument in `f₄`-coordinates. It is now the bullet "Absorbing `f₄^0` (on `𝔖`)" of the layer device.
  - NITs applied: `U_t` defined; `E[𝔗^N1_{C₃}]` obtained by conditioning on `A` (#218 (1.2), not this note's (1.2)); the a.e. derivative justified; (3.2) restricted to `C₁`; the factor `|ξ̂|` in `I₃`; the reflection cited as (S.3); the case indicator `{c_τ ≥ 4η}` shown to be even; `|ŷ_t|` in `I₁`'s window; `|m_i|` bounded in Step 1.
  - The referee's own toy (`d = 3`, exact Gaussian-kernel jet law, `f₄` integrated exactly) found `D/(rk)` converging for `κ ∈ {r², r, 1/4, 1/2, 1}`. Breaking the reflection made `D` of order `k` (Remark 3).
- *Slice C (§§4–6 and the header): AMEND.*
  - Remark 2 misstated what fixes `2/3` for the elder and rejected densities, and omitted #242's Conjecture 7. It is rewritten, and #242 is added to *Cited only* and *Not claimed*.
  - §5 said "note TS §5 verbatim", which would import TS's `θ = 2/3`. It now states `θ = 4/5`, `ρ ≤ min(r₄, r₀)` with TL⁻'s radius at `θ = 4/5`, and the other radius conditions.
  - *Consumed* gains Theorem TL⁻ at `θ = 4/5`, the inputs of note TS §5, note EM's sections, the read ids of TS, EM and EM.1, #237 Step U3, the reduction step of #237's Lemma Λ, and [R] §2's `T_r`.
  - The prior-work paragraph omitted some pointers to the route; it now lists them.
  - Remark 3 said the toy was kept in the project archive. It is published below instead, and Remark 3 now says numpy and scipy and states the model's simplifications.
  - NITs applied, among them: mutant M4 was rejected by L4's range guard before the ledger minimum (`5/24 → 1/5`), and is now `5/24 → 41/200`; L4's description; the list of what the controls do not test.

### lu_exact.py

```python
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
```

```json
{"checks":{"L1_shift":20,"L2_typed":4000,"L3_drift":5,"L4_ledger":39,"L5_integrals":600,"L6_exponents":603},"object":"CL-LU-GAP-DIFFERENCE-20261006-v1","passed":true,"total":5267}
```

### Appendix: the exploration script of Remark 3 (not a control; not part of the proof)

`toy_diff.py` is the toy model that note LU's Remark 3 describes. It uses numpy and scipy (`scipy.special.ndtr`), so it lies outside the standard-library rule for controls and outside the repository. The output below was produced with Python 3.11.15, numpy 2.4.4 and scipy 1.17.1 by `python3 toy_diff.py > toy_diff_out.txt`, with the fixed seed in the script (`2·10⁷` samples per entry, in 10 batches, with reflection pairs). The Monte Carlo stream is fixed by the seed for these versions; other versions may differ in the last digits. Remark 3's table is the column `D/(r^2 kappa)`. Its standard errors are the `+-` values, and the largest is `0.004`.

### toy_diff.py

```python
"""Toy check (exploration only) of the difference mechanism behind 'Lemma U for differences'.

Model (m = 1, d = 2): jets under the k = 0 law
  A ~ N(-1, 0.6^2)          even (Delta = A, s = -1)
  f4 | A ~ N(0.3 A, 1)       even
  C ~ N(0, 1), eta ~ N(0,1)  even
  gamma, B, f5 ~ N(0, 1)     odd; under the k-law each odd jet is shifted by k * w
Polynomials of #237 (2.1) for m = 1:
  Y' = (f4/12) Delta - gamma^2/4,  U = Y' + 3 k B
  V = (3k/4) C + (f4/24) B + (f5/120) Delta - gamma eta / 12
Endpoint quantities (truncated after order r):
  m_M = -6 kappa Delta + U - r V,  m_S = 6 kappa Delta + U + r V,  a = s m_M, b = s m_S
Typed weight W = (-a)_+ b_+ 1{a < 0 < b}; T(k) = E[W 1{A < 0}].
Claim to probe: D(kappa) := T(k) - T(0) - E_0[(36 kappa^2 Delta^2 - Y'^2)_+ 1{A<0}] = O(r^2 kappa) for 0 < kappa <= 1.
f4 is integrated exactly (W is a product of two affine functions of f4 on an interval); the rest by Monte Carlo with
common random numbers and reflection (antithetic) pairs.
"""
import sys
import numpy as np
from scipy.special import ndtr

rng = np.random.default_rng(20261006)
w = dict(gamma=0.7, B=-0.4, f5=0.5)


def trunc_moments(lo, hi, m, sd):
    """E[Z^j 1{lo < Z < hi}], j = 0, 1, 2, for Z ~ N(m, sd^2); lo/hi may be +-inf."""
    a = (lo - m) / sd
    b = (hi - m) / sd
    pa = np.where(np.isfinite(a), np.exp(-0.5 * np.where(np.isfinite(a), a, 0.0) ** 2) / np.sqrt(2 * np.pi), 0.0)
    pb = np.where(np.isfinite(b), np.exp(-0.5 * np.where(np.isfinite(b), b, 0.0) ** 2) / np.sqrt(2 * np.pi), 0.0)
    P = ndtr(b) - ndtr(a)
    # standardized moments over [a, b]
    e1 = pa - pb
    aa = np.where(np.isfinite(a), a, 0.0)
    bb = np.where(np.isfinite(b), b, 0.0)
    e2 = P + aa * pa - bb * pb
    M0 = P
    M1 = m * P + sd * e1
    M2 = m * m * P + 2 * m * sd * e1 + sd * sd * e2
    return M0, M1, M2


def W_expect(k, kappa, r, J):
    """E over f4 of the typed weight, given the other jets J (arrays), at gap k (law shift applied by caller)."""
    A, C, eta, gamma, B, f5 = J
    s = -1.0
    Delta = A
    mean4 = 0.3 * A
    sd4 = 1.0
    # affine in f4: Y' = (Delta/12) f4 - gamma^2/4 ; V = (B/24) f4 + [ (3k/4) C + f5 Delta / 120 - gamma eta / 12 ]
    U0 = -gamma ** 2 / 4 + 3 * k * B
    U1 = Delta / 12
    V0 = 0.75 * k * C + f5 * Delta / 120 - gamma * eta / 12
    V1 = B / 24
    # a = s m_M = s(-6 kappa Delta + U - r V), b = s m_S = s(6 kappa Delta + U + r V); typed iff a < 0 < b; W = -a b
    a0 = s * (-6 * kappa * Delta + U0 - r * V0)
    a1 = s * (U1 - r * V1)
    b0 = s * (6 * kappa * Delta + U0 + r * V0)
    b1 = s * (U1 + r * V1)
    # interval {a0 + a1 z < 0} and {b0 + b1 z > 0}
    lo = np.full_like(A, -np.inf)
    hi = np.full_like(A, np.inf)
    # a0 + a1 z < 0
    za = -a0 / np.where(a1 != 0, a1, 1.0)
    hi = np.where(a1 > 0, np.minimum(hi, za), hi)
    lo = np.where(a1 < 0, np.maximum(lo, za), lo)
    # b0 + b1 z > 0
    zb = -b0 / np.where(b1 != 0, b1, 1.0)
    lo = np.where(b1 > 0, np.maximum(lo, zb), lo)
    hi = np.where(b1 < 0, np.minimum(hi, zb), hi)
    ok = hi > lo
    lo2 = np.where(ok, lo, 0.0)
    hi2 = np.where(ok, hi, 0.0)
    M0, M1, M2 = trunc_moments(lo2, hi2, mean4, sd4)
    # -a b = -(a0 + a1 z)(b0 + b1 z) = -(a0 b0) - (a0 b1 + a1 b0) z - a1 b1 z^2
    val = -(a0 * b0) * M0 - (a0 * b1 + a1 * b0) * M1 - (a1 * b1) * M2
    return np.where(ok & (A < 0), val, 0.0)


def lam_expect(kappa, J):
    """E over f4 of (36 kappa^2 Delta^2 - Y'^2)_+ 1{A<0} at the k = 0 law (r = 0)."""
    A, C, eta, gamma, B, f5 = J
    Delta = A
    c = 6 * kappa * np.abs(Delta)
    beta = -gamma ** 2 / 4
    sl = Delta / 12
    # |sl f4 + beta| < c  <=> f4 in interval
    z1 = (-c - beta) / sl
    z2 = (c - beta) / sl
    lo = np.minimum(z1, z2)
    hi = np.maximum(z1, z2)
    M0, M1, M2 = trunc_moments(lo, hi, 0.3 * A, 1.0)
    # c^2 - (sl z + beta)^2
    val = (c * c - beta * beta) * M0 - 2 * sl * beta * M1 - sl * sl * M2
    return np.where(A < 0, val, 0.0)


def sample(n):
    A = rng.normal(-1.0, 0.6, n)
    C = rng.normal(0, 1, n)
    eta = rng.normal(0, 1, n)
    gamma = rng.normal(0, 1, n)
    B = rng.normal(0, 1, n)
    f5 = rng.normal(0, 1, n)
    return A, C, eta, gamma, B, f5


def shifted(J, k, sign=1.0):
    A, C, eta, gamma, B, f5 = J
    g = sign * gamma + k * w['gamma']
    b = sign * B + k * w['B']
    f = sign * f5 + k * w['f5']
    return A, C, eta, g, b, f


def run(r, kappas, n=2_000_000, reps=10):
    acc = {kap: [] for kap in kappas}
    for _ in range(reps):
        J = sample(n)
        T0 = 0.5 * (W_expect(0.0, 0.0, r, shifted(J, 0.0, 1)) + W_expect(0.0, 0.0, r, shifted(J, 0.0, -1)))
        for kap in kappas:
            k = kap * r
            Tk = 0.5 * (W_expect(k, kap, r, shifted(J, k, 1)) + W_expect(k, kap, r, shifted(J, k, -1)))
            L = 0.5 * (lam_expect(kap, shifted(J, 0.0, 1)) + lam_expect(kap, shifted(J, 0.0, -1)))
            acc[kap].append(np.mean(Tk - T0 - L))
    out = {}
    for kap in kappas:
        v = np.array(acc[kap])
        out[kap] = (v.mean(), v.std(ddof=1) / np.sqrt(len(v)))
    return out


if __name__ == '__main__':
    for r in (0.1, 0.05, 0.025):
        kappas = [r * r, r, 0.3, 1.0]
        res = run(r, kappas)
        for kap in kappas:
            m, se = res[kap]
            print('r=%-6g kappa=%-8g  D=% .3e +- %.1e   D/(r^2 kappa)=% .3f +- %.3f' % (r, kap, m, se, m / (r * r * kap), se / (r * r * kap)))
        sys.stdout.flush()
```

### toy_diff_out.txt

```text
r=0.1    kappa=0.01      D= 1.212e-05 +- 5.7e-09   D/(r^2 kappa)= 0.121 +- 0.000
r=0.1    kappa=0.1       D=-5.251e-04 +- 3.0e-07   D/(r^2 kappa)=-0.525 +- 0.000
r=0.1    kappa=0.3       D=-7.335e-03 +- 2.9e-06   D/(r^2 kappa)=-2.445 +- 0.001
r=0.1    kappa=1         D=-9.007e-02 +- 1.6e-05   D/(r^2 kappa)=-9.007 +- 0.002
r=0.05   kappa=0.0025    D= 8.257e-07 +- 5.6e-10   D/(r^2 kappa)= 0.132 +- 0.000
r=0.05   kappa=0.05      D=-1.380e-05 +- 6.4e-09   D/(r^2 kappa)=-0.110 +- 0.000
r=0.05   kappa=0.3       D=-1.839e-03 +- 5.8e-07   D/(r^2 kappa)=-2.452 +- 0.001
r=0.05   kappa=1         D=-2.257e-02 +- 9.0e-06   D/(r^2 kappa)=-9.029 +- 0.004
r=0.025  kappa=0.000625  D= 4.892e-08 +- 3.2e-11   D/(r^2 kappa)= 0.125 +- 0.000
r=0.025  kappa=0.025     D= 8.652e-07 +- 1.5e-09   D/(r^2 kappa)= 0.055 +- 0.000
r=0.025  kappa=0.3       D=-4.604e-04 +- 3.3e-07   D/(r^2 kappa)=-2.456 +- 0.002
r=0.025  kappa=1         D=-5.650e-03 +- 2.7e-06   D/(r^2 kappa)=-9.040 +- 0.004
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_