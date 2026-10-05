# The one-dimensional lifetime and crest-to-trough laws on the line: Theorems 1D and 1D⁺ for stationary processes on `ℝ`

Object: CL-D1-LINE-20261004-v1.2.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 4 October 2026. Dylan Roy — delegated AI
work.
**v1.1 (before any nonauthor pickup; v1 was `f34ffd7`).** The hypothesis loses v1's (R3a), the decay
`|ρ^{(j)}(x)| ≤ C(1 + |x|)^{−1}` for `j ≤ 2`. (H_ℝ) is now purely spectral: (R1)–(R3) below. Lemma 4.3_ℝ no longer makes
the cross-covariances between the samples and the pins small. Conditioning on the three pin observations lowers at most
three eigenvalues of the samples' covariance (interlacing), and the density bound loses three powers of `ε`, which the
growing number of samples absorbs. The decay needed elsewhere, `ρ, ρ', ρ'' → 0`, follows from (R1) by the Riemann–Lebesgue
lemma (Lemma 4.1_ℝ). Lemma F_ℝ now uses at least `23` cells; its rate, and the theorem, are unchanged.
**v1.2 (wording only; no statement, hypothesis, constant, rate or control changes).** v1.1 (`2635309`) passed all
four nonauthor slice reads with no required amendment: A (Grok Bot agent 8), B (Grok Bot agent 1; OpenAI / GPT-6
Astra Pro supplemental), C (OpenAI/Codex C137) and D (Grok Bot agent 3). v1.2 carries their optional notes. Slice B's
notes coincide in part with an author-side check of §2 (same provider; not review evidence). §2 now says that the
global-maximum alternative is excluded under `Q` also for [1D⁺] Lemma W and the fields `f_φ` of Proposition M, defines
`t₁`, fixes the domain of a Taylor remainder, and lists the inputs and the replaced circle-only parts in full. §0–§1
state the evenness of `s`, the smooth version and the window-determined marks. §5 records the void cap `t₀ ≤ L/4`
and names the source of each term of (5.1). The dependency labels are narrowed (header, §7). `SOURCES.json` records
Math- #210 as merged.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph,
STATUS, PROOF_INDEX, prize or Boolean change. Same GitHub account as every lane; zero organizational independence.
Before submission, two clean-context same-family referees (Anthropic Claude subagents) read the draft: slices A–B and
C–D of §9. Both returned ACCEPT WITH MINOR FIXES, with no major finding. Their fixes are applied here, and a delta check
found them fixed (`SOURCES.json`, `referee`). v1.1's new material came after that pass: Lemma 4.1_ℝ, the interlacing
form of Lemma 4.3_ℝ, and Lemma F_ℝ with `23` cells. A second delta check by the same referees returned:
- slice C ACCEPT and slice B ACCEPT;
- slices A and D ACCEPT WITH MINOR FIXES, for one sentence of §0 and the packaging. Both are applied.

**What is new.** Math- #214 proves Theorem 1D on the circle `R/LZ`, and Math- #238 sharpens it to Theorem 1D⁺ (remainder
`O(h^{3/4})`). #214 §6.4 notes that the near-pair analysis is local, and that on the line only the far bound of its
Lemma 4.3 needs a decorrelation hypothesis. This note supplies that bound, and with it the line versions of both theorems,
under the hypothesis (H_ℝ) of §0. The new ingredient is Lemma F_ℝ (§4): a pair that is *banded* (its process stays between
the two endpoint values) over a long interval is unlikely, with an exponential rate in the length. The proof uses three
standard tools:
- Ingham's inequality, for a lower bound on all but at most three eigen-directions of the conditional covariance of
  many well-separated derivative samples;
- Landau's inequality, on cells of fixed length;
- Gaussian concentration, for the number of cells where the second derivative is large.

The constants are those of #214 and #238. For the covariance `e^{−x²/2}` on `ℝ`, the crest-to-trough density per crest is
the classical object of Rice (1944/45), Cartwright–Longuet-Higgins (1956) and Lindgren (2019). It is
`f_H(h) = 0.19971814h^{−1/3} − 0.27165891h^{1/4} + 0.41725471h^{1/3} + O(h^{3/4})`.

**Dependencies (consumed; merged).**
- Math- #214, `frontiers/d1_third_order_law_20261001/PROOF.md`, blob `1591ecee`, merged at `e4ca2b3` ([1D]). Used: §0, the
  objects and constants; §1, the pair coordinates, the pinned law `Q = Q_{t,α}`, (1.2)–(1.4), Lemma 1.2, Lemma 1.3 and
  Remark 1.4; §2, Proposition 2.2; §3, Lemmas 3.1–3.3 and Corollary 3.4; §4, Lemma 4.1, Lemma 4.2 (near form), and the
  part of Lemma 4.3 on `[t_*, t₀]`; in §5, the adjacency estimate only.
- Math- #238, `frontiers/d1_sharp_remainder_20261001/PROOF.md`, blob `8dc558a7`, merged at `8404169` ([1D⁺]). Used: §0, and
  §§1–3 (Lemma E, Proposition 2.2⁺, Lemmas Φ and W, Proposition M) and the part of §4 on `(0, t_*]`; the assembly is
  redone in §5.

**External (standard).**
- Ingham's inequality: A. E. Ingham, *Some trigonometrical inequalities with applications to the theory of series*,
  Math. Z. 41 (1936) 367–379. See also R. M. Young, *An Introduction to Nonharmonic Fourier Series*, rev. ed. (2001), Ch. 4,
  §1.
- Gaussian concentration for functions that are Lipschitz along the Cameron–Martin space: Borell, Tsirelson–Ibragimov–
  Sudakov. See V. I. Bogachev, *Gaussian Measures* (1998), Theorem 4.5.7, or M. Ledoux, *The Concentration of Measure
  Phenomenon* (2001), §2.1.
- Borell–TIS and Sudakov–Fernique, as used in [1D] Lemma 4.3.
- Bulinskaya's lemma, as in [1D] Lemma 1.1.
- The two-point Kac–Rice formula with Borel marks, as in [1D] §1.
- Maruyama's theorem: a stationary Gaussian sequence whose covariance tends to `0` is mixing.

## 0. Statement

**Setting.** `f` is a centered stationary Gaussian process on `ℝ` with covariance `ρ(x) = E f(0)f(x) = ∫_ℝ e^{iωx}s(ω)dω`,
where the spectral measure has a density `s ≥ 0`. Since `f` is real, `s` is even, so (R2) below also holds on
`[−ω₂, −ω₁]`; and (R1) gives a version with `C^∞` sample paths (Bulinskaya's lemma and the window space of §1 use
`C³`). Write `λ_{2j} := (−1)^jρ^{(2j)}(0) = ∫ω^{2j}s(ω)dω`.

