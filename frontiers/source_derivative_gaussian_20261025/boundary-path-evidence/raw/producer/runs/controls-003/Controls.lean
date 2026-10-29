import AdaptiveFoldBoundaryPath
import Mathlib.Analysis.Calculus.FDeriv.Pow

noncomputable section
open Set
open scoped Topology ContDiff
namespace AdaptiveFoldBoundaryPathControls
open AdaptiveFoldTransverseRidge AdaptiveFoldBoundaryPath
open AdaptiveFoldScalar (J)

def polynomial (b : ℝ) (p : ℝ × ℝ) : ℝ := p.1^3/3 - p.1/4 - b*p.2^2

theorem polynomial_c4 (b : ℝ) : ContDiff ℝ 4 (polynomial b) := by unfold polynomial; fun_prop

theorem polynomial_gradient (b : ℝ) (p : ℝ × ℝ) :
    Vx (polynomial b) p = p.1^2-1/4 ∧ Vy (polynomial b) p = -2*b*p.2 := by
  have hx : HasFDerivAt (fun q : ℝ × ℝ => q.1) (ContinuousLinearMap.fst ℝ ℝ ℝ) p := hasFDerivAt_fst
  have hy : HasFDerivAt (fun q : ℝ × ℝ => q.2) (ContinuousLinearMap.snd ℝ ℝ ℝ) p := hasFDerivAt_snd
  have hd := (((hx.pow 3).mul_const (3:ℝ)⁻¹).sub (hx.mul_const (4:ℝ)⁻¹)).sub ((hy.pow 2).const_mul b)
  change HasFDerivAt (polynomial b) _ p at hd
  constructor
  · unfold Vx partialX
    rw [hd.fderiv]
    simp [ex]
  · unfold Vy partialY
    rw [hd.fderiv]
    simp [ey]
    ring

theorem polynomial_Gderiv (b : ℝ) (p : ℝ × ℝ) :
    fderiv ℝ (Vy (polynomial b)) p = (-2*b) • ContinuousLinearMap.snd ℝ ℝ ℝ := by
  have hf : Vy (polynomial b) = fun q : ℝ × ℝ => -2*b*q.2 := funext fun p => (polynomial_gradient b p).2
  rw [hf]
  exact ((hasFDerivAt_snd (𝕜 := ℝ) (p := p)).const_mul (-2*b)).fderiv

theorem polynomial_Gsecond (b : ℝ) (p : ℝ × ℝ) :
    fderiv ℝ (fderiv ℝ (Vy (polynomial b))) p = 0 := by
  have hf : fderiv ℝ (Vy (polynomial b)) = fun _ =>
      (-2*b) • ContinuousLinearMap.snd ℝ ℝ ℝ := funext (polynomial_Gderiv b)
  rw [hf]
  simp

theorem polynomial_Hderiv (b : ℝ) (p : ℝ × ℝ) :
    fderiv ℝ (Vx (polynomial b)) p = (2*p.1) • ContinuousLinearMap.fst ℝ ℝ ℝ := by
  have hf : Vx (polynomial b) = fun q : ℝ × ℝ => q.1^2-1/4 := funext fun p => (polynomial_gradient b p).1
  rw [hf]
  have hd := ((hasFDerivAt_fst (𝕜 := ℝ) (p := p)).pow 2).sub_const (1/4:ℝ)
  rw [hd.fderiv]
  congr 1
  ring

theorem polynomial_Hsecond (b : ℝ) (p a e : ℝ × ℝ) :
    fderiv ℝ (fderiv ℝ (Vx (polynomial b))) p a e = 2*a.1*e.1 := by
  have hf : fderiv ℝ (Vx (polynomial b)) = fun q =>
      (2*q.1) • ContinuousLinearMap.fst ℝ ℝ ℝ := funext (polynomial_Hderiv b)
  rw [hf]
  have hd := ((hasFDerivAt_fst (𝕜 := ℝ) (p := p)).const_mul 2).smul_const
    (ContinuousLinearMap.fst ℝ ℝ ℝ)
  rw [hd.fderiv]
  simp

theorem polynomial_structure {b : ℝ} (hb : 0 < b) :
    StructuralRectangleData (polynomial b) univ 1 (2*b) 0 0 0 2 := by
  constructor
  · norm_num
  · positivity
  · norm_num
  · norm_num
  · norm_num
  · exact isOpen_univ
  · exact (polynomial_c4 b).contDiffOn
  · exact subset_univ _
  · intro x hx y hy
    simp [partialY, polynomial_Gderiv, ey]
  · intro x hx
    rw [(polynomial_gradient b _).2]
    dsimp
    linarith
  · intro x hx
    rw [(polynomial_gradient b _).2]
    dsimp
    linarith
  · intro x hx
    rw [(polynomial_gradient b _).2]
    simp
  · intro x hx y hy
    simp [partialX, polynomial_Gderiv, ex]
  · intro x hx y hy
    rw [polynomial_Gsecond]
    simp
  · intro x hx y hy
    rw [polynomial_Gsecond]
    simp
  · intro x hx y hy
    rw [polynomial_Gsecond]
    simp
  · intro x hx y hy
    rw [polynomial_Gsecond]
    simp
  · intro x hx y hy
    simp [partialY, polynomial_Hderiv, ey]
  · intro x hx y hy
    norm_num [polynomial_Hsecond, ex]
  · intro x hx y hy
    norm_num [polynomial_Hsecond, ex, ey]
  · intro x hx y hy
    norm_num [polynomial_Hsecond, ex, ey]
  · intro x hx y hy
    norm_num [polynomial_Hsecond, ey]
  · norm_num [profileError, accelerationRadius]
  · norm_num [polynomial_gradient]
  · norm_num [polynomial_gradient]
  · norm_num [polynomial]

