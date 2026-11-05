import OlderClearanceControls

open SourceActualFoldTorus OlderClearanceControls

/- Sole false strict-margin mutation, restricted to its concrete actual case.
Positive controls already prove both the actual weak H0-map witness at0 and
the strict-clearance obstruction at the starting path point. -/
theorem mutant_identity_forward :
    relaxedOlderClearance ℝ (id : ℝ → ℝ) 0 0 →
      (0 : ℝ) ∈ strictClearanceSet (id : ℝ → ℝ) 0 := by
  simp only [relaxed_actual_at_zero, identity_no_strict_clearance_at_zero, true_implies]
