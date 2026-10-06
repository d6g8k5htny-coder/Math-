# D5/C6 named-rejection workflow repair

Dylan Roy - delegated AI engineering work. Actual author: OpenAI / GPT-6 Astra
Pro, `lm006-continuation-wrapper-repair-20261005`. Scientific effect **NONE**;
shared-account/provider organizational-independence credit **0**. This addresses
Math-#314, under pickup 6007256016 and contract clarification 6007291547. It does
not modify the scientific checkers, their proof packets, manifests or outputs.
Current execution and review dispositions belong to the PR's source-bound record.

## Why an adapter is necessary

The original three workflows accepted any mutant process exiting 1, including
an unrelated RuntimeError; they also ignored baseline stderr. D5 and C6 Palm
intentionally raise uncaught AssertionError through their own `require` function.
Factorial instead emits JSON with an exact failed-check set. Requiring empty
stderr and JSON directly from every unchanged original CLI would reject genuine
D5/Palm controls. The repair translates only their authentic assertion carrier.

`tools/d5_c6_replay.py` runs the full original script in a fresh child process.
For D5/Palm it accepts only an exact AssertionError class, argument message,
checker filename and final `(check_group, require)` traceback pair. It then emits
an identified JSON rejection with empty stderr. Output preceding the exception
is not suppressed and therefore fails the parent. All other exceptions propagate
as failures. The parent requires exit 1, empty stderr and an exact typed JSON
record. Normal completion is not rejection.

Factorial retains its original JSON output. The parent requires exactly its
baseline object/scope/check schema, exactly one mapped false check, all remaining
checks true, and `passed` false. Duplicate keys, nonfinite numbers, floats,
coerced Boolean/integer values, missing/extra fields and trailing data fail.
Every baseline must exit 0, reproduce the frozen RESULTS.json bytes and have
empty stderr. The complete ordered mutant inventory is mandatory in both modes.

The original workflow membership/size/hash checks and final tracked Git-diff
check are retained. This is not a general sandbox or an authenticity guarantee
against a malicious replacement of an entire reviewed repository. A process
protocol does not prove the mathematical claim tested by a finite checker.

## Authentic source cut and measured contracts

Repository `d6g8k5htny-coder/Math-`, source cut
`2f8b6f372be383d752e9dd30d38234faa977243c`.

| Family | Unchanged checker path | Git blob |
|---|---|---|
| D5 | `frontiers/d5_dimension_lift_20260929/lift_exact_check.py` | `460efe46126bb1b7b45954a7a8e0ef2f8e93c739` |
| Palm | `frontiers/c6_palm_route_20260929/palm_exact_check.py` | `6b0c73baeeb2ac566160e23cc405daec07eb7585` |
| Factorial | `frontiers/c6_factorial_moment_20260929/c6_check.py` | `0adaf6382e89af8ce2537c994013d0c5e05b011d` |

All three original baselines and every mutant were actually executed normally
and under optimization: 48 native processes total. The 10 D5 and 7 Palm messages
and originating groups agree across modes and are recorded in the helper and
independently in the test fixtures. The 4 factorial failures are respectively
ELIMINATION, PACKING, RADIAL and REMAINDER. The unmodified baseline identities are:

| Family | Bytes | RESULTS.json SHA-256 |
|---|---:|---|
| D5 | 5184 | `ae9ca864ff9db1f239910fa7c349c297aa1b5ffbd9863786ca20a61a6c1814e5` |
| Palm | 2775 | `7812de453ff1efd77ffc2431874243713615ce4fcc0e55f2beae991e24f6f6bc` |
| Factorial | 285 | `82ef312659552ef7fd783e188961df62088764ef79f575e3b29720585f32109f` |

The predecessor workflow blobs, used for red-phase controls, are respectively
`06a9c445bc8ae7b4af78bdb1ddee41f533e3a7db`,
`9dba863a2c1c155d8fa267da2de9cc91d8bce186`, and
`6d3a141555d4ed98f9ab9c1e6ff36e00683282da`.

## Regression and hosted execution boundary

```sh
python -B -S -m unittest discover -s tests -p test_d5_c6_workflows.py -v
python -B -O -S -m unittest discover -s tests -p test_d5_c6_workflows.py -v
```

The suite has 14 methods. Its workflow tests use 232 real committed temporary
Git repositories per outer mode, with hash-consistent synthetic checker/output
fixtures. They execute the entire original or repaired verification shell step,
including its membership/hash checks and final Git-diff command. No subprocess
is mocked. Every one of the 21 named mutant stages is targeted separately in
both child modes. Additional helper tests verify baseline/mutant timeout stages,
unknown-label exits, inventory completeness and strict JSON types.

The fixture scripts are not scientific evidence. They deliberately use small
synthetic baselines where no numerical reproduction claim is being made. A
predecessor replay can use the current test file with `WORKFLOW_SOURCE_ROOT`
pointing to a checkout containing the original three workflow blobs; the helper
unit tests still use the current helper while those workflow fixtures execute
the original shell code. Expected failures demonstrate the old admission defect.

All three workflows now run full repository `tests/` discovery in both outer
Python modes, with explicit fail-fast shell settings. Full-history checkout is
needed by the existing historical proof-reachability tests. Trigger paths cover
the helper and `tests/**`; existing action SHAs, Python 3.11.16, original process
timeouts, job timeouts, permissions and mathematical packet paths are unchanged.

Local source copies were authenticated before execution. Complete local GitHub
checkout was unavailable, so local full-repository discovery and original full
packet-membership verification are not claimed. Dedicated hosted jobs must run
the full repository tests and actual complete scientific packets at the tested
candidate. A general green formal/downstream check alone does not establish that
these three dedicated workflows executed. A later source/base requires its own
applicable checks; old receipts must not be rebound.

## Nonclaims

No D5/C6 theorem, Gaussian regression step, continuum argument, Palm law, global
closure, formal alignment, Lean source, scientific register or prize is changed.
Nonauthor technical review and eligible nonauthor/nonreader integration remain
separate from this author-side repair and its tests. The exact historical proof
and checker bytes remain available without edits or retrospective acceptance.
