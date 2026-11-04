import SourceTwoRemoteFirstJetWitness
import Lean.Elab.Tactic.Omega

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix
open I4Source I4Weights I4SourceConfluentPins I4SourceRawPinConditioning
open I4SourceFinitePinKernel I4SourceRemoteJetWitness I4SourceTwoRemoteFirstJetWitness

namespace TwoRemoteFirstJetControls

private theorem unit_circle_ne (L : ℝ) (hL : L=2 ∨ L= -2) :
    ((1:ℝ):AddCircle L) ≠ 0 := by
  intro h
  obtain ⟨n,hn⟩ := (AddCircle.coe_eq_zero_iff (p:=L)).mp h
  have hex : ∃ k : ℤ, (k:ℝ)*2=1 := by
    rcases hL with rfl|rfl
    · exact ⟨n,by simpa only [zsmul_eq_mul] using hn⟩
    · refine ⟨-n,?_⟩
      have hh : (n:ℝ)*(-2)=1 := by simpa only [zsmul_eq_mul] using hn
      push_cast
      linarith
  obtain ⟨k,hk⟩ := hex
  have hkZ : k*(2:ℤ)=1 := by exact_mod_cast hk
  omega

private theorem half_circle_ne : ((1/2:ℝ):AddCircle (2:ℝ)) ≠ 0 := by
  intro h
  obtain ⟨n,hn⟩ := (AddCircle.coe_eq_zero_iff (p:=(2:ℝ))).mp h
  have hh : (n:ℝ)*2=1/2 := by simpa only [zsmul_eq_mul] using hn
  have h4 : (n:ℝ)*4=1 := by linarith
  have h4Z : n*(4:ℤ)=1 := by exact_mod_cast h4
  omega

private theorem ne_from_coordinate (L : ℝ) (x y : Fin 2 → ℝ) (j : Fin 2)
    (h : (((x j-y j):ℝ):AddCircle L) ≠ 0) :
    I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L y := by
  intro hxy
  apply h
  rw [AddCircle.coe_sub,sub_eq_zero]
  exact congrFun hxy j

private theorem repeated_separations (L : ℝ) (hL : L=2 ∨ L= -2) :
    I4Torus.torusProjection 2 L ![1,0] ≠ I4Torus.torusProjection 2 L (endpointM 0) ∧
    I4Torus.torusProjection 2 L ![1,0] ≠ I4Torus.torusProjection 2 L (endpointS 0) ∧
    I4Torus.torusProjection 2 L ![0,1] ≠ I4Torus.torusProjection 2 L (endpointM 0) ∧
    I4Torus.torusProjection 2 L ![0,1] ≠ I4Torus.torusProjection 2 L (endpointS 0) ∧
    I4Torus.torusProjection 2 L ![1,0] ≠ I4Torus.torusProjection 2 L ![0,1] := by
  refine ⟨?_,?_,?_,?_,?_⟩
  · apply ne_from_coordinate L _ _ 0
    simpa [endpointM] using unit_circle_ne L hL
  · apply ne_from_coordinate L _ _ 0
    simpa [endpointS] using unit_circle_ne L hL
  · apply ne_from_coordinate L _ _ 1
    simpa [endpointM] using unit_circle_ne L hL
  · apply ne_from_coordinate L _ _ 1
    simpa [endpointS] using unit_circle_ne L hL
  · apply ne_from_coordinate L _ _ 0
    simpa using unit_circle_ne L hL

/-- Actual internally constructed directions, all36 raw and36 joint-observation pairings. -/
theorem actual_repeated_pin_witnesses :
    ∃ v : Fin 6 → (SourceMode 2 →₀ ℝ),
      (∀ i s, finitePairing (rawPinCoefficient 2 0 i) (v s)=0) ∧
      (∀ j s, finitePairing (twoRemoteFirstJetCoefficient 2 ![1,0] ![0,1] j) (v s)=if j=s then 1 else 0) := by
  have h := repeated_separations 2 (Or.inl rfl)
  exact actual_finite_twoRemoteFirstJet_witnesses (by norm_num) 0 ![1,0] ![0,1]
    h.1 h.2.1 h.2.2.1 h.2.2.2.1 h.2.2.2.2

