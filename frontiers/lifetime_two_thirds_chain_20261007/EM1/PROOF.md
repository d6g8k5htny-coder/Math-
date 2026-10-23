# Lifetime addendum EM.1: the bad region of Lemma S‴ through the sheared box, and the intermediate elder mass `O(ℓ^{2/3}log(1/ℓ))` on `κ ≤ r`

Object: `CL-EM1-BAD-REGION-20261006-v1`. Claim: main#229 6024074852 (claim 2).
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 6 October 2026, for Dylan Roy (delegated AI
work). The same session wrote note EM and every consumed packet except [182] and [R], which are OpenAI's.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph, STATUS,
PROOF_INDEX, prize or Boolean change; no numerical constant is certified. Same GitHub account as every lane;
organizational independence 0. Before posting, two clean-context Claude subagents of this session refereed the draft in two
slices. Both returned AMEND with no blocking finding, and every finding is applied here. These are author-side reads and
earn no review credit.

**What is new.**
- **Lemma B** (§2). Note EM's bad region `ℬ` (a soft transverse direction at `M`) costs, once integrated, no more than its
  good region: `E_Q[(W_r/r²)e1_ℬ] ≤ Cr²[rκ + r²κ^{2/3}]P^N` for `0 < k ≤ r²`.
  - EM's `Cr²min(r^{7/2}, r^{3/2}κ^{2/3})P^N` still holds. Up to a factor 2, (B.1) is the smaller exactly when `κ ≤ r^{5/2}`,
    which contains EM's crossover `κ = r³`. Pointwise, (B.1)'s second term exceeds the good region's
    `r^{7/3}κ^{2/3}log(2/r)` by the factor `r^{−1/3}/log(2/r)`; on `[ℓ^{1/5}, r_*]` both integrate to `O(ℓ^{2/3})`.
  - The tool is EM's Lemma X itself, which is deterministic and does not need [N]'s Lemma Q′. On typed pairs the shear is
    short in the soft direction: `|τ|² < |ã|/μ`. So `r|τ| ≤ 1` once `μ ≥ 7𝒩̄r²`, and the cubic coefficient along the shear is
    `|α| ≤ 19𝒩̄^{3/2}(1 + μ^{−1/2})`. The transverse faces need only `μ ≳ 𝒩̄r^{4/3}κ^{1/3}`.
  - Without Lemma Q′ there is no typed window, so the threshold is weaker than on `𝒢`. Lemma X covers `ℬ₁ = ℬ ∩ {μ ≥ μ₀}`.
    There a new member of EM's Lemma V, (V.4), prices a small Schur complement `s < ε` beside a transverse eigenvalue
    `μ ∈ [x, 2x]` at `ε²x^{5/2}`, and `ℬ₁`'s part is at most `Cr^{5/6}` times the right side of (B.1). Both terms of (B.1)
    come from the rest, `ℬ₀ = ℬ ∩ {μ < μ₀}`, through EM's (V.1) with `t = μ₀` in place of `t ≍ r`.
- **Theorem S‴⁺** (§3). For `0 < r ≤ r_*` and `0 < k ≤ r²`, `E_Q[(W_r/r²)e] ≤ Cr²[rκ + r²κ^{2/3}]P^N` and
  `0 ≤ 𝐓_r^{eld}(k, u) ≤ C(rκ + r²κ^{2/3})`.
- **Corollary EM.1** (§3). The intermediate elder mass on `[ℓ^{1/5}, r_0^*]` is `O(ℓ^{2/3}log(1/ℓ))`. This is note TS Remark 1's
  formal target `O(ℓ^{2/3})` up to the logarithm, reached without a `C³` bound on [N]'s ridge.
  - In note EM's ledger the bad-region row moves from `9/14` to `2/3`. Corollary EM's `O(ℓ^{9/14})` is unchanged: its two
    remaining `9/14` rows, `ρ³` and `ℓ³ρ^{−11}`, belong to note TS's decomposition.
  - EM Remark 1's condition for going beyond `9/14` now reads: one of its first two items. With the first (a version of #237's
    Lemma U for `𝐓_r(k) − 𝐓_r(0)` with error `O(r²min(1, κ) + r min(k, 1/k))`, #237 Remark 2), and #229 (W⁺.3) for
    `∫_0^ρ𝐓_r(0)`, the ledger's least exponent is `2/3`, up to a logarithm.

