import SourceEndpointHessianWitness
import Lean.Elab.Tactic.Omega

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix
open I4Foundation I4Source I4Weights I4SmoothCarrier I4SourceDerivativeGaussian
open I4SourceConfluentPins I4SourceConfluentLimits I4SourceRawPinConditioning
open I4SourceFinitePinKernel I4SourceFiniteTrig I4SourceRemoteJetWitness
open I4SourceEndpointHessianWitness

namespace EndpointHessianControls

/-- Literal raw Hessian rows in ordinary XX,XY,YY order. -/
theorem literal_row_order (L r : ℝ) :
    endpointHessianCoefficient L r 0 0 = rawDerivativeCoefficient L r 6 ∧
    endpointHessianCoefficient L r 0 1 = rawDerivativeCoefficient L r 7 ∧
    endpointHessianCoefficient L r 0 2 = rawDerivativeCoefficient L r 8 ∧
    endpointHessianCoefficient L r 1 0 = rawDerivativeCoefficient L r 9 ∧
    endpointHessianCoefficient L r 1 1 = rawDerivativeCoefficient L r 10 ∧
    endpointHessianCoefficient L r 1 2 = rawDerivativeCoefficient L r 11 :=
  ⟨rfl,rfl,rfl,rfl,rfl,rfl⟩

/-- The actual ordinary mixed derivative has no doubled normalization. -/
theorem literal_mixed_directions (L r : ℝ) :
    endpointHessianCoefficient L r 0 1 =
      derivativeCoefficient 2 L 2 (endpointM r) ![directionX,directionY] ∧
    endpointHessianCoefficient L r 1 1 =
      derivativeCoefficient 2 L 2 (endpointS r) ![directionX,directionY] := by
  constructor
  · change derivativeCoefficient 2 L 2 (endpointM r) (rawDerivativeDirections 7) = _
    congr 1
    funext i
    fin_cases i <;> rfl
  · change derivativeCoefficient 2 L 2 (endpointS r) (rawDerivativeDirections 10) = _
    congr 1
    funext i
    fin_cases i <;> rfl

/-- The selected rows are the actual smooth source Hessian observations. -/
theorem actual_observation_series {L : ℝ} (hL : L ≠ 0) (r : ℝ) (ω : SmoothSample 2 L) :
    rawPinsWithHessians L r ω 6 = scalarSeries (endpointHessianCoefficient L r 0 0) (sampleInclusion 2 L ω) ∧
    rawPinsWithHessians L r ω 7 = scalarSeries (endpointHessianCoefficient L r 0 1) (sampleInclusion 2 L ω) ∧
    rawPinsWithHessians L r ω 8 = scalarSeries (endpointHessianCoefficient L r 0 2) (sampleInclusion 2 L ω) ∧
    rawPinsWithHessians L r ω 9 = scalarSeries (endpointHessianCoefficient L r 1 0) (sampleInclusion 2 L ω) ∧
    rawPinsWithHessians L r ω 10 = scalarSeries (endpointHessianCoefficient L r 1 1) (sampleInclusion 2 L ω) ∧
    rawPinsWithHessians L r ω 11 = scalarSeries (endpointHessianCoefficient L r 1 2) (sampleInclusion 2 L ω) := by
  have h := rawPinsWithHessians_series hL r ω
  exact ⟨congrFun h 6,congrFun h 7,congrFun h 8,congrFun h 9,congrFun h 10,congrFun h 11⟩

private theorem separated_signed_units (L r : ℝ) (hL : L=2 ∨ L= -2) (hr : r=1 ∨ r= -1) :
    I4Torus.torusProjection 2 L (endpointM r) ≠
      I4Torus.torusProjection 2 L (endpointS r) := by
  intro h
  have hz : (((endpointM r 0-endpointS r 0):ℝ):AddCircle L) = 0 := by
    rw [AddCircle.coe_sub,sub_eq_zero]
    exact congrFun h 0
  obtain ⟨n,hn⟩ := (AddCircle.coe_eq_zero_iff (p:=L)).mp hz
  rcases hL with rfl|rfl <;> rcases hr with rfl|rfl
  all_goals norm_num [endpointM,endpointS,zsmul_eq_mul] at hn
  all_goals
    have hnR : (n:ℝ)*2=1 ∨ (n:ℝ)*2= -1 := by
      first | exact Or.inl (by linarith) | exact Or.inr (by linarith)
    have hnZ : (n:ℤ)*2=1 ∨ (n:ℤ)*2= -1 := by
      rcases hnR with h1|h1
      · left
        exact_mod_cast h1
      · right
        exact_mod_cast h1
    omega

