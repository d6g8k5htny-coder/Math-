import SourceFiniteTrig

/-! Actual finite original-mode witnesses for remote six-jets, retaining the
same original period and literal raw pin rows. No conditional law, Gaussian
regression or global genericity assertion is made. -/

noncomputable section
set_option autoImplicit false
open scoped BigOperators
open I4Source I4Weights I4SourceFiniteTrig I4SourceFinitePinKernel
open I4SourceConfluentPins I4SourceRawPinConditioning I4SourceDerivativeGaussian
open I4SourceConfluentLimits

namespace I4SourceRemoteJetWitness

/-- The six original coefficient rows, ordered value,dx,dy,dxx,dxy,dyy. -/
def remoteJetCoefficient (L : ℝ) (x : Fin 2 → ℝ) : Fin 6 → SourceMode 2 → ℝ :=
  ![fun m => modeCoefficient 2 L m x,
    derivativeCoefficient 2 L 1 x (fun _ => directionX),
    derivativeCoefficient 2 L 1 x (fun _ => directionY),
    derivativeCoefficient 2 L 2 x ![directionX,directionX],
    derivativeCoefficient 2 L 2 x ![directionX,directionY],
    derivativeCoefficient 2 L 2 x ![directionY,directionY]]

private def axisFrequency (j : Fin 2) : Fin 2 → ℤ := Pi.single j 1

private theorem phase_axis (L : ℝ) (j : Fin 2) (y : Fin 2 → ℝ) :
    phase 2 L (axisFrequency j) y = sourceC L * y j := by
  fin_cases j <;> simp [phase,axisFrequency,Fin.sum_univ_succ]

private def axisCosPoly (L : ℝ) (p : Fin 2 → ℝ) (j : Fin 2) : TrigPoly :=
  translate L p [⟨1,axisFrequency j,0⟩]

private def axisSinPoly (L : ℝ) (p : Fin 2 → ℝ) (j : Fin 2) : TrigPoly :=
  translate L p [⟨1,axisFrequency j,-Real.pi/2⟩]

private def factorPoly (L : ℝ) (p : Fin 2 → ℝ) (j : Fin 2) : TrigPoly :=
  constant 1 ++ scale (-1) (axisCosPoly L p j)

private def pinFactor (L : ℝ) (p : Fin 2 → ℝ) (j : Fin 2) (y : Fin 2 → ℝ) : ℝ :=
  1-Real.cos (sourceC L*(y j-p j))

private theorem eval_axisCosPoly (L : ℝ) (p : Fin 2 → ℝ) (j : Fin 2) (y : Fin 2 → ℝ) :
    eval L (axisCosPoly L p j) y = Real.cos (sourceC L*(y j-p j)) := by
  rw [axisCosPoly,eval_translate]
  simp [eval,termEval,phase_axis]

private theorem eval_axisSinPoly (L : ℝ) (p : Fin 2 → ℝ) (j : Fin 2) (y : Fin 2 → ℝ) :
    eval L (axisSinPoly L p j) y = Real.sin (sourceC L*(y j-p j)) := by
  rw [axisSinPoly,eval_translate]
  simpa [eval,termEval,phase_axis,sub_eq_add_neg,neg_div] using
    Real.cos_sub_pi_div_two (sourceC L*(y j-p j))

private theorem eval_factorPoly (L : ℝ) (p : Fin 2 → ℝ) (j : Fin 2) (y : Fin 2 → ℝ) :
    eval L (factorPoly L p j) y = pinFactor L p j y := by
  rw [factorPoly,eval_append,eval_constant,eval_scale,eval_axisCosPoly]
  simp [pinFactor,sub_eq_add_neg]

private def annihilator (L r : ℝ) (jM jS : Fin 2) (y : Fin 2 → ℝ) : ℝ :=
  (pinFactor L (endpointM r) jM y)^2 * (pinFactor L (endpointS r) jS y)^2

private def annihilatorPoly (L r : ℝ) (jM jS : Fin 2) : TrigPoly :=
  mul (mul (factorPoly L (endpointM r) jM) (factorPoly L (endpointM r) jM))
    (mul (factorPoly L (endpointS r) jS) (factorPoly L (endpointS r) jS))

private theorem eval_annihilatorPoly (L r : ℝ) (jM jS : Fin 2) (y : Fin 2 → ℝ) :
    eval L (annihilatorPoly L r jM jS) y = annihilator L r jM jS y := by
  simp only [annihilatorPoly,eval_mul,eval_factorPoly,annihilator,pow_two]

private theorem pinFactor_contDiff (L : ℝ) (p : Fin 2 → ℝ) (j : Fin 2) :
    ContDiff ℝ (⊤ : ℕ∞) (pinFactor L p j) := by
  exact contDiff_const.sub (contDiff_const.mul (((ContinuousLinearMap.proj j : (Fin 2 → ℝ) →L[ℝ] ℝ).contDiff).sub contDiff_const)).cos

private theorem annihilator_contDiff (L r : ℝ) (jM jS : Fin 2) :
    ContDiff ℝ (⊤ : ℕ∞) (annihilator L r jM jS) :=
  ((pinFactor_contDiff L (endpointM r) jM).pow 2).mul
    ((pinFactor_contDiff L (endpointS r) jS).pow 2)

private theorem annihilator_pin_values (L r : ℝ) (jM jS : Fin 2) :
    annihilator L r jM jS (endpointM r) = 0 ∧
      annihilator L r jM jS (endpointS r) = 0 := by
  simp [annihilator,pinFactor]

private theorem annihilator_pin_derivatives (L r : ℝ) (jM jS : Fin 2) :
    fderiv ℝ (annihilator L r jM jS) (endpointM r) = 0 ∧
      fderiv ℝ (annihilator L r jM jS) (endpointS r) = 0 := by
  have hA := (pinFactor_contDiff L (endpointM r) jM).differentiable (by simp)
  have hB := (pinFactor_contDiff L (endpointS r) jS).differentiable (by simp)
  constructor
  · have h := (((hA (endpointM r)).hasFDerivAt.pow 2).mul
      ((hB (endpointM r)).hasFDerivAt.pow 2)).fderiv
    change fderiv ℝ (annihilator L r jM jS) (endpointM r) = _ at h
    simpa [pinFactor] using h
  · have h := (((hA (endpointS r)).hasFDerivAt.pow 2).mul
      ((hB (endpointS r)).hasFDerivAt.pow 2)).fderiv
    change fderiv ℝ (annihilator L r jM jS) (endpointS r) = _ at h
    simpa [pinFactor] using h

end I4SourceRemoteJetWitness
