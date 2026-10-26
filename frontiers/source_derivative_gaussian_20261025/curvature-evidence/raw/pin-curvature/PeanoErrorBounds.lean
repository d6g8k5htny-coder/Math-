import SourceConfluentLimits

noncomputable section

open MeasureTheory Set I4SourceConfluentLimits
open scoped Interval

namespace I4PeanoErrorBounds

/-- A nonnegative continuous scalar weight preserves a uniform error bound,
with its exact mass. -/
theorem abs_weighted_integral_le (w f : ℝ → ℝ)
    (hwc : Continuous w) (hfc : Continuous f) (B : ℝ)
    (hw : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), 0 ≤ w t)
    (hf : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), |f t| ≤ B) :
    |∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t * f t| ≤
      B * ∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t := by
  calc
    _ ≤ ∫ t in (-1/2 : ℝ)..(1/2 : ℝ), |w t * f t| :=
      intervalIntegral.abs_integral_le_integral_abs (by norm_num)
    _ ≤ ∫ t in (-1/2 : ℝ)..(1/2 : ℝ), B * w t := by
      apply intervalIntegral.integral_mono_on (by norm_num)
        ((hwc.mul hfc).abs.intervalIntegrable _ _)
        ((continuous_const.mul hwc).intervalIntegrable _ _)
      intro t ht
      change |w t * f t| ≤ B * w t
      rw [abs_mul, abs_of_nonneg (hw t ht)]
      calc
        w t * |f t| ≤ w t * B := mul_le_mul_of_nonneg_left (hf t ht) (hw t ht)
        _ = B * w t := mul_comm _ _
    _ = _ := intervalIntegral.integral_const_mul _ _

/-- Subtracting a constant from the averaged function subtracts that constant
times the exact weight mass. -/
theorem abs_weighted_integral_sub_mass_le (w g : ℝ → ℝ)
    (hwc : Continuous w) (hgc : Continuous g) (r c B : ℝ)
    (hw : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), 0 ≤ w t)
    (hg : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), |g (r*t) - c| ≤ B) :
    |(∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t * g (r*t)) -
      c * (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t)| ≤
      B * (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t) := by
  have hc : Continuous (fun t => g (r*t)) :=
    hgc.comp (continuous_const.mul continuous_id)
  have heq : (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t * (g (r*t)-c)) =
      (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t * g (r*t)) -
        c * (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t) := by
    simp_rw [mul_sub]
    have hi1 : IntervalIntegrable (fun t => w t * g (r*t)) volume (-1/2 : ℝ) (1/2 : ℝ) :=
      (hwc.mul hc).intervalIntegrable _ _
    have hi2 : IntervalIntegrable (fun t => w t * c) volume (-1/2 : ℝ) (1/2 : ℝ) :=
      (hwc.mul continuous_const).intervalIntegrable _ _
    rw [intervalIntegral.integral_sub hi1 hi2]
    rw [intervalIntegral.integral_mul_const]
    ring
  rw [← heq]
  exact abs_weighted_integral_le w _ hwc (hc.sub continuous_const) B hw hg

theorem peanoCubic_nonneg (t : ℝ) (ht : t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ)) :
    0 ≤ peanoCubic t := by
  unfold peanoCubic
  have hp : 0 ≤ (t+1/2)*(1/2-t) := mul_nonneg (by linarith [ht.1]) (by linarith [ht.2])
  nlinarith

/-- The same scalar Lipschitz bound controls every point of the scaled interval
around the literal value at the origin, retaining the half-interval factor. -/
theorem scaled_lipschitz_center_error (g : ℝ → ℝ) (C r : ℝ) (hC : 0 ≤ C) (hr : 0 ≤ r)
    (hlip : ∀ x y : ℝ, |g x-g y| ≤ C * |x-y|)
    (u : ℝ) (hu : u ∈ Icc (-1/2 : ℝ) (1/2 : ℝ)) :
    |g (r*u)-g 0| ≤ r*C/2 := by
  have huabs : |u| ≤ (1/2 : ℝ) := abs_le.mpr ⟨by linarith [hu.1], hu.2⟩
  calc
    _ ≤ C * |r*u-0| := hlip _ _
    _ = C * (r*|u|) := by rw [sub_zero, abs_mul, abs_of_nonneg hr]
    _ ≤ C * (r*(1/2)) :=
      mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left huabs hr) hC
    _ = r*C/2 := by ring

