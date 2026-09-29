# Elder-failure lower bound in every dimension: the soft-eigenplane lift

**Object:** CL-ELDER-LOWER-ALL-D-20260929-v1. **Author:** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`).
**Disposition:** author-side proof candidate; **nonauthor analytic review required**. Scientific effect: NONE. No
register, `STATUS`, `PROOF_INDEX`, `GRAPH`, prize or premise changes.

## 0. What is closed, and what is consumed

The reconciled D1 chain states (reconciliation §2): "**No lower bound is asserted for `d ≥ 3`**." The planar direct
lower bound OA-ELDER-LOWER-DENSITY-GAP-20260928-v1 (`frontiers/window_multiplicity_laws_20260928/
ELDER_LOWER_AND_DENSITY_GAP.md`, blob `aaefc8da…`, Theorem E1) gives `1 − p_r ≥ c r³` in `d = 2` and was ACCEPTed
with no defect in `reviews/d1_elder_lower_claude_20260928/REVIEW.md`. This note lifts it to every fixed `d ≥ 2`.

**Theorem E1_d (direct lower bound, every dimension).** Fix `d ≥ 2`, `L > 0`, compact `B` and `K ⊂ (0,∞)`. For the
parent's typed pair law `Q_r^W` (P §1: `2(d+1)` pins, full normalizer `Z_r`) and the parent's global ordinary
elder selector `p_r(b,k,R)` (P §8 maximin), there are `c, r_* > 0` with

    1 − p_r(b,k,R) ≥ c r³,   0 < r ≤ r_*,                                   (D1)

uniformly over `b ∈ B`, `k ∈ K` and all orthonormal frames `R`.

**Corollary E2_d.** With the parent's Theorem A (P (1.1), accepted at existential scope):
`c r³ ≤ 1 − p_r ≤ C r³` in every `d ≥ 2`; and with P §§9–11, the compact-window selection-density loss is
`ν_cand(ℓ) − ν_eld(ℓ) = Θ(ℓ^{2/3})` in every `d ≥ 2`. The parent's `O(ℓ^{2/3})` compact-window rate is therefore
optimal in order in every dimension, not only in the plane.

Consumed, unchanged: the parent P = `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`
(blob `dfed3b8d…`) read with the reconciliation reading rule — §1 (law, pins, `W_r`, `Z_r`, `p_r`), §2 (finite-jet
rank), §3 (uniform positive definiteness of the contact jet covariance; (3.5)), §4 (uniform conditional `C⁴`
moments), (5.1), (5.3), §8 (maximin definition, generic locus), Theorem A, §§9–11; and the planar record's
(E1) obstruction, (E5)–(E6) path with its `k/64` margins, (E7) pinned normal form, (L9)–(L13) box mass and
`C⁴` control, (E8)/(L15) ledger. Nothing in those sources is re-proved here; the new content is §§2–4.

## 1. Why the planar event does not lift naively, and what does

Write `m = d − 1` and let `A = D_y² f(0)` be the transverse Hessian at the midpoint. The planar event pins the
single transverse second derivative to `f_zz(0) ≈ −(3k/2) r` (a box of width `∝ r`, hence `Q_r`-mass `∝ r`), and
that is the entire source of the factor `r¹` in the ledger `r · r⁴ / r² = r³`.

The wrong lift is to make *every* transverse direction soft: pinning all `m(m+1)/2` entries of `A` to `O(r)`
values costs `Q_r`-mass `∝ r^{m(m+1)/2}`, and the two endpoint determinants then carry `r^{1+m}` each, so the
ledger becomes `r^{m(m+1)/2} · r^{2+2m} / r²`, which is `r⁷` already at `d = 3`.

The right lift matches the parent's own upper-bound mechanism. P §7 controls `Q^W(G_r^c)` by integrating the
weight over the boundary layer where **only the smallest** transverse eigenvalue `λ_1` is `O(r)`, with
`λ_2, …, λ_m` free (P (7.1)–(7.4)); the `r³` there is `∫_0^{Dr} λ_1(λ_1 + …) dλ_1`. So the lower-bound event must
be: **one soft transverse eigenvalue of order `r`, all others of order one**. The planar path then lives in the
plane spanned by the axis and the soft eigenvector, and the hard directions contribute only `O(1)` factors.

## 2. The event

Fix `ε ∈ (0, 1/16]` with also `ε ≤ 1/(2√m)`, `0 < σ_1 < σ_2 < ∞`, and `K_4 < ∞`, all to be chosen (depending on `d, L, B, K` only). Let
`−A(0) = O Λ O^T` with `Λ = diag(λ_1 ≤ … ≤ λ_m)` and `e_1 = O e_1` a unit eigenvector for `λ_1` (on the event below
`λ_1` is simple, so `e_1` is determined up to sign; fix the sign by a measurable rule). Write
`(x, y_1, y')` for coordinates along the axis, along `e_1`, and along `e_1^⊥ ⊂ ℝ^m`. The event `E_r` is the
intersection of:

- **(E-soft)** `|λ_1 − (3k/2) r| < εk r` (so `s := −λ_1/r` lies within `εk` of the planar target `−3k/2`);
- **(E-hard)** `λ_j ∈ [σ_1, σ_2]` for `j = 2, …, m`;
- **(E-jet)** in the frame `(x, e_1)`, the four planar-slice third-order jets at `0` satisfy the planar box:
  `|f_{xxy_1}| < εk`, `|f_{xy_1y_1} + 2k| < εk`, `|f_{y_1y_1y_1}| < εk` (the planar (L9) box minus its
  `f_zz` coordinate, which (E-soft) replaces);
- **(E-mix)** `|f_{xx y_j}(0)| < εk` for every transverse direction `y_j` in `e_1^⊥`;
- **(E-C⁴)** `‖f‖_{C⁴(X)} ≤ K_4`.

(E-soft) is a condition on `A(0)` only; so is (E-hard); the frame `e_1` used in (E-jet)/(E-mix) is a function of
`A(0)`.

## 3. On `E_r` the planar obstruction applies in the soft eigenplane

Let `Π = {y' = 0}` be the plane through `M, S` spanned by the axis and `e_1`, and let `g = f|_Π`, a smooth function
of `(x, y_1)`. Its six planar pins are the restrictions of the parent's `2(d+1)` pins: `g(M) = b`, `g(S) = b − kr³`,
`∂_x g = ∂_{y_1} g = 0` at `M` and `S` (the transverse gradient pins in direction `e_1`). Its degree-`≤ 3` jets at `0`
in the `(x, y_1)` frame are: `g_{y_1y_1}(0) = −λ_1`, so `s = −λ_1/r` is within `εk` of `−3k/2` by (E-soft), and `g_{xxy_1}, g_{xy_1y_1},
g_{y_1y_1y_1}` inside the planar box by (E-jet). Its `C⁴` norm is at most `K_4` by (E-C⁴). Therefore the planar
pinned normal form (E7) holds for `g` verbatim, with `s = g_{y_1y_1}(0)/r`, `a = g_{xxy_1}`, `β = g_{xy_1y_1}`,
`c = g_{y_1y_1y_1}` inside the planar targets' `ε`-box, and the planar choice of `ε` and `r_*` (E7 within `k/64` of
`G_k` in `C⁰` on `B(0,3) ∩ Π`) is available unchanged. Hence the three-segment path (E5) scaled by `r`, which lies in
`Π`, connects `M` to a point with `f`-value `> b` while staying `> b − kr³/4 > f(S)`.

