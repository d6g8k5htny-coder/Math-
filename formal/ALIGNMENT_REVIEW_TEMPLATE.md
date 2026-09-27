# Formalization alignment review — template

Copy this file to `reviews/formal_alignment_<claim_id>_<YYYYMMDD>/REVIEW.md`, fill every field, and register the record in `formal/FORMALIZATION_STATUS.json` under `entries[].alignment_review.record` with the file's bytes and SHA-256, the reviewed informal blob, and the reviewed Lean source pins. `formal/formal_gate.py` refuses an `ACCEPT` whose record is missing, mis-pinned, stale against the current Lean sources or informal blob, or authored by the same agent/session as the formalization.

**Scientific effect: NONE.** This review answers one question: *does the Lean statement say what the informal statement says, on the informal statement's exact domain, with the informal statement's exact hypotheses?* It does not re-prove the theorem (the kernel did that for the Lean text) and it does not accept the informal claim (that is the Layer 0 review recorded in the landing manifest).

---

# Formalization alignment review — `<claim_id>`

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes, premises, `claims/LANDING_CLAIMS.json`, or the downstream hard gate.

## Subject

| Field | Value |
|---|---|
| Landing claim | `<claim_id>` |
| Informal statement | `<statement_path>` at blob `<40-hex>` (must equal the landing manifest's `source.blob`) |
| Informal heading | `<statement_heading from the landing manifest>` |
| Formal object | `<formal_object from the registry>` |
| Lean statement | `<package>` / `<module>` / `<decl>` |
| Reviewed Lean sources | one row per pinned `.lean` file: path, bytes, SHA-256 (must equal the registry pins) |
| Registry status at review | `specified` / `proved` / `kernel_checked` |
| Axiom audit at review | `AXIOMS.expected` SHA-256 for each package touched |

## Reviewer provenance

| Field | Value |
|---|---|
| Provider | `<openai / anthropic / xai / google / human / …>` |
| Model / person | `<model family or name>` |
| Agent / session | `<cursor bcId, Codex task id, … ; must differ from the formal author's>` |
| Formal author (from registry) | `<provider / model_family / agent>` |
| Organizational independence | `true` only if the authoritative predicate is met; same-provider review earns none. State the reason either way. |
| Exposure | Which files were read in full. Whether the reviewer ran `lake build`, the axiom audit, or `formal_gate.py --with-lean`, and at which commit. |

## Interface dispositions

One row per `components[]` entry and one for the main statement. `ACCEPT` means the Lean text matches the cited informal location, including quantifiers, domain, normalization, open/closed endpoints and units. `AMEND_REQUIRED` names the exact discrepancy. `OUT_OF_SCOPE` means the component is a prose-only interface and the reviewer confirms it is correctly *not* claimed by any theorem's hypotheses.

| Component id | Informal location | Lean declaration | Disposition | Reason |
|---|---|---|---|---|
| `<statement>` | | | | |
| | | | | |

## Hypothesis audit

List every hypothesis of every kernel-checked theorem and state which informal input it encodes. Confirm that the conclusion does not exceed the informal statement. Confirm that no definition silently strengthens or weakens the informal object (for example a `Prop` defined with `<` where the proof text has `≤`, a parameter fixed where the informal statement quantifies, or a `0` default outside the informal domain that a theorem could exploit).

## Findings

Numbered. Each finding cites the Lean line and the informal line.

## Disposition

`ACCEPT` / `AMEND_REQUIRED`, with the exact scope accepted. An `ACCEPT` here plus a `kernel_checked` status yields the lane verdict `FORMAL_KERNEL_CHECKED_ALIGNED`. It does not change the landing disposition, the hard-gate classification, or any scientific register.

## Registry record to paste

```json
"alignment_review": {
  "status": "ACCEPT",
  "record": {
    "path": "reviews/formal_alignment_<claim_id>_<YYYYMMDD>/REVIEW.md",
    "bytes": 0,
    "sha256": "<64-hex>",
    "reviewer": {"provider": "<...>", "model_family": "<...>", "agent": "<...>"},
    "organizational_independence": false,
    "reviewed_informal_blob": "<40-hex>",
    "reviewed_sources": {"formal/lean/<...>.lean": {"bytes": 0, "sha256": "<64-hex>"}}
  }
}
```
