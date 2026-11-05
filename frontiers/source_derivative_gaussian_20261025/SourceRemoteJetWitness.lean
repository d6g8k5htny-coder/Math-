import SourceFiniteTrig
import SourceTorus
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Tactic.FunProp

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

private theorem remoteJetCoefficient_summable {L : ℝ} (hL : L ≠ 0)
    (x : Fin 2 → ℝ) (j : Fin 6) : Summable (remoteJetCoefficient L x j) := by
  fin_cases j
  · change Summable (fun m => modeCoefficient 2 L m x)
    have he : derivativeCoefficient 2 L 0 x (fun i => Fin.elim0 i) =
        fun m => modeCoefficient 2 L m x := by
      funext m
      exact iteratedFDeriv_zero_apply _
    rw [← he]
    exact derivativeCoefficient_summable 2 hL 0 x (fun i => Fin.elim0 i)
  · exact derivativeCoefficient_summable 2 hL 1 x (fun _ => directionX)
  · exact derivativeCoefficient_summable 2 hL 1 x (fun _ => directionY)
  · exact derivativeCoefficient_summable 2 hL 2 x ![directionX,directionX]
  · exact derivativeCoefficient_summable 2 hL 2 x ![directionX,directionY]
  · exact derivativeCoefficient_summable 2 hL 2 x ![directionY,directionY]

private def rawFunctionPins (r : ℝ) (f : (Fin 2 → ℝ) → ℝ) : Fin 6 → ℝ :=
  ![f (endpointM r),f (endpointS r),
    fderiv ℝ f (endpointM r) directionX,fderiv ℝ f (endpointS r) directionX,
    fderiv ℝ f (endpointM r) directionY,fderiv ℝ f (endpointS r) directionY]

private theorem rawPin_pairing {L : ℝ} (hL : L ≠ 0) (r : ℝ) (p : TrigPoly) (i : Fin 6) :
    finitePairing (rawPinCoefficient L r i) (toSource L p) = rawFunctionPins r (eval L p) i := by
  change finitePairing (derivativeCoefficient 2 L (rawDerivativeOrder (Fin.castAdd 6 i))
    (rawDerivativePoint r (Fin.castAdd 6 i)) (rawDerivativeDirections (Fin.castAdd 6 i)))
      (toSource L p) = _
  rw [toSource_derivative hL]
  fin_cases i <;>
    first | exact iteratedFDeriv_zero_apply _ | exact iteratedFDeriv_one_apply _

/- Integrated once from frozen torus helper; section SHA256 24483ebad3befebc16ae12b498a606b73548989e2717c3c6242d99f8f7148c78. No helper object/kernel. -/
open I4Weights I4Torus

private theorem sourceC_ne_zero {L : ℝ} (hL : L ≠ 0) : sourceC L ≠ 0 := by
  exact div_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero) hL

private theorem cosine_sourceC_eq_one_iff {L : ℝ} (hL : L ≠ 0) (a b : ℝ) :
    Real.cos (sourceC L * (a - b)) = 1 ↔
      (a : AddCircle L) = (b : AddCircle L) := by
  constructor
  · intro hc
    obtain ⟨n, hn⟩ := (Real.cos_eq_one_iff _).mp hc
    have ht : 2 * Real.pi ≠ 0 := mul_ne_zero (by norm_num) Real.pi_ne_zero
    have hdiv : (n : ℝ) = (a - b) / L := by
      apply mul_left_cancel₀ ht
      calc
        (2 * Real.pi) * (n : ℝ) = (n : ℝ) * (2 * Real.pi) := by ring
        _ = sourceC L * (a - b) := hn
        _ = (2 * Real.pi) * ((a - b) / L) := by unfold sourceC; ring
    have hperiod : n • L = a - b := by
      simpa only [zsmul_eq_mul] using (eq_div_iff hL).mp hdiv
    have hz : ((a - b : ℝ) : AddCircle L) = 0 :=
      (AddCircle.coe_eq_zero_iff (p := L)).mpr ⟨n, hperiod⟩
    rw [AddCircle.coe_sub] at hz
    exact sub_eq_zero.mp hz
  · intro hab
    have hz : ((a - b : ℝ) : AddCircle L) = 0 := by
      rw [AddCircle.coe_sub]
      exact sub_eq_zero.mpr hab
    obtain ⟨n, hn⟩ := (AddCircle.coe_eq_zero_iff (p := L)).mp hz
    have hn' : (n : ℝ) * L = a - b := by
      simpa only [zsmul_eq_mul] using hn
    have hdiv : (n : ℝ) = (a - b) / L := (eq_div_iff hL).mpr hn'
    apply (Real.cos_eq_one_iff _).mpr
    refine ⟨n, ?_⟩
    calc
      (n : ℝ) * (2 * Real.pi) = (2 * Real.pi) * ((a - b) / L) := by
        rw [hdiv]
        ring
      _ = sourceC L * (a - b) := by unfold sourceC; ring

