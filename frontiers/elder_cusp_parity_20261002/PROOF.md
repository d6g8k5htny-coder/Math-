# The elder cusp kernel: the candidate rate, and no linear term at fixed `κ`

Object: CL-ELDER-CUSP-PARITY-20261002-v1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 2 October 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph,
STATUS, PROOF_INDEX, prize or Boolean change; no numerical constant is certified. Same GitHub account as every lane;
zero organizational independence.

**What is new.** At the cusp scale `k = κr`, the elder kernel `r^{−2}A_r^{eld}(b, κr, u)` tends to the elder cusp kernel
`𝒜^{eld}(b, κ, u)`. Math- #229 (merged) proves this with error `C(r(1 + κ) + κ²r^{3/2} + κ³r²)` (its Lemma CE⁺), while the
candidate kernel has error `Cr(1 + κ)` (Lemma C⁺ there). The two extra terms come from two bad events of Math- #220's
Lemma Q, which decides the elder mark from the window field. Math- #237 (open) proves that the candidate cusp kernel has
no `O(r)` term after the birth height is integrated out; its Remark 3 records that the elder kernel has none *formally*,
without a proof. This note proves the following.
- **Lemma Q′** (§1): Lemma Q with relaxed margins. `Γ = |γ|/λ` is replaced by `Γ̃ = |A^{−1}γ|`, the ridge maximizer is
  located in a ball of radius `ϱ = max(1, 8ḡ/λ)` instead of `1`, and every `φ` is decided, not only `|φ| ≤ 1`.
- **Proposition CE⁺⁺** (§2): the elder cusp kernel with the candidate's error `Cr(1 + κ)`. On the typed window, Lemma Q′
  needs only `λ ≳ 𝒩r(1 + |γ| + ‖B‖)(1 + |f₄|/κ)`. This removes #229's two elder-only ledger rows. The exponent `3/7` of
  #229 does not change (Remark 2).
- **Theorem N** (§§3–5): for `κ` in a fixed compact subset of `(0, ∞)`, the elder and candidate cusp kernels have no
  `O(r)` term, pointwise in the birth height `b`: the error is `O(r²)`. The proof computes the `O(r)` term. The edges of
  the elder window and the typed weight both move at first order by multiples of one jet polynomial,

      Q₁ := f₅/120 − ηᵀA^{−1}γ/12 + γᵀA^{−1}BA^{−1}γ/8,

  the coefficient of the ridge correction `rQ₁X(X² − ¼)²`. The edges `|φ| = 1/3` move to `|φ| = 1/3 + rQ₁/(2κ)`, and the
  weight changes by `12κrΔ²Q₁`. `Q₁` is odd under the point reflection of the jets, and every zeroth-order quantity is
  even, so the parity factorization (#220 (F7)) makes the `O(r)` term `O(rk)`.
- **Corollary N′** (§6): in every fixed cusp window `κ₀ ≤ ℓ/r⁴ ≤ κ₁`, the elder, candidate and rejected densities are a
  constant times `ℓ^{1/4}` plus `O(ℓ^{3/4})`. There is no term of order `ℓ^{1/2}`.

An elder analogue of #237's Theorem P, the whole elder density with a remainder beyond `ℓ^{1/2}`, needs the two ends
`κ → ∞` and `κ → 0`, where Theorem N is not uniform. Remark 1 says where the argument stops.

**Dependencies (consumed; all merged).**
- Math- #220 (`frontiers/elder_third_order_20261001/PROOF.md`, blob `c8767dde`; merged at `0d79778`): §0; §1 (the setting,
  `𝔓`, Lemma CU.1′ (1.1) and its proof, Lemma S (1.2), Lemma Q and its proof, (M1)–(M6)); §2 (notation, (F1)–(F7),
  (2.1)–(2.2), Lemma G, Lemma CE and its proof, Steps E1–E6).
- Math- #229 (`frontiers/third_order_rate_20261001/PROOF.md`, blob `110ed33a`; merged at `6f74f7a`): Lemma L (L.1); Lemma CE⁺
  (CE⁺.1) and its proof (Step E2⁺ with (3.1)–(3.2), Step E3⁺); §5 (the ledger, for Remarks 1–2).
- Math- #218 (`frontiers/candidate_third_order_20261001/PROOF.md`, blob `70ca57ef`; merged at `fb6ee97`): Lemma D (1.1) and
  (1.2); Step F1, (2.1)–(2.2); Lemma C, Step C1 (its three cases) and Step C3.
- Math- #232 (`frontiers/c2_finite_jet_transfer_20261001/PROOF.md`, blob `54cc4a1a`; merged at `7fe06b0`): §2, (2.1)–(2.4).
- Math- #207 (`frontiers/cusp_second_order_20261001/PROOF.md`, blob `f6df5a73`; merged at `566b1a1`): §0 (the cusp objects
  and the cusp polynomial (0.2)); Theorem CU.2 and Proposition CU.3, through #220; §4 (4.1).

**Merged inputs.** [R] (R2)–(R5); [P] §2 (finite-jet rank) and §15 (parity factorization), through #218 and #220;
Math- #191 (`441152df`: Lemma E Step 3, the exchange `det H_M(−r) = det H_S(r)`).
**Cited only.** Math- #237 (open: Lemma Π, the expansion of Lemma Ω (a) here; Lemma K; its cusp-scale statement after
Lemma U; Remarks 3–4), Math- #238 (open: Lemma W, the `d = 1` form of Lemma Q″), Math- #216 (open: the Monte Carlo of the
lifetime densities), Math- #198 (through #220).

## 0. Statement

Setting and notation are those of #220 §§0–2 and #229 §0:
- fixed `d ≥ 2`, `m = d − 1`, `L > 0`, the [P] field on `X = R^d/(LZ^d)`; near pins `M = −ru/2`, `S = ru/2` at heights `b`,
  `b − kr³`; the pinned law `Q = Q_{r,b,k}`; the pin density `π_r(v_r)`; `P = 1 + |b| + k`; `κ = k/r`;
- the scaled endpoint Hessians `K_M`, `K_S`, `W_r/r² = F_d(K_M)F_{d−1}(K_S)`, the elder mark `e`, and the kernels
  `A_r = 12π_r(v_r)E_Q[W_r/r²]`, `A_r^{eld} = 12π_r(v_r)E_Q[(W_r/r²)e]` and `A_0`; so `r^{−2}A_r^{eld} = 12π_r(v_r)E_Q[ω_re]`
  with the *weight* `ω_r := r^{−2}F_d(K_M)F_{d−1}(K_S)`;
- the free jets `J′ ⊃ J″ ⊃ J‴` of `f = F_r` at `0` (order `≤ 9`; `J″ = J′ ∖ {f₄}`, `J‴ = J″ ∖ {A}`), `𝒩 = 𝒩_r = 1 + k + ‖F_r‖_{C⁹}`,
  and the contact law at `v_0(b, k)`, with expectation `E_{v_0(b,k)}`;
- jets at `0`: `A = D_Θ²f`, `B = ∂_uA`, `C = ∂_u²A`, `γ = ∇_Θ∂_u²f`, `η = ∇_Θ∂_u³f`, `f₄ = ∂_u⁴f`, `f₅ = ∂_u⁵f`; `Δ = det A`,
  `J = adj A`, `Δ_B = tr(JB)`, `Δ_C = tr(JC)`, `Δ_BB = D²det(A)[B, B]`, `J_B = D adj(A)[B]`; `λ = λ_min(−A)` on `{A < 0}`;
- `Y′ = (f₄/12)Δ − γᵀJγ/4`, `Y_r = Y′ + 3kΔ_B`, `φ_r = (f₄ − 3γᵀA^{−1}γ)/(72κ) = Y′/(6κΔ)`,
  `w_κ(A, Y) = (36κ²Δ² − Y²)₊1{A < 0}` and `w_κ^{eld}(A, Y) = w_κ(A, Y)1{|Y| < 2κ|Δ|}`;
