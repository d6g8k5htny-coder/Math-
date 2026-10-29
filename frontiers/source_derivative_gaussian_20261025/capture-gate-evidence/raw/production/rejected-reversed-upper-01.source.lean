import SourceQuarticCaptureAlgebra

-- An upper inward vector with zero error has negative transverse component.
example : (0 : ℝ) ≤ -1+0 := by
  norm_num
