# Lifetime note TL: the rejected kernel uniformly on the soft layer, the `κ ≥ 1` side of IBA2-009, and the elder density with remainder `ℓ^{4/9}log(1/ℓ)`

Object: `CL-TL-SOFT-LAYER-20261006-v1`. Claim: main#229 6015458484; pickup on main#259 6015463045.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 6 October 2026, for Dylan Roy (delegated AI
work). The author also wrote [K], [N] (#240), #237 and #242–#244.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph, STATUS,
PROOF_INDEX, prize or Boolean change; no numerical constant is certified. Same GitHub account as every lane;
organizational independence 0.

**What is new.**
- **Theorem TL** (§§1–4). Let `𝐓_r^{rej}(k, u) := ∫r^{−2}A_r^{rej}(b, k, u) db` be the birth-integrated rejected kernel and
  `𝓐^{rej}(κ, u) := ∫𝒜^{rej}(b, κ, u) db` its cusp limit. In every `d ≥ 2`,
  `|𝐓_r^{rej}(k, u) − 𝓐^{rej}(κ, u)| ≤ C r²(1 + κ)` for `0 < r ≤ r₀`, `κ ≥ 1` and `k = κr ≤ 1`.
  - This is the relative bound (TL_a) of main#259 6001580409 with `a = 2`, after the `b`-integral. The error is `O(r²)` plus
    `O(k²/κ)`. Since `κ𝓐^{rej} → ∫F₀ db > 0` (#242 Theorem 1), that is a relative error `O(k²)`.
  - [N]'s Theorem N gives `O(r²)` only on compact `κ`-windows.
- **Why Theorem N was not uniform, and what replaces it.** [N]'s pathwise lemmas (Q′, Q″, R₂ and Ω) hold for every `κ`. The
  non-uniformity came from two integration steps: Step N1's margin `λ₃`, whose constant grows with `κ₁`, and Step N4's
  expansion of the edge shift `36rQ₁` in `f₄`. This note makes four changes.
  - The good event uses the `κ`-normalized margin `λ ≥ C𝒩r(1 + |γ| + ‖B‖ + |η|)(1 + |f₄|/κ)`, as in [N]'s own (2.3).
  - Birth integration (#237 Lemma R) makes the parity of the odd jets exact at every `r`.
  - The edge shift is expanded along the radial direction of `γ`, where `z − f₄ = 3|γ|²ωᵀ(−A)^{−1}ω`. There every function
    involved varies on the scale `κ`, while the shift is `O(κt)` with `t = 12kB/γ²`. Along `f₄` the scale is `1`, and
    that is where [N]'s constants grew.
  - Two window lemmas (§1) bound, uniformly in `κ`, the weighted mass of the rejected window (`C/κ`) and that of thin
    slabs at its edges (`C·width/κ²`).
- **Corollary TL1 (IBA2-009, the `κ ≥ 1` side).** The separations with `ℓ/r⁴ ≥ 1` contribute
  `ℓ^{1/4}∫_0^1∫𝓐^{rej}(s^{−4}, u) dσ ds + O(ℓ^{2/3})` to the rejected density. So that side has no term of order
  `ℓ^{1/2}`, and the tail condition (4.2) of Math-#296 holds at `κ → ∞` (TAIL-L).
- **Corollary TL2 (Math-#296's moving band).** `J_ℓ(y) = F̄₀ + O(ℓ^{1/5})` uniformly on compact `y`-bands. The band
  `y₁ ≤ k³/r ≤ y₂` therefore carries the cusp kernel's own share `(ℓ^{1/2}/10)F̄₀∫_{y₁}^{y₂}y^{−3/2}dy` up to `O(ℓ^{7/10})`,
  and no other half-power mass.
- **Corollary TL3 (the elder and rejected densities).**
  `ν_eld(ℓ) = cℓ^{−1/3} + c₁ℓ^{1/4} + c₂ℓ^{1/3} + ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{4/9}log(1/ℓ))`. With #187 the far term is
  `O(ℓ^{2/3})`, and `ρ_rej` has the same remainder. This improves #229's `3/7`. Three terms attain the exponent `4/9`: the
  cusp-kernel error on `κ ≤ 1` (`ρ²`), the cusp tail (`ℓ²ρ^{−7}`), and #229's bound on the intermediate elder mass, which
  also carries the logarithm.

**Not claimed.**
- The `κ → 0` side (TAIL-S). **IBA2-009 stays OPEN.** Nothing is claimed about an `ℓ^{1/2}` term of the whole elder or
  rejected density: `4/9 < 1/2`.
- No statement pointwise in `b`. No identification of the `k²/κ` term (which carries `R_{2/3}` of #242).
- No certified numerical value, and no uniformity in `d` or `L`.
- Nothing beyond the existential scope of the consumed packets.

**Consumed (all on Math- `main`; blob identities checked at `08f86862`, unchanged since `11f9127f`).**
- [N] = #240 `frontiers/elder_cusp_parity_20261002/PROOF.md` (blob `16a1db06`): §0 notation and (0.1); Lemma Q′; Proposition
  CE⁺⁺ with (2.2)–(2.3), (CE⁺⁺.1), its radius `r₂′` and the `𝔅_λ′` computation; Lemma R₂ (3.2); the model near the edges
  and Lemma Q″ (3.5); Lemma Ω (4.1)–(4.2); Step N1 (typing, the weight, the margins, `N₂`).
- #237 `frontiers/candidate_parity_rate_20261001/PROOF.md` (blob `a97bf528`): Lemma R (R.1)–(R.4); the moment bound for `T`
  under `Q̄_{r,k}` (§2); Step U2 (Case 3) and Step U4; Lemma U (U.1) with its radius `r₃`, Lemma K (K.1) and §5's main-term
  computation; Theorem P (P.1).
- #242 `frontiers/soft_rejected_pairs_20261002/PROOF.md` (blob `271412db`): §0, with (0.2) and the identity
  `I^{cand} − c₁ = ∫_0^∞∫∫𝒜^{rej}(b, s^{−4}, u) db dσ(u) ds`; Theorem 1 (1.0) with Remark 3.
- #220 `frontiers/elder_third_order_20261001/PROOF.md` (blob `c8767dde`): §0's identities for `ν_eld` and `cℓ^{−1/3}`, and
  `P`; §1's `r_Q`; (F1), (F2); Step E2 (the `𝒩`-layers); the proof of Lemma G (the Gaussian score along an interpolation of
  Gaussian laws); §4's `r_0^* ≤ r_0^{[K]}`.
- #229 `frontiers/third_order_rate_20261001/PROOF.md` (blob `110ed33a`): Lemma C⁺ (C⁺.1); §5's bound
  `I^{eld} = O(ℓ^{4/9}log(1/ℓ))` on `[ℓ^{2/9}, r_0^*]`.
- #218 `frontiers/candidate_third_order_20261001/PROOF.md` (blob `70ca57ef`): Step F1 (the free jets `J′`); Lemma D (1.1);
  Step C1 (its three cases).
- [K] `frontiers/c7_total_bounded_20260929/PROOF.md` (blob `28748b08`): §2's pathwise bound on `W_r/r²`; (K2); §4's use of
  the cap implication of [P] §8. `ERRATUM_NORMALIZED_FORM.md` (blob `b6764ce6`) does not touch them.
- [R] `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`): (R5), the Gaussian bound on `π_r(v_r)`.
- Math-#296 `reviews/iba2_009_matching_20261005/REPORT.md` (blob `a0b398f5`): the band formula (2.2)–(2.3) and the criterion
  (4.1)–(4.2).
- #187 `frontiers/far_elder_rate_20260930/PROOF.md` (blob `07260114`): the far bound, for the last form of TL3 only.

**Cited only.** #243 (Theorem FL, with its Remark 1), #242 Proposition 4 and Lemma 5, #244, #170/#175, #198 Lemma F′, and
the QS chain A4–A4.3 (rates at fixed `k` in a compact set, a different regime); [P] §8 through [K] §4; main#259 6001580409
((TL_a) and its consequences), 6001189633 (Sol's criterion), 6001319075 and 6001313460 (the TAIL-L and TAIL-S
obstructions).

**Prior work and overlap** (searched before drafting, as this lane's rule requires: the tree of `main`, the project
archive, and main#229 and main#259 for claims). No packet on `main` approximates the rejected kernel by its cusp limit with
a rate uniform as `κ → ∞` with `k → 0`, or improves the elder exponent `3/7`. ([K] (K2) bounds the rejected kernel by
`C/κ` uniformly; §5 uses that bound.) [N] Remark 1 predicted that uniformity would give `4/9` with a logarithm.
#237 proves the analogous uniform bound for the candidate kernel (Lemma U); its Remark 3 records why that proof does not
reach the elder kernel. That is still true: Theorem TL is proved for the rejected kernel by a different route, and
Corollary TL3 combines the two.

## 0. Setting and statement

Setting and notation are those of [N] §0, #237 §§0–1 and #242 §0. Fix `d ≥ 2`, `m := d − 1`, `L > 0` and the [P] field on
`X = R^d/(LZ^d)`. The near pins are `M = −ru/2` (a maximum) and `S = ru/2` (an index-`m` saddle) at gap `k`, so
`f(M) − f(S) = kr³`; `κ := k/r`, `ℓ = kr³ = κr⁴`.
- *Kernels.* `A_r(b, k, u) = 12π_r(v_r)E_Q[W_r/r²]`, `A_r^{rej} := A_r − A_r^{eld} = 12π_r(v_r)E_Q[(W_r/r²)(1 − e)]`, with the
  elder mark `e = 1{d_f(M) = f(S)}`. The weight is `ω_r := r^{−2}F_d(K_M)F_{d−1}(K_S) = r^{−2}Π1_{typed}`,
  `Π := −det K_M det K_S`, so `r^{−2}A_r^{rej} = 12π_r(v_r)E_Q[ω_r(1 − e)]`.
- *Birth integration* (#237 §1). `V_r` is the vector of rows (1.1) there, `v(k) = (0_d, 0_d, 12k)` its target, and
  `Q̄_{r,k}` the law of the field given `V_r = v(k)`; the birth height is integrated out. By (R.1), applied with the
  factor `1 − e` (Tonelli: (R.1) disintegrates over the birth height for any nonnegative functional),

      𝐓_r^{rej}(k, u) := ∫_R r^{−2}A_r^{rej}(b, k, u) db = 12 p_{V_r}(v(k)) E_{Q̄_{r,k}}[ω_r(1 − e)].                         (0.1)

- *Jets at `0`* ([N] §0): `A`, `B = ∂_uA`, `γ`, `η`, `f₄`, `f₅`; `Δ = det A`, `J = adj A`, `λ = λ_min(−A)` on `{A < 0}`;
  `Γ̃ := |A^{−1}γ|`, `q := γᵀA^{−1}γ`, `z := f₄ − 3q`; `Q₁` and `P₁ = Δ²Q₁` of [N] (0.1); `Y′ = (f₄/12)Δ − γᵀJγ/4`; and
  `w₀ := 36κ²Δ² − Y′²`, a polynomial in the jets. On `{A < 0}`, `Y′ = Δz/12` and `w₀ = (Δ²/144)(5184κ² − z²)`. The parity
  map `𝒫` negates the odd jets (`γ`, `B`, `f₅`, …). `z`, `w₀`, `Δ`, `Γ̃` are `𝒫`-even; `Q₁` and `P₁` are `𝒫`-odd.
- *The cusp side.* `𝒜^{rej} := 𝒜^{cand} − 𝒜^{eld}` (#242 (0.2)). Integrating #242 (0.2) in `b` as in #237 Step U4,

      𝓐^{rej}(κ, u) := ∫_R 𝒜^{rej}(b, κ, u) db = 12 p_{V_0}(v(0)) E_{Q̄_{0,0}}[G₀],        G₀ := w₀ 1{A < 0, 24κ ≤ |z| < 72κ},   (0.2)

  since `1/3 ≤ |φ| < 1` is `24κ ≤ |z| < 72κ` and `36κ²Δ²(1 − φ²) = w₀` there.
- *Constants.* `C, c, N` denote constants that depend only on `d` and `L` (and on the exponents named), may change from
  line to line, and never depend on `r`, `k`, `κ`, `b` or `u`. `P := 1 + |b| + k` as in #220 §0.

**Theorem TL (the rejected kernel on the soft layer).** There are `r₀ > 0` and `C` such that for `0 < r ≤ r₀`, `κ ≥ 1` with
`k = κr ≤ 1`, and `u ∈ S^{d−1}`,

    |𝐓_r^{rej}(k, u) − 𝓐^{rej}(κ, u)| ≤ C r² (1 + κ).                                                                  (TL)

In terms of the gap, `r²(1 + κ) = r² + k²/κ`. By #242 Theorem 1, `κ𝓐^{rej}(κ, u) = ∫F₀(b, u)db + O(1/κ)` with
`∫F₀ db > 0`, so (TL) is an error `O(κr² + k²) = O(k²)` relative to the size of `𝓐^{rej}`.

**Corollary TL1 (the separations with `ℓ/r⁴ ≥ 1`).** As `ℓ ↓ 0`,

    ∫_0^{ℓ^{1/4}}∫_{S^{d−1}} 𝐓_r^{rej}(ℓ/r³, u) dσ(u) dr = ℓ^{1/4}∫_0^1∫_{S^{d−1}} 𝓐^{rej}(s^{−4}, u) dσ(u) ds + O(ℓ^{2/3}).   (TL1)

**Corollary TL2 (the moving band of Math-#296).** With #296's `J_ℓ(y) = k_ℓB_{r_ℓ}(k_ℓ)/r_ℓ³`,
`r_ℓ = ℓ^{3/10}y^{−1/10}`, `k_ℓ = ℓ^{1/10}y^{3/10}` and `B_r(k) = ∫∫A_r^{rej} db dσ`, and with `F̄₀ := ∫∫F₀ db dσ`
(#242 (1.0)): for every `0 < y₁ < y₂ < ∞` there is `C` with `|J_ℓ(y) − F̄₀| ≤ Cℓ^{1/5}` for `y ∈ [y₁, y₂]` and small `ℓ`.
Hence #296's band contribution (its `ν_{[a,b]}` with `[a, b] = [y₁, y₂]`) is
`(ℓ^{1/2}/10)F̄₀∫_{y₁}^{y₂}y^{−3/2} dy + O(ℓ^{7/10})`.

**Corollary TL3 (the elder and rejected densities).** As `ℓ ↓ 0`,

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{4/9} log(1/ℓ)),                      (TL3.1)
    ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁) ℓ^{1/4} − ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{4/9} log(1/ℓ)),                             (TL3.2)

and with #187 (`0 ≤ ν_eld^{far,r_0^*} ≤ Cℓ^{2/3}`) the far terms may be dropped. For the SIDE24 law (`d = 3`, `L = 24`) this
reads `ν_{3,24}(ℓ) = cℓ^{−1/3}(1 + (c₁/c)ℓ^{7/12} + (c₂/c)ℓ^{2/3} + O(ℓ^{7/9}log(1/ℓ)))`, against #229's `O(ℓ^{16/21})`.

## 1. The law after birth integration, and two window lemmas

`J′` is the vector of free jets of `f` at `0` of order `≤ 9` (#218 Step F1); it contains `A, f₄, γ, B, η, f₅`. Split it into
its even part `E` (jets of even order: `A`, `f₄`, `η`, …) and its odd part `O` (`γ`, `B`, `f₅`, …), and write `O = (γ, O′)`.
Put `𝒩 := 1 + k + max_{1≤|α|≤9}‖∂^αf‖_{C⁰(X)}`. The pathwise statements of [N], of #220 (F1)–(F2) and of [K] §2 ask `𝒩`
to bound the sup norm of the field as well. Apply them to `f − f(M)`. It has the same `e`, the same window fields and the
same jets of positive order, and `sup|f − f(M)| ≤ (√d L/2)sup|∇f|`. So they hold with `C_L𝒩` in place of `𝒩`, where
`C_L := max(1, √d L/2)`, and `C_L` is absorbed into the constants (`C₄`, `C₁₂`, `c₁₃` and `N` below).

**Facts under `Q̄_{r,k}`** (`0 ≤ r ≤ r_0^*`, `0 ≤ k ≤ 1`).
- (B1) `J′` is Gaussian, and its covariance `Γ_r` lies between `c₀I` and `C₀I` (#237 (R.4) with #218 Step F1).
- (B2) `E` and `O` are independent. `E` is centred, and its law does not depend on `k`. `O ~ N(k w_r, Σ_{O,r})`, with
  `w_r` and `Σ_{O,r}` independent of `k` (#237 (R.2)). The means and covariances are smooth even functions of `r`, so they
  differ from those at `r = 0` by `O(r²)` (#237 (R.4)). In particular `Q̄_{r,0}` is invariant under `𝒫`.
- (B3) `p_{V_r}(v(k)) = p_{V_r}(v(0))e^{−a_rk²}`, with `a_r > 0` smooth and even in `r`. Indeed `V_r` is Gaussian and
  `p_{V_r}(v(−k)) = p_{V_r}(v(k))` (#237 (R.2)), so the log-density along the line `{v(k)}` is an even quadratic polynomial in `k`.
- (B4) Given the other free jets, `f₄` is Gaussian with variance in `[c, C]` and mean `μ₄`, a linear function of the other
  even jets. Given the other free jets, `A` is Gaussian on `Sym(m)` with covariance between `cI` and `CI` and mean linear in
  the other even jets. Both are Schur complements in `Γ_r`, together with (B2). So #218 Lemma D applies conditionally: for
  `ε > 0`, `E[(1 + ‖A‖)^n1{A < 0, λ < ε} | rest] ≤ C(1 + |rest|)^{n′}ε` and
  `E[(1 + ‖A‖)^n1{|Δ| < ε} | rest] ≤ C(1 + |rest|)^{n′}ε`.
- (B5) `E[𝒩^p | J′] ≤ C_p(1 + |J′|)^p` (#237 §2, the bound for #218's `T` under `Q̄_{r,k}`).

Call `𝔏` the class of Gaussian laws of `J′` with covariance between `c₀I` and `C₀I` and mean of norm `≤ C₀`. It contains
`Q̄_{r,k}` for `r ≤ r_0^*`, `k ≤ 1`, and every law whose mean and covariance interpolate linearly between two such laws.
Call `𝔏_× ⊂ 𝔏` the laws under which `E` and `O` are independent and `E` is centred (as in (B2)). The small-ball bounds of
(B4) hold for every law in `𝔏`, since they use only the covariance bounds (the conditional means are then affine in the
other jets, of size `≤ C(1 + |rest|)`); the stated form of the means holds in `𝔏_×`. Under a law in `𝔏_×`, `γ` given `O′`
is Gaussian, `N(μ_γ(O′), Σ′)`, with `c₀I ≤ Σ′ ≤ C₀I` and `|μ_γ(O′)| ≤ C(1 + |O′|)`.

**The window.** On `{A < 0}`, `|q| = γᵀ(−A)^{−1}γ ≤ |γ|²/λ`, `z = f₄ + 3|q| ≥ f₄`, and

    Γ̃² = |A^{−1}γ|² ≤ |q|/λ,        so        Δ²Γ̃^{2j} ≤ λ^{2−j}|q|^j‖A‖^{2m−2}        (j = 0, 1, 2),                         (1.1)

because `Δ² ≤ λ²‖A‖^{2m−2}` and `|(−A)^{−1}γ|² ≤ λ_max((−A)^{−1})·γᵀ(−A)^{−1}γ`.

**Lemma W₁ (the rejected window has mass `1/κ`).** For `p, s ≥ 0` there is `C` such that for every law in `𝔏` and `κ ≥ 1`,

    E[(1 + |J′|)^p λ^s 1{A < 0, |z| ≥ 20κ}] ≤ C κ^{−1−s}.                                                              (1.2)

In particular, with `Δ² ≤ λ²‖A‖^{2m−2}`: `E[(1 + |J′|)^p κ^aΔ²λ^s1{A < 0, |z| ≥ 20κ}] ≤ Cκ^{a−3−s}`.

*Proof.* On `{A < 0, |z| ≥ 20κ}`, either `|f₄| ≥ 10κ` or `3|q| ≥ 10κ`; in the second case `λ ≤ 3|γ|²/(10κ) =: ε`.
- *`|f₄| ≥ 10κ`.* Bound `1 ≤ (|f₄|/(10κ))^{N′}` and `λ^s ≤ ‖A‖^s`. The expectation is `≤ Cκ^{−N′}` for every `N′`.
- *`λ ≤ ε`.* Then `λ^s ≤ ε^s`. Condition on all jets except `A`; by (B4), `E[(1 + ‖A‖)^n1{A < 0, λ < ε} | rest] ≤ C(1 + |rest|)^{n′}ε`.
  Since `(1 + |J′|)^p ≤ (1 + |rest|)^p(1 + ‖A‖)^p`, the contribution is `≤ CE[(1 + |rest|)^{n″}ε^{1+s}] ≤ Cκ^{−1−s}`, because
  `ε^{1+s} = (3|γ|²/10)^{1+s}κ^{−1−s}` and `γ` is part of `rest`. ∎

**Lemma W₂ (edge slabs).** Let `x₀ ∈ {24κ, 72κ}`, `κ ≥ 1`, and
`𝒮_{x₀} := {A < 0, |f₄| ≤ 13κ, |z − x₀| ≤ 4κ}`. Let the law be in `𝔏_×`, and put `T := (E, O′)`, so that `J′ = (T, γ)`. On
`{A < 0}` write `γ = ρω` (`ρ = |γ|`, `ω ∈ S^{m−1}`; for `m = 1`, `S⁰ = {±1}` with counting measure) and
`μ(A, ω) := ωᵀ(−A)^{−1}ω`, so that `z = f₄ + 3ρ²μ`. Let `Y ≥ 0` be Borel, with `Y ≤ Ȳ(T)(1 + |γ|)^M` on `𝒮_{x₀}`, and for each
`(T, ω)` let `Z(T, ω) ⊂ [x₀ − 4κ, x₀ + 4κ]` be a Borel set of Lebesgue measure `≤ h̄(T)`. Then for every `N` there is `C`
(depending also on `M`, `N`) such that

    E[Y 1{z ∈ Z(T, γ/|γ|)} 1_{𝒮_{x₀}}] ≤ (C/κ) E[h̄(T)Ȳ(T)(1 + |O′|)^{M+m+2N} min(1, (κλ)^{−N}) 1{A < 0, |f₄| ≤ 13κ}].   (1.3)

If moreover `h̄Ȳ ≤ κ^aλ^sΠ(T)` with `s ≥ 0` and `Π ≥ 0` bounded by a polynomial in `|T|`, the right side is `≤ Cκ^{a−2−s}`.

*Proof.* Fix `T` with `A < 0` and `|f₄| ≤ 13κ`, and `ω`. The map `ρ ↦ z = f₄ + 3ρ²μ` is increasing on `(0, ∞)`, with
`dz/dρ = 6ρμ = 2(z − f₄)/ρ`. The law of `γ` given `O′` has density `p_γ ≤ C exp(−|γ − μ_γ|²/(2C₀))`. So

    E[Y1{z ∈ Z}1_{𝒮} | T] ≤ ∫_{S^{m−1}}dσ(ω) ∫_{Z(T,ω)} Ȳ(T)(1 + ρ)^M p_γ(ρω) ρ^m/(2(z − f₄)) dz,        ρ = ρ(z).

On the slab `z − f₄ ≥ x₀ − 4κ − 13κ ≥ 7κ`, and `ρ` ranges over `[ρ₋, ρ₊]` with `ρ_±² = (x₀ ± 4κ − f₄)/(3μ)`. Since
`μ ≤ 1/λ`, `ρ₋² ≥ 7κλ/3`; and `ρ₊²/ρ₋² ≤ (x₀ + 17κ)/(x₀ − 17κ) ≤ 41/7 < 9`, so `ρ₊ ≤ 3ρ₋`. As `|ρω − μ_γ| ≥ ρ − |μ_γ|`,

    sup_{[ρ₋,ρ₊]}(1 + ρ)^{M+m}p_γ(ρω) ≤ C(1 + 3ρ₋)^{M+m}e^{−(ρ₋ − |μ_γ|)₊²/(2C₀)} ≤ C_N(1 + |μ_γ|)^{M+m+2N}min(1, ρ₋^{−2N}):

if `ρ₋ ≤ 2|μ_γ| + 1`, the middle term is `≤ C(1 + |μ_γ|)^{M+m}`, and `(1 + |μ_γ|)^{2N}min(1, ρ₋^{−2N}) ≥ 2^{−2N}`;
otherwise `ρ₋ > 1` and `ρ₋ − |μ_γ| ≥ ρ₋/2`, and the Gaussian factor beats every power of `ρ₋`. With `ρ₋^{−2N} ≤ (7κλ/3)^{−N}`
and `|μ_γ| ≤ C(1 + |O′|)`, the inner integral is `≤ h̄Ȳ·C(1 + |O′|)^{M+m+2N}min(1, (κλ)^{−N})/(14κ)`; integrate over `ω` and
then over `T`.

For the second statement, condition on `T ∖ {A}` (`γ` is already integrated out). Under a law in `𝔏_×` the law of `A` given
`T ∖ {A}` is its law given the other even jets (`E ⊥ O`), so (B4) applies. In dyadic layers of `λ` it gives, for `N > s + 1`,
`E[λ^s(1 + ‖A‖)^nmin(1, (κλ)^{−N})1{A < 0} | rest] ≤ Σ_{j≥0}(2^j/κ)^s 2^{−(j−1)N}C(1 + |rest|)^{n′}2^j/κ ≤ Cκ^{−1−s}(1 + |rest|)^{n′}`,
which gives `(C/κ)·κ^a·κ^{−1−s}`. ∎

*Use.* W₁ and W₂ are the only places where the size of the rejected window enters. Every weight below is `κ²Δ²` times
quantities controlled by (1.1) on the window (where `|q| ≤ (|z| + |f₄|)/3`). So it is a sum of terms `κ^aλ^sΠ`, and
the lemmas turn each term into a power of `κ`.

## 2. The rejected weight on a `κ`-normalized good event

Fix `κ ≥ 1` with `k = κr ≤ 1`, and let `c_e = 1/200` and `δ_e = 1/96` be the constants of [N] §3. Put

    G_r := (w₀ + 12kP₁)₊ 1{A < 0, |z| ≥ 24κ + 36rQ₁, r|Q₁| ≤ c_eκ}.                                                   (2.1)

On its support, `|36rQ₁| ≤ 36c_eκ` and `12k|P₁| = 12κrΔ²|Q₁| ≤ 12c_eκ²Δ²`. Also `w₀ + 12kP₁ > 0` forces
`z² < 5184κ² + 1728c_eκ²`. Hence

    0 ≤ G_r ≤ 37κ²Δ² 1{A < 0, 23κ ≤ |z| ≤ 73κ}.                                                                      (2.2)

The *good event* is

    𝔊 := {A < 0, λ ≥ λ₄, 𝒩 ≤ c₁₃/r, |Δ| ≥ C₁₂ r 𝒩^{N₂}(1 + ‖B‖)},        λ₄ := C₄𝒩r(1 + |γ| + ‖B‖ + |η|)(1 + |f₄|/κ).

The factor `1 + |f₄|/κ`, not `1 + |f₄|`, is the point. It is [N]'s `λ₂′` of (2.3) with `|η|` added. [N]'s Step N1 used
`λ₃ = C₁₁𝒩r(…)(1 + |f₄|)` with `C₁₁ ≍ κ₁`.

**Lemma GE (the decision on `𝔊`).** Let `N₂ := max(N₁, m − 1)` as in [N] Step N1 (`N₁` of #220 (F1)). There are `C₄`,
`C₁₂` (large), `c₁₃` (small) and `r₄ ∈ (0, min(r_0^*, r_Q, 1/10)]` (`r_Q` of #220 §1) such that, for `0 < r ≤ r₄`,
`κ ≥ 1`, `k = κr ≤ 1` and every `f ∈ C⁹(X)` with the pins, on `𝔊`:
- (a) the pair is not anti-typed, and `ω_r = (w₀ + 12kP₁ + ε_ω)₊`, where `|ε_ω| ≤ C(r² + k²)𝒩^N`;
- (b) if the pair is typed: `|φ_r| < 3`, `Γ̃² ≤ 72κ(1 + |f₄|/κ)/λ`, and (Q′1), (Q′2), `ε̃ ≤ c_eκ`, `ζ := r|Q₁|/κ ≤ c_e` hold, as
  does Lemma R₂;
- (c) if the pair is typed, then `1 − e = 1{|z| ≥ 24κ + 36rQ₁}` off the edge set
  `ℰ := {||z| − 24κ − 36rQ₁| ≤ 72κϑ}`, with `ϑ` as in [N] (3.5); and on `𝔊 ∩ {typed}`, `ℰ ⊂ {23κ ≤ |z| ≤ 25κ}`.

*Proof.* (a) Since `λ ≥ λ₄ > r𝒩`, Case 1 of #218 Step C1 holds: the pair is typed iff `s·det K_M < 0 < s·det K_S`
(`s = (−1)^m`). By #220 (F1), `s(det K_S − det K_M) = 12k|Δ| + O(r²𝒩^{N₁})`. This is positive when
`|Δ| ≥ C₁₂r𝒩^{N₂}`, `N₂ ≥ N₁`, `C₁₂` large, because `12k|Δ| ≥ 12C₁₂r²𝒩^{N₂}` (`κ ≥ 1`). So no pair is anti-typed, and
`ω_r = (r^{−2}Π)₊`. The weight is [N] Step N1, "The weight": by Lemma Ω (4.1)–(4.2),
`r^{−2}Π = w₀ + 12kP₁ + 9k²[Δ(Δ_C + Δ_BB) − Δ_B²] + O(r²𝒩^N)`.

(b) On typed pairs, `|rY_r| < 6k|Δ| + Cr²𝒩^{N₁}`, so `|Y_r| < 7κ|Δ|` by the margin on `|Δ|`. Since
`Y_r = 6κΔφ_r + 3kΔ_B` and `|Δ_B| ≤ m𝒩^{m−1}‖B‖`, we get `|φ_r| ≤ 7/6 + m/(2C₁₂) < 3`. Then `3|q| = |f₄ − 72κφ_r| ≤ |f₄| + 216κ`,
and (1.1) gives `Γ̃² ≤ (|f₄| + 216κ)/(3λ) ≤ 72κ(1 + |f₄|/κ)/λ`. With `λ ≥ λ₄`, `𝒩r ≤ c₁₃`, `k ≤ 1` and `κ ≥ 1`:
- `r‖B‖Γ̃²/(8κ) ≤ 9r‖B‖(1 + |f₄|/κ)/λ ≤ 9/C₄`;
- `r|η|Γ̃/(12κ) ≤ (1/12)(72·r|η|·r|η|(1 + |f₄|/κ)/λ)^{1/2} ≤ (1/12)(72c₁₃/C₄)^{1/2}`;
- `r|f₅|/(120κ) ≤ c₁₃/120`.

  So `ζ ≤ c_e` for `C₄` large and `c₁₃` small.
- `ε̃ = 220C₁𝒩r(1 + Γ̃)² ≤ 440C₁c₁₃ + 440C₁𝒩r·72κ(1 + |f₄|/κ)/λ ≤ (440C₁c₁₃ + 31680C₁/C₄)κ ≤ c_eκ`.
- (Q′1), first part: with `R′ = 5M̃ + 4 + 3((κ + 1)/λ)^{1/2}`, `M̃ = (35/8)Γ̃`, it suffices that `3𝒩r`, `4𝒩r²`, `(175/8)𝒩r²Γ̃` and
  `3𝒩r²((κ + 1)/λ)^{1/2}` are each `≤ λ/8`.
  - The first two hold for `C₄ ≥ 32`.
  - The third holds if `175²·72𝒩²r⁴κ(1 + |f₄|/κ) ≤ λ³`. Since `r⁴κ = r³k ≤ r³`, this follows from `λ³ ≥ C₄³𝒩³r³(1 + |f₄|/κ)³`.
  - The fourth holds if `576𝒩²r⁴(κ + 1) ≤ λ³`, and `r⁴(κ + 1) ≤ 2r³`.
- (Q′1), second part: `6r + 2r²R′ ≤ L/4`. Here `rΓ̃ ≤ (72kr(1 + |f₄|/κ)/λ)^{1/2} ≤ (72/C₄)^{1/2}`, so
  `2r²·5M̃ ≤ 44r` for `C₄ ≥ 72`. Also `(κ + 1)/λ ≤ 2κ/(C₄r)`, so `2r²·3((κ + 1)/λ)^{1/2} ≤ 6r²(2κ/(C₄r))^{1/2} = 6r(2k/C₄)^{1/2} ≤ 6r`.
  So `r ≤ r₄` suffices.
- (Q′2): `2C₁𝒩r ≤ λ` for `C₄ ≥ 2C₁`, and `5r(1 + M̃) ≤ 1` for `r ≤ 1/10` and `(175/8)(72/C₄)^{1/2} ≤ 1/2`.
- Lemma R₂ needs (Q′1)–(Q′2) and `𝒩 ≥ ‖f‖_{C⁶}` (orders `≥ 1`).

(c) As in [N] Step N1: off `J₊ ∪ J₋`, Lemma Q′ decides `e = 1{|φ_r| < 1/3}`, since `2ε̃/(3κ) ≤ 1/300 < δ_e`. There
`1{|φ_r| < 1/3} = 1{|z| < 24κ + 36rQ₁}`, since `36r|Q₁| ≤ 36c_eκ < 72κδ_e`. On `J_±`, Lemma Q″ (c) decides `e` as stated, off
`ℰ`. Finally `ϑ = C₁₀[ζ² + ε₂′/κ + ε̃²/κ²]` is small on `𝔊 ∩ {typed}`. Here `ε₂′ = C₉[𝒩r²(1 + Γ̃)³ + 𝒩²r²(1 + Γ̃)²/λ]`
([N] (3.2)); use `(1 + Γ̃)³ ≤ 4(1 + Γ̃³)` and `(1 + Γ̃)² ≤ 2(1 + Γ̃²)`:
- `𝒩r²/κ ≤ c₁₃r` and `𝒩r²Γ̃³/κ ≤ 72^{3/2}k^{1/2}/C₄^{3/2}`;
- `𝒩²r²/(λκ) ≤ c₁₃/C₄` and `𝒩²r²Γ̃²/(λκ) ≤ 72/C₄²`;
- by (b), `ζ ≤ 9/C₄ + (72c₁₃/C₄)^{1/2}/12 + c₁₃/120` and `ε̃/κ ≤ 440C₁c₁₃ + 31680C₁/C₄`.

Each bound tends to `0` as `C₄ → ∞` and `c₁₃ → 0`. So `72κϑ + 36r|Q₁| = κ(72ϑ + 36ζ) ≤ κ` for `C₄` large and `c₁₃`
small. ∎

**Proposition RW (the rejected weight).** For `0 < r ≤ r₄`, `κ ≥ 1` and `k = κr ≤ 1`,

    |E_{Q̄_{r,k}}[ω_r(1 − e)] − E_{Q̄_{r,k}}[G_r]| ≤ C r²(1 + κ).                                                        (2.3)

*Proof.* By Lemma GE, on `𝔊` off `ℰ`:
- if the pair is typed, then `ω_r(1 − e) = (w₀ + 12kP₁ + ε_ω)₊1{|z| ≥ 24κ + 36rQ₁}`, and the cutoff `r|Q₁| ≤ c_eκ` of `G_r`
  holds;
- if it is not typed, then `ω_r = 0` and `(w₀ + 12kP₁ + ε_ω)₊ = 0`.

In both cases `|ω_r(1 − e) − G_r| ≤ |ε_ω|1{A < 0, |z| ≥ 23κ}`. So

    |ω_r(1 − e) − G_r| ≤ (ω_r + G_r)(1_{𝔊^c} + 1_{𝔊∩{typed}∩ℰ}) + |ε_ω|1{A < 0, |z| ≥ 23κ}.

Write `E` for `E_{Q̄_{r,k}}`. Facts (B4)–(B5) are used in dyadic layers of `𝒩` throughout, as in #220 Step E2: on
`{𝒩 ∈ [2^j, 2^{j+1})}` replace `𝒩` by `2^{j+1}` in every threshold and pay `P(𝒩 ≥ 2^j | J′) ≤ C_p2^{−jp}(1 + |J′|)^p`.

*The term `|ε_ω|`.* By (B5) and Lemma W₁, `E[|ε_ω|1{A<0, |z| ≥ 23κ}] ≤ C(r² + k²)/κ ≤ Cr²(1 + κ)`.

*The complement of `𝔊`.* `𝔊^c ⊂ 𝔅_a ∪ 𝔅_b ∪ 𝔅_c ∪ 𝔅_d`. Throughout:
- (F2) of #220 gives `ω_r ≤ 36κ²Δ² + Cr(1 + κ)𝒩^N`;
- [K] §2's pathwise bound `W_r/r² ≤ C(k + r)²(1 + ‖f‖_{C⁴})^{2m+4}` gives `ω_r ≤ C(1 + κ)²𝒩^N` (with `C_L`, as in §1);
- (2.2) gives `G_r ≤ 37κ²Δ²`.

The four events:
- `𝔅_a := {λ_max(A) ≥ −r𝒩}`. If `λ_max(A) > r𝒩`, the pair is not typed and `A ≮ 0`, so both terms vanish. If
  `|λ_max(A)| ≤ r𝒩`, #237 Step U2 (Case 3) gives `ω_r ≤ C(k + r)²𝒩^N`, and this event has probability `≤ Cr` with
  polynomial weights (#218 Lemma D in `𝒩`-layers). `G_r` there is covered by `𝔅_b`. So the contribution is
  `≤ Cr(k + r)² ≤ Cr²(1 + κ)`, since `rk² = r²κk`.
- `𝔅_b := {A < 0, λ < λ₄}`. This is [N] §2's `𝔅_λ′` computation with `λ₄` in place of `λ₂′`. Put
  `t₁ := 2C₄𝒩r(1 + |γ| + ‖B‖ + |η|)`, so that `λ₄ ≤ t₁max(1, |f₄|/κ)`.
  - On `{λ < t₁}`, `Δ² ≤ t₁²‖A‖^{2m−2}`, and (B4) given all jets but `A` gives `E[κ²Δ²1{λ < t₁}] ≤ Cκ²E[t₁³(…)] ≤ Cκ²r³`.
  - On `{t₁ ≤ λ < t₁|f₄|/κ}`, bound `κ²Δ² ≤ κ^{−1/2}t₁^{5/2}|f₄|^{5/2}λ^{−1/2}‖A‖^{2m−2}`. By (B4),
    `E[λ^{−1/2}(1 + ‖A‖)^n1{A < 0} | rest]` is polynomially bounded. This gives `Cκ^{−1/2}r^{5/2}`.
  - The part `Cr(1 + κ)𝒩^N` costs `Cr(1 + κ)E[λ₄(…)] ≤ Cr²(1 + κ)`.

  In all, `C(κ²r³ + r²(1 + κ)) ≤ Cr²(1 + κ)`, because `κ²r³ = r²κk`.
- `𝔅_c := {𝒩 > c₁₃/r}`. `E[(C(1 + κ)²𝒩^N + 37κ²𝒩^{2m})(r𝒩/c₁₃)⁴] ≤ C(1 + κ)²r⁴ ≤ Cr²`.
- `𝔅_d := {A < 0, |Δ| < ε}`, `ε := C₁₂r𝒩^{N₂}(1 + ‖B‖)`. Here `κ²Δ² ≤ κ²ε²`, and `P(|Δ| < ε | rest) ≤ Cε(…)` by (B4). So the
  contribution is `≤ C(κ²r³ + r(1 + κ)r) ≤ Cr²(1 + κ)`.

*The edge set on `𝔊 ∩ {typed}`.* There `ω_r ≤ 37κ²Δ² + |ε_ω|`, `G_r ≤ 37κ²Δ²`, and `𝔊 ∩ {typed} ∩ ℰ ⊂ {23κ ≤ |z| ≤ 25κ}`
(Lemma GE (c)). The part `|ε_ω|` is bounded as above. For `74κ²Δ²`, take `𝒩`-layers. On layer `j`, `ℰ ⊂ ℰ_j`, where `ℰ_j` is `ℰ` with `𝒩 = 2^{j+1}` in
`ϑ`, which is increasing in `𝒩`.
- *`|f₄| > 13κ`.* Given the jets other than `f₄`, `Q₁` and `ϑ_j` are fixed, and `ℰ_j ∩ {23κ ≤ |z| ≤ 25κ}` is two
  `f₄`-intervals of length `≤ min(144κϑ_j, 2κ)`. They lie where `|f₄ − 3q| ∈ [23κ, 25κ]`, so `|f₄| ≥ max(13κ, 3|q| − 25κ)`.
  - The conditional density of `f₄` there is `≤ C exp(−c(max(13κ, 3|q| − 25κ) − |μ₄|)₊²)` (B4). Since
    `max(13κ, 3|q| − 25κ) ≥ (κ + |q|)/2`, it is `≤ C_N(1 + |μ₄|)^{N′}(κ + |q|)^{−N}`, and `μ₄` is linear in the other even
    jets.
  - By (1.1), `κ²Δ²·κϑ_j` is a polynomial in `(r, 𝒩, |q|, ‖A‖, |γ|, ‖B‖, |η|, |f₅|)` times `r²κ^N`.
  - So this part is `≤ C_N r²κ^{−N}`.
- *`|f₄| ≤ 13κ`.* Then `z ≥ −13κ`, so `𝔊 ∩ {typed} ∩ ℰ ⊂ 𝒮_{24κ}`. Use Lemma W₂ with `x₀ = 24κ`,
  `Y := 74κ²Δ²C_p2^{−jp}(1 + |J′|)^p` and `Ȳ_j(T) := 74C_p2^{−jp}κ²Δ²(1 + |T|)^p`.
  - On the slab `|q| = (z − f₄)/3 ≤ 41κ/3`, so `Γ̃² ≤ Γ̄² := 41κ/(3λ)`, and `|Q₁| ≤ Q̄₁ := |f₅|/120 + |η|Γ̄/12 + ‖B‖Γ̄²/8`, a
    function of `T`.
  - In `z`, `|dQ₁/dz| ≤ Q̄₁/(z − f₄) ≤ Q̄₁/(7κ)` (§3, (3.2)). So on `{rQ̄₁ ≤ 7κ/72}` the map `z ↦ z − 36rQ₁` has derivative
    `≥ 1/2`, and the set `Z_j(T, ω)` of slab points of `ℰ_j` has measure `≤ h̄_j(T) := 288κϑ̄_j(T)`, where `ϑ̄_j` is `ϑ_j`
    with `Γ̃ → Γ̄` and `|Q₁| → Q̄₁`.
  - On `{rQ̄₁ > 7κ/72}`, bound `1 ≤ (72rQ̄₁/(7κ))²` and use Lemma W₁. By (1.1),
    `Δ²Q̄₁² ≤ C‖A‖^{2m−2}(λ²f₅² + |η|²κλ + ‖B‖²κ²)`, so this part is `≤ Cr²(κ^{−3} + κ^{−1} + κ)`.
  - `h̄_jȲ_j` is a sum of terms `κ^aλ^sΠ(T)`, by `Δ² ≤ λ²‖A‖^{2m−2}` and `Γ̄² = 41κ/(3λ)`. Lemma W₂ turns each into
    `κ^{a−2−s}`:

    | factor of `κ³Δ²` in `h̄Ȳ` | `(a, s)` after `Δ² ≤ λ²‖A‖^{2m−2}` | `κ^{a−2−s}` |
    |---|---|---|
    | `ζ̄² = r²Q̄₁²/κ²` | `(1, 2)`, `(2, 1)`, `(3, 0)` | `κ^{−3}`, `κ^{−1}`, `κ` |
    | `r²(1 + Γ̄)³/κ` | `(2, 2)`, `(7/2, 1/2)` | `κ^{−2}`, `κ` |
    | `r²(1 + Γ̄)²/(λκ)` | `(2, 1)`, `(3, 0)` | `κ^{−1}`, `κ` |
    | `ε̄²/κ² ∝ r²(1 + Γ̄)⁴/κ²` | `(1, 2)`, `(3, 0)` | `κ^{−3}`, `κ` |

    Each term carries `r²` and a power of `2^j` that the factor `2^{−jp}` absorbs. So this part is `≤ Cr²(1 + κ)`.

Collecting gives (2.3). ∎

## 3. Parity and the edge shift

For real `s` (a signed separation, with `κ` fixed) put

    G_s := (w₀ + 12κsP₁)₊ 1{A < 0, |z| ≥ 24κ + 36sQ₁, |s||Q₁| ≤ c_eκ},                                                 (3.0)

so that `G_r` is (2.1) and `G₀ = w₀1{A < 0, 24κ ≤ |z| < 72κ}` is (0.2). Since `z`, `w₀` are `𝒫`-even and `Q₁`, `P₁` are
`𝒫`-odd, `G_s(E, −O) = G_{−s}(E, O)`. (2.2) holds for every `|s| ≤ r`.

**The radial parametrization.** Fix `T = (E, O′)` with `A < 0`, and `ω ∈ S^{m−1}`. Put `μ := ωᵀ(−A)^{−1}ω` and `γ = ρω`. Then
`z = f₄ + 3ρ²μ`, and

    Q₁ = c₀ + c₁ρ + c₂ρ²,        c₀ = f₅/120,  c₁ = −ηᵀA^{−1}ω/12,  c₂ = ωᵀA^{−1}BA^{−1}ω/8.                             (3.1)

Viewed as functions of `z ∈ (f₄, ∞)`, `dρ/dz = ρ/(2(z − f₄))`. Since `|c₁|ρ ≤ |η|Γ̃/12` and `|c₂|ρ² ≤ ‖B‖Γ̃²/8`,

    |dQ₁/dz| ≤ (|η|Γ̃/12 + ‖B‖Γ̃²/4)/(2(z − f₄)).                                                                       (3.2)

Given `T`, `z` has the density `ρ_z(z) := p_γ(ρω)ρ^m/(2(z − f₄))` with respect to `dz dσ(ω)`, and, since
`|ρωᵀ∇log p_γ(ρω)| ≤ ρ(ρ + |μ_γ|)/c₀`,

    |d log ρ_z/dz| ≤ C(1 + ρ² + |μ_γ|²)/(z − f₄).                                                                       (3.3)

**The envelope.** On `{A < 0, |f₄| ≤ 12κ}` put `Γ̂² := 85κ/(3λ)` and `Q̂₁ := |f₅|/120 + |η|Γ̂/12 + ‖B‖Γ̂²/8`, functions of `T`.
Let `|f₄| ≤ 12κ` and `z ∈ [23κ, 73κ]`; this interval contains the support of `G_s` there, by (2.2) and `z ≥ f₄ > −23κ`.
Then `|q| = (z − f₄)/3 ≤ 85κ/3` and `z − f₄ ≥ 11κ`, so by (1.1) and (3.2), `Γ̃ ≤ Γ̂`, `|Q₁| ≤ Q̂₁` and
`|dQ₁/dz| ≤ Q̂₁/(z − f₄) ≤ Q̂₁/(11κ)` on the whole interval. Also, by (1.1),

    Δ²Q̂₁ ≤ C‖A‖^{2m−2}(λ²|f₅| + |η|κ^{1/2}λ^{3/2} + ‖B‖κλ),        Δ²Q̂₁² ≤ C‖A‖^{2m−2}(λ²f₅² + |η|²κλ + ‖B‖²κ²).       (3.4)

**Lemma Δ (the edge shift).** For `p ≥ 0` there is `C` such that for every law in `𝔏_×`, `κ ≥ 1` and `0 < r ≤ 1/κ`:

    E[|G_r − G_{−r}|(1 + |J′|)^p] ≤ C r,                                                                                 (Δ.1)
    |E[G_r + G_{−r} − 2G₀]| ≤ C r²(1 + κ).                                                                               (Δ.2)

*Proof.* Fix `χ ∈ C¹(R; [0, 1])` with `χ = 1` on `[−11, 11]`, `χ = 0` off `(−12, 12)` and `|χ′| ≤ 2`, and split
`G_s = χ(f₄/κ)G_s + (1 − χ(f₄/κ))G_s =: G_s^R + G_s^F`.

*Part R (`|f₄| < 12κ`), the bad part.* Let `𝒦 := {rQ̂₁ ≤ c_eκ}`, an event in `T`. On `𝒦^c`, bound each `|G_s^R|` by (2.2) and
`1_{𝒦^c}` by `(rQ̂₁/(c_eκ))^j`, with `j = 1` for (Δ.1) and `j = 2` for (Δ.2). By (3.4) and Lemma W₁ (`κ^aλ^s ↦ κ^{a−1−s}`):
- for (Δ.1), `rE[κΔ²Q̂₁(…)1{|z| ≥ 23κ}] ≤ Cr(κ^{−2} + κ^{−1} + 1)`;
- for (Δ.2), `r²E[Δ²Q̂₁²(…)1{|z| ≥ 23κ}] ≤ Cr²(κ^{−3} + κ^{−1} + κ)`.

*Part R on `𝒦`.* Fix `(T, ω)` with `T ∈ 𝒦`, `A < 0`, `|f₄| < 12κ`. Then the cutoff in (3.0) holds for `s = ±r` on the
support, and `G_s^R` is `χ(f₄/κ)` times `(w₀ + sβ)₊1{z ≥ 24κ + 36sQ₁}`, with `β := 12κΔ²Q₁`.
- *The edge.* For `|s| ≤ r` the map `z ↦ z − 36sQ₁(z)` has derivative `≥ 1 − 36c_e/11 > 0.98` on `[23κ, 73κ]`, and
  `|36sQ₁| ≤ 0.18κ`. So `{z ∈ [23κ, 73κ] : z ≥ 24κ + 36sQ₁(z)} = [z_e(s), 73κ]`, with a unique edge
  `z_e(s) ∈ (23.8κ, 24.2κ)`, `z_e(0) = 24κ`, and `δ_± := z_e(±r) − 24κ = ±36rQ₁(z_e(±r))`. Hence `|δ_±| ≤ 36rQ̂₁` and, by
  the mean value theorem with `|dQ₁/dz| ≤ Q̂₁/(11κ)`,

      |δ₊ + δ₋| = 36r|Q₁(z_e(r)) − Q₁(z_e(−r))| ≤ 36r·(Q̂₁/(11κ))·72rQ̂₁ ≤ 236 r²Q̂₁²/κ.                                  (3.5)

- *The integrals.* With `S(s) := ∫_{z_e(s)}^{73κ}(w₀ + sβ)₊ρ_z dz`, put `Z := 48κ`. On `[z_e(s), Z]`,
  `w₀ ≥ (Δ²/144)(5184 − 2304)κ² = 20κ²Δ² > 12c_eκ²Δ² ≥ |sβ|`, so the positive part can be dropped there. With
  `F := w₀ρ_z` and `Φ(x) := ∫_{24κ}^x F`,

      S(r) + S(−r) − 2S(0) = −[Φ(z_e(r)) + Φ(z_e(−r))] + r∫_{z_e(r)}^{z_e(−r)}βρ_z + ∫_Z^{73κ}[(w₀ + rβ)₊ + (w₀ − rβ)₊ − 2(w₀)₊]ρ_z.

  - First term: `|Φ(24κ + δ) − F(24κ)δ| ≤ ½δ²sup|F′|`. With (3.5) it is `≤ F(24κ)·236r²Q̂₁²/κ + (36rQ̂₁)²sup_{[23.8κ,24.2κ]}|F′|`.
    By (3.3), `|w₀′| ≤ κΔ²/2` and `w₀ ≤ 36κ²Δ²`, `|F′| ≤ CκΔ²(1 + ρ² + |μ_γ|²)ρ_z` there.
  - Second term: `≤ r·72rQ̂₁·12κΔ²Q̂₁·sup ρ_z`.
  - Third term: the integrand is `≤ r|β|1{|w₀| ≤ r|β|}`. Since `(Δ²/144)|72κ − z|(72κ + z) ≤ 12κrΔ²Q̂₁` there,
    `|z − 72κ| ≤ 24rQ̂₁ ≤ 0.12κ`. So this term is `≤ 48rQ̂₁·12κrΔ²Q̂₁·sup_{[71κ,73κ]}ρ_z`.

  So

      |S(r) + S(−r) − 2S(0)| ≤ C r²κΔ²Q̂₁² Σ_{x₀∈{24κ,72κ}} sup_{|z−x₀|≤κ}(1 + ρ² + |μ_γ|²)ρ_z(z).                    (3.6)

  For the first difference, between `z_e(r)` and `z_e(−r)` one of the two integrands is `0` and the other is `≤ 37κ²Δ²`
  (by (2.2)); beyond both edges `|(w₀ + rβ)₊ − (w₀ − rβ)₊| ≤ 2r|β|`. So

      ∫|(w₀ + rβ)₊1{z ≥ z_e(r)} − (w₀ − rβ)₊1{z ≥ z_e(−r)}|ρ_z dz ≤ 72rQ̂₁·37κ²Δ² sup_{[23.8κ,24.2κ]}ρ_z + 24κr∫_{23κ}^{73κ}Δ²|Q₁|ρ_z dz.   (3.7)

- *Integration.* The supremum over a slab is the quantity of Lemma W₂'s proof:
  `∫dσ(ω) sup_{|z−x₀|≤κ}(1 + ρ)^{M}ρ_z ≤ (C/κ)(1 + |O′|)^{N′}min(1, (κλ)^{−N})`, with `N′ = M + m + 2N`.
  - Then (3.6) and (3.4) give `|E[(G_r^R + G_{−r}^R − 2G₀^R)1_𝒦]| ≤ Cr²E_T[(λ²f₅² + |η|²κλ + ‖B‖²κ²)(…)min(1, (κλ)^{−N})]`, which
    is `≤ Cr²(κ^{−3} + κ^{−1} + κ)` by `E_T[λ^s(…)min(1, (κλ)^{−N})] ≤ Cκ^{−1−s}`.
  - Likewise, the first term of (3.7) contributes `≤ CrE_T[κΔ²Q̂₁(…)min(1, (κλ)^{−N})] ≤ Cr(κ^{−2} + κ^{−1} + 1)`.
  - The second term contributes `≤ 24κrE[Δ²Q̂₁(…)1{|z| ≥ 23κ}] ≤ Cκr(κ^{−3} + κ^{−2} + κ^{−1})` by Lemma W₁.
  - The weights `(1 + |J′|)^p ≤ (1 + |T|)^p(1 + ρ)^p` are absorbed in both steps.

*Part F (`|f₄| > 11κ`).* Condition on `J″ := J′ ∖ {f₄}`. By (B4), `f₄` is then `N(μ₄, σ₄²)` with `σ₄² ∈ [c, C]`. On
`{A < 0}`, `z = f₄ + 3|q|`, and `q`, `Q₁`, `P₁` and the cutoff do not involve `f₄`.
- *The Gaussian factor.* Wherever `G_s^F ≠ 0` (`|s| ≤ r`), `|z| ≤ 73κ` and `|f₄| > 11κ`, so
  `|f₄| ≥ max(11κ, 3|q| − 73κ) ≥ (κ + |q|)/3`. Hence `(1 + |f₄ − μ₄|)p₄ ≤ C exp(−c((κ + |q|)/3 − |μ₄|)₊²)
  ≤ C_N(1 + |μ₄|)^{N′}(κ + |q|)^{−N}`, and `μ₄` is linear in the other even jets. This covers the cutoff, the edges, the
  kinks and the interior term of the first difference below.
- *The cutoff.* It is common to `G_{±r}` and absent from `G₀`. Its failure costs
  `2E[G₀1{r|Q₁| > c_eκ}(1 − χ)] ≤ (C r²/κ²)E[κ²Δ²Q₁²1{24κ ≤ |z| < 72κ, |f₄| ≥ 11κ}] ≤ C_N r²κ^{−N}`. Here (1.1) bounds
  `Δ²Q₁²` by a polynomial in `|q|` and the other jets, and the Gaussian factor gives `κ^{−N}`.
- *The edges.* On `{r|Q₁| ≤ c_eκ}` the rejected set in `f₄` is `{f₄ ≥ e₊(s)} ∪ {f₄ ≤ e₋(s)}` (within the typed range), with
  `e_±(s) = ±24κ − 3|q| ± 36sQ₁`. These are exactly linear in `s`: `{e_±(r), e_±(−r)} = {e_±(0) + a, e_±(0) − a}` with
  `a := 36rQ₁`, `|a| ≤ 0.18κ`. With `ψ := 1 − χ(·/κ)`, `F_± := ψw₀p₄` and `Φ_±(x) := ∫_{e_±(0)}^{e_±(0)+x}F_±`, the upper
  edge contributes `−[Φ₊(a) + Φ₊(−a)]` to the second difference and the lower edge `+[Φ₋(a) + Φ₋(−a)]`. Each is
  `≤ a²sup_{|f₄−e_±(0)|≤|a|}|F_±′|` in absolute value, plus `r|β|·2|a|·sup ψp₄`. The kinks at `|z| = 72κ` contribute
  `≤ r|β|·96r|Q₁|·sup ψp₄`.
- `|F_±′| ≤ C[κΔ² + κ²Δ²(1 + |f₄ − μ₄|)]p₄` near the edges, since `|ψ′| ≤ 2/κ`, `|w₀′| ≤ κΔ²/2` and `w₀ ≤ 36κ²Δ²`.
- With (1.1), `Q₁²Δ² ≤ C(f₅²λ² + |η|²|q|λ + ‖B‖²q²)‖A‖^{2m−2}`, and the factor `(κ + |q|)^{−N}` absorbs every power of `|q|` and
  `κ`. So `|E[G_r^F + G_{−r}^F − 2G₀^F]| ≤ C_N r²κ^{−N}`, and in the same way `E[|G_r^F − G_{−r}^F|(1 + |J′|)^p] ≤ C_N rκ^{−N}`.

Adding Parts R and F gives (Δ.1) and (Δ.2). ∎

So the first-order effect of the edge shift is `O(r) = O(t/κ)`, that is `O(t)` per unit of the window mass `≍ 1/κ`, and the
second-order effect is `O(r²κ) = O(t²/κ)`, that is `O(t²)` per unit. In `f₄` alone the second difference would carry
`sup|p_{f₄}′|` over a shift `36rQ₁ ≍ κt`, and that costs the factor `κ`.

## 4. Proof of Theorem TL

Fix `κ ≥ 1`, `0 < r ≤ r₀ := r₄` and `k = κr ≤ 1`, and write `E_{r,k} := E_{Q̄_{r,k}}`. Then `r₀ ≤ r_0^* ≤ r_0^{[K]}`, the
radius of [K] (#220 §4).

*Step 1 (the rejected weight).* By (0.1) and Proposition RW,
`𝐓_r^{rej}(k, u) = 12p_{V_r}(v(k))(E_{r,k}[G_r] + O(r²(1 + κ)))`.

*Step 2 (the odd mean).* By (B2), `Q̄_{r,k}` and `Q̄_{r,0}` differ only in the mean `kw_r` of `O`. Let `𝕃_t` have odd mean `tkw_r`
(`0 ≤ t ≤ 1`). Then `h(t) := E_{𝕃_t}[G_r]` is smooth, with `h′(0) = kE_{r,0}[G_rℓ_r(O)]`, `ℓ_r(O) := w_rᵀΣ_{O,r}^{−1}O`, and
`|h″(t)| ≤ Ck²E_{𝕃_t}[G_r(1 + |O|)²] ≤ Ck²/κ` (the Gaussian score, as in the proof of #220 Lemma G; (2.2) and Lemma W₁). So
`E_{r,k}[G_r] = E_{r,0}[G_r] + kE_{r,0}[G_rℓ_r] + O(k²/κ)`.

*Step 3 (first order vanishes by parity).* `Q̄_{r,0}` is `𝒫`-invariant, `G_r∘𝒫 = G_{−r}` and `ℓ_r∘𝒫 = −ℓ_r`. So
`E_{r,0}[G_rℓ_r] = ½E_{r,0}[(G_r − G_{−r})ℓ_r]`, and by (Δ.1) `|kE_{r,0}[G_rℓ_r]| ≤ Ckr = Cκr²`.

*Step 4 (second order).* By parity `E_{r,0}[G_r] = E_{r,0}[G_{−r}]`, so
`E_{r,0}[G_r] = E_{r,0}[G₀] + ½E_{r,0}[G_r + G_{−r} − 2G₀] = E_{r,0}[G₀] + O(r²(1 + κ))` by (Δ.2).

*Step 5 (`r → 0` in the law).* `Q̄_{r,0}` and `Q̄_{0,0}` are centred Gaussian laws in `𝔏_×` whose covariances differ by
`O(r²)` (B2). Along the linear interpolation of the covariances, the Gaussian score (as in the proof of #220 Lemma G) and
Lemma W₁ give
`|E_{r,0}[G₀] − E_{0,0}[G₀]| ≤ Cr²sup_tE_t[G₀(1 + |J′|)²] ≤ Cr²/κ`.

*Step 6 (the prefactor).* By (B3) and #237 (R.4) (`p_{V_r}` is smooth and even in `r`),
`|p_{V_r}(v(k)) − p_{V_0}(v(0))| ≤ C(r² + k²)`, and all expectations above are `O(1/κ)`.

Collecting Steps 1–6,
`𝐓_r^{rej}(k, u) = 12p_{V_0}(v(0))E_{0,0}[G₀] + O(r²(1 + κ) + k²/κ + (r² + k²)/κ) = 𝓐^{rej}(κ, u) + O(r²(1 + κ))` by (0.2).
The constants depend on the covariance bounds of §1, which are uniform over the compact set of frames. This proves (TL). ∎

## 5. Proofs of the corollaries

**Two bounds.** For `κ ≥ 1`:
- `0 ≤ 𝐓_r^{rej}(k, u) ≤ C/κ` for all `k > 0` and `r ≤ min(k, r₀)`. This is (K2) with `1 − e ≤ 1 − 1_{cap}`, where `cap`
  is [K]'s cap event (written `G_r` in [K], and unrelated to (2.1) here): on it the elder partner of `M` is `S` ([P] §8, as
  [K] §4 uses it; the "rejected fold mass" of #220 and #229; Math-#296 (2.1)). For the `b`-integral add
  `π_r(v_r) ≤ Ce^{−c(b²+k²)}` ([R] (R5)): `r^{−2}A_r^{rej} ≤ Cπ_r(v_r)(r/k)P^N`.
- `0 ≤ 𝓐^{rej}(κ, u) ≤ C/κ`, by #242 Theorem 1 integrated in `b`.

For `κ ≤ 1`, `𝓐^{rej}(κ, u) ≤ Cκ³`: in (0.2), `G₀ ≤ 36κ²Δ²1{|z| < 72κ}`, and given the jets other than `f₄`, `|z| < 72κ` is
an `f₄`-interval of length `144κ` (B4).

*Proof of Corollary TL1.*
- On `0 < r ≤ ℓ^{1/3}` (`k ≥ 1`), the first bound gives `∫_0^{ℓ^{1/3}}Cr⁴/ℓ dr = (C/5)ℓ^{2/3}`.
- On `ℓ^{1/3} ≤ r ≤ ℓ^{1/4}`, `κ = ℓ/r⁴ ≥ 1` and `k = ℓ/r³ ≤ 1`, so (TL) applies. Its error integrates to
  `C∫(r² + ℓr^{−2}) dr ≤ C(ℓ^{3/4} + ℓ^{2/3})`. The main term is `ℓ^{1/4}∫_{ℓ^{1/12}}^1𝓐^{rej}(s^{−4}, u) ds` after `r = ℓ^{1/4}s`.
- The missing piece `ℓ^{1/4}∫_0^{ℓ^{1/12}}𝓐^{rej}(s^{−4}, u) ds` is `≤ Cℓ^{1/4}∫_0^{ℓ^{1/12}}s⁴ ds = (C/5)ℓ^{2/3}`.

Integrating over `u` gives (TL1).

*The tail criterion of Math-#296.* #296 (4.1) writes this part of the residual as `(ℓ^{1/4}/4)∫E_ℓ(κ)κ^{−5/4}dκ`, with
`E_ℓ(κ) := ∫(𝐓_r^{rej}(ℓ/r³, u) − 𝓐^{rej}(κ, u))dσ(u)` at `r = (ℓ/κ)^{1/4}`. No fold term needs subtracting, since the
rejected fold mass is `O(ℓ^{2/3})`. By (TL) and the two bounds,
- `|E_ℓ(κ)| ≤ C(ℓ/κ)^{1/2}(1 + κ)` for `1 ≤ κ ≤ ℓ^{−1/3}`;
- `|E_ℓ(κ)| ≤ C/κ` for `κ ≥ ℓ^{−1/3}`.

So for `κ̄ ≥ 1` (#296's cutoff `b`),
`ℓ^{−1/4}∫_{κ̄}^∞|E_ℓ|κ^{−5/4}dκ ≤ Cℓ^{1/4}∫_{κ̄}^{ℓ^{−1/3}}(κ^{−7/4} + κ^{−3/4})dκ + Cℓ^{−1/4}∫_{ℓ^{−1/3}}^∞κ^{−9/4}dκ ≤ C(ℓ^{1/4}κ̄^{−3/4} + ℓ^{1/6})`,
which tends to `0`. This is the `b → ∞` half of #296 (4.2).

*Proof of Corollary TL2.*
- `B_r(k) = r²∫𝐓_r^{rej}(k, u)dσ(u)`, so `J_ℓ = κ∫𝐓_r^{rej}dσ` with `κ = k/r = ℓ^{−1/5}y^{2/5}`.
- On `y ∈ [y₁, y₂]` and for small `ℓ`, `κ ≥ 1` and `k = ℓ^{1/10}y^{3/10} ≤ 1`. By (TL), `|J_ℓ − κ∫𝓐^{rej}(κ, u)dσ| ≤ Cκr²(1 + κ) ≤ 2Ck² = 2Cℓ^{1/5}y^{3/5}`.
- By #242 Theorem 1 integrated in `b` and `u`, `|κ∫𝓐^{rej}(κ, u)dσ − F̄₀| ≤ C/κ = Cℓ^{1/5}y^{−2/5}`.

The last statement is #296 (2.3). ∎

*Proof of Corollary TL3.* Put `ρ := ℓ^{2/9}`; for small `ℓ`, `ρ ≤ min(r₀, r₃, r₂′)`, where `r₃` is the radius of #237
Lemma U and `r₂′` that of [N] Proposition CE⁺⁺. By #220 §0 (at `r_0 = r_0^*`) and `cℓ^{−1/3} = ∫_0^∞∫r^{−2}𝐀₀`, with
`𝐀₀ := ∫A₀ db`,

    ν_eld − cℓ^{−1/3} − ν_eld^{far,r_0^*} = 𝒦₁ − 𝒦₂ + I^{eld} + J₄,                                                     (5.1)

where:
- `𝒦₁ := ∫_0^ρ∫(𝐓_r − r^{−2}𝐀₀)(ℓ/r³, u)dσ dr`;
- `𝒦₂ := ∫_0^ρ∫𝐓_r^{rej}(ℓ/r³, u)dσ dr`;
- `I^{eld} := ∫_ρ^{r_0^*}∫𝐓_r^{eld}dσ dr`, where `𝐓_r^{eld} := ∫r^{−2}A_r^{eld}db`;
- `J₄ := −∫_ρ^∞∫r^{−2}𝐀₀ dσ dr`.

On `[0, ρ]` this uses `𝐓_r^{eld} = 𝐓_r − 𝐓_r^{rej}`. The four terms:
- *`𝒦₁`.* For `r ≤ ρ ≤ ℓ^{1/5}`, `k = ℓ/r³ ≥ r²`, so #237 Lemma U applies, and #237 §5's main-term computation with `ρ` in
  place of its split gives `𝒦₁ = c₂ℓ^{1/3} + I^{cand}ℓ^{1/4} + O(ρ³ + ℓ^{2/3} + ℓ²ρ^{−5} + ℓ²ρ^{−7})`. Here
  `ρ³ = ℓ^{2/3}`, `ℓ²ρ^{−5} = ℓ^{8/9}` and `ℓ²ρ^{−7} = ℓ^{4/9}`.
- *`𝒦₂`.*
  - On `[0, ℓ^{1/4}]`, use (TL1).
  - On `[ℓ^{1/4}, ρ]`, `κ ≤ 1`. There (CE⁺⁺.1) of [N] and (C⁺.1) of #229 give
    `|r^{−2}A_r^{rej}(b, κr, u) − 𝒜^{rej}(b, κ, u)| ≤ Cr(1 + |b|)^Ne^{−cb²}`, which integrates to `O(ρ²) = O(ℓ^{4/9})`.
  - The main terms add up to `ℓ^{1/4}∫_0^{ρℓ^{−1/4}}∫𝓐^{rej}(s^{−4}, u)dσ ds`. This is `(I^{cand} − c₁)ℓ^{1/4}` (#242 §0) minus
    a tail `≤ Cℓ^{1/4}∫_{ρℓ^{−1/4}}^∞s^{−12}ds = O(ℓ³ρ^{−11}) = O(ℓ^{5/9})`.
- *`I^{eld}`.* `I^{eld} = O(ℓ^{4/9}log(1/ℓ))` by #229 §5 (on `[ℓ^{2/9}, r_0^*]`, through (W⁺.2) and Lemma S′).
- *`J₄`.* `0 ≤ r^{−2}𝐀₀ ≤ Cκ²`, so `|J₄| ≤ Cℓ²ρ^{−7} = O(ℓ^{4/9})`.

So (5.1) is `c₁ℓ^{1/4} + c₂ℓ^{1/3} + O(ℓ^{4/9}log(1/ℓ))`, which is (TL3.1). Subtracting (TL3.1) from #237 (P.1) gives (TL3.2).
For the SIDE24 form, divide by `cℓ^{−1/3}`: `ℓ^{4/9}/ℓ^{−1/3} = ℓ^{7/9}`, and #229's remainder gave `ℓ^{3/7+1/3} = ℓ^{16/21}`. ∎

*The ledger of (5.1)* (exponents of `ℓ` at `ρ = ℓ^{2/9}`):

| Term | Source | Exponent |
|---|---|---|
| `ℓ²ρ^{−7}` | the cusp tail of `𝒦₁`; `J₄` | **4/9** |
| `ρ²` | (CE⁺⁺.1), (C⁺.1) on `[ℓ^{1/4}, ρ]` | **4/9** |
| `I^{eld}` | #229 §5 | **4/9**, with `log(1/ℓ)` |
| `ℓ³ρ^{−11}` | the tail of `∫𝓐^{rej}` | 5/9 |
| `ρ³`, `ℓ^{2/3}` | Lemma U; TL1 (fold mass, (TL)'s error, the missing piece) | 2/3 |
| `ℓ^{3/4}` | (TL)'s `r²` part | 3/4 |
| `ℓ²ρ^{−5}` | the finite part of `𝐀₂` | 8/9 |

The split `ρ = ℓ^{2/9}` balances `ρ²` against `ℓ²ρ^{−7}`, so moving it cannot improve `4/9`: a larger `ρ` raises `ρ²`, a
smaller one raises `ℓ²ρ^{−7}`. Removing the `ℓ^{4/9}` rows needs the `κ → 0` side: an elder (hence rejected) cusp-kernel
error better than `O(r)` uniformly on `κ ≤ 1`, and a sharper intermediate elder bound. That is TAIL-S.

## 6. Remarks

1. **Relation to (TL_a) and to the TAIL-L record of main#259.**
   - (TL) is (TL_a) of 6001580409 with `a = 2`, after the `b`-integral. In Sol's form (6001189633 §2) it is `p = 1`. That
     answers, for the birth-integrated kernel, the "no sourced `p`" of agent 8's obstruction (6001319075).
   - 6001580409 said that a proof must decide the elder mark on #242's soft localization `λ₁ ≈ γ₁²/κ` at `r > 0`, and that
     Theorem N's Step N1 excludes that region through `λ ≥ λ₃ ≳ κr`. The first point holds. The second describes [N]'s
     proof as written, not its lemmas: Lemma GE shows that the soft localization lies in the good event as soon as
     `γ₁² ≳ 𝒩k`, because every margin that Lemmas Q′, Q″ and R₂ need has the form `λ ≳ 𝒩r(…)(1 + |f₄|/κ)`.
   - The decision there is [N]'s Lemma Q″. Its first-order edge shift `rQ₁/(2κ)` is `≈ 3φ²t` on the soft layer, which is
     #242's `φ_e = 1/3 + t/3 + …` at `φ = 1/3`. The second-order terms are bounded here, not expanded. So (TL) does not
     compute the `k²/κ` term.
2. **Sharpness of the order** (a remark from cited results, not a statement of this note).
   - At fixed `k > 0`, #243 Theorem FL, with dominated convergence in `b` ((K2) and [R] (R5)), gives
     `κ𝐓_r^{rej}(k, u) → ∫F(k; b, u)db` as `r ↓ 0`. #242 Theorem 1 gives `κ𝓐^{rej}(k/r, u) → ∫F₀(b, u)db`. So
     `κ(𝐓_r^{rej}(k, u) − 𝓐^{rej}(k/r, u)) → ∫(F − F₀)(k; b, u)db`.
   - In #242's model case (the Gaussian kernel on `R^d`), Proposition 4 gives `F = F₀H(k)` with
     `H(k) − 1 = (12/25)k² + O(k³) ≠ 0`. #243 Remark 1 records that the torus field's jets differ from the model's in law
     by `O(e^{−L²/8})` (#242 §0). This note does not prove the transfer of `H` to the torus field.
   - If the limit is nonzero for the field at hand (as in the model case), then the `κr² = k²/κ` part of (TL) cannot be
     replaced by `o(κr²)` uniformly. That part carries `R_{2/3}` (#242 Lemma 5).
3. **`d ≥ 3`.** The proof of Theorem TL uses neither the eigenframe of `A` nor #242's Proposition 2′, and no lower bound on
   the stiff eigenvalues: `λ = λ_min(−A)` and (1.1) suffice. Configurations with several soft eigenvalues are covered by
   Lemmas W₁, W₂ and Δ, because the radial parametrization of `γ` does not single out a direction. (The corollaries also
   use #242 Theorem 1, whose proof works in the eigenframe.)
4. **What remains of IBA2-009 (TAIL-S).**
   - For `κ ≤ 1` the best elder-kernel (hence rejected-kernel) error on file is `O(r)` ((CE⁺⁺.1), (C⁺.1)), which over
     `[ℓ^{1/4}, ρ]` gives `ρ²`. (The candidate kernel has `O(r²)` there after the `b`-integral, by #237 Lemma U.)
   - The intermediate elder mass is `O(ℓ^{4/9}log(1/ℓ))` (#229).
   - Neither is `o(ℓ^{1/2})`. Agent 3's TAIL-S obstruction (6001313460) stands, and so does Math-#296's matching
     criterion at `a → 0`.
5. **Consistency.**
   - On compact `κ`-windows inside `[1, ∞)`, (TL) implies the `b`-integral of the difference of [N] (N.2) and (N.1), which
     is the rejected kernel's.
   - (TL3.1) implies the expansions of #229 (E3⁺.0) and #220 (E3.0), with a smaller remainder; their bounds on the far
     term are separate inputs (#187; #198 Lemma F′). (TL3.2) implies #229 (R⁺.1).
   - With #242 Theorem 1, (TL) gives #296's band limit (TL2), which is the value #296 §5 asked to determine.
6. **Constants.** No constant is certified, and the ones implied are large. In (Δ.2) the dominant part comes from the
   cutoff `r|Q₁| ≤ c_eκ`: the Chebyshev step on `𝒦^c` costs a factor `∝ 1/c_e² = 4·10⁴`. In an author-side quadrature for
   one `m = 1` law in `𝔏_×`, the ratio `|E[G_r + G_{−r} − 2G₀]|/(r²(1 + κ))` reached about `4·10⁴` at some `(r, κ)`, against
   about `1` in the limit `r → 0` at fixed `κ`. The relative error `O(k²)` of Theorem TL carries constants of this kind.

## 7. Exact controls (`tl_exact.py`; stdlib; exact rationals; deterministic; byte-identical under `-O`)

The script and its expected stdout are published in the controls comment that follows this note.

- **T1** (1.1) on matrices `A = −O diag(λ)Oᵀ`, built from rational eigenvalues and rational orthogonal `O` (Cayley
  transforms), with rational `γ` in `m = 1, 2, 3`. Checked: `Γ̃² ≤ |q|/λ` and `Δ²Γ̃^{2j} ≤ λ^{2−j}|q|^j‖A‖^{2m−2}`
  (`j = 0, 1, 2`, with `‖A‖ = λ_max`), squared where needed.
- **T2** the radial parametrization:
  - `z − f₄ = 3ρ²μ` and `dz/dρ = 2(z − f₄)/ρ` as polynomial identities;
  - (3.1) on rational data;
  - `|c₁|ρ ≤ |η|Γ̃/12` and `|c₂|ρ² ≤ ‖B‖Γ̃²/8`;
  - (3.2), with the derivative computed exactly, and `μ ≤ |ω|²/λ`.
- **T3** Lemma W₂'s constants: `z − f₄ ≥ 7κ` on both slabs; `ρ₊²/ρ₋² ≤ 41/7` (indeed `≤ 15/7`).
- **T4** constants of §§2–3:
  - the derivative bound `1 − 36c_e/11 > 49/50`;
  - the edge interval `(23.8κ, 24.2κ)`;
  - `36·72/11 ≤ 236`;
  - `w₀ ≥ 20κ²Δ²` on `[z_e, 48κ]` and `20 > 12c_e`;
  - the kink window `1728/72 = 24` and `24c_e ≤ 0.12`;
  - `|w₀′| ≤ κΔ²/2` on `[23.8κ, 24.2κ]`;
  - the support bound `z² < 5184κ² + 1728c_eκ²`, so `|z| < 73κ`, and `85κ/3`, `41κ/3` as the bounds for `|q|`;
  - `36 + 12c_e ≤ 37` in (2.2);
  - the arithmetic `440·72 = 31680`, `175/4 ≤ 44` and `131³ ≥ 175²·72` of Lemma GE (b);
  - the piecewise-linear tail bounds `max(11κ, 3|q| − 73κ) ≥ (κ + |q|)/3` and `max(11κ, 3|q| − 25κ) ≥ (κ + |q|)/3`
    (Part F) and `max(13κ, 3|q| − 25κ) ≥ (κ + |q|)/2` (Proposition RW), exactly at the kink and by the final slope.
- **T5** the exponent lists:
  - every `κ^aλ^s` term of §2's table and of §3's second differences, through `κ^{a−2−s}` (W₂) or `κ^{a−1−s}` (W₁), is
    `≤ κ`;
  - every term of §3's first differences ((3.7), and the `𝒦^c` part) is `≤ κ⁰`: `(2, 2), (5/2, 3/2), (3, 1)` through W₂
    and `(1, 2), (3/2, 3/2), (2, 1)` through W₁;
  - every bad-event term `r^aκ^b` of §2 is `≤ r²max(1, κ)` on `1 ≤ κ ≤ 1/r`. This holds iff `a ≥ 2` and `b ≤ a − 1`,
    because the ratio is log-linear in `log κ`.

  The `(a, s)` lists are transcribed from §§2–3, not derived from the weights by the script.
- **T6** the corollaries, in exact exponent arithmetic, with each integral's exponent derived from its endpoints:
  - TL1: `ℓ^{2/3}` (the part `k ≥ 1`, `(TL)`'s `ℓr^{−2}` part, the missing piece) and `ℓ^{3/4}` (`(TL)`'s `r²` part);
  - the #296 tail bound `ℓ^{1/4}κ̄^{−3/4} + ℓ^{1/6}`, from the integrands `ℓ^{1/4}κ^{−7/4}`, `ℓ^{1/4}κ^{−3/4}` and
    `ℓ^{−1/4}κ^{−9/4}` and the cut `κ = ℓ^{−1/3}`;
  - TL2: `κ = ℓ^{−1/5}y^{2/5}`, `k² = ℓ^{1/5}y^{3/5}`, `1/κ = ℓ^{1/5}y^{−2/5}`, and the band remainder `ℓ^{7/10}`;
  - TL3's ledger at `ρ = ℓ^θ`: the rows `ℓ²ρ^{−7}`, `ρ²`, `ℓ³ρ^{−11}` and `ℓ^{3/4}` derived from their integrals; the rows
    `I^{eld}` (`4/9`, #229 §5), `ρ³` and `ℓ²ρ^{−5}` (#237 §5) recorded from the cited sources. At `θ = 2/9` the least
    exponent is `4/9`, attained exactly by the three bold rows, and `θ = 2/9` balances `ρ²` against `ℓ²ρ^{−7}`;
  - SIDE24's `7/9` against `16/21`.
- **T7** Lemma Δ's edge mechanism on explicit models. Take a positive quadratic density `ρ_z` on `[23κ, 73κ]` and
  `Q₁(z) = c₀ + c₂′(z − f₄)`, an affine rational stand-in for (3.1) (no `c₁ρ` term). Then `z_e(s)` is rational, and
  `S₁(s) := ∫_{z_e(s)}^{48κ}(w₀ + sβ)ρ_z dz` is an exact rational integral. On a grid of rational parameters (`κ ∈ {1, 3, 10}`,
  `f₄ ∈ {−12κ, 0, 12κ}`, two values of `Δ²`, three of `(c₀, c₂′)`, and `r`, `r/2`, `r/4` with `rQ̂₁ = c_eκ/2`), the script checks:
  - `|δ_±| ≤ 36rQ̂₁` and `|δ_±| < κ/5`;
  - the identity `δ₊ + δ₋ = 36r(Q₁(z_e(r)) − Q₁(z_e(−r)))` (true by construction of `z_e`) and (3.5) with the model's exact
    Lipschitz constant `|c₂′|`;
  - `|S₁(r) + S₁(−r) − 2S₁(0)| ≤ F(24κ)|δ₊ + δ₋| + ½(δ₊² + δ₋²)sup|F′| + r|δ₊ − δ₋|sup|βρ_z|`, the inequality behind
    (3.6), with exact polynomial upper bounds for the suprema over `[23.8κ, 24.2κ]`;
  - the signed first difference `|S₁(r) − S₁(−r)|` against a bound of the form (3.7), with `sup|w₀ + rβ|` in place of
    `37κ²Δ²`.

  T7 does not model the `c₁ρ` term, the kink at `72κ` (its integrals stop at `48κ`), or the absolute first difference.

**Not covered by any control** (checked by hand, and by the referees' own computations recorded in the review):
the parity `G_s(E, −O) = G_{−s}(E, O)`; `ρ_z` and (3.3); (3.4); the envelope bounds for the true radial `Q₁`; the identity
for `S(r) + S(−r) − 2S(0)` with its kink term; Part F; the analytic content of §2 (Lemma GE, Proposition RW) and of §§4–5
(Steps 1–6, the two bounds of §5, the Jacobians of TL1–TL2, (5.1) and the identification with `I^{cand} − c₁`).

Mutants, each breaking one control:
- `M1` T2: `dz/dρ = (z − f₄)/ρ`.
- `M2` T1: `Γ̃² ≤ |q|λ`.
- `M3` T4: `z − f₄ ≥ 12κ` on the edge range.
- `M4` T6: `ρ = ℓ^{1/5}` in TL3, so the least exponent becomes `2/5`.
- `M5` T6: `κ = ℓ^{−1/5}y^{−2/5}` in TL2.
- `M6` T3: the slab `|f₄| ≤ 17κ`.
- `M7` T7: `δ₊ + δ₋` computed with `Q₁(z_e(r)) + Q₁(z_e(−r))`.
- `M8` T4: the kink window `12rQ̂₁`.
- `M9` T5: a first-difference row `(3, 1)` replaced by `(3, 0)`.
- `M10` T4: the window tail bound with `9κ` in place of `11κ`.

Each mutant exits `1` with empty stdout and `FAILED: <group>` on stderr. An unknown mutant label, a missing label, or an
extra argument exits `2`.

## 8. Review slices

- **A** §§0–1: the setting and (0.1)–(0.2), facts (B1)–(B5) against #237 Lemma R and #218, Lemma W₁, Lemma W₂ (polar
  coordinates, the slab, the dyadic layers), and (1.1).
- **B** §2: the good event, Lemma GE (each margin of [N]'s Lemmas Q′, Q″, R₂ with `λ₄`) and Proposition RW (the four bad
  events and the edge set, with its table).
- **C** §3: Lemma Δ. Parts R (the radial parametrization, the edge, (3.5)–(3.7), the integration) and F (the cutoff, the
  edges and kinks in `f₄`).
- **D** §§4–5 and §7: the assembly (Steps 1–6), Corollaries TL1–TL3 and the #296 tail bound, the ledger, and `tl_exact.py`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_