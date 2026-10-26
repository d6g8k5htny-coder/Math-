# SIDE24 d = 5, 6 mutant wrappers: authenticate the intended rejections

Dylan Roy — delegated AI engineering. Actual author: Anthropic Claude, session
`session_017Mi3hxjaxV45x6zo6o1ee3` (Claude017), stage
`SIDE24-WRAPPERS-REPAIR-017-20261026`, pickup Math-#322/6427944196. Dylan approved
this stage in the author's session at about 21:30Z on 26 October 2026. This session
wrote the three packets. Scientific effect NONE; shared-account organizational
credit 0. Author-side implementation only: a separate nonauthor engineering review
and a separate integrator are required. No mathematical acceptance is asserted.

The method is the one C8 used for its own wrappers in #518/#519
(`reviews/c8_check_mode_wrappers_20261026/SCOPE.md`). The helper, references and
test are new, separate files, and C8's `tools/check_mode_*` and
`tests/test_check_mode_workflows.py` are untouched.

## Finding and exact source

01Cz's ledger (Math-#322/6388271177) classifies all three wrappers as
`status_only`. Each mutant was accepted on exit status 1 alone, with its stdout and
stderr discarded. So an unrelated crash, a silent exit 1, or a report that fails
for another reason counted as an intended rejection. The baseline was already
compared byte for byte with `RESULTS.json`, but its stderr was discarded.

