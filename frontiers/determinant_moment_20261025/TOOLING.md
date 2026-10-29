# Determinant gate tools

Run commands from STATUS.md serially. No additional Python packages are required.
The exact Lean toolchain/Mathlib/dependency revisions remain unchanged.

| Tool | Purpose and verification boundary |
|---|---|
| gate.py | Authenticates source/dependencies/runtime, fresh build/checker, targets/types, complete inventory, two compiled and five proof/axiom controls, before/after identity, source/run-bound receipt. New loader tests reproduce stale pyc and changed-source attacks. |
| compiled_inventory.py | Exact core ff8 helper; generates and strictly parses module ConstantInfo/closure protocol. Existing core auditor controls remain separately source-preserved. |
| determinant_inventory.py | Lossless typed91-record binding,20 internal proofs, exact module IR counts and four compatibility pairs. Frozen baseline and intended-finding checks for the unchanged core injection payloads.39 policy/harness tests include actual historical census and synthetic external responses. |
| tests/run_cbz_mutations.py | Six cases, each selected green baseline followed by exact intended assertion failures. Core-policy mutation fixtures deliberately rebind the independent source hash to measure policy deletions. No Lean execution. Optional --output outside source retains raw logs. |
| tests/run_adapter_mutations.py |12 cases times two actual Python modes with exact selected-case/phase outcomes, positive baselines and unique retained output. Five adverse runner tests include import/runtime/setup/teardown/cleanup and invalid-status cases. No Lean execution inside these controls. |

Every tool is self-contained; maintenance owner none. These bounded controls
serve G0/G2/G4/G6/G11 only within their stated domain; none certifies every
Layer A property in the federation. Old target-only and historical package
receipts retain their original checked_commit and scope.

[COMPILED_BINDING.md](COMPILED_BINDING.md) explains actual census provenance and
compatibility. The41 IR extra counts are metadata; names/payloads are not
authenticated. The module table and transitive closure concern kernel
ConstantInfos. No broader continuum statement is claimed by that audit.

The native workflow installs the unchanged pinned Lean/Mathlib setup, runs the
component and shared source controls in both modes, retains adapter mutation
logs, then invokes gate.py --execute. Its complete runtime path subsumes the
previous build/checker/raw-observation steps and adds exact admission, closure,
seven controls and final identity. Nothing is disabled to hide a failing check.
Actual current-source gate outcome must be read from the run/artifact.

Publication evidence:171 component controls pass each mode in retained successful
local runs; one earlier parallel normal run has8 retained temporary-path errors
and was rerun serially.24 paired adapter mutations all killed; both production
loader/evidence defects independently reproduced and corrected. Actual repaired
Lean gate execution remains pending at this source-publication checkpoint.
