import SourceCompactTargetMoments

/-!
# Physical curvature estimates at every cubic-gap target

The affine Peano kernels bound the first four physical normalized endpoint
entries by half the actual third derivative majorant. Only the two zero
gradient-difference pins enter. Transverse errors and the strict-type curvature
consequences need no pin equations. The actual gap-law conclusion derives its
support and covariance invertibility on one interval from the nonzero period.
No value is prescribed for pin 5 beyond its literal target `12*k`.
-/

noncomputable section

open I4Foundation I4Source I4SmoothCarrier I4Smooth I4SourceConfluentPins
open I4SourceEndpointRegression I4SourceEndpointEstimates I4SourceSmoothConditional
open I4SourceSmoothPalm I4SourceConditionalMajorant I4SourcePinCurvatureBounds
open I4SourceCompactTargetMoments I4PeanoErrorBounds I4ConfluentIntegralIdentities
open MeasureTheory ProbabilityTheory Set Matrix
open scoped Interval Topology

set_option autoImplicit false

namespace I4SourceGapPinCurvature

/-- Direct affine Peano bounds, independent of the sixth pin and of a radius cap. -/
theorem source_normalized_first_four_third_bound {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : r ≠ 0) (sample : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r sample 3 = 0)
    (h4 : sourceConfluentPinsAt L r sample 4 = 0) :
    ∀ i : Fin 4, |sourceNormalizedEndpoints L r sample i.castSucc.castSucc| ≤
      sourceDerivativeMajorant L 3 sample / 2 := by
  have hf (t : ℝ) (_ht : t ∈ Icc (-1/2:ℝ) (1/2:ℝ)) :
      |iteratedDeriv 3 (sourceF L sample) (r*t) - 0| ≤
        sourceDerivativeMajorant L 3 sample := by
    simpa only [sub_zero] using sourceF_third_abs_le hL sample (r*t)
  have hh (t : ℝ) (_ht : t ∈ Icc (-1/2:ℝ) (1/2:ℝ)) :
      |iteratedDeriv 2 (sourceH L sample) (r*t) - 0| ≤
        sourceDerivativeMajorant L 3 sample := by
    simpa only [sub_zero] using sourceH_second_abs_le hL sample (r*t)
  have hfM := left_weighted_error _ (sourceF_third_continuous hL sample) r 0
    (sourceDerivativeMajorant L 3 sample) hf
  have hfS := right_weighted_error _ (sourceF_third_continuous hL sample) r 0
    (sourceDerivativeMajorant L 3 sample) hf
  have hhM := left_weighted_error _ (sourceH_second_continuous hL sample) r 0
    (sourceDerivativeMajorant L 3 sample) hh
  have hhS := right_weighted_error _ (sourceH_second_continuous hL sample) r 0
    (sourceDerivativeMajorant L 3 sample) hh
  rw [source_normalized_peano hL r hr sample h3 h4]
  intro i
  fin_cases i
  · change |-(∫ u in (-1/2:ℝ)..(1/2:ℝ),
        I4SourceConfluentLimits.peanoLeft u * iteratedDeriv 3 (sourceF L sample) (r*u))| ≤ _
    simpa only [abs_neg, zero_div, sub_zero] using hfM
  · change |(∫ u in (-1/2:ℝ)..(1/2:ℝ),
        I4SourceConfluentLimits.peanoRight u * iteratedDeriv 3 (sourceF L sample) (r*u))| ≤ _
    simpa only [zero_div, sub_zero] using hfS
  · change |-(∫ u in (-1/2:ℝ)..(1/2:ℝ),
        I4SourceConfluentLimits.peanoLeft u * iteratedDeriv 2 (sourceH L sample) (r*u))| ≤ _
    simpa only [abs_neg, zero_div, sub_zero] using hhM
  · change |(∫ u in (-1/2:ℝ)..(1/2:ℝ),
        I4SourceConfluentLimits.peanoRight u * iteratedDeriv 2 (sourceH L sample) (r*u))| ≤ _
    simpa only [zero_div, sub_zero] using hhS

/-- All four entries are bounded by the original radius for every nonzero r. -/
theorem source_normalized_first_four_bound {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : r ≠ 0) (sample : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r sample 3 = 0)
    (h4 : sourceConfluentPinsAt L r sample 4 = 0) :
    ∀ i : Fin 4, |sourceNormalizedEndpoints L r sample i.castSucc.castSucc| ≤
      sourceGammaRadius L sample := by
  intro i
  exact (source_normalized_first_four_third_bound hL r hr sample h3 h4 i).trans
    ((by linarith [sourceDerivativeMajorant_nonneg L 3 sample] :
      sourceDerivativeMajorant L 3 sample / 2 ≤ sourceDerivativeMajorant L 3 sample).trans
      (sourceDerivativeMajorant_le_radius L sample 3))

