## Lifetime note V24: author controls, exact executable and stdout, and the author-side referee record

This publishes the standard-library control script that note V24 ([6034159111](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6034159111)) cites in §7, so anyone can replay it. The controls check the finite algebra and every numerical constant of the note:
- V1: the model jet covariance, its floor `I/4` and least pivots, `q_∞ = 12`, and the conditional law of `x_e`;
- V2: the image bound `E_d(L)` and `δ_d(L)`;
- V3: the homogeneity exponents and the sandwich factors;
- V4: the Gamma ratios, the identity for `Π^R` and the model values (3.2);
- V5: the interval-Isserlis enclosures;
- V6: Lemma J and Corollary V2's constants;
- V7: Lemma K and `M`;
- V8: the assembly, asserting the header's table;
- V9: Lemma K's Step 1.

They do not test notes C3, SL and C7, Lemma 0's dominated convergence, Weyl's formula, the existence of the edge limits, Isserlis' theorem itself, the density inequality (2.1), or #244's Theorem A. §7 of the note says so.

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction rule.** The same as in [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189): the file is the exact text between the first ```` ```python ```` fence after its `###` heading and the next ```` ``` ```` line, plus a final newline. The expected stdout is the single JSON line in the following ```` ```json ```` fence, plus one newline.

**Identities.** `v24_exact.py`: 33,760 B, SHA-256 `92cac2a6cf18de1cdb965365ccc6229ce8ce62753bb920c8de1e68e133366e08`. Stdout: 605 B, SHA-256 `4176f93a9835a08a55d2db6dc8f16ac901ca9948df5d04f3cf90e77059855680`.

**Run.** A full run takes about 4.6 s.
- `python3 -B -S v24_exact.py`: exit 0, with exactly the stdout below.
- `python3 -B -O -S v24_exact.py`: byte-identical output. No check depends on an `assert`.
- `--mutant M1` … `M12`: each exits 1 in both modes, with empty stdout and `FAILED: <group>` on stderr:

  | Mutant | Change | Group |
  |---|---|---|
  | M1 | floor `1/3` | `V1_covariance` |
  | M2 | `T₆ = 75` | `V2_image_bound` |
  | M3 | birth pinned, `q = 2d + 2` | `V3_sandwich` |
  | M4 | `G₄`'s constant `1/6` | `V4_gamma_parts` |
  | M5 | `a₂^∞ = 35` for `Π^c` | `V4_gamma_parts` |
  | M6 | `J ≥ 1/1000` | `V6_J_bounds` |
  | M7 | `K = 300` | `V7_lemma_K` |
  | M8 | `η = 12δ` | `V5_moment_perturbation` |
  | M9 | the claim `≤ 10⁻¹¹⁰` at `L = 24` | `V8_assembly` |
  | M10 | `(ψ − c′)/ψ ≤ 3/2` | `V9_lemmaK_step1` |
  | M11 | `Π^R`'s coefficient `−9216 → −9215` | `V4_gamma_parts` |
  | M12 | the nonnegative-part term of `η_R` dropped | `V8_assembly` |

- An unknown label (`--mutant M13`, `--mutant M0`), a bare `--mutant`, extra arguments, or any other argument: exit 2, with `usage: v24_exact.py [--mutant M1..M12]` on stderr.

The output was produced with Python 3.11.15. The script uses only `json`, `sys`, `fractions` and `itertools`, and is ASCII.

