# Compact gap normalizer: exact-source and specification review

26 October 2026. OpenAI/Codex `/root/compact_gap_normalizer_source_review`.
**PASS: no source amendment requested. Scientific effect NONE.** This is a fresh
read-only source/specification alignment review of the new module and its new
helper joins. It earns **zero provider-distinct review credit**: the producer,
helper authors and this reviewer are OpenAI/Codex. The review was exposed to the
source, preflight, helper explanations and producer execution records; it is not
a blind reconstruction or a new independent-provider acceptance record.

## Exact reviewed candidate and contract

The reviewed source is
`/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceCompactGapNormalizer.lean`,
**24753 bytes**, SHA256
`d0f9319ac2ca792a9733659453583f4f71acc7ccccbcaba4ba1942566516065a`.
Identity is transcribed from the dispatch, `FROZEN_SOURCE.json` and producer
receipts, without a new hash campaign. The corresponding producer object is
1477944 bytes, SHA256
`36548ee275e757fe1a7fc507395d5d2bd6353cc65e686eb631472dbe5e40eed3`.

The binding source contract and plan were read at PRECODE commit
`40f22f53bc5897e45fa8679d4d90dc88e1b28ba6`, together with
`/workspace/scratch/compact-gap-normalizer-preflight/REPORT.md`. The final theorem
at source lines 406–481 matches their closed endpoint:

```text
L != 0, B >= 0, 0 < k0 <= k1
  => exists c > 0, 0 < delta <= 1, chosen before r,b,k,
     for every 0 < r < delta, |b| <= B, k0 <= k <= k1,
       Integrable W (sourceGapLaw hL r b k)
       and c*r^2 <= integral W d(sourceGapLaw hL r b k).
```

The law and physical weight are the same literal ones in both conclusions.
There is no final premise for moments, Gaussian density/mass, pin support,
Hessian type, event probability, integrability or the desired normalizer floor.
The signed period is assumed nonzero, never positive. Constants may depend on
`L,B,k0,k1`; this source makes no unbounded-height, vanishing-gap, all-period,
frame or translation uniformity claim.

## Fresh mathematical alignment

1. **Lower Gaussian density and unit-interval mass, lines 32–99.** The helper
   retains arbitrary bounded affine mean `mu`, with `|mu| <= M`, rather than
   replacing it by zero. From `x in [-2,-1]`, the proof gets
   `|x-mu| <= 2+M`. The variance lower bound `V/2 <= nu` gives
   `V <= 2*nu` and hence the lower exponential factor. The variance upper
   bound `nu <= 2*V` gives the lower inverse-square-root prefactor. Thus
   `eta = (sqrt(4*pi*V))^-1 * exp(-(2+M)^2/V)` is a correct positive density
   lower bound. Both `nu>0` and `nu!=0` are derived. Integration uses the
   integrable Gaussian PDF and the interval's exact length one before comparing
   real Bochner integrals. The new lower estimate is not inferred from an old
   upper-density estimate.

2. **Actual marginal, target mean and variance interval, lines 103–171.**
   `sourceGapLaw_q_hasLaw` pushes the existing actual source posterior/product
   reconstruction through `sourceContactQ` and the old exact identity
   `curvatureReconstruct_Q`. It does not rebuild the old Gaussian/product law.
   The scalar law is the existing `curvatureScalarLaw` with mean
   `curvatureBeta L r dot sourceGapPins r b k` and variance
   `(curvatureVariance L r).toNNReal`. The six-term absolute sum and Pi/sup-norm
   coordinate bound correctly yield `M=6*J*(B+13*K)`, specialized to `K=k1`
   in the final theorem. The bounds obtained at prescribed `b=0` are used only
   for beta, invertibility and the Schur variance floor; the old prescribed
   mean estimate `_hmean` is deliberately unused. The variance upper bound
   comes from the old `curvatureVariance_tendsto`, while the lower bound is
   `V/2` for `V=sourceContactSchur L>0`. Their positive common interval and the
   `toNNReal` coercion use the derived actual positive variance.

3. **Good event and mass subtraction, lines 174–215.** The event uses the
   original, unchanged `sourceGammaRadius`, not a residual or proxy radius.
   Its measurability follows from the existing measurable q and Gamma maps.
   For `A=max 1 (2*H/eta)`, the proof combines the nonnegative first-moment
   Markov inequality with inclusion `{Gamma>A} subset {Gamma>=A}` and finite
   real-measure set subtraction. It obtains mass at least `eta/2` without
   asserting q/Gamma independence. The same unweighted law is used throughout.

