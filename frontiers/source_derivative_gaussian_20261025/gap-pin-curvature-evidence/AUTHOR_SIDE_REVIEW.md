# SourceGapPinCurvature exact-source/spec review

26 October 2026. **PASS for the reviewed source/spec alignment; no findings.**
Scientific effect: **NONE**. This is a fresh read-only source/spec-quality review,
not scientific acceptance or a provider-distinct review.

Review principal: **Dylan Roy — delegated AI review**. Actual performer:
OpenAI/Codex, `/root/gap_pin_curvature_source_review`, nonauthor of this new
source, same provider family as its producer. Organizational/provider-distinct
independence credit: **0**. Dylan's personal reading: **PENDING**; this is not an
approval queue.

## Exact reviewed identity and evidence reuse

Reviewed file:
`/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceGapPinCurvature.lean`.
Frozen source SHA256
`67f6c671e4ed8a7cb8557fc6027403f4fd1e94cba984e672eaa3ceb94ab8847e`,
13,281 bytes. The producer personally confirmed no future production edits are
planned. Identities below are transcribed from the producer's existing records;
this reviewer did not recalculate hashes.

- `../gap-pin-curvature-construct/FROZEN_SOURCE.json`: frozen at
  `2026-10-26T09:47:28.162822+00:00`; object SHA256
  `00378503fe93cca757712046d9c6818296880b5524d7c0096f87794c2657eb2c`,
  467,776 bytes.
- `../gap-pin-curvature-construct/runs/compile-002/receipt.json`: the strict
  warning-as-error compilation exited 0, with the same source and object
  identities before/after and an empty diagnostic log.
- `../gap-pin-curvature-construct/runs/kernel-001/receipt.json`: the producer's
  named own-module kernel invocation exited 0 on the same source/object
  identities; the diagnostic log is empty. This review did not invoke a kernel.
- `../gap-pin-curvature-construct/runs/inventory-001/{receipt.json,output.log}`:
  the existing module-index inventory exited 0 on those unchanged source/object
  identities. Its complete ten-constant result is classified below.
- `../gap-pin-curvature-construct/runs/controls-002/receipt.json`: the existing
  positive-control compile exited 0 on those unchanged source/object identities.
  This reviewer read the receipt and did not run or independently re-audit the
  producer's controls.

The workspace owner clarification in `/workspace/AGENTS.md` was read and applied:
completed applicable verification is reusable, a new reviewer/handoff does not
justify replay, and provider-distinct process obligations remain separate from
established mathematics. The qualified 38-module/32-input slice, existing Peano
identities, derivative majorants, determinant arithmetic and strict-type
arithmetic are reused. The uncovered obligation here is alignment of this new
interface/composition with its frozen specification. No builds, tests, kernels,
controls, axiom audits or hash campaigns were run by this reviewer. No source,
configuration, cache, commits or external posts were changed. Only this report
was created.

## Binding material read

- `/workspace/AGENTS.md`, the repository `AGENTS.md` and `README.md`.
- The canonical local copies of the standing mandate, delegation and current
  workflow, with their onboarding links carried below.
- PRECODE commit `c47964f89d819dde79019b0ac544dc9b4bfd710c`,
  `SOURCE_GAP_PIN_CURVATURE.md` and `SOURCE_GAP_PIN_CURVATURE_PLAN.md`, read via
  `git show`, and the corresponding current files.
- `../actual-fold-cutoff-probability-preflight/REPORT.md`, especially item 1 at
  lines 143–159.
- The complete new source, and bounded existing-source interfaces needed to
  assess its literal carrier, weight, targets and composition. These interface
  reads are not renewed verification of the old proofs.
- The producer's frozen control contract, freeze record and existing execution
  receipts cited above.

## Source/spec alignment

All line references in this section are to the frozen new source unless a file
is named explicitly.

1. **Direct first-four bounds, no sixth pin.** Lines 28–64 use only `hL`, a
   nonzero radius, and zero confluent rows 3 and 4. The proof obtains actual
   bounds on `iteratedDeriv 3 (sourceF L sample)` and
   `iteratedDeriv 2 (sourceH L sample)` from the qualified third-derivative
   majorant (35–41), applies the existing left/right affine weighted integral
   estimates with center zero (42–49), and rewrites the exact
   `source_normalized_peano` identity (50). The four cases retain the correct
   left minus/right plus signs and yield the stronger bound `Gamma_3/2`.
   The imported weighted integral interfaces use nonnegative Peano weights and
   their exact half masses (`SourcePinCurvatureBounds.lean:133,146`). Lines
   67–77 weaken this to the original `sourceGammaRadius`. No `pin5=2`, positive
   gap, birth height or radius cap enters. Allowing all nonzero r here is a
   valid strengthening of the requested positive-radius interface.

2. **Pin-free transverse errors.** Lines 80–100 require only `hL` and `0≤r`.
   They use the actual `sourceQCurve_lipschitz` and its value at zero, then
   evaluate the two literal endpoints `-r/2` and `r/2`. The existing half-scale
   Lipschitz estimate is conservatively weakened to `r*Gamma_3`. No pin equation
   or target normalization is consumed.

3. **Literal determinant factors and q-sensitive physical weight.** Lines
   103–119 apply the qualified determinant arithmetic to the actual normalized
   endpoint entries. Lines 122–134 rewrite `sourceSmoothWeight_eq` and apply
   `endpointWeight_curvature_le`, giving exactly
   `W ≤ 2*r^2*Gamma^2*q^2 + 8*r^4*Gamma^4`. The only pin hypotheses are rows
   3 and 4. `SourceSmoothPalm.lean:132–147` defines the original endpoint
   Hessians, strict maximum/saddle indicator and absolute determinant product;
   its lines 163–167 establish the exact weight equality used here. There is
   no replacement weight, hidden scaling, alternate period or framed carrier.

