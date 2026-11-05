# CBZ packet source admission implementation plan

> **For agentic workers:** use superpowers:subagent-driven-development; owner explicitly opts out of questions/approval waits.

**Goal:** Close demonstrated omitted-source declaration acceptance in two existing Lean packet gates.
**Architecture:** One bounded source census helper, two existing gate adapters, exact manifests and adverse/self-mutation controls. Preserve target APIs and proofs.
**Tech Stack:** Python standard library; unchanged Lean4.34.1/mathlib d13f23b7 projects.
**Spec:** ../specs/2026-10-29-cbz-packet-admission-design.md

## Global Constraints
No proof changes, weakening/deletion of tests, fabricated execution, permissive unparsed syntax, scientific/status promotion, broad new scanner or new research.

## Review Focus
- Private/protected/indented/attributed declarations cannot silently disappear.
- Nested comments and strings cannot hide or fabricate declarations.
- Adding an unused axiom/sorry/native-code dependency fails even after file hash rebind.
- Helper substitution/symlink must fail before untrusted helper execution.
- Source census must not be described as compiled-environment coverage.

### Task 1: Repair both packet admission boundaries
**Files:** tools/lean_packet_admission.py; tests/test_lean_packet_admission.py; frontiers/determinant_moment_20261025/gate.py, manifest.json, tests/test_gate.py, README.md; frontiers/cap_first_exit_lean_20261002/gate.py, MANIFEST.json, existing test files, README.md. Add narrow determinant workflow only if needed; do not change core formal gate.
**Interfaces:** helper returns deterministic ordered declaration records with module/namespace/name/kind/privacy and rejects unsupported syntax; each gate checks fixed helper SHA and exact census in its manifest while retaining its existing target list.
- [x] Inspect supported current source grammar and existing helper/test patterns before choosing parser detail.
- [x] Add source-fixture tests with all source file hashes rebound but no declaration census update: private/indented/attributed declaration, unused axiom/sorry/native_decide must be rejected. Observe actual RED.
- [x] Implement fail-closed supported grammar and exact census; legitimate current sources pass, proof bytes unchanged.
- [x] Add comment/string/unterminated-input, namespace/section, malformed census, helper substitution/symlink tests.
- [x] Update only actual gate/test/helper hashes and source-census metadata, never proof hashes to conceal edits.
- [x] Run normal/-O helper and both packet suites, source gates, and core regression to detect interaction. Record all failures/skips.
- [x] Isolate mutants removing census/forbidden-token/helper-integrity checks; tests must kill each. Report actual killed/total, no declared full G0.
- [ ] Ensure real hosted packet gate can execute via existing Cap and narrow determinant route with retained logs. No local kernel claim if runtime unavailable.
- [x] Document exact usage, bounded coverage, residual compiled-census gap, registration text; self-review and commit only owned files.
### Task 2: Review/publication
- [x] Independent source review and resolve findings.
- [ ] Fresh branch/PR/head reconciliation, publish tested commit.
- [ ] Observe actual hosted output, repair concrete failures, and deliver exact evidence to canonical #684 single-writer integration.


Current source completion: `5591b44`; composition of published default `e877242` is `6a988d1`.
Whole-branch review and scoped fix reviews retained under `cbz/evidence/source-admission-db642-20261029/`.
Two final findings are addressed, including LF physical-line correspondence. Hosted qualification and canonical integration remain unobserved at this publication.
