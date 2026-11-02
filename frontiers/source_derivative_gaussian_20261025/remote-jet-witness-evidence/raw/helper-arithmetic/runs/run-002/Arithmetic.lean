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
  simp only [ContinuousLinearMap.add_apply, ContinuousLinearMap.smul_apply, smul_eq_mul]
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
    simp only [ContinuousLinearMap.add_apply, ContinuousLinearMap.smul_apply, smul_eq_mul]
    ring
  · rw [fderiv_fun_mul (hPdiff x) (hQdiff x)]
    simp only [ContinuousLinearMap.add_apply, ContinuousLinearMap.smul_apply, smul_eq_mul]
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

end I4SourceRemoteJetWitness
