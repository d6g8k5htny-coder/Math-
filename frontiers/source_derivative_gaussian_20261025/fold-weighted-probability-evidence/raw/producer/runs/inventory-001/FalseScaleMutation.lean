import Controls

open FoldWeightedControls

/-- Deliberately false omitted-8^5 inclusion at the proved counterexample. -/
theorem omitted_scale_mutation :
    ¬ ((1:ℝ)/100000000 * (16*1)^5 ≤ 1/100 ∧
      1024*(16*1)^5 ≤ -(-100:ℝ)/((1:ℝ)/100000000)) →
    ((1:ℝ)/(100*2^5) < (1:ℝ)/100000000*1^5 ∨
      -(1024*(16:ℝ)^5)*((1:ℝ)/100000000)*1^5 ≤ -100) := by
  have proved_counterexample := omitted_scale_counterexample
  norm_num
