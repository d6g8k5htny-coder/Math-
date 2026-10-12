# C183 Q2/Q5 supplied-data preparation

This additive helper prepares input-contract and disclosure-model tests requested
by [handoff6089120259](https://github.com/d6g8k5htny-coder/Math-/pull/397#issuecomment-6089120259).
It is a pure validator/projector for explicitly supplied JSON bytes. It never
collects an environment, reads a referenced path, launches a process, consumes
live traces, changes source, or implements the forty proposed experiments.

**PR397 HOLD / NOT_READY / NO_MERGE remains.** Historical cause is UNKNOWN;
historical environment equivalence and actual U/I environment matching are
NOT_ESTABLISHED. Collector qualification, live recorder payload suppression and
experiment execution are NOT_RUN. Scientific effect NONE; promotion permission
is always false. Existing Q1/Q6 helper, fixtures and documentation are unchanged.

## Bounded interface and acceptance

The API is `project(raw_bytes)` returning a report, `render(raw_bytes)`
returning canonical JSON bytes plus LF, and `main(binary_input, binary_output)`
for explicitly supplied streams. The CLI uses stdin/stdout only, without file
arguments. Exit0 means VALID_SUPPLIED_INPUT, exit1 means INCOMPLETE_INPUT,
exit2 means INVALID_INPUT. These are structural supplied-data outcomes only.

All input keys are fixed. Rejected values and unrecognized key names never
appear in diagnostics. Invalid input has no projection; diagnostics contain
only fixed error codes and categories. The projection preserves only the schema
below. No raw argv, pathname, URL, write buffer, arbitrary environment/config
entry, version/image free text or unknown event/field is admitted. Digests are
opaque supplied identities, not authenticated producers or a universal secret
detector: callers must not intentionally encode secrets into admitted fields.

Parser bounds are 1 MiB input, nesting depth8 (root container counts as1),
256 UTF-8 bytes per scalar string/key, and2048 synthetic event records.
Output is capped at1 MiB; overflow is refused rather than truncated.
Depth is checked before JSON decoding. Duplicate keys, floats/nonfinite values,
wrong exact types (including bool-as-int), invalid Unicode and unknown keys
fail closed. These parser bounds do not modify experimental runtime budgets.

Input has `schema_version:1`, `records:{U:..., I:...}` and `events:[...]`.
Absent root/record/group/mandatory fields and explicit UNKNOWN values produce
INCOMPLETE_INPUT; wrong supplied values produce INVALID_INPUT. Missing event
fields are invalid instead of silently omitted. Explicit empty events produce
EMPTY_SUPPLIED_MODEL and no writer inference.

Each record contains:
- `origin`: SYNTHETIC or SUPPLIED; neither authenticates acquisition
- `observed_at_unix_s`: tagged integer0..253402300799
- `command_shape`: C183_UNITTEST_DISCOVER_V1
- `mode`: normal or optimized
- `variant`: baseline or accept_numeric_required
- `observer`: NONE for U; OUTSIDE_SOURCE for I
- `sources`: pristine, numeric_mutant, observer tagged SHA-256 identities
- `environment`: locale (C/C.UTF-8/OTHER), timezone (UTC/OTHER), selection_sha256
- `configuration`: gc_auto (-1..1000000), maintenance_auto/gc_auto_detach/
  maintenance_auto_detach (exact booleans), hooks_policy/template_policy
  (DEFAULT/DISABLED/CUSTOM), effective_sha256
- `binaries`: git_sha256, python_sha256, stdlib_sha256
- `mount`: filesystem (ext4/xfs/overlay/tmpfs/apfs/OTHER), identity_sha256,
  read_only (exact boolean)

A tagged field is exactly `{"state":"UNKNOWN"}` or
`{"state":"REPORTED","value":...}`. SHA-256 is64 lowercase hex characters.
Baseline numeric_mutant and U observer must be explicit UNKNOWN; they are
inapplicable rather than mandatory provenance. Numeric variants and I require
their corresponding reported identities. This does not attest mutation anchors,
pristine-source equality, or instrumentation behavior; Q1/Q6 and future
qualification keep their own acceptance tests.

C183_UNITTEST_DISCOVER_V1 denotes the authenticated original wrapper's list
`[sys.executable, "-B", *mode_flags, "-S", "-m", "unittest", "discover",
"-p", "test_*.py", "-v"]`, where mode_flags is[] or["-O"]. It is data,
not a runnable command. Source:
[original wrapper lines142–155](https://github.com/d6g8k5htny-coder/Math-/blob/81c31f5d61c509256f8d13a4635ca0c85fb8d989/frontiers/downstream_gate_20260925/run_validation.py#L142-L155),
blob fcf6480529d6b521628e2635e7c1e271ecfa39a4. Actual executable paths, cwd,
and environment identities are not recovered by this descriptor.

The limited U/I comparison ignores the declared observer treatment and observer
identity, and reports fixed field categories for other supplied differences.
Origin and observation time are acquisition metadata and are not matched
environment fields. UNKNOWN/missing mandatory values make the comparison
incomplete. Matching means only equality of supplied selected fields. OTHER,
DEFAULT and CUSTOM are broad labels; their matching never establishes the
underlying settings or a full actual environment. Supplied digests do not prove
that bytes came from any particular machine. Actual admitted experiment records
and independent byte/capture evidence remain needed to discharge Q2.

Event-model records have exactly kind, operation, sequence, result, subject and
errno. Kinds/operations are PROCESS (START/EXIT), FILESYSTEM
(CREATE/WRITE/UNLINK/RMDIR), CONFIG (SELECT). Subject is FIXTURE/DESCENDANT/
OUTSIDE. Result is OK/ERROR/UNKNOWN; errno is0..4095 and is0 unless result is
ERROR. Sequence is0..1000000000 and strictly increasing. These are synthetic
typed samples, not a parser for Trace2/syscall streams or evidence of actual
ancestry, namespace coverage, clocks, dropped events or NO_WRITER.

## Historical facts remain separate

Fixed reference: repository d6g8k5htny-coder/Math-, PR397 head
8177f47bbb66b7cc0dca430941832740a5480dee; tested merge
81c31f5d61c509256f8d13a4635ca0c85fb8d989; run37742226653,
job113195346919, artifact11534366248. Missing effective configuration,
effective environment, binary/library identities, mount identity,
writer/start identity and residual entries stay unknown in every output.
Supplying a new complete record cannot backfill historical provenance.

[Original real ERROR and failed aggregate](https://github.com/d6g8k5htny-coder/Math-/pull/397#issuecomment-6054734380)
and [documentary review's execution stop](https://github.com/d6g8k5htny-coder/Math-/pull/397#issuecomment-6088814073)
remain controlling. No earlier denied author-closeout report is reproduced.
No historical denied artifact transfer is retried. No cleanup retry, lock
removal, descendant signal, runtime downgrade or weakened ERROR refusal follows
from these tests. Original30-second child cap, shared15-minute/256-MiB cap,
and10-second Q wait remain future qualified-driver obligations.

## Test-first evidence and handoff

The initial regression-only draft intentionally omits the helper and checks
42 methods against the required public API. It needs actual hosted RED evidence
before implementation; it is not a passing candidate or a cleanup reproduction.
Tests use only synthetic fixtures and the existing ordinary full-regression-suite
PR trigger. No workflow edit, manual dispatch or local project execution occurs.

Hosted normal and optimized results, actual tested commit, source-clean guard,
canary suppression evidence, frozen four-path diff and separate nonauthor review
must be recorded before any engineering acceptance. Green supplied-data tests
cannot establish suppression by a live future recorder: Q5 still requires tested
capture/export behavior at that boundary. Q3/Q4 and experiment approval remain
separate, and the forty-case matrix remains NOT_RUN.
