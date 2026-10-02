# The fold-scale rejection limit through #242's soft model: Conjecture 6 of Math- #242 in every dimension, and its identification with the failure law of #170/#175

Object: CL-FOLD-LIMIT-20261002-v1.4. Versions:
- v1, `008b299`.
- v1.1, `0740b2c`: the prior-work record AUTH-243-01, and Proposition FL.7.
- v1.2, `11a4cd4`: rebinds #242 v1.2, and cites Codex's direct `d ≥ 3` cross-check of FL.7. Nonauthor slices A–E
  reviewed this head.
- v1.3: applies the four minor findings of those reviews, OA-243-B-01, B-02, B-03 (Proposition FL.4) and D-01 (Step 5 of
  Theorem FL). It records Codex's reviewed direct identity D.1 after Proposition FL.7, and rebinds #242 v1.3, whose
  §§0–3 are byte-identical to v1.2. No statement changes; §9 lists the changed bytes.
- v1.4: rebinds #242 v1.4 (`ffc7005`, blob `c1592915`). #242 v1.4 changes only its header and §5, after the C78 delta
  review (5394316763), so the consumed §§0–3 are still byte-identical to the bytes the slice reviews read. The workflow now
  resolves the #242 PR before reading the source. Once #242 has merged, its pinned blob must be in this tree, with no
  fallback to the historical head. This applies the automated finding 4167121714 (raised on #244, same pattern). No
  statement or proof changes; §9 lists the changed bytes.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 2 October 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE (Theorem FL, Propositions FL.4 and FL.7, Lemmas FL.1–FL.3; Corollaries FL.5 and FL.6
recover merged results of #170 and #175).
Nonauthor review required. Scientific effect: NONE — no register, graph, STATUS, PROOF_INDEX, prize or Boolean change; no
numerical constant is certified. Same GitHub account as every lane; zero organizational independence.

**Why.** Math- #242 (open) studies the rejected pairs at the end `κ = ℓ/r⁴ → ∞` of the cusp scale. It defines the fold-scale
rejection rate `F(k; b, u)` through an explicit soft model `G_k` and the elder decision of its Lemma 2 (#242 (3.1)), and states
as **Conjecture 6** that the actual rejected kernel at a fixed gap `k = ℓ/r³` converges to it:

    lim_{r↓0} (k/r)·r^{−2}A_r^{rej}(b, k, u) = F(k; b, u).                                                         (0.0)

**Prior work (recorded in v1.1, AUTH-243-01).** That the left side of (0.0) converges is not new. Two OpenAI packets are
merged on `main` as author-side candidates, each at its stated conditional scope:
- Math- #170 (`d = 2`), conditional on its Theorem E and its source interfaces;
- Math- #175 (fixed `d ≥ 3`), conditional on its source interfaces and its Theorem H.

Their Theorems S and F prove, at fixed marks, `r^{−3}(1 − p_r) → a_fail` (`= α₁ + α₂` in #170, `a1 + a2` in #175). This is an
identified Gaussian integral over the window-saddle classifier of #170's typed cubic. Their §§9 and 7 give the compact-window
`ℓ^{2/3}` coefficient. Since `(k/r)r^{−2}A_r^{rej} = kA_r·r^{−3}(1 − p_r)`, the left side of (0.0) tends to `kA_∗a_fail`. Two
further statements here are also theirs:
- the decision transfer from a window model to the global field (#170 Theorem E(2)–(3), #175 Theorem H);
- the lower bound `d(M̂) ≥ L_S` by a critical chord through `S` (#170 §3).

#242 and v1 of this note did not cite them. What Conjecture 6 adds is the identification of the limit with #242's `F`.

This note proves (0.0) in every `d ≥ 2` along a partly different route (§§1–3). It identifies the two limits directly in
`d = 2`, and by uniqueness of limits in `d ≥ 3` (Proposition FL.7). Theorem FL is the fold-scale counterpart of #207's
Theorem CU.4 (the cusp kernels at a fixed `κ`). Its decision step is #242's Lemma 2: the slices are cubic, and in one case
the saddle is a slice minimum. The transverse curvature is zoomed at the scale `r` (the soft layer), and the domination
comes from the parent's deterministic cap region ([P] §7), which confines rejection to that layer. The zoom and the
domination are as in #170 §8 and #175 §§2 and 4.

**What is new.**
- **Theorem FL** (§3). (0.0) holds for every `d ≥ 2`, `L > 0`, `b ∈ R`, `k > 0` and `u ∈ S^{d−1}`, uniformly for `(b, k)` in
  compact subsets of `R × (0, ∞)`. The limit defining `F` in #242 (3.1) exists, and `F` is continuous and positive.
  - *Relative to #170/#175,* which are pointwise at fixed marks, the identification with `F`, the continuity and the local
    uniformity are new.
  - *The decision and convergence steps take a different route.* They condition on the contact Hessian with a Weyl zoom
    and use #242's slice decision with Proposition FL.4. They do not consume [CUB], [TWO], [SC], [LOCAL] or #175's
    hard-fibre lemma.
  - *The domination step is the same cap-region mechanism as theirs.*
- **Proposition FL.7** (§4, the identification). #242's model and #170's cubic are the same function,
  `G_k(X, ζ) = P_θ(X, kζ)/k` with `θ = (−λ̃/k, γ, B, C_3)`, and their typed domains, limiting weights and maximin decisions
  agree.
  - In `d = 2`, `F = kA_∗a_fail` is a direct identity of model integrals. With #170 Theorem S it gives a second proof of
    (0.0) at each fixed `(b, k, u)`.
  - In `d ≥ 3` the identity follows from Theorem FL and #175 Theorem F by uniqueness of limits. It is therefore conditional
    on #175's interfaces. Codex's supplement D.1, reviewed by another Codex agent, gives it directly as an identity of
    model integrals in every fixed `d`, without #175 Theorem F (Remark after Proposition FL.7).
- **Corollaries FL.5 and FL.6** (§4) are not new. They are #170 Theorem S and §9 (`d = 2`) and #175 Theorem F and §7
  (`d ≥ 3`), recovered with the constants in #242's form:
  - `r^{−3}(1 − p_r) → F/(k·A_∗)`, now locally uniformly in `(b, k)`;
  - `ν_cand − ν_eld = d_{𝐁,𝐊}ℓ^{2/3} + o(ℓ^{2/3})`, with `d_{𝐁,𝐊} = C_fail^{𝐁,𝐊}` of #170 §9 in `d = 2`.
- **Proposition FL.4** (§2) re-proves, in #242's normalization, the decision transfer of #170 Theorem E(2)–(3) and #175
  Theorem H. For every parameter `ϖ` in a full-measure set `𝒦`, every `C²`-small perturbation of the model with the two pins
  as critical points has the model's elder decision. This holds for the global superlevel filtration of any field that
  realizes the perturbation in a window.
  - *What differs is the method:* explicit paths and traps crossing the saddle along model curves (Lemma FL.3), an `ε`-form
    for a merely continuous global field, and the generic set `𝒦` adapted to #242's slice decision.
  - In `d ≥ 3` the stiff directions enter as a negative definite form; this is #175's hard tube.
- **Lemma FL.2** (§2). `𝒦` has full measure, with explicit Jacobians `z⁴(X ± ½)/(96φ²)` for the level conditions.
  - In the model a rejected maximum always dies strictly above the saddle level. This is #170 §3's critical chord through
    `S`; OpenAI Codex observed it on #242 as an axial path.
  - #242's case (D′) requires `χ > 0`: for `β > 2`, `χ < 0` the pair is always rejected.
- **Lemma FL.1** (§1) makes #242's expansions (2.1) and (2.6) quantitative: the soft window of a pinned `C⁵` field is
  `C²`-close to the model, at rate `r` (`d = 2`) or `r^{1/2}` (`d ≥ 3`), with a constant linear in `‖f‖_{C⁵}` and independent
  of the transverse eigenvalues.

**What is not claimed.**
- Conjecture 7 of #242 (the `ℓ^{2/3}` term of the unrestricted `ρ_rej`) is not proved. It needs (0.0) uniformly from the
  cusp scale to the fold scale with integrable errors, and the intermediate separations (#242 §4, inputs (i)–(iii)).
- Theorem FL is a limit without rate, at fixed `k` (locally uniformly). No numerical value is certified.
- No priority is claimed for #170's and #175's results:
  - the existence of the limit in (0.0);
  - the constant in `1 − p_r ~ r³`;
  - the compact-window `ℓ^{2/3}` coefficient;
  - the transfer of the window decision to the global field;
  - the critical-chord bound `d(M̂) ≥ L_S`.

**Dependencies.**
- Consumed (merged):
  - [P] (`imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d`): §1 (`Q`, `W_r`, `Z_r`,
    `p_r`), §2 (finite-jet rank), §3 ((3.3)–(3.5)), §§5–6 ((5.3), (6.2)), §7 (the cap region and (7.7)), §8 (pinned
    genericity and the maximin), §§10–12 ((10.2), (10.3), (11.1)–(11.2), (12.1), (12.3)).
  - [CAP] (`imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md`, blob `0633aca3`): §§1 and 5, the deterministic cap
    theorem, as used in [P] §7: on its cap region every `C⁴` field with the pins has maximin `d_f(M) = f(S)`.
  - [R] (`frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf`): (R2)–(R3) (the coupling; the pathwise
    bound (3.2) is derived from them), (R5), (R11).
  - #207 (`frontiers/cusp_second_order_20261001/PROOF.md`, blob `f6df5a73`): §0 (the elder mark and the maximin), Theorem
    CU.1 (the pin identities), and the structure of Proposition CU.3 and Theorem CU.4.
  - [C7-K] (`frontiers/c7_total_bounded_20260929/PROOF.md`, blob `28748b08`): (K2).
- Consumed (unmerged): #242 (`frontiers/soft_rejected_pairs_20261002/PROOF.md` at `ffc7005`, blob `c1592915`; v1.4): §0,
  (2.1)–(2.5), Lemmas 2 and 3, Proposition 2′ ((2.6)), (3.1). #242's §§0–3 are byte-identical to its v1.2 (blob
  `ad4beb84`), which the slice reviews of v1.2 of this note read. v1.3 changed only #242's header, §4's numerical
  sentences and §§5–9, and v1.4 only its header, §5 and §9. This note must be rebound if that blob changes.
- Consumed through #207 §0: [E2] (`reviews/d1_section9_borel_repair_20260925/REPAIR.md`, blob `fe9b9ce4`), for the Borel
  measurability of the elder mark. Reading rules for [P]: [E1] (`imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md`,
  blob `213594d6`) and [REC] (`reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md`, blob `75da2597`).
- Compared (merged, author-side candidates at their stated conditional scope), and consumed by Proposition FL.7 only:
  - #170 (`frontiers/local_elder_geometry_20260930/PROOF.md`, blob `ef2aa579`):
    - §2: the typed cubic `P_θ`, `B′`, `C(P)`, the null sets, and Theorem E(1);
    - §§7 and 8.1: the classifier `n(θ)`, (S1) and the weight `w_+`;
    - §8.5 (S11): the weight limit;
    - §8.6: the mass `α₁ + α₂`;
    - Theorem S, (S2);
    - §9: `C_fail`.
  - #175 (`frontiers/concave_fibre_elder_20260930/PROOF.md`, blob `923d3236`):
    - §§1–2: the model and the soft cubic, `n ∈ {0, 1, 2}`;
    - §3: Theorem H;
    - §5: Theorem F, (S1)–(S3);
    - §7.

  Through them, FL.7 depends transitively on #170's [CUB] classifier (via Theorem E(1)). In `d ≥ 3` it also depends on
  #175's source interfaces ([SC], [LOCAL], and the hard-fibre lemma).
- Cited only: OpenAI Codex's #242 Slice B review (comment 5948352439, the axial path in Lemma FL.2(c)); OA dimension lift
  (`frontiers/elder_dimension_lift_20260928/PROOF.md`, blob `7303bd79`): (A3); #229
  (`frontiers/third_order_rate_20261001/PROOF.md`, blob `110ed33a`): (R⁺.1); #242 Theorem 1 and Proposition 4 (same blob as
  above).

## 0. Setting and notation

Setting and notation are those of #242 §0 and §2, through #207 §0 and [P].
- **The field and the pair.** Fix `d ≥ 2`, `m := d − 1`, `L > 0`, and the [P] field on `X = R^d/(LZ^d)`. The near pins are
  `M = −ru/2` and `S = ru/2`, at heights `b` and `b − kr³`, with zero gradients; the gap `k > 0` is **fixed**. `Q = Q_{r,b,k,u}`
  is the pinned law, `π_r(v_r)` the pin density, `W_r = |det H_M det H_S|1{H_M < 0, index H_S = m}` the typed weight, and
  `e = 1{d_f(M) = f(S)}` the elder mark for the maximin `d_f(M) = sup{min_t f(γ(t)) : γ(0) = M, f(γ(1)) > f(M)}` (#207 §0;
  Borel by [E2]). The kernels are
  
      A_r := 12π_r(v_r)E_Q[W_r/r²],    A_r^{rej} := 12π_r(v_r)E_Q[(W_r/r²)(1 − e)],    1 − p_r = A_r^{rej}/A_r,          (0.1)
  
  with `p_r = p_r(b, k, u)` the selection probability of [P] §1 (there written `p_r(b, k, R)`, with frame `R` and `u = Re_1`),
  and `A_r → A_∗(b, k, u) := 12π_0(u; v_0(b, k))z_0(b, k, u) > 0` ([P] (10.3), where it is written `A_0`; [R] (R11)).
- **The contact law** at `v_0(b, k)` is the law of the field given `f(0) = b`, `∂_uf = ∂_u²f = 0`, `∂_u³f = 12k`,
  `∇_Θf = ∇_Θ∂_uf = 0` at `0` ([P] (3.3)–(3.4)); `E_{v_0(b,k)}` is its expectation. Its transverse Hessian `𝔸 := D_Θ²f(0)` is a
  nondegenerate Gaussian matrix with density `p_𝔸 ≤ C_0e^{−c_0|·|²}` on `Sym(m)` ([P] §§3, 5).
- **Jets and the soft eigenvalue.** For `f ∈ C⁵` let `A := D_Θ²f(0)`, and let `λ_1 ≤ λ_2 ≤ ⋯ ≤ λ_m` be the eigenvalues of
  `−A` (of either sign) with an orthonormal eigenbasis `e_1, …, e_m`. Put

      λ̃ := kλ_1/r,    γ := ∂_u²∂_{e_1}f(0),    B := ∂_u∂_{e_1}²f(0),    C_3 := ∂_{e_1}³f(0),    Y := 3kB − γ²/4.          (0.2)

  When `λ̃ > 0` and `γ ≠ 0`, the normalized parameter of #242 (2.2) is `ϖ = ϖ(f) := (φ, β, χ)` with

      φ := γ²/(24λ̃),    β := kB/λ̃ = 2tφ,    χ := k²C_3γ/λ̃² = χ_0φ²,    t := 12kB/γ²,    χ_0 := 576k²C_3/γ³.            (0.3)

  These do not depend on the sign of `e_1`.
- **The model** (#242 (2.3)). `G_ϖ(X, z) = A₀(X) + ½(X² − ¼)z − ½(1 − βX)z² + (χ/6)z³`, `A₀(X) = (X + ½)²(X − 1)/(12φ)`,
  `L_S := −1/(24φ)`, with critical points `M̂ = (−½, 0)` (value `0`) and `Ŝ = (½, 0)` (value `L_S`). It is *typed* iff
  `ϖ ∈ 𝒯 := {φ > 0, |φ − β/2| < 1}`; this is #242 (2.4). The slice notation `p = X² − ¼`, `a = 1 − βX`, `D = a² − χp`, the
  ridge and valley values `R(X)`, `V(X)` at the slice critical points `z_r(X)`, `z_v(X)`, open slices, and the interval `I_M`
  are those of #242 §2. For typed `ϖ`, `e(G_ϖ) := 1{d(M̂) = L_S}` is the actual elder decision of `G_ϖ` on `R²`, with
  `d(M̂)` the maximin of #207 §0 for `G_ϖ`. On the generic set `𝒦` of §2 it is the decision of #242 Lemma 2, and #242's
  rejected set `𝓡(t, χ_0)` and integral `I(t, χ_0)` ((2.5) there) are read with this decision.
- **Windows.** The soft window and its normalized form are

      Φ(X, ζ, η) := rXu + rkζe_1 + r^{3/2}Σ_{i≥2}η_ie_i,    𝔉(X, ζ, η) := (f(Φ(X, ζ, η)) − b)/(kr³),
      𝔊(X, z, η) := (λ̃/γ²)𝔉(X, (γ/λ̃)z, η).                                                                        (0.4)

  The model of #242 (2.1), (2.6) is `G_k^{(d)}(X, ζ, η) := G_k(X, ζ) − (1/(2k))Σ_{i≥2}λ_iη_i²`, with `G_k` built from
  `(λ̃, γ, B, C_3)`. By #242 (2.3), `(λ̃/γ²)G_k^{(d)}(X, (γ/λ̃)z, η) = G_ϖ(X, z) − 𝔮(η)`, where
  `𝔮(η) := ½ηᵀ𝒬η` and `𝒬 := (λ̃/(kγ²))diag(λ_2, …, λ_m)`.

## 1. The soft window

**Lemma FL.1 (the soft window).** Let `w ≥ 1` and `0 < k_− ≤ k_+`. There are `C = C(d, w, k_±)` and `r_0 = r_0(d, w, k_+, L)`
with the following property. Let `0 < r ≤ r_0`, `k ∈ [k_−, k_+]`, and let `f ∈ C⁵(X)` have critical points `M = −ru/2` and
`S = ru/2` with `f(M) = b` and `f(S) = b − kr³`. Then on `𝒲_w := {|X| ≤ w, |ζ| ≤ w, |η| ≤ w}`,

    ‖𝔉 − G_k^{(d)}‖_{C²(𝒲_w)} ≤ C‖f‖_{C⁵(X)}ϑ(r),    ϑ(r) := r (d = 2),  r^{1/2} (d ≥ 3).                         (1.1)

The bound holds for every sign and size of `λ̃` and of the `λ_i`, which enter `G_k^{(d)}` exactly.

*Proof.* Put `N := ‖f‖_{C⁵}`, `x = rX`, `y_1 = rkζ` and `y_i = r^{3/2}η_i` (`i ≥ 2`), in the eigenframe of `A`. Expand `f` at
`0` to total order `4`. The remainder `ρ_5` satisfies `|∂^αρ_5| ≤ C_dN(|x| + |y|)^{5−|α|}` for `|α| ≤ 2`. On `𝒲_w`,
`|x| + |y| ≤ c_wr`, and `∂_X = r∂_x`, `∂_ζ = rk∂_{y_1}`, `∂_{η_i} = r^{3/2}∂_{y_i}`. So `(kr³)^{−1}ρ_5∘Φ` is `O(Nr²)` in
`C²(𝒲_w)`. The Taylor monomial `x^iy_1^jy′^l` (`l` a multi-index over `i′ ≥ 2`) contributes
`r^{ex(i,j,l)}k^{j−1}X^iζ^jη^l` times its coefficient, with

    ex(i, j, l) := i + j + 3|l|/2 − 3.                                                                               (1.2)

Apart from the monomials listed below, every monomial of degree `≤ 4` has `ex ≥ 1` when `|l| ≠ 1` and `ex ≥ ½` when
`|l| = 1`, and its coefficient is a derivative of order `3` or `4`, bounded by `N`. The listed monomials are pinned or
exact:
- `|l| = 0`, `i + j ≤ 3`. The axial pins give, exactly as in #207 Theorem CU.1 with `κr⁴ = kr³`,
  `f(0) − b = −kr³/2 + f_4r⁴/384 + O(Nr⁵)`, `∂_uf(0) = −(3/2)kr² + O(Nr⁴)`, `∂_u²f(0) = −(r²/24)f_4 + O(Nr³)` and
  `∂_u³f(0) = 12k + O(Nr²)`. The transverse pins give `∂_{e_1}f(0) = −(r²/8)γ + O(Nr⁴)` and `∂_u∂_{e_1}f(0) = O(Nr²)`. And
  `∂_{e_1}²f(0) = −λ_1 = −λ̃r/k` exactly. Inserting these, the monomials with `i + j ≤ 3` give #242 (2.1):
  `G_k(X, ζ) + O(Nr)`. The `O(Nr)` collects `f_4r(1/16 − X²/2)/(24k)` and `∂_u∂_{e_1}f(0)Xζ/r`; with the `x⁴` monomial the
  `f_4`-terms form #242's `rf_4(X² − ¼)²/(24k)`.
- `|l| = 2`, `i = j = 0` (`ex = 0`): `½Σ∂_{e_i}∂_{e_{i′}}f(0)y_iy_{i′} = −½Σλ_iy_i²`, which gives `−(1/(2k))Σλ_iη_i²`
  exactly.
- `|l| = 1`, `i + j ≤ 1` (`ex ≤ −½`). The transverse pins along `e_i` give `∂_{e_i}f(0) = −(r²/8)γ_{e_i} + O(Nr⁴)` and
  `∂_u∂_{e_i}f(0) = O(Nr²)`; the eigenframe gives `∂_{e_1}∂_{e_i}f(0) = 0`. They contribute
  `−(r^{1/2}/(8k))γ_{e_i}η_i + O(Nr^{3/2})`, which is `O(Nr^{1/2})`.

In `d = 2` only `|l| = 0` occurs, so every unlisted monomial has `ex ≥ 1`. This proves (1.1). ∎

These are #242's expansions (2.1) and (2.6), read as deterministic Taylor statements with an explicit remainder, as #207
Theorem CU.1 does at the cusp scale. Control F3 checks the exponent bookkeeping (1.2) and the rates. If `λ̃ > 0` and `γ ≠ 0`, then (0.4)
gives, on `𝒲′ := {|X| ≤ w, |z| ≤ wλ̃/|γ|, |η| ≤ w}`,

    ‖𝔊 − (G_ϖ − 𝔮)‖_{C²(𝒲′)} ≤ (λ̃/γ²)max(1, |γ|/λ̃)²·C‖f‖_{C⁵}ϑ(r).                                              (1.3)

## 2. The model decision is stable

### 2.1 Generic parameters and the shape of a rejection

Let `𝒦` be the set of `ϖ ∈ 𝒯` such that:
- (G0) `β ≠ 2`, `χ ≠ 0` and `β² ≠ χ`;
- (G1) `M̂` is the only critical point of `G_ϖ` at level `0`, and `Ŝ` the only one at level `L_S`;
- (G2) `R` has no finite limit along an unbounded `I_M` (the third hypothesis of #242 Lemma 2);
- (G3) no open slice has its inflection value equal to `L_S`: there is no `X` with `D(X) = 0` and
  `A₀(X) + a(X)³/(6χ²) = L_S`.

**Lemma FL.2 (generic parameters).**
- (a) `𝒯 ∖ 𝒦` is a Lebesgue null set, and on `𝒦` the hypotheses of #242 Lemma 2 hold.
- (b) For `ϖ ∈ 𝒦`, every finite end `X_e` of `I_M` is either a non-open slice with `R(X_e) = L_S`, or an open slice whose
  inflection value `A₀(X_e) + a(X_e)³/(6χ²)` (the common limit of `R` and `V`) exceeds `L_S`.
- (c) For every typed `ϖ`, `d(M̂) ≥ L_S`; so `e(G_ϖ) = 0` if and only if `M` dies strictly above `L_S`. For `ϖ ∈ 𝒦` with
  `e(G_ϖ) = 1`, either `β < 2` and case (D) of #242 Lemma 2 holds, or `β > 2`, `χ > 0` and case (D′) holds.

So in the model a rejected maximum never survives below the saddle level, and (D′) requires `χ > 0`.

*Proof of (a).* (G0) excludes three null sets.

(G1). Write `Γ_0 := (∂_XG_ϖ, ∂_zG_ϖ, G_ϖ)` and `Γ_S := (∂_XG_ϖ, ∂_zG_ϖ, G_ϖ − L_S)` as functions of `(X, z, ϖ)`. Since
`∂_φA₀ = −A₀/φ` and `∂_φL_S = 1/(24φ²)`, their Jacobians in `ϖ = (φ, β, χ)` have determinants (control F2)

    det ∂_ϖΓ_0 = z⁴(X + ½)/(96φ²),    det ∂_ϖΓ_S = z⁴(X − ½)/(96φ²).                                               (2.1)

So on `{z ≠ 0, X ≠ −½}` the map `Γ_0` is a submersion. Its zero set there is a two-dimensional submanifold of `R² × 𝒯`, and
the projection of that set to `𝒯 ⊂ R³` is null (Sard). On the line `X = −½` a critical point with `z ≠ 0` has
`z = (2 + β)/χ = 1/β` and value `G_ϖ(−½, z) = −z²(2 + β)/12 ≠ 0`, since `2 + β > 2φ > 0` on `𝒯`. On `{z = 0}`,
`∂_zG_ϖ = ½(X² − ¼)` vanishes only at `M̂` and `Ŝ`. The same argument for `Γ_S` uses the line `X = ½`, where a critical
point with `z ≠ 0` has value `G_ϖ − L_S = −z²(2 − β)/12 ≠ 0`.

(G2). If `β² < χ`, then `D → −∞` as `|X| → ∞` and `I_M` is bounded. If `β² > χ`, put `ω := (β² − χ)^{1/2}`. Then
`D(X) ~ ω²X²`, the slices are non-open for large `|X|`, and along them `R(X) = A₀ + (p/3)z_r − (a/6)z_r²` with
`z_r ~ X/(ω − β)` as `X → +∞` and `z_r ~ −X/(ω + β)` as `X → −∞` (`ω ≠ ±β` by (G0)). Hence `R(X) = κ_±X³ + O(X²)` as
`X → ±∞`, with

    κ_+ := 1/(12φ) + (2ω − β)/(6(ω − β)²),    κ_− := 1/(12φ) − (2ω + β)/(6(ω + β)²).                               (2.2)

For fixed `(β, χ)` each `κ_±` is strictly monotone in `φ`, so it vanishes for at most one `φ`. Off the null set
`{κ_+κ_− = 0}`, `R → ±∞` along every unbounded direction, so (G2) holds. (The witness of control F4 has `κ_+ = 0` exactly; its
`I_M` is bounded, so (G2) holds for it all the same.)

(G3). On `{D = 0}` the slice has a double critical point `z = a/χ`, with value `A₀ + a³/(6χ²)`. The map
`(X, ϖ) ↦ (D, A₀ + a³/(6χ²) − L_S)` has Jacobian determinant in `(φ, χ)` equal to `−p(A₀ − L_S)/φ` on `{D = 0}`, and
`A₀ − L_S = (X − ½)²(X + 1)/(12φ)` (control F2). Off `X ∈ {±½, −1}` the map is a submersion, and its zero set projects to a
null set. At `X = −1` the conditions force `a(−1) = 0` and then `χ = 0`; at `X = ½` they force `β = 2`; at `X = −½`,
`D = (1 + β/2)² > 0`.

*Proof of (b).* At a non-open end `R(X_e) = L_S` by continuity. At an open end the ridge and valley values tend to the
inflection value, which is therefore `≥ L_S`; equality is excluded by (G3).

*Proof of (c).* The axial segment `{(X, 0) : −½ ≤ X ≤ 2}` carries `G_ϖ = A₀`, with `A₀ − L_S = (X − ½)²(X + 1)/(12φ) ≥ 0`
(equality only at `Ŝ`), and it ends at `A₀(2) = 25/(48φ) > 0`. So `d(M̂) ≥ L_S` for every typed `ϖ`. This is #170 §3's
critical-chord bound through `S` (for a cubic, the restriction to a chord between two critical points is
`P(M) + (P(Y) − P(M))(3t² − 2t³)`). OpenAI Codex observed it for #242's model in its review of Lemma 2
(comment 5948352439). Hence `e(G_ϖ) = 1` iff `d(M̂) ≤ L_S`, i.e. iff for every
`c > L_S` the point `M` is the highest point of its component of `{G_ϖ > c}`. Assume this, with `ϖ ∈ 𝒦`. As in Step 1 of the
proof of Lemma 2:
- (i) `R < 0` on `I_M ∖ {−½}`. A point `X*` with `R(X*) > 0` would put a point above `0` into `M`'s component at the level
  `min_{[−½, X*]}R > L_S`. A point with `R(X*) = 0` and `R ≤ 0` nearby would be a critical point at level `0`, excluded by (G1).
- (ii) `V ≤ L_S` on `I_M`; otherwise a ridge piece and a far piece merge above `L_S`.
- (iii) `I_M` is bounded. `R` is an algebraic function of `X`, so it has a limit in `[−∞, ∞]` along an unbounded `I_M`; by
  (G2) the limit is `±∞`. `R → +∞` would give (i)'s first alternative, and `R → −∞` contradicts `R > L_S`.
- (iv) No end of `I_M` is open. By (b), at an open end `R` and `V` tend to a value `> L_S`, so `V > L_S` near it inside
  `I_M`, against (ii).

Now look at the slices with `|X| < ½` and `a(X) > 0`. If `χ > 0`, then `D = a² + χ|p| > a²`, so `z_r < 0 < z_v`. If `χ < 0`
and `D > 0`, then `z_v < z_r < 0`. In both cases `z = 0` lies on the ridge side of the slice, so

    R(X) > G_ϖ(X, 0) = A₀(X) > L_S,                                                                                 (2.3)

because `A₀ − L_S = (X − ½)²(X + 1)/(12φ) > 0` on `(−1, ½)`.
- *`β < 2`.* On `𝒯`, `β > −2`, so `a > 0` on `[−½, ½]`. By (iv) no slice in `(−½, ½)` is open: the first open slice to the right
  of `−½` would be an open end of `I_M`. By (2.3), `(−½, ½) ⊂ I_M`. Since `R(½) = L_S`, the right end of `I_M` is `½`.
  Moreover `V < L_S` on `(X_L, ½)`: a point with `V = L_S` would be a local maximum of `V`, hence a critical point at level
  `L_S` other than `Ŝ`. With (i)–(iii), this is case (D) of Lemma 2.
- *`β > 2`, `χ < 0`.* At `X = 1/β ∈ (0, ½)`, `a = 0` and `p < 0`, so `D = −χp < 0`: the slice is open. The first open slice to
  the right of `−½` lies in `(−½, 1/β]` and is an open end of `I_M`, against (iv). So this case does not occur: for `β > 2`,
  `χ < 0` the pair is always rejected.
- *`β > 2`, `χ > 0`.* For `|X| < ½`, `D = a² + χ|p| > a² ≥ 0`, so `z_r < 0 < z_v` whatever the sign of `a`, and (2.3) holds
  on `(−½, ½)`. At `½`, `R(½) = L_S + (2/3)|a(½)|³/χ² > L_S`. So `[−½, ½] ⊂ I_M`. As before `V < L_S` on `I_M ∖ {½}`; at `½` the
  valley point is `Ŝ`. With (i)–(iii), this is case (D′). ∎

### 2.2 Crossing a saddle

**Lemma FL.3 (crossing a nondegenerate critical point).** Let `H_0` be a polynomial on `R^n` with a critical point `s`, let
`c ∈ C²(B̄_{ρ_0}; R^n)`, `B̄_{ρ_0} ⊂ R^j` a closed ball of some radius `ρ_0 > 0`, with `c(0) = s` and `Dc(0)` injective, and
suppose the form `Dc(0)ᵀHess H_0(s)Dc(0)` is positive definite (respectively negative definite). There are `ρ_3 ∈ (0, ρ_0]`
and `ε_0 > 0` such that: for every `H ∈ C²(B(s, 2ρ_c))` with `∇H(s) = 0` and `‖H − H_0‖_{C²(B(s, 2ρ_c))} ≤ ε_0`, where
`ρ_c := ρ_3 sup|Dc|`, the function `H∘c − H(s)` is positive (respectively negative) on `0 < |w| ≤ ρ_3`.

*Proof.* Put `h := H∘c`. Then `∇h(0) = Dc(0)ᵀ∇H(s) = 0` and
`Hess h(w) = Dc(w)ᵀHess H(c(w))Dc(w) + Σ_i∂_iH(c(w))Hess c_i(w)`. For `|w| ≤ ρ_3`:
`Hess H(c(w)) = Hess H_0(s) + O(ρ_3 + ε_0)`, because `H_0` has a Lipschitz Hessian on compacts;
`|∇H(c(w))| ≤ |∇H_0(c(w))| + ε_0 = O(ρ_3 + ε_0)`; and `Dc(w) = Dc(0) + O(ρ_3)`. So `Hess h` stays definite, with a fixed margin,
on `|w| ≤ ρ_3` when `ρ_3` and `ε_0` are small. Taylor's formula with integral remainder at `0` gives the sign. ∎

### 2.3 The stability proposition

**Proposition FL.4 (stability of the model decision).** Let `ϖ ∈ 𝒦` and let `𝒬` be a positive definite
`(m − 1) × (m − 1)` matrix (nothing if `m = 1`), `𝔮(η) := ½ηᵀ𝒬η`, `q_− := λ_min(𝒬)`.

*Convention for `m = 1` (OA-243-B-01).* There are then no stiff variables `η`. Read `W × B̄_{R_η}` as `W`, `𝔮` as `0`, and
`M̂_0`, `Ŝ_0` as `M̂`, `Ŝ`. Every clause below that involves `η`, `𝒬`, `q_−` or `R_η` is vacuous and is omitted, including the
term `q_−ρ²/8` in the choice of `ε` and the choice of `R_η` in Step 4.

There are a compact rectangle
`W = W_ϖ ⊂ R²` containing `M̂` and `Ŝ` in its interior, a radius `R_η = R_η(ϖ, 𝒬)` and an `ε = ε(ϖ, 𝒬) > 0` with the
following property. Let `𝔊 ∈ C²(W × B̄_{R_η})` satisfy

- (S1) `M̂_0 := (−½, 0, 0)` and `Ŝ_0 := (½, 0, 0)` are critical points of `𝔊`;
- (S2) `‖𝔊 − (G_ϖ − 𝔮)‖_{C²(W × B̄_{R_η})} ≤ ε`.

Let `f` be continuous on `X`, and let `Ψ : W × B̄_{R_η} → X` be continuous and injective, with `Ψ(M̂_0) = M`, `Ψ(Ŝ_0) = S` and
`f∘Ψ = b + s𝔊` for constants `b ∈ R` and `s > 0`. Then

    1{d_f(M) = f(S)} = e(G_ϖ).                                                                                       (2.4)

If moreover `f` is `C²` near `M` and `S` and `Ψ` is a `C²` diffeomorphism near `M̂_0` and `Ŝ_0`, then `M` is a nondegenerate
local maximum of `f` and `S` a nondegenerate critical point of index `m`.

*Proof.* The curves `σ_±`, the path `Γ`, the set `𝒟_2`, the constants `τ`, `Z`, `ρ_1`, `r_ϖ` and the rectangle `W` below
depend on `ϖ` only. The radius `ρ`, the margin `δ`, and `ε` and `R_η` depend on `ϖ` and `𝒬` (OA-243-B-03).

*Step 1 (types).* By (S2), `Hess 𝔊(M̂_0)` is within `ε` of `diag(Hess G_ϖ(M̂), −𝒬)`, which is negative definite (on `𝒯`,
`det Hess G_ϖ(M̂) = (1 + β/2 − φ)/(4φ) > 0` and `∂_z²G_ϖ(M̂) = −(1 + β/2) < 0`). Likewise `Hess 𝔊(Ŝ_0)` is within `ε` of
`diag(Hess G_ϖ(Ŝ), −𝒬)`, which has index `m` (`det Hess G_ϖ(Ŝ) = −(1 − β/2 + φ)/(4φ) < 0`). For small `ε` the inertia
persists (Weyl), and it transfers to `f` through `Ψ`.

*Step 2 (paths and traps).* Two elementary facts, valid for any `c′ ∈ R`.
- (Path) If `Γ ⊂ W × B̄_{R_η}` is a path from `M̂_0` to a point `𝔭̂` with `𝔊(𝔭̂) > 𝔊(M̂_0)`, and `𝔊 ≥ c′` on `Γ`, then
  `d_f(M) ≥ b + sc′`. Indeed `Ψ∘Γ` is a path from `M` to a point above `f(M)` along which `f ≥ b + sc′`.
- (Trap) Let `𝒟` be open in `R^d`, with `𝒟 ⊂ int(W × B̄_{R_η})` and `𝒟̄ ⊂ W × B̄_{R_η}`. Suppose `M̂_0 ∈ 𝒟`, `𝔊 ≤ c′` on
  `∂𝒟`, and `𝔊 < 𝔊(M̂_0)` on `𝒟 ∖ {M̂_0}`. Then `d_f(M) ≤ b + sc′`.

  Indeed, if `c′ ≥ 𝔊(M̂_0)`, the bound is trivial: every admissible path starts at `M`, so
  `d_f(M) ≤ f(M) = b + s𝔊(M̂_0) ≤ b + sc′` (OA-243-B-02). Let now `c′ < 𝔊(M̂_0)`, so that `M ∈ {f > b + sc′}`. By invariance
  of domain `Ψ(𝒟)` is open in `X`. Its closure lies in the compact set `Ψ(𝒟̄)`, so its boundary lies in `Ψ(∂𝒟)`, where
  `f ≤ b + sc′`. The path component `C` of `{f > b + sc′}` containing `M` therefore lies in `Ψ(𝒟)`, so `f < f(M)` on
  `C ∖ {M}`. A path from `M` to a point above `f(M)` must leave `C`, and so it meets `{f ≤ b + sc′}`.

*Step 3 (model certificates).* By Lemma FL.2(c), `ϖ ∈ 𝒦` falls in exactly one of three cases. Each comes with a
certificate built from `ϖ` alone and, for every small radius `ρ > 0`, a margin `δ = δ(ρ) > 0`; decreasing `ρ` decreases
`δ`. The radius `ρ` is fixed in Step 4, with `2ρ ≤ ρ_3`.

- **(R)** `e(G_ϖ) = 0`, so `M` dies above `L_S`. Then there is a compact path `Γ` from `M̂` to a point `𝔭` with
  `G_ϖ(𝔭) > 2δ`, along which `G_ϖ ≥ L_S + 2δ`. (By the definition of the maximin, and because components of open subsets of
  `R²` are path connected.)
- **(D), (D′)** `e(G_ϖ) = 1`. Then there are:
  - `C²` curves `σ_±` through `Ŝ` (`σ_±(0) = Ŝ`), with `σ_+′(0)` ascending and `σ_−′(0)` descending for `Hess G_ϖ(Ŝ)`;
  - a compact path `Γ` from `M̂` to a point `𝔭` with `G_ϖ(𝔭) > 2δ`, containing the arc `σ_+([−ρ, ρ])`, with
    `G_ϖ ≥ L_S + 2δ` on `Γ ∖ σ_+((−ρ, ρ))`;
  - a bounded open `𝒟_2 ∋ M̂` whose boundary contains `σ_−([−ρ, ρ])`, with `G_ϖ ≤ L_S − 2δ` on
    `∂𝒟_2 ∖ σ_−((−ρ, ρ))` and `G_ϖ ≤ −2δ` on `𝒟̄_2 ∖ B(M̂, ρ)`.

*The certificates exist in cases (D) and (D′).* Write `z_∂(X) := z_r(X) − Z·sgn χ` for a large constant `Z`; this is on
the side of the ridge point away from the valley. On that side the slice decreases to `−∞`, so `G_ϖ(X, z_∂(X)) < L_S − 1`
on any compact set of non-open slices once `Z` is large. For a compact interval `J` of non-open slices put

    𝒟_2(J) := {(X, z) : X ∈ int J, z strictly between z_∂(X) and z_v(X)}.                                          (2.5)

On each closed slice segment of `𝒟̄_2(J)` the slice rises from `z_∂` to its maximum `R(X)` at `z_r` and falls to `V(X)` at
`z_v`, so `G_ϖ ≤ R(X)` there.

By Lemma FL.2(b)–(c), the finite ends of `I_M` are non-open with `R = L_S`. They differ from `½` except for the right end in
case (D), so there `R′ ≠ 0` by (G1): a zero would make `(X_e, z_r(X_e))` a critical point at level `L_S`. Hence `R < L_S`
just outside `I_M`. (Here `R′` is the derivative of `R`.)
- *(D)* (`β < 2`). `I_M = (X_L, ½)`, with `V < L_S` and `R < 0` (for `X ≠ −½`) on `(X_L, ½)`. At `½`, `z_r(½) = 0`,
  `R(½) = L_S` and `V(½) = L_S − (2/3)a(½)³/χ² < L_S`.
  - *Curves.* `σ_−(t) := (½, t)` is descending: `∂_z²G_ϖ(Ŝ) = −a(½) < 0`. `σ_+(t) := (½ + t, z_r(½ + t))` is the ridge
    curve; it is ascending, because `σ_+′(0)ᵀHess G_ϖ(Ŝ)σ_+′(0) = R″(½) = det Hess G_ϖ(Ŝ)/∂_z²G_ϖ(Ŝ) > 0`.
  - *Trap.* `𝒟_2 := 𝒟_2([X_L − τ, ½])` for small `τ > 0`. Its right side is the segment
    `{½} × [z_∂(½), z_v(½)] ⊃ σ_−([−ρ, ρ])`, on which `G_ϖ < L_S` except at `Ŝ`. Its left side carries
    `G_ϖ ≤ R(X_L − τ) < L_S`, and its curved sides carry `G_ϖ < L_S`. Inside, `G_ϖ ≤ R(X) < 0` except at `M̂`.
  - *Path.* Follow the ridge from `M̂` to `σ_+(ρ_1)`. There `R ≥ L_S + 2δ` on `[−½, ½ − ρ]`, and `R > L_S` on `(½, ½ + ρ_1]`.
    Then go down the segment `{X_1} × [0, z_r(X_1)]`, `X_1 := ½ + ρ_1`. Since `p(X_1), a(X_1) > 0`, the slice is increasing
    on `[0, z_r(X_1)]`: for `χ > 0`, `0 < z_r < z_v`, and for `χ < 0`, `z_v < 0 < z_r`. So `G_ϖ ≥ A₀(X_1) > L_S` there.
    Finish along `{z = 0}` to
    `𝔭 := (2, 0)`. There `G_ϖ = A₀` and `A₀ − L_S = (X − ½)²(X + 1)/(12φ)` increases on `[X_1, 2]`, and
    `A₀(2) = 25/(48φ) > 0`.
- *(D′)* (`β > 2`, `χ > 0`). `½ ∈ I_M = (X_L, X_R)`, with `R < 0` on `I_M ∖ {−½}` and `V < L_S` on `I_M ∖ {½}`. At `½`,
  `z_v(½) = 0`, `V(½) = L_S`, `V″(½) = det Hess G_ϖ(Ŝ)/∂_z²G_ϖ(Ŝ) < 0`, and `z_r(½) = 2a(½)/χ` with `R(½) > L_S`.
  - *Curves.* `σ_+(t) := (½, t)` is ascending: `∂_z²G_ϖ(Ŝ) = −a(½) > 0`. `σ_−(t) := (½ + t, z_v(½ + t))` is the valley curve,
    which is descending: `σ_−′(0)ᵀHess G_ϖ(Ŝ)σ_−′(0) = V″(½) < 0`.
  - *Trap.* `𝒟_2 := 𝒟_2([X_L − τ, X_R + τ])` for small `τ > 0`. Its upper (valley) boundary carries `G_ϖ = V ≤ L_S`, with
    equality only at `Ŝ`, and `V ≤ L_S − 2δ` off `σ_−((−ρ, ρ))`. The other sides carry `G_ϖ < L_S`, and inside
    `G_ϖ ≤ R(X) < 0` except at `M̂`.
  - *Path.* Follow the ridge from `M̂` to `(½, z_r(½))`; there `R > L_S` on `[−½, ½]`. Then go along the slice `{½} × ·` through
    `Ŝ` to a point `𝔭 = (½, z_𝔭)` on the far side of `0`, with `G_ϖ(𝔭) > 2δ`. The slice at `½` has its only critical points at
    `z_r(½)` (maximum) and `0` (minimum, value `L_S`), and it tends to `+∞` on the far side.

In both cases the curves `σ_±`, the path `Γ` and the set `𝒟_2` do not depend on `ρ`, and for every small `ρ > 0`
compactness gives `δ(ρ) > 0`. In case (R), `δ` does not depend on `ρ` at all.

*Step 4 (persistence).* First fix a radius `r_ϖ > 0` and a compact rectangle `W = W_ϖ` whose interior contains `Γ`,
`𝒟̄_2` and the closed `r_ϖ`-discs about `M̂` and `Ŝ`. Both depend on `ϖ` only (OA-243-B-03).

The three maps are `t ↦ (σ_+(t), 0)` and `(t, η) ↦ (σ_−(t), η)` at `Ŝ_0`, and the identity at `M̂_0`. The forms of
`H_0 := G_ϖ − 𝔮` on their tangent spaces are `σ_+′ᵀ𝐇_Sσ_+′ > 0`, `diag(σ_−′ᵀ𝐇_Sσ_−′, −𝒬) < 0` and
`diag(Hess G_ϖ(M̂), −𝒬) < 0`, with `𝐇_S := Hess G_ϖ(Ŝ)`.
- Let `ε_0` and `ρ_3` be the smallest tolerance and radius that Lemma FL.3 gives for the three maps, and `ρ_c` the largest
  of their radii `ρ_3 sup|Dc|`.
- Decrease `ρ_3` until `2ρ_c ≤ r_ϖ`. Lemma FL.3 still holds with the same `ε_0`: its proof uses `H` only on
  `c(B̄_{ρ_3})`, and its margins improve as `ρ_3` decreases.
- Fix `ρ ∈ (0, ρ_3/2]` small enough for Step 3, and put `δ := δ(ρ)`.
- Choose `ε ≤ min(δ/2, ε_0, q_−ρ²/8)`, with `ε < 1`, so small that Step 1 applies. Choose a radius `R_η ≥ 2ρ_c` with
  `q_−R_η²/2 ≥ max_W G_ϖ − L_S + 3`.

Then `W × B̄_{R_η}` contains the balls `B(s, 2ρ_c)` of Lemma FL.3. Only `ρ_3`, `ε_0`, `ρ`, `δ`, `ε` and `R_η` depend on
`𝒬`, as the statement says. By (S2), `|𝔊(M̂_0)| ≤ ε` and `|𝔊(Ŝ_0) − L_S| ≤ ε`.

- **(R).** On `Γ × {0}`, `𝔊 ≥ L_S + 2δ − ε > L_S + ε ≥ 𝔊(Ŝ_0)`, and `𝔊(𝔭, 0) > 2δ − ε > 𝔊(M̂_0)`. By (Path),
  `d_f(M) ≥ b + s(L_S + 2δ − ε) > f(S)`. So `1{d_f(M) = f(S)} = 0`.
- **(D), (D′).**
  - *Path.* Take `Γ × {0}`. Off the crossing arc, `𝔊 ≥ L_S + 2δ − ε > 𝔊(Ŝ_0)`. On `σ_+([−ρ, ρ]) × {0}`, `𝔊 ≥ 𝔊(Ŝ_0)` by Lemma
    FL.3. At the end, `𝔊(𝔭, 0) > 𝔊(M̂_0)`. By (Path), `d_f(M) ≥ f(S)`.
  - *Trap.* Take `𝒟 := 𝒟_2 × B_{R_η}`. First, `𝔊 < 𝔊(M̂_0)` on `𝒟 ∖ {M̂_0}`:
    - off `B(M̂, ρ) × B_{R_η}`, `𝔊 ≤ −2δ + ε < −ε`;
    - on `B(M̂, ρ) × {|η| ≥ ρ}`, `𝔊 ≤ −q_−ρ²/2 + ε < −ε`;
    - on `B(M̂, ρ) × {|η| < ρ} ⊂ B(M̂_0, 2ρ)`, by Lemma FL.3 for the identity map (`2ρ ≤ ρ_3`).

    Second, `𝔊 ≤ 𝔊(Ŝ_0)` on `∂𝒟`:
    - on `𝒟̄_2 × ∂B_{R_η}`, `𝔊 ≤ max_W G_ϖ − q_−R_η²/2 + ε < L_S − 2`;
    - on `(∂𝒟_2 ∖ σ_−((−ρ, ρ))) × B̄_{R_η}`, `𝔊 ≤ L_S − 2δ + ε < 𝔊(Ŝ_0)`;
    - on `σ_−([−ρ, ρ]) × {|η| ≤ ρ}`, where `|(t, η)| ≤ 2ρ ≤ ρ_3`, `𝔊 ≤ 𝔊(Ŝ_0)` by Lemma FL.3;
    - on `σ_−([−ρ, ρ]) × {|η| ≥ ρ}`, `𝔊 ≤ L_S − q_−ρ²/2 + ε < 𝔊(Ŝ_0)`, because `G_ϖ∘σ_− ≤ L_S` near `0` (Lemma FL.3 with
      `H = H_0`).

    By (Trap) with `c′ := 𝔊(Ŝ_0)`, `d_f(M) ≤ f(S)`.

  So `d_f(M) = f(S)`, and `1{d_f(M) = f(S)} = 1`. ∎

*Remarks.*
1. As in #207, only window information is used: every conclusion is an explicit path inside `Ψ(W × B̄_{R_η})` or a trap whose
   closure lies inside it. So the landscape outside the window cannot change the decision.
2. The field ridge and valley are never needed. The certificates are the model's curves, and at `Ŝ` a crossing curve, which
   Lemma FL.3 makes robust using only `C²` closeness and the criticality of `Ŝ_0`.
3. `W`, `δ`, `ρ` and `ε` are not uniform in `ϖ`. Theorem FL needs only the pointwise statement, because it passes to the limit
   by dominated convergence at each fixed parameter.
4. The proof works verbatim for a continuous function on `R²` in place of `f`, with `Ψ = id` (Steps 2–4 only use
   invariance of domain). Applied to `G_{ϖ′}` (with `𝔮 = 0`), it shows: for every `ϖ ∈ 𝒦` there is a neighbourhood `U` of
   `ϖ` such that the actual decision `e(G_{ϖ′})` equals `e(G_ϖ)` for every typed `ϖ′ ∈ U`, generic or not. So
   `ϖ ↦ e(G_ϖ)` is continuous at every point of the full-measure set `𝒦`, hence Lebesgue measurable. The `(R)` part needs
   only `C⁰` closeness on `Γ`, and so holds without genericity.

## 3. The fold-scale limit

**Theorem FL.** Let `d ≥ 2`, `L > 0` and `u ∈ S^{d−1}`. For every `b ∈ R` and `k > 0`,

    lim_{r↓0} (k/r)·r^{−2}A_r^{rej}(b, k, u) = F(k; b, u),                                                          (3.1)

where `F` is #242 (3.1), and the limit there exists. `F` is continuous and positive, and the convergence is uniform for
`(b, k)` in compact subsets of `R × (0, ∞)`.

*Proof.* Fix `u` and a compact set `𝒞 ⊂ R × (0, ∞)` of `(b, k)`. Constants are uniform over `𝒞`; `P := 1 + |b| + k`.

*Step 1 (coupling and conditioning).* Use the coupling (R3) of [R]: on one probability space `(Ω, ℙ)` an unconditioned copy
`𝖥` of the field gives `F_r := 𝖥 + C_rΣ_r^{−1}(v_r − U_r)` with law `Q`, and `F_0 := 𝖥 + C_0Σ_0^{−1}(v_0 − U_0)` with the
contact law. By (R2) and Taylor's formula for the centred difference quotients `U_r` (e.g. `U_3 = ∂_u³𝖥(0) +
(r²/40)∂_u⁵𝖥(0) + ⋯`), pathwise,

    ‖F_r − F_0‖_{C⁵} ≤ r²T,    ‖F_0‖_{C⁵} ≤ T,    T := C(P + ‖𝖥‖_{C⁵}),                                          (3.2)

and `T` has all moments ([P] §2). Let `𝔸 := D_Θ²F_0(0)`. The pair `(F_r, 𝔸)` is jointly Gaussian, so

    F_r = μ_r + 𝔅_r(𝔸 − E𝔸) + g_r    (r ≥ 0),                                                                      (3.3)

with deterministic `μ_r := EF_r` and `𝔅_r := Cov(F_r, 𝔸)Cov(𝔸)^{−1}`, and `g_r` centred and independent of `𝔸`. From
(3.2), `‖μ_r − μ_0‖_{C⁵} + ‖𝔅_r − 𝔅_0‖_{C⁵} ≤ Cr²P`. For `a ∈ Sym(m)` put `F_r^a := μ_r + 𝔅_r(a − E𝔸) + g_r`.
- *Pins.* Every `F_r^a` has the pins. The pin functionals `ℓ_j` satisfy `ℓ_j(F_r) = v_{r,j}` on `Ω`, so `ℓ_j(F_r)` is
  deterministic. Hence `ℓ_j(𝔅_r) = Cov(ℓ_j(F_r), 𝔸)Cov(𝔸)^{−1} = 0`, `ℓ_j(μ_r) = v_{r,j}`, and `ℓ_j(g_r) = 0` identically.
- *Contact Hessian.* Similarly, since `D_Θ²F_0(0) = 𝔸`, `D_Θ²𝔅_0(0)` is the identity of `Sym(m)`, `D_Θ²μ_0(0) = E𝔸` and
  `D_Θ²g_0(0) = 0`. So `D_Θ²F_0^a(0) = a` exactly.
- *Representation.* By independence and Fubini, for Borel `Ξ ≥ 0`,
  `E_Q[Ξ(f)] = ∫_{Sym(m)}p_𝔸(a)E[Ξ(F_r^a)]da`.
- *Pathwise bounds.* `‖F_r^a − F_0^a‖_{C⁵} ≤ Cr²(T + P(1 + |a| + |𝔸|)) =: r²T_a`. Since `F_0^a = F_0 + 𝔅_0(a − 𝔸)`,
  also `‖F_r^a‖_{C⁵} ≤ C(T + P + |a| + |𝔸|)`.

*Step 2 (the exceptional set, and the zoom).* Let `M_3`, `M_4` be the third- and fourth-derivative suprema of [P] on the
local cylinder. By [P] (7.7), `(k/r)E_Q[(W_r/r⁴)1{rM_4 > 3k/10}] ≤ (k/r³)·Cr⁴ → 0`. Write the rest in Weyl coordinates on
`Sym(m)`: `a = −O diag(μ_1, …, μ_m)Oᵀ` with `μ_1 < ⋯ < μ_m`, `da = c_m𝒱(μ)dμ dO`, `𝒱(μ) := Π_{i<j}(μ_j − μ_i)`. Then put
`μ_1 = μ̃r/k`:

    (k/r)E_Q[(W_r/r⁴)(1 − e)1{rM_4 ≤ 3k/10}]
        = c_m∫ 1{μ̃r/k < μ_2 < ⋯ < μ_m} p_𝔸(a_r)𝒱(μ̃r/k, μ_2, …, μ_m) h_r(μ̃, μ_2, …, μ_m, O) dμ̃ dμ_2⋯dμ_m dO,       (3.4)

where `a_r := −O diag(μ̃r/k, μ_2, …, μ_m)Oᵀ`, `h_r := E[Ξ_r(F_r^{a_r})]` and
`Ξ_r(f) := (W_r(f)/r⁴)(1 − e(f))1{rM_4(f) ≤ 3k/10}`. (For `m = 1` there is no `O` and no `μ_2, …`.)

*Step 3 (pointwise limits).* If `μ_2 < 0`, the indicator `1{μ̃r/k < μ_2}` in (3.4) vanishes for small `r`. So fix `μ̃ ≠ 0`,
`0 < μ_2 < ⋯ < μ_m` and `O`. Put `a* := −O diag(0, μ_2, …, μ_m)Oᵀ`, `f_r := F_r^{a_r}` and `f* := F_0^{a*}`. As `r → 0`,
pathwise:
- (i) `‖f_r − f*‖_{C⁵} ≤ r²T_{a_r} + C|μ̃|r/k → 0`.
- (ii) `D_Θ²f_r(0) = a_r + O(r²T_{a_r})`, and `μ̃r/k` is the smallest eigenvalue of `−a_r` for small `r`. Hence
  `λ̃(f_r) = μ̃ + O(rT_{a_r}) → μ̃`, the other eigenvalues tend to `μ_2, …, μ_m`, and `e_1(f_r) → Oε_1` up to sign (spectral
  gap `μ_2 > 0`).
- (iii) `(γ, B, C_3)(f_r) → (γ*, B*, C_3*)`, the jets of `f*` at `0` along `Oε_1`. Also `Y(f_r) → Y* := 3kB* − γ*²/4`.
- (iv) By Lemma FL.1, `‖𝔉_r − G_k^{(d)}[f_r]‖_{C²(𝒲_w)} ≤ C‖f_r‖_{C⁵}ϑ(r) → 0`. And `G_k^{(d)}[f_r] → G_k^{(d)}[*]`, the model
  built from `(μ̃, γ*, B*, C_3*)` and `μ_2, …, μ_m`. Here `𝔉_r` is the window (0.4) of `f_r` in its own eigenframe.

Consequences:
- *The `M_4` indicator* tends to `1`, since `rM_4(f_r) ≤ Cr‖f_r‖_{C⁴}`.
- *Types and weight.* Since `f_r∘Φ_r = b + kr³𝔉_r` with `Φ_r` affine, the Hessians of `f_r` at `M`, `S` are congruent to
  those of `𝔉_r` at `M̂_0`, `Ŝ_0` up to a positive factor. Computing the determinant of `Φ_r`'s linear part,

      W_r(f_r)/r⁴ = k^{2(m−1)}|det Hess 𝔉_r(M̂_0)·det Hess 𝔉_r(Ŝ_0)|·1{typed}    (exactly).                            (3.5)

  The limit Hessians are block diagonal. At `M̂_0` the planar block is `[[−6, −γ*/2], [−γ*/2, −μ̃ − kB*/2]]`, with
  determinant `6μ̃ + Y*`. At `Ŝ_0` it is `[[6, γ*/2], [γ*/2, −μ̃ + kB*/2]]`, with determinant `−6μ̃ + Y*`. The stiff block is
  `−diag(μ_2, …, μ_m)/k`.

  So off the null set `{6μ̃ = ±Y*}` the inertia converges. The limit is typed iff `μ_2 > 0` and `|Y*| < 6μ̃`, which forces
  `μ̃ > 0`. And `W_r(f_r)/r⁴ → (μ_2⋯μ_m)²(36μ̃² − Y*²)1{μ_2 > 0, |Y*| < 6μ̃}`.
- *Decision.* Suppose `μ_2 > 0`, `μ̃ > 0`, `γ* ≠ 0` and `ϖ* := ϖ(μ̃, γ*, B*, C_3*) ∈ 𝒦`. Apply Proposition FL.4 with
  `(ϖ, 𝒬) := (ϖ*, 𝒬*)`, `𝒬* := (μ̃/(kγ*²))diag(μ_2, …, μ_m)`, to the normalized window `𝔊_r` of `f_r`:
  - (S1) holds exactly;
  - (S2) holds for small `r`, by (1.3), (iv), `ϖ(f_r) → ϖ*` and `𝒬(f_r) → 𝒬*`;
  - `Ψ_r(X, z, η) := Φ_r(X, (γ(f_r)/λ̃(f_r))z, η)` is affine and injective on the bounded window for small `r`, and
    `f_r∘Ψ_r = b + s_r𝔊_r` with `s_r := kr³γ(f_r)²/λ̃(f_r) > 0`.

  So `e(f_r) = e(G_{ϖ*})` for small `r`.
- *Full measure.* For fixed `μ̃ > 0`, `μ_2, …, μ_m > 0` and `O`, the vector `(γ*, B*, C_3*)` is Gaussian, being affine in
  `g_0`. Its covariance is nondegenerate: these are three distinct third-order functionals, and the conditional covariance
  given the contact pins and `𝔸` is positive definite by [P] §2. The map `(γ, B, C_3) ↦ ϖ = (γ²/(24μ̃), kB/μ̃, k²C_3γ/μ̃²)` is
  a local diffeomorphism on `{γ ≠ 0}`, with Jacobian determinant `k³γ²/(12μ̃⁴)`. So `ϖ*` has an absolutely continuous law,
  and by Lemma FL.2, `ℙ(ϖ* ∈ 𝒯 ∖ 𝒦) = ℙ(γ* = 0) = ℙ(|Y*| = 6μ̃) = 0`.

Hence, almost surely, `Ξ_r(f_r) → Ξ* := (μ_2⋯μ_m)²(36μ̃² − Y*²)1{μ_2 > 0, |Y*| < 6μ̃}(1 − e(G_{ϖ*}))`. The weight bound
(3.6) below gives `sup_r E[Ξ_r(f_r)²] < ∞`, so `h_r → h := E[Ξ*]` (Vitali). Also `p_𝔸(a_r) → p_𝔸(a*)`,
`𝒱(μ̃r/k, μ_2, …) → 𝒱(0, μ_2, …)`, and `1{μ̃r/k < μ_2} → 1{μ_2 > 0}`.

*Step 4 (domination).* Let `U_a := 1 + ‖F_r^a‖_{C⁵} ≤ C(T + P + |a| + |𝔸|)`. Then `M_3, M_4 ≤ CU_a`, and
`‖A_M − a‖ ≤ (r/2)M_3 + ‖D_Θ²(F_r^a − F_0^a)(0)‖ ≤ CrU_a + r²T_a`, where `A_M := D_Θ²F_r^a(M)`.
- *Weight.* On the typed support, `A_M < 0`. By [P] (6.2) and Weyl's inequality (`λ_j(−A_M) ≤ |μ_j| + ‖A_M − a‖`), with
  `h = M_3`,

      W_r/r⁴ ≤ (h²/4)(λ_1/r)(λ_1/r + 3h/2)Π_{j≥2}λ_j(λ_j + rh) ≤ CU′²(|μ̃| + U′)²Π_{j≥2}(|μ_j| + U′)²,                 (3.6)

  where `U′ := U_a + rT_a`.
- *Soft layer.* The deterministic cap theorem ([CAP] §§1 and 5, as used in [P] §7) shows that every `C⁴` field with the
  pins has `d_f(M) = f(S)`, i.e. `e = 1`, on the cap region `{λ_min(−A_M) > (4/(3k))rM_3², rM_4 ≤ 3k/10}`. It uses no Morse
  or genericity hypothesis, because our mark is the maximin itself. So on `{typed, e = 0, rM_4 ≤ 3k/10}`,
  `λ_min(−A_M) ≤ (4/(3k))rM_3²`. Hence `μ̃r/k = λ_1(−a) ≤ CrU′²`. On the typed support, `λ_min(−A_M) > 0`, so `μ̃ ≥ −CU′`.
  Thus the support of `Ξ_r(f_r)` lies in `{−CU′ ≤ μ̃ ≤ CU′²}`.
- *Removing `μ̃` from `U′`.* We have `|a_r| ≤ |μ̃|r/k + Σ_{j≥2}|μ_j|`.
  - `m ≥ 2`: on the domain of (3.4), `μ̃r/k < μ_2`. If `μ̃ ≥ 0`, then `|μ̃|r/k < |μ_2|`. If `μ̃ < 0`, the support bound
    gives `|μ̃| ≤ C(P + Σ|μ_j| + T + |𝔸| + |μ̃|r/k)`, so `|μ̃| ≤ 2C(P + Σ|μ_j| + T + |𝔸|)` once `Cr/k ≤ ½`. Either way, on
    the support, `U′ ≤ Ū := C(P + Σ_{j≥2}|μ_j| + T + |𝔸|)`.
    With `1{|μ̃| ≤ CŪ²} ≤ (1 + CŪ²)^q(1 + |μ̃|)^{−q}`, `p_𝔸(a_r) ≤ C_0e^{−c_0Σ_{j≥2}μ_j²}` and
    `𝒱 ≤ C(1 + |μ̃| + Σ|μ_j|)^{m(m−1)/2}`, the integrand of (3.4) is at most
    `C_q(1 + |μ̃|)^{m(m−1)/2+2−q}(1 + Σ_{j≥2}|μ_j|)^{c_q}e^{−c_0Σ_{j≥2}μ_j²}`. With `q := m(m−1)/2 + 4` this is
    integrable and independent of `r`.
  - `m = 1`: `|a_r| = |μ̃|r/k`. For `μ̃ < 0` the support bound gives `|μ̃| ≤ 2CV`, `V := P + T + |𝔸|`, as for `m ≥ 2`. For
    `μ̃ ≥ 0` it gives `μ̃ ≤ C(V + μ̃r/k)²`. So either `μ̃ ≤ C′V²` (*near branch*), which is dominated as for `m ≥ 2`, or
    `μ̃ ≥ k²/(C′r²)` (*far branch*). On the far
    branch, `p_𝔸(−μ̃r/k) ≤ C_0e^{−c_0μ̃²r²/k²}` and (3.6) is polynomial in `μ̃` and `r^{−1}`. So the far branch contributes
    `O(r^{−c}e^{−c′/r²}) → 0`, uniformly.

*Step 5 (conclusion).* By dominated convergence in (3.4), and since `12π_r(v_r) → 12π_0(u; v_0(b, k))` ([R] (R5)),

    (k/r)r^{−2}A_r^{rej} → 12π_0(u; v_0(b,k)) c_m∫_{0<μ_2<⋯<μ_m}∫_O p_𝔸(a*)𝒱(0, μ_2, …) ∫_0^∞ h dμ̃ dμ_2⋯dO.           (3.7)

By #242 §2, the change of variables `μ̃ = γ*²/(24φ)` turns `36μ̃² − Y*²` into `(γ*⁴/16)(φ^{−2} − (1 − t*)²)` and `dμ̃` into
`(γ*²/(24φ²))dφ`. So by Fubini, `∫_0^∞h dμ̃ = (μ_2⋯μ_m)²E[(γ*⁶/384)I(t*, χ_0*)]`, with `t*`, `χ_0*` as in (0.3) and `I` as
in #242 (2.5).

It remains to identify (3.7) with #242 (3.1). By Weyl's formula, with `0 < λ_1 < ⋯ < λ_m` the eigenvalues of `−a`,

    ε^{−1}E_{v_0}[Υ1{𝔸 < 0, λ_1 < ε}]
        = c_m∫_{0<λ_2<⋯<λ_m}∫_O ε^{−1}∫_0^{min(ε, λ_2)} p_𝔸(a)𝒱(λ)E[Υ(F_0^a)] dλ_1 dλ_2⋯dλ_m dO,

where `Υ := (γ_1⁶/384)(λ_2⋯λ_m)²I(t, χ_0)`. For `m = 1` the upper limit is `ε` and there are no hard eigenvalues. The
ordering `λ_1 < λ_2` must be kept (OA-243-D-01). Write the inner average as `∫_0^1 1{εs < λ_2}(⋯)|_{λ_1 = εs} ds`. For
every fixed ordered hard spectrum the indicator tends to `1`, and the bounds below dominate in `s`, the hard spectrum and
`O`. The inner average tends to its value at `λ_1 = 0`, for three reasons:
- by #242 Lemma 3, `γ⁶I ≤ C(γ⁶ + k³|B|³ + k⁴C_3²)`, which is integrable with Gaussian weights;
- `I` is continuous at almost every `(t, χ_0)`. By Remark 4 of §2, the actual decision is constant near each point of `𝒦`;
  for almost every `(t, χ_0)` the set `{φ : (φ, 2tφ, χ_0φ²) ∉ 𝒦}` is null, so `1{φ ∈ 𝓡(t′, χ_0′)} → 1{φ ∈ 𝓡(t, χ_0)}` for
  almost every `φ` as `(t′, χ_0′) → (t, χ_0)`. Lemma 3 bounds `φ` away from `0` on the rejected set, locally uniformly,
  which gives domination in `φ`;
- the jets of `F_0^a` along `e_1(a)` depend continuously on `a` and have a nondegenerate Gaussian law.

So the limit in #242 (3.1) exists, and (3.7) equals `F(k; b, u)`.

*Uniformity and continuity.* The proof applies verbatim along any sequence `(r_n, b_n, k_n) → (0, b, k)` in `(0, 1] × 𝒞`.
The contact law depends on `(b, k)` only through an affine shift of the mean ([P] (3.3)), so `p_𝔸` and the jets move
continuously. All bounds above are uniform on `𝒞`. A diagonal argument then gives both the continuity of `F` on `𝒞` and the
uniform convergence. Positivity is proved in Corollary FL.5. (Uniformity in `u` would need `u_n → u` in this argument as
well; it is not claimed.) ∎

## 4. The identification with #170/#175, the selection loss, and the compact-window density difference

**Proposition FL.7 (the model of #170 and #175).** For the jets `(λ̃, γ, B, C_3)` of (0.2), put
`θ := (s, a, β′, c) := (−λ̃/k, γ, B, C_3)`. In `d = 2` these are #170's coordinates `(f_zz(0)/r, f_xxz(0), f_xzz(0), f_zzz(0))`
(§8.1 there); in `d ≥ 3` they are #175's soft coordinates (`μ_1 = −rs`, §2 there). Let

    P_θ(X, Z) := 2kX³ − 3kX/2 − k/2 + sZ²/2 + (a/2)(X² − ¼)Z + (β′/2)XZ² + (c/6)Z³,    B′ := β′ − a²/(12k),        (4.0)

be #170's typed cubic. Let `n(θ)` be its number of additional critical points with values in `(−k, 0)`, that is, the
number of points of `C(P_θ)` (#170 §2; the classifier of #170 §§7 and 8.1, with `n ∈ {0, 1, 2}` by #175 §2). Then:
- (i) `G_k(X, ζ) = P_θ(X, kζ)/k` identically.
- (ii) `Y = 3kB′`. So the typed domains agree (`s < −|B′|/2` iff `|Y| < 6λ̃`), and so do the limiting weights:
  `9k²(4s² − B′²) = 36λ̃² − Y²`.
- (iii) For typed `θ` with `γ ≠ 0`, off #170's null sets `Σ_k ∪ Δ_k`, `1 − e(G_ϖ) = 1{n(θ) > 0}`.
- (iv) `F(k; b, u) = kA_∗(b, k, u)·a_fail(b, k, u)` and `d_{𝐁,𝐊} = C_fail^{𝐁,𝐊}`.
  - In `d = 2`, `a_fail = α₁ + α₂` is #170's (S2), and `C_fail` is #170 §9. This case is an identity of model integrals.
  - In `d ≥ 3`, `a_fail = a1 + a2` is #175's (S2)–(S3), and `C_fail` is #175 §7 (L1). This case uses uniqueness of limits
    and is conditional on #175 Theorem F.

*Proof.*
- (i) This is a polynomial identity (control F7). `2(X + ½)²(X − 1) = 2X³ − 3X/2 − ½`, and the terms of #242 (2.1) in `ζ`,
  `ζ²` and `ζ³` are `(γ/2)(X² − ¼)ζ`, `−(λ̃/2)ζ² + (kB/2)Xζ²` and `(k²C_3/6)ζ³`. These are the terms of `P_θ(X, kζ)/k`.
- (ii) `Y = 3kB − γ²/4 = 3kB′`, and `λ̃ = −ks`.
- (iii) By (i) and (0.4), `G_ϖ(X, z) = (λ̃/(kγ²))P_θ(X, k(γ/λ̃)z)`. This is an invertible linear change of variables
  fixing `M̂ = M` and `Ŝ = S`, followed by a positive factor; it preserves maximin levels up to that factor, and it maps
  `L_S` to `−k`. By #170 Theorem E(1), the maximin level of `P_θ` is `h_*(θ) = max({−k} ∪ P_θ(C(P_θ))) ≥ −k`. So
  `e(G_ϖ) = 1` iff `h_*(θ) = −k` iff `n(θ) = 0`.
- (iv) In `d = 2`, Step 5 of Theorem FL and Fubini give
  `F = 12π_0(u; v_0)∫_0^∞dμ̃∫(36μ̃² − Y²)1{|Y| < 6μ̃}(1 − e(G_ϖ))h_0(0, γ, B, C_3)dγ dB dC_3`. Here `h_0` is the joint
  density of `(𝔸, γ, B, C_3)` under the contact law, with `e_1` the transverse unit vector of #170's frame. Flipping `e_1`
  changes neither `ϖ` nor `w_+` nor `n`. Put `μ̃ = −ks`, so that `dμ̃/ds = −k` and `∫_0^∞dμ̃ = k∫_{−∞}^0 ds`, and use
  (ii)–(iii). This becomes `k·12π_0∫w_+(θ)h_0(0, a, β′, c)1{n(θ) > 0}dθ`, which is `k·A_∗·a_fail` by #170 (S1)–(S2), (S11)
  and `A_∗ = 12π_0z_0`.
  - *Every `d ≥ 2`.* Uniqueness of limits gives the same identity. `(k/r)r^{−2}A_r^{rej} = kA_r·r^{−3}(1 − p_r)` tends to `F`
    by Theorem FL, and to `kA_∗a_fail` by #170 Theorem S or #175 Theorem F.
  - *In `d ≥ 3` the integrands also agree, up to the normalization `c_m dO` of the Weyl formula.*
    `𝒱(0, μ_2, …, μ_m)(μ_2⋯μ_m)² = Π_{j≥2}μ_j³Π_{2≤i<j}(μ_j − μ_i)` is #175's hard factor, and both decisions are the planar
    one (#175 Theorem H; Proposition FL.4 here).
  - *OpenAI Codex's cross-check.* Codex's antecedent cross-check (comment 5951210964 on #243) argues the `d ≥ 3` identity
    directly. It matches #175 (S1)'s `c_m`, Haar variable and hard Vandermonde with (3.4) and (3.7), and finds no orientation
    or factor-of-two discrepancy. This is root-authored support and is not reviewed here.
  - *The last claim.* Integrating `(1/3)k^{−8/3}F = A_∗a_fail/(3k^{5/3})` gives `d_{𝐁,𝐊} = C_fail^{𝐁,𝐊}`. ∎

*Remark (D.1: a direct identity in every `d`).* OpenAI Codex's supplement D.1 is §3 of its review 5391986303 on #242. It
is bound to #242 v1.2's PROOF, whose §§0–3 are unchanged in v1.3.
- D.1 proves `F = kA_∗a_fail` directly, as an identity of model integrals in every fixed `d`, under its stated
  contact-density and deterministic-classifier interfaces (#170, #175 and [SC]). It uses neither Theorem FL nor #175
  Theorem F.
- A different Codex agent reviewed it (5954510413, on this PR): PASS_TECHNICAL_SCOPED, with no finding. The review notes
  that an author may adopt the identity in FL.7 while keeping every hypothesis needed for an actual-field conclusion.
- With D.1, (iv) holds in `d ≥ 3` without #175 Theorem F. This note records D.1 as reviewed support and does not reproduce
  it. D.1, its review and this note are on the same account (organizational independence 0).

**A second proof of (0.0) in `d = 2`.** At each fixed `(b, k, u)`, conditional on #170's interfaces, (0.0) follows without
the field analysis of §§1–3. The ingredients are:
- #170 Theorem S;
- `A_r → A_∗` ([P] (10.3));
- parts (i)–(iii) above, and the computation in (iv);
- the existence of the limit in #242 (3.1).

That last limit is a model-level fact. In `d = 2` the jets `(γ, B, C_3)` do not depend on an eigenvector, so it follows from
dominated convergence with #242 Lemma 3's bound; Step 5 of Theorem FL proves it in every `d`.

Theorem FL is then a second proof with a partly different route, and it also gives continuity and local uniformity. In
`d ≥ 3` the direct computation would also need the Weyl normalization of #175 §2 matched with (3.4). This note does not do it;
Codex's cross-check 5951210964 argues it, and D.1 (the Remark above) proves it.

**Corollary FL.5 (the constant in `1 − p_r ~ r³`; #170 Theorem S, #175 Theorem F).** For fixed `u ∈ S^{d−1}`, uniformly
for `(b, k)` in compact subsets of `R × (0, ∞)`,

    r^{−3}(1 − p_r(b, k, u)) → F(k; b, u)/(k·A_∗(b, k, u)) ∈ (0, ∞)    (r → 0).                                        (4.1)

*Proof.* By (0.1), `r^{−3}(1 − p_r) = r^{−3}A_r^{rej}/A_r = k^{−1}[(k/r)r^{−2}A_r^{rej}]/A_r`. Theorem FL and
`A_r → A_∗ > 0` uniformly ([P] (10.3)) give (4.1).

*Positivity of `F`.* At `ϖ = (φ, 0, 0)` the slices are concave (`a = 1`, `χ = 0`), `R(X) = A₀ + p²/8`, and exactly
(control F6)

    R(X) − L_S = (X − ½)²[2(X + 1) + 3φ(X + ½)²]/(24φ).                                                              (4.2)

The bracket is a quadratic in `X` with discriminant `4 − 12φ`, so for `φ > 1/3` it is positive: `R > L_S` for all `X ≠ ½`,
and `R ~ X⁴/8 → +∞` as `X → −∞`. So `I_M ⊃ (−∞, ½)` and `M` dies above `L_S`, along the ridge into `X → −∞`. By Remark 4 of §2
this `(R)` certificate persists, with only `C⁰` closeness on a compact path, for every `ϖ′` near `(φ, 0, 0)`; by compactness,
uniformly for `φ ∈ [1/3 + δ_5, 1 − δ_5]`. So `𝓡(t, χ_0) ⊃ [1/3 + δ_5, 1 − δ_5]` for `|t| + |χ_0| ≤ θ`, and there
`I(t, χ_0) ≥ ∫_{1/3+δ_5}^{1−δ_5}φ^{−2}(φ^{−2} − (1 − t)²)dφ > 0` (for `θ` small). Given `𝔸 = a*`, the event
`{|t*| + |χ_0*| ≤ θ, γ* ≠ 0}` has positive probability, since the jets are nondegenerate Gaussian. Also `p_𝔸 > 0`,
`π_0 > 0` and `𝒱 > 0` almost everywhere. Hence `F > 0`. ∎

[P]'s Theorem A gives `1 − p_r ≤ Cr³`, and the OA dimension lift (A3) gives `1 − p_r ≥ cr³`, both uniformly. The constant
was first identified by #170 Theorem S (`d = 2`) and #175 Theorem F (`d ≥ 3`) as `α₁ + α₂`. (4.1) recovers it in #242's form,
and the two forms agree by Proposition FL.7. The positivity argument above is independent of theirs.

**Corollary FL.6 (the compact-window density difference; #170 §9, #175 §7).** Let `𝐁` (births) and
`𝐊 = [k_−, k_+] ⊂ (0, ∞)` (gap marks) be compact intervals of positive length, and let `ν_cand`, `ν_eld` be the compact-window
densities of [P]'s Theorem B. Then

    ν_cand(ℓ) − ν_eld(ℓ) = d_{𝐁,𝐊}ℓ^{2/3} + o(ℓ^{2/3}),    d_{𝐁,𝐊} := (1/3)∫_{S^{d−1}}∫_𝐁∫_𝐊 k^{−8/3}F(k; b, u)dk db dσ(u) ∈ (0, ∞).   (4.3)

Consequently `E[N_cand(0, t] − N_eld(0, t]] = (3/5)d_{𝐁,𝐊}t^{5/3} + o(t^{5/3})`. And for every real `q > −5/3`,
`E Σ_{candidate, not selected, ℓ ≤ t}ℓ^q = d_{𝐁,𝐊}t^{q+5/3}/(q + 5/3) + o(t^{q+5/3})`. #170 §9 and #175 §7 already sharpen
[P] (1.2) and (12.1) from upper bounds to asymptotic laws, with `C_fail^{𝐁,𝐊} = d_{𝐁,𝐊}` (Proposition FL.7). The `q`-moment
form is the same integration.

*Proof.* By [P] (11.1)–(11.2), at `r = (ℓ/k)^{1/3}`,
`ν_cand(ℓ) − ν_eld(ℓ) = ℓ^{−1/3}∫A_r(1 − p_r)/(3k^{2/3}) db dk dσ = ℓ^{−1/3}∫A_r^{rej}/(3k^{2/3})`. Since `r³ = ℓ/k`,
`A_r^{rej} = (ℓ/k²)·[(k/r)r^{−2}A_r^{rej}]`, so

    ℓ^{−2/3}(ν_cand(ℓ) − ν_eld(ℓ)) = (1/3)∫_{S^{d−1}×𝐁×𝐊} k^{−8/3}[(k/r)r^{−2}A_r^{rej}(b, k, u)] dk db dσ.            (4.4)

By [C7-K] (K2) (`r ≤ k_−`), `(k/r)r^{−2}A_r^{rej} ≤ 12π_r(v_r)CP^N` is bounded on the compact window. Theorem FL and
dominated convergence give (4.3), and `d_{𝐁,𝐊} > 0` by the positivity of `F`. The cumulative and moment statements follow
by integrating (4.3) against `ℓ^q dℓ` on `(0, t]`, as in [P] §12. ∎

*Remarks.*
1. #242 Proposition 4 computes `F = F_0(b)H(k)` for the Gaussian kernel `e^{−|x|²/2}` on `R^d`, the model case, not for the
   torus field of Theorem FL. For that model the formula reads `d_{𝐁,𝐊} = (1/3)|S^{d−1}|∫_𝐁F_0 db·∫_𝐊 k^{−8/3}H(k)dk`; for the
   periodized torus field the jets' laws differ by `O(e^{−L²/8})` (#242 §0).
2. Without the lower cutoff `k_−`, the integral in (4.3) diverges at `k → 0` whenever `F` stays bounded below there, as for
   the Gaussian kernel, where `F(k) → F_0 > 0` (#242 Proposition 4). Cutting it at the cusp scale `k ≍ ℓ^{1/4}` produces
   `ℓ^{2/3}·ℓ^{−5/12} = ℓ^{1/4}`, the order of #229's term `(I^{cand} − c_1)ℓ^{1/4}`. This is why the unrestricted `ℓ^{2/3}`
   coefficient (#242 Conjecture 7) needs the two-scale composite and the intermediate separations, while the compact-window
   coefficient (4.3) does not.

## 5. Numerical evidence (exploration; not part of the proofs)

The scripts and records are in the project archive (`exploration/`; numpy and scipy, outside the repository).

**Decision and weight convergence on exactly pinned fields** (`fold_d2.py`, `fold_d3.py`).
- *Setup.* Gaussian kernel `e^{−|x|²/2}`, `b = 0`, `k = 0.4`. Jets of order `≤ 6` at `0` are drawn from the contact law with
  `𝔸 = 0` (`d = 2`) or `𝔸 = −diag(0, μ_2)`, `μ_2 ~ U(0.5, 3)` (`d = 3`), and `γ` from the `γ⁶`-tilted law.
- *Fields.* For each sample, and each `φ` on a logarithmic grid over the typed range (40 points in `d = 2`, 24 in `d = 3`),
  take the exactly pinned degree-6 polynomial at separation `r` with `∂_{e_1}²f(0) = −μ̃r/k`, `μ̃ = γ²/(24φ)`.
- *Decisions.* Its normalized window (0.4) is flood-filled at the levels `L_S ± 2·10⁻³|L_S|`, on a 601² grid (`d = 2`) or a
  181² × 41 grid (`d = 3`). The model `G_ϖ` (`G_ϖ − 𝔮` in `d = 3`) is flood-filled on the same grid.
- *Weights and integrals.* `W_r/r⁴` comes from the exact Hessians. Per sample, the integral
  `I_r := (384/γ⁶)∫(W_r/r⁴)(1 − e_r)dμ̃` is compared with the model integral (including the factor `μ_2²` in `d = 3`).

| `d` | samples | `r` | mean `I_r` / mean model integral (same grid) | decision mismatches |
|---|---|---|---|---|
| 2 | 400 | 0.1 | 0.918 ± 0.054 | 378 / 15,171 (2.5%) |
| 2 | 400 | 0.03 | 0.998 ± 0.005 | 110 / 15,215 (0.72%) |
| 2 | 400 | 0.01 | 1.0015 ± 0.0026 | 35 / 15,223 (0.23%) |
| 2 | 400 | 0.003 | 0.9999 ± 0.0023 | 10 / 15,230 (0.066%) |
| 3 | 120 | 0.1 | 1.20 ± 0.14 | 80 / 2,696 (3.0%) |
| 3 | 120 | 0.01 | 0.9927 ± 0.0037 | 5 / 2,733 (0.18%) |
| 3 | 120 | 0.001 | 0.99938 ± 0.00031 | 0 / 2,737 |

- *Mismatch rates.* In `d = 2` the mismatch rate falls in proportion to `r`, the rate of Lemma FL.1.
- *Weights.* The median relative weight error `|W_r/r⁴ ÷ lim − 1|` in `d = 3` is `1.8·10⁻²`, `1.1·10⁻³` and `1.1·10⁻⁴`
  at `r = 0.1, 0.01, 0.001`. That is rate `r`, not `r^{1/2}`: the `r^{1/2}`-terms of #242 (2.6) are linear in `η`, so they
  move the pin Hessians' determinants only at order `r`.
- *Why the same grid.* The comparison is made on the same grid because the grid decision itself differs from the
  one-dimensional implementation of #242 Lemma 2 (`dec1d`, a fixed-tolerance numerical scan) at 37 of 15,232 points in
  `d = 2` and 26 of 2,737 in `d = 3`. Against `dec1d` the ratios settle at `0.992` (`d = 2`) and `0.967` (`d = 3`), which are
  the grid model's own offsets.

**Lemma FL.2(c).** The first half (`d(M̂) ≥ L_S`) is the one-line axial-path argument. The case statement was also tested.
- *Author.* On 1,500 typed points from #242's validation law (500 elder, 1,000 rejected), a two-dimensional flood fill shows
  `M` dead at `L_S + 2·10⁻³|L_S|` for 998 rejected points. Of the other two:
  - one is near-degenerate: `V` exceeds `L_S` by `10⁻⁴` near `X = 0.39`, and the point dies above `L_S` at a finer offset;
  - the other has `|χ| < 10⁻²`, and its far valley lies outside the box.
- *Referee (same family, independent scripts).* 14,040 typed points were tested in seven families: broad, Gaussian jets,
  `β > 2`, `|β − 2| ∈ [10⁻⁶, 10⁻¹]`, `|χ| ∈ [10⁻⁷, 10⁻³]`, near the typed edge, and near the elder edge. The death level was
  computed by bisection on the exact slice structure. No point had `d(M̂) < L_S`, and no elder point had `β > 2`, `χ < 0`.
  The bisection agreed with a two-dimensional flood fill on 800 cross-check points, after one grid artifact was resolved.

**Lemma FL.1 and Proposition FL.4 beyond polynomials (referee, independent).**
- *Lemma FL.1.* The fields were exactly pinned non-polynomial fields (trigonometric base plus polynomial correction),
  evaluated in 60-digit arithmetic. The `C²` error of the window falls by `100.0` per factor `100` in `r` in `d = 2`, and by
  `10.1` in `d = 3`. It is identical for `λ̃ ∈ {3/2, 100, −5, 1/100}` and for the stiff eigenvalues tested.
- *Proposition FL.4.* The perturbations were non-polynomial and `C²`-small (sums of sines, corrected to keep `M̂` and `Ŝ`
  critical). They were applied to five model points in `d = 2`, and to three in `d = 3` with a stiff direction coupled to the
  plane. The decision persisted up to the largest amplitude tested (`10⁻²` in `d = 2`, `3·10⁻³` in `d = 3`), with one
  exception: #242's near-degenerate (D′) point flips at amplitudes `≥ 3·10⁻³`. This is consistent with `ε` depending on the
  margins.

**Proposition FL.7(iii) (v1.1 referee, independent).** The comparison was made on 1,800 typed points: 1,500 broad, and 300
in the (D′) family, 141 of them elder. The parameters were `k ∈ [0.1, 5]` and `λ̃ ∈ [0.1, 10]`, with both signs of `γ`.
- *Method.* #170's classifier (the critical points of `P_θ` with values in `(−k, 0)`, found from a resultant) was compared
  with an independent one-dimensional implementation of #242 Lemma 2 on `G_ϖ`.
- *Result.* There were no disagreements once the scanner's grid was refined near `X = ½`, where `I_M`'s right end can lie
  very close to `½`. All 243 points with `β > 2`, `χ < 0` have `n > 0`.
- *The identity (iv).* `(γ⁶/384)I(t, χ_0) = k∫w_+1{n > 0}ds` was checked on four jet triples, to relative error
  `≤ 1.2·10⁻⁶`.

## 6. Scope and relation to other packets

- **#242.** Conjecture 6 is Theorem FL. The definition (3.1) of `F` is the actual fold-scale limit of the rejected kernel in
  every dimension. For the Gaussian kernel on `R^d` (#242's model case), #242 Proposition 4 describes `F` as `F = F_0H`, with
  `H(k) = 1 + (12/25)k² + O(k³)`. #170/#175 define `a_fail` for the torus field only. In `d = 2`, Proposition FL.7(iv) is an
  identity of model integrals, so `F_0H/k` is the integral `A_∗a_fail` evaluated with the `R^d` kernel's jets. The jets of the
  periodized torus field differ from these by `O(e^{−L²/8})`.
  Proposition 2′ of #242 (the stiff directions) is transferred to the field here, as part of Proposition FL.4.
- **#170 and #175 (merged author-side candidates, at their stated conditional scope).** Their Theorems S and F prove the
  failure law `r^{−3}(1 − p_r) → a_fail` at fixed marks.
  - *Their route.* #170's Theorem E decides the window cubic by critical chords and isolating caps, with [CUB]'s classifier,
    and transfers it to the global field. #175's Theorem H adds, for `d ≥ 3`, a hard-fibre barrier of width `r^{3/2}`.
  - *Their domination* is the parent's cap implication on `{λ_1 > (4/(3k))rM_3², rM_4 ≤ 3k/10}`, with [P] (6.2) and (7.7).
  - *Their compact-window coefficient* is in their §§9 and 7.
  - *Theorem FL's route.* It reaches the same limit through a different decision and convergence step: conditioning on the
    contact Hessian with a Weyl zoom, #242's slice decision, and the path/trap stability of Proposition FL.4. It does not
    consume [CUB], [TWO], [SC], [LOCAL] or the hard-fibre lemma.
  - *Shared steps.* Theorem FL's domination step uses the same cap-region mechanism and the same `m = 1` near/far split
    (#170 §8.3). The stiff scale `r^{3/2}` of Proposition FL.4 is #175's hard tube.
  - *Proposition FL.7* shows that the two limits are the same Gaussian integral in `d = 2`. In `d ≥ 3` they are equal by
    uniqueness of limits, and directly by Codex's reviewed D.1 (Remark after FL.7).
- **#242 Conjecture 7** is not proved. It needs inputs (i)–(ii) of #242 §4. Input (i) asks for (3.1) with an error that,
  integrated against `dr` from the cusp scale to the fold scale, is `O(ℓ^{3/4})` after the composite is subtracted. That
  needs quantitative margins in Proposition FL.4 near the decision boundary, which the present pointwise argument does not
  give. Input (ii) (the intermediate separations) is untouched.
- **[P], the dimension lift, and [C7-K].** Corollaries FL.5 and FL.6 restate, in #242's form, the constants of the `Θ(r³)`
  selection loss and of the `Θ(ℓ^{2/3})` compact-window density difference, which #170/#175 identified first. Their orders
  were known from [P] Theorems A and B, the OA lower bound (A3), and [C7-K] (K2).
- **Matching.** #242 Theorem 1 gives `κ𝒜^{rej} → F_0` as `κ → ∞` at the cusp scale, and Theorem FL gives the fold-scale
  limit `F(k)`. That `F(k) → F_0` as `k → 0` is proved in #242 only for the Gaussian kernel on `R^d` (Proposition 4,
  `H → 1`). It is what the composite of #242 Lemma 5 assumes. Neither limit is uniform in the overlap, and that is not
  claimed here.
- **Not claimed:** any rate in (3.1); uniformity as `k → 0` or `k → ∞`; any statement about `ν_cand`'s own corrections.

## 7. Controls

`fold_check.py` (standard library, exact rationals; F4 also prints floating-point margins on fixed points) produces
`RESULTS.json`, byte-identical under `-O`.
- **F1.** The model at the pins:
  - `det Hess G_ϖ(M̂) = (1 + β/2 − φ)/(4φ)`, `∂_z²G_ϖ(M̂) = −(1 + β/2)` and `det Hess G_ϖ(Ŝ) = −(1 − β/2 + φ)/(4φ)`, by exact
    central differences (exact for cubics), on random rationals;
  - the typed region `𝒯`;
  - the unnormalized determinants `6λ̃ + Y` and `−6λ̃ + Y`, and the normalization (0.4);
  - the window determinant identity behind (3.5), `|det Hess f| = k^{m−1}r²|det Hess 𝔉|`, for `m = 1, 2, 3`.
- **F2.** Lemma FL.2:
  - the Jacobians (2.1), as polynomial identities in `(X, z, 1/φ, β, χ)`, with the derivatives taken by exact polynomial
    differentiation;
  - the critical values on `X = ±½`, the factorization of `A₀ − L_S` and the end value `A₀(2) = 25/(48φ)` of the axial path,
    the double root `z = a/χ` and the inflection value on `D = 0`, and the `1/φ`-scaling of `A₀ − L_S`;
  - the coefficients `κ_±` of (2.2), against the leading-order slice equation and against `R(X)/X³` at `X = ±10⁶`
    (floating point); `κ_+ = 0` for the witness;
  - the Jacobian `k³γ²/(12μ̃⁴)` of `(γ, B, C_3) ↦ ϖ`, by exact differentiation.
- **F3.** Lemma FL.1:
  - the exponent table (1.2) for every monomial of degree `≤ 4` in `d = 2, 3, 4`, and the order-5 remainder;
  - on exactly pinned degree-6 fields with rational coefficients, the measured `C²` error of the window against
    `G_k^{(d)}` at four points. It drops by `99.87` (`d = 2`) and by `10.0001` (`d = 3`) when `r` drops by `100`: rates `r`
    and `r^{1/2}`. (The referee's check on non-polynomial fields gave the same rates; §5.)
- **F4.** Proposition FL.4:
  - the exact (D′) witness `G_{(3/2, 8/3, 20/3)}(X, z) = (1/9)G_{(1/6, 0, 0)}(X + 2z, 3z)` (found by OpenAI Codex on #242), as a
    polynomial identity;
  - a polynomial factorization showing that `G_{(1/6, 0, 0)}` has exactly the critical points `(±½, 0)` and `(−3, 35/8)`, so
    the witness has exactly three, with values `0`, `−1/36` and `−125/384`;
  - the crossing forms at `Ŝ` on rational points in cases (D) and (D′);
  - the two elementary facts used in Lemma FL.2(c): for `β > 2`, `χ < 0` the slice at `1/β` is open; for `χ > 0`, `D > a²` on
    `|X| < ½`;
  - the floating-point margins of the certificates of Step 3 on three fixed points, one per case.
- **F5.** Theorem FL: the change of variables `μ̃ ↔ φ`, the constant `384`, and `χ = k²C_3γ/μ̃² = χ_0φ²`, on random rationals.
- **F6.** The corollaries:
  - the factorization (4.2), as a polynomial identity in `(X, 1/φ)`, and its discriminant `4 − 12φ`;
  - the concave slice at `ϖ = (φ, 0, 0)` (`G = R` at `z_r = p/2`);
  - exact Sturm certificates of `(R)` along the ridge for `φ ∈ {2/5, 1/2, 3/4, 9/10}`: no root of `R − L_S − 1/200` on
    `[−3, −½]`, and `R(−3) > 0`;
  - the exponents of the pushforward (4.4) and of Remark 2.
- **F7.** Proposition FL.7:
  - `G_k(X, ζ) = P_θ(X, kζ)/k` as a polynomial identity in `(X, ζ)`, on random rational jets with `λ̃` of either sign;
  - `Y = 3kB′`, the weight identity `9k²(4s² − B′²) = 36λ̃² − Y²`, and the equivalence of the typed domains;
  - the hard-factor identity `𝒱(0, μ_2, …, μ_m)(μ_2⋯μ_m)² = Π μ_j³Π(μ_j − μ_i)` for `m = 2, 3, 4`;
  - the exponent `−8/3 + 1 = −5/3` of `d_{𝐁,𝐊} = C_fail^{𝐁,𝐊}`, and `dμ̃/ds = −k`.

Mutants `M1`–`M8` each fail only their own control (`M1` F1, `M2` F2, `M3` F3, `M4` and `M7` F4, `M5` F5, `M6` F6, `M8` F7); the checker
names the failing control on stderr, and an unknown label exits 2.

**What the controls do not test.**
- Proposition FL.4 for non-polynomial perturbations.
- The transversality and Sard arguments themselves (only their Jacobians).
- Lemma FL.2(c) beyond its two elementary facts (it is tested numerically in §5).
- The probabilistic steps of Theorem FL (coupling, conditioning, domination).
- The use of #170 Theorem E(1) in Proposition FL.7(iii). The referee's numerical comparison in §5 tests it.

These are argued in the text and are the subject of review slices B–E.

## 8. Sources (exact identities in `SOURCES.json`)

| Tag | Path (blob) | Use |
|---|---|---|
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (`dfed3b8d`) | §§1–3, 5–8, 10–12 — consumed |
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (`247b3ecf`) | (R2)–(R3), (R5), (R11) — consumed |
| #207 | `frontiers/cusp_second_order_20261001/PROOF.md` (`f6df5a73`) | §0, Theorem CU.1, the structure of CU.3–CU.4 — consumed |
| [C7-K] | `frontiers/c7_total_bounded_20260929/PROOF.md` (`28748b08`) | (K2) — consumed |
| [CAP] | `imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md` (`0633aca3`) | §§1, 5: the deterministic cap theorem — consumed (as in [P] §7) |
| [E1], [REC] | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` (`213594d6`), `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` (`75da2597`) | reading rules for [P] |
| [E2] | `reviews/d1_section9_borel_repair_20260925/REPAIR.md` (`fe9b9ce4`) | the elder mark is Borel — consumed |
| #242 | `frontiers/soft_rejected_pairs_20261002/PROOF.md` at `ffc7005` (`c1592915`, v1.4; §§0–3 as in v1.2's `ad4beb84`), unmerged | §0, (2.1)–(2.6), Lemmas 2–3, Proposition 2′, (3.1) — consumed |
| OA lift | `frontiers/elder_dimension_lift_20260928/PROOF.md` (`7303bd79`) | (A3) — cited |
| #229 | `frontiers/third_order_rate_20261001/PROOF.md` (`110ed33a`) | (R⁺.1) — cited |
| #170 | `frontiers/local_elder_geometry_20260930/PROOF.md` (`ef2aa579`) | §2 (Theorem E(1)), §§7–8 (the classifier, (S1), (S11), the mass `α₁ + α₂`), Theorem S, §9 — compared; consumed by Proposition FL.7 only |
| #175 | `frontiers/concave_fibre_elder_20260930/PROOF.md` (`923d3236`) | §§1–2, §3 (Theorem H), §5 (Theorem F, (S1)–(S3)), §7 — compared; consumed by Proposition FL.7 only |

## 9. Review slices

- **A** — §§0–1: the setting, Lemma FL.1 and (1.3); in particular the exponent table and the pinned coefficients in
  `d ≥ 3`.
- **B** — §2: Lemma FL.2 (the transversality arguments, (G2), (G3), and the trichotomy (c)), Lemma FL.3, and Proposition
  FL.4 (the facts (Path) and (Trap), the certificates in cases (R), (D), (D′), and the persistence in Step 4, including
  the stiff directions).
- **C** — §3, Steps 1–3: the coupling and the conditioning on `𝔸`, the Weyl zoom (3.4), the window identity (3.5), and the
  almost-everywhere convergence (full measure of `ϖ* ∈ 𝒦`).
- **D** — §3, Steps 4–5: the domination (cap region, (3.6), the `m = 1` far branch), and the identification with #242 (3.1).
- **E** — §4: Proposition FL.7 (the identification with #170/#175) and Corollaries FL.5 and FL.6 (the positivity of `F`, and
  the use of [P] (11.2) and [C7-K] (K2)), with §§5–6.

A reviewer should record, per slice: ACCEPT, ACCEPT WITH FIXES (list), or REJECT (with the failing step).

**Changed bytes in v1.4** (for a delta check against v1.3 at `4835564`):
- *Header:* the object label, the v1.4 entry, and the #242 dependency (rebound to v1.4).
- *§8:* the #242 source row.
- *§9:* this list.
- *Workflow:* the binding of the consumed #242 (finding 4167121714).

Everything else in `PROOF.md`, and `fold_check.py` and `RESULTS.json`, is unchanged.

**Changed bytes in v1.3** (for delta checks against the v1.2 slice reviews at `11a4cd4`):
- *Header:* the object label and versions; the FL.7 item of "What is new" (D.1); the #242 dependency (rebound to v1.3).
- *§2 (slice B):* the `m = 1` convention after Proposition FL.4's first sentence (B-01); the trivial case in the proof of
  (Trap) (B-02); the proof's first sentence, Step 3's first paragraph, the sentence after the certificates, and Step 4's
  first paragraph (B-03).
- *§3 (slice D):* the Weyl equality in Step 5, with the ordered upper limit `min(ε, λ_2)` and the sentence after it (D-01).
- *§4 (slice E):* the Remark on D.1 after Proposition FL.7, and the last clause of the paragraph after "A second proof".
- *§§6, 8–9:* the FL.7 item of §6, the #242 source row, and this list.

No statement changes in substance; Proposition FL.4's statement gains only the `m = 1` convention. §§0–1, §§2.1–2.2,
§3's Steps 1–4, the proofs of FL.5–FL.7, §§5 and 7, `fold_check.py` and `RESULTS.json` are unchanged.
