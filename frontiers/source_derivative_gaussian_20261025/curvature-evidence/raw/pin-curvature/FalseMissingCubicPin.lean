import SourcePinCurvatureBounds
open I4SourcePinCurvatureBounds
-- The constant function three is continuous and 0-Lipschitz, but does not
-- satisfy cubic pin two. Omitting that essential premise would give this
-- false zero-error conclusion, even at positive nonunit radius.
example : |(fun _ : ℝ => (3:ℝ)) ((2:ℝ)*0) - 2| ≤ (2:ℝ)*0 := by
  norm_num
