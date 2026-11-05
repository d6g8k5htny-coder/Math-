import AdaptiveFoldScalarBarrier
import Mathlib.Analysis.Calculus.LocalExtr.Rolle
import Mathlib.Analysis.Calculus.MeanValue

noncomputable section
open Set

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
        exact le_rfl
      have hlt : x < -(1 / 2 : ℝ) := lt_of_le_of_ne hleft heq
      have h := hf.slope_mono_adjacent hx hpJ hlt
        (by norm_num : -(1 / 2 : ℝ) < 1 / 2)
      simp only [hm, hp, sub_self, zero_div, zero_sub] at h
      have hden : 0 < -(1 / 2 : ℝ) - x := by linarith
      have := (div_le_iff₀ hden).mp h
      linarith
    · by_cases heq : x = (1 / 2 : ℝ)
      · rw [heq, hp]
        exact le_rfl
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
