**C291 isolated negative-control execution report**

All seven requested source mutations were rejected at their intended semantic locations. The unused private custom-axiom carrier compiled, and the copied complete module-origin audit rejected its unused private axiom. All five actual Lean executions are terminal. No further Lean execution is planned by this agent.

Actual executor: OpenAI Codex subagent `c291_field_feasibility`, delegated work for Dylan Roy. This is AI execution and evidence inspection; Dylan Roy did not personally perform this review. The agent inspected the full exact constructor source, fixture generator/runners, all manifests, the selected complete semantic diagnostic blocks, and terminal receipts/log hashes. These are compiler proof-binding controls and an axiom-guard control, not independent mathematical or scientific acceptance.

The source-bound fixture generation is `negative-project/generations/0b581f8569781d82`. Its manifest SHA-256 is `f511a499d1804a3033728cc576e9c6bba0f8954039f811b9ec1fe71cc73df279`. It binds production field SHA-256 `daf0949a14d4ed8bd19fbdc564f0f8c3fad72ed243de73e39d65b2951576919a` and production audit SHA-256 `fea8df29106f295238b3a039bb2aae350167a9ada2326d6d00ba6f6663be52c3`.

| Execution | Actual Lean exit | Seconds | Interpretation |
|---|---:|---:|---|
| Original seven-clone positive baseline | 0 | 201.525 | Compilation succeeded. Original wrapper correctly remains `control_pass=false` because proof printing elided the 21 local-helper references. |
| Separate proof-binding import/print probe | 0 | 197.705 | All 21 exact own-helper references observed with proof printing enabled; original compiled objects unchanged. |
| Seven constructor mutations | 1 | 234.207 | Every intended semantic range rejected; no timeout or import/unknown-identifier failure. |
| Private unused-axiom carrier | 0 | 231.405 | Full source clone plus one unused private axiom compiled without errors or warnings. |
| Copied whole-module axiom audit | 1 | 337.217 | Intended private unused-axiom rejection, no timeout, no false success marker. |

The two-part positive acceptance is `negative-runs/positive-acceptance-0b581f8569781d82/TWO_PART_ACCEPTANCE.json`, SHA-256 `114095a00fbb6c5e56acfa23e43b3eaf13673b1fc9174dcc0f97d84d5d87714c`. It binds the original successful Lean compile and its exact objects to the separate probe. It does not rewrite the original failed wrapper result or recompile the unchanged cloned proofs. Both wrapped positive and mutated source modules retain the original imports and proof bodies and use separate namespaces. They do not import `SourceLifetimeField`; constructor references to their own cloned helpers were observed explicitly.

| Single substantive source edit | Selected source diagnostic | Actual mismatch |
|---|---:|---|
| `F := 0` | 78:16 | Original raw second-moment theorem versus the expected integral of `0 * 0`. |
| `F := F + 1` | 163:16 | Original raw second moment versus the expected shifted product integral. |
| `P := 0` | 241:12 | `IsProbabilityMeasure (smoothLaw d L)` versus `IsProbabilityMeasure 0`. |
| Extra constructor premise `0 < d` | 353:2 | The explicit zero-dimensional consumer receives `0 < 0 → GaussianFieldInterface 0 1` instead of `GaussianFieldInterface 0 1`. |
| Double raw covariance | 370:2 | Original covariance versus twice that covariance. |
| Raw covariance argument `x - y` changed to `x + y` | 455:2 | Original difference covariance versus sum covariance. |
| Quadratic conclusion `0 ≤ Q` changed to `0 ≤ -Q` | 562:2 | Variance nonnegativity versus nonnegativity of negative variance. |

Line numbers above refer to the exact `NegativeConstructorMutants.lean` in the executed generation. Full diagnostics, including dependent recovery errors, remain preserved in its stdout. The designated zero-dimensional consumer error is required separately from its downstream arity/projection errors. No global cosine/sine sign flip is counted as a rejecting control. Every raw clone was reconstructed byte-for-byte from the original source and its sole substantive edit; namespace wrapping is recorded separately.

The axiom rejection is exactly:

```text
forbidden transitive axiom _private.NegativeUnusedAxiom.0.C291Negative.UnusedAxiom.c291UnusedCustomAxiom in _private.NegativeUnusedAxiom.0.C291Negative.UnusedAxiom.c291UnusedCustomAxiom
```

This error occurred at copied audit source line 19. The private axiom occurs exactly once in the carrier source and is not used by the endpoint. The audit retains `setExporting false`, complete module-origin inventory, kernel-declaration checks, and transitive axiom collection. Its stderr contains only the explicitly recorded audit progress lines.

The copied negative audit must not be described as a completed standard-only census: it intentionally stops at the forbidden axiom. Its reported module inventories total 421, including 13 declarations attributed to `NegativeUnusedAxiom`. Its `SourceLifetimeField` inventory contains 11 rather than the production audit's 12; the previously emitted `UniversalLaw.Spec.Lifetime.covQuadForm.eq_1` does not appear in the negative audit's declaration output before rejection. Import-order reassignment of the shared generated equation declaration is a plausible explanation, not a separately established result of this control. The production audit's independent green 409-declaration result remains separate evidence.

All five START/RECEIPT/stdout/stderr quartets were verified. Each archived `RUNNER.py` matches its recorded runner SHA-256; the probe's `IMPORTED_RUNNER.py` also matches. All recorded logs match receipt hashes. Production sources and objects remained unchanged during these runs; dependency metadata and nine repository pins were checked. The main final index is `NEGATIVE_FINAL_INDEX.json`; the detailed hash index is `negative-project/FINAL_NEGATIVE_EVIDENCE.json`.

Historical evidence is retained: the original five-case generation, the earlier seven-case generation against the older audit, preparation-only generation `58c7f2c6f5b4aa24` with its stale-census-string assertion failure, the original positive wrapper's proof-elision failure, and unexecuted generation `e6605ee45163cb9b`. The waiting fresh-baseline wrapper for the last generation was canceled before any Lean child started when the parent selected the import/print probe. No failed receipt was edited.

The parent owns the frozen final source rebuild, standard kernel replay, final master check, independent mutation-verifier consumption, external publication, and custody. This subtask did not run those checks or claim their success. Scientific effect: NONE.
