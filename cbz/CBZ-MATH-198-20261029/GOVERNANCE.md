# Contribution governance and tool ownership

The owner’s 29 October 2026 Crystalline Baseline Protocol controls this work.
Shared federation integration belongs to main#684's canonical writer. This
contribution opens no research front and requires no human/quorum approval.

Immutable rules: no placeholders or unverified axioms; no floating-point
certification or weakened mathematical bounds; preserve failing tests and exact
quarantine boundaries; identify vacuity; report only observed verification;
exercise certification tools with adverse/mutation controls. The accepted Lean
axiom set is `propext`, `Classical.choice`, `Quot.sound`. Compiler/dependency
trust remains explicit. A finite Python suite is not a formal proof of Python
correctness and a static scanner grants no kernel proof credit.

Operational statutes: keep source immutable throughout a campaign; inventory
complete source file sets and bytes; serialize native compilers; preserve failed
attempts and costs; use explicit pinned runtimes; keep outputs outside source;
separate historical evidence from current execution. Relocating a quarantine
path changes its prefix only; the exact source hash remains checked. Public
quarantine is a source-identified projection, not a competing federation index.

## Tool registry

All tools have maintenance owner `none — self-contained`. The common command in
README runs their controls; source-bound receipts identify the exact tested code.

| Tool | Purpose | Self-verification | CBZ criteria served |
| --- | --- | --- | --- |
| `tools/layer_a_audit.py` | Bounded exact-inventory Lean lexer/import/quarantine and rational certificate checks | Scanner suite and four weakened-scanner code mutants; declared threshold4/4 killed | 4,7,9 |
| `tools/contribution_gate.py` | Literal-argv local replay, complete source freeze and truthful scope reporting | Real failure, source-set/hash drift, malformed plans and timeout tests | 5,9,11 |
| `tools/recorded_process.py`, `tools/process_supervisor.py` | Bounded Linux owned-subtree lifecycle, streams and receipts | Nested sessions, double forks, parent death, output limits and descendant cleanup controls | 5,9 |
| `tools/owned_kernel_audit.py`, `tools/owned_kernel_controls.py` | All owned module-table declaration occurrences, private/aux bodies/types/axioms and exact198 target coverage | Inventory/provenance/parser tampering, omission/cycle controls and executable bad-body/axiom rejection controls | 3,4,5,6 |
| `project/rebuild.py`, `project/support/process.py` | Pinned fresh proof graph compilation and198 explicit kernel body/type/declaration/axiom checks | Retained-interruption accounting control and actual fresh Lean execution | 3,5,6 |
| `project/integration/engine_audit/catalog.py` | Exact49 endpoint source/saved-evidence catalog | Catalog CLI, metadata/statement/proof/source-binding tampering | 3,9 |
| `project/integration/engine_audit/ul_engine/` | Request/state-capacity-aware checkpoint transport and search | Resource/lifecycle/deadline/alias/fairness controls | 5,9 |
| `project/integration/native_worker/{native.py,session.py,runtime_support.py,pinned_runtime.py,exec_guard.py,verify_native_saved.py}` | Explicit pinned native build, typed known-proof reuse, fresh worker verification, exact saved controller/wire binding | Runtime relocation, exact controller inventory, malformed/omitted certificate and teardown controls; actual native replay | 5,9 |
| `project/integration/corpus_admission/{admission.py,fixture_builder.py,run_verification.py}` | Strict saved-policy corpus admission and explicit fixture-only positives | Contamination/split/provenance/typing denials and normal/optimized CLI campaign | 5,9 |

For individual CLIs use `python -B PATH --help`; Python test suites run via
`python -B -m unittest discover -s tests -v` and the same command with `-O` from
this directory and each listed component directory. Native replay is orchestrated
by the README command. Historical source snapshots are data, never gate code.
