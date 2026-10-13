## QS addendum A3.4: the `d = 3` soft-layer jet law at rate `r` under the actual weight (C92 Theorem J and C93 (E1)–(E12) in `d = 3`)

**Object.** `CL-QS-A3-4-SOFT-LAYER-LAW-20261005-v1`.

**Who.** Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`, the author of QS and A3–A3.3. Dylan Roy — delegated AI work.

**Claim.** This delivers the third item of claim [5978801726](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5978801726), the soft-layer measure transfer, renewed in A3.3 ([5998500022](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5998500022)) to 22:00Z, and releases the claim. Author-side. Scientific effect: NONE. The executable and its stdout are in a companion controls comment, posted right after this one.

**Consumed (merged; read, not edited).**
- **[P]** (`imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d`), read with its amendments as the reconciliation record requires (`reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md`, blob `75da2597`): E1 (`imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md`, `213594d6`) and E2 (`reviews/d1_section9_borel_repair_20260925/REPAIR.md`, `fe9b9ce4`). Used: §1 (the pins, `Q_r`, `W_r`), §2 (positive Fourier spectrum), §§3–5 (the contact frame and the regression moments).
- **[R]** (`frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf`): §2 ((R2)–(R4): the centered observations `U_r`, `U_r − U_0 = O(r²)` uniformly over frames) and §4 ((R10), the full normalizer in every `d`).
- **#243** (`frontiers/soft_fold_limit_20261002/PROOF.md`, blob `6502cf7b`): the jets (0.2).
- **C92** and **C93** (`frontiers/planar_soft_layer_chain_20261003/C92/PROOF.md`, blob `4f6598a1`; `…/C93/PROOF.md`, blob `204fd6f3`): the `d = 2` theorems whose proofs are re-run here in `d = 3`. Only their arguments are reused, not their `d = 2` statements.

**Consumed (author-side, pending review).** A3.3 ([5998500022](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5998500022)): Lemma P and Proposition W3, in their `C⁴` form (A3.3 §2: both hold with `‖f‖_{C⁴}` in place of `‖f‖_{C⁵}`). Lemma D, Theorem J₃'s (J₃.3) and (J₃.5), and the actual-measure statements of Corollary E₃ are conditional on W3. Lemma S, Lemma CM₃, the identity (J₃.18), (J₃.4), and the model statements (E₃.3) and (E₃.10) use neither W3 nor Lemma P.

**Cited.** #243, Steps 1–3 of the proof of Theorem FL, (3.3)–(3.5) (Remark 2). A3.2's Corollary WF (Remark 1). C91 (W4)–(W5) and (W15)–(W16) (§6).

**What is new.**
1. **Lemma CM₃**, the `d = 3` analogue of C92 (J8)–(J10): the 20 contact jets of order at most 3 are uniformly nondegenerate, and the conditional moments of the field norm are polynomial in the conditioning jets.
2. **Theorem J₃**, the `d = 3` analogue of C92 Theorem J (J3)–(J5). On the soft layer `{|λ̃| ≤ Λ}` the weighted law of `(λ̃, λ₂, θ, t)` has a density `g_r`. Here `λ₂` is the hard eigenvalue, `θ` the eigenframe angle and `t` the free third-order jets. `g_r` is `O(r)`-close in polynomially weighted `L¹` to an explicit limit `g₀`, with the full normalizer. The hard eigenvalue is integrated down to `0` and across its sign change, which is where W3's uniformity is used.
3. **Corollary E₃**, the `d = 3` analogue of C93 (E1)–(E12): typing-edge strip bounds, the untyped weighted mass `Q_r^W(D_Λ ∩ T^c) ≤ Cr⁴`, and the truncated inverse moments.

With A3.3, this gives an author-side proof candidate in `d = 3`, conditional on W3 and pending nonauthor review, for the finite-`r` jet-law part of A3.2's C92 row and the edge-envelope part of its C93 row. It does not cover C92 (J6)–(J7) and (J20) or C93 (E13)–(E20) (§6).

### 0. Setting and notation

- **Field and pins ([P] §1).** `d = 3`, `X = ℝ³/(Lℤ³)`, the centered variance-one field with the periodized kernel `K_L`. The pins are `M = −(r/2)u` at height `b` and `S = (r/2)u` at height `b − kr³`, with zero gradients. `Q_r` is the regression law, and `W_r = |det H_M det H_S| 1{H_M < 0, ind H_S = 2}`. Also `Z_r := E_{Q_r}W_r` and `Q_r^W := (W_r/Z_r)Q_r`.
- **Parameters.** `b ∈ B₀` (a fixed compact set), `k ∈ [k₋, k₊] ⊂ (0, ∞)` and `0 < Λ < ∞` are fixed. Let `(u, θ₁, θ₂)` be any orthonormal frame. Every constant below depends only on `L`, `B₀`, `k_±` and `Λ` (and on `p`, `q` where they appear), and is uniform in `b`, `k`, the frame and `0 < r ≤ r₀`.
- **Contact observations ([R] §2).** `U_r ∈ ℝ⁸`: the four axial rows and the four transverse rows of [R] §2, with target `v_r = (b − kr³/2, −kr², 0, 12k, 0, 0, 0, 0)`. Its contact limit is `U₀ = (f, f_x, f_xx, f_xxx, f_{y₁}, f_{xy₁}, f_{y₂}, f_{xy₂})(0)`, with `v₀ = (b, 0, 0, 12k, 0, 0, 0, 0)`.
- **Midpoint jets.**
  - `A := D²_Θf(0) ∈ Sym(2)` in the basis `(θ₁, θ₂)` of `Θ = u^⊥`.
  - `t ∈ ℝ⁹`: the nine third-order partials at `0` in the frame, other than `f_xxx(0)`.
  - `N := 1 + max_{|α|≤4} sup_X |D^αf|`, as in C92.
- **Spectral coordinates.** Let `λ₁ ≤ λ₂` be the eigenvalues of `−A` and `λ̃ := kλ₁/r`.
  - Where `λ₁ < λ₂`, let `θ ∈ [0, π)` be the angle of the `λ₁`-eigenline, `e₁ = cos θ θ₁ + sin θ θ₂` and `e₂ = −sin θ θ₁ + cos θ θ₂`.
  - The jets of #243 (0.2) in this eigenframe are `γ = cos θ t_{xx1} + sin θ t_{xx2}` and `B = cos²θ t_{x11} + 2 sin θ cos θ t_{x12} + sin²θ t_{x22}`. Here `t_{xxj} = ∂_u²∂_{θ_j}f(0)` and `t_{xij} = ∂_u∂_{θ_i}∂_{θ_j}f(0)`.
  - Then `Y = 3kB − γ²/4`, `a_M := 6λ̃ + Y`, `a_S := 6λ̃ − Y` and `w := (a_M)₊(a_S)₊`. Under `e₁ ↦ −e₁`, `γ` changes sign and `B` does not, so `w` is a function of `(λ̃, θ, t)`.
- **The soft layer.** `D_Λ := {(λ̃, λ₂, θ, t) : |λ̃| ≤ Λ, λ₂ ∈ ℝ, θ ∈ [0, π), t ∈ ℝ⁹}`. For Borel `E ⊂ D_Λ` put

      μ_r(E) := r^{−5} E_{Q_r}[W_r 1{(λ̃, λ₂, θ, t) ∈ E}],                                                     (J₃.1)

  evaluated on the full-measure event `{λ₁ < λ₂}`. `P := 1 + |λ₂| + |t|` is the polynomial weight.
- **The weight in the window.** `D_r := W_r/r⁴ = k²F₃(H_{M̂₀})F₂(H_{Ŝ₀})` (A3.3, step 1 of W3), with `F_j(X) := |det X|1{ind X = j}` and the window Hessians `H_p` of A3.3 §§1–2.

### 1. Lemma CM₃ (the 20 contact jets)

Put `V_r := (U_r, A, t) ∈ ℝ²⁰`.

**Lemma CM₃.** After reducing `r₀`:
- **(a)** `cI ≤ Cov(V_r) ≤ CI` and `Cov(V_r) − Cov(V₀) = O(r²)`.
- **(b)** Given `U_r = v_r`, `(A, t)` has a Gaussian density `ρ_r` on `Sym(2) × ℝ⁹`, with respect to `dA₁₁ dA₁₂ dA₂₂ dt` (independent entries; Lemma S uses the same coordinates), with `ρ_r(a, t) ≤ Ce^{−c(|a|² + |t|²)}` and

      |ρ_r(a, t) − ρ₀(a, t)| ≤ C r² (1 + |a| + |t|)² e^{−c(|a|² + |t|²)}.                                   (J₃.9′)

- **(c)** For every finite `p ≥ 0` (for `p < 1` by Jensen from `p = 1`),

      E[N^p | U_r = v_r, A = a, t] ≤ C_p (1 + |a| + |t|)^p.                                                 (J₃.10)

*Proof.* This is C92 §2 with ten functionals replaced by twenty.
1. **Rank.** At contact, the 20 entries of `V₀` are exactly the 20 distinct partial derivatives of order at most 3 at `0`, in the frame: `U₀` has 8, `A` has 3, `t` has 9, and none is repeated (control S2).
   - A real combination `Σ c_α ∂^αf(0)` has variance `Σ_n a_n |P(2πn/L)|²`, with `P(ξ) = Σ c_α (iξ)^α`. [P] §2 gives `a_n > 0` for every `n ∈ ℤ³`.
   - If the variance is zero, then `P(Rᵀξ) = 0` for every `ξ ∈ (2π/L)ℤ³`, where `R` is the frame. A polynomial vanishing on a scaled copy of `ℤ³` is zero (apply the one-variable zero theorem coordinate by coordinate). So `P∘Rᵀ = 0`, hence `P = 0` and `c = 0`, and `Cov(V₀)` is positive definite in every frame.
   - The frame space is compact and `Cov(V₀)` is continuous on it, so its eigenvalues lie in a fixed `[c, C]`.
2. **Contact rate.** `U_r − U₀ = O(r²)` in every `L^p`, with the same rate for cross-covariances with fixed derivatives, uniformly over frames ([R] §2). `A` and `t` do not depend on `r`. This gives (a) after reducing `r₀`.
3. **The conditional law.** Schur complements give (b)'s covariance, uniformly elliptic with `O(r²)` differences. The conditional mean `Cov((A, t), U_r)Cov(U_r)⁻¹v_r` is bounded (compact `b`, `k`), with `O(r²)` differences, since `v_r − v₀ = O(kr²)`.
   - Interpolate mean and covariance linearly. The derivative of the Gaussian density along the segment is the density times a polynomial of degree 2 in `(a, t)` with `O(r²)` coefficients. Integrating gives (J₃.9′), as in C92 (J9).
4. **Conditional moments.** Given `V_r = (v_r, a, t)`, the field is `m + g`.
   - `m = Cov(f(·), V_r)Cov(V_r)⁻¹(v_r, a, t)` has `‖m‖_{C⁴} ≤ C(1 + |a| + |t|)`, by (a) and bounded derivatives of the covariance.
   - The residual `g` does not depend on `(a, t)` and has uniformly bounded `C⁴` moments: each centered conditional Fourier coefficient has variance at most its unconditional one, and `Σ√a_n (1 + |n|)⁴ < ∞` with Minkowski (C92 §2).
   - So `N ≤ 1 + ‖m‖_{C⁴} + ‖g‖_{C⁴}` gives (c). ∎

### 2. Spectral coordinates and the exact density identity

**Lemma S.** For `r > 0` put `Ψ_r(λ̃, λ₂, θ) := −R_θ diag(rλ̃/k, λ₂) R_θᵀ`, with `R_θ` the rotation by `θ`. On `{λ₂ > rλ̃/k} × [0, π)` the map `Ψ_r` is a bijection onto `Sym(2)` minus the null line `{−A ∈ ℝI}`, and

    |det DΨ_r| = (r/k)(λ₂ − rλ̃/k).                                                                           (J₃.S)

*Proof.* For `S = R_θ diag(μ₁, μ₂)R_θᵀ`, `|∂(S₁₁, S₁₂, S₂₂)/∂(μ₁, μ₂, θ)| = |μ₂ − μ₁|`: the determinant is `(μ₁ − μ₂)·(−(cos²θ + sin²θ)²)`. Then use `μ₁ = rλ̃/k`. Each matrix with distinct eigenvalues has exactly one ordered spectrum and one eigenline angle in `[0, π)`. Control S1 checks the Jacobian exactly at rational points. ∎

**The density identity.** Disintegrate `E_{Q_r}` over `(A, t)` with density `ρ_r` and the regression version of C92 §2. Change variables by Lemma S, and use `W_r = r⁴D_r`. For every nonnegative measurable `F` on `D_Λ` and every `p ≥ 0`,

    r^{−5} E_{Q_r}[W_r N^p F(λ̃, λ₂, θ, t)] = ∫_{D_Λ} F · g_r^{(p)} dλ̃ dλ₂ dθ dt,
    g_r^{(p)} := k^{−1}(λ₂ − rλ̃/k)₊ ρ_r(Ψ_r(λ̃, λ₂, θ), t) E[D_r N^p | U_r = v_r, A = Ψ_r(λ̃, λ₂, θ), t].     (J₃.18)

Tonelli applies to these nonnegative integrands. `g_r := g_r^{(0)}` is the density of `μ_r`. The factor `r⁵` is `r` from the soft eigenvalue (`dλ₁ = (r/k)dλ̃`) times `r⁴` from the weight, as in `d = 2`.

### 3. The weight given the jets

**Lemma D.** For `0 < r ≤ 1`, pathwise for the exactly pinned field,

    |D_r − (λ₂)₊² w| ≤ C r (1 + N)⁷ (1 + |λ₂|)⁶ (1 + |λ̃| + |t|²)⁶.                                       (J₃.16)

*Proof.* We read A3.3's `‖f‖_{C⁴}` in the max convention, so it is at most `N`. Hence `rN ≤ 1` gives W3's hypothesis, and the right sides of (W3) and (P.1) increase with their `N`. Also `|γ|, |B| ≤ 2|t|`, so `Π := 1 + |λ̃| + γ² + |B| + N ≤ C(1 + |λ̃| + |t|²)(1 + N)`.
- **If `rN ≤ 1`.** (W3) gives at most `CrN(|λ₂| + rN)Π⁴(1 + |λ₂|)² ≤ CrN(1 + |λ₂|)³Π⁴`.
- **If `rN > 1`.** Lemma P holds for every `r ≤ 1`. It gives `‖H_p‖ ≤ C(Π + |λ₂| + N)` at both pins, from the model blocks, `r^{1/2}|Da| ≤ CN` and `‖E_p‖ ≤ CNr`. So `D_r ≤ k²‖H_{M̂₀}‖³‖H_{Ŝ₀}‖³ ≤ C(Π + |λ₂| + N)⁶`, and `(λ₂)₊²w ≤ C(1 + |λ₂|)²Π²`. Multiplying by `rN > 1` gives the same form.

In both cases the right side is at most that of (J₃.16). ∎

**Corollary.** By Lemma CM₃(c), on `D_Λ`, where `|Ψ_r| ≤ |λ₂| + Λ/k₋`:

    |E[D_r | U_r = v_r, A, t] − (λ₂)₊²w| ≤ C r P^{25},                                                     (J₃.17)
    E[D_r N^p | U_r = v_r, A, t] ≤ C_p (λ₂)₊² w P^p + C_p r P^{p+25}.                                     (E₃.7)

### 4. Theorem J₃ (the soft-layer law)

Let `ρ₀` be the joint density of `(A, t)` given `U₀ = v₀`. Put `A₀(λ₂, θ) := −λ₂ e₂e₂ᵀ` (that is, `Ψ_r` at `r = 0`), and

    g₀(λ̃, λ₂, θ, t) := k^{−1} λ₂ ρ₀(A₀(λ₂, θ), t) · λ₂² w   for λ₂ > 0,   and 0 for λ₂ ≤ 0,
    m_Λ := ∫_{D_Λ} g₀,      z₀ := E[(6k)² det(A)² 1{A < 0} | U₀ = v₀],      z_r := Z_r/r².                   (J₃.2)

`g₀` vanishes for `λ̃ ≤ 0`, since `a_M + a_S = 12λ̃`. Let `μ₀` be the measure `g₀ dλ̃ dλ₂ dθ dt` on `D_Λ`.

**Theorem J₃.** After reducing `r₀`:
- **(J₃.3)** For every finite `q ≥ 0`: `∫_{D_Λ} P^q |g_r − g₀| ≤ C_{Λ,q} r`.
- **(J₃.4)** `0 < m_* ≤ m_Λ ≤ m^* < ∞`, `0 < z_* ≤ z₀ ≤ z^* < ∞`, `|z_r − z₀| ≤ Cr` and `z_r ≥ z_*/2`.
- **(J₃.5)** The normalized law `η_r(E) := r^{−3}Q_r^W((λ̃, λ₂, θ, t) ∈ E)` equals `μ_r/z_r`, with `∫_{D_Λ} P^q |g_r/z_r − g₀/z₀| ≤ Cr`. In particular `Q_r^W(|λ̃| ≤ Λ) = r³m_Λ/z₀ + O(r⁴)`.

*Proof.*
1. **Pointwise comparison, where `λ₂ > max(0, rλ̃/k)`.** Write `E_r` for the conditional expectation in (J₃.17). Then

       g_r − g₀ = −(rλ̃/k²) ρ_r(Ψ_r) E_r + k^{−1}λ₂ [ρ_r(Ψ_r, t) − ρ₀(A₀, t)] E_r + k^{−1}λ₂ ρ₀(A₀, t) [E_r − λ₂²w].

   - **The density term.** By (J₃.9′), the shift `|Ψ_r − A₀| = r|λ̃|/k ≤ rΛ/k₋` and the affine gradient of `log ρ₀`, `|ρ_r(Ψ_r, t) − ρ₀(A₀, t)| ≤ C r P² e^{−c(λ₂² + |t|²)}`. This is the analogue of C92 (J9).
   - **The weight term.** By (J₃.17), `E_r ≤ λ₂²w + CrP^{25} ≤ CP^{27}` on `D_Λ`.
   - **Together,** `|g_r − g₀| ≤ C r P^{30} e^{−c(λ₂² + |t|²)}`.
2. **The two strips.**
   - **`rλ̃/k < λ₂ ≤ 0`** (only for `λ̃ < 0`). Here `g₀ = 0`, the factor `λ₂ − rλ̃/k` is at most `rΛ/k₋`, and `E_r ≤ CrP^{25}` because `(λ₂)₊ = 0`. The strip has `λ₂`-width at most `rΛ/k₋`, so it contributes `O(r³)`.
   - **`0 < λ₂ ≤ rλ̃/k`** (only for `λ̃ > 0`). Here `g_r = 0`, since no matrix has `λ₂ < λ₁`, and `g₀ ≤ Cλ₂³P⁴e^{−c|t|²} ≤ Cr³P⁴e^{−c|t|²}`. The strip contributes `O(r⁴)`.
3. **(J₃.3).** Integrate 1–2 against `P^q`. The Gaussian factor makes every polynomial weight integrable, and `θ` ranges over `[0, π)`.
4. **(J₃.4).**
   - `z_r = E_{Q_r}[W_r/r²]`, since `F_d(K_M)F_{d−1}(K_S) = W_r/r²` in [R] §4. So [R] (R10) gives `|z_r − z₀| ≤ Cr(k + r)P_R^N ≤ Cr`, with [R]'s `P_R = 1 + |b| + k` bounded.
   - **Lower bound for `z₀`.** Given `U₀ = v₀`, `A` is a nondegenerate Gaussian on `Sym(2)` with mean and covariance in a compact set (Lemma CM₃). So it lies in `{‖A + I‖ ≤ ½}` with probability at least `c > 0`. There `A < 0` and `|det A| ≥ 1/4`, so `z₀ ≥ 36k₋²c/16`. The upper bound is a Gaussian moment. Reduce `r₀` so that `Cr₀ ≤ z_*/2`.
   - **Lower bound for `m_Λ`.** On the box `λ̃ ∈ [Λ/4, Λ/2]`, `λ₂ ∈ [1, 2]`, `|t| ≤ δ_Λ`, take `δ_Λ` so small that `|Y| ≤ Λ`. There `w ≥ (3Λ/2)² − Λ² > 0`, and `ρ₀` is bounded below on that compact set. The upper bound follows from the Gaussian majorant.
5. **(J₃.5).** `r^{−3}Q_r^W(E) = r^{−3}·r⁵μ_r(E)/(r²z_r) = μ_r(E)/z_r`. Add and subtract `g₀/z_r`, then use (J₃.3), `|1/z_r − 1/z₀| ≤ Cr` and `∫P^qg₀ < ∞`. ∎

**Remarks.**
1. **Where W3's uniformity enters.** `g₀` carries `λ₂³`: `λ₂` from the Jacobian (J₃.S) and `λ₂²` from the hard weight. The proof integrates `λ₂` over all of `ℝ`, including `λ₂ → 0`, where the soft and hard eigenvalues coalesce, and the strip `λ₂ ≤ 0`. A3.2's Corollary WF would not do here. It is multiplicative and needs `kδ < λ₂/2` and `θ_p < 2`, so it says nothing on the strip `λ₂ ≲ r`, on `λ₂ ≤ 0`, or near the typing edges. Where it applies, its error is integrable; the obstruction is its domain. (J₃.16) is additive and holds everywhere.
2. **Antecedent.** #243's proof of Theorem FL (Steps 1–3, (3.3)–(3.5)) uses the same Weyl coordinates and the same Jacobian `μ₂ − μ̃r/k`. It conditions on the contact Hessian of a coupled field, and finds without a rate the pointwise limit `μ₂²(36μ̃² − Y*²)1{μ₂ > 0, |Y*| < 6μ̃}` of `W_r/r⁴`, which is `(λ₂)₊²w`. Theorem J₃ conditions on the actual jets and adds the rate `r` for the weighted jet law. That is the quantitative step C92 adds in `d = 2`.
3. **Every `d ≥ 3` (sketch only).** Weyl's integration formula on `Sym(d − 1)` replaces (J₃.S) by the Vandermonde `Π_{i<j}|λ_j − λ_i|` times Haar measure, and Lemma CM₃ holds verbatim with all partials of order at most 3. The main missing input is A3.3 Remark 2's `d`-dimensional W3, which is only sketched there. The strips for several hard eigenvalues and the crude `rN > 1` bound (a `d`-dimensional Lemma P) would also have to be written out.

### 5. Corollary E₃ (typing edges)

Let `T := {λ₂ > 0, a_M > 0, a_S > 0}` (the model's typed set), `h := min(a_M, a_S)` and `A_* := 12Λ`. On `T`, `λ̃ > 0`, `a_M + a_S = 12λ̃`, and `w = s(12λ̃ − s)` with `s = a_i`.

**Corollary E₃.** For `i ∈ {M, S}`, finite `p, q ≥ 0` and nonnegative measurable `φ` on `(0, A_*)`:

    r^{−5} E_{Q_r}[W_r N^p P^q 1_{D_Λ∩T} φ(a_i)] ≤ C_{p,q} ∫₀^{A_*} φ(s)(s + r) ds,                          (E₃.2)
    ∫_T P^q φ(a_i) dμ₀ ≤ C_q ∫₀^{A_*} φ(s) s ds.                                                               (E₃.3)

Hence, for `0 < δ ≤ A_*`:

    μ₀(T ∩ {h ≤ δ}) ≤ Cδ²,     r^{−5}E_{Q_r}[W_r N^pP^q 1_{D_Λ∩T}1{h ≤ δ}] ≤ C(δ² + rδ),                  (E₃.4)
    E_{Q_r^W}[N^pP^q 1_{D_Λ∩T}1{h ≤ δ}] ≤ C r³(δ² + rδ),                                                     (E₃.5)
    Q_r^W(D_Λ ∩ T^c) ≤ C r⁴.                                                                                  (E₃.6)

For every finite `v ≥ 0` and `0 < δ < A_*`:

    r^{−5}E_{Q_r}[W_r N^pP^q 1_{D_Λ∩T} a_i^{−v}1{a_i ≥ δ}] ≤ C ∫_δ^{A_*} [s^{1−v} + r s^{−v}] ds,             (E₃.11)

and `∫_T a_i^{−v} dμ₀` is finite exactly when `v < 2` (E₃.10).

*Proof.*
1. **(E₃.2).** Use (J₃.18) with `F = P^q1_Tφ(a_i)`, then (E₃.7). On `T`, change variables from `B` to `s = a_i`, holding `λ̃`, `λ₂`, `θ`, `γ` and the other jets fixed.
   - `B = ⟨b_θ, t″⟩`, with `t″ = (t_{x11}, t_{x12}, t_{x22})` and `b_θ = (cos²θ, 2 sin θ cos θ, sin²θ)`. Here `|b_θ|² = 1 + 2 sin²θ cos²θ ∈ [1, 3/2]` (control S3).
   - Rotate `t″` orthonormally so that `B/|b_θ|` is a coordinate, then use `∂a_i/∂B = ±3k`. The Jacobian is at most `1/(3k₋)`. `γ` uses the disjoint coordinates `t_{xx1}`, `t_{xx2}`, so it stays fixed.
   - By Lemma CM₃(b) and `|Ψ_r|² ≥ λ₂²/2 − C` in the coordinates `(A₁₁, A₁₂, A₂₂)`: `ρ_r(Ψ_r, t) ≤ Ce^{−c(λ₂²/2 + |t|²)}`. As in C93's proof after (E9), absorb `P^m` into half of the exponent and drop the decay in the `B` direction. The remaining `λ₂`, `θ` and jet integrals are bounded uniformly in `(λ̃, s)`.
   - What is left is `C∫₀^Λ dλ̃ ∫₀^{12λ̃} φ(s)[s(12λ̃ − s) + r] ds ≤ C∫₀^{A_*} φ(s)(s + r) ds`.
2. **(E₃.3).** The same computation with `g₀` and no field norm.
3. **(E₃.4)–(E₃.5).** Take `φ = 1{s ≤ δ}`, so the integral is `δ²/2 + rδ`, and take a union over `i`. Then multiply by `r³/z_r` and use (J₃.4).
4. **(E₃.6).** `g₀ = 0` off `T`, so `μ₀(D_Λ ∩ T^c) = 0`, and (J₃.3) gives `μ_r(D_Λ ∩ T^c) ≤ Cr`. Multiply by `r³/z_r`.
5. **(E₃.10)–(E₃.11).** Take `φ(s) = s^{−v}1{s ≥ δ}` in (E₃.2) and (E₃.3).
   - The lower half of (E₃.10) is C93's argument. Restrict to `λ̃ ∈ [Λ/3, 2Λ/3]`, `λ₂ ∈ [1, 2]`, the other jets in a small box, and `0 < s < s₀ < Λ`. There `12λ̃ − s ≥ 3Λ`, the density is bounded below, and `w ≥ cs`.
   - As in C93 (E12), no untruncated inverse moment of the actual measure is inferred. ∎

### 6. Where this sits in A3.2's map (`d = 3`)

| row | after A3.3 | after A3.4 |
|---|---|---|
| C92 | the weight (W3) and the normalizer ([R] (R10)); the Gaussian part open | **Author-side candidate for the jet law (conditional on W3; review pending):** Lemma CM₃ (J8–J10), Theorem J₃ (J3–J5, J9, J16–J19). **Open:** the analogue of C92 (J6)–(J7) and (J20), the growing-window Taylor failure. |
| C93 | Corollary TE (pathwise) | **Author-side candidate for (E1)–(E12) (conditional on W3; review pending):** Corollary E₃. **Open:** the analogue of C93 §§3–4 (E13)–(E20), the Hessian transfer on growing windows, which needs a `d = 3` window error bound like C91 (W4)–(W5), with the matrix transfer (W15)–(W16). |
| C94, C97 (weighted part), C98 (`d ≥ 3` strata), C101/C103 (the rate) | open | unchanged |

The `d = 3` analogue of C101's rate needs the two open rows above, the `d ≥ 3` strata (C98) and the weighted decision estimates (C94, C97). Theorem J₃ and Corollary E₃ supply its jet-law and edge inputs.

### 7. Checks

`a34_exact.py` (companion controls comment): standard library only, exact rationals, seeded. No check depends on an `assert`. The output is byte-identical under `-O`.
- **S1.** Lemma S: on random rational `(μ₁, μ₂, τ)`, with rational rotations `cos θ = (1 − τ²)/(1 + τ²)`, `sin θ = 2τ/(1 + τ²)`, the exact Jacobian of `(A₁₁, A₁₂, A₂₂)` in `(μ₁, μ₂, τ)` is `|μ₂ − μ₁|·2/(1 + τ²)`, and with `μ₁ = rλ̃/k` the Jacobian in `(λ̃, λ₂, τ)` carries the factor `r/k` of (J₃.S). Also `−Ae₁ = μ₁e₁` and `−Ae₂ = μ₂e₂` exactly.
- **S2.** Lemma CM₃'s rank step:
  - `U₀ ∪ A ∪ t` is exactly the set of 20 multi-indices of order at most 3, with no repetition.
  - The 20 × 20 matrix of monomials of degree at most 3 at the principal-lattice points `{α ∈ ℕ³ : |α| ≤ 3}` is invertible.
- **S3.** The eigenframe jets. On random rational cubics, exact directional derivatives along `e₁ = (0, cos θ, sin θ)` equal the formulas for `γ` and `B`. Also `w` is invariant under `e₁ ↦ −e₁`, and `|b_θ|² = 1 + 2 sin²θ cos²θ ∈ [1, 3/2]`.
- **S4.** The edge algebra: `a_M + a_S = 12λ̃`, `w = s(12λ̃ − s)` on `T`, `∂a_M/∂B = 3k = −∂a_S/∂B`, and `w = 0` whenever `λ̃ ≤ 0`.
- **S5.** The strip integral. `∫₀^Λ dλ̃ ∫₀^{min(δ, 12λ̃)} s(12λ̃ − s) ds`, computed exactly for several rational `δ`, lies between `c_Λδ²` and `C_Λδ²`.
- **Mutants**, each rejected in its own control:
  - N1: Jacobian without the eigenvalue gap;
  - N2: a point set on the plane `x₃ = 0` in S2, which makes the matrix singular;
  - N3: `B` rotated with `(cos θ, sin θ)`;
  - N4: `a_M + a_S = 6λ̃`;
  - N5: the strip integral scaling as `δ`;
  - N6: a repeated functional in S2's list (`(1,1,1)` replaced by `(1,1,0)`).

These check finite algebra only. The analytic steps (Gaussian regression, the interpolation in (J₃.9′), Tonelli, and W3 itself) are argued above, not tested.

A clean-context referee of the same provider read the pre-release text (ACCEPT WITH MINOR FIXES; same-provider, so not review evidence). Its fixes are applied:
- a false sentence in Remark 1 about Corollary WF;
- the status wording ("author-side candidate", not "closed");
- the open-scope lists;
- the definition of `μ₀` and the reference measure on `Sym(2)`;
- the frame rotation in the rank step;
- the norm convention in Lemma D;
- source bookkeeping.

Its suggested control N6 is included.

### 8. Not claimed

- The `d = 3` analogues of C92 (J6)–(J7) and (J20) and of C93 (E13)–(E20) (§6); any weighted decision estimate; a `d = 3` rate for `1 − p_r`.
- Any statement for `d ≥ 4` beyond Remark 3's sketch.
- Numerical constants. `C` depends only on `L`, `B₀`, `k_±`, `Λ`, `p` and `q`.
- Independence from A3.3's W3 where it is used (see "Consumed"): those conclusions are conditional on it, and A3.3 is author-side and unreviewed.

### 9. Review request

A bounded nonauthor read of Lemma CM₃, Lemma S, Lemma D, Theorem J₃ and Corollary E₃, and a replay of `a34_exact.py`. A3.3's W3 can be read first or together. Please claim first.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_