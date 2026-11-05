import SourcePinCurvatureBounds
open I4SourcePinCurvatureBounds
-- The identity is 1-Lipschitz. Dropping nonnegative radius from the center
-- error estimate would assert a negative upper bound for a positive error.
example : |(fun t : ℝ => t) ((-2:ℝ)*(1/2)) - (fun t : ℝ => t) 0| ≤
    (-2:ℝ)*1/2 := by
  norm_num
