# Cap I4: nonnegative polar-coordinate Lean sub-bridge

Author: OpenAI / GPT-6 Astra Pro, cap-i4-polar-formal-20261006, delegated by Dylan Roy.
Source cut: Math- 2f8b6f372be383d752e9dd30d38234faa977243c. Scientific effect NONE.
This is an isolated companion, not a change to formal/ or its target inventory.
Initial scope claim: main#229 comment6007417630. No author self-merge.

## Formal scope

The four definitions and nineteen theorems give the explicit ordered eigenvalue
coordinates of [[a,b],[b,d]], continuity and positive-support measurability,
trace/determinant/Frobenius identities, and the actual nonnegative polar
change of variables. The density comparison permits an arbitrary anisotropic
input density with a pointwise spectral envelope; it does not assume that the
input equals that envelope. The integral is ENNReal-valued and retains its polar
radius factor and the complete mathlib polar domain.

The last theorem integrates that comparison over the trace coordinate. This is
NOT YET the full entry-Lebesgue/eigenvalue pushforward: the entry-to-trace linear
volume change (absolute determinant 2), trace/radius-to-eigenvalue change
(absolute determinant 1/2), and angular evaluation are not formalized here.
Nor are the actual field density/regression, residual independence/moments,
typed determinant inequality, geometric event or full normalizer instantiated.
No new moment8 or moment9 claim is added; those ordinary proofs and reviews
remain in their own packets. The general spectral theorem is not assumed.

## Consumed sources

P: imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md,
blob dfed3b8d318a3ab1950957f393307733a4bef3f2; read its normalizer with
ERRATUM_CONGRUENCE.md, blob213594d6ca6a86fb938110f4d166d9ce275a02d0.
Ordinary d3 route: PR313 PROOF.md blobc30e3f5ff600b058a30087ff794c7cf304e4aafc,
reviewed at8e90773b28ecce66ed30458d58aef1b6cb83666a. That source review is NOT
an alignment review of this new Lean file.
Actual imported polar theorem: mathlib d13f23b723b8a846827a245b89c10fc7d3f11612,
Mathlib/Analysis/SpecialFunctions/PolarCoord.lean,
blob053dcbf1bcd84f42dcc8273dd4afb0d87a6755e6.

## Execution and limitations

Run bash companions/cap_i4_polar_20261006/replay.sh from a complete repository
with the pinned Lean toolchain and dependencies. The workflow installs the
existing toolchain, verifies dependency HEADs, runs both seven-method Python
suites in normal/optimized modes, compiles this module with warnings as errors,
prints every declared type and transitive axiom list, runs fresh leanchecker,
and requires both intended False-goal controls. Source records must match
before/after execution and evidence is retained on failure. Existing formal/
proofs are not rebuilt by this standalone workflow; it is not a new receipt
for their 63-target inventory. Local source/finite/parser tests are not a
kernel replay. Any failed or unfinished hosted attempt stays failed/unfinished.

A source-bound nonauthor alignment read is required before any stronger claim.
