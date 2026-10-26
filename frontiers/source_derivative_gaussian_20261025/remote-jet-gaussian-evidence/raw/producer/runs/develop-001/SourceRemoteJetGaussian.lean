import SourceRemoteJetWitness
import SourceCompactTargetMoments

/-! The literal remote six-jet on the actual raw posterior sample. All-radius
sampling identities retain the deterministic target mean. The conditional-law
and raw-fiber assertions use one existing target-independent inverse interval. -/

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix Topology
open I4Foundation I4Source I4Weights I4Smooth I4SmoothCarrier
open I4SourceGaussian I4SourceCovariance I4SourceDerivativeGaussian
open I4SourceConfluentPins I4SourceConfluentLimits I4SourceEndpointRegression
open I4SourceSmoothConditional I4SourceRawPinConditioning
open I4SourceRemoteJetWitness MeasureTheory ProbabilityTheory

namespace I4SourceRemoteJetGaussian

/-- Ordinary jet order: value,dx,dy,dxx,dxy,dyy. -/
def remoteJet (L : ℝ) (x : Fin 2 → ℝ) (ω : SmoothSample 2 L) : Fin 6 → ℝ :=
  jet2 (smoothSourceField 2 L ω) x

/-- Remote rows and literal raw-pin columns. -/
def remoteCrossCovariance (L r : ℝ) (x : Fin 2 → ℝ) : Matrix (Fin 6) (Fin 6) ℝ :=
  fun j i => ∑' m, remoteJetCoefficient L x j m * rawPinCoefficient L r i m

/-- The total raw-covariance regression matrix, including singular radii. -/
def remoteRegressionMatrix (L r : ℝ) (x : Fin 2 → ℝ) : Matrix (Fin 6) (Fin 6) ℝ :=
  remoteCrossCovariance L r x * (rawPinCovariance L r)⁻¹

/-- Actual residual rows b-Ra on the unchanged original coefficient index. -/
def remoteResidualCoefficient (L r : ℝ) (x : Fin 2 → ℝ) :
    Fin 6 → SourceMode 2 → ℝ :=
  I4SourceFinitePinKernel.residualCoefficient (rawPinCoefficient L r)
    (remoteJetCoefficient L x) (remoteRegressionMatrix L r x)

/-- Target-independent covariance, explicitly the residual coefficient Gram. -/
def remoteResidualCovariance (L r : ℝ) (x : Fin 2 → ℝ) : Matrix (Fin 6) (Fin 6) ℝ :=
  I4ContactGram.coefficientGram (remoteResidualCoefficient L r x)

/-- The full deterministic mean at a literal six-vector raw target. -/
def remotePosteriorMean (L r : ℝ) (x : Fin 2 → ℝ) (t : Fin 6 → ℝ) : Fin 6 → ℝ :=
  remoteRegressionMatrix L r x *ᵥ t

-- Six-row adapters integrated once from frozen text-only helper.
/- Required context: inside namespace I4SourceRemoteJetGaussian, after remoteJet;
   open I4Source I4SmoothCarrier I4SourceGaussian I4SourceDerivativeGaussian
     I4SourceConfluentPins. This is text for one integration, not a helper module. -/

private theorem remoteJet_series {L : ℝ} (hL : L ≠ 0)
    (x : Fin 2 → ℝ) (ω : SmoothSample 2 L) :
    remoteJet L x ω = fun j =>
      scalarSeries (I4SourceRemoteJetWitness.remoteJetCoefficient L x j)
        (sampleInclusion 2 L ω) := by
  funext j
  fin_cases j
  · change smoothSourceField 2 L ω x =
      scalarSeries (fun m => modeCoefficient 2 L m x) (sampleInclusion 2 L ω)
    simpa only [derivativeCoefficient, iteratedFDeriv_zero_apply] using
      (smoothSourceField_derivative_series 2 hL ω 0 x (fun i => Fin.elim0 i))
  · change fderiv ℝ (smoothSourceField 2 L ω) x directionX =
      scalarSeries (derivativeCoefficient 2 L 1 x (fun _ => directionX))
        (sampleInclusion 2 L ω)
    simpa only [iteratedFDeriv_one_apply] using
      (smoothSourceField_derivative_series 2 hL ω 1 x (fun _ => directionX))
  · change fderiv ℝ (smoothSourceField 2 L ω) x directionY =
      scalarSeries (derivativeCoefficient 2 L 1 x (fun _ => directionY))
        (sampleInclusion 2 L ω)
    simpa only [iteratedFDeriv_one_apply] using
      (smoothSourceField_derivative_series 2 hL ω 1 x (fun _ => directionY))
  · exact smoothSourceField_derivative_series 2 hL ω 2 x ![directionX,directionX]
  · exact smoothSourceField_derivative_series 2 hL ω 2 x ![directionX,directionY]
  · exact smoothSourceField_derivative_series 2 hL ω 2 x ![directionY,directionY]

