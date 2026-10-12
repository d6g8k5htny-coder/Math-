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

Regression-only head455baad7be177888685807ecb23a6724b58f1850, tree
6496117bed52f4fdcad5720d50125ff9306a73ca, intentionally omitted the helper.
[Hosted RED run38193877982/1, job114632222385](https://github.com/d6g8k5htny-coder/Math-/actions/runs/38193877982/job/114632222385)
bound tested merge4d5b2e42f060f77c101e94094380b0ca90fb2012 and executed605
normal-mode methods: exactly42 missing-helper assertion failures, zero unittest
ERROR records. Optimized mode and the source-clean step were not reached.
Only after this observed RED was the helper implemented. This is a
missing-implementation control, not historical cleanup reproduction.

Tests use only synthetic fixtures and the existing ordinary full-regression-suite
PR trigger. No workflow edit, manual dispatch or local project execution occurs.
Each successor requires its own passing hosted receipt and nonauthor verdict.

Hosted normal and optimized results, actual tested commit, source-clean guard,
canary suppression evidence, frozen four-path diff and separate nonauthor review
must be recorded before any engineering acceptance. Green supplied-data tests
cannot establish suppression by a live future recorder: Q5 still requires tested
capture/export behavior at that boundary. Q3/Q4 and experiment approval remain
separate, and the forty-case matrix remains NOT_RUN.

## R1 stream-contract amendment

Nonauthor [review5486003508](https://github.com/d6g8k5htny-coder/Math-/pull/437#pullrequestreview-5486003508)
at742d2c662dbb45a09ffc03335e36b99a5c5d6501 requires an amendment:
one short read is not EOF, and a successful write call need not deliver all bytes.
The tests-only successor adds eight methods for chunked input, hidden trailing
bytes, cumulative cap, nonbytes/nonblocking read results, partial writes,
invalid/no-progress write counts, and exceptions after partial progress.
Tests-only head4653171e7befbad44ed93fad0c90fbfe22e65a94 retained helper
blob9203c32b821c731b369c03158532bd96b69a9351. Actual
[RED run38194828418/1, job114635075401](https://github.com/d6g8k5htny-coder/Math-/actions/runs/38194828418/job/114635075401)
bound tested6678e9a6902b870aaa1eb83994e2fe5387918cf7 and tested tree
a6418252c08e28a0f9163df6e479034580b969f5:613 normal methods, exactly
eight intended stream assertion failures, zero unittest ERROR records.
Optimized mode and source-clean guard were skipped. No canary marker appeared
in the native decoded log. Repair was written only after this observed RED.

The earlier42-control candidate742d2c66 had passed605 methods in each mode at
[run38194422074/1, job114633857603](https://github.com/d6g8k5htny-coder/Math-/actions/runs/38194422074/job/114633857603);
tested34477fd0f5b79c32f8cc33df5ef3bab773e680c2, tested tree
d0c821a4860503b9da0768f422ad72dd717493e0, base49fb197c02ac8d1f16d162771292649c8adad331.
That historical green lacked R1 regressions and cannot override the finding.
The author initially repeated the head tree as its tested tree in a receipt;
[explicit correction6116529944](https://github.com/d6g8k5htny-coder/Math-/pull/437#issuecomment-6116529944)
retains the error and native log/Git correction.

The repaired stream boundary reads through explicit empty-bytes EOF, enforcing
the cumulative input cap before extending its buffer. None and nonbytes read
results are unsupported and immediately yield INPUT_STREAM; stream exceptions
yield fixed INPUT_IO without their message. A short nonempty read is not EOF.
The caller supplies a finite synchronous stream; the helper does not implement
a timeout or nonblocking wait. See the
[Python binary I/O contract](https://docs.python.org/3/library/io.html#io.RawIOBase.read).

Output completes positive partial writes using bounded memoryview slices.
None, zero, Boolean, negative and overlarge counts are refused immediately;
exceptions return exit2 without echoing their message. Read/write loops must
consume/emit at least one byte to continue, bounding iteration count by the byte
caps. A failed sink may retain a prefix; exit2 never claims successful report
delivery, and no second diagnostic is appended to that failed sink. Success
means the supplied sink accepted every report byte, not durable storage or
remote acknowledgment. The repair retains50 methods and requires fresh both-mode
hosted GREEN plus the separate reviewer's successor disposition.
