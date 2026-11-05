import SourceAdaptiveFoldChart
import AdaptiveFoldBoundaryPath

/-! Wide fixed-axis rectangle estimates for the actual source under explicit
sample cutoffs. This module retains the physical q/(6kr) scale. -/

noncomputable section
open Set MeasureTheory
open I4SmoothCarrier I4SourceConfluentPins I4SourceConditionalMajorant
open I4SourcePinCurvatureBounds I4SourcePinPreservingQuartic
open I4SourceAdaptiveFoldChart I4ActualFoldChartJets
open AdaptiveFoldTransverseRidge AdaptiveFoldBoundaryPath
open AdaptiveFoldScalar (J)
open scoped ContDiff Interval Matrix BigOperators
set_option autoImplicit false

namespace I4SourceAdaptiveFoldEstimates

def sourceT {L : ℝ} (k₀ : ℝ) (sample : SmoothSample 2 L) : ℝ :=
  max 1 (1/(6*k₀)) * (8 * sourceGammaRadius L sample)

def sourceKappa {L : ℝ} (r k : ℝ) (sample : SmoothSample 2 L) : ℝ :=
  -sourceQ L sample / (6*k*r)

theorem sourceT_one_le {L : ℝ} (k₀ : ℝ) (sample : SmoothSample 2 L) :
    1 ≤ sourceT k₀ sample := by
  have hΓ := one_le_sourceGammaRadius L sample
  have hD : (1 : ℝ) ≤ max 1 (1/(6*k₀)) := le_max_left _ _
  unfold sourceT
  nlinarith

theorem source_scale_le {L k₀ k : ℝ} (sample : SmoothSample 2 L)
    (hk₀ : 0 < k₀) (hk : k₀ ≤ k) :
    sourceGammaRadius L sample / (6*k) ≤ sourceT k₀ sample := by
  have hkpos : 0 < k := hk₀.trans_le hk
  have hΓ := sourceGammaRadius_nonneg L sample
  have hi : 1/(6*k) ≤ 1/(6*k₀) := by
    apply one_div_le_one_div_of_le (by positivity)
    nlinarith
  have hD := le_max_right (1 : ℝ) (1/(6*k₀))
  have hD0 : 0 ≤ max (1 : ℝ) (1/(6*k₀)) := le_trans zero_le_one (le_max_left _ _)
  unfold sourceT
  rw [div_eq_mul_inv]
  nlinarith

/-- The literal product/Pi inclusion is contractive for their max/sup norms. -/
theorem coord_norm_le (p : ℝ × ℝ) : ‖(![p.1,p.2] : Fin 2 → ℝ)‖ ≤ ‖p‖ := by
  apply (pi_norm_le_iff_of_nonneg (norm_nonneg p)).mpr
  intro i
  fin_cases i
  · simpa using norm_fst_le p
  · simpa using norm_snd_le p

/-- A full operator bound is derived from the actual source operator majorant;
it is never inferred from entrywise coordinate bounds. -/
theorem actual_jet_norm_bound {L r k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hk : 0 < k)
    (n : ℕ) (p : ℝ × ℝ) :
    ‖iteratedFDeriv ℝ n (actualFoldPotential r k sample) p‖ ≤
      r^n / (6*k*r^3) * sourceDerivativeMajorant L n sample := by
  have ha : 0 ≤ (6*k*r^3)⁻¹ * r^n := by positivity
  have hM := sourceDerivativeMajorant_nonneg L n sample
  apply ContinuousMultilinearMap.opNorm_le_bound (by positivity)
  intro v
  have h := pullback_jet (smoothSourceField 2 L sample)
    (smoothSourceField_smooth 2 hL sample) n ((6*k*r^3)⁻¹) r p v
  have hV : actualFoldPotential r k sample =
      fun q => (6*k*r^3)⁻¹ * smoothSourceField 2 L sample (r • ![q.1,q.2]) := by
    ext q
    simp [actualFoldPotential, div_eq_mul_inv, mul_comm]
  rw [hV, h, Real.norm_eq_abs, abs_mul, abs_of_nonneg ha]
  have hs := source_derivative_abs_le hL sample n (r • ![p.1,p.2])
    (fun i => ![(v i).1,(v i).2])
  have hp : (∏ i, ‖(![(v i).1,(v i).2] : Fin 2 → ℝ)‖) ≤ ∏ i, ‖v i‖ :=
    Finset.prod_le_prod (fun _ _ => norm_nonneg _) (fun i _ => coord_norm_le (v i))
  calc
    _ ≤ ((6*k*r^3)⁻¹ * r^n) *
        (sourceDerivativeMajorant L n sample * ∏ i, ‖v i‖) :=
      mul_le_mul_of_nonneg_left (hs.trans (mul_le_mul_of_nonneg_left hp hM)) ha
    _ = _ := by ring

