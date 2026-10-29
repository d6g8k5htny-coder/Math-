# Layer A source scanner scope and implementation plan

The owner fixed the baseline-zero scope and explicitly ruled out further human
questions. This tool supplements actual kernel rechecks; it never certifies a
Lean proof or the meaning of an arbitrary program.

The chosen approach is a bounded, standard-library lexer plus a complete hashed
file inventory and dependency graph. A regex-only scan cannot safely distinguish
nested comments, escaped strings and character literals. A complete Lean parser
or semantic classifier would exceed the authorized offline scanner scope.

Implementation order:

- [x] Write executable behavior tests and observe the initial failing result.
- [x] Implement bounded lexical checks, exact inventory, imports and quarantine.
- [x] Implement the narrow exact rational certificate schema; operational timing
  records receive integrity checks and no mathematical credit.
- [x] Run normal and optimized tests, including weakened-scanner mutations.
- [x] Read the separate engineering threat review, fix findings and rerun.
- [x] Document supported/unsupported cases and integration thresholds precisely.

The manifest and full quarantine schema are explicit inputs, never discovered
through hidden ignore rules. Every file below each declared inventory root must
be listed, including unsupported files. An unsupported file can only be excluded
through the canonical quarantine index with reason, exact boundary, no owner,
zero maintenance and dependency isolation.

## Invocation and machine result

```sh
python -B tools/layer_a_audit.py --root SNAPSHOT \
  --manifest MANIFEST.json --quarantine QUARANTINE.json
```

All three inputs are required. CLI argument/input failures emit a terminal JSON
finding and exit 1. Successful bounded checks exit 0 with `status: PASS` or
`PASS_WITH_QUARANTINE`. Every report has `kernel_verified: false`. `--help` is
ordinary command help. Findings contain `code`, `path`, one-based `line` and
Unicode code-point `column`, `message` and `severity`. Non-source schema findings
point to their manifest/index and use line/column 1; they are not JSON pointers.

`PASS_WITH_QUARANTINE` certifies only the admitted active checks. It does not
promote quarantined content, prove any obligation, or mean that a whole project
has been closed. Quarantined findings remain in the output with the quarantine
ID. Out-of-scope historical locations remain explicit uncertified references.

## Manifest contract

The exact top-level keys are `schema`, `roots`, `external_imports`, `files`, with
schema `cbz-layer-a-manifest-v1`. Roots are disjoint canonical relative
directories. Every regular file below them must appear exactly once, including
files that need quarantine. There are no `.git`, build, suffix or hidden-file
ignore rules. Enumerate an immutable scoped contribution or explicitly classify
the complete desired checkout. This tool cannot prove that a caller's chosen
roots cover the owner's intended federation: that inventory contract is an
external input and the result applies only to the declared roots.

Each file entry has `path`, `sha256`, `kind`. Lean entries additionally have
`module`, exactly equal to the path below their root without `.lean` and with
slashes changed to dots. Module IDs are unique; exact external imports may not
shadow local modules. Every import must resolve to an inventoried local module
or an exact declared external name. Implicit `Init` is included unless the file
declares `prelude`. External entries each have nonempty `identity` and `reason`.
They record a declared trust boundary; the scanner does not independently verify
an external repository, compiler binary or library cache. The actual kernel
campaign must pin and check those dependencies.

Supported kinds:

| Kind | Checks and credit |
| --- | --- |
| `lean_proof` | Hash/inventory plus bounded lexical/import checks; no kernel credit |
| `lean_auditor` | Explicitly hashed trusted metaprogram source, direct escape checks and imports; semantics/execution remain outside this scanner |
| `rational_certificate` | Only the exact JSON schema below, evaluated using integer `Fraction` arithmetic |
| `operational_record` | Well-formed finite JSON plus integrity; timings receive no mathematical credit |
| `operational_source` | UTF-8 bytes plus integrity only; no execution, semantic or Python-import credit |
| `unsupported` | Fails unless the exact file is explicitly quarantined |

A `.lean` file cannot be relabeled as an operational or unsupported file. It
must retain a Lean module identity even when quarantined. Unknown kinds fail.

## Canonical quarantine

The one supplied index uses `cbz-quarantine-v1`, with an `entries` array. Each
record has exactly these eleven keys: `id`, `title`, `layer_a_status`,
`exact_boundary`, `blocking_reason`, `attempted`, `resumption_cost`, `isolation`,
`owner`, `maintenance`, `location`. The first ten values are nonempty strings;
owner is exactly `none`, maintenance exactly `zero`. Location is a nonempty array
of exact `{path,sha256,scope}` objects. Scope is `file`, `directory`, `repo-ref`
or `obligation`.

Active file locations must match the manifest's exact SHA256. Hash, missing-file,
resource and symlink failures can never be waived. An active import reaching a
quarantined file fails, including through a chain of active local imports.
Directory exclusions covering active files are rejected; use exact file records.
External historical directory/repo references are reported without verifying
their stored tree digests. This scanner does not certify their restoration.

An `obligation` location is `source-path#Named.Target` or a named `::premise`
fragment. For inventoried Lean source its SHA256 must match. It is reported in
`unproved_obligations`; the valid definition file is not excluded or blocked from
imports. The fragment is a declared boundary, not a proof that this scanner has
resolved its elaborated declaration or established the proposition. External
register/JSON fragments are reference-only. No second quarantine index is made.

