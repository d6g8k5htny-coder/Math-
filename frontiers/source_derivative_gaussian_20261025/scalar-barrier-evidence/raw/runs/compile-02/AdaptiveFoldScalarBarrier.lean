import Mathlib.Analysis.Convex.Deriv
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
# Normalized adaptive fold scalar barrier

A deterministic scalar companion to the conventional adaptive elder proof, §4.
Explicit derivative jets and normalized pins give scalar comparisons and arm
separation. This file does not construct an actual transverse ridge, an ambient
rectangle, a physical chart or path, an elder relation, or a probability bound.
The existing generic interpolation and topological libraries are not repeated.
-/

noncomputable section
open Set MeasureTheory

namespace AdaptiveFoldScalar

/-- The normalized scalar domain. -/
def J : Set ℝ := Icc (-(3 / 2 : ℝ)) (3 / 2)

/-- The quadratic lower-curvature comparison, zero at both pins. -/
def q (x : ℝ) : ℝ := (x ^ 2 - (1 / 4 : ℝ)) / 2

/-- Scalar consequences only; no ambient ridge or elder data are bundled. -/
structure ScalarBarrier (a a₁ φ : ℝ → ℝ) : Prop where
  middle_comparison : ∀ x ∈ Icc (-(1 / 2 : ℝ)) (1 / 2), a x ≤ q x
  left_comparison : ∀ x ∈ Icc (-(3 / 2 : ℝ)) (-(1 / 2 : ℝ)), q x ≤ a x
  right_comparison : ∀ x ∈ Icc (1 / 2 : ℝ) (3 / 2), q x ≤ a x
  middle_neg : ∀ x ∈ Ioo (-(1 / 2 : ℝ)) (1 / 2), a x < 0
  left_pos : ∀ x ∈ Ico (-(3 / 2 : ℝ)) (-(1 / 2 : ℝ)), 0 < a x
  right_pos : ∀ x ∈ Ioc (1 / 2 : ℝ) (3 / 2), 0 < a x
  left_deriv : a₁ (-(1 / 2 : ℝ)) ≤ -(1 / 2 : ℝ)
  right_deriv : (1 / 2 : ℝ) ≤ a₁ (1 / 2 : ℝ)
  left_gain : φ (-(3 / 2 : ℝ)) ≤ φ (-(1 / 2 : ℝ)) - 5 / 12
  right_gain : φ (1 / 2 : ℝ) + 5 / 12 ≤ φ (3 / 2 : ℝ)
  left_barrier : φ (-(3 / 2 : ℝ)) ≤ φ (1 / 2 : ℝ) - 1 / 4
  right_older : φ (-(1 / 2 : ℝ)) + 1 / 4 ≤ φ (3 / 2 : ℝ)
  ceiling : ∀ x ∈ Icc (-(3 / 2 : ℝ)) (1 / 2), φ x ≤ φ (-(1 / 2 : ℝ))
  floor : ∀ x ∈ Icc (-(1 / 2 : ℝ)) (3 / 2), φ (1 / 2 : ℝ) ≤ φ x

/-- The derivative of the comparison quadratic. -/
theorem q_hasDerivAt (x : ℝ) : HasDerivAt q x x := by
  convert ((hasDerivAt_pow 2 x).sub_const (1 / 4 : ℝ)).div_const 2 using 1 <;>
    (simp only [q, Pi.sub_apply, id]; norm_num <;> ring)

/-- The primitive used for both exact arm integrals. -/
theorem primitive_hasDerivAt (x : ℝ) :
    HasDerivAt (fun t : ℝ => t ^ 3 / 6 - t / 8) (q x) x := by
  convert ((hasDerivAt_pow 3 x).div_const 6).sub
    ((hasDerivAt_id x).div_const 8) using 1 <;> (simp only [q, Pi.sub_apply, id]; norm_num <;> ring)

/-- The left comparison arm has exactly the gain 5/12. -/
theorem integral_q_left :
    (∫ x in (-(3 / 2 : ℝ))..(-(1 / 2 : ℝ)), q x) = 5 / 12 := by
  have hc : Continuous q := continuous_iff_continuousAt.mpr (fun x => (q_hasDerivAt x).continuousAt)
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt
    (a := -(3 / 2 : ℝ)) (b := -(1 / 2 : ℝ))
    (fun x _ => primitive_hasDerivAt x) (hc.intervalIntegrable _ _)
  norm_num at h ⊢
  exact h

