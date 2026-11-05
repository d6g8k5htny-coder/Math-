# Complete finite Gaussian / literal residual application text

Frozen 26 October 2026 at approximately 20:16 UTC, **before one producer integration**. This is **UNCOMPILED TEXT ONLY**, supplied by `/root/endpoint_gaussian_ac_text` to `/root/h0_older_clearance_construct` for actual authorized57 module `SourceRawPinFreeCoordinates`, namespace `I4SourceRawPinFreeCoordinates`.

Root's `ROOT_GO.json` was read. Actual native pickup `6426116065` was created 20:06:22 UTC, board `6426116811`; precode `f01e0c7e94b5e1f929bfe18fe6bb01e3c44060b1`; actual GO 20:07:34.061496 UTC. The published concrete control contract was frozen before implementation/helper text. Checkpoint21:15 UTC and terminal23:30 UTC/end are unchanged. These process facts are carried from root's record, without an external lookup or old identity check.

The entire needed section is `SECTION.lean.txt`; exact narrow imports are in `IMPORTS.txt`. Insert the complete section once after the producer's actual frame/maps, deterministic identities and `freeMaps_measurable`, inside the target namespace/noncomputable section. There is no helper object or standalone test target.

## Exact producer context and deterministic dependencies

The producer confirmed all names and signatures before drafting. The actual frame is `RawPinFreeFrame L r n` with precisely `chi : Fin n → SourceMode 2 →₀ ℝ`, the finite Gram delta field, and literal six-row raw-kernel field from the published contract. The maps are the literal finite pairing, finite shift and full finite-projection residual defined there.

The helper consumes these **already authored deterministic producer identities**, with implicit L,r,n and frame F:

- `chi_summable F j : Summable (fun m => F.chi j m)`.
- `chi_normSquared F j : (∑' m, (F.chi j m)^2) = 1`.
- `freeCoordinate_eq_unitDirection F j : (fun ω => freeCoordinate F ω j) = unitDirection (fun m => F.chi j m)`.
- `freeResidualSample_val F ω m : (freeResidualSample F ω).val m = ω.val m - ∑ j, F.chi j m * freeCoordinate F ω j`.
- `finitePairing_eq_tsum a v : finitePairing a v = ∑' m, a m * v m`.
- The public `freeMaps_measurable F` conjunction, exactly as frozen in the production contract.

These are finite algebra/summability/map identifications to be proved by the producer from the actual definitions. They are not new frame premises or desired probabilistic certificates. The helper itself assumes no independence, Gaussian law, rank, covariance inverse, r≠0, n>0, or posterior identity. The only source-law hypothesis in its probabilistic propositions is the existing `hL : L ≠ 0`. The raw-kernel field is not needed for this Gaussian part; it is used by the producer's separate deterministic posterior reconstruction.

## Complete proof route and no scalar shortcut

Each standard scalar marginal is obtained **only** by the accepted public `unitDirection_hasLaw` after rewriting the exact free-coordinate map and supplying the producer's finite-support/Gram norm identities. No new scalar mean/variance/Gaussian proof chain is copied.

Independently, one general finite-row construction uses rows indexed by `Fin n ⊕ I`: every finite chi row and every original coefficient singleton row. Public `scalarSeries_finite_hasGaussianLaw`, actual smooth-carrier `observation_map_eq`, and a finite coordinate-selection CLM give joint Gaussianity of the **entire** free vector and each original finite coefficient cylinder. The vector's joint Gaussianity is its first marginal, including n=0.

Public `scalarSeries_covariance` plus the producer's finite pairing/tsum identity gives the full Gram covariance. Public Gaussian zero-covariance independence gives `iIndepFun` for the coordinates of this jointly Gaussian vector. Only then are the reused scalar standard laws combined using `iIndepFun.map_fun_eq_pi_map` to obtain the entire iid `Measure.pi` law. Separate scalar marginals are never treated as a joint law.

A private finite CLM subtracts the sum over **every** free index from each coefficient cylinder. Mapping the whole jointly Gaussian pair through that CLM gives joint Gaussianity of the vector and the actual finite residual cylinder. Public scalar/coefficient covariance, finite covariance sums, and Gram delta make every vector/residual cross-covariance zero. This supplies vector-versus-cylinder independence.

