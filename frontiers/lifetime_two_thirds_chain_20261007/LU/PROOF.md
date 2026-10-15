# Lifetime note LU: Lemma U for differences, and the three densities with remainder `O(ℓ^{2/3})` up to a logarithm

Object: `CL-LU-GAP-DIFFERENCE-20261006-v1`. Claim: main#229 6024580296.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 6 October 2026, for Dylan Roy (delegated AI
work). The same session wrote every consumed packet and note: #187, #207, #218, #229, #237, notes TS and EM, and addendum
EM.1. The consumed packets in turn consume OpenAI-authored sources, among them [R], [P], [Z] and [182].
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph, STATUS,
PROOF_INDEX, prize or Boolean change; no numerical constant is certified. Same GitHub account as every lane;
organizational independence 0. Before posting, three clean-context Claude subagents of this session refereed the draft in
three slices. All three returned AMEND with no blocking finding, and every finding is applied here. These are author-side
reads and earn no review credit.

**What is new.**
- **Lemma U₀** (§3). For `0 < k ≤ r` (that is, `κ ≤ 1`), `|𝐓_r(k, u) − 𝐓_r(0, u) − Λ_κ(u)| ≤ Crk`. Here
  `Λ_κ := 12p_{V_0}(v(0))E_{Q̄_{0,0}}[(36κ²Δ² − Y′²)₊1{A<0}] = ∫_R𝒜^{cand}(b, κ, u)db` is the birth-integrated candidate cusp
  kernel, and `Λ_κ = 𝓐(κ) + r^{−2}𝐀_0(k) + O(k²κ²)` (note TS's (5.0)).
  - #237's Lemma U needs `κ ≥ r`, and on `r ≤ κ ≤ 1` its error is `O(r²)`. Here the error is `O(rk) = O(r²κ)`, and `k` may be
    as small as one likes.
  - The tools:
    - the law at gap `k` is the law at gap `0` shifted by `kμ_r`, with `μ_r` odd (§1; #207 Lemma L uses the same affine
      structure at fixed `b`);
    - along the shift, `∂_k(det K_S − det K_M) = 12 det A + O(r²)`, with no `r¹` term (§2);
    - at `k = 0` the reflection `z ↦ −z` fixes the law, keeps the endpoint sum `x` and negates the endpoint difference `y`.

    So every first-order error is odd and integrates to zero, and the `k`-derivative of the error is `O(r)`.
- **Theorem U⁼ (Lemma U for differences)** (§4). For every `k > 0`,
  `|𝐓_r(k) − 𝐓_r(0) − r^{−2}𝐀_0(k) − [𝐀₂(k) − 𝐀₂(0)] − 𝓐(κ)| ≤ C(r²min(1, κ) + r min(k, 1/k))`. This is the version that
  #237 Remark 2 describes: it holds for all `k > 0`, its error is the one stated there, and the `k = 0` term `𝐓_r(0)` absorbs
  `J₂`.
- **Theorem P⁺** (§4). `ν_cand(ℓ) = cℓ^{−1/3} + B_{d,L} + I^{cand}ℓ^{1/4} + c₂ℓ^{1/3} + O(ℓ^{2/3})`, improving #237's `O(ℓ^{3/5})`.
  The split `ρ` is now fixed. The least exponent of the remainder, `2/3`, comes from the fold-scale term `r min(k, 1/k)` of
  #237's (U.1) on `κ ≥ 1`, which #237 Remark 2 calls plausibly the next term; the remainder is bounded, not identified.
- **Corollary LU** (§5), with note TS and addendum EM.1.
  - `ν_eld(ℓ) = cℓ^{−1/3} + c₁ℓ^{1/4} + c₂ℓ^{1/3} + O(ℓ^{2/3}log(1/ℓ))`, improving note EM's `O(ℓ^{9/14})`.
  - `ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + O(ℓ^{2/3}log(1/ℓ))`, improving `O(ℓ^{3/5})`.
  - For SIDE24 the relative remainder is `O(ℓ log(1/ℓ))`, against note EM's `O(ℓ^{41/42})`.

**Not claimed.**
- No sharpness of `2/3`, and no identification of an `ℓ^{2/3}` coefficient. The remainders are bounded, not expanded.
- Nothing about #242's Conjecture 7: its conjectured term `R_{2/3}ℓ^{2/3}` of `ρ_rej + ν_eld^{far,r_0^*}` lies inside the
  remainder `O(ℓ^{2/3}log(1/ℓ))` of (LU).
- No change to any statement of #237, note TS, note EM or EM.1; Theorem P⁺ and Corollary LU replace their remainders only.
- Nothing pointwise in `b`; no certified number; no uniformity in `d` or `L`.
- Nothing beyond the existential scope of the consumed packets and notes. Whether IBA2-009 closes is for the audit's owners.

**Consumed.**
- #237 `frontiers/candidate_parity_rate_20261001/PROOF.md` (blob `a97bf528`):
  - §§0–2: the setting, Lemma R, the rows #237 (1.1), Lemma Π (in the deterministic form of its proof, through #218 Step F1),
    the polynomials #237 (2.1), and Lemma K with its proof;
  - Lemma Λ's proof, its reduction step (`p_{V_0}(v(s)) = p_{V_0}(v(0))e^{−as²}`);
  - Lemma U ((U.1)), Step U2 (a) (the layer and `f₄`-density device), Step U3 (the Gaussian interpolation of laws) and Step U4;
  - §5: the decomposition, the definition of `J₂`, the main-term computation, and the bounds on `J₃`–`J₅`;
  - [R] §2's expansion of `T_r`, as quoted in the proof of Lemma R (R.4).
- #218 `frontiers/candidate_third_order_20261001/PROOF.md` (blob `70ca57ef`): §0 (`𝒜^{cand}`), Lemma D, (1.2), Step F1 (the
  free jets), and (0.1).
