# D2 composite receipt consumers implementation plan

> **For agentic workers:** Use superpowers:executing-plans for this single coordinated source task and one fresh whole-branch engineering/security review.

**Goal:** Make the three existing D2 source/receipt consumers accept the explicitly qualified RF312 source cut and its composite receipt identity while refusing drift and downgrade.

**Architecture:** Keep raw manifest, formal tree and gate pins distinct from the composite receipt digest. Each checker validates the exact outside-tree `manifest_identity` helper bytes before evaluating those verified bytes, then calls that actual helper. A cohesive `validate_core_receipt(core,current)` used by `finish` checks current source, the composite identity and kernel-status label. Existing source snapshots additionally bind the helper.

**Tech Stack:** Python standard library, Git metadata and temporary protocol fixtures only.

**Spec:** [Private proposal pickup](https://github.com/d6g8k5htny-coder/Math-/pull/312#issuecomment-6468894513). Source basis `80946e1cf311b3cbbb051bb3662357b11f8b3d75`; parent four-path source owner retains custody. This private proposal grants no existing312 ref/body/Ready/integration seat.

## Global constraints

- Formal tree `8922fd8c833df0c52d4a8c7b5c3ad802b93098d4`; raw manifest SHA256 `ba7d11e43574e39da3c759e0501399a6dcd1b7da32b157a4a6b01f5c133b3062`; gate SHA256 `509b6eb3b5ee2dc7e42810a40b07192b0feaf3924c9dbb398db43cb44e16e731`.
- Composite receipt identity `481653d73d00f64bf06fefbf24be994f60ebe5c54f826abf899461f6e6937066`.
- Outside-tree validator: `tools/required_formal_check.py`, blob `0b9d694bdf888c75826ca07ae176c5a5c43b8880`, SHA256 `6c27355237b45d3999298522c141984ff5b7c114f18b3c555cc45989976fc6dc`.
- Preserve all formal and companion Lean/contract/import/target/toolchain/dependency/workflow bytes, source scientific dispositions and historical evidence. No original receipt is rebound.
- No finite-law diagnostics, actual mathematics, Lean/kernel, full gate/replay or CI run. Only targeted protocol classes in normal and optimized modes.
- Initial implementation remains private. Existing312 branch publication requires a later actual source-owner handoff and fresh state reconciliation.

## Review focus

- Loading an unbound helper outside the formal tree must refuse before evaluating its bytes; symlinks or drift cannot become trusted code.
- A valid composite receipt passes; the raw digest, wrong commit or wrong kernel-status label refuses.
- Manifest, overlay, core tree and helper mutations refuse without a legacy fallback.
- Atom's two unchanged imported companion Lean pins and the existing runtime re-observation controls remain intact.
- New SOURCE_FILES hashes describe actual new code/tests/documentation while all mathematical payload bytes and earlier evidence remain exact.

## Task1: Update the three consumers

**Files:** Each companion's `check.py`, existing test file, `SOURCE_FILES.json` and README/SCOPE, plus this plan (13 paths). Moment test file is `test_bridge.py`; square and atom use `test_check.py`.

**Interfaces:** Reuse `manifest_identity(manifest: Path, raw: bytes) -> str`. Add each checker's `core_identity() -> str` and `validate_core_receipt(core: dict, current: dict) -> None`; `source` and `finish` must use them.

- [ ] Run the unchanged three `FinalRuntimeTests` classes in normal and optimized modes. Expected21 methods per mode PASS.
- [ ] Add targeted `CoreIdentityProtocolTests`: actual `source()` on a temporary Git copy, actual producer `source_check` plus actual receipt validator, raw-digest/wrong-commit/non-kernel refusal, and helper/manifest/overlay/symlink drift refusal. Run those classes before production edits; expect missing source-cut/receipt support failures.
- [ ] Add the fixed source pins and bound-helper path. Validate helper symlink/hash/blob before evaluating the verified byte string, call actual `manifest_identity`, and require the exact composite digest. Have `source` include the helper's current Git/blob identity and have `finish` call the production receipt validator.
- [ ] Append dated engineering source-cut qualifications without rewriting old mathematical/historical text; regenerate only existing SOURCE_FILES core_tree and changed payload identities.
- [ ] Run the new targeted protocol classes and existing FinalRuntimeTests in both modes; require all PASS. Check whitespace and exact source preservation, including all9 formal Lean blobs and5 companion Lean/contract blobs.
- [ ] Commit one private candidate, obtain fresh distinct whole-branch engineering/security review, and deliver exact parent/head/tree/paths/logs. No publication to the existing312 ref or integration is implied.

Protocol fixtures may use synthetic receipts and Git commits; they are never hosted or kernel evidence. No same-family scientific review or status promotion is claimed.
