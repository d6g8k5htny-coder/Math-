# Frozen actual-fold torus source/specification review

Disposition: **PASS**, for the frozen source and the clarified H0-free interface.
No blocking source or specification findings remain.

Reviewer: OpenAI / GPT-6 family / Codex subagent
`/root/torus_source_review_recovery`. This is a same-family technical review,
not a separately authenticated provider-distinct scientific/alignment review.
Scientific effect: **NONE**.

## Identity and scope

- Source: `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceActualFoldTorus.lean`.
- Frozen SHA-256: `d2ca01d1f881852372c371215c30216bee7d917fdf2eaafbbd097f8c840e20c6`.
- Source size in the completed execution receipts: 17,840 bytes.
- Completed source object SHA-256: `9dd9d93e12ddb685ece1348b0699045b7e57b362cb48eaa54ac4373ddb9fd6e9`.
- Specification: `SOURCE_ACTUAL_FOLD_TORUS.md`; implementation plan:
  `SOURCE_ACTUAL_FOLD_TORUS_PLAN.md`, in the same source directory.
- Read-only source/specification/quality review. Only this assigned scratch
  report was written. No source, configuration, cache, tests, build, kernel,
  audit, commit, publication, or agent work was performed by this reviewer.

Read `/workspace/AGENTS.md` and repository `AGENTS.md`. The owner clarification
requires reuse of completed applicable verification and separates mathematical
evidence from provider-distinct review. Completed strict-003, kernel-001,
inventory-001, and controls-002 receipts and relevant retained source/control
text were inspected as existing evidence; none was rerun. Accepted upstream
Cap, elder-clearance, real-cover, and source-estimate mathematics was reused.

The standing owner mandate and delegation were read from their local canonical
copies. Future handoffs must carry their canonical links:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

## Interface clarification and specification alignment

The frozen source explicitly defines `SourceActualFoldTorus.TorusTrapData`
(lines 124–135). It does not define a same-named replacement `ElderTrap`, and
its module comment reserves typed H0 `ElderTrap` conversion as a downstream
obligation (lines 4–6). The old `TorusFiltration.ElderTrap` is defined in
`frontiers/asymmetric_elder_bridge_20261017/ElderInterval.lean:104`, whose
first import is `OrdinaryH0`; it is outside the qualified H0-free
`inputs/elder/ElderClearance.lean` branch.

The initially inspected spec/plan still used the old type name in their stated
goal. Root corrected only that documentation during this review. The changed
spec lines 32, 46, and 77–89, and plan lines 3 and 28–32, now explicitly select
the H0-free `TorusTrapData` bundle and leave old typed conversion/H0 downstream.
The clarification records root's reported 06:35 ruling before the source and
states that the wording correction was recorded after interruption; this review
does not independently authenticate the ruling's timestamp or claim that the
documentation commit predated the source. The clarified mathematical interface
matches the frozen source; no source change or mathematical weakening was
needed to resolve the wording issue.

## Source review findings

1. **Literal sample, period, field, and carrier: PASS.**
   `actualTorusField` consumes `SmoothSample 2 L`, returns a function on
   `I4Torus.SourceTorus 2 L`, and evaluates the same
   `smoothSourceField 2 L sample` at a selected lift (lines 34–38).
   Exact pullback uses the accepted fiber-respect theorem on
   `sampleInclusion 2 L sample` (lines 40–49). There is no substitution by
   `abs L` and no `Fact (0 < L)` premise. Projection continuity, openness,
   surjectivity, and T2 are provided for arbitrary `L` (lines 15–32);
   the field descent and continuity require exactly `hL : L ≠ 0`
   (lines 41–63). Thus negative original periods are included.

2. **Physical map and quotient topology: PASS.**
   The map is literally `torusProjection 2 L (r • ![p.1,p.2])`
   (lines 65–67). Its continuity and openness are composed from quotient
   projection facts and the existing physical/coordinate equivalence
   (lines 69–100). The compact image is closed in a T2 target
   (lines 176–177, 206). The frontier bound uses only the accepted compact-image
   inclusion `CapFirstExit.frontier_image_subset`, continuity, openness,
   compactness, and the normalized frontier bound (lines 178–183).
   No global injectivity, local inverse, frontier equality, quotient
   homeomorphism, or extra `r < |L|/8` hypothesis is used.

3. **Same witness, absolute levels, and physical scale: PASS.**
   The physical endpoint identities use the original `endpointM r` and
   `endpointS r` (lines 221–232). Exact pullback has amplitude `6*k*r^3`
   with no removed offset (lines 234–241); the accepted definition of
   `actualFoldPotential` divides the entire original field by that amplitude
   (`SourceAdaptiveFoldChart.lean:192–194`). The raw pin event supplies
   absolute maximum `b` and saddle level `b-k*r^3` (lines 245–268), rather
   than only their difference. The normalized gain `a/4` becomes exactly
   `(3/2)*k*r^3` (lines 269–280). The same retained rectangle's path is mapped
   once through `γ.map he`, preserving its floor and saddle midpoint
   (lines 193–214, 281–284). The closed actual-law endpoint obtains one
   `U,z` and passes that same `z` and rectangle/path data into this transport
   (lines 327–331). Older exclusion follows from the derived height ceiling
   and strict height gain (lines 188–192, 208), without injectivity.

