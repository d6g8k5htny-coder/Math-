# The elder density to third order up to its far part, and the three-term law with rate `ℓ^{4/11}` conditional on Math- #187

Object: CL-ELDER-THIRD-ORDER-20261001-v1.1 (supersedes v1 on the same branch).
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 1 October 2026.

**v1.1 changes.**
- Lemma B′, and with it #207 Lemma CU.5 and the exponent `β`, is replaced by two new lemmas (§3):
  - **Lemma H.** The rescaled Hessian `H̃ = Λ_r^{−1}H_MΛ_r^{−1}`, with `Λ_r = diag(r, 1, …, 1)`, is a uniformly
    nondegenerate Gaussian under the pins for all `r ≤ r_0^*`.
  - **Lemma S′.** `E_Q[(W_r/r²)e] ≤ Cℓ^{2/3}r^{−2}(κ + r)P^N` for `r ≤ r_0^*` and `k ≤ r`.

  Together they are the near-regime spectral refinement that #198 Remark 1 describes.
- The intermediate separations `[ρ_c, r_0^*]` now contribute `O(ℓ^{2/5})`: #198 (W.1) below `ℓ^{2/15}`, Lemma S′ above.
  So (E3.0) is an expansion with only the far elder density at the fixed radius `r_0^*` left unexpanded.
- Consequently (E3.3) has the rate `O(ℓ^{4/11})` and uses #187 at the single separation `r_0^*`. v1's `ε`-argument
  (`r₁ ↓ 0`) is gone, and so is v1 Remark 2's need for a quantified `C(ρ)`. Corollary E3′(3) gets the same rate.
- (E3.1), (E3.2) and Lemmas CU.1′, S, Q, G, CE and O′ are unchanged, except that Lemma CE's radius no longer involves
  #207 Lemma CU.5. (CU.5 still appears in #218's dependency list, but only nominally: #218's Step F1 re-proves the
  nondegeneracy of the free jets on `(0, r_0^*]`.)
- Controls: X1 is the new ledger. X8 (Lemma S′'s linear algebra) and X9 (Lemma H's exact form (H.1) on exactly pinned
  polynomial fields) are new, with mutants M6–M8.
- The nonauthor reviews of v1 on #220 (OpenAI / Codex, delegated; Slices A, B and C, all PASS_TECHNICAL at their stated
  scope) requested two amendments:
  - **OA-220-B-01**, applied: Lemma G (b) now assumes `E[H(E)] < ∞`, and Step E6 records why it holds there.
  - **OA-220-C-01**, superseded: it repaired v1 Remark 2's shrinking cut-off `r₁ = ℓ^{1/(3(p+β))}`, which could fall
    below the cusp band. v1.1 has no shrinking cut-off: the near/far cut is the fixed `r_0^*`, and Remark 2 is replaced.
- #191 and #198 have been merged with the blobs consumed here, so they are now listed as merged inputs. #207's head moved
  to `782211f`, a merge of `main`; its PROOF blob `f6df5a73` is unchanged.

**v1.1 review record.** Before submission of v1.1, a clean-context same-family referee read the v1 → v1.1 delta
against all eight sources at their declared blobs (`REFEREE_2.md` in the project archive). Its verdict was ACCEPT WITH
MINOR FIXES, with no major finding.
- *What it verified independently.*
  - (H.1), symbolically by Peano kernels (sympy), and on non-polynomial test functions.
  - Lemma H's covariance, numerically. The direct form of `H̃` and the segment form (H.1) agree to `7·10⁻¹¹` for the
    Gaussian kernel (two representations sharing one covariance code), and they reproduce the author's 60-digit
    `mpmath` exploration, which uses the raw pins. The segment form was also evaluated on small tori (`L = 2, 3, 6` in
    `d = 2`, `L = 3` in `d = 3`) in several frames.
  - The `ε²` mechanism of Lemma S′, by Monte Carlo under the exact pinned law of `H̃`.
  - The §4 ledger and every comparison claim, in exact rationals.
  - All controls and mutants.
- *Fixes applied.*
  - **MINOR-1.** (F1) is stated for every `r ≤ r_0^*`, as the own-jet form of #198 (3.1), with the reason.
  - **Nits.** The pin rows `U_r` and the target `v_r` are cited from [P] (3.1)–(3.3). The continuity and invertibility
    arguments of Lemma H (a) are made explicit. The rescaling matrix is renamed `Λ_r`, to avoid a clash with [R] §4's
    `D_r`. `n′` is defined in Lemma S′, and Lemma H (b) cites the argument of #218 (1.2), not its statement. The
    identification of #187's far density with #198's (2.1), the content of the first equivalence, and Remark 1's
    attribution are all corrected or stated. X8 now asserts the attained case. The exploration paragraph records the
    small-torus constants.

**v1 review record.** Before submission of v1, a clean-context same-family referee read the whole note against its
sources (`REFEREE_1.md` in the project archive). Its verdict was ACCEPT WITH MINOR FIXES, with no major finding. Its
four minor findings and nine nits were applied:
- the radius `r_Q` is defined, and Step E2 states the conditions on `r` alone;
- (F3) and (F5) are derived from #218 Step F1 instead of being attributed;
- Remark 3 now describes #216's Monte Carlo correctly: its elder-pair row estimates `ν_eld` itself;
- the title no longer states the conditional (E3.3) as proved;
- the nits: the derivation of `λ₂`, notation, dependency citations and Remarks 2, 4 and 6.

The referee also tested Lemma Q's decision by a two-dimensional union–find maximin on 48 exactly pinned fields, all three
cases, margins down to `0.02`: 48 of 48 agree (floating point; exploration).

Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph,
STATUS, PROOF_INDEX, prize or Boolean change; no numerical constant is certified. Same GitHub account as every lane;
zero organizational independence.

**Dependencies (consumed, now merged).** Math- #191 and #198 were merged into `main` on 1 October 2026 (merge commits
`9556547` and `124c37d`), with the same blobs that v1 consumed. They are now merged inputs:
- Math- #191 (`frontiers/remainder_vanishing_20260930/PROOF.md`, blob `441152df`): Lemma E Steps 1–4, §2 (2.1), the
  admissible radius `r_0^*`.
- Math- #198 (`frontiers/remainder_rate_20260930/PROOF.md`, blob `abfb98ae`): (3.1) and the sign window of §3, Lemma
  B's barrier (1.2) and §1's elder-density identity, Lemma W's (W.1), the far integral (2.1), Lemma F′.

**Dependencies (unmerged, consumed).** This note cannot be integrated before the following, and must be rebound if any
of them changes:
- Math- #207 (`frontiers/cusp_second_order_20261001/PROOF.md`, v1.1 blob `f6df5a73`): §0 (the cusp objects), the proof
  of Theorem CU.1, Theorem CU.2, the structure of Proposition CU.3 (re-proved here with explicit margins), §6 ((6.1),
  (CU.2)).
- Math- #218 (`frontiers/candidate_third_order_20261001/PROOF.md`, blob `70ca57ef`): Lemma D (also applied here to the
  rescaled Hessian of Lemma H), (1.2) and its proof, Lemma F (Steps F1, F3, (F.2)), Lemma C (Steps C1, C2 and C3),
  Lemma O, Theorem T and §4 (the fold region and the exponent ledger).
- For (E3.3) and Corollary E3′(3) only: Math- #187 (`frontiers/far_elder_rate_20260930/PROOF.md`, blob `07260114` at
  `75c686c`), Theorem F at the single separation `ρ = r_0^*`. (Rebound on 1 October from blob `37dcf6ef`: #187's
  status sentence now records that #182 is integrated. Theorem F and its proof are unchanged.)

**Merged inputs:** [R], [P] with [E1]/[E2]/[REC] ([P] §2's linear independence of derivative functionals also enters
Lemma H directly), [C7-K] ((K2) and §4), and [Z] (Z13)–(Z14) with [P] §10 (the change of variables behind the
near/far identity); [182] and further parts of [Z] enter through #198 and #191.

## 0. Statement

Setting and notation are those of #218 §0, which are those of [R], #191, #198 and #207:
- fixed `d ≥ 2`, `m = d − 1`, `L > 0`, the [P] field on `X = R^d/(LZ^d)`;
- near pins `M = −ru/2`, `S = ru/2` at heights `b`, `b − kr³`, the pinned law `Q = Q_{r,b,k}`, the pin density
  `π_r(v_r)`, `P = 1 + |b| + k`, the scaled endpoint Hessians `K_M`, `K_S`, and `W_r/r² = F_d(K_M)F_{d−1}(K_S)`;
- the elder mark `e = 1{d_f(M) = f(S)}`, with `d_f(M) = sup{min_t f(γ(t)) : γ(0) = M, f(γ(1)) > f(M)}` ([P] §8; Borel by
  [E2] §9);
- the kernels `A_r = 12π_r(v_r)E_Q[W_r/r²]`, `A_r^{eld} = 12π_r(v_r)E_Q[(W_r/r²)e]` and `A_0 = 12π_0(v_0)z_0`.

For every `r_0 ∈ (0, r_0^*]`, the canonical marked Kac–Rice version of the elder density is

    ν_eld(ℓ) = ∫_0^{r_0}∫_R∫_{S^{d−1}} r^{−2}A_r^{eld}(b, ℓ/r³, u) dσ db dr + ν_eld^{far,r_0}(ℓ).

This combines #198 §1's identity on separations `[ρ, r_0)` (the identity behind (B.2)), the far integral #198 (2.1),
and the change of variables of [P] §10 ([Z] (Z13)–(Z14)); #207 §0 states it at `r_0 = r_0^*`. Also
`cℓ^{−1/3} = ∫_0^∞∫∫ r^{−2}A_0(b, ℓ/r³, u)`. The candidate and rejected densities are `ν_cand` and
`ρ_rej = ν_cand − ν_eld` (#198 §0).

**Cusp objects (#207 §§0, 4, 6).** Jets at `0` under the contact law at the zero-gap target `v_0(b, 0)`: `f₄`, `γ`,
`A`, `Δ = det A` and `Y = (f₄/12)Δ − γᵀadj(A)γ/4`; `E_0[· | b]` is the expectation under that law. For `κ > 0`,

    w_κ^{eld}(A, Y) := (36κ²(det A)² − Y²) 1{A < 0, |Y| < 2κ|det A|},
    loss_κ(A, Y) := 36κ²(det A)²1{A < 0} − w_κ^{eld}(A, Y) = [Y²1{|Y| < 2κ|Δ|} + 36κ²Δ²1{|Y| ≥ 2κ|Δ|}] 1{A < 0},   (0.1)

`𝒜^{eld}(b, κ, u) = 12π_0(u; v_0(b, 0))E_0[w_κ^{eld} | b]` and `𝒜^{con}(b, κ, u) = 12π_0(u; v_0(b, 0))E_0[36κ²Δ²1{A < 0} | b]`,
so that `𝒜^{eld} − 𝒜^{con} = −12π_0E_0[loss_κ | b] ≤ 0`. The second-order coefficient is

    c₁ = ∫_{S^{d−1}}∫_R∫_0^∞ (𝒜^{eld} − 𝒜^{con})(b, s^{−4}, u) ds db dσ(u) < 0                           (0.2)

(#207 §6: the `s`-integral is (6.1), and (0.2) is (CU.2)). The third-order coefficient `c₂` is #218 (0.1), the
Hadamard finite part of `(1/3)∫∫∫A₂k^{−4/3}`, where `A₂(b, k, u)` is the fold coefficient of #218 Lemma F, with
`A₂(b, 0, u) = −12π_0E_0[Y²1{A < 0} | b]` ((F.2) there). `𝒜^{cand}` is #218 §0's candidate cusp kernel (weight
`(36κ²Δ² − Y²)1{A < 0, |Y| < 6κ|Δ|}`), and `I^{cand}` and `B_{d,L}` are as in #218 §0.

**Theorem E3 (the elder density to third order).** For every `d ≥ 2` and `L > 0`, as `ℓ ↓ 0`,

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{4/11}),    0 ≤ ν_eld^{far,r_0^*}(ℓ) ≤ C ℓ^{1/3}.   (E3.0)

Consequently

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + O(ℓ^{1/3});                                                    (E3.1)
    ν_eld(ℓ) ≥ c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} − C ℓ^{4/11};                                          (E3.2)

and if, in addition, Math- #187's Theorem F holds at the separation `ρ = r_0^*` (`ν_eld^{far,r_0^*}(ℓ) ≤ Cℓ^{2/3}`), then

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{4/11}).                                         (E3.3)

