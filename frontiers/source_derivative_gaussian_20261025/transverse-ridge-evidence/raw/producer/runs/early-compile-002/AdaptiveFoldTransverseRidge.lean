import Mathlib.Analysis.Calculus.ImplicitContDiff
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
    (hG.contDiffAt (hO.mem_nhds hlowO)).continuousAt.comp
      (show ContinuousAt (fun t : ℝ => (t, -R)) x from
        continuousAt_id.prodMk continuousAt_const)
  have hup : ContinuousAt (fun t => G (t, R)) x :=
    (hG.contDiffAt (hO.mem_nhds hupO)).continuousAt.comp
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
    simp [B, mul_assoc, hq]
  · apply ContinuousLinearMap.ext
    intro t
    change B (A t) = t
    rw [hA]
    simp [B, mul_assoc, hq]

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

end AdaptiveFoldTransverseRidge
