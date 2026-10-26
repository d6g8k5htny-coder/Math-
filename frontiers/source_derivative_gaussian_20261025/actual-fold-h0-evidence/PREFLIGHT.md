# Actual torus → old typed ElderTrap → ordinary H0: next-leaf preflight

26 October 2026. Read-only research preflight by OpenAI/Codex `/root/torus_h0_conversion_preflight`, delegated by `/root`. Only this report is written. No build, test, kernel invocation, cache/source/config mutation, commit, external post, or subagent dispatch was performed. Root retains contract, registration, implementation routing and publication ownership. Scientific effect NONE.

## Decision

The next useful leaf is **one actual singular-H0 interval direct summand on the same literal product AddCircle torus, under the same actual `sourceGapLaw` and existing sample cutoffs**. There is no additional geometric or global-Morse premise needed for this leaf. The current `TorusTrapData` supplies every hypothesis of the old proved `elderTrap_of_boundary`, which constructs the old typed `TorusFiltration.ElderTrap`; `elderDirectSummand` then constructs the interval and complement.

The remaining work is a small typed conversion and actual-law composition, plus the uncovered engineering task of composing the old H0 modules using narrow imports at the existing pin. It is not a new ridge proof, compact-Morse proof, H0 comparison proof, or interval-splitting proof. A theorem merely assuming an `ElderTrap`, conditional Morse certificate, or desired summand as a final premise would miss this reachable actual-law endpoint.

The exact interval is `[-b, -(b-k*r^3))` in increasing parameter `t=-height`, with length `k*r^3>0`. This supplies an ordinary-H0 summand and its excluded death endpoint. It does not identify the canonical Morse-labeled maximum/saddle partner, an exhaustive barcode, or a weighted parent theorem.

## Completed evidence carried forward

Workspace guidance at `/workspace/AGENTS.md` applies: completed, applicable verification is reusable; a new agent/session/handoff does not justify replay. New checks must name the actual changed scope. Provider-distinct review/process requirements stay separate from completed mathematical evidence.

The delegated frozen input is:

- `frontiers/source_derivative_gaussian_20261025/SourceActualFoldTorus.lean`, 17,840 bytes, SHA-256 `d2ca01d1f881852372c371215c30216bee7d917fdf2eaafbbd097f8c840e20c6`.
- Its retained `/workspace/scratch/actual-fold-torus-construct/runs/strict-003/receipt.json` records strict compilation exit 0; the sole `kernel-001/receipt.json` records standard own-module checker exit 0; `INVENTORY.json` records all 50 owned constants, classified, with only `propext`, `Classical.choice`, `Quot.sound`; `controls-002/receipt.json` records exit 0. These records were read and reused, not replayed.
- Retained torus object identity: `/workspace/scratch/actual-fold-torus-construct/build/SourceActualFoldTorus.olean`, 733,480 bytes, SHA-256 `9dd9d93e12ddb685ece1348b0699045b7e57b362cb48eaa54ac4373ddb9fd6e9`, from `SOURCE_OBJECT_IDENTITIES.json`. Root's recorded source-cut handoff there is `33a305a35312eca7fbfd04a4ed4f5269db69b97c`; this report performs no new source-cut validation.

The old elder package's completed evidence is in:

- `frontiers/asymmetric_elder_bridge_20261017/historical-results/LOCAL_FORMAL_EXECUTION_RESULT.json` and `LOCAL_FORMAL_EXECUTION_REPORT.md`.
- `review/NONAUTHOR_ELDER_BRIDGE_REVIEW.json`: `ACCEPT_SCOPED`, no must-fix findings, actual separate OpenAI/Codex nonauthor, source exposure disclosed, organizational/provider-distinct credit zero.
- Historical final serial process exited 0 on 17 October. Eight old modules have actual standard own-constant kernel replays: `SuperlevelBar`, `ClosedSuperlevel`, `OrdinaryH0`, `ElderClearance`, `ElderClearanceControls`, `ElderInterval`, `ElderIntervalControls`, `ElderBridge`. The 49 distinct printed targets used only standard3; that old named-target census is explicitly not an exhaustive generated-constant census. Three substantive negatives and nine anonymous interval examples already have their recorded execution credit.

