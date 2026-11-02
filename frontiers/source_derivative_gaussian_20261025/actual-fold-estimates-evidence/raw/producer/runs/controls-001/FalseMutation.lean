import SourceAdaptiveFoldEstimates
open AdaptiveFoldBoundaryPath

-- Deliberately omit only the large-kappa cutoff and claim the resulting false budget.
example : 1 + profileError (1/2) 3 1 ≤ 2-3*(1/100 : ℝ)*1 := by
  norm_num [profileError, accelerationRadius]
