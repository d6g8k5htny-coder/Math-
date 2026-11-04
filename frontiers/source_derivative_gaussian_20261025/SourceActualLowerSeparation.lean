import SourceActualFiniteSuperlevelComponents
import SourceActualTorusSuperlevelLocalBasis
import SourceActualFoldTorus
import Mathlib.Topology.Separation.Regular
import Mathlib.Topology.Order.Compact
import Mathlib.Topology.Connected.Basic
import Mathlib.Topology.Connected.PathConnected
import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FunProp

noncomputable section

open Set Filter Topology
open UniversalLaw.Spec.Lifetime
open I4LifetimeField I4SmoothCarrier
open scoped BigOperators Topology

namespace I4SourceActualLowerSeparation

private theorem actualSource_closedSuperlevel_ambient_separation
    {L : ℝ} (hL : 0 < L) (omega : I4SmoothCarrier.SmoothSample 2 L)
    (hm : UniversalLaw.Spec.Lifetime.IsMorseDistinct 2 L
      (I4LifetimeField.actualField 2 L omega)) (c : ℝ) :
    ∃ U : ZerothHomotopy (TorusFiltration.superlevel_set
        (SourceActualFoldTorus.actualTorusField hL.ne' omega) (-c)) →
        Set (I4Torus.SourceTorus 2 L),
      (∀ i, IsOpen (U i)) ∧
      (Pairwise fun i j => Disjoint (U i) (U j)) ∧
      (∀ x : TorusFiltration.superlevel_set
          (SourceActualFoldTorus.actualTorusField hL.ne' omega) (-c),
        x.val ∈ U (ZerothHomotopy.mk x)) ∧
      (∀ (i : ZerothHomotopy (TorusFiltration.superlevel_set
          (SourceActualFoldTorus.actualTorusField hL.ne' omega) (-c)))
          (x : TorusFiltration.superlevel_set
            (SourceActualFoldTorus.actualTorusField hL.ne' omega) (-c)),
        x.val ∈ U i ↔ ZerothHomotopy.mk x = i) := by
  classical
  let F : I4Torus.SourceTorus 2 L → ℝ :=
    SourceActualFoldTorus.actualTorusField hL.ne' omega
  let H : Set (I4Torus.SourceTorus 2 L) :=
    TorusFiltration.superlevel_set F (-c)
  let I := ZerothHomotopy H
  let : Fact (0 < L) := ⟨hL⟩
  let : Fact (L ≠ 0) := ⟨hL.ne'⟩
  let : CompactSpace (I4Torus.SourceTorus 2 L) := by
    change CompactSpace (Fin 2 → AddCircle L)
    infer_instance
  let : T2Space (I4Torus.SourceTorus 2 L) := by
    change T2Space (Fin 2 → AddCircle L)
    infer_instance
  let : NormalSpace (I4Torus.SourceTorus 2 L) := inferInstance
  have hF : Continuous F :=
    SourceActualFoldTorus.actualTorusField_continuous hL.ne' omega
  have hHclosed : IsClosed H :=
    TorusFiltration.superlevel_isClosed F hF (-c)
  have hHcompact : IsCompact H := hHclosed.isCompact
  let : CompactSpace H := isCompact_iff_compactSpace.mp hHcompact
  let : Finite I :=
    I4SourceActualFiniteSuperlevelComponents.actualSource_finite_closedSuperlevel_components
      hL omega hm c

  -- These are precisely the canonical quotient fibers, without any imported
  -- local-path-connected subtype instance or supplied partition certificate.
  let P : I → Set H := fun i => {x | ZerothHomotopy.mk x = i}
  have hPopen : ∀ i : I, IsOpen (P i) := by
    intro i
    rw [isOpen_iff_forall_mem_open]
    intro x hx
    have hxi : ZerothHomotopy.mk x = i := hx
    have hxheight : c ≤ F x.val := by
      simpa only [H, TorusFiltration.superlevel_set, neg_neg, Set.mem_ofPred_eq]
        using x.property
    obtain ⟨V, hV, hxV, _, hVPC⟩ :=
      I4SourceActualTorusSuperlevelLocalBasis.actualSource_torus_closedSuperlevel_localPathConnectedBasis
          hL omega hm c x.val hxheight Set.univ isOpen_univ (Set.mem_univ _)
    refine ⟨Subtype.val ⁻¹' V, ?_, hV.preimage continuous_subtype_val, hxV⟩
    intro y hy
    have hyheight : c ≤ F y.val := by
      simpa only [H, TorusFiltration.superlevel_set, neg_neg, Set.mem_ofPred_eq]
        using y.property
    have hxy : JoinedIn H x.val y.val :=
      (hVPC.joinedIn x.val ⟨hxV, hxheight⟩ y.val ⟨hy, hyheight⟩).mono (by
        intro z hz
        change -(-c) ≤ F z
        simpa only [neg_neg, Set.mem_ofPred_eq, F] using hz.2)
    have hmkeq : ZerothHomotopy.mk x = ZerothHomotopy.mk y :=
      (TorusFiltration.superlevel_component_eq_iff_joinedIn F (-c) x y).mpr hxy
    exact hmkeq.symm.trans hxi

  -- PUBLIC63 has supplied only Finite I. The complementary union here is
  -- indexed by the finite subtype of all canonical classes other than i.
  have hPcomplOpen : ∀ i : I, IsOpen ((P i)ᶜ) := by
    intro i
    have hcompl : (P i)ᶜ = ⋃ j : {j : I // j ≠ i}, P j.val := by
      apply Set.Subset.antisymm
      · intro x hx
        have hxi : ZerothHomotopy.mk x ≠ i := hx
        exact Set.mem_iUnion.mpr ⟨⟨ZerothHomotopy.mk x, hxi⟩, rfl⟩
      · intro x hx
        obtain ⟨j, hxj⟩ := Set.mem_iUnion.mp hx
        have hxj' : ZerothHomotopy.mk x = j.val := hxj
        show ZerothHomotopy.mk x ≠ i
        intro hxi
        exact j.property (hxj'.symm.trans hxi)
    rw [hcompl]
    exact isOpen_iUnion (fun j : {j : I // j ≠ i} => hPopen j.val)
  have hPclosed : ∀ i : I, IsClosed (P i) := by
    intro i
    simpa only [compl_compl] using (hPcomplOpen i).isClosed_compl

  let C : I → Set (I4Torus.SourceTorus 2 L) :=
    fun i => Subtype.val '' P i
  let D : I → Set (I4Torus.SourceTorus 2 L) :=
    fun i => Subtype.val '' (P i)ᶜ
  have hCcompact : ∀ i : I, IsCompact (C i) := by
    intro i
    exact (hPclosed i).isCompact.image continuous_subtype_val
  have hDcompact : ∀ i : I, IsCompact (D i) := by
    intro i
    exact (hPopen i).isClosed_compl.isCompact.image continuous_subtype_val
  have hCDdisjoint : ∀ i : I, Disjoint (C i) (D i) := by
    intro i
    refine Set.disjoint_left.mpr ?_
    intro q hqC hqD
    obtain ⟨x, hx, hxq⟩ := hqC
    obtain ⟨y, hy, hyq⟩ := hqD
    have hxy : x = y := Subtype.ext (hxq.trans hyq.symm)
    exact hy (hxy ▸ hx)

  have hsep : ∀ i : I,
      ∃ A B : Set (I4Torus.SourceTorus 2 L),
        IsOpen A ∧ IsOpen B ∧ C i ⊆ A ∧ D i ⊆ B ∧ Disjoint A B := by
    intro i
    exact normal_separation (hCcompact i).isClosed (hDcompact i).isClosed
      (hCDdisjoint i)
  let A : I → Set (I4Torus.SourceTorus 2 L) :=
    fun i => Classical.choose (hsep i)
  let B : I → Set (I4Torus.SourceTorus 2 L) :=
    fun i => Classical.choose (Classical.choose_spec (hsep i))
  have hselected : ∀ i : I,
      IsOpen (A i) ∧ IsOpen (B i) ∧ C i ⊆ A i ∧ D i ⊆ B i ∧
        Disjoint (A i) (B i) := by
    intro i
    exact Classical.choose_spec (Classical.choose_spec (hsep i))
  have hA : ∀ i : I, IsOpen (A i) := fun i => (hselected i).1
  have hB : ∀ i : I, IsOpen (B i) := fun i => (hselected i).2.1
  have hCA : ∀ i : I, C i ⊆ A i := fun i => (hselected i).2.2.1
  have hDB : ∀ i : I, D i ⊆ B i := fun i => (hselected i).2.2.2.1
  have hAB : ∀ i : I, Disjoint (A i) (B i) :=
    fun i => (hselected i).2.2.2.2
  let U : I → Set (I4Torus.SourceTorus 2 L) :=
    fun i => A i ∩ ⋂ j : {j : I // j ≠ i}, B j.val
  have hUopen : ∀ i : I, IsOpen (U i) := by
    intro i
    exact (hA i).inter
      (isOpen_iInter_of_finite (fun j : {j : I // j ≠ i} => hB j.val))
  have hCU : ∀ i : I, C i ⊆ U i := by
    intro i q hqi
    refine ⟨hCA i hqi, Set.mem_iInter.mpr ?_⟩
    intro j
    apply hDB j.val
    obtain ⟨x, hxi, hxq⟩ := hqi
    refine ⟨x, ?_, hxq⟩
    change ZerothHomotopy.mk x ≠ j.val
    change ZerothHomotopy.mk x = i at hxi
    intro hxj
    exact j.property (hxj.symm.trans hxi)
  have hUpairwise : Pairwise fun i j : I => Disjoint (U i) (U j) := by
    intro i j hij
    refine Set.disjoint_left.mpr ?_
    intro q hqi hqj
    have hqBi : q ∈ B i := Set.mem_iInter.mp hqj.2 ⟨i, hij⟩
    exact Set.disjoint_left.mp (hAB i) hqi.1 hqBi

  -- Explicit ambient trace equality, including empty fibers and empty H.
  have htraceEq : ∀ i : I, U i ∩ H = C i := by
    intro i
    apply Set.Subset.antisymm
    · intro q hq
      let x : H := ⟨q, hq.2⟩
      have hxi : ZerothHomotopy.mk x = i := by
        by_contra hne
        have hqD : q ∈ D i := ⟨x, hne, rfl⟩
        exact Set.disjoint_left.mp (hAB i) hq.1.1 (hDB i hqD)
      exact ⟨x, hxi, rfl⟩
    · intro q hq
      obtain ⟨x, hxi, hxq⟩ := hq
      refine ⟨hCU i ⟨x, hxi, hxq⟩, ?_⟩
      exact hxq ▸ x.property
  have hcover : ∀ x : H, x.val ∈ U (ZerothHomotopy.mk x) := by
    intro x
    exact hCU (ZerothHomotopy.mk x) ⟨x, rfl, rfl⟩
  have htrace : ∀ (i : I) (x : H),
      x.val ∈ U i ↔ ZerothHomotopy.mk x = i := by
    intro i x
    constructor
    · intro hx
      have hmem : x.val ∈ C i := by
        rw [← htraceEq i]
        exact ⟨hx, x.property⟩
      obtain ⟨y, hy, hyx⟩ := hmem
      have hyx' : y = x := Subtype.ext hyx
      exact hyx' ▸ hy
    · intro hxi
      exact hCU i ⟨x, hxi, rfl⟩
  exact ⟨U, hUopen, hUpairwise, hcover, htrace⟩

private theorem actualSource_lower_clearance
    {L : ℝ} (hL : 0 < L) (omega : SmoothSample 2 L) (c : ℝ)
    (U : Set (I4Torus.SourceTorus 2 L)) (hU : IsOpen U)
    (hcover : {q | c ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega q} ⊆ U) :
    ∃ delta : ℝ, 0 < delta ∧ ∀ b : ℝ, c - delta ≤ b → b ≤ c →
      {q | b ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega q} ⊆ U := by
  let : Fact (0 < L) := ⟨hL⟩
  let F := SourceActualFoldTorus.actualTorusField hL.ne' omega
  have hF : Continuous F := SourceActualFoldTorus.actualTorusField_continuous hL.ne' omega
  by_cases hK : Uᶜ.Nonempty
  · have hcompact : IsCompact Uᶜ := hU.isClosed_compl.isCompact
    obtain ⟨x, hx, hmax⟩ := hcompact.exists_isMaxOn hK hF.continuousOn
    have hxc : F x < c := by
      apply lt_of_not_ge
      intro hcx
      exact hx (hcover hcx)
    refine ⟨(c - F x) / 2, by linarith, ?_⟩
    intro b hlow _ q hq
    by_contra hqU
    have hle : F q ≤ F x := hmax hqU
    change b ≤ F q at hq
    linarith
  · refine ⟨1, by norm_num, ?_⟩
    intro b _ _ q _
    by_contra hqU
    exact hK ⟨q, hqU⟩

private theorem joinedIn_disjoint_open_piece
    {X : Type*} [TopologicalSpace X] {I : Type*}
    (U : I → Set X) (hU : ∀ i, IsOpen (U i))
    (hdis : Pairwise fun i j => Disjoint (U i) (U j))
    {a b : X} (hpath : JoinedIn (⋃ i, U i) a b)
    (i : I) (ha : a ∈ U i) : b ∈ U i := by
  classical
  let V : Set X := ⋃ j, ⋃ (_ : j ≠ i), U j
  have hV : IsOpen V := isOpen_iUnion fun j => isOpen_iUnion fun _ => hU j
  have hdV : Disjoint (U i) V := by
    apply Set.disjoint_left.mpr
    intro x hxi hxV
    rcases mem_iUnion.mp hxV with ⟨j, hj⟩
    rcases mem_iUnion.mp hj with ⟨hji, hxj⟩
    exact (Set.disjoint_left.mp (hdis hji.symm)) hxi hxj
  have hrange : Set.range hpath.somePath ⊆ U i ∪ V := by
    rintro x ⟨t, rfl⟩
    rcases mem_iUnion.mp (hpath.somePath_mem t) with ⟨j, hj⟩
    by_cases hji : j = i
    · exact Or.inl (hji ▸ hj)
    · exact Or.inr (mem_iUnion.mpr ⟨j, mem_iUnion.mpr ⟨hji, hj⟩⟩)
  have hstart : (Set.range hpath.somePath ∩ U i).Nonempty :=
    ⟨a, ⟨0, by simp⟩, ha⟩
  have hsub : Set.range hpath.somePath ⊆ U i :=
    IsPreconnected.subset_left_of_subset_union (hU i) hV hdV hrange hstart
      (isConnected_range hpath.somePath.continuous).isPreconnected
  exact hsub ⟨1, by simp⟩

private theorem actualSource_injective_of_ambient_separation
    {L : ℝ} (hL : 0 < L) (omega : SmoothSample 2 L) (c : ℝ)
    (U : ZerothHomotopy
      (TorusFiltration.superlevel_set
        (SourceActualFoldTorus.actualTorusField hL.ne' omega) (-c)) →
        Set (I4Torus.SourceTorus 2 L))
    (hU : ∀ i, IsOpen (U i))
    (hdis : Pairwise fun i j => Disjoint (U i) (U j))
    (hmem : ∀ x : TorusFiltration.superlevel_set
        (SourceActualFoldTorus.actualTorusField hL.ne' omega) (-c),
      x.val ∈ U (ZerothHomotopy.mk x))
    (htrace : ∀ i (x : TorusFiltration.superlevel_set
        (SourceActualFoldTorus.actualTorusField hL.ne' omega) (-c)),
      x.val ∈ U i ↔ ZerothHomotopy.mk x = i) :
    ∃ delta : ℝ, 0 < delta ∧ ∀ b : ℝ, c - delta ≤ b →
      ∀ hbelow : b ≤ c, Function.Injective
        (TorusFiltration.superlevel_componentInclusion
          (SourceActualFoldTorus.actualTorusField hL.ne' omega)
          (s := -c) (t := -b) (neg_le_neg hbelow)) := by
  classical
  let F := SourceActualFoldTorus.actualTorusField hL.ne' omega
  by_cases hH : (TorusFiltration.superlevel_set F (-c)).Nonempty
  · let V := ⋃ i, U i
    have hV : IsOpen V := isOpen_iUnion hU
    have hcover : {q | c ≤ F q} ⊆ V := by
      intro q hq
      let x : TorusFiltration.superlevel_set F (-c) :=
        ⟨q, by simpa [TorusFiltration.superlevel_set] using hq⟩
      exact mem_iUnion.mpr ⟨ZerothHomotopy.mk x, hmem x⟩
    obtain ⟨delta, hdelta, hclear⟩ :=
      actualSource_lower_clearance hL omega c V hV hcover
    refine ⟨delta, hdelta, ?_⟩
    intro b hlow hbelow q r heq
    obtain ⟨x, rfl⟩ := ZerothHomotopy.mk_surjective q
    obtain ⟨y, rfl⟩ := ZerothHomotopy.mk_surjective r
    have hx : c ≤ F x.val := by
      simpa [TorusFiltration.superlevel_set] using x.property
    have hy : c ≤ F y.val := by
      simpa [TorusFiltration.superlevel_set] using y.property
    let xb : TorusFiltration.superlevel_set F (-b) :=
      ⟨x.val, by simpa [TorusFiltration.superlevel_set] using le_trans hbelow hx⟩
    let yb : TorusFiltration.superlevel_set F (-b) :=
      ⟨y.val, by simpa [TorusFiltration.superlevel_set] using le_trans hbelow hy⟩
    change ZerothHomotopy.mk xb = ZerothHomotopy.mk yb at heq
    have hjoined : JoinedIn (TorusFiltration.superlevel_set F (-b)) x.val y.val :=
      (TorusFiltration.superlevel_component_eq_iff_joinedIn F (-b) xb yb).mp heq
    have hlower : TorusFiltration.superlevel_set F (-b) ⊆ V := by
      intro z hz
      apply hclear b hlow hbelow
      simpa [TorusFiltration.superlevel_set] using hz
    have hyU : y.val ∈ U (ZerothHomotopy.mk x) :=
      joinedIn_disjoint_open_piece U hU hdis (hjoined.mono hlower)
        (ZerothHomotopy.mk x) (hmem x)
    exact ((htrace _ y).mp hyU).symm
  · refine ⟨1, by norm_num, ?_⟩
    intro b _ _ q _ _
    obtain ⟨x, _⟩ := ZerothHomotopy.mk_surjective q
    exact False.elim (hH ⟨x.val, x.property⟩)

theorem actualSource_closedSuperlevel_componentInclusion_locally_injective
    {L : ℝ} (hL : 0 < L) (omega : I4SmoothCarrier.SmoothSample 2 L)
    (hm : UniversalLaw.Spec.Lifetime.IsMorseDistinct 2 L
      (I4LifetimeField.actualField 2 L omega)) (c : ℝ) :
    ∃ delta : ℝ, 0 < delta ∧ ∀ (b : ℝ), c - delta ≤ b →
      ∀ hbelow : b ≤ c, Function.Injective
        (TorusFiltration.superlevel_componentInclusion
          (SourceActualFoldTorus.actualTorusField hL.ne' omega)
          (s := -c) (t := -b) (neg_le_neg hbelow)) := by
  obtain ⟨U, hU, hdis, hmem, htrace⟩ :=
    actualSource_closedSuperlevel_ambient_separation hL omega hm c
  exact actualSource_injective_of_ambient_separation hL omega c U hU hdis hmem htrace

end I4SourceActualLowerSeparation
