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
open I4SourceConfluentLimits I4PeanoErrorBounds
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

/- Integrated once from /root/fold_numeric_budget. Frozen source 123bf1063c4d4360b656f68753caa75d3d58de1d143735344805037228489bfe; section 1fd2fb6af035481a5ae460da928bf9efa2dd029fe376bfe87e143af183570c71. Scratch elaboration reused; no helper kernel. -/
namespace I4ActualFoldNumeric
open AdaptiveFoldBoundaryPath

structure NumericalBudget (T r κ : ℝ) : Prop where
  kappa_pos : 0 < κ
  c_pos : 0 < κ / 2
  radius_pos : 0 < 4 / Real.sqrt κ
  radius_le : 4 / Real.sqrt κ ≤ 1 / 8
  twice_T_le : 2 * T ≤ κ / 2
  strict_center : T < 2 * Real.sqrt κ
  rT_le : r * T ≤ 1 / 100
  slope_le : 6 * T / κ ≤ 1
  error_le : profileError (κ / 2) (3 * T) T ≤ 72 * T ^ 2 / κ
  curvature : 1 + profileError (κ / 2) (3 * T) T ≤ 2 - 3 * r * T
  capture : T / (κ / 2) ≤ 4 / Real.sqrt κ
  drop : 1 ≤ ((κ / 2) / 2) * (4 / Real.sqrt κ - T / (κ / 2)) ^ 2
  radius_curvature_eq : (κ / 2) * (4 / Real.sqrt κ) = 2 * Real.sqrt κ

