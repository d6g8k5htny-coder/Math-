# The one-dimensional lifetime and crest-to-trough laws with remainder `O(h^{3/4})`

Object: CL-D1-SHARP-REMAINDER-20261001-v1.2.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 1 October 2026.
**v1.1 (labels, binding and one expository addition; no mathematical change):** (i) after the xAI concern on Math- #214
(comments 5940492097 and 5940563636), #214 v1.2 renamed its theorem **Theorem 1D**, label only, so that it is not read
as the cap component D1 (Math- #193, #194). This note follows: its theorem is **Theorem 1D⁺**, with displays
(1D⁺.1)–(1D⁺.2), and #214 is cited as [1D], bound to its v1.2 blob. (ii) Proposition M's bad-event step names the
moments that its Cauchy–Schwarz bounds use, as suggested in the Codex Slice D review (Math- #238, review 5386194030).
The object identifier and the paths keep `D1`/`d1`, which there mean dimension one.
**v1.2 (rebinding and the nonblocking amendments of the nonauthor reviews; no mathematical change):** (i) [1D] is rebound
to Math- #214 v1.3 (head `54666d2`, PROOF blob `1591ecee`). v1.3 applies the clarifications its reviewers asked for
(comment 5933752065, items 1–4; review 5387031124, E-LIT). None changes a statement used here: [1D] Lemma 4.3 still gives
`O(h^{3/4})` on `[t_*, t₀]`, its `[t₁, t₀]` part now written `O(h(log(1/h))^{3/2})`. (ii) The two reporting corrections of
the Slice E review (review 5387084565). §5.1 no longer says that disjoint exponent families exclude logarithms, or that the
later exponents are established (E-SCOPE-01). §5.4 describes its model as a degree-40 truncation of the Gaussian-kernel
series, not the stationary process (E-SCOPE-02). (iii) The optional sentence of the Slice C review (review 5386932211) in
the proof of Lemma W: critical points outside the window cannot change the decision. (iv) §6 records the acceptance
boundary of [1D].
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph,
STATUS, PROOF_INDEX, prize or Boolean change. Same GitHub account as every lane; zero organizational independence.
**Consumes** Math- #214 (open, unmerged; head `54666d26e1…`, `frontiers/d1_third_order_law_20261001/PROOF.md` blob
`1591ecee`, v1.3), cited below as [1D]. Its nonauthor analytic review (OpenAI Codex, comment 5933752065, "Slices A–D and
Theorem D1 ACCEPTED at the stated circle scope", under the theorem's former name) was given on head `f4a58df`, with
supplementary derivations in comments 5930841283 and 5931058934. The refresh to `cf162b1` merged `main` and left the
packet's bytes unchanged. v1.2 (`4703fc7`) changed labels only (carried forward in comment 5941929764). v1.3 (`54666d2`)
applies that review's four listed clarifications and the attribution amendment of the Slice E review (5387031124). Used
from [1D]: §§0–5 as stated, and also the intermediate estimates in the proof of [1D] Prop. 2.2 (c)–(d). §2 reruns those
estimates on a longer range. The expansions among them follow from [1D] Lemma 1.3, the bounds on `ζ_θ` are properties
of `ζ_θ` alone, and none of them uses `t ≤ t_*` (Prop. 2.2⁺ (c)). Nothing else is consumed.

## 0. Statement

Setting, notation and constants are those of [1D] §0–§1:
- the circle `T = R/LZ` and the hypothesis (H);
- the canonical two-point densities `ν₊` (crest-to-trough amplitude) and `ν` (persistence lifetime);
- the pair at `±τ`, with separation `t = 2τ`, gap `h`, `α = 12h/t³` and `κ = h/t⁴`;
- the pinned law `Q = Q_{t,α}` and the pair variables `E₁, E₂, m = c(t)α, v₁, v₂`;
- the constants `C₀, C₁, I = (3^{1/4}/2)C₁, B₂`.

Throughout, `‖u‖_{C²} := max(sup|u|, sup|u'|, sup|u''|)` on `[−2, 2]`.

**Theorem 1D⁺.** Under (H), as `h ↓ 0` and `ℓ ↓ 0`,

    ν₊(h) = (C₀/2) h^{−1/3} + (I/2) h^{1/4} + B₂ h^{1/3} + O(h^{3/4}),                        (1D⁺.1)
    ν(ℓ)  =  C₀ ℓ^{−1/3}   +  C₁ ℓ^{1/4}  + 2B₂ ℓ^{1/3} + O(ℓ^{3/4}).                        (1D⁺.2)

In particular `2ν₊(ℓ) − ν(ℓ) = (I − C₁)ℓ^{1/4} + O(ℓ^{3/4})`. [1D] §0 reads `2ν₊ − ν` as the density of adjacent
max/min pairs that are not elder pairs.

[1D] proved the same expansions with `O(h^{1/2})`; its proof gives `O(h^{0.57})` for (1D.1). The exponent `3/4` is the
order of the first correction to the cusp term (§5.1). No claim is made that its coefficient is nonzero.

**What limited [1D], and what replaces it.**

| | [1D] | limit | here |
|---|---|---|---|
| `E₂`-correction | Prop. 2.2 (a): kernel `≤ Ct²` on `t ≤ t_*` | `O(t_*³) = O(h^{0.61})` | Lemma E: kernel `≤ Ct² min(1, s)`, `s = m v₁^{−1/2} ≍ κ`, so `O(h^{3/4})` |
| tails at `t_*` | Prop. 2.2 (c), (d): fold and cusp cut at `t_*` separately | `O(h²t_*^{−7}) = O(h^{0.57})` | Prop. 2.2⁺ (b): their difference, the model kernel, is `O(h³t^{−12})` beyond `t_*`, so both are integrated to a fixed `t₀` |
| elder misclassification | §5: window perturbation of relative size `t/κ`, bounded in absolute value | `O(h^{1/2})` | Lemmas Φ, W and Prop. M: given all but `φ_G = E₁/m`, the elder set is an interval `(φ₋, φ₊)` independent of `φ_G`. The misclassified mass is first order in the mean of the first-order part of `φ₊ − φ₋ − 2/3`, which is `O(t²)`, and second order in its fluctuation, `O((t/κ)²)`. |

**Mechanism.**
- *Splitting and regression.* Under `Q` the field splits into independent even and odd parts ([1D] Remark 1.4).
  Regressing the even part on `E₁` makes the rescaled field affine in `φ_G := E₁/m` (Lemma Φ). The profile is
  `≈ 3(X² − ¼)²`, and the remainder is independent of `φ_G`.
- *The elder set is an interval.* The elder rule is monotone in `φ_G` near the window edges `±1/3`. So, given the
  remainder, the elder set is an interval `(φ₋, φ₊)`. To first order its edges move by the values of the perturbation at
  `∓3/2`, where `∂_φ` of the competing critical value is `12` (Lemma W).
- *What moves the edges.* The even remainder `B` moves both edges the same way. A translation of the window costs
  nothing to first order, because the weight and the density of `φ_G` are even. The odd part changes the window length
  by `O(3/2)/6`, and the deterministic even profile `φÊ` changes it by `−Ê(3/2)/18`.
- *Why the mean is `O(t²)`.* The mean of this first-order part is `O(t²)`: the pins see the odd jets only through
  `α ≍ κt`, and `Ê = O(t²)`.
- *Second order.* The fluctuations, of relative size `t/κ`, enter at second order, and through the correlation
  `2m Cov(E₂, O(3/2))` of `O` with the weight.

Both orders are relative `O(t² + (t/κ)²)` of the edge mass, which integrates to `O(h^{3/4})` (Proposition M).

**Not claimed.** The `h^{3/4}` coefficient or its sign; sharpness of `3/4`; uniformity in the covariance; anything on `R`
([1D] §6.4).

## 1. The `E₂`-correction

As in [1D] §2, let `E₁ ~ N(0, v₁)` and `E₂ ~ N(0, v₂)` be independent, `m > 0` and `s := m v₁^{−1/2}`. Put

    w := ((m + E₂)² − E₁²)⁺1{m + E₂ > 0},   G₁ := E w,   G_{1/3} := E[w 1{|E₁| < m/3}],
    g_θ := E[(m² − E₁²)⁺1{|E₁| < θm}]   for θ ∈ {1, 1/3}.

**Lemma E.** For `θ ∈ {1, 1/3}`, with an absolute constant `C`,

    0 ≤ G_θ − g_θ ≤ C [ v₂ min(1, s) + (v₂ + m²) e^{−m²/(8v₂)} ].                                   (1.1)

*Proof.* For `a ≥ 0` put `q_a(e) := (m + e)² − a²` and `χ_a(e) := q_a(e)1{m + e > a} = ((m + e)² − a²)⁺1{m + e > 0}`.
`χ_a` is convex: it is zero for `e ≤ a − m`, equal to `q_a` beyond, and `q_a'(a − m) = 2a ≥ 0`. So
`Ψ(a) := Eχ_a(E₂) − χ_a(0) ≥ 0`. By independence, `G₁ − g₁ = EΨ(|E₁|)` and
`G_{1/3} − g_{1/3} = E[Ψ(|E₁|)1{|E₁| < m/3}]`, which gives the lower bound.

If `m² < 64v₂`, the upper bound is trivial: `G_θ − g_θ ≤ G₁ ≤ E(m + E₂)² = m² + v₂ ≤ e⁸(v₂ + m²)e^{−m²/(8v₂)}`. So assume
`m² ≥ 64v₂`, and put `T(x) := E[E₂²1{|E₂| > x}] ≤ C(v₂ + x²)e^{−x²/(2v₂)}`.

(i) `a ≤ m/2`. On `{|E₂| ≤ m/2}`, `χ_a(E₂) = χ_a(0) + 2mE₂ + E₂²`, and `E[E₂1{|E₂| ≤ m/2}] = 0`. On `{|E₂| > m/2}`,
`χ_a(E₂) ≤ (m + |E₂|)² ≤ 9E₂²`. So `Ψ(a) ≤ v₂ + 9T(m/2)`.

(ii) `m/2 < a ≤ 2m`, with `b := |a − m|`.
- If `a < m`, then `χ_a = q_a − q_a1{E₂ ≤ −b}`. On `{E₂ ≤ −b}`,
  `−q_a(E₂) = (|E₂| − b)(m + a − |E₂|) ≤ 3m(|E₂| − b)⁺`. Since `Eq_a(E₂) − q_a(0) = v₂`, `Ψ(a) ≤ v₂ + 3mE(|E₂| − b)⁺`.
- If `a ≥ m`, then `χ_a(0) = 0` and `χ_a(e) = (e − b)⁺(e − b + 2a) ≤ (|e| − b)⁺(|e| + 4m)`.

In both cases `Ψ(a) ≤ v₂ + E[(|E₂| − |a − m|)⁺(|E₂| + 4m)]`.

(iii) `a > 2m`, with `b := a − m > m`. For `e > b`, `χ_a(e) ≤ e(e + b + 2m) ≤ 4e²`, so `Ψ(a) ≤ 4T(m)`.

For `θ = 1/3` only (i) occurs, and `P(|E₁| < m/3) ≤ min(1, s)`. For `θ = 1`,

    EΨ(|E₁|) ≤ (v₂ + 9T(m/2))P(|E₁| ≤ 2m) + E[(|E₂| + 4m)∫_{m/2}^{2m}(|E₂| − |a − m|)⁺p_{|E₁|}(a)da] + 4T(m).

Fix `E₂ = e`. If `|e| ≤ m/2`, the integrand lives on `|a − m| < |e|`, where `p_{|E₁|}(a) ≤ 2(2πv₁)^{−1/2}e^{−s²/8}`,
and `∫(|e| − |a − m|)⁺da = e²`. If `|e| > m/2`, the integral is at most `|e|`. So the middle term is at most

    2(2πv₁)^{−1/2}e^{−s²/8}E[(|E₂| + 4m)E₂²] + 9T(m/2) ≤ C(m + v₂^{1/2})v₂v₁^{−1/2}e^{−s²/8} + 9T(m/2).

Now `m v₁^{−1/2} = s`, `v₂^{1/2} ≤ m/8`, `s e^{−s²/8} ≤ 2 min(1, s)` and `P(|E₁| ≤ 2m) ≤ 2 min(1, s)`, which give
(1.1). ∎

Control C6 checks this order on a grid. Write `Φ` and `ϕ` for the standard normal distribution function and density.
- `(G_θ − g_θ)/(v₂ min(1, s))` stays in `[0, 2]`.
- As `v₂/v₁ → 0`, `(G_θ − g_θ)/v₂` approaches `2Φ(s) − 1 + 2sϕ(s)` for `θ = 1` and `2Φ(s/3) − 1` for `θ = 1/3`.

## 2. The sign kernels to `O(h^{3/4})`

**Proposition 2.2⁺.** Fix `δ ∈ (0, 1/10]` and `t_* := (12h)^{1/(5−δ)}`, as in [1D] Prop. 2.2 (`t ≤ t_*` iff
`α ≥ t^{2−δ}`). For `θ ∈ {1, 1/3}`, with `I₁ := I` and `I_{1/3} := C₁`,

    ∫₀^{t_*} K_θ^{sign}(t, h) dt = (C₀/2) h^{−1/3} + (I_θ/2) h^{1/4} + B₂ h^{1/3} + O(h^{3/4}).

*Proof.* Fix `t₀ ∈ (0, 1]` so small that the expansions of [1D] Lemma 1.3 hold on `t ≤ t₀`, and let `h` be so small
that `t_* ≤ t₀`. The model kernel ([1D] Prop. 2.2 (b)) is

    k_θ := (12/t⁴)p_t g_θ = (12/t⁴)p_t m² − (12/t⁴)p_t v₁ζ_θ(s).

By Lemma 1.3:
- `m ≍ τα`, `v₁ ≍ τ⁴`, `v₂ ≍ τ⁶`;
- `p_t ≤ Ce^{−α²/(4σ₃²)}` and `(12/t⁴)v₁ ≤ C`;
- `s ≤ Cα/τ ≤ Ch/t⁴`.

(a) *The `E₂`-correction.* On `t ≤ t_*`, `m²/v₂ ≥ cα²τ^{−4} ≥ ct^{−2δ}`. Lemma E gives

    0 ≤ K_θ^{sign} − k_θ ≤ C(12/t⁴)p_t[v₂ min(1, s) + (v₂ + m²)e^{−m²/(8v₂)}] ≤ Ct² min(1, Ch/t⁴) + Ct^{−4}e^{−ct^{−2δ}},

using `(1 + α²)p_t ≤ C`. Since `∫₀^∞ t² min(1, h/t⁴) dt = (4/3)h^{3/4}` and

    ∫₀^{t_*}t^{−4}e^{−ct^{−2δ}}dt ≤ C_{c,δ} t_* e^{−(c/2)t_*^{−2δ}} = O(h^N) for every N,   C_{c,δ} := sup_{t>0}t^{−4}e^{−(c/2)t^{−2δ}} < ∞,

we get `∫₀^{t_*}(K_θ^{sign} − k_θ)dt = O(h^{3/4})`.

The correction is integrated only up to `t_*`. Beyond `t ≍ h^{1/5}`, where `m ≍ v₂^{1/2}`, the difference
`K₁^{sign} − k₁` contains the non-adjacent sign pairs, whose contribution is of order one in `h` ([1D] §6.2); that range
is handled by the band lemma (§4).

(b) *The tail of the model kernel.* `k_θ = (12/t⁴)p_t v₁γ_θ(s)` with
`0 ≤ γ_θ(s) = E[(s² − Z²)1{|Z| < θs}] ≤ s²P(|Z| < s) ≤ s³`. Hence `0 ≤ k_θ ≤ Cs³ ≤ Ch³t^{−12}` and

    ∫_{t_*}^{t₀}k_θ dt ≤ Ch³t_*^{−11} = O(h^{3 − 11/(5−δ)}).

Since `δ ≤ 1/9`, the exponent is at least `3/4`; it is `37/49` for `δ = 1/10`. Here the fold term `(12/t⁴)p_t m²` and the
cusp term `(12/t⁴)p_t v₁ζ_θ(s)` are each of order `h²t^{−8}`. Their difference `k_θ` is smaller by the factor
`s ≍ h/t⁴`, since `γ_θ(s) = 2θ(1 − θ²/3)(2π)^{−1/2}s³(1 + O(s²))`. [1D] cut each at `t_*` separately and lost
`h²t_*^{−7}`.

(c) *The model integral to `t₀`.* Run [1D] Prop. 2.2 (c)–(e) with the upper limit `t_*` replaced by `t₀`. None of the
estimates used in that proof uses `t ≤ t_*`. The expansions follow from [1D] Lemma 1.3 for `t ≤ t₀` and `α ≤ τ^{−1}`,
and from `p_t ≤ Ce^{−α²/(4σ₃²)}` beyond. The bounds on `ζ_θ` are properties of `ζ_θ` alone, and the split at `t_c` is a
device of the proof. The estimates are: the fold expansion with its `O(τ⁴(1 + α⁴))` term, the cusp expansion with
`|ε| ≤ Cτ²(1 + α²)`, the bounds on `ζ_θ`, `ζ_θ'` and `1 − ζ_θ`, and the split at `t_c = h^{1/4}`. The changes:
- in (c), the two leading integrals lose only their ranges `t > t₀`, which are `O(h²t₀^{−7}) = O(h²)`; the `τ⁴` term is
  `O(h)`, and the range `α > τ^{−1}` is `O(e^{−c/h})`;
- in (d), the Mellin integral loses its range `t > t₀`, where `ζ_θ(s₀) ≤ Cs₀² = Ch²t^{−8}`, so `O(h²)`;
- the integral of `p₃(α) − p₃(0)` loses its range `t > t₀`, where `|p₃(α) − p₃(0)| ≤ Cα² ≤ Ch²t^{−6}`, so `O(h²)`;
- the term in `1 − ζ_θ(s₀)` is `O(h^{3/4})`, as there;
- the error `ε` is `O(h^{3/4})`, as there, the range `t ∈ [h^{1/4}, t₀]` using `ζ_θ(s₀) ≤ Cs₀²`;
- (e) is unchanged.

So `∫₀^{t₀}k_θ dt = (C₀/2)h^{−1/3} + (I_θ/2)h^{1/4} + B₂h^{1/3} + O(h^{3/4})`.

Finally `∫₀^{t_*}K_θ^{sign} = ∫₀^{t₀}k_θ − ∫_{t_*}^{t₀}k_θ + ∫₀^{t_*}(K_θ^{sign} − k_θ)`. ∎

## 3. The elder decision at first order

### 3.1 Regression along `φ_G`

Fix `t ≤ t₀` and `α > 0`, and work under `Q = Q_{t,α}`. By [1D] Remark 1.4, `f = f_e + f_o` with `f_e` and `f_o`
independent.
- `f_e` is centered, and its law does not depend on `α`: its only pin, `U₂ = 0`, is homogeneous, and `U₁, U₃` are
  functionals of `f_o`.
- `f_o` has mean `αμ_t`, with `μ_t` deterministic and odd, and its centered part has a law that does not depend on `α`.

As in [1D] Lemma 1.2, `E₁ := f_e''(τ)`, `m := E_Q f_o''(τ) = c(t)α`, `E₂ := f_o''(τ) − m`, `v₁ := Var_Q E₁` and
`s := m v₁^{−1/2}`. Define

    ψ(x) := Cov_Q(f_e(x), E₁)/v₁,   f_e^⊥ := f_e − E₁ψ,   φ_G := E₁/m,   ω := (f_o, f_e^⊥).

With `b := f(−τ)` and `F(X) := (f(tX) − b)/h` (the window field `𝔉` of [1D] Lemma 3.2),

    F = 2X³ − (3/2)X − ½ + O + B + φ_G Ψ̂,                                                        (3.1)
    O(X) := f_o(tX)/h − 2X³ + (3/2)X,   B(X) := (f_e^⊥(tX) − f_e^⊥(τ))/h,   Ψ̂(X) := (m/h)(ψ(tX) − ψ(τ)).

This uses `f_e(−τ) = f_e(τ)` and `f_o(−τ) = −f_o(τ) = h/2` on the pin event. The model
`g_φ = 2X³ − (3/2)X − ½ + 3φ(X² − ¼)²` is the odd cubic plus the even quartic (checker C1). So
`F = g_{φ_G} + O + B + φ_GÊ` with `Ê := Ψ̂ − 3(X² − ¼)²`.

**Lemma Φ.** (Φ.0) Under `Q`:
- `φ_G ~ N(0, s^{−2})` is independent of `ω`, and `E₂` is a functional of `f_o`;
- `O` is odd, and `B`, `Ψ̂`, `Ê` are even;
- `Ψ̂` is deterministic and depends on `t` only;
- `O`, `B`, `Ê` and their first derivatives vanish at `X = ±½`.

For `t ≤ t₀`, uniformly in `α`, on `[−2, 2]`:

- (Φ.1) `‖Ê‖_{C²} ≤ Cτ²`;
- (Φ.2) `‖E_Q O‖_{C²} ≤ Ct²` and `‖O − E_QO‖_{C²} ≤ C(t/κ)K̃^o`, where `K̃^o := sup_{[−2t, 2t]}|(f_o − E_Qf_o)^{(5)}|`;
- (Φ.3) `‖B‖_{C²} ≤ C(t²/κ)K^⊥` for a random variable `K^⊥` with `E_Q e^{c(K^⊥)²} ≤ C`; also `E_Q e^{c(K̃^o)²} ≤ C`;
- (Φ.4) `f_o''(τ) = (h/t²)(6 + O''(½))`, so `m = (h/t²)(6 + E_QO''(½))` and `E₂ = (h/t²)(O − E_QO)''(½)`. In particular,
  for `t ≤ t₀` small, `m ≥ h/t²` and `|E₂|/m ≤ ‖O − E_QO‖_{C²}/5`. Also `s = (72κ/σ₄)(1 + O(τ²))`.

*Proof.* (Φ.0) `f_e^⊥` is jointly Gaussian with `E₁` and uncorrelated with it, and `f_o` is independent of `f_e`. The
parities are those of `f_e` and `f_o`. The vanishing at `±½`:
- `f_e'(±τ) = 0` under `Q`, so `ψ'(±τ) = 0` and `(f_e^⊥)'(±τ) = 0`;
- `Ψ̂(±½) = 0` because `ψ` is even, and `Ψ̂'(±½) = (mt/h)ψ'(±τ) = 0`. Since `3(X² − ¼)²` vanishes to second order at
  `±½`, so does `Ê`;
- `f_o(±τ) = ∓h/2` and `f_o'(±τ) = 0`, while `2X³ − (3/2)X` takes the values `∓½` at `±½` with zero derivative there.

(Φ.1) Let `a_j := f^{(j)}(0)`. Taylor's formula gives `f_e(x) = a₀ + a₂x²/2 + a₄x⁴/24 + R(x)`, with
`|R^{(k)}(x)| ≤ C|x|^{6−k}K^e` (`k ≤ 2`) and `K^e := sup_{[−2t, 2t]}|f_e^{(6)}|`. The pin `f_e'(τ) = 0` gives
`a₂ = −a₄τ²/6 − R'(τ)/τ`, hence (checker C3)

    f_e(x) − f_e(τ) = a₄(x² − τ²)²/24 + R̃(x),   R̃(x) := R(x) − R(τ) − R'(τ)(x² − τ²)/(2τ),
    E₁ = a₄τ²/3 + ρ₁,   ρ₁ := R''(τ) − R'(τ)/τ,

with `|∂_X^k R̃(tX)| ≤ Ct⁶K^e` on `[−2, 2]` (`k ≤ 2`) and `|ρ₁| ≤ Cτ⁴K^e`. The `Q`-law of `f_e` is free of `α`, and
`E_Q(K^e)² ≤ C` by Sudakov–Fernique and Borell–TIS, as in [1D] Lemma 4.3. Also `V := Var_Q a₄ → σ₄²`, so `V ∈ [c, C]`.
Then

    v₁ = (τ⁴/9)V(1 + O(τ²)),   Cov_Q(f_e(tX) − f_e(τ), E₁) = (t⁴/24)(X² − ¼)²(τ²V/3)(1 + O(τ²)) + Cov_Q(R̃(tX), E₁),

and `|Cov_Q(∂_X^kR̃(tX), E₁)| ≤ Ct⁶τ²`. Since `m/h = 12c(t)/t³ = (6/t²)(1 + O(τ²))` (Lemma 1.3), the first term gives
`(m/(hv₁))(t⁴/24)(τ²V/3)(X² − ¼)² = 3(X² − ¼)²(1 + O(τ²))`; checker C3 checks the leading constant `3`. The second term
contributes `O(t^{−2}t⁶τ²τ^{−4}) = O(t²)` in `C²`.

(Φ.2) Write `f_o(x) = a₁x + a₃x³/6 + R_o(x)`, with `|R_o^{(k)}(x)| ≤ C|x|^{5−k}K^o` and `K^o := sup_{[−2t, 2t]}|f_o^{(5)}|`.
The odd cubic `H₀(x) := h(2(x/t)³ − (3/2)(x/t))` satisfies `H₀'(τ) = 0` and `H₀(τ) = −h/2`. Let `p₁`, `p₂` be the odd
cubic Hermite basis at `τ`: `p₁(x) = (3/2)(x/τ) − ½(x/τ)³` and `p₂(x) = (τ/2)((x/τ)³ − x/τ)`, so that `p₁(τ) = 1`,
`p₁'(τ) = 0`, `p₂(τ) = 0` and `p₂'(τ) = 1`. The pins then give

    f_o = H₀ + R̃_o,   R̃_o := R_o − R_o(τ)p₁ − R_o'(τ)p₂.

So `O = R̃_o(t·)/h` and `‖O‖_{C²} ≤ C(t⁵/h)K^o = C(t/κ)K^o`. The map `f_o ↦ R̃_o` is linear, which gives both bounds.
- *Applied to `αμ_t`* it gives `‖E_QO‖_{C²} ≤ C(αt⁵/h)sup_{[−2t, 2t]}|μ_t^{(5)}| = 12Ct² sup|μ_t^{(5)}|`. The sup is
  bounded uniformly: `μ_t^{(5)}(x) = Cov(f_o^{(5)}(x), (U₁, U₃))Cov(U₁, U₃)^{−1}e₂` is continuous in `(t, x)`,
  `Cov(U₁, U₃)` is invertible for each `t > 0` ([1D] Lemma 1.1), and it has a nondegenerate limit as `t ↓ 0` ([1D] Lemma
  1.3). So `sup_{t ≤ t₀}sup_{[−2t,2t]}|μ_t^{(5)}| < ∞`.
- *Applied to `f_o − E_Qf_o`* it gives the second bound.

(Φ.3) We have `B = [a₄^⊥(t⁴/24)(X² − ¼)² + R̃^⊥(tX)]/h`, where `a₄^⊥ := a₄ − E₁Cov_Q(a₄, E₁)/v₁` and
`R̃^⊥ := R̃ − E₁Cov_Q(R̃, E₁)/v₁`.
- `Var_Q a₄^⊥ = Var_Q(a₄ | E₁) ≤ Var_Q(a₄ − 3E₁/τ²) = 9Var_Q(ρ₁)/τ⁴ ≤ Cτ⁴`.
- `|E₁Cov_Q(∂_X^kR̃(tX), E₁)/v₁| ≤ Ct⁶|Z|`, with `Z := E₁v₁^{−1/2}` standard normal.

So the bound holds with `K^⊥ := C(|a₄^⊥|/t² + K^e + |Z|)`. Each term has a Gaussian tail uniformly, and so does `K̃^o`
(Borell–TIS).

(Φ.4) `f_o''(τ) = (h/t²)∂_X²(2X³ − (3/2)X + O)|_{X=½}` and `∂_X²(2X³ − (3/2)X)|_{½} = 6`. Then
`|E_QO''(½)| ≤ Ct²`. Lemma 1.3 gives `s = mv₁^{−1/2} = 3α/(τσ₄)(1 + O(τ²))`, and `3α/(τσ₄) = 72κ/σ₄`. ∎

### 3.2 The window edges

The model `g_φ` of [1D] (3.1) has its third critical point at `X₃ = −1/(2φ)`. There (checker C1)

    Γ₊(φ) := g_φ(X₃) + 1 = (φ + 1)³(3φ − 1)/(16φ³),   Γ₋(φ) := g_φ(X₃) = (φ − 1)³(3φ + 1)/(16φ³),
    Γ₊'(φ) = Γ₋'(φ) = 3(1 − φ²)²/(16φ⁴),   Γ₊(1/3) = Γ₋(−1/3) = 0,   Γ₊'(1/3) = Γ₋'(−1/3) = 12,   g_φ''(X₃) = 3(1 − φ²)/φ.   (3.2)

Put `η₀ := 1/100`, `J₊ := [1/3 − η₀, 1/3 + η₀]` and `J₋ := −J₊`.

**Lemma W (the window edges to first order).** There is an absolute `c₀ > 0` with the following property.

*Hypotheses.*
- `η⁰, Ê ∈ C²([−2, 2])` vanish with their first derivatives at `±½`;
- `ε := ‖η⁰‖_{C²} + 2‖Ê‖_{C²} ≤ c₀`;
- for `φ ∈ R`, `F_φ := g_φ + η_φ` on `[−2, 2]`, with `η_φ := η⁰ + φÊ`;
- for each `φ`, `F_φ` is the window field of a pair `(𝔐, 𝔖) = (−½, ½)` of a function `f_φ` on `T`.

*Conclusions.*
- (W.1) There are `φ₊ ∈ J₊` and `φ₋ ∈ J₋` such that, for every `φ` for which the pair is typed, `𝔖` is `𝔐`'s death
  point iff `φ₋ < φ < φ₊`, except at `φ ∈ {φ₋, φ₊}`.
- (W.2) `φ₊ = 1/3 − η_{1/3}(−3/2)/12 + r₊` and `φ₋ = −1/3 − η_{−1/3}(3/2)/12 + r₋`, with `|r_±| ≤ Cε²`.
- (W.3) If `η⁰ = O + B` with `O` odd and `B` even, then
  `φ₊ − φ₋ − 2/3 = O(3/2)/6 − (Ê(3/2) + Ê(−3/2))/36 + r₊ − r₋`. If moreover `Ê` is even,

      φ₊ − φ₋ − 2/3 = O(3/2)/6 − Ê(3/2)/18 + r₊ − r₋.                                            (3.3)

*Proof.* *Typing.* For `|φ| ≤ 2`, `‖F_φ − g_φ‖_{C²} ≤ ε`, and typing forces `|φ| < 1 + ε/6` ([1D] Lemma 3.3). For
`|φ| > 2` the pair is not typed:
- for `φ > 2`, `F_φ''(−½) = 6(φ − 1) + η⁰''(−½) + φÊ''(−½) ≥ 6(φ − 1) − ε − φε/2 > 0`;
- for `φ < −2`, symmetrically `F_φ''(½) < 0`.

*Off the edges.* [1D] Lemma 3.3 with `η = η₀`, taking `c₀ ≤ c₀^{[1D]}η₀`, gives: for typed `φ` with
`||φ| − 1/3| ≥ η₀`, `𝔖` is the death point iff `|φ| < 1/3`.

*The edge `J₊`.* Fix `φ ∈ J₊`. The model satisfies, exactly (checker C2):
- `g' = 12φ(X² − ¼)(X − X₃)` with `X₃ ∈ [−150/97, −150/103] ⊂ [−1.55, −1.45]`;
- `12φ(X² − ¼) ≥ 2.9` on `[−2, −1]`;
- `g(−2) = 675φ/16 − 27/2 ≥ 9/64`;
- `g''(X₃) ≥ 7.7`, and `|g'''| = |12 + 72φX| ≤ 52` on `[−1.6, −1.4]`;
- `g(X₃) = Γ₊(φ) − 1 ≤ −0.88`;
- `g + 1 ≥ 2(X + 1)(X − ½)² ≥ 3(X − ½)²` on `[½, 3/2]`, and `g(3/2) = 12φ + 4 > 7`;
- `g' < 0` on `(−½, ½)`, with `|g'| ≥ 1.8(½ − |X|)`;
- `g − g(X₃) = (X − X₃)²(3φX² − X + (1 − 6φ²)/(4φ))`, and the quadratic factor is `≥ 2.24` on `[−2, −1]`.

Since `η_φ` and `η_φ'` vanish at `±½` and `|η_φ''| ≤ ε`, we have `|η_φ'(X)| ≤ ε|X ∓ ½|` and
`|η_φ(X)| ≤ (ε/2)(X ∓ ½)²`. Hence, for `c₀ ≤ 1/10` small enough:
- `F' < 0` on `(−½, ½)`;
- `F + 1 ≥ (3 − ε)(X − ½)² > 0` on `(½, 3/2]`, and `F(3/2) > 0`;
- `F' > 0` on `[−1, −½)`, since `g' ≥ 1.7|X + ½|` there;
- on `[−2, −1]`, `F'` vanishes only within `ε/2.9 ≤ 1/20` of `X₃`. There `g'' ≥ 7.7 − 52/20 ≥ 5.1`, so `F'' ≥ 5`.

So `F` has on `[−2, −½)` exactly one critical point `X₃'`, a nondegenerate minimum, and `F(−2) > 0 > F(X₃')`.
- The arc from `𝔐` in the positive direction descends to `𝔖`, stays above `−1` elsewhere, and exceeds `0` before `3/2`:
  `m₊ = −1`.
- The arc in the negative direction descends to `F(X₃')` and rises above `0` before `−2`:
  `m₋ = F(X₃') = μ₊(φ) := min_{[−2, −1]}F_φ`.

Hence `𝔖` is the death point iff `μ₊(φ) < −1`.

For `φ' > φ`, on `[−2, −1]`,

    F_{φ'} − F_φ = (φ' − φ)(3(X² − ¼)² + Ê) ≥ (φ' − φ)(27/16 − ε) ≥ φ' − φ,

so `μ₊` increases with slope at least `1`. Since `g ≥ g(X₃) + 2.24(X − X₃)² ≥ g(X₃) + 1.45(X − X₃)²` on `[−2, −1]` and
`|η_φ'| ≤ ε`,

    Γ₊(φ) − 1 + η_φ(X₃(φ)) − ε²/5.8 ≤ μ₊(φ) ≤ Γ₊(φ) − 1 + η_φ(X₃(φ)).

At `φ = 1/3` this gives `|μ₊(1/3) + 1| ≤ 2ε`. So the root `φ₊` of `μ₊ = −1` exists, is unique in `J₊`, and satisfies
`|φ₊ − 1/3| ≤ 2ε`. At `φ₊`:
- `Γ₊(φ₊) = 12(φ₊ − 1/3) + O(ε²)`, by (3.2) and `|Γ₊''| ≤ C` on `J₊`;
- `η_{φ₊}(X₃(φ₊)) = η_{1/3}(−3/2) + O(ε²)`, since `|η_{φ₊} − η_{1/3}| ≤ |φ₊ − 1/3|‖Ê‖_{C⁰}` and
  `|X₃(φ₊) + 3/2| ≤ C|φ₊ − 1/3|`.

This proves (W.2) for `φ₊`.

*The edge `J₋`.* This is the mirror case. Checker C1 checks the symmetry `g(−X, −φ) = −1 − g(X, φ)` and
`Γ₋(φ) = −Γ₊(−φ)`; checker C2 checks `g(2) + 1 = 675φ/16 + 27/2 ≤ −9/64` and `g''(X₃) ≤ −7.7`. Fix `φ ∈ J₋`.
- *The negative direction.* The arc falls below `−1` before exceeding `0`, as in [1D] Lemma 3.3 (E) for `φ < 0`. So
  `m₋ < −1`.
- *The positive direction.* The arc descends to `𝔖` and rises to a nondegenerate local maximum `F(X₃'')`, with `X₃''`
  near `X₃ ∈ [1.45, 1.55]`. It then falls below `−1` before `2`. So `m₊ = −1` iff `μ₋(φ) := max_{[1, 2]}F_φ > 0`.

Hence `𝔖` is the death point iff `μ₋(φ) > 0`. The function `μ₋` increases with slope at least `1`, and by the same
envelope bound its root `φ₋` satisfies (W.2).

In both edge cases, critical points outside `[−2, 2]` play no part. Along each arc they come only after the arc's first
crossing above `F(𝔐) = 0`, which ends that arc's contribution to `m_±`, or after the arc has already fallen below the
saddle value `−1`, which already gives `m_± < −1`.

(W.1) collects the three regimes. For (W.3):

    η_{1/3}(−3/2) = −O(3/2) + B(3/2) + Ê(−3/2)/3,   η_{−1/3}(3/2) = O(3/2) + B(3/2) − Ê(3/2)/3.

The even part `B` cancels from the window length; it only translates the window (checker C4). ∎

### 3.3 The misclassified mass

Let `K(t, h)` be the elder kernel [1D] (1.3) and `K_{1/3}^{sign} = (12/t⁴)p_t E_Q[w 1{|φ_G| < 1/3}]` the sign kernel,
where `w = (−f''(−τ))⁺f''(τ)⁺ = ((m + E₂)² − E₁²)⁺1{m + E₂ > 0}` ([1D] (1.4)).

**Proposition M.** For `δ ∈ (0, 1/10]` and `t_*` as above, `∫₀^{t_*}|K(t, h) − K_{1/3}^{sign}(t, h)| dt = O(h^{3/4})`.

*Proof.* Fix `α` and `t ≤ t_*`, with `h` small enough that `t_* ≤ t₀`. By Lemma Φ, conditionally on `ω`:
- `φ_G` has density `p_s(φ) := (s/√(2π))e^{−s²φ²/2}`;
- `E₂`, and the field (3.1) for each value of `φ_G`, are functions of `(ω, φ_G)`;
- `w = W(φ_G)` with `W(φ) := m²((1 + E₂/m)² − φ²)⁺1{m + E₂ > 0}`.

Put

    ε(ω) := ‖O‖_{C²} + ‖B‖_{C²} + 2‖Ê‖_{C²},     𝒢 := {ε(ω) ≤ c₁},

with `c₁ ≤ c₀` so small that on `𝒢` Lemma W applies to `F_φ = g_φ + (O + B) + φÊ` (with `Ê` even, (Φ.0)) and
`|E₂|/m ≤ 1/10` (Φ.4). On `𝒢`, `W > 0` on `(φ₋, φ₊)`, so the pair is typed there, and by (W.1)

    E_Q[w 1{elder} | ω] = ∫_{φ₋}^{φ₊} W p_s dφ,     E_Q[w 1{|φ_G| < 1/3} | ω] = ∫_{−1/3}^{1/3} W p_s dφ.

*First order.* On `𝒢`, `|φ₊ − 1/3|, |φ₋ + 1/3| ≤ Cε ≤ 1/12`, and `W` and `p_s` are even. So

    Δ := ∫_{φ₋}^{φ₊} W p_s − ∫_{−1/3}^{1/3} W p_s = (Wp_s)(1/3)·(φ₊ − φ₋ − 2/3) + r₂,
    |r₂| ≤ ½[(φ₊ − 1/3)² + (φ₋ + 1/3)²] sup_{1/4 ≤ |φ| ≤ 5/12}|(Wp_s)'| ≤ Cε² m²(1 + s²) s e^{−s²/32},

since `|(Wp_s)'(φ)| ≤ (2m²|φ| + Ws²|φ|)p_s(φ)` and `p_s(φ) ≤ (s/√(2π))e^{−s²/32}` for `|φ| ≥ 1/4`. With
`e_s := p_s(1/3) = (s/√(2π))e^{−s²/18}`, on `𝒢` we have `(Wp_s)(1/3) = e_s(8m²/9 + 2mE₂ + E₂²)`. By (3.3),

    Δ = e_s (8m²/9 + 2mE₂ + E₂²)(O(3/2)/6 − Ê(3/2)/18) + R₄,   |R₄| ≤ C m²(1 + s²) s e^{−s²/32} ε².

*The mean.* `E₂` is centered, and `E₂` and `O − E_QO` are jointly Gaussian, so `E[E₂²(O − E_QO)(3/2)] = 0` and

    E[(8m²/9 + 2mE₂ + E₂²) O(3/2)] = (8m²/9 + v₂)E_QO(3/2) + 2m Cov_Q(E₂, O(3/2)).

The bounds:
- by (Φ.2), `|E_QO(3/2)| ≤ Ct²` and `|Cov_Q(E₂, O(3/2))| ≤ v₂^{1/2}(Var_Q O(3/2))^{1/2} ≤ Cτ³(t/κ)`;
- by (Φ.1), `|Ê(3/2)| ≤ Cτ²`;
- since `m(t/κ) = 12mt²/α ≍ τ³`, also `mτ³(t/κ) ≤ Cm²(t/κ)²`;
- `v₂ ≤ Cm²`, since `m²/v₂ ≥ ct^{−2δ} ≥ c` on `t ≤ t_*` (Prop. 2.2⁺ (a)).

Hence

    |E[e_s(8m²/9 + 2mE₂ + E₂²)(O(3/2)/6 − Ê(3/2)/18)]| ≤ C e_s m² (t² + (t/κ)²),

and by (Φ.2)–(Φ.3), `E_Qε² ≤ C(t⁴ + (t/κ)² + (t²/κ)² + τ⁴) ≤ C(t² + (t/κ)²)`.

*The bad event.* Off `𝒢` there are two contributions. Both are bounded by Cauchy–Schwarz, using Gaussian moments: since
`E₂ ~ N(0, v₂)`, `E(m + |E₂|)⁴ ≤ C(m² + v₂)²` and `E(8m²/9 + 2mE₂ + E₂²)⁴ ≤ C(m² + v₂)⁴`.
- Both conditional expectations are at most `E[w | ω] ≤ (m + |E₂|)²`. By Cauchy–Schwarz this contributes at most
  `C(m² + v₂)P(𝒢^c)^{1/2}`.
- The main term above carries `e_s ≤ s/√(2π)` and the factor `Y := O(3/2)/6 − Ê(3/2)/18`. Here `E_Q[O(3/2)⁴] ≤ C`
  (Φ.2), and `Ê` is deterministic with `|Ê(3/2)| ≤ Cτ²` (Φ.1), so `E_QY⁴ ≤ C`. By Hölder, the mixed moment
  `E[(8m²/9 + 2mE₂ + E₂²)²Y²]` is at most `C(m² + v₂)²`, and by Cauchy–Schwarz the term contributes at most
  `Cs(m² + v₂)P(𝒢^c)^{1/2}`.

On `t ≤ t_*` we have `κ/t = α/(12t²) ≥ t^{−δ}/12` and `‖E_QO‖_{C²} + 2‖Ê‖_{C²} ≤ Ct² ≤ c₁/2`. The Gaussian tails of
`K̃^o` and `K^⊥` then give `P(𝒢^c) ≤ Ce^{−c(κ/t)²} ≤ Ce^{−ct^{−2δ}}`.

*Collecting.* For `t ≤ t_*`,

    |K − K_{1/3}^{sign}| ≤ C(12/t⁴)p_t [ m²(1 + s²) s e^{−s²/32}(t² + (t/κ)²) + (1 + s)(m² + v₂)e^{−ct^{−2δ}} ].

Now `(12/t⁴)m² ≤ Cα²/t² ≤ Cs²`, `(12/t⁴)v₂ ≤ Ct²` and `(t/κ)² = 144t⁴/α² ≤ Ct²/s²`, because `α/t ≍ s ≍ h/t⁴` (Φ.4).
- *The first part* is at most `Ct²(s + s⁵)e^{−s²/32} ≤ Ct² min(h/t⁴, e^{−ch²/t⁸})`. Its integral over `(0, ∞)` is
  `≤ Ch^{3/4}`: split at `t = h^{1/4}`, or substitute `t = (h/u)^{1/4}`, `t²dt = (1/4)h^{3/4}u^{−7/4}du` (checker C7).
- *The second part* is at most `C(1 + s³)e^{−ct^{−2δ}} ≤ C(1 + h³t^{−12})e^{−ct^{−2δ}}`. Its integral over `(0, t_*]`
  is `≤ C'_{c,δ}(1 + h³)t_*e^{−(c/2)t_*^{−2δ}} = O(h^N)`, where `C'_{c,δ} := sup_{t>0}(1 + t^{−12})e^{−(c/2)t^{−2δ}}`. ∎

## 4. Proof of Theorem 1D⁺

Fix `δ = 1/10`, and `t₀` as in Proposition 2.2⁺, small enough also for [1D] Lemma 4.3 (whose own `t₀` is a fixed constant
in `(0, L/4]`).

**(1D⁺.1).** Write `ν₊ = ∫₀^{t_*}K₊ + ∫_{t_*}^{L}K₊`, where `L` is the length of the circle.
- On `(0, t_*]`, `K₊ = K₁^{sign} − (12/t⁴)p_tE_Q[w1{not adjacent}]`. By [1D] Lemma 3.1, non-adjacency forces
  `K₅ ≥ ct^{−δ}`, so the correction integrates to `O(h^N)` ([1D] §5). Proposition 2.2⁺ with `θ = 1` gives the expansion.
- On `[t_*, L)`, `K₊ ≤ K^{band}` (an adjacent pair is banded), and [1D] Lemma 4.3 gives `O(h^{3/4}) + O(h)`.

**(1D⁺.2).** Write `ν = 2∫₀^{L/2}K` ([1D] §1).
- On `(0, t_*]`, `K = K_{1/3}^{sign} + (K − K_{1/3}^{sign})`. Proposition 2.2⁺ with `θ = 1/3` gives the expansion with
  `I_{1/3} = C₁`, and Proposition M bounds the rest by `O(h^{3/4})`.
- On `[t_*, L/2]`, an elder pair is banded or co-banded ([1D] §4), so `K ≤ K^{band} + K^{co}`, and [1D] Lemma 4.3 gives
  `O(h^{3/4})`.

Doubling gives (1D⁺.2). ∎

## 5. Remarks

**5.1 The order `h^{3/4}`.** Four pieces are each `h^{3/4}` times a convergent Mellin-type integral; here they are only
bounded:
- the `E₂`-correction (for `θ = 1/3`, `G_{1/3} − g_{1/3} = v₂P(|E₁| < m/3)(1 + o(1))`);
- the `τ²`-corrections of the cusp kernel ([1D] Prop. 2.2 (d), the error `ε`);
- the term `(p₃(α) − p₃(0))(1 − ζ_θ(s₀))`;
- for `ν`, the window edges of Proposition M: the mean of the first-order part of `φ₊ − φ₋ − 2/3`, the correlation term
  `2m Cov_Q(E₂, O(3/2))`, and the second-order terms.

Heuristically, the two-scale structure produces two families of exponents:
- the fold family `−1/3 + 2k/3`, at `t ≍ h^{1/3}`;
- the cusp family `1/4 + j/2`, at `t ≍ h^{1/4}`.

These never coincide (`8k = 7 + 6j` has no solution; checker C7), so the two families cannot resonate with each other.
That alone does not exclude logarithms from later integrals: `∫_h^1(h/t)dt = h log(1/h)` is `O(h^{3/4})` and sits at the
fold family's exponent `1` (Slice E review 5387084565, E-SCOPE-01). A further scale `t ≍ h^{1/5}` appears where the
quintic jet competes and `m ≍ E₂`. There the model kernel loses relative order one, which by power counting contributes
order `h^{4/5}`. So, formally, the exponents after `1/3` are `3/4`, then `4/5`, then `1`. This is a power-counting
conjecture. A full later expansion is not proved here, and nothing here shows that the actual densities have a nonzero
`h^{4/5}` term or no logarithms beyond `h^{3/4}`.

On sharpness, [1D] §6.2 records that for the Gaussian kernel the `θ = 1/3` sign-kernel remainder after three terms is
`≈ 0.038h^{3/4}`, constant over `h = 10^{−10}, …, 10^{−26}`; a referee recomputed `0.0381`. This is evidence only that
the `θ = 1/3` sign-kernel integral has a nonzero `h^{3/4}` term for that kernel. It does not show that a nonzero
`h^{3/4}` term survives in `ν`, where Proposition M's misclassified mass is of the same order, or in `ν₊`; neither is
examined here.

**5.2 Where the parity enters.** Without the independence of `(φ₋, φ₊)` from `φ_G`, the misclassified mass can only be
bounded by the probability that `φ_G` lies within the edge fluctuation, `O(t/κ)` relative. That is [1D]'s `O(h^{1/2})`.
Three facts make the first order a mean:
- the regression of Lemma Φ, which is exact for Gaussian fields;
- the independence of `E₂` (odd) from `φ_G` (even), which makes the weight a function of `φ_G` given `ω` ([1D] Remark
  1.4);
- the evenness of `W` and `p_s`, which reduces the first order to the window length (3.3).

The mean of the first-order part is `O(t²)`. The even remainder is centered and cancels, `Ê = O(t²)`, and the odd
part's mean `E_QO(3/2)` comes from `E[f^{(5)} | pins] ∝ α`. For the Gaussian kernel, `E_QO(3/2) = −6t²(1 + O(t²))`:
`E[a₅ | a₁ = 0, a₃ = α] = −10α`, and `O(3/2) ≈ a₅t⁵/(20h)`, since the odd profile `X(X² − ¼)²/120` equals `1/20` at
`3/2` (checker C3).

**5.3 `d ≥ 2`.** The elder window of Math- #207, #220 and #229 is the same one-dimensional window `|φ| < 1/3` along each
transverse fiber, and Lemma W is a statement on one fiber. It is open whether Proposition M lifts to an elder density in
`d ≥ 2` with remainder beyond `ℓ^{3/7}` (#229), as Math- #237 (open, author-side) proposes for the candidate density. The
transverse dependence of the edges and the far elder density would have to be controlled. This note claims nothing in
`d ≥ 2`.

**5.4 Numerical evidence (exploration, outside the repository).** These checks use numpy, scipy and mpmath, and are
archived with the project record.

- *Lemma E.* By 200-node Gauss–Hermite quadrature, `(G_θ − g_θ)/(v₂ min(1, s))` stays in `(0, 1.60]` for `θ = 1` and in
  `(0, 1.00]` for `θ = 1/3`, on `s ∈ [0.01, 12]` and `v₂^{1/2}/v₁^{1/2} ∈ [s/256, s/8]`. As `s → 0` the `θ = 1` ratio
  tends to `4/√(2π) ≈ 1.596`.
- *The edge scaling: setup.* The model is a degree-40 truncation of the series of the Gaussian-kernel process,
  `f(x) = e^{−x²/2}Σ_{n ≤ 40}ξ_nx^n/√(n!)`. Its covariance is `e^{−(x²+y²)/2}Σ_{n≤40}(xy)^n/n!`, not the stationary kernel
  `e^{−(x−y)²/2}`: at `x = y = 1` its variance falls short of `1` by more than `1/(3·41!)` (Slice E review 5387084565,
  E-SCOPE-02). This finite model is conditioned exactly on the pins (Matheron's formula, coefficients at 60 digits); that
  does not make it the stationary process, and no truncation, rounding or sampling error bound is certified. The edges
  `φ±` are found by bisection, and `Δ` is integrated in closed form in `φ_G`. The table gives
  `E[Δ]/E[∫_{−1/3}^{1/3}Wp_s]`, divided by `t²`.

  | `t` | samples | `s = 2` | `s = 1` |
  |---|---|---|---|
  | 0.2 | 4·10⁴ | `−0.285 ± 0.018` | `+0.214 ± 0.040` |
  | 0.1 | 4·10⁴ | `−0.274 ± 0.036` | `+0.222 ± 0.080` |
  | 0.05 | 1.6·10⁵ | `−0.367 ± 0.036` | `+0.270 ± 0.080` |
  | 0.025 | 6.4·10⁵ | `−0.272 ± 0.036` | `+0.266 ± 0.080` |

- *The edge scaling: findings.*
  - A first-order term `∝ t` would make these ratios grow by a factor `8` over this range; they stay flat.
  - A referee's independent reduced leading-order model predicts the `t → 0` limits `+0.164` (`s = 1`) and `−0.308`
    (`s = 2`). The tabled values for `t ≤ 0.1` are consistent with these (`χ² ≈ 3.7` and `4.7` on 3 degrees of freedom).
  - In that model the mean part and the fluctuation part have opposite signs at both `s`. Their sizes differ: `−0.36` and
    `+0.52` at `s = 1`, `−0.32` and `+0.01` at `s = 2`. This explains the sign change.
  - In the finite model, the conditional values are `E_QO(3/2)/t² = −5.841, −5.960, −5.990, −5.997` and
    `Ê(3/2)/t² = −12.88, −13.12, −13.18, −13.19` at `t = 0.2, 0.1, 0.05, 0.025`, with limits `−6` and `−13.2`.
  - For `t ∈ {0.1, 0.05}`, a direct grid decision with `φ_G` sampled agreed with `1{φ₋ < φ_G < φ₊}` on all `3.3·10⁵`
    typed samples.
  - At `t = 0.2` there were 12 and 102 mismatches, where `t/κ ≥ 1.3`.
  - The constants are large. For instance `‖Ê‖_{C²}/τ² ≈ 2.6·10³` for the Gaussian kernel, so Lemma W's smallness
    condition is reached only at small `t`.
- *Lemma W.* At 40 digits, `(φ₊ − 1/3 + η_{1/3}(−3/2)/12)/ε²` converges as `ε = 10^{−2}, 10^{−3}, 10^{−4}`: to `0.0833`
  for `η⁰ = εX(X² − ¼)²` (odd) and `0.750` for `η⁰ = ε(X² − ¼)²(X² + ½)` (even). With a `φ`-dependent profile, (3.3)
  held to `1.1ε²`. Checker C5 repeats this with the standard library at `ε = 10^{−3}, 10^{−4}, 10^{−5}`.
- *Lemma W (W.1), by a referee.* A direct arc and persistence decision agreed with the interval structure in about
  `2.5·10⁵` typed decisions at `C²` norm `≤ 0.5`, for random perturbations satisfying the hypotheses.

## 6. Sources (exact identities in `SOURCES.json`)

**Consumed.** [1D] = Math- #214, `frontiers/d1_third_order_law_20261001/PROOF.md`, blob `1591ecee` at head
`54666d26e1…` (v1.3; open; bound by the workflow's drift gate). The v1.1 blob `873532b9` differs from the v1.2 blob
`3389ef8c` in labels only. v1.3 applies the clarifications its reviewers requested, listed below. It supplies:
- §0: the setting and constants;
- §1: Lemmas 1.1–1.3, the canonical versions (1.2)–(1.3), (1.4) and Remark 1.4;
- §2: the sign kernels, `γ_θ`, `ζ_θ`, Lemma 2.1, Prop. 2.2 (b)–(e), and the intermediate estimates in its proof of
  (c)–(d);
- §3: Lemma 3.1, Lemma 3.2's window field `𝔉`, the model (3.1) and Lemma 3.3;
- §4: Lemmas 4.1–4.3;
- §5: the adjacency argument.

*The acceptance boundary of [1D].* Its nonauthor acceptance (OpenAI Codex, comment 5933752065, carried to v1.2 by comment
5941929764) binds the manuscript together with the supplementary derivations in comments 5930841283, 5931058934 and
5933752065. Its four listed clarifications are in v1.3's text:
- `f_o(τ) = −h/2` in Lemma 3.2;
- `0 ≤ α ≤ τ^{−1}` for the relative density expansion of Lemma 1.3;
- Lemma 4.3's band bound on `[t₁, t₀]` with the explicit `√log` cutoffs, `O(h(log(1/h))^{3/2})`;
- the global-maximum alternative in the negative case of Lemma 3.3.

This note uses [1D] with these clarifications, in particular Lemma 4.3's `O(h^{3/4})` through that logarithmic
calculation. [1D]'s Slice E review (5387031124) accepted the coefficient comparison and the public controls, and its
attribution amendment is applied in v1.3. The review does not cover [1D]'s outside-repository exploration, and none of it
is used here.

**Cited only.**
- Math- #237 (`frontiers/candidate_parity_rate_20261001/PROOF.md`, open): the `d ≥ 2` parity argument for the candidate
  density, for comparison (§5.3).
- Math- #207 (merged; `frontiers/cusp_second_order_20261001/PROOF.md`), #220 (`frontiers/elder_third_order_20261001/PROOF.md`)
  and #229 (`frontiers/third_order_rate_20261001/PROOF.md`), both merged on 1 October with the pinned blobs: the elder
  window and densities in `d ≥ 2` (§5.3).

External: Sudakov–Fernique and Borell–TIS (as used in [1D] Lemma 4.3); Gaussian regression.

## 7. Exact controls

`d1p_check.py` uses the standard library: exact rationals for C1–C4 and C7, `Decimal` at 60 digits for C5, and float
quadrature, reported to 6 digits, for C6. Its output is `RESULTS.json`, byte-identical under `-O`. Mutants `M1`–`M7` each
fail their own control and exit 1; the failure message names the control, and the workflow checks it. An unknown or bare
label exits 2.

| Control | Checks |
|---|---|
| C1 | The model's parity split, `g_φ = (2X³ − (3/2)X) + (3φ(X² − ¼)² − ½)`, and the mirror symmetry `g(−X, −φ) = −1 − g(X, φ)`. The edge functions (3.2): `Γ_±`, `Γ₊ − Γ₋ = 1`, `Γ₋(φ) = −Γ₊(−φ)`, the derivative `3(1 − φ²)²/(16φ⁴)` and the slope `12` at `±1/3`. These are rational-function identities, verified at 200 rational points within degree bounds. Also `g''(X₃) = 3(1 − φ²)/φ`. |
| C2 | The margins of Lemma W on `J_±`, exactly: `g(−2) ≥ 9/64`; `g(2) + 1 ≤ −9/64`; `g''(X₃) ≥ 7.7` and `g'' ≥ 5.1` within `1/20` of `X₃`; `Γ₊ ≤ 0.12` on `J₊`; `12φ(X² − ¼) ≥ 2.9` on `[−2, −1]`; the bounds on `|g'|`; the right-side factorization; `X₃ ∈ [−1.55, −1.45]`; and the quadratic-growth factor `3φX² − X + (1 − 6φ²)/(4φ) ≥ 2.24` on `[−2, −1] × J₊`. The last is checked as a polynomial identity, together with monotonicity in `X` and `φ` and the value at the corner. |
| C3 | The pin algebra of Lemma Φ, as polynomial identities: `H₀`; the Hermite basis `p₁`, `p₂`; the even pin identity and `E₁ = a₄τ²/3 + ρ₁`; the odd profiles `X(X² − ¼)²/120` and `X(X² − ¼)²(2X² + 1)/10080`; the even profiles `(X² − ¼)²/24` and `(X² − ¼)²(X² + ½)/720`. Also, as scalar arithmetic, the leading regression constant `3`, and for the Gaussian kernel `E[a₅ | a₁ = 0, a₃ = α] = −10α`, giving the leading `E_QO(3/2) = −6t²`. |
| C4 | A bookkeeping check of (3.3), for random rational odd/even polynomials vanishing to second order at `±½`: the even part cancels from the window length. |
| C5 | (W.2)–(W.3) numerically. The edges `φ±` are computed at 60 digits (Newton for the critical point, bisection in `φ`) for four perturbation shapes (odd, even, mixed with a `φ`-profile, generic). Here `ε` is the shape coefficient, not Lemma W's `ε`, at `ε = 10^{−3}, 10^{−4}, 10^{−5}`. It checks that the edge errors are `≤ 10ε²`, the window-length error is `≤ 20ε²`, and the ratios to `ε²` stabilize to 2%. Observed: the edge errors are at most `1.25ε²` and the length error at most `1.5001ε²`. For the odd shape the ratios tend to `±1/12` and `1/6`, for the even shape to `±3/4` and `3/2`. It does not test (W.1). |
| C6 | Lemma E numerically, on a 16-point grid: `(G_θ − g_θ)/v₂` by composite Simpson quadrature, the bound `0 ≤ · ≤ 2 min(1, s)`, and the small-`v₂` limits. |
| C7 | The ledger. Checked: `∫₀^∞t² min(1, h/t⁴) = (4/3)h^{3/4}`, by scaling to `h = 1` and evaluating the exact antiderivatives `u³/3` and `−1/u` of the two pieces; `3 − 11/(5 − δ) ≥ 3/4` iff `δ ≤ 1/9` (`37/49` at `δ = 1/10`); the integrability exponent `−3/4` of Proposition M; the disjointness of the fold and cusp exponent sets, `{−1/3 + 2k/3}` and `{1/4 + j/2}`. Recorded only: the heuristic quintic-scale exponent `4/5` of §5.1 and [1D]'s exponents. |

What the controls do not test: Lemma E's proof, Lemma Φ's estimates, Lemma W's perturbation argument, (W.1),
Proposition M and the assembly are proved in prose only. C5 and C6 are numerical consistency checks, not proofs.

## 8. Review slices

- **A** §1–§2: Lemma E and Proposition 2.2⁺ (the refined `E₂`-correction, the tail of the model kernel, the model
  integral to `t₀`).
- **B** §3.1: Lemma Φ (the regression, the decomposition (3.1), the estimates (Φ.1)–(Φ.4)).
- **C** §3.2: Lemma W (the edges, the margins, the envelope bound, (3.3)).
- **D** §3.3–§4: Proposition M and the assembly, including the bad event and the integrals.
- **E** §5 and the controls.
