# Lifetime note C7: exact records and a replayable checker

Incorporated on 7 October 2026. **Scientific effect: NONE. No new mathematics and no status change.**

This packet stores lifetime note C7, the elder density's `ℓ^{2/3}` term and #242's Conjecture 7 in its `o(ℓ^{2/3})` form, in the repository, byte for byte. It was posted on [main#229](https://github.com/d6g8k5htny-coder/main/issues/229) and read there in every slice. The directory `C7/` holds:
- the claim and the frozen note;
- the controls comment, with the control script and its stdout extracted verbatim from it;
- the read request and the two other summonses;
- the three nonauthor verdicts of record;
- the author's read-complete note.

Anthropic Claude, who is also the author of note C7, incorporated it under claim [6030235472](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6030235472). This is custody only; no proof byte is changed. `SOURCES.json` pins every stored file (12 files, one control script) by byte count and SHA-256, and `replay.py` verifies all of it.

## Status and attribution

- **Author.** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`), for Dylan Roy (delegated AI work).
  - The same session wrote the consumed notes TS, EM, EM.1, LU, C3 and SL, and the consumed packets #187, #188, #220, #229, #240 and #242.
  - [R], [P] and [182], which those packets consume, are OpenAI's.
- **Reads.** Each read is by a Cursor cloud agent running xAI Grok 4.7 (`grok-4.7-high-fast`; non-Claude, nonauthor), summoned one bounded task at a time under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035).
  - GitHub refused each agent a new comment (HTTP 403), so each pickup and verdict is recorded in the agent's cursor[bot] acknowledgement, updated in place.
  - Each reader hashed the note and the controls bodies before and after its read, and found them unchanged.
  - Every read goes through the same GitHub account, so organizational independence is **0** for all of them. None is an owner reading.
- **Verdicts are scoped.** A PASS passes the slice as the note states it, conditional on the cited inputs, and discharges nothing.
- **Amendments of record.** None. All three slices are PASS with no required change.
- **Author-side referees.** Before posting, three clean-context referee passes in the same session read the draft, one per slice. They are not review evidence. The note's header records them, the controls comment lists their findings, and the reports are kept in the project archive.
- **Conditionality.** Every statement is conditional on the consumed sources at their stated scopes, which the note's header lists with blobs. Among them are:
  - note EM (custody packet Math-#388);
  - addendum EM.1 and notes LU, C3 and SL (Math-#390);
  - note TS (Math-#387).
- **What governs.** The note's own statements, hypotheses and "not claimed" section govern. The summary below paraphrases them.
- **Not edited here.** No other packet, no `PROOF_INDEX.md`, STATUS, register or graph.

| Slice | Scope | Verdict (reader) |
|---|---|---|
| A | §§0–2: the statements, the proof of Theorem E, the proof of Corollary E1; K1–K3 and K7's `σ = 5/24` part, with M1–M3 | PASS (Cursor `bc-dddeb178…`, [6030070803](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6030070803)) |
| B | §§3–4: Lemma D, Lemma D′, Proposition G₀; K4–K6 with M4, M5, M6, M8 | PASS (Cursor `bc-ee21e46f…`, [6030077684](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6030077684)) |
| C | §§5–6 and the header: the proof of Theorem C7, Remarks 1–6, the header for overclaim; K7 with M7, and the invalid invocations | PASS (Cursor `bc-70175f37…`, [6030083350](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6030083350)) |

## What the note states (paraphrase; the note governs)

The setting is that of note EM and note TS. Here `κ = k/r` and the lifetime is `ℓ = kr³`. `𝐓_r` and `𝐓_r^{eld}` are the candidate and elder kernels integrated over the birth height.
- **Theorem E.** On `κ ≤ r`, `0 ≤ 𝐓_r^{eld}(k, u) ≤ C[Υ(r, κ) + r²κ^{2/3}]`, where `Υ(r, κ) := min(rκ, r³(1 + log₊(κ/r²)))`.
  - The new input is one line of note EM's §4.1: on typed pairs in EM's good event, the soft curvature `s` is capped by typedness (`s < s + s_S ≤ 12κ + 2ε̃`), not only by EM's Lemma X.
- **Corollary E1.** The intermediate elder mass on `[ℓ^{1/5}, r_0^*]` is `O(ℓ^{2/3})`. So `ν_eld` and `ρ_rej` have remainder `O(ℓ^{2/3})`, and SIDE24's relative remainder is `O(ℓ)`. Note LU had a factor `log(1/ℓ)` in both.
- **Lemmas D and D′.** On [N]'s window, an elder pair keeps the window ridge between the heights of `S` and `M`, on all of `[−½, ½]` or on all of `[−3, −½]`.
  - Lemma D is deterministic. It assumes that no other critical point sits at the height of `S`.
  - Lemma D′ shows that this holds almost surely.
- **Proposition G₀.** `r^{−3}𝐓_r^{eld}(cr³, u) → 0` for every `c > 0`, uniformly in `u`. This is the one scale at which Theorem E's bound is of order `r³`.
- **Theorem C7.** In every `d ≥ 2` and for every `L`:
  - `ν_eld = cℓ^{−1/3} + c₁ℓ^{1/4} + c₂ℓ^{1/3} + (c₃ − R_{2/3})ℓ^{2/3} + ν_eld^{far,r_0^*} + o(ℓ^{2/3})` (C7.1);
  - `ρ_rej + ν_eld^{far,r_0^*} = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + R_{2/3}ℓ^{2/3} + o(ℓ^{2/3})` (C7.2);
  - here `c₃` is note C3's and `R_{2/3}` is note SL's. (C7.2) is #242's Conjecture 7 with `o(ℓ^{2/3})` in place of `O(ℓ^{3/4})`, and with SL's `R_{2/3}`, which has the `b`-integral inside;
  - with #188's Theorem G, the far terms are `O(ℓ^N)` (C7.3). For SIDE24 this gives `ν_{3,24}(ℓ) = cℓ^{−1/3}(1 + (c₁/c)ℓ^{7/12} + (c₂/c)ℓ^{2/3} + ((c₃ − R_{2/3})/c)ℓ + o(ℓ))`.

## What the note does not establish

From its "not claimed" section:
- no rate: the remainder of (C7.1)–(C7.2) is `o(ℓ^{2/3})`, and #242's `O(ℓ^{3/4})` form of Conjecture 7 stays open;
- no value and no sign of `c₃ − R_{2/3}` for the torus field, in particular nothing at `L = 24`. The model values (`≈ 0.062` in `d = 2`, `≈ 0.077` in `d = 3`) are exploration;
- nothing pointwise in `b`, no certified number, and no uniformity in `d` or `L`;
- no change to any statement of the consumed notes and packets: Corollary E1 replaces note LU's remainders only. Whether IBA2-009 closes is for the audit's owners.

## Not included

- **The consumed sources.** The packets are on `main` at their own paths (`SOURCES.json`, `related_packets`). The custody packets of the consumed notes are:
  - Math-#390 for EM.1, LU, C3 and SL;
  - Math-#388 for note EM;
  - Math-#387 for note TS.
- **The clean-context referee reports** (same provider and session; not review evidence). They are kept in the project archive.
- **Coordination.** `C7/CLAIM.md` and `C7/AUTHOR_READ_COMPLETE_AND_PACKET_CLAIM.md` also carry an integration request and an integration update for this lane's earlier custody packets. That coordination is not part of the object. Other coordination comments that record no pickup, verdict or author response are not stored.

## Replay

    python3 -B -S frontiers/c7_elder_two_thirds_20261007/replay.py
    python3 -B -O -S frontiers/c7_elder_two_thirds_20261007/replay.py

`replay.py` uses the standard library only and takes about fifteen seconds per mode. It is Math-#390's replay (itself the hardened replay of #388, #387, #384, #360 and the QS `d = 3` packet), with this packet's paths, fingerprints and negative control. It runs four checks:
1. **Identities.** Every stored file has the identity pinned in `SOURCES.json`, and the tree holds nothing else.
2. **Extraction.** `C7/author_controls.py` and `C7/author_controls_stdout.json` equal the fenced payload in the stored controls comment, under the rule that comment states (that of [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189)). The stdout is a ```` ```json ```` fence.
3. **The checker.** `c7_exact.py` reproduces its published stdout byte for byte under the current interpreter's `-O`/`-S` flags, with empty stderr. That stdout reports 38,937 checks in seven groups, K1–K7.
   - Each of its 8 mutants and 5 invalid invocations reproduces its exact source-bound rejection: exit code, stdout and stderr fingerprints, with the intended group or the usage line. An exit code alone does not pass.
   - The fingerprint table in `replay.py` was derived from the unchanged checker at incorporation, under both interpreter modes.
4. **Negative controls.**
   - A one-byte change to the stored note (`C7/PROOF.md`) is detected.
   - A checker with one changed constant is rejected, failing exactly at `K5_window`. The constant is `c7_exact.py`'s `384`, the coefficient of Lemma R₂'s window at `X = 0`, replaced by `192`.

The workflow `.github/workflows/lifetime-c7-elder.yml` runs on Python 3.11.16, in two jobs, one per mode. Each job runs the protocol and raw-evidence tests (`tests/test_lifetime_c7_elder_replay_protocol.py`, `tests/test_lifetime_c7_elder_replay_evidence.py`), then the replay. These finite controls support algebra and a discrete model of Lemma D only, as the reads say; they do not prove the analytic statements.
