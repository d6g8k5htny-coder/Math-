import Controls

open I4Source I4SourceRawPinConditioning I4SourceFinitePinKernel
open I4SourceTwoRemoteFirstJetWitness TwoRemoteFirstJetControls

-- Sole mutation omits only hxy. All four retained quotient separations are proved in Controls.
example : ∃ v : Fin 6 → (SourceMode 2 →₀ ℝ),
    (∀ i s, finitePairing (rawPinCoefficient 2 0 i) (v s)=0) ∧
    (∀ j s, finitePairing (twoRemoteFirstJetCoefficient 2 ![1,0] ![1,0] j) (v s)=if j=s then 1 else 0) := by
  simp only [collision_no_witnesses]