/-- Literal noninterleaved order valueX,dxX,dyX,valueY,dxY,dyY. -/
theorem literal_row_order (L : ℝ) (x y : Fin 2 → ℝ) :
    twoRemoteFirstJetCoefficient L x y =
      ![remoteJetCoefficient L x 0,remoteJetCoefficient L x 1,remoteJetCoefficient L x 2,
        remoteJetCoefficient L y 0,remoteJetCoefficient L y 1,remoteJetCoefficient L y 2] := rfl

/-- Six distinct target entries are realized by the actual original finite directions. -/
theorem actual_target_vector :
    ∃ w : SourceMode 2 →₀ ℝ,
      (∀ i, finitePairing (rawPinCoefficient 2 0 i) w=0) ∧
      (∀ j, finitePairing (twoRemoteFirstJetCoefficient 2 ![1,0] ![0,1] j) w= ![1,2,3,4,5,6] j) := by
  classical
  obtain ⟨v,hker,hright⟩ := actual_repeated_pin_witnesses
  have hp (a : SourceMode 2 → ℝ) (z : SourceMode 2 →₀ ℝ) :
      finitePairing a z=Finsupp.linearCombination ℝ a z := by
    simp [finitePairing,Finsupp.linearCombination_apply,Finsupp.sum,smul_eq_mul,mul_comm]
  refine ⟨∑ s : Fin 6, (![1,2,3,4,5,6] s : ℝ) • v s,?_,?_⟩
  · intro i
    simp_rw [hp]
    rw [map_sum]
    simp_rw [map_smul,← hp]
    simp [hker]
  · intro j
    simp_rw [hp]
    rw [map_sum]
    simp_rw [map_smul,← hp]
    simp [hright,smul_eq_mul]

/-- Original signed negative period, with the same admissible repeated pins. -/
theorem actual_negative_period_witnesses :
    ∃ v : Fin 6 → (SourceMode 2 →₀ ℝ),
      (∀ i s, finitePairing (rawPinCoefficient (-2) 0 i) (v s)=0) ∧
      (∀ j s, finitePairing (twoRemoteFirstJetCoefficient (-2) ![1,0] ![0,1] j) (v s)=if j=s then 1 else 0) := by
  have h := repeated_separations (-2) (Or.inr rfl)
  exact actual_finite_twoRemoteFirstJet_witnesses (by norm_num) 0 ![1,0] ![0,1]
    h.1 h.2.1 h.2.2.1 h.2.2.2.1 h.2.2.2.2

private theorem negative_radius_separations :
    I4Torus.torusProjection 2 2 ![0,0] ≠ I4Torus.torusProjection 2 2 (endpointM (-1)) ∧
    I4Torus.torusProjection 2 2 ![0,0] ≠ I4Torus.torusProjection 2 2 (endpointS (-1)) ∧
    I4Torus.torusProjection 2 2 ![0,1] ≠ I4Torus.torusProjection 2 2 (endpointM (-1)) ∧
    I4Torus.torusProjection 2 2 ![0,1] ≠ I4Torus.torusProjection 2 2 (endpointS (-1)) ∧
    I4Torus.torusProjection 2 2 ![0,0] ≠ I4Torus.torusProjection 2 2 ![0,1] := by
  refine ⟨?_,?_,?_,?_,?_⟩
  · apply Ne.symm
    apply ne_from_coordinate 2 _ _ 0
    simpa [endpointM] using half_circle_ne
  · apply ne_from_coordinate 2 _ _ 0
    simpa [endpointS] using half_circle_ne
  · apply ne_from_coordinate 2 _ _ 1
    simpa [endpointM] using unit_circle_ne 2 (Or.inl rfl)
  · apply ne_from_coordinate 2 _ _ 1
    simpa [endpointS] using unit_circle_ne 2 (Or.inl rfl)
  · apply Ne.symm
    apply ne_from_coordinate 2 _ _ 1
    simpa using unit_circle_ne 2 (Or.inl rfl)

