# SourceCompactFoldWeightedProbability exact-source/spec-quality review

Verdict: **PASS — no source/spec findings or amendments requested.**

Attribution: **Dylan Roy — delegated AI review**; actual performer
OpenAI/Codex, agent `/root/compact_fold_weighted_probability_source_review`.
This is a fresh nonauthor technical source/spec review of the new composition.
The reviewer is in the same OpenAI family as the producer: provider-distinct
and organizational-independence credit **0**; scientific effect **NONE**.
Dylan's personal reading is **PENDING**, an optional retrospective reading aid.

## Exact frozen identity

Reviewed source:
`/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceCompactFoldWeightedProbability.lean`.

- PRECODE: `b8114e28d0e440e078a831c8df7fe69411b3a6e5`,
  `SOURCE_COMPACT_FOLD_WEIGHTED_PROBABILITY.md` and its PLAN.
- Source: 8,882 bytes, SHA256
  `97e6c694b62d90f6b723b0e510691e019f763ff26ebba743664d596dc72223b9`.
- Producer strict-001 object: 499,208 bytes, SHA256
  `7f5e51ce282049a8ea7a72af338b826fe8faa16eb739a2f697b88a63270140b6`.
- Producer [FROZEN_SOURCE.json](/workspace/scratch/compact-fold-weighted-probability-construct/FROZEN_SOURCE.json)
  records final freeze at `2026-10-26T10:30:47.779505+00:00`, before the
  planned sole named own-module kernel invocation. The producer and root both
  explicitly confirmed unchanged final source and no planned source edits.

These identities are transcribed from existing producer receipts/freeze, not
recomputed. The producer's successful strict compile is labeled `compile-001`
in its receipt and is the strict-001 referred to in the handoff. It used
`-DwarningAsError=true`, returned exit 0, and recorded an empty diagnostic log.

## Source/spec alignment

Line references below are to the frozen source.

1. **Literal varying law and exact measurable cutoff event: PASS (22–44).**
   `sourceCompactFoldGood` consists precisely of
   `r*(sourceT k0 sample)^5 <= 1/100` and
   `1024*(sourceT k0 sample)^5 <= sourceKappa r k sample`.
   `sourceCompactFoldWeightedLaw` is definitionally
   `prwMeasure (sourceGapLaw hL r b k) (sourceSmoothWeight L r)` on
   `SmoothSample 2 L`. The new event uses the actual varying k. Its
   measurability follows directly from the inherited measurable T and kappa
   maps. No geometric selector or choice of complement enters the event.

2. **Full scale and correct uniform obstruction inclusion: PASS (32–76).**
   The inherited `sourceScale k0 = 8*max 1 (1/(6*k0))` and
   `sourceT k0 = sourceScale k0 * sourceGammaRadius L` are retained.
   Epsilon is the inherited `1/(100*sourceScale k0^5)` and the new uniform
   coefficient is exactly `6*k1*1024*sourceScale k0^5`.
   The scalar inclusion uses positive lambda/r/k and nonnegative Gamma.
   In the second branch, strict failure is multiplied by the positive
   denominator `6*k*r`, and `k <= k1` is multiplied only by the nonnegative
   `6*1024*lambda^5*r*Gamma^5`. Thus its final one-sided obstruction has
   the correct sign, r power and full `6*k1` factor. The first branch gives
   the strict regularity event; the second is conservatively closed.
   The actual-sample wrapper supplies the original Gamma nonnegativity and
   derives `k > 0` from `0 < k0 <= k`. It proves only Good-complement subset
   bad-union; it does not claim a reverse inclusion.

