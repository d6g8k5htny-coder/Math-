import GapMorseDistinctControls

open GapMorseDistinctControls

example :
    ((control59_B control59_xStar
      (fderiv ℝ control59_theta control59_xStar control59_eX)) 0 =
      (-(fderiv ℝ control59_g control59_xStar control59_eX)) 0) := by
  rw [dropped_DBtheta_eq_iff_false]
