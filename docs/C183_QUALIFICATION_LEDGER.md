# C183 Q1/Q6 offline ledger preparation

This isolated four-file proposal prepares an offline supplied-byte outcome and
identity ledger for [PR397](https://github.com/d6g8k5htny-coder/Math-/pull/397).
It implements only the first qualification group in the
[handoff](https://github.com/d6g8k5htny-coder/Math-/pull/397#issuecomment-6089120259).
It does not implement a collector, launch a child, run experiments, change a
runtime or change PR397's HOLD / NOT_READY / NO_MERGE disposition.

## Test-first checkpoint

The first draft commit `d29dc03a73dbab847e6a5792ed49842b0572ba8c`
deliberately contained no helper implementation. Hosted run38168778516/attempt1,
job114556777353, tested merge`cdecbd22a0a034248079a4f9e4f73ad966729558`,
executed529 normal-mode tests:30 intended missing-API assertion failures and
zero errors. Optimized mode was not reached after the normal-mode failure.
This is an implementation RED, not historical cleanup reproduction. The
subsequent implementation has a different exact source identity and needs its
own hosted results. No local project tests were run.

Nonauthor review5484709386 at implementation`b9a139ad9e3fd5bbebd65f6432c8e3d61cde2987`
requires three bounded amendments: terminal partial-summary accounting, finite
numeric parsing and validation of original ZIP names before normalization.
The next test-only commit preserves that implementation and adds regression
controls. Its actual hosted result must precede the repair; these static
counterexamples are not yet claimed as executed failures. Original review and
RED evidence remain unchanged.

Regression-only head`8ac18f435a18ed1fa5fc4be80a0847b64275cf22` binds the
first35 controls to hosted run38170248987. A second test-only successor adds
one explicit partial-summary capacity control: every observed status must fit
its claimed population, and total claimed FAIL+ERROR must not exceed the
reported count. Neither test-only successor changes the reviewed helper bytes.

## Offline use

Run only in a project-authorized execution environment:

```sh
python -B -S tools/c183_qualification_ledger.py
python -B -S tools/c183_qualification_ledger.py --archive ORIGINAL.zip --sources HISTORICAL_PACKAGE
```

The first command prints a deterministic ledger with all input gates NOT_RUN.
The second reads the explicitly supplied archive and historical package. It
never downloads evidence, imports those sources or writes output files. JSON
goes to stdout. Invalid supplied inputs produce valid=false JSON and exit2;
missing optional inputs are NOT_RUN, not a failure or a pass.

The archive reader checks its canonical whole-byte identity and all bounded
members' names, kinds, sizes and CRCs, returning only five fixed member names.
The public low-level read_zip_members API also accepts a caller-supplied expected
identity for synthetic custody tests; only build_ledger imposes the historical
archive pin. It is not producer authentication. CLI file checks reject symlinks
and nonregular/oversized inputs, but are not a hostile concurrent-filesystem
sandbox. The caller supplies stable read-only inputs.

The source gate verifies12 pinned files plus the manifest, derives71 method
identities and24 unique anchors by inert AST inspection, and records the numeric
guard mutation separately. It never compiles or imports any project module.
The original wrapper substring predicate and the stricter outcome parser are
separate functions; evaluating the former does not certify completed coverage.

The whole original archive is not embedded in these tests. Hosted fixtures test
its reader with synthetic ZIPs, and independently validate the authentic five
members and thirteen source bodies. Do not report the helper's canonical
original-archive branch as executed unless a separate receipt establishes it.

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