4. **Parameterized cubic/axial join, lines 221–286.** The scalar wrapper uses
   `f(x)=g(x)-c+2` and the existing cubic-kernel mass `1/6` to satisfy the old
   target-two theorem. Continuity, interval integrability and unchanged
   Lipschitz constant are supplied. At actual pin row5=`12*k`, with rows3=4=0,
   the old pin5 integral and normalized Peano identity yield axial centers
   `-6*k,+6*k`. The affine half-mass error estimates are conservatively weakened
   to `r*Gamma`. No special `k=1/6` theorem is silently reused at a different k.

5. **Strict physical Hessians and literal weight, lines 289–401.** For
   `0<r<min 1 (min (1/(2*A)) (k0/(2*A^2)))`, the arithmetic derives
   `v0<=-3*k0`, `v1>=3*k0`, `v4,v5<=-1/2`,
   `DM=v0*v4-r*v2^2>=k0`, and `DS=v1*v5-r*v3^2<=-3*k0/2`.
   The literal physical determinants remain `r*DM,r*DS`. The actual strict
   negative-definite criterion at M and negative determinant at S establish the
   precise strict type branch of `egm_weight`; their determinant product gives
   `W>=k0^2*r^2`. The source wrapper rewrites the actual raw Hessians and actual
   `sourceSmoothWeight`, retaining the physical type indicator and both radius
   factors. It reuses the old generalized cross-entry/q errors. The source
   expressly says this is Hessian typing; endpoint criticality also needs the
   gradient pins. No criticality claim is inferred from rows3,4,5 alone.

6. **Closed assembly and real integration, lines 406–481.** The final proof
   derives `H=C*(1+B)` from the old n=1 height moment, fixes A, and intersects
   all positive radii before introducing r,b,k. It sets
   `c=k0^2*eta/2>0`. Full literal pin support is derived a.e. from
   `sourceGapLaw_curvature_bounds`; rows3=4=0,row5=`12*k` are extracted inside
   the proof. An explicit probability instance comes from the existing Markov
   source kernel, so its use is independent of the W normalizer. W integrability
   is obtained at line417 from the new numerator's helper and used at line469
   before real integral comparison. The integrable measurable event indicator
   integrates to `k0^2*r^2*Q.real E`, yielding the exact final floor.

## Dependency and helper custody

The Gaussian and deterministic reports were read at
`/workspace/scratch/compact-normalizer-gaussian/REPORT.md` and
`/workspace/scratch/compact-normalizer-deterministic/REPORT.md`.
Their frozen needed sections are respectively:

- 3532 bytes, SHA256
  `2286f304a69e742b84d762f8df649d4788643237d67be90009ed2cfa76bf671f`;
- 9906 bytes, SHA256
  `3ac2bdd270d54608cca584be8083598d5c813e552a75dc2caaa191b9348d7f41`.

These helper identities and exact-once integration are transcribed from the
producer freeze metadata, not recomputed. The integrated bodies were read as
part of the fresh review above. No scratch helper object is needed as a
production import.

The sole imported new numerator helper is
`I4SourceGapWeightedNumerator.sourceGapLaw_weight_integrable`, source lines
31–48 in `SourceGapWeightedNumerator.lean`. Its frozen source is 20999 bytes,
SHA256 `b2fedf3739884ff716d11c85ebcf5de328fc76bc2a5bed31e8ea72c61d2f87a3`;
object SHA256
`2e6708f3f238cc5a6e1756edf926dab74cab2f05333978853cb6384cb3ff4a63`.
It derives integrability from existing all-target fourth moments, W
measurability/nonnegativity and the old `W<=10*r^2*Gamma^4` bound. Its imports
do not include `SourceCompactGapNormalizer`, and its proof does not use a
positive normalizer. Thus the normalizer-to-numerator dependency is acyclic;
the elementary integrability join is borrowed exactly as requested.

## Source declarations and actual-module inventory

The source has 13 named theorem targets and two definitions. All 15 are
classified below. Generated constants are tracked separately rather than
silently excluded by namespace or theorem-only filtering.

| Source line | Declaration | Classification |
|---|---|---|
| 32 | `gaussianCompactLowerConstant` | New explicit scalar constant definition |
| 35 | `gaussianCompactLowerConstant_pos` | New constant positivity |
| 41 | `gaussianPDFReal_lower_compact` | New bounded-mean, two-sided-variance lower PDF estimate |
| 73 | `gaussianReal_Icc_lower_compact` | New lower PDF-to-real-mass integration join |
| 103 | `sourceGap_curvatureMean_bound` | New literal target/Pi-norm mean estimate |
| 124 | `sourceGapLaw_q_hasLaw` | New marginal composition of the accepted actual law |
| 141 | `sourceGapLaw_negative_interval_mass` | New compact actual-law Gaussian parameter assembly |
| 174 | `sourceCompactGoodEvent` | New event definition on original q/Gamma |
| 177 | `sourceCompactGoodEvent_measurable` | New measurability composition |
| 183 | `sourceCompactGoodEvent_mass` | New Markov and finite subtraction join |
| 221 | `cubic_pin_pointwise_error_target` | New translation wrapper of accepted scalar cubic estimate |
| 251 | `source_normalized_gap_axial_errors` | New arbitrary-k actual axial join |
| 289 | `endpointWeight_gap_floor` | New finite strict physical-type/determinant arithmetic |
| 375 | `sourceSmoothWeight_gap_floor` | New literal source-Hessian/weight composition |
| 406 | `sourceGapLaw_compact_normalizer` | New closed actual-law compact normalizer theorem |

