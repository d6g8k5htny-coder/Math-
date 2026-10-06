## QS addendum A3.1: the `d ≥ 3` torus lift, the H0 partner, and an order-`r` window certificate

**Object.** `CL-QS-A3-1-TORUS-H0-WINDOW-20261003-v1`.

**Who.** Anthropic Claude, in session `session_01NMeKEismAyeqgdB4sy2NJU`, acting for Dylan Roy (Dylan Roy — delegated AI work). It is the author of:
- QS ([5961415030](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5961415030));
- A1 and A2;
- A3 ([5970263575](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5970263575)).

**Claim.** [5970374887](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5970374887). This is author-side and deterministic. Scientific effect: NONE.

**Consumed (read, not edited):**
- **A3:** Lemma SR, Theorems QS-E′_d and QS-R_d, and the notation of A3 §0.
- **C95**, [5964938563](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5964938563), §§5–6 ((G13)–(G14), the covering argument). Its review is [5965062739](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5965062739).
- **C96**, [5965141133](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5965141133), §1, the deterministic lemma. Its review is [5965199940](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5965199940).
- **[P]**, Math- `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`:
  - §1: the setting, for any `d ≥ 2`, and the weight `W_r`;
  - §8: the Morse locus and the Borel elder event.
- **#242** (landed), Math- `frontiers/soft_rejected_pairs_20261002/PROOF.md`:
  - §2: (2.1), Proposition 2′ with (2.6), and the remark "Consistency with Theorem 1".
- **#243** (landed), Math- `frontiers/soft_fold_limit_20261002/PROOF.md`:
  - §0: the eigenframe, the jets (0.2) and the chart (0.4);
  - Lemma FL.1 and its proof;
  - Proposition FL.4 and §6.
- **#175** (merged), Math- `frontiers/concave_fibre_elder_20260930/`: Theorem H (`PROOF.md`) and the hard-fibre lemma.
- **QS §1:** `μ`, `m_S`, `ε_M`, `κ_•` and `J_•`.
- **QS §7:** the raw identity `G_k(X, ζ) = P(X + γζ/12, γζ)`.
- **A2 Corollary 9(b):** the raw radius.

**What this adds.**
1. **Lemma TL_d.** This is C95 (G14) in every dimension.
2. **Lemma N_d and Corollary H_d.** These give the global ordinary superlevel elder partner of `M_r` under A3's explicit hypotheses, on [P] §8's Morse locus:
   - under QS-E′_d, the partner is `S_r`;
   - under QS-R_d with `W_r > 0`, it is not.

   #175 Theorem H already identifies the actual partner in `d ≥ 3` at a fixed target, for all sufficiently small `r`. With items 1–2, the first two non-claims of A3 §6 are addressed (author-side; pending review).
3. **Lemma FL.1′.** #242 Proposition 2′ (2.6) isolates the `r^{1/2}` term `r^{1/2} Σ_i η_i a_i(X, ζ)` with explicit `a_i` and an `O(r)` remainder. FL.1′ states (2.6) with #243 FL.1's quantitative `C²` remainder, `O(‖f‖_{C⁵} r)`. FL.1 itself places the `r^{1/2}` term in its error, which gives `ϑ(r) = r^{1/2}`.
4. **Lemma SR′ and Theorem C_d.**
   - #242 §2's "Consistency with Theorem 1" computes formally that maximizing the `γ`-part of this term over `η` contributes at order `r`.
   - Lemma SR′ makes this rigorous with explicit bounds. The reduced height is then `O(r)`-close to `P` in `C²`.
   - Theorem C_d is a certificate for the actual torus decision in `d ≥ 3`. Its margins are QS-type and explicit, its error budget is any computable bound, and its orders are those of `d = 2`.
   - It is a fixed-`k` deterministic ingredient of the quantitative-margin input that #243 §6 names as missing.
5. **Remark M.** The certificate depends on the frame only through sign-free, rotation-invariant quantities. These are Borel on `{λ_1 < λ_2}`.

### 0. Setting

- **Field and pins ([P] §1).** Fix `d ≥ 3`, `L > 0` and `X := ℝ^d/(Lℤ^d)`, with quotient `π: ℝ^d → X`.
  - The pins are `M_r = −(r/2)u` and `S_r = (r/2)u`, at heights `b` and `b − kr³`, with zero gradients and `k > 0`.
  - The weight is `W_r = |det H_M det H_S| 1{H_M < 0, index H_S = d − 1}`.
