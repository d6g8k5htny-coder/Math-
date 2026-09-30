# Living bars have flat components: the far elder density is `O(ℓ^N)` for every `N`

Object: CL-FAR-ELDER-FLAT-RIDGE-20260930-v1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 30 September 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register,
graph, STATUS, PROOF_INDEX, prize or Boolean change; no numerical constant is claimed. Same GitHub account as
every lane; zero organizational independence. Successor in rate to Math- #187 (`CL-FAR-ELDER-RATE-20260930-v1`,
`O(ℓ^{2/3})`), which it does not modify and whose barrier lemma it does not use.

## 0. Statement

Fixed `d ≥ 2`, torus `X = R^d/(LZ^d)`, the variance-one periodized Gaussian field of [P] §1, and a fixed
separation `ρ ∈ (0, L/4]`. For `y ∈ X` with `dist(0, y) ≥ ρ` write, as in [P] §14 and Math- #187 §0,

    O_y = (f(0), ∇f(0), f(y), ∇f(y)),      v_{b,ℓ} = (b, 0, b − ℓ, 0),
    p_y(v) = the Gaussian density of O_y at v,      Q_{y,b,ℓ} = the regression law given O_y = v_{b,ℓ},
    W(f) = |det H_0 det H_y| 1{H_0 < 0, index H_y = d − 1},      e_y(f) = the Borel ordinary elder mark
    ([P] §8: the global superlevel elder death partner of the maximum at 0 is the saddle at y),

and the far elder density per unit volume at lifetime `ℓ` (the canonical marked Kac–Rice version, [P] §9 read as
[E2]; height Jacobian 1 on this domain, [P] §14)

    ν_eld^{far,ρ}(ℓ) = ∫_{dist(0,y) ≥ ρ} ∫_R p_y(v_{b,ℓ}) E_{Q_{y,b,ℓ}}[W(f) e_y(f)] db dy.            (0.1)

[P] §14's argument gives `ν_eld^{far,ρ}(ℓ) ≤ C` on `(0, 1]` ((14.1) is its case `ρ = r_0`); [Z] gives
`ν_eld^{far,ρ}(ℓ) → 0` with no rate; Math- #187 gives `O(ℓ^{2/3})`. The SIDE24 manuscript's Proposition A.3.2 / A.3.2′ asserts `O(ℓ)` without a valid proof (July audit
F-02).

**Theorem G.** For every `ρ ∈ (0, L/4]` and every integer `N ≥ 1` there is `C = C(d, L, ρ, N) < ∞` such that

    ν_eld^{far,ρ}(ℓ) ≤ C ℓ^N,        0 < ℓ ≤ 1.                                                    (0.2)

Consequently, for `0 < t ≤ 1`, `E N_eld^{far,ρ}(0, t] ≤ C t^{N+1}/(N+1)` per unit volume, and for every real `q`
(however negative) `E Σ_{far elder bars, ℓ_i ≤ t} ℓ_i^q < ∞`: the far elder population has all inverse-lifetime
moments.

The proof rests on a deterministic inequality that holds on the superlevel component of *every* living bar.

**Lemma 1 (flat components).** Let `f ∈ C²(X)` and `K > 0` with `K ≥ sup_X ‖D²f‖_op`. Let `x_0` be a local maximum,
`b = f(x_0)`, and let `t < b` be such that the connected component `C_t` of `x_0` in the open set `{f > t}`
contains no point with `f > b`. Then for every `p ∈ C_t`

    |∇f(p)|² ≤ 2K (b − f(p)) ≤ 2K (b − t).                                                          (1.1)

The hypothesis holds exactly for `t ≥ b − ℓ(x_0)`, where `ℓ(x_0)` is the lifetime of the `H_0` bar of `x_0` under
the superlevel filtration with the elder rule ([P] §8): as long as the bar is alive, its component contains no
older (higher) maximum, and a component with a point above `b` would contain one (§1).

**Lemma 2 (crossing).** If the death partner `y` of `x_0` satisfies `dist(x_0, y) ≥ ρ`, then for `t = b − ℓ(x_0)`
the component `C_t` meets every sphere `∂B(x_0, r)`, `0 < r < ρ`, and on `C_t` one has `b − ℓ(x_0) < f ≤ b` and
`|∇f| < (2Kℓ(x_0))^{1/2}`.

