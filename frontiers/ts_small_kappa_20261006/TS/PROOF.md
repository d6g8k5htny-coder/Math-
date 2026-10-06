# Lifetime note TS: the `κ ≤ 1` side of IBA2-009 (TAIL-S), a rescaled elder barrier, and the elder and rejected densities with remainder `ℓ^{4/7}log(1/ℓ)`

Object: `CL-TS-SMALL-KAPPA-20261006-v1`. Claim: main#229 6019827162; pickup on main#259 6019832792.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 6 October 2026, for Dylan Roy (delegated AI
work). The author also wrote [K], [N] (#240), #237, #242–#244 and note TL.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph, STATUS,
PROOF_INDEX, prize or Boolean change; no numerical constant is certified. Same GitHub account as every lane;
organizational independence 0.

**What is new.**
- **Lemma S″** (§1). For `0 < r ≤ r_0^*`, `b ∈ R` and `0 < k ≤ r`,
  `E_Q[(W_r/r²)e] ≤ Cr²(κ + r)κ^{2/3}P^N`.
  - #220's Lemma S′ gives `Cℓ^{2/3}r^{−2}(κ + r)P^N = Cr^{2/3}(κ + r)κ^{2/3}P^N`, so the gain is the factor `r^{4/3}`.
  - The barrier of [182] §3 is run in [N]'s window coordinates `(X, Ξ)`. There the pins make every third derivative
    `O(𝒩)`, while in the original coordinates the barrier pays for `‖D³f‖` in every direction. So an elder pair needs
    `λ_min(−H̃) ≤ C𝒩^{2/3}κ^{1/3}` instead of Lemma S′'s `Cℓ^{1/3}r^{−2}𝒩^{2/3} = Cκ^{1/3}r^{−2/3}𝒩^{2/3}`.
- **Theorem TL⁻** (§§2–4). For each `θ ∈ (0, 1)`, `|𝐓_r^{rej}(k, u) − 𝓐^{rej}(κ, u)| ≤ C_θ(κr² + r³/κ)` for `0 < r ≤ r₀`
  and `r^θ ≤ κ ≤ 1`.
  - This is note TL's Theorem for `κ ≤ 1`. For `κ ≥ r^{1/2}` the error is at most `2κr²`, which is `O((r/κ)²)` relative to
    the size `κ³` of `𝓐^{rej}`.
  - The proof is TL's, with `κ ≤ 1` scalings: the good event asks `𝒩 ≤ c₁₃κ/r` and `|Δ| ≥ C₁₂(r/κ)𝒩^{N₂}(1 + ‖B‖)`; the
    windows of the cusp weight are intervals in `f₄` of length `O(κ)`, on which the density of `f₄` carries the factor
    `(1 + |q|)^{−N}`; and the edge shift is expanded in `f₄`, whose density varies on the scale `1 ≥ κ`. No radial
    parametrization is needed.
- **Corollary TS** (§5). `ν_eld(ℓ) = cℓ^{−1/3} + c₁ℓ^{1/4} + c₂ℓ^{1/3} + ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{4/7}log(1/ℓ))`, and
  `ρ_rej` likewise. This improves TL's `ℓ^{4/9}log(1/ℓ)`. For SIDE24 the relative remainder is `O(ℓ^{19/21}log(1/ℓ))`.
- **Corollary TS′** (§5). Neither density has a term of order `ℓ^{1/2}`. With note TL (the `κ ≥ 1` side), this is the
  global statement that IBA2-009 asks for, at the scope of the consumed packets.
- **Bookkeeping.** In TL's decomposition (5.1), the term `J₄` and the cusp tail of #237's main term are both of order
  `ℓ²ρ^{−7}`, with opposite signs. By #237 Lemma K and Lemma R (R.2), `r^{−2}𝐀₀(κr, u) − 𝓐^{con}(κ, u) = O(κ²k²)` exactly. So
  TL's ledger row `ℓ²ρ^{−7}` cancels, and the split can move to `ρ = ℓ^{3/14}`.

**Not claimed.**
- No sharpness of `4/7`. It is fixed by the intermediate elder mass, where #229's typed bound and Lemma S″ balance at
  `a = ℓ^{1/7}` (Remark 1).
- Nothing pointwise in `b`. No identification of further terms of either density.
- No certified numerical value, and no uniformity in `d` or `L`.
- Whether IBA2-009 closes is for the audit's owners, after nonauthor reads. This note changes no status.
- Nothing beyond the existential scope of the consumed packets.

**Consumed.** Packets on Math- `main` (blob identities checked at `08f86862`), and note TL as posted:
- note TL, main#229 6017975404 (served body `9cb199e0…468f`; read in three slices with no amendment; custody packet
  Math-#384): §0 (notation, (0.1)–(0.2), Theorem TL, Corollary TL1); §1 (facts (B1)–(B5), the class `𝔏`, (1.1)); §2 (the
  weight `G_r` (2.1)–(2.2), Lemma GE and Proposition RW, whose proofs §2 here modifies); §3 ((3.0) and the parity
  `G_s(E, −O) = G_{−s}(E, O)`); §4 (Steps 1–6); §5 ((5.1) and its terms).
- [N] = #240 `frontiers/elder_cusp_parity_20261002/PROOF.md` (blob `16a1db06`): §0 notation and (0.1); §1, the window
  coordinates `Φ(X, Ξ) = rXu + r²ΘΞ`, `𝔉 = r^{−4}(f∘Φ − b)`, and Lemma Q′; §3 Lemma R₂, the model near the edges and
  Lemma Q″; §4 Lemma Ω.
- #237 `frontiers/candidate_parity_rate_20261001/PROOF.md` (blob `a97bf528`): Lemma R (R.1)–(R.4); Lemma K (K.1) and its
  proof (the value at `r = 0`); Lemma D′; Lemma U (U.1) with its radius `r₃`; §5's main-term computation; Theorem P (P.1).
- #229 `frontiers/third_order_rate_20261001/PROOF.md` (blob `110ed33a`): Proposition W⁺, (W⁺.1)–(W⁺.2), with (4.1)–(4.2)
  of its proof.
- #220 `frontiers/elder_third_order_20261001/PROOF.md` (blob `c8767dde`): §0 (the near/far identity for `ν_eld` at
  `r_0 = r_0^*`); Lemma H (a)–(b); the proof of Lemma S′; (F1).
- #198 `frontiers/remainder_rate_20260930/PROOF.md` (blob `abfb98ae`) and [182]
  `frontiers/fixed_r_inverse_lifetime_20260930/PROOF.md` (blob `0d401877`): the maximin death level [182] (2) and the
  barrier [182] §3, as #198 §1 uses them; #198 §3's sign window.
- #218 `frontiers/candidate_third_order_20261001/PROOF.md` (blob `70ca57ef`): Lemma D; Step C1; (0.1) (the definition of
  `c₂`).
- #242 `frontiers/soft_rejected_pairs_20261002/PROOF.md` (blob `271412db`): §0, with the identity
  `I^{cand} − c₁ = ∫_0^∞∫∫𝒜^{rej}(b, s^{−4}, u) db dσ(u) ds`.
- #187 `frontiers/far_elder_rate_20260930/PROOF.md` (blob `07260114`): the far bound, for the last form of (TS.1) only.
- [R] `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`): (R5), the Gaussian bound on `π_r(v_r)`.

**Cited only.** Math-#296 `reviews/iba2_009_matching_20261005/REPORT.md` (blob `a0b398f5`), §§1 and 4 (the matching problem
and its sufficient criterion); main#259 6001313460 (agent 3's TAIL-S obstruction), 6001580409 and 6001189633; [N] Remarks 1
and 4; #237 Remarks 3–4; #229 Remark 1; [K] (K2) through note TL.

