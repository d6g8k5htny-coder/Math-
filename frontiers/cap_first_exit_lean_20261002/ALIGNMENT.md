# Alignment: Lean statements against the source lines

**Sources, pinned by git blob on main and checked by `gate.py`:**

| Source | Path | Role |
|---|---|---|
| SP | `reviews/d1_cap_elder_partner_second_pass_claude_20260930/REVIEW.md` | the line-numbered reconstruction of CAP §§2–5. L13, L16, L17 and L19–L22 are proved here. L7, L11, L12 and L18 enter `ridge_capHyp` as hypotheses. |
| CAP | `imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md` | the deterministic theorem that SP reconstructs |

The source setting (SP §2) is as follows:

- coordinates `(x, y) ∈ ℝ × ℝ^(d-1)`;
- pins `M = (-r/2, 0)` and `S = (r/2, 0)`;
- `b = f(M)` and `s = f(S) = b - r³/6`;
- the cap `C = [-2r, r/2] × B̄(0, 2r)`;
- the ridge `x ↦ (x, h(x))`.

## 1. Hypotheses

| Lean field | Lean statement | Source | Notes for the reviewer |
|---|---|---|---|
| `CapHyp.mem` | `M ∈ C` | SP L16 (`M = (-r/2, 0)`, `-2r ≤ -r/2 ≤ r/2`) | |
| `CapHyp.ceiling` | `∀ x ∈ C, f x ≤ b` | SP L16 | Lean does not require `f M = b`. The source has it, but no conclusion needs it. |
| `CapHyp.frontier_le` | `∀ x ∈ frontier C, f x ≤ s` | SP L17 (left face), L18 (curved side), L19 (right face) | `frontier` is the topological frontier in the ambient space `X`. See interface I1. |
| `CapHyp.older` | `b < f z` | SP L17 (`g(2r) ≥ b + 11r³/96`), L20 | `z = (2r, h(2r))` |
| `CapHyp.ridge` | `∃ γ : Path M z, ∀ t, s ≤ f (γ t)` | SP L20 | The source ridge is the graph of `h` on `[a, 2r]`. Its minimum is exactly `s`, at `S`. Lean needs only `≥ s`. |
| `hS` (in `path_through_saddle`, `saddle_cut`) | `∀ x ∈ frontier C, x ≠ S → f x < s` | SP L19, "only `S` attains it" | Strict on the left face (L17) and on the curved side (L18). Equality on the right face only at `S`. |

## 2. Conclusions