**Lemma 3 (near-critical balls).** If `|∇f(p)| ≤ (2K_0ℓ)^{1/2}`, `b − ℓ < f(p) ≤ b`, `sup‖D²f‖ ≤ K_0` and
`r_ℓ = (ℓ/K_0)^{1/2}`, then every `q ∈ B(p, r_ℓ)` satisfies `|∇f(q)| ≤ 3(K_0ℓ)^{1/2}` and `|f(q) − b| ≤ 3ℓ`.

**What is not claimed.** No statement about the far *rejected* density (which stays of order one: [U] (U1) gives it
the lower bound `c_* > 0` at `ρ = r_0`, and [Z] identifies its limit); no near-pair statement (Lemma 1 is
consistent with the near law but adds nothing there, §4); no numerical `C`; no uniformity in `L`, `d`, `N` or
`ρ ↓ 0`; nothing about the true order of `ν_eld^{far,ρ}` beyond (0.2) (§4 records the expectation that it is
super-polynomially small; no rate is conjectured).

## 1. Proofs of the deterministic lemmas

**Lemma 1.** Let `p ∈ C_t` with `g = ∇f(p) ≠ 0` (for `g = 0` there is nothing to prove), `e = g/|g|`, and
`φ(s) = f(p + se)` for `0 ≤ s ≤ |g|/K` (a straight segment in the flat torus; only the values along it are used).
Since `‖D²f‖ ≤ K`, `φ'(s) = ⟨∇f(p + se), e⟩ ≥ |g| − Ks ≥ 0` on that range, so `φ` is nondecreasing and
`φ(s) ≥ f(p) > t`: the segment lies in `{f > t}` and is connected to `p`, hence lies in `C_t`. By hypothesis
`φ(s) ≤ b` there. At `s = |g|/K`,

    b ≥ φ(|g|/K) ≥ f(p) + ∫_0^{|g|/K} (|g| − Ku) du = f(p) + |g|²/(2K),

which is (1.1); the second inequality is `f(p) > t`. ∎

*The hypothesis for living bars.* In [P] §8 the ordinary death level of a maximum `x_0` is the superlevel maximin
`d_f(x_0) = sup{ min_γ f : γ a path from x_0 to a point above b }` and `ℓ(x_0) = b − d_f(x_0)`. If `C_t` contained a
point `z` with `f(z) > b`, then, `C_t` being open and connected (hence path-connected), a path inside
`C_t ⊂ {f > t}` from `x_0` to `z` would give `d_f(x_0) ≥ min_γ f > t`, i.e. `t < b − ℓ(x_0)`. So for every
`t ≥ b − ℓ(x_0)` — the death level included — `C_t ⊂ {f ≤ b}`, and Lemma 1 applies. (For an essential maximum,
`d_f = −∞` and every `t` qualifies.)

**Lemma 2.** With `t = b − ℓ(x_0)` and `C := C_t`: the mark `e_y = 1` is the event `d_f(x_0) = f(y)` of [P] §8,
which on the Morse distinct-value locus says that the component of `x_0` in `{f > s}` merges, as `s` decreases
through `t = f(y)`, with a component containing a higher maximum, at the index-`(d − 1)` saddle `y` ([P] §1 counts
negative eigenvalues, so `y` has `d − 1` negative and one positive direction). Locally at `y`,
`f = t + u² − |w|²` in Morse coordinates (`u ∈ R`, `w ∈ R^{d−1}`), so `{f > t}` near `y` is the double cone
`{|u| > |w|}`; each nappe lies in one component of `{f > t}`, and `C` contains one of them — otherwise the handle
at `y` would leave `C` a component of `{f > s}` for `s` slightly below `t`, forcing `d_f(x_0) < t`. Each nappe has
`y` in its closure, so `y ∈ cl(C)`. A connected set `C ∋ x_0` with a closure point at distance `≥ ρ` meets every
sphere `∂B(x_0, r)`, `0 < r < ρ`: otherwise `C ⊂ {dist < r} ∪ {dist > r}`, two disjoint open sets, so
`C ⊂ {dist < r}` and `cl(C) ⊂ {dist ≤ r}`, excluding `y`. The bounds are (1.1) with `b − f(p) < b − t = ℓ(x_0)`. ∎

