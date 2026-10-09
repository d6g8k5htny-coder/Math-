## QS addendum A4.3: the planar decision on dyadic windows at compact `K` — sector errors `O(r⁴log(1/r))`, the failure-measure rate `r^β` for every `β < 1`, endpoint `O(r⁴log(1/r)⁴)`, and `ν_rej = C_failℓ^{2/3} + O(ℓ log(1/ℓ)⁴)`

**Object.** `CL-QS-A4-3-PLANAR-DYADIC-WINDOWS-20261006-v1`.

**Who.** Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`, the author of A4, A4.1, A4.2 and A3.11. Dylan Roy — delegated AI work. Author-side. Scientific effect: NONE.

**Claim.** [6010186331](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6010186331); this delivery releases it.

**What this is.** A3.11 ([6009956838](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6009956838)) removed the `d = 3` chain's obstruction at the exponent `2/3` by reading each pinned pair on the smallest dyadic window that holds its certificate and paying each shell's decision bands with C82's coarea density localized to the shell's sub-layer (its Lemma 1.1). Its Remark 5 said the same shells would do the same for the planar chain and that the transfer was not carried out there. This note carries it out, in C103's compact-`K` setting with A4.1's local endpoint and A4.2's four compact-`K` lemmas, which is where Corollary PD_ER lives. Nothing is new in substance: Lemma 1.1 is dimension-free (the same cubic `P_QS`, the same fibre identity `w(y)dλ = (γ⁶/384)(ψ² − c²)dψ`), and the shell bookkeeping is A3.11's with C103's displays in place of A3.8's — the planar chain has no hard direction, so there is no barrel and no `λ₂`-band, and the layer law's remainder is `rH³` (C103 (S5)) in place of `rH⁶`.

The results, uniformly over births `b ∈ B₀`, gaps `k ∈ K = [k_-, k_+]` and frames: on every fixed layer `Q_r^W(D_Λ ∩ (H_r Δ E)) ≤ C_{K,Λ}r⁴log(1/r)` (Theorem SE″_K; A4.2 Theorem ER_K and C124 (4): `r^{11/3}`); `‖ν_r^F − ν_0^F‖_var ≤ C_{K,β}r^β` for every `β < 1` (Theorem QFE″_K; A4.1 Theorem QFE′_K: `β < 2/3`); `1 − p_r = r³(α₁ + α₂) + O_K(r⁴log(1/r)⁴)` (Theorem ER′_K; A4.2: `r^{11/3}log(1/r)^{8/3}`); and `ν_rej^{B,K}(ℓ) = C_failℓ^{2/3} + O(ℓ log(1/ℓ)⁴)` with its cumulative, moment and fraction corollaries (Corollary PD_ER′; A4.2's PD_ER: `ℓ^{8/9}log(1/ℓ)^{8/3}`). The coefficient `α₁ + α₂` (C101/CUB, C103 §6) is unchanged.

**Consumed.**
- *Merged or reviewed, as A4.2 consumes them.* C103 ([5967841127](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5967841127); my cross-provider review [5972892024](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5972892024)): its §0 setting, (S4)–(S8) (the uniform actual weighted laws), §2 (the edge integrals (S9)–(S11)), §3 ((S12)–(S24): the window error, the radii (S13), the margin (S15), the Hessian transfer (S21)–(S23) and the admissibility list (S24)), §4 ((S25)–(S28): the transport, the selected and rejected certificates, the null sets, the comparison) and §§5–6 as FT_K uses them. C101 ([5967063473](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5967063473)) §4.1 for the radius sub-layer (`λ < H_γ/ρ²`, `H_γ = (3/8)(|γ| + 12)²`). C124 ([5974162498](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5974162498)) Lemmas JB, DB, ES, FT and its ledger (15), through A4.2's compact-`K` forms. C82 ([5959920397](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5959920397)) §§2–3 through A3.11 Lemma 1.1. C94–C98 and [P] exactly as C103 consumes them.
- *Author-side.* A4 ([5972396791](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5972396791); reviewed [5972610615](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5972610615)) Lemma LE; A4.1 ([5973261552](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973261552)) Lemma LE_K, Corollary LE_K, Lemma B′_K; A4.2 ([5974565257](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5974565257); Slices A–D read) Lemmas JB_K, DB_K, ES_K, FT_K, Theorem ER_K's proof and Corollary PD_ER; Corollary PD ([5973476391](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973476391), Codex PASS) §2; A3.11 Lemma 1.1 (Slice 1 PASS [6009971496](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6009971496)) and its §§2–4 as the template.
- Everything below is conditional exactly as A4.2's Theorem ER_K and Corollary PD_ER are: on C103's inputs at their stated scopes (C102's regression constants, C94–C98's geometry, C96's identification, [P]'s cap and tails), on A4/A4.1's endpoint certificate, and on C82 §§2–3 through Lemma 1.1.

### 0. Setting and notation

- **As in C103 §0 and A4.1 §0.** The side-`L` planar torus; `b ∈ B₀`, `k ∈ K = [k_-, k_+]` with `0 < k_- ≤ k_+ < ∞`, all frames; `Q_r`, `W_r`, `Z_r = r²z_r`, `Q_r^W`; the normalized jets `y = (λ, γ, B, C)`, `t = (γ, B, C)`, `Pjet = 1 + |γ| + |B| + |C|`; `a_M = 24λ − γ² + 12B`, `a_S = 24λ + γ² − 12B` (C103 §2), `T = {a_M > 0, a_S > 0}`, the weight `w(y) = a_Ma_S/16` on `T`; `D, J, ψ, c, Rq`, the cubic `P_QS`, `μ`, `h = 1 − μ`, `E`, `Rsec`; the window `w` (C103's `w₀`), `W_w`, `E_r = F_r − G_y`, `E0(r, w) = sup_{W_w}|E_r|`, the field norm `N`; `Rbox`, `Rch` (C103 (S13)); `D_Λ = {|λ| ≤ Λ}`, `H = 1 + Λ`; `μ_r(Φ) := μ_r(Φ; D_Λ) = r^{−5}E_{Q_r}[W_rΦ; D_Λ]`, `ν_r^F`, `ν_0^F`; `e(w) := rw⁴`, `η_K(w) := 2K₂(K)rw²`; the constants `K₀(K)`, `K₂(K)` (C103 (S12)), `C_V = 500K₀(K)·48²/3` and `c_* = 3/[250(48Λ)²]` (C103 (S15)), `C_η = 5K₂(K)/3`. `C_K` denotes constants depending only on `L`, `B₀`, `K` and the fixed moment orders; never on `Λ`, `w`, `r`, `(b, k, R)` or a shell index.
- **Standing conditions** (C103): `0 < r ≤ r₀`, `Λ ≥ 1`, `rH/k_- ≤ 1`; and `r ≤ e^{−1}` wherever `log(1/r)` appears.
- **The radius sub-layers** (C101 §4.1, C103 (S13)–(S14)). With `H_γ := (3/8)(|γ| + 12)²`, for `w ≥ 5`,

      D_Λ ∩ ({Rbox ≥ w} ∪ {Rch ≥ w}) ⊂ {λ ≤ U(γ, w)},      U(γ, w) := min(Λ, 4H_γ/w²),                        (0.1)

  because `Rbox ≥ w` gives `(5/2)(|γ| + 12)/√(24λ) ≥ w − 3/2 ≥ w − 5/2`, hence `λ ≤ (25/96)(|γ| + 12)²/(w − 5/2)²`, and `Rch ≥ w` gives `λ ≤ H_γ/(w − 5/2)²`, with `w − 5/2 ≥ w/2`. On `T`, `λ > 0`. (C103 (S14) is stated for `Rbox > w₀` or `Rch > w₀`; the boundary is a null set, and the same proof covers `≥`.) Also `H_γ ≤ 54(1 + |γ|)² ≤ 54Pjet²`, so polynomials in `H_γ` are absorbed by the Gaussian envelope of C103 (S4).
- **The windows and the shells**, as A3.11 (0.3)–(0.4):

      w_max := r^{−3/16},    w_j := 5·2^j  (j ≥ 0),    J := max{j : w_j ≤ w_max},                               (0.2)

  so `w_J ≤ w_max < 2w_J`, `J + 1 ≤ 2log(1/r)`, `e(w_J) ≤ e_max := r^{1/4}`, `η_K(w_J) ≤ η_max := 2K₂(K)r^{5/8}`. The shells are defined by the radius of each sector's certificate, `ρ_E := Rbox` on `E` and `ρ_R := Rch` on `Rsec`:

      S_0^• := {ρ_• < w_0},      S_j^• := {w_{j−1} ≤ ρ_• < w_j}  (1 ≤ j ≤ J),      S_top^• := {ρ_• ≥ w_J}.         (0.3)

  By (0.1), `D_Λ ∩ S_j^• ⊂ {λ ≤ U(γ, w_{j−1})}` for `1 ≤ j ≤ J`. The pairs of shell `j` are read on the window `w_j`. Besides the standing conditions, the admissibility list C103 (S24), as A4.2's Theorem ER_K step 2 modifies it (`(27K₀C_T/8)H³e ≤ 1` replaced by `η_K ≤ 1`, no `d`, and `2K₀(K)e ≤ 1/4` added), holds at every `w_j ≤ w_J` once it holds at `w_J`: `w_J ≥ 5`, `r(1 + k_+)w_J ≤ L/4`, `e(w_J) ≤ r^{1/4} ≤ 1`, `2K₀(K)r^{1/4} ≤ 1/4`, `C_VH²r^{1/4} ≤ 1`, `η_max ≤ 1` (and `C_ηrw_J² = (5/6)η_K(w_J) ≤ 1`). The first, third, fourth and sixth hold for `r ≤ r₁ := min(r₀, e^{−1}, 5^{−16/3}, (8K₀(K))^{−4}, (2K₂(K))^{−8/5})`, the second for `r ≤ r₂(L, K)`, and the fifth is the one condition that sees `Λ`; it is verified in each schedule below.

### 1. The localized band and the sub-layer integrals (conditional as C103 is)

**Lemma 1.1 (A3.11's Lemma 1.1, verbatim).** Fix `t = (γ, B, C)` with `γ ≠ 0`. For every `U > 0` and `x > 0`,

    ∫ 1_T 1{λ ≤ U} 1{|μ| ≤ x} w(y) dλ ≤ 192xU³,                                                              (1.1)

and the left side without the band indicator is at most `12U³`.

*Proof.* A3.11 Lemma 1.1: on the fibre, `c` and `Rq` are fixed, `ψ = 24λ/γ²`, `T` is `{ψ > |c|}`, and `w(y)dλ = (γ⁶/384)(ψ² − c²)dψ` (C103 §3.3). The cubic is C101's, hence C82's; C82 §2's two monotone saddle branches with `dv/dψ = −Z²/48` and C82 §3's coarea density `48(ψ² − c²)/Z² ≤ (4/3)ψ³` for `v ≤ 1/2` (C82 (12)–(14)) give `(16/3)xψ_U³` for the fibre band with `ψ_U = 24U/γ²` and `x ≤ 1/2`, hence `192xU³`; the unbanded sub-layer is `12U³ ≤ 24xU³` for `x > 1/2`. ∎

**Lemma 1.2 (sub-layer moments and edge integrals at compact `K`).** Under the standing conditions, for `w ≥ 5`, the sub-layer `S := T ∩ {λ ≤ U(γ, w)}`, fixed `m, q ≥ 0`, `i ∈ {M, S}` and nonnegative measurable `φ`:

    μ_r(N^mPjet^q1_S) ≤ C_K(w^{−8} + rH³w^{−4}),                                                             (1.2)
    μ_r(N^mPjet^q1_Sφ(a_i)) ≤ C_K∫₀^∞φ(s)(w^{−4}s + rH³w^{−2})ds.                                             (1.3)

*Proof.* C103 §2 and (S14) with the `λ`-range `(0, U]`, `U := U(γ, w) ≤ 4H_γ/w²`. By (S4)–(S5) and the Jacobian `r/k⁴` of (S6), the `N^mPjet^q`-weighted density is at most `C_Ke^{−c|t|²}[w(y)Pjet^{m+q} + rH³Pjet^{m+q+4}]`. Change variables `B → s = a_i` (Jacobian `1/12`); on `T`, `0 < s < 48λ` and `w(y) = s(48λ − s)/16`.
- (1.2): `∫₀^U∫₀^{48λ}[s(48λ − s)/16]ds dλ = 288U⁴` and `∫₀^U∫₀^{48λ}ds dλ = 24U²` (C103 (S13)'s elementary integrals), with `U⁴ ≤ 256H_γ⁴/w⁸` and `U² ≤ 16H_γ²/w⁴`; the Gaussian absorbs `H_γ⁴Pjet^{m+q+4}`.
- (1.3): for fixed `s`, `∫_{s/48}^{U}[(48λ − s)/16]dλ = (48U − s)²/1536 ≤ (3/2)U² ≤ 24H_γ²/w⁴` and `∫_{s/48}^{U}dλ ≤ U ≤ 4H_γ/w²`; so the integrand becomes `C_K[H_γ²w^{−4}s + rH³H_γw^{−2}]Pjet^{m+q+4}e^{−c|t|²}` and the Gaussian absorbs the rest (C103 (S9)'s proof, with the `λ`-interval `(s/48, U]` in place of `(0, Λ]`). ∎

(1.3) is C103 (S9) with `(H², rH⁴)` replaced by `(w^{−4}, rH³w^{−2})`; (1.2) is (S14)'s content for the sub-layer.

**Lemma 1.3 (the sub-layer correlated band at compact `K`).** Under the standing conditions, for `w ≥ 5`, `S_T := D_Λ ∩ T ∩ {γ ≠ 0} ∩ {λ ≤ U(γ, w)}`, fixed `p ≥ 0` and every `δ > 0`,

    μ_r(N^p1_{S_T}1{|μ| ≤ δ}) ≤ C_{K,p}(δw^{−6} + rH³w^{−2}).                                                 (1.4)

*Proof.* A4.2's proof of Lemma JB_K with Lemma 1.1 in place of C82 LB and the `λ`-range `(0, U]`: the error part integrates to `C_prH³U ≤ C_prH³w^{−2}`; for the principal part, `U = U(γ, w)` is constant on the fibre `t`, and Lemma 1.1 bounds the fibre integral by `192δU³ ≤ 12288δH_γ³/w⁶`, which the Gaussian envelope of (S4) integrates. No width restriction is needed (A3.11 Lemma 1.3). ∎

**Lemma 1.4 (the sub-layer decision band without a cut at compact `K`).** Under the standing conditions, for `w ≥ 5`, `S_T` as in Lemma 1.3 and every `δ > 0`,

    μ_r(S_T ∩ {|μ| ≤ δN}) ≤ C_K(δw^{−6} + rH³w^{−2}).                                                         (1.5)

*Proof.* C124's covering in A4.2's Lemma DB_K, over all shells: `1{|μ| ≤ δN} ≤ 1{|μ| ≤ δ} + Σ_{j≥0}4^{−j}N²1{|μ| ≤ 2^{j+1}δ}` (if `2^jδ < |μ| ≤ 2^{j+1}δ ≤ δN` then `N > 2^j`; `μ = −∞` is in no band). Lemma 1.3 with `p = 0` and `p = 2` at every width gives `C_K((1 + 4)δw^{−6} + (1 + 4/3)rH³w^{−2})`. The wide-shell moment `H³a²` of DB_K is not needed on a sub-layer. ∎

### 2. The shell ledger (conditional as C103 is)

Fix `1 ≤ j ≤ J`; write `w := w_j`, `w′ := w_{j−1} = w/2`, `e_j := e(w_j) = 16rw′⁴`, `η_j := η_K(w_j) = 8K₂(K)rw′²`, `U′ := U(γ, w′)` and `S_T^j := D_Λ ∩ T ∩ {γ ≠ 0} ∩ {λ ≤ U′}` (so `D_Λ ∩ S_j^• ∩ T ∩ {γ ≠ 0} ⊂ S_T^j`, by (0.1); `μ_r` lives on `D_Λ`).

**Lemma 2.1.** Under the standing conditions, `r ≤ min(r₁, r₂)` and `C_VH²r^{1/4} ≤ 1`, for `1 ≤ j ≤ J`:
- **(a) The decision band.** `μ_r(S_T^j ∩ (E ∪ Rsec) ∩ {E0(r, w_j) ≥ |μ|/2}) ≤ C_K(rw′^{−2} + rH³w′^{−2})`.
- **(b) The selected margin.** With `ε_j := 2K₀(K)e_j/c_* ≤ C_VH²e_j`, `μ_r(S_T^j ∩ E ∩ {E0(r, w_j) ≥ v/2}) ≤ μ_r(S_T^j ∩ {a_S² ≤ ε_jN}) ≤ C_K(H²r + r^{3/2}H⁴)`.
- **(c) The endpoint strip.** `μ_r(S_T^j ∩ Rsec ∩ ({η_jN(γ² + 72) ≥ a_M} ∪ {η_jN ≥ 1})) ≤ C_K(rw′^{−4} + r^{3/2}H³w′^{−2} + r²H³)`.
- **(d) The Hessian transfer.** `μ_r(T ∩ {H_i^{err}(r, w_j) ≥ τ_i^{tol}}) ≤ C_K(H⁵r²w_j⁴ + H⁷r²w_j²)` for `i ∈ {M, S}`, `τ_M^{tol} = 1`, `τ_S^{tol} = 2/5`.

*Proof.*
- **(a)** By C103 (S12), `E0(r, w_j) ≤ K₀(K)Ne_j`, so the event lies in `S_T^j ∩ {|μ| ≤ 2K₀(K)e_jN}`; Lemma 1.4 at `w′` and `δ = 2K₀(K)e_j = 32K₀(K)rw′⁴` gives `δw′^{−6} = 32K₀(K)rw′^{−2}`.
- **(b)** C103 (S15)'s argument with (1.3) at `w′` in place of (S9)–(S11): on `E`, `v ≥ c_*a_S²`, so `E0 ≥ v/2` forces `a_S² ≤ ε_jN`. Split at `a_S = d₁`; with `(x₁, x₀) := (w′^{−4}, rH³w′^{−2})` the strip costs `x₁d₁²/2 + x₀d₁` and the squared-Markov part with the weight `N²` costs `ε_j²(x₁d₁^{−2}/2 + x₀d₁^{−3}/3)`; at `d₁ = √ε_j` the total is `x₁ε_j + (4/3)x₀√ε_j` (A3.11 Lemma 2.1(b)). Now `x₁ε_j ≤ w′^{−4}·C_VH²·16rw′⁴ = 16C_VH²r` and `x₀√ε_j ≤ rH³w′^{−2}(16C_VH²r)^{1/2}w′² = 4C_V^{1/2}r^{3/2}H⁴`.
- **(c)** A4.1's proof of Lemma B′_K with (1.3) and (1.2), split at `a_M = d := √η_j/w′` instead of `√η_j`, exactly as A3.11 Lemma 2.1(c): the strip `{a_M ≤ d}` costs `x₁d²/2 + x₀d = η_jw′^{−6}/2 + rH³w′^{−3}√η_j`; the Markov event `{N(γ² + 72) > d/η_j}` (the planar strip is `η_jN(γ² + 72) ≥ a_M`, without A3.7's factor `4`) costs `(73²η_j²/d²)·C_K(w′^{−8} + rH³w′^{−4}) = C_K(η_jw′^{−6} + η_jrH³w′^{−2})` by (1.2) at `(m, q) = (2, 4)` and `γ² + 72 ≤ 73Pjet²`; `{η_jN ≥ 1}` costs `η_j²·C_K(w′^{−8} + rH³w′^{−4})`. With `η_j = 8K₂(K)rw′²`: `η_jw′^{−6} = 8K₂rw′^{−4}`, `rH³w′^{−3}√η_j = (8K₂)^{1/2}r^{3/2}H³w′^{−2}`, `η_jrH³w′^{−2} = 8K₂r²H³`, `η_j²w′^{−8} = 64K₂²r²w′^{−4}`, `η_j²rH³w′^{−4} = 64K₂²r³H³`.
- **(d)** C103 (S23) at the deterministic window `w_j`; its hypotheses are (S12) at `w_j`, `C_ηrw_j² = (5/6)η_K(w_j) ≤ 1` and the standing conditions, which §0 supplies for every `w_j ≤ w_J` (the condition `C_VH²e ≤ 1` of (S24) is not used by (S23); it is assumed here for (b) and the schedules). ∎

**Lemma 2.2 (the shell sums).** From A3.11's Lemma 2.2 (the sums used here): `Σ_{j=1}^{J}w_{j−1}^{−2} ≤ 4/75`, `Σ_{j=1}^{J}w_{j−1}^{−4} ≤ 16/9375`, `Σ_{j=1}^{J}w_j⁴ ≤ (16/15)w_J⁴`, `Σ_{j=1}^{J}w_j² ≤ (4/3)w_J²`, `J ≤ 2log(1/r) − 1`, `w_J⁴ ≤ r^{−3/4}`, `w_J² ≤ r^{−3/8}`, `w_J^{−8} ≤ 256r^{3/2}`, `w_J^{−4} ≤ 16r^{3/4}`.

### 3. The fixed layer at `O(r⁴log(1/r))`

**Theorem SE″_K (the sector errors by shells).** Under the standing conditions and `r ≤ min(r₁, r₂)`, with `C_VH²r^{1/4} ≤ 1`, define

    Good^{E″} := ⋃_{j=0}^{J}(S_j^E ∩ Good_sel(r, w_j)),      Good^{R″} := ⋃_{j=0}^{J}(S_j^R ∩ Good_LE,K(r, w_j)),

where `Good_sel(r, w) := E ∩ {Rbox ≤ w, E0(r, w) < min(v, −μ)/2, H_M^{err}(r, w) < 1, H_S^{err}(r, w) < 2/5}` is C103 §4's selected good event and `Good_LE,K(r, w)` is A4.1's Corollary LE_K event. Then `D_f(M_r) = f(S_r)` on `Good^{E″}` and `D_f(M_r) > f(S_r)` on `Good^{R″}` (so, on the Morse locus, `H_r` holds on the first and fails on the second), and

    μ_r(E ∖ Good^{E″}) ≤ C_K[r^{3/2} + r^{7/4}H³ + H⁵r^{5/4} + H⁷r^{13/8} + rH⁴ + H²r log(1/r) + r^{3/2}H⁴log(1/r) + H⁵r^{3/2}],   (3.1)
    μ_r(Rsec ∖ Good^{R″}) ≤ C_K[r^{3/2} + r^{7/4}H³ + rH⁴ + H³r + r^{3/2}H⁴ + r²H³log(1/r)].                                  (3.2)

*Proof.* The certificates are C103 §4's (selected: C95's interface `G` through (S25); rejected: A4.1 Corollary LE_K), each applied at the deterministic window `w_j` on its shell, where the radius condition holds by definition of the shell. The shells partition each sector, so `E ∖ Good^{E″} ⊂ S_top^E ∪ ⋃_j(S_j^E ∖ Good_sel(r, w_j))`, and on `S_j^E`

    S_j^E ∖ Good_sel(r, w_j) ⊂ {E0(r, w_j) ≥ v/2} ∪ {E0(r, w_j) ≥ −μ/2} ∪ {H_M^{err}(r, w_j) ≥ 1} ∪ {H_S^{err}(r, w_j) ≥ 2/5},

(C103 §4: `E0 < min(v, −μ)/2` fails only if one of the two halves fails); likewise `S_j^R ∖ Good_LE,K(r, w_j) ⊂ {E0(r, w_j) ≥ μ/2} ∪ {η_jN(γ² + 72) ≥ a_M} ∪ {η_jN ≥ 1}`.
1. **The tops.** C103 (S14) at `w_J` and Lemma 2.2: `C_K(w_J^{−8} + rH³w_J^{−4}) ≤ C_K(r^{3/2} + r^{7/4}H³)`.
2. **The Hessians, summed** (elder side). Lemma 2.1(d) for `j ≥ 1` and (S23) at `w_0 = 5` for `j = 0`: `Σ_{j=0}^{J}(H⁵r²w_j⁴ + H⁷r²w_j²) ≤ C_K(H⁵r²w_J⁴ + H⁷r²w_J²) ≤ C_K(H⁵r^{5/4} + H⁷r^{13/8})`.
3. **The margins, summed** (elder side). Lemma 2.1(b) for `j ≥ 1`: `C_K(H²r + r^{3/2}H⁴)` per shell, `J ≤ 2log(1/r)` shells; (S15) at `e_0 = 625r` for `j = 0`: `C_K(H⁴r + H⁵r^{3/2})`.
4. **The decision bands, summed** (both sides). Lemma 2.1(a) for `j ≥ 1` and Lemma 2.2: `C_K(r + rH³)`; A4.2's Lemma DB_K at `e_0 = 625r` for `j = 0` (its hypothesis `2K₀(K)e_0 ≤ 1/4` holds for `r ≤ r₁`): `C_K(r + rH⁴ + H³r²) ≤ C_KrH⁴`.
5. **The endpoint strips, summed** (rejected side). Lemma 2.1(c) for `j ≥ 1` and Lemma 2.2: `C_K(r + r^{3/2}H³ + r²H³log(1/r))`; A4.1's Lemma B′_K at `η_0 = 50K₂(K)r` for `j = 0`: `C_K(H³r + rH⁴√r)`.
Add (with `H⁴r ≤ rH⁴`, `rH³ ≤ rH⁴`, `r^{3/2}H³ ≤ r^{3/2}H⁴`). Multiply by `r³/z_r ≤ 2r³/z_*` (C103 (S6)–(S7)) for `Q_r^W`. ∎

**Theorem SE″_K, continued (the fixed layer).** For fixed `Λ ≥ 1`, uniformly over `b ∈ B₀`, `k ∈ K` and frames, for `0 < r ≤ r_{K,Λ}`,

    Q_r^W(D_Λ ∩ (H_r Δ E)) ≤ C_{K,Λ}r⁴log(1/r),                                                                (3.3)

and C103 (S28)'s two comparisons hold with `C_{K,Λ}r log(1/r)` in place of `C·Rerr`.

*Proof.* C103 §4's inclusion `D_Λ ∩ (H_r Δ E) ⊂ (E ∖ Good^{E″}) ∪ (Rsec ∖ Good^{R″}) ∪ (D_Λ ∩ T^c)` up to the null sets (S26) and `{γ = 0}` and the `Q_r^W`-null non-Morse locus, with the two certificates; (S8) bounds the leakage by `C_KrH⁴`. At fixed `Λ` every term of (3.1)–(3.2) is `O(r log(1/r))` once `r ≤ r_{K,Λ} := min(r₁, r₂, (C_VH²)^{−4}, k_-/H)` (the last entry is the standing condition `rH/k_- ≤ 1`). ∎

At fixed `Λ` the exponents of (3.1), in the order displayed, are `3/2, 7/4, 5/4, 13/8, 1, 1⁻, 3/2⁻, 3/2` (a minus marks a logarithm), and those of (3.2) are `3/2, 7/4, 1, 1, 3/2, 2⁻`. A4.2's and C124's eleven-term ledgers (`R_*^K`, (15)) are replaced: the radius tail `w^{−8}` and the window error `e` no longer meet, and the exponent `11/3` of C124 (4) becomes `4` up to the logarithm.

### 4. The exhaustion

**The ledger.** Under the standing conditions, `r ≤ min(r₁, r₂)` and `C_VH²r^{1/4} ≤ 1`, define

    R_*^{K″}(r, H) := rH⁴ + H²r log(1/r) + H⁵r^{5/4} + r^{3/2}H⁵ + r^{3/2}H⁴log(1/r) + H⁷r^{13/8} + r^{7/4}H³ + r²H³log(1/r).   (4.1)

Every term of (3.1)–(3.2) is bounded by a constant times a term of (4.1) (`H³r ≤ rH⁴`, `r^{3/2} ≤ r^{3/2}H⁵`, `r^{3/2}H⁴ ≤ r^{3/2}H⁵`).

**Proposition 4.1 (the layer comparison).** Under those conditions,

    r^{−3}Q_r^W(D_Λ ∩ (H_r Δ E)) ≤ C_KR_*^{K″},      ‖ν_r^F|_{D_Λ} − ν_0^F|_{D_Λ}‖_var ≤ C_KR_*^{K″}.                    (4.2)

*Proof.* C103 (S28) with (3.1)–(3.2) in place of (S27), as A4.2's Theorem ER_K step 1 uses it with `R_*^K`: the first bound is Theorem SE″_K's inclusion with the leakage (S8); the second replaces `1_{F_r}` by `1_{Rsec}` on the typed domain, adds the off-`T` leakage, and uses (S8)'s normalized density comparison `C_KrH⁴` against the fixed raw-jet indicator `Rsec`. ∎

**Theorem QFE″_K (every `β < 1`).** Fix `β ∈ (0, 1)`. There are `C_{K,β} < ∞` and `r_{K,β} > 0`, uniform over `b ∈ B₀`, `k ∈ K` and frames, such that for `0 < r ≤ r_{K,β}`

    ‖ν_r^F − ν_0^F‖_var ≤ C_{K,β}r^β,      1 − p_r = r³(α₁ + α₂) + O_{K,β}(r^{3+β}),                                 (4.3)

and the raw-jet law conditional on failure converges at the same rate.

*Proof.* A4.1's proof of Theorem QFE′_K with Proposition 4.1 and the schedule `α := (1 − β)/8`, `Λ := r^{−α}` (so `H ≤ 2r^{−α}`); the tails are A4.2's Lemma FT_K, `ν_r^F(D_Λ^c) + ν_0^F(D_Λ^c) ≤ C_Ke^{−c_Kr^{−α}} + C_Kr = O(r)`. With `H` replaced by `r^{−α}` the `r`-exponents of (4.1) are:

| term | exponent | at least `β` because |
|---|---|---|
| `rH⁴` | `(1 + β)/2` | `β ≤ 1` |
| `H²r log(1/r)` | `(3 + β)/4`, minus a logarithm | `β < 1` strictly |
| `H⁵r^{5/4}` | `5/8 + 5β/8` | `β ≤ 5/3` |
| `r^{3/2}H⁵` | `7/8 + 5β/8` | `β ≤ 7/3` |
| `r^{3/2}H⁴log(1/r)` | `1 + β/2`, minus a logarithm | `β < 2` |
| `H⁷r^{13/8}` | `3/4 + 7β/8` | `β ≤ 6` |
| `r^{7/4}H³` | `11/8 + 3β/8` | `β ≤ 11/5` |
| `r²H³log(1/r)` | `13/8 + 3β/8`, minus a logarithm | `β < 13/5` |

The conditions hold for small `r`: `rH/k_- ≤ 2r^{(7 + β)/8}/k_- ≤ 1`, `C_VH²r^{1/4} ≤ 4C_Vr^{β/4} ≤ 1`, `w_max ≥ 5`, `r ≤ e^{−1}`. Combine (4.2) with FT_K: `‖ν_r^F − ν_0^F‖_var ≤ C_KR_*^{K″} + O(r) ≤ C_{K,β}r^β`. The second statement is `φ = 1` (C103 (S34)), and the conditional one uses C103 §6's floor `α₁ + α₂ ≥ M_*` as in A4.2 step 5. ∎

**Theorem ER′_K (the endpoint).** There are `C_K < ∞` and `r_K ∈ (0, e^{−1}]`, uniform over `b ∈ B₀`, `k ∈ K` and frames, such that for `0 < r < r_K`

    ‖ν_r^F − ν_0^F‖_var ≤ C_Kr log(1/r)⁴,      1 − p_r = r³(α₁ + α₂) + O_K(r⁴log(1/r)⁴),                              (4.4)

and the raw-jet law conditional on failure converges at the same rate.

*Proof.* A4.2's Theorem ER_K step 4 with Proposition 4.1: `Λ := D_Klog(1/r)` with `D_K ≥ 1` so large that both tails of FT_K are `O(r)`; `H ≤ (1 + D_K)log(1/r)`; `C_VH²r^{1/4} ≤ 1` for small `r`. In (4.1), `rH⁴ ≤ C_Kr log(1/r)⁴`, `H²r log(1/r) ≤ C_Kr log(1/r)³`, and every other term is `r^{1+a}` times a power of `log(1/r)` with `a ≥ 1/4`, hence `O(r)`. ∎

The coefficient `α₁ + α₂` is C103 §6's (CUB G11), unchanged.

### 5. Corollary PD_ER′ (conditional on Theorem ER′_K, as PD_ER is on ER_K)

In Corollary PD's setting (births in a compact interval `B` of positive length, gaps in `K` with `k_- < k_+`, orientations in `S¹`, its `C_fail` and `c_cand`): there are `ℓ_* ∈ (0, e^{−1}]` and `C < ∞`, depending only on `L`, `B` and `K`, such that for `0 < ℓ, t < ℓ_*`:
- **(i)** `|ν_rej(ℓ) − C_failℓ^{2/3}| ≤ Cℓ log(1/ℓ)⁴`;
- **(ii)** `|EN_rej(0, t] − (3/5)C_failt^{5/3}| ≤ 6Ct²log(1/t)⁴`;
- **(iii)** for every real `q > −5/3`, `|EΣ_{nonselected, ℓ≤t}ℓ^q − C_failt^{q+5/3}/(q + 5/3)| ≤ 8139·Ct^{q+2}log(1/t)⁴`;
- **(iv)** `ν_rej(ℓ)/ν_cand(ℓ) = (C_fail/c_cand)ℓ + O(ℓ^{4/3}log(1/ℓ)⁴)`;
- **(v)** for each fixed `β ∈ (0, 1)` there are `ℓ_β` and `C_β` such that (i)–(iv) hold for `ℓ, t < ℓ_β` with `C_βℓ^{(2+β)/3}`, `C_βt^{(5+β)/3}`, `C_βt^{q+(5+β)/3}` and `C_βℓ^{1+β/3}` in place of the logarithmic errors.

PD's (o) is unchanged.

*Proof.* A4.2's proof of Corollary PD_ER with (4.4) and (4.3) in place of Theorem ER_K: `|ϱ_r − a_fail| ≤ C_Kr log(1/r)⁴` for `r < r_K`, and PD's conversion `r ≤ k_-^{−1/3}ℓ^{1/3}`, `log(1/r) ≤ (2/3)log(1/ℓ)` (for `k_+ ≤ 1/ℓ`) gives `r log(1/r)⁴ ≤ (2/3)⁴k_-^{−1/3}ℓ^{1/3}log(1/ℓ)⁴`. PD's step 4: the `(A_r − A_0)` term is `O(ℓ^{1/3})`, absorbed since `log(1/ℓ) ≥ 1`; so `|ℓ^{−2/3}ν_rej − C_fail| ≤ Cℓ^{1/3}log(1/ℓ)⁴`, which is (i). PD's step 5 with `ℓ = ts`: `log(1/ℓ)⁴ ≤ log(1/t)⁴(1 + log(1/s))⁴`, so the error integral is at most `Ct^{q+2}log(1/t)⁴∫₀¹s^{q+1}(1 + log(1/s))⁴ds`, and with `s = e^{−x}` the last integral is `Σ_{j=0}^{4}C(4, j)j!/(q + 2)^{j+1}`, finite exactly when `q > −2`; for `q > −5/3`, `q + 2 > 1/3`, so it is at most `Σ_jC(4, j)j!3^{j+1} = 8139`, and at `q = 0` it is `Σ_jC(4, j)j!/2^{j+1} = 21/4 < 6`. PD's step 6 gives (iv), and its step 7 with (4.3) gives (v), with `1/(q + (5 + β)/3) ≤ 3/β`. ∎

### 6. Remarks

1. **What binds.** As in A3.11 Remark 1: at fixed `Λ` the margins' sum `H²r log(1/r)` (one `≍ H²r` per shell, from the quadratic tolerance floor `v ≥ c_*a_S²` of C103 (S15)); in the exhaustion the layer law's `rH⁴` ((S8), from (S5)'s `rH³` and the layer's length), whence the fourth power of the logarithm. Neither is removed here.
2. **What transfers and what does not.** The shells, Lemma 1.1 and the sub-layer integrals transfer because C103's fibre identity and edge integrals have A3.8's shape with `(H², rH⁴, rH³)` for `(H², rH⁷, rH⁶)`; the planar chain has no barrel, no `λ₂`-band and no hard-gap term, so the elder side has three pieces (margin, level, Hessians) instead of A3.6's seven. A3.11's `w_max = r^{−3/16}` was forced by A3.5's Theorem G₃; here any `w_max = r^{−ω}` with `1/8 ≤ ω < 1/4` would do for the fixed layer and the endpoint, and for Theorem QFE″_K with `α` re-chosen so that `C_VH²e(w_J) ≤ 1` survives (`(1 − 4ω) − 2α > 0`); `3/16` is kept for uniformity with A3.11 (it makes `e(w_J) ≤ r^{1/4}`).
3. **The compact-`K` dependence** is A4.2's: through `K₀(K)`, `K₂(K)`, `C_V`, `C_η`, C102's Gaussian constants and [P]'s tail constants, and the two conditions `rH/k_- ≤ 1`, `r(1 + k_+)w ≤ L/4`. Nothing is claimed as `k_- → 0`.
4. **At `k = 1`** (C124's setting, `K = {1}`), the same statements hold with C124's constants `K₀ = 167/192`, `K₂ = 115/48`: C124's Theorem ER (3)–(4) with `r log(1/r)⁴`, `r⁴log(1/r)⁴` and `r⁴log(1/r)` in place of `r^{2/3}log^{8/3}`, `r^{11/3}log^{8/3}` and `r^{11/3}`.
5. **Not optimized.** No sharpness, no removal of the logarithms, no exponent above `1` in `r`.

### 7. Checks

**Controls** (`a43_exact.py`, posted below; standard library only, exact rationals except Z5's floating-point shell counts and Z7's Simpson check): Z1 Lemma 1.1's constants in the planar fibre identity (the same `192U³`, `12U³`); Z2 the planar sub-layer integrals (`288U⁴`, `24U²`, `(48U − s)²/1536 ≤ (3/2)U²`), the radius sub-layer (0.1) (`(25/96) ≤ 3/8`; `w − 5/2 ≥ w/2`), and `H_γ ≤ 54Pjet²`; Z3 Lemma 2.1(b)'s split total `x₁ε + (4/3)x₀√ε` and the shell values `16C_VH²r`, `4C_V^{1/2}r^{3/2}H⁴`; Z4 Lemma 2.1(c)'s optimization `d = √η/w′` and its five shell values; Z5 Lemma 2.2's sums and `J ≤ 2log(1/r) − 1`; Z6 the exponent table of Theorem QFE″_K (the eight closed forms for `α = (1 − β)/8`, all `≥ β`, the three logarithmic ones `> β`), the derived `(r, log)`-powers of (4.1) for ER′_K (`rH⁴ → (1, 4)`, `H²r log(1/r) → (1, 3)`, every other term `r^{≥5/4}`), the four inequalities named after (4.1) and the two exponent lists after (3.3), and the side conditions' exponents (`(7 + β)/8`, `β/4`); Z7 Corollary PD_ER′'s constants (`Σ_jC(4, j)j!3^{j+1} = 8139`, `Σ_jC(4, j)j!/2^{j+1} = 21/4`, `(2/3)⁴ = 16/81`) with a Simpson check of the integral identity at `q = 0`; Z8 the `k = 1` constants of Remark 4 (`K₀(1) = 167/192`, `K₂(1) = 115/48` from C103 (S12), `η_K = (115/24)rw²`). Mutants M1–M10 exit 1 naming their group; any other argument exits 2. Lemma 1.1's numerics are A3.11's Z9 and exploration (the cubic is the same).

**Referee** (one clean-context pass, same provider and session; not review evidence): see the controls comment.

### 8. Not claimed

- No new estimate: every bound is C103's, A4.1's, A4.2's or A3.11's, read shell by shell.
- No removal of the logarithms; no exponent above `1` in `r`; no sharpness.
- No `k_- → 0`, no growing `K` or `L`, no `d ≥ 3` statement (A3.11 is the `d = 3` note); no replacement-bar, once-counted-bar or real-valued-mark statement.
- No change to C103, C124, A4, A4.1, A4.2, PD or PD_ER: their statements stand; this note supersedes their rates where it is cited.

### 9. Review request

Two bounded slices; one reader may take both. Please claim first (a pickup naming the two body SHAs), then post PASS / AMEND (with the exact change) / BLOCK (with the reason), the scope actually checked and what was not checked, and disclose provider, model and session.
- **Slice 1 (§§0–3).** (0.1) against C101 §4.1 and C103 (S13); Lemmas 1.2–1.4 against C103 §2, (S14), A4.2 Lemmas JB_K/DB_K and A3.11 Lemmas 1.1–1.4; Lemma 2.1 against C103 (S15), (S23), A4.1 Lemma B′_K and A3.11 Lemma 2.1; Theorem SE″_K's inclusions against C103 §4 and A4.1 Corollary LE_K (the three-piece elder side, the three-piece rejected side, the tops, the sums); control groups Z1–Z5.
- **Slice 2 (§§4–5).** (4.1), Proposition 4.1 against C103 (S28)/A4.2 step 1; Theorems QFE″_K and ER′_K against A4.1 Theorem QFE′_K and A4.2 Theorem ER_K (the table, the side conditions, FT_K's tails, the power `4`); Corollary PD_ER′ against A4.2 §3 and PD §2 (the constants `21/4`, `8139`, `(2/3)⁴`, the thresholds); §§6 and 8 for overclaim; control groups Z6–Z8.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_