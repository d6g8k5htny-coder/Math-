import Mathlib.Analysis.Calculus.ImplicitContDiff
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Calculus.Deriv.Prod
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Topology.Compactness.Compact
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-! A transverse root is constructed on an open collar of the closed parameter interval.
The collar, rather than an arbitrary extension from the closed interval, makes all
regularity conclusions full two-sided conclusions at its endpoints. -/

open Set Filter
open scoped Topology ContDiff

namespace AdaptiveFoldTransverseRidge

def ex : ℝ × ℝ := (1, 0)
def ey : ℝ × ℝ := (0, 1)
noncomputable def partialX (G : ℝ × ℝ → ℝ) (p : ℝ × ℝ) : ℝ := fderiv ℝ G p ex
noncomputable def partialY (G : ℝ × ℝ → ℝ) (p : ℝ × ℝ) : ℝ := fderiv ℝ G p ey
noncomputable def Vx (V : ℝ × ℝ → ℝ) : ℝ × ℝ → ℝ := partialX V
noncomputable def Vy (V : ℝ × ℝ → ℝ) : ℝ × ℝ → ℝ := partialY V

theorem contDiffOn_partialY {G : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)}
    {n m : ℕ∞ω} (hO : IsOpen O) (hG : ContDiffOn ℝ n G O) (hmn : m + 1 ≤ n) :
    ContDiffOn ℝ m (partialY G) O := by
  exact (hG.fderiv_of_isOpen hO hmn).clm_apply contDiffOn_const

theorem hasDerivAt_slice {G : ℝ × ℝ → ℝ} {x y : ℝ}
    (hG : DifferentiableAt ℝ G (x, y)) :
    HasDerivAt (fun t => G (x, t)) (partialY G (x, y)) y := by
  have h := hG.hasFDerivAt.comp_hasDerivAt y
    ((hasDerivAt_const y x).prodMk (hasDerivAt_id y))
  simpa [Function.comp_def, partialY, ey] using h

/-- A compact vertical strip gives an open horizontal collar with a strict
negative derivative margin and the original strict opposite boundary signs. -/
theorem exists_structural_collar
    {G : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)} {l u R c : ℝ}
    (hc : 0 < c) (hO : IsOpen O) (hG : ContDiffOn ℝ 2 G O)
    (hrect : Icc l u ×ˢ Icc (-R) R ⊆ O)
    (hneg : ∀ x ∈ Icc l u, ∀ y ∈ Icc (-R) R, partialY G (x, y) ≤ -c)
    (hlower : ∀ x ∈ Icc l u, 0 < G (x, -R))
    (hupper : ∀ x ∈ Icc l u, G (x, R) < 0) (hR : 0 < R) :
    ∃ U : Set ℝ, IsOpen U ∧ Icc l u ⊆ U ∧
      ∀ x ∈ U, (∀ y ∈ Icc (-R) R, (x, y) ∈ O ∧ partialY G (x, y) < -c / 2) ∧
        0 < G (x, -R) ∧ G (x, R) < 0 := by
  let S : Set ℝ := {x | (∀ y ∈ Icc (-R) R,
    (x, y) ∈ O ∧ partialY G (x, y) < -c / 2) ∧ 0 < G (x, -R) ∧ G (x, R) < 0}
  refine ⟨interior S, isOpen_interior, ?_, fun x hx => (show x ∈ S from interior_subset hx)⟩
  intro x hx
  apply mem_interior_iff_mem_nhds.mpr
  have hGy := contDiffOn_partialY hO hG (m := 1) (by norm_num)
  have hs : ∀ᶠ t in 𝓝 x, ∀ y ∈ Icc (-R) R,
      (t, y) ∈ O ∧ partialY G (t, y) < -c / 2 := by
    apply isCompact_Icc.eventually_forall_of_forall_eventually
    intro y hy
    have hp : (x, y) ∈ O := hrect ⟨hx, hy⟩
    have hg : ContinuousAt (partialY G) (x, y) :=
      (hGy.contDiffAt (hO.mem_nhds hp)).continuousAt
    have hn : partialY G (x, y) < -c / 2 := by linarith [hneg x hx y hy]
    filter_upwards [hO.mem_nhds hp, hg.eventually_lt_const hn] with p hpO hpG
    exact ⟨hpO, hpG⟩
  have hlowO : (x, -R) ∈ O := hrect ⟨hx, by constructor <;> linarith⟩
  have hupO : (x, R) ∈ O := hrect ⟨hx, by constructor <;> linarith⟩
  have hlow : ContinuousAt (fun t => G (t, -R)) x :=
    (hG.contDiffAt (hO.mem_nhds hlowO)).continuousAt.comp (f := fun t : ℝ => (t, -R))
      (show ContinuousAt (fun t : ℝ => (t, -R)) x from
        continuousAt_id.prodMk continuousAt_const)
  have hup : ContinuousAt (fun t => G (t, R)) x :=
    (hG.contDiffAt (hO.mem_nhds hupO)).continuousAt.comp (f := fun t : ℝ => (t, R))
      (show ContinuousAt (fun t : ℝ => (t, R)) x from
        continuousAt_id.prodMk continuousAt_const)
  filter_upwards [hs, hlow.eventually_const_lt (hlower x hx),
    hup.eventually_lt_const (hupper x hx)] with t ht hl hu
  exact ⟨ht, hl, hu⟩