A path in `Π` is a path in the torus, so P §8's maximin gives `d_f(M) ≥ b − kr³/4 > f(S)`, i.e. (E3) holds for the
`d`-dimensional field. On the generic (Morse, distinct-value) locus this forces the global ordinary elder partner of
`M` to differ from `S`. This is exactly the planar §1 argument; no gradient-flow, separatrix or extra-saddle statement
is used.

## 4. Mass, weight, normalizer: the ledger is `r · r⁴ / r² = r³` in every `d`

**(a) `Q_r(E_r) ≥ c_1 r`.** Under `Q_r`, `A(0)` is a nondegenerate Gaussian on `Sym_m` with covariance uniformly
bounded above and below and uniformly bounded mean (P §3, the Schur-complement statement preceding (3.5)); hence its
density is bounded *below* by a positive constant on every fixed compact set. In eigenvalue coordinates
`(λ, O)`, Lebesgue measure on `Sym_m` is `c_m ∏_{i<j} (λ_j − λ_i) dλ dO` (P §7, second paragraph). On
(E-soft)∩(E-hard) every factor `λ_j − λ_1` lies in `[σ_1/2, 2σ_2]` for small `r`; the remaining factors
`λ_j − λ_i` (`2 ≤ i < j`) vanish on the diagonal of the hard box, but their integral over the *ordered* hard box is
a positive constant independent of `r`. So the Lebesgue measure of `{A : (E-soft), (E-hard)}` is `c · 2εk r ·
(1 + O(r))` with `c > 0`, and `Q_r((E-soft)∩(E-hard)) ≥ c_1' r`. (Checker `V*`: the exact eigenvalue-region measure for
`m = 2, 3` is a polynomial in `r` with positive linear coefficient.)

Conditionally on `A(0)` (which fixes the frame `e_1`), the odd third-order jets and the mixed jets in (E-jet),
(E-mix) — finitely many derivative functionals at `0`, distinct from the pins and from `A(0)` — have a Gaussian
conditional law whose covariance is uniformly nondegenerate (P §2 finite-jet rank; P §3 compactness over frames)
and whose mean is affine in the conditioned values, hence bounded on the event. A fixed box of side `2εk` in a
rotated frame is a rotated box; by compactness of `O(m)` and continuity of the conditional law in the frame, its
conditional probability is at least `c_2 > 0` uniformly. So `Q_r((E-soft)∩(E-hard)∩(E-jet)∩(E-mix)) ≥ c_1' c_2 r`.

Finally (E-C⁴): exactly as in the planar (L12)–(L13), condition on all the pinned jets before bounding the `C⁴`
norm. Because the jet list depends on the frame, disintegrate on `A(0)` first; conditionally on `A(0) = A` the
list `(U_r, A, J_sel(e_1(A)))` is a fixed finite list of distinct functionals whose covariance floor is uniform
over `O(m)` by compactness, so the P §4 regression argument applies with uniformly bounded coefficients and gives a
uniform conditional `C⁴` moment; `K_4` can then be chosen with conditional probability `≥ 1/2` at every jet target
in the box. Hence `Q_r(E_r) ≥ c_1 r`, `c_1 = c_1' c_2 / 2`. One may not replace this by subtracting
an unconditional tail from a rare event of size `r` (planar N-note, retained).

**(b) `W_r ≥ c_2 r⁴` on `E_r`.** In the frame `(x, e_1, e_1^⊥)`:

- *Axial entries.* P (5.2): `|α_M + 6k| ≤ rM_4/2`, `|α_S − 6k| ≤ rM_4/2`; on (E-C⁴) these are `6k(1 ± O(r))`.
- *Transverse blocks.* `A_M = A(0) − (r/2) ∂_x A(0) + O(r² K_4)` and `A_S = A(0) + (r/2) ∂_x A(0) + O(r² K_4)`.
  In the eigenframe of `A(0)`: the `(e_1,e_1)` entries are `−λ_1 ∓ (r/2) f_{xy_1y_1}(0) + O(r²)`, i.e.
  `−(k/2) r (1 ± 3ε)` at `M` and `−(5k/2) r (1 ± (3/5)ε)` at `S` up to `O(r)` (using (E-soft) and `f_{xy_1y_1} ≈ −2k`, the
  planar values `−k/2`, `−5k/2` of the scaled model); the hard block is `−diag(λ_2, …, λ_m) + O(r)`; the
  soft–hard off-diagonals are `∓(r/2) f_{x y_1 y_j}(0) + O(r²) = O(r K_4)`. For `r ≤ r_*` small, both blocks are
  negative definite (the `2×2` minors need `(k/2) r σ_1 > O(r²)`), and
  `|det A_M| = (k/2) r ∏_{j≥2} λ_j · (1 ± 3ε + O(r))`, `|det A_S| = (5k/2) r ∏_{j≥2} λ_j · (1 ± (3/5)ε + O(r))`.
- *Types.* `H_M = [[rα_M, rβ_M^T],[rβ_M, A_M]]` with `α_M < 0` and `A_M ≺ 0`; by the pin identity (5.3),
  `det H_M / r = α_M det A_M − r β_M^T adj(A_M) β_M`, so `H_M ≺ 0` once the correction is dominated (next item).
  `H_S` has `α_S > 0` and `A_S ≺ 0`, hence index exactly `m = d − 1`. These are the parent's typed support.