> **(H_ℝ)**
> - (R1) `∫(1 + |ω|)^n s(ω)dω < ∞` for every `n`.
> - (R2) There are `0 < ω₁ < ω₂` and `s₀ > 0` with `s ≥ s₀` almost everywhere on `[ω₁, ω₂]`.
> - (R3) `S₆ := ess sup_ω (1 + ω⁶)s(ω) < ∞`.

Example: `ρ(x) = e^{−x²/2}`, with `s(ω) = (2π)^{−1/2}e^{−ω²/2}` and `λ_{2j} = (2j − 1)!!`, satisfies (H_ℝ). Take `[ω₁, ω₂] = [1, 2]`,
for instance. (R1) is [1D]'s smoothness, and (R2) replaces [1D]'s positivity of every Fourier coefficient. (R3) bounds
the spectral density with the weight `1 + ω⁶`. No decay rate of `ρ` is assumed: by (R1) and the Riemann–Lebesgue lemma,
`ρ^{(j)}(x) → 0` as `|x| → ∞` for every `j`. [1D] §6.4 asks, on the line, for "uniform nondegeneracy of separated
values". Here that comes from (R2) through Ingham's inequality and interlacing for the samples (Lemma 4.3_ℝ), and from
the Riemann–Lebesgue lemma for the pins (Lemma 4.1_ℝ).

**Objects** ([1D] §0, with `T` replaced by `ℝ`). By Lemma 1.1_ℝ, almost surely `f` is a Morse function with alternating
maxima and minima and pairwise distinct critical values. By Lemma 1.5_ℝ, almost surely `f` exceeds every level on every
half-line. For a local maximum `M`, put `x₊ := inf{x > M : f(x) > f(M)}` and `x₋ := sup{x < M : f(x) > f(M)}`. These are
finite by Lemma 1.5_ℝ, `x₋ < M < x₊`, and `f(x_±) = f(M)`.
- The **crest-to-trough amplitude** is `H(M) := f(M) − f(S⁺(M))`, where `S⁺(M)` is the next critical point in the positive
  direction (a minimum).
- The **persistence lifetime** is `ℓ(M) := f(M) − d(M)`. Here `d(M) := max(m₋, m₊)`, and `m_±` is the minimum of `f` on the
  segment between `M` and `x_±`. So on `ℝ` every maximum has a finite bar.

  The minimum `m_±` is attained strictly inside the segment, at a local minimum. The point where `d(M)` is attained is
  therefore a minimum `S(M)`, `M`'s **death point**. It is unique, because the critical values are distinct.

The intensities are `Λ₊(B) := E#{M ∈ [0, 1) : H(M) ∈ B}` and `Λ(B) := E#{M ∈ [0, 1) : ℓ(M) ∈ B}`. `ν₊` and `ν` are their
canonical two-point Kac–Rice versions (1.2_ℝ)–(1.3_ℝ).

**Theorem 1D_ℝ.** Under (H_ℝ), as `h ↓ 0` and `ℓ ↓ 0`,

    ν₊(h) = (C₀/2) h^{−1/3} + (I/2) h^{1/4} + B₂ h^{1/3} + O(h^{3/4}),                        (1D_ℝ.1)
    ν(ℓ)  =  C₀ ℓ^{−1/3}   +  C₁ ℓ^{1/4}  + 2B₂ ℓ^{1/3} + O(ℓ^{3/4}),                        (1D_ℝ.2)

with the constants of [1D] §0, which are explicit functions of `λ₂, λ₄, λ₆, λ₈`:
- `C₀ = 2·72^{−1/6}Γ(7/6)(2π)^{−1/2}p₁₂σ₃^{4/3}`;
- `C₁ = −(8/21)24^{1/4}μ_{7/4}(2π)^{−1/2}p₁₂σ₄^{7/4}/σ₃`;
- `I = (3^{1/4}/2)C₁`;
- `B₂ = 2^{1/2}3^{1/3}Γ(5/6)(2π)^{−1/2}p₁₂σ₃^{2/3}·𝒬/(120λ₂λ₄D)`.

Here `D := λ₂λ₆ − λ₄²` and the other symbols are those of [1D] §0. In particular, Theorem 1D's (1D.1)–(1D.2) with
`O(h^{1/2})` hold on `ℝ`.

For `e^{−x²/2}`, the constants are `C₀ = 0.11011038`, `C₁ = −0.22760636`, `I = −0.14977341` and `B₂ = 0.11502229`. On `ℝ`
these are exact: there is no periodization correction. The rate of maxima is `(2π)^{−1}(λ₄/λ₂)^{1/2} = √3/(2π)`, so per
crest `f_H(h) = 0.19971814h^{−1/3} − 0.27165891h^{1/4} + 0.41725471h^{1/3} + O(h^{3/4})`. ([1D] §0 prints the last
coefficient as `0.41725`.) The leading constant is the one of Math- #210.

