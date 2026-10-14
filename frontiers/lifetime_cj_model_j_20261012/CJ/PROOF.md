# Lifetime note CJ: a certified enclosure of note C3's model number `J`, and the value of the candidate density's `ℓ^{2/3}` coefficient at every side `L ≥ 10`

Object: `CL-CJ-MODEL-J-ENCLOSURE-20261007-v1`. Claim: main#229 6038732027, which took the `J` half of request 1 of 6033651797;
its lease lapsed on 7 October when the author's session hit a usage limit, and the main#307 comment that carries this note
renews it.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 7 October 2026, revised 12 October 2026 after
the author-side referee round of §7, for Dylan Roy (delegated AI work). The same session wrote #242, #244 and notes C3, SL, C7,
V24 and DC.
Disposition: AUTHOR-SIDE PROOF CANDIDATE, computer-assisted; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no
register, graph, STATUS, PROOF_INDEX, prize or Boolean change. Same GitHub account as every lane; organizational independence
0.

Proposition 2's enclosure is computed by the standard-library script of §6, in outward-rounded decimal arithmetic. Every
other step is proved by hand. The script also checks, independently of the production lines: Lemma 1's `k`-integral at three
points, by a separate bracket; Lemma 1's constant, built from its derivation; the special functions against the Wronskian and
two series; the derivative formulas of Lemma 2, by bracketed increments; and the quadrature machinery against a closed form.
As internal controls, it checks the remainder assembly against the Leibniz majorant and an exact rational sum, and every
certified printed number against this text (§6).

