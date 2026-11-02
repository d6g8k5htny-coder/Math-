import SourceWeightedCurvatureBound
open I4ScalarProductCurvature
example : |(100 : ℝ)| ≤ 1*(1*(1+1*1))^5*(1/100)*1^5 := by
  have hdom : (101 : ℝ) ≤ 1*(|100|+1) := by norm_num
  have hslab : |(100 : ℝ)| ≤ 1*(1/100)*101^5 := by norm_num
  have hS : (1 : ℝ) ≤ 1 := le_rfl
  norm_num
