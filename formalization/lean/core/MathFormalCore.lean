import MathFormalCore.Side24.Arithmetic

/-!
# MathFormalCore

Layer 1 (formal specification and proof) of the Math- verification stack,
core-only package. Every declaration in this library is kernel-checked from
the Lean 4 core prelude; no Mathlib, no compiler-trusting evaluation, no
placeholder proofs (the gate rejects those constructs textually and by axiom audit).

Scientific effect: NONE. A kernel-checked theorem verifies exactly the Lean
statement written here. Whether that statement matches the informal proof text
is the separate alignment-review lane recorded in
`formalization/FORMALIZATION_STATUS.json`; neither lane flips `lemma_closed`,
prizes, premises, or any landing disposition.
-/