/-- The low-drop potential meets every structural input, including exact pins. -/
theorem lowdrop_structure :
    StructuralRectangleData (polynomial (1/100)) univ 1 (1/50) 0 0 0 2 := by
  convert polynomial_structure (by norm_num : (0:ℝ)<1/100) using 1; norm_num

/-- Its literal frontier value exceeds the literal saddle level. -/
theorem lowdrop_counterexample :
    (-(1/2:ℝ),1) ∈ frontier (leftBox 1) ∧
    polynomial (1/100) S < polynomial (1/100) (-(1/2:ℝ),1) ∧
    polynomial (1/100) (-(1/2:ℝ),1) = 11/150 ∧
    polynomial (1/100) S = -1/12 := by
  constructor
  · rw [leftBox, frontier_prod_eq, closure_Icc, closure_Icc,
      frontier_Icc (by norm_num : -(1:ℝ) ≤ 1),
      frontier_Icc (by norm_num : -(3/2:ℝ) ≤ 1/2)]
    simp only [mem_union, mem_prod, mem_Icc, mem_insert_iff, mem_singleton_iff]
    norm_num
  · norm_num [polynomial, S]

/-- The full boundary/path theorem is instantiated with the frozen positive
polynomial and its actual derivative data, rather than a supplied zero ridge. -/
theorem positive_constructed_boundary_path :
    ∃ (U : Set ℝ) (z : ℝ → ℝ) (γ : Path M (olderPoint z)),
      RidgeScalarData (polynomial 4) univ 1 8 0 0 0 U z ∧
      RectangleBoundaryPathData (polynomial 4) 1 8 z ∧
      (∀ x ∈ U, z x = 0) ∧ olderPoint z = (3/2,0) ∧
      (∀ p ∈ frontier (leftBox 1), polynomial 4 p ≤ polynomial 4 S) ∧
      (∀ t : unitInterval, γ t = (pathX t,0)) ∧
      (∀ t : unitInterval, polynomial 4 S ≤ polynomial 4 (γ t)) ∧
      γ pathMidpoint = S := by
  have hs : StructuralRectangleData (polynomial 4) univ 1 8 0 0 0 2 := by
    convert polynomial_structure (by norm_num : (0:ℝ)<4) using 1
  obtain ⟨U,z,hz,hg⟩ := exists_transverse_ridge_boundary_path hs (by norm_num) (by norm_num)
  have heq : ∀ x ∈ U, z x = 0 := by
    intro x hx
    have hr := (hz.root x hx).2.2
    rw [(polynomial_gradient 4 _).2] at hr
    dsimp at hr
    linarith
  obtain ⟨γ,hγ,hfloor,hmid⟩ := hg.path
  refine ⟨U,z,γ,hz,hg,heq,?_,hg.frontier_bound,?_,hfloor,hmid⟩
  · simp only [olderPoint, heq _ (hz.interval_subset (by norm_num [J]))]
  · intro t
    rw [hγ]
    have hx : pathX t ∈ U := hz.interval_subset
      ⟨by linarith [(pathX_mem t).1], (pathX_mem t).2⟩
    rw [heq _ hx]

/-- The two literal gradient pins and the normalization are numerical identities. -/
theorem positive_pins_gap :
    Vx (polynomial 4) M = 0 ∧ Vy (polynomial 4) M = 0 ∧
    Vx (polynomial 4) S = 0 ∧ Vy (polynomial 4) S = 0 ∧
    polynomial 4 M - polynomial 4 S = 1/6 := by
  norm_num [polynomial_gradient, polynomial, M, S]

theorem lowdrop_analytic_constructed :
    ∃ (U : Set ℝ) (z : ℝ → ℝ),
      RidgeScalarData (polynomial (1/100)) univ 1 (1/50) 0 0 0 U z ∧
      (∀ x ∈ U, z x = 0) := by
  obtain ⟨U,z,hz⟩ := exists_transverse_ridge_scalar_barrier lowdrop_structure
  refine ⟨U,z,hz,?_⟩
  intro x hx
  have hr := (hz.root x hx).2.2
  rw [(polynomial_gradient (1/100) _).2] at hr
  dsimp at hr
  linarith

theorem lowdrop_margin_and_failed_budget :
    (0:ℝ)/(1/50) ≤ 1 ∧ (1/50/2:ℝ)*(1-0/(1/50))^2 < 1 := by norm_num

end AdaptiveFoldBoundaryPathControls