**Prior work and overlap** (searched before drafting, as this lane's rule requires: the tree of `main`, the project
archive, and main#229 and main#259 for claims since TL's delivery 6018024601). No packet or claim bounds the rejected
kernel uniformly as `κ → 0`, or improves the `r`-dependence of #220's Lemma S′. [N] Remark 1 and agent 3's obstruction
record why Theorem N does not reach `κ → 0`; their third point, the intermediate elder mass, is what Lemma S″ addresses.

## 0. Setting and statement

Setting and notation are those of note TL §0, which follows [N] §0, #237 §§0–1 and #242 §0. Fix `d ≥ 2`, `m := d − 1`,
`L > 0` and the [P] field on `X = R^d/(LZ^d)`. The near pins are `M = −ru/2` (a maximum) and `S = ru/2` (an index-`m`
saddle) at gap `k`, so `f(M) − f(S) = kr³`; `κ := k/r` and `ℓ = kr³ = κr⁴`.
- *Kernels.* `A_r`, `A_r^{eld}`, `A_r^{rej} = A_r − A_r^{eld}` and the weight `ω_r = r^{−2}F_d(K_M)F_{d−1}(K_S)` are TL's.
  The elder mark is `e = 1{d_f(M) = f(S)}`, where `d_f(M)` is the maximin death level of [182] (2):
  `d_f(M) = sup{min_t f(γ(t)) : γ(0) = M, f(γ(1)) > f(M)}`.
- *Birth-integrated kernels.* `𝐓_r(k, u) := ∫r^{−2}A_r db` (#237), `𝐓_r^{rej}` (TL (0.1)) and
  `𝐓_r^{eld} := 𝐓_r − 𝐓_r^{rej} = ∫r^{−2}A_r^{eld} db`.
- *Cusp side.* `𝓐^{rej}(κ, u)` is TL (0.2). For `* ∈ {cand, eld, con}` put `𝓐^*(κ, u) := ∫_R𝒜^*(b, κ, u) db`, so that #237's
  `𝓐 = 𝓐^{cand} − 𝓐^{con}` and `𝓐^{rej} = 𝓐^{cand} − 𝓐^{eld}`. `𝐀₀(k, u)` and `𝐀₂(k, u)` are #237 Lemma K's.
- *Jets* ([N] §0, TL §0): `A`, `B`, `γ`, `η`, `f₄`, `f₅`, `Δ = det A`, `λ = λ_min(−A)` on `{A < 0}`, `Γ̃`, `q`, `z = f₄ − 3q`,
  `Q₁`, `P₁ = Δ²Q₁` and `w₀ = (Δ²/144)(5184κ² − z²)`. On `{A < 0}`, `z = f₄ + 3|q|`. `J′` is the vector of free jets of
  order `≤ 9`, `J″ := J′ ∖ {f₄}` and `J‴ := J″ ∖ {A}`.
- *Window coordinates* ([N] §1). With `Θ` an orthonormal frame of `u^⊥`, `Φ(X, Ξ) := rXu + r²ΘΞ` and
  `𝔉 := r^{−4}(f∘Φ − b)`. Then `M = Φ(−½, 0)`, `S = Φ(½, 0)`, `𝔉(−½, 0) = 0` and `𝔉(½, 0) = −κ`.
- *The rescaled Hessian* (#220 Lemma H). `H_M := D²f(M)`, `Λ_r := diag(r, 1, …, 1)` in the frame `(u, Θ)` and
  `H̃ := Λ_r^{−1}H_MΛ_r^{−1}`.
- *Constants.* `C, c, N` depend only on `d` and `L` (and on `θ`, `p` where indicated), may change from line to line, and
  never depend on `r`, `k`, `κ`, `b` or `u`. `P := 1 + |b| + k`. In §1, `𝒩_r := 1 + k + ‖F_r‖_{C⁹}` as in #220; in §§2–4,
  `𝒩` is TL §1's (the two differ by the factor `C_L` there).

**Lemma S″ (the elder weight through a rescaled barrier).** For `0 < r ≤ r_0^*`, `b ∈ R`, `u ∈ S^{d−1}` and `0 < k ≤ r`,

    E_Q[(W_r/r²) e] ≤ C r² (κ + r) κ^{2/3} P^N,                                                                     (S″.1)
    0 ≤ r^{−2}A_r^{eld}(b, k, u) ≤ C (κ + r) κ^{2/3} (1 + |b|)^N e^{−cb²},        0 ≤ 𝐓_r^{eld}(k, u) ≤ C (κ + r) κ^{2/3}.   (S″.2)

**Theorem TL⁻ (the rejected kernel for `κ ≤ 1`).** For every `θ ∈ (0, 1)` there are `r₀ > 0` and `C` such that for
`0 < r ≤ r₀`, `r^θ ≤ κ ≤ 1` and `u ∈ S^{d−1}`,

    |𝐓_r^{rej}(k, u) − 𝓐^{rej}(κ, u)| ≤ C (κr² + r³/κ).                                                              (TL⁻)

**Corollary TS (the elder and rejected densities).** As `ℓ ↓ 0`,

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{4/7} log(1/ℓ)),                       (TS.1)
    ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁) ℓ^{1/4} − ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{4/7} log(1/ℓ)).                              (TS.2)

With #187 (`0 ≤ ν_eld^{far,r_0^*} ≤ Cℓ^{2/3}`) the far terms may be dropped. For the SIDE24 law (`d = 3`, `L = 24`) this
reads `ν_{3,24}(ℓ) = cℓ^{−1/3}(1 + (c₁/c)ℓ^{7/12} + (c₂/c)ℓ^{2/3} + O(ℓ^{19/21}log(1/ℓ)))`, against TL's `O(ℓ^{7/9}log(1/ℓ))`.

**Corollary TS′ (no term of order `ℓ^{1/2}`).** If `ν_eld(ℓ) = cℓ^{−1/3} + c₁ℓ^{1/4} + c₂ℓ^{1/3} + eℓ^{1/2} + o(ℓ^{1/2})`,
then `e = 0`. If `ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + e′ℓ^{1/2} + o(ℓ^{1/2})`, then `e′ = 0`.

*Proof.* `4/7 > 1/2`, and the far terms are `O(ℓ^{2/3})`. ∎

So the matched residual of the elder density, and of the rejected density, is `O(ℓ^{4/7}log(1/ℓ)) = o(ℓ^{1/2})`. That is
the conclusion Math-#296's sufficient criterion (4.1)–(4.2) was designed to give, proved here directly by the decomposition
of §5, with Theorem TL on `κ ≥ 1`, Theorem TL⁻ on `ℓ^{1/7} ≤ κ ≤ 1` and Lemma S″ beyond.

## 1. A rescaled barrier: proof of Lemma S″