/-- The right comparison arm has exactly the gain 5/12. -/
theorem integral_q_right :
    (∫ x in (1 / 2 : ℝ)..(3 / 2 : ℝ), q x) = 5 / 12 := by
  have hc : Continuous q := continuous_iff_continuousAt.mpr (fun x => (q_hasDerivAt x).continuousAt)
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt
    (a := (1 / 2 : ℝ)) (b := (3 / 2 : ℝ))
    (fun x _ => primitive_hasDerivAt x) (hc.intervalIntegrable _ _)
  norm_num at h ⊢
  exact h

/-- Normalized convex core. Differentiability jets, zero pins and the gap are
explicit inputs; no barrier or elder conclusion occurs among the premises. -/
theorem scalarBarrier_of_convex (a a₁ φ : ℝ → ℝ)
    (hconv : ConvexOn ℝ J (fun x => a x - q x))
    (ha : ∀ x ∈ J, HasDerivAt a (a₁ x) x)
    (hφ : ∀ x ∈ J, HasDerivAt φ (a x) x)
    (hleft : a (-(1 / 2 : ℝ)) = 0)
    (hright : a (1 / 2 : ℝ) = 0)
    (hgap : φ (-(1 / 2 : ℝ)) - φ (1 / 2 : ℝ) = 1 / 6) :
    ScalarBarrier a a₁ φ := by
  have hlJ : -(1 / 2 : ℝ) ∈ J := by norm_num [J]
  have hrJ : (1 / 2 : ℝ) ∈ J := by norm_num [J]
  have hlq : a (-(1 / 2 : ℝ)) - q (-(1 / 2 : ℝ)) = 0 := by
    norm_num [q, hleft]
  have hrq : a (1 / 2 : ℝ) - q (1 / 2 : ℝ) = 0 := by
    norm_num [q, hright]
  have hmid : ∀ x ∈ Icc (-(1 / 2 : ℝ)) (1 / 2), a x ≤ q x := by
    intro x hx
    have h := hconv.le_on_segment hlJ hrJ
      (show x ∈ segment ℝ (-(1 / 2 : ℝ)) (1 / 2) from by
        rw [segment_eq_Icc (by norm_num : -(1 / 2 : ℝ) ≤ 1 / 2)]; exact hx)
    simp only [hlq, hrq, max_self] at h
    linarith
  have hL : ∀ x ∈ Icc (-(3 / 2 : ℝ)) (-(1 / 2 : ℝ)), q x ≤ a x := by
    intro x hx
    by_cases heq : x = -(1 / 2 : ℝ)
    · subst x; norm_num [q, hleft]
    have hlt : x < -(1 / 2 : ℝ) := lt_of_le_of_ne hx.2 heq
    have hxJ : x ∈ J := ⟨hx.1, by linarith [hx.2]⟩
    have h := hconv.slope_mono_adjacent hxJ hrJ hlt
      (by norm_num : -(1 / 2 : ℝ) < 1 / 2)
    simp only [hlq, hrq, sub_self, zero_div, zero_sub] at h
    have hden : 0 < -(1 / 2 : ℝ) - x := by linarith
    have := (div_le_iff₀ hden).mp h
    linarith
  have hR : ∀ x ∈ Icc (1 / 2 : ℝ) (3 / 2), q x ≤ a x := by
    intro x hx
    by_cases heq : x = (1 / 2 : ℝ)
    · subst x; norm_num [q, hright]
    have hlt : (1 / 2 : ℝ) < x := lt_of_le_of_ne hx.1 (Ne.symm heq)
    have hxJ : x ∈ J := ⟨by linarith [hx.1], hx.2⟩
    have h := hconv.slope_mono_adjacent hlJ hxJ
      (by norm_num : -(1 / 2 : ℝ) < 1 / 2) hlt
    simp only [hlq, hrq, sub_self, zero_div, sub_zero] at h
    have hden : 0 < x - (1 / 2 : ℝ) := by linarith
    have := (le_div_iff₀ hden).mp h
    linarith
  have hmn : ∀ x ∈ Ioo (-(1 / 2 : ℝ)) (1 / 2), a x < 0 := by
    intro x hx
    have hb := hmid x ⟨hx.1.le, hx.2.le⟩
    have hp := mul_pos (sub_pos.mpr hx.1) (sub_pos.mpr hx.2)
    dsimp [q] at hb
    nlinarith
  have hLp : ∀ x ∈ Ico (-(3 / 2 : ℝ)) (-(1 / 2 : ℝ)), 0 < a x := by
    intro x hx
    have hb := hL x ⟨hx.1, hx.2.le⟩
    have hp := mul_pos (show 0 < -x - 1 / 2 by linarith [hx.2])
      (show 0 < -x + 1 / 2 by linarith [hx.2])
    dsimp [q] at hb
    nlinarith
  have hRp : ∀ x ∈ Ioc (1 / 2 : ℝ) (3 / 2), 0 < a x := by
    intro x hx
    have hb := hR x ⟨hx.1.le, hx.2⟩
    have hp := mul_pos (show 0 < x - 1 / 2 by linarith [hx.1])
      (show 0 < x + 1 / 2 by linarith [hx.1])
    dsimp [q] at hb
    nlinarith
  have hld : a₁ (-(1 / 2 : ℝ)) ≤ -(1 / 2 : ℝ) := by
    have h := hconv.le_slope_of_hasDerivAt hlJ hrJ
      (by norm_num : -(1 / 2 : ℝ) < 1 / 2)
      ((ha _ hlJ).sub (q_hasDerivAt _))
    norm_num [slope_def_field, hlq, hrq] at h
    linarith
  have hrd : (1 / 2 : ℝ) ≤ a₁ (1 / 2 : ℝ) := by
    have h := hconv.slope_le_of_hasDerivAt hlJ hrJ
      (by norm_num : -(1 / 2 : ℝ) < 1 / 2)
      ((ha _ hrJ).sub (q_hasDerivAt _))
    norm_num [slope_def_field, hlq, hrq] at h
    linarith
  have hcq : Continuous q := continuous_iff_continuousAt.mpr (fun x => (q_hasDerivAt x).continuousAt)
  have hca : ContinuousOn a J := fun x hx => (ha x hx).continuousAt.continuousWithinAt
  have hLa : IntervalIntegrable a volume (-(3 / 2 : ℝ)) (-(1 / 2 : ℝ)) :=
    (hca.mono (show Icc (-(3 / 2 : ℝ)) (-(1 / 2 : ℝ)) ⊆ J from by
      intro x hx; exact ⟨hx.1, by linarith [hx.2]⟩)).intervalIntegrable_of_Icc (by norm_num)
  have hRa : IntervalIntegrable a volume (1 / 2 : ℝ) (3 / 2 : ℝ) :=
    (hca.mono (show Icc (1 / 2 : ℝ) (3 / 2 : ℝ) ⊆ J from by
      intro x hx; exact ⟨by linarith [hx.1], hx.2⟩)).intervalIntegrable_of_Icc (by norm_num)
  have hlg : φ (-(3 / 2 : ℝ)) ≤ φ (-(1 / 2 : ℝ)) - 5 / 12 := by
    have hbound := intervalIntegral.integral_mono_on (by norm_num)
      (hcq.intervalIntegrable (-(3 / 2 : ℝ)) (-(1 / 2 : ℝ))) hLa hL
    have hftc := intervalIntegral.integral_eq_sub_of_hasDerivAt
      (a := -(3 / 2 : ℝ)) (b := -(1 / 2 : ℝ))
      (fun x hx => hφ x (by
        rw [uIcc_of_le (by norm_num)] at hx
        exact ⟨hx.1, by linarith [hx.2]⟩)) hLa
    rw [integral_q_left, hftc] at hbound
    linarith
  have hrg : φ (1 / 2 : ℝ) + 5 / 12 ≤ φ (3 / 2 : ℝ) := by
    have hbound := intervalIntegral.integral_mono_on (by norm_num)
      (hcq.intervalIntegrable (1 / 2 : ℝ) (3 / 2 : ℝ))) hRa hR
    have hftc := intervalIntegral.integral_eq_sub_of_hasDerivAt
      (a := (1 / 2 : ℝ)) (b := (3 / 2 : ℝ))
      (fun x hx => hφ x (by
        rw [uIcc_of_le (by norm_num)] at hx
        exact ⟨by linarith [hx.1], hx.2⟩)) hRa
    rw [integral_q_right, hftc] at hbound
    linarith
  have hLmono : MonotoneOn φ (Icc (-(3 / 2 : ℝ)) (-(1 / 2 : ℝ))) := by
    apply monotoneOn_of_hasDerivWithinAt_nonneg (convex_Icc _ _)
    · intro x hx; exact (hφ x ⟨hx.1, by linarith [hx.2]⟩).continuousAt.continuousWithinAt
    · intro x hx; exact (hφ x ⟨(interior_subset hx).1,
        by linarith [(interior_subset hx).2]⟩).hasDerivWithinAt
    · intro x hx
      have hx' := interior_subset hx
      have hb := hL x hx'
      dsimp [q] at hb
      nlinarith [mul_nonneg_of_nonpos_of_nonpos
        (show x + 1 / 2 ≤ 0 by linarith [hx'.2])
        (show x - 1 / 2 ≤ 0 by linarith [hx'.2])]
  have hManti : AntitoneOn φ (Icc (-(1 / 2 : ℝ)) (1 / 2)) := by
    apply antitoneOn_of_hasDerivWithinAt_nonpos (convex_Icc _ _)
    · intro x hx; exact (hφ x ⟨by linarith [hx.1], by linarith [hx.2]⟩).continuousAt.continuousWithinAt
    · intro x hx; exact (hφ x ⟨by linarith [(interior_subset hx).1],
        by linarith [(interior_subset hx).2]⟩).hasDerivWithinAt
    · intro x hx
      have hx' := interior_subset hx
      have hb := hmid x hx'
      dsimp [q] at hb
      nlinarith [mul_nonpos_of_nonneg_of_nonpos
        (show 0 ≤ x + 1 / 2 by linarith [hx'.1])
        (show x - 1 / 2 ≤ 0 by linarith [hx'.2])]
  have hRmono : MonotoneOn φ (Icc (1 / 2 : ℝ) (3 / 2)) := by
    apply monotoneOn_of_hasDerivWithinAt_nonneg (convex_Icc _ _)
    · intro x hx; exact (hφ x ⟨by linarith [hx.1], hx.2⟩).continuousAt.continuousWithinAt
    · intro x hx; exact (hφ x ⟨by linarith [(interior_subset hx).1],
        (interior_subset hx).2⟩).hasDerivWithinAt
    · intro x hx
      have hx' := interior_subset hx
      have hb := hR x hx'
      dsimp [q] at hb
      nlinarith [mul_nonneg (show 0 ≤ x + 1 / 2 by linarith [hx'.1])
        (show 0 ≤ x - 1 / 2 by linarith [hx'.1])]
  refine ⟨hmid, hL, hR, hmn, hLp, hRp, hld, hrd, hlg, hrg,
    by linarith, by linarith, ?_, ?_⟩
  · intro x hx
    by_cases hl : x ≤ -(1 / 2 : ℝ)
    · exact hLmono ⟨hx.1, hl⟩ (by norm_num) hl
    · exact hManti (by norm_num) ⟨(lt_of_not_ge hl).le, hx.2⟩ (lt_of_not_ge hl).le
  · intro x hx
    by_cases hr : x ≤ (1 / 2 : ℝ)
    · exact hManti ⟨hx.1, hr⟩ (by norm_num) hr
    · exact hRmono (by norm_num) ⟨(lt_of_not_ge hr).le, hx.2⟩ (lt_of_not_ge hr).le

/-- Explicit second-derivative adapter. The final assumptions are derivative
jets, curvature and normalized pins, rather than a desired barrier certificate. -/
theorem scalarBarrier_of_secondDerivative (a a₁ a₂ φ : ℝ → ℝ)
    (ha : ∀ x ∈ J, HasDerivAt a (a₁ x) x)
    (ha₁ : ∀ x ∈ J, HasDerivAt a₁ (a₂ x) x)
    (hcurv : ∀ x ∈ J, 1 ≤ a₂ x)
    (hφ : ∀ x ∈ J, HasDerivAt φ (a x) x)
    (hleft : a (-(1 / 2 : ℝ)) = 0)
    (hright : a (1 / 2 : ℝ) = 0)
    (hgap : φ (-(1 / 2 : ℝ)) - φ (1 / 2 : ℝ) = 1 / 6) :
    ScalarBarrier a a₁ φ := by
  apply scalarBarrier_of_convex a a₁ φ ?_ ha hφ hleft hright hgap
  apply convexOn_of_hasDerivWithinAt2_nonneg (convex_Icc _ _)
    (f' := fun x => a₁ x - x) (f'' := fun x => a₂ x - 1)
  · intro x hx
    exact ((ha x hx).sub (q_hasDerivAt x)).continuousAt.continuousWithinAt
  · intro x hx
    exact ((ha x (interior_subset hx)).sub (q_hasDerivAt x)).hasDerivWithinAt
  · intro x hx
    exact ((ha₁ x (interior_subset hx)).sub (hasDerivAt_id x)).hasDerivWithinAt
  · intro x hx
    linarith [hcurv x (interior_subset hx)]

end AdaptiveFoldScalar