- **Maximin on the torus (C95 (G13)).** `D_f(M_r) := sup{min_t f(ω(t)) : ω continuous in X, ω(0) = M_r, f(ω(1)) > b}`, with `sup ∅ = −∞`. The quantity `d_g(M̂)` is A3's maximin over continuous paths in `ℝ^d`.
- **Eigenframe and jets (#243 §0, #242 §2).**
  - `A := D²_Θ f(0)` is the transverse Hessian at the midpoint. The eigenvalues of `−A` are `λ_1 ≤ λ_2 ≤ ⋯ ≤ λ_{d−1}`, with orthonormal eigenvectors `e_1, …, e_{d−1}`, and `λ̃ := kλ_1/r`.
  - The soft jets are `γ, B, C_3` of (0.2). For the hard indices `i ≥ 2`, put `γ_i := ∂_u²∂_{e_i}f(0)`, `β_i := ∂_u∂_{e_1}∂_{e_i}f(0)` and `ν_i := ∂²_{e_1}∂_{e_i}f(0)`.
- **Chart.**
  - `Φ(X, ζ, η) := rXu + rkζe_1 + r^{3/2} Σ_{i≥2} η_i e_i` and `𝔉 := (f∘π∘Φ − b)/(kr³)` (#243 (0.4)).
  - With `γ ≠ 0`, use QS §7's planar coordinates, `X = u − Z/12` and `ζ = Z/γ`, and put `g(u, Z, η) := 𝔉(u − Z/12, Z/γ, η)`.
  - So `η ∈ ℝ^{d−2}` plays the role of A3's hard variable `z`. The pins are `M̂ = (−½, 0, 0)` and `Ŝ = (½, 0, 0)`.
  - `Ψ(u, Z, η) := Φ(u − Z/12, Z/γ, η)` is an invertible affine map of `ℝ^d` when `γ ≠ 0`, `k > 0` and `r > 0`.

### 1. Lemma TL_d (the torus lift in every dimension)

**Statement.** Let `d ≥ 1`, `f ∈ C(X)`, `x₀ ∈ X` and `b := f(x₀)`. Let `Ψ: ℝ^d → ℝ^d` be an invertible affine map, let `ŷ` satisfy `π(Ψ(ŷ)) = x₀`, and let `σ > 0`. Put `g := (f∘π∘Ψ − b)/σ`. Then

    D_f(x₀) = b + σ d_g(ŷ),        with  b + σ(−∞) := −∞.                                                     (TL)

*Proof.*
- `p := π∘Ψ` is a covering map: `π` is a covering and `Ψ` is a homeomorphism.
- Every continuous path `ω` in `X` from `x₀` has exactly one lift `ω̂` from `ŷ`, meaning `p∘ω̂ = ω`. Conversely, every path `ω̂` from `ŷ` is the lift of `p∘ω̂`. So `ω ↔ ω̂` is a bijection between the path families, before any endpoint condition is imposed.
- Along corresponding paths, `f∘ω = b + σ g∘ω̂`. Hence `f(ω(1)) > b` holds exactly when `g(ω̂(1)) > 0 = g(ŷ)`, and `min f∘ω = b + σ min g∘ω̂`.
- The map `t ↦ b + σt` is increasing and commutes with suprema, including the empty one. ∎

This is C95's argument for (G14), and it does not use `d = 2`. Neither injectivity of `p` on a window nor the embedding `2rw ≤ L/4` is needed: windows may wrap around the torus and paths may wind.

**Applied here** with an invertible affine `Ψ` such that `π∘Ψ` maps `M̂` to `M_r` and `Ŝ` to `S_r`, and with `σ = kr³`:

    D_f(M_r) = b + kr³ d_g(M̂).

### 2. Lemma N_d (pin types)

**Hypotheses.**
- A3's (B1)–(B2) hold on `Ω × B̄_ε` with `M, S ∈ Ω`.
- The pins are exact.
- (E2_d) holds at `S` and (E3_d) holds at `M`. Only the values at these two points are used.

**Conclusion.** `M̂` is a nondegenerate local maximum of `g`, of Morse index `d`. `Ŝ` is a nondegenerate critical point of index `d − 1`. The same holds for `f` at `M_r` and `S_r`.

*Proof.* Inertia `In = (n₊, n₋, n₀)` counts positive, negative and zero eigenvalues.
1. **The reduced Hessian at `S`.**
   - By QS §§1 and 3, `D²P(S) = diag(6, −2κ_S)` and `J_S = diag(1/√3, 1/√κ_S)`, so `J_S D²P(S) J_S = diag(2, −2)`.
   - By Weyl's inequality and `‖J_S D²e_G(S) J_S‖ ≤ 2/5`, the eigenvalues of `J_S D²G(S) J_S` lie in `[8/5, 12/5] ∪ [−12/5, −8/5]`, one in each.
   - By Sylvester's law, `In D²G(S) = (1, 1, 0)`.
2. **The reduced Hessian at `M`.** Here `J_M D²P(M) J_M = −2I` and `‖J_M D²e_G(M) J_M‖ < 1`, so `In D²G(M) = (0, 2, 0)`.
3. **The full Hessian.**
   - At the pins `ζ = 0` (SR(e)). So by SR(d), `D²G` is the Schur complement of `g_zz` in `D²g` at `(S, 0)`, and likewise at `(M, 0)`.
   - Haynsworth's inertia additivity gives `In D²g = In g_zz + In D²G = (0, m, 0) + In D²G`, with `m = d − 2`.
   - Hence `In D²g(Ŝ) = (1, d − 1, 0)` and `In D²g(M̂) = (0, d, 0)`.
4. **Transfer to `f`.** We have `f∘π∘Ψ = b + kr³ g` with `Ψ` affine, so `kr³ D²g = DΨᵀ (D²f) DΨ` at the pins. Sylvester's law applies again. ∎

### 3. Corollary H_d (the actual torus decision and the H0 partner)

**Setting.** Use [P] §1 with `d ≥ 3`, and let `f ∈ C²(X)` have the exact pins. Let `g := (f∘π∘Ψ − b)/(kr³)`, where `Ψ` is any invertible affine map such that `π∘Ψ` maps `M̂` to `M_r` and `Ŝ` to `S_r`. §0's chart is one such map. It needs `f ∈ C³`, so that `γ` and the eigenframe are defined, and `γ ≠ 0`.

**(E) Elder side.** Suppose `g` satisfies the hypotheses of A3's Theorem QS-E′_d.
- Then `D_f(M_r) = b − kr³ = f(S_r)`, and `M_r` is not a global maximum of `f`.
- If also `f` is Morse with distinct critical values, then the finite ordinary-superlevel H0 class born at `M_r` dies at `S_r` under the elder rule. Its bar is `(b − kr³, b)`.

**(R) Rejected side.** Suppose `g` satisfies the hypotheses of QS-R_d.
- Then `D_f(M_r) > f(S_r)`.
- Suppose also that `f` is Morse with distinct critical values, that `M_r` is a local maximum, and that `S_r` has index `d − 1`. The last two hold on `{W_r > 0}`. Then the class born at `M_r` does not die at `S_r`. That is, the global ordinary elder partner of `M_r` is not `S_r`.

*Proof.*
1. **The maximin statements.** (TL) turns the maximin conclusions of QS-E′_d and QS-R_d into these statements.
2. **Not a global maximum.**
   - In (E), the lifted axis path of QS-E′_d's step 4 ends where `g > 0`. Its projection therefore ends where `f > b`.
   - In (R), the lifted chord does the same.
3. **The H0 statements.**
   - Apply C96's deterministic lemma with `X = T^d_L`, which is a compact connected smooth manifold.
   - In (E), Lemma N_d makes `M_r` a local maximum and gives `S_r` index `d − 1 = dim X − 1`. In (R) these are hypotheses.
   - In both cases `f(S_r) < f(M_r)`.
   - In (E), the lemma's implication (1) ⇒ (2) gives the conclusion. In (R), the contrapositive of (2) ⇒ (1) does. ∎

**The Morse hypothesis costs no mass.**
- [P] §8 proves, in every `d ≥ 2` and at each fixed `r`, that the pinned field is `Q_r`-almost surely Morse with distinct critical values. By absolute continuity this also holds `Q_r^W`-almost surely.
- [P] §8 also proves that `{d_f(M) = f(S)}` is Borel.
- [P] §8 already records that, on that locus, this maximin equality "expresses ordinary elder death at S". C96 proves this at the present convention.

**In [P]'s terms, on the Morse locus.** Consider the event that the global elder partner of `M` is `S`, whose `Q^W`-probability is `p_r`.
- It contains the set where QS-E′_d's hypotheses hold.
- It is disjoint from the set where QS-R_d's hypotheses hold and `W_r > 0`.

**Prior work.** #175 Theorem H proves a qualitative counterpart in `d ≥ 3`. At a fixed target, for every sufficiently small `r`, it gives `d_f(M) = b + r³h_r` and identifies the actual elder partner on the Morse locus. Corollary H_d differs in two ways:
- its hypotheses are the explicit ones of A3;
- it uses the torus lift rather than an embedded barrel.

### 4. Lemma FL.1′ (#242 (2.6) with FL.1's quantitative `C²` remainder)

**Hypotheses.** Those of #243 Lemma FL.1, with `d ≥ 3` and `r ≤ min(1, r₀)`:
- `w ≥ 1` and `0 < k_− ≤ k ≤ k_+`;
- `r₀ = r₀(d, w, k_+, L)` as in FL.1;
- `f ∈ C⁵(X)` with the pins;
- the eigenframe of `A`.

Put `N := ‖f‖_{C⁵}` and, for each hard index `i ≥ 2`,

    a_i(X, ζ) := (γ_i/(2k))(X² − ¼) + β_i Xζ + (k/2) ν_i ζ².

This is #242's `G_{1/2} = Σ_i a_i η_i` in (2.6).

**Conclusion.** On `𝒲_w := {|X| ≤ w, |ζ| ≤ w, |η| ≤ w}`,

    ‖𝔉 − G_k^{(d)} − r^{1/2} Σ_{i≥2} η_i a_i‖_{C²(𝒲_w)} ≤ C′ N r,        C′ = C′(d, w, k_±).                       (FL.1′)

*Proof.* Follow FL.1's proof, but keep the `|l| = 1` monomials apart; this is #242's grouping in its proof of (2.6). The `|l| = 1` monomials with `ex < 1` are as follows.
- **`i + j = 0`.** The transverse pins give `∂_{e_i}f(0) = −(r²/8)γ_i + O(Nr⁴)`. These terms contribute `−(r^{1/2}/(8k))γ_i η_i + O(Nr^{5/2})`.
- **`i + j = 1`.** The pins give `∂_u∂_{e_i}f(0) = O(Nr²)`, and the eigenframe gives `∂_{e_1}∂_{e_i}f(0) = 0`. These terms contribute `O(Nr^{3/2})`.
- **`i + j = 2` (`ex = ½`).** The Taylor coefficients of `x²y_i`, `xy_1y_i` and `y_1²y_i` are `γ_i/2`, `β_i` and `ν_i/2`. These terms contribute `r^{1/2} η_i [(γ_i/(2k))X² + β_i Xζ + (k/2)ν_i ζ²]`. FL.1 bounded them only by `O(Nr^{1/2})`.

The terms with `i + j ∈ {0, 2}` add up to `r^{1/2} η_i a_i(X, ζ)`. Everything else is as in FL.1:
- the `|l| = 1`, `i + j = 3` monomials (`ex = 3/2`), and every monomial with `ex ≥ 1`, are `O(Nr)`;
- the `|l| = 0`, `i + j ≤ 3` monomials give `G_k + O(Nr)`;
- the `|l| = 2`, `i = j = 0` monomials give exactly `−(1/(2k)) Σ λ_i η_i²`;
- the remainder `ρ₅` is `O(Nr²)` in `C²`.

Each of these is a bound on derivatives up to order 2 on the bounded window. The value `r ≤ 1` absorbs `r^{3/2}` and `r^{5/2}` into `r`. ∎

**Remarks.**
- `a` is an explicit quadratic in `(X, ζ)`. Its coefficients are third derivatives of `f`, so `|a|`, `‖Da‖` and `‖D²a‖` can be computed from the jets and are at most `c_a(d, w, k_±) N` on `𝒲_w`.
- So FL.1's `r^{1/2}` in `d ≥ 3` comes entirely from the odd term `r^{1/2} η·a`. This is A3 §4's hard gradient, written in the `r^{3/2}` scaling.
- #242 (2.6) and #243 §5 already identified this term. #243 §5 observed that it moves the pin Hessians only at order `r`. Lemma SR′ shows that it moves the reduced height, and hence the decision, only at order `r`.

### 5. Lemma SR′ (comparison with a separable model)

**Setting.** Let `Ω ⊂ ℝ²` be open, and suppose that on a neighbourhood of `Ω × B̄_ε ⊂ ℝ² × ℝ^m`

    g(x, z) = P(x) − ½ zᵀQz + s z·a(x) + E(x, z).

Here `Q` is constant and symmetric with `Q ⪰ Λ₀I`, `s ≥ 0`, `a ∈ C²(Ω; ℝ^m)` and `E ∈ C²`. Let `δ₀, δ₁, δ₂, α₀, α₁, α₂` be any upper bounds for the following suprema:
- `δ₀ ≥ sup|E|`, `δ₁ ≥ sup|E_z|` and `δ₂ ≥ sup max(‖E_zz‖, ‖E_xz‖, ‖E_xx‖)`, all over `Ω × B̄_ε`;
- `α₀ ≥ sup|a|`, `α₁ ≥ sup‖Da‖` and `α₂ ≥ sup_x sup_{|e|=1} ‖D²(e·a)‖`, all over `Ω`.

Let `0 < Λ ≤ Λ₀ − δ₂`.

**Statement.** Suppose `sα₀ + δ₁ < Λε/2`. Then (B1) and (B2) hold with this `Λ`. Moreover, with `e_G := G − P`,

    |e_G| ≤ δ₀ + (sα₀ + δ₁)²/(2Λ),                                                              (SR′0)
    ‖D²e_G‖ ≤ δ₂ + sα₂(sα₀ + δ₁)/Λ + (sα₁ + δ₂)²/Λ.                                              (SR′2)

*Proof.*
1. **(B1) and (B2).** First, `g_zz = −Q + E_zz ⪯ −ΛI`. Second, `q₀(x) = |s a(x) + E_z(x, 0)| ≤ sα₀ + δ₁ < Λε/2`.
2. **(SR′0).** SR(b) gives `0 ≤ G − g(·, 0) ≤ q₀²/(2Λ)`, and `g(x, 0) − P(x) = E(x, 0)`.
3. **(SR′2).**
   - SR(d) gives `D²G = g_xx − g_xz g_zz⁻¹ g_zx` at `(x, ζ(x))`.
   - `g_xx(x, z) = D²P(x) + s Σ_j z_j D²a_j(x) + E_xx(x, z)`, since `−½zᵀQz` does not depend on `x`.
   - Hence `‖g_xx(x, ζ) − D²P(x)‖ ≤ sα₂|ζ| + δ₂`, with `|ζ| ≤ q₀/Λ` by SR(a).
   - Finally `‖g_xz g_zz⁻¹ g_zx‖ ≤ ‖g_xz‖²/Λ`, with `‖g_xz‖ ≤ sα₁ + δ₂`. ∎

**What is gained over SR(d).** The `z`-dependence of the model part of `g_xx` is explicit and linear, with slope at most `sα₂`. `E` enters only through `δ₂` at the point `(x, ζ(x))`. So SR′ needs no `z`-Lipschitz constant `N₃` of `D²_x g`, which here would require a `C³` bound on `E`.

**The bounds are sharp.** The referee below found a quadratic-fibre family that attains both.

### 6. Theorem C_d (an order-`r` window certificate in `d ≥ 3`)

**Hypotheses.**
- **Setting.** [P] §1 with `d ≥ 3` and `k ∈ [k_−, k_+]`. The field `f ∈ C⁵(X)` has the exact pins, and `r ≤ min(1, r₀)`.
- **Jets.** `λ̃ > 0`, `γ ≠ 0`, `λ_2 > 0` and `ψ > |c|`, where `(ψ, c, R)` come from the jets by QS §7. The numbers `μ`, `m_S`, `ε_M` and `κ_•` are QS §1's, for this `P`.
- **Windows.**
  - `ε := 4√(k/λ_2)`.
  - `ρ_E := 3/2 + (5/2)(|γ| + 12)/√(24λ̃)` (A2 Corollary 9(b)) and `ρ_R := 5/2 + (17/6)(|γ| + 12)/√(24λ̃)`. The latter is the same computation for `𝔚_R`; see R1 below.
  - A window size `w` with `w > ρ_•` and `w ≥ ε`, and `Ω := {(u, Z) : |(X, ζ)| < w}`.
- **Error budget.**
  - `E := g − P + (1/(2k)) ηᵀ diag(λ_2, …, λ_{d−1}) η − r^{1/2} η·a`, in the `(u, Z, η)` chart.
  - `δ` is any number with `δ ≥ max(δ₀, δ₁, δ₂)` for this `E` on `Ω × B̄_ε`, as in SR′.
  - `α_j` are any upper bounds for the norms of `a` in the `(u, Z)` chart, as in SR′. They can be computed from the jets.
- **Derived quantities.**

      Λ := λ_2/k − δ,    Ξ₀ := δ + (r^{1/2}α₀ + δ)²/(2Λ),    Ξ₂ := δ + r^{1/2}α₂(r^{1/2}α₀ + δ)/Λ + (r^{1/2}α₁ + δ)²/Λ.

- **Barrel inequalities (both sides).** Assume `δ < λ_2/(2k)` and `r^{1/2}α₀ + δ ≤ √(λ_2/k)`.

**(E) Elder side.** Use `w > ρ_E`. Suppose:
- `μ < 0`, with QS's convention `|μ| := ∞` when there is no extra saddle;
- `Ξ₀ < min(|μ|, m_S, ε_M)`;
- `Ξ₂ ≤ (2/5) min(3, κ_S)` and `Ξ₂ < min(3, κ_M)`.

Then:
- `D_f(M_r) = f(S_r)`;
- `M_r` and `S_r` have Morse indices `d` and `d − 1`;
- on the Morse locus, the global ordinary elder partner of `M_r` is `S_r`.

**(R) Rejected side.** Use `w > ρ_R`. Suppose `0 < μ < 1` and `Ξ₀ < min(μ, 4(1 − μ))`. Then:
- `D_f(M_r) > f(S_r)`;
- on the Morse locus intersected with `{W_r > 0}`, the global ordinary elder partner of `M_r` is not `S_r`.

Here `μ < 1` is automatic (QS §1), and the chord `K` lies in `𝔚_R` (A3 §0).

**Orders.** By FL.1′, any `δ ≥ χ_γ C′ N r` is admissible, where `χ_γ := (1 + 1/12 + 1/|γ|)²` (step 1). We also have `α_j ≤ χ_γ c_a N` and `1/Λ < 2k/λ_2`. At fixed `w ≥ max(ρ_•, 4√(k/λ_2))`, this gives

    Ξ₀, Ξ₂ ≤ C″ χ_γ² N(1 + kN/λ_2) r,    with C″ = C″(d, w, k_±).

So the required margins are of order `r`, as in `d = 2` (C94/C95), and not of order `r^{1/2}`. The constants also depend on `λ_2`, `λ̃` and `γ` through `w`, and on `γ` through `χ_γ`.

*Proof.*
1. **The decomposition.**
   - By QS §7, `G_k(X(u, Z), ζ(u, Z)) = P(u, Z)` identically.
   - So `E` is the FL.1′ remainder, written in the `(u, Z, η)` chart.
   - The linear map `(u, Z) ↦ (X, ζ)` has norm at most `1 + 1/12 + 1/|γ|`. So `C²` sizes in `(u, Z, η)` are at most `χ_γ` times those in `(X, ζ, η)`, on the set whose raw image lies in `𝒲_w`.
2. **The barrel.**
   - Put `Q := diag(λ_i)/k ⪰ (λ_2/k)I`.
   - Since `δ < λ_2/(2k)`, we have `Λ > λ_2/(2k)`.
   - (B3): `Λε² > (λ_2/(2k))·(16k/λ_2) = 8`.
   - (B2): `Λε/2 > √(λ_2/k) ≥ r^{1/2}α₀ + δ`.
   - `Ω` contains `𝔚_E` when `w > ρ_E` (A2 Corollary 9(b)), and it contains `𝔚_R ⊃ K` when `w > ρ_R`.
   - `Ω × B̄_ε ⊂ 𝒲_w`, because `ε ≤ w`.
3. **The planar hypotheses.**
   - Lemma SR′, with `s = r^{1/2}` and `δ_j := δ`, gives `|e_G| ≤ Ξ₀` and `‖D²e_G‖ ≤ Ξ₂` on `Ω`.
   - Then `‖J_•D²e_G J_•‖ ≤ Ξ₂/min(3, κ_•)` (A3 §2) gives (E2_d) and (E3_d).
   - Choose QS's tolerance `η_QS ∈ (Ξ₀, min(|μ|, m_S, ε_M))`. Then (H) and (E1_d) hold with `η_QS`.
   - The pins of `g` are exact because those of `f` are.
4. **Conclusion.** A3's QS-E′_d (respectively QS-R_d), with Lemma N_d and Corollary H_d, gives the statements. ∎

**Relation to [P]'s cap route.** As #243 §6 records, [P]'s cap implication decides the partner on `{λ_min(−A_M) > (4/(3k))rM_3², rM_4 ≤ 3k/10}`, in every `d`. Here `A_M` is the transverse Hessian at the pin `M`.
- In midpoint terms this is the stiff regime `λ̃ > (4/3)M_3²`, up to a shift of at most `kM_3/2` in `λ̃`. There the partner is always `S`.
- Theorem C_d addresses the soft layer, `λ̃ = O(1)`, where both outcomes occur.

**Relation to #243 and #175.**
- **Qualitative transfers.** #243 Proposition FL.4 and #175 Theorem H already transfer the decision in `d ≥ 3`.
- **What FL.4 needs.** FL.4's tolerance `ε(ϖ, 𝒬)` is not explicit. With FL.1 in its normalized form (1.3), FL.4 applies once `(λ̃/γ²) max(1, |γ|/λ̃)² · C N r^{1/2} ≤ ε(ϖ, 𝒬)`, for `ϖ ∈ 𝒦`, and with the window containment `W_ϖ × B̄_{R_η} ⊂ 𝒲′`.
- **What Theorem C_d changes.** Its margins are explicit and of QS type. It measures the error after the fibre maximization, where it is `O(r)`.
- **The counterpart in `d = 2`** is QS/A2 + C95.
- **What it covers of #243 §6.** It is a fixed-`k` deterministic ingredient of #243 §6's input (i). That input also needs uniformity from the cusp scale to the fold scale (`k → 0`) and the weighted half; neither is done here (§9).

### 7. Remark M (the frame)

- **The hard frame does not matter.** Take `δ`, `α_j` and `Λ₀` with Euclidean and operator norms. Then the following are invariant under `η ↦ Oη` with `O ∈ O(d − 2)`:
  - the hypotheses (B1)–(B3);
  - Lemmas SR and SR′;
  - Theorems QS-E′_d, QS-R_d and C_d;
  - the quantities `δ`, `α_j` and `Λ₀`.

  The maximin `d_g(M̂)` is invariant too, since the path families correspond bijectively. FL.1′ holds for any orthonormal basis of the hard space `span(e_2, …, e_{d−1})`, which is `A`-invariant, with `Q := −A|_hard/k ⪰ (λ_2/k)I` (not necessarily diagonal). Only the hard subspace matters.
- **The soft direction enters through sign-free quantities only.** Under `e_1 ↦ −e_1`:
  - `ζ ↦ −ζ` and `γ ↦ −γ`, so `Z = γζ` and `X` are unchanged;
  - `ψ`, `c` and `R` are unchanged (as #243 §0 notes for its own parameters);
  - `β_i ↦ −β_i`, so `a` is unchanged as a function of the point.
- **Measurability of the frame.** On the open set `{λ_1 < λ_2}`, the spectral projections of `−A` onto the `λ_1`-eigenline and onto the hard subspace depend continuously on `A`. So the line `ℝe_1` and the hard subspace are Borel functions of `(u, f)`. This addresses A3 §6's "measurable midpoint eigenframe" item.
- **Measurability of the other inputs.** These are Borel as well, by routine arguments not written out here:
  - `N` is a countable supremum;
  - `α_j`, `κ_•`, `m_S` and `ε_M` are continuous in the jets;
  - `μ` is a semi-algebraic function of `(ψ, c, R)`.
- **Still open.** The probability of the eigengap event (§9).

### 8. Checks (exploration outside the repository)

**`a31_exact.py`** (standard library; exact rationals and integers; SHA256 of stdout `a826b265…`):
- **N1, pin types (1,200 checks).** Weyl and Haynsworth on synthetic rational blocks with `m = 1, 2`. This includes the extreme cases `‖E‖ = 2/5` at `S` and `‖E‖ = 96/97` at `M`.
- **F1, FL.1′ bookkeeping (6,001 checks).**
  - The monomials with `ex < 1` are exactly `{|l| = 0, i + j ≤ 3}`, `{|l| = 1, i + j ≤ 2}` and `{|l| = 2, i = j = 0}`.
  - On random rational quartics in `d = 3`, with only the **hard** transverse pins solved symbolically in `s = r^{1/2}`:
    - `[η¹]𝔉 − s a = O(s³)`;
    - `[η²]𝔉 + λ_2/(2k) = O(s²)`;
    - `[η³]𝔉 = O(s³)` and `[η⁴]𝔉 = O(s⁶)`.
- **R1, raw radii (1,600 checks).** The bounds for `ρ_E` and `ρ_R`, checked exactly at the parallelogram vertices.
- **C1, barrel constants (800 checks).** The constants `ε = 4/v` and `Λ = v² − δ` with `v² = λ_2/k`, and `δ` up to `v²/2 − 10⁻⁶`.
- **H1, the discrete analogue of C96's lemma (1,671 local maxima).** These are on periodic grids in `d = 2, 3, 4`. For each local maximum, the union-find elder death equals the bottleneck maximin over all torus paths.
- **Controls.** Five mutants exit 1, an unknown label exits 2, and the output under `-O` is byte-identical.

**`a31_numeric.py`** (numpy).
- **Fields.** Twelve exactly pinned degree-6 polynomial fields in `d = 3`, in the midpoint eigenframe, with `k ∈ [0.3, 2]`, `λ̃ ∈ [0.3, 3]` and `λ_2/k ∈ [1, 4]`.
- **Window.** The raw window `|X|, |ζ| ≤ 2` and `|η| ≤ ε`. This is smaller than Theorem C_d's `Ω`, so it tests the rates, not the certificate on `𝔚_E`.
- **Reduced height.** `G` is computed by a grid scan with Newton refinement in `η`.

Maxima over the 12 fields:

| `r` | `𝔉 − G_k^{(d)}` (FL.1) | `𝔉 − G_k^{(d)} − r^{1/2}η·a` (FL.1′) | `sup|e_G|` | Gershgorin bound on `sup‖D²e_G‖` |
|---|---|---|---|---|
| 0.1 | 8.4 | 3.3 | 1.6 | 4.4 |
| 0.03 | 4.1 | 0.94 | 0.43 | 1.1 |
| 0.01 | 2.2 | 0.30 | 0.14 | 0.37 |
| 0.003 | 1.2 | 0.090 | 0.041 | 0.11 |
| 0.001 | 0.67 | 0.030 | 0.014 | 0.036 |

The first two columns are `C²` sizes. The last uses central differences (step `10⁻³`) on a 9×9 interior grid in the `(X, ζ)` chart.
- **Slopes.** The median log–log slopes over the last step are 0.53, 1.02, 1.00 and 1.00. So FL.1's `r^{1/2}` is attained, and the other three columns are of order `r`.
- **The mechanism.** `(G − 𝔉(·, 0))/r` converges to `k a²/(2λ_2)` (the error at `r = 0.001` is 0.020, falling linearly).
- **SR(b) with the section error.** It held at every grid point. The largest ratio, 1, is attained at the pins, where `q₀ = 0`.
- **QS §7.** Its identity holds to `1.1·10⁻¹⁴`.

**Clean-context referee.** A separate Claude agent in this session, which had not seen the draft, returned **ACCEPT WITH REVISIONS (minor)** with no blocking or major error. It is the same provider and the same session, so this is not review evidence.
- **Its findings.** All 14 were applied before posting:
  - the explicit error budget in C_d (any computable `δ`);
  - "fixed-`k` ingredient" in place of "deterministic half";
  - SR′'s remark, and SR′ with upper bounds;
  - `C³` for §0's chart in H_d;
  - the cap region at `A_M`;
  - FL.4's normalization and conditions;
  - credit to #242 (2.6) and #175 Theorem H;
  - the parameter dependence in "Orders";
  - measurability;
  - notation;
  - descriptions of the checks;
  - "addressed" in place of "closed".
- **Its independent checks** (scripts and logs kept with this record):
  - **(a) Symbolic FL.1′.** General symbolic polynomials, degree ≤ 6 in `d = 3` and ≤ 5 in `d = 4`, with **all** pins and the eigenframe imposed. The residual is `O(r)` coefficientwise and does not depend on the eigenvalues. Six mutants fail.
  - **(b) SR′.** 420 non-quadratic fibres with `m = 1, 2`: 0 violations, and a tight family attains ratio 1.
  - **(c) Scaling.** Three non-polynomial exactly pinned `d = 3` fields in 50-digit arithmetic, `r` from 0.1 to `10⁻⁴`, in the `(u, Z)` chart. FL.1's error has slope ≈ 0.51; FL.1′'s residual, `sup|G − P|` and `sup‖D²(G − P)‖` have slope ≈ 1.00.
  - **(d) Radii.** `ρ_R` is exact, and `K ⊂ 𝔚_R` was re-derived.
  - **(e) End to end.** 100 exactly pinned `d = 3` fields with **measured** `δ_j` and `α_j`.
    - The bounds `sup|e_G| ≤ Ξ₀` and `sup‖D²e_G‖ ≤ Ξ₂` held in all 100, with largest ratios 0.991 and 0.971.
    - There were 30 elder and 40 rejected certificates, with **0** decision mismatches against a 3-D grid maximin.
    - Lemma N_d's inertia held in 30 of 30.
    - The 30 fields without a certificate still followed their model decisions, so the certificate is conservative.

### 9. Not claimed; what is open

- **The weighted half in `d ≥ 3`.** This is the `Q^W`-mass of the complement of Theorem C_d's certificate:
  - near the decision boundary (`μ` near 0 or 1, and `min(m_S, ε_M)` small);
  - on `{λ_2 small}`;
  - on the `C⁵`-norm tails;
  - near the typing edges;
  - where the window grows (`λ̃` small, `|γ|` large, `λ_2/k` small);
  - where the chart factor `χ_γ` grows (`|γ|` small).

  So there is no rate for `1 − p_r` in `d ≥ 3`, and nothing towards #242 Conjecture 7.
- **Uniformity in `k`.** Theorem C_d is for `k ∈ [k_−, k_+]`. It is not uniform as `k → 0`, from the cusp scale to the fold scale, which #243 §6's input (i) needs.
- **Constants.** `C′` and `r₀` are inherited from #243 Lemma FL.1 and are not explicit. The certificate itself takes any computable `δ`.
- **Measurability.** The Borel measurability of the full certificate event is routine but not written out (Remark M).
- **What was open in A3 §6.**
  - The first two items, the torus lift and the H0 identification, are now addressed, author-side and pending review.
  - The third item is addressed except for the probability of the eigengap.
  - The probabilistic items remain open.

**Review request.** A bounded nonauthor read of:
- Lemma FL.1′ (the bookkeeping against FL.1's and #242's proofs);
- Lemma SR′;
- the composition in Theorem C_d;
- Corollary H_d's use of C96 and [P] §8.

Please claim first.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_