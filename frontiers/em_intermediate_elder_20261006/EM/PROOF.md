# Lifetime note EM: the intermediate elder mass through a sheared box barrier, and the elder density with remainder `O(ℓ^{9/14})`

Object: `CL-EM-INTERMEDIATE-ELDER-20261006-v1`. Claim: main#229 6021554589.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 6 October 2026, for Dylan Roy (delegated AI
work). The same session wrote [N], #187, #198, #218, #220, #229, #237, #242–#244 and notes TL and TS. [182] and [R] are
OpenAI's.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph, STATUS,
PROOF_INDEX, prize or Boolean change; no numerical constant is certified. Same GitHub account as every lane;
organizational independence 0.

**What is new.**
- **Lemma S‴** (§4). For `0 < r ≤ r_*`, `b ∈ R`, `u ∈ S^{d−1}` and `0 < k ≤ r²` (that is, `κ ≤ r`),
  `E_Q[(W_r/r²)e] ≤ Cr²[rκ + r^{7/3}κ^{2/3}log(2/r) + min(r^{7/2}, r^{3/2}κ^{2/3})]P^N`.
  - On `κ ≤ r`, note TS's Lemma S″ gives `Cr²(κ + r)κ^{2/3}P^N ≤ 2Cr²·rκ^{2/3}P^N`. Against `rκ^{2/3}`, the three terms gain
    `κ^{1/3}`, `r^{4/3}log(2/r)` and `r^{1/2}`.
  - The proof splits by `λ`, the least eigenvalue of `−A`, the transverse Hessian at the midpoint of the pins.
  - On the good event `𝒢 = {A < 0, λ ≥ C_G𝒩r}`, Lemma X (§2) applies: a barrier on a box, in window coordinates sheared by
    the exact Schur direction at `M̂`.
    - Along that direction the cubic coefficient is `12κ − z/2 + O(𝒩̄^{5/2}rλ^{−3/2})`, and on typed pairs [N]'s Lemma Q′
      gives `|z| < 72κ + O(𝒩̄²r/λ)`. The faces of the box across the shear need only the transverse curvature `μ`.
    - So on `𝒢` an elder pair has soft curvature `s ≲ κ + 𝒩̄(κ/μ)^{1/2} + κ^{1/3}(κ + 𝒩̄^{5/2}rμ^{−3/2})^{2/3}`. Lemma S″'s
      isotropic barrier bounds only the least eigenvalue of `−H̃`, by `C₆𝒩^{2/3}κ^{1/3}`.
  - Off `𝒢`, `M` has a soft transverse direction. Lemma S″'s barrier is combined with Lemma V (§3), a small-ball estimate
    for the Gaussian rescaled Hessian (#220 Lemma H): a transverse eigenvalue below `t` costs `t^{3/2}`, and `t^{1/2}`
    beside a soft eigenvalue below `ε`.
- **Corollary EM** (§5). As `ℓ ↓ 0`, `ν_eld(ℓ) = cℓ^{−1/3} + c₁ℓ^{1/4} + c₂ℓ^{1/3} + O(ℓ^{9/14})` and
  `ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + O(ℓ^{3/5})`. For SIDE24 the relative remainder is `O(ℓ^{41/42})`.
  - This improves note TS's `ℓ^{4/7}log(1/ℓ)`.
  - The elder density now has a smaller proven remainder than the candidate density, whose remainder is #237's `ℓ^{3/5}`.
    `ρ_rej` reaches that `ℓ^{3/5}`.
  - In TS's decomposition at `ρ = ℓ^{3/14}`, three ledger rows sit at `9/14`. Two of them belong to the decomposition and
    not to the new lemma (Remark 1).

**Not claimed.**
- No sharpness of `9/14`, and none of any term of Lemma S‴.
- Nothing pointwise in `b`, and no identification of further terms of either density.
- No certified numerical value, and no uniformity in `d` or `L`.
- Nothing beyond the existential scope of the consumed packets and notes. Corollary TS′ (no `ℓ^{1/2}` term) is unchanged and
  is not re-argued here. Whether IBA2-009 closes is for the audit's owners.

**Consumed.**
- Note TS, main#229 6020794123, to be read with its successor text 6021299833. It is read in every slice, with readback
  PASS 6021301151; its custody packet is Math-#387. Used here:
  - §0 (notation; `𝓐^*`, `𝐓_r^*`, the jets) and §1's constant `C₀`;
  - Lemma S″'s (S″.2): on `[r_*, r_0^*]` in §5, and for the comparison in the header;
  - §1 as amended: the barrier (1.3), and from Step 4 the typed bound `|det K_S| ≤ Cr(κ + r)𝒩^{N₃}` and the layer argument;
  - §5: the decomposition (5.1), the bounds of each term, and the ledger, with the inputs those bounds consume (note TL's
    decomposition and Corollary TL1, #237 Lemmas U and K, #242 §0, #218 (0.1), (5.0), and Theorem TL⁻ at `θ = 2/3`).
- [N] = #240 `frontiers/elder_cusp_parity_20261002/PROOF.md` (blob `16a1db06`): §0 (the jets and (0.1)); §1: the window
  coordinates, the cusp polynomial `𝔓`, and Lemma Q′ under (Q′1)–(Q′2) only. From its statement: the ridge, with (1.2′)
  and (1.3′) for `ε₂`. From its proof, at `X = ±½`: Step Q1 (`∂_Ξ²𝔉 ≤ −(λ/2)I` on the window), Step Q2′ (`g_𝔉″` is the
  Schur complement of `∂_Ξ²𝔉` in `Hess 𝔉`) and Step Q4 (the pin values).
- #220 `frontiers/elder_third_order_20261001/PROOF.md` (blob `c8767dde`): §0 (`W_r/r² = F_d(K_M)F_{d−1}(K_S)`), §1 (the norm
  convention and `r_Q`), and Lemma H (a)–(b).
- [R] `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`): §4 (`|det K_i| = |det H_i|/r`) and (R5).
- [182] `frontiers/fixed_r_inverse_lifetime_20260930/PROOF.md` (blob `0d401877`): the maximin death level (2).
- #229 `frontiers/third_order_rate_20261001/PROOF.md` (blob `110ed33a`): Proposition W⁺, (W⁺.2).
- #237 `frontiers/candidate_parity_rate_20261001/PROOF.md` (blob `a97bf528`): Theorem P, (P.1).
- #187 `frontiers/far_elder_rate_20260930/PROOF.md` (blob `07260114`): the far bound `0 ≤ ν_eld^{far,r_0^*} ≤ Cℓ^{2/3}`.

**Cited only.** #218 `frontiers/candidate_third_order_20261001/PROOF.md` (blob `70ca57ef`), Lemma D. (V.3) below is its first
bound applied to the block `K`, re-proved in §3 with the same eigenvalue coordinates.

**Prior work and overlap.** This lane's rule requires a search before drafting. I searched the tree of `main`, the project
archive, and main#229 and main#259 since note TS's delivery.
- No packet or claim bounds the elder kernel below Lemma S″ on `κ ≤ r`.
- None has a joint small-ball estimate like (V.1)–(V.2), which couple the least eigenvalue of a principal block with that
  of the whole matrix. The nearest are #218 Lemma D (one small eigenvalue) and #237 Lemmas D′ and D″ (§3: the bounded
  density of `det G`, and two small eigenvalues of one matrix at cost `ε²`).
- Note TS Remark 1 recorded a formal refinement that needed a `C³` bound on [N]'s ridge, and did not attempt it.
- Lemma X needs no `C³` bound on the ridge. It uses a box in sheared coordinates, whose transverse faces need only `μ`. The
  ridge enters Lemma S‴ only through Lemma Q′'s `C²` control at `X = ±½`, in the typed window (4.1).
- What it gives is weaker than TS Remark 1's formal `r^{7/3}κ^{2/3}`: on `𝒢` it adds `rκ`, which costs only a logarithm
  after integration, and off `𝒢` it stops at `min(r^{7/2}, r^{3/2}κ^{2/3})`. Even so, it moves the elder remainder to `9/14`.

