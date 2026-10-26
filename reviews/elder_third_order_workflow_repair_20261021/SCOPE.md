# Elder third-order wrapper: authenticate the intended rejection

Dylan Roy — delegated AI engineering. Actual author: Anthropic Claude, session
`session_015wNj8LPTKXsaT68G3DgPPh` (C8), stage `E3-WRAPPER-REPAIR-C8-20261021`,
pickup Math-#322/6326697003; Dylan approved this repair and its draft PR in the
author's session. Scientific effect NONE; shared-account organizational credit 0.
Author-side implementation only. A separate nonauthor engineering review and a
separate integrator are required. Because this changes a workflow, a merge also
needs Dylan's decision for this pull request. No mathematical acceptance or proof
correction is asserted.

## Finding and exact source

The finding is the elder-third-order case of AUD-LEGACY-MUTANT-01 (#322). It was
established by another session's full-shell diagnostic, Math-#322/6325841078
(OpenAI GPT-6 Astra Pro), which this repair credits. The complete wrapper
accepted an unrelated crash or a silent exit 1 at every M1–M8 stage in both
modes, wrong mutant output, unexpected stderr, baseline stderr and an M9 with
the wrong streams. The baseline kept only the child's stdout, and every mutant
and M9 kept only its exit status. The checker itself was not reported to crash,
and no theorem is refuted by a wrapper defect.

| Object | Identity |
|---|---|
| Base, Math- `main` | `180d6406b0a51b268a152241a70bde6a1b39a142` |
| Workflow before this change | blob `f5a06fcef3c20239a64b86b27370c3daa7c37a52` |
| `e3_check.py` (unchanged) | blob `b5f04a87f2d2984280bf394bd4e5f3db560e1b33`, 31,425 B |
| `RESULTS.json` (unchanged) | 3,533 B, SHA-256 `3390d0fc2fd74138fb34b6d5447c7d56191ffc4257fe9ba3985786d1ab661fb1` |

The workflow blob is the diagnostic's `f247407330dd068880bc68f66520f95d8fee2296`
plus only the `setup-python` pin update of `2c041de` (24 October). The checker,
`RESULTS.json` and `SOURCES.json` are byte-identical at the reference file's
`source_cut` (`b25cac0b`) and at the base.

## Repair and preservation

Six files: the workflow, `tools/legacy_json_replay.py` (one inventory row and the
docstring's family count), `tools/legacy_json_contracts.json` (one new family and
one provenance sentence), `tests/test_legacy_json_workflows.py`,
`tests/test_legacy_workflow_triggers.py` (one family row) and this note.

The workflow now calls the existing `replay()` that far-elder, local-pairing and
c6-cluster already use, instead of its own exit-only loop. It gains the same two
earlier steps those workflows run: the trigger-coverage test, and the complete
shell rejection contract for its own family, both in both Python modes. It also
gains the same trigger paths. The comment that sat inside the path list moved
above `'on':` with the same meaning, because the trigger test's path reader
accepts only plain quoted rows.

Unchanged:
- the whole source-verification block that runs before any child: packet
  membership and file identities, the tree-bound merged sources, and the
  API-bound unmerged sources with their drift gate;
- the action pins, read-only permissions, `persist-credentials: false`,
  Python 3.11.16, the 10-minute job budget and the 600-second child budget;
- the terminal NONE/false record and the final `git diff --exit-code`;
- every packet file (`e3_check.py`, `PROOF.md`, `RESULTS.json`, `SOURCES.json`,
  `README.md`) and the other three families' reference entries.

## The contract

The references are complete reports measured from the unchanged CLI, never
outputs learned from the invocation under test.

- **Baseline:** exit 0, empty stderr, and stdout byte-identical to `RESULTS.json`.
- **M1–M8:** exit 1, empty stderr, and one strict JSON object structurally equal
  to the measured report: the same keys, types, values and list order.
- **M9:** exit 2, empty stdout, and stderr exactly `unknown mutant label\n`, which
  is the checker's own message for an unknown label.

The references were measured under CPython 3.11.15 in both modes, twice, with
identical bytes each time. Each report fails exactly the check whose source branch
the mutant changes, and every other check is byte-identical to the baseline's:

| Mutant | Failing check |
|---|---|
| M1, M8 | `X1_exponent_ledger` |
| M2 | `X3_margins` |
| M3 | `X4_decision_1d` |
| M4 | `X5_weighted_taylor` |
| M5 | `X6_lemma_S` |
| M6 | `X8_lemma_S_prime_algebra` |
| M7 | `X9_lemma_H_exact_form` |

That is an observation, not a rule. The protocol compares whole reports, so it
assumes no exactly-one-failed-check rule.

## Execution and non-vacuous regressions

All of the following ran locally on CPython 3.11.15 at the base above.

- **Real checker:** `replay('elder-third-order', …)` on the actual packet gave
  20/20 `protocol_ok`: the baseline, M1–M8 and M9 in both modes.
- **Trigger test:** OK in both modes.
- **Shell rejection contract for this family** (`LEGACY_TEST_FAMILY=elder-third-order`):
  15 tests OK in both modes, about 42 seconds each.
- **RED control:** the same tests, with `LEGACY_SOURCE_ROOT` set to the unchanged
  `main`, give 72 false acceptances:

  | Test | False acceptances |
  |---|---|
  | crashes | 16 |
  | silent exits | 16 |
  | wrong reasons | 16 |
  | JSON-contract faults | 18 |
  | unknown-label diagnostics | 4 |
  | baseline stderr | 2 |

  The valid inventory, wrong exits, source guards and exact baseline bytes were
  already enforced before this change, and those tests pass there too.
- **Budget:** past hosted runs of this workflow took about 3 to 5.5 minutes. The
  two new steps add about 1.5 minutes locally.

## Limits

- The local interpreter is 3.11.15, not the hosted 3.11.16. The hosted run is the
  qualifying execution.
- The synthetic fixture exercises the source-verification block with empty
  unmerged-source lists. The API-bound dependency path runs only in the real
  hosted job.
- This repairs one wrapper. Other wrappers named in #322 keep their own stages.