**Lemma 3.** For `q ∈ B(p, r_ℓ)`: `|∇f(q)| ≤ |∇f(p)| + K_0r_ℓ ≤ (√2 + 1)(K_0ℓ)^{1/2} < 3(K_0ℓ)^{1/2}` and
`|f(q) − f(p)| ≤ |∇f(p)|r_ℓ + K_0r_ℓ²/2 ≤ (√2 + 1/2)ℓ`, so `|f(q) − b| ≤ (1 + √2 + 1/2)ℓ < 3ℓ` (checker F4). ∎

## 2. Fixed-separation Gaussian facts (as in Math- #187 §2, with `N` further sites)

Fix `N ≥ 1`. For `y ∈ D_ρ := {dist(0, y) ≥ ρ}` and sites `q = (q_1, …, q_N)` with

    dist(0, q_j) ≥ ρ/(4N),   dist(q_i, q_j) ≥ ρ/(4N) (i ≠ j),   dist(q_j, y) ≥ ρ/4,                    (2.0)

put `V_y = (O_y, H_0, H_y)` and `Z_q = (f(q_1), ∇f(q_1), …, f(q_N), ∇f(q_N))` (`N(d + 1)` coordinates). All entries
of `(V_y, Z_q)` are distinct derivative evaluations at `N + 2` distinct sites, so by [P] §2 (distinct-site rank of
the Fourier-summable covariance) their joint covariance is positive definite; it is continuous in `(y, q)`, hence
uniformly positive definite on the compact set of configurations (2.0). Consequently:

(a) the covariance of `V_y` is a principal submatrix of the covariance of `(V_y, Z_q)`, hence uniformly positive
    definite on `D_ρ`; so the joint density of `V_y` at `(v_{b,ℓ}, H_0, H_y)` is at most
    `C exp[−c(|v_{b,ℓ}|² + |H_0|² + |H_y|²)] ≤ C exp[−c(b² + |H_0|² + |H_y|²)]` (as `|v_{b,ℓ}| ≥ |b|`), i.e.

        p_y(v_{b,ℓ}) · density(H_0, H_y | O_y = v_{b,ℓ}) ≤ C exp[−c(b² + |H_0|² + |H_y|²)],                    (2.a)

    uniformly for `y ∈ D_ρ`, `b ∈ R`, `0 < ℓ ≤ 1` (this is the [P] §14 bound behind (14.1), restated; Math- #187
    (2.1) is the same statement). Integrating `|det H_0 det H_y|` against it, `p_y(v_{b,ℓ}) E[W | O_y = v_{b,ℓ}] ≤
    C exp(−cb²)` and `∫_{D_ρ}∫_R p_y(v_{b,ℓ}) E_Q[W] db dy ≤ C` for `0 < ℓ ≤ 1`;

(b) the conditional law of `Z_q` given `V_y` is Gaussian with covariance the Schur complement of the joint
    covariance, uniformly positive definite on (2.0); its density is therefore bounded by a constant
    `C_N = C(d, L, ρ, N)` **uniformly in the conditioning values** (the conditional covariance does not depend on
    them). Hence for every `b`, `H_0`, `H_y`, `ℓ ≤ 1` and `K_0 ≥ 1`,

        Q( |f(q_j) − b| ≤ 3ℓ and |∇f(q_j)| ≤ 3(K_0ℓ)^{1/2} for all j  |  V_y ) ≤ C_N (6ℓ)^N (ω_d 3^d (K_0ℓ)^{d/2})^N
                                                                        = C'_N K_0^{dN/2} ℓ^{N(1 + d/2)};        (2.1)

