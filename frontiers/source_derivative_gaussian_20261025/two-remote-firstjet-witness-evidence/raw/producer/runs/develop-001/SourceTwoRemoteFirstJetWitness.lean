import SourceRemoteJetWitness
import Lean.Elab.Tactic.Omega

/-! Actual joint first-jet-six finite directions modulo the literal raw pins.
Repeated pins and arbitrary signed radii are retained. No joint Gaussian law is asserted. -/

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix Topology
open I4Source I4Weights I4SourceDerivativeGaussian I4SourceConfluentPins
open I4SourceConfluentLimits I4SourceRawPinConditioning I4SourceFinitePinKernel
open I4SourceFiniteTrig I4SourceRemoteJetWitness

namespace I4SourceTwoRemoteFirstJetWitness

/-- Literal joint order: valueX,dxX,dyX,valueY,dxY,dyY. -/
def twoRemoteFirstJetCoefficient (L : ℝ) (x y : Fin 2 → ℝ) : Fin 6 → SourceMode 2 → ℝ :=
  ![remoteJetCoefficient L x 0,remoteJetCoefficient L x 1,remoteJetCoefficient L x 2,
    remoteJetCoefficient L y 0,remoteJetCoefficient L y 1,remoteJetCoefficient L y 2]

-- Integrated once from frozen text-only minimal first-jet arithmetic helper.
/- Text-only first-jet arithmetic for one integration into
I4SourceTwoRemoteFirstJetWitness. Uncompiled helper; producer's new-module
qualification covers the actual integrated text. Only germs0/1/2 are used. -/

private def firstJet (f : (Fin 2 → ℝ) → ℝ) (p : Fin 2 → ℝ) : Fin 3 → ℝ :=
  ![f p, fderiv ℝ f p directionX, fderiv ℝ f p directionY]

private def firstJetProduct (a b : Fin 3 → ℝ) : Fin 3 → ℝ :=
  ![a 0*b 0, a 1*b 0+a 0*b 1, a 2*b 0+a 0*b 2]

private def firstJetCoefficients (P : (Fin 2 → ℝ) → ℝ) (p : Fin 2 → ℝ)
    (t : Fin 3 → ℝ) : Fin 3 → ℝ :=
  let a0 := t 0/P p
  ![a0, (t 1-fderiv ℝ P p directionX*a0)/P p,
    (t 2-fderiv ℝ P p directionY*a0)/P p]

private def firstJetInterpolant (c : ℝ) (p : Fin 2 → ℝ)
    (P : (Fin 2 → ℝ) → ℝ) (t : Fin 3 → ℝ) (z : Fin 2 → ℝ) : ℝ :=
  P z * ∑ s : Fin 3,
    firstJetCoefficients P p t s * localGerm c p (Fin.castAdd 3 s) z

private theorem firstJet_mul (P Q : (Fin 2 → ℝ) → ℝ)
    (hP : ContDiff ℝ 2 P) (hQ : ContDiff ℝ 2 Q) (p : Fin 2 → ℝ) :
    firstJet (fun z => P z*Q z) p =
      firstJetProduct (firstJet P p) (firstJet Q p) := by
  have h := jet2_mul P Q hP hQ p
  ext j
  have hj := congrFun h (Fin.castAdd 3 j)
  fin_cases j <;> simpa [firstJet, firstJetProduct, jet2, mulJet2] using hj

private theorem firstJet_scale (a : ℝ) (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ 2 f) (p : Fin 2 → ℝ) :
    firstJet (fun z => a*f z) p = fun j => a*firstJet f p j := by
  have h := fderiv_const_mul (hf.differentiable (by norm_num) p) a
  ext j
  fin_cases j
  · rfl
  · change fderiv ℝ (fun z => a*f z) p directionX = a*fderiv ℝ f p directionX
    rw [h]
    simp
  · change fderiv ℝ (fun z => a*f z) p directionY = a*fderiv ℝ f p directionY
    rw [h]
    simp