/-- Both internally constructed endpoint families: all36 raw and18 own-Hessian pairings. -/
theorem actual_two_families :
    ∃ v : Fin 2 → Fin 3 → (SourceMode 2 →₀ ℝ),
      (∀ e i s, finitePairing (rawPinCoefficient 2 1 i) (v e s) = 0) ∧
      (∀ e j s, finitePairing (endpointHessianCoefficient 2 1 e j) (v e s) = if j=s then 1 else 0) :=
  actual_finite_endpointHessian_witnesses (by norm_num) 1
    (separated_signed_units 2 1 (Or.inl rfl) (Or.inl rfl))

/-- Distinct Hessian targets1,2,3 use the actual finite original directions. -/
theorem distinct_hessian_targets :
    ∃ w : Fin 2 → (SourceMode 2 →₀ ℝ),
      (∀ e i, finitePairing (rawPinCoefficient 2 1 i) (w e) = 0) ∧
      (∀ e j, finitePairing (endpointHessianCoefficient 2 1 e j) (w e) = ![1,2,3] j) := by
  classical
  obtain ⟨v,hker,hright⟩ := actual_two_families
  have hp (a : SourceMode 2 → ℝ) (z : SourceMode 2 →₀ ℝ) :
      finitePairing a z = Finsupp.linearCombination ℝ a z := by
    simp [finitePairing,Finsupp.linearCombination_apply,Finsupp.sum,smul_eq_mul,mul_comm]
  refine ⟨fun e => ∑ s : Fin 3, (![1,2,3] s : ℝ) • v e s,?_,?_⟩
  · intro e i
    simp_rw [hp]
    rw [map_sum]
    simp_rw [map_smul,← hp]
    simp [hker]
  · intro e j
    simp_rw [hp]
    rw [map_sum]
    simp_rw [map_smul,← hp]
    simp [hright,smul_eq_mul]

/-- The original signed negative period is retained in the actual source directions. -/
theorem actual_negative_period_families :
    ∃ v : Fin 2 → Fin 3 → (SourceMode 2 →₀ ℝ),
      (∀ e i s, finitePairing (rawPinCoefficient (-2) 1 i) (v e s) = 0) ∧
      (∀ e j s, finitePairing (endpointHessianCoefficient (-2) 1 e j) (v e s) = if j=s then 1 else 0) :=
  actual_finite_endpointHessian_witnesses (by norm_num) 1
    (separated_signed_units (-2) 1 (Or.inr rfl) (Or.inl rfl))

/-- Negative radius swaps the literal endpoint positions without a positivity assumption. -/
theorem actual_negative_radius_families :
    ∃ v : Fin 2 → Fin 3 → (SourceMode 2 →₀ ℝ),
      (∀ e i s, finitePairing (rawPinCoefficient 2 (-1) i) (v e s) = 0) ∧
      (∀ e j s, finitePairing (endpointHessianCoefficient 2 (-1) e j) (v e s) = if j=s then 1 else 0) :=
  actual_finite_endpointHessian_witnesses (by norm_num) (-1)
    (separated_signed_units 2 (-1) (Or.inl rfl) (Or.inr rfl))

/-- A concrete nonzero nonsymmetric rectangular correction, for both endpoint tags. -/
theorem concrete_rectangular_posDef (e : Fin 2) :
    (I4ContactGram.coefficientGram (residualCoefficient (rawPinCoefficient 2 1)
      (endpointHessianCoefficient 2 1 e)
      (fun j i => ((j.val+1:ℕ):ℝ)*((i.val+2:ℕ):ℝ)))).PosDef :=
  actual_endpointHessian_residual_coefficientGram_posDef (by norm_num) 1
    (separated_signed_units 2 1 (Or.inl rfl) (Or.inl rfl)) e _

/-- The same actual3x6 interface also accepts zero correction at both endpoints. -/
theorem zero_rectangular_posDef (e : Fin 2) :
    (I4ContactGram.coefficientGram (residualCoefficient (rawPinCoefficient 2 1)
      (endpointHessianCoefficient 2 1 e) (0 : Matrix (Fin 3) (Fin 6) ℝ))).PosDef :=
  actual_endpointHessian_residual_coefficientGram_posDef (by norm_num) 1
    (separated_signed_units 2 1 (Or.inl rfl) (Or.inl rfl)) e _

-- Concrete actual polynomial supporting the sole scalar-normalization mutation.
private def concreteCos (p : Fin 2 → ℝ) : TrigPoly :=
  translate 2 p [⟨1,Pi.single (0:Fin 2) 1,0⟩]

private def concreteFactor (p : Fin 2 → ℝ) : TrigPoly :=
  constant 1 ++ scale (-1) (concreteCos p)