## 0. Setting and statements

Setting and notation are note TS's (§0), with its §1 constant: `𝒩 = 𝒩_r = 1 + k + ‖F_r‖_{C⁹}`, and `C₀ = C₀(d) ≥ 1` such that
every derivative of `f = F_r` of order `≤ 9` along unit vectors is at most `C₀𝒩`, and every gradient of such a derivative of
order `≤ 8` is at most `C₀𝒩` in norm. Put `𝒩̄ := C₀𝒩`. Then `𝒩̄ ≥ max(1, ‖f‖_{C⁵})` in #220 §1's operator-norm convention,
so [N]'s Lemma Q′ applies with `𝒩̄` in place of its `𝒩`. Constants `C, c, N` depend only on `d` and `L` and may change from
line to line. `P = 1 + |b| + k`, `m = d − 1`, and `M = −ru/2`, `S = ru/2` are the pins, with `f(M) = b` and
`f(S) = b − kr³ = b − κr⁴`.

*Window coordinates* ([N] §1). `Φ(X, Ξ) = rXu + r²ΘΞ`, `𝔉 = r^{−4}(f∘Φ − b)`, `M̂ = (−½, 0)`, `Ŝ = (½, 0)`. The chain rule
gives `∂_X^a∂_Ξ^β𝔉 = r^{a + 2|β| − 4}(∂_u^a∂_Θ^βf)∘Φ`. [N]'s cusp polynomial is
`𝔓(X, Ξ) = 2κ(X + ½)²(X − 1) + (f₄/24)(X² − ¼)² + ½(X² − ¼)γ·Ξ + ½ΞᵀAΞ`.

*Jets at `0`* ([N] §0). These are `A = D_Θ²f(0)`, `γ = ∂_u²∇_Θf(0)` and `f₄ = ∂_u⁴f(0)`. On `{A < 0}` put
`λ := λ_min(−A)`, `Γ̃ := |A^{−1}γ|`, `q := γᵀA^{−1}γ`, `z := f₄ − 3q` and `φ := z/(72κ)`.

*The Hessian at `M` in window coordinates* (note TS §1, #220 Lemma H). It is
`H̃ = D²𝔉(M̂) = [[ã, β̃ᵀ], [β̃, D]]`, with `ã = r^{−2}∂_u²f(M)`, `β̃ = r^{−1}∂_u∇_Θf(M)` and `D = D_Θ²f(M)`.
- On `{D < 0}` put `μ := λ_min(−D)` and `s := β̃ᵀD^{−1}β̃ − ã`, which is minus the Schur complement of `D` in `H̃`.
- On `{H̃ < 0}`, `s > 0` and `|det H̃| = s|det D|`.
- At `S`: `H̃_S = D²𝔉(Ŝ)`, its `Θ`-block `D_S = D_Θ²f(S)`, and `s_S := ã_S − β̃_SᵀD_S^{−1}β̃_S`, the Schur complement of `D_S`
  in `H̃_S` (not minus it; `s_S > 0` at a typed `S` with `D_S < 0`).

*The good event.* `𝒢 := {A < 0, λ ≥ C_G𝒩r}`, with `C_G = C_G(d, L)` fixed in §4.1.

**Lemma P (third-order pin relations at `M`).** Let `f` satisfy the derivative bounds above, have the pins
(`∇f(M) = ∇f(S) = 0`, `f(M) − f(S) = kr³`), and let `0 < r ≤ 1`. Then

    |∂_u³f(0) − 12k| ≤ (3/80)C₀𝒩r²,        |r^{−1}∂_u³f(M) − 12κ + f₄/2| ≤ (13/80)C₀𝒩r,                         (P.1–2)
    |β̃ + γ/2| ≤ (5/12)C₀𝒩r,        ‖D − A‖, ‖D_S − A‖ ≤ ½C₀𝒩r,        |∂_u²∇_Θf(M) − γ| ≤ ½C₀𝒩r.                     (P.3–4)

So `E := 𝔉 − 𝔓` satisfies `|D³E(M̂)[(v_X, w)^{⊗3}]| ≤ C₀𝒩r(|v_X| + |w|)³` for all `v_X ∈ R` and `w ∈ R^{d−1}`.

**Lemma X (the sheared box).** This lemma is deterministic.
- *Setting.* `f ∈ C⁴(X)`, and `𝒩̄ > 0` is a number such that every derivative of `f` of order 3 at `M`, and of order 4
  everywhere, along unit vectors is at most `𝒩̄` (for `f = F_r`, §0's `𝒩̄ = C₀𝒩` qualifies). `M̂` is a critical point of `𝔉`
  with `𝔉(M̂) = 0`, `f(S) = b − κr⁴` with `κ > 0`, and `H̃ < 0`.
- *Notation.* Put `τ := −D^{−1}β̃` and `α := D³𝔉(M̂)[(1, τ)^{⊗3}]`, and let `T ≥ |α|`.
- *Hypotheses.* Assume
  - `r|τ| ≤ 1` and `r + 2r²(κ/μ)^{1/2} ≤ L/4`;
  - `μ³ ≥ (256/9)𝒩̄²r⁴κ` and `μ² ≥ (64/3)𝒩̄r⁴κ`.
- *Conclusion.* If

      s ≥ max{ ((256/9)κT²)^{1/3},  ((1024/3)𝒩̄κ)^{1/2},  64𝒩̄(κ/μ)^{1/2},  1024𝒩̄²r²κ/μ²,  16κ },                     (X.0)

  then `d_f(M) ≤ b − (5/4)κr⁴ < f(S)`. In particular `e = 0`.

**Lemma V (small balls in `Sym(d)`).** Let `Y` be a Gaussian random element of `Sym(d)` with `c_V·I ≤ Cov(Y) ≤ C_V·I` and
`|EY| ≤ m₀`. Write `−Y = [[a, yᵀ], [y, K]]` in a fixed orthonormal frame, with `K ∈ Sym(m)`, and put `λ₁ := λ_min(−Y)`. For
each `n ≥ 0` there are `C_n` and `N` (depending on `d`, `c_V`, `C_V` and `n`) such that for all `ε, t, x > 0`

    E[(1 + ‖Y‖)^n λ₁ 1{Y < 0, λ₁ ≤ ε, λ_min(K) ≤ t}] ≤ C_n(1 + m₀)^N ε² t^{1/2},                                       (V.1)
    E[(1 + ‖Y‖)^n λ₁ 1{Y < 0, λ_min(K) ≤ t}] ≤ C_n(1 + m₀)^N t^{5/2},                                                   (V.2)
    E[(1 + ‖Y‖)^n 1{K > 0, x ≤ λ_min(K) ≤ 2x}] ≤ C_n(1 + m₀)^N x.                                                      (V.3)

**Lemma S‴ (the elder weight on `κ ≤ r`).** There are `r_* > 0` and `C, N` such that for `0 < r ≤ r_*`, `b ∈ R`,
`u ∈ S^{d−1}` and `0 < k ≤ r²`,

    E_Q[(W_r/r²) e] ≤ C r² [ rκ + r^{7/3}κ^{2/3}log(2/r) + min(r^{7/2}, r^{3/2}κ^{2/3}) ] P^N,                          (S‴.1)
    0 ≤ 𝐓_r^{eld}(k, u) ≤ C [ rκ + r^{7/3}κ^{2/3}log(2/r) + min(r^{7/2}, r^{3/2}κ^{2/3}) ].                              (S‴.2)

**Corollary EM (the elder and rejected densities).** As `ℓ ↓ 0`,

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{9/14}),                                                      (EM.1)
    ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁) ℓ^{1/4} + O(ℓ^{3/5}).                                                          (EM.2)

For the SIDE24 law (`d = 3`, `L = 24`):
`ν_{3,24}(ℓ) = cℓ^{−1/3}(1 + (c₁/c)ℓ^{7/12} + (c₂/c)ℓ^{2/3} + O(ℓ^{41/42}))`, with `c = c_{3,24}`, against TS's
`O(ℓ^{19/21}log(1/ℓ))`.

