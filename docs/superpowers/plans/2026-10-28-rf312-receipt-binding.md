# RF312 receipt binding implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for this single task, followed by one fresh whole-branch engineering review.

**Goal:** Make the current required-check consumer bind the producer's exact base-manifest plus overlay identity while retaining explicitly non-overlay legacy behavior.

**Architecture:** Add a fixed opt-in declaration to the base manifest. The consumer derives one identity from that declaration and the original bytes; it never accepts whichever of raw/composite happens to match. Preserve the producer, helper, overlay and every mathematical source byte.

**Tech Stack:** Python standard library; existing unittest suites; no new dependency.

**Spec:** [DCL-RF312-BIND-001](https://github.com/d6g8k5htny-coder/Math-/pull/312#pullrequestreview-5658582326), [current source reconciliation](https://github.com/d6g8k5htny-coder/Math-/pull/312#issuecomment-6467595927), and [actual new author pickup](https://github.com/d6g8k5htny-coder/Math-/pull/312#issuecomment-6468228926).

## Global constraints

- Base source head: `66d66e43e3f3f58835bc938717dacf8532aaffc3`; current Math Main `4a0d51bbd06f0d9ac731a1d1df38f25999797135` is a separate integration cut.
- Four paths only: this plan, `formal/manifest.json`, `tools/required_formal_check.py`, `tests/test_required_formal_check.py`.
- Exact declaration: `"source_identity": {"schema": "rf312-overlay-v1", "overlay": "manifest.overlay.json"}`.
- Declared mode hashes `manifest_bytes + b'\0RF312-OVERLAY\0' + overlay_bytes` exactly as the unchanged producer does.
- Legacy mode requires both declaration absence and reserved overlay absence; explicit null, unknown contracts and undeclared overlays refuse.
- Overlay must be the fixed regular non-symlink sibling and strict JSON with exactly `schema_version` (integer1) and `files` (string-to-lowercase-64hex bindings).
- Preserve checked commit/run/attempt, clean dependency locks, both runtime observations, receipt/log bytes and all existing acceptance predicates.
- No proof/Lean/source-target/producer/helper/overlay/workflow/status changes, no real Lean or kernel execution, no CI request, Ready or integration. Existing unit fixtures may invoke only copied-tree metadata CLI validation and synthetic runtime responders.
- Three D2 companion pin/raw-receipt holds remain separate and unchanged. Old reviews/receipts keep their original identities; predecessor closeouts remain UNKNOWN.

## Review focus

- Legacy raw receipts must remain valid only without any declaration or reserved overlay.
- Unknown/null/extra/path-changing identity declarations and duplicate/invalid JSON must refuse.
- Missing/dangling/symlink/directory overlays must refuse before reading any target.
- Raw/composite source drift and a raw-receipt downgrade must fail without rewriting the original receipt.
- The bridge regression must call the actual producer source-check and actual consumer; its runtime receipt remains an explicitly synthetic fixture, not kernel evidence.

## Task1: Reconcile source identity at the receipt boundary

**Files:** the four exact paths above.

**Interfaces:** Keep `bind_receipt(receipt: Path, manifest: Path, env: dict, git_head: str) -> dict` unchanged. Add internal `manifest_identity(manifest: Path, raw: bytes) -> str`; reuse existing strict JSON validation, context checks and dependency-lock validation with the same captured base bytes.

- [ ] Run clean existing consumer67 and formal244 unittest suites in normal and optimized modes. Expected: all pass.
- [ ] Add an actual-producer→fixture-receipt→consumer success test and direct malformed/downgrade/refusal controls. Run before production edits. Expected: the bridge fails with the original manifest/receipt mismatch and weak old-consumer cases are exposed.
- [ ] Add only the fixed declaration to the base manifest and implement strict identity selection in the consumer. No raw fallback in the overlay regime.
- [ ] Run the new consumer scope and both complete affected suites in normal and optimized modes. Expected: all existing/new methods pass; no real Lean, dependency/network or mathematical execution.
- [ ] Verify all old manifest fields and every non-owned source/overlay/helper/Lean/workflow byte remain exact; run whitespace validation and record the new raw/composite identity.
- [ ] Commit, obtain separate exact-tree engineering review, then publish at most one expected-old-head guarded fast-forward amendment to existing#312. Keep Draft and release only this source role. Fresh current-base/Ready/hosted qualification and integration remain separate.
