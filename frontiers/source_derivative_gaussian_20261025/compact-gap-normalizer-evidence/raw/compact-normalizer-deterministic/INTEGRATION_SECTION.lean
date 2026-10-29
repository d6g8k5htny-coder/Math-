open I4Foundation I4Source I4SmoothCarrier I4Smooth I4SourceConfluentPins
open I4SourceEndpointRegression I4SourceEndpointEstimates I4SourceSmoothConditional
open I4SourceSmoothPalm I4SourceConditionalMajorant I4SourcePinCurvatureBounds
open I4SourceCompactTargetMoments I4SourceGapPinCurvature I4PeanoErrorBounds
open I4ConfluentIntegralIdentities I4SourceConfluentLimits ResearchFormalCoreR1
open MeasureTheory ProbabilityTheory Set Matrix
open scoped Interval Topology

set_option autoImplicit false

namespace SourceCompactGapNormalizer

/-- Translate the established cubic error theorem to any literal cubic target. -/
theorem cubic_pin_pointwise_error_target (g : ℝ → ℝ) (hgc : Continuous g)
    (C r c : ℝ) (hC : 0 ≤ C) (hr : 0 ≤ r)
    (hlip : ∀ x y : ℝ, |g x - g y| ≤ C * |x-y|)
    (hpin : 6 * (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic t * g (r*t)) = c)
    (u : ℝ) (hu : u ∈ Icc (-1/2 : ℝ) (1/2 : ℝ)) :
    |g (r*u) - c| ≤ r*C := by
  let f : ℝ → ℝ := fun x => g x-c+2
  have hfc : Continuous f := (hgc.sub continuous_const).add continuous_const
  have hfl (x y : ℝ) : |f x-f y| ≤ C*|x-y| := by
    simpa only [f, show g x-c+2-(g y-c+2) = g x-g y by ring] using hlip x y
  have hmass : (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic t) = 1/6 := by
    linarith [peano_kernel_masses.2.2.2]
  have hcK : Continuous peanoCubic := by unfold peanoCubic; fun_prop
  have hiG : IntervalIntegrable (fun t => peanoCubic t*g (r*t)) volume
      (-1/2 : ℝ) (1/2 : ℝ) :=
    (hcK.mul (hgc.comp (continuous_const.mul continuous_id))).intervalIntegrable _ _
  have hiC : IntervalIntegrable (fun t => peanoCubic t*c) volume
      (-1/2 : ℝ) (1/2 : ℝ) := (hcK.mul continuous_const).intervalIntegrable _ _
  have hi2 : IntervalIntegrable (fun t => peanoCubic t*2) volume
      (-1/2 : ℝ) (1/2 : ℝ) := (hcK.mul continuous_const).intervalIntegrable _ _
  have hfp : 6*(∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic t*f (r*t)) = 2 := by
    simp_rw [f, mul_add, mul_sub]
    rw [intervalIntegral.integral_add (hiG.sub hiC) hi2,
      intervalIntegral.integral_sub hiG hiC,
      intervalIntegral.integral_mul_const, intervalIntegral.integral_mul_const, hmass]
    linarith
  have h := cubic_pin_pointwise_error f hfc C r hC hr hfl hfp u hu
  simpa only [f, show g (r*u)-c+2-2 = g (r*u)-c by ring] using h