**Author-side referee record (not review evidence).** Before posting, three clean-context Claude subagents of this session refereed the draft in the three slices of the note's §8, against the consumed sources. Each re-derived its slice and ran independent numerics: exact `Σ_∞` in two frames, lattice sums at 300 digits, random and adversarial perturbations for Lemma 3, a scan of (K) over 8M points (best constant `2.9074`), `J = 4.1977819815839`, and two independent quadratures of `D` (`0.07673811 ± 5·10⁻⁸`, `0.076735 ± 3·10⁻⁶`). All three returned **AMEND**. Slice B's one blocking finding was about scope. A fourth clean-context subagent then read the changes back and returned **AMEND** with no blocking finding. These reads carry organizational-independence credit 0 and are not review evidence. Every finding is applied:
- **Blocking (scope).** B-1: Lemma K reaches #242's `I` only through #244's Theorem A, which is conditional (#170 Theorem E(1), [CUB] Theorem C, [CUB] (C8)–(C11)). The condition is now stated in *Consumed*, *Not claimed*, §0, Lemma 0, Lemma K (now stated for `Φ`), Theorem V, Corollary V2 and Remarks 1–2. The `c₃` half and Corollary V1 do not use #244. With R-1: the cited parts of #244 that Lemma K uses (Remark 4, Corollary A.1's (3.1)–(3.2), Lemma B.2) are algebra on the cubic, and the note says so.
- **Non-blocking.**
  - A-1 = B-2: `e ↦ −e` maps `x_e` to `ιx_e`, `ι = diag(−1, 1, −1)`, not to `−x_e`. The weights are `ι`-invariant; Lemma 4 now assumes it and proves evenness in `e` (R-8 renamed the reflection from `R` to `ι`).
  - B-3: Lemma K's four coefficients listed (`5.3`, `3.26`, `323.74`, `323.38`); V7 asserts each (R-6).
  - B-4: Lemma J's normal density is `ϕ`, not the kernel `φ`.
  - B-5: V4 checks `Π^R = (1/32)g⁶I_quad(…)` exactly on a 315-point grid that proves the identity (R-13), with mutant M11.
  - C-1: the header no longer says that the note gives a value of `R_0.6666666666666666`: it supplies the transfer, and `Ĩ` stays uncertified.
  - C-2: the header's sign sentence now requires `|J/30 − Ĩ| > 4.2·10⁻¹⁰⁵`.
  - C-3 (with R-2): Remark 2. The sign needs only `D ≤ 0.61`; the value needs `D` and `J`; both at #244 Theorem A's scope.
  - C-4: *Not claimed* now has a bullet on the `R_0.6666666666666666` half's condition.
  - C-5, C-6: sources added to *Consumed* (#237; #242's (2.5), Theorem 1, (1.1a)–(1.1b)) and *Cited only* (#216, #223, [SIDE24], note LU's ids, the MC comment).
  - C-7: Remark 3 cites [6033651797](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6033651797) and matches its dimensions. With R-12, it also mentions the free-fit tension (`0.060 ± 0.007` in `d = 3`).
  - C-8: V8 now asserts the eight table entries, with mutant M12.
- **Nits.**
  - A-2, R-7: `Δ` defined explicitly; the excluded `φ` do not affect `I`; analyticity at `(0, 0)`.
  - A-3: Lemma 0's domination at gap `k`, via parity; the `ε`-limit for each `b`; the model value checked directly (`Ψ_∞^{ψ^R} = 25w_∞H`); "the pin density times (1.1)".
  - A-4: `e = ±θ₁` in `d = 2`.
  - A-5: the least pivots asserted.
  - A-6: the mean-value proof of the shell count.
  - A-7: `𝒮_d > 0` from #242's Theorem 1.
  - A-8: the scale renamed `τ`, and the joint density renamed `p^{oO}`.
  - A-9, R-9: Lemma 3's hypotheses.
  - B-6: V4's Gamma ratios generated from the recursion, with `s_j` derived.
  - B-7: `I_quad` is the Taylor polynomial (checked symbolically, not used).
  - B-8: `c′ = 0` covered, and the nonnegativity of the factors stated.
  - B-9: `v_o(k)` introduced.
  - B-10: `J ≥ 5.07·10⁻⁴`; `e^{−1/16}` listed under V6.
  - B-11: general `G_j`.
  - C-9: Remark 4's exponent.
  - C-10, R-10: Remark 1's SIDE24 bound, against the exact model coefficient.
  - C-11: Remark 5.
  - C-12: "one may take `L₀(d) = 10`".
  - C-13: the model's `F₀`.
  - C-14: `D` in the disposition.
  - C-15, R-5: V9 relabelled, its tautologies replaced by real checks.
  - C-16: the claim's scope widening stated.
  - C-17: the split's wording.
  - C-18: the positive and negative parts corrected to `0.663146` and `0.586408`.
  - R-3: "with its `B = 0` paragraph".
  - R-4: `I(0, 0) = 20/3` is #242's direct computation, and `w_∞` uses note C3's identity, which does not use #244.
  - R-11: *Prior work*'s quotation of note SL.

### v24_exact.py

```python
"""Exact controls for note V24 (CL-V24-TWO-THIRDS-TRANSFER-20261007-v1).

Standard library only; exact rational arithmetic; deterministic; output identical under -O.
Usage: python3 -B -S v24_exact.py [--mutant M1..M12]
On success: one JSON line on stdout, exit 0.
On a failed control: nothing on stdout, 'FAILED: <group>' on stderr, exit 1.
On invalid arguments: usage on stderr, exit 2.
"""
import json
import sys
from fractions import Fraction as F
from itertools import permutations, product

USAGE = "usage: v24_exact.py [--mutant M1..M12]\n"
MUTANTS = {"M%d" % i for i in range(1, 13)}


def parse(argv):
    if len(argv) == 0:
        return None
    if len(argv) == 2 and argv[0] == "--mutant" and argv[1] in MUTANTS:
        return argv[1]
    sys.stderr.write(USAGE)
    sys.exit(2)


MUT = parse(sys.argv[1:])


class Failed(Exception):
    pass


def need(cond, group):
    if not cond:
        raise Failed(group)


def sci(x, digits=4):
    """Upward-rounded decimal string of a positive rational (for the record only)."""
    x = F(x)
    if x == 0:
        return "0"
    e = 0
    while x >= 10:
        x /= 10
        e += 1
    while x < 1:
        x *= 10
        e -= 1
    scale = 10 ** (digits - 1)
    m = -((-x.numerator * scale) // x.denominator)  # ceiling
    if m >= 10 * scale:
        m //= 10
        e += 1
    s = str(m)
    return "%s.%se%d" % (s[0], s[1:], e)


# ---------------------------------------------------------------- rational bounds of constants
def exp_lower(x, n=None):
    """A rational lower bound of e^x for rational x >= 0 (partial sum of the series)."""
    x = F(x)
    n = n or (2 * int(x) + 40)
    s, t = F(0), F(1)
    for j in range(n + 1):
        s += t
        t = t * x / (j + 1)
    return s


def exp_neg_upper(x):
    """A rational upper bound of e^{-x}, x >= 0."""
    return 1 / exp_lower(x)


def sqrt_upper(a, b=1):
    """Rational r with r^2 >= a/b (Newton from above, exact check)."""
    q = F(a, b)
    r = F(int(float(q) ** 0.5 * 10 ** 6) + 1, 10 ** 6)
    while r * r < q:
        r += F(1, 10 ** 6)
    return r


def sqrt_lower(a, b=1):
    q = F(a, b)
    r = F(int(float(q) ** 0.5 * 10 ** 6), 10 ** 6)
    while r * r > q:
        r -= F(1, 10 ** 6)
    return r


SQ2_U, SQ2_L = sqrt_upper(2), sqrt_lower(2)
SQ3_U = sqrt_upper(3)
PI_L, PI_U = F(314159, 100000), F(314160, 100000)
GAMMA16_U = F(6)        # Gamma(1/6) = 6 Gamma(7/6) <= 6, since Gamma <= 1 on [1, 2]
GAMMA23_U = F(3, 2)     # Gamma(2/3) = (3/2) Gamma(5/3) <= 3/2
GAMMA76_U = F(1)


# ---------------------------------------------------------------- V1: model jet covariance
def dfact(n):
    r = 1
    while n > 1:
        r *= n
        n -= 2
    return r


def dphi0(alpha):
    if any(a % 2 for a in alpha):
        return F(0)
    s = 1
    for a in alpha:
        s *= (-1) ** (a // 2) * dfact(a - 1)
    return F(s)


def cov(a, b):
    return (-1) ** sum(b) * dphi0(tuple(x + y for x, y in zip(a, b)))


def jets(d):
    """Jet list in the frame (u, theta_1..theta_m): pins, A, B, gamma, C (birth integrated)."""
    m = d - 1
    names, idx = [], []

    def add(nm, al):
        names.append(nm)
        idx.append(tuple(al))
    for i in range(d):
        add("f_%d" % i, [1 if j == i else 0 for j in range(d)])
    for i in range(d):
        add("f_0%d" % i, [(1 if j == 0 else 0) + (1 if j == i else 0) for j in range(d)])
    add("f_000", [3] + [0] * m)
    npins = len(names)
    th = list(range(1, d))
    for a in range(m):
        for b in range(a, m):
            al = [0] * d
            al[th[a]] += 1
            al[th[b]] += 1
            add("A_%d%d" % (th[a], th[b]), al)
    for a in range(m):
        for b in range(a, m):
            al = [0] * d
            al[0] += 1
            al[th[a]] += 1
            al[th[b]] += 1
            add("B_%d%d" % (th[a], th[b]), al)
    for a in range(m):
        al = [0] * d
        al[0] += 2
        al[th[a]] += 1
        add("g_%d" % th[a], al)
    seen = set()
    for c in product(th, repeat=3):
        key = tuple(sorted(c))
        if key in seen:
            continue
        seen.add(key)
        al = [0] * d
        for x in key:
            al[x] += 1
        add("C_" + "".join(map(str, key)), al)
    M = [[cov(a, b) for b in idx] for a in idx]
    return names, idx, M, npins


def ldl_pivots(M):
    n = len(M)
    A = [row[:] for row in M]
    piv = []
    for k in range(n):
        p = A[k][k]
        piv.append(p)
        if p == 0:
            return piv
        for i in range(k + 1, n):
            f = A[i][k] / p
            for j in range(k, n):
                A[i][j] -= f * A[k][j]
    return piv


def solve(M, b):
    n = len(M)
    A = [row[:] + [b[i]] for i, row in enumerate(M)]
    for k in range(n):
        p = next(i for i in range(k, n) if A[i][k] != 0)
        A[k], A[p] = A[p], A[k]
        for i in range(n):
            if i != k and A[i][k] != 0:
                f = A[i][k] / A[k][k]
                A[i] = [x - f * y for x, y in zip(A[i], A[k])]
    return [A[i][n] / A[i][i] for i in range(n)]


def inv(M):
    n = len(M)
    cols = [solve(M, [F(int(i == j)) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def proj_weights(fn, e):
    """Coefficients of gamma_e, B_ee, C_eee on the independent odd free coordinates."""
    wg = [F(0)] * len(fn)
    wb = [F(0)] * len(fn)
    wc = [F(0)] * len(fn)
    for a, nm in enumerate(fn):
        if nm.startswith("g_"):
            wg[a] = e[int(nm[2:]) - 1]
        elif nm.startswith("B_"):
            i, j = int(nm[2]) - 1, int(nm[3]) - 1
            wb[a] = e[i] * e[j] * (1 if i == j else 2)
        elif nm.startswith("C_"):
            ks = [int(c) - 1 for c in nm[2:]]
            mult = len(set(permutations(ks)))
            pr = F(1)
            for k_ in ks:
                pr *= e[k_]
            wc[a] = pr * mult
    return wg, wb, wc


MODEL = {}


def v1():
    g = "V1_covariance"
    n = 0
    floor = F(1, 3) if MUT == "M1" else F(1, 4)
    for d in (2, 3):
        names, idx, M, npins = jets(d)
        N = len(names)
        need(N == (9 if d == 2 else 19) and npins == 2 * d + 1, g)
        need(all(M[i][j] == M[j][i] for i in range(N) for j in range(N)), g)
        order = [sum(a) for a in idx]
        need(max(order[i] + order[j] for i in range(N) for j in range(N)) == 6, g)
        need(max(abs(x) for row in M for x in row) == 15, g)
        odd = [i for i in range(N) if order[i] % 2]
        even = [i for i in range(N) if order[i] % 2 == 0]
        need(all(M[i][j] == 0 for i in odd for j in even), g)          # parity split
        piv = ldl_pivots([[M[i][j] - (floor if i == j else 0) for j in range(N)] for i in range(N)])
        need(all(p > 0 for p in piv), g)                                 # Sigma_inf >= I/4
        need(min(piv) == (F(3, 4) if d == 2 else F(329, 556)), g)       # the least pivots stated in Lemma 1(a)
        pins_o = [i for i in range(npins) if order[i] % 2]
        free_o = [i for i in odd if i >= npins]
        So = [[M[i][j] for j in pins_o] for i in pins_o]
        Soi = inv(So)
        l = pins_o.index(names.index("f_000"))
        need(72 * Soi[l][l] == 12, g)                                    # q_inf = 12
        SFP = [[M[i][j] for j in pins_o] for i in free_o]
        R = [[sum(SFP[a][b] * Soi[b][c] for b in range(len(pins_o))) for c in range(len(pins_o))]
             for a in range(len(free_o))]
        need(all(R[a][l] == 0 for a in range(len(free_o))), g)          # M_inf = 0
        SFF = [[M[i][j] for j in free_o] for i in free_o]
        S = [[SFF[a][b] - sum(R[a][c] * SFP[b][c] for c in range(len(pins_o))) for b in range(len(free_o))]
             for a in range(len(free_o))]
        fn = [names[i] for i in free_o]
        es = [(F(1),), (F(-1),)] if d == 2 else [(F(1), F(0)), (F(0), F(1)), (F(3, 5), F(4, 5)),
                                                 (F(-5, 13), F(12, 13)), (F(8, 17), F(-15, 17)),
                                                 (F(-20, 29), F(-21, 29))]
        for e in es:
            need(sum(x * x for x in e) == 1, g)
            W = proj_weights(fn, e)
            C3 = [[sum(W[x][a] * S[a][b] * W[y][b] for a in range(len(fn)) for b in range(len(fn)))
                   for y in range(3)] for x in range(3)]
            need(C3 == [[2, 0, 0], [0, 2, 0], [0, 0, 6]], g)
            # l1 and l2 norms of the projection weights (used for no bound; recorded)
            n += 1
        MODEL[d] = dict(N=N, npins=npins, Ne=len(even) - (d), n_free=N - npins,
                        n_even_free=len([i for i in even if i >= npins]), min_pivot=str(min(piv)))
        n += 1
    return n


# ---------------------------------------------------------------- V2: the lattice-tail image bound
def telephone(j):
    t = [1, 1]
    for i in range(2, j + 1):
        t.append(t[i - 1] + (i - 1) * t[i - 2])
    return t[j]


def hermite_e(j):
    """Coefficients of the probabilists' Hermite polynomial He_j (lowest degree first)."""
    a, b = [1], [0, 1]
    if j == 0:
        return a
    for i in range(1, j):
        c = [0] + b
        for k in range(len(a)):
            c[k] -= i * a[k]
        a, b = b, c
    return b


E_BOUND = {}


def v2():
    g = "V2_image_bound"
    n = 0
    T = [telephone(j) for j in range(7)]
    if MUT == "M2":
        T[6] = 75
    need(T == [1, 1, 2, 4, 10, 26, 76], g)
    for j in range(7):
        need(sum(abs(c) for c in hermite_e(j)) == T[j], g)   # one direction: |He_j(x)| <= T_j max(1,|x|)^j
        n += 1
    need(max(dfact(j - 1) for j in range(0, 7, 2)) == 15, g)   # perfect matchings at x = 0
    for d in (2, 3):
        for a in range(1, 201):
            need((2 * a + 1) ** d - (2 * a - 1) ** d <= 2 * d * 3 ** (d - 1) * a ** (d - 1), g)
            n += 1
    # ratio of successive terms of a^s e^{-L^2 a^2/2}, s <= d + 5 <= 8, L >= 10: <= 2^8 e^{-150} < 1/3
    need(3 * 2 ** 8 < exp_lower(150), g)
    for d in (2, 3):
        N = MODEL[d]["N"]
        for L in (10, 24):
            ex = exp_neg_upper(F(L * L, 2))
            E = 3 * d * 3 ** (d - 1) * (76 * d ** 3 * L ** 6 + 15) * ex
            delta = 4 * N * E
            E_BOUND[(d, L)] = (E, delta)
            need(delta < F(1, 10 ** 8), g)
            n += 1
    # monotone in L >= 10: (a L^6 + b) e^{-L^2/2} decreases when L^2 > 6
    return n


# ---------------------------------------------------------------- V3: homogeneity and the sandwich
SAND = {}


def v3():
    g = "V3_sandwich"
    n = 0
    for d in (2, 3):
        m = d - 1
        N = MODEL[d]["N"]
        q = 2 * d + 1 if MUT != "M3" else 2 * d + 2
        nfree = N - q
        # Phi_{aS}(k) = a^{e0} Phi_S(k/sqrt a):  e0 = -N/2 + n/2 + 3 + (m - 1) - 1/2
        e0 = F(-N, 2) + F(nfree, 2) + 3 + (m - 1) - F(1, 2)
        need(e0 == 0, g)
        # k-integral: k = sqrt(a) k', k^{-8/3} dk = a^{-4/3 + 1/2} k'^{-8/3} dk'
        need(F(-4, 3) + F(1, 2) == F(-5, 6), g)
        # even block (P_e, A): exponent h_e = -(d + nA)/2 + nA/2 + (m - 1) - 1/2 = d/2 - 5/2
        nA = m * (m + 1) // 2
        he = F(-(d + nA), 2) + F(nA, 2) + (m - 1) - F(1, 2)
        need(he == F(d, 2) - F(5, 2), g)
        for L in (10, 24):
            E, delta = E_BOUND[(d, L)]
            # full vector: ((1+delta)/(1-delta))^{N/2} (1+delta)^{-5/6} <= 1 + (N+1) delta (sixth powers)
            up = (1 + (N + 1) * delta)
            need(((1 + delta) / (1 - delta)) ** (3 * N) <= up ** 6 * (1 + delta) ** 5, g)
            lo = (1 - (N + 1) * delta)
            need(((1 - delta) / (1 + delta)) ** (3 * N) >= lo ** 6 * (1 - delta) ** 5, g)
            # weights w = p_{P_o}(0) * E[1]: ratio within 1 +- eps1, eps1 = (2N) delta
            # p ratio in [(1+delta)^{-(d+1)/2}, (1-delta)^{-(d+1)/2}];
            # E ratio in [((1-delta)/(1+delta))^{Ne/2} (1-delta)^{he}, ((1+delta)/(1-delta))^{Ne/2} (1+delta)^{he}]
            Ne = d + nA
            two_he = 2 * he
            need(two_he.denominator == 1 and Ne + two_he >= 0, g)
            two_he = int(two_he)
            eps1 = 2 * N * delta
            # upper (squared): (1-delta)^{-(d+1)} ((1+delta)/(1-delta))^{Ne} (1+delta)^{2he} <= (1+eps1)^2
            need((1 + delta) ** (Ne + two_he) <= (1 + eps1) ** 2 * (1 - delta) ** (d + 1 + Ne), g)
            # lower (squared): (1+delta)^{-(d+1)} ((1-delta)/(1+delta))^{Ne} (1-delta)^{2he} >= (1-eps1)^2
            need((1 - delta) ** (Ne + two_he) >= (1 - eps1) ** 2 * (1 + delta) ** (d + 1 + Ne), g)
            SAND[(d, L)] = dict(eps1=eps1)
            n += 1
    return n


# ---------------------------------------------------------------- polynomials in (g, beta, c) and k
# a polynomial: dict {(i, j, l, s): coeff} for g^i beta^j c^l k^s
def pmul(p, q):
    r = {}
    for (a, b, c, s), x in p.items():
        for (a2, b2, c2, s2), y in q.items():
            key = (a + a2, b + b2, c + c2, s + s2)
            r[key] = r.get(key, 0) + x * y
    return {k: v for k, v in r.items() if v != 0}


def padd(*ps):
    r = {}
    for p in ps:
        for k, v in p.items():
            r[k] = r.get(k, 0) + v
    return {k: v for k, v in r.items() if v != 0}


def pscale(p, c):
    return {k: v * c for k, v in p.items()}


G = {(1, 0, 0, 0): F(1)}
BE = {(0, 1, 0, 0): F(1)}
CC = {(0, 0, 1, 0): F(1)}
K = {(0, 0, 0, 1): F(1)}


def pc(x):
    return {(0, 0, 0, 0): F(x)}


def ppow(p, e):
    r = pc(1)
    for _ in range(e):
        r = pmul(r, p)
    return r


# Pi_c = (4/3) X^3, X = g^2/4 - 3 k beta
X = padd(pscale(ppow(G, 2), F(1, 4)), pscale(pmul(K, BE), -3))
PI_C = pscale(ppow(X, 3), F(4, 3))
# Pi_R = (1/32) gamma^6 Iquad(t, chi), t = 12 k beta/g^2, chi = 576 k^2 c/g^3
PI_R = pscale(padd(pscale(ppow(G, 6), F(20, 3)),
                   pscale(pmul(K, pmul(BE, ppow(G, 4))), -240),
                   pscale(pmul(ppow(K, 2), pmul(CC, ppow(G, 3))), 512),
                   pscale(pmul(ppow(K, 2), pmul(ppow(BE, 2), ppow(G, 2))), 2496),
                   pscale(pmul(ppow(K, 3), pmul(BE, pmul(CC, G))), -9215 if MUT == "M11" else -9216),
                   pscale(pmul(ppow(K, 4), ppow(CC, 2)), F(26624, 3))), F(1, 32))


class Iv:
    """Closed rational interval."""
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = F(lo)
        self.hi = F(lo) if hi is None else F(hi)

    def __add__(self, o):
        o = o if isinstance(o, Iv) else Iv(o)
        return Iv(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __mul__(self, o):
        o = o if isinstance(o, Iv) else Iv(o)
        c = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return Iv(min(c), max(c))

    __rmul__ = __mul__


def matchings(items):
    """All partial matchings of a list of indices: yields (pairs, singles)."""
    if not items:
        yield [], []
        return
    first, rest = items[0], items[1:]
    for pairs, singles in matchings(rest):
        yield pairs, [first] + singles
    for i in range(len(rest)):
        other = rest[:i] + rest[i + 1:]
        for pairs, singles in matchings(other):
            yield [(first, rest[i])] + pairs, singles


def gauss_moment_poly(alpha, mu, S):
    """E[x^alpha] for x ~ N(k mu, S), as {power of k: value}; mu, S entries may be Iv."""
    items = []
    for v, a in enumerate(alpha):
        items += [v] * a
    out = {}
    for pairs, singles in matchings(items):
        term = Iv(1)
        for (i, j) in pairs:
            term = term * S[i][j]
        for i in singles:
            term = term * mu[i]
        s = len(singles)
        out[s] = out.get(s, Iv(0)) + term
    return out


def expect(poly, mu, S):
    """Coefficients a_j (by power of k) of E[poly] under N(k mu, S)."""
    out = {}
    for (i, j, l, s), c in poly.items():
        mom = gauss_moment_poly((i, j, l), mu, S)
        for r, val in mom.items():
            out[s + r] = out.get(s + r, Iv(0)) + val * c
    return out


S0 = [[F(2), F(0), F(0)], [F(0), F(2), F(0)], [F(0), F(0), F(6)]]
GJ = {0: F(-3, 5), 2: F(1, 2), 4: F(1, 12), 6: F(7, 72)}   # G_j(q) = Gamma(1/6) GJ[j] q^{-(3j-5)/6}
A_INF = {}


def v4():
    g = "V4_gamma_parts"
    n = 0
    # G_j from Gamma(x + 1) = x Gamma(x): Gamma(-5/6) = -(6/5)Gamma(1/6); Gamma(7/6) = Gamma(1/6)/6;
    # Gamma(13/6) = (7/6)(1/6)Gamma(1/6); G_0 = (1/2)Gamma(-5/6) q^{5/6}, G_j = (1/2)Gamma((3j-5)/6) q^{-(3j-5)/6}
    # Gamma(s)/Gamma(1/6) from Gamma(s + 1) = s Gamma(s), starting at s = 1/6 (and going down once to -5/6)
    gam = {F(1, 6): F(1)}
    s_ = F(1, 6)
    for _ in range(2):
        gam[s_ + 1] = s_ * gam[s_]
        s_ += 1
    gam[F(-5, 6)] = gam[F(1, 6)] / F(-5, 6)
    # the substitution s = q k^2 turns k^{j-8/3} e^{-q k^2} dk into (1/2) q^{-(3j-5)/6} s^{(3j-5)/6 - 1} e^{-s} ds
    sj = {j: F(3 * j - 5, 6) for j in (0, 2, 4, 6)}
    need(-1 < sj[0] < 0 and all(sj[j] > 0 for j in (2, 4, 6)), g)
    need(all(F(j, 2) - F(4, 3) + F(1, 2) == sj[j] for j in sj), g)     # k^{j - 8/3} dk with k = (s/q)^{1/2}
    derived = {j: F(1, 2) * gam[sj[j]] for j in sj}
    if MUT == "M4":
        derived[4] = F(1, 6)
    need(derived == GJ, g)
    # Pi_R is (1/32) g^6 Iquad(12 k beta/g^2, 576 k^2 c/g^3): both sides are polynomials of degree <= 4, 2, 2, 6 in
    # k, beta, c, g, so agreement on the grid k in {0..4}, beta, c in {0, 1, 2}, g in {1..7} (315 points) is an identity
    pts = [(F(gv), F(bv), F(cv), F(kv)) for gv in range(1, 8) for bv in range(3) for cv in range(3) for kv in range(5)]
    need(len(pts) == 315, g)
    for gv, bv, cv, kv in pts:
        t_, chi = 12 * kv * bv / gv ** 2, 576 * kv ** 2 * cv / gv ** 3
        iq = F(20, 3) - 20 * t_ + F(8, 9) * chi + F(52, 3) * t_ ** 2 - F(4, 3) * t_ * chi + F(13, 486) * chi ** 2
        val = sum(c * gv ** a * bv ** b * cv ** cc * kv ** e for (a, b, cc, e), c in PI_R.items())
        need(val == gv ** 6 * iq / 32, g)
        n += 1
    # model expectations (mu = 0, S0)
    mu0 = [Iv(0)] * 3
    S0i = [[Iv(x) for x in row] for row in S0]
    for name, poly, expect_a in (("c", PI_C, {0: F(5, 2), 2: F(36)}), ("R", PI_R, {0: F(25), 2: F(312), 4: F(1664)})):
        a = expect(poly, mu0, S0i)
        av = {j: v.lo for j, v in a.items() if v.lo != 0}
        need(all(v.lo == v.hi for v in a.values()), g)
        if MUT == "M5" and name == "c":
            av[2] = F(35)
        need(av == expect_a, g)
        A_INF[name] = av
        n += 1
    # the coefficient of Gamma(1/6) 12^{-1/6} in sum_j a_j G_j(12):  12^{(5/6)} = 12 * 12^{-1/6}, 12^{-(3j-5)/6} = 12^{-1/6} 12^{-(j-2)/2}
    def coef12(av):
        s = F(0)
        for j, x in av.items():
            s += x * GJ[j] * (F(12) if j == 0 else F(1, 12 ** ((j - 2) // 2)))
        return s
    need(coef12(A_INF["c"]) == 0, g)                 # (G.3): the polynomial part of c3 vanishes in the model
    need(coef12(A_INF["R"]) == F(-112, 9), g)        # Itilde_quad = -(112/675) Gamma(1/6) 12^{-1/6}
    # c3(inf) = Pos_inf[rho_c] = (1/3)(S/25)(8/3)(15/16) J S = (J/30) S
    need(F(1, 3) * F(1, 25) * F(8, 3) * F(15, 16) == F(1, 30), g)
    # Itilde_quad from Gamma_inf[Pi_R] = (1/3)(S/25) sum_j a_j G_j(12) -> (1/75)(-112/9)
    need(F(1, 75) * F(-112, 9) == F(-112, 675), g)
    # model identity E[gamma^6 Iquad] = 800 + 9984 k^2 + 53248 k^4
    need({j: 32 * x for j, x in A_INF["R"].items()} == {0: 800, 2: 9984, 4: 53248}, g)
    n += 4
    return n


# ---------------------------------------------------------------- V5: perturbed moments (interval Isserlis)
ALPHA = {}


def v5():
    g = "V5_moment_perturbation"
    n = 0
    for (d, L), (E, delta) in sorted(E_BOUND.items()):
        # |mu_Y| <= 12 delta sqrt(s_Y)/(sqrt 6 (1 - delta)) <= 12 delta/(1 - delta); |dS| <= delta sqrt(s_i s_j) <= 6 delta
        eta = (12 if MUT == "M8" else 13) * delta
        need(12 * delta / (1 - delta) <= eta and 6 * delta <= eta, g)
        mu = [Iv(-eta, eta)] * 3
        S = [[Iv(S0[i][j] - eta, S0[i][j] + eta) for j in range(3)] for i in range(3)]
        for name, poly in (("c", PI_C), ("R", PI_R)):
            a = expect(poly, mu, S)
            ainf = A_INF[name]
            alpha = {}
            for j, iv in a.items():
                need(j % 2 == 0 or (iv.lo <= 0 <= iv.hi), g)
                c0 = ainf.get(j, F(0))
                alpha[j] = max(abs(iv.lo - c0), abs(iv.hi - c0))
            # odd powers of k vanish by the reflection symmetry (even in k); their enclosures only contain 0
            ALPHA[(d, L, name)] = {j: x for j, x in alpha.items() if j % 2 == 0}
            n += 1
    return n


# ---------------------------------------------------------------- V6: J bounds
JB = {}


def v6():
    g = "V6_J_bounds"
    # upper: J <= (16/15) 27 E[B_+^3] (1/2) 12^{-2/3} Gamma(2/3),  E[B_+^3] = 2^{3/2} sqrt(2/pi)
    need(F(5) ** 3 <= 144, g)                          # 12^{2/3} >= 5
    sq2pi_u = sqrt_upper(2 * 100000, 314159)           # sqrt(2/pi) with pi >= 3.14159
    eb3 = 2 * SQ2_U * sq2pi_u
    J_up = F(16, 15) * 27 * eb3 * F(1, 2) * F(1, 5) * GAMMA23_U
    need(J_up <= 10, g)
    # lower: k in [1/4, 1/2], B >= 1, gamma^2 <= 1/4: 3kB - gamma^2/4 >= 11/16
    e_m12 = 1 - F(1, 2) + F(1, 8) - F(1, 48)           # e^{-1/2} >= (alternating partial sum)
    s2pi = sqrt_upper(2 * 314160, 100000)               # sqrt(2 pi) <= , pi <= 3.14160
    phi1 = e_m12 / s2pi                                 # phi(1) >=
    p_b = (1 - 1 / SQ2_L) * phi1 if (1 - 1 / SQ2_L) > 0 else F(0)
    # careful: 1/sqrt2 <= 1/SQ2_L, so 1 - 1/sqrt 2 >= 1 - 1/SQ2_L
    phi_s = (1 - F(1, 16)) / s2pi                       # phi(1/(2 sqrt 2)) >= e^{-1/16}/sqrt(2pi) >= (15/16)/sqrt(2pi)
    p_g = 2 * (1 / (2 * SQ2_U)) * phi_s                 # P(|Z| <= 1/(2 sqrt 2)) >= 2 (1/(2 sqrt 2)) phi(.)
    e3 = 1 / (F(27183, 10000) ** 3)                     # e^{-3} >= 1/2.7183^3
    k_int = F(1, 4) * F(63, 10)                         # int_{1/4}^{1/2} k^{-8/3} dk >= (1/4) 2^{8/3} >= (1/4)(6.3)
    need(F(63, 10) ** 3 <= 2 ** 8, g)
    J_low = F(16, 15) * F(11, 16) ** 3 * p_b * p_g * e3 * k_int
    claim = F(1, 1000) if MUT == "M6" else F(1, 2000)
    need(J_low >= claim, g)
    JB.update(J_up=F(10), J_low=claim, J_low_exact=J_low)
    # Corollary V2: Gamma(1/6) = 6 Gamma(7/6) >= 6 gamma(7/6, 64), with T = 64, T^{1/6} = 2, T^{7/6} = 128:
    # gamma(s, T) = sum_n (-1)^n T^{s+n}/(n! (s+n)); for n >= T the terms decrease, so the tail after n0 is <= a_{n0}
    s = F(7, 6)
    part, a, n0 = F(0), None, 300
    fact = 1
    for n_ in range(n0 + 1):
        if n_ > 0:
            fact *= n_
        a = F(128 * 64 ** n_, fact) / (n_ + s)
        if n_ < n0:
            part += a if n_ % 2 == 0 else -a
    need(n0 > 64 and part - a >= F(9277, 10000), g)                 # Gamma(7/6) >= 0.9277
    need(F(6608, 10000) ** 6 * 12 <= 1, g)                           # 12^{-1/6} >= 0.6608
    gq = F(112, 675) * 6 * F(9277, 10000) * F(6608, 10000)           # (112/675) Gamma(1/6) 12^{-1/6} >=
    need(gq + claim / 30 >= F(6103, 10000), g)                       # J/30 - Itilde >= 0.6103 - D
    JB.update(gq_low=gq)
    return 6


# ---------------------------------------------------------------- V7: Lemma K and the crude Pos bounds
KCONST = {}


def polyS_reduce(p):
    """p: dict {(i, j): coeff} for t^i S^j; reduce S^2 = 1 - 4t/3."""
    changed = True
    while changed:
        changed = False
        q = {}
        for (i, j), c in p.items():
            if j >= 2:
                q[(i, j - 2)] = q.get((i, j - 2), 0) + c
                q[(i + 1, j - 2)] = q.get((i + 1, j - 2), 0) - F(4, 3) * c
                changed = True
            else:
                q[(i, j)] = q.get((i, j), 0) + c
        p = {k: v for k, v in q.items() if v != 0}
    return p


def tmul(p, q):
    r = {}
    for (a, b), x in p.items():
        for (c, d), y in q.items():
            r[(a + c, b + d)] = r.get((a + c, b + d), 0) + x * y
    return {k: v for k, v in r.items() if v != 0}


def tadd(*ps):
    r = {}
    for p in ps:
        for k, v in p.items():
            r[k] = r.get(k, 0) + v
    return {k: v for k, v in r.items() if v != 0}


def v7():
    g = "V7_lemma_K"
    n = 0
    # I_0 = c' delta^2 + delta^3/3, c' = 1 - t, delta = 1/2 - t + (3/2) S  (#244 Corollary A.1, t <= 2/3)
    cp = {(0, 0): F(1), (1, 0): F(-1)}
    dl = {(0, 0): F(1, 2), (1, 0): F(-1), (0, 1): F(3, 2)}
    I0 = polyS_reduce(tadd(tmul(cp, tmul(dl, dl)), {k: v / 3 for k, v in tmul(dl, tmul(dl, dl)).items()}))
    target = tadd({(0, 0): F(11, 3), (1, 0): F(-21, 2), (2, 0): F(17, 2), (3, 0): F(-4, 3)},
                  tmul({(0, 0): F(3, 2)}, tmul({(0, 0): F(1), (1, 0): F(-1)}, {(0, 1): F(2), (1, 1): F(-3)})))
    need(I0 == target, g)
    P0 = {i: c for (i, j), c in I0.items() if j == 0}
    P1 = {i: c for (i, j), c in I0.items() if j == 1}
    s0 = {0: F(1), 1: F(-2, 3), 2: F(-2, 9)}
    comb = dict(P0)
    for i, c in P1.items():
        for i2, c2 in s0.items():
            comb[i + i2] = comb.get(i + i2, 0) + c * c2
    comb = {k: v for k, v in comb.items() if v != 0}
    need(comb == {0: F(20, 3), 1: F(-20), 2: F(52, 3), 3: F(-8, 3), 4: F(-1)}, g)
    need(P1 == {0: F(3), 1: F(-15, 2), 2: F(9, 2)}, g)     # (3/2)(2 - 5t + 3t^2)
    # sqrt(1-x) = 1 - x/2 - x^2/8 - x^3/(16 (1-xi)^{5/2}); x = 4t/3 gives 1 - (2/3)t - (2/9)t^2
    need(F(4, 3) / 2 == F(2, 3) and (F(4, 3) ** 2) / 8 == F(2, 9), g)
    # |R_S| <= (64/27)|t|^3 3^{5/2}/16 on |t| <= 1/2;  3^{5/2} <= 15.59
    need(F(1559, 100) ** 2 >= 243, g)
    rs = F(64, 27) * F(1559, 100) / 16
    k_small = F(8, 3) + F(1, 2) + F(3, 2) * F(21, 4) * rs          # |t| <= 1/2 : coefficient of |t|^3
    need(k_small <= 22, g)
    # |t| >= 1/2: delta <= 3|t| + 98^{1/3}|t| <= 7.62|t|; I_0 <= 3|t| delta^2 + delta^3/3; |Iquad(t,0)| <= 84 t^2
    need(F(462, 100) ** 3 >= 98, g)
    dmax = 3 + F(462, 100)
    need(dmax <= F(762, 100), g)
    i0max = 3 * dmax ** 2 + dmax ** 3 / 3
    need(i0max <= 322, g)
    need(F(20, 3) * 4 + 20 * 2 + F(52, 3) == 84, g)
    k2 = F(322)
    # Step 1: |dPhi/dR| <= 2 sqrt3 (1 + |t|^{3/2}) + (sqrt2/12)|R|, |R| <= |chi| + 8 + 12|t|
    c_chi = 2 * SQ3_U + 2 * SQ2_U / 3
    c_chi2 = SQ3_U + SQ2_U / 12 + SQ2_U / 2
    c_t3 = SQ3_U
    c_t2 = SQ2_U / 2
    # check the expansion  |chi|[2 sqrt3 (1 + |t|^{3/2}) + (sqrt2/12)(|chi| + 8 + 12|t|)]
    need(F(8, 12) == F(2, 3) and F(12, 12) == 1, g)
    # Step 3: |Iquad(t,chi) - Iquad(t,0)| <= (8/9)|chi| + (2/3)(t^2 + chi^2) + (13/486) chi^2
    tot_chi = c_chi + F(8, 9)
    tot_chi2 = c_chi2 + F(2, 3) + F(13, 486)
    tot_t3 = c_t3 + k2
    tot_t2 = c_t2 + k2 + F(2, 3)
    need(tot_chi < F(53, 10) and tot_chi2 < F(326, 100) and tot_t3 < F(32374, 100) and tot_t2 < F(32338, 100), g)
    KK = max(tot_chi, tot_chi2, tot_t3, tot_t2)
    claim = F(300) if MUT == "M7" else F(324)
    need(KK <= claim, g)
    # crude moments of t^2, |t|^3, |chi|, chi^2 (normalized as in Pos): sum <= 31
    m1 = F(576, 2400) * F(1, 2) * GAMMA16_U                       # 12^{-1/6} <= 1
    eb3 = 2 * (2 * SQ2_U * sqrt_upper(2 * 100000, 314159))         # E|B|^3 = 2^{3/2} * 2 sqrt(2/pi)
    need(eb3 <= F(452, 100), g)
    m2 = F(1728, 2400) * F(452, 100) * F(1, 2) * F(1, 5) * GAMMA23_U
    ec = SQ2_U * sqrt_upper(3) * sqrt_upper(2 * 100000, 314159)    # E|C| = sqrt6 sqrt(2/pi)
    need(ec <= 2, g)
    m3 = F(576, 2400) * 2 * F(452, 100) * F(1, 2) * GAMMA16_U
    need(F(18) ** 6 <= F(12) ** 7, g)                              # 12^{-7/6} <= 1/18
    m4 = F(331776 * 6, 2400) * F(1, 2) * F(1, 18) * GAMMA76_U
    M = m1 + m2 + m3 + m4
    need(M <= 31, g)
    KCONST.update(K=claim, M=F(31), k_small=k_small, i0max=i0max)
    n += 6
    return n


# ---------------------------------------------------------------- V8: assembly
RESULT = {}
TABLE = {(2, 10, "c"): F(588, 10 ** 11), (2, 10, "R"): F(781, 10 ** 8), (3, 10, "c"): F(197, 10 ** 9),
         (3, 10, "R"): F(497, 10 ** 6), (2, 24, "c"): F(488, 10 ** 112), (2, 24, "R"): F(648, 10 ** 109),
         (3, 24, "c"): F(164, 10 ** 110), (3, 24, "R"): F(413, 10 ** 107)}


def v8():
    g = "V8_assembly"
    n = 0
    for (d, L), (E, delta) in sorted(E_BOUND.items()):
        N = MODEL[d]["N"]
        eps1 = SAND[(d, L)]["eps1"]
        dq = 12 * delta / (1 - delta)                       # |q_L - 12|
        out = {}
        for name in ("c", "R"):
            ainf = A_INF[name]
            alpha = ALPHA[(d, L, name)]
            # sum_j a_j g_j(q), g_0 = -(3/5) q^{5/6}, g_j = GJ[j] q^{-(3j-5)/6}; for q in [11, 13]:
            #   |g_j(q)| <= |GJ[j]| * 13 (j = 0), <= |GJ[j]| (j >= 2);  |g_j'(q)| <= 1/2
            gmax = {j: abs(GJ[j]) * (13 if j == 0 else 1) for j in GJ}
            need(dq < 1, g)
            s_at_qL = sum(abs(x) * gmax[j] for j, x in ainf.items())          # crude |sum a_j g_j(q_L)|
            diff = dq * sum(abs(x) for x in ainf.values()) * F(1, 2)             # |sum a_j (g_j(q_L) - g_j(12))|
            if name == "c":
                # sum a_j g_j(q) = q^{-1/6}(18 - (3/2) q): at q_L at most (3/2) dq
                s_at_qL = F(3, 2) * dq
                diff = s_at_qL
            pert = sum(alpha.get(j, 0) * gmax[j] for j in GJ)
            gamma_err = F(1, 75) * GAMMA16_U * (eps1 * s_at_qL + diff + (1 + eps1) * pert)
            if name == "c":
                pos_err = (N + 1) * delta * JB["J_up"] / 30
            else:
                pos_err = (N + 1) * delta * KCONST["K"] * KCONST["M"]
                if MUT == "M12":
                    pos_err = 0
            out[name] = gamma_err + pos_err
        RESULT[(d, L)] = out
        for name in ("c", "R"):
            ent = TABLE[(d, L, name)]
            need(out[name] <= ent <= out[name] * F(101, 100), g)       # the header's entries, rounded up
        # c3(L) > 0: J_low/30 exceeds the transfer error
        need(out["c"] < JB["J_low"] / 30, g)
        if L == 24:
            lim = F(1, 10 ** 110) if MUT == "M9" else F(1, 10 ** 100)
            need(out["c"] <= lim and out["R"] <= lim, g)
        n += 1
    return n


# ---------------------------------------------------------------- V9: Lemma K, Step 1
def v9():
    g = "V9_lemmaK_step1"
    n = 0
    # polynomial identities in y with c' symbolic (dicts {(power of y, power of c'): coeff}):
    #   d/dy[(y - c')^2 (y + 2c')] = 3 (y - c')(y + c');  d/dy[c' y^2 + y^3/3] = y (y + 2c')  (c' >= 0, delta = y);
    #   with delta = y + 2c' (c' < 0, |c'| = -c'):  d/dy[-c' delta^2 + delta^3/3] = y (y + 2c')
    def pm(p, q):
        r = {}
        for (a, b), x in p.items():
            for (c_, d_), y_ in q.items():
                r[(a + c_, b + d_)] = r.get((a + c_, b + d_), 0) + x * y_
        return {k_: v for k_, v in r.items() if v != 0}

    def pa(*ps):
        r = {}
        for p_ in ps:
            for k_, v in p_.items():
                r[k_] = r.get(k_, 0) + v
        return {k_: v for k_, v in r.items() if v != 0}

    def dy(p_):
        return {(a - 1, b): x * a for (a, b), x in p_.items() if a > 0}
    Y, C1 = {(1, 0): F(1)}, {(0, 1): F(1)}
    cub = pm(pm(pa(Y, {(0, 1): F(-1)}), pa(Y, {(0, 1): F(-1)})), pa(Y, {(0, 1): F(2)}))
    need(dy(cub) == pm({(0, 0): F(3)}, pm(pa(Y, {(0, 1): F(-1)}), pa(Y, C1))), g)
    target = pm(Y, pa(Y, {(0, 1): F(2)}))
    phi_pos = pa(pm(C1, pm(Y, Y)), {(3, 0): F(1, 3)})
    need(dy(phi_pos) == target, g)
    dl = pa(Y, {(0, 1): F(2)})
    phi_neg = pa(pm({(0, 1): F(-1)}, pm(dl, dl)), {k_: v / 3 for k_, v in pm(dl, pm(dl, dl)).items()})
    need(dy(phi_neg) == target, g)
    n += 3
    # (psi - c')/psi <= 2 on the admissible range psi >= psi_0 = max(2c', -c')
    two = F(2) if MUT != "M10" else F(3, 2)
    for c_ in (F(-3), F(-1, 2), F(0), F(1, 3), F(2)):
        psi0 = max(2 * c_, -c_)
        for extra in (F(0), F(1, 7), F(1), F(9)):
            psi = psi0 + extra
            if psi == 0:
                continue
            need(psi - c_ <= two * psi, g)
            n += 1
    # (a + b)^{3/2} <= sqrt2 (a^{3/2} + b^{3/2}) on rational squares a = x^2, b = y^2: (x^2 + y^2)^3 <= 2 (x^3 + y^3)^2
    for x in (F(0), F(1, 2), F(1), F(3, 2), F(2)):
        for yv in (F(0), F(1, 3), F(1), F(4, 3)):
            need((x * x + yv * yv) ** 3 <= 2 * (x ** 3 + yv ** 3) ** 2, g)
            n += 1
    # I(0, 0) = Phi(1, 8) = 20/3 = I_quad(0, 0): at c' = 1, R = 8 the cubic (y - 1)^2 (y + 2) = R^2/16 reads
    # (y - 2)(y + 1)^2 = 0 (a cubic identity, checked at four points); its largest root y = 2 gives c' y^2 + y^3/3
    for yv in (F(-3), F(0), F(1, 2), F(5)):
        need((yv - 1) ** 2 * (yv + 2) - F(8) ** 2 / 16 == (yv - 2) * (yv + 1) ** 2, g)
    need(1 * F(2) ** 2 + F(2) ** 3 / 3 == F(20, 3), g)
    # the positive part of c3 vanishes at k = 0: (3*0*beta - g^2/4)_+ = 0
    for gv in (F(-3), F(-1, 2), F(0), F(5, 7)):
        need(max(F(0), 0 - gv * gv / 4) == 0, g)
    return n + 9


def main():
    try:
        counts = {}
        for name, fn in (("V1", v1), ("V2", v2), ("V3", v3), ("V4", v4), ("V5", v5), ("V6", v6), ("V7", v7),
                         ("V8", v8), ("V9", v9)):
            counts[name] = fn()
    except Failed as ex:
        sys.stderr.write("FAILED: %s\n" % ex.args[0])
        sys.exit(1)
    rec = {"object": "CL-V24-TWO-THIRDS-TRANSFER-20261007-v1", "passed": True, "counts": counts,
           "floor_min_pivot": {str(d): MODEL[d]["min_pivot"] for d in (2, 3)},
           "E_upper": {"%d,%d" % k: sci(v[0]) for k, v in sorted(E_BOUND.items())},
           "delta_upper": {"%d,%d" % k: sci(v[1]) for k, v in sorted(E_BOUND.items())},
           "J_low": str(JB["J_low"]), "J_up": str(JB["J_up"]), "K": str(KCONST["K"]), "M": str(KCONST["M"]),
           "transfer_over_S": {"%d,%d" % k: {n_: sci(x) for n_, x in sorted(v.items())}
                               for k, v in sorted(RESULT.items())}}
    sys.stdout.write(json.dumps(rec, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
```

```json
{"E_upper":{"2,10":"2.111e-12","2,24":"1.753e-113","3,10":"3.206e-11","3,24":"2.662e-112"},"J_low":"1/2000","J_up":"10","K":"324","M":"31","counts":{"V1":10,"V2":411,"V3":4,"V4":321,"V5":8,"V6":6,"V7":6,"V8":4,"V9":51},"delta_upper":{"2,10":"7.599e-11","2,24":"6.309e-112","3,10":"2.437e-9","3,24":"2.023e-110"},"floor_min_pivot":{"2":"3/4","3":"329/556"},"object":"CL-V24-TWO-THIRDS-TRANSFER-20261007-v1","passed":true,"transfer_over_S":{"2,10":{"R":"7.804e-6","c":"5.876e-9"},"2,24":{"R":"6.479e-107","c":"4.878e-110"},"3,10":{"R":"4.969e-4","c":"1.965e-7"},"3,24":{"R":"4.125e-105","c":"1.632e-108"}}}
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_