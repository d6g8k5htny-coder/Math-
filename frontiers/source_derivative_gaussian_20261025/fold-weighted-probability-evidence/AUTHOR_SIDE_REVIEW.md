# SourceFoldWeightedProbability: readonly source/spec review

26 October 2026. **PASS — no source/spec alignment defect found.**

This is a fresh technical source review by OpenAI/Codex
`/root/fold_weighted_probability_source_review`, a nonproducer subagent of
the coordinating OpenAI lane. It is the same provider/family as the producer
and earns **zero provider-distinct scientific/alignment credit**. Scientific
effect: **NONE**. Provider-distinct review and scientific acceptance remain
separate requirements; this review does not alter them.

## Exact reviewed object and binding specification

- Source: `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceFoldWeightedProbability.lean`.
- Producer-frozen source SHA256:
  `58b77d6c0886fb5ef005749f468648d3c3ce6c99905f89963bf99c4ebee763d0`,
  7,837 bytes, frozen at `2026-10-26T09:46:14.325908+00:00`.
- Identity is transcribed from the assigned freeze,
  `/workspace/scratch/fold-weighted-probability-construct/FROZEN_SOURCE.json`
  and `runs/strict-003/receipt.json`; no digest was recomputed.
- Binding PRECODE commit:
  `c47964f89d819dde79019b0ac544dc9b4bfd710c`,
  `SOURCE_FOLD_WEIGHTED_PROBABILITY.md` and
  `SOURCE_FOLD_WEIGHTED_PROBABILITY_PLAN.md`. Both exact commit versions
  and the working copies were read.
- The authoritative mapping
  `/workspace/scratch/actual-fold-cutoff-probability-preflight/REPORT.md`
  was read. Its older 37-module as-of inventory is superseded for this
  assignment by the supplied completed 38-module/32-input qualification;
  this review does not reopen either inventory or the old mathematics.

The entire 163-line new source was read. The imported theorem signatures and
literal definitions necessary to assess the new composition were inspected;
their established proofs, kernel checks and controls were not rerun or
reviewed afresh. The source imports only `SourceActualFoldH0` and
`SourceWeightedCurvatureBound` (lines 1–2).

## Declaration classification and source mapping

All names below lie in namespace `SourceFoldWeightedProbability`. These
are the **19 explicitly named source declarations: five definitions and
14 theorems**. Generated/private-constant enumeration and transitive axiom
qualification belong to the producer's module-index check, not this source
classification.

| Class | Declarations and starting lines | Reviewed meaning |
|---|---|---|
| Five definitions | `sourceScale`:21; `sourceCutoffEps`:22; `sourceCutoffA`:23; `sourceFoldGood`:26; `sourceFoldWeightedLaw`:31 | Full scale, exact cutoffs, literal measurable-event carrier and actual normalized physical-weight law. |
| Three sign theorems | `sourceScale_pos`:35; `sourceCutoffEps_pos`:40; `sourceCutoffA_nonneg`:44 | Required positive scale/epsilon and nonnegative obstruction coefficient are derived. |
| Two source identities | `sourceT_eq_scale`:48; `sourceKappa_one_sixth`:53 | T=λΓ and κ=−q/r, with the entire factor eight retained. |
| Three measurability theorems | `sourceT_measurable`:59; `sourceKappa_measurable`:63; `sourceFoldGood_measurable`:67 | Borel measurability of the literal scalar cutoffs and their conjunction. |
| Two failure reductions | `cutoff_failure_inclusion`:76; `sourceFoldGood_compl_subset`:91 | Pointwise strict cutoff failure lies in the old strict regularity/closed one-sided-curvature obstruction union. |
| Two law theorems | `sourceFoldWeightedLaw_eq`:101; `sourceFoldWeightedLaw_absolutelyContinuous`:107 | Exact identification with the qualified sixth-gap weighted law and derived absolute continuity to the same actual conditional gap law. |
| Two closed endpoints | `sourceFoldWeightedProbability_bound`:113; `sourceFoldWeightedProbability_h0`:133 | Derived cubic normalized failure probability; the same bound plus weighted-a.e. actual ordinary H0, clearance and real-supremum conclusion on one coefficient-field-independent interval. |

There is no explicitly named Prop bundle or private helper in this source.
The scalar failure theorem is a genuine algebraic helper with explicit
hypotheses, not an assumed model certificate. No `sorry`, `admit`, custom
axiom, `native_decide`, `implemented_by` or Mathlib umbrella import appears
in the reviewed source. Transitive evidence is the producer's separate
qualification obligation.

## Findings supporting PASS

1. **Literal event and actual physical law (lines 26–33).** The event is
   exactly `r*T^5 ≤ 1/100 ∧ 1024*T^5 ≤ sourceKappa r (1/6) sample` on the
   original `SmoothSample 2 L`. The law is literally
   `prwMeasure (sourceGapLaw hL r b (1/6)) (sourceSmoothWeight L r)`.
   The imported `sourceSmoothWeight` remains the actual strict
   maximum/saddle endpoint determinant weight (`SourceSmoothPalm.lean`:145).
   `sourceGapLaw` is the actual posterior at the literal six-vector target
   (`SourceCompactTargetMoments.lean`:150–154). There is no surrogate law,
   changed carrier, potential-rescaled weight or desired-probability premise.

2. **All scale and sign factors (lines 21–23, 35–57).** With
   `D=max 1 (1/(6*k₀))`, the source uses `λ=8*D`,
   `eps=1/(100*λ^5)` and `A=1024*λ^5`. It derives the required signs and
   `sourceT=λ*sourceGammaRadius`. Specialization of the actual kappa
   denominator `6*k*r` to `k=1/6` gives `−q/r` exactly. In particular,
   the probability reduction retains `8^5`; it does not use the smaller
   D-only coefficients.