private theorem firstJet_sum (f : Fin 3 → (Fin 2 → ℝ) → ℝ)
    (hf : ∀ s, ContDiff ℝ 2 (f s)) (p : Fin 2 → ℝ) :
    firstJet (fun z => ∑ s, f s z) p = fun j => ∑ s, firstJet (f s) p j := by
  have h : fderiv ℝ (fun z => ∑ s, f s z) p = ∑ s, fderiv ℝ (f s) p :=
    fderiv_fun_sum (fun s _ => (hf s).differentiable (by norm_num) p)
  ext j
  fin_cases j
  · rfl
  · change fderiv ℝ (fun z => ∑ s, f s z) p directionX =
      ∑ s, fderiv ℝ (f s) p directionX
    rw [h]
    simp
  · change fderiv ℝ (fun z => ∑ s, f s z) p directionY =
      ∑ s, fderiv ℝ (f s) p directionY
    rw [h]
    simp

private theorem firstJetGerm_contDiff (c : ℝ) (p : Fin 2 → ℝ) (s : Fin 3) :
    ContDiff ℝ 2 (localGerm c p (Fin.castAdd 3 s)) := by
  fin_cases s
  · change ContDiff ℝ 2 (fun _ : Fin 2 → ℝ => (1:ℝ))
    exact contDiff_const
  · change ContDiff ℝ 2 (fun z : Fin 2 → ℝ => Real.sin (c*(z 0-p 0))/c)
    fun_prop
  · change ContDiff ℝ 2 (fun z : Fin 2 → ℝ => Real.sin (c*(z 1-p 1))/c)
    fun_prop

private theorem firstJet_localGerm (c : ℝ) (hc : c ≠ 0) (p : Fin 2 → ℝ)
    (j s : Fin 3) :
    firstJet (localGerm c p (Fin.castAdd 3 s)) p j = if j=s then 1 else 0 := by
  have h := localGerm_jet2 c hc p (Fin.castAdd 3 j) (Fin.castAdd 3 s)
  fin_cases j <;> fin_cases s <;> simpa [firstJet, jet2] using h

private theorem firstJet_germ_combination (c : ℝ) (hc : c ≠ 0)
    (p : Fin 2 → ℝ) (a : Fin 3 → ℝ) :
    firstJet (fun z => ∑ s : Fin 3, a s*localGerm c p (Fin.castAdd 3 s) z) p = a := by
  have hsmooth : ∀ s : Fin 3, ContDiff ℝ 2 (localGerm c p (Fin.castAdd 3 s)) :=
    firstJetGerm_contDiff c p
  have hscale : ∀ s : Fin 3,
      ContDiff ℝ 2 (fun z => a s*localGerm c p (Fin.castAdd 3 s) z) :=
    fun s => contDiff_const.mul (hsmooth s)
  rw [firstJet_sum _ hscale]
  ext j
  calc
    (∑ s : Fin 3, firstJet (fun z => a s*localGerm c p (Fin.castAdd 3 s) z) p j) =
        ∑ s : Fin 3, a s*(if j=s then 1 else 0) := by
      apply Finset.sum_congr rfl
      intro s _
      rw [firstJet_scale _ _ (hsmooth s)]
      exact congrArg (fun v : ℝ => a s*v) (firstJet_localGerm c hc p j s)
    _ = a j := by simp

private theorem firstJetInterpolant_contDiff (c : ℝ) (p : Fin 2 → ℝ)
    (P : (Fin 2 → ℝ) → ℝ) (hP : ContDiff ℝ 2 P) (t : Fin 3 → ℝ) :
    ContDiff ℝ 2 (firstJetInterpolant c p P t) := by
  exact hP.mul (ContDiff.sum (fun s _ =>
    contDiff_const.mul (firstJetGerm_contDiff c p s)))