(c) regressing the field on `V_y` (the argument of [P] §4, applied at the two far sites `0`, `y` instead of the
    near pins): `f = m + g` with `g` a centred Gaussian field independent of `V_y`,
    `‖m‖_{C²} ≤ C(1 + |b| + |H_0| + |H_y|)` for `ℓ ≤ 1`, and `sup_X ‖D²g‖_op` a.s. finite with
    `E sup_X ‖D²g‖_op ≤ C` and `σ_*² := sup_{x ∈ X, |v| = 1} Var(vᵀD²g(x)v) ≤ C`, uniformly on `D_ρ` (the
    regression coefficients are fixed smooth covariance derivatives times the uniformly bounded inverse
    covariance of `V_y`, and `g`'s covariance is dominated by the field's). Since `‖A‖_op = sup_{|v|=1} |vᵀAv|`
    for symmetric `A`, the Borell–TIS inequality (Adler–Taylor, *Random Fields and Geometry*, Theorem 2.1.1)
    applied to the centred Gaussian process `(x, v, ±) ↦ ±vᵀD²g(x)v` on the compact `X × S^{d−1} × {±}` gives,
    for `u > 0`,

        P( sup_X ‖D²g‖_op > E sup_X ‖D²g‖_op + u ) ≤ exp(−u²/(2σ_*²));                                   (2.2)

(d) for every `y ∈ D_ρ`, `b ∈ R` and `ℓ > 0`, the law `Q_{y,b,ℓ}` is almost surely Morse with distinct critical
    values: [P] §8's pinned-genericity argument (distinct-site rank modulo the pins, the overdetermined-zero
    lemma on a mesh, pinned heights distinct since `ℓ > 0`, countable exhaustion) uses nothing about the pin
    separation and applies verbatim at the far pins `0`, `y`. This is where the Borel mark `e_y = 1{d_f(0) =
    f(y)}` of [E2] means ordinary elder death *at* `y` (Lemma 2 needs the distinct-value locus: off it, a second
    saddle at the same height could carry the merge).

Nothing here tends to `r = 0`; no normalizer or cap estimate is used.

## 3. Proof of Theorem G

Fix `N`, `y ∈ D_ρ`, `b`, `0 < ℓ ≤ ℓ_1 := ρ²/(64N²)` (for `ℓ_1 < ℓ ≤ 1` the bound (0.2) is §2(a) with a larger
`C`), and work under `Q = Q_{y,b,ℓ}`. Put `K := 1 + sup_X ‖D²f‖_op` and fix a threshold `K_0 ≥ 2` to be chosen.
All pathwise statements below are on the full-measure generic locus of §2(d).

*Step 1 (the event forces `N` flat sites).* On `{W(f) > 0, e_y(f) = 1}` the origin is a nondegenerate maximum with
`f(0) = b` whose death partner is the saddle `y` at `f(y) = b − ℓ`, so `ℓ(0) = ℓ` and `dist(0, y) ≥ ρ`. Lemma 2
with the shells

    S_j := { q : | dist(0, q) − jρ/(2N) | < ρ/(8N) },   j = 1, …, N,

gives points `p_j ∈ C ∩ ∂B(0, jρ/(2N)) ⊂ S_j` with `|∇f(p_j)| < (2Kℓ)^{1/2}` and `b − ℓ < f(p_j) ≤ b`. On the
further event `{K ≤ K_0}`, Lemma 3 with `r_ℓ = (ℓ/K_0)^{1/2} ≤ ℓ^{1/2} ≤ ρ/(8N)` (so `B(p_j, r_ℓ) ⊂ S_j`; the ball
is embedded since `r_ℓ < L/2`) gives

    B(p_j, r_ℓ) ⊂ A_j := { q ∈ S_j : |∇f(q)| ≤ 3(K_0ℓ)^{1/2}, |f(q) − b| ≤ 3ℓ },
    vol(A_j) ≥ ω_d r_ℓ^d = ω_d (ℓ/K_0)^{d/2}.

Hence, pathwise,

    W e_y 1{K ≤ K_0} ≤ W · ∏_{j=1}^N [ vol(A_j) / (ω_d (ℓ/K_0)^{d/2}) ].                                (3.1)

*Step 2 (Kac–Rice with `N` extra sites).* Taking expectations, writing `vol(A_j) = ∫_{S_j} 1_{A_j}(q_j) dq_j` and
using Fubini,

    E_Q[W e_y 1{K ≤ K_0}] ≤ (K_0/ℓ)^{dN/2} ω_d^{−N} ∫_{S_1 × … × S_N} E_Q[ W · ∏_j 1_{A_j}(q_j) ] dq.