private theorem remoteJetCoefficient_summable_local {L : ℝ} (hL : L ≠ 0)
    (x : Fin 2 → ℝ) (j : Fin 6) :
    Summable (I4SourceRemoteJetWitness.remoteJetCoefficient L x j) := by
  fin_cases j
  · change Summable (fun m => modeCoefficient 2 L m x)
    have he : derivativeCoefficient 2 L 0 x (fun i => Fin.elim0 i) =
        fun m => modeCoefficient 2 L m x := by
      funext m
      exact iteratedFDeriv_zero_apply _
    rw [← he]
    exact derivativeCoefficient_summable 2 hL 0 x (fun i => Fin.elim0 i)
  · exact derivativeCoefficient_summable 2 hL 1 x (fun _ => directionX)
  · exact derivativeCoefficient_summable 2 hL 1 x (fun _ => directionY)
  · exact derivativeCoefficient_summable 2 hL 2 x ![directionX,directionX]
  · exact derivativeCoefficient_summable 2 hL 2 x ![directionX,directionY]
  · exact derivativeCoefficient_summable 2 hL 2 x ![directionY,directionY]

private theorem remoteJetCoefficient_weighted_summable_local {L : ℝ} (hL : L ≠ 0)
    (x : Fin 2 → ℝ) (ω : SmoothSample 2 L) (j : Fin 6) :
    Summable (fun m => I4SourceRemoteJetWitness.remoteJetCoefficient L x j m *
      sampleInclusion 2 L ω m) := by
  fin_cases j
  · change Summable (fun m => modeCoefficient 2 L m x * sampleInclusion 2 L ω m)
    simpa only [derivativeCoefficient, iteratedFDeriv_zero_apply] using
      (I4SourceSmoothConditional.derivativeCoefficient_weighted_summable hL ω 0 x
        (fun i => Fin.elim0 i))
  · exact I4SourceSmoothConditional.derivativeCoefficient_weighted_summable hL ω 1 x
      (fun _ => directionX)
  · exact I4SourceSmoothConditional.derivativeCoefficient_weighted_summable hL ω 1 x
      (fun _ => directionY)
  · exact I4SourceSmoothConditional.derivativeCoefficient_weighted_summable hL ω 2 x
      ![directionX,directionX]
  · exact I4SourceSmoothConditional.derivativeCoefficient_weighted_summable hL ω 2 x
      ![directionX,directionY]
  · exact I4SourceSmoothConditional.derivativeCoefficient_weighted_summable hL ω 2 x
      ![directionY,directionY]


private theorem remoteJet_measurable {L : ℝ} (hL : L ≠ 0) (x : Fin 2 → ℝ) :
    Measurable (remoteJet L x) := by
  have heq : remoteJet L x = fun ω j =>
      scalarSeries (remoteJetCoefficient L x j) (sampleInclusion 2 L ω) :=
    funext (remoteJet_series hL x)
  rw [heq]
  exact Measurable.of_eval (fun j =>
    (scalarSeries_measurable _).comp (sampleInclusion_measurable 2 L))

