# SourceGapWeightedNumerator exact-source/spec-quality review

Verdict: **PASS — no source/spec amendments requested.**

Performer: OpenAI/Codex, `/root/gap_weighted_numerator_source_review`, a
nonauthor technical source reviewer in the same OpenAI family as the producer.
Organizational/provider-distinct independence credit: **0**. Scientific effect:
**NONE**. This is a fresh, bounded source/spec-quality review, not a replay of
the accepted mathematics or an execution audit.

## Exact identity and authority

Reviewed source:
`/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceGapWeightedNumerator.lean`

- Source SHA256: `b2fedf3739884ff716d11c85ebcf5de328fc76bc2a5bed31e8ea72c61d2f87a3`;
  20,999 bytes.
- Producer's strict-006 object SHA256:
  `2e6708f3f238cc5a6e1756edf926dab74cab2f05333978853cb6384cb3ff4a63`;
  1,730,640 bytes.
- PRECODE: `40f22f53bc5897e45fa8679d4d90dc88e1b28ba6`.
- Producer explicitly confirmed the final source is frozen unchanged and no
  source edits are planned. [FROZEN_SOURCE.json](/workspace/scratch/gap-weighted-numerator-construct/FROZEN_SOURCE.json)
  records the freeze at `2026-10-26T10:12:13.168211+00:00`.

These identities are reused from the existing strict-006 receipt and freeze
record; no hash was recalculated. The strict-006 receipt records exit 0 with
`-DwarningAsError=true` and an empty diagnostic log. The review reads the source
and its existing inventory; it performs no build, test, kernel run, axiom audit,
hash campaign, cache mutation, commit or external post. Only this owned scratch
report is written. No workers were launched.

Read `/workspace/AGENTS.md`, repository AGENTS/README and formal scope/check
authority, the binding SOURCE_GAP_WEIGHTED_NUMERATOR.md and PLAN, frozen control
contract, and preflight REPORT item 3. The standing owner mandate and delegation
were read from their repository copies:
[mandate](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md),
[delegation](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md).
The owner reuse instruction applies: completed applicable verification is reused;
a new reviewer alone does not justify repetition. The existing 41 qualified
modules/32 inputs and the old product-density, regular-integral, Holder/Markov,
moment mathematics, plus SourceGapPinCurvature and
SourceAllTargetCurvatureResidual, are accepted dependencies, not reverified
claims. Provider-distinct process remains separate from that mathematical
evidence.

## Source/spec assessment

Line numbers below refer to the frozen source.

1. **Closed literal endpoint, lines 350–380: PASS.**
   `sourceGapLaw_bad_union_numerator` assumes only signed real `L != 0`, fixed
   nonnegative B/K/A and positive eps. Its N and delta precede r/b/k, with
   `N >= 0` and `0 < delta <= 1`; every `|b| <= B`, `|k| <= K` and
   `0 < r < delta` is covered. The measure is literally `sourceGapLaw hL r b k`,
   the integrand is the physical `sourceSmoothWeight L r`, and the event is
   exactly `sourceRegularityBad L r eps union sourceCurvatureOneSided L r A`.
   Both global and restricted Bochner integrability are returned. No moment,
   density, product-law, covariance/variance, invertibility, pin, weight-bound,
   numerator or normalizer/floor certificate remains a final premise.

2. **Reusable weight integrability, lines 31–47: PASS.**
   The helper has one interval selected from hL alone, before all real b/k.
   It uses the existing all-target Gamma fourth-moment integrability and the
   actual-law a.e. bound `W <= 10*r^2*Gamma^4`. Measurability and nonnegativity
   justify the dominated-integrability step. The separate normalizer source
   imports this module and consumes this exact helper at its line 417; the
   numerator's imports at lines 1–3 contain no normalizer and create no cycle.

3. **Irregular-layer rate and integrability, lines 52–166: PASS.**
   Compact moments retain one shared interval before n/r/b/k. The actual gap-law
   sixth-power Markov specialization uses Gamma^30 and yields the r^6 base tail
   (lines 70–99). The physical square estimate is
   `W^2 <= 100*r^4*Gamma^8` (125–129). The integrable majorant and actual W-square
   integrability are established before integral monotonicity (130–142).
   Existing `prw_numerator_bound` is then applied under that same gap law; the
   square-root factors give r^2 times r^3, hence r^5 (143–166). No denominator or
   normalized probability is used.