Fix `0 < r ≤ r_0^*`, `b`, `u` and `0 < k ≤ r`, and let `f = F_r` under `Q`. Recall `r_0^* ≤ r_0^{[R]} ≤ 1` and
`r_0^* ≤ L/(4√2)` (#220, proof of Lemma S′). Let `C₀ = C₀(d) ≥ 1` be such that every derivative of `f` of order `j ≤ 9` along
unit vectors `v₁, …, v_j` is at most `C₀‖f‖_{C⁹}` in absolute value, and every gradient of such a derivative with `j ≤ 8`
is at most `C₀‖f‖_{C⁹}` in norm. (Only orders `≤ 4` are used.)

*Step 1 (the pins at third order).* Put `g(t) := f(M + tu)` for `0 ≤ t ≤ r`. The pins give `g(0) = b`, `g(r) = b − kr³` and
`g′(0) = g′(r) = 0`, and `|g⁗| ≤ C₀𝒩_r` on `[0, r]`. Taylor's formula at `0`, for `g` and for `g′`, gives

    g(r) = b + g″(0)r²/2 + g‴(0)r³/6 + R₄,    g′(r) = g″(0)r + g‴(0)r²/2 + R₃′,    |R₄| ≤ C₀𝒩_r r⁴/24,  |R₃′| ≤ C₀𝒩_r r³/6.

So `g(r) − b − (r/2)g′(r) = −g‴(0)r³/12 + R₄ − rR₃′/2`. The left side is `−kr³`, hence

    |∂_u³f(M) − 12k| = |g‴(0) − 12k| = 12|R₄ − rR₃′/2|/r³ ≤ (3/2) C₀𝒩_r r.                                           (1.1)

(Control S1 checks (1.1) on pinned polynomials, where the identity `g‴(0) − 12k = 12(R₄ − rR₃′/2)/r³` is exact. The constant
`3/2` is crude: the Peano kernel of `R₄ − rR₃′/2` is `−(r − t)²(r + 2t)/12`, of one sign, so the sharp constant is `1/2`,
attained for constant `g⁗`. Nothing below depends on it.)

*Step 2 (third derivatives in window coordinates).* Write `M̂ := (−½, 0)` and `ξ := (X, Ξ) − M̂`. By the chain rule,
`∂_X^a∂_Ξ^β𝔉 = r^{a + 2|β| − 4}(∂_u^a∂_Θ^βf)∘Φ`. In particular `D²𝔉(M̂) = r^{−4}DH_MD` with `D := diag(r, r², …, r²)`,
which is `H̃` (entrywise: `r^{−2}∂_u²f(M)`, `r^{−1}∂_u∇_Θf(M)`, `D_Θ²f(M)`; control S2). Also `∇𝔉(M̂) = 0` and
`𝔉(M̂) = 0`. For `|ξ| ≤ 1` the point `x = Φ(M̂ + ξ)` satisfies `|x − M| ≤ r|ξ_X| + r²|ξ_Ξ| ≤ r|ξ| ≤ r` (as `r ≤ 1`), and the
third derivatives (`a + |β| = 3`) are bounded as follows:
- `(a, |β|) = (3, 0)`: `r^{−1}|∂_u³f(x)| ≤ r^{−1}|∂_u³f(M)| + r^{−1}|x − M|·|∇∂_u³f| ≤ 12κ + (3/2)C₀𝒩_r + C₀𝒩_r`, by
  (1.1);
- `(2, 1)`: `|∂_u²∂_Θf| ≤ C₀𝒩_r`; `(1, 2)`: `r|∂_u∂_Θ²f| ≤ C₀𝒩_r`; `(0, 3)`: `r²|∂_Θ³f| ≤ C₀𝒩_r`.

Since `κ ≤ 1 ≤ 𝒩_r`, every third partial derivative of `𝔉` is at most `16C₀𝒩_r` on `{|ξ| ≤ 1}`. Hence
`|D³𝔉[ξ′, ξ′, ξ′]| ≤ C₅𝒩_r|ξ′|³` there, for every vector `ξ′`, with `C₅ = C₅(d)`. Without (1.1) the entry `(3, 0)` would only
be `O(r^{−1}𝒩_r)`, and the barrier below would give back Lemma S′'s `r`-dependence.

*Step 3 (the barrier).* Fix a realization in `{W_r > 0} ∩ {e = 1}`. Then `H_M < 0`, so `H̃ < 0`; put `λ := λ_min(−H̃)`.
By Taylor's formula, for `|ξ| ≤ 1`,

    𝔉(M̂ + ξ) ≤ ½ξᵀH̃ξ + (C₅𝒩_r/6)|ξ|³ ≤ −(λ/2)|ξ|² + (C₅𝒩_r/6)|ξ|³.

Put `δ := min(1, 3λ/(2C₅𝒩_r))`. For `|ξ| ≤ δ`, `(C₅𝒩_r/6)|ξ| ≤ λ/4`, so `𝔉(M̂ + ξ) ≤ −(λ/4)|ξ|²`. Let
`E := Φ(M̂ + B̄(0, δ))`, an ellipsoid. `Φ` is affine and injective, and `|Φ(M̂ + ξ) − M| ≤ r|ξ| ≤ r < L/2`; the projection
`R^d → X` is injective and open on `B(M, L/2)`. So `E` is an embedded closed topological ball in `X`, with interior
containing `M` and boundary `Φ(M̂ + ∂B(0, δ))`. On `E`, `f ≤ b`, so no point of `E` lies above `b`; on its boundary
`f ≤ b − r⁴λδ²/4`. Every continuous path from `M` to a point where `f > b` leaves `E`, so it crosses the boundary. By the
maximin characterization ([182] (2)), `d_f(M) ≤ b − r⁴λδ²/4`. On `{e = 1}`, `d_f(M) = f(S) = b − κr⁴`. Hence

    κ ≥ λδ²/4.                                                                                                        (1.2)

If `δ = 1`, then `λ ≤ 4κ`. Otherwise `δ = 3λ/(2C₅𝒩_r)` and (1.2) reads `λ³ ≤ (16/9)C₅²𝒩_r²κ`. Since `κ ≤ 1 ≤ 𝒩_r`, in
both cases

    0 < λ_min(−H̃) ≤ ε″(𝒩_r),        ε″(t) := C₆ t^{2/3} κ^{1/3},        C₆ := max(4, ((16/9)C₅²)^{1/3})          (1.3)

(control S2). This is [182] §3's argument, with the ball `B(M, a_Lλ/K)` replaced by the image of a ball in window
coordinates; as there, it does not claim that `S` lies on `∂E`.

*Step 4 (the weight and the layers).* This is #220's proof of Lemma S′ with `ε″` in place of its `ε`. On
`{W_r > 0} ∩ {e = 1}`: `|det K_M| = |det H_M|/r = r|det H̃| ≤ rλ‖H̃‖^{d−1}`; the pair is typed, so #198 §3's sign window
applied to #220 (F1) gives `|det K_S| ≤ 12k|Δ| + 2max_i|R_i| ≤ Cr(κ + r)𝒩_r^{N₃}`, with an exponent `N₃ ≥ max(m, N₁)`
(#220's exponent there, renamed to avoid a clash with §2's `N₂`); and `{H̃ < 0, λ_min(−H̃) ≤ ε} ⊂ {|λ_max(H̃)| ≤ ε}`. So,
everywhere,

    (W_r/r²) e ≤ C r²(κ + r) ε″(𝒩_r) ‖H̃‖^{d−1} 𝒩_r^{N₃} 1{|λ_max(H̃)| ≤ ε″(𝒩_r)}.

On `{𝒩_r ∈ [2^j, 2^{j+1})}` replace `ε″(𝒩_r)` by `ε_j := ε″(2^{j+1})`. Lemma H (b) gives
`P_Q(𝒩_r ≥ 2^j | H̃) ≤ C_p2^{−jp}(P + |H̃|)^p`, and Lemma H (a) with #218 Lemma D (first bound, `n = d − 1 + p`,
`n′ = n + d(d − 1)/2`) gives `E_Q[‖H̃‖^{d−1}(P + |H̃|)^p1{|λ_max(H̃)| < 2ε_j}] ≤ CP^{p+n′}ε_j`. So the `j`-th term is at most
`C2^{j(N₃ + 4/3 − p)}r²(κ + r)κ^{2/3}P^N`, and `p = N₃ + 2` makes the series converge. This is (S″.1).

*(S″.2).* `r^{−2}A_r^{eld} = 12π_r(v_r)r^{−2}E_Q[(W_r/r²)e]`, `π_r(v_r) ≤ Ce^{−c(b² + k²)}` ([R] (R5)) and
`P^Ne^{−ck²} ≤ C(1 + |b|)^N`; integrating in `b` gives the bound on `𝐓_r^{eld}`. ∎

*Comparison.* (S″.1) divided by #220 (S′.1) is `r⁴κ^{2/3}ℓ^{−2/3} = r^{4/3}`. At fixed `r` both are `O(ℓ^{2/3})`, the order
of #187's far density; the gain is in the `r`-dependence, as `r → 0` with `κ ≤ 1`. In #220 and #229 Lemma S′ was used on
`[a, r_0^*]` with `a = ℓ^{2/15}` and `ℓ^{1/9}`; with (S″.2), `∫_a^{r_0^*}𝐓_r^{eld}dr ≤ C(ℓ^{5/3}a^{−17/3} + ℓ^{2/3}a^{−2/3})`
whenever `a ≥ ℓ^{1/4}`, so that `κ = ℓ/r⁴ ≤ 1` on `[a, r_0^*]` (control S5).

## 2. The rejected weight for `κ ≤ 1`

Throughout §§2–3, `0 < κ ≤ 1` and `k = κr ≤ r`; the lower bound `κ ≥ r^θ` enters only in §4. Facts (B1)–(B5), the classes
`𝔏 ⊃ 𝔏_×` and the inequality (1.1) of note TL §1 are used as there. `G_r` is TL (2.1), and TL (2.2),

    0 ≤ G_r ≤ 37κ²Δ² 1{A < 0, 23κ ≤ |z| ≤ 73κ},

holds for every `κ > 0`: its derivation uses only the cutoff `r|Q₁| ≤ c_eκ`.

**Windows in `f₄`.** For `κ ≤ 1` every window below is a set of values of `f₄`, given `J″`. Given `J″`, `f₄` is Gaussian with
variance in `[c, C]` and a mean `μ₄` with `|μ₄| ≤ C(1 + |J″|)` (B4). On `{A < 0}`, `z = f₄ + 3|q|`, and `q` does not involve
`f₄`.

**Lemma W⁻ (windows carry a Gaussian factor).** For `p, s ≥ 0` there are `C` and `N` (depending on `p` and `s`) such that, for
every law in `𝔏`, every
`0 < κ ≤ 1` and every `J″`-measurable Borel set `I = I(J″) ⊂ {x : |x + 3|q|| ≤ 216κ}` (on `{A < 0}`),

    E[(1 + |J′|)^p 1{A < 0, f₄ ∈ I} | J″] ≤ C |I| (1 + |J″|)^{N} (1 + |q|)^{−s}.                                       (2.1⁻)

*Proof.* `(1 + |J′|)^p ≤ (1 + |J″|)^p(1 + |f₄|)^p`. The density `p₄` of `f₄` given `J″` satisfies
`(1 + |x|)^pp₄(x) ≤ C_N(1 + |μ₄|)^{p+N}(1 + |x|)^{−N}` for every `N` (if `|x| ≥ 2|μ₄|` the Gaussian factor beats every power
of `|x|`; otherwise `1 + |x| ≤ 1 + 2|μ₄|`). On `I`, `|x| ≥ 3|q| − 216`, so `(1 + |x|)^{−s} ≤ 217^s(1 + |q|)^{−s}`: if
`|q| ≤ 216` the right side is at least `1`, and otherwise `|x| ≥ 3|q| − 216 ≥ 2|q|`. Integrate over `I`. ∎

*Use.* With (1.1) of TL, `Δ²Γ̃^{2j} ≤ λ^{2−j}|q|^j‖A‖^{2m−2}` (`j = 0, 1, 2`, and by interpolation `j = 1/2, 3/2`), and
`λ ≤ ‖A‖`, every weight below is at most
`κ^a` times a polynomial in `(|J″|, |q|)` of degree at most `2` in `|q|`, which (2.1⁻) with `s = 2` absorbs. In particular

    Δ²Q₁² ≤ C‖A‖^{2m−2}(λ²f₅² + |η|²|q|λ + ‖B‖²q²),        Δ²|Q₁| ≤ C‖A‖^{2m−2}(λ²|f₅| + |η||q|^{1/2}λ^{3/2} + ‖B‖|q|λ),   (2.2⁻)

from `|Q₁| ≤ |f₅|/120 + |η|Γ̃/12 + ‖B‖Γ̃²/8` and (1.1). So, for instance, `E[κ²Δ²Q₁²(1 + |J′|)^p1{A < 0, |z| ≤ 73κ}] ≤ Cκ³`.

**The good event.** Let `c_e = 1/200`, `δ_e = 1/96` and `N₂` be as in TL §2, and put

    𝔊⁻ := {A < 0, λ ≥ λ₄, 𝒩 ≤ c₁₃κ/r, |Δ| ≥ C₁₂(r/κ)𝒩^{N₂}(1 + ‖B‖)},        λ₄ := C₄𝒩r(1 + |γ| + ‖B‖ + |η|)(1 + |f₄|/κ),

with TL's `λ₄`. Only the last two conditions differ from TL's `𝔊` (`𝒩 ≤ c₁₃/r` and `|Δ| ≥ C₁₂r𝒩^{N₂}(1 + ‖B‖)`), and they
coincide with TL's at `κ = 1`.

**Lemma GE⁻ (the decision on `𝔊⁻`).** There are `C₄`, `C₁₂` (large), `c₁₃` (small) and
`r₄⁻ ∈ (0, min(r_0^*, r_Q, 1/10, L/228)]` such that, for `0 < r ≤ r₄⁻`, `0 < κ ≤ 1` and every `f ∈ C⁹(X)` with the pins,
conclusions (a)–(c) of TL's Lemma GE hold on `𝔊⁻`:
- (a) the pair is not anti-typed, and `ω_r = (w₀ + 12kP₁ + ε_ω)₊` with `|ε_ω| ≤ C(r² + k²)𝒩^N`;
- (b) if the pair is typed: `|φ_r| < 3`, `Γ̃² ≤ 72κ(1 + |f₄|/κ)/λ`, and (Q′1), (Q′2), `ε̃ ≤ c_eκ`, `ζ := r|Q₁|/κ ≤ c_e` hold, as
  does Lemma R₂;
- (c) if the pair is typed, then `1 − e = 1{|z| ≥ 24κ + 36rQ₁}` off `ℰ := {||z| − 24κ − 36rQ₁| ≤ 72κϑ}`, and on
  `𝔊⁻ ∩ {typed}`, `ℰ ⊂ {23κ ≤ |z| ≤ 25κ}`.

*Proof.* TL's proof, line by line; every inequality that used `κ ≥ 1` there is replaced as follows (control S3 records the
arithmetic).
- (a) By #220 (F1), `s(det K_S − det K_M) = 12k|Δ| + O(r²𝒩^{N₁})`. On `𝔊⁻`, `12k|Δ| = 12κr|Δ| ≥ 12C₁₂r²𝒩^{N₂}`, so this is
  positive for `C₁₂` large and `N₂ ≥ N₁`. The weight is then Lemma Ω (4.1)–(4.2), as in TL: `ε_ω` collects
  `9k²[Δ(Δ_C + Δ_BB) − Δ_B²]` and `O(r²𝒩^N)`.
