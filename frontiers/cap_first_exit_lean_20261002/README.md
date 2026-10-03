# Cap first exit in Lean: the topological global step of D1 component III

**Object:** `CAP-FIRST-EXIT-LEAN-20261002-v1`. **Author:** Anthropic / Claude, Claude Code session `017Mi3hx…`.
**Kind:** a Lean 4 / Mathlib formalization, with its own source and execution gate. **Scientific effect:** NONE. No
register, catalog, STATUS, PROOF_INDEX, GRAPH or `formal/` scope change. **Same GitHub account as every lane: zero
organizational-independence credit.** The author will not merge.

## What is proved

The audit of D1 named one step as load-bearing: the deterministic implication from the local good event to "`S` is
the *global* elder partner of `M`". It asked for that step to have a completely independent derivation.

That implication has two parts:

- **Analytic part (CAP §§2–5, second pass L1–L20).** From `G_r`, construct a cap `C` and a ridge with three
  properties:
  - (C1) `f ≤ b` on `C`;
  - (C2) `f ≤ s` on the frontier of `C`, with only `S` attaining `s` (C2⁺);
  - (C3) a path from `M` to an older point `z`, `f(z) > b`, along which `f ≥ s`.
- **Topological part (L21–L22).** From (C1)–(C3), deduce `M`'s global maximin level and its superlevel death level.

