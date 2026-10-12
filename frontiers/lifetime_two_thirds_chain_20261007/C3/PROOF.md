# Lifetime note C3: the `ℓ^{2/3}` term of the candidate density

Object: `CL-C3-CANDIDATE-TWO-THIRDS-20261006-v1`. Claim: main#229 6026342638.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 6 October 2026, for Dylan Roy (delegated AI
work). The same session wrote #218, #229, #237 and #242, and notes TL, TS, EM, EM.1 and LU. The consumed packets in turn
consume OpenAI-authored sources, among them [R], [P] and [Z].
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph, STATUS,
PROOF_INDEX, prize or Boolean change; no numerical constant is certified. Same GitHub account as every lane;
organizational independence 0. Before posting, three clean-context Claude subagents of this session refereed the draft in
three slices. All three returned AMEND. The one blocking finding (Slice C) was the scope of Corollary G′: it claimed
sharpness for the model field, for which Theorems P⁺ and C3 are not stated. Corollary G′ is now about the model value of
`c₃`. Every finding is applied here, four of them differently from the proposal: C-1 and C-2 by a new result,
Proposition G″, which transfers the sign to the torus field for large `L`, in place of the proposed hedges; C-7 by the
Slice A referee's independent Monte Carlo table; and C-13 by a derivation in control E4. Proposition G″, controls E7–E9 and
the numerics now in Remark 6 were added after the three slice reads. A fourth clean-context subagent then read the
changes, including Proposition G″ and E7–E9. It returned AMEND with no blocking finding (Proposition G″'s neighbourhood of
jet laws must consist of parity-split ones), and its findings are applied. The controls comment lists every finding. These
are author-side reads and earn no review credit.

**What is new.**
- **Lemma F₃ (the fold layer at order `r`)** (§2). At every fixed gap `k > 0`, the typed-minus-surrogate difference is
  `𝐓_r(k) − 𝐒_r(k) = r𝐋_F(k) + o(r)`, with an explicit coefficient
  `𝐋_F(k) = (12/(9k))p_{V_0}(v(k))𝔼_k[P²|3kB_ee − γ_e²/4|³; λ_max(A) = 0⁻]` (§0).
  - The difference is the layer `{|x| ≥ y}` of the typed region near `λ_max(A) = 0`. Here `e` is the null eigenvector of
    `A`, `P` the product of its other eigenvalues, and `𝔼_k[·; λ_max(A) = 0⁻]` the edge density of `λ_max(A)`.
  - The strip where `A < 0` but `A_M` is not negative definite adds nothing. For small `r`, off a set that costs `o(r)`,
    the Schur complement of `A_M` in the scaled endpoint Hessian `K_M` is negative there, so the strip lies inside the
    layer.
  - #218's Lemma F, with #237 Lemma K, bounds this difference by `O(r(1 + k^{−1}))`; Lemma F₃ identifies it to `o(r)`.
- **Lemma T₁ (the cusp tail)** (§3). `κ(𝓐(κ) − 𝐀₂(0)) → a₁ := (12/9)p_{V_0}(v(0))𝔼_0[P²(γ_e²/4)³; λ_max(A) = 0⁻]`, and
  `a₁ = (1/10)∫F₀db` with #242's `F₀`.
- **Theorem C3** (§4). In every `d ≥ 2`,
  `ν_cand(ℓ) = cℓ^{−1/3} + B_{d,L} + I^{cand}ℓ^{1/4} + c₂ℓ^{1/3} + c₃ℓ^{2/3} + o(ℓ^{2/3})`, with
  `c₃ = (1/3)∫_S∫_0^∞[𝐋_F(k, u) − a₁(u)/k]k^{−5/3}dk dσ(u)`. This identifies the remainder of note LU's Theorem P⁺ at its own
  order. It is #237 Remark 2's fold-scale term ("plausibly the next term"), and the "`ℓ^{2/3}` term of `ν_cand`" that #242
  Conjecture 7's Remark 1 leaves open ("the typed boundary `λ ≍ r` also produces an `|r|³` term in the candidate kernel").
- **Proposition G (Gaussian kernel)** (§5). For the model case `C(z) = e^{−|z|²/2}` on `R^d` and every `d ≥ 2`, the
  coefficient (C3), evaluated on the model's jet law, is `(J/30)∫_S∫_RF₀ db dσ`, with
  `J := (16/15)∫_0^∞e^{−12k²}E[(3kB − γ²/4)₊³]k^{−8/3}dk > 0` (`γ`, `B` independent `N(0, 2)`).
  - A Gamma-function identity cancels exactly the contribution of `E[X³] = 15/8 + 27k²`, together with the density factor
    `e^{−12k²}` and the cusp-tail subtraction. This leaves `J` as the integral of a positive function, so the model value of
    `c₃` is positive (Corollary G′).
  - Numerically (exploration; §5) `J = 4.1977820`, and the model value of `c₃` is `0.0127896` (`d = 2`) and `0.0160923`
    (`d = 3`), so `c₃/c_{d,∞} = 0.174229` and `0.385205`.
- **Proposition G″ (the torus field for large `L`)** (§5). Near the model's jet law at `0`, the coefficient `c₃` is a
  continuous functional of the jet law among those of stationary fields, and the torus field's jet law tends to the model's
  as `L → ∞`. So the torus field's `c₃(L)` tends to the model value. For `L ≥ L₀(d)` it is positive, and then the torus
  field attains the remainder `O(ℓ^{2/3})` of note LU's Theorem P⁺. `L₀(d)` is not quantified.

**Not claimed.**
- No rate: the remainder is `o(ℓ^{2/3})`, by dominated convergence (Remark 4).
- Nothing about `ν_eld` or `ρ_rej` beyond one equivalence. With Theorem C3, Conjecture 7 of #242 (with `o(ℓ^{2/3})` in place
  of `O(ℓ^{3/4})`) is equivalent to an `ℓ^{2/3}` term `(c₃ − R_{2/3})ℓ^{2/3}` of the near elder density
  `ν_eld − ν_eld^{far,r_0^*}` (Remark 3). That conjecture stays open.
- No change to any statement of #218, #237, #242, note LU or the notes it consumes.
- No certified number. The numerical values of §5 are exploration (quadrature), and the sign of the model value of `c₃` is
  proved, not certified. For the torus field the sign of `c₃(L)`, and so the sharpness of Theorem P⁺, is proved only for
  `L ≥ L₀(d)` with `L₀(d)` not quantified: nothing is proved at `L = 24` (Remark 5).
- Nothing pointwise in `b`; no uniformity in `d` or `L`; nothing beyond the existential scope of the consumed sources.

**Consumed.**
- Note LU (main#229 6025486512, with successor text 6026230530; Slice A PASS 6025530037, Slice B AMEND 6025531584, readback
  PASS 6026231785, Slice C PASS 6025535376): §0 (the setting); Lemma S (S.4) (typedness when `A_M, A_S < 0`, used in §2
  Step 2) and its scaled Hessians `K_i = D_r^{−1}H_iD_r^{−1}`; Theorem U⁼, and §4's proof of Theorem P⁺ (the decomposition at
  a fixed split `ρ`, the absorption of `J₂`, the main terms and `J₃`–`J₅`); §2's paragraph on `𝔗` (the deterministic form of
  Lemma Π).
- #237 `frontiers/candidate_parity_rate_20261001/PROOF.md` (blob `a97bf528`): the setting of §§0–2; Lemma R; Lemma Π in
  the deterministic form of its proof; the polynomials (2.1); Lemma K ((K.1), and `𝐀₂(0, u) = ∫A₂(b, 0, u)db`); Step U2 (a)
  (the layer device); Step U4 (the formula for `𝓐`, and the disintegration of (R.1) at `r = 0`).
