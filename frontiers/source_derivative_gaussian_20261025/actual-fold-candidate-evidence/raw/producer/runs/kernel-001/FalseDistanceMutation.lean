import SourceActualFoldCandidate

noncomputable section
set_option autoImplicit false
open UniversalLaw.Spec.Lifetime I4SourceActualFoldCandidate

/-- Specialized false consequence of deleting r<L/2 from the literal distance
claim. The retained positive L=1,r=1 wraps through one full parent period. -/
theorem false_drop_small_radius :
    torusDist 2 1 (endpointLiftM 1) (endpointLiftS 1) = 1 := by
  have hcounterexample := endpoint_lifts_torusDist_unit_ne_radius
  have hzero := endpoint_lifts_torusDist_unit_zero
  rw [hzero]
  norm_num
