import SourcePinPreservingQuartic

noncomputable section
open I4SourcePinPreservingQuartic
open scoped BigOperators

set_option autoImplicit false

namespace I4QuarticCaptureAlgebra

def rawRadius (U : Fin 8 → ℝ) : ℝ := 1 + ∑ i, |U i|

def regular (r : ℝ) (U : Fin 8 → ℝ) : Prop :=
  r * rawRadius U ^ 5 ≤ 1 / (1024 * quarticK0)

def captureWidth (r : ℝ) (U : Fin 8 → ℝ) : ℝ := quarticWidth r U (rawRadius U)

def captureSigma (r : ℝ) (U : Fin 8 → ℝ) : ℝ := 4 * rawRadius U * captureWidth r U

theorem rawRadius_one_le (U : Fin 8 → ℝ) : 1 ≤ rawRadius U := by
  have h : 0 ≤ ∑ i, |U i| := Finset.sum_nonneg (fun _ _ => abs_nonneg _)
  unfold rawRadius
  linarith

theorem rawRadius_pos (U : Fin 8 → ℝ) : 0 < rawRadius U :=
  lt_of_lt_of_le (by norm_num) (rawRadius_one_le U)

theorem rawRadius_sum_abs_eq (U : Fin 8 → ℝ) : ∑ i, |U i| = rawRadius U - 1 := by
  unfold rawRadius
  ring

theorem rawRadius_coord_abs_le_sub_one (U : Fin 8 → ℝ) (i : Fin 8) :
    |U i| ≤ rawRadius U - 1 := by
  rw [← rawRadius_sum_abs_eq]
  exact Finset.single_le_sum (fun j (_ : j ∈ (Finset.univ : Finset (Fin 8))) =>
    abs_nonneg (U j)) (Finset.mem_univ i)

theorem rawRadius_coord_abs_le (U : Fin 8 → ℝ) (i : Fin 8) : |U i| ≤ rawRadius U := by
  linarith [rawRadius_coord_abs_le_sub_one U i]

theorem captureWidth_pos (r : ℝ) (U : Fin 8 → ℝ) (hr : 0 ≤ r) :
    0 < captureWidth r U := quarticWidth_pos r _ hr (rawRadius_one_le U) U

theorem captureFstar_le_radius (r : ℝ) (U : Fin 8 → ℝ) (hr1 : r ≤ 1) :
    quarticFstar r U ≤ 2 * rawRadius U := by
  have h0 := rawRadius_coord_abs_le U 0
  have h4 := rawRadius_coord_abs_le U 4
  have hR := rawRadius_one_le U
  have hm : r * |U 4| ≤ |U 4| := mul_le_of_le_one_left (abs_nonneg _) hr1
  unfold quarticFstar
  linarith

theorem captureWidth_radius_le (r : ℝ) (U : Fin 8 → ℝ) (hr1 : r ≤ 1) :
    rawRadius U * captureWidth r U ≤ 1 / 2048 := by
  have hR := rawRadius_one_le U
  have hR0 : 0 ≤ rawRadius U := (by norm_num : (0 : ℝ) ≤ 1).trans hR
  have hF := captureFstar_le_radius r U hr1
  have hpow : rawRadius U ^ 2 ≤ rawRadius U ^ 5 := pow_le_pow_right₀ hR (by norm_num)
  have hm := mul_le_mul_of_nonneg_left hF hR0
  have hden : 0 < quarticK0 * rawRadius U ^ 5 :=
    mul_pos (by norm_num [quarticK0]) (pow_pos (rawRadius_pos U) 5)
  calc
    _ = (rawRadius U * quarticFstar r U) / (quarticK0 * rawRadius U ^ 5) := by
      unfold captureWidth quarticWidth
      ring
    _ ≤ 1 / 2048 := by
      apply (div_le_iff₀ hden).mpr
      norm_num only [quarticK0]
      nlinarith

theorem captureWidth_le (r : ℝ) (U : Fin 8 → ℝ) (hr1 : r ≤ 1) :
    captureWidth r U ≤ 1 / 2048 :=
  (certificate_width_geometry _ _ (rawRadius_one_le U) (captureWidth_radius_le r U hr1)).1

theorem captureWidth_le_one_sixteenth (r : ℝ) (U : Fin 8 → ℝ) (hr1 : r ≤ 1) :
    captureWidth r U ≤ 1 / 16 := by
  linarith [captureWidth_le r U hr1]

theorem captureWidth_radius_le_one_sixtyfourth (r : ℝ) (U : Fin 8 → ℝ) (hr1 : r ≤ 1) :
    rawRadius U * captureWidth r U ≤ 1 / 64 := by
  linarith [captureWidth_radius_le r U hr1]

theorem capture_r_le_width (r : ℝ) (U : Fin 8 → ℝ) (hr : 0 < r)
    (hreg : regular r U) : r ≤ captureWidth r U / 1024 := by
  have hden : 0 < quarticK0 * rawRadius U ^ 5 :=
    mul_pos (by norm_num [quarticK0]) (pow_pos (rawRadius_pos U) 5)
  have hF := one_le_quarticFstar r hr.le U
  have hb : (r * rawRadius U ^ 5) * (1024 * quarticK0) ≤ 1 :=
    (le_div_iff₀ (by norm_num [quarticK0] : (0 : ℝ) < 1024 * quarticK0)).mp hreg
  apply (le_div_iff₀ (by norm_num : (0 : ℝ) < 1024)).mpr
  unfold captureWidth quarticWidth
  apply (le_div_iff₀ hden).mpr
  calc
    _ = (r * rawRadius U ^ 5) * (1024 * quarticK0) := by ring
    _ ≤ 1 := hb
    _ ≤ quarticFstar r U := hF

theorem captureSigma_pos (r : ℝ) (U : Fin 8 → ℝ) (hr : 0 ≤ r) :
    0 < captureSigma r U := by
  unfold captureSigma
  exact mul_pos (mul_pos (by norm_num) (rawRadius_pos U)) (captureWidth_pos r U hr)

theorem captureSigma_le (r : ℝ) (U : Fin 8 → ℝ) (hr1 : r ≤ 1) :
    captureSigma r U ≤ 1 / 512 := by
  unfold captureSigma
  linarith [captureWidth_radius_le r U hr1]

theorem four_captureWidth_le_captureSigma (r : ℝ) (U : Fin 8 → ℝ) (hr : 0 ≤ r) :
    4 * captureWidth r U ≤ captureSigma r U := by
  have h := mul_le_mul_of_nonneg_right (rawRadius_one_le U) (captureWidth_pos r U hr).le
  unfold captureSigma
  nlinarith

end I4QuarticCaptureAlgebra
