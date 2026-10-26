import SourceRemoteJetWitness

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix
open I4SourceRemoteJetWitness I4SourceFinitePinKernel I4SourceFiniteTrig
open I4Source I4Weights I4SourceConfluentPins I4SourceRawPinConditioning
open I4SourceDerivativeGaussian I4SourceConfluentLimits

open Lean in
macro "remotePrivate%" n:ident : term => do
  let pref := Lean.Name.str (Lean.Name.num `_private.SourceRemoteJetWitness 0) "I4SourceRemoteJetWitness"
  return Lean.mkIdent (pref ++ n.getId)

namespace RemoteJetControls

/-- All36 identity-germ entries hold at every translated center. -/
theorem all_germ_entries (c : ℝ) (hc : c ≠ 0) (x : Fin 2 → ℝ) :
    ∀ j s : Fin 6, jet2 (localGerm c x s) x j = if j=s then 1 else 0 :=
  localGerm_jet2 c hc x

/-- The mixed germ has mixed entryone and every other ordinary derivative entryzero. -/
theorem translated_mixed_germ :
    jet2 (localGerm 2 ![3,-1] 4) ![3,-1] = ![0,0,0,0,1,0] := by
  ext j
  rw [localGerm_jet2 2 (by norm_num)]
  fin_cases j <;> norm_num

/-- Actual smooth product jets retain the puresecondfactor2 and mixedcrossfactor1. -/
theorem actual_product_coefficients (P Q : (Fin 2 → ℝ) → ℝ)
    (hP : ContDiff ℝ 2 P) (hQ : ContDiff ℝ 2 Q) (x : Fin 2 → ℝ) :
    jet2 (fun y => P y*Q y) x 3 =
      jet2 P x 3*jet2 Q x 0+2*jet2 P x 1*jet2 Q x 1+jet2 P x 0*jet2 Q x 3 ∧
    jet2 (fun y => P y*Q y) x 4 =
      jet2 P x 4*jet2 Q x 0+jet2 P x 1*jet2 Q x 2+
        jet2 P x 2*jet2 Q x 1+jet2 P x 0*jet2 Q x 4 := by
  rw [jet2_mul P Q hP hQ]
  exact ⟨rfl,rfl⟩

/-- Nontrivial scalar rows independently exercise both multiplicities. -/
theorem scalar_product_entries :
    mulJet2 ![2,3,5,7,11,13] ![17,19,23,29,31,37] 3 = 291 ∧
    mulJet2 ![2,3,5,7,11,13] ![17,19,23,29,31,37] 4 = 413 ∧
    mulJet2 ![2,3,5,7,11,13] ![17,19,23,29,31,37] 5 = 525 := by
  norm_num [mulJet2]

private def affineP (y : Fin 2 → ℝ) : ℝ := 2+y 0+y 1

/-- Nonconstant multiplier with both first derivativesone and a second-order target. -/
theorem nonconstant_interpolation :
    jet2 (interpolant 2 0 affineP ![3,5,7,11,13,17]) 0 = ![3,5,7,11,13,17] := by
  apply jet2_interpolate_mul 2 (by norm_num) 0 affineP
  · unfold affineP
    fun_prop
  · norm_num [affineP]

/-- The multiplier used above really has two nonzero first derivatives. -/
theorem affineP_nonzero_first :
    fderiv ℝ affineP 0 directionX = 1 ∧ fderiv ℝ affineP 0 directionY = 1 := by
  have h : HasFDerivAt (𝕜 := ℝ) affineP
      ((ContinuousLinearMap.proj (0 : Fin 2) : (Fin 2 → ℝ) →L[ℝ] ℝ) + ContinuousLinearMap.proj (1 : Fin 2)) 0 := by
    simpa only [zero_add] using
      (((hasFDerivAt_const (2:ℝ) (0 : Fin 2 → ℝ)).add (hasFDerivAt_apply (0 : Fin 2) (0 : Fin 2 → ℝ))).add
        (hasFDerivAt_apply (1 : Fin 2) (0 : Fin 2 → ℝ)))
  rw [h.fderiv]
  norm_num [directionX,directionY]

/-- A constant multiplier2 separately checks the denominator/amplitude normalization. -/
theorem constant_two_interpolation :
    jet2 (interpolant 2 ![3,-1] (fun _ => 2) ![3,5,7,11,13,17]) ![3,-1] =
      ![3,5,7,11,13,17] :=
  jet2_interpolate_mul 2 (by norm_num) _ _ contDiff_const (by norm_num) _

/-- Concrete represented squared factors annihilate actual values and full derivatives. -/
theorem represented_pin_annihilation :
    let F := eval 2 ((remotePrivate% annihilatorPoly) 2 1 0 0)
    F (endpointM 1) = 0 ∧ F (endpointS 1) = 0 ∧
      fderiv ℝ F (endpointM 1) = 0 ∧ fderiv ℝ F (endpointS 1) = 0 := by
  have he : eval 2 ((remotePrivate% annihilatorPoly) 2 1 0 0) =
      (remotePrivate% annihilator) 2 1 0 0 :=
    funext ((remotePrivate% eval_annihilatorPoly) 2 1 0 0)
  dsimp only
  rw [he]
  exact ⟨((remotePrivate% annihilator_pin_values) 2 1 0 0).1,
    ((remotePrivate% annihilator_pin_values) 2 1 0 0).2,
    ((remotePrivate% annihilator_pin_derivatives) 2 1 0 0).1,
    ((remotePrivate% annihilator_pin_derivatives) 2 1 0 0).2⟩

private theorem torus_ne_of_cos_ne {L : ℝ} (hL : L ≠ 0) (x p : Fin 2 → ℝ)
    (j : Fin 2) (hc : Real.cos (sourceC L*(x j-p j)) ≠ 1) :
    I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L p := by
  intro h
  exact hc (((remotePrivate% cosine_sourceC_eq_one_iff) hL (x j) (p j)).mpr (congrFun h j))

private theorem separated_M :
    I4Torus.torusProjection 2 2 (0 : Fin 2 → ℝ) ≠
      I4Torus.torusProjection 2 2 (endpointM 1) := by
  apply torus_ne_of_cos_ne (by norm_num) _ _ 0
  have he : sourceC 2*((0 : Fin 2 → ℝ) 0-endpointM 1 0) = Real.pi/2 := by
    dsimp [sourceC,endpointM]
    ring
  rw [he,Real.cos_pi_div_two]
  norm_num

private theorem separated_S :
    I4Torus.torusProjection 2 2 (0 : Fin 2 → ℝ) ≠
      I4Torus.torusProjection 2 2 (endpointS 1) := by
  apply torus_ne_of_cos_ne (by norm_num) _ _ 0
  have he : sourceC 2*((0 : Fin 2 → ℝ) 0-endpointS 1 0) = -(Real.pi/2) := by
    dsimp [sourceC,endpointS]
    ring
  rw [he,Real.cos_neg,Real.cos_pi_div_two]
  norm_num

/-- Actual original-mode witnesses, all36 raw pairings in literal order and all36remote. -/
theorem actual_witness_instance :
    ∃ v : Fin 6 → (SourceMode 2 →₀ ℝ),
      (∀ i s, finitePairing (rawPinCoefficient 2 1 i) (v s) = 0) ∧
      (∀ j s, finitePairing (remoteJetCoefficient 2 0 j) (v s) = if j=s then 1 else 0) :=
  actual_finite_remoteJet_witnesses (by norm_num) 1 0 separated_M separated_S

private theorem repeated_separated :
    I4Torus.torusProjection 2 2 (![1,0] : Fin 2 → ℝ) ≠
      I4Torus.torusProjection 2 2 (endpointM 0) := by
  apply torus_ne_of_cos_ne (by norm_num) _ _ 0
  have he : sourceC 2*((![1,0] : Fin 2 → ℝ) 0-endpointM 0 0) = Real.pi := by
    dsimp [sourceC,endpointM]
    ring
  rw [he,Real.cos_pi]
  norm_num

/-- Repeated pinsr0 need no covarianceinverse or endpoint-distinctness premise. -/
theorem repeated_pin_witnesses :
    ∃ v : Fin 6 → (SourceMode 2 →₀ ℝ),
      (∀ i s, finitePairing (rawPinCoefficient 2 0 i) (v s) = 0) ∧
      (∀ j s, finitePairing (remoteJetCoefficient 2 ![1,0] j) (v s) = if j=s then 1 else 0) := by
  apply actual_finite_remoteJet_witnesses (by norm_num) 0 ![1,0] repeated_separated
  simpa only [endpointM,endpointS,neg_zero,zero_div] using repeated_separated

private theorem negative_separated :
    I4Torus.torusProjection 2 (-2) (![1,0] : Fin 2 → ℝ) ≠
      I4Torus.torusProjection 2 (-2) (endpointM 0) := by
  apply torus_ne_of_cos_ne (by norm_num) _ _ 0
  have he : sourceC (-2)*((![1,0] : Fin 2 → ℝ) 0-endpointM 0 0) = -Real.pi := by
    dsimp [sourceC,endpointM]
    ring
  rw [he,Real.cos_neg,Real.cos_pi]
  norm_num

/-- Negative original period is retained literally. -/
theorem negative_period_witnesses :
    ∃ v : Fin 6 → (SourceMode 2 →₀ ℝ),
      (∀ i s, finitePairing (rawPinCoefficient (-2) 0 i) (v s) = 0) ∧
      (∀ j s, finitePairing (remoteJetCoefficient (-2) ![1,0] j) (v s) = if j=s then 1 else 0) := by
  apply actual_finite_remoteJet_witnesses (by norm_num) 0 ![1,0] negative_separated
  simpa only [endpointM,endpointS,neg_zero,zero_div] using negative_separated

/-- The actual residual Gram is positive definite for arbitrary correction R. -/
theorem arbitrary_correction_Gram (R : Matrix (Fin 6) (Fin 6) ℝ) :
    (I4ContactGram.coefficientGram
      (residualCoefficient (rawPinCoefficient 2 1) (remoteJetCoefficient 2 0) R)).PosDef :=
  actual_remote_residual_coefficientGram_posDef (by norm_num) 1 0 separated_M separated_S R

/-- The same arbitrary-R conclusion still holds at repeated pins. -/
theorem repeated_arbitrary_Gram (R : Matrix (Fin 6) (Fin 6) ℝ) :
    (I4ContactGram.coefficientGram
      (residualCoefficient (rawPinCoefficient 2 0) (remoteJetCoefficient 2 ![1,0]) R)).PosDef := by
  apply actual_remote_residual_coefficientGram_posDef (by norm_num) 0 ![1,0] repeated_separated _ R
  simpa only [endpointM,endpointS,neg_zero,zero_div] using repeated_separated

/-- At the collision x=M, the retained other-pin quotient inequality is true. -/
theorem collision_retained_separation :
    I4Torus.torusProjection 2 2 (endpointM 1) ≠ I4Torus.torusProjection 2 2 (endpointS 1) := by
  apply torus_ne_of_cos_ne (by norm_num) _ _ 0
  have he : sourceC 2*(endpointM 1 0-endpointS 1 0) = -Real.pi := by
    dsimp [sourceC,endpointM,endpointS]
    ring
  rw [he,Real.cos_neg,Real.cos_pi]
  norm_num

/-- Genuine collision counterexample: remotevalue is literal originalpinrow0. -/
theorem collision_no_witness :
    ¬ ∃ v : Fin 6 → (SourceMode 2 →₀ ℝ),
      (∀ i s, finitePairing (rawPinCoefficient 2 1 i) (v s) = 0) ∧
      (∀ j s, finitePairing (remoteJetCoefficient 2 (endpointM 1) j) (v s) = if j=s then 1 else 0) := by
  rintro ⟨v,hker,hright⟩
  have hrow : remoteJetCoefficient 2 (endpointM 1) 0 = rawPinCoefficient 2 1 0 := by
    funext m
    change modeCoefficient 2 2 m (endpointM 1) =
      iteratedFDeriv ℝ 0 (modeCoefficient 2 2 m) (endpointM 1) (rawDerivativeDirections 0)
    exact (iteratedFDeriv_zero_apply _).symm
  have h0 := hker 0 0
  have h1 := hright 0 0
  rw [hrow] at h1
  norm_num at h1
  linarith

end RemoteJetControls
