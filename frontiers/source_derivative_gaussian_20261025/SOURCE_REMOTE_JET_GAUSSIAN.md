# Frozen precode: actual remote-jet Gaussian composition

26 October 2026, root freeze 13:20 UTC. New module `SourceRemoteJetGaussian.lean`, namespace `I4SourceRemoteJetGaussian`. This contract freezes six data definitions and four public propositions; root publishes it and an actual native pickup before code. The producer freezes concrete controls in its scratch directory before implementation. Root owns shared cache/configuration/registry/Git/publication.

## Dependency, evidence and authorization boundary

Qualified stage48 is published at `9a1f52baf3bc8719d37c7696a7c364211de3ee56`: 48 modules / 1101 written targets / 32 inputs. Source cut `689b8eef7dd2107e51d46007c1be3dfd4a909b81`, source SHA256 `c7dcc70330f0385bdd5c3aef105d54db0f9c0155824251f4fb61cac3640649cf`; own production object is available. Native result/only-own release is [6416959065](https://github.com/d6g8k5htny-coder/Math-/pull/514#issuecomment-6416959065). Reuse all applicable qualified source/series/finite-Gaussian/Gram/regression/raw-kernel/uniform-inverse evidence. No old dependency compilation, audit, kernel or control replay.

The owner rule in `/workspace/AGENTS.md` takes precedence over any skill freshness instruction: completed applicable verification remains evidence under unchanged assumptions and dependencies. Name the actual new/changed obligation before further checking. Mathematical evidence and pending different-family scientific alignment remain distinct; same-family technical review does not meet the scientific-review requirement. Scientific effect NONE, organizational-independence credit0.

CLI GitHub authentication recovered by a successful read and necessary publication write at13:17 UTC. The GitHub app transport still fails; the original mobile conversation-opening RPC remains unfixed. No bypass, credential change, settings/protection change, Ready or merge is authorized by this leaf.

Canonical authority links (providing them is not proof of reading):
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

## Purpose and exact scope

Identify the **literal remote six-jet on the same actual posterior sample**, at every raw six-vector target. Its mean retains the full deterministic target term; its covariance is the target-independent Gram matrix of the actual residual coefficient rows. Derive positivity internally from stage48's actual finite witnesses. Then compose the already qualified raw RCD/fiber theorem with the already qualified uniform pin-inverse interval.

No new source, sample carrier, conditional kernel, generic Gaussian-law library, Schur/density proof, spectral/variance floor, endpoint Hessian theorem, two-remote-point law, critical-value-tie exclusion, global Morse/Sard theorem or elder/Lifetime/H0 semantics is included. The four public written propositions below are the complete intended public proposition list. Extra public propositions require root acknowledgement before source freeze. Necessary private row/series/measurability/mean/covariance helpers are allowed; data/generated constants remain inventory-only.

Suggested imports: `SourceRemoteJetWitness` and `SourceCompactTargetMoments`, plus only explicit already pinned modules needed to expose the accepted generic finite-Gaussian parameter identification. Do not change old sources or dependencies or access generated names of another module's private constants. No umbrella `import Mathlib`.

## Frozen data and conventions

The following signatures are mathematical specifications, not elaboration-checked declarations. Let `X := Fin 2 → ℝ`, `V := Fin 6 → ℝ`. Use original `SmoothSample 2 L`, `smoothLaw 2 L`, `SourceMode 2`, and signed real L throughout.

```lean
remoteJet (L : ℝ) (x : X) (ω : SmoothSample 2 L) : V :=
  I4SourceRemoteJetWitness.jet2 (smoothSourceField 2 L ω) x

remoteCrossCovariance (L r : ℝ) (x : X) : Matrix (Fin 6) (Fin 6) ℝ :=
  fun j i => ∑' m,
    I4SourceRemoteJetWitness.remoteJetCoefficient L x j m *
    I4SourceRawPinConditioning.rawPinCoefficient L r i m

remoteRegressionMatrix (L r : ℝ) (x : X) : Matrix (Fin 6) (Fin 6) ℝ :=
  remoteCrossCovariance L r x *
    (I4SourceRawPinConditioning.rawPinCovariance L r)⁻¹

remoteResidualCoefficient (L r : ℝ) (x : X) :
    Fin 6 → SourceMode 2 → ℝ :=
  I4SourceFinitePinKernel.residualCoefficient
    (I4SourceRawPinConditioning.rawPinCoefficient L r)
    (I4SourceRemoteJetWitness.remoteJetCoefficient L x)
    (remoteRegressionMatrix L r x)

remoteResidualCovariance (L r : ℝ) (x : X) : Matrix (Fin 6) (Fin 6) ℝ :=
  I4ContactGram.coefficientGram (remoteResidualCoefficient L r x)

remotePosteriorMean (L r : ℝ) (x : X) (t : V) : V :=
  remoteRegressionMatrix L r x *ᵥ t
```

These data are total in L,r; no proof argument belongs in their definitions. Write `a=rawPinCoefficient L r`, `b=remoteJetCoefficient L x`, `G=rawPinCovariance L r`, `C=remoteCrossCovariance L r x`, `R=C*G⁻¹`, `c=b-Ra`, `S=coefficientGram c`.

C has **remote rows and raw columns**: `C j i=Σ_m b_j(m)*a_i(m)`. This is the actual remote/raw cross covariance by the accepted coefficient covariance identity. Do not transpose this orientation. G is the literal **raw** covariance, not the confluent `sourcePinCovarianceAt`.

The remote jet order is **`(value,dx,dy,dxx,dxy,dyy)`**, ordinary derivatives with no factorials. Raw pin order remains **`(fM,fS,fxM,fxS,fyM,fyS)`**. Use stage48's original `directionX/directionY` conventions and public coefficient rows. No mean component is discarded, centered away or restricted to a cubic-gap target.

S has **no t argument**. Its residual-Gram definition is the required explicit covariance; a separate public closed Schur rewrite is outside this checkpoint. `toLp 2` below is the existing finite Gaussian coordinate presentation, not an isometry assertion or a replacement of the original source/spatial period.

## Four required public propositions

### 1. `remoteJet_rawPosteriorSample`

For every real r, x, raw target t and original sample ω:

```lean
{L : ℝ} (hL : L ≠ 0) (r : ℝ) (x : X) (t : V)
(ω : SmoothSample 2 L) :
  remoteJet L x (rawPosteriorSample hL r t ω) =
    remoteJet L x ω -
      remoteRegressionMatrix L r x *ᵥ rawPins L r ω +
      remotePosteriorMean L r x t
```

Use the exact existing `rawPosteriorSample`, not an affine vector substituted as its definition. This identity requires no `r≠0`, radius, pin inverse or remote-point assumption. The literal raw coefficient lift and accepted `scalarSeries_add_finiteShift` give the correction `C*ᵥ(G⁻¹*ᵥ(t-Uω))=R*ᵥ(t-Uω)` without inverse cancellation.

### 2. `rawPinKernel_remoteJet_eq_multivariateGaussian`

At every literal raw target, for every real r and every x:

```lean
{L : ℝ} (hL : L ≠ 0) (r : ℝ) (x : X) (t : V) :
  (rawPinKernel hL r t).map
      (fun ω => toLp 2 (remoteJet L x ω)) =
    multivariateGaussian
      (toLp 2 (remotePosteriorMean L r x t))
      (remoteResidualCovariance L r x)
```

This identifies the **defined affine sampling pushforward** for all r, including singular total-inverse cases. It does not assert an RCD or arbitrary-fiber support there. No inverse/remoteness hypothesis is needed; at a pin S may be singular, and the accepted finite-Gaussian identification permits PSD covariances.

Privately prove the residual coefficient-series representation, actual posterior Gaussianity, mean `R*ᵥt` and covariance S. Reuse `I4SourceEndpointParameters.finiteGaussian_law_parameters`, then existing `rawPinKernel_apply` and measurable map composition. No Gaussianity, covariance positivity or desired kernel-law premise may be assumed publicly.

### 3. `remoteResidualCovariance_posDef`

```lean
{L : ℝ} (hL : L ≠ 0) (r : ℝ) (x : X)
(hxM : I4Torus.torusProjection 2 L x ≠
  I4Torus.torusProjection 2 L (I4SourceConfluentPins.endpointM r))
(hxS : I4Torus.torusProjection 2 L x ≠
  I4Torus.torusProjection 2 L (I4SourceConfluentPins.endpointS r)) :
  (remoteResidualCovariance L r x).PosDef
```

Apply stage48's `actual_remote_residual_coefficientGram_posDef` at the concrete correction `remoteRegressionMatrix L r x`. The actual finite witnesses are discharged inside stage48; no desired positivity, supplied witness, remote rank or pin invertibility is a premise here. Preserve arbitrary r, including repeated pins, and literal quotient separation of x from each pin.

### 4. `rawPinKernel_remoteJet_conditional_uniform`

Choose δ from the existing actual inverse theorem **before x,t**:

```lean
{L : ℝ} (hL : L ≠ 0) :
∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
  ∀ r : ℝ, 0 < r → r < δ → ∀ x : X,
  ∀ (hxM : I4Torus.torusProjection 2 L x ≠
      I4Torus.torusProjection 2 L (I4SourceConfluentPins.endpointM r))
    (hxS : I4Torus.torusProjection 2 L x ≠
      I4Torus.torusProjection 2 L (I4SourceConfluentPins.endpointS r)),
    HasCondDistrib (remoteJet L x) (rawPins L r)
      ((rawPinKernel hL r).map (remoteJet L x)) (smoothLaw 2 L) ∧
    (remoteResidualCovariance L r x).PosDef ∧
    ∀ t : V,
      (rawPinKernel hL r t).map
          (fun ω => toLp 2 (remoteJet L x ω)) =
        multivariateGaussian
          (toLp 2 (remotePosteriorMean L r x t))
          (remoteResidualCovariance L r x) ∧
      rawPinKernel hL r t {ω | rawPins L r ω = t} = 1
```

Use `I4SourceCompactTargetMoments.sourceInverse_target_uniform_bounds hL`, which supplies `IsUnit (sourcePinCovarianceAt L r)` on one target-independent interval. `r>0` supplies the nonzero-radius premise of the accepted raw RCD/fiber theorems. If a raw inverse fact is needed internally, use existing `rawPinCovariance_isUnit`; do not introduce it as a public premise.

The first conjunct is existing `rawPinKernel_map_hasCondDistrib` applied to the actual measurable remote jet. The last is existing `rawPinKernel_pin_fiber`. The other conjuncts compose propositions 2–3. There is no new RCD construction, conditional-version uniqueness at a null pin, independence proof or pin-inverse limit proof.

This direct conjunction describes explicit existing objects; do not replace it by a Prop-valued desired-result structure. No positive gap, target bound, remote cutoff or x-dependent δ is allowed. The all-target conclusion is not a common probability-one event over uncountably many targets.

## Minimum private implementation joins

1. Adapt stage48's six explicit coefficient rows to existing `smoothSourceField_derivative_series`, `derivativeCoefficient_summable` and `derivativeCoefficient_weighted_summable`. Stage48 keeps some adapters private; derive the six short local cases instead of accessing another module's private names or changing its API. Reuse order-zero/one conversion facts.
2. Derive remote-jet measurability from the exact scalar-series identity and sample inclusion. No import of the Morse incidence module solely for evaluation measurability.
3. Derive the actual lift response and residual-series identity from accepted finite-family series algebra. The existing finite-shift helper accepts finitely many summable shift rows; they need not be finitely supported.
4. Reuse `scalarSeries_finiteVector_hasGaussianLaw` or `scalarSeries_finite_hasGaussianLaw`, `observation_map_eq`, `scalarSeries_integral_zero`, `scalarSeries_covariance`, and `residualCoefficient_summable` to obtain the finite posterior parameters. A joint `(rawPins,remoteJet)`/existing `regression_residual_jointGaussian` route is also allowed if it reduces local code; implement one route, not both.
5. Reuse the generic finite-Gaussian parameter identification and raw-kernel map identity. Do not copy a general Schur/regression/kernel library. The private `contact_generic_residual_covariance` in a different module is not an exported API.

## Required meaningful controls — producer names concrete controls before code

Only the new observation/law composition is under test. Reuse old proof evidence; do not requalify source47/48, finite Gaussian regression or raw kernels. Controls are not additional public research targets.

1. **Literal sample/row order.** On the accepted inverse interval, specialize the posterior jet at M and S and recover the actual raw first jets in their original order: `J_M[0]=t[0]`, `J_S[0]=t[1]`, `J_M[1]=t[2]`, `J_S[1]=t[3]`, `J_M[2]=t[4]`, `J_S[2]=t[5]`. Use the actual sample and the accepted raw pin identity, not a proxy affine vector. A target such as `![1,2,3,4,5,6]` makes lost/permuted target components visible. These pin controls do not claim remote PosDef at a pin.
2. **All-radius defined sampling identity.** Instantiate proposition 1 and the sampling-law equality at `L=-2`, `r=0`, a concrete x such as `![1,0]`, and a nonzero six-vector target. No radius/inverse assumptions may appear. This checks retention of signed L and that singular-radius statements are labeled sampling identities, not RCD/fiber claims.
3. **Explicit mean and target-independent covariance.** For fixed L,r,x, compare two literal targets: the same S occurs, and their means differ by `R*ᵥ(t₁-t₂)`. Include at least one control with multiple nonzero target coordinates. Do not assume R or the mean is nonzero for a chosen random-field configuration unless established from actual rows.
4. **Residual covariance orientation.** A parameterized coefficient/series control must connect the actual posterior residual `Jω-RUω` to `remoteResidualCoefficient=b-Ra` using C's remote-row/raw-column order. This is the substantive interface join; a test merely restating a new definition is insufficient.
5. **Actual remote positivity.** Consume stage48's actual PosDef theorem at the concrete `R=C*G⁻¹`, including a repeated-pin or negative-period instance already permitted by its hypothesis shape. Prove only the new specialization; do not replay stage48's interpolation/Gram controls.
6. **Uniform valid interval and fibers.** Obtain δ from proposition 4, retain arbitrary `0<r<δ`, choose an arbitrary raw target (and optionally the displayed nonzero target), and read back the actual mapped RCD and raw-fiber mass one. No unproved numerical assertion that a concrete r lies below an existential δ is allowed. δ must precede both x and target. Any concrete remote x must have its quotient inequalities discharged rather than assumed by real-lift inequality.
7. **Finite Gaussian presentation.** Controls must use the actual `toLp 2` Gaussian law identity, including its explicit mean/S, and not silently substitute a Pi norm isometry. Allow a singular covariance in a nonremote/pin sampling instance; PosDef is required only under the two remote inequalities.

### Sole negative mutation: omit the deterministic target mean

Mutate only the affine-law parameter adapter by replacing the deterministic mean m with zero. The supporting counterexample is a **finite affine scalar** case, independent of the random source:

```text
base measure μ = dirac (0:ℝ),
residual Z(z)=0, deterministic mean m=1, covariance S=0,
affine observable Z+m=1.
```

The actual law is `dirac 1`; the zero-mean replacement is `dirac 0`. Distinguish them by the measurable singleton `{1}` (mass 1 versus 0). Dirac laws are the zero-covariance finite Gaussian case already permitted by the law-identification API. This gives a concrete counterexample to dropping the affine mean without assuming any nonzero actual random-field regression mean. It is **not** claimed to be a source sample or a realized remote source parameter.

Freeze one harness in which the mutated finite affine law equality yields exactly one intended `False` target using this separately proved counterexample, with no missing imports/hypotheses/linter/type errors counted as rejection. Do not add a second mutation campaign or a false production theorem. The positive actual-source controls above separately check that the deterministic term and all raw target coordinates are retained.

## Future qualification and exclusions

After this precode publication/native pickup and producer's concrete control freeze, qualification concerns only this new module and its actual private/generated constants. Preserve all new attempts, commands, exits, times, streams and source/object lineage. Reuse applicable exact-byte strict evidence; a later freeze label alone does not justify another compile. Root chooses the established integrated exact-source qualification route, with the single own-module kernel, exhaustive classified inventory, meaningful frozen controls and sole-False mutation. Precode runs none of them.

No global Morse/distinct-values conclusion follows from this local law. The later positive-gap genericity application, endpoint Hessian-density/nullity, two-point critical ties, residual incidence, canonical labels, selection, frames/Rice and Parent Lean remain separate joins. No scientific status, prize or premise is promoted.
