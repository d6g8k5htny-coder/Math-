# Soft rejected pairs in `d = 2`: the `1/κ` tail of the rejected cusp kernel, the fold-scale rejection function, and a conjectured `ℓ^{2/3}` term

Object: CL-SOFT-REJECTED-20261002-v1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 2 October 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE (Theorem 1, Lemmas 2, 3 and 5, Proposition 4); CONJECTURES 6 and 7, with numerical
evidence. Nonauthor review required. Scientific effect: NONE — no register, graph, STATUS, PROOF_INDEX, prize or Boolean
change; no numerical constant is certified. Same GitHub account as every lane; zero organizational independence.

**Why.** Math- #229 (merged) proves
`ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} − ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{3/7})` ((R⁺.1)). Math- #240 (open) proves that each
fixed cusp window `κ₀ ≤ ℓ/r⁴ ≤ κ₁` contributes a multiple of `ℓ^{1/4}` with error `O(ℓ^{3/4})`, and its Remark 1 leaves the
ends `κ → ∞` and `κ → 0` open. This note studies the end `κ → ∞` for the rejected pairs in `d = 2`. Formally it is the only
source of the next term of `ρ_rej` (§4).

**What is new.**
- **Theorem 1** (§1). In `d = 2`, `κ𝒜^{rej}(b, κ, u) = F₀(b, u) + O(κ^{−1})` as `κ → ∞`, uniformly with Gaussian decay in
  `b`, where `F₀ = (5/24)π₀(u; v₀(b, 0))p_A(0 | b)E[γ⁶] > 0`. The rejected weight sits on *soft* transverse curvatures
  `λ = −A ∈ [γ²/(24κ), γ²/(8κ)]`, up to relative errors `O(1/κ)`.
- **The fold-scale soft model** (§2). At fixed `k = ℓ/r³` and `λ = λ̃r/k`, the window field divided by `κ = k/r` tends to an
  explicit polynomial `G_k` in which two more jets enter: `B = ∂_uA` and `C₃ = ∂_Θ³f`. **Lemma 2** decides the elder mark in
  `G_k` exactly by a one-dimensional scan, including a case in which the saddle is not on the ridge. **Lemma 3** gives an a
  priori elder region. The typed weight is `(γ⁴/16)(φ^{−2} − (1 − 12kB/γ²)²)₊`.
- **Proposition 4** (§3). For the Gaussian kernel, the fold-scale rejection rate is `F(k; b) = F₀(b)H(k)` with `H` free of `b`,
  and `H(k) = 1 + (12/25)k² + O(k³)`. The elder edge moves to `φ_e = 1/3 + t/3 + 10t²/27 + O(t³)` (`t = 12kB/γ²`). The
  resulting `+312/25` nearly cancels the `−12` of the pin density `e^{−12k²}`.
- **Lemma 5 and Conjecture 7** (§4). The two-scale composite density has the expansion
  `(I^{cand} − c₁)ℓ^{1/4} + R_{2/3}ℓ^{2/3} + O(ℓ^{3/4})`, with `R_{2/3}` given by `F` and `F₀`. Conjecture 7 says that
  `ρ_rej + ν_eld^{far,r_0^*} − B_{2,L}` has the same expansion. For the Gaussian kernel, numerically `R_{2/3} ≈ −0.049`
  (§5).
- **Evidence** (§5, exploration):
  - the tail of Theorem 1 by quadrature;
  - Lemma 2 against a two-dimensional flood fill;
  - `H` by quadrature;
  - #216's Monte Carlo of the rejected adjacent pairs, binned by lifetime and by `s = r/ℓ^{1/4}`. It shows the predicted
    suppression at small `s`: for `s < 0.8`, 37 pairs are observed and 35.3 predicted, against 4,322 from the cusp kernel
    alone.

**Dependencies.**
- Consumed (all merged): #220 (`frontiers/elder_third_order_20261001/PROOF.md`, blob `c8767dde`): §0 ((0.1), (0.2)) and §1
  (window coordinates, (1.1), Lemma Q, (M1)–(M6)). #218 (`frontiers/candidate_third_order_20261001/PROOF.md`, blob
  `70ca57ef`): §0 (`𝒜^{cand}`, `I^{cand}`, `B_{d,L}`). #229 (`frontiers/third_order_rate_20261001/PROOF.md`, blob
  `110ed33a`): (R⁺.1) and §0 (`Y_r`). #207 (`frontiers/cusp_second_order_20261001/PROOF.md`, blob `f6df5a73`): §§0, 4, 6 and
  Theorem CU.2(c). [R] (`frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf`): (R5). [P] §2, through #220.
- Cited only: [C7-K] (`frontiers/c7_total_bounded_20260929/PROOF.md`, blob `28748b08`): (K2). #240 (open): Lemma Q′, Step N6,
  Corollary N′, Remarks 1 and 4. #237 (open): Theorem P, Remark 4. #216 (open): the Monte Carlo. #187 (merged) and #188 (open): the far
  elder density.

## 0. Setting

Setting and notation are those of #220 §0 and #218 §0 (through #207 §§0, 4, 6), specialized to `d = 2`, `m = 1`:
- the [P] field on `X = R²/(LZ²)`; near pins `M = −ru/2`, `S = ru/2` at heights `b` and `b − kr³`; `κ = k/r`, so the lifetime is
  `ℓ = kr³ = κr⁴`; `Θ` is the unit vector orthogonal to `u`;
