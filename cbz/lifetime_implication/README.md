# Literal E2-to-E4 implication — candidate

The candidate source `Bounds.lean` proposes that, for supplied field,
elder and pair-law interfaces, the literal planar lower predicate E2 implies
the literal two-sided predicate E4. E4 itself assumes the literal parent
upper predicate. On valid inputs, the proof combines the witnesses at
`min rLower rUpper`; on invalid inputs the implications can be vacuous.

This does not prove either assumed estimate, construct a field or elder
interface, identify the pair law with the intended geometric probability,
or establish the parent results. It is a logical assembly statement only.

The source is outside the fixed-inventory statement packet. Workflow
`.github/workflows/cbz-lifetime-e2-e4.yml` checks the packet first,
temporarily copies the candidate, compiles it and runs `leanchecker`;
its axiom report must be inspected before any claim. It assumes the hosted
runner, Lean and pinned dependencies are trusted. No successful execution
has yet been observed; the candidate is not classified CLOSED.