These old results remain established on their displayed assumptions. Original header comments saying `NOT_RUN` or historical `PENDING` do not erase later bound receipts. Their historical macOS arm64 artifact custody does not itself establish current Linux artifact availability or new narrow-import composition. A pending institutional/provider-distinct process requirement does not turn these proofs into unverified mathematics.

## Exact old interfaces and conversion

Repository-relative old source paths:

| Module | Source | Principal role |
|---|---|---|
| `ClosedSuperlevel` | `companions/torus_filtration_20261011/ClosedSuperlevel.lean` | Actual closed superlevels, inclusion maps, path-component quotient, singular-H0 filtration |
| `OrdinaryH0` | `companions/torus_filtration_20261011/OrdinaryH0.lean` | Actual Mathlib singular H0 naturally compared with `ZerothHomotopy` coproducts |
| `ElderInterval` | `frontiers/asymmetric_elder_bridge_20261017/ElderInterval.lean` | Old typed trap, interval, section, retraction, direct sum |
| `ElderBridge` | `frontiers/asymmetric_elder_bridge_20261017/ElderBridge.lean` | Boundary-data constructor and geometric H0 join |
| `ElderClearance` | existing qualified `inputs/elder/ElderClearance.lean` | Arbitrary-space strict separation/threshold facts; old Euclidean C263 specialization |

The old source-bound graph records these identities; no mathematical revalidation or fresh hash campaign was performed here:

| Old module | Bytes | SHA-256 |
|---|---:|---|
| `ClosedSuperlevel` | 8,088 | `90d1481b75d9c6d14e462c3fbf0bf7c7cdd0efb9eaad68d6732400658753b1c2` |
| `OrdinaryH0` | 19,803 | `3d6b0d6b53413c484b1d010bccf0d53ae7f75becb2d747868f22dbd673fe0a88` |
| `ElderInterval` | 16,006 | `3dab19342c307f6b70f4fa05ac913b4ead083742a56408db71b45276c0acb9ab` |
| `ElderBridge` | 3,683 | `6b0be1116f6b357b0ffbda202c572c27c2788b98bee639e228375a5ebeea1fa9` |
| `ElderClearance` | 5,866 | `d3d78472881059546402218cc77792eeef00755c222bb02499d69abd3b5cd57e` |

`ElderInterval.lean:104` defines, for arbitrary `X : Type u` with topology and `g : X → ℝ`:

```lean
structure ElderTrap (g : X → ℝ) (M P : X) (m d : ℝ) (D : Set X) : Prop where
  death_lt_birth : d < m
  maximum_height : g M = m
  older_height : m < g P
  maximum_inside : M ∈ D
  older_outside : P ∉ D
  height_ceiling : ∀ x ∈ D, g x ≤ m
  active_clopen : ∀ t, elderActive m d t →
    IsClopen {x : superlevel_set g t | x.val ∈ D}
  closed_path : JoinedIn (superlevel_set g (-d)) M P
```

Here `elderActive m d t := -m ≤ t ∧ t < -d`; `superlevel_set g t := {x | -t ≤ g x}`.

The exact old constructor is `TorusFiltration.elderTrap_of_boundary`, `ElderBridge.lean:30`:

```lean
(g : X → ℝ) (D : Set X) (m d : ℝ) (M P : X)
(hD : IsClosed D) (hboundary : ∀ x ∈ frontier D, g x ≤ d)
(hdm : d < m) (hMheight : g M = m) (hM : M ∈ D)
(hheight : ∀ x ∈ D, g x ≤ m) (hP : m < g P)
(γ : Path M P) (hγ : ∀ t : unitInterval, d ≤ g (γ t))
: ElderTrap g M P m d D
```

The current `SourceActualFoldTorus.TorusTrapData`, source line 124, maps to it without extra premises:

| Constructor argument | Existing `T : TorusTrapData g M P b d D` field |
|---|---|
| `hD` | `T.domain_closed` |
| `hboundary` | `T.frontier_bound` |
| `hdm` | `T.death_lt_birth` |
| `hMheight` | `T.maximum_height` |
| `hM` | `T.maximum_inside` |
| `hheight` | `T.height_ceiling` |
| `hP` | `T.older_height` |
| `γ`, `hγ` | existential witness from `T.closed_path` |

Thus the minimum convenient generic new declaration is a theorem with type

```lean
TorusTrapData g M P b d D → TorusFiltration.ElderTrap g M P b d D
```

whose proof consumes the old constructor. Eliminating `T.closed_path` into the old `Prop` is legitimate. For a term-valued direct-sum constructor, use a noncomputable witness choice, or package its existence in `Nonempty`; no measurable path/domain/older-point selection is required for the proposed a.e. existence theorem.

The equivalent direct field conversion uses existing `T.older_outside` and `T.strict_trace`, and `elderTrap_closedTrace_isClopen g D d t T.strict_trace ht.2`; its closed-path field is the supplied `γ` with `neg_neg` simplification. That route duplicates no hard proof, but importing and calling `elderTrap_of_boundary` best preserves the accepted interface lineage. Both routes need the old H0 branch because the typed trap itself resides in `ElderInterval`, not the reused H0-free `ElderClearance`.

The existing H0 consumers require only an actual coefficient field:

```lean
elderSection T : elderInterval K b d ⟶ H
elderRetraction T : H ⟶ elderInterval K b d
elderSection_retraction T : elderSection T ≫ elderRetraction T = 𝟙 _
elderDirectSummand T :
  H ≅ elderInterval K b d ⊞ kernel (elderRetraction (k := K) T)
```

where `H := superlevel_h0Filtration g (ModuleCat.of K K)`. `elderBoundaryDirectSummand`, `ElderBridge.lean:55`, combines the same constructor and direct sum in one existing definition. The old declarations use a common universe `u` for `X` and `K`; a first actual-torus theorem can simply take `(K : Type) [Field K]` (including `ℚ`, `ℝ`, `ZMod 2`) rather than introduce a gratuitous universe-lift obligation.

No maximum uniqueness, nondegenerate Hessian, index saddle, global MorseDistinct, local contractibility, local path connectivity, compactness, or path-component=connected-component theorem is required by these typed interfaces. Even continuity of `g` is not required by the H0 split once its trap is supplied. The arbitrary-space constructor only needs the displayed topology and geometry. The actual torus field is already continuous anyway.

`elder_clopen_path_iff` descends the clopen-domain indicator along actual paths to `ZerothHomotopy`. Its use of path-component inclusion into connected components is an always-valid one-way fact; it does not require their equality. The old singular H0 computation is the path-component computation on arbitrary spaces. This is why the much larger compact-Morse local-path-connectivity adapter is unnecessary here.

## Meaningful minimum actual-law leaf

The current strong input is `SourceActualFoldTorus.sourceGapLaw_actual_torus_trap_clearance`, source line 289. It derives the explicit box, retained path and trap internally under `sourceGapLaw hL r b k`. Reuse its same `δ`, same event, same `U,z` witnesses. Do not replace its hypotheses by supplied normalized/raw pins, supplied ridge data, a desired trap, or an H0 certificate.

A clean proposed public conclusion, for fixed `(K : Type) [Field K]`, is the following interface shape. This is a specification sketch, not compiled implementation:

```lean
∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
  ∀ k₀ : ℝ, 0 < k₀ → ∀ r : ℝ, 0 < r → r < δ →
    ∀ b k : ℝ, k₀ ≤ k → ∀ᵐ sample ∂sourceGapLaw hL r b k,
      let T := sourceT k₀ sample
      let κ := sourceKappa r k sample
      r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
        (∃ C : ℝ ⥤ ModuleCat K,
          Nonempty
            (superlevel_h0Filtration (actualTorusField hL sample)
                (ModuleCat.of K K) ≅
              elderInterval K b (b-k*r^3) ⊞ C)) ∧
        strictClearanceSet (actualTorusField hL sample)
            (torusProjection 2 L (endpointM r)) = Iio (b-k*r^3) ∧
        strictClearanceDeath (actualTorusField hL sample)
            (torusProjection 2 L (endpointM r)) = b-k*r^3
```

The declared surrounding parameter remains `{L : ℝ} (hL : L ≠ 0)`. The hL-only `δ` remains before `k₀,r,b,k`, and the original sample and signed period remain unchanged. No probability estimate for the two numerical cutoffs is claimed by this leaf.

An additional, still-small theorem can retain the literal `z`, image box and converted old `ElderTrap`, with `C` exactly the old retraction kernel. That exposes the actual maps, while the simpler public theorem above existentially hides their unneeded choices. Existence of a complement is a genuine theorem about the actual singular-H0 filtration, not a renamed geometric certificate or a conditional restatement of the split.

The proof composition is finite: obtain the existing `δ`; enter its existing a.e. event; apply the already derived cutoffs; unpack `U,z` and the torus trap; convert it through `elderTrap_of_boundary`; choose `C := kernel (elderRetraction convertedTrap)` and the old `elderDirectSummand`; retain the already proved strict cut/death equalities. There is no new analytic argument.

For actual H0 death interpretation, the old `elderDifference_map_dead` proves `[M]-[P]` maps to zero at all parameters `t ≥ -(b-k*r^3)`; `elderDifference_projection` makes it nonzero on active fibers over the field; `elder_control_birth` includes `-b`, and `elder_control_death` excludes the death endpoint. Ordinary individual point classes remain nonzero. These are already proved old claims, not new test obligations.

The old `elderBoundary_death_eq` and `elderTrap_death_eq` have literal carrier `superlevelBar_E n` and cannot be instantiated with `SourceTorus 2 L`. The current polymorphic `strictClearanceDeath` is the actual torus real supremum and already equals `d`; it is the right torus companion to the old H0 interval endpoint. No quotient equivalence, path lift, period change, or redefinition of the Euclidean C263 API is necessary for this leaf. Claiming the old Euclidean death declaration itself now has a torus instance would be false.

## Dependency and import composition

Observed old graph:

```text
ClosedSuperlevel → Mathlib
OrdinaryH0      → Mathlib, ClosedSuperlevel
ElderInterval   → OrdinaryH0
ElderBridge     → ElderClearance, ElderInterval
ElderClearance  → SuperlevelBar
```

The current source package already has the qualified narrow `SuperlevelBar` and exact old `ElderClearance` under the unique `inputs/elder` root. Its `lakefile.toml` registers `SuperlevelBar`, `ElderClearance`, `ReusedCompactFrontier` there. It does not register `ClosedSuperlevel`, `OrdinaryH0`, `ElderInterval`, `ElderBridge`; the current default targets end at `SourceActualFoldDeath`, with the frozen torus module's own qualified artifact retained in scratch. Root owns future registration and cache custody.

A bounded presence-only scan of `/workspace` found current `SuperlevelBar.olean` and `ElderClearance.olean` only in `/workspace/scratch/actual-fold-clearance-inputs/build`, and no matching H0/interval/bridge artifacts. This does not establish that historical oleans do not exist elsewhere. Current torus and upstream artifacts exist under their retained scratch/build paths and production caches as recorded by their owners; reuse them by custody rather than relaunching their checks.

