# Deterministic arbitrary-gap physical-weight helper

26 October 2026. OpenAI/Codex `/root/compact_normalizer_deterministic`.
Scientific effect **NONE**. This is author/helper work, with zero provider-distinct
review credit and zero separate research credit.

## Frozen integration handoff

Use `INTEGRATION_SECTION.lean` once in the producer's new
`SourceCompactGapNormalizer.lean`. The section includes all required opens,
`set_option autoImplicit false`, and namespace `SourceCompactGapNormalizer`.
The producer's existing `SourceGapPinCurvature` import suffices. No scratch
module import or scratch object belongs in production. Exact frozen identities
are in `FROZEN_SECTION.json`.

Four declarations, each necessary for the actual source wrapper:

1. `cubic_pin_pointwise_error_target`: applies the old scalar error theorem
   to `g-c+2`; its new target-two average uses the reused cubic mass `1/6`.
   It does not reprove scalar Peano mathematics.
2. `source_normalized_gap_axial_errors`: rows 3=4=0 and row5=`12*k`
   imply normalized errors about `-6*k` and `6*k`, both at most `r*Gamma`.
   It composes `source_pin5_eq`, the old pin5 integral,
   `sourceF_third_lipschitz`, affine weighted errors and
   `source_normalized_peano`. The intermediate weighted errors retain their
   half mass before weakening to the original radius.
3. `endpointWeight_gap_floor`: finite six-vector arithmetic gives the literal
   strict negative-definite M Hessian, literal negative S determinant, and
   physical endpoint weight at least `k0^2*r^2`. It keeps physical determinant
   factors `r*(v0*v4-r*v2^2)` and `r*(v1*v5-r*v3^2)`, and unfolds the actual
   strict type indicator in `egm_weight`.
4. `sourceSmoothWeight_gap_floor`: composes axial errors, the frozen gap-leaf
   first-four bound and pin-free transverse errors, rewrites actual physical
   Hessians with their existing identities, and uses `sourceSmoothWeight_eq`.
   Its exact signature is in the frozen section. It returns
   `sourceSmoothTyped L r sample` and
   `k0^2*r^2 <= sourceSmoothWeight L r sample` from only rows3,4,5 plus
   `q in [-2,-1]`, `Gamma<=A`, `1<=A`, `0<k0<=k` and
   `0<r<min 1 (min (1/(2*A)) (k0/(2*A^2)))`.

The arithmetic establishes `v0<=-3*k0`, `3*k0<=v1`, `v4,v5<=-1/2`,
`DM>=k0`, `DS<=-3*k0/2`; `dm2_negative_iff` proves the actual strict type.
No endpoint criticality, canonical partner, global Morse, normalized
probability, contact limit or Parent conclusion is claimed. Criticality would
also require the common gradient pins; those are not assumed by this floor.

## New-only elaboration evidence and retained failures

`runs/compile-003/receipt.json` records strict warning-as-error elaboration
PASS at **10:07:31 UTC**, 7.47 seconds, with an empty log. Its scratch object
is only elaboration evidence, not a standalone named-module kernel result.
The specific uncovered obligation tested was the new translated-cubic wrapper,
new arbitrary-gap axial join, finite physical determinant/type arithmetic and
actual source wrapper. Completed old mathematics, kernel, audits, controls and
reviews were reused and not rerun.

All three attempts retain exact source snapshots, commands, exits, UTC times,
source identities and output logs. `compile-001` failed before elaboration
because the absolute scratch input lay outside Lean's default package root;
`--root` corrected that invocation. `compile-002` found the numeral-coercion
presentation in a majorant inequality needed an explicit real typed statement,
and rejected deprecated `if_pos` under Werror; both were corrected.
`compile-003` is the sole successful frozen scratch elaboration. No further
unchanged verification is needed here. The producer will perform its one
integrated own-module kernel, exhaustive actual-module inventory/axiom audit,
and new controls after every integration section and numerator are frozen.

No production source, inputs, configuration, cache, manifest, Git commit,
external post, worker, standalone kernel, audit or control was modified or run.
Only `/workspace/scratch/compact-normalizer-deterministic` was written.
`EXECUTION_RECORD_INDEX.json` points to every new elaboration receipt.

## Reuse, authority and boundaries

Read workspace reuse guidance, repository entry/README, formal README/SCOPE
and required-check contract, published PRECODE commit
`40f22f53bc5897e45fa8679d4d90dc88e1b28ba6` compact-normalizer source contract
and plan, and authoritative preflight
`/workspace/scratch/compact-gap-normalizer-preflight/REPORT.md`.
Reuse the established **41 source / 32 input** mathematics and applicable
completed verification. A new helper, handoff or provider-distinct process
requirement does not erase those mathematical results.
The consumed frozen gap leaf has source SHA256
`67f6c671e4ed8a7cb8557fc6027403f4fd1e94cba984e672eaa3ceb94ab8847e` and qualified
object SHA256 `00378503fe93cca757712046d9c6818296880b5524d7c0096f87794c2657eb2c`,
transcribed from its producer report without replay.

Read local canonical owner mandate, delegation and workflow. Carry the canonical
owner links in future onboarding:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

A link does not establish a later recipient has read it. Root owns registration,
production qualification/cache, commits and publication. Producer checkpoint
10:45 UTC and terminal 11:45 UTC remain unchanged.