- #218 `frontiers/candidate_third_order_20261001/PROOF.md` (blob `70ca57ef`): §0 and (F.2) (the value `𝐀₂(0)`); Lemma D and
  its proof (Weyl's integration formula and the Vandermonde cancellation); Lemma O's proof (the dyadic layers of `|Y|`);
  (1.2); Step F1.
- #229 `frontiers/third_order_rate_20261001/PROOF.md` (blob `110ed33a`): (W⁺.2) at `κ = 0`.
- #242 `frontiers/soft_rejected_pairs_20261002/PROOF.md` (blob `271412db`): Theorem 1's definitions (1.0a) and (1.0) of `𝔇`
  and `F₀`, and the positivity `𝔇 > 0`, with its proof's Weyl-coordinate argument (1.1a)–(1.1b) and the uniform bound of its
  proof of Corollary 1′; Corollary 1′ (the values of `∫∫F₀`); §0 (the model case, and the torus field's covariance as the
  periodization of `C`, which agrees with `C` up to `O(e^{−L²/8})`).

**Cited only.**
- #237's README (review record: the author-side referee's `k²/κ` coefficient of the layer), #237 Remarks 2 and 4, note TL's
  Remark 2 (the rejected fold limit `F − F₀`), note LU's Remark 2.
- #242's Lemma 5 and Conjecture 7, #244 (`R_{2/3}`, numerically), and #229's Corollary R⁺ (`ρ_rej = ν_cand − ν_eld`), for
  Remark 3.
- #216 and #223 (the values of `c_{2,∞}`, `c_{3,∞}`, and #223's `c₂`), for the ratios `c₃/c` and Remark 3's count ratios;
  #207 §8's values of `c₁`, for the same; #207 §8 Remark 3 (the SIDE24 jet covariances), for Proposition G″ and Remark 5.
- Note LU's Corollary LU (the SIDE24 relative remainder) and addendum EM.1 (the intermediate elder mass); #242 §4's inputs
  (i)–(ii), its matched-asymptotics count, and Conjecture 7's Remark 1; #216's Monte Carlo of the elder density; #220 (0.2)
  (the elder coefficient `c₁`); #187 and #188 (the far elder density); note TL's Corollary TL1; and #243 Theorem FL (through
  note TL's Remark 2). All are for Remarks 3–4 and the header.

**Prior work and overlap.** I searched main#229, #259 and #275 and the Math- tree at `34618d0d`. The term is named, not
identified, in #237 Remark 2 ("It is plausibly the next term, but neither its non-vanishing nor the sharpness of Lemma Λ is
proved"), in #237's README (the author-side referee's numerics: "The `k²/κ` coefficient of the layer was nonzero, about
`+0.005`"), in #242 Conjecture 7's Remark 1, and in note LU's Remark 2. Note TL's Remark 2 concerns the analogous `k²/κ`
term of the rejected kernel, which carries `R_{2/3}`, not this term. No packet or claim identifies it. This note's claim is
6026342638.

## 0. Setting and statements

Setting and notation are #237's (§§0–2) and note LU's (§0). In particular: `m = d − 1`, `s := (−1)^m`; the pins
`M = −ru/2`, `S = ru/2`; the rows `V_r`, the target `v(k) = (0_d, 0_d, 12k)`, the density `p_{V_r}` and the law `Q̄_{r,k}`
(#237 (1.1)); the scaled endpoint Hessians `K_M`, `K_S`, and `Π = −det K_M det K_S`; the kernel and its fixed-cone
surrogate (#237 (R.1))

    𝐓_r(k, u) = 12p_{V_r}(v(k))E_{Q̄_{r,k}}[r^{−2}Π 1_{typed}],        𝐒_r(k, u) = 12p_{V_r}(v(k))E_{Q̄_{r,k}}[r^{−2}Π 1{A<0}];

`𝐀_0`, `𝐀₂` (Lemma K), `𝓐(κ, u) = ∫_R(𝒜^{cand} − 𝒜^{con})(b, κ, u)db` and `κ = k/r`. The jets at `0` are `A = ∇_Θ²f(0)`,
`B = ∂_uA`, `γ = ∇_Θ∂_u²f(0)`, `f₄`, …; `Δ = det A`, `A^♯ = adj A`, `Δ_B = tr(A^♯B)`, `Y′ = (f₄/12)Δ − γᵀA^♯γ/4`, and
`U = Y′ + 3kΔ_B`, `V` as in #237 (2.1), built from the jets of the field at gap `k`. Constants `C, c, N` depend only on `d`
and `L`, except where a dependence on `k` is stated.

*The edge.* The eigenvalues `λ₁ ≤ ⋯ ≤ λ_m` of `A` are simple almost surely. Put `λ := λ_m`, let `e` be a unit eigenvector for
`λ_m` (determined up to sign), and put

    P := λ₁⋯λ_{m−1}  (P := 1 if m = 1),    B_ee := eᵀBe,    γ_e := eᵀγ,    U_red := 3kB_ee − γ_e²/4.                (0.1)

`U_red` is even in `e`. For a law `Q` of the jets and a measurable `φ ≥ 0` put

    𝔼_Q[φ; λ_m = 0⁻] := lim_{ε↓0} ε^{−1} E_Q[φ 1{−ε < λ_m < 0}]                                                    (0.2)

when the limit exists. Write `𝔼_k` for `𝔼_{Q̄_{0,k}}` and define, for `k ∈ R` and `u ∈ S^{d−1}`,

    𝔏(k, u) := 𝔼_k[P²|U_red|³; λ_m = 0⁻],        𝐋_F(k, u) := (12/(9k)) p_{V_0}(v(k)) 𝔏(k, u)   (k > 0),
    a₁(u) := (12/9) p_{V_0}(v(0)) 𝔏(0, u),        𝐄(k, u) := 𝐋_F(k, u) − a₁(u)/k.                                (0.3)

At `k = 0`, `U_red = −γ_e²/4` and `𝔏(0, u) = 𝔼_0[P²γ_e⁶; λ_m = 0⁻]/64`.

**Lemma 0 (the edge expectations).** The limits (0.3) exist. `𝔏(·, u)` is continuous and even on `R`, with
`𝔏(k, u) ≤ C(1 + |k|)^N`, uniformly in `u`. Moreover `𝔏(k, u) = 𝔼_A[P²h_k(e); λ_m = 0⁻]`, where
`h_k(e) := E_{Q̄_{0,k}}[|U_red|³ | A]` depends on `A` only through `e`.

**Lemma F₃ (the fold layer at order `r`).** For every `k > 0` and `u`,

    lim_{r↓0} (𝐓_r(k, u) − 𝐒_r(k, u))/r = 𝐋_F(k, u).                                                              (F₃)

**Lemma T₁ (the cusp tail).** For every `u`, `lim_{κ→∞} κ(𝓐(κ, u) − 𝐀₂(0, u)) = a₁(u)`. Moreover `a₁(u) = (1/10)∫_RF₀(b, u)db`,
with `F₀` as in #242 (1.0).

**Theorem C3 (the `ℓ^{2/3}` term of the candidate density).** In every `d ≥ 2` and for every `L`, `|𝐄(k, u)| ≤ C min(k, 1/k)`
for `k > 0`, and as `ℓ ↓ 0`

    ν_cand(ℓ) = c ℓ^{−1/3} + B_{d,L} + I^{cand} ℓ^{1/4} + c₂ ℓ^{1/3} + c₃ ℓ^{2/3} + o(ℓ^{2/3}),
    c₃ := (1/3) ∫_{S^{d−1}} ∫_0^∞ 𝐄(k, u) k^{−5/3} dk dσ(u).                                                       (C3)

**Proposition G (the Gaussian kernel).** Let `C(z) = e^{−|z|²/2}` on `R^d` (the model case of #242 §0), `d ≥ 2`, and
evaluate (0.3) and (C3) on the model's jet law. Then:
- (G.1) For every `k` and every unit `e ⊥ u`, under `Q̄_{0,k}` the pair `(γ_e, B_ee)` is independent of `A`, and its law is that
  of two independent `N(0, 2)` variables, not depending on `k`. Moreover `p_{V_0}(v(k)) = e^{−12k²}p_{V_0}(v(0))`.
- (G.2) Put `g(k) := E|3kB − γ²/4|³` for independent `γ, B ~ N(0, 2)`. Then `g(0) = 15/8` and
  `𝐄(k, u) = (a₁/k)(e^{−12k²}g(k)/g(0) − 1)`, with `a₁ = (1/10)∫F₀db` independent of `u`.
- (G.3) `c₃ = (J/30)∫_{S^{d−1}}∫_RF₀ db dσ`, where

      J := ∫_0^∞ (e^{−12k²}g(k)/g(0) − 1) k^{−8/3} dk = (16/15) ∫_0^∞ e^{−12k²} E[(3kB − γ²/4)₊³] k^{−8/3} dk > 0.        (G)

  With #242's Corollary 1′, `c₃ = J·5√3/(288π²)` in `d = 2` and `c₃ = J·25√30/(1152π³)` in `d = 3`.

**Corollary G′ (the model value is positive).** For the Gaussian kernel, the coefficient `c₃` of (C3), evaluated on the
model's jet law, is positive. By Theorem C3, for any field to which it applies and whose `c₃` is nonzero, the remainder
`O(ℓ^{2/3})` of note LU's Theorem P⁺ is of exact order `ℓ^{2/3}`. Theorems P⁺ and C3 are stated for the torus field of #237
§0; Proposition G″ transfers the sign to it for large `L`.

**Proposition G″ (the torus field for large `L`).** Let `c₃(L)` be the coefficient (C3) of the torus field of side `L`
(#237 §0). Then `c₃(L) → (J/30)∫_{S^{d−1}}∫_RF₀ db dσ` as `L → ∞`, with the model's `F₀`. Hence there is `L₀(d)` such that,
for `L ≥ L₀(d)`, `c₃(L) > 0`, and the remainder `O(ℓ^{2/3})` of note LU's Theorem P⁺ is of exact order `ℓ^{2/3}` for the
torus field. `L₀(d)` is not quantified here.

## 1. The edge and two identities

*Proof of Lemma 0.* By #237 Lemma R (R.2) at `r = 0`, the odd jets are independent of the even ones, and their law under
`Q̄_{0,k}` has a mean linear in `k` and a covariance independent of `k`; the law of `A` does not depend on `k`. So
`E_{Q̄_{0,k}}[P²|U_red|³1{−ε < λ_m < 0}] = E_A[P²h_k(e)1{−ε < λ_m < 0}]`, with `h_k(e)` a Gaussian expectation of
`|3kB_ee − γ_e²/4|³` that is continuous in `(k, e)` and `≤ C(1 + |k|)^N`. Under Weyl's integration formula
`A = O diag(λ)Oᵀ`, `dA = c_m|V(λ)|dλ dO` (#218 Lemma D's proof; #242 (1.1a)), the law of `A` has the density
`c_m|V(λ)|p_A(O diag(λ)Oᵀ)` in `(λ, O)`, with `p_A` a nondegenerate Gaussian density. This density is continuous in `λ_m`
across `0` on `{λ_{m−1} < 0}`, and `P²h_k(e)` does not depend on `λ_m`. Dominated convergence (the Gaussian factor dominates
`P²(1 + |V|)`) gives the limit,

    𝔏(k, u) = c_m ∫∫_{λ₁<⋯<λ_{m−1}<0} P² h_k(Oε_m) |V(λ₁, …, λ_{m−1}, 0)| p_A(O diag(λ₁, …, λ_{m−1}, 0)Oᵀ) dλ′ dO,      (1.1)

which is continuous in `k` and bounded as stated. Evenness: by Lemma R (R.3) at `r = 0`, the reflection maps `Q̄_{0,k}` to
`Q̄_{0,−k}`, fixes `A` and negates the odd jets, and `U_red(−k; −B, −γ) = U_red(k; B, γ)`. ∎

**Two identities.** Let `A` have simple top eigenvalue `λ`, unit eigenvector `e`, and the other eigenpairs `(λ_j, e_j)`.
- (I.1) *The adjugate at the edge.* `Δ = λP` and `A^♯ = P eeᵀ + λR`, with `R := Σ_{j<m}(∏_{i<m, i≠j}λ_i)e_je_jᵀ`.
  Consequently

      Y′ = P(−γ_e²/4) + λW₀,    U = P·U_red + λW,    W₀ := Pf₄/12 − γᵀRγ/4,    W := W₀ + 3k tr(RB).                   (1.2)

  Indeed `A^♯` has the eigenvalues `∏_{i≠j}λ_i` on `e_j`; for `j = m` this is `P`, and for `j < m` it contains the factor `λ`.
  Then `γᵀA^♯γ = Pγ_e² + λγᵀRγ` and `Δ_B = PB_ee + λ tr(RB)`. These are polynomial identities in the eigen-coordinates
  (control E1).
- (I.2) *The layer integral.* For `a ≥ 0` and `β > 0`, `∫_{−∞}^0 (a² − β²λ²)₊ dλ = 2a³/(3β)`. With `a = |P||U_red|` and
  `β = 6κ|P|` this is `P²|U_red|³/(9κ)` (control E2).

## 2. Proof of Lemma F₃

Fix `k > 0` and `u`; constants below may depend on `k`. Let `g ~ Q̄_{r,k}`, write `E` for `E_{Q̄_{r,k}}`, and let
`𝔗 := 1 + ‖g‖_{C^{N₀}(𝔅)}` (the fixed-`k` analogue of note LU §2's `𝔗`), with `E[𝔗^p | J] ≤ C_p(1 + k + |J|)^p` for the
free-jet vector `J` (#218 (1.2); #237 Lemma R (R.4)). Note LU §2's deterministic form of Lemma Π applies to `g`, with
constants depending on `k`. By (R.1), `𝐓_r − 𝐒_r = 12p_{V_r}(v(k))E[Λ]` with

    Λ := r^{−2}Π (1_{typed} − 1{A < 0}),

and `p_{V_r}(v(k)) → p_{V_0}(v(k))` (R.4). So it suffices to show `E[Λ] = (r/(9k))𝔏(k, u) + o(r)`.

*Step 1 (the endpoint quantities).* Put `m_i := det K_i/r`, `𝔞 := s m_M`, `𝔟 := s m_S`, `x := (𝔞 + 𝔟)/2`, `y := (𝔟 − 𝔞)/2`.
Then `r^{−2}Π = −m_Mm_S = y² − x²`, and `𝔞 < 0 < 𝔟` if and only if `|x| < y`. By Lemma Π at gap `k` (deterministic form,
applied to the pinned field `g`; note LU §2),

    x = s U + ε₊,    y = 6κ sΔ + r s V + ε₋,    |ε_±| ≤ C r² 𝔗^N.                                                   (2.1)

Also `|m_i| ≤ C(1 + κ)𝔗^N`, so `|Λ| ≤ C(1 + κ)²𝔗^N` everywhere.

*Step 2 (localization).* Let `η := r^{1/4}`, `θ := 1/(16(m + 1))`, `𝔊 := {𝔗 ≤ r^{−θ}}` and
`𝔈 := {λ_{m−1} ≤ −η, |P| ≥ η²}` (`𝔈 := Ω` if `m = 1`). Note `‖A_M − A‖ + ‖A_S − A‖ ≤ r𝔗`, where `A_i := ∇_Θ²g(i)`.
- *Off `𝔊`.* `P(𝔊^c | J) ≤ C_pr^p(1 + k + |J|)^{p/θ}` for every `p` (Markov's inequality with `E[𝔗^{p/θ} | J]`), so
  `E[|Λ|1_{𝔊^c}] ≤ C(1 + κ)²r^p = o(r)`.
- *Where `Λ` can be nonzero.* On `𝔊`: if `λ ≥ 2r𝔗`, then `λ_max(A_M) > 0`, so `g` is not typed, and `A ≮ 0`; hence `Λ = 0`. If
  `λ ≤ −2r𝔗`, then `A_M, A_S < 0`, so `typed ⟺ |x| < y` (note LU (S.4)) and `Λ = (x² − y²)1{|x| ≥ y}`, which vanishes unless
  `6κ|Δ| ≤ |x| + |y − 6κ|Δ|| ≤ C𝔗^N`. So on `𝔊`, `Λ ≠ 0` only on `{|λ| < 2r𝔗} ∪ {A < 0, |Δ| ≤ C(r/k)𝔗^N}`, and there
  `|Λ| ≤ C𝔗^N` (on the first set `6κ|Δ| ≤ 12k𝔗^m`).
- *On `𝔊 \ 𝔈`.* Off `𝔈`, a second eigenvalue lies within `η′ := max(η, η^{2/(m−1)})` of `0` (if `|P| < η²`, some `|λ_j| < η^{2/(m−1)}`,
  `j < m`). In Weyl coordinates for the law of `A` under `Q̄_{r,k}` (as in the proof of Lemma 0), both sets above then
  confine two eigenvalues:
  - `{|λ_m| < ε}` with a second eigenvalue in an interval of length `≤ 2η′`: probability `≤ C(1 + |μ_A|)^Nεη′`, since the joint
    density of two eigenvalues is bounded;
  - `{A < 0, |Δ| ≤ δ}`: as in the proof of #218 Lemma D's second bound, integrate the eigenvalue of least modulus over an
    interval of length `2δ/D`, where the factor `D` cancels against the Vandermonde product. The remaining integral confines a
    second eigenvalue to an interval of length `≤ 2η′`. So the probability is `≤ C(1 + |μ_A|)^Nδη′`.

  With the layer device of #237 Step U2 (a) for the factor `𝔗^N` (condition on `A`, and sum over dyadic layers of `𝔗`),
  `E[|Λ|1_{𝔊\𝔈}] ≤ C(r + r/k)η′ = o(r)`.

*Step 3 (typedness near the edge, on `𝔊 ∩ 𝔈`).* Here the second-largest eigenvalues of `A_M` and `A_S` are at most
`−r^{1/4} + r𝔗 < 0`, and `λ` is simple with gap at least `r^{1/4}/2` when `|λ| < 2r𝔗`. First-order eigenvalue perturbation
gives

    λ_M := λ_max(A_M) = λ − (r/2)B_ee + O(r^{7/4}𝔗²),                                                               (2.2)

since `A_M − A = −(r/2)B + O(r²𝔗)` and the second-order term is `≤ ‖A_M − A‖²/gap`. By Haynsworth's inertia additivity,
`H_M < 0 ⟺ λ_M < 0 ∧ 𝔞 < 0`, and, because `A_S` has at most one nonnegative eigenvalue, `ind H_S = d − 1 ⟺ 𝔟 > 0` (if
`A_S < 0` the Schur complement must be positive, if `A_S` has one positive eigenvalue it must be negative; either way
`det H_S` has the sign `s`). Hence on `𝔊 ∩ 𝔈`

    Λ = (y² − x²)(1{λ_M < 0, |x| < y} − 1{λ < 0}) = Λ₁ + Λ₂ + Λ₃,
    Λ₁ := (x² − y²)1{λ < 0, |x| ≥ y},  Λ₂ := −(y² − x²)1{λ < 0, |x| < y, λ_M ≥ 0},  Λ₃ := (y² − x²)1{λ ≥ 0, λ_M < 0, |x| < y}.

*Step 4 (`Λ₃` and `Λ₂`).* By (I.1) and (2.1), with `sP = −|P|` on `𝔈`: `y = 6κ sλP + rsV + ε₋` and
`x = s(PU_red + λW) + ε₊`.
- *`Λ₃`* (the sliver `{λ ≥ 0 > λ_M}`). For `λ ≥ 0`, `sΔ = sλP = −λ|P| ≤ 0`. So `y > |x| ≥ 0` forces `y ≤ rC𝔗^N`, and
  `|Λ₃| ≤ y² ≤ Cr²𝔗^N`.
- *`Λ₂`* (the strip) vanishes for small `r`. On `𝔊 ∩ 𝔈 ∩ {λ < 0 ≤ λ_M}` the matrix `A_M` has exactly one nonnegative
  eigenvalue `λ_M`, positive almost surely, and its other eigenvalues are `≤ −r^{1/4}/2` (Step 3, for small `r`). Write
  `K_M = [[α_M, √r β_Mᵀ], [√r β_M, A_M]]` with `α_M = ∂_u²g(M)/r` and `β_M = ∇_Θ∂_ug(M)/r`; the pins give
  `α_M = −6k + O(r𝔗)` and `|β_M| ≤ C𝔗` (#237's proof of Lemma Π; note LU §2). With `e_{M,j}` the unit eigenvectors of
  `A_M`, the Schur complement of `A_M` in `K_M` is
  `σ_M = α_M − r(β_M·e_{M,m})²/λ_M − rΣ_{j<m}(β_M·e_{M,j})²/λ_j(A_M) ≤ −6k + Cr𝔗 + 2r^{3/4}|β_M|² < 0` for `r ≤ r(k)` (on
  `𝔊`). Since `det A_M` has the sign `−s`, `det K_M = det A_M·σ_M` has the sign `s`: `𝔞 > 0`, so `|x| ≥ y`. Hence `Λ₂ = 0` on
  `𝔊 ∩ 𝔈` for `r ≤ r(k)` (control E7). For `m = 1` the sum over `j < m` is empty, and `σ_M < α_M < 0`.

  So the strip lies inside the layer `{|x| ≥ y}`. To first order this is the computation `|U_red| ≥ γ_e²/4 − 3kB_ee` and
  `6κ|λ| ≤ −3kB_ee + O(kr^{3/4}𝔗²)` on the strip (by (2.2)).

*Step 5 (the layer `Λ₁`).* Put `a := |P||U_red|` and `β := 6κ|P|`, functions of `Rest := (λ₁, …, λ_{m−1}, O, odd jets)`. By
(I.1) and (2.1), with `sλP = |λ||P|` for `λ < 0`,

    x² − y² = a² − β²λ² + ϱ,    ϱ = 2PU_red·λW + λ²W² − 2β|λ|(rsV + ε₋) − (rsV + ε₋)² + O((1 + a + |λW|)|ε₊|)        (2.3)

(control E8).
- *Where `y < 0`.* With `λ < 0` this forces `6κ|λ||P| ≤ Cr𝔗^N`, a `λ`-interval of length `≤ Cr²𝔗^N/(k|P|)`. The Weyl density
  of `A` under `Q̄_{r,k}` (as in the proof of Lemma 0) carries the Vandermonde factor `|P|` at `λ_m = 0`, which cancels the
  `1/|P|` as in #218 Lemma D's second bound; with `|Λ| ≤ C𝔗^N`, this set costs `O(r²/k)`.
- *The perturbation.* Elsewhere `Λ₁ = (a² − β²λ² + ϱ)₊`, and `|(a² − β²λ² + ϱ)₊ − (a² − β²λ²)₊|` is at most `|ϱ|` where either
  is positive. On `𝔊 ∩ 𝔈`, `β = 6κ|P| ≥ 6kr^{−1/2}`, while `|W| ≤ C𝔗^m ≤ Cr^{−1/16}`. So `|λ||W| ≤ β|λ|/2` for small `r`, and
  positivity forces `β|λ| ≤ 2a + Cr𝔗^N`, that is `|λ| ≤ (r/(3k))(|U_red| + Cr^{1/2}𝔗^N)`. There (2.3) gives
  `|ϱ| ≤ C(r/k)(1 + a)²𝔗^N + Cr(1 + a)𝔗^N`. So this costs `O(r²(1 + k^{−2}))` after the layer device.
- *The main part.* Let `J(λ, Rest)` be the joint density of `(λ_m, Rest)` under `Q̄_{r,k}`: the Weyl density of `A` (as in
  the proof of Lemma 0, for the law of `A` under `Q̄_{r,k}`) times the Gaussian density of the odd jets, which are independent
  of `A` (R.2). It is `C¹` in `λ` on `(λ_{m−1}, ∞)`, and `|∂_λJ| ≤ C(1 + |Rest|)^N q(Rest)` for `λ_{m−1} < λ ≤ 1`, with `q` a
  Gaussian factor. (There is no factor `|P|` here: `∂_λ∏_{j<m}(λ − λ_j)` is a sum of products of `m − 2` of the factors and
  is not small when one `|λ_j|` is. The factor `P²` of the result comes from `a²`.) On `𝔈 ∩ {|U_red| < 6kr^{−3/4}}` we have
  `a/β = |U_red|/(6κ) = r|U_red|/(6k) < η ≤ |λ_{m−1}|`, so by (I.2)

      ∫_{−∞}^0 (a² − β²λ²)₊ J(λ, Rest) dλ = J(0⁻, Rest) P²|U_red|³/(9κ) + O((a/β)² a² sup_{|λ|≤a/β}|∂_λJ|),

  and the error integrates over `Rest` to `O(r²k^{−2})`; the event `{|U_red| ≥ 6kr^{−3/4}}` costs `O(r^p)`. Integrating over
  `Rest` on `𝔈`, `E[Λ₁] = (r/(9k))𝔼_{Q̄_{r,k}}[P²|U_red|³1_𝔈; λ_m = 0⁻] + O(r²(1 + k^{−2}))`, the `O` including the costs
  above and `𝔊^c`. (The edge expectation under `Q̄_{r,k}` exists by the argument of Lemma 0.)
- *The limit.* As `r ↓ 0`, `1_𝔈 ↑ 1` on `{λ_{m−1} < 0}`, and the law of the finite jet vector `(A, γ, B)` under `Q̄_{r,k}` is a
  smooth function of `r` with uniformly nondegenerate covariance (R.4). So `𝔼_{Q̄_{r,k}}[P²|U_red|³1_𝔈; λ_m = 0⁻] → 𝔏(k, u)`
  by (1.1) and dominated convergence.

Steps 2–5 give `E[Λ] = (r/(9k))𝔏(k, u) + o(r)`, hence (F₃). ∎

## 3. Proof of Lemma T₁

By #237 Step U4, `𝓐(κ) = −12p_{V_0}(v(0))E_{Q̄_{0,0}}[min(Y′², 36κ²Δ²)1{A<0}]`, and by Lemma K
(`𝐀₂(0, u) = ∫_RA₂(b, 0, u)db`) and #218 (F.2), integrated in `b` by the disintegration of (R.1) at `r = 0` (Tonelli; as in
#237 Step U4), `𝐀₂(0) = −12p_{V_0}(v(0))E_{Q̄_{0,0}}[Y′²1{A<0}]`. Hence

    𝓐(κ) − 𝐀₂(0) = 12 p_{V_0}(v(0)) E_{Q̄_{0,0}}[(Y′² − 36κ²Δ²)₊ 1{A<0}].                                              (3.1)

Put `η := κ^{−1/4}` and `𝔈_κ := {λ_{m−1} ≤ −η, |P| ≥ η²}`, as in §2 Step 2 with `1/κ` in place of `r`. The integrand of
(3.1) is at most `Y′²` and vanishes unless `A < 0` and `|Δ| ≤ |Y′|/(6κ)`.

*Off `𝔈_κ`* (so `m ≥ 2`), use the dyadic layers of `|Y′|` of #218's proof of Lemma O. On `{2^{j−1} ≤ |Y′| < 2^j}` (`j ≥ 1`;
`{|Y′| < 1}` for `j = 0`) the integrand is at most `4^j`, and the event lies in `{A < 0, |Δ| ≤ δ_j}` with `δ_j := 2^j/(6κ)`,
which does not depend on `A`. Given `A`, `(f₄, γ)` is Gaussian with mean affine in `A` and bounded covariance, and `Y′` is a
polynomial in `(f₄, γ)` with coefficients polynomial in `A`, so `P(|Y′| ≥ 2^{j−1} | A) ≤ C_p2^{−jp}(1 + ‖A‖)^{n_p}`. The
second sub-bullet of §2 Step 2's bullet *On `𝔊 \ 𝔈`* (the proof of #218 Lemma D's second bound, with a second eigenvalue
within `η′ := max(η, η^{2/(m−1)})` of `0`), with the weight `(1 + ‖A‖)^{n_p}`, gives
`E[(1 + ‖A‖)^{n_p}1{A < 0, |Δ| ≤ δ_j}1_{𝔈_κ^c}] ≤ Cδ_jη′`. Summing over `j` with `p > 3` gives
`E[Y′²1{A<0, |Δ| ≤ |Y′|/(6κ)}1_{𝔈_κ^c}] ≤ Cκ^{−1}η′ = o(κ^{−1})`.

*On `𝔈_κ`*, (I.1) and (1.2) give `Δ = λP` and `Y′ = P(−γ_e²/4) + λW₀`. With `a := |P|γ_e²/4` and `β := 6κ|P|`, the integrand
is `(a² − β²λ² + ϱ)₊` with `ϱ = −Pγ_e²λW₀/2 + λ²W₀²`. Off `{|W₀| ≥ κ^{1/2}}`, whose cost is `O(κ^{−p})` for every `p`,
`β ≥ 6κ^{1/2} ≥ 2|W₀|` on `𝔈_κ`. So positivity forces `β|λ| < a + |λ||W₀| ≤ a + β|λ|/2`, that is `|λ| ≤ γ_e²/(12κ)` (on
`𝔈_κ` this window lies in `(λ_{m−1}, 0)`, where the density is `C¹` in `λ`, unless `γ_e² ≥ 12κ^{3/4}`; given `A`, `γ_e` is
centred Gaussian with bounded variance, so that event costs `O(κ^{−p})` against the weight `Y′²`), and there, for `κ ≥ 1`,
`|ϱ| ≤ |P|γ_e⁴|W₀|/(24κ) + γ_e⁴W₀²/(144κ²) ≤ (1 + |P|)(1 + γ_e²)²(1 + |W₀|)²/κ` (control E9). As in §2 Step 5 (with `r/k`
replaced by `1/κ`, and no field remainder), the perturbation costs `O(κ^{−2})`, and (I.2) gives

    E[(Y′² − 36κ²Δ²)₊1{A<0}1_{𝔈_κ}] = (1/(9κ)) 𝔼_0[P²(γ_e²/4)³ 1_{𝔈_κ}; λ_m = 0⁻] + O(κ^{−2}).

Also `𝔼_0[P²(γ_e²/4)³1_{𝔈_κ}; λ_m = 0⁻] → 𝔏(0, u)` as `κ → ∞`, by (1.1) and monotone convergence. Multiplying by
`12p_{V_0}(v(0))κ` gives `κ(𝓐(κ) − 𝐀₂(0)) → a₁`.

*The identity `a₁ = (1/10)∫F₀db`.* #242 (1.0a) defines `𝔇(b, u) := lim ε^{−1}E₀[γ₁⁶(λ₂⋯λ_m)²1{A<0, λ₁ < ε} | b]`, where
`λ₁ < ⋯ < λ_m` are there the eigenvalues of `−A` and `γ₁` is `γ`'s component along the eigenvector of `λ₁`. Write `μ_i` for
these eigenvalues, to avoid a clash with this note's `λ_i` (the eigenvalues of `A`): `μ_i = −λ_{m+1−i}`. So
`{A < 0, μ₁ < ε} = {−ε < λ_m < 0}` (the event of (0.2)), the eigenvector of `μ₁` is `±e`, `γ₁² = γ_e²` and
`(μ₂⋯μ_m)² = (λ₁⋯λ_{m−1})² = P²`. For each `ε > 0`, the disintegration of (R.1) at `r = 0`, `k = 0` (as in #237 Step U4)
gives `∫_Rπ₀(u; v₀(b, 0))ε^{−1}E₀[γ₁⁶(μ₂⋯μ_m)²1{A<0, μ₁ < ε} | b]db = p_{V_0}(v(0))ε^{−1}E_{Q̄_{0,0}}[P²γ_e⁶1{−ε < λ_m < 0}]`.
Let `ε ↓ 0`. The right side tends to `p_{V_0}(v(0))𝔼_0[P²γ_e⁶; λ_m = 0⁻]` (Lemma 0). On the left, dominated convergence
applies. By #242 (1.1a)–(1.1b) and (G1), `ε^{−1}E₀[γ₁⁶(μ₂⋯μ_m)²1{A<0, μ₁ < ε} | b] ≤ C(1 + |b|)^N` for `0 < ε ≤ 1`: this is
the bound of #242's proof of Corollary 1′, with `E[γ₁⁶ | A] = 15(e₁ᵀΣ_γe₁)³ ≤ C`. And `π₀(u; v₀(b, 0)) ≤ Ce^{−cb²}` ([R]
(R5), as in #242's proof of Theorem 1). So `∫_Rπ₀(u; v₀(b, 0))𝔇(b, u)db = p_{V_0}(v(0))𝔼_0[P²γ_e⁶; λ_m = 0⁻]`, and, with
`F₀ = (5/24)π₀𝔇`,

    a₁ = (12/9)(1/64) p_{V_0}(v(0)) 𝔼_0[P²γ_e⁶; λ_m = 0⁻] = (1/48)(24/5) ∫F₀ db = (1/10) ∫F₀ db.   ∎               (3.2)

## 4. Proof of Theorem C3

*The decomposition.* Note LU §4's proof of Theorem P⁺ (at its fixed split `ρ := min(r₄, r₀/2)`, `ℓ ≤ ρ³`; #237 §5's
decomposition, `J₂` absorbed) gives

    ν_cand − cℓ^{−1/3} − B_{d,L} − I^{cand}ℓ^{1/4} − c₂ℓ^{1/3} = ∫_0^ρ ∫_{S^{d−1}} D_r(ℓ/r³, u) dσ(u) dr + O(ℓ),
    D_r(k, u) := 𝐓_r(k, u) − 𝐓_r(0, u) − r^{−2}𝐀_0(k, u) − [𝐀₂(k, u) − 𝐀₂(0, u)] − 𝓐(k/r, u),                       (4.1)

with the main terms `c₂ℓ^{1/3} + O(ℓ²ρ^{−5})` and `I^{cand}ℓ^{1/4} + O(ℓ²ρ^{−7})`, and `J₃`, `J₄`, `J₅` of order `ℓ` or
smaller.

*The fold variable.* Put `r = ℓ^{1/3}s`, so `k = ℓ/r³ = s^{−3}` and `κ = ℓ^{−1/3}s^{−4}`, and `φ_r(k, u) := D_r(k, u)/r`. Then

    ∫_0^ρ D_r(ℓ/r³, u) dr = ℓ^{2/3} ∫_0^{ρℓ^{−1/3}} s φ_{ℓ^{1/3}s}(s^{−3}, u) ds.                                     (4.2)

*Domination.* By Theorem U⁼ (note LU), `|φ_r(k)| ≤ C(r min(1, κ) + min(k, 1/k))`. In the fold variable
`r min(1, κ) = min(ℓ^{1/3}s, s^{−3}) ≤ min(1, s^{−3})` for `s ≤ ρℓ^{−1/3}` (as `ρ ≤ 1`, which we may assume by taking
`r₄ ≤ 1`), and `min(k, 1/k) = min(s^{−3}, s³)`. So `|sφ| ≤ 2Cs·min(1, s^{−3})`, which is integrable on `(0, ∞)` (control
E6).

*The pointwise limit.* Fix `k > 0` and `u`, and let `r ↓ 0`. Then:
- `(𝐓_r(k) − 𝐒_r(k))/r → 𝐋_F(k)` by Lemma F₃;
- `(𝐒_r(k) − r^{−2}𝐀_0(k) − 𝐀₂(k))/r = O(r)` by Lemma K ((K.1): `|r²𝐒_r − 𝐀_0 − r²𝐀₂| ≤ Cr⁴(1 + k)^Ne^{−ck²}`);
- `𝐓_r(0)/r ≤ Cr²log(2/r) → 0` by #229 (W⁺.2) at `κ = 0`, integrated in `b` (as in note LU §4);
- `(𝓐(k/r) − 𝐀₂(0))/r = (1/k)·κ(𝓐(κ) − 𝐀₂(0)) → a₁/k` by Lemma T₁, since `κ = k/r → ∞`.

So `φ_r(k, u) → 𝐋_F(k, u) − a₁(u)/k = 𝐄(k, u)`. In particular `|𝐄(k, u)| ≤ C min(k, 1/k)`, the limit of the domination.

*Conclusion.* By (4.2) and dominated convergence (also in `u`), `ℓ^{−2/3}∫_0^ρ∫D_r(ℓ/r³, u)dσ dr` tends to
`∫_S∫_0^∞ s𝐄(s^{−3}, u)ds dσ(u)`. With `s = k^{−1/3}`, `s ds = (1/3)k^{−5/3}dk`, and this is `c₃`. With (4.1), this is (C3). ∎

## 5. The Gaussian kernel and the torus field: proofs of Proposition G, Corollary G′ and Proposition G″

*Covariances.* For `C(z) = e^{−|z|²/2}`, `E[∂^αf(0)∂^βf(0)] = (−1)^{|β|}∂^{α+β}C(0)`, and `∂^αC(0) = ∏_i (−1)^{α_i/2}(α_i − 1)!!`
when every `α_i` is even, and `0` otherwise. Take `u` and a unit `e ⊥ u` as two coordinate axes (the model is isotropic).
- (G.1) The pins of `Q̄_{0,k}` are `∇f(0) = 0`, `∂_u∇f(0) = 0` and `∂_u³f(0) = 12k`. The odd jet `γ_e = ∂_u²∂_ef(0)` has
  variance `3` and covariance `−1` with `∂_ef(0)`, and none with the other odd pins; so given the pins it is `N(0, 2)`. The
  odd jet `B_ee = ∂_u∂_e²f(0)` has variance `3` and covariances `−1` with `∂_uf(0)` and `3` with `∂_u³f(0)`. Since
  `Cov(∂_u³f, ∂_uf) = −3` and `Var(∂_uf) = 1`, `B_ee + ∂_uf(0)` is uncorrelated with both `∂_uf(0)` and `∂_u³f(0)`. So the
  regression of `B_ee` on the pins is `−∂_uf(0)`, which vanishes under the pins: `B_ee` is `N(0, 3 − 2 + 1) = N(0, 2)` given the
  pins, for every `k`. `Cov(γ_e, B_ee) = 0`, and their regressions use disjoint sets of pins that are uncorrelated with each
  other (`∂_ef(0)`; and `∂_uf(0)`, `∂_u³f(0)`), so their conditional covariance is `0` and they are independent; both are odd,
  hence independent of `A`. Finally `∂_u³f(0)` is correlated only with `∂_uf(0)` among the other pins
  (`Var(∂_u³f) = 15`, covariance `−3`), so its conditional variance is `6`, and `v(k)ᵀCov(V_0)^{−1}v(k)/2 = (12k)²/12 = 12k²`
  (control E3, exactly in `d = 2, 3, 4`, including a non-axial `e` in `d ≥ 3`).
- (G.2) By (G.1) and Lemma 0, `h_k(e) = g(k)` for every `e`, so `𝔏(k, u) = g(k)𝔡̄`, with `𝔡̄ := 𝔼_A[P²; λ_m = 0⁻]` independent
  of `k` and `u` (so `∫π₀(u; v₀(b, 0))𝔡(b)db = p_{V_0}(v(0))𝔡̄` with #242's `𝔡(b)`). Hence
  `𝐄(k) = (12/(9k))𝔡̄(p_{V_0}(v(k))g(k) − p_{V_0}(v(0))g(0)) = (a₁/k)(e^{−12k²}g(k)/g(0) − 1)`.
  `g(0) = E[γ⁶]/64 = 15·2³/64 = 15/8`. `a₁ = (1/10)∫F₀db` is (3.2).
- (G.3) Write `X := γ²/4 − 3kB`. Then `g(k) = E|X|³ = E[X³] + 2E[(−X)₊³]`, and from the moments of `N(0, 2)`,
  `E[X³] = E[γ⁶]/64 + 3E[γ²/4]·9k²E[B²] = 15/8 + 27k²` (control E4). So

      e^{−12k²}g(k)/g(0) − 1 = [e^{−12k²}(1 + (72/5)k²) − 1] + (16/15)e^{−12k²}E[(3kB − γ²/4)₊³].

  For `a > 0` and `b ∈ R`, `∫_0^∞(e^{−ak²}(1 + bk²) − 1)k^{−8/3}dk = (1/2)Γ(1/6)a^{−1/6}(b − 6a/5)`: substitute `t = ak²`, and
  use `∫_0^∞(e^{−t} − 1)t^{−11/6}dt = Γ(−5/6) = −(6/5)Γ(1/6)` and `∫_0^∞e^{−t}t^{−5/6}dt = Γ(1/6)`. Here `a = 12` and
  `b = 72/5 = 6·12/5`, so the bracket integrates to `0` (control E4). The remaining integrand is positive, which is (G):
  `J > 0`. It converges, since `E[(3kB − γ²/4)₊³] ≤ E[(3kB)₊³] = O(k³)` at `0`, with Gaussian decay at `∞`. Finally, by (C3),
  `c₃ = (1/3)∫_S∫_0^∞(a₁/k)(…)k^{−5/3}dk dσ = (J/3)∫_Sa₁dσ = (J/30)∫_S∫_RF₀ db dσ`, and #242's Corollary 1′ gives
  `∫∫F₀ = 25√3/(48π²)` (`d = 2`) and `125√30/(192π³)` (`d = 3`) (control E5). ∎

*Corollary G′.* `∫∫F₀ > 0` (#242 Theorem 1: `𝔇 > 0`) and `J > 0`, so the model value of `c₃` is positive. The rest is
Theorem C3. ∎

*Proposition G″.* Write `θ` for the covariance of the finite jet vector `(V₀, A, B, γ)` at `0`, in the frame `(u, Θ)`
(derivatives of order at most `3`, so `θ` consists of derivatives of order at most `6` of the covariance at `0`). Call `θ`
*parity-split* if every jet of even order is uncorrelated with every jet of odd order. A stationary field has an even
covariance, so `θ_∞` and every `θ(L, u)` below are parity-split. For parity-split `θ`, Gaussian regression on the pins
`V₀ = v(k)` gives, as in Lemma R (R.2) at `r = 0` and the proof of Lemma 0: the law of `A`, which is centred and does not
depend on `k`; the law of `(B, γ)`, which is independent of `A`, with mean `k·m_θ` and a covariance `S_θ` not depending on
`k`; and `p_{V_0}(v(k)) = p_{V_0}(v(0))e^{−q_θk²}` with `q_θ > 0`. Let `𝒩` be a compact neighbourhood of `θ_∞` within the
parity-split covariances, on which all these covariances are uniformly nondegenerate. Constants below are uniform on `𝒩` and
in `u`.
- *A uniform bound.* By Lemma 0, and since (0.2) is linear on integrands whose edge limits exist (here those of `𝔏(k, u)`
  and `𝔏(0, u)`), `𝐄(k, u) = (12/(9k))𝔼_A[P²Φ_k(e); λ_m = 0⁻]`, with
  `Φ_k(e) := p_{V_0}(v(k))h_k(e) − p_{V_0}(v(0))h_0(e)`. Given `A`, `(B_ee, γ_e)` is Gaussian with mean linear in `k` and
  covariance not depending on `k`; writing it as `k·m + (centred part)`, the map `k ↦ |3kB_ee − γ_e²/4|³` is `C²` pathwise
  (`x ↦ |x|³` is `C²`), with first and second derivatives bounded by a polynomial in the centred jets for `|k| ≤ 1`. So
  `Φ_k(e)` is `C²` in `k` with `|∂_k²Φ_k(e)| ≤ C` for `|k| ≤ 1`. It is even in `k` (as in the proof of Lemma 0) and vanishes
  at `k = 0`, so `|Φ_k(e)| ≤ Ck²`. With `𝔼_A[P²; λ_m = 0⁻] ≤ C` (by (1.1)), `|𝐄(k, u)| ≤ Ck` for `k ≤ 1`. For `k ≥ 1`,
  `0 ≤ 𝐋_F(k, u) ≤ (C/k)e^{−q_θk²}(1 + k)^N` and `a₁/k ≤ C/k`. So `|𝐄(k, u)| ≤ C min(k, 1/k)` on `𝒩`.
- *Continuity.* At fixed `(k, u)`, `𝐄(k, u)` is continuous in `θ ∈ 𝒩`: in (1.1) the integrand is continuous in `θ` and
  dominated by `C(1 + |λ′|)^Ne^{−c|λ′|²}` uniformly on `𝒩`. By the uniform bound and dominated convergence in `(k, u)`, `c₃`
  is continuous in `u ↦ θ(u) ∈ 𝒩` for uniform convergence in `u`.
- *The torus field.* Its covariance is the periodization `Σ_{n∈Z^d}C(z + nL)` of `C` (#242 §0, "the periodized kernel of
  the torus field"; #207 §8 Remark 3). At `z = 0` every derivative of order at most `6` of the terms `n ≠ 0` is
  `O(L⁶e^{−L²/2})` in total. So `θ(L, u) → θ_∞` as `L → ∞`, uniformly in `u`, and `c₃(L) → c₃(θ_∞) = (J/30)∫∫F₀ > 0` by
  Proposition G and Corollary G′. The rest is Theorem C3 for the torus field. ∎

*Values* (exploration; not part of the proof; mpmath quadrature; script and output in the exploration comment).
`J = 4.1977820`. In `d = 2`, the model value of `c₃` is `0.0127896` and `c₃/c_{2,∞} = 0.174229`; in `d = 3`, `c₃ = 0.0160923`
and `c₃/c_{3,∞} = 0.385205`, with `c_{2,∞} = 0.073406919`, `c_{3,∞} = 0.041775932` (#216, #223). The Slice C referee
computed `J` by a different route (integrating `B` against a Bessel function `K_{4/3}`) and got `4.1977819815839`. The
small-`k` behaviour is `e^{−12k²}g(k)/g(0) − 1 = (12/5)k² + c_{7/2}k^{7/2} + O(k⁴)`, with
`c_{7/2} = 256·6^{7/2}Γ(9/4)/(525π) ≈ 93.04` (from the density `w^{−1/2}` of `w = γ²/4` near `0`); so
`𝐄(k) = (12/5)a₁k + O(k^{5/2})`, and `𝐄(k)` changes sign at `k ≈ 0.369`.

## 6. Remarks

1. **Where `c₃` comes from.** At the fold scale the typed region differs from the cone `{A < 0}` in three places: the layer
   `{|x| ≥ y}` (the gap is too small to separate the endpoint determinants), the strip `{A < 0 ≤ λ_max(A_M)}`, and the
   sliver `{λ_max(A) ≥ 0 > λ_max(A_M)}`, which costs at most `O(r²)` (Step 4). Step 4 shows that for small `r` the strip
   lies inside the layer, off a set that costs `o(r)`: there the Schur complement of `A_M` in `K_M` is negative. To first
   order, `|U_red| ≥ −3kB_ee` on the strip, while `6κ|λ| ≤ −3kB_ee` up to `O(kr^{3/4}𝔗²)`. So the whole first-order effect
   is the layer's coefficient `𝔏(k)`, and `c₃` measures how it depends on `k`: through the explicit `3kB_ee` in `U_red`,
   through the law of the odd jets, and through the density factor `p_{V_0}(v(k))`. #237 Remark 2 traces the term to "the
   `k`-dependence of the layer coefficient (Lemma Λ)" and to Step U2 (b). At fixed `k` the latter's term `rsV` in `y` moves
   the layer by `O(r²/k)`, so it does not enter `c₃`.
2. **The author-side referee's numerics in #237.** #237's README (review record) reports a `d = 2` Gaussian-kernel Monte
   Carlo in which "The `k²/κ` coefficient of the layer was nonzero, about `+0.005`". Here the layer's correction is
   `r𝐄(k)`, and `rk = k²/κ`. As `k → 0`, `r𝐄(k) = (12/5)a₁rk + O(rk^{5/2})`, with `(12/5)a₁ = 0.0034913` per direction `u`,
   birth-integrated, in `d = 2`. But the `k^{7/2}` coefficient of `e^{−12k²}g(k)/g(0) − 1` is about `93` (§5). So at moderate
   gaps the effective coefficient `a₁(e^{−12k²}g(k)/g(0) − 1)/k²` is `0.0045`, `0.0056` and `0.0055` at `k = 0.05`, `0.1` and
   `0.2`, and `𝐄(k)` changes sign at `k ≈ 0.369`. The README's `+0.005` lies in this range. The README does not give the
   fit's `k`-range or normalization, so the comparison is only qualitative.
3. **The elder and rejected densities.** By #229's Corollary R⁺, `ρ_rej = ν_cand − ν_eld`. So, given Theorem C3, #242's
   Conjecture 7 with `o(ℓ^{2/3})` in place of `O(ℓ^{3/4})` is equivalent to
   `ν_eld − ν_eld^{far,r_0^*} = cℓ^{−1/3} + c₁ℓ^{1/4} + c₂ℓ^{1/3} + (c₃ − R_{2/3})ℓ^{2/3} + o(ℓ^{2/3})`, where `c₁` is the
   elder `ℓ^{1/4}` coefficient (#220 (0.2)).
   - For the Gaussian kernel #244's closed form gives `R_{2/3} = −0.048779` (`d = 2`) and `−0.061375` (`d = 3`) (exploration).
     So the conjectured coefficient is `c₃ − R_{2/3} ≈ 0.061569` and `0.077467`, that is `0.8387c` and `1.8544c`.
   - For SIDE24 (`d = 3`, `L = 24`), with the model values (Remark 5), this would make the next relative term of the near
     elder density `≈ 1.854ℓ`. For `ν_eld` itself the far term also enters at this order: #187 bounds `ν_eld^{far,r_0^*}` only
     by `O(ℓ^{2/3})`, and #188's `O(ℓ^N)` is not used here. Both lie inside note LU's `O(ℓ log(1/ℓ))`.
   - #216's Monte Carlo of the elder density (three-term law `1.006 ± 0.004` in `d = 2`, `1.008 ± 0.010` in `d = 3`, on
     `[10⁻⁴, 10⁻²]`) is consistent with a positive term of this size: on that range the term would raise the count ratio to
     about `1.004` (`d = 2`) and `1.009` (`d = 3`). It is not a test. Those ratios are also consistent with no such term,
     #216's fields are tori of side `64` and `16` and include far pairs, and over wider ranges #237 Remark 4 records elder
     and rejected residuals that single-power fits place at `p ≈ 0.14–0.33` in six of eight fits (one elder fit gives
     `0.54`).
   - What a proof would still need are #242's inputs (i) and (ii), in their `o(ℓ^{2/3})` form. (i) On the soft layer
     `κ ≥ 1`, note TL's Corollary TL1 has remainder `O(ℓ^{2/3})`, and its Remark 2 records, through #243 Theorem FL, the
     rejected fold limit `κ(𝐓_r^{rej} − 𝓐^{rej}) → ∫(F − F₀)db` at fixed `k`. The soft layer's `ℓ^{2/3}` coefficient is not
     derived from these here. (ii) On the intermediate separations, note LU leaves the elder mass at `O(ℓ^{2/3}log(1/ℓ))`
     (addendum EM.1). Nothing here is claimed for either part.
4. **Why `o(ℓ^{2/3})`.** Theorem C3 uses Lemmas F₃ and T₁ only pointwise in `k`, and Theorem U⁼ only as a dominating function.
   A rate would need (F₃) uniformly in `k` with a rate, and the matching of the fold-side and cusp-side expansions on
   `1 ≪ κ`, `k ≪ 1`. Formally (#242's matched-asymptotics count), the next terms are `ℓ^{3/4}` from the cusp side and then `ℓ`.
5. **The torus field.** Theorem C3 holds for the torus field itself, with `c₃` given by (C3). Proposition G and Corollary G′
   are about the model value; Proposition G″ transfers its sign to the torus field for `L ≥ L₀(d)`, with `L₀(d)` not
   quantified. At `L = 24` the torus field's jet covariances differ from the model's by `O(e^{−288})` (the terms `n ≠ 0` of
   the periodization; #207 §8 Remark 3).
   A modulus of continuity for `c₃` in the jet law, which is not proved here, would show that the digits of §5 are unchanged
   at `L = 24`, so that `c₃(24) > 0` and Theorem P⁺ is sharp for SIDE24. That is not proved or certified here.
6. **Numerical illustration** (exploration; not part of the proof; numpy, scipy and mpmath, outside the repository; scripts
   and output in the exploration comment).
   - *Lemma F₃.* The Slice A referee wrote an independent Monte Carlo: exact Gaussian conditioning on #237's rows at 60
     digits, defensive importance sampling of `λ_max(A)`, and typedness decided by the eigenvalues of `K_M` and `K_S`, so
     Step 3's criterion is tested rather than assumed. For the Gaussian kernel it gives the ratio `(𝐓_r − 𝐒_r)/(r𝐋_F)`,
     ± one standard error over the samples (`1.2·10⁷` per entry in `d = 2`, `8·10⁶` in `d = 3`):

     | `d` | `k` | `r = 0.0025` | `0.005` | `0.01` | `0.02` | `0.04` |
     |---|---|---|---|---|---|---|
     | 2 | 0.2 | `0.9964 ± 0.0034` | `1.0024 ± 0.0033` | `1.0025 ± 0.0033` | `0.9998 ± 0.0032` | `1.0014 ± 0.0032` |
     | 2 | 0.4 | `0.9997 ± 0.0021` | `0.9986 ± 0.0021` | `0.9986 ± 0.0021` | `1.0031 ± 0.0021` | `1.0027 ± 0.0021` |
     | 2 | 0.6 | `0.9965 ± 0.0018` | `1.0044 ± 0.0018` | `1.0034 ± 0.0018` | `0.9994 ± 0.0018` | `1.0015 ± 0.0018` |
     | 2 | 0.8 | `0.9963 ± 0.0017` | `0.9994 ± 0.0017` | `1.0017 ± 0.0018` | `1.0024 ± 0.0017` | `1.0006 ± 0.0017` |
     | 3 | 0.2 | `0.9983 ± 0.0048` | `0.9946 ± 0.0048` | `0.9983 ± 0.0049` | `0.9908 ± 0.0047` | `0.9928 ± 0.0046` |
     | 3 | 0.4 | `0.9994 ± 0.0032` | `0.9982 ± 0.0031` | `0.9971 ± 0.0032` | `0.9973 ± 0.0031` | `0.9947 ± 0.0031` |
     | 3 | 0.6 | `1.0020 ± 0.0027` | `1.0010 ± 0.0027` | `0.9987 ± 0.0027` | `0.9990 ± 0.0027` | `0.9944 ± 0.0026` |
     | 3 | 0.8 | `1.0052 ± 0.0025` | `1.0031 ± 0.0025` | `1.0013 ± 0.0025` | `0.9982 ± 0.0025` | `0.9974 ± 0.0025` |

     Over the 40 entries `χ²/dof = 1.35`, and the largest deviation is `2.38` standard errors. The criterion of Step 3 agreed
     with the eigenvalue decision in every sample where it applies, and `|Λ₂|/r`, `|Λ₃|/r` were below `2·10⁻¹⁰` in every
     entry. At `k = 0.8`, `e^{−12k²}g(k)/g(0) = 0.0170`, so the comparison distinguishes `𝐋_F(k)` from the cusp-tail value
     `a₁/k` by a factor of about `59`. In `d = 3` it also distinguishes the weight `P²` from `|P|` and `|P|³`, which would
     give ratios `2.50–2.54` and `0.333–0.338`. These runs supersede the author's earlier ones (a few replicates per entry),
     whose quoted errors understated the uncertainty.
   - *Lemma T₁.* The Slice B referee's independent quadrature gives `κ(𝓐(κ) − 𝐀₂(0))/a₁ − 1 = −1.1·10⁻⁴`, `−1.1·10⁻⁶`,
     `−1.1·10⁻⁸`, `−1.1·10⁻¹⁰` at `κ = 10, 10², 10³, 10⁴` in `d = 2`, and `−1.07·10⁻³`, `−9.4·10⁻⁵`, `−9.3·10⁻⁶`,
     `−9.3·10⁻⁷` in `d = 3`.

## 7. Exact controls (`c3_exact.py`; stdlib; exact rationals; deterministic; byte-identical under `-O`)

The script and its stdout are published in the next comment, with the extraction rule.
- **E1** (I.1) on random rational spectra and rational orthogonal frames (Cayley transforms), `m = 1, 2, 3`: `Δ = λP`,
  `A^♯ = Peeᵀ + λR`, `γᵀA^♯γ = Pγ_e² + λγᵀRγ`, `tr(A^♯B) = PB_ee + λtr(RB)`, and hence (1.2).
- **E2** (I.2) exactly: `∫_{−a/β}^0(a² − β²λ²)dλ = 2a³/(3β)`, and `= P²|U_red|³/(9κ)` at `a = |P||U_red|`, `β = 6κ|P|`.
- **E3** (G.1) by exact Gaussian conditioning on the pins, from the derivative moments of `e^{−|z|²/2}`, in `d = 2, 3, 4`:
  the conditional variances `2, 2` of `γ_e`, `B_ee`, their zero covariance, their zero regression on `∂_u³f` (the law does not
  depend on `k`), and the conditional variance `6` of `∂_u³f` (the factor `e^{−12k²}`); with `e` a coordinate axis and, in
  `d ≥ 3`, `e = (3/5)e₂ + (4/5)e₃`.
- **E4** `E[(γ²/4 − 3kB)³] = 15/8 + 27k²` as a polynomial in `k` (Gaussian moments), `g(0) = 15/8`, `27/g(0) = 72/5 = 6·12/5`;
  and the Gamma identity's bookkeeping, derived from the substitution `t = ak²`: the exponents of `t` and `a` in the two
  terms, the conditions `−1 < s₁ < 0 < s₂` for `∫(e^{−t} − 1)t^{s₁−1}dt = Γ(s₁)` and `∫e^{−t}t^{s₂−1}dt = Γ(s₂)`, the
  recurrence `Γ(s₁) = Γ(s₂)/s₁` with `s₂ = s₁ + 1 = 1/6`, and the resulting coefficient `(1/2)(b − 6a/5)` of `Γ(1/6)a^{−1/6}`,
  which vanishes at `(a, b) = (12, 72/5)`. The values `Γ(1/6)`, `Γ(−5/6)` themselves are not computed.
- **E5** The constants: (3.2)'s `(12/9)(1/64) = 1/48` and `(1/48)/(5/24) = 1/10`; `E[γ⁶] = 120`; (G.3)'s `(1/3)(1/10) = 1/30`;
  and the factors `(1/30)(25/48) = 5/288` and `(1/30)(125/192) = 25/1152` of Corollary 1′'s values.
- **E6** The domination of §4 on exact perfect powers: `min(ℓ^{1/3}s, s^{−3}) + min(s³, s^{−3}) ≤ 2min(1, s^{−3})` for
  `s ≤ ρℓ^{−1/3}`, `ρ ≤ 1`; `κ = ℓ^{−1/3}s^{−4}`; and `s ds = (1/3)k^{−5/3}dk` as exponent arithmetic.
- **E7** Step 4's strip on random rational instances (`m = 1, 2, 3`; `A_M` with one positive eigenvalue and the others
  `≤ −η`; `r` a rational square): the Schur identity `det K_M = det A_M·σ_M`, the bound
  `σ_M ≤ α_M + r|β_M|²/η`, and, whenever that bound is negative, the sign `s` of `det K_M` (so `𝔞 > 0`).
- **E8** (2.3) as an exact identity for both signs `s = ±1`: `x² − y² = a² − β²λ² + ϱ` with the cross term `2PU_red·λW`.
- **E9** §3's bound on `ϱ` for `κ ≥ 1` on the window `|λ| ≤ γ_e²/(12κ)`, including instances with large `|P|`.

Mutants, each rejected with exit 1, empty stdout and `FAILED: <group>` on stderr:

| Mutant | Change | Fails at |
|---|---|---|
| M1 | `R` with the factor `∏_{i≠j}λ_i` taken over all `i ≤ m` | `E1_edge` |
| M2 | the layer constant `2/3 → 1/2` | `E2_layer` |
| M3 | `B_ee` conditioned without the pin `∂_uf(0)` | `E3_jets` |
| M4 | `E[X³]`'s coefficient `27 → 24` | `E4_moments` |
| M5 | `12/9 → 12/8` in `a₁` | `E5_constant` |
| M6 | the dominating exponent `s^{−3} → s^{−2}` | `E6_domination` |
| M7 | the bound on `σ_M` without the term `r|β_M|²/η` | `E7_strip` |
| M8 | (2.3)'s cross term with a factor `s` | `E8_cross` |
| M9 | §3's bound on `ϱ` without the factor `1 + |P|` | `E9_tail` |
| M10 | the Gamma recurrence inverted, `Γ(s₁) = s₁Γ(s₁ + 1)` | `E4_moments` |

**What the controls do not test.** The analytic estimates of §§2–4 (the localization, the strip and layer bounds, the edge
limits, dominated convergence), Weyl's formula, Haynsworth's additivity and the eigenvalue perturbation bound, Lemma Π,
Lemma K, (W⁺.2), Theorem U⁼, the Gamma-function values themselves, #242's (1.0a) and Corollary 1′, Proposition G″'s
continuity argument, and the numerical values of §5.

## 8. Review slices

- **A: §§0–2.** The statements, Lemma 0, the identities (I.1)–(I.2), and Lemma F₃'s proof: the localization, typedness near
  the edge, the strip (the Schur-complement argument), and the layer. Controls E1, E2, E7, E8; mutants M1, M2, M7, M8.
- **B: §§3–4.** Lemma T₁ and the identity `a₁ = (1/10)∫F₀db`, and Theorem C3's proof: the decomposition, the domination, the
  pointwise limit. Controls E5, E6, E9; mutants M5, M6, M9.
- **C: §§5–6 and the header.** Proposition G, Corollary G′ and Proposition G″ (the jet laws, `g`, the Gamma identity,
  positivity, the transfer to the torus field, the values), the remarks, and the header for overclaim. Controls E3, E4 and
  E5's (G.3) checks; mutants M3, M4 and M10.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_