The smallest support extension is four old module copies, totaling 47,580 original bytes, under one unique source-root resolution. Preserve declaration/proof bodies; adapt only import headers needed for the new environment. Do not copy `SuperlevelBarField`, `Specifications.Field`, broad old `TorusTopology`, compact-Morse source copies, or full cap analysis. They are not dependencies of the selected endpoint and would introduce unnecessary name/axiom/interface risk. Do not install a second same-name `SuperlevelBar` alongside the qualified narrow copy.

At the existing Lean `v4.34.1` / Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612` pin, the following actual narrow library entrypoints were inspected in source:

- `Mathlib.AlgebraicTopology.SingularHomology.HomologyZero`: publicly imports the simplicial H0 computation, singular homology basic, and TopCat zeroth homotopy. It defines the exact existing `TopCat.singularHomology₀Iso` and augmentation used by old `OrdinaryH0`.
- `Mathlib.Algebra.Category.ModuleCat.Biproducts`: publicly imports `ModuleCat.Abelian` and short-complex ModuleCat; the latter supports the required homology environment. `ModuleCat.Abelian` imports module kernels/limits and supplies the abelian instance. An explicit extra `ModuleCat.Abelian` import may therefore be redundant, but is harmless.
- `Mathlib.CategoryTheory.Abelian.FunctorCategory`: supplies abelian functor-category structure and publicly imports preadditive functor-category and functor-category finite limits. This is an available robust way to obtain the kernel/biproduct functor environment. A smaller imports-only choice via the corresponding preadditive/limits modules may suffice; no minimality-by-elaboration claim is made here.
- `Mathlib.Tactic.Linarith`, `Mathlib.Tactic.NormNum`, `Mathlib.Tactic.Abel` for the old source's actual tactics, plus the real topology/order definitions and path-component/clopen facts needed by `ClosedSuperlevel` and `ElderInterval`. Current source's existing narrow real/topology imports may cover some, but each standalone support module should declare its actual needs rather than rely on the eventual consumer's imports.

Concretely: replace `ClosedSuperlevel`'s umbrella with finite singular-homology/zeroth-homotopy + real-topology + tactic imports; replace `OrdinaryH0`'s umbrella with `HomologyZero` and its category needs; explicitly import the ModuleCat/functor-category/tactic environment in the interval branch where needed, retaining all old bodies. `ElderBridge` can retain its exact two imports and complete body. The exact sufficient finite union remains an **uncovered import-elaboration obligation**; this read-only stage does not certify a proposed list or claim an observed OOM. Cached old umbrella oleans would still carry the transitive umbrella, so retrieving them alone does not resolve that composition requirement.

A natural new consumer module `SourceActualFoldH0` would import `SourceActualFoldTorus` and `ElderBridge`, with no H0 imports added upstream to the frozen source-law geometry module. A generic conversion and one actual-law theorem are enough; no new large record or parallel H0 implementation is warranted.

## Genuine missing obligations and excluded stronger endpoints

| Claimed endpoint | What is still missing now |
|---|---|
| Old typed `ElderTrap` on this torus, actual-law theorem | No geometric premise. New conversion and new actual-law composition are not yet implemented. Old H0 source-root/import composition is not yet qualified in this environment. |
| One actual singular-H0 interval/complement, exact endpoints | The same finite implementation/composition obligations; actual field instance is supplied by the theorem. No global Morse or uniqueness premise. |
| Literal old Euclidean C263 death on the torus carrier | A type-level mismatch, not a hidden hypothesis to assume. Use current polymorphic torus strict supremum instead. A separate spatial quotient/path-lift equivalence would be needed only if the stronger identity to old Euclidean definitions were demanded. |
| Canonically selected old `Lifetime.SuperlevelBarInterface.ElderPartner` / `IsFiniteBar` at pinned `M,S` | Formal local Hessian/inertia typing; literal global `IsMorseDistinct` under the exact every-target raw conditional law; a bound intrinsic Lifetime interface and its identification with the actual H0 elder semantics; quotient-distance/nonidentification for the literal candidate pair and coherent representative transport. Death level alone is insufficient. |
| Quantitative weighted Parent A/B in Lean | Actual measurable elder event, every-target conditioned genericity/semantics, source-bound weighted numerator and positive lower normalizer joins, mark/frame quantifiers, and for B actual once-counted Campbell/Rice density/Jacobian/version composition. The one H0 summand supplies none of these probability/counting conclusions automatically. |

The **formal** canonical gap must not be confused with a new conventional mathematical gap. The existing actual conventional application at `actual-adaptive-elder-application/PROOF.md` already supplies the needed source reasoning: §4 applies the old H0 trap; §5 gives explicit finite-supported kernel directions for the actual every-target posterior, residual Gaussian decomposition, remote Sard/one-/two-point area and endpoint-Hessian density to establish conditional Morse/distinct values; §8 gives the intrinsic Lifetime/H0 interpretation and once-counting; later sections give actual planar A/B. Its handoff explicitly says these claims are conventional and produce no Lean A/B or conditional-Morse implementation. Reuse those completed source/proof checks under their actual evidence; any source-specific/provider-distinct review still pending is a separate process item. This preflight does not re-audit those arguments or call their process-pending label an unproved mathematical premise.

In particular the accepted compact-Morse adapter under `frontiers/compact_morse_elder_adapter_20261018/` is an existing scoped conventional proof of a different route: from supplied smooth periodic Morse maximum to trap. It has `ACCEPT_SCOPED_CONVENTIONAL` and no new Lean implementation. Its finite-critical-set and critical-level local-path-connectivity work is needed when the trap must be recovered from general Morse geometry; current explicit torus `TorusTrapData` has already bypassed those prerequisites. Do not reopen or formalize that larger route just to obtain this next interval.

The names `conditionalMorseDistinct`, `globalMorseDistinct`, `weightedParent` are useful obligation labels in this handoff; exact-name searches did not locate current Lean declarations with those names in this source slice. The literal interface is `UniversalLaw.Spec.Lifetime.IsMorseDistinct` and the given-record `SuperlevelBarInterface.elderPartner_iff`, `inputs/Lifetime.lean:318,355`. That clause explicitly requires smoothness, periodicity and `IsMorseDistinct`, then characterizes partner by maximum type, saddle type, nonessentiality and death equality. `IsFiniteBar` at line 368 adds the candidate-pair/positive-gap requirements. Neither this given record nor a similarly named conditional record is automatically the actual H0 filtration.

## Verification boundary for a later authorized implementation

No additional verification was run here. The specific changes that would warrant later bounded checks are (1) the import-only support successors in this Linux/pinned environment, (2) the new conversion and actual-law constants, and (3) their registration/identity joins. Retain source bodies and import-only diffs with old identities. Compile only necessary missing successor artifacts after resolving imports; reuse already applicable clearance, torus and upstream artifacts. The root's established new-module strict/own-module/exhaustive-inventory/control contract can then apply to the genuinely new module.

Do not rerun old eight-module kernels, controls or old mathematical review to manufacture freshness. Do not extend the old 49-target named census into a fictitious exhaustive claim. An inventory/axiom check of genuinely new constants should bind their actual transitive dependencies and require standard3; a textual absence of `axiom` is not enough. Importing a broad given-interface or a second module copy is not a substitute for identifying the right old definitions. Provider-distinct process, hosted current-commit registration checks, and scientific acceptance remain separate from this bounded mathematical composition.

The finite recommendation to root is therefore: preserve the frozen torus module; route four import-only support copies under one root; implement generic `TorusTrapData → ElderTrap`; export the same-law a.e. actual singular-H0 interval/complement and retain current exact torus strict death; stop before canonical partner and weighted-parent closure. There is no need for another mathematical permission request or an additional conditional certificate.

Standing owner mandate and delegation, read alongside current workflow and repo guidance:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

Carrying these canonical links does not establish that a future recipient has read them.
