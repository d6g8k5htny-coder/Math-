## QS addendum A3.6: the `d = 3` weighted decision on the bounded soft layer (C94, C97 and C98 in `d = 3`)

**Object.** `CL-QS-A3-6-WEIGHTED-DECISION-20261005-v1`.

**Who.** Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`, the author of QS and A3–A3.5. Dylan Roy — delegated AI work. Author-side. Scientific effect: NONE.

**Claim.** [6001753394](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6001753394); this delivery releases it. The executable and its stdout are in a companion controls comment, posted right after this one.

**Consumed.**
- *Merged or reviewed.*
  - [P] (with E1, E2 and the reconciliation) §§1 and 8; [R] §4; #243 (0.2).
  - C82 ((7), Theorem LB and §2's finite branches); C94 §§0–5, C97 §§0–3 and 5, C98 §§1–4, and C96. These are main#229 comments, incorporated in Math- `frontiers/planar_soft_layer_chain_20261003/`.
  - QS §§1 and 7; A1's W1, as C94 §2 uses it; A2's (H).
  - A3 (§0's windows, Lemma SR, QS-E′_d) and A3.1 (Lemmas TL_d and N_d, Corollary H_d, the radii of §6), with the erratum [5998430951](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5998430951).
- *Author-side, with scoped nonauthor reads.*
  - A3.3: Proposition W3, Lemma P and the step-1 window identity.
  - A3.4, read with its successor [5999301338](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5999301338): Lemma CM₃, (J₃.2)–(J₃.5), (J₃.9′), (J₃.17), (J₃.18), (E₃.2), (E₃.6), (E₃.7), §5 step 1 (the change of variables `B → a_i`), and Theorem J₃'s step 1 (the shift `Ψ_r − A₀`). Its actual-measure statements are conditional on A3.3 (W3, Lemma P and the window identity).
  - A3.5: Lemma FW₃ and (FW.0), Proposition D₃, Lemma T₃, Lemma E₃⁺, the proof of Corollary FW₃′, (G₃.1)–(G₃.3), (G₃.5), and Remarks 3–4. Its reads were S1 PASS and S2, S3 PASS_SCOPED.
- Every weighted statement below is therefore conditional on A3.4 and, through it, on A3.3. The certificates (Theorem E₃(a), Lemma SC, Theorem R₃(a)) and §1 are deterministic.

**What is new.**
1. **Theorem E₃** (§3), C94 in `d = 3`.
   - On the model elder sector `E`, a good event fails with weighted mass `O(r^{7/2})`. It is built from A3.5's barrel, reduced height and Hessian transfer, with C94's random tolerance `τ_E = ½min(v, −μ)`.
   - On the good event, A3's QS-E′_d decides elder pairing.
   - The new estimate is the hard-gap term `C_e kN²rw⁴/λ₂` of A3.5's (D₃) against the random tolerance, through A3.5's joint edge–gap majorant (E₃⁺).
2. **Lemma SC and Theorem R₃** (§4), C97 in `d = 3`. C97's two-margin chord certifies rejection when drawn in the plane of the pin axis and the soft eigenvector. It needs no barrel, no reduced height, no gradient pin and no bound on `λ₂`. This removes the hard gap from the rejected side; the bad mass is again `O(r^{7/2})`.
3. **Theorem BL₃** (§5), C98 in `d = 3`. `Q_r^W(D_Λ ∩ (H_r Δ E)) ≤ Cr^{7/2}` and `Q_r^W(H_r | D_Λ) = m_E/m_Λ + O(√r)`, with a joint jet/Boolean total-variation bound. All are uniform in `b ∈ B₀`, `k ∈ [k₋, k₊]` and the frame.
4. **Appendix A** carries the riders promised in [6001626468](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6001626468): Proposition G₃⁻ with its proof, and four wording notes on A3.5.

### 0. Setting and notation

- **As in A3.4 §0 and A3.5 §0.**
  - `d = 3`; the pins `M_r = −(r/2)u`, `S_r = (r/2)u` at heights `b`, `b − kr³`; `Q_r`, `W_r = |det H_M det H_S|1{H_M < 0, ind H_S = 2}`, `Z_r`, `Q_r^W`. The parameters are `b ∈ B₀`, `k ∈ [k₋, k₊]` and `Λ`, all fixed.
  - The coordinates `(λ̃, λ₂, θ, t)`; the eigenframe `(u, e₁, e₂)`; the soft jets `γ, B, C₃`; `Y = 3kB − γ²/4`, `a_M = 6λ̃ + Y`, `a_S = 6λ̃ − Y`, `w_λ = (a_M)₊(a_S)₊`.
  - `D_Λ = {|λ̃| ≤ Λ}`, `T = {λ₂ > 0, a_M > 0, a_S > 0}`, `A_* = 12Λ`, the jet weight `P = 1 + |λ₂| + |t|` (Euclidean norms) and the field norm `N` of A3.5 §0.
  - `μ_r` (J₃.1) with density `g_r` (J₃.18), `μ₀ = g₀ dλ̃dλ₂dθdt` (J₃.2), and `Q_r^W = r³μ_r/z_r` on `D_Λ`, with `z_r ≥ z_*/2` (J₃.4)–(J₃.5).
- **Letters.** These avoid clashes with A3.4, A3.5 and the planar chain.
  - QS's cubic is `P_QS`.
  - The highest extra saddle of `P_QS` is `Y*`, and its depth is `h_Y`. `Y` is A3.4's jet.
  - A3.5's chart error is written `ℰ`. `E` is the elder sector, and `E_S`, `E_M` are QS's ellipses.
  - A3.5's normalized Hessian suprema `H_i` of (T₃.2) are written `ℋ_M`, `ℋ_S`. `H_M`, `H_S` are the pin Hessians.
  - The chart variable of A3.5 is `η`, so C94's tolerance is written `τ_E`.
  - The width of the level band is `ϱ`, since `d` is the dimension. A3.4's `h` is not used.
- **The cubic (QS §7).** On `T ∩ {γ ≠ 0}` put

      D := γ² − 12kB = −4Y,   J := 8γ³ − 144kBγ + 576k²C₃,   ψ := 24λ̃/γ²,   c := D/γ²,   R := J/γ³,
      P_QS(u, Z) := 2u³ − 3u/2 − 1/2 − (ψ + 2cu)Z²/48 + RZ³/3456.                                     (0.1)

  Then `G_k(X, ζ) = P_QS(X + γζ/12, γζ)`, `a_M = γ²(ψ − c)/4`, `a_S = γ²(ψ + c)/4`, and `T ∩ {γ ≠ 0} = {λ₂ > 0, ψ > |c|}`. Also `κ_M = (ψ − c)/48 = a_M/(12γ²)` and `κ_S = (ψ + c)/48 = a_S/(12γ²)`, as in A3.5's Lemma T₃.
- **QS §1's model quantities.**
  - `τ̂_•`, `m_S = 2/(125τ̂_S²)` and `ε_M = min(1/(8τ̂_M²), 1)`; put `v := min(m_S, ε_M)`.
  - `μ := max{P_QS(Y′) + 1 : Y′ an extra nondegenerate saddle}`, with `μ = −∞` if there is none. It is Borel. When finite it is attained, and a highest saddle `Y*` has a Borel selection (C82 §2, C97 §1).
  - On `{μ > 0}`, `h_Y := −P_QS(Y*) = 1 − μ ∈ (0, 1)` (C97 (R7)).
- **Sectors** (C94 (C4), C97 (R4)):

      E := D_Λ ∩ T ∩ {γ ≠ 0, ψ ≥ 2c, R² ≤ 16(ψ − 2c)²(ψ + c), μ < 0},     Rsec := D_Λ ∩ T ∩ {γ ≠ 0, μ > 0}.      (0.2)

  These are C94's and C97's sets of soft jets, intersected with `{λ₂ > 0}`. On them put `τ_E := ½min(v, −μ)` and `τ_R := ½min(μ, 4h_Y)`, both finite and positive.
- **Radii** (A3.1 §6): `ρ_E := 3/2 + (5/2)(|γ| + 12)/√(24λ̃)` and `ρ_R := 5/2 + (17/6)(|γ| + 12)/√(24λ̃)`. If `ρ_E < w`, the raw image of `𝔚_E` lies in `{|(X, ζ)| < w} ⊂ Ω_w`. If `ρ_R < w`, the same holds for `𝔚_R`, which contains C97's chord `K := [M, 2Y* − M]` (A3 §0).
- **Chart and error** (A3.5 §0): `Φ`, `𝔉`, `Ω_w`, `𝒲_w` and `ℰ := 𝔉 − G_k + (λ₂/(2k))η² − r^{1/2}η·a₂`. On `η = 0`, `𝔉(X, ζ, 0) = G_k(X, ζ) + ℰ(X, ζ, 0)`. We write `g(u, Z, η) := 𝔉(u − Z/12, Z/γ, η)` (A3.1 §0) and `e := rw⁴` throughout.
- **Decision events.**
  - `D_f(M_r)` is A3.1 §0's maximin on the torus, and `A_r := {D_f(M_r) = f(S_r)}`.
  - `H_r` is C96's designated event: the finite ordinary-superlevel H0 class born at `M_r` dies at `S_r` under the elder rule. It is defined false off the Borel locus where `f` is Morse with distinct critical values.
  - On `{W_r > 0}`, `M_r` is a local maximum and `S_r` has index 2. So C96's deterministic lemma on `T³` (A3.1 Corollary H_d, step 3) and [P] §8 give `H_r = A_r` `Q_r^W`-almost surely.

### 1. Lemma M₃ (model facts in the `d = 3` normalization; deterministic)

**(a) Chart** (QS §7, A3.5 §3). `G_k(X, ζ) = P_QS(X + γζ/12, γζ)`, and the identities after (0.1).

**(b) Jacobian.** Fix `(λ₂, θ, t)` with `γ ≠ 0`. Then `λ̃ = γ²ψ/24`, and on `{ψ > |c|}`

    w_λ dλ̃ = (γ⁶/384)(ψ² − c²) dψ.                                                                       (1.1)

**(c) Poles.** `γ⁶|c|³ = |D|³` and `γ⁶R² = J²`.

**(d) The elder tolerance floor.** Let `a = 2/(3√3)`. On `E`,

    τ̂_S ≤ a(2ψ − c + 3|c|)/(ψ + c) ≤ 3aA_*/a_S,    τ̂_M ≤ 4a,    v ≥ c_* a_S²,    c_* := 3/(250A_*²) = 1/(12000Λ²).   (1.2)

**(e) The rejected endpoint floor.** On `Rsec`,

    h_Y ≥ c_h a_M³/P⁶,    c_h := 4/(27C_τ),    C_τ := (4/9)A_*³ + (1 + 24k₊)²A_*/4 + (8 + 288k₊ + 1152k₊²)²/2304.   (1.3)

**(f) The chord** (C97 (R8)–(R10)). On `Rsec`, `K ⊂ 𝔚_R` and `P_QS(M + s(Y* − M)) = h_Y(2s³ − 3s²)` for `0 ≤ s ≤ 2`.

**(g) Coverage** (C98 (B10), (B16)–(B17)). `E = D_Λ ∩ T ∩ {γ ≠ 0, μ < 0}`. Moreover

    {μ = 0} ⊂ {F = 0},    F := J² − 16(24λ̃ − 2D)²(24λ̃ + D).

*Proof.*
- **(a)** QS §7 (Q7, S15); A3.5 §3 uses the same chart.
- **(b)** We have `w_λ = a_Ma_S = (γ⁴/16)(ψ² − c²)` and `dλ̃ = (γ²/24)dψ`.
- **(c)** Substitute `c = D/γ²` and `R = J/γ³`.
- **(d)**
  - With `κ_S = (ψ + c)/48`, the middle term of `τ̂_S` is `3a|c|/(ψ + c)`. The last term is `√3|R|/(18(ψ + c)^{3/2})`, which is at most `a(ψ − 2c)/(ψ + c)` exactly when `R² ≤ 16(ψ − 2c)²(ψ + c)`. Adding gives the first bound.
  - Since `|c| < ψ`, `2ψ − c + 3|c| < 6ψ`, and `6aψ/(ψ + c) = 36aλ̃/a_S ≤ 3aA_*/a_S`.
  - Then `m_S ≥ 2a_S²/(1125a²A_*²) = c_*a_S²`, because `a² = 4/27`.
  - `τ̂_M ≤ 4a` is A1's W1, as in C94 §2. It gives `ε_M ≥ 1/(128a²) = 27/512 > 3/250 ≥ c_*a_S²`, because `a_S < a_M + a_S = 12λ̃ ≤ A_*`.
  - This is C94 (C8) with C94's `a_S^{C94} = 4a_S` and `A_*^{C94} = 48Λ`.
- **(e)**
  - C97 (R7) gives `h_Y ≥ 4/(27τ̂_M²)`.
  - With `κ_M = a_M/(12γ²)`, `τ̂_M = (1/√3)[2/3 + |D|/(2a_M) + |J|/(48a_M^{3/2})]`. This is C97 (R12) with C97's `s = 4a_M`.
  - The three-term square inequality gives `τ̂_M² ≤ [4a_M³/9 + D²a_M/4 + J²/2304]/a_M³`.
  - Next, `|γ| ≤ |t|`. `B = ∂_u∂_{e₁}²f(0)` and `C₃ = ∂_{e₁}³f(0)` are values of symmetric forms at a unit vector, so they are bounded by Frobenius norms: `|B| ≤ √2|t| ≤ 2P` and `|C₃| ≤ √3|t| ≤ 2P`.
  - Hence `|D| ≤ (1 + 24k₊)P²` and `|J| ≤ (8 + 288k₊ + 1152k₊²)P³`. With `a_M ≤ A_*` and `P ≥ 1`, `τ̂_M² ≤ C_τP⁶/a_M³`.
  - The bound is crude: `P⁶` and the frame constants are far from sharp. Only its form is used.
- **(f)** C97 (R8)–(R10); the cubic is the same. The identity holds at every extra critical point `Y′ ≠ M` with `h = −P_QS(Y′)`, and `K ⊂ 𝔚_R` holds when `0 < h < 1`.
- **(g)** C98 §1 is pure algebra in `(ψ, c, R)`. Multiplying C98 (B16)'s `R² = 16(ψ − 2c)²(ψ + c)` by `γ⁶` gives `F = 0`, by (c) and `γ²ψ = 24λ̃`. ∎

### 2. Two weighted estimates (conditional on A3.4)

**Lemma Rad₃ (the radius tails).** For finite `m, q ≥ 0`, `w ≥ 5` and `• ∈ {E, R}`,

    r^{−5} E_{Q_r}[W_r N^m P^q 1_{D_Λ∩T} 1{ρ_• ≥ w}] ≤ C_{m,q}(w^{−8} + rw^{−4}).                       (2.1)

*Proof.*
1. **The event.** `ρ_E ≥ w` is equivalent to `λ̃ ≤ Θ_E(γ)/(w − 3/2)²`, with `Θ_E(γ) := (25/96)(|γ| + 12)²`. Likewise `ρ_R ≥ w` is equivalent to `λ̃ ≤ Θ_R(γ)/(w − 5/2)²`, with `Θ_R(γ) := (289/864)(|γ| + 12)²`. For `w ≥ 5`, `w − 5/2 ≥ w/2`, so both give `λ̃ ≤ U := min(Λ, 4Θ_•(γ)/w²)`.
2. **The density.** Use (J₃.18) and (E₃.7), as in the proof of A3.5's (E₃⁺).
   - On `T`, `λ̃ > 0`, so `(λ₂ − rλ̃/k)₊ ≤ λ₂`.
   - `ρ_r(Ψ_r, t) ≤ Ce^{−c(λ₂²/2 + |t|²)}` absorbs `P^{m+q+25}` into half of its exponent.
   - Change variables from `B` to `s = a_S`, holding `(λ̃, λ₂, θ, γ)` and the other jets fixed. The Jacobian is at most `1/(3k₋)` (A3.4 §5, step 1). On `T`, `0 < s < 12λ̃` and `w_λ = s(12λ̃ − s)`.
3. **The integrals.** Exactly, `∫₀^U∫₀^{12λ̃} s(12λ̃ − s) ds dλ̃ = 72U⁴` and `∫₀^U∫₀^{12λ̃} ds dλ̃ = 6U²`. So the left side of (2.1) is at most `C∫λ₂(λ₂²U⁴ + rU²)e^{−cλ₂²/4}e^{−c|t|²/4}`, with `U ≤ 4Θ_•(γ)/w²`. Integrate the polynomial in `γ` against the Gaussian. ∎

This is C94 (C6) and C97 (R15). C94's `288U⁴` is `4·72U⁴`: the integrand is the same `w_λ`, and C94's variable is `s′ = a_S^{C94} = 4s`, so `ds′ = 4ds`.

**Lemma LB₃ (the level band).** For `0 < δ ≤ 1/2`,

    μ₀(T ∩ {γ ≠ 0, |μ| ≤ δ}) ≤ Cδ,        μ_r(D_Λ ∩ T ∩ {γ ≠ 0, |μ| ≤ δ}) ≤ C(δ + r).                       (2.2)

*Proof.*
1. **The fibre.** By (J₃.2), `g₀ = k^{−1}λ₂³ρ₀(A₀(λ₂, θ), t)w_λ` on `λ₂ > 0`. Fix `(λ₂, θ, t)` with `γ ≠ 0`. Then `c` and `R` are fixed and `ψ` is linear in `λ̃`.
2. **The band integral.** By (1.1), C82's Theorem LB (with the indicator `{|μ| ≤ δ}`) and Lemma M₃(c),

       ∫ 1{|μ| ≤ δ} w_λ dλ̃ ≤ (γ⁶/384)δ[(1024/3)|c|³ + 64R²] = (δ/384)[(1024/3)|D|³ + 64J²].

   Here the integral runs over all `λ̃` with `ψ > |c|`. Extending it beyond `D_Λ` only enlarges a nonnegative integral.
3. **The model measure.** By Lemma CM₃(b), `ρ₀(A₀, t) ≤ Ce^{−c(λ₂² + |t|²)}`. `|D|³ + J²` is bounded by a polynomial in `t` (for example `|D|³ ≤ 1 + D⁴`), with coefficients bounded for `k ∈ [k₋, k₊]`. Integrating against `k₋^{−1}λ₂³e^{−c(λ₂² + |t|²)}` gives `Cδ`.
4. **The actual measure.** The indicator is bounded and supported in `D_Λ`, so (J₃.3) gives `μ_r ≤ μ₀ + ∫_{D_Λ}|g_r − g₀| ≤ Cδ + Cr`. ∎

This is C94 (C11) in `d = 3`. The hard eigenvalue enters only through the weight `λ₂³`, which is integrable.

### 3. Theorem E₃ (the elder side; (a) deterministic, (b)–(c) conditional on A3.4)

Fix C91's thresholds `τ_M = 1` and `τ_S = 2/5` (A3.5 Remark 4). For `0 < r ≤ r₀` and deterministic `w ≥ 5` with `r^{1/2}w ≤ 1`, define inside `E`

    Good^E(r, w) := E ∩ {ρ_E < w} ∩ (B_r) ∩ {sup_{Ω_w}|G − G_k| < τ_E} ∩ {ℋ_M < 1} ∩ {ℋ_S < 2/5}.           (3.1)

- `(B_r)` is A3.5's barrel event `λ₂ > C_B kN²rw⁴`.
- `G` is the reduced height of Proposition D₃, defined on `(B_r)`.
- `ℋ_i` are A3.5's `H_i` of (T₃.2).

`Good^E` is Borel: `ρ_E`, `τ_E` and `μ` are Borel (C82 §2, C97 §1), `G` and `ℋ_i` are Borel on `(B_r)` (A3.5 Remark 3), and each supremum is a countable one.

**Theorem E₃.**
- **(a) The certificate.** On `Good^E`, `D_f(M_r) = f(S_r)`, and `M_r` and `S_r` are nondegenerate with Morse indices 3 and 2. On the Morse locus, `H_r` holds.
- **(b) The bad mass.** For `0 < ϱ ≤ 1/4` and finite `p ≥ 1`,

      Q_r^W(E ∖ Good^E) ≤ C r³[w^{−8} + rw^{−4} + e + r√e + ϱ + r + (e/ϱ)^p + (e/ϱ)⁴ + r(e/ϱ)² + e⁴ + re² + r²w⁴].   (3.2)

- **(c) The rate.** With `w = r^{−1/16}`, `ϱ = r^{1/2}` and `p = 2`, for `r` small,

      Q_r^W(E ∖ Good^E) ≤ C r^{7/2},    Q_r^W(E ∖ H_r) ≤ C r^{7/2}.                                          (3.3)

*Proof of (a).* We check the hypotheses of A3's Theorem QS-E′_d for `g` in the `(u, Z, η)` chart. Let `Ω` be the `(u, Z)`-preimage of `Ω_w`, and `ε := 4√(k/λ₂)`.
- **`ψ > |c|`** holds on `E ⊂ T`.
- **(B1)–(B3)** hold on `Ω × B̄_ε`, by `(B_r)` and Proposition D₃(a).
- **`Ω ⊃ 𝔚_E`**, because `ρ_E < w`.
- **(H)** holds with tolerance `τ_E`, since `μ < 0` and `0 < τ_E < min(|μ|, m_S, ε_M)`.
- **(E1_d).** Heights are chart-invariant, and `e_G = (G − G_k)∘φ` in A3.5's notation. So `sup_{𝔚_E}|e_G| ≤ sup_{Ω_w}|G − G_k| < τ_E`.
- **(E2_d) and (E3_d).** `E_S, E_M ⊂ 𝔚_E ⊂ Ω` (A3 §0). By Lemma T₃, `ℋ_S < 2/5` and `ℋ_M < 1` bound `‖J_•D²e_GJ_•‖` there.
- **The pins** are exact.

So QS-E′_d gives `d_g(M̂) = −1`. A3.1's Corollary H_d (E), with Lemma N_d and C96, gives the rest. ∎

*Proof of (b).* By (3.1), `E ∖ Good^E` lies in the union of four sets:

    F_ρ := E ∩ {ρ_E ≥ w},   F_B := E ∖ (B_r),   F_H := E ∩ (B_r) ∩ ({ℋ_M ≥ 1} ∪ {ℋ_S ≥ 2/5}),
    F_V := E ∩ (B_r) ∩ {sup_{Ω_w}|G − G_k| ≥ τ_E}.

We bound each in `μ_r`, then multiply by `r³/z_r`. The union bound needs no independence among these events.
1. **`F_ρ`.** Lemma Rad₃ gives `C(w^{−8} + rw^{−4})`.
2. **`F_B`.** `(B_r)^c = {λ₂ ≤ C_BkN²rw⁴} ⊂ {λ₂ ≤ δ_BN²}`, with `δ_B := C_Bk₊e`. So (G₃.3) gives `C(e⁴ + re²)`.
3. **`F_H`.** (G₃.2), with `τ_M = 1` and `τ_S = 2/5`, gives `Cr²w⁴`.
4. **`F_V`, the split.** On `(B_r)`, (D₃) gives `sup_{Ω_w}|G − G_k| ≤ K₀Ne + C_ekN²e/λ₂`. If this is at least `τ_E = ½min(v, −μ)`, one of its two terms is at least `v/4` or at least `−μ/4`. So `F_V` lies in the union of:
   - `V₁ := {K₀Ne ≥ v/4}`;
   - `V₂ := {C_ekN²e/λ₂ ≥ v/4}`;
   - `V₃ := {K₀Ne ≥ −μ/4}`;
   - `V₄ := {C_ekN²e/λ₂ ≥ −μ/4}`.

   All four are intersected with `E`.
5. **`V₁`, Taylor against the margin.** By (1.2), `V₁ ⊂ {a_S² ≤ ε_V N}`, with `ε_V := 4K₀e/c_*`.
   - Split at `a_S = d₁`. On `a_S ≥ d₁`, Markov's inequality gives `1{a_S² ≤ ε_VN} ≤ ε_V²N²a_S^{−4}`.
   - (E₃.2), with the moment `N²`, gives `μ_r(V₁) ≤ C[d₁² + rd₁ + ε_V²(d₁^{−2}/2 + rd₁^{−3}/3)]`.
   - Take `d₁ = √ε_V`; if `√ε_V ≥ A_*`, the strip alone suffices. The result is `C(ε_V + r√ε_V) ≤ C(e + r√e)`.

   This is C94 (C9)–(C10).
6. **`V₂`, the hard gap against the margin.** By (1.2), `V₂ ⊂ {λ₂a_S² ≤ ε′_V N²}`, with `ε′_V := 4C_ek₊e/c_*`. Use (E₃⁺) with `y = a_S`.
   - *The strip `{a_S ≤ d₁}`* costs `C∫∫_{y≤d₁} λ₂(λ₂²y + r)e^{−cλ₂²} ≤ C(d₁² + rd₁)`.
   - *Away from the strip,* Markov's inequality in `N` gives `1{λ₂y² ≤ ε′_VN²} ≤ N^{10}min(1, (δ_y/λ₂)⁵)`, with `δ_y := ε′_V/y²`. Use (E₃⁺) with the moment `N^{10}`. For each `y`, exactly,

         ∫₀^∞ min(1, (δ/l)⁵) l(l²y + r) dl = (5/4)yδ⁴ + (5/6)rδ².                                    (3.4)

     With `δ = δ_y`, this is `(5/4)ε′_V⁴y^{−7} + (5/6)rε′_V²y^{−4}`. Its integral over `y > d₁` is at most `(5/24)ε′_V⁴d₁^{−6} + (5/18)rε′_V²d₁^{−3}`.
   - *With `d₁ = √ε′_V`*, the strip and the away part add up to at most `C(ε′_V + r√ε′_V) ≤ C(e + r√e)`. Their elementary part is `d₁² + rd₁ + (5/24)ε′_V⁴d₁^{−6} + (5/18)rε′_V²d₁^{−3} = (29/24)ε′_V + (23/18)r√ε′_V` (X9). If `√ε′_V ≥ A_*`, the strip alone suffices.

   The hard gap therefore costs the same as the Taylor term: the margin `v` and the edge strip of (E₃⁺) involve the same `a_S`.
7. **`V₃`, Taylor against the level.** `V₃ ⊂ {−2ϱ ≤ μ < 0} ∪ {2K₀Ne ≥ ϱ}`. Lemma LB₃ (width `2ϱ ≤ 1/2`) bounds the first set by `C(ϱ + r)`. Markov's inequality, with `r^{−5}E_{Q_r}[W_rN^p1_{D_Λ}] ≤ C_p` (proof of FW₃′), bounds the second by `C_p(e/ϱ)^p`. This is C94 (C14).
8. **`V₄`, the hard gap against the level.** `V₄ ⊂ {−2ϱ ≤ μ < 0} ∪ {λ₂ ≤ δ₄N²}`, with `δ₄ := 2C_ek₊e/ϱ`. Lemma LB₃ bounds the first set, and (G₃.3) bounds the second by `C(δ₄⁴ + rδ₄²) = C((e/ϱ)⁴ + r(e/ϱ)²)`.

Adding steps 1–8 and multiplying by `r³/z_r ≤ 2r³/z_*` proves (3.2). ∎

*Proof of (c).* With `w = r^{−1/16}`, `e = r^{3/4}` and `e/ϱ = r^{1/4}`. The exponents of the bracket in (3.2), in order, are

    1/2, 5/4, 3/4, 11/8, 1/2, 1, 1/2, 1, 3/2, 3, 5/2, 7/4.

All are at least `1/2`. For small `r`, the side conditions hold: `w ≥ 5`, `r^{1/2}w = r^{7/16} ≤ 1` and `ϱ ≤ 1/4`. Finally, `E ∖ H_r ⊂ (E ∖ Good^E) ∪ {not Morse}` by (a), and the second set is `Q_r^W`-null ([P] §8). ∎

The ledger is C94's eight terms plus four from the hard gap: `(e/ϱ)⁴`, `r(e/ϱ)²`, `e⁴` and `re²`.

### 4. Lemma SC (the slice chord; deterministic) and Theorem R₃ (the rejected side)

**Lemma SC.** Let `f ∈ C(X)` with `f(M_r) = b` and `f(S_r) = b − kr³`. Let `(u, e₁, e₂)` be an orthonormal frame with `u` the pin axis, and let `k, r > 0`. Let `γ ≠ 0`, `λ̃`, `B` and `C₃` be real numbers with `ψ > |c|` and `0 < μ < 1`. In the application they are the jets of `f` in its eigenframe. Let `Y*` and `K` be as in §0, and `g` as there. Put `e₀ := g(·, ·, 0) − P_QS` on `𝔚_R`, the error of the planar section. If

    sup_K |e₀| < min(μ, 4h_Y),                                                                              (4.1)

then `D_f(M_r) > f(S_r)`. No gradient pin, no barrel and no bound on `λ₂` is used.

*Proof.*
1. By Lemma M₃(f), `P_QS ≥ −h_Y = μ − 1` on `K`, and `P_QS = 4h_Y` at the far end `s = 2`. So `g(·, ·, 0) = P_QS + e₀ > −1` on `K`, and `g > 0` at the far end.
2. Since `K` is compact, `m := min_K g(·, ·, 0) > −1`.
3. The path `s ↦ (M + s(Y* − M), 0)`, `0 ≤ s ≤ 2`, lies in `ℝ³`. It starts at `M̂`, where `g = 0`, and ends where `g > 0`. So `d_g(M̂) ≥ m > −1`.
4. A3.1's (TL) applies to continuous `f` and to paths in `ℝ³` through the covering `π∘Ψ`. It gives `D_f(M_r) = b + kr³d_g(M̂) > b − kr³ = f(S_r)`. ∎

The path lies in the plane through the midpoint spanned by `u` and `e₁`. Only heights along it are used.

**Theorem R₃** ((a) deterministic, (b)–(c) conditional on A3.4). For `0 < r ≤ r₀` and deterministic `w ≥ 5`, define inside `Rsec`

    Good^R(r, w) := Rsec ∩ {ρ_R < w} ∩ {sup_{Ω̄_w}|ℰ(·, ·, 0)| < τ_R}.                                     (4.2)

It is Borel, for the reasons given after (3.1).
- **(a) The certificate.** On `Good^R`, `D_f(M_r) > f(S_r)`. On the Morse locus intersected with `{W_r > 0}`, `H_r` fails.
- **(b) The bad mass.** For `0 < ϱ ≤ 1/4` and finite `p ≥ 1`,

      Q_r^W(Rsec ∖ Good^R) ≤ C r³[w^{−8} + rw^{−4} + e^{2/3} + re^{1/3} + ϱ + r + (e/ϱ)^p].             (4.3)

- **(c) The rate.** With `w = r^{−1/16}`, `ϱ = r^{1/2}` and `p = 2`, `Q_r^W(Rsec ∖ Good^R) ≤ Cr^{7/2}` and `Q_r^W(Rsec ∩ H_r) ≤ Cr^{7/2}`.

*Proof.*
- **(a)**
  - `ρ_R < w` puts the raw image of `K` in `Ω_w`. There `e₀ = ℰ(·, ·, 0)` composed with the chart, so (4.1) holds with room `τ_R < min(μ, 4h_Y)`, and Lemma SC applies.
  - On `{W_r > 0}`, `M_r` is a local maximum and `S_r` has index 2, and `f(S_r) < f(M_r)`. C96's lemma, read contrapositively as in A3.1's Corollary H_d (R), shows that on the Morse locus the class born at `M_r` does not die at `S_r`.
- **(b)** By (FW.0), `sup_{Ω̄_w}|ℰ(·, ·, 0)| ≤ K₀Ne`. This bound is C91's Theorem 1 for the planar section (A3.5 §1, step 4). It uses only the in-plane value and gradient pins of the section, which hold under `Q_r`; the transverse pin and `λ₂` are not used. So `Rsec ∖ Good^R` lies in the union of three sets.
  1. *`{ρ_R ≥ w}`.* Lemma Rad₃ gives `C(w^{−8} + rw^{−4})`.
  2. *`{K₀Ne ≥ 2h_Y}`.* By (1.3) this lies in `{a_M³ ≤ ε_hNP⁶}`, with `ε_h := K₀e/(2c_h)`. Split at `a_M = d₂`. Away from the strip, use Markov's inequality in squared form and (E₃.2) with the moment `N²` and the weight `P^{12}`:

         μ_r ≤ C[d₂² + rd₂ + ε_h²(d₂^{−4}/4 + rd₂^{−5}/5)].

     Take `d₂ = ε_h^{1/3}`; if `d₂ ≥ A_*`, the strip alone suffices. This gives `C(e^{2/3} + re^{1/3})`, as in C97 (R16)–(R17).
  3. *`{K₀Ne ≥ μ/2}`.* This lies in `{0 < μ ≤ 2ϱ} ∪ {K₀Ne ≥ ϱ}`. Lemma LB₃ and Markov's inequality give `C(ϱ + r + (e/ϱ)^p)`, as in C97 (R18).

  Multiply by `r³/z_r`.
- **(c)** The exponents of (4.3), in order, are `1/2, 5/4, 1/2, 5/4, 1/2, 1, 1/2`. The second statement follows from (a), since `{W_r = 0}` and the non-Morse set are `Q_r^W`-null. ∎

### 5. Theorem BL₃ (the bounded layer in `d = 3`; conditional on A3.4)

Put `m_E := μ₀(E)`, `m_R := μ₀(Rsec)` and `m_Λ := μ₀(D_Λ)`, and write `ϑ := (λ̃, λ₂, θ, t)`.

**Theorem BL₃.** Uniformly in `b ∈ B₀`, `k ∈ [k₋, k₊]` and the frame, for `0 < r ≤ r₀`:

    (a)  E = D_Λ ∩ T ∩ {γ ≠ 0, μ < 0},    m_Λ = m_E + m_R,    0 < m_* ≤ m_E, m_R ≤ m_Λ ≤ m^* < ∞;
    (b)  Q_r^W(D_Λ ∩ (H_r Δ E)) ≤ C r^{7/2};
    (c)  Q_r^W(D_Λ ∩ H_r) = r³m_E/z₀ + O(r^{7/2}),    Q_r^W(D_Λ ∖ H_r) = r³m_R/z₀ + O(r^{7/2});
    (d)  Q_r^W(H_r | D_Λ) = m_E/m_Λ + O(√r),  and  m_*/m^* ≤ m_E/m_Λ ≤ 1 − m_*/m^*;
    (e)  for every bounded Borel φ on D_Λ × {0, 1},
         |r^{−3}E_{Q_r^W}[1_{D_Λ}φ(ϑ, 1_{H_r})] − z₀^{−1}∫_{D_Λ} φ(ϑ, 1_E(ϑ)) dμ₀| ≤ C‖φ‖_∞ √r.

*Proof.*
1. **Coverage.**
   - Lemma M₃(g) gives the first identity in (a).
   - The neutral set `T ∩ {γ ≠ 0, μ = 0}` lies in `{F = 0}`. For each `θ`, the map `t ↦ (γ, B, C₃)` is linear and onto `ℝ³`. So for fixed `(λ̃, λ₂, θ)`, `F` is a polynomial in `t`. It is nonzero, because it is quadratic in `C₃` with leading coefficient `(576k²)² ≠ 0`. Likewise `γ` is a nonzero linear function of `t`.
   - By Fubini, `{F = 0}` and `{γ = 0}` are Lebesgue-null in `ϑ`. Both `μ_r` (J₃.18) and `μ₀` (J₃.2) have densities, so these sets are null for both.
   - Since `g₀ = 0` off `T`, `m_Λ = m_E + m_R`.
2. **Positive masses.**
   - *An elder witness.* Take `λ̃ = Λ/2`, `γ = 1`, `B = (1 + 6Λ)/(12k)` and `C₃ = (4 + 72Λ)/(576k²)`. Then `ψ = 12Λ`, `c = −6Λ` and `R = 0`.
     - By C82 (7), for `c < 0` an extra critical point needs `R² + 64c(ψ² − c²) ≥ 0`. Here this quantity is `−64·6Λ·108Λ² = −41472Λ³ < 0`. The condition is open, so `μ = −∞` on a neighbourhood.
     - Also `ψ > 2c`, `R² < 16(ψ − 2c)²(ψ + c)` and `a_M, a_S > 0`. These are strict and persist.
     - This is C94's witness in the present normalization.
   - *A rejected witness.* Take `λ̃ = Λ/2`, `γ = 1`, `B = 1/(12k)`, `R₀ := √(32ψ³)` and `C₃ = (R₀ + 4)/(576k²)`. Then `c = 0`, `R = R₀`, and `a_M = a_S = 3Λ > 0`, so `T` holds strictly at an interior point of `D_Λ`.
     - The only extra saddle is `σ = 1`, `Z = 48ψ/R₀`, with `P_QS = −1/2` and `det Hess P_QS = −ψ/4 < 0`. So `μ = 1/2`. This is C97's witness.
     - A small neighbourhood keeps `0 < μ < 1`, by continuity of the nondegenerate saddle.
   - *The masses.* The set of `ϑ` with `λ₂ ∈ [1, 2]`, `|t| ≤ T₀` and `(λ̃, γ, B, C₃)` in either neighbourhood has positive Lebesgue measure, by step 1's surjectivity. There `g₀ = k^{−1}λ₂³ρ₀(A₀, t)w_λ` is bounded below, uniformly in the compact parameters, by Lemma CM₃(a). The upper bound is `m_Λ ≤ m^*` (J₃.4).
3. **The error (b).**
   - `D_Λ ∩ (H_r Δ E)` lies in `(E ∖ H_r) ∪ (Rsec ∩ H_r) ∪ (D_Λ ∩ T^c)`, up to the null sets of step 1.
   - Theorems E₃(c) and R₃(c) bound the first two by `Cr^{7/2}`. (E₃.6) bounds the third by `Cr⁴`.
4. **Masses and the conditional probability, (c)–(d).** By (J₃.5), `Q_r^W(E) = r³m_E/z₀ + O(r⁴)`, and likewise for `D_Λ`. Add or subtract (b). Divide by `Q_r^W(D_Λ) = r³[m_Λ/z₀ + O(r)]`, whose bracket has a uniform positive floor. Step 2 gives `m_E/m_Λ ≥ m_*/m^*` and `m_R/m_Λ ≥ m_*/m^*`.
5. **The joint measure, (e).** This is C98 §4.
   - Replacing `1_{H_r}` by `1_E` changes the integrand only on the mismatch set, by at most `2‖φ‖_∞`. After the `r^{−3}` rescaling this costs `C‖φ‖_∞√r`.
   - Then `r^{−3}E_{Q_r^W}[1_{D_Λ}φ(ϑ, 1_E)] = ∫_{D_Λ}φ(ϑ, 1_E)g_r/z_r dϑ`, and (J₃.5) gives the `Cr‖φ‖_∞` comparison. ∎

### 6. Remarks

1. **The rejected side needs no barrel.**
   - Lemma SC replaces A3's QS-R_d and the rejected half of A3.1's Theorem C_d for the purpose of rejection. Those used the reduced height and the hypotheses (B1)–(B2). The slice uses neither, nor the gradient pin, nor any lower bound on `λ₂`.
   - The lifted chord would need only a lower bound on `G − P_QS ≥ e₀`, but `G` exists only on a barrel. The slice needs no barrel.
   - So `(D₃)`'s hard-gap term never enters the rejected side, and Theorem R₃ is C97 with A3.4's law.
2. **Why the hard gap costs nothing extra on the elder side.**
   - Against the margin `v ≥ c_*a_S²`, the term `C_ekN²e/λ₂` gives the two-variable small-ball event `{λ₂a_S² ≲ N²e}` (step 6). Its mass, `C(e + r√e)`, comes from (E₃⁺)'s joint density `λ₂(λ₂²a_S + r)`.
   - Against the level `−μ`, it reduces to the hard-gap strip of (G₃.3) at width `e/ϱ` (step 8).
   - The conditional error is `O(√r)`, as in `d = 2`. The rate is not optimized.
3. **What is planar and what is not.** The sectors `E` and `Rsec`, the margins and the chord are the planar ones, through QS §7's chart. The hard direction enters through the barrel `(B_r)`, the reduced height's `1/λ₂` and the weight `λ₂³` of `g₀`. For `d ≥ 4`, A3.4 Remark 3's caveats apply: a `d`-dimensional W3, and several hard eigenvalues.
4. **Not a rate for `1 − p_r`.** In `d = 2` the planar chain reaches `1 − p_r = r³(α₁ + α₂) + O(r^{13/4})` (C101 and C103 in `frontiers/planar_soft_layer_chain_20261003/`). It also uses the failure raw-jet measure in variation and the local endpoint margin of A4 ([5972396791](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5972396791)). Neither is done here in `d = 3`.

### 7. Checks

**Exact controls** (`a36_exact.py`; companion comment). Standard library only; exact rationals, with rigorous rational bounds for square roots; byte-identical output with `-O`.

| Group | What it checks |
|---|---|
| X1 | (0.1) and Lemma M₃(a): `G_k(u − Z/12, Z/γ) = P_QS(u, Z)`, `D = −4Y`, `a_M = γ²(ψ − c)/4`, `a_S = γ²(ψ + c)/4`, on 400 rational jets |
| X2, X3 | (1.1), and M₃(c) (arithmetic consistency) |
| X4 | the raw forms of `τ̂_M` and `τ̂_S` (rational, after squaring the `R`-terms) |
| X5 | (1.2): the constant `16`, `c_* = 3/(250A_*²) = 1/(12000Λ²)` and `27/512 > 3/250`. On 1,500 points of A1's elder side intersected with `D_Λ`, which contains `E` (`μ` is not evaluated): `m_S ≥ c_*a_S²` and `τ̂_M ≤ 4a`, both in the rigorous direction, and the equality case of the latter |
| X6 | (1.3): the jet bounds `|γ| ≤ |t|` and `|B|, |C₃| ≤ 2P` in rational frames, the bounds on `|D|` and `|J|`, the three-term square inequality and `τ̂_M² ≤ C_τP⁶/a_M³`, including 20 near-extremal jets for the `C₃` term. The bound is crude, so this is a consistency check, not a sharpness check |
| X7 | Lemma Rad₃: the two radius equivalences; `72U⁴`, `6U²` and C94's `288U⁴ = 4·72U⁴`, computed independently by Simpson's rule (exact for these polynomials) |
| X8 | C82's exact value `J_δ(0, R) = δR²/24` (from the critical point, its height and the `ψ`-integral), and the conversion in Lemma LB₃ step 2 |
| X9 | (3.4), checked against an independent computation (Simpson on `[0, δ]`; the substitution `l = δ/x` and Simpson beyond); the Markov majorant of step 6; the away integral (substitution and Boole's rule); the total `(29/24)ε′_V + (23/18)r√ε′_V` |
| X10 | the splits of step 5 and of Theorem R₃(b), with their integrals checked by substitution and Simpson or Boole |
| X11 | the two exponent ledgers and their minima |
| X12 | the two witnesses in the `d = 3` normalization, including the discriminant `−41472Λ³` of C82 (7) (exact at `Λ = 6`, `ψ = 72`, `R₀ = 3456` for the rejected one) |
| X13 | M₃(f) on 400 exact rational extra saddles with general `c` (QS Q4's construction: `σ ∈ (−1, 3)`, `0 < h < 1`), and `K ⊂ 𝔚_R` |
| X14 | M₃(g): `F`'s leading coefficient `(576k²)²`, and exact neutral points with `P_QS + 1 = 0` on `R² = 16(ψ − 2c)²(ψ + c)` |
| X15 | Appendix A: the threshold `1/8`, the integral floor, the exponent range `3/16 < β < 1/4` at `p = 4`, and `w_λ ≥ 5Λ²/4` on the box |
| X16 | on X13's saddles, with jets built from `(ψ, c, R)`: C97 (R7) `h_Y ≥ 4/(27τ̂_M²)` and the chain to `c_h a_M³/P⁶`, both in the rigorous direction |
| X17 | the inclusions of Theorem E₃'s steps 2 and 4–8 and of Theorem R₃(b), tested at their boundaries, so that each factor in `ε_V`, `ε′_V`, `δ_B`, `δ₄` and `ε_h` matters |

Mutants M1–M13 each change one formula and exit 1, naming the failing groups; bad arguments exit 2.

**Exploration** (outside the repository; floating point, not part of the proofs).
- *The margins.* 2 × 10⁶ random points were drawn on A1's elder side, which contains `E`; `μ` was not evaluated. The largest ratios were `τ̂_M/(4a) = 1.0000`, at `c/ψ = 1/2` and `R = 0`, and `τ̂_S` over the bound of (1.2) `= 1.0000`, at `R² = 16(ψ − 2c)²(ψ + c)`. Both maxima lie on the boundary of `E`, where `μ = 0`, and are approached from inside `E`.
- *The small ball.* For the majorant of (E₃⁺) with `c = 1`, the mass of `{λ₂y² ≤ ε}` divided by `ε + r√ε` stays in `[0.21, 0.61]`. This was computed by quadrature for `ε ∈ [10⁻⁸, 10⁻²]` and `r ∈ {0, 10⁻⁴, 10⁻²}`. So step 6's form `e + r√e` is sharp for the majorant.

### 8. Not claimed

- No `d = 3` rate for `1 − p_r`, no `Λ → ∞`, no gap marks outside `[k₋, k₊]`, no `d ≥ 4`.
- Every weighted statement is conditional on A3.4, hence on A3.3 (W3, Lemma P and the window identity). The geometric inputs are A3, A3.1 and C96, at their reviewed scope.
- Lemma SC, the certificates and the identities of §1 are deterministic.
- The constants are explicit where displayed, and crude. The `C` of §§2–5 are not numerical.

### 9. Review request

A bounded nonauthor read in three slices. Please claim first.
- **Slice 1.** §1 (Lemma M₃) and §4 (Lemma SC, Theorem R₃), with X1–X8, X10–X13 and X16.
- **Slice 2.** §2 (Lemmas Rad₃ and LB₃) and §3 (Theorem E₃), with X5, X7–X11 and X17.
- **Slice 3.** §5 (Theorem BL₃), §6 and Appendix A, with X12, X14 and X15.

A replay of `a36_exact.py` (both modes, M1–M13) can go with any slice.

### Appendix A. A3.5 riders (from [6001626468](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6001626468))

**Proposition G₃⁻** (author-side, conditional on A3.4 like Theorem G₃). Let `w = r^{−β}` with `1/8 < β < 1/4`. Then `Q_r^W(D_Λ ∖ G₃) ≥ c r^{7−16β}` for `0 < r ≤ r₁`. With (G₃.5) at `p ≥ 4`, `Q_r^W(D_Λ ∖ G₃) ≍ r^{7−16β}` for `3/16 < β < 1/4`, so `3/16` is sharp for `G₃`.

*Proof.*
1. **Inclusion.** Put `δ := C_Bk₋rw⁴`. Since `N ≥ 1` and `k ≥ k₋`, `{λ₂ ≤ δ} ⊂ (B_r)^c ⊂ G₃^c`, by (G₃.1).
2. **A box.** Take A3.4's box from the proof of (J₃.4): `λ̃ ∈ [Λ/4, Λ/2]` and `|t| ≤ δ_Λ`. There `w_λ ≥ 5Λ²/4` and `λ̃ > 0`, so box `× {λ₂ > 0}` lies in `D_Λ ∩ T`. Also `ρ₀(A₀(λ₂, θ), t) ≥ 2ϖ₀ > 0` for `λ₂ ∈ [0, 1]`.
3. **A density floor.** For `λ₂ ∈ [C′r^{1/2}, δ]`, with `C′` large:
   - `(λ₂ − rλ̃/k)₊ ≥ λ₂/2`;
   - `ρ_r(Ψ_r, t) ≥ ϖ₀`, by (J₃.9′) together with the shift `|Ψ_r − A₀| ≤ rΛ/k₋` and the Lipschitz bound on `ρ₀` (A3.4, Theorem J₃, step 1);
   - `E_r ≥ λ₂²w_λ − CrP^{25} ≥ λ₂²w_λ/2`, by (J₃.17).

   So (J₃.18) gives `g_r ≥ ϖ₁λ₂³`.
4. **Integration.** `β > 1/8` gives `δ ≥ 2C′r^{1/2}` for small `r`, and `β < 1/4` gives `δ ≤ 1`. So `μ_r(box × [C′r^{1/2}, δ]) ≥ ϖ₂δ⁴`. Then `Q_r^W = r³μ_r/z_r` with `z_r ≤ 2z^*` gives `Q_r^W(D_Λ ∖ G₃) ≥ cr³δ⁴ = c′r^{7−16β}`. ∎

The additive error of (J₃.17) enters multiplied by the Jacobian `λ₂`, so it costs `rλ₂` against `λ₂³`. That is the source of the threshold `1/8`, which A3.5's Remark 1 already noted. Grok Bot agent 15 proposed the argument (S3-O2, with threshold `1/6`); the inclusion needed is `G₃ ⊂ (B_r)`.

**Wording notes.**
- **S1-O1.** Lemma FW₃ is stated for `k ∈ [k₋, k₊]`, as in A3.4 §0. It needs no torus condition such as C91's (W0), because `f∘π` is a function on `ℝ³` and the bounds are Taylor bounds.
- **S1-O2.** In step 5 of FW₃'s proof, the bound on `Q − r²ka₂` is divided by `kr^{3/2}`. The constants `A₁` and `A₃` use `w ≥ 1`, which absorbs `w⁰` and `w¹` into `w³` and `w²`.
- **S1-O4.** The near-attainment ratios in A3.5 §7 are relative to the script's box-local bound for `N`, not to the global operator-norm `N` of the lemma.
- **S3-O1.** A3.5 §8's list of conditional inputs also includes A3.4 §5 step 1 (the change of variables `B → a_i`) and Lemma CM₃(b)'s majorant of `ρ_r`. Neither uses W3 or Lemma P.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_