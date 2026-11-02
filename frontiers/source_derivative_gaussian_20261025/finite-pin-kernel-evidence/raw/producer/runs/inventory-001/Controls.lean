import SourceFinitePinKernel

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix
open I4SourceFinitePinKernel I4Source I4Smooth I4SmoothCarrier
open I4SourceConfluentPins I4SourceRawPinConditioning

namespace FinitePinControls

private theorem pairing_finite {ι : Type*} [Fintype ι]
    (a : ι → ℝ) (v : ι →₀ ℝ) : finitePairing a v = ∑ m, a m * v m := by
  classical
  exact Finsupp.sum_fintype _ _ (fun _ => mul_zero _)

private def cancelWitness : Fin 2 →₀ ℝ := Finsupp.equivFunOnFinite.symm ![-1,1]
private def cancelPins : Fin 1 → Fin 2 → ℝ := fun _ => ![1,1]
private def cancelObs : Fin 1 → Fin 2 → ℝ := fun _ => ![0,1]

/-- Both support entries and observation-times-direction multiplication matter. -/
theorem nontrivial_pairing :
    finitePairing (![2,3] : Fin 2 → ℝ)
      (Finsupp.equivFunOnFinite.symm (![-1,4] : Fin 2 → ℝ)) = 10 := by
  norm_num [pairing_finite,Fin.sum_univ_succ]

/-- A nonzero finite direction annihilates pins but is an observation right inverse. -/
theorem nontrivial_kernel_witness :
    finitePairing (cancelPins 0) cancelWitness = 0 ∧
      finitePairing (cancelObs 0) cancelWitness = 1 := by
  norm_num [pairing_finite,cancelPins,cancelObs,cancelWitness,Fin.sum_univ_succ]

/-- The original finite witness forces positivity for every correction matrix. -/
theorem arbitrary_correction_posDef (R : Matrix (Fin 1) (Fin 1) ℝ) :
    (I4ContactGram.coefficientGram (residualCoefficient cancelPins cancelObs R)).PosDef := by
  apply coefficientGram_posDef_of_finite_kernel_rightInverse
    cancelPins cancelObs R (fun _ => summable_fintype _) (fun _ => summable_fintype _)
    (fun _ => cancelWitness)
  · intro i s
    fin_cases i
    exact nontrivial_kernel_witness.1
  · intro j s
    fin_cases j
    fin_cases s
    exact nontrivial_kernel_witness.2

/-- At R=7 the residual pairing is still one; neither row is the zero pin row. -/
theorem residual_pairing_seven :
    finitePairing (residualCoefficient cancelPins cancelObs (!![7]) 0) cancelWitness = 1 := by
  rw [finitePairing_residualCoefficient]
  simp [Fin.sum_univ_succ,nontrivial_kernel_witness.1,nontrivial_kernel_witness.2]

/-- The new summability adapter applies to the same concrete corrected rows. -/
theorem residual_summability (R : Matrix (Fin 1) (Fin 1) ℝ) :
    Summable (residualCoefficient cancelPins cancelObs R 0) :=
  residualCoefficient_summable _ _ _ (fun _ => summable_fintype _)
    (fun _ => summable_fintype _) 0

/-- No-pin rows are permitted: the witness then supplies direct observation separation. -/
theorem no_pins_posDef :
    (I4ContactGram.coefficientGram
      (residualCoefficient (fun i : Fin 0 => Fin.elim0 i)
        (fun _ : Fin 1 => fun _ : Fin 1 => (1:ℝ))
        (fun _ : Fin 1 => fun i : Fin 0 => Fin.elim0 i))).PosDef := by
  apply coefficientGram_posDef_of_finite_kernel_rightInverse _ _ _
    (fun i => Fin.elim0 i) (fun _ => summable_fintype _)
    (fun _ => Finsupp.single (0 : Fin 1) 1)
  · intro i
    exact Fin.elim0 i
  · intro j s
    fin_cases j
    fin_cases s
    norm_num [pairing_finite,Fin.sum_univ_succ]

/-- No observation rows are permitted, with positive definiteness on the zero space. -/
theorem no_observations_posDef :
    (I4ContactGram.coefficientGram
      (residualCoefficient (fun _ : Fin 1 => fun _ : Fin 1 => (1:ℝ))
        (fun j : Fin 0 => Fin.elim0 j)
        (fun j : Fin 0 => Fin.elim0 j))).PosDef := by
  apply coefficientGram_posDef_of_finite_kernel_rightInverse _ _ _
    (fun _ => summable_fintype _) (fun j => Fin.elim0 j)
    (fun j => Fin.elim0 j)
  · intro _ s
    exact Fin.elim0 s
  · intro j
    exact Fin.elim0 j

/-- A finite shift stays in the literal original carrier even at period zero. -/
theorem original_carrier_zero_period (ω : SmoothSample 2 0) (v : SourceMode 2 →₀ ℝ) :
    goodSample 2 0 (fun m => ω.val m + v m) :=
  (finiteShiftSample v ω).property

/-- A concrete original DC-coordinate shift is exactly two at every period. -/
theorem dc_shift_coeff {L : ℝ} (ω : SmoothSample 2 L) :
    (finiteShiftSample (Finsupp.single none 2) ω).val none = ω.val none + 2 := by
  simp

/-- Exact raw response at radius zero with a nonzero finite original shift. -/
theorem raw_zero_radius_response (ω : SmoothSample 2 1) (i : Fin 6) :
    rawPins 1 0 (finiteShiftSample (Finsupp.single none 2) ω) i =
      rawPins 1 0 ω i + rawPinCoefficient 1 0 i none * 2 := by
  have h := congrFun (rawPins_finiteShiftSample (by norm_num : (1:ℝ)≠0) 0
    (Finsupp.single none 2) ω) i
  simpa [finitePairing] using h

/-- Every literal six-target vector is allowed, with arbitrary radius and original sample. -/
theorem everytarget_commutation (r : ℝ) (t : Fin 6 → ℝ)
    (v : SourceMode 2 →₀ ℝ) (hker : ∀ i, finitePairing (rawPinCoefficient 1 r i) v = 0)
    (ω : SmoothSample 2 1) :
    rawPosteriorSample (by norm_num : (1:ℝ)≠0) r t (finiteShiftSample v ω) =
      finiteShiftSample v (rawPosteriorSample (by norm_num : (1:ℝ)≠0) r t ω) :=
  rawPosteriorSample_finiteShiftSample (by norm_num) r t v hker ω

/-- The singular zero-radius case needs no covariance or invertibility premise. -/
theorem zero_radius_commutation (t : Fin 6 → ℝ) (v : SourceMode 2 →₀ ℝ)
    (hker : ∀ i, finitePairing (rawPinCoefficient 1 0 i) v = 0) (ω : SmoothSample 2 1) :
    rawPosteriorSample (by norm_num : (1:ℝ)≠0) 0 t (finiteShiftSample v ω) =
      finiteShiftSample v (rawPosteriorSample (by norm_num : (1:ℝ)≠0) 0 t ω) :=
  everytarget_commutation 0 t v hker ω

/-- Concrete omitted-hker counterexample: original right inverse but residual zero. -/
theorem omitted_kernel_counterexample :
    finitePairing (fun _ : Fin 1 => (1:ℝ)) (Finsupp.single 0 1) = 1 ∧
      ¬ (I4ContactGram.coefficientGram
        (residualCoefficient (fun _ : Fin 1 => fun _ : Fin 1 => (1:ℝ))
          (fun _ : Fin 1 => fun _ : Fin 1 => (1:ℝ)) (!![1]))).PosDef := by
  constructor
  · norm_num [pairing_finite,Fin.sum_univ_succ]
  · intro h
    have hz : (![1] : Fin 1 → ℝ) ≠ 0 := by
      intro hh
      have hh0 := congrFun hh 0
      norm_num at hh0
    have hp := h.dotProduct_mulVec_pos hz
    norm_num [I4ContactGram.coefficientGram,residualCoefficient,Matrix.mulVec,
      dotProduct,Fin.sum_univ_succ] at hp

end FinitePinControls
