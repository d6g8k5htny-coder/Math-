# Planar soft-layer chain C91–C103: exact records and replayable checkers

Incorporated on 3 October 2026. **Scientific effect: NONE. No new mathematics and no status change.**

This packet stores twelve reviewed objects in the repository, byte for byte: C91–C99 and C101–C103. OpenAI/Codex lanes posted them as native comments on [main#229](https://github.com/d6g8k5htny-coder/main/issues/229) between 00:22Z and 10:40Z on 3 October 2026. For each object the packet holds:
- the frozen proof;
- the full nonauthor review;
- the delivery note;
- every published checker with its exact stdout.

Anthropic Claude incorporated them at the authors' request (pickups [5969536391](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5969536391) and [5969615506](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5969615506); requests listed in `SOURCES.json`).

Two objects from the same run are left out:
- **C100**, a reader-interface object;
- **C104**, the d = 3 contact transfer, which bears on the separate C6/C8 lane (#184, #217).

## Status and attribution

- **Authorship and custody stay with the authors.** The authors are OpenAI/Codex lanes, named per object in `SOURCES.json` together with the reviewer and the verdict quoted from the delivery note. Their R17 claims and Drive deliveries also stay with them.
- **Independence.** Every review is a same-account, delegated AI review. Organizational independence is **0**, and Dylan Roy's personal reading is **PENDING**.
- **What governs.** Each proof's own statement, hypotheses and limits govern. The summaries below paraphrase the delivery notes and are not a substitute for them.
- **Not edited here.** No other packet, `PROOF_INDEX.md`, STATUS, register or graph.

## The objects

| Object | What its delivery note records (paraphrase; see the note) | Stored |
|---|---|---|
| C91 | For an exactly pinned planar C⁴ field, the value, gradient and Hessian-entry errors on a window of size `w` are at most `K_j N r w^{4−j}`. At `k = 1` these constants are `167/192`, `635/384` and `115/48`. It also gives the raw-to-rescaled Hessian transfer, keeping both typing-edge denominators. | `C91/` |
| C92 | **Theorem J.** An `O(r)` polynomial-weighted L¹ comparison for the actual weighted jets on a fixed bounded soft-Hessian layer. The soft-layer probability is `r³m_Λ/z₀ + O(r⁴)` with the full normalizer. | `C92/` |
| C93 | The normalized probability of the two typing-edge strips is `≤ C r³(δ² + rδ)`. A truncated Hessian-transfer bound holds. On `w = r^{−β}`, `0 ≤ β < 1/4`, the analytic bad mass is `O(r⁴)`. | `C93/` |
| C94 | On the planar model-elder sector `E`, `Q_r^W(E \ Good) ≤ C r^{7/2}` and `Q_r^W(Good | E) = 1 − O(√r)`. Its §6 is conditional on a geometric interface `G`. | `C94/` |
| C95 | It corrects A2 v1 (C90's three findings) and supplies `G`. The corrected object is (A2 v1, C95 §§1–3). With `A_r` the maximin event: `Q_r^W(E \ A_r) ≤ C r^{7/2}` and `Q_r^W(A_r | E) = 1 − O(√r)`. | `C95/` |
| C96 | The designated maximin event equals finite ordinary-superlevel H0 elder death, on a compact connected closed Morse manifold with distinct critical values. | `C96/` |
| C97 | The rejected-side companion: `Q_r^W(Rsec ∩ H_r) ≤ C r^{7/2}`. It keeps both the saddle margin `μ` and the endpoint margin `4(1 − μ)`. | `C97/` |
| C98 | `E` equals the negative-margin sector exactly. With `Rsec`, it covers the typed bounded layer up to a set that is null under both laws. So `Q_r^W(D_Λ ∩ (H Δ E)) ≤ C r^{7/2}`, and the conditional pairing probability is `m_E/m_Λ + O(√r)`. | `C98/` |
| C99 | For the once-counted selected-bar population: finite-scale absolute continuity, an explicit limiting density, and `‖h^{−5}q_h − q₀‖_{L¹(0,∞)} → 0`. This is conditional on seven analytic interfaces plus U/ROOTS. The occurrence-conditioned conclusion consumes the O interface of the open Math-#234. | `C99/` |
| C101 | At `k = 1`, `1 − p_r = r³(α₁ + α₂) + O(r^{13/4})`, and more generally `O_β(r^{3+β})` for `0 < β < 1/2`. The failure raw-jet measure divided by `r³` converges in variation at rate `O_β(r^β)`. | `C101/` |
| C102 | Original-law Gaussian transfer on a fixed compact gap interval `K ⊂ (0, ∞)`. It gives the physical-jet volume factor `r/k⁴`, correlated moment bounds, typing strips, `Z_r = r²z_r` with `z_r = z₀ + O(r)`, and `A_r = A₀ + O(r)`. | `C102/` |
| C103 | Uniform on compact `K`, the designated-pair failure raw-jet measure has variation error `O_K(r^{1/4})`, and `1 − p_r = r³(α₁ + α₂) + O_K(r^{13/4})`. | `C103/` |

**Common setting.** A normalized periodized Gaussian field on a fixed planar torus. Birth heights lie in a fixed compact set, all orthonormal frames are allowed, and the full weighted normalizer is used.
- **Gap mark.** C91–C101 use gap mark `k = 1`. C102 and C103 cover a fixed compact `K` of positive gaps.
- **Soft layer.** C91–C98 work on a fixed bounded soft layer `Λ`.
- **Rarity.** `E` is a rare sector of mass order `r³`, so the conditional statements are not unconditional probabilities tending to one.

## How the pieces fit

- **C91 → C92 → C93 → C94.** Taylor control on growing windows (C91) feeds the weighted jet transfer (C92), the typing-edge strips (C93), and the trap window with its random margins (C94).
- **C95.** It corrects A2 and supplies `G`, completing the elder side.
- **C96.** It identifies the maximin event with ordinary H0 elder death.
- **C97 and C98.** C97 handles the rejected side, and C98 shows that the two sectors cover the bounded layer.
- **C99.** It turns the bounded-layer comparison into lifetime densities for the once-counted population.
- **C101, C102 and C103.** C101 gives a quantitative rate at `k = 1`. C102 transfers the Gaussian estimates to a compact gap interval, and C103 makes C101's rate uniform on it.

Repository context:
- C91 makes the planar window dependence of `frontiers/soft_fold_limit_20261002` (Theorem FL, #243) explicit.
- C95's corrected A2 and C97's chord build on the QS/A2 comments on main#229.

## What the chain does not establish

From the delivery notes:
- no growing-`Λ` or all-marks theorem;
- no total-variation bound for the field or for real-valued marks;
- no identification of all small bars, and no converse;
- no regional shrinking multiple-witness, intermediate or coarea closure;
- no gap tending to 0;
- no higher-dimensional or infinite-volume result;
- no Conjecture 7 closure, and no final global density or remainder closure.

C99 claims no quantitative rate. C101 and C103 count each designated candidate's failure once, and do not count replacement bars. Since then, #248 has merged a separate planar remote-collision bound with a shrinking cutoff (C107); it is not part of this packet.

## Replay

    python3 -B -S frontiers/planar_soft_layer_chain_20261003/replay.py
    python3 -B -O -S frontiers/planar_soft_layer_chain_20261003/replay.py

`replay.py` uses the standard library only. It runs four checks:
1. **Identities.** Every stored file has the identity pinned in `SOURCES.json`, and the tree holds nothing else. C96's frozen proof (7657 bytes, SHA256 `7198ff63…`) is the tail of its native comment.
2. **Fourteen checkers.** Each reproduces its published stdout. These are the independent checkers of C91–C95, C97–C99 and C101–C103, plus the author controls of C99, C101 and C103.
   - Five of them print the interpreter version (`SOURCES.json` records the line). On that line only, the published version is replaced by the running one, and every other byte must be identical.
   - The rest must match byte for byte.
3. **C102's source tree.** It is assembled in a temporary directory from the stored copies and the repository paths in `C102/SOURCE_IDENTITIES.json`, each checked by size and hash first.
4. **Negative controls.** Three must be rejected:
   - a one-byte change to a stored proof;
   - a C93 checker with one changed constant;
   - a changed byte outside a version line.

**Limits.** As each review says, the checkers support algebra. They do not prove the analytic or topological claims.

## Files

- **Each `C9x/` or `C10x/` folder** holds exact comment bodies:
  - `PROOF.md`, `REVIEW.md` and `DELIVERY.md`;
  - where published: `CHECKER_COMMENT.md`, `AUTHOR_CONTROLS_COMMENT.md`, `HANDOFF.md`, `COMPLETION.md` (C96) and `SOURCES_COMMENT.md` (C103).
- **Checker payloads.** `checker.py` with `checker_stdout.txt`, and `author_controls.py` with `author_controls_stdout.txt`, are extracted verbatim from those comments. Each fence is saved with its final newline.
- **`C102/SOURCE_IDENTITIES.json`** is C102's published source manifest.
- **`SOURCES.json`** gives the exact identities of every stored file. For each object it also records:
  - author, reviewer and the verdict as recorded;
  - the unstored pickup and ownership comments (with hashes);
  - the published Drive delivery identity (not downloaded or relied on);
  - the main#229 comments its proof names;
  - the extraction rule and version line of each checker.
- **`replay.py`** is the replay described above.
