# Bounded Lean packet source admission

Component registration input: `tools/lean_packet_admission.registry.json`.
This records source tooling for parent review, without awarding a canonical
registration, CLOSED disposition, compiled qualification or mathematical status.

`tools/lean_packet_admission.py` is the standard-library source census consumed
by the determinant and Cap adapters. Each adapter fixes the helper path, refuses
symlink ancestors, checks its manifest SHA-256 and executes those verified bytes.
It inventories ordered module/namespace/name/kind/privacy records and compares
exactly with reviewed census metadata. The current public ABI remains determinant
66 targets and Cap 152. The determinant source census includes 19 legitimate
private declarations; none are renamed or made public.

Supported source includes the reviewed theorem/lemma/definition/abbreviation,
named instance and structure forms, balanced scopes, nested comments and literal
strings. Unsupported declarations, command wrappers, metaprogramming, forbidden
logical-placeholder/axiom/native tokens and incomplete lexical input reject.
Opaque indented code is admitted only with the reviewed ordered continuation
fingerprint and preceding column-zero anchors. Rebinding ordinary file digests
never updates this boundary. A changed continuation binding needs separate review.
This is a bounded source identity check, not a complete Lean parser or compiled
constant audit. Structure-generated and private/auxiliary compiled constants need
separate qualified compiled evidence.

Run from repository root:

```sh
python -B -S -m unittest discover -s tests -p test_lean_packet_admission.py -v
python -B -O -S -m unittest discover -s tests -p test_lean_packet_admission.py -v
python -B -S -m unittest discover -s tests -p test_source_admission_mutations.py -v
python -B -O -S -m unittest discover -s tests -p test_source_admission_mutations.py -v
python -B -S tests/run_source_admission_mutations.py --output /tmp/fresh-source-admission-mutations
```

The runner derives the repository from its own location and requires a fresh
output directory outside it. It carries forward all fourteen exercised round-1
mutations plus the declaration-header binding removal (fifteen total), both Python modes, the same packet/helper/shared-test/Cap-pin copy
paths, and three unmodified full-suite controls per mode. Each selected mutation
first runs an unmodified same-copy baseline. Every baseline requires positive
unittest discovery and a clean OK; kills require positive matching discovery,
nonzero exit and actual assertion failures in a recorded test body. The same
subprocess records unittest body entry and each failure phase. Setup, teardown,
cleanup and class/module fixture failures reject; missing/duplicate/malformed
phase evidence and unsupported custom lifecycle hooks reject. Timeouts never
produce a classified result. Import/setup errors, skips, zero-test
or duplicate/missing matrix entries, nonunique anchors and surviving mutants fail
the command. The output records raw baseline/mutant logs, argv, exit status and
log hashes. Helper SHA rebinding isolates only the intended helper removal from
its independent integrity guard. Source-gate removals retain the original fixture
hash rebinding behavior. No Python `assert` is used for the runner's decisions.
The determinant workflow runs the ten focused runner self-tests, with both file
paths as triggers. The full fifteen-mutation/two-mode command is standalone;
workflow source-test success does not mean it executed. This is a scoped
experiment, not federation G0, full G6 or a Lean execution.

The determinant workflow calls `source_check()` explicitly for source-only
identity. Its separate observation step after pinned Lean setup checks source
and helper identity, rebuilds, replays leanchecker, and runs the unchanged bound
compiled helper's `inventory_source()` while retaining raw output. Observation
status for this composition is **NOT_RUN / UNQUALIFIED**. Observation output
never populates a manifest automatically or creates an acceptance receipt.
The authoritative subsequent `gate.py --execute` remains fail-closed with
`CBZ_COMPILED_INVENTORY_UNQUALIFIED` until a separately qualified exact census is
bound. The copied compiled adapter cannot currently admit the legitimate private
non-target theorem inventory. This is a tooling qualification gap; its rules and
proof visibility remain unchanged. A workflow failing at the authoritative gate
is not a failed mathematical proof or a successful kernel qualification.

Every opaque declaration/header physical line now has a separate per-module
`source_admission.declarations` count/SHA binding, including complete one-line
declarations without an indented continuation. Lexical code selects declaration
headers, but the fingerprint retains the entire selected physical line, including
literal/comment text. The current bindings were made only from the unchanged
reviewed proof sources. Missing/malformed/stale bindings reject. Ordinary file
hash rebinding cannot authorize an appended arbitrary command or header tail.
Continuation bindings and the source census remain unchanged. These are narrow
reviewed syntax-admission bindings, not a full Lean parser or evidence that any
injected tail elaborates. The review's one local Lean launcher probe failed
before processing input; no successful grammar/kernel execution is inferred.
