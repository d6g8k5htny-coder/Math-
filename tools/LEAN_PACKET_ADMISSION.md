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
output directory outside it. It carries forward all sixteen existing mutations
and adds two runner mutations: removal of the exact exit-status restriction and
removal of the exact integer return-code type restriction (eighteen total).
Both Python modes retain the same packet/helper/shared-test/Cap-pin copy paths
and three unmodified full-suite controls per mode. The runner and its self-test
are also copied into each case; self-tests import the mutated copied runner,
while the original launcher records their unittest phases. The complete matrix
has 42 result records, 42 same-copy baselines and 84 raw logs. Each selected
mutation first runs an unmodified same-copy baseline. Every baseline requires
positive unittest discovery, a clean OK and exact integer exit status 0; kills
require positive matching discovery, exact integer exit status 1 and actual
assertion failures in a recorded test body. The same
subprocess records unittest body entry and each failure phase. Setup, teardown,
cleanup and class/module fixture failures reject; missing/duplicate/malformed
phase evidence and unsupported custom lifecycle hooks reject. Timeouts never
produce a classified result. An unrelated exit handler changing a body-failure
child's status to 2 rejects even when its recorded phases are valid. Separate
synthetic result controls refuse booleans, strings, floats, integer subclasses,
missing statuses and integer statuses outside 0/1. Import/setup errors, skips, zero-test
or duplicate/missing matrix entries, nonunique anchors and surviving mutants fail
the command. The output records raw baseline/mutant logs, argv, exit status and
log hashes. Helper SHA rebinding isolates only the intended helper removal from
its independent integrity guard. Source-gate removals retain the original fixture
hash rebinding behavior. No Python `assert` is used for the runner's decisions.
The determinant workflow runs the thirteen focused runner self-tests, with both file
paths as triggers. The full eighteen-mutation/two-mode command is standalone;
workflow source-test success does not mean it executed. This is a scoped
experiment, not federation G0, full G6 or a Lean execution.
Earlier sixteen-case matrices and receipts remain historical evidence at their
own source identities; they are not relabeled as eighteen-case runs.

The determinant workflow calls `source_check()` explicitly for source-only
identity. After pinned Lean setup, its complete `--execute` gate checks source
and helper identity, rebuilds, replays leanchecker and audits the full bound
compiled census. A separate determinant policy binds91 exact typed non-public
records without changing the shared source helper or the inherited compiled
core. Native run40945103791 at bc5c47fe/tested7e95ff64 actually reached all seven
intended controls; its source263-record endpoints,21 owned logs and separately
retained full console were verified. This exact historical result is not
execution of later grader/documentation bytes. Read the component STATUS and
QUARANTINE records for current-source qualification, provenance and limits.
Source census output never populates a compiled manifest or awards acceptance
automatically. The registry's UNQUALIFIED compiled-census value describes this
source checker's own output, not the separate packet's actual compiled audit.
No source-only observation is a mathematical proof or scientific alignment.

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

Physical-line correction: LF (`\n`) is the line separator throughout the lexical
code census, continuation and declaration-header traversal. Raw and lexed rows
are paired with an explicit equal-count check and strict zip; Unicode separators
inside comments or literals cannot shift or silently truncate that pairing.
Benign comment/string fixtures check exact selected header bytes and harmless
definition-value changes. Existing reviewed packet source and all admission
bindings remain unchanged. The sixteenth mutant reintroduces the old divergent
`splitlines()` pairing and is exercised only against these benign fixtures.
