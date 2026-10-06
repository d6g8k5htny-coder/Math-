# The planar compact-`K` chain (Corollary PD, QS addenda A4.1–A4.3): exact records and a replayable checker

Incorporated on 6 October 2026. **Scientific effect: NONE. No new mathematics and no status change.**

This packet stores four reviewed objects in the repository, byte for byte, all posted on [main#229](https://github.com/d6g8k5htny-coder/main/issues/229):
- Corollary PD (the planar compact-window rejected-candidate lifetime density with a rate);
- QS addendum A4.1 (A4's planar rate made uniform over a compact gap interval `K`);
- QS addendum A4.2 (C124's planar endpoint rate made uniform over `K`, with Corollary PD at the endpoint);
- QS addendum A4.3 (the planar decision on dyadic windows at compact `K`).

For each object it holds:
- the frozen note and the author's claim;
- every nonauthor pickup and verdict of record, the erratum, the support note that preceded A4.1, the delivery notes and the author responses;
- the control script and its stdout, extracted verbatim from the stored controls comment. Corollary PD's ledger is extracted from the note itself, which publishes it in its §4.

Anthropic Claude, who is also the author of the four objects, incorporated them under claim [6014798862](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6014798862). This is custody only; no proof byte is changed. `SOURCES.json` pins every stored file (45 files, 4 control scripts) by byte count and SHA-256, and `replay.py` verifies all of it.

## Status and attribution

- **Author.** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`), for Dylan Roy (delegated AI work).
- **Reads.** Each object has bounded nonauthor reads, listed in the table:
  - OpenAI Codex read Corollary PD, A4.1 and A4.2's slice D.
  - Grok Bot agents 15, 1 and 11 (non-Claude, nonauthor; provider undisclosed in their own pickups) read A4.2's slices A–C.
  - Two Cursor cloud agents running xAI Grok 4.7 (`grok-4.7-high-fast`) read A4.3, summoned one bounded task at a time under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035).
  - Every read goes through the same GitHub account, so organizational independence is **0** for all of them. None is an owner reading.
- **Verdicts are scoped.** PASS_SCOPED, PASS_SCOPED_COMPOSITION and "PASS (scoped, conditional)" pass the slice as the note states it, conditional on the cited inputs, and discharge nothing.
- **Amendments of record.** There were none:
  - A4.1's erratum E1 is author-side, and the review read A4.1 together with E1;
  - PD's clarification C-PD-1 was accepted by the author;
  - A4.2's slice C raised three optional wording items.
- **Conditionality.** Every statement is conditional on the planar chain it builds on, at that chain's reviewed scope:
  - C101, C102, C103 and C124 are in `frontiers/planar_soft_layer_chain_20261003/`;
  - A4 is in `frontiers/planar_rejected_endpoint_margin_20261003/`;
  - A4.3 also uses A3.11's shell bookkeeping (in `frontiers/qs_d3_soft_layer_chain_20261005/` once Math-#359 lands).
  `SOURCES.json` records this per object.
- **What governs.** Each note's own statement, hypotheses, "not claimed" section and erratum govern. The summaries below paraphrase them.
- **Not edited here.** No other packet (the A4 packet keeps its historical "not included" entry for A4.1), no `PROOF_INDEX.md`, STATUS, register or graph.

| Object | Note | Reads of record (verdict; reader) | Amendment record |
|---|---|---|---|
| PD | [5973476391](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973476391) (ledger in its §4) | steps 1–4 and their source interfaces: PASS_SCOPED_COMPOSITION (OpenAI Codex, [5973563650](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973563650)) | clarification C-PD-1, accepted ([5973590979](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973590979)) |
| A4.1 | [5973261552](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973261552), controls [5973265245](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973265245) | A4.1 with E1: PASS_SCOPED (OpenAI Codex, [5973672811](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973672811)) | erratum E1 [5973478388](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973478388); author acknowledgment [5974025302](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5974025302), no amendment |
| A4.2 | [5974565257](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5974565257), controls [5974567585](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5974567585) | A (JB_K, DB_K) PASS (Grok Bot agent 15, [5975798694](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5975798694)); B (ES_K, FT_K) PASS (agent 1, [5975812240](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5975812240)); C (Theorem ER_K) PASS (agent 11, [5976045296](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5976045296)); D (Corollary PD_ER) PASS_SCOPED (OpenAI Codex, [5975703487](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5975703487)) — all scoped, conditional | none required (three optional wording items in C) |
| A4.3 | [6010510789](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6010510789), controls [6010511425](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6010511425) | Slice 1 PASS (Cursor `bc-ac3b4ec5…`, [6010522535](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6010522535)); Slice 2 PASS (Cursor `bc-896b2b0f…`, [6011056566](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6011056566)) | none required; author round note [6011224732](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6011224732) |

## What the chain states (paraphrase; the notes govern)

The setting is the planar pinned-pair problem of C101–C103 on the torus: two pins at heights `b` and `b − kr³` with zero gradients, the regression law, the typed weight and its tilted law `Q_r^W`, the soft layer `D_Λ`, the elder event `H_r`, the selection probability `p_r`, the failure measure `ν_r^F`, and CUB's coefficients `α₁ + α₂`; `K = [k₋, k₊] ⊂ (0, ∞)` is a compact gap interval.

- **Corollary PD.** On a compact window `B × K` of births and gaps, the rejected-candidate (nonselected) lifetime density is `ν_rej(ℓ) = C_fail ℓ^{2/3} + O(ℓ^{3/4})`. It comes with the candidate density `c_cand ℓ^{−1/3} + O(1)`, the cumulative count `(3/5)C_fail t^{5/3} + O(t^{7/4})`, the `q`-moments for `q > −5/3`, and the nonselected fraction `(C_fail/c_cand)ℓ + O(ℓ^{13/12})`. Its (v) gives exponents `ℓ^{(2+β)/3}` for every `β < 2/3`, conditional on A4.1. The proof composes C103's rate with [P] §§10–12's radial ledger along #175 §7's identity.
- **A4.1.** A4's sharper planar rate, made uniform over compact `K`, in C103's setting. Lemma LE_K and Corollary LE_K are A4's local endpoint margin at gap `k`; Lemmas B′_K and Band_K follow. Theorem QFE′_K: for every `β < 2/3`, `‖ν_r^F − ν_0^F‖_var ≤ C_{K,β}r^β` and `1 − p_r = r³(α₁ + α₂) + O_{K,β}(r^{3+β})`, uniformly over `b`, `k ∈ K` and frames. Corollary SE_K: on a fixed layer the sector errors are `O(r^{11/3−ε})`. Erratum E1 corrects two remarks: C102 §8's premise is one event theorem, which C103 supplies.
- **A4.2.** C124's Lemmas JB, DB, ES and FT are re-proved on C103's interfaces. Theorem ER_K is the endpoint at compact `K`: `‖ν_r^F − ν_0^F‖_var ≤ C_K r^{2/3}log(1/r)^{8/3}` and `1 − p_r = r³(α₁ + α₂) + O_K(r^{11/3}log(1/r)^{8/3})`, with fixed-layer errors `C_{K,Λ}r^{11/3}`. Corollary PD_ER gives `ν_rej(ℓ) = C_fail ℓ^{2/3} + O(ℓ^{8/9}log(1/ℓ)^{8/3})`, with the cumulative, moment (`q`-uniform constant `3073C`) and fraction forms.
- **A4.3.** A3.11's dyadic-window decision, transported to C103's chain:
  - the layer is cut into dyadic shells of the raw radii, each read on its own deterministic window;
  - each shell's bands are paid by A3.11's localized level-band bound through C103's fibre identity;
  - the margins and A4.1's endpoint strip are summed over the `O(log(1/r))` shells.

  Results:
  - Theorem SE″_K: fixed-layer errors `C_{K,Λ}r⁴log(1/r)`.
  - Theorem QFE″_K: `‖ν_r^F − ν_0^F‖_var ≤ C_{K,β}r^β` for every `β < 1`.
  - Theorem ER′_K: `1 − p_r = r³(α₁ + α₂) + O_K(r⁴log(1/r)⁴)`.
  - Corollary PD_ER′: `ν_rej(ℓ) = C_fail ℓ^{2/3} + O(ℓ log(1/ℓ)⁴)`.
  - Remark 4: the `k = 1` constants.

## What the chain does not establish

From the notes' own "not claimed" sections:
- no `k₋ → 0` (no small-gap or unrestricted-mark rate), no growing `K` or `L`, and nothing in `d ≥ 3` (the `d = 3` chain is the QS packet);
- no removal of the logarithms, no exponent above `1` in `r`, and no sharpness;
- no statement about replacement bars, once-counted bars or real-valued mark total variation;
- no change to C101–C103, C124, A4 or any reviewed statement. Each note is additive; A4.3 supersedes the earlier rates only where it is cited.

## Not included

- **A4**, stored in `frontiers/planar_rejected_endpoint_margin_20261003/`, and **C91–C103, C124, C127**, stored in `frontiers/planar_soft_layer_chain_20261003/`.
- **The clean-context referee reports** and the exploration scripts (same provider, same session; not review evidence). They are kept in the project archive.
- **`a41_numeric.py`**, the 50-digit mpmath exploration inside A4.1's controls comment. It is stored there verbatim but not extracted or replayed, since it is not standard-library code.
- **Chief-of-Staff routing, roll-ups and acknowledgments.** Each pickup and verdict of record is stored.

## Replay

    python3 -B -S frontiers/planar_compact_k_chain_20261006/replay.py
    python3 -B -O -S frontiers/planar_compact_k_chain_20261006/replay.py

`replay.py` uses the standard library only and takes under a minute per mode (A4.1's script about 4 s per run, A4.2's about 1.5 s, the others under 0.1 s). It is the QS `d = 3` packet's replay (`frontiers/qs_d3_soft_layer_chain_20261005/replay.py`, in Math-#359's version) with this packet's paths, fingerprints and negative control. It runs four checks:
1. **Identities.** Every stored file has the identity pinned in `SOURCES.json`, and the tree holds nothing else.
2. **Extraction.** Each control script and its stdout equal the fenced payloads in the stored source comment, under the rule each controls comment states (that of [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189)). The fence language follows the stored stdout's suffix: ```` ```text ```` for PD, A4.1 and A4.2, and ```` ```json ```` for A4.3.
3. **The checkers.** All four scripts reproduce their published stdout byte for byte under the current interpreter's `-O`/`-S` flags, with empty stderr: `pd_ledger.py` (PD; stored as `PD/ledger_control.py`), `a41_exact.py`, `a42_exact.py` and `a43_exact.py`. Each of their 25 mutant invocations and 9 invalid invocations reproduces its exact source-bound rejection (exit code, stdout and stderr fingerprints with the intended reason), not merely an exit code. The fingerprint table in `replay.py` was derived from the unchanged checkers at incorporation, under both interpreter modes.
4. **Negative controls.** A one-byte change to a stored note (`A4_3/PROOF.md`) is detected. A checker with one changed constant (A4.3's Lemma 1.1 constant `192` replaced by `96`) is rejected, failing exactly at `Z1_lemma11_constants`.

The workflow `.github/workflows/planar-compact-k-chain.yml` runs the protocol and raw-evidence tests (`tests/test_planar_compact_k_replay_protocol.py`, `tests/test_planar_compact_k_replay_evidence.py`) and then both modes, as two jobs, on Python 3.11.16. These finite controls support algebra only, as the reads say; they do not prove the analytic statements.
