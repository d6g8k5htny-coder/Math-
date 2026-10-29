# Manual readings of the lexical Layer A signals

The generator flags lines; a reader decides what they are. These readings cover every open PR whose
record has `signals_total > 0` at the 2026-10-29 17:17Z observation. Performer: Anthropic Claude,
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
