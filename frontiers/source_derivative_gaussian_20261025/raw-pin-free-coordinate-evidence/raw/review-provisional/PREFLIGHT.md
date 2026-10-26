# SourceRawPinFreeCoordinates: independent read-only preflight

26 October 2026. OpenAI/Codex `/root/actual_canonical_partner_preflight`, delegated by `/root`. **UNCLAIMED future-contract assessment only.** Only this new report is written. No code, helper section, harness, probe, Lean invocation, build, test, control, audit, kernel, hash campaign, Git/cache/shared-metadata action or external action. Source55/56 code and helpers were not inspected. Earlier preflight directories are unchanged. Root retains prospective contract, concrete-control freeze, native pickup, PRECODE/GO, implementation routing, qualification and publication ownership.

## Decision

The proposed bounded surface is feasible with the accepted public APIs. No mathematical or API-level blocker was found. The genuinely new result is the **whole finite Gaussian vector independent of the whole literal projected residual sample**, expressed as the residual-first joint pushforward. It is not already proved by the old scalar-own-residual statements, and it must not enter `RawPinFreeFrame` as an assumption.

No implementation is authorized by this report. The stated serial publication and root's proper PRECODE/native-pickup/GO remain future prerequisites. The original research goal stays active; scientific effect NONE; same-family/different-provider credit 0. Different-family scientific/process requirements remain separate from completed applicable mathematical verification.

## Inputs read and evidence reused

Read the three requested design/readiness artifacts:

- `/workspace/scratch/raw-pin-free-coordinate-preflight/REPORT.md`.
- `/workspace/scratch/raw-pin-free-coordinate-controls-preflight/REPORT.md`.
- `/workspace/scratch/raw-pin-free-coordinate-construct/READINESS.md`.

Read only the relevant named accepted source and pinned Mathlib API declarations below. These readings are interface assessment, not re-verification of their mathematics. `/workspace/AGENTS.md` remains controlling: reuse completed applicable verification; no new reviewer, handoff, source cut or pending process requirement justifies repeating unchanged checks. Any later check must identify its actual changed or uncovered scope.

Onboarding reports published qualified scope through source54 at `72eb5de8`, source55 final-control qualification in progress and source56 full mathematical/root/final-review PASS with serial publication pending. Those supplied statuses are not independently re-established or modified here.

All packet-relative source paths below refer to `frontiers/source_derivative_gaussian_20261025/` in `/workspace/Math-curvature-20261026`. Pinned Mathlib is the existing `d13f23b723b8a846827a245b89c10fc7d3f11612`, Lean `v4.34.1`; no toolchain/cache operation occurred.

## Exact surface and scope

Root's prospective module/namespace is `SourceRawPinFreeCoordinates` / `I4SourceRawPinFreeCoordinates`. Preserve its selected **Z** name if frozen; `freeCoordinate` in the older design notes is only a prior proposed spelling.

The surface can remain precisely one structure, three maps and three authored public propositions:

1. `RawPinFreeFrame L r n`: deterministic `χ : Fin n → (SourceMode 2 →₀ ℝ)`, Gram delta, and zero pairings of each of the six original raw observation rows against each direction. Use the public `finitePairing` in **observation-times-direction** order. No law, independence, desired reconstruction, residual-rank or genericity field.
2. Maps `Z`, `freeShiftSample`, `freeResidualSample`. The combined finite lift is private. The residual is coefficientwise subtraction of **every** free projection term, not erasure on the support union.
3. One proposition bundles `Measurable Z`, joint measurability of the shift in `(z,sample)`, and measurability of the residual. A second states the residual-first product map with the whole iid standard-Gaussian `Fin n → ℝ` vector. A third states the pointwise all-target raw posterior reconstruction at sample level.

“Exactly three public propositions” concerns authored public results; a structure necessarily generates field projections/recursors and the final declaration inventory must still account for them. Keep finite-linear-map/cylinder/covariance/process/retraction support private. There is no current need for additional public Fubini, raw-kernel product-pushforward, scalar-independence, zero-residual-coordinate or reconstruction lemmas. Consumers can derive such consequences from the selected statements when needed.

The maps and measurability are valid for every real L and r from finite carrier arithmetic. The law and posterior reconstruction use the existing necessary `hL : L ≠ 0`. Neither may gain `r ≠ 0`, a nonsingular pin covariance, or `n > 0`. This is for each supplied deterministic frame at fixed L,r; do not silently assert measurability of a parameterized frame selection as L,r vary.

The law must literally read, in mathematical notation,

`(smoothLaw 2 L).map (sample ↦ (R sample, Z sample)) = ((smoothLaw 2 L).map R).prod (Measure.pi (_ : Fin n ↦ gaussianReal 0 1))`.

The pointwise reconstruction is, for **all** full targets t, samples ω and real r,

`rawPosteriorSample hL r t ω = freeShiftSample (Z ω) (rawPosteriorSample hL r t (R ω))`.

This unrestricted-target algebra is valid even at singular r=0. It asserts no singular-radius conditional-distribution identification, fiber support, posterior genericity, conditional Morse conclusion or existence of a useful frame for every parameter. The earlier positive-gap restriction for a future conditional-Morse theorem does not restrict these algebraic identities or Gaussian free-coordinate laws.

## Accepted APIs: sufficient joins and real obligations

| Exact public API | Application and boundary |
|---|---|
| `I4SourceFinitePinKernel.finitePairing`, `SourceFinitePinKernel.lean:17` | A row paired with a finitely supported original direction; finite linearity is a small new application. |
| `finiteShiftSample`, `finiteShiftSample_val`, same source:96,105 | Literal coefficient addition preserving the original all-order smooth subtype, for every L. No fresh summability theory is required. |
| `rawPins_finiteShiftSample`, same source:123 | Exact response of all six raw rows, every real r. |
| `rawPosteriorSample_finiteShiftSample`, same source:139 | Sample equality at every target/radius from zero raw pairings; no covariance-invertibility premise. This is the entire deterministic posterior engine needed. |
| `I4SourceSmoothConditional.scalarSeries_finite_hasGaussianLaw`, `SourceSmoothConditionalKernel.lean:363` | Arbitrary finite row index τ and summable deterministic rows on `coefficientLaw`. This supplies the new **joint**, not merely marginal, Gaussian construction. |
| `I4SmoothCarrier.observation_map_eq`, `inputs/SourceSmoothCarrier.lean:116` | Transfers the measurable finite-row observation law to the same `smoothLaw` subtype. |
| `I4SourceCovariance.scalarSeries_covariance`, `inputs/SourceCovariance.lean:13`; `covariance_comp_inclusion`, `inputs/SourceSmoothCarrier.lean:162` | Accepted covariance engine/transport. Finite support and Gram identify the actual finite sums. |
| `I4SourceCurvatureDecomposition.unitDirection_hasLaw`, `SourceCurvatureDecomposition.lean:285` | Gives each normalized summable free scalar its exact standard-Gaussian marginal after pointwise identification. This can avoid a new scalar mean/variance proof chain. It supplies no vector independence by itself. |
| `HasGaussianLaw.indepFun_of_covariance_eval`, Mathlib `Probability/Distributions/Gaussian/HasGaussianLaw/Independence.lean:339` | Jointly Gaussian finite vector pair plus all cross-coordinate covariance zero gives independence of the entire two vectors. Empty index types are allowed. |
| `HasGaussianLaw.iIndepFun_of_covariance_eq_zero`, same source:261 | Whole free-vector joint Gaussianity plus off-diagonal covariance zero yields joint coordinate independence. Its finite-index hypothesis allows `Fin 0`. |
| `iIndepFun.map_fun_eq_pi_map`, Mathlib `Probability/Independence/Basic.lean:840` | Joint independence and measurable marginals give the entire vector's product law. Combine with the preceding public scalar marginal law. |
| `HasGaussianLaw.map_eq_gaussianReal`, Mathlib `Gaussian/HasGaussianLaw/Basic.lean:78` | An alternative scalar marginal route if useful; it requires actual mean/variance identification and is not necessary when `unitDirection_hasLaw` is reused. |
| `IndepFun.indepFun_process`, Mathlib `Probability/Independence/Process/Basic.lean:351` | Requires measurable whole vector, measurable residual coordinates, and independence from **each finite residual cylinder**. Gives independence from the entire original-mode coefficient process. No reduction to separate scalar independence is licensed. |
| `exists_measurable_sampleProjection`, `SourceSmoothConditionalKernel.lean:36` | A measurable retraction from coefficient functions onto smooth samples, pointwise identity on every included smooth sample. Composing it identifies the literal residual sample, not just a distributionally equivalent replacement. |
| `IndepFun.map_prod_eq_prod_map_map`, Mathlib `Probability/Independence/Basic.lean:708` | With the established measurability/finite measure, yields exact joint pushforward; swap independence first to obtain residual-first order and replace the proved Z marginal. |

For a finite original mode set I, use rows indexed by `Fin n ⊕ I`: every free χ row and the coordinate single rows for modes in I. Finite support supplies summability. The accepted arbitrary-finite-row Gaussian engine, observation transport and a finite continuous linear projection give joint Gaussianity of `(Z,R restricted to I)`. No random coefficient sample is placed in ℓ².

The genuinely new covariance application uses Gram to get `Cov(Zj,Zk)=δjk` and then subtracts **all** n projection terms to get `Cov(Zj,Rm)=0`. The private cylinder proof must retain the whole vector Z when invoking finite Gaussian independence. Only after that step should the process API promote independence to the whole residual coefficient function and the measurable retraction identify the smooth sample. This is a finite application of accepted public engines, with no need to copy an old private scalar proof chain.

For posterior reconstruction, privately reconstruct ω as the full finite shift of Rω, establish raw-zero pairings of the combined finite lift, then apply the accepted shift-commutation theorem. This also works at r=0 because it is exact equality for the existing total inverse definition. The desired posterior formula is a conclusion, never a frame premise.

## Concrete control freeze is feasible

The requested controls use real original coefficients and distinguish the intended projection from plausible wrong implementations. No helper text or implementation is supplied here.

**Four original modes at L=2,r=0.** Frequencies A=(1,0), B=(2,0), C=(0,1), D=(0,2), each with canonical positive-first-nonzero half-lattice witness and Bool=false. Public `inputs/SourceFourierSeries.lean:16,19,29` fixes the actual index type and cosine convention. These modes are pairwise distinct by their frequency vectors, independently of membership proof terms. Do not substitute `sourceContactMode`'s selected sine at (2,0), or access private generated names.

Their actual amplitudes Aq are `sqrt(2*sourceWeight 2 2 kq/sourceZ 2 2)`. Positivity follows from public `sourceWeight_eq_physical` and `sourceZ_pos` (`inputs/SpectralWeights.lean:103,125`) and exponential/square-root positivity. It is not a supplied amplitude certificate. Let DAB=√(AA²+AB²), DCD=√(AC²+AD²). The first finite direction has coefficients AB/DAB, −AA/DAB at A,B; the second AD/DCD, −AC/DCD at C,D. All other coefficients are zero.

Gram follows from the two normalization identities and disjoint supports. The literal six raw columns at r=0 are `(Aq,Aq,0,0,0,0)`: both endpoints coincide at zero, and cosine first derivatives vanish there. The public raw row definitions in `SourceRawPinConditioning.lean:34` and `SourceConfluentLimits.lean:24–38` match this claim. Derive these columns and all six pairings, rather than assume a desired raw-kernel certificate.

**3/5–4/5 rotation.** The two directions ψ0=(3χ0+4χ1)/5 and ψ1=(−4χ0+3χ1)/5 genuinely involve all four original modes. Verify exact Gram, raw-zero pairings, coordinate transformation, and equality of the full projection/residual. This is a finite coefficient rotation and makes no spatial source-law rotational-invariance claim.

**Positive retained residual.** For the actual finite smooth sample with coefficient1 at mode A and zero elsewhere, the true residual's A coefficient is AA²/DAB²>0, unchanged after the frame rotation. Support-union erasure gives zero. Include this positive identity: merely checking Z(R)=0 cannot distinguish erasure, since erasure also satisfies that equation. This is not a second mutation.

**n=0.** Instantiate the main joint law and all-target posterior theorem with the empty frame. The finite lift is zero, shift/residual are identities, and the free vector is the unique empty function. Mathlib `Measure.pi_of_empty`, `MeasureTheory/Constructions/Pi.lean:340`, handles the empty product law. No special positivity assumption or substitute one-dimensional theorem should enter the main statement.

**Sole negative: omit the second projection.** Freeze ω1 as `finiteShiftSample χ1 (zeroSample 2 2)`, target0, and diagnostic mode C=the actual cosine (0,1). Exact Gram gives Zω1=(0,1). The true residual is zero; omitting only the χ1 projection leaves ω1. Raw pins of ω1 are zero, so at target0 its literal singular-radius posterior is ω1; the posterior of zero is zero, without using an inverse-covariance assertion. The coefficient q=AD/DCD is strictly positive. True reconstruction gives q and the mutant gives2q at C.

Before the sole intended-False attempt, the actual frame, smooth sample, raw columns, coordinate values, residual values and q-versus2q mismatch must each pass as positive facts. The negative assertion must be this precise mutated reconstruction equality. An import/name/type failure or an unrelated false formula does not provide the intended control. The deterministic witness has no asserted positive Gaussian mass.

## Remaining decisions and handoff

No source change is needed before root's prospective freeze. The only surface decision to settle explicitly is final spelling/argument order of Z and the bundled measurability proposition; fix the joint shift domain `(z,sample)` and residual-first law order before helpers are authorized. Freeze all concrete modes, amplitudes, rotation, retained coefficient and the sole mismatch assertion in the same contract. The root brief already supplies the required mathematical choices.

The new module will still need finite pairing/shift identities, exact map measurability, the joint finite-Gaussian application, whole-vector iid law, whole-residual transport, posterior composition and concrete controls implemented and qualified after GO. This preflight supplies none of that execution credit. It supplies no conditional-Morse, remote-jet rank, selector, Rice, density or parent closure claim.

Later qualification should cover genuinely new code/constants and controls under root's existing contract, reusing unchanged qualified Gaussian/carrier/pin/posterior evidence. Source55/56 publication/review state and different-family/process requirements must stay separate. No old verification should be replayed for freshness.

Canonical onward authority is carried without claiming that delivery means reading:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