| Lean theorem | Statement | Source | Notes |
|---|---|---|---|
| `CapHyp.barrier` | every path from `M` to a point `> b` has a point with `f ≤ s` | SP L21, first two sentences | "Whatever it does afterwards": no constraint on the path outside `C`. |
| `connectionLevels`, `CapHyp.maximin_isGreatest`, `CapHyp.maximin_eq` | `IsGreatest {m ∣ ∃ w γ, b < f w ∧ ∀ t, m ≤ f (γ t)} s`, and `sSup = s` | SP L21, `d_f(M) = s` | The set's supremum is `sup_γ inf_t f(γ t)`. For continuous `f`, `inf_t` is SP's `min_γ f`. SP has `f(γ(1)) > f(M)`; Lean has `> b`, which is the same since `b = f(M)` in SP. |
| `component_joined` | a path inside `U` puts its endpoint in `M`'s component of `U` | standard | |
| `CapHyp.component_separated` | if `U` misses `frontier C`, then `M`'s component of `U` has no point `> b` | SP L21 in component form | Proved by `preconnected_subset_of_frontier_disjoint`. No path-connectedness and no continuity of `f`. |
| `CapHyp.elder_merge_iff_closed` | `(∃ w ∈ connectedComponentIn {x ∣ h ≤ f x} M, b < f w) ↔ h ≤ s` | SP L22 (filtration `{f ≥ t}`) | |
| `CapHyp.elder_merge_iff_open` | the same with `{x ∣ h < f x}` and `h < s` | the open-superlevel convention | Supplied so either convention can be used. |
| `CapHyp.joinedLevels`, `CapHyp.elder_death_level` | `IsGreatest {h ∣ ∃ w ∈ cc{f ≥ h}(M), b < f w} s` | SP L22, "the largest `t` at which it contains a point of value `> b`, i.e. at `t = d_f(M)`" | Both halves of SP's "i.e." are proved: the largest such `t` exists and is `s`, and `s = d_f(M)`. See interface I2. |
| `CapHyp.path_through_saddle` | under `hS`, every path from `M` to a point `> b` inside `{f ≥ s}` passes through `S` | SP L19 + L21 | |
| `CapHyp.saddle_cut`, `toy_saddle_cut` | under `hS` and `M ≠ S`: `M ∈ connectedComponentIn ({f ≥ s} \ {S}) M`, and every point of that component has `f ≤ b` | replaces SP L22's "distinct critical values make it `S`" | A topological identification of the merge point. Together with `elder_merge_iff_closed` at `h = s`, removing `S` at the death level disconnects `M` from every older point. The membership conjunct rules out the vacuous case `M = S`; SP's pins are distinct (`-r/2 ≠ r/2`). No Morse hypothesis. |
| `isClosed_connectedComponentIn` | a connected component of a closed set is closed | standard | Not in Mathlib at the pinned revision; proved from `IsPreconnected.closure`. |
| `CapHyp.older_peak` | `[CompactSpace X] [LocallyConnectedSpace X]`, `Continuous f`, `h ≤ s` ⇒ `∃ p ∈ cc{f ≥ h}(M), b < f p ∧ IsLocalMax f p ∧ ∀ w ∈ cc{f ≥ h}(M), f w ≤ f p` | SP L22, "the older endpoint" | Compactness gives the maximum over the closed component. Local connectedness makes that maximum a local maximum of `f` on `X`: the `{f > h}`-component of `p` is an open neighbourhood inside the component. |
| `CapHyp.elder_alive` | `f M = b`, `s < h` ⇒ `∀ w ∈ cc{f ≥ h}(M), f w ≤ f M` | SP L22, the class is alive above `s` | No compactness needed. |
| `CapHyp.olderPeakLevels`, `CapHyp.elder_death_level_peak` | `IsGreatest {h ∣ ∃ p ∈ cc{f ≥ h}(M), f M < f p ∧ IsLocalMax f p} s` | SP L22, the death level | This is the elder rule's death level, stated with older local maxima instead of older points. |
| `frontier_image_subset` | `Continuous e`, `IsOpenMap e`, `T2Space X`, `IsCompact C` ⇒ `frontier (e '' C) ⊆ e '' frontier C` | I1 | No injectivity: if a preimage of a frontier point were interior to `C`, the open map would make the point interior to `e '' C`. |
| `CapHyp.map`, `CapHyp.map_saddle` | `CapHyp (f ∘ e) C M z b s` ⇒ `CapHyp f (e '' C) (e M) (e z) b s`; and (C2⁺) for the lift ⇒ (C2⁺) for `e S` | I1 | |
| `torusCover`, `torusCover_continuous`, `torusCover_isOpenMap`, `CapHyp.toTorus` | for any frame `φ : Y ≃ₜ ℝ^d`, a cap for `f ∘ torusCover L d ∘ φ` on compact `C` gives a cap for `f` on the torus `(ℝ/Lℤ)^d` | I1; SP §2's coordinates, "every frame" | The torus is `Fin d → AddCircle L`. |
| `frontier_cylinder`, `isCompact_cylinder` | `frontier (Icc a c ×ˢ closedBall 0 R) = {a, c} ×ˢ closedBall 0 R ∪ Icc a c ×ˢ sphere 0 R` for `a ≤ c`, `R ≠ 0`, in `ℝ × E` with `E` a real normed space; compact when `E` is proper | SP L16–L19 (`a = -2r`, `c = r/2`, `R = 2r`) | The three pieces are L17's left face, L19's right face and L18's curved side. |
| `convex_zeros_between`, `convex_zeros_left`, `convex_zeros_right` | a convex function vanishing at `a < c` is `≤ 0` on `[a, c]` and `≥ 0` outside | SP L13, L17 | Uses `ConvexOn.le_on_segment` and `ConvexOn.slope_mono_adjacent`. |
| `ridge_profile` | on `D = [-2r, 2r]`: `g' = F`, `F(-r/2) = F(r/2) = 0`, `ConvexOn D (F - (x + r/2)(x - r/2)/8)` ⇒ `g ≤ g(-r/2)` on `[-2r, r/2]`; `g(r/2) ≤ g` on `[-r/2, 2r]`; `g(-2r) ≤ g(-r/2) - 9r³/32`; `g(r/2) + 9r³/32 ≤ g(2r)` | SP L13 (sign pattern), L16 (ceiling along the ridge), L17 (both exact integrals `9r³/32`), L20 (ridge minimum) | SP states L12 as `F'' − 1/4 > 0`; Lean takes the weaker convexity of `F − q`. L17's integrals come from comparing `g` with `Q = x³/24 − r²x/32`, `Q' = q`. |
| `ridge_capHyp` | `CapHyp f C M z b s`, with `C = Icc (-2r) (r/2) ×ˢ closedBall 0 (2r)`, `M = (-r/2, h(-r/2))`, `z = (2r, h(2r))`, `b = g(-r/2)`, `s = g(r/2)` | SP L16, L17, L19, L20 | Hypotheses, all local as in SP: `hT` = L7's `f(x, y) ≤ g(x)` on `C`; `hg` = L11 on `[-2r, 2r]`; `hh` = continuity of `h` on `[-r/2, 2r]`; `hFa`, `hFc` = critical pins; `hconv` = L12 on `[-2r, 2r]`; `hside` = L18 (non-strict suffices); `hM` (`h(a) = 0` in SP); `hgap` (SP: `r³/6 < 9r³/32`). The ridge path does not need to stay in `C`. |
| `ridge_saddle_strict` | under `hTs` (the unique transverse maximizer, L7) and a strict `hside`, every frontier point other than `S = (r/2, h(r/2))` has `f < s` | SP L19, "only `S` attains it" | The left face is strict through `hgap`; the right face is strict through uniqueness. |
| `CapHyp.congr` | from `g = f` on `closure C` and along one ridge `γ₀`, `CapHyp g C M z b s` | the audit's exterior-invariance corollary (Math-#193 deliverable 2) | `closure C ⊇ C ∪ frontier C`. In SP, `C` is closed. |

## 3. Non-vacuity and necessity, proved in Lean

The toy model is `toyF x = max (-|x|) (x - 2)` on `ℝ`, with:

- the cap `[-2, 1]`;
- `M = 0`, `b = 0`;
- `S = 1`, `s = -1`;
- `z = 3`;
- the ridge `t ↦ 3t`.

The proved facts are:

- `toy_capHyp` and `toy_saddle_strict`: the toy satisfies (C1)–(C3) and (C2⁺).
- `toy_death_level`: the death level is `-1`.
- `toy_needs_C2`, at `s = -3/2`: Lean proves that (C1) and (C3) hold, that (C2) fails (`f(1) = -1 > -3/2`), and that
  the maximin level is not `-3/2`.
- `toy_needs_C1`, at `b = -1/2`: Lean proves that (C2) and (C3) hold, that (C1) fails (`f(0) = 0 > -1/2`), and that
  the maximin level is not `-1`. The witness is the constant path.
- `toy_needs_C3`, at `s = 5`: Lean proves that (C1), (C2) and `b < f(z)` hold, that no ridge exists (every path starts
  at `f(M) = 0 < 5`), and that the maximin level is not `5`.

Each necessity theorem is one conjunction, so it certifies its own premises, not only its conclusion.

`ridgeToy_capHyp` and `ridgeToy_saddle_strict` instantiate `ridge_capHyp` and `ridge_saddle_strict` at SP's normalization, with `r = 1`, `E = ℝ`, `f(x, y) = x³/3 − x/4 − y²`, `h = 0` and `F = x² − 1/4`. The gap there is exactly `r³/6`, so all ridge hypotheses are jointly satisfiable.

The toy lives on `ℝ`, which is not compact. So the older-peak theorems (`older_peak`, `elder_death_level_peak`) have
no concrete instance exhibited in Lean. Their extra hypotheses (compact, locally connected, continuous `f`) hold on the
torus.

The toy is one-dimensional, so its "saddle" `S = 1` is a local minimum, the index-`d−1` point for `d = 1`. The toy
illustrates the hypotheses; it is not a model of the planar cap.

## 4. Interfaces that stay informal

| | Interface | Where it is argued | Why it is outside this packet |
|---|---|---|---|
| I1 | Coordinates: SP's cap is `[-2r, r/2] × B̄(0, 2r)` in a frame `φ` of the periodic lift, and SP's "boundary" is the topological frontier. The transport to the torus (`CapHyp.toTorus`) and the face list (`frontier_cylinder`) are proved; the transport needs no embedding radius | SP §2 | Only the identification of SP's objects with these Lean objects remains. |
| I2 | Persistence bookkeeping: in H0 superlevel persistence with distinct critical values, the class born at a local maximum `M` dies at the largest level at which its component contains a strictly higher local maximum (the elder rule) | SP L22, P §8 | This is the definition of the elder pairing. On a compact, locally connected space, Lean proves that this level is `s` (`elder_death_level_peak`). Only the identification of the persistence module's pairing with that definition is informal. |
| I3 | The multi-variable analytic steps L1–L12 and L18, which supply `hT`, `hTs`, `hg`, `hFa`, `hFc`, `hconv`, `hside` and `hgap` of `ridge_capHyp` from `G_r` | SP L1–L12, L18; CAP §§2–5 | Hermite identity, increments, strong concavity, implicit function theorem, ridge identity, `F''` bound and curved-side estimate, with exact constants checked by SP's script, not in Lean. L13, L16, L17, L19 and L20 are proved in Lean from these outputs. |
| I4 | Theorem A, measurability, `Q^W(G_r^c) ≤ C r³` | P §§7–8, C1, G1 | probability |

## 5. Review contract

An alignment review should be written by a non-Claude lane (OpenAI/Codex, xAI/Grok, or another provider). Its record
names:

- the reviewer's provider and agent;
- the exact head commit;
- the `MANIFEST.json` SHA-256.

For each row of §§1–2, the record gives ALIGNED, MISALIGNED (with the corrected statement), or NOT ASSESSED. For each
row of §4, it says whether the interface is stated correctly.

A changed Lean source, toolchain or pin makes an earlier review stale. A same-provider read, including any Claude
read, gives zero independence credit. A build or merge is not an alignment review.
