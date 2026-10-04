# Planar rejected-endpoint margin (QS addendum A4): exact records and a replayable checker

Incorporated on 3 October 2026; reader status updated the same day after the incorporation reviews (section "Status and attribution"). **Scientific effect: NONE. No new mathematics and no status change.**

This packet stores one reviewed object in the repository, byte for byte: QS addendum A4, posted on [main#229](https://github.com/d6g8k5htny-coder/main/issues/229) as comment [5972396791](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5972396791). It holds:
- the frozen proof and the author's claim;
- the full nonauthor review C117, with its pickup, its exposure correction and its completion note;
- the author's acknowledgment of that review;
- the author controls comment, with the checker and its stdout extracted verbatim.

Anthropic Claude, who is also A4's author, incorporated it under claim [5973297507](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973297507). This is custody only; no proof byte is changed. The C119 notice [5972971500](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5972971500) released the sequencing after Math-#249 merged.

## Status and attribution

- **Author.** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`), for Dylan Roy (delegated AI work).
- **Review.** C117: OpenAI/Codex `/root/next_math_triage`, a nonauthor of A4. Its verdict is ACCEPT / PASS_TECHNICAL_SCOPED, conditional on the retained source interfaces, with no required amendment. Its exposure to the author's checker before its own control design is disclosed in `A4/REVIEW_EXPOSURE_CORRECTION.md`.
- **Independence.** The review is provider-distinct but goes through the same account, so organizational independence is **0**.
- **Owner review.** Dylan Roy's owner workflow clarification, recorded in [5973603003](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973603003), reports ongoing review and removes generic external-human and personal-reading waits. It is not a retroactive exact-source verdict.
- **Incorporation reviews of head `5217c22`.**
  - Same-provider custody and reproducibility read: Anthropic Claude, session `017Mi3hx…`, [5973577038](https://github.com/d6g8k5htny-coder/Math-/pull/256#issuecomment-5973577038). PASS, with provider-distinct and organizational credit 0. Its wording note N2 is applied below. Its optional hardening note N1 (stricter mutant checks in `replay.py`) is deferred, because it would change executable bytes.
  - Provider-distinct incorporation audit C123: OpenAI/Codex `/root/next_math_triage`, [review 5402884161](https://github.com/d6g8k5htny-coder/Math-/pull/256#pullrequestreview-5402884161) and completion [5973925620](https://github.com/d6g8k5htny-coder/Math-/pull/256#issuecomment-5973925620). PASS for source custody, interface compatibility and the hosted checks. It asked for this reader-status update.
- **Historical fields.** `SOURCES.json` records the incorporation snapshot at head `5217c22`. Its `excluded.A4.1` and `objects[0].personal_reading` fields are historical, not present-day gates; this README carries the current status.
- **What governs.** The proof's own statement, hypotheses and limits govern. The summary below paraphrases them.
- **Not edited here.** No other packet, `PROOF_INDEX.md`, STATUS, register or graph.

## What A4 states (paraphrase; see `A4/PROOF.md`, and `A4/CLAIM.md` item 2 for the comparison with `O(r^{7/2})`)

- **Lemma LE.** The exact pins make the Taylor error vanish to second order at `raw M` along the raw chord `K_raw` (§1(i)); evaluated at the doubled endpoint, it is at most `4K₂Nrw²·|v|²`. Also `4h ≥ 2·min(1, a_M/(γ² + 72))·|v|²`, and the constant is attained. So the endpoint certificate needs only `a_M` against `η_LE = 2K₂ r w²`, not C97's `h ≥ c_h a_M³/Pjet⁶`.
- **Fixed soft layer `Λ`.** The rejected and elder sector errors are `O(r^{11/3−ε})` for every `ε > 0`. This improves the `O(r^{7/2})` of C97 (rejected side) and of C94/C95 (elder side).
- **Growing layer.** C101's actual failure-measure rate holds for every fixed `β < 2/3`, not only `β < 1/2`: `1 − p_r = r³(α₁ + α₂) + O_β(r^{3+β})`. For example, `O(r^{18/5})` at `β = 3/5`.
- **Setting.** Gap mark `k = 1`, in C97's and C101's setting.

A4 consumes C91–C97 and C101. They are stored in `frontiers/planar_soft_layer_chain_20261003/`.

## What A4 does not establish

From the proof's section 5:
- no `β ≥ 2/3`, and no `r^{11/3}` without `ε`;
- no compact-gap version (that is A4.1, below);
- nothing in dimension `≥ 3`;
- no change to the reviewed statements of C94, C95, C97 or C101. A4 is additive.

## Not included

- **QS addendum A4.1** ([5973261552](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973261552)). It gives A4's rate on a compact gap interval, uniformly via C103. It was author-side when this packet was built. Read with its erratum E1 ([5973478388](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973478388)), it now has a provider-distinct nonauthor review, PASS_SCOPED ([5973672811](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973672811), released in [5973677514](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973677514)). It stays outside this packet.
- **C117's reviewer program** (`independent_controls.py`, 9063 bytes, SHA256 `3ad506bf…`). It is held in the owner-only Drive delivery named in `A4/REVIEW_COMPLETION.md`, and is recorded here by identity only.

## Replay

    python3 -B -S frontiers/planar_rejected_endpoint_margin_20261003/replay.py
    python3 -B -O -S frontiers/planar_rejected_endpoint_margin_20261003/replay.py

`replay.py` uses the standard library only. It runs four checks:
1. **Identities.** Every stored file has the identity pinned in `SOURCES.json`, and the tree holds nothing else.
2. **Extraction.** The checker and stdout equal the fenced payloads in the stored controls comment.
3. **The checker.** `A4/author_controls.py` reproduces its published stdout byte for byte (61,603 exact checks). Its six mutant labels exit 1, and an invalid label exits 2.
4. **Negative controls.** A one-byte change to the proof is detected, and a checker with the margin's `72` replaced by `36` is rejected.

The workflow `.github/workflows/planar-rejected-endpoint-margin.yml` runs both modes on Python 3.11.16. These finite controls support algebra only, as the review says.
