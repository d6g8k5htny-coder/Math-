import SourceRemoteJetWitness
import Lean.Elab.Tactic.Omega

/-! Separate ordinary Hessian-three finite right inverses at the literal endpoints.
The families annihilate raw six-pins. No cross-endpoint Hessian conditions or
joint six-Hessian rank are asserted. -/

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix
open I4Source I4Weights I4SourceDerivativeGaussian I4SourceConfluentPins
open I4SourceConfluentLimits I4SourceRawPinConditioning I4SourceFinitePinKernel
open I4SourceFiniteTrig I4SourceRemoteJetWitness

namespace I4SourceEndpointHessianWitness

private def rowIndex (e : Fin 2) (j : Fin 3) : Fin 12 :=
  ![![6,7,8],![9,10,11]] e j

/-- Literal ordinary XX,XY,YY rows6..8 at M and9..11 at S. -/
def endpointHessianCoefficient (L r : ℝ) (e : Fin 2) : Fin 3 → SourceMode 2 → ℝ :=
  fun j => rawDerivativeCoefficient L r (rowIndex e j)

private def endpointPoint (r : ℝ) (e : Fin 2) : Fin 2 → ℝ :=
  ![endpointM r,endpointS r] e

private def otherPoint (r : ℝ) (e : Fin 2) : Fin 2 → ℝ :=
  ![endpointS r,endpointM r] e

private theorem sourceC_ne_zero {L : ℝ} (hL : L ≠ 0) : sourceC L ≠ 0 :=
  div_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero) hL

private theorem endpoint_separated {L : ℝ} (r : ℝ)
    (hsep : I4Torus.torusProjection 2 L (endpointM r) ≠
      I4Torus.torusProjection 2 L (endpointS r)) (e : Fin 2) :
    I4Torus.torusProjection 2 L (endpointPoint r e) ≠
      I4Torus.torusProjection 2 L (otherPoint r e) := by
  fin_cases e
  · exact hsep
  · exact hsep.symm

private theorem endpoint_cos_ne_one {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hsep : I4Torus.torusProjection 2 L (endpointM r) ≠
      I4Torus.torusProjection 2 L (endpointS r)) (e : Fin 2) :
    Real.cos (sourceC L * (endpointPoint r e 0 - otherPoint r e 0)) ≠ 1 := by
  intro hc
  obtain ⟨n, hn⟩ := (Real.cos_eq_one_iff _).mp hc
  have ht : 2 * Real.pi ≠ 0 := mul_ne_zero (by norm_num) Real.pi_ne_zero
  have hdiv : (n : ℝ) = (endpointPoint r e 0 - otherPoint r e 0) / L := by
    apply mul_left_cancel₀ ht
    calc
      (2 * Real.pi) * (n : ℝ) = (n : ℝ) * (2 * Real.pi) := by ring
      _ = sourceC L * (endpointPoint r e 0 - otherPoint r e 0) := hn
      _ = (2 * Real.pi) * ((endpointPoint r e 0 - otherPoint r e 0) / L) := by
        unfold sourceC
        ring
  have hnL : n • L = endpointPoint r e 0 - otherPoint r e 0 := by
    simpa only [zsmul_eq_mul] using (eq_div_iff hL).mp hdiv
  have hz : ((endpointPoint r e 0 - otherPoint r e 0 : ℝ) : AddCircle L) = 0 :=
    (AddCircle.coe_eq_zero_iff (p := L)).mpr ⟨n,hnL⟩
  rw [AddCircle.coe_sub] at hz
  apply endpoint_separated r hsep e
  funext j
  fin_cases j
  · exact sub_eq_zero.mp hz
  · fin_cases e <;> simp [endpointPoint,otherPoint,endpointM,endpointS,I4Torus.torusProjection]

-- Integrated once from frozen text-only arithmetic helper.
/- Text-only endpoint Hessian arithmetic helper.
   Intended insertion: namespace I4SourceEndpointHessianWitness, after
   `open I4SourceRemoteJetWitness` and the producer's existing imports.
   Depends only on public source48 `jet2`, `mulJet2`, `localGerm`,
   `localGerm_jet2`, and `jet2_mul`; no foreign private API.
   This helper text has not been compiled or otherwise Lean-checked. -/

private def pinMultiplier (c : ℝ) (q y : Fin 2 → ℝ) : ℝ :=
  (1 - Real.cos (c * (y 0 - q 0))) ^ 2

