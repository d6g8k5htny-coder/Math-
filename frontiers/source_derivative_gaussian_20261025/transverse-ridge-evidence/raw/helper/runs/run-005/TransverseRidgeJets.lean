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
    Filter.Eventually.mono (hU.mem_nhds hx) fun t ht => hzero t ht
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
      (fun _ => (0 : ℝ)) := Filter.Eventually.mono (hU.mem_nhds hx) fun t ht =>
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

/-- Explicit four-coordinate expansion of a bilinear form. -/
theorem bilinear_graph_vector
    (B : (ℝ × ℝ) →L[ℝ] (ℝ × ℝ) →L[ℝ] ℝ) (z : ℝ) :
    B (1, z) (1, z) = B ex ex + z * B ex ey + z * B ey ex + z ^ 2 * B ey ey := by
  have hv : (1, z) = ex + z • ey := by ext <;> simp [ex, ey]
  calc
    B (1, z) (1, z) = (B ex + z • B ey) (1, z) := by rw [hv, map_add, map_smul]
    _ = B ex (1, z) + z * B ey (1, z) := rfl
    _ = _ := by rw [clm_graph_vector, clm_graph_vector]; ring

/-- Four coordinate bounds control the graph tangent without a product norm conversion. -/
theorem abs_bilinear_graph_vector_le
    (B : (ℝ × ℝ) →L[ℝ] (ℝ × ℝ) →L[ℝ] ℝ) {M : ℝ}
    (hxx : |B ex ex| ≤ M) (hxy : |B ex ey| ≤ M)
    (hyx : |B ey ex| ≤ M) (hyy : |B ey ey| ≤ M) (z : ℝ) :
    |B (1, z) (1, z)| ≤ M * (1 + |z|) ^ 2 := by
  rw [bilinear_graph_vector]
  calc
    |B ex ex + z * B ex ey + z * B ey ex + z ^ 2 * B ey ey| ≤
        |B ex ex| + |z * B ex ey| + |z * B ey ex| + |z ^ 2 * B ey ey| := by
      exact (abs_add _ _).trans (add_le_add_right
        ((abs_add _ _).trans (add_le_add_right (abs_add _ _) _)) _)
    _ = |B ex ex| + |z| * |B ex ey| + |z| * |B ey ex| + |z| ^ 2 * |B ey ey| := by
      rw [abs_mul, abs_mul, abs_mul, abs_pow]
    _ ≤ M + |z| * M + |z| * M + |z| ^ 2 * M := by
      gcongr
    _ = M * (1 + |z|) ^ 2 := by ring

/-- Scalar denominator estimate, with its sign retained explicitly. -/
theorem abs_neg_div_le_of_le_neg {a b c M : ℝ} (hc : 0 < c) (hM : 0 ≤ M)
    (hb : b ≤ -c) (ha : |a| ≤ M) : |(-a) / b| ≤ M / c := by
  have hbneg : b < 0 := lt_of_le_of_lt hb (neg_neg_of_pos hc)
  have hab : c ≤ |b| := by rw [abs_of_neg hbneg]; linarith
  rw [abs_div, abs_neg]
  apply (div_le_iff₀ (lt_of_lt_of_le hc hab)).2
  calc
    |a| ≤ M := ha
    _ = (M / c) * c := by field_simp
    _ ≤ (M / c) * |b| := mul_le_mul_of_nonneg_left hab (div_nonneg hM hc.le)

