# Lean statement specifications (2026-10-10)

Scientific effect: **NONE**. Organizational-independence credit of this packet: 0 (Anthropic /
Claude, delegated AI work). Alignment status of every statement: `PENDING_INDEPENDENT_REVIEW`.
Formal progress of every declaration here: `specified`. No claim, premise, obligation or
disposition changes because this packet exists, builds, or is green in CI.

## What this packet is

A **statement-only** Lean 4 + Mathlib package. Each module declares, as `def … : Prop` and
interface `structure`s, the mathematical objects and results that the byte-pinned Layer 0 texts
under `sources/` describe. Two independent stages hold the modules to "statements only". The
source scan (`check.py`, no Lean) refuses `theorem`, `lemma`, `example`, `instance`, `axiom`,
`sorry` and the rest of its lexical list as whole tokens of comment-stripped code, refuses string
literals, guillemet names, `#` commands and attributes outright, requires every command keyword
at column 0 (so `open … in` and indented commands are refused), refuses `section` and `variable`
(no module needs them; a `variable (h : False)` would add a hypothesis the scan cannot see), requires an
explicit result type on every definition, refuses proof-shaped result types, `Sort` and `_root_`.
It is a fail-closed pre-Lean stage, not a Lean lexer. The authority is the environment audit of
`check.py --execute`: Lean's own `ConstantInfo` of every constant the five modules add refuses
any theorem, axiom, opaque constant, instance or definition whose type is a proposition beyond
what `structure` and `def` elaboration generate, refuses any transitive axiom outside `propext`,
`Classical.choice`, `Quot.sound`, and requires Lean's statement definitions (type syntactically
`∀ …, Prop`, read without reduction, so a `Set`-valued definition is auxiliary exactly as the
scan's `: Prop` rule has it), structures and auxiliary definitions to equal the register and the
scan exactly. A `def … : Prop` that
elaborates is a precise statement of what would have to be proved. It is not L5 of the #95
ladder; it is `specified`.