More precisely, (E3.0) reduces the third-order law to the far elder density at the one fixed separation `r_0^*`:
- for `0 < θ ≤ 4/11`, `ν_eld(ℓ) − cℓ^{−1/3} − c₁ℓ^{1/4} − c₂ℓ^{1/3} = O(ℓ^θ)` if and only if `ν_eld^{far,r_0^*}(ℓ) = O(ℓ^θ)`
  (for `θ ≤ 1/3` both sides hold by (E3.1) and #198 Lemma F′, so the content is `1/3 < θ ≤ 4/11`);
- the three-term law with remainder `o(ℓ^{1/3})` holds if and only if `ν_eld^{far,r_0^*}(ℓ) = o(ℓ^{1/3})`.

**Corollary E3′ (the rejected density).** With Theorem T of #218,

    ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁) ℓ^{1/4} − ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{4/11}).                                  (E3′.0)

In particular:
1. `ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + O(ℓ^{1/3})` — a rate for #207's (CU′.2);
2. `ρ_rej(ℓ) ≤ B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + Cℓ^{4/11}`;
3. under #187's Theorem F at `ρ = r_0^*`, `ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + O(ℓ^{4/11})`: the `ℓ^{1/3}`
   terms of the candidate and elder densities are equal, so the rejected density has none.

(E3.1) is a rate for #207's (CU.1), which claimed no rate for its `o(ℓ^{1/4})`. (E3.3) identifies the third coefficient
of the elder law with the `c₂` that Math- #216 defines and computes (`0.22152441` in `d = 2`, `0.16123405` in `d = 3`
for the Gaussian kernel; numerical approximations, not certified), with the rate `ℓ^{4/11}` of #218's Theorem T.