- the cusp kernels `𝒜^{cand}`, `𝒜^{eld}` and `𝒜^{con}` (#220 §0, #218 §0).

New notation, on `{A < 0}`:

    Γ̃ := |A^{−1}γ|,    q := γᵀA^{−1}γ,    z := f₄ − 3q = 72κφ_r,
    Q₁ := f₅/120 − ηᵀA^{−1}γ/12 + γᵀA^{−1}BA^{−1}γ/8,    P₁ := (Δ²/120)f₅ − (Δ/12)γᵀJη + (1/8)γᵀJBJγ = Δ²Q₁.    (0.1)

`P₁` is a polynomial in the jets, defined for every `A`. The *parity map* `𝒫` negates the jets of odd order (`γ`, `B`, `f₅`,
…) and fixes those of even order (`A`, `C`, `η`, `f₄`, …), as in #237 §0. `Δ`, `q`, `z`, `Y′` and `Γ̃` are `𝒫`-invariant;
`Q₁` and `P₁` change sign. Finally `w₀ := 36κ²Δ² − Y′² = (Δ²/144)(5184κ² − z²)`.

**Lemma Q′ (the elder decision with relaxed margins).** Deterministic; stated in §1.

**Proposition CE⁺⁺ (the elder cusp kernel with the candidate rate).** There are `r₂′ > 0` and `C, c, N` such that for
`0 < r ≤ r₂′`, `b ∈ R`, `u ∈ S^{d−1}` and `κ > 0` with `κr ≤ 1`,

    |r^{−2}(A_r^{eld} − A_0)(b, κr, u) − (𝒜^{eld} − 𝒜^{con})(b, κ, u)| ≤ C r (1 + κ) (1 + |b|)^N e^{−cb²}.        (CE⁺⁺.1)

**Theorem N (no linear term at fixed `κ`).** Let `K ⊂ (0, ∞)` be compact. There are `r_K > 0` and `C, c, N` such that for
`0 < r ≤ r_K`, `κ ∈ K`, `b ∈ R` and `u ∈ S^{d−1}`,

    |r^{−2}(A_r^{eld} − A_0)(b, κr, u) − (𝒜^{eld} − 𝒜^{con})(b, κ, u)| ≤ C r² (1 + |b|)^N e^{−cb²},              (N.1)
    |r^{−2}(A_r − A_0)(b, κr, u) − (𝒜^{cand} − 𝒜^{con})(b, κ, u)| ≤ C r² (1 + |b|)^N e^{−cb²}.                  (N.2)

The proof identifies the `O(r)` term (§5, Steps N4–N5): it is `12π_0(v_0(b, k))·r·E_{v_0(b,k)}[Q₁Ψ_κ]`, where `Ψ_κ`, the
`𝒫`-invariant functional (5.3), collects the edge densities and the first-order weight; it is `O(rk)` by parity.

**Corollary N′ (cusp windows).** Let `0 < κ₀ < κ₁ < ∞` and `* ∈ {eld, cand, rej}`, with `A_r^{rej} := A_r − A_r^{eld}` and
`𝒜^{rej} := 𝒜^{cand} − 𝒜^{eld}`. As `ℓ ↓ 0`,

    ∫_{(ℓ/κ₁)^{1/4}}^{(ℓ/κ₀)^{1/4}}∫_R∫_{S^{d−1}} r^{−2}A_r^*(b, ℓ/r³, u) dσ(u) db dr
        = ℓ^{1/4} ∫_{κ₁^{−1/4}}^{κ₀^{−1/4}}∫_R∫_{S^{d−1}} 𝒜^*(b, s^{−4}, u) dσ(u) db ds + O(ℓ^{3/4}).                  (N′.1)

So the part of each density from the separations with `ℓ/r⁴ ∈ [κ₀, κ₁]` has no term of order `ℓ^{1/2}`.

**What is not claimed.**
- Nothing about the whole elder or rejected density beyond #229: (E3⁺.0)–(E3⁺.1) with remainder `O(ℓ^{3/7})` stand.
  Theorem N is not uniform as `κ → ∞` or `κ → 0`, and Corollary N′ excludes both ends (Remark 1).
- The constants of Theorem N depend on `K`. No uniformity in `d` or `L`.
- No certified numerical value. The numerics of Remarks 3–4 are exploration.
- Nothing beyond the existential scope of [R], [P], #191, #207, #218, #220, #229 and #232.

## 1. The elder decision with relaxed margins

The setting is #220 §1: `f ∈ C⁵(X)`, `𝒩 ≥ max(1, ‖f‖_{C⁵})`, `0 < r ≤ r_Q`, `κ > 0`, and `M = −ru/2`, `S = ru/2` critical
points with `f(M) = b` and `f(S) = b − κr⁴`; `Φ(X, Ξ) = rXu + r²ΘΞ`, `𝔉 = r^{−4}(f∘Φ − b)`, the cusp polynomial
`𝔓(X, Ξ) = 2κ(X + ½)²(X − 1) + (f₄/24)(X² − ¼)² + ½(X² − ¼)γ·Ξ + ½ΞᵀAΞ`, and for `A < 0`, `Ξ*(X) = −½(X² − ¼)A^{−1}γ` and
`g(X) = 𝔓(X, Ξ*(X)) = κ[2(X + ½)²(X − 1) + 3φ(X² − ¼)²]` with `φ = (f₄ − 3γᵀA^{−1}γ)/(72κ)`. `C₁ = C₁(d)` is the constant of
#220 (1.1).

**Lemma Q′.** Suppose `A ≤ −λI` with `λ > 0`, and put

    Γ̃ := |A^{−1}γ|,    M̃ := (35/8)Γ̃,    ε̃ := 220 C₁𝒩r(1 + Γ̃)²,    R′ := 5M̃ + 4 + 3((κ + 1)/λ)^{1/2}.

Assume
- (Q′1) `𝒩(3r + r²R′) ≤ λ/2` and `6r + 2r²R′ ≤ L/4`;
- (Q′2) `2C₁𝒩r ≤ λ` and `5r(1 + M̃) ≤ 1`;
- (Q′3) `ε̃ ≤ κ/4`;
- (Q′4) `||φ| − 1/3| > 2ε̃/(3κ)`.

Then

    e(f) = 1{d_f(M) = f(S)} = 1{|φ| < 1/3}.                                                                   (1.1′)

Moreover, under (Q′1)–(Q′2) alone: for each `X ∈ [−3, 2]`, `𝔉(X, ·)` has a unique maximizer `Ξ_𝔉(X)` over `{|Ξ| ≤ R′}`, with

    |Ξ_𝔉(X) − Ξ*(X)| ≤ 2C₁𝒩r(1 + M̃)/λ ≤ 1 + M̃;                                                             (1.2′)

the ridge `g_𝔉(X) := 𝔉(X, Ξ_𝔉(X))` is `C²` with `g_𝔉(−½) = 0`, `g_𝔉(½) = −κ` and `g_𝔉′(±½) = 0`; and `h := g_𝔉 − g` satisfies

    ε₀ := sup|h|,  ε₁ := sup|h′|,  ε₂ := sup|h″|  ≤  ε̃  on [−3, 2],      |h(X)| ≤ (ε₂/2)(X ∓ ½)².                  (1.3′)

*Proof.* Follow #220's proof of Lemma Q. Steps Q2 and Q6 change, and `R′` replaces `R`.
- *Step Q1* is unchanged with `R′`: by (Q′1), `Φ` embeds a neighbourhood of `𝒲′ := [−3, 2] × {|Ξ| ≤ R′}`, and
  `∂_Ξ²𝔉 ≤ −(λ/2)I` on `𝒲′`.
- *Step Q2′ (the ridge).* Fix `X ∈ [−3, 2]`; then `|Ξ*(X)| ≤ ½(35/4)Γ̃ = M̃`. Put `ḡ := C₁𝒩r(1 + M̃)` and
  `ϱ := max(1, 8ḡ/λ)`; by (Q′2), `ϱ ≤ 4(1 + M̃)`. The ball `{|Ξ − Ξ*| ≤ ϱ}` lies in `{|Ξ| ≤ 5M̃ + 4} ⊂ 𝒲′`, and there
  `r|Ξ| ≤ 1` by (Q′2), so #220 (1.1) applies.
  - *The maximizer.* `∂_Ξ𝔓(X, Ξ*) = 0`, so `|∂_Ξ𝔉(X, Ξ*)| ≤ ḡ` by (1.1). On the sphere `|Ξ − Ξ*| = ϱ`, strong concavity
    gives `𝔉(X, Ξ) ≤ 𝔉(X, Ξ*) + ḡϱ − (λ/4)ϱ² < 𝔉(X, Ξ*)`. So the maximizer over `{|Ξ| ≤ R′}` is unique and lies in the
    open ball, where `∂_Ξ𝔉 = 0`; strong concavity gives `|Ξ_𝔉 − Ξ*| ≤ 2ḡ/λ`, and `2ḡ/λ ≤ 1 + M̃` by (Q′2). This is (1.2′).
    `g_𝔉` is `C²`, and `g_𝔉″` is the Schur complement of `∂_Ξ²𝔉` in `Hess 𝔉` at `(X, Ξ_𝔉)`, as in #220.
  - *The vector `γ`.* Let `D̄ := ∫_0^1∂_Ξ²𝔉(X, Ξ* + t(Ξ_𝔉 − Ξ*)) dt`. Then `Ξ_𝔉 − Ξ* = −D̄^{−1}∂_Ξ𝔉(X, Ξ*)`, and
    `‖D̄ − A‖ ≤ λ/2` (Step Q1), so `|D̄^{−1}γ| ≤ |A^{−1}γ| + ‖D̄^{−1}‖‖D̄ − A‖|A^{−1}γ| ≤ 2Γ̃`. Hence

        |γ·(Ξ_𝔉 − Ξ*)| ≤ 2Γ̃ḡ.                                                                                (1.4′)

    #220 bounds the same quantity by `|γ||Ξ_𝔉 − Ξ*|`. Replacing `Γ` by `Γ̃` here, and below, is what relaxes the margins.
  - *`C⁰` and `C¹`.* As in #220, `ε₀ ≤ C₁𝒩r(1 + |Ξ_𝔉|)² ≤ 4C₁𝒩r(1 + M̃)²`. Since `g_𝔉′(X) = ∂_X𝔉(X, Ξ_𝔉)` (the envelope
    identity), `g′(X) = ∂_X𝔓(X, Ξ*)` and `∂_X𝔓` depends on `Ξ` only through `Xγ·Ξ`, (1.1) and (1.4′) give
    `ε₁ ≤ 4C₁𝒩r(1 + M̃)² + 6Γ̃ḡ`.
  - *`C²`.* Take `(a, b, D) = (∂_X²𝔓, Xγ, A)` at `(X, Ξ*)` and the blocks `(a′, b′, D′)` of `Hess 𝔉` at `(X, Ξ_𝔉)`.
    `∂_X²𝔓` depends on `Ξ` only through `γ·Ξ`, so `|a′ − a| ≤ 2ḡ + 2Γ̃ḡ` by (1.1) and (1.4′). Also `|b′ − b| ≤ β̄ := 2ḡ` and
    `‖D′ − D‖ ≤ C₁𝒩r ≤ λ/2`. With `|D^{−1}b| = |X|Γ̃ ≤ 3Γ̃`, `|D′^{−1}b| ≤ 6Γ̃` and `|D′^{−1}b′| ≤ 6Γ̃ + 2β̄/λ`, the identity
    `b′ᵀD′^{−1}b′ − bᵀD^{−1}b = (b′ − b)ᵀD′^{−1}(b′ + b) + bᵀD′^{−1}(D − D′)D^{−1}b` gives
    `ε₂ ≤ |a′ − a| + β̄(12Γ̃ + 2β̄/λ) + 18C₁𝒩rΓ̃²`, and `2β̄²/λ ≤ 2β̄(1 + M̃)` by (Q′2).
  - *Collecting.* With `M̃ = (35/8)Γ̃`: `ε₀/(C₁𝒩r) ≤ 4 + 35Γ̃ + (1225/16)Γ̃²`, `ε₁/(C₁𝒩r) ≤ 4 + 41Γ̃ + (1645/16)Γ̃²` and
    `ε₂/(C₁𝒩r) ≤ 6 + (279/4)Γ̃ + (3333/16)Γ̃²`. Each is at most `220(1 + Γ̃)²` coefficientwise (control X1).
