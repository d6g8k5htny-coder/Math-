import SourcePinCurvatureBounds

/-! New fifth-order symmetric Peano calculations for the actual quartic
transfer candidate. Generic remainder hypotheses below are explicit; this
does not itself prove the actual source's Taylor remainder or capture. -/

noncomputable section
open MeasureTheory Set I4SourceConfluentLimits I4PeanoErrorBounds
open scoped Interval
set_option autoImplicit false

namespace I4ActualQuarticTransfer

theorem peanoCubic_first_moment :
    (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * u) = 0 := by
  have heq : (fun u : ℝ => peanoCubic u * u) = (fun u => (1/4 : ℝ) * u - u^3) := by
    funext u
    unfold peanoCubic
    ring
  have hi1 : IntervalIntegrable (fun u : ℝ => (1/4 : ℝ)*u) volume (-1/2 : ℝ) (1/2 : ℝ) := by
    apply Continuous.intervalIntegrable
    fun_prop
  have hi2 : IntervalIntegrable (fun u : ℝ => u^3) volume (-1/2 : ℝ) (1/2 : ℝ) :=
    (continuous_id.pow 3).intervalIntegrable _ _
  rw [heq, intervalIntegral.integral_sub hi1 hi2, intervalIntegral.integral_const_mul]
  norm_num [integral_id, integral_pow]

theorem peanoCubic_normalized_second_moment :
    6 * (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * u^2) = 1/20 := by
  have heq : (fun u : ℝ => peanoCubic u * u^2) =
      (fun u => (1/4 : ℝ) * u^2 - u^4) := by
    funext u
    unfold peanoCubic
    ring
  have hi1 : IntervalIntegrable (fun u : ℝ => (1/4 : ℝ)*u^2) volume (-1/2 : ℝ) (1/2 : ℝ) := by
    apply Continuous.intervalIntegrable
    fun_prop
  have hi2 : IntervalIntegrable (fun u : ℝ => u^4) volume (-1/2 : ℝ) (1/2 : ℝ) :=
    (continuous_id.pow 4).intervalIntegrable _ _
  rw [heq, intervalIntegral.integral_sub hi1 hi2, intervalIntegral.integral_const_mul]
  norm_num [integral_pow]

theorem symmetric_cubic_pin_second_order (g : ℝ → ℝ) (hgc : Continuous g)
    (r t c G : ℝ) (_hG : 0 ≤ G)
    (hpin : 6 * (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * g (r*u)) = 2)
    (hrem : ∀ u ∈ Icc (-1/2 : ℝ) (1/2 : ℝ),
      |g (r*u) - t - r*u*c| ≤ G*r^2*u^2/2) :
    |t-2| ≤ G*r^2/40 := by
  let f : ℝ → ℝ := fun u => g (r*u)-t-r*u*c
  have hcK : Continuous peanoCubic := by unfold peanoCubic; fun_prop
  have hcf : Continuous f := by dsimp [f]; fun_prop
  have hcg : Continuous (fun u => g (r*u)) := by fun_prop
  have hmass : (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u) = 1/6 := by
    linarith [peano_kernel_masses.2.2.2]
  have hmom : (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * u^2) = 1/120 := by
    linarith [peanoCubic_normalized_second_moment]
  have hlinear : (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * (r*u*c)) = 0 := by
    calc
      _ = (r*c) * ∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * u := by
        rw [← intervalIntegral.integral_const_mul]
        congr 1
        funext u
        ring
      _ = 0 := by rw [peanoCubic_first_moment]; ring
  have heq : 6 * (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * f u) = 2-t := by
    dsimp [f]
    simp_rw [mul_sub]
    have hi1 : IntervalIntegrable (fun u => peanoCubic u * g (r*u)) volume
        (-1/2 : ℝ) (1/2 : ℝ) := (hcK.mul hcg).intervalIntegrable _ _
    have hi2 : IntervalIntegrable (fun u => peanoCubic u * t) volume
        (-1/2 : ℝ) (1/2 : ℝ) := (hcK.mul continuous_const).intervalIntegrable _ _
    have hi3 : IntervalIntegrable (fun u => peanoCubic u * (r*u*c)) volume
        (-1/2 : ℝ) (1/2 : ℝ) := by
      apply Continuous.intervalIntegrable
      fun_prop
    have hi12 : IntervalIntegrable (fun u => peanoCubic u * g (r*u)-peanoCubic u*t)
        volume (-1/2 : ℝ) (1/2 : ℝ) := hi1.sub hi2
    rw [intervalIntegral.integral_sub hi12 hi3, intervalIntegral.integral_sub hi1 hi2,
      intervalIntegral.integral_mul_const, hmass, hlinear]
    linarith [hpin]
  have hbound : |∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * f u| ≤ G*r^2/240 := by
    calc
      _ ≤ ∫ u in (-1/2 : ℝ)..(1/2 : ℝ), |peanoCubic u * f u| :=
        intervalIntegral.abs_integral_le_integral_abs (by norm_num)
      _ ≤ ∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * (G*r^2*u^2/2) := by
        apply intervalIntegral.integral_mono_on (by norm_num)
          ((hcK.mul hcf).abs.intervalIntegrable _ _)
          ((hcK.mul (by fun_prop)).intervalIntegrable _ _)
        intro u hu
        change |peanoCubic u * f u| ≤ peanoCubic u * (G*r^2*u^2/2)
        rw [abs_mul, abs_of_nonneg (peanoCubic_nonneg u hu)]
        exact mul_le_mul_of_nonneg_left (hrem u hu) (peanoCubic_nonneg u hu)
      _ = (G*r^2/2) * ∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u*u^2 := by
        rw [← intervalIntegral.integral_const_mul]
        congr 1
        funext u
        ring
      _ = G*r^2/240 := by rw [hmom]; ring
  have habs : |t-2| = 6 * |∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * f u| := by
    rw [abs_sub_comm, ← heq, abs_mul]
    norm_num
  rw [habs]
  linarith [hbound]

end I4ActualQuarticTransfer
