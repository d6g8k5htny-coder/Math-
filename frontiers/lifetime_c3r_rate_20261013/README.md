# Lifetime note C3-R: a rate after the `ℓ^{2/3}` term — exact records, the controls and a replayable checker

Incorporated on 13 October 2026. **Scientific effect: NONE. No new mathematics and no status change.**

This packet stores one lifetime note in the repository, byte for byte, together with the control script it pins. The note was posted on [main#307](https://github.com/d6g8k5htny-coder/main/issues/307) (the agent message board that continues [main#229](https://github.com/d6g8k5htny-coder/main/issues/229)) and read there in two slices; Slice A was PASS, Slice B an AMEND of one sentence in Remark 2, applied as v1.1 and read back.

- **Note C3-R** (`C3R/`) quantifies note C3 (`frontiers/lifetime_two_thirds_chain_20261007/C3/`): in every `d ≥ 2` and for every `L`, the candidate density satisfies (C3) with remainder `O(ℓ^{2/3+δ})` instead of `o(ℓ^{2/3})`, with the same `c₃`. Admissible exponents: `δ(2) = 1/30`, `δ(3) = 1/50`, `δ(4) = 1/51`, `δ(5) = 1/70`, `δ(6) = 1/89`; in general `δ(d) > 0` is given by Lemma 4. The route keeps the error terms of C3's proofs of Lemmas F₃ and T₁ (Lemmas F₃-R and T₁-R, with free localization exponents), and integrates in C3's fold variable with a split between the fold side and the cusp side. No sharpness is claimed, and no numerical constant is certified.

The directory holds:
- `C3R/`: the task definition, the claim and a checkpoint; the note as read (v1.0, `PROOF_v1_0_AS_READ.md`) and of record (v1.1, `PROOF.md`); the controls comment; the two slice summonses (and the Slice B re-summons) and the two slice verdicts; the author's record of the applied AMEND with the readback summons; the readback verdict; and the read-complete note, which carries this object's claim;
- `controls/`: `c3r_exact.py` (controls E1–E3, the exponent arithmetic of Lemma 4 in exact rationals) and `c3r_mutants.py` (mutants M1–M4), with their recorded stdout in `controls/results/`.

Anthropic Claude, who is also the author of the note, incorporated it under the claim in the read-complete note ([6146954758](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6146954758)). This is custody only; no proof byte and no control byte is changed. `SOURCES.json` pins every stored file by byte count and SHA-256, and `replay.py` verifies all of it and replays the controls.

## Status and attribution

- **Author.** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`), for Dylan Roy (delegated AI work); the serving model changed from Claude Fable 5.1 to Claude Opus 5.5 at about 12:30Z on 13 October at the owner's instruction (same session, claim and custody). The note was revised after an author-side referee round (two same-session subagents, both AMEND, applied before posting; not review evidence; listed in the note's Remark 5).
- **Controls.** The controls comment (`C3R/AUTHOR_CONTROLS_COMMENT.md`) pins the four control files by byte count, SHA-256 and git blob at Math- commit `9232eff05a5753f41c9ea5528f797b7bf1df1967` (branch `claude/dd-model-d-enclosure-wip-20261013`, the author's recovery branch). `controls/` holds the same bytes. The controls check arithmetic only: which error terms appear in (4.1), and the analytic lemmas, are the reads' business.
- **Reads.** Each read is by a Cursor cloud agent running xAI Grok 4.7 (`grok-4.7-high-fast`; non-Claude, nonauthor), summoned one bounded task at a time under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035). GitHub refused each agent a new comment (HTTP 403), so each pickup and verdict is recorded in the agent's cursor[bot] acknowledgement, updated in place. Every read goes through the same GitHub account, so organizational independence is **0**. None is an owner reading.
- **Verdicts are scoped.** A PASS passes the slice as the note states it, conditional on the cited inputs (note C3, note LU, #237, #218, #229 at their stated scopes), and discharges nothing.
- **What governs.** The note's own statements, hypotheses and "not claimed" section govern.
- **Not edited here.** No other packet, no `PROOF_INDEX.md`, STATUS, register or graph.

| Read | Scope | Verdict (reader) |
|---|---|---|
| Slice A | §§0–2: the statement, the route (1.1)–(1.4), the proof of Lemma F₃-R, against C3 §§0–2, 4 and the cited sources | PASS (Cursor `bc-994338a5…`, [6146023223](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6146023223)) |
| Slice B | §§3–6: Lemma T₁-R, the integration (Lemma 4), the numbers, the remarks; the controls replayed in both modes, the mutants rejected | AMEND, one sentence of Remark 2 (what note C7 inherits) (Cursor `bc-ef61bc68…`, [6146366500](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6146366500)); applied in v1.1 |
| Readback | the byte diff v1.0 → v1.1 against the AMEND | PASS, exactly the three stated edits (Cursor `bc-1cf2c41a…`, [6146720347](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6146720347)) |

## Replay

```
python3 -B -S frontiers/lifetime_c3r_rate_20261013/replay.py
python3 -B -O -S frontiers/lifetime_c3r_rate_20261013/replay.py
```

Each run (about ten seconds) checks the tree against `SOURCES.json`, the controls comment's pin table against `controls/`, the named identities in the verdicts and author records, replays `c3r_exact.py` and `c3r_mutants.py` under the current interpreter's flags (exit 0, stdout byte-identical to the stored record, empty stderr), and runs two negative controls (a one-byte change to `C3R/PROOF.md`; `δ(3) = 1/49` in a copy of `c3r_exact.py`), each of which must be rejected. The workflow `.github/workflows/lifetime-c3r-rate.yml` runs the protocol tests and the replay in both modes. Python standard library only.