## 1. Proof of Lemma P

Put `h := r/2`, `p(x) := f(xu)` and `ψ(x) := ∇_Θf(xu)` for `|x| ≤ h`. The pins give `p′(±h) = 0`, `p(−h) − p(h) = 8kh³` and
`ψ(±h) = 0`. Also `|p⁽⁵⁾| ≤ C₀𝒩` and `|ψ‴| ≤ C₀𝒩`, so `|ψ″(x) − ψ″(0)| ≤ |x|C₀𝒩`; and `ψ″(0) = γ`.

- *(P.1).* Taylor's formula at `0`, with integral remainder:
  - `p′(±h) = p′(0) ± hp″(0) + (h²/2)p‴(0) ± (h³/6)p⁗(0) + R₁(±h)`, with `|R₁| ≤ (h⁴/24)C₀𝒩`;
  - `p(±h) = p(0) ± hp′(0) + (h²/2)p″(0) ± (h³/6)p‴(0) + (h⁴/24)p⁗(0) + R₀(±h)`, with `|R₀| ≤ (h⁵/120)C₀𝒩`.

  The sum of the first pair gives `2p′(0) = −h²p‴(0) − R₁(h) − R₁(−h)`. Put this into
  `8kh³ = p(−h) − p(h) = −2hp′(0) − (h³/3)p‴(0) + R₀(−h) − R₀(h)`. That gives
  `8kh³ = (2/3)h³p‴(0) + h(R₁(h) + R₁(−h)) + R₀(−h) − R₀(h)`, so

      |p‴(0) − 12k| ≤ (3/(2h³))(2h⁵/24 + 2h⁵/120)C₀𝒩 = (3/20)h²C₀𝒩 = (3/80)r²C₀𝒩.

  On quintic profiles (constant `p⁽⁵⁾`) the error is `(r²/40)|p⁽⁵⁾|` exactly (control E1).
- *(P.2).* `p‴(−h) = p‴(0) − hp⁗(0) + R₂` with `|R₂| ≤ (h²/2)C₀𝒩`. Since `h/r = ½`, `r^{−1}∂_u³f(M) − 12κ + f₄/2` equals
  `r^{−1}(p‴(0) − 12k) + r^{−1}R₂`. So it is at most `(3/80 + 1/8)rC₀𝒩 = (13/80)C₀𝒩r`. On quintic profiles it is
  `(r/10)|p⁽⁵⁾|` exactly.
- *(P.3).* Taylor at `−h` gives `0 = ψ(h) = ψ(−h) + 2hψ′(−h) + 2h²ψ″(−h) + R₃`, with `|R₃| ≤ ((2h)³/6)C₀𝒩`. So
  `β̃ = r^{−1}ψ′(−h) = −½ψ″(−h) − R₃/(2hr)`, and

      |β̃ + γ/2| ≤ ½|ψ″(−h) − γ| + (4h³/3)C₀𝒩/(4h²) ≤ (h/2 + h/3)C₀𝒩 = (5/12)C₀𝒩r.

- *(P.4).* These are mean-value bounds along the segments from `0` to `M` and to `S`, each of length `h`.
- *`D³E(M̂)`.* `𝔓`'s third derivatives are `∂_X³𝔓 = 12κ + f₄X` and `∂_X²∂_Ξ𝔓 = γ`; the others vanish. So at `M̂`:
  - the `(3, 0)` entry of `D³E` is `r^{−1}∂_u³f(M) − (12κ − f₄/2)`, at most `(13/80)C₀𝒩r` by (P.2);
  - the `(2, 1)` entry is `∂_u²∇_Θf(M) − γ`, at most `½C₀𝒩r` by (P.4);
  - the `(1, 2)` entry is `r∂_u∂_Θ²f(M)`, at most `C₀𝒩r`;
  - the `(0, 3)` entry is `r²∂_Θ³f(M)`, at most `C₀𝒩r²`.

  Hence `|D³E(M̂)[(v_X, w)^{⊗3}]| ≤ C₀𝒩r((13/80)|v_X|³ + (3/2)|v_X|²|w| + 3|v_X||w|² + r|w|³) ≤ C₀𝒩r(|v_X| + |w|)³`. ∎

## 2. Proof of Lemma X

*Step 1 (the shear).* Put `Ψ(t, ζ) := M̂ + (t, τt + ζ)` for `t ∈ R` and `ζ ∈ R^{d−1}`, and `𝔊 := 𝔉∘Ψ`. `Ψ` is affine with
`DΨ = J := [[1, 0], [τ, I]]` and `det J = 1`. So `𝔊(0) = 0` and `∇𝔊(0) = 0`. Since the block `D` satisfies `Dτ = −β̃`,

    D²𝔊(0) = JᵀH̃J = [[ã + 2β̃·τ + τᵀDτ, (β̃ + Dτ)ᵀ], [β̃ + Dτ, D]] = diag(−s, D)                                        (2.1)

(control E2). `D ≤ −μI`, and `s > 0` because `H̃ < 0`.

*Step 2 (Taylor bounds).* Since `Ψ` is affine, `D^j𝔊(w)[v^{⊗j}] = D^j𝔉(Ψ(w))[(Jv)^{⊗j}]`, and
`D^j𝔉(x)[v^{⊗j}] = r^{−4}D^jf(Φ(x))[(DΦv)^{⊗j}]` with `DΦ(v_X, v_Ξ) = rv_Xu + r²Θv_Ξ`.
- *The fourth derivatives.* So `|D⁴𝔉(x)[(v_X, v_Ξ)^{⊗4}]| ≤ 𝒩̄(|v_X| + r|v_Ξ|)⁴` everywhere.
- *The quartic remainder.* For `w = (t, ζ)`, `Jw = (t, τt + ζ)`. With `r|τ| ≤ 1` and `(x + y)⁴ ≤ 8(x⁴ + y⁴)`, the Taylor
  remainder `R₄(w)` of order four satisfies
  `|R₄(w)| ≤ (𝒩̄/24)(2|t| + r|ζ|)⁴ ≤ (𝒩̄/3)(16t⁴ + r⁴|ζ|⁴)`.
- *The cubic term.* Put `V := (1, τ)` and `Z := (0, ζ)`. Then
  `D³𝔊(0)[w^{⊗3}] = αt³ + 3t²D³𝔉(M̂)[V, V, Z] + 3tD³𝔉(M̂)[V, Z, Z] + D³𝔉(M̂)[Z^{⊗3}]`. Since `|DΦV| ≤ r(1 + r|τ|) ≤ 2r`
  and `|DΦZ| = r²|ζ|`, the third-derivative bound at `M` gives:
  - `|D³𝔉(M̂)[V, V, Z]| ≤ 𝒩̄(1 + r|τ|)²|ζ| ≤ 4𝒩̄|ζ|`;
  - `|D³𝔉(M̂)[V, Z, Z]| ≤ 𝒩̄r(1 + r|τ|)|ζ|² ≤ 2𝒩̄r|ζ|²`;
  - `|D³𝔉(M̂)[Z^{⊗3}]| ≤ 𝒩̄r²|ζ|³`.

Hence, for all `t` and `ζ`,

    𝔊(t, ζ) ≤ −½st² − ½μ|ζ|² + (T/6)|t|³ + 2𝒩̄t²|ζ| + 𝒩̄r|t||ζ|² + (𝒩̄r²/6)|ζ|³ + (16𝒩̄/3)t⁴ + (𝒩̄r⁴/3)|ζ|⁴.        (2.2)