private def hessianJetIndex (s : Fin 3) : Fin 6 :=
  ⟨s.val + 3, by omega⟩

private def normalizedGerm (c : ℝ) (p q : Fin 2 → ℝ) (s : Fin 3)
    (y : Fin 2 → ℝ) : ℝ :=
  (pinMultiplier c q p)⁻¹ * pinMultiplier c q y *
    localGerm c p (hessianJetIndex s) y

private theorem pinMultiplier_contDiff (c : ℝ) (q : Fin 2 → ℝ) :
    ContDiff ℝ (⊤ : ℕ∞) (pinMultiplier c q) := by
  unfold pinMultiplier
  exact (contDiff_const.sub
    (contDiff_const.mul
      (((ContinuousLinearMap.proj (0 : Fin 2) : (Fin 2 → ℝ) →L[ℝ] ℝ).contDiff).sub
        contDiff_const)).cos).pow 2

private theorem hessianLocalGerm_contDiff (c : ℝ) (p : Fin 2 → ℝ) (s : Fin 3) :
    ContDiff ℝ (⊤ : ℕ∞) (localGerm c p (hessianJetIndex s)) := by
  fin_cases s
  · change ContDiff ℝ (⊤ : ℕ∞) (fun y : Fin 2 → ℝ =>
      (1-Real.cos (c*(y 0-p 0)))/c^2)
    fun_prop
  · change ContDiff ℝ (⊤ : ℕ∞) (fun y : Fin 2 → ℝ =>
      Real.sin (c*(y 0-p 0))*Real.sin (c*(y 1-p 1))/c^2)
    fun_prop
  · change ContDiff ℝ (⊤ : ℕ∞) (fun y : Fin 2 → ℝ =>
      (1-Real.cos (c*(y 1-p 1)))/c^2)
    fun_prop

private theorem normalizedGerm_contDiff (c : ℝ) (p q : Fin 2 → ℝ) (s : Fin 3) :
    ContDiff ℝ (⊤ : ℕ∞) (normalizedGerm c p q s) := by
  exact (contDiff_const.mul (pinMultiplier_contDiff c q)).mul
    (hessianLocalGerm_contDiff c p s)

private theorem pinMultiplier_value (c : ℝ) (q : Fin 2 → ℝ) :
    pinMultiplier c q q = 0 := by
  simp [pinMultiplier]

private theorem pinMultiplier_fderiv (c : ℝ) (q : Fin 2 → ℝ) :
    fderiv ℝ (pinMultiplier c q) q = 0 := by
  have hA : ContDiff ℝ (⊤ : ℕ∞)
      (fun y : Fin 2 → ℝ => 1 - Real.cos (c * (y 0 - q 0))) := by
    exact contDiff_const.sub
      (contDiff_const.mul
        (((ContinuousLinearMap.proj (0 : Fin 2) : (Fin 2 → ℝ) →L[ℝ] ℝ).contDiff).sub
          contDiff_const)).cos
  have h := (((hA.differentiable (by simp)) q).hasFDerivAt.pow 2).fderiv
  change fderiv ℝ (pinMultiplier c q) q = _ at h
  simpa using h

private theorem endpoint_jet2_scale (a : ℝ) (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ 2 f) (x : Fin 2 → ℝ) :
    jet2 (fun y => a * f y) x = fun j => a * jet2 f x j := by
  have h1 := fderiv_const_mul (hf.differentiable (by norm_num) x) a
  have h2 := iteratedFDeriv_const_smul_apply' (a := a) (x := x) hf.contDiffAt
  simp only [smul_eq_mul] at h2
  ext j
  fin_cases j <;> dsimp [jet2]
  · rw [h1]
    simp
  · rw [h1]
    simp
  · rw [h2]
    rfl
  · rw [h2]
    rfl
  · rw [h2]
    rfl

