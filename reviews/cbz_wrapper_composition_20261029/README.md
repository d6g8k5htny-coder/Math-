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