- (b) On typed pairs `|rY_r| < 6k|Δ| + Cr²𝒩^{N₁}`, and `Cr𝒩^{N₁} ≤ κ|Δ|` on `𝔊⁻`; so `|Y_r| < 7κ|Δ|`. With
  `Y_r = 6κΔφ_r + 3kΔ_B` and `|Δ_B| ≤ m𝒩^{m−1}‖B‖`,
  `|φ_r| < 7/6 + rm𝒩^{m−1}‖B‖/(2|Δ|) ≤ 7/6 + κm/(2C₁₂) < 3`. The bound on `Γ̃²` is TL's. Then, with `λ ≥ λ₄`,
  `r/κ ≤ c₁₃/𝒩` and `k ≤ 1`:
  - `r‖B‖Γ̃²/(8κ) ≤ 9r‖B‖(1 + |f₄|/κ)/λ ≤ 9/C₄`;
  - `r|η|Γ̃/(12κ) ≤ (1/12)(72r²|η|²(1 + |f₄|/κ)/(κλ))^{1/2} ≤ (1/12)(72r|η|/(C₄𝒩κ))^{1/2} ≤ (1/12)(72c₁₃/C₄)^{1/2}`;
  - `r|f₅|/(120κ) ≤ 𝒩r/(120κ) ≤ c₁₃/120`.

  So `ζ ≤ c_e`. Next, `ε̃ = 220C₁𝒩r(1 + Γ̃)² ≤ 440C₁𝒩r(1 + Γ̃²) ≤ (440C₁c₁₃ + 31680C₁/C₄)κ ≤ c_eκ`. For (Q′1), it
  suffices that `3𝒩r`, `4𝒩r²`, `(175/8)𝒩r²Γ̃` and `3𝒩r²((κ + 1)/λ)^{1/2}` are each `≤ λ/8`:
  - the first two hold for `C₄ ≥ 32`;
  - the third holds if `175²·72𝒩²r⁴κ(1 + |f₄|/κ) ≤ λ³`, which follows from `λ³ ≥ C₄³𝒩³r³(1 + |f₄|/κ)³`, `κr ≤ 1` and
    `C₄ ≥ 131`;
  - the fourth holds if `1152𝒩²r⁴ ≤ λ³`, since `κ + 1 ≤ 2`.

  For the second part of (Q′1), `r²Γ̃² ≤ 72κr²(1 + |f₄|/κ)/λ ≤ 72k/(C₄𝒩) ≤ 72/C₄`, so `2r²·5M̃ ≤ 44r` for `C₄ ≥ 72`; and
  `(κ + 1)/λ ≤ 2/(C₄r)`, so `2r²·3((κ + 1)/λ)^{1/2} ≤ 6r(2r/C₄)^{1/2} ≤ 6r`; and `2r²·4 = 8r² ≤ r`. So
  `6r + 2r²R′ ≤ 57r ≤ L/4` for `r ≤ L/228`. (Q′2) and Lemma R₂ are as in TL.
- (c) As in TL. Off `J₊ ∪ J₋`, Lemma Q′ decides `e = 1{|φ_r| < 1/3}`: (Q′3) is `ε̃ ≤ κ/4`, and (Q′4) holds because
  `||φ_r| − 1/3| > δ_e > 2c_e/3 ≥ 2ε̃/(3κ)`. There `1{|φ_r| < 1/3} = 1{|z| < 24κ + 36rQ₁}`, since
  `36r|Q₁| ≤ 36c_eκ < 72κδ_e`. On `J_±`, Lemma Q″ (c) decides `e` off `ℰ`. The terms of `ϑ = C₁₀[ζ² + ε₂′/κ + ε̃²/κ²]`:
  `𝒩r²/κ ≤ c₁₃r`; `𝒩r²Γ̃³/κ ≤ 72^{3/2}k^{1/2}/C₄^{3/2}`; `𝒩²r²/(λκ) ≤ 𝒩r/(C₄κ) ≤ c₁₃/C₄`; `𝒩²r²Γ̃²/(λκ) ≤ 72/C₄²`; and `ζ`,
  `ε̃/κ` as in (b). Each tends to `0` as `C₄ → ∞` and `c₁₃ → 0`, so `72κϑ + 36r|Q₁| ≤ κ`. ∎

**Proposition RW⁻ (the rejected weight for `κ ≤ 1`).** For every `p ≥ 1` there is `C_p` such that, for `0 < r ≤ r₄⁻` and
`0 < κ ≤ 1`,

    |E_{Q̄_{r,k}}[ω_r(1 − e)] − E_{Q̄_{r,k}}[G_r]| ≤ C (κr² + r³/κ) + C_p (r/κ)^p.                                       (2.3⁻)

*Proof.* By Lemma GE⁻, on `𝔊⁻` off `ℰ`: if the pair is typed, `ω_r(1 − e) = (w₀ + 12kP₁ + ε_ω)₊1{|z| ≥ 24κ + 36rQ₁}` and
the cutoff of `G_r` holds; if it is not typed, `ω_r = 0` and `(w₀ + 12kP₁ + ε_ω)₊ = (r^{−2}Π)₊ = 0`, so `G_r ≤ |ε_ω|`.
Typed pairs on `𝔊⁻` have `|z| = 72κ|φ_r| < 216κ`, and `G_r` vanishes off `{|z| ≤ 73κ}`. Hence

    |ω_r(1 − e) − G_r| ≤ (ω_r + G_r)(1_{(𝔊⁻)^c} + 1_{𝔊⁻∩{typed}∩ℰ}) + |ε_ω| 1{A < 0, |z| < 216κ}.

