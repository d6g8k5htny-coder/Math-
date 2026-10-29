# Math CBZ tool registry

| Tool | Entrypoint | Scope | Current runtime status |
|---|---|---|---|
| CBZ-MATH-NATIVE-KERNEL-01 | tools/cbz_kernel_gate.py; tools/cbz_kernel_registry.json | Eight native Lean packages, currently 119 source modules; fresh native builds, module kernel replay, independent complete declaration censuses, axiom closure and actual compiled controls | NOT_EVALUATED for this integration |
| Q-CUSP-BINARY64-20261029 | tools/check_cusp_quarantine.py; quarantine/Q-CUSP-BINARY64-20261029.json | One preserved 16-file binary64 packet and its explicitly denied numerical consumers | Integrity/nonconsumption checks only; A3_NOT_PROVEN |

The native workflow is .github/workflows/cbz-kernel.yml. It supports pull_request, main pushes, workflow_call and workflow_dispatch without a historical head guard. It installs Lean 4.34.1 once, uses Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612 and the exact nine dependency records, and retains evidence under .lake/cbz-kernel/. Its actual positive/empty-module and unused-axiom/sorry/native controls execute before long native builds. Fixture source bytes and immediate control results are retained; later failures cannot turn them into a full-package success.

Run focused source/control tests from the repository root:

```sh
python3 -B -S -m unittest discover -s tests -p test_cbz_kernel_gate.py -v
python3 -B -O -S -m unittest discover -s tests -p test_cbz_kernel_gate.py -v
python3 -B -S -m unittest discover -s tests -p test_cusp_quarantine.py -v
python3 -B -O -S -m unittest discover -s tests -p test_cusp_quarantine.py -v
```

The auditor has a narrow self-mutation gate. Run `python3 -B -S -m unittest discover -s tests -p test_cbz_kernel_mutations.py -v` (and the same with `-O`) and `python3 -B -S tools/cbz_kernel_mutations.py --output .lake/cbz-kernel/mutations-NEW`. The runner requires all66 baseline method bodies to pass in both modes, then kills all nine declared nonstale guard mutants by their designated actual body AssertionError, with completed supported lifecycle and zero errors/skips/startup failures. Its17 harness controls reject fixture failures and stale observations. The real Lean preflight separately compiles and runs theorem-value-omission and foreign-raw-version-omission collectors; both must emit complete false-clear protocols and be caught by their exact compiled sorry control. A compiler failure cannot count as a kill. These are bounded auditor self-tests, not full semantic or all-generated-code qualification.

The raw-record collector builds and independently checks the full imported module/ConstantInfo index. Native raw declarations are direct roots; each referenced Name reaches every imported version. The only permitted native aliases have identical theorem constructor, name, level parameters, type and proof expressions under Expr.equal, and TheoremVal.all, with a raw owner witness and selected checked declaration. Raw/unique closure counts and aliases are explicit protocol-v2 fields. Missing records, unsupported module sidecars and different proof payloads refuse. Dependency cache objects remain trusted inputs rather than freshly rebuilt dependencies.

Dependency attestation covers every tracked Git entry. Its only symlink exceptions are three independently inspected aliases at the exact registered package, revision, path, Git blob and raw link payload: Batteries documentation README and two inactive Mathlib Python benchmark aliases. It hashes and enumerates the link payload without following its target, and records that limited role. These aliases are not gate compiler inputs; unknown links/revisions and all native Lean/configuration/gate source links or symlinked ancestors remain refused.

Run the native inventory, then actual execution only with the exact pinned runtime and dependency checkouts available:

```sh
python3 -B -S tools/cbz_kernel_gate.py --inventory
python3 -B -S tools/cbz_kernel_gate.py --execute --expected-commit "$(git rev-parse HEAD)" --timeout 1800
```

Inventory success is SOURCE_INVENTORY_ONLY with kernel_status NOT_EVALUATED. Execution writes a success receipt only after every native package, kernel replay, compiled census, axiom audit, control and final identity recheck passes. A failed or absent phase stays REFUSED/NOT_EVALUATED. The 43 Lean paths outside these eight native packages remain outside this gate's scope.

Run quarantine integrity and the deliberately denied admission attempt:

```sh
python3 -B -S tools/check_cusp_quarantine.py
python3 -B -S tools/check_cusp_quarantine.py --consume frontiers/cusp_coefficient_certified_20261001/certificate.py
```

The first command must exit 0 with QUARANTINE_INTEGRITY_OK and cbz_certificate_admitted false. The second must exit 1 with REFUSED. An unrelated --consume source must exit 2 with NOT_COVERED and remains uncertified. The existing cusp workflow preserves its numerical replay and mutants as diagnostics; its green result cannot discharge A3.

Explicit-source callers must treat both exit 1 and exit 2 as non-admission. The validator is opt-in and does not automatically enforce quarantine in other downstream workflows or authenticate every descriptive consumer/reference field. Global consumer isolation and A3 closure are outside its scope.

Component-local determinant commands and the compiled-inventory quarantine are preserved in frontiers/determinant_moment_20261025/TOOLING.md. Neither this registry nor the all-native gate changes that component's bound inventory or scientific status.


