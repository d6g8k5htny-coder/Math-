import SourcePinCurvatureBounds

noncomputable section
open I4SmoothCarrier I4SourceConfluentPins I4SourceEndpointRegression
open I4SourcePinCurvatureBounds I4SourceConditionalMajorant I4SourceEndpointEstimates
open I4SourceSmoothPalm I4SourceSmoothConditional ResearchFormalCoreR1
open I4SourceDerivativeGaussian I4SourceGaussian
open MeasureTheory Set Matrix Filter
open scoped Interval BigOperators Topology
set_option autoImplicit false

namespace I4SourcePinCurvatureBounds

theorem sourceQ_measurable {L : ℝ} (hL : L ≠ 0) : Measurable (sourceQ L) := by
  have he : sourceQ L = fun ω => scalarSeries
      (derivativeCoefficient 2 L 2 0 ![directionY,directionY]) (sampleInclusion 2 L ω) := by
    funext ω
    exact smoothSourceField_derivative_series 2 hL ω 2 0 _
  rw [he]
  exact (scalarSeries_measurable _).comp (sampleInclusion_measurable 2 L)

theorem sourceA_measurable {L : ℝ} (hL : L ≠ 0) : Measurable (sourceA L) := by
  have he : sourceA L = fun ω => scalarSeries
      (derivativeCoefficient 2 L 3 0 ![directionX,directionX,directionY]) (sampleInclusion 2 L ω) := by
    funext ω
    exact smoothSourceField_derivative_series 2 hL ω 3 0 _
  rw [he]
  exact (scalarSeries_measurable _).comp (sampleInclusion_measurable 2 L)

theorem source_normalized_determinant_bounds {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1) (ω : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0)
    (h5 : sourceConfluentPinsAt L r ω 5 = 2) :
    |sourceNormalizedEndpoints L r ω 0*sourceNormalizedEndpoints L r ω 4-
      r*sourceNormalizedEndpoints L r ω 2^2| ≤
      sourceGammaRadius L ω*|sourceQ L ω|+2*r*sourceGammaRadius L ω^2 ∧
    |sourceNormalizedEndpoints L r ω 1*sourceNormalizedEndpoints L r ω 5-
      r*sourceNormalizedEndpoints L r ω 3^2| ≤
      sourceGammaRadius L ω*|sourceQ L ω|+2*r*sourceGammaRadius L ω^2 := by
  have hv := source_normalized_endpoint_first_four_bounds hL r hr hr1 ω h3 h4 h5
  obtain ⟨_,_,_,_,hM,hS⟩ := source_normalized_endpoint_errors hL r hr ω h3 h4 h5
  have hΓ : sourceDerivativeMajorant L 3 ω ≤ sourceGammaRadius L ω :=
    sourceDerivativeMajorant_le_radius L ω 3
  have hM' := hM.trans (mul_le_mul_of_nonneg_left hΓ hr.le)
  have hS' := hS.trans (mul_le_mul_of_nonneg_left hΓ hr.le)
  exact ⟨endpoint_det_abs_le r _ _ hr.le (sourceGammaRadius_nonneg L ω) _ _ _
      (hv 0) (hv 2) hM',
    endpoint_det_abs_le r _ _ hr.le (sourceGammaRadius_nonneg L ω) _ _ _
      (hv 1) (hv 3) hS'⟩

