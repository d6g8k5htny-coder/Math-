# Nonauthor analytic review: remote within-window height decoupling (Math-#120)

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes, premises, `STATUS`,
`PROOF_INDEX`, `GRAPH`, the candidate registry or any author source. It records verdicts. Integration is a
separate act.

## Object

| Field | Value |
|---|---|
| Object | OA-REMOTE-HEIGHT-DECOUPLING-20260928-v1 (OpenAI / ChatGPT) |
| Branch / head | `chatgpt/remote-height-decoupling-20260928` / `f3e16585338e4c4dc878df43f9117b1b3ed5a479` ([Math-#120](https://github.com/d6g8k5htny-coder/Math-/pull/120)) |
| `PROOF.md` | Git blob `4d7af587db20515955585732d8150d912c89c0e4`, 13747 B, SHA256 `67249f0311342beab7833cb60c3239d9888df96befda4fbae3ec29a66f8cd78e` |
| Consumed, already on main | [RM] `frontiers/remote_window_20260924/PROOF.md` (blob `b383bfcc…`): §§2–5, (2), (5), (8), (11), (12). [RC] `frontiers/remote_collision_20260928/PROOF.md` (blob `7b48a88e…`): Corollary D. Both blobs match main at `63857fe`. |
| Request | [Owner comment 5878357612](https://github.com/d6g8k5htny-coder/Math-/pull/120#issuecomment-5878357612), "especially (H7)–(H15)" |
| Prior review | OpenAI same-provider, source-exposed review [5344808206](https://github.com/d6g8k5htny-coder/Math-/pull/120#pullrequestreview-5344808206): no blocker. This record is the requested different-provider review. |

## Provenance

| Field | Value |
|---|---|
| Reviewer | Anthropic Claude, Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3` |
| Relation | Different provider from the OpenAI author. Same GitHub account as every lane, so no organizational independence is claimed. |
| Exposure | I read `PROOF.md` in full, its README, RECONNAISSANCE, SOURCE_MAP and `check.py`, RM §§1–6, and the OpenAI review above before writing this record. **I am the author of [RC]** ([Math-#110](https://github.com/d6g8k5htny-coder/Math-/pull/110)), whose Corollary D supplies `q_r <= C r^5 |E|`. I consumed RM there. So the probability slice (H18)–(H20) is not independent of my own earlier work. The analytic slice (H7)–(H15) consumes only RM. |
| Author code | Replayed from a `git archive` of `f3e1658`: `verify.py` passes all sources, 12 tests per mode, 5 mutants rejected per mode, and identical output pairs. |
| Independent checks | `height_exact_check.py` is my own exact-rational suite. It shares no code with the author's `check.py` and tests different objects, notably an exact finite-rank Gaussian regression model for (H7)–(H10). It does not replace the Gaussian arguments below. |

## Verdicts

| Interface | Verdict |
|---|---|
| (H7) exact pathwise identity `F_h - F_h' = (h - h') g` | **ACCEPT** |
| (H8) uniform `C^q` bound on `g` | **ACCEPT**, with note N2 |
| (H9) `V_r g = e_h`, so the ORIGINAL endpoint values and gradients of `g` vanish | **ACCEPT** |
| (H10) vector zero-average column bound `(r/2)‖D^3 g‖` | **ACCEPT** |
| (H11) Lipschitz endpoint and witness blocks, with no `1/r` loss | **ACCEPT**, and it is deterministic (N1) |
| (H12) `W_r/r^2 = F_d(K_M) F_(d-1)(K_S)` by positive congruence | **ACCEPT** |
| (H13) = RM (8) filtered-determinant Lipschitz bound | **ACCEPT** |
| (H14) product difference and moments; (H15) uniform `L` | **ACCEPT**. `Z_r` is independent of the witness height (§3). |
| (H16)–(H17) marked mean measure, variation `<= (d+1) L l^2 |E|/3` | **ACCEPT** |
| **(H1)** `O(r^3)` own-marginal factorization of the normalized mean | **ACCEPT** |
| (H18)–(H19) mixture, `a <= q`; **(H2)** with the factor two; **(H3)** | **ACCEPT** |
| **(H4)** physical mean `O(r^5)`, variance `O(r^8)` | **ACCEPT** |
| (H20), configuration-level `TV = ε`, measurable and randomized selectors | **ACCEPT** |
| §7 contact-profile compatibility; (H21) abstract `r^2` barrier | **ACCEPT**. It is correctly not claimed as Gaussian sharpness. |

No defect was found. Notes N1–N6 strengthen or delimit the text without changing it.

---

## §1 — (H7)–(H9): the regression direction and the original pins

The regression realization is affine in the target. So `F_h - F_h' = Cov(F(·),V_r) Σ_r^{-1}(a_h - a_h')`, and
`a_h - a_h' = (h - h') e_h`. That is (H7), pathwise and exact. It is one coupling, not an independence statement.

Applying the observation functionals to the deterministic function `g(z) = Cov(F(z),V_r) Σ_r^{-1} e_h` gives
`V_r[g] = Cov(V_r,V_r) Σ_r^{-1} e_h = e_h`. Differentiation commutes with covariance for this smooth field. So
`U_r[g] = 0`, `∇g(x) = 0` and `g(x) = 1`. For `r > 0`, `U_r` is an invertible linear re-expression of
`(f(M), ∇f(M), f(S), ∇f(S))`, with determinant `12 r^{-(d+3)}` in RM §2. Hence all `2(d+1)` original observations
of `g` vanish. That is (H9).

The owner's first falsification target therefore holds. The zero is a statement about the original values and
gradients, not a contact substitute.

**Exact check (finite-rank Gaussian model).** Take `F = Σ ξ_m φ_m` over all monomials of degree `<= 5` in the plane,
with independent `ξ_m ~ N(0, 1/(a!b!))`. At `x = (3/5, 2/7)` and `r ∈ {1/3, 1/7, 1/19}`, the direction `g` is computed
exactly. The suite confirms:

- `V_raw[g] = e_h`, including all six original pins.
- `g` is identical whether the pins are written raw or through RM's `U_r` rows (including the `12/r^3` row).
- For a rational `ξ`, `F_h1 - F_h2 = (h1 - h2) g` coefficientwise, and each `F_h` realizes every original target.

The `no-endpoint-pins` and `gradient-target` mutants fail these checks.

**N2 (what (H8) needs).** Cauchy–Schwarz bounds `|∂_z^α Cov(F(z),V_i)|` by `(Var ∂^α F(z) · Var V_i)^{1/2}`. So the
input is uniformly bounded **variances** of the divided-difference rows, not bounded raw coefficients: the fourth
row carries `12/r^3`. RM §2 supplies this through `U_r -> U_0` at second order in `L^2`. `Σ_r^{-1}` is uniformly
bounded on `O(d) × D_ρ` by compactness. The model is consistent with this: the coefficient sup-norm of `g_r - g_0`
is 1.50, 0.091 and 0.0057 at `r = 1/4, 1/16, 1/64`, a ratio of about 16 per factor 4 despite the `r^{-3}`
coefficient. Three observed ratios are consistent with `O(r^2)` but do not by themselves prove that asymptotic. The
proof is RM's analytic argument, which this observation does not replace.

## §2 — (H10)–(H12): no `1/r` loss in the endpoint columns

The gradient pins on `g` give `∫_0^r D^2 g(M + t u) u dt = ∇g(S) - ∇g(M) = 0`. Integrating by parts:

- `D^2 g(M) u = -(1/r) ∫_0^r (r - t) D^3 g(M + t u)[u,u] dt`
- `D^2 g(S) u = (1/r) ∫_0^r t D^3 g(M + t u)[u,u] dt`

Both are vector identities, so no common Rolle point is needed, and each gives the bound `(r/2) ‖D^3 g‖_∞`. That is
(H10).

The exact check verifies both identities, for the `xx` and `xz` entries, and the bound at both endpoints. The
`no-endpoint-pins` mutant breaks the identities **and** the bound. This shows the homogeneous gradient pins are what
remove the `1/r`.

With `α_i = f_uu(i)/r` and `β_i = ∇_⊥ f_u(i)/r`, the `h`-differences are `(h - h') g_uu(i)/r` and
`(h - h') ∇_⊥ g_u(i)/r`, each at most `(1/2)‖D^3 g‖ |h - h'|`. `A_i` and `H_x` change by `(h - h')` times bounded
second derivatives of `g`. That is (H11). The owner's second target holds: the column changes are
`O(r |h - h'|)` before the division by `r`.

**N1 (deterministic Lipschitz).** `g` is deterministic, so every difference in (H11) is a deterministic number
bounded by a deterministic `C|h - h'|`, for every `ω`. That is stronger than the text needs. Moments enter only
through the `max(‖·‖)^{d-1}` factors in (H14).

(H12): `H_i = D_r K_i D_r` with `D_r = diag(√r, I_{d-1})`. Sylvester's law preserves inertia, and
`det H_i = r det K_i`. So `F_j(H_i) = r F_j(K_i)` for every `j`, including the singular cases. The exact check covers
150 random rational instances in each of `d = 2, 3`, with the index computed exactly by Descartes' rule on the real-rooted
characteristic polynomial. The `unscaled-beta` mutant (no `√r` on `β`) fails.

## §3 — (H13)–(H15): filtered determinants, moments, and the normalizer

(H13) is RM (8), and the proof there is correct. If `X` has index `j` and `Y` does not, the segment from `X` to `Y`
contains a singular matrix `Z`. Then `|F_j(X) - F_j(Y)| = |det X - det Z|`, and `‖X - Z‖ <= ‖X - Y‖`,
`‖Z‖ <= max(‖X‖,‖Y‖)`. The determinant bound `|det X - det Z| <= n max^{n-1} ‖X - Z‖` uses `‖adj‖ <= ‖·‖^{n-1}`.

The exact check tests the implied Frobenius form on 300 random pairs and six forced index flips across a singular
matrix, with `ε` down to `10^-6`. The `indicator-only` mutant (the bare index indicator) fails on the flips. This
confirms that the Lipschitz quantity is the filtered determinant, as the text says.

(H14): write `T_h = F_d(K_M(h)) F_{d-1}(K_S(h)) F_j(H_x(h))` and apply
`|abc - a'b'c'| <= |a - a'||bc| + |a'||b - b'||c| + |a'b'||c - c'|`. Each difference is at most
`d max(‖·‖)^{d-1} C|h - h'|`. RM (5) gives uniform moments of all the matrices over the extra height pin, and Hölder
then gives `E|T_h - T_h'| <= C|h - h'|`. `E T_h` is the conditional expectation in (H5), because `F_h` has exactly the
conditional law given `Y_x = (0,h)`.

**Normalizer (owner's third target).** `Z_r = E_{Q_r} W_r` is an endpoint-only functional. It does not involve
`Y_x`, so it is independent of `h`, and RM (11) makes `r^2/Z_r` uniformly bounded. The density
`p_{Y_x|U_r=v_r}(0,h)` is Gaussian with uniformly positive covariance and bounded mean, so it and its `h`-derivative
are bounded. The product rule gives (H15) with `L` uniform over `x ∈ D_ρ`, marks, frames and small `r`. No
derivative of an indicator, and no differentiation under an unbounded expectation, is used.

**N3 (why the rate improves).** `R_{r,j}(x,·)` is `Θ(1)`, and it varies by `O(|h - h'|) = O(r^3)` across the window.
So the within-window density is flat to **relative** `O(r^3)`. The contact comparison in RM gives only `O(r)`, because
the finite-`r` spatial and index drift is common to all heights. The new proof avoids that drift by comparing at the
same `r`.

## §4 — (H16)–(H17) and (H1)

RM's height disintegration gives the density in `t` on Borel subwindows, so (H16) holds as an equality of finite
marked measures. By Jensen,

`∫_0^1 |R(b - lθ) - R̄| dθ <= L l ∫∫ |θ - t| = L l/3`.

The exact check confirms `∫∫ |θ - t| = 1/3`. It also checks the mean deviation `<= L/3` on 300 random piecewise-linear
Lipschitz profiles; the affine extremal case gives `L/4`, and the `lip-constant` mutant (`L/6`) fails.

The comparison measure `μ^Y ⊗ λ` has the same mass `m_r`. So

`TV <= (d+1) L l^2 |E| / (6 m_r)`,

and the RM lower bound `m_r >= c r^3 |E|` gives `O(r^3)`, with `|E|` cancelling. That is (H1).

## §5 — (H18)–(H20), (H2)–(H4), selectors

`a = E[N; N >= 2] <= E[N(N-1)] = q`, because `N <= N(N-1)` for `N >= 2`. The mixture identity gives
`TV(S, μ/m) = (a/m) TV(S, η/a) <= a/m`. The factor two in (H2) comes from two separate costs: the mixture, and the
change of marginal from `π_r` to `π_{r,1}`. (H3) needs only one of them. (H4) follows because `0 <= θ <= 1`, so TV
controls `E θ` and `E θ^2` and `|Var θ - 1/12| <= 3δ`. With `l = k r^3`, the errors are `l · r^2 = O(r^5)` and
`l^2 · r^2 = O(r^8)`.

(H20): `1{N >= 1} >= N - N(N-1)/2` and `1{N >= 2} <= N(N-1)/2`, so `ε <= q/(2m - q)`. The nonempty configuration law
is `(1 - ε)`·singletons + `ε`·multiples, and the two parts have disjoint supports, so its TV to the embedded `S_r` is
exactly `ε`. A deterministic or randomized selector agrees with `S_r` on `{N = 1}`, so its law is within `ε`.

All of these were checked on 300 random exact configuration laws with 8 marks and up to 3 points, plus one extremal
law with an equality case: the singleton at one mark and the pair on two others. That law gives equality in both
`TV(S, μ/m) = a/m` and `ε = q/(2m - q)`, so neither bound can be tightened in general. The mutants
`a-as-probability` (using `P(N >= 2)` in place of `a`) and `eps-over-2m` fail on it. Both a min-mark selector and the
uniform randomized selector satisfy the selector bounds.

## §6 — §7 compatibility and the (H21) barrier

`TV(S_r, π_E ⊗ λ) <= O(r^2) + TV(π_{r,1}, π_E) = O(r)`. The given premises only establish `O(r)` here. No lower
bound or optimal Gaussian profile rate is claimed. There is no conflict with (H1)–(H3).

The (H21) example was rebuilt exactly at `r = 1/2, 1/3, 1/10, 1/50`:

- The mean is exactly `m × Unif{A,B} × Unif(0,1)`.
- `q = a = r^5`.
- The singleton height TV is `r^2/(2(1 - r^2))`, which is at most `a/m`.
- The law is valid for `r <= 1/2`, and the TV exceeds `r^3` for `r <= 1/10`.

Within each height half the densities are constant, so bin-level TV equals the continuous TV. The example is
abstract. It shows that the two moment premises cannot give `O(r^3)`, and the text correctly does not claim a
Gaussian lower bound.

**N4 (consistency with #116).** On the whole torus, #116's LOCAL (L3) gives `P(N >= 2 | N >= 1) >= c_0`; see my
review in [Math-#123](https://github.com/d6g8k5htny-coder/Math-/pull/123). Here `ε = O(r^2)` only on `D_ρ`. The
two statements are consistent: the fixed-`ρ` restriction is exactly what separates them, and #120 claims nothing
global.

**N5 (dimension).** RM and RC Corollary D both hold for every fixed `d >= 2`, so #120's `d >= 2` scope is
supported. Constants depend on `d, L, ρ, B, K`.

**N6 (candidate C5).** #120 does not consume #116's `HEIGHT_MARKS.md`. It proves a different, own-marginal target.
Nothing here reviews C5.

## Checks run

```
python3 -B -S verify.py                         # author packet at f3e1658 (git archive): PASS, 12 tests, 5 mutants per mode
python3 -B -S height_exact_check.py             # rc 0, stdout == RESULTS.json
python3 -B -O -S height_exact_check.py          # rc 0, byte-identical
python3 -B -S height_exact_check.py --mutant M  # rc 1 for each of the nine mutants:
    no-endpoint-pins gradient-target unscaled-beta indicator-only lip-constant
    eps-over-2m a-as-probability p2-r6 var-l
```

Python standard library only. The workflow `.github/workflows/remote-height-review.yml` verifies the packet tree
against `SOURCE_FILES.json`, replays both modes and requires every mutant to be rejected.

## Not established here

- RM's own premises: the covariance floor, the moments (5) and the Kac–Rice formula (12). They are consumed as
  written, with RM's existing review status.
- Any `ρ -> 0`, global, `k -> 0`, unbounded-mark or random-domain statement. The text excludes all of these.
- Numerical `C`, `r_*`, or an optimal Gaussian rate.
- Organizational independence: all lanes share one GitHub account, and I wrote RC.

## Revision history

- **v1**, reviewing head `f3e1658`: initial packet.
- **v2**, responding to [owner comment 5879827321](https://github.com/d6g8k5htny-coder/Math-/pull/123#issuecomment-5879827321).
  Wording only; no verdict, check or source changes.
  - §6 no longer infers from an `O(r)` upper bound that the contact-profile rate "cannot be better". The given
    premises establish only `O(r)`, and no lower bound is claimed.
  - N2 now presents the three finite-rank ratios as consistent with `O(r^2)`, not as a proof of it.
