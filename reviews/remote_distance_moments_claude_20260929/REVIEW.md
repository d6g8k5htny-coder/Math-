# Nonauthor analytic review: remote pair-distance moments and the transition at order one (Math-#116, C4)

Scientific effect: **NONE**. This file changes no register, status, graph node, lemma flag, prize or author source.
It records a verdict on candidate C4 of `reviews/candidates_pending_20260928/CANDIDATES.md`. Integration is a
separate act.

## Object

| Field | Value |
|---|---|
| Object | OA-WINDOW-MULTIPLICITY-DISTANCE-20260928-v1 (OpenAI / ChatGPT) |
| Branch / head | `chatgpt/window-multiplicity-laws-20260928` / `0507e3a1dbd3dede84cbeb805947c70aa16ebc36` ([Math-#116](https://github.com/d6g8k5htny-coder/Math-/pull/116)) |
| `REMOTE_DISTANCE_MOMENTS.md` | Git blob `d077743b7fda8b1bb2e1bafdab97d01bb9e321b1`, 11097 B, SHA256 `b40dc67a0c4760d3db796914bdc50cbbd5fd1371786772fa919a3a100467b41d`, 234 lines |
| Consumed, on main | [RP] `frontiers/window_multiplicity_laws_20260928/REMOTE_PAIR_LAW.md` (blob `3fb60204…`, integrated by Math-#129 at `e7f8aca`). [RC] `frontiers/remote_collision_20260928/PROOF.md` (blob `7b48a88e…`): (4.1)–(4.3), Lemmas 1–3, 5. [RM] `frontiers/remote_window_20260924/PROOF.md` (blob `b383bfcc…`): §6 (15), §4 endpoint identities, full normalizer. |
| Request | [Owner comment 5880152796](https://github.com/d6g8k5htny-coder/Math-/pull/116#issuecomment-5880152796), which left C4 open after the C3 claim; claimed in [5888678663](https://github.com/d6g8k5htny-coder/Math-/pull/116#issuecomment-5888678663) |

## Provenance and exposure

| Field | Value |
|---|---|
| Reviewer | Anthropic Claude, Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3` |
| Relation | Different provider from the OpenAI author. Same GitHub account as every lane, so no organizational independence is claimed. |
| Exposure | **I authored [RC]**, and C4 uses its frame, Lemma 2 and Lemma 5. I reviewed [RP] (C3, ACCEPT) and [Math-#128](https://github.com/d6g8k5htny-coder/Math-/pull/128) (ACCEPT), whose Theorem I overlaps the first line of (D5). This review checks their use in C4, not their truth. |
| Author code | `algebra.py` is absent from the tree, as `PUBLICATION.json` discloses. I did not run, request or reconstruct it. |
| Independent checks | `distance_review_check.py` is my own exact-rational suite, written from the markdown. It covers finite identities only. |

## Verdicts

| Interface (lines) | Verdict |
|---|---|
| §1 (8–57): `M_p` for `p ≥ 0`; `A_p` (D2) for `0 ≤ p < 7`; `Λ_2` (D3); `B_p` (D4) | **ACCEPT**; see N6 on the `4 < p < 7` range of (D2). |
| §2 (59–102): the sharper determinant bound (D6), the conditioned bound (D7), the radial envelope (D8) | **ACCEPT**; see §1 below. The height integral is exact (N2). |
| §3 (104–128): the diagonal bound (D9), `0 < B_p < ∞`, the fixed-distance density (D10) | **ACCEPT**; see §2 below. (D10) reads RM (15) for mixed indices (N1). |
| §4 (130–168), **Theorem D (D5)**: `r^{5+p}A_p` for `0 ≤ p < 1`; `r⁶(A_1 + B_1)` at `p = 1`; `r⁶B_p` for `p > 1` | **ACCEPT** at the stated fixed-`E`, fixed-`ρ`, existential scope; see §3 below. |
| §5 (170–201): the limiting law (D13), the `s^{−8}` tail and `R^{−7}` survival (D14), and, for `p ≥ 0`, `E[S^p] < ∞` iff `p < 7` | **ACCEPT**; see §4 below. |
| §6 (203–223): (D15), (D16), quantiles and RMS; TV does not control unbounded moments | **ACCEPT** |
| §7 (225–234) boundary | **ACCEPT** as stated. |

No defect was found. Notes N1–N6 delimit the result without changing it.

---

## §1 — the height-retaining determinant bound and the envelope (§2)

**(D6).** On `∇f(x) = ∇f(x+δe) = 0`, RC's (R7) gives `H_x e = δ(−½D³f[e,e,·] + O(δK))` with `K ≍ 1 + ‖f‖_{C⁴}`.
So in a frame beginning with `e`, both the axial entry and the cross block carry a factor `δ`. The Peano identity
[RC] (4.2) gives `T = −12t + O(δK)`, so `α = −T/2 + O(δK) = 6t + O(δK)` at `x`, and `−6t + O(δK)` at `x'`.

`DET` checks both facts exactly.
- The block identity `det[[δα, δβᵀ],[δβ, A]] = δα det A − δ²βᵀadj(A)β` holds on 100 random rational matrices, 22 of
  them with singular `A` (20 forced, 2 by chance).
- On the axial fields `g'(u) = (c₀ + c₁u)(u² − δu)`, which have critical points at `0` and `δ`:
  `t = −c₀/6 − c₁δ/12`, `α_x = 6t + (c₁/2)δ` and `α_{x'} = −6t + (c₁/2)δ`, exactly. So the `O(δK)` remainder is
  genuinely present, with slope `c₁/2`.

Hence `|det H| ≤ Cδ(|t|K^{d−1} + δK^d)`.

**(D7).** Multiply the two determinant bounds, `W_r ≤ Cr²K^{2d}` ([RC] Lemma 3) and `Z_r ≥ cr²`. [RC] Lemma 2 gives
conditional `K`-moments `≤ C(1+|t|)^q` and a `V_δ`-density `≤ C(1+|t|)^{−q}` for every `q`. Together these give
`Cδ²(t² + δ²)(1+|t|)^{−q}`. The conditioning value of `D3_δ` is exactly `t`, so using `t` inside (D6) is legitimate.

**(D8).** With `a = kr³/δ³`, the two windows allow `(y, t)` with `y ∈ I_r` and `|t| ≤ a`. The `y`-section at fixed
`t` has length `(kr³ − δ³|t|)_+`. The height integral is therefore exactly

    ∫_{−a}^{a} (t² + δ²)(kr³ − δ³|t|) dt = kr³(a³/6 + δ²a),

because `δ³a = kr³`. The note's bound `C kr³(a³ + δ²a)` is correct (N2, `ENVELOPE`).

With the density power `δ^{−d−3}`, `dy' = δ³dt`, the determinants `δ²` and polar `δ^{d−1}`, the radial density is
`C r³δ(a³ + δ²a) = C(k³r^{12}δ^{−8} + kr⁶)` for `δ ≥ r`. For `δ ≤ r`, the `t`-integral is bounded and the density is
`C r³δ`. Both exponents are checked for every d.

The sharper envelope is necessary at `p = 1`. RP's envelope `r⁴s·min(1, s^{−3})` equals `r⁶δ^{−2}` for `δ ≥ r`. Its
first moment puts equal mass on every dyadic shell, so the middle region would contribute `≍ r⁶log(1/r)`, not
`O(A^{−6})r⁶`. The `ENVELOPE` shell sum shows this. It confirms the point in 5880152796.

## §2 — the diagonal and the fixed-distance kernel (§3)

At `Q_0` with both witness heights equal to `b`, the collision frame has `t = 0` exactly, so (D6) gives
`|det H| ≤ Cδ²K^d` at each witness. The ledger is: product `δ⁴`, value-gradient density `δ^{−d−3}` ([RC] (4.3) at
`r = 0`, where [RC] Lemma 1 already includes `r = 0`), polar `δ^{d−1}`. It totals `δ⁰` for every d (`DIAGONAL`). So
`δ^{d−1}Λ_2(x, x+δe)` is bounded. The bounding envelope `δ^p` is locally integrable for `p > −1`, hence `B_p < ∞` on
the claimed domain `p ≥ 0`. This is sufficiency only: no negative-moment threshold for the actual kernel `Λ_2` is
established here. Off-diagonal positivity alone does not give a positive limiting diagonal coefficient; a positive
bounded radial kernel such as `exp(−1/δ)` has every negative moment finite.

Positivity: at distinct remote sites, the two Hessians and `B_0` have full joint conditional support by [RM] §2's
distinct-jet principle, so `Λ_2 > 0` off the diagonal. A positive-volume `E` has `E × E` of positive measure at some
fixed separation.

(D10) is [RM] (15) at `m = 2`, `η = ε`: the density is `(kr³)²Λ_2 + O(r⁷)`, uniform on `dist ≥ ε`. The factor
`dist^p` is bounded there, and Borel `E × E` restriction is an equality of finite measures. See N1 on indices.

## §3 — Theorem D (§4)

**`0 ≤ p < 1`.** This is RP's dominated convergence with the weight `s^p`. The envelope `s^{p+1}min(1, s^{−3})` is
integrable, and separated pairs give `O(r^{1−p})` after division. (D11) is exactly #128's (I11), which I checked there
on exact instances for negative and positive `p`. (D2) at `p = 0` is RP's `(3/40)12^{2/3}`.

**`p > 1`.** Divide by `r⁶`. The contributions are:
- `δ ≤ r`: `r³∫_0^r δ^{p+1}dδ/r⁶ = r^{p−1}/(p+2)`;
- the `r^{12}` part on `[r, ε]`: `r⁶(ε^{p−7} − r^{p−7})/(p−7)`, which is `O(r^{p−1})` for `p < 7` and
  `O(r⁶ε^{p−7})` for `p > 7`. These are checked exactly for integer `p`, including monotone decrease in `r`. At
  `p = 7` it is `r⁶log(ε/r)`;
- the `r⁶` part: `≤ ε^{p+1}/(p+1)`;
- `dist ≥ ε`: `B_p(ε) + O_ε(r)` by (D10).

Letting `r → 0` and then `ε → 0`, monotone convergence (by (D9)) gives `B_p(ε) ↑ B_p`. Correct.

**`p = 1`.** The three pieces are all nonnegative:
- the inner part `δ ≤ Ar`, after division by `r⁶`, converges to `A_1(A) = A_0∫_0^A s g_S(s) ds`, by dominated
  convergence on the compact range `s ≤ A`;
- the middle part is at most `r⁶∫_{Ar}^ε δ^{−7}dδ = A^{−6}/6 − r⁶ε^{−6}/6` plus `ε²/2`, checked exactly (`REGIMES`);
- the outer part converges to `B_1(ε)`.

So `A_1(A) + B_1(ε) ≤ liminf ≤ limsup ≤ A_1(A) + B_1(ε) + CA^{−6} + Cε²`. Then `A ↑ ∞` and `ε ↓ 0` give
`A_1 + B_1` without any uniform-integrability assumption. `A_1 = (k²/(2z_0))∫∫p E[w_0|T|(det A)²]` matches (D2) at
`p = 1`, since `3·12/(4·3·6) = 1/2`.

## §4 — the limiting law and its tail (§5–§6)

(D13) is #128's (I20), accepted there, with the same `Ψ_E`. The substitution `t = kv/s³` gives
`k⁴s^{−9}∫_{−1}^1 v²(1−|v|)Ψ_E(kv/s³)dv`, and `∫v²(1−|v|) = 1/6`. Bounded continuous `Ψ_E` with `Ψ_E(0) > 0` gives
(D14), with constants `6` and `6/7`.

`TAIL` checks the limit on an exact piecewise-polynomial model `Ψ = (1 − t²)_+`:
`s⁹∫t²(k − s³|t|)_+Ψ dt → k⁴/6` with error `O(s^{−6})`. For `p ≥ 0`, `E[S^p] < ∞` iff `p < 7`, and then it equals
`A_p/A_0` by the Tonelli identity `108/((p+2)(p+5))` (`MOMENTS`). `g_S = O(s)` at `0`. Across real `p`, the lower
endpoint is `−2`, from #128's positive `J_0` (N5); the upper-tail argument alone is not a complete real-moment domain.

The tail reproduces the envelope's shape: `r⁴g_S(δ/r) ≈ (6k⁴Ψ_E(0)/z_0)r^{12}δ^{−8}`. So the first term of (D8) is
the actual microscopic tail, not slack. The two terms of (D8) cross at `δ ≍ r^{3/4}` (N3).

(D15): `E[S_r] = r^{−1}M_1/M_0 → (A_1 + B_1)/A_0`, which exceeds `E[S] = A_1/A_0` by `B_1/A_0 > 0`. (D16):
`E[S_r^p] = r^{−p}M_p/M_0 ~ (B_p/A_0)r^{1−p}`. The RMS distance is `√(M_2/M_0) ~ √(rB_2/A_0)`. Quantile convergence
follows from TV convergence to a law with a positive continuous density on `(0, ∞)`. The explanation offered, that a
pair-weighted mass of order `r` sits at fixed physical distances, is exactly the `B_p` term.

## Notes

- **N1 (index reading of (D10)).** [RM] (15) is stated for ordered `m`-tuples of a single index `j`. (D10) needs the
  all-index sum, which includes mixed pairs `(i, j)`, `i ≠ j`. The [RM] §6 argument is index-agnostic: distinct-site
  regression, `F_i` continuous, `W_r` once and `Z_r` once. [RC] Lemma 5 already re-derived the mixed-index upper bound.
  I read (D10) as that argument applied to each index pair and summed. This is an interface reading, not a gap.
- **N2 (exact height integral).** `∫_{−a}^{a}(t² + δ²)(kr³ − δ³|t|)dt = kr³(a³/6 + δ²a)`. The note's `C(a³ + δ²a)`
  is correct and not sharp in the constant.
- **N3 (consistency, not a joint limit).** The microscopic tail `(6k⁴Ψ_E(0)/z_0)r^{12}δ^{−8}` matches (D8)'s first
  term. The fixed-distance radial density is bounded by (D9). The crossover `δ ≍ r^{3/4}` is heuristic. No uniform
  intermediate-scale asymptotic is claimed or accepted.
- **N4 (why the sharper bound matters).** With RP's envelope alone, the `p = 1` middle region would be
  `≍ r⁶log(1/r)`. The height-retaining (D6)–(D8) is what makes the two-cutoff argument close.
- **N5 (relation to Math-#128).** (D5)'s first line and (D13) coincide with #128's Theorem I and (I20). Combined:
  - the pair-weighted limit `S` has `E[S^p] < ∞` exactly for `−2 < p < 7`;
  - `M_p` is microscopic exactly for `−2 < p < 1`;
  - the lower boundary comes from #128's `J_r > 0`, the upper boundary from `B_1 > 0` here.

  Neither note consumes the other.
- **N6 ((D2) for `4 < p < 7`).** The negative power `|T|^{(4−p)/3}`, with `(4−p)/3 > −1`, is integrable because the
  conditional density of `T` given `(Y, B_0, A)` is bounded. That conditional variance is positive by the distinct-jet
  floor. So the tower property applies with the weight `w_0(det A)²`. Conditioning on `Y` alone would not justify
  pulling the weight out; the note's wording "weighted conditional Gaussian density" is consistent with this reading.

## What this review does not do

- It does not review C5 (`HEIGHT_MARKS.md`) or C6.
- It accepts no event-conditioned pair law, uniform intermediate-scale asymptotic, global (pin-inclusive) factorial
  bound, uniformity as `ρ → 0` or over oscillating `E_r`, numerical constant, or persistence interpretation.
- It does not run or reconstruct `algebra.py`, and it changes no register.

## Revisions

- **v2** (wording only, requested in [5888822723](https://github.com/d6g8k5htny-coder/Math-/pull/130#issuecomment-5888822723)):
  §2 now says the bounded envelope gives `B_p < ∞` for `p ≥ 0` (sufficiency only, no negative threshold for `Λ_2`),
  and the `p < 7` moment statement is qualified to `p ≥ 0` in the verdict table and §4. No verdict, proof reading or
  checker change.

## Reproduce

    python -B -S distance_review_check.py            # prints RESULTS.json byte for byte
    python -B -O -S distance_review_check.py         # identical
    python -B -S distance_review_check.py --mutant M # exit 1 for each of the 7 mutants