/-- A globally Lipschitz function with cubic Peano average two stays within
`r*C` of two everywhere in the scaled interval. -/
theorem cubic_pin_pointwise_error (g : ℝ → ℝ) (hgc : Continuous g)
    (C r : ℝ) (hC : 0 ≤ C) (hr : 0 ≤ r)
    (hlip : ∀ x y : ℝ, |g x - g y| ≤ C * |x-y|)
    (hpin : 6 * (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic t * g (r*t)) = 2)
    (u : ℝ) (hu : u ∈ Icc (-1/2 : ℝ) (1/2 : ℝ)) :
    |g (r*u) - 2| ≤ r*C := by
  have hcK : Continuous peanoCubic := by unfold peanoCubic; fun_prop
  have hcG : Continuous (fun t => g (r*u) - g (r*t)) := by
    exact continuous_const.sub (hgc.comp (continuous_const.mul continuous_id))
  have hbound : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), |g (r*u) - g (r*t)| ≤ r*C := by
    intro t ht
    have hud : |u-t| ≤ 1 := abs_le.mpr ⟨by linarith [hu.1, ht.2], by linarith [hu.2, ht.1]⟩
    calc
      _ ≤ C * |r*u-r*t| := hlip _ _
      _ = C * (r*|u-t|) := by rw [← mul_sub, abs_mul, abs_of_nonneg hr]
      _ ≤ C * r := mul_le_mul_of_nonneg_left (mul_le_of_le_one_right hr hud) hC
      _ = r*C := mul_comm _ _
  have hi := abs_weighted_integral_le peanoCubic _ hcK hcG (r*C) peanoCubic_nonneg hbound
  have hmass := peano_kernel_masses.2.2.2
  have hmass' : (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic t) = 1/6 := by
    linarith [hmass]
  rw [hmass'] at hi
  have heq : 6 * (∫ t in (-1/2 : ℝ)..(1/2 : ℝ),
      peanoCubic t * (g (r*u)-g (r*t))) = g (r*u)-2 := by
    simp_rw [mul_sub]
    have hi1 : IntervalIntegrable (fun t => peanoCubic t * g (r*u)) volume
        (-1/2 : ℝ) (1/2 : ℝ) := (hcK.mul continuous_const).intervalIntegrable _ _
    have hi2 : IntervalIntegrable (fun t => peanoCubic t * g (r*t)) volume
        (-1/2 : ℝ) (1/2 : ℝ) :=
      (hcK.mul (hgc.comp (continuous_const.mul continuous_id))).intervalIntegrable _ _
    rw [intervalIntegral.integral_sub hi1 hi2]
    rw [intervalIntegral.integral_mul_const]
    rw [hmass']
    nlinarith [hpin, hmass]
  have habs : |g (r*u)-2| = 6 * |∫ t in (-1/2 : ℝ)..(1/2 : ℝ),
      peanoCubic t * (g (r*u)-g (r*t))| := by
    rw [← heq, abs_mul]
    norm_num
  rw [habs]
  nlinarith [hi, hmass]

/-- The left affine Peano average retains half the uniform pointwise error. -/
theorem left_weighted_error (g : ℝ → ℝ) (hgc : Continuous g) (r c B : ℝ)
    (hg : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), |g (r*t)-c| ≤ B) :
    |(∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoLeft t * g (r*t)) - c/2| ≤ B/2 := by
  have hc : Continuous peanoLeft := by unfold peanoLeft; fun_prop
  have hw : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), 0 ≤ peanoLeft t := by
    intro t ht
    unfold peanoLeft
    linarith [ht.2]
  have h := abs_weighted_integral_sub_mass_le peanoLeft g hc hgc r c B hw hg
  rw [peano_kernel_masses.2.1] at h
  simpa only [mul_one_div] using h

/-- The right affine Peano average retains half the uniform pointwise error. -/
theorem right_weighted_error (g : ℝ → ℝ) (hgc : Continuous g) (r c B : ℝ)
    (hg : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), |g (r*t)-c| ≤ B) :
    |(∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoRight t * g (r*t)) - c/2| ≤ B/2 := by
  have hc : Continuous peanoRight := by unfold peanoRight; fun_prop
  have hw : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), 0 ≤ peanoRight t := by
    intro t ht
    unfold peanoRight
    linarith [ht.1]
  have h := abs_weighted_integral_sub_mass_le peanoRight g hc hgc r c B hw hg
  rw [peano_kernel_masses.2.2.1] at h
  simpa only [mul_one_div] using h

end I4PeanoErrorBounds