/-- Consequences of the literal derivative formulas and coordinate bounds. -/
theorem zero_graph_derivative_bounds {G : ℝ × ℝ → ℝ} {ζ : ℝ → ℝ}
    {O : Set (ℝ × ℝ)} {U : Set ℝ} {c M₁ M₂ : ℝ}
    (hO : IsOpen O) (hU : IsOpen U)
    (hG : ContDiffOn ℝ 2 G O) (hζ : ContDiffOn ℝ 2 ζ U)
    (hgraph : ∀ x ∈ U, (x, ζ x) ∈ O) (hzero : ∀ x ∈ U, G (x, ζ x) = 0)
    (hc : 0 < c) (hM₁ : 0 ≤ M₁) (hM₂ : 0 ≤ M₂)
    {x : ℝ} (hx : x ∈ U) (hy : partialY G (x, ζ x) ≤ -c)
    (hfirst : |partialX G (x, ζ x)| ≤ M₁)
    (hxx : |fderiv ℝ (fderiv ℝ G) (x, ζ x) ex ex| ≤ M₂)
    (hxy : |fderiv ℝ (fderiv ℝ G) (x, ζ x) ex ey| ≤ M₂)
    (hyx : |fderiv ℝ (fderiv ℝ G) (x, ζ x) ey ex| ≤ M₂)
    (hyy : |fderiv ℝ (fderiv ℝ G) (x, ζ x) ey ey| ≤ M₂) :
    |deriv ζ x| ≤ M₁ / c ∧
      |deriv (deriv ζ) x| ≤ (M₂ / c) * (1 + |deriv ζ x|) ^ 2 := by
  have hyne : partialY G (x, ζ x) ≠ 0 := ne_of_lt (lt_of_le_of_lt hy (neg_neg_of_pos hc))
  obtain ⟨h₁, h₂⟩ := zero_graph_derivative_formulas hO hU hG hζ hgraph hzero hx hyne
  constructor
  · rw [h₁]
    exact abs_neg_div_le_of_le_neg hc hM₁ hy hfirst
  · rw [h₂]
    have hcoord := abs_bilinear_graph_vector_le
      (fderiv ℝ (fderiv ℝ G) (x, ζ x)) hxx hxy hyx hyy (deriv ζ x)
    have hbound := abs_neg_div_le_of_le_neg hc
      (mul_nonneg hM₂ (sq_nonneg (1 + |deriv ζ x|))) hy hcoord
    exact hbound.trans_eq (by ring)

/-- A center-to-root bound from a strictly negative derivative on a closed scalar interval. -/
theorem root_abs_le_center_div {f : ℝ → ℝ} {R c M z : ℝ}
    (hR : 0 ≤ R) (hc : 0 < c)
    (hf : ContinuousOn f (Icc (-R) R))
    (hdf : DifferentiableOn ℝ f (interior (Icc (-R) R)))
    (hneg : ∀ y ∈ interior (Icc (-R) R), deriv f y ≤ -c)
    (hz : z ∈ Icc (-R) R) (hroot : f z = 0) (hcenter : |f 0| ≤ M) :
    |z| ≤ M / c := by
  have hzero : (0 : ℝ) ∈ Icc (-R) R := ⟨by linarith, hR⟩
  apply (le_div_iff₀ hc).2
  rcases le_total 0 z with hpos | hnonpos
  · have hm := (convex_Icc (-R) R).image_sub_le_mul_sub_of_deriv_le
      hf hdf hneg 0 hzero z hz hpos
    rw [hroot, abs_of_nonneg hpos]
    have := le_abs_self (f 0)
    nlinarith
  · have hm := (convex_Icc (-R) R).image_sub_le_mul_sub_of_deriv_le
      hf hdf hneg z hz 0 hzero hnonpos
    rw [hroot, abs_of_nonpos hnonpos]
    have := neg_le_abs (f 0)
    nlinarith

/-- Actual vertical partials supply the scalar mean-value hypotheses. -/
theorem zero_graph_center_bound {G : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)}
    {R c M x z : ℝ} (hO : IsOpen O) (hG : ContDiffOn ℝ 2 G O)
    (hR : 0 ≤ R) (hc : 0 < c)
    (hstrip : ∀ y ∈ Icc (-R) R, (x, y) ∈ O)
    (hneg : ∀ y ∈ Icc (-R) R, partialY G (x, y) ≤ -c)
    (hz : z ∈ Icc (-R) R) (hroot : G (x, z) = 0) (hcenter : |G (x, 0)| ≤ M) :
    |z| ≤ M / c := by
  have hslice : ∀ y ∈ Icc (-R) R,
      HasDerivAt (fun t => G (x, t)) (partialY G (x, y)) y := by
    intro y hy
    have hGy : ContDiffAt ℝ 2 G (x, y) := (hO.contDiffOn_iff.mp hG) (hstrip y hy)
    have hp : HasDerivAt (fun t => (x, t)) (0, 1) y :=
      (hasDerivAt_const y x).prodMk (hasDerivAt_id y)
    exact (hGy.differentiableAt (by norm_num)).hasFDerivAt.comp_hasDerivAt y hp
  apply root_abs_le_center_div hR hc _ _ _ hz hroot hcenter
  · intro y hy
    exact (hslice y hy).continuousAt.continuousWithinAt
  · intro y hy
    exact (hslice y (interior_subset hy)).differentiableAt.differentiableWithinAt
  · intro y hy
    rw [(hslice y (interior_subset hy)).deriv]
    exact hneg y (interior_subset hy)

end AdaptiveFoldTransverseRidge
