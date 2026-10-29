import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Calculus.Deriv.Prod
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

open Set Filter
open scoped Topology

namespace AdaptiveFoldTransverseRidge

def ex : ℝ × ℝ := (1, 0)
def ey : ℝ × ℝ := (0, 1)
noncomputable def partialX (G : ℝ × ℝ → ℝ) (p : ℝ × ℝ) : ℝ := fderiv ℝ G p ex
noncomputable def partialY (G : ℝ × ℝ → ℝ) (p : ℝ × ℝ) : ℝ := fderiv ℝ G p ey

/-- Literal coordinate expansion; uses no choice of product norm. -/
theorem clm_graph_vector (L : (ℝ × ℝ) →L[ℝ] ℝ) (z : ℝ) :
    L (1, z) = L ex + z * L ey := by
  have hv : (1, z) = ex + z • ey := by ext <;> simp [ex, ey]
  rw [hv, map_add, map_smul]
  rfl

theorem clm_vertical_vector (L : (ℝ × ℝ) →L[ℝ] ℝ) (z : ℝ) :
    L (0, z) = z * L ey := by
  have hv : (0, z) = z • ey := by ext <;> simp [ey]
  rw [hv, map_smul]
  rfl

/-- Full derivatives follow from C² regularity on an open neighborhood. -/
theorem c2_full_derivative_jets {ζ : ℝ → ℝ} {U : Set ℝ}
    (hU : IsOpen U) (hζ : ContDiffOn ℝ 2 ζ U) {x : ℝ} (hx : x ∈ U) :
    HasDerivAt ζ (deriv ζ x) x ∧
      HasDerivAt (deriv ζ) (deriv (deriv ζ) x) x := by
  have hζx : ContDiffAt ℝ 2 ζ x := (hU.contDiffOn_iff.mp hζ) hx
  have hζ₁ : ContDiffOn ℝ 1 (deriv ζ) U := hζ.deriv_of_isOpen hU (by norm_num)
  have hζ₁x : ContDiffAt ℝ 1 (deriv ζ) x := (hU.contDiffOn_iff.mp hζ₁) hx
  exact ⟨(hζx.differentiableAt (by norm_num)).hasDerivAt,
    (hζ₁x.differentiableAt (by norm_num)).hasDerivAt⟩

/-- The first derivative of the identically zero graph equation. -/
theorem zero_graph_first_chain {G : ℝ × ℝ → ℝ} {ζ : ℝ → ℝ}
    {O : Set (ℝ × ℝ)} {U : Set ℝ}
    (hO : IsOpen O) (hU : IsOpen U)
    (hG : ContDiffOn ℝ 2 G O) (hζ : ContDiffOn ℝ 2 ζ U)
    (hgraph : ∀ x ∈ U, (x, ζ x) ∈ O) (hzero : ∀ x ∈ U, G (x, ζ x) = 0)
    {x : ℝ} (hx : x ∈ U) :
    fderiv ℝ G (x, ζ x) (1, deriv ζ x) = 0 := by
  have hGx : ContDiffAt ℝ 2 G (x, ζ x) := (hO.contDiffOn_iff.mp hG) (hgraph x hx)
  have hζx := (c2_full_derivative_jets hU hζ hx).1
  have hp : HasDerivAt (fun t => (t, ζ t)) (1, deriv ζ x) x :=
    (hasDerivAt_id x).prodMk hζx
  have hchain := (hGx.differentiableAt (by norm_num)).hasFDerivAt.comp_hasDerivAt x hp
  have heq : (fun t => G (t, ζ t)) =ᶠ[𝓝 x] (fun _ => (0 : ℝ)) :=
    (hU.mem_nhds hx).mono fun t ht => hzero t ht
  have hz : HasDerivAt (fun t => G (t, ζ t)) 0 x :=
    (hasDerivAt_const x (0 : ℝ)).congr_of_eventuallyEq heq
  exact hchain.unique hz

