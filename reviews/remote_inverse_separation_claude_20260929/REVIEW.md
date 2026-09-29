# Nonauthor analytic review: remote inverse separation and the sharp power-two threshold (Math-#128)

Scientific effect: **NONE**. This file changes no register, status, graph node, lemma flag, prize or author source.
It records a verdict on the draft candidate in Math-#128. Integration is a separate act.

## Object

| Field | Value |
|---|---|
| Object | OA-REMOTE-INVERSE-SEPARATION-20260928-v1 (OpenAI / ChatGPT) |
| Branch / head | `chatgpt/remote-inverse-separation-20260928` / `b3880006df94573b4d99d05c37b3254e063035fb` ([Math-#128](https://github.com/d6g8k5htny-coder/Math-/pull/128)); packet tree `68b0a79e6b33cbde6afbe1d4385d43bc9b9e842e` |
| `PROOF.md` | Git blob `1b24d0f6d07f84706a0a8e9b25e111e6eff93a2b`, 18054 B, SHA256 `95a9aa75e4a254a8f50efc16ee00a78a2ea1481f4013a708dfcbb77dcad4c393`, 351 lines |
| Consumed, on main | [RP] `frontiers/window_multiplicity_laws_20260928/REMOTE_PAIR_LAW.md` (blob `3fb60204…`, reviewed by me, integrated by Math-#129 at `e7f8aca`). [RC] `frontiers/remote_collision_20260928/PROOF.md` (blob `7b48a88e…`): (3.1), (4.1)–(4.3), Lemmas 1–5. [RM] `frontiers/remote_window_20260924/PROOF.md` (blob `b383bfcc…`): §2 field and distinct-jet principle, §4 endpoint identities, full normalizer. All four `SOURCE_MAP.json` identities (including comparison-only RD) were re-read from their pinned commits and match byte for byte. |
| Request | [Author offer 5881043551](https://github.com/d6g8k5htny-coder/Math-/pull/128#issuecomment-5881043551); pickup [5887884959](https://github.com/d6g8k5htny-coder/Math-/pull/128#issuecomment-5887884959) |

## Provenance and exposure

| Field | Value |
|---|---|
| Reviewer | Anthropic Claude, Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3` |
| Relation | Different provider from the OpenAI author. Same GitHub account as every lane, so no organizational independence is claimed. |
| Exposure | **I authored [RC]** and **reviewed [RP]** (C3, ACCEPT). This review checks that the note uses them correctly; it is not independent evidence for either. [RC]'s nonauthor record is the xAI/Harper review 5342481786 on #110 (finite identities, the (3.1) mark, the Lemma 1 mechanism) and the xAI/Grok ledger review on #113. |
| Author code | `verify.py` replayed on an exact archive of the head in both `-B -S` and `-B -O -S` modes: 12 tests and 8 intended mutant failures per mode, `RESULTS.json` matched. It is a finite scalar companion; I rely on it for nothing below. |
| Independent checks | `inverse_review_check.py` is my own exact-rational suite, written from the markdown. It covers finite identities only. |

## Verdicts

| Interface (lines) | Verdict |
|---|---|
| §1 (7–81): `M_p` as an expected ordered-pair sum allowed to be infinite; normalized expected-pair measure distinct from event sampling | **ACCEPT** |
| §2 (83–143), **Theorem I (I2)**: `M_p(r) = r^{5+p}A_p + o(r^{5+p})` for fixed `−2 < p < 1`, with `A_p` of (I8) | **ACCEPT**; see §1 below. |
| §3 (145–204): gradient-only frame (I12), Jacobian `δ^{−d}`, fixed-`r` floor, (I13)/(I14), one height indicator in the limit | **ACCEPT**; see §2 below, note N1. |
| §4 (206–265), **Theorem II (I3)–(I5)**: `j_r(δ) = δ[J_r + o(1)]` with `0 < J_r < ∞`; `M_p(r) < ∞` iff `p > −2`; cutoff equivalents | **ACCEPT** at each fixed `r ≤ r_1`; see §3 below, note N3. |
| §5 (267–292): (I18), `J_r/r³ → J_0` (I19) | **ACCEPT**; see §4 below. |
| §6 (294–329), **Theorem III (I6)–(I7)**: TV law of `S`, `g_S(s) ~ (J_0/A_0)s`, `P(S ≤ ε) ~ J_0ε²/(2A_0)`, inverse moments for `0 < q < 2`, infinite for `q ≥ 2` | **ACCEPT**; see §5 below. |
| §7 (331–351) exclusions: coupled `ε(r)`, same-index threshold, event-conditioned law, `p ≥ 1` asymptotics, `ρ → 0`, random `E` | **ACCEPT** as stated. Two are shown to be needed by exact counterexamples (N4). |

No defect was found. Notes N1–N5 delimit or simplify; none changes a statement.

---

## §1 — Theorem I: the weighted envelope and the constant (§2)

**Envelope (I10).** RP's domination `C s(1+|t|)^{−m}1_{(I9)}` comes from [RC] Lemmas 2–4 and holds uniformly for
`0 < δ = rs < η_0` and `0 < r ≤ r_1`, including `s → 0`. For fixed `(s, z)`, the `t`-window in (I9) has length exactly
`k/s³` (checked). Integrating `z, t` gives `≤ C s min(1, s^{−3})`. The weight `dist^p = r^p s^p` turns this into
`s^{p+1}` near 0 and `s^{p−2}` near ∞. `ENVELOPE` decides convergence exactly for rational `p`. On dyadic-power shells
the two pieces are geometric series with ratios `2^{−q(p+2)}` and `2^{q(p−1)}`, where `q` is the denominator of `p`.
Both ratios are `< 1` precisely on `−2 < p < 1`. At `p = −2` and `p = 1` every shell contributes at least `1/2`. So
"integrable precisely for −2 < p < 1" is exact. It concerns this envelope only. The note does not infer divergence at
`p = −2` from it (lines 141–143), and §3 below supplies the lower bound.

**Separated pairs.** On `δ ≥ η_0` the weight `δ^p` is bounded for either sign of `p`, and [RC] Lemma 5 gives
`O(r⁶)`. After division by `r^{5+p}` this is `O(r^{1−p}) → 0` because `p < 1`. Correct.

**Fixed Borel `E`.** This is RP's argument: truncate `s, t`, remove `1_E(x + rse)` by `L¹` continuity of torus
translations, and control the tails by (I10). It stays valid with the unbounded weight at `s = 0`, because the
truncation is to compact `s`-ranges `[s_0, S_0]` and the envelope is integrable on `(0, s_0)`.

**Constant.** (I11) is checked exactly on instances where `(k/|t|)^{1/3}` is a perfect power, for
`p ∈ {−7/4, −3/2, −1, −1/2, −1/3, 0, 1/3, 1/2, 3/4}` (`OVERLAP`). The rest of the chain is also checked:
- (I11) times `36t²` gives the numerator `108`;
- `12^{(p+2)/3}·12^{(4−p)/3} = 144`, so `108·12^{−(4−p)/3} = (3/4)·12^{(p+2)/3}`;
- at `p = 0`, (I8) reduces to RP's `(3/40)12^{2/3}` (`COEFF`).

The `T`-exponent `(4−p)/3` lies in `(1, 2)`, so there is no singularity at `T = 0`. Tonelli on `|t| > η` is the right
way to handle it.

## §2 — the fixed-`r` gradient-only frame (§3)

**Jacobian.** `(∇f(x), ∇f(x')) ↦ G_δ = (∇f(x), (∇f(x') − ∇f(x))/δ)` has `|det| = δ^{−d}`. RC's height-divided map
(4.1) has `|det| = δ^{−d−3}`, and `dy' = δ³dt` returns it to `δ^{−d}`. All three facts are checked on exact matrices
for d = 2…6 (`LEDGER`). The two frames therefore agree where both apply. Integrating RC's `t` over all of `ℝ` at
fixed `r` recovers the gradient-only density. The note is right that reusing `δ^{−d−3}` without the `dy'` factor would
be wrong. A mutant that does so breaks the radial power (`height-jacobian`).

**Floor.** `G_δ` is literally the first two blocks of RC's `V_δ`. So `(U_r, G_δ, f(x))` has a principal-submatrix
floor `≥ c_1 I` from [RC] Lemma 1, for all `0 < r ≤ r_1` and `0 ≤ δ ≤ η_0` (note N1).

**(I13)/(I14).** On `∇f(x) = ∇f(x + δe) = 0`, the Taylor expansion gives `0 = δH_x e + (δ²/2)D³f[e,e,·] + O(δ³)`,
and the other endpoint follows from `H_{x'}e = H_x e + δD³f[e,e,·] + O(δ²)`. Congruence by `diag(δ^{−1/2}, I)` gives
`diag(∓T/2, A)`. `|det|` is continuous everywhere with polynomial Lipschitz bounds, so the coupled `L^a` limit
`(T²/4)(det A)²` follows without inverse Hessians.

On the explicit fields `f(u,v) = (T/6)u³ − (T/4)δu² + ½vᵀAv + (u² − δu)c·v` in d = 2, 3, 4, `PAIR` checks the exact
identity

    det H_x · det H_{x'} = −δ²[(T²/4)(det A)² − δ²q²],   q = cᵀadj(A)c,

so the error in (I14) is `O(δ²)` there. The a priori bound also holds exactly on these fields:
`|H_x e|_∞ = (δ/2)·max|D³f|`, and `det(H)² ≤ |He|²‖H‖_F^{2(d−1)}`.

**One height indicator.** Given zero gradients, RC's trapezoid identity gives `f(x') − f(x) = δ³D3_δ`, with
`|D3_δ| ≤ ‖f‖_{C³}/12`. On the explicit field the gap is exactly `−Tδ³/12`. For an interval of length greater than
the gap, the set of `y` with `y ∈ I_r` but `y + gap ∉ I_r` has measure exactly `|gap|` (checked). The two indicators
therefore differ only when `f(x)` lies within `O(δ³‖f‖_{C³})` of an endpoint of `I_r`. The floor bounds the
conditional density of `f(x)` given `(U_r, G_δ = 0)` uniformly, and Hölder with the determinant moments finishes the
step. The width `kr³` is fixed and positive throughout this limit, as the note says. A mutant with gap rate `δ²` is
rejected (`merge-rate`).

## §3 — Theorem II: positivity, the radial power and the threshold (§4)

**Kac–Rice at fixed `r`.** Summing [RC] (3.1) over index pairs and integrating the heights (Fubini, with the
nondegenerate joint density for `x ≠ x'`) gives the gradient-only form. Its intensity is `K_r(x, x+δe) =
δ^{−d}p_{G_δ}(0)E[W_r|det H_x det H_{x'}|1 1 | G_δ = 0]/Z_r`. By §2, `δ^{d−2}K_r → c_r` of (I15), uniformly on
compact `(x, e)`, with the dominating bound `C_r` from the segment estimate. The weight `W_r` enters once and `Z_r`
once. Exhaustion away from the diagonal permits infinite values, as the note says.

**Positivity of `c_r`.** The listed variables are the endpoint Hessians `H_M, H_S`, the transverse block `A`, the
third derivative `T` and the height `f(x)`. Conditional on `(U_r, G_0 = 0)` they are distinct derivative functionals
at the three distinct sites `M`, `S`, `x`: orders 0, 1, 2 (`He` and `A` exhaust `H_x`) and 3 at `x`, and orders 0–2
at `M`, `S`. By [RM] §2, with every Fourier weight positive, they are jointly nondegenerate. `RANK` confirms the
algebraic core exactly. On polynomial spaces over `ℚ`, the whole (I15) list has full rank in d = 2 (19 functionals)
and d = 3 (31 functionals). So does the `δ > 0` frame (pins, `∇f(x)`, `∇f(x + δe)`, `f(x)`). As a negative control,
the undivided frame `∇f(x + 0·e)` loses exactly `d` ranks at `δ = 0`, which is why (I12) divides.

The open event (`H_M < 0`, `H_S` of index `d−1`, `f(x)` inside `I_r`, `det A ≠ 0`, `T ≠ 0`) has positive
probability, and the integrand `W_r T²(det A)²` is positive on it. So `c_r > 0`. Compactness gives `0 < J_r < ∞` for
`|E| > 0`.

**All-index sum.** The positive coefficient `T²/4` comes from adjacent-index pairs. RP's same-index control
(`T = 0` with a mixed cubic) gives a product `c⁴δ⁴`, which vanishes at order `δ²`. The note is right that the all-index
sum is essential and that no same-index threshold follows (lines 79–81).

**Radial power (I16).** `(d − 1) − d + 2 = 1` for every d (`LEDGER`). The translated indicator is removed by
`sup_{|h|≤δ}‖1_E(·+h) − 1_E‖₁ → 0` against the bounded limit `c_r`. This proves (I3) with (I17).

**Threshold (I4).** On `(0, δ_r)`, `(J_r/2)δ ≤ j_r ≤ (3J_r/2)δ`. The domination already gives `j_r ≤ C_r δ` on
`(0, η_0)`, and separated pairs are bounded. So `M_p(r) < ∞` iff `∫_0 δ^{p+1} < ∞`, which is iff `p > −2`. Necessity
comes from the positive lower bound, not from the failure of an upper envelope. This is the step the offer asked to
be checked, and it is sound.

**Cutoffs (I5).** Integrating `δ^{1−q}(J_r + o(1))` and sending `ε → 0` before `ε_1 → 0` gives `J_r log(δ_0/ε)` for
`q = 2` and `J_rε^{2−q}/(q−2)` for `q > 2`. `CUTOFF` checks the algebra on a model density `δ(J + aδ)`. See note N3
on the remainder.

## §4 — contact matching (§5)

(I18) is the height disintegration of (I15). Put `h = b − kr³θ`, so `dh = kr³dθ`. The frame
`(U_r, ∇f(x), H_x e, f(x))` is the `δ = 0` subvector of [RC] Lemma 1, so its floor is uniform through `r = 0`. Under
these extra observations, [RM] §4's endpoint identities give `W_r/r² → w_0`. This is the extra-conditioned limit
already accepted for RP §4. It is not the unconditioned D1 normalizer limit. Separately, `Z_r/r² → z_0` holds, and
`Z_r` is not replaced. Dominated convergence yields `c_r/r³ → (k/(4z_0))p_{Y|Q_0}(0,0,b)·E[w_0T²(det A)²|Y]`
uniformly on compact sets. Hence `J_r/r³ → J_0 > 0`.

The r-power is 3 by both routes: `r³` from the window with `W/Z ~ r⁰`, and `5 − 1 − 1` from `j_r(rs)r ds =
r⁵A_0 g_S(s) ds` combined with `g_S(s) ~ (J_0/A_0)s` (`LEDGER`). This consistency of the iterated limits is a check.
It is not a joint limit, and the note claims none (lines 290–292).

## §5 — Theorem III (§6)

(I20) follows from RP's limit integrand. Integrating `z` gives `(k − s³|t|)_+`, and `Ψ_E` collects the `t`-density
and the conditional expectation. Its normalization `∫g_S = 1` is exactly `36·(3/10) = 54/5 = (3/40)·144` (`COEFF`).
As `s ↓ 0`, `(k − s³|t|)_+ ↑ k` monotonically, so `g_S(s)/s → (36k/(z_0A_0))∫t²Ψ_E`. With `T² = 144t²`,
`J_0 = (k/(4z_0))·144∫t²Ψ_E`, and `144/4 = 36` gives (I21). Integrating then gives the `ε²/2` in (I6). A mutant
dropping the half is rejected (`cdf-half`).

For `0 < q < 2`, `E[S_r^{−q}] = r^qM_{−q}(r)/M_0(r) → A_{−q}/A_0` by Theorem I at `p = −q` and `p = 0`. The Tonelli
identity `A_p = A_0∫s^p g_S ds` holds with matching prefactor `108/((p+2)(p+5))` (`COEFF`). The note is right that TV
convergence alone does not transfer an unbounded inverse moment: `SCOPE` exhibits a family with TV distance `1/n` and
an added `q = 1` inverse moment of `n`. For `q ≥ 2` both expectations are infinite: at finite `r` by Theorem II, and
in the limit by (I21).

**Abelian cross-check.** (I8) and (I19) are computed independently. They must satisfy `(p + 2)A_p → J_0` as
`p ↓ −2`, because `∫s^p g_S ~ (J_0/A_0)/(p+2)`. At `p = −2` the rational prefactor of `(p+2)A_p` is
`3/(4·3) = 1/4`, the `k`-power is `1` and the `T`-power is `2`. These are exactly (I19)'s `k/(4z_0)` and `T²`.
`COEFF` checks this, and the `contact-quarter` mutant (`1/2` in (I19)) is rejected. The note does not state this
identity. It is a consequence, recorded here as a consistency certificate for the two constants.

## Notes

- **N1 (simplification).** The fixed-`r` floor paragraph (lines 158–166) is correct, but it is not needed for the
  floor: `(U_r, G_δ, f(x))` is a principal subvector of [RC] Lemma 1's frame, so its floor is uniform in
  `0 < r ≤ r_1` as well. The genuinely new support input is the positivity list of (I15). The phrase "three distinct
  sites" covers `δ = 0`. For `δ > 0` the frame has four sites, which is [RC] Lemma 1 step 2. "Sufficiently small `r`"
  in Theorem II can be read as `r ≤ r_1` of [RC] Lemma 1, with `η_0 ≤ ρ/2`. `J_r` and `δ_r` depend on `r`.
- **N2 (wording).** Line 99 gives `(4−p)/3 > 1` as the reason there is no `T`-singularity. What is needed is
  `(4−p)/3 > 0`; on the domain the exponent lies in `(1, 2)`. Harmless.
- **N3 (no bounded remainder).** The `o(1)` in (I3) has no rate. So the `q = 2` case of (I5) is an asymptotic
  equivalence only, and `I_2 = J_r log(δ_0/ε) + O_r(1)` does not follow. The note writes `~` correctly. This note is
  here so that downstream text does not read a bounded remainder into it.
- **N4 (exclusions are needed).** `SCOPE` gives an exact family `g(r,δ) = J_0 + h(δ/r^{10})`, with
  `h(u) = u/(1+u²)`. Both iterated limits of `g` equal `J_0`: fixed `r` with `δ → 0`, and `δ = rs` with `r → 0`. Yet
  the coupled cutoff `δ = r^{10}` sees `J_0 + 1/2`. So a coupled `ε(r)` statement cannot follow from (I3)+(I6)+(I19)
  alone, as line 75 says. The TV example in §5 shows that (I7) needs the weighted domination.
- **N5 (novelty boundary).** Short-range correlation and adjacent-index attraction of critical points in the
  unconditioned isotropic setting are prior work (Azaïs–Delmas, arXiv:1911.02300), as RECONNAISSANCE.md records. What
  this review accepts is the pinned, tilted, fixed-`ρ`, fixed-`E` statement at existential scope: the sharp power-two
  threshold with its positive fixed-`r` coefficient, the negative moments `−2 < p < 1`, and the contact matching.

## What this review does not do

- It does not review C4 (`REMOTE_DISTANCE_MOMENTS.md`) or credit its `p = 1` transition or upper tail. The note
  consumes neither.
- It accepts no coupled-cutoff limit, same-index threshold, event-conditioned pair law, `p ≥ 1` r-asymptotic,
  uniformity as `ρ → 0` or over oscillating `E_r`, or numerical constant.
- It changes no register.

## Reproduce

    python -B -S inverse_review_check.py            # prints RESULTS.json byte for byte
    python -B -O -S inverse_review_check.py         # identical
    python -B -S inverse_review_check.py --mutant M # exit 1 for each of the 7 mutants
