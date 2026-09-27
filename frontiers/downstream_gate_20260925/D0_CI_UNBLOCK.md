# D0 CI unblock — main PR87 packet allowlist

**Object:** D0-PACKET-ALLOWLIST-FIX-20260925-v1  
**Author:** Cursor. **Scientific effect: NONE.**

## Diagnosis

[main PR87](https://github.com/d6g8k5htny-coder/main/pull/87) (`chatgpt/downstream-crosswalk-20260925`) adds `docs/math_status/DOWNSTREAM_CROSSWALK_20260925.md`. Hardening `ci` / `math_status_check.py` fails with:

```text
PROBLEM packet: unexpected files ['DOWNSTREAM_CROSSWALK_20260925.md']
```

Observed on Actions runs `36135447237` and `36135443158`. Navigation and withdrawal-governance checks already SUCCEEDED.

Root cause: `EXPECTED_NAMES` / `TRANSCRIPTION_NAMES` in `tools/math_status_check.py` and `PACKET.json` transcriptions do not yet list the new crosswalk file.

Secondary hazard: the prose line `None sets D3 lemma_closed=true.` matches `ASSIGN_TRUE` and would fail after allowlisting; rephrase to `None promotes D3 lemma_closed.`

## Exact fix (ready to apply on main)

Portable patch: [`patches/d0_packet_allowlist.patch`](patches/d0_packet_allowlist.patch)

Applies on top of PR87 head `3d4969ab40d36a38ebf6ea1c3608035a706a7576`:

1. Register `DOWNSTREAM_CROSSWALK_20260925.md` in `TRANSCRIPTION_NAMES` and `NOTE_PHRASES`.
2. Pin sha256 `d53b286029d034576245406152c188fe2470ccb089e51f73e9087e34bf5a0e10` (4804 bytes) in `PACKET.json`.
3. Rephrase the `lemma_closed=true` negation as above.
4. Docstring: six → seven transcribed bodies.

Local verification after apply: `python tools/math_status_check.py` → `problems=0`, `lemma_closed=false`.

## Why this is filed in Math-

Cursor Cloud Agent has **Contents:Write on Math-** but received **403 pushing to `d6g8k5htny-coder/main`**. The fix was prepared and locally verified in a main worktree; it could not be published on that forge tip from this session. This note + patch are the source-bound D0/D7 unblock recipe for an agent/owner with main write access (or for merging into PR87).

## Non-claims

- Does not merge PR87.
- Does not flip any scientific Boolean.
- Does not edit Math- PR7.
- Does not touch the #91 Drive vault.
