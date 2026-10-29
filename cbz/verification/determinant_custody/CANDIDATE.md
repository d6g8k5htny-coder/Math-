# Current determinant repair candidate

This candidate extends the real-Git-tested initial source guard with sanitized Lean/Git child environments, refusal of nested build and evidence symlinks, and a reason-bound mutation grader. It retains all original component assertions; synthetic orchestration fixtures mock the new source-boundary helper because those fixtures do not execute Lean or claim source custody. The separate real-Git custody tests exercise the boundary itself.

Observed prior results: initial11 controls passed in both modes on2c039fe8; inherited Lean-path exposure failed exactly one of15 tests in both modes on4f11c870. The first nested-build fixture at8689e9 produced a fixture error, not a valid red; its corrected and later symlink/grader/Git-child tests were committed before this candidate and are still pending. Full retained suite, all named source mutants, the grader's own mutations, and actual Lean/kernel execution are pending. No final success is claimed.

Pre/post source checks assume no transient change restored between observations. Dependency build caches are reused, and runtime authenticity and source-to-cached-object correspondence require separate evidence. Git and SHA-256 source bindings rely on their collision-resistance assumptions. These are limits on the source-custody claim, not mathematical axioms.
