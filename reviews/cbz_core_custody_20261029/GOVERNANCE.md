# Core source-custody tool registry

2026-10-29 — Layer B: core custody belongs in the existing formal/gate.py
compatibility wrapper. The reviewed gate_helper.py collector remains unchanged;
no theorem statement, bound, dependency revision or axiom policy is loosened.

Tool: formal/gate.py, with formal/tests/test_source_custody.py and
formal/tests/test_source_custody_mutation.py.
Purpose: exact committed/loaded source and pinned-dependency byte identity before
and after kernel execution; correct effective process root and truthful receipts.
Commands and finite self-verification: formal/SOURCE_CUSTODY.md.
Owner: none, self-contained. CBZ criteria served: 4, 6, 9, 11.
Initial observed source qualification: 5522d13478b8ec0baa803a98356592ff1b8c1efe,
266 tests/mode, 11/11 source mutants/mode, 20 real-Git cases, no skips.
The tracked-dependency-link extension is separately tested on its exact successor;
the earlier observation is not transferred to changed code.

Tool: .github/workflows/cbz-core-custody.yml.
Purpose: pinned Python/Lean hosted source qualification, actual kernel gate,
independently checked downloaded raw artifacts and recoverable Git preservation.
Usage: trusted branch push or the Math #537 PR workflow.
Self-verification: source tests/mutants, actual kernel outcomes and exact Git blob
plus complete tree readback; no green is inferred before these observations.
Wire verifier reuse: immutable 4351227b53a3f7f401e59d129530fb68055d0284,
SHA256 77463e76d49fc68c0e8db85f6671fc7a0efaccecd93727572b3d02242b8647b1;
its own tests/source mutations are maintained by the determinant integrity lane.
Owner: none, self-contained. Criteria: 6, 9, 11.

Tool: .github/workflows/cbz-retire-superseded-runs.yml.
Purpose: free CI capacity by cancelling obsolete PR-run source cuts after fresh
identity/status rechecks, while retaining all current-head runs/tests/artifacts.
Usage: trusted branch push that changes this workflow. Seven selection controls
run before any action; the actual source-bound report is uploaded and logged.
Observed: 40947126080/job123705321047 SUCCESS, 93 enumerated nonterminal runs,
27 cancellation requests, 63 current/terminal records retained. This is run
orchestration only and earns no mathematical/test pass.
Owner: none, self-contained. Criteria: 5, 6, 9.

Successor adds three simulated cancellation outcome/order controls to the seven selection controls and persists an in-flight record before each cancellation request. Run 40950835486 failed after a nonzero cancellation response and produced no partial report; any earlier cancellation requests in that run remain unattributed. The successor remains unqualified until its actual execution is observed. A completed run encountered after a refused POST is recorded as already terminal, not as a successful cancellation.
