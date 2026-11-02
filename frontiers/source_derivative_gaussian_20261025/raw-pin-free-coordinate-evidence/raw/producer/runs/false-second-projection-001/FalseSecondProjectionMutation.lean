import FreeCoordinateControls

open FreeCoordinateControls I4SourceRawPinConditioning

example :
    (rawPosteriorSample (by norm_num : (2 : ℝ) ≠ 0) 0 0 control57_omega1).val
      control57_mC = control57_mutantReconstruction.val control57_mC := by
  rw [control57_mutant_equality_iff_false]