**What is new.**
- **Theorem CJ.** `4.1977819534 ≤ J ≤ 4.1977820097`, where `J = (16/15)∫_0^∞ e^{−12k²}E[(3kB − γ²/4)₊³]k^{−8/3} dk` with
  `γ, B` independent `N(0, 2)` (note C3's (G)). So `J = 4.19778198 ± 3·10⁻⁸`.
- **Corollary CJ1 (the candidate density).** For `d ∈ {2, 3}` and every real side `L ≥ 10`, note C3's coefficient `c₃(L)`
  of `ℓ^{2/3}` in the candidate density satisfies

  | `d` | `L ≥ 10` | `L ≥ 24` |
  |---|---|---|
  | 2 | `0.012789638 ≤ c₃(L) ≤ 0.012789640` | `0.012789638 ≤ c₃(L) ≤ 0.012789639` |
  | 3 | `0.016092288 ≤ c₃(L) ≤ 0.016092334` | `0.016092310 ≤ c₃(L) ≤ 0.016092312` |

  For SIDE24, `c₃(24) = 0.016092311 ± 10⁻⁹`. This does not use #244.
- **Corollary CJ2 (note C7's coefficient).** At #244 Theorem A's conditional scope, `J/30 − Ĩ ≥ 0.311509`, so for every real
  `L ≥ 10`: `(c₃ − R_{2/3})(L) ≥ 0.035768` (`d = 3`; `≥ 0.035825` for `L ≥ 24`) and `≥ 0.028472` (`d = 2`). Note DC had
  `0.1711𝒮_d`, that is `0.019677` and `0.015639`. The exploration values are `0.0774672` and `0.0615684` (note V24,
  Remark 1); the certified bounds are about 46% of them. The bound is one-sided because `D` has no certified lower bound.
- **The route.**
  - Integrating `k` out first gives a modified Bessel function (Lemma 1):
    `J = (16/45)(4π)^{−1/2}∫_0^∞ h(a)ψ(a) da` with `h(a) := E[(a − W)₊³]`, `W ~ Gamma(1/2, 1)`, and
    `ψ(a) := (432/a²)^{2/3}K_{4/3}(2a/√3)`.
  - `h` has closed-form derivatives through lower incomplete gamma functions, with explicit monotonicity, and `ψ` is
    completely monotone (Lemma 2).
  - So Simpson's rule on each cell, with its remainder bounded through explicit bounds of the fourth derivative (Lemma 3),
    and closed-form tails (Lemma 4) enclose the integral.

**Not claimed.**
- No lower bound for `D`, so no value of note C7's coefficient: Corollary CJ2 is one-sided. The other half of request 1 of
  6033651797, a two-sided enclosure of `D`, stays open.
- Corollary CJ2 rests on #244's Theorem A through notes V24 and DC; Theorem CJ and Corollary CJ1 do not. #244's Theorem A
  is conditional on merged author-side candidates at their stated scope: #170 Theorem E(1), [CUB] Theorem C, and [CUB]'s
  height identities (C8)–(C11) with its `B = 0` paragraph (#244's disposition). Corollary CJ2 also inherits the scopes of
  notes C7 and V24, as note DC's Corollary DC2 does.
- Nothing for `d ≥ 4` or `L < 10` (note V24's scope), and no rate (notes C3 and C7 keep their `o(ℓ^{2/3})`).
- Proposition 2 is computer-assisted. The script ran on CPython 3.11.15 with libmpdec 2.5.1 (Python's `decimal`), with
  directed rounding. Its rigor assumes the documented correct rounding of `exp` and `ln`, which it widens by one unit in the
  last place. Square roots are verified by squaring.

**Consumed.**
- Note C3 (main#229 6027862273; Slices A, B and C PASS): (G), the definition of `J`, and Proposition G,
  `c₃^∞ = (J/30)𝒮_d`.
- Note V24 (main#229 6034159111; Slices A, B and C PASS): Theorem V's table, both columns of each side.
- Note DC (main#229 6037455875; Slices A, B and C PASS): Theorem DC (`D ≤ 0.438822`) and the enclosure
  `−Ĩ_quad ∈ [0.6104056, 0.6104057]` (group corollary), with note V24's identity `Ĩ = Ĩ_quad + D`; for Corollary CJ2 only.
- #242 `frontiers/soft_rejected_pairs_20261002/PROOF.md` (blob `271412db`): Corollary 1′, `𝒮₂ = 25√3/(48π²)`,
  `𝒮₃ = 125√30/(192π³)`.

**Cited only.**
- Note C7 (main#229 6030039377): Theorem C7, which identifies `c₃ − R_{2/3}` as the `ℓ^{2/3}` coefficient of the elder
  density `ν_eld`, for the name of Corollary CJ2; and note SL's `R_{2/3}`, through note V24's Theorem V.
- The NIST Digital Library of Mathematical Functions (DLMF), for standard facts about Bessel and gamma functions: 10.25.2
  (the series of `I_ν`), 10.27.4 (`K_ν` through `I_{±ν}`), 10.28.2 (a Wronskian), 10.29.1 and 10.29.4 (recurrences), 10.30.2
  (`K_ν` near `0`), 10.32.9 and 10.32.10 (integral representations of `K_ν`), 10.43.19 (the Mellin transform of `K_ν`), and
  8.5.1 with 8.7.1 (the series of `γ(a, x)`).

**Prior work and overlap.**
- I read main#229 from 6037933403 to 6038554880 and found no other claim on `J`; main#307 (the board's continuation) has no
  claim on `J` either, through 6129928223.
- Note V24 proves only `J ∈ [1/2000, 10]` (Lemma J). Note C3 §5 and its Slice C referee give the floating-point value
  `4.1977819815839`; the referee integrated `B` against `K_{4/3}`, the same Bessel function as Lemma 1.
- No packet on Math- `main` at `7d2f6250` encloses `J`, and none of the packets landed since (through `aef861eb`) does.

## 0. Setting

Let `γ, B` be independent `N(0, 2)`, and `W := γ²/4`. Then `γ²/2` is `χ²₁`, so `W` is `Gamma(1/2, 1)`, with density
`π^{−1/2}w^{−1/2}e^{−w}` on `(0, ∞)`. Note C3's (G) is

    J = (16/15)∫_0^∞ e^{−12k²}E[(3kB − W)₊³] k^{−8/3} dk.                                                    (0.1)

Put `h(a) := E[(a − W)₊³]` for real `a` (so `h = 0` on `(−∞, 0]`), `b := 2/√3`, and

    ψ(a) := (432/a²)^{2/3}K_{4/3}(ba)   (a > 0),                                                               (0.2)

with `K_ν` the modified Bessel function of the second kind. `γ(s, x) := ∫_0^x t^{s−1}e^{−t}dt` is the lower incomplete gamma
function.

## 1. Lemma 1: integrating `k` out

**Lemma 1.** `J = (16/45)(4π)^{−1/2}∫_0^∞ h(a)ψ(a) da`.

*Proof.* For `k > 0`, `E[(3kB − W)₊³ | B] = h(3kB)`, which vanishes for `B ≤ 0`. With the density `(4π)^{−1/2}e^{−B²/4}` of `B`
and `a = 3kB`,

    E[(3kB − W)₊³] = ∫_0^∞ h(a)(4π)^{−1/2}e^{−a²/(36k²)} da/(3k).

Everything is nonnegative, so by Tonelli

    J = (16/45)(4π)^{−1/2}∫_0^∞ h(a)[∫_0^∞ k^{−11/3}e^{−12k² − a²/(36k²)} dk] da.

In the inner integral put `p = 12`, `q = a²/36` and `t = pk²`, so `dk = dt/(2√(pt))`:

    ∫_0^∞ k^{−11/3}e^{−pk² − q/k²} dk = ½p^{4/3}∫_0^∞ t^{−7/3}e^{−t − pq/t} dt = p^{4/3}(pq)^{−2/3}K_{4/3}(2√(pq)),

by DLMF 10.32.10, `∫_0^∞ t^{−ν−1}e^{−t − z²/(4t)}dt = 2(z/2)^{−ν}K_ν(z)`, with `ν = 4/3` and `z = 2√(pq)`. Here
`p^{4/3}(pq)^{−2/3} = (p/q)^{2/3} = (432/a²)^{2/3}` and `2√(pq) = 2a/√3 = ba`. ∎

The control group representation checks the inner identity at `a = 1/2, 2, 5` by a separate bracket of the left side. It
also builds the constant from its derivation, `(16/15)·(1/3)·(4π)^{−1/2}` (the `16/15` of (0.1), the `1/3` of `dB = da/(3k)`
and the density of `B`), and checks it against the literal `16/45` of Lemma 1 and the identity `KJ·√(4π)·45/16 = 1` (§6).

## 2. Lemma 2: the two factors

**Lemma 2.** (a) *The factor `h`.* On `(0, ∞)`, `h` is `C⁴`, with

    h′ = 3E[(a − W)₊²],  h″ = 6E[(a − W)₊],  h‴ = 6P(W ≤ a),  h⁗ = 6π^{−1/2}a^{−1/2}e^{−a},                 (2.1)

and `E[(a − W)₊ⁿ] = π^{−1/2}Σ_{k=0}^n C(n, k)a^{n−k}(−1)^kγ(k + ½, a)`. The functions `h, h′, h″, h‴` are nonnegative and
nondecreasing, and `h⁗` is positive and nonincreasing. Moreover `h(a) ≤ a³` and `h(a) ≤ (32/35)π^{−1/2}a^{7/2}`.

(b) *The factor `ψ`.* `ψ` is completely monotone on `(0, ∞)`: `(−1)^jψ^{(j)} > 0` for every `j`, so each `|ψ^{(j)}|` is
nonincreasing. With `u(x) := x^{−4/3}K_{4/3}(x)`, `ψ^{(j)}(a) = 432^{2/3}b^{4/3 + j}u^{(j)}(ba)` and, for `ν = 4/3`,

    u′ = −x^{−ν}K_{ν+1},  u″ = x^{−ν}K_{ν+2} − x^{−ν−1}K_{ν+1},  u‴ = 3x^{−ν−1}K_{ν+2} − x^{−ν}K_{ν+3},
    u⁗ = 3x^{−ν−2}K_{ν+2} − 6x^{−ν−1}K_{ν+3} + x^{−ν}K_{ν+4}.                                                  (2.2)

Moreover `ψ(a) ≤ 432^{2/3}2^{1/3}Γ(4/3)b^{−4/3}a^{−8/3}`, and `K_ν(x) ≤ K_ν(x₀)e^{−(x − x₀)}` for `x ≥ x₀ > 0`.

*Proof.* (a) For `n ≥ 2`, `d/da E[(a − W)₊ⁿ] = nE[(a − W)₊^{n−1}]` by dominated differentiation; for `n = 1` the derivative
is `P(W < a) = P(W ≤ a)` (dominated convergence; `W` has a density); and `d/da P(W ≤ a)` is the density of `W`. This gives
(2.1). The first four are expectations of nonnegative functions that are nondecreasing in `a`. The density
`π^{−1/2}a^{−1/2}e^{−a}` decreases. Expanding `(a − w)ⁿ` and integrating against the density of `W` over `(0, a)` gives the
sum, since `∫_0^a w^{k−1/2}e^{−w}dw = γ(k + ½, a)`. Finally `(a − W)₊³ ≤ a³` for `a > 0`, and

    h(a) = π^{−1/2}∫_0^a (a − w)³w^{−1/2}e^{−w}dw ≤ π^{−1/2}∫_0^a (a − w)³w^{−1/2}dw = π^{−1/2}a^{7/2}B(½, 4),

with `B(½, 4) = Γ(½)Γ(4)/Γ(9/2) = 32/35`.

(b) By DLMF 10.32.9, `K_ν(x) = ∫_0^∞ e^{−x cosh t}cosh(νt)dt`, a Laplace transform of a positive measure, so `K_ν` is
completely monotone; so is `x^{−4/3}`, and so is their product, `u` (products of completely monotone functions are completely
monotone). Composition with `a ↦ ba`, `b > 0`, preserves it. The derivative of a completely monotone function is minus a
completely monotone function, so `|ψ^{(j)}|` is nonincreasing. Strict signs: by Leibniz,
`(−1)^jψ^{(j)}(a) = 432^{2/3}Σ_i C(j, i)[(−1)^i(a^{−4/3})^{(i)}]·[b^{j−i}(−1)^{j−i}K_{4/3}^{(j−i)}(ba)]`, and every factor is
positive, since `(−1)^mK_ν^{(m)}(x) = ∫_0^∞(cosh t)^me^{−x cosh t}cosh(νt)dt > 0`. For (2.2), DLMF 10.29.4 gives
`(d/dx)[x^{−μ}K_μ(x)] = −x^{−μ}K_{μ+1}(x)` for every `μ`. With `w_m := x^{−ν−m}K_{ν+m}`, this reads `w_m′ = −x·w_{m+1}`, and

    u = w_0,  u′ = −x w_1,  u″ = −w_1 + x²w_2,  u‴ = 3x w_2 − x³w_3,  u⁗ = 3w_2 − 6x²w_3 + x⁴w_4,

which is (2.2). The bound on `ψ`: `x^νK_ν(x)` is nonincreasing (`(x^νK_ν)′ = −x^νK_{ν−1} < 0`, DLMF 10.29.4) and tends to
`2^{ν−1}Γ(ν)` at `0` (DLMF 10.30.2), so `K_ν(x) ≤ 2^{ν−1}Γ(ν)x^{−ν}`. The last bound follows from 10.32.9 and `cosh t ≥ 1`:
`e^{−x cosh t} ≤ e^{−x₀cosh t}e^{−(x − x₀)}`. ∎

*Evaluation of the special functions* (used by the script; each is an enclosure).
- `π` by Machin's formula, each arctangent series stopped with its first omitted term as the error.
- `Γ(1/3)` and `Γ(2/3)` from `Γ(a) = γ(a, X) + Γ(a, X)` at `X = 130`: `γ(a, X) = X^ae^{−X}Σ_{n≥0}X^n/(a(a+1)···(a+n))` (DLMF
  8.7.1 with 8.2.6; equivalently 8.5.1, the Kummer-function form, with `M` expanded; positive terms, tail bounded
  geometrically once the ratio `X/(a + n + 1)` is below `1`), and `0 ≤ Γ(a, X) ≤ X^{a−1}e^{−X}` for `a ≤ 1`. The script
  checks both against the reflection formula `Γ(1/3)Γ(2/3) = 2π/√3`.
- `I_μ(x) = (x/2)^μΣ_m (x²/4)^m/(m!Γ(m + μ + 1))` (DLMF 10.25.2) for `μ = ±4/3, ±7/3`, with `1/Γ(m + μ + 1)` from
  `Γ(1/3)`, `Γ(2/3)` and `Γ(x + 1) = xΓ(x)`. From `m = 2` on, the terms have one sign and the ratios
  `(x²/4)/((m + 1)(m + 1 + μ))` decrease; once the ratio is at most `½`, the tail is at most the last term.
- `K_{4/3} = (π/√3)(I_{4/3} − I_{−4/3})` and `K_{7/3} = (π/√3)(I_{−7/3} − I_{7/3})` (DLMF 10.27.4, with
  `sin(4π/3) = −√3/2`, `sin(7π/3) = √3/2`), then `K_{10/3}, K_{13/3}, K_{16/3}` by `K_{μ+1} = K_{μ−1} + (2μ/x)K_μ`
  (10.29.1), which adds positive terms. The cancellation in `I_{−ν} − I_ν` costs about `29.6` digits at the largest argument
  `x = 30b ≈ 34.64`; there the `K` enclosures have relative width about `1.5·10⁻¹⁵`, set by stopping each series at `10⁻⁴⁵`
  of its sum. The script works with `50` digits.
- `γ(s, a)` for `s = ½, 3/2, 5/2, 7/2` by the same positive series as `γ(a, X)`, stopped once the next ratio `a/(s + n + 1)`
  is at most `½`; the later ratios are smaller, so the tail is at most the last term, which is added on the right.

## 3. Lemma 3: Simpson cells

**Lemma 3.** Let `0 < a₀ < a₁`, `Δ := a₁ − a₀`, `m := (a₀ + a₁)/2` and `F := hψ`. Then

    |∫_{a₀}^{a₁}F − (Δ/6)(F(a₀) + 4F(m) + F(a₁))| ≤ (Δ⁵/2880)·Σ_{j=0}^4 C(4, j)·H_j·|ψ^{(4−j)}(a₀)|,                (3.1)

with `H_j := h^{(j)}(a₁)` for `j ≤ 3` and `H_4 := h⁗(a₀)`.

*Proof.* `F` is `C⁴` on `[a₀, a₁]` (Lemma 2), and Simpson's rule has remainder `−(Δ⁵/2880)F⁗(ξ)` for some `ξ ∈ (a₀, a₁)`. By
Leibniz, `|F⁗| ≤ Σ_jC(4, j)|h^{(j)}||ψ^{(4−j)}|`. On the cell, `0 ≤ h^{(j)} ≤ h^{(j)}(a₁)` for `j ≤ 3`, `0 < h⁗ ≤ h⁗(a₀)`,
and `|ψ^{(i)}| ≤ |ψ^{(i)}(a₀)|`, by Lemma 2. ∎

The majorant of (3.1) therefore dominates the Leibniz majorant `Σ_jC(4, j)h^{(j)}(x)|ψ^{(4−j)}(x)|` at every `x` of the cell;
the script checks this at `a₀`, `m` and `a₁` of every cell (group remainder, §6).

## 4. Lemma 4: the tails

**Lemma 4.** For `0 < A₀ < A₁`:

    0 ≤ ∫_0^{A₀}hψ ≤ (32/35)π^{−1/2}·432^{2/3}2^{1/3}Γ(4/3)b^{−4/3}·(6/11)A₀^{11/6},
    0 ≤ ∫_{A₁}^∞hψ ≤ 432^{2/3}A₁^{−4/3}K_{4/3}(bA₁)·(A₁³/b + 3A₁²/b² + 6A₁/b³ + 6/b⁴).

*Proof.* Near `0`, use `h(a) ≤ (32/35)π^{−1/2}a^{7/2}` and `ψ(a) ≤ 432^{2/3}2^{1/3}Γ(4/3)b^{−4/3}a^{−8/3}`, and integrate
`a^{5/6}`. Above `A₁`, use `h(a) ≤ a³`, `a^{−4/3} ≤ A₁^{−4/3}` and `K_{4/3}(ba) ≤ K_{4/3}(bA₁)e^{−b(a − A₁)}`, and integrate
`a³e^{−b(a − A₁)}` exactly. ∎

## 5. Proposition 2, Theorem CJ and the corollaries

**Proposition 2.** On the partition of `[10⁻⁶, 30]` into 1500 cells,
- `300` geometric cells on `[10⁻⁶, 0.05]` (ratio `(5·10⁴)^{1/300}`),
- uniform cells: `400` on `[0.05, 1]`, `300` on `[1, 4]`, `300` on `[4, 12]` and `200` on `[12, 30]`,

every interior point rounded to 12 significant digits (which changes only the geometric piece and `[4, 12]`, whose step `2/75`
is not a terminating decimal), the sum of the Simpson values of `hψ` with the remainders (3.1), Lemma 4 with `A₀ = 10⁻⁶` and
`A₁ = 30`, and Lemma 1 give

    4.1977819534 ≤ J ≤ 4.1977820097.

The Simpson remainders contribute at most `2.81·10⁻⁸` and the tails at most `1.53·10⁻¹¹` (after the factor
`(16/45)(4π)^{−1/2}`). Cell widths and midpoints are exact decimals.

*Proof.* The script evaluates `h` and `ψ` with their derivatives by Lemma 2 and the enclosures listed after it, in interval
arithmetic with outward rounding, and sums (3.1) cell by cell, and Lemma 4. ∎

**Theorem CJ** follows from Lemma 1 and Proposition 2.

*Proof of Corollary CJ1.* Note C3's Proposition G gives the model value `c₃^∞ = (J/30)𝒮_d`, with #242's Corollary 1′ for
`𝒮_d`. Note V24's Theorem V gives `|c₃(L) − c₃^∞| ≤ η_c𝒮_d` with `η_c = 5.88·10⁻⁹` (`d = 2`) and `1.97·10⁻⁷` (`d = 3`) for
`L ≥ 10`, and `4.88·10⁻¹¹⁰`, `1.64·10⁻¹⁰⁸` for `L ≥ 24`. The script evaluates `[(J_lo/30 − η_c)𝒮_d, (J_hi/30 + η_c)𝒮_d]`
outward. Note V24's `c₃` half does not use #244. ∎

*Proof of Corollary CJ2.* Note V24 gives `Ĩ = Ĩ_quad + D`, and note DC gives `D ≤ 0.438822` and
`−Ĩ_quad ≥ 0.6104056`, at #244 Theorem A's conditional scope. So `J/30 − Ĩ ≥ 4.1977819534/30 + 0.6104056 − 0.438822 ≥
0.311509`. With note V24's `|R_{2/3}(L) − Ĩ𝒮_d| ≤ η_R𝒮_d` (`η_R = 7.81·10⁻⁶`, `4.97·10⁻⁴` for `L ≥ 10`; `6.48·10⁻¹⁰⁷`,
`4.13·10⁻¹⁰⁵` for `L ≥ 24`), `(c₃ − R_{2/3})(L) ≥ (0.311509 − η_c − η_R)𝒮_d`, evaluated outward by the script. ∎

**Remarks.**
1. *Precision.* The enclosure's width, `5.6·10⁻⁸`, is almost all Simpson's remainder bound, which is pessimistic by a factor
   of about `5300`: the midpoint of the enclosure is within `10⁻¹⁰` of the floating-point value `4.19778198158390`. A finer
   partition would narrow it.
2. *Note C7's coefficient.* With `D` known numerically (`0.0767381`, note V24 Remark 1), `J/30 − Ĩ = 0.673594` and the
   coefficient is `0.0774672` in `d = 3`. Corollary CJ2's `0.311509` is a certified lower bound; certifying the value needs a
   lower bound for `D` (note DC, Remark 3, sketches a route).
3. *Floating-point references.* The assembly value `4.1977819815839038` was computed in `mpmath` at 30 digits from Lemma 1's
   form, with `h` by incomplete gamma functions and `besselk`. Two independent evaluations straight from (0.1), with `B`
   integrated in closed form and no Bessel function (the Slice A and Slice B referees of §7), give
   `4.197781981583903820606028` and `4.19778198158390381`; a third, in Lemma 1's form with `h` by direct quadrature
   (Slice A), gives `4.197781981583903820606025`, and a fourth, with `h` by Kummer's `₁F₁` (Slice B), gives
   `4.19778198158390382`. All lie inside the enclosure.

## 6. Controls (`cj_exact.py`; standard library; deterministic; byte-identical under `-O`)

`python3 -B -S cj_exact.py` prints one JSON line (835 bytes with its newline, SHA-256 `c42031da…5a34e`) and exits 0. The
script is 26,090 bytes, SHA-256 `b3be1503…15458`. It runs at 50 digits in about 50 seconds, 21,154 checks in all. Every check
is `need(...)`; a failed check prints `FAILED: <group>` on stderr, nothing on stdout, and exits 1; the domain guards of the
interval primitives fail the same way, as groups interval_division, interval_sqrt and interval_ln. An invalid invocation
prints the usage line and exits 2. The default `decimal` context traps every inexact or rounded operation, so any arithmetic
written without an explicit directed context can only ever be exact.

| group | checks |
|---|---|
| primitives | `neg` and `absmax` (interval negation and absolute value) are exact at 50 digits |
| pi | Machin's `π`: width below `10⁻⁴⁵`, against 50 digits |
| gamma | `Γ(1/3)`, `Γ(2/3)` against 50 digits, the reflection formula, widths |
| bessel | the Wronskian `I_ν K_{ν+1} + I_{ν+1}K_ν = 1/x` (DLMF 10.28.2) at `x = 0.3, 1.7, 6.5, 20, 34`; `K_{4/3}(x + 1) ≤ e^{−1}K_{4/3}(x)` at three points; positivity of every `K` evaluated |
| h_function | at six points: nonnegativity, the two bounds of Lemma 2(a), the increment of each of `h, h′, h″, h‴` over `[a, a + 10⁻⁶]` against the next derivative at both ends, and, for `a ≤ 0.01`, `h` against the alternating series `π^{−1/2}Σ_n(−1)^na^{n+7/2}B(n + ½, 4)/n!` |
| psi_function | at the same points: the signs of `ψ, …, ψ⁗` and the increments of `ψ, …, ψ‴` against the next derivative, which checks (2.2) |
| representation | Lemma 1's `k`-integral at `a = 1/2, 2, 5`: a monotone-cell bracket (10,000 geometric cells on `[0.004, 4]`, tails bounded) contains `(432/a²)^{2/3}K_{4/3}(ba)` and is narrower than 2%; the constant `(16/15)·(1/3)·(4π)^{−1/2}` against the literal `16/45·(4π)^{−1/2}`, and `KJ·(4π)^{1/2}·45/16 = 1` |
| partition | the partition: consecutive pieces share endpoints, the points increase, the ends are `10⁻⁶` and `30` |
| moment | the Simpson sums, the `j ≤ 3` terms of (3.1), `ψ` and its derivatives and both tail formulas, with `h` replaced by `a³`, against `∫_0^∞a³ψ = 432^{2/3}2^{2/3}b^{−8/3}Γ(2/3)` (DLMF 10.43.19); exact widths, sums and midpoints of every cell; the rounded remainder sum against the same sum in exact rational arithmetic. A dropped remainder fails it, and so does a remainder divided by `1000`, through the rational sum |
| remainder | at `a₀`, `m` and `a₁` of every cell, in both Simpson runs: the majorant of (3.1) is at least the Leibniz majorant `Σ_jC(4, j)h^{(j)}|ψ^{(4−j)}|` evaluated there from the lower ends of the enclosures, with binomials from `math.comb` |
| J_cells | exact widths, sums and midpoints; the rounded remainder sum against the exact rational sum; `J > 0`; width below `10⁻⁷`; the width of `J` is at least `KJ_lo·(2·remainder + tails)`, so no allowance was dropped |
| tails | both tails below `10⁻⁹`; the exponent `11/6 > 0` |
| assembly | the enclosure contains the floating-point value `4.1977819815839038` (Remark 3) |
| corollary | `0.31150 ≤ J_lo/30 + 0.6104056 − 0.438822 ≤ 0.31151`; positivity of every bound of Corollaries CJ1 and CJ2 |
| pinned | every certified printed string equals this note's text: the two endpoints of `J`, the remainder and tail allowances, `0.311509`, and the twelve numbers of Corollaries CJ1 and CJ2 |

Mutants (`--mutant Mi`; each exits 1 with empty stdout, at the stated group):

| mutant | change | fails at |
|---|---|---|
| M1 | `Γ(a, X)`'s bound replaced by `−10³⁰` times itself | gamma |
| M2 | `K_{4/3}` multiplied by `1.01` | bessel |
| M3 | `h` replaced by `E[(a − W)₊²]` | h_function |
| M4 | `u⁗`'s coefficient `6` replaced by `5` | psi_function |
| M5 | Simpson's middle weight `4` replaced by `3` | moment |
| M6 | `ψ`'s Bessel argument `ba` replaced by `1.1ba` | psi_function |
| M7 | the second piece of the partition starts at `0.06` | partition |
| M8 | Lemma 1's constant `16/45` replaced by `16/15` (the factor `1/3` dropped) | representation |
| M9 | note DC's `0.438822` replaced by `0.338822` | corollary |
| M10 | `γ(3/2, a)` replaced by `γ(5/2, a)` | h_function |
| M11 | Simpson's constant `2880` replaced by `2880000` (the remainder divided by `1000`) | moment |
| M12 | the binomials of (3.1) replaced by `1, 1, 1, 1, 1` | remainder |
| M13 | both tails dropped from the upper end of the integral | J_cells |
| M14 | `η_c` dropped from the lower bounds of Corollary CJ1 | pinned |

Invalid invocations (exit 2): `--bogus`, `--mutant M15`, a bare `--mutant`, `--mutant m14`, `--mutant M1 extra`.

*What no control cross-checks.* The choice of endpoints in (3.1) beyond the three-point domination of group remainder (a
mutant that takes `h^{(j)}` at `a₀` instead of `a₁` passes every numerical group and fails only at pinned); the tail constants
of Lemma 4 beyond `< 10⁻⁹` and the pinned strings; the `𝒮_d` and `η` arithmetic of the corollaries beyond positivity, the
`0.3115` bracket and the pinned strings; libmpdec's correct rounding of `exp` and `ln`; and the analytic steps of Lemmas 1–4
beyond their numerical identities.

*Author-side probes.* Twelve one-line edits that each narrow a certified bound (the Slice B referee's list, four of which
are now mutants M11–M14: the
remainder divided by `1000` or set to `0`, `h^{(j)}` or `ψ^{(i)}` taken at the wrong endpoint, the binomials replaced by
ones, `Δ⁶` for `Δ⁵`, the tails or the remainder dropped from one end, the low tail's exponent raised, `η_c` or `η_R`
dropped, and `−Ĩ_quad` raised by `10⁻⁶`) all exit 1 under the revised script, at moment, remainder, J_cells, pinned or
corollary. Before the revision ten of them passed every check.

## 7. Review

*Author-side referee round (7 October), clean context, two slices by separate Claude agents given only the draft, the script
and the expected stdout.* Slice A (§§0–2): BLOCK, one finding: `neg` and `absmax` used Python's unary minus and `abs()`, which
round to the thread's default 28-digit context, so the `ψ′` enclosure missed the true value at most Simpson nodes by up to
`4.9·10⁻²⁸` relative; the printed numbers were unaffected (the fix moves the unquantized endpoints by about `10⁻³⁷`). Fixed
by `copy_negate()` and `copy_abs()`, a trapping default context and group primitives. Its non-blocking points (the circular
constant check, the `n = 1` case of Lemma 2(a), the strict signs, the series stopping rules) are applied above. Slice B
(§§3–6 and the header): AMEND, no blocking finding; its main point, that most edits which only narrow the enclosure were
caught by no control, is answered by the rational remainder sum, groups remainder, J_cells' width test and pinned, and
mutants M11–M14; its nits (the moment row, the partition description, the `d = 2, L ≥ 24` row, Remark 2's `0.0767381`, the
exact midpoint test, the domain-guard sentence, two wordings in the header and Remark 2, the route of the assembly value,
the citation of notes C7 and SL) are applied above. Both referees evaluated `J` independently from (0.1) (Remark 3). A
third agent then read the revision back against both reports in a clean context (AMEND: one misattributed floating-point
route in Remark 3, corrected). Their reports and scratch work are kept with the author's record. These reads are
same-provider and earn no organizational-independence credit.

*Nonauthor slices requested (main#307):*
- **A** — §§0–2: the setting, Lemma 1 (with DLMF 10.32.10) and Lemma 2 (including complete monotonicity and (2.2)); groups
  primitives, representation, h_function, psi_function; mutants M3, M4, M8, M10.
- **B** — §§3–6 and the header: Lemma 3, Lemma 4, the evaluation of the special functions, Proposition 2, Theorem CJ, the
  corollaries against notes C3, V24 and DC, and the script; the remaining groups; mutants M1, M2, M5, M6, M7, M9, M11–M14
  and the invalid invocations.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_