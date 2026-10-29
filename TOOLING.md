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

The auditor has a narrow self-mutation gate. Run `python3 -B -S -m unittest discover -s tests -p test_cbz_kernel_mutations.py -v` (and the same with `-O`) and `python3 -B -S tools/cbz_kernel_mutations.py --output .lake/cbz-kernel/mutations`. The runner requires the unmodified 44-test suite to pass in both modes, then kills all eight declared nonstale guard mutants by their one intended assertion, with zero errors/skips/startup failures. The real Lean preflight also removes theorem-value traversal in one generated auditor and requires the compiled sorry control to expose the false clear result. A compiler failure cannot count as a kill. These are bounded auditor self-tests, not full semantic or all-generated-code qualification.

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