theorem numerical_budget {T r κ : ℝ}
    (hT : 1 ≤ T) (hr : 0 < r)
    (hrT : r * T ^ 5 ≤ 1 / 100) (hκ : 1024 * T ^ 5 ≤ κ) :
    NumericalBudget T r κ := by
  have hT0 : 0 ≤ T := by linarith
  have hTpos : 0 < T := by linarith
  have hT5 : 1 ≤ T ^ 5 := one_le_pow₀ hT
  have hT15 : T ≤ T ^ 5 := by
    simpa using pow_le_pow_right₀ hT (show 1 ≤ 5 by norm_num)
  have hT25 : T ^ 2 ≤ T ^ 5 := pow_le_pow_right₀ hT (by norm_num)
  have hk : 0 < κ := by linarith
  have hc : 0 < κ / 2 := by positivity
  have hsqrt : 0 < Real.sqrt κ := Real.sqrt_pos.mpr hk
  have hsqrt0 : 0 ≤ Real.sqrt κ := le_of_lt hsqrt
  have hsqrt_sq : Real.sqrt κ ^ 2 = κ := Real.sq_sqrt (le_of_lt hk)
  have hroot : 32 * T ≤ Real.sqrt κ := by
    apply (sq_le_sq₀ (by positivity) hsqrt0).mp
    nlinarith
  have hTroot : T ≤ Real.sqrt κ := by linarith
  have hradius : 4 / Real.sqrt κ ≤ 1 / 8 := by
    apply (div_le_iff₀ hsqrt).mpr
    linarith
  have htwice : 2 * T ≤ κ / 2 := by nlinarith
  have hcenter : T < 2 * Real.sqrt κ := by linarith
  have hrT1 : r * T ≤ 1 / 100 := by
    exact (mul_le_mul_of_nonneg_left hT15 (le_of_lt hr)).trans hrT
  let s := 6 * T / κ
  have hs0 : 0 ≤ s := by dsimp [s]; positivity
  have hs1 : s ≤ 1 := by
    dsimp [s]
    apply (div_le_iff₀ hk).mpr
    nlinarith
  have hfirst : T * (2 * s + s ^ 2) ≤ 18 * T ^ 2 / κ := by
    calc
      T * (2 * s + s ^ 2) ≤ T * (3 * s) := by
        apply mul_le_mul_of_nonneg_left _ hT0
        nlinarith
      _ = 18 * T ^ 2 / κ := by dsimp [s]; ring
  have hsecond : (6 * T ^ 2 / κ) * (1 + s) ^ 2 ≤ 24 * T ^ 2 / κ := by
    calc
      (6 * T ^ 2 / κ) * (1 + s) ^ 2 ≤ (6 * T ^ 2 / κ) * 4 := by
        apply mul_le_mul_of_nonneg_left _ (by positivity)
        nlinarith
      _ = 24 * T ^ 2 / κ := by ring
  have herr_eq : profileError (κ / 2) (3 * T) T =
      T * (2 * s + s ^ 2) + (6 * T ^ 2 / κ) * (1 + s) ^ 2 := by
    dsimp [profileError, accelerationRadius, s]
    field_simp [hk.ne']
    ring
  have herr42 : profileError (κ / 2) (3 * T) T ≤ 42 * T ^ 2 / κ := by
    rw [herr_eq]
    calc
      _ ≤ 18 * T ^ 2 / κ + 24 * T ^ 2 / κ := add_le_add hfirst hsecond
      _ = 42 * T ^ 2 / κ := by ring
  have herr72 : profileError (κ / 2) (3 * T) T ≤ 72 * T ^ 2 / κ := by
    exact herr42.trans (div_le_div_of_nonneg_right (by nlinarith [sq_nonneg T])
      (le_of_lt hk))
  have hquotient : T ^ 2 / κ ≤ 1 / 1024 := by
    apply (div_le_iff₀ hk).mpr
    nlinarith
  have hcurv : 1 + profileError (κ / 2) (3 * T) T ≤ 2 - 3 * r * T := by
    have heq : 42 * T ^ 2 / κ = 42 * (T ^ 2 / κ) := by ring
    rw [heq] at herr42
    nlinarith
  have hcap2 : T / (κ / 2) ≤ 2 / Real.sqrt κ := by
    apply (div_le_div_iff₀ hc hsqrt).mpr
    have hprod := mul_le_mul_of_nonneg_right hTroot hsqrt0
    nlinarith
  have hcap : T / (κ / 2) ≤ 4 / Real.sqrt κ := by
    apply hcap2.trans
    exact div_le_div_of_nonneg_right (by norm_num) hsqrt0
  have hdropbase : 2 / Real.sqrt κ ≤ 4 / Real.sqrt κ - T / (κ / 2) := by
    have hsplit : 4 / Real.sqrt κ = 2 / Real.sqrt κ + 2 / Real.sqrt κ := by ring
    linarith
  have hdrop0 : 0 ≤ 2 / Real.sqrt κ := by positivity
  have hdrop_sq : (2 / Real.sqrt κ) ^ 2 ≤
      (4 / Real.sqrt κ - T / (κ / 2)) ^ 2 := by
    exact (sq_le_sq₀ hdrop0 (hdrop0.trans hdropbase)).mpr hdropbase
  have hdrop_id : ((κ / 2) / 2) * (2 / Real.sqrt κ) ^ 2 = 1 := by
    field_simp [hsqrt.ne']
    nlinarith only [hsqrt_sq]
  have hdrop : 1 ≤ ((κ / 2) / 2) *
      (4 / Real.sqrt κ - T / (κ / 2)) ^ 2 := by
    rw [← hdrop_id]
    exact mul_le_mul_of_nonneg_left hdrop_sq (by positivity)
  have hrc : (κ / 2) * (4 / Real.sqrt κ) = 2 * Real.sqrt κ := by
    field_simp [hsqrt.ne']
    nlinarith only [hsqrt_sq]
  exact ⟨hk, hc, by positivity, hradius, htwice, hcenter, hrT1, hs1,
    herr72, hcurv, hcap, hdrop, hrc⟩

end I4ActualFoldNumeric

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
    funext i
    fin_cases i <;> rfl
  have h := component_jet V hV 2 p ![u,v] w
  rw [hd] at h
  simpa only [iteratedFDeriv_two_apply, Matrix.cons_val_zero, Matrix.cons_val_one] using h


/-- Ordered second jet of either coordinate component of the actual potential. -/
theorem actual_component_second {L r k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (hr : r ≠ 0) (p u v w : ℝ × ℝ) :
    fderiv ℝ (fderiv ℝ (fun q => fderiv ℝ (actualFoldPotential r k sample) q w)) p u v =
      iteratedFDeriv ℝ 3 (smoothSourceField 2 L sample) (r • ![p.1,p.2])
        ![![u.1,u.2],![v.1,v.2],![w.1,w.2] ] / (6*k) := by
  rw [component_second _ (actualFoldPotential_smooth hL r k sample)]
  have h := pullback_jet (smoothSourceField 2 L sample)
    (smoothSourceField_smooth 2 hL sample) 3 ((6*k*r^3)⁻¹) r p ![u,v,w]
  have hV : actualFoldPotential r k sample =
      fun q => (6*k*r^3)⁻¹ * smoothSourceField 2 L sample (r • ![q.1,q.2]) := by
    ext q
    simp [actualFoldPotential, div_eq_mul_inv, mul_comm]
  have hd : (fun i : Fin 3 => ![(![u,v,w] i).1,(![u,v,w] i).2]) =
      ![![u.1,u.2],![v.1,v.2],![w.1,w.2] ] := by
    funext i
    fin_cases i <;> rfl
  rw [hV, h, hd]
  field_simp [hr]

theorem actual_Vy_second {L r k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (hr : r ≠ 0) (p u v : ℝ × ℝ) :
    fderiv ℝ (fderiv ℝ (Vy (actualFoldPotential r k sample))) p u v =
      iteratedFDeriv ℝ 3 (smoothSourceField 2 L sample) (r • ![p.1,p.2])
        ![![u.1,u.2],![v.1,v.2],directionY] / (6*k) :=
  actual_component_second hL sample hr p u v ey

theorem actual_Vx_second {L r k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (hr : r ≠ 0) (p u v : ℝ × ℝ) :
    fderiv ℝ (fderiv ℝ (Vx (actualFoldPotential r k sample))) p u v =
      iteratedFDeriv ℝ 3 (smoothSourceField 2 L sample) (r • ![p.1,p.2])
        ![![u.1,u.2],![v.1,v.2],directionX] / (6*k) :=
  actual_component_second hL sample hr p u v ex

theorem component_first (V : ℝ × ℝ → ℝ) (hV : ContDiff ℝ (⊤ : ℕ∞) V)
    (p u v : ℝ × ℝ) :
    fderiv ℝ (fun q => fderiv ℝ V q v) p u = iteratedFDeriv ℝ 2 V p ![u,v] := by
  have hd : Fin.snoc (fun _ : Fin 1 => u) v = ![u,v] := by
    funext i
    fin_cases i <;> rfl
  have h := component_jet V hV 1 p (fun _ => u) v
  simpa only [iteratedFDeriv_one_apply, hd] using h

/-- Actual source permutation, transported through the literal pullback. -/
theorem actual_second_swap {L r k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (p u v : ℝ × ℝ) :
    iteratedFDeriv ℝ 2 (actualFoldPotential r k sample) p ![u,v] =
      iteratedFDeriv ℝ 2 (actualFoldPotential r k sample) p ![v,u] := by
  have hV : actualFoldPotential r k sample =
      fun q => (6*k*r^3)⁻¹ * smoothSourceField 2 L sample (r • ![q.1,q.2]) := by
    ext q
    simp [actualFoldPotential, div_eq_mul_inv, mul_comm]
  rw [hV, pullback_jet _ (smoothSourceField_smooth 2 hL sample),
    pullback_jet _ (smoothSourceField_smooth 2 hL sample)]
  apply congrArg (fun t : ℝ => (6*k*r^3)⁻¹*r^2*t)
  let d : Fin 2 → Fin 2 → ℝ := ![![u.1,u.2],![v.1,v.2] ]
  have hp := source_derivative_comp_perm hL sample 2 (r • ![p.1,p.2]) d
    (Equiv.swap 0 1)
  have hd : d ∘ Equiv.swap 0 1 = ![![v.1,v.2],![u.1,u.2] ] := by
    funext i
    fin_cases i <;> simp [d]
  rw [hd] at hp
  have huv : (fun i : Fin 2 => ![(![u,v] i).1,(![u,v] i).2]) = d := by
    funext i
    fin_cases i <;> rfl
  have hvu : (fun i : Fin 2 => ![(![v,u] i).1,(![v,u] i).2]) =
      ![![v.1,v.2],![u.1,u.2] ] := by
    funext i
    fin_cases i <;> rfl
  rw [huv, hvu]
  exact hp.symm

theorem actual_Hy_eq_Gx {L r k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (p : ℝ × ℝ) :
    partialY (Vx (actualFoldPotential r k sample)) p =
      partialX (Vy (actualFoldPotential r k sample)) p := by
  change fderiv ℝ (fun q => fderiv ℝ (actualFoldPotential r k sample) q ex) p ey =
    fderiv ℝ (fun q => fderiv ℝ (actualFoldPotential r k sample) q ey) p ex
  rw [component_first _ (actualFoldPotential_smooth hL r k sample),
    component_first _ (actualFoldPotential_smooth hL r k sample)]
  exact actual_second_swap hL sample p ey ex

/-- Full actual operator bounds give a fixed-tuple jet Lipschitz bound. -/
theorem jet_lipschitz (V : ℝ × ℝ → ℝ) (hV : ContDiff ℝ (⊤ : ℕ∞) V)
    (n : ℕ) (u : Fin n → ℝ × ℝ) (hu : ∀ i, ‖u i‖ ≤ 1)
    (C : ℝ) (hbound : ∀ p, ‖iteratedFDeriv ℝ (n+1) V p‖ ≤ C)
    (p q : ℝ × ℝ) :
    |iteratedFDeriv ℝ n V p u - iteratedFDeriv ℝ n V q u| ≤ C * ‖p-q‖ := by
  have hvn : ContDiff ℝ (n+1 : ℕ) V := hV.of_le (by simp)
  have hd : Differentiable ℝ (iteratedFDeriv ℝ n V) :=
    hvn.differentiable_iteratedFDeriv (by exact_mod_cast Nat.lt_succ_self n)
  have hD : ‖iteratedFDeriv ℝ n V p - iteratedFDeriv ℝ n V q‖ ≤ C*‖p-q‖ := by
    apply Convex.norm_image_sub_le_of_norm_fderiv_le
      (fun x _ => hd x) (fun x _ => ?_) convex_univ (mem_univ _) (mem_univ _)
    rw [norm_fderiv_iteratedFDeriv]
    exact hbound x
  have hp : ∏ i, ‖u i‖ ≤ (1 : ℝ) :=
    Finset.prod_le_one₀ (fun _ _ => norm_nonneg _) (fun i _ => hu i)
  calc
    _ = ‖(iteratedFDeriv ℝ n V p - iteratedFDeriv ℝ n V q) u‖ := rfl
    _ ≤ ‖iteratedFDeriv ℝ n V p - iteratedFDeriv ℝ n V q‖ * ∏ i, ‖u i‖ :=
      ContinuousMultilinearMap.le_opNorm _ _
    _ ≤ ‖iteratedFDeriv ℝ n V p - iteratedFDeriv ℝ n V q‖ :=
      mul_le_of_le_one_right (norm_nonneg _) hp
    _ ≤ _ := hD

theorem point_norm_sub_le (x y u v : ℝ) :
    ‖((x,y) : ℝ × ℝ)-(u,v)‖ ≤ |x-u|+|y-v| := by
  simp only [Prod.norm_def, Prod.fst_sub, Prod.snd_sub, Real.norm_eq_abs]
  exact max_le (le_add_of_nonneg_right (abs_nonneg _))
    (le_add_of_nonneg_left (abs_nonneg _))

theorem axes_norm (u : ℝ × ℝ) (hu : u = ex ∨ u = ey) : ‖u‖ ≤ (1 : ℝ) := by
  rcases hu with rfl | rfl <;> norm_num [ex, ey, Prod.norm_def]

theorem second_component_bound {L r k₀ k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hk₀ : 0 < k₀) (hk : k₀ ≤ k)
    (p u v w : ℝ × ℝ) (hu : ‖u‖ ≤ 1) (hv : ‖v‖ ≤ 1) (hw : ‖w‖ ≤ 1) :
    |fderiv ℝ (fderiv ℝ (fun q => fderiv ℝ (actualFoldPotential r k sample) q w)) p u v|
      ≤ sourceT k₀ sample := by
  rw [component_second _ (actualFoldPotential_smooth hL r k sample)]
  have hprod : ∏ i, ‖(![u,v,w] : Fin 3 → ℝ × ℝ) i‖ ≤ (1 : ℝ) := by
    apply Finset.prod_le_one₀ (fun _ _ => norm_nonneg _)
    intro i _
    fin_cases i <;> assumption
  exact (ContinuousMultilinearMap.le_opNorm _ _).trans
    ((mul_le_of_le_one_right (norm_nonneg _) hprod).trans
      (actual_third_norm_bound hL sample hr hk₀ hk p))


theorem component_first_as_second (V : ℝ × ℝ → ℝ)
    (hV : ContDiff ℝ (⊤ : ℕ∞) V) (p u v : ℝ × ℝ) :
    fderiv ℝ (fun q => fderiv ℝ V q v) p u = fderiv ℝ (fderiv ℝ V) p u v := by
  simpa only [iteratedFDeriv_two_apply, Matrix.cons_val_zero, Matrix.cons_val_one]
    using component_first V hV p u v

theorem hasDerivAt_xslice {G : ℝ × ℝ → ℝ} {x y : ℝ}
    (hG : DifferentiableAt ℝ G (x,y)) :
    HasDerivAt (fun t => G (t,y)) (partialX G (x,y)) x := by
  have h := hG.hasFDerivAt.comp_hasDerivAt x
    ((hasDerivAt_id x).prodMk (hasDerivAt_const x y))
  simpa [Function.comp_def, partialX, ex] using h

theorem hasDerivAt_xslice_component (G : ℝ × ℝ → ℝ)
    (hG : ContDiff ℝ (⊤ : ℕ∞) G) (x y : ℝ) (w : ℝ × ℝ) :
    HasDerivAt (fun t => fderiv ℝ G (t,y) w)
      (fderiv ℝ (fderiv ℝ G) (x,y) ex w) x := by
  have h := hasDerivAt_xslice
    ((component_smooth G hG w).differentiable (by simp) (x,y))
  simpa only [partialX, component_first_as_second G hG] using h

theorem actual_second_lipschitz {L r k₀ k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hk₀ : 0 < k₀) (hk : k₀ ≤ k)
    (p q u v : ℝ × ℝ) (hu : ‖u‖ ≤ 1) (hv : ‖v‖ ≤ 1) :
    |fderiv ℝ (fun t => fderiv ℝ (actualFoldPotential r k sample) t v) p u -
      fderiv ℝ (fun t => fderiv ℝ (actualFoldPotential r k sample) t v) q u| ≤
      sourceT k₀ sample * ‖p-q‖ := by
  rw [component_first _ (actualFoldPotential_smooth hL r k sample),
    component_first _ (actualFoldPotential_smooth hL r k sample)]
  apply jet_lipschitz _ (actualFoldPotential_smooth hL r k sample) 2 ![u,v]
    _ _ (actual_third_norm_bound hL sample hr hk₀ hk) p q
  intro i
  fin_cases i <;> assumption

theorem actual_third_lipschitz {L r k₀ k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hk₀ : 0 < k₀) (hk : k₀ ≤ k)
    (p q u v w : ℝ × ℝ) (hu : ‖u‖ ≤ 1) (hv : ‖v‖ ≤ 1) (hw : ‖w‖ ≤ 1) :
    |fderiv ℝ (fderiv ℝ (fun t => fderiv ℝ (actualFoldPotential r k sample) t w)) p u v -
      fderiv ℝ (fderiv ℝ (fun t => fderiv ℝ (actualFoldPotential r k sample) t w)) q u v| ≤
      r * sourceT k₀ sample * ‖p-q‖ := by
  rw [component_second _ (actualFoldPotential_smooth hL r k sample),
    component_second _ (actualFoldPotential_smooth hL r k sample)]
  apply jet_lipschitz _ (actualFoldPotential_smooth hL r k sample) 3 ![u,v,w]
    _ _ (actual_fourth_norm_bound hL sample hr hk₀ hk) p q
  intro i
  fin_cases i <;> assumption

/-- Coordinate oscillations, obtained from the proved full actual majorant. -/
theorem actual_coordinate_oscillation {L r k₀ k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hk₀ : 0 < k₀) (hk : k₀ ≤ k)
    (x y u : ℝ) :
    |partialY (Vy (actualFoldPotential r k sample)) (x,y) + sourceKappa r k sample|
        ≤ sourceT k₀ sample * (|x|+|y|) ∧
    |partialX (Vy (actualFoldPotential r k sample)) (x,y) -
        partialX (Vy (actualFoldPotential r k sample)) (x,0)| ≤ sourceT k₀ sample * |y| ∧
    |partialY (Vx (actualFoldPotential r k sample)) (x,y) -
        partialY (Vx (actualFoldPotential r k sample)) (x,0)| ≤ sourceT k₀ sample * |y| ∧
    |fderiv ℝ (fderiv ℝ (Vx (actualFoldPotential r k sample))) (x,y) ex ex -
        fderiv ℝ (fderiv ℝ (Vx (actualFoldPotential r k sample))) (u,0) ex ex|
      ≤ r * sourceT k₀ sample * (|x-u|+|y|) := by
  have hx : ‖ex‖ ≤ (1 : ℝ) := axes_norm ex (Or.inl rfl)
  have hy : ‖ey‖ ≤ (1 : ℝ) := axes_norm ey (Or.inr rfl)
  have hT : 0 ≤ sourceT k₀ sample := (by norm_num : (0:ℝ) ≤ 1).trans (sourceT_one_le _ _)
  have hcenter : partialY (Vy (actualFoldPotential r k sample)) (0,0) =
      -sourceKappa r k sample := by
    rw [partialY, actualFoldPotential_transverse_center hL sample hr.ne']
    unfold sourceKappa sourceQ
    ring
  refine ⟨?_,?_,?_,?_⟩
  · have h := actual_second_lipschitz hL sample hr hk₀ hk (x,y) (0,0) ey ey hy hy
    change |partialY (Vy (actualFoldPotential r k sample)) (x,y) -
      partialY (Vy (actualFoldPotential r k sample)) (0,0)| ≤ _ at h
    rw [hcenter, sub_neg_eq_add] at h
    exact h.trans (by simpa only [sub_zero] using
      mul_le_mul_of_nonneg_left (point_norm_sub_le x y 0 0) hT)
  · have h := actual_second_lipschitz hL sample hr hk₀ hk (x,y) (x,0) ex ey hx hy
    exact h.trans (by simpa only [sub_self, abs_zero, zero_add, sub_zero] using
      mul_le_mul_of_nonneg_left (point_norm_sub_le x y x 0) hT)
  · have h := actual_second_lipschitz hL sample hr hk₀ hk (x,y) (x,0) ey ex hy hx
    exact h.trans (by simpa only [sub_self, abs_zero, zero_add, sub_zero] using
      mul_le_mul_of_nonneg_left (point_norm_sub_le x y x 0) hT)
  · have h := actual_third_lipschitz hL sample hr hk₀ hk (x,y) (u,0) ex ex ex hx hx hx
    exact h.trans (by simpa only [sub_zero] using
      mul_le_mul_of_nonneg_left (point_norm_sub_le x y u 0) (mul_nonneg hr.le hT))


theorem second_component_smooth (G : ℝ × ℝ → ℝ)
    (hG : ContDiff ℝ (⊤ : ℕ∞) G) (u v : ℝ × ℝ) :
    ContDiff ℝ (⊤ : ℕ∞) (fun p => fderiv ℝ (fderiv ℝ G) p u v) := by
  have he : (fun p => fderiv ℝ (fderiv ℝ G) p u v) =
      (fun p => fderiv ℝ (fun q => fderiv ℝ G q v) p u) := by
    funext p
    exact (component_first_as_second G hG p u v).symm
  rw [he]
  exact component_smooth _ (component_smooth G hG v) u

/-- The completed Peano weight has exactly unit mass after normalization. -/
theorem normalized_peano_mass :
    (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), (3/2-6*u^2)) = 1 := by
  have he : (fun u : ℝ => 3/2-6*u^2) = fun u => 6*peanoCubic u := by
    funext u
    unfold peanoCubic
    ring
  rw [he, intervalIntegral.integral_const_mul]
  exact peano_kernel_masses.2.2.2

/-- The normalized actual Peano average controls the axial jet on the wider box. -/
theorem actual_axial_pointwise_error {L r k₀ k R : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hk₀ : 0 < k₀) (hk : k₀ ≤ k)
    (hN : NormalizedFoldData (actualFoldPotential r k sample)) (hR : R ≤ 1/8)
    (x : ℝ) (hx : x ∈ J) (y : ℝ) (hy : y ∈ Icc (-R) R) :
    |2-fderiv ℝ (fderiv ℝ (Vx (actualFoldPotential r k sample))) (x,y) ex ex|
      ≤ 3*r*sourceT k₀ sample := by
  let K : ℝ × ℝ → ℝ := fun p =>
    fderiv ℝ (fderiv ℝ (Vx (actualFoldPotential r k sample))) p ex ex
  have hV := actualFoldPotential_smooth hL r k sample
  have hH : ContDiff ℝ (⊤ : ℕ∞) (Vx (actualFoldPotential r k sample)) :=
    component_smooth _ hV ex
  have hK : Continuous (fun t : ℝ => K (t,0)) :=
    (second_component_smooth _ hH ex ex).continuous.comp
      (continuous_id.prodMk continuous_const)
  have hT : 0 ≤ sourceT k₀ sample := (by norm_num : (0:ℝ)≤1).trans (sourceT_one_le _ _)
  have hxy : |x| ≤ 3/2 ∧ |y| ≤ 1/8 := by
    exact ⟨abs_le.mpr hx, (abs_le.mpr hy).trans hR⟩
  have hbound : ∀ u ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), |K (u,0)-K (x,y)| ≤
      3*r*sourceT k₀ sample := by
    intro u hu
    have huabs : |u| ≤ (1/2 : ℝ) := abs_le.mpr hu
    have hdist : |x-u|+|y| ≤ 3 := by
      have ha := abs_sub x u
      linarith
    have h := (actual_coordinate_oscillation hL sample hr hk₀ hk x y u).2.2.2
    rw [abs_sub_comm] at h
    exact h.trans (by nlinarith [mul_nonneg hr.le hT])
  have hw : ∀ u ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), 0 ≤ (3/2-6*u^2) := by
    intro u hu
    have h := peanoCubic_nonneg u hu
    unfold peanoCubic at h
    linarith
  have h := abs_weighted_integral_sub_mass_le
    (fun u => 3/2-6*u^2) (fun t => K (t,0)) (by fun_prop) hK
    1 (K (x,y)) (3*r*sourceT k₀ sample) hw (by simpa only [one_mul] using hbound)
  have hp := hN.2.2.2.2.2.2
  change (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), (3/2-6*u^2)*K (u,0)) = 2 at hp
  simpa only [one_mul, hp, normalized_peano_mass, mul_one] using h

/-- A fixed negative vertical derivative and the center bound give strict signs. -/
theorem vertical_boundary_signs (G : ℝ × ℝ → ℝ)
    (hG : ContDiff ℝ (⊤ : ℕ∞) G) {R c T : ℝ}
    (hR : 0 < R) (hcenter : ∀ x ∈ J, |G (x,0)| ≤ T)
    (hneg : ∀ x ∈ J, ∀ y ∈ Icc (-R) R, partialY G (x,y) ≤ -c)
    (hmargin : T < c*R) :
    (∀ x ∈ J, 0 < G (x,-R)) ∧ (∀ x ∈ J, G (x,R) < 0) := by
  have hslice (x : ℝ) : ContDiff ℝ (⊤ : ℕ∞) (fun y => G (x,y)) :=
    hG.comp (contDiff_const.prodMk contDiff_id)
  have hder (x y : ℝ) : deriv (fun t => G (x,t)) y = partialY G (x,y) :=
    (hasDerivAt_slice (hG.differentiable (by simp) (x,y))).deriv
  constructor
  · intro x hx
    have h := (convex_Icc (-R) R).image_sub_le_mul_sub_of_deriv_le
      (hslice x).continuous.continuousOn
      (hslice x).differentiable (by simp) |>.differentiableOn
    have hb := h (C := -c) (by
      intro y hy
      rw [hder]
      exact hneg x hx y (interior_subset hy))
      (-R) ⟨le_rfl, by linarith⟩ 0 ⟨by linarith, hR.le⟩ (by linarith)
    have hc := (abs_le.mp (hcenter x hx)).1
    nlinarith
  · intro x hx
    have h := (convex_Icc (-R) R).image_sub_le_mul_sub_of_deriv_le
      (hslice x).continuous.continuousOn
      ((hslice x).differentiable (by simp)).differentiableOn
      (C := -c) (by
        intro y hy
        rw [hder]
        exact hneg x hx y (interior_subset hy))
      0 ⟨by linarith, hR.le⟩ R ⟨by linarith, le_rfl⟩ hR.le
    have hc := (abs_le.mp (hcenter x hx)).2
    nlinarith

end I4SourceAdaptiveFoldEstimates
