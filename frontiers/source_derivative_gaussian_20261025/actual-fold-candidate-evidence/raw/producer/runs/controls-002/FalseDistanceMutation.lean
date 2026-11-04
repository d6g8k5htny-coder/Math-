import SourceActualFoldCandidate

noncomputable section
set_option autoImplicit false
open UniversalLaw.Spec.Lifetime I4SourceActualFoldCandidate

/-- Sole mutation: deleting r<L/2 falsely claims the distance equals every
positive real lift separation. The actual L=1,r=1 parent lattice infimum is zero. -/
theorem false_drop_small_radius :
    ∀ {L r : ℝ}, 0 < L → 0 < r →
      torusDist 2 L (endpointLiftM r) (endpointLiftS r) = r := by
  intro L r hL hr
  by_cases hsmall : r < L/2
  · exact endpoint_lifts_torusDist hL hr hsmall
  · have hcounterexample := endpoint_lifts_torusDist_unit_ne_radius
    have hzero := endpoint_lifts_torusDist_unit_zero
    have _keep_counterexample := hcounterexample
    have _keep_zero := hzero
    exact False.elim (by trace_state)