private theorem firstJetInterpolant_self (c : ℝ) (hc : c ≠ 0) (p : Fin 2 → ℝ)
    (P : (Fin 2 → ℝ) → ℝ) (hP : ContDiff ℝ 2 P) (hPp : P p ≠ 0)
    (t : Fin 3 → ℝ) :
    firstJet (firstJetInterpolant c p P t) p = t := by
  have hQ : ContDiff ℝ 2 (fun z => ∑ s : Fin 3,
      firstJetCoefficients P p t s * localGerm c p (Fin.castAdd 3 s) z) :=
    ContDiff.sum (fun s _ => contDiff_const.mul (firstJetGerm_contDiff c p s))
  unfold firstJetInterpolant
  rw [firstJet_mul P _ hP hQ, firstJet_germ_combination c hc]
  ext j
  fin_cases j <;> simp [firstJetProduct, firstJetCoefficients, firstJet] <;>
    field_simp [hPp] <;> ring

private theorem firstJetInterpolant_zero (c : ℝ) (p : Fin 2 → ℝ)
    (P : (Fin 2 → ℝ) → ℝ) (hP : ContDiff ℝ 2 P) (q : Fin 2 → ℝ)
    (hPq : P q = 0) (hdPq : fderiv ℝ P q = 0) (t : Fin 3 → ℝ) :
    firstJet (firstJetInterpolant c p P t) q = 0 := by
  have hQ : ContDiff ℝ 2 (fun z => ∑ s : Fin 3,
      firstJetCoefficients P p t s * localGerm c p (Fin.castAdd 3 s) z) :=
    ContDiff.sum (fun s _ => contDiff_const.mul (firstJetGerm_contDiff c p s))
  unfold firstJetInterpolant
  rw [firstJet_mul P _ hP hQ]
  ext j
  fin_cases j <;> simp [firstJetProduct, firstJet, hPq, hdPq]


private theorem sourceC_ne_zero {L : ℝ} (hL : L ≠ 0) : sourceC L ≠ 0 :=
  div_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero) hL

private theorem circle_eq_of_cos_one {L : ℝ} (hL : L ≠ 0) (u v : ℝ)
    (hc : Real.cos (sourceC L*(u-v))=1) : (u : AddCircle L)=(v : AddCircle L) := by
  obtain ⟨n,hn⟩ := (Real.cos_eq_one_iff _).mp hc
  have hπ : 2*Real.pi ≠ 0 := mul_ne_zero (by norm_num) Real.pi_ne_zero
  have hd : (n:ℝ)=(u-v)/L := by
    apply mul_left_cancel₀ hπ
    calc
      (2*Real.pi)*(n:ℝ) = (n:ℝ)*(2*Real.pi) := by ring
      _ = sourceC L*(u-v) := hn
      _ = (2*Real.pi)*((u-v)/L) := by unfold sourceC; ring
  have hp : n • L = u-v := by simpa only [zsmul_eq_mul] using (eq_div_iff hL).mp hd
  have hz : ((u-v:ℝ):AddCircle L)=0 := (AddCircle.coe_eq_zero_iff (p:=L)).mpr ⟨n,hp⟩
  rw [AddCircle.coe_sub] at hz
  exact sub_eq_zero.mp hz

private theorem positive_axis {L : ℝ} (hL : L ≠ 0) (p a : Fin 2 → ℝ)
    (hpa : I4Torus.torusProjection 2 L p ≠ I4Torus.torusProjection 2 L a) :
    ∃ j : Fin 2, 0 < 1-Real.cos (sourceC L*(p j-a j)) := by
  have hcoord : ∃ j : Fin 2, (p j : AddCircle L) ≠ (a j : AddCircle L) := by
    by_contra h
    push_neg at h
    apply hpa
    funext j
    exact h j
  obtain ⟨j,hj⟩ := hcoord
  refine ⟨j,sub_pos.mpr (lt_of_le_of_ne (Real.cos_le_one _) ?_)⟩
  intro hc
  exact hj (circle_eq_of_cos_one hL _ _ hc)

private def squaredFactor (c : ℝ) (a : Fin 2 → ℝ) (j : Fin 2) (z : Fin 2 → ℝ) : ℝ :=
  (1-Real.cos (c*(z j-a j)))^2

private theorem squaredFactor_C2 (c : ℝ) (a : Fin 2 → ℝ) (j : Fin 2) :
    ContDiff ℝ 2 (squaredFactor c a j) := by
  unfold squaredFactor
  fun_prop