**How it works.** The decomposition is that of Theorem T (#218 §4), with the elder kernel in place of the candidate
kernel.
- *Fold scale `r ≍ ℓ^{1/3}`.* The elder deficit `A_r − A_r^{eld}` is at most `Cr³/k` ([C7-K] (K2)), which contributes
  `O(ρ_f⁵/ℓ)`, the same order as the boundary layer of #218 Lemma F. So the fold region gives `c₂ℓ^{1/3}` exactly as
  for the candidate density.
- *Cusp scale `r ≍ ℓ^{1/4}`.* Lemma CE gives the elder cusp kernel with the candidate rate, `O(r(1 + κ)²)`. Its new
  input is Lemma Q, a quantitative form of #207's Proposition CU.3: the elder decision is correct as soon as the rescaled
  ridge is within `(3/2)κ||φ| − 1/3|` of the model ridge in `C⁰` and within `κ/4` in `C²`. Both distances are
  `O(𝒩r(1 + |γ|/λ)²)`, where `λ` is the transverse concavity and `𝒩` bounds the `C⁵` norm. A wrong decision therefore needs `φ` in a window of width
  `O(𝒩r(1 + |γ|/λ)²/κ)` or a small `λ`, and the weight `36κ²Δ²` pays for both: `Δ² ≤ λ²‖A‖^{2m−2}` cancels the `1/λ²`.
- *Overlap.* Lemma O′: `𝒜^{cand} − 𝒜^{eld} = O(1/κ)`, so the elder cusp loss tends to `A₂(b, 0)` at rate `1/κ`, as the
  candidate loss does (#218 Lemma O). The overlap cancellation of #218 §4 goes through unchanged.
- *Intermediate separations `ρ_c ≤ r ≤ r_0^*`.* Split at `ℓ^{2/15}`.
  - Below the split, #198's unmarked bound (W.1) suffices.
  - Above it, Lemma S′ applies. #198's barrier puts an eigenvalue of `−H_M` below `(ℓK²/c_L)^{1/3}`. The pins make the
    axial curvature `∂_u²f(M)` of order `r²`, so the right object is the rescaled Hessian `H̃ = Λ_r^{−1}H_MΛ_r^{−1}`, and
    the barrier puts `λ_min(−H̃)` below `Cℓ^{1/3}r^{−2}`.
  - Lemma H shows that `H̃` is a uniformly nondegenerate Gaussian under the pins. So #218's Lemma D charges that event
    twice: once in `|det H̃|` and once in probability. The result is `E_Q[(W_r/r²)e] ≤ Cℓ^{2/3}r^{−2}(κ + r)P^N`.
  - Both halves integrate to `O(ℓ^{2/5})`.
- *Far separations `r ≥ r_0^*`.* `ν_eld^{far,r_0^*}` stays as it is in (E3.0).
  - #198 Lemma F′ bounds it by `Cℓ^{1/3}`, which gives (E3.1).
  - #187 bounds it by `C(r_0^*)ℓ^{2/3}`, which gives (E3.3) with the rate `ℓ^{4/11}`.

  Only the one fixed separation `r_0^*` is involved, so no limit in a cut-off and no dependence of #187's constant on
  `ρ` are needed.

**What is not claimed.**
- (E3.3) and Corollary E3′(3) are conditional on #187, an unmerged author-side candidate, used at the single separation
  `r_0^*`. (E3.0)–(E3.2), (E3′.0) and Corollary E3′(1)–(2) do not use it.
- No sharpness of the exponent `4/11`. It is the least exponent of #218's ledger, attained by `ρ_f⁵/ℓ` and `ℓ²ρ_f^{−6}`.
  The intermediate separations contribute only `O(ℓ^{2/5})`.
- No certified numerical value of `c`, `c₁`, `c₂`, `I^{cand}` or `B_{d,L}`.
- No uniformity in `d` or `L`; no finite-radius band; no statement about the adjacent-pair density, which #216 also
  measures.
- Nothing beyond the existential scope of [R], [Z], [C7-K], #191, #198, #207, #218 and (for (E3.3)) #187.

## 1. The elder decision, quantitatively

This section is deterministic. Fix `f ∈ C⁵(X)` and `𝒩 ≥ max(1, ‖f‖_{C⁵})`, where `‖f‖_{C^q}` is the supremum over `X`
of the operator norms of the derivatives of order `≤ q`. Let `0 < r ≤ r_Q := min{1/10, r_L}`, where `r_L` is the
positive root of `6r + 10r² = L/8`; let `κ > 0`, and let `M = −ru/2`, `S = ru/2` be
critical points with `f(M) = b`, `f(S) = b − κr⁴`. In the frame `(u, Θ)` put `Φ(X, Ξ) := rXu + r²ΘΞ`,
`𝔉 := r^{−4}(f∘Φ − b)`, and let `(f₄, γ, A)` be the jets of `f` at `0` and `𝔓` the cusp polynomial (#207 (0.2)) built
from them:

    𝔓(X, Ξ) = 2κ(X + ½)²(X − 1) + (f₄/24)(X² − ¼)² + ½(X² − ¼)γ·Ξ + ½ΞᵀAΞ.

When `A < 0`, `Ξ*(X) := −½(X² − ¼)A^{−1}γ` and `g(X) := 𝔓(X, Ξ*(X)) = κ[2(X + ½)²(X − 1) + 3φ(X² − ¼)²]` with
`φ := (f₄ − 3γᵀA^{−1}γ)/(72κ)` (#207 Theorem CU.2 (a)).

**Lemma CU.1′ (weighted Taylor bounds).** There is `C₁ = C₁(d)` such that on `{|X| ≤ 3, r|Ξ| ≤ 1}`

    |𝔉 − 𝔓|, |∂_X(𝔉 − 𝔓)| ≤ C₁𝒩r(1 + |Ξ|)²,   |∂_Ξ(𝔉 − 𝔓)|, |∂_X²(𝔉 − 𝔓)|, |∂_X∂_Ξ(𝔉 − 𝔓)| ≤ C₁𝒩r(1 + |Ξ|),   ‖∂_Ξ²(𝔉 − 𝔓)‖ ≤ C₁𝒩r.   (1.1)

*Proof.* Follow the proof of #207 Theorem CU.1, keeping track of `Ξ`. There are three sources of `𝔉 − 𝔓`.
- *Pin corrections.* The pinned jets differ from the values that produce `𝔓` by `O(𝒩r⁵)` (`ϑ₀ − b`), `O(𝒩r⁴)` (`ϑ₁`),
  `O(𝒩r³)` (`ϑ₂`), `O(𝒩r²)` (`ϑ₃`), `O(𝒩r⁴)` (`ψ₀`) and `O(𝒩r²)` (`ψ₁`); the constants do not depend on `κ`, which enters
  only through the exact pins. After rescaling they contribute `O(𝒩r)(1 + |X|³) + O(𝒩r)|X||Ξ| + O(𝒩r²)|Ξ|`, and their
  derivatives obey (1.1).
- *Dropped monomials.* These are the Taylor monomials `x^iy^j` with weighted degree `i + 2|j| ≥ 5` and total degree
  `i + |j| ≤ 4`: `(i, |j|) ∈ {(3,1), (1,2), (2,2), (0,3), (1,3), (0,4)}`, with coefficients bounded by `C𝒩`. Each becomes
  `r^aX^iΞ^j` with `a = i + 2|j| − 4 ≥ 1`. On `r|Ξ| ≤ 1` (and `r ≤ 1`), `r^a|Ξ|^s ≤ r|Ξ|^{s−a+1}` for `s ≥ a − 1`, and `≤ r` otherwise.
  Here `|j| − a + 1 = 5 − i − |j| ≤ 2`. A derivative in `Ξ` lowers `s` by one. Two derivatives in `X` need `i ≥ 2`,
  and then `5 − i − |j| ≤ 1`. One derivative in `X` keeps the bound `(1 + |Ξ|)²`, through `∂_X(rXΞ²) = rΞ²`.
- *Remainder.* `|∂^αρ₅(x, y)| ≤ C𝒩(|x| + |y|)^{5−|α|}` for `|α| ≤ 2`. At `(rX, r²Ξ)` with `|X| ≤ 3` and `r|Ξ| ≤ 1`,
  `|x| + |y| ≤ 4r`. So `|∂_X^p∂_Ξ^q[r^{−4}ρ₅(rX, r²Ξ)]| = r^{p+2q−4}|∂_x^p∂_y^qρ₅| ≤ C𝒩4⁵r^{1+q}`. ∎ (The `∂_X` bound in (1.1) is not used
below.)

Checker X5 verifies the mechanism exactly on pinned polynomial fields in `d = 2, 3`: every monomial `r^aX^iΞ^j` of
`𝔉 − 𝔓` has `a ≥ 1` and `|j| ≤ a + 1`.

**Lemma S (Schur complements).** Let `D, D′ ∈ Sym(m)` with `D ≤ −λI` and `D′ ≤ −(λ/2)I`, and let `a, a′ ∈ R` and
`b, b′ ∈ R^m`. Put `s := a − bᵀD^{−1}b` and `s′ := a′ − b′ᵀD′^{−1}b′`. Then

    |s′ − s| ≤ |a′ − a| + (2/λ)|b′ − b|(|b| + |b′|) + (2/λ²)|b|²‖D′ − D‖.                                   (1.2)

*Proof.* `b′ᵀD′^{−1}b′ − bᵀD^{−1}b = (b′ − b)ᵀD′^{−1}(b′ + b) + bᵀD′^{−1}(D − D′)D^{−1}b`, with `‖D′^{−1}‖ ≤ 2/λ` and
`‖D^{−1}‖ ≤ 1/λ`. ∎

**Lemma Q (the elder decision with explicit margins).** Suppose `A ≤ −λI` with `λ > 0`, and put

    Γ := |γ|/λ,    ε* := 80C₁𝒩r(1 + Γ)²,    R := 5(1 + Γ) + 3((κ + 1)/λ)^{1/2}.

Assume
- (Q1) `𝒩(3r + r²R) ≤ λ/2` and `6r + 2r²R ≤ L/4`;
- (Q2) `5r(1 + Γ) ≤ 1` and `8C₁𝒩r(1 + 5Γ) ≤ λ`;
- (Q3) `ε* ≤ κ/4`;
- (Q4) `|φ| ≤ 1` and `||φ| − 1/3| > 2ε*/(3κ)`.

Then

    e(f) = 1{d_f(M) = f(S)} = 1{|φ| < 1/3}.                                                              (1.3)

*Proof.* Put `M₁ := (35/8)Γ`, so that `|Ξ*(X)| ≤ ½·(35/4)|A^{−1}γ| ≤ M₁` for `X ∈ [−3, 2]`.

*Step Q1 (the window).* Let `𝒲 := [−3, 2] × {|Ξ| ≤ R}`.
- `Φ` is linear and injective. `Φ(𝒲)` has diameter at most `5r + 2r²R < L/4` by (Q1), so `Φ` embeds a neighbourhood of
  `𝒲` in the torus. In particular it maps the interior and boundary of every subregion of `𝒲` onto the interior and
  boundary of its image.
- On `𝒲`, `∂_Ξ²𝔉(X, Ξ) = D_Θ²f(Φ(X, Ξ)) ≤ A + ‖D³f‖(3r + r²R)I ≤ −(λ/2)I` by (Q1), as `‖D³f‖ ≤ 𝒩`.

*Step Q2 (the ridge and its distance from the model's).* Fix `X ∈ [−3, 2]`. The ball `{|Ξ − Ξ*(X)| ≤ 1}` lies in
`{|Ξ| ≤ 5(1 + Γ)}`, where `r|Ξ| ≤ 1` by (Q2); and it lies in `𝒲`.
- *The maximizer.* Since `∂_Ξ𝔓(X, Ξ*) = 0`, (1.1) gives `|∂_Ξ𝔉(X, Ξ*)| ≤ C₁𝒩r(1 + M₁) ≤ λ/8` by (Q2). So on the sphere
  `|Ξ − Ξ*| = 1`, `𝔉(X, Ξ) ≤ 𝔉(X, Ξ*) + λ/8 − λ/4 < 𝔉(X, Ξ*)`. Hence the unique maximizer `Ξ_𝔉(X)` of the strictly
  concave `𝔉(X, ·)` over `{|Ξ| ≤ R}` lies in the open unit ball around `Ξ*`. There `∂_Ξ𝔉 = 0`, and strong concavity gives
  `|Ξ_𝔉 − Ξ*| ≤ (2/λ)|∂_Ξ(𝔉 − 𝔓)(X, Ξ*)| ≤ 1/4`.
- *The ridge function.* `g_𝔉(X) := 𝔉(X, Ξ_𝔉(X))` is `C²` by the implicit function theorem. Its second derivative is the
  Schur complement of `∂_Ξ²𝔉` in `Hess 𝔉` at `(X, Ξ_𝔉)`. The same holds for `g` with `(𝔓, Ξ*)` (#207 Proposition CU.3,
  Step 1).
- *`C⁰` distance.* `g − |𝔉 − 𝔓|(X, Ξ*) ≤ 𝔉(X, Ξ*) ≤ g_𝔉(X) ≤ 𝔓(X, Ξ_𝔉) + |𝔉 − 𝔓|(X, Ξ_𝔉) ≤ g + |𝔉 − 𝔓|(X, Ξ_𝔉)`.
  Hence `ε₀ := sup_{[−3,2]}|g_𝔉 − g| ≤ C₁𝒩r(5/4 + M₁)² ≤ ε*`.
- *`C²` distance.* Apply (1.2) with `(a, b, D) = (∂_X²𝔓, Xγ, A)` at `(X, Ξ*)` and `(a′, b′, D′)` the blocks of `Hess 𝔉`
  at `(X, Ξ_𝔉)`.
  - `∂_X²𝔓` depends on `Ξ` only through `γ·Ξ`, so `|a′ − a| ≤ C₁𝒩r(5/4 + M₁) + |γ||Ξ_𝔉 − Ξ*| ≤ C₁𝒩r[(5/4 + M₁) + 2Γ(1 + M₁)]`.
  - `|b′ − b| ≤ C₁𝒩r(5/4 + M₁) ≤ 5λ/32` by (Q2), `‖D′ − D‖ ≤ C₁𝒩r`, and `|b| ≤ 3|γ|`.
  - So `ε₂ := sup_{[−3,2]}|g_𝔉″ − g″| ≤ C₁𝒩r[(5/4 + M₁)(21/16 + 12Γ) + 2Γ(1 + M₁) + 18Γ²]
    = C₁𝒩r[105/64 + (2911/128)Γ + (317/4)Γ²] ≤ ε*`.

  (Checker X6 verifies (1.2) and both polynomial bounds exactly.)

*Step Q3 (reduction to the ridge).* This is #207 Proposition CU.3, Steps 2–3, with `𝒲` as above.
- For every `t`, each nonempty `X`-fiber of `𝒲 ∩ {𝔉 > t}` is convex and contains `Ξ_𝔉(X)`, and it is nonempty iff
  `g_𝔉(X) > t`. So the path components of `𝒲 ∩ {𝔉 > t}` are the parts over the components of
  `{X ∈ [−3, 2] : g_𝔉(X) > t}`, and the supremum of `𝔉` over such a part is the supremum of `g_𝔉` over that interval.
- On `|Ξ| = R`, `|Ξ − Ξ_𝔉(X)| ≥ R − M₁ − 1/4 ≥ 3((κ + 1)/λ)^{1/2}`, so by strong concavity
  `𝔉(X, Ξ) ≤ g_𝔉(X) − (9/4)(κ + 1)`.                                                                   (1.4)

*Step Q4 (exact values at the pins).* `M = Φ(−½, 0)` and `S = Φ(½, 0)` are critical points of `f`. So `(±½, 0)` are
critical points of `𝔉`, `Ξ_𝔉(±½) = 0`, `g_𝔉(−½) = 0`, `g_𝔉(½) = −κ` and `g_𝔉′(±½) = 0`. The same holds for `g`.
Therefore `h := g_𝔉 − g` satisfies `|h| ≤ ε₀` and `|h(X)| ≤ (ε₂/2)(X ∓ ½)²` on `[−3, 2]`.

*Step Q5 (the margins of the model ridge).* With `X₃ := −1/(2φ)`, from #207 (2.1) and Theorem CU.2 (d):
- (M1) `g + κ = κ(X − ½)²[2(X + 1) + 3φ(X + ½)²]` and `g = κ(X + ½)²[2(X − 1) + 3φ(X − ½)²]`;
- (M2) `g + κ ≥ κ(X − ½)²` on `[−½, X_R]` when `|φ| < 1/3`, where `X_R := 2` for `φ ≥ −1/4` and `X_R := X₃ = 1/(2|φ|) ∈ (3/2, 2)`
  for `−1/3 < φ < −1/4`. For `φ ≥ 0` the bracket is `≥ 2(X + 1) ≥ 1`; for `φ < 0` it is `1 + (X + ½)(2 − 3|φ|(X + ½)) ≥ 1`
  as long as `X + ½ ≤ 2/(3|φ|)`, which holds up to `X₃ = 1/(2|φ|)` when `|φ| ≤ 1/3`;
- (M3) `g ≤ −κ(X + ½)²` on `[−3/2, ½]` when `φ ≤ 1/3`. The bracket is `≤ 2(X − 1) + (X − ½)²`, which is convex and equals
  `−1` at both ends;
- (M4) `g(X₃) + κ = κ(φ + 1)³(3φ − 1)/(16φ³)` and `g(X₃) = κ(φ − 1)³(3φ + 1)/(16φ³)`. Hence:
  - for `1/3 ≤ φ ≤ 1`, `g(X₃) + κ − (3/2)κ(φ − 1/3) = κ(3φ − 1)[(φ + 1)³ − 8φ³]/(16φ³)
    = κ(3φ − 1)(1 − φ)(7φ² + 4φ + 1)/(16φ³) ≥ 0`;
  - for `−1 ≤ φ ≤ −1/3`, the same identity in `ψ = −φ` gives `−g(X₃) ≥ (3/2)κ(|φ| − 1/3)`;
  - for `−1/3 ≤ φ < 0`, with `ψ = −φ`, `g(X₃) = κ(1 + ψ)³(1 − 3ψ)/(16ψ³)` and
    `g(X₃) − 12κ(1/3 − ψ) = κ(1 − 3ψ)[(1 + ψ)³ − 64ψ³]/(16ψ³) = κ(1 − 3ψ)²(21ψ² + 6ψ + 1)/(16ψ³) ≥ 0`;
- (M5) `g(2) = κ(25/2 + (675/16)φ)`, `g(−3/2) = κ(−5 + 12φ)` and `g(−3) = κ(−50 + (3675/16)φ)`. So `g(2) ≥ (125/64)κ` for
  `φ ≥ −1/4`; `g(2) ≤ −(25/16)κ` and `g(−3/2) ≤ −9κ` for `φ ≤ −1/3`; `g(−3/2) + κ = −12κ(1/3 − φ)`; and
  `g(−3) ≥ (425/16)κ` for `φ ≥ 1/3`;
- (M6) `g′ = 6κ(X² − ¼)(1 + 2φX)`. For `1/3 < φ ≤ 1`, `g` decreases on `[−3, X₃]` and increases on `[X₃, −½]`. For
  `−1 ≤ φ < −1/3`, `g` increases on `[½, X₃]` and decreases on `[X₃, 2]`.

(Checkers X2–X3 verify (M1)–(M5) exactly.)

*Step Q6 (the decision).* By (Q3)–(Q4), `ε₂ ≤ ε* ≤ κ/4` and `ε₀ ≤ ε* < (3/2)κ||φ| − 1/3|`.
- *Case E, `|φ| < 1/3`.*
  - *Path.* On `[−½, X_R]`, (M2) and Step Q4 give `g_𝔉 + κ ≥ (κ − ε₂/2)(X − ½)² ≥ 0`. At `X_R`, `g_𝔉(X_R) > 0`: for
    `φ ≥ −1/4`, `g(2) ≥ (125/64)κ > κ/4 ≥ ε₀`; otherwise `g(X₃) ≥ 12κ(1/3 − |φ|) > ε₀` by (M4). So the ridge curve
    `X ↦ Φ(X, Ξ_𝔉(X))`, `X ∈ [−½, X_R]`, runs from `M` through `S` to a point above `b`, and along it `f ≥ f(S)`. Hence
    `d_f(M) ≥ f(S)`.
  - *Trap.* Let `𝒟 := (−3/2, ½) × {|Ξ| < R}` and `𝒟_phys := Φ(𝒟)`.
    - At `X = −3/2`: `𝔉 ≤ g_𝔉(−3/2) ≤ −κ − 12κ(1/3 − φ) + ε₀ < −κ`, since `ε₀ < 12κ(1/3 − φ)` (for `φ ≤ 0` the margin is
      `≥ 4κ`).
    - At `X = ½`: `𝔉 ≤ g_𝔉(½) = −κ`, with equality only at `Ξ = 0`, i.e. at `S`.
    - On `[−3/2, ½]`, (M3) and Step Q4 give `g_𝔉 ≤ −(κ − ε₂/2)(X + ½)² ≤ 0`. So at `|Ξ| = R`, (1.4) gives
      `𝔉 ≤ −(9/4)(κ + 1) < −κ`.

    So `f ≤ f(S)` on `∂𝒟_phys`. The path component `C` of `{f > f(S)}` containing `M` does not meet `∂𝒟_phys`, hence
    `C ⊂ 𝒟_phys`. By Step Q3 its supremum is `b + r⁴ sup g_𝔉` over an interval in `(−3/2, ½)`, which is `≤ b`. So every
    path from `M` to a point above `b` leaves `C`, and `d_f(M) ≤ f(S)`. Thus `e = 1`.
- *Case R⁺, `1/3 < φ ≤ 1`.* By (M6) and (M4), `min_{[−3,−½]} g = g(X₃) ≥ −κ + (3/2)κ(φ − 1/3)`, so
  `min_{[−3,−½]} g_𝔉 > −κ`. Also `g_𝔉(−3) ≥ (425/16)κ − κ/4 > 0` by (M5). So the ridge curve from `M` to `X = −3` ends
  above `b` and stays above `f(S)`: `d_f(M) > f(S)` and `e = 0`.
- *Case R⁻, `−1 ≤ φ < −1/3`.* Put `t* := −(5/4)κ` and `𝒟′ := (−3/2, 2) × {|Ξ| < R}`.
  - `g_𝔉 ≤ 0` on `[−3/2, 2]`. On `[−3/2, ½]` this is (M3) with Step Q4. On `[½, 2]`, (M6) and (M4) give
    `g ≤ g(X₃) ≤ −(3/2)κ(|φ| − 1/3) < −ε₀`.
  - On `∂𝒟′`: `g_𝔉(−3/2) ≤ −9κ + κ/4 < t*` and `g_𝔉(2) ≤ −(25/16)κ + κ/4 < t*` by (M5); at `|Ξ| = R`, (1.4) gives
    `𝔉 ≤ −(9/4)(κ + 1) < t*`.

  So the component `C′` of `{f > b + r⁴t*}` containing `M` lies in `Φ(𝒟′)`, and its supremum is at most `b`. Every path
  from `M` to a point above `b` leaves `C′`, so `d_f(M) ≤ b + r⁴t* < f(S)` (or `d_f(M) = −∞`), and `e = 0`. ∎

Only window information is used, as in #207: every conclusion is an explicit path inside `Φ(𝒲)` or a trap whose boundary
lies inside it. No type condition is used either: Lemma Q does not need `M`, `S` to be typed.

## 2. The elder cusp kernel with a rate

**Notation for this section.** Let `0 < r ≤ r₂`, `κ > 0` and `k = κr ≤ 1`, and let `f = F_r` under `Q`.
- `𝒩_r := 1 + k + ‖F_r‖_{C⁹}`.
- `J′` is the vector of free jets of `f` at `0` of order `≤ 9` (#218 Step F1); `J″ := J′ ∖ {f₄}` and
  `J‴ := J″ ∖ {A}`, where `A := D_Θ²f(0)`.
- `Δ := det A`, `λ := λ_min(−A)` on `{A < 0}`, `γ := ∇_Θ∂_u²f(0)` and `B := ∂_uD_Θ²f(0)`. All of these lie in `J′`.
- `Y_r := (f₄/12)Δ + 3k tr(adj(A)B) − γᵀadj(A)γ/4`. This is #191's `Y`, built from `F_r`'s own jets.
- `Y′ := Y_r − 3k tr(adj(A)B)` and `φ_r := (f₄ − 3γᵀA^{−1}γ)/(72κ)`, so that `Y′ = 6κΔφ_r`.
- `w_κ(A, Y) := (36κ²(det A)² − Y²)₊1{A < 0}`.

**Facts used.**
- (F1) `det K_M = −6kΔ + rY_r + R_M` and `det K_S = 6kΔ + rY_r + R_S`, with `|R_i| ≤ Cr²(1 + k)𝒩_r^{N₁}`. This is the
  own-jet form of #198 (3.1): `F_r`'s own transverse Hessian `A` replaces `A_0`, and `𝒩_r` replaces #191's `T`. It holds
  pathwise for every `0 < r ≤ r_0^*` and `k > 0`, not only in this section's range. Indeed, #191 Steps 1–3 are pathwise
  Taylor expansions of the pinned function `F_r` about its own jets at `0`, with remainders polynomial in `‖F_r‖_{C⁷}` and
  `k` for every `r ≤ 1`; the coupling enters only once, through `‖A − A_0‖ ≤ r²T` in Step 2, and that step disappears
  when `A` is used (#218 Step F1 records this). Also `r_0^* ≤ r_0^{[R]} ≤ 1` ([R] §2).
- (F2) `|r^{−2}F_d(K_M)F_{d−1}(K_S) − w_κ(A, Y_r)| ≤ Cr(1 + κ)𝒩_r^N`. This is #218 (C.2) with `(A, 𝒩_r)` in place of
  `(A_0, T)`. Its case analysis (Step C1) uses only (F1) and `‖A_i − A‖ ≤ (r/2)‖F_r‖_{C³} ≤ r𝒩_r`.
- (F3) Given `J″`, `f₄` is Gaussian under `Q`, with variance in `[c, C]` and mean `μ`, `|μ| ≤ C(P + |J″|)`. Indeed,
  under `Q` the vector `J′` is Gaussian; `Cov_Q(J′)` is uniformly invertible on `(0, r_0^*]` (#218 Step F1); and
  `E_QJ′ = Cov(J′, U_r)Σ_r^{−1}v_r`, so `|E_QJ′| ≤ C|v_r| ≤ CP` by [R] (R2)–(R3). `Var_Q(f₄ | J″)` is a Schur complement
  in `Cov_Q(J′)`, hence at least `λ_min(Cov_Q J′) ≥ c` and at most `Var_Q(f₄) ≤ C`. The conditional mean is
  `E_Qf₄ + Cov_Q(f₄, J″)Cov_Q(J″)^{−1}(J″ − E_QJ″)`, with coefficients bounded by the same uniform invertibility. (#207
  Lemma CU.5 proves the density bound for small `r`, given its own vector of free jets of order `≤ 8`; the argument here
  covers all of `(0, r_0^*]`.) So the conditional density is at most a constant `C₀`, and since the Gaussian factor
  absorbs polynomial weights, for every `J″`-measurable interval `I` and `p ≥ 0`

      E_Q[(1 + |f₄|)^p 1{f₄ ∈ I} | J″] ≤ C_p (P + |J″|)^p |I|.                                            (2.1)
- (F4) #218 (1.2) with `J₀ = J′`: `E_Q[𝒩_r^p | J′] ≤ C_p(P + |J′|)^p`.
- (F5) Given `J‴`, `A` is Gaussian under `Q`, with covariance between `cI` and `CI` (a Schur complement in `Cov_Q(J′)`,
  as in (F3)) and mean `μ_A`, `|μ_A| ≤ C(P + |J‴|)`. So #218 Lemma D applies conditionally:

      E_Q[(1 + ‖A‖)^n 1{|λ_max(A)| < ε} | J‴] ≤ C (P + |J‴|)^{n′} ε,    n′ = n + m(m − 1)/2.                  (2.2)
- (F6) #218 Step F3: under `Q`, `J′ ~ N(μ_r, Γ_r)`, and under the contact law at `v_0(b, k)`, `J′ ~ N(μ_0, Γ_0)`, with
  `|μ_r − μ_0| ≤ Cr²P`, `‖Γ_r − Γ_0‖ ≤ Cr²` and `Γ_r, Γ_0 ≥ cI`.
- (F7) The parity factorization ([P] §15; #218 Step C3). Under the contact law at `v_0(b, k)`, the even free jets
  (among them `A` and `f₄`) are independent of the odd ones (among them `γ`). The law of the even jets does not depend on
  `k`. The odd jets are `N(12kw, Σ_o)`, with `w` and `Σ_o` independent of `k`. Finally
  `π_0(v_0(b, k)) = p_e(b, 0, 0)p_o(0, 12k, 0)`, where `p_o` is a centred Gaussian density.

**Lemma G (two Gaussian comparisons).** Fix `n`, `p` and `0 < c_G ≤ C_G`.
- (a) Let `J ~ N(μ, Γ)` and `J̃ ~ N(μ̃, Γ̃)` on `R^n`, with `c_GI ≤ Γ, Γ̃ ≤ C_GI`, and let `G` be Borel with
  `|G(j)| ≤ H(1 + |j|)^p`. Then
  `|E G(J̃) − E G(J)| ≤ CH(1 + |μ| + |μ̃|)^{p+2}(|μ̃ − μ| + ‖Γ̃ − Γ‖)`.
- (b) Let `E` and `O` be independent, with `O ~ N(s, Σ)` on `R^{n_o}`, `c_GI ≤ Σ ≤ C_GI` and `|s| ≤ s₀`. Let
  `G(e, −o) = G(e, o)` and `|G(e, o)| ≤ H(e)(1 + |o|)^p`, and assume `E[H(E)] < ∞`. Then
  `|E G(E, O) − E G(E, O₀)| ≤ C|s|²E[H(E)]`, where `O₀ ~ N(0, Σ)` is independent of `E` and `C` depends also on `s₀`.
  (v1.1, after the nonauthor Slice B review's OA-220-B-01: without `E[H(E)] < ∞` both expectations can be infinite,
  e.g. `G(e, o) = H(e) = e` with `E` nonintegrable; the integrability is also what justifies differentiating under
  the integral below.)

*Proof.*
- (a) Interpolate `(μ_t, Γ_t)` linearly; then `c_GI ≤ Γ_t ≤ C_GI`. The Gaussian density satisfies
  `∂_t log p_t(j) = (j − μ_t)ᵀΓ_t^{−1}δμ + ½(j − μ_t)ᵀΓ_t^{−1}δΓΓ_t^{−1}(j − μ_t) − ½tr(Γ_t^{−1}δΓ)`, so
  `|∂_tp_t| ≤ C(|δμ| + ‖δΓ‖)(1 + |j − μ_t|²)p_t`. Integrate `|G||∂_tp_t|` over `j` and `t ∈ [0, 1]`.
- (b) `h(s) := E G(E, O_s)` is smooth, and even in `s`: substitute `o ↦ −o` and use `G(e, −o) = G(e, o)` and the
  evenness of the centred density. So `∇h(0) = 0`, and `|h(s) − h(0)| ≤ ½|s|²sup_{|t|≤s₀}‖∇²h(t)‖`. Differentiating the
  density twice gives `‖∇²h(t)‖ ≤ CE[H(E)]` for `|t| ≤ s₀`. ∎

(b) differentiates the Gaussian density, not `G`: no regularity of `G` is needed, which matters because `loss_κ` jumps at
`|Y| = 2κ|Δ|`.

**Lemma CE (the elder cusp kernel with a rate).** There are `r₂ > 0` and `C, c, N` such that for `0 < r ≤ r₂`,
`b ∈ R`, `u ∈ S^{d−1}` and `κ > 0` with `κr ≤ 1`,

    |r^{−2}(A_r^{eld} − A_0)(b, κr, u) − (𝒜^{eld} − 𝒜^{con})(b, κ, u)| ≤ C r (1 + κ)² (1 + |b|)^N e^{−cb²}.      (CE.1)

This is #218's (C.1) for the elder kernel, with the same rate.

*Proof.* Take `r₂ := min(r_0^*, 1/2, r_Q)`. (v1 also required `r₂ ≤` the radius of #207 Lemma CU.5, for Lemma B′; v1.1
does not use Lemma CU.5.)

*Step E1 (pathwise comparison).* Put `G(J′) := w_κ(A, Y_r)1{|φ_r| < 1/3}`. Since
`r^{−2}F_dF_{d−1}e − G = (r^{−2}F_dF_{d−1} − w_κ)e + w_κ(e − 1{|φ_r| < 1/3})`, (F2) bounds the first term by
`Cr(1 + κ)𝒩_r^N`. Consider the second term on `{w_κ > 0}`.
- If the pair is not typed, `F_dF_{d−1} = 0`, and (F2) gives `w_κ ≤ Cr(1 + κ)𝒩_r^N`.
- If it is typed and Lemma Q's hypotheses (Q1)–(Q4) hold for `f = F_r` with `𝒩 = 𝒩_r`, then
  `e = 1{|φ_r| < 1/3}` by (1.3), and the term vanishes.

Let `𝔅` be the event that (Q1)–(Q4) fail. Then

    |r^{−2}F_d(K_M)F_{d−1}(K_S)e − G(J′)| ≤ 2Cr(1 + κ)𝒩_r^N + w_κ(A, Y_r)1_𝔅.                                 (2.3)

*Step E2 (the wrong decisions have small weight).* `E_Q[w_κ(A, Y_r)1_𝔅] ≤ Cr(1 + κ)²P^N`.
- *The bad event.* The conditions of Lemma Q on `r` alone hold because `r ≤ r₂ ≤ r_Q`: `r ≤ 1/10` and
  `6r + 10r² ≤ L/8`. The others are monotone in `𝒩` and `λ`. With `R ≤ 5(1 + Γ) + 3((κ + 1)/λ)^{1/2}`, they reduce as
  follows (write `𝒩` for `𝒩_r`).
  - (Q1), first part: it holds if `3𝒩r`, `5𝒩r²(1 + Γ)` and `3𝒩r²((κ + 1)/λ)^{1/2}` are each `≤ λ/6`; this follows
    from `λ ≥ 18𝒩r`, `λ ≥ 60𝒩r²`, `λ² ≥ 60𝒩r²|γ|` and `λ^{3/2} ≥ 18𝒩r²(κ + 1)^{1/2}`. The last follows from
    `λ ≥ 18^{2/3}2^{1/3}𝒩r`, as `r(κ + 1) ≤ 2`.
  - (Q1), second part: given `6r + 10r² ≤ L/8`, it holds if `10r²|γ|/λ ≤ L/16` and `6r²((κ + 1)/λ)^{1/2} ≤ L/16`, which
    follow from `λ ≥ 160r²|γ|/L` and `λ ≥ (96/L)²r⁴(κ + 1)`.
  - (Q2): `5r(1 + Γ) ≤ 1` holds if `λ ≥ 10r|γ|`; `8C₁𝒩r(1 + 5Γ) ≤ λ` holds if `λ ≥ 16C₁𝒩r` and `λ² ≥ 80C₁𝒩r|γ|`.
  - (Q3): `ε* ≤ κ/4` holds if `κ ≥ 1280C₁𝒩r` and `λ² ≥ 1280C₁𝒩r|γ|²/κ`, by `(1 + Γ)² ≤ 2(1 + Γ²)`.

  Since `κr ≤ 1 ≤ 𝒩` gives `r²|γ| ≤ r|γ| ≤ |γ|(𝒩r/κ)^{1/2}`, and `r⁴(κ + 1) ≤ 2r`, all of these hold whenever
  `κ ≥ C₂𝒩_r r` and `λ ≥ λ₂(𝒩_r)`, where `C₂ = C₂(d, L)` and

      λ₂(𝒩) := C₂[𝒩r + (𝒩r|γ|)^{1/2} + |γ|(𝒩r/κ)^{1/2}].

  So `𝔅 ⊂ 𝔅_λ ∪ 𝔅_κ ∪ 𝔅_4 ∪ 𝔅_5`, with `𝔅_λ := {λ < λ₂(𝒩_r)}`, `𝔅_κ := {κ < C₂𝒩_r r}`,
  `𝔅_4 := {||φ_r| − 1/3| ≤ 2ε*/(3κ)}` and `𝔅_5 := {|φ_r| > 1}`.
- *The common reduction.* `w_κ(A, Y_r) ≤ 36κ²Δ²1{A < 0, |Y_r| < 6κ|Δ|}`. `Y_r` is affine in `f₄` with slope `Δ/12`
  and `J″`-measurable intercept. So `{|Y_r| < 6κ|Δ|}` is `{f₄ ∈ I_typ}` for a `J″`-measurable interval `I_typ` of length `144κ`.
  The thresholds of `𝔅_λ`, `𝔅_κ` and `𝔅_4` depend on `𝒩_r`. On `{𝒩_r ∈ [2^j, 2^{j+1})}`, replace `𝒩_r` by `2^{j+1}`,
  bound `1{𝒩_r ≥ 2^j}` by (F4), then integrate `f₄` by (2.1). This gives, for each `j`, a factor
  `C_p2^{−jp}(P + |J″|)^p`. The sum over `j` converges for `p` large.
- *`𝔅_λ`.* Integrating `f₄` over `I_typ` gives a factor `min(1, 144C₀κ)`. On `{λ < λ₂}`, `Δ² ≤ λ₂²‖A‖^{2m−2}`, and (2.2),
  applied given `J‴` (`λ₂` depends on `|γ|`, which lies in `J‴`), gives a factor `λ₂`. So the contribution is at most
  `Cκ²min(1, κ)Σ_j2^{−jp}E[λ₂(2^{j+1})³(P + |J‴|)^{N}]` (`N` a generic exponent). The three terms of `λ₂³` contribute
  `κ²min(1, κ)(r³ + r^{3/2} + (r/κ)^{3/2})P^N ≤ Cr(1 + κ)²P^N`, using `κr ≤ 1` and `r ≤ 1`.
- *`𝔅_κ`.* `P(𝒩_r > κ/(C₂r) | J′) ≤ min(1, C_3(r/κ)³(P + |J′|)³)`, so the contribution is at most
  `Cκ²min(1, κ)min(1, (r/κ)³)P^N ≤ Cr³P^N`.
- *`𝔅_4`.* This is `f₄` in two `J″`-measurable intervals of total length `192ε*`, with
  `ε* = 80C₁𝒩_r r(1 + Γ)²`. With `Δ²(1 + Γ)² ≤ 2Δ² + 2|γ|²‖A‖^{2m−2}` (as `Δ² ≤ λ²‖A‖^{2m−2}`), the contribution is
  `≤ Crκ²P^N`.
- *`𝔅_5` (on `{w_κ > 0}`).* `|Y_r| < 6κ|Δ| < |Y′|`, so `6κ|Δ| − |Y_r| < τ := 3k|tr(adj(A)B)|`, and
  `w_κ ≤ 12κ|Δ|τ`. Also `|Y′|` lies in `(6κ|Δ|, 6κ|Δ| + τ)`, which puts `f₄` in two intervals of total length
  `24τ/|Δ|`. The contribution is `≤ 288C₀κE[τ²(P + |J″|)^p] ≤ Cκ³r²P^N ≤ Cκ²rP^N`.

*Step E3 (removing the `k`-term).* `G₀(J′) := w_κ^{eld}(A, Y′)` equals `w_κ(A, Y′)1{|φ_r| < 1/3}`, because
`|φ_r| < 1/3 ⟺ |Y′| < 2κ|Δ|`. `w_κ` is Lipschitz in `Y` with constant `12κ|Δ|` (#218 Step C2; checker T3 there). Hence
`|G − G₀| ≤ 12κ|Δ|·3k|tr(adj(A)B)| ≤ Cκ²r‖A‖^{N}|B|`, and `E_Q|G − G₀| ≤ Cκ²rP^N`.

*Step E4 (from `Q` to the contact law at `v_0(b, k)`).* `|G₀| ≤ 36κ²|J′|^{2m}`. By (F6) and Lemma G (a),
`|E_Q[G₀] − E_{v_0(b,k)}[G₀]| ≤ Cκ²r²P^N`.

*Step E5 (densities).* By [R] (R5) as used in #218 Step C3, `|π_r(v_r) − π_0(v_0(b, k))| ≤ Cr²P²e^{−c(b²+k²)}`. Also
`E_Q[r^{−2}F_dF_{d−1}e] ≤ C(1 + κ)²P^N` by the sign window. Hence, by Steps E1–E4,

    r^{−2}A_r^{eld}(b, κr, u) = 12π_0(v_0(b, k))E_{v_0(b,k)}[w_κ^{eld}(A, Y)] + O(r(1 + κ)²P^Ne^{−c(b²+k²)}).

`r^{−2}A_0(b, κr, u) = 12π_0(v_0(b, k))E_{v_0(b,k)}[36κ²Δ²1{A < 0}]` exactly (#218 Step C3). Subtracting,

    r^{−2}(A_r^{eld} − A_0)(b, κr, u) = −12π_0(v_0(b, k))E_{v_0(b,k)}[loss_κ(A, Y)] + O(r(1 + κ)²P^Ne^{−c(b²+k²)}).   (2.4)

*Step E6 (the target `v_0(b, k) → v_0(b, 0)`).* `loss_κ` depends on the even jets `(A, f₄)` and on the odd jet `γ`
only through `γᵀadj(A)γ`, so it is even in the odd jets. Also `0 ≤ loss_κ ≤ 9Y²`: on `{|Y| ≥ 2κ|Δ|}`,
`36κ²Δ² ≤ 9Y²`. So Lemma G (b) applies with `E = (A, f₄)`, `O` the odd jets and
`H(A, f₄) = C(1 + |f₄|)²(1 + ‖A‖)^{2m}` (the odd-jet factor of `Y²` is absorbed in `(1 + |o|)^p`, `p = 4`), and
`E[H] ≤ C(1 + |b|)^N` under the contact law. By (F7) and Lemma G (b) with `s = 12kw` (`|s| ≤ 12|w|`, as `k ≤ 1`),
`|E_{v_0(b,k)}[loss_κ] − E_{v_0(b,0)}[loss_κ]| ≤ Ck²(1 + |b|)^N`, with no growth in `κ`. And
`p_o(0, 12k, 0) = p_o(0, 0, 0)(1 + O(k²))`. So the right side of (2.4) is
`(𝒜^{eld} − 𝒜^{con})(b, κ, u) + O(k²(1 + |b|)^Ne^{−cb²}) + O(r(1 + κ)²P^Ne^{−c(b²+k²)})`. Since `k² = κ²r² ≤ r(1 + κ)²`
and `P^Ne^{−ck²} ≤ C(1 + |b|)^N`, this is (CE.1). ∎

(The coupling `(F_r, F_0)` is not used in this proof. Every pathwise statement concerns `F_r` alone, and the passage to
the contact law is Lemma G (a) applied to the free-jet laws.)

## 3. The overlap and the intermediate separations

**Lemma O′ (elder overlap).** For `κ ≥ 1`,

    0 ≤ (𝒜^{cand} − 𝒜^{eld})(b, κ, u) ≤ C κ^{−1} (1 + |b|)^N e^{−cb²}.                                      (O′.1)

Consequently, with #218 Lemma O, `|(𝒜^{eld} − 𝒜^{con})(b, κ, u) − A₂(b, 0, u)| ≤ Cκ^{−1}(1 + |b|)^Ne^{−cb²}`.

*Proof.* `𝒜^{cand} − 𝒜^{eld} = 12π_0E_0[(36κ²Δ² − Y²)1{A < 0, 2κ|Δ| ≤ |Y| < 6κ|Δ|} | b]`. On this event
`36κ²Δ² ≤ 9Y²` and `|Δ| ≤ |Y|/(2κ)`. So the difference is at most `108π_0E_0[Y²1{|Δ| ≤ |Y|/(2κ)} | b]`, and the dyadic
argument of #218 Lemma O (Lemma D for `det A`, with the Gaussian tails of `Y` given `A`) bounds this by
`Cκ^{−1}(1 + |b|)^Ne^{−cb²}`. ∎

The next two lemmas replace v1's Lemma B′. They hold for every separation `0 < r ≤ r_0^*`, not only for `r ≤ r₂`. Their
only inputs from §2 are `𝒩_r := 1 + k + ‖F_r‖_{C⁹}`, `Δ = det A` and (F1), the own-jet form of #198 (3.1), which holds
for every `r ≤ r_0^*` (see (F1)).

**Lemma H (the rescaled Hessian at `M`).** Let `0 < r ≤ r_0^*`, `b ∈ R` and `0 < k ≤ r` (so `κ = k/r ≤ 1`), and let
`f = F_r` under `Q`. In the frame `(u, Θ)` put `Λ_r := diag(r, 1, …, 1)`, `H_M := D²f(M)` and
`H̃ := Λ_r^{−1}H_MΛ_r^{−1}`, so that

    H̃_uu = r^{−2}∂_u²f(M),    H̃_uΘ = r^{−1}∂_u∇_Θf(M),    H̃_ΘΘ = D_Θ²f(M),    det H_M = r² det H̃.

(`Λ_r` is not [R] §4's `D_r = diag(√r, I)`, which defines `K_M = D_r^{−1}H_MD_r^{−1}`; the two are related by
`H̃ = diag(r^{−1/2}, I) K_M diag(r^{−1/2}, I)`.)

There are `c > 0` and `C, C_p < ∞`, depending only on `d`, `L` (and `p`), such that:
- (a) under `Q`, `H̃` is a Gaussian random element of `Sym(d)` with `cI ≤ Cov_Q(H̃) ≤ CI` and `|E_QH̃| ≤ CP`, so #218
  Lemma D applies to `G = H̃` with `|μ| ≤ CP`;
- (b) `E_Q[𝒩_r^p | H̃] ≤ C_p(P + |H̃|)^p` for every `p ≥ 1`.

*Proof.* *The exact form.* Put `g(t) := f(M + tu)` and `h(t) := ∇_Θf(M + tu)` for `0 ≤ t ≤ r`. Taylor's formula with
integral remainder gives, for every `C⁴` function,

    r²g″(0)/6 = [g(r) − g(0) − rg′(0)] − (r/3)[g′(r) − g′(0)] + (1/6)∫_0^r t(r − t)² g⁗(t) dt,
    rh′(0) = [h(r) − h(0)] − ∫_0^r (r − t) h″(t) dt.

Under `Q` the pins give `g(0) = b`, `g(r) = b − kr³`, `g′(0) = g′(r) = 0` and `h(0) = h(r) = 0`. So the bracketed pin
combinations equal `−kr³` and `0`, and with `t = rs`

    H̃ = m_κ + 𝒢_r(f),    m_κ := −6κ e_u e_uᵀ,
    𝒢_r(f) := ( ∫_0^1 s(1 − s)² ∂_u⁴f(M + rsu) ds ;  −∫_0^1 (1 − s) ∂_u²∇_Θf(M + rsu) ds ;  D_Θ²f(M) ),              (H.1)

listing the `uu`, `uΘ` and `ΘΘ` blocks. `𝒢_r` is a linear map on `C⁴` functions with `|𝒢_r(g)| ≤ C‖g‖_{C⁴}`. It is
defined also at `r = 0`, where `𝒢_0(g) = (∂_u⁴g(0)/12, −∂_u²∇_Θg(0)/2, D_Θ²g(0))`; for the cusp jets this is
`(f₄/12, −γ/2, A)`. Control X9 checks (H.1) exactly on pinned polynomial fields.

*(a).* Under `Q`, `f` is the Gaussian field `F` conditioned on its pin rows ([R] (R2)–(R3)). Let `U_r = T_rO_r` be the
rescaled pin rows of [P] (3.1) (`U0`–`U3` and `V_{j0}`, `V_{j1}`), with target
`v_r = (b − kr³/2, −kr², 0, 12k, 0, …, 0)` ([P] (3.3)); as `r → 0` they converge to the six pinned jets
`(F, ∂_uF, ∂_u²F, ∂_u³F, ∇_ΘF, ∂_u∇_ΘF)` at `0`. Then `Cov_Q(H̃) = Cov(𝒢_r(F) | U_r)`, the Schur complement of `U_r` in
the Gram matrix `Γ_r` of `(𝒢_r(F), U_r)`.
- *Continuity.* Every entry of `(𝒢_r(F), U_r)` is an integral of some `∂^αF(M + rsu)`, `|α| ≤ 4`, against a fixed finite
  measure on `s ∈ [0, 1]` (a density or an endpoint mass), independent of `r`; by Taylor's formula this holds for the
  difference rows of [P] (3.1) too. So each entry of `Γ_r` has the form
  `∫∫ ±∂^{α+β}K_L(r(s − s′)u) μ_i(ds) μ_j(ds′)`, with `K_L` the smooth covariance of `F`. This is continuous on the
  compact set `[0, r_0^*] × {frames}`, including at `r = 0`.
- *`r > 0`.* The map from `(D²F(M), O_r)` to `(𝒢_r(F), U_r)` is block-triangular with invertible diagonal blocks:
  `𝒢_r(F) = Λ_r^{−1}D²F(M)Λ_r^{−1} − (a linear function of the pins)` by the two identities above, read for an
  arbitrary `C⁴` function, and `U_r = T_rO_r` with `|det T_r| = 12r^{−(d+3)}` ([P] (3.2)). So `(𝒢_r(F), U_r)` is an
  invertible linear image of `(D²F(M), F(M), F(S), ∇F(M), ∇F(S))`. These are distinct derivative evaluation
  functionals at the two distinct sites `M ≠ S` (`r ≤ r_0^* < L`), linearly independent by [P] §2: "Any finite list of
  distinct derivative evaluation functionals at distinct sites is linearly independent."
- *`r = 0`.* `(𝒢_0(F), U_0)` is an invertible image of `∂_u⁴F(0)`, `∂_u²∇_ΘF(0)` and `D_Θ²F(0)` together with the six
  pinned jets. These are distinct jets at one point in the frame `(u, Θ)`, independent by [P] §2: "At one site in a
  rotated frame the same assertion also follows …".

So `Γ_r` is invertible at every point of the compact set, hence `Γ_r ≥ cI` uniformly. Therefore
`Cov_Q(H̃) ≥ λ_min(Γ_r)I ≥ cI` (the inverse of the Schur complement is a block of `Γ_r^{−1}`), and
`Cov_Q(H̃) ≤ Cov(𝒢_r(F)) ≤ CI`.

For the mean, `E_QH̃ = m_κ + Cov(𝒢_r(F), U_r)Cov(U_r)^{−1}v_r`, with `|v_r| ≤ |b| + 14k`. The regression coefficient is
bounded by the same uniform invertibility, and `|m_κ| = 6κ ≤ 6`. So `|E_QH̃| ≤ CP`; this is the computation of (F3)
with `𝒢_r` in place of `J′`.

*(b).* Conditioning `Q` on `H̃` is conditioning `F` on `(𝒢_r(F), U_r) = (H̃ − m_κ, v_r)`, whose Gram matrix `Γ_r` is
uniformly invertible by (a).
- The conditional mean of `F` is the regression on these values. Its `C⁹` norm is `≤ C(P + |H̃|)`, since `Γ_r^{−1}` is
  bounded, the covariances of `F(·)` with `𝒢_r(F)` and `U_r` have bounded `C⁹` norms, and `|m_κ| ≤ 6`.
- The conditional covariance is at most `Cov F`, so by Anderson's inequality the conditional moments of the centred
  part's `C⁹` norm are at most those of `F`.

This is the argument (not the statement) of #218 (1.2), applied to the conditioning vector `(𝒢_r(F), U_r)`; no
coupling is needed, because `𝒩_r` involves `F_r` only. (Jensen's inequality can replace Anderson's: write the centred
field as `g + h` with `h` centred and independent of `g`; then `E‖g‖^p ≤ E‖g + h‖^p`.) Since
`𝒩_r = 1 + k + ‖F_r‖_{C⁹}` and `k ≤ P`, (b) follows. ∎

**Lemma S′ (the elder weight through the rescaled Hessian).** For `0 < r ≤ r_0^*`, `b ∈ R` and `0 < k ≤ r`, with `ℓ = kr³` and
`κ = k/r ≤ 1`,

    E_Q[(W_r/r²) e] ≤ C ℓ^{2/3} r^{−2} (κ + r) P^N.                                                        (S′.1)

*Proof.*
- *The barrier, rescaled.* Fix a realisation in `{W_r > 0} ∩ {e = 1}`. Then `H_M < 0`, so `H̃ < 0`.
  - #198 (1.2) gives `λ_min(−H_M) ≤ (ℓK²/c_L)^{1/3}`, where `K = 1 + ‖D²f‖_∞ + ‖D³f‖_∞ ≤ C_K𝒩_r`.
  - Since `−H_M = Λ_r(−H̃)Λ_r` and `|Λ_rv| ≥ r|v|` (`r ≤ 1`), `vᵀ(−H_M)v ≥ r²λ_min(−H̃)|v|²`. So
    `λ_min(−H_M) ≥ r²λ_min(−H̃)` (control X8).

  Hence

      0 < λ_min(−H̃) ≤ ε(𝒩_r),        ε(t) := C₃ ℓ^{1/3} r^{−2} t^{2/3},    C₃ := (C_K²/c_L)^{1/3}.             (S′.2)

- *The weight.* By [R] §4's dictionary, `|det K_M| = |det H_M|/r = r|det H̃| ≤ rλ_min(−H̃)‖H̃‖^{d−1}`. The pair is
  typed, so the two determinants have opposite signs, and the sign window (#198 §3) applied to (F1) gives
  `|det K_S| ≤ 12k|Δ| + 2max_i|R_i| ≤ Cr(κ + r)𝒩_r^{N₂}`, using `|Δ| ≤ 𝒩_r^m` and `1 + k ≤ 𝒩_r`. Since
  `{H̃ < 0, λ_min(−H̃) ≤ ε} ⊂ {|λ_max(H̃)| ≤ ε}`, everywhere

      (W_r/r²) e ≤ C r²(κ + r) ε(𝒩_r) ‖H̃‖^{d−1} 𝒩_r^{N₂} 1{|λ_max(H̃)| ≤ ε(𝒩_r)}.

- *Dyadic layers in `𝒩_r`.* On `{𝒩_r ∈ [2^j, 2^{j+1})}`, `ε(𝒩_r) ≤ ε_j := ε(2^{j+1})`. Condition on `H̃`, and bound
  `P_Q(𝒩_r ≥ 2^j | H̃) ≤ C_p2^{−jp}(P + |H̃|)^p` by Lemma H (b). Then

      E_Q[(W_r/r²) e] ≤ C r²(κ + r) Σ_{j≥0} 2^{(j+1)N₂ − jp} ε_j E_Q[‖H̃‖^{d−1}(P + |H̃|)^p 1{|λ_max(H̃)| < 2ε_j}].

  By Lemma H (a), #218 Lemma D (first bound, for `d × d` matrices, with `n = d − 1 + p` and `n′ := n + d(d − 1)/2`)
  bounds the expectation by `CP^{p+n′}ε_j`. So the `j`-th term is at most `C2^{j(N₂ + 4/3 − p)}P^Nℓ^{2/3}r^{−4}`. Take `p = N₂ + 2`; the series
  converges and gives (S′.1). ∎

**How (S′.1) compares with #198 (B.1).** (B.1) is `E_Q[(W_r/r²)e] ≤ Cℓ^{1/3}r^{−1}(k + r)P^N`. The ratio of (S′.1) to
(B.1) is `ℓ^{1/3}r^{−2}(k + r²)/(k + r)`. With `k = ℓr^{−3} ≤ r`, this is `≍ ℓ^{4/3}r^{−6}` for `r ≤ ℓ^{1/5}` and
`≍ ℓ^{1/3}r^{−1}` for `r ≥ ℓ^{1/5}`, so (S′.1) is the sharper bound once `r ≫ ℓ^{2/9}`, in particular on all of
`[ℓ^{2/15}, r_0^*]`.
- The gain is the second factor `ε`. The barrier puts `H̃` within `ε` of the singular set, and Lemma H makes that event
  cost `ε` in probability (Lemma D).
- The size `ε ≍ ℓ^{1/3}r^{−2}` reflects the pins: they make `∂_u²f(M)` of order `r²`. The `uu`-entry of `H̃` tends to
  `f₄/12 − 6κ` as `r → 0`.

Lemma H is the lower bound on the conditional variance of the axial curvature under the pins, with `f₄` in the
limiting rows, that #198 Remark 1 asks for. Lemma S′ is the resulting refinement of #198 Lemma B, by the spectral
mechanism of #187 §3. At a fixed separation, (S′.1) is `O(ℓ^{2/3})`, the order of #187's Theorem F.

## 4. Proof of Theorem E3 and of Corollary E3′

*Setup.* As in #218 §4, put `ρ_f := ℓ^{1/4 + 1/44}` and `ρ_c := ℓ^{1/4 − 1/36} = ℓ^{2/9}`, with `s_f := ρ_fℓ^{−1/4} = ℓ^{1/44}`
and `s_c := ρ_cℓ^{−1/4} = ℓ^{−1/36}`; also put `a := ℓ^{2/15}`. Let `r₂` be as in Lemma CE, and take `ℓ` so small that
`ρ_c ≤ r₂`, `a < r_0^*` and `ℓρ_f^{−3} ≤ 1`. Then `ρ_f < ρ_c < a`, since `3/11 > 2/9 > 2/15`. By the near/far identity
at `r_0 = r_0^*` (§0),

    ν_eld(ℓ) − cℓ^{−1/3} = F^{eld} + K^{eld} + I^{eld} − J₄ + ν_eld^{far,r_0^*}(ℓ),

with all integrands at `(b, ℓ/r³, u)`, inner integrals `db dσ(u)`, and
- `F^{eld} := ∫_0^{ρ_f}∫∫ r^{−2}(A_r^{eld} − A_0)`;
- `K^{eld} := ∫_{ρ_f}^{ρ_c}∫∫ r^{−2}(A_r^{eld} − A_0)`;
- `I^{eld} := ∫_{ρ_c}^{r_0^*}∫∫ r^{−2}A_r^{eld} ≥ 0`;
- `J₄ := ∫_{ρ_c}^∞∫∫ r^{−2}A_0 ≥ 0`.

*`F^{eld}`: the fold region.* Write `A_r^{eld} = A_r − A_r^{rej}`, `A_r^{rej} := 12π_r(v_r)E_Q[(W_r/r²)(1 − e)]`.
- The candidate part `∫_0^{ρ_f}∫∫r^{−2}(A_r − A_0)` is #218's `F`:
  `c₂ℓ^{1/3} + ρ_f∫∫A₂(b, 0, u) + O(ρ_f² + ρ_f⁵/ℓ + ℓρ_f^{−2})` (#218 §4, from Lemma F).
- For `r ≤ ρ_f < ℓ^{1/4}`, `k = ℓ/r³ > r`, and `r ≤ r₂ ≤ r_0^* ≤ r_0^{[K]}`. So [C7-K] (K2), with `1 − e ≤ 1_{G_r^c}` ([C7-K] §4) and (R5), gives
  `0 ≤ r^{−2}A_r^{rej} ≤ Cr^{−2}(r³/k)P^Ne^{−c(b²+k²)} ≤ C(r⁴/ℓ)(1 + |b|)^Ne^{−cb²}`. Integrated, this is `O(ρ_f⁵/ℓ)`.

So `F^{eld} = c₂ℓ^{1/3} + ρ_f∫∫A₂(b, 0, u) + O(ρ_f² + ρ_f⁵/ℓ + ℓρ_f^{−2})`.

*`K^{eld}`: the cusp region.* Here `k ≤ ℓρ_f^{−3} ≤ 1` and `r ≤ ρ_c ≤ r₂`.
- By (CE.1) with `κ = ℓ/r⁴`, the error is `∫_{ρ_f}^{ρ_c}Cr(1 + ℓr^{−4})²dr ≤ C(ρ_c² + ℓρ_f^{−2} + ℓ²ρ_f^{−6})`.
- With `r = sℓ^{1/4}`, the main term is `ℓ^{1/4}∫∫∫_{s_f}^{s_c}(𝒜^{eld} − 𝒜^{con})(b, s^{−4}, u) ds db dσ`.
- *Upper tail.* `0 ≤ 𝒜^{con} − 𝒜^{eld} ≤ 𝒜^{con} ≤ Cs^{−8}(1 + |b|)^Ne^{−cb²}`, so the part over `s > s_c` is `O(s_c^{−7})`.
- *Lower end.* By Lemma O′ and #218 Lemma O, `∫_0^{s_f}(𝒜^{eld} − 𝒜^{con})(b, s^{−4}, u) ds = s_fA₂(b, 0, u) + O(s_f⁵)`, since `s ≤ s_f < 1` means `κ = s^{−4} ≥ 1`.
- With (0.2),
  `K^{eld} = c₁ℓ^{1/4} − ρ_f∫∫A₂(b, 0, u) + O(ℓ^{1/4}s_f⁵ + ℓ^{1/4}s_c^{−7} + ρ_c² + ℓρ_f^{−2} + ℓ²ρ_f^{−6})`.

*The overlap cancels.* The terms `±ρ_f∫∫A₂(b, 0, u)` cancel, and `ℓ^{1/4}s_f⁵ = ρ_f⁵/ℓ`, `ℓ^{1/4}s_c^{−7} = ℓ²ρ_c^{−7}`. The
error terms are those of #218 §4: by #218's ledger (checker T1 there; X1 here), every exponent is `≥ 4/11`. So

    F^{eld} + K^{eld} = c₁ℓ^{1/4} + c₂ℓ^{1/3} + O(ℓ^{4/11}).                                              (4.1)

*`J₄`.* `A_0 ≤ k²H` gives `0 ≤ J₄ ≤ Cℓ²ρ_c^{−7} = Cℓ^{4/9}`.

*`I^{eld}`: intermediate separations.* On `[ρ_c, r_0^*]`, `k = ℓ/r³ ≤ ℓρ_c^{−3} = ℓ^{1/3} ≤ 1`. Split at `a = ℓ^{2/15}`.
- *On `[ρ_c, a]`.* `e ≤ 1`, #198 (W.1) and (R5) give
  `0 ≤ r^{−2}A_r^{eld} ≤ r^{−2}A_r ≤ Cr^{−2}(k² + r⁴)P^Ne^{−c(b²+k²)} ≤ C(κ² + r²)(1 + |b|)^Ne^{−cb²}`, with
  `κ = ℓr^{−4}`. This integrates to at most `C(ℓ²ρ_c^{−7} + a³) = C(ℓ^{4/9} + ℓ^{2/5})`.
- *On `[a, r_0^*]`.* Here `κ = ℓr^{−4} ≤ ℓ^{7/15} ≤ 1`, i.e. `k ≤ r`. Lemma S′ with (R5) gives
  `0 ≤ r^{−2}A_r^{eld} ≤ Cℓ^{2/3}r^{−4}(κ + r)(1 + |b|)^Ne^{−cb²} = Cℓ^{2/3}(ℓr^{−8} + r^{−3})(1 + |b|)^Ne^{−cb²}`. This
  integrates to at most `C(ℓ^{5/3}a^{−7} + ℓ^{2/3}a^{−2}) = C(ℓ^{11/15} + ℓ^{2/5})`.

So `0 ≤ I^{eld} ≤ Cℓ^{2/5}`. The split point balances `a³` against `ℓ^{2/3}a^{−2}` (control X1).

*Conclusion.* By (4.1), `0 ≤ I^{eld} ≤ Cℓ^{2/5}` and `0 ≤ J₄ ≤ Cℓ^{4/9}`, and since `4/11 < 2/5 < 4/9`,

    ν_eld(ℓ) − cℓ^{−1/3} − c₁ℓ^{1/4} − c₂ℓ^{1/3} − ν_eld^{far,r_0^*}(ℓ) = O(ℓ^{4/11}).

This is (E3.0). The bound `0 ≤ ν_eld^{far,r_0^*}(ℓ) ≤ Cℓ^{1/3}` there is #198 Lemma F′ at `r_0 = r_0^*`
(`r_0^* ≤ L/(4√2) < L/2`).
- (E3.1): `ν_eld^{far,r_0^*} = O(ℓ^{1/3})` absorbs `c₂ℓ^{1/3}` and the `O(ℓ^{4/11})`.
- (E3.2): `ν_eld^{far,r_0^*} ≥ 0`.
- (E3.3): #187's Theorem F at `ρ = r_0^*` (`∈ (0, L/2]`) gives `ν_eld^{far,r_0^*}(ℓ) ≤ C(r_0^*)ℓ^{2/3} ≤ Cℓ^{4/11}` for
  `0 < ℓ ≤ 1`. #187's far density (its (0.1)) at `ρ = r_0^*` is the same integral as #198's (2.1) at `r_0 = r_0^*`: the
  same domain `{dist(0, y) ≥ r_0^*}`, the same `O_y`, `v_{b,ℓ}`, `p_y`, `Q_{y,b,ℓ}` and `W`, and the same Borel mark of
  [P] §8.
- The two equivalences: by (E3.0) the difference of the two sides is `O(ℓ^{4/11})`, which is `O(ℓ^θ)` for `θ ≤ 4/11`
  and `o(ℓ^{1/3})`. ∎

*Proof of Corollary E3′.* `ρ_rej = ν_cand − ν_eld`. Subtracting (E3.0) from #218's (T.1),
`ν_cand(ℓ) = cℓ^{−1/3} + B_{d,L} + I^{cand}ℓ^{1/4} + c₂ℓ^{1/3} + O(ℓ^{4/11})`, gives (E3′.0): the `cℓ^{−1/3}` and
`c₂ℓ^{1/3}` terms cancel. Then (1) follows from `ν_eld^{far,r_0^*} ≤ Cℓ^{1/3}`, (2) from `ν_eld^{far,r_0^*} ≥ 0`, and (3)
from #187's Theorem F at `ρ = r_0^*`. ∎

## 5. Remarks

1. **Why the elder law has the candidate's `c₂`.** The elder rule enters the expansion at three places.
   - At the fold scale the rejected mass is `O(r³/k)` ([C7-K] (K2)). That is the order of the boundary layer, below
     `ℓ^{1/3}` after integration.
   - At the cusp scale the elder rule is the window `|φ| < 1/3` (#207). It changes the `ℓ^{1/4}` coefficient from
     `I^{cand}` to `c₁`, and changes nothing at order `ℓ^{1/3}`: by Lemma O′ the elder and candidate cusp losses have the
     same limit `A₂(b, 0)` as `κ → ∞`, which is what the finite part `c₂` subtracts.
   - At intermediate separations, elder pairs need a soft maximum. On `[ℓ^{2/15}, r_0^*]` Lemma S′ bounds the elder
     weight by `ℓ^{2/3}r^{−2}(κ + r)`; below `ℓ^{2/15}` the unmarked bound (W.1) suffices. Together these separations
     carry only `O(ℓ^{2/5})`.
   - At far separations #187 gives `O(ℓ^{2/3})`, but #187 is an unmerged candidate; (E3.0) keeps that part separate.

   So `c₂` is a fold-scale quantity, as #216 argued formally. (E3.0) makes this a theorem up to the far part, and (E3.3)
   completes it conditional on #187.
2. **The far part is the only remaining input.** (E3.0) reduces the elder third-order law to the far elder density at
   the fixed separation `r_0^*`.
   - v1 needed an `ε`-argument in a cut-off `r₁ ↓ 0`, and a rate would have needed #187's constant quantified as
     `C(ρ) ≤ Cρ^{−p}`. Lemma S′ removes both: below `r_0^*` the elder mass is controlled directly.
   - Any bound `ν_eld^{far,r_0^*}(ℓ) = O(ℓ^θ)` gives the three-term law with remainder `O(ℓ^{min(θ, 4/11)})`. #187's
     Theorem F gives `θ = 2/3`.
   - #188 (unmerged; cited only, not consumed) proposes `ν_eld^{far,ρ}(ℓ) = O(ℓ^N)` for every `N` and every
     `ρ ∈ (0, L/4]`, which would serve equally (`r_0^* ≤ L/(4√2)`).
   - Lemma S′ also sharpens #198 (B.2). For `ℓ^{1/4} ≤ ρ ≤ r_0^*`, the elder density from separations in `[ρ, r_0^*)`
     is `≤ C(ℓ^{2/3}ρ^{−2} + ℓ^{5/3}ρ^{−7})`, against #198's `Cℓ^{1/3}(ρ^{−1} + ℓρ^{−5})`; the new bound is smaller
     when `ρ ≫ ℓ^{2/9}`.
3. **The SIDE24 values and the Monte Carlo (exploration, not certified).** For the Gaussian kernel in `d = 3`, #207 §8
   and #216 give `c = 0.0417759`, `c₁ = −0.2118484` and `c₂ = 0.1612340`. So under (E3.3)
   `ν_{3,24}(ℓ) ≈ cℓ^{−1/3}(1 − 5.0711ℓ^{7/12} + 3.8595ℓ^{2/3})` up to a relative `O(ℓ^{23/33})`; the Gaussian-kernel values agree with
   the `L = 24` torus up to a relative `O(e^{−L²/8})`. The elder-pair row of #216 v1.2 §3 is an exploratory estimate of
   `ν_eld` itself: the exact elder rule by union–find on the full periodized field, `d = 2` at `L = 64` and `d = 3` at
   `L = 16`. On `[10⁻⁴, 10⁻²]` it gives data/law `1.006 ± 0.004` (`χ² = 7.0/11`) in `d = 2` and `1.008 ± 0.010`
   (`χ² = 5.0/11`) in `d = 3` for the three-term law, and rejects the two-term law (`χ² = 714/11` and `175/11`). Its
   adjacent-pair row, which #218 Remark 3 concerns, is not covered here.
4. **Lemma Q is field-independent.** It is a deterministic statement about `C⁵` functions with two pinned critical
   points: the elder window `|φ| < 1/3` of #207 is stable, with explicit margins, as long as
   `𝒩r(1 + |γ|/λ)² ≪ κ||φ| − 1/3|` and `λ ≫ 𝒩r + (𝒩r|γ|)^{1/2}`, with the window inside the torus ((Q1)–(Q4)). #207's
   Proposition CU.3 is its qualitative case. Only §§2–4 use the law of the [P] field.
5. **For the manuscript.** Once #207, #218 and this note are reviewed (#191 and #198 are merged), the abstract can state
   `ν_{3,24}(ℓ) = c_{3,24}ℓ^{−1/3} + c₁ℓ^{1/4} + O(ℓ^{1/3})` with `c₁ < 0` the explicit integral (CU.2). With #187 it can
   state the three-term law with remainder `O(ℓ^{4/11})`. Until then V3 edit E10 is the safe statement.
6. **Consistency.**
   - (E3.0) implies (E3.1), which implies #207's (CU.1) and #198's (0.1).
   - Corollary E3′(1) implies #207's (CU′.2).
   - Corollary E3′(1), with `I^{cand} − c₁ = (1 − 3^{1/4}/2)|c₁| > 0` (#207 (CU′.2)), shows that the rejected density
     approaches `B_{d,L}` from above, by the rejected cusp mass, now with a rate. Corollary E3′(2) bounds the approach
     from above to order `ℓ^{4/11}`. By (E3′.0), the only other `ρ_rej`-correction above order `ℓ^{4/11}` is
     `−ν_eld^{far,r_0^*}`.
   - (S′.1) at a fixed separation is `O(ℓ^{2/3})`, the order of #187's far bound. Accordingly (E3.0) holds with
     `r_0^*` replaced by any fixed `r_0 ∈ (0, r_0^*]`: by Lemma S′ the elder mass from separations in `[r_0, r_0^*)` is
     `O(ℓ^{2/3})`.

## 6. Sources (exact identities in `SOURCES.json`)

| Tag | Path | Role |
|---|---|---|
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`) | (R2)–(R5): pin covariance, regression, moments, pin densities; §4 scaled Hessians — consumed |
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`) | §2 finite-jet rank (also for Lemma H), §8 maximin and elder mark, §§9–10 as [E2] (the near/far identity), §15 parity factorization and (15.2) — consumed |
| [E1] | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` (blob `213594d6`) | reading rule |
| [E2] | `reviews/d1_section9_borel_repair_20260925/REPAIR.md` (blob `fe9b9ce4`) | §9 replacement |
| [REC] | `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` (blob `75da2597`) | reading rule |
| [C7-K] | `frontiers/c7_total_bounded_20260929/PROOF.md` (blob `28748b08`) | (K2); §4 `1 − e ≤ 1_{G_r^c}` — consumed |
| [Z] | `frontiers/c7_zero_gap_limit_20260929/PROOF.md` (blob `5b6328ea`) | (Z13)–(Z14): the change of variables in the near/far identity — consumed |
| #191 | `frontiers/remainder_vanishing_20260930/PROOF.md` (merged 1 October 2026 at `9556547`; blob `441152df`) | Lemma E Steps 1–4, §2 (2.1), `r_0^*` — consumed |
| #198 | `frontiers/remainder_rate_20260930/PROOF.md` (merged 1 October 2026 at `124c37d`; blob `abfb98ae`) | (3.1), §3 sign window, Lemma B's barrier (1.2) and §1 identity, Lemma W (W.1), (2.1), Lemma F′ — consumed |
| #207 | `frontiers/cusp_second_order_20261001/PROOF.md` (unmerged; v1.1 blob `f6df5a73`) | §0, proof of CU.1, CU.2, structure of CU.3, §6 ((6.1), (CU.2)) — **consumed, unmerged** |
| #218 | `frontiers/candidate_third_order_20261001/PROOF.md` (unmerged; blob `70ca57ef`) | Lemma D (also for `H̃`), (1.2) and its proof, Lemma F (F1, F3, (F.2)), Lemma C (C1, C2, C3), Lemma O, Theorem T, §4 — **consumed, unmerged** |
| #187 | `frontiers/far_elder_rate_20260930/PROOF.md` (unmerged; blob `07260114` at `75c686c`, rebound from `37dcf6ef` after a status-only repair) | Theorem F at `ρ = r_0^*` — **consumed, unmerged, for (E3.3) and Corollary E3′(3) only** |
| #216 | `frontiers/third_order_coefficient_20261001/` (unmerged) | numerical `c₂`, the Monte Carlo — cited only |
| #188 | `frontiers/far_elder_flat_ridge_20260930/PROOF.md` (unmerged) | Theorem G, an alternative far bound (Remark 2) — cited only |

## 7. Exact controls (`e3_check.py`; stdlib; exact rationals; byte-identical under `-O`)

- **X1** the exponent ledger of §4.
  - #218's ledger: least exponent `4/11`, attained exactly by `ρ_f⁵/ℓ` and `ℓ²ρ_f^{−6}`.
  - The intermediate terms: `ℓ²ρ_c^{−7}` and `a³` on `[ρ_c, a]`; `ℓ^{5/3}a^{−7}` and `ℓ^{2/3}a^{−2}` on `[a, r_0^*]`. All
    have exponents `> 4/11`, the least being `2/5`.
  - The facts used: `ρ_f < ρ_c < a`; `k ≤ ℓ^{1/3}` on `[ρ_c, r_0^*]`; `κ ≤ ℓ^{7/15} ≤ 1` on `[a, r_0^*]`; and that
    `a = ℓ^{2/15}` balances `a³` against `ℓ^{2/3}a^{−2}`.
- **X2** the ridge identities (M1) and the closed forms (M4)–(M5), as exact polynomial identities in `Q[X, φ]`, with
  `g(X₃)` checked on a grid of rational `φ`.
- **X3** the margins:
  - (M4) through the factorizations `(φ + 1)³ − 8φ³ = (1 − φ)(7φ² + 4φ + 1)` and `(1 + ψ)³ − 64ψ³ = (1 − 3ψ)(21ψ² + 6ψ + 1)`;
  - (M2)–(M3) on dense rational grids of `(φ, X)`;
  - the sharpness of `3/2` (equality at `φ = 1`).
- **X4** the one-dimensional decision under perturbation. For random rational `φ` and polynomial perturbations
  `h = (X² − ¼)²q(X)`, scaled so that rigorous coefficient bounds give `sup|h″| ≤ κ/4` and
  `sup|h| < (3/2)κ||φ| − 1/3|`, the path and trap inequalities of Step Q6 hold exactly on a fine rational grid in every
  case.
- **X5** Lemma CU.1′'s mechanism. On exactly pinned polynomial fields of degree 6–7 in `d = 2, 3` with `k = κr`, every
  monomial `r^aX^iΞ^j` of `𝔉 − 𝔓` has `a ≥ 1` and `|j| ≤ a + 1`, and the bound is attained (`rXΞ²`).
- **X6** Lemma S on random rational instances and on near-extremal ones; and the two polynomial bounds of Step Q2,
  `(5/4 + 35Γ/8)² ≤ 80(1 + Γ)²` and `105/64 + (2911/128)Γ + (317/4)Γ² ≤ 80(1 + Γ)²`.
- **X7** the pointwise facts of §§2–3: `0 ≤ loss_κ ≤ 9Y²`; the equivalence `|φ| < 1/3 ⟺ |Y′| < 2κ|Δ|`; the Lemma O′
  domination; and Step E2's `𝔅_5` bound `w_κ ≤ 12κ|Δ|τ` when `|Y_r| < 6κ|Δ| < |Y′|`.
- **X8** Lemma S′'s linear algebra, on 121 instances in `d = 2, 3, 4`. Each has `−H̃ = O diag(λ) Oᵀ`, with `O` a rational
  orthogonal matrix (Cayley transform) and rational `λ`, and `H_M = Λ_rH̃Λ_r`. The checks:
  - `det H_M = r² det H̃`;
  - `−H_M − r²λ_min(−H̃)I` is positive semidefinite, by all principal minors, so `λ_min(−H_M) ≥ r²λ_min(−H̃)`; at the
    instance `H̃ = −I`, `r = 1/2` the matrix is singular, so the bound is attained;
  - `|det H̃| ≤ λ_min(−H̃)‖H̃‖^{d−1}`.
- **X9** Lemma H's exact form (H.1). The fields are exactly pinned polynomial fields (`d = 2`: degree 6 and 7; `d = 3`:
  degree 6; `k = κr`), at the separations `r ∈ {1/3, 2/7, 1/2, 1}`. The checks:
  - the pins themselves;
  - `r^{−2}∂_u²f(M) = −6κ + ∫_0^1 s(1 − s)²∂_u⁴f(M + rsu) ds`;
  - `r^{−1}∂_u∂_θf(M) = −∫_0^1 (1 − s)∂_u²∂_θf(M + rsu) ds`;
  - as polynomials in `r`, the values at `r = 0`: `−6κ + f₄/12`, `−γ/2` and `A`.
- **Mutants.** Each exits 1:
  - M1 `ρ_c = ℓ^{1/4 − 1/120}`;
  - M2 margin constant `8/5` in place of `3/2`;
  - M3 elder threshold `0.36` in place of `1/3` in X4;
  - M4 the claim `|j| ≤ a` in X5;
  - M5 coefficient `1/λ` in place of `2/λ` in (1.2);
  - M6 the factor `1` in place of `r²` in X8 (`λ_min(−H_M) ≥ λ_min(−H̃)`);
  - M7 the kernel `s²(1 − s)` in place of `s(1 − s)²` in (H.1) (the same mass `1/12`, hence the same `r = 0` value);
  - M8 the split at `ℓ^{1/5}` in place of `ℓ^{2/15}` (then `ℓ^{2/3}a^{−2} = ℓ^{4/15}`, below `4/11`).

  An unknown label exits 2.

**What the controls do not test.** Lemma CU.1′ for non-polynomial fields; the probability estimates of Lemma CE (Steps
E2–E6); Lemma G; Lemma O′, Lemma H's covariance bounds and Lemma S′ as statements about random fields; and the assembly
of §4. These are proved in prose only.

**Exploration (floating point; archive only, not a control).**
- *The Gaussian kernel on `R^d`, the large-`L` regime.* `Cov(H̃ | pins)` for `e^{−|z|²/2}` (`d = 2, 3`; 60-digit
  `mpmath`) has smallest eigenvalue `0.1667` at `r = 0.001`. It decreases smoothly to `0.1360` at `r = 1`, `0.0714` at
  `r = 2` and `0.0239` at `r = 3`, and the largest eigenvalue is `2` throughout.
  - In `d = 2` the conditional covariance at `r → 0` is diagonal, with eigenvalues `24/144 = 1/6`, `2/4 = 1/2` and `2`:
    `Var(f₄ | pins) = 105 − 81 = 24`, `Var(γ | pins) = 3 − 1 = 2` and `Var(A | pins) = 3 − 1 = 2`, for the entries
    `f₄/12`, `−γ/2` and `A` of `H̃`.
  - The decrease at large `r` is the scaling `H̃_uu = r^{−2}∂_u²f(M)`: once the pin at `S` stops constraining
    `∂_u²f(M)`, the variance of `H̃_uu` is about `2r^{−4}` (`0.0247` at `r = 3`).
- *Small tori.* The referee's independent probe (REFEREE_2, R2) found the bound positive and smooth at `r = 0` on tori
  with `L = 2, 3, 6` in `d = 2` and `L = 3` in `d = 3`, over several frames, for `r` up to `1.5·min(1, L/(4√2))`. The
  constant depends on `L` and the frame and can be tiny: `λ_min ≈ 4·10⁻⁵` at `d = 2`, `L = 2`, `u = e₁`,
  `r ≈ 0.354`. Lemma H claims no uniformity in `L`.

## 8. Review slices

- **A** §1: Lemma CU.1′, Lemma S and Lemma Q. Points to check:
  - the window and its embedding;
  - the ridge and the `C⁰`/`C²` distances;
  - the reduction to the ridge;
  - the margins (M1)–(M6);
  - the three cases of Step Q6.
- **B** §2: Lemma G and Lemma CE. Points to check:
  - (F1)–(F7) against #198, #207 and #218;
  - the pathwise comparison (2.3);
  - the four bad events of Step E2 and their dyadic `𝒩_r`-bookkeeping;
  - the Gaussian comparisons of Steps E4 and E6.
- **C** §§3–4: Lemma O′; Lemma H (the exact form (H.1), the uniform nondegeneracy at `r = 0` and `r > 0`, the
  conditional moments); Lemma S′ (the rescaled barrier, the sign window, the dyadic use of Lemma D); the decomposition
  at `r_0^*`, the fold-region elder deficit, the split at `ℓ^{2/15}`; and Corollary E3′.
