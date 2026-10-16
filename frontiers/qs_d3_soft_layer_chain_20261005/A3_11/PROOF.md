## QS addendum A3.11: the `d = 3` decision on dyadic windows — fixed-layer errors `O(r⁴log(1/r))`, and the failure-measure rate `r^β` for every `β < 1`, endpoint `O(r⁴log(1/r)⁷)`

**Object.** `CL-QS-A3-11-DYADIC-WINDOWS-20261006-v1`.

**Who.** Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`, the author of QS and A3–A3.10. Dylan Roy — delegated AI work. Author-side. Scientific effect: NONE.

**Claim.** [6009293688](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6009293688); this delivery releases it.

**What this is.** A3.7 Remark 1 and A3.8 Remark 1 name the strict obstruction at the exponent `2/3`: the radius tail `w^{−8}` (A3.6's Lemma Rad₃) against the window error `e = rw⁴` (A3.5's (FW.0) and (D₃)), both through *one deterministic window* `w`, balanced at `w = r^{−1/12}`. A3.7 Remark 2 names the way out — read each pair on a window of its own raw radius — and the reason it was not taken: the decision bands then have widths that depend on the fibre variable `ψ`, which C82's Theorem LB does not allow (C82 §5). This note takes that way out with deterministic windows after all. The layer is cut into dyadic shells `w_{j−1} ≤ ρ_• < w_j`, `w_j = 5·2^j ≤ r^{−3/16}`; the pairs of shell `j` are read on the window `w_j` (deterministic, so A3.5–A3.7's machinery applies verbatim), and the shell's decision bands are paid with a *localized* form of C82's theorem: C82 §3's coarea density `48(ψ² − c²)/Z² ≤ (4/3)ψ³` on the saddle branches, restricted to the sub-layer `λ̃ ≤ 4Θ_•(γ)/w_{j−1}²` that the shell lives in (A3.6, proof of Rad₃), gives the fibre bound `192·x·U³` (Lemma 1.1) in place of A3.7's `x·Ł`. Each shell then costs `O(r/w_{j−1}²)` for its bands and `O(r)` for its margins, and the shell sums are `O(r)` and `O(r log(1/r))`. There is no radius tail except at the top window, where it is `O(r^{3/2})`.

The results: on every fixed layer `Q_r^W(D_Λ ∩ (H_r Δ E)) ≤ C_Λr⁴log(1/r)` (Theorem BL₃″; A3.7: `r^{11/3}`); with A3.8's exhaustion, `‖ν_r^F − ν_0^F‖_var ≤ C_βr^β` for every `β < 1` (Theorem QFE₃′; A3.8: `β < 2/3`) and `1 − p_r = r³α^{(3)} + O(r⁴log(1/r)⁷)` (Theorem ER₃′; A3.8: `r^{11/3}log(1/r)^{8/3}`); and, through A3.9 and A3.10 unchanged, `ν_rej^{B,K}(ℓ) = C_fail^{(3)}ℓ^{2/3} + O(ℓ log(1/ℓ)⁷)` with its cumulative, moment and fraction corollaries (Corollary PD₃′). The coefficient `α^{(3)} = F/(kA_0)` is A3.9's; nothing changes in it. The new mathematics is Lemma 1.1 and the shell bookkeeping of §§2–3; everything else is A3.5–A3.8 read shell by shell.

**Consumed.**
- *Merged or reviewed.* [P] (`imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d`) and [R] (`frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf`) exactly where A3.8–A3.10 use them. C82 ([5959920397](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5959920397), Codex; my cross-provider review [5961696684](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5961696684), ACCEPT) §§2–3: the branch structure of the extra saddles of the sheared cubic and the coarea density bound. These are intermediate statements of C82's proof of Theorem LB, which the review reconstructed line by line; Lemma 1.1 uses them and not Theorem LB's statement.
- *Author-side, each read in all its slices by nonauthor lanes* (same GitHub account, organizational-independence credit 0; verdicts PASS / PASS_SCOPED, with successor texts where AMENDs were issued; A3.8's three slices and its successor text are recorded in [6008843064](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6008843064), A3.9's read in [6009099266](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6009099266)). A3.4 ([5999129544](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5999129544) with [5999301338](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5999301338)), A3.5 ([6001191875](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6001191875)), A3.6 ([6002480647](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002480647)), A3.7 ([6004622009](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6004622009)), A3.8 ([6007704303](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6007704303) with [6008104016](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6008104016)), A3.9 ([6008067902](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6008067902)) and A3.10 ([6008550120](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6008550120); read PASS [6009306797](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6009306797)). The lemmas used are named at each step; A3.8's `H`-ledgers (its Lemmas 1.1–1.3, 2.1–2.4, 3.1–3.2, 4.1–4.2 and 5.1–5.4) are used as stated.
- Everything below is conditional on A3.3–A3.8 at their stated scopes — on A3.4 (through it A3.3) for every weighted statement, and directly on A3.5's Lemmas FW₃, D₃, T₃, E₃⁺, A3.6's Theorem E₃(a), Lemma M₃ and Rad₃, A3.7's Lemmas LE₃, B₃, Corollary LE₃ and its §5, and A3.8's Lemmas 1.1–1.3, 2.1–2.4, 3.1–3.2, 4.1–4.2 and 5.1–5.4 (the certificates of A3.6 and A3.7 are deterministic); §5 is in addition conditional on A3.9 and A3.10 at their stated scopes.

### 0. Setting and notation

- **As in A3.8 §0.** `d = 3`; the pins; `Q_r`, `W_r`, `Z_r = r²z_r`, `Q_r^W`; the spectral coordinates `ϑ = (λ̃, λ₂, θ, t)` on `X := ℝ × ℝ × [0, π) × ℝ⁹` (A3.8's successor text); the jets `γ, B, C₃`, `Y`, `a_M`, `a_S`, `w_λ = (a_M)₊(a_S)₊`; `T`, `P = 1 + |λ₂| + |t|`, the field norm `N ≥ 1`; `D, J, ψ, c, R`, `P_QS`; `μ`, `Y*`, `h_Y`; `E`, `Rsec`; the raw radii `ρ_E = 3/2 + (5/2)(|γ| + 12)/√(24λ̃)` and `ρ_R = 5/2 + (17/6)(|γ| + 12)/√(24λ̃)` (A3.6 §0); `𝔉`, `Ω_w`, `ℰ`, `G`, `G_k`, `(B_r) = (B_r(w)) := {λ₂ > C_BkN²rw⁴}`, `ℋ_M = ℋ_M(w)`, `ℋ_S = ℋ_S(w)` (A3.5; the window `w` is now displayed, since several windows are in play); `e(w) := rw⁴`, `η_LE(w) := 2K₂rw²`; `H_r`, `F_r := H_r^c`, `p_r := Q_r^W(H_r)`; the constants `K₀, K₂, C_B, C_e, D_h, C_h, K₀^{[P]}`.
- **The layer and the measures** (A3.8 §0). `Λ ≥ 1`, `H := 1 + Λ`, `D_Λ`, `A_* := 12Λ`; `μ_r(V) := r^{−5}E_{Q_r}[W_r1_V1_{D_Λ}]`, so `Q_r^W(V ∩ D_Λ) = r³μ_r(V)/z_r`; `μ₀ := g₀dϑ`; `U_T := D_Λ ∩ T ∩ {γ ≠ 0}`; `Rsec^{(∞)}`, `E^{(∞)}`; `ν_r^F`, `ν_0^F`, `m_R^{(∞)}`, `α^{(3)} := m_R^{(∞)}/z₀`; the variation norm without the factor `1/2`.
- **Standing conditions** (A3.8 (0.1)):

      0 < r ≤ r₀,    Λ ≥ 1,    rH ≤ 1,    rH⁴ ≤ 1,                                                          (0.1)

  and in addition `r ≤ e^{−1}` wherever `log(1/r)` appears. Constants `C, c` depend only on `L`, `B₀`, `k_±` and the stated moment orders; never on `Λ`, `r`, `b`, `k`, the frame or a window. The dependence on `Λ` is displayed as a power of `H`.
- **The radius sub-layers** (A3.6, proof of Lemma Rad₃, step 1). With `Θ_E(γ) := (25/96)(|γ| + 12)²` and `Θ_R(γ) := (289/864)(|γ| + 12)²`, for `w ≥ 5`

      {ρ_• ≥ w} ⊂ {λ̃ ≤ U_•(γ, w)},      U_•(γ, w) := min(Λ, 4Θ_•(γ)/w²)       (• ∈ {E, R}),                 (0.2)

  because `ρ_E ≥ w` is `λ̃ ≤ Θ_E/(w − 3/2)²`, `ρ_R ≥ w` is `λ̃ ≤ Θ_R/(w − 5/2)²`, and `w − 5/2 ≥ w/2` for `w ≥ 5`. On `T`, `λ̃ > 0`. Note `Θ_•(γ) ≤ 289(1 + |t|)²/6 ≤ 49P²`, since `|γ| ≤ |t|` and `(|t| + 12)² ≤ 144(1 + |t|)²`; so every polynomial in `Θ_•(γ)` is absorbed by the Gaussian factor of the densities, as in A3.6.
- **The windows and the shells.** Put

      w_max := r^{−3/16},    w_j := 5·2^j  (j ≥ 0),    J := max{j : w_j ≤ w_max},                               (0.3)

  so that `w_J ≤ w_max < 2w_J` and `J + 1 ≤ 1 + (3/16)log₂(1/r) ≤ 2log(1/r)` for `r ≤ e^{−1}`. The largest errors in play are `e(w_J) ≤ e_max := rw_max⁴ = r^{1/4}` and `η_LE(w_J) ≤ η_max := 2K₂rw_max² = 2K₂r^{5/8}`. For `• ∈ {E, R}` the shells are

      S_0^• := {ρ_• < w_0},      S_j^• := {w_{j−1} ≤ ρ_• < w_j}  (1 ≤ j ≤ J),      S_top^• := {ρ_• ≥ w_J};         (0.4)

  they partition the sector. By (0.2), `S_j^• ⊂ {λ̃ ≤ U_•(γ, w_{j−1})}` for `1 ≤ j ≤ J`. The pairs of shell `j` are read on the window `w_j`: on `S_j^•`, `ρ_• < w_j`, and `w_j ≥ 5`, `r^{1/2}w_j ≤ r^{1/2}w_max = r^{5/16} ≤ 1`, `e(w_j) ≤ r^{1/4} ≤ 1`, `η_LE(w_j) ≤ 1` for `r ≤ r₁ := min(r₀, e^{−1}, (2K₂)^{−8/5}, 5^{−16/3})` (the last makes `w_max ≥ 5`). Throughout, `r ≤ r₁`.

### 1. The localized band (Lemma 1.1 deterministic; the rest conditional on A3.4)

**Lemma 1.1 (C82's density, localized).** Fix `(λ₂, θ, t)` with `λ₂ > 0` and `γ ≠ 0`. For every `U > 0` and every `x > 0`,

    ∫ 1_T 1{λ̃ ≤ U} 1{|μ| ≤ x} w_λ dλ̃ ≤ 192 x U³,                                                              (1.1)

and the left side without the band indicator is at most `12U³`.

*Proof.* On the fibre `c` and `R` are fixed, `ψ = 24λ̃/γ²`, `T` is `{ψ > |c|}` (with `λ₂ > 0`), and `w_λdλ̃ = (γ⁶/384)(ψ² − c²)dψ` (A3.6 (1.1)). The sub-layer is `{|c| < ψ ≤ ψ_U}` with `ψ_U := 24U/γ²`.
1. **No band.** `∫_{|c|}^{ψ_U}(ψ² − c²)dψ ≤ ψ_U³/3`, and `(γ⁶/384)(24U/γ²)³/3 = 12U³`.
2. **`x ≤ 1/2`, C82's branches.** C82 §2 shows that the extra nondegenerate saddles of `P_QS` form at most two branches, each a `C¹` curve parametrized by `ψ` on an interval, along which `v := P_QS(Y) + 1` is strictly decreasing with `dv/dψ = −Z²/48` (the envelope identity; `Z ≠ 0` on a branch). C82 §3 shows that on each branch, wherever `v ≤ 1/2`, the coarea density is bounded by

       (ψ² − c²)|dψ/dv| = 48(ψ² − c²)/Z² = ψ³(1 − ρ²)/(3x_C) ≤ (4/3)ψ³,

   in C82's variables `ρ = c/ψ`, `x_C = ψZ²/144` (C82 (12)–(14): (12) for `v ≤ 0`, (13) for `0 ≤ v ≤ 1/2`, and (14) is the density bound). The exceptional values `c = 0` and `R = 0` are covered by C82 §2 (one branch, `v = 1 − 16ψ³/R²` when `c = 0`; no saddle when `c = R = 0`). Since `μ` is the maximum of `v` over the extra nondegenerate saddles, `{|μ| ≤ x} ⊂ ⋃_{branches}{|v| ≤ x}`. On a branch, `v` is monotone, so `{|v| ≤ x}` is an interval of the branch, and the change of variables `ψ → v` gives

       ∫_{branch} 1{ψ ≤ ψ_U}1{|v| ≤ x}(ψ² − c²)dψ = ∫_{|v|≤x} 1{ψ(v) ≤ ψ_U}(ψ² − c²)|dψ/dv| dv ≤ 2x·(4/3)ψ_U³,

   using the density bound (valid since `|v| ≤ x ≤ 1/2`) and `ψ(v) ≤ ψ_U` on the integrand's support. Two branches give `(16/3)xψ_U³`, and `(γ⁶/384)(16/3)x(24U/γ²)³ = 192xU³`.
3. **`x > 1/2`.** Drop the band: `12U³ ≤ 24xU³ ≤ 192xU³`. ∎

C82's Theorem LB bounds the whole fibre band by `x·(1024/3)|c|³ + 64xR²` through the *global* bound `ψ³ ≤ 64|c|³ + 12R²` on the band; (1.1) replaces that global bound by the sub-layer's own `ψ_U³`. For a narrow sub-layer this is far smaller (the `c = 0` slice: the band sits at `ψ³ ≈ R²/16`, so for `ψ_U³ < R²(1 − x)/16` the left side of (1.1) is zero, while C82's exact mass (4) of the whole band is `xR²/24`). The width `x` is deterministic on the fibre, as C82 §5 requires; the localization is a restriction of the domain of integration only.

**Lemma 1.2 (sub-layer moments and edge integrals).** Under (0.1), for `w ≥ 5`, `• ∈ {E, R}`, the sub-layer `S := T ∩ {λ̃ ≤ U_•(γ, w)}`, fixed `m, q ≥ 0`, `i ∈ {M, S}`, and nonnegative measurable `φ`:

    μ_r(N^mP^q1_S) ≤ C_{m,q}(w^{−8} + rH⁶w^{−4}),                                                              (1.2)
    μ_r(N^mP^q1_Sφ(a_i)) ≤ C_{m,q}∫₀^∞φ(s)(w^{−4}s + rH⁶w^{−2})ds,                                             (1.3)
    μ_r(N^mP^q1_Sφ(a_i, λ₂)) ≤ C_{m,q}∫₀^∞∫₀^∞φ(y, λ₂)λ₂(w^{−4}λ₂²y + rH⁶w^{−2})e^{−cλ₂²}dy dλ₂.                 (1.4)

*Proof.* A3.8's Lemmas 2.1 and 2.2 with the `λ̃`-range `(0, U]`, `U := U_•(γ, w) ≤ 4Θ_•(γ)/w²`. By (J₃.18), A3.8's (1.1)–(1.2) and `(λ₂ − rλ̃/k)₊ ≤ λ₂` on `T`, the density is at most `Cλ₂e^{−c(λ₂²/2 + |t|²)}[λ₂²w_λP^{m} + rH⁶P^{m+25}]P^q`. Change variables from `B` to `s = a_i` (Jacobian at most `1/(3k₋)`); on `T`, `0 < s < 12λ̃` and `w_λ = s(12λ̃ − s)`.
- (1.2): `∫₀^U∫₀^{12λ̃}[λ₂²s(12λ̃ − s) + rH⁶]ds dλ̃ = 72λ₂²U⁴ + 6rH⁶U²`, as in A3.8 Lemma 2.2, with `U⁴ ≤ 256Θ_•⁴/w⁸` and `U² ≤ 16Θ_•²/w⁴`; the Gaussian absorbs `Θ_•(γ)^4P^{m+q+25}`.
- (1.3): for fixed `s`, `∫_{s/12}^{U}(12λ̃ − s)dλ̃ = (12U − s)²/24 ≤ 6U² ≤ 12U² ≤ 192Θ_•²/w⁴` and `∫_{s/12}^{U}dλ̃ ≤ U ≤ 4Θ_•/w²`; so the integrand becomes `Cλ₂[λ₂²Θ_•²w^{−4}s + rH⁶Θ_•w^{−2}]e^{−c(…)}` and the Gaussian absorbs the rest (A3.8 Lemma 2.1's proof, with `12U²` for its `12Λ·Λ` and `U` for its `Λ`).
- (1.4): the same with `λ₂` kept in the integrand (A3.5's proof of (E₃⁺)). ∎

The right sides of (1.3)–(1.4) are A3.8's (2.1)–(2.2) with `(H², rH⁷)` replaced by `(w^{−4}, rH⁶w^{−2})`: on a sub-layer of a narrow shell the weight `w_λ` is small and the layer is short.

**Lemma 1.3 (the sub-layer correlated band, with `H`).** Under (0.1), for `w ≥ 5`, `• ∈ {E, R}`, `S_T := U_T ∩ {λ̃ ≤ U_•(γ, w)}` and fixed `p, q ≥ 0`:
- **(a)** for every `δ > 0`, `μ_r(N^pP^q1_{S_T}1{|μ| ≤ δ}) ≤ C_{p,q}(δw^{−6} + rH⁶w^{−2})`;
- **(b)** for every `δ > 0`, `μ_r(N^pP^q1_{S_T}1{λ₂|μ| ≤ δ}) ≤ C_{p,q}(δw^{−6} + rH⁶w^{−2})`.

Neither bound needs a width at most `1/2`: Lemma 1.1 holds for every `x`, because a wide band on a sub-layer costs at most the sub-layer itself, `12U³ ≤ 24xU³`. (A3.8's Lemma 3.1 needed `δ ≤ 1/2` and `λ₂ ≥ 2δ` because the whole layer costs `Λ³`.)

*Proof.* A3.8's Lemma 3.1 with Lemma 1.1 in place of C82's Theorem LB. By (J₃.18), A3.8's (1.1)–(1.2) and `(λ₂ − rλ̃/k)₊ ≤ λ₂` on `T`, the density is at most `Cλ₂e^{−c(λ₂²/2 + |t|²)}[λ₂²w_λP^p + rH⁶P^{p+25}]P^q`, and only `w_λ` depends on `λ̃`. The remainder term, with the indicators bounded by `1` and `λ̃ ∈ (0, U]`, integrates to `CrH⁶U ≤ CrH⁶w^{−2}` (Gaussian in `Θ_•`). For the main term, on the fibre `(λ₂, θ, t)` the quantity `U = U_•(γ, w)` is a constant (it depends on `γ`, a function of `(θ, t)`), and Lemma 1.1 bounds the fibre integral `∫1_T1{λ̃ ≤ U}1{|μ| ≤ x}w_λdλ̃` by `192xU³ ≤ 12288xΘ_•³/w⁶`. In (a), `x = δ`. In (b), on the fibre `λ₂` is fixed and `{λ₂|μ| ≤ δ} = {|μ| ≤ δ/λ₂}`, so `x = δ/λ₂` (of any size); the weight `λ₂³·(δ/λ₂)·192U³ = 192λ₂²δU³` is integrable. Integrate `λ₂³P^{p+q}Θ_•³e^{−c(…)}`. ∎

**Lemma 1.4 (sub-layer decision bands without a cut, with `H`).** Under (0.1), for `w ≥ 5`, `• ∈ {E, R}`, `S_T` as in Lemma 1.3 and every `δ > 0`,

    μ_r(S_T ∩ {|μ| ≤ δN}) ≤ C(δw^{−6} + rH⁶w^{−2}),                                                              (1.5)
    μ_r(S_T ∩ {λ₂|μ| ≤ δN²}) ≤ C(δw^{−6} + rH⁶w^{−2}).                                                           (1.6)

*Proof.* A3.7's Lemma MB₃ with Lemma 1.3 in place of its JB₃. `N ≥ 1`, and `μ = −∞` lies in neither event.
1. **(1.5).** A3.7's pointwise covering, over all shells of `|μ|`:

       1{|μ| ≤ δN} ≤ 1{|μ| ≤ δ} + Σ_{j≥0}4^{−j}N²1{|μ| ≤ 2^{j+1}δ}

   (if `2^jδ < |μ| ≤ 2^{j+1}δ` and `|μ| ≤ δN`, then `N > 2^j`). Apply `μ_r(1_{S_T}·)` and Lemma 1.3(a) with `p = 0` and `p = 2`, at every width: `C(δw^{−6} + rH⁶w^{−2}) + CΣ_{j≥0}4^{−j}(2^{j+1}δw^{−6} + rH⁶w^{−2}) = C((1 + 4)δw^{−6} + (1 + 4/3)rH⁶w^{−2})`.
2. **(1.6).** Likewise, over all shells of `λ₂|μ|`:

       1{λ₂|μ| ≤ δN²} ≤ 1{λ₂|μ| ≤ δ} + Σ_{j≥0}16^{−j}N⁴1{λ₂|μ| ≤ 4^{j+1}δ}

   (if `4^jδ < λ₂|μ| ≤ 4^{j+1}δ` and `λ₂|μ| ≤ δN²`, then `N² > 4^j`). Lemma 1.3(b) with `p = 0` and `p = 4` gives `C(δw^{−6} + rH⁶w^{−2}) + CΣ_j16^{−j}(4^{j+1}δw^{−6} + rH⁶w^{−2}) = C((1 + 16/3)δw^{−6} + (1 + 16/15)rH⁶w^{−2})`. ∎

A3.8's Lemma 3.2 paid its wide shells with a moment (`H³δ²`) and with one hard-gap strip (`H⁴δ⁴ + rH⁸δ²`); on a sub-layer neither is needed. The hard-gap strips of the barrels remain, and are paid once at the largest window (§3).

### 2. The shells (conditional on A3.4 and A3.7)

**What shell `j` pays.** Fix `1 ≤ j ≤ J` and write `w := w_j`, `w′ := w_{j−1} = w/2`, `e_j := e(w_j) = rw_j⁴ = 16rw′⁴`, `η_j := η_LE(w_j) = 2K₂rw_j² = 8K₂rw′²`, `U′ := U_•(γ, w′)`, and `S_T^j := U_T ∩ {λ̃ ≤ U′}` (so `S_j^• ⊂ S_T^j` for `• ∈ {E, R}`, by (0.2)). All constants below are free of `j`.

**Lemma 2.1 (the shell ledger).** Under (0.1), for `1 ≤ j ≤ J`:
- **(a) Bands.** For `δ_j := C′e_j` with a fixed `C′`, `μ_r(S_T^j ∩ {|μ| ≤ δ_jN}) ≤ C(rw′^{−2} + rH⁶w′^{−2})` and `μ_r(S_T^j ∩ {λ₂|μ| ≤ δ_jN²}) ≤ C(rw′^{−2} + rH⁶w′^{−2})`.
- **(b) Margins.** With `ε_j := 4K₀e_j/c_*` and `ε′_j := 4C_ek₊e_j/c_*` (A3.8 Lemma 4.1: `ε_j, ε′_j ≤ C_VH²e_j`),

      μ_r(S_T^j ∩ {a_S² ≤ ε_jN}) ≤ C(H²r + r^{3/2}H⁷),      μ_r(S_T^j ∩ {λ₂a_S² ≤ ε′_jN²}) ≤ C(H²r + r^{3/2}H⁷).

- **(c) The endpoint strip.** `μ_r(S_T^j ∩ Rsec ∩ ({η_jN(γ² + 72) ≥ 4a_M} ∪ {η_jN ≥ 1})) ≤ C(rw′^{−4} + r^{3/2}H⁶w′^{−2} + r²H⁶)`.
- **(d) The Hessian transfer.** `μ_r(T ∩ {γ ≠ 0} ∩ (B_r(w_j)) ∩ {ℋ_i(w_j) ≥ τ_i}) ≤ C(H⁴r²w_j⁴ + H⁸r²w_j²)` for `i ∈ {M, S}`, `τ_M = 1`, `τ_S = 2/5`.

*Proof.*
- **(a)** Lemma 1.4 at `w′` and `δ = δ_j = 16C′rw′⁴`: `δ_jw′^{−6} = 16C′rw′^{−2}`.
- **(b)** A3.8's Lemma 4.1 with (1.3)–(1.4) at `w′` in place of (2.1)–(2.2), that is with `(x₁, x₀) = (w′^{−4}, rH⁶w′^{−2})` in place of `(H², rH⁷)`. *The first:* split at `a_S = d₁`; the strip costs `x₁d₁²/2 + x₀d₁`, and away from it Markov's inequality in squared form with (1.3) and the weight `N²` costs `ε_j²(x₁d₁^{−2}/2 + x₀d₁^{−3}/3)`; with `d₁ = √ε_j` the total is exactly `x₁ε_j + (4/3)x₀√ε_j`. *The second:* the strip costs `C(x₁d₁² + x₀d₁)`; away from it, `1{λ₂y² ≤ ε′_jN²} ≤ N^{10}min(1, (δ_y/λ₂)⁵)` with `δ_y = ε′_j/y²`, and A3.6's exact integral (3.4) with `(x₁y, x₀)` gives `(5/4)x₁yδ_y⁴ + (5/6)x₀δ_y²` for each `y`, hence `(5/24)x₁ε′_j⁴d₁^{−6} + (5/18)x₀ε′_j²d₁^{−3}` over `y > d₁`; with `d₁ = √ε′_j` the elementary part is `(29/24)x₁ε′_j + (23/18)x₀√ε′_j` (A3.8, Lemma 4.1). Now `x₁ε_j ≤ w′^{−4}C_VH²·16rw′⁴ = 16C_VH²r` and `x₀√ε_j ≤ rH⁶w′^{−2}(16C_VH²r)^{1/2}w′² = 4C_V^{1/2}r^{3/2}H⁷`; likewise for `ε′_j`. If `√ε_j ≥ A_*` (or `√ε′_j ≥ A_*`), the strip alone suffices, as in A3.6.
- **(c)** A3.7's proof of Lemma B₃ with (1.3) and (1.2), split at `a_M = d` instead of `√η`: if `η_jN(γ² + 72) ≥ 4a_M` and `a_M > d`, then `N(γ² + 72) > 4d/η_j`. So the event lies in the union of `{a_M ≤ d}`, which costs `x₁d²/2 + x₀d` by (1.3) with `i = M`; of `{N(γ² + 72) > 4d/η_j}`, where `1 ≤ (η_j/(4d))²N²(γ² + 72)² ≤ (73²η_j²/(16d²))N²P⁴`, which costs `(73²η_j²/(16d²))·C(w′^{−8} + rH⁶w′^{−4})` by (1.2) with `(m, q) = (2, 4)`; and of `{η_jN ≥ 1}`, where `1 ≤ η_j²N²`, which costs `η_j²·C(w′^{−8} + rH⁶w′^{−4})`. Take `d := √η_j/w′`. Then `x₁d² = η_jw′^{−6}`, `x₀d = rH⁶w′^{−3}√η_j`, `(η_j²/d²)w′^{−8} = η_jw′^{−6}`, `(η_j²/d²)rH⁶w′^{−4} = η_jrH⁶w′^{−2}`, and with `η_j = 8K₂rw′²`: `η_jw′^{−6} = 8K₂rw′^{−4}`, `rH⁶w′^{−3}√η_j = (8K₂)^{1/2}r^{3/2}H⁶w′^{−2}`, `η_jrH⁶w′^{−2} = 8K₂r²H⁶`, `η_j²w′^{−8} = 64K₂²r²w′^{−4}` and `η_j²rH⁶w′^{−4} = 64K₂²r³H⁶`; every term is one of those displayed.
- **(d)** A3.8's Lemma 2.4 at the deterministic window `w_j`; it needs `w_j ≥ 5` and `r^{1/2}w_j ≤ 1`, which (0.3) gives. ∎

**Lemma 2.2 (the shell sums).** `Σ_{j=1}^{J}w_{j−1}^{−2} = Σ_{i≥0}(5·2^i)^{−2} ≤ 4/75`, `Σ_{j=1}^{J}w_{j−1}^{−4} ≤ 16/9375`, `Σ_{j=1}^{J}w_{j−1}⁴ ≤ (16/15)w_{J−1}⁴ ≤ (1/15)w_J⁴`, `Σ_{j=1}^{J}w_j⁴ ≤ (16/15)w_J⁴`, `Σ_{j=1}^{J}w_j² ≤ (4/3)w_J²`, and `J ≤ 2log(1/r) − 1`. Moreover `w_J⁴ ≤ w_max⁴ = r^{−3/4}`, `w_J² ≤ r^{−3/8}`, `w_J^{−8} ≤ 256r^{3/2}` and `w_J^{−4} ≤ 16r^{3/4}`.

*Proof.* Geometric series; `w_J > w_max/2` from (0.3); `J + 1 ≤ 1 + (3/16)log₂(1/r)` and `log₂(1/r) ≤ (3/2)log(1/r)` give `J ≤ (9/32)log(1/r) ≤ 2log(1/r) − 1` for `r ≤ e^{−1}`. ∎

### 3. The fixed layer at `O(r⁴log(1/r))` (conditional on A3.4 and A3.7)

**Theorem E₃″ (the elder side by shells).** Under (0.1) and `r ≤ r₁`, define

    Good^E_j := S_j^E ∩ Good^E(r, w_j)   (0 ≤ j ≤ J),      Good^{E″} := ⋃_{j=0}^{J}Good^E_j,

with `Good^E(r, w)` A3.6's (3.1). Then A3.6's Theorem E₃(a) holds on `Good^{E″}` (on it `D_f(M_r) = f(S_r)`, hence `H_r` on the Morse locus), and

    μ_r(E ∖ Good^{E″}) ≤ C[r^{3/2} + r^{7/4}H⁶ + H⁴r + H⁸r^{3/2} + H⁴r^{5/4} + H⁸r^{13/8} + rH⁷ + H²r log(1/r) + r^{3/2}H⁷log(1/r)].   (3.1)

*Proof.* The certificate is Theorem E₃(a) applied with the deterministic window `w_j` on each `Good^E_j`. For the bad mass, `E ∖ Good^{E″} ⊂ S_top^E ∪ ⋃_{j=0}^{J}(S_j^E ∖ Good^E(r, w_j))`, and on `S_j^E` the radius condition `ρ_E < w_j` of (3.1) holds, so A3.6's proof of Theorem E₃(b), step 4, at the window `w_j` gives

    S_j^E ∖ Good^E(r, w_j) ⊂ F_B^j ∪ F_H^j ∪ V₁^j ∪ V₂^j ∪ V₃^j ∪ V₄^j,

with `F_B^j := S_j^E ∖ (B_r(w_j)) ⊂ {λ₂ ≤ C_Bk₊e_jN²}`, `F_H^j := S_j^E ∩ (B_r(w_j)) ∩ ({ℋ_M(w_j) ≥ 1} ∪ {ℋ_S(w_j) ≥ 2/5})`, and, by (D₃) at `w_j` on `(B_r(w_j))`, `V₁^j ⊂ S_j^E ∩ {a_S² ≤ ε_jN}`, `V₂^j ⊂ S_j^E ∩ {λ₂a_S² ≤ ε′_jN²}` (A3.6 steps 5–6 with `v ≥ c_*a_S²`), `V₃^j ⊂ S_j^E ∩ {|μ| ≤ 4K₀e_jN}` and `V₄^j ⊂ S_j^E ∩ {λ₂|μ| ≤ 4C_ek₊e_jN²}` (A3.7 steps 7′–8′). Bound the pieces in `μ_r`:
1. **The top.** `S_top^E = E ∩ {ρ_E ≥ w_J}`: A3.8 Lemma 2.2 at `w_J` and Lemma 2.2 give `C(w_J^{−8} + rH⁶w_J^{−4}) ≤ C(r^{3/2} + r^{7/4}H⁶)`.
2. **The barrels, once.** `⋃_jF_B^j ⊂ {λ₂ ≤ C_Bk₊e_JN²}`, a set inclusion, since `e_j ≤ e_J`; A3.8 Lemma 2.3 at `δ = C_Bk₊e_J` and `e_J ≤ r^{1/4}` give `C(H⁴e_J⁴ + rH⁸e_J²) ≤ C(H⁴r + H⁸r^{3/2})`. (Summing the shells instead, `Σ_jC(H⁴e_j⁴ + rH⁸e_j²) ≤ (16/15)C(H⁴e_J⁴ + rH⁸e_J²)`, gives the same.)
3. **The Hessians, summed.** Lemma 2.1(d) for `j ≥ 1` and A3.8 Lemma 2.4 at `w_0 = 5` for `j = 0`; by Lemma 2.2, `Σ_{j=0}^{J}(H⁴r²w_j⁴ + H⁸r²w_j²) ≤ C(H⁴r²w_J⁴ + H⁸r²w_J²) ≤ C(H⁴r^{5/4} + H⁸r^{13/8})`.
4. **The margins, summed.** For `j ≥ 1`, Lemma 2.1(b) on `S_T^j ⊃ S_j^E` gives `C(H²r + r^{3/2}H⁷)` per shell; for `j = 0`, A3.8 Lemma 4.1 on the whole layer at `e_0 = 625r` gives `C(H⁴r + H⁸r^{3/2})`. With `J ≤ 2log(1/r)`: `C(H⁴r + H⁸r^{3/2} + H²r log(1/r) + r^{3/2}H⁷log(1/r))`.
5. **The level bands, summed.** For `j ≥ 1`, Lemma 2.1(a) at `C′ = 4K₀` for `V₃^j` and at `C′ = 4C_ek₊` for `V₄^j`: `C(rw′^{−2} + rH⁶w′^{−2})` per shell, and Lemma 2.2 sums these to `C(r + rH⁶)`. For `j = 0`, A3.8 Lemma 3.2 at `δ = 2500K₀r` and `δ = 2500C_ek₊r`: `C(r + rH⁷ + H³r² + H⁴r⁴ + rH⁸r²) ≤ C(rH⁷)` under (0.1).
Add; every term is in (3.1) (with `rH⁶ ≤ rH⁷`). Multiply by `r³/z_r ≤ 2r³/z_*` for `Q_r^W`. ∎

**Theorem R₃″ (the rejected side by shells).** Under (0.1) and `r ≤ r₁`, define

    Good^{R″} := ⋃_{j=0}^{J}(S_j^R ∩ Good^{R′}(r, w_j)),

with `Good^{R′}(r, w)` A3.7's (3.2). Then A3.7's Corollary LE₃ holds on `Good^{R″}` (on it `D_f(M_r) > f(S_r)`, hence `H_r` fails on the Morse locus in `{W_r > 0}`), and

    μ_r(Rsec ∖ Good^{R″}) ≤ C[r^{3/2} + r^{7/4}H⁶ + rH⁷ + H³r + r^{3/2}H⁷ + r²H⁶log(1/r)].                           (3.2)

*Proof.* The certificate is Corollary LE₃ at the deterministic window `w_j` on each piece (`w_j ≥ 1`). For the bad mass, A3.7's proof of Theorem R₃′ at `w_j` on `S_j^R` (where `ρ_R < w_j`): `S_j^R ∖ Good^{R′}(r, w_j)` lies in the union of `S_j^R ∩ {|μ| ≤ 2K₀e_jN}` (by (FW.0), `sup_{Ω̄_{w_j}}|ℰ(·, ·, 0)| ≤ K₀Ne_j`) and of Lemma B₃'s event at `η = η_j`. Then:
1. **The top** costs `C(r^{3/2} + r^{7/4}H⁶)`, as in Theorem E₃″ step 1.
2. **The bands, summed.** Lemma 2.1(a) at `C′ = 2K₀` for `j ≥ 1`, and A3.8 Lemma 3.2 at `δ = 1250K₀r` for `j = 0`: `C(rH⁷)`, as in Theorem E₃″ step 5.
3. **The endpoint strips, summed.** Lemma 2.1(c) for `j ≥ 1` and Lemma 2.2: `C(r + r^{3/2}H⁶ + r²H⁶log(1/r))`; for `j = 0`, A3.8 Lemma 4.2 at `η_0 = 50K₂r`: `C(H³r + rH⁷√r)`.
Add and multiply by `r³/z_r`. ∎

**Theorem BL₃″ (the bounded layer in `d = 3`, at `O(r⁴log(1/r))`).** Uniformly in `b ∈ B₀`, `k ∈ [k₋, k₊]` and the frame, for fixed `Λ ≥ 1` and `0 < r ≤ r_Λ`, A3.6's Theorem BL₃ holds with (b)–(e) replaced by:

    (b″) Q_r^W(D_Λ ∩ (H_r Δ E)) ≤ C_Λr⁴log(1/r);
    (c″) Q_r^W(D_Λ ∩ H_r) = r³m_E/z₀ + O(r⁴log(1/r)),    Q_r^W(D_Λ ∖ H_r) = r³m_R/z₀ + O(r⁴log(1/r));
    (d″) Q_r^W(H_r | D_Λ) = m_E/m_Λ + O(r log(1/r));
    (e″) for every bounded Borel φ on D_Λ × {0, 1},
         |r^{−3}E_{Q_r^W}[1_{D_Λ}φ(ϑ, 1_{H_r})] − z₀^{−1}∫_{D_Λ}φ(ϑ, 1_E(ϑ))dμ₀| ≤ C_Λ‖φ‖_∞ r log(1/r).

*Proof.* A3.6's proof of Theorem BL₃ with Theorems E₃″ and R₃″ in place of E₃(c) and R₃(c) in step 3: `D_Λ ∩ (H_r Δ E) ⊂ (E ∖ Good^{E″}) ∪ (Rsec ∖ Good^{R″}) ∪ (D_Λ ∩ T^c)` up to the null sets of A3.6's Lemma M₃(g) and the non-Morse locus, by the two certificates. At fixed `Λ`, `H` is a constant, and under `r ≤ r_Λ := min(r₁, H^{−4})` the condition (0.1) holds; every term of (3.1)–(3.2) is then `O(r log(1/r))` (the largest are `H²r log(1/r)` and `rH⁷`), and `(E₃.6)` bounds the leakage by `Cr`. The other errors of steps 3–5 are `O(r⁴)` from (E₃.6) and (J₃.5). ∎

At fixed `Λ` the exponents of (3.1), in the order displayed, are `3/2, 7/4, 1, 3/2, 5/4, 13/8, 1, 1⁻, 3/2⁻` (a minus marks a logarithm), and those of (3.2) are `3/2, 7/4, 1, 1, 3/2, 2⁻`. A3.7's `w^{−8}`, `e` and `rw^{−4}` are gone: the radius tail survives only at the top window `w_J ≈ r^{−3/16}`, where it is `r^{3/2}`, and no decision band is ever read on a window larger than its pair's shell needs.

### 4. The exhaustion (conditional on A3.4 and A3.7)

**The ledger.** Under (0.1) and `r ≤ r₁`, define

    Rerr₃″(r, H) := rH⁷ + H²r log(1/r) + H⁴r^{5/4} + r^{3/2}H⁸ + r^{3/2}H⁷log(1/r) + H⁸r^{13/8} + r^{7/4}H⁶ + r²H⁶log(1/r).   (4.1)

Every term of (3.1) and (3.2) is bounded by a constant times a term of (4.1): `H⁴r ≤ rH⁷`, `H³r ≤ rH⁷`, `r^{3/2} ≤ r^{3/2}H⁸`, `r^{3/2}H⁷ ≤ r^{3/2}H⁸`.

**Proposition 4.1 (the layer comparison).** Under (0.1) and `r ≤ r₁`,

    r^{−3}Q_r^W(D_Λ ∩ (H_r Δ E)) ≤ C Rerr₃″,      ‖ν_r^F|_{D_Λ} − ν_0^F|_{D_Λ}‖_var ≤ C Rerr₃″.                      (4.2)

*Proof.* A3.8's Proposition 6.1 with (3.1)–(3.2) in place of A3.7's Theorems E₃′ and R₃′: the first bound is Theorem BL₃″'s inclusion with the leakage `μ_r(D_Λ ∩ T^c) ≤ CrH⁷` (A3.8 (1.4)); the second is A3.8's second bound, whose density comparison is A3.8 (1.4)'s `CrH⁷`. ∎

**Theorem QFE₃′ (every `β < 1`).** Fix `β ∈ (0, 1)`. There are `C_β < ∞` and `r_β > 0`, uniform over `b ∈ B₀`, `k ∈ [k₋, k₊]` and the frame, such that for `0 < r ≤ r_β`

    ‖ν_r^F − ν_0^F‖_var ≤ C_βr^β,      1 − p_r = r³α^{(3)} + O_β(r^{3+β}),                                      (4.3)

and the raw-jet law conditional on failure converges at the same rate.

*Proof.* A3.8's proof of Theorem QFE₃ with Proposition 4.1 and the schedule `α := (1 − β)/8`, `Λ := r^{−α}` (so `H ≤ 2r^{−α}`), and a fixed integer `m ≥ 8β/(1 − β)`. With `H` replaced by `r^{−α}` the `r`-exponents of the terms of (4.1) and of the tails are:

| term | exponent | at least `β` because |
|---|---|---|
| `rH⁷` | `(1 + 7β)/8` | `β ≤ 1` |
| `H²r log(1/r)` | `(3 + β)/4`, minus a logarithm | `β < 1` strictly; the logarithm is absorbed |
| `H⁴r^{5/4}` | `(3 + 2β)/4` | `β ≤ 3/2` |
| `r^{3/2}H⁸` | `1/2 + β` | |
| `r^{3/2}H⁷log(1/r)` | `(5 + 7β)/8`, minus a logarithm | `β < 5` |
| `H⁸r^{13/8}` | `5/8 + β` | |
| `r^{7/4}H⁶` | `1 + 3β/4` | |
| `r²H⁶log(1/r)` | `(5 + 3β)/4`, minus a logarithm | `β < 5` |
| `Λ^{−m}` (A3.8 Lemmas 5.1 and 5.3) | `mα ≥ β` | the choice of `m` |
| the far exceptions of A3.8 Lemma 5.1 | `1` | |

The conditions hold for small `r`: `rH⁴ ≤ 16r^{(1 + β)/2} ≤ 1` (hence `rH ≤ 1`), `w_max ≥ 5`, `r ≤ e^{−1}`. Combine (4.2) with A3.8's two polynomial tails: `‖ν_r^F − ν_0^F‖_var ≤ C Rerr₃″ + ν_r^F(D_Λ^c) + ν_0^F(D_Λ^c) ≤ C_βr^β`. Apply this to `φ = 1` for the second statement, and A3.8's floor `α^{(3)} ≥ M_*` for the conditional one. ∎

**Theorem ER₃′ (the endpoint).** There are `C < ∞` and `r_* ∈ (0, e^{−1}]`, uniform over `b ∈ B₀`, `k ∈ [k₋, k₊]` and the frame, such that for `0 < r < r_*`

    ‖ν_r^F − ν_0^F‖_var ≤ Cr log(1/r)⁷,      1 − p_r = r³α^{(3)} + O(r⁴log(1/r)⁷),                                (4.4)

and the raw-jet law conditional on failure converges at the same rate.

*Proof.* A3.8's proof of Theorem ER₃ with Proposition 4.1. Take `Λ := D_*log(1/r)` with `D_* ≥ 1` so large that both exponential tails of A3.8 Lemma 5.4 are `O(r)`; then `H ≤ (1 + D_*)log(1/r)`, and (0.1) holds for small `r`. In (4.1), `rH⁷ ≤ Cr log(1/r)⁷`, `H²r log(1/r) ≤ Cr log(1/r)³`, and every other term is `r^{1+a}` times a power of `log(1/r)` with `a ≥ 1/4`, hence `O(r)`. ∎

**The coefficient** is unchanged: `α^{(3)} = m_R^{(∞)}/z₀ = F(k; b, u)/(kA_0(b, k, u))` (A3.8 §6, A3.9 Theorem 9.2).

### 5. Consequences for A3.9 and A3.10 (conditional as those notes are)

**Corollary 9.3′ (A3.9's Corollary 9.3 with the new rates).** In `d = 3`, for every fixed `β ∈ (0, 1)` there are `C_β` and `r_β > 0`, and there are `C` and `r_* ∈ (0, e^{−1}]`, uniform over `b ∈ B₀`, `k ∈ [k₋, k₊]` and the frame, such that A3.9's (9.4) holds, in both its forms, with `r^β` for `β < 1` and with `r log(1/r)⁷` in place of `r^{2/3}log(1/r)^{8/3}`.

*Proof.* A3.9's proof of Corollary 9.3 with (4.3)–(4.4) in place of A3.8's (6.3)–(6.4); its other input, [R] (R11)'s `|A_r − A_0| ≤ Cr` on the compact window, is `O(r^β)` for `β ≤ 1` and `O(r log(1/r)⁷)` for `r ≤ e^{−1}`. ∎

**Corollary PD₃′ (A3.10's Corollary PD₃ with the new rates).** In A3.10's setting (`d = 3`; the compact window `B × K`, `0 < k₋ ≤ k₊`; `S²`; `ν_cand`, `ν_eld`, `ν_rej`, `c_cand`, `C_fail^{(3)}`, `N_rej`), there are `ℓ_* ∈ (0, e^{−1}]` and `C < ∞`, depending only on `L`, `B` and `K`, such that for `0 < ℓ, t < ℓ_*`:
- **(o)** unchanged: `ν_cand(ℓ) = c_candℓ^{−1/3} + O(1)`, and the same for `ν_eld`;
- **(i)** `|ν_rej(ℓ) − C_fail^{(3)}ℓ^{2/3}| ≤ Cℓ log(1/ℓ)⁷`;
- **(ii)** `|EN_rej(0, t] − (3/5)C_fail^{(3)}t^{5/3}| ≤ 146Ct²log(1/t)⁷`;
- **(iii)** for every real `q > −5/3`, `|EΣ_{nonselected, ℓ≤t}ℓ^q − C_fail^{(3)}t^{q+5/3}/(q + 5/3)| ≤ 46149330·Ct^{q+2}log(1/t)⁷`;
- **(iv)** `ν_rej(ℓ)/ν_cand(ℓ) = (C_fail^{(3)}/c_cand)ℓ + O(ℓ^{4/3}log(1/ℓ)⁷)`, that is `ν_eld(ℓ) = ν_cand(ℓ)[1 − (C_fail^{(3)}/c_cand)ℓ + O(ℓ^{4/3}log(1/ℓ)⁷)]`;
- **(v)** for each fixed `β ∈ (0, 1)` there are `ℓ_β` and `C_β` such that (i)–(iv) hold for `ℓ, t < ℓ_β` with `C_βℓ^{(2+β)/3}`, `C_βt^{(5+β)/3}`, `C_βt^{q+(5+β)/3}` and `C_βℓ^{1+β/3}` in place of the logarithmic errors.

*Proof.* A3.10's proof with (4.3)–(4.4) in its step 2: `|ϱ_r − α^{(3)}| ≤ C₁r log(1/r)⁷` for `r < r_*`, and A3.10's conversion `r ≤ k₋^{−1/3}ℓ^{1/3}`, `log(1/r) ≤ (2/3)log(1/ℓ)` (for `k₊ ≤ 1/ℓ`) gives `r log(1/r)⁷ ≤ (2/3)⁷k₋^{−1/3}ℓ^{1/3}log(1/ℓ)⁷`. In step 4, the `(A_r − A_0)α^{(3)}` term is `O(ℓ^{1/3})`, absorbed since `log(1/ℓ) ≥ 1`; so `|ℓ^{−2/3}ν_rej − C_fail^{(3)}| ≤ Cℓ^{1/3}log(1/ℓ)⁷`, which is (i). In step 5, with `ℓ = ts`, `log(1/ℓ)⁷ ≤ log(1/t)⁷(1 + log(1/s))⁷`, so the error integral is at most `Ct^{q+2}log(1/t)⁷∫₀¹s^{q+1}(1 + log(1/s))⁷ds`, and with `s = e^{−x}` the last integral is `Σ_{j=0}^{7}C(7, j)j!/(q + 2)^{j+1}`, finite exactly when `q > −2`; for `q > −5/3`, `q + 2 > 1/3`, so it is at most `Σ_jC(7, j)j!·3^{j+1} = 46149330`, and at `q = 0` it is `Σ_jC(7, j)j!/2^{j+1} = 2325/16 < 146`. The main term is A3.10's. Step 6 gives (iv) with `ℓ[C_fail^{(3)} + O(ℓ^{1/3}log(1/ℓ)⁷)]/[c_cand + O(ℓ^{1/3})]`. Step 7 with (4.3) gives (v), with `1/(q + (5 + β)/3) ≤ 3/β` for `q > −5/3`. ∎

The `d = 3` rejected lifetime density on compact windows is thus known to the order `ℓ`, up to a logarithm — the order at which [P] §§10–12's own candidate expansion `ν_cand = c_candℓ^{−1/3} + O(1)` places its next term (relative `ℓ^{1/3}`).

### 6. Remarks

1. **What binds now.** At fixed `Λ`, the margins' sum `H²r log(1/r)`: shell `j` pays `x₁ε_j ∝ w′^{−4}·rw′⁴ = r` for the strip `{a_S ≲ √ε_j}` of the elder tolerance `v ≥ c_*a_S²` (A3.6 (1.2)), and there are `≈ (3/16)log₂(1/r)` shells. Removing the logarithm would need a tolerance floor better than quadratic in `a_S` near the sector's edge, or a window for the elder certificate smaller than `ρ_E` on that edge; neither is attempted. In the exhaustion the layer-law remainder `rH⁷` binds (A3.8 Lemma 1.3), which is where the exponent `7` of the endpoint logarithm comes from (A3.8 Remark 1: the sixth power of Lemma D's (J₃.16) and the layer's length); it costs nothing in the polynomial rate.
2. **Why deterministic windows suffice.** A3.7 Remark 2 feared a `ψ`-dependent band width. The shells make the width deterministic on each shell (`4K₀e_jN`, with `N` handled by A3.7's pointwise Markov covering) and move the `ψ`-dependence into the *domain* of the fibre integral, which Lemma 1.1 localizes. The same device localizes A3.8's edge integrals (Lemma 1.2). Nothing in C82 §5 is contravened: every band C82's density sees has a fixed width at most `1/2`.
3. **What is not localized.** The barrels' hard-gap strips `{λ₂ ≤ C_Bk₊e_jN²}` (A3.8 Lemma 2.3) are paid once, at the largest window, and the Hessian transfer (A3.8 Lemma 2.4) is summed over the windows; their costs `H⁴e_J⁴ ≤ H⁴r` and `H⁴r²w_J⁴ ≤ H⁴r^{5/4}` are already within the budget, because `e_J ≤ r^{1/4}` and `w_J ≤ r^{−3/16}` (A3.5's `β ≤ 3/16`, Proposition G₃⁻'s sharp threshold, is exactly what makes `e_J⁴ ≤ r`).
4. **The top window.** `w_max = r^{−3/16}` is the largest window A3.5's Theorem G₃ allows at the `r⁴` level; the pairs above it (`ρ_• ≥ w_J`, that is `λ̃ ≲ r^{3/8}`) are not decided and cost `w_J^{−8} ≍ r^{3/2}`. Any `w_max = r^{−ω}` with `1/8 ≤ ω ≤ 3/16` would do.
5. **The planar chain.** The same shells, with C124's JB/DB (which rest on C82's Theorem LB in the same way), C94 (C6)'s radius tails, C94 (C9)–(C10)'s margins and A4's Lemma B, would replace the exponent `11/3` of C124's Theorem ER (4) and A4.2's Theorem ER_K by `4` up to a logarithm, and Corollary PD / PD_ER's `ℓ^{8/9}log^{8/3}` by `ℓ log^a`. This is not carried out here: the planar lemmas' exact forms (their edge integrands and `K`-uniform constants) must be re-read before the transfer is claimed. A3.10's Remark on the `d = 2` transport stands as it is.
6. **`d ≥ 4`**: as A3.8 Remark 3.

### 7. Checks

**Controls** (`a311_exact.py`, posted below; standard library only, exact rationals except the stated numeric group): Z1 the constants of Lemma 1.1 (`(γ⁶/384)(16/3)(24U/γ²)³ = 192U³`, `(γ⁶/384)(24U/γ²)³/3 = 12U³`, `12 ≤ 24x` for `x ≥ 1/2`); Z2 the exact critical-point identities of the sheared cubic used in Lemma 1.1 step 2 (`σ² − 1 = cZ²/36`, `RZ = 48(ψ − cσ)`, `P = (σ − 1)/2 − ψZ²/144`, `∂_ψP = −Z²/48`, `det Hess = −σ(ψ − cσ)/4 − c²Z²/144 = (c − σψ)/4`, C82 (5)), at exact rational points; Z3 the sub-layer integrals of Lemma 1.2 (`72U⁴`, `6U²`, `12U²`) and the bounds `U ≤ 4Θ/w²`, `Θ_• ≤ 49P²`; Z4 Lemma 2.1(b)'s split totals (`x₁ε + (4/3)x₀√ε`, `(29/24)x₁ε′ + (23/18)x₀√ε′`) and their shell values (`16C_VH²r`, `4C_V^{1/2}r^{3/2}H⁷`); Z5 Lemma 2.1(c)'s optimization (`d = √η/w′` equalizes the strip and the Markov term) and the five shell values; Z6 Lemma 2.2's sums and `J ≤ 2log(1/r) − 1`; Z7 the exponent table of Theorem QFE₃′ on a grid of `β` (every term `≥ β`, the three logarithmic terms `> β`), the ER₃′ powers, and the dominated terms of (4.1); Z8 Corollary PD₃′'s constants (`Σ_jC(7, j)j!3^{j+1} = 46149330`, `Σ_jC(7, j)j!/2^{j+1} = 2325/16`) and `(2/3)⁷`; Z9 (numeric, floating point, deterministic sample) a direct check of Lemma 1.1 on sampled `(c, R)`: on each saddle branch of the sheared cubic (the roots of C82's quadratic (6), typed by C82 (5)), the band `{|v| ≤ x}` is located by bisection in `ψ` (`v` is monotone on a branch) and `∫1{ψ ≤ ψ_U}1{|μ| ≤ x}(ψ² − c²)dψ` is bounded by the closed-form integral over the union of the branch intervals, which is compared with `(16/3)xψ_U³` for `x ∈ {1/2, 1/4, 1/10, 1/50, 1/1000}` and several `ψ_U` per sample, including the top of each band; the density bound `48(ψ² − c²)/Z² ≤ (4/3)ψ³` is checked at `v ≤ 1/2` along the branches. Z7 derives the `(r, log)`-powers of (4.1) from its term list rather than from a typed table. Mutants M1–M12 exit 1 naming their group; any other argument exits 2.

**Exploration** (outside the repository; numpy): a grid version of Z9 on 400 samples with 60001 `ψ`-points each (6400 band tests) and a branch-wise version maximizing over `ψ_U`: the ratio of the band integral to `(16/3)xψ_U³` never exceeds `0.25` (maximized over `ψ_U`: `0.090, 0.121, 0.154, 0.209, 0.243` for `x = 1/2, 1/4, 1/10, 1/50, 1/1000`; it grows as `x ↓ 0`, as it must: on a branch where the density bound is tight a narrow band costs `≈ (8/3)xψ³`, half of (1.1)'s two-branch allowance); the density ratio to `(4/3)ψ³` reaches `0.84` on the grid sample and `0.9955` in the referee's wider sample, near degenerate saddles (`c < 0`, `ψ ≈ |c|`, `v ≈ 0`), so C82's bound is essentially attained there.

**Referee** (one clean-context pass, same provider and session; not review evidence): see the controls comment.

### 8. Not claimed

- No new estimate on the layer law, the certificates, the model or the tails: Lemma 1.1 is C82's proof read on a sub-domain, and everything else is A3.5–A3.8 shell by shell.
- No removal of the logarithms (Remark 1); no exponent above `1` in `r` (the layer law's `O(r)` is the natural scale of (J₃.5)); no statement that `r⁴` is sharp.
- No planar (`d = 2`) statement (Remark 5); no `d ≥ 4` statement; no unrestricted (`k → 0`) rate; no numerical coefficient.
- No change to A3.7, A3.8, A3.9 or A3.10: their statements remain correct as posted; this note supersedes their rates where it is cited.

### 9. Review request

Three bounded slices; one reader may take all three. Please claim first (a pickup naming the two body SHAs), then post PASS / AMEND (with the exact change) / BLOCK (with the reason), the scope actually checked and what was not checked, and disclose provider, model and session.
- **Slice 1 (the new lemma).** Lemma 1.1 against C82 §§2–3 (the branch structure, the envelope identity, the density bound and its range `v ≤ 1/2`; the exceptional values `c = 0`, `R = 0`); Lemmas 1.2–1.4 against A3.8's Lemmas 2.1–2.2 and 3.1–3.2 and A3.7's Lemma MB₃; control groups Z1–Z3, Z9.
- **Slice 2 (the shells).** (0.2)–(0.4); Lemma 2.1 (a)–(d) against A3.6 §3 steps 4–8, A3.7 Lemmas B₃, JB₃, MB₃ and §5, and A3.8 Lemmas 2.3–2.4, 4.1–4.2; Lemma 2.2; Theorems E₃″, R₃″ and BL₃″ (the inclusions, the unions at the largest window, the sums); control groups Z4–Z6.
- **Slice 3 (the exhaustion and the consequences).** (4.1), Proposition 4.1, Theorems QFE₃′ and ER₃′ against A3.8 §§5–6; Corollaries 9.3′ and PD₃′ against A3.9 §3 and A3.10 §2; §§6 and 8 for overclaim; control groups Z7–Z8.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_