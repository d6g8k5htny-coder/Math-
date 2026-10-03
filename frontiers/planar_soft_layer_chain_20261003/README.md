# Planar soft-layer chain C91–C98: exact records and replayable checkers

Incorporated on 3 October 2026. **Scientific effect: NONE. No new mathematics and no status change.**

This packet stores eight reviewed objects in the repository, byte for byte. OpenAI/Codex lanes posted them as native comments on [main#229](https://github.com/d6g8k5htny-coder/main/issues/229) between 00:22Z and 05:21Z on 3 October 2026. For each object the packet holds:
- the frozen proof;
- the full nonauthor review;
- the delivery note;
- where one was published, the independent checker and its exact stdout.

Anthropic Claude incorporated them at the authors' request (pickup [5969536391](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5969536391); requests listed in `SOURCES.json`).

## Status and attribution

- **Authorship and custody stay with the authors.** The authors are OpenAI/Codex `root01a0bbb5` for every object except C96, which is by `root01a0adb2`. Their R17 claims and Drive deliveries also stay with them. Each `SOURCES.json` record names the author and reviewer, and quotes the verdict from the delivery note.
- **Independence.** Every review is a same-account, delegated AI review. Organizational independence is **0**, and Dylan Roy's personal reading is **PENDING**.
- **What governs.** Each proof's own statement, hypotheses and limits govern. The summaries below paraphrase the delivery notes and are not a substitute for them.
- **Not edited here.** No other packet, `PROOF_INDEX.md`, STATUS, register or graph.

## The objects

| Object | What its delivery note records (paraphrase; see the note) | Stored |
|---|---|---|
| C91 | For an exactly pinned planar C⁴ field, the value, gradient and Hessian-entry errors on a window of size `w` are at most `K_j N r w^{4−j}`. At `k = 1` these constants are `167/192`, `635/384` and `115/48`. It also gives the raw-to-rescaled Hessian transfer, keeping both typing-edge denominators. | `C91/` |
| C92 | **Theorem J.** An `O(r)` polynomial-weighted L¹ comparison for the actual weighted jets on a fixed bounded soft-Hessian layer. The soft-layer probability is `r³m_Λ/z₀ + O(r⁴)` with the full normalizer, and the growing-window Taylor failure is `o(r³)` in the stated regime. | `C92/` |
| C93 | The full normalized probability of the two typing-edge strips is `≤ C r³(δ² + rδ)`. A truncated Hessian-transfer bound holds. On `w = r^{−β}`, `0 ≤ β < 1/4`, the analytic bad mass is `O(r⁴)` against a soft-layer mass of order `r³`. | `C93/` |
| C94 | On the planar model-elder sector `E`, `Q_r^W(E \ Good) ≤ C r^{7/2}` and `Q_r^W(Good | E) = 1 − O(√r)`. Its §6 is conditional on a geometric interface `G`. | `C94/` |
| C95 | It corrects A2 v1 (C90's three findings) and supplies `G`. The corrected object is (A2 v1, C95 §§1–3). With `A_r` the event that the maximin level of the pinned maximum equals the pinned saddle height: `Q_r^W(E \ A_r) ≤ C r^{7/2}` and `Q_r^W(A_r | E) = 1 − O(√r)`. | `C95/` |
| C96 | The designated maximin event equals finite ordinary-superlevel H0 elder death on a compact connected closed Morse manifold with distinct critical values. So C95 transfers to the designated H0 pairing. | `C96/` |
| C97 | The rejected-side companion. On the rejected sector `Rsec`, `Q_r^W(Rsec ∩ H_r) ≤ C r^{7/2}`. It keeps both the saddle margin `μ` and the endpoint margin `4(1 − μ)`. | `C97/` |
| C98 | `E` equals the negative-margin sector exactly. With `Rsec`, it covers the typed bounded layer up to a set that is null under both laws. So `Q_r^W(D_Λ ∩ (H Δ E)) ≤ C r^{7/2}`, and the conditional pairing probability is `m_E/m_Λ + O(√r)`. | `C98/` |

**Common setting.** A normalized periodized Gaussian field on a fixed planar torus of side `L`. The gap mark is `k = 1`, birth heights lie in a fixed compact set, all orthonormal frames are allowed, `Λ` is fixed and finite, and the full weighted normalizer `Z_r` is used. `E` is a rare sector of mass order `r³`, so the conditional statements are not unconditional probabilities tending to one.

## How the pieces fit

- **C91 → C92 → C93 → C94.** Taylor control on growing windows (C91) feeds the weighted jet transfer (C92), the typing-edge strips (C93), and then the trap window with its random margins (C94).
- **C94 + C95.** C95 corrects A2 and supplies C94's interface `G`, completing the elder side.
- **C96.** It identifies the maximin event with ordinary H0 elder death.
- **C97 and C98.** C97 handles the rejected side, and C98 shows that the two sectors cover the bounded layer.

Repository context:
- C91 makes the planar window dependence of `frontiers/soft_fold_limit_20261002` (Theorem FL, #243) explicit.
- C95's corrected A2 and C97's chord build on the QS/A2 comments on main#229.

## What the chain does not establish

From C98's delivery note:
- no growing-`Λ` or all-marks theorem;
- no total-variation bound for the field or the real-valued marks;
- no converse for all small bars;
- no regional shrinking-collision estimate;
- no higher-dimensional or infinite-volume result;
- no final global density or remainder closure.

Since then, #248 has merged a separate planar remote-collision bound with a shrinking cutoff (C107); it is not part of this packet.

## Replay

    python3 -B -S frontiers/planar_soft_layer_chain_20261003/replay.py
    python3 -B -O -S frontiers/planar_soft_layer_chain_20261003/replay.py

`replay.py` uses the standard library only. It runs four checks:
1. Every stored file has the identity pinned in `SOURCES.json`, and the tree holds nothing else.
2. C96's frozen proof (7657 bytes, SHA256 `7198ff63…`) is the tail of its native comment.
3. Each of the seven published checkers (C91, C92, C93, C94, the C95 helper, C97, C98) reproduces its published stdout byte for byte.
4. Two negative controls: a one-byte change to a stored proof is detected, and a C93 checker with one changed constant fails.

**Limits.** As each review says, these finite checkers support algebra. They do not prove the analytic or topological claims.

## Files

- **`C9x/`.**
  - `PROOF.md`, `REVIEW.md` and `DELIVERY.md`: exact comment bodies.
  - `C95/`, `C97/`, `C98/`: `CHECKER_COMMENT.md` is the comment that published the checker.
  - `C96/COMPLETION.md`: the author's completion note.
  - `checker.py` and `checker_stdout.txt`: extracted verbatim from the review or checker comment, each with a final newline, as the reviews instruct.
- **`SOURCES.json`.** Exact identities of every stored file, plus the following for each object:
  - author, reviewer and the verdict as recorded;
  - the unstored pickup comments (with hashes);
  - the published Drive delivery identity (not downloaded or relied on);
  - the main#229 comments its proof names.
- **`replay.py`.** The replay described above.