4. **Explicit geometric data and strict clearance: PASS.**
   `TorusTrapData` records actual closed domain, inside/outside endpoints,
   absolute heights, ceiling/frontier bounds, strict trace, and an actual
   closed-level path; it has no clearance equation, death equation, partner,
   or homology field (lines 122–135). Construction derives its clopen trace
   from closedness and frontier bounds using the accepted old theorem
   (lines 200–213). The new generic predicate quantifies over a strictly
   higher endpoint and an actual path strictly above `h` at every parameter
   (lines 109–115), and agrees definitionally with C263 on its original
   Euclidean carrier (lines 117–120). The accepted arbitrary-space threshold
   theorem gives the forward inclusion; the actual path floor `d ≤ g(γ t)`
   gives all `h < d` in reverse (lines 137–152). Consequently the set is
   exactly `Iio d`, excluding `d`; real `sSup` is exactly `d`
   (lines 154–158). Strict clearance has not been replaced by closed
   clearance, and no optimal path is inferred merely from a supremum.

5. **Closed original-law quantifiers and premises: PASS.**
   The final endpoints quantify one `0 < δ ≤ 1` from `hL` before
   `k₀,r,b,k`; retain the literal `sourceGapLaw hL r b k` and the qualified
   `sourceT`/`sourceKappa`; and require only `k₀ > 0`, `0 < r < δ`,
   `k₀ ≤ k` and the two displayed numeric sample cutoffs
   (lines 286–311, 333–345). The proof takes the minimum of the hL-only
   estimate and inverse intervals and derives invertibility and the raw pin
   event internally (lines 312–327). Desired pin, unit, trap, path, clearance,
   death, regularity, global-injection, and Morse certificates are not final
   endpoint premises. The theorem asserts no probability of the cutoffs.

## Declaration classification

The source has 19 public authored theorems, one private chart-identity lemma,
four definitions, and one structure. The completed exhaustive module-index
inventory contains 50 constants, including 25 generated constants; generated
projections/constructors/recursors/equation/simp constants must remain inventory
entries rather than being promoted into additional research theorem targets.

| Class | Source declarations and lines |
|---|---|
| Quotient topology support | `torusProjection2L_continuous` 16; `torusProjection2L_open` 21; `torusProjection2L_surjective` 27; `sourceTorus2L_t2` 32 |
| Literal descent/physical support | `actualTorusField_pullback` 41; `actualTorusField_continuous` 52; `torusPhysicalMap_continuous` 74; `torusPhysicalMap_open` 85; `actualTorusField_physical_pullback` 96 |
| Predicate/clearance glue | `strictClearanceSet_eq_C263` 118; `TorusTrapData.strictClearanceSet_eq_Iio` 139; `TorusTrapData.strictClearanceDeath_eq` 155 |
| Generic geometric transport | `scaled_rectangle_trap` 166 |
| Actual endpoint/scaling identities | `torusPhysicalMap_M` 222; `torusPhysicalMap_S` 229; `torusPhysicalMap_field_eq` 235 |
| Actual geometric composition | `actual_rectangle_torus` 245 |
| Closed original-law endpoints | `sourceGapLaw_actual_torus_trap_clearance` 289; `sourceGapLaw_actual_torus_clearance` 335 |
| Private support | `physicalPi_eq_chart` 69 |
| Definitions | `actualTorusField` 36; `torusPhysicalMap` 66; `strictClearanceSet` 110; `strictClearanceDeath` 114 |
| Explicit data interface | `TorusTrapData` 124 |

`inputs/elder/ReusedCompactFrontier.lean:19–29` is an unchanged accepted proof
snapshot with narrow import/composition support, not a new research target or
new proof credit. Its use here is new composition only. Source endpoints
establish actual torus geometric trap data and strict-clearance/death level;
they do not produce the old typed `ElderTrap`, an H0 summand, canonical selected
partner, conditioned global MorseDistinct, weighted cutoff/failure probability,
frame-law/isotropy, count-density, or Parent A/B closure.

## Reused completed verification evidence

All paths below are under
`/workspace/scratch/actual-fold-torus-construct/runs/` and bind the frozen
source hash and object hash recorded above:

- `strict-003/receipt.json`: warning-as-error compilation, exit 0;
  completed 2026-10-26 06:39:54 UTC, empty output log.
- `kernel-001/receipt.json`: the single named own-module `leanchecker`
  execution, exit 0; completed 06:40:31 UTC, empty output log.
- `inventory-001/receipt.json` and `output.log`: exit 0; completed
  06:40:29 UTC; exhaustive 50-constant own-module inventory, transitive
  axioms only `propext`, `Classical.choice`, `Quot.sound`.
- `controls-002/receipt.json`: warning-as-error new-interface controls,
  exit 0; completed 06:41:29 UTC, empty output log. Retained control source
  checks negative original L, nonzero b, k different from 1/6, exact pullback,
  physical amplitude, quotient-equal distinct lifts/noninjectivity,
  same-sample periodicity, reused C263 interface, sSup, and strict endpoint
  exclusion. Old physical normal-form proof evidence is consumed rather
  than replayed.

This review does not assert a new kernel/control run or authenticate any
provider-distinct review. Source-root/cache/target registration, publication,
current CI, and the separately authenticated scientific/alignment process
remain root's distinct obligations. Existing applicable mathematical evidence
remains established while those process obligations are pending.
