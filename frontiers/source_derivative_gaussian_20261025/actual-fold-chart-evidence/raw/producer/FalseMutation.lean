import Controls

open ActualFoldChartControls AdaptiveFoldTransverseRidge MeasureTheory
open scoped Interval

/-- This false mutation deliberately drops factor6k from the normalized chart. -/
example : (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), (3/2-6*u^2) *
    (fderiv ℝ (fderiv ℝ (Vx omittedFactorPotential)) (u,0) ex ex)) = 2 := by
  rw [omittedFactor_average]
  norm_num
