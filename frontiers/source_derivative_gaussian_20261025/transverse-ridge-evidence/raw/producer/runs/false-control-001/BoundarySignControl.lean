import Controls

open Set
open scoped Topology ContDiff
namespace AdaptiveFoldTransverseRidgeControls
open AdaptiveFoldTransverseRidge

theorem negativeV_c4 : ContDiff ℝ 4 negativeV := by unfold negativeV; fun_prop

theorem negativeV_upper_sign_fails (x : ℝ) : Vy negativeV (x, 1) = 2 := by
  rw [negativeV_Vy]
  norm_num

/-- Same regularity and strict negative second vertical partial as in the
construction, but no root: the strict upper boundary sign is indispensable. -/
theorem boundary_signs_are_substantive :
    ContDiff ℝ 4 negativeV ∧
    (∀ p : ℝ × ℝ, partialY (Vy negativeV) p ≤ -(1 : ℝ)) ∧
    (∀ x : ℝ, 0 < Vy negativeV (x, -1)) ∧
    (∀ x : ℝ, ¬ ∃ y ∈ Icc (-(1 : ℝ)) 1, Vy negativeV (x, y) = 0) := by
  refine ⟨negativeV_c4, ?_, ?_, negativeV_no_root⟩
  · intro p; rw [negativeV_strict_vertical]
  · intro x; rw [negativeV_Vy]; norm_num

end AdaptiveFoldTransverseRidgeControls
