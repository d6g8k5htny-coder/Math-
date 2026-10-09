# Lifetime note TS: exact records and a replayable checker

Incorporated on 6 October 2026. **Scientific effect: NONE. No new mathematics and no status change.**

This packet stores lifetime note TS in the repository, byte for byte. The note was posted on [main#229](https://github.com/d6g8k5htny-coder/main/issues/229), with a pickup and a delivery pointer on [main#259](https://github.com/d6g8k5htny-coder/main/issues/259) (IBA2-009). It holds:
- the frozen note and the author's claim, pickup and delivery pointer;
- the controls comment, and the control script `ts_exact.py` with its stdout, extracted verbatim from it;
- the read request and summonses, every nonauthor pickup and verdict of record, the author's successor text for the one amendment, its readback, and the author's read-complete note.

Anthropic Claude, who is also the author of the note, incorporated it under claim [6021671402](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6021671402). This is custody only; no proof byte is changed. `SOURCES.json` pins every stored file (16 files, one control script) by byte count and SHA-256, and `replay.py` verifies all of it.

## Status and attribution

- **Author.** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`), for Dylan Roy (delegated AI work). The author also wrote [N] (#240), #237, #242–#244 and note TL, which the note consumes.
- **Reads.** Three slices and one readback, each read by a Cursor cloud agent running xAI Grok 4.7 (`grok-4.7-high-fast`; non-Claude, nonauthor), summoned one bounded task at a time under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035). Slices B and C passed; Slices A–D asked for one amendment, which was applied as successor text and read back PASS. Every read goes through the same GitHub account, so organizational independence is **0** for all of them. None is an owner reading.
- **Verdicts are scoped.** A PASS passes the slice as the note states it, conditional on the cited inputs, and discharges nothing.
- **Amendments of record.** One. The Slices A–D read [6020822268](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6020822268) found one false comparison in §1 Step 2 (`|x − M| ≤ r|ξ|`; the correct bound is `r√(1 + r²)|ξ| ≤ r√2`). The author applied it exactly, as three replacements in §1, in the successor text [6021299833](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6021299833) §2. Its readback is PASS ([6021301151](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6021301151)). No constant, exponent or stated bound changes, and the stored note body is the frozen one.
- **Author-side referee.** Before posting, three clean-context referee passes in the same session read the note in three slices. They are not review evidence; their reports are kept in the project archive.
- **Conditionality.** Every statement is conditional on the consumed sources at their stated scopes:
  - note TL ([6017975404](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6017975404), read in three slices; its custody packet is Math-#384);
  - [N] (#240), #237, #229, #220, #198, [182], #218, #242 and [R] (R5);
  - #187, for the last form of (TS.1).

  The note's header lists their blobs.
- **What governs.** The note's own statement, hypotheses and "not claimed" section govern, read with the successor text. The summary below paraphrases them.
- **Not edited here.** No other packet, no `PROOF_INDEX.md`, STATUS, register or graph.

| Slice | Scope | Verdict (reader) |
|---|---|---|
| B | §2: Lemma W⁻, (2.2⁻), Lemma GE⁻, Proposition RW⁻; control S3 with M4 | PASS (Cursor `bc-fc3c840f…`, [6020812551](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6020812551)) |
| C | §§3–4: Lemma Δ⁻ and Steps 1–6 of Theorem TL⁻; S4, S6 with M8, M9 | PASS (Cursor `bc-13c209f1…`, [6020820817](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6020820817)) |
| A–D | §1 (Lemma S″), §0 and §§5–7: (5.0), Corollaries TS and TS′, the ledger, the remarks, the header; S1, S2, S5 with their mutants | AMEND, one comparison in §1 Step 2 (Cursor `bc-2bf93428…`, [6020822268](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6020822268)) |
| readback | the successor text [6021299833](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6021299833) §2 against the AMEND | PASS (Cursor `bc-8e7c19e7…`, [6021301151](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6021301151)) |

## What the note states (paraphrase; the note governs)

The setting is note TL's, which follows [N] §0, #237 §§0–1 and #242 §0. `𝐓_r^{eld}` and `𝐓_r^{rej}` are the elder and rejected kernels integrated over the birth height, `𝓐^{rej}(κ, u)` is the rejected cusp limit (#242), and `κ = k/r`.
- **Lemma S″ (a rescaled elder barrier).** For `0 < k ≤ r`, `E_Q[(W_r/r²)e] ≤ Cr²(κ + r)κ^{2/3}P^N`, so `𝐓_r^{eld} ≤ C(κ + r)κ^{2/3}`. This is #220's Lemma S′ improved by the factor `r^{4/3}`.
  - The proof runs [182]'s barrier in [N]'s window coordinates, where the pins make every third derivative `O(𝒩)`.
  - The successor text corrects one distance comparison in its Step 2 (`r√(1 + r²)|ξ|` in place of `r|ξ|`). No constant or result changes.
- **Theorem TL⁻ (the rejected kernel for `κ ≤ 1`).** For each `θ ∈ (0, 1)`, `|𝐓_r^{rej}(k, u) − 𝓐^{rej}(κ, u)| ≤ C_θ(κr² + r³/κ)` on `r^θ ≤ κ ≤ 1`. It is note TL's proof with `κ ≤ 1` scalings.
- **The contact cancellation (5.0).** `r^{−2}𝐀₀(κr, u) − 𝓐^{con}(κ, u) = (e^{−a₀k²} − 1)𝓐^{con}(κ, u)` for every `k ≥ 0`. It removes note TL's ledger row `ℓ²ρ^{−7}`.
- **Corollary TS.**
  - `ν_eld(ℓ) = cℓ^{−1/3} + c₁ℓ^{1/4} + c₂ℓ^{1/3} + ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{4/7}log(1/ℓ))`, and `ρ_rej` likewise.
  - For SIDE24 the relative remainder is `O(ℓ^{19/21}log(1/ℓ))`.
- **Corollary TS′.** Neither the elder nor the rejected density has a term of order `ℓ^{1/2}`. With note TL's `κ ≥ 1` side, this is the global statement IBA2-009 asks for, at the scope of the consumed sources.

## What the note does not establish

From the note's "not claimed" section:
- no sharpness of `4/7`;
- nothing pointwise in `b`, and no identification of further terms;
- no certified numerical value, and no uniformity in `d` or `L`;
- whether IBA2-009 closes, which is for the audit's owners.

## Not included

- **The consumed sources** (note TL, [N], #237, #229, #220, #198, [182], #218, #242, #187, [R]). The packets are on `main` at their own paths; note TL's custody packet is Math-#384.
- **The clean-context referee reports** and their exploration scripts (same provider and session; not review evidence). They are kept in the project archive.
- **Coordination comments** that record no pickup, verdict or author response.

## Replay

    python3 -B -S frontiers/ts_small_kappa_20261006/replay.py
    python3 -B -O -S frontiers/ts_small_kappa_20261006/replay.py

`replay.py` uses the standard library only and takes a few seconds per mode. It is Math-#384's replay (itself Math-#360's planar packet replay, and that the QS `d = 3` packet's hardened replay), with this packet's paths, fingerprints and negative control. It runs four checks:
1. **Identities.** Every stored file has the identity pinned in `SOURCES.json`, and the tree holds nothing else.
2. **Extraction.** `TS/author_controls.py` and `TS/author_controls_stdout.json` equal the fenced payloads in the stored controls comment, under the rule it states (that of [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189)). The stdout is a ```` ```json ```` fence.
3. **The checker.** `ts_exact.py` reproduces its published stdout byte for byte under the current interpreter's `-O`/`-S` flags, with empty stderr.
   - Each of its 10 mutants and 3 invalid invocations reproduces its exact source-bound rejection: exit code, stdout and stderr fingerprints, with the intended group. An exit code alone does not pass.
   - The fingerprint table in `replay.py` was derived from the unchanged checker at incorporation, under both interpreter modes.
4. **Negative controls.**
   - A one-byte change to the stored note (`TS/PROOF.md`) is detected.
   - A checker with one changed constant (S3's `C₄ = 131` replaced by `130`) is rejected, failing exactly at `S3_constants`.

The workflow `.github/workflows/ts-small-kappa.yml` runs on Python 3.11.16. It runs the protocol and raw-evidence tests (`tests/test_ts_small_kappa_replay_protocol.py`, `tests/test_ts_small_kappa_replay_evidence.py`), then the replay in both modes, as two jobs. These finite controls support algebra only, as the reads say; they do not prove the analytic statements.