*Step 3 (the box).* Put `δ_t := 2(κ/s)^{1/2}`, `δ_ζ := 2(κ/μ)^{1/2}` and `𝒬 := {|t| ≤ δ_t, |ζ| ≤ δ_ζ}`. Since
`s, μ, κ, 𝒩̄ > 0` and `T ≥ 0`, (X.0) and the two hypotheses on `μ` are together equivalent to the following seven conditions
(control E4 checks the direction used, from (X.0) and the hypotheses to (a)–(g)):

    (a) (T/6)δ_t ≤ s/16 ⟺ s³ ≥ (256/9)κT²;            (b) (16𝒩̄/3)δ_t² ≤ s/16 ⟺ s² ≥ (1024/3)𝒩̄κ;
    (c) 2𝒩̄δ_ζ ≤ s/16 ⟺ s ≥ 64𝒩̄(κ/μ)^{1/2};          (d) 𝒩̄rδ_t ≤ μ/16 ⟺ s ≥ 1024𝒩̄²r²κ/μ²;
    (e) (𝒩̄r²/6)δ_ζ ≤ μ/16 ⟺ μ³ ≥ (256/9)𝒩̄²r⁴κ;       (f) (𝒩̄r⁴/3)δ_ζ² ≤ μ/16 ⟺ μ² ≥ (64/3)𝒩̄r⁴κ;
    (g) δ_t ≤ ½ ⟺ s ≥ 16κ.

By (a)–(c), on `𝒬` the error terms `(T/6)|t|³`, `(16𝒩̄/3)t⁴` and `2𝒩̄t²|ζ|` of (2.2) are each at most `(s/16)t²`; by
(d)–(f), the error terms `𝒩̄r|t||ζ|²`, `(𝒩̄r²/6)|ζ|³` and `(𝒩̄r⁴/3)|ζ|⁴` are each at most `(μ/16)|ζ|²`. So

    𝔊 ≤ −(5/16)(st² + μ|ζ|²) ≤ 0 on 𝒬.                                                                                   (2.3)

On the faces `|t| = δ_t`, `𝔊 ≤ −(5/16)sδ_t² = −(5/4)κ`. On the faces `|ζ| = δ_ζ`, `𝔊 ≤ −(5/16)μδ_ζ² = −(5/4)κ`.

*Step 4 (the maximin level).* Put `𝓔 := π(Φ(Ψ(𝒬)))`, with `π: R^d → X` the projection.
- `Φ∘Ψ` is affine and injective. By (g) and `r|τ| ≤ 1`, a point of `Φ(Ψ(𝒬))` satisfies
  `|Φ(Ψ(t, ζ)) − M| ≤ r|t| + r²|τt + ζ| ≤ r(1 + r|τ|)δ_t + r²δ_ζ ≤ r + 2r²(κ/μ)^{1/2} ≤ L/4 < L/2`, and `π` is injective
  and open on `B(M, L/2)`.
- So `𝓔` is an embedded closed topological ball. Its interior contains `M`, and its boundary is `π(Φ(Ψ(∂𝒬)))`.
- By (2.3), `f ≤ b` on `𝓔`, and `f ≤ b − (5/4)κr⁴` on its boundary.
- Every continuous path from `M` to a point where `f > b` leaves `𝓔`, so it crosses the boundary.

By the maximin characterization ([182] (2)), `d_f(M) ≤ b − (5/4)κr⁴ < b − κr⁴ = f(S)`, and `e = 0`. ∎

Lemma X needs no more than this: `M̂` is critical with value `0`, the gap is `κ`, and `H̃ < 0`. The pins enter in §4,
through the structure of `α` and the typed window.

## 3. Proof of Lemma V

Use the coordinates `(a, y, K) ∈ R × R^m × Sym(m)` of `−Y`, the entries on and above the diagonal, and take Lebesgue measure
on `Sym(d)` in them. For `R ≥ 1` put `B_R := {|Y| ≤ R}` (Frobenius norm); on `B_R`, `|a|, |y|, ‖K‖ ≤ R`. Let
`μ₁ ≤ … ≤ μ_m` be the eigenvalues of `K`, with orthonormal eigenvectors `v_i`, and put `β_i := y·v_i`.

*Three Lebesgue estimates.*
- *(L0)* For every `x > 0`, `Leb{K ∈ Sym(m): ‖K‖ ≤ R, K > 0, x ≤ μ₁ ≤ 2x} ≤ CR^N x`. Weyl's change of variables to
  eigenvalues and an eigenframe has Jacobian `c_m∏_{i<j}|μ_i − μ_j| ≤ c_m(2R)^{m(m−1)/2}`, and in the eigenvalue variables
  the set has measure at most `x(2R)^{m−1}`. (For `m = 1` it is an interval of length at most `x`.)
- *(L1)* On `B_R ∩ {Y < 0}`, `K > 0` and `a > yᵀK^{−1}y = Σ_iβ_i²/μ_i`, because the Schur complement of `K` in `−Y` is
  positive. As `a ≤ R`, `β_i² < Rμ_i` for every `i`.
