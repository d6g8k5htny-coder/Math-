# Reconnaissance memo — 25 September 2026

Scope: implement a small algebraic SMT pilot for existing P15 source obligations, not discover a new P15 theorem. Scientific effect NONE. No novelty or priority claim.

Inspected primary documentation:

1. Microsoft Z3 Guide, Arithmetic: https://microsoft.github.io/z3guide/docs/theories/Arithmetic/ . Real sorts represent mathematical reals rather than floating point. Division at zero is underspecified, so the curvature obligation uses a cleared denominator and separately proves it positive. Unknown is never interpreted as success.
2. Z3 C API: https://z3prover.github.io/api/html/group__capi.html . Used context/configuration, SMT-LIB evaluation, error-handler, version, and lifetime-management interfaces. The available native runtime permits a Python-standard-library ctypes wrapper without requiring a Python Z3 package.
3. Lean reference, Validating a Lean Proof: https://lean-lang.org/doc/reference/latest/ValidatingProofs/ . Kernel proof checking and the correspondence between a formal statement and intended mathematical claim are separate validation questions. This pilot does not run Lean or claim proof-assistant verification.

Internal source actually read: Math-/frontiers/full_price_20260924/PROOF.md at baca69c394ab42130c61771bee74e808703f1ce7; byte identities in SPEC.json. F5, F10, F11, and section 6 supply the algebraic targets. The full hazard interpolation, probability model, palette coverage, and sharpness remain external analytic obligations. A strict F10 endpoint strengthening is false at p=1; the actual p_star application is unaffected.

Outcome: reuse established SMT technology; verify a tightly scoped source translation with explicit false variants and non-vacuous premises. Export solver proof objects while explicitly retaining solver/translation trust. This bounded reconnaissance does not establish comprehensive historical coverage or novelty.