| Object | Identity |
|---|---|
| Math- `main` at characterization and branch base | `7d63d08f6cfadfd9c2ef28039a370d741126f9a0` (the merge of #519) |
| `side24-d5-closed-form.yml` before | blob `7c39892950068e1e7f9c9e0f4c1897cfbdfb3a30` |
| `side24-d5-coefficient.yml` before | blob `9f46fffa48b4162356bbe269e54f68602deef1c6` |
| `side24-d6-coefficient.yml` before | blob `6059c2ecde9e7edf4fda1efeece3ce964483e322` |
| `closed_form_d4.py` (unchanged) | blob `e087f4c0007ae2473d28230771588da57f794aab`, 45,019 B |
| `cone_moment_d5.py` (unchanged) | blob `9d918805865031c8ef9ae5d4d0c3266e1a396a98`, 46,082 B |
| `cone_moment_d6.py` (unchanged) | blob `c5e56694d96c885373a7b70868259eeb9fdfa746`, 68,731 B |
| d=5 closed-form `RESULTS.json` (unchanged) | 16,765 B, SHA-256 `b878c1d3534a1ce72f01bb461a06b8777888bc0a5fdd9413fc1a4f8a565a2bb3` |
| d=5 coefficient `RESULTS.json` (unchanged) | 5,435 B, SHA-256 `81c4bc072b7eab4d2f1725b3d873076dac6bc31ab1a06779d3299d9e81b3cbaf` |
| d=6 coefficient `RESULTS.json` (unchanged) | 8,319 B, SHA-256 `82d1c19f9f503fd9211c6dcf356ec62aee9ec9eda44792bc38be4f3690637832` |

The three packet trees are `d2e9f088`, `dc7dfac0` and `dcbeffef`. The ledger read
the workflows at `d1f6ad28` as blobs `40fe9334`, `93ac2e5e` and `c45d9a5a`. The
only change since is 2c041de (24 October), which moved each file's
`actions/setup-python` pin from `5fda3b95` to `6d4fd22b`. The mutant logic the
ledger classified is unchanged. The imported `tools/legacy_json_replay.py` (blob
`854db466`) and `tests/test_legacy_workflow_triggers.py` (blob `c2e37a3a`) are
the blobs every local run below used.

## Repair and preservation

Eight files: `tools/side24_mutant_replay.py`, the three files in
`tools/side24_mutant_contracts/` and `tests/test_side24_mutant_workflows.py` (all
new), the three workflows, and this note.

`tools/side24_mutant_replay.py` follows `tools/legacy_json_replay.py` and reuses
that module's strict JSON reader and structural comparison instead of copying
them. For each family it binds the checker's git blob and the `RESULTS.json` size
and digest. It then runs the fixed inventory in both modes, exactly as the old
wrappers did: from the repository root, with the absolute script path, and with
`<script>` and `<script> --mutant M`. For every child it requires the following:

- **Baseline:** exit 0, stdout byte-equal to `RESULTS.json`, and stderr exactly
  one timing line `seconds N.N`.
- **Report mutant:** exit 1, stderr exactly one timing line, and one strict JSON
  report on stdout that is structurally equal to the report measured from the
  unchanged checker.
- **Guard mutant:** exit 1, empty stdout, and a stderr that starts with
  `Traceback (most recent call last):`, ends with the measured final exception
  line, and carries no timing line.

The references are in one file per family, because the d=5 closed-form reports
alone take 139 KB compactly and the strict reader caps a document at 256 KB.

Each workflow now calls `replay()` in place of its own exit-only loop. It gains
one earlier step that runs `tests/test_side24_mutant_workflows.py` for its own
family in both modes. It also gains the trigger paths for the helper and its
inputs (`tools/**`, `tools.py`), for that test, and for
`tests/test_legacy_workflow_triggers.py`, whose strict path reader the test
reuses.

Unchanged:
- the source block before any child: the packet manifest, the main-resident pins
  and, for d=5 and d=6, the quoted d=2, 3 enclosures;
- the `RESULTS.json` certification checks (16, 13 and 20 checks, and the d=5
  closed forms), which now run once on the committed bytes. Each mode's baseline
  stdout must still equal those bytes;
- the action pins, read-only permissions, `persist-credentials: false`, Python
  3.11.16 and the job budgets (15, 60 and 120 minutes);
- the per-child timeouts (600, 1500 and 3000 s), the four workers, the mutant
  order within each mode and the terminal record;
- the final `git diff --exit-code`;
- every packet file.

One ordering detail changes. The old wrappers ran each mode's baseline and then
that mode's mutants. The helper runs each mode's baseline together with its
mutants in one pool, and it checks every child of that mode before starting the
next mode.

## Disclosed deviations from #519

1. **Timing line on stderr.** These checkers print `seconds N.N` on stderr in
   every run that reaches a report, so the contract requires exactly that one
   line. It does not require empty stderr. The pickup said "empty stderr", and
   this is the measured behaviour instead. No other byte is allowed.
2. **Guard references.** In the d=5 closed-form family and the d=6 family, the
   `vandermonde` mutant never reaches a report. The checker's own structural
   guard raises
   `ValueError: an even p3-power occurred; J_k would carry an error function`
   (d=5 closed form) and the same exception text in the d=6 checker. The reference for these is that guard
   only: exit 1, empty stdout, a traceback ending in that exact line. The d=5
   coefficient `vandermonde` reaches a report and is a report reference.
   This means the old wrappers' `vandermonde` rejection in those two families was
   never a failing check. It was an exception, and the repaired wrappers pin
   which one.

## The contract

| Family | Report references | Guard references |
|---|---|---|
| `side24-d5-closed-form` | 13 | 1 (`vandermonde`) |
| `side24-d5-coefficient` | 11 | 0 |
| `side24-d6-coefficient` | 13 | 1 (`vandermonde`) |

Every report reference has `passed: false`, its own label, and at least one false
check. Each mutant fails a different set of checks, and the references pin the
whole report, so a failure for another reason, a crash, a silent exit, extra
stderr, or a report for another label is rejected.

## Execution and non-vacuous regressions

All of the following ran locally on CPython 3.11.15, with `main` `7d63d08f`
characterized and the branch cut from it.

- **Characterization:** the unchanged checkers, in both modes, exactly as the
  wrappers ran them. Every normal and optimized stdout is byte-identical. Every
  baseline stdout equals `RESULTS.json`. The exit statuses are as above. Locally
  a d=5 closed-form child takes about 1–3 s, a d=5 coefficient child about 80 s
  and a d=6 child about 175 s.
- **Real checkers through the helper:** `replay()` on the three actual packets
  gave `protocol_ok` for every child: 30 for d=5 closed form in 41 s,
  24 for d=5 coefficient in 16.9 minutes with two workers, and 30 for d=6 in
  25.3 minutes with the workflow's four workers. All under the per-child timeouts.
- **This test file:** 14 tests OK in both modes for each family as the workflow
  step runs it (about 56 s, 40 s and 42 s per mode), and 14 tests OK in both modes for all three
  families together under the full suite's discovery (about 110 s per mode).
- **RED control:** the same tests, with `SIDE24_MUTANT_SOURCE_ROOT` set to
  unchanged `main`, run each old wrapper shell against the same fixture. They
  give these false acceptances:

  | Test | d=5 closed form | d=5 coefficient | d=6 |
  |---|---|---|---|
  | crashes (every mutant, both modes) | 28 | 22 | 28 |
  | other guard faults (another exception, stdout, timing line, silent) | 8 | 0 | 8 |
  | silent exits, wrong values, wrong label | 10 | 10 | 10 |
  | report JSON and stderr faults | 16 | 16 | 16 |
  | baseline stderr | 2 | 2 | 2 |
  | **total** | **64** | **50** | **64** |

  The wrong exit statuses, baseline byte drift and baseline crashes were already
  rejected there and still are. The trigger, step and import tests fail there
  too, as expected.
- **Real-checker RED control:** a copy of `closed_form_d4.py` that raises an
  unrelated `RuntimeError` on `--mutant jacobian` gives exit 1 in both modes. The
  old acceptance rule accepts it. The helper's `_check` with the real reference
  rejects it.
- **Repository suites:** the 44 test modules that read workflow files pass on the
  branch except `test_proof_slice_check`, which fails with the same 20 failures
  and errors on unchanged `main` in this container. They differ only in synthetic
  commit IDs, so the failure is local and independent of this change.

## Limits

- The local interpreter is 3.11.15, not the hosted 3.11.16. The hosted runs are
  the qualifying execution.
- The synthetic fixture uses a one-entry pin list and a minimal manifest. The real
  pins run only in the real hosted job.
- The other `status_only` SIDE24 wrappers in the ledger
  (`side24-periodization-firstvar`, `side24-periodization-remainder`,
  `side24-v1-coefficient-review`) are not this session's packets and are not in
  this stage.
