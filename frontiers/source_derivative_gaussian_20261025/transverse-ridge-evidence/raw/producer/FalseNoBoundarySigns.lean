import BoundarySignControl

open Set
open AdaptiveFoldTransverseRidge AdaptiveFoldTransverseRidgeControls

-- Expected mathematical rejection: the actual zero y=3 lies outside [-1,1].
-- C4 regularity, strict Gy=-1 and the positive lower sign all hold, as proved
-- in boundary_signs_are_substantive. Omitting the upper boundary sign is false.
example : ∃ y ∈ Icc (-(1 : ℝ)) 1, Vy negativeV (0, y) = 0 := by
  refine ⟨3, ?_, ?_⟩
  · norm_num
  · rw [negativeV_Vy]
    norm_num