/-- Literal posterior response, requiring neither a radius nor an inverse premise. -/
theorem remoteJet_rawPosteriorSample {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x : Fin 2 → ℝ) (t : Fin 6 → ℝ) (ω : SmoothSample 2 L) :
    remoteJet L x (rawPosteriorSample hL r t ω) = remoteJet L x ω -
      remoteRegressionMatrix L r x *ᵥ rawPins L r ω + remotePosteriorMean L r x t := by
  have hresp : remoteJet L x (rawPosteriorSample hL r t ω) =
      remoteJet L x ω + remoteRegressionMatrix L r x *ᵥ (t - rawPins L r ω) := by
    ext j
    rw [remoteJet_series hL x, remoteJet_series hL x]
    change scalarSeries (remoteJetCoefficient L x j)
      (fun m => ω.val m + ∑ i, rawPinCoefficient L r i m *
        (((rawPinCovariance L r)⁻¹ *ᵥ (t - rawPins L r ω)) i)) = _
    rw [scalarSeries_add_finiteShift _ _ _ _
      (remoteJetCoefficient_summable_local hL x j) (rawPinCoefficient_summable hL r)
      (remoteJetCoefficient_weighted_summable_local hL x ω j)]
    change _ + (remoteCrossCovariance L r x *ᵥ
      ((rawPinCovariance L r)⁻¹ *ᵥ (t - rawPins L r ω))) j = _
    rw [Matrix.mulVec_mulVec]
    rfl
  rw [hresp, Matrix.mulVec_sub, remotePosteriorMean]
  abel

