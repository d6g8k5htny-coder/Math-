import SourceAdaptiveFoldChart
import AdaptiveFoldBoundaryPath
import Mathlib.Analysis.Calculus.LocalExtr.Rolle

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

/- Integrated once from /root/fold_two_pin_bounds. Frozen source d85a5ff3e6be506b1762dfe91a6f0a3efc44229311b4f448c0b90e84b0b31038; section 5cd3f6ef111a6045e4e3a8b52af6bec5c5f2616b77131c7e5452560c73a4f87c. Scratch elaboration reused; no helper kernel. -/
namespace I4ActualFoldTwoPin
open AdaptiveFoldScalar

private theorem convex_zero_pin_sign (f : ℝ → ℝ)
    (hf : ConvexOn ℝ J f) (hm : f (-(1 / 2 : ℝ)) = 0)
    (hp : f (1 / 2 : ℝ) = 0) :
    (∀ x ∈ Icc (-(1 / 2 : ℝ)) (1 / 2), f x ≤ 0) ∧
    (∀ x ∈ J, x ≤ -(1 / 2 : ℝ) ∨ (1 / 2 : ℝ) ≤ x → 0 ≤ f x) := by
  have hmJ : -(1 / 2 : ℝ) ∈ J := by norm_num [J]
  have hpJ : (1 / 2 : ℝ) ∈ J := by norm_num [J]
  constructor
  · intro x hx
    have h := hf.le_on_segment hmJ hpJ
      (show x ∈ segment ℝ (-(1 / 2 : ℝ)) (1 / 2) from by
        rw [segment_eq_Icc (by norm_num : -(1 / 2 : ℝ) ≤ 1 / 2)]
        exact hx)
    simpa only [hm, hp, max_self] using h
  · intro x hx hxarm
    rcases hxarm with hleft | hright
    · by_cases heq : x = -(1 / 2 : ℝ)
      · rw [heq, hm]
      have hlt : x < -(1 / 2 : ℝ) := lt_of_le_of_ne hleft heq
      have h := hf.slope_mono_adjacent hx hpJ hlt
        (by norm_num : -(1 / 2 : ℝ) < 1 / 2)
      simp only [hm, hp, sub_self, zero_div, zero_sub] at h
      have hden : 0 < -(1 / 2 : ℝ) - x := by linarith
      have := (div_le_iff₀ hden).mp h
      linarith
    · by_cases heq : x = (1 / 2 : ℝ)
      · rw [heq, hp]
      have hlt : (1 / 2 : ℝ) < x := lt_of_le_of_ne hright (Ne.symm heq)
      have h := hf.slope_mono_adjacent hmJ hx
        (by norm_num : -(1 / 2 : ℝ) < 1 / 2) hlt
      simp only [hm, hp, sub_self, zero_div, sub_zero] at h
      have hden : 0 < x - (1 / 2 : ℝ) := by linarith
      have := (le_div_iff₀ hden).mp h
      linarith