private theorem normalizedGerm_own_jet (c : ℝ) (hc : c ≠ 0)
    (p q : Fin 2 → ℝ) (hα : pinMultiplier c q p ≠ 0) (s : Fin 3) :
    jet2 (normalizedGerm c p q s) p =
      ![0, 0, 0, if (0 : Fin 3) = s then 1 else 0,
        if (1 : Fin 3) = s then 1 else 0,
        if (2 : Fin 3) = s then 1 else 0] := by
  have hP : ContDiff ℝ 2 (pinMultiplier c q) :=
    (pinMultiplier_contDiff c q).of_le (by norm_num)
  have hG : ContDiff ℝ 2 (localGerm c p (hessianJetIndex s)) :=
    (hessianLocalGerm_contDiff c p s).of_le (by norm_num)
  have hfun : normalizedGerm c p q s =
      (fun y => (pinMultiplier c q p)⁻¹ *
        (pinMultiplier c q y * localGerm c p (hessianJetIndex s) y)) := by
    funext y
    dsimp [normalizedGerm]
    ring
  have hjet : jet2 (localGerm c p (hessianJetIndex s)) p =
      (fun j => if j = hessianJetIndex s then 1 else 0) := by
    funext j
    exact localGerm_jet2 c hc p j (hessianJetIndex s)
  rw [hfun, endpoint_jet2_scale _ _ (hP.mul hG), jet2_mul _ _ hP hG, hjet]
  ext j
  fin_cases s <;> fin_cases j <;> simp [mulJet2, hessianJetIndex, jet2, hα]

private theorem normalizedGerm_value_other (c : ℝ) (p q : Fin 2 → ℝ)
    (s : Fin 3) : normalizedGerm c p q s q = 0 := by
  simp [normalizedGerm, pinMultiplier_value]

private theorem normalizedGerm_fderiv_other (c : ℝ) (p q : Fin 2 → ℝ)
    (s : Fin 3) : fderiv ℝ (normalizedGerm c p q s) q = 0 := by
  have hP : DifferentiableAt ℝ (pinMultiplier c q) q :=
    (pinMultiplier_contDiff c q).differentiable (by simp) q
  have hG : DifferentiableAt ℝ (localGerm c p (hessianJetIndex s)) q :=
    (hessianLocalGerm_contDiff c p s).differentiable (by simp) q
  change fderiv ℝ (fun y =>
    ((pinMultiplier c q p)⁻¹ * pinMultiplier c q y) *
      localGerm c p (hessianJetIndex s) y) q = 0
  rw [fderiv_fun_mul (hP.const_mul _) hG, fderiv_const_mul hP]
  simp [pinMultiplier_value, pinMultiplier_fderiv]

private theorem normalizedGerm_other_lower (c : ℝ) (_hc : c ≠ 0)
    (p q : Fin 2 → ℝ) (s : Fin 3) :
    jet2 (normalizedGerm c p q s) q 0 = 0 ∧
      jet2 (normalizedGerm c p q s) q 1 = 0 ∧
      jet2 (normalizedGerm c p q s) q 2 = 0 := by
  constructor
  · exact normalizedGerm_value_other c p q s
  constructor
  · change fderiv ℝ (normalizedGerm c p q s) q directionX = 0
    rw [normalizedGerm_fderiv_other]
    rfl
  · change fderiv ℝ (normalizedGerm c p q s) q directionY = 0
    rw [normalizedGerm_fderiv_other]
    rfl


private def axisFrequency (j : Fin 2) : Fin 2 → ℤ := Pi.single j 1

private theorem phase_axis (L : ℝ) (j : Fin 2) (y : Fin 2 → ℝ) :
    phase 2 L (axisFrequency j) y = sourceC L * y j := by
  fin_cases j <;> simp [phase,axisFrequency,Fin.sum_univ_succ]

private def axisCosPoly (L : ℝ) (p : Fin 2 → ℝ) (j : Fin 2) : TrigPoly :=
  translate L p [⟨1,axisFrequency j,0⟩]

private def axisSinPoly (L : ℝ) (p : Fin 2 → ℝ) (j : Fin 2) : TrigPoly :=
  translate L p [⟨1,axisFrequency j,-Real.pi/2⟩]

private def factorPoly (L : ℝ) (q : Fin 2 → ℝ) (j : Fin 2) : TrigPoly :=
  constant 1 ++ scale (-1) (axisCosPoly L q j)

private def multiplierPoly (L : ℝ) (q : Fin 2 → ℝ) : TrigPoly :=
  mul (factorPoly L q 0) (factorPoly L q 0)

