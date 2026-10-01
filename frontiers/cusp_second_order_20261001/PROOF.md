# The cusp crossover: the elder rule at `r ≍ k` and the second-order term `ν_eld(ℓ) = cℓ^{−1/3} + c₁ℓ^{1/4} + o(ℓ^{1/4})`

Object: CL-CUSP-SECOND-ORDER-20261001-v1.1 (v1 → v1.1, before any review: v1's formal Remark 2 is proved — Theorem CU′,
the candidate and rejected densities to order `ℓ^{1/4}`, §7, through the gap-Lipschitz Lemma L; a clean-context referee pass
on §7 found no error or gap and seven minor points, all applied; Lemma CU.5's window-length bound repaired after Codex
P1 4150765060 (the root difference is bounded symmetrically through the sign window); checker C8 and mutant M5 added;
§§1–6 otherwise unchanged except one clarifying clause in §4 (iv); remarks, sources, controls and slices renumbered
§§8–11).
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 1 October 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register,
graph, STATUS, PROOF_INDEX, prize or Boolean change; the numerical values of §8 are exploration, not certified.
Same GitHub account as every lane; zero organizational independence.
**Dependencies (unmerged, consumed):** Math- #191 (`frontiers/remainder_vanishing_20260930/PROOF.md`, v1.1 blob
`441152df`: Lemma E (E.1) and Steps 1–3 with its dominating variable `T`, §2 (2.1), the admissible radius `r_0^*`) and
Math- #198 (`frontiers/remainder_rate_20260930/PROOF.md`, v1.1 blob `abfb98ae`: §1 the elder-density identity and
Lemma B (B.2), §2 Lemma F′, §3 (3.1)–(3.2) and Lemma W). This note cannot be integrated before both and must be rebound
if either changes. Merged inputs: [R], [C7-K], [P] with [E1]/[E2]/[REC] directly; [Z] directly in §7 ((Z2)–(Z3), (Z10),
the [P] §14 input of (Z16)) and transitively ((Z10), (Z13)–(Z14) and `r_0^{[Z]}`, inside #198 and #191); [182] (the
deterministic barrier, inside #198 Lemmas B and F′; its §3 has a Slice-A acceptance from this same author only)
transitively.

## 0. Statement

Setting and notation are those of [R] (`frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf`),
#191 §0 and #198 §0: fixed `d ≥ 2`, `m = d − 1`, `L > 0`, the [P] field on `X = R^d/(LZ^d)`; near pins `M = −ru/2`,
`S = ru/2` at heights `b`, `b − kr³` with zero gradients; the regression law `Q = Q_{r,b,k}` and the coupling
`(F_r, F_0)` of [R] (R3)–(R4); `P = 1 + |b| + k`; the typed weight `W_r` with `W_r/r² = F_d(K_M)F_{d−1}(K_S)`; the elder
mark `e = 1{d_f(M) = f(S)}` for the maximin `d_f(M) = sup{min_t f(γ(t)) : γ(0) = M, f(γ(1)) > f(M)}` ([P] §8, Borel by
[E2] §9); the kernels

    A_r = 12π_r(v_r)E_Q[W_r/r²],   A_r^{eld} = 12π_r(v_r)E_Q[(W_r/r²)e],   A_0 = 12π_0(v_0)z_0,

so that ([P] (10.2), #191 (2.1), #198 §1) `ν_eld(ℓ) = ∫_0^{r_0^*}∫_R∫_{S^{d−1}} r^{−2}A_r^{eld}(b, ℓ/r³, u) dσ db dr + ν_eld^{far,r_0^*}(ℓ)`
and `cℓ^{−1/3} = ∫_0^∞∫∫ r^{−2}A_0(b, ℓ/r³, u) dσ db dr`, `c = c_{d,L}` of [P] (15.2), `r_0^*` the admissible radius of #191 §0.

**Cusp variables.** `κ := k/r = ℓ/r⁴` and `s := rℓ^{−1/4} = κ^{−1/4}`. The gap is `ℓ = kr³ = κr⁴`: the scale `r ≍ k`
is the scale at which the height gap is quartic in the separation.

**Jets.** For a `C⁵` function `f`, in the frame `(u, Θ)` of the pair: `f₄ := ∂_u⁴f(0)`, `γ := ∇_Θ∂_u²f(0) ∈ R^m`,
`A := D_Θ²f(0) ∈ Sym(m)`, `Δ := det A`,

    Y := (f₄/12)Δ − γᵀadj(A)γ/4,        φ := Y/(6κΔ) = (f₄ − 3γᵀA^{−1}γ)/(72κ)   (A invertible).        (0.1)

(`Y` is #191's `Y` at `k = 0`; it is a scalar.) `E₀[· | b]` denotes expectation over the jets of `F₀` under the contact
law at the zero-gap target `v₀(b, 0)`, i.e. given `f(0) = b`, `∂_uf(0) = ∂_u²f(0) = ∂_u³f(0) = 0`,
`∇_Θf(0) = ∇_Θ∂_uf(0) = 0`.

**Theorem CU (second-order term of the elder lifetime law).** For every `d ≥ 2`, `L > 0`, for the canonical marked
Kac–Rice version of the elder density ([P] §9 read as [E2]),

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + o(ℓ^{1/4})        (ℓ ↓ 0),                                        (CU.1)
    c₁ = −(192/7)·2^{1/4} ∫_{S^{d−1}}∫_R π₀(u; v₀(b,0)) E₀[|Y|^{7/4}|Δ|^{1/4}1{A < 0} | b] db dσ(u)  ∈ (−∞, 0).   (CU.2)

Equivalently, with the parity factorization of [P] §15 (odd and even jets are independent),
`c₁ = −(192/7)2^{1/4}∫_{S^{d−1}} p_G(0)p_{V_u}(0)(2π)^{−1/2}τ_u^{−1} E[|Y|^{7/4}|Δ|^{1/4}1{A<0} | V_u = 0, G = 0, t_u = 0] dσ(u)`,
`G = ∇f(0)`, `V_u = (∂_u²f, ∇_Θ∂_uf)(0)`, `t_u = ∂_u³f(0)`, `τ_u² = Var(t_u | G = 0)`. So
`ν_eld(ℓ) = cℓ^{−1/3}(1 + (c₁/c)ℓ^{7/12} + o(ℓ^{7/12}))`; for the manuscript's field (`d = 3`, `L = 24`) the exploration of
§8 gives `c₁ ≈ −0.21185`, `c₁/c ≈ −5.071`.

**Theorem CU′ (the candidate and rejected densities; §7).** Under the same hypotheses, with `B_{d,L}` the equal-height
mass of [Z] (Z3),

    ν_cand(ℓ) = c ℓ^{−1/3} + B_{d,L} + I^{cand} ℓ^{1/4} + o(ℓ^{1/4}),        I^{cand} = (3^{1/4}/2) c₁ < 0,                (CU′.1)
    ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁) ℓ^{1/4} + o(ℓ^{1/4}),               I^{cand} − c₁ = (1 − 3^{1/4}/2)|c₁| > 0.       (CU′.2)

The far pairs contribute `O(ℓ)`: the `ℓ^{1/4}` terms are carried by the cusp scale. The candidate density needs no elder
decision, and its non-cusp remainder is Lipschitz in the gap because the gap enters the pinned law affinely (Lemma L).

The mechanism is a **cusp crossover**: rescaled at `x = rX` (axis), `y = r²Ξ` (transverse, `Ξ ∈ R^m`), heights `r⁴`,
the pinned field converges to the random polynomial

    𝔓(X, Ξ) = 2κ(X + ½)²(X − 1) + (f₄/24)(X² − ¼)² + ½(X² − ¼)γ·Ξ + ½ΞᵀAΞ                                (0.2)

(Theorem CU.1), whose superlevel topology reduces exactly to the quartic ridge
`g(X) = κ[2(X + ½)²(X − 1) + 3φ(X² − ¼)²]` (Theorem CU.2). For `𝔓`, the pair is typed iff `|φ| < 1` — the sign window
of #198 Lemma W — and **`S` is `M`'s elder partner iff `|φ| < 1/3`**: the elder window is exactly one third of the typed
window, its boundary being the configurations in which the two competing saddles (`φ = 1/3`) or maxima (`φ = −1/3`)
have equal heights, `g(X₃) + κ = κ(φ + 1)³(3φ − 1)/(16φ³)` and `g(X₃) = κ(φ − 1)³(3φ + 1)/(16φ³)`. The model's decision
is stable (Proposition CU.3), so the elder kernel at fixed `κ` converges (Theorem CU.4); a window-probability bound
(Lemma CU.5) controls the intermediate separations; and the cusp integral gives (CU.2), with
`∫_0^∞ loss ds = (16/7)2^{1/4}|Y|^{7/4}|Δ|^{1/4}`.

**What is not claimed.** No rate for the `o(ℓ^{1/4})` in (CU.1), (CU′.1) or (CU′.2); no certified numerical value of
`c₁`, `I^{cand}` or `B_{d,L}` (§8 is exploration); no uniformity in `d`, `L`; no finite-radius band; nothing beyond
the existential scope of Theorem R, [Z], #191 and #198. Conditional on #191, #198 and this note's review, the exponent
question left in #198 Remark 1 is settled: `1/4` is the true order and the coefficient is negative.

## 1. The cusp limit field

**Theorem CU.1.** Let `f ∈ C⁵(X)`, `0 < r ≤ 1`, `κ > 0`, and let `M = −ru/2`, `S = ru/2` be critical points of `f` with
`f(M) = b`, `f(S) = b − κr⁴`. For `R ≥ 1` with `2Rr ≤ L/4`, put `𝒲_R := [−R, R] × {|Ξ| ≤ R}` and
`𝔉(X, Ξ) := r^{−4}[f(rXu + r²ΘΞ) − b]`. Let `𝔓` be (0.2) with the jets `(f₄, γ, A)` of `f` at `0`. Then

    ‖𝔉 − 𝔓‖_{C²(𝒲_R)} ≤ C(d, R) r ‖f‖_{C⁵}.                                                         (1.1)

*Proof.* Write `ϑ_j := ∂_u^jf(0)`, `ψ_j := ∂_u^j∇_Θf(0)` (so `ϑ₄ = f₄`, `ψ₂ = γ`), `h := r/2`, `N := ‖f‖_{C⁵}`.
Taylor's formula along the axis, `ϑ(x) := f(xu) = Σ_{j≤4}ϑ_jx^j/j! + ρ(x)` with `|ρ| ≤ N|x|⁵/120`, `|ρ'| ≤ N|x|⁴/24`, and
the pins `ϑ'(±h) = 0`, `ϑ(−h) = b`, `ϑ(h) = b − 16κh⁴` give successively
`ϑ'(h) − ϑ'(−h) = 2ϑ₂h + ϑ₄h³/3 + O(Nh⁴) = 0`, `ϑ'(h) + ϑ'(−h) = 2ϑ₁ + ϑ₃h² + O(Nh⁴) = 0`,
`ϑ(h) − ϑ(−h) = 2ϑ₁h + ϑ₃h³/3 + O(Nh⁵) = −16κh⁴` and `ϑ(h) + ϑ(−h) = 2ϑ₀ + ϑ₂h² + ϑ₄h⁴/12 + O(Nh⁵) = 2b − 16κh⁴`, hence

    ϑ₂ = −(r²/24)f₄ + O(Nr³),   ϑ₃ = 12κr + O(Nr²),   ϑ₁ = −(3/2)κr³ + O(Nr⁴),   ϑ₀ − b = (−κ/2 + f₄/384)r⁴ + O(Nr⁵).

The transverse pins `ψ(±h) = 0` for `ψ(x) := ∇_Θf(xu) = ψ₀ + ψ₁x + γx²/2 + ψ₃x³/6 + O(N|x|⁴)` give
`ψ₀ = −(r²/8)γ + O(Nr⁴)` and `ψ₁ = O(Nr²)`. Expand `f` at `0` to total order 4 in `(x, y)`: the remainder `ρ₅` satisfies
`|∂^αρ₅(x, y)| ≤ CN(|x| + |y|)^{5−|α|}` (`|α| ≤ 2`), and at `(x, y) = (rX, r²Ξ)`, `(X, Ξ) ∈ 𝒲_R`, `|x| + |y| ≤ 2Rr`; with
`∂_X = r∂_x`, `∂_Ξ = r²∂_y`, every derivative of order `≤ 2` of `r^{−4}ρ₅(rX, r²Ξ)` is `O(C_R N r)`. The Taylor monomials
`x^iy^j` with weighted degree `i + 2|j| ≥ 5` contribute `O(C_R N r)` in `C²(𝒲_R)` likewise. The monomials of weighted
degree `≤ 4` are `(i, |j|) ∈ {(0,0), (1,0), (2,0), (3,0), (4,0), (0,1), (1,1), (2,1), (0,2)}`; inserting the pinned values,

    r^{−4}[ϑ₀ − b + ϑ₁rX + ϑ₂r²X²/2 + ϑ₃r³X³/6 + f₄r⁴X⁴/24 + ψ₀·r²Ξ + ψ₁·r³XΞ + γ·r⁴X²Ξ/2 + r⁴ΞᵀAΞ/2]
      = [−κ/2 − (3/2)κX + 2κX³] + (f₄/24)[1/16 − X²/2 + X⁴] + [−γ·Ξ/8 + γ·X²Ξ/2] + ½ΞᵀAΞ + O(C_R N r),

and `−κ/2 − (3/2)κX + 2κX³ = 2κ(X + ½)²(X − 1)`, `1/16 − X²/2 + X⁴ = (X² − ¼)²`, `−γ·Ξ/8 + γ·X²Ξ/2 = ½(X² − ¼)γ·Ξ`. ∎

(Checker C4 verifies, exactly, that for pinned polynomials of degree 6 in `d = 2, 3` the Laurent polynomial
`r^{−4}[f(rX, r²Ξ) − b]` has no negative powers of `r` and constant term exactly `𝔓(X, Ξ)`. A referee pass also checked
the `O(r)` rate on a non-polynomial field.)

## 2. The model: fiber reduction and the elder window

**Theorem CU.2.** Let `κ > 0`, `f₄ ∈ R`, `γ ∈ R^m`, `A ∈ Sym(m)` negative definite; `𝔓` as in (0.2); `φ`, `Y` as in
(0.1); `X₃ := −1/(2φ)` for `φ ≠ 0`.

(a) *(Fiber reduction.)* `𝔓(X, Ξ) = g(X) + ½(Ξ − Ξ*(X))ᵀA(Ξ − Ξ*(X))`, with `Ξ*(X) := −½(X² − ¼)A^{−1}γ` and

    g(X) = κ[2(X + ½)²(X − 1) + 3φ(X² − ¼)²],        g'(X) = 6κ(X² − ¼)(1 + 2φX).                           (2.1)

(b) *(Critical points, types.)* The critical points of `𝔓` are `(X, Ξ*(X))` with `g'(X) = 0`: `M = (−½, 0)`, `S = (½, 0)`
and, for `φ ∉ {0, ±1}`, `(X₃, Ξ*(X₃))`. `𝔓(M) = 0`, `𝔓(S) = −κ`; `det Hess 𝔓(M) = 6κ(φ − 1)Δ = Y − 6κΔ`,
`det Hess 𝔓(S) = 6κ(φ + 1)Δ = Y + 6κΔ`; `M` is a nondegenerate maximum and `S` a nondegenerate critical point of index
`m` iff `|φ| < 1`.

(c) *(Elder window.)* Let `|φ| < 1` and let `d_𝔓(M)` be the maximin connection level of `M` for `𝔓` on `R^{1+m}` (paths
to points with `𝔓 > 0`; `−∞` if there are none). Then

    d_𝔓(M) = −κ = 𝔓(S)  if |φ| < 1/3;        d_𝔓(M) = g(X₃) > −κ  if 1/3 < φ < 1;        d_𝔓(M) = −∞  if −1 < φ < −1/3.

(d) `g(X₃) + κ = κ(φ + 1)³(3φ − 1)/(16φ³)`, `g(X₃) = κ(φ − 1)³(3φ + 1)/(16φ³)`; at `φ = 1/3`,
`g − g(½) = (κ/16)(2X − 1)²(2X + 3)²` (the two saddles `½`, `−3/2` at equal height); at `φ = −1/3`,
`g = −(κ/16)(2X − 3)²(2X + 1)²` (the two maxima `−½`, `3/2` at equal height).

*Proof.* (a) `½(Ξ − Ξ*)ᵀA(Ξ − Ξ*) = ½ΞᵀAΞ + ½(X² − ¼)γ·Ξ + (1/8)(X² − ¼)²γᵀA^{−1}γ`; subtracting from (0.2) leaves
`2κ(X + ½)²(X − 1) + ((f₄ − 3γᵀA^{−1}γ)/24)(X² − ¼)²`, and `(f₄ − 3γᵀA^{−1}γ)/24 = 3κφ`. (b) In the coordinates
`(X, Z)`, `Z := Ξ − Ξ*(X)` (a `C^∞` diffeomorphism with unit Jacobian), `𝔓 = g(X) + ½ZᵀAZ`: critical points are
`{Z = 0, g' = 0}`, and at a critical point the Hessian changes by a congruence of determinant one, so
`det Hess_{(X,Ξ)}𝔓 = g''·Δ` and the inertia is that of `diag(g'', A)`. From (2.1), `g''(−½) = 6κ(φ − 1)`,
`g''(½) = 6κ(φ + 1)`, and `6κφΔ = Y`. (c) For every `t`, `{𝔓 > t} = {(X, Ξ*(X) + Z) : g(X) > t, Zᵀ(−A)Z < 2(g(X) − t)}` —
over each `X` with `g(X) > t` a nonempty open ellipsoid, empty otherwise. Hence a point above `0` exists over `X` iff
`g(X) > 0`; every path satisfies `min 𝔓 ≤ min g(X(·))`, and the lifted path `X ↦ (X, Ξ*(X))` has `𝔓 = g`. So `d_𝔓(M)` is
the one-dimensional maximin `max(d₋, d₊)`, `d₋` (resp. `d₊`) the supremum over `x < −½` (resp. `x > −½`) with `g(x) > 0`
of `min g` on the segment between `−½` and `x` (`sup ∅ = −∞`). On `(−½, ½)`, `g' < 0` (`1 + 2φX ≥ 1 − |φ| > 0`), so `g`
falls from `0` to `−κ`. *`0 ≤ φ < 1/3`:* on `(½, ∞)`, `g' > 0` and `g → +∞`, so `d₊ = −κ`; on `(−∞, −½)`, either `φ = 0`
and `g' > 0` (so `g < 0` there and `d₋ = −∞`), or `X₃ < −3/2` is a local minimum with `g(X₃) < −κ` by (d) and `g → +∞` as
`X → −∞`, so `d₋ = g(X₃) < −κ`. *`1/3 < φ < 1`:* `d₊ = −κ` as before; `X₃ ∈ (−3/2, −½)` is a local minimum, `g → +∞` to
the left, and `g(X₃) > −κ` by (d), so `d₋ = g(X₃)`. *`−1/3 < φ < 0`:* on `(−∞, −½)`, `g' > 0`, so `d₋ = −∞`; on `(½, ∞)`,
`g` rises to the local maximum `X₃ > 3/2` with `g(X₃) > 0` by (d) (`(φ−1)³ < 0`, `3φ + 1 > 0`, `φ³ < 0`), so `d₊ = −κ`.
*`−1 < φ < −1/3`:* `d₋ = −∞`; now `g(X₃) < 0` with `X₃ ∈ (½, 3/2)`, `g < 0` on `(−½, ∞)`, so `d₊ = −∞` and `M` is the unique
global maximum. (d) is algebra (checker C1). ∎

The typed condition `|φ| < 1` is `|Y| < 6κ|Δ|`, the sign window of #198 Lemma W at leading order; the elder condition
is `|Y| < 2κ|Δ|`. Checker C2 recomputes (c) for 117 rational `φ` by an exact one-dimensional union-find maximin on a
grid containing every critical point (hence exact), and C5 the determinants and inertias of (b). A referee pass
confirmed (c) by an independent two-dimensional maximin of the full model (no fiber reduction) in 34 cases.

## 3. Stability of the decision

**Proposition CU.3.** Fix `δ ∈ (0, 1/20)`, put `R_δ := 30δ^{−2}` and `𝒲 := [−3, 2] × {|Ξ| ≤ R_δ}`, and let `K_δ` be the
set of `(κ, f₄, γ, A)` with `κ ∈ [δ, δ^{−1}]`, `A ≤ −δI`, `‖A‖ + |γ| + |f₄| ≤ δ^{−1}` and
`|φ| ∈ [0, 1/3 − δ] ∪ [1/3 + δ, 1 − δ]`. There is `ε = ε(δ, m) > 0` such that: if `f ∈ C²(X)`, `M = −ru/2` and `S = ru/2`
are critical points of `f` with `f(M) = b`, `f(S) = b − κr⁴`, the map `Φ : (X, Ξ) ↦ rXu + r²ΘΞ` is injective on `𝒲`
(so that, being a local diffeomorphism, it maps the interior and boundary of every subregion of `𝒲` onto the interior
and boundary of its image), `(κ, f₄, γ, A) ∈ K_δ` and `‖𝔉 − 𝔓‖_{C²(𝒲)} ≤ ε` (`𝔉 = r^{−4}(f∘Φ − b)`, `𝔓 = 𝔓_{κ,f₄,γ,A}`,
`C²` norms with operator norms on the derivatives), then `M` is a nondegenerate local maximum, `S` a nondegenerate
critical point of index `m`, and

    e(f) = 1{d_f(M) = f(S)} = 1{|φ| < 1/3}.                                                            (3.1)

*Proof.* Constants `C_δ, μ_δ, c_δ, η_δ, …` below depend only on `δ, m` (continuity on the compact `K_δ`).

*Step 1 (the ridge of `𝔉`).* On `𝒲`, `∂_Ξ²𝔉 ≤ A + εI ≤ −(δ/2)I` for `ε ≤ δ/2`. For `X ∈ [−3, 2]`,
`|Ξ*(X)| ≤ (35/8)δ^{−2}`. Since `𝔉(X, ·) ≤ g(X) − (δ/2)|· − Ξ*(X)|² + ε` and `𝔉(X, Ξ*(X)) ≥ g(X) − ε`, every maximizer of
`𝔉(X, ·)` over `|Ξ| ≤ R_δ` lies within `2(ε/δ)^{1/2} < 1` of `Ξ*(X)`, hence in the interior; by strict concavity it is
unique, `Ξ_𝔉(X)`, and the first-order identity `A(Ξ_𝔉 − Ξ*) = ∂_Ξ𝔓(X, Ξ_𝔉) = ∂_Ξ(𝔓 − 𝔉)(X, Ξ_𝔉)` improves this to
`|Ξ_𝔉 − Ξ*| ≤ ε/δ`. By the implicit function theorem `Ξ_𝔉 ∈ C¹`, and `g_𝔉(X) := 𝔉(X, Ξ_𝔉(X))` is `C²` with
`g_𝔉' = ∂_X𝔉(·, Ξ_𝔉)`, `g_𝔉'' = [∂_X²𝔉 − ∂_{XΞ}𝔉(∂_Ξ²𝔉)^{−1}∂_{ΞX}𝔉](·, Ξ_𝔉)`; the same formulas hold for `g` with `(𝔓, Ξ*)`.
Hence `‖g_𝔉 − g‖_{C²([−3,2])} ≤ C_δε`.

*Step 2 (connectivity reduces to one dimension).* For every `t`, each nonempty `X`-fiber of `𝒲 ∩ {𝔉 > t}` is convex
(a ball cut by a superlevel set of a concave function) and contains `Ξ_𝔉(X)`, and it is nonempty iff `g_𝔉(X) > t`. So the
path components of `𝒲 ∩ {𝔉 > t}` are the parts over the components of `{X ∈ [−3, 2] : g_𝔉(X) > t}`, and the supremum of
`𝔉` over such a part is the supremum of `g_𝔉` over the interval.

*Step 3 (transverse boundary).* On `|Ξ| = R_δ`, `|Ξ − Ξ*| ≥ 25δ^{−2}`, so `𝔉 ≤ max_{[−3,2]}g − 312δ^{−3} + ε`; since
`|g| ≤ 280κ ≤ 280δ^{−1}` on `[−3, 2]` and `δ^{−2} > 400`, `𝔉 < −2κ − 1` there.

*Step 4 (types).* `M ↔ (−½, 0)` and `S ↔ (½, 0)` are critical points of `𝔉`, so `Ξ_𝔉(±½) = 0`, `g_𝔉'(±½) = 0`,
`g_𝔉(−½) = 0` and `g_𝔉(½) = −κ` exactly. `g''(−½) = 6κ(φ − 1) ≤ −6δ²` and `g''(½) ≥ 6δ²`, so for `C_δε < 3δ²` the
Schur complement `g_𝔉''` of `∂_Ξ²𝔉 < 0` in `Hess 𝔉` is negative at `M` and positive at `S` (Haynsworth): `M` is a
nondegenerate maximum and `S` has index `m`, for `𝔉` and hence for `f`.

*Step 5 (the decision).* Let `τ := δ/10` and let `Z_g` be the set of **all** real zeros of `g'`: `±½` and, for `φ ≠ 0`,
`X₃` — wherever it lies, inside or outside `[−3, 2]`. All are nondegenerate (`g''(X₃) = 3κ(1 − φ²)/φ`), `|X₃ ∓ ½| ≥ δ/2`,
`|g''| ≥ c_δ > 0` on the `τ`-neighbourhoods of the points of `Z_g` (referee computation: `c_δ ≈ 3.6κδ`), and `|g'| ≥ μ_δ > 0`
on the points of `[−3, 2]` at distance `≥ τ` from `Z_g` (compactness of `K_δ`). For `C_δε < ½min(μ_δ, c_δτ)`, `g_𝔉'` has
exactly the zeros `±½` and, when `X₃ ∈ [−3 + τ, 2 − τ]`, one more zero `X₃^𝔉` within `τ` of `X₃` (nondegenerate), with the
same sign pattern as `g'` elsewhere on `[−3, 2]` away from the `τ`-neighbourhoods of `Z_g`.

*Case E, `|φ| ≤ 1/3 − δ`.* By §2, `g` increases on `[−3/2, −½]` (for `φ > 0` because `X₃ < −3/2 − 4δ`), decreases on
`[−½, ½]` and increases on `[½, X_R]`, where `X_R := 2` if `φ ≥ 0` and `X_R := min(2, X₃ − τ)` if `φ < 0`; and
`g(−3/2) = κ(−5 + 12φ) ≤ −κ(1 + 12δ)`, `g(X_R) ≥ η_δ > 0` (`g(2) = κ(12.5 + 42.1875φ) ≥ 1.9κ` for `φ ≥ −¼`, and for
`φ < −¼`, `X₃ ≤ 2` and `g(X₃ − τ) ≥ g(X₃) − Cκτ² ≥ 11κδ` since `g(X₃) ≥ 12κδ` by (d); numerically `g(X_R) ≥ 0.8κ` at
`δ = 1/21`). The same holds for `g_𝔉`, with `−κ(1 + 11δ)` and `η_δ/2`. *Path:* the ridge curve `X ↦ Φ(X, Ξ_𝔉(X))`,
`X ∈ [−½, X_R]`, runs from `M` through `S` to a point where `f > b`, and along it `f − b = r⁴g_𝔉 ≥ −κr⁴ = f(S) − b`. So
`d_f(M) ≥ f(S)`. *Trap:* let `D := (−3/2, ½) × {|Ξ| < R_δ}` and `D_phys := Φ(D)`, `∂D_phys = Φ(∂D)`. On `∂D`:
`𝔉 ≤ g_𝔉(−3/2) < −κ` at `X = −3/2`; `𝔉 < −2κ − 1` at `|Ξ| = R_δ`; at `X = ½`, `𝔉(½, Ξ) ≤ g_𝔉(½) = −κ` with equality only at
`Ξ = 0`, i.e. at `S`. So `f ≤ f(S)` on `∂D_phys`. The path component `C` of `{f > f(S)}` containing `M` does not meet
`∂D_phys` (the first exit of a path in `C` from `D_phys` would land on it), hence `C ⊂ D_phys`, and by Step 2 its supremum is
`b + r⁴ sup g_𝔉` over the component of `{g_𝔉 > −κ} ∩ (−3/2, ½)` containing `−½`, which is `b + r⁴g_𝔉(−½) = b`. So `C`
contains no point above `b`, and every path from `M` to a point above `b` leaves `C` and meets `{f ≤ f(S)}`:
`d_f(M) ≤ f(S)`. Hence `d_f(M) = f(S)` and `e = 1`.

*Case R⁺, `φ ∈ [1/3 + δ, 1 − δ]`.* `X₃ ∈ (−3/2, −½ − δ/2)` is a nondegenerate local minimum of `g`; `g` decreases on
`[−3, X₃]` and increases on `[X₃, −½]`; `g(X₃) ≥ −κ + 0.44δκ` by (d); `g(−3) = κ(−50 + 229.6875φ) ≥ 26κ`. For `g_𝔉` the
same holds with `g_𝔉(X₃^𝔉) ≥ −κ + 0.4δκ`. The ridge curve from `M` to `X = −3` ends where `f > b` and has minimum
`b + r⁴g_𝔉(X₃^𝔉) > f(S)`: `d_f(M) > f(S)`, `e = 0`.

*Case R⁻, `φ ∈ [−1 + δ, −1/3 − δ]`.* `X₃ ∈ (½ + δ/2, 3/2)`; `g` increases on `[−3/2, −½]`, decreases on `[−½, ½]`,
increases on `[½, X₃]`, decreases on `[X₃, 2]`; `g(−3/2) ≤ −9κ`, `g(2) ≤ −1.5κ`, `g(X₃) ≤ −1.5δκ < 0`. Put
`t_* := −(5/4)κ` and `D' := (−3/2, 2) × {|Ξ| < R_δ}`: `𝔉 < t_*` on `∂D'` (at the ends by the values of `g_𝔉`, on the
transverse boundary by Step 3), the component `C'` of `{f > b + r⁴t_*}` containing `M` lies in `Φ(D')`, and its supremum is
at most `b + r⁴max(g_𝔉(−½), g_𝔉(X₃^𝔉)) = b`. So `d_f(M) ≤ b + r⁴t_* < f(S)` (or `M` is the global maximum, `d_f(M) = −∞`),
and `e = 0`. ∎

Only window information is used: every conclusion is either an explicit path inside `Φ(𝒲)` or a trap whose boundary
lies inside it, so the exterior landscape cannot change the decision. No Morse–Smale, separatrix or genericity
assumption is made; `e` is computed exactly.

## 4. The kernels at the cusp scale

**Theorem CU.4.** For fixed `b ∈ R`, `u ∈ S^{d−1}` and `κ > 0`, as `r ↓ 0`,

    r^{−2}A_r(b, κr, u) → 𝒜^{cand},   r^{−2}A_r^{eld}(b, κr, u) → 𝒜^{eld},   r^{−2}A₀(b, κr, u) → 𝒜^{con},       (4.1)

`𝒜^• := 12π₀(u; v₀(b, 0))E₀[w^• | b]` with `w^{cand} := (36κ²Δ² − Y²)1{A < 0, |Y| < 6κ|Δ|}`,
`w^{eld} := (36κ²Δ² − Y²)1{A < 0, |Y| < 2κ|Δ|}` and `w^{con} := 36κ²Δ²1{A < 0}`.

*Proof.* Work under the coupling (R3) with `k = κr`; `T` dominates `1 + k + ‖F_r‖_{C⁷} + ‖F₀‖_{C⁷} + r^{−2}‖F_r − F₀‖_{C²}`
with `‖T‖_p ≤ C_pP` ([R] (R4); #191 §1). The contact law of `F₀` has target `v₀(b, κr)`, which differs from `v₀(b, 0)`
only in the coordinate `12k`; the regression mean is affine in the target and the covariance does not depend on it, so
`F₀ = F₀⁰ + 12k·w₀` with `F₀⁰` of target `v₀(b, 0)` and `w₀` a fixed smooth function: the `E₀`-variables are the jets of
`F₀⁰`, and those of `F₀` differ from them by deterministic `O(κr)` vectors.

(i) *Weights.* By #198 (3.1), `det K_M = r(Y_r − 6κΔ₀) + R_M`, `det K_S = r(Y_r + 6κΔ₀) + R_S`, `|R_i| ≤ Cr²(1 + k)T^{N₁}`,
with `Y_r = (f₄/12)Δ₀ + 3k tr(adj(A₀)B) − q` (#191's `Y`). As `r → 0`, `Y_r → Y` and `Δ₀ → Δ` (the `E₀`-variables) in every
`L^p`, so `det K_i/r → Y ∓ 6κΔ` in every `L^p`.

(ii) *Types.* `{W_r > 0} = {index K_M = d, index K_S = d − 1}`. On `{A < 0, |Y| ≠ 6κ|Δ|}`, for small `r`, `A_M, A_S < 0`
and, by Haynsworth, the indices are `m + 1{σ_i < 0}` with `σ_i = det K_i/det A_i`; with `sign Δ = (−1)^m` this gives
`typed ⟺ |Y| < 6κ|Δ|` in the limit. On `{A < 0}^c`, a typed configuration needs `A_M < 0`, hence `λ_max(A₀) ≤ CrT`, of
probability `→ 0` (the deterministic `O(κr)` shift between `A₀` and `A` included). So
`1{W_r > 0} → 1{A < 0, |Y| < 6κ|Δ|}` in probability.

(iii) *Marks.* By Theorem CU.1, `‖𝔉_r − 𝔓_r‖_{C²(𝒲)} ≤ C_δrT` for the rescaled `F_r` and `𝔓_r` built from the jets of
`F_r`. On `{(κ, jets of F_r) ∈ K_δ, C_δrT ≤ ε(δ)}`, Proposition CU.3 gives `e = 1{|φ_r| < 1/3}`, `φ_r` built from the jets of
`F_r`, and `φ_r → φ = Y/(6κΔ)` in probability. The typed event minus this good event has probability at most
`P(C_δrT > ε(δ)) + P(|jets(F_r) − E₀-jets| > η_δ) + P((κ, E₀-jets) ∉ K_{2δ}, A < 0, |Y| < 6κ|Δ|) + o(1)`, with `η_δ` so small
that `η_δ`-perturbations of points of `K_{2δ}` stay in `K_δ`; the first two terms `→ 0` as `r → 0`, and the third `→ 0` as
`δ → 0`, because the `E₀`-jets are a nondegenerate Gaussian vector ([P] §2 finite-jet rank) and, given `(A, γ)`, `f₄` has a
nondegenerate Gaussian law — so `φ` has a continuous distribution and `P(|φ| ∈ (1/3 − 2δ, 1/3 + 2δ) ∪ (1 − 2δ, 1))`,
`P(λ_max(A) ∈ (−2δ, 0))`, `P(large jets)` all vanish as `δ → 0`.

(iv) *Expectations.* On the typed event `W_r/r² = −det K_M det K_S`, and by #198 (3.2)
`W_r/r² ≤ C(κ²r²Δ₀² + r⁴(1 + k)²T^{2N₁})`, so `(W_r/r²)/r²` is bounded in `L²` and uniformly integrable. With (i)–(ii) for the
candidate limit and (i)–(iii) for the elder limit,
`E_Q[W_r/r²]/r² → E₀[w^{cand} | b]` and `E_Q[(W_r/r²)e]/r² → E₀[w^{eld} | b]` (note `|φ| < 1/3 ⟺ |Y| < 2κ|Δ|`).

(v) *Densities.* `π_r(v_r) → π₀(v₀(b, 0))` by [R] (R5) and the continuity of `π₀` in the target;
`A₀(b, κr, u)/r² = 12π₀(v₀(b, κr))·36κ²E[Δ²1{A < 0} | v₀(b, κr)] → 𝒜^{con}`. ∎

## 5. The typed window has small probability

**Lemma CU.5.** There are `C, N` and, for `m = d − 1`, the exponents `θ = 1/2`, `β = min(1/8, 1/(4m))` such that for
`0 < r ≤ r₁`, `b ∈ R`, `0 ≤ k ≤ 1`,

    E_Q[W_r/r²] ≤ C (k² + r⁴)(min(1, k/r)^{θ} + r^{β}) P^N.                                              (5.1)

(#198 Lemma W is (5.1) without the factor in parentheses.)

*Proof.* Let `J` be the vector of all partial derivatives of `f = F_r` at `0` of orders `≤ 8` in the frame `(u, Θ)`,
`J = (J_pin, f₄, J')`, where `J_pin := (f, ∂_uf, ∂_u²f, ∂_u³f, ∇_Θf, ∇_Θ∂_uf)(0)` and `J'` is the rest. (`J'` must exclude the
pinned jets: with `∂_u²f(0)` in `J'`, the pin row `U₃` would determine `(r²/24)f₄` up to `O(r⁷)`.)

*Conditional density of `f₄`.* Under `Q`, `(f₄, J')` is Gaussian with the law of `(f₄, J')` given `U_r = v_r`, so
`Var_Q(f₄ | J') = Var(f₄ | J', U_r)`. As `r → 0`, `U_r → U₀ = J_pin` in `L²` of the field, and `(J', J_pin)` and
`(f₄, J', J_pin)` are families of distinct partial derivatives at one point, hence nondegenerate ([P] §2). The Gram
matrix of `(J', U_r)` therefore stays uniformly invertible for `r ≤ r₁` (uniformly over frames), and
`Var(f₄ | J', U_r) → Var(f₄ | J', J_pin) > 0`. So the conditional density of `f₄` given `J'` under `Q` is bounded by a
constant `C₀`.

*Affine structure.* Expanding `α_i = ∂_u²f(x_iu)/r`, `A_i = D_Θ²f(x_iu)`, `β_i = ∇_Θ∂_uf(x_iu)/r` (`x_i = ∓r/2`) to order 8
in `x_i` and inserting the pin identities to the same order (`∂_u²f(0) = −(r²/24)f₄ + (terms in J') + …`,
`∂_u³f(0) = 12k − (r²/40)∂_u⁵f(0) + …`, `∇_Θ∂_uf(0) = (terms in J')`; the transverse pins involve no `f₄`),
`det K_i = α_i det A_i − rβ_iᵀadj(A_i)β_i = d_i(J')f₄ + c_i(J') + ρ_i`, with `d_i(J') = (r/12)det A_i(J')` and a Taylor
remainder `|ρ_i| ≤ Cr⁶(1 + ‖f‖_{C⁹})^{N₂}`. (A referee pass verified exactly, on a general pinned polynomial of degree 8
in `d = 2`, that `A_i, β_i` contain no `f₄` and `det K_i` is of degree 1 in `f₄` with slope `(r/12)det A_i`.) Let
`E₁ := {‖F_r‖_{C⁹} + T ≤ r^{−η}}` with `η := 1/(8max(N₁, N₂))` (`N₁, N₂ ≥ m + 1`, enlarged if necessary, so `mη < 1/8`); on `E₁`, `|ρ_i| ≤ Cr⁵`, and `P(E₁^c) ≤ C_q r^qP^{N_q}` for every
`q` ([R] (R4)).

*The window.* Let `Δ := det D_Θ²f(0)` (a coordinate of `J'`) and `B₁ := {|Δ| ≥ r^{1/2}}`. On `B₁ ∩ E₁` and for small `r`,
`|det A_i(J') − Δ| ≤ Cr^{1−mη} ≤ |Δ|/2`, so `det A_M(J')`, `det A_S(J')` have the sign of `Δ` and `|d_i| ≥ (r/24)|Δ| ≥ r^{3/2}/24`.
Write `Λ_i(x) := d_ix + c_i` (`J'`-measurable coefficients), so that `det K_i = Λ_i(f₄) + ρ_i`, and `z_i := −c_i/d_i`. On the
typed event the two determinants have opposite signs (#198 §3) while `d_M`, `d_S` have the same sign, so `f₄` lies within
`max_i|ρ_i|/|d_i| ≤ Cr⁵/min|d_i|` of the segment between `z_M` and `z_S`; hence `{W_r > 0} ∩ B₁ ∩ E₁ ⊂ {f₄ ∈ I(J')}`, `I(J')`
the `J'`-measurable interval spanned by `z_M`, `z_S`, enlarged by `Cr⁵/min|d_i|`. Its length on this event: since
`Λ_i(f₄) = d_i(f₄ − z_i)`, `z_S − z_M = Λ_M(f₄)/d_M − Λ_S(f₄)/d_S`, and on the typed event the sign window (#198 Lemma W's
argument with (3.1)) gives `|det K_i| ≤ 12k|Δ₀| + 2max_j|R_j|`, so `|Λ_i(f₄)| ≤ 12k|Δ| + Cr^{2−N₁η}` on `E₁` (the swap
`Δ₀ → Δ` costs `12k|Δ₀ − Δ| ≤ Cr²T^m ≤ Cr^{2−mη}`, absorbed as `N₁ ≥ m + 1`, and `|ρ_i| ≤ Cr⁵`). With `|d_i| ≥ (r/24)|Δ|` and
`|Δ| ≥ r^{1/2}`,

    |I(J')| ≤ 48(12k|Δ| + Cr^{2−N₁η})/(r|Δ|) + Cr^{7/2} ≤ C(k/r + r^{1/2−N₁η}) ≤ λ := C(k/r + r^{1/4}).

(v1 bounded `z_S − z_M` through an asymmetric identity containing `(d_S − d_M)(f₄ + c_M/d_M)` and did not bound that term —
Codex P1 4150765060 on Math- #207; the symmetric form needs no bound on `d_S − d_M`.) Put `I(J') := R` on the
`J'`-measurable set `{d_Md_S ≤ 0}`. The event `{|I(J')| ≤ λ}` is `J'`-measurable and `{W_r > 0} ∩ B₁ ∩ E₁` is contained in
`{f₄ ∈ I(J')} ∩ {|I(J')| ≤ λ}`; `E₁` and the sign window involve the coupling variables `T`, `Δ₀`, so this inclusion holds on
the coupling space, and the dominating event depends on `F_r` alone, so
`P_Q({W_r > 0} ∩ B₁ ∩ E₁) ≤ E[1{|I(J')| ≤ λ}P_Q(f₄ ∈ I(J') | J')] ≤ C₀λ`.

*Small determinant.* Under `Q`, `D_Θ²f(0)` is a nondegenerate Gaussian symmetric matrix and `Δ` a polynomial of degree `m`
in it. `E_Q[Δ²] ≥ c > 0` uniformly in `(r, b, k, frame)`: the top (`m`-th) Wiener-chaos component of `det(μ + G)` is the
Wick product of `det G`, which does not depend on the mean `μ`. So by the Carbery–Wright inequality
`P_Q(|Δ| < r^{1/2}) ≤ Cr^{1/(2m)}`.

*Weights.* On the typed event, `W_r/r² ≤ C(k²Δ₀² + r⁴(1 + k)²T^{2N₁})` (#198 (3.2)), whose `L²` norm is `≤ C(k² + r⁴)P^N`.
By Cauchy–Schwarz, `E_Q[(W_r/r²)1_{B₁∩E₁}] ≤ C(k² + r⁴)P^N·min(1, C₀λ)^{1/2} ≤ C(k² + r⁴)P^N(min(1, k/r)^{1/2} + r^{1/8})`,
`E_Q[(W_r/r²)1_{B₁^c}] ≤ C(k² + r⁴)P^N r^{1/(4m)}` and `E_Q[(W_r/r²)1_{E₁^c}] ≤ C(k² + r⁴)P^N r^q`. Summing gives (5.1). ∎

## 6. Proof of Theorem CU

Fix `S ≥ 1` and `ε₀ ∈ (0, β/(12(3 + β)))` with `β` of Lemma CU.5, put `ρ₁ := ℓ^{1/12 − ε₀}` and take `ℓ` so small that
`Sℓ^{1/4} < ρ₁ ≤ min(r₁, r_0^*)` and `Sℓ^{1/4} ≤ r_0^{[K]}`. Split

    ν_eld(ℓ) − cℓ^{−1/3} = I₁ + I₂ + I₃ + I₄ + I₅,

`I₁ := ∫_{r<Sℓ^{1/4}}∫∫ r^{−2}(A_r^{eld} − A₀)`, `I₂ :=` the same over `Sℓ^{1/4} ≤ r < ρ₁`, `I₃ := ∫_{ρ₁≤r<r_0^*}∫∫ r^{−2}A_r^{eld}`,
`I₄ := −∫_{r≥ρ₁}∫∫ r^{−2}A₀`, `I₅ := ν_eld^{far,r_0^*}(ℓ)`, all integrands evaluated at `(b, ℓ/r³, u)`.

*`I₁`.* With `r = sℓ^{1/4}`, `I₁ = ℓ^{1/4}∫∫∫_0^S [r^{−2}(A_r^{eld} − A₀)](b, ℓ/r³, u) ds db dσ`, and at fixed `s` the
integrand is evaluated at `κ = s^{−4}`, so by Theorem CU.4 it converges to `(𝒜^{eld} − 𝒜^{con})(b, s^{−4}, u)`.
Domination: for `s ≤ 1` (`κ ≥ 1`, i.e. `r ≤ k`), `|r^{−2}(A_r − A₀)| ≤ H(b, k) ≤ Ce^{−cb²}` by #191 (E.1), and
`r^{−2}(A_r − A_r^{eld}) = 12π_rE_Q[(W_r/r²)(1 − e)]/r² ≤ Ce^{−c(b²+k²)}P^N(r³/k)/r² = Ce^{−c(b²+k²)}P^N s⁴ ≤ Ce^{−c'b²}` by
[C7-K] (K2) (valid as `r ≤ min(k, r_0^{[K]})`) and `1 − e ≤ 1_{G_r^c}` ([C7-K] §4); for `1 ≤ s ≤ S`,
`r^{−2}A_r ≤ C(κ² + r²)P^Ne^{−c(b²+k²)} ≤ Ce^{−c'b²}` by #198 Lemma W and (R5), and `r^{−2}A₀ ≤ Cκ²e^{−cb²}`. Dominated
convergence: `I₁ = ℓ^{1/4}[∫∫∫_0^S(𝒜^{eld} − 𝒜^{con})(b, s^{−4}, u) ds db dσ + o(1)]`.

*`I₂`.* By Lemma CU.5 with (R5) and `A₀ ≤ k²H`, `r^{−2}(A_r^{eld} + A₀) ≤ C[(κ² + r²)(min(1, κ)^{1/2} + r^β) + κ²]e^{−c'b²}`
for `κ ≤ 1`. With `κ = ℓr^{−4}`: `∫_{Sℓ^{1/4}}^∞ κ²dr = ℓ^{1/4}S^{−7}/7` and `∫_{Sℓ^{1/4}}^∞ κ^{5/2}dr = ℓ^{1/4}S^{−9}/9`;
`∫_{Sℓ^{1/4}}^∞ κ²r^β dr ≤ Cℓ^{1/4+β/4}S^{−7+β}`; `∫_0^{ρ₁} r²κ^{1/2}dr = ℓ^{1/2}ρ₁` and `∫_0^{ρ₁} r^{2+β}dr ≤ ρ₁^{3+β}`, both `o(ℓ^{1/4})`
because `(1/12 − ε₀)(3 + β) > 1/4` by the choice of `ε₀`. So `|I₂| ≤ Cℓ^{1/4}S^{−7} + o(ℓ^{1/4})`.

*`I₃, I₄, I₅`.* #198 Lemma B (B.2) gives `0 ≤ I₃ ≤ Cℓ^{1/3}(ρ₁^{−1} + ℓρ₁^{−5}) = O(ℓ^{1/4+ε₀})`; `|I₄| ≤ Cℓ²ρ₁^{−7} = o(ℓ^{1/4})`;
#198 Lemma F′ gives `0 ≤ I₅ ≤ Cℓ^{1/3}`.

*Conclusion.* `ℓ^{−1/4}(ν_eld(ℓ) − cℓ^{−1/3})` has `limsup` and `liminf` within `CS^{−7}` of
`∫∫∫_0^S(𝒜^{eld} − 𝒜^{con}) ds db dσ`. The integrand equals `−12π₀E₀[loss(s) | b]` with
`loss(s) := Y²1{|Y| < 2s^{−4}|Δ|} + 36s^{−8}Δ²1{|Y| ≥ 2s^{−4}|Δ|}` on `{A < 0}` (and `0` off it); `loss ≥ 0` and, with
`s₁ := (2|Δ|/|Y|)^{1/4}`,

    ∫_0^∞ loss(s) ds = Y²s₁ + (36/7)Δ²s₁^{−7} = (16/7)Y²s₁ = (16/7)·2^{1/4}|Y|^{7/4}|Δ|^{1/4}                     (6.1)

(since `36Δ²s₁^{−8} = 9Y²`; checker C6). By Tonelli the `s`-integral over `(0, ∞)` converges absolutely; letting
`S → ∞` gives (CU.1) with `c₁ = −12∫∫π₀E₀[(16/7)2^{1/4}|Y|^{7/4}|Δ|^{1/4}1{A < 0} | b] db dσ`, which is (CU.2). The
expectation is finite (Gaussian moments; `π₀` has Gaussian decay in `b`) and strictly positive because `Y ≠ 0`,
`A < 0` has positive probability under the nondegenerate contact law; so `c₁ < 0`. ∎

## 7. The candidate and rejected densities

For the candidate density no elder decision is needed, and the part of the remainder that is not cusp-scale — the
equal-height mass `B_{d,L}` of [Z] — is reached at a Lipschitz rate in the gap, because the gap enters the pinned law
affinely. Notation: `Ψ_ℓ^{cand}(b, y) = p_y(v_{b,ℓ})E_{Q_{y,b,ℓ}}[W]` and `Ψ_0` as in [Z] (Z2) (unmarked; #191 §0), so that
`r^{−2}A_r(b, ℓ/r³, u) = r^{d−1}Ψ_ℓ^{cand}(b, ru)` and `B_{d,L} = ∫_{X∖{0}}∫_R Ψ_0 db dy = ∫_0^{r₀}∫∫ r^{−2}A_r(b, 0, u) dσ db dr
+ ∫_{dist(0,y)≥r₀}∫Ψ_0 db dy` for every `r₀ ∈ (0, r_0^*]` (#191 (2.1)–(2.2), [Z] (Z3)).

**Lemma L (the gap enters Lipschitz).** There are `C, c, N` such that for `0 < r ≤ r_0^*`, `b ∈ R`, `u ∈ S^{d−1}` and
`0 ≤ k ≤ 1`,

    |A_r(b, k, u) − A_r(b, 0, u)| ≤ C (k² + kr²)(1 + |b|)^N e^{−cb²},                                     (7.1)

and for every `r₀ ∈ (0, r_0^*]` there is `C_{r₀}` such that for `dist(0, y) ≥ r₀` and `0 ≤ ℓ ≤ 1`,

    |Ψ_ℓ^{cand}(b, y) − Ψ_0(b, y)| ≤ C_{r₀} ℓ (1 + |b|)^N e^{−cb²}.                                         (7.2)

*Proof of (7.1).* *Affine structure.* [R] (R3) realizes `Q_{r,b,k}` as `F_r = F + C_rΣ_r^{−1}(v_r − U_r)` with one
unconditioned copy `F` for all `(b, k)`, and the target `v_r = (b − kr³/2, −kr², 0, 12k, 0, …, 0)` ([R] §2) is affine in `k`.
Hence `F_r^{(k)} = F_r^{(0)} + kω_r` with `ω_r := C_rΣ_r^{−1}δv_r`, `δv_r := (−r³/2, −r², 0, 12, 0, …, 0)`: deterministic,
pinned with `b = 0`, `k = 1` (`U_r(ω_r) = δv_r`), and `‖ω_r‖_{C⁷} ≤ ‖C_r‖_{C⁷}‖Σ_r^{−1}‖|δv_r| ≤ C` uniformly in `r ≤ r_0^*` and
frames by (R2). Put `T₀ := 1 + ‖F_r^{(0)}‖_{C⁷} + ‖ω_r‖_{C⁷}`; by (R3), `‖F_r^{(0)}‖_{C⁷} ≤ ‖F‖_{C⁷} + C(|b| + |U_r|)`, so
`‖T₀‖_p ≤ C_p(1 + |b|)`, and `‖F_r^{(k')}‖_{C⁷} ≤ T₀` for `0 ≤ k' ≤ 1`. (In the polynomial model of checker C8 the shift is
`ω_r = 2(x − r)(x + r/2)²`, with no transverse part, so `det K_i` is affine in `k'` with slope `∓6 det A_i`; for the actual
regression function `ω_r` has transverse parts, and only the bounds below are used.)

*The typed product along the gap.* The scaled endpoint Hessians are linear in the field, so
`K_i(k') = K_i(0) + k'K_i[ω_r]`, with `‖K_i[ω_r]‖ ≤ C` (by #191 (1.1) for the pinned `ω_r`, `α_i[ω_r] = ∓6 + O(r)`) and
`‖K_i(k')‖ ≤ CT₀` (#191 (1.1), (1.3), (1.5)). Hence `det K_i(k')` is a polynomial in `k'` with
`|∂_{k'}det K_i| = |tr(adj K_i(k')·K_i[ω_r])| ≤ CT₀^{d−1}`. The typed product `w(k') := F_d(K_M(k'))F_{d−1}(K_S(k'))` is
continuous on `[0, k]`: an index changes only where an eigenvalue crosses zero, where the corresponding determinant,
hence `w`, vanishes. Between the finitely many zeros of the polynomial `p := det K_M det K_S` (if `p ≡ 0`, then `w ≡ 0`),
`w = ±p` or `w = 0`, so for every realization

    |w(k) − w(0)| ≤ ∫_0^k |∂_{k'}(det K_M det K_S)| 1{typed(k')} dk'.

On `typed(k')` the two determinants have opposite signs, and the deterministic expansions of #191 §1 Steps 1–3 with
the `(1 + k)`-quantified remainder of #198 (3.1) — applied to the pinned `C⁷` function `F_r^{(k')}`, with `D_y²F_r^{(k')}(0)`
in place of `A₀` — give `det K_{M,S}(k') = ∓6k'Δ' + rY' + R_{M,S}` with `|R_i| ≤ Cr²T₀^{N₁}`; so, as in #198 Lemma W,
`|det K_i(k')| ≤ 12k'T₀^m + 2Cr²T₀^{N₁}`. Hence `|∂_{k'}(det K_M det K_S)| ≤ C(k' + r²)T₀^N` on `typed(k')`, so
`|w(k) − w(0)| ≤ C(k² + kr²)T₀^N`, and taking expectations,
`|Z_r/r²(b, k, u) − Z_r/r²(b, 0, u)| ≤ C(k² + kr²)(1 + |b|)^N`.

*The density factor.* `π_r(v_r(b, ·))` is a Gaussian density whose covariance is uniformly invertible for `r ≤ r_0^*`
([R] (R2), (R5)), evaluated at a target affine in `k`: `|π_r(v_r(b, k)) − π_r(v_r(b, 0))| ≤ Ck(1 + |b|)e^{−cb²}`. With
`Z_r/r² ≤ C(k² + r⁴)(1 + |b|)^N` (#198 Lemma W) and `A_r = 12π_r(v_r)Z_r/r²`, (7.1) follows (`k³ ≤ k²`, `kr⁴ ≤ kr²`).

*Proof of (7.2).* The same, with the two-site regression in place of the near one ([Z] (Z10): `f_ℓ = f_0 + ℓh_y`,
`f_0 ~ Q_{y,b,0}`, `h_y` deterministic). [Z] states (Z10) at fixed separation only; the uniform facts on the compact
`D_{r₀} = {dist(0, y) ≥ r₀}` are #198 §2 (a), (b), (2.2): `λ_min(Cov O_y) ≥ c₀ > 0`, the regression functions `ψ^y_j` are
bounded in `C³` uniformly (so `h_y = −ψ^y_{f(y)}` has `sup_y ‖h_y‖_{C²} ≤ C_{r₀}`), and the Hessian moments under `Q_{y,b,ℓ}`
are `≤ C_p(1 + |b|)^p` uniformly in `y ∈ D_{r₀}` and `ℓ ∈ [0, 1]` ((2.2) at `ℓ = 0` by the same proof); and
`|∂_ℓ p_y(v_{b,ℓ})| = p_y(v_{b,ℓ})|(Γ_y^{−1}v_{b,ℓ})_{f(y)}| ≤ C_{r₀}(1 + |b|)e^{−cb²}`. The typed product
`W(f_ℓ) = |det H_0 det H_y|1{H_0 < 0, index H_y = d − 1}` is continuous and piecewise polynomial in `ℓ` for the same reason,
with `|∂_ℓ(det H_0 det H_y)| ≤ C(‖f_0‖_{C²} + ‖h_y‖_{C²})^{2d−1}‖h_y‖_{C²}`. ∎

**Theorem CU′ (the candidate and rejected densities).** Under the hypotheses of Theorem CU, as `ℓ ↓ 0`,

    ν_cand(ℓ) = c ℓ^{−1/3} + B_{d,L} + I^{cand} ℓ^{1/4} + o(ℓ^{1/4}),
    I^{cand} = −(96/7)·6^{1/4} ∫_{S^{d−1}}∫_R π₀(u; v₀(b,0)) E₀[|Y|^{7/4}|Δ|^{1/4}1{A < 0} | b] db dσ(u) = (3^{1/4}/2) c₁ < 0,   (CU′.1)

    ρ_rej(ℓ) = ν_cand(ℓ) − ν_eld(ℓ) = B_{d,L} + (I^{cand} − c₁) ℓ^{1/4} + o(ℓ^{1/4}),   I^{cand} − c₁ = (1 − 3^{1/4}/2)|c₁| > 0.   (CU′.2)

Moreover, for every `r₀ ∈ (0, r_0^*]`, `ν_cand^{far,r₀}(ℓ) = ∫_{dist(0,y)≥r₀}∫Ψ_0 db dy + O(ℓ)`: the `ℓ^{1/4}` terms are
near-diagonal, carried by the cusp scale. (CU′.1) uses only Lemma L, the candidate part of Theorem CU.4 (with CU.1),
#191 ((E.1), §§1–2), #198 ((3.1), Lemma W, §2), [R], [Z] and [P] §14 — not Proposition CU.3, Lemma CU.5, [C7-K] or #198
Lemmas B, F′ — so it can be accepted separately; (CU′.2) = (CU′.1) − (CU.1) inherits everything Theorem CU uses.

*Proof.* Fix `S ≥ 1` and `r₀ ∈ (0, r_0^*]`, and let `ℓ` be so small that `Sℓ^{1/4} < r₀`. By the separation-variable identity
(#191 (2.1)) and the decomposition of `B_{d,L}` above,

    ν_cand(ℓ) − cℓ^{−1/3} − B_{d,L} = J₁ − J₂ + J₃ − J₄ + J₅,

`J₁ := ∫_{r<Sℓ^{1/4}}∫∫ r^{−2}(A_r − A₀)(b, ℓ/r³, u)`, `J₂ := ∫_{r<Sℓ^{1/4}}∫∫ r^{−2}A_r(b, 0, u)`,
`J₃ := ∫_{Sℓ^{1/4}≤r<r₀}∫∫ r^{−2}[A_r(b, ℓ/r³, u) − A_r(b, 0, u)]`, `J₄ := ∫_{r≥Sℓ^{1/4}}∫∫ r^{−2}A₀(b, ℓ/r³, u)` and
`J₅ := ∫_{dist(0,y)≥r₀}∫(Ψ_ℓ^{cand} − Ψ_0) db dy` (inner integrals `db dσ(u)`), using the far Kac–Rice identity
`ν_cand^{far,r₀}(ℓ) = ∫_{dist(0,y)≥r₀}∫Ψ_ℓ^{cand} db dy` (#191 §2, "the far candidate density"; #198 (2.1) without the mark).
*`J₁`* is `I₁` of §6 with `A_r` in place of `A_r^{eld}`: (E.1) gives the majorant `|r^{−2}(A_r − A₀)| ≤ H(b, k) ≤ Ce^{−cb²}` on
the whole range, and the pointwise limit is Theorem CU.4 for `𝒜^{cand}` (steps (i), (ii), (iv), (v); no Proposition CU.3), so
`J₁ = ℓ^{1/4}[∫∫∫_0^S(𝒜^{cand} − 𝒜^{con})(b, s^{−4}, u) ds db dσ + o(1)]`.
*`J₂`*: by Lemma W at `k = 0`, `0 ≤ r^{−2}A_r(b, 0, u) ≤ Cr²(1 + |b|)^Ne^{−cb²}`, so `J₂ = O(S³ℓ^{3/4})`.
*`J₃`*: on `r ≥ Sℓ^{1/4}`, `k = ℓ/r³ ≤ 1`, and by (7.1) `|J₃| ≤ C∫_{Sℓ^{1/4}}^∞ (ℓ²r^{−8} + ℓr^{−3}) dr ≤ C(ℓ^{1/4}S^{−7} + ℓ^{1/2}S^{−2})`.
*`J₄`*: `A₀ ≤ k²H` gives `0 ≤ J₄ ≤ Cℓ^{1/4}S^{−7}`. *`J₅`*: `|J₅| ≤ C_{r₀}ℓ` by (7.2), which is also the far statement.
Hence `ℓ^{−1/4}(ν_cand(ℓ) − cℓ^{−1/3} − B_{d,L})` has `limsup` and `liminf` within `CS^{−7}` of
`∫∫∫_0^S(𝒜^{cand} − 𝒜^{con}) ds db dσ`. The integrand is `−12π₀E₀[min(Y², 36s^{−8}Δ²)1{A < 0} | b]` (§4: `w^{cand} − w^{con}`
`= −min(Y², 36κ²Δ²)` on `{A < 0}`), and with `s₂ := (6|Δ|/|Y|)^{1/4}`,

    ∫_0^∞ min(Y², 36s^{−8}Δ²) ds = Y²s₂ + (36/7)Δ²s₂^{−7} = (8/7)Y²s₂ = (8/7)·6^{1/4}|Y|^{7/4}|Δ|^{1/4}               (7.3)

(checker C6). Letting `S → ∞` gives (CU′.1); `I^{cand}/c₁ = (8/7)6^{1/4}/((16/7)2^{1/4}) = 3^{1/4}/2` (checker C8). (CU′.2) is
(CU′.1) minus (CU.1). ∎

The rejected coefficient has a direct reading: `loss_eld − loss_cand = (36κ²Δ² − Y²)1{2κ|Δ| ≤ |Y| < 6κ|Δ|} ≥ 0` is the weight
of typed cusp-scale pairs outside the elder window (`1/3 ≤ |φ| < 1`), and
`∫_0^∞(loss_eld − loss_cand) ds = (16/7)Y²s₁ − (8/7)Y²s₂ = (8/7)(2^{5/4} − 6^{1/4})|Y|^{7/4}|Δ|^{1/4}` (checker C8, exactly in
`Q(3^{1/4})`). So the rejected density approaches `B_{d,L}` from above, and the excess is the rejected part of the
cusp-scale typed pairs. For the Gaussian kernel (exploration, §8): `I^{cand} = −0.1772744` and `I^{cand} − c₁ = 0.0921244` in
`d = 2`; `I^{cand} = −0.1394041` and `I^{cand} − c₁ = 0.0724443` in `d = 3`.

## 8. Remarks

1. **The crossover.** At fixed `κ` the elder share of the typed weight is the weight of `{|φ| < 1/3}` inside
   `{|φ| < 1}`, with weight `36κ²Δ²(1 − φ²)`. As `κ → ∞` (the cap regime `r ≪ k`) the rejected weighted mass concentrates
   on `|Δ| ≲ |Y|/κ` and is `≍ 1/κ = r/k`: the scaling `r³/k` of [C7-K] (K2) for the mass, i.e. a rejected *fraction*
   `≍ (r/k)³`, the `Θ(r³)` of [P] Theorem A and Math-#149 at fixed `k` (a referee pass found rejected fraction `× κ³ → 0.0106`
   in `d = 2`). As `κ → 0` the typed weight itself vanishes relative to the contact weight (it is `O(κ)` of it), and
   within it the elder share tends to `13/27`: since `∫_{|y|<cκ|Δ|}(36κ²Δ² − y²) dy = κ³|Δ|³(72c − 2c³/3)`, the ratio for
   `c = 2` (elder) and `c = 6` (typed) is `(416/3)/288 = 13/27` (referee computation; `0.48148` numerically in `d = 2`).
   Theorem Z's statement that all equal-height candidates are rejected concerns the different limit `k → 0` at fixed `r`,
   which does not commute with this one and lies outside the order-`r²` model (its typed weight is the `O(r⁴)` of
   #198 (W.4)). The cusp scale `r ≍ k` is the crossover between the cap regime and that equal-height regime, and the
   elder rule on it is the single number `1/3`.
2. **Candidate and rejected densities.** v1 recorded (CU′.1)–(CU′.2) as formal and said that a proof needs the rate of the
   `B_{d,L}`-part (the candidate kernel at `k → 0` over intermediate separations and the far candidate kernel). §7
   supplies it in the simplest form — both kernels are Lipschitz in the gap (Lemma L), because the gap enters the
   pinned regression affinely — and no elder information is needed for the candidate density. The rejected density
   approaches `B_{d,L}` from above, the excess being the rejected part of the cusp-scale typed pairs (§7).
3. **Numerical values (exploration, not controls).** For the Gaussian kernel `e^{−|z|²/2}` on `R^d` (the periodized
   SIDE24 covariance differs by factors `1 + O(e^{−288})`), the parity form of (CU.2) reduces to
   `c₁ = −(16/7)2^{1/4}π^{−(d−1/2)}J_d`, `J_d := E[|Y|^{7/4}|Δ|^{1/4}1{A<0} | V_u = 0, G = 0, t_u = 0]` (`d = 2, 3`), with the
   conditional laws of checker C7. `d = 2`: `c = 0.0734069193`, `c₁ = −0.26939883`, `c₁/c = −3.669938` (composite
   Gauss–Legendre quadrature, two resolutions agreeing to ten digits; confirmed by an independent referee quadrature);
   `d = 3`: `c = 0.0417759318`, `c₁ = −0.21184835`, `c₁/c = −5.071062` (deterministic quadrature over the negative-definite
   cone, two resolutions agreeing to `10^{−8}` relative), cross-checked by the shipped fixed-seed Monte Carlo over the same
   law (`−0.21163 ± 0.00014`, 1.6 standard errors), a development Monte Carlo (`−0.21188 ± 0.00010`, `2·10⁸` samples) and
   an independent referee conditional Monte Carlo (`−0.211848 ± 0.000024`, `5·10⁸` samples). So
   `ν_{3,24}(ℓ) ≈ 0.041776ℓ^{−1/3} − 0.21185ℓ^{1/4}`: the relative correction `5.071ℓ^{7/12}` is 1% at `ℓ ≈ 2.3·10^{−5}` and
   10% at `ℓ ≈ 1.2·10^{−3}`. By (CU′.1)–(CU′.2), `I^{cand} = −0.1394041` and `I^{cand} − c₁ = +0.0724443` in `d = 3`
   (`−0.1772744`, `+0.0921244` in `d = 2`). The exploration also
   tests (3.1) against the actual global elder rule of random pinned plane quintics (graded-grid union-find maximin of
   the rescaled field): at `r = 0.01` all 32 typed random cases agree with `|φ| < 1/3`, and in targeted cases at
   `r = 0.003` the boundary lies between `|φ| = 0.32` and `0.345`. (Development runs at `r = 0.05`, not shipped, disagreed
   only within `O(r/κ)` of `|φ| = 1/3` or `|φ| = 1`.)
4. **For the manuscript.** Once #191, #198 and this note are reviewed, the abstract can read
   `ν_{3,24}(ℓ) = c_{3,24}ℓ^{−1/3} + c₁ℓ^{1/4} + o(ℓ^{1/4})` with `c₁ < 0` the explicit Gaussian integral (CU.2), numerically
   `c₁ ≈ −0.2118`. Until then V3 edit E10 (`(1 + O(ℓ^{1/3}))`) is the safe statement; E12/E13 are strengthened by this
   note at candidate status.
5. **The collision field.** `𝔓` is the zoom-in limit at the scale where a maximum and a saddle are about to annihilate
   with gap comparable to the fourth power of their separation. Theorems CU.1–CU.3 are deterministic statements about
   `C⁵` functions: any field whose rescaled pinned landscape is `C²`-close to `𝔓` has the elder window `1/3` there, and
   only the law of `(f₄, γ, A)` — hence `c₁` — depends on the field. Theorem CU.4, Lemma CU.5 and §6 are proved here only
   for the [P] torus field.
6. **Consistency.** (i) #198 Remark 1's formal candidate computation is reproduced exactly (window `|Y| < 6κ|Δ|`, loss
   `min(Y², 36κ²Δ²)`), and its elder inequality `I^{eld} ≤ I^{cand}` is sharpened to `c₁ = 2·3^{−1/4}I^{cand}`. (ii) The
   typed window `|φ| < 1` is #198 Lemma W's sign window. (iii) Theorem CU is consistent with #198's `O(ℓ^{1/4})` and #191's
   `o(1)` (it uses the same inputs, so this is not an independent confirmation of them).

## 9. Sources (exact identities in `SOURCES.json`)

| Tag | Path | Role |
|---|---|---|
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`) | (R3)–(R5), §4 scaled Hessians, Lemma R3.2 — consumed |
| [C7-K] | `frontiers/c7_total_bounded_20260929/PROOF.md` (blob `28748b08`) | (K2); §4 `1 − e ≤ 1_{G_r^c}` — consumed |
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`) | §2 finite-jet rank, §4 regression, §8 maximin, §§9–10 as [E2], (10.2), §14 (far nondegeneracy), §15 (15.2) — consumed |
| [E1] | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` (blob `213594d6`) | reading rule |
| [E2] | `reviews/d1_section9_borel_repair_20260925/REPAIR.md` (blob `fe9b9ce4`) | §9 replacement |
| [REC] | `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` (blob `75da2597`) | reading rule |
| [182] | `frontiers/fixed_r_inverse_lifetime_20260930/PROOF.md` (blob `0d401877`) | §3 barrier — consumed through #198 Lemmas B, F′ |
| [Z] | `frontiers/c7_zero_gap_limit_20260929/PROOF.md` (blob `5b6328ea`) | (Z2)–(Z3), (Z10), §2 (a.s. nonsingular endpoint Hessians), the [P] §14 input of (Z16) — consumed in §7; (Z10), (Z13)–(Z14), `r_0^{[Z]}` — consumed through #198, #191 |
| #191 | `frontiers/remainder_vanishing_20260930/PROOF.md` (unmerged; v1.1 blob `441152df`) | (E.1), Lemma E Steps 1–3 and `T`, §2 (2.1)–(2.2) and the unmarked kernel `Ψ_ℓ^{cand}`, `r_0^*` — **consumed, unmerged** |
| #198 | `frontiers/remainder_rate_20260930/PROOF.md` (unmerged; v1.1 blob `abfb98ae`) | §1 elder-density identity and Lemma B (B.2), §2 Lemma F′ and its uniform far facts (a), (b), (2.2), (2.1), §3 (3.1)–(3.2) and Lemma W — **consumed, unmerged** |
| [CW] | A. Carbery, J. Wright, *Distributional and L^q norm inequalities for polynomials over convex bodies in R^n*, Math. Res. Lett. 8 (2001) 233–248 | small-ball bound for `det` (Lemma CU.5) — external, classical |

## 10. Exact controls and exploration

`cusp_check.py` (stdlib, exact rationals; `RESULTS.json` its output, byte-identical under `-O`): C1 the quartic
ridge identities and factorizations; C2 the elder window by exact 1D maximin for 117 rational `φ`; C3 the fiber
reduction; C4 the cusp limit field for pinned polynomials of degree 6 in `d = 2, 3`; C5 the model's endpoint
determinants and typed window; C6 the cusp integrals (6.1) and the candidate analogue; C7 the Gaussian-kernel
conditional covariances used by the exploration; C8 the affine gap structure behind Lemma L in the special case of pinned
polynomials (the `k`-shift `2(x − r)(x + r/2)²` has no transverse part there, so `∂_k det K_{M,S} = ∓6 det A_{M,S}` exactly; the
actual regression shift has transverse parts, covered only by the prose), the common `rY`, the constant `I^{cand}/c₁ = 3^{1/4}/2`, the
rejected cusp integral exactly in `Q(3^{1/4})` and the small-`κ` share `13/27`. Mutants M1 (threshold 1/2), M2 (constant
8/7), M3 (drop `γ·Ξ`), M4 (coefficient 2 in `e₄`), M5 (sign of `∂_k det K_M`) exit 1; an unknown label exits 2.

**What the controls do not test.** Theorem CU.1 for non-polynomial fields, Proposition CU.3, Theorem CU.4, Lemma CU.5,
§6, Lemma L for random fields and the assembly of Theorem CU′ are proved in prose only. `explore_cusp.py` (stdlib, floating point, not replayed by the workflow; output in
`EXPLORE.json`) is exploration: the actual-landscape test of the elder window and the numerical `c₁`. Neither is
acceptance.

## 11. Review slices

A: Theorems CU.1–CU.2 — the pinned Taylor bookkeeping, the fiber reduction and the one-dimensional maximin (§§1–2).
B: Proposition CU.3 — the ridge of a perturbed field, the reduction of connectivity, the trap and path arguments, the
   margins (§3).
C: Theorem CU.4 and Lemma CU.5 — the kernel limits and the window probability (§§4–5), including the conditional
   density of `f₄` and the small-determinant bound.
D: §6 — the decomposition, the dominations, the choice of `ρ₁`, the cusp integral (6.1), the sign of `c₁`; §8.
E: §7 — Lemma L (the affine gap structure of the pinned regression, the continuity of the typed product along the gap,
   the sign-window bound at intermediate gaps, the density factor; the far analogue through (Z10)) and the assembly of
   Theorem CU′ (the decomposition `J₁`–`J₅`, the cusp integral (7.3), the constants).
