# The elder density to third order: `ν_eld(ℓ) = cℓ^{−1/3} + c₁ℓ^{1/4} + O(ℓ^{1/3})`, and the `c₂ℓ^{1/3}` term conditional on Math- #187

Object: CL-ELDER-THIRD-ORDER-20261001-v1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 1 October 2026.
Before submission, a clean-context same-family referee read the whole note against its sources (`REFEREE_1.md` in the
project archive). Its verdict was ACCEPT WITH MINOR FIXES, with no major finding. Its four minor findings and nine nits
are applied:
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

**Dependencies (unmerged, consumed).** This note cannot be integrated before the following, and must be rebound if any
of them changes:
- Math- #191 (`frontiers/remainder_vanishing_20260930/PROOF.md`, v1.1 blob `441152df`): Lemma E Steps 1–4, §2 (2.1),
  the admissible radius `r_0^*`.
- Math- #198 (`frontiers/remainder_rate_20260930/PROOF.md`, v1.1 blob `abfb98ae`): (3.1) and the sign window of §3,
  Lemma B's display (1.3) and §1's elder-density identity, the far integral (2.1), Lemma F′.
- Math- #207 (`frontiers/cusp_second_order_20261001/PROOF.md`, v1.1 blob `f6df5a73`): §0 (the cusp objects), the proof
  of Theorem CU.1, Theorem CU.2, the structure of Proposition CU.3 (re-proved here with explicit margins), Lemma CU.5's
  statement (5.1) and its proof, §6 ((6.1), (CU.2)).
- Math- #218 (`frontiers/candidate_third_order_20261001/PROOF.md`, blob `70ca57ef`): Lemma D, (1.2), Lemma F (Steps
  F1, F3, (F.2)), Lemma C (Steps C1, C2 and C3), Lemma O, Theorem T and §4 (the fold region and the exponent ledger).
- For (E3.3) only: Math- #187 (`frontiers/far_elder_rate_20260930/PROOF.md`, blob `37dcf6ef`), Theorem F.

**Merged inputs:** [R], [P] with [E1]/[E2]/[REC], [C7-K] ((K2) and §4), and [Z] (Z13)–(Z14) with [P] §10 (the change
of variables behind the near/far identity); [182] and further parts of [Z] enter through #198 and #191.

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

**Theorem E3 (the elder density to third order).** For every `d ≥ 2` and `L > 0`, as `ℓ ↓ 0`:

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + O(ℓ^{1/3});                                                    (E3.1)
    ν_eld(ℓ) ≥ c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} − C ℓ^{4/11};                                          (E3.2)

and if, in addition, Math- #187's Theorem F holds (`ν_eld^{far,ρ}(ℓ) ≤ C(ρ)ℓ^{2/3}` for each fixed `ρ ∈ (0, L/2]`), then

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + o(ℓ^{1/3}).                                         (E3.3)

All three follow from one two-sided estimate. With `β := min(1/8, 1/(4m))` (#207 Lemma CU.5's exponent), there are
`r₂ > 0` and `C < ∞` such that for every `r₁ ∈ (0, r₂]` and `0 < ℓ ≤ ℓ₀(r₁)`

    −Cℓ^{4/11} ≤ ν_eld(ℓ) − cℓ^{−1/3} − c₁ℓ^{1/4} − c₂ℓ^{1/3} ≤ Cℓ^{4/11} + Cℓ^{1/3}r₁^β + ν_eld^{far,r₁}(ℓ),      (E3.0)

with `C` independent of `r₁`.

**Corollary E3′ (the rejected density).** With Theorem T of #218,
1. `ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + O(ℓ^{1/3})` — a rate for #207's (CU′.2);
2. `ρ_rej(ℓ) ≤ B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + Cℓ^{4/11}`;
3. under #187's Theorem F, `ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + o(ℓ^{1/3})`: the `ℓ^{1/3}` terms of the
   candidate and elder densities are equal, so the rejected density has none.

(E3.1) is a rate for #207's (CU.1), which claimed no rate for its `o(ℓ^{1/4})`. (E3.3) identifies the third coefficient
of the elder law with the `c₂` that Math- #216 defines and computes (`0.22152441` in `d = 2`, `0.16123405` in `d = 3`
for the Gaussian kernel; numerical approximations, not certified).

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
- *Intermediate separations `ℓ^{1/5} ≤ r ≤ r₁`.* Lemma B′ multiplies three facts: #198's barrier for the elder mark
  (`|det K_M| ≤ Cℓ^{1/3}K^{d−1/3}/r`), the sign window for `det K_S`, and #207 CU.5's bound on the typed probability. The
  result is `Cℓ^{1/3}r₁^β`, small with `r₁`. Below `ℓ^{1/5}`, #207's (5.1) suffices.
