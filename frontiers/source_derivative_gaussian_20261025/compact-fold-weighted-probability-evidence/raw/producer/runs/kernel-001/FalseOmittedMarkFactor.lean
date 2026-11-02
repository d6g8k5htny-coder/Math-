import Controls

open CompactFoldWeightedControls

/-- Deliberately false inclusion suppressing 6*k1 at the proved scalar witness. -/
theorem omitted_mark_factor_mutation :
    ¬ (((1:ℝ)/1000000000)*(16*1)^5 ≤ 1/100 ∧
      1024*(16*1)^5 ≤ -(-5:ℝ)/(6*2*((1:ℝ)/1000000000))) →
      ((1:ℝ)/(100*16^5) < ((1:ℝ)/1000000000)*1^5 ∨
        -(1024*(16:ℝ)^5)*((1:ℝ)/1000000000)*1^5 ≤ -5) := by
  have proved_counterexample := second_cutoff_failure_witness
  norm_num
