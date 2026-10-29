# P15 contribution status

This directory is a self-contained P15 proof, bounded native proof-reuse and
verification contribution to the Universal Law federation. Canonical federation
integration and cleanup are coordinated in main#684. It is not an RL training run.

## State

**LOCAL_CONTRIBUTION_PASS; federation Partial Baseline; CBZ-0=false.**
A fresh clone of source commit `23474d09e6ba0018b2de598b6fe933f5ca5eb35b`
passed all17 local jobs with fresh external proof/native caches. Every delivered
execution input retains the exact tested hash in evidence/SOURCE_BINDINGS.json.
The selected relocated Lean executable was actually used. Global current-trunk
regressions, refs/PRs, pin synchronization and the federation tagged cold start
are separate obligations; none is inferred from this result.

## Closed and observed

- 198 explicit theorem-body/type/declaration/axiom checks over29 fresh proof
  modules:49 original packet endpoints,4 helpers,96 General results,49 wrappers.
- All30 owned modules:889 logical module/name occurrences,882 unique names,
  including886 bodies and3 primitives. Every duplicate equation-theorem body is
  checked separately. The primitive module is replayed with pinned leanchecker.
  The1109 codegen-only extra names have an explicit IR-only boundary.
- 204 Python tests in each normal/optimized mode:92 auditor/supervisor tests,
 43 engine tests,44 admission tests,24 native-adapter tests,1 accounting test.
- Four scanner source mutants killed; all7 native rejection/cycle/weakening
  controls pass. Original failed attempts remain preserved as forensic evidence.
- All49 native endpoint certificates exported, verified in-session and rechecked
  by a fresh worker; wrong-target/open-term/forbidden-axiom controls reject.
  All4 workers acknowledge shutdown, exit0 and require no forced termination.
- Only propext, Classical.choice and Quot.sound are permitted transitive axioms.

These are source-exposed known-proof reuse results. No learned policy, eligible
scientific training corpus, discovery, novelty or measured speedup is claimed.

## Quarantine boundaries

QUARANTINE.json contains seven exact records projected from the canonical private
index identified in QUARANTINE_PROJECTION.json. PROOF_INDEX.md preserves all198
CLOSED names and the full relevant boundaries. Owner is none; maintenance zero.

The unrestricted historical Talagrand prize and modern threshold conjectures
remain unproved. General/Threshold defines the goals and proves conditional
reductions, not universal palette/price-certificate existence. Generic handwritten
counterexamples outside the accepted graph, corpus/learning effectiveness and
unmeasured scaling remain quarantined. Failed first campaigns and unsupported
historical exploration/seal entrypoints remain inactive data. No closed proof
imports a quarantined mathematical assertion. Strong hypotheses and original
bounds remain part of every CLOSED signature; the two-block local-cover regression
supplies a nonvacuous localization example.

## Tools and exact replay

Run from this directory on Linux x86_64 with Python3.12+, Git, /proc and prctl
process support; provide16GiB RAM and the documented pinned external runtime.
RUNTIME.md has the exact standalone installation commands and eight dependency
pins. External compiler/shared libraries and precompiled Mathlib caches remain
trusted inputs, not an independently rebuilt compiler/library proof.

Lean4.34.1 executable SHA256 is
`e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550`;
leanchecker SHA256 is
`ccef1bfe9bfeecea65137d94a69033c1a89f360711f50fa3178e7ba3e696fcbe`.
Mathlib commit is `d13f23b723b8a846827a245b89c10fc7d3f11612`.
Serialize heavy native execution. New output/build destinations must not exist.

```sh
python -B tools/contribution_gate.py --source "$PWD/project" \
  --lean /ABS/LEAN_4_34_1/bin/lean --mathlib-root /ABS/MATHLIB_D13F23B7 \
  --build-dir /ABS/NEW_BUILD --output /ABS/NEW_EVIDENCE
```

The command runs all17 jobs, preserves failures/resources, checks exact complete
source file sets before/after children, and emits LOCAL_CONTRIBUTION_PASS only for
observed success. It always emits cbz_zero:false. It launches no training.

| Tool | Purpose |
| --- | --- |
| tools/layer_a_audit.py | Bounded formal-source lexer/inventory/import/quarantine plus exact-rational certificate checks; grants no kernel proof credit. |
| tools/owned_kernel_audit.py and owned_kernel_controls.py | Paired compiled module inventories, all logical occurrence types/bodies/axioms, primitive replay and actual rejection/weakening controls. |
| tools/contribution_gate.py | Full literal-argv replay and complete immutable-input inventory. |
| tools/recorded_process.py and process_supervisor.py | Bounded Linux owned-process cleanup and stream/CPU/RSS receipts. |
| project/rebuild.py and support/process.py | Pinned fresh proof graph and198 explicit checks. |
| project/integration/engine_audit | Exact49-endpoint evidence catalog, checkpoint transport/search and resource admission. |
| project/integration/native_worker | Pinned builds, typed fixed actions, fresh structural certificates and saved wire/source integrity. |
| project/integration/corpus_admission | Strict provenance/exposure/family split admission; positive examples are fixtures only. |

Individual Python suites use `python -B -m unittest discover -s tests -v` and
`python -B -O -m unittest discover -s tests -v` from this directory or each
component directory. GOVERNANCE.md is the contribution tooling registry and
Layer B rules; the append-only canonical decision ledger belongs to main#684.
ACCEPTANCE.json and evidence/cold01 contain the actual source-bound observations.

## Immutable invariants

No logical placeholders or unverified new axioms. No floating-point mathematical
certification or weakened bounds. Preserve failing tests and exact isolation
boundaries. Mark vacuity. Report only observed verification. Self-test auditors
and retain mutations/failures. A saved receipt is not a new kernel execution,
a definition is not a proof and a local pass is not federation CBZ-0.