4. **Pin-free strict upper curvature and slab.** Lines 137–147 derive the
   negative transverse maximum entry from positive literal weight and actual
   strict type, then combine it with the independent transverse error. The
   conclusion is `q < r*Gamma_3`. Lines 150–157 use the qualified scalar slab
   arithmetic to give `|q| ≤ max A 1*r*Gamma^5`, with `A : ℝ` and the one-sided
   lower obstruction visible. Neither theorem assumes pins, a positive gap,
   a birth height or `r≤1`. No positivity condition on A is silently required.

5. **Useful coarse physical bound.** Lines 160–179 require `0<r≤1` and only
   rows 3 and 4. The proof derives `q²≤Gamma²` from the actual second derivative
   majorant, uses `r⁴≤r²`, and obtains exactly `W≤10*r²*Gamma⁴`. The unit-radius
   cap is used in this arithmetic and is absent from the sharper estimate.

6. **Every literal zero-row target.** Lines 183–210 quantify an arbitrary
   six-vector p with only `p 3=p 4=0`. Current covariance invertibility is a
   genuine premise of this general kernel helper. The proof derives all-target
   pin support from the actual `sourceSmoothKernel_pin_fiber` and measurable
   fiber, then derives the pointwise estimates. Endpoint estimates and support
   certificates are conclusions, not desired-bound premises. Slots 0,1,2,5
   remain unrestricted.

7. **Closed actual-gap law, correct quantifiers.** Lines 214–226 have only
   `hL : L≠0` as model input. A single positive `δ≤1` is chosen before r,b,k;
   all real b,k are quantified after every `0<r<δ`. Lines 227–235 obtain the
   interval and current invertibility internally from
   `sourceInverse_target_uniform_bounds hL`, instantiate the all-target helper,
   and discharge both zero rows by the literal gap target. The output includes
   the full equality `sourceConfluentPinsAt ... = sourceGapPins r b k`.
   `SourceCompactTargetMoments.lean:150` defines this target literally as
   `![b-k*r^3/2,0,0,0,0,12*k]`, so its slot-5 conclusion is `12*k`, not 2.
   The gap law is the actual posterior kernel at that target (same file:153–154)
   and has the qualified every-target raw lift (174–177). No final `IsUnit`,
   raw-pin certificate, endpoint-bound certificate or desired estimate is a
   premise. The slab threshold A remains explicitly quantified in the output.
   Every carrier and derivative retains the same original L. The signature
   allows negative L and k=1, as well as nonpositive k.

8. **Scope remains narrow.** The source makes no normalized weighted
   probability, compact positive normalizer floor, all-target residual-moment,
   r^5 numerator, count-density, framed-law, canonical-pair or Parent closure
   claim. Its single import is the requested narrow `SourceCompactTargetMoments`.
   No old export is changed.

## Declaration classification

The source contains exactly ten handwritten declarations, all public theorems
in namespace `I4SourceGapPinCurvature`. There are no handwritten definitions,
private declarations, structures, instances or axioms.

| Line | Public handwritten theorem | Research role |
|---|---|---|
| 28 | `source_normalized_first_four_third_bound` | Direct Peano/third-majorant endpoint interface |
| 67 | `source_normalized_first_four_bound` | Original-radius endpoint interface |
| 80 | `source_normalized_transverse_errors` | Pin-free actual transverse error interface |
| 103 | `source_normalized_determinant_bounds` | Physical determinant-factor estimate |
| 122 | `sourceSmoothWeight_curvature_bound` | Exact q-sensitive physical weight estimate |
| 137 | `source_positive_weight_curvature_upper` | Pin-free strict-type curvature consequence |
| 150 | `source_bad_curvature_slab` | Pin-free one-sided-to-symmetric slab consequence |
| 160 | `sourceSmoothWeight_radius_bound` | Unit-radius coarse physical weight estimate |
| 183 | `sourceSmoothKernel_curvature_bounds_ae` | Every-target zero-row support/composition helper |
| 214 | `sourceGapLaw_curvature_bounds` | Closed all-real-height/all-real-gap actual-law endpoint |

The producer's existing `runs/inventory-001/output.log` enumerates the actual
owned-module index and reports `COMPLETE_NEW_MODULE_INVENTORY|SourceGapPinCurvature|10`.
Its ten names exactly match the ten source theorems above. Thus the exhaustive
classification is: **10 public handwritten theorems; 0 private declarations;
0 generated declarations; 0 definition declarations; 0 axiom declarations**.
For each of the ten, the existing transitive axiom output is exactly
`[propext, Classical.choice, Quot.sound]`. This reviewer read and reused that
producer inventory; no inventory, elaboration or axiom audit was regenerated.

## Disposition and handoff

No source/spec alignment findings. PASS applies only to the exact frozen source
identity above and the unchanged qualified dependency slice. A future change to
the reviewed source, hypotheses or consumed dependencies requires assessment
limited to the affected scope. This report supplies same-family technical
review only. The separate provider-distinct alignment process remains separate
and earns no credit from this report; it does not invalidate the established
mathematics. Producer qualification/control requirements and root publication
requirements retain their own evidence and ownership.

Canonical authority links carried forward:

- [15 October 2026 standing mandate](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md)
- [Standing owner delegation](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md)
- [Current workflow](https://github.com/d6g8k5htny-coder/main/blob/main/governance/OP-WORKFLOW-20260930.md)

These links establish availability, not a future recipient's personal reading.
