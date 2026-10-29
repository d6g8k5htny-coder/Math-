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


Transport regression: tests/test_workflow_receipt_transport.py executes the
workflow's literal Bash pipeline against synthetic log/receipt output. Run
`python -B -S -m unittest discover -s frontiers/determinant_moment_20261025/tests -p test_workflow_receipt_transport.py -v`
from the repository root, and repeat with -O. It includes a historical-placement
mutation and gate-failure propagation. It is a bounded transport test, not a
Lean-result generator. The existing workflow runs these controls in both modes
before the actual Lean gate and uploads the aggregate console separately from
receipt-hashed logs. Source is manifest-bound; maintenance owner none. Current
successor execution is pending at publication; use the actual run/artifact.


| artifact_integrity.py | Narrow downloaded ZIP/receipt verifier. Requires --archive, --expected-commit, --expected-manifest and --output. Authenticates all receipt.logs bytes and both independent identities; no kernel credit.17 actual ZIP/CLI fixtures and six intended policy mutants, pending hosted execution at publication. Maintenance owner none; serves G0/G6/G8/G11 within this metadata boundary. |

From the repository root, run the complete component suite serially in normal
and -O Python modes, and repeat tests/run_cbz_mutations.py with --output outside
the package. The runner now retains all six earlier outer mutants and adds six
artifact-policy mutants: log hash, commit, manifest, duplicate member, unsafe
member and empty inventory. Threshold12/12 exact intended kills in each mode,
with same-selection passing baselines and no test/import errors. The dedicated
downloaded-artifact workflow runs those commands and preserves their raw logs.
Its request file pins the old negative artifact12924995112 and repaired positive
artifact12928575403 including source identities and independently observed ZIP
digests. A positive result means byte transport integrity only.


Durable preservation is part of that same workflow: after successful downloads
and checks it records only the two raw ZIPs, four reports, SUMMARY.json,
SHA256SUMS and README under evidence/cbz-determinant-transport-20261029/ on a
fresh evidence branch. Every created Git blob is checked against its exact
bytes and the new tree is read back without truncation. PUBLICATION.json names
the resulting branch/commit/file SHA256s. Integrate that ordinary descendant
after checks; future local verification uses those committed ZIPs and requires
no90-day artifact URL. No mathematical status is awarded by publication.