- *The `β` correction is dominated.* From the transverse gradient pins, `f_{y_j}(x,0)` vanishes at `x = ∓ r/2`, so
  `f_{y_j}(x,0) = (x² − r²/4) g_j(x)` with `g_j(0) = f_{xxy_j}(0)/2 + O(rK_4)`; differentiating,
  `β_{M,j} = f_{xy_j}(M)/r = −f_{xxy_j}(0)/2 + O(rK_4)`. By (E-jet) (`j = 1`) and (E-mix) (`j ≥ 2`),
  `‖β_M‖ ≤ (√m/2) εk + O(r)`, and the same at `S`. Since `‖adj(A_M)‖ ≤ ∏_{j≥2} λ_j (1 + O(r))` (drop the soft
  eigenvalue), the correction `r² ‖β‖² ‖adj A_M‖` is at most `(m ε²/4) k² r² ∏ λ_j`, against the main term
  `3 k² r² ∏ λ_j (1 − ε)(1 − 3ε)` (the factor `(1 − ε)` absorbing `|α_M| ≥ 6k(1 − ε)` for small `r`). For
  `ε ≤ 1/16` and `ε ≤ 1/(2√m)` this is dominated with room; the checker verifies the exact rational inequality
  `3(1−ε)(1−3ε) − mε²/4 ≥ 3/2` at `ε = 1/16`, `m = 1..4`, and the analogue `15(1−ε)(1−3ε/5) − mε²/4 ≥ 15/2` at `S`.

Therefore `|det H_M| ≥ (3/2) k² r² ∏_{j≥2} λ_j` and `|det H_S| ≥ (15/2) k² r² ∏_{j≥2} λ_j`, so
`W_r ≥ c_2 r⁴` with `c_2 = (45/4) k_-⁴ σ_1^{2(m−1)}`. (Checker `D*`: the exact model determinants are
`3k²σ^{m−1}r²` and `15k²σ^{m−1}r²`, product `45k⁴σ^{2(m−1)}r⁴`, for `m = 1..4`; `m = 1` recovers the planar values.)

**(c) `Z_r ≤ C_Z r²`.** P (5.3) with (5.1) and the uniform `Q_r` moments of P §4, exactly as in the planar (L14)
(or `[RM] (11)`).

**(d) Ledger.** `Q_r^W(E_r) = E_Q[W_r 1_{E_r}] / Z_r ≥ c_2 r⁴ · c_1 r / (C_Z r²) = c r³`, and every field in
`E_r` satisfies the obstruction of §3. This proves (D1). All constants are existential and independent of
`r, b, k` and the frame on the compact ranges; `ε, σ_1, σ_2, K_4, r_*` depend on `d, L, B, K` only.

## 5. Corollary E2_d and what it does not say

**Consistency with the cap theorem (sanity check, not part of the proof).** The parent's cap theorem guarantees
pairing on `G_r = {λ_min(−A_M) > (4/(3k)) r M_3², rM_4 ≤ 3k/10}`, so the obstruction event must lie in `G_r^c`. It
does: on `E_r` the soft eigenvalue is `λ_min(−A_M) ≈ (k/2) r`, while `M_3 ≥ |f_{xy_1y_1}| ≈ 2k` forces
`(4/(3k)) r M_3² ≥ (16/3) k r > (k/2) r`. The event sits squarely in the parent's depth-failure boundary layer —
the same layer whose weighted mass P §7 bounds above by `C r³` — which is why the two bounds meet at `r³`.

The upper half is P Theorem A verbatim (P §7 is dimension-free). Composition with P §§9–11 is the planar (E9)–(E11)
computation, which is written for general `d` (the ledger `r A_r dr db dk dσ` and the change `ℓ = kr³` do not see
`d`); the `k^{−5/3}` bounding factor is finite on the compact gap window. Hence `Θ(ℓ^{2/3})` in every `d`.

Not supplied: any numerical `c, C, r_*`; any statement outside compact marks (the unrestricted difference is the
C7-total question, untouched here); any rate for `ν_cand` or `ν_eld` individually; any change to the parent's
existential scope; nonauthor acceptance. The `d = 2` case is not re-proved — it is the accepted planar record — and
this note adds nothing to it.

## 6. Review requested (non-Claude lane)

Slice A (finite algebra; identities): §4(b) model determinants and the `β`-domination inequality; the eigenvalue-
region measure scaling; the ledger. All in `lower_all_d_check.py`.
Slice B (continuum, three steps): (i) the lower density bound for `A(0)` on compacts under `Q_r` (P §3); (ii) the
conditional box probability in the *random* eigenframe (P §§2–3 + compactness of `O(m)`); (iii) the `C⁴` control
after conditioning (planar (L12)–(L13), P §4). OpenAI (author of the planar record and the parent) and xAI are the
natural lanes; the planar base was reviewed by a Claude session, so a non-Claude read of §3's "restriction inherits
the planar normal form" step is the highest-value single check.

## Reproduce

    python -B -S lower_all_d_check.py            # prints RESULTS.json byte for byte
    python -B -O -S lower_all_d_check.py         # identical
    python -B -S lower_all_d_check.py --mutant M # exit 1 for M in {M1, M2, M3}
