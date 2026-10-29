import SourceFinitePinKernel

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix
open I4SourceFinitePinKernel

/-- The scalar original observation has the required right-inverse pairing. -/
private theorem scalar_rightInverse :
    finitePairing (fun _ : Fin 1 => (1:ℝ)) (Finsupp.single 0 1) = 1 := by
  simp [finitePairing]

/-- Actual finite algebra counterexample to dropping ONLY the pin-kernel hypothesis. -/
private theorem scalar_residual_not_posDef :
    ¬ (I4ContactGram.coefficientGram
      (residualCoefficient (fun _ : Fin 1 => fun _ : Fin 1 => (1:ℝ))
        (fun _ : Fin 1 => fun _ : Fin 1 => (1:ℝ)) (!![1]))).PosDef := by
  intro h
  have hz : (![1] : Fin 1 → ℝ) ≠ 0 := by
    intro hh
    have hh0 := congrFun hh 0
    norm_num at hh0
  have hp := h.dotProduct_mulVec_pos hz
  norm_num [I4ContactGram.coefficientGram,residualCoefficient,Matrix.mulVec,
    dotProduct,Fin.sum_univ_succ] at hp

/-- Specialized false consequence of omitting hker: a=b=R=v=1 has zero residual. -/
theorem false_without_kernel :
    (I4ContactGram.coefficientGram
      (residualCoefficient (fun _ : Fin 1 => fun _ : Fin 1 => (1:ℝ))
        (fun _ : Fin 1 => fun _ : Fin 1 => (1:ℝ)) (!![1]))).PosDef := by
  have hright := scalar_rightInverse
  have hcounterexample := scalar_residual_not_posDef
  rw [Matrix.posDef_iff_dotProduct_mulVec]
  constructor
  · ext i j
    fin_cases i
    fin_cases j
    simp [I4ContactGram.coefficientGram,residualCoefficient,Fin.sum_univ_succ]
  · intro z hz
    norm_num [I4ContactGram.coefficientGram,residualCoefficient,Matrix.mulVec,
      dotProduct,Fin.sum_univ_succ]
