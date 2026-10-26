# C8 check-mode wrappers, batch 1: authenticate the intended verdicts

Dylan Roy — delegated AI engineering. Actual author: Anthropic Claude, session
`session_015wNj8LPTKXsaT68G3DgPPh` (C8), stage `C8-WRAPPERS-REPAIR-C8-20261026`,
pickup Math-#322/6422210000. Dylan approved draft PRs for the seven `c8-*`
wrappers around this session's packets, in the author's session at about 16:45Z
on 26 October 2026. Scientific effect NONE; shared-account organizational credit 0.
Author-side implementation only: a separate nonauthor engineering review and a
separate integrator are required. No mathematical acceptance is asserted.

The branch is cut from Math- `main` `1965142e`, the merge of #518. The
repository-wide suite that runs these new tests needs #518's 45-minute budget.

## Finding and exact source

01Cz's ledger (Math-#322/6388271177) classifies both wrappers as `status_only`.
Each mutant was accepted on exit status 1 alone, with its stdout and stderr
discarded. The baseline `--check` was accepted on exit status 0 alone, with its
stderr discarded and its stdout only echoed. So an unrelated crash, a silent exit
1 or a failure for another reason counted as an intended rejection.

| Object | Identity |
|---|---|
| Math- `main` at characterization | `f0f90857dcf7586e5195fcb05c0058657fba4003` |
| Branch base (`main`, the merge of #518) | `1965142e66a067c69ea2b936517226a6bbf2cdd8` |
| `c8-cap-failure-coefficient-dims.yml` before | blob `afb65fea440ffde64731d5d16bc3aafb7aa2d250` |
| `c8-normalizer-floor-planar.yml` before | blob `c3eeb1758cee919bac592db55c190bb76ddfd4e1` |
| `cap_coefficient_dims.py` (unchanged) | blob `af7e9d103f962f613c57f5e695f030165e348beb`, 24,393 B |
| `floor.py` (unchanged) | blob `29f1b512062fda6b3565429e9fe53e91b9b3c2f8`, 44,876 B |
| dims `RESULTS.json` (unchanged) | 6,837 B, SHA-256 `1406d5138ac3d33bcb0358f6a3005a67e3a4a2dbfc2c43bc3ac2593667550608` |
| normalizer `RESULTS.json` (unchanged) | 1,874,499 B, SHA-256 `a2c4d6890cc9ab0984605f78ccf89b38d93b9515b8d70a6d5e5c3d417b4b3882` |

Both packet trees, `4866eab3` (dims) and `f734b522` (normalizer), are identical at
`f0f90857` and at `1965142e`, and so are both workflow blobs. The imported
`tools/legacy_json_replay.py` (blob `854db466`) and
`tests/test_legacy_workflow_triggers.py` (blob `c2e37a3a`) are the blobs every
local run below used.

## Repair and preservation

Six files: `tools/check_mode_replay.py`, `tools/check_mode_contracts.json` and
`tests/test_check_mode_workflows.py` (all new), the two workflows, and this note.

`tools/check_mode_replay.py` follows `tools/legacy_json_replay.py`, and it reuses
that module's strict JSON reader and structural comparison instead of copying
them. For each family it binds the checker's git blob and the `RESULTS.json` size
and digest. It then runs the fixed inventory in both modes, from the packet
directory, exactly as the old wrappers did: `--check` and `--check --mutant M`.
For every child it requires:

- the exact exit status: 0 for the baseline, 1 for each mutant;
- empty stderr;
- one strict JSON verdict on stdout, structurally equal to the verdict measured
  from the unchanged checker.

Each workflow now calls `replay()` in place of its own exit-only loops. It gains
one earlier step that runs `tests/test_check_mode_workflows.py` for its own family
in both modes. It also gains the trigger paths for the helper and its inputs
(`tools/**`, `tools.py`), for that test, and for `tests/test_legacy_workflow_triggers.py`,
whose strict path reader the test reuses.

Unchanged:
- the source block before any child: the packet manifest and the main-resident
  pins;
- the action pins, read-only permissions, `persist-credentials: false`, Python
  3.11.16 and the job budgets;
- the per-child timeouts (600 s and 1500 s), the mutant order within each mode
  and the terminal record;
- the final `git diff --exit-code`;
- the normalizer's `workflow_dispatch` full-regeneration job;
- every packet file.

One ordering detail changes, in the dims wrapper only. It ran both baselines
before any mutant. The helper runs each mode's complete inventory in turn, as the
normalizer wrapper already did, and as the characterization runs measured it.
Each child is still a separate process started from the packet directory.

## The contract

The references are complete verdicts measured from the unchanged CLIs, never
outputs learned from the invocation under test.

- **Baseline:** exit 0, empty stderr, and the measured `{"check": "ok", …,
  "mutant": null}` verdict, which carries the certified values that `--check` has
  already compared with `RESULTS.json`.
- **Each mutant:** exit 1, empty stderr, and exactly the verdict that the checker's
  `require()` prints: `{"check": "FAIL", "reason": …, "mutant": M}`.

| Family | Mutants (in run order) | Measured reason |
|---|---|---|
| `c8-cap-failure-coefficient-dims` | `no-y-tail`, `r3-one`, `no-bp`, `frob-omega-off` | `certified values differ from RESULTS.json` |
| `c8-normalizer-floor-planar` | `swap-minmax`, `drop-torus-error`, `sign-saddle` | `exact replay of low r=[63/512,1/8],b=[0,1/8],k=[1/2,3/4]` |

Within each family every mutant fails the same first check. The verdict names
that check, and the mutant label, but not which quantity the mutant changed. That
is how these checkers report, and the packet bytes stay unchanged. The contract
therefore pins the first failing check exactly. A crash, a silent exit, stderr
output, a failure at any other check, or a verdict for another label is rejected.

## Execution and non-vacuous regressions

All of the following ran locally on CPython 3.11.15. The characterization and the
real-checker replay ran on #518's head `b0dd89f`. The tests and the RED control ran
again on `1965142e`.

- **Characterization:** two separate runs of the unchanged checkers, in both
  modes. Every normal and optimized stdout is byte-identical, every stderr is
  empty, and the exit statuses are as above. Locally, the normalizer baseline
  takes about 6 minutes per mode, each normalizer mutant 28 to 33 seconds, and
  each dims child under half a second.
- **Real checkers through the helper:** `replay()` on both actual packets gave
  `protocol_ok` for every child: 10 for dims in 2.5 seconds and 8 for the
  normalizer in about 14.5 minutes. Every stdout digest equals the characterized
  one.
- **This test file:** 13 tests OK in both modes, both as the workflow step runs it
  and under the full suite's discovery, about 23 seconds per mode for both
  families.
- **RED control:** the same tests, with `CHECK_MODE_SOURCE_ROOT` set to unchanged
  `main`, give 90 false acceptances:

  | Test | dims | normalizer |
  |---|---|---|
  | crashes | 8 | 6 |
  | silent exits | 8 | 6 |
  | wrong reasons | 8 | 6 |
  | wrong mutant label | 2 | 2 |
  | baseline faults (stderr, wrong value, missing key, malformed) | 8 | 8 |
  | JSON faults (stderr, duplicate, NaN, trailing, extra, missing, malformed) | 14 | 14 |

  The wrong exit statuses were already rejected there and still are. The trigger,
  step and import tests fail there too, as expected, and so does the dims
  inventory-order check, because the old dims wrapper ran both baselines first.

## Limits

- The local interpreter is 3.11.15, not the hosted 3.11.16. The hosted runs are
  the qualifying execution.
- The synthetic fixture uses a one-entry pin list and a minimal manifest. The real
  pins run only in the real hosted job.
- This is batch 1 of seven. `c8-cap-failure-coefficient-planar`,
  `c8-lifetime-difference-constant`, `c8-theorem-a-constants-d3`,
  `c8-theorem-a-constants-planar` and `c8-torus-vanishing-remainder` keep their
  own stages.
