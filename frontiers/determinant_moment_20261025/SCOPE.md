# Exact DM2 formal scope

Author OpenAI/Codex /root; source-alignment PENDING_INDEPENDENT_REVIEW.
The complete preimplementation source binding is SOURCE_MAP.md and remains bound.

| Declaration | Source mapping and hypotheses |
|---|---|
| dm2_untyped | Section 3: both exact determinant factors; arbitrary nine real jets; 0<r<=1. Proves the stronger bound before type restriction. |
| dm2_pointwise | Section 2's exact W²<=16r⁴R⁸; no extra type or probability assumptions. |
| dm2_negative_iff | Auxiliary two-dimensional Sylvester criterion, proved for every symmetric real 2x2 matrix, connecting the literal quadratic-form indicator with measurable polynomial inequalities. |
| dm2_weight_measurable | Measurability of the actual indicator-weight product for every real r, with no null-boundary premise. |
| dm2_moment | Sections 2–3: measurable nine-jet map, integrable eighth radius power, integral<=M8, 0<r<=1 yield squared-weight integrability and integral<=16M8r⁴. The arbitrary-measure statement strengthens the source probability-law implication without adding a premise. |

All definitions, matrix entries, signs and coordinate ordering are in the Lean
source and SOURCE_MAP.md. The retained 13 scalar baseline declarations preserve their statement/proof bodies from formal/ at c4eabc1a; COMPATIBILITY.md documents their historical repairs.
Their imported historical review is not transferred to the changed package.

The new theorem does not prove a concrete Gaussian moment, jet identification,
normalizer floor, actual Palm construction, full event tail, GT5, P0.2, lifetime
or persistence theorem. Scientific effect NONE; no register changes.

The unchanged retained gate builds all 18 registered targets, runs leanchecker,
audits transitive axioms against propext/Classical.choice/Quot.sound, and executes
its original five rejection controls. controls/ adds two explicit false DM2
mutations: r^6 instead of r^4 and omission of q from R. Those separate executions
are recorded independently. The gate retains its exact provider-distinct alignment
validator; a same-provider technical source review earns zero organizational
independence and does not supply a machine ACCEPTED alignment record.

## Import-only memory repair

The original full-Mathlib build passed but kernel replay exceeded 16GiB.
SOURCE_MAP.md records that failure and the narrow-import successor. Every
scalar statement/proof body, gate.py, pin and rejection control is preserved;
only imports and their exact preservation-test expectations changed.