def unnormalizedPoly : TrigPoly :=
  mul (mul (concreteFactor (endpointS 1)) (concreteFactor (endpointS 1)))
    (scale (Real.pi^2)⁻¹ (concreteFactor (endpointM 1)))

private def concreteMultiplier (q : Fin 2 → ℝ) (y : Fin 2 → ℝ) : ℝ :=
  (1-Real.cos (Real.pi*(y 0-q 0)))^2

private theorem concreteCos_eval (p y : Fin 2 → ℝ) :
    eval 2 (concreteCos p) y = Real.cos (Real.pi*(y 0-p 0)) := by
  rw [concreteCos,eval_translate]
  simp [eval,termEval,phase,sourceC,Fin.sum_univ_succ]

private theorem concreteFactor_eval (p y : Fin 2 → ℝ) :
    eval 2 (concreteFactor p) y = 1-Real.cos (Real.pi*(y 0-p 0)) := by
  rw [concreteFactor,eval_append,eval_constant,eval_scale,concreteCos_eval]
  ring

private theorem unnormalizedPoly_eval :
    eval 2 unnormalizedPoly = fun y => concreteMultiplier (endpointS 1) y *
      localGerm Real.pi (endpointM 1) 3 y := by
  funext y
  simp only [unnormalizedPoly,eval_mul,eval_scale,concreteFactor_eval]
  simp [concreteMultiplier,localGerm,div_eq_mul_inv,pow_two,mul_assoc,mul_comm]

private theorem concreteMultiplier_contDiff (q : Fin 2 → ℝ) :
    ContDiff ℝ (⊤:ℕ∞) (concreteMultiplier q) := by
  unfold concreteMultiplier
  fun_prop

/-- At both endpoints the opposite-pin multiplier has literal valuealpha4. -/
theorem concrete_alphas :
    concreteMultiplier (endpointS 1) (endpointM 1) = 4 ∧
    concreteMultiplier (endpointM 1) (endpointS 1) = 4 := by
  norm_num [concreteMultiplier,endpointM,endpointS,Real.cos_neg,Real.cos_pi]

/-- The own germ has zero value/gradient and ordinary XX/XY/YY basis normalization. -/
theorem concrete_germ_jets (s : Fin 3) :
    jet2 (localGerm Real.pi (endpointM 1) (Fin.castAdd 3 s + 3)) (endpointM 1) =
      fun j => if j=(Fin.castAdd 3 s+3) then 1 else 0 := by
  ext j
  exact localGerm_jet2 Real.pi Real.pi_ne_zero _ j _

/-- The multiplier vanishes to first order at its own opposite pin. -/
theorem concrete_other_lower :
    concreteMultiplier (endpointS 1) (endpointS 1) = 0 ∧
    fderiv ℝ (concreteMultiplier (endpointS 1)) (endpointS 1) = 0 := by
  constructor
  · simp [concreteMultiplier]
  · have hA : DifferentiableAt ℝ (fun y : Fin 2 → ℝ =>
        1-Real.cos (Real.pi*(y 0-endpointS 1 0))) (endpointS 1) := by fun_prop
    have h := (hA.hasFDerivAt.pow 2).fderiv
    change fderiv ℝ (concreteMultiplier (endpointS 1)) (endpointS 1) = _ at h
    simpa using h

/-- The ACTUAL unnormalized original finite direction pairs with literal row6 as4. -/
theorem unnormalized_actual_row6 :
    finitePairing (rawDerivativeCoefficient 2 1 6) (toSource 2 unnormalizedPoly) = 4 := by
  have he : rawDerivativeCoefficient 2 1 6 =
      derivativeCoefficient 2 2 2 (endpointM 1) ![directionX,directionX] := by
    change derivativeCoefficient 2 2 2 (endpointM 1) (rawDerivativeDirections 6) = _
    congr 1
    funext i
    fin_cases i <;> rfl
  rw [he]
  rw [toSource_derivative (by norm_num),unnormalizedPoly_eval]
  change jet2 (fun y => concreteMultiplier (endpointS 1) y *
    localGerm Real.pi (endpointM 1) 3 y) (endpointM 1) 3 = 4
  rw [jet2_mul _ _ ((concreteMultiplier_contDiff _).of_le (by simp))]
  · simp_rw [localGerm_jet2 Real.pi Real.pi_ne_zero]
    simp [mulJet2,jet2,concrete_alphas.1]
  · unfold localGerm
    fun_prop

/-- Counterexample to omitting alpha^-1, linked to actual raw row6 and toSource. -/
theorem scalar_normalization_counterexample :
    finitePairing (rawDerivativeCoefficient 2 1 6) (toSource 2 unnormalizedPoly) ≠ 1 := by
  rw [unnormalized_actual_row6]
  norm_num

end EndpointHessianControls
