# Nonauthor analytic review: direct planar elder lower bound and local window multiplicity (Math-#116)

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes, premises, `STATUS`,
`PROOF_INDEX`, `GRAPH`, the candidate registry or any author source. It records verdicts on candidates
C1 and C2 of `reviews/candidates_pending_20260928/CANDIDATES.md`. Integration is a separate act.

## Object

| Field | Value |
|---|---|
| Objects | OA-ELDER-LOWER-DENSITY-GAP-20260928-v1 and OA-WINDOW-MULTIPLICITY-LOCAL-20260928-v1 (OpenAI / ChatGPT) |
| Branch / head | `chatgpt/window-multiplicity-laws-20260928` / `0507e3a1dbd3dede84cbeb805947c70aa16ebc36` ([Math-#116](https://github.com/d6g8k5htny-coder/Math-/pull/116)) |
| `ELDER_LOWER_AND_DENSITY_GAP.md` | Git blob `aaefc8da9668e819591dd9db0b34442394f2362e`, 10229 B, SHA256 `8ce05a43bde8e0d718f09e2da1ffe75d3ec5893489254afdbf5b58b602cdba0c` |
| `LOCAL_MULTIPLICITY.md` | Git blob `b5c18aac5529c5f975ee5bb056b304debafc6697`, 13100 B, SHA256 `e6272e8709835ca6290fecb7034fa84832dde08c3c4cc990a48b8019e89e7c8d` |
| Consumed, already on main | [LP] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d…`): §1 selector, §8 maximin, §§9–11 ledger, Theorem A. [IW] `frontiers/intermediate_window_20260928/PROOF.md` (blob `f53a527c…`): (I5). [RM] `frontiers/remote_window_20260924/PROOF.md` (blob `b383bfcc…`): frame and (11). |
| Request | [Owner comment 5877622700](https://github.com/d6g8k5htny-coder/Math-/pull/116#issuecomment-5877622700) |

## Provenance

| Field | Value |
|---|---|
| Reviewer | Anthropic Claude, Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3` |
| Relation | Different provider from the OpenAI author. Same GitHub account as every lane, so no organizational independence is claimed. |
| Exposure | I read both modules in full, the #116 README, SOURCE_MAP and PUBLICATION records, and LP §§1, 8–11. I wrote the #106 nonauthor review of LP Theorem A and the §9 repair, the #109 review of [IW], and the #110 remote-collision proof [RC]. The upper halves of (E4), (E11) and (L1) consume objects I reviewed or wrote, so for those halves this review is **not** independent of its inputs. The direct lower halves (E2) and (L1)-lower consume none of them. |
| Author code | The author's `algebra.py` is absent from the PR tree, as `PUBLICATION.json` discloses. **I did not run it and do not claim any execution of it.** |
| Independent checks | `elder_lower_exact_check.py` is my own exact-rational suite, written from the markdown. It checks only finite identities. Every Gaussian step below was argued by hand and is not replaced by those checks. |

## Verdicts

The lower result (E2) is judged separately from the parent-dependent (E4) and (E11), as requested.

| Interface | Verdict |
|---|---|
| (E1) ordinary maximin elder definition and the path obstruction | **ACCEPT**. It is LP §8's definition verbatim; see §1. |
| (E5)–(E6) three-segment path, min `-7k/32`, end `+17k/64`, `k/64` margins | **ACCEPT**. Hand-derived; exact check `PATH_*`. |
| (E7) = (L6)–(L8) pinned normal form, including `-aZ/8` | **ACCEPT**. Hand-derived; exact check on a generic degree-6 field with the pins solved. |
| (L9)–(L11) ten-jet Schur floor through `r = 0`; box mass `>= c r` | **ACCEPT**; see §3. |
| (L12)–(L13) `C^4` control **after** conditioning on the physical jets | **ACCEPT**; see §4. |
| (L5), (L14) `W_r >= c r^4`; full `Z_r <= C r^2`; (E8)/(L15) ledger `r·r^4/r^2` | **ACCEPT**; see §5. |
| **Theorem E1, (E2)–(E3)**: `1 - p_r >= c r^3`, d = 2 | **ACCEPT** at its stated existential scope. |
| **Corollary E2, (E4)**: `c r^3 <= 1 - p_r <= C r^3` | **ACCEPT** as a composition with LP Theorem A, accepted at existential scope in [Math-#106](https://github.com/d6g8k5htny-coder/Math-/pull/106). |
| (E9)–(E11) compact-window loss `Θ(ℓ^{2/3})` | **ACCEPT** as a composition with LP §§9–11 and (E4); see §6. |
| **Theorem L, (L1)**: `c r^3 <= Q^W(A_r) <= Q^W{N_r >= 2} <= C r^3` | **ACCEPT**. The lower bound is direct. The upper bound uses the merged (I5). |
| (L2), (L3) | **ACCEPT** |
| §7, (L16) Bernoulli comparison `TV = h` | **ACCEPT**. Hand-derived; checked exactly on random finite laws. |

No defect was found. Notes N1–N5 below record observations that strengthen or delimit the text without changing it.

---

## §1 — the obstruction (E1) and why it suffices

LP §8 defines the ordinary superlevel death height of a local maximum `M` as the maximin `(E1)`, with the empty
supremum for a global maximum. On the generic locus the elder partner of `M` is the unique critical point at height
`d_f(M)`. `S` has height `f(S)`, and critical values are almost surely distinct. So `d_f(M) > f(S)` forces the partner
to differ from `S`. A single admissible path supplies that lower bound: it must end strictly above `f(M) = b` and stay
strictly above `f(S)`. No gradient-flow, separatrix or saddle-connection statement is used, and none is needed. The
event has positive probability, and the generic locus has full measure, so the intersection costs nothing.

## §2 — the cubic, the path and the normal form

**Cubic.** For `G_k = k(2X^3 - 3X/2 - 1/2 - 3Z^2/4 - XZ^2)`, `∇G_k = k(6X^2 - 3/2 - Z^2, -(3/2 + 2X)Z)`, and
`G_xx = 12kX`, `G_xz = -2kZ`, `G_zz = -k(3/2 + 2X)`. At `M_* = (-1/2,0)` the Hessian is `diag(-6k,-k/2)` (maximum,
det `3k^2`). At `S_* = (1/2,0)` it is `diag(6k,-5k/2)` (saddle, det `-15k^2`). The heights are `0` and `-k`. The
extra points solve `X = -3/4`, `Z^2 = 15/8`. There `G = k(-27/32 + 9/8 - 1/2) = -7k/32`, `G_zz = 0`, and
det `= -4k^2 Z^2 = -15k^2/2`. Also `|P_±|^2 = 9/16 + 15/8 = 39/16 < 4`.

**Path.** On `X = -3/4` the `Z`-terms cancel: `-3Z^2/4 - XZ^2 = 0`. So segment 2 is the level line `-7k/32`, and it
passes **through** the extra saddle `P_+` (`√(15/8) ≈ 1.369 < 9/4`). Segment 1 is
`g_1(v) = -3v^2/16 - v^3/32`, which is nonincreasing. Segment 3 has `g_3'(v) = (51 - 36v - 6v^2)/64 >= 9/64`. The
path minimum is `-7k/32` and the end value is `+17k/64`. With `‖F - G_k‖_∞ < k/64` on `B(0,3)` and the exact pin
`F(-1/2,0) = 0`, the path stays above `-15k/64 > -k/4` and ends above `k/4`. Physically, the path stays above
`b - kr^3/4`, ends above `b + kr^3/4 > b`, and `b - kr^3/4 - f(S) = 3kr^3/4`. This is (E3).

**N1 (level region).** Segment 2 runs along a level line through a saddle of `G_k`. Under perturbation, that line
tilts and the saddle moves. The argument never uses the level or the saddle: it only uses the strict `C^0` margin
`k/64`, which survives every sub-`k/64` perturbation. The author's remark that the proof "does not rely on that level
remaining exactly constant" is therefore correct, and it is the reason the argument works.

**Normal form (E7)/(L7).** Put `h = r/2`. Cubic Hermite interpolation of the axial data
`f(∓h) = b, b - kr^3` and `f_x(∓h) = 0` gives the leading coefficient `2k`, so `f_xxx(0) = 12k + O(rK)`. It also gives
`f(0) - b = -kr^3/2 + O(r^4 K)`. The half-sums and half-differences of the endpoint expansions of `f_x` and `f_z`
give `f_x(0) = -(r^2/8)f_xxx(0) + O(r^3K)` and `f_z(0) = -(r^2/8)f_xxz(0) + O(r^3K)`, with
`f_xx(0), f_xz(0) = O(r^2 K)`. After the rescaling `(f(rX,rZ) - b)/r^3`:

- `f_x(0) X/r^2` becomes `-3kX/2`.
- `f_z(0) Z/r^2` becomes `-aZ/8`.
- The cubic terms become `2kX^3`, `(a/2)X^2Z`, `(β/2)XZ^2` and `(c/6)Z^3`.
- `f_zz(0) Z^2/(2r)` becomes `(s/2)Z^2`.
- Every other term is `O(rK)` in `C^2(B(0,3))`.

This is (L6)–(L7). The `-aZ/8` term is exactly the `f_z(0)` contribution, so dropping it breaks both transverse
gradient pins at order one. The exact check solves the six pins on a generic degree-6 field and confirms
`F - P = O(r)` identically in the free coefficients. The `drop-aZ-over-8` mutant is rejected.

## §3 — the ten-jet floor through `r = 0` and the box mass (L9)–(L11)

At `r = 0` the endpoint frame is `U_0 = (f, f_x, f_xx, f_xxx, f_z, f_xz)` at the midpoint. Appending
`J = (f_zz, f_xxz, f_xzz, f_zzz)` gives all `1 + 2 + 3 + 4 = 10` planar jets of order `<= 3`, each exactly once.
A null combination `Σ c_α ∂^α f(0)` would make the polynomial `Σ c_α (iξ)^α` vanish on the whole dual lattice
`(2π/L)Z^2`, because every periodized Gaussian Fourier weight is positive. A nonzero polynomial of degree `<= 3`
cannot vanish on a two-dimensional lattice, so the covariance is positive definite. The divided-difference frame `U_r` is continuous in `r` up to `0` ([RM] §2, LP §3), and frames range
over compact `O(2)`. Hence the joint covariance of `(U_r, J)` has a uniform floor `λ_* > 0` and a uniform ceiling for
`0 <= r <= r_1`.

By the Schur complement, `J | U_r = v_r` has covariance at least `λ_*` and mean `Cov(J,U)Σ_U^{-1} v_r`. That mean is
bounded because `v_r` is bounded. Its Gaussian density is therefore bounded below by some `ρ_* > 0` on any fixed
compact set. The target box (L10) lies in such a set. Its volume is `(2εkr)(2εk)^3 = 16ε^4k^4r` (exact check), so
`Q_r{J ∈ B_r} >= 16ρ_* ε^4 k_-^4 r`.

The `r` comes only from the **physical** `f_zz` width `εkr`. Normalizing `f_zz/r` would cancel that factor
illegitimately. The author's warning about this is correct.

## §4 — `C^4` control after the rare restriction (L12)–(L13)

Condition on the joint vector `V = (U_r, J)` at a target `(v_r, j)` with `j ∈ B_r`. The regular conditional field is
`F + Cov(F,V)Σ_V^{-1}((v_r,j) - V)`, where `F` is an unconditioned copy. The kernel is real-analytic, and the
observations are divided differences of order `<= 3` (averages of derivatives). So each coefficient function
`Cov(F(·),V_i)` has a uniformly bounded `C^4` norm, and `Σ_V^{-1}` is uniformly bounded by §3. The targets are bounded.
Therefore
`E[‖f‖_{C^4}^p | V = (v_r,j)] <= C_p(1 + E‖F‖_{C^4}^p + E|V|^p)`, uniformly. Choose `K` by Markov so the conditional
probability of `{‖f‖_{C^4} <= K}` is at least `1/2` at **every** target. Integrating over the box gives
`Q_r{J ∈ B_r, ‖f‖_{C^4} <= K} >= (c_J/2) r`.

This is the correct order of operations. Subtracting a fixed unconditioned tail from an event of mass `O(r)` would
fail.

**N2 (constants).** The dependency chain is acyclic. `ε` fixes the box and `c_J(ε)`. `K` is uniform over all targets
with `ε <= 1`. `r_*` is then chosen from `ε` and `K`. The `C^0` gap between `P` and `G_k` on `B(0,3)` on the box is at
most `εk(9/2 + 111/8 + 27/2 + 9/2) < 37εk`, so `ε < 1/4800` suffices for a `k/128` share of the `k/64` budget.

## §5 — tilt and normalizer (L5), (L14), (E8)

`F(X,Z) = (f(rX,rZ) - b)/r^3` gives `∇²f = r ∇²F`. In `d = 2`, each physical determinant is `r^2` times the scaled one.
On the event, the scaled pinned Hessians are `C^2`-close to `diag(-6k,-k/2)` and `diag(6k,-5k/2)`, so both indices
persist. With the author's floors `3/2 k^2` and `15/2 k^2`, `W_r >= (45/4)k_-^4 r^4` (exact check: weight `45k^4` and
floor `45/4`).

For the full normalizer, `f_x(M) = f_x(S) = 0` gives `∫_0^1 f_xx(M + t r e_1) dt = 0`, so `|f_xx(M)| <= r‖f‖_{C^3}`.
Likewise `f_z(M) = f_z(S) = 0` gives `|f_xz(M)| <= r‖f‖_{C^3}`. Hence
`|det H_M| <= 2r‖f‖_{C^2}‖f‖_{C^3}` and the same holds at `S`, so `W_r <= C r^2 (1 + ‖f‖_{C^3})^4`. The uniform `Q_r`
moments then give `Z_r <= C_Z r^2`. `Z_r > 0` because the event above has positive probability. The normalizer is
the **full** `E_{Q_r} W_r`, not a restricted one. The ledger is `r · r^4 / r^2 = r^3` (exact check, `weight-power`
mutant rejected).

## §6 — composition (E4), (E9)–(E11)

(E4)'s upper half is LP Theorem A, `1 - p_r <= C r^3` uniformly over `B × K × O(d)`. It is accepted at existential
scope in [Math-#106](https://github.com/d6g8k5htny-coder/Math-/pull/106), merged at `5eba8f7`.

(E9) is LP (10.2) verbatim: `A_r = 12 π_r(v_r) Z_r/r^2`, with no factor `1/2`. LP (11.1) gives
`r dr/dℓ = (1/3)k^{-2/3}ℓ^{-1/3}` (exact check `radial_jacobian_r_dr`). Multiplying by `1 - p ≍ r^3 = ℓ/k` gives the
integrand order `ℓ^{2/3}k^{-5/3}` (exact check `loss_exponent_*`). The lower half uses (E2) and `inf A_r > 0`. The
upper half is LP §11's display.

LP §§8–15 interfaces are accepted by the
[D1-A–E review](https://github.com/d6g8k5htny-coder/main/issues/63#issuecomment-5841570965). The §9 Borel repair is
accepted in #106 Part II.

**N3 (sharpness of Theorem A in d = 2).** (E4) makes Theorem A's `r^3` rate sharp in order for `d = 2`, uniformly on
the compact marks. This **supersedes** the remark in my #106 review, where sharpness was restricted to the (6.1)/(6.2)
matrix relaxation. That restriction remains correct for the relaxation statement. The Gaussian rate itself is now
shown sharp by the direct event, not by the relaxation. Consequently LP's `O(ℓ^{2/3})` selection-density loss cannot
be improved to `o(ℓ^{2/3})` in `d = 2`. Nothing is said about `d > 2` or about the leading constant.

## §7 — local multiplicity (L1)–(L3), (L16)

Choose disjoint closed disks about `P_±` inside `B(0,2)`, away from `M_*` and `S_*`. By the implicit function theorem
applied to `∇G_1` at nondegenerate zeros, there is a `C^2` neighborhood with one saddle per disk and heights in
`(-1, 0)`. Positive scaling by `k` preserves critical points and indices, scales heights by `k` and determinants by
`k^2`. So the neighborhood is uniform over `[k_-, k_+]`, and on the §3–§5 event (with the smaller `ε` for `C^2`) both
witnesses exist with physical heights in `I_r`. This gives the lower half of (L1) with the same `r · r^4/r^2`
ledger.

The upper half is `1{N >= 2} <= N/2` together with (I5) summed over indices. (I5) is merged
([Math-#107](https://github.com/d6g8k5htny-coder/Math-/pull/107) and my review in [Math-#109](https://github.com/d6g8k5htny-coder/Math-/pull/109)). (L2) follows from
`N(N-1) >= 2·1{N >= 2}`, and (L3) from dividing (L1) by `Q^W{N >= 1} <= C r^3` (exact check `counting_inequalities`).

For (L16), write `σ` for the singleton submeasure, `η` for the mean measure on `{N >= 2}`, `h = η(S)` and
`α = P(N >= 2)`. Then `Law Ξ - Ber(μ)` has signed masses `h - α >= 0` on the empty stratum, `-η` on singletons and
`α` on multiples. The total variation is `2h`, so the probability TV is exactly `h`, and `2α <= h <= m_r`. Because `-η` has one
sign, its variation is its mass, so the check may aggregate the singleton stratum. It verifies `TV = h` on 1000+
random exact count laws with a nontrivial multiple stratum. The `tv-half` mutant is
rejected.

**N4 (the #110 scope).** (L1)–(L2) show that a torus-wide `O(r^5)` factorial bound is false. This confirms that the
fixed-radius `D_ρ` restriction in the merged remote-collision proof ([Math-#110](https://github.com/d6g8k5htny-coder/Math-/pull/110))
was necessary, not a proof convenience. There is no conflict: `A_r` occurs within distance `O(r)` of the pins.

**N5 (one box, two conclusions).** The same jet box, intersected with the smaller `C^2` neighborhood, carries both
(E3) and `A_r`. This does not mean every two-saddle configuration defeats the elder pairing, and the source does not
claim that (LOCAL §8: "`A_r` by itself does not determine elder pairing").

## Checks run

```
python3 -B -S elder_lower_exact_check.py                          # rc 0, stdout == RESULTS.json
python3 -B -O -S elder_lower_exact_check.py                       # rc 0, byte-identical
python3 -B -S elder_lower_exact_check.py --mutant drop-aZ-over-8  # rc 1
python3 -B -S elder_lower_exact_check.py --mutant hessian-sign    # rc 1
python3 -B -S elder_lower_exact_check.py --mutant path-endpoint   # rc 1
python3 -B -S elder_lower_exact_check.py --mutant weight-power    # rc 1
python3 -B -S elder_lower_exact_check.py --mutant tv-half         # rc 1
```

Python standard library only. The workflow `.github/workflows/elder-lower-review.yml` verifies the packet tree against
`SOURCE_FILES.json`, replays both modes and requires every mutant to be rejected.

## Not established here

- `REMOTE_PAIR_LAW.md`, `REMOTE_DISTANCE_MOMENTS.md`, `HEIGHT_MARKS.md` (C3–C5). The owner routed these to Grok/Harper.
- Numerical `c`, `r_*`, or any leading constant. The results are existential.
- `d > 2`, a shrinking gap mark, a growing torus, all-height counts, or a global second factorial moment upper bound
  (C6).
- A runnable reproduction of the author's suite. It is absent from the tree and was not run.
- Organizational independence: all lanes share one GitHub account.

A non-Claude review of §§3–5 (the Gaussian steps) remains welcome before any status integration.

## Revision history

- **v1**, reviewing head `0507e3a`: initial packet.