- the jets at `0` under the contact law at `v₀(b, k)` (#220 §2; expectation `E_{v₀(b,k)}`, and `E₀[· | b]` at `k = 0`):
  `A = ∂_Θ²f` (a scalar), `f₄ = ∂_u⁴f`, `γ = ∂_u²∂_Θf`, `B = ∂_u∂_Θ²f = ∂_uA`, `C₃ = ∂_Θ³f`. On `{A < 0}` put `λ := −A`, so
  `Δ = A = −λ`, `adj A = 1`, and

      Y = (f₄/12)Δ − γ²/4 = −(λ/12) z,    z := f₄ + 3γ²/λ = f₄ − 3γᵀA^{−1}γ,    φ := z/(72κ);                    (0.1)

- the cusp kernels (#220 (0.1), #218 §0): `𝒜^*(b, κ, u) = 12π₀(u; v₀(b, 0))E₀[w_κ 1_* | b]` with
  `w_κ = 36κ²Δ² − Y² = (λ²/144)(5184κ² − z²)`, `1_cand = 1{A < 0, |z| < 72κ}` and `1_eld = 1{A < 0, |z| < 24κ}`. So

      𝒜^{rej}(b, κ, u) := (𝒜^{cand} − 𝒜^{eld})(b, κ, u) = 12π₀(u; v₀(b, 0)) E₀[(λ²/144)(5184κ² − z²) 1{A < 0, 24κ ≤ |z| < 72κ} | b].   (0.2)

  The contact terms cancel, so by #220 (0.2) and #218 §0, `I^{cand} − c₁ = ∫_{S¹}∫_R∫_0^∞𝒜^{rej}(b, s^{−4}, u) ds db dσ(u)`.

Two facts about the contact law are used. The pin set splits into even pins `(f, ∂_u²f, ∂_u∂_Θf)` and odd pins
`(∂_uf, ∂_u³f, ∂_Θf)`, and even- and odd-order derivatives of a stationary field at a point are uncorrelated; the
nondegeneracy statements come from the finite-jet rank of [P] §2.
- (G1) Under `v₀(b, 0)`, `γ` is centred Gaussian with variance `σ_γ²(u) > 0` and independent of `(A, f₄)`.
- (G2) Given `b`, `(A, f₄)` is a nondegenerate Gaussian vector whose mean is affine in `b`. Write `p_A(a | b)` for the density
  of `A`, and `p_A(a | f₄, b)` for its conditional density given `f₄`.

**The Gaussian kernel.** For `C(x) = e^{−|x|²/2}` on `R²`, an exact computation (control S3) gives the following. Given
`∇f(0) = 0`, the third-order jets `(∂_u³f, γ, B, C₃)` are independent, with variances `(6, 2, 2, 6)`, and uncorrelated with
every even jet. Hence under `v₀(b, k)` the jets `(γ, B, C₃)` are centred and independent of `(A, f₄)`, and the gap pin
`∂_u³f = 12k` contributes the factor `e^{−144k²/(2·6)} = e^{−12k²}` to the pin density.                                         (0.3)
The periodized kernel of the torus field agrees with `C` up to `O(e^{−L²/8})`. Statements labelled *Gaussian kernel* are
about the model case `C` on `R²`, as in #207 §8.

## 1. The soft tail of the rejected cusp kernel

**Theorem 1.** There are `C, c, N` such that for `κ ≥ 1`, `b ∈ R` and `u ∈ S¹`,

    |κ 𝒜^{rej}(b, κ, u) − F₀(b, u)| ≤ C κ^{−1} (1 + |b|)^N e^{−cb²},     F₀(b, u) := (5/24) π₀(u; v₀(b, 0)) p_A(0 | b) E[γ⁶].   (1.0)

For the Gaussian kernel `E[γ⁶] = 15σ_γ⁶ = 120`, so `F₀ = 25π₀(v₀(b, 0))p_A(0 | b)`.

*Proof.* Fix `b` and `u`. The constants below are uniform in `u` and polynomial in `b` before the factor `π₀`, which carries
`e^{−c₀b²}` ([R] (R5)). Split the expectation in (0.2) on `{A < 0}`.

*Step 1 (negative `z` and large `|f₄|`).* By (0.1), `z ≥ f₄` on `{A < 0}`. So `z ≤ −24κ` forces `f₄ ≤ −24κ`, and the weight is
at most `36κ²λ²`. On `{|f₄| ≥ κ}`, (G2) gives `E₀[λ²1{|f₄| ≥ κ} | b] ≤ C(1 + |b|)^N e^{−c(κ − C|b|)₊²}`. Multiplied by `π₀`,
this is `≤ C(1 + |b|)^N e^{−cb²}e^{−cκ²}` (if `|b| ≥ κ/(2C)`, use `e^{−c₀b²}`). Both parts are `O(κ^{−2})` after
multiplying by `κ`.

*Step 2 (the soft window).* On `{|f₄| < κ, 24κ ≤ z < 72κ}` we have `3γ²/λ = z − f₄ ∈ (23κ, 73κ)`, so the event is
`{λ ∈ (3γ²/(72κ − f₄), 3γ²/(24κ − f₄)]}`. For fixed `(γ, f₄)`, `λ ↦ φ = (f₄ + 3γ²/λ)/(72κ)` is a decreasing bijection onto
`[1/3, 1)`, with `λ = 3γ²/(72κφ − f₄)` and `|dλ/dφ| = 216κγ²/(72κφ − f₄)²`. Using `5184κ² − z² = 5184κ²(1 − φ²)`,

    ∫ p_A(−λ | f₄, b) (λ²/144)(5184κ² − z²) 1{…} dλ = ∫_{1/3}^{1} p_A(−λ(φ) | f₄, b) · 69984 κ³ γ⁶ (1 − φ²)/(72κφ − f₄)⁴ dφ.   (1.1)

Since `69984/72⁴ = 1/384`, the factor `69984κ³/(72κφ − f₄)⁴` equals `(384κφ⁴)^{−1}(1 − f₄/(72κφ))^{−4}`, and
`|f₄/(72κφ)| ≤ 1/24` on this event. So

    |(1 − f₄/(72κφ))^{−4} − 1| ≤ C|f₄|/κ,      |p_A(−λ | f₄, b) − p_A(0 | f₄, b)| ≤ C_b λ ≤ C_b γ²/κ,                     (1.2)

where `C_b` is a polynomial in `|b|` and `|f₄|` (the conditional density is Gaussian, with variance bounded below and mean
affine in `(f₄, b)`). Hence (1.1) equals `(γ⁶/(384κ))p_A(0 | f₄, b)∫_{1/3}^1(φ^{−4} − φ^{−2})dφ + κ^{−2}O(γ⁸ + γ⁶|f₄|)·poly`,
and `∫_{1/3}^1(φ^{−4} − φ^{−2})dφ = 20/3`.

*Step 3 (integration).* Integrate over `f₄` given `b`; restoring `|f₄| ≥ κ` costs Step 1's bound. Use
`E[p_A(0 | f₄, b) | b] = p_A(0 | b)`, and integrate over `γ` by (G1), with `E[γ⁶], E[γ⁸] < ∞`. Multiplying by `12π₀` and
by `κ` gives `κ𝒜^{rej} = 12π₀p_A(0 | b)E[γ⁶](20/3)/384 + O(κ^{−1})·poly(b)π₀`, and `12·(20/3)/384 = 5/24`. ∎

*Remarks on Theorem 1.*
1. Theorem 1 is about the cusp kernel `𝒜^{rej}` itself, not about the non-uniformity of #240's Theorem N as `κ → ∞`. The
   rejected weight sits on `λ ∈ [γ²/(24κ), γ²/(8κ)]` (Step 2), so the rejected pairs at large `κ` are soft in the transverse
   direction. In #220's elder decision they are the pairs with `|φ| ∈ (1/3, 1)` coming from `3γ²/λ ≈ z`, not from `f₄`.
2. Expanding (1.2) to first order gives `κ𝒜^{rej}/F₀ = 1 + c(b)/κ + O(κ^{−2})` with
   `c(b) = (12/5)[E(f₄ | A = 0, b)/18 − ∂_a log p_A(0 | b)·E[γ⁸]/(24E[γ⁶])]`, where `12/5` is the mean of `1/φ` under the
   weight `φ^{−4} − φ^{−2}` on `[1/3, 1]`. For the Gaussian kernel, `A ~ N(−b, 2)` and `f₄ ~ N(−3b, 24)` are independent
   given `b`, and `c(b) = 0.3b`.
3. With `s = κ^{−1/4}`, for an isotropic field `∫_{S¹}𝒜^{rej}(b, s^{−4}, u) dσ(u) = 2πF₀(b)s⁴ + O(s⁸(1 + |b|)^N e^{−cb²})`.
   So the `s`-integral defining `I^{cand} − c₁` converges at `s = 0` like `s⁵`, and `s ≤ s₀` contributes
   `2π∫F₀ db · s₀⁵/5 + O(s₀⁹)`.
4. *Numerically* (Gaussian kernel; §5):
   - `F₀(0) = 0.008207`, `F₀(1) = 0.003019` and `∫F₀ db = 0.0145472`, so the `s⁴`-coefficient is `2π∫F₀ db = 0.091403`.
   - `κ𝒜^{rej}(0, κ)/F₀(0) = 0.509, 0.751, 0.917, 0.977, 0.9985, 0.9999` at `κ = 1/2, 1, 2, 4, 16, 64` (`c(0) = 0`).
   - `κ(κ𝒜^{rej}/F₀ − 1) = 0.280, 0.295` at `b = 1` and `−0.318, −0.305` at `b = −1`, at `κ = 16, 64`, as `c(±1) = ±0.3`
     predicts.

## 2. The fold-scale soft model

Theorem 1 shows where the rejected weight sits as `κ → ∞` along the cusp scale. The *fold scale* is the regime of fixed
`k = ℓ/r³` and `r → 0`, so again `κ = k/r → ∞`. There the pair is rejected only if the transverse curvature is of order `r`
([C7-K] (K2) bounds the rejected weight by `O(r³/k)`), and two more jets enter. This section is formal for the field (the
limit is Conjecture 6) and exact for the model.

*The limit window field.* In the window coordinates of #220 §1 (`Φ(X, Ξ) = rXu + r²ΞΘ`, `𝔉 = r^{−4}(f∘Φ − b)`), put `λ = λ̃/κ`
and `Ξ = κζ`, so that `x = rX` and `y = rkζ`. Every monomial `x^iy^j` of the Taylor expansion at `0` contributes
`r^{i+j−3}k^{j−1}X^iζ^j` to `𝔉/κ = (f(rX, rkζ) − b)/(kr³)`. After the pin corrections of #220 (1.1),

    𝔉(X, κζ)/κ = G_k(X, ζ) + r G₁(X, ζ) + O_k(r²(1 + |ζ|)⁵)    (|X| ≤ 3, rk|ζ| ≤ 1),
    G_k(X, ζ) := 2(X + ½)²(X − 1) + ½(X² − ¼)γζ − ½λ̃ζ² + ½kBXζ² + (k²/6)C₃ζ³,                                         (2.1)
    G₁ = (f₄/(24k))(X² − ¼)² + (k/4)∂_u²∂_Θ²f·X²ζ² + (k²/6)∂_u∂_Θ³f·Xζ³ + (k³/24)∂_Θ⁴f·ζ⁴ + (1/6)∂_u³∂_Θf·X(X² − ¼)ζ.

Control S10 checks (2.1), including `G₁`, on exactly pinned polynomial fields. The pins are exact: `G_k(−½, 0) = 0`,
`G_k(½, 0) = −1`, and `∇G_k = 0` at both.

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

The scaled Kac–Rice weight is `36λ̃² − Y² = (γ⁴/16)(φ^{−2} − c′²)`. With `dλ̃ = (γ²/(24φ²))dφ`, the weight per unit `φ` is
`(γ⁶/384)φ^{−2}(φ^{−2} − c′²)`. By (2.4), `1 + β/2 − φ = 1 − φc′ > 0`, so the `z`-curvature `−(1 + β/2)` at `M` is negative.

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
- (D′) `1 − β/2 < 0` and `χ ≠ 0`, `½ ∈ I_M`, `I_M = (X_L, X_R)` is bounded, and on `I_M` we have `R < 0` for `X ≠ −½` and
  `V < L_S` for `X ≠ ½`.

If `1 − β/2 < 0` and `χ = 0`, then `e = 0`.

*Proof.* Fix a level `c`. On a non-open slice, `{z : G(X, z) > c}` has a bounded *ridge piece* around `z_r` when `R(X) > c`.
When `χ ≠ 0` it also has an unbounded *far piece* beyond `z_v`, and the two are one interval iff `V(X) > c`. On an open slice
the set is unbounded (one or two half-lines, or `R`), and `G → +∞` along it, as along every far piece.
1. *Above `L_S`.* Let `c ↓ L_S`. Suppose no `X ∈ I_M` has `V(X) > c`. Then the component of `{G > c}` containing `M` is the union of
   the ridge pieces over `I_M`. These vary continuously and shrink to points at finite ends of `I_M`, and the supremum of the
   union is `max_{I_M} R`. So `M` is still the oldest point of its component iff `I_M` is bounded and `R < 0` on
   `I_M ∖ {−½}`.
   - If `I_M` is unbounded, then as `|X| → ∞` along it, either some limit point of `I_M` is open or `R → ±∞` (a finite limit is
     excluded by hypothesis). The value `−∞` contradicts `R > L_S` on `I_M`, so the component reaches above `0`.
   - If some `X ∈ I_M` has `V(X) > c`, the component meets a far piece.
   In all of these cases `M` has died at a level above `L_S`, and `e = 0`.
2. *`1 − β/2 > 0`.* At `X = ½`, where `p = 0`, the slice has its local maximum at `z = 0`, with value `L_S`. So `S` lies on the
   ridge, and the right end of `I_M` is at most `½`.
   - If it is smaller, `R` drops below `L_S` between `M` and `S`, so `S` is not in the closure of `M`'s component above `L_S`,
     and `e = 0`.
   - Otherwise, for `c < L_S` close to `L_S`, the component of `M` contains `S` and the segment `{(X, 0) : X > ½}`. Along it
     `G = A₀(X)` increases from `L_S` to `+∞`. So `S` merges `M`'s component with one containing points above `0`, and `M` dies
     at `S`.
3. *`1 − β/2 < 0`.* Now `a(½) < 0`.
   - If `χ = 0`, `a` vanishes at `X = 1/β ∈ (0, ½)`, and `R = A₀ + p²/(8a) → +∞` as `X ↑ 1/β`. Meanwhile
     `R ≥ G(X, 0) = A₀ > L_S` on `(−½, 1/β)`. So `R > 0` somewhere on `I_M`, and `e = 0`.
   - If `χ ≠ 0`, the slice at `X = ½` has its local minimum at `z = 0` (value `L_S`) and its local maximum at `z = 2a(½)/χ`
     (value `L_S + (2/3)|a(½)|³/χ² > L_S`). So `S` is the valley point of this slice. `V` has a strict local maximum `L_S` at
     `X = ½`, because the Schur complement of `∂_z²G(S) > 0` in the indefinite Hessian is negative.
   - If `½ ∉ I_M`, `S` is not in the closure of `M`'s component above `L_S`, and `e = 0`.
   - If `½ ∈ I_M` and Step 1 leaves `M` alive, then for `c < L_S` close to `L_S` the slice at `X = ½` is one interval. So `M`'s
     component contains the far piece at `X = ½`, along which `G → +∞`, and `S` kills `M`. ∎

Case (D′) is not empty. Numerically (control S8), `(φ, β, χ) = (0.2401, 2.1425, 0.5536)` is elder, with `I_M ≈ (−1.032, 0.515)`.
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

## 3. The fold-scale rejection function

Formally, at fixed `k` the rejected kernel is the expectation of the rejected weight of §2 over the jets. With
`λ = λ̃r/k`, the law of `λ` near `0` contributes `p_A(0 | b)·(r/k)dλ̃`, and the contact pin density at gap `k` is
`π₀(u; v₀(b, k))`. This motivates

    F(k; b, u) := 12 π₀(u; v₀(b, k)) p_A(0 | b, k) E_{v₀(b,k)}[(γ⁶/384) I(12kB/γ², 576k²C₃/γ³) | A = 0],                (3.1)

with the expectation under the contact law at `v₀(b, k)`, conditioned on `A = 0`. Formally,
`r^{−2}A_r^{rej}(b, k, u) = (r/k)F(k; b, u) + o(r)` (Conjecture 6 below). As `k → 0`, `I → I(0, 0) = 20/3`, and (3.1) tends
to the `F₀` of Theorem 1.

**Proposition 4 (Gaussian kernel).** Let `C(x) = e^{−|x|²/2}`. Then:
1. `F(k; b) = F₀(b)H(k)`, where `H(k) := e^{−12k²}E[γ⁶I(t, χ₀)]/(E[γ⁶]·20/3)` does not depend on `b`; here `(γ, B, C₃)` are
   independent `N(0, 2)`, `N(0, 2)` and `N(0, 6)`, and `(t, χ₀) = (12kB/γ², 576k²C₃/γ³)`.
2. `H(k) = 1 + (12/25)k² + O(k³)` as `k → 0`.
3. `H(k) ≤ C(1 + k⁴)e^{−12k²}`; in particular `|H(k) − 1| ≤ C min(1, k²)`.

*Proof.* (1) By (0.3), the gap pin contributes `e^{−12k²}`, so `π₀(v₀(b, k)) = π₀(v₀(b, 0))e^{−12k²}`. This is the factor
`e^{−a′k²}`, `a′ = 12`, of #240 Step N6. `p_A(0 | b, k) = p_A(0 | b)`, and the law of `(γ, B, C₃)` is as stated, centred and
independent of `(A, f₄, b)`.

(2) *The edge at `χ₀ = 0`.* For `χ = 0` and `a > 0` the ridge is `R = A₀ + p²/(8a)`. At `t = 0` it is
`[2(X + ½)²(X − 1) + 3φ(X² − ¼)²]/(24φ)`, and

    R − L_S = (X − ½)²[2(X + 1) + 3φ(X + ½)²]/(24φ)      (t = 0),                                                    (3.2)

whose bracket has discriminant `4 − 12φ` in `X + ½`. At `φ = 1/3`, (3.2) is `((X − ½)(X + 3/2))²/(24φ)`, with a nondegenerate
double zero at `X = −3/2`. The elder edge solves `R(X) = L_S`, `R′(X) = 0` in `(X, φ)` at `β = 2tφ`. The Jacobian at
`(−3/2, 1/3, t = 0)` is `−96 ≠ 0`, so the implicit function theorem gives analytic `X_e(t)` and `φ_e(t)`. Their series
(control S4) are

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

(The true next correction is of order `k^{7/2}`, since `E[γ⁶t⁴] = ∞`.)

(3) Lemma 3 gives `γ⁶I ≤ C(γ⁶ + 1728k³|B|³ + 331776k⁴C₃²)`. ∎

So for the Gaussian kernel the rejected-pair rate at the fold scale starts at its cusp-scale value `F₀`. The pin density
lowers it by `12k²`, and the motion of the elder edge raises it by `(312/25)k²`, so the two nearly cancel (`12/25`
remains). Numerically `H₀ − 1` (with `C₃` ignored) already changes sign near `k ≈ 0.08`.

For another stationary kernel with `B` and `γ` independent of each other and of `∂_u³f` under the contact law, the two
coefficients are `−144/(2σ₃²)` and `(1872/75)σ_B²/σ_γ⁴`, with `σ₃² := Var(∂_u³f | ∇f(0) = 0)`. For the Gaussian kernel,
`σ_B² = σ_γ² = 2` and `σ₃² = 6`.

## 4. The composite density and the conjectured `ℓ^{2/3}` term

The cusp kernel is the `k → 0` limit, and `(r/k)F(k; b, u)` the `κ → ∞` limit, of the same rejected kernel. Theorem 1 says
that they agree in the overlap: `F(k)/F₀ → 1`. Put `H(k; b, u) := F(k; b, u)/F₀(b, u)`; for the Gaussian kernel this is the `H(k)`
of Proposition 4. The simplest density built from both limits is the *composite*

    ν^c(ℓ) := ∫_0^∞∫_R∫_{S¹} 𝒜^{rej}(b, ℓ/r⁴, u) H(ℓ/r³; b, u) dσ(u) db dr.                                            (4.1)

**Lemma 5 (expansion of the composite).** Let `H ≥ 0` be measurable with `|H(k; b, u) − 1| ≤ C_H min(1, k²)` uniformly
(Proposition 4(3) for the Gaussian kernel). Then, as `ℓ ↓ 0`,

    ν^c(ℓ) = (I^{cand} − c₁) ℓ^{1/4} + R_{2/3} ℓ^{2/3} + O(ℓ^{3/4}),
    R_{2/3} := ∫_{S¹}∫_R∫_0^∞ v⁴[F(v^{−3}; b, u) − F₀(b, u)] dv db dσ(u),    F := F₀H.                                 (4.2)

For the Gaussian kernel, `R_{2/3} = 2π∫F₀ db · Ĩ` with `Ĩ := ∫_0^∞ v⁴[H(v^{−3}) − 1] dv`.

*Proof.* The inner integral converges: its integrand is `O(v⁴)` at `0` and `O(v^{−2})` at `∞`, with Gaussian decay in `b`.
Write `H = 1 + (H − 1)`. The term with `1` is `ℓ^{1/4}(I^{cand} − c₁)` after `r = sℓ^{1/4}` (§0). For the term with `H − 1`, let
`P(b) := (1 + |b|)^N e^{−cb²}`.
- *`r > ℓ^{1/4}` (`κ < 1`).* `0 ≤ 𝒜^{rej} ≤ 𝒜^{con} ≤ Cκ²P(b)` and `|H − 1| ≤ Cℓ²r^{−6}`, so this part is
  `≤ Cℓ⁴∫_{ℓ^{1/4}}^∞ r^{−14} dr = O(ℓ^{3/4})`.
- *`r ≤ ℓ^{1/4}` (`κ ≥ 1`).* By Theorem 1, `𝒜^{rej} = F₀r⁴/ℓ + O(P(b)r⁸/ℓ²)`. With `r = vℓ^{1/3}`, the main part is
  `ℓ^{2/3}∫_0^{ℓ^{−1/12}}v⁴(F(v^{−3}) − F₀)dv`, which equals `ℓ^{2/3}` times the full `v`-integral up to `O(ℓ^{1/12})`. The
  error is `≤ CP(b)ℓ∫_0^{ℓ^{−1/12}}v⁸min(1, v^{−6})dv = O(P(b)ℓ^{3/4})`.
Integrating over `b` and `u` gives (4.2). ∎

**Conjecture 6 (the fold-scale limit).** In `d = 2`, for every `k > 0`, `b` and `u`,
`lim_{r↓0} (k/r)·r^{−2}A_r^{rej}(b, k, u) = F(k; b, u)`, locally uniformly in `k`.

**Conjecture 7 (the next term of the rejected density).** In `d = 2`,

    ρ_rej(ℓ) + ν_eld^{far,r_0^*}(ℓ) = B_{2,L} + (I^{cand} − c₁) ℓ^{1/4} + R_{2/3} ℓ^{2/3} + O(ℓ^{3/4}),                       (4.3)

with `R_{2/3}` as in (4.2); equivalently, `ρ_rej + ν_eld^{far,r_0^*} − B_{2,L} − ν^c = O(ℓ^{3/4})`. This is (R⁺.1) of #229 with
its remainder resolved. If `ν_eld^{far,r_0^*}(ℓ) = O(ℓ^{3/4})` (#188, open, claims `O(ℓ^N)`), then
`ρ_rej = B_{2,L} + (I^{cand} − c₁)ℓ^{1/4} + R_{2/3}ℓ^{2/3} + O(ℓ^{3/4})`. For the Gaussian kernel, numerically
`R_{2/3} ≈ −0.049` (§5).

*What a proof needs.* Inputs (i) and (ii) are missing; (iii) is needed only to drop the far term.
- (i) *The soft layer.* A two-scale version of Conjecture 6, uniform from the cusp scale to the fold scale (`κ ≥ κ₁`), with
  errors integrating to `O(ℓ^{3/4})`. In fixed cusp windows this is #240's Theorem N (`O(r²)`). The new part is the window
  field's elder decision in the soft scaling `λ ≍ r`: Lemma 2 with margins for the field, as #240 Lemma Q′ gives them with
  `ε̃` for `λ ≍ 1`.
- (ii) *The end `κ → 0`.* On the intermediate separations `ℓ^{1/4} ≪ r ≤ r_0^*`, the rejected kernel must match `B_{2,L}`'s part
  plus the composite's own part, up to errors integrating to `O(ℓ^{3/4})`. (The composite is not negligible there:
  `𝒜^{rej} ≍ κ³` as `κ → 0`, so `r ≥ Sℓ^{1/4}` contributes about `ℓ^{1/4}S^{−11}`.) The best available bounds on these
  separations are #229's `O(ℓ^{4/9}log(1/ℓ))` (elder) and #237's `O(ℓ^{3/5})` (candidate), both larger than `ℓ^{2/3}`.
- (iii) *The far elder density.* #187 (merged) gives `ν_eld^{far,r_0^*}(ℓ) ≤ Cℓ^{2/3}`, which is the same order as the
  conjectured term. Conjecture 7 is stated with `ν_eld^{far,r_0^*}` on the left for that reason; #188's `O(ℓ^N)` would remove
  it.

Formally, a matched-asymptotics count gives cusp-side powers `ℓ^{(m+1)/4}` and fold-side powers `ℓ^{(m+1)/3}`. In `ρ_rej` the
fold-scale kernel is `O(r³/k)` ([C7-K] (K2)), with leading coefficient `F` (formally, Theorem 1 and Proposition 4). This
makes `ℓ^{2/3}` the first fold-side power and `ℓ^{3/4}` the next cusp-side one (#240 Corollary N′).

*Remarks.*
1. `ν_cand` has no term from this mechanism. In `ν_eld = ν_cand − ρ_rej` the soft layer contributes `−R_{2/3}ℓ^{2/3}`, in
   addition to any `ℓ^{2/3}` term of `ν_cand`: the typed boundary `λ ≍ r` also produces an `|r|³` term in the candidate kernel.
   #237's remainder `ℓ^{3/5}` allows both. Only `ρ_rej`, or the rejected Monte Carlo row binned in `s`, tests `R_{2/3}` alone,
   and only subject to (ii)–(iii).
2. For the Gaussian kernel, `Ĩ` is dominated by `v ∈ [1, 1.5]`, that is `k ∈ [0.3, 1]`, where `H` falls from `≈ 1` to `≈ 0`. The
   contributions are `−0.200` (`v < 1`), `−0.563` (`1 ≤ v ≤ 1.5`), `+0.003` (`1.5 ≤ v ≤ 2`) and `+0.223` (`v ≥ 2`).
3. `R_{2/3}/(I^{cand} − c₁) ≈ −0.53`. Since `ℓ^{5/12} = 0.147` at `ℓ = 10^{−2}`, the `ℓ^{2/3}` term is about 8% of the `ℓ^{1/4}`
   term there.

## 5. Numerical evidence (exploration; not part of the proofs)

Gaussian kernel `e^{−|z|²/2}`, `d = 2`. The scripts are in the project archive
`V2_2/frontiers_soft_rejected_pairs_20261002/exploration/` (numpy, scipy, mpmath, sympy); none is part of the repository.

1. *Theorem 1.* Quadrature of (0.2) under the contact law (`fastk.py`, `soft_d2.py`) gives the numbers of Remark 4 of §1. The
   `b`-integrated tail is `κ∫𝒜^{rej}(b, κ) db → 0.0145472 = ∫F₀ db`. Also `∫∫𝒜^{rej}(b, s^{−4}) ds db = 0.014662`, and its `2π`
   multiple is `I^{cand} − c₁ = 0.092124`.
2. *Lemma 2.* The one-dimensional decision (`dec1d.py`) was compared with a flood fill of `{G > L_S ± ε}` on an `(X, z)` grid
   (`model2d.py`, `validate_D2.py`).
   - 600 parameter points drawn as in the computation of `H`: no disagreement.
   - 300 points with `β > 2`: one disagreement. There the valley exceeds `L_S` by `2·10^{−4}`, below the flood fill's
     default `ε`; with `ε_rel = 5·10^{−4}` the flood fill agrees.
   - The referee's independent comparison (500 points, 40 of them (D′)-elder) agrees after resolving two numerical
     artifacts.
3. *The function `I`.*
   - A `101 × 121` table of `I(t, χ₀)` on `|t| ≤ 30`, `|χ₀| ≤ 2000` (`Itab2d_v2.py`), and an exact evaluator for other points
     (`Ifast.py`).
   - `I(t, 0)/|t|³ = 1.95, 1.51, 1.39` at `t = −10², −10³, −10⁴`, tending to `4/3`.
   - `I(0, χ₀)/χ₀² = 0.0228, 0.0212, 0.0209` at `χ₀ = 10³, 10⁴, 10⁵`, tending to `1/48`.
4. *The function `H`.* `H = H₀ + Δ_χ`.
   - `H₀`, the value with `C₃` ignored, comes from a 639-point table of `I(t, 0)` on `|t| ≤ 400`, its asymptotic forms beyond
     (`|t|³(4/3 + 5.74|t|^{−1/2})` and `t − 2/3`), and adaptive quadrature in `t` and `γ²` down to `γ → 0` (`Hk0b.py`). Its
     small-`k` values reproduce `(H₀ − 1)/k² → 12/25`, and it agrees with the referee's independent `H₀` to `3·10^{−5}`.
   - `Δ_χ` is the difference of two direct quadratures over `(|γ|, B, C₃)`, with and without `C₃` (`Hdirect4.py`). These use
     32 Gauss–Legendre nodes in `|γ|` on `[0, 7.5]` and 24 Gauss–Hermite nodes in `B` and in `C₃`, with the table inside its
     range and the exact evaluator outside it.
   - Accuracy checks: without the table, `Δ_χ(0.2)` changes by `2·10^{−5}`; with 48 nodes in `|γ|`, `H` changes by
     `5·10^{−5}`. For small `k`, `Δ_χ ≈ 62k⁴`. The quadrature `H` agrees with a table-free direct quadrature at `k = 0.2` to
     `1.3·10^{−4}`.
   - Values:

     | `k` | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 1.0 |
     |---|---|---|---|---|---|---|---|---|---|
     | `H₀` | 0.9976 | 0.9334 | 0.7403 | 0.4663 | 0.2268 | 0.0845 | 0.0241 | 0.0053 | 0.0001 |
     | `H` | 1.0039 | 1.0041 | 0.9345 | 0.7271 | 0.4397 | 0.2007 | 0.0687 | 0.0177 | 0.0005 |
     | `e^{−12k²}` | 0.887 | 0.619 | 0.340 | 0.147 | 0.050 | 0.013 | 0.003 | 0.0005 | 0.000006 |

5. *`R_{2/3}`.*
   - `Ĩ = −0.536` (`assemble2.py`; a dense trapezoid rule gives `−0.537`), so `R_{2/3} = 0.0914028·Ĩ = −0.049`.
   - Sensitivity: a uniform shift of `H` by `±0.002` on `k ≥ 0.1` moves `Ĩ` by `±0.018`. Halving the small-`k` term `62k⁴`
     moves it by `−0.021`, and multiplying it by `1.5` by `+0.021`. So `Ĩ = −0.54 ± 0.03` and `R_{2/3} = −0.049 ± 0.003`.
   - With `C₃` ignored (`H = H₀`), `Ĩ = −1.133` and `R_{2/3} = −0.104`. With the pin density alone (`H = e^{−12k²}`),
     `Ĩ = 12^{5/6}Γ(−5/6)/6 = −8.829` and `R_{2/3} = −0.807`. So the soft model's extra jets matter: `B` nearly cancels the pin
     density at small `k`, and `C₃` raises `H` at `k ≈ 0.2–0.7`.
6. *#216's Monte Carlo.* The raw `d = 2` records (`batchA2.npz`: 4,000 samples, 271,272 rejected adjacent pairs with `ℓ < 0.3`)
   were compared with the composite (`composite.py`, `comp2d.py`). #216's row counts *adjacent* rejected pairs, which carry no
   `B_{2,L}` (#218 Remark 3). By §4 (inputs (ii)–(iii), and the `ℓ^{3/4}` order), these totals do not test the global
   `ℓ^{2/3}` coefficient. What they do test, bin by bin in `s = r/ℓ^{1/4}`, is the fold-side suppression described by `H`.
   - *Small `s` (the fold side).* For `s < 0.8` and `ℓ ∈ [10^{−4}, 0.1)`, 37 pairs are observed, 35.3 predicted by the
     composite, and 4,322 by the cusp kernel alone. In the bin `ℓ ∈ [3·10^{−3}, 10^{−2})`, `s ∈ [0.6, 0.8)` the three numbers
     are 12, 13.1 and 143. For `s ∈ [0.8, 1)` they are 2,248, 1,904 and 7,766.
   - *`s ≥ 1` (the cusp side).* The composite and the cusp kernel agree. The data exceed both by up to 25% at `ℓ ≥ 10^{−2}`,
     which is not modelled here (finite-`r` cusp corrections, the `ℓ^{3/4}` order).
   - *Totals.* On `[10^{−4}, 10^{−2}]` the ratio of the counts to `(I^{cand} − c₁)ℓ^{1/4}` alone is `0.959 ± 0.017`; to the
     composite, `1.040`; to the two-term law with `R_{2/3} = −0.049`, `1.018`.

## 6. Scope and relation to other packets

- **#229 (R⁺.1).** It proves `ρ_rej = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} − ν_eld^{far,r_0^*} + O(ℓ^{3/7})`. Conjecture 7 would resolve
  its remainder in `d = 2`, given inputs (i)–(ii) of §4 (and (iii) to drop the far term). Theorem 1, Lemma 5 and Proposition 4 do not change any statement
  of #229.
- **#240 Remark 1.** It leaves the ends `κ → ∞` and `κ → 0` of Theorem N open. Theorem 1 describes the `κ → ∞` end of the
  *rejected* cusp kernel in `d = 2`: it decays like `1/κ`, while `𝒜^{cand}` and `𝒜^{eld}` grow like `κ²`. Lemma Q′'s margins do
  not reach the soft window `λ ≍ γ²/κ` where the rejected weight sits.
- **#237 Remark 4 and #240 Remark 4.** They found residuals of #216's Monte Carlo about the three-term laws that two-power
  fits could not attribute (`ℓ^{1/2}` against `ℓ^{2/3} + ℓ^{3/4}`). Conjecture 7 predicts a contribution `−R_{2/3}ℓ^{2/3}` to
  `ν_eld`, in addition to any `ℓ^{2/3}` term of `ν_cand`, with a coefficient computed independently of the Monte Carlo.
- **[C7-K] (K2)** bounds the fold-scale rejected weight by `O(r³/k)`. Formally (Conjecture 6) the bound is attained: the
  leading term of `r^{−2}A_r^{rej}` is `(r/k)F(k; b, u)`, and `F(k) → F₀ ≠ 0` as `k → 0` (Theorem 1).
- **Not claimed.**
  - Conjectures 6 and 7 are not proved. The values of `H` and `R_{2/3}` are numerical and not certified.
  - Nothing for `d ≥ 3`. There the soft direction is an eigenvector of a `(d − 1) × (d − 1)` matrix, and `F₀` needs the density
    of its smallest eigenvalue at `0`; the `1/κ` form of Theorem 1 is expected to persist.
  - Nothing about the candidate density's own `ℓ^{2/3}` term.
  - Lemma 2, Lemma 3 and Proposition 4 are statements about the limit model (2.1). Their transfer to the field is
    Conjecture 6.
  - The Gaussian-kernel statements are about the model case on `R²`.

## 7. Controls

`soft_check.py` uses the standard library and exact rationals, except S8 (fixed floating-point cases). Its output is
`RESULTS.json`.

| Control | Checks |
|---|---|
| S1 | Theorem 1: `69984/72⁴ = 1/384`; `∫_{1/3}^1(φ^{−4} − φ^{−2})dφ = 20/3`; `12·(20/3)/384 = 5/24`; `F₀ = 25π₀p_A(0 \| b)`; the soft window at `f₄ = 0` |
| S2 | the algebra of `G_k` at 60 random rational points: its derivatives (exact four-point stencils), pins, `det H_M = 6λ̃ + Y`, `det H_S = −6λ̃ + Y`, the normalization (both signs of `γ`), weight, measure and typed window |
| S3 | the Gaussian kernel's jet covariances from Hermite numbers: (0.3), and `a′ = 144/(2·6) = 12` |
| S4 | (3.3) as exact truncated series; the double zero at `t = 0`; the Jacobian `−96` |
| S5 | (3.4), and the antiderivative of the weight |
| S6 | `E[γ⁶] = 120`, `E[γ⁶t²] = 576k²`, `312/25`, `12/25`, and the moment identities of Proposition 4's proof |
| S7 | every numerical inequality of Lemma 3's proof, including the critical-value formulas as identities |
| S8 | Lemma 2 on 16 fixed parameter points with known answers, including case (D′), in floating point |
| S9 | the error exponents of Lemma 5 |
| S10 | the limit (2.1), including `G₁`, on three exactly pinned degree-6 fields with `A = −λ̃r/k`, at `r = 10^{−3}` and `10^{−4}` |

Mutants `M1`–`M10` each break exactly one control (`M1` S1, `M2` S3, `M3` S4, `M4` S5, `M5` S7, `M6` S8, `M7` S9, `M8` S2,
`M9` S6, `M10` S10); an unknown label exits 2.

## 8. Sources (exact identities in `SOURCES.json`)

| Tag | Path | Role |
|---|---|---|
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`) | (R5): Gaussian decay of the pin density — consumed |
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`) | §2 finite-jet rank, through #220 — consumed |
| [E1], [E2], [REC] | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md`, `reviews/d1_section9_borel_repair_20260925/REPAIR.md`, `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` | reading rules and the Borel elder mark, through #220 — consumed |
| #207 | `frontiers/cusp_second_order_20261001/PROOF.md` (blob `f6df5a73`) | §§0, 4, 6 (the cusp objects); Theorem CU.2(c) — consumed |
| #218 | `frontiers/candidate_third_order_20261001/PROOF.md` (blob `70ca57ef`) | §0: `𝒜^{cand}`, `I^{cand}`, `B_{d,L}`; Remark 3 — consumed |
| #220 | `frontiers/elder_third_order_20261001/PROOF.md` (blob `c8767dde`) | §0 ((0.1), (0.2)); §1 (window coordinates, (1.1), Lemma Q, (M1)–(M6)) — consumed |
| #229 | `frontiers/third_order_rate_20261001/PROOF.md` (blob `110ed33a`) | (R⁺.1); §0 (`Y_r`); §5 — consumed |
| [C7-K] | `frontiers/c7_total_bounded_20260929/PROOF.md` (blob `28748b08`) | (K2) — cited |
| #187 | `frontiers/far_elder_rate_20260930/PROOF.md` (blob `07260114`) | (0.2): `ν_eld^{far} ≤ Cℓ^{2/3}` — cited |
| #240 | `frontiers/elder_cusp_parity_20261002/PROOF.md` (open PR; blob `16a1db06`) | Lemma Q′, Step N6, Corollary N′, Remarks 1 and 4 — cited |
| #237 | `frontiers/candidate_parity_rate_20261001/PROOF.md` (open PR) | Theorem P's remainder, Remark 4 — cited |
| #216 | `frontiers/third_order_coefficient_20261001/NOTE.md` (open PR) | the full-field Monte Carlo (§5) — cited |
| #188 | far elder density `O(ℓ^N)` (open PR) | §4 (iii) — cited |

## 9. Review slices

- **A** (§1): Theorem 1, its proof and Remarks 1–3.
- **B** (§2): the limit field (2.1) and its monomial bookkeeping, the normalization, typing and weight, Lemma 2 (including case
  (D′)) and Lemma 3.
- **C** (§3): Proposition 4, namely the edge (3.3), the identification of the rejected set near `(0, 0)`, the series (3.4), the
  averaging and the bound off `𝒢`.
- **D** (§4): Lemma 5, and whether Conjectures 6 and 7 are stated precisely, with inputs (i)–(iii) complete and consistent with
  #187, #229 and #240.
- **E** (§§5–7): the evidence is described accurately and kept separate from the proofs, and the controls match their
  claims.
