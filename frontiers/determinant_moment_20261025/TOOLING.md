# Determinant compiled admission tooling

Source baseline: d6g8k5htny-coder/Math-@8151f592918a845bf19eb8eafaf8444540a32734, frontiers/determinant_moment_20261025/.

compiled_inventory.py is a byte-identical copy of that commit's formal/gate_helper.py. Only inventory_source, bound_inventory, audit_inventory and compiled_admission are consumed by gate.py. The helper enumerates Lean module-table constants, retains private/generated names losslessly, computes transitive type/value axiom closure across every package constant, and rejects missing/extra/unbound declarations. The bound manifest does not allow user-written theorems to be hidden as non-target constants.

Retained stages: source and original-byte identities; exact source module root/target pre-check; dependency lock; exact Lean4.34.1 release5045d0056413266e57c625dcd7c365b10e377c52; clean pinned dependencies before/after; fresh package build; leanchecker; target axiom reports; elaborated types; five existing proof/axiom rejection controls; source/runtime recheck; exact receipt/run identity fields. Added stages: actual compiled package inventory, all-constant closure, and two compiled admission controls (hidden sorry proof and range-less compiler-shaped theorem).

Run component tests:
```sh
python -B -S -m unittest discover -s tests -v
python -B -O -S -m unittest discover -s tests -v
python -B -S tests/run_cbz_mutations.py
```
Protocol fixtures and mocked subprocess responses in tests are explicitly synthetic unit inputs. Their receipts remain temporary test products and are never current-package kernel evidence. Real pinned Lean status for this repair: NOT_RUN.

The portable component-local mutation command above uses sys.executable, selected positive baselines and disposable source copies outside the component. It reuses the five existing cases, requires each mutation location exactly once, and accepts only the exact intended failing test names with positive collected counts and no import/test errors. The original source inventory must remain unchanged. Optional --output must name a directory outside the component; for example, `python -B -S tests/run_cbz_mutations.py --output /tmp/determinant-cbz-mutations`. No task-local checkout/evidence/mutations directory is assumed. STATUS.md carries these same component-only verification commands.

Receipt invalidation occurs before all CLI argument/source/manifest/qualification checks, including source-only quarantine. The helper is loaded lazily after bound-file validation. Safe active receipt paths are cleared; directory symlinks refuse without being followed. Historical final receipts remain immutable. QUARANTINE.json binds exact Lean/module hashes instead of a manifest self-hash, with the complete mathematical evidence boundary and zero maintenance.

Current `python -B -S gate.py` and `python -B -S gate.py --execute` both return1 with CBZ_COMPILED_INVENTORY_UNQUALIFIED, without a kernel receipt. The source_check Python API remains a diagnostic identity check, never a completeness or execution claim.

Activation requires a real pinned Lean environment: preserve all source/dependency identities, execute the helper's Inventory.lean census against this package, inspect the exact non-target constant records and bind them in manifest.json.compiled_inventory, then execute gate.py --execute so the new runtime census must reproduce the binding and all existing/new controls succeed. Never seed the binding from the column-zero source regex or current core package's different inventory. Unsupported names/module-system objects, private non-target records not representable by this helper, or any mismatched census remain rejected until explicitly implemented and tested; do not suppress findings.

The local evidence directory outside this component records baseline78 tests, the actual regression RED run, normal/optimized successor tests, mutation runs, unchanged proof hashes, CLI quarantine, and source bytes. These are engineering results and preserve the real Lean NOT_RUN boundary.

Initial local verification, 2026-10-29: predecessor78/78 tests passed in each Python mode; the first successor98/98 tests passed in each mode. All78 original test bodies remain unchanged. Five deliberate admission/runtime/receipt mutations were killed by test assertions, with no import or test errors. All14 original Lean paths remain byte-identical. The core helper copy is byte-identical (SHA256 ff8a5374597772b2d37054fd722c2243c4b552a63802c69f7c605519832be6c4). Both CLI forms returned1 with the exact quarantine reason, and no candidate kernel receipt exists. Real Lean execution: NOT_RUN.

Focused follow-up verification:109/109 tests passed in normal and optimized modes, including actual CLI source/manifest/helper failure and quarantine cleanup, symlink/historical-evidence safety, the complete quarantine record and a cold-start portable-runner copy. The ten initial CLI/quarantine regression methods were observed RED with13 assertion failures before the fix; the missing portable runner was also observed RED before implementation. The component-local five-case mutation runner then passed with green selected baselines, positive test counts and exact intended assertion failures; sources remained unchanged. No forbidden axiom finding, repaired-gate Lean run, independent auditor work or CBZ CLOSED evidence is inferred from these engineering results.