Write `E` for `E_{Q̄_{r,k}}`, and use `𝒩`-layers as in TL. Two pathwise bounds on the weights are used:
- (W1) `ω_r ≤ 4(6κ|Δ| + ϱ)²1{|Y_r| ≤ 6κ|Δ| + ϱ}`, with the slack `ϱ := C_Rr𝒩^{N₁}` (#229 (4.1), where it is called `η`;
  here `η` is the jet `∇_Θ∂_u³f(0)`). It holds everywhere, since a typed pair has `det K_M det K_S < 0`. Given `J″`, in the
  layer `j`, `{|Y_r| ≤ 6κ|Δ| + ϱ_j}` is an interval of `f₄` of length `144κ + 24ϱ_j/|Δ|` (#229 Step W2). This window is not of
  the form in Lemma W⁻, and it is used below only with the bounded density of `f₄` (B4): the weights integrated over it
  contain no power of `|q|`.
- (W2) `G_r ≤ 37κ²Δ²1{A < 0, 23κ ≤ |z| ≤ 73κ}`: two intervals of `f₄`, of total length `100κ`.

*The term `|ε_ω|`.* By (B5) and (2.1⁻), `E[|ε_ω|1{A < 0, |z| < 216κ}] ≤ C(r² + k²)κ ≤ 2Cκr²`.

*The complement of `𝔊⁻`.* `(𝔊⁻)^c ⊂ 𝔅_a ∪ 𝔅_b ∪ 𝔅_c ∪ 𝔅_d`, with `𝔅_a := {λ_max(A) ≥ −r𝒩}`, `𝔅_b := {A < 0, λ < λ₄}`,
`𝔅_c := {𝒩 > c₁₃κ/r}` and `𝔅_d := {A < 0, |Δ| < ε_d}`, `ε_d := C₁₂(r/κ)𝒩^{N₂}(1 + ‖B‖)`.
- `𝔅_a`. If `λ_max(A) > r𝒩`, the pair is not typed and `A ≮ 0`, so both terms vanish. If `|λ_max(A)| ≤ r𝒩`, then
  `|Δ| ≤ r𝒩^m`, and (W1) gives `ω_r ≤ Cr²𝒩^N`; with #218 Lemma D in layers this part costs `≤ Cr³`. `G_r` there is covered by
  `𝔅_b`, since `λ ≤ r𝒩 < λ₄`.
- `𝔅_b`. Put `t₁ := 2C₄𝒩r(1 + |γ| + ‖B‖ + |η|)`, so that `λ₄ ≤ t₁max(1, |f₄|/κ)`.
  - Here and in `𝔅_d`, `A` is integrated given `J‴`. Under every law in `𝔏`, the law of `A` given `J‴` is again a Schur
    complement: Gaussian with covariance `≥ c₀I` and mean affine in `J‴` (as in #220 (F5)). So #218 Lemma D and #237
    Lemma D′ apply to it, as (B4) does.
  - On `{λ < t₁}`: `κ²Δ² ≤ κ²t₁²‖A‖^{2m−2}`. For `G_r`, integrate `f₄` over (W2) by (2.1⁻), then `A` given `J‴`:
    `≤ Cκ³E[t₁³(…)] ≤ Cκ³r³`. For `ω_r`, bound the window factor by `1`: `E[(κ²t₁² + ϱ²)1{λ < t₁}] ≤ Cr³`.
  - On `{t₁ ≤ λ < t₁|f₄|/κ}`: `κλ < t₁|f₄|`, so `κ²Δ² ≤ κ²λ²‖A‖^{2m−2} ≤ t₁²f₄²‖A‖^{2m−2}`. For `G_r`, (2.1⁻) over (W2) gives
    `≤ Cκr²`. For the `κ²Δ²` part of `ω_r`, integrate `f₄` over (W1)'s interval: `≤ Cr²E[min(1, κ + ϱ_j/|Δ|)(…)]`, and #229
    (4.2) (`E[(1 + ‖A‖)^nmin(1, s/|Δ|) | J‴] ≤ C(…)s(4 + 2log₂(1/s))` for `s ≤ 1/2`; for larger `ϱ_j` use `min ≤ 1 ≤ 2ϱ_j`)
    gives `≤ Cr²(κ + r log(2/r))`. For the `ϱ²` part, condition on the jets other than `A`: `P(λ < t₁|f₄|/κ | …) ≤
    Ct₁|f₄|/κ` (B4), so it costs `≤ Cr³/κ`.

  So `𝔅_b` costs `≤ C(κr² + r³/κ + r³log(2/r))`, and `r³log(2/r) ≤ κr² + r³/κ` for `r ≤ r₄⁻` (the right side is at least
  `2r^{5/2}`).
- `𝔅_c`. By (W1), `ω_r ≤ C𝒩^N`, and `G_r ≤ 37𝒩^{2m}`. Markov's inequality gives `≤ C_p(r/κ)^p`.
- `𝔅_d`. For `G_r`: `κ²Δ² ≤ κ²ε_d²`; (2.1⁻) over (W2), then `P(|Δ| < ε_d | J‴) ≤ Cε_d(…)` (B4), give `≤ Cκ³E[ε_d³(…)] ≤ Cr³`.
  For `ω_r`: `6κ|Δ| + ϱ ≤ Cr𝒩^{N}(1 + ‖B‖)`, so `ω_r ≤ Cr²𝒩^N(1 + ‖B‖)²` on (W1)'s interval. Integrating `f₄`, then `A` in
  dyadic layers of `|Δ|` (Lemma D′ of #237), gives `≤ Cr²E[κ·ε_d + ϱ(1 + log₂(ε_d/ϱ)₊)] ≤ Cr³(1 + log(2/κ)) ≤ Cr³/κ`.

*The edge set on `𝔊⁻ ∩ {typed}`.* There `ω_r ≤ 37κ²Δ² + |ε_ω|` and `G_r ≤ 37κ²Δ²`, and the part `|ε_ω|` is bounded above.
In the layer `j`, `ℰ ⊂ ℰ_j`, with `ϑ` evaluated at `𝒩 = 2^{j+1}`; given `J″`, `ℰ_j ∩ {23κ ≤ |z| ≤ 25κ}` lies in two intervals
of `f₄` of total length `≤ 288κϑ_j`. By (2.1⁻) the cost is at most `C2^{−jp}E[κ³Δ²ϑ_j(1 + |J″|)^N(1 + |q|)^{−2}]`, and:
- `κ³Δ²ζ² = κr²Δ²Q₁²`, bounded by (2.2⁻);
- `κ³Δ²ε₂′/κ ≤ Cκ²r²𝒩²[Δ²(1 + Γ̃³) + Δ²(1 + Γ̃²)/λ] ≤ Cκ²r²𝒩²‖A‖^{2m−2}(λ² + λ^{1/2}|q|^{3/2} + λ + |q|)`;
- `κ³Δ²ε̃²/κ² ≤ Cκr²𝒩²Δ²(1 + Γ̃⁴) ≤ Cκr²𝒩²‖A‖^{2m−2}(λ² + q²)`.

So the edge set costs `≤ Cκr²`. Collecting gives (2.3⁻). ∎

For `κ ≥ 1` the same events cost `O(r²(1 + κ))` (TL Proposition RW). For `κ ≤ 1` the window has mass `O(κ)` instead of
`O(1/κ)`, and the margins on `𝒩` and `|Δ|` scale with `r/κ`. That is where the terms `r³/κ` and `(r/κ)^p` come from: they
measure how far the pair is from the cusp regime `r ≪ κ`.

## 3. The edge shift for `κ ≤ 1`

`G_s` is TL (3.0): `G_s = (w₀ + 12κsP₁)₊1{A < 0, |z| ≥ 24κ + 36sQ₁, |s||Q₁| ≤ c_eκ}`, with `G_s(E, −O) = G_{−s}(E, O)`.

**Lemma Δ⁻ (the edge shift for `κ ≤ 1`).** For `p ≥ 0` there is `C` such that, for every law in `𝔏`, `0 < κ ≤ 1` and
`0 < r ≤ 1`,

    E[|G_r − G_{−r}| (1 + |J′|)^p] ≤ C r κ²,                                                                         (Δ.1⁻)
    |E[G_r + G_{−r} − 2G₀]| ≤ C r² κ.                                                                                 (Δ.2⁻)

*Proof.* Condition on `J″` with `A < 0`. Then `q`, `Q₁`, `P₁`, `β := 12κΔ²Q₁ = 12κP₁` and the cutoff do not involve `f₄`,
and `z = f₄ + 3|q|`.

*The cutoff.* On `{r|Q₁| > c_eκ}`, `G_{±r} = 0`. So `G_r − G_{−r} = 0` there, and for (Δ.2⁻) the cutoff costs
`2E[G₀1{r|Q₁| > c_eκ}] ≤ 2(r/(c_eκ))²E[36κ²Δ²Q₁²1{A < 0, 24κ ≤ |z| < 72κ}] ≤ Cr²κ`, by (2.1⁻) and (2.2⁻).

*On `{r|Q₁| ≤ c_eκ}`.* Then `|36sQ₁| ≤ 36c_eκ = 0.18κ` and `|sβ| ≤ 12c_eκ²Δ²` for `|s| ≤ r`. In `f₄`, the rejected set of
`G_s` is `{f₄ ≥ e₊(s)} ∪ {f₄ ≤ e₋(s)}`, with

    e_±(s) := ±(24κ + 36sQ₁) − 3|q|,        so that {e_±(r), e_±(−r)} = {e_±(0) + a, e_±(0) − a},  a := 36rQ₁:

the edges are exactly linear in `s` (for the upper edge, `e₊(±r) = e₊(0) ± a`). Take the upper branch; the lower one is its mirror. With `Z′ := 48κ − 3|q|` (the
value of `f₄` at `z = 48κ`) and `p₄` the density of `f₄` given `J″`,

    S₊(s) := ∫_{e₊(s)}^{∞} (w₀ + sβ)₊ p₄ df₄ = ∫_{e₊(s)}^{Z′} (w₀ + sβ) p₄ df₄ + ∫_{Z′}^{∞} (w₀ + sβ)₊ p₄ df₄,

because on `24κ − 0.18κ ≤ z ≤ 48κ`, `w₀ ≥ (Δ²/144)(5184 − 2304)κ² = 20κ²Δ² > |sβ|`. Hence, with `F₊ := w₀p₄` and
`Φ₊(x) := ∫_{e₊(0)}^{e₊(0)+x}F₊ df₄`,

    S₊(r) + S₊(−r) − 2S₊(0) = −[Φ₊(a) + Φ₊(−a)] + rβ∫_{e₊(r)}^{e₊(−r)} p₄ df₄ + ∫_{Z′}^{∞}[(w₀ + rβ)₊ + (w₀ − rβ)₊ − 2(w₀)₊] p₄ df₄.

- *First term.* `Φ₊(0) = 0` and `Φ₊″ = F₊′`, so `|Φ₊(a) + Φ₊(−a)| ≤ a²sup_{|f₄ − e₊(0)| ≤ |a|}|F₊′|`. There
  `|z| ≤ 24.2κ`, so `|w₀′| = (Δ²/72)|z| ≤ κΔ²/2`; also `w₀ ≤ 36κ²Δ²` and `|p₄′| ≤ C(1 + |f₄ − μ₄|)p₄`. So
  `|F₊′| ≤ CκΔ²(1 + |f₄ − μ₄|)p₄` (`κ ≤ 1`).
- *Second term.* `≤ r|β|·2|a|·sup p₄ = 864κr²Δ²Q₁²·sup p₄`.
- *The kink.* The integrand is nonzero only where `|w₀| ≤ r|β|`, that is `|5184κ² − z²| ≤ 1728κr|Q₁|`. Since
  `1728κr|Q₁| ≤ 8.64κ²`, there `z ≥ 71.9κ`, and `|z − 72κ| ≤ 1728κr|Q₁|/(143.9κ) ≤ 12.1r|Q₁|`. The integrand is at most
  `r|β|` (a symmetric second difference of `y ↦ y₊`). So the kink contributes `≤ r|β|·24.2r|Q₁|·sup p₄ ≤ 291κr²Δ²Q₁²·sup p₄`.

Every supremum is over `f₄` with `|z| ≤ 73κ`, where (2.1⁻)'s argument gives
`(1 + |f₄ − μ₄|)p₄ ≤ C(1 + |J″|)^N(1 + |q|)^{−2}`. With (2.2⁻), `E|S₊(r) + S₊(−r) − 2S₊(0)| ≤ Cκr²`. The lower branch is the
mirror image under `z ↦ −z` (`f₄ ↦ −f₄ − 6|q|`, with `p₄` reflected) at the same `s`: there `e₋(±r) = e₋(0) ∓ a`, the edge
term enters as `+[Φ₋(a) + Φ₋(−a)]`, and the three bounds, all in absolute value, are the same. This proves (Δ.2⁻).

For (Δ.1⁻), on each branch: between `e₊(r)` and `e₊(−r)` (length `2|a|`), one of the two integrands is `0` and the other is at
most `37κ²Δ²`; elsewhere `|(w₀ + rβ)₊ − (w₀ − rβ)₊| ≤ 2r|β|` on a window of length at most `50κ`. So, adding the two
branches, `E[|G_r − G_{−r}|(1 + |f₄|)^p | J″] ≤ Crκ²Δ²|Q₁|·sup(1 + |x|)^pp₄`, and (2.1⁻) with (2.2⁻) gives (Δ.1⁻). ∎

For `κ ≥ 1` TL expands the edge shift along the radial direction of `γ`, because the `f₄`-density varies on the scale `1`
while the window has width `≍ κ`. For `κ ≤ 1` the window has width `≍ κ ≤ 1`, so the expansion in `f₄` is the natural one,
and `|F₊′| ≤ CκΔ²(…)` gives the factor `κ` directly. The second-order effect is `O(r²κ)`, which is `O((r/κ)²)` per unit of
the window mass `≍ κ³`.

## 4. Proof of Theorem TL⁻

Fix `θ ∈ (0, 1)`, put `p := ⌈3/(1 − θ)⌉`, and let `r^θ ≤ κ ≤ 1` and `0 < r ≤ r₀ := r₄⁻`. Then
`(r/κ)^p ≤ r^{(1−θ)p} ≤ r³ ≤ r³/κ`. Write `E_{r,k} := E_{Q̄_{r,k}}`. The steps are TL §4's.

*Step 1 (the rejected weight).* By (0.1) of TL and Proposition RW⁻,
`𝐓_r^{rej}(k, u) = 12p_{V_r}(v(k))(E_{r,k}[G_r] + O(κr² + r³/κ))`.

*Step 2 (the odd mean).* As in TL, `h(t) := E_{𝕃_t}[G_r]`, `h′(0) = kE_{r,0}[G_rℓ_r]`, and
`|h″(t)| ≤ Ck²E_{𝕃_t}[G_r(1 + |O|)²] ≤ Ck²κ³`, by TL (2.2) and (2.1⁻) (the laws `𝕃_t` are in `𝔏`). So
`E_{r,k}[G_r] = E_{r,0}[G_r] + kE_{r,0}[G_rℓ_r] + O(k²κ³)`.

*Step 3 (first order vanishes by parity).* `E_{r,0}[G_rℓ_r] = ½E_{r,0}[(G_r − G_{−r})ℓ_r]`, and `|ℓ_r| ≤ C(1 + |O|)`, so by
(Δ.1⁻) `|kE_{r,0}[G_rℓ_r]| ≤ Ckrκ² = Cκ³r²`.

*Step 4 (second order).* By parity (`Q̄_{r,0}` is `𝒫`-invariant and `G_r∘𝒫 = G_{−r}`), `E_{r,0}[G_r] = E_{r,0}[G_{−r}]`, so
`E_{r,0}[G_r] = E_{r,0}[G₀] + ½E_{r,0}[G_r + G_{−r} − 2G₀] = E_{r,0}[G₀] + O(κr²)` by (Δ.2⁻).

*Step 5 (`r → 0` in the law).* As in TL, along the linear interpolation of the covariances,
`|E_{r,0}[G₀] − E_{0,0}[G₀]| ≤ Cr²sup_tE_t[G₀(1 + |J′|)²] ≤ Cr²κ³`.

*Step 6 (the prefactor).* `|p_{V_r}(v(k)) − p_{V_0}(v(0))| ≤ C(r² + k²)`, and all the expectations above are `O(κ³)`.

Collecting Steps 1–6, `𝐓_r^{rej}(k, u) = 12p_{V_0}(v(0))E_{0,0}[G₀] + O(κr² + r³/κ + k²κ³ + κ³r² + r²κ³ + (r² + k²)κ³)`
(Steps 1, 2, 3, 5 and 6; Step 4's `O(κr²)` is in the first term), and the terms after `r³/κ` are at most `Cκ³r² ≤ Cκr²`,
since `k ≤ r` and `κ ≤ 1`. By TL (0.2) the main term is `𝓐^{rej}(κ, u)`. This proves (TL⁻). ∎

(Control S6 checks that each monomial `r^aκ^b` of §§2–4 is at most `κr² + r³/κ` on `r ≤ κ ≤ 1`.)

## 5. Proofs of the corollaries

**Three bounds on the cusp side.** For `0 < κ ≤ 1`:
- `0 ≤ 𝓐^{eld}(κ, u) ≤ 𝓐^{cand}(κ, u) ≤ Cκ³`. Indeed `𝓐^{cand} = 12p_{V_0}(v(0))E_{Q̄_{0,0}}[w_κ(A, Y′)]` (#237 Step U4's
  disintegration), and `w_κ(A, Y′) ≤ 36κ²Δ²1{A < 0, |z| < 72κ}`; apply (2.1⁻).
- `0 ≤ 𝓐^{rej}(κ, u) ≤ Cκ³` likewise (TL §5).
- *The contact kernels.* At fixed `b`, #218 Step C3 gives `r^{−2}A_0(b, κr, u) = 12π_0(v_0(b, k))36κ²E_0[Δ²1{A<0} | v_0(b, k)]`
  exactly, with `π_0(v_0(b, k)) = p_even(b, 0, 0)p_odd(0, 12k, 0)` and a conditional law of the even jets (so of `A`) that
  does not depend on `k`. The odd pin vector is centred Gaussian, so `p_odd(0, 12k, 0) = p_odd(0, 0, 0)e^{−a₀k²}` with
  `a₀ > 0`, for every `k ≥ 0`. Comparing with #218's `𝒜^{con}(b, κ, u) = 12π_0(v_0(b, 0))E_0[36κ²Δ²1{A<0} | b]` gives
  `r^{−2}A_0(b, κr, u) = e^{−a₀k²}𝒜^{con}(b, κ, u)` pointwise in `b`. (Equivalently, after the `b`-integral: #237 Lemma K's
  value `𝐀₀(k, u) = 12p_{V_0}(v(k))·36k²E_{Q̄_{0,k}}[Δ²1{A<0}]` at `r = 0`, with `p_{V_0}(v(k)) = p_{V_0}(v(0))e^{−a₀k²}`.)
  Integrating in `b`, for every `k ≥ 0`, exactly,

      r^{−2}𝐀₀(κr, u) − 𝓐^{con}(κ, u) = (e^{−a₀k²} − 1)𝓐^{con}(κ, u),        so   |r^{−2}𝐀₀(κr, u) − 𝓐^{con}(κ, u)| ≤ Cκ²k².   (5.0)

*Proof of Corollary TS.* Put `ρ := ℓ^{3/14}` and `a := ℓ^{1/7}`. For small `ℓ`, `ρ ≤ min(r₃, r₀)` (`r₃` of #237 Lemma U,
`r₀` of Theorem TL⁻ at `θ = 2/3`), `ℓ^{1/4}` is below the radius of Theorem TL, and `a < r_0^*`. The order is
`ℓ^{1/3} < ℓ^{1/4} < ρ < ℓ^{1/5} < a`. TL's decomposition (5.1) holds at this `ρ`:

    ν_eld − cℓ^{−1/3} − ν_eld^{far,r_0^*} = 𝒦₁ − 𝒦₂ + I^{eld} + J₄,                                                      (5.1)

with `𝒦₁ := ∫_0^ρ∫(𝐓_r − r^{−2}𝐀₀)`, `𝒦₂ := ∫_0^ρ∫𝐓_r^{rej}`, `I^{eld} := ∫_ρ^{r_0^*}∫𝐓_r^{eld}` and `J₄ := −∫_ρ^∞∫r^{−2}𝐀₀`
(integrands at `(ℓ/r³, u)`, inner integrals `dσ(u)`, outer `dr`). We keep the cusp tails explicit.

- *`𝒦₁`.* For `r ≤ ρ ≤ ℓ^{1/5}`, `k = ℓ/r³ ≥ r²`, so #237 Lemma U applies. #237 §5's computation with `ρ` in place of its
  split gives `∫_0^ρ[𝐀₂(ℓ/r³) − 𝐀₂(0)] = c₂ℓ^{1/3} + O(ℓ²ρ^{−5})` (after `∫dσ`; #218 (0.1) and Lemma K), and
  `∫_0^ρ𝓐(ℓ/r⁴)dr = ℓ^{1/4}∫_0^{ρℓ^{−1/4}}𝓐(s^{−4})ds = I^{cand}ℓ^{1/4} − ∫_ρ^∞𝓐(ℓ/r⁴)dr`. The error of (U.1) integrates
  to `O(ρ³ + ℓ^{2/3})`. So

      𝒦₁ = c₂ℓ^{1/3} + I^{cand}ℓ^{1/4} − ∫_ρ^∞∫𝓐(ℓ/r⁴, u) dσ dr + O(ρ³ + ℓ^{2/3} + ℓ²ρ^{−5}).

- *`𝒦₂`.*
  - On `[0, ℓ^{1/4}]`, Corollary TL1: `ℓ^{1/4}∫_0^1∫𝓐^{rej}(s^{−4}, u)dσ ds + O(ℓ^{2/3}) = ∫_0^{ℓ^{1/4}}∫𝓐^{rej}(ℓ/r⁴, u) + O(ℓ^{2/3})`.
  - On `[ℓ^{1/4}, ρ]`, `κ = ℓ/r⁴ ∈ [ℓ^{1/7}, 1]`, and `r ≤ ρ` gives `r^{2/3} ≤ ρ^{2/3} = ℓ^{1/7} ≤ κ`. So Theorem TL⁻ applies with
    `θ = 2/3`, and its error integrates to `C∫_{ℓ^{1/4}}^ρ(ℓr^{−2} + r⁷/ℓ)dr ≤ C(ℓ^{3/4} + ρ⁸/ℓ)`.
  - By #242 §0, `I^{cand} − c₁ = ∫_S∫_0^∞𝓐^{rej}(s^{−4}, u)ds dσ`. So

        𝒦₂ = (I^{cand} − c₁)ℓ^{1/4} − ∫_ρ^∞∫𝓐^{rej}(ℓ/r⁴, u) dσ dr + O(ℓ^{2/3} + ℓ^{3/4} + ρ⁸/ℓ).

- *The cusp tails and `J₄`.* Since `𝓐 − 𝓐^{rej} = 𝓐^{eld} − 𝓐^{con}`,

      𝒦₁ − 𝒦₂ + J₄ = c₂ℓ^{1/3} + c₁ℓ^{1/4} − ∫_ρ^∞∫𝓐^{eld}(ℓ/r⁴, u) + ∫_ρ^∞∫[𝓐^{con}(ℓ/r⁴, u) − r^{−2}𝐀₀(ℓ/r³, u)] + O(…).

  By the first bound, `0 ≤ ∫_ρ^∞∫𝓐^{eld} ≤ Cℓ³∫_ρ^∞r^{−12}dr = (C/11)ℓ³ρ^{−11}`. By (5.0) with `κ²k² = ℓ⁴r^{−14}`, the contact
  difference is at most `(C/13)ℓ⁴ρ^{−13}`. This is where TL's row `ℓ²ρ^{−7}` goes: TL bounded `J₄` and the cusp tail of `𝒦₁`
  separately, each by `Cℓ²ρ^{−7}`, and (5.0) shows that they cancel.
- *`I^{eld}`.* `I^{eld} ≥ 0`. On `[ρ, r_0^*]`, `k = ℓ/r³ ≤ ℓρ^{−3} ≤ r` and `κ ≤ ℓ^{1/7} ≤ 1`. Split at `ℓ^{1/5}` and `a`:
  - on `[ρ, ℓ^{1/5}]`, `κ ≥ r`, and (W⁺.2) integrated in `b` gives `𝐓_r^{eld} ≤ 𝐓_r ≤ C(κ + r)²(κ + r log(2/r))
    ≤ 4C(κ³ + κ²r log(2/r))`, which integrates to `≤ C(ℓ³ρ^{−11} + ℓ²ρ^{−6}log(1/ℓ))`;
  - on `[ℓ^{1/5}, a]`, `κ ≤ r`, and (W⁺.2) gives `𝐓_r^{eld} ≤ 8Cr³log(2/r)`, which integrates to `≤ Ca⁴log(1/ℓ)`;
  - on `[a, r_0^*]`, (S″.2) gives `𝐓_r^{eld} ≤ C(κ + r)κ^{2/3} = C(ℓ^{5/3}r^{−20/3} + ℓ^{2/3}r^{−5/3})`, which integrates to
    `≤ C(ℓ^{5/3}a^{−17/3} + ℓ^{2/3}a^{−2/3})`.

Collecting, `ν_eld − cℓ^{−1/3} − c₁ℓ^{1/4} − c₂ℓ^{1/3} − ν_eld^{far,r_0^*}` is bounded by the sum of the rows of the ledger
below, and at `ρ = ℓ^{3/14}`, `a = ℓ^{1/7}` the least exponent is `4/7`. This is (TS.1). Subtracting (TS.1) from #237 (P.1)
(remainder `ℓ^{3/5}`, and `3/5 > 4/7`) gives (TS.2). For SIDE24 divide by `cℓ^{−1/3}`: `4/7 + 1/3 = 19/21`. ∎

*The ledger of (TS.1)* (exponents of `ℓ` at `ρ = ℓ^{3/14}`, `a = ℓ^{1/7}`; control S5):

| Term | Source | Exponent |
|---|---|---|
| `a⁴log(1/ℓ)` | `I^{eld}` on `[ℓ^{1/5}, a]`, (W⁺.2) (the typed mass at `κ ≤ r`) | **4/7**, with `log(1/ℓ)` |
| `ℓ^{2/3}a^{−2/3}` | `I^{eld}` on `[a, r_0^*]`, Lemma S″ | **4/7** |
| `ρ³` | the `r²` part of Lemma U | 9/14 |
| `ℓ³ρ^{−11}` | the elder cusp tail; (W⁺.2) on `[ρ, ℓ^{1/5}]` | 9/14 |
| `ℓ^{2/3}` | Lemma U at the fold scale; Corollary TL1 | 2/3 |
| `ℓ²ρ^{−6}log(1/ℓ)` | (W⁺.2) on `[ρ, ℓ^{1/5}]` | 5/7, with `log(1/ℓ)` |
| `ρ⁸/ℓ` | the `r³/κ` part of (TL⁻) | 5/7 |
| `ℓ^{3/4}` | the `κr²` part of (TL⁻) | 3/4 |
| `ℓ^{5/3}a^{−17/3}` | Lemma S″, its `κ^{5/3}` part | 6/7 |
| `ℓ²ρ^{−5}` | the finite part of `𝐀₂` | 13/14 |
| `ℓ⁴ρ^{−13}` | the contact difference (5.0) | 17/14 |

The split `a = ℓ^{1/7}` balances the two bold rows, so moving it cannot improve `4/7`. Any `ρ = ℓ^σ` with
`1/5 < σ ≤ 17/77` gives the same result: `σ > 1/5` keeps Lemma U and (W⁺.2) in range and makes Theorem TL⁻ apply with
`θ = (1 − 4σ)/σ < 1`, and `σ ≤ 17/77` keeps `ℓ³ρ^{−11}` at or below `ℓ^{4/7}`. The choice `σ = 3/14` gives `θ = 2/3`.

*How each improvement contributes* (control S5).
- With TL's inputs and the bookkeeping (5.0) alone, the least exponent stays `4/9`, from #229's intermediate bound.
- Adding Lemma S″, but not Theorem TL⁻, gives `6/13`: `ρ²` (the `O(r)` cusp error on `κ ≤ 1`) against `ℓ³ρ^{−11}`, at
  `ρ = ℓ^{3/13}`. Since `6/13 < 1/2`, this is not enough.
- Theorem TL⁻ removes `ρ²`, and the least exponent becomes `4/7`. So both new inputs are needed to pass `ℓ^{1/2}`.
- (5.0) is not needed for `4/7` itself: without it, TL's row `ℓ²ρ^{−7}` stays, and its exponent `2 − 7σ` is at least `4/7`
  exactly for `σ ≤ 10/49`. So `4/7` still holds for `σ ∈ (1/5, 10/49]`, but only with Theorem TL⁻ at `θ = (1 − 4σ)/σ ≥ 9/10`,
  close to its edge `κ ≈ r`. With (5.0), `σ = 3/14` and `θ = 2/3` suffice.

## 6. Remarks

1. **What fixes `4/7`.** The two bold rows are the intermediate elder mass. On `κ ≤ r` (that is `r ≥ ℓ^{1/5}`) #229's bound
   (W⁺.2) is the typed mass `r³log(2/r)`, which ignores the elder mark, and Lemma S″ is `rκ^{2/3}`. They cross at
   `r = ℓ^{1/7}`. Every other row has exponent at least `9/14`. (Balancing with the logarithm,
   `a = ℓ^{1/7}(log(1/ℓ))^{−3/14}`, would give `O(ℓ^{4/7}(log(1/ℓ))^{1/7})`.)
   - *A formal refinement (not proved).* On typed pairs the ridge profile through `M` has cubic and quartic coefficients
     `O(κ + r𝒩/|Δ|)` in window coordinates, not `O(𝒩)`: the typed window pins `z` to `|z| < 72κ + O(r/|Δ|)`. Running the
     barrier along the ridge with that bound would give `λ ≲ κ^{1/3}(κ + r)^{2/3}`, hence formally an elder kernel
     `≲ r^{7/3}κ^{2/3}` on `κ ≤ r` and an intermediate mass `O(ℓ^{2/3})`. That needs a `C³` bound on [N]'s ridge
     `g_𝔉` (Lemma Q′ controls only `C²`), and it is not attempted here.
2. **Agent 3's obstruction and [N] Remark 1.** Agent 3 (main#259 6001313460) recorded three points about [N]: the window
   `48κ` against the shift `36r|Q₁|`; no improvement of the intermediate elder mass; and that even a uniform `C(r² + k²)` on
   `r ≤ κ ≤ 1/r` would leave that mass. They stand for [N] as written. Here the first is handled by restricting Theorem TL⁻
   to `κ ≥ r^θ`, the second and third by Lemma S″. [N] Remark 1's further point, the fold family `ρ_f⁵/ℓ`, is removed by
   #237 Lemma U for the candidate kernel and by Corollary TL1 for the rejected one (`κ ≥ 1`).
3. **Numerical evidence** (exploration; not part of the proof; to be archived with the note).
   - *The rejected kernel at small `κ`.* [N]'s Monte Carlo `elder_f4int.py` (project archive
     `V2_2/frontiers_elder_cusp_parity_20261002/exploration/`, unchanged, sha256 `ecc584fe…d223`) was rerun at `b = 0`,
     `κ ∈ {1/2, 1/4, 1/10}`, `r ∈ {0.003, 0.006, 0.009, 0.012, 0.016, 0.02}`, `N = 20000` (antithetic in the odd jets),
     cubic fits in `r` (`d = 2`, Gaussian kernel). The rejected kernel's linear coefficient relative to its value is
     `+0.0007 ± 0.0173`, `+0.0043 ± 0.0033` and `+0.0045 ± 0.0024`. Its quadratic coefficient relative to its value is
     about `−5 ± 4`, `0.3 ± 0.9` and `−2.0 ± 0.9`. These are at fixed `b`, not integrated in `b`. (TL⁻ allows `κr² + r³/κ`
     absolutely, that is a relative quadratic coefficient up to a constant times `κ^{−2} = 4, 16, 100`; the observed ones
     are of order one.) The rejected fraction of the candidate kernel is `0.078`, `0.250` and `0.467`, rising towards the
     cusp value `14/27 ≈ 0.519` of `κ → 0`.
   - *The full-field Monte Carlo of #216* (#237 Remark 4, [N] Remark 4). Joint `ℓ^{1/2} + ℓ^{3/4}` fits of the elder and
     rejected *adjacent-pair* residuals gave nonzero `ℓ^{1/2}` coefficients, while `ℓ^{2/3} + ℓ^{3/4}` fits were comparable
     ([N] Remark 4). Corollary TS′ shows that `ν_eld` and `ρ_rej` have no `ℓ^{1/2}` term, so those coefficients describe the
     fit range (or the adjacent-pair density, which is not `ν_eld`), not an asymptotic `ℓ^{1/2}` term.
4. **`d ≥ 3`.** Lemma S″ uses #220's Lemma H, which holds in every `d ≥ 2`. Theorem TL⁻'s proof uses neither the eigenframe
   of `A` nor a lower bound on the stiff eigenvalues: `λ = λ_min(−A)`, (1.1) of TL and the conditional law of `f₄` suffice.
5. **Consistency.**
   - At `κ = 1` both (TL) and (TL⁻) give `O(r²)`.
   - (S″.1) implies #220's (S′.1) for `r ≤ 1`, by the factor `r^{4/3}`.
   - (TS.1) implies TL (TL3.1) and #229 (E3⁺.0), with a smaller remainder; (TS.2) implies (TL3.2).
6. **Constants.** No constant is certified. Those implied by Theorem TL⁻ grow like TL's (TL Remark 6), and `C_θ` grows as
   `θ → 1` through `p = ⌈3/(1 − θ)⌉`.

## 7. Exact controls (`ts_exact.py`; stdlib; exact rationals; deterministic; byte-identical under `-O`)

The script and its expected stdout are published in the controls comment that follows this note.

- **S1** (1.1) on pinned polynomial profiles `g(t) = b + αt² + βt³ + γ₄t⁴ + γ₅t⁵ + γ₆t⁶`, with `α, β` solved exactly from
  `g(r) = b − kr³` and `g′(r) = 0`, for 156 rational cases (`0 < r ≤ 1`, `0 ≤ k ≤ r`), including constant `g⁗`, where
  `g‴(0) − 12k = −rg⁗/2`. Checked: the pins; the identity `g‴(0) − 12k = 12(R₄ − rR₃′/2)/r³`; the Taylor bounds on `R₄` and
  `R₃′` with the exact supremum of `|g⁗|` on `[0, r]`; and `|g‴(0) − 12k| ≤ (3/2)r sup|g⁗|`.
- **S2** the barrier:
  - the scaling exponents `a + 2|β| − 4` of the window coordinates, for the second and third derivatives;
  - `r^{−4}DH_MD = Λ_r^{−1}H_MΛ_r^{−1}` exactly, for random rational symmetric `H_M` in `d = 2, 3, 4`;
  - for 120 rational `(λ, C₅, 𝒩)`: on `[0, δ]`, `δ = min(1, 3λ/(2C₅𝒩))`, `−(λ/2)t² + (C₅𝒩/6)t³ ≤ −(λ/4)t²`; and
    `κ ≥ λδ²/4` (at the extremal `κ = λδ²/4` and two larger values, all `≤ 1`) forces `λ³ ≤ max(64κ³, (16/9)C₅²𝒩²κ)` and
    `λ³ ≤ C₆³𝒩²κ`;
  - the ratio `r^{4/3}` between (S″.1) and (S′.1).
- **S3** the constants of §§1–3: `131³ ≥ 175²·72`, `1152`, `31680`, `57 = 6 + 44 + 1 + 6`, Lemma Q′'s `36c_e < 72δ_e` and
  `2c_e/3 < δ_e`, TL (2.2)'s `36 + 12c_e ≤ 37` and `|z| < 73κ`, `216 = 3·72`, `w₀ ≥ 20κ²Δ²`, the edge range `24.2κ`, `|w₀′|`,
  the kink (`8.64`, `71.9`, `12.1`, `291`), `864`, `2664`, `1200`, the window lengths `100`, `288`, `432`, `e₊ − e₋ ≥ 47κ`,
  Lemma W⁻'s two cases in `|q|`, and `|φ_r| < 3`.
- **S4** Lemma Δ⁻'s mechanism on explicit models. With `F` linear, `Φ(a) + Φ(−a) = F′a²` exactly. With the exact `w₀` as a
  polynomial in `f₄` and a positive quadratic stand-in for `p₄`, on a grid (`κ ∈ {1/10, 1/3, 1}`, `3|q| ∈ {0, 1, 5}`, two
  `Δ²`, three `Q₁`, and `r` with `r|Q₁| = c_eκ, c_eκ/2, c_eκ/5`), the script checks:
  - the identity `S₊(r) + S₊(−r) − 2S₊(0) = −[Φ₊(a) + Φ₊(−a)] + rβ∫_{e₊(r)}^{e₊(−r)}p₄` for the integrals up to `z = 48κ`;
  - `|Φ₊(a) + Φ₊(−a)| ≤ a²sup|F₊′|`, with an exact polynomial bound for the supremum;
  - `|w₀′| ≤ κΔ²/2` on the edge range, `w₀ = 20κ²Δ²` at `z = 48κ` and `|rβ| ≤ 12c_eκ²Δ²`;
  - `|w₀| ≥ r|β|` at `z = 72κ ± 12.1r|Q₁|`, so the kink lies in that window;

  and that the kink integrand `(w + h)₊ + (w − h)₊ − 2w₊` lies in `[0, |h|]` and vanishes for `|w| ≥ |h|`.
- **S5** the ledger of (TS.1), each row's exponent derived from its integral (the rows `ℓ^{2/3}` and `ℓ²ρ^{−5}` recorded
  from #237 §5 and TL1):
  - at `ρ = ℓ^{3/14}`, `a = ℓ^{1/7}` the least exponent is `4/7`, attained exactly by the two bold rows, and the other rows
    are `9/14, 9/14, 2/3, 5/7, 5/7, 3/4, 6/7, 13/14, 17/14`;
  - `θ = (1 − 4σ)/σ = 2/3` at `σ = 3/14`; the least exponent is `4/7` for `σ` in `(1/5, 17/77]` (four values checked) and
    drops below it just above `17/77`; `σ = 1/5` is the edge `θ = 1`;
  - `a = ℓ^{1/7}` balances the bold rows; `κ²k² = ℓ⁴r^{−14}`;
  - the contributions: `4/9` (TL's inputs), `6/13 < 1/2` (Lemma S″ without Theorem TL⁻), and, without (5.0), least
    exponent `4/7` at `σ = 10/49` (where `θ = 9/10`) and below `4/7` just above it;
  - SIDE24's `19/21`, against TL's `7/9` and #229's `16/21`; and `3/5 > 4/7` for (TS.2).
- **S6** every error monomial `r^aκ^b` of §§2–4 (seventeen, transcribed from the text) is at most `κr² + r³/κ` on
  `r ≤ κ ≤ 1`. In `log κ` the right side is the maximum of two linear functions crossing at `κ = r^{1/2}`, so the test is
  `a + b ≥ 2`, `a + b/2 ≥ 5/2` and `a ≥ 2`. Also `(1 − θ)⌈3/(1 − θ)⌉ ≥ 3` for four values of `θ`.

**Not covered by any control** (checked by hand): Lemma W⁻'s Gaussian factor; the analytic content of Lemma S″ (the
barrier's topology, Lemma H, the layers); Lemma GE⁻ beyond its arithmetic; Proposition RW⁻; Lemma Δ⁻ beyond S4's models
(the true `p₄`, the lower branch, the cutoff); Steps 1–6 of §4; (5.0); and §5's use of the consumed results.

Mutants, each breaking one control:
- `M1` S1: `|g‴(0) − 12k| ≤ (1/4)r sup|g⁗|`.
- `M2` S2: `δ = min(1, 3λ/(C₅𝒩))`.
- `M3` S2: `(4/9)C₅²𝒩²κ` in place of `(16/9)C₅²𝒩²κ`.
- `M4` S3: `130³` in place of `131³`.
- `M5` S5: `a = ℓ^{1/8}`, so the least exponent becomes `1/2`.
- `M6` S5: the contact row left at TL's `ℓ²ρ^{−7}` (no cancellation), so the least exponent becomes `1/2`.
- `M7` S5: SIDE24's shift `1/4` in place of `1/3`.
- `M8` S6: the monomial `r³/κ` replaced by `r²/κ`.
- `M9` S4: the bound `a²sup|F′|/2`.
- `M10` S2: `D = diag(r, r, …, r)`.

Each mutant exits `1` with empty stdout and `FAILED: <group>` on stderr. An unknown mutant label, a missing label, or an
extra argument exits `2`.

## 8. Review slices

- **A** §1: Lemma S″ — the pin relation (1.1), the third derivatives in window coordinates, the barrier (1.2)–(1.3) and its
  use of [182] (2), and the layers (Lemma H, #218 Lemma D).
- **B** §2: Lemma W⁻, (2.2⁻), the good event, Lemma GE⁻ (each margin of [N]'s Lemmas Q′, Q″, R₂ against `λ₄`, `𝒩 ≤ c₁₃κ/r`
  and `|Δ| ≥ C₁₂(r/κ)𝒩^{N₂}(1 + ‖B‖)`), and Proposition RW⁻ (the four bad events and the edge set).
- **C** §§3–4: Lemma Δ⁻ (the edges in `f₄`, the cutoff, the kink, (Δ.1⁻)) and Steps 1–6.
- **D** §0, §§5–7: the statements, (5.0), the proof of Corollary TS with its ledger, Corollary TS′, the remarks and
  `ts_exact.py`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_