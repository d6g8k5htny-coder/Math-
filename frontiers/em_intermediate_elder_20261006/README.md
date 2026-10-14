# Lifetime note EM: exact records and a replayable checker

Incorporated on 6 October 2026. **Scientific effect: NONE. No new mathematics and no status change.**

This packet stores lifetime note EM in the repository, byte for byte. The note was posted on [main#229](https://github.com/d6g8k5htny-coder/main/issues/229), with a delivery pointer on [main#259](https://github.com/d6g8k5htny-coder/main/issues/259) (IBA2-009). It holds:
- the frozen note and the author's claim and delivery pointer;
- the controls comment, and the control script `em_exact.py` with its stdout, extracted verbatim from it;
- the read request and summonses, every nonauthor pickup and verdict of record, the author's successor text for the one amendment, its readback, and the author's read-complete note.

Anthropic Claude, who is also the author of the note, incorporated it under claim [6024074852](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6024074852) (claim 1). This is custody only; no proof byte is changed. `SOURCES.json` pins every stored file (15 files, one control script) by byte count and SHA-256, and `replay.py` verifies all of it.

## Status and attribution

- **Author.** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`), for Dylan Roy (delegated AI work). The same session wrote note TS, [N] (#240), #187, #220, #229 and #237, which the note consumes; [182] and [R] are OpenAI's.
- **Reads.** Three slices and one readback, each read by a Cursor cloud agent running xAI Grok 4.7 (`grok-4.7-high-fast`; non-Claude, nonauthor), summoned one bounded task at a time under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035). Slices A and C passed; Slice B asked for one amendment, which was applied as successor text and read back PASS. Every read goes through the same GitHub account, so organizational independence is **0** for all of them. None is an owner reading.
- **Verdicts are scoped.** A PASS passes the slice as the note states it, conditional on the cited inputs, and discharges nothing.
- **Amendments of record.** One. The Slice B read [6023045290](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6023045290) found that one absorption in §4.1 (c), after (4.4), did not follow from the reason written: the weakened shift bound `|δτ| ≤ Γ̃/4 + ½` drops the factor `r`. The author applied the exact change in the successor text [6023434026](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6023434026) §2: the middle term uses the sharp shift `|δτ| ≤ (2𝒩̄r/λ)(Γ̃/4 + 5/12)`, so `3𝒩̄|δτ| ≤ ((3/2)√C_Γ + 5/2)𝒩̄^{5/2}rλ^{−3/2}`. Its readback is PASS ([6023435335](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6023435335)). No constant, exponent or stated bound changes, and the stored note body is the frozen one.
- **Author-side referee.** Before posting, three clean-context referee passes in the same session read the note in three slices. They are not review evidence; their reports are kept in the project archive.
- **Conditionality.** Every statement is conditional on the consumed sources at their stated scopes:
  - note TS ([6020794123](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6020794123), with its successor text [6021299833](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6021299833); read in every slice; its custody packet is Math-#387);
  - [N] (#240), #220, [R], [182], #229, #237 and #187.

  The note's header lists their blobs.
- **What governs.** The note's own statement, hypotheses and "not claimed" section govern, read with the successor text. The summary below paraphrases them.
- **Not edited here.** No other packet, no `PROOF_INDEX.md`, STATUS, register or graph.

| Slice | Scope | Verdict (reader) |
|---|---|---|
| A | §§1–2: Lemma P and Lemma X; controls E1, E2, E4 with M1–M3, M5, M6, M11 | PASS (Cursor `bc-68aae9d7…`, [6023042554](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6023042554)) |
| B | §§3–4: Lemma V and the proof of Lemma S‴; E3, E5, E7 with M4, M9, M10 | AMEND, one absorption in §4.1 (c) (Cursor `bc-2e83c5a5…`, [6023045290](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6023045290)) |
| C | §0, §§5–6 and the header: the statements, Corollary EM with its ledger, the remarks; E6 with M7, M8 | PASS (Cursor `bc-16115a6c…`, [6023050789](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6023050789)) |
| readback | the successor text [6023434026](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6023434026) §2 against the AMEND | PASS (Cursor `bc-3f10fc96…`, [6023435335](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6023435335)) |

## What the note states (paraphrase; the note governs)

The setting is note TS's (§0), with its §1 constant `C₀` and `𝒩̄ = C₀𝒩`. `e` is the elder mark, `W_r` the typed weight, `𝐓_r^{eld}` the elder kernel integrated over the birth height, and `κ = k/r`.
- **Lemma P (third-order pin relations at `M`).** The pins fix the third derivatives at `0` and `M` up to explicit errors: `|∂_u³f(0) − 12k| ≤ (3/80)𝒩̄r²`, `|r^{−1}∂_u³f(M) − 12κ + f₄/2| ≤ (13/80)𝒩̄r` and `|β̃ + γ/2| ≤ (5/12)𝒩̄r`, and the transverse blocks at `M` and `S` are within `½𝒩̄r` of `A`. So the window function differs from [N]'s cusp polynomial by third derivatives `O(𝒩̄r)` at `M̂`.
- **Lemma X (the sheared box).** A deterministic barrier in window coordinates sheared by the exact Schur direction at `M̂`. Under its hypotheses (`r|τ| ≤ 1`, an embedding condition, and two lower bounds on the transverse curvature `μ`), if the soft curvature `s` is at least the explicit threshold (X.0), then the death level of `M` falls below `f(S)` and the pair is not elder (`e = 0`). The faces across the shear need only `μ`.
- **Lemma V (small balls in `Sym(d)`).** For a nondegenerate Gaussian symmetric matrix, a transverse eigenvalue below `t` costs `t^{3/2}`, and `t^{1/2}` beside a soft eigenvalue below `ε` ((V.1)–(V.3)).
- **Lemma S‴ (the elder weight on `κ ≤ r`).** For `0 < k ≤ r²`, `E_Q[(W_r/r²)e] ≤ Cr²[rκ + r^{7/3}κ^{2/3}log(2/r) + min(r^{7/2}, r^{3/2}κ^{2/3})]P^N`, and `𝐓_r^{eld}` is bounded by the bracket. On the good event (`A < 0`, `λ_min(−A) ≥ C_G𝒩r`) the proof uses Lemma X with [N]'s Lemma Q′; off it (the bad region), note TS's barrier with Lemma V.
- **Corollary EM.**
  - `ν_eld(ℓ) = cℓ^{−1/3} + c₁ℓ^{1/4} + c₂ℓ^{1/3} + O(ℓ^{9/14})`, and `ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + O(ℓ^{3/5})`.
  - For SIDE24 the relative remainder is `O(ℓ^{41/42})`, against note TS's `O(ℓ^{19/21}log(1/ℓ))`.
  - In note TS's decomposition at `ρ = ℓ^{3/14}`, three ledger rows sit at `9/14`; two belong to the decomposition, and the third is Lemma S‴'s bad region (Remark 1).

## What the note does not establish

From the note's "not claimed" section:
- no sharpness of `9/14`, and none of any term of Lemma S‴;
- nothing pointwise in `b`, and no identification of further terms of either density;
- no certified numerical value, and no uniformity in `d` or `L`;
- whether IBA2-009 closes, which is for the audit's owners.

## Not included

- **The consumed sources** (note TS, [N], #220, [R], [182], #229, #237, #187). The packets are on `main` at their own paths; note TS's custody packet is Math-#387.
- **Addendum EM.1** ([6024077582](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6024077582)), which treats the bad region through Lemma X and is under its own reads. It changes no statement of note EM.
- **The clean-context referee reports** and the exploration script `smallball.py` behind Remark 4 (same provider and session; not review evidence). They are kept in the project archive.
- **Coordination comments** that record no pickup, verdict or author response.

## Replay

    python3 -B -S frontiers/em_intermediate_elder_20261006/replay.py
    python3 -B -O -S frontiers/em_intermediate_elder_20261006/replay.py

`replay.py` uses the standard library only and takes a few seconds per mode. It is Math-#387's replay (itself Math-#384's, Math-#360's planar packet replay, and that the QS `d = 3` packet's hardened replay), with this packet's paths, fingerprints and negative control. It runs four checks:
1. **Identities.** Every stored file has the identity pinned in `SOURCES.json`, and the tree holds nothing else.
2. **Extraction.** `EM/author_controls.py` and `EM/author_controls_stdout.json` equal the fenced payloads in the stored controls comment, under the rule it states (that of [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189)). The stdout is a ```` ```json ```` fence.
3. **The checker.** `em_exact.py` reproduces its published stdout byte for byte under the current interpreter's `-O`/`-S` flags, with empty stderr.
   - Each of its 11 mutants and 3 invalid invocations reproduces its exact source-bound rejection: exit code, stdout and stderr fingerprints, with the intended group. An exit code alone does not pass.
   - The fingerprint table in `replay.py` was derived from the unchanged checker at incorporation, under both interpreter modes.
4. **Negative controls.**
   - A one-byte change to the stored note (`EM/PROOF.md`) is detected.
   - A checker with one changed constant ((P.2)'s `13/80` replaced by `1/20`) is rejected, failing exactly at `E1_pins`.

The workflow `.github/workflows/em-intermediate-elder.yml` runs on Python 3.11.16. It runs the protocol and raw-evidence tests (`tests/test_em_intermediate_elder_replay_protocol.py`, `tests/test_em_intermediate_elder_replay_evidence.py`), then the replay in both modes, as two jobs. These finite controls support algebra only, as the reads say; they do not prove the analytic statements.
