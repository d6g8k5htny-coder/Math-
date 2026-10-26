# All-target curvature residual: source/spec review

26 October 2026. Reviewer: OpenAI/Codex, agent
`/root/all_target_curvature_residual_source_review`. Disposition: **PASS** for
the assigned technical source/spec-quality scope. No blocking findings or
requested source changes. Same OpenAI family review; provider-distinct credit
**0**. Scientific effect: **NONE**.

## Exact object, authority and reuse

Reviewed source:
`/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceAllTargetCurvatureResidual.lean`.
Source SHA256 supplied in the root handoff and producer frozen record:
`4ae29bc3f2f206cca558df3f78853061cf4892499ac918e40253edd68d44371f`.
Own `.olean` SHA256 from those existing records:
`0a193cd6fc68ac0507169dc0a601d8f804dd51fc382d6ea86c2997715d2d245e`.
No hash was recalculated by this reviewer. Line references below identify that
source as read.

Read `/workspace/AGENTS.md`, repository `AGENTS.md`, README, formal README/scope
and required-check contract, plus the local canonical owner mandate, standing
delegation and current workflow. Read the binding
`SOURCE_ALL_TARGET_CURVATURE_RESIDUAL.md` and PLAN directly from PRECODE commit
`5141e92c22edc6a62d307e59f52dbfb2bdb1aba8`, the producer precode control contract
and freeze records, and item 2 of
`/workspace/scratch/actual-fold-cutoff-probability-preflight/REPORT.md`.

Owner instruction applied: completed applicable verification remains reusable;
new reviewer/session/handoff alone does not justify replay. Existing 38 qualified
modules / 32 inputs and their established mathematical evidence are dependencies.
The old all-target scalar/product law, density bound, shift identity and posterior
moment mathematics were not reproved or reverified. Their relevant source
interfaces were read only to assess correspondence of the new composition.
Provider-distinct process obligations are tracked separately and do not erase
completed mathematical evidence.

This reviewer ran no build, Lean, test, kernel, control, audit or hash campaign;
made no source/configuration/cache/manifest/commit/post changes; and spawned no
agents. Only this review scratch directory was written. Producer evidence cited
below was read, not regenerated.

## Statement and proof correspondence

| Obligation | Source evidence and assessment |
|---|---|
| Literal generic radius and original carrier | Lines 31–32 define `allTargetCurvatureResidualRadius hL r p ρ` as exactly `sourceGammaRadius L (posteriorSample hL r p ρ)`, with arbitrary `p : Fin 6 → ℝ` and `ρ : SmoothSample 2 L`. There is no changed carrier, recentering of p, replacement target or fixed default pin. |
| Measurability, lower bound and contact curvature | Lines 34–45 compose the existing measurable maps, use the original Gamma lower bound 1, and bound the absolute posterior contact Q by this literal S. These are pointwise every-target statements. |
| Generic reconstruction domination | Lines 47–88 bound every derivative majorant at `curvatureReconstruct hL r p ρ q`. The original reconstruction uses `q − sourceContactQ(posteriorSample p ρ)`; lines 61–62 retain and bound that term by `|q|+S`. Lines 90–104 sum these estimates to Gamma with factor `1+curvatureEnvelopeTotal L U`. No zero-mean substitution occurs. |
| Residual image | Lines 106–117 reuse the already generic `curvaturePosterior_residual_eq_shift` at the actual target p. The right side is exactly Gamma of `posteriorSample hL r p ω` plus the envelope total times `|curvatureZ L r ω|`. The minus sign of the residual shift is retained and then absorbed by absolute value. |
| Actual residual moment law | Lines 119–180 conclude integrability and a Bochner integral bound under literally `curvatureResidualLaw hL r`. Lines 168–175 use the measurable pushforward by `curvatureResidualSample` and `integral_map`; no `sourceGapLaw` or posterior law is relabeled as residual. `sourceSmoothKernel hL r p` is used only for the input posterior Gamma moment and its correct sampling identity. |
| Exact old specialization | Lines 183–186 prove by `rfl` that p=`sourcePrescribedPins r b` gives exactly the old `curvatureResidualRadius hL r b ρ`. This matches its retained definition at `SourceCurvatureDecomposition.lean:1041`. |
| Closed uniform endpoint | Lines 191–203 quantify `∃ δ A H` immediately after hL, with `0<δ≤1`, `A,H≥0`, before every r,p,ρ,q,n. Each moment constant is `∀ n, ∃ C≥0` before r,p; the actual bound is `C*(1+‖p‖)^n`. No invertibility, variance, envelope or moment certificate is an endpoint premise. |
| Internal choices are target-independent | Lines 204–220 select the covariance-direction envelope and parameter bounds at literal b=0 and the existing all-target posterior moments. Their interval minimum is independent of p and n. The extra mean bound in the parameter interface is discarded. Positive variance follows from the Schur floor; covariance invertibility is extracted internally. Lines 221–228 take A=`1+H`, H=`curvatureEnvelopeTotal L U`, with one U for all targets. |
| Polynomial growth retained | Lines 229–243 instantiate posterior moment bounds at arbitrary p and choose `C_n=2^(n−1)*(M_n+H^n*standardAbsMoment n)`. The inequality `(1+‖p‖)^n≥1` absorbs the target-independent Gaussian moment term into the polynomial factor. It does not erase target growth. |
| Natural n=0 | Every moment signature includes n=0. In lines 147–180 and 232, `n−1` is natural subtraction, so at n=0 the factor is 1, with no negative exponent or division. Both zeroth powers equal 1, `standardAbsMoment 0=1` from its existing definition, and the bound specializes to the finite constant `M_0+1`. No n>0 premise is required. |
| Literal gap targets and height growth | Lines 247–269 substitute the existing `sourceGapPins r b k`, under the same actual residual law. Delta is chosen before K,n,b,k (even independent of K); C may depend on K and n. Lines 263–269 use the existing `‖sourceGapPins‖≤|b|+13K` on r≤1 and preserve `C_n(L,K)*(1+|b|)^n`. Both signs of b and k are allowed when `|k|≤K`; no positive mark or bounded-height premise is smuggled in. |
| Signed L and import boundary | The only period assumption throughout is `hL : L ≠ 0`. The source keeps `SmoothSample 2 L` for signed L, including L=−1, and imports only `SourceCompactTargetMoments` and `SourceCurvatureDecomposition` at lines 1–2. It does not invoke a new weight/probability module or a positive-L replacement. |

