# The third-order coefficient of the short-lifetime law: the fold-scale finite part, `d = 1, 2, 3`

Object: CL-THIRD-ORDER-COEFF-20261001-v1.1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 1 October 2026.
**v1.1 (after the Codex review of v1 on Math- #216, head `205550f`).**
- *Replay.* The replay is now interpreter-independent: every float sum uses `math.fsum`, and the `r`-fit uses `r/max r`.
  The output is byte-identical on CPython 3.10–3.14.
- *Precision.* `c₂` is quoted to 8 significant digits. Summation order moves the 10th digit.
- *Workflow.* The workflow verifies the cited unmerged sources by blob id.
- *Provenance.* The owner's post-stop instructions are recorded exactly (`SOURCES.json`, `delivered_under`).
The coefficients are unchanged.
Disposition: FORMAL COEFFICIENT WITH NUMERICAL EVIDENCE. In `d = 1` it is a theorem (Math- #214); in `d ≥ 2` the
expansion (0.2) is not proved here. Nonauthor review required. Scientific effect: NONE — no register, graph, STATUS,
PROOF_INDEX, prize or Boolean change. Same GitHub account as every lane; zero organizational independence.
**Dependencies:** none consumed. The computation uses only the merged two-point kernel of [R]
(`frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf`). The following are cited for comparison:
- Math- #214 (`d = 1`, Theorem D1);
- Math- #207 (Theorem CU: `c₁` and the cusp loss);
- Math- #191 (the even contact expansion);
- the merged values of `c_{2,∞}` and `c_{3,∞}`.

## 0. Statement

**Setting.** We use the notation of [R] §§2–4 and #207 §0:
- the [P] field on `X = R^d/(LZ^d)`, with pins `M = −ru/2` and `S = ru/2`;
- the symmetric pin vector `U_r`, with target `v_r = (b − kr³/2, −kr², 0, 12k, 0, …, 0)`;
- its density `π_r`;
- the two-point kernel

      A_r(b, k, u) = 12 π_r(v_r) E[ |det H_M| |det H_S| 1{typed} | U_r = v_r ] / r²,

  so that the near part of the elder lifetime density is `∫dσ(u)∫db∫dr r^{−2}A_r^{eld}(b, ℓ/r³, u)` (#207 (0.1)).

At fixed `(b, k, u)`, `A_r = A₀ + r²A₂ + O(r³)`. There is no `r¹` term (#191's even contact expansion; checker T5).
Here `A₀ = 12π₀(v₀)·36k²E[Δ²1{A<0} | v₀]` is the contact kernel, and

    A₂(b, 0, u) = −12 π₀(u; v₀(b, 0)) E₀[ Y² 1{A < 0} | b ]                                              (0.1)

is the small-`s` limit of #207's cusp loss `loss(s) → Y²` (`s → 0`), with `Y = (f₄/12)Δ − γᵀadj(A)γ/4`. Define

    c₂ := (1/3) ∫_{S^{d−1}} ∫_R ∫_0^∞ [A₂(b, k, u) − A₂(b, 0, u)] k^{−4/3} dk db dσ(u),

the Hadamard finite part of `(1/3)∫A₂k^{−4/3}dk`. The integral converges: `A₂(b, k) − A₂(b, 0) = O(k)` as `k → 0`.

**Claim (formal in `d ≥ 2`).**

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{1/2})        (ℓ ↓ 0),                         (0.2)

with `c₁` the coefficient of #207 (CU.2). The same `c₂` appears in the near candidate density and in the density of
adjacent (max, saddle) pairs, with `c₁` replaced by `I^{cand} = (3^{1/4}/2)c₁` (#207 (CU′.1)). The reason is that `c₂` is
a fold-scale quantity, and the elder rule enters only through the cusp window.

**What is established here.**
1. **`d = 1`.** The formula gives exactly #214's `2B₂`, for every covariance satisfying #214's (H). For the finite part
   this is an identity (§2.3). For the total it is verified numerically to `10⁻⁹` for two kernels (checkers T1, T2). In
   `d = 1`, (0.2) is #214's Theorem D1.
2. **Values for the Gaussian kernel `e^{−|z|²/2}`** (the SIDE24 covariance up to factors `1 + O(e^{−L²/8})`):

   | `d` | `c` (recomputed; equals the merged value) | `c₂` | `c₂/c` | `c₁/c` (#207, #214) |
   |---|---|---|---|---|
   | 1 | `0.110110378959` (`C₀`) | `0.23004458` (`= 2B₂`) | `2.089218` | `−2.0671` |
   | 2 | `0.073406919306` (`c_{2,∞}`) | `0.22152441` | `3.017759` | `−3.6699` |
   | 3 | `0.041775931845` (`c_{3,∞}`) | `0.16123405` | `3.859496` | `−5.0711` |

   The numerical precision of `c₂` is about `2·10⁻⁸` relative. Changing the summation order (the built-in `sum` of
   CPython 3.12+ against `math.fsum`) moves it by up to that amount.

3. **Full-field Monte Carlo in `d = 2` and `d = 3` (§3; exploration, outside the repository).** The *parameter-free*
   three-term law (0.2) matches the actual elder-rule persistence of the periodized Gaussian field on `[10⁻⁴, 10⁻²]`.
   Both the leading term alone and the two-term law `cℓ^{−1/3} + c₁ℓ^{1/4}` are rejected.

**Consequence for SIDE24 (`d = 3`).** The relative correction is
`ν/(cℓ^{−1/3}) − 1 = −5.071ℓ^{7/12} + 3.859ℓ^{2/3} + …`. The `ℓ^{1/3}` term cancels about 40–50% of the `ℓ^{1/4}` term at
moderate `ℓ`. The combined correction is `1%` at `ℓ ≈ 4.6·10⁻⁵` and `10%` at `ℓ ≈ 3.6·10⁻³`. For the `ℓ^{1/4}` term alone
(#207 §8, V3 edit E15) the corresponding values are `2.3·10⁻⁵` and `1.2·10⁻³`. §4 gives the table.

**What is not claimed.**
- No proof of (0.2) in `d ≥ 2`. A proof needs a rate `O(r)` in #207's kernel limit CU.4, uniform in `κ` with integrable
  domination, together with quantitative fold-scale bounds. That is the open item "a rate for the `o(ℓ^{1/4})`"
  (concordance §9 item 6).
- No certified enclosure of `c₂`. The values are floating point; the stated digits are stable under the grid and `r`-set
  changes of checkers T3, T4.
- No statement about the terms after `c₂`.
- Nothing about `L ≠ ∞`, beyond the `O(e^{−L²/8})` periodization factors.

## 1. Why the finite part (formal derivation)

Put `s := rℓ^{−1/4}`, so that `κ = ℓ/r⁴ = s^{−4}` and `k = ℓ/r³ = ℓ^{1/4}s^{−3}`. The near integrand `r^{−2}A_r^{eld}(b, ℓ/r³, u)`
has two regimes.

- **Fold regime (`s ≪ 1`, `κ ≫ 1`).** Every typed pair is an elder pair: the non-elder part is `O(r³/k)`, [C7-K] (K2).
  At fixed `k`,

      r^{−2}A_r = r^{−2}A₀(b, k) + A₂(b, k) + O(r).

- **Cusp regime (`s ≍ 1`).** By #207 CU.4,

      r^{−2}A_r^{eld} = r^{−2}A₀ + (𝒜^{eld} − 𝒜^{con})(b, κ) + o(1),

  and `(𝒜^{eld} − 𝒜^{con})(b, κ) = −12π₀E₀[loss(s) | b] → A₂(b, 0)` as `κ → ∞`, by (0.1).

The composite approximation

    r^{−2}A₀(b, k) + A₂(b, k) + [(𝒜^{eld} − 𝒜^{con})(b, κ) − A₂(b, 0)]

reproduces both regimes:
- for `s ≪ 1` the bracket vanishes;
- for `s ≍ 1` we have `k → 0` and `A₂(b, k) → A₂(b, 0)`.

Integrating over `r` gives three pieces, each converging separately:

    ∫ r^{−2}A₀ dr = cℓ^{−1/3},
    ∫ [A₂(b, ℓ/r³) − A₂(b, 0)] dr = (ℓ^{1/3}/3) ∫ [A₂(b, k) − A₂(b, 0)] k^{−4/3} dk,
    ∫ (𝒜^{eld} − 𝒜^{con})(b, ℓ/r⁴) dr = ℓ^{1/4} ∫ (𝒜^{eld} − 𝒜^{con})(b, s^{−4}) ds.

The third piece is #207's `c₁` integrand. The neglected pieces are the following, each `O(ℓ^{1/2})` *if* the cusp limit
CU.4 holds with rate `O(r)`:
- the fold remainder;
- the cusp remainder;
- the mixed term `A₂(b, k) − A₂(b, 0) = O(k)` at `s ≍ 1`.

In `d = 1` this is exactly the structure of #214's Proposition 2.2:
- the fold part (c) gives `B₂^{(1)}`;
- the cusp part (d), split as `p₃(α) = p₃(0) + (p₃(α) − p₃(0))`, gives the Mellin term `(I_θ/2)h^{1/4}` and the finite
  part `B₂^{(2)}`.

There it is proved.

## 2. The computation

**2.1 Pinned Gaussian structure.**
- *Jets.* The jets `J = (∂^αf(0))_{|α|≤N}` at the midpoint have covariance `(−1)^{|β|}∂^{α+β}ρ(0)`. We take `N = 12, 10, 8`
  for `d = 1, 2, 3`.
- *Pin rows and Hessians.* Both are linear forms in `J`, by Taylor along `u = e₁`.
- *Truncation.* The error is `≤ r^{N−2}` times a Gaussian moment, below `10⁻¹⁵` relative at `r ≤ 0.011`.
- *Conditioning.* We condition on `U_r = v_r` in Decimal arithmetic (50 digits), then pass to floats. The small conditional
  variances, `O(r⁴)`, come from `O(1)` cancellations and need the extra digits.

**2.2 The typed indicator.**
- **`d = 1`.** At fixed `k > 0` the typed event has probability `1 − O(e^{−ck²/r²})`, so `E[(−h_M)h_S]` is used.
- **`d = 2`.** `1{typed} = 1{f_yy(0) < 0}` up to `O(r)` shifts of the boundary. Because `|det H_M det H_S|` vanishes
  quadratically there, the error in `A_r` is `O(r³)`. The expectation of the quartic product given `f_yy(0)` follows from
  Isserlis' formula; the half-line integral uses truncated Gaussian moments.
- **`d = 3`.** `1{typed} = 1{A < 0}`, with `A = D_y²f(0)` (`2 × 2`), again up to `O(r³)`.
  - The conditional law of `A` is invariant under transverse rotations. It is `Var a₁₁ = Var a₂₂ = 2`,
    `Cov(a₁₁, a₂₂) = 0` and `Var a₁₂ = 1`, given the pins.
  - So `E[det H_M det H_S | A]` depends only on the eigenvalues. It is a polynomial of degree `≤ 6` in
    `(b_eff, k, λ₁, λ₂)`, obtained from Isserlis' formula over the 76 partial matchings of each of the 36 permutation
    products.
  - It is integrated over `λ₂ < λ₁ < 0` with the eigenvalue Jacobian `π(λ₁ − λ₂)`.
  - Here `b_eff := b − kr³/2`, the target's height coordinate. The transverse block's conditional mean does not depend on
    `k`, by parity; the checker asserts this.

**2.3 The finite part in `d = 1`.**
- The `b`-integral of (0.1) is `−(σ₄²/12)p₁₂p₃(12k)`, because `Y = f₄/12` and `∫π₀E₀[f₄²]db = p₁₂p₃·σ₄²`.
- So the finite-part integral, with `α = 12k`, is `(2/3)(−σ₄²p₁₂/12)12^{1/3}∫₀^∞(p₃(α) − p₃(0))α^{−4/3}dα`. This is
  `2B₂^{(2)}` of #214 §2(e), the factor 2 accounting for the two orientations.
- The fold part is #214's `τ²`-coefficient of `(12/t⁴)p_tm²`, written in the coordinates of [R].
- T1 and T2 check the total against the closed form `2B₂` (#214 (D1.2)):
  - Gaussian kernel: `0.2300445808` against `0.2300445803`;
  - mixture `(e^{−x²/2} + e^{−2x²})/2`: `0.5760427428` against `0.5760427425`.

**2.4 Numerics.**
- *Expansion coefficients.* `A₀` and `A₂` come from least squares on `(1, r², r³, r⁴)` over five separations:
  `r = 0.001…0.005` in `d = 1`, `r = 0.003…0.011` in `d = 2, 3`.
- *Quadrature.* Gauss–Legendre in `b ∈ [−8, 8]` and in `t = k^{1/3} ∈ [0, K^{1/3}]`, with `K = 8`, and `K = 27` for the
  mixture.
- *Tail.* The term `|S^{d−1}|K^{−1/3}∫db(−A₂(b, 0))` beyond `K` is added analytically.
- *`d = 3` cone.* A Gauss–Legendre rule in `(s, t)`, with `λ₁ = −s` and `λ₂ = −s − t`.
- *Convergence.*

  | `d` | `c` relative error | `c₂` stability |
  |---|---|---|
  | 2 | `2·10⁻¹⁴` | two `r`-sets agree to `3·10⁻⁹` |
  | 3 | `10⁻¹⁰` (grid `(40, 80, 32²)`) | a coarser grid `(32, 48, 24²)` moves it by `4.5·10⁻⁸` |

  Rounding sensitivity is about `2·10⁻⁸` relative (v1.1 note).

## 3. Full-field Monte Carlo (exploration; outside the repository)

**Method** (C and numpy; archived with the project record, not part of this packet, per the standard-library rule).
- **Synthesis.** Exact spectral synthesis of the periodized kernel, with `ρ̂(k) = (2π)^{d/2}L^{−d}e^{−|k|²/2}`:
  - `d = 2`: `L = 64`, on a `2048²` grid;
  - `d = 3`: `L = 16`, on a `256³` grid.
- **Critical points.** All critical points are found and refined:
  - candidates from the fine-grid gradient;
  - Newton on degree-10 (`d = 2`) or degree-8 (`d = 3`) Taylor expansions, from spectrally exact coarse-grid derivatives;
  - a partner search along soft Hessian directions, for close fold pairs inside one cell.
- **Merges.** Ascending lines from every `(d−1)`-saddle, by RK2 with a backtracking line search, give the merges.
- **Persistence.** The superlevel `H₀` persistence follows by union–find with the elder rule. It is exact for the computed
  critical values.
- **Integrity.**
  - Critical-point counts match Kac–Rice: `d = 2`: `376.50` maxima per sample against `376.37`.
  - The Euler characteristic is 0 in every retained sample.
  - Every maximum but one dies.
  - A dense-seed Newton search found no missed critical point in six `20 × 20` subregions (`d = 2`) and two `5³` subregions
    (`d = 3`).
  - Taylor evaluation matches exact trigonometric evaluation to `10⁻¹⁴` (`d = 2`) and `3·10⁻¹⁰` (`d = 3`).

**Results (interim: `d = 2`, 1150 samples, volume `4.7·10⁶`; `d = 3`, 240 samples, volume `9.8·10⁵`).** Counts are binned
in 24 logarithmic bins on `[10⁻⁵, 0.3]` and compared with the bin integrals of (0.2). There are no free parameters.

| `d` | range of `ℓ` | elder pairs: data/(0.2) | `χ²/bins` | adjacent pairs: data/(0.2 with `I^{cand}`) | `χ²/bins` |
|---|---|---|---|---|---|
| 2 | `[10⁻⁴, 10⁻²]` | `0.999 ± 0.007` | `5.1/11` | `0.997 ± 0.007` | `5.9/11` |
| 2 | `[10⁻⁴, 3·10⁻²]` | `1.012 ± 0.005` | `22.1/14` | `1.003 ± 0.004` | `9.9/14` |
| 3 | `[10⁻⁴, 10⁻²]` | `1.029 ± 0.020` | `9.4/11` | `1.022 ± 0.020` | `10.2/11` |
| 3 | `[10⁻⁴, 3·10⁻²]` | `1.027 ± 0.014` | `11.8/14` | `1.009 ± 0.013` | `10.7/14` |

On `[10⁻⁴, 10⁻²]` in `d = 2`, the leading term alone gives `χ² = 61/11`, and the two-term law `χ² = 96/11`. Their total
ratios there are `0.94` and `1.09`.

Beyond `ℓ ≈ 0.03` the elder data exceed (0.2) by a few per cent, from the next terms.

**Rejected adjacent pairs.** These are adjacent pairs (the saddle ascends to the maximum) that are not elder pairs. They
test the cusp window directly, because the fold terms cancel. A fit `aℓ^{1/4} + bℓ^{1/2} + eℓ^{3/4}` gives:
- `d = 2`: `a = 0.088 ± 0.007`, against `I^{cand} − c₁ = 0.0921`;
- `d = 3`: `a = 0.057 ± 0.013`, against `0.0724`.

A fit without the `ℓ^{1/2}` term gives `0.081 ± 0.001` and `0.062 ± 0.002`. That fit is biased: a relative `ℓ^{1/4}`
correction is visible in `d ≥ 2`. In `d = 1` there was none (#214 §6.2).

## 4. The SIDE24 correction sizes (`d = 3`, Gaussian kernel)

| `ℓ` | `−5.071ℓ^{7/12}` | `+3.859ℓ^{2/3}` | sum (three-term relative correction) |
|---|---|---|---|
| `10⁻⁵` | `−0.0061` | `+0.0018` | `−0.0044` |
| `10⁻⁴` | `−0.0235` | `+0.0083` | `−0.0152` |
| `10⁻³` | `−0.0902` | `+0.0386` | `−0.0516` |
| `10⁻²` | `−0.3455` | `+0.1791` | `−0.1663` |

The combined correction is `1%` at `ℓ ≈ 4.6·10⁻⁵` and `10%` at `ℓ ≈ 3.6·10⁻³`. V3 edit E15's sizes describe the
`ℓ^{1/4}` term only (#214 caution); with this note the manuscript can quote both. Both are formal for `d = 3`.

## 5. Sources (exact identities in `SOURCES.json`)

Merged:
- [R] `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (`247b3ecf`): the kernel, the pin vector and its target;
- `reviews/side24_v1_coefficient_claude_20260929/RESULTS.json`: `c_{2,∞}`;
- `coefficients/side24_v1/ENCLOSURE.json`: `c_{3,24} = c_{3,∞}(1 + O(e^{−288}))`.

Cited, unmerged:
- #207 `frontiers/cusp_second_order_20261001/PROOF.md`: `c₁`, the cusp loss, Theorem CU′;
- #214 `frontiers/d1_third_order_law_20261001/PROOF.md`: `B₂` and its proof in `d = 1`;
- #191 `frontiers/remainder_vanishing_20260930/PROOF.md`: the even contact expansion.

## 6. Controls

`c2_check.py` uses the standard library only. Its output is `RESULTS.json`, byte-identical under `-O`. Mutants M1–M4 exit 1,
and an unknown label exits 2. The run takes about 25 seconds.
- **T1–T2** `d = 1`: `c = C₀` to `10⁻¹⁰` and `c₂ = 2B₂` to `10⁻⁸`, against #214's closed forms, for the Gaussian kernel and
  the mixture.
- **T3** `d = 2`: `c = c_{2,∞}` to `10⁻¹⁰`; `c₂` from two `r`-sets agreeing to `10⁻⁸`.
- **T4** `d = 3`: `c = c_{3,∞}` to `10⁻⁸`; `c₂` stable to `10⁻⁶` between two grids.
- **T5** no `r¹` term: the ratio to `A₀` is below `10⁻⁶` at six test points, while the `r²` ratio is `O(1)`.
- **T6** the overlap term (0.1) in `d = 2`: at four heights, `A₂(b, 0)` from the `r`-fit equals `−12π₀E₀[Y²1{A<0} | b]`
  to `10⁻⁶`. The latter is computed directly from the jets, with `Y = f_xxxx a/12 − γ²/4`. In `d = 1` the same identity
  holds to `2·10⁻¹²` (development check).
- **Mutants:**
  - M1 drops the finite-part subtraction;
  - M2 takes the `r³` coefficient for `A₂`;
  - M3 uses a wrong sphere measure in `d = 2`;
  - M4 drops the analytic tail.

What the controls do not test: the formal derivation of §1 in `d ≥ 2`, and the Monte Carlo of §3, which is exploration.

## 7. Review slices

- **A** §0 and §1: the definition of `c₂`, and whether the composite-expansion argument is right. In particular, that the
  overlap term is exactly (0.1).
- **B** §2.1–§2.3: the pinned structure, the `O(r³)` indicator replacement, and the `d = 1` identity with #214.
- **C** §2.4 and `c2_check.py`: the numerics and their convergence.
- **D** §3–§4: the Monte Carlo method and its interpretation (exploration).