For `q ∈ S_1 × … × S_N` the configuration satisfies (2.0): consecutive shells are separated by `ρ/(4N)`, the first
from the origin by `3ρ/(8N)`, and every shell from `y` by at least `ρ − ρ/2 − ρ/(8N) ≥ ρ/4` (checker F6). `W` is a
function of `(H_0, H_y) ⊂ V_y`, so by the tower property and (2.1)

    E_Q[ W · ∏_j 1_{A_j}(q_j) ] = E_Q[ W · Q(∀j: |f(q_j) − b| ≤ 3ℓ, |∇f(q_j)| ≤ 3(K_0ℓ)^{1/2} | V_y) ]
                                ≤ C'_N K_0^{dN/2} ℓ^{N(1 + d/2)} E_Q[W].

Since `vol(S_1 × … × S_N) ≤ C`, this gives (checker F5 for the exponent ledger)

    E_Q[W e_y 1{K ≤ K_0}] ≤ C_N K_0^{dN} ℓ^N E_Q[W].                                                    (3.2)

*Step 3 (the tail `K > K_0`).* By §2(c), `K ≤ 1 + C(1 + |b| + |H_0| + |H_y|) + sup_X ‖D²g‖_op`. Put
`m_* := sup_{y ∈ D_ρ} E sup_X ‖D²g‖_op < ∞`. On the event `E_1 := {1 + C(1 + |b| + |H_0| + |H_y|) ≤ K_0/2}` (an
event of `V_y`), `K > K_0` forces `sup‖D²g‖_op > K_0/2`, and for `K_0 ≥ 4m_*` (2.2) with `u = K_0/4` gives
`Q(K > K_0 | V_y) ≤ exp(−K_0²/(32σ_*²))` there (`g` is independent of `V_y`). Hence

    E_Q[W e_y 1{K > K_0}] ≤ exp(−K_0²/(32σ_*²)) E_Q[W] + E_Q[W 1{E_1^c}],                                (3.3)

and, integrating against `p_y(v_{b,ℓ}) db dy`, the second term is bounded through (2.a): for `K_0 ≥ 4(1 + C)`,
`E_1^c ⊂ {|b| + |H_0| + |H_y| ≥ K_0/(4C)}`, and `∫∫ p_y E_Q[W 1{|b| + |H_0| + |H_y| ≥ K_0/(4C)}] db dy ≤
C exp(−c'K_0²)` (the integral of `|det H_0 det H_y| e^{−c(b² + |H_0|² + |H_y|²)}` over that region).

*Step 4 (choice of `K_0`).* Take `K_0 = K_0(ℓ) := max{4m_* + 4(1 + C) + 2, C_2 (N log(1/ℓ))^{1/2}}` with
`C_2² ≥ max{32σ_*², 1/c'}`, so that `exp(−K_0²/(32σ_*²)) ≤ ℓ^N` and `exp(−c'K_0²) ≤ ℓ^N`. Integrating (3.2)–(3.3) in
`(b, y)` with §2(a):

    ν_eld^{far,ρ}(ℓ) ≤ C_N K_0(ℓ)^{dN} ℓ^N + C ℓ^N ≤ C'_N ℓ^N (1 + log(1/ℓ))^{dN/2},     0 < ℓ ≤ ℓ_1.

As `N` is arbitrary, applying this with `N + 1` in place of `N` and absorbing the logarithm (`ℓ(1 + log(1/ℓ))^a`
is bounded on `(0, 1]`) gives (0.2). The cumulative and moment statements follow by integrating `ℓ^N` over
`(0, t] ⊂ (0, 1]` (`∫_0^t ℓ^{q+N} dℓ < ∞` once `N > −q − 1`). ∎

## 4. Remarks

