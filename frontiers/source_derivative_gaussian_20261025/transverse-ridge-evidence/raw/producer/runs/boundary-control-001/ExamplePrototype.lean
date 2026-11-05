import Mathlib.Analysis.Calculus.ImplicitContDiff
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Calculus.Deriv.Prod
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
open Set
open scoped Topology ContDiff
namespace Test
noncomputable def V (p : ℝ×ℝ) := p.1*p.2 - p.2*p.2*(1/2)
noncomputable def Vy (p : ℝ×ℝ) := fderiv ℝ V p (0,1)
example : ContDiff ℝ 4 V := by unfold V; fun_prop
 theorem vderiv (p : ℝ×ℝ) : Vy p = p.1-p.2 := by
  have hx : HasFDerivAt (fun q : ℝ×ℝ => q.1) (ContinuousLinearMap.fst ℝ ℝ ℝ) p := hasFDerivAt_fst
  have hy : HasFDerivAt (fun q : ℝ×ℝ => q.2) (ContinuousLinearMap.snd ℝ ℝ ℝ) p := hasFDerivAt_snd
  have h := (hx.mul hy).sub ((hy.mul hy).mul_const (1/2 : ℝ))
  change HasFDerivAt V _ p at h
  unfold Vy
  rw [h.fderiv]
  simp
  <;> ring
example (p : ℝ×ℝ) : fderiv ℝ Vy p (0,1) = -1 := by
  have hfun : Vy = fun q : ℝ×ℝ => q.1-q.2 := funext vderiv
  rw [hfun, ((hasFDerivAt_fst (𝕜:=ℝ) (p:=p)).sub (hasFDerivAt_snd (𝕜:=ℝ) (p:=p))).fderiv]
  simp
end Test
