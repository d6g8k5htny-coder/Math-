import SourceGapPinCurvature

noncomputable section

open I4Foundation I4Source I4SmoothCarrier I4Smooth I4SourceConfluentPins
open I4SourceEndpointRegression I4SourceEndpointEstimates I4SourceSmoothConditional
open I4SourceSmoothPalm I4SourceConditionalMajorant I4SourcePinCurvatureBounds
open I4SourceCompactTargetMoments I4PeanoErrorBounds I4ConfluentIntegralIdentities
open MeasureTheory ProbabilityTheory Set Matrix
open scoped Interval Topology

set_option autoImplicit false

open ResearchFormalCoreR1

namespace GapPinCurvatureControls

theorem generic_all_target {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : 0 < r) (p : Fin 6 → ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (h3 : p 3 = 0) (h4 : p 4 = 0) :
    ∀ᵐ sample ∂sourceSmoothKernel hL r p,
      sourceConfluentPinsAt L r sample = p ∧
      sourceSmoothWeight L r sample ≤
        2*r^2*sourceGammaRadius L sample^2*sourceQ L sample^2+
          8*r^4*sourceGammaRadius L sample^4 ∧
      (r ≤ 1 → sourceSmoothWeight L r sample ≤ 10*r^2*sourceGammaRadius L sample^4) ∧
      (0 < sourceSmoothWeight L r sample →
        sourceQ L sample < r*sourceDerivativeMajorant L 3 sample) ∧
      (∀ A : ℝ, 0 < sourceSmoothWeight L r sample →
        -A*r*sourceGammaRadius L sample^5 ≤ sourceQ L sample →
        |sourceQ L sample| ≤ max A 1*r*sourceGammaRadius L sample^5) :=
  I4SourceGapPinCurvature.sourceSmoothKernel_curvature_bounds_ae hL r hr p hG h3 h4

theorem generic_closed_gap {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ,
      ∀ᵐ sample ∂sourceGapLaw hL r b k,
        sourceConfluentPinsAt L r sample = sourceGapPins r b k ∧
        sourceSmoothWeight L r sample ≤
          2*r^2*sourceGammaRadius L sample^2*sourceQ L sample^2+
            8*r^4*sourceGammaRadius L sample^4 ∧
        sourceSmoothWeight L r sample ≤ 10*r^2*sourceGammaRadius L sample^4 ∧
        (0 < sourceSmoothWeight L r sample →
          sourceQ L sample < r*sourceDerivativeMajorant L 3 sample) ∧
        (∀ A : ℝ, 0 < sourceSmoothWeight L r sample →
          -A*r*sourceGammaRadius L sample^5 ≤ sourceQ L sample →
          |sourceQ L sample| ≤ max A 1*r*sourceGammaRadius L sample^5) :=
  I4SourceGapPinCurvature.sourceGapLaw_curvature_bounds hL

theorem negative_period : (-1 : ℝ) ≠ 0 := by norm_num

/-- Nondefault target: the literal sixth coordinate is twelve, never two. -/
theorem nondefault_slot5 (r : ℝ) :
    sourceGapPins r 3 1 5 = 12 ∧ sourceGapPins r 3 1 5 ≠ 2 := by
  norm_num [sourceGapPins]

theorem negative_gap_slot5 (r : ℝ) : sourceGapPins r 3 (-2) 5 = -24 := by
  norm_num [sourceGapPins]

/-- The same hL-only interval works for k=1 and k=-2 at original L=-1. -/
theorem closed_nondefault_negative_period :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      (∀ᵐ sample ∂sourceGapLaw negative_period r 3 1,
        sourceConfluentPinsAt (-1) r sample 5 = 12 ∧
        sourceSmoothWeight (-1) r sample ≤
          2*r^2*sourceGammaRadius (-1) sample^2*sourceQ (-1) sample^2+
            8*r^4*sourceGammaRadius (-1) sample^4 ∧
        (∀ A : ℝ, 0 < sourceSmoothWeight (-1) r sample →
          -A*r*sourceGammaRadius (-1) sample^5 ≤ sourceQ (-1) sample →
          |sourceQ (-1) sample| ≤ max A 1*r*sourceGammaRadius (-1) sample^5)) ∧
      (∀ᵐ sample ∂sourceGapLaw negative_period r 3 (-2),
        sourceConfluentPinsAt (-1) r sample 5 = -24 ∧
        sourceSmoothWeight (-1) r sample ≤ 10*r^2*sourceGammaRadius (-1) sample^4) := by
  obtain ⟨δ,hδ,hδ1,hb⟩ := I4SourceGapPinCurvature.sourceGapLaw_curvature_bounds negative_period
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ
  constructor
  · filter_upwards [hb r hr hrδ 3 1] with sample hs
    exact ⟨(congrFun hs.1 5).trans (nondefault_slot5 r).1, hs.2.1, hs.2.2.2.2⟩
  · filter_upwards [hb r hr hrδ 3 (-2)] with sample hs
    exact ⟨(congrFun hs.1 5).trans (negative_gap_slot5 r), hs.2.2.1⟩

/-- Actual q-error, positive-weight and slab exports have no pin premises. -/
theorem pin_free_transverse_and_slab (r : ℝ) (hr : 0 < r)
    (sample : SmoothSample 2 (-1)) :
    (|sourceNormalizedEndpoints (-1) r sample 4 - sourceQ (-1) sample| ≤
        r*sourceDerivativeMajorant (-1) 3 sample ∧
      |sourceNormalizedEndpoints (-1) r sample 5 - sourceQ (-1) sample| ≤
        r*sourceDerivativeMajorant (-1) 3 sample) ∧
    (0 < sourceSmoothWeight (-1) r sample →
      sourceQ (-1) sample < r*sourceDerivativeMajorant (-1) 3 sample) ∧
    (∀ A : ℝ, 0 < sourceSmoothWeight (-1) r sample →
      -A*r*sourceGammaRadius (-1) sample^5 ≤ sourceQ (-1) sample →
      |sourceQ (-1) sample| ≤ max A 1*r*sourceGammaRadius (-1) sample^5) :=
  ⟨I4SourceGapPinCurvature.source_normalized_transverse_errors negative_period r hr.le sample,
    I4SourceGapPinCurvature.source_positive_weight_curvature_upper negative_period r hr sample,
    fun A hW hq => I4SourceGapPinCurvature.source_bad_curvature_slab
      negative_period r hr sample hW A hq⟩

/-- Direct Peano first-four bounds do not need r positive or bounded above. -/
theorem negative_radius_first_four (sample : SmoothSample 2 (-1))
    (h3 : sourceConfluentPinsAt (-1) (-3) sample 3 = 0)
    (h4 : sourceConfluentPinsAt (-1) (-3) sample 4 = 0) :
    ∀ i : Fin 4, |sourceNormalizedEndpoints (-1) (-3) sample i.castSucc.castSucc| ≤
      sourceDerivativeMajorant (-1) 3 sample/2 :=
  I4SourceGapPinCurvature.source_normalized_first_four_third_bound negative_period (-3)
    (by norm_num) sample h3 h4

/-- The physical strict-type weight really is positive for nonzero q. -/
theorem physical_q_weight_value :
    sourceEndpointWeight (1/4) ![-1,1,0,0,-1/2,-1/2] = 1/64 := by
  norm_num [sourceEndpointWeight, egm_weight, sourcePhysicalCoordinates, egm_HM, egm_HS,
    dm2_negative_iff, Matrix.det_fin_two]

/-- The strict boundary at q=0 contributes zero. -/
theorem physical_q_zero_weight : sourceEndpointWeight (1/4) ![-1,1,0,0,0,0] = 0 := by
  norm_num [sourceEndpointWeight, egm_weight, sourcePhysicalCoordinates, egm_HM, egm_HS,
    dm2_negative_iff, Matrix.det_fin_two]

/-- The retained q-sensitive determinant estimate is exercised at nonzero q. -/
theorem q_sensitive_weight_arithmetic :
    sourceEndpointWeight (1/4) ![-1,1,0,0,-1/2,-1/2] ≤
      2*(1/4:ℝ)^2*1^2*(-1/2)^2+8*(1/4:ℝ)^4*1^4 := by
  apply endpointWeight_curvature_le (1/4) 1 (-1/2) (by norm_num) (by norm_num)
    ![-1,1,0,0,-1/2,-1/2] <;> norm_num

theorem q_sensitive_ceiling_changes :
    (2*(1/4:ℝ)^2*1^2*0^2+8*(1/4:ℝ)^4*1^4) <
      2*(1/4:ℝ)^2*1^2*(-1/2)^2+8*(1/4:ℝ)^4*1^4 := by norm_num

/-- Nonzero negative q saturates the one-sided-to-symmetric slab at A=3. -/
theorem slab_arithmetic_saturation :
    |(-3/2 : ℝ)| ≤ max (3:ℝ) 1*(1/2)*1^5 ∧
    |(-3/2 : ℝ)| = max (3:ℝ) 1*(1/2)*1^5 := by
  constructor
  · exact curvature_slab_of_upper (-3/2) (1/2) 1 1 3
      (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  · norm_num

end GapPinCurvatureControls
