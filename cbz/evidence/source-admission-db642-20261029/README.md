# Bounded packet source admission — DB642

Coordination: [main#684](https://github.com/d6g8k5htny-coder/main/issues/684).
This contribution repairs source-admission omissions in the existing determinant
and Cap packets. It is evidence for the existing CBZ integration queue, not a
separate procedure, canonical status index, or CBZ-0 declaration.

The initial proof source is Math
`8151f592918a845bf19eb8eafaf8444540a32734`. The compiled safeguard already
published in Math#528, commit `74565f013575b7b05ecfc4034cd5d638ee355353`, is
preserved. Reviewed final local source is
`5591b44e1f19846b2b6aa44664a902e2c7963340`, tree
`a911fe6f1b33d4cca22df25d303f7b7516816cd9`. Publication also retains the five
disjoint C8 wrapper paths already merged in default
`e877242cf68fb24c605066f16dd07f513ee75a1d`, then adds evidence and plans.
The native delivery commit has its own identity. Hash equality, not an
assumption that local and native commit IDs coincide, establishes source equality.

## Correction and observed evidence

The two gate adapters now require the fixed, digest-bound helper and an exact
ordered source census. They separately bind opaque continuations and entire
declaration/header lines, preserving literal and comment text in those header
bindings. Updating ordinary file hashes does not silently authorize an omitted
declaration or unknown command. Existing proofs, public target lists and all
legitimate private declarations retain their bytes and visibility.

The portable mutation runner requires a clean selected baseline with positive
test discovery. It records unittest lifecycle phases so a setup, teardown or
cleanup assertion cannot masquerade as a test-body kill. All fourteen earlier
mutations remain; the fifteenth removes the new header binding and the sixteenth
regresses physical-line alignment. Raw and stripped source use LF consistently,
with equal row counts and strict pairing. Unicode separators inside comments or
strings cannot shift a declaration onto another physical source line.

| Final local observation | Result |
|---|---|
| Shared helper, normal / optimized | 20 / 20 tests pass |
| Determinant packet controls, normal / optimized | 117 / 117 tests pass |
| Cap packet controls, normal / optimized | 45 / 45 tests pass |
| Mutation runner controls | 10 per mode at 60f9912; affected matrix self-test 1 per mode at 5591b44; lifecycle functions unchanged |
| Actual source mutations | 16 per mode; 32/32 killed |
| Unmodified full-suite controls | 6/6 pass |
| Positive selected/control baselines | 38/38 pass |
| Protected proof/control/toolchain/pin files | 95/95 byte-identical |
| Published compiled/receipt functions and helper | Preserved |

The latest source and complete-matrix evidence is `composition-fix2/` inside the archive, including
exact commands, interpreter modes, log hashes, original RED observations and
final source bindings. The unchanged lifecycle implementation uses its explicitly
retained `composition-fix/` evidence; no invented combined test run is claimed. Earlier reports and intermediate
failures retain their original meaning and are not substituted for final results.
The source-level whole-branch review and subsequent scoped fix reviews are
included separately. The archive contains historical experiment scripts for
provenance; they are inert records, not approved certifiers or required commands.
The inheritable active tools are the repository files documented below.

## Commands and registration input

Use [the existing tool documentation](../../../tools/LEAN_PACKET_ADMISSION.md)
for exact source-test and mutation commands, supported grammar, helper binding
and lifecycle boundaries. The adjacent
[registry input](../../../tools/lean_packet_admission.registry.json) binds the
active implementation, tests, runner and documentation by SHA-256. The canonical
writer can register those tools in the existing GOVERNANCE/TOOLING/STATUS files;
this directory does not award that registration itself. Maintenance is
self-contained; any source or supported syntax change requires fresh scoped
verification and reviewed bindings.

Run from the repository root, with a new output directory outside the checkout:

```sh
python -B -S -m unittest discover -s tests -p test_lean_packet_admission.py -v
python -B -O -S -m unittest discover -s tests -p test_lean_packet_admission.py -v
python -B -S -m unittest discover -s tests -p test_source_admission_mutations.py -v
python -B -O -S -m unittest discover -s tests -p test_source_admission_mutations.py -v
python -B -S tests/run_source_admission_mutations.py --output /tmp/fresh-source-admission-mutations
```

The workflow runs the focused runner self-tests. The complete 16-by-2 mutation
experiment is a standalone command; it is not implied by workflow success.

## Compiled boundary

No local Lean/kernel pass is claimed. Cap's existing workflow and the narrow
determinant workflow provide the hosted execution routes. At this source cut the
determinant compiled inventory is still null and its authoritative CLI refuses
with `CBZ_COMPILED_INVENTORY_UNQUALIFIED`. The new observation step retains raw
build, leanchecker and inventory output without rebinding a census or issuing an
acceptance receipt; the following authoritative step preserves failure.

The canonical integration owner is separately qualifying the actual determinant
private names, proof-valued instance and generated compiled entries. This source
repair neither replaces that work nor weakens its inherited gate. A missing
tooling qualification is not mathematical impossibility. These local checks do
not establish all compiled constants, semantic alignment, non-vacuity, all Layer
A, federation G0–G11, or CLOSED/quarantine dispositions.

## Retention and recovery

`evidence.zip` preserves the original reports, reviews, failures, commands and
raw observations. `ARCHIVE_MANIFEST.json` lists every archived path, size and
SHA-256; `SHA256SUMS` binds the delivered evidence files. The archive has no
absolute or parent-traversal member paths. Extract it into a fresh directory
outside the source checkout when inspecting historical evidence.

`source-history.bundle` preserves the local implementation and base-composition commits before
the coherent native delivery. Its prerequisite is the public Math#528 baseline
above; `git bundle verify source-history.bundle` can be run in a clone containing
that baseline. This is recovery data, not an active branch, a new workflow, or a
claim that an earlier failing implementation is admitted.

No existing claim is transferred, no board is rolled over, and no historical
failure or proof obligation is erased by this contribution.
