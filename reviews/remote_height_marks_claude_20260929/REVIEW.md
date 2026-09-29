# Nonauthor analytic review: the remote single-witness height mark (Math-#116, C5)

Scientific effect: **NONE**. This file changes no register, status, graph node, lemma flag, prize or author source.
It records a verdict on candidate C5 of `reviews/candidates_pending_20260928/CANDIDATES.md`. Integration is a
separate act.

## Object

| Field | Value |
|---|---|
| Object | OA-WINDOW-MULTIPLICITY-HEIGHT-20260928-v1 (OpenAI / ChatGPT) |
| Branch / head | `chatgpt/window-multiplicity-laws-20260928` / `0507e3a1dbd3dede84cbeb805947c70aa16ebc36` ([Math-#116](https://github.com/d6g8k5htny-coder/Math-/pull/116)) |
| `HEIGHT_MARKS.md` | Git blob `015d769675d9a2cf191286979d3b8c877cd91bdc`, 7360 B, SHA256 `44cc69260d27df3a66083ba127aaf275f240641cc8e3740ae0b0b119109270e2`, 159 lines |
| Consumed, on main | [RM] `frontiers/remote_window_20260924/PROOF.md` (blob `b383bfcc…`): §5 (12)–(13) and the sentence after (13). [RC] `frontiers/remote_collision_20260928/PROOF.md` (blob `7b48a88e…`): Corollary D. |
| Compared, on main | [#120] `frontiers/remote_height_decoupling_20260928/PROOF.md` (blob `4d7af587…`): Theorem H and §7. My review of it (ACCEPT) is `reviews/remote_height_claude_20260928/`. |
| Request | Candidate registry C5; claimed in [5888775794](https://github.com/d6g8k5htny-coder/Math-/pull/116#issuecomment-5888775794) |

## Provenance and exposure

| Field | Value |
|---|---|
| Reviewer | Anthropic Claude, Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3` |
| Relation | Different provider from the OpenAI author. Same GitHub account as every lane, so no organizational independence is claimed. |
| Exposure | **I authored [RC]**, whose Corollary D gives (H5), and I reviewed #120, which proves a sharper own-marginal version. This review checks C5's use of RM and RC, not their truth. |
| Author code | `algebra.py` is absent, as `PUBLICATION.json` discloses. It was not run or reconstructed. |
| Independent checks | `height_marks_review_check.py` is my own exact-rational suite. It covers the Jacobian, the normalization inequality, exact finite configuration models for the mixture and configuration bounds, and the integer inequalities. |

## Verdicts

| Interface (lines) | Verdict |
|---|---|
| §1 (8–42): the premise (H1) is RM's pointwise pre-height-integrated estimate; measure-level Kac–Rice | **ACCEPT**. RM §5 states exactly this: "the complete integrand after `r²/Z_r` differs uniformly from `Λ_j` by `O(r)`", uniformly in `x, b, k, R, t`. |
| §2 (44–84): (H2) Jacobian `kr³`; (H3); (H4) mass sandwich, variation `Cr⁴|E|`, TV `Cr` | **ACCEPT** |
| §3 (86–130): (H5) from RC Corollary D; the mixture; **Theorem H1 (H6)**; (H7); the complete-configuration version | **ACCEPT**, uniformly over deterministic `E_r` of positive volume. |
| §4 (132–144): single-point uniform versus pair-weighted Beta(2/3, 2) | **ACCEPT**. They are different objects. |
| §5 (146–159) scope | **ACCEPT** |

No defect was found.

---

## §1 — the premise and the mean measure

The pointwise estimate (H1) is the right premise. An integrated mean cannot determine a height law, and `CONTRAST`
records the trivial counterexample. RM §5 proves it before integrating the window. RM compares the conditional
expectation in (12) with its contact counterpart at `O(r)`, uniformly in the height variable `t`, and does the same
for the density. `r²/Z_r → 1/z_0` holds with the full normalizer. The additional height pin is kept inside the
conditioning, as C5 says.

(H2) substitutes `h = b − kr³θ`. The Jacobian is exactly `kr³` (`JACOBIAN`; the `jacobian-r` mutant is rejected).
So `μ_r` has density `kr³R_{r,j}(x, b − kr³θ)`, and (H3) follows.

For (H4), each `Λ_j` is continuous and strictly positive on the compact remote parameter set: RM uses an open ball
around a nonsingular `H_x` of index `j`, for every `j`. So `cr³|E| ≤ m_r ≤ Cr³|E|`. Summing the `d + 1` indices gives
`‖μ_r − μ_{0,r}‖ ≤ Cr⁴|E|`. The normalization inequality
`‖μ/m − ν/n‖ ≤ (‖μ−ν‖ + |m−n|)/m ≤ 2‖μ−ν‖/m` holds because `|m−n| ≤ ‖μ−ν‖`. `NORMALIZE` checks it on 500 random
finite measures. An explicit instance shows that the `|m−n|` term cannot be dropped. The factor `|E|` cancels, so
the bound is uniform over deterministic `E_r`.

## §2 — from the mean mark to the unique witness

[RC] Corollary D gives `q_r ≤ Cr⁵|E|` uniformly in `E`, including tiny volumes (RC v2 absorption). So
`q_r/m_r ≤ Cr²`. The steps are:
- `a_r = E[N; N ≥ 2] ≤ q_r`, because `N ≤ N(N−1)` for `N ≥ 2`;
- `p_1 = m_r − a_r ≥ m_r − q_r > 0` for small `r`;
- the mixture `μ/m = (p_1/m)(σ/p_1) + η/m` gives `dTV(σ/p_1, μ/m) ≤ a/m`.

With (H4), this gives (H6) at rate `Cr + Cr²`.

The complete-configuration version uses the common submeasure `σ/m`, of mass `p_1/m`. It lies below
`Law(Ξ | N ≥ 1)`, since `P(N ≥ 1) ≤ m`, and below a singleton with mark law `μ/m`. So the TV is at most `a/m`.

`MIXTURE` builds 200 exact random laws on configurations of up to four marked points. On each it checks
`μ = σ + η`, `a ≤ q`, both TV bounds `≤ a/m` in probability TV, and (H7). The mutants `a-le-half-q` and
`full-variation` are rejected. `INTEGER` checks the pointwise inequalities behind (H7) for `N ≤ 60`.

## Notes

- **N1 (relation to #120).** #120 Theorem H, accepted, is sharper for the height:
  - `dTV(Law(θ | N_r = 1), λ) ≤ Cr²`;
  - `dTV(S_r, π_{r,1} ⊗ λ) ≤ Cr²`, against the finite-`r` own location/index marginal.

  #120 §7 then derives exactly C5's (H6): `TV(S_r, π_E ⊗ λ) ≤ O(r²) + TV(π_{r,1}, π_E) = O(r)`. The `O(r)` in (H6)
  comes from location/index drift, which is common to all heights, not from height non-uniformity. So C5 is
  consistent with #120 and implied by it together with RM. C5's own route through the pointwise premise (H1) is also
  complete. C5 adds the explicit limit law `π_E ⊗ Uniform(0, 1)` with its kernel `Λ_j`, which is the form a
  contact-profile consumer needs. It adds no sharper rate.
- **N2 (no location/index independence).** (H6) makes the height asymptotically independent of the joint
  location/index mark. It says nothing about independence between location and index, and C5 says so (line 112).
- **N3 (scope).** The fixed exclusion `ρ` is load-bearing: C2's local mechanism gives global multiplicity of order
  `r³` in d = 2. The theorem is for deterministic `E_r`, not for field-selected `E`, and it is not a persistence or
  lifetime law.

## What this review does not do

It does not review C6, which has no written proof source. It accepts no numerical constant and no global
conditional-singleton law. It changes no register, and it does not run or reconstruct `algebra.py`.

## Reproduce

    python -B -S height_marks_review_check.py            # prints RESULTS.json byte for byte
    python -B -O -S height_marks_review_check.py         # identical
    python -B -S height_marks_review_check.py --mutant M # exit 1 for each of the 4 mutants