private theorem squaredFactor_zero (c : ℝ) (a : Fin 2 → ℝ) (j : Fin 2) :
    squaredFactor c a j a = 0 ∧ fderiv ℝ (squaredFactor c a j) a=0 := by
  constructor
  · simp [squaredFactor]
  · have hA : DifferentiableAt ℝ (fun z : Fin 2 → ℝ => 1-Real.cos (c*(z j-a j))) a := by fun_prop
    have h := (hA.hasFDerivAt.pow 2).fderiv
    change fderiv ℝ (squaredFactor c a j) a = _ at h
    simpa using h

private def tripleMultiplier (c : ℝ) (a : Fin 3 → (Fin 2 → ℝ)) (k : Fin 3 → Fin 2)
    (z : Fin 2 → ℝ) : ℝ :=
  squaredFactor c (a 0) (k 0) z * squaredFactor c (a 1) (k 1) z * squaredFactor c (a 2) (k 2) z

private theorem tripleMultiplier_C2 (c : ℝ) (a : Fin 3 → (Fin 2 → ℝ)) (k : Fin 3 → Fin 2) :
    ContDiff ℝ 2 (tripleMultiplier c a k) :=
  ((squaredFactor_C2 c (a 0) (k 0)).mul (squaredFactor_C2 c (a 1) (k 1))).mul
    (squaredFactor_C2 c (a 2) (k 2))

private theorem tripleMultiplier_zero (c : ℝ) (a : Fin 3 → (Fin 2 → ℝ))
    (k : Fin 3 → Fin 2) (i : Fin 3) :
    tripleMultiplier c a k (a i)=0 ∧ fderiv ℝ (tripleMultiplier c a k) (a i)=0 := by
  have hA (j : Fin 3) := (squaredFactor_C2 c (a j) (k j)).differentiable (by norm_num)
  have hz (j : Fin 3) := squaredFactor_zero c (a j) (k j)
  constructor
  · fin_cases i <;> simp [tripleMultiplier,(hz 0).1,(hz 1).1,(hz 2).1]
  · change fderiv ℝ (fun z => (squaredFactor c (a 0) (k 0) z *
      squaredFactor c (a 1) (k 1) z) * squaredFactor c (a 2) (k 2) z) (a i)=0
    rw [fderiv_fun_mul ((hA 0 (a i)).mul (hA 1 (a i))) (hA 2 (a i)),
      fderiv_fun_mul (hA 0 (a i)) (hA 1 (a i))]
    fin_cases i <;> simp [(hz 0).1,(hz 0).2,(hz 1).1,(hz 1).2,(hz 2).1,(hz 2).2]

private def axisCos (L : ℝ) (a : Fin 2 → ℝ) (j : Fin 2) : TrigPoly :=
  translate L a [⟨1,Pi.single j 1,0⟩]

private def axisSin (L : ℝ) (a : Fin 2 → ℝ) (j : Fin 2) : TrigPoly :=
  translate L a [⟨1,Pi.single j 1,-Real.pi/2⟩]

private theorem eval_axisCos (L : ℝ) (a z : Fin 2 → ℝ) (j : Fin 2) :
    eval L (axisCos L a j) z=Real.cos (sourceC L*(z j-a j)) := by
  rw [axisCos,eval_translate]
  fin_cases j <;> simp [eval,termEval,phase,sourceC,Fin.sum_univ_succ]

private theorem eval_axisSin (L : ℝ) (a z : Fin 2 → ℝ) (j : Fin 2) :
    eval L (axisSin L a j) z=Real.sin (sourceC L*(z j-a j)) := by
  have hp : phase 2 L (Pi.single j 1) (z-a)=sourceC L*(z j-a j) := by
    fin_cases j <;> simp [phase,sourceC,Fin.sum_univ_succ]
  rw [axisSin,eval_translate]
  simpa [eval,termEval,hp,sub_eq_add_neg,neg_div] using
    Real.cos_sub_pi_div_two (sourceC L*(z j-a j))

private def squaredFactorPoly (L : ℝ) (a : Fin 2 → ℝ) (j : Fin 2) : TrigPoly :=
  let A := constant 1 ++ scale (-1) (axisCos L a j)
  mul A A

