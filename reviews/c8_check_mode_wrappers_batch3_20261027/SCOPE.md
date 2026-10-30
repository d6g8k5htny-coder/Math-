# C8 check-mode wrappers, batch 3: the planar Theorem A constants and torus remainder wrappers

Dylan Roy — delegated AI engineering. Actual author: Anthropic Claude, session
`session_015wNj8LPTKXsaT68G3DgPPh` (C8), stage `C8-WRAPPERS-REPAIR-C8-20261026`,
batch 3, pickup Math-#322/6422210000 and its batch-3 lines Math-#322/6426350379
and, after two lapses, Math-#322/6502862532. Dylan approved draft PRs for the seven `c8-*` wrappers
around this session's packets, in the author's session at about 16:45Z on 26
October 2026. Scientific effect NONE; shared-account organizational credit 0.
Author-side implementation only: a separate nonauthor engineering review and a
separate integrator are required. No mathematical acceptance is asserted.

The branch is cut from Math- `main` `9f8dbb4d`, which includes batch 2
(Math-#520, merged as `e877242c`), because it extends the same helper, reference
file and test file. The scope notes of batches 1 and 2 are unchanged.

## Finding and exact source

01Cz's ledger (Math-#322/6388271177) classifies both wrappers as `status_only`:

- `c8-theorem-a-constants-planar` accepted its two baselines on exit status 0
  alone, with stderr discarded and stdout only echoed, and each mutant on exit
  status 1 alone, with its stdout and stderr captured and thrown away.
- `c8-torus-vanishing-remainder` accepted its baseline on exit status 0 alone and
  each mutant on `p.wait() == 1` alone, with the mutants' stdout and stderr sent
  to `/dev/null`.

So an unrelated crash, a silent exit 1 or a failure for another reason counted as
an intended rejection, and the baselines' verdicts were never compared. The ledger
read the workflow blobs `3a5ee3eb` and `ccf71286` at `d1f6ad28`. The blobs below
differ from those only in the `actions/setup-python` pin (`2c041de`), so the
classification still applies.

| Object | Identity |
|---|---|
| Math- `main` at characterization | `4a0d51bbd06f0d9ac731a1d1df38f25999797135` |
| Branch base (`main`, after batch 2's merge `e877242c`) | `9f8dbb4d18b9f3ebd9ffac6b0caa42df9f343966` |
| `c8-theorem-a-constants-planar.yml` before | blob `85fffc7938dd7daae3ab921d2d957d1a2ab7931a` |
| `c8-torus-vanishing-remainder.yml` before | blob `3c06386130f3c7e2c36b9b39ae274017c8648f5a` |
| `theorem_a.py` (unchanged) | blob `ae279e9015483a666ece8deb2544cbc458a5e270`, 52,864 B |
| theorem-A `RESULTS.json` (unchanged) | 150,257 B, SHA-256 `b4a77fd298297f6dfe077748d32b66f1fd209130443d2eaceea4463ef063c0fe` |
| `theorem_v.py` (unchanged) | blob `5fd6b75df48940f293f0c112c1005418dcd75bde`, 41,036 B |
| torus `RESULTS.json` (unchanged) | 405,837 B, SHA-256 `395171fac7e6656c8fa4e6ef518633f99e0921d2d83bf7317608fe0cd73983a6` |
| torus `theorem_b.py` (unchanged, loaded) | blob `36b39dbd33ef2e6d277ce1c3820b3f0d6659d779`, 53,141 B |
| torus `engine_e2.py` (unchanged, loaded) | blob `ae279e9015483a666ece8deb2544cbc458a5e270`, 52,864 B |
| torus `engine_e3.py` (unchanged, loaded) | blob `267890232119b35206be7a8cc74d730de9a68644`, 76,209 B |

The packet trees (`95d1459b` and `04fc5584`) and both workflow blobs are
identical at `4a0d51bb` and `9f8dbb4d`. As the torus
`SOURCE_MAP.json` pins them, the three loaded files are byte-identical packet
copies: `theorem_b.py` of the lifetime-difference packet's Theorem L certificate
(Math-#215), `engine_e2.py` of `theorem_a.py` (Math-#206), and `engine_e3.py` of
the d = 3 packet's `theorem_a3.py` (Math-#212). The imported
`tools/legacy_json_replay.py` (blob `854db466`) and
`tests/test_legacy_workflow_triggers.py` (blob `c2e37a3a`) are the blobs every
local run below used, except `tools/legacy_json_replay.py`: Math-#312 (on
`main` since `8151f592`) changed it to blob `1aa66bb3`, in `_unknown_stderr()`
only. `ProtocolError`, `strict_json` and `_same`, the three names the helper
imports, are byte-identical in both blobs and do not call it. The tests and the
RED control below ran on this branch's tree, with `1aa66bb3`.

## Repair and preservation

Five files: `tools/check_mode_replay.py`, `tools/check_mode_contracts.json`,
`tests/test_check_mode_workflows.py`, the two workflows, and this note.

- **`tools/check_mode_replay.py`:**
  - Two inventory rows, and a `PLANNED` set for families whose wrapper ran a
    child list other than the batch-1 and batch-2 shapes. `_plan()` restates
    each one with its arguments, timeouts and concurrency:
    - theorem-A, one child at a time: normal `--check-full --procs 2`
      (3600 s), optimized `--check --procs 2` (3600 s), then each mutant in
      normal mode only as `--check --procs 2 --mutant M` (1800 s);
    - torus, in each matrix job: `--check` (3600 s), then all five
      `--mutant M` at once (3600 s each), which take no `--check`.
  - `PER_JOB_MODE`: the torus wrapper ran one interpreter mode per matrix job,
    so `replay()` takes that job's `FLAGS` and runs that mode only. Any other
    family refuses `flags`, and a `PLANNED` family refuses a `timeout`.
  - `STDERR_REJECTIONS`: the torus checker rejects with `SystemExit('FAIL: …')`:
    exit 1, nothing on stdout, and one line on stderr. For it a mutant must
    match that line byte for byte; its success line is the JSON
    `{"object": …, "check": "passed", "scientific_effect": "NONE"}`.
  - `LOADS`: the torus checker loads `theorem_b.py`, which loads `engine_e2.py`
    and `engine_e3.py`. The reference file binds their git blobs as it binds
    the checker's, so a change to any of them needs a new characterization. No
    earlier family's checker loads another packet file.
  - The children of a stage run through one `_stage()`: one at a time, or on
    a thread pool with verdicts read in submission order. The batch-1 and
    batch-2 families keep their order, arguments, timeouts, concurrency and
    checks; their code path is refactored into `_stage()` and is covered by
    the same tests as before.
- **`tools/check_mode_contracts.json`:** two new families with the measured
  verdicts. A `PLANNED` family stores one baseline verdict per mode. The
  earlier families' entries are unchanged.
- **`tests/test_check_mode_workflows.py`:** the families join the tables.
  `groups()` restates each wrapper's child list on its own, apart from the
  helper. The synthetic checker accepts exactly the arguments each wrapper
  passed in each mode, and nothing else. A matrix family is tested once per
  job, with that job's `FLAGS`. New tests: the stderr channel (stdout output,
  stderr output, wrong exit), and rebound sources (a changed checker or loaded
  file whose manifest row moved with it must fail before any child starts).
  The custody test also requires every other Python file in each packet to be
  a bound loaded source. The reference custody digest moves with the new
  families.
- **The workflows:** each calls `replay(...)` in place of its exit-only child
  loops (`replay('c8-torus-vanishing-remainder', root, flags=flags)` for the
  matrix job), and gains the same earlier contract step and trigger paths as
  the batch-1 and batch-2 wrappers.

Unchanged: the source block before any child; the action pins, read-only
permissions, `persist-credentials: false`, Python 3.11.16, the matrix and the
120-minute job budgets; the checker arguments, the per-child timeouts, the
mutant order and concurrency; the terminal records; the final
`git diff --exit-code`; every packet file.

Two behaviors change, on failure or timing only:

- The old torus wrapper raised at the first mutant that did not exit 1 and left
  the other four running; the helper waits for them before it raises.
- Each torus mutant's 3600 s now counts from its own start. Before, a later
  mutant's wait began only after the earlier waits returned.

## The contract

The references are complete verdicts measured from the unchanged CLI, never
outputs learned from the invocation under test.

**`c8-theorem-a-constants-planar`:**

- **Baselines:** exit 0, empty stderr, and the measured verdict
  `{"check": "ok", "bands_replayed": N, "C_table": {…}, "C_table_side24": {…},
  "mutant": null}`, with all seven entries of each `C` table as `RESULTS.json`
  stores them (for example `"1/512": "54156592391/10000"`, the README's
  `C(1/512) = 5415659.2391`):
  - normal `--check-full --procs 2`: `N = 153`, every band;
  - optimized `--check --procs 2`: `N = 11`, the sampled bands.

  The checker prints it only after the canonical layout, the parameters, the
  band list, every replayed band record, both `C` tables and the
  sharp-coefficient floors have matched `RESULTS.json`.
- **Each mutant** (normal `--check --procs 2 --mutant M`): exit 1, empty stderr,
  and exactly the verdict its `require()` prints, `{"check": "FAIL", "reason": …,
  "mutant": M}`.

| Mutants (in order) | Measured reason |
|---|---|
| `no-delta`, `cap-half`, `no-zfloor-correction`, `no-om-term` | `band 0 (['0', '1/536870912']) differs from RESULTS.json` |

`--check` computes its 11 sampled bands under the mutant and then compares them
in index order, so every mutant fails at band 0, the band `[0, 2^-29]`. The
verdict names that band and the label, not which quantity the mutant changed.
That is how this checker reports, and the packet bytes stay unchanged. The
contract therefore pins the first failing check exactly. A crash, a silent exit,
stderr output, a failure at any other check, or a verdict for another label is
rejected.

**`c8-torus-vanishing-remainder`**, in each mode:

- **Baseline** (`--check`): exit 0, empty stderr, and the measured verdict
  `{"object": "CL-C8-TORUS-VANISHING-REMAINDER-20261001-v1", "check": "passed",
  "scientific_effect": "NONE"}`, the same in both modes.
- **Each mutant** (`--mutant M`): exit 1, empty stdout, and exactly the stderr
  line `FAIL: replay differs from RESULTS.json`, for `torus-const-only`,
  `exp-radius`, `no-lin`, `no-om-term` and `coupling-half`, the same in both
  modes.

Each torus mutant passes the checker's twelve internal `require()` checks and
fails only at the final comparison of its whole replay with `RESULTS.json`. The
line therefore shows that the mutated certificate ran to the end and changed the
stored result, not which quantity changed. That is how this checker reports, and
the packet bytes stay unchanged. A crash (its traceback is on stderr), a silent
exit, any stdout, any other stderr, or a failure at an internal check is
rejected.

## Execution and non-vacuous regressions

All of the following ran locally. The characterization ran on 28 October on
`4a0d51bb`, on CPython 3.11 (that container's patch release was not recorded).
The tests and the RED control ran on 29 October on this branch's tree, on
CPython 3.11.17. A first, interrupted pass on 27 October (CPython 3.11.15, on
`1965142e`, the same packet trees) measured the same verdicts: its run-1
contract is byte-identical to this one.

- **Characterization:** two separate runs of the unchanged checkers, with the
  wrappers' exact arguments, each child a separate process started from its
  packet directory. All 18 stdout and stderr byte strings of the second
  run equal the first run's, and the exit statuses are as above. The
  reference file built from them is 5,677 B, SHA-256
  `be7415ca2ca6d2df0bca4eab12026fffd985f8a79a12863e4cfa7a8e0bff52dd`. These runs
  started the two families side by side, which changes only the timing: in
  run A, theorem-A's `--check-full` took 37 minutes beside the torus children,
  its sampled `--check` 2.0 minutes, and each mutant 1.0 to 2.4 minutes; a
  torus baseline took about 5 minutes, and the five mutants about 8 to 9
  minutes at once.
- **The real checkers through the helper:** the hosted jobs at this head run
  them, and they are the qualifying execution. Local runs, as the workflow
  steps run them, are recorded in the pull request.
- **This test file:** 15 tests OK in both modes, for each new family alone, as
  its workflow step runs it (about 8 s per mode for theorem-A and 12 s for
  torus), and for all five families (about 61 s per mode).
- **RED control:** the same tests, with `CHECK_MODE_SOURCE_ROOT` set to this
  branch's base `9f8dbb4d`, whose two wrappers are unchanged. In each mode,
  and the same on 27 and 28 October against `6fbdbba3` and `8dca89cf`:

  | Test | theorem-A | torus |
  |---|---|---|
  | crashes | 4 | 10 |
  | silent exits | 4 | 10 |
  | wrong reasons | 4 | 10 |
  | wrong mutant label | 1 | — |
  | baseline faults (stderr, wrong value, missing key, malformed) | 8 | 8 |
  | JSON faults (stderr, duplicate, NaN, trailing, extra, missing, malformed) | 7 | — |
  | stderr-channel faults (stdout, stderr) | — | 4 |
  | rebound sources (checker; and a loaded file) | 1 | 2 |
  | **false acceptances** | **29** | **44** |

  The wrong exit statuses were already rejected there. For torus, whose
  mutants run at once, those four subtests fail there only on the new
  requirement that the error name the faulty child. The trigger, step and
  import tests fail there too (nine subtests per family), as expected. The
  inventory test passes there, because the old wrappers ran the same schedule.
- **Full suite:** the hosted `full-suite` job at this head is the qualifying
  run; a local run is recorded in the pull request.

## Limits

- The local interpreters were 3.11.17 and an unrecorded 3.11 release, not the
  hosted 3.11.16. The hosted run is the qualifying execution.
- The synthetic fixture uses a one-entry pin list and a minimal manifest. The real
  pins and packet copies run only in the real hosted jobs.
- The torus mutants share one measured reason (above). The theorem-A mutants are
  checked in normal mode only, as the wrapper ran them.
- This is batch 3 of seven. `c8-lifetime-difference-constant` and
  `c8-theorem-a-constants-d3` keep their own stages.
