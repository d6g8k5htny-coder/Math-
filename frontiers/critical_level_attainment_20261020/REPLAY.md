# Replaying C294 conditional death-level attainment

This command/interface guide accompanies the actual local final verification: seven isolated builds, two standard named-module kernel replays, the complete235-declaration axiom census and the omitted-LPC rejection passed. FINAL_SEQUENCE_RESULT.json and negative-final/RECEIPT.json provide the actual execution records. Frozen inventory SHA256 a819e8a4cf37b3b3527dd32045fc08c5dd5967022c2d70c1ee009add352a1f2d binds the inputs. Mathematical review and later publication/custody results are separate records.

The explicit actual closed-superlevel LPC admission remains open. No supplied path, finite event list, full elder/barcode theorem, stochastic Morse admission, scientific acceptance or hosted C294 registration is inferred.

## Pinned inputs and runtime

Five immutable sources in SOURCE_INPUTS.json: Lifetime, TorusTopology, SuperlevelBar, ClosedSuperlevel, MorseFiniteCritical. Two new modules: CriticalLevelAttainment, CriticalLevelAxiomAudit. SOURCE_INPUTS records safe relative project_path/input_path, size, SHA-256 and Git blob for each input; actual freeze/receipts bind all seven sources.

- Lean **4.34.1**, retained Darwin aarch64 runtime.
- Mathlib **d13f23b723b8a846827a245b89c10fc7d3f11612**.
- Pinned project lake-manifest.json SHA-256 **d63753befccc21923783a5085148e3ff028d97134ea52f5a08bd87ecf1b0b043**; toolchain SHA-256 **d5edba4e4b8faad9c1baeadb265716d20d03be4d1a2647dc5e35b0c0325bea7b**.
- lean executable SHA-256 **1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554**.
- leanchecker executable SHA-256 **cfde41cb11dde58c84e9c60c551fd104bb2fc1104ad44dca932a923120272a35**.
- C291 dependency inventory baseline SHA-256 **b78b6e0f99bd38c633ae2677c55698363b1290e6d4318e505991c8df259ae2e3**.

The runtime/cache locations are explicit in run_final_phase.py. Its runtime() checks the exact executable and manifest bytes and every manifest package's pinned HEAD; only actual existing compiled package roots enter the import path. It deliberately permits pinned packages such as Cli that have no compiled Lean root, matching C291's baseline. This is not a fresh package rebuild or provenance authentication of the entire cached import closure.

LEAN_PATH begins with this package's isolated **final-build**, followed by existing pinned dependency build/lib/lean paths. The retained Lean installation supplies its runtime core. Environment strips inherited LEAN/LAKE/LD_/DYLD_ variables, pins PATH to the explicit runtime bin plus system paths, sets LEAN_NUM_THREADS=2 and uses a per-phase temporary directory. No shared-cache object is an output destination.

## Final preparation and serial phase commands

The following are the command shapes root executed from the native C294 directory after source freeze under the fresh claim. Replay only in a separate fresh destination; the delivered directories and once-only receipts must be preserved. Do not run the driver and then repeat individual phases.

```sh
python3 -B prepare_final_inputs.py --freeze
python3 -B run_final_sequence.py
python3 -B run_negative.py
```

Preparation requires absent final-project/final-build/final inventory, writes a unique append-only record under final-prepare-attempts/, checks all seven exact sources, derives the local import DAG, copies source bytes into fresh final-project and creates empty isolated final-build. FINAL_SOURCE_INVENTORY binds the preparer, phase runner, unique start record, source hashes/order/imports, dependency inventory and C291 baseline. evidence/FINAL_BUILD_INITIALIZATION records empty outputs and dependency reuse. A legacy FINAL_PREPARE_START is not required or overwritten.

The expected frozen order and the driver's concrete phase CLI are:

```sh
python3 -B run_final_phase.py build Lifetime
python3 -B run_final_phase.py build TorusTopology
python3 -B run_final_phase.py build SuperlevelBar
python3 -B run_final_phase.py build ClosedSuperlevel
python3 -B run_final_phase.py build MorseFiniteCritical
python3 -B run_final_phase.py build CriticalLevelAttainment
python3 -B run_final_phase.py build CriticalLevelAxiomAudit
python3 -B run_final_phase.py kernel CriticalLevelAttainment
python3 -B run_final_phase.py kernel CriticalLevelAxiomAudit
```

The serial driver reads inventory.build_order, appends only the two NEW kernel phases and stops at the first unresolved failure. All compiler runners share lean-slot.lock with development run_lean.py; do not bypass it with parallel manual commands.

Underlying build command shapes, with placeholders denoting the runner's pinned/isolated absolute locations:

```text
<PINNED_BIN>/lean -j2 -M4096 -o <FINAL_BUILD>/Lifetime.olean <FINAL_PROJECT>/Lifetime.lean
<PINNED_BIN>/lean -j2 -M4096 -o <FINAL_BUILD>/TorusTopology.olean <FINAL_PROJECT>/TorusTopology.lean
<PINNED_BIN>/lean -j2 -M4096 -o <FINAL_BUILD>/SuperlevelBar.olean <FINAL_PROJECT>/SuperlevelBar.lean
<PINNED_BIN>/lean -j2 -M4096 -o <FINAL_BUILD>/ClosedSuperlevel.olean <FINAL_PROJECT>/ClosedSuperlevel.lean
<PINNED_BIN>/lean -j2 -M4096 -o <FINAL_BUILD>/MorseFiniteCritical.olean <FINAL_PROJECT>/MorseFiniteCritical.lean
<PINNED_BIN>/lean -j2 -M4096 -DwarningAsError=true -o <FINAL_BUILD>/CriticalLevelAttainment.olean <FINAL_PROJECT>/CriticalLevelAttainment.lean
<PINNED_BIN>/lean -j2 -M4096 -DwarningAsError=true -o <FINAL_BUILD>/CriticalLevelAxiomAudit.olean <FINAL_PROJECT>/CriticalLevelAxiomAudit.lean
<PINNED_BIN>/leanchecker -v CriticalLevelAttainment
<PINNED_BIN>/leanchecker -v CriticalLevelAxiomAudit
```

These are **standard named-module kernel replays against imported dependencies**, not --fresh, independent/external verification, a fresh all-import closure replay or hosted execution. Each fresh phase directory retains START/PREFLIGHT/PROCESS_START/RECEIPT and complete stdout/stderr. Receipt binds executable, runner, frozen source inventory, actual command, source/object/dependency before-and-after identities, exit/timeout and process-reaping observations.

Configured caps are **600s per ordinary build/kernel phase**, **900s for the audit build**, **600s for N1**. These are bounded settings, not observed passes. Root set the600s cap before freeze after an immutable-input development load reached240s; the900s audit allowance follows retained earlier audit experience. Thread/memory settings remain2/-M4096. Actual elapsed time, return codes and failures must come from receipts.

## Complete measured audit

CriticalLevelAxiomAudit enumerates module-origin declarations with exporting disabled, including generated/private helpers, for exactly these six source/proof modules:
Lifetime, TorusTopology, SuperlevelBar, ClosedSuperlevel, MorseFiniteCritical, CriticalLevelAttainment.

Markers:
```text
ATTAINMENT_AUDIT_MODULE <module> COUNT <measured module total>
ATTAINMENT_AUDIT_DECL <actual name> AXIOMS [<actual possibly wrapped list>]
ATTAINMENT_AUDIT_STANDARD_ONLY_PASS COUNT <measured total>
```

ATTAINMENT_AUDIT_PROGRESS on stderr is progress only. Actual module record totals must equal their emitted declaration counts; names must be globally unique; total must equal all parsed records. Every transitive axiom list must be a subset of propext, Classical.choice, Quot.sound. Both public targets must occur in the explicit required-name array and census:
TorusCriticalAttainment.quotient_death_attainment and TorusCriticalAttainment.euclidean_death_attainment.