/-- Strict vertical decrease gives a unique interior zero on each collar slice. -/
theorem slice_unique_root
    {G : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)} {x R c : ℝ}
    (hR : 0 < R) (hc : 0 < c) (hO : IsOpen O) (hG : ContDiffOn ℝ 2 G O)
    (hstrip : ∀ y ∈ Icc (-R) R, (x, y) ∈ O ∧ partialY G (x, y) < -c / 2)
    (hlower : 0 < G (x, -R)) (hupper : G (x, R) < 0) :
    ∃ z ∈ Ioo (-R) R, G (x, z) = 0 ∧
      ∀ y ∈ Icc (-R) R, G (x, y) = 0 → y = z := by
  have hcont : ContinuousOn (fun y => G (x, y)) (Icc (-R) R) := by
    intro y hy
    exact ((hG.contDiffAt (hO.mem_nhds (hstrip y hy).1)).continuousAt.comp
      (continuousAt_const.prodMk continuousAt_id)).continuousWithinAt
  have hanti : StrictAntiOn (fun y => G (x, y)) (Icc (-R) R) := by
    apply strictAntiOn_of_deriv_neg (convex_Icc _ _) hcont
    intro y hy
    have hy' : y ∈ Icc (-R) R := interior_subset hy
    rw [(hasDerivAt_slice ((hG.contDiffAt (hO.mem_nhds (hstrip y hy').1)).differentiableAt
      (by norm_num))).deriv]
    linarith [(hstrip y hy').2]
  have hzero : (0 : ℝ) ∈ Icc (G (x, R)) (G (x, -R)) :=
    ⟨le_of_lt hupper, le_of_lt hlower⟩
  obtain ⟨z, hz, hz0⟩ := intermediate_value_Icc' (by linarith : -R ≤ R) hcont hzero
  have hzL : -R < z := by
    rcases hz.1.eq_or_lt with h | h
    · exfalso; have : G (x, -R) = 0 := h.symm ▸ hz0; linarith
    · exact h
  have hzU : z < R := by
    rcases hz.2.eq_or_lt with h | h
    · exfalso; have : G (x, R) = 0 := h ▸ hz0; linarith
    · exact h
  refine ⟨z, ⟨hzL, hzU⟩, hz0, ?_⟩
  intro y hy hy0
  exact hanti.injOn hy hz (hy0.trans hz0.symm)

/-- A scalar vertical derivative has its explicit reciprocal linear inverse. -/
theorem vertical_isInvertible {G : ℝ × ℝ → ℝ} {p : ℝ × ℝ}
    (hq : partialY G p ≠ 0) :
    (fderiv ℝ G p ∘L ContinuousLinearMap.inr ℝ ℝ ℝ).IsInvertible := by
  let A := fderiv ℝ G p ∘L ContinuousLinearMap.inr ℝ ℝ ℝ
  let B : ℝ →L[ℝ] ℝ := (partialY G p)⁻¹ • ContinuousLinearMap.id ℝ ℝ
  have hA (t : ℝ) : A t = t * partialY G p := by
    change fderiv ℝ G p (0, t) = t * _
    have hv : (0, t) = t • ey := by ext <;> simp [ey]
    rw [hv, map_smul]
    rfl
  apply ContinuousLinearMap.IsInvertible.of_inverse (g := B)
  · apply ContinuousLinearMap.ext
    intro t
    change A (B t) = t
    rw [hA]
    simp only [B, smul_apply, ContinuousLinearMap.id_apply, smul_eq_mul]
    field_simp
  · apply ContinuousLinearMap.ext
    intro t
    change B (A t) = t
    rw [hA]
    simp only [B, smul_apply, ContinuousLinearMap.id_apply, smul_eq_mul]
    field_simp

/-- Patching the locally unique chosen zero to the genuine local C² IFT function.
This lemma proves regularity; it assumes no continuity of the chosen zero. -/
theorem contDiffOn_of_unique_zero
    {G : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)} {U : Set ℝ} {z : ℝ → ℝ} {R c : ℝ}
    (hc : 0 < c) (hO : IsOpen O) (hG : ContDiffOn ℝ 2 G O) (hU : IsOpen U)
    (hz : ∀ x ∈ U, z x ∈ Ioo (-R) R ∧ (x, z x) ∈ O ∧ G (x, z x) = 0)
    (hneg : ∀ x ∈ U, partialY G (x, z x) < -c / 2)
    (hunique : ∀ x ∈ U, ∀ y ∈ Icc (-R) R, G (x, y) = 0 → y = z x) :
    ContDiffOn ℝ 2 z U := by
  apply hU.contDiffOn_iff.mpr
  intro x hx
  have hGp : ContDiffAt ℝ 2 G (x, z x) := hG.contDiffAt (hO.mem_nhds (hz x hx).2.1)
  have hq : partialY G (x, z x) ≠ 0 := ne_of_lt (by linarith [hneg x hx])
  have hi := vertical_isInvertible hq
  let ψ := hGp.implicitFunction (by norm_num) hi
  have hψ : ContDiffAt ℝ 2 ψ x := hGp.contDiffAt_implicitFunction (by norm_num) hi
  have hψx : ψ x = z x := hGp.implicitFunction_apply_self (by norm_num) hi
  have hψin : ∀ᶠ t in 𝓝 x, ψ t ∈ Ioo (-R) R :=
    hψ.continuousAt.eventually (isOpen_Ioo.mem_nhds (hψx.symm ▸ (hz x hx).1))
  have heq : ∀ᶠ t in 𝓝 x, G (t, ψ t) = 0 := by
    filter_upwards [hGp.eventually_apply_implicitFunction (by norm_num) hi] with t ht
    exact ht.trans (hz x hx).2.2
  apply hψ.congr_of_eventuallyEq
  filter_upwards [hU.mem_nhds hx, hψin, heq] with t ht htψ ht0
  exact (hunique t ht (ψ t) (Ioo_subset_Icc_self htψ) ht0).symm

/-- Generic structural construction, used below with the literal partial `Vy V`. -/
theorem exists_unique_c2_zero
    {G : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)} {l u R c : ℝ}
    (hR : 0 < R) (hc : 0 < c) (hO : IsOpen O) (hG : ContDiffOn ℝ 2 G O)
    (hrect : Icc l u ×ˢ Icc (-R) R ⊆ O)
    (hneg : ∀ x ∈ Icc l u, ∀ y ∈ Icc (-R) R, partialY G (x, y) ≤ -c)
    (hlower : ∀ x ∈ Icc l u, 0 < G (x, -R))
    (hupper : ∀ x ∈ Icc l u, G (x, R) < 0) :
    ∃ (U : Set ℝ) (z : ℝ → ℝ), IsOpen U ∧ Icc l u ⊆ U ∧ ContDiffOn ℝ 2 z U ∧
      (∀ x ∈ U, z x ∈ Ioo (-R) R ∧ (x, z x) ∈ O ∧ G (x, z x) = 0) ∧
      (∀ x ∈ U, ∀ y ∈ Icc (-R) R, G (x, y) = 0 → y = z x) ∧
      (∀ x ∈ U, partialY G (x, z x) < -c / 2) := by
  classical
  obtain ⟨U, hU, hJU, hstr⟩ := exists_structural_collar hc hO hG hrect hneg hlower hupper hR
  have hex : ∀ x ∈ U, ∃ z ∈ Ioo (-R) R, G (x, z) = 0 ∧
      ∀ y ∈ Icc (-R) R, G (x, y) = 0 → y = z := by
    intro x hx
    exact slice_unique_root hR hc hO hG (hstr x hx).1 (hstr x hx).2.1 (hstr x hx).2.2
  let z : ℝ → ℝ := fun x => if hx : x ∈ U then (hex x hx).choose else 0
  have hchosen (x : ℝ) (hx : x ∈ U) : z x ∈ Ioo (-R) R ∧ G (x, z x) = 0 ∧
      ∀ y ∈ Icc (-R) R, G (x, y) = 0 → y = z x := by
    simpa only [z, dite_eq_left hx] using (hex x hx).choose_spec
  have hz : ∀ x ∈ U, z x ∈ Ioo (-R) R ∧ (x, z x) ∈ O ∧ G (x, z x) = 0 := by
    intro x hx
    exact ⟨(hchosen x hx).1, ((hstr x hx).1 _ (Ioo_subset_Icc_self (hchosen x hx).1)).1,
      (hchosen x hx).2.1⟩
  have hu : ∀ x ∈ U, ∀ y ∈ Icc (-R) R, G (x, y) = 0 → y = z x :=
    fun x hx => (hchosen x hx).2.2
  have hn : ∀ x ∈ U, partialY G (x, z x) < -c / 2 :=
    fun x hx => ((hstr x hx).1 _ (Ioo_subset_Icc_self (hchosen x hx).1)).2
  exact ⟨U, z, hU, hJU, contDiffOn_of_unique_zero hc hO hG hU hz hn hu, hz, hu, hn⟩

/-- Literal C⁴ potential → constructed C² transverse ridge on an open collar.
There is no ridge function or ridge regularity among the premises. -/
theorem exists_unique_c2_transverse_ridge
    {V : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)} {l u R c : ℝ}
    (hR : 0 < R) (hc : 0 < c) (hO : IsOpen O) (hV : ContDiffOn ℝ 4 V O)
    (hrect : Icc l u ×ˢ Icc (-R) R ⊆ O)
    (hneg : ∀ x ∈ Icc l u, ∀ y ∈ Icc (-R) R, partialY (Vy V) (x, y) ≤ -c)
    (hlower : ∀ x ∈ Icc l u, 0 < Vy V (x, -R))
    (hupper : ∀ x ∈ Icc l u, Vy V (x, R) < 0) :
    ∃ (U : Set ℝ) (z : ℝ → ℝ), IsOpen U ∧ Icc l u ⊆ U ∧ ContDiffOn ℝ 2 z U ∧
      (∀ x ∈ U, z x ∈ Ioo (-R) R ∧ (x, z x) ∈ O ∧ Vy V (x, z x) = 0) ∧
      (∀ x ∈ U, ∀ y ∈ Icc (-R) R, Vy V (x, y) = 0 → y = z x) ∧
      (∀ x ∈ U, partialY (Vy V) (x, z x) < -c / 2) := by
  have hG : ContDiffOn ℝ 2 (Vy V) O := contDiffOn_partialY hO hV (by norm_num)
  exact exists_unique_c2_zero hR hc hO hG hrect hneg hlower hupper

/-! The following derivative-chain helpers are integrated from the checked scratch
work of `/root/transverse_ridge_jets`, frozen run-004 (26 October 2026).
They are instantiated with the constructed ridge in the theorem below. -/

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



/-- Potential restricted to the constructed graph. -/
noncomputable def profile (V : ℝ × ℝ → ℝ) (z : ℝ → ℝ) (x : ℝ) : ℝ := V (x, z x)
/-- The profile slope is the literal horizontal partial. -/
noncomputable def profileSlope (V : ℝ × ℝ → ℝ) (z : ℝ → ℝ) (x : ℝ) : ℝ :=
  Vx V (x, z x)
noncomputable def profileSlopeFirst (V : ℝ × ℝ → ℝ) (z : ℝ → ℝ) (x : ℝ) : ℝ :=
  fderiv ℝ (Vx V) (x, z x) (1, deriv z x)
noncomputable def profileSlopeSecond (V : ℝ × ℝ → ℝ) (z : ℝ → ℝ) (x : ℝ) : ℝ :=
  fderiv ℝ (fderiv ℝ (Vx V)) (x, z x) (1, deriv z x) (1, deriv z x) +
    fderiv ℝ (Vx V) (x, z x) (0, deriv (deriv z) x)

/-- Literal profile jets ready for the scalar-barrier interface. All derivatives
are full derivatives on the open collar. -/
theorem profile_derivative_jets
    {V : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)} {U : Set ℝ} {z : ℝ → ℝ}
    (hO : IsOpen O) (hV : ContDiffOn ℝ 4 V O) (hU : IsOpen U)
    (hz : ContDiffOn ℝ 2 z U) (hgraph : ∀ x ∈ U, (x, z x) ∈ O)
    (hzero : ∀ x ∈ U, Vy V (x, z x) = 0) {x : ℝ} (hx : x ∈ U) :
    HasDerivAt (profile V z) (profileSlope V z x) x ∧
    HasDerivAt (profileSlope V z) (profileSlopeFirst V z x) x ∧
    HasDerivAt (profileSlopeFirst V z) (profileSlopeSecond V z x) x := by
  have hVp : ContDiffAt ℝ 4 V (x, z x) := hV.contDiffAt (hO.mem_nhds (hgraph x hx))
  obtain ⟨hz1, hz2⟩ := c2_full_derivative_jets hU hz hx
  have hp : HasDerivAt (fun t => (t, z t)) (1, deriv z x) x :=
    (hasDerivAt_id x).prodMk hz1
  have hH : ContDiffAt ℝ 3 (Vx V) (x, z x) :=
    (hVp.fderiv_right (by norm_num)).clm_apply contDiffAt_const
  have hfirst := (hVp.differentiableAt (by norm_num)).hasFDerivAt.comp_hasDerivAt x hp
  have hfirst' : HasDerivAt (profile V z) (profileSlope V z x) x := by
    have hv : fderiv ℝ V (x, z x) (1, deriv z x) = Vx V (x, z x) := by
      rw [clm_graph_vector]
      change Vx V (x, z x) + deriv z x * Vy V (x, z x) = _
      rw [hzero x hx, mul_zero, add_zero]
    change HasDerivAt (fun t => V (t, z t)) (Vx V (x, z x)) x
    rw [hv] at hfirst
    exact hfirst
  have hsecond := (hH.differentiableAt (by norm_num)).hasFDerivAt.comp_hasDerivAt x hp
  have hDH : ContDiffAt ℝ 2 (fderiv ℝ (Vx V)) (x, z x) := hH.fderiv_right (by norm_num)
  have hL := (hDH.differentiableAt (by norm_num)).hasFDerivAt.comp_hasDerivAt x hp
  have hv : HasDerivAt (fun t => ((1 : ℝ), deriv z t)) (0, deriv (deriv z) x) x :=
    (hasDerivAt_const x (1 : ℝ)).prodMk hz2
  exact ⟨hfirst', hsecond, hL.clm_apply hv⟩

/-! Quantitative helpers integrated once from helper frozen run-007. -/
theorem bilinear_graph_vector
    (B : (ℝ × ℝ) →L[ℝ] (ℝ × ℝ) →L[ℝ] ℝ) (z : ℝ) :
    B (1, z) (1, z) = B ex ex + z * B ex ey + z * B ey ex + z ^ 2 * B ey ey := by
  have hv : (1, z) = ex + z • ey := by ext <;> simp [ex, ey]
  calc
    B (1, z) (1, z) = (B ex + z • B ey) (1, z) := by
      have hB : B (1, z) = B ex + z • B ey := by rw [hv, map_add, map_smul]
      exact congrArg (fun L : (ℝ × ℝ) →L[ℝ] ℝ => L (1, z)) hB
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
      have h₁ := abs_add_le (B ex ex) (z * B ex ey)
      have h₂ := abs_add_le (B ex ex + z * B ex ey) (z * B ey ex)
      have h₃ := abs_add_le (B ex ex + z * B ex ey + z * B ey ex) (z ^ 2 * B ey ey)
      linarith
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
    rw [hroot] at hm
    rw [abs_of_nonneg hpos]
    have := le_abs_self (f 0)
    nlinarith
  · have hm := (convex_Icc (-R) R).image_sub_le_mul_sub_of_deriv_le
      hf hdf hneg z hz 0 hzero hnonpos
    rw [hroot] at hm
    rw [abs_of_nonpos hnonpos]
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
  apply root_abs_le_center_div (f := fun y => G (x, y)) hR hc _ _ _ hz hroot hcenter
  · intro y hy
    exact (hslice y hy).continuousAt.continuousWithinAt
  · intro y hy
    exact (hslice y (interior_subset hy)).differentiableAt.differentiableWithinAt
  · intro y hy
    rw [(hslice y (interior_subset hy)).deriv]
    exact hneg y (interior_subset hy)



/-- The constructed ridge, its actual full derivative formulas, structural bounds,
and literal potential/profile jets. The quantitative premises concern only the
closed rectangle and the potential's coordinate derivatives. -/
theorem exists_unique_c2_transverse_ridge_with_jets
    {V : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)} {l u R c M₀ M₁ M₂ : ℝ}
    (hR : 0 < R) (hc : 0 < c) (hO : IsOpen O) (hV : ContDiffOn ℝ 4 V O)
    (hrect : Icc l u ×ˢ Icc (-R) R ⊆ O)
    (hneg : ∀ x ∈ Icc l u, ∀ y ∈ Icc (-R) R, partialY (Vy V) (x, y) ≤ -c)
    (hlower : ∀ x ∈ Icc l u, 0 < Vy V (x, -R))
    (hupper : ∀ x ∈ Icc l u, Vy V (x, R) < 0)
    (hM₁ : 0 ≤ M₁) (hM₂ : 0 ≤ M₂)
    (hcenter : ∀ x ∈ Icc l u, |Vy V (x, 0)| ≤ M₀)
    (hfirst : ∀ x ∈ Icc l u, ∀ y ∈ Icc (-R) R, |partialX (Vy V) (x, y)| ≤ M₁)
    (hxx : ∀ x ∈ Icc l u, ∀ y ∈ Icc (-R) R,
      |fderiv ℝ (fderiv ℝ (Vy V)) (x, y) ex ex| ≤ M₂)
    (hxy : ∀ x ∈ Icc l u, ∀ y ∈ Icc (-R) R,
      |fderiv ℝ (fderiv ℝ (Vy V)) (x, y) ex ey| ≤ M₂)
    (hyx : ∀ x ∈ Icc l u, ∀ y ∈ Icc (-R) R,
      |fderiv ℝ (fderiv ℝ (Vy V)) (x, y) ey ex| ≤ M₂)
    (hyy : ∀ x ∈ Icc l u, ∀ y ∈ Icc (-R) R,
      |fderiv ℝ (fderiv ℝ (Vy V)) (x, y) ey ey| ≤ M₂) :
    ∃ (U : Set ℝ) (z : ℝ → ℝ), IsOpen U ∧ Icc l u ⊆ U ∧ ContDiffOn ℝ 2 z U ∧
      (∀ x ∈ U, z x ∈ Ioo (-R) R ∧ (x, z x) ∈ O ∧ Vy V (x, z x) = 0) ∧
      (∀ x ∈ U, ∀ y ∈ Icc (-R) R, Vy V (x, y) = 0 → y = z x) ∧
      (∀ x ∈ U, partialY (Vy V) (x, z x) < -c / 2) ∧
      (∀ x ∈ U, HasDerivAt z (deriv z x) x ∧
        HasDerivAt (deriv z) (deriv (deriv z) x) x ∧
        partialY (Vy V) (x, z x) ≠ 0 ∧
        deriv z x = -partialX (Vy V) (x, z x) / partialY (Vy V) (x, z x) ∧
        deriv (deriv z) x =
          -(fderiv ℝ (fderiv ℝ (Vy V)) (x, z x) (1, deriv z x) (1, deriv z x)) /
            partialY (Vy V) (x, z x)) ∧
      (∀ x ∈ Icc l u, |z x| ≤ M₀ / c ∧ |deriv z x| ≤ M₁ / c ∧
        |deriv (deriv z) x| ≤ (M₂ / c) * (1 + |deriv z x|) ^ 2) ∧
      (∀ x ∈ U, HasDerivAt (profile V z) (profileSlope V z x) x ∧
        HasDerivAt (profileSlope V z) (profileSlopeFirst V z x) x ∧
        HasDerivAt (profileSlopeFirst V z) (profileSlopeSecond V z x) x) := by
  obtain ⟨U, z, hU, hJU, hz, hroot, huniq, hn⟩ :=
    exists_unique_c2_transverse_ridge hR hc hO hV hrect hneg hlower hupper
  have hG : ContDiffOn ℝ 2 (Vy V) O := contDiffOn_partialY hO hV (by norm_num)
  have hgraph : ∀ x ∈ U, (x, z x) ∈ O := fun x hx => (hroot x hx).2.1
  have hzero : ∀ x ∈ U, Vy V (x, z x) = 0 := fun x hx => (hroot x hx).2.2
  refine ⟨U, z, hU, hJU, hz, hroot, huniq, hn, ?_, ?_, ?_⟩
  · intro x hx
    obtain ⟨h₁, h₂⟩ := c2_full_derivative_jets hU hz hx
    have hden : partialY (Vy V) (x, z x) ≠ 0 := ne_of_lt (by linarith [hn x hx])
    exact ⟨h₁, h₂, hden, zero_graph_derivative_formulas hO hU hG hz hgraph hzero hx hden⟩
  · intro x hx
    have hxU := hJU hx
    have hy : z x ∈ Icc (-R) R := Ioo_subset_Icc_self (hroot x hxU).1
    have hb₀ := zero_graph_center_bound hO hG hR.le hc
      (fun y hy => hrect ⟨hx, hy⟩) (hneg x hx) hy (hzero x hxU) (hcenter x hx)
    have hb := zero_graph_derivative_bounds hO hU hG hz hgraph hzero hc hM₁ hM₂ hxU
      (hneg x hx _ hy) (hfirst x hx _ hy) (hxx x hx _ hy) (hxy x hx _ hy)
      (hyx x hx _ hy) (hyy x hx _ hy)
    exact ⟨hb₀, hb⟩
  · intro x hx
    exact profile_derivative_jets hO hV hU hz hgraph hzero hx

end AdaptiveFoldTransverseRidge