The lower-level helper lemmas explicitly accept envelope/invertibility/variance
inputs as appropriate; the final endpoint discharges these internally. This
distinction is clear in the actual source. The existing interfaces consumed are
`SourceCurvatureDecomposition.lean:594–608` (actual residual law), 736–739
(literal reconstruction), 846–859 (direction envelope), 1164–1167 (generic shift
identity), and `SourceCompactTargetMoments.lean:111–116,150,180–182`
(all-target moments and literal target/norm bound). These citations identify
reused dependencies, not new verification of them.

No normalized varying-mark probability, compact normalizer floor, weighted r^5
numerator, canonical partner, conditional Morse, frame/count-density law, or
Parent Lean theorem is asserted by the new statements. Existing conventional
Parent mathematics retains its prior evidence and scope.

## Actual declaration classification

Read producer `runs/inventory-002/output.log` and its successful receipt in
`/workspace/scratch/all-target-curvature-residual-construct/`. The module-index
inventory reports **12 actual constants**. Direct source comparison gives
**11 written declarations = 1 definition + 10 theorems**, plus **1 generated
theorem**. This is an actual inventory classification, not an assumed public-name
or theorem-target count.

All names below have prefix `I4SourceAllTargetCurvatureResidual.`.

| Actual constant | Classification | Source line |
|---|---|---:|
| `allTargetCurvatureResidualRadius` | Written definition | 31 |
| `allTargetCurvatureResidualRadius_measurable` | Written theorem | 34 |
| `one_le_allTargetCurvatureResidualRadius` | Written theorem | 39 |
| `sourceContactQ_posterior_abs_le_allTargetRadius` | Written theorem | 42 |
| `sourceDerivativeMajorant_allTarget_curvatureReconstruct` | Written theorem | 47 |
| `sourceGammaRadius_allTarget_curvatureReconstruct` | Written theorem | 90 |
| `allTargetCurvatureResidualRadius_image_bound` | Written theorem | 106 |
| `allTargetCurvatureResidualRadius_moment_bound` | Written theorem | 119 |
| `allTargetCurvatureResidualRadius_prescribed` | Written theorem | 183 |
| `allTargetCurvatureResidualRadius_uniform_bounds` | Written theorem | 191 |
| `allTargetCurvatureResidualRadius_gap_height_moments` | Written theorem | 247 |
| `allTargetCurvatureResidualRadius.congr_simp` | Generated theorem associated with the radius definition | 31 |

The producer inventory's transitive axiom lists for all 12 constants contain
only `propext`, `Classical.choice`, `Quot.sound`. No axiom audit was rerun here.
No additional instances, private helper declarations, opaque declarations,
custom axioms or nonstandard implementation escape appeared in the reviewed
source or that completed inventory.

## Reused qualification and process limits

Existing producer receipts bind the same source/object identities above:
`strict-002` exited 0 in 4.730830192565918 seconds;
`kernel-001` exited 0 in 5.407623529434204 seconds;
`inventory-002` exited 0 in 3.284644603729248 seconds and reports all 12 constants.
The producer `FROZEN_SOURCE.json` records freeze preceding the named sole
own-module kernel. These are read-only observations, not additional executions
or an independent authentication of the producer's entire process.

Positive/negative control qualification, custody/registration/cache/publication,
hosted CI and separately authenticated provider-distinct alignment remain the
producer/root's separate process scopes. This source assessment does not wait
for or replace them. The precode negative arithmetic control is properly scoped
as failure of the erasure step `(1+‖p‖)^n≤1`, not as a counterexample to every
possible target-uniform moment estimate.

Canonical authority links read through their local canonical copies, carried
forward for onboarding (a link alone does not establish recipient reading):

- [15 October owner mandate](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md)
- [Standing owner delegation](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md)
- [Current workflow](https://github.com/d6g8k5htny-coder/main/blob/main/governance/OP-WORKFLOW-20260930.md)

Handoff: reuse this source/spec assessment only for these unchanged bytes,
hypotheses and consumed dependencies. Recheck only a genuinely changed or
uncovered scope. Provider-distinct review remains separate; this report supplies
same-family technical review only, with scientific effect NONE.
