# Package declaration admission hardening

Scientific effect: **NONE**. Engineering successor for RF-GATE-01 (Math- issue #310), implemented by OpenAI / GPT-5.6 Sol in `round11-gate-hardening-20261005`. The #309 mathematical declarations are preserved.

The predecessor used a column-zero theorem/lemma regex. Lean accepts declarations outside it, so declarations could compile outside manifest and axiom coverage. This successor intentionally enforces a conservative grammar rather than claiming to parse arbitrary Lean: one `namespace ResearchFormalCoreR1`; column-zero `theorem`, `lemma`, `def`, or `noncomputable def`; declaration-bearing alternatives and nested namespaces fail closed after comments and strings are removed.

The manifest records all package declarations, not just theorem targets. Execute-time transitive-axiom auditing covers definitions as well as theorems; the historical target-only `axioms` receipt field is retained and `declaration_axioms` is additive. Lean4.34.1, dependency pins, leanchecker and all five existing negative controls are unchanged.

Test-first predecessor `82f4de13f0e41253740d880f26fdc63fda772323` / run37394891831 failed with nine intended regression failures before Lean installation. A successor must pass those regressions, complete Python suites in both modes, source identity and the actual pinned Lean/leanchecker/axiom/type workflow. This is engineering evidence, not independent mathematical alignment or reviewer authentication.