1. **What the far `O(1)` is.** [P] (14.1) bounds the far *candidate* density by a constant, [U] (U1) shows the far
   *rejected* density is at least `c_* > 0` on `(0, ℓ_0]` (at `ρ = r_0`), and [Z] identifies its limit as
   `∫_{D_ρ}∫Ψ_0 db dy ∈ (0, B_{d,L})`. Theorem G says that, to every polynomial order, all of the far candidate
   mass is rejected mass: far maximum/saddle pairs with a small gap exist in profusion, but essentially none of
   them is a bar. There is no tension with Lemma 1. With `C` the component of `0` in `{f > b − ℓ}`, a rejected far
   pair `(0, y)` (`f(y) = b − ℓ`, `∇f(y) = 0`, `y` not the death partner of `0`) is of one of three kinds: (i)
   `y ∉ cl(C)` — the two critical points are joined only through lower levels, which is [U]'s separated type;
   (ii) `C` already contains a point above `b` — the bar of `0` is dead at that level, Lemma 1's hypothesis fails;
   (iii) `y ∈ cl(C)` and `C ⊂ {f ≤ b}`, but `y` kills a third, lower maximum's bar or both nappes at `y` lie in
   `C` (an `H_1` birth). In case (iii) Lemmas 1–2 and §3 apply verbatim, so that part of the rejected density is
   also `O(ℓ^N)`; the order-one rejected mass lives in (i) and (ii), where nothing constrains the gradient.
2. **Consistency with the near law.** For a pinned pair at separation `r` and gap `ℓ = kr³` the axial model
   profile is the cubic `P` with `P′(x) = 6k(x² − r²/4)` ([P] (3.1)–(3.3), `P‴ = 12k`), and (1.1) holds on the
   whole axial segment with `K = 6kr` already (checker F3 uses `1 + 6kr`, exact): on this model `|∇f| ≍ kr²` against
   `(Kkr³)^{1/2} ≍ k r²`, so the inequality is consistent with the near scaling and carries no extra information
   there. Lemma 1 is a theorem, so near pairs satisfy it as well; the point is only that it does not improve the
   near remainder of Theorem R.
3. **Relation to Math- #187.** Theorem F there (`O(ℓ^{2/3})`) came from the soft-maximum barrier
   `λ_min(−H_0) ≤ (ℓK²/c_L)^{1/3}` (Math- #182 §3 (8)–(9), re-proved there) and the determinant weight `∏λ_j`;
   that mechanism sees only the Hessian at the maximum, and its spectral integral `∫_0^u λ dλ` is of order
   `ℓ^{2/3}` (no claim is made that the method cannot be sharpened). Lemma 1 sees the whole component and turns
   the far event into `N` jointly nondegenerate site conditions, each costing `ℓ^{1 + d/2}` against a volume
   `ℓ^{d/2}`, with an `N`-dependent constant. #187's Corollaries F1–F2 are superseded in rate, not in validity.
4. **The true order (non-claim).** The far event forces the field to stay within a band of width `ℓ` around the
   pinned level while its gradient stays `O(ℓ^{1/2})` along a connected set of diameter `ρ` chosen by the field
   itself — a small-ball-type event in `C¹`, though not a standard one (the set is random and the band is pinned).
   The expectation is that `ν_eld^{far,ρ}` is super-polynomially small; no rate is conjectured, and the `N`-site
   argument cannot produce one because `C_N` grows with `N`.
5. **For the manuscript.** In Theorem R's near/far decomposition ([R] §7, `ρ = r_0`), the far *elder* term is
   `O(ℓ^N)` for every `N`; Theorem R's `O(1)` remainder is unchanged — it comes from the near terms (R16) (the
   near candidate contact error) and (R18) (the near pairing loss), and, for the candidate density, from the far
   rejected `O(1)` of [P] (14.1). The manuscript's A.3.2′ (far elder contribution `O(1)`, hence `o(ℓ^{−1/3})`
   relative) rests on the reviewed (14.1) and should stay; this note, like #187, is an unreviewed candidate rate
   that the V3 text may cite as such, not a replacement of a reviewed statement.

## 5. Sources (exact identities in `SOURCES.json`)