- *Step Q3* is unchanged: on `|Ξ| = R′`, `|Ξ − Ξ_𝔉| ≥ R′ − (2M̃ + 1) ≥ 3((κ + 1)/λ)^{1/2}`, so #220 (1.4) holds:
  `𝔉(X, Ξ) ≤ g_𝔉(X) − (9/4)(κ + 1)`. *Steps Q4–Q5* are unchanged. Step Q4 gives the pin values and the last bound in (1.3′).
- *Step Q6′ (the decision).* By (Q′3)–(Q′4), `ε₂ ≤ ε̃ ≤ κ/4` and `ε₀ ≤ ε̃ < (3/2)κ||φ| − 1/3|`. Cases E (`|φ| < 1/3`), R⁺ for
  `1/3 < φ ≤ 1` and R⁻ for `−1 ≤ φ < −1/3` are #220's, word for word. Two cases are new.
  - *Case R⁺, `φ > 1`.* On `[−3, −½]`, `1 + 2φX ≤ 1 − φ < 0`, so `g′ = 6κ(X² − ¼)(1 + 2φX) ≤ 0` (M6). Hence
    `min_{[−3,−½]}g = g(−½) = 0` and `g_𝔉 ≥ −ε₀ > −κ` there, while `g_𝔉(−3) ≥ g(−3) − ε₀ > 0`, as
    `g(−3) = κ(−50 + (3675/16)φ) > 179κ` (M5). The ridge curve from `M` to `X = −3` stays above `f(S)` and ends above `b`.
    So `d_f(M) > f(S)` and `e = 0`.
  - *Case R⁻, `φ < −1`.* By (M1), `g + κ = κ(X − ½)²[2(X + 1) + 3φ(X + ½)²]`. On `[½, 2]` the bracket is at most
    `−(3X² + X − 5/4)`, which vanishes at `X = ½` and decreases for `X > −1/6`. So `g ≤ −κ` and `g_𝔉 < 0` on `[½, 2]`; on
    `[−3/2, ½]`, (M3) and (1.3′) give `g_𝔉 ≤ 0`. On the boundary of `𝒟′ = (−3/2, 2) × {|Ξ| < R′}`:
    `g_𝔉(−3/2) ≤ κ(−5 + 12φ) + ε₀ < −(5/4)κ` and `g_𝔉(2) ≤ κ(25/2 + (675/16)φ) + ε₀ < −(5/4)κ` (M5); and `𝔉 ≤ −(9/4)(κ + 1)`
    at `|Ξ| = R′`. #220's trap argument of Case R⁻, with `t* = −(5/4)κ`, gives `e = 0`. ∎

So Lemma Q′ needs neither #220's condition `8C₁𝒩r(1 + 5Γ) ≤ λ` nor `|φ| ≤ 1`. The first is the source of the term
`(𝒩r|γ|)^{1/2}` in #220's margin `λ₂`, and so of `κ²r^{3/2}` in #229 (CE⁺.1); the second is the source of `𝔅_5 = {|φ_r| > 1}`,
and so of `κ³r²`.

## 2. The elder cusp kernel with the candidate rate

