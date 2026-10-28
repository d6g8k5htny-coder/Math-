import SaddleUppercutsControls

example : ActualSaddleUppercutsControls.nonnegativeUpperMutation := by
  rw [show ActualSaddleUppercutsControls.nonnegativeUpperMutation ↔ False from
    ⟨ActualSaddleUppercutsControls.nonnegativeUpperMutation_false, fun h => h.elim⟩]