| Tag | Path | Role |
|---|---|---|
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`) | §1 field; §2 distinct-site rank; §4 regression/independent residual; §8 elder rule and maximin; §9 marked Kac–Rice (read as [E2]); §14 far pairs and (14.1) |
| [E1] | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` (blob `213594d6`) | reading rule |
| [E2] | `reviews/d1_section9_borel_repair_20260925/REPAIR.md` (blob `fe9b9ce4`) | §9 replacement; measurability of `e_y` |
| [REC] | `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` (blob `75da2597`) | W1; consumption contract |
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`) | Theorem R, §7 near/far split (cited only) |
| [Z] | `frontiers/c7_zero_gap_limit_20260929/PROOF.md` (blob `5b6328ea`) | far rejected limit (cited only; OpenAI candidate, non-OpenAI review required) |
| [U] | `frontiers/unrestricted_selection_difference_20260929/PROOF.md` (blob `5a55b179`) | (U1) lower bound (cited only; OpenAI review `reviews/c7_nonvanishing_openai_20260929`) |
| #187 | `frontiers/far_elder_rate_20260930/PROOF.md` (Math- #187, unmerged) | predecessor rate `O(ℓ^{2/3})` (cited only; §2 restates its fixed-separation facts from [P] directly) |
| lit. | Adler–Taylor, *Random Fields and Geometry* (2007), Thm 2.1.1 (Borell–TIS) | standard inequality, §2(c) |

Consumed: [P] §§1, 2, 4 and 8 (their arguments, applied at the far pins `0`, `y`), 9 (as [E2]), 14; [E1]; [E2];
[REC] §§1, 5, 7. Cited only: [R], [Z], [U], #187.

## 6. Exact controls (`flat_ridge_check.py`; stdlib; exact rationals; byte-identical under `-O`)

F1 Lemma 1 on the explicit two-maximum landscape `f(x, y) = g(x) − y²`, `g′(x) = −4(x + 1)(x − 1/10)(x − 11/10)`
(elder maximum at `x = −1`, height `203/150`; younger at `x = 11/10`, height `31339/30000`; saddle at `x = 1/10`,
height `−661/30000`; younger lifetime `16/15`): the grid component (spacing `1/50` on `[−2, 2]²`, union-find) of
the younger maximum in `{f > t}` has 4873 points at `t` = saddle height `+ 1/1000` and 4884 points at the death
level `t` = saddle height itself, and (1.1) holds at every one of them with `K = 21`, the exact operator-norm bound
of the Hessian on the `x`-interval spanned by the component's grid points widened by one step (`[3/25, 38/25]`,
resp. `[1/10, 38/25]`; for this separable `f` the component is `{y² < g(x) − t}` over an `x`-interval, which the
widened grid interval contains); the largest ratio `|∇f|²/(2K(b − f))` is `350/451 ≈ 0.78`, so the factor-2
mutant M5 (`|∇f|² ≤ K(b − f)`) fails, at `(31/25, −3/50)`; the elder's component (6034 further points above `t`)
is present and, tested by mutant M1, violates (1.1) at `(−36/25, −7/25)`, a point with `f < b` (not the trivial
`f > b` case); mutant M2 (`K = 1`) fails at `(21/50, −11/25)`; the equality case `f = b − K|x|²/2` of (1.1) is
checked exactly.
F2 the uphill-segment inequality and monotonicity of the proof of Lemma 1 at 16 rational segments with the same
`K = 21`.
F3 the near cubic: (1.1) on `[−r/2, r/2]` with `K = 1 + 6kr` at 189 rational points, and `P(−r/2) − P(r/2) = kr³`.
F4 Lemma 3's constants through squares; mutant M3 (constant 2) fails.
F5 the exponent ledger `(K_0/ℓ)^{dN/2}(K_0^{d/2}ℓ^{1+d/2})^N = K_0^{dN}ℓ^N`, `d ∈ {2,3,5}`, `N ∈ {1,2,7}`; mutant M4
fails. Mutants `M1`–`M5` exit 1; an unknown label exits 2.
F6 the shell geometry (2.0) for `N = 1, …, 6` and three values of `ρ`.

The controls check the deterministic inequalities and the bookkeeping; they do not prove the Gaussian estimates of
§2 and are not acceptance.

## 7. Review slices

A: Lemma 1 and its hypothesis for living bars (the elder-rule argument in §1), Lemma 2, Lemma 3.
B: §2 (a)–(d) — the uniform conditional density bound with `N` extra sites from [P] §2, the regression
   decomposition and the use of Borell–TIS, and the far-pin genericity (d); whether (2.1) is stated at the right
   scope.
C: §3 — the volume/Markov step (3.1), the tower-property step, the `K_0` splitting and the choice (Step 4), and the
   integration in `(b, y)`; Remarks 1–3 for consistency with [U], [Z], [R] and #187.