*Proof of Proposition CE⁺⁺.* Take `r₂′ ≤ r₂ = min(r_0^*, 1/2, r_Q)` (#220 Lemma CE). For `κ ≤ 1`, #229 (CE⁺.1) already gives
(CE⁺⁺.1), since `κ²r^{3/2} + κ³r² ≤ 2r` when `κ, r ≤ 1`.
Let `κ ≥ 1`. Follow #229's proof of Lemma CE⁺, that is, #220's proof of Lemma CE with Steps E2⁺ and E3⁺, with Lemma Q′ in
place of Lemma Q in Step E1. Then #220 (2.3) holds with `𝔅′`, the event that (Q′1)–(Q′4) fail for `f = F_r` and
`𝒩 = 𝒩_r`, in place of `𝔅`. Steps E3⁺–E6 are unchanged and cost `CκrP^N + Cκ²r²P^N + Cr²(1 + κ)²P^N + Ck²(1 + |b|)^N`,
which is `≤ Cr(1 + κ)P^N` for `κr ≤ 1` (#229, control R6). It remains to show

    E_Q[w_κ(A, Y_r)1_{𝔅′}] ≤ C κ r P^N        (κ ≥ 1, κr ≤ 1).                                                  (2.1)

- *The typed window controls `Γ̃`.* On `{w_κ(A, Y_r) > 0}`, `A < 0` and `|Y_r| < 6κ|Δ|`. Since `Y_r = 6κΔφ_r + 3kΔ_B` and
  `|Δ_B|/|Δ| = |tr(A^{−1}B)| ≤ m‖B‖/λ`, `|φ_r| < 1 + rm‖B‖/(2λ)`. Also `|q| ≥ λΓ̃²` (as `−A ≥ λI`) and
  `3|q| ≤ |f₄| + 72κ|φ_r|`. Hence

      Γ̃² ≤ (|f₄| + 72κ)/(3λ) + 12κrm‖B‖/λ²        on {w_κ(A, Y_r) > 0}.                                        (2.2)

- *The conditions.* `r ≤ r₂′ ≤ r_Q` and `𝒩 ≥ 1`. Bound `Γ̃ ≤ |γ|/λ` in (Q′1)–(Q′2), and use (2.2) in (Q′3). As in #220's
  Step E2, (Q′1)–(Q′3) hold on `{w_κ(A, Y_r) > 0}` as soon as `κ ≥ C₂′𝒩r` and

      λ ≥ λ₂′ := C₂′ 𝒩 r (1 + |γ| + ‖B‖)(1 + |f₄|/κ),        C₂′ = C₂′(d, L).                                (2.3)

  In detail: (Q′1) holds if `λ ≥ 18𝒩r`, `λ ≥ 48𝒩r²`, `λ² ≥ (525/2)𝒩r²|γ|` and `λ ≥ 18^{2/3}2^{1/3}𝒩r` (the last from
  `r(κ + 1) ≤ 2`, as in #220), together with `λ ≥ (700/L)r²|γ|` and `λ ≥ (96/L)²r⁴(κ + 1)`; (Q′2) holds if `λ ≥ 2C₁𝒩r`
  and `λ ≥ (175/4)r|γ|` (with `r ≤ 1/10`); and by (2.2), (Q′3) holds if `κ ≥ 3520C₁𝒩r`, `λ ≥ 2347C₁𝒩r(|f₄| + 72κ)/κ` and
  `λ² ≥ 84480mC₁𝒩r²‖B‖`. Each is implied by (2.3) for a suitable `C₂′`, using `(𝒩x)^{1/2} ≤ 𝒩(1 + x)` and `r ≤ 1` (control X1
  records the constants). So

      𝔅′ ∩ {w_κ > 0} ⊂ 𝔅_λ′ ∪ 𝔅_κ′ ∪ 𝔅_4′,    𝔅_λ′ := {λ < λ₂′},  𝔅_κ′ := {κ < C₂′𝒩r},
      𝔅_4′ := {||φ_r| − 1/3| ≤ 2ε̃/(3κ)} ∖ (𝔅_λ′ ∪ 𝔅_κ′)   (as in #229).

- *`𝔅_4′`.* This is #229's (3.1) with `ε̃` in place of `ε*`. On `𝔅_4′ ∩ {w_κ > 0}`, (Q′3) holds, so `1/6 ≤ |φ_r| ≤ 1/2`, and `|f₄| ≥ 6κ` or
  `λ ≤ |γ|²/(2κ)` (#229 (3.2)); `𝔅_4′` puts `f₄` in two `J″`-measurable intervals (after #220's `𝒩`-layers) of total length
  `192ε̃`; and `Δ²(1 + Γ̃)² ≤ 2Δ² + 2|Jγ|²` is a polynomial in `J″`. #229's two pieces give `CκrP^N`.
- *`𝔅_κ′`.* `Cr³P^N`, as #220's `𝔅_κ`.
- *`𝔅_λ′`.* Put `t₁ := 2C₂′𝒩r(1 + |γ| + ‖B‖)`, so that `λ₂′ ≤ t₁max(1, |f₄|/κ)`, and use #220's `𝒩`-layers.
  - On `{λ < t₁}`, integrate `f₄` over the typed interval (length `144κ`), bound `Δ² ≤ t₁²‖A‖^{2m−2}`, and apply #220 (2.2)
    given `J‴`: the contribution is `≤ Cκ²E[t₁³(P + |J‴|)^N] ≤ Cκ²r³P^N ≤ CκrP^N`.
  - On `{t₁ ≤ λ < t₁|f₄|/κ}`, `w_κ ≤ 36κ²λ²‖A‖^{2m−2}` and `1 ≤ (t₁|f₄|/(κλ))^{5/2}`. So the contribution is at most
    `36κ^{−1/2}E[t₁^{5/2}|f₄|^{5/2}λ^{−1/2}‖A‖^{2m−2}] ≤ Cκ^{−1/2}r^{5/2}P^N`: by Hölder's inequality it suffices that
    `E[λ^{−3/4} | J‴] ≤ C(P + |J‴|)^n`, which is #218 Lemma D (1.1) in dyadic layers of `λ`. For `κ ≥ 1` this is `≤ CrP^N`.

This proves (2.1), hence (CE⁺⁺.1). ∎

## 3. The ridge and the decision to second order

The first-order part of the window field is the polynomial

    𝔔(X, Ξ) := (f₅/120)X(X² − ¼)² + (1/6)X(X² − ¼)η·Ξ + ½XΞᵀBΞ.                                                (3.0)

For #232's exact pinned family (2.4), in the window coordinates `x = rX`, `y = r²Ξ`, `r^{−4}(f − b) = 𝔓 + r𝔔 + (r²/4)X²ΞᵀCΞ`
(control X3).

**Lemma CU.1″ (second-order weighted Taylor bounds).** In the setting of §1 with `𝒩 ≥ max(1, ‖f‖_{C⁶})`, there is
`C₈ = C₈(d)` such that on `{|X| ≤ 3, r|Ξ| ≤ 1}`

    |𝔉 − 𝔓 − r𝔔| ≤ C₈𝒩r²(1 + |Ξ|)³,        |∂_Ξ(𝔉 − 𝔓 − r𝔔)| ≤ C₈𝒩r²(1 + |Ξ|)².                                (3.1)

*Proof.* This is #220's proof of Lemma CU.1′, one order further, with the same three sources.
- *Pin corrections.* With `𝒩 ≥ ‖f‖_{C⁶}`, the pinned jets differ from the values that produce `𝔓 + r𝔔` by `O(𝒩r⁵)` (`∂_uf`),
  `O(𝒩r⁴)` (`∂_u²f`, `∇_Θf`) and `O(𝒩r³)` (`∂_u³f`, `∇_Θ∂_uf`); `f(0)` cancels against `b = f(M)`. After rescaling they
  contribute `O(𝒩r²)(1 + |Ξ|)`.
- *Dropped monomials.* These are `x^iy^j` with `i + 2|j| ≥ 6` and `i + |j| ≤ 5`, with coefficients bounded by `C𝒩`. Each
  becomes `r^aX^iΞ^j` with `a = i + 2|j| − 4 ≥ 2` and `|j| ≤ a + 1`. On `r|Ξ| ≤ 1`, `r^a|Ξ|^{|j|} ≤ r²|Ξ|^{|j|−a+2}`, and
  `|j| − a + 2 ≤ 3`.
- *Remainder.* `|∂^αρ₆(x, y)| ≤ C𝒩(|x| + |y|)^{6−|α|}`; at `(rX, r²Ξ)`, `|x| + |y| ≤ 4r`, so `q` derivatives in `Ξ` give
  `C𝒩r^{2+q}`.

A derivative in `Ξ` lowers the power of `|Ξ|` by one. Control X3 checks on pinned polynomial fields in `d = 2, 3` that every
monomial `r^aX^iΞ^j` of `𝔉 − 𝔓 − r𝔔` has `a ≥ 2` and `|j| ≤ a + 1`. ∎

**Lemma R₂ (the ridge to second order).** Assume (Q′1)–(Q′2) and `𝒩 ≥ max(1, ‖f‖_{C⁶})`. For `X ∈ [−3, 2]`,

    |h(X) − rQ₁X(X² − ¼)²| ≤ ε₂′ := C₉[𝒩r²(1 + Γ̃)³ + 𝒩²r²(1 + Γ̃)²/λ],        C₉ = C₉(d).                       (3.2)

*Proof.* Write `𝔉 = 𝔓 + r𝔔 + ℜ`. By substitution, `𝔔(X, Ξ*(X)) = Q₁X(X² − ¼)²` (control X4).
- *Lower bound.* `g_𝔉(X) ≥ 𝔉(X, Ξ*) = g + rQ₁X(X² − ¼)² + ℜ(X, Ξ*)`.
- *Upper bound.* With `v := Ξ_𝔉 − Ξ*`, `𝔓(X, Ξ_𝔉) = g + ½vᵀAv ≤ g − (λ/2)|v|²`. `𝔔` is quadratic in `Ξ` with `∂_Ξ²𝔔 = XB`, so
  `r𝔔(X, Ξ_𝔉) ≤ r𝔔(X, Ξ*) + r|∂_Ξ𝔔(X, Ξ*)||v| + (3r/2)‖B‖|v|²`, and `(3r/2)‖B‖ ≤ (3/2)𝒩r ≤ λ/4` by (Q′1). Hence

      g_𝔉 − g − rQ₁X(X² − ¼)² ≤ |ℜ(X, Ξ_𝔉)| + r|∂_Ξ𝔔||v| − (λ/4)|v|² ≤ |ℜ(X, Ξ_𝔉)| + r²|∂_Ξ𝔔(X, Ξ*)|²/λ.

Here `|∂_Ξ𝔔(X, Ξ*)| = |(1/6)X(X² − ¼)η + XBΞ*| ≤ C𝒩(1 + Γ̃)`; and by (3.1) and (1.2′), `|ℜ| ≤ C₈𝒩r²(2 + 2M̃)³` at `Ξ*` and at
`Ξ_𝔉`, where `r|Ξ| ≤ 1`. ∎

**The model near the edges** (control X2). Put `δ_e := 1/96`, `J_± := {φ : |φ ∓ 1/3| ≤ δ_e}`, `X₃ := −1/(2φ)`,

    Ψ(φ) := (φ + 1)³(3φ − 1)/(16φ³) = (g(X₃) + κ)/κ,        Ψ₋(φ) := (φ − 1)³(3φ + 1)/(16φ³) = g(X₃)/κ          (3.3)

(#220 (M4)), `c₃ := 281/128` and `c₄ := (c₃/2)(9/44)²`. For `φ ∈ J₊`:
- `X₃ ∈ [−48/31, −16/11] ⊂ (−3, −5/4)`, and `g″ ≥ c₃κ` on `[−3, −5/4]` (`g″/(6κ) = 6φX² + 2X − φ/2` is decreasing in `X` and
  increasing in `φ` there, and equals `281/768` at `(φ, X) = (31/96, −5/4)`);
- `g′ ≥ 0` on `[X₃, −½]`, so `g ≥ g(−5/4) ≥ g(X₃) + c₄κ` on `[−5/4, −½]`; and `g(−3) ≥ 24κ`;
- `g ≤ −(κ/2)(X + ½)²` on `[X₃, ½]`; and (M2) holds on `[−½, 2]`, with `g(2) ≥ (125/64)κ`.

For `φ ∈ J₋` the mirror statements hold on `[½, 2]`: `X₃ ∈ [16/11, 48/31]`, `g″ ≤ −c₃κ` on `[5/4, 2]`, `g′ ≥ 0` on `[½, X₃]`,
so `g ≤ g(5/4) ≤ g(X₃) − c₄κ` on `[½, 5/4]`; `g(2) ≤ −(112/100)κ`; `|g(X₃)| ≤ κ/7`; `g + κ ≥ (κ/2)(X − ½)²` on `[−½, X₃]`; and
(M3) holds on `[−3/2, ½]` with `g(−3/2) ≤ −7κ`. Finally, for `|t| ≤ δ_e`,

    Ψ(1/3 + t) = 12t + Ψ₂(t)t²,  Ψ₋(−1/3 + t) = 12t + Ψ₂⁻(t)t²,  X₃(X₃² − ¼)² = ∓6 + ω_±(t)t  (φ = ±1/3 + t),       (3.4)

with `|Ψ₂|, |Ψ₂⁻| ≤ 90` and `|ω_±| ≤ 120`. (`Ψ(1/3 + t) = 12t − 81t² + …`, and on `J₊`, `X₃(X₃² − ¼)² = −6 + 99t + …`.)

**Lemma Q″ (the decision near the edges).** Assume (Q′1)–(Q′2) and `ε̃ ≤ c_eκ` with `c_e := 1/200`.
- (a) If `φ ∈ J₊`: `e = 1` if `min_{[−3,−½]}g_𝔉 < −κ`, and `e = 0` if `min_{[−3,−½]}g_𝔉 > −κ`. Moreover
  `min_{[−3,−½]}g_𝔉 = κΨ(φ) − κ + h(X₃) + θ` with `−ε₁²/(2c₃κ) ≤ θ ≤ 0`.
- (b) If `φ ∈ J₋`: `e = 1` if `max_{[½,2]}g_𝔉 > 0`, and `e = 0` if `max_{[½,2]}g_𝔉 < 0`. Moreover
  `max_{[½,2]}g_𝔉 = κΨ₋(φ) + h(X₃) + θ` with `0 ≤ θ ≤ ε₁²/(2c₃κ)`.
- (c) If moreover (3.2) holds and `ζ := r|Q₁|/κ ≤ c_e`, then with `t := φ ∓ 1/3` on `J_±`,

      e = 1{±t < rQ₁/(2κ)}    unless    |t ∓ rQ₁/(2κ)| ≤ ϑ := C₁₀[ζ² + ε₂′/κ + ε̃²/κ²].                        (3.5)

  In `z = 72κφ`: near both edges, `e = 1{|z| < 24κ + 36rQ₁}` unless `||z| − 24κ − 36rQ₁| ≤ 72κϑ`.

*Proof.* (a) *Location of the minimum.* `ε₀ ≤ ε̃ < c₄κ/2`. `min_{[−3,−½]}g_𝔉 ≤ g_𝔉(X₃) ≤ g(X₃) + ε₀`, while
`g_𝔉 ≥ g − ε₀ > g(X₃) + ε₀` on `[−5/4, −½]` and at `X = −3`. So every minimizer `X̂` lies in `(−3, −5/4)`, where `g″ ≥ c₃κ`
and `g′(X₃) = 0`. There `g(X̂) ≥ g(X₃) + (c₃κ/2)(X̂ − X₃)²` and `h(X̂) ≥ h(X₃) − ε₁|X̂ − X₃|`, so
`g_𝔉(X̂) ≥ g(X₃) + h(X₃) − ε₁²/(2c₃κ)`; and `g_𝔉(X̂) ≤ g_𝔉(X₃) = g(X₃) + h(X₃)`. With (3.3) this is the formula for the minimum.

*The decision.* Suppose `g_𝔉(X̂) < −κ`, and let `𝒟 := (X̂, ½) × {|Ξ| < R′}`.
- At `X = X̂`, `𝔉 ≤ g_𝔉(X̂) < −κ`. At `X = ½`, `𝔉 ≤ −κ`, with equality only at `S`.
- On `[X̂, ½]`, `g_𝔉 ≤ 0`. On `[X̂, −5/4]`, `g` is convex, so `g ≤ max(g(X̂), g(−5/4))`, with `g(X̂) < −κ + ε₀` and
  `g(−5/4) ≤ −9κ/32`; so `g_𝔉 ≤ g + ε₀ < 0`. On `[−5/4, ½]`, `g ≤ −(κ/2)(X + ½)²` and `|h| ≤ (ε₂/2)(X + ½)²`. So, at
  `|Ξ| = R′`, `𝔉 ≤ −(9/4)(κ + 1)` by #220 (1.4).

As in #220's Case E, the path component of `{f > f(S)}` containing `M` lies in `Φ(𝒟)` and has supremum `≤ b`, so
`d_f(M) ≤ f(S)`; and #220's path of Case E (on `[−½, 2]`, by (M2), (1.3′) and `g(2) ≥ (125/64)κ`) gives `d_f(M) ≥ f(S)`. So
`e = 1`. If instead `g_𝔉 > −κ` on `[−3, −½]`, the ridge curve from `M` to `X = −3` stays above `f(S)` and ends above `b`,
since `g_𝔉(−3) ≥ 24κ − ε₀ > 0`; so `e = 0`.

(b) The mirror argument on `[½, 2]`: maximizers `X̂` of `g_𝔉` lie in `(5/4, 2)`, and the formula is proved as in (a).
- If `g_𝔉(X̂) > 0`, the ridge curve from `M` through `S` to `X̂` stays at or above `f(S)`: on `[−½, X₃]`,
  `g_𝔉 + κ ≥ ((κ − ε₂)/2)(X − ½)² ≥ 0`, and between `X₃` and `X̂`, `g ≥ min(g(X₃), g(X̂)) ≥ −κ/7 − ε₀` (concavity on
  `[5/4, 2]`), so `g_𝔉 > −κ`. It ends above `b`, so `d_f(M) ≥ f(S)`; and (M3) with `g(−3/2) ≤ −7κ` gives #220's left trap,
  so `d_f(M) ≤ f(S)` and `e = 1`.
- If `g_𝔉(X̂) < 0`, then `g_𝔉 ≤ 0` on `[−3/2, 2]`, `g_𝔉(2) ≤ −(112/100)κ + ε₀ < −(111/100)κ` and `g_𝔉(−3/2) < −(111/100)κ`.
  #220's trap of Case R⁻, with `t* := −(111/100)κ`, gives `e = 0`.

(c) Take `J₊`. By (a), (3.3), (3.4) and (3.2): `e = 1` if `12κt + κΨ₂t² + rQ₁(−6 + ω₊t) + h₂ + θ < 0`, and `e = 0` if the
left side is `> 0`. Here `h₂ := h(X₃) − rQ₁X₃(X₃² − ¼)²`, so `|h₂| ≤ ε₂′`, and `−ε₁²/(2c₃κ) ≤ θ ≤ 0`. So
`e ≠ 1{t < rQ₁/(2κ)}` only if

    |12κt − 6rQ₁| ≤ 90κt² + 120r|Q₁||t| + ε₂′ + ε₁²/(2c₃κ) =: E(t).

On this event, `|t| ≤ δ_e` gives `90κt² ≤ κ|t|`, and `120r|Q₁| ≤ κ` as `ζ ≤ c_e`; so `10κ|t| ≤ 6r|Q₁| + ε₂′ + ε₁²/(2c₃κ)`,
that is `|t| ≤ C(ζ + ε₂′/κ + ε̃²/κ²)`. Substituting back, `12κ|t − rQ₁/(2κ)| ≤ E(t) ≤ Cκ(ζ² + ε₂′/κ + ε̃²/κ²)` when
`ε₂′ ≤ κ`; if `ε₂′ > κ`, then `ϑ ≥ C₁₀ ≥ 1 > |t ∓ rQ₁/(2κ)|` and (3.5) holds trivially. This is (3.5) on `J₊`. On `J₋` the same
computation with (b), `Ψ₋` and `ω₋` gives `e = 1{t > −rQ₁/(2κ)}` up to the same window. In `z`, `t = (z ∓ 24κ)/(72κ)`. ∎

Lemma Q″ (c) is the form for `d ≥ 2` of #238's Lemma W (W.2), where the window field is one-dimensional and the edges are
`±1/3 − η(∓3/2)/12` up to `O(ε²)`, `η` the perturbation of the field. Here the perturbation of the ridge is
`η = rQ₁X(X² − ¼)²`, and `−η(∓3/2)/(12κ) = ±rQ₁/(2κ)`.

## 4. The weight inside the elder window

**Lemma Ω.** (a) For `0 < r ≤ r_0^*` and `0 < k ≤ 1`, pathwise,

    det K_M = −6kΔ + rU − r²V + O(r³(1 + k)𝒩^N),    det K_S = 6kΔ + rU + r²V + O(r³(1 + k)𝒩^N),
    −det K_M det K_S = 36k²Δ² + r²(12kΔV − U²) + O(r⁴(1 + k)^N𝒩^N),                                              (4.1)

with `U := Y_r` and `V := (3k/4)(Δ_C + Δ_BB) + (f₄/24)Δ_B + (f₅/120)Δ − (1/12)γᵀJη − (1/8)γᵀJ_Bγ` (#232 (2.2)).

(b) As polynomials in the jets,

    36κ²Δ² + 12kΔV − U² = w₀ + 12kP₁ + 9k²[Δ(Δ_C + Δ_BB) − Δ_B²].                                               (4.2)

(c) `P₁ = Δ²Q₁` on `{A invertible}`; `P₁` and `Q₁` are `𝒫`-odd; `w₀` is `𝒫`-invariant.

*Proof.* (a) By #218 Step F1, applied to each factor and to the product, `det K_M`, `det K_S` and `−det K_M det K_S` equal
polynomials in `(J′; r, k)` up to `O(r³(1 + k)T^N)`, resp. `O(r⁴T^{n₀})` (#218 (2.1)). The coefficients are identities of
polynomials, which may be read off on exactly pinned polynomial fields. #232 (2.1)–(2.3) give the coefficients up to `r²`.
On pinned polynomial fields, `−det H(−r/2)det H(r/2)/r²` is even in `r`: the pinned jets that enter the Hessians are even in
`r` (#191 Lemma E Step 3: `det H_M(−r) = det H_S(r)`). So the product has no `r³` term. #220 replaces `T` by `𝒩_r` in
the same way, as in its own-jet form (F1). Control X3 checks the coefficients of `r⁰, …, r³` on pinned polynomial fields in
`d = 2, 3, 4`. #237 Lemma Π
states the same expansion.

(b) Expand `U² = (Y′ + 3kΔ_B)²` and `V = V_o + (3k/4)(Δ_C + Δ_BB)`. The first-order part is `k(12ΔV_o − 6Y′Δ_B)`, and

    12ΔV_o − 6Y′Δ_B = (Δ²/10)f₅ − ΔγᵀJη + (3/2)γᵀ(Δ_BJ − ΔJ_B)γ = 12P₁,

because `ΔJ_B = Δ_BJ − JBJ`: for invertible `A`, `J = ΔA^{−1}` gives `J_B = Δ_BA^{−1} − ΔA^{−1}BA^{−1}`, and the identity of
polynomials extends to all `A` (control X4).

(c) `J = ΔA^{−1}`; the parity of each monomial is read off its odd factors (control X4). ∎

So inside the elder window the weight is `w₀ + 12κrΔ²Q₁ + O(r² + k²)`. On `{A invertible}`, `V_o = ΔQ₁ + α₄Δ_B` with
`α₄ := z/24` (control X4), and `Y′ = 2Δα₄`: the first-order parts `12kΔV_o` of `12kΔV` and `−6kY′Δ_B` of `−U²` combine into
`12kΔ²Q₁`, a multiple of the same polynomial that moves the edges.

## 5. Proof of Theorem N

Fix `K = [κ₀, κ₁]`. Constants may depend on `K`, `d` and `L`. Take `r_K ≤ min(r_0^*, 1/2, r_Q, 1/κ₁)` small, write
`𝒩 = 𝒩_r`, and let `0 < r ≤ r_K`, `κ ∈ K` and `k = κr`.

*Step N1 (the good event).* Let `𝔊` be the event that
- `A < 0` and `λ ≥ λ₃ := C₁₁𝒩r(1 + |γ| + ‖B‖)(1 + |f₄|)`;
- `𝒩 ≤ c₁₁/r` (so `|f₅| ≤ c₁₁/r`);
- `|Δ| ≥ C₁₂r𝒩^{N₂}(1 + ‖B‖)`, `N₂ := max(N₁, m − 1)` (`N₁` of #220 (F1)),

with `C₁₁`, `C₁₂` large and `c₁₁` small. On `𝔊`:
- *Typing.* Case 1 of #218 Step C1 holds (`λ_max(A) < −r𝒩`, with `𝒩` in place of #218's `T` as in #220 (F2)), so the pair
  is typed iff `s·det K_M < 0 < s·det K_S` (`s = (−1)^m`). By #220 (F1), `s·det K_M = −6k|Δ| + r·sY_r + O(r²𝒩^{N₁})` and `s·det K_S = 6k|Δ| + r·sY_r + O(r²𝒩^{N₁})`, with
  `|Y_r| ≤ (|z|/12)|Δ| + 3κr|Δ_B|` and `|Δ_B| ≤ m𝒩^{m−1}‖B‖`. The margin on `|Δ|` gives: on `{|z| ≤ 30κ}` the pair is typed;
  every typed pair has `|φ_r| < 1 + C/(κ₀C₁₂) < 3`; and no pair is anti-typed (`s·det K_M > 0 > s·det K_S`).
- *The margins.* On typed pairs, `|φ_r| < 3`, so `Γ̃² ≤ |q|/λ ≤ (|f₄| + 216κ)/(3λ)`. So (Q′1)–(Q′3) hold with `ε̃ ≤ c_eκ`
  (as in §2), and `ζ = r|Q₁|/κ ≤ c_e`: `r‖B‖Γ̃² ≤ (1 + 216κ₁)/(3C₁₁)`, `r|η|Γ̃ ≤ ((1 + 216κ₁)c₁₁/(3C₁₁))^{1/2}` and
  `r|f₅| ≤ r𝒩 ≤ c₁₁`. Lemma Q′ decides `e` off `J₊ ∪ J₋` (`2ε̃/(3κ) < δ_e`), Lemma R₂ holds (`‖f‖_{C⁶} ≤ 𝒩`), and Lemma Q″
  decides `e` on `J_±`; off `J_±`, `1{|φ_r| < 1/3} = 1{|z| < 24κ + 36rQ₁}`, since `r|Q₁|/(2κ) ≤ c_e/2 < δ_e`.
- *The weight.* On typed pairs, `ω_r = −r^{−2}det K_M det K_S = w₀ + 12kP₁ + ε_ω` with `|ε_ω| ≤ C(r² + k²)𝒩^N`, by (4.1)–(4.2).
  Typed pairs with `|z| > 30κ` have `|φ_r| > 5/12`, so `e = 0`.

Put

    G_r(J′) := (w₀ + 12kP₁)1{A < 0, |z| < 24κ + 36rQ₁, r|Q₁| ≤ c_eκ}.                                         (5.1)

Since `36r|Q₁| ≤ 36c_eκ < 6κ`, the window of `G_r` lies in `{|z| < 30κ}`. Hence, on `𝔊`, `ω_re = G_r(J′) + ε_ω1{|z| < 24κ + 36rQ₁}`,
except on the edge windows `{||z| − 24κ − 36rQ₁| ≤ 72κϑ}` of (3.5).

*Step N2 (the exceptional events).*

    E_Q|ω_re − G_r(J′)| ≤ C r² P^N.                                                                           (5.2)

- *On `𝔊`.* `E|ε_ω| ≤ C(r² + k²)P^N`. For the edge windows, the integration in `f₄` needs an event that does not involve
  `f₄`. Put `𝔊″ := {A < 0, λ ≥ C₁₁𝒩r(1 + |γ| + ‖B‖), 𝒩 ≤ c₁₁/r, Γ̃² ≤ (1 + 216κ₁)/(3C₁₁𝒩r)}`; by the margins of Step N1,
  `𝔊 ∩ {typed} ⊂ 𝔊″`.
  - On `𝔊″`, `ζ ≤ c_e` and `ε̃ ≤ c_eκ` as in Step N1, and `ε₂′/κ ≤ C(C₁₁^{−1} + r^{1/2})/κ₀`. So `ϑ ≤ ϑ̄`, a small constant,
    and the edge windows are two `f₄`-intervals of length `144κϑ` within `(36c_e + 72ϑ̄)κ ≤ κ` of `3q ± 24κ`; after #220's
    `𝒩`-layers they are `J″`-measurable.
  - On `𝔊 ∩ {typed}`, `k|P₁| = κr|Q₁|Δ² ≤ c_eκ²Δ²`, so there `ω_r, |G_r| ≤ Cκ²Δ² + |ε_ω|`. The `|ε_ω|` part is bounded
    without the window. For `Cκ²Δ²1_{𝔊″}` on the windows, integrate `f₄` given `J″`. The powers of `Γ̃` in `ϑ` are at most
    four, besides `(1 + Γ̃)²/λ`. Use `Δ² ≤ λ²‖A‖^{2m−2}` and `Γ̃² ≤ |q|/λ`: `Δ²Γ̃⁴ ≤ ‖A‖^{2m−2}q²`,
    `Δ²Γ̃³ ≤ λ^{1/2}‖A‖^{2m−2}|q|^{3/2}` and `Δ²Γ̃²/λ ≤ ‖A‖^{2m−2}|q|`. On the windows, `f₄ = 3q ± 24κ + O(κ)`, and the
    Gaussian decay of the conditional density of `f₄` (#220 (F3)) gives `(1 + |q|)²sup_{windows}p_{f₄} ≤ C(1 + |m₄| + κ)²`.
    The windows cost `Cr²P^N`.
- *`A ≮ 0`.* `G_r = 0`. By #218 Step C1 (Cases 2 and 3), `E_Q[ω_r1{λ_max(A) ≥ −r𝒩}] ≤ Cr(k + r)²P^N ≤ Cr³P^N`.
- *`A < 0`, `λ < λ₃`.* By #220 (F2), `ω_r ≤ w_κ(A, Y_r) + Cr(1 + κ)𝒩^N`; and `|G_r| ≤ C(κ²Δ² + k|P₁|)1{|z| < 25κ}`. The `𝔅_λ′`
  computation of §2, with `λ₃` in place of `λ₂′`, gives `C(r³ + r^{5/2})P^N` for the terms `w_κ` and `κ²Δ²`. The terms
  `Cr(1 + κ)𝒩^N` and `k|P₁|` contribute `Cr·E[λ₃(…)] ≤ Cr²P^N`: since `λ₃` involves `f₄`, apply #218 Lemma D to `A` given
  `J′ ∖ {A}` (a Schur complement in `Cov_Q(J′)`, as in #220 (F5)).
- *`𝒩 > c₁₁/r`.* Probability `≤ C_pr^pP^p` (#220 (F4)), with polynomial weights: `Cr²P^N`.
- *`|Δ| < C₁₂r𝒩^{N₂}(1 + ‖B‖)`.* There `ω_r ≤ 36κ²Δ² + Cr𝒩^N` and `|G_r| ≤ 36κ²Δ² + Ck|P₁|`. By #218 Lemma D,
  `E[(1 + ‖A‖)^n1{|Δ| < ε} | J‴] ≤ C(P + |J‴|)^{n′}ε`; in `𝒩`-layers, this costs `Cr²P^N`.

*Step N3 (to the contact law).* `|G_r(j)| ≤ C(1 + |j|)^N`, since `w₀` and `P₁` are polynomials. By #220 (F6) and Lemma G (a),
`|E_Q[G_r] − E_{v_0(b,k)}[G_r]| ≤ Cr²P^N`.

*Step N4 (the expansion).* Under the contact law at `v_0(b, k)`, given all free jets except `f₄`, `f₄` is Gaussian with
variance `σ₄² ∈ [c, C]` and a mean `m₄` that depends only on the even jets (#220 (F3) at `r = 0`, and (F7)). Let `p_z` be the
conditional density of `z = f₄ − 3q`. With `δ := 36rQ₁`, `12kP₁ = (κΔ²/3)δ`, so `E[G_r | rest] = I(δ)1{|δ| ≤ 36c_eκ}`, where

    I(s) := ∫_{|z| < 24κ + s} [(Δ²/144)(5184κ² − z²) + (κΔ²/3)s] p_z(z) dz        (|s| < 24κ).

`I(0) = E[w_κ^{eld}(A, Y′) | rest]`, since `|Y′| < 2κ|Δ| ⟺ |z| < 24κ`. Since `w₀ = 32κ²Δ²` at `z = ±24κ`,

    I′(0) = Ψ_κ/36,        Ψ_κ := 1152κ²Δ²[p_z(24κ) + p_z(−24κ)] + 12κΔ²·P(|z| < 24κ | rest),                       (5.3)

and `δI′(0) = rQ₁Ψ_κ`. For `|δ| ≤ 36c_eκ`, `|I(δ) − I(0) − δI′(0)| ≤ ½δ²sup_{|s| ≤ 36c_eκ}|I″(s)|`, with
`|I″(s)| ≤ CΔ²(κ + κ²)sup_{23κ ≤ |x| ≤ 25κ}(p_z + |p_z′|)(x)`. For `|δ| > 36c_eκ`, `|I(0)| + |δI′(0)| ≤ |I(0)|(δ/(36c_eκ))² + C|δ|²Ψ_κ/κ`,
where `|I(0)| ≤ 36κ²Δ²·P(|z| < 24κ | rest)`. Now `p_z(x) = p_{f₄}(x + 3q)`, and
`Δ²δ² ≤ Cr²‖A‖^{2m−2}(f₅²λ² + |η|²|q|λ + ‖B‖²q²)`, by `|Q₁| ≤ |f₅|/120 + |η|Γ̃/12 + ‖B‖Γ̃²/8`, `Γ̃² ≤ |q|/λ` and
`Δ² ≤ λ²‖A‖^{2m−2}`. Every term above carries `p_z` or `P(|z| < 24κ | rest)` on `|z| ≤ 25κ`, so the Gaussian decay of
`p_{f₄}` in `q` absorbs the powers of `q`, as in Step N2. Hence

    E_{v_0(b,k)}[G_r] = E_{v_0(b,k)}[w_κ^{eld}(A, Y′)] + r·E_{v_0(b,k)}[Q₁Ψ_κ] + O(r²P^N).                          (5.4)

*Step N5 (parity).* By #220 (F7), under the contact law at `v_0(b, k)`, the even free jets `E` are independent of the odd
ones, `O ~ N(12kw, Σ_o)`. Write `Q₁Ψ_κ = G(E, O)`. `Q₁` is odd in `O`. `Ψ_κ` depends on `O` only through `q`, which is even,
because the conditional law of `f₄` depends only on `E`. So `G(e, −o) = −G(e, o)`, and `E_{v_0(b,0)}[Q₁Ψ_κ] = 0`. Moreover
`|Q₁Ψ_κ| ≤ C(1 + κ)²|P₁|·(1 + sup p_z) ≤ C(1 + |j|)^N`, so Lemma G (a), moving the odd mean from `0` to `12kw`, gives

    |E_{v_0(b,k)}[Q₁Ψ_κ]| ≤ C k (1 + |b|)^N.                                                                (5.5)

By #220 Step E6, `E_{v_0(b,k)}[w_κ^{eld}] = E_{v_0(b,0)}[w_κ^{eld}] + O(k²(1 + |b|)^N)`.

*Step N6 (assembly).* By [R] (R5), as in #220 Step E5, `|π_r(v_r) − π_0(v_0(b, k))| ≤ Cr²P²e^{−c(b² + k²)}`; by (F7),
`π_0(v_0(b, k)) = p_e(b, 0, 0)p_o(0, 12k, 0) = π_0(v_0(b, 0))e^{−a′k²}` for some `a′ > 0`; and `E_Q[ω_re] ≤ C(1 + κ)²P^N`.
With (5.2)–(5.5),

    r^{−2}A_r^{eld}(b, κr, u) = 12π_0(v_0(b, 0))E_{v_0(b,0)}[w_κ^{eld}(A, Y′)] + O(r²(1 + |b|)^Ne^{−cb²})
                              = 𝒜^{eld}(b, κ, u) + O(r²(1 + |b|)^Ne^{−cb²}),

using `rk = κr²`, `k² = κ²r²` and `P^Ne^{−ck²} ≤ C(1 + |b|)^N`. Also `r^{−2}A_0(b, κr, u) = 𝒜^{con}(b, κ, u)e^{−a′k²}` (#218
Step C3 and (F7): the even-jet law does not depend on `k`), and `𝒜^{con} ≤ Cκ²(1 + |b|)^Ne^{−cb²}`. Subtracting gives (N.1).

*Proof of (N.2).* The same steps, with the typed window in place of the elder window.
- *Step N1.* In Case 1, `ω_r = (−r^{−2}det K_M det K_S)₊ − (−r^{−2}det K_M det K_S)1_{anti}`: a typed pair has
  `det K_M det K_S < 0`, a pair that is neither typed nor anti-typed has `det K_M det K_S ≥ 0`. On `𝔊` there are no anti-typed
  pairs, so `ω_r = (w₀ + 12kP₁ + ε_ω)₊`.
- *Steps N2–N3* with `G_r^{cand} := (w₀ + 12kP₁)₊1{A < 0, r|Q₁| ≤ c_eκ}`, using `|(x + ε)₊ − x₊| ≤ |ε|`. Its support lies in
  `{|z| < 73κ}`.
- *Step N4.* `|(w₀ + ε)₊ − (w₀)₊ − ε1{w₀ > 0}| ≤ |ε|1{|w₀| ≤ |ε|}` with `ε = 12kP₁`. Since `5184κ² − z² = (72κ − |z|)(72κ + |z|)`,
  `{|w₀| ≤ 12k|P₁|}` puts `z` in two windows of half-width `24r|Q₁|` around `±72κ`, and the Gaussian decay of Step N2 gives
  `O(κr²P^N)`. So `E[G_r^{cand} | rest] = E[w_κ(A, Y′) | rest] + rQ₁Ψ_κ^{cand} + O(r²…)` with
  `Ψ_κ^{cand} := 12κΔ²P(|z| < 72κ | rest)`, which is `𝒫`-invariant. There is no edge term, because the typed weight vanishes
  at the edges of the typed window.
- *Step N5.* (5.5) holds for `Ψ_κ^{cand}`, and `E_{v_0(b,k)}[w_κ(A, Y′)] = E_{v_0(b,0)}[w_κ(A, Y′)] + O(k²(1 + |b|)^N)` by #220
  Lemma G (b), as in #218 Step C3 with #229 Lemma L.
- *Step N6* as above. ∎

## 6. Proof of Corollary N′

Let `r₋ := (ℓ/κ₁)^{1/4}` and `r₊ := (ℓ/κ₀)^{1/4}`, and take `ℓ` so small that `r₊ ≤ r_K` for `K = [κ₀, κ₁]`. For `r ∈ [r₋, r₊]`,
`κ := ℓ/r⁴ ∈ K` and `ℓ/r³ = κr`. By (N.1), (N.2) and Step N6,

    r^{−2}A_r^*(b, ℓ/r³, u) = 𝒜^*(b, ℓ/r⁴, u) + O(r²(1 + |b|)^Ne^{−cb²})        (* ∈ {eld, cand}),

and the difference gives `* = rej`. Integrate over `u`, `b` and `r ∈ [r₋, r₊]`. With `r = ℓ^{1/4}s`,
`∫_{r₋}^{r₊}𝒜^*(b, ℓ/r⁴, u) dr = ℓ^{1/4}∫_{κ₁^{−1/4}}^{κ₀^{−1/4}}𝒜^*(b, s^{−4}, u) ds`, and the error is at most
`C∫_{r₋}^{r₊}r² dr ≤ (C/3)κ₀^{−3/4}ℓ^{3/4}` (control X6). ∎

## 7. Remarks

1. **Where the argument stops.** Theorem N is a statement at fixed `κ`. The linear term `rE[Q₁Ψ_κ]` is `O(rk)` for *every*
   `κ` by (5.5), so formally the elder kernel has no `O(r)` term at any `κ`, and the formal `ℓ^{1/2}` term of #218 §0 and
   #229 §0 does not arise from the cusp scale. What is not uniform is the remainder.
   - *`κ → ∞` (the fold side).* In the soft region `λ ≈ |γ|²/κ`, `Γ̃ ≈ κ/|γ|`, and the edge shift `rQ₁/(2κ)` has size
     `≈ k‖B‖/|γ|²` instead of `r`: the expansion is in `k`, not in `r`. At the fold scale `k ≍ 1` the decision in this
     region depends on the higher transverse jets: with `Ξ ≈ κ`, the monomial `r²Ξ³` of the window field has relative size
     `≈ k²`. The constants of Theorem N grow polynomially in `κ`, which is not enough for #229's ledger at `ρ_f`.
   - *`κ → 0` (the intermediate side).* The elder window has width `48κ` in `f₄`, and the edges move by `36r|Q₁|`. For
     `κ ≲ r` the expansion does not apply, and the intermediate elder mass is #229's `O(ℓ^{4/9}log(1/ℓ))`.
   - *What would follow from uniformity.* Suppose (N.1) held with error `C(r² + k²)` uniformly for `r ≤ κ ≤ 1/r`. Then #229's
     decomposition, with `ρ_c = ℓ^{1/5}` and #237's Lemma K for the finite part, would give the elder density with remainder
     `O(ℓ^{4/9}log(1/ℓ))`, from the intermediate separations. It would not go beyond `ℓ^{1/2}`: the fold family `ρ_f⁵/ℓ`
     would balance `ℓ²ρ_f^{−5}` at `ℓ^{1/2}` (control X6). Going beyond `ℓ^{1/2}` needs, as for the candidate in #237, a
     uniform two-scale description that removes the fold family, here including the rejected fold mass of [C7-K] (K2).
2. **#229's ledger.** With (CE⁺⁺.1) in place of (CE⁺.1), the rows `ℓ²ρ_f^{−11/2}` and `ℓ³ρ_f^{−9}` of #229 §5 disappear. The
   elder's fold and cusp rows are then the candidate's; the elder keeps its intermediate rows (`ℓ^{4/9}log(1/ℓ)`). The least
   exponent is still `3/7`, from `ρ_f⁵/ℓ` against `ℓρ_f^{−2}` (control X6). #229 Remark 1 observed that for the elder density Lemma Q's bad events would become the obstruction once the linear
   pair is resolved; after Proposition CE⁺⁺ they no longer are.
3. **Numerical evidence** (exploration; project archive `V2_2/frontiers_elder_cusp_parity_20261002/exploration/`; not part of
   the proof). `d = 2`, Gaussian kernel `e^{−|z|²/2}`.
   - *Quadrature* (`cusp_quad.py`). `𝒜^{cand}` and `𝒜^{eld}` under the contact law. At `(b, κ) = (0, ½), (0, 1), (0, 2), (1, 1)`:
     `𝒜^{cand} = 0.119692, 0.495998, 2.003851, 0.640405` and `𝒜^{eld} = 0.111331, 0.489836, 2.000088, 0.637500`.
   - *Monte Carlo of the kernels at `r > 0`* (`elder_f4int.py`). The free jets of order `≤ 8` are sampled under the exact pinned
     law, with common random numbers across `r ∈ {0.005, 0.01, 0.015, 0.02, 0.03, 0.04}` and antithetic odd jets
     (`N = 20000`). The pinned jets are solved from the pin rows, `f₄` is integrated in closed form, and the elder set in `f₄`
     is an interval found by bisection on the ridge conditions. Cubic fits `g₀ + g₁r + g₂r² + g₃r³` give `g₀` within `0.3`
     standard errors of the quadrature for the candidate and the elder kernels, and within `0.9` standard errors for the
     rejected kernel at `b = 0` (`2.1` at `b = 1`).
   - *The linear coefficient.* For the rejected kernel, `g₁/𝒜^{cand} = +0.007 ± 0.006, +0.003 ± 0.007, +0.003 ± 0.009,
     −0.003 ± 0.003` at the four points: consistent with zero. (Relative to the rejected kernel itself the uncertainties
     are `±0.09` at `κ = ½` up to `±5` at `κ = 2`.) The natural scale is the absolute first-order integrand `E|Q₁Ψ_κ^{rej}|`
     (`first_order_scale.py`): `0.020, 0.031, 0.040, 0.016`. Relative to it, the fitted `g₁` is `0.04 ± 0.04` at `κ = ½`.
   - *The candidate's cubic fit.* Its `g₁` is `19`–`44` standard errors from zero for `κ ≥ 1` (up to `0.03` relative), a fit
     artefact: with `g₀ + g₁r + g₂r² + g₄r⁴` instead, the point estimates drop to `−6·10⁻⁵`, `−2.5·10⁻³` and `−5.5·10⁻⁵`
     (`κ = 1`, `κ = 2`, and `b = 1`), at most `1.3·10⁻³` relative.
4. **The Monte Carlo of #216** (project archive `V2_2/numerics_lifetime_mc_20261001/results/mc{2,3}_final.json`; `altfit.py`).
   #237 Remark 4 found that the elder and rejected residuals about the three-term law are not consistent with zero, with an
   `ℓ^{1/2}` coefficient in joint `ℓ^{1/2} + ℓ^{3/4}` fits. On `[10⁻⁴, 0.3]` (19 bins, 17 degrees of freedom), the fits
   `ℓ^{1/2} + ℓ^{3/4}` and `ℓ^{2/3} + ℓ^{3/4}` are comparable, with `χ²` in that order: `10.4` and `11.9` (elder, `d = 2`), `18.0`
   and `20.6` (rejected adjacent pairs, `nR`, `d = 2`), `8.0` and `6.9` (elder, `d = 3`), `8.1` and `9.3` (rejected adjacent
   pairs, `d = 3`); `|Δχ²| ≤ 2.6`. On this range `ℓ^{2/3}` and `ℓ^{3/4}` are nearly collinear: their fitted amplitudes
   (`±0.14` to `±0.22`) cancel. The data do not single out `ℓ^{1/2}`, and Theorem N gives no reason to expect it from the
   cusp scale.
5. **Consistency.**
   - (CE⁺⁺.1) implies #229 (CE⁺.1), which implies #220 (CE.1).
   - (N.2), integrated in `b`, agrees with #237's cusp-scale consequence of Lemma U (`O((1 + κ)²r²)`).
   - Lemma Ω (a) is #237 Lemma Π, and #232 (2.3) with the `r³` term removed by evenness. Since `V_o = ΔQ₁ + α₄Δ_B`, #232's `V`
     contains `Q₁` as well.
   - Lemma Q″ is the `d ≥ 2` form of #238 Lemma W.

## 8. Sources (exact identities in `SOURCES.json`)

| Tag | Path | Role |
|---|---|---|
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`) | (R2)–(R5): pin densities, moments — consumed |
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`) | §2 finite-jet rank, §15 parity factorization, through #218 and #220 — consumed |
| #191 | `frontiers/remainder_vanishing_20260930/PROOF.md` (blob `441152df`) | Lemma E Step 3 (evenness) — consumed |
| #207 | `frontiers/cusp_second_order_20261001/PROOF.md` (blob `f6df5a73`) | §0, (0.2), Theorem CU.2, Proposition CU.3, (4.1) — consumed |
| #218 | `frontiers/candidate_third_order_20261001/PROOF.md` (blob `70ca57ef`) | Lemma D, (1.2), Step F1, Step C1, Step C3 — consumed |
| #220 | `frontiers/elder_third_order_20261001/PROOF.md` (blob `c8767dde`) | §1 (Lemma CU.1′, Lemma S, Lemma Q, (M1)–(M6)); §2 ((F1)–(F7), Lemma G, Lemma CE) — consumed |
| #229 | `frontiers/third_order_rate_20261001/PROOF.md` (blob `110ed33a`) | Lemma L, Lemma CE⁺, §5 — consumed |
| #232 | `frontiers/c2_finite_jet_transfer_20261001/PROOF.md` (blob `54cc4a1a`) | §2 (2.1)–(2.4) — consumed |
| #237 | `frontiers/candidate_parity_rate_20261001/PROOF.md` (open PR; blob `a97bf528`) | Lemma Π, Lemma K, Lemma U, Remarks 3–4 — cited |
| #238 | `frontiers/d1_sharp_remainder_20261001/PROOF.md` (open PR; blob `3b2ec970`) | Lemma W — cited |
| #216 | `frontiers/third_order_coefficient_20261001/NOTE.md` (open PR) | Monte Carlo — cited |

## 9. Exact controls (`ecp_check.py`; stdlib; exact rationals; byte-identical under `-O` and on CPython 3.10–3.14)

- **X1** Lemma Q′ and Proposition CE⁺⁺: the polynomial bounds for `ε₀`, `ε₁`, `ε₂` and the constant `220` (exact polynomial
  arithmetic); `|q| ≥ λΓ̃²` and the Frobenius-norm form of `|tr(A^{−1}B)| ≤ m‖B‖/λ` on random negative definite rational
  matrices (`m = 1, 2, 3`); `κ²r^{3/2} + κ³r² ≤ 2r` on a rational grid; and, as recorded arithmetic that cannot fail,
  `ϱ ≤ 4(1 + M̃)`, the slack on `|Ξ| = R′`, the constants of (2.3) and the exponents of the `5/2`-power step.
- **X2** the model ridge: (M1), (M4) and (3.3) as identities; the new cases of Step Q6′; on `J_±`, the constants `c₃` and `c₄`,
  the bounds on `g(−3)`, `g(2)`, `g(−3/2)`, `g(X₃)` and the brackets, by exact monotonicity; the expansions (3.4) with
  `|Ψ₂|, |Ψ₂⁻| ≤ 90` and `|ω_±| ≤ 120`.
- **X3** pinned polynomial fields: in `d = 2, 3` with `k = κr`, the window field `𝔓 + r𝔔 + O(r²)`, with every monomial of
  `𝔉 − 𝔓 − r𝔔` having `a ≥ 2` and `|j| ≤ a + 1`, and #232's family (2.4) in window coordinates and with its pins; in
  `d = 2, 3, 4` at fixed `k`, Lemma Ω (a): the coefficients of `r⁰, …, r³` of `det K_M`, `det K_S` and `−det K_M det K_S`.
- **X4** the identities of Lemma Ω (b)–(c): `ΔJ_B = Δ_BJ − JBJ` (`m = 1, 2, 3`, including singular `A`), (4.2), `P₁ = Δ²Q₁`,
  `V_o = ΔQ₁ + α₄Δ_B`, `𝔔(X, Ξ*) = Q₁X(X² − ¼)²`, and the parities.
- **X5** the first-order bookkeeping: `w₀(±24κ) = 32κ²Δ²`, `12kP₁ = (κΔ²/3)·36rQ₁`, the edge shift `36rQ₁` in `z` from
  `rQ₁/(2κ)` in `φ`, the linear edge equations, `I′(0) = Ψ_κ/36` on polynomial test densities, and the half-width `24r|Q₁|`
  of the candidate's kink windows.
- **X6** Corollary N′ and the ledgers: the substitution `r = ℓ^{1/4}s`; `∫_{r₋}^{r₊}r²dr ≤ κ₀^{−3/4}ℓ^{3/4}/3`; #229's ledger
  with and without the elder rows (least exponent `3/7` at `ρ_f = ℓ^{2/7}` in both); the conditional ledger of Remark 1.

Mutants, each breaking one control: `M1` (X3: `f₅/60` in `𝔔`), `M2` (X4: the sign of `ηᵀA^{−1}γ/12` in `Q₁`), `M3` (X5: the
edge shift `18rQ₁`), `M4` (X2: `|ω_±| ≤ 100`), `M5` (X1: the constant `200`), `M6` (X3: the saddle at `r/2 + r⁴`, which breaks
the evenness in Lemma Ω (a)), `M7` (X6: `ρ_f = ℓ^{1/4}`). An unknown mutant label exits `2`.

## 10. Review slices

- **A** §§1–2: Lemma Q′ (Steps Q2′ and Q6′) and Proposition CE⁺⁺ (the conditions (2.3) and the three bad events).
- **B** §3: Lemma CU.1″, Lemma R₂, the model near the edges and Lemma Q″.
- **C** §4 and Steps N4–N5: Lemma Ω, the identity `12ΔV_o − 6Y′Δ_B = 12P₁`, the expansion (5.4) and the parity (5.5).
- **D** Steps N1–N3 and N6, and (N.2): the good event, the exceptional events (5.2) and the candidate case.
- **E** §§6–7 and the controls: Corollary N′, the ledger remarks and the exploration.