The producer's existing `INVENTORY.json`, `TARGET_CLASSIFICATION.json`,
`runs/inventory-001/output.log` and receipt were read. Their 13/2/4
classification agrees with the source map above. The actual environment
module-index selection reports **19 constants**, all with transitive axioms a
subset of `{propext,Classical.choice,Quot.sound}`. In addition to the 15 entries
above it includes these four generated theorem constants:

- `SourceCompactGapNormalizer.gaussianCompactLowerConstant._proof_1`;
- `SourceCompactGapNormalizer.gaussianCompactLowerConstant._proof_2`;
- `SourceCompactGapNormalizer.sourceCompactGoodEvent_mass._simp_1_3`;
- `ResearchFormalCoreR1.egm_weight.eq_1`.

The first three are elaborator-generated scalar/simplification support. The
last is a generated equation theorem for the unfolded imported physical weight
definition, recorded under its actual external namespace. It is still owned
by this environment's module index and correctly included. These are support
constants, not four extra scientific theorem claims. There is no unexplained
source declaration, axiom, opaque, inductive or recursor in the reported module
inventory. This classification is a review of the producer's existing output,
not a new audit execution.

## Existing execution evidence read, not rerun

Producer receipts under `/workspace/scratch/compact-gap-normalizer-construct`:

- `runs/compile-005/receipt.json`: warning-as-error elaboration PASS,
  exit0, empty log, 10:10:16 UTC; exact reviewed source/object identities above.
- `runs/controls-002/receipt.json`: positive controls PASS, exit0, empty log,
  10:11:43 UTC. Source read exercises signed `L=-1`, `b=3`, k=1 and k=2 with
  shared c/delta, strictly positive real integral with integrability, affine
  mean bound, both variance endpoints and literal strict physical types.
- `runs/false-omitted-radius-001/output.log`: the proved physical unit-weight
  counterexample gives exactly the intended residual `False` when the physical
  `r^2` factor is omitted. No unrelated diagnostic appears in that output.
- `runs/kernel-001/receipt.json`: the producer's sole named own-module kernel
  PASS, exit0, empty log, 10:14:15 UTC after source/helper/numerator freezes.
- `runs/inventory-001/receipt.json`: exhaustive actual-module-index inventory
  and standard-three transitive axiom check PASS, exit0, 10:14:20 UTC.

The final producer `FROZEN_SOURCE.json` explains why compile-005 remains
applicable after final numerator qualification: the sole consumed
`sourceGapLaw_weight_integrable` statement/proof is byte-identical between the
early and final numerator artifacts (recorded declaration SHA256
`662f4614ace6995188f2c03d79f7019accbb765e8c9f23133ba326f9e2527744`), and the
later appended declarations are unused here. The final environment import is
also exercised by the existing controls-002 and final own-module kernel.
Qualification timing alone supplies no reason to repeat the unchanged strict
elaboration. This dependency join is reused as producer evidence, not recomputed.

This source/spec review does not duplicate execution-audit ownership or claim
new kernel evidence. Completed, applicable verification remains reusable under
`/workspace/AGENTS.md`. The established 41 source/32 support-input mathematics,
old scalar/product Gaussian laws, moments, Peano identities, physical weight
estimates and accepted conventional contact-limit mathematics were used as
accepted dependencies; their proofs/checks/reviews were not replayed.

## Limits, authority and handoff

The theorem proves a coarse positive quadratic floor. It does not prove uniform
contact-limit asymptotics, a normalized cutoff/Palm probability estimate,
canonical partner/elder selection, a framed or translated law, global Morse
behavior, count density or a Parent theorem. The source's comments accurately
preserve those limits. A pending provider-distinct process requirement does not
erase the accepted mathematics or this scoped technical PASS.

Read workspace/repository instructions, README, formal README/SCOPE and the
required-check contract, plus the canonical local owner mandate, delegation and
current workflow. Carry the canonical links in future onboarding:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

Links establish availability, not an unobserved later recipient's reading.
Root retains cache/registration/commit/native-publication ownership and the
separately authenticated provider-distinct scientific process. This reviewer
wrote only this report under
`/workspace/scratch/compact-gap-normalizer-source-review`. No source,
configuration, cache, commit, external post, worker, build/test/kernel/audit,
control or hash-campaign execution occurred.