3. **Closed normalized probability endpoint: PASS (86–125).**
   Final hypotheses are only `L != 0`, `B >= 0`, `0 < k0 <= k1`.
   `sourceGapLaw_bad_union_numerator` supplies the actual compact numerator
   and Bochner integrability internally; `sourceGapLaw_compact_normalizer`
   supplies the positive actual denominator floor internally. Their displayed
   inherited interfaces match the consumed law, weight and compact mark
   bounds. The proof derives `|k| <= k1` from positivity, rather than assuming
   a default gap mark. It chooses `C=N/c >= 0` and
   `delta=min deltaN deltac` before r,b,k. For all `0<r<delta`, `|b|<=B`
   and `k0<=k<=k1`, the floor gives a strictly positive real weight integral.
   Inherited `prw_isProbabilityMeasure` then proves that this exact law is a
   probability measure. Finite real-measure monotonicity uses the one-way
   event inclusion; inherited `prw_measure_real` gives the same-law Bochner
   ratio on the measurable bad-union. Correct denominator direction yields
   `N*r^5/(c*r^2)=(N/c)*r^3` for positive r.
   No desired numerator, normalizer, probability, AC, pin, type, geometry,
   H0 or model certificate is a final premise.

4. **Shared uniform interval and weighted-a.e. ordinary H0: PASS (79–82,
   130–158).** Absolute continuity is derived from the existing prwMeasure
   property for precisely the same `sourceGapLaw hL r b k` and weight.
   The H0 endpoint intersects the probability radius with the inherited
   hL-only actual torus-H0 radius before introducing r,b,k or a coefficient
   field K. It retains the same C and the same probability bound on that
   shared interval. The inherited `sourceGapLaw_actual_torus_h0` is applied
   at this actual k and its source-law a.e. implication is transported by
   the derived same-law AC. Membership in Good supplies exactly its two
   cutoffs. For each field K, weighted-almost every Good sample has the
   actual ordinary singular-H0 summand `elderInterval K b (b-k*r^3)` with
   a complement, strict clearance `Iio (b-k*r^3)`, and real strict-clearance
   death/supremum `b-k*r^3`. The inherited interval convention includes
   birth `-b` and excludes death `-(b-k*r^3)`.
   The statement is `forall K, almost everywhere`; it does not assert one
   K-independent null set or a measurable choice of geometric data.

5. **Carrier, quantifiers and scope: PASS (4–8, 22–29, 86–92, 130–145).**
   Signed real `L != 0` is preserved, so negative periods are covered.
   Every bounded birth height and every gap in the displayed compact positive
   interval is covered. The fixed-k=1/6 module supplies scale/measurability
   helpers, not its fixed-mark probability endpoint. There is no surrogate
   residual/centered law, removed physical type indicator, or hardcoded k=1/6
   in the new endpoint. Constants may depend on L,B,k0,k1; the result asserts
   no unbounded-height, k0-to-zero, all-L, frame or translation uniformity.
   The source accurately excludes a canonical Morse-labeled partner. It
   proves no conditional Morse theorem, canonical selection or intrinsic
   lifetime/H0 identification, frame/translation transport, actual Campbell
   or count-density identity, or Parent A/B Lean closure.

## Existing inventory and classification

The producer's [Inventory.lean](/workspace/scratch/compact-fold-weighted-probability-construct/Inventory.lean),
[output](/workspace/scratch/compact-fold-weighted-probability-construct/runs/inventory-001/output.log)
and existing successful receipt were read, not executed. Selection is by
actual environment module index, not namespace prefix or theorem-only filter.
The output reports **21** owned constants: **7 public written theorems,
3 definitions, 11 generated theorem supports**.

| Source line | Written declaration | Classification |
| --- | --- | --- |
| 22 | `sourceCompactFoldGood` | Explicit measurable-cutoff event definition |
| 27 | `sourceCompactFoldWeightedLaw` | Literal actual weighted-law definition |
| 32 | `sourceCompactCutoffA` | Full uniform obstruction coefficient definition |
| 34 | `sourceCompactCutoffA_nonneg` | Public coefficient sign theorem |
| 39 | `sourceCompactFoldGood_measurable` | Public event measurability theorem |
| 48 | `varying_cutoff_failure_inclusion` | Public new varying-k scalar inclusion |
| 66 | `sourceCompactFoldGood_compl_subset` | Public actual-sample event inclusion |
| 79 | `sourceCompactFoldWeightedLaw_absolutelyContinuous` | Public same-law AC composition |
| 86 | `sourceCompactFoldWeightedProbability_bound` | Public closed uniform probability endpoint |
| 130 | `sourceCompactFoldWeightedProbability_h0` | Public shared-interval weighted H0 endpoint |

