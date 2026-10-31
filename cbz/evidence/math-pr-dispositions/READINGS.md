# Manual readings of the lexical Layer A signals

The generator flags lines; a reader decides what they are. Section 1 covers every open PR whose record
had `signals_total > 0` at the 2026-10-29 17:17Z observation; section 2 covers the rows that gained
signals by the committed 23:05:51Z snapshot (`dispositions.json`), so the final snapshot is manually
covered too (MTW finding on #529, `READINGS.md:3`). Performer: Anthropic Claude,
session `session_01NMeKEismAyeqgdB4sy2NJU` (Claude01N). A reading is a classification of the flagged
lines only; it is not a review of the PR and certifies nothing about the mathematics.

| PR(s) | Signal | Flagged lines (merge-base..head) | Reading |
|---|---|---|---|
| #482, #487, #491, #496, #497, #504, #514 | `lean_admit_added` = 3 | Three English sentences inside a Lean doc-comment / string block, all the same anchor text: `Anchor: "These densities admit versions with"`, `… lifetime densities admit versions \`νc\`, \`νe\` …`, `… essential global maximum excluded) admit`. | **Prose, not a tactic.** The verb "admit" in a quoted source sentence. No `admit` tactic is added by any of these PRs. Not a Layer A1 signal. |
| #482 | `skips_added` = 1 | `self.skipTest("not a git checkout")` in a new test. | An environment guard: the test needs a git checkout and declares that it did not run otherwise. It is not a silenced failing test. A reader of the PR should confirm the guarded test runs in CI (where the checkout exists). |
| #482 | `float_in_certificate_code_added` = 1 | Comment `# census required 458.5s …` and version strings `'4.34.1'`, `leanprover/lean4:v4.35.0` in a path whose name matches `check`/`verify`. | Decimal literals inside a comment and version strings; no arithmetic on bounds. Not an A3 signal. |
| #491, #496, #497, #504 | `float_in_certificate_code_added` = 7 (stack root #491; inherited by the stacked PRs) | `LEAN_VERSION = '4.34.1'`, `'leanprover/lean4:v4.34.1'` comparisons/writes, and `timeout=0.1` in `c299_hosted_verify.py` and its tests. | Version strings and a subprocess timeout. No bound is computed. Not an A3 signal. |

Net effect on the recommended dispositions: none of the flagged lines is a Layer A hazard, so the
integrate candidates #482 and #487 need no Layer A repair before integration; their remaining
conditions are the ordinary ones (fresh green `math-downstream-gates` on the current base, and the
integrator's own read).

## 2. Rows with signals in the committed 23:05:51Z snapshot (Math- `main` `9f8dbb4d`)

Read on the heads recorded in `dispositions.json`; all are `ACTIVE-OWNER-LANE` rows (their lanes'
call), so the reading changes no disposition. Flagged lines, merge-base..head:

| PR | Head | Signal | Flagged lines | Reading |
|---|---|---|---|---|
| #529 (this PR) | `c6d44917` | `skips_added` = 2 | `@unittest.skip("later")`, `self.skipTest("later")` inside the `PY_DIFF` **fixture string** of `test_disposition_lib.py`. | Test data for the scanner's own skip detector, not a skipped test. |
| #530 | `c48194fb` | `float_in_certificate_code_added` = 3 | `TOOLCHAIN = "leanprover/lean4:v4.34.1"` and a `# Lean 4.34.1 …` comment in `tools/cbz_kernel_gate.py`; `(F(1, 2), "k=0.5")` in `tools/check_c8_quarantine.py`. | Version strings and a `Fraction(1, 2)` labelled `"k=0.5"` in a string. No float arithmetic. Not an A3 signal. |
| #536 | `0dd9f215` | `skips_added` = 1 | `self.skipTest('controlled skip')` inside a quoted mutant-source string in `frontiers/determinant_moment_20261025/tests/test_cbz_mutation_runner.py`. | A planted mutant that the mutation runner must detect; test data, not a skipped test. |
| #541 | `94a78d8b` | `skips_added` = 1 | `self.skipTest('skip')` in `tests/test_lifetime_dd_node_oracle.py`. | A real `skipTest` call in a new test; its guard condition decides whether a case is silently skipped. **A reader of #541 should confirm the condition is an environment guard, not a silenced assertion** (A5). Reported to that lane through the row, not repaired here. |
| #542 | `3f27e9d3` | `lean_sorry_added` 6, `lean_admit_added` 7, `lean_axiom_added` 1, `lean_native_decide_added` 6, `skips_added` 2, `float…` 12 | All `sorry`/`native_decide` hits are inside doc-comments or backticked prose (`No \`sorry\`, \`native_decide\`, …`) of `P15Elementary.lean` copies; all `admit` hits are the prose "admit genuinely empty local covers" in `Amalgamation.lean` copies; the one `axiom` is `axiom OwnedKernelControl.Bad : False` in `…/generated/OwnedKernelAudit/Control_axiom.lean`, a generated **negative control** by name and location; the two skips are OS-permission environment guards (`root bypasses directory permission restrictions`); the float hits are `time.sleep(0.01)`, `stop.wait(0.05)`, deadlines in seconds, `import math` in process-supervision helpers, and version/identity strings. | Prose, a deliberate negative-control axiom outside any proof module, environment guards, timing constants. No Layer A hazard among the flagged lines. The PR's many evidence copies multiply the counts (the same prose line appears in 9 frozen copies). |