Each `--execute` call creates a fresh `.lake/cbz-kernel/executions/attempt-<unique-id>/`. Read `.lake/cbz-kernel/current-execution.json` to locate the current attempt; its success receipt lives inside that directory. A failed attempt records REFUSED without a new success receipt. Previous complete/incomplete attempts and their source/control logs remain unchanged. Top-level reference history is retained separately. The source-inventory initial step and G0 mutation evidence remain separate and are not overwritten by native execution. Repeated mutation commands archive the prior mutation output under `mutations/history/`; an early refusal replaces only the current result, never leaves an old PASS as current. Use distinct output roots/checkouts for concurrent invocations.


Latest actual attempt: run40938100721 at tested merge7db34c265162dc2538720729ac6212355e4e3e6d refused on project2 P15Hazard compiled census46versus45 after two project results. Artifact12927120552 (745675bytes; SHA2566c4fd6359a7e57732468077121ea32cf749024d6d9f160a9a40ffb58b1413eb6) preserves the failure. The eight-project tool remains unqualified until actual full-scope success.


### CBZ-MATH-C8-QUARANTINE-01

Use [tools/check_c8_quarantine.py](tools/check_c8_quarantine.py), [registry](tools/c8_quarantine_registry.json) and [scope/commands](docs/cbz/C8_QUARANTINE.md). Run `python -B -S tools/check_c8_quarantine.py` for integrity only; use `--consume` or `--consume-output` for explicit nonadmission. Denied sources/106 outputs return1; exact 3 witnesses and unrelated inputs return2 NOT_COVERED.

Run `python -B -S tools/c8_quarantine_mutations.py --output .lake/c8-quarantine/mutations` after the normal/optimized harness and workflow tests. The source-bound cut requires healthy unchanged 41-method baselines, all 13 intended assertion kills per mode, and independent health for every CLI call. The14 harness controls reject startup/input-dependent crashes, invalid JSON/typed structure, errors/skips, multiple failures and stale evidence. Original legacy replay blocks stay diagnostic and byte-preserved. Receipts alone do not establish global A8/A3 or theorem closure.


- **CBZ-C2-ORACLE-QUALIFICATION:** `tools/cbz_c2_oracle_qualification/REGISTRY.json` and sibling README. External qualification preserves original C2 oracle SHA256 `b462b1b24613f74abd66042e0f347f69423595e9a1aedf1c6b45197425afe075` and both original packets. Observed Python 3.12.14 normal/optimized: original 38 methods; external 25-case complete baseline; runner 12 controls; 12/12 actual source mutants killed at intended assertions with zero mutant errors/skips. Runner rejects surviving, startup/input-dependent crash, stale, wrong-assertion, skipped and incomplete-case evidence as kills, and refuses a source changed after its pin read. Exact scope is nine supplied closed-form enclosures plus declared finite operation guards/remainders; no Gaussian derivation, full engine proof, kernel, semantic or federation certificate. Owner: none; maintenance: zero. Replay commands and new-output-path requirement are in the component README.
- CI command coverage: `.github/workflows/c2-interval-audit.yml` preserves original59a authentication and run bytes, adds tool-directory PR eligibility, and runs the runner controls and full finite cuts in normal/optimized modes. The exact added shell body passed locally; hosted qualification remains NOT_EVALUATED until an actual run is observed. An always-after-started-step artifact retains copied source/evidence for30 days with the repository's existing pinned upload action.

- C2 oracle qualification now requires phase-sealed current-source evidence. The original oracle remains SHA256 `b462b1b24613f74abd66042e0f347f69423595e9a1aedf1c6b45197425afe075`; its25 external test method bodies and22 packet files are unchanged. Current19 runner controls reject setup/teardown/cleanup assertions as kills and retain genuine BODY assertions, typed event-counter provenance and stale-output refusal. The standalone44-method component passes in both modes; fresh12/12 source-mutant cuts pass with every25-case baseline body attested. Earlier12-control observations remain historical. Existing CI commands discover all19 current controls automatically; hosted execution of this repair remains NOT_EVALUATED. Scope stays the nine supplied closed forms and declared finite checks, with no broader analytic/kernel/federation certificate.

- C8 lifecycle repair supersedes the earlier14-control collector for current qualification. The C8 checker remains SHA256 `ee09075645f68e73a30037457a3c535825a8dd369e4de73680753fe92cab11b4`; packet and41 core tests are unchanged. The repaired harness has22 controls and requires typed `unittest.body-phase/v1` evidence: complete setup, actual body entry/exit, successful teardown/cleanup and matching failure-event counters. Only the designated BODY AssertionError kills; CLI health must belong to that selected body. Actual setup/teardown/cleanup assertions now refuse in normal/optimized Python, genuine body kills remain valid, and reused observation paths refuse before launch. Fresh current-source cuts again kill13/13 mutants in both modes. Earlier cuts remain historical without retroactive lifecycle attestation. Scope remains the C8 quarantine boundary; no arithmetic/kernel/global isolation or CBZ admission.
