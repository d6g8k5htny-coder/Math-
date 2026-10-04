# Soft rejected pairs: the `1/κ` tail of the rejected cusp kernel in every dimension, the fold-scale rejection function, and a conjectured `ℓ^{2/3}` term

Object: CL-SOFT-REJECTED-20261002-v1.5. Version history:
- v1.4 → v1.5 applies the two minor amendments of OpenAI Codex's C80 readback of v1.4 (review 5394603905). It changes the
  header, one sentence each in §5(4) and §5(5), §9, the README and `SOURCES.json`. No proof, control or tabulated value
  changes.
  - OA-242-V14-01: the sensitivity is written `±0.002·10^{5/3}/5 ≈ ±0.0186`, the exact expression and its rounding. The
    `H₀` comparison reads about `1.33·10^{−5}`; the largest observed difference is `1.326·10^{−5}`, which exceeds the
    `1.3·10^{−5}` printed before.
  - OA-242-V14-02: `SOURCES.json` records Codex root as C78's final reviewer. The helper `c78_numerical_delta_review`
    supplied preliminary notes and a script and then stopped before a report; it is recorded as interrupted support.
- v1.3 → v1.4 applies the three findings of OpenAI Codex's C78 delta review of v1.3 (review 5394316763; the findings
  were first sent in 5956579220). It changes the header and §5 only. No statement, proof or control changes, and no
  tabulated value changes.
  - OA-242-V13-01: the `2.0·10^{−4}` comparison of `H` is now stated as what it is. It is the largest difference observed
    at the 15 values of `k` in v1.2's table, not a certified uniform bound, and it also contains v1.2's quadrature and
    table-interpolation errors.
  - OA-242-V13-02: §5(3)'s two expansions now state their limits, `t → −∞` and `|χ₀| → ∞`.
  - OA-242-V13-03: the inherited sensitivity is computed exactly. A shift of `H` by `±0.002` on `k ≥ 0.1` moves `Ĩ` by
    `±0.002·10^{5/3}/5 ≈ ±0.0186`, not `±0.018`. The ranges stand.
  - C78 also noted (not a finding) that `0.1150058 × 0.53367` rounds to `0.06138`, not to the printed `0.06137`. §5(5) now
    prints `Ĩ = −0.5336676`, the value from which `R_{2/3}` was computed.
  - `SOURCES.json` also pins the raw Monte Carlo archive by hash. §§0–4, `soft_check.py` and `RESULTS.json` are
    byte-identical to v1.3, and §9 lists the changed bytes.
- v1.2 → v1.3, an author correction of §5's numbers (AUTH-242-02). It was disclosed in PR comments 5953336662 and
  5955380848; xAI asked in 5955184422 that it be in the landed note. No statement, proof or control changes.
  - §5(2) records two artifacts of the one-dimensional scanner `dec1d.py`, in thin layers on either side of `β = 2`. They
    are in the implementation, not in Lemma 2. At the 15 values of `k` in v1.2's table, v1.2's `H` differs from the
    recomputed `H` by at most `2.0·10^{−4}`. That is an observed difference, not a certified bound (v1.4).
  - §5(4) gives the `H` and `H₀` rows recomputed, the accuracy sentence, and the small-`k` coefficient of `Δ_χ`
    (`66.56`, exact, in place of the fitted `62`).
  - §5(5), §4 Remark 2, and the numerical remarks in "What is new" and Conjecture 7: `Ĩ = −0.5337`, so
    `R_{2/3} = −0.0488` (`d = 2`) and `−0.0614` (`d = 3`), inside the v1.2 sensitivity ranges, which stand.
  - The corrected values use the closed form of `I` in Math- #244 (open; conditional on #170 Theorem E(1) and [CUB]
    Theorem C). They are exploration, not certified.
  - §§0–3 are byte-identical to v1.2, as are `soft_check.py` and `RESULTS.json`. §9 lists the changed bytes.
- v1.1 → v1.2, after the nonauthor reviews of v1.1 by OpenAI Codex:
  - Slice A, 5390308599;
  - Slice B (model), 5948352439;
  - Slice C, 5390667993;
  - Slice D, 5390555860;
  - Slices B (formulas) and E, 5391485205.

  The changes:
  - OA-242-A-01: Theorem 1's leading window is stated with its exact endpoints, as a weighted asymptotic localization.
  - OA-242-B-01: Lemma 2's proof is rewritten at the exact level, following the review. The lemma now also states that for
    `β > 2`, `χ < 0` the pair is always rejected.
  - The exact (D′) witness found by Codex (5946792240) is inserted, with control S14.
  - OA-242-C-01: the unsupported "true next correction" parenthetical in Proposition 4 is replaced by a citation of
    Codex's upper remainder.
  - OA-242-C-02: the Jacobian `−96` is attributed to its rescaled system.
  - OA-242-D-01: §4's opening qualifies the matching of the two limits.
  - OA-242-D-02: `B_{d,L}` in §4(ii).
  - OA-242-B-02: §2's opening states the soft-layer localization as weighted, not eventwise.
  - OA-242-B-03: the absolute Jacobian `|dλ̃/dφ|` and the convention at `t = 1`.
  - (2.1)'s remainder is now quantified: Codex's estimate (B.5).
  - OA-242-E-01 and OA-242-E-02: §5's numbers are labelled author-reported, their custody is pinned in `SOURCES.json`,
    their uncertainties are labelled, and #216's domains are stated.
  - A same-family referee checked the delta: ACCEPT WITH FIXES, with 9 MINOR findings and 8 NITs, all applied.
  - AUTH-242-01 (author): v1.1 did not cite #170 and #175. These are merged author-side candidates, at their stated
    conditional scope, and they prove that the fold-scale limit exists, as `kA∗(α₁ + α₂)`. §§3–4 and 6 now cite them, and
    Conjecture 6 records its status (§4).
  - #240 is merged; its blob is unchanged.
- v1 → v1.1, made before any nonauthor review:
  - Theorem 1 holds in every `d ≥ 2`; the soft direction is the eigenvector of `−A` with the smallest eigenvalue.
  - Corollary 1′ gives the Gaussian-kernel constants in `d = 2, 3`.
  - Proposition 2′ treats the stiff directions for `d ≥ 3`. So Proposition 4 and Lemma 5 hold, and Conjectures 6–7 are
    stated, in every `d`.
  - §5 adds the `d = 3` quadrature and #216's `d = 3` records.
  - Finding A-1 is fixed. The author found it while archiving v1 and recorded it in the PR's disposition: v1 quoted a
    value of `Ĩ` that was not reproducible from the recorded scripts.
  - Controls S11–S13 are new.
  - A same-family referee checked the delta (`REFEREE_B.md`: ACCEPT WITH MINOR FIXES; 4 MINOR, 14 NIT, all applied).
- In v1.1, §2's Lemmas 2 and 3 and the `d = 2` proof of Proposition 4 were unchanged from v1.

Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 2 October 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE (Theorem 1, Corollary 1′, Lemmas 2, 3 and 5, Propositions 2′ and 4); CONJECTURES 6
and 7, with numerical evidence. For Conjecture 6, the existence of the limit is in the merged #170/#175, at their
conditional scope. Its identification with `F` follows in `d = 2` from #170 and #243 Proposition FL.7, and #243 (open)
claims a proof in every `d`. Nonauthor review required. Scientific effect: NONE — no register, graph, STATUS,
PROOF_INDEX, prize or Boolean change; no numerical constant is certified. Same GitHub account as every lane; zero
organizational independence.

**Why.** Math- #229 (merged) proves
`ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} − ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{3/7})` ((R⁺.1)). Math- #240 (merged) proves that each
fixed cusp window `κ₀ ≤ ℓ/r⁴ ≤ κ₁` contributes a multiple of `ℓ^{1/4}` with error `O(ℓ^{3/4})`, and its Remark 1 leaves the
ends `κ → ∞` and `κ → 0` open. This note studies the end `κ → ∞` for the rejected pairs. Formally it is the only source of
the next term of `ρ_rej` (§4).

**What is new.**
- **Theorem 1** (§1). In every `d ≥ 2`, `κ𝒜^{rej}(b, κ, u) = F₀(b, u) + O(κ^{−1})` as `κ → ∞`, uniformly with Gaussian decay
  in `b`.
  - The constant is `F₀ = (5/24)π₀(u; v₀(b, 0))𝔇(b, u) > 0`. Here `𝔇` is the density at `0` of the smallest eigenvalue `λ₁`
    of `−A`, weighted by `γ₁⁶(λ₂⋯λ_m)²`, where `γ₁` is the component of `γ` along the soft eigenvector.
  - In `d = 2`, `𝔇 = p_A(0 | b)E[γ⁶]`.
  - The rejected weight sits on *soft* transverse curvatures. On Step 2's event it sits exactly on
    `λ₁ ∈ (3γ₁²/(72κ − f̃₄), 3γ₁²/(24κ − f̃₄)]`. For fixed jets this window is `[γ₁²/(24κ), γ₁²/(8κ)]` up to relative errors
    `O(1/κ)`. This is a weighted, asymptotic localization, not a pointwise one: the double-soft and large-jet events are
    handled separately (Step 1).
- **Corollary 1′** (Gaussian kernel). `∫∫F₀ db dσ = 25√3/(48π²) ≈ 0.09140` in `d = 2`, and `125√30/(192π³) ≈ 0.11501` in
  `d = 3`.
- **The fold-scale soft model** (§2). It is the same function as #170's typed cubic, in other coordinates (#243
  Proposition FL.7). At fixed `k = ℓ/r³` and `λ₁ = λ̃r/k`, the window field divided by `κ = k/r` tends to an
  explicit polynomial `G_k`, in which two more jets enter: `B = ∂_uA` and `C₃ = ∂_Θ³f`, taken along the soft direction.
  - **Lemma 2** decides the elder mark in `G_k` exactly by a one-dimensional scan, including a case in which the saddle is
    not on the ridge. For `β > 2` that case needs `χ > 0`. An exact witness is given.
  - **Lemma 3** gives an a priori elder region.
  - The typed weight is `(γ⁴/16)(φ^{−2} − (1 − 12kB/γ²)²)₊`.
  - **Proposition 2′** (`d ≥ 3`). The stiff transverse directions live at the scale `r^{3/2}` and decouple. The limit is
    `G_k` plus a negative definite quadratic form in them, with the same elder decision.
- **Proposition 4** (§3). For the Gaussian kernel in every `d ≥ 2` (through Proposition 2′ for `d ≥ 3`), the fold-scale
  rejection rate is `F(k; b) = F₀(b)H(k)`, with `H` independent of `b` and of `d`, and `H(k) = 1 + (12/25)k² + O(k³)`.
  - The elder edge moves to `φ_e = 1/3 + t/3 + 10t²/27 + O(t³)`, where `t = 12kB/γ²`.
  - The resulting `+312/25` nearly cancels the `−12` of the pin density `e^{−12k²}`.
- **Lemma 5 and Conjecture 7** (§4).
  - The two-scale composite density has the expansion `(I^{cand} − c₁)ℓ^{1/4} + R_{2/3}ℓ^{2/3} + O(ℓ^{3/4})`, with `R_{2/3}`
    given by `F` and `F₀`.
  - Conjecture 7 says that `ρ_rej + ν_eld^{far,r_0^*} − B_{d,L}` has the same expansion.
  - For the Gaussian kernel, numerically `R_{2/3} ≈ −0.049` in `d = 2` and `≈ −0.061` in `d = 3` (§5).
- **Evidence** (§5, exploration):
  - the tail of Theorem 1, by quadrature in `d = 2` and `d = 3`;
  - Lemma 2 against a two-dimensional flood fill;
  - `H`, by quadrature;
  - #216's Monte Carlo of the rejected adjacent pairs in `d = 2` and `d = 3`, binned by lifetime and by `s = r/ℓ^{1/4}`. It
    shows the predicted suppression at small `s`:

    | | observed (`s < 0.8`) | composite | cusp kernel alone |
    |---|---|---|---|
    | `d = 2` | 37 | 35.3 | 4,322 |
    | `d = 3` | 11 | 10.7 | 1,329 |

**Dependencies.**
- Consumed (all merged):
  - #220 (`frontiers/elder_third_order_20261001/PROOF.md`, blob `c8767dde`): §0 ((0.1), (0.2)) and §1 (window coordinates,
    (1.1), Lemma Q, (M1)–(M6)).
  - #218 (`frontiers/candidate_third_order_20261001/PROOF.md`, blob `70ca57ef`): §0 (`𝒜^{cand}`, `I^{cand}`, `B_{d,L}`).
  - #229 (`frontiers/third_order_rate_20261001/PROOF.md`, blob `110ed33a`): (R⁺.1) and §0 (`Y_r`).
  - #207 (`frontiers/cusp_second_order_20261001/PROOF.md`, blob `f6df5a73`): §§0, 4, 6; the parity factorization of
    [P] §15, as stated after (CU.2); Theorem CU.1, for the transverse pins; and Theorem CU.2(c).
  - [R] (`frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf`): (R5).
  - [P] §2, through #220.
- Cited only:
  - [C7-K] (`frontiers/c7_total_bounded_20260929/PROOF.md`, blob `28748b08`): (K2).
  - #240 (merged at `7636cae`, blob unchanged): Lemma Q′, Step N6, Corollary N′, Remarks 1 and 4.
  - #170 (`frontiers/local_elder_geometry_20260930/PROOF.md`, blob `ef2aa579`) and #175
    (`frontiers/concave_fibre_elder_20260930/PROOF.md`, blob `923d3236`), both merged: the failure law
    `r^{−3}(1 − p_r) → α₁ + α₂` (Theorems S and F), the compact-window coefficient, #170 §3 (the critical chord), and #170
    Theorem E. These are prior work for §§2–4; both packets are author-side candidates at their stated conditional scope.
  - #243 (open; its five review slices are at head `11a4cd4`): Theorem FL and Proposition FL.7 (Conjecture 6).
  - #244 (open, head `1781c0f`): the closed form of `I` (Theorem A), `t* = 2/3` (Corollary A.1) and the expansion of `H` to
    order `k⁴` (Theorem B), conditional on #170 Theorem E(1) and [CUB] Theorem C. §5's v1.3 numbers use it.
  - #237 (open): Theorem P, Remark 4.
  - #216 (open): the Monte Carlo in `d = 2, 3`.
  - #187 (merged) and #188 (open): the far elder density.

## 0. Setting

Setting and notation are those of #220 §0 and #218 §0 (through #207 §§0, 4, 6). Fix `d ≥ 2` and put `m := d − 1`.
- **The field and the pair.** The [P] field lives on `X = R^d/(LZ^d)`. The near pins are `M = −ru/2` and `S = ru/2`, at
  heights `b` and `b − kr³`. Put `κ = k/r`, so the lifetime is `ℓ = kr³ = κr⁴`; `Θ` ranges over `u^⊥`.
