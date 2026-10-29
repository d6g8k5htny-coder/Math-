import IntrinsicProbabilityControls

open UniversalLaw.Spec.Lifetime TorusFiltration IntrinsicProbabilityControls

/- Sole mutation: delete the empty-cut branch of the new guarded-death
upper-preimage formula, at the concrete zero norm-BCF and level-1. The passed
control separately proves the left membership and excludes the right one. -/
theorem mutated_missing_empty_branch :
    ((-1 : ℝ) < superlevelBar_deathHeight (zeroBCF : E 2 → ℝ) 0 ↔
      (-1 : ℝ) ∈ superlevelBar_clearanceSet (zeroBCF : E 2 → ℝ) 0) := by
  simp only [zero_bcf_mutation_counterexample.1, zero_bcf_mutation_counterexample.2, true_iff]
