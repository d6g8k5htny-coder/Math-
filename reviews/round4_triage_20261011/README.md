# Round-4 triage table (2026-10-11) — scheduling artifact, no authority

**Scientific effect: NONE.** This directory publishes, byte-exact, the triage table that classified the 82
registered Props of `specifications/lean_statements_20261010` that had no proof-packet theorem before round 4
(74 rows; the other 8 are P15 parametrised predicates the proof packet's README had already classified as
vocabulary). It exists so that a nonauthor reader of Math- PR #434 can compare the register's "Round-4 triage"
sentences and the proof-packet README rows with their source. It is published on a reading branch only; it is
not part of any packet, gate or receipt, and nothing consumes it.

- `triage_table.json`: 74 rows with keys `declaration`, `module`, `group`, `verdict`, `effort`, `route`,
  `finding`, `mathlib`, `probes`. sha256 `91c3f8d6fd39fdd13c59bd4fef420fa6d4c9338945f1ca6b74edf46ef668de83`, 201,423 bytes.
- Produced on 2026-10-11 by this lane's triage workflow (Anthropic / Claude, Claude Code cloud session
  `session_01Cz7WZybv8znP64SpPj6sWY`; same GitHub account as every lane, organizational-independence credit 0).
- Verdict vocabulary: `PROVABLE_NOW`, `PROVABLE_WITH_WORK`, `BLOCKED_MISSING_MATHLIB`, `BLOCKED_INTERFACE`,
  `PREDICATE_VOCABULARY`. These are **work-scheduling labels with no authority over any register label**:
  no claim-level `formal_progress`, no LANDING_CLAIMS disposition, no PROOF_INDEX entry and no alignment status
  changes because of a verdict. `BLOCKED_INTERFACE` records interface under-determination (a concrete inhabitant
  of the interface refutes the Prop), never a statement defect. `BLOCKED_MISSING_MATHLIB` names what is absent at
  Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`; the lemmas it lists as present are the ones inspected, not the gap.
- The `probes` entries describe scratch Lean elaborations made during the triage. **Probes are not receipts and
  are not cited as evidence anywhere**; they were run on an unverified worktree and record nothing about any commit.
- Where this table and a committed register sentence disagree, the register (Math- PR #434, head `48bfcbae`)
  was derived from this table by scripts kept outside the repository and the difference is a defect to report
  on that PR; neither document moves a status.

Alignment of every statement with its anchor stays `PENDING_INDEPENDENT_REVIEW`.