/-- Literal axial centers for arbitrary cubic-gap pin 12*k. -/
theorem source_normalized_gap_axial_errors {L : ℝ} (hL : L ≠ 0)
    (r k : ℝ) (hr : 0 < r) (sample : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r sample 3 = 0)
    (h4 : sourceConfluentPinsAt L r sample 4 = 0)
    (h5 : sourceConfluentPinsAt L r sample 5 = 12*k) :
    |sourceNormalizedEndpoints L r sample 0 + 6*k| ≤ r*sourceGammaRadius L sample ∧
    |sourceNormalizedEndpoints L r sample 1 - 6*k| ≤ r*sourceGammaRadius L sample := by
  have hΓ4 := sourceDerivativeMajorant_nonneg L 4 sample
  have hpin := pin5_integral (sourceF L sample) (sourceF_C3 hL sample) r hr.ne'
  rw [← source_pin5_eq hL r sample,h5] at hpin
  have hf := cubic_pin_pointwise_error_target _ (sourceF_third_continuous hL sample)
    _ r (12*k) hΓ4 hr.le (sourceF_third_lipschitz hL sample) hpin.symm
  have hleft := left_weighted_error _ (sourceF_third_continuous hL sample) r (12*k)
    (r*sourceDerivativeMajorant L 4 sample) hf
  have hright := right_weighted_error _ (sourceF_third_continuous hL sample) r (12*k)
    (r*sourceDerivativeMajorant L 4 sample) hf
  have hbound : r*sourceDerivativeMajorant L 4 sample/2 ≤ r*sourceGammaRadius L sample := by
    have hm : r*sourceDerivativeMajorant L 4 sample ≤ r*sourceGammaRadius L sample :=
      mul_le_mul_of_nonneg_left (sourceDerivativeMajorant_le_radius L sample 4) hr.le
    linarith [mul_nonneg hr.le hΓ4]
  rw [source_normalized_peano hL r hr.ne' sample h3 h4]
  constructor
  · change |-(∫ u in (-1/2:ℝ)..(1/2:ℝ),
        peanoLeft u * iteratedDeriv 3 (sourceF L sample) (r*u)) + 6*k| ≤ _
    have heq : (12*k)/2 = 6*k := by ring
    rw [heq] at hleft
    simpa only [show -(∫ u in (-1/2:ℝ)..(1/2:ℝ),
      peanoLeft u * iteratedDeriv 3 (sourceF L sample) (r*u)) + 6*k =
      -((∫ u in (-1/2:ℝ)..(1/2:ℝ),
        peanoLeft u * iteratedDeriv 3 (sourceF L sample) (r*u))-6*k) by ring,
      abs_neg] using hleft.trans hbound
  · change |(∫ u in (-1/2:ℝ)..(1/2:ℝ),
        peanoRight u * iteratedDeriv 3 (sourceF L sample) (r*u)) - 6*k| ≤ _
    have heq : (12*k)/2 = 6*k := by ring
    rw [heq] at hright
    exact hright.trans hbound

/-- Finite physical-Hessian arithmetic retaining the literal strict type branch. -/
theorem endpointWeight_gap_floor (r k k0 A q : ℝ) (v : Fin 6 → ℝ)
    (hr : 0 < r) (hk0 : 0 < k0) (hk : k0 ≤ k) (hA : 1 ≤ A)
    (hrδ : r < min 1 (min (1/(2*A)) (k0/(2*A^2))))
    (hq : q ∈ Icc (-2 : ℝ) (-1 : ℝ))
    (h0 : |v 0+6*k| ≤ r*A) (h1 : |v 1-6*k| ≤ r*A)
    (h2 : |v 2| ≤ A) (h3 : |v 3| ≤ A)
    (h4 : |v 4-q| ≤ r*A) (h5 : |v 5-q| ≤ r*A) :
    (dm2Negative (egm_HM r (sourcePhysicalCoordinates v)) ∧
      (egm_HS r (sourcePhysicalCoordinates v)).det < 0) ∧
    k0^2*r^2 ≤ sourceEndpointWeight r v := by
  have hA0 : 0 < A := by linarith
  have hrA : r*A < 1/2 := by
    have h := (lt_div_iff₀ (by positivity : 0 < 2*A)).mp
      (lt_of_lt_of_le hrδ (min_le_of_right_le (min_le_left _ _)))
    nlinarith
  have hrAA : r*A^2 < k0/2 := by
    have h := (lt_div_iff₀ (by positivity : 0 < 2*A^2)).mp
      (lt_of_lt_of_le hrδ (min_le_of_right_le (min_le_right _ _)))
    nlinarith
  have hAA : A ≤ A^2 := by nlinarith
  have hrAk : r*A < k0/2 :=
    (mul_le_mul_of_nonneg_left hAA hr.le).trans_lt hrAA
  have hv0 : v 0 ≤ -3*k0 := by
    have h := (abs_le.mp h0).2
    linarith
  have hv1 : 3*k0 ≤ v 1 := by
    have h := (abs_le.mp h1).1
    linarith
  have hv4 : v 4 ≤ -1/2 := by
    have h := (abs_le.mp h4).2
    linarith [hq.2]
  have hv5 : v 5 ≤ -1/2 := by
    have h := (abs_le.mp h5).2
    linarith [hq.2]
  have hb2 : (v 2)^2 ≤ A^2 := by
    simpa only [sq_abs] using pow_le_pow_left₀ (abs_nonneg (v 2)) h2 2
  have hb3 : (v 3)^2 ≤ A^2 := by
    simpa only [sq_abs] using pow_le_pow_left₀ (abs_nonneg (v 3)) h3 2
  have hMprod : 3*k0/2 ≤ v 0*v 4 := by
    calc
      3*k0/2 = (-3*k0)*(-1/2) := by ring
      _ ≤ (-3*k0)*v 4 := mul_le_mul_of_nonpos_left hv4 (by linarith)
      _ ≤ v 0*v 4 := mul_le_mul_of_nonpos_right hv0 (by linarith)
  have hSprod : v 1*v 5 ≤ -3*k0/2 := by
    calc
      _ ≤ (3*k0)*v 5 := mul_le_mul_of_nonpos_right hv1 (by linarith)
      _ ≤ (3*k0)*(-1/2) := mul_le_mul_of_nonneg_left hv5 (by positivity)
      _ = _ := by ring
  have hDM : k0 ≤ v 0*v 4-r*(v 2)^2 := by
    have h := mul_le_mul_of_nonneg_left hb2 hr.le
    linarith
  have hDS : v 1*v 5-r*(v 3)^2 ≤ -3*k0/2 := by
    linarith [mul_nonneg hr.le (sq_nonneg (v 3))]
  have hdetM : (egm_HM r (sourcePhysicalCoordinates v)).det =
      r*(v 0*v 4-r*(v 2)^2) := by
    simp [egm_HM,sourcePhysicalCoordinates,Matrix.det_fin_two]
    ring
  have hdetS : (egm_HS r (sourcePhysicalCoordinates v)).det =
      r*(v 1*v 5-r*(v 3)^2) := by
    simp [egm_HS,sourcePhysicalCoordinates,Matrix.det_fin_two]
    ring
  have htype : dm2Negative (egm_HM r (sourcePhysicalCoordinates v)) ∧
      (egm_HS r (sourcePhysicalCoordinates v)).det < 0 := by
    constructor
    · change dm2Negative !![r*v 0,r*v 2;r*v 2,v 4]
      rw [dm2_negative_iff]
      constructor
      · exact mul_neg_of_pos_of_neg hr (by linarith)
      · have hp : 0 < r*(v 0*v 4-r*(v 2)^2) := mul_pos hr (lt_of_lt_of_le hk0 hDM)
        nlinarith only [hp]
    · rw [hdetS]
      exact mul_neg_of_pos_of_neg hr (by linarith)
  refine ⟨htype,?_⟩
  rw [sourceEndpointWeight,egm_weight,ite_eq_left htype,hdetM,hdetS]
  have hDS' : k0 ≤ -(v 1*v 5-r*(v 3)^2) := by linarith
  have hp := mul_le_mul hDM hDS' hk0.le (lt_of_lt_of_le hk0 hDM).le
  have hsign : r*(v 0*v 4-r*(v 2)^2)*(r*(v 1*v 5-r*(v 3)^2)) ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos
      (mul_nonneg hr.le (lt_of_lt_of_le hk0 hDM).le)
      (mul_nonpos_of_nonneg_of_nonpos hr.le (by linarith))
  rw [abs_of_nonpos hsign]
  have hmul := mul_le_mul_of_nonneg_left hp (sq_nonneg r)
  nlinarith only [hmul]

/-- Actual physical weight floor on the bounded-radius, negative-q event.
Only Hessian typing is asserted; endpoint criticality needs the gradient pins. -/
theorem sourceSmoothWeight_gap_floor {L : ℝ} (hL : L ≠ 0)
    (r k k0 A : ℝ) (hr : 0 < r) (hk0 : 0 < k0) (hk : k0 ≤ k) (hA : 1 ≤ A)
    (hrδ : r < min 1 (min (1/(2*A)) (k0/(2*A^2))))
    (sample : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r sample 3 = 0)
    (h4 : sourceConfluentPinsAt L r sample 4 = 0)
    (h5 : sourceConfluentPinsAt L r sample 5 = 12*k)
    (hq : sourceQ L sample ∈ Icc (-2 : ℝ) (-1 : ℝ))
    (hΓ : sourceGammaRadius L sample ≤ A) :
    sourceSmoothTyped L r sample ∧ k0^2*r^2 ≤ sourceSmoothWeight L r sample := by
  obtain ⟨ha0,ha1⟩ := source_normalized_gap_axial_errors hL r k hr sample h3 h4 h5
  have hcross := source_normalized_first_four_bound hL r hr.ne' sample h3 h4
  obtain ⟨ht4,ht5⟩ := source_normalized_transverse_errors hL r hr.le sample
  have hΓ3 := (sourceDerivativeMajorant_le_radius L sample 3).trans hΓ
  have hrΓ := mul_le_mul_of_nonneg_left hΓ hr.le
  have hrΓ3 := mul_le_mul_of_nonneg_left hΓ3 hr.le
  obtain ⟨ht,hW⟩ := endpointWeight_gap_floor r k k0 A (sourceQ L sample)
    (sourceNormalizedEndpoints L r sample) hr hk0 hk hA hrδ hq
    (ha0.trans hrΓ) (ha1.trans hrΓ) ((hcross 2).trans hΓ) ((hcross 3).trans hΓ)
    (ht4.trans hrΓ3) (ht5.trans hrΓ3)
  constructor
  · unfold sourceSmoothTyped
    rw [sourceRawHM_eq_normalized L r hr.ne' sample,
      sourceRawHS_eq_normalized L r hr.ne' sample]
    exact ht
  · rw [sourceSmoothWeight_eq L r hr.ne' sample]
    exact hW

end SourceCompactGapNormalizer
