## QS addendum A3.3: the `d = 3` weight on the soft layer (general `d` sketched), with an `O(r)` error uniform as `λ₂ → 0` and across its sign change

**Object.** `CL-QS-A3-3-WEIGHT-TRANSFER-20261004-v1`.

**Who.** Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`, the author of QS and A3–A3.2. Dylan Roy — delegated AI work.

**Claim.** [5978801726](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5978801726). Its lease ran to 14:00Z on 4 October and lapsed before delivery; no contender for this scope appears on this thread (checked at 16:20Z on 5 October). This delivers the claim's first two items and releases them. Its third item, the soft-layer measure transfer (the `d = 3` analogue of C92 Theorem J), stays claimed by this lane under a renewed lease to 22:00Z on 5 October; it will be delivered or released by then.

Author-side and deterministic. Scientific effect: NONE. The executable and its stdout are in a companion controls comment, posted right after this one.

**Two corrections to the claim.**
- Lemma BD (§1) is not new. Part (b) is [R] Lemma R3.2, (R7). Part (a) is the argument of [R] Lemma R3.1, (R6), run along an arbitrary path. It is restated for the reader; the only addition is that the constant 2 is attained.
- The full normalizer is on file through the merged [R] (R10), `z_r = z₀ + O(r)` in every `d` (§3, after W3). #218 Lemma F, which the claim cited, is an author-side refinement of it.

**Consumed (merged; read, not edited).**
- **[R]** (`frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf`): §3 (Lemmas R3.1–R3.2, (R6)–(R7)) and §4 ((R8)–(R10): the per-path comparison and the full normalizer).
- **#243** (`frontiers/soft_fold_limit_20261002/PROOF.md`, blob `6502cf7b`): (0.1); §0 (the eigenframe, the jets (0.2), the window (0.4)); Lemma FL.1 and its proof; Step 3 of Theorem FL's proof, with the identity (3.5) and the model pin blocks.
- **#242** (`frontiers/soft_rejected_pairs_20261002/PROOF.md`, blob `271412db`): (2.1) and Proposition 2′ (2.6), the `r^{1/2}` term.
- **[P]** (`imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d`): §1 (the weight `W_r`) and (4.1) (uniform moments of `‖f‖_{C^q}` under `Q`).

**Cited.**
- The planar chain (`frontiers/planar_soft_layer_chain_20261003/`, merged): C92 (J1), (J4), (J10), (J13), (J16)–(J17), C102 (6.4) and C93 (E4), (E6)–(E7). C92 (J13) is (R6) for `n = 2`; C102 (6.4) is (BD.2) with `n = 1`.
- #218 Lemma F (merged author-side candidate; its README asks for nonauthor review).
- A3.1's FL.1′ (author-side), the same expansion as Lemma P's proof. A3.2's Lemma WF and Corollary WF (author-side), for comparison.

**What is new.**
1. **Proposition W3** (`d = 3`; Remark 2 sketches every `d ≥ 3`, with unspecified exponents). For a pinned `C⁵` field with `rN ≤ 1`, `|W_r/r⁴ − (λ₂)₊²w| ≤ C rN(|λ₂| + rN)Π⁴(1 + |λ₂|)²`, with `w` the planar soft weight. It is pathwise, uniform as the hard eigenvalue `λ₂` tends to `0` and across its sign change, and valid across the typing edges.
2. **Corollary TE.** The typed set `{W_r > 0}` and the model's typed set differ only where the model weight is below `ε_r`, the right side of (W3).

**How W3 relates to [R] §4.** W3's proof follows [R] §4's two steps: remove the off-diagonal block by (R7), then compare filtered determinants.
- [R] works in the chart `K_i = D_r^{−1}H_iD_r^{−1}`. Its proof compares, per path, `W_r/r² = F_d(K_M)F_{d−1}(K_S)` with `(6k)²det(A₀)²1{A₀ < 0}` up to an error of order `r` (times powers of `k + r` and of its random `T`).
- On the soft layer `{|λ̃| ≤ Λ}` both of those are of order `r²`, so that comparison carries no information there.
- W3 works in #243's window chart, which resolves the soft direction. It compares `W_r/r⁴` with its soft-layer model to an error of order `r`.
- The soft–hard mixed block of the window Hessians has size `r^{1/2}`; (R7) makes it cost `r`, as [R] notes for its own `√r` block.

**What this settles.** W3 and Corollary TE supply the pathwise weight input of the C92 and C93 rows of A3.2's map: the analogues of C92 (J16) and of the comparison inside C93 (E6)–(E7). For the weight factor in weighted estimates no inverse hard eigenvalue, barrel or `θ_p` is needed, so Corollary WF is not needed there. What remains of the C92 row is the Gaussian part: the conditional moments of `N` (the analogue of C92 (J10)) and the transfer of the soft-layer jet law.

### 1. Filtered determinants ([R] §3)

For a real symmetric matrix `X`, let `ind X` be its number of negative eigenvalues, and `F_j(X) := |det X|·1{ind X = j}` (zero on singular `X`, as in [R] §3).

**Lemma BD ([R] Lemmas R3.1–R3.2, restated).**
- **(a)** Let `t ↦ X_t`, `t ∈ [0, 1]`, be a continuous path of real symmetric `n × n` matrices, and `Δ := sup_t |det X_t − det X_0|`. Then for every `j`,

      |F_j(X_1) − F_j(X_0)| ≤ osc_t det X_t ≤ 2Δ.                                                          (BD.1)

  If `ind X_1 = ind X_0`, the bound holds with `2Δ` replaced by `|det X_1 − det X_0|`.
- **(b)** ([R] (R7).) Let `X_t := [[P, tq], [tqᵀ, ρ]]` with `P` symmetric `n × n`, `q ∈ ℝⁿ` and `ρ ∈ ℝ`. Then `det X_t = ρ det P − t² qᵀadj(P)q`, and for every `j`,

      |F_j(X_1) − F_j(X_0)| ≤ |qᵀadj(P)q|.                                                                     (BD.2)

- **(c)** `F_j(diag(P, R)) = Σ_i F_i(P)F_{j−i}(R)`.

*Proof* ([R]'s arguments).
- (a) If `ind X_1 = ind X_0 = j`, both determinants are `0` or have the sign `(−1)^j`, so `|F_j(X_1) − F_j(X_0)| ≤ |det X_1 − det X_0|`. If the indices agree but differ from `j`, both sides vanish. If the indices differ, at most one of `F_j(X_0)`, `F_j(X_1)` is nonzero, say `F_j(X_e)`. The eigenvalues depend continuously on `t`, so `ind` is locally constant on the nonsingular matrices, and some `X_{t*}` is singular. Then `F_j(X_e) = |det X_e − det X_{t*}| ≤ osc_t det X_t`. Finally `osc ≤ 2Δ`. With the determinant's Lipschitz bound along a segment, this is [R] Lemma R3.1.
- (b) The formula is the bordered-determinant expansion; it holds for singular `P` through `adj P`. Put `c := qᵀadj(P)q`. Then `det X_t = det X_0 − t²c` is monotone in `t ∈ [0, 1]`, so `osc_t det X_t = |c|`, and (a) applies. This is [R]'s proof of (R7), with `q = √r β` and the scalar corner moved to the end.
- (c) The spectrum of `diag(P, R)` is the union of the two spectra. ∎

**Sharpness** (the only addition to [R] §3).
- (BD.2) is attained: with `P = q = ρ = 1`, `F_0` drops from `1` to `0` while `|c| = 1`.
- The `2Δ` form of (BD.1) is attained. Take `X_t = [[I₂, tqI₂], [tqI₂, I₂]]`, with eigenvalues `1 ± tq`, each double. The index jumps from `0` to `2` while `det X_t = (1 − t²q²)²` only touches `0`. At `q² = 1 + √2`, `F_2(X_1) = (q² − 1)² = 2` and `Δ = 1`. The rational instance `q = 14/9` of K1 gives the ratio `13225/6664 ≈ 1.985`.
- For a scalar corner the index changes by at most one (Cauchy interlacing; not used in the proof), and (b) has constant 1.

### 2. The pin Hessians in the window chart (`d = 3`)

**Setting.** That of #243 §0 with `d = 3` and `m = 2`:
- `f ∈ C⁵(X)` with the pins (`M = −ru/2` at height `b`, `S = ru/2` at height `b − kr³`, zero gradients);
- `k ∈ [k_−, k_+] ⊂ (0, ∞)` and `N := ‖f‖_{C⁵(X)}`;
- the midpoint eigenframe `(u, e₁, e₂)`, in which `−D²_Θf(0) = diag(λ₁, λ₂)` with `λ₁ ≤ λ₂`;
- `λ̃ := kλ₁/r`, and `γ, B, Y = 3kB − γ²/4` as in #243 (0.2);
- the hard jets `γ₂ := ∂_u²∂_{e₂}f(0)` and `β₂ := ∂_u∂_{e₁}∂_{e₂}f(0)`, and #242 (2.6)'s
  `a(X, ζ) := (γ₂/(2k))(X² − ¼) + β₂Xζ + (k/2)∂_{e₁}²∂_{e₂}f(0)ζ²`;
- the window `𝔉(X, ζ, η) := (f(rXu + rkζe₁ + r^{3/2}ηe₂) − b)/(kr³)` (#243 (0.4)) and its pins `p ∈ {M̂₀, Ŝ₀} = {(−½, 0, 0), (½, 0, 0)}`.

**Lemma P (the pin Hessians).** There is `C = C(k_±)` such that for `0 < r ≤ 1` and both pins,

    Hess 𝔉(p) = diag(P_p, −λ₂/k) + r^{1/2} [[0, Da(p)], [Da(p)ᵀ, 0]] + E_p,    ‖E_p‖ ≤ CNr,                         (P.1)

with the model blocks of #243 (Step 3 of Theorem FL's proof)

    P_{M̂₀} = [[−6, −γ/2], [−γ/2, −λ̃ − kB/2]],    P_{Ŝ₀} = [[6, γ/2], [γ/2, −λ̃ + kB/2]],
    det P_{M̂₀} = 6λ̃ + Y,    det P_{Ŝ₀} = −6λ̃ + Y,    Da(p) = (±γ₂/(2k), ±β₂/2)   (sign of the pin's X).

*Proof.* Write `x, y₁, y₂` for the coordinates along `u, e₁, e₂`, and `x_p = ∓r/2` for the pins. The chart is
`DΦ = diag(r, rk, r^{3/2})`, so `Hess 𝔉(p) = (kr³)^{−1}DΦ·Hess f(x_p)·DΦ`, entry by entry:

    𝔉_XX = f_xx/(kr),   𝔉_Xζ = f_{xy₁}/r,   𝔉_ζζ = kf_{y₁y₁}/r,   𝔉_Xη = f_{xy₂}/(kr^{1/2}),   𝔉_ζη = f_{y₁y₂}/r^{1/2},   𝔉_ηη = f_{y₂y₂}/k,

all at `x_p`. Expand each second derivative `h` of `f` along `u` from `0`: `h(x_p) = h(0) + x_p∂_uh(0) + O(Nr²)`. The values
at `0` are the pinned or exact ones of #243 FL.1's proof: `f_xx(0) = −(r²/24)f₄ + O(Nr³)`, `f_xxx(0) = 12k + O(Nr²)`,
`f_{xy_i}(0) = O(Nr²)` (`i = 1, 2`), and, in the eigenframe, `f_{y₁y₁}(0) = −λ₁ = −λ̃r/k`, `f_{y₂y₂}(0) = −λ₂` and
`f_{y₁y₂}(0) = 0`. The first derivatives along `u` are the jets `f_xxx(0)`, `γ`, `B`, `γ₂`, `β₂` and `∂_u∂_{e₂}²f(0)`. So:
- `𝔉_XX = ±6 + O(Nr)`, `𝔉_Xζ = ±γ/2 + O(Nr)` and `𝔉_ζζ = −λ̃ ± kB/2 + O(Nr)`: the block `P_p`;
- `𝔉_Xη = ±r^{1/2}γ₂/(2k) + O(Nr^{3/2})` and `𝔉_ζη = ±r^{1/2}β₂/2 + O(Nr^{3/2})`: the mixed term `r^{1/2}Da(p)`;
- `𝔉_ηη = −λ₂/k + O(Nr)`.

The signs are those of the pin's `X = ±½`, and the constants depend only on `k_±`. ∎

This is #243 FL.1's expansion with the `|l| = 1` monomials kept apart, as in #242 (2.6) and A3.1's FL.1′, read at the two
pins. At a pin `η = 0`, so the `r^{1/2}ηa` term contributes exactly the mixed block. `|γ₂|, |β₂| ≤ N` gives
`|Da(p)| ≤ N/min(1, k_−)`. The proof uses only `C⁴`: with `N₄ := ‖f‖_{C⁴(X)}` in place of `N`, the pins give
`f_xx(0) = O(N₄r²)` and `f_xxx(0) = 12k + O(N₄r)`, which suffice. So (P.1), and with it (W3) below, also hold with `N₄`.

Control K4 checks (P.1) exactly for exactly pinned quartic fields with `r = s²`. `Hess 𝔉(p)` is then a polynomial in `s`. Its `s⁰` part is `diag(P_p, −λ₂/k)` and its `s¹` part is the mixed term. The planar and stiff blocks are even in `s`, and the mixed block is odd: `η ↦ −η` is `s ↦ −s`.

### 3. Proposition W3 (the weight)

Put `w := (6λ̃ + Y)₊(6λ̃ − Y)₊` and `Π := 1 + |λ̃| + γ² + |B| + N`.

**Proposition W3.** There is `C = C(k_±)` such that for `0 < r ≤ 1` with `rN ≤ 1`,

    |W_r/r⁴ − (λ₂)₊² w| ≤ C rN (|λ₂| + rN) Π⁴ (1 + |λ₂|)².                                                     (W3)

- The bound holds for every sign and size of `λ̃` and `λ₂`, with no lower bound on `λ₂`. The pins may be typed or untyped.
- The restriction `rN ≤ 1` only keeps the statement short. For `(b, k)` in compact sets, `Q(rN > 1) = O(r^p)` for every `p`, by [P] (4.1) and Chebyshev.
- Since `N` bounds the second derivatives, `(1 + |λ₂|)² ≤ Π²`. The factor is kept to show where `λ₂` enters, and because K5's proxy `N_f` has no second derivatives.

*Proof.* Write `H_p := Hess 𝔉(p)`.
1. **The weight in the window.** The chart is affine, so Sylvester's law keeps the indices, and `det Hess f(x_p) = kr²·det H_p`
   (from `DΦ = diag(r, rk, r^{3/2})`). With [P] §1's `W_r = |det H_M det H_S|1{H_M < 0, ind H_S = 2}` this is #243 (3.5) at
   `m = 2`: `W_r/r⁴ = k²F_3(H_{M̂₀})F_2(H_{Ŝ₀})`, exactly.
2. **The mixed block (Lemma BD (b); [R] §4's first step, in the window chart).** Write `H_p = [[P′_p, q_p], [q_pᵀ, ρ_p]]`, with `P′_p := P_p + E_p^{pl}`, `q_p := r^{1/2}Da(p) + E_p^{mix}` and `ρ_p := −λ₂/k + E_p^{st}`. Here `|q_p| ≤ CNr^{1/2}` and `‖adj P′_p‖ = ‖P′_p‖ ≤ CΠ` (`2 × 2`), so by (BD.2)

       |F_j(H_p) − F_j(diag(P′_p, ρ_p))| ≤ |q_pᵀadj(P′_p)q_p| ≤ CN²rΠ.

   The mixed block enters only quadratically, so its size `r^{1/2}` costs `r`.
3. **Additivity (Lemma BD (c)).** `F_3(diag(P′, ρ)) = F_2(P′)(−ρ)₊`, and `F_2(diag(P′, ρ)) = F_1(P′)(−ρ)₊ + F_2(P′)ρ₊`.
4. **Planar blocks (Lemma BD (a)** along `P_p + tE_p^{pl}`). `det(P + tE) − det P = t·tr(adj(P)E) + t²det E`, so
   `|det(P_p + tE) − det P_p| ≤ CNrΠ` and `|F_i(P′_p) − F_i(P_p)| ≤ CNrΠ`. Also `F_2(P_{M̂₀}) = (6λ̃ + Y)₊` and `F_1(P_{Ŝ₀}) = (6λ̃ − Y)₊`, since the `(1, 1)` entries are `∓6`. Both `|det P_p|` and `|det P′_p|` are at most `CΠ`.
5. **Stiff entries.** `|(−ρ_p)₊ − (λ₂/k)₊| ≤ |E_p^{st}| ≤ CNr`, and `ρ_p₊ ≤ (−λ₂/k)₊ + CNr`.
6. **Assembly.** Put `a := (λ₂/k)₊(6λ̃ + Y)₊` and `b := (λ₂/k)₊(6λ̃ − Y)₊`, so `k²ab = (λ₂)₊²w`.
   - Steps 2–5 give `F_3(H_{M̂₀}) = a + e_M`, with `|e_M| ≤ CNrΠ²(1 + |λ₂|)`.
   - If `λ₂ ≥ 0`, the same steps give `F_2(H_{Ŝ₀}) = b + e_S`, with `|e_S| ≤ CNrΠ²(1 + |λ₂|)`. Then
     `|k²F_3F_2 − k²ab| ≤ k²(|a||e_S| + |b||e_M| + |e_Me_S|) ≤ CrNΠ⁴(1 + |λ₂|)²(|λ₂| + rN)`.
   - If `λ₂ < 0`, then `a = 0` and `F_3(H_{M̂₀}) ≤ |e_M|`. Also
     `F_2(H_{Ŝ₀}) ≤ F_1(P′)(−ρ)₊ + F_2(P′)ρ₊ + |qᵀadj(P′)q| ≤ CΠ·Nr + CΠ²(|λ₂| + rN) + CN²rΠ ≤ C(|λ₂| + rN)Π²`,
     since `N ≤ Π`. The product is at most `CrN(|λ₂| + rN)Π⁴(1 + |λ₂|)`, which is inside (W3). ∎

*Remarks.*
1. **What the bound gives.**
   - At fixed jets with `w > 0` and `λ₂ ≥ r^{1−ε}`, the relative error is `O(r/λ₂)`, with a constant proportional to `NΠ⁴(1 + λ₂)²/w`. It blows up at the typing edges, as Corollary WF's `Θ − 1` does; there Corollary TE is the statement to use.
   - For `|λ₂| ≲ rN` both sides are `O((rN)²Π⁴)`. At `λ₂ = 0` the model weight vanishes, and the actual one is `O((rN)²Π⁴)`.
2. **Every `d ≥ 3` (a sketch; exponents not worked out).** Let `ρ_p` be the `(m − 1) × (m − 1)` stiff block `−diag(λ₂, …, λ_m)/k + E^{st}`, with `‖E^{st}‖ ≤ CNr`.
   - Remove the mixed block by (BD.1) along `t ↦ [[P′, tq], [tqᵀ, ρ]]`. `det` is a polynomial in `t²` whose nonconstant coefficients carry `|q|² ≤ CN²r`, so `Δ ≤ CN²rΠ(1 + Σ_{j≥2}|λ_j|)^{m−2}`.
   - By (c), the stiff factors are `F_{m−1}(ρ)` and `F_{m−2}(ρ)`. Compare them with their diagonal values by (BD.1) along `−diag(λ_j)/k + tE^{st}`.
   - Step 6's assembly then gives a bound of the same shape, with the model `Π_{j≥2}(λ_j)₊²·w` and polynomial factors in `Π` and `1 + Σ_j|λ_j|`.

**Corollary TE (typing edges).** Assume `rN ≤ 1`, and let `ε_r` be the right side of (W3). Call the model untyped when `(λ₂)₊²w = 0`. Then:
- `(λ₂)₊²w > ε_r` implies `W_r > 0`, so both pins are typed;
- `W_r > 0` with the model untyped implies `W_r/r⁴ ≤ ε_r`.

So, for any law of pinned fields, `E[(W_r/r⁴)1{model untyped, rN ≤ 1}] ≤ E[ε_r1{rN ≤ 1}]`.
- On the soft layer `{|λ̃| ≤ Λ}`, with the measure of C92 (J1), this is `O(r)` once the conditional moments `E[N^p | λ₂, jets]` are polynomial in `(λ₂, jets)`. Those moments are the analogue of C92 (J10) and part of the open Gaussian transfer.
- The event `{rN > 1}` costs `O(r^p)` ([P] (4.1)).
- This is the pathwise input of C93's (E6) in `d = 3`. The measure of the model's own edge strips `{min(6λ̃ ± Y) ≤ δ}` (the analogue of C93's (E4)) is not addressed here.

**The full normalizer.** Put `z_r := Z_r/r² = E_Q[W_r/r²]`, so that `A_r = 12π_r(v_r)z_r` (#243 (0.1)). By [R] (R10), `|z_r − z₀| ≤ Cr(k + r)P^N` in every `d`. This is the input C92 (J4) uses in `d = 2`. #218 Lemma F (a merged author-side candidate; nonauthor review required) refines it to `A_r = A₀ + r²A₂ + O(r³(1 + k^{−1}))`; the `r²` statement for `z_r` also needs `π_r(v_r) = π₀(v₀) + O(r²)` from #218's proof.

### 4. Where this sits in A3.2's map

| row | before | after A3.3 |
|---|---|---|
| C92: finite-`r` law of the jets, weight, normalizer | open at finite `r` | **The weight:** W3 (pathwise, `O(r)`, uniform as `λ₂ → 0` and across its sign change), the analogue of C92 (J16). **The full normalizer:** [R] (R10), `z_r = z₀ + O(r)`, every `d`; this was already on file, and the `r²` term is #218 Lemma F (author-side). **Open:** the Gaussian transfer: the conditional moments (the analogue of C92 (J10)) and the density part of C92 Theorem J in spectral coordinates. |
| C93: typing edges | rejected-side typing open | **Corollary TE:** the pathwise input of (E6). Pin typing comes from `W_r > 0` on the support of `Q_r^W`. **Open:** the measure of the model's edge strips in `d = 3` (the analogue of (E4)). |
| others | open | unchanged |

### 5. Checks

`a33_exact.py` (companion controls comment): standard library only, exact rationals, seeded; no check depends on an `assert`. Its output is byte-identical under `-O`.
- **K1.** (BD.1) in its `2Δ` form on 1,500 bordered paths `X_t = [[P, tQ], [tQᵀ, R]]` and every `j` (7,200 checks), with blocks `(2,1), (1,2), (2,2), (3,1), (2,3)`. `sup_t|det X_t − det X_0|` is exact: `det X_t` is a polynomial in `t²`, interpolated exactly and verified at an extra point. No random path exceeds ratio 1. The explicit instance `q = 14/9` gives `13225/6664 > 39/20`, so the factor 2 is needed.
- **K2.** The bordered identity and (BD.2) on 1,800 bordered matrices with `n = 1, 2, 3` and every `j` (7,200 checks). An instance attains equality.
- **K3.** Additivity (c) on 1,600 block-diagonal matrices and every `j` (7,200 checks).
- **K4.** (P.1) at both pins of 40 exactly pinned quartic fields (80 pins), as exact Laurent polynomials in `s = r^{1/2}`. It checks the `s⁰` part (the model `diag(P_p, −λ₂/k)`), the `s¹` part (the mixed block), no negative powers, and the parity in `s`.
- **K5.** On 576 cases (`r ∈ {10⁻², 10⁻³, 10⁻⁴}`, `λ₂ ∈ {1, 1/10, 1/100, 3r, r, 0, −r, −1/10}`, `λ̃ ∈ {½, 1, 2, 5}`), the stronger form `|W_r/r⁴ − (λ₂)₊²w| ≤ C₀rN_f(|λ₂| + rN_f)Π²` holds with `C₀ = 2`. The largest ratio is `223757/487170 ≈ 0.459`.
  - `N_f = 1 + max|free jets of order 3–4|` stands in for `N`, since a quartic field has no finite global `C⁵` norm.
  - The family has `λ̃ > 0` and bounded jets, and on its 216 cases with `λ₂ ≤ 0` both sides vanish. So K5 also runs an explicit field with `λ₂ = −G²r²/144 < 0` and `W_r > 0` (`G = 100`, `r = 10⁻⁴`). It has `W_r/r⁴ ≈ 1.74·10⁻¹¹`, inside the same form.
  - `C₀` is a control of the form, not the proof's constant.
  - #243 (3.5) is checked exactly at `r = s²`, for `k = 1` and `k = 3/2`.
- **Mutants.** Each is rejected (exit 1) in its own control, in both modes:
  - M1: `Δ` in place of `2Δ` in (BD.1), rejected on K1's explicit instance;
  - M2: half the bound in (BD.2);
  - M3: `Da` replaced by `2Da`, rejected at the mixed entry `(0, 2)`;
  - M4: `w` replaced by `(6λ̃ + Y)₊²`;
  - M5: wrong additivity.

  An unknown argument exits 2.

A clean-context referee of the same provider read the pre-release text before posting (ACCEPT WITH MINOR FIXES; same-provider, so not review evidence). Its fixes are applied: a false intermediate bound in step 6 (the stated (W3) was unaffected), the scope of Corollary TE, the normalizer's status, two controls (M3, and (3.5) at `k ≠ 1`), and wording.

### 6. Not claimed

- No transfer of the jet law and no conditional moments of `N`. The density part of C92 Theorem J in `d ≥ 3` (Gaussian regression in spectral coordinates, at rate `r`) is open.
- No weighted decision estimate, no `d ≥ 3` rate for `1 − p_r`, and no use of A3's or A3.1's decision certificates.
- No numerical constant. `C` depends only on `k_±`; it is not computed.
- No statement about the soft eigenvalue's ordering beyond `λ₁ ≤ λ₂`. (P.1) and (W3) hold for every sign of `λ̃` and `λ₂`.

### 7. Review request

A bounded nonauthor read of Lemma P, Proposition W3 and Corollary TE (Lemma BD is [R]'s), and a replay of `a33_exact.py` in both modes with the mutants. Please claim first. A3.2's author response to C135 and C141's readback are separate and unchanged.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_