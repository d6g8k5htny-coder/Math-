# Actual physical endpoint composition: completed local proof

Sole production source:
`/workspace/Math-/frontiers/source_derivative_gaussian_20261025/SourceEndpointEstimates.lean`.

Source SHA256:
`d1f08d80d06d1ac08afbdd700370059fd8eaf0d4e483916e742efcdd1f664598`.

Final theorem:
`I4SourceEndpointEstimates.sourcePhysicalEndpoint_estimates_and_weighted_events`.

Its only research inputs are `L ≠ 0` and an arbitrary fixed real height `b`.
It derives constants `C ≥ 0`, `c > 0` and `0 < δ ≤ 1` such that every
`0 < r < δ` has literal physical weight square integrability, second moment
at most `C*r^4`, normalizer at least `c*r^2`, the explicit W-weighted actual
physical endpoint probability, and the `sqrt(C)/c * sqrt(K_r.real E)` bound
for every measurable endpoint event.

The final physical law is the canonical `sourcePhysicalEndpointKernel` at the
literal prescribed pin. Identification with the adjusted kernel uses the
proved literal measure equality from the common-residual affine-kernel
construction in `SourcePhysicalEndpointKernel`. A null-fiber identity alone
is not used to identify RCD versions. The module also derives eventual
`HasCondDistrib` for the actual physical normalized endpoint vector using
actual small-radius covariance invertibility.

No final covariance limit, Gaussian law, invertibility, uniform parameter
bound, moment or positive normalizer is added as a premise.

## Evidence

`qualification_receipt.json` binds the source, exact commands, exits, raw logs,
25 public targets, axiom reports, control hashes and remaining boundaries.

- Final compile `physical_assembly_attempt1`: exit 0, empty output, `.olean`
  generated. This completed compile was reused during qualification.
- Named `leanchecker SourceEndpointEstimates`: run once, exit 0, empty output.
- All 25 public transitive axiom reports: only `propext`, `Classical.choice`,
  `Quot.sound`.
- Elaborated final types: exit 0; final theorem has only `hL` and `b` inputs.
- Positive physical-order/radius-squared/strict-zero-boundary controls: exit 0.
- False omitted-permutation and false radius-power controls: each exit 1 at an
  intended unsolved `False` goal.

The earlier `stage*` logs and explicitly uncompiled assembly drafts remain as
history. The final source and qualification receipt supersede the pending
checkpoint; drafts are not final proof evidence.

## Lineage and scope

Actual OpenAI/Codex `/root/dm2_landed_composition` is the sole implementer.
Actual OpenAI/Codex helper `/root/dm2_landed_composition/peano_strategy` supplied
the normalizer-floor assembly draft incorporated into the module. This is
author-side work, not independent scientific review.

Completed actual covariance-limit, contact-parameter and canonical physical
kernel proofs are consumed directly. The 23 bound inputs, including the
byte-identical 11-module 66-target packet, were reused without rebuild or
re-audit. Earlier mode-chain, weighted-integral and regularized-continuity
scratch contributions to `SourceConfluentLimits` have separately preserved
evidence in the parent scratch directory.

Uniformity over unbounded height, whole-field geometric Kac-Rice/Palm
identification, arbitrary field-dependent events, GT5 and later parents remain
outside this theorem. Scientific effect NONE; different-family scientific
review remains separate. No commits or external posts were made.

Per `/workspace/AGENTS.md`, reuse this completed applicable verification. Do
not repeat it because of a handoff, new session or pending process requirement.
Root owns final inventory, Lakefile, records and publication integration.