private theorem rawPinCoefficient_weighted_summable_local {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (ω : SmoothSample 2 L) (i : Fin 6) :
    Summable (fun m => rawPinCoefficient L r i m * sampleInclusion 2 L ω m) :=
  derivativeCoefficient_weighted_summable hL ω
    (rawDerivativeOrder (Fin.castAdd 6 i)) (rawDerivativePoint r (Fin.castAdd 6 i))
    (rawDerivativeDirections (Fin.castAdd 6 i))

private theorem remoteResidual_series {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x : Fin 2 → ℝ) (ω : SmoothSample 2 L) :
    remoteJet L x ω - remoteRegressionMatrix L r x *ᵥ rawPins L r ω =
      fun j => scalarSeries (remoteResidualCoefficient L r x j) (sampleInclusion 2 L ω) := by
  ext j
  rw [remoteJet_series hL x, rawPins_series hL r]
  have hs := hasSum_sum (fun i (_ : i ∈ Finset.univ) =>
    ((rawPinCoefficient_weighted_summable_local hL r ω i).hasSum).mul_left
      (remoteRegressionMatrix L r x j i))
  have ht := (remoteJetCoefficient_weighted_summable_local hL x ω j).hasSum.sub hs
  symm
  convert ht.tsum_eq using 1
  apply tsum_congr
  intro m
  simp only [remoteResidualCoefficient, I4SourceFinitePinKernel.residualCoefficient,
    sub_mul, Finset.sum_mul]
  congr 1
  apply Finset.sum_congr rfl
  intro i _
  ring

private theorem remoteResidual_summable {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x : Fin 2 → ℝ) (j : Fin 6) : Summable (remoteResidualCoefficient L r x j) :=
  I4SourceFinitePinKernel.residualCoefficient_summable _ _ _
    (rawPinCoefficient_summable hL r) (remoteJetCoefficient_summable_local hL x) j

private def remoteResidual (L r : ℝ) (x : Fin 2 → ℝ)
    (ω : SmoothSample 2 L) : Fin 6 → ℝ :=
  fun j => scalarSeries (remoteResidualCoefficient L r x j) (sampleInclusion 2 L ω)

private theorem remoteResidual_hasGaussianLaw {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (x : Fin 2 → ℝ) : HasGaussianLaw (remoteResidual L r x) (smoothLaw 2 L) := by
  have hm : Measurable (fun η j => scalarSeries (remoteResidualCoefficient L r x j) η) :=
    Measurable.of_eval (fun j => scalarSeries_measurable _)
  refine ⟨(hm.comp (sampleInclusion_measurable 2 L)).aemeasurable, ?_⟩
  rw [show remoteResidual L r x = (fun ω j =>
    scalarSeries (remoteResidualCoefficient L r x j) (sampleInclusion 2 L ω)) from rfl,
    observation_map_eq 2 hL _ hm]
  exact (scalarSeries_finiteVector_hasGaussianLaw 6 _ (remoteResidual_summable hL r x)).isGaussian_map

private theorem remoteResidual_integral_zero {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (x : Fin 2 → ℝ) : (∫ ω, remoteResidual L r x ω ∂smoothLaw 2 L) = 0 := by
  ext j
  have hh := (ContinuousLinearMap.proj j : (Fin 6 → ℝ) →L[ℝ] ℝ).integral_comp_comm
    (remoteResidual_hasGaussianLaw hL r x).integrable
  change (∫ ω, remoteResidual L r x ω j ∂smoothLaw 2 L) =
    (∫ ω, remoteResidual L r x ω ∂smoothLaw 2 L) j at hh
  rw [← hh]
  change (∫ ω, scalarSeries (remoteResidualCoefficient L r x j)
    (sampleInclusion 2 L ω) ∂smoothLaw 2 L) = 0
  rw [← integral_map (sampleInclusion_measurable 2 L).aemeasurable
    (scalarSeries_measurable _).aestronglyMeasurable, sampleInclusion_map 2 hL]
  exact scalarSeries_integral_zero _ (remoteResidual_summable hL r x j)

private theorem remoteResidual_covariance {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (x : Fin 2 → ℝ) (i j : Fin 6) :
    covariance (fun ω => remoteResidual L r x ω i)
      (fun ω => remoteResidual L r x ω j) (smoothLaw 2 L) =
      remoteResidualCovariance L r x i j := by
  unfold remoteResidual
  rw [covariance_comp_inclusion 2 hL _ _ (scalarSeries_measurable _) (scalarSeries_measurable _)]
  exact I4SourceCovariance.scalarSeries_covariance _ _
    (remoteResidual_summable hL r x i) (remoteResidual_summable hL r x j)

private theorem remotePosterior_eq_residual_add_mean {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (x : Fin 2 → ℝ) (t : Fin 6 → ℝ) (ω : SmoothSample 2 L) :
    remoteJet L x (rawPosteriorSample hL r t ω) =
      remoteResidual L r x ω + remotePosteriorMean L r x t := by
  rw [remoteJet_rawPosteriorSample hL, remoteResidual_series hL]
  rfl

private theorem remotePosterior_hasGaussianLaw {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (x : Fin 2 → ℝ) (t : Fin 6 → ℝ) :
    HasGaussianLaw (fun ω => remoteJet L x (rawPosteriorSample hL r t ω)) (smoothLaw 2 L) := by
  have hR := remoteResidual_hasGaussianLaw hL r x
  have hg : HasGaussianLaw (fun ω => remoteResidual L r x ω + remotePosteriorMean L r x t)
      (smoothLaw 2 L) := by
    refine ⟨hR.aemeasurable.add aemeasurable_const, ?_⟩
    have : IsGaussian ((smoothLaw 2 L).map (remoteResidual L r x)) := hR.isGaussian_map
    convert (inferInstance : IsGaussian (((smoothLaw 2 L).map (remoteResidual L r x)).map
      (fun v => v + remotePosteriorMean L r x t))) using 1
    rw [AEMeasurable.map_map_of_aemeasurable (by fun_prop) hR.aemeasurable]
    rfl
  exact hg.congr (Filter.Eventually.of_forall (fun ω =>
    (remotePosterior_eq_residual_add_mean hL r x t ω).symm))

private theorem remotePosterior_integral {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (x : Fin 2 → ℝ) (t : Fin 6 → ℝ) :
    (∫ ω, remoteJet L x (rawPosteriorSample hL r t ω) ∂smoothLaw 2 L) =
      remotePosteriorMean L r x t := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  simp_rw [remotePosterior_eq_residual_add_mean hL]
  rw [integral_add (remoteResidual_hasGaussianLaw hL r x).integrable (integrable_const _),
    remoteResidual_integral_zero hL, integral_const, zero_add]
  simp

private theorem remotePosterior_covariance {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (x : Fin 2 → ℝ) (t : Fin 6 → ℝ) (i j : Fin 6) :
    covariance (fun ω => remoteJet L x (rawPosteriorSample hL r t ω) i)
      (fun ω => remoteJet L x (rawPosteriorSample hL r t ω) j) (smoothLaw 2 L) =
      remoteResidualCovariance L r x i j := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  simp_rw [remotePosterior_eq_residual_add_mean hL]
  have hR := remoteResidual_hasGaussianLaw hL r x
  change covariance (fun ω => remoteResidual L r x ω i + remotePosteriorMean L r x t i)
    (fun ω => remoteResidual L r x ω j + remotePosteriorMean L r x t j) _ = _
  rw [covariance_add_const_left (hR.eval i).integrable,
    covariance_add_const_right (hR.eval j).integrable]
  exact remoteResidual_covariance hL r x i j

/-- Defined sampling law at every radius and literal raw target; S may be singular. -/
theorem rawPinKernel_remoteJet_eq_multivariateGaussian {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (x : Fin 2 → ℝ) (t : Fin 6 → ℝ) :
    (rawPinKernel hL r t).map (fun ω => toLp 2 (remoteJet L x ω)) =
      multivariateGaussian (toLp 2 (remotePosteriorMean L r x t))
        (remoteResidualCovariance L r x) := by
  have hp : Measurable (rawPosteriorSample hL r t) :=
    (rawPosteriorSample_measurable hL r).comp (measurable_const.prodMk measurable_id)
  have hj : Measurable (fun ω => toLp 2 (remoteJet L x ω)) :=
    (by fun_prop : Measurable (fun v : Fin 6 → ℝ => toLp 2 v)).comp (remoteJet_measurable hL x)
  rw [rawPinKernel_apply, Measure.map_map hj hp]
  exact (I4SourceEndpointParameters.finiteGaussian_law_parameters
    (remotePosterior_hasGaussianLaw hL r x t) _ (remotePosterior_integral hL r x t)
    _ (remotePosterior_covariance hL r x t)).2

/-- Actual finite original-mode witnesses force remote residual positivity. -/
theorem remoteResidualCovariance_posDef {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x : Fin 2 → ℝ)
    (hxM : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointM r))
    (hxS : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointS r)) :
    (remoteResidualCovariance L r x).PosDef :=
  actual_remote_residual_coefficientGram_posDef hL r x hxM hxS (remoteRegressionMatrix L r x)

/-- One inverse interval precedes remote points and targets. -/
theorem rawPinKernel_remoteJet_conditional_uniform {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ → ∀ x : Fin 2 → ℝ,
      ∀ (hxM : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointM r))
        (hxS : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointS r)),
      HasCondDistrib (remoteJet L x) (rawPins L r)
        ((rawPinKernel hL r).map (remoteJet L x)) (smoothLaw 2 L) ∧
      (remoteResidualCovariance L r x).PosDef ∧
      ∀ t : Fin 6 → ℝ,
        (rawPinKernel hL r t).map (fun ω => toLp 2 (remoteJet L x ω)) =
          multivariateGaussian (toLp 2 (remotePosteriorMean L r x t))
            (remoteResidualCovariance L r x) ∧
        rawPinKernel hL r t {ω | rawPins L r ω = t} = 1 := by
  obtain ⟨K, δ, _hK, hδ, hδ1, hb⟩ :=
    I4SourceCompactTargetMoments.sourceInverse_target_uniform_bounds hL
  refine ⟨δ, hδ, hδ1, ?_⟩
  intro r hr hrδ x hxM hxS
  have hG := (hb r hr hrδ).1
  refine ⟨rawPinKernel_map_hasCondDistrib hL r hr.ne' hG _ (remoteJet_measurable hL x),
    remoteResidualCovariance_posDef hL r x hxM hxS, ?_⟩
  intro t
  exact ⟨rawPinKernel_remoteJet_eq_multivariateGaussian hL r x t,
    rawPinKernel_pin_fiber hL r hr.ne' hG t⟩

end I4SourceRemoteJetGaussian
