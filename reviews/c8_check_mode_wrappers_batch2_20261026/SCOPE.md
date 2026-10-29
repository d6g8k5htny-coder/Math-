# C8 check-mode wrappers, batch 2: the planar cap-failure wrapper

Dylan Roy — delegated AI engineering. Actual author: Anthropic Claude, session
`session_015wNj8LPTKXsaT68G3DgPPh` (C8), stage `C8-WRAPPERS-REPAIR-C8-20261026`,
batch 2, pickup Math-#322/6422210000 and its batch-2 line Math-#322/6424054207.
Dylan approved draft PRs for the seven `c8-*` wrappers around this session's
packets, in the author's session at about 16:45Z on 26 October 2026. Scientific
effect NONE; shared-account organizational credit 0. Author-side implementation
only: a separate nonauthor engineering review and a separate integrator are
required. No mathematical acceptance is asserted.

The branch is cut from Math- `main` `7d63d08f`, the merge of batch 1 (Math-#519),
because it extends the same helper, reference file and test file. Batch 1's scope
note, `reviews/c8_check_mode_wrappers_20261026/SCOPE.md`, is unchanged.

## Finding and exact source

01Cz's ledger (Math-#322/6388271177) classifies `c8-cap-failure-coefficient-planar`
as `status_only`. It accepted the baseline `--check --procs 2` on exit status 0
alone, with its stderr discarded and its stdout only echoed, and each mutant
`--check --procs 1 --mutant M` on exit status 1 alone, with its stdout and stderr
discarded. So an unrelated crash, a silent exit 1 or a failure for another reason
counted as an intended rejection.

| Object | Identity |
|---|---|
| Math- `main` at characterization | `1965142e66a067c69ea2b936517226a6bbf2cdd8` |
| Branch base (`main`, the merge of batch 1) | `7d63d08f6cfadfd9c2ef28039a370d741126f9a0` |
| `c8-cap-failure-coefficient-planar.yml` before | blob `f4c7e79161c695502242df9e1172c1ffcdeb1074` |
| `cap_coefficient.py` (unchanged) | blob `cfdaa4d7ceaaf707ed7c066570215862879cce65`, 28,336 B |
| `RESULTS.json` (unchanged) | 6,427 B, SHA-256 `d3de1a20793fbbcbb051b5740af45628627b905827fe2e0d4758ac9e37c36088` |

The packet tree `82e961ec`, the checker blob and the workflow blob are identical
at `1965142e` and at `7d63d08f`. The imported `tools/legacy_json_replay.py` (blob
`854db466`) and `tests/test_legacy_workflow_triggers.py` (blob `c2e37a3a`) are
the blobs every local run below used.

## Repair and preservation

Five files: `tools/check_mode_replay.py`, `tools/check_mode_contracts.json`,
`tests/test_check_mode_workflows.py`, the planar workflow, and this note.

- **`tools/check_mode_replay.py`:** one inventory row, and one `POOLED` row that
  states how the original wrapper ran this checker: the baseline with
  `--procs 2`, each mutant with `--procs 1`, and the mutants two at a time.
  `replay()` keeps that schedule for this family: both baselines first, one at a
  time, then the six mutants on two threads, with each verdict read in submission
  order. The first failing verdict stops the run; children not yet started are
  cancelled, and the at most two already running finish. Each child is checked
  exactly as in batch 1: exit status, empty stderr, and the complete measured
  verdict. The two batch-1 families keep their sequential path unchanged.
- **`tools/check_mode_contracts.json`:** one new family with the measured
  verdicts. The batch-1 families' entries are unchanged.
- **`tests/test_check_mode_workflows.py`:** the family joins the tables. The
  synthetic checker now accepts exactly the arguments each wrapper passed, and
  nothing else. For this family, the inventory test expects both baselines first
  and then the six mutants in any order, and each rejection test also requires
  the error to name the faulty child, since two mutants may run at once. The
  reference custody digest moves with the new family.
- **The workflow:** calls `replay('c8-cap-failure-coefficient-planar', root,
  timeout=2400)` in place of its exit-only loops and thread pool. It gains the
  same earlier contract step and trigger paths as the batch-1 wrappers.

Unchanged: the source block before any child; the action pins, read-only
permissions, `persist-credentials: false`, Python 3.11.16 and the 75-minute job
budget; the per-child timeout (2400 s); the checker arguments; the mutant order;
the two-at-a-time mutant concurrency; the terminal record; the final
`git diff --exit-code`; every packet file.

One behavior changes, on failure only. The old pool's `with` block waited for
every queued mutant before it raised; the helper cancels the mutants not yet
started.

## The contract

The references are complete verdicts measured from the unchanged CLI, never
outputs learned from the invocation under test.

- **Baseline** (`--check --procs 2`): exit 0, empty stderr, and the measured
  verdict `{"check": "ok", "k_values": 6, "c_G(0,2)": ["5324360.4426",
  "5324360.4427"], "c_G(6/5,1/6)": ["35736.7352", "35736.8785"], "mutant": null}`.
  The checker prints it only after all six certified records, every `R(b)` and
  `c_G` enclosure, and the headline and `[CAP] (3)` checks have matched
  `RESULTS.json`.
- **Each mutant** (`--check --procs 1 --mutant M`): exit 1, empty stderr, and
  exactly the verdict that the checker's `require()` prints: `{"check": "FAIL",
  "reason": …, "mutant": M}`.

| Family | Mutants (in submission order) | Measured reason |
|---|---|---|
| `c8-cap-failure-coefficient-planar` | `no-third-jet`, `sign-lo`, `variance-yyy` | `certified record for k = 1/6 differs from RESULTS.json` |

Every mutant fails at the first of the six k values, which the checker certifies
on its own before it starts its pool ("a mutant fails here"). The verdict names
that check and the mutant label, but not which quantity the mutant changed. That
is how this checker reports, and the packet bytes stay unchanged. The contract
therefore pins the first failing check exactly. A crash, a silent exit, stderr
output, a failure at any other check, or a verdict for another label is rejected.

## Execution and non-vacuous regressions

All of the following ran locally on CPython 3.11.15. The characterization ran on
`1965142e`. The tests, the RED control and the real-checker replay ran on this
branch's tree.

- **Characterization:** two separate runs of the unchanged checker, in both
  modes, with the wrapper's exact arguments, each child a separate process
  started from the packet directory. All 8 stdout byte strings of the second run
  equal the first run's, and the normal and optimized stdout are identical. Every
  stderr is empty, and the exit statuses are as above. These runs started more
  children at once than the wrapper does, which changes only the timing: a
  baseline took 14 to 16 minutes and a mutant 3 to 4 minutes.
- **The real checker through the helper:** `replay()` on the actual packet, run
  as the workflow step runs it, gave `protocol_ok` for all 8 children in 36.4
  minutes. Each baseline took about 13.5 minutes, one at a time, and the six
  mutants then took 9.4 minutes, two at a time. Every stdout digest equals the
  characterized one. The old wrapper's hosted step took about 35 minutes on its
  last two runs, on the same schedule.
- **This test file:** 13 tests OK in both modes, as the workflow step runs it
  (this family alone, about 9 seconds per mode), for all three families (about
  32 seconds per mode), and under the full suite's discovery.
- **RED control:** the same tests, with `CHECK_MODE_SOURCE_ROOT` set to unchanged
  `main` `1965142e`, give 42 false acceptances in each mode:

  | Test | planar |
  |---|---|
  | crashes | 6 |
  | silent exits | 6 |
  | wrong reasons | 6 |
  | wrong mutant label | 2 |
  | baseline faults (stderr, wrong value, missing key, malformed) | 8 |
  | JSON faults (stderr, duplicate, NaN, trailing, extra, missing, malformed) | 14 |

  The wrong exit statuses were already rejected there. Those four subtests fail
  there only on the new requirement that the error name the faulty child. The
  trigger, step and import tests fail there too, as expected. The inventory test
  passes there, because the old wrapper ran the same schedule.
- **Full suite, normal mode:** 1,039 tests, as with batch 1 alone. The same 37
  tests fail with and without this change and on `1965142e` (167 failures and 3
  errors). All of them fail at git's `--no-lazy-fetch` capability check, because
  local git is 2.43.0. None is in the new or legacy test files: all 13 new tests
  and the 7 legacy trigger tests pass.

## Limits

- The local interpreter is 3.11.15, not the hosted 3.11.16. The hosted run is the
  qualifying execution.
- The synthetic fixture uses a one-entry pin list and a minimal manifest. The real
  pins run only in the real hosted job.
- This is batch 2 of seven. `c8-lifetime-difference-constant`,
  `c8-theorem-a-constants-d3`, `c8-theorem-a-constants-planar` and
  `c8-torus-vanishing-remainder` keep their own stages.
