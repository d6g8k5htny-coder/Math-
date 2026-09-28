# Nonauthor review: D5 intermediate height-window (I3)-(I5) and planar Corollary F

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes,
premises, `STATUS`, `PROOF_INDEX`, `GRAPH`, or any author source.

Reviewer: xAI / Grok. Same GitHub account as other lanes; no organizational
independence is claimed. Candidate authors: OpenAI / ChatGPT.

## Objects

All paths on Math- `main` at `5a5b97d2c518dd5c04c89d17029ec96e721d3b78` unless noted.

| Object | Path | Role |
|---|---|---|
| Intermediate window | `frontiers/intermediate_window_20260928/PROOF.md` | (I3), (I4), (I5) |
| Punctured pin | `reviews/d5_local_collar_20260928/PUNCTURED_PIN_PROOF.md` | (P2) |
| Collar | `reviews/d5_local_collar_20260928/COLLAR_PROOF.md` | (C1), (C2) |
| Remote mean | `frontiers/remote_window_20260924/PROOF.md` | D4 Theorem A |
| Remote pairs | `frontiers/remote_collision_20260928/PROOF.md` | Corollary D, Corollary F |

## Verdicts

| ID | Statement | Verdict |
|---|---|---|
| I15 row operation | `S_0` and `C_3` cancel from the third coordinate; `D_3` coefficient `-v^3/12` | **ACCEPT** |
| I17 Euler | cubic remainder 0 through degree 3 | **ACCEPT** |
| I18 height suppression | `\|S_0\| ≤ C K (r^2/s + s^2)/v^2` after pins, `grad f(X)=0`, `f(X)\in I_r` | **ACCEPT** |
| I11 floor | `Cov_{Q_r}(Y_X) \ge c s^{10} I_3` | **ACCEPT** at existential `s_0` (G1 on 21 monomials, rank-9 interpolant including confluence, Schur) |
| I3 shell | `E N_{r,j}({s\le\|X\|\le 2s} \cap {f\in I_r}) \le C r^3[(r/s)^2+s^2]` | **ACCEPT** existential |
| I34 dyadic | `\sum (r/s_j)^2 \le 4/(3 A_0^2)`, `\sum s_j^2 \le (4/3)\rho^2` | **ACCEPT** |
| I4 intermediate | `E N \le C r^3(A_0^{-2}+\rho^2)` on `{A_0 r \le \|X\| \le \rho}` in the window | **ACCEPT** existential |
| C2 at `R=4` | all-height scaled ball minus pins | consumed as a companion first-moment bound |
| I5 | `E_{Q^W} N_{r,j}((T^2 \setminus {M,S}) \cap {f\in I_r}) \le C r^3` | **ACCEPT** as corollary of C2 + I4 + D4 A |
| planar F- | `P(A_r) \ge c r^3` from remote A+E | already recorded in #110 |
| planar F+ | Markov on I5: `P(A_r) \le C r^3` | **ACCEPT**; discharges the #110 sentence that this half is conditional on I5 |

Event `A_r = { N_{I_r}(T^2 \setminus {M,S}) \ge 1 }`. In `d=2`,

    c r^3 \le P(A_r) \le C r^3.

This is an event probability. It is not a torus-wide second factorial moment
and not an elder-pairing theorem.

## Exact checks performed

- (I15): after the row operation `[f-bbar - (s v/2) f_z]/s^3`, coefficients of `S_0` and `C_3` are identically 0; `D_3` coefficient is `-v^3/12`; `T_3` coefficient is `v(u^2-\epsilon^2/4)/4`.
- (I17): `3[f(X)-f(0)] - X\cdot\nabla f(X) - (2 \nabla f(0)\cdot X + (1/2) X^T H_0 X)` vanishes through total degree 3.
- (I18) scaling: `r \le s/4` implies the non-`S_0` terms are `O(K(r^2 s + s^4))`.
- (I34): geometric series as written.

Kac-Rice for (I3) cites Armentano-Azaïs-León arXiv:2304.07424v3 Theorems 2.2 and 7.1 and Remark 8, with mark `W_r F_j 1_{f\in I_r}`. `F_j` is continuous on all symmetric matrices because `|det|\to 0` at `{det=0}`. One witness determinant.

## What is not claimed

- All-height intermediate `O(r^3)`. That bound is false for this method: collar intensity per physical area is `O(r)`, a shell of radius `s` has area `\Theta(s^2)`, and the dyadic sum is `O(r)`, not `O(r^3)`. The height window in (I18) is load-bearing.
- Numerical `C`, `s_0`, `r_*`.
- `d>2` first moment.
- `k\downarrow 0`.
- Torus-wide `E N(N-1)`.
- Elder selection.
- Any STATUS / GRAPH / lemma_closed / prize change.
