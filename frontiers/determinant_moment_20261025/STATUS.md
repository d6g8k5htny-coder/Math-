# Component status: determinant compiled admission

This file covers only frontiers/determinant_moment_20261025/. It is not a federation CBZ status or a global proof index.

Current boundary: **QUARANTINED**. Package-wide A2/A8 compiled completeness and transitive axiom-closure evidence for the exact13 source modules plus root remain unestablished. No actual forbidden axiom finding is asserted. Real repaired-gate Lean execution is **NOT_RUN**; no current CBZ CLOSED claim or active kernel receipt is supplied. See [QUARANTINE.json](QUARANTINE.json) for the exact source/module hashes, missing evidence, attempted work, resumption cost, isolation, owner:null and maintenance:zero.

The repaired Python gate retains all original proof bytes and prior checks, adds compiled-package admission, and invalidates the active .lake/formal-evidence/receipt.json before CLI qualification. Historical proved metadata, handoff files and immutable final receipts remain scoped historical inputs.

## How to verify

Run these exact commands from this component directory:

```sh
python -B -S -m unittest discover -s tests -v
python -B -O -S -m unittest discover -s tests -v
python -B -S tests/run_cbz_mutations.py
python -B -S gate.py
python -B -S gate.py --execute
```

The unit suites and portable five-case mutation gate must exit0. The mutation runner uses the current interpreter, disposable copies outside this source tree, green selected baselines and exact intended assertion failures with positive test counts; import or zero-test failures do not qualify. It verifies source preservation. Add --output with a directory outside the component to retain its reports; without it, JSON results are printed and temporary copies are removed.

Current local engineering verification:109/109 unit tests passed in each Python mode, and all five portable mutation cases were rejected for the intended assertions. All78 original test bodies and all14 Lean source paths remain unchanged. These results do not supply the missing actual package-wide kernel/axiom evidence.

Both current gate CLI commands must exit1 with CBZ_COMPILED_INVENTORY_UNQUALIFIED because the actual non-target compiled inventory binding is absent. This intentional quarantine result is not a successful Lean run. A structurally supplied binding alone still cannot make a source-only invocation award execution.

[TOOLING.md](TOOLING.md) explains the actual execution stages, portable commands, verification records and resumption requirements. [GOVERNANCE.md](GOVERNANCE.md) states authority and evidence limits. Qualification requires the actual pinned Lean census, bound non-target inventory, kernel replay, all-constant axiom closure and every retained/new control; approval family is not the blocking reason.