| file | role |
|---|---|
| `Specifications.lean` | root; imports exactly the five modules below, in this order |
| `Specifications/Field.lean` | shared objects of the periodized Gaussian lifetime track (namespace `UniversalLaw.Spec.Field`) |
| `Specifications/Lifetime.lean` | lifetime parent Theorems A/B/C, remainder, planar laws (`UniversalLaw.Spec.Lifetime`) |
| `Specifications/Side24.lean` | SIDE24 coefficient objects and enclosure statements (`UniversalLaw.Spec.Side24`) |
| `Specifications/RN.lean` | RN count interface, fixed-window and collision statements (`UniversalLaw.Spec.RN`) |
| `Specifications/P15.lean` | P15 realized covers, price boundary, price budget, full price (`UniversalLaw.Spec.P15`) |
| `REGISTER.json` | the statement register: claim rows, their Lean statements, formal-progress labels, what is not established, next step |
| `sources/` | byte-pinned Layer 0 copies (`sources/SOURCES.json`: repository, commit, path, blob, bytes, sha256) |
| `check.py`, `test_check.py`, `replay.sh` | the checker, its unit tests and negative controls, the local replay |
| `lakefile.toml`, `lean-toolchain`, `lake-manifest.json` | Lean `leanprover/lean4:v4.34.1`, Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`, lock identical to `formal/lake-manifest.json`; `autoImplicit = false` so an unbound name in a header is an error, never a silent implicit parameter |
| `.github/workflows/lean-specifications.yml` | CI: tests, source check, `lean-action` with the Mathlib cache, `check.py --execute`, artifact of `.lake/evidence/` |

## Declarations

150 registered declarations (141 `def … : Prop`, 9 interface `structure`), every one with formal progress `specified`; the 123 auxiliary definitions and abbreviations of the modules are inventory only and are not register statements. Names are given without the module namespace `UniversalLaw.Spec.<Module>.`; the source column is the pinned source named by the docstring's `Source:` line. Anchors and "Not established" cells are copied verbatim from the Lean docstrings (`Anchor:` and `Does not claim:` lines) through REGISTER.json.

### `Specifications/Field.lean` (12 registered declarations)

| declaration | kind | source | registered under claim rows |
|---|---|---|---|
| `IsLPeriodic` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsSmooth` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `GaussianFieldInterface` | structure | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsCriticalPoint` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `HessianHasInertia` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsNondegMax` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsIndexSaddle` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsCandidatePair` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsMorseDistinct` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `SuperlevelBarInterface` | structure | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsFiniteBar` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsLifetimeDensityVersion` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |

### `Specifications/Lifetime.lean` (24 registered declarations)

| declaration | kind | source | registered under claim rows |
|---|---|---|---|
| `IsLPeriodic` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsSmooth` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `GaussianFieldInterface` | structure | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsCriticalPoint` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `HessianHasInertia` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsNondegMax` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsIndexSaddle` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsCandidatePair` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsMorseDistinct` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `SuperlevelBarInterface` | structure | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsFiniteBar` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime` |
| `IsLifetimeDensityVersion` | def_prop | `lifetime-parent` | `lifetime-remainder`, `math.uniform-matrix-cap-lifetime`, `D1-THM-B` |
| `IsWindowPair` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime`, `D1-THM-B` |
| `IsWindowElderPair` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime`, `D1-THM-B` |
| `IsUnrestrictedPair` | def_prop | `lifetime-parent` | `lifetime-remainder`, `math.uniform-matrix-cap-lifetime`, `D1-THM-C` |
| `PairLawInterface` | structure | `lifetime-parent` | `math.uniform-matrix-cap-lifetime`, `D1-THM-A` |
| `ParentUniformSelectionA` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime`, `D1-THM-A` |
| `ParentCompactWindowDensityB` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime`, `D1-THM-B` |
| `IsUnrestrictedLeadingCoefficient` | def_prop | `lifetime-parent` | `lifetime-remainder`, `math.uniform-matrix-cap-lifetime`, `D1-THM-C` |
| `ParentUnrestrictedLeadingDensityC` | def_prop | `lifetime-parent` | `math.uniform-matrix-cap-lifetime`, `D1-THM-C` |
| `RemainderBoundedR1` | def_prop | `lifetime-remainder` | `lifetime-remainder`, `math.lifetime-remainder` |
| `PlanarElderLowerE2` | def_prop | `elder-lower-density-gap` | `OA-ELDER-LOWER-DENSITY-GAP-20260928-v1` |
| `PlanarTwoSidedRateE4` | def_prop | `elder-lower-density-gap` | `OA-ELDER-LOWER-DENSITY-GAP-20260928-v1` |
| `PlanarDensityGapE11` | def_prop | `elder-lower-density-gap` | `OA-ELDER-LOWER-DENSITY-GAP-20260928-v1` |

### `Specifications/Side24.lean` (28 registered declarations)

| declaration | kind | source | registered under claim rows |
|---|---|---|---|
| `ThetaSummable` | def_prop | `side24-proof` | `side24-coefficient` |
| `IsUnitTuple` | def_prop | `side24-proof` | `side24-coefficient` |
| `DerivativePairingBound` | def_prop | `side24-proof` | `side24-coefficient` |
| `DerivativeBoundAtLeastOne` | def_prop | `side24-proof` | `side24-coefficient` |
| `DerivativeBoundAtZero` | def_prop | `side24-proof` | `side24-coefficient` |
| `LatticeImageSumBound` | def_prop | `side24-proof` | `side24-coefficient` |
| `SuccessiveTermRatio` | def_prop | `side24-proof` | `side24-coefficient` |
| `ExponentialBounds` | def_prop | `side24-proof` | `side24-coefficient` |
| `ImageBound` | def_prop | `side24-proof` | `side24-coefficient` |
| `CovarianceOrdering` | def_prop | `side24-proof` | `side24-coefficient` |
| `EntrywiseCovarianceBound` | def_prop | `side24-proof` | `side24-coefficient` |
| `ReferenceCovarianceLowerBound` | def_prop | `side24-proof` | `side24-coefficient` |
| `ReferenceOddAndPinBlocks` | def_prop | `side24-proof` | `side24-coefficient` |
| `DensityComparison` | def_prop | `side24-proof` | `side24-coefficient` |
| `IntegrandRatioBounds` | def_prop | `side24-proof` | `side24-coefficient` |
| `ReferencePinDensityProduct` | def_prop | `side24-proof` | `side24-coefficient` |
| `ReferenceCoefficientIdentity` | def_prop | `side24-proof` | `side24-coefficient` |
| `ConeMomentInterface` | structure | `side24-proof` | `side24-coefficient` |
| `NegDefCone` | def_prop | `side24-proof` | `side24-coefficient` |
| `ConeMomentD1Identity` | def_prop | `side24-proof` | `side24-coefficient` |
| `ConeMomentD2Identity` | def_prop | `side24-proof` | `side24-coefficient` |
| `ConeMomentD2Algebra` | def_prop | `side24-proof` | `side24-coefficient` |
| `TraceMoments` | def_prop | `side24-proof` | `side24-coefficient` |
| `RayleighSquareLaw` | def_prop | `side24-proof` | `side24-coefficient` |
| `ElementaryConeIntegral` | def_prop | `side24-proof` | `side24-coefficient` |
| `PeriodicCoefficientInterface` | structure | `side24-proof` | `side24-coefficient`, `math.side24-coefficient` |
| `CoefficientEnclosure` | def_prop | `side24-proof` | `side24-coefficient`, `math.side24-coefficient` |
| `ReferenceComparison` | def_prop | `side24-proof` | `side24-coefficient`, `math.side24-coefficient` |

### `Specifications/RN.lean` (28 registered declarations)

| declaration | kind | source | registered under claim rows |
|---|---|---|---|
| `IsCriticalPoint` | def_prop | `lifetime-parent` | `rn-fixed-remote-window` |
| `HessianHasInertia` | def_prop | `lifetime-parent` | `rn-fixed-remote-window` |
| `HolderCountBoundN1` | def_prop | `rn-count-interface` | `rn-count-interface`, `math.rn-count-interface` |
| `HolderConsequenceN2` | def_prop | `rn-count-interface` | `rn-count-interface`, `math.rn-count-interface` |
| `ConditionalMeanIdentityN3` | def_prop | `rn-count-interface` | `rn-count-interface`, `math.rn-count-interface` |
| `UniformCounterexampleN4` | def_prop | `rn-count-interface` | `rn-count-interface`, `math.rn-count-interface` |
| `ExponentialTailLayerCakeN5` | def_prop | `rn-count-interface` | `rn-count-interface`, `math.rn-count-interface` |
| `PinnedLawInterface` | structure | `rn-fixed-remote-window` | `rn-fixed-remote-window`, `math.rn-fixed-remote-window` |
| `FixedRemoteMeanMeasureA2` | def_prop | `rn-fixed-remote-window` | `rn-fixed-remote-window`, `math.rn-fixed-remote-window`, `math.rn-region.fixed-remote`, `math.d5-component.remote-window-proof` |
| `FixedRemoteCountBoundA3` | def_prop | `rn-fixed-remote-window` | `rn-fixed-remote-window`, `math.rn-fixed-remote-window`, `math.rn-region.fixed-remote`, `math.d5-component.remote-window-proof` |
| `FixedAnnulusWindowCandidateA2` | def_prop | `rn-fixed-annulus-window` | `rn-fixed-annulus-window`, `math.rn-fixed-annulus-window`, `math.rn-region.fixed-annulus-window` |
| `AnnulusBridgeAllHeight2` | def_prop | `rn-annulus-bridge` | `math.rn-region.mesoscopic-scaled-annulus`, `math.d5-component.annulus-proof` |
| `D5aPuncturedPinDisks` | def_prop | `d5-reconciliation` | `math.rn-region.pin-collision`, `math.d5-pin-neighborhood-first-moment`, `math.d5-component.punctured-pin-proof` |
| `D5bMicrodisk` | def_prop | `d5-reconciliation` | `math.rn-region.pin-collision`, `math.d5-pin-neighborhood-first-moment`, `math.d5-component.punctured-pin-proof` |
| `D5cCollarC1` | def_prop | `d5-reconciliation` | `math.d5-pin-neighborhood-first-moment`, `math.d5-component.collar-proof` |
| `D5dSummedPinNeighbourhoodC2` | def_prop | `d5-reconciliation` | `math.rn-region.mesoscopic-scaled-annulus`, `math.rn-region.pin-collision`, `math.d5-pin-neighborhood-first-moment` |
| `D5eIntermediateShellsI3I4` | def_prop | `d5-reconciliation` | `math.rn-region.intermediate-r-to-rho`, `math.d5-pin-neighborhood-first-moment`, `math.d5-component.intermediate-window-proof` |
| `D5fGlobalWindowFirstMomentI5` | def_prop | `d5-reconciliation` | `math.d5-pin-neighborhood-first-moment`, `math.d5-component.intermediate-window-proof` |
| `DimensionLiftPuncturedPinBallP` | def_prop | `d5-dimension-lift` | `CL-D5-DIMENSION-LIFT-20260929-v1` |
| `DimensionLiftCompactCollarC` | def_prop | `d5-dimension-lift` | `CL-D5-DIMENSION-LIFT-20260929-v1` |
| `DimensionLiftIntermediateShellsI` | def_prop | `d5-dimension-lift` | `CL-D5-DIMENSION-LIFT-20260929-v1` |
| `DimensionLiftGlobalWindowG` | def_prop | `d5-dimension-lift` | `CL-D5-DIMENSION-LIFT-20260929-v1` |
| `FourierCutoffPlanarSecondFactorialF4` | def_prop | `c6-fourier-cutoff` | `OA-C6-FOURIER-20260929-v1` |
| `PalmRouteFactorialMomentsQ` | def_prop | `c6-palm-route` | `CL-C6-PALM-20260929-v1` |
| `PalmRouteSecondFactorialTheta` | def_prop | `c6-palm-route` | `CL-C6-PALM-20260929-v1` |
| `RareClusterPoissonObstructionO` | def_prop | `c6-rare-cluster` | `OA-C6-RARE-CLUSTER-20260929-v1` |
| `RemoteCollisionSecondFactorialD` | def_prop | `remote-collision` | `math.rn-region.witness-collision`, `CL-D5-REMOTE-COLLISION-20260928-v1` |
| `WitnessCollisionNearPinPairsTarget` | def_prop | `d5-reconciliation` | `math.rn-region.witness-collision` |

### `Specifications/P15.lean` (58 registered declarations)

| declaration | kind | source | registered under claim rows |
|---|---|---|---|
| `RealizedData` | structure | `p15-realized-covers` | `p15-realized-covers` |
| `IsRealizedFamily` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `IsGood` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `IsKDecomposable` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `IsGeneratorCover` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `IsPaletteFeasible` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `PaletteNumberAttained` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `IsMinimalForbidden` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `IsTransversal` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `MinimalForbiddenCharacterisation` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `LocalRestriction` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `LocalDecomposability` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `LocalObstructionIsFullBlock` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `LocalPriceChain` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `IndependentBlockHazard` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `FullBlockCoverIff` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `CoverCostHazardBound` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `WholeGroundChromaticNumber` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `ElementaryPaletteFormula` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `TriangleNeedsThree` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `Benchmark816IsRealized` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `Benchmark816Palette` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `Benchmark816Cover` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `Benchmark816WholeGround` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `Benchmark816MinimalForbiddenCounts` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `Benchmark816Price` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `Benchmark816UnionBound` | def_prop | `p15-realized-covers` | `p15-realized-covers` |
| `TwoCoordGeneratorPrices` | def_prop | `p15-price-boundary` | `p15-price-boundary`, `math.p15-price-boundary` |
| `DemandOneRefutation` | def_prop | `p15-price-boundary` | `p15-price-boundary`, `math.p15-price-boundary` |
| `LogOnePlusBelowIdentity` | def_prop | `p15-price-boundary` | `p15-price-boundary` |
| `LogRatioBound` | def_prop | `p15-price-budget` | `p15-price-budget-restricted` |
| `RatioExponentBound` | def_prop | `p15-price-budget` | `p15-price-budget-restricted` |
| `RestrictedLocalBudget` | def_prop | `p15-price-budget` | `p15-price-budget-restricted` |
| `RestrictedTransformedPriceBudget` | def_prop | `p15-price-budget` | `p15-price-budget-restricted` |
| `RhoTestSufficient` | def_prop | `p15-price-budget` | `p15-price-budget-restricted` |
| `CapTestAtTwoThirds` | def_prop | `p15-price-budget` | `p15-price-budget-restricted` |
| `Benchmark816TransformedRange` | def_prop | `p15-price-budget` | `p15-price-budget-restricted` |
| `Benchmark816RationalPrice` | def_prop | `p15-price-budget` | `p15-price-budget-restricted` |
| `FullTransformedPriceBudget` | def_prop | `p15-full-price` | `p15-full-price`, `math.p15-full-price` |
| `RhoStarEnclosure` | def_prop | `p15-full-price` | `p15-full-price`, `math.p15-full-price` |
| `RhoStarBelowSixSevenths` | def_prop | `p15-full-price` | `p15-full-price` |
| `IsProperDownset` | def_prop | `p15-full-price` | `p15-full-price` |
| `HazardStarPositive` | def_prop | `p15-full-price` | `p15-full-price` |
| `CoordinatewiseConcavity` | def_prop | `p15-full-price` | `p15-full-price` |
| `HazardProductBound` | def_prop | `p15-full-price` | `p15-full-price` |
| `HazardPhiBound` | def_prop | `p15-full-price` | `p15-full-price` |
| `FullGroundPriceBound` | def_prop | `p15-full-price` | `p15-full-price` |
| `PhiAtPStar` | def_prop | `p15-full-price` | `p15-full-price` |
| `FullGroundBudgetIff` | def_prop | `p15-full-price` | `p15-full-price` |
| `CapacityHazardIsBinomial` | def_prop | `p15-full-price` | `p15-full-price` |
| `OddMajorityIdentity` | def_prop | `p15-full-price` | `p15-full-price` |
| `CapacityWorstCase` | def_prop | `p15-full-price` | `p15-full-price` |
| `HStarExceedsOne` | def_prop | `p15-full-price` | `p15-full-price` |
| `LocalPriceBoundFull` | def_prop | `p15-full-price` | `p15-full-price` |
| `GlobalAssemblyHazard` | def_prop | `p15-full-price` | `p15-full-price` |
| `SharpnessOfRhoStar` | def_prop | `p15-full-price` | `p15-full-price`, `math.p15-full-price` |
| `DemandOneBoundary` | def_prop | `p15-full-price` | `p15-full-price` |
| `SixSeventhsCertificate` | def_prop | `p15-full-price` | `p15-full-price` |

## Claims

171 claim rows: 10 `landing_claim`, 33 `graph_node`, 2 `open_obligation`, 95 `proof_index_result`, 7 `existing_lean_package`, 12 `main_experiment_proof`, 12 `exact_certificate`. Claim-level formal progress: 33 `specified` (a `def … : Prop` stating the claim itself is registered), 138 `none`; no research claim is `proved` or `kernel-checked`. 197 statement entries point at the 150 declarations of this package (all `specified`); 31 statement entries are kernel-proved arithmetic theorems of main's `formal/` package (label `proved`: the 31 Side24 targets at origin/main `f6deeba7`; main's 28 P15 arithmetic targets are NOT listed because they exist only in this programme's uncommitted main worktree, on no commit), listed as the arithmetic skeleton of the claim they sit under and never as the claim. `disposition` is the verbatim LANDING_CLAIMS value or `—` (null). Nothing in these tables is a scientific status, a review verdict or an acceptance; alignment of every statement is `PENDING_INDEPENDENT_REVIEW`.

| claim_id | kind | disposition (LANDING_CLAIMS, verbatim) | formal_progress | layer 0 source | statements |
|---|---|---|---|---|---|
| `side24-coefficient` | landing_claim | REVIEWED_SCOPED | `specified` | `side24-proof` | 28 specified: `ThetaSummable`, `IsUnitTuple`, `DerivativePairingBound`, `DerivativeBoundAtLeastOne`, `DerivativeBoundAtZero`, `LatticeImageSumBound`, `SuccessiveTermRatio`, `ExponentialBounds`, `ImageBound`, `CovarianceOrdering`, `EntrywiseCovarianceBound`, `ReferenceCovarianceLowerBound`, `ReferenceOddAndPinBlocks`, `DensityComparison`, `IntegrandRatioBounds`, `ReferencePinDensityProduct`, `ReferenceCoefficientIdentity`, `ConeMomentInterface`, `NegDefCone`, `ConeMomentD1Identity`, `ConeMomentD2Identity`, `ConeMomentD2Algebra`, `TraceMoments`, `RayleighSquareLaw`, `ElementaryConeIntegral`, `PeriodicCoefficientInterface`, `CoefficientEnclosure`, `ReferenceComparison`; 27 proved (main): `pairing_sum_six`, `pairing_sum_le_six`, `pairing_terms_six`, `sixth_moment_double_factorial`, `lattice_shell_constant`, `geometric_ratio_constants`, `period_exponent`, `image_constant_value`, `exp_taylor_partial_sum_gt_ten`, `covariance_relative_bound`, `odd_block_eigenvalues`, `odd_block_shifted_minors`, `smaller_eigenvalue_exceeds_third`, `exponent_bounds`, `exponent_values`, `ratio_constant_ordering`, `density_comparison_below_reported`, `conditional_third_derivative_variance`, `transverse_covariance_entries_thirds`, `cone_moment_m1_thirds`, `trace_and_traceless_variances`, `fourth_moment_of_trace`, `exponential_moment_of_trace`, `cone_moment_m2_algebra`, `cube_root_simplification`, `pin_determinant_and_joint_dimension`, `hessian_block_eigenvalues` |
| `lifetime-remainder` | landing_claim | REVIEWED_SCOPED | `specified` | `lifetime-remainder` | 4 specified: `RemainderBoundedR1`, `IsUnrestrictedPair`, `IsUnrestrictedLeadingCoefficient`, `IsLifetimeDensityVersion` |
| `rn-count-interface` | landing_claim | HOLD_WITH_DOMAIN | `none` | `rn-count-interface` | 5 specified: `HolderCountBoundN1`, `HolderConsequenceN2`, `ConditionalMeanIdentityN3`, `UniformCounterexampleN4`, `ExponentialTailLayerCakeN5` |
| `rn-fixed-remote-window` | landing_claim | HOLD_WITH_DOMAIN | `specified` | `rn-fixed-remote-window` | 5 specified: `PinnedLawInterface`, `IsCriticalPoint`, `HessianHasInertia`, `FixedRemoteMeanMeasureA2`, `FixedRemoteCountBoundA3` |
| `rn-fixed-annulus-window` | landing_claim | REVIEWED_SCOPED | `specified` | `rn-fixed-annulus-window` | 1 specified: `FixedAnnulusWindowCandidateA2` |
| `p15-realized-covers` | landing_claim | HOLD_WITH_DOMAIN | `specified` | `p15-realized-covers` | 27 specified: `RealizedData`, `IsRealizedFamily`, `IsGood`, `IsKDecomposable`, `IsGeneratorCover`, `IsPaletteFeasible`, `PaletteNumberAttained`, `IsMinimalForbidden`, `IsTransversal`, `MinimalForbiddenCharacterisation`, `LocalRestriction`, `LocalDecomposability`, `LocalObstructionIsFullBlock`, `LocalPriceChain`, `IndependentBlockHazard`, `FullBlockCoverIff`, `CoverCostHazardBound`, `WholeGroundChromaticNumber`, `ElementaryPaletteFormula`, `TriangleNeedsThree`, `Benchmark816IsRealized`, `Benchmark816Palette`, `Benchmark816Cover`, `Benchmark816WholeGround`, `Benchmark816MinimalForbiddenCounts`, `Benchmark816Price`, `Benchmark816UnionBound` |
| `p15-price-boundary` | landing_claim | EXACT_COUNTEREXAMPLE | `specified` | `p15-price-boundary` | 3 specified: `TwoCoordGeneratorPrices`, `DemandOneRefutation`, `LogOnePlusBelowIdentity` |
| `p15-price-budget-restricted` | landing_claim | HOLD_WITH_DOMAIN | `specified` | `p15-price-budget` | 8 specified: `LogRatioBound`, `RatioExponentBound`, `RestrictedLocalBudget`, `RestrictedTransformedPriceBudget`, `RhoTestSufficient`, `CapTestAtTwoThirds`, `Benchmark816TransformedRange`, `Benchmark816RationalPrice` |
| `p15-full-price` | landing_claim | REVIEWED_SCOPED | `specified` | `p15-full-price` | 20 specified: `FullTransformedPriceBudget`, `RhoStarEnclosure`, `RhoStarBelowSixSevenths`, `IsProperDownset`, `HazardStarPositive`, `CoordinatewiseConcavity`, `HazardProductBound`, `HazardPhiBound`, `FullGroundPriceBound`, `PhiAtPStar`, `FullGroundBudgetIff`, `CapacityHazardIsBinomial`, `OddMajorityIdentity`, `CapacityWorstCase`, `HStarExceedsOne`, `LocalPriceBoundFull`, `GlobalAssemblyHazard`, `SharpnessOfRhoStar`, `DemandOneBoundary`, `SixSeventhsCertificate` |
| `downstream-hard-gate` | landing_claim | ENGINEERING_HOLD | `none` | `downstream-graph` | — |
| `math.uniform-matrix-cap-lifetime` | graph_node | — | `specified` | `lifetime-parent` | 32 specified: `IsLPeriodic`, `IsSmooth`, `GaussianFieldInterface`, `IsCriticalPoint`, `HessianHasInertia`, `IsNondegMax`, `IsIndexSaddle`, `IsCandidatePair`, `IsMorseDistinct`, `SuperlevelBarInterface`, `IsFiniteBar`, `IsLifetimeDensityVersion`, `IsLPeriodic`, `IsSmooth`, `GaussianFieldInterface`, `IsCriticalPoint`, `HessianHasInertia`, `IsNondegMax`, `IsIndexSaddle`, `IsCandidatePair`, `IsMorseDistinct`, `SuperlevelBarInterface`, `IsFiniteBar`, `IsLifetimeDensityVersion`, `IsWindowPair`, `IsWindowElderPair`, `IsUnrestrictedPair`, `PairLawInterface`, `ParentUniformSelectionA`, `ParentCompactWindowDensityB`, `IsUnrestrictedLeadingCoefficient`, `ParentUnrestrictedLeadingDensityC` |
| `math.d1-component.congruence-erratum` | graph_node | — | `none` | `downstream-graph` | — |
| `math.d1-component.section9-replacement-v1_1` | graph_node | — | `none` | `downstream-graph` | — |
| `math.d1-component.marked-cylinder-cap` | graph_node | — | `none` | `marked-cylinder-cap` | — |
| `math.d1-component.reconciliation-record` | graph_node | — | `none` | `downstream-graph` | — |
| `math.lifetime-remainder` | graph_node | — | `specified` | `lifetime-remainder` | 1 specified: `RemainderBoundedR1` |
| `math.side24-coefficient` | graph_node | — | `specified` | `side24-proof` | 3 specified: `PeriodicCoefficientInterface`, `CoefficientEnclosure`, `ReferenceComparison` |
| `math.rn-count-interface` | graph_node | — | `none` | `rn-count-interface` | 5 specified: `HolderCountBoundN1`, `HolderConsequenceN2`, `ConditionalMeanIdentityN3`, `UniformCounterexampleN4`, `ExponentialTailLayerCakeN5` |
| `math.rn-fixed-remote-window` | graph_node | — | `specified` | `rn-fixed-remote-window` | 3 specified: `PinnedLawInterface`, `FixedRemoteMeanMeasureA2`, `FixedRemoteCountBoundA3` |
| `math.rn-region.fixed-remote` | graph_node | — | `specified` | `downstream-graph` | 2 specified: `FixedRemoteMeanMeasureA2`, `FixedRemoteCountBoundA3` |
| `math.rn-region.mesoscopic-scaled-annulus` | graph_node | — | `specified` | `d5-reconciliation` | 2 specified: `D5dSummedPinNeighbourhoodC2`, `AnnulusBridgeAllHeight2` |
| `math.rn-region.pin-collision` | graph_node | — | `specified` | `d5-reconciliation` | 3 specified: `D5aPuncturedPinDisks`, `D5bMicrodisk`, `D5dSummedPinNeighbourhoodC2` |
| `math.rn-region.intermediate-r-to-rho` | graph_node | — | `specified` | `d5-reconciliation` | 1 specified: `D5eIntermediateShellsI3I4` |
| `math.rn-region.witness-collision` | open_obligation | — | `specified` | `d5-reconciliation` | 2 specified: `WitnessCollisionNearPinPairsTarget`, `RemoteCollisionSecondFactorialD` |
| `math.rn-mesoscopic-reduction` | graph_node | — | `none` | `downstream-graph` | — |
| `math.p15-full-price` | graph_node | — | `specified` | `p15-full-price` | 3 specified: `FullTransformedPriceBudget`, `RhoStarEnclosure`, `SharpnessOfRhoStar` |
| `math.p15-price-boundary` | graph_node | — | `specified` | `p15-price-boundary` | 2 specified: `TwoCoordGeneratorPrices`, `DemandOneRefutation` |
| `math.rn-selector-region-crosswalk` | graph_node | — | `none` | `downstream-graph` | — |
| `math.rn-fixed-annulus-window` | graph_node | — | `specified` | `rn-fixed-annulus-window` | 1 specified: `FixedAnnulusWindowCandidateA2` |
| `math.rn-region.fixed-annulus-window` | graph_node | — | `specified` | `downstream-graph` | 1 specified: `FixedAnnulusWindowCandidateA2` |
| `math.d5-pin-neighborhood-first-moment` | graph_node | — | `specified` | `d5-reconciliation` | 6 specified: `D5aPuncturedPinDisks`, `D5bMicrodisk`, `D5cCollarC1`, `D5dSummedPinNeighbourhoodC2`, `D5eIntermediateShellsI3I4`, `D5fGlobalWindowFirstMomentI5` |
| `math.d5-component.punctured-pin-proof` | graph_node | — | `specified` | `d5-reconciliation` | 2 specified: `D5aPuncturedPinDisks`, `D5bMicrodisk` |
| `math.d5-component.punctured-pin-review-111` | graph_node | — | `none` | `downstream-graph` | — |
| `math.d5-component.punctured-pin-continuum-review` | graph_node | — | `none` | `downstream-graph` | — |
| `math.d5-component.punctured-pin-continuum-check` | graph_node | — | `none` | `downstream-graph` | — |
| `math.d5-component.collar-review` | graph_node | — | `none` | `downstream-graph` | — |
| `math.d5-component.annulus-review` | graph_node | — | `none` | `downstream-graph` | — |
| `math.d5-component.i5-review-xai` | graph_node | — | `none` | `downstream-graph` | — |
| `math.d5-component.i5-review-claude` | graph_node | — | `none` | `downstream-graph` | — |
| `math.d5-component.offpin-second-moment-review` | graph_node | — | `none` | `downstream-graph` | — |
| `math.d5-component.collar-proof` | graph_node | — | `specified` | `d5-reconciliation` | 1 specified: `D5cCollarC1` |
| `math.d5-component.annulus-proof` | graph_node | — | `specified` | `rn-annulus-bridge` | 1 specified: `AnnulusBridgeAllHeight2` |
| `math.d5-component.intermediate-window-proof` | graph_node | — | `specified` | `d5-reconciliation` | 2 specified: `D5eIntermediateShellsI3I4`, `D5fGlobalWindowFirstMomentI5` |
| `math.d5-component.remote-window-proof` | graph_node | — | `specified` | `rn-fixed-remote-window` | 2 specified: `FixedRemoteMeanMeasureA2`, `FixedRemoteCountBoundA3` |
| `D1-THM-A` | proof_index_result | — | `specified` | `lifetime-parent` | 2 specified: `PairLawInterface`, `ParentUniformSelectionA` |
| `D1-THM-B` | proof_index_result | — | `specified` | `lifetime-parent` | 4 specified: `IsWindowPair`, `IsWindowElderPair`, `IsLifetimeDensityVersion`, `ParentCompactWindowDensityB` |
| `D1-THM-C` | proof_index_result | — | `specified` | `lifetime-parent` | 3 specified: `IsUnrestrictedPair`, `IsUnrestrictedLeadingCoefficient`, `ParentUnrestrictedLeadingDensityC` |
| `OA-ELDER-LOWER-DENSITY-GAP-20260928-v1` | proof_index_result | — | `specified` | `elder-lower-density-gap` | 3 specified: `PlanarElderLowerE2`, `PlanarTwoSidedRateE4`, `PlanarDensityGapE11` |
| `two-scale-s6-s21` | proof_index_result | — | `none` | `—` | — |
| `axial-density` | proof_index_result | — | `none` | `—` | — |
| `fixed-transverse-chart` | proof_index_result | — | `none` | `—` | — |
| `CL-D5-DIMENSION-LIFT-20260929-v1` | proof_index_result | — | `specified` | `d5-dimension-lift` | 4 specified: `DimensionLiftPuncturedPinBallP`, `DimensionLiftCompactCollarC`, `DimensionLiftIntermediateShellsI`, `DimensionLiftGlobalWindowG` |
| `OA-C6-FOURIER-20260929-v1` | proof_index_result | — | `none` | `c6-fourier-cutoff` | 1 specified: `FourierCutoffPlanarSecondFactorialF4` |
| `CL-C6-PALM-20260929-v1` | proof_index_result | — | `specified` | `c6-palm-route` | 2 specified: `PalmRouteFactorialMomentsQ`, `PalmRouteSecondFactorialTheta` |
| `OA-C6-RARE-CLUSTER-20260929-v1` | proof_index_result | — | `none` | `c6-rare-cluster` | 1 specified: `RareClusterPoissonObstructionO` |
| `CL-D5-REMOTE-COLLISION-20260928-v1` | proof_index_result | — | `none` | `remote-collision` | 1 specified: `RemoteCollisionSecondFactorialD` |
| `cumulative-transfer-correction` | proof_index_result | — | `none` | `cumulative-transfer-correction` | — |
| `hist.D0-RN-UNIF-historical-predicates` | open_obligation | — | `none` | `downstream-graph` | — |
| `lean:main-formal-UniversalLaw` | existing_lean_package | — | `none` | `side24-enclosure` | 4 proved (main): `d2_endpoints_adjacent`, `d3_endpoints_adjacent`, `d3_below_d2`, `endpoints_in_unit_tenth` |
| `lean:math-formal-ResearchFormalCoreR1` | existing_lean_package | — | `none` | `—` | — |
| `lean:math-companion-d2_moment_bridge_20261006` | existing_lean_package | — | `none` | `—` | — |
| `lean:math-companion-d2_square_schur_20261006` | existing_lean_package | — | `none` | `—` | — |
| `lean:math-companion-d2_atom_integral_20261006` | existing_lean_package | — | `none` | `—` | — |
| `lean:math-frontier-cap_first_exit_lean_20261002` | existing_lean_package | — | `none` | `marked-cylinder-cap` | — |
| `lean:math-w3scratch-side24-proposal` | existing_lean_package | — | `none` | `—` | — |
| `main:experiments/universality/finite_gaussian_contact` | main_experiment_proof | — | `none` | `—` | — |
| `main:experiments/universality/finite_candidate_lifetime` | main_experiment_proof | — | `none` | `—` | — |
| `main:experiments/universality/finite_fold_chart` | main_experiment_proof | — | `none` | `—` | — |
| `main:experiments/universality/finite_weighted_fold_window` | main_experiment_proof | — | `none` | `—` | — |
| `main:experiments/universality/finite_contact_genericity` | main_experiment_proof | — | `none` | `—` | — |
| `main:experiments/universality/finite_elder_transfer` | main_experiment_proof | — | `none` | `—` | — |
| `main:experiments/universality/finite_h0_lifetime` | main_experiment_proof | — | `none` | `—` | — |
| `main:experiments/universality/fold_structural_universality` | main_experiment_proof | — | `none` | `—` | — |
| `main:experiments/universality/periodized_gaussian_h0` | main_experiment_proof | — | `none` | `—` | — |
| `main:experiments/universality/iid_short_bar_process` | main_experiment_proof | — | `none` | `—` | — |
| `main:experiments/periodic_h0/spectral_shrinking_bins` | main_experiment_proof | — | `none` | `—` | — |
| `main:unmerged-codex-prs-330-350` | main_experiment_proof | — | `none` | `—` | — |
| `cert:main-periodic_h0-exact_h0_1` | exact_certificate | — | `none` | `—` | — |
| `cert:main-periodic_h0-certificate8` | exact_certificate | — | `none` | `—` | — |
| `cert:main-periodic_h0-nodal1` | exact_certificate | — | `none` | `—` | — |
| `cert:main-periodic_h0-hessian1` | exact_certificate | — | `none` | `—` | — |
| `cert:main-periodic_h0-gaussian_tail1` | exact_certificate | — | `none` | `—` | — |
| `cert:main-periodic_h0-gaussian_coupling1` | exact_certificate | — | `none` | `—` | — |
| `cert:main-periodic_h0-word_polynomial1` | exact_certificate | — | `none` | `—` | — |
| `cert:main-periodic_h0-finite_count_loss1` | exact_certificate | — | `none` | `—` | — |
| `cert:main-periodic_h0-count_confidence1` | exact_certificate | — | `none` | `—` | — |
| `cert:main-universality-fold_controls` | exact_certificate | — | `none` | `—` | — |
| `cert:math-side24_v1-coefficient.py` | exact_certificate | — | `none` | `side24-enclosure` | — |
| `cert:math-full_price-full_price.py` | exact_certificate | — | `none` | `p15-full-price` | — |

Packets listed by PROOF_INDEX by id only (82 rows, kind `proof_index_result`, formal progress `none`, no statements, bytes not pinned here; each row's `not_established` says the statement was not extracted and no verdict is implied):

`CL-SIDE24-PFV-20260929-v1`, `OA-SIDE24-REMAINDER-20260929-v1`, `CL-SIDE24-PERIODIZATION-REMAINDER-20260929-v1`, `OA-CONTACT-ANGULAR-TAIL-20260925-v1`, `OA-PIN-MICRO-COV-20260926-v1`, `OA-D5-MICRODISK-20260926-v1`, `D5-PIN-MICRODISK-20260927-v1`, `OA-BF-SIX-PIN-HESSIAN-20260926-v1`, `OA-CONTACT-KERNEL-SUBSTITUTE-20260926-v1`, `OA-D5-SHORT-EDGE-20260928-v1`, `CL-D5-PIN-DISK-20260928-v1`, `OA-D5-REMOTE-SINGLETON-LAW-20260928-v1`, `OA-REMOTE-HEIGHT-DECOUPLING-20260928-v1`, `OA-WINDOW-MULTIPLICITY-LOCAL`, `OA-WINDOW-MULTIPLICITY-REMOTE`, `OA-WINDOW-MULTIPLICITY-DISTANCE`, `OA-WINDOW-MULTIPLICITY-HEIGHT`, `OA-REMOTE-INVERSE-SEPARATION-20260928-v1`, `OA-ELDER-DIMENSION-LIFT-20260928-v1`, `CL-ELDER-LOWER-ALL-D-20260929-v1.1`, `CL-C6-FACTORIAL-20260929-v1`, `CL-C6-SHARPENED-20260929-v1`, `OA-C6-COUNT-CAP-BOUNDARY-20260929-v1`, `OA-LOCAL-CLUSTER-TIGHTNESS-20260929-v1`, `OA-REMOTE-MIXED-INVERSE-20260929-v1`, `CL-D1-UNRESTRICTED-DIFFERENCE-20260929-v3`, `CL-C7-TOTAL-BOUNDED-20260929-v1.2`, `OA-C7-ZERO-GAP-LIMIT-20260929-v1`, `OA-SARD-ROBUST-CHARTS-20260929-v1`, `OA-SARD-A2-FIXED-FRAME-20260929-v2`, `packet:sard_g_a2_regularity_20260929`, `packet:sard_g_pinned_transfer_20260929`, `OA-P15-BIPARTITE-OVERLAP-20260928-v1`, `OA-P15-TAIL-LOAD-20260928-v1`, `packet:planar_cubic_cluster_20260929`, `packet:c6_marked_fourier_20260929`, `packet:c6_cluster_law_20260929`, `packet:cluster_exponential_weight_20260930`, `packet:spectral_cluster_closure_20260929`, `packet:lifetime_moment_boundary_20260930`, `packet:radial_rate_20260930`, `packet:extreme_cluster_sampling_20260930`, `packet:fixed_r_inverse_lifetime_20260930`, `packet:local_elder_geometry_20260930`, `packet:concave_fibre_elder_20260930`, `packet:elder_partner_extremes_20260930`, `packet:remainder_vanishing_20260930`, `packet:elder_selected_extremes_20260930`, `packet:remainder_rate_20260930`, `packet:far_elder_rate_20260930`, `packet:short_bar_endpoint_law_20261001`, `packet:c2_finite_jet_transfer_20261001`, `packet:cusp_second_order_20261001`, `packet:candidate_third_order_20261001`, `packet:elder_third_order_20261001`, `packet:third_order_rate_20261001`, `packet:elder_cusp_parity_20261002`, `packet:separated_fold_multiplicity_20261002`, `packet:subpin_collision_20261002`, `packet:soft_rejected_pairs_20261002`, `packet:soft_fold_limit_20261002`, `packet:soft_closed_form_20261002`, `packet:cusp_torus_transfer_20261001`, `packet:moving_remote_collision_20261003`, `packet:ordinary_short_bar_occurrence_20261001`, `packet:replacement_bar_occurrence_20261001`, `packet:strict_unique_replacement_coefficient_20261003`, `packet:unique_replacement_bar_intensity_20261001`, `packet:planar_rejected_endpoint_margin_20261003/A4`, `packet:planar_soft_layer_chain_20261003/C91`, `packet:planar_soft_layer_chain_20261003/C92`, `packet:planar_soft_layer_chain_20261003/C93`, `packet:planar_soft_layer_chain_20261003/C94`, `packet:planar_soft_layer_chain_20261003/C95`, `packet:planar_soft_layer_chain_20261003/C96`, `packet:planar_soft_layer_chain_20261003/C97`, `packet:planar_soft_layer_chain_20261003/C98`, `packet:planar_soft_layer_chain_20261003/C99`, `packet:planar_soft_layer_chain_20261003/C101`, `packet:planar_soft_layer_chain_20261003/C102`, `packet:planar_soft_layer_chain_20261003/C103`, `packet:planar_soft_layer_chain_20261003/C124`.

## What this packet is not

* Not a proof of anything. Every registered declaration is a definition or a structure. The
  source scan refuses `theorem`, `lemma`, `example`, `instance`, `axiom`, `sorry`, `native_decide`,
  `unsafe`, `opaque`, `partial`, `macro`, `notation`, `set_option` and the rest of the lexical list
  as whole tokens of comment-stripped code; the environment audit of `--execute` refuses, by
  Lean's `ConstantInfo`, any theorem, axiom, opaque constant, instance or definition whose type is
  a proposition that `structure`/`def` elaboration did not generate, and the build log is refused
  on `declaration uses` (sorry) and on Lean's "is a proposition; use `theorem`" linter.
* Not a receipt from a local run. `--execute --allow-dirty` was run once locally (2026-10-10, worktree
  UNVERIFIED: not evidence about any commit): `lake build` of the five modules passed against the
  pinned Mathlib `d13f23b7`; `lake env leanchecker Specifications` was killed by the sandbox's memory
  cgroup (exit 137 at 13.4 GB resident) before finishing, so `execute()` failed closed at that step
  and wrote no receipt. The later stages were then run with the same functions over the fresh oleans:
  `#check` of all 150 registered declarations, `#print axioms` (149 within `{propext,
  Classical.choice, Quot.sound}`, 1 within `{propext, Quot.sound}`), the environment audit (558
  constants, 0 refused: 141 statements, 9 structures, 123 auxiliary, 285 generated, equal to the
  register and the scan) and every negative control. The first receipt for the real packet is the
  hosted `lean-specifications.yml` run; its `leanchecker` step over `import Mathlib` has the
  `cap-first-exit-lean.yml` precedent (about 30 minutes on a 16 GB runner) within the 45-minute
  budget, and that budget and the runner's memory are untimed here.
* Not an alignment review. Whether a Prop says what its anchor says is the independent reviewer's
  question (DESIGN honesty checklist). The register only records `PENDING_INDEPENDENT_REVIEW`.
* Not a scientific status. Dispositions in the register are transcribed verbatim from
  `claims/LANDING_CLAIMS.json` at the pinned commit; the checker refuses any other value.
* Not a kernel receipt for the research claims. `--execute` shows that the statements elaborate
  and depend on no axiom beyond `propext`, `Classical.choice`, `Quot.sound`; the receipt says
  `formalization_status: "specified"` and nothing stronger.
* Not evidence from a dirty worktree. A receipt produced with `--allow-dirty` records the
  worktree as unverified and is not evidence about any commit.

## How to run

```bash
# source mode (the optional positional `source` names the same default mode): identity against
# HEAD, lexical refusals, root imports, declaration inventory vs REGISTER.json and back,
# vocabulary, verbatim anchors (at least 16 characters), pinned bytes, lock, toolchain
python3 -B -S specifications/lean_statements_20261010/check.py
python3 -B -S specifications/lean_statements_20261010/check.py source

