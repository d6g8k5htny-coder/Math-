# Lifetime note TL: exact records and a replayable checker

Incorporated on 6 October 2026. **Scientific effect: NONE. No new mathematics and no status change.**

This packet stores lifetime note TL in the repository, byte for byte. The note was posted on [main#229](https://github.com/d6g8k5htny-coder/main/issues/229), with a pickup and a delivery pointer on [main#259](https://github.com/d6g8k5htny-coder/main/issues/259) (IBA2-009). It holds:
- the frozen note and the author's claim, pickup and delivery pointer;
- the controls comment, and the control script `tl_exact.py` with its stdout, extracted verbatim from it;
- the read requests and summonses, every nonauthor pickup and verdict of record, and the author's round note.

Anthropic Claude, who is also the author of the note, incorporated it under claim [6019049654](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6019049654). This is custody only; no proof byte is changed. `SOURCES.json` pins every stored file (14 files, one control script) by byte count and SHA-256, and `replay.py` verifies all of it.

## Status and attribution

- **Author.** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`), for Dylan Roy (delegated AI work). The author also wrote [K], [N] (#240), #237 and #242–#244, which the note consumes.
- **Reads.** Three slices, each read by a Cursor cloud agent running xAI Grok 4.7 (`grok-4.7-high-fast`; non-Claude, nonauthor), summoned one bounded task at a time under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035): Slices A–B, C and D, all PASS. Every read goes through the same GitHub account, so organizational independence is **0** for all of them. None is an owner reading.
- **Verdicts are scoped.** A PASS passes the slice as the note states it, conditional on the cited inputs, and discharges nothing.
- **Amendments of record.** None. No reader requested a change; the author's round note [6019049654](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6019049654) records that the note and the controls stay frozen as posted.
- **Author-side referee.** Before posting, three clean-context referee passes in the same session read the note in three slices. They are not review evidence; their reports are kept in the project archive.
- **Conditionality.** Every statement is conditional on the consumed packets at their stated scopes: [N] (#240), #237, #242, #220, #229, #218, [K] (K2) with its erratum, [R] (R5) and Math-#296, and #187 for the last form of TL3. The note's header lists their blobs.
- **What governs.** The note's own statement, hypotheses and "not claimed" section govern. The summary below paraphrases them.
- **Not edited here.** No other packet, no `PROOF_INDEX.md`, STATUS, register or graph.

| Slice | Scope | Verdict (reader) |
|---|---|---|
| A–B | §§0–2: the setting, the window lemmas W₁ and W₂, Lemma GE, Proposition RW; controls T1, T5 | PASS (Cursor `bc-df5cfd1f…`, [6018510549](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6018510549)) |
| C | §3: Lemma Δ (Parts R and F) and what Steps 3–4 use; controls T2, T3, T4, T7 | PASS (Cursor `bc-d851d2ca…`, [6018013576](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6018013576)) |
| D | §§4–7 and the header: Steps 1–6, the bounds of §5, Corollaries TL1–TL3 and the Math-#296 tail, the ledger, the remarks; control T6 | PASS (Cursor `bc-b84a2c6b…`, [6018770333](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6018770333)) |

## What the note states (paraphrase; the note governs)

The setting is [N]'s cusp problem on the torus, birth-integrated as in #237. `𝐓_r^{rej}(k, u)` is the rejected kernel integrated over the birth height, and `𝓐^{rej}(κ, u)` is its cusp limit (#242), with `κ = k/r`.
- **Theorem TL.** In every `d ≥ 2`, `|𝐓_r^{rej}(k, u) − 𝓐^{rej}(κ, u)| ≤ Cr²(1 + κ)` for `0 < r ≤ r₀`, `κ ≥ 1` and `k = κr ≤ 1`. Relative to the size `1/κ` of the kernel, this is an error `O(k²)`. It is (TL_a) of main#259 6001580409 with `a = 2`.
- **The proof.**
  - [N]'s pathwise decision lemmas are used on a `κ`-normalized good event (Lemma GE). This gives Proposition RW, the rejected weight up to `O(r²(1 + κ))`.
  - Two window lemmas, uniform in `κ`, bound the weighted mass of the rejected window (`C/κ`) and of thin slabs at its edges.
  - Birth integration makes the parity exact.
  - The edge shift is expanded along the radial direction of `γ` (Lemma Δ: first difference `O(r)`, second `O(r²(1 + κ))`).
- **Corollary TL1.** The separations with `κ ≥ 1` contribute `ℓ^{1/4}∫_0^1∫𝓐^{rej}(s^{−4}, u) dσ ds + O(ℓ^{2/3})` to `ρ_rej`. Math-#296's tail condition (4.2) therefore holds at `κ → ∞` (TAIL-L).
- **Corollary TL2.** `J_ℓ(y) = F̄₀ + O(ℓ^{1/5})` uniformly on compact `y`-bands. Math-#296's moving band therefore carries only the cusp kernel's own share.
- **Corollary TL3.** `ν_eld(ℓ) = cℓ^{−1/3} + c₁ℓ^{1/4} + c₂ℓ^{1/3} + ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{4/9}log(1/ℓ))`, and `ρ_rej` likewise, against #229's `ℓ^{3/7}`. For SIDE24 the relative remainder is `O(ℓ^{7/9}log(1/ℓ))`, against `ℓ^{16/21}`. Three terms attain `4/9`.

## What the note does not establish

From the note's "not claimed" section:
- the `κ → 0` side (TAIL-S): **IBA2-009 stays OPEN**;
- nothing about an `ℓ^{1/2}` term of the whole elder or rejected density (`4/9 < 1/2`);
- nothing pointwise in `b`, and no identification of the `k²/κ` term;
- no certified numerical value, and no uniformity in `d` or `L`.

## Not included

- **The consumed packets** ([N], #237, #242, #220, #229, #218, [K], #187, Math-#296); they are on `main` at their own paths.
- **The clean-context referee reports** and their exploration scripts (same provider and session; not review evidence). They are kept in the project archive.
- **Coordination comments** that record no pickup, verdict or author response.

## Replay

    python3 -B -S frontiers/tl_soft_layer_20261006/replay.py
    python3 -B -O -S frontiers/tl_soft_layer_20261006/replay.py

`replay.py` uses the standard library only and takes a few seconds per mode. It is Math-#360's planar packet replay, itself the QS `d = 3` packet's hardened replay, with this packet's paths, fingerprints and negative control. It runs four checks:
1. **Identities.** Every stored file has the identity pinned in `SOURCES.json`, and the tree holds nothing else.
2. **Extraction.** `TL/author_controls.py` and `TL/author_controls_stdout.json` equal the fenced payloads in the stored controls comment, under the rule it states (that of [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189)). The stdout is a ```` ```json ```` fence.
3. **The checker.** `tl_exact.py` reproduces its published stdout byte for byte under the current interpreter's `-O`/`-S` flags, with empty stderr. Each of its 10 mutants and 3 invalid invocations reproduces its exact source-bound rejection (exit code, stdout and stderr fingerprints with the intended group), not merely an exit code. The fingerprint table in `replay.py` was derived from the unchanged checker at incorporation, under both interpreter modes.
4. **Negative controls.** A one-byte change to the stored note (`TL/PROOF.md`) is detected. A checker with one changed constant (T4's window tail constant `11` replaced by `9`) is rejected, failing exactly at `T4_constants`.

The workflow `.github/workflows/tl-soft-layer.yml` runs the protocol and raw-evidence tests (`tests/test_tl_soft_layer_replay_protocol.py`, `tests/test_tl_soft_layer_replay_evidence.py`) and then both modes, as two jobs, on Python 3.11.16. These finite controls support algebra only, as the reads say; they do not prove the analytic statements.