**Not claimed.**
- No improvement of Corollary EM's `9/14`, of `ρ_rej`'s `3/5`, or of any statement of note TS beyond its kernel bound
  (S″.1)–(S″.2) on `κ ≤ r`, which (S‴⁺) sharpens, as EM's (S‴.1)–(S‴.2) did.
- No sharpness of any term; nothing pointwise in `b`; no certified number; no uniformity in `d` or `L`.
- Nothing beyond the existential scope of note EM and the packets it consumes.

**Consumed.**
- Note EM, main#229 6023010944 (controls 6023024039), to be read with its successor text 6023434026 (the AMEND, applied to
  the middle term of (4.4)). It is read in every slice: A PASS 6023042554, B AMEND 6023045290, C PASS 6023050789, and
  readback PASS 6023435335. Used here: §0 (notation, the good event `𝒢`, the bad region `ℬ`, Lemmas P, X and V); Lemma P
  (P.2) and (P.4); Lemma X; Lemma V (V.1), with §3's Lebesgue estimates (L0)–(L1) and Gaussian transfer; §4.1 (the
  good-region bound, (e), and the layers of (f)); §4.2 ((4.7), and `μ < t(𝒩)` on `ℬ`); §4.3; and §5 with its ledger and
  Remark 1.
- Note TS, main#229 6020794123 with successor text 6021299833: (1.3) and §1 Step 4 (`|det K_S| ≤ Cr(κ + r)𝒩^{N₃}` on typed
  pairs; the layers); (S″.1)–(S″.2); §5.
- #220 `frontiers/elder_third_order_20261001/PROOF.md` (blob `c8767dde`): §0 (`W_r/r² = |det K_M||det K_S|` on typed pairs);
  Lemma H, its exact form (H.1) (`|ã| ≤ 6κ + 𝒩̄/12`), (a) and (b).
- [R] (blob `247b3ecf`) §4 and (R5); [182] (blob `0d401877`) (2), through Lemma X; #229 (blob `110ed33a`) (W⁺.2), and (W⁺.3)
  for §3's scenario; #187 (blob `07260114`), through EM §5 only; #237 (blob `a97bf528`) Lemma U ((U.1)) and Remark 2.

**Cited only.** #198 `frontiers/remainder_rate_20260930/PROOF.md` (blob `abfb98ae`), (W.4), for a comparison in §3.

**Prior work and overlap.** I searched the tree of `main`, the project archive, and main#229 and main#259 since note EM.
Nothing else bounds the elder kernel on a soft transverse direction below note TS's barrier. EM Remark 1 named "a barrier
adapted to the soft transverse direction" as an open item; this addendum supplies it with EM's own Lemma X. The nearest
packets with a soft transverse direction are at a fixed gap `k ∈ [k₋, k₊]` (`κ = k/r → ∞`):
`frontiers/elder_dimension_lift_20260928` (an elder-failure lower event) and the QS `d = 3` soft-layer chain
(`frontiers/qs_d3_soft_layer_chain_20261005`, soft layer `|kλ₁/r| ≤ Λ`). Neither bounds the elder kernel on `κ ≤ r`.

## 0. Setting and statements

Notation is note EM's (§0). In particular `𝒩̄ = C₀𝒩 ≥ 1`, `H̃ = [[ã, β̃ᵀ], [β̃, D]]`, `μ = λ_min(−D)`,
`s = β̃ᵀD^{−1}β̃ − ã`, `τ = −D^{−1}β̃`, `𝒢 = {A < 0, λ_min(−A) ≥ C_G𝒩r}` and `ℬ = {W_r > 0} ∖ 𝒢`; on `ℬ`,
`μ < t(𝒩) := (C_G + C₀)𝒩r` (EM §4.2). Put `q_D := β̃ᵀ(−D)^{−1}β̃ ≥ 0`, so that `s = −ã − q_D`, and

    μ₀(𝒩) := 7𝒩̄r² + 4𝒩̄r^{4/3}κ^{1/3},        ℬ₁ := ℬ ∩ {μ ≥ μ₀(𝒩)},        ℬ₀ := ℬ ∩ {μ < μ₀(𝒩)}.