- *Far separations.* #198 Lemma F′ gives `O(ℓ^{1/3})`, which proves (E3.1). #187 gives `O(ℓ^{2/3})`, and letting
  `r₁ ↓ 0` after `ℓ ↓ 0` proves (E3.3).

**What is not claimed.**
- No rate in (E3.3). A rate would follow from a far bound with explicit dependence on the separation,
  `C(ρ) ≤ Cρ^{−p}` (Remark 2).
- (E3.3) is conditional on #187, an unmerged author-side candidate. (E3.1), (E3.2) and Corollary E3′(1)–(2) do not use it.
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
- (F1) `det K_M = −6kΔ + rY_r + R_M` and `det K_S = 6kΔ + rY_r + R_S`, with `|R_i| ≤ Cr²(1 + k)𝒩_r^{N₁}`. This is #198
  (3.1) with `F_r`'s own transverse Hessian `A` in place of `A_0`. #218 Step F1 records why: #191 Steps 1–3 expand the
  pinned function `F_r` about its own jets at `0`, and pass to `A_0` only through `‖A − A_0‖ ≤ r²T`.
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
  `G(e, −o) = G(e, o)` and `|G(e, o)| ≤ H(e)(1 + |o|)^p`. Then `|E G(E, O) − E G(E, O₀)| ≤ C|s|²E[H(E)]`, where
  `O₀ ~ N(0, Σ)` is independent of `E` and `C` depends also on `s₀`.

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

*Proof.* Take `r₂ ≤ min(r_0^*, 1/2, r_Q, r_{CU})`, where `r_{CU}` is the radius `r₁` of #207 Lemma CU.5.

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
`36κ²Δ² ≤ 9Y²`. By (F7) and Lemma G (b) with `s = 12kw` (`|s| ≤ 12|w|`, as `k ≤ 1`),
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

**Lemma B′ (elder pairs at intermediate separations).** For `0 < r ≤ min(r_{CU}, r_0^*)`, `b ∈ R` and `0 < k ≤ 1`, with
`ℓ = kr³` and `κ = k/r`,

    E_Q[(W_r/r²) e] ≤ C ℓ^{1/3} (κ + r) (min(1, κ)^{1/2} + r^β) P^N,        β = min(1/8, 1/(4m)).              (B′.1)

