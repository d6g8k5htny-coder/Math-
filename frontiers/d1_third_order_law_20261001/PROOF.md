# The one-dimensional lifetime and crest-to-trough laws to third order: `C₀ℓ^{−1/3} + C₁ℓ^{1/4} + 2B₂ℓ^{1/3} + O(ℓ^{1/2})`

Object: CL-D1-THIRD-ORDER-20261001-v1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 1 October 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph,
STATUS, PROOF_INDEX, prize or Boolean change. Same GitHub account as every lane; zero organizational independence.
**Dependencies: none.** The proof is self-contained (Gaussian conditioning, the two-point Kac–Rice formula, Taylor's
formula, Markov's polynomial inequality). Cited for comparison only: Math- #207 (Theorem CU, `d ≥ 2`; its (CU.2) at
`d = 1` is this note's `C₁`, §6.1), Math- #210 (the `d = 1` remark whose leading constant this note proves), and the
merged literature reconnaissance `reviews/literature_lifetime_law_recon_20260929/RECONNAISSANCE.md`.

## 0. Statement

**Setting.** `T = R/LZ` (`L > 0`) and `f` a centered stationary Gaussian process on `T` with covariance
`ρ(x) = E f(0)f(x)`, under the hypothesis

> **(H)** `ρ ∈ C^∞(T)` and `ρ̂(n) := L^{−1}∫_T ρ(x)e^{−2πinx/L}dx > 0` for every `n ∈ Z`.

Example: the periodization `Σ_k e^{−(x+kL)²/2}` of the Gaussian kernel (`ρ̂(n) = (2π)^{1/2}L^{−1}e^{−2π²n²/L²}`), the
one-dimensional analogue of the SIDE24 torus field. Write `λ_{2j} := (−1)^jρ^{(2j)}(0)`, `a_j := f^{(j)}(0)`,

    D := λ₂λ₆ − λ₄²,   σ₃² := D/λ₂ = Var(a₃ | a₁),   σ₄² := λ₈ − λ₆²/λ₄ = Var(a₄ | a₂),
    p₁₂ := (2π)^{−1}(λ₂λ₄)^{−1/2} = density of (a₁, a₂) at 0,   p₃(α) := (2πσ₃²)^{−1/2}e^{−α²/(2σ₃²)}.

**Objects.** By (H) and Lemma 1.1, almost surely `f` is a Morse function with finitely many critical points, alternating
maxima and minima, with pairwise distinct critical values. For a local maximum `M`:

- the **crest-to-trough amplitude** `H(M) := f(M) − f(S⁺(M))`, `S⁺(M)` the next critical point in the positive
  direction (a minimum);
- if `M` is not the global maximum, the **persistence lifetime** `ℓ(M) := f(M) − d(M)` of the superlevel filtration,
  `d(M) := sup_γ min f∘γ` over paths from `M` to points higher than `f(M)` (the elder rule; in one dimension
  `d(M) = max(m₋, m₊)`, `m_±` the minimum of `f` along the arc from `M` in direction `±` up to the first point higher
  than `f(M)`). The point where `d(M)` is attained is a minimum `S(M)`, `M`'s **death point** (elder partner).

The intensities `Λ₊(B) := L^{−1}E#{M : H(M) ∈ B}` and `Λ(B) := L^{−1}E#{M not global : ℓ(M) ∈ B}` are absolutely
continuous; `ν₊`, `ν` denote their **canonical (two-point Kac–Rice) versions** (1.2)–(1.3).

**Theorem D1.** Under (H), as `h ↓ 0` and `ℓ ↓ 0`,

    ν₊(h) = (C₀/2) h^{−1/3} + (I/2) h^{1/4} + B₂ h^{1/3} + O(h^{1/2}),                        (D1.1)
    ν(ℓ)  =  C₀ ℓ^{−1/3}   +  C₁ ℓ^{1/4}  + 2B₂ ℓ^{1/3} + O(ℓ^{1/2}),                        (D1.2)

with, writing `μ_q := E|Z|^q` for a standard normal `Z` (`μ_{7/4} = 2^{7/8}Γ(11/8)π^{−1/2}`),

    C₀ = 2·72^{−1/6} Γ(7/6) (2π)^{−1/2} p₁₂ σ₃^{4/3},
    C₁ = −(8/21)·24^{1/4} μ_{7/4} (2π)^{−1/2} p₁₂ σ₄^{7/4}/σ₃  = −(2^{25/8}/7) 3^{−3/4} π^{−2} Γ(11/8) σ₄^{7/4} σ₃^{−1}(λ₂λ₄)^{−1/2},
    I  = (3^{1/4}/2) C₁,
    B₂ = 2^{1/2}3^{1/3} Γ(5/6) (2π)^{−1/2} p₁₂ σ₃^{2/3} · 𝒬/(120λ₂λ₄D),   𝒬 := 4λ₂²λ₄λ₈ + 26λ₂λ₄²λ₆ − 5λ₂²λ₆² − 25λ₄⁴.

So `C₁ < 0 < C₀`; `I − C₁ = (1 − 3^{1/4}/2)|C₁| > 0` is the density coefficient of adjacent max/min pairs that are
not elder pairs, `2ν₊(ℓ) − ν(ℓ) = (I − C₁)ℓ^{1/4} + O(ℓ^{1/2})`.

For the Gaussian kernel (`λ_{2j} = (2j − 1)!!`; the periodization changes them by `O(L^{2j}e^{−L²/2})`, invisible
below for `L ≥ 10`): `C₀ = 0.11011038`, `C₁ = −0.22760636`, `I = −0.14977341`, `B₂ = 0.11502229`, `𝒬/(120λ₂λ₄D) = 3/4`. Per
crest (dividing `ν₊` by the rate `(2π)^{−1}(λ₄/λ₂)^{1/2}` of maxima) the crest-to-trough density is
`f_H(h) = 0.19971814 h^{−1/3} − 0.27165891 h^{1/4} + 0.41725 h^{1/3} + O(h^{1/2})`; its leading constant is #210's.

**Mechanism.** A short bar is a fold: a maximum `M` and an adjacent minimum `S` at separation `t` with gap
`h ≈ αt³/12`, `α ≈ f'''`. Integrating the fold law over `t` gives `C₀h^{−1/3}` (scale `t ≍ h^{1/3}`). At `t ≍ h^{1/4}`
the quartic jet competes with the cubic (the cusp): on that scale the pair sees the quartic ridge
`g(X) = κ[2(X + ½)²(X − 1) + 3φ(X² − ¼)²]`, `κ = h/t⁴`, `φ = f''''/(72κ)` — the case `d = 1` of #207's ridge — and the
pair is adjacent iff `|φ| < 1`, an elder pair iff `|φ| < 1/3`; the fold law overcounts there, and integrating the
deficit over the scale gives the `h^{1/4}` terms. The `h^{1/3}` term collects the `τ²`-corrections of the pinned law at
the fold scale and the finite part of the cusp integrand's `τ`-tail (§2).

**What is not claimed.** No statement on `R` (§6.4); no uniformity in the covariance; no explicit constant in the
`O(·)`; the `O(h^{1/2})` is not claimed sharp (the proof gives `O(h^{0.57})` for (D1.1); the numerics of §6.2 suggest
the next terms are `O(h^{3/4})`).

## 1. Two-point representation and the pinned law

**Lemma 1.1 (nondegeneracy).** For distinct `x₁, …, x_k ∈ T` and any `J`, the Gaussian vector
`(f^{(j)}(x_i))_{i ≤ k, j ≤ J}` is nondegenerate. Hence `f` is a.s. Morse with distinct critical values.

*Proof.* `f(x) = Σ_n ρ̂(n)^{1/2}ξ_n e^{2πinx/L}` with independent standard complex Gaussians (`ξ_{−n} = ξ̄_n`). A linear
combination `Σ c_{ij}f^{(j)}(x_i)` has variance `Σ_n ρ̂(n)|P(n)|²`, `P(n) := Σ_{i,j}c_{ij}(2πin/L)^j z_i^n`,
`z_i := e^{2πix_i/L}` distinct; it vanishes iff `P(n) = 0` for all `n ∈ Z` (as all `ρ̂(n) > 0`), i.e. iff all the
polynomial coefficients vanish (the sequences `n^j z_i^n` are linearly independent: their generating functions have
poles of distinct locations). The Morse property and the distinctness of critical values then follow from Bulinskaya's
lemma applied to `(f', f'')` and to `(f'(x), f'(y), f(x) − f(y))` on `{x ≠ y}`. ∎

**The pair coordinates.** By stationarity put the maximum at `−τ` and the other critical point at `τ`, `t := 2τ ∈ (0, L)`
the distance from `−τ` to `τ` in the positive direction. Define

    U₁ := (f'(−τ) + f'(τ))/2,   U₂ := (f'(τ) − f'(−τ))/t,   U₃ := (6/t²)(f'(−τ) + f'(τ)) + 12(f(−τ) − f(τ))/t³.

On the pin event `{f'(±τ) = 0, f(−τ) − f(τ) = h}` one has `U = (0, 0, α)`, `α := 12h/t³`, and the linear map
`(f'(−τ), f'(τ), f(−τ) − f(τ)) ↦ U` has determinant `12/t⁴`. Let `p_t(α)` be the density of `U` at `(0, 0, α)` and
`Q = Q_{t,α}` the conditional law of `f` given `U = (0, 0, α)`; set `κ := h/t⁴ = α/(12t)`.

**The canonical versions.** The marked two-point Kac–Rice formula (e.g. Azaïs–Wschebor 2009, Ch. 6, for zeros of
`(f'(x), f'(y))` on `{x ≠ y}` with a bounded Borel weight; the marked form is the one-dimensional case of the argument
of [P] §9 as repaired in [E2]) gives, for bounded Borel `ψ ≥ 0` and Borel marks `𝔪`,
`L^{−1}E Σ_{(x,y)} 𝔪 ψ(f(x) − f(y)) = ∫ψ(h)∫₀^L (12/t⁴)p_t(α)E_Q[(−f''(−τ))⁺f''(τ)⁺𝔪]dt dh`, the sum over ordered pairs
`(x, y)` of a local maximum `x` and a local minimum `y` (the weight `(−f''(−τ))⁺f''(τ)⁺` vanishes on the other types), with
`y` at distance `t ∈ (0, L)` from `x` in the positive direction. With `𝔪 = 1{f' < 0 on (−τ, τ)}` (then `τ = S⁺(−τ)`) and
`𝔪 = 1{τ = S(−τ)}`:

    ν₊(h) := ∫₀^L K₊(t, h) dt,   K₊(t, h) := (12/t⁴) p_t(α) E_Q[(−f''(−τ))⁺ f''(τ)⁺ 1{f' < 0 on (−τ, τ)}],      (1.2)
    ν(ℓ)  := ∫₀^L K(t, ℓ) dt,    K(t, ℓ)  := (12/t⁴) p_t(α) E_Q[(−f''(−τ))⁺ f''(τ)⁺ 1{τ = S(−τ)}].              (1.3)

Reflection `x ↦ −x` preserves the law and maps a pair at positive distance `t` to one at `L − t`, so `K(t, ℓ) = K(L − t, ℓ)`
and `ν(ℓ) = 2∫₀^{L/2}K(t, ℓ)dt`.

**Lemma 1.2 (reflection structure).** Under `Q_{t,α}`: `E_Q f''(±τ) = ±c(t)α` for a function `c(t)`; with
`E₁ := (f''(τ) + f''(−τ))/2` and `E₂ := (f''(τ) − f''(−τ))/2 − c(t)α`, the pair `(E₁, E₂)` is centered Gaussian with a
law independent of `α`, `Cov(E₁, E₂) = 0`, variances `v₁(t), v₂(t)`, and with `m := c(t)α`

    −f''(−τ) = m − E₁ + E₂,   f''(τ) = m + E₁ + E₂,   (−f''(−τ))⁺f''(τ)⁺ = ((m + E₂)² − E₁²)⁺ 1{m + E₂ > 0}.     (1.4)

*Proof.* Let `R f := f(−·)`; `Rf` has the law of `f`. Then `U(Rf) = (−U₁, U₂, −U₃)(f)` and `(Rf)''(±τ) = f''(∓τ)`.
Conditional means are linear in the conditioning value: `E_Q f''(±τ) = m_±α`. By invariance,
`m₊α = E[(Rf)''(τ) | U(Rf) = (0,0,α)] = E[f''(−τ) | U(f) = (0, 0, −α)] = −m₋α`; so `m₊ = −m₋ =: c(t)`, and `E₁` is
centered. Conditional covariances do not depend on the conditioning value, and the same invariance gives
`Var_Q f''(τ) = Var_Q f''(−τ)`, i.e. `Cov(E₁, E₂) = 0`. The last identity: for `m + E₂ > 0` the product of the two
factors is `(m + E₂)² − E₁²`, positive iff `m + E₂ > |E₁|`; if `m + E₂ ≤ 0` the factors have nonpositive sum. ∎

**Lemma 1.3 (expansions).** As `τ ↓ 0` (none of the first five quantities depends on `α`),

    c(t) = τ(1 + c₂τ² + O(τ⁴)),                c₂ = −(λ₂λ₈ − λ₄λ₆)/(15D),
    det Cov(U) = λ₄D(1 + d₂τ² + O(τ⁴)),          d₂ = (8λ₄²λ₆ − 3λ₂λ₄λ₈ − 5λ₂λ₆²)/(15λ₄D),
    [Cov(U)^{−1}]₃₃ = σ₃^{−2}(1 + q₂τ² + O(τ⁴)),  q₂ = (λ₂²λ₈ − 6λ₂λ₄λ₆ + 5λ₄³)/(5λ₂D),
    v₁(t) = (τ⁴σ₄²/9)(1 + O(τ²)),               v₂(t) = (τ⁶/225)(λ₁₀ − (λ₆³ − 2λ₄λ₆λ₈ + λ₂λ₈²)/D)(1 + O(τ²)),

and `p_t(α) = (2π)^{−3/2}(det Cov U)^{−1/2}exp(−α²[Cov(U)^{−1}]₃₃/2)`. In particular
`p_t(α) = p₁₂p₃(α)(1 + τ²u(α) + O(τ⁴(1 + α⁴)))` for `α ≤ τ^{−1}`, `u(α) := −d₂/2 − q₂α²/(2σ₃²)`, and
`p_t(α) ≤ Ce^{−α²/(4σ₃²)}` for all `α` and `τ ≤ τ₀`. Each quantity is an even function of `τ` (`c` odd).

*Proof.* Taylor's formula at `0` (all `a_j`, remainders bounded by `τ^K sup|f^{(K+1)}|`) gives

    U₁ = a₁ + a₃τ²/2 + a₅τ⁴/24 + …,   U₂ = a₂ + a₄τ²/6 + a₆τ⁴/120 + …,   U₃ = a₃ + a₅τ²/10 + a₇τ⁴/280 + …,
    (f''(τ) − f''(−τ))/2 = τ(U₃ + a₅τ²/15 + a₇τ⁴/210 + …),   E₁ = U₂ + a₄τ²/3 + a₆τ⁴/30 + …,

(the coefficient of `a₁` in `U₃` cancels: `(3/τ²)a₁ − (3/τ³)a₁τ = 0`), with `E a_ia_j = (−1)^{(i−j)/2}λ_{i+j}` for `i ≡ j`
mod 2 and `0` otherwise. Odd and even jets are independent, so `{U₁, U₃, (f''(τ) − f''(−τ))/2}` is independent of
`{U₂, E₁}`; `Cov(U)` is block diagonal. Then (i) `c(t)α = E[(f''(τ) − f''(−τ))/2 | U₁ = 0, U₃ = α] = τ(α + (τ²/15)E[a₅ |
U₁ = 0, U₃ = α] + O(τ⁴α))` and `E[a₅ | a₁ = 0, a₃ = α] = α(λ₄λ₆ − λ₂λ₈)/D`; (ii) `Var U₁ = λ₂ − λ₄τ² + O(τ⁴)`,
`Var U₃ = λ₆ − λ₈τ²/5 + O(τ⁴)`, `Cov(U₁, U₃) = −λ₄ + (3/5)λ₆τ² + O(τ⁴)`, so `det Cov(U₁, U₃) = D − (τ²/5)(λ₂λ₈ − λ₄λ₆)
+ O(τ⁴)`, `[Cov U^{−1}]₃₃ = Var U₁/det Cov(U₁, U₃)` and `Var U₂ = λ₄ − λ₆τ²/3 + O(τ⁴)`, which give `q₂` and `d₂`; (iii)
`v₁ = Var(E₁ | U₂) = (τ⁴/9)Var(a₄ | a₂)(1 + O(τ²))`; (iv) `E₂ = τ³(a₅ − E[a₅ | U₁, U₃])/15 + O(τ⁵)`, whence `v₂`. Evenness:
`U` is invariant under `τ ↦ −τ` (which exchanges the pins) and `(f''(τ) − f''(−τ))/2` changes sign. The bounds on
`p_t` follow from `Cov U → Cov(a₁, a₂, a₃)` (nondegenerate). ∎

(Checker C4 verifies every coefficient above exactly, as Laurent series with rational coefficients computed from the
covariance itself — not through the jets — for two kernels.)

**Remark 1.4 (parity split).** Put `f_e(x) := (f(x) + f(−x))/2` and `f_o(x) := (f(x) − f(−x))/2`. Since `ρ` is even,
`Cov(f_e(x), f_o(y)) = 0`, so the Gaussian processes `f_e` and `f_o` are independent. `U₁ = f_o'(τ)`,
`U₃ = (12/t²)f_o'(τ) − (24/t³)f_o(τ)` and `(f''(τ) − f''(−τ))/2 = f_o''(τ)` are functionals of `f_o`, while
`U₂ = 2f_e'(τ)/t` and `E₁ = f_e''(τ)` are functionals of `f_e`. Hence under `Q` the processes `f_e` and `f_o` remain
independent, and `E₁` is independent of `f_o`.

## 2. The sign kernels and their asymptotics

For `θ ∈ {1, 1/3}` define the **sign kernels** (explicit functions of `(t, h)`; `m = c(t)α`)

    K_θ^{sign}(t, h) := (12/t⁴) p_t(α) G_θ,   G₁ := E((m + E₂)² − E₁²)⁺1{m + E₂ > 0},   G_{1/3} := E((m + E₂)² − E₁²)⁺1{m + E₂ > 0}1{|E₁| < m/3},

the expectations over independent `E₁ ~ N(0, v₁)`, `E₂ ~ N(0, v₂)`. By (1.4), `K₁^{sign}` is the two-point density of
(maximum, minimum) pairs with gap `h` *without* the adjacency mark; `K_{1/3}^{sign}` adds the window `|φ_G| < 1/3`,
`φ_G := E₁/m`, which §3 shows is the elder rule at the pair scale. For `Z` standard normal and `s ≥ 0` put

    γ_θ(s) := E[(s² − Z²)1{|Z| < θs}] = s² − ζ_θ(s),   ζ_θ(s) := E[Z²1{|Z| < θs}] + s²P(|Z| ≥ θs),

so `0 ≤ ζ_θ(s) ≤ C min(1, s²)` and `|1 − ζ_θ(s)| ≤ C(1 + s²)e^{−θ²s²/2}`; `ζ₁(s) = E min(Z², s²)`.

**Lemma 2.1 (Mellin integrals).** `∫₀^∞ ζ_θ(s)s^{−5/4}ds = k_θμ_{7/4}` with `k_θ = 4θ^{1/4} + (4/7)θ^{−7/4}`:
`k₁ = 32/7`, `k_{1/3} = (64/7)3^{−1/4}`; hence `k₁/k_{1/3} = 3^{1/4}/2`.

*Proof.* Fubini: for fixed `z`, `∫₀^∞(z²1{|z| < θs} + s²1{|z| ≥ θs})s^{−5/4}ds = z²∫_{|z|/θ}^∞ s^{−5/4}ds +
∫₀^{|z|/θ}s^{3/4}ds = |z|^{7/4}(4θ^{1/4} + (4/7)θ^{−7/4})`. ∎

**Proposition 2.2.** Fix `δ ∈ (0, 1/10]` and put `t_* := (12h)^{1/(5 − δ)}`, so that `t ≤ t_*` iff `α ≥ t^{2−δ}`. Then

    ∫₀^{t_*} K_θ^{sign}(t, h) dt = (C₀/2) h^{−1/3} + (I_θ/2) h^{1/4} + B₂ h^{1/3} + O(h^{0.57}),   I₁ := I,  I_{1/3} := C₁.

*Proof.* **(a) The `E₂`-correction.** Put `g_θ(m, v₁) := E(m² − E₁²)⁺1{|E₁| < θm}`. For fixed `a := |E₁|` the map
`e ↦ (m + e − a)⁺(m + e + a)` is convex (it vanishes for `e ≤ a − m` and equals `(m + e)² − a²` beyond, with right
derivative `2a ≥ 0` at the kink), and `E₂` is centered and independent of `E₁`; hence
`0 ≤ G_θ − g_θ ≤ v₂ + 2E[|E₁||E₂|1{||E₁| − m| ≤ |E₂|}]`. In the straddle term, on `{|E₂| ≤ m/2}` one has
`|E₁| ∈ [m/2, 3m/2]`, where the density of `|E₁|` is `≤ Cv₁^{−1/2}e^{−s²/8}` (`s := m v₁^{−1/2}`); the complement has
`E[|E₁||E₂|1{|E₂| > m/2}] ≤ C(v₁v₂)^{1/2}e^{−m²/(8v₂)}`, and `m²/v₂ ≍ α²/τ⁴ ≥ t^{−2δ}` on `{t ≤ t_*}`. Hence
`0 ≤ G_θ − g_θ ≤ C(v₂ + m v₂ v₁^{−1/2}e^{−s²/8}) + O(t^{N})` for every `N`. With `v₁ ≍ τ⁴`, `v₂ ≍ τ⁶`, `m ≍ τα`,
`s ≍ α/t`: the error kernel is `≤ C p_t(α)(t² + αt e^{−cα²/t²}) ≤ C t²` (as `xe^{−cx²}` is bounded), and
`∫₀^{t_*}Ct²dt = O(t_*³) = O(h^{3/(5−δ)})`.

**(b) Scaling.** `g_θ(m, v₁) = v₁γ_θ(s)` with `s := m v₁^{−1/2}`, so `(12/t⁴)p_t g_θ = (12/t⁴)p_t m² − (12/t⁴)p_t v₁ζ_θ(s)`.

**(c) The fold part.** By Lemma 1.3, `(12/t⁴)p_t m² = (3α²/t²)p₁₂p₃(α)[1 + τ²(u(α) + 2c₂) + O(τ⁴(1 + α⁴))]` for
`α ≤ τ^{−1}` (the complement, `t < (6h)^{1/2}`, contributes `O(e^{−c/h})` to this and to every term below, since there
`α ≥ τ^{−1} ≥ ch^{−1/2}` and `p_t(α) ≤ Ce^{−α²/(4σ₃²)}`). Substituting `α = 12h/t³`,
`dt = (1/3)(12h)^{1/3}α^{−4/3}dα`, `τ² = (12h/α)^{2/3}/4`:

    ∫₀^∞ (3α²/t²)p₁₂p₃(α) dt = p₁₂(12h)^{−1/3}∫₀^∞ α^{4/3}p₃(α)dα = (C₀/2)h^{−1/3},
    ∫₀^∞ (3α²/t²)p₁₂p₃(α)τ²(u(α) + 2c₂) dt = (1/4)p₁₂(12h)^{1/3}∫₀^∞ α^{2/3}p₃(α)(u(α) + 2c₂)dα =: B₂^{(1)}h^{1/3},

the `τ⁴`-term gives `O(h)`, and the part `t > t_*` of the first integral is `O(h²t_*^{−7}) = O(h^{0.57})`.

**(d) The cusp part.** For `α ≤ τ^{−1}`, `(12/t⁴)p_t v₁ζ_θ(s) = (σ₄²/12)p₁₂p₃(α)ζ_θ(s₀)(1 + ε)` with `s₀ := 3α/(τσ₄)`
and `|ε| ≤ Cτ²(1 + α²)`: by Lemma 1.3, `(12/t⁴)v₁ = (σ₄²/12)(1 + O(τ²))`, `p_t = p₁₂p₃(α)(1 + O(τ²(1 + α²)))` and
`s = s₀(1 + O(τ²))`, while `|ζ_θ'(s)| ≤ C min(s, e^{−θ²s²/4})` and `ζ_θ(s₀) ≥ c min(1, s₀²)`. Note `s₀ = 72h/(σ₄t⁴)`. Split `p₃(α) = p₃(0) + (p₃(α) − p₃(0))`:

- `p₃(0)∫₀^∞ζ_θ(s₀(t))dt = p₃(0)(72h/σ₄)^{1/4}(1/4)∫₀^∞ζ_θ(s)s^{−5/4}ds = p₃(0)(72h/σ₄)^{1/4}k_θμ_{7/4}/4` (Lemma 2.1);
  with the prefactor `−σ₄²p₁₂/12` this is `(I_θ/2)h^{1/4}`:
  `I_θ/2 = −(σ₄²/48)(72/σ₄)^{1/4}k_θμ_{7/4}p₁₂p₃(0)`, i.e. `I = −(4/21)72^{1/4}…`, `C₁ = −(8/21)24^{1/4}μ_{7/4}(2π)^{−1/2}p₁₂σ₄^{7/4}/σ₃`.
- `∫₀^∞(p₃(α) − p₃(0))ζ_θ(s₀)dt = ∫₀^∞(p₃(α) − p₃(0))dt − ∫₀^∞(p₃(α) − p₃(0))(1 − ζ_θ(s₀))dt`. The first equals
  `(1/3)(12h)^{1/3}∫₀^∞(p₃(α) − p₃(0))α^{−4/3}dα` (convergent at both ends); with the prefactor this is
  `B₂^{(2)}h^{1/3}`, `B₂^{(2)} := −(σ₄²p₁₂/36)12^{1/3}∫₀^∞(p₃(α) − p₃(0))α^{−4/3}dα > 0`. The second is `O(h^{3/4})`:
  `|p₃(α) − p₃(0)| ≤ C min(1, α²)` and `|1 − ζ_θ(s₀)| ≤ C(1 + s₀²)e^{−θ²s₀²/2}`; on `{s₀ ≤ 1}` = `{t ≥ ct_c}`,
  `t_c := h^{1/4}`, use `α² = 144h²t^{−6}`; on `{s₀ ≥ 1}` substitute `t = (72h/(σ₄s₀))^{1/4}`.
- The error `ε`: on `{t ≤ t_c}` it is `≤ C∫₀^{t_c}τ²dt`, on `{t ≥ t_c}` use `ζ_θ(s₀) ≤ Cs₀² = Ch²t^{−8}`; both `O(h^{3/4})`.
- The part `t > t_*`: `ζ_θ(s₀) ≤ Cs₀²`, so `O(h²t_*^{−7})`.

**(e) Closed forms.** `∫₀^∞α^{q}p₃(α)dα = σ₃^q 2^{(q−1)/2}Γ((q + 1)/2)(2π)^{−1/2}` (`q > −1`) gives `C₀`. Since
`Γ(11/6) = (5/6)Γ(5/6)`, `∫₀^∞α^{8/3}p₃ = (5/3)σ₃²∫₀^∞α^{2/3}p₃`, so `B₂^{(1)} = (1/4)·12^{1/3}p₁₂M(2c₂ − d₂/2 − 5q₂/6)`,
`M := ∫₀^∞α^{2/3}p₃ = 2^{−1/6}Γ(5/6)(2π)^{−1/2}σ₃^{2/3}`; and `∫₀^∞(e^{−x²/2} − 1)x^{−4/3}dx = 2^{−7/6}Γ(−1/6) =
−6·2^{−7/6}Γ(5/6)` gives `B₂^{(2)} = 12^{1/3}p₁₂M·σ₄²/(12σ₃²)`. Then

    B₂ := B₂^{(1)} + B₂^{(2)} = 12^{1/3}p₁₂M[(2c₂ − d₂/2 − 5q₂/6)/4 + σ₄²/(12σ₃²)] = 12^{1/3}p₁₂M·𝒬/(120λ₂λ₄D),

the last equality being the polynomial identities `30λ₂λ₄D(2c₂ − d₂/2 − 5q₂/6) = −6λ₂²λ₄λ₈ + 26λ₂λ₄²λ₆ + 5λ₂²λ₆² −
25λ₄⁴` and `120λ₂λ₄D·σ₄²/(12σ₃²) = 10λ₂²(λ₄λ₈ − λ₆²)`, whose sum is `𝒬` (checker C5). Collecting (a)–(d) proves the
proposition. ∎

## 3. Adjacency and the elder rule at the pair scale

Write `K₅ := sup_{[−2t, 2t]}(|f^{(5)}| + |f^{(6)}|)`.

**Lemma 3.1 (Rolle).** If `f'(±τ) = 0` and `f'` has two further zeros in `(−τ, τ)`, then `|U₃| ≤ 5τ²K₅`.

*Proof.* `f''''` vanishes at some `ξ ∈ (−τ, τ)` and `f'''` at two points, so `|f'''| ≤ t²K₅` on `[−τ, τ]`, in particular
`|a₃| ≤ 4τ²K₅`; and `|U₃ − a₃| ≤ (3/(2τ²))(2τ⁴K₅/24) + (3/(2τ³))(2τ⁵K₅/120) = (3/20)τ²K₅`. ∎

**Lemma 3.2 (the window field; #207 Theorem CU.1 at `d = 1`).** Let `f(−τ) = b`, `f(τ) = b − h`, `f'(±τ) = 0`,
`𝔉(X) := [f(tX) − b]/h` and `g(X) := 2(X + ½)²(X − 1) + 3φ(X² − ¼)²` with `φ := f''''(0)t⁴/(72h)`. With
`K^o := sup_{[−2t,2t]}|f_o^{(5)}|` and `K^e := sup_{[−2t,2t]}|f_e^{(6)}|` (Remark 1.4),
`‖𝔉 − g‖_{C²([−2, 2])} ≤ C(tK^o + t²K^e)/κ`.

*Proof.* As in #207 (CU.1) with no transverse variable, divided by `κ`, keeping track of parity. The even pins
`f_e'(τ) = 0` and `f_e(τ) = b − h/2` involve only even jets and even remainders (of order 6 for `f_e`); the odd pins
`f_o'(τ) = 0` and `f_o(τ) = h/2` only odd jets and odd remainders (of order 5). They give `ϑ₂ = −(t²/24)f₄ + O(K^et⁴)`,
`ϑ₀ − b = (−κ/2 + f₄/384)t⁴ + O(K^et⁶)`, `ϑ₃ = 12κt + O(K^ot²)` and `ϑ₁ = −(3/2)κt³ + O(K^ot⁴)`, and `t^{−4}` times the
degree-4 Taylor polynomial is `κg`. The Taylor remainder is `O(K^o|x|⁵ + K^e|x|⁶)`. After division by `h = κt⁴`, each
correction and its two `X`-derivatives are `O((tK^o + t²K^e)/κ)` on `[−2, 2]`. ∎

The model has `g(−½) = 0`, `g(½) = −1`, `g'(X) = 6(X + ½)(X − ½)(1 + 2φX)`, the third critical point `X₃ = −1/(2φ)`, and

    g(X) = (X + ½)²[2(X − 1) + 3φ(X − ½)²],      g(X) + 1 = (X − ½)²[2(X + 1) + 3φ(X + ½)²],
    g(X₃) = (φ − 1)³(3φ + 1)/(16φ³),               g(X₃) + 1 = (φ + 1)³(3φ − 1)/(16φ³).                          (3.1)

**Lemma 3.3 (the window decides, with margins).** Let `η ∈ (0, 1/4]`, `F ∈ C²([−2, 2])` with `F(−½) = 0`, `F(½) = −1`,
`F'(±½) = 0`, `F''(−½) < 0 < F''(½)`, and `‖F − g‖_{C²([−2,2])} ≤ ε ≤ c₀η` (`c₀` absolute). Let `𝔐, 𝔖` be the points
`−½, ½` of the rescaled field `F = 𝔉`. Then:
(E) if `|φ| ≤ 1/3 − η`, `𝔖` is `𝔐`'s death point;
(R) if `|φ| ≥ 1/3 + η`, `𝔖` is not `𝔐`'s death point. (Typing forces `|φ| < 1 + ε/6`, since `g''(∓½) = ∓6(1 ∓ φ)`.)

*Proof.* (E) From (3.1), for `|φ| ≤ 1/3`: the bracket `2(X − 1) + 3φ(X − ½)²` is at most `−1` on `[−3/2, −½]` (convex or
increasing in `X`, value `−5 + 12φ ≤ −1` at `−3/2` and `−3 + 3φ ≤ −2` at `−½`), so `g ≤ −(X + ½)²` there and
`g(−3/2) = −5 + 12φ ≤ −1 − 12η` when `φ ≤ 1/3 − η` (and `≤ −5` when `φ ≤ 0`); and for `φ ≥ −1/3` the bracket
`2(X + 1) + 3φ(X + ½)² ≥ 2(X + 1) − (X + ½)² ≥ 1` on `[½, 3/2]`, so `g + 1 ≥ (X − ½)²` there, while
`g(3/2) = 4(1 + 3φ) ≥ 12η`. On `[−½, ½]`, `g' < 0` (as `1 + 2φX > 0`), so `g ∈ (−1, 0)` inside. With `ε` small, `F` keeps
these sign patterns: near `±½` by `F''(−½) ≤ g''(−½) + ε = −6(1 − φ) + ε < 0` and `F''(½) ≥ 6(1 + φ) − ε > 0`, away
from `±½` by the quadratic margins. Hence the arc from `𝔐` in the negative direction reaches `F(−3/2) < −1` while
`F < 0`, so `m₋ < −1`; the arc in the positive direction stays `> −1` except at `𝔖` and exceeds `0` at `3/2`, so
`m₊ = −1 = F(𝔖)`. Thus `d(𝔐) = max(m₋, m₊) = F(𝔖)`.
(R) If `1/3 + η ≤ φ < 1`: `X₃ ∈ (−3/2, −½)` is the only critical point of `g` in `[−2, −½)`, a minimum with
`g(X₃) + 1 = (φ + 1)³(3φ − 1)/(16φ³) ≥ (3φ − 1)/2 ≥ 3η/2` (as `(1 + 1/φ)³/16 ≥ 1/2` for `φ ≤ 1`), and
`g(−2) = (9/4)(−6 + 75φ/4) ≥ 9/16`; so `F > −1 + η` on `[−2, −½]` and `F(−2) > 0`: the negative arc from `𝔐` exceeds
`F(𝔐)` before reaching `−1`, `m₋ > −1 = F(𝔖)`, and `d(𝔐) ≥ m₋ > F(𝔖)`.
If `−1 < φ ≤ −1/3 − η`: `X₃ ∈ (½, 3/2)` is a maximum with `g(X₃) ≤ (3φ + 1)/2 ≤ −3η/2`, `g(2) + 1 = (9/4)(6 − 75|φ|/4) ≤
−9/16`, and `g < 0` on `(−½, 2]`; so the positive arc from `𝔐` falls below `−1` before exceeding `0`: `m₊ < −1`; and
`m₋ < −1` as in (E) (`φ < 0`). Then `d(𝔐) < F(𝔖)`.
If `1 ≤ φ < 1 + ε/6`: `g' < 0` on `[−2, −½)` (the factor `1 + 2φX` is negative there), so `g ≥ 0` on `[−2, −½]`,
`g(−2) ≥ 9/16`, and `F ≥ −ε > −1` there with `F(−2) > 0`: `m₋ > −1`. If `−1 − ε/6 < φ ≤ −1`: the bracket
`2(X + 1) + 3φ(X + ½)² ≤ 2(X + 1) − 3(X + ½)² < 0` on `(½, 2]`, so `g < −1` there and the (R) argument for `φ < 0` applies
verbatim. ∎

(Checker C3 verifies (3.1), the critical-point structure, the margins used above, and the decision itself by exact
one-dimensional persistence of the quartic for 117 rational `φ`.)

**Corollary 3.4 (the elder decision at the pair scale).** On `{t ≤ t_*}` (i.e. `α ≥ t^{2−δ}`) let `(−τ, τ)` be a typed
pair and define `φ_G := E₁/m`. Then `|φ_G − φ| ≤ C(τ²|φ| + t²K^e/κ)` and, outside the event

    𝔅 := {C(tK^o/κ + t²K^e/κ + τ²) ≥ c₀ min(||φ_G| − 1/3|, 1/4)},

`τ = S(−τ)` iff `|φ_G| < 1/3`.

*Proof.* `E₁ = f_e''(τ)` and, on `U₂ = 0`, `a₂ = −a₄τ²/6 + O(τ⁴K^e)`, so `E₁ = a₄τ²/3 + O(τ⁴K^e)`; `m = τα(1 + c₂τ² + O(τ⁴))`
(Lemma 1.3); and `φ = a₄t⁴/(72h) = a₄τ/(3α)`. So `φ_G = φ(1 − c₂τ² + O(τ⁴)) + O(τ³K^e/α)`, and `τ³/α = τ²/(24κ)`. Apply
Lemma 3.3 with `ε = C(tK^o + t²K^e)/κ` (Lemma 3.2) and `η := min(||φ| − 1/3|, 1/4)`, transported from `φ` to `φ_G` by
the first bound (the deterministic `τ²` term is why `𝔅` contains `τ²`). ∎

## 4. Thin pairs: the band lemma and the flat band

A pair at `±τ` with gap `h` is **banded** if `f(τ) ≤ f ≤ f(−τ)` on `[−τ, τ]` (the arc of length `t`), and
**co-banded** if the same holds on the complementary arc (length `L − t`). Every adjacent typed pair (crest-to-trough)
is banded (monotone). An elder pair is banded or co-banded: `f > f(S)` and `f ≤ f(M)` along the arc on which the death
value `d(M) = m_±` is attained, i.e. the arc from `M` to its death point (not necessarily the arc of length `t`).

**Lemma 4.1 (band lemma).** Let `k ≥ 4`, `t ≤ 1`, the pair banded with gap `h`, and `K := sup_{[−τ,τ]}|f^{(k+2)}|`. Then
`|a_j| ≤ C_k(h + τ^{k+2}K)τ^{−j}` for `1 ≤ j ≤ k + 1`, and `|f''(±τ)| ≤ C_k(hτ^{−2} + τ^kK)`.

*Proof.* With `P` the Taylor polynomial of `f` at `0` of degree `k + 1`, `|f − P| ≤ τ^{k+2}K/(k + 2)!` on `[−τ, τ]`, so
`|P − f(τ) − h/2| ≤ h/2 + τ^{k+2}K`; Markov's inequality for polynomials of degree `k + 1` on `[−τ, τ]` bounds
`P^{(j)}(0) = a_j`, and `f''(±τ) = P''(±τ) + O(τ^kK)`. ∎

**Lemma 4.2 (interior values).** For fixed `−1 < ξ₁ < … < ξ_N < 1` with `∫_{−1}^1 Π_{i}(ξ − ξ_i)(ξ² − 1)dξ ≠ 0`, the
conditional density under `Q_{t,α}` of `(f'(τξ_i))_{i ≤ N}` is at most `C τ^{−N(N+5)/2}` for `τ ≤ τ₀`. (Far form) For
points `y₁, …, y_N` at distance `≥ t₀/4` from both pins, the conditional density of `(f'(y_i))` and, jointly, of
`(f'(y_i), f''(±τ))` is at most `C` uniformly in `t ∈ (0, L)`.

*Proof.* `(f'(−τ), f'(τ), f(−τ) − f(τ), f'(τξ₁), …, f'(τξ_N)) = A_τ(a₁, …, a_{N+3}) + O(τ^{N+3})`, where `A_τ =
B·diag(τ^{j−1})` up to one factor `τ` in the integral row and `B` (evaluations of polynomials of degree `N + 2` at
`−1, 1, ξ_i` and the integral over `[−1, 1]`) is invertible by the stated condition; so the covariance determinant of the
full vector is `≍ τ^{(N+3)(N+2) + 2}` and that of the pin vector `≍ τ⁸` (the case `N = 0`), and the Schur complement has
determinant `≍ τ^{N(N+5)}`. Far form: for pins at distance `≥ t₀/4` (on either side) this is compactness and Lemma 1.1;
as the pins merge (`t ↓ 0` or `t ↑ L`), `U` converges to the jet `(a₁, a₂, a₃)` at the merged point, which is jointly
nondegenerate with the far values (Lemma 1.1), so the Schur complements stay bounded below. ∎

**Lemma 4.3 (thin pairs are negligible).** Let `K^{band}(t, h) := (12/t⁴)p_t(α)E_Q[|f''(−τ)f''(τ)|1{banded}]` and
`K^{co}(t, h)` the same with `1{co-banded}`. Then `∫_{t_*}^{t₀}K^{band}dt = O(h^{3/4})`, `∫_{t₀}^{L}K^{band}dt = O(h)`
and `∫_{t_*}^{L/2}K^{co}dt = O(h)`.

*Proof.* Take `k = 8`, `N = 2`. Under `Q`, `(a₄, …, a₉)` has a density bounded uniformly in `τ ≤ τ₀` and `α`
(`Cov(a₄..a₉ | U) → Cov(a₄..a₉ | a₁, a₂, a₃)`), and `K` is sub-Gaussian with mean `O(1 + α)`; decomposing `K` dyadically
and using Lemma 4.1, for `t ≤ t₁ := h^{1/10}` the kernel is `≤ C t^{−4}(h/t²)²Π_{j=4}^{9}min(1, h t^{−j}) + O(h^{10})`.
On `[t_*, h^{1/5}]` only `j = 4` is active: `≤ Ch³t^{−12}`, integral `≤ Ch³t_*^{−11} = O(h^{0.75})`; on
`[h^{1/m}, h^{1/(m+1)}]`, `5 ≤ m ≤ 9`, the bound is `h^{m−1}t^{−8−Σ_{j=4}^{m}j}`, with integral `O(h^{4/5})` for `m = 5`
and smaller beyond (the dyadic decomposition of `K` adds at most powers of `log(1/h)`, absorbed since
`3 − 11/(5 − δ) > 3/4`). For `t ∈ [t₁, t₀]`: banded with `h ≤ t^{10}` gives `|f''(±τ)| ≤ C τ⁸(1 + K)` (Lemma 4.1) and, by
Landau's inequality on the band, `|f'(τξ_i)| ≤ 2(h max(sup|f''|, 1))^{1/2}`; truncating `K` and `sup|f''|` at
`C(log(1/h))^{1/2}` (the complement has probability `O(h^{10})`), Lemma 4.2 gives
`K^{band} ≤ Ct^{−4}t^{16}·h log(1/h)·t^{−7}`, integrable, total `O(h log(1/h))`. Far: the band (resp. co-band) arc has length `≥ t₀`
(resp. `≥ L/2`); take `N = 4` points on it at distance `≥ t₀/4` from both pins, where Landau's inequality gives
`|f'(y_i)| ≤ 2(hB)^{1/2}`, `B := max(sup_T|f''|, 1)`. Condition also on `f''(±τ)` (far form of Lemma 4.2) and truncate
`B` at `C(log(1/h))^{1/2}`: the mark costs `O(h²(log(1/h))²)` uniformly, while `∫(12/t⁴)p_t(α)E_Q|f''(−τ)f''(τ)|dt` over
`[t₀, L)` (resp. `[t_*, L/2]`) is `O(h^{−1/3})` (near a merging of the pins it is the near-pair integral, `O(h^{−1/3})`). ∎

## 5. Proof of Theorem D1

**(D1.1).** Split `ν₊ = ∫₀^{t_*} + ∫_{t_*}^{t₀} + ∫_{t₀}^{L}`. On `(0, t_*]`, `K₊ = K₁^{sign} − (12/t⁴)p_tE_Q[(⋯)⁺1{not
adjacent}]` and non-adjacency forces `K₅ ≥ ct^{−δ}` (Lemma 3.1), whose `Q`-probability is `≤ exp(−ct^{−2δ})` (Borell–TIS
for the conditioned process; `α ≤ t^{−δ}/C` or `p₃(α)` is negligible); the correction is `O(h^{N})` for every `N`.
Proposition 2.2 (`θ = 1`) gives the expansion. On `[t_*, t₀]`, `K₊ ≤ K^{band}`: `O(h^{3/4})`; on `[t₀, L)`,
`K₊ ≤ K^{band}`: `O(h)` (Lemma 4.3). Total remainder `O(h^{0.57})`.

**(D1.2).** `ν = 2∫₀^{L/2}K dt`. On `(0, t_*]`, by Corollary 3.4, `K = K_{1/3}^{sign}` up to (i) the event `𝔅` and (ii)
`{K₅ ≥ ct^{−δ}}`; (ii) is `O(h^N)` as above. For (i), `𝔅` forces `|E₁| ∈ m[1/3 − x, 1/3 + x]` with
`x := C(tK^o/κ + t²K^e/κ + τ²)/c₀` (or `x ≥ 1/4`, which needs `K^o + K^e ≥ ct^{−δ}`, an `O(h^N)` event). Since
`E₁ ~ N(0, v₁)` is independent of `K^o` under `Q` (Remark 1.4), the `K^o`- and `τ²`-parts of the window have probability
`≤ C(tE[K^o]/κ + τ²)s e^{−s²/20}` (`s = m v₁^{−1/2}`), with `E_Q[K^o] ≤ C(1 + α)`. The `K^e`-part is correlated with `E₁`;
summing `min(P(K^e ≥ 2^j), C(t²2^j/κ)s e^{−s²/20})` over dyadic shells costs at most a factor `C(1 + α)(log(1/h))^{1/2}`.
The weight is `((m + E₂)² − E₁²)⁺ ≤ 2m² + 2E₂²`. Using `κ = α/(12t)`, `(12/t⁴)m² ≍ α²/t²` and `s ≍ α/t`, the misclassified
part of the kernel is `≤ C p₃(α)(1 + α)·(α²/t²)·[(t²/α)(α/t) + τ²·(α/t)]e^{−cα²/t²}·(1 + t(log(1/h))^{1/2})`, i.e.
`≤ C p₃(α)(1 + α)(α²/t)e^{−cα²/t²}(1 + t(log(1/h))^{1/2})`, plus `O(h^N)`. Over `{t ≤ h^{1/4}}` (where `α ≳ t`) its
integral is `O(h^{1/2})` after the substitution `t = (72h/(σ₄s₀))^{1/4}`; over `{t ≥ h^{1/4}}` it is
`≤ C∫_{h^{1/4}}h²t^{−7}dt = O(h^{1/2})`. Proposition 2.2 with `θ = 1/3`, doubled, gives the expansion. On `[t_*, L/2]`, an
elder pair is banded or co-banded (§4), so `K ≤ K^{band} + K^{co}` and Lemma 4.3 applies. Total remainder `O(ℓ^{1/2})`. ∎

## 6. Remarks

**6.1 The case `d = 1` of Theorem CU (#207).** (CU.2) reads `c₁ = −(192/7)2^{1/4}∫_{S^{d−1}}p_G(0)p_{V_u}(0)(2π)^{−1/2}τ_u^{−1}
E[|Y|^{7/4}|Δ|^{1/4}1{A<0} | …]dσ(u)`. At `d = 1`: `S⁰ = {±1}` with counting measure, `A` is the empty matrix (`Δ = 1`,
`1{A < 0} = 1`, `adj(A)γ = 0`), so `Y = f₄/12`, `p_Gp_V = p₁₂`, `τ_u = σ₃`, and `E|f₄/12|^{7/4} = 12^{−7/4}σ₄^{7/4}μ_{7/4}`.
The result equals `C₁` exactly: `(192/7)2^{1/4}·2·12^{−7/4} = (2^{15/4}/7)3^{−3/4}` and `(8/21)24^{1/4} = (2^{15/4}/7)3^{−3/4}`
(checker C1). Likewise `I/C₁ = 3^{1/4}/2` is (CU′.1)'s `I^{cand}/c₁`, and `I − C₁ > 0` is (CU′.2)'s rejected coefficient.
The one-dimensional window `|φ| < 1/3` is #207's elder window with no transverse fiber. The two proofs are independent:
here the pair-scale kernel is an explicit Gaussian integral and the elder rule is decided on a fixed window (§3);
#207 needs the fiber reduction, the stability proposition and a window-probability lemma in `d ≥ 2`. So this note is an
independent check of #207's normalization `(192/7)2^{1/4}` and of the loss integral, in the one dimension where
everything is explicit — not a proof of any part of #207.

**6.2 Numerical evidence (exploration, not part of the proof).**
- *Exact two-point Rice integral* (checker C6; standard library, about three seconds: Decimal for the Gaussian
  conditioning, a closed form or a split Gauss–Legendre rule for `G₁`). It evaluates
  `dev(h) := h^{1/3}∫₀^{t₀}K₁^{sign}dt/(C₀/2) − 1` for `h = 10^{−11}, …, 10^{−16}` and fits
  `dev/h^{7/12} = a + b h^{1/12} + r h^{−1/4}`; the last term is the non-adjacent sign pairs inside `t₀`, an `O(1)` part of
  `K₁^{sign}` that the adjacency mark removes from `ν₊`. Gaussian kernel (`t₀ = 0.04`): `a = −1.3602117`,
  `b = 2.0892177`, against `I/C₀ = −1.3602115`, `B₂/(C₀/2) = 2.0892180`. Mixture kernel `(e^{−x²/2} + e^{−2x²})/2`
  (`t₀ = 0.01`; `λ₂, λ₄, λ₆, λ₈ = 5/2, 51/2, 975/2, 26985/2`): `a = −1.4697391`, `b = 2.1373811`, against
  `−1.4697376`, `2.1373703`. An mpmath computation at 50–130 digits down to `h = 10^{−24}` agrees (outside the
  repository).
- *Monte Carlo of the persistence and crest-to-trough densities* (numpy; outside the repository per the standard-library
  rule; archived with the project record): exact spectral synthesis of the periodized Gaussian kernel on circles of length
  `≈ 1.05·10⁵`, total length `8.4·10⁷`, critical points by bracketed Newton on degree-6 Taylor polynomials from exact
  grid derivatives, exact one-dimensional persistence. Over `ℓ ∈ [10⁻⁵, 10⁻²]` the ratio of the empirical `ν` to the
  three-term law is `1.000 ± 0.003` (to the leading term alone it drifts to `0.95`); the density of adjacent max/min pairs
  that are *not* elder pairs, fitted as `Aℓ^{1/4} + Bℓ^{3/4}`, gives `A = 0.07779 ± 0.00080` against
  `I − C₁ = 0.0778330` (`χ²/dof = 0.6`); non-adjacent bars are `< 0.2%` of all bars at `ℓ ≤ 0.05`.
- *Pre-review referee computations (same author family; not acceptance).* An independent implementation of the sign
  kernels (conditioning from the closed-form covariance at `40 + 12log₁₀(1/t)` digits, `h` down to `10^{−40}`) gave the
  `h^{1/4}` coefficients `−0.0748867035` (`θ = 1`) and `−0.1138031794` (`θ = 1/3`) against `I/2` and `C₁/2`, and the `h^{1/3}`
  coefficient `0.11502229` against `B₂` (relative agreement `10^{−9}` to `10^{−11}`); after the three terms the remainder
  divided by `h^{3/4}` is constant (`≈ 0.038`, `θ = 1/3`) over `h = 10^{−10}, …, 10^{−26}`, so for the sign kernels the next
  term is of order `h^{3/4}`. A second independent Monte Carlo (`2.6·10⁷` length) gave `ν`/three-term `= 0.9961 ± 0.0026`
  and `ν₊`/three-term `= 0.9986 ± 0.0037` on `[10⁻³, 10⁻²)`, rejecting the one- and two-term laws (`|z| ≥ 14`).
- *Why plain histograms look flat.* For the Gaussian kernel the second and third terms nearly cancel on
  `10⁻⁴ ≤ ℓ ≤ 10⁻²`: `ν/(C₀ℓ^{−1/3}) − 1 = ℓ^{7/12}(−2.067 + 2.089ℓ^{1/12}) + …` (`−1.6%` at `ℓ = 10⁻³`), and for the
  crest-to-trough density `−1.360 + 2.089ℓ^{1/12}` vanishes at `ℓ ≈ 0.006`.

**6.3 Literature.** #147 and #210 found no small-amplitude exponent for the crest-to-trough law in Rice 1944/45,
Cartwright–Longuet-Higgins 1956, Lindgren 1972 or Lindgren 2019 (whose exact joint law of adjacent extremes contains
(D1.1) implicitly), and Perez (arXiv:2012.09459) states the smooth short-bar law as open. Theorem D1 makes #210's remark a
theorem on the circle and adds two terms. Not located is not absent; the database pass of #147 remains to be run.

**6.4 The line.** The near-pair analysis (§§1–3, Lemma 4.1) is local. On `R` the far bound of Lemma 4.3 needs a
decorrelation hypothesis (uniform nondegeneracy of separated values); with, e.g., exponentially decaying `ρ^{(j)}` the
same proof applies. Not claimed here.

## 7. Sources (exact identities in `SOURCES.json`)

Cited for comparison only (nothing is consumed): Math- #207 `frontiers/cusp_second_order_20261001/PROOF.md` (v1.1, head
`826b8be`); Math- #210 `reviews/literature_classical_neighbors_20261001/ADDENDUM.md` (v1.1, head `7929169`); merged
`reviews/literature_lifetime_law_recon_20260929/RECONNAISSANCE.md` (`003b9879`); for the marked Kac–Rice convention [P]
`imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` §9 and [E2]
`reviews/d1_section9_borel_repair_20260925/REPAIR.md`. External: J.-M. Azaïs and M. Wschebor, *Level Sets and Extrema of
Random Processes and Fields* (Wiley, 2009), Ch. 6; Markov's and Landau's inequalities; Bulinskaya's lemma.

## 8. Exact controls and exploration

`d1_check.py` (standard library; output `RESULTS.json`, byte-identical under `-O`; mutants M1–M5 exit 1, an unknown label
exits 2):
- **C1** the constants: exponent bookkeeping in `2^a3^bπ^c` with rational exponents — (CU.2) at `d = 1` equals `C₁`, the two
  printed forms of `C₁` agree, `I/C₁ = 3^{1/4}/2`, `C₀` from the fold integral.
- **C2** Lemma 2.1: `k_θ` exactly for `θ = 1, 1/3`, and a quadrature check of `∫ζ_θ s^{−5/4}`.
- **C3** the model (3.1): polynomial identities; the critical-point structure; the margins of Lemma 3.3 at rational `φ`
  (including the extension to `1 ≤ |φ| ≤ 6/5`); the
  decision by exact persistence of `g` for 117 rational `φ ∈ (−1, 1)`: elder iff `|φ| < 1/3`.
- **C4** Lemma 1.3: block structure and the coefficients `c₂, d₂, q₂`, `v₁`, `v₂` as exact Laurent series in `τ` computed from
  the covariance (not from the jets) for the Gaussian kernel and the mixture `(e^{−x²/2} + e^{−2x²})/2`.
- **C5** the `B₂` assembly: the polynomial identity of §2(e) (exact multivariate polynomials) and the Gaussian-kernel value
  `𝒬/(120λ₂λ₄D) = 3/4`.
- **C6** the two-point Rice integral (§6.2), both kernels: fitted `a`, `b` within `2·10⁻⁴` and `3·10⁻³` of the predictions.

What the controls do not test: Lemma 1.1, the Kac–Rice representation, the error bounds of Proposition 2.2, Lemmas 3.2–4.3
and the assembly (§5) are proved in prose only; C6 is a numerical consistency check of Proposition 2.2's constants, not a
proof.

## 9. Review slices

- **A** §1: the pair coordinates and Jacobian, Lemma 1.2 (reflection), Lemma 1.3 (the jet expansions and their coefficients).
- **B** §2: Proposition 2.2 — the convexity bound (a), the split (b)–(d), the closed forms (e) and the `B₂` identity.
- **C** §3: Lemmas 3.1–3.3 and Corollary 3.4 — the model, the margins, the window decision.
- **D** §4–§5: the band lemma, interior densities, thin and far pairs, and the assembly, including the misclassification
  bound in (D1.2).
- **E** §6: the comparison with #207 and the numerical evidence.