/-- Negative radius retains its literal swapped endpoints. -/
theorem actual_negative_radius_witnesses :
    ∃ v : Fin 6 → (SourceMode 2 →₀ ℝ),
      (∀ i s, finitePairing (rawPinCoefficient 2 (-1) i) (v s)=0) ∧
      (∀ j s, finitePairing (twoRemoteFirstJetCoefficient 2 ![0,0] ![0,1] j) (v s)=if j=s then 1 else 0) := by
  have h := negative_radius_separations
  exact actual_finite_twoRemoteFirstJet_witnesses (by norm_num) (-1) ![0,0] ![0,1]
    h.1 h.2.1 h.2.2.1 h.2.2.2.1 h.2.2.2.2

/-- Actual residual Gram at zero correction, without a pin inverse. -/
theorem zero_correction_posDef :
    (I4ContactGram.coefficientGram (residualCoefficient (rawPinCoefficient 2 0)
      (twoRemoteFirstJetCoefficient 2 ![1,0] ![0,1]) (0 : Matrix (Fin 6) (Fin 6) ℝ))).PosDef := by
  have h := repeated_separations 2 (Or.inl rfl)
  exact actual_twoRemoteFirstJet_residual_coefficientGram_posDef (by norm_num) 0 ![1,0] ![0,1]
    h.1 h.2.1 h.2.2.1 h.2.2.2.1 h.2.2.2.2 _

/-- The same actual residual object accepts a nonzero nonsymmetric6×6 correction. -/
theorem nonsymmetric_correction_posDef :
    (I4ContactGram.coefficientGram (residualCoefficient (rawPinCoefficient 2 0)
      (twoRemoteFirstJetCoefficient 2 ![1,0] ![0,1])
      (fun j i => ((j.val+1:ℕ):ℝ)*((i.val+2:ℕ):ℝ)))).PosDef := by
  have h := repeated_separations 2 (Or.inl rfl)
  exact actual_twoRemoteFirstJet_residual_coefficientGram_posDef (by norm_num) 0 ![1,0] ![0,1]
    h.1 h.2.1 h.2.2.1 h.2.2.2.1 h.2.2.2.2 _

/-- At the collision all four remote/pin separations still hold exactly. -/
theorem collision_retained_separations :
    I4Torus.torusProjection 2 2 ![1,0] ≠ I4Torus.torusProjection 2 2 (endpointM 0) ∧
    I4Torus.torusProjection 2 2 ![1,0] ≠ I4Torus.torusProjection 2 2 (endpointS 0) ∧
    I4Torus.torusProjection 2 2 ![1,0] ≠ I4Torus.torusProjection 2 2 (endpointM 0) ∧
    I4Torus.torusProjection 2 2 ![1,0] ≠ I4Torus.torusProjection 2 2 (endpointS 0) := by
  have h := repeated_separations 2 (Or.inl rfl)
  exact ⟨h.1,h.2.1,h.1,h.2.1⟩

/-- Actual coincident value rows0 and3 rule out the claimed joint right inverse. -/
theorem collision_no_witnesses :
    ¬ ∃ v : Fin 6 → (SourceMode 2 →₀ ℝ),
      (∀ i s, finitePairing (rawPinCoefficient 2 0 i) (v s)=0) ∧
      (∀ j s, finitePairing (twoRemoteFirstJetCoefficient 2 ![1,0] ![1,0] j) (v s)=if j=s then 1 else 0) := by
  rintro ⟨v,_hker,hright⟩
  have h0 := hright 0 0
  have h3 := hright 3 0
  have he : twoRemoteFirstJetCoefficient 2 ![1,0] ![1,0] 0 =
      twoRemoteFirstJetCoefficient 2 ![1,0] ![1,0] 3 := rfl
  rw [he] at h0
  norm_num at h0 h3
  have hh : (1:ℝ)=0 := h0.symm.trans h3
  norm_num at hh

end TwoRemoteFirstJetControls