4. **Regular-layer same-law join, lines 169–302: PASS.**
   The product wrapper augments the pullback event only with actual zero pin
   rows 3/4 and `sourceQ(Ψ p) = p.1`, then uses a.e. support to prove exact
   integral equality (189–222). It does not require row 5 = 2. Pullback
   integrability is obtained before invoking the existing
   `scalar_product_regular_integral_bound` (210–241). The closed wrapper chooses
   `x = sourceGapPins r b k`, `ν = curvatureScalarLaw L r x`,
   `ρ = curvatureResidualLaw hL r`, and the correctly swapped reconstruction
   `Ψ p = curvatureReconstruct hL r x p.2 p.1` (278–302). Its residual radius,
   seventeenth moment and reconstruction domination all use that same x and
   residual law. The all-target interval-mass result retains the affine target
   mean. Invertibility and positive variance are derived internally on the
   common small-radius interval (253–277). No centered/default-target law is
   substituted.

5. **Actual bad-union reduction, lines 306–345: PASS.**
   The reduction works at the integrand level under any measure with integrable
   physical W. All three events are measurable before indicator integrals and
   integral monotonicity. Outside the irregular event, positive W invokes the
   actual one-sided-to-symmetric slab theorem; the separate W = 0 branch keeps
   zero-weight samples without assuming positive weight a.e. No type filtering,
   normalized weighted-law support, or extra pin premise enters this reduction.

6. **Carrier, marks and scope: PASS.**
   The same `SmoothSample 2 L` carrier and signed `L != 0` are retained throughout.
   Every bounded real k is allowed, including negative and nondefault values;
   there is no k = 1/6 or positive-gap restriction. The final theorem is an
   unnormalized r^5 weighted integral. It establishes no positive floor,
   normalized probability, canonical partner, conditional Morse statement,
   frame/midpoint transport, Campbell/count identity, count density or parent
   Lean theorem. The source's own scope text at lines 8–11 and 347–349 agrees.

## Exhaustive existing inventory classification

Read the producer's existing
[inventory output](/workspace/scratch/gap-weighted-numerator-construct/runs/inventory-001/output.log),
[receipt](/workspace/scratch/gap-weighted-numerator-construct/runs/inventory-001/receipt.json),
[classification](/workspace/scratch/gap-weighted-numerator-construct/TARGET_CLASSIFICATION.json)
and [inventory](/workspace/scratch/gap-weighted-numerator-construct/INVENTORY.json).
The existing inventory selects by actual module index, not namespace prefix;
it records 10 constants, all theorem-kind, with no omitted constants:

| Classification | Declaration | Source line |
| --- | --- | --- |
| Written public theorem | `sourceGapLaw_weight_integrable` | 31 |
| Written public theorem | `sourceGapLaw_compact_moments` | 52 |
| Written public theorem | `sourceGapLaw_regularity_base_bound` | 70 |
| Written public theorem | `sourceGapLaw_regularity_numerator` | 103 |
| Written public theorem | `sourceGapLaw_regular_numerator_of_product` | 169 |
| Written public theorem | `sourceGapLaw_regular_numerator` | 247 |
| Written public theorem | `sourceBadUnion_integral_le` | 306 |
| Written public theorem | `sourceGapLaw_bad_union_numerator` | 350 |
| Generated simplification theorem | `I4SourceGapWeightedNumerator.sourceGapLaw_regularity_base_bound._simp_1_1` | generated |
| Generated definitional congruence, current-module-owned in imported namespace | `I4SourceCompactTargetMoments.sourceGapLaw.congr_simp` | generated |

The first eight short names belong to `I4SourceGapWeightedNumerator`.
The existing transitive axiom output records an empty list for `_simp_1_1` and
exactly `propext`, `Classical.choice`, `Quot.sound` for each other constant.
This is reused execution evidence, not a fresh audit. The old-namespace
`congr_simp` is correctly retained in the current module's generated inventory.

Findings: **none**. Kernel/control qualification and any separately authenticated
provider-distinct alignment requirement remain distinct from this source review.