`IndepFun.indepFun_process` then quantifies all finite original-mode cylinders to obtain independence from the whole residual coefficient process. Finally the public measurable sample projection/retraction is composed with that process, and its pointwise left-inverse identity on the literal residual sample identifies the whole `SmoothSample 2 L` residual. The first factor is neither an erased sample nor a separate Gaussian model with matching covariance.

The public final proposition is exactly `freeResidual_freeCoordinate_joint_map`, with **residual first** and the full iid Gaussian vector second. The result uses `.symm` on the established vector/sample independence before the product-map theorem. The entire construction works for Fin0 through the same statements; no positive-dimension branch or premise is inserted.

## Authored inventory supplied by this section

One private data definition: `freeGaussian_projection`, the finite projection CLM.

Thirteen private propositions:

1. `freeGaussian_scalar_hasLaw`.
2. `freeGaussian_finiteCoefficients_hasGaussianLaw`.
3. `freeGaussian_vector_hasGaussianLaw`.
4. `freeGaussian_covariance_gram`.
5. `freeGaussian_coefficient_covariance`.
6. `freeGaussian_iIndepFun`.
7. `freeGaussian_pi_map`.
8. `freeGaussian_projection_apply`.
9. `freeGaussian_finiteResidual_hasGaussianLaw`.
10. `freeGaussian_residual_zero_covariance`.
11. `freeGaussian_finiteResidual_indepFun`.
12. `freeGaussian_process_indepFun`.
13. `freeGaussian_sample_indepFun`.

Exactly one authored public proposition: `freeResidual_freeCoordinate_joint_map`. There is no extra public independence/covariance/raw-kernel-product/null-section theorem, no explicit mode control and no posterior rewrite in this helper. The producer's final exhaustive inventory must include generated declarations as well as these authored names.

## Pinned accepted API text read

All source paths are in the existing packet `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025` and its pinned `.lake/packages/mathlib/Mathlib`:

- `SourceCurvatureDecomposition.lean:273–302`: `unitDirection`, its measurable/standard law, and public coefficient covariance.
- `SourceSmoothConditionalKernel.lean:36`: `exists_measurable_sampleProjection`, with pointwise left inverse on every smooth sample.
- `SourceSmoothConditionalKernel.lean:363,377,475`: general `scalarSeries_finite_hasGaussianLaw`, `scalarSeries_single`, and `coefficient_hasGaussianLaw`; these are in `I4SourceSmoothConditional`, not a new Gaussian namespace.
- `inputs/SourceSmoothCarrier.lean`: public `observation_map_eq`, `covariance_comp_inclusion`, smooth-law normalization and original inclusion measurability, whose accepted mathematics is reused.
- `inputs/SourceCovariance.lean:13`: public `scalarSeries_covariance`.
- `Probability/Distributions/Gaussian/HasGaussianLaw/Independence.lean:261,339`: jointly Gaussian coordinate iIndepFun and whole vector/cylinder zero-cross-covariance independence.
- `Probability/Independence/Basic.lean:840,703,756`: iid pi-map, residual-first product-map and measurable composition.
- `Probability/Independence/Process/Basic.lean:351`: whole process independence from all finite cylinders.
- `Probability/Moments/Covariance.lean:139,190,271`: constant multiplication, subtraction and finite-sum covariance.
- `MeasureTheory/Function/LpSeminorm/TriangleInequality.lean:148`: nondeprecated `memLp_finsetSum`.
- `Topology/Algebra/Module/ContinuousLinearMap/PiProd.lean:219,238`: finite pi/projection evaluation. The supplied text uses `_root_.sum_apply` and `_root_.smul_apply`, avoiding deprecated CLM aliases.

Only read-only accepted API lookup and new text writing occurred. No Lean/name probe/test/build/check/kernel/audit/control campaign or object creation was performed. No old payload was hashed, no packet source was edited, and no Git/cache/shared metadata/configuration/external action occurred. All earlier helper/review directories are unchanged. No58 source or in-flight55 source/helper was inspected or consumed.

The needed new text/import/provenance identities are recorded once before one integration. The final producer-integrated module, including any necessary local amendments, is the sole qualification target. No standalone helper qualification or mathematical/scientific credit is claimed. Owner `/workspace/AGENTS.md` requires completed applicable verification to be reused; pending different-family/process work remains separate and cannot erase that evidence. Scientific effect **NONE**; same-family/provider-distinct credit **0**.

Canonical onward authority carried from the published control contract, without claiming link reading:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