**Measured result:235 unique declarations, all standard-only.** Module counts are103/38/25/32/20/17 in the listed order. Actual stdout SHA256062a8168ad5b05f1238ea8fd516d7fc5a806941cf77480b6de6837921c294386. Root bound final_master.py to this measured count and actual frozen inventory; no C293 count or verdict was transferred.

## N1: omit the actual closed-LPC premise

Actual fixture: negative-project/WithoutClosedLPC.lean. Its purpose is to invoke the actual final attainment theorem while omitting its explicit closed-level LPC input, not to supply the path as an assumption.

```text
<PINNED_BIN>/lean -j2 -M4096 <C294_ROOT>/negative-project/WithoutClosedLPC.lean
```

run_negative.py uses the same slot/runtime/imported objects and captures full stdout/stderr. A successful negative-control **result** requires a nonzero compiler exit without timeout, actual type mismatch containing **LocallyPathConnectedSpace**, no unknown-module/identifier/syntax/object-file failure, and unchanged frozen sources/imported sources/objects. Mere command failure is not success. The receipt also binds the fixture, negative runner, Lean executable and inventory. Root binds ROOT_ACCEPTANCE.closed_lpc_diagnostic_token to the actual observed symbol. **N1 observed result:** expected type-mismatch rejection, rc1,74.2482s, no timeout, actual LocallyPathConnectedSpace input displayed; source and imported objects unchanged. Diagnostic stdout SHA256103fca1879ac4965b80766263cab5f18f64dbe46ddbb9de70aef49976fbdafd8.

## Metadata reuse, failures and final artifact steps

Dependencies use the hash-verified C291 baseline and exact pathset. At identical size/mtime_ns/inode, prior byte digests are explicitly reused. Changed metadata triggers byte hashing and requires the same digest; a changed pathset/hash fails closed. Receipts report reused counts and rehashed deltas. This does not claim a full fresh dependency rehash, source rebuild or absence of all possible undetectable metadata-preserving mutation. No shared-cache bytes are copied or written.

Retain all development failures/streams/receipts, source-attempt snapshots and interrupted preparation records. Do not clear final outputs or restart the once-only driver after failure. Any actual correction needs a documented successor receipt and only the affected/unfinished work; old results are not rewritten.

After exact-source mathematical review and acceptance, root may finalize documentation and run, in their appropriate later stages:
```sh
python3 -B prepare_publication.py
python3 -B build_packet.py
python3 -B final_master.py
```
These are **not three immediate commands**: publication raw/Git-object readback and applicable hosted-job evidence must precede private packet construction; private upload/native raw download equality must precede the once-only artifact master. See evidence/MASTER_CONTRACT.md and PACKAGING_ADAPTATION.md for exact interfaces.

Private output is C294_CRITICAL_LEVEL_ATTAINMENT_DELIVERY.zip using canonical C288 builder SHA-25688d6e30182ae682d27f4d156f6c935f8373168ca6ff14d3141cd69c4b036d3a3. Public prefix is frontiers/critical_level_attainment_20261020/. Public text projection records native/projected hashes separately and forbids changes to Lean bytes. Private packet preserves complete development/native evidence, objects and compressed native dependency inventory.

Exact mathematical review is recorded separately in reviews/NONAUTHOR_REVIEW.md. Publication, hosted, private custody and final master are later stages, reported by the terminal delivery rather than claimed by this command guide. Existing registered hosted checks do not execute C294's new modules; new_formal_execution stays LOCAL_ONLY_NOT_REGISTERED_IN_HOSTED_FORMAL unless a separately owned registration and actual execution establish otherwise. Artifact binding is not mathematical/scientific acceptance.

[Owner mandate](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md) and [standing delegation](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md) accompany this handoff.