- *(L2) The secular equation.* Fix `(y, K)` with `K > 0`. For `0 ≤ λ < μ₁`,
  `det(−Y − λI) = det(K − λI)(a − a(λ))` with `a(λ) := λ + Σ_iβ_i²/(μ_i − λ)`, and `a(·)` is increasing. With `K − λI > 0`,
  `−Y − λI > 0` exactly when `a > a(λ)` (Sylvester's criterion, `K` first). So:
  - `Y < 0` exactly when `a > a(0)`; and for `0 < ε < μ₁`, `{Y < 0, λ₁ ≤ ε}` is the `a`-interval `(a(0), a(ε)]`;
  - if `2ε ≤ μ₁`, then `a(ε) − a(0) = ε + εΣ_iβ_i²/(μ_i(μ_i − ε)) ≤ ε(1 + 2Σ_iβ_i²/μ_i²) ≤ ε(1 + 2mR/μ₁)`, by (L1);
  - if `μ₁ < 2ε`, the `a`-range has length at most `2R`.

  Control E5 checks the factorization, the interval characterization, the bound on `a(ε) − a(0)` and (L1) exactly.

*(V.1) on `B_R`.* Split `{μ₁ ≤ t}` into the dyadic shells `μ₁ ∈ (x, 2x]`, `x = 2^{−i−1}t`, `i ≥ 0`; shells with `x ≥ R` are
empty. In each shell the `K`-measure is at most `CR^Nx`, by (L0). Given `K`, the map `y ↦ (β_i)` is orthogonal, and by (L1)
only `β₁` is confined, to `|β₁| < (2Rx)^{1/2}`; so the `y`-measure is at most `2(2Rx)^{1/2}(2R)^{m−1}`.
- *Shells with `x ≥ 2ε`.* There `μ₁ > 2ε`, so the `a`-length is at most `ε(1 + 2mR/x) ≤ (1 + 2m)εR/x`, as `x ≤ R`. The shell
  has measure at most `CR^{N′}εx^{1/2}`. Over the dyadic `x ≤ t` these sum to at most `CR^{N′}εt^{1/2}`, since
  `Σ_{i≥0}2^{−i/2} ≤ 4`.
- *Shells with `x < 2ε`.* The `a`-length is at most `2R`, and the shell has measure at most `CR^{N′}x^{3/2}`. Over the
  dyadic `x < min(2ε, t)` these sum to at most `CR^{N′}min(2ε, t)^{3/2} ≤ 2CR^{N′}εt^{1/2}`.

So `Leb(B_R ∩ {Y < 0, λ₁ ≤ ε, μ₁ ≤ t}) ≤ CR^{N′}εt^{1/2}`. On this set `(1 + ‖Y‖)^nλ₁ ≤ (2R)^nε`, which gives one more
factor `ε`.

*(V.2) on `B_R`.* The same shells without the `a`-constraint have measure at most `CR^{N′}x^{3/2}`. By Cauchy interlacing,
`λ₁ = λ_min(−Y) ≤ λ_min(K) = μ₁ ≤ 2x` on the shell. The weighted shells sum to at most `CR^{N′+n}Σ_x x^{5/2} ≤ CR^{N′+n}t^{5/2}`.

*(V.3) on `B_R`* is (L0) times the `(a, y)`-measure `(2R)^{1+m}`, times `(2R)^n`.

*From Lebesgue measure to the Gaussian law.* In these coordinates `Y` has a density at most `C_*exp(−c_*|Y − EY|²)`, with
`c_*, C_*` depending only on `d`, `c_V` and `C_V`. Put `S_0 := {|Y − EY| < 1}` and `S_j := {2^{j−1} ≤ |Y − EY| < 2^j}` for
`j ≥ 1`. On `S_j`, `|Y| ≤ m₀ + 2^j =: R_j ≤ (1 + m₀)2^j`, and the density is at most `C_*e^{−c_*4^{j−1}}` for `j ≥ 1` (and
`C_*` on `S_0`). Each left side of (V.1)–(V.3) is at most `Σ_j(density bound on S_j) × (the B_{R_j} bound)`, with
`R_j^{N″} ≤ (1 + m₀)^{N″}2^{jN″}`, and the series converges. ∎

The exponents of the Lebesgue estimates appear to be attained. In a Monte Carlo with `−Y = I + GOE` (exploration,
Remark 4), `P(Y < 0, μ₁ ≤ t)/t^{3/2}` stays nearly constant over `t ∈ [0.025, 0.2]`, and
`P(Y < 0, λ₁ ≤ ε, μ₁ ≤ t)/(εt^{1/2})` over six pairs with `t ∈ [0.0125, 0.2]` and `ε ∈ [0.005, 0.02]`.

## 4. Proof of Lemma S‴

Take `r_* ≤ min(r_0^*, r_Q)` (`r_0^*` of #220; `r_Q ≤ 1/10` of #220 §1, as in [N] §1), small enough for the finitely many
conditions below. Fix `0 < r ≤ r_*`, `b`, `u` and `0 < k ≤ r²`, and let `f = F_r` under `Q`; so `κ ≤ r ≤ 1/10`.
`W_r > 0` means that the pair is typed (`H_M < 0` and `H_S` has index `m`), so `H̃ < 0`. Split `{W_r > 0}` into
`𝒢 ∩ {W_r > 0}` and the rest, `ℬ`.

### 4.1 The good region `𝒢`

*(a) Lemma Q′ applies.* On `𝒢`, `Γ̃ ≤ |γ|/λ ≤ 𝒩̄/λ ≤ C₀/(C_Gr)`. With this crude bound, (Q′1)–(Q′2) hold with `𝒩̄` once
`C_G` is large and `r ≤ r_*`. With [N]'s `M̃ = (35/8)Γ̃` and `R′ = 5M̃ + 4 + 3((κ + 1)/λ)^{1/2}`, it suffices that:
- `2C₁𝒩̄r ≤ λ`, `3𝒩̄r ≤ λ/4`, `5r(1 + M̃) ≤ 1` and `𝒩̄r²R′ ≤ λ/4`;
- `6r + 2r²R′ ≤ L/4`, where `R′ ≤ (175/8)𝒩̄/λ + 4 + 3√2λ^{−1/2}`.

Each holds for `C_G ≥ C(d)C₀(1 + C₁)` and small `r`. Fix `C_G := max(C(d)C₀(1 + C₁), 3520C₀C₁, 64C₀)`. Then on `𝒢` also
`λ ≥ 3520C₁𝒩̄r`, used in (4.2), and `λ ≥ 64C₀𝒩r`, used in (c)–(e). Lemma Q′ ((1.2′)–(1.3′)), with Steps Q1, Q2′ and Q4 of
its proof in [N] §1, gives the following.
- `Ξ_𝔉(±½) = 0`, since `M̂` and `Ŝ` are critical and `𝔉(±½, ·)` is strictly concave on `{|Ξ| ≤ R′}`. So the ridge's
  second derivatives at `X = ±½` are the Schur complements of `∂_Ξ²𝔉` in `Hess𝔉` at `M̂` and `Ŝ`:
  `g_𝔉″(−½) = −s` and `g_𝔉″(½) = s_S`.
- With [N]'s ridge error `h := g_𝔉 − g` (not §1's `h = r/2`), `|h″| ≤ ε₂ ≤ ε̃ := 220C₁𝒩̄r(1 + Γ̃)²`, where
  `g″(∓½) = ∓6κ(1 ∓ φ)` (control E3).
- `∂_Ξ²𝔉 ≤ −(λ/2)I` on the window. In particular `D_S ≤ −(λ/2)I` (which also follows from (P.4) and Weyl's inequality).

*(b) The typed window.* `H_M < 0` gives `s > 0`. `H_S` has index `m` while `D_S < 0`, so its Schur complement is positive:
`s_S > 0`. Hence `6κ(1 − φ) = s + h″(−½) > −ε₂` and `6κ(1 + φ) = s_S − h″(½) > −ε₂`. So

    |z| < 72κ + 12ε̃,        s + s_S = 12κ + h″(½) − h″(−½) ≤ 12κ + 2ε̃.                                                    (4.1)

Next, `|q| = |f₄ − z|/3 ≤ (𝒩̄ + 72κ + 12ε̃)/3`, and `Γ̃² = γᵀA^{−2}γ ≤ |q|/λ`. With `ε̃ ≤ 440C₁𝒩̄r(1 + Γ̃²)` and
`λ ≥ 3520C₁𝒩̄r`, this gives

    Γ̃² ≤ C_Γ𝒩̄/λ,        C_Γ := (2/3)(73 + 5280C₁),        so        ε̃ ≤ C𝒩̄²r/λ                                    (4.2)

(control E7; `κ ≤ 1 ≤ 𝒩̄`, and `1 ≤ 𝒩̄/λ` because `λ ≤ ‖A‖ ≤ 𝒩̄`).

*(c) The cubic coefficient along the shear.* Write `δτ := τ − ½A^{−1}γ`. `𝔓`'s third derivatives at `M̂` along `V = (1, τ)`
give `D³𝔓(M̂)[V^{⊗3}] = 12κ − f₄/2 + 3γ·τ` (control E3). With `3γ·½A^{−1}γ = (3/2)q`,

    α = 12κ − z/2 + 3γ·δτ + D³E(M̂)[V^{⊗3}].                                                                              (4.3)

- *The shift `δτ`.* `μ ≥ λ − ½C₀𝒩r ≥ λ/2` by (P.4) and Weyl's inequality. By (P.3)–(P.4),
  `δτ = ½D^{−1}(A − D)A^{−1}γ − D^{−1}(β̃ + γ/2)`, so `|δτ| ≤ (C₀𝒩r/μ)(Γ̃/4 + 5/12) ≤ Γ̃/4 + ½`, as `μ ≥ C₀𝒩r`. Then
  `|τ| ≤ Γ̃/2 + |δτ| ≤ Γ̃ + 1` (control E7).
- *The bound on `α`.* By (4.1), (4.2), Lemma P and `|γ| ≤ 𝒩̄`,

      |α| ≤ 48κ + 6ε̃ + 3𝒩̄|δτ| + C₀𝒩r(2 + Γ̃)³ ≤ 48κ + C_α𝒩̄^{5/2} r λ^{−3/2} =: T,                                   (4.4)

  using `1 ≤ 𝒩̄/λ` for each of the last three terms (control E7).

*(d) Lemma X on `𝒢`.* By (4.2), `r|τ| ≤ r(Γ̃ + 1) ≤ 1` and the embedding condition holds, for small `r`. Since
`μ ≥ λ/2 ≥ C_G𝒩r/2`, `μ³ ≥ (256/9)𝒩̄²r⁴κ` and `μ² ≥ (64/3)𝒩̄r⁴κ` hold too. So Lemma X applies, with §0's `𝒩̄`, and on
`𝒢 ∩ {W_r > 0} ∩ {e = 1}` the soft curvature `s` lies below the maximum in (X.0).
- That maximum simplifies. `λ ≥ 2μ/3`, because `μ ≤ λ + ½C₀𝒩r`. `1024𝒩̄²r²κ/μ² ≤ κ`, because `μ ≥ 32C₀𝒩r = 32𝒩̄r`. And
  `((1024/3)𝒩̄κ)^{1/2} ≤ C𝒩̄(κ/μ)^{1/2}`, because `μ ≤ ‖D‖ ≤ 𝒩̄`.
- So

      s < ε̄(κ, μ, 𝒩) := C_ε[ κ + 𝒩̄(κ/μ)^{1/2} + κ^{1/3}(κ + 𝒩̄^{5/2}rμ^{−3/2})^{2/3} ].                               (4.5)

*(e) The weight.* `W_r/r² = F_d(K_M)F_{d−1}(K_S)` (#220 §0), which on typed pairs is `|det K_M||det K_S|`, and
`|det K_i| = |det H_i|/r` ([R] §4). As `det H_M = r²det H̃` and `det H_S = r²det H̃_S`, `|det K_M| = r|det H̃| = rs|det D|`
and `|det K_S| = r|det H̃_S| = rs_S|det D_S|`.
- `|det D| ≤ μ𝒩̄^{m−1}`.
- `|det D_S| ≤ λ_min(−D_S)𝒩̄^{m−1} ≤ 3μ𝒩̄^{m−1}`, since `λ_min(−D_S) ≤ λ + ½C₀𝒩r ≤ (3/2)λ ≤ 3μ` by (P.4).
- `s_S ≤ 12κ + 2ε̃ ≤ C𝒩̄²r/μ`, by (4.1)–(4.2), `κ ≤ r` and `μ ≤ 𝒩̄`.

Hence

    (W_r/r²) e 1_𝒢 ≤ C 𝒩̄^N r³ μ s 1{0 < s < ε̄(κ, μ, 𝒩)} 1{C_G𝒩r/2 ≤ μ ≤ 𝒩̄} 1{H̃ < 0}.                            (4.6)

*(f) The expectation.*
- *The layers.* On `{𝒩 ∈ [2^j, 2^{j+1})}` the right side of (4.6) is at most
  `F_j(H̃) := C2^{jN}r³μs1{0 < s < ε_j(μ)}1{x_j ≤ μ ≤ y_j}1{H̃ < 0}`, with `ε_j(μ) := ε̄(κ, μ, 2^{j+1})`,
  `x_j := C_G2^{j−1}r` and `y_j := C₀2^{j+1}` (`ε̄` increases with `𝒩`). As in note TS §1, Step 4,
  `P_Q(𝒩 ≥ 2^j | H̃) ≤ C_p2^{−jp}(P + ‖H̃‖)^p` (#220 Lemma H (b)). So the `j`-th layer contributes at most
  `C_p2^{−jp}E_Q[F_j(H̃)(P + ‖H̃‖)^p]`.
- *The `ã`-integration.* Given `(β̃, D)`, the entry `ã` of the Gaussian `H̃` (#220 Lemma H (a)) is Gaussian with variance in
  `[c, C]` and mean `m_ã = O(P + |β̃| + ‖D‖)`. Since `‖H̃‖ ≤ |ã| + 2|β̃| + ‖D‖`, and `(1 + |ã − m_ã|)^p` times the
  conditional density of `ã` is at most `C_p`, the weight `(P + ‖H̃‖)^p` costs only `C(P + |β̃| + ‖D‖)^p`, uniformly in `μ`.
  As `s = β̃ᵀD^{−1}β̃ − ã`, integrating `s` over `(0, ε)` gives, for every `ε > 0`,

      E_Q[s1{0 < s < ε}(P + ‖H̃‖)^p | β̃, D] ≤ Cε²(P + |β̃| + ‖D‖)^p.

- *The `μ`-integration.* Split `[x_j, y_j]` into at most `log₂(y_j/x_j) + 1 = log₂(8C₀/(C_Gr)) ≤ Clog(2/r)` dyadic shells
  `[x, 2x]`. By (V.3) for `Y = H̃` and `K = −D` (Lemma H (a): `m₀ ≤ CP`), the shell `[x, 2x]` contributes at most
  `C2^{jN}P^N x sup_{μ∈[x,2x]} r³με_j(μ)²`.
- *The integrand.* By (4.5), `(κ + y)^{4/3} ≤ 2^{1/3}(κ^{4/3} + y^{4/3})` and `κ ≤ 1`,
  `με̄² ≤ C𝒩̄^N[μκ² + κ + r^{4/3}κ^{2/3}μ^{−1}]`. So the shell `[x, 2x]` contributes at most
  `C2^{jN}P^N r³[x²κ² + xκ + r^{4/3}κ^{2/3}]`, and the shells of layer `j` together at most
  `C2^{jN}P^N r³[κ + r^{4/3}κ^{2/3}log(2/r)]` (`x ≤ y_j`, `κ² ≤ κ`; control E7 for the exponents).
- *Summing the layers.* `p` is large, so the series over `j` converges.

Hence `E_Q[(W_r/r²)e1_𝒢] ≤ Cr²[rκ + r^{7/3}κ^{2/3}log(2/r)]P^N`.

### 4.2 The bad region `ℬ = {W_r > 0} ∖ 𝒢`

On `ℬ`, `λ_min(−A) < C_G𝒩r`; this includes the case `A ≮ 0`. By (P.4) and Weyl's inequality,
`μ = λ_min(−D) < t(𝒩) := (C_G + C₀)𝒩r`. Note TS §1, Step 4 (the sign window of #198 §3 applied to #220 (F1)) gives
`|det K_S| ≤ Cr(κ + r)𝒩^{N₃}` on typed pairs. Also `|det K_M| = r|det H̃| ≤ rλ₁‖H̃‖^{d−1}`, where `λ₁ := λ_min(−H̃)`. So

    (W_r/r²) 1_ℬ ≤ C r²(κ + r) 𝒩^{N₃} λ₁ ‖H̃‖^{d−1} 1{H̃ < 0, μ < t(𝒩)}.                                                    (4.7)

- *Without the elder mark.* Use the layers of §4.1 (f) and (V.2) with `t_j := (C_G + C₀)2^{j+1}r` (Lemma H (a): `Y = H̃`,
  `K = −D`, `m₀ ≤ CP`). This gives `E_Q[(W_r/r²)1_ℬ] ≤ Cr²(κ + r)r^{5/2}P^N`.
- *With the elder mark.* On `{e = 1}`, note TS (1.3) gives `λ₁ ≤ ε″(𝒩) = C₆𝒩^{2/3}κ^{1/3}`. Use the same layers, and (V.1)
  with `ε″_j := ε″(2^{j+1}) = C₆2^{2(j+1)/3}κ^{1/3}` and the same `t_j`. This gives
  `E_Q[(W_r/r²)e1_ℬ] ≤ Cr²(κ + r)κ^{2/3}r^{1/2}P^N`.

With `κ ≤ r`, `E_Q[(W_r/r²)e1_ℬ] ≤ Cr²min(r^{7/2}, r^{3/2}κ^{2/3})P^N`.

### 4.3 Conclusion

Adding §§4.1–4.2 gives (S‴.1). For (S‴.2), use `r^{−2}A_r^{eld} = 12π_r(v_r)r^{−2}E_Q[(W_r/r²)e]`,
`π_r(v_r) ≤ Ce^{−c(b² + k²)}` ([R] (R5)) and `P^Ne^{−ck²} ≤ C(1 + |b|)^N`, and integrate in `b`, as in note TS's (S″.2). ∎

## 5. Proof of Corollary EM

Use note TS §5 verbatim: the decomposition (5.1) at `ρ = ℓ^{3/14}`, `𝒦₁`, `𝒦₂`, the cusp tails and `J₄` with (5.0), and the
part of `I^{eld}` on `[ρ, ℓ^{1/5}]`. Only `I^{eld}` on `[ℓ^{1/5}, r_0^*]` changes; there `κ = ℓ/r⁴ ≤ r`, and for small `ℓ`,
`ℓ^{1/5} < ℓ^{1/7} < r_*`.
- *On `[r_*, r_0^*]`.* (S″.2) gives `𝐓_r^{eld} ≤ C(κ + r)κ^{2/3} ≤ Cr_*^{−8/3}ℓ^{2/3}`, so this part is `O(ℓ^{2/3})`.
- *On `[ℓ^{1/5}, r_*]`.* Take the smaller of (S‴.2) and (W⁺.2). The latter gives `𝐓_r^{eld} ≤ 𝐓_r ≤ 8Cr³log(2/r)` for
  `κ ≤ r`, as in note TS §5. Then:
  - *The `rκ` term.* `rκ = ℓr^{−3}` meets `r³` at `r = ℓ^{1/6}`. So
    `∫_{ℓ^{1/5}}^{r_*}min(r³log(2/r), ℓr^{−3})dr ≤ ℓ^{2/3}log(2/ℓ^{1/5}) + ℓ^{2/3}/2 = O(ℓ^{2/3}log(1/ℓ))`.
  - *The `r^{7/3}` term.* `r^{7/3}κ^{2/3}log(2/r) = ℓ^{2/3}r^{−1/3}log(2/r)` is integrable at `0`, so it contributes `O(ℓ^{2/3})`.
  - *The bad region.* `r^{3/2}κ^{2/3} = ℓ^{2/3}r^{−7/6}` meets `r^{7/2}` at `r = ℓ^{1/7}`. So

        ∫_{ℓ^{1/5}}^{r_*} min(r^{7/2}, ℓ^{2/3}r^{−7/6}) dr ≤ (2/9)ℓ^{9/14} + 6ℓ^{2/3}ℓ^{−1/42} = (56/9)ℓ^{9/14}.

So `I^{eld}` on `[ℓ^{1/5}, r_0^*]` is `O(ℓ^{9/14})`. It replaces note TS's rows `a⁴log(1/ℓ)`, `ℓ^{2/3}a^{−2/3}` and
`ℓ^{5/3}a^{−17/3}`; the split `a` is no longer needed.

*The ledger of (EM.1)* (exponents of `ℓ` at `ρ = ℓ^{3/14}`; control E6):

| Term | Source | Exponent |
|---|---|---|
| `ρ³` | the `r²` part of #237 Lemma U (note TS) | **9/14** |
| `ℓ³ρ^{−11}` | the elder cusp tail; (W⁺.2) on `[ρ, ℓ^{1/5}]` (note TS) | **9/14** |
| `∫min(r^{7/2}, r^{3/2}κ^{2/3})` | Lemma S‴, the bad region, on `[ℓ^{1/5}, r_*]` | **9/14** |
| `∫min(r³log, rκ)` | Lemma S‴ (good region) with (W⁺.2) | 2/3, with `log(1/ℓ)` |
| `ℓ^{2/3}` | #237 Lemma U at the fold scale; Corollary TL1; Lemma S‴'s `r^{7/3}` term; (S″.2) on `[r_*, r_0^*]` | 2/3 |
| `ℓ²ρ^{−6}log(1/ℓ)` | (W⁺.2) on `[ρ, ℓ^{1/5}]` | 5/7, with `log(1/ℓ)` |
| `ρ⁸/ℓ` | the `r³/κ` part of (TL⁻) | 5/7 |
| `ℓ^{3/4}` | the `κr²` part of (TL⁻) | 3/4 |
| `ℓ²ρ^{−5}` | the finite part of `𝐀₂` | 13/14 |
| `ℓ⁴ρ^{−13}` | the contact difference (5.0) | 17/14 |

- *The least exponent.* It is `9/14`, attained by three rows. `σ = 3/14` is the only maximizer of `min(3σ, 3 − 11σ)`, and it
  gives Theorem TL⁻ at `θ = (1 − 4σ)/σ = 2/3 < 1`.
- *The far term.* #187 gives `0 ≤ ν_eld^{far,r_0^*} ≤ Cℓ^{2/3}`, and `2/3 > 9/14`, so it is absorbed. This is (EM.1).
- *(EM.2).* Subtract (EM.1) from #237 (P.1), whose remainder is `ℓ^{3/5}`; `c₂` cancels, and `3/5 < 9/14`.
- *SIDE24.* Divide by `cℓ^{−1/3}`: `9/14 + 1/3 = 41/42`. ∎

*How each input contributes* (control E6).
- Note TS: `4/7`, from its rows `a⁴log` and `ℓ^{2/3}a^{−2/3}`.
- Lemma S‴'s good region with (W⁺.2), but the bad region bounded only by Lemma S″ with (V.1) and (W⁺.2):
  - `min(r³, r^{3/2}κ^{2/3})` meets at `κ = r^{9/4}`, that is `r = ℓ^{4/25}`;
  - this gives `O(ℓ^{16/25}log(1/ℓ))`, and `16/25 < 9/14`.
- With (V.2) as well (the typed mass of the bad region, `r^{7/2}`): `9/14`.

## 6. Remarks

1. **What fixes `9/14`.** At `σ = 3/14` three ledger rows sit at `9/14`: `ρ³` and `ℓ³ρ^{−11}`, which cross there, and the bad
   region, whose exponent does not depend on `σ`.
   - Two belong to note TS's decomposition and not to Lemma S‴:
     - `ρ³`, the `r²` error of #237's Lemma U integrated over `[0, ρ]` (largest near `r = ρ`, where `κ = ℓ^{1/7}`; Lemma U's
       fold-scale part is the row `ℓ^{2/3}`);
     - `ℓ³ρ^{−11}`, the elder cusp tail, together with the typed bound (W⁺.2) on `[ρ, ℓ^{1/5}]`, where `κ ≥ r`.
   - The third is Lemma S‴'s bad region, a soft transverse direction at `M`. There the bound `min(r^{7/2}, r^{3/2}κ^{2/3})`
     integrates to order exactly `ℓ^{9/14}` (at most `(56/9)ℓ^{9/14}`, §5).
   - Going beyond `9/14` needs the third of the following and at least one of the first two (`ρ³` and `ℓ³ρ^{−11}` trade
     against each other through `σ`):
     - the `r²` term of the candidate kernel at `k ≥ r²` (in #237 the `r²` part of Lemma U is one source of the row `ρ³`,
       one of three rows that fix `ℓ^{3/5}` there together with the cap `ρ ≤ ℓ^{1/5}`; #237 Remark 2);
     - an elder matching on `[ρ, ℓ^{1/5}]`, where Theorem TL⁻ stops at `κ = r^θ`;
     - a barrier adapted to the soft transverse direction (along it the window third derivatives `(1, 2)` and `(0, 3)` carry
       the factors `r` and `r²`).

     On the ledger, the third with either of the first two, if its own error is negligible, gives `2/3` up to a logarithm.
     None is attempted.
2. **Relation to note TS Remark 1.**
   - *What TS recorded.* Its formal refinement runs the barrier along [N]'s ridge, to reach `λ_min(−H̃) ≲ κ^{1/3}(κ + r)^{2/3}`,
     an elder kernel `≲ r^{7/3}κ^{2/3}` on `κ ≤ r` and an intermediate mass `O(ℓ^{2/3})`. That needs a `C³` bound on the ridge,
     and TS did not attempt it.
   - *What Lemma X does instead.* It works in a box. Along the shear only the cubic coefficient `α` and the quartic bound
     enter. The `(2, 1)` derivative `≈ γ` enters `α` through `3γ·τ` (4.3), which turns `f₄` into `z`. The ridge's bending
     away from the shear line enters only through the cross term `2𝒩̄t²|ζ|`, so it costs `s ≳ 𝒩̄(κ/μ)^{1/2}`.
   - *The price.* That term gives the elder kernel `O(rκ)` on `𝒢`. It integrates, with (W⁺.2), to `O(ℓ^{2/3}log(1/ℓ))`.
   - *The upshot.* The good region alone would give an intermediate mass `O(ℓ^{2/3}log(1/ℓ))`. The `9/14` comes from the bad
     region and from the decomposition.
3. **The two densities.** The elder density is now known to `O(ℓ^{9/14})`, and the candidate density (#237) to `O(ℓ^{3/5})`.
   The rejected density, their difference, inherits `ℓ^{3/5}`. For the elder density, Lemma S‴ lifts the intermediate mass on
   `[ℓ^{1/5}, r_0^*]` from note TS's `ℓ^{4/7}log(1/ℓ)` to `ℓ^{9/14}`. It is no longer the only limiting term: its bad region
   now ties with the two rows of the decomposition (Remark 1). In notes TL and TS that mass was a limiting term; in #229 it
   was `O(ℓ^{4/9}log(1/ℓ))`, behind the fold and cusp rows at `3/7`.
4. **Numerical evidence for Lemma V** (exploration; not part of the proof; `numpy`, outside the repository; script
   `smallball.py`, to be archived with the note). The setup is `−Y = I + GOE`, with entries `N(0, 1)` on the diagonal and
   `N(0, 1/2)` off it, 4,000,000 samples, seed `20261006`; `P(Y < 0)` is `0.560` (`d = 2`) and `0.279` (`d = 3`). The pairs
   `(ε, t)` are `(0.02, 0.2)`, `(0.02, 0.1)`, `(0.02, 0.05)`, `(0.01, 0.05)`, `(0.005, 0.05)` and `(0.005, 0.0125)`.

   | `d` | `P(Y < 0, μ₁ ≤ t)/t^{3/2}`, `t = 0.2, 0.1, 0.05, 0.025` | `P(Y < 0, λ₁ ≤ ε, μ₁ ≤ t)/(εt^{1/2})` |
   |---|---|---|
   | 2 | `0.172, 0.167, 0.167, 0.165` | `0.213–0.248` |
   | 3 | `0.251, 0.255, 0.255, 0.258` | `0.345–0.385` |

   The ratios vary by at most 5% and 17% in `d = 2`, and 3% and 12% in `d = 3`, consistent with both exponents of the
   Lebesgue estimates behind (V.1)–(V.2) being attained.
5. **What Lemma X does not use.**
   - It does not use the pins at `S`, beyond the value `f(S) = b − κr⁴`.
   - It does not use Lemma Q′. The structure of `α` (4.3) and the typed window (4.1) are what make its threshold small on
     typed pairs.
   - Note TS's barrier (§1, Step 3) is its unsheared analogue: a ball instead of a box, the least eigenvalue `λ₁` of `−H̃` in
     place of `s` and `μ`, and the crude cubic bound `C₅𝒩` in every direction.

## 7. Exact controls (`em_exact.py`; stdlib; exact rationals; deterministic; byte-identical under `-O`)

The script and its stdout are published in the next comment, with the extraction rule.
- **E1** Lemma P on random pinned profiles, exactly. These are sextic and septic `p` with `p′(±h) = 0`, and quintic `ψ` with
  `ψ(±h) = 0`.
  - It checks (P.1)–(P.3) against `sup|p⁽⁵⁾|` and `sup|ψ‴|`, computed exactly, and the exact error
    `p‴(0) − 12k = −12c₅h² − 18c₇h⁴`.
  - On quintic profiles it checks the attained ratios `1/40` and `1/10`.
  - It checks the coefficients of the `D³E(M̂)` bound against `(|v_X| + |w|)³`.
- **E2** Lemma X's shear (2.1), exactly, for random negative definite `D` with `d = 2, 3`: `JᵀH̃J = diag(−s, D)`, `det J = 1`,
  `det H̃ = −s det D`.
- **E3** The cusp polynomial along the shear: `D³𝔓(M̂)[V³] = 12κ − f₄/2 + 3γ·τ = 12κ − z/2 + 3γ·δτ` (4.3); the value and
  slope of `𝔓` along the shear at `M̂`; the model Schur values `∓6κ(1 ∓ φ)`, and the second derivative along the model
  shear. It also checks the typed-window implications (4.1) on rational samples.
- **E4** Lemma X's box: on every accepted sample (all thresholds of (X.0) and both `μ`-hypotheses hold), the conditions
  (a)–(g) in squared form; the passage from the right side of (2.2) to (2.3) on a 5 × 5 grid of the box; the faces
  `−(5/4)κ`; `(x + y)⁴ ≤ 8(x⁴ + y⁴)`. Two boundary samples sit between the thresholds `(128/9)κT²` and `(256/9)κT²`.
- **E5** Lemma V's algebra, exactly: the factorization `det(−Y − λI) = det(K − λI)(a − a(λ))` at the roots and at random `a`;
  the interval characterization by Sylvester's criterion at `λ = 0` and `λ = ε`; the bound on `a(ε) − a(0)`; (L1);
  `min(2ε, t)^{3/2} ≤ 2εt^{1/2}`; `Σ2^{−i/2} ≤ 4`; and a self-check of the exponent arithmetic of (V.1)–(V.2).
- **E6** The ledger of (EM.1).
  - The rows at `σ = 3/14` and the three rows at `9/14`; the maximizer `σ = 3/14`.
  - The crossovers `ℓ^{1/6}` (giving `2/3`) and `ℓ^{1/7}` (giving `9/14`), with the bad region's exponent `−7/6` derived from
    `κ = ℓr^{−4}` and the constant `2/9 + 6 = 56/9`; the integrability of `ℓ^{2/3}r^{−1/3}`.
  - SIDE24's `41/42`; `3/5` for (EM.2); the far term absorbed; and the counterfactuals `4/7` and `16/25`.
- **E7** The constants of §4.1: (4.2)'s `C_Γ` on rational samples; (4.4)'s comparison `𝒩̄²r/λ ≤ 𝒩̄^{5/2}rλ^{−3/2}`;
  `|δτ| ≤ Γ̃/4 + ½` and `|τ| ≤ Γ̃ + 1`; `1024𝒩̄²r²κ/μ² ≤ κ` for `C_G ≥ 64C₀`; and the exponents of §4.1 (f).

Mutants, each rejected with exit 1, empty stdout and `FAILED: <group>` on stderr:

| Mutant | Change | Fails at |
|---|---|---|
| M1 | (P.1)'s constant `3/80 → 1/50` | `E1_pins` |
| M2 | (P.2)'s constant `13/80 → 1/20` | `E1_pins` |
| M3 | the shear's sign | `E2_shear` |
| M4 | `3γ·τ → 2γ·τ` | `E3_model` |
| M5 | (a)'s threshold `256/9 → 128/9` | `E4_box` |
| M6 | `δ_t² = 4κ/s → 2κ/s` | `E4_box` |
| M7 | `σ = 3/14 → 1/5` | `E6_ledger` |
| M8 | the bad-region typed exponent `7/2 → 3` | `E6_ledger` |
| M9 | the `β₁`-exponent `1/2 → 1` in E5's exponent self-check | `E5_volume` |
| M10 | the factor `2` in the `a`-interval bound `→ 1` | `E5_volume` |
| M11 | (P.3)'s constant `5/12 → 1/16` | `E1_pins` |

Invalid arguments exit 2 with the usage line.

**What the controls do not test.** The analytic estimates: Lemma P's Taylor remainders for non-polynomial `f`, and (P.4); the
Taylor bound (2.2) itself (E4 starts from its right side) and Step 4 of Lemma X (the embedding, the boundary of `𝓔` and the
maximin step); Lemma Q′'s use, Lemma H, the Gaussian integrations of §§3–4, and the corollary's integrals beyond their
exponents. The controls support the algebra only.

## 8. Review slices

- **A: §§1–2.** Lemma P, and Lemma X with the conditions (a)–(g) and the maximin step. Controls E1, E2 and E4, with mutants
  M1–M3, M5, M6 and M11.
- **B: §§3–4.** Lemma V (the Lebesgue estimates and the Gaussian transfer), and the proof of Lemma S‴. The latter covers
  Lemma Q′'s applicability, the typed window (4.1)–(4.2), the cubic coefficient (4.3)–(4.4), and the good-region and
  bad-region expectations. Controls E3, E5 and E7, with mutants M4, M9 and M10.
- **C: §0 and §§5–6, and the header.** The statements, Corollary EM with its ledger, the remarks, and the header for overclaim.
  Control E6, with mutants M7 and M8.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_