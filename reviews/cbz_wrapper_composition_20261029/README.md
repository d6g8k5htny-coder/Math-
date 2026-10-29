# Current-base replay-wrapper composition

Prepared 2026-10-29 19:41:09 UTC from Math- main e877242cf68fb24c605066f16dd07f513ee75a1d.

This candidate composes the three engineering-only deltas in PR370 and PR379, the four-path PR492 exact-verdict repair, and PR385's LM006 execution driver. Original source heads are additional commit parents, so the original failed test file and every historical test remain recoverable.

PR385's malformed test file is replaced by the complete authenticated recovery blob 1ee8a1d2c4d2b5846d28c229ace7513d95fd3c47 (10554 bytes, SHA256 774385be9aea0bfb3dac46884e7abcc6748a424fce5601206164778ee096e2f2), changing only its exact Python-version assertion to 3.11.16. All17 test methods are retained. The workflow uses the already deployed current checkout/setup-python pins and Python3.11.16. The PR370/379 workflows retain their complete protocol repairs with the current setup-python pin. No scientific checker arithmetic, mathematical bound, result fixture, Lean source, dependency or packet pin is changed except PR492's already documented exact mutant-report protocol.

## Verification state

NOT_VERIFIED for this composed source until its actual native jobs finish. Earlier green receipts remain bound to their historical source heads and are not transferred. No repository-wide or CBZ-0 claim is made here. This branch is an execution-custody repair candidate, not mathematical acceptance.

## Exact local commands

Use CPython3.11.16 with its bin directory first in PATH (synthetic children invoke python).

```sh
python -B -S -m unittest discover -s tests -p test_soft_fold_workflow.py -v
python -B -O -S -m unittest discover -s tests -p test_soft_fold_workflow.py -v
python -B -S -m unittest discover -s reviews/third_order_protocol_20261006 -p test_third_order_rate_workflow.py -v
python -B -O -S -m unittest discover -s reviews/third_order_protocol_20261006 -p test_third_order_rate_workflow.py -v
python -B -S -m unittest discover -s tests -p test_elder_cusp_parity_workflow.py -v
python -B -O -S -m unittest discover -s tests -p test_elder_cusp_parity_workflow.py -v
python -B -S -m unittest discover -s tests -p test_lm006_oned_coefficient_replay.py -v
python -B -O -S -m unittest discover -s tests -p test_lm006_oned_coefficient_replay.py -v
python -B -S tools/lm006_oned_coefficient_replay.py --mode normal --output /tmp/lm006-normal-unique
python -B -S tools/lm006_oned_coefficient_replay.py --mode optimized --output /tmp/lm006-optimized-unique
```

The three dedicated exact-control workflows also run authentic baseline/mutant child invocations with their complete source and dependency checks. The fixture suites intentionally use synthetic reports to prove each wrapper rejects crashes, unrelated nonzero exits, wrong verdicts, corrupt outputs, stale sources and postflight drift. They do not certify mathematical bounds.

## Operational decision

The managed shell execution service stopped returning observations while preparing the local composition. A separate native GitHub tree/commit is used to obtain genuine hosted execution without assuming a local merge or test completed. No remote merge, ref rewrite, source deletion, protection change, or old result relabelling is performed. Central federation tool registration remains in main's GOVERNANCE.md and TOOLING.md; this README supplies source-local use and verification boundaries for the composed candidate.

## Custody repair after the first scoped successes

The five targeted jobs passed at head59d0094ee388946de24b934ed3bca96ac73c4191 / tested merge3f127c6f492b0b498e3097bdd20525cee68918e5. Those exact historical observations are recorded in PR533 comment6506952638. Review then found that LM006's Git helper honored replacement refs and ambient Git redirection, and an imported driver could label its later committed file as the code that ran.

Three real-Git/API controls produced an actual optimized RED at head82c9004c2a6472a3913292e92543d21fbab174ef, run40946125351/job123701825783:20 methods, exactly3 intended assertion failures, zero errors. The normal original-driver RED remained queued when this repair was prepared and is not claimed. The observed failure artifact is12928953745, GitHub ZIP SHA2561dc4b8b1fe8ec1c763b208827ddd3171221db2d54d078721c1ebdf06b110d251.

The driver now sanitizes its Git environment, disables replacement objects, and checks loaded driver bytes inside both execution-source snapshots. The focused suite has21 methods, preserving all original17. For each new guard, it also runs a clean target baseline and an actual source mutant. Every child must run exactly its intended test in the requested interpreter mode and fail for that guard's reason. Full mutant streams are retained as base64 in LM006_CUSTODY_SOURCE_MUTATION log records. The declared threshold is3/3 source mutants in EACH Python mode; the paired focused commands above execute it. Fresh guard-fix results had not yet completed when this text was prepared; consult their exact native head and checkout identities.

See [tool registry](GOVERNANCE.md) and [decision ledger](DECISIONS.md). Historical SCOPE records retain their original observations; their superseded author/family/approval requirements do not govern CBZ admission.

## LM006 executed-code identity

The supported test harness imports the exact single-read driver source with `compile` and `exec`, and binds its later source check to the very same bytes. The driver also compares its running module code object with the code compiled from its current source and refuses ordinary stale bytecode. The workflow's direct Python script execution compiles source. Arbitrary attacker-controlled bytecode can remove any self-check inside itself; callers requiring source identity must use the source-only loader or direct script execution. This is execution/custody evidence, not mathematical or formal verification, and changes no numerical bounds.

The normal-mode intended RED was observed at source ae3c35b41590ae8494c37602cdf87fc09c6ffb26, run40950416828/job123716743203: one actual timestamp-valid, same-size poisoned bytecode executed although the recorded loaded-source bytes were legitimate. See the retained [failure excerpt](../../cbz/evidence/lm006-bytecode-20261029/normal-red.log). A repaired-source hosted run of all preserved tests and source mutations in both modes remains required; do not infer a pass from this commit.