/-- The second derivative of the same graph equation uses the actual second Frechet derivative. -/
theorem zero_graph_second_chain {G : ℝ × ℝ → ℝ} {ζ : ℝ → ℝ}
    {O : Set (ℝ × ℝ)} {U : Set ℝ}
    (hO : IsOpen O) (hU : IsOpen U)
    (hG : ContDiffOn ℝ 2 G O) (hζ : ContDiffOn ℝ 2 ζ U)
    (hgraph : ∀ x ∈ U, (x, ζ x) ∈ O) (hzero : ∀ x ∈ U, G (x, ζ x) = 0)
    {x : ℝ} (hx : x ∈ U) :
    fderiv ℝ (fderiv ℝ G) (x, ζ x) (1, deriv ζ x) (1, deriv ζ x) +
      fderiv ℝ G (x, ζ x) (0, deriv (deriv ζ) x) = 0 := by
  have hGx : ContDiffAt ℝ 2 G (x, ζ x) := (hO.contDiffOn_iff.mp hG) (hgraph x hx)
  obtain ⟨hζx, hζ₁x⟩ := c2_full_derivative_jets hU hζ hx
  have hp : HasDerivAt (fun t => (t, ζ t)) (1, deriv ζ x) x :=
    (hasDerivAt_id x).prodMk hζx
  have hDG : ContDiffAt ℝ 1 (fderiv ℝ G) (x, ζ x) :=
    hGx.fderiv_right (by norm_num)
  have hL := (hDG.differentiableAt (by norm_num)).hasFDerivAt.comp_hasDerivAt x hp
  have hv : HasDerivAt (fun t => ((1 : ℝ), deriv ζ t))
      (0, deriv (deriv ζ) x) x := (hasDerivAt_const x (1 : ℝ)).prodMk hζ₁x
  have hchain := hL.clm_apply hv
  have heq : (fun t => fderiv ℝ G (t, ζ t) (1, deriv ζ t)) =ᶠ[𝓝 x]
      (fun _ => (0 : ℝ)) := (hU.mem_nhds hx).mono fun t ht =>
    zero_graph_first_chain hO hU hG hζ hgraph hzero ht
  have hz : HasDerivAt (fun t => fderiv ℝ G (t, ζ t) (1, deriv ζ t)) 0 x :=
    (hasDerivAt_const x (0 : ℝ)).congr_of_eventuallyEq heq
  exact hchain.unique hz

/-- Quotient identities for the actual full first and second derivatives. -/
theorem zero_graph_derivative_formulas {G : ℝ × ℝ → ℝ} {ζ : ℝ → ℝ}
    {O : Set (ℝ × ℝ)} {U : Set ℝ}
    (hO : IsOpen O) (hU : IsOpen U)
    (hG : ContDiffOn ℝ 2 G O) (hζ : ContDiffOn ℝ 2 ζ U)
    (hgraph : ∀ x ∈ U, (x, ζ x) ∈ O) (hzero : ∀ x ∈ U, G (x, ζ x) = 0)
    {x : ℝ} (hx : x ∈ U) (hy : partialY G (x, ζ x) ≠ 0) :
    deriv ζ x = -partialX G (x, ζ x) / partialY G (x, ζ x) ∧
    deriv (deriv ζ) x =
      -(fderiv ℝ (fderiv ℝ G) (x, ζ x) (1, deriv ζ x) (1, deriv ζ x)) /
        partialY G (x, ζ x) := by
  have hfirst := zero_graph_first_chain hO hU hG hζ hgraph hzero hx
  have hsecond := zero_graph_second_chain hO hU hG hζ hgraph hzero hx
  rw [clm_graph_vector] at hfirst
  rw [clm_vertical_vector] at hsecond
  change partialX G (x, ζ x) + deriv ζ x * partialY G (x, ζ x) = 0 at hfirst
  change _ + deriv (deriv ζ) x * partialY G (x, ζ x) = 0 at hsecond
  constructor <;> apply (eq_div_iff hy).2 <;> linarith

end AdaptiveFoldTransverseRidge