**What is not claimed.**
- No uniformity in the covariance, and no explicit constant in any `O(·)`.
- No sharpness of `3/4`, and nothing on the sign of the `h^{3/4}` coefficient ([1D⁺] §0).
- Nothing for spectral measures with a singular part, or for spectral densities that are not bounded below on an interval
  away from `0` ((R2)). For example, a spectrum on finitely many points violates Lemma 1.1_ℝ; with two points `±1`, the
  process is `A cos x + B sin x`, and `H = 2√(A² + B²)` has no `h^{−1/3}` law (#210 §3).
- Nothing for spectral densities with `(1 + ω⁶)s` unbounded ((R3)). That excludes a spectral pole at `0` (long-range
  dependence), and also spiky high-frequency tails, which (R1) alone would allow.

## 1. The process on `ℝ`

**Lemma 1.1_ℝ (nondegeneracy).** For distinct `x₁, …, x_k ∈ ℝ` and any `j₀ ≥ 0`, the Gaussian vector
`(f^{(j)}(x_i))_{i ≤ k, j ≤ j₀}` is nondegenerate. Almost surely, `f` is Morse with pairwise distinct critical values.

*Proof.* `Var Σ c_{ij}f^{(j)}(x_i) = ∫|P(ω)|²s(ω)dω` with `P(ω) := Σ_{i,j}c_{ij}(iω)^je^{iωx_i}`.
- `P` is entire. If the variance vanishes, `P = 0` almost everywhere on `[ω₁, ω₂]` by (R2), hence `P ≡ 0`.
- Writing `P(ω) = Σ_i q_i(ω)e^{iωx_i}` with polynomials `q_i`, the functions `ω^je^{iωx_i}` (distinct `x_i`) are linearly
  independent, so every `c_{ij}` vanishes.
- The Morse property and distinct critical values follow from Bulinskaya's lemma. Apply it to `(f', f'')` and to
  `(f'(x), f'(y), f(x) − f(y))` on compact subsets of `{x ≠ y}`, exactly as in [1D] Lemma 1.1, then take a countable union.
  ∎

**Lemma 1.5_ℝ (unboundedness on half-lines).** Almost surely, `sup_{[b,∞)}f = sup_{(−∞,b]}f = +∞` for every `b ∈ ℝ`.

*Proof.* `ρ(n) → 0` by the Riemann–Lebesgue lemma, since `s ∈ L¹`. So the stationary Gaussian sequence `(f(n))_{n∈ℤ}` is
mixing (Maruyama), hence ergodic. For each `c`, `P(f(0) > c) > 0`, so by Birkhoff's theorem `f(n) > c` for infinitely many
`n ≥ 0` and infinitely many `n ≤ 0`, almost surely. Intersect over `c ∈ ℕ`. ∎

**The pair coordinates and the canonical versions.** These are as in [1D] §1: the maximum at `−τ`, the other critical
point at `τ`, `t = 2τ > 0`, and `U` with the density `p_t` and the conditional law `Q = Q_{t,α}`. The coordinate change
`(f'(−τ), f'(τ), f(−τ) − f(τ)) ↦ U` has determinant `12/t⁴`. So

    (12/t⁴)p_t(α) = p_V(0, 0, h),   V := (f'(−τ), f'(τ), f(−τ) − f(τ)),                       (1.1_ℝ)

the density of `V` at `(0, 0, h)`. `σ(V) = σ(U)`, so `Q` is also the law given `V = (0, 0, h)`.

**The process under `Q`.** By Gaussian regression, under `Q` the process `f` has the law of `m_{t,h} + X`. Here
`m_{t,h} := Cov(f(·), V)Σ_VV^{−1}(0, 0, h)ᵀ`, and the residual `X := f − Cov(f(·), V)Σ_VV^{−1}V` is independent of `V`. The
entries of `Cov(f(x), V)` are `ρ'(−τ − x)`, `ρ'(τ − x)` and `ρ(−τ − x) − ρ(τ − x)`, which are bounded in `x`. So:
- `m_{t,h}` is bounded, and `X` differs from `f` by a bounded function. By Lemma 1.5_ℝ, `X` is unbounded above on every
  half-line almost surely, and so is `f` under `Q`, for every `(t, α)`.
- Off the pins, the vectors `(f'(x), f''(x))`, `(f'(x), f'(y), f(x) − f(y))` and `(f'(x), f(x) − f(±τ))` stay
  nondegenerate given `V` (Lemma 1.1_ℝ). By Bulinskaya's lemma, under `Q` the process `f` is Morse with distinct critical
  values, and `f''(±τ) ≠ 0`, almost surely.

So the objects of §0, and the marks below, are defined `Q`-almost surely for every `(t, α)`.

**The Kac–Rice representation on `ℝ`.** The marked two-point Kac–Rice formula of [1D] §1 holds on `ℝ` for pairs with
`x ∈ [0, 1)` and `y = x + t`, `t > 0`. The marks are Borel functions of `f` on a compact window around the pair, or
increasing limits of such functions. The argument is this:
- On the domain `{x ∈ [0, 1], t ∈ [ε, 1/ε]}` (the intensities use `[0, 1)`; the point `x = 1` is a null event), the pair
  law is nondegenerate (Lemma 1.1_ℝ). A mark that depends on `f`
  restricted to `[x − r, x + r]` is a Borel function on the Polish space `C²([−r, 1 + 1/ε + r])`, which also carries the
  pair's segment `[x, x + t]`. The argument of [1D] §1 ([P] §9 as repaired in [E2]) therefore applies verbatim.
- Let `ε ↓ 0`, by monotone convergence.
- The crest-to-trough mark `1{f' < 0 on (−τ, τ)}` depends on `f` on the pair's segment.
- The elder mark `𝔪 := 1{τ = S(−τ)}` is the increasing limit, as `r → ∞`, of
  `𝔪·1{x₋ and x₊ of the maximum −τ lie within distance < r of −τ}`. Each term is a Borel function of `f` on
  `[−τ − r, −τ + r]`. The limit holds `Q`-almost surely by the preceding paragraph, so monotone convergence applies on both
  sides of the formula.

Hence

    ν₊(h) := ∫₀^∞ K₊(t, h) dt,     ν(ℓ) := 2∫₀^∞ K(t, ℓ) dt,                                      (1.2_ℝ)–(1.3_ℝ)

with `K₊` and `K` the kernels (1.2)–(1.3) of [1D]. `K` is for the death point at `+t`. The death point at `−t` gives the same
kernel by the reflection `f ↦ f(−·)`, which preserves the law; this is the factor `2`. (On the circle the reflection gave
`ν = 2∫₀^{L/2}K`.)

## 2. What transfers from the circle

The following parts of [1D] and [1D⁺] concern a pair at separation `t ≤ t₀`, for a fixed small `t₀`, or hold for every
`t > 0`. They involve the pinned law `Q`, the jets at the midpoint, and suprema of derivatives over `[−2t, 2t]`:
- [1D] Lemmas 1.2–1.3 and Remark 1.4 (Lemma 1.2 and Remark 1.4 hold for every `t > 0`); §2, including Proposition 2.2;
  §3 (Lemmas 3.1–3.3 and Corollary 3.4); Lemma 4.1; the near form of Lemma 4.2; Lemma 4.3 on `[t_*, t₀]`; and, in §5,
  the adjacency estimate (the Borell–TIS bound for `{K₅ ≥ ct^{−δ}}` under `Q`, with `K₅` a supremum over `[−2t, 2t]`);
- [1D⁺] §§1–3 (Lemma E, Proposition 2.2⁺, Lemmas Φ and W, and Proposition M), and the part of §4 on `(0, t_*]`.

Their proofs use the following, all available on `ℝ`:
- the moments `λ_{2j}`;
- the nondegeneracy of finitely many derivatives at finitely many distinct points: the pins, the midpoint and the
  sample points of [1D] Lemma 4.2 (Lemma 1.1_ℝ, in place of [1D] Lemma 1.1);
- the parity split of [1D] Remark 1.4, which needs only that `ρ` is even;
- Borell–TIS and Sudakov–Fernique for suprema over compact intervals.

So they hold on `ℝ` with the same proofs. The global parts of [1D] §§0–1 are replaced in §§0–1 above:
- [1D] Lemma 1.1 (the positivity of the Fourier coefficients), by Lemma 1.1_ℝ;
- the normalization `L^{−1}`, the range `t ∈ (0, L)` and the reflection `K(t) = K(L − t)` in (1.2)–(1.3), by
  (1.2_ℝ)–(1.3_ℝ);
- the finiteness of the critical set, by its local finiteness (the Morse property, Lemma 1.1_ℝ); and the exclusion of the
  global maximum, by Lemma 1.5_ℝ and its form under `Q` in §1: `Q`-almost surely, for every `(t, α)`, no global maximum
  exists and `x_±` are finite;
- the far form of [1D] Lemma 4.2 and the part of [1D] Lemma 4.3 on `[t₀, L)` with its co-banded bound, by Lemma 3.1_ℝ
  and Lemma F_ℝ; and the circle assemblies ([1D] §5 apart from the adjacency estimate, [1D⁺] §4 on `[t_*, L)`), by §5.

Three points need a word.
- [1D] Lemma 3.3 holds on `ℝ`, and its global-maximum alternative does not occur: under `Q` every maximum of `f` has a
  finite bar (§1). The same holds for [1D⁺] Lemma W, read with "a function `f_φ` on `ℝ`", and for its use in [1D⁺]
  Proposition M on the fields `f_φ = f + (φ − φ_G)m(ψ − ψ(τ))`, for every `φ` given `ω`. There
  `ψ(x) = Cov_Q(f_e(x), E₁)/v₁` is built from `ρ′(τ ± x)` and `ρ″(τ ± x)`, so it is bounded by (R1), and each `f_φ`
  differs from `f` by a bounded function. So, on the `Q`-almost sure event of §1, each `f_φ` is unbounded above on both
  half-lines, and every maximum of `f_φ` has a finite bar. In particular, when both arcs fall below `−1` (the edge `J₋`
  with `μ₋(φ) ≤ 0`, or the negative case of [1D] Lemma 3.3 (R)), `𝔖` is not the death point of `𝔐`.
- In the step of [1D] Lemma 4.3 on `[t₁, t₀]`, `sup|f''|` is the supremum over the band `[−τ, τ]`; Landau's inequality on
  the band needs nothing more. (On `ℝ`, `sup_ℝ|f''| = ∞` almost surely.) With this reading, the near part of [1D] Lemma 4.3
  gives

      ∫_{t_*}^{t₀} K^{band}(t, h) dt = O(h^{3/4}).                                                (2.1)

  Here `K^{band}(t, h) := (12/t⁴)p_t(α)E_Q[|f''(−τ)f''(τ)|1{banded}]`, and "banded" means `f(τ) ≤ f ≤ f(−τ)` on `[−τ, τ]`.
  Also `t_* := (12h)^{1/(5−δ)}` with `δ ∈ (0, 1/10]`, as in [1D] Proposition 2.2; §5 takes `δ = 1/10`. Here
  `t₁ := h^{1/10}` is [1D]'s notation (its Lemma 4.3), unrelated to `T₁` of Lemma 4.1_ℝ. The same band reading applies
  to the Taylor remainders `τ^K sup|f^{(K+1)}|` in the proof of [1D] Lemma 1.3: the supremum is over `[−τ, τ]`.
- Beyond the list above, [1D⁺] uses the following:
  - `E_Q(K^e)² ≤ C` with `K^e = sup_{[−2t,2t]}|f_e^{(6)}|`, in (Φ.1) and, through `K^⊥`, in (Φ.3) and Proposition M;
  - the invertibility of `Cov(U₁, U₃)` for `t > 0` in (Φ.2), now by Lemma 1.1_ℝ;
  - uniform Gaussian tails of `K̃^o` and `K^⊥` in (Φ.3);
  - `E_Q[O(3/2)⁴] ≤ C` in Proposition M.

  The first, third and fourth are suprema or moments over `[−2t, 2t]`, bounded by Sudakov–Fernique and Borell–TIS on
  a compact interval. The second also gives `sup_{t≤t₀}sup_{[−2t,2t]}|μ_t^{(5)}| < ∞` in (Φ.2), through the continuity
  of `(t, x) ↦ μ_t^{(5)}(x)` (by (R1)) and the nondegenerate limit of [1D] Lemma 1.3.

Two facts from [1D] §4 are used in the following form.
- An adjacent typed pair is banded: `f' < 0` on `(−τ, τ)`, so `f` is monotone there.
- An elder pair is banded on the segment between `M` and its death point. If `S(M)` lies on the positive side, the segment
  `[M, S(M)]` lies in `[M, x₊]`, so `f ≤ f(M)` on it. Also `f ≥ f(S(M))` there, since `S(M)` minimizes `f` on `[M, x₊]`.
  With the maximum at `−τ` and the death point at `τ`, this is the banded event. On the circle, [1D] also needed a
  co-banded case (the complementary arc); on `ℝ` there is none.

## 3. The compact middle range

**Lemma 3.1_ℝ.** For every fixed `T₀ ≥ t₀`, `∫_{t₀}^{T₀}K^{band}(t, h)dt = O(h²log(1/h))`.

*Proof.* This is the far part of [1D] Lemma 4.3, on the compact range `t ∈ [t₀, T₀]`, with two changes:
- `sup_T|f''|` is replaced by `B := max(sup_{[−τ,τ]}|f''|, 1)`;
- on `ℝ` there is no complementary arc.

The steps are as follows.
- **The interior points.** Choose four points `y_i` in `[−τ, τ]` at mutual distances `≥ t₀/8` and at distance `≥ t₀/4`
  from both pins.
- **The density bound.** The conditional density of `(f'(y_i))_{i ≤ 4}` given `(V, f''(−τ), f''(τ))` is at most `C`,
  uniformly on this compact configuration set. The conditional covariance is nondegenerate by Lemma 1.1_ℝ, applied to the
  distinct points `±τ, y_i`, and its determinant is continuous in the configuration. So it is bounded below on the compact
  set.
- **Landau's inequality on the band.** Lemma 4.2_ℝ on `Δ = [y_i − t₀/16, y_i + t₀/16] ⊂ [−τ, τ]` gives
  `|f'(y_i)| ≤ (hB)^{1/2} + 16h/t₀ ≤ 2(hB)^{1/2}` on the banded event, for small `h`.
- **Truncation of `B`.** Under `Q`, `f''` has mean bounded by `Cα ≤ C` and centered part `f''_c` with
  `E_Q sup_{[−τ,τ]}|f''_c| ≤ E sup_{[0,T₀]}|f''|` (Sudakov–Fernique). Borell–TIS gives `B ≤ b_h := C(log(1/h))^{1/2}`
  outside an event of `Q`-probability `O(h^{20})`.
- **The kernel bound.** On `{banded} ∩ {B ≤ b_h}`, every `|f'(y_i)|` is at most `ε_h := 2(hb_h)^{1/2}`. Given
  `(V, f''(−τ), f''(τ))`, this has probability at most `Cε_h⁴ = Ch²log(1/h)`. On `{B > b_h}` use Cauchy–Schwarz. Hence
  `E_Q[|f''(−τ)f''(τ)|1{banded}] ≤ Ch²log(1/h)·E_Q|f''(−τ)f''(τ)| + O(h^{10})`. By (1.1_ℝ),
  `(12/t⁴)p_t(α) = p_V(0, 0, h) ≤ C` on `[t₀, T₀]`, again by Lemma 1.1_ℝ and compactness.

Integrating over the compact range gives the claim. ∎

## 4. The far band on `ℝ`

Fix `w := 4π/(ω₂ − ω₁)`. A **cell** is an interval of length `w`.

**Lemma 4.1_ℝ (pins far apart).** `Σ_VV` has diagonal `(λ₂, λ₂, 2(ρ(0) − ρ(t)))` and off-diagonal entries `−ρ''(t)`,
`ρ'(t)`, `ρ'(t)`. It is invertible for every `t > 0` (Lemma 1.1_ℝ). There is `T₁` such that
`λ_min(Σ_VV) ≥ c_V := min(λ₂, ρ(0))/2` for `t ≥ T₁`.

*Proof.* `Cov(f'(y), f'(z)) = −ρ''(z − y)` and `Cov(f'(y), f(z)) = −ρ'(z − y)` give the entries. By (R1), `s`, `ωs` and
`ω²s` are integrable, so `ρ(t)`, `ρ'(t)` and `ρ''(t)` tend to `0` (Riemann–Lebesgue). Gershgorin's theorem then gives the
bound for large `t`. ∎

**Lemma 4.2_ℝ (Landau's inequality on an interval).** Let `Δ` be a compact interval with midpoint `y` and length `|Δ| > 0`,
and `g ∈ C²(Δ)`. Put `osc := sup_Δ g − inf_Δ g` and `S := sup_Δ|g''|`. Then `|g'(y)| ≤ (osc·S)^{1/2} + 2osc/|Δ|`.

*Proof.* If `osc = 0`, `g` is constant and `g'(y) = 0`. Otherwise, for `0 < u ≤ |Δ|/2`, Taylor's formula at `y` gives
`|2ug'(y)| ≤ |g(y + u) − g(y − u)| + u²S ≤ osc + u²S`, so `|g'(y)| ≤ osc/(2u) + uS/2`.
- If `S = 0`, then `g` is affine and `|g'(y)| = osc/|Δ|`.
- If `S > 0` and `(osc/S)^{1/2} ≤ |Δ|/2`, take `u = (osc/S)^{1/2}` to get `(osc·S)^{1/2}`.
- Otherwise `S < 4osc/|Δ|²`, and `u = |Δ|/2` gives `osc/|Δ| + |Δ|S/4 < 2osc/|Δ|`.

(Checker C1.) ∎

**Lemma 4.3_ℝ (a density bound for many samples).** There is `λ_* > 0`, depending only on `s₀`, `ω₁` and `ω₂`, with the
following property. Let `t > 0`, and let `y₀ < … < y_{N−1}` be points of `[−τ, τ]` with `y_{i+1} − y_i ≥ w`. Then for every
`G ⊂ {0, …, N − 1}` with `|G| ≥ 6` and every `ε > 0`,

    P_Q(|f'(y_i)| ≤ ε for all i ∈ G) ≤ (ε(2e/λ_*)^{1/2})^{|G|−3}.                                (4.1)

*Proof.* Let `Y := (f'(y_i))_{i∈G}`, `k := |G|` and `m := k − 3`.

- **Ingham's inequality.** For real `c_i`,

      Var(Σ_G c_if'(y_i)) = ∫|Σ_G c_i(iω)e^{iωy_i}|²s(ω)dω ≥ s₀ω₁²∫_{ω₁}^{ω₂}|Σ_G c_ie^{iωy_i}|²dω ≥ s₀ω₁²c_I Σc_i².

  The constant `c_I > 0` depends only on `w` and `ω₂ − ω₁`, and the last step is Ingham's inequality. The exponents `y_i`
  are `w`-separated, and the interval has length `ω₂ − ω₁ = 4π/w > 2π/w`. A translation of the interval multiplies each
  term by `e^{iω_cy_i}`, a unit factor. So `λ_min(Σ_YY) ≥ λ_* := s₀ω₁²c_I`.
- **Conditioning on the pins costs at most three dimensions.** Under `Q`, `Y` is Gaussian, given `V = (0, 0, h)`, with
  covariance `Σ := Σ_YY − P`, where `P := Σ_YVΣ_VV^{−1}Σ_VY` is positive semidefinite of rank at most `3`. Order
  eigenvalues increasingly. For `j ≥ 4`, every `j`-dimensional subspace meets `ker P` in dimension at least `j − 3`, and on
  `ker P` the quadratic forms of `Σ` and `Σ_YY` agree. By the Courant–Fischer theorem, `μ_j(Σ) ≥ μ_{j−3}(Σ_YY) ≥ λ_*`
  (checker C6). So at most three eigenvalues of `Σ` are below `λ_*`. No decay of the cross-covariances `Σ_YV` is needed.
- **Projection.** Let the rows of the `m × k` matrix `B` be orthonormal eigenvectors of `Σ` for `μ₄, …, μ_k`. Then `BY` is
  Gaussian on `ℝ^m` with covariance `diag(μ₄, …, μ_k) ⪰ λ_*·Id`, so its density is at most `(2πλ_*)^{−m/2}`; its mean
  does not matter. If `|f'(y_i)| ≤ ε` for all `i ∈ G`, then `‖BY‖₂ ≤ ‖Y‖₂ ≤ εk^{1/2}`. The ball of that radius in `ℝ^m`
  has volume `π^{m/2}(εk^{1/2})^m/Γ(m/2 + 1) ≤ (2πek/m)^{m/2}ε^m`, by `Γ(x + 1) ≥ ∫_x^∞ u^xe^{−u}du ≥ x^xe^{−x}` (checker C6
  spot-checks it for `3 ≤ m ≤ 300`).
  Since `k ≥ 6`, `k/m ≤ 2`. Multiplying gives `(ekε²/(mλ_*))^{m/2} ≤ (2eε²/λ_*)^{m/2}`, which is (4.1). ∎

**Lemma 4.4_ℝ (few rough cells).** Let `t ≥ T₁`, and let `J₀, …, J_{N−1}` be cells in `[−τ, τ]` with disjoint interiors.
Put `S_i := sup_{J_i}|f''|` and `n_R := #{i : S_i > R}`. There are `σ_F`, `R₀` and `h₀`, depending only on `ρ` and `w` (not
on `N`, `t` or the cells), such that for `R ≥ R₀` and `h ≤ h₀`,

    P_Q(n_R ≥ N/2) ≤ exp(−NR²/(8σ_F²)).                                                          (4.2)

*Proof.* Under `Q`, `f = m + X`, with `m := m_{t,h}` and `X` the residual of §1 (whose law is the same under `Q`).
- `|m''| ≤ C_mh`. The entries of `Cov(f''(x), V)` are values of `ρ''` and `ρ'''`, bounded by (R1), and
  `λ_min(Σ_VV) ≥ c_V` for `t ≥ T₁` (Lemma 4.1_ℝ).
- `X` is centered. Let `H` be the reproducing kernel Hilbert space of `f`, i.e. its Cameron–Martin space. The Cameron–Martin
  space of `X` is the orthogonal complement in `H` of the three representers of `V`, with the `H`-norm.
- Let `Ū` be the smallest interval containing the cells. The law of `X` restricted to `Ū` is a centered Gaussian measure on
  the separable Banach space `C²(Ū)`. Its Cameron–Martin space consists of the restrictions `g|_Ū` of the elements `g` of
  the space above, with the quotient norm `inf{‖g‖_H : g in that space, g|_Ū = k}`.

Put `F(k) := (Σ_i sup_{J_i}|k''|²)^{1/2}` for `k ∈ C²(Ū)`, a continuous seminorm.

**`F` is Lipschitz along the Cameron–Martin space.** Every `g ∈ H` has the form `g(x) = ∫e^{iωx}φ(ω)s(ω)dω` with
`‖g‖_H² = ∫|φ|²s`. By Plancherel, `∫_ℝ|g''|² = 2π∫ω⁴|φ|²s² ≤ 2πS₆‖g‖_H²`, and likewise for `g'''`, with `S₆` from (R3).
On each cell, `sup_{J_i}|u|² ≤ 2(w^{−1}∫_{J_i}|u|² + w∫_{J_i}|u'|²)` (checker C4); apply this to `u = g''`. The cells have
disjoint interiors, so

    F(g)² ≤ 2(w^{−1}∫|g''|² + w∫|g'''|²) ≤ 4πS₆(w^{−1} + w)‖g‖_H² =: σ_F²‖g‖_H².

`F(g)` depends only on `g|_Ū`. Taking the infimum over the `g` in the Cameron–Martin space of `X` with `g|_Ū = k` gives
`F(k) ≤ σ_F‖k‖` on the Cameron–Martin space of `X|_Ū`.
Also `|F(x + k) − F(x)| ≤ F(k)`, `F` being a seminorm.

**Concentration.** The Gaussian concentration inequality for such functions gives
`P(F(X) ≥ EF(X) + u) ≤ e^{−u²/(2σ_F²)}` for `u > 0`.

**The mean of `F(X)`.**
- On each cell, `sup|X''|` is the supremum of the centered process `(x, ±) ↦ ±X''(x)` on `J_i × {±1}`.
- Conditioning does not increase the variance of a linear functional. So the increments of this process have variances at
  most those of `(x, ±) ↦ ±f''(x)`. Sudakov–Fernique and stationarity give `E sup_{J_i}|X''| ≤ μ_w := E sup_{[0,w]}|f''|`.
- Borell–TIS (variance `≤ λ₄`, both tails) gives `Var sup_{J_i}|X''| ≤ ∫₀^∞ 2u·2e^{−u²/(2λ₄)}du = 4λ₄`. So
  `E sup_{J_i}|X''|² ≤ μ_w² + 4λ₄ ≤ M₂ := (μ_w + 2λ₄^{1/2})²`.
- Hence `EF(X) ≤ (EF(X)²)^{1/2} ≤ (NM₂)^{1/2}`.

**Conclusion.** On `{n_R ≥ N/2}`, `F(f) ≥ (N/2)^{1/2}R`, and `F(f) ≤ F(m) + F(X) ≤ N^{1/2}C_mh + F(X)`. So
`F(X) − EF(X) ≥ N^{1/2}(R/√2 − C_mh − M₂^{1/2})`.

Let `R ≥ R₀ := 5(M₂^{1/2} + 1)` and `h ≤ h₀ := 1/C_m`. Then `C_mh + M₂^{1/2} ≤ R/5`. Also `1/√2 − 1/5 ≥ 1/2`, because
`(1/2 + 1/5)² = 49/100 ≤ 1/2` (checker C6). With `4` in place of `5` the step fails, since `(1/2 + 1/4)² > 1/2`.

So `F(X) − EF(X) ≥ N^{1/2}R/2`, and concentration with `u = N^{1/2}R/2` gives (4.2). ∎

**Lemma F_ℝ (the far band).** There is `T₀ ≥ t₀` such that `∫_{T₀}^∞ K^{band}(t, h)dt = O(h²)` as `h ↓ 0`.

*Proof.* Take `T₀ := max(T₁, t₀, 24w)`. For `t ≥ T₀`, put `N := ⌊(t − 2w)/w⌋ + 1 ≥ 23` and `y_i := −τ + w + iw` for
`0 ≤ i < N`; then `y_{N−1} ≤ τ − w`. Let `J_i` be the cell centred at `y_i`. These cells lie in `[−τ, τ]` and have
disjoint interiors.

*Banded pairs have small slopes at good cells.* On the banded event, `osc_{J_i}f ≤ h`. Lemma 4.2_ℝ gives
`|f'(y_i)| ≤ (hS_i)^{1/2} + 2h/w`.

*The good-cell bound.* Let `R := A(log(1/h))^{1/2}`, with `A` fixed and `A² ≥ 2σ_F²`.
- Take `h ≤ h₀` so small that `R ≥ R₀`.
- Put `ε := (hR)^{1/2} + 2h/w` and `q := 4ε(2e/λ_*)^{1/2}`. Then `q ≤ C_qh^{1/2}(log(1/h))^{1/4}`. Take `h` so small that
  also `q ≤ 1/16` and `h^{A²/(16σ_F²)} ≤ 1/2`.
- On `{n_R < N/2}`, more than `N/2` cells have `S_i ≤ R`, and on the banded event `|f'(y_i)| ≤ ε` at each of them. So some
  `G ⊂ {0, …, N − 1}` with `|G| = ⌈N/2⌉ ≥ 12` has `|f'(y_i)| ≤ ε` for all `i ∈ G`. There are at most `2^N` such `G`.
- Use (4.1) for each `G`, and (4.2) for `{n_R ≥ N/2}`. Since `ε(2e/λ_*)^{1/2} = q/4 ≤ 1`, the exponent `⌈N/2⌉ − 3` may be
  lowered to `N/2 − 3`:

      P_Q(banded) ≤ exp(−NR²/(8σ_F²)) + 2^N(q/4)^{N/2−3} = exp(−NR²/(8σ_F²)) + 64q^{N/2−3}.

*The kernel.* By (1.1_ℝ), Cauchy–Schwarz and `(x + y)^{1/2} ≤ x^{1/2} + y^{1/2}`,

    K^{band}(t, h) ≤ p_V(0, 0, h)·(E_Q[f''(−τ)²f''(τ)²])^{1/2}·P_Q(banded)^{1/2} ≤ C_K(exp(−NR²/(16σ_F²)) + 8q^{N/4−3/2}).

The constant `C_K` is uniform in `t ≥ T₀`, for two reasons. First, `p_V(0, 0, h) ≤ (2πc_V)^{−3/2}` (Lemma 4.1_ℝ). Second,
under `Q` each `f''(±τ)` is Gaussian with variance `≤ λ₄` and mean `m''(±τ)`, which is at most `C_mh`.

*Summation.* The set `{t : N(t) = n}` has length `≤ w`, and `exp(−nR²/(16σ_F²)) = h^{nA²/(16σ_F²)}`. The two geometric
series have ratios `h^{A²/(16σ_F²)} ≤ 1/2` and `q^{1/4} ≤ 1/2`, so each is at most twice its first term:

    ∫_{T₀}^∞ K^{band} dt ≤ C_Kw Σ_{n≥23}(h^{nA²/(16σ_F²)} + 8q^{n/4−3/2}) ≤ 2C_Kw(h^{23A²/(16σ_F²)} + 8q^{17/4}).

Here `23A²/(16σ_F²) ≥ 23/8` and `q^{17/4} ≤ C_q^{17/4}h^{17/8}(log(1/h))^{17/16}`. So the integral is
`O(h^{17/8}(log(1/h))^{17/16})`, which is `O(h²)`. (Checker C5 checks this exponent bookkeeping and the geometric steps at
sample values.) ∎

## 5. Proof of Theorem 1D_ℝ

Fix `δ = 1/10` and `t₀` as in [1D⁺] §4 (small enough for [1D] Lemma 4.3), and `T₀ ≥ t₀` as in Lemma F_ℝ. On `ℝ` the cap
`t₀ ≤ L/4`, which [1D⁺] §4 inherits from the far form of [1D] Lemma 4.2, is void: that form is not used. The three
terms of (5.1) come from (2.1) on `[t_*, t₀]`, Lemma 3.1_ℝ on `[t₀, T₀]` and Lemma F_ℝ on `[T₀, ∞)`:

    ∫_{t_*}^∞ K^{band}(t, h) dt = O(h^{3/4}) + O(h²log(1/h)) + O(h²) = O(h^{3/4}).                (5.1)

**(1D_ℝ.1).** Write `ν₊ = ∫₀^{t_*}K₊ + ∫_{t_*}^∞K₊`.
- On `(0, t_*]` the argument is [1D⁺] §4 verbatim. `K₊ = K₁^{sign} − (12/t⁴)p_tE_Q[(−f''(−τ))⁺f''(τ)⁺1{not adjacent}]`.
  Non-adjacency forces `K₅ ≥ ct^{−δ}` ([1D] Lemma 3.1), so the correction integrates to `O(h^k)` for every `k`.
  Then [1D⁺] Proposition 2.2⁺ with `θ = 1` gives the three terms with remainder `O(h^{3/4})`.
- On `[t_*, ∞)`, an adjacent pair is banded, so `K₊ ≤ K^{band}`, and (5.1) applies.

**(1D_ℝ.2).** Write `ν = 2∫₀^∞K`, by (1.3_ℝ).
- On `(0, t_*]`, as in [1D⁺] §4: `K = K_{1/3}^{sign} + (K − K_{1/3}^{sign})`. [1D⁺] Proposition 2.2⁺ with `θ = 1/3` gives the
  expansion with `I_{1/3} = C₁`, and [1D⁺] Proposition M bounds the rest by `O(h^{3/4})`.
- On `[t_*, ∞)`, an elder pair is banded (§2), so `K ≤ K^{band}`, and (5.1) applies.

Doubling gives (1D_ℝ.2). The constants are those of [1D] §0. They depend only on `λ₂, λ₄, λ₆, λ₈`, through `p₁₂`, `σ₃`, `σ₄`,
`D` and `𝒬`. For `e^{−x²/2}` their values, and the per-crest constants, are given in §0. ∎

## 6. Remarks

1. **What changed from the circle.** On `T`, [1D] Lemma 4.3's far part used four interior points, and compactness of the
   circle gave a bounded density and a bounded `sup_T|f''|`.
   - On `ℝ` the band can be arbitrarily long, so a fixed number of points does not make the kernel integrable in `t`. The
     number of cells must grow with `t`.
   - Two uniformities then replace compactness. Ingham's inequality gives a covariance lower bound that does not degrade
     with the number of samples, and conditioning on the three pin observations lowers at most three eigenvalues
     (Lemma 4.3_ℝ). Gaussian concentration controls the number of cells where `f''` is large (Lemma 4.4_ℝ); a union bound
     over `N` cells would cost a factor `N`, which is not integrable.
   - The price is (R2)–(R3): an absolutely continuous spectrum, with a density bounded below on an interval away from `0`
     and bounded with the weight `1 + ω⁶`. No decay rate of the covariance is needed.
2. **The hypotheses.**
   - (R2) is used twice: in Lemma 1.1_ℝ, and through Ingham's inequality in Lemma 4.3_ℝ. In the latter, it is used for
     `f'`, whose spectral density `ω²s(ω)` vanishes at `0`, hence `ω₁ > 0`.
   - For the Gaussian covariance, the samples' covariance is also directly diagonally dominant at spacings `≥ 2`, with
     `λ_min ≥ 1/6` uniformly in `N` (checker C2). Ingham's inequality is needed for covariances without such explicit
     decay. At spacing `1` the Gaussian row sum is `1 − 5.3·10⁻⁷`: the infinite Toeplitz matrix is then almost singular,
     and diagonal dominance gives no usable bound.
   - (R3) bounds the Lipschitz constant `σ_F`.
   - The decorrelation used is qualitative: `ρ, ρ', ρ'' → 0` (Riemann–Lebesgue), in Lemma 1.5_ℝ and Lemma 4.1_ℝ. v1
     assumed `|ρ^{(j)}(x)| ≤ C(1 + |x|)^{−1}` for `j ≤ 2`, to make the cross-covariances `Σ_YV` small; the interlacing step
     of Lemma 4.3_ℝ makes that unnecessary.
3. **Relation to the classical literature (#210).**
   - For `ρ = e^{−x²/2}`, (1D_ℝ.1) per crest is the small-amplitude law of crest-to-trough heights of a stationary
     Gaussian process on the line. Its leading constant `0.19971814` is #210's `C`.
   - #210's two-point check integrates the sign kernel up to `t ≤ 1.5`, without the adjacency mark. The non-adjacent pairs
     it includes contribute `O(1)` there, as #210 v1.3 §3 derives from [1D] Lemmas 1.3 and 3.1. #210 §3 notes that #214
     claims nothing on the line. Once this note is reviewed, that sentence can cite Theorem 1D_ℝ instead.
4. **Exploration.** None was needed. The statement is a transfer, and the new lemmas are deterministic or standard
   estimates. The checker tests the elementary inequalities that the proof uses (§8).

## 7. Sources (exact identities in `SOURCES.json`)

| Tag | Path | Role |
|---|---|---|
| [1D] | `frontiers/d1_third_order_law_20261001/PROOF.md` (blob `1591ecee`, merged `e4ca2b3`) | consumed: the parts listed in §2 (§§0–4, and the adjacency estimate of §5) |
| [1D⁺] | `frontiers/d1_sharp_remainder_20261001/PROOF.md` (blob `8dc558a7`, merged `8404169`) | consumed: §§0–3, and §4 on `(0, t_*]` |
| [P], [E2] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`), `reviews/d1_section9_borel_repair_20260925/REPAIR.md` (blob `fe9b9ce4`) | the marked Kac–Rice convention, through [1D] §1 — cited |
| #210 | `reviews/literature_classical_neighbors_20261001/ADDENDUM.md` (Math- #210, merged at `0cdc19f`; blob `b289c7cd`, as read at head `213dd9e`) | comparison only (Remark 3) |

## 8. Exact controls (`line_check.py`; standard library; exact rationals except C3; byte-identical under `-O`)

- **C1 Landau on an interval (Lemma 4.2_ℝ).**
  - Random rational polynomials of degree `≤ 4` are tested on intervals of six lengths. So are S-shaped cubics
    `As(1 − (2s/|Δ|)²)` plus small terms, which have `|g'(y)| > 2osc/|Δ|` (counted with an upper bound for `osc`).
  - `S = sup|g''|` is computed exactly: `g''` is quadratic, so its maximum is at an endpoint or the vertex.
  - `osc` is bounded from below by the values at a grid and at bisection-refined zeros of `g'`. The inequality's right
    side increases in `osc`, so a lower bound suffices.
  - The inequality is checked in exact arithmetic, and so is the Taylor step `|2ug'(y)| ≤ |g(y + u) − g(y − u)| + u²S`.
  - The nearly affine family `g = s + εs²` on a unit interval shows that the term `2osc/|Δ|` is needed: there
    `|g'(y)| = 1` while `(osc·S)^{1/2} = (2ε)^{1/2}`.
- **C2 Gaussian covariance: diagonal dominance.** The correlation `−ρ''(kw) = (1 − k²w²)e^{−k²w²/2}` of `f'` samples at
  spacing `w`, with `λ₂ = 1`.
  - The off-diagonal row sum `2Σ_{k≥1}|1 − k²w²|e^{−k²w²/2}` is bounded above with `e^{−x} ≤ 1/Σ_{j≤40}x^j/j!` and a
    geometric tail bound.
  - The upper bounds are `0.82207665`, `0.17774502` and `0.01006388` at `w = 2, 3, 4`, each `≤ 5/6`.
  - Each term decreases in `w` once `kw ≥ 2 > √3`, because `((x² − 1)e^{−x²/2})' = x(3 − x²)e^{−x²/2}`.
  - So for every spacing `w ≥ 2` and every `N`, `λ_min ≥ 1/6`.
- **C3 The constants.** `C₀, C₁, I, B₂` from `λ_{2j} = (2j − 1)!!` and [1D] §0's closed forms, against the printed values.
  The per-crest coefficients are checked against `0.19971814`, `−0.27165891` and `0.41725471`.
  - Exact: `𝒬 = 1620`, `𝒬/(120λ₂λ₄D) = 3/4`, and [1D]'s decomposition of `𝒬` at the Gaussian moments.
  - Floating point: the two printed forms of `C₁` agree.
- **C4 The cell Sobolev bound.** `sup_J|u|² ≤ 2(w^{−1}∫_J|u|² + w∫_J|u'|²)` is checked for random rational polynomials `u` of
  degree `≤ 5`, on intervals of five lengths `w`. The integrals are exact, and the supremum is bounded above on a grid with
  a derivative margin.
  - Proof of the bound: `u(x)² ≤ u(z)² + 2∫_J|uu'|`; average over `z ∈ J` and use `2ab ≤ a²/w + wb²`. This gives
    `sup|u|² ≤ 2w^{−1}∫u² + w∫u'²`.
  - The constant `1` is false: `u = 1 + (s/w)²/2` on `[0, w]` has `sup|u|² = 9/4 > 103/60 = w^{−1}∫u² + w∫u'²`. The sharp
    constant is `coth 1 = 1.313…`.
- **C5 The summation of Lemma F_ℝ**, at sample values.
  - `Σ_{n=23}^{M}x^n = (x^{23} − x^{M+1})/(1 − x)`, and `x^{23}/(1 − x) ≤ 2x^{23}`, for `x ∈ {1/2, 1/3, 1/10, 1/1000}`.
  - `2^N(q/4)^{N/2−3} = 64q^{N/2−3}`, the step to the union bound's form.
  - `N ≥ 23` and `y_{N−1} ≤ τ − w` when `t ≥ 24w`, at sample values.
  - The final exponents: `23A²/(16σ_F²) ≥ 23/8 > 2` for `A² ≥ 2σ_F²`, and `(23 − 6)/4·(1/2) = 17/8` with log power `17/16`.
- **C6 The ingredients of Lemmas 4.3_ℝ–4.4_ℝ.**
  - Interlacing: for random rational `A = λ·Id + MMᵀ` and `P = Σ_{s≤r}u_su_sᵀ` with `r ≤ 3`, an exact `LDLᵀ` count
    (Sylvester's law of inertia) shows that `A − P − λ·Id` has at most `r` negative eigenvalues. A deterministic family
    attains `r`.
  - Stirling: `Γ(m/2 + 1) ≥ (m/(2e))^{m/2}` for `3 ≤ m ≤ 300`, with rational bounds for `e` and `√π`; and `k/(k − 3) ≤ 2`
    for `k ≥ 6`.
  - The threshold `R₀ = 5(M₂^{1/2} + 1)`: `(1/2 + 1/5)² ≤ 1/2`.

**Mutants** (`--mutant M`) exit 1, each in its own control:
- M1 drops the `2osc/|Δ|` term (C1);
- M2 uses the Sobolev constant `1` in place of `2` (C4);
- M3 takes the spacing `w = 1` in place of `2` (C2);
- M4 drops the factor `2` of `C₀` (C3);
- M5 takes `23A²/(32σ_F²)` (C5);
- M6 takes `R₀ = 4(M₂^{1/2} + 1)` (C6);
- M7 allows only `r − 1` small eigenvalues after a rank-`r` conditioning (C6).

An unknown label exits 2.

## 9. Review slices

- **A §§0–1.** The objects on `ℝ`; Lemma 1.1_ℝ, Lemma 1.5_ℝ, the process under `Q`, and the Kac–Rice representation on `ℝ`
  with the two marks.
- **B §2.** The claim that the listed parts of [1D] and [1D⁺] are local. Check each for any use of compactness of `T`.
- **C §§3–4.** Lemma 3.1_ℝ; Lemmas 4.1_ℝ–4.4_ℝ (the pin covariance, Landau, Ingham with interlacing, Gaussian
  concentration); Lemma F_ℝ.
- **D §5 and the controls.** The assembly, the constants, `line_check.py`.