- **The jets** at `0`, under the contact law at `v₀(b, k)` (#220 §2; expectation `E_{v₀(b,k)}`, and `E₀[· | b]` at `k = 0`):
  - `A = D_Θ²f ∈ Sym(m)`, `f₄ = ∂_u⁴f` and `γ = ∇_Θ∂_u²f ∈ R^m`;
  - `Δ = det A` and `Y = (f₄/12)Δ − γᵀadj(A)γ/4`;
  - `φ = Y/(6κΔ) = (f₄ − 3γᵀA^{−1}γ)/(72κ)`.
- **The eigenframe.** On `{A < 0}` write `Λ := −A`. Its eigenvalues are `0 < λ₁ ≤ λ₂ ≤ ⋯ ≤ λ_m`, with an orthonormal
  eigenbasis `e₁, …, e_m`, and `γ_i := γ·e_i`. Then

      z := 72κφ = f₄ + 3Σ_i γ_i²/λ_i,    Y = (Δ/12)z,    Δ² = (λ₁⋯λ_m)²,    w_κ := 36κ²Δ² − Y² = 36κ²Δ²(1 − φ²).    (0.1)

  In `d = 2` (`m = 1`), `λ := λ₁ = −A` and `adj A = 1`, so `z = f₄ + 3γ²/λ` and `w_κ = (λ²/144)(5184κ² − z²)`.
- **The jets along a transverse direction.** For a unit vector `e ⊥ u` put `γ_e := ∂_u²∂_ef`, `B_e := ∂_u∂_e²f` and
  `C_e := ∂_e³f`. In `d = 2`, write `B := B_Θ = ∂_uA` and `C₃ := C_Θ = ∂_Θ³f`.
- **The cusp kernels** (#220 (0.1), #218 §0) are `𝒜^*(b, κ, u) = 12π₀(u; v₀(b, 0))E₀[w_κ1_* | b]`, with weight `w_κ`,
  `1_cand = 1{A < 0, |φ| < 1}` and `1_eld = 1{A < 0, |φ| < 1/3}`. So

      𝒜^{rej}(b, κ, u) := (𝒜^{cand} − 𝒜^{eld})(b, κ, u) = 12π₀(u; v₀(b, 0)) E₀[36κ²Δ²(1 − φ²) 1{A < 0, 1/3 ≤ |φ| < 1} | b].   (0.2)

  The contact terms cancel. So, by #220 (0.2) and #218 §0, `I^{cand} − c₁ = ∫_{S^{d−1}}∫_R∫_0^∞𝒜^{rej}(b, s^{−4}, u) ds db dσ(u)`.

**Two facts about the contact law.** The pin set splits into even pins `(f, ∂_u²f, ∇_Θ∂_uf)` and odd pins
`(∂_uf, ∂_u³f, ∇_Θf)`. Even-order and odd-order derivatives of a stationary field at a point are uncorrelated. The
nondegeneracy statements come from the finite-jet rank of [P] §2.
- (G1) Under `v₀(b, 0)`, `γ` is a centred Gaussian vector with nondegenerate covariance `Σ_γ(u)`, independent of `(A, f₄)`.
  In `d = 2`, `Σ_γ = σ_γ²`.
- (G2) Given `b`, `(A, f₄)` is a nondegenerate Gaussian vector on `Sym(m) × R` whose mean is affine in `b`.
  - `p(A, f₄ | b)` is its density with respect to Lebesgue measure on `Sym(m) × R`.
  - In `d = 2`, `p_A(a | b)` is the density of `A`, and `p_A(a | f₄, b)` its conditional density given `f₄`.

**The Gaussian kernel.** For `C(x) = e^{−|x|²/2}` on `R^d`, exact computations (controls S3 and S12) give the following.
1. *Odd jets.* Given `∇f(0) = 0`, and for every unit vector `e ⊥ u`, the jets `(∂_u³f, γ_e, B_e, C_e)` are independent, with
   variances `(6, 2, 2, 6)`, and uncorrelated with every even jet. Hence:
   - under `v₀(b, k)` the jets `(γ_e, B_e, C_e)` are centred and independent of `(A, f₄)`;
   - `γ ~ N(0, 2I_m)`;
   - the gap pin `∂_u³f = 12k` contributes the factor `e^{−144k²/(2·6)} = e^{−12k²}` to the pin density.
2. *Even jets.* Given the even pins `(f, ∂_u²f, ∇_Θ∂_uf) = (b, 0, 0)`:
   - `A = −bI_m + G`, where `G` has independent entries with `Var G_ii = 2` and `Var G_ij = 1` for `i ≠ j` (the Gaussian
     orthogonal ensemble);
   - `f₄ ~ N(−3b, 24)` is independent of `A`.

This is (0.3). The periodized kernel of the torus field agrees with `C` up to `O(e^{−L²/8})`. Statements labelled
*Gaussian kernel* are about the model case `C` on `R^d`, as in #207 §8.

## 1. The soft tail of the rejected cusp kernel

**Theorem 1.** Let `d ≥ 2`. The limit

    𝔇(b, u) := lim_{ε↓0} ε^{−1} E₀[γ₁⁶ (λ₂⋯λ_m)² 1{A < 0, λ₁ < ε} | b] ∈ (0, ∞)                                    (1.0a)

exists, and there are `C, c, N` such that for `κ ≥ 1`, `b ∈ R` and `u ∈ S^{d−1}`,

    |κ 𝒜^{rej}(b, κ, u) − F₀(b, u)| ≤ C κ^{−1} (1 + |b|)^N e^{−cb²},        F₀(b, u) := (5/24) π₀(u; v₀(b, 0)) 𝔇(b, u).        (1.0)

The empty product `λ₂⋯λ_m` equals `1` when `m = 1`.
- *Special forms of `𝔇`.*
  - By (G1), `E[γ₁⁶ | A] = 15(e₁ᵀΣ_γe₁)³`.
  - In `d = 2`, `𝔇 = p_A(0 | b)E[γ⁶]`, so `F₀ = (5/24)π₀p_A(0 | b)E[γ⁶]`.
  - If `Σ_γ = σ_γ²I_m`, then `𝔇 = 15σ_γ⁶𝔡`, where `𝔡` is the density at `0` of `λ₁`, weighted by `(λ₂⋯λ_m)²`.
- *Gaussian kernel* (`σ_γ² = 2`). `𝔇 = 120𝔡` and `F₀ = 25π₀𝔡`.

*Proof.* Fix `b` and `u`. The constants below are uniform in `u` and polynomial in `b` before the factor `π₀`, which carries
`e^{−c₀b²}` ([R] (R5)). For `m = 1` put `λ₁ := λ`. For `m ≥ 2`, matrices with a repeated eigenvalue form a null set. By Weyl's
integration formula, Lebesgue measure on the negative definite cone pulls back, under
`(λ, O) ↦ −O diag(λ)Oᵀ` (`0 < λ₁ < ⋯ < λ_m`, `O ∈ O(m)`, `e_i = Oε_i`), to `c_m V(λ) dλ dO` with
`V(λ) := Π_{i<j}(λ_j − λ_i)`. So, for measurable `g ≥ 0`,

    E₀[g 1{A < 0} | b] = c_m ∫∫∫ E_γ[g] ψ dλ dO df₄,        ψ := p(−O diag(λ)Oᵀ, f₄ | b) V(λ),                           (1.1a)

where `E_γ` integrates over `γ` by (G1). Write `x₀ := (−O diag(0, λ₂, …, λ_m)Oᵀ, f₄)`, `p₀ := p(x₀ | b)` and
`ψ₀ := ψ|_{λ₁=0}`, and let `μ(b)` be the mean of `(A, f₄)`, which is affine in `b`. For a Gaussian density,
`p(x + h) ≤ p(x)e^{C|h|(1 + |x − μ(b)|)}` and `|∇p(x)| ≤ C(1 + |x − μ(b)|)p(x)`, and `V` is a polynomial. So for
`0 ≤ λ₁ ≤ min(λ₂, 1)`

    |ψ − ψ₀| ≤ λ₁K,        K := C(1 + |x₀| + |b|)^{N₀} e^{C|x₀ − μ(b)|} p₀,                                                 (1.1b)

and `∫K ≤ C(1 + |b|)^N`, because a Gaussian density beats the exponential factor. For `m = 1` there is no `λ₂`: read
`min(λ₂, 1)` as `1`, and the conditions on `λ₂` below are void.

Put `f̃₄ := f₄ + 3Σ_{i≥2}γ_i²/λ_i` (so `f̃₄ = f₄` when `m = 1`). Then `z = 3γ₁²/λ₁ + f̃₄ ≥ f̃₄ ≥ f₄`.

*Step 1 (negative `z`, large `|f₄|`, double-soft pairs).*
- *Negative `z`.* `z ≤ −24κ` forces `f₄ ≤ −24κ`, and the weight is at most `36κ²Δ²`.
- *Large `|f₄|`.* On `{|f₄| ≥ κ/2}`, (G2) gives `E₀[Δ²1{|f₄| ≥ κ/2} | b] ≤ C(1 + |b|)^N e^{−c(κ − C|b|)₊²}`. Multiplied by `π₀`,
  this is `≤ C(1 + |b|)^N e^{−cb²}e^{−cκ²}` (if `|b| ≥ κ/(2C)`, use `e^{−c₀b²}`).
- *Double-soft pairs.* Let `δ > 0` and consider the event `{λ₁ < λ₂ ≤ δ}` (only for `m ≥ 2`).
  - There `w_κ ≤ 36κ²λ₁²λ₂²(λ₃⋯λ_m)²` and `V ≤ λ₂·Π_{j≥3}λ_j^{j−1}`. The density `p` is bounded and has Gaussian decay in
    `(λ₃, …, λ_m, f₄)`.
  - Hence `E₀[w_κ1{λ₁ < λ₂ ≤ δ} | b, γ] ≤ Cκ²∫_0^δ∫_0^{λ₂}λ₁²λ₂³ dλ₁dλ₂ ≤ Cκ²δ⁷`, polynomially in `b`.
  - There are two uses. First, if `|f₄| < κ/2` and `f̃₄ ≥ κ`, then `3|γ|²/λ₂ ≥ 3Σ_{i≥2}γ_i²/λ_i ≥ κ/2`, which forces
    `λ₂ ≤ δ := 6|γ|²/κ`.
    Second, the event of Step 2 with `λ₂ ≤ γ₁²/(7κ)` has `δ := γ₁²/(7κ)`.
  - In both cases `E_γ` of `κ·κ²δ⁷` is `O(κ^{−4})`.

All these parts are `O(κ^{−2})` after multiplying by `κ`.

*Step 2 (the soft window).* Work on `{|f̃₄| < κ, 24κ ≤ z < 72κ, λ₂ > γ₁²/(7κ), |γ|² ≤ κ}`. The complement of the last
condition costs `O(e^{−cκ})` by (G1), since the weight is at most `36κ²Δ²`.
- *The window.* `3γ₁²/λ₁ = z − f̃₄ ∈ (23κ, 73κ)`, so `λ₁ ∈ (3γ₁²/(72κ − f̃₄), 3γ₁²/(24κ − f̃₄)]`, and in particular
  `λ₁ < 3γ₁²/(23κ) < min(λ₂, 1)`.
- *The substitution.* Fix `(λ₂, …, λ_m, O, f₄, γ)`. Then `f̃₄` is fixed, and `λ₁ ↦ φ = (f̃₄ + 3γ₁²/λ₁)/(72κ)` is a decreasing
  bijection of the window onto `[1/3, 1)`, with `λ₁ = 3γ₁²/(72κφ − f̃₄)` and `|dλ₁/dφ| = 216κγ₁²/(72κφ − f̃₄)²`.
- *The integral.* Write `Π′ := (λ₂⋯λ_m)²`, so `Δ² = λ₁²Π′`. Then

      ∫ ψ 36κ²Δ²(1 − φ²) 1{…} dλ₁ = ∫_{1/3}^{1} ψ|_{λ₁=λ₁(φ)} · 69984 κ³ γ₁⁶ Π′ (1 − φ²)/(72κφ − f̃₄)⁴ dφ.           (1.1)

Since `69984/72⁴ = 1/384`, the factor `69984κ³/(72κφ − f̃₄)⁴` equals `(384κφ⁴)^{−1}(1 − f̃₄/(72κφ))^{−4}`, and
`|f̃₄/(72κφ)| ≤ 1/24` on this event. So

    |(1 − f̃₄/(72κφ))^{−4} − 1| ≤ C|f̃₄|/κ,        |ψ − ψ₀| ≤ λ₁K ≤ γ₁²K/(7κ)   (by (1.1b)).                         (1.2)

Hence (1.1) equals `(γ₁⁶Π′/(384κ))ψ₀∫_{1/3}^1(φ^{−4} − φ^{−2})dφ + κ^{−2}O((γ₁⁸ + γ₁⁶|f̃₄|)Π′(ψ₀ + K))`, and
`∫_{1/3}^1(φ^{−4} − φ^{−2})dφ = 20/3`.

*Step 3 (integration).* Integrate over `(λ₂, …, λ_m, O, f₄)` and `γ`, and restore the sets excluded in Step 2 at the costs of
Step 1.
- *The errors are finite.* `Π′|f̃₄| ≤ Π′|f₄| + 3Σ_{i≥2}γ_i²λ_iΠ_{j≥2, j≠i}λ_j²` is a polynomial: each `1/λ_i` is cancelled by
  `λ_i²`. So the error terms are finite, with Gaussian decay.
- *The excluded sets, for the main term.* The main-term integrand `(20/3)/(384κ)·E_γ[γ₁⁶]Π′ψ₀` must also be bounded on the
  sets excluded in Step 2.
  - Since `V(0, λ₂, …, λ_m) ≤ λ₂Π_{j≥3}λ_j^{j−1}`, we have `Π′ψ₀ ≤ Cλ₂³·poly(λ₃, …, λ_m)·p₀`. So on `{λ₂ ≤ δ}` the
    integrand integrates to `O(δ⁴/κ)`, which is `O(κ^{−5})` for both choices of `δ` in Step 1.
  - On `{|f₄| ≥ κ/2}` and `{|γ|² > κ}` the Gaussian tails of `p₀` and of `γ` apply. Since `f̃₄ ≥ f₄`, this covers
    `{|f̃₄| ≥ κ}`, as in Step 1.
- *The main term.* It is `(20/3)/(384κ)` times `c_m∫∫∫E_γ[γ₁⁶]Π′ψ₀ dλ₂⋯dλ_m dO df₄`. This equals `𝔇`: by (1.1a),
  `ε^{−1}E₀[γ₁⁶Π′1{A < 0, λ₁ < ε} | b]` is the average over `λ₁ ∈ [0, ε)` of the same integral with `ψ` in place of `ψ₀`,
  and (1.1b) with dominated convergence gives the limit. This also proves that the limit (1.0a) exists.
- *Positivity.* `𝔇 > 0` because `ψ₀ > 0` and `γ₁ ≠ 0` on sets of positive measure.

Multiplying by `12π₀` and by `κ` gives (1.0), since `12·(20/3)/384 = 5/24`. In `d = 2`, `ψ = p(−λ, f₄ | b)` and `𝔇 = p_A(0 | b)E[γ⁶]`
(by (G1)). ∎

*Remarks on Theorem 1.*
1. Theorem 1 is about the cusp kernel `𝒜^{rej}` itself, not about the non-uniformity of #240's Theorem N as `κ → ∞`.
   - The rejected weight sits on `λ₁ ∈ (3γ₁²/(72κ − f̃₄), 3γ₁²/(24κ − f̃₄)]` (Step 2), with the other eigenvalues of order
     one. For fixed jets this is `[γ₁²/(24κ), γ₁²/(8κ)]` with relative error `O(1/κ)`. The shorthand is a weighted
     asymptotic localization, not a uniform one over all jets.
     - *Example.* With `m = 1`, `f₄ = κ/2` and `γ = 1`, the upper endpoint is `48/47` times `γ²/(8κ)` for every `κ`.
     - Such growing-jet configurations are exponentially suppressed (OA-242-A-01). Those with `|f̃₄| ≥ κ` are Step 1's
       large-jet event, as are the double-soft ones. Those with `|f̃₄| < κ` (for example `f₄ = κ/4`, ratio `96/95`) are covered
       by the error term (1.2) of Step 2.

     So the rejected pairs at large `κ` are soft in exactly one transverse direction.
   - In #220's elder decision they are the pairs with `|φ| ∈ (1/3, 1)` coming from `3γ₁²/λ₁ ≈ z`, not from `f₄`.
2. In `d = 2`, expanding (1.2) to first order gives `κ𝒜^{rej}/F₀ = 1 + c(b)/κ + O(κ^{−2})`, with
   `c(b) = (12/5)[E(f₄ | A = 0, b)/18 − ∂_a log p_A(0 | b)·E[γ⁸]/(24E[γ⁶])]`. Here `12/5` is the mean of `1/φ` under the
   weight `φ^{−4} − φ^{−2}` on `[1/3, 1]`. For the Gaussian kernel, `A ~ N(−b, 2)` and `f₄ ~ N(−3b, 24)` are independent given
   `b`, and `c(b) = 0.3b`.
   In `d ≥ 3` the coefficient also involves the positive shift `f̃₄ − f₄ = 3Σ_{i≥2}γ_i²/λ_i` and the `λ₁`-derivative of the
   eigenvalue density, and it is not odd in `b`. For the Gaussian kernel in `d = 3`, numerically
   `κ(κ𝒜^{rej}/F₀ − 1) → −0.266` at `b = 0` and `+0.083` at `b = 1` (`perb3.py`, at `κ` up to `10⁴`).
3. With `s = κ^{−1/4}`, `∫_{S^{d−1}}𝒜^{rej}(b, s^{−4}, u) dσ(u) = (∫F₀ dσ)s⁴ + O(s⁸(1 + |b|)^N e^{−cb²})`. So the `s`-integral
   defining `I^{cand} − c₁` converges at `s = 0` like `s⁵`, and `s ≤ s₀` contributes `(∫∫F₀ db dσ)s₀⁵/5 + O(s₀⁹)`.
4. *Numerically* (Gaussian kernel; §5):
   - *`d = 2`.* `F₀(0) = 0.008207`, `F₀(1) = 0.003019` and `∫F₀ db = 0.0145472`, so `∫∫F₀ db dσ = 0.091403`.
     - `κ𝒜^{rej}(0, κ)/F₀(0) = 0.509, 0.751, 0.917, 0.977, 0.9985, 0.9999` at `κ = 1/2, 1, 2, 4, 16, 64`; here `c(0) = 0`.
     - `κ(κ𝒜^{rej}/F₀ − 1) = 0.280, 0.295` at `b = 1` and `−0.318, −0.305` at `b = −1`, at `κ = 16, 64`, as `c(±1) = ±0.3`
       predicts.
   - *`d = 3`*, integrated over `b` and `u`. `κ∫∫𝒜^{rej} db dσ / ∫∫F₀ db dσ = 0.6697, 0.9899, 0.99936, 0.99994` at
     `κ = 1, 10, 100, 1000`.
   - *`d = 3`*, per `b`. `κ𝒜^{rej}(b, κ)/F₀(b) = 0.99730, 0.99973, 0.999973` at `b = 0` and `1.00079, 1.000082, 1.0000083` at
     `b = 1`, at `κ = 10², 10³, 10⁴`.

**Corollary 1′ (Gaussian kernel).** Let `C(x) = e^{−|x|²/2}` on `R^d`.
- *`d = 2`.* `F₀(b) = 25π₀(b)p_A(0 | b)`, where `A ~ N(−b, 2)` given `b`, and

      ∫_{S¹}∫_R F₀ db dσ = 25√3/(48π²) ≈ 0.0914028.

- *`d = 3`.* Given `b`, the eigenvalues of `Λ = −A` are `λ_{1,2} = −t ∓ ρ`, with `t ~ N(−b, 1)` and `ρ ~ Rayleigh(1)`
  independent. Hence, with `ϕ` the standard normal density,

      𝔡(b) = ∫_0^∞ (2ρ)² ρe^{−ρ²/2} ϕ(ρ − b) dρ,    F₀ = 25π₀𝔡,    ∫_{S²}∫_R F₀ db dσ = 125√30/(192π³) ≈ 0.1150058.

*Proof.*
- *The law of `Λ`.* By (0.3), `A = −bI + G`. For `m = 2`, write `G = τI + G₀` with `G₀` traceless. Then
  `τ = (G₁₁ + G₂₂)/2 ~ N(0, 1)`, and `G₀` has the independent `N(0, 1)` coordinates `(G₁₁ − G₂₂)/2` and `G₁₂`. So the
  eigenvalues of `G₀` are `±ρ`, with `ρ ~ Rayleigh(1)` independent of `τ`, and `t := τ − b`. At `λ₁ = 0` we have `t = −ρ` and
  `λ₂ = 2ρ`. The density of `λ₁` at `0` given `ρ` is that of `t` at `−ρ`, namely `ϕ(ρ − b)`. This gives `𝔡`. With
  `E[γ₁⁶] = 15·2³ = 120`, it follows that `F₀ = (5/24)·120π₀𝔡`.
- *The integrals.* We use the parity factorization of #207 (stated after (CU.2)):
  `∫_R π₀(u; v₀(b, 0))E₀[g | b] db = p_G(0)p_{V_u}(0)(2π)^{−1/2}τ_u^{−1}E[g | V_u = 0, G = 0, t_u = 0]`, where `f(0)` is
  free in the law on the right.
  - For the Gaussian kernel the prefactor is `(2π)^{−d}/(6√π)`. Indeed `G ~ N(0, I_d)`; `V_u` has independent coordinates with
    variances `3` and `1` (`m` times); and `τ_u² = 6`.
  - Under the law on the right (control S12), `A ~ N(0, 8/3)` in `d = 2`. In `d = 3`, `t ~ N(0, 5/3)`, with the traceless part
    as before.
  - So `𝔡` integrates to `(16π/3)^{−1/2}` in `d = 2`. In `d = 3` it integrates to
    `∫_0^∞4ρ³e^{−ρ²/2}(10π/3)^{−1/2}e^{−3ρ²/10} dρ = (25/8)(10π/3)^{−1/2}`.
  - The factorization is applied to `𝔡`, which is an `ε`-limit. The exchange of `lim_ε` and `∫db` is justified by dominated
    convergence: by (1.1a)–(1.1b), `ε^{−1}E₀[Π′1{A < 0, λ₁ < ε} | b] ≤ C(1 + |b|)^N` uniformly in `ε ≤ 1`.
  - Multiplying by `25`, `|S^{d−1}|` and `(2π)^{−d}/(6√π)` gives the two values (control S12). ∎

In the cusp variable the integrated tail coefficient is thus larger in `d = 3` (`0.1150`) than in `d = 2` (`0.0914`). The
rejected coefficient itself is smaller: `I^{cand} − c₁ = 0.07244` against `0.09212` (#207 §8).

## 2. The fold-scale soft model

Theorem 1 shows where the rejected weight sits as `κ → ∞` along the cusp scale. The *fold scale* is the regime of fixed
`k = ℓ/r³` and `r → 0`, so again `κ = k/r → ∞`.
- *Where the rejected weight sits.* [C7-K] (K2) bounds the rejected weight by `O(r³/k)`, and [P]'s cap region shows that in
  weighted expectation the rejection comes from transverse curvatures of order `r`.
- *Weighted, not eventwise* (OA-242-B-02). This is a statement in weighted expectation, not an eventwise restriction over
  all derivative jets. An event of probability `r³` can have curvature of order one. For example, the exact cubic with
  `k = 1`, `λ̃ = 1/r`, `γ² = 12/r` and `B = C₃ = 0` has `φ = ½` and is rejected, with mixed jets growing like `r^{−1/2}`.
- *So the soft contribution is studied with `λ = (r/k)λ̃`,* and two more jets enter.

This section is formal for the field (the limit is Conjecture 6) and exact for the model. It is written for `d = 2`;
Proposition 2′ at its end reduces `d ≥ 3` to it.

*The limit window field.* In the window coordinates of #220 §1 (`Φ(X, Ξ) = rXu + r²ΞΘ`, `𝔉 = r^{−4}(f∘Φ − b)`), put `λ = λ̃/κ`
and `Ξ = κζ`, so that `x = rX` and `y = rkζ`. Every monomial `x^iy^j` of the Taylor expansion at `0` contributes
`r^{i+j−3}k^{j−1}X^iζ^j` to `𝔉/κ = (f(rX, rkζ) − b)/(kr³)`. After the pin corrections of #220 (1.1),

    𝔉(X, κζ)/κ = G_k(X, ζ) + r G₁(X, ζ) + O_k(r²(1 + |ζ|)⁵)    (|X| ≤ 3, rk|ζ| ≤ 1),
    G_k(X, ζ) := 2(X + ½)²(X − 1) + ½(X² − ¼)γζ − ½λ̃ζ² + ½kBXζ² + (k²/6)C₃ζ³,                                         (2.1)
    G₁ = (f₄/(24k))(X² − ¼)² + (k/4)∂_u²∂_Θ²f·X²ζ² + (k²/6)∂_u∂_Θ³f·Xζ³ + (k³/24)∂_Θ⁴f·ζ⁴ + (1/6)∂_u³∂_Θf·X(X² − ¼)ζ.

Control S10 checks (2.1), including `G₁`, on exactly pinned polynomial fields. The pins are exact: `G_k(−½, 0) = 0`,
`G_k(½, 0) = −1`, and `∇G_k = 0` at both.
- *The remainder is quantified* by OpenAI Codex's root-authored estimate (B.5) in its review 5391485205. For
  `f ∈ C⁵([−1, 1]²)` with the pins, `M := max_{i+j=5}sup|∂_x^i∂_y^jf|`, `0 < r ≤ 1/3`, `|X| ≤ 3` and `rk|ζ| ≤ 1`,
  the `O_k` term of (2.1) is at most `M r²[17203/(7680k) + (1303/384)|ζ| + (9k/4)ζ² + (3k²/4)|ζ|³ + (k³/8)ζ⁴ + (k⁴/120)|ζ|⁵]`.
  This is a deterministic value estimate. It is uniform for `k` in compacts of `(0, ∞)` and bounded `M`.
- Such constants do not by themselves dominate a Gaussian integral over unbounded jets.

*Normalization.* For `γ > 0` set `ζ = (γ/λ̃)z` and

    φ := γ²/(24λ̃),    t := 12kB/γ²,    β := kB/λ̃ = 2tφ,    χ₀ := 576k²C₃/γ³,    χ := χ₀φ².                          (2.2)

(For `γ < 0`, replace `(γ, C₃, ζ)` by `(−γ, −C₃, −ζ)`.) Then `G_k = (γ²/λ̃) G` with

    G(X, z) = A₀(X) + ½(X² − ¼)z − ½(1 − βX)z² + (χ/6)z³,    A₀(X) := 2(X + ½)²(X − 1)/(24φ),                    (2.3)

with `M = (−½, 0)` at level `0` and `S = (½, 0)` at level `L_S := −1/(24φ)`. At `t = χ₀ = 0`, the ridge of (2.3) is the cusp
ridge `g/(24φκ)` of #220 §1 with `f₄ = 0`, and `φ` is #220's `φ` in the limit `κ → ∞` (Theorem 1, Step 2).

*Typing and weight.* The Hessians of `G_k` at the pins have determinants `6λ̃ + Y` (at `M`) and `−6λ̃ + Y` (at `S`), with
`Y := 3kB − γ²/4`; this is `Y_r = Y′ + 3kΔ_B` of #229 §0 in the limit. So `M` is a nondegenerate maximum and `S` a saddle iff
`|Y| < 6λ̃`, that is

    0 < φ < 1/|c′|,    c′ := 1 − t.                                                                                    (2.4)

The scaled Kac–Rice weight is `36λ̃² − Y² = (γ⁴/16)(φ^{−2} − c′²)`. Since `dλ̃/dφ = −γ²/(24φ²)`, with the absolute Jacobian
`|dλ̃/dφ| = γ²/(24φ²)` (OA-242-B-03), the weight per unit `φ` is `(γ⁶/384)φ^{−2}(φ^{−2} − c′²)`. At `t = 1` (`c′ = 0`), (2.4)
reads `φ > 0`, with upper endpoint `∞`. By (2.4), `1 + β/2 − φ = 1 − φc′ > 0`, so the `z`-curvature `−(1 + β/2)` at `M` is negative.

*Slices.* For fixed `X`, `z ↦ G(X, z)` is a polynomial of degree at most three. Write `p := X² − ¼`, `a := 1 − βX` and
`D := a² − χp`. Call `X` *open* if the slice has no local maximum (`χ = 0` and `a ≤ 0`, or `χ ≠ 0` and `D ≤ 0`). Otherwise
`R(X)` is the value at the local maximum and `V(X)` the value at the local minimum (`V := −∞` if `χ = 0`). For `χ ≠ 0` the
critical points are `z_r = (a − √D)/χ` (maximum) and `z_v = (a + √D)/χ` (minimum); for `χ = 0`, `z_r = p/(2a)`. At a critical
point `z_*`, `G = A₀ + (p/3)z_* − (a/6)z_*²`.

**Lemma 2 (the elder decision in the model).** Let `(φ, β, χ)` satisfy (2.4) with `β ≠ 2`. Let `I_M` be the connected component
of `{X not open: R(X) > L_S}` containing `−½`. Suppose that `M` is the only critical point of `G` at level `0`, that `S` is the only one at level `L_S`, and that `R` has no
finite limit along an unbounded `I_M`. This excludes a null set of parameters.
Then `S` kills `M` in the superlevel filtration of `G` (the elder rule) iff one of the following holds.

- (D) `1 − β/2 > 0`, the right end of `I_M` is `½`, its left end `X_L` is finite, and on `(X_L, ½)` we have `V < L_S` and `R < 0`
  for `X ≠ −½`.
- (D′) `1 − β/2 < 0` and `χ > 0`, `½ ∈ I_M`, `I_M = (X_L, X_R)` is bounded, and on `I_M` we have `R < 0` for `X ≠ −½` and
  `V < L_S` for `X ≠ ½`.

If `1 − β/2 < 0` and `χ ≤ 0`, then `S` does not kill `M`. Below, `e := 1{S kills M}`.

*Proof.* Fix a level `c`. On a non-open slice, `{z : G(X, z) > c}` has a bounded *ridge piece* around `z_r` when `R(X) > c`.
When `χ ≠ 0` it also has an unbounded *far piece* beyond `z_v`, and the two are one interval iff `V(X) > c`. On an open slice
the set is unbounded (one or two half-lines, or `R`), and `G → +∞` along it, as along every far piece. The argument works at
the exact level `L_S` (OA-242-B-01), following OpenAI Codex's review of v1.1 (5948352439).
1. *The exact level.* Let `U` be the component of `{G > L_S}` containing `M`.
   - *The axial segment.* `{(X, 0) : −½ ≤ X ≤ 2}` carries `G = A₀`, with `A₀ − L_S = (X − ½)²(X + 1)/(12φ) ≥ 0` (equality only
     at `S`). It ends at `A₀(2) = 25/(48φ) > 0`. This is the critical-chord bound of #170 §3. So the death level of `M` is
     `≥ L_S`, and `(−½, ½) × {0} ⊂ U`.
   - *If `U` contains a point above `0`,* a path in `U` reaches it, because `U` is open and connected. By compactness the
     path has minimum `> L_S`, so `M` dies above `L_S`, and `e = 0`.
   - *Otherwise* every path from `M` to a point above `0` leaves `U`, so the death level is exactly `L_S`. Since `S` is the
     only critical point at that level, `S` kills `M`: `e = 1`.
2. *When `U` reaches above `0`.* `U` contains the ridge tube over `I_M`. It contains a point above `0` in each of three cases:
   - `R > 0` somewhere on `I_M`;
   - `V > L_S` somewhere on `I_M` (a far piece joins, along which `G → +∞`);
   - `I_M` is unbounded. `R` is an algebraic function of `X`, so it has a limit in `[−∞, ∞]` along `I_M`. A finite limit is
     excluded by hypothesis, and `−∞` contradicts `R > L_S`.

   *An open end of `I_M` reduces to these cases.*
   - If `χ ≠ 0`, then as `X` tends to an open end inside `I_M`, `R` and `V` tend to the common inflection value, which is
     `≥ L_S` because `R > L_S` on `I_M`.
     - If that value exceeds `L_S`, then `V > L_S` nearby (the second case).
     - If it equals `L_S`, then either `V > L_S` nearby, or the inflection point is a critical point at level `L_S` other
       than `S`. It is not `S`, because `D(½) = a(½)² > 0` when `β ≠ 2`.
   - If `χ = 0`, an open end is a zero of `a`, where `R → +∞` (the first case).

   If none of the three cases holds, then `I_M` is bounded with non-open ends, `U` is the ridge tube over `I_M`, and
   `sup_U G = 0`, attained at `M`. Here the equality cases are excluded by the hypotheses:
   - a ridge value `0` at some `X ≠ −½`, with `R ≤ 0` nearby, would be a critical point at level `0`;
   - a valley value `L_S`, with `V ≤ L_S` nearby, would be a critical point at level `L_S`, hence `S`.

   So `e = 1` iff `I_M` is bounded, `R < 0` on `I_M ∖ {−½}`, and `V < L_S` on `I_M` except at `S`. In particular its ends are
   then non-open.
3. *A slice fact.* Let `|X| < ½` and `a(X) > 0`, with a non-open slice.
   - If `χ > 0`, then `D = a² + χ|p| > a²`, so `z_r < 0 < z_v`.
   - If `χ < 0`, then `z_v < z_r < 0`.
   - If `χ = 0`, then `z_r = p/(2a) < 0`.

   In every case the slice decreases strictly from `z_r` to `0` (between `z_r` and `z_v`, or beyond `z_r` away from `z_v`), so
   `R(X) > G(X, 0) = A₀(X) > L_S`.
4. *`1 − β/2 > 0`.* On (2.4), `β > −2`, so `a > 0` on `[−½, ½]`. By Step 3, the first open slice to the right of `−½`, if it
   lies in `(−½, ½)`, is an open end of `I_M`, and then `e = 0` by Step 2. Otherwise `(−½, ½) ⊂ I_M`.
   - At `X = ½`, where `p = 0`, the slice has its local maximum at `z = 0`, with value `L_S`. So `S` is the ridge point there,
     and the right end of `I_M` is `½`.
   - Inside `(X_L, ½)` a point with `V = L_S` would be a critical point at level `L_S` other than `S`.

   With Step 2 this is (D).
5. *`1 − β/2 < 0`.* Now `a(½) < 0`, and `a` vanishes at `X = 1/β ∈ (0, ½)`.
   - *`χ = 0`.* `R = A₀ + p²/(8a) → +∞` as `X ↑ 1/β`, while `R ≥ G(X, 0) = A₀ > L_S` on `(−½, 1/β)`. So `R > 0` somewhere
     on `I_M`, and `e = 0`.
   - *`χ < 0`.* At `X = 1/β`, `D = −χp < 0`, so that slice is open. By Step 3, the first open slice in `(−½, 1/β]` is an open
     end of `I_M`, and `e = 0` by Step 2.
   - *`χ > 0`.* For `|X| < ½`, `D > a² ≥ 0` and `z_r < 0 < z_v` whatever the sign of `a`, so `R > A₀ > L_S` on `(−½, ½)`.
     - At `X = ½` the slice has its local minimum at `z = 0` (value `L_S`) and its local maximum at `z = 2a(½)/χ` (value
       `L_S + (2/3)|a(½)|³/χ² > L_S`). So `[−½, ½] ⊂ I_M`, and `S` is the valley point at `X = ½`.
     - `V` has a strict local maximum `L_S` there, because the Schur complement of `∂_z²G(S) > 0` in the indefinite Hessian
       is negative.

     With Step 2 this is (D′). ∎

#243's Lemma FL.2(c) gives the same case analysis. Off #170's null sets `Σ_k ∪ Δ_k`, #170 Theorem E(1) and #243
Proposition FL.7(iii) let the decision be read off the critical values: `e = 0` iff `G` has a critical point with value in
`(L_S, 0)`.

Case (D′) is not empty.
- *An exact witness,* found by OpenAI Codex (5946792240) (control S14):

      G_{(3/2, 8/3, 20/3)}(X, z) = (1/9)·G_{(1/6, 0, 0)}(X + 2z, 3z).

  - The right side has concave slices and `φ = 1/6 < 1/3`, so `R = (X + ½)²(X² + 3X − 15/4)/8` and
    `R − L_S = (X − ½)²(X² + 5X + 17/4)/8`. It satisfies (D), with `I_M = ((−5 + 2√2)/2, ½)`, because the convex quadratic
    `X² + 3X − 15/4` is negative on `[−2, ½]`.
  - The linear map fixes `M` and `S`, and a positive factor preserves elder decisions. So the witness, which has `β = 8/3 > 2`
    and `χ = 20/3 > 0`, is elder: case (D′).
  - It has exactly three critical points, with values `0`, `L_S = −1/36` and `−125/384`. In its own coordinates
    `I_M ≈ (−1.50494, 0.51622)`.
- *A numerical example* (control S8): `(φ, β, χ) = (0.2401, 2.1425, 0.5536)` is elder, with `I_M ≈ (−1.032, 0.515)`.

The margins vanish quadratically at the special points `X = −½` (for `R`) and `X = ½` (for `V`), as the lemma requires. A
flood fill of `{G > L_S ± ε}` on a grid agrees with Lemma 2 at 900 random typed parameter points, once one near-degenerate
point is rechecked with a smaller `ε` (§5).

Let `𝓡(t, χ₀) ⊂ (0, 1/|1 − t|)` be the set of `φ` that are rejected at `(φ, 2tφ, χ₀φ²)`, and set

    I(t, χ₀) := ∫_{𝓡(t, χ₀)} φ^{−2}(φ^{−2} − (1 − t)²) dφ.                                                              (2.5)

**Lemma 3 (an a priori elder region).** If `φ ≤ (1/20)·min(1, |t|^{−1}, |χ₀|^{−2/3})`, read with `0^{−1} = ∞`, the configuration
is elder. Hence `I(t, χ₀) ≤ (8000/3)·max(1, |t|³, χ₀²)`.

*Proof.* Then `φ ≤ 1/20`, `|β| ≤ 1/10` and `|χ| ≤ 1/400`, with `χ² ≤ φ/8000`. We check (D) of Lemma 2 with `X_L ∈ (−2, −½)`.
- *Critical values.* On `[−2, ½]`, `a ∈ [0.8, 1.2]`, `|p| ≤ 15/4` and `|χp| ≤ 1/100`. So `D > 0`, and `s := √D` satisfies
  `s/a ∈ [0.99, 1.01]`. Exactly, `R − A₀ = p²(a + 2s)/(6(a + s)²)` and `V − A₀ = (a + s)²(a − 2s)/(6χ²)`. Hence
  `R − A₀ ≤ 0.128p²/a` and `V − A₀ ≤ −0.33/χ²`.
- *Middle.* On `(−½, ½)`, `z = 0` lies on the descending side of the local maximum, so `R(X) ≥ G(X, 0) = A₀(X) > L_S`. Also
  `1 − β/2 > 0`. So the right end of `I_M` is `½`.
- *Left dip.* At `X = −2`, `R − A₀ ≤ 0.128·(225/16)/0.8 < 2.3`, while `A₀(−2) = 13.5L_S`. Since `12.5/(24φ) > 2.3`,
  `R(−2) < L_S`. Hence `X_L > −2`.
- *No trigger on `(X_L, ½)`.* On `[−2, −½)`, `R ≤ (X + ½)²[2(X − 1)/(24φ) + 0.128(X − ½)²/a] < 0`, since
  `2(X − 1)/(24φ) ≤ −1/(8φ) ≤ −5/2` and `0.128(X − ½)²/a ≤ 1`. On `(−½, ½)` the bracket is at most `−1/(24φ) + 0.135 < 0`.
  And `V ≤ A₀ − 0.33/χ² < L_S`, since `A₀ ≤ 0` on `[−2, ½]` and `χ² ≤ φ/8000`.
Finally `φ^{−2}(φ^{−2} − c′²) ≤ φ^{−4}`, so `I ≤ ∫_{φ_*}^∞ φ^{−4} dφ = φ_*^{−3}/3`. ∎

The constants of Lemma 3 are crude. Numerically:
- the elder edge `φ_e(t, χ₀)` satisfies `φ_e|t| → 1/2` as `t → −∞`, and `φ_e|χ₀|^{2/3} → 16^{1/3}` as `|χ₀| → ∞`. In the second
  case the valley at `M`, `V(−½) = −(2/3)/χ²`, reaches `L_S` when `χ² = 16φ`;
- for `t ≥ t*`, with `t* ∈ (0.65, 0.68)`, the elder edge at `χ₀ = 0` is `β = 2`, that is `φ_e = 1/t`;
- correspondingly `I(t, 0) = (2 − t)(2t − 1)²/3` on `[t*, 1]`, `I(t, 0) = t − 2/3` for `t ≥ 1`, `I(t, 0) ~ (4/3)|t|³` as
  `t → −∞`, and `I(0, χ₀) ~ χ₀²/48`.

*The stiff directions (`d ≥ 3`).* Let `m ≥ 2`, and work in the eigenframe of `A` at `0`. There `A = −diag(λ₁, …, λ_m)`, with
soft direction `e₁`, `λ₁ = λ̃r/k`, and stiff eigenvalues `λ₂, …, λ_m` fixed. Put `x = rX` and
`y = rkζe₁ + r^{3/2}Σ_{i≥2}η_ie_i`. Let `G_k` be (2.1) with the jets along `e₁`: `γ = γ_{e₁}`, `B = B_{e₁}`, `C₃ = C_{e₁}`.

**Proposition 2′.** On `{|X| ≤ 3, |ζ| + |η| ≤ R}`,

    (f(rXu + y) − b)/(kr³) = G_k(X, ζ) − (1/(2k))Σ_{i≥2}λ_iη_i² + r^{1/2}G_{1/2}(X, ζ, η) + O_{k,R}(r),
    G_{1/2} := Σ_{i≥2} [(γ_{e_i}/(2k))(X² − ¼) + (∂_u∂_{e₁}∂_{e_i}f) Xζ + (k/2)(∂_{e₁}²∂_{e_i}f) ζ²] η_i.                (2.6)

The limit `G_k^{(d)} := G_k(X, ζ) − (1/(2k))Σ_{i≥2}λ_iη_i²` has the elder decision of `G_k`:
- (a) the critical points of `G_k^{(d)}` are those of `G_k` with `η = 0`, at the same levels, with `m − 1` additional negative
  Hessian eigenvalues `−λ_i/k`. So `M` is a nondegenerate maximum, and `S` a nondegenerate critical point of index `m`,
  exactly when (2.4) holds;
- (b) for every level `c`, the projection `(X, ζ, η) ↦ (X, ζ)` maps the connected components of `{G_k^{(d)} > c}`
  bijectively onto those of `{G_k > c}`, and the supremum of a component equals that of its image;
- (c) hence `S` kills `M` for `G_k^{(d)}` iff it does for `G_k`, and Lemma 2 decides the elder mark. In the original
  units, the Hessians of the window field at the pins are block diagonal up to `O(r)`, with stiff block
  `−diag(λ₂, …, λ_m)`. So the typed weight gains the factor `(λ₂⋯λ_m)²`, as in Theorem 1's `Π′`.

*Proof.* The monomial `x^i y₁^j Π_{i′≥2} y_{i′}^{l_{i′}}` of the Taylor expansion at `0` contributes `r^{i+j+3|l|/2−3}k^{j−1}`
times a monomial in `(X, ζ, η)`. Exponents below `1` occur only for three groups:
- the monomials of (2.1) (`|l| = 0`, `i + j ≤ 3`);
- the stiff quadratic (`|l| = 2`, `i = j = 0`, exponent `0`);
- `|l| = 1` with `i + j ≤ 2` (exponent `i + j − 3/2`). Within this group:
  - `y₁y_{i′}` (exponent `−1/2`) has coefficient `∂_{e₁}∂_{e_{i′}}f(0) = 0` in the eigenframe;
  - `y_{i′}` (exponent `−3/2`) and `xy_{i′}` (exponent `−1/2`) have the pinned coefficients
    `∂_{e_{i′}}f(0) = −(r²/8)γ_{e_{i′}} + O(r⁴)` and `∂_u∂_{e_{i′}}f(0) = O(r²)` (the transverse pins, as in #207 Theorem
    CU.1). They contribute `−(γ_{e_{i′}}/(8k))r^{1/2}η_{i′}` and `O(r^{3/2})`;
  - `x²y_{i′}`, `xy₁y_{i′}` and `y₁²y_{i′}` have exponent `1/2` and give `G_{1/2}`.

The other monomials, and the Taylor remainder, are `O(r)` on the window. This proves (2.6).
- For (a), `∇_ηG_k^{(d)} = −(λ_iη_i/k)_i` vanishes only at `η = 0`.
- For (b), the fiber of `{G_k^{(d)} > c}` over `(X, ζ)` is the open ellipsoid `{Σλ_iη_i² < 2k(G_k(X, ζ) − c)}`, which is
  nonempty iff `G_k(X, ζ) > c`. The projection is continuous and open, its fibers are connected, and its image is
  `{G_k > c}`, so it induces a bijection of components. The supremum over a fiber is attained at `η = 0`.
- (c) follows from (a) and (b), and from the block form of the Hessians. In physical coordinates the pin Hessian is
  `[[rS + O(r²), rC + O(r²)], [rCᵀ + O(r²), D + O(r)]]` with `D = −diag(λ₂, …, λ_m)` fixed and invertible. Its Schur
  complement is `rS + O(r²)`, so `det = r²det(D)det(S) + O(r³)`, as OpenAI Codex's Slice B review (§3) spells out. This is not
  uniform as a second transverse eigenvalue tends to `0`. ∎

Control S13 checks (2.6), including `G_{1/2}`, on exactly pinned degree-6 fields in `d = 3`, at `r = 10^{−6}` and `10^{−8}`
(so that `r^{1/2}` is rational). Like (2.1) and #207 Theorem CU.1, (2.6) is a deterministic Taylor statement for every `C⁵`
field with these pins. What is formal is the use of the limit model's elder decision for the field (Conjecture 6).

*Consistency with Theorem 1.* Maximize the `γ`-part of `r^{1/2}G_{1/2}` over `η_i` against the stiff quadratic
`−λ_iη_i²/(2k)`. The maximum is at `η_i = r^{1/2}γ_{e_i}(X² − ¼)/(2λ_i)`, and its value is
`rγ_{e_i}²(X² − ¼)²/(8kλ_i) = r(3γ_{e_i}²/λ_i)(X² − ¼)²/(24k)`. Added to the term `r(f₄/(24k))(X² − ¼)²` of `G₁`, it turns `f₄`
into `f̃₄ = f₄ + 3Σ_{i≥2}γ_{e_i}²/λ_i`. This is the fold-scale image of Step 2 of Theorem 1.

## 3. The fold-scale rejection function

Formally, at fixed `k` the rejected kernel is the expectation of the rejected weight of §2 over the jets.
- With `λ₁ = λ̃r/k`, the law of `λ₁` near `0` contributes its density at `0` times `(r/k)dλ̃`.
- The stiff directions contribute the weight factor `(λ₂⋯λ_m)²` (Proposition 2′(c)).
- The contact pin density at gap `k` is `π₀(u; v₀(b, k))`.

This motivates

    F(k; b, u) := 12 π₀(u; v₀(b, k)) lim_{ε↓0} ε^{−1} E_{v₀(b,k)}[(γ₁⁶/384)(λ₂⋯λ_m)² I(12kB₁/γ₁², 576k²C₁/γ₁³) 1{A < 0, λ₁ < ε}],   (3.1)

with `(γ₁, B₁, C₁) := (γ_{e₁}, B_{e₁}, C_{e₁})` and the expectation under the contact law at `v₀(b, k)`. In `d = 2` this is
`12π₀(u; v₀(b, k))p_A(0 | b, k)E_{v₀(b,k)}[(γ⁶/384)I(12kB/γ², 576k²C₃/γ³) | A = 0]`. Formally,
`r^{−2}A_r^{rej}(b, k, u) = (r/k)F(k; b, u) + o(r)` (Conjecture 6 below). Formally, as `k → 0`, `I → I(0, 0) = 20/3`, and
(3.1) tends to the `F₀` of Theorem 1. For the Gaussian kernel this is proved by Proposition 4 (`H → 1`).

*Prior work (AUTH-242-01; not cited in v1.1).* Here `A_r^{rej} := A_r(1 − p_r)`, with `A_r` the candidate kernel of [P]
§§10–11 and `A∗ := lim A_r` ([P] (10.3), where it is written `A_0`). The merged packets #170 (`d = 2`, Theorem S) and #175
(fixed `d ≥ 3`, Theorem F) are author-side candidates at their stated conditional scope. They prove that `r^{−3}(1 − p_r)`
converges at fixed marks. The limit is `a_fail = α₁ + α₂`, a Gaussian integral over the window-saddle classifier of #170's
typed cubic.
- So the fold-scale limit of `(k/r)r^{−2}A_r^{rej} = kA_r·r^{−3}(1 − p_r)` exists, and equals `kA∗a_fail`. Their §§9 and 7
  also give the compact-window `ℓ^{2/3}` coefficient `C_fail`.
- #242's `G_k` is #170's cubic `P_θ(X, kζ)/k` at `θ = (−λ̃/k, γ, B, C₃)`, with the same typed domain, weight and maximin
  decision (#243 Proposition FL.7).
  - *In `d = 2`,* (3.1) equals `kA∗a_fail` by a model-level computation (#243 Proposition FL.7(iv)). With #170 Theorem S
    this gives Conjecture 6 at each fixed `(b, k, u)`, conditional on #170's interfaces.
  - *In `d ≥ 3`* the identity uses #243's Theorem FL (open) and uniqueness of limits.
- The remaining content of Conjecture 6 is local uniformity in `k`, and the `d ≥ 3` case. #243 claims both, by a partly
  different route.

**Proposition 4 (Gaussian kernel).** Let `C(x) = e^{−|x|²/2}` on `R^d`, `d ≥ 2`. Then:
1. `F(k; b) = F₀(b)H(k)`, where `H(k) := e^{−12k²}E[γ⁶I(t, χ₀)]/(E[γ⁶]·20/3)` depends on neither `b` nor `d`. Here
   `(γ, B, C₃)` are independent `N(0, 2)`, `N(0, 2)` and `N(0, 6)`, and `(t, χ₀) = (12kB/γ², 576k²C₃/γ³)`.
2. `H(k) = 1 + (12/25)k² + O(k³)` as `k → 0`.
3. `H(k) ≤ C(1 + k⁴)e^{−12k²}`; in particular `|H(k) − 1| ≤ C min(1, k²)`.

*Proof.* (1) By (0.3), the gap pin contributes `e^{−12k²}`, so `π₀(v₀(b, k)) = π₀(v₀(b, 0))e^{−12k²}`. This is the factor
`e^{−a′k²}`, `a′ = 12`, of #240 Step N6.
- The law of the even jets does not depend on `k`. So `p_A(0 | b, k) = p_A(0 | b)`, and in general the weighted density of
  `λ₁` at `0` is the `𝔡(b)` of Theorem 1.
- The law of `(γ, B, C₃)` is as stated, centred and independent of `(A, f₄, b)`.
- In `d ≥ 3` the soft direction `e₁` is a function of `A`. By (0.3) the odd jets are independent of `A`, and for every
  fixed unit `e ⊥ u` the triple `(γ_e, B_e, C_e)` has the stated law. So `(γ₁, B₁, C₁)` has that law and is independent of
  `(A, f₄)`.

Hence the expectation in (3.1) factorizes as `𝔡(b)` times the soft-jet average, and `F = F₀H` with the same `H` in every `d`.

(2) *The edge at `χ₀ = 0`.* For `χ = 0` and `a > 0` the ridge is `R = A₀ + p²/(8a)`. At `t = 0` it is
`[2(X + ½)²(X − 1) + 3φ(X² − ¼)²]/(24φ)`, and

    R − L_S = (X − ½)²[2(X + 1) + 3φ(X + ½)²]/(24φ)      (t = 0),                                                    (3.2)

whose bracket has discriminant `4 − 12φ` in `X + ½`. At `φ = 1/3`, (3.2) is `((X − ½)(X + 3/2))²/(24φ)`, with a nondegenerate
double zero at `X = −3/2`. The elder edge solves `R(X) = L_S`, `R′(X) = 0` in `(X, φ)` at `β = 2tφ`. Equivalently it solves
`N = N_X = 0` for the rescaled `N := 24φa(R − L_S)`.
- The Jacobian of `(N, N_X)` in `(X, φ)` at `(−3/2, 1/3, t = 0)` is `−96 ≠ 0`. For the literal system `(R − L_S, R′)` it is
  `−3/2`, and for `Q := N/(X − ½)²` it is `−6` (OA-242-C-02).
- So the implicit function theorem gives analytic `X_e(t)` and `φ_e(t)`. Their series (control S4) are

    X_e(t) = −3/2 − t/3 − t²/3 + O(t³),    φ_e(t) = 1/3 + t/3 + (10/27)t² + O(t³).                                    (3.3)

*The rejected set near `(0, 0)`.* For `|t| ≤ t₀` and `|χ₀| ≤ δ₀` (small constants),
`𝓡(t, χ₀) = (φ_e(t, χ₀), 1/|1 − t|)`, where `φ_e(t, χ₀)` is the same tangency for the ridge of the cubic slices.
- *Elder side.* For `φ_* ≤ φ < φ_e`, Lemma 2's condition (D) involves only `X ∈ [X_L, ½] ⊂ [−2, ½]`. At `t = χ₀ = 0` it holds
  with strict margins for `φ ≤ 1/3 − δ`; this is the exact cusp-ridge decision of #207 Theorem CU.2(c) and #220 (M1)–(M6).
  Strict inequalities on a compact set persist for small `|t|, |χ₀|`. Near the edge, the implicit function theorem applies.
  Lemma 3 covers `φ < φ_*`.
- *Rejected side.* For `φ ∈ [1/3 + δ, 2]` at `t = χ₀ = 0`, the bracket in (3.2) is positive, so `R − L_S ≥ c(δ) > 0` on `[−3, −½)`.
  Also `R(−3) > 0`, since `24φR(−3) = −50 + (3675/16)φ > 0`. Again these are strict inequalities on a compact set. On it
  `a ∈ [1 − 3|β|, 1 + 3|β|]` and `D > 0` for small `|t|` and `|χ₀|`. So the left part of `I_M` reaches a point with `R > 0` before
  closing, and `e = 0`, up to the typed edge `1/|1 − t| ≤ 2`.
- *`χ₀`-direction.* For `|χ₀| ≤ δ₀`, the valley satisfies `V ≤ L_S − c/χ²` on `[−3, ½]`, as in Lemma 3, so it never triggers. The
  tangency `φ_e(t, χ₀)` is smooth in `(t, χ₀)`, and so is `I`.

With `∫_a^bφ^{−2}(φ^{−2} − c′²)dφ = (a^{−3} − b^{−3})/3 − c′²(a^{−1} − b^{−1})` and `b = 1/c′`,

    I(t, 0) = φ_e^{−3}/3 − (1 − t)²/φ_e + (2/3)(1 − t)³ = 20/3 − 20t + (52/3)t² + O(t³).                                (3.4)

*Averaging.* Split the expectation on `𝒢 := {|t| ≤ t₀, |χ₀| ≤ δ₀}`.
- On `𝒢`, Taylor's formula gives `I = 20/3 − 20t + ∂_{χ₀}I(0, 0)χ₀ + (52/3)t² + O(|t|³ + |t||χ₀| + χ₀²)`. The linear terms have mean
  zero: `B` and `C₃` are symmetric and independent of `γ`, and `𝒢` is symmetric in each.
- The moments are finite: `γ⁶t² = 144k²B²γ²`, `γ⁶|t|³ = 1728|k|³|B|³`, `γ⁶|t||χ₀| = 6912|k|³|B||C₃||γ|` and
  `γ⁶χ₀² = 331776k⁴C₃²`. Moreover `E[γ⁶t²] = 576k²`.
- Off `𝒢`, Lemma 3 bounds `γ⁶I` by `C(γ⁶ + k³|B|³ + k⁴C₃²)`. For `k ≤ 1`, `𝒢^c` forces `γ² ≤ ε := Ck(|B| + |C₃|^{2/3})`, and
  `E[γ^{2j}1{γ² ≤ ε} | B, C₃] ≤ Cε^{j+1/2}`. So `𝒢^c` costs `O(k^{7/2})`, and so does the mean of `γ⁶t² = 144k²B²γ²` over `𝒢^c`.
Hence

    E[γ⁶I(t, χ₀)] = 120·(20/3) + (52/3)·576k² + O(k³),    H(k) = e^{−12k²}(1 + (312/25)k²) + O(k³) = 1 + (12/25)k² + O(k³).

The divergence of `E[γ⁶t⁴]` does not by itself show a term of order `k^{7/2}` (OA-242-C-01).
- OpenAI Codex's Slice C review (5390667993, §5) proves the sharper upper remainder `H(k) = 1 + (12/25)k² + O(k^{7/2})`, by
  sign averaging and a truncated inverse moment. That support is Codex's own and is not reviewed here.
- No nonzero `k^{7/2}` coefficient is claimed.

(3) Lemma 3 gives `γ⁶I ≤ C(γ⁶ + 1728k³|B|³ + 331776k⁴C₃²)`. ∎

So for the Gaussian kernel the rejected-pair rate at the fold scale starts at its cusp-scale value `F₀`, in every
dimension.
- The pin density lowers it by `12k²`, and the motion of the elder edge raises it by `(312/25)k²`. The two nearly cancel,
  and `12/25` remains.
- Numerically, `H₀ − 1` (with `C₃` ignored) already changes sign near `k ≈ 0.08`.

For another stationary kernel with `B` and `γ` independent of each other and of `∂_u³f` under the contact law, the two
coefficients are `−144/(2σ₃²)` and `(1872/75)σ_B²/σ_γ⁴`, with `σ₃² := Var(∂_u³f | ∇f(0) = 0)`. For the Gaussian kernel,
`σ_B² = σ_γ² = 2` and `σ₃² = 6`.

## 4. The composite density and the conjectured `ℓ^{2/3}` term

Theorem 1 describes the cusp kernel's tail as `κ → ∞`: `κ𝒜^{rej} → F₀`. At the fold scale the leading term of the same
rejected kernel is, by Conjecture 6, `(r/k)F(k; b, u)`. Its existence is #170/#175's failure law, and its identification
with (3.1) is discussed after (3.1). That the two limits agree in the overlap, `F(k)/F₀ → 1` as `k → 0`, is a further statement about (3.1). It needs (3.1)
plus domination, and for the Gaussian kernel Proposition 4 proves it (`H → 1`). Theorem 1 alone does not give it
(OA-242-D-01). Put `H(k; b, u) := F(k; b, u)/F₀(b, u)`; for the Gaussian kernel this is the `H(k)` of Proposition 4. The
simplest density built from both limits is the *composite*

    ν^c(ℓ) := ∫_0^∞∫_R∫_{S^{d−1}} 𝒜^{rej}(b, ℓ/r⁴, u) H(ℓ/r³; b, u) dσ(u) db dr.                                       (4.1)

**Lemma 5 (expansion of the composite).** Let `H ≥ 0` be measurable with `|H(k; b, u) − 1| ≤ C_H min(1, k²)` uniformly
(Proposition 4(3) for the Gaussian kernel). Then, as `ℓ ↓ 0`,

    ν^c(ℓ) = (I^{cand} − c₁) ℓ^{1/4} + R_{2/3} ℓ^{2/3} + O(ℓ^{3/4}),
    R_{2/3} := ∫_{S^{d−1}}∫_R∫_0^∞ v⁴[F(v^{−3}; b, u) − F₀(b, u)] dv db dσ(u),    F := F₀H.                            (4.2)

For the Gaussian kernel, `R_{2/3} = (∫∫F₀ db dσ)·Ĩ`, with `Ĩ := ∫_0^∞ v⁴[H(v^{−3}) − 1] dv` the same in every `d`, and
`∫∫F₀ db dσ` given by Corollary 1′.

*Proof.* The inner integral converges: its integrand is `O(v⁴)` at `0` and `O(v^{−2})` at `∞`, with Gaussian decay in `b`.
Write `H = 1 + (H − 1)`. The term with `1` is `ℓ^{1/4}(I^{cand} − c₁)` after `r = sℓ^{1/4}` (§0). For the term with `H − 1`, let
`P(b) := (1 + |b|)^N e^{−cb²}`.
- *`r > ℓ^{1/4}` (`κ < 1`).* `0 ≤ 𝒜^{rej} ≤ 𝒜^{con} ≤ Cκ²P(b)` and `|H − 1| ≤ Cℓ²r^{−6}`, so this part is
  `≤ Cℓ⁴∫_{ℓ^{1/4}}^∞ r^{−14} dr = O(ℓ^{3/4})`.
- *`r ≤ ℓ^{1/4}` (`κ ≥ 1`).* By Theorem 1, `𝒜^{rej} = F₀r⁴/ℓ + O(P(b)r⁸/ℓ²)`. With `r = vℓ^{1/3}`, the main part is
  `ℓ^{2/3}∫_0^{ℓ^{−1/12}}v⁴(F(v^{−3}) − F₀)dv`, which equals `ℓ^{2/3}` times the full `v`-integral up to `O(ℓ^{1/12})`. The
  error is `≤ CP(b)ℓ∫_0^{ℓ^{−1/12}}v⁸min(1, v^{−6})dv = O(P(b)ℓ^{3/4})`.
Integrating over `b` and `u` gives (4.2). ∎

**Conjecture 6 (the fold-scale limit).** In every `d ≥ 2`, with `F` as in (3.1), for every `k > 0`, `b` and `u`,
`lim_{r↓0} (k/r)·r^{−2}A_r^{rej}(b, k, u) = F(k; b, u)`, locally uniformly in `k`.

*Status (v1.2).*
- *Existence of the limit, as `kA∗(α₁ + α₂)`.* This is in #170 (`d = 2`) and #175 (`d ≥ 3`): merged author-side candidates,
  at their conditional scope.
- *`d = 2`, at fixed `(b, k, u)`.* This follows from #170 Theorem S and #243 Proposition FL.7(iv), a model-level identity.
- *Local uniformity in `k`, and `d ≥ 3`.* #243 (open; author-side) claims a proof (Theorem FL). Its five nonauthor slice
  reviews (same account, organizational independence 0) are delivered at head `11a4cd4`, with four minor clarifications
  to apply.
- The label is kept here until #243 lands.

**Conjecture 7 (the next term of the rejected density).** In every `d ≥ 2`,

    ρ_rej(ℓ) + ν_eld^{far,r_0^*}(ℓ) = B_{d,L} + (I^{cand} − c₁) ℓ^{1/4} + R_{2/3} ℓ^{2/3} + O(ℓ^{3/4}),                       (4.3)

with `R_{2/3}` as in (4.2).
- Equivalently, `ρ_rej + ν_eld^{far,r_0^*} − B_{d,L} − ν^c = O(ℓ^{3/4})`. This is (R⁺.1) of #229 with its remainder resolved.
- If `ν_eld^{far,r_0^*}(ℓ) = O(ℓ^{3/4})` (#188, open, claims `O(ℓ^N)`), then
  `ρ_rej = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + R_{2/3}ℓ^{2/3} + O(ℓ^{3/4})`.
- For the Gaussian kernel, numerically `R_{2/3} ≈ −0.049` in `d = 2` and `R_{2/3} ≈ −0.061` in `d = 3` (§5).

*What a proof needs.* Inputs (i) and (ii) are missing; (iii) is needed only to drop the far term.
- (i) *The soft layer.* A two-scale version of Conjecture 6, uniform from the cusp scale to the fold scale (`κ ≥ κ₁`), with
  errors integrating to `O(ℓ^{3/4})`. In fixed cusp windows this is #240's Theorem N (`O(r²)`). The new part is the window
  field's elder decision in the soft scaling `λ ≍ r`: Lemma 2 with margins for the field, as #240 Lemma Q′ gives them with
  `ε̃` for `λ ≍ 1`. In `d ≥ 3` it also needs Proposition 2′ for the field, uniformly in the stiff eigenvalues.
- (ii) *The end `κ → 0`.* On the intermediate separations `ℓ^{1/4} ≪ r ≤ r_0^*`, the rejected kernel must match `B_{d,L}`'s part
  plus the composite's own part, up to errors integrating to `O(ℓ^{3/4})`. (The composite is not negligible there:
  `𝒜^{rej} ≍ κ³` as `κ → 0`, so `r ≥ Sℓ^{1/4}` contributes about `ℓ^{1/4}S^{−11}`.) The best available bounds on these
  separations are #229's `O(ℓ^{4/9}log(1/ℓ))` (elder) and #237's `O(ℓ^{3/5})` (candidate), both larger than `ℓ^{2/3}`.
- (iii) *The far elder density.* #187 (merged) gives `ν_eld^{far,r_0^*}(ℓ) ≤ Cℓ^{2/3}`, which is the same order as the
  conjectured term. Conjecture 7 is stated with `ν_eld^{far,r_0^*}` on the left for that reason; #188's `O(ℓ^N)` would remove
  it.

Formally, a matched-asymptotics count gives cusp-side powers `ℓ^{(j+1)/4}` and fold-side powers `ℓ^{(j+1)/3}`
(`j = 0, 1, 2, …`). In `ρ_rej` the
fold-scale kernel is `O(r³/k)` ([C7-K] (K2)), with leading coefficient `F` (formally, Conjecture 6; existence by #170/#175). This
makes `ℓ^{2/3}` the first fold-side power and `ℓ^{3/4}` the next cusp-side one (#240 Corollary N′).

*Remarks.*
1. `ν_cand` has no term from this mechanism. In `ν_eld = ν_cand − ρ_rej` the soft layer contributes `−R_{2/3}ℓ^{2/3}`, in
   addition to any `ℓ^{2/3}` term of `ν_cand`: the typed boundary `λ ≍ r` also produces an `|r|³` term in the candidate kernel.
   #237's remainder `ℓ^{3/5}` allows both. Only `ρ_rej`, or the rejected Monte Carlo row binned in `s`, tests `R_{2/3}` alone,
   and only subject to (ii)–(iii).
2. For the Gaussian kernel, `Ĩ` is dominated by `v ∈ [1, 1.5]`, that is `k ∈ [0.3, 1]`, where `H` falls from `≈ 1` to `≈ 0`. The
   contributions are `−0.200` (`v < 1`), `−0.563` (`1 ≤ v ≤ 1.5`), `+0.003` (`1.5 ≤ v ≤ 2`) and `+0.227` (`v ≥ 2`) (v1.3,
   by `itilde_split.py` of §5's v1.3 custody item; v1.2 had `+0.223` for `v ≥ 2`).
3. `R_{2/3}/(I^{cand} − c₁) ≈ −0.53` in `d = 2` and `≈ −0.85` in `d = 3`. Since `ℓ^{5/12} = 0.147` at `ℓ = 10^{−2}`, the
   `ℓ^{2/3}` term there is about 8% (`d = 2`) and 12% (`d = 3`) of the `ℓ^{1/4}` term.

## 5. Numerical evidence (exploration; not part of the proofs)

Gaussian kernel `e^{−|z|²/2}`, `d = 2` unless stated otherwise.
- *Status.* The numbers below are author-reported exploration, not independently reproduced (OA-242-E-01).
- *Where the scripts are.* They are in the project archive `V2_2/frontiers_soft_rejected_pairs_20261002/exploration/`
  (numpy, scipy, mpmath, sympy); none is part of the repository.
- *Pinned identities.* `SOURCES.json` (`exploration_manifest`) pins every script, table and log there by its SHA-256,
  including those of the Monte Carlo comparison. #216's raw records are pinned by name in #216's archive
  `SIDE24_MC_raw_2026-10-01.zip`.
- *v1.3.* The scripts and logs behind the corrected values are in `exploration/v13/` of the same archive, pinned in
  `SOURCES.json` (`exploration_manifest`, `v13_files`). They evaluate #244's closed form; #244's own exploration is
  pinned in its `SOURCES.json`.

1. *Theorem 1.*
   - *`d = 2`.* Quadrature of (0.2) under the contact law (`fastk.py`, `soft_d2.py`) gives the numbers of Remark 4 of §1.
     The `b`-integrated tail is `κ∫𝒜^{rej}(b, κ) db → 0.0145472 = ∫F₀ db`. Also `∫∫𝒜^{rej}(b, s^{−4}) ds db = 0.014662`,
     and its `2π` multiple is `I^{cand} − c₁ = 0.092124`.
   - *`d = 3`.* Two quadratures compute `G(κ) := ∫∫𝒜^{rej} db dσ` under the `b`-integrated law of Corollary 1′'s proof.
     - `Gd.py` integrates `f₄` in closed form and `λ₁` on a logarithmic grid, for `κ ≤ 25`. It reproduces the `d = 2`
       profile of `fastk.py` to `10^{−7}`.
     - `Gphi.py` uses the substitution of Step 2, for `κ ≥ 5`.
     - On the overlap the two agree to `2·10^{−5}`.
   - *`d = 3` results.* `κG(κ) = 0.115005` at `κ = 10⁴`, against Corollary 1′'s `0.1150058`.
     - `∫_0^∞G(s^{−4})ds = 0.072444` on a grid refined near the sharp maximum of `G` at `κ ≈ 0.41` (step `0.025` in `log s`;
       `G3_merged_fine.log`). This matches `I^{cand} − c₁ = 0.0724443` (#207 §8, #216) to `10^{−6}`.
     - A plain Monte Carlo at `κ = 1` agrees: `0.07707 ± 0.00020`, against `0.07702`.
2. *Lemma 2.* The one-dimensional decision (`dec1d.py`) was compared with a flood fill of `{G > L_S ± ε}` on an `(X, z)` grid
   (`model2d.py`, `validate_D2.py`).
   - 600 parameter points drawn as in the computation of `H`: no disagreement.
   - 300 points with `β > 2`: one disagreement. There the valley exceeds `L_S` by `2·10^{−4}`, below the flood fill's
     default `ε`; with `ε_rel = 5·10^{−4}` the flood fill agrees.
   - The referee's independent comparison (500 points, 40 of them (D′)-elder) agrees after resolving two numerical
     artifacts.
   - *Two artifacts of `dec1d.py` (v1.3, AUTH-242-02).* Both are in thin layers on either side of `β = 2`. They are errors
     of the implementation, not of Lemma 2, and the comparison with the closed form of #244 found them.
     - *Just above `β = 2`, false rejections.* Here `a(½) = 1 − β/2 < 0`. The slices just right of `X = ½` lose their
       maximum at a fold, at distance `≈ a(½)²/χ` from `½`, which can be far below the grid step. `dec1d.py` treats a first
       grid point past `½` whose slice has no maximum as an open end. But if the fold value `A₀ + a³/(6χ²)` is below `L_S`,
       the band closes before the fold, and `S` is the death saddle. Example: at `(t, χ₀) = (9.005434, 193.926947)`,
       `dec1d.py` rejects `φ ∈ (0.11104, 0.12491)`, and the rejected set is `(0.11245, 0.12491)`.
     - *Just below `β = 2`, with `χ < 0`, false acceptances.* The tolerance `δ = 10^{−3}` of `dec1d.py` treats a band that
       ends within `10^{−3}` of `X = ½` as ending at `S`. But the slices just left of `X = ½` open (at distance
       `≈ a(½)²/|χ|`), and the axial segment joins `M` to the far region above `L_S`, so the pair is rejected.
     - The flood fill errs the other way here: its level offset `ε` exceeds the relevant level gaps. So the comparisons
       above did not expose the artifacts.
     - At the 15 values of `k` in v1.2's table (`k = 0.1, 0.15, …, 0.6` and `0.7, 0.8, 0.9, 1.0`), v1.2's `H` differs from
       the recomputed `H` of item 4 by at most `2.0·10^{−4}`, at `k = 0.4`. This is the largest observed difference at
       those points, not a certified uniform bound on the artifacts' effect, and it also contains v1.2's quadrature and
       table-interpolation errors (OA-242-V13-01).
     - Items 4–5 give the corrected values. Control S8 stays clear of this region (§7).
3. *The function `I`.*
   - A `101 × 121` table of `I(t, χ₀)` on `|t| ≤ 30`, `|χ₀| ≤ 2000` (`Itab2d_v2.py`), and an exact evaluator for other points
     (`Ifast.py`).
   - `I(t, 0)/|t|³ = 1.95, 1.51, 1.39` at `t = −10², −10³, −10⁴`, tending to `4/3`.
   - `I(0, χ₀)/χ₀² = 0.0228, 0.0212, 0.0209` at `χ₀ = 10³, 10⁴, 10⁵`, tending to `1/48`.
   - *The closed form (v1.3).* #244 (open) derives `I` exactly, conditional on #170 Theorem E(1) and [CUB] Theorem C,
     through #243 Proposition FL.7's identification. With `ψ = 1/φ` and `c′ = 1 − t`, off a null set the pair is elder iff
     `ψ ≥ 2c′` and `(χ₀ + 8 − 12t)² ≤ 16(ψ − 2c′)²(ψ + c′)`. So `I = |c′|δ² + δ³/3`, where `δ = ψ_e − |c′|` and `ψ_e` is the
     largest root of that cubic.
     - The table above agrees with it to a median relative difference of `1.8·10^{−7}`. The 97 of its 12,221 entries that
       differ by more than `10^{−3}` are explained: 7 tiny intervals the grid misses, 54 table resolution, and 36 the
       artifacts of item 2.
     - In particular `t* = 2/3` exactly (§2 has `t* ∈ (0.65, 0.68)`), and the two limits above have the exact next terms
       `I(t, 0) = (4/3)|t|³ + 3√3|t|^{5/2} + O(t²)` as `t → −∞` and
       `I(0, χ₀) = χ₀²/48 + 16^{−2/3}|χ₀|^{4/3} + O(|χ₀|)` as `|χ₀| → ∞` (OA-242-V13-02). For `t ≥ 1`, instead,
       `I(t, 0) = t − 2/3` exactly (#244 Corollary A.1). At `t = 0`, Theorem A's formula depends on `χ₀` only through
       `(χ₀ + 8)²`, so the second expansion holds in both directions.
4. *The function `H`.* `H = H₀ + Δ_χ`.
   - `H₀`, the value with `C₃` ignored, comes from a 639-point table of `I(t, 0)` on `|t| ≤ 400`, its asymptotic forms beyond
     (`|t|³(4/3 + 5.74|t|^{−1/2})` and `t − 2/3`), and adaptive quadrature in `t` and `γ²` down to `γ → 0` (`Hk0b.py`). Its
     small-`k` values reproduce `(H₀ − 1)/k² → 12/25`, and it agrees with the referee's independent `H₀` to `3·10^{−5}`.
   - `Δ_χ` is the difference of two direct quadratures over `(|γ|, B, C₃)`, with and without `C₃` (`Hdirect4.py`). These use
     32 Gauss–Legendre nodes in `|γ|` on `[0, 7.5]` and 24 Gauss–Hermite nodes in `B` and in `C₃`, with the table inside its
     range and the exact evaluator outside it.
   - Accuracy checks (v1.2): without the table, `Δ_χ(0.2)` changes by `2·10^{−5}`; with 48 nodes in `|γ|`, `H` changes by
     `5·10^{−5}`; and the quadrature `H` agrees with a table-free direct quadrature at `k = 0.2` to `1.3·10^{−4}`. All three
     checks use `dec1d.py`, so none of them measures its bias (item 2). Against the recomputed values, v1.2's `H` is off
     by up to `2.0·10^{−4}` at the tabulated `k` (at `k = 0.4`; an observed difference, item 2).
   - *Recomputed values (v1.3).* The rows below come from #244's closed form of `I`. `H` and `H₀` are evaluated by nested
     Gauss–Legendre quadrature over `(|γ|, B, C₃)`, split at the kinks of the integrand. Raising the node counts from `60³`
     to `100³` changes them by less than `10^{−10}`, and #244's referee reproduces the `H` row with an independent
     quadrature.
     - At the 15 values of `k` in v1.2's table, the v1.2 values differ from these by at most `2.0·10^{−4}` (`H`, at
       `k = 0.4`) and about `1.33·10^{−5}` (`H₀`, at `k = 0.35`). These are observed differences, not certified bounds.
     - At four decimals the v1.2 rows had `H = 1.0039, 0.9345, 0.7271, 0.4397, 0.2007` at `k = 0.1, 0.3, 0.4, 0.5, 0.6`
       and `H₀ = 0.4663` at `k = 0.4`.
   - *Small `k`.* `Δ_χ/k⁴ → 53248/800 = 66.56` (#244 Theorem B, Step 3); v1.2 used the fitted value `62`. #244 Theorem B
     also gives `H = 1 + (12/25)k² + h_{7/2}k^{7/2} + (728/25)k⁴ + o(k⁴)`, with
     `h_{7/2} = 16Γ(9/4)(1728√6 − 4332√2 − 2721)/(2625π) ≈ −10.144`. So the upper remainder `O(k^{7/2})` from Codex's
     Slice C review, cited in the proof of Proposition 4(2), is attained (OA-242-C-01). This packet itself still claims no
     `k^{7/2}` coefficient.
   - Values (v1.3):

     | `k` | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 1.0 |
     |---|---|---|---|---|---|---|---|---|---|
     | `H₀` | 0.9976 | 0.9334 | 0.7403 | 0.4662 | 0.2268 | 0.0845 | 0.0241 | 0.0053 | 0.0001 |
     | `H` | 1.0040 | 1.0041 | 0.9344 | 0.7269 | 0.4395 | 0.2006 | 0.0687 | 0.0177 | 0.0005 |
     | `e^{−12k²}` | 0.887 | 0.619 | 0.340 | 0.147 | 0.050 | 0.013 | 0.003 | 0.0005 | 0.000006 |

5. *`R_{2/3}`.*
   - *v1.3.* With `H` from #244's closed form, `Ĩ = −0.5336676`. The quadrature is Gauss–Legendre in `q = k^{1/3}` on
     `[0.1, 1.2]`, with #244 Theorem B's expansion below `q = 0.1` and `H = 0` above `q = 1.2`, where `H < 2·10^{−13}`. With
     16 and 24 nodes per segment the results agree to `2.5·10^{−8}`.
     - So `R_{2/3} = 0.0914028·Ĩ = −0.04878` in `d = 2` and `R_{2/3} = 0.1150058·Ĩ = −0.06137` in `d = 3`. Both lie inside
       the sensitivity ranges below, which stand.
     - *Why v1.2 differed.* Its `Ĩ` (`−0.5361` on the dense grid, `−0.5364` by `assemble2.py`) was off by about
       `−0.0025`. By the decomposition in #244 §5, about `−0.0019` comes from v1.2's interpolation of `Δ_χ` between the
       nodes `k = 0.1, 0.15, 0.2`, and about `−0.0008` from its small-`k` model `62k⁴`. Only about `+0.0002` comes from the
       artifacts of item 2 (`k = 0.25–0.7`).
   - *The v1.2 computation, kept as a record.*
     - `Ĩ = −0.536` (`assemble2.py`).
     - The 200-point grid `H_dense3.json` is written by `dense2.py --write`. It has the same values of `H` as v1's
       `H_dense2.json`, and its `R23` field comes from the quadrature of its interpolant, `Ĩ = −0.5361`.
     - The check mode of `dense2.py` (`dense2.log`) shows trapezoid and Simpson rules on the same grid giving `−0.535` to
       `−0.536`.
     - v1 quoted `−0.537` for "a dense trapezoid rule". That was the `R23` field stored in `H_dense2.json`, produced by an
       unrecorded rule (finding A-1, found by the author while archiving v1).
     - So v1.2 had `R_{2/3} = 0.0914028·Ĩ = −0.049` in `d = 2` and `R_{2/3} = 0.1150058·Ĩ = −0.0617` in `d = 3`.
   - *Sensitivity (v1.2; the ranges stand).* A uniform shift of `H` by `±0.002` on `k ≥ 0.1` (that is, `v ≤ 10^{1/3}`)
     moves `Ĩ` by exactly `±0.002·∫_0^{10^{1/3}}v⁴dv = ±0.002·10^{5/3}/5 ≈ ±0.0186` (v1.2 printed `±0.018`;
     OA-242-V13-03). Halving
     v1.2's small-`k` term `62k⁴` moves it by `−0.021`, and multiplying it by `1.5` by `+0.021`. So `Ĩ = −0.54 ± 0.03`,
     `R_{2/3} = −0.049 ± 0.003` in `d = 2` and `R_{2/3} = −0.062 ± 0.004` in `d = 3`.
   - *Comparisons.* With `C₃` ignored (`H = H₀`), `Ĩ = −1.134` and `R_{2/3} = −0.104` (v1.3; v1.2 had `Ĩ = −1.133`). With
     the pin density alone (`H = e^{−12k²}`), `Ĩ = 12^{5/6}Γ(−5/6)/6 = −8.829` and `R_{2/3} = −0.807`. So the soft model's
     extra jets matter: `B` nearly cancels the pin density at small `k`, and `C₃` raises `H` at `k ≈ 0.2–0.7`.
6. *#216's Monte Carlo.* The raw records were compared with the composite: `composite.py` and `comp2d.py` in `d = 2`, and
   `compd.py` in `d = 3`. The records are `batchA2.npz` (`d = 2`: 4,000 samples, 271,272 rejected adjacent pairs with
   `ℓ < 0.3`) and `batch3B.npz` (`d = 3`: 996 samples, 45,952 such pairs).
   - *#216's domains.* The fields are periodized on the torus of side `L = 64` (`d = 2`) and `L = 16` (`d = 3`). The
     comparison with the composite of the `R^d` Gaussian kernel is exploratory, not a certified transfer.
   - *What the row counts.* #216's row counts *adjacent* rejected pairs, which carry no `B_{d,L}` (#218 Remark 3).
   - *Uncertainties (OA-242-E-02).* They are descriptive.
     - Each `±` on a ratio is the Poisson relative error `1/√n` of the observed count.
     - "`+4.8σ`" is the Pearson residual `(651 − 540)/√540`.
     - The `χ²` values are Pearson sums over the bins with at least five counts, a selection that depends on the data.
     - Pairs from one field realization can be correlated, so none of these is a calibrated significance. By §4 (inputs (ii)–(iii), and the `ℓ^{3/4}` order), these totals do not test the global
   `ℓ^{2/3}` coefficient. What they do test, bin by bin in `s = r/ℓ^{1/4}`, is the fold-side suppression described by `H`.
   - *Small `s` (the fold side).* For `s < 0.8` and `ℓ ∈ [10^{−4}, 0.1)`, 37 pairs are observed, 35.3 predicted by the
     composite, and 4,322 by the cusp kernel alone. In the bin `ℓ ∈ [3·10^{−3}, 10^{−2})`, `s ∈ [0.6, 0.8)` the three numbers
     are 12, 13.1 and 143. For `s ∈ [0.8, 1)` they are 2,248, 1,904 and 7,766.
   - *`s ≥ 1` (the cusp side).* The composite and the cusp kernel agree. The data exceed both by up to 25% at `ℓ ≥ 10^{−2}`,
     which is not modelled here (finite-`r` cusp corrections, the `ℓ^{3/4}` order).
   - *Totals.* On `[10^{−4}, 10^{−2}]` the ratio of the counts to `(I^{cand} − c₁)ℓ^{1/4}` alone is `0.959 ± 0.017`; to the
     composite, `1.040`; to the two-term law with `R_{2/3} = −0.049`, `1.018`.
   - *`d = 3`, small `s`.* For `s < 0.8` and `ℓ ∈ [10^{−4}, 0.1)`, 11 pairs are observed, 10.7 predicted by the composite,
     and 1,329 by the cusp kernel alone. For `s ∈ [0.8, 1)` the three numbers are 651, 540 and 2,240 (`comp3d_final4.log`).
   - *The test discriminates `H`.* With the pin density alone in place of `H` (`H = e^{−12k²}`), the predictions would be 1.2
     (`s < 0.8`) and 82.7 (`s ∈ [0.8, 1)`) (`comp3d_pin.log`).
   - *The transition bin `s ∈ [0.8, 1)`.* The data exceed the composite. In `d = 3` the Pearson residual is `+4.8`
     (descriptive; see above), and in `d = 2` the counts are 2,248 against 1,904. In both dimensions the excess is concentrated at `ℓ ≥ 3·10^{−2}`, where the data exceed the composite anyway.
   - *`d = 3` totals.* The script keeps bins with at least five counts, so the effective ranges are `[3.1·10^{−4}, 9.7·10^{−3}]`
     (8 bins) and `[3.1·10^{−4}, 2.3·10^{−2}]` (10 bins). In `d = 2` the first range is `[1.3·10^{−4}, 9.7·10^{−3}]` (10 bins).

     | `d = 3` range | `(I^{cand} − c₁)ℓ^{1/4}` alone | composite | two-term law, `R_{2/3} = −0.0617` | χ²: `ℓ^{1/4}` alone / composite |
     |---|---|---|---|---|
     | `[3.1·10^{−4}, 9.7·10^{−3}]` | `0.884 ± 0.040` | `1.008` | `0.975` | 11.8 / 2.1 (8 bins) |
     | `[3.1·10^{−4}, 2.3·10^{−2}]` | `0.858 ± 0.024` | `1.032` | `0.989` | 44.9 / 5.1 (10 bins) |
   - *Over #216's whole range* `[10^{−4}, 0.3]` the composite does not describe the counts: data/composite rises to `1.63`
     near `ℓ ≈ 0.25`. This is the region of finite-`r` cusp corrections and the `ℓ^{3/4}` order, as in `d = 2`. In particular,
     #216's three-parameter fit of the `ℓ^{1/4}` coefficient on that range, `0.069 ± 0.006`, lies only `0.55σ` below
     `0.0724`, so it is not evidence of a deficit either way.

## 6. Scope and relation to other packets

- **#229 (R⁺.1).** It proves `ρ_rej = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} − ν_eld^{far,r_0^*} + O(ℓ^{3/7})`. Conjecture 7 would resolve
  its remainder in every `d ≥ 2`, given inputs (i)–(ii) of §4 (and (iii) to drop the far term). Theorem 1, Lemma 5 and
  Proposition 4 do not change any statement of #229.
- **#240 Remark 1.** It leaves the ends `κ → ∞` and `κ → 0` of Theorem N open. Theorem 1 describes the `κ → ∞` end of the
  *rejected* cusp kernel in every `d ≥ 2`: it decays like `1/κ`, while `𝒜^{cand}` and `𝒜^{eld}` grow like `κ²`. Lemma Q′'s margins do
  not reach the soft window `λ ≍ γ²/κ` where the rejected weight sits.
- **#237 Remark 4 and #240 Remark 4.** They found residuals of #216's Monte Carlo about the three-term laws that two-power
  fits could not attribute (`ℓ^{1/2}` against `ℓ^{2/3} + ℓ^{3/4}`). Conjecture 7 predicts a contribution `−R_{2/3}ℓ^{2/3}` to
  `ν_eld`, in addition to any `ℓ^{2/3}` term of `ν_cand`, with a coefficient computed independently of the Monte Carlo.
- **[C7-K] (K2)** bounds the fold-scale rejected weight by `O(r³/k)`. Formally (Conjecture 6) the bound is attained: the
  leading term of `r^{−2}A_r^{rej}` is `(r/k)F(k; b, u)`. That leading term exists by #170/#175. For the Gaussian kernel,
  `F(k) → F₀ ≠ 0` as `k → 0` (Proposition 4).
- **#170 and #175 (merged author-side candidates, at their stated conditional scope).** They prove the fold-scale failure
  law `r^{−3}(1 − p_r) → α₁ + α₂` and the compact-window `ℓ^{2/3}` coefficient (AUTH-242-01). #170 Theorem E decides the
  window cubic. That is the same decision as Lemma 2, computed by another method: critical chords and [CUB]'s classifier.
- **#243 (open).** Theorem FL and Proposition FL.7 claim a proof of Conjecture 6.
- **#244 (open).** Conditional on #170 Theorem E(1) and [CUB] Theorem C, and through #243 Proposition FL.7's
  identification, it gives `𝓡(t, χ₀)` and `I(t, χ₀)` of (2.5) in closed form, `t* = 2/3`, and
  `H = 1 + (12/25)k² + h_{7/2}k^{7/2} + (728/25)k⁴ + o(k⁴)`. It changes no statement here. §5's v1.3 numbers use it.
- **Not claimed.**
  - Conjectures 6 and 7 are not proved here. For Conjecture 6, see its status in §4. The values of `H` and `R_{2/3}` are
    numerical and not certified.
  - In `d ≥ 3` the fold-scale statements rest on Proposition 2′. It is exact for the model. Its transfer to the field is
    #175 Theorem H for #170's cubic, and #243 Proposition FL.4 here.
  - Nothing about the candidate density's own `ℓ^{2/3}` term.
  - Lemma 2, Lemma 3 and Proposition 4 are statements about the limit models (2.1) and (2.6). Their transfer to the field
    is Conjecture 6.
  - No priority is claimed for the existence of the fold-scale limit, or for the compact-window `ℓ^{2/3}` coefficient
    (#170, #175).
  - The Gaussian-kernel statements are about the model case on `R^d`.

## 7. Controls

`soft_check.py` uses the standard library and exact rationals, except S8 (fixed floating-point cases). Its output is
`RESULTS.json`, which also prints the closed forms of S12 in floating point. In mutant mode the checker prints the names
of the failing controls to stderr.

| Control | Checks |
|---|---|
| S1 | Theorem 1: `69984/72⁴ = 1/384`; `∫_{1/3}^1(φ^{−4} − φ^{−2})dφ = 20/3`; `12·(20/3)/384 = 5/24`; `F₀ = 25π₀p_A(0 \| b)`; the soft window at `f₄ = 0` |
| S2 | the algebra of `G_k` at 60 random rational points: its derivatives (exact four-point stencils), pins, `det H_M = 6λ̃ + Y`, `det H_S = −6λ̃ + Y`, the normalization (both signs of `γ`), weight, measure and typed window |
| S3 | the Gaussian kernel's jet covariances from Hermite numbers: (0.3), and `a′ = 144/(2·6) = 12` |
| S4 | (3.3) as exact truncated series; the double zero at `t = 0`; the Jacobian `−96` (computed for `24φ(R − L_S)`, which equals `N` at `t = 0`) |
| S5 | (3.4), and the antiderivative of the weight |
| S6 | `E[γ⁶] = 120`, `E[γ⁶t²] = 576k²`, `312/25`, `12/25`, and the moment identities of Proposition 4's proof |
| S7 | every numerical inequality of Lemma 3's proof, including the critical-value formulas as identities |
| S8 | Lemma 2 on 16 fixed parameter points with known answers, including case (D′), in floating point; the scan is not reliable within about `4·10^{−3}` of `β = 2` (none of the 16 points is there; §5(2) describes the two artifacts there, and #244's control C9 confirms the 16 decisions from the closed form) |
| S9 | the error exponents of Lemma 5 |
| S10 | the limit (2.1), including `G₁`, on three exactly pinned degree-6 fields with `A = −λ̃r/k`, at `r = 10^{−3}` and `10^{−4}` |
| S11 | Theorem 1 for `m = 2, 3` in rational eigenframes (Cayley rotations): `z = f₄ − 3γᵀA^{−1}γ = 3γ₁²/λ₁ + f̃₄`, `Y = (Δ/12)z`, `w_κ = 36κ²Δ²(1 − φ²)`, the substitution (1.1) with the factor `Π′`, `69984/72⁴ = 1/384`, and the double-soft implication of Step 1 |
| S12 | the Gaussian kernel in `d = 3` from Hermite numbers: given the even pins, `A = −bI + G` with `G` in the Gaussian orthogonal ensemble and `f₄ ~ N(−3b, 24)` independent; the `b`-integrated law (`t ~ N(0, 5/3)`, `f₄ \| t ~ N(6t/5, 138/5)`; `d = 2`: `[[8/3, 2], [2, 30]]`); the odd jets along `e = (3/5, 4/5)` (variances `(6, 2, 2, 6)`); Corollary 1′'s constants `25√3/(48π²)` and `125√30/(192π³)` |
| S13 | Proposition 2′: (2.6), including `G_{1/2}`, on two exactly pinned degree-6 fields in `d = 3` at `r = 10^{−6}` and `10^{−8}` |
| S14 | Lemma 2's exact (D′) witness: `G_{(3/2, 8/3, 20/3)}(X, z) = (1/9)G_{(1/6, 0, 0)}(X + 2z, 3z)` on a unisolvent `4 × 4` rational grid (hence identically); typing; the three critical points `(±½, 0)`, `(−3, 35/8)` of `G_{(1/6,0,0)}` (gradient zero, and the factorization `∂_XG(X, p/2) = (X² − ¼)(3/2 + X/2)`), with witness values `0`, `−1/36 = L_S`, `−125/384`; the (D) certificate at `(1/6, 0, 0)`: the two factorizations `R = (X + ½)²(X² + 3X − 15/4)/8` and `R − L_S = (X − ½)²(X² + 5X + 17/4)/8`, with the signs of their quadratic factors; and, for `β > 2`, `χ < 0`, the open slice `D(1/β) = −χp(1/β) < 0` on rational points |

Mutants `M1`–`M13` each break exactly one control (`M1` S1, `M2` S3, `M3` S4, `M4` S5, `M5` S7, `M6` S8, `M7` S9, `M8` S2,
`M9` S6, `M10` S10, `M11` S11, `M12` S12, `M13` S13, `M14` S14); an unknown label exits 2.

## 8. Sources (exact identities in `SOURCES.json`)

| Tag | Path | Role |
|---|---|---|
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`) | (R5): Gaussian decay of the pin density — consumed |
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`) | §2 finite-jet rank, through #220 — consumed |
| [E1], [E2], [REC] | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md`, `reviews/d1_section9_borel_repair_20260925/REPAIR.md`, `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` | reading rules and the Borel elder mark, through #220 — consumed |
| #207 | `frontiers/cusp_second_order_20261001/PROOF.md` (blob `f6df5a73`) | §§0, 4, 6 (the cusp objects, and the parity factorization after (CU.2), used in Corollary 1′); Theorem CU.2(c) — consumed |
| #218 | `frontiers/candidate_third_order_20261001/PROOF.md` (blob `70ca57ef`) | §0: `𝒜^{cand}`, `I^{cand}`, `B_{d,L}`; Remark 3 — consumed |
| #220 | `frontiers/elder_third_order_20261001/PROOF.md` (blob `c8767dde`) | §0 ((0.1), (0.2)); §1 (window coordinates, (1.1), Lemma Q, (M1)–(M6)) — consumed |
| #229 | `frontiers/third_order_rate_20261001/PROOF.md` (blob `110ed33a`) | (R⁺.1); §0 (`Y_r`); §5 — consumed |
| [C7-K] | `frontiers/c7_total_bounded_20260929/PROOF.md` (blob `28748b08`) | (K2) — cited |
| #187 | `frontiers/far_elder_rate_20260930/PROOF.md` (blob `07260114`) | (0.2): `ν_eld^{far} ≤ Cℓ^{2/3}` — cited |
| #240 | `frontiers/elder_cusp_parity_20261002/PROOF.md` (merged at `7636cae`; blob `16a1db06`, unchanged) | Lemma Q′, Step N6, Corollary N′, Remarks 1 and 4 — cited |
| #170 | `frontiers/local_elder_geometry_20260930/PROOF.md` (merged; blob `ef2aa579`) | §3 (the critical chord), Theorem E, Theorem S, §9 — cited (prior work, AUTH-242-01) |
| #175 | `frontiers/concave_fibre_elder_20260930/PROOF.md` (merged; blob `923d3236`) | Theorems H and F, §7 — cited (prior work, AUTH-242-01) |
| #243 | `frontiers/soft_fold_limit_20261002/PROOF.md` (open PR, head `11a4cd4`; blob `3d9faa87`) | Theorem FL, Proposition FL.7, Lemma FL.2(c) — cited (Conjecture 6) |
| #244 | `frontiers/soft_closed_form_20261002/PROOF.md` (open PR, head `1781c0f`; blob `310ef828`) | Theorems A and B, Corollary A.1, §5 — cited (§5's v1.3 numbers) |
| #237 | `frontiers/candidate_parity_rate_20261001/PROOF.md` (open PR) | Theorem P's remainder, Remark 4 — cited |
| #216 | `frontiers/third_order_coefficient_20261001/NOTE.md` (open PR) | the full-field Monte Carlo in `d = 2, 3` (§5) — cited |
| #188 | far elder density `O(ℓ^N)` (open PR) | §4 (iii) — cited |

## 9. Review slices

- **A** (§§0–1): Theorem 1 in every `d`, its proof (spectral coordinates, the double-soft bound, the substitution),
  Remarks 1–3, and Corollary 1′.
- **B** (§2): the limit field (2.1) and its monomial bookkeeping, the normalization, typing and weight, Lemma 2 (including case
  (D′)), Lemma 3, and Proposition 2′.
- **C** (§3): Proposition 4, namely the definition (3.1) and the factorization in every `d`, the edge (3.3), the
  identification of the rejected set near `(0, 0)`, the series (3.4), the averaging and the bound off `𝒢`.
- **D** (§4): Lemma 5, and whether Conjectures 6 and 7 are stated precisely, with inputs (i)–(iii) complete and consistent with
  #187, #229 and #240.
- **E** (§§5–7): the evidence is described accurately and kept separate from the proofs, and the controls match their
  claims.

**Changed bytes in v1.5** (for a delta check against C80's readback of v1.4, 5394603905):
- *Header:* the object label, the new v1.5 entry, and `≈` in the v1.4 entry (V14-01).
- *§5:* the `H₀` figure in item 4's comparison sentence, and `≈` in item 5's sensitivity sentence (V14-01).
- *§9:* this list.

Everything else in `PROOF.md`, and `soft_check.py` and `RESULTS.json`, is unchanged.

**Changed bytes in v1.4** (for a delta check against the C78 review of v1.3, 5394316763):
- *Header:* the object label, the new v1.4 entry, and the `2.0·10^{−4}` sentence of the v1.3 entry (V13-01).
- *§5:* the last item of item 2 (V13-01); the expansions in item 3 (V13-02); item 4's accuracy sentence and the
  comparison sentence after the recomputation (V13-01); item 5's first sentence (`Ĩ` printed to seven digits, C78's
  rounding note) and its sensitivity sentence (V13-03).
- *§9:* this list.

§§0–4, §§6–8, every value in §5's tables, every other value in §5, `soft_check.py` and `RESULTS.json` are unchanged.
The only changed numbers are the sensitivity `±0.0186` (V13-03) and the extra digits of `Ĩ` in item 5.

**Changed bytes in v1.3** (for a delta check against the v1.2 reviews; AUTH-242-02):
- *Header:* the object label and version history, the closing numerical item of "What is new" (`≈ −0.061` in `d = 3`),
  and the Dependencies (#243's reviewed head, #244).
- *§4:* Conjecture 6's status (#243's reviews), the numerical sentence after Conjecture 7 (`≈ −0.061`), and the
  `v ≥ 2` contribution in Remark 2 (`+0.227`).
- *§5:* the v1.3 custody item; item 2's account of the two `dec1d.py` artifacts; item 3's closed-form paragraph; item 4's
  accuracy sentence, recomputation paragraph, small-`k` paragraph and both value rows; item 5's v1.3 paragraph, and the
  regrouping of its v1.2 record, sensitivity and comparisons (`Ĩ = −1.134` with `C₃` ignored).
- *§§6–8:* the #244 item, the S8 row, and the #243 and #244 source rows.
- *§9:* this list.

§§0–3 (byte-identical), Lemma 5, Conjectures 6 and 7 themselves, §5(1) and §5(6), `soft_check.py` and `RESULTS.json`
are unchanged.

**Changed bytes in v1.2** (for a delta check against the v1.1 reviews):
- *Header:* the version history, the Disposition, "Why" (#240 merged), "What is new" (the window, A-01; the soft model and
  Lemma 2 notes), and the Dependencies (#240, #170, #175, #243).
- *§1:* Remark 1 (A-01).
- *§2:*
  - the opening (B-02);
  - the remainder estimate after (2.1);
  - the absolute Jacobian and `t = 1` (B-03);
  - Lemma 2's statement (`χ > 0` in (D′), `χ ≤ 0` rejected, `e` defined) and its proof (B-01);
  - the exact witness and the remark after the proof;
  - the Schur complement in Proposition 2′'s proof.
- *§3:* the sentence on `k → 0` after (3.1), the prior-work paragraph, the Jacobian normalization (C-02), and the `k^{7/2}`
  sentence (C-01).
- *§4:* the opening (D-01), Conjecture 6's status, input (ii) (D-02), and the matched-asymptotics sentence.
- *§5:* the status, custody and uncertainty labels (E-01, E-02), and #216's domains.
- *§§6–8:*
  - the [C7-K] item, the #170/#175/#243 items and "Not claimed";
  - the S4, S8 and S14 rows;
  - the sources.

§§0–1's proofs, Lemma 3, Proposition 2′, Proposition 4's statement and proof (apart from C-01 and C-02), and Lemma 5 are
unchanged.