private def hessianGermPoly (L : ℝ) (p : Fin 2 → ℝ) (s : Fin 3) : TrigPoly :=
  ![scale ((sourceC L)^2)⁻¹ (factorPoly L p 0),
    scale ((sourceC L)^2)⁻¹ (mul (axisSinPoly L p 0) (axisSinPoly L p 1)),
    scale ((sourceC L)^2)⁻¹ (factorPoly L p 1)] s

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
    eval L (factorPoly L p j) y = 1-Real.cos (sourceC L*(y j-p j)) := by
  rw [factorPoly,eval_append,eval_constant,eval_scale,eval_axisCosPoly]
  ring

private theorem eval_multiplierPoly (L : ℝ) (q y : Fin 2 → ℝ) :
    eval L (multiplierPoly L q) y = pinMultiplier (sourceC L) q y := by
  rw [multiplierPoly,eval_mul,eval_factorPoly]
  simp only [pinMultiplier,pow_two]

private theorem eval_hessianGermPoly (L : ℝ) (p y : Fin 2 → ℝ) (s : Fin 3) :
    eval L (hessianGermPoly L p s) y = localGerm (sourceC L) p (hessianJetIndex s) y := by
  fin_cases s <;> simp [hessianGermPoly,hessianJetIndex,localGerm,eval_scale,
    eval_mul,eval_factorPoly,eval_axisSinPoly,div_eq_mul_inv,mul_comm]

private def witnessPoly (L r : ℝ) (e : Fin 2) (s : Fin 3) : TrigPoly :=
  scale (pinMultiplier (sourceC L) (otherPoint r e) (endpointPoint r e))⁻¹
    (mul (multiplierPoly L (otherPoint r e)) (hessianGermPoly L (endpointPoint r e) s))

private theorem eval_witnessPoly (L r : ℝ) (e : Fin 2) (s : Fin 3) :
    eval L (witnessPoly L r e s) =
      normalizedGerm (sourceC L) (endpointPoint r e) (otherPoint r e) s := by
  funext y
  rw [witnessPoly,eval_scale,eval_mul,eval_multiplierPoly,eval_hessianGermPoly]
  simp only [normalizedGerm,mul_assoc]

private theorem multiplier_at_endpoint_pos {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hsep : I4Torus.torusProjection 2 L (endpointM r) ≠
      I4Torus.torusProjection 2 L (endpointS r)) (e : Fin 2) :
    0 < pinMultiplier (sourceC L) (otherPoint r e) (endpointPoint r e) := by
  have hc : Real.cos (sourceC L * (endpointPoint r e 0 - otherPoint r e 0)) < 1 :=
    lt_of_le_of_ne (Real.cos_le_one _) (endpoint_cos_ne_one hL r hsep e)
  exact sq_pos_of_pos (sub_pos.mpr hc)

