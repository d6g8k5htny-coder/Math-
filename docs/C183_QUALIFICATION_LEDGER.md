# C183 Q1/Q6 offline ledger preparation

This isolated four-file proposal prepares an offline supplied-byte outcome and
identity ledger for [PR397](https://github.com/d6g8k5htny-coder/Math-/pull/397).
It implements only the first qualification group in the
[handoff](https://github.com/d6g8k5htny-coder/Math-/pull/397#issuecomment-6089120259).
It does not implement a collector, launch a child, run experiments, change a
runtime or change PR397's HOLD / NOT_READY / NO_MERGE disposition.

## Test-first checkpoint

The first draft commit deliberately contains no helper implementation. Its
hosted tests must fail with `required offline API absent`, rather than import or
setup errors. This is an implementation RED, not a new reproduction of the
historical cleanup failure. A later implementation and hosted GREEN will have
different exact commit/run identities. No local project tests were run.

## Evidence boundaries

Historical source commit: `81c31f5d61c509256f8d13a4635ca0c85fb8d989`.
Historical PR head: `8177f47bbb66b7cc0dca430941832740a5480dee`.
Historical base: `2ca3bf262f34a729589ad87eefe6cf6af5adcb6c`.
Run `37742226653`, attempt 1, job `113195346919`.
Original wrapper blob: `fcf6480529d6b521628e2635e7c1e271ecfa39a4`.
Current main's wrapper is not that historical source.

The fixture's `source_files` contains thirteen complete historical public source
bodies read from that immutable commit. `members` contains five exact public
artifact members, not reconstructed transcripts. Its `synthetic` section is
separate three-method parser input and is never historical execution evidence.
The original archive was acquired through one fresh native descriptor and
inertly checked: 507793 bytes, SHA-256
`ce224c87fffea10a41b0d3403eee59b81b4b05f06e809ce6623863dd311da65c`,
169 unique bounded regular members. The archive itself is not committed here.

The helper must preserve historical normal baseline71OK, numeric mutant
68OK/2FAIL/1ERROR, and the forty proposed NOT_RUN cases as separate populations.
Expected/discovered method counts cannot replace observed method outcomes.
Historical `REPORT.json` remains passed=false and modes=[], with the original
two-space `Oct  1` Python literal. Numeric child return codes absent from the
retained original records remain unknown. Cause remains UNKNOWN.

## Early-stop contract

This is a data-only decision after a child has exited or reached a cap. Stop
scheduling subsequent specimens after an unexpected ERROR/timeout. It never
interrupts a running process. Timed-out/interrupted outcomes remain incomplete.
The deliberately injected ERROR control may meet its own expectation only while
the original wrapper still refuses the specimen. That is not mutant acceptance.

The original30-second suite and proposed15-minute/256-MiB overall caps and
10-second Q wait remain future driver obligations; this helper enforces none of
them at runtime. It neither signals descendants nor preserves a residual fixture.

## Validation and remaining work

New tests use the existing full-regression-suite hosted workflow, triggered by
tools/** and tests/**. No workflow change or manual dispatch is needed. Required
checks still apply to their actual tested commit. These tests do not execute any
of the28 matrix specimens or12 controls, including the30 planned full suites.

Historical archive identity, selected member identity and source identity are
separate gates. Missing inputs report NOT_RUN; validating embedded member bytes
does not establish whole-archive verification or historical runtime equality.
Matched environment/disclosure, qualified observation/residual custody,
collector implementation, reviewed experiment admission and repair remain open.
Missing original writer/config/binary/mount provenance is never manufactured.
Source-exposed AI engineering gives organizational-independence credit0 and
scientific effect NONE. Separate nonauthor review and integration are required.