/-- Full jets and two zero pins control the whole normalized interval, including both arms. -/
theorem two_pin_bounds_on_J (g g1 g2 : ℝ → ℝ) (T : ℝ)
    (hT : 0 ≤ T)
    (hg : ∀ x ∈ J, HasDerivAt g (g1 x) x)
    (hg1 : ∀ x ∈ J, HasDerivAt g1 (g2 x) x)
    (hg2 : ∀ x ∈ J, |g2 x| ≤ T)
    (hm : g (-(1 / 2 : ℝ)) = 0) (hp : g (1 / 2 : ℝ) = 0) :
    ∀ x ∈ J, |g x| ≤ (T / 2) * |x ^ 2 - 1 / 4| ∧ |g1 x| ≤ 2 * T := by
  have hconvplus : ConvexOn ℝ J (fun x => T * q x + g x) := by
    apply convexOn_of_hasDerivWithinAt2_nonneg (convex_Icc _ _)
      (f' := fun x => T * x + g1 x) (f'' := fun x => T + g2 x)
    · intro x hx
      exact (((q_hasDerivAt x).const_mul T).add (hg x hx)).continuousAt.continuousWithinAt
    · intro x hx
      exact (((q_hasDerivAt x).const_mul T).add
        (hg x (interior_subset hx))).hasDerivWithinAt
    · intro x hx
      convert (((hasDerivAt_id x).const_mul T).add
        (hg1 x (interior_subset hx))).hasDerivWithinAt using 1 <;> first | rfl | simp
    · intro x hx
      have h := (abs_le.mp (hg2 x (interior_subset hx))).1
      linarith
  have hconvminus : ConvexOn ℝ J (fun x => T * q x - g x) := by
    apply convexOn_of_hasDerivWithinAt2_nonneg (convex_Icc _ _)
      (f' := fun x => T * x - g1 x) (f'' := fun x => T - g2 x)
    · intro x hx
      exact (((q_hasDerivAt x).const_mul T).sub (hg x hx)).continuousAt.continuousWithinAt
    · intro x hx
      exact (((q_hasDerivAt x).const_mul T).sub
        (hg x (interior_subset hx))).hasDerivWithinAt
    · intro x hx
      convert (((hasDerivAt_id x).const_mul T).sub
        (hg1 x (interior_subset hx))).hasDerivWithinAt using 1 <;> first | rfl | simp
    · intro x hx
      have h := (abs_le.mp (hg2 x (interior_subset hx))).2
      linarith
  have hplus := convex_zero_pin_sign (fun x => T * q x + g x) hconvplus
    (by norm_num [q, hm]) (by norm_num [q, hp])
  have hminus := convex_zero_pin_sign (fun x => T * q x - g x) hconvminus
    (by norm_num [q, hm]) (by norm_num [q, hp])
  have hsubJ : Icc (-(1 / 2 : ℝ)) (1 / 2) ⊆ J := by
    intro x hx
    constructor <;> dsimp [J] at * <;> linarith [hx.1, hx.2]
  obtain ⟨ξ, hξ, hgξ⟩ := exists_hasDerivAt_eq_zero
    (by norm_num : -(1 / 2 : ℝ) < 1 / 2)
    (fun x hx => (hg x (hsubJ hx)).continuousAt.continuousWithinAt)
    (by rw [hm, hp]) (fun x hx => hg x (hsubJ ⟨hx.1.le, hx.2.le⟩))
  have hξJ : ξ ∈ J := hsubJ ⟨hξ.1.le, hξ.2.le⟩
  intro x hx
  constructor
  · by_cases hleft : x < -(1 / 2 : ℝ)
    · have ha := hplus.2 x hx (Or.inl hleft.le)
      have hb := hminus.2 x hx (Or.inl hleft.le)
      have hsq : 0 ≤ x ^ 2 - (1 / 4 : ℝ) := by nlinarith [sq_nonneg (x + 1 / 2)]
      rw [abs_of_nonneg hsq]
      apply abs_le.mpr
      dsimp [q] at ha hb
      constructor <;> nlinarith
    · by_cases hright : (1 / 2 : ℝ) < x
      · have ha := hplus.2 x hx (Or.inr hright.le)
        have hb := hminus.2 x hx (Or.inr hright.le)
        have hsq : 0 ≤ x ^ 2 - (1 / 4 : ℝ) := by nlinarith [sq_nonneg (x - 1 / 2)]
        rw [abs_of_nonneg hsq]
        apply abs_le.mpr
        dsimp [q] at ha hb
        constructor <;> nlinarith
      · have hmid : x ∈ Icc (-(1 / 2 : ℝ)) (1 / 2) := ⟨le_of_not_gt hleft, le_of_not_gt hright⟩
        have ha := hplus.1 x hmid
        have hb := hminus.1 x hmid
        have hsq : x ^ 2 - (1 / 4 : ℝ) ≤ 0 := by
          have := mul_nonneg (show 0 ≤ x + 1 / 2 by linarith [hmid.1])
            (show 0 ≤ 1 / 2 - x by linarith [hmid.2])
          nlinarith
        rw [abs_of_nonpos hsq]
        apply abs_le.mpr
        dsimp [q] at ha hb
        constructor <;> nlinarith
  · have hmv := Convex.norm_image_sub_le_of_norm_deriv_le
      (f := g1) (s := J) (C := T)
      (fun y hy => (hg1 y hy).differentiableAt)
      (fun y hy => by rw [(hg1 y hy).deriv, Real.norm_eq_abs]; exact hg2 y hy)
      (convex_Icc _ _) hξJ hx
    rw [hgξ, sub_zero, Real.norm_eq_abs, Real.norm_eq_abs] at hmv
    have hdist : |x - ξ| ≤ 2 := by
      apply abs_le.mpr
      dsimp [J] at hx
      constructor <;> linarith [hx.1, hx.2, hξ.1, hξ.2]
    exact hmv.trans (by nlinarith)

/-- The quadratic envelope is at most T on the entire interval J. -/
theorem two_pin_abs_le_on_J (g g1 g2 : ℝ → ℝ) (T : ℝ)
    (hT : 0 ≤ T)
    (hg : ∀ x ∈ J, HasDerivAt g (g1 x) x)
    (hg1 : ∀ x ∈ J, HasDerivAt g1 (g2 x) x)
    (hg2 : ∀ x ∈ J, |g2 x| ≤ T)
    (hm : g (-(1 / 2 : ℝ)) = 0) (hp : g (1 / 2 : ℝ) = 0) :
    ∀ x ∈ J, |g x| ≤ T ∧ |g1 x| ≤ 2 * T := by
  intro x hx
  have h := two_pin_bounds_on_J g g1 g2 T hT hg hg1 hg2 hm hp x hx
  refine ⟨h.1.trans ?_, h.2⟩
  have hx' := hx
  dsimp [J] at hx'
  have hsq : x ^ 2 ≤ (9 / 4 : ℝ) := by
    have := mul_nonneg (show 0 ≤ x + 3 / 2 by linarith [hx'.1])
      (show 0 ≤ 3 / 2 - x by linarith [hx'.2])
    nlinarith
  have habs : |x ^ 2 - (1 / 4 : ℝ)| ≤ 2 := by
    apply abs_le.mpr
    constructor <;> nlinarith [sq_nonneg x]
  nlinarith

end I4ActualFoldTwoPin

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
  calc
    _ ≤ max 1 (1/(6*k₀)) * sourceGammaRadius L sample := by
      simpa [div_eq_mul_inv, mul_comm] using
        mul_le_mul_of_nonneg_left (hi.trans hD) hΓ
    _ ≤ _ := by unfold sourceT; nlinarith

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
    Finset.prod_le_prod₀ (fun _ _ => norm_nonneg _) (fun i _ => coord_norm_le (v i))
  calc
    _ ≤ ((6*k*r^3)⁻¹ * r^n) *
        (sourceDerivativeMajorant L n sample * ∏ i, ‖v i‖) :=
      mul_le_mul_of_nonneg_left (hs.trans (mul_le_mul_of_nonneg_left hp hM)) ha
    _ = _ := by ring

theorem actual_third_norm_bound {L r k₀ k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hk₀ : 0 < k₀) (hk : k₀ ≤ k)
    (p : ℝ × ℝ) :
    ‖iteratedFDeriv ℝ 3 (actualFoldPotential r k sample) p‖ ≤ sourceT k₀ sample := by
  have hkpos : 0 < k := hk₀.trans_le hk
  have h := actual_jet_norm_bound hL sample hr hkpos 3 p
  have he : r^3/(6*k*r^3) = 1/(6*k) := by field_simp [hr.ne']
  rw [he] at h
  have hm := sourceDerivativeMajorant_le_radius L sample (3 : Fin 6)
  exact h.trans ((mul_le_mul_of_nonneg_left hm (by positivity)).trans
    (by simpa [div_eq_mul_inv, mul_comm] using source_scale_le sample hk₀ hk))

theorem actual_fourth_norm_bound {L r k₀ k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hk₀ : 0 < k₀) (hk : k₀ ≤ k)
    (p : ℝ × ℝ) :
    ‖iteratedFDeriv ℝ 4 (actualFoldPotential r k sample) p‖ ≤ r * sourceT k₀ sample := by
  have hkpos : 0 < k := hk₀.trans_le hk
  have h := actual_jet_norm_bound hL sample hr hkpos 4 p
  have he : r^4/(6*k*r^3) = r/(6*k) := by field_simp [hr.ne']
  rw [he] at h
  have hm := sourceDerivativeMajorant_le_radius L sample (4 : Fin 6)
  calc
    _ ≤ (r/(6*k)) * sourceGammaRadius L sample := h.trans (mul_le_mul_of_nonneg_left hm (by positivity))
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
  have hd : Fin.snoc ![u,v] w = ![u,v,w] := by
    ext i
    fin_cases i <;> rfl
  have h := component_jet V hV 2 p ![u,v] w
  rw [hd] at h
  simpa only [iteratedFDeriv_two_apply, Matrix.cons_val_zero, Matrix.cons_val_one] using h

end I4SourceAdaptiveFoldEstimates