private theorem endpointHessianCoefficient_summable {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (e : Fin 2) (j : Fin 3) : Summable (endpointHessianCoefficient L r e j) :=
  derivativeCoefficient_summable 2 hL (rawDerivativeOrder (rowIndex e j))
    (rawDerivativePoint r (rowIndex e j)) (rawDerivativeDirections (rowIndex e j))

private theorem rawPin_pairing {L : ℝ} (hL : L ≠ 0) (r : ℝ) (p : TrigPoly) (i : Fin 6) :
    finitePairing (rawPinCoefficient L r i) (toSource L p) =
      ![eval L p (endpointM r),eval L p (endpointS r),
        fderiv ℝ (eval L p) (endpointM r) directionX,fderiv ℝ (eval L p) (endpointS r) directionX,
        fderiv ℝ (eval L p) (endpointM r) directionY,fderiv ℝ (eval L p) (endpointS r) directionY] i := by
  change finitePairing (derivativeCoefficient 2 L (rawDerivativeOrder (Fin.castAdd 6 i))
    (rawDerivativePoint r (Fin.castAdd 6 i)) (rawDerivativeDirections (Fin.castAdd 6 i)))
      (toSource L p) = _
  rw [toSource_derivative hL]
  fin_cases i <;> first | exact iteratedFDeriv_zero_apply _ | exact iteratedFDeriv_one_apply _

private theorem endpointHessian_pairing {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (e : Fin 2) (p : TrigPoly) (j : Fin 3) :
    finitePairing (endpointHessianCoefficient L r e j) (toSource L p) =
      jet2 (eval L p) (endpointPoint r e) (hessianJetIndex j) := by
  change finitePairing (derivativeCoefficient 2 L (rawDerivativeOrder (rowIndex e j))
    (rawDerivativePoint r (rowIndex e j)) (rawDerivativeDirections (rowIndex e j)))
      (toSource L p) = _
  rw [toSource_derivative hL]
  fin_cases e <;> fin_cases j <;>
    congr 1 <;> funext i <;> fin_cases i <;> rfl

private theorem witness_raw_zero {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hsep : I4Torus.torusProjection 2 L (endpointM r) ≠
      I4Torus.torusProjection 2 L (endpointS r)) (e : Fin 2) (s : Fin 3) (i : Fin 6) :
    finitePairing (rawPinCoefficient L r i) (toSource L (witnessPoly L r e s)) = 0 := by
  rw [rawPin_pairing hL,eval_witnessPoly]
  have ho := normalizedGerm_own_jet (sourceC L) (sourceC_ne_zero hL)
    (endpointPoint r e) (otherPoint r e) (multiplier_at_endpoint_pos hL r hsep e).ne' s
  have hq := normalizedGerm_other_lower (sourceC L) (sourceC_ne_zero hL)
    (endpointPoint r e) (otherPoint r e) s
  have hp0 : normalizedGerm (sourceC L) (endpointPoint r e) (otherPoint r e) s
      (endpointPoint r e) = 0 := congrFun ho 0
  have hp1 : fderiv ℝ (normalizedGerm (sourceC L) (endpointPoint r e) (otherPoint r e) s)
      (endpointPoint r e) directionX = 0 := congrFun ho 1
  have hp2 : fderiv ℝ (normalizedGerm (sourceC L) (endpointPoint r e) (otherPoint r e) s)
      (endpointPoint r e) directionY = 0 := congrFun ho 2
  fin_cases e <;> fin_cases i <;>
    first | exact hp0 | exact hp1 | exact hp2 | exact hq.1 | exact hq.2.1 | exact hq.2.2

private theorem witness_hessian_identity {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hsep : I4Torus.torusProjection 2 L (endpointM r) ≠
      I4Torus.torusProjection 2 L (endpointS r)) (e : Fin 2) (j s : Fin 3) :
    finitePairing (endpointHessianCoefficient L r e j) (toSource L (witnessPoly L r e s)) =
      if j=s then 1 else 0 := by
  rw [endpointHessian_pairing hL,eval_witnessPoly,
    normalizedGerm_own_jet (sourceC L) (sourceC_ne_zero hL)
      (endpointPoint r e) (otherPoint r e) (multiplier_at_endpoint_pos hL r hsep e).ne' s]
  fin_cases j <;> rfl

/-- Two separate marginal right inverses in the unchanged original coefficient modes. -/
theorem actual_finite_endpointHessian_witnesses {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hsep : I4Torus.torusProjection 2 L (endpointM r) ≠
      I4Torus.torusProjection 2 L (endpointS r)) :
    ∃ v : Fin 2 → Fin 3 → (SourceMode 2 →₀ ℝ),
      (∀ e i s, finitePairing (rawPinCoefficient L r i) (v e s) = 0) ∧
      (∀ e j s, finitePairing (endpointHessianCoefficient L r e j) (v e s) =
        if j=s then 1 else 0) := by
  refine ⟨fun e s => toSource L (witnessPoly L r e s),?_,?_⟩
  · exact fun e i s => witness_raw_zero hL r hsep e s i
  · exact fun e j s => witness_hessian_identity hL r hsep e j s

/-- Actual marginal residual Gram positivity for every real rectangular3×6 correction. -/
theorem actual_endpointHessian_residual_coefficientGram_posDef {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hsep : I4Torus.torusProjection 2 L (endpointM r) ≠
      I4Torus.torusProjection 2 L (endpointS r))
    (e : Fin 2) (R : Matrix (Fin 3) (Fin 6) ℝ) :
    (I4ContactGram.coefficientGram (I4SourceFinitePinKernel.residualCoefficient
      (rawPinCoefficient L r) (endpointHessianCoefficient L r e) R)).PosDef := by
  obtain ⟨v,hker,hright⟩ := actual_finite_endpointHessian_witnesses hL r hsep
  exact coefficientGram_posDef_of_finite_kernel_rightInverse _ _ R
    (rawPinCoefficient_summable hL r) (endpointHessianCoefficient_summable hL r e)
    (v e) (hker e) (hright e)


end I4SourceEndpointHessianWitness