private theorem remote_positive_coordinate {L : ℝ} (hL : L ≠ 0)
    (x p : Fin 2 → ℝ)
    (hx : torusProjection 2 L x ≠ torusProjection 2 L p) :
    ∃ j : Fin 2, 0 < 1 - Real.cos (sourceC L * (x j - p j)) := by
  classical
  have hex : ∃ j : Fin 2, (x j : AddCircle L) ≠ (p j : AddCircle L) := by
    by_contra h
    push Not at h
    apply hx
    funext j
    exact h j
  obtain ⟨j, hj⟩ := hex
  refine ⟨j, sub_pos.mpr ?_⟩
  apply lt_of_le_of_ne (Real.cos_le_one _)
  intro hc
  exact hj ((cosine_sourceC_eq_one_iff hL (x j) (p j)).mp hc)


/- Integrated once from frozen arithmetic helper; section SHA256 7f59349e9b1b995314762a0bc886818dc6db59db027121a4c1663600d473a304. No helper object/kernel. -/
def jet2 (f : (Fin 2 → ℝ) → ℝ) (x : Fin 2 → ℝ) : Fin 6 → ℝ :=
  ![f x, fderiv ℝ f x directionX, fderiv ℝ f x directionY,
    iteratedFDeriv ℝ 2 f x ![directionX,directionX],
    iteratedFDeriv ℝ 2 f x ![directionX,directionY],
    iteratedFDeriv ℝ 2 f x ![directionY,directionY]]

def localGerm (c : ℝ) (x : Fin 2 → ℝ) (s : Fin 6) (y : Fin 2 → ℝ) : ℝ :=
  ![1, Real.sin (c*(y 0-x 0))/c, Real.sin (c*(y 1-x 1))/c,
    (1-Real.cos (c*(y 0-x 0)))/c^2,
    Real.sin (c*(y 0-x 0))*Real.sin (c*(y 1-x 1))/c^2,
    (1-Real.cos (c*(y 1-x 1)))/c^2] s

def mulJet2 (p q : Fin 6 → ℝ) : Fin 6 → ℝ :=
  ![p 0*q 0, p 1*q 0+p 0*q 1, p 2*q 0+p 0*q 2,
    p 3*q 0+2*p 1*q 1+p 0*q 3,
    p 4*q 0+p 1*q 2+p 2*q 1+p 0*q 4,
    p 5*q 0+2*p 2*q 2+p 0*q 5]

def inverseMulJet2Coefficients (p t : Fin 6 → ℝ) : Fin 6 → ℝ :=
  let a0 := t 0/p 0
  let a1 := (t 1-p 1*a0)/p 0
  let a2 := (t 2-p 2*a0)/p 0
  let a3 := (t 3-p 3*a0-2*p 1*a1)/p 0
  let a4 := (t 4-p 4*a0-p 1*a2-p 2*a1)/p 0
  let a5 := (t 5-p 5*a0-2*p 2*a2)/p 0
  ![a0,a1,a2,a3,a4,a5]

def interpolant (c : ℝ) (x : Fin 2 → ℝ) (P : (Fin 2 → ℝ) → ℝ)
    (t : Fin 6 → ℝ) (y : Fin 2 → ℝ) : ℝ :=
  P y * ∑ s : Fin 6, inverseMulJet2Coefficients (jet2 P x) t s * localGerm c x s y

private theorem localGerm_contDiff (c : ℝ) (x : Fin 2 → ℝ) (s : Fin 6) :
    ContDiff ℝ (⊤ : ℕ∞) (localGerm c x s) := by
  unfold localGerm
  fin_cases s <;> dsimp <;> fun_prop