**Lemma V′ (a fourth small ball).** In the setting of EM's Lemma V (`−Y = [[a, yᵀ], [y, K]]`), put `s_Y := a − yᵀK^{−1}y` on
`{K > 0}` and `μ₁ := λ_min(K)`. For each `n ≥ 0` there are `C_n` and `N` such that for all `ε, x > 0`

    E[(1 + ‖Y‖)^n s_Y μ₁ 1{K > 0, 0 < s_Y < ε, x ≤ μ₁ ≤ 2x}] ≤ C_n(1 + m₀)^N ε² x^{5/2}.                                (V.4)

**Lemma B (the bad region).** There are `r_* > 0` and `C, N` such that for `0 < r ≤ r_*`, `b ∈ R`, `u ∈ S^{d−1}` and
`0 < k ≤ r²`,

    E_Q[(W_r/r²) e 1_ℬ] ≤ C r² [ rκ + r²κ^{2/3} ] P^N.                                                                (B.1)

**Theorem S‴⁺ (the elder weight on `κ ≤ r`).** For the same `r, b, u, k`,

    E_Q[(W_r/r²) e] ≤ C r² [ rκ + r²κ^{2/3} ] P^N,        0 ≤ 𝐓_r^{eld}(k, u) ≤ C (rκ + r²κ^{2/3}).                       (S‴⁺)

**Corollary EM.1.** As `ℓ ↓ 0`, `∫_{ℓ^{1/5}}^{r_0^*}∫𝐓_r^{eld}(ℓ/r³, u) dσ(u) dr = O(ℓ^{2/3}log(1/ℓ))`.

## 1. Proof of Lemma V′

On `B_R` (EM §3's coordinates and notation), `{K > 0, s_Y > 0} = {Y < 0}`, so (L1) holds: `β_i² < Rμ_i`. Split nothing: the
event already fixes the shell. The `K`-measure of `{x ≤ μ₁ ≤ 2x}` is at most `CR^Nx` (L0). Given `K`, only `β₁` is confined,
to `|β₁| < (2Rx)^{1/2}`, so the `y`-measure is at most `2(2Rx)^{1/2}(2R)^{m−1}`. Given `(y, K)`, `{0 < s_Y < ε}` is an
`a`-interval of length `ε`. On the set, `(1 + ‖Y‖)^n s_Yμ₁ ≤ (2R)^n·ε·2x`. So the `B_R`-part is at most `CR^{N′}ε²x^{5/2}`, and
EM §3's Gaussian transfer gives (V.4). ∎

(Control B4 checks the `x`-exponent `1 + 1/2 + 1 = 5/2` against the exponent used in §2 (d).)

## 2. Proof of Lemma B

Take `r_*` at most note EM's `r_*` (so `r_* ≤ r_Q ≤ 1/10`) and so small that `r + r^{3/2} ≤ L/4` for `r ≤ r_*`. Fix
`r ≤ r_*`, `b`, `u` and `0 < k ≤ r²`, so `κ ≤ r ≤ r_* ≤ 1/10`; `f = F_r` under `Q`. Work on a typed pair (`W_r > 0`), so
`H̃ < 0`, `D < 0` and `s > 0`.

*(a) The shear is short in the soft direction.* `(−D)^{−2} ≤ μ^{−1}(−D)^{−1}`, so `|τ|² = β̃ᵀ(−D)^{−2}β̃ ≤ q_D/μ`. As `s > 0`,
`q_D < −ã ≤ |ã|`. By #220 (H.1), the `uu` entry is `ã = −6κ + ∫_0^1 v(1 − v)²∂_u⁴f(M + rvu)dv` (#220 writes `s` for `v`);
with `∫_0^1 v(1 − v)²dv = 1/12` and `|∂_u⁴f| ≤ 𝒩̄`, `|ã| ≤ 6κ + 𝒩̄/12 ≤ 7𝒩̄` (`κ ≤ 1 ≤ 𝒩̄`). Hence

    |τ|² < 7𝒩̄/μ,        and        r|τ| ≤ 1   when   μ ≥ 7𝒩̄r²                                                       (2.1)

(control B1, on exact rational typed Hessians with rational eigenframes, and on boundary witnesses with `r²|τ|² > 0.99`).

*(b) The cubic coefficient along the shear.* `α = D³𝔉(M̂)[(1, τ)^{⊗3}]` has four parts: `r^{−1}∂_u³f(M)`, at most
`12κ + |f₄|/2 + (13/80)𝒩̄r ≤ 13𝒩̄` by EM (P.2) (`κ ≤ 1 ≤ 𝒩̄`, `|f₄| ≤ 𝒩̄`, `r ≤ 1`); `3∂_u²∇_Θf(M)·τ`, at most `3𝒩̄|τ|`;
`3r∂_uD_Θ²f(M)[τ, τ]`, at most `3𝒩̄r|τ|²`; and `r²D_Θ³f(M)[τ^{⊗3}]`, at most `𝒩̄r²|τ|³`. On `{μ ≥ 7𝒩̄r²}`, `r|τ| ≤ 1`, so
with (2.1)

    |α| ≤ 13𝒩̄ + 𝒩̄|τ|(3 + 3r|τ| + (r|τ|)²) ≤ 13𝒩̄ + 7𝒩̄(7𝒩̄/μ)^{1/2} ≤ T := 19𝒩̄^{3/2}(1 + μ^{−1/2})                    (2.2)

(`7√7 < 19`, and `13𝒩̄ ≤ 19𝒩̄^{3/2}` as `𝒩̄ ≥ 1`; control B2, with `𝒩̄` from `28/25` to `112`, including boundary samples
with `r|τ| = 1`).

*(c) Lemma X on `ℬ₁`.* On `ℬ₁`:
- `r|τ| ≤ 1` by (2.1), since `μ ≥ 7𝒩̄r²`;
- `r + 2r²(κ/μ)^{1/2} ≤ r + 2r²(r/(7r²))^{1/2} ≤ r + r^{3/2} ≤ L/4` by the choice of `r_*`;
- `μ³ ≥ 64𝒩̄³r⁴κ ≥ (256/9)𝒩̄²r⁴κ`, since `μ ≥ 4𝒩̄r^{4/3}κ^{1/3}` and `𝒩̄ ≥ 1`; and `μ² ≥ 49𝒩̄²r⁴ ≥ (64/3)𝒩̄r⁴κ`, since
  `μ ≥ 7𝒩̄r²` and `κ ≤ 1 ≤ 𝒩̄`.

(Control B3 checks the last two bullets at `μ = μ₀(𝒩)`.) So Lemma X applies with (2.2), and on `ℬ₁ ∩ {e = 1}` the curvature
`s` lies below the maximum in EM's (X.0). Each of its five terms is at most `1024𝒩̄²ε_ℬ(κ, μ)`, where (`ε_ℬ` depends on `r`
too)

    ε_ℬ(κ, μ) := κ + κ^{1/3} + (κ/μ)^{1/2} + (κ/μ)^{1/3} + r²κ/μ²:                                                    (2.3)

