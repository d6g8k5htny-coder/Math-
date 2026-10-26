import SourcePinCurvatureBounds

noncomputable section
open I4SmoothCarrier I4SourceConfluentPins I4SourceEndpointRegression
open I4SourcePinCurvatureBounds I4SourceConditionalMajorant I4ConfluentIntegralIdentities
open I4SourceConfluentLimits I4PeanoErrorBounds MeasureTheory Set
open scoped Interval BigOperators
set_option autoImplicit false

namespace I4SourcePinCurvatureBounds

theorem sourceQCurve_zero (L : ℝ) (ω : SmoothSample 2 L) :
    sourceQCurve L ω 0 = sourceQ L ω := by
  have h0 : (![0,0] : Fin 2 → ℝ) = 0 := by ext i; fin_cases i <;> rfl
  simp only [sourceQCurve,sourceQ,h0]

theorem sourceQ_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    |sourceQ L ω| ≤ sourceDerivativeMajorant L 2 ω :=
  by simpa only [sourceQCurve_zero] using sourceQCurve_abs_le hL ω 0

theorem sourceA_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    |sourceA L ω| ≤ sourceDerivativeMajorant L 3 ω := by
  rw [← sourceH_second_zero hL ω]
  exact sourceH_second_abs_le hL ω 0

/-- Six literal endpoint errors on the actual confluent pin fiber. -/
theorem source_normalized_endpoint_errors {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (ω : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0)
    (h5 : sourceConfluentPinsAt L r ω 5 = 2) :
    |sourceNormalizedEndpoints L r ω 0 + 1| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |sourceNormalizedEndpoints L r ω 1 - 1| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |sourceNormalizedEndpoints L r ω 2 + sourceA L ω/2| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |sourceNormalizedEndpoints L r ω 3 - sourceA L ω/2| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |sourceNormalizedEndpoints L r ω 4 - sourceQ L ω| ≤ r*sourceDerivativeMajorant L 3 ω ∧
    |sourceNormalizedEndpoints L r ω 5 - sourceQ L ω| ≤ r*sourceDerivativeMajorant L 3 ω := by
  have hΓ4 := sourceDerivativeMajorant_nonneg L 4 ω
  have hΓ3 := sourceDerivativeMajorant_nonneg L 3 ω
  have hhalf : r*sourceDerivativeMajorant L 4 ω/2 ≤ r*sourceDerivativeMajorant L 4 ω :=
    by nlinarith [mul_nonneg hr.le hΓ4]
  have hpin := pin5_integral (sourceF L ω) (sourceF_C3 hL ω) r hr.ne'
  rw [← source_pin5_eq hL r ω,h5] at hpin
  have hp : 6*(∫ t in (-1/2:ℝ)..(1/2:ℝ),
      peanoCubic t * iteratedDeriv 3 (sourceF L ω) (r*t)) = 2 := hpin.symm
  have hf := cubic_pin_pointwise_error _ (sourceF_third_continuous hL ω)
    _ r hΓ4 hr.le (sourceF_third_lipschitz hL ω) hp
  have hFleft := left_weighted_error _ (sourceF_third_continuous hL ω) r 2
    (r*sourceDerivativeMajorant L 4 ω) hf
  have hFright := right_weighted_error _ (sourceF_third_continuous hL ω) r 2
    (r*sourceDerivativeMajorant L 4 ω) hf
  have hh (t : ℝ) (ht : t ∈ Icc (-1/2:ℝ) (1/2:ℝ)) :
      |iteratedDeriv 2 (sourceH L ω) (r*t)-sourceA L ω| ≤
        r*sourceDerivativeMajorant L 4 ω := by
    have h := scaled_lipschitz_center_error _ _ r hΓ4 hr.le
      (sourceH_second_lipschitz hL ω) t ht
    rw [sourceH_second_zero hL ω] at h
    exact h.trans (by nlinarith [mul_nonneg hr.le hΓ4])
  have hHleft := left_weighted_error _ (sourceH_second_continuous hL ω) r (sourceA L ω)
    (r*sourceDerivativeMajorant L 4 ω) hh
  have hHright := right_weighted_error _ (sourceH_second_continuous hL ω) r (sourceA L ω)
    (r*sourceDerivativeMajorant L 4 ω) hh
  have hq (t : ℝ) (ht : t ∈ Icc (-1/2:ℝ) (1/2:ℝ)) :
      |sourceQCurve L ω (r*t)-sourceQ L ω| ≤ r*sourceDerivativeMajorant L 3 ω := by
    have h := scaled_lipschitz_center_error _ _ r hΓ3 hr.le
      (sourceQCurve_lipschitz hL ω) t ht
    rw [sourceQCurve_zero] at h
    exact h.trans (by nlinarith [mul_nonneg hr.le hΓ3])
  have hQM : |sourceQCurve L ω (-r/2)-sourceQ L ω| ≤ r*sourceDerivativeMajorant L 3 ω := by
    have h := hq (-1/2) (by constructor <;> norm_num)
    have he : r*(-1/2) = -r/2 := by ring
    rw [he] at h
    exact h
  have hQS : |sourceQCurve L ω (r/2)-sourceQ L ω| ≤ r*sourceDerivativeMajorant L 3 ω := by
    have h := hq (1/2) (by constructor <;> norm_num)
    have he : r*(1/2) = r/2 := by ring
    rw [he] at h
    exact h
  rw [source_normalized_peano hL r hr.ne' ω h3 h4]
  change |-(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u * iteratedDeriv 3 (sourceF L ω) (r*u))+1| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoRight u * iteratedDeriv 3 (sourceF L ω) (r*u))-1| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |-(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u * iteratedDeriv 2 (sourceH L ω) (r*u))+sourceA L ω/2| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoRight u * iteratedDeriv 2 (sourceH L ω) (r*u))-sourceA L ω/2| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |sourceQCurve L ω (-r/2)-sourceQ L ω| ≤ r*sourceDerivativeMajorant L 3 ω ∧
    |sourceQCurve L ω (r/2)-sourceQ L ω| ≤ r*sourceDerivativeMajorant L 3 ω
  refine ⟨?_,?_,?_,?_,hQM,hQS⟩
  · have he : |-(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u *
        iteratedDeriv 3 (sourceF L ω) (r*u))+1| =
        |(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u *
        iteratedDeriv 3 (sourceF L ω) (r*u))-2/2| := by
      rw [show (2:ℝ)/2=1 by norm_num,← abs_neg]; congr 1; ring
    rw [he]
    exact hFleft.trans hhalf
  · rw [show (2:ℝ)/2=1 by norm_num] at hFright
    exact hFright.trans hhalf
  · have he : |-(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u *
        iteratedDeriv 2 (sourceH L ω) (r*u))+sourceA L ω/2| =
        |(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u *
        iteratedDeriv 2 (sourceH L ω) (r*u))-sourceA L ω/2| := by
      rw [← abs_neg]; congr 1; ring
    rw [he]
    exact hHleft.trans hhalf
  · exact hHright.trans hhalf