All short names belong to `SourceCompactFoldWeightedProbability`.
The 11 generated theorem constants are:

- `sourceCompactFoldGood._proof_1` and `._proof_2`;
- `sourceCompactCutoffA._proof_1`;
- `sourceCompactFoldWeightedLaw.congr_simp`;
- `sourceCompactFoldWeightedProbability_bound._simp_1_3` through `._simp_1_9`.

These are proof/elaboration/simplification support, not 11 additional written
research claims. There are no private written declarations, data instances,
Prop bundles, unexplained axioms, opaque declarations, inductives, constructors
or recursors in the reported inventory. Every transitive axiom row is a subset
of `{propext, Classical.choice, Quot.sound}`. This is classification of existing
producer output, not a fresh axiom-audit run.

## Existing controls and execution evidence reused

The precode spec and frozen `CONTROL_CONTRACT.md` preceded production code;
`CONTROL_CONTRACT.json` records the freeze at 10:28:22 UTC. Existing receipts
bind strict compilation, controls and inventory to the same source/object
identities above. Controls returned exit 0 at 10:30:28 UTC, inventory exit 0
at 10:30:40 UTC. The source-specific controls read exercise:

- L=-1, B=3, k0=1/12, k1=2; exact scale16 and
  `A=6*2*1024*16^5=12884901888` (Controls lines14–51);
- literal varying law/event, measurability and same-law AC/AE transfer
  (16–23,40–51,78–87);
- one C/delta for actual marks `(b,k)=(-3,1)` and `(3,2)`, and the full
  shared-interval H0 endpoint before every coefficient field (90–121);
- fifth-over-second cubic cancellation and closed-boundary arithmetic
  (67–76).

Controls lines54–65 prove at the prescribed scalar witness
`r=1/10^9, Gamma=1, q=-5, k=2, lambda=16` that the first cutoff holds,
the second fails, the reduced coefficient misses the obstruction, and the
full coefficient catches it. This is honestly a finite arithmetic witness;
it does not assert an actual posterior sample with those Gamma/q values.
The existing `false-omitted-mark-factor-001/output.log` reports exactly one
unsolved residual `False` and no unrelated diagnostic, with exit 1. The false
implication omits precisely the required `6*k1` factor. No negative control
was replayed for this review. The sole final own-module kernel remains
producer-owned; this source review creates no separate execution claim.

## Reuse, authority and handoff

Read `/workspace/AGENTS.md`, repository AGENTS/README, formal README/SCOPE and
required-check authority; read the binding precode spec/plan and the local
canonical owner mandate, standing delegation and current workflow.
Carry the canonical owner links into onboarding/handoffs:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

Completed applicable verification is reused under the 25 October owner
clarification. The accepted 43-module/32-input environment at 6efd145, old
numerator and positive-floor mathematics, Gaussian laws/moments, scale helpers,
ordinary-H0/clearance mathematics and conventional positive-gap results remain
accepted dependencies. Only consumed definitions/interfaces needed to assess
this new glue were consulted; their mathematical proofs, controls, kernel
checks and reviews were not replayed. In particular, a pending separately
authenticated provider-distinct process does not erase that mathematical
evidence or this scoped technical PASS.

Conditional genericity, if formalized downstream, must be restricted to each
prescribed positive-gap raw target with distinct torus endpoints. Arbitrary
unrestricted raw vectors are not covered; equal-height zero-gradient targets
can force equal critical values. The present endpoint does not need such a
genericity premise. Unrestricted Gaussian laws/moments retain their accepted
scope.

Root retains registration, cache, commits, publication, hosted checks and the
provider-distinct process. The reviewer wrote only this report under its
assigned scratch directory. No source/config/cache/manifest mutation, worker,
test/build/kernel/audit/hash-campaign execution, commit or external post was
performed. Findings: **none**.
