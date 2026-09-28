# Nonauthor analytic review: D5 intermediate height-window bridge (Math-#107)

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes, premises, `STATUS`,
`PROOF_INDEX`, `GRAPH` or any author source. It records verdicts. Integration is a separate act.

## Object

| Field | Value |
|---|---|
| Object | OA-D5-INTERMEDIATE-WINDOW-20260928-v1 (OpenAI / ChatGPT) |
| Branch / head | `chatgpt/intermediate-window-20260928` / `742e72e427cd98e529af4d86b3917b1c7f144f01` ([Math-#107](https://github.com/d6g8k5htny-coder/Math-/pull/107)) |
| `PROOF.md` | Git blob `f53a527ce0204fda271f24730b62b4223a5e43ec`, 27775 B, SHA256 `b3eb9456d7058b5b78149cfca4e072679beda85cd1a0293d209664a542db66cf` |
| Consumed, already on main | `reviews/d5_local_collar_20260928/` (#105), `frontiers/remote_window_20260924/PROOF.md` (blob `b383bfcc88ec4ad497dff01fb6640e429ba24a84`) |
| Companion review | Grok record [Math-#108](https://github.com/d6g8k5htny-coder/Math-/pull/108), head `05291156…` |

## Provenance

| Field | Value |
|---|---|
| Reviewer | Anthropic Claude, Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3` |
| Relation | Different provider from the OpenAI author. Same GitHub account as every lane, so no organizational independence is claimed. |
| Exposure | I read `PROOF.md` in full, Grok's #108 review, the #105 collar statement, and the remote Theorem A statement. I also reviewed #105 earlier (comment 5872932723), and (I5) consumes #105's local theorem, so this review and that one share a reviewer. |
| Independent checks | `iw_exact_check.py` was written without reading the author's `algebra.py`. The author's runner was also replayed from a `git archive` of `742e72e`: 15 tests in each mode and 10 mutants rejected, matching `RESULTS.json`. |

## Verdicts

| Interface | Verdict |
|---|---|
| (I7)–(I9) Hermite frame; remainder uniform through ε = 0 | **ACCEPT** |
| (I10)–(I11) observation floor `c s^10` | **ACCEPT**. It is conservative; Grok's sharper `diag(s^8,s^8,s^10)` is correct and not needed. |
| (I12)–(I16) pinned expansions, row operation, target, Jacobian | **ACCEPT**. Checked exactly on a generic degree-six field with the pins solved. |
| (I17)–(I18) Euler critical-height suppression | **ACCEPT** |
| (I19)–(I22) endpoint and witness determinant bounds | **ACCEPT** |
| (I23)–(I26) axial strip | **ACCEPT** |
| (I27)–(I30) transverse rank, relative covariance, conditional moments | **ACCEPT** |
| (I31)–(I32) shell ledger | **ACCEPT** |
| (I33) weighted Kac–Rice with height disintegration | **ACCEPT**, with citation note N3 |
| (I34) dyadic summation | **ACCEPT** |
| **(I3) shell** and **(I4) intermediate** | **ACCEPT** at the stated existential scope |
| **(I5) global single-witness first moment** | **ACCEPT** as a composition. The explicit tiling is given in N1. It depends on #105 (C2) and the reviewed remote Theorem A. |

Each of Grok's HOLD items, (I11), (I18), (I25)/(I30), (I33), (I3), (I4) and (I5), is addressed below.

---

## §3 — observation floor through confluence (I7)–(I11)

**Hermite frame** (checked exactly, group `H`). For a generic degree-9 `g`:

- `H(0) = s0 - a^2 d1/2`, `H'(0) = (3d0 - s1)/2`, `H''(0) = d1`, `H'''(0) = 3(s1 - d0)/a^2` reproduce every cubic.
- `H'''(0) = [3/(4a^3)] ∫_{-a}^{a} (a^2-t^2) g'''`, with kernel mass 1.
- `d0` and `d1` are the averages of `g'` and `g''`.
- None of the four formulas contains a negative power of `a`.

So every scaled endpoint coordinate is a bounded functional on `C^3` uniformly for `0 <= ε <= 1/4`. The degree-six
Taylor remainder of `g(Y) = f(sY)` has derivatives of order at most 3 of size `O(s^6 K_6)` on `|Y| <= 2`. This gives
(I9) with no ε-loss. The same weight appears in my D1 review as the `U3` average.

**Rank at confluence** (group `RK`).

- `z^2, z^3, xz^2` and `x^4, x^5, x^2z` annihilate the six contact functionals.
- Their value/gradient minors at `w` are exactly `-v^6` and `u^10`.
- The negative control confirms the drop at degree four: on the axis every 3×3 minor of the kernel's witness rows is
  identically zero.
- For `ε > 0` the three sites are distinct (`|w| >= 1 > ε/2`), and the cardinal construction gives rank 9.
- `B_{ε,w}` is polynomial in `ε`, so it is continuous at `ε = 0`. Compactness of `[0,1/4] × A` gives a uniform
  `σ_min`.

**Floor.**

- `J_5` consists of 21 distinct one-site derivative functionals, so `Cov(J_5) >= c I` uniformly over frames (lattice
  positivity plus compactness).
- For a unit row: `std(a·V) >= c s^5 ||aB|| - C s^6 >= c' s^5`.
- Unscaling multiplies coordinates by `s^{-j} >= 1`.
- The Schur complement on `U_r` then has `λ_min >= λ_min(Cov(U_r, Y_X))`.

This gives (I11). On Grok's note: the gradient rows carry an extra `s^{-1}`, so the sharp floor is
`diag(s^8, s^8, s^10)`. `c s^10 I_3` is a valid, weaker floor, and only the weaker floor is used.

## §4 — expansions (I12)–(I16): checked on a generic field

Group `EX` takes a **generic degree-six** field (28 coefficients). It solves the six pins exactly for
`(c00,c10,c20,c30,c01,c11)` through the Hermite formulas and checks the following.

- The six pins hold identically.
- Every order in (I12):
  - `f(0)-b̄ = O(r^4)`;
  - `f_x(0) + 3kr^2/2 = O(r^4)`;
  - `f_z(0) + r^2T_3/8 = O(r^4)`;
  - `f_xx(0), f_xz(0) = O(r^2)`;
  - `f_xxx(0) - 12k = O(r^2)`.
- After `X = s(u,v)` and `r = εs`, the reduced vector `Z` of (I14) has **no negative power of s**. So the apparent
  `S_0/s` term cancels exactly.
- `Z`'s `s^0` part equals `mean + BJ` of (I15) exactly, including the third-row coefficients `v d_e/4` for `T_3`,
  `0` for `C_3` and `S_0`, and `-v^3/12` for `D_3`.
- The physical Jacobian is `s^6`.

`B` is read off the computed `s^0` part rather than typed. Group `TR` then checks:

- the `(C_3,D_3,S_0)` minor equals `v^6/24`;
- Cauchy–Binet holds for `det(BB^T)`;
- every entry of `B` is `O(|v|)`.

Mutants `d3-coefficient`, `no-row-operation` and `minor-constant` are refuted.

The `O(sK)` remainders, on the other hand, come from Taylor's theorem with `K = C(1+||f||_{C^6})`. They use
`ε <= 1/4` in comparisons such as `r^2/s <= s` and `r^4/s^3 <= r`.

## §5 — Euler suppression and determinants (I17)–(I22): HOLD item (I18)

Group `EU` checks exactly that `3[f(X)-f(0)] - X·∇f(X) = 2∇f(0)·X + ½XᵀH_0X + Σ_{j>=4}(3-j)P_j(X)`. The cubic
terms cancel.

At a critical point `X`, the left side is `3(y - f(0))`, and the degree-four-and-higher part is `O(s^4 K)`. The terms
other than `(s^2v^2/2)S_0` are bounded as follows:

- `3|y-f(0)| <= 3k r^3/2 + C r^4 K`, since `|y - b̄| <= kr^3/2`;
- `2|∇f(0)·X| <= C r^2 s K`;
- `(s^2/2)|f_xx(0)u^2 + 2f_xz(0)uv| <= C r^2 s^2 K`.

With `r^3 <= r^2 s` and `r^2s^2 <= r^2 s` (both checked on 3,000 exact random pairs `r <= s/4 <= 1/4`), this gives
`|S_0| v^2 <= C K (r^2/s + s^2)`.

This is **pathwise**. It holds on every field that satisfies the six pins and has a critical point at `X` with height
in `I_r`, so it needs no conditioning argument: it holds almost surely under the conditional law in (I33). It is
false without the height window, because then the `3|y - f(0)|` term is `O(1)`.

**(I19).** The gradient pins make the segment averages of `(f_xx, f_xz)` zero, so `||H_M e_x||, ||H_S e_x|| <= Kr/2`.
Also `f_zz(M), f_zz(S) = S_0 + O(rK)`, and expanding the 2×2 determinant gives (I19).

**(I20).** From `∇f(X) = ∇f(M) = 0`:

- `H_M(X-M) = O(K|X-M|^2) = O(Ks^2)`.
- Subtracting `(su + r/2) H_M e_x = O(Krs)` and dividing by `s|v|` gives `||H_M e_z|| <= CKs/|v|`.
- Transport adds `3Ks <= 6Ks/|v|`.

**(I21) and (I22).** Group `LG` checks the product `W|det H_X|/Z = K^6 s^2 (r+s^2)^2 v^{-6}` symbolically, using
`|S_0| + rK <= CK(r+s^2)/v^2` and `r^2/s <= r/4`. (I22) needs only `|S_0| <= K` and `|det H_X| <= CK^2`.

## §6–§7 — densities and conditional moments: HOLD items (I25)/(I30)

**Axial strip (I23)–(I26).**

- On `|v| <= v_0` we have `u^2 >= 1 - v_0^2`, so `d_e >= 1 - v_0^2 - 1/64 > 0`.
- The mean of `f_x/s^2` is at least `6k_- d_e - C v_0 - C s >= c_0`, and its variance is at most `C(v^2+s^2)`,
  because the deterministic part carries no variance.
- For positive definite `Σ`, `xᵀΣ^{-1}x >= x_1^2/Σ_11`. This bounds the **full** three-dimensional Mahalanobis
  exponent below by `c/(v^2+s^2)`, whatever the value of `y`.
- On `|v| <= s^{1/8}` the density is therefore at most `C s^{-15} exp(-c s^{-1/4})`.

**(I25), where Grok asked about ε-loss and pin versus witness conditioning.**

- Under `Q_r`, regress the whole field on `Y_X`. The cross-covariances satisfy
  `|Cov_Q(D^αf(z), Y_X)| <= (Var D^αf · Var Y_X)^{1/2} = O(1)`, and `||Σ_X^{-1}|| <= C s^{-10}`.
- The target deviation `(0,y) - E_Q Y_X` is bounded, so the conditional mean moves by at most `C s^{-10}` in `C^6`.
- The residual is `f - E_Q f - A(Y_X - E_Q Y_X)` with `||A||_{C^6} <= C s^{-10}`, so its sixth moment is at most
  `C s^{-60}`.

Every constant depends only on `(I6)` under `Q_r`, on `(I11)`, and on the bounded window. None depends on `ε`.

**(I27)–(I30).**

- `σ_min(B) >= c v^4`, because `σ_1σ_2σ_3 >= v^6/24` and `σ_1, σ_2 <= C|v|`.
- The `O(s)` remainder costs at most `C s/v^4 <= C s^{1/2}` relative to `||aB||`, since `|v| >= s^{1/8}`. So
  `Cov(Z) >= c BBᵀ`, `det >= c v^12` and `||Cov^{-1}|| <= C v^{-8}`.
- For (I30), regress on `Z`. `Var Z = O(1)`, so `|Cov(D^αf, Z)| = O(1)` by Cauchy–Schwarz. The target `τ` is bounded
  by (I16), and the same argument gives `C|v|^{-48}`.
- (I29): the Gaussian penalty `exp(-c/(v^2+s^2)) <= exp(-c/(2v^2))` holds on `|v| <= v_0`, because `s <= |v|`. The
  prefactor is `C|v|^{-6}`, and the Jacobian contributes `s^{-6}`.

## §8–§10 — ledger, Kac–Rice and dyadic sum: HOLD items (I33), (I3), (I4)

**(I31) and (I32).** These are checked symbolically. In addition,
`2r^3[(r/s)^2+s^2] - r^3(r+s^2)^2/s^2 = r^3(r/s - s)^2 >= 0` holds exactly. The axial strip adds `C r^3 s^2`. This
proves (I3).

**(I34).** Every partial sum `Σ_{j<=n} 4^{-j}` is below `4/3` (checked exactly for n < 80). With `A_0 >= 4`, every
shell has `r <= s_j/4`, and the constants of (I3) do not depend on `j`. This proves (I4).

**(I33).** The Theorem 7.1 mark is `g = min(W_r, N) · 1{H_X ∈ O_j} · 1{f(X) ∈ open I}`, where `O_j` is the open
set of nonsingular symmetric matrices with `j` negative eigenvalues. The witness determinant is **not** part of the
mark: Theorem 7.1's Jacobian factor `Δ(X) = |det H_X|` supplies it, and `Δ · 1{H_X ∈ O_j} = F_j(H_X)`. So the witness
determinant appears exactly once, as in (I33). *(Corrected in v2; see Revision history.)*

- `W_r` is a continuous nonnegative functional of the field (the endpoint determinants and type indicators enter
  through the continuous `F_d`, `F_(d-1)`). Indicators of the open sets `O_j` and `I` are lower semicontinuous. So
  `g` satisfies hypotheses (a)–(b) of arXiv:2304.07424v3 Theorem 7.1, and Remark 8 gives (c).
- On the compact shell, the nondegeneracy of `∇f(X)` required by Theorem 2.1's hypotheses follows from (I11).
- Monotone convergence in `N` and in the interval, together with the nondegenerate joint density of `(∇f, f)(X)`,
  gives (I33).

**N3 (citation).** Theorem 7.1 is stated under Theorem 2.1. Remark 7 is the Gaussian bridge, as in my D1 §9 note N2.

## (I5) — the global composition: HOLD item (I5)

**N1 (explicit tiling).** Use one `(Q_r, W_r, Z_r)` throughout. Distances are measured from the midpoint.

| Region | Source | Parameter choice | Height |
|---|---|---|---|
| `|X| <= 4r`, pins removed | #105 synthesis (C2), "any fixed R >= 1" | **R = 4** | all heights, which contains `I_r` |
| `4r <= |X| <= s_0` | (I4) of this note | **A_0 = 4, ρ = s_0** | `I_r` |
| `|X| >= s_0` | remote Theorem A (`frontiers/remote_window_20260924`), "fix 0 < ρ < L/4", reviewed ACCEPT (main#76) | **ρ = s_0** | `I_r` |

Boundaries are assigned once, and `r` is taken below all three cutoffs. So:

- **No annulus is left uncovered.** This answers Grok's tiling caveat.
- The note's §10 "direct remote check" is **not needed**. The reviewed Theorem A already allows any fixed ρ, so
  (I5) does not depend on that new paragraph.
- The PR53/PR55 **pin-neighborhood AMEND** concerns the superseded PR53 reconnaissance integral. (I5) does not
  consume PR53. Its local piece is #105 (C2), whose punctured-pin and collar proofs were merged at `aeed376` after
  nonauthor review. The PROOF_INDEX lines describing that gap (the D5 pin-neighborhood entry) predate #105 and are
  stale as navigation, not as verdicts.

**What (I5) is.** A global first moment `E_{Q_r^W} N_{r,j}(torus \ {M,S}) <= C r^3` for witnesses **in the between-pin
height window**, in the fixed planar `T`-periodic model with compact marks. By Markov, the `Q_r^W`-probability of any
additional window critical point is at most `C r^3`.

**What it is not.** It is not an all-height count, a factorial moment or collision estimate, elder selection, a
numerical constant, or uniformity in `T`, `k -> 0` or dimension.

## Revision history

- **v1**, head `5f96246`: initial record.
- **v2**: responds to the integrator's repair request on Math-#109 (comment 5874648263). Two changes:
  - The (I33) paragraph's Theorem 7.1 mark is corrected from `min(W_r F_j(H_X), N)`, which would count
    `|det H_X|` twice once the formula's Jacobian is applied, to `min(W_r, N) 1{H_X ∈ O_j}`.
  - An unmanifested `__pycache__` binary is removed from the tree.
- The verdicts are unchanged. #107's own (I33) text uses the witness type/height mark and is correct; the slip was in
  this review's paraphrase.

## Checks run

```
python -B -S iw_exact_check.py                          # rc 0
python -B -O -S iw_exact_check.py                       # rc 0, byte-identical to RESULTS.json
python -B -S iw_exact_check.py --mutant hermite-kernel      # rc 1
python -B -S iw_exact_check.py --mutant degree-four         # rc 1
python -B -S iw_exact_check.py --mutant d3-coefficient      # rc 1
python -B -S iw_exact_check.py --mutant no-row-operation    # rc 1
python -B -S iw_exact_check.py --mutant minor-constant      # rc 1
```

Author runner at `742e72e`, from a `git archive` extraction: all 15 tests pass in both modes, all 10 mutants are
rejected, and the output matches the stored summary.

Python standard library only. These are exact identities. The continuum steps are the written arguments above.

## Not established here

- Factorial moments or shrinking multiple-witness collisions. This is the remaining D5 line.
- Elder selection, which D1 Theorem A covers separately.
- Numerical `C`, `s_0` or `r_*`.
- Any STATUS, PROOF_INDEX or GRAPH transition.
- Organizational independence, since all lanes share one account.
