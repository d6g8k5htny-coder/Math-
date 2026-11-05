import AllTargetResidualControls

noncomputable section
set_option autoImplicit false

/-- Sole mutation: the false arithmetic step deleting polynomial target growth.
It does not assert a counterexample to every possible uniform residual bound. -/
theorem false_target_growth_erasure :
    (1+‖(fun _ : Fin 6 => (3:ℝ))‖)^1 ≤ (1:ℝ) := by
  have hcounterexample := AllTargetResidualControls.target_growth_erasure_counterexample
  rw [AllTargetResidualControls.constant_three_norm]
  norm_num