3. **Strict/closed failure direction (lines 76–99).** Failure of the
   first closed good cutoff yields `eps < r*Γ^5`. Failure of the second
   yields `−A*r*Γ^5 < q` after multiplication by the assumed positive
   radius; weakening that to `−A*r*Γ^5 ≤ q` gives exactly the existing
   closed `sourceCurvatureOneSided` set. Only the required inclusion
   `Gᶜ ⊆ regularityBad ∪ curvatureOneSided` is claimed. Boundary points
   in the closed obstruction need not fail G, and no reverse inclusion is
   used. The positive-r assumption appears explicitly in both reduction
   theorems.

4. **Measurability and normalized cubic endpoint (lines 59–72, 101–127).**
   G is an intersection of two measurable scalar inequalities, requiring
   no ridge/older-point selection. The law identity uses the established
   literal `sourceGapLaw_one_sixth` equality. The endpoint invokes
   `sourceWeightedCurvature_bound` only with `hL`, fixed b, the derived
   A/eps and their signs. Probability, C≥0, δ>0, δ≤1 and the cubic union
   bound are obtained internally from that theorem, and measure monotonicity
   gives the desired complement bound. No moment, density, numerator,
   normalizer floor or desired cutoff-bound certificate is a premise.
   C and δ are outside the radius quantifier and may depend on L,b,k₀.
   The displayed `_hk₀` positivity input is unused by this probability
   composition, which is harmless and does not weaken its stated scope.

5. **Same-law weighted AE transport and one H0 interval (lines 107–109,
   133–161).** Absolute continuity is derived directly from the generic
   with-density property of `prwMeasure` to the exact
   `sourceGapLaw hL r b (1/6)`, not assumed and not transported to another
   posterior. The established closed `sourceGapLaw_actual_torus_h0`
   endpoint (`SourceActualFoldH0.lean`:115) supplies δH and the actual
   ordinary singular-H0 splitting and clearance. The new radius is
   `min δP δH`, positive and at most one, chosen before r and K. Its
   almost-everywhere implication is transported by absolute continuity;
   G's two literal conjuncts discharge exactly the old numerical premises.
   The only normalization of the gap is the proved arithmetic equality
   `(1/6)*r^3 = r^3/6`. The conclusion is the actual functor isomorphism
   with a complement, `elderInterval K b (b-r^3/6)`, exact clearance set
   `Iio (b-r^3/6)` and death `b-r^3/6`. `elderActive` has closed birth and
   open death (`inputs/elder/ElderInterval.lean`:24), hence its increasing
   parameter interval is precisely `[-b,-(b-r^3/6))`.
   `strictClearanceDeath` is literally the real `sSup` of the explicit
   strict-clearance set (`SourceActualFoldTorus.lean`:114–115).

6. **Quantifiers and honest scope (lines 4–7, 113–147).** The probability
   endpoint allows fixed k₀>0; the H0 endpoint adds k₀≤1/6 as required by
   the old geometry. L has only the original nonzero-period hypothesis,
   so negative original L remains allowed. The actual torus field and
   point retain that same L; the existing quotient uses the original
   period and supports either sign. The interval works before the
   coefficient field K is selected. This does not assert a single common
   null set simultaneously for every field. There is no compact-height
   or varying-k uniform normalized theorem, canonical selected partner,
   conditional Morse theorem, exhaustive barcode, frame/translation law,
   weighted count-density theorem or Parent A/B Lean claim. No existential
   geometric/selector event is assigned a probability.

## Verification reuse and remaining process

The workspace owner clarification in `/workspace/AGENTS.md` was read and
applied. Completed applicable verification is reusable; a handoff alone is
not a reason to repeat unchanged checks. Existing weighted-curvature,
normalizer, all-target density, torus and H0 mathematics is reused. This
review addresses only new literal event/law identification, scalar reduction,
quantifier order and AE composition. It ran **no Lean compile, build, kernel,
control, audit or hash campaign**, and spawned no agents.

The producer's existing `runs/strict-003/receipt.json` records warning-as-error
compile exit 0, 4.799805164337158 seconds, the same frozen source SHA above,
and object SHA256
`3c5e59ee676f589de711731c6b414d54c2ee41f819cd0418593fd594e6eaaff7`.
This is reused execution evidence, not a new reviewer run. The pre-source
`CONTROL_CONTRACT.md` was read; its new-only controls cover the original
negative period, actual law/endpoint, scale `λ=16`, substantive strict/closed
arithmetic and the counterexample-backed sole-False mutation. The producer
retains sole ownership of its one named own-module kernel, exhaustive
module-index transitive standard-three/classification check and controls.
Their final outcomes must be taken from the producer's records; no such
outcome is inferred or replaced by this PASS.

Only this report was written, under the assigned scratch directory. No
source/config/cache, repository metadata, commit or external post was changed.

Authority read: repository AGENTS, README, formal README/SCOPE and required
formal-check contract, plus the local canonical mandate, delegation and
workflow copies. Required canonical handoff links:

- [15 October standing mandate](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md)
- [Standing owner delegation](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md)
- [Live workflow](https://github.com/d6g8k5htny-coder/main/blob/main/governance/OP-WORKFLOW-20260930.md)

These links establish availability, not a future reader's acknowledgment.
Retain the completed verification evidence and the owner's reuse instruction
in subsequent handoffs. This technical PASS supplies no provider-distinct
scientific credit and changes no scientific-status register or acceptance.