- #207 `frontiers/cusp_second_order_20261001/PROOF.md` (blob `f6df5a73`): (7.1), (7.2), and §7's `I^{cand}`.
- #229 `frontiers/third_order_rate_20261001/PROOF.md` (blob `110ed33a`): (W⁺.2) and (W⁺.3).
- For Corollary LU only:
  - note TS (main#229 6020794123, with successor text 6021299833; read in every slice, readback PASS 6021301151): Theorem TL⁻
    (§0; proved in §§2–4 for every `θ ∈ (0, 1)`), here at `θ = 4/5`; and §5: the decomposition (5.1), the bounds on `𝒦₂`, the
    cusp tails and `J₄` with (5.0), and `I^{eld}` on `[ρ, ℓ^{1/5}]`, with the inputs those bounds consume (note TL's
    decomposition and Corollary TL1, #242 §0, #237 Lemma K, #229 (W⁺.2));
  - note EM (main#229 6023010944, with successor text 6023434026; Slice A PASS 6023042554, Slice B AMEND 6023045290, Slice C
    PASS 6023050789, readback PASS 6023435335): §5 (`[r_*, r_0^*]` by (S″.2), and the far term) and its ledger, through
    Corollary EM.1;
  - addendum EM.1 (main#229 6024077582; Slice A PASS 6024106995, Slice B PASS 6024112289): Corollary EM.1;
  - #187 `frontiers/far_elder_rate_20260930/PROOF.md` (blob `07260114`): the far bound `0 ≤ ν_eld^{far,r_0^*} ≤ Cℓ^{2/3}`, through
    note EM §5.

**Cited only.**
- #207 Lemma L's proof (the affine structure in `k` at fixed `b`) is the precedent for §1; nothing in §1 relies on it.
- #242 `frontiers/soft_rejected_pairs_20261002/PROOF.md` (blob `271412db`): Lemma 5 and Conjecture 7, for Remark 2 and *Not
  claimed*.

**Prior work and overlap.** I searched the tree of Math- `main` (`665f744a`), the project archive, and main#229, main#259
and main#275.
- No packet or claim proves this route. It is #237 Remark 2's "A route to `2/3` (not attempted)". #237's README (*Not
  claimed*), note EM Remark 1 (its first item) and addendum EM.1 (its header, §3, and its Slice B read 6024112289) point to it.
  This note's claim is 6024580296.
- #207's (7.1) bounds `𝐓_r(k) − 𝐓_r(0)` by `O(κ² + k)` for `k ≤ 1` without identifying the main term; Lemma U₀ identifies it
  to `O(rk)` on `κ ≤ 1`.
- At the order this note reaches, #242's Conjecture 7 predicts a term `R_{2/3}ℓ^{2/3}` of `ρ_rej + ν_eld^{far,r_0^*}`; this note
  does not address it.

## 0. Setting and statements

Setting and notation are #237's (§§0–2). In particular: `m = d − 1` and `s := (−1)^m`; the pins `M = −ru/2`, `S = ru/2`; the
rows `V_r` with target `v(k) = (0_d, 0_d, 12k)` (#237 (1.1)), their density `p_{V_r}`, and the regression law `Q̄_{r,k}`; the scaled
endpoint Hessians `K_M`, `K_S`, `Π = −det K_M det K_S`, and `𝐓_r(k, u) = 12p_{V_r}(v(k))E_{Q̄_{r,k}}[r^{−2}Π1_{typed}]` (R.1).
The jets at `0` are `A = ∇_Θ²f(0)`, `B`, `C`, `γ`, `η`, `f₄`, `f₅`, with `Δ := det A`, `A^♯ := adj A`, `Δ_B := tr(A^♯B)`,
`Y′ = (f₄/12)Δ − γᵀA^♯γ/4`, and `U`, `V = V_o + kV_e` as in #237 (2.1). `𝐀_0`, `𝐀₂` are Lemma K's, and
`𝓐(κ, u) = ∫_R(𝒜^{cand} − 𝒜^{con})(b, κ, u) db`, `κ = k/r`. Constants `C, c, N` depend only on `d` and `L`.

For `κ ≥ 0` put

    Λ_κ(u) := 12 p_{V_0}(v(0)) E_{Q̄_{0,0}}[(36κ²Δ² − Y′²)₊ 1{A < 0}].                                              (0.1)

Since #218 §0 gives `𝒜^{cand} = 12π_0E_0[(36κ²Δ² − Y²)₊1{A<0} | b]`, (R.1)'s disintegration gives `Λ_κ = ∫_R𝒜^{cand}(b, κ, u) db`.

*The identity.* `36κ²Δ² − min(Y′², 36κ²Δ²) = (36κ²Δ² − Y′²)₊`. By #237 Step U4, `𝓐(κ) = −12p_{V_0}(v(0))E_{Q̄_{0,0}}[min(Y′², 36κ²Δ²)
1{A<0}]`. By the proof of Lemma K, `r^{−2}𝐀_0(k) = 12p_{V_0}(v(k))·36κ²E_{Q̄_{0,k}}[Δ²1{A<0}]`, and the law of `A` does not
depend on `k` (Lemma R (R.2), at `r = 0` by (R.4)). `V_0` is centred Gaussian and `v(k) = kv(1)`, so
`p_{V_0}(v(k)) = e^{−a₀k²}p_{V_0}(v(0))` with `a₀ := v(1)ᵀCov(V_0)^{−1}v(1)/2`. Hence

    Λ_κ = 𝓐(κ) + e^{a₀k²} r^{−2}𝐀_0(k),        0 ≤ Λ_κ − 𝓐(κ) − r^{−2}𝐀_0(k) ≤ C k²κ².                                (0.2)

(Equivalently, `∫_R𝒜^{con}db = e^{a₀k²}r^{−2}𝐀_0(k)`, which is note TS's (5.0) rearranged.)

**Lemma U₀ (the gap difference on `κ ≤ 1`).** There are `C, r₄ > 0` such that for `0 < r ≤ r₄`, `0 < k ≤ r` and `u ∈ S^{d−1}`,

    |𝐓_r(k, u) − 𝐓_r(0, u) − Λ_{k/r}(u)| ≤ C r k.                                                                   (U₀)

**Theorem U⁼ (Lemma U for differences).** For `0 < r ≤ r₄`, `k > 0` and `u`,

    |𝐓_r(k, u) − 𝐓_r(0, u) − r^{−2}𝐀_0(k, u) − [𝐀₂(k, u) − 𝐀₂(0, u)] − 𝓐(k/r, u)| ≤ C (r²min(1, κ) + r min(k, 1/k)).   (U⁼)

**Theorem P⁺ (the candidate density with remainder `ℓ^{2/3}`).** As `ℓ ↓ 0`,

    ν_cand(ℓ) = c ℓ^{−1/3} + B_{d,L} + I^{cand} ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{2/3}).                                        (P⁺)

**Corollary LU (with note TS and addendum EM.1).** As `ℓ ↓ 0`,

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{2/3}log(1/ℓ)),
    ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁) ℓ^{1/4} + O(ℓ^{2/3}log(1/ℓ)).                                                  (LU)

For SIDE24 (`d = 3`, `L = 24`, `c = c_{3,24}`): `ν_{3,24}(ℓ) = cℓ^{−1/3}(1 + (c₁/c)ℓ^{7/12} + (c₂/c)ℓ^{2/3} + O(ℓ log(1/ℓ)))`.

## 1. The shift and the reflection

**Lemma S.** Fix `0 < r ≤ r_0^*` and `u`. For a field `g` and a pin `i ∈ {M, S}` write `H_i(g) := D²g(i)`, `A_i(g) := ∇_Θ²g(i)`,
and `K_i(g) := D_r^{−1}H_i(g)D_r^{−1}` with `D_r := diag(√r, I_m)` in the frame `(u, Θ)`.
- (S.1) *The shift.* There is a deterministic odd function `μ = μ_{r,u}` (`μ(−z) = −μ(z)`) with `V_r(μ) = v(1)` and
  `‖μ‖_{C^{N₀}} ≤ C` uniformly in `r` and `u` (`N₀ = 9`), such that for `f ~ Q̄_{r,0}` and every `k ∈ R`, `f + kμ ~ Q̄_{r,k}`.
- (S.2) *Linearity.* `A(f + kμ) = A(f)`, and the endpoint Hessians are affine in `k`: `K_i(f + kμ) = K_i(f) + kK_i(μ)`. So
  `det K_i(f + kμ)` is a polynomial in `k` of degree `≤ d`, with `∂_k det K_i(f + kμ) = tr(adj K_i(f + kμ)·K_i(μ))`.
- (S.3) *Reflection.* For `f̃(z) := f(−z)`: `f̃ ~ Q̄_{r,0}`, `(f + kμ)~ = f̃ − kμ`, and `K_M(g̃) = K_S(g)` for every field `g`. The
  jets of `f̃` at `0` are `𝒫` applied to those of `f`.
- (S.4) *Typed configurations.* For a pinned field `g` put `m_i(g) := det K_i(g)/r`, `𝔞 := s m_M`, `𝔟 := s m_S`,
  `x := (𝔞 + 𝔟)/2`, `y := (𝔟 − 𝔞)/2`. If `g` is typed, then `𝔞 < 0 < 𝔟`. If moreover `A_M(g) < 0` and `A_S(g) < 0`, then `g` is
  typed if and only if `𝔞 < 0 < 𝔟`, and then

      r^{−2}Π(g) 1_{typed}(g) = G(x, y),        G(x, y) := (y₊² − x²)₊.                                              (1.1)

- (S.5) *Continuity in `k`.* Along `k ↦ g_k := f + kμ`, the inertia of each `H_i(g_k)` is constant on every interval on which
  `det K_i(g_k) ≠ 0`. So if `g_{k₁}` and `g_{k₂}` differ in typedness, some `m_i(g_k)` vanishes for some `k` between them.

*Proof.* (S.1) Under `Q̄_{r,0}` the field is Gaussian regression on `V_r = 0`; under `Q̄_{r,k}` on `V_r = v(k) = k v(1)`. The
conditional covariance does not depend on the target and the conditional mean is linear in it, so `f + kμ ~ Q̄_{r,k}` with
`μ := Cov(f(·), V_r)Cov(V_r)^{−1}v(1)` (unconditioned covariances), and `V_r(μ) = v(1)`. By Lemma R (R.2), `Cov(V_r)` is
block-diagonal between the rows built from `f_o` (the average gradient and `T_r`) and those built from `f_e` (the gradient
difference), `v(1)` sits in the first block, and `f_o ⊥ f_e`; so `μ(z) = Cov(f_o(z), ·)(…)` is odd. The bound: `Cov(V_r)` is
uniformly invertible (Lemma R (R.4)), and `Cov(f(·), V_r)` consists of centred difference quotients of derivatives of the
covariance function.
(S.2) `A` is a second derivative at `0` and `μ` is odd, so `∇_Θ²μ(0) = 0`. `K_i` is linear in the field, and Jacobi's formula
gives the derivative.
(S.3) Lemma R (R.3) at `k = 0`; `μ(−z) = −μ(z)`; and `D²g̃(z) = D²g(−z)`, which exchanges the pins `M` and `S`.
(S.4) If `A_i < 0`, then by Haynsworth's inertia additivity `H_M < 0` iff the Schur complement of `A_M` in `H_M` is negative,
that is iff `det H_M` has the sign `−s` (as `det A_M` has the sign `s`), that is iff `𝔞 < 0`; and `ind H_S = d − 1` iff the
Schur complement of `A_S` is positive, iff `𝔟 > 0`. Without the hypothesis, typed implies that `det H_M` has the sign
`(−1)^d = −s` and `det H_S` the sign `s` (the converse fails). On `{𝔞 < 0 < 𝔟}`, `r^{−2}Π = −m_Mm_S = −𝔞𝔟 = y² − x²` and
`|x| < y`; and `G(x, y) = 0` unless `|x| < y`, since `y ≤ 0` forces `y₊ = 0`.
(S.5) The eigenvalues of `H_i(g_k)` are continuous in `k`, and the inertia changes only when one of them crosses `0`. ∎

So for `f ~ Q̄_{r,0}` put `x_k := x(f + kμ)` and `y_k := y(f + kμ)`, polynomials in `k`. By (S.3),
`x_k(f̃) = x_{−k}(f)` and `y_k(f̃) = −y_{−k}(f)`. In particular

    x₀ is even, y₀ is odd, ∂_k x_k|_{k=0} is odd, ∂_k y_k|_{k=0} is even,                                        (1.2)

under `f ↦ f̃`, which preserves `Q̄_{r,0}` and maps the jets by `𝒫`.

## 2. The derivatives along the shift

Let `𝔗 := 1 + sup_{|k|≤1}‖f + kμ‖_{C^{N₀}(𝔅)}`, with `𝔅` the closed ball of radius `r_0^*` about `0`. Then
`𝔗 ≤ 1 + ‖f‖_{C^{N₀}(𝔅)} + C`, and as in #218 (1.2), `E[𝔗^p | J] ≤ C_p(1 + |J|)^p` for the vector `J` of free jets at `0` of order
`≤ N₀` (uniformly nondegenerate under `Q̄_{r,0}` by #237 Lemma R (R.4); #218 Step F1 is the same argument under `Q`). `𝔗` is
invariant under `f ↦ f̃`.

`𝔗` dominates the remainders of Lemma Π at every `k ∈ [−1, 1]`. In #237's proof of Lemma Π (through #218 Step F1) those
remainders are Taylor remainders of the pinned field. So for every `C⁹` field `g` pinned at `v(k)`,
`det K_M(g) = −6kΔ + rU − r²V + O(r³(1 + |k|)^N(1 + ‖g‖_{C⁹(𝔅)})^N)`, and likewise for `K_S`, with `U`, `V` the polynomials
#237 (2.1) in the jets of `g`. The coupling terms of #218's `T` are not used there. We apply this to `g = f + kμ`, which is pinned
at `v(k)`.

**Lemma E.** For `0 < r ≤ r_0^*` and `|k| ≤ 1`, with `′ = d/dk` and everything evaluated at `f + kμ`:

    ∂_k(det K_S − det K_M) = 6(det A_S + det A_M) + O(r²𝔗^N) = 12Δ + O(r²𝔗^N),                                  (E.1)
    ∂_k(det K_S + det K_M) = O(r𝔗^N),        ∂_k²(det K_S ± det K_M) = O(r𝔗^N).                                    (E.2)

Hence `r y_k′ = 6sΔ + O(r²𝔗^N)`, `x_k′ = O(𝔗^N)` and `x_k″ = O(𝔗^N)`. Moreover, by Lemma Π at gap `0`,

    x₀ = sY′ + O(r²𝔗^N),        y₀ = rsV_o + O(r²𝔗^N),        x₀′ = ξ̂ + O(r𝔗^N),   ξ̂ := s(3Δ_B − γᵀA^♯γ_μ/2),          (2.1)

where `γ_μ := ∂_u²∇_Θμ(0)`. `Y′` and `ξ̂` do not involve `f₅` or higher jets, and `ξ̂` does not involve `f₄`; `V_o` is affine
in `f₄` with slope `Δ_B/24`; `Y′` is affine in `f₄` with slope `Δ/12`. `ξ̂` and `V_o` are odd, `Y′` and `Δ` even.

*Proof.* Write `g = f + kμ`, `α_i := ∂_u²g(i)/r` and `β_i := ∇_Θ∂_ug(i)/r`, so that `K_i = [[α_i, √r β_iᵀ], [√r β_i, A_i]]`.
For a bordered matrix, `(adj K_i)_{uu} = det A_i`, `(adj K_i)_{uΘ} = −√r adj(A_i)β_i` and
`(adj K_i)_{ΘΘ} = α_i adj(A_i) + O(r𝔗^N)`.
- *The entries of `K_i(μ)`.* `μ` is odd and `V_r(μ) = v(1)`, so `∂_u²μ`, `∇_Θ∂_uμ` and `∇_Θ²μ` are odd. With [R] §2's
  `T_r = ∂_u³(·)(0) + O(r²)` on `C⁵` functions, `∂_u³μ(0) = 12 + O(r²)`. Hence
  `K_S(μ)_{uu} = ∂_u²μ(S)/r = 6 + O(r²) = −K_M(μ)_{uu} + O(r²)`,
  `K_i(μ)_{uΘ} = ±(√r/2)γ_μ + O(r^{5/2})` and `K_i(μ)_{ΘΘ} = ±(r/2)B_μ + O(r³)` (sign `+` at `S`), with `B_μ := ∂_u∇_Θ²μ(0)`.
- *The pinned jets of `g`* (#237's proof of Lemma Π): `∂_u²g(0) = O(r²𝔗)` and `∇_Θ∂_ug(0) = O(r²𝔗)`. So
  `α_S + α_M = O(r𝔗)`, `β_S + β_M = O(r𝔗)`, `β_S − β_M = γ(g) + O(r²𝔗)`, `A_S + A_M = 2A + O(r²𝔗)` and
  `A_S − A_M = rB(g) + O(r³𝔗)`. Here `γ(g)`, `B(g)` are the jets of `g`, equal to `γ`, `B` at `k = 0`; `A(g) = A`.
- *Jacobi's formula* (S.2), term by term:
  `∂_k det K_S = 6 det A_S − r(adj(A_S)β_S)·γ_μ + (r/2)tr((adj K_S)_{ΘΘ}B_μ) + O(r²𝔗^N)` and
  `∂_k det K_M = −6 det A_M + r(adj(A_M)β_M)·γ_μ − (r/2)tr((adj K_M)_{ΘΘ}B_μ) + O(r²𝔗^N)`.
- *The difference.* `adj(A_S)β_S + adj(A_M)β_M = A^♯(β_S + β_M) + (adj A_S − A^♯)β_S + (adj A_M − A^♯)β_M = O(r𝔗^N)`, since
  `adj A_S − A^♯ = −(adj A_M − A^♯) + O(r²𝔗^N)` and `β_S − β_M = O(𝔗)`. Likewise `(adj K_S)_{ΘΘ} + (adj K_M)_{ΘΘ} = O(r𝔗^N)`,
  from `α_S + α_M = O(r𝔗)`. And `det A_S + det A_M = 2Δ + O(r²𝔗^N)`, since `det(A + h) + det(A − h) − 2det A = O(|h|²𝔗^N)` with
  `h = (A_S − A_M)/2 = O(r𝔗)` and `A_S + A_M − 2A = O(r²𝔗)`. This is (E.1).
- *The sum.* With `Δ_B(g) := tr(A^♯B(g))`, `det A_S − det A_M = rΔ_B(g) + O(r³𝔗^N)` and
  `adj(A_S)β_S − adj(A_M)β_M = A^♯γ(g) + O(r𝔗^N)`, while `(adj K_S)_{ΘΘ} − (adj K_M)_{ΘΘ} = O(𝔗^N)` enters multiplied by `r`. So
  `∂_k(det K_S + det K_M) = O(r𝔗^N)` for `|k| ≤ 1`. At `k = 0`, where `Δ_B(g) = Δ_B` and `γ(g) = γ`, the last difference is
  `O(r𝔗^N)`: there `α_S, α_M = O(r𝔗)` (since `∂_u²g(0)` and `∂_u³g(0)` are `O(r²𝔗)`), and `adj A_S − adj A_M = O(r𝔗^N)`. Hence
  `∂_k(det K_S + det K_M)|_{k=0} = 6rΔ_B − rγᵀA^♯γ_μ + O(r²𝔗^N)`.
- *Second derivatives.* `∂_k² det(K + kL)` is a sum of the `2 × 2` minors of `L = K_i(μ)` times complementary cofactors of
  `K + kL`; every `2 × 2` minor of `K_i(μ)` is `O(r)`, by the sizes `O(1)`, `O(√r)`, `O(r)` of its `uu`, `uΘ`, `ΘΘ` entries.
- *Division.* `y = s(m_S − m_M)/2` and `x = s(m_S + m_M)/2`, with `m_i = det K_i/r`; this gives the stated derivatives. At
  `k = 0`, Lemma Π gives `m_M = Y′ − rV_o + O(r²𝔗^N)` and `m_S = Y′ + rV_o + O(r²𝔗^N)`, hence the first two parts of (2.1), and
  the sum above gives `x₀′ = s(6Δ_B − γᵀA^♯γ_μ)/2 + O(r𝔗^N)`. The parities: `B`, `γ`, `f₅` are odd and `A`, `C`, `η`, `f₄` even
  (so `Δ_B` and `A^♯_B` are odd, and `V_o` is odd by #237 §2), and `γ_μ` is deterministic. ∎

(Control L1 checks (E.1), the first part of (E.2) and the reflection of (S.3), in exact rational arithmetic, at five random
pinned polynomial fields, three in `d = 2` and two in `d = 3`, with `r` and `k` symbolic: the `r⁰` and `r¹` coefficients of
`∂_k(det K_S − det K_M) − 12Δ` vanish, and so does the `r⁰` coefficient of `∂_k(det K_S + det K_M)`. The absence of the `r¹`
term comes from the gradient-difference pins; mutant M7, a nonzero transverse gradient-difference target, produces one.)

## 3. Proof of Lemma U₀

Fix `u`, `0 < r ≤ r₄` and `0 < k ≤ r`; `κ = k/r ≤ 1`. Let `f ~ Q̄_{r,0}`, write `E` for `E_{Q̄_{r,0}}`, `g_t := f + tμ`, `x_t, y_t` as
in §1, and `c_τ := 6τ|Δ|`.

*Step 0 (reductions).*
- `𝐓_r(t) = 12p_r e^{−a_r t²}E[W_t]` with `W_t := r^{−2}Π(g_t)1_{typed}(g_t)`, `p_r := p_{V_r}(v(0))` and
  `a_r := v(1)ᵀCov(V_r)^{−1}v(1)/2`, bounded above and below. Since `0 ≤ W_t ≤ C𝔗^N`, the factor `e^{−a_rk²} − 1` costs
  `O(k²) ≤ O(rk)`.
- `Λ_κ` versus its version at `r`, `Λ_κ^{(r)} := 12p_rE[(c_κ² − Y′²)₊1{A<0}]`: by Lemma R (R.4) the law of the finite jet vector
  under `Q̄_{r,0}` and `p_r` are smooth even functions of `r`; Gaussian interpolation of the means and covariances (as in #237
  Step U3) and `(c_κ² − Y′²)₊ ≤ 36κ²Δ²` give `|Λ_κ − Λ_κ^{(r)}| ≤ Cr²κ² = Ck² ≤ Crk`.

It therefore suffices to prove

    |E[W_k] − E[W_0] − E[(c_κ² − Y′²)₊1{A < 0}]| ≤ C r k.                                                            (3.1)

*Step 1 (cases).* Put `ε₀ := r^{3/4}`, `C₁ := {λ_max(A) < −ε₀}`, `C₂ := {λ_max(A) > ε₀}`, `C₃ := {|λ_max(A)| ≤ ε₀}` (events of the
jet `A` alone), and `𝔊 := {𝔗 ≤ r^{−1/8}}`.
- *Lipschitz bound.* `t ↦ W_t` is continuous (by (S.5), `W_t = |m_Mm_S|` jumps to or from `0` only where a factor vanishes) and
  piecewise polynomial, with `|∂_t(m_Mm_S)| ≤ C𝔗^N/r` by Lemma E and `|m_i(g_t)| ≤ C𝔗^N` on `[0, r]` ((2.1) and Lemma E). So
  `|W_k − W_0| ≤ Cκ𝔗^N`, and likewise `|G(x_k, y_k) − G(x_0, y_0)| ≤ Cκ𝔗^N`.
- *Off `𝔊`.* `P(𝔊^c) ≤ C_pr^{p}` for every `p`, so these parts of (3.1) are `O(κr^p) ≤ O(rk)`, uniformly in `k ∈ (0, r]`; also
  `E[c_κ²1_{𝔊^c}] ≤ Cκ²r^p`.
- *`𝔊 ∩ C₂`.* `‖A_i(g_t) − A‖ ≤ r𝔗 ≤ r^{7/8} < ε₀/2` for small `r`, so `A_i(g_t)` has a positive eigenvalue, `H_M(g_t) ≮ 0`, and
  `W_t = 0` for `t ∈ [0, k]`. Also `A ≮ 0`.
- *`𝔊 ∩ C₁`.* Likewise `A_M(g_t), A_S(g_t) < 0`, so `W_t = G(x_t, y_t)` by (1.1).

*Step 2 (the near-singular case `C₃`).* On `𝔊 ∩ C₃`, `|Δ| ≤ ε₀𝔗^{m−1}` and `|λ_max(A_i(g_t))| ≤ 3ε₀/2`, so `|det A_i| ≤ 2ε₀𝔗^{m−1}`.
- By Lemma Π at gap `t`, applied to the pinned field `g_t` (with `U_t := Y′(g_t) + 3tΔ_B(g_t)`, the `U` of #237 (2.1) built from
  the jets of `g_t`), `|m_i(g_t) − U_t| ≤ C(κε₀ + r)𝔗^N =: δ₃` for both `i`. If `g_t` is typed, `𝔞 < 0 < 𝔟` forces `|U_t| ≤ δ₃`,
  so `|m_i(g_t)| ≤ 2δ₃`.
- By Jacobi's formula and Lemma E's entries, `|∂_t det K_i| ≤ 6|det A_i| + Cr𝔗^N`, so `|∂_t m_i| ≤ C(ε₀/r + 1)𝔗^N`, and over
  `[0, k]` each `m_i` moves by at most `C(κε₀ + k)𝔗^N`.
- If `g_0` and `g_k` are both typed, `|W_k − W_0| ≤ C(κε₀ + k)δ₃𝔗^N`. If exactly one is typed, (S.5) gives a zero of some `m_i` on
  `[0, k]`, so at the typed end that factor is `≤ C(κε₀ + k)𝔗^N` and the other is `≤ 2δ₃`. In all cases
  `|W_k − W_0| ≤ C(κε₀ + k)(κε₀ + r)𝔗^N ≤ Cκr^{3/2}𝔗^N`.
- Conditioning on `A` (`E[𝔗^N | A] ≤ C(1 + ‖A‖)^N`, the bound of §2, that is #218 (1.2)) and #218 Lemma D (first bound) give
  `E[𝔗^N1_{C₃}] ≤ Cε₀`. So `C₃` contributes `≤ Cκr^{9/4} ≤ Crk` to (3.1), and the main term `≤ 36κ²E[Δ²1_{C₃}] ≤ Cκ²ε₀³ ≤ Crk`
  (control L6 checks the exponents).

*Step 3 (the regular case `C₁`: the derivative).* Put `F(t) := E[G(x_t, y_t)1_{C₁}]` and `Φ(τ) := E[(c_τ² − Y′²)₊1_{C₁}]`. By
Step 1 the `C₁`-parts of (3.1) are `F(k) − F(0) − Φ(κ) + O(rk)`, and `Φ(0) = 0`.
- Both functions are Lipschitz on `[0, k]`: `Φ` is `C¹`, and for each realization `t ↦ G(x_t, y_t)` is Lipschitz with constant
  `C𝔗^N/r` (`G` is Lipschitz on bounded sets; `x_t, y_t` are polynomials in `t` with coefficients `O(𝔗^N/r)`).
- `G` is differentiable off `{|x| = y > 0}`. A path meets this set at finitely many `t`, unless `x_t ≡ ±y_t` with `y_t ≥ 0`, in
  which case `G(x_t, y_t) ≡ 0` and the formula below also gives `0`. By Fubini, `F′(t) = E[∂_tG(x_t, y_t)1_{C₁}]` for almost
  every `t`, and

      F(k) − F(0) − Φ(κ) = ∫_0^k [F′(t) − r^{−1}Φ′(t/r)] dt.

It suffices to show `|F′(t) − r^{−1}Φ′(t/r)| ≤ Cr` for almost every `t ∈ (0, k]`. Off `{|x| = y > 0}`, `∂_xG = −2x1{|x| < y}` and
`∂_yG = 2y1{|x| < y}`; and `Φ′(τ) = E[12|Δ|c_τ1{|Y′| < c_τ}1_{C₁}]`. With `r y_t′ = 6|Δ| + e_t`, `|e_t| ≤ Cr²𝔗^N` on `C₁`
(Lemma E; `sΔ = |Δ|` on `{A < 0}`), and `τ := t/r`,

    F′(t) − r^{−1}Φ′(τ) = (12/r) I₁ + (2/r) I₂ − 2 I₃,
    I₁ := E[|Δ|(y_t1{|x_t| < y_t} − c_τ1{|Y′| < c_τ})1_{C₁}],   I₂ := E[y_t1{|x_t| < y_t}e_t1_{C₁}],   I₃ := E[x_t1{|x_t| < y_t}x_t′1_{C₁}].

So we need `|I₁| ≤ Cr²`, `|I₂| ≤ Cr²` and `|I₃| ≤ Cr`. `I₂` is immediate: `|y_t| ≤ C𝔗^N`.

*The polynomial frame.* Put `x̂ := sY′` (even), `v := rsV_o` (odd), `ŷ_t := v + c_τ` and `ζ_t := tξ̂` (odd). By Lemma E and (2.1),
on `C₁` and for `0 ≤ t ≤ r`,

    |x_t − x̂ − ζ_t| ≤ Cr²𝔗^N,        |y_t − ŷ_t| ≤ Cr²𝔗^N,        |x_t′ − ξ̂| ≤ Cr𝔗^N.                                      (3.2)

*The integration variable.* On `C₁`, `x̂ = (|Δ|/12)f₄ + sβ`, with `β := −γᵀA^♯γ/4`. Given the other free jets `J^♭`, `f₄` is
Gaussian with a mean `m₄` that is linear in the *even* jets and a variance `σ₄² ∈ [c, C]` (Lemma R (R.2); #218 Step F1). So,
given `J^♭`, `x̂` is Gaussian with a density `p` of scale `|Δ|σ₄/12` (`sup p ≤ C/|Δ|`, `sup|p′| ≤ C/Δ²`) that depends on even
quantities only.
- Write `V_o = (Δ_B/24)f₄ + a₀`, with `a₀` free of `f₄`. Then `v` is an affine function `v(x̂)` of `x̂`, with slope
  `ϑ := rsΔ_B/(2|Δ|)` (odd).
- Put `f₄^0 := −12sβ/|Δ|` (where `x̂ = 0`), and write `v_± := v(±c_τ)` for the value of `v` where `x̂ = ±c_τ`, that is at
  `f₄ = f₄^± = f₄^0 ± 72τ`. It is odd: each term of `V_o` has an odd number of odd factors, and `f₄^±` is even. Also
  `|v_±| ≤ Cr(1 + |Δ_B| + |a₀|)(1 + |f₄^0|)`.
- Put `𝔖 := {|Δ| ≥ r(1 + |Δ_B|)}`, an even event. On `𝔖`, `|ϑ| ≤ 1/2`.

*Sets.* For `|ϑ| ≤ 1/2` and `w ∈ R`, `{x̂ : |x̂ + w| < c_τ + v(x̂)}` is the interval `(X₋, X₊)` (empty if `X₋ ≥ X₊`) with, exactly,

    X₊ − c_τ = (v₊ − w)/(1 − ϑ),        X₋ + c_τ = −(v₋ + w)/(1 + ϑ).                                               (3.3)

So its endpoints differ from `±c_τ` by at most `2(|v_±| + |w|)`. Likewise, `x̂ ↦ |x̂| − c_τ − v(x̂)` has slope at least `1/2` in
modulus on each half-line, so `{||x̂| − c_τ − v(x̂)| ≤ δ}` is at most two intervals of total length `≤ 8δ`.

*The layer device* (#237 Step U2 (a)). Remainders carry `𝔗^N`.
- On the layer `{𝔗 ∈ [2^j, 2^{j+1})}` replace `𝔗` by `2^{j+1}`, and use `P(𝔗 ≥ 2^j | J) ≤ C_p2^{−jp}(1 + |J|)^p`.
- Integrate `x̂` given `J^♭` against `p`; after multiplication by `(1 + |J|)^p`, `p` stays bounded by `C(1 + |J^♭|)^N/|Δ|`. In
  particular, on `𝔖`, an event that confines `x̂` to `O(1)` intervals of total length `λ` (depending on `J^♭` and the layer)
  has weighted probability `≤ Cλ/|Δ|`.
- *Absorbing `f₄^0` (on `𝔖`).* In `f₄`-coordinates the interval of (3.3) is `((f₄^0 − e₋)/(1 + ϑ), (f₄^0 + e₊)/(1 − ϑ))` with
  `e_∓ := 12(c_τ + rsa₀ ± w)/|Δ|`; for `v ↦ −v` replace `(ϑ, a₀, w)` by `(−ϑ, −a₀, −w)`. On `𝔖`, `r ≤ |Δ|` and
  `|ζ_t| ≤ |Δ||ξ̂|` (as `t ≤ r`), so `|e_∓| ≤ E := C(1 + |a₀| + |ξ̂|)` whenever `|w| ≤ |ζ_t|`. Since `|ϑ| ≤ 1/2`, these
  intervals, their symmetric differences, and the segments between `±c_τ` and `X_±` all lie in
  `{|f₄| ≥ (2/3)(|f₄^0| − E)}`, where `(1 + |f₄^0|)^n p ≤ C_n(1 + E + |m₄|)^n/|Δ|`. On `{c_τ ≥ 4η}` (below) the
  `2η`-neighbourhoods of `±c_τ` have `f₄`-radius `24η/|Δ| ≤ 36τ`. This is what absorbs the powers of `|f₄^0|` below.
  Closeness to `±c_τ` in `x̂` alone would not: an `x̂`-window of length `≍ |v_±|` has `f₄`-length up to `2|ϑ||f₄^±| + C`, and
  without the Gaussian factor `E[η²1_{C₁∩𝔖}] ⊇ (r²/4)E[Δ_B²β²Δ^{−2}1_{C₁∩𝔖}] ≫ r²`.
- Off `𝔖`, `|Δ| < r(1 + |Δ_B|)` is a polynomial bound, used directly.
- `E[|Δ|^{−1}1_𝔖(1 + |J|)^N] ≤ Clog(2/r)`, by #218 Lemma D (second bound) in dyadic layers of `|Δ| ≥ r`.

*`I₃`.*
- By (3.2), replacing `x_t′` by `ξ̂` costs `O(r)`, since `|x_t| < y_t ≤ C𝔗^N` on the support.
- Replacing `x_t1{|x_t| < y_t}ξ̂` by `x̂1{|x̂| < ŷ_t}ξ̂` costs at most `|ξ̂|(|x_t − x̂| + (|ŷ_t| + δ)1{||x̂| − ŷ_t| ≤ δ})`, with
  `δ := |x_t − x̂| + |y_t − ŷ_t| ≤ C(t + r²)𝔗^N`.
  - On `𝔖` the indicator confines `x̂` to length `≤ 8δ`, so after the layer device it costs `≤ CE[(r + κ|Δ|)r/|Δ|]`.
  - Off `𝔖` the whole term is `≤ C(r + κr)(1 + |J|)^N𝔗^N`, on an event of probability `≤ Cr`.

  With `E[|Δ|^{−1}1_𝔖] ≤ Clog(2/r)`, the replacement costs `O(r)`.
- For the main part, the reflection (S.3) maps `(x̂, v(·), ξ̂)` to `(x̂, −v(·), −ξ̂)` and fixes `C₁`, `𝔖`, `c_τ`, `p` and the
  law. So

      E[x̂ξ̂1{|x̂| < c_τ + v}1_{C₁}] = ½E[x̂ξ̂(1{|x̂| < c_τ + v} − 1{|x̂| < c_τ − v})1_{C₁}].

  By (3.3) with `w = 0`, the two indicators differ on intervals of total length `≤ 4(|v₊| + |v₋|)` near `±c_τ`, where
  `|x̂| ≤ c_τ + 2(|v₊| + |v₋|)`. On `𝔖` this is `≤ CE[(κ|Δ| + r)|ξ̂|·r/|Δ|] ≤ C(κr + r²log(2/r))`; off `𝔖` it is `≤ Cr²`.

So `|I₃| ≤ Cr`.

*`I₁`.* Replace `(x_t, y_t)` by `(x̂ + ζ_t, ŷ_t)`.
- By (3.2) this costs `E[|Δ||y_t − ŷ_t|] ≤ Cr²`, plus `E[|Δ||ŷ_t|1{||x̂ + ζ_t| − ŷ_t| ≤ Cr²𝔗^N}]`.
- The latter is `≤ Cr²`. On `𝔖` the window has `x̂`-length `≤ Cr²𝔗^N`, the density is `≤ C/|Δ|` and the weight is `|Δ||ŷ_t|`.
  Off `𝔖`, `|Δ||ŷ_t| ≤ Cr²(1 + |J|)^N𝔗^N`.

What remains is

    E[|Δ|(ŷ_t1{|x̂ + ζ_t| < ŷ_t} − c_τ1{|x̂| < c_τ})1_{C₁}] = E[|Δ|v1{|x̂ + ζ_t| < c_τ + v}1_{C₁}] + E[|Δ|c_τ(1{|x̂ + ζ_t| < c_τ + v} − 1{|x̂| < c_τ})1_{C₁}].

- *The first term.* By the reflection it equals `½E[|Δ|v(1{|x̂ + ζ_t| < c_τ + v} − 1{|x̂ − ζ_t| < c_τ − v})1_{C₁}]`.
  - By (3.3) the two sets differ on intervals of total length `≤ 8η` near `±c_τ`, where `η := |v₊| + |v₋| + |ζ_t|`, and there
    `|v| ≤ 3η`.
  - So on `𝔖` the term is `≤ CE[|Δ|η²/|Δ|] ≤ C(r² + t²) ≤ Cr²`, the Gaussian factor of `p` absorbing the powers of `|f₄^0|`.
  - Off `𝔖` it is `≤ Cr²` directly (`|Δ| ≤ r(1 + |Δ_B|)`, `|v| ≤ Cr(1 + |J|)^N`).
- *The second term.* By (3.3) with `w = ζ_t`, the first event is `{X₋ < x̂ < X₊}`.
  - *Where `c_τ ≥ 4η`* the interval is nonempty. By Taylor's formula for the distribution function of `x̂`,
    `P(X₋ < x̂ < X₊) − P(|x̂| < c_τ) = p(c_τ)(v₊ − ζ_t) + p(−c_τ)(v₋ + ζ_t) + R`. Here
    `|R| ≤ C(η|ϑ|·sup_{±c_τ}p + η²·sup|p′|)`, the sup taken within `2η` of `±c_τ`. The first-order part is a sum of odd
    quantities (`v_±`, `ζ_t`) with even coefficients (`p(±c_τ)`), so its expectation against the even weight
    `|Δ|c_τ1{c_τ ≥ 4η}1_{C₁∩𝔖}` vanishes by the reflection (`η` is a sum of moduli of odd quantities, so `{c_τ ≥ 4η}` is
    even). With `|ϑ| ≤ r|Δ_B|/(2|Δ|)`, `p ≤ C/|Δ|`, `|p′| ≤ C/Δ²` and `|Δ|c_τ ≤ 6κΔ²`, the remainder contributes
    `≤ Cκ(ηr|Δ_B| + η²) ≤ Cκr²`.
  - *Where `c_τ < 4η`*, both probabilities are `≤ C(c_τ + η)/|Δ|`, and with the weight `|Δ|c_τ` the term is `≤ Cη² ≤ Cr²`.
  - *Off `𝔖`*, `|Δ|c_τ ≤ 6κΔ² ≤ Cr²(1 + |J|)^N`, and the term is `≤ Cr²` directly.

So `|I₁| ≤ Cr²`. Hence `|F′(t) − r^{−1}Φ′(τ)| ≤ Cr`, and integrating over `t ∈ (0, k]` gives `|F(k) − F(0) − Φ(κ)| ≤ Crk`.

*Conclusion.* Steps 0–3 give (3.1), hence (U₀), with `r₄ ≤ r_0^*` small enough for Step 1. ∎

## 4. Proofs of Theorem U⁼ and Theorem P⁺

*Theorem U⁼.*
- *`κ ≤ 1`.* By (U₀), (0.2) and Lemma K (`|𝐀₂(k) − 𝐀₂(0)| ≤ Ck²`), the left side of (U⁼) is
  `≤ Crk + Ck²κ² + Ck² ≤ C′rk = C′r²min(1, κ)`.
- *`κ ≥ 1`.* Then `k ≥ r ≥ r²`, so #237's (U.1) applies (take `r₄ ≤ r₃`), with error `C(r² + r min(k, 1/k))`. And
  `0 ≤ 𝐓_r(0, u) ≤ Cr³log(2/r) ≤ Cr²` by #229 (W⁺.2) at `κ = 0`, integrated in `b`. ∎

*Theorem P⁺.* Use #237 §5's decomposition, at its radius `r₀ ∈ (0, r_0^*]`, with a *fixed* split `ρ := min(r₄, r₀/2)` and
`ℓ ≤ ρ³`:

    ν_cand − cℓ^{−1/3} − B_{d,L} = ∫_0^ρ∫_S[𝐓_r(ℓ/r³, u) − r^{−2}𝐀_0(ℓ/r³, u)] dσ dr + J₂ + J₃ + J₄ + J₅.

- *`J₂` is absorbed.* `J₂ = −∫_0^ρ∫∫r^{−2}A_r(b, 0, u) = −∫_0^ρ∫𝐓_r(0, u)dσ dr`, which cancels the `𝐓_r(0)` of (U⁼).
- *The main terms*, exactly as in #237 §5: `∫_0^ρ[𝐀₂(ℓ/r³) − 𝐀₂(0)]dr = c₂ℓ^{1/3} + O(ℓ²ρ^{−5})` (after `∫dσ`; #218 (0.1) and
  Lemma K), and `∫_0^ρ𝓐(ℓ/r⁴)dr = I^{cand}ℓ^{1/4} + O(ℓ²ρ^{−7})`.
- *The error of (U⁼)* integrates over `[0, ρ]` to at most `C((4/3)ℓ^{3/4} + (6/5)ℓ^{2/3})`: `∫_0^ρ r²min(1, ℓ/r⁴)dr ≤ ℓ^{3/4}/3 + ℓ^{3/4}`,
  splitting at `ℓ^{1/4}`, and `∫_0^∞ r min(ℓ/r³, r³/ℓ)dr = ℓ^{2/3}/5 + ℓ^{2/3}`, splitting at `ℓ^{1/3}` (control L5).
- *The rest* (#237 §5 with `ρ` fixed): `|J₃| ≤ C(ℓ²ρ^{−7} + ℓρ^{−2}) = O(ℓ)` (#207 (7.1), `k ≤ ℓρ^{−3} ≤ 1`),
  `0 ≤ −J₄ ≤ Cℓ²ρ^{−7} = O(ℓ²)`, and `|J₅| ≤ Cℓ` (#207 (7.2)).

The least exponent is `2/3`, from the fold-scale part of (U⁼); the next are `3/4` and `1` (control L4). ∎

## 5. Proof of Corollary LU

Use note TS §5 with `ρ := ℓ^σ` in place of its `ℓ^{3/14}` (the decomposition (5.1), `𝒦₂`, the cusp tails and `J₄` with (5.0),
and `I^{eld}` on `[ρ, ℓ^{1/5}]`; TS's second split `a` is not used), with two replacements:
- *In `𝒦₁`*, Theorem U⁼ in place of #237's Lemma U:
  `𝒦₁ = ∫_0^ρ∫𝐓_r(0) + c₂ℓ^{1/3} + I^{cand}ℓ^{1/4} − ∫_ρ^∞∫𝓐(ℓ/r⁴, u)dσ dr + O(ℓ^{3/4} + ℓ^{2/3} + ℓ²ρ^{−5})`. Note TS's
  (5.1) has no `J₂`, so the term `∫_0^ρ∫𝐓_r(0, u)dσ dr` stays; by #229 (W⁺.3) it is `≤ Cρ⁴log(2/ρ)`. (With `y = ru`,
  `dy = r^{d−1}dr dσ(u)` for `ρ < L/2`, and `r^{d−1}Ψ_0(b, ru) = r^{−2}A_r(b, 0, u)` as in #229's proof of (W⁺.3), the integral in
  (W⁺.3) is this one; equivalently, integrate (W⁺.2) at `κ = 0` over `[0, ρ]`.)
- *`I^{eld}` on `[ℓ^{1/5}, r_0^*]`*: Corollary EM.1, `O(ℓ^{2/3}log(1/ℓ))`.

Take `σ = 5/24`, and `ℓ` so small that `ρ ≤ min(r₄, r₀)`, with `r₀` the radius of Theorem TL⁻ at `θ = 4/5`, that `ℓ^{1/4}` is
below the radius of Theorem TL, and that `ℓ^{1/5} < r_*`. Then `ℓ^{1/4} < ρ < ℓ^{1/5}`, and on `[ℓ^{1/4}, ρ]`,
`κ = ℓ/r⁴ ≥ ℓ^{1/6} = ρ^{4/5} ≥ r^{4/5}`. So Theorem TL⁻ applies with `θ = (1 − 4σ)/σ = 4/5 < 1` (note TS §5's `θ = 2/3` does not
reach `κ = ρ^{4/5}`), and the ledger is:

| Term | Source | Exponent at `σ = 5/24` |
|---|---|---|
| `ℓ^{2/3}` | the fold-scale part of (U⁼); Corollary TL1; (S″.2) on `[r_*, r_0^*]`; #187 | **2/3** |
| `ℓ^{2/3}log(1/ℓ)` | Corollary EM.1 (both regions of the elder weight on `κ ≤ r`, with (W⁺.2)) | **2/3**, with `log(1/ℓ)` |
| `ρ⁸/ℓ` | the `r³/κ` part of (TL⁻) | **2/3** (`8σ − 1`) |
| `ℓ^{3/4}` | the `r²min(1, κ)` part of (U⁼); the `κr²` part of (TL⁻) | 3/4 |
| `ℓ²ρ^{−6}log(1/ℓ)` | (W⁺.2) on `[ρ, ℓ^{1/5}]` | 3/4 (`2 − 6σ`), with `log(1/ℓ)` |
| `ℓ³ρ^{−11}` | the elder cusp tail; (W⁺.2) on `[ρ, ℓ^{1/5}]` | 17/24 (`3 − 11σ`) |
| `ρ⁴log(2/ρ)` | `∫_0^ρ∫𝐓_r(0)`, #229 (W⁺.3) | 5/6 (`4σ`), with `log(1/ℓ)` |
| `ℓ²ρ^{−5}` | the finite part of `𝐀₂` | 23/24 |
| `ℓ⁴ρ^{−13}` | the contact difference (5.0) | 31/24 |

The least exponent is `2/3`, with `log(1/ℓ)`; every `σ ∈ [5/24, 7/33]` gives the same (control L4). This is the first line of (LU).
Subtracting it from (P⁺) gives the second (`cℓ^{−1/3}` and `c₂ℓ^{1/3}` cancel). For SIDE24 divide by `cℓ^{−1/3}`: `2/3 + 1/3 = 1`. ∎

## 6. Remarks

1. **Why the error is `O(rk)`.** In `y = s(m_S − m_M)/2` the gap enters at slope `6|Δ|/r` (E.1), and the `r¹` correction to that
   slope cancels between the endpoints; that cancellation comes from the gradient-difference pins. Everything else that moves
   with `k` is odd at `k = 0`: the endpoint difference `y₀ ≈ rsV_o` and the drift `ξ̂` of the endpoint sum (oddness of `μ` is what
   makes `ξ̂` odd). Their first-order effects average to zero over the reflection, so the `k`-derivative of the error is `O(r)`,
   with no `O(1)` part. This is #237's parity (Lemma Λ, Step U2 (b)) carried to the whole range `κ ≤ 1`, at the level of the
   exact endpoint determinants rather than the layer variable alone.
2. **What fixes `2/3` now.**
   - *The candidate density.* Only the fold-scale term `r min(k, 1/k)` of #237's (U.1), on `κ ≥ 1`. Over `[0, ℓ^{1/4}]` it
     integrates to `(6/5)ℓ^{2/3} − ℓ^{3/4}`; Lemma U₀'s range `κ ≤ 1` contributes at most `ℓ^{3/4}`. #237 Remark 2 calls it
     plausibly the next term, and the author-side referee numerics in #237's README (review record) found the `k²/κ`
     coefficient of the layer nonzero for the Gaussian kernel in `d = 2`. Going beyond `2/3` for `ν_cand` would need that
     coefficient.
   - *The elder and rejected densities.* For every `σ ∈ [5/24, 7/33]` four rows sit at `2/3`: that fold-scale term, Corollary
     TL1, the intermediate mass (Corollary EM.1, with a logarithm) and the far bound (#187). The rows `ρ⁸/ℓ` (Theorem TL⁻'s
     `r³/κ`) and `ℓ³ρ^{−11}` reach `2/3` only at the ends `σ = 5/24` and `σ = 7/33`. Going beyond `2/3` would need all four.
     #242's Conjecture 7 predicts a term `R_{2/3}ℓ^{2/3}` of `ρ_rej + ν_eld^{far,r_0^*}` (numerically `R_{2/3} ≈ −0.061` for the
     Gaussian kernel in `d = 3`), so for these densities `2/3` is expected to be the order of the next term. (LU) neither proves
     nor tests that conjecture.
3. **Numerical illustration** (exploration; not part of the proof; numpy and scipy, outside the repository; script
   `toy_diff.py`, SHA-256 `1f9653b8b5ab7acec756c16226da61caca7b037a751a2bd44ba665f9525cd9cd`, and its output `toy_diff_out.txt`,
   published with the controls in the next comment). A toy model in `d = 2` (`m = 1`), with an ad hoc Gaussian law of the jets,
   the polynomials (2.1), the endpoint quantities `m_i = det K_i/r` of Lemma Π truncated after order `r`, the law shift of the
   odd jets, `f₄` integrated exactly and the rest by Monte Carlo with reflection pairs, gives `D := T(k) − T(0) − Λ_κ` (both
   without the density factor) with `D/(r²κ)` bounded:

   | `r` | `κ = r²` | `κ = r` | `κ = 0.3` | `κ = 1` |
   |---|---|---|---|---|
   | 0.1 | 0.121 | −0.525 | −2.445 | −9.007 |
   | 0.05 | 0.132 | −0.110 | −2.452 | −9.029 |
   | 0.025 | 0.125 | 0.055 | −2.456 | −9.040 |

   (2·10⁷ samples per entry; standard errors at most `0.004`.) A referee's independent toy, in `d = 3` with an exact
   Gaussian-kernel jet law, found `D/(rk)` converging for `κ ∈ {r², r, 1/4, 1/2, 1}`, and found that giving the odd jets a
   nonzero mean at `k = 0` (breaking the reflection) makes `D` of order `k`, not `rk`.
4. **Constants.** No constant is certified.

## 7. Exact controls (`lu_exact.py`; stdlib; exact rationals; deterministic; byte-identical under `-O`)

The script and its stdout are published in the next comment, with the extraction rule.
- **L1** Lemma E on pinned polynomial fields, in exact rational arithmetic: five random fields (three in `d = 2`, two in `d = 3`),
  of degree 6 with rational free jets, `r` and `k` symbolic (polynomials in `r` with the pins solved order by order, and the
  pins of `f` and `μ` checked directly). It checks that `μ` is odd and pinned at `v(1)`, that the `r⁰` and `r¹` coefficients of
  `∂_k(det K_S − det K_M) − 12Δ` and the `r⁰` coefficient of `∂_k(det K_S + det K_M)` vanish identically in `k`, and the
  reflection `det K_M(f̃ − kμ) = det K_S(f + kμ)`.
- **L2** (1.1) on rational samples: `(−𝔞)₊𝔟₊1{𝔞 < 0 < 𝔟} = G((𝔞 + 𝔟)/2, (𝔟 − 𝔞)/2)`.
- **L3** The `x₀′` formula of (2.1) on the same fields: the `r¹` coefficient of `∂_k(det K_S + det K_M)` at `k = 0` equals
  `6Δ_B − γᵀA^♯γ_μ`.
- **L4** The ledgers, with transcribed exponents for the `σ`-free rows and exponents from their monomials for the
  `σ`-dependent ones: (P⁺) at fixed `ρ` (least `2/3`, attained only by the fold-scale row), and (LU) at the ends and the
  midpoint of `σ ∈ [5/24, 7/33]` (least `2/3`, with `θ ∈ [5/7, 4/5]`); the rows are affine in `σ`, so this covers the interval.
- **L5** The two integrals of §4, exactly on perfect powers.
- **L6** Step 2's exponents (`9/4 ≥ 2` for `ε₀ = r^{3/4}`, exactly on perfect powers), `r·r^{−1/8} < r^{3/4}/2` on `𝔊` for small `r`,
  and the slope bounds on `𝔖` (`|Δ|/12 − r|Δ_B|/24 ≥ |Δ|/24` and `|ϑ| ≤ 1/2`).

Mutants, each rejected with exit 1, empty stdout and `FAILED: <group>` on stderr:

| Mutant | Change | Fails at |
|---|---|---|
| M1 | (E.1)'s coefficient `12 → 11` | `L1_shift` |
| M2 | the reflection with `f̃ + kμ` in place of `f̃ − kμ` | `L1_shift` |
| M3 | `ξ̂`'s coefficient `3Δ_B → 2Δ_B` | `L3_drift` |
| M4 | the scenario's `σ = 5/24 → 41/200` (inside `(1/5, 5/24)`; the row `ρ⁸/ℓ` drops to `16/25`) | `L4_ledger` |
| M5 | the constant `4/3 → 1` | `L5_integrals` |
| M6 | `ε₀ = r^{3/4} → r^{1/2}` | `L6_exponents` |
| M7 | `f`'s transverse gradient-difference target `0 → r` (pins checked against it; an `r¹` term appears in (E.1)) | `L1_shift` |

**What the controls do not test.** Lemmas R, Π and K and the layer device (#237), Lemma D and (1.2) (#218), the Gaussian
facts behind Lemma S, the probabilistic estimates of §3, #237's (U.1) and §5's main terms, (7.1)–(7.2), (W⁺.2)–(W⁺.3),
Theorem TL⁻ and Corollary TL1, note TS §5, Corollary EM.1, #187, and the transcription of the ledger rows from their sources.

## 8. Review slices

- **A: §§0–2.** The statements, the identity (0.2), Lemma S and Lemma E. Controls L1–L3, mutants M1–M3 and M7.
- **B: §3.** The proof of Lemma U₀: the reductions, the cases, the near-singular case, the derivative, the polynomial frame,
  the integration variable and the absorption of `f₄^0`, the layer device, and the estimates of `I₁`, `I₂`, `I₃`. Control L6,
  mutant M6.
- **C: §§4–6 and the header.** Theorem U⁼, Theorem P⁺, Corollary LU with its ledger against #237 §5, note TS §5 and EM.1, the
  remarks, and the header for overclaim. Controls L4–L5, mutants M4–M5.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_