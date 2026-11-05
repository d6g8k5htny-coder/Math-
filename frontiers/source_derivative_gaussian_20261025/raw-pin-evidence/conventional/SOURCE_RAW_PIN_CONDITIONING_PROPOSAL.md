# Proposed sole new module: SourceRawPinConditioning.lean

Preimplementation scratch proposal for root freeze. No production file is created by this proposal. Namespace `I4SourceRawPinConditioning`. Import the qualified `SourceSmoothPalm` chain; add only narrow matrix/API imports actually needed. No baseline source edits or verification reruns. Do not register a generic Kac–Rice axiom or count definition based on the desired formula.

The sole purpose is to bind the already reviewed conventional actual raw-pin Campbell theorem to the concrete canonical whole-carrier law by a checked **every-target coefficient identity**. This module does not formalize the geometric Campbell sum or the area formula. Its final probability identity has only `hL : L ≠ 0`, fixed `b`, and a sufficiently small positive `r`; current covariance-unit premises belong in intermediate lemmas and are derived eventually.

## Literal definitions

Use the existing raw order `(fM,fS,fxM,fxS,fyM,fyS)`, endpoints `(-r/2,0),(r/2,0)` and the same `SmoothSample 2 L` carrier. Reuse `rawDerivativeCoefficient` and its first six indices rather than introduce a new Fourier realization.

```lean
-- Definition prototypes, not yet compiled production code.
rawPinCoefficient (L r : ℝ) (i : Fin 6) (m : SourceMode 2) : ℝ :=
  rawDerivativeCoefficient L r (Fin.castAdd 6 i) m

rawPinCovariance (L r : ℝ) : Matrix (Fin 6) (Fin 6) ℝ :=
  fun i j => covariance (fun ω => rawPins L r ω i)
    (fun ω => rawPins L r ω j) (smoothLaw 2 L)

rawPinLift (L r : ℝ) (y : Fin 6 → ℝ) (m : SourceMode 2) : ℝ :=
  ∑ i, rawPinCoefficient L r i m * ((rawPinCovariance L r)⁻¹ *ᵥ y) i

rawPosteriorSample (hL : L ≠ 0) (r : ℝ) (t : Fin 6 → ℝ)
    (ω : SmoothSample 2 L) : SmoothSample 2 L :=
  -- Underlying coefficient is literally:
  -- ω.val + rawPinLift L r (t - rawPins L r ω).
  -- Supply the proved goodSample finite-shift property.

rawPinKernel (hL : L ≠ 0) (r : ℝ) :
    Kernel (Fin 6 → ℝ) (SmoothSample 2 L) :=
  (Kernel.id ×ₖ Kernel.const _ (smoothLaw 2 L)).map
    (fun p => rawPosteriorSample hL r p.1 p.2)
```

The comments in the last prototypes describe construction obligations; they are not Lean holes in a claimed source. `rawPinLift`/posterior/kernel may be defined at every `r`, with mathlib's existing nonsingular-inverse convention at singular covariance. Fiber/RCD/coordinate-equivalence conclusions require `r ≠ 0` and current confluent covariance invertibility. Do not imply conditioning at `r=0` has six independent raw pins.

For the normalized prescribed measure, use an explicit name that does not promise global probability:

```lean
rawPrescribedWeightedMeasure (hL : L ≠ 0) (r b : ℝ) : Measure (SmoothSample 2 L) :=
  prwMeasure (rawPinKernel hL r ![b,b-r^3/6,0,0,0,0])
    (sourceSmoothWeight L r)
```

This is a measure at every parameter. Probability is derived for sufficiently small positive `r` from the existing positive floor. This minimal module does **not** define a globally normalized raw mark Markov kernel with a zero-normalizer branch. That additional API needs independently derived joint weight measurability and pointwise integrability before it is promised; the conventional proof already states its exact zero branch.

## Required source and algebra bridge

1. `rawPinCoefficient_summable` and `rawPins_series`: each raw coordinate is its actual summable Fourier coefficient series for every carrier sample. Obtain these by restricting the existing twelve-coordinate source series. Derive raw observation measurability, including arbitrary raw targets.
2. `rawPinCovariance_coefficient`: the literal covariance above equals `∑' m, rawPinCoefficient ... i m * rawPinCoefficient ... j m`. Reuse the actual derivative covariance theorem; do not define covariance to be a synthetic Gram without proving equality.
3. Let `T_r` be the matrix of the **existing** `confluentEquiv r hr` in the standard `Fin 6` basis. Prove both the actual coefficient-column identity `pinCoefficient L r · m = T_r *ᵥ rawPinCoefficient L r · m` and the covariance identity `sourcePinCovarianceAt L r = T_r * rawPinCovariance L r * T_r.transpose`. The matrix is not an independently chosen pin convention.
4. Derive `IsUnit(rawPinCovariance L r)` from `hr : r ≠ 0` and `hG : IsUnit(sourcePinCovarianceAt L r)`. A covariance PSD/positive-definite corollary may be useful for a later raw Gaussian-density API, but must use actual covariance facts.
5. Use `ActualGeometricPalmJoin.coefficient_lift_congr` from checked scratch `RawConfluentLift.lean` (or incorporate the exact proved lemma with attribution) to prove, for every `y,m`,

       pinLift L r (confluentTransform r y) m = rawPinLift L r y m.

   The checked generic identity requires only `IsUnit T_r` and retains the actual vector/mean; actual covariance nondegeneracy supplies the source conditioning interpretation.
6. Prove `rawPosteriorSample_eq_posteriorSample` **pointwise**, for every `t,ω`,

       rawPosteriorSample hL r t ω
         = posteriorSample hL r (confluentTransform r t) ω.

   First unfold the raw/confluent observation relation, use linearity on `t - rawPins ... ω`, and apply the same-lift identity. This is not a statement restricted to the raw-pin fiber.

## Required kernel API

Provide the literal sampling formula and Markov instance from joint posterior measurability. Then prove every-pin kernel equality:

```lean
rawPinKernel_apply ... t :
  rawPinKernel hL r t = (smoothLaw 2 L).map (rawPosteriorSample hL r t)

rawPinKernel_eq_confluent ... (hr : r ≠ 0)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (t : Fin 6 → ℝ) :
  rawPinKernel hL r t = sourceSmoothKernel hL r (confluentTransform r t)
```

Also expose equality with the **kernel comap** along the measurable equivalence `confluentEquiv r hr`, so downstream transport does not rewrite pointwise indefinitely.

The existing mathlib API is sufficient to transfer the RCD statement; no new residual-independence proof is needed. Apply `HasCondDistrib.measurableEquiv_comp_right` from `Mathlib.Probability.HasCondDistrib` to the proved `sourceSmoothKernel_hasCondDistrib`, with the inverse raw/confluent measurable equivalence. Its resulting observation is literally `rawPins`; its resulting kernel is the confluent kernel comapped by `T_r`. Rewrite with the proved kernel equality. Export

```lean
rawPinKernel_hasCondDistrib (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (hG : IsUnit (sourcePinCovarianceAt L r)) :
  HasCondDistrib (id : SmoothSample 2 L → SmoothSample 2 L)
    (rawPins L r) (rawPinKernel hL r) (smoothLaw 2 L)
```

Optionally derive raw pin support from pointwise posterior reconstruction and expose the measurable-functional pushforward through existing `HasCondDistrib.comp_left`. These are useful direct corollaries; they do not replace the all-target coefficient identity. Derive `rawPinCovariance_eventually_isUnit` and `rawPinKernel_eventually_hasCondDistrib` using the already proved `(sourceEndpoint_parameter_limits hL 0).1` plus eventual positive radius, with no height input or new limit hypotheses.

## Required prescribed normalized-weight identity

The already proved `prescribed_target` transforms the literal raw target to `sourcePrescribedPins r b`. Use it with every-target kernel equality to obtain

```lean
rawPinKernel_prescribed ... hr hG :
  rawPinKernel hL r ![b,b-r^3/6,0,0,0,0] = sourceSmoothLaw hL r b

rawPrescribedWeightedMeasure_eq ... hr hG :
  rawPrescribedWeightedMeasure hL r b = sourceSmoothWeightedLaw hL r b
```

The physical weight is **the existing literal** `sourceSmoothWeight`, not an endpoint substitute. The measure equality follows by rewriting the base measure inside the existing `prwMeasure` definition; no scalar Gaussian density or radius Jacobian belongs in it. It is valid wherever the kernel equality is valid, without a separate positivity assumption. Derive its eventual probability/event/endpoint/support consequences by rewriting the existing `sourceSmoothPalm_estimates hL b` result. Do not reprove its moment or normalizer estimates.

## Verification and retained boundary

Only this new source/application should receive new compile, named kernel, exported-target axiom and meaningful positive/negative checks, once root freezes the contract and authorizes production. Reuse all unchanged source/kernel/normalizer evidence. Controls should cover arbitrary nonzero target/mean, a nontrivial invertible row transformation, and failure of dropping a transform factor; a null-fiber-only identity is not an adequate control.

The new module would mechanically identify the canonical raw version used by the reused analytic Campbell theorem with our formal full-carrier weighted law. It would **not** be a Lean proof of Kac–Rice, a formal geometric point-process sum, a global mark-kernel normalization theorem, conditional Morse at every pin, capture/elder selection or original-goal closure. Different-family review remains a separate process requirement, not a new mathematical gap in the already accepted conventional Rice theorem.