private theorem eval_squaredFactorPoly (L : ℝ) (a z : Fin 2 → ℝ) (j : Fin 2) :
    eval L (squaredFactorPoly L a j) z=squaredFactor (sourceC L) a j z := by
  simp only [squaredFactorPoly,eval_mul,eval_append,eval_constant,eval_scale,eval_axisCos]
  simp only [squaredFactor,pow_two]
  ring

private def tripleMultiplierPoly (L : ℝ) (a : Fin 3 → (Fin 2 → ℝ))
    (k : Fin 3 → Fin 2) : TrigPoly :=
  mul (mul (squaredFactorPoly L (a 0) (k 0)) (squaredFactorPoly L (a 1) (k 1)))
    (squaredFactorPoly L (a 2) (k 2))

private theorem eval_tripleMultiplierPoly (L : ℝ) (a : Fin 3 → (Fin 2 → ℝ))
    (k : Fin 3 → Fin 2) : eval L (tripleMultiplierPoly L a k)=tripleMultiplier (sourceC L) a k := by
  funext z
  simp only [tripleMultiplierPoly,eval_mul,eval_squaredFactorPoly,tripleMultiplier]

private def firstGermPoly (L : ℝ) (p : Fin 2 → ℝ) (j : Fin 3) : TrigPoly :=
  ![constant 1,scale (sourceC L)⁻¹ (axisSin L p 0),scale (sourceC L)⁻¹ (axisSin L p 1)] j

private theorem eval_firstGermPoly (L : ℝ) (p z : Fin 2 → ℝ) (j : Fin 3) :
    eval L (firstGermPoly L p j) z=localGerm (sourceC L) p (Fin.castAdd 3 j) z := by
  fin_cases j <;> simp [firstGermPoly,localGerm,eval_constant,eval_scale,eval_axisSin,
    div_eq_mul_inv,mul_comm]

private def interpolationPoly (L : ℝ) (p : Fin 2 → ℝ) (a : Fin 3 → (Fin 2 → ℝ))
    (k : Fin 3 → Fin 2) (t : Fin 3 → ℝ) : TrigPoly :=
  mul (tripleMultiplierPoly L a k)
    ((scale (firstJetCoefficients (tripleMultiplier (sourceC L) a k) p t 0) (firstGermPoly L p 0) ++
      scale (firstJetCoefficients (tripleMultiplier (sourceC L) a k) p t 1) (firstGermPoly L p 1)) ++
      scale (firstJetCoefficients (tripleMultiplier (sourceC L) a k) p t 2) (firstGermPoly L p 2))

private theorem eval_interpolationPoly (L : ℝ) (p : Fin 2 → ℝ)
    (a : Fin 3 → (Fin 2 → ℝ)) (k : Fin 3 → Fin 2) (t : Fin 3 → ℝ) :
    eval L (interpolationPoly L p a k t)=
      firstJetInterpolant (sourceC L) p (tripleMultiplier (sourceC L) a k) t := by
  funext z
  simp only [interpolationPoly,eval_mul,eval_tripleMultiplierPoly,eval_append,
    eval_scale,eval_firstGermPoly,firstJetInterpolant]
  simp [Fin.sum_univ_succ,add_assoc]

private theorem raw_pairing {L : ℝ} (hL : L ≠ 0) (r : ℝ) (F : TrigPoly) (i : Fin 6) :
    finitePairing (rawPinCoefficient L r i) (toSource L F) =
      ![firstJet (eval L F) (endpointM r) 0,firstJet (eval L F) (endpointS r) 0,
        firstJet (eval L F) (endpointM r) 1,firstJet (eval L F) (endpointS r) 1,
        firstJet (eval L F) (endpointM r) 2,firstJet (eval L F) (endpointS r) 2] i := by
  change finitePairing (derivativeCoefficient 2 L (rawDerivativeOrder (Fin.castAdd 6 i))
    (rawDerivativePoint r (Fin.castAdd 6 i)) (rawDerivativeDirections (Fin.castAdd 6 i))) (toSource L F)=_
  rw [toSource_derivative hL]
  fin_cases i <;> first | exact iteratedFDeriv_zero_apply _ | exact iteratedFDeriv_one_apply _

private theorem first_pairing {L : ℝ} (hL : L ≠ 0) (p : Fin 2 → ℝ)
    (F : TrigPoly) (j : Fin 3) :
    finitePairing (remoteJetCoefficient L p (Fin.castAdd 3 j)) (toSource L F)=firstJet (eval L F) p j := by
  fin_cases j
  · exact toSource_eval hL F p
  · exact (toSource_derivative hL F 1 p (fun _ => directionX)).trans (iteratedFDeriv_one_apply _)
  · exact (toSource_derivative hL F 1 p (fun _ => directionY)).trans (iteratedFDeriv_one_apply _)

private theorem local_finite_witnesses {L : ℝ} (hL : L ≠ 0) (r : ℝ) (p q : Fin 2 → ℝ)
    (hpM : I4Torus.torusProjection 2 L p ≠ I4Torus.torusProjection 2 L (endpointM r))
    (hpS : I4Torus.torusProjection 2 L p ≠ I4Torus.torusProjection 2 L (endpointS r))
    (hpq : I4Torus.torusProjection 2 L p ≠ I4Torus.torusProjection 2 L q) :
    ∃ v : Fin 3 → (SourceMode 2 →₀ ℝ),
      (∀ i s, finitePairing (rawPinCoefficient L r i) (v s)=0) ∧
      (∀ j s, finitePairing (remoteJetCoefficient L p (Fin.castAdd 3 j)) (v s)=if j=s then 1 else 0) ∧
      (∀ j s, finitePairing (remoteJetCoefficient L q (Fin.castAdd 3 j)) (v s)=0) := by
  obtain ⟨jM,hM⟩ := positive_axis hL p (endpointM r) hpM
  obtain ⟨jS,hS⟩ := positive_axis hL p (endpointS r) hpS
  obtain ⟨jq,hq⟩ := positive_axis hL p q hpq
  let a : Fin 3 → (Fin 2 → ℝ) := ![endpointM r,endpointS r,q]
  let k : Fin 3 → Fin 2 := ![jM,jS,jq]
  let P := tripleMultiplier (sourceC L) a k
  have hP : ContDiff ℝ 2 P := tripleMultiplier_C2 _ a k
  have hPp : 0 < P p := mul_pos (mul_pos (sq_pos_of_pos hM) (sq_pos_of_pos hS)) (sq_pos_of_pos hq)
  have hzero (i : Fin 3) : P (a i)=0 ∧ fderiv ℝ P (a i)=0 := tripleMultiplier_zero _ a k i
  refine ⟨fun s => toSource L (interpolationPoly L p a k (fun j => if j=s then 1 else 0)),?_,?_,?_⟩
  · intro i s
    rw [raw_pairing hL,eval_interpolationPoly]
    have hM0 := firstJetInterpolant_zero (sourceC L) p P hP (endpointM r)
      (hzero 0).1 (hzero 0).2 (fun j => if j=s then 1 else 0)
    have hS0 := firstJetInterpolant_zero (sourceC L) p P hP (endpointS r)
      (hzero 1).1 (hzero 1).2 (fun j => if j=s then 1 else 0)
    change firstJet (firstJetInterpolant (sourceC L) p P _) (endpointM r)=0 at hM0
    change firstJet (firstJetInterpolant (sourceC L) p P _) (endpointS r)=0 at hS0
    rw [hM0,hS0]
    fin_cases i <;> rfl
  · intro j s
    rw [first_pairing hL,eval_interpolationPoly,
      firstJetInterpolant_self (sourceC L) (sourceC_ne_zero hL) p P hP hPp.ne']
  · intro j s
    rw [first_pairing hL,eval_interpolationPoly]
    exact congrFun (firstJetInterpolant_zero (sourceC L) p P hP q
      (hzero 2).1 (hzero 2).2 _) j

private def localColumn (s : Fin 6) : Fin 3 := ⟨s.val % 3,Nat.mod_lt _ (by norm_num)⟩

private theorem rows_summable {L : ℝ} (hL : L ≠ 0) (x y : Fin 2 → ℝ)
    (j : Fin 6) : Summable (twoRemoteFirstJetCoefficient L x y j) := by
  have hval (p : Fin 2 → ℝ) : Summable (fun m => modeCoefficient 2 L m p) := by
    have he : derivativeCoefficient 2 L 0 p (fun i => Fin.elim0 i)=fun m => modeCoefficient 2 L m p := by
      funext m
      exact iteratedFDeriv_zero_apply _
    rw [← he]
    exact derivativeCoefficient_summable 2 hL 0 p (fun i => Fin.elim0 i)
  fin_cases j
  · exact hval x
  · exact derivativeCoefficient_summable 2 hL 1 x (fun _ => directionX)
  · exact derivativeCoefficient_summable 2 hL 1 x (fun _ => directionY)
  · exact hval y
  · exact derivativeCoefficient_summable 2 hL 1 y (fun _ => directionX)
  · exact derivativeCoefficient_summable 2 hL 1 y (fun _ => directionY)

/-- Joint first-jet-six right inverse in actual finite original coefficient directions. -/
theorem actual_finite_twoRemoteFirstJet_witnesses {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x y : Fin 2 → ℝ)
    (hxM : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointM r))
    (hxS : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointS r))
    (hyM : I4Torus.torusProjection 2 L y ≠ I4Torus.torusProjection 2 L (endpointM r))
    (hyS : I4Torus.torusProjection 2 L y ≠ I4Torus.torusProjection 2 L (endpointS r))
    (hxy : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L y) :
    ∃ v : Fin 6 → (SourceMode 2 →₀ ℝ),
      (∀ i s, finitePairing (rawPinCoefficient L r i) (v s)=0) ∧
      (∀ j s, finitePairing (twoRemoteFirstJetCoefficient L x y j) (v s)=if j=s then 1 else 0) := by
  obtain ⟨vx,hxraw,hxx,hxy0⟩ := local_finite_witnesses hL r x y hxM hxS hxy
  obtain ⟨vy,hyraw,hyy,hyx0⟩ := local_finite_witnesses hL r y x hyM hyS hxy.symm
  let v : Fin 6 → (SourceMode 2 →₀ ℝ) := fun s => if s.val<3 then vx (localColumn s) else vy (localColumn s)
  refine ⟨v,?_,?_⟩
  · intro i s
    fin_cases s <;> simp only [v,localColumn] <;> first | exact hxraw i _ | exact hyraw i _
  · intro j s
    fin_cases j <;> fin_cases s <;> simp [v,localColumn,twoRemoteFirstJetCoefficient] <;>
      first | exact hxx _ _ | exact hyy _ _ | exact hxy0 _ _ | exact hyx0 _ _

/-- Actual joint first-jet residual Gram positivity for every6×6 real correction. -/
theorem actual_twoRemoteFirstJet_residual_coefficientGram_posDef {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (x y : Fin 2 → ℝ)
    (hxM : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointM r))
    (hxS : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointS r))
    (hyM : I4Torus.torusProjection 2 L y ≠ I4Torus.torusProjection 2 L (endpointM r))
    (hyS : I4Torus.torusProjection 2 L y ≠ I4Torus.torusProjection 2 L (endpointS r))
    (hxy : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L y)
    (R : Matrix (Fin 6) (Fin 6) ℝ) :
    (I4ContactGram.coefficientGram (I4SourceFinitePinKernel.residualCoefficient
      (rawPinCoefficient L r) (twoRemoteFirstJetCoefficient L x y) R)).PosDef := by
  obtain ⟨v,hker,hright⟩ := actual_finite_twoRemoteFirstJet_witnesses hL r x y hxM hxS hyM hyS hxy
  exact coefficientGram_posDef_of_finite_kernel_rightInverse _ _ R
    (rawPinCoefficient_summable hL r) (rows_summable hL x y) v hker hright

end I4SourceTwoRemoteFirstJetWitness