theorem sourceGammaRadius_ge_third_fourth (L : ℝ) (ω : SmoothSample 2 L) :
    1+sourceDerivativeMajorant L 3 ω+sourceDerivativeMajorant L 4 ω ≤ sourceGammaRadius L ω := by
  have h0 := sourceDerivativeMajorant_nonneg L 0 ω
  have h1 := sourceDerivativeMajorant_nonneg L 1 ω
  have h2 := sourceDerivativeMajorant_nonneg L 2 ω
  have h5 := sourceDerivativeMajorant_nonneg L 5 ω
  unfold sourceGammaRadius
  simp only [Fin.sum_univ_succ]
  change 1+sourceDerivativeMajorant L 3 ω+sourceDerivativeMajorant L 4 ω ≤
    1+(sourceDerivativeMajorant L 0 ω+(sourceDerivativeMajorant L 1 ω+
      (sourceDerivativeMajorant L 2 ω+(sourceDerivativeMajorant L 3 ω+
        (sourceDerivativeMajorant L 4 ω+(sourceDerivativeMajorant L 5 ω+0))))))
  linarith

theorem source_normalized_endpoint_first_four_bounds {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1) (ω : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0)
    (h5 : sourceConfluentPinsAt L r ω 5 = 2) :
    ∀ i : Fin 4, |sourceNormalizedEndpoints L r ω i.castSucc.castSucc| ≤ sourceGammaRadius L ω := by
  obtain ⟨h0,h1,h2,h3',_,_⟩ := source_normalized_endpoint_errors hL r hr ω h3 h4 h5
  have hΓ4 := sourceDerivativeMajorant_nonneg L 4 ω
  have hΓ3 := sourceDerivativeMajorant_nonneg L 3 ω
  have hA := sourceA_abs_le hL ω
  have hR := sourceGammaRadius_ge_third_fourth L ω
  have he : r*sourceDerivativeMajorant L 4 ω ≤ sourceDerivativeMajorant L 4 ω :=
    mul_le_of_le_one_left hΓ4 hr1
  intro i
  fin_cases i
  · have hh := abs_add_le (sourceNormalizedEndpoints L r ω 0+1) (-1)
    norm_num at hh
    have heq : sourceNormalizedEndpoints L r ω 0+1+-1=sourceNormalizedEndpoints L r ω 0 := by ring
    exact hh.trans (by linarith)
  · have hh := abs_add_le (sourceNormalizedEndpoints L r ω 1-1) 1
    norm_num at hh
    have heq : sourceNormalizedEndpoints L r ω 1-1+1=sourceNormalizedEndpoints L r ω 1 := by ring
    exact hh.trans (by linarith)
  · have hh := abs_add_le (sourceNormalizedEndpoints L r ω 2+sourceA L ω/2) (-sourceA L ω/2)
    have heq : sourceNormalizedEndpoints L r ω 2+sourceA L ω/2+-sourceA L ω/2=
        sourceNormalizedEndpoints L r ω 2 := by ring
    rw [heq,abs_div,abs_neg] at hh
    norm_num at hh
    exact hh.trans (by linarith)
  · have hh := abs_add_le (sourceNormalizedEndpoints L r ω 3-sourceA L ω/2) (sourceA L ω/2)
    have heq : sourceNormalizedEndpoints L r ω 3-sourceA L ω/2+sourceA L ω/2=
        sourceNormalizedEndpoints L r ω 3 := by ring
    rw [heq,abs_div] at hh
    norm_num at hh
    exact hh.trans (by linarith)

end I4SourcePinCurvatureBounds
