import SourceRawPinConditioning

noncomputable section
open I4SmoothCarrier I4SourceConfluentPins I4SourceEndpointRegression I4SourceEndpointEstimates
open I4SourceSmoothConditional I4SourceSmoothPalm I4SourceRawPinConditioning
open MeasureTheory ProbabilityTheory Filter Matrix
open scoped Topology Matrix
set_option autoImplicit false

-- This raw target has nonzero unequal heights and four nonzero gradients.
-- The actual source supplies the covariance hypothesis on a small-radius interval.
example : ∀ᶠ r in 𝓝[>] (0 : ℝ),
    rawPins 1 r (rawPosteriorSample (by norm_num : (1 : ℝ) ≠ 0) r
      ![3,-2,1,4,-5,7] (zeroSample 2 1)) = ![3,-2,1,4,-5,7] := by
  filter_upwards [(sourceEndpoint_parameter_limits (by norm_num : (1 : ℝ) ≠ 0) 0).1,
    self_mem_nhdsWithin] with r hG hr
  exact rawPosteriorSample_rawPins (by norm_num) r (ne_of_gt hr) hG _ _

-- The literal confluent transform mixes the value and derivative observations.
example : confluentMatrix 2 (by norm_num) *ᵥ ![3,1,4,-2,5,-1] =
    (![2,1,2,-3,-3,6] : Fin 6 → ℝ) := by
  rw [confluentMatrix_mulVec]
  ext i
  fin_cases i <;> norm_num [confluentTransform]

-- Both target factors are essential even in a one-dimensional nontrivial row map.
example : ((2:ℝ)*3) * (1/(2*1*2)) * (2*5) = 3*(1/1)*5 := by norm_num

-- The actual identity-valued RCD is conditioned on raw observations, with only L≠0.
example : ∀ᶠ r in 𝓝[>] (0 : ℝ),
    HasCondDistrib (id : SmoothSample 2 1 → SmoothSample 2 1) (rawPins 1 r)
      (rawPinKernel (by norm_num : (1 : ℝ) ≠ 0) r) (smoothLaw 2 1) :=
  rawPinKernel_eventually_hasCondDistrib (by norm_num)

-- The actual nonzero height b=3 retains probability and both physical supports.
example : ∃ δ : ℝ, 0 < δ ∧ ∀ r : ℝ, 0 < r → r < δ →
    IsProbabilityMeasure (rawPrescribedWeightedMeasure (by norm_num : (1 : ℝ) ≠ 0) r 3) ∧
      rawPrescribedWeightedMeasure (by norm_num : (1 : ℝ) ≠ 0) r 3
        {ω | rawPins 1 r ω = ![3,3-r^3/6,0,0,0,0]} = 1 ∧
      rawPrescribedWeightedMeasure (by norm_num : (1 : ℝ) ≠ 0) r 3
        {ω | sourceSmoothTyped 1 r ω} = 1 := by
  obtain ⟨C,c,δ,_hC,_hc,hδ,_hδ1,hest⟩ :=
    rawPrescribedWeightedMeasure_estimates (by norm_num : (1 : ℝ) ≠ 0) 3
  refine ⟨δ,hδ,?_⟩
  intro r hr hrδ
  obtain ⟨_hsq,_hm,_hf,hprob,_hevent,_hmap,hraw,htype⟩ := hest r hr hrδ
  exact ⟨hprob,hraw,htype⟩