*Proof.* Use the notation of §2 (`𝒩_r`, `Δ = det A`).
- *The weight on the elder event.* On `{W_r > 0, e = 1}`, #198 (1.3) gives
  `|det K_M| = |det H_M|/r ≤ C ℓ^{1/3}K^{d−1/3}/r`, where `K = 1 + ‖D²f‖_∞ + ‖D³f‖_∞ ≤ C𝒩_r`. On the typed event the
  two determinants have opposite signs, so the sign window (#198 §3), applied to (F1), gives
  `|det K_S| ≤ 12k|Δ| + 2max_i|R_i| ≤ r(12κ|Δ| + Cr(1 + k)𝒩_r^{N₁})`. With `|Δ| ≤ 𝒩_r^m` and `k ≤ 1`,
  `(W_r/r²)e ≤ Cℓ^{1/3}(κ + r)𝒩_r^N1{W_r > 0}`.
- *The typed probability.* The proof of #207 Lemma CU.5 gives `P_Q({W_r > 0} ∩ B₁ ∩ E₁) ≤ C₀λ_{CU}` with
  `λ_{CU} = C(k/r + r^{1/4})`, `P_Q(B₁^c) ≤ Cr^{1/(2m)}` (Carbery–Wright, uniformly in the mean) and
  `P_Q(E₁^c) ≤ C_qr^qP^{N_q}`. Hence `P_Q(W_r > 0) ≤ C(min(1, κ) + r^{1/4} + r^{1/(2m)})P^N`.
- *Cauchy–Schwarz.* `E_Q[(W_r/r²)e] ≤ Cℓ^{1/3}(κ + r)‖𝒩_r^N‖_{L²(Q)}P_Q(W_r > 0)^{1/2}`, which is (B′.1). ∎

## 4. Proof of Theorem E3 and of Corollary E3′

*Setup.* As in #218 §4, put `ρ_f := ℓ^{1/4 + 1/44}` and `ρ_c := ℓ^{1/4 − 1/36} = ℓ^{2/9}`, with `s_f := ρ_fℓ^{−1/4} = ℓ^{1/44}`
and `s_c := ρ_cℓ^{−1/4} = ℓ^{−1/36}`. Let `r₂` be as in Lemma CE, fix `r₁ ∈ (0, r₂]`, and take `ℓ` so small that
`ρ_c < ℓ^{1/5} < r₁` and `ℓρ_f^{−3} ≤ 1`. By the near/far identity at `r_0 = r₁` (§0),

    ν_eld(ℓ) − cℓ^{−1/3} = F^{eld} + K^{eld} + I^{eld} − J₄ + ν_eld^{far,r₁}(ℓ),

with all integrands at `(b, ℓ/r³, u)`, inner integrals `db dσ(u)`, and
- `F^{eld} := ∫_0^{ρ_f}∫∫ r^{−2}(A_r^{eld} − A_0)`;
- `K^{eld} := ∫_{ρ_f}^{ρ_c}∫∫ r^{−2}(A_r^{eld} − A_0)`;
- `I^{eld} := ∫_{ρ_c}^{r₁}∫∫ r^{−2}A_r^{eld} ≥ 0`;
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

*`I^{eld}`: intermediate separations.* Split at `ℓ^{1/5}`.
- *On `[ρ_c, ℓ^{1/5}]`.* `e ≤ 1` and #207 (5.1) with (R5) give
  `0 ≤ r^{−2}A_r^{eld} ≤ r^{−2}A_r ≤ C(κ² + r²)(min(1, κ)^{1/2} + r^β)(1 + |b|)^Ne^{−cb²}`. Here `κ ≤ s_c^{−4} ≤ 1`. The
  four products integrate to at most
  `C(ℓ^{1/4}s_c^{−9} + ℓ²ρ_c^{−7+β} + ℓ^{1/2}ℓ^{1/5} + ℓ^{(3+β)/5}) = C(ℓ^{1/2} + ℓ^{4/9+2β/9} + ℓ^{7/10} + ℓ^{(3+β)/5})`.
- *On `[ℓ^{1/5}, r₁]`.* `κ = ℓr^{−4} ≤ r` and `κ^{1/2} ≤ r^{1/2} ≤ r^β`, so (B′.1) with (R5) gives
  `r^{−2}A_r^{eld} ≤ 4Cℓ^{1/3}r^{−1+β}(1 + |b|)^Ne^{−cb²}`. This integrates to at most `(4C/β)ℓ^{1/3}r₁^β`.

So `0 ≤ I^{eld} ≤ Cℓ^{4/9} + Cℓ^{1/3}r₁^β`, with `C` independent of `r₁`.

*Conclusion.* `4/11 < 4/9 < 1/2 < 3/5 < 7/10`. Hence (E3.0):
`−Cℓ^{4/11} − Cℓ^{4/9} ≤ ν_eld − cℓ^{−1/3} − c₁ℓ^{1/4} − c₂ℓ^{1/3} ≤ Cℓ^{4/11} + Cℓ^{1/3}r₁^β + ν_eld^{far,r₁}(ℓ)`, using
`I^{eld} ≥ 0`, `ν_eld^{far,r₁} ≥ 0` and `J₄ ≤ Cℓ^{4/9}`.
- (E3.2) is the left inequality.
- (E3.1): take `r₁ = r₂` (`< L/2`). #198 Lemma F′ gives `ν_eld^{far,r₂}(ℓ) ≤ C(r₂)ℓ^{1/3}`, so the right side is `O(ℓ^{1/3})`, and
  `c₂ℓ^{1/3}` is absorbed.
- (E3.3): #187 Theorem F at `ρ = r₁` gives `ν_eld^{far,r₁}(ℓ) ≤ C(r₁)ℓ^{2/3}`. So
  `limsup_{ℓ↓0} ℓ^{−1/3}|ν_eld − cℓ^{−1/3} − c₁ℓ^{1/4} − c₂ℓ^{1/3}| ≤ Cr₁^β` for every `r₁ ∈ (0, r₂]`. Let `r₁ ↓ 0`. ∎

*Proof of Corollary E3′.* `ρ_rej = ν_cand − ν_eld`.
1. Corollary T′ of #218 and (E3.1).
2. (T.1) and (E3.2): `ρ_rej ≤ [cℓ^{−1/3} + B_{d,L} + I^{cand}ℓ^{1/4} + c₂ℓ^{1/3} + Cℓ^{4/11}] − [cℓ^{−1/3} + c₁ℓ^{1/4} + c₂ℓ^{1/3} − Cℓ^{4/11}]`.
3. (T.1) and (E3.3). ∎

## 5. Remarks

1. **Why the elder law has the candidate's `c₂`.** The elder rule enters the expansion at three places.
   - At the fold scale the rejected mass is `O(r³/k)` ([C7-K] (K2)). That is the order of the boundary layer, below
     `ℓ^{1/3}` after integration.
   - At the cusp scale the elder rule is the window `|φ| < 1/3` (#207). It changes the `ℓ^{1/4}` coefficient from
     `I^{cand}` to `c₁`, and changes nothing at order `ℓ^{1/3}`: by Lemma O′ the elder and candidate cusp losses have the
     same limit `A₂(b, 0)` as `κ → ∞`, which is what the finite part `c₂` subtracts.
   - At intermediate and far separations, elder pairs need a soft maximum (#198 Lemma B, #187), which costs a power of
     `ℓ`.

   So `c₂` is a fold-scale quantity, as #216 argued formally; (E3.3) makes this a theorem, conditional on #187.
2. **What a rate in (E3.3) would need.** The `o(ℓ^{1/3})` comes from the `ε`-argument in `r₁`. #187 proves
   `ν_eld^{far,ρ}(ℓ) ≤ C(ρ)ℓ^{2/3}` with `C(ρ)` not quantified as `ρ ↓ 0`. If `C(ρ) ≤ Cρ^{−p}`, then (E3.0) with
   `r₁ = ℓ^{1/(3(p+β))}` gives the rate `O(ℓ^{min(4/11, 1/3 + β/(3(p+β)))})`. (When `p + β ≤ 5/3` this `r₁` lies below
   `ℓ^{1/5}`; then #207's (5.1) covers all of `[ρ_c, r₁]`, and the split at `ℓ^{1/5}` is not needed.) Such a bound is the near-diagonal spectral refinement that #198 Remark 1
   describes: the conditional variance of the axial curvature under the pins, with `f₄` appended to the pin rows.
3. **The SIDE24 values and the Monte Carlo (exploration, not certified).** For the Gaussian kernel in `d = 3`, #207 §8
   and #216 give `c = 0.0417759`, `c₁ = −0.2118484` and `c₂ = 0.1612340`. So under (E3.3)
   `ν_{3,24}(ℓ) ≈ cℓ^{−1/3}(1 − 5.0711ℓ^{7/12} + 3.8595ℓ^{2/3})` up to `o(ℓ^{2/3})`; the Gaussian-kernel values agree with
   the `L = 24` torus up to a relative `O(e^{−L²/8})`. The elder-pair row of #216 v1.2 §3 is an exploratory estimate of
   `ν_eld` itself: the exact elder rule by union–find on the full periodized field, `d = 2` at `L = 64` and `d = 3` at
   `L = 16`. On `[10⁻⁴, 10⁻²]` it gives data/law `1.006 ± 0.004` (`χ² = 7.0/11`) in `d = 2` and `1.008 ± 0.010`
   (`χ² = 5.0/11`) in `d = 3` for the three-term law, and rejects the two-term law (`χ² = 714/11` and `175/11`). Its
   adjacent-pair row, which #218 Remark 3 concerns, is not covered here.
4. **Lemma Q is field-independent.** It is a deterministic statement about `C⁵` functions with two pinned critical
   points: the elder window `|φ| < 1/3` of #207 is stable, with explicit margins, as long as
   `𝒩r(1 + |γ|/λ)² ≪ κ||φ| − 1/3|` and `λ ≫ 𝒩r + (𝒩r|γ|)^{1/2}`, with the window inside the torus ((Q1)–(Q4)). #207's
   Proposition CU.3 is its qualitative case. Only Lemma CE and §4 use the law of
   the [P] field.
5. **For the manuscript.** Once #191, #198, #207, #218 and this note are reviewed, the abstract can state
   `ν_{3,24}(ℓ) = c_{3,24}ℓ^{−1/3} + c₁ℓ^{1/4} + O(ℓ^{1/3})` with `c₁ < 0` the explicit integral (CU.2). With #187 it can
   state the three-term law. Until then V3 edit E10 is the safe statement.
6. **Consistency.**
   - (E3.1) implies #207's (CU.1) and #198's (0.1).
   - Corollary E3′(1) implies #207's (CU′.2).
   - Corollary E3′(1), with `I^{cand} − c₁ = (1 − 3^{1/4}/2)|c₁| > 0` (#207 (CU′.2)), shows that the rejected density
     approaches `B_{d,L}` from above, by the rejected cusp mass, now with a rate; Corollary E3′(2) bounds the approach
     from above to order `ℓ^{4/11}`.

## 6. Sources (exact identities in `SOURCES.json`)

| Tag | Path | Role |
|---|---|---|
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`) | (R2)–(R5): pin covariance, regression, moments, pin densities; §4 scaled Hessians — consumed |
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`) | §2 finite-jet rank, §8 maximin and elder mark, §§9–10 as [E2] (the near/far identity), §15 parity factorization and (15.2) — consumed |
| [E1] | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` (blob `213594d6`) | reading rule |
| [E2] | `reviews/d1_section9_borel_repair_20260925/REPAIR.md` (blob `fe9b9ce4`) | §9 replacement |
| [REC] | `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` (blob `75da2597`) | reading rule |
| [C7-K] | `frontiers/c7_total_bounded_20260929/PROOF.md` (blob `28748b08`) | (K2); §4 `1 − e ≤ 1_{G_r^c}` — consumed |
| [Z] | `frontiers/c7_zero_gap_limit_20260929/PROOF.md` (blob `5b6328ea`) | (Z13)–(Z14): the change of variables in the near/far identity — consumed |
| #191 | `frontiers/remainder_vanishing_20260930/PROOF.md` (unmerged; v1.1 blob `441152df`) | Lemma E Steps 1–4, §2 (2.1), `r_0^*` — **consumed, unmerged** |
| #198 | `frontiers/remainder_rate_20260930/PROOF.md` (unmerged; v1.1 blob `abfb98ae`) | (3.1), §3 sign window, Lemma B (1.3) and §1 identity, (2.1), Lemma F′ — **consumed, unmerged** |
| #207 | `frontiers/cusp_second_order_20261001/PROOF.md` (unmerged; v1.1 blob `f6df5a73`) | §0, proof of CU.1, CU.2, structure of CU.3, proof of CU.5 and (5.1), §6 ((6.1), (CU.2)) — **consumed, unmerged** |
| #218 | `frontiers/candidate_third_order_20261001/PROOF.md` (unmerged; blob `70ca57ef`) | Lemma D, (1.2), Lemma F (F1, F3, (F.2)), Lemma C (C1, C2, C3), Lemma O, Theorem T, Corollary T′, §4 — **consumed, unmerged** |
| #187 | `frontiers/far_elder_rate_20260930/PROOF.md` (unmerged; blob `37dcf6ef`) | Theorem F — **consumed, unmerged, for (E3.3) and Corollary E3′(3) only** |
| #216 | `frontiers/third_order_coefficient_20261001/` (unmerged) | numerical `c₂`, the Monte Carlo — cited only |
| #188 | `frontiers/far_elder_flat_ridge_20260930/PROOF.md` (unmerged) | an alternative far bound — cited only |

## 7. Exact controls (`e3_check.py`; stdlib; exact rationals; byte-identical under `-O`)

- **X1** the exponent ledger of §4: #218's ledger (least `4/11`) and the intermediate terms `ℓ^{1/4}s_c^{−9}`,
  `ℓ²ρ_c^{−7+β}`, `ℓ^{7/10}`, `ℓ^{(3+β)/5}` for `β ∈ {1/8, 1/12, 1/16, 1/20}`, all with exponents `> 4/11`; the order
  `ρ_c < ℓ^{1/5}`; and the facts used on `[ℓ^{1/5}, r₁]`: `κ ≤ r` and `κ^{1/2} ≤ r^β`.
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
- **Mutants.** Each exits 1:
  - M1 `ρ_c = ℓ^{1/4 − 1/120}`;
  - M2 margin constant `8/5` in place of `3/2`;
  - M3 elder threshold `0.36` in place of `1/3` in X4;
  - M4 the claim `|j| ≤ a` in X5;
  - M5 coefficient `1/λ` in place of `2/λ` in (1.2).

  An unknown label exits 2.

**What the controls do not test.** Lemma CU.1′ for non-polynomial fields, the probability estimates of Lemma CE
(Steps E2–E6), Lemma G, Lemmas O′ and B′ as statements about random fields, and the assembly of §4. These are proved in
prose only.

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
- **C** §§3–4: Lemmas O′ and B′, the decomposition, the fold-region elder deficit, the intermediate split, the limit
  `r₁ ↓ 0`, and Corollary E3′.