# unit tests and negative controls, both interpreter modes (no Lean needed)
python3 -B -S specifications/lean_statements_20261010/test_check.py
python3 -B -O -S specifications/lean_statements_20261010/test_check.py

# execution: fresh lake build, leanchecker, #check and #print axioms of every registered
# declaration, the environment audit of every constant the modules add, the negative controls
# (source-side, Lean-side and of the audit itself), receipt under .lake/evidence/ (needs the
# pinned toolchain and the Mathlib cache or a source build of Mathlib d13f23b7)
export PATH="$HOME/.elan/bin:$PATH"
python3 -B -S specifications/lean_statements_20261010/check.py --execute

# everything in order
bash specifications/lean_statements_20261010/replay.sh
```

Environment: Lean `leanprover/lean4:v4.34.1` (release commit `5045d0056413266e57c625dcd7c365b10e377c52`),
Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`, full dependency lock in `lake-manifest.json`
(identical to `formal/lake-manifest.json` except the package name). CI uses
`leanprover/lean-action@f061402b660e0c34644504b324e830f2991d4865` with `use-mathlib-cache: 'true'`.
Without the Mathlib cache (hosts `cache.mathlib.org`, `release.lean-lang.org`,
`reservoir.lean-lang.org`), Mathlib must be built from source, which takes hours.
