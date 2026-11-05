# DD mutation-origin repair

Source test SHA256: `17049a25399065a56687edba3ddadae2672e06286541b25600b5b7ea3ab957a7`. Prepared 2026-10-29 on composition6d06680
(tree e54ee23c, identical to native Math541 babb5934).

## Defect and exact resolution

The prior mutation helper accepted any unittest failure with no errors. A planted
AssertionError in the production subject was therefore credited as an oracle kill.
The retained original reproducer logs demonstrate this in normal and optimized
Python. This does not refute historical finite kills or alter the production
exact-output process contracts. It does invalidate generic future-use admission
based on failure counts alone.

The repaired test-local `OracleOriginResult` captures raw traceback code identities
before unittest clears them. A regular failure must be the identical exception
escaping the actual selected synchronous method; subtest failures must occur
while that method is active. The selected body's code must occur exactly once in
the traceback, followed only by the explicitly enumerated unittest assertion
helper code objects. Subject, test-helper and nested-callback assertions refuse,
including same-file code; no filename/text heuristic grants admission. Setup,
teardown, cleanup, manual fixture calls into the body, lazy bodies, returned deferred/non-None values, errors, skips,
expected failures, duplicate/missing execution and terminal events all refuse.
Every original mutant first runs an admitted positive baseline. The frozen
population must have exact start/stop/body/terminal accounting.

## Observed finite verification

Pinned CPython3.11.16 executed22 methods normally and optimized, both OK with zero
skips: all10 original test method ASTs remain byte-identical, including real bounded
specimens and the original16 subject mutants;12 self-test methods are additive.
Five effective grader-source omissions were assertion-killed per mode using the
unchanged outer origin grader. Two isolated skip/expected-failure omissions remain
behaviorally redundant under exact terminal accounting. They are retained with
explicit non-kill assertions, not reported as detected defects. The initial two
failed meta-expectations are retained in redundant-guard-red logs; no failing
production check was deleted or weakened.

Commands: `python3.11 -B -S -m unittest tests.test_lifetime_dd_node_oracle -v`
and the same with `-O`. The existing dedicated workflow already discovers this
file; no workflow change is required. Production replay.py, all certificates,
fixtures, numerical algorithms and workflow bytes are unchanged.

## Limits and ownership

This is a bounded trusted-process engineering harness, not mathematical
certification or hostile Python-code attestation. Arbitrary same-process monkey
patching of unittest/result internals is outside its boundary. Full repository
regression, new hosted checks and final federation gates remain unexecuted here.
Historical hosted runs remain bound to their prior source. Maintenance: none
except deliberate source/runtime changes. Register the test-local verifier under
the existing DD tool entry during canonical integration; this does not create a
new general-purpose auditor.

The earlier full-normal/full-optimized logs retain the preceding21-method cut.
Final22-method evidence is in final-normal/final-optimized; both exits are0.