This packet kernel-checks three things:
- the whole topological part;
- the one-variable and assembly steps of the analytic part (L13, L16, L17, L19, L20, in `ridge_capHyp`);
- since v1.5, L1–L2 and the slice steps:
  - L1–L2, the Hermite bound `g(a) − g(c) ≤ m(c − a)³/12`, which under the normalization `b − s = r³/6` forces `m ≥ 2`;
  - since v1.6, L3–L4: the transverse Hessian's increments from its third-derivative bounds `m` (mean value inequality), then the slice strong concavity `δ = λ − 5rm` from SP's Hessian bound at `M`;
  - L5, the transverse-gradient bound, from the third-derivative bound `m`;
  - L7, the transverse maximum and its uniqueness; since v1.7 also the existence of the ridge `h` (compactness) and its strict differentiability (Mathlib's implicit function theorem plus uniqueness of the critical point);
  - L8, the ridge bound;
  - L11's chain rule;
  - L18, the curved side.

  These are derived from L4's output, the strong concavity of each transverse slice. `ridge_capHyp_sp` takes SP's hypotheses with `m ≥ 2` assumed. `ridge_capHyp_normalized` derives `m ≥ 2` from SP's normalization (gap exactly `r³/6`, pins critical, third derivatives bounded by `m`). `ridge_capHyp_H1` (v1.6) also derives `hconc` and `δ > rm(8m − 5)` from SP's hypothesis (H1) `λ > 8rm²`.

Since v1.8, `ridge_capHyp_source` composes these steps from SP's source data on a collar `[−2r − ε, 2r + ε] × B̄(0, 2r)` of `D` (`0 < ε ≤ r/2`). The data are the derivatives of `f` with the third-derivative bounds `m`, (H1), the critical pins and the gap `r³/6`. From them it proves:
- that a ridge `h` exists, and `h(∓r/2) = 0`;
- L8's interior bound, and the implicit-function regularity of `h` on `[−2r, 2r]`;
- L11, and then (C1)–(C3) and (C2⁺) on the cap.

Since v1.9, `ridge_capHyp_C3` also derives L12's `hconv`, from the second and third derivatives of `f` on the collar:
- L6: chord slopes of L5's convexity pair give `‖w'‖ ≤ m · max(|x|, r/2) ≤ 2mr`.
- L9: the differentiated ridge equation gives `‖h'‖ ≤ 2s + 2s²`, with `s = mr/δ`.
- L12: `F' = D²f[(1, h'), (1, 0)]` is the maximum of `ζ ↦ D²f[(1, ζ), (1, ζ)]`, so `F' − x/4` is monotone with no second derivative of `h`. With SP's constants, `F'' ≥ 7/4 − 48/121 · (3 + 72/121 + 576/14641) > 1/4`.

Since v2.0, `ridge_capHyp_C4` also derives the one analytic input that `ridge_capHyp_C3` still takes, SP's L4 bound `f_xxx ≥ 7/4` on `D = [−2r, 2r] × B̄(0, 2r)`:
- L2's second statement: some point of the pin interval has `f_xxx ≥ 2`. This comes from a one-sided Hermite bound, by contradiction (`third_deriv_exists_two`).
- L4: (H2) `rn ≤ 1/20`, with a bound `n` on the derivative of `f_xxx`, gives `f_xxx ≥ 2 − 3rn ≥ 7/4` on the collar (`fxxx_lower`).

So the hypotheses of `ridge_capHyp_C4` are SP's (H1), (H2), the critical pins, the gap `r³/6` and the derivative data with the bounds `m` and `n`. No step of L1–L20 remains a hypothesis.

In the topological theorems, `X` is any topological space, and nothing is assumed about `f` outside `C` except along the
single ridge path.
- The core theorems use only (C1)–(C3): no metric, smoothness, Morse, compactness or probability hypothesis. Their
  separation steps do not even use continuity of `f`.
- The two older-peak theorems, `older_peak` and `elder_death_level_peak`, add compactness, local connectedness and
  continuity of `f`. All three hold on the torus.

| Lean declaration | Statement |
|---|---|
| `CapHyp f C M z b s` | (C1)–(C3) as one `Prop` structure |
| `CapHyp.maximin_isGreatest`, `maximin_eq` | `d_f(M) = sup_γ inf_t f(γ t) = s`, attained (L21) |
| `CapHyp.elder_merge_iff_closed` | for every `h`: the component of `M` in `{f ≥ h}` contains a point `> b` **iff** `h ≤ s` |
| `CapHyp.elder_merge_iff_open` | for every `h`: the component of `M` in `{f > h}` contains a point `> b` **iff** `h < s` |
| `CapHyp.elder_death_level` | the largest such `h` exists and equals `s` (L22's death level) |
| `CapHyp.path_through_saddle` | under (C2⁺): every path from `M` to a point `> b` inside `{f ≥ s}` passes through `S` |
| `CapHyp.saddle_cut`, `toy_saddle_cut` | under (C2⁺) and `M ≠ S`: `M` lies in its own component of `{f ≥ s} \ {S}`, so the statement is not vacuous, and that component has no point `> b`. `S` is a cut point at the death level. The toy shows this on concrete data |
| `CapHyp.older_peak` | on a compact, locally connected space with continuous `f`: for every `h ≤ s`, `M`'s component in `{f ≥ h}` contains a local maximum `p` of `f` with `f p > b` that is highest in the component (the older class) |
| `CapHyp.elder_alive` | with `b = f M`: for every `h > s`, `M` is a highest point of its component in `{f ≥ h}` |
| `CapHyp.elder_death_level_peak` | compact, locally connected, continuous, `b = f M`: the largest level at which `M`'s component contains a strictly higher local maximum exists and is `s` |
| `CapHyp.congr` | exterior invariance: agreement on `closure C` and along one ridge preserves every hypothesis, hence every conclusion |
| `CapHyp.map`, `CapHyp.map_saddle` | transport: if the lift `f ∘ e` satisfies (C1)–(C3) (and (C2⁺)) on a compact cap `C`, then `f` satisfies them on `e '' C`. Needs only `e` continuous and open and the target Hausdorff; no injectivity |
| `torusCover`, `CapHyp.toTorus` | the covering map `ℝ^d → (ℝ/Lℤ)^d` is continuous and open, so a cap verified for the periodic lift in any coordinate frame transfers to the torus with the same `b`, `s`. No embedding radius is needed for this step |
| `frontier_cylinder`, `isCompact_cylinder` | `frontier ([a, c] × B̄(0, R)) = {a, c} × B̄(0, R) ∪ [a, c] × S(0, R)`: exactly the end faces and curved side estimated in L17–L19; the cylinder is compact |
| `ridge_profile` | L13, L16, L17 and L20 in one variable. Assume, on `[−2r, 2r]`, that `g' = F`, `F(∓r/2) = 0` and `F − (x + r/2)(x − r/2)/8` is convex. Then `g ≤ g(−r/2)` on `[−2r, r/2]` and `g ≥ g(r/2)` on `[−r/2, 2r]`. Also `g(−2r) ≤ g(−r/2) − 9r³/32` and `g(2r) ≥ g(r/2) + 9r³/32`: the exact face integrals |
| `ridge_capHyp`, `ridge_saddle_strict` | (C1)–(C3), and (C2⁺), on the cylinder `[−2r, r/2] × B̄(0, 2r)`, derived from the multi-variable outputs, each assumed only where SP supplies it: L7 (transverse maximum, unique for (C2⁺)), L11 (`g' = F` on `[−2r, 2r]`), L12 (`F'' ≥ 1/4` as convexity on `[−2r, 2r]`), L18 (curved side), and the gap `b − s < 9r³/32` |
| `strongConcave_le_of_hasFDerivAt`, `slice_le` | the engine: a `δ`-strongly concave `φ` with derivative `L` at `p ∈ K` satisfies `φ y ≤ φ p + L(y − p) − (δ/2)‖y − p‖²` on `K`. At a critical point this is L7, `f(x, y) ≤ g(x) − (δ/2)‖y − h(x)‖²` |
| `slice_ridge_bound` | L8: `δ‖h(x)‖ ≤ ‖w(x)‖`, where `w(x)` is the slice derivative at `y = 0` |
| `slice_curved` | L18: on `‖y‖ = R` the slice is `< s` once `‖w‖ ≤ ω ≤ Rδ`, `g(x) ≤ b` and `2δ(b − s) < (Rδ − ω)²` |
| `slice_hasFDerivAt`, `ridge_hasDerivAt`, `ridge_inputs_of_joint` | L11: with the ridge equation `∂_y f = 0` along `y = h(x)`, `g' = ∂_x f(x, h(x))`. Joint derivatives and a differentiable `h` supply `hh`, `hg` and the slice critical points |
| `ridge_capHyp_of_slices` | (C1)–(C3) and (C2⁺) on the cylinder, with the transverse hypotheses of `ridge_capHyp` replaced by L4 (`hconc`), the critical points `h(x) ∈ B̄(0, 2r)`, L5 (`‖w‖ ≤ ω`) and `2δ(b − s) < (2rδ − ω)²` |
| `convexOn_add_node`, `two_node_bound`, `slice_gradient_bound` | L5: if `u` vanishes at `a < c` and `|u''| ≤ m` (weak form), then `|u(x)| ≤ (m/2)|(x − a)(x − c)|`, inside and outside `[a, c]`. For the slice derivatives `w(x)` at `y = 0`, this gives `‖w(x)‖ ≤ (m/2)|x² − r²/4| ≤ 2mr²` on the cap |
| `ridge_capHyp_sp` | the cap from SP's normalized hypotheses: `m ≥ 2` (L2), `δ > rm(8m − 5)` with `hconc` (L4), the weak third-derivative bound on `w` (L5), critical points with `h(∓r/2) = 0` (L7), L11, L12 and gap `≤ r³/6`. `ω`, `hωr` and `hcurv` are derived |
| `spToyF`, `spToy_capHyp` | `x³/3 − x/4 − 12y²` (`m = 2`, `δ = 24 > 22`, gap `r³/6`) meets every hypothesis of `ridge_capHyp_sp` |
| `hermite_gap_le`, `hermite_m_ge_two` | L1–L2: if `g' = G` vanishes at `a < c` and `|G''| ≤ m` (weak form), then `g(a) − g(c) ≤ m(c − a)³/12`. At the gap `r³/6` on `[−r/2, r/2]`, this forces `m ≥ 2` |
| `ridge_capHyp_normalized`, `spToy_normalized` | the cap with `m ≥ 2` derived from the normalization (L1–L2) instead of assumed; `spToyF` meets every hypothesis |
| `strongConcaveOn_of_hessian` | second-order condition: `H y v v ≤ −δ‖v‖²` for the second derivative on a convex set gives `δ`-strong concavity |
| `hessian_increment` | L3: derivative bounds `m` on `∂_x H` (along `y = 0`) and on `D_y H` (along rays) give `‖H(p) − H(M)‖ ≤ m(|Δx| + ‖Δy‖)` |
| `transverse_hessian_le`, `slices_strongConcave` | L4: `H(M) ≤ −λ` and those increments give `H ≤ −(λ − 5rm)` on the cap, so each slice is `(λ − 5rm)`-strongly concave |
| `ridge_capHyp_H1`, `h1ToyF`, `h1Toy_capHyp` | the cap from SP's (H1) `λ > 8rm²` with Hessian data in place of `hconc`; `x³/3 − x/4 − 20y²` (`λ = 40 > 32`) meets every hypothesis |
| `slice_critical_unique`, `slice_critical_exists`, `ridge_exists` | L7 existence: a `δ`-strongly concave slice with `‖∂_y f(x, 0)‖ < δ · 2r` has exactly one critical point, and it lies in the open ball; a ridge map `h` exists |
| `isInvertible_of_negDef`, `ridge_hasStrictFDerivAt`, `ridge_differentiable` | L7 regularity: a negative definite transverse Hessian is invertible, and the implicit function of `∂_y f = 0` agrees with `h`, so `h` is strictly differentiable on `[−2r, 2r]` with `h' = −(∂_y G)⁻¹ ∂_x G` |
| `h1Toy_ridge_differentiable` | every hypothesis of `ridge_differentiable` at `h1ToyF` (`h = 0`, `G = −40y`, `δ = 40`, `U = (−3, 3)`), listed in the proposition itself, and its conclusion |
| `hessian_increment_D`, `transverse_hessian_le_D`, `slices_strongConcave_D` | L3–L4 on SP's full domain: on the collar `x ∈ [−2r − ε, 2r + ε]`, `0 < ε ≤ r/2`, the increment is at most `3r + 2r = 5r` (SP: `9r/2 < 5r` on `D`), so every slice is `(λ − 5rm)`-strongly concave |
| `ridge_capHyp_source` | the composed source route (v1.8). From the source data on the collar it proves that a ridge exists on `(−2r − ε, 2r + ε)`. For any such ridge with L12's `hconv`, it proves `h(∓r/2) = 0` and the cap with `M = (−r/2, 0)` and `S = (r/2, 0)`. Inside: L5 gives `‖w‖ ≤ 3mr² < 2rδ`, L8 gives the open ball, `DG ∘ inr = H` is negative definite, the IFT gives `h'`, and then L11 and `ridge_capHyp_H1` follow |
| `h1Toy_source` | `h1ToyF` meets every hypothesis of `ridge_capHyp_source` (`ε = 1/2`, joint derivative `(x² − 1/4, −40y)`); the theorem gives its ridge and its cap |
| `convex_deriv_sign`, `two_node_deriv_bound`, `slice_gradient_deriv_bound` | L6 (v1.9). If `u` vanishes at `∓r/2` and `|u''| ≤ m` holds in the weak form, then `|u'(x)| ≤ m · max(|x|, r/2)`. Outside the pins the chord through them has slope `0`; between them the chord to a pin and L5 give `mr/2`. For the slice derivatives at `y = 0` this is SP's `‖w'‖ ≤ 2mr` on `[−2r, 2r]` |
| `schur_max` | L9 and the Schur maximum. Take a bilinear `Q` on `ℝ × E` with `δ`-negative-definite transverse part, and `η` with `Q (1, η) (0, ·) = 0`. Then `δ‖η‖ ≤ ‖Q (1, 0) (0, ·)‖`, and `Q (1, η) (1, η) = Q (1, η) (1, 0)`. If `Q` is symmetric, `Q (1, ζ) (1, ζ) ≤ Q (1, η) (1, η)` for every `ζ` |
| `ridge_second_identity`, `transverse_hessian_eq` | the differentiated ridge equation `D²f[(1, h'), (0, ·)] = 0` (L11's first identity), and `H = D²f[(0, ·), (0, ·)]` |
| `trilinear_lower`, `l12_lower`, `l12_constants`, `l9_arith`, `dx_grad_increment` | L12's correction terms, `f_xxx − m((1 + ‖b‖)²(1 + ‖a‖) − 1)`. SP's constants: `m ≥ 2` and `δ > rm(8m − 5)` give `7/4 − m((1 + u)³ − 1) ≥ 1/4` for `u = 2s + 2s²`. Also L9's arithmetic, and L3 in `y` for `∂_x ∇_y f` |
| `ridge_hconv` | L12 as `hconv`. Along the ridge, assume `D²f` is symmetric with negative-definite transverse part, `‖h'‖ ≤ u`, and `s ↦ D²f(s, h s)[(1, b), (1, b)]` has derivative `≥ 1/4` for `‖b‖ ≤ u`. Then `F − (x + r/2)(x − r/2)/8` is convex on `[−2r, 2r]`. For `η = h'(x₁)`: `F'(x₂) − F'(x₁) ≥ D²f(x₂)[(1, η), (1, η)] − D²f(x₁)[(1, η), (1, η)] ≥ (x₂ − x₁)/4` |
| `ridge_source_facts`, `ridge_capHyp_C3` | the cap from SP's `C³` source data (v1.9). It assumes `ridge_capHyp_source`'s data, `D²f` and the third derivatives on the collar, the block bound `m`, and `f_xxx ≥ 7/4` on `D`. It proves that a ridge exists, that `h(∓r/2) = 0`, and the cap with `M = (−r/2, 0)`, deriving L12's `hconv` rather than assuming it |
| `h1Toy_C3` | `h1ToyF` meets every hypothesis of `ridge_capHyp_C3`: `D²f = diag(2x, −40)`, and only `f_xxx = 2` is nonzero among the third derivatives. The theorem gives its ridge and its cap without a supplied `hconv` |
| `hermite_gap_le_concave`, `third_deriv_exists_two` | L1 from the concave half alone (`g''' ≤ m` weakly gives `g(a) − g(c) ≤ m(c − a)³/12`), and L2's second statement (v2.0). If `g'''` is continuous on the pin interval and the gap is `r³/6`, then `g''' ≥ 2` somewhere there. Otherwise its maximum `M' < 2` would give a gap `≤ M'r³/12 < r³/6` |
| `fxxx_lower` | L4's `f_xxx ≥ 7/4` (v2.0): if `‖D f_xxx‖ ≤ n` on the collar, `f_xxx(x₀, 0) ≥ 2` and (H2) `rn ≤ 1/20`, then `f_xxx ≥ 2 − 3rn ≥ 7/4` (SP: `2 − 5rn`) |
| `ridge_capHyp_C4` | the cap from SP's hypotheses (v2.0): `ridge_capHyp_C3` with `f_xxx ≥ 7/4` replaced by a derivative `Φ4` of `f_xxx` with `‖Φ4‖ ≤ n` and (H2) `rn ≤ 1/20` |
| `h1Toy_C4` | `h1ToyF` meets every hypothesis of `ridge_capHyp_C4` (`f_xxx = 2` constant, `n = 0`). The theorem gives its ridge and cap with neither `hconv` nor `f_xxx ≥ 7/4` supplied |
| `sp_curved_side_constants` | SP's constants (`m ≥ 2`, `δ > rm(8m − 5)`, `ω ≤ 2mr²`, gap `r³/6`) satisfy `ω ≤ 2rδ` and the curvature condition |
| `ridgeToy_joint`, `ridgeToy_slices` | the ridge toy (`δ = 2`, `ω = 0`) meets every input of the slice route, which re-derives (C1)–(C3) and (C2⁺) |
| `ridgeToy_capHyp`, `ridgeToy_saddle_strict` | SP's normalization at `r = 1` (`f = x³/3 − x/4 − y²`, gap exactly `r³/6`) satisfies every ridge hypothesis, so they are jointly satisfiable |
| `toy_capHyp`, `toy_death_level` | a concrete instance on `ℝ`, showing the hypotheses are satisfiable and the theorems are not vacuous |
| `toy_needs_C1`, `toy_needs_C2`, `toy_needs_C3` | proved counterexamples: for each of (C1), (C2), (C3), Lean proves that the other two hold, that this one fails, and that the maximin conclusion fails |

The two engines of the proof are:

- `path_meets_frontier`: a path that leaves `C` meets `frontier C`.
- `preconnected_subset_of_frontier_disjoint`: a preconnected set that meets `C` and avoids `frontier C` lies inside
  `C`.

The second is what lets the component statements avoid path-connectedness and continuity of `f`.

`saddle_cut` gives a topological reason why the death happens at `S`. The source instead identifies `S` through a
Morse-theoretic step: distinct critical values make the merging critical point unique. `saddle_cut` does not need
that step.

## What is not proved here

This packet does not formalize:

- the source data themselves. Since v2.0 every analytic step of L1–L20 is proved: L1–L12, L13 and L16–L20, with L7's
  existence, uniqueness and regularity of `h`. `ridge_capHyp_C4` takes, as hypotheses, the derivatives `Df`, `DG`,
  `H`, `D2f`, the third derivatives and the derivative of `f_xxx`, with the bounds `m` and `n`, on the collar
  `[−2r − ε, 2r + ε] × B̄(0, 2r)`. SP has `f ∈ C⁴` near `D` and bounds the
  third derivatives on `D`. On a thin enough collar the bound `m + η` holds by continuity, and (H1) stays strict for
  small `η`; Lean does not prove this step;
- the match between the source's coordinates and the Lean objects: that SP's cap is `[-2r, r/2] × B̄(0, 2r)` in a
  frame `φ` and that SP analyses the periodic lift. The transport to the torus and the face list are themselves
  proved (`CapHyp.toTorus`, `frontier_cylinder`);
- the definition of the H0 superlevel persistence pairing itself: that the class born at a local maximum `M` dies at
  the largest level at which its component contains a strictly higher local maximum. On a compact, locally connected
  space Lean proves that this level is `s` (`elder_death_level_peak`); only the persistence-module bookkeeping is
  informal;
- L23, P §8, and every probabilistic statement (Theorem A, `Q^W(G_r^c) ≤ C r^3`).

So issue Math-#193's "D1 Lean / kernel formalization" remains **partially** unsupplied. [ALIGNMENT.md](ALIGNMENT.md)
maps every Lean statement to its source line and lists these interfaces.

## Running it

The package pins the same toolchain and Mathlib revision as `formal/`: Lean `v4.34.1`, Mathlib `d13f23b7`. It has its
own `lakefile.toml` and `lake-manifest.json`, and it neither imports nor alters `formal/`.

    python3 frontiers/cap_first_exit_lean_20261002/gate.py              # source gate (no Lean needed)
    python3 -m unittest discover -s frontiers/cap_first_exit_lean_20261002 -p 'test_*.py' -v
    cd frontiers/cap_first_exit_lean_20261002 && lake exe cache get && cd -
    python3 frontiers/cap_first_exit_lean_20261002/gate.py --execute    # build, replay, axioms, controls

The source gate checks:

- every file against `MANIFEST.json` (bytes and SHA-256), and the exact tree;
- the two pinned sources on main, by git blob;
- toolchain and dependency pins;
- that the only import is `Mathlib`;
- that no forbidden token (`sorry`, `axiom`, `native_decide`, `set_option`, …) appears outside comments;
- that the declared targets equal the manifest list.

`--execute` additionally:

- fails unless the running Lean is exactly the pinned release, and unless every dependency worktree is at its pinned
  revision with no staged, unstaged or untracked changes (checked before the build and again when the receipt is
  bound);
- rebuilds the package fresh;
- replays the module with `leanchecker`;
- prints the axioms of all 113 declarations, requiring exactly the manifest's report: each uses only `propext`,
  `Classical.choice`, `Quot.sound`;
- runs three negative controls (an injected `sorry`, a custom axiom, and `native_decide`). The audit must reject each.

The workflow `.github/workflows/cap-first-exit-lean.yml` runs all of this on pull requests that touch the packet.

A green run is kernel evidence for the displayed Lean statements, relative to Lean's kernel and the pinned toolchain.
It does not show that the statements say what the source says. That is the job of the alignment review requested
in [ALIGNMENT.md](ALIGNMENT.md), which must come from a non-Claude lane.