private theorem directional_contDiff (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ 2 f) (v : Fin 2 → ℝ) :
    ContDiff ℝ 1 (fun y => fderiv ℝ f y v) := by
  exact (hf.fderiv_right (by norm_num)).clm_apply contDiff_const

private theorem directional_second (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ 2 f) (x u v : Fin 2 → ℝ) :
    fderiv ℝ (fun y => fderiv ℝ f y v) x u =
      iteratedFDeriv ℝ 2 f x ![u,v] := by
  have hdf : DifferentiableAt ℝ (fderiv ℝ f) x :=
    (hf.fderiv_right (m := 1) (by norm_num)).differentiable (by norm_num) x
  rw [fderiv_clm_apply hdf (differentiableAt_const v)]
  simp [iteratedFDeriv_two_apply]

private theorem product_second (P Q : (Fin 2 → ℝ) → ℝ)
    (hP : ContDiff ℝ 2 P) (hQ : ContDiff ℝ 2 Q) (x u v : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 2 (fun y => P y*Q y) x ![u,v] =
      iteratedFDeriv ℝ 2 P x ![u,v]*Q x +
      fderiv ℝ P x u*fderiv ℝ Q x v +
      fderiv ℝ P x v*fderiv ℝ Q x u +
      P x*iteratedFDeriv ℝ 2 Q x ![u,v] := by
  have hPdiff := hP.differentiable (by norm_num)
  have hQdiff := hQ.differentiable (by norm_num)
  have hDP := (directional_contDiff P hP v).differentiable (by norm_num)
  have hDQ := (directional_contDiff Q hQ v).differentiable (by norm_num)
  have hfun : (fun y => fderiv ℝ (fun z => P z*Q z) y v) =
      (fun y => P y*fderiv ℝ Q y v + Q y*fderiv ℝ P y v) := by
    funext y
    rw [fderiv_fun_mul (hPdiff y) (hQdiff y)]
    simp
  rw [← directional_second _ (hP.mul hQ), hfun]
  rw [fderiv_fun_add (f := fun y => P y*fderiv ℝ Q y v)
    (g := fun y => Q y*fderiv ℝ P y v)
    ((hPdiff x).mul (hDQ x)) ((hQdiff x).mul (hDP x)),
    fderiv_fun_mul (hPdiff x) (hDQ x), fderiv_fun_mul (hQdiff x) (hDP x)]
  simp only [add_apply, smul_apply, smul_eq_mul]
  rw [directional_second Q hQ, directional_second P hP]
  ring

theorem jet2_mul (P Q : (Fin 2 → ℝ) → ℝ)
    (hP : ContDiff ℝ 2 P) (hQ : ContDiff ℝ 2 Q) (x : Fin 2 → ℝ) :
    jet2 (fun y => P y*Q y) x = mulJet2 (jet2 P x) (jet2 Q x) := by
  have hPdiff := hP.differentiable (by norm_num)
  have hQdiff := hQ.differentiable (by norm_num)
  ext j
  fin_cases j <;> dsimp [jet2, mulJet2]
  · rw [fderiv_fun_mul (hPdiff x) (hQdiff x)]
    simp only [add_apply, smul_apply, smul_eq_mul]
    ring
  · rw [fderiv_fun_mul (hPdiff x) (hQdiff x)]
    simp only [add_apply, smul_apply, smul_eq_mul]
    ring
  · rw [product_second P Q hP hQ]
    ring
  · rw [product_second P Q hP hQ]
  · rw [product_second P Q hP hQ]
    ring

private theorem inverseMulJet2_right (p t : Fin 6 → ℝ) (hp : p 0 ≠ 0) :
    mulJet2 p (inverseMulJet2Coefficients p t) = t := by
  ext j
  fin_cases j <;> simp [mulJet2, inverseMulJet2Coefficients] <;> field_simp <;> ring

private theorem jet2_const (a : ℝ) (x : Fin 2 → ℝ) :
    jet2 (fun _ => a) x = ![a,0,0,0,0,0] := by
  ext j
  fin_cases j <;> simp [jet2, iteratedFDeriv_two_apply]

private theorem jet2_scale (a : ℝ) (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ 2 f) (x : Fin 2 → ℝ) :
    jet2 (fun y => a*f y) x = fun j => a*jet2 f x j := by
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

private theorem jet2_add (f g : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ 2 f) (hg : ContDiff ℝ 2 g) (x : Fin 2 → ℝ) :
    jet2 (fun y => f y+g y) x = jet2 f x+jet2 g x := by
  have h1 := fderiv_fun_add (hf.differentiable (by norm_num) x)
    (hg.differentiable (by norm_num) x)
  have h2 := iteratedFDeriv_add_apply (x := x) hf.contDiffAt hg.contDiffAt
  change iteratedFDeriv ℝ 2 (fun y => f y+g y) x = _ at h2
  ext j
  fin_cases j <;> dsimp [jet2]
  · rw [h1]
    rfl
  · rw [h1]
    rfl
  · rw [h2]
    rfl
  · rw [h2]
    rfl
  · rw [h2]
    rfl

private theorem phase_hasFDerivAt (c : ℝ) (z : Fin 2 → ℝ) (i : Fin 2)
    (y : Fin 2 → ℝ) :
    HasFDerivAt (fun w : Fin 2 → ℝ => c*(w i-z i))
      (c • (ContinuousLinearMap.proj i : (Fin 2 → ℝ) →L[ℝ] ℝ)) y := by
  simpa only [sub_zero, Pi.sub_apply] using
    ((hasFDerivAt_apply (𝕜 := ℝ) i y).sub (hasFDerivAt_const (𝕜 := ℝ) (z i) y)).const_mul c

private theorem axis_sin_first (c : ℝ) (z : Fin 2 → ℝ) (i : Fin 2)
    (y v : Fin 2 → ℝ) :
    fderiv ℝ (fun w => Real.sin (c*(w i-z i))) y v =
      Real.cos (c*(y i-z i))*c*v i := by
  rw [(phase_hasFDerivAt c z i y).sin.fderiv]
  simp
  ring

private theorem axis_cos_first (c : ℝ) (z : Fin 2 → ℝ) (i : Fin 2)
    (y v : Fin 2 → ℝ) :
    fderiv ℝ (fun w => Real.cos (c*(w i-z i))) y v =
      -Real.sin (c*(y i-z i))*c*v i := by
  rw [(phase_hasFDerivAt c z i y).cos.fderiv]
  simp
  ring

private theorem axis_sin_second (c : ℝ) (z : Fin 2 → ℝ) (i : Fin 2)
    (y u v : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 2 (fun w => Real.sin (c*(w i-z i))) y ![u,v] =
      -Real.sin (c*(y i-z i))*c^2*u i*v i := by
  have hf : ContDiff ℝ 2 (fun w : Fin 2 → ℝ => Real.sin (c*(w i-z i))) := by
    fun_prop
  have hfun : (fun w : Fin 2 → ℝ =>
      fderiv ℝ (fun a => Real.sin (c*(a i-z i))) w v) =
      (fun w => (c*v i)*Real.cos (c*(w i-z i))) := by
    funext w
    rw [axis_sin_first]
    ring
  rw [← directional_second _ hf, hfun,
    fderiv_const_mul (phase_hasFDerivAt c z i y).cos.differentiableAt]
  simp only [smul_apply, smul_eq_mul]
  rw [axis_cos_first]
  ring

private theorem axis_cos_second (c : ℝ) (z : Fin 2 → ℝ) (i : Fin 2)
    (y u v : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 2 (fun w => Real.cos (c*(w i-z i))) y ![u,v] =
      -Real.cos (c*(y i-z i))*c^2*u i*v i := by
  have hf : ContDiff ℝ 2 (fun w : Fin 2 → ℝ => Real.cos (c*(w i-z i))) := by
    fun_prop
  have hfun : (fun w : Fin 2 → ℝ =>
      fderiv ℝ (fun a => Real.cos (c*(a i-z i))) w v) =
      (fun w => (-c*v i)*Real.sin (c*(w i-z i))) := by
    funext w
    rw [axis_cos_first]
    ring
  rw [← directional_second _ hf, hfun,
    fderiv_const_mul (phase_hasFDerivAt c z i y).sin.differentiableAt]
  simp only [smul_apply, smul_eq_mul]
  rw [axis_sin_first]
  ring

private theorem axis_sin_jet (c : ℝ) (x : Fin 2 → ℝ) (i : Fin 2) :
    jet2 (fun y => Real.sin (c*(y i-x i))) x =
      ![0,c*directionX i,c*directionY i,0,0,0] := by
  ext j
  fin_cases j <;> simp [jet2, axis_sin_first, axis_sin_second]

private theorem axis_cos_jet (c : ℝ) (x : Fin 2 → ℝ) (i : Fin 2) :
    jet2 (fun y => Real.cos (c*(y i-x i))) x =
      ![1,0,0,-c^2*directionX i*directionX i,
        -c^2*directionX i*directionY i,-c^2*directionY i*directionY i] := by
  ext j
  fin_cases j <;> simp [jet2, axis_cos_first, axis_cos_second]

private theorem normalized_sin_jet (c : ℝ) (hc : c ≠ 0)
    (x : Fin 2 → ℝ) (i : Fin 2) :
    jet2 (fun y => Real.sin (c*(y i-x i))/c) x =
      ![0,directionX i,directionY i,0,0,0] := by
  have hf : ContDiff ℝ 2 (fun y : Fin 2 → ℝ => Real.sin (c*(y i-x i))) := by
    fun_prop
  have hfun : (fun y : Fin 2 → ℝ => Real.sin (c*(y i-x i))/c) =
      (fun y => c⁻¹*Real.sin (c*(y i-x i))) := by
    funext y
    simp [div_eq_mul_inv, mul_comm]
  rw [hfun, jet2_scale _ _ hf, axis_sin_jet]
  ext j
  fin_cases j <;> simp [hc]

private theorem normalized_cos_jet (c : ℝ) (hc : c ≠ 0)
    (x : Fin 2 → ℝ) (i : Fin 2) :
    jet2 (fun y => (1-Real.cos (c*(y i-x i)))/c^2) x =
      ![0,0,0,directionX i*directionX i,
        directionX i*directionY i,directionY i*directionY i] := by
  have hf : ContDiff ℝ 2 (fun y : Fin 2 → ℝ => Real.cos (c*(y i-x i))) := by
    fun_prop
  have hn : ContDiff ℝ 2 (fun y : Fin 2 → ℝ =>
      1+(-1)*Real.cos (c*(y i-x i))) := by fun_prop
  have hfun : (fun y : Fin 2 → ℝ => (1-Real.cos (c*(y i-x i)))/c^2) =
      (fun y => (c^2)⁻¹*(1+(-1)*Real.cos (c*(y i-x i)))) := by
    funext y
    simp [div_eq_mul_inv, mul_comm, sub_eq_add_neg]
  have hneg : ContDiff ℝ 2 (fun y : Fin 2 → ℝ => -1*Real.cos (c*(y i-x i))) := by
    fun_prop
  rw [hfun, jet2_scale _ _ hn, jet2_add _ _ contDiff_const hneg,
    jet2_const, jet2_scale _ _ hf, axis_cos_jet]
  ext j
  fin_cases j <;> simp <;> field_simp

theorem localGerm_jet2 (c : ℝ) (hc : c ≠ 0) (x : Fin 2 → ℝ) (j s : Fin 6) :
    jet2 (localGerm c x s) x j = if j=s then 1 else 0 := by
  fin_cases s
  · change jet2 (fun _ => 1) x j = _
    rw [jet2_const]
    fin_cases j <;> norm_num
  · change jet2 (fun y => Real.sin (c*(y 0-x 0))/c) x j = _
    rw [normalized_sin_jet c hc x 0]
    fin_cases j <;> norm_num [directionX, directionY]
  · change jet2 (fun y => Real.sin (c*(y 1-x 1))/c) x j = _
    rw [normalized_sin_jet c hc x 1]
    fin_cases j <;> norm_num [directionX, directionY]
  · change jet2 (fun y => (1-Real.cos (c*(y 0-x 0)))/c^2) x j = _
    rw [normalized_cos_jet c hc x 0]
    fin_cases j <;> norm_num [directionX, directionY]
  · have hfun : localGerm c x 4 = (fun y =>
        (Real.sin (c*(y 0-x 0))/c)*(Real.sin (c*(y 1-x 1))/c)) := by
      funext y
      dsimp [localGerm]
      field_simp
    change jet2 (localGerm c x 4) x j = if j=4 then 1 else 0
    rw [hfun, jet2_mul]
    · rw [normalized_sin_jet c hc x 0, normalized_sin_jet c hc x 1]
      fin_cases j <;> norm_num [mulJet2, directionX, directionY]
    · fun_prop
    · fun_prop
  · change jet2 (fun y => (1-Real.cos (c*(y 1-x 1)))/c^2) x j = _
    rw [normalized_cos_jet c hc x 1]
    fin_cases j <;> norm_num [directionX, directionY]

private theorem jet2_sum (f : Fin 6 → (Fin 2 → ℝ) → ℝ)
    (hf : ∀ s, ContDiff ℝ 2 (f s)) (x : Fin 2 → ℝ) :
    jet2 (fun y => ∑ s, f s y) x = fun j => ∑ s, jet2 (f s) x j := by
  have h1 : fderiv ℝ (fun y => ∑ s, f s y) x = ∑ s, fderiv ℝ (f s) x :=
    fderiv_fun_sum (fun s _ => (hf s).differentiable (by norm_num) x)
  have h2 : iteratedFDeriv ℝ 2 (fun y => ∑ s, f s y) x =
      ∑ s, iteratedFDeriv ℝ 2 (f s) x :=
    iteratedFDeriv_fun_sum_apply (fun s _ => (hf s).contDiffAt)
  ext j
  fin_cases j <;> dsimp [jet2]
  · rw [h1]
    simp
  · rw [h1]
    simp
  · rw [h2]
    simp
  · rw [h2]
    simp
  · rw [h2]
    simp

private theorem jet2_germ_combination (c : ℝ) (hc : c ≠ 0)
    (x : Fin 2 → ℝ) (a : Fin 6 → ℝ) :
    jet2 (fun y => ∑ s, a s*localGerm c x s y) x = a := by
  have hsmooth : ∀ s, ContDiff ℝ 2 (localGerm c x s) :=
    fun s => (localGerm_contDiff c x s).of_le (by norm_num)
  have hscale : ∀ s, ContDiff ℝ 2 (fun y => a s*localGerm c x s y) :=
    fun s => contDiff_const.mul (hsmooth s)
  rw [jet2_sum _ hscale]
  ext j
  calc
    (∑ s, jet2 (fun y => a s*localGerm c x s y) x j) =
        ∑ s, a s*(if j=s then 1 else 0) := by
      apply Finset.sum_congr rfl
      intro s _
      rw [jet2_scale _ _ (hsmooth s)]
      exact congrArg (fun z : ℝ => a s*z) (localGerm_jet2 c hc x j s)
    _ = a j := by simp

theorem jet2_interpolate_mul (c : ℝ) (hc : c ≠ 0) (x : Fin 2 → ℝ)
    (P : (Fin 2 → ℝ) → ℝ) (hP : ContDiff ℝ 2 P) (hp : P x ≠ 0)
    (t : Fin 6 → ℝ) :
    jet2 (interpolant c x P t) x = t := by
  have hsmooth : ∀ s, ContDiff ℝ 2 (localGerm c x s) :=
    fun s => (localGerm_contDiff c x s).of_le (by norm_num)
  have hQ : ContDiff ℝ 2 (fun y => ∑ s : Fin 6,
      inverseMulJet2Coefficients (jet2 P x) t s*localGerm c x s y) :=
    ContDiff.sum (fun s _ => contDiff_const.mul (hsmooth s))
  unfold interpolant
  rw [jet2_mul P _ hP hQ, jet2_germ_combination c hc]
  exact inverseMulJet2_right (jet2 P x) t hp


private theorem remoteJet_pairing {L : ℝ} (hL : L ≠ 0) (p : TrigPoly)
    (x : Fin 2 → ℝ) (j : Fin 6) :
    finitePairing (remoteJetCoefficient L x j) (toSource L p) = jet2 (eval L p) x j := by
  fin_cases j
  · exact toSource_eval hL p x
  · exact (toSource_derivative hL p 1 x (fun _ => directionX)).trans
      (iteratedFDeriv_one_apply _)
  · exact (toSource_derivative hL p 1 x (fun _ => directionY)).trans
      (iteratedFDeriv_one_apply _)
  · exact toSource_derivative hL p 2 x ![directionX,directionX]
  · exact toSource_derivative hL p 2 x ![directionX,directionY]
  · exact toSource_derivative hL p 2 x ![directionY,directionY]

private def germPoly (L : ℝ) (x : Fin 2 → ℝ) : Fin 6 → TrigPoly :=
  ![constant 1,
    scale (sourceC L)⁻¹ (axisSinPoly L x 0),
    scale (sourceC L)⁻¹ (axisSinPoly L x 1),
    scale ((sourceC L)^2)⁻¹ (factorPoly L x 0),
    scale ((sourceC L)^2)⁻¹ (mul (axisSinPoly L x 0) (axisSinPoly L x 1)),
    scale ((sourceC L)^2)⁻¹ (factorPoly L x 1)]

private theorem eval_germPoly (L : ℝ) (x : Fin 2 → ℝ) (s : Fin 6) (y : Fin 2 → ℝ) :
    eval L (germPoly L x s) y = localGerm (sourceC L) x s y := by
  fin_cases s
  · exact eval_constant L 1 y
  · change eval L (scale (sourceC L)⁻¹ (axisSinPoly L x 0)) y =
      Real.sin (sourceC L*(y 0-x 0))/sourceC L
    rw [eval_scale,eval_axisSinPoly]
    ring
  · change eval L (scale (sourceC L)⁻¹ (axisSinPoly L x 1)) y =
      Real.sin (sourceC L*(y 1-x 1))/sourceC L
    rw [eval_scale,eval_axisSinPoly]
    ring
  · change eval L (scale ((sourceC L)^2)⁻¹ (factorPoly L x 0)) y =
      (1-Real.cos (sourceC L*(y 0-x 0)))/(sourceC L)^2
    rw [eval_scale,eval_factorPoly]
    simp only [pinFactor,div_eq_mul_inv]
    ring
  · change eval L (scale ((sourceC L)^2)⁻¹
      (mul (axisSinPoly L x 0) (axisSinPoly L x 1))) y =
        Real.sin (sourceC L*(y 0-x 0))*Real.sin (sourceC L*(y 1-x 1))/(sourceC L)^2
    rw [eval_scale,eval_mul,eval_axisSinPoly,eval_axisSinPoly]
    ring
  · change eval L (scale ((sourceC L)^2)⁻¹ (factorPoly L x 1)) y =
      (1-Real.cos (sourceC L*(y 1-x 1)))/(sourceC L)^2
    rw [eval_scale,eval_factorPoly]
    simp only [pinFactor,div_eq_mul_inv]
    ring

private def combinationPoly (L : ℝ) (x : Fin 2 → ℝ) (a : Fin 6 → ℝ) : TrigPoly :=
  scale (a 0) (germPoly L x 0) ++ scale (a 1) (germPoly L x 1) ++
  scale (a 2) (germPoly L x 2) ++ scale (a 3) (germPoly L x 3) ++
  scale (a 4) (germPoly L x 4) ++ scale (a 5) (germPoly L x 5)

private theorem eval_combinationPoly (L : ℝ) (x : Fin 2 → ℝ) (a : Fin 6 → ℝ)
    (y : Fin 2 → ℝ) :
    eval L (combinationPoly L x a) y = ∑ s, a s * localGerm (sourceC L) x s y := by
  simp [combinationPoly,eval_append,eval_scale,eval_germPoly,Fin.sum_univ_succ]

private def witnessPoly (L r : ℝ) (x : Fin 2 → ℝ) (jM jS : Fin 2)
    (t : Fin 6 → ℝ) : TrigPoly :=
  mul (annihilatorPoly L r jM jS)
    (combinationPoly L x (inverseMulJet2Coefficients (jet2 (annihilator L r jM jS) x) t))

private theorem eval_witnessPoly (L r : ℝ) (x : Fin 2 → ℝ) (jM jS : Fin 2)
    (t : Fin 6 → ℝ) :
    eval L (witnessPoly L r x jM jS t) =
      interpolant (sourceC L) x (annihilator L r jM jS) t := by
  funext y
  rw [witnessPoly,eval_mul,eval_annihilatorPoly,eval_combinationPoly]
  rfl

private theorem interpolant_pin_zero (L r : ℝ) (x : Fin 2 → ℝ) (jM jS : Fin 2)
    (t : Fin 6 → ℝ) :
    rawFunctionPins r (interpolant (sourceC L) x (annihilator L r jM jS) t) = 0 := by
  let P := annihilator L r jM jS
  let a := inverseMulJet2Coefficients (jet2 P x) t
  let Q := fun y => ∑ s, a s * localGerm (sourceC L) x s y
  have hP : Differentiable ℝ P := (annihilator_contDiff L r jM jS).differentiable (by simp)
  have hQtop : ContDiff ℝ (⊤ : ℕ∞) Q :=
    ContDiff.sum (fun s _ => contDiff_const.mul (localGerm_contDiff (sourceC L) x s))
  have hQ := hQtop.differentiable (by simp)
  obtain ⟨hvM,hvS⟩ := annihilator_pin_values L r jM jS
  obtain ⟨hdM,hdS⟩ := annihilator_pin_derivatives L r jM jS
  change P (endpointM r) = 0 at hvM
  change P (endpointS r) = 0 at hvS
  change fderiv ℝ P (endpointM r) = 0 at hdM
  change fderiv ℝ P (endpointS r) = 0 at hdS
  have hFM : interpolant (sourceC L) x P t (endpointM r) = 0 := by
    change P (endpointM r)*Q (endpointM r) = 0
    rw [hvM]
    simp
  have hFS : interpolant (sourceC L) x P t (endpointS r) = 0 := by
    change P (endpointS r)*Q (endpointS r) = 0
    rw [hvS]
    simp
  have hdFM : fderiv ℝ (interpolant (sourceC L) x P t) (endpointM r) = 0 := by
    change fderiv ℝ (fun y => P y*Q y) (endpointM r) = 0
    rw [fderiv_fun_mul (hP _) (hQ _),hvM,hdM]
    simp
  have hdFS : fderiv ℝ (interpolant (sourceC L) x P t) (endpointS r) = 0 := by
    change fderiv ℝ (fun y => P y*Q y) (endpointS r) = 0
    rw [fderiv_fun_mul (hP _) (hQ _),hvS,hdS]
    simp
  change rawFunctionPins r (interpolant (sourceC L) x P t) = 0
  ext i
  fin_cases i <;> simp [rawFunctionPins,hFM,hFS,hdFM,hdFS]

/-- Concrete finite original-mode directions annihilate all six literal raw
pins and interpolate the full remote six-jet. Repeated pins and arbitrary
radius are allowed; the only geometry is remote separation from each pin. -/
theorem actual_finite_remoteJet_witnesses {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x : Fin 2 → ℝ)
    (hxM : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointM r))
    (hxS : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointS r)) :
    ∃ v : Fin 6 → (SourceMode 2 →₀ ℝ),
      (∀ i s, finitePairing (rawPinCoefficient L r i) (v s) = 0) ∧
      (∀ j s, finitePairing (remoteJetCoefficient L x j) (v s) = if j=s then 1 else 0) := by
  obtain ⟨jM,hM⟩ := remote_positive_coordinate hL x (endpointM r) hxM
  obtain ⟨jS,hS⟩ := remote_positive_coordinate hL x (endpointS r) hxS
  have hpx : 0 < annihilator L r jM jS x := mul_pos (pow_pos hM 2) (pow_pos hS 2)
  have hP2 : ContDiff ℝ 2 (annihilator L r jM jS) :=
    (annihilator_contDiff L r jM jS).of_le (by norm_num)
  refine ⟨fun s => toSource L (witnessPoly L r x jM jS (fun j => if j=s then 1 else 0)),?_,?_⟩
  · intro i s
    rw [rawPin_pairing hL,eval_witnessPoly]
    exact congrFun (interpolant_pin_zero L r x jM jS (fun j => if j=s then 1 else 0)) i
  · intro j s
    rw [remoteJet_pairing hL,eval_witnessPoly]
    exact congrFun (jet2_interpolate_mul (sourceC L) (sourceC_ne_zero hL) x
      (annihilator L r jM jS) hP2 hpx.ne' (fun j => if j=s then 1 else 0)) j

/-- Actual remote residual coefficient Gram positivity for EVERY finite
correction matrix, without a pin-inverse, target or conditional-law premise. -/
theorem actual_remote_residual_coefficientGram_posDef {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x : Fin 2 → ℝ)
    (hxM : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointM r))
    (hxS : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointS r))
    (R : Matrix (Fin 6) (Fin 6) ℝ) :
    (I4ContactGram.coefficientGram
      (residualCoefficient (rawPinCoefficient L r) (remoteJetCoefficient L x) R)).PosDef := by
  obtain ⟨v,hker,hright⟩ := actual_finite_remoteJet_witnesses hL r x hxM hxS
  exact coefficientGram_posDef_of_finite_kernel_rightInverse _ _ R
    (rawPinCoefficient_summable hL r) (remoteJetCoefficient_summable hL x) v hker hright

end I4SourceRemoteJetWitness