/-- The physical strict-type determinant weight of the actual field has the
curvature bound, including its zero-type boundary. -/
theorem sourceSmoothWeight_curvature_bound {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1) (ω : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0)
    (h5 : sourceConfluentPinsAt L r ω 5 = 2) :
    sourceSmoothWeight L r ω ≤
      2*r^2*sourceGammaRadius L ω^2*sourceQ L ω^2+8*r^4*sourceGammaRadius L ω^4 := by
  have hv := source_normalized_endpoint_first_four_bounds hL r hr hr1 ω h3 h4 h5
  obtain ⟨_,_,_,_,hM,hS⟩ := source_normalized_endpoint_errors hL r hr ω h3 h4 h5
  have hΓ : sourceDerivativeMajorant L 3 ω ≤ sourceGammaRadius L ω :=
    sourceDerivativeMajorant_le_radius L ω 3
  rw [sourceSmoothWeight_eq L r hr.ne' ω]
  exact endpointWeight_curvature_le r _ _ hr.le (sourceGammaRadius_nonneg L ω) _
    (hv 0) (hv 1) (hv 2) (hv 3)
    (hM.trans (mul_le_mul_of_nonneg_left hΓ hr.le))
    (hS.trans (mul_le_mul_of_nonneg_left hΓ hr.le))

theorem source_positive_weight_curvature_upper {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (ω : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0)
    (h5 : sourceConfluentPinsAt L r ω 5 = 2)
    (hW : 0 < sourceSmoothWeight L r ω) :
    sourceQ L ω < r*sourceDerivativeMajorant L 3 ω := by
  have ht := (sourceSmoothWeight_pos_iff L r ω).mp hW
  have hneg : sourceNormalizedEndpoints L r ω 4 < 0 := by
    apply strict_endpoint_transverse_neg r _
    rw [← sourceRawHM_eq_normalized L r hr.ne' ω]
    exact ht.1
  have herror := (source_normalized_endpoint_errors hL r hr ω h3 h4 h5).2.2.2.2.1
  have hlow := (abs_le.mp herror).1
  linarith

theorem source_bad_curvature_slab {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (ω : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0)
    (h5 : sourceConfluentPinsAt L r ω 5 = 2)
    (hW : 0 < sourceSmoothWeight L r ω) (K : ℝ)
    (hq : -K*r*sourceGammaRadius L ω^5 ≤ sourceQ L ω) :
    |sourceQ L ω| ≤ max K 1*r*sourceGammaRadius L ω^5 :=
  curvature_slab_of_upper _ _ _ _ K hr.le (one_le_sourceGammaRadius L ω)
    (sourceDerivativeMajorant_le_radius L ω 3)
    (source_positive_weight_curvature_upper hL r hr ω h3 h4 h5 hW) hq

/-- The completed actual all-pin support supplies the three pin equations. -/
theorem source_prescribed_pin_constraints_ae {L : ℝ} (hL : L ≠ 0) (r b : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) :
    ∀ᵐ ω ∂sourceSmoothLaw hL r b,
      sourceConfluentPinsAt L r ω 3 = 0 ∧ sourceConfluentPinsAt L r ω 4 = 0 ∧
      sourceConfluentPinsAt L r ω 5 = 2 := by
  have hm : MeasurableSet {ω : SmoothSample 2 L |
      sourceConfluentPinsAt L r ω = sourcePrescribedPins r b} :=
    measurableSet_eq_fun (sourceConfluentPinsAt_measurable hL r) measurable_const
  have hp : ∀ᵐ ω ∂sourceSmoothLaw hL r b,
      sourceConfluentPinsAt L r ω = sourcePrescribedPins r b := by
    apply (mem_ae_iff_prob_eq_one hm).2
    exact sourceSmoothKernel_pin_fiber hL r hG (sourcePrescribedPins r b)
  filter_upwards [hp] with ω hω
  exact ⟨by simpa [sourcePrescribedPins] using congrFun hω 3,
    by simpa [sourcePrescribedPins] using congrFun hω 4,
    by simpa [sourcePrescribedPins] using congrFun hω 5⟩

theorem sourceSmoothLaw_curvature_bound_ae {L : ℝ} (hL : L ≠ 0) (r b : ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1) (hG : IsUnit (sourcePinCovarianceAt L r)) :
    ∀ᵐ ω ∂sourceSmoothLaw hL r b,
      sourceSmoothWeight L r ω ≤
        2*r^2*sourceGammaRadius L ω^2*sourceQ L ω^2+8*r^4*sourceGammaRadius L ω^4 ∧
      (∀ K : ℝ, 0 < sourceSmoothWeight L r ω →
        -K*r*sourceGammaRadius L ω^5 ≤ sourceQ L ω →
        |sourceQ L ω| ≤ max K 1*r*sourceGammaRadius L ω^5) := by
  filter_upwards [source_prescribed_pin_constraints_ae hL r b hG] with ω hω
  exact ⟨sourceSmoothWeight_curvature_bound hL r hr hr1 ω hω.1 hω.2.1 hω.2.2,
    fun K hW hq => source_bad_curvature_slab hL r hr ω hω.1 hω.2.1 hω.2.2 hW K hq⟩

/-- Only the actual nonzero period and fixed height remain as model premises;
current covariance invertibility and all-pin support are derived upstream. -/
theorem source_curvature_estimates {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothLaw hL r b,
        sourceSmoothWeight L r ω ≤
          2*r^2*sourceGammaRadius L ω^2*sourceQ L ω^2+8*r^4*sourceGammaRadius L ω^4 ∧
        (∀ K : ℝ, 0 < sourceSmoothWeight L r ω →
          -K*r*sourceGammaRadius L ω^5 ≤ sourceQ L ω →
          |sourceQ L ω| ≤ max K 1*r*sourceGammaRadius L ω^5) := by
  obtain ⟨δ,hδ,hsub⟩ := mem_nhdsGT_iff_exists_Ioo_subset.mp
    (sourceEndpoint_parameter_limits hL b).1
  refine ⟨min δ 1,lt_min hδ (by norm_num),min_le_right _ _,?_⟩
  intro r hr hrδ
  exact sourceSmoothLaw_curvature_bound_ae hL r b hr
    (hrδ.le.trans (min_le_right _ _))
    (hsub ⟨hr,lt_of_lt_of_le hrδ (min_le_left _ _)⟩)

end I4SourcePinCurvatureBounds
