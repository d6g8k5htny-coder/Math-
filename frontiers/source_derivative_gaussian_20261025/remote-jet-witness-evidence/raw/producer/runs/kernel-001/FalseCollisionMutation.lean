import Controls

noncomputable section
set_option autoImplicit false
open I4SourceRemoteJetWitness I4SourceFinitePinKernel I4Source
open I4SourceConfluentPins I4SourceRawPinConditioning

/-- Sole mutation: retain hL and the VALID other-pin quotient separation but
omit only hxM at x=M. The passed control proved this actual witness assertion
impossible by literal pinrow0=remotevaluerow, hence0=1. -/
theorem false_drop_only_hxM (_hL : (2:ℝ) ≠ 0)
    (_hxS : I4Torus.torusProjection 2 2 (endpointM 1) ≠
      I4Torus.torusProjection 2 2 (endpointS 1)) :
    ∃ v : Fin 6 → (SourceMode 2 →₀ ℝ),
      (∀ i s, finitePairing (rawPinCoefficient 2 1 i) (v s) = 0) ∧
      (∀ j s, finitePairing (remoteJetCoefficient 2 (endpointM 1) j) (v s) = if j=s then 1 else 0) := by
  have hretained_separation := RemoteJetControls.collision_retained_separation
  have hcounterexample := RemoteJetControls.collision_no_witness
  simp only [hcounterexample]
