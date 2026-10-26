# Actual whole-carrier Gaussian conditioning: frozen source contract

Frozen before implementation,25October2026, OpenAI/Codex root and
/root/uniform_jet_moment_sources. Scientific effect NONE; original goal ACTIVE.

Base7a2ee81ecb088813b7c6f8cd383d66acb2c7f773. Sole production ownership:
SourceSmoothConditionalKernel.lean in the isolated worktree
/workspace/Math-wholefield-20261025/frontiers/source_derivative_gaussian_20261025.
No edits to the delivered14modules or23input sources. Completed baseline
verification/artifacts are reused; new worktree/session is not a reason to
rerun them. Only new code/affected obligations receive new checks.

Bounded native claim: main#539/6404338072. Checkpoint23:15UTC;
terminal2026-10-26T00:00UTC. Existing Claude01Cz source review and other
owners' lanes remain theirs. Different-family scientific review is separate.

The source/API proposal below is adopted as the preimplementation contract.
Its exact summability, measurability, independence, all-pin and null-pin
compatibility obligations are mandatory; none may be replaced by the desired
conclusion as a premise. Path references below identify the preserved source
at the base; the implementation uses this isolated checkout's same files.

## Fixed actual objects

Work at fixed `L : ℝ` with `hL : L ≠ 0`, and fixed `r : ℝ`. Let

- `M := I4Source.SourceMode 2`;
- `S := I4SmoothCarrier.SmoothSample 2 L`;
- `μ := I4SmoothCarrier.smoothLaw 2 L`;
- `X := I4SourceEndpointRegression.sourceConfluentPinsAt L r`;
- `a i m := I4SourceConfluentLimits.pinCoefficient L r i m`;
- `G := I4SourceEndpointRegression.sourcePinCovarianceAt L r`.

Every source object above is the already-defined literal source object. No new Gaussian field,
conditional realization, independence premise, or full-field/Palm identification is introduced.

For `y : Fin 6 → ℝ`, define the coefficient lift

`lift y m := ∑ i, a i m * ((G⁻¹ *ᵥ y) i)`.

Define `posteriorSample x ω : S` by the literal coefficient identity

`(posteriorSample x ω).val m = ω.val m + lift (x - X ω) m`.

The subtype proof is an obligation to prove, not an assumption: for every order `n` and row `i`,
`orderModeBound n 2 L` and `|a i|` are summable; their product is summable by the existing
`I4ContactGram.coefficient_product_summable`. Finite scalar combinations and the triangle
inequality give every-order `goodSample` preservation. Joint measurability of `(x,ω) ↦
posteriorSample x ω` follows from the exact series formula for `X`, coordinatewise
measurability, finite linear algebra, and `Measurable.subtype_mk`.

Also expose new per-sample summability helpers
`Summable (fun m => a i m * ω.val m)` and the analogous adjusted coefficient theorem.
These follow from `ω.property` and derivative majorants before applying the finite
observation CLM. The existing exact series proofs already contain that argument in
private helpers (`SourceConfluentLimits.lean:51` and `:64`); a small new generic helper
is needed because those helpers are private. An equality of `tsum` values alone must
not be used as if it proved summability when establishing shift linearity.

## Proposed bounded new module

Suggested sole file: `SourceSmoothConditionalKernel.lean`.
Suggested namespace: `I4SourceSmoothConditional`.
Import the completed source coefficient/regression modules and the narrow new Mathlib import
`Mathlib.Probability.Independence.Process.Basic`. The eventual hL-only specialization may
import completed `SourceEndpointEstimates`; no existing file needs alteration.

Define a Markov kernel from the actual law by

`K := (Kernel.id ×ₖ Kernel.const (Fin 6 → ℝ) μ).map
        (fun p => posteriorSample p.1 p.2)`.

Required exports, with exact mathematical content:

1. Actual carrier preservation, joint measurability, `IsMarkovKernel K`, and
   `∀ x, K x = μ.map (posteriorSample x)`.
2. With `hG : IsUnit G`, exact pin reconstruction for all samples and all pin values:
   `∀ x ω, X (posteriorSample x ω) = x`.
   Consequently `∀ x, (K x).map X = Measure.dirac x`, equivalently full mass on the
   literal measurable fiber `{ω | X ω = x}`.
3. With `hG`, `HasCondDistrib (id : S → S) X K μ`.
   The conclusion is proved from actual Gaussian coefficients and actual coefficient Gram;
   no residual Gaussianity or independence premise is accepted.
4. For every measurable `F : S → E`, the direct corollary
   `HasCondDistrib F X (K.map F) μ`.
   Thus arbitrary events in the actual carrier sigma algebra and measurable field
   functionals can be conditioned by this specified version.
5. With `hG`, all-pin endpoint compatibility:
   `∀ x, (K x).map (sourceAdjustedEndpoints L r) = sourceEndpointKernel L r x`.
   This is an exact equality for every pin value, including prescribed null pins.
6. The actual eventual specialization has only `hL`:
   `∀ᶠ r in 𝓝[>] (0 : ℝ), HasCondDistrib id (sourceConfluentPinsAt L r) (K L r) μ`.
   The existing `(sourceEndpoint_parameter_limits hL 0).1` supplies actual eventual
   invertibility; the fixed-r `hG` premise is not retained in this final specialization.

At `x = sourcePrescribedPins r b`, item 2 and the existing exact pin-fiber theorem then
give compatibility with the literal normalized physical endpoint vector. Either include
that corollary here or compose it in a separate owner-approved module.

## Proof of the genuine infinite-dimensional obligation

Let `R ω := posteriorSample 0 ω`. For every finite set `I : Finset M`, prove joint
Gaussianity of `(X, fun m : I => (R ω).val m)`. Each coefficient coordinate is a scalar
series with a Kronecker coefficient, and every pin is its actual summable coefficient
series. The already-proved finite scalar-series Gaussian theorem gives their joint law;
finite linear maps give the residual law. The actual covariance identity is

`Cov(ω_m, X_i) = a i m`.

Together with `G⁻¹ G = 1`, this yields zero cross covariance of `R` and `X`.
`HasGaussianLaw.indepFun_of_covariance_eval` gives independence for each finite residual
vector and the full pin vector. Upgrade with
`IndepFun.indepFun_process` (or its a.e. variant), then transport independence from
coefficient inclusion to the subtype using the measurable retraction supplied by
`MeasurableSet.exists_measurable_proj`. The good set is nonempty because it contains
the zero coefficient sample.

The residual coordinates are generally correlated with each other. `iIndepFun` of
residual coordinates is neither needed nor claimed. Individual-coordinate independence
from `X` alone is insufficient: every finite residual vector must be handled.

The generic existing `regression_pair_hasCondDistrib` accepts an arbitrary residual
measurable space, so apply it to `R : S → S`. Reconstruct by the jointly measurable
map `(x,ρ) ↦ ρ + lift x` on the carrier, which equals the original sample at
`(X ω,R ω)` for every sample. `HasCondDistrib.comp_left` produces item 3.
The direct-shift kernel and this residual/reconstruction kernel agree by map composition.

For item 5, prove pointwise

`V (posteriorSample x ω) = V ω + C *ᵥ (G⁻¹ *ᵥ (x - X ω))`,

where `V = sourceAdjustedEndpoints L r` and `C = sourceCrossCovarianceAt L r`.
The already-proved exact adjusted series and cross-Gram identities justify interchanging
the finite sum and the absolutely convergent coefficient pairing. This identifies the
pushforward with the existing literal affine endpoint kernel for every x.

## Exact existing evidence and APIs to reuse, without rerunning

Packet: `/workspace/Math-/frontiers/source_derivative_gaussian_20261025`.

- `inputs/SourceSmooth.lean:101`: `orderModeBound_summable`; `:181`: every-order `goodSample`.
- `inputs/SourceSmoothCarrier.lean:63`: measurable good set; `:85`: actual subtype;
  `:99`: inclusion pushes actual smooth law to original product law;
  `:116`: all measurable observation-law transport; `:162`: covariance transport.
- `SourceConfluentLimits.lean:45,48`: actual pin/adjusted coefficients;
  `:118,124`: their summability; `:130,142`: exact every-sample series;
  `:154,163,173`: actual G/C/B product sums. Completed source SHA256
  `1635a05bbd5b56608bc0a1a04eb4404c2df4601f1255f5846c1342a597bf5b0b`.
- `ContactJetCovariance.lean:80`: `coefficient_product_summable`.
- `SourceDerivativeGaussian.lean:123`: actual standard-product finite scalar-series
  joint Gaussian theorem. It currently uses `Fin n`; finite subtype reindexing is a
  bounded new helper, not a missing mathematical assumption.
- `inputs/SourceCovariance.lean:13`: exact scalar-series covariance.
- `inputs/ResearchFormalCoreR1/GaussianRegressionKernel.lean:43`:
  `regression_pair_hasCondDistrib`, generic in the residual space.
- `SourceEndpointRegression.lean:151`: all-pin literal endpoint kernel formula;
  `:162`: existing finite endpoint HasCondDistrib theorem.
- `SourceEndpointEstimates.lean:192`: actual eventual pin-covariance invertibility.

Pinned Mathlib at `.lake/packages/mathlib`:

- `Probability/Independence/Process/Basic.lean:330,341,351,363`:
  `process_indepFun`, its a.e. variant, `indepFun_process`, its a.e. variant.
  These use all finite restrictions and do not assert mutual coordinate independence.
- `Probability/Distributions/Gaussian/HasGaussianLaw/Independence.lean:339`:
  `HasGaussianLaw.indepFun_of_covariance_eval`, arbitrary finite coordinate types.
- `MeasureTheory/MeasurableSpace/Embedding.lean:87`: measurable subtype inclusion;
  `:171`: `MeasurableSet.exists_measurable_proj`.
- `Probability/HasCondDistrib.lean:38`: definition via joint law/compProd;
  `:67`: `HasCondDistrib.comp_left`.
- Optional RCD comparison only: `MeasureTheory/Constructions/Polish/Basic.lean:154`
  gives countable-product standard Borel; `:1110` gives measurable-subset standard Borel.
  `Probability/Kernel/CondDistrib.lean` gives an abstract regular conditional law, with
  uniqueness only almost everywhere in the pin law. It cannot establish a chosen
  value at a prescribed probability-zero pin.

## Boundaries and remaining costs

No mathematical obstruction was found. No infinite-dimensional normed Gaussian API,
Cameron–Martin theorem, or abstract disintegration theorem is required for the direct kernel.
Formalization costs are finite-index reindexing, exact scalar-series shift algebra,
joint subtype measurability, and finite-to-process independence. These are genuine
new proof obligations, not completed merely by this proposal.

The result conditions the existing measurable coefficient/smooth carrier. A separate
chosen topological C∞ function-space law, geometric-event measurability, Morse/elder/
counting properties, and identification with a geometric Palm law are not supplied by
this module. In particular an arbitrary event measurable only in a completed measure
space does not automatically become an event of the carrier sigma algebra: its
measurability must be stated or proved in the intended measurable space.

Research performed by source/API inspection only. No old checks or builds rerun,
no production files edited, and no new Lean verification claimed for this proposal.
