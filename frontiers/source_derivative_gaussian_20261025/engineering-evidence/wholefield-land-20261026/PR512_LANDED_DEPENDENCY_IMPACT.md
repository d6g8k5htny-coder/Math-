# Landed PR513 dependency impact on the still-open PR512 disposition

Scope: read-only reconciliation against the accepted landed-main snapshot `180d6406b0a51b268a152241a70bde6a1b39a142`. This report supplies newly material dependency facts. It does not take an incident/integration seat, decide keep versus revert, dispose of a16, recommend a disposition, or authorize rollback.

## New material fact

PR513 is now legitimately on main. Its source-specific modules `SourceSmoothConditionalKernel`, `SourceSmoothPalm`, and `SourceConditionalMajorant` each transitively require **all 37 Lean source files added by PR512 inside `frontiers/source_derivative_gaussian_20261025/`: 14 baseline modules and 23 fixed inputs**. The fourth PR513 module, `GaussianWeightedMajorants`, imports only Mathlib and has no local PR512 source dependency. Keeping the four later module files while deleting PR512's baseline would therefore retain source files with unresolved imports; it would not preserve the landed source package.

This supersedes earlier descriptions limited to open PR513/PR514 readiness: the affected whole-field source is already accepted main content. PR513's successful later integration and green checks do not erase the earlier PR512 process breach or supply an owner/CoS keep-versus-revert or a16 disposition. No owner/CoS disposition is observed in the supplied evidence. Gov33's integrated note is record-only.

Record-accuracy correction: the later-supplied native PR512 comment https://github.com/d6g8k5htny-coder/Math-/pull/512#issuecomment-6408015044 was posted at04:09, after the prior04:08 snapshot. In that comment, the Cursor parent calls **its own obligation** closed-as-KEEP on the stated grounds of tip retention and no authorized revert. It expressly leaves a16 and the CoS board receipt open and says no Cursor revert occurred. This report records that claimant and limited scope without adopting or adjudicating the claim. Retained ancestry or the absence of an authorized revert is not treated here as authority for an owner/CoS disposition. This correction changes no landed180 dependency finding and warrants no repeated graph or mathematical verification.

## Immutable composition and evidence used

- PR512 merge: `8b5451059903997a1956c3a9c52f02cf09928bef`; ordered parents `b29c4b769cac85437b409d152651d5cce4140015`, `f0cba7dcaec2a5a9ce54bf8d8e6bda06340184b7`. The analyzed inverse is specifically its first-parent delta.
- PR513 legitimate merge at 2026-10-26 04:45:03 UTC: `180d6406b0a51b268a152241a70bde6a1b39a142`; ordered parents `1cba5115253d43e1e46caa7e0381fcb3f6108cbd`, `c0c92e7241f6ed41770b0fb6896b483d1c2ed2b0`; tree `cf3e699e9deb25a7ce1b12b92b1c2f50dd3ba82f`.
- The existing integration report `/workspace/scratch/wholefield-integration/REPORT.md` supplies the completed gate evidence: independent engineering composition COMMENT5647406155; reused scoped Claude scientific PASS6405469445; actual Codex auto-review6408330630/receipt6408348162 with no findings; exact tested composition; all four landed180 check-runs successful at its final 04:49 read. That evidence is reused, not rerun here.
- The landed package manifest enumerates 18 source modules and 292 target declarations. Completed applicable mathematical verification and its independent scoped review remain reusable under `/workspace/AGENTS.md`. Provider-distinct review/process obligations are tracked separately and do not make established mathematics unverified.

The local object database initially lacked180. A permitted immutable fetch of exactly180 supplied the missing Git objects without updating a branch or checked-out file (`--no-tags --no-write-fetch-head`). Analysis used commit metadata, path deltas and textual imports; no Lean, kernel, audit, control or unchanged-source hash verification was run. No revert operation or simulated revert was run.

## Exact import dependency

Let `S = frontiers/source_derivative_gaussian_20261025/`. Paths below resolve through this package's own `lakefile.toml`: baseline modules at `S`, and its `SourceDerivativeInputs` library at `S/inputs`. Matching module names in other independently configured frontier packages do not provide implicit replacement imports.

| Landed PR513 module | Direct local imports at180 | PR512-added source paths in transitive closure |
| --- | --- | ---: |
| `SourceSmoothConditionalKernel.lean` | line1 `SourceEndpointEstimates` | 37 |
| `SourceSmoothPalm.lean` | line1 `SourceSmoothConditionalKernel` | 37 |
| `GaussianWeightedMajorants.lean` | none; all imports are Mathlib | 0 |
| `SourceConditionalMajorant.lean` | lines1–3 `SourceSmoothConditionalKernel`, `GaussianWeightedMajorants`, `SourceSmoothPalm` | 37 |

The principal baseline edges are explicit:

- `SourceEndpointEstimates:1–7` imports `SourceEndpointParameters`, `SourceConfluentLimits`, `SourceContactEndpointParameters`, `SourcePhysicalEndpointKernel`, `GaussianRegressionLimits`, `ResearchFormalCoreR1.GaussianNormalizerLimit`, `ResearchFormalCoreR1.PalmReweighting`.
- `SourceEndpointParameters:1` imports `SourceEndpointRegression`; `SourcePhysicalEndpointKernel:1` imports `SourceEndpointParameters`.
- `SourceConfluentLimits:1–5` imports `SourceEndpointRegression`, `SourceDerivativeContinuity`, `SourceContactSchur`, `SourceContactEndpointParameters`, `ConfluentIntegralIdentities`.
- `SourceEndpointRegression:1–2` imports `SourceConfluentPins`, `ResearchFormalCoreR1.GaussianRegressionKernel`; `SourceConfluentPins:1` and `SourceDerivativeContinuity:1` import `SourceDerivativeGaussian`.
- `SourceContactEndpointParameters:1` imports `SourceContactSchur`; `SourceContactSchur:1` imports `SourceContactCovariance`; `SourceContactCovariance:1–2` imports `SourceDerivativeGaussian`, `ContactJetCovariance`; `SourceDerivativeGaussian:1` imports `SourceSmoothCarrier`.
- `ResearchFormalCoreR1.GaussianNormalizerLimit:1–3` imports `GaussianCoupling`, `NormalizerFloor`, `EndpointNormalizerBridge` in that namespace. The latter imports `EndpointGaussianMoments` and `NormalizerFloor`; the former endpoint module imports `GaussianJetMoments`, which imports `DeterminantMoment` and `GaussianScalarMoments`. `NormalizerFloor` imports `GaussianNormalizer`.
- `SourceSmoothCarrier` imports `SourceSmooth`, `SourceGaussianLaw`, `SourceCovariance`, `SourceTorusC4`. Their local import chain reaches the remaining fixed source-realization inputs listed below.

The exact 37-file mathematical import closure, all introduced by512, is:

```text
S/ConfluentIntegralIdentities.lean
S/ContactJetCovariance.lean
S/GaussianRegressionLimits.lean
S/SourceConfluentLimits.lean
S/SourceConfluentPins.lean
S/SourceContactCovariance.lean
S/SourceContactEndpointParameters.lean
S/SourceContactSchur.lean
S/SourceDerivativeContinuity.lean
S/SourceDerivativeGaussian.lean
S/SourceEndpointEstimates.lean
S/SourceEndpointParameters.lean
S/SourceEndpointRegression.lean
S/SourcePhysicalEndpointKernel.lean
S/inputs/GaussianSeriesFoundation.lean
S/inputs/SpectralWeights.lean
S/inputs/SourceFourierSeries.lean
S/inputs/SourceC4.lean
S/inputs/SourceGaussianLaw.lean
S/inputs/SourceLattice.lean
S/inputs/SourceKernel.lean
S/inputs/SourceCovariance.lean
S/inputs/SourceTorus.lean
S/inputs/SourceTorusC4.lean
S/inputs/SourceSmooth.lean
S/inputs/SourceSmoothCarrier.lean
S/inputs/ResearchFormalCoreR1/DeterminantMoment.lean
S/inputs/ResearchFormalCoreR1/EndpointGaussianMoments.lean
S/inputs/ResearchFormalCoreR1/EndpointNormalizerBridge.lean
S/inputs/ResearchFormalCoreR1/GaussianCoupling.lean
S/inputs/ResearchFormalCoreR1/GaussianJetMoments.lean
S/inputs/ResearchFormalCoreR1/GaussianNormalizer.lean
S/inputs/ResearchFormalCoreR1/GaussianNormalizerLimit.lean
S/inputs/ResearchFormalCoreR1/GaussianRegressionKernel.lean
S/inputs/ResearchFormalCoreR1/GaussianScalarMoments.lean
S/inputs/ResearchFormalCoreR1/NormalizerFloor.lean
S/inputs/ResearchFormalCoreR1/PalmReweighting.lean
```

In particular, the determinant modules used by513 are the **vendored input copies under `S/inputs/ResearchFormalCoreR1`**, not live imports from the separate `frontiers/determinant_moment_20261025` package. Restoring only the latter package would not restore513's configured imports.

## What reversing PR512's first-parent delta targets

The immutable delta `b29c4b7 → 8b54510` contains **759 paths: 753 additions and six existing-path modifications**, exclusively in two frontier packages:

| Package |512 additions targeted for deletion|512 existing modifications targeted for reversal|
| --- | ---: | ---: |
| `frontiers/determinant_moment_20261025/` |254|6|
| `S/` |499|0|
| Total |753|6|

Of the753 added paths,748 have no subsequent path-content change between512 and landed180. These include **all47 added `.lean` source files**: ten determinant-package Gaussian modules plus the37-file `S` closure above. They also include the source packet's original evidence, input bindings, origin manifest, pinned build files, and source contracts. The inverse delta targets these for deletion; the 512-modified determinant aggregator is separately restored to its prior content.

The only five512-added paths subsequently edited on main are:

```text
S/README.md
S/SCOPE.md
S/SOURCE_MANIFEST.json
S/SOURCE_SHA256SUMS
S/lakefile.toml
```

They were added by512 and modified by513, so an ordinary Git inverse encounters an add-then-later-modified deletion situation requiring reconciliation (normally modify/delete conflicts). This report derives that overlap from immutable path/content deltas; it does not claim an executed revert or conflict-resolution result. Discarding the five paths would discard513's package documentation/qualification inventory and its library/default-target configuration as well.

The six pre-existing paths whose512 changes the inverse targets are:

```text
frontiers/determinant_moment_20261025/LINEAGE_VALIDATION.md
frontiers/determinant_moment_20261025/README.md
frontiers/determinant_moment_20261025/ResearchFormalCoreR1.lean
frontiers/determinant_moment_20261025/SCOPE.md
frontiers/determinant_moment_20261025/blueprint/src/content.tex
frontiers/determinant_moment_20261025/manifest.json
```

None has a subsequent content delta between512 and180. The aggregator change is precisely removal of the ten added Gaussian-module import lines; its prior `AlgebraV2`, `ProbabilityCompanionsV2`, and `DeterminantMoment` imports remain. Existing pre512 determinant source files themselves are not deletion targets.

PR513's actual delta has161 new paths and the five modifications above. Its four new `.lean` modules, new field contracts/catalog, and field-evidence paths are not512 delta paths and therefore are not direct deletion targets of the inverse. A revert commit would preserve later commit ancestry, including513, while potentially breaking the source content on which those later files rely. Preserved descendant history alone is insufficient to preserve their usable composition.

## Constraints and smallest source-preserving shapes for a separately authorized rollback

Any separately authorized disposition that promises to preserve513 must explicitly reconcile:

1. All37 listed baseline/input source paths at their accepted scientific identities, or an independently justified replacement import arrangement; the three source-specific513 modules; and the independently Mathlib-only majorants module.
2. The current package configuration for18 source modules and23 inputs, pinned Mathlib/toolchain/manifest dependencies, and the five shared paths with513 edits. Retaining only37 Lean files without their configured package would not preserve the accepted composition.
3. Original verification failures/successes, source contracts, input/origin binding records, manifests and catalogs, and the513 field evidence. Historical origin commits remain historical provenance even if a separate current package is removed. Evidence reuse and provider/process disposition must remain explicit.
4. Later main descendants and any planned PR514 base/content reconciliation. The supplied PR514 state is31 qualified modules/866 declarations/25 inputs at main-base19d2608, with66037 a local contract-only change. That is separate from513's landed18-module/23-input package; no514 readiness or source requalification was performed here.

Two small, reviewable source-preserving shapes are available for an authorized owner to assess; neither is chosen or authorized by this report:

- **A scoped inverse with explicit retained dependencies.** Exclude the accepted513 dependency packet and its necessary build/provenance/evidence paths from deletion, retain the current513 edits in the five shared paths, and describe exactly which other512 effects are being reversed. Keeping the complete existing `S` packet is easier to review than silently pruning its evidence; the mathematical minimum is the37-path closure, not a complete packaging/retention policy. If the separate determinant packet is reversed while `S` survives, its vendored input copies must remain; those inputs do not resolve against the determinant packet automatically. This is a partial512 reversal and needs an explicit disposition that permits that scope.
- **An explicitly coupled inverse and readmission/restoration.** If policy requires a full512 inverse in history, separately authorize and review restoration/readmission of the same source closure with its configuration, bindings and evidence so that the final candidate tree preserves513. The combined final composition, intermediate-state handling and provenance must be made reviewable before integration. Calling this a restoration does not cure the original unsupported merge or waive any provider-distinct review requirement. Unchanged mathematical evidence remains reusable; only actual changed composition/dependencies or uncovered obligations justify additional verification.

Removing the37 baseline paths while preserving513's behavior would instead require an explicit replacement/relocation/import change and applicable review. It is not achieved by ordinary revert semantics and is not proposed or implemented here.

## Activity boundary

Only this report was written, including the later supplied-comment record-accuracy correction. No source, original worktree, checked-out branch, commit, merge, revert, issue/PR comment, role reservation, process disposition, scientific-status field, or CI setting was changed. No agents were spawned. The only Git mutation was the expressly permitted immutable-object fetch. No unrelated517/RBO/other-repository assessment was undertaken.
