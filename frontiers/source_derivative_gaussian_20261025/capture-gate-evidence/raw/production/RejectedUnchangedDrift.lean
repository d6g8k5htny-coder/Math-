import SourceQuarticCaptureAlgebra

-- P=-3, permitted error=1/4: the actual drift is -11/4, larger than -3.
example : (-3 : ℝ)+1/4 ≤ -3 := by
  norm_num
