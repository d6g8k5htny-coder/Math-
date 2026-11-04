import SourceCompactGapNormalizer

noncomputable section

open I4Foundation I4Source I4SmoothCarrier I4Smooth I4SourceConfluentPins
open I4SourceEndpointRegression I4SourceEndpointEstimates I4SourceSmoothConditional
open I4SourceSmoothPalm I4SourceConditionalMajorant I4SourcePinCurvatureBounds
open I4SourceCompactTargetMoments I4SourceCurvatureDecomposition
open SourceCompactGapNormalizer ResearchFormalCoreR1
open MeasureTheory ProbabilityTheory Set Matrix
open scoped Topology NNReal

set_option autoImplicit false

namespace CompactGapNormalizerControls

theorem generic_closed_actual {L : ℝ} (hL : L ≠ 0)
    (B k0 k1 : ℝ) (hB : 0 ≤ B) (hk0 : 0 < k0) (hk01 : k0 ≤ k1) :
    ∃ c δ : ℝ, 0 < c ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → k0 ≤ k → k ≤ k1 →
        Integrable (sourceSmoothWeight L r) (sourceGapLaw hL r b k) ∧
        c*r^2 ≤ ∫ ω, sourceSmoothWeight L r ω ∂sourceGapLaw hL r b k :=
  sourceGapLaw_compact_normalizer hL B k0 k1 hB hk0 hk01

theorem negative_period : (-1 : ℝ) ≠ 0 := by norm_num

/-- One pair c,delta handles two nondefault marks under the original signed period. -/
theorem signed_period_nondefault_marks :
    ∃ c δ : ℝ, 0 < c ∧ 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      (Integrable (sourceSmoothWeight (-1) r) (sourceGapLaw negative_period r 3 1) ∧
        c*r^2 ≤ ∫ ω, sourceSmoothWeight (-1) r ω ∂sourceGapLaw negative_period r 3 1) ∧
      (Integrable (sourceSmoothWeight (-1) r) (sourceGapLaw negative_period r 3 2) ∧
        c*r^2 ≤ ∫ ω, sourceSmoothWeight (-1) r ω ∂sourceGapLaw negative_period r 3 2) := by
  obtain ⟨c,δ,hc,hδ,hδ1,h⟩ := sourceGapLaw_compact_normalizer negative_period
    3 1 2 (by norm_num) (by norm_num) (by norm_num)
  exact ⟨c,δ,hc,hδ,hδ1,fun r hr hrδ =>
    ⟨h r hr hrδ 3 1 (by norm_num) (by norm_num) (by norm_num),
      h r hr hrδ 3 2 (by norm_num) (by norm_num) (by norm_num)⟩⟩

/-- This real Bochner integral is strictly positive, and integrability is explicit. -/
theorem signed_period_positive_real_integral :
    ∃ δ : ℝ, 0 < δ ∧ ∀ r : ℝ, 0 < r → r < δ →
      Integrable (sourceSmoothWeight (-1) r) (sourceGapLaw negative_period r 3 2) ∧
      0 < ∫ ω, sourceSmoothWeight (-1) r ω ∂sourceGapLaw negative_period r 3 2 := by
  obtain ⟨c,δ,hc,hδ,_hδ1,h⟩ := signed_period_nondefault_marks
  refine ⟨δ,hδ,?_⟩
  intro r hr hrδ
  exact ⟨(h r hr hrδ).2.1,(mul_pos hc (sq_pos_of_pos hr)).trans_le (h r hr hrδ).2.2⟩

/-- The actual affine target stays visible at b=3,k=2, rather than a zero mean. -/
theorem bounded_affine_mean (hβ : ∀ i, |curvatureBeta (-1) (1/4) i| ≤ 1) :
    |curvatureMean (-1) (1/4) (sourceGapPins (1/4) 3 2)| ≤ 174 := by
  have h := sourceGap_curvatureMean_bound (-1) (1/4) 3 2 3 2 1
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) hβ
  norm_num at h ⊢
  exact h

/-- Both variance endpoints are used, with a nonzero bounded mean. -/
theorem gaussian_two_variance_endpoints :
    gaussianCompactLowerConstant 2 3 ≤ gaussianPDFReal 2 1 (-2) ∧
    gaussianCompactLowerConstant 2 3 ≤ gaussianPDFReal 2 4 (-2) := by
  constructor
  · exact gaussianPDFReal_lower_compact 2 3 2 1
      (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  · exact gaussianPDFReal_lower_compact 2 3 2 4
      (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)

/-- Actual strict physical types and the coarse quadratic lower bound. -/
theorem literal_strict_physical_floor :
    (dm2Negative (egm_HM (1/4) (sourcePhysicalCoordinates ![-6,6,0,0,-1,-1])) ∧
      (egm_HS (1/4) (sourcePhysicalCoordinates ![-6,6,0,0,-1,-1])).det < 0) ∧
    (1:ℝ)^2*(1/4)^2 ≤ sourceEndpointWeight (1/4) ![-6,6,0,0,-1,-1] := by
  apply endpointWeight_gap_floor (1/4) 1 1 1 (-1) ![-6,6,0,0,-1,-1] <;> norm_num

/-- Unit normalized determinants carry the literal physical r-squared factor. -/
theorem physical_unit_determinant_weight :
    sourceEndpointWeight (1/4) ![-1,1,0,0,-1,-1] = (1/4:ℝ)^2 := by
  norm_num [sourceEndpointWeight,egm_weight,sourcePhysicalCoordinates,egm_HM,egm_HS,
    dm2_negative_iff,Matrix.det_fin_two]

theorem omitted_radius_square_counterexample :
    ¬ (1:ℝ) ≤ sourceEndpointWeight (1/4) ![-1,1,0,0,-1,-1] := by
  rw [physical_unit_determinant_weight]
  norm_num

end CompactGapNormalizerControls