/-- The transverse endpoint errors need no pin equations at all. -/
theorem source_normalized_transverse_errors {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : 0 ≤ r) (sample : SmoothSample 2 L) :
    |sourceNormalizedEndpoints L r sample 4 - sourceQ L sample| ≤
      r*sourceDerivativeMajorant L 3 sample ∧
    |sourceNormalizedEndpoints L r sample 5 - sourceQ L sample| ≤
      r*sourceDerivativeMajorant L 3 sample := by
  have hq (u : ℝ) (hu : u ∈ Icc (-1/2:ℝ) (1/2:ℝ)) :
      |sourceQCurve L sample (r*u) - sourceQ L sample| ≤
        r*sourceDerivativeMajorant L 3 sample := by
    have h := scaled_lipschitz_center_error _ _ r
      (sourceDerivativeMajorant_nonneg L 3 sample) hr
      (sourceQCurve_lipschitz hL sample) u hu
    rw [sourceQCurve_zero] at h
    exact h.trans (by nlinarith [mul_nonneg hr (sourceDerivativeMajorant_nonneg L 3 sample)])
  constructor
  · change |sourceQCurve L sample (-r/2) - sourceQ L sample| ≤ _
    have h := hq (-1/2) (by constructor <;> norm_num)
    simpa only [show r*(-1/2) = -r/2 by ring] using h
  · change |sourceQCurve L sample (r/2) - sourceQ L sample| ≤ _
    have h := hq (1/2) (by constructor <;> norm_num)
    simpa only [show r*(1/2) = r/2 by ring] using h

/-- The two literal physical normalized determinant factors. -/
theorem source_normalized_determinant_bounds {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : 0 < r) (sample : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r sample 3 = 0)
    (h4 : sourceConfluentPinsAt L r sample 4 = 0) :
    |sourceNormalizedEndpoints L r sample 0*sourceNormalizedEndpoints L r sample 4-
      r*sourceNormalizedEndpoints L r sample 2^2| ≤
      sourceGammaRadius L sample*|sourceQ L sample|+2*r*sourceGammaRadius L sample^2 ∧
    |sourceNormalizedEndpoints L r sample 1*sourceNormalizedEndpoints L r sample 5-
      r*sourceNormalizedEndpoints L r sample 3^2| ≤
      sourceGammaRadius L sample*|sourceQ L sample|+2*r*sourceGammaRadius L sample^2 := by
  have hv := source_normalized_first_four_bound hL r hr.ne' sample h3 h4
  obtain ⟨hM,hS⟩ := source_normalized_transverse_errors hL r hr.le sample
  have hΓ := mul_le_mul_of_nonneg_left (sourceDerivativeMajorant_le_radius L sample 3) hr.le
  exact ⟨endpoint_det_abs_le r _ _ hr.le (sourceGammaRadius_nonneg L sample) _ _ _
      (hv 0) (hv 2) (hM.trans hΓ),
    endpoint_det_abs_le r _ _ hr.le (sourceGammaRadius_nonneg L sample) _ _ _
      (hv 1) (hv 3) (hS.trans hΓ)⟩