theorem actual_third_norm_bound {L r k₀ k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hk₀ : 0 < k₀) (hk : k₀ ≤ k)
    (p : ℝ × ℝ) :
    ‖iteratedFDeriv ℝ 3 (actualFoldPotential r k sample) p‖ ≤ sourceT k₀ sample := by
  have h := actual_jet_norm_bound hL sample hr (hk₀.trans_le hk) 3 p
  have he : r^3/(6*k*r^3) = 1/(6*k) := by field_simp [hr.ne']
  rw [he] at h
  have hm := sourceDerivativeMajorant_le_radius L sample (3 : Fin 6)
  exact h.trans ((mul_le_mul_of_nonneg_left hm (by positivity)).trans
    (by simpa [div_eq_mul_inv, mul_comm] using source_scale_le sample hk₀ hk))

theorem actual_fourth_norm_bound {L r k₀ k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hk₀ : 0 < k₀) (hk : k₀ ≤ k)
    (p : ℝ × ℝ) :
    ‖iteratedFDeriv ℝ 4 (actualFoldPotential r k sample) p‖ ≤ r * sourceT k₀ sample := by
  have h := actual_jet_norm_bound hL sample hr (hk₀.trans_le hk) 4 p
  have he : r^4/(6*k*r^3) = r/(6*k) := by field_simp [hr.ne']; ring
  rw [he] at h
  have hm := sourceDerivativeMajorant_le_radius L sample (4 : Fin 6)
  calc
    _ ≤ (r/(6*k)) * sourceGammaRadius L sample := h.trans (by gcongr)
    _ = r * (sourceGammaRadius L sample/(6*k)) := by ring
    _ ≤ _ := mul_le_mul_of_nonneg_left (source_scale_le sample hk₀ hk) hr.le

/-- Differentiating a fixed component appends that direction last. -/
theorem component_jet (V : ℝ × ℝ → ℝ) (hV : ContDiff ℝ (⊤ : ℕ∞) V)
    (n : ℕ) (p : ℝ × ℝ) (v : Fin n → ℝ × ℝ) (u : ℝ × ℝ) :
    iteratedFDeriv ℝ n (fun q => fderiv ℝ V q u) p v =
      iteratedFDeriv ℝ (n+1) V p (Fin.snoc v u) := by
  have hd : ContDiff ℝ (⊤ : ℕ∞) (fderiv ℝ V) := hV.fderiv_right (by simp)
  calc
    _ = iteratedFDeriv ℝ n (fderiv ℝ V) p v u :=
      iteratedFDeriv_clm_apply_const_apply hd (by simp)
    _ = _ := by rw [iteratedFDeriv_succ_apply_right, Fin.init_snoc, Fin.snoc_last]

theorem component_smooth (V : ℝ × ℝ → ℝ) (hV : ContDiff ℝ (⊤ : ℕ∞) V)
    (u : ℝ × ℝ) : ContDiff ℝ (⊤ : ℕ∞) (fun q => fderiv ℝ V q u) :=
  (hV.fderiv_right (by simp)).clm_apply contDiff_const

/-- Both ordered mixed entries remain literal, with the fixed component last. -/
theorem component_second (V : ℝ × ℝ → ℝ) (hV : ContDiff ℝ (⊤ : ℕ∞) V)
    (p u v w : ℝ × ℝ) :
    fderiv ℝ (fderiv ℝ (fun q => fderiv ℝ V q w)) p u v =
      iteratedFDeriv ℝ 3 V p ![u,v,w] := by
  rw [← iteratedFDeriv_two_apply (𝕜 := ℝ) _ p ![u,v], component_jet V hV]
  congr 1
  ext i
  fin_cases i <;> rfl

end I4SourceAdaptiveFoldEstimates
