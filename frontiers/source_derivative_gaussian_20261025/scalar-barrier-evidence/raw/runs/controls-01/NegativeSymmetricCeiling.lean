import Controls

open AdaptiveFoldScalar AdaptiveFoldScalarControls

/-- Deliberately false mutation: extend the valid asymmetric ceiling to all J.
The obstruction is the concrete boundary inequality 3/4 ≤ 1/12. -/
theorem false_full_symmetric_ceiling :
    ∀ x ∈ J, canonicalPhi x ≤ canonicalPhi (-(1 / 2 : ℝ)) := by
  have hbad : canonicalPhi (3 / 2 : ℝ) ≤ canonicalPhi (-(1 / 2 : ℝ)) := by
    norm_num [canonicalPhi]
  exact False.elim ((not_le_of_gt canonical_symmetric_violation) hbad)
