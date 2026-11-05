import SourceFiniteTrig
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Tactic.FunProp

noncomputable section
open scoped BigOperators
set_option autoImplicit false

namespace I4SourceRemoteJetWitness
open I4SourceConfluentPins

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
  fin_cases j <;> simp [hc] <;> field_simp <;> ring

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
    _ = a j := by simp [eq_comm]

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

end I4SourceRemoteJetWitness