## Exact numerical certificates

Only this narrow schema receives numerical certificate credit:

```json
{"schema":"cbz-rational-certificate-v1","inequalities":[
  {"left":"949/1024","relation":">","right":"11/12"}
]}
```

Relations are `<`, `<=`, `=`, `>=`, `>`. Operands are signed integer or
positive-denominator rational strings. JSON numbers, booleans, scientific
strings, denominator zero, NaN/Infinity, duplicate keys, unknown fields and false
inequalities fail. All decisions use `Fraction`; float formatting never decides
a mathematical certificate. Only the supplied inequalities are checked: this
does not establish that they model an external theorem or computation correctly.

Lean decimal/scientific literals are permitted. In a real-valued theorem they
are exact `OfScientific` rational notation, including the existing 24-digit real
bounds; a decimal token is not evidence of floating arithmetic. Direct `Float`,
`Float32`, `Float64` identifiers/qualified segments are rejected in proof files,
including locally declared aliases mentioning them. This is a bounded lexical
rule, not type inference or a solution to arbitrary alias/program classification.

## Supported lexical and graph checks

The lexer handles nested block comments, line comments, ordinary escaped string
delimiters, zero-or-more-hash raw strings, character literals, Unicode identifiers,
escaped identifiers, field projections and the set image/preimage notations.
Comments/literal contents do not create false forbidden-token findings. Escaped
identifiers containing prohibited names still reject. Unterminated constructs,
delimiter imbalance, obvious dangling terminal constructs and invalid UTF-8 fail.

Direct `sorry`, `admit`, `sorryAx`, new `axiom`, `native_decide`, the built-in
`decide +native` spelling, native reflection axioms, actual `skipKernelTC` option
and explicit unsafe/extern/unchecked-declaration names reject. `#print axioms`
and ordinary local variables named `axioms` are harmless. Proof files reject the
recognized macro/elaboration/notation/opaque/environment-command forms instead
of pretending to expand them. Interpolated strings in proofs are unsupported.
Explicit auditor files permit only simple `s!` identifier interpolations, whose
qualified segments are also checked for prohibited names. Complex string macros
fail. Escaped module names are unsupported imports, never reinterpreted as a
dotted module. Local import cycles fail.

The tool checks exact scope inventory, missing/extra files, byte hashes,
duplicates, module/path agreement, external shadows, symlink roots/ancestors/
leaves, unreadable traversal and special files. It assumes a stable snapshot;
it is not a transactional filesystem or protection against a hostile concurrent
writer replacing directories between system calls.

It cannot certify full Lean syntax or elaboration, exhaustively classify
preexisting imported macro aliases, infer all types, validate an arbitrary
auditor's semantics, prove source-to-theorem alignment, check Python operational
imports, solve arbitrary theorem obligations, establish novelty, or replace the
actual kernel body/type/transitive-axiom audit. These are capability limits, not
an additional approval or model-family gate. Unsupported recognized input paths
fail rather than quietly widening the supported subset.

## Declared limits and verification

Limits are 2 MiB per file/control JSON, 64 MiB total inventoried file bytes,
10,000 files, 1,000 disjoint roots, 20,000 traversed entries including directories,
500,000 tokens per Lean file, 256 nested comments, 2,000 findings, 10,000 rational
inequalities, 512 levels of local dependencies and 1,000 decimal digits per
rational numerator/denominator. Relative
paths are at most 1,024 characters with components at most 255 UTF-8 bytes;
filesystem paths are at most 4,096 characters. Exceeding a bound fails closed.
External libraries are excluded only through the explicit external-import trust
map, never through a claim to have scanned all Mathlib sources.

The initial 20-test suite failed because the executable did not exist. Subsequent
observed RED/GREEN cycles cover real review findings, including raw-string
desynchronization, auditor interpolation, malformed/falsy schemas, module/path
relabeling, actual native aliases/options, permission errors and path bounds.
The separate read-only engineering reviewer reported no remaining important or
critical findings after the fixes. No Lean/native process was launched here.

The current scanner suite has 40 tests. Four source mutations disable escape,
omitted-file, direct Float-alias or exact rational/boolean validation in temporary
scanner copies; the original negative test
methods are executed unchanged against each copy and must fail with test
assertions rather than import/runtime errors. Normal and optimized runners
propagate `-O` to their actual scanner and mutant-control child processes.

At the actual 30-file contribution check, all files/hashes were examined with
zero source findings and six canonical named goal/premise obligations retained:
`PASS_WITH_QUARANTINE`, not universal mathematical closure. Its three explicit
auditor modules are trusted source identities; the 29-module/198-body native
kernel campaign remains separate evidence.

Final verification commands on the delivered scanner/test source:

```sh
python -B -m unittest discover -s tests -p 'test_*.py' -v
python -B -O -m unittest discover -s tests -p 'test_*.py' -v
```

Both returned 0 with 62 tests, OK: the 40 scanner tests plus 22 current federation
tests. The scanner and mutation subprocesses receive the optimization flag in
the second run. These are executable engineering checks, not a claim that a
finite test suite formally proves the Python scanner correct.