/-- Exact physical q-sensitive weight estimate, with no sixth-pin restriction. -/
theorem sourceSmoothWeight_curvature_bound {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : 0 < r) (sample : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r sample 3 = 0)
    (h4 : sourceConfluentPinsAt L r sample 4 = 0) :
    sourceSmoothWeight L r sample ≤
      2*r^2*sourceGammaRadius L sample^2*sourceQ L sample^2+
        8*r^4*sourceGammaRadius L sample^4 := by
  have hv := source_normalized_first_four_bound hL r hr.ne' sample h3 h4
  obtain ⟨hM,hS⟩ := source_normalized_transverse_errors hL r hr.le sample
  have hΓ := mul_le_mul_of_nonneg_left (sourceDerivativeMajorant_le_radius L sample 3) hr.le
  rw [sourceSmoothWeight_eq L r hr.ne' sample]
  exact endpointWeight_curvature_le r _ _ hr.le (sourceGammaRadius_nonneg L sample) _
    (hv 0) (hv 1) (hv 2) (hv 3) (hM.trans hΓ) (hS.trans hΓ)

/-- Strict maximum type forces the upper curvature bound, without any pins. -/
theorem source_positive_weight_curvature_upper {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : 0 < r) (sample : SmoothSample 2 L)
    (hW : 0 < sourceSmoothWeight L r sample) :
    sourceQ L sample < r*sourceDerivativeMajorant L 3 sample := by
  have ht := (sourceSmoothWeight_pos_iff L r sample).mp hW
  have hneg : sourceNormalizedEndpoints L r sample 4 < 0 := by
    apply strict_endpoint_transverse_neg r _
    rw [← sourceRawHM_eq_normalized L r hr.ne' sample]
    exact ht.1
  have hlow := (abs_le.mp (source_normalized_transverse_errors hL r hr.le sample).1).1
  linarith

/-- The one-sided obstruction lies in this symmetric slab; no pin is needed. -/
theorem source_bad_curvature_slab {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : 0 < r) (sample : SmoothSample 2 L)
    (hW : 0 < sourceSmoothWeight L r sample) (A : ℝ)
    (hq : -A*r*sourceGammaRadius L sample^5 ≤ sourceQ L sample) :
    |sourceQ L sample| ≤ max A 1*r*sourceGammaRadius L sample^5 :=
  curvature_slab_of_upper _ _ _ _ A hr.le (one_le_sourceGammaRadius L sample)
    (sourceDerivativeMajorant_le_radius L sample 3)
    (source_positive_weight_curvature_upper hL r hr sample hW) hq

/-- A coarse physical weight bound on the unit radius interval. -/
theorem sourceSmoothWeight_radius_bound {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : 0 < r) (hr1 : r ≤ 1) (sample : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r sample 3 = 0)
    (h4 : sourceConfluentPinsAt L r sample 4 = 0) :
    sourceSmoothWeight L r sample ≤ 10*r^2*sourceGammaRadius L sample^4 := by
  have hq : sourceQ L sample^2 ≤ sourceGammaRadius L sample^2 := by
    simpa only [sq_abs] using pow_le_pow_left₀ (abs_nonneg (sourceQ L sample))
      ((sourceQ_abs_le hL sample).trans (sourceDerivativeMajorant_le_radius L sample 2)) 2
  have hr2 : r^2 ≤ 1 := by nlinarith [sq_nonneg r]
  have hr4 : r^4 ≤ r^2 := by nlinarith [sq_nonneg r]
  calc
    _ ≤ 2*r^2*sourceGammaRadius L sample^2*sourceQ L sample^2+
        8*r^4*sourceGammaRadius L sample^4 :=
      sourceSmoothWeight_curvature_bound hL r hr sample h3 h4
    _ ≤ 2*r^2*sourceGammaRadius L sample^2*sourceGammaRadius L sample^2+
        8*r^2*sourceGammaRadius L sample^4 := add_le_add
      (mul_le_mul_of_nonneg_left hq (by positivity))
      (mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_left hr4 (by norm_num))
        (pow_nonneg (sourceGammaRadius_nonneg L sample) 4))
    _ = _ := by ring

/-- Every literal target with zero rows 3 and 4 has the physical estimates.
The all-target posterior support is derived, not an endpoint estimate premise. -/
theorem sourceSmoothKernel_curvature_bounds_ae {L : ℝ} (hL : L ≠ 0)
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
        |sourceQ L sample| ≤ max A 1*r*sourceGammaRadius L sample^5) := by
  have hm : MeasurableSet {sample : SmoothSample 2 L |
      sourceConfluentPinsAt L r sample = p} :=
    measurableSet_eq_fun (sourceConfluentPinsAt_measurable hL r) measurable_const
  have hp : ∀ᵐ sample ∂sourceSmoothKernel hL r p,
      sourceConfluentPinsAt L r sample = p := by
    apply (mem_ae_iff_prob_eq_one hm).2
    exact sourceSmoothKernel_pin_fiber hL r hG p
  filter_upwards [hp] with sample hs
  have hs3 : sourceConfluentPinsAt L r sample 3 = 0 := (congrFun hs 3).trans h3
  have hs4 : sourceConfluentPinsAt L r sample 4 = 0 := (congrFun hs 4).trans h4
  exact ⟨hs, sourceSmoothWeight_curvature_bound hL r hr sample hs3 hs4,
    fun hr1 => sourceSmoothWeight_radius_bound hL r hr hr1 sample hs3 hs4,
    source_positive_weight_curvature_upper hL r hr sample,
    fun A hW hq => source_bad_curvature_slab hL r hr sample hW A hq⟩

/-- Closed actual varying-gap law endpoint: one interval from hL alone,
then every radius, every real height and every real cubic-gap coefficient. -/
theorem sourceGapLaw_curvature_bounds {L : ℝ} (hL : L ≠ 0) :
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
          |sourceQ L sample| ≤ max A 1*r*sourceGammaRadius L sample^5) := by
  obtain ⟨_K,δ,_hK,hδ,hδ1,hbounds⟩ := sourceInverse_target_uniform_bounds hL
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ b k
  have hG := (hbounds r hr hrδ).1
  have hp := sourceSmoothKernel_curvature_bounds_ae hL r hr (sourceGapPins r b k) hG
    (by simp [sourceGapPins]) (by simp [sourceGapPins])
  change ∀ᵐ sample ∂sourceSmoothKernel hL r (sourceGapPins r b k), _
  filter_upwards [hp] with sample hs
  exact ⟨hs.1, hs.2.1, hs.2.2.1 (hrδ.le.trans hδ1), hs.2.2.2⟩

end I4SourceGapPinCurvature
