import SourcePinPreservingQuartic
-- Replacing the required maximum C1 norm by the sum would require this
-- false numeric inequality. This canary must fail at an unsolved False goal.
example : (683/480 : ℝ)+(2623/960 : ℝ) ≤ 3 := by
  norm_num