`((256/9)κT²)^{1/3} ≤ 22𝒩̄κ^{1/3}(1 + μ^{−1/3})` (as `(256/9)·19² ≤ 22³` and `(1 + y)^{2/3} ≤ 1 + y^{2/3}`);
`((1024/3)𝒩̄κ)^{1/2} ≤ 18.5𝒩̄(κ/μ)^{1/2}` (as `μ ≤ ‖D‖ ≤ 𝒩̄`); `64𝒩̄(κ/μ)^{1/2}`; `1024𝒩̄²r²κ/μ²`; `16κ` (control B3). Hence

    (W_r/r²) e 1_{ℬ₁} ≤ C 𝒩^N r²(κ + r) s μ 1{0 < s < 1024𝒩̄²ε_ℬ(κ, μ)} 1{μ₀(𝒩) ≤ μ < t(𝒩)} 1{H̃ < 0}:                (2.4)

here `W_r/r² = |det K_M||det K_S|` on typed pairs (#220 §0), `|det K_M| = r s|det D| ≤ r sμ𝒩̄^{m−1}` (EM §4.1 (e)), and
`|det K_S| ≤ Cr(κ + r)𝒩^{N₃}` (note TS §1, Step 4).

*(d) The expectation over `ℬ₁`.* Use 𝒩-layers as in EM §4.1 (f): on `{𝒩 ∈ [2^j, 2^{j+1})}` the right side of (2.4) is at most
the same expression with the factor `𝒩̄²` of `1024𝒩̄²ε_ℬ` at `2^{j+1}`, `μ₀(𝒩) ≥ μ₀(2^j)` and `t(𝒩) ≤ t(2^{j+1}) =: t_j`, and
#220 Lemma H (b) gives the factor `C_p2^{−jp}(P + ‖H̃‖)^p`. Split `[μ₀(2^j)/2, t_j]` into dyadic shells `[x, 2x]`. Since `ε_ℬ`
decreases in `μ`, (V.4) for `Y = H̃` (so `a = −ã`, `y = −β̃`, `K = −D`, `s_Y = s`, `μ₁ = μ`; Lemma H (a): `m₀ ≤ CP`) bounds
the shell by `C2^{jN}P^N ε_ℬ(κ, x)²x^{5/2}`. With `ε_ℬ² ≤ 5[κ² + κ^{2/3} + κ/μ + (κ/μ)^{2/3} + r⁴κ²/μ⁴]`, the shells sum to at
most `C2^{jN}P^N` times

    κ²t_j^{5/2} + κ^{2/3}t_j^{5/2} + κt_j^{3/2} + κ^{2/3}t_j^{11/6} + r⁴κ²μ₀(2^j)^{−3/2},

the first four from the top shell and the last from the bottom one. With `t_j ≤ C2^jr` and `μ₀(2^j) ≥ 4r^{4/3}κ^{1/3}`, this is at
most `C2^{jN}P^N[κ²r^{5/2} + κ^{2/3}r^{5/2} + κr^{3/2} + κ^{2/3}r^{11/6} + r²κ^{3/2}]`. Multiply by `r²(κ + r) ≤ 2r³` and sum the
layers (`p` large):

    E_Q[(W_r/r²) e 1_{ℬ₁}] ≤ C r²[ κ²r^{7/2} + κ^{2/3}r^{7/2} + κr^{5/2} + κ^{2/3}r^{17/6} + κ^{3/2}r³ ] P^N ≤ C r²[ rκ + r²κ^{2/3} ] P^N,

since on `0 < κ ≤ r ≤ 1` a monomial `r^aκ^b` is at most `r^{a′}κ^{b′}` when `b ≥ b′` and `a + b ≥ a′ + b′` (control B4).

*(e) The rest, `ℬ₀`.* By EM (4.7), `(W_r/r²)1_{ℬ₀} ≤ Cr²(κ + r)𝒩^{N₃}λ₁‖H̃‖^{d−1}1{H̃ < 0, μ < μ₀(𝒩)}`, and on `{e = 1}` note TS
(1.3) gives `λ₁ ≤ ε″(𝒩) = C₆𝒩^{2/3}κ^{1/3}`. The layers and EM's (V.1) with `ε = ε″(2^{j+1})` and `t = μ₀(2^{j+1})` give

    E_Q[(W_r/r²) e 1_{ℬ₀}] ≤ C r²(κ + r) κ^{2/3} μ₀(1)^{1/2} P^N ≤ C r²[ r²κ^{2/3} + r^{5/3}κ^{5/6} ] P^N,

as `μ₀(2^{j+1})^{1/2} = 2^{(j+1)/2}μ₀(1)^{1/2}` (the factor goes into the layer sum) and `μ₀(1)^{1/2} ≤ C(r + r^{2/3}κ^{1/6})`.
Finally `r^{5/3}κ^{5/6} = (rκ)^{1/2}(r^{7/3}κ^{2/3})^{1/2} ≤ rκ + r²κ^{2/3}` (control B4).

Adding (d) and (e) gives (B.1). ∎

## 3. Proofs of Theorem S‴⁺ and Corollary EM.1

*Theorem S‴⁺.* EM §4.1 bounds the good region by `Cr²[rκ + r^{7/3}κ^{2/3}log(2/r)]P^N`, and `r^{1/3}log(2/r) ≤ C` on
`(0, 1/10]`. Add Lemma B. The bound on `𝐓_r^{eld}` follows as in EM §4.3. ∎

*Corollary EM.1.* On `[r_*, r_0^*]`, note TS's (S″.2) gives `O(ℓ^{2/3})` (EM §5). On `[ℓ^{1/5}, r_*]`, `κ = ℓ/r⁴ ≤ r`; take the smaller
of (S‴⁺) and #229 (W⁺.2), `𝐓_r^{eld} ≤ 8Cr³log(2/r)`:
- `∫_{ℓ^{1/5}}^{r_*}min(r³log(2/r), ℓr^{−3})dr = O(ℓ^{2/3}log(1/ℓ))`, as in EM §5;
- `∫_0^{r_*}r²κ^{2/3}dr = ℓ^{2/3}∫_0^{r_*}r^{−2/3}dr = 3r_*^{1/3}ℓ^{2/3}`. ∎

*The ledger of note EM with Lemma B* (control B5). EM's row `∫min(r^{7/2}, r^{3/2}κ^{2/3})` (`9/14`) becomes `∫r²κ^{2/3}` (`2/3`),
and the bad region's `rκ` joins the row `∫min(r³log, rκ)` (`2/3`, with `log(1/ℓ)`), whose source is now both regions with
(W⁺.2); without (W⁺.2), `∫_{ℓ^{1/5}}rκ dr` is of order `ℓ^{3/5}`. At `σ = 3/14` the least exponent is still `9/14`, now attained
exactly by `ρ³` and `ℓ³ρ^{−11}`.
- If `ρ³` were replaced by `ℓ^{3/4}` (the integral of `r²min(1, κ)` over `[0, ρ]`, which #237 Remark 2's route would give), the
  least exponent would be `2/3` for every `σ ∈ [5/24, 7/33]`, with Theorem TL⁻ at `θ = (1 − 4σ)/σ < 1` there. That route is
  for `𝐓_r(k) − 𝐓_r(0)` and absorbs #237's `J₂`; note TS's (5.1) has no `J₂`, so in `𝒦₁` it leaves
  `∫_0^ρ∫𝐓_r(0, u)dσ dr ≤ Cρ⁴log(2/ρ)` (#229 (W⁺.3)), a row of exponent `4σ ≥ 5/6` there. (With #198 (W.4)'s `Cρ³`, the bound
  #237 uses for `J₂`, the row `ρ³` would stay.)
- Replacing `ℓ³ρ^{−11}` instead would need an elder matching on `[ρ, ℓ^{1/5}]`, where `r ≤ κ ≤ r^{2/3}` at `σ = 3/14`. Written
  through `𝐓^{eld} = 𝐓 − 𝐓^{rej}`, it needs two inputs there.
  - On the candidate side, Lemma U's error `Cr²` is at least `𝓐^{eld}`'s own size (`𝓐^{eld} ≤ Cκ³`, note TS §5) and
    integrates to `O(ℓ^{3/5})`; the first route's error `r²min(1, κ) = r²κ ≤ κ³` would remove this.
  - On the rejected side, Theorem TL⁻ stops at `κ = r^θ`, and even its error `κr² + r³/κ` would integrate to `O(ℓ^{3/5})`
    there.

  So the second route needs the first route's input and a rejected matching below `κ = r^θ`; the first route is the more
  direct one.

## 4. Remarks

1. **Why the bad region was the obstacle, and why it no longer is.** Note TS's isotropic barrier bounds only the least
   eigenvalue `λ₁` of `−H̃`. On `ℬ`, Cauchy interlacing and EM §4.2 (`λ_min(−A) < C_G𝒩r`, with (P.4) and Weyl's inequality)
   already give `λ₁ ≤ μ < t(𝒩) ≲ 𝒩r`; so for `κ ≥ r³` that barrier says nothing there, and EM paid the full typed mass
   `r^{7/2}`. In the sheared box the soft transverse direction is a coordinate direction `ζ`, with cubic and quartic
   coefficients `𝒩̄r²` and `𝒩̄r⁴`, so its faces cost only `μ ≳ r^{4/3}κ^{1/3}`; the price is moved to the shear direction,
   whose curvature is `s`. A small `s` beside a small `μ` is doubly rare: (V.4). Both terms of (B.1) come from `ℬ₀`, through
   (V.1) with `t = μ₀` in place of `t ≍ r`; by (V.4), `ℬ₁`'s bound is at most `Cr^{5/6}` times (B.1)'s.
2. **What Lemma B does not use.** Not [N]'s Lemma Q′, not EM's typed window (4.1), and no property of `A` beyond EM §4.2's
   `μ < t(𝒩)`: on `ℬ` the matrix `A` may be singular or indefinite. The barrier step (§2 (a)–(c), up to (2.3)) uses only
   Lemma X, (P.2), #220 (H.1) and the typed sign `s > 0`. The weight (2.4) and the expectations (§2 (d)–(e)) add #220 §0 and
   Lemma H (a)–(b), EM §4.1 (e) and (f), EM's (V.1) and (4.7), Lemma V′, and note TS's (1.3) and §1 Step 4.
3. **Constants.** No constant is certified. `C` depends on `C_G` through `t(𝒩)` only.

## 5. Exact controls (`em1_exact.py`; stdlib; exact rationals; deterministic; byte-identical under `-O`)

The script and its stdout are published in the next comment, with the extraction rule.
- **B1** (2.1) on exact typed Hessians: rational eigenframes for `m = 1, 2`, `|τ|²μ ≤ q_D < −ã`, `(−D)τ = β̃`, and
  `(r|τ|)² ≤ 1` once `μ ≥ 7𝒩̄r²`; boundary witnesses (`m = 1`, `𝒩̄ = 1`, `|ã| = 7`, `s = 10⁻⁶`, `μ = 7r²`) with
  `0.99 < r²|τ|² ≤ 1`; and `6κ + 𝒩̄/12 ≤ 7𝒩̄`.
- **B2** (2.2), exactly (by squaring), on samples with `7𝒩̄` a perfect square (`𝒩̄ = 7j²`, `j` rational, `28/25 ≤ 𝒩̄ ≤ 112`),
  including boundary samples with `r|τ| = 1`.
- **B3** The hypotheses and thresholds of §2 (c): the last two hypothesis bullets at `μ = μ₀(𝒩)` on exact perfect powers
  (`r = a³`, `κ = c³ ≤ r`, so `r^{4/3}κ^{1/3} = a⁴c`), with their constants `4³ ≥ 256/9` and `7² ≥ 64/3`;
  `(256/9)·19² ≤ 22³`, `(1 + u³)² ≤ (1 + u²)³`, the cubed inequality for (a) on exact perfect powers, and (b) against
  `18.5𝒩̄(κ/μ)^{1/2}`.
- **B4** The shell sums of §2 (d) and the two monomials of §2 (e), their domination by `rκ` and `r²κ^{2/3}` on
  `0 < κ ≤ r ≤ 1`, the AM–GM identity, and (V.4)'s `x`-exponent `1 + 1/2 + 1` against the exponent used in §2 (d).
- **B5** The ledger: the bad-region row, derived from its monomial `r²κ^{2/3}`; the two remaining `9/14` rows; and the
  scenario on `[5/24, 7/33]`, with `ρ³ → ℓ^{3/4}` derived from the two pieces of `∫_0^ρr²min(1, κ)` and the (W⁺.3) row `4σ`.

Mutants, each rejected with exit 1, empty stdout and `FAILED: <group>` on stderr:

| Mutant | Change | Fails at |
|---|---|---|
| M1 | the bound on `ã`: `7𝒩̄ → 6𝒩̄` | `B1_tau` |
| M2 | (2.2)'s constant `19 → 18` | `B2_cubic` |
| M3 | (V.4)'s exponent `5/2 → 3/2` | `B4_shells` |
| M4 | `μ₀^{1/2}`'s second term `r^{2/3}κ^{1/6} → r^{1/2}κ^{1/6}` | `B4_shells` |
| M5 | the bad-region row `2/3 → 3/5` | `B5_ledger` |
| M6 | the scenario's left end `5/24 → 1/5` | `B5_ledger` |
| M7 | (2.1)'s threshold `7𝒩̄r² → 𝒩̄r²` | `B1_tau` |
| M8 | `μ₀`'s second coefficient `4 → 3` | `B3_threshold` |

**What the controls do not test.** Lemma X and Lemma V themselves (note EM); the weight (2.4); the Gaussian integrations of
§2 (d)–(e); the domination rule itself (B4 applies it); the expansion `μ₀(1)^{1/2} ≤ C(r + r^{2/3}κ^{1/6})` (its exponents are
taken as given); the 𝒩-layer monotonicity; `r^{1/3}log(2/r) ≤ C`; and Corollary EM.1's integrals beyond their exponents.

## 6. Review slices

- **A: §§0–1 and §2 (a)–(c).** Lemma V′; the shear bound (2.1); the cubic bound (2.2); the hypotheses of Lemma X on `ℬ₁`; the
  threshold (2.3); the weight (2.4). Controls B1–B3, mutants M1, M2, M7 and M8.
- **B: §2 (d)–(e), §§3–4 and the header.** The layered expectations, the shell sums, `ℬ₀`, Theorem S‴⁺, Corollary EM.1, the
  ledger and the remarks. Controls B4–B5, mutants M3–M6.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_