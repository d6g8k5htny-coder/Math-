import MorseFiniteCritical
import SuperlevelBar
import ClosedSuperlevel

/-!
# Conditional attainment at the literal C263 death height

The fixed older critical endpoint is derived from C293 and compact topology.
The only additional geometric premise is local path connectivity of the actual
closed death superlevel. This file does not derive that premise from Morse data,
prove strict death drop, or identify an elder saddle or an exhaustive barcode.
-/

noncomputable section

open Set Topology
open UniversalLaw.Spec.Lifetime TorusFiltration TorusMorseFinite

namespace TorusCriticalAttainment

/-- The lattice formula is identical in the two frozen source predicates. -/
theorem periodic_transport {d : ℕ} {L : ℝ} {g : E d → ℝ}
    (hperiodic : IsLPeriodic d L g) : torus_isPeriodic d L g := by
  simpa only [IsLPeriodic, torus_isPeriodic, latticeVec, torus_latticeVec] using hperiodic

def descendedHeight (d : ℕ) (L : ℝ) (hL : 0 < L) (g : E d → ℝ)
    (hperiodic : IsLPeriodic d L g) : torus_quotient d L hL → ℝ :=
  torus_descend d L hL g (periodic_transport hperiodic)

@[simp] theorem descendedHeight_proj (d : ℕ) (L : ℝ) (hL : 0 < L)
    (g : E d → ℝ) (hperiodic : IsLPeriodic d L g) (x : E d) :
    descendedHeight d L hL g hperiodic (torus_proj d L hL x) = g x := rfl

theorem descendedHeight_continuous {d : ℕ} {L : ℝ} (hL : 0 < L)
    {g : E d → ℝ} (hperiodic : IsLPeriodic d L g) (hsmooth : IsSmooth d g) :
    Continuous (descendedHeight d L hL g hperiodic) :=
  torus_descend_continuous d L hL g (periodic_transport hperiodic)
    ((hsmooth 0).continuous)

/-- Closed connected components of a closed subspace, viewed in the ambient space. -/
theorem closed_connectedComponentIn {X : Type*} [TopologicalSpace X]
    {s : Set X} (hs : IsClosed s) (x : X) :
    IsClosed (connectedComponentIn s x) := by
  by_cases hx : x ∈ s
  · rw [connectedComponentIn_eq_image hx]
    exact hs.isClosedEmbedding_subtypeVal.isClosedMap _ isClosed_connectedComponent
  · rw [connectedComponentIn_eq_empty hx]
    exact isClosed_empty

/-- Compact directed intersection connectedness; the members need not be path connected.
This auxiliary lemma uses the compact-Hausdorff separation argument, not compactness of paths. -/
theorem preconnected_iInter_of_directed {X ι : Type*} [TopologicalSpace X]
    [CompactSpace X] [T2Space X] [Nonempty ι] (K : ι → Set X)
    (hclosed : ∀ i, IsClosed (K i)) (hconnected : ∀ i, IsPreconnected (K i))
    (hdirected : Directed (· ⊇ ·) K) : IsPreconnected (⋂ i, K i) := by
  rw [isPreconnected_iff_subset_of_fully_disjoint_closed (isClosed_iInter hclosed)]
  intro a b ha hb hcover hab
  obtain ⟨u, v, hu, hv, hau, hbv, huv⟩ := normal_separation ha hb hab
  have hd : Disjoint (u ∪ v)ᶜ (⋂ i, K i) :=
    disjoint_compl_left_iff_subset.mpr (hcover.trans (union_subset_union hau hbv))
  obtain ⟨i, hi⟩ := (hu.union hv).isClosed_compl.isCompact.elim_directed_family_closed
    K hclosed hd hdirected
  have hKi : K i ⊆ u ∪ v := disjoint_compl_left_iff_subset.mp hi
  rcases (hconnected i).subset_or_subset hu hv huv hKi with hKu | hKv
  · left
    intro x hx
    rcases hcover hx with hxa | hxb
    · exact hxa
    · exact False.elim (Set.disjoint_left.mp huv (hKu (mem_iInter.mp hx i)) (hbv hxb))
  · right
    intro x hx
    rcases hcover hx with hxa | hxb
    · exact False.elim (Set.disjoint_left.mp huv (hau hxa) (hKv (mem_iInter.mp hx i)))
    · exact hxb

/-- Closedness of the actual lattice gives the actual quotient its Hausdorff topology. -/
theorem quotient_t2 (d : ℕ) (L : ℝ) (hL : 0 < L) :
    T2Space (torus_quotient d L hL) := by
  let : IsClosed ((torus_periodLattice d L hL).toAddSubgroup : Set (E d)) :=
    (torus_periodLattice d L hL).toAddSubgroup.isClosed_of_discreteTopology
  infer_instance

/-- Ambient local path connectivity descends to C263's actual quotient. -/
theorem quotient_locallyPathConnectedSpace (d : ℕ) (L : ℝ) (hL : 0 < L) :
    LocallyPathConnectedSpace (torus_quotient d L hL) := by
  exact inferInstanceAs (LocallyPathConnectedSpace (Quotient _))

/-- A component maximum strictly inside a superlevel is a local maximum.
Ambient local connectedness suffices; the closed superlevel need not be locally connected. -/
theorem component_maximum_isLocalMax {X : Type*} [TopologicalSpace X]
    [LocallyConnectedSpace X] (F : X → ℝ) (hF : Continuous F)
    (a : ℝ) (x q : X) (hq : q ∈ connectedComponentIn {y | a ≤ F y} x)
    (haq : a < F q) (hmax : IsMaxOn F (connectedComponentIn {y | a ≤ F y} x) q) :
    IsLocalMax F q := by
  apply hmax.isLocalMax
  rw [connectedComponentIn_eq hq]
  apply connectedComponentIn_mem_nhds
  exact Filter.mem_of_superset ((isOpen_lt continuous_const hF).mem_nhds haq)
    (fun y hy => show a ≤ F y from (show a < F y from hy).le)

/-- A quotient local maximum pulls back to a literal critical point.
No manifold derivative on the quotient is introduced. -/
theorem localMax_mem_quotientCriticalSet {d : ℕ} {L : ℝ} (hL : 0 < L)
    {g : E d → ℝ} (hperiodic : IsLPeriodic d L g)
    (q : torus_quotient d L hL)
    (hq : IsLocalMax (descendedHeight d L hL g hperiodic) q) :
    q ∈ quotientCriticalSet d L hL g := by
  obtain ⟨x, rfl⟩ := torus_proj_surjective d L hL q
  refine ⟨x, ?_, rfl⟩
  exact (hq.comp_continuous (torus_proj_continuous d L hL).continuousAt).fderiv_eq_zero

/-- The actual strict cut puts an older critical point in every closed component
strictly below the literal death height. -/
theorem older_critical_in_component (d : ℕ) (L : ℝ) (hL : 0 < L)
    (g : E d → ℝ) (hsmooth : IsSmooth d g) (hperiodic : IsLPeriodic d L g)
    (M : E d) (hnonessential : ¬ superlevelBar_isEssential g M)
    (a : ℝ) (ha : a < superlevelBar_deathHeight g M) :
    ∃ Q ∈ quotientCriticalSet d L hL g,
      g M < descendedHeight d L hL g hperiodic Q ∧
      Q ∈ connectedComponentIn {q | a ≤ descendedHeight d L hL g hperiodic q}
        (torus_proj d L hL M) := by
  let X := torus_quotient d L hL
  let F := descendedHeight d L hL g hperiodic
  let m := torus_proj d L hL M
  let A : Set X := {q | a ≤ F q}
  let K := connectedComponentIn A m
  let : CompactSpace X := ⟨torus_compact d L hL⟩
  let : LocallyPathConnectedSpace X := quotient_locallyPathConnectedSpace d L hL
  have hF : Continuous F := descendedHeight_continuous hL hperiodic hsmooth
  have hg : Continuous g := (hsmooth 0).continuous
  have hA : IsClosed A := by
    simpa only [A, ← superlevel_neg_height] using superlevel_isClosed F hF (-a)
  have hK : IsCompact K := (closed_connectedComponentIn hA m).isCompact
  have hm : m ∈ A := (ha.le.trans (superlevelBar_death_le_start g hg M hnonessential))
  obtain ⟨y, hy, γ, hγ⟩ := (superlevelBar_strict_cut g hg M hnonessential a).mp ha
  have hpath : JoinedIn A m (torus_proj d L hL y) :=
    ⟨γ.map (torus_proj_continuous d L hL), fun t => (hγ t).le⟩
  have hyK : torus_proj d L hL y ∈ K := by
    rw [show K = connectedComponentIn A m from rfl, connectedComponentIn_eq_image hm]
    exact ⟨⟨torus_proj d L hL y, hpath.target_mem⟩,
      pathComponent_subset_component _ (mem_pathComponent_iff.mpr hpath.joined_subtype), rfl⟩
  obtain ⟨Q, hQ, hmax⟩ := hK.exists_isMaxOn ⟨m, mem_connectedComponentIn hm⟩ hF.continuousOn
  have hQolder : g M < F Q := hy.trans_le (hmax hyK)
  have haQ : a < F Q :=
    ha.trans_le (superlevelBar_death_le_start g hg M hnonessential) |>.trans hQolder
  have hlocal : IsLocalMax F Q := component_maximum_isLocalMax F hF a m Q hQ haQ hmax
  exact ⟨Q, localMax_mem_quotientCriticalSet hL hperiodic Q hlocal, hQolder, hQ⟩

/-- Main conditional theorem. The endpoint, its strict older height, the path, and
its attained minimum are conclusions. Only closed-level LPC is an extra geometric input. -/
theorem quotient_death_attainment (d : ℕ) (L : ℝ) (hL : 0 < L)
    (g : E d → ℝ) (hsmooth : IsSmooth d g) (hperiodic : IsLPeriodic d L g)
    (hmorse : IsMorseDistinct d L g) (M : E d)
    (hnonessential : ¬ superlevelBar_isEssential g M)
    (hclosedLPC : LocallyPathConnectedSpace
      {q : torus_quotient d L hL //
        superlevelBar_deathHeight g M ≤ descendedHeight d L hL g hperiodic q}) :
    ∃ Q ∈ quotientCriticalSet d L hL g,
      g M < descendedHeight d L hL g hperiodic Q ∧
      ∃ γ : Path (torus_proj d L hL M) Q,
        (∀ t : unitInterval,
          superlevelBar_deathHeight g M ≤ descendedHeight d L hL g hperiodic (γ t)) ∧
        ∃ t : unitInterval,
          descendedHeight d L hL g hperiodic (γ t) = superlevelBar_deathHeight g M := by
  let X := torus_quotient d L hL
  let F := descendedHeight d L hL g hperiodic
  let m := torus_proj d L hL M
  let δ := superlevelBar_deathHeight g M
  let I := Set.Iio δ
  let A : Set X := {q | δ ≤ F q}
  let K : I → Set X := fun a => connectedComponentIn {q | a.val ≤ F q} m
  let C : Set X := quotientCriticalSet d L hL g ∩ {q | g M < F q}
  let : CompactSpace X := ⟨torus_compact d L hL⟩
  let : T2Space X := quotient_t2 d L hL
  let : Nonempty I := ⟨⟨δ - 1, by change δ - 1 < δ; linarith⟩⟩
  let : LocallyPathConnectedSpace A := hclosedLPC
  have hF : Continuous F := descendedHeight_continuous hL hperiodic hsmooth
  have hg : Continuous g := (hsmooth 0).continuous
  have hmA : m ∈ A := superlevelBar_death_le_start g hg M hnonessential
  have hmK : ∀ a : I, m ∈ K a := by
    intro a
    apply mem_connectedComponentIn
    change a.val ≤ F m
    exact (show a.val < δ from a.property).le.trans hmA
  have hKclosed : ∀ a : I, IsClosed (K a) := fun a =>
    closed_connectedComponentIn (isClosed_le continuous_const hF) m
  have hKconnected : ∀ a : I, IsPreconnected (K a) := fun _ =>
    isPreconnected_connectedComponentIn
  have hKdirected : Directed (· ⊇ ·) K := by
    intro a b
    refine ⟨⟨max a.val b.val, ?_⟩, ?_, ?_⟩
    · change max a.val b.val < δ
      exact max_lt a.property b.property
    · apply connectedComponentIn_mono m
      intro q h
      change a.val ≤ F q
      change max a.val b.val ≤ F q at h
      exact (le_max_left a.val b.val).trans h
    · apply connectedComponentIn_mono m
      intro q h
      change b.val ≤ F q
      change max a.val b.val ≤ F q at h
      exact (le_max_right a.val b.val).trans h
  have hCcompact : IsCompact C :=
    ((quotientCriticalSet_finite d L hL g hsmooth hperiodic hmorse).subset
      inter_subset_left).isCompact
  have hCK : ∀ a : I, (C ∩ K a).Nonempty := by
    intro a
    obtain ⟨Q, hQ, hQolder, hQK⟩ :=
      older_critical_in_component d L hL g hsmooth hperiodic M hnonessential a.val a.property
    exact ⟨Q, ⟨hQ, hQolder⟩, hQK⟩
  have hCinter : (C ∩ ⋂ a : I, K a).Nonempty := by
    by_contra hn
    have hd : Disjoint C (⋂ a : I, K a) := by
      exact Set.disjoint_iff_inter_eq_empty.mpr (Set.not_nonempty_iff_eq_empty.mp hn)
    obtain ⟨a, ha⟩ := hCcompact.elim_directed_family_closed K hKclosed hd hKdirected
    exact (Set.not_nonempty_iff_eq_empty.mpr ha.inter_eq) (hCK a)
  obtain ⟨Q, hQC, hQinter⟩ := hCinter
  have hinterA : (⋂ a : I, K a) ⊆ A := by
    intro q hq
    by_contra hn
    have hlt : F q < δ := lt_of_not_ge hn
    obtain ⟨a, hqa, haδ⟩ := exists_between hlt
    have hqa' := connectedComponentIn_subset {q | a ≤ F q} m
      (mem_iInter.mp hq ⟨a, haδ⟩)
    exact (not_le_of_gt hqa) hqa'
  have hconn : IsPreconnected (⋂ a : I, K a) :=
    preconnected_iInter_of_directed K hKclosed hKconnected hKdirected
  have hQcomp : Q ∈ connectedComponentIn A m :=
    hconn.subset_connectedComponentIn (mem_iInter.mpr hmK) hinterA hQinter
  have hQA : Q ∈ A := hinterA hQinter
  have hsubcomp : (⟨Q, hQA⟩ : A) ∈ connectedComponent (⟨m, hmA⟩ : A) := by
    rw [connectedComponentIn_eq_image hmA] at hQcomp
    obtain ⟨q, hq, hqQ⟩ := hQcomp
    have heq : q = (⟨Q, hQA⟩ : A) := Subtype.ext hqQ
    rwa [heq] at hq
  have hjoined : Joined (⟨m, hmA⟩ : A) (⟨Q, hQA⟩ : A) := by
    rw [← pathComponent_eq_connectedComponent] at hsubcomp
    exact mem_pathComponent_iff.mp hsubcomp
  obtain ⟨p⟩ := hjoined
  let γ : Path m Q := p.map continuous_subtype_val
  have hγ : ∀ t : unitInterval, δ ≤ F (γ t) := fun t => (p t).property
  have hattain : ∃ t : unitInterval, F (γ t) = δ := by
    by_contra hn
    have hstrict : ∀ t : unitInterval, δ < F (γ t) := by
      intro t
      exact lt_of_le_of_ne (hγ t) (fun heq => hn ⟨t, heq.symm⟩)
    have heuc := (torus_strict_higher_path_iff d L hL g
      (periodic_transport hperiodic) M δ).mpr ⟨Q, hQC.2, γ, hstrict⟩
    exact superlevelBar_death_not_mem_clearance g hg M hnonessential heuc
  exact ⟨Q, hQC.1, hQC.2, γ, hγ, hattain⟩

/-- Prescribed-start lift of the attained path, including literal criticality
of the actual lifted endpoint. -/
theorem euclidean_death_attainment (d : ℕ) (L : ℝ) (hL : 0 < L)
    (g : E d → ℝ) (hsmooth : IsSmooth d g) (hperiodic : IsLPeriodic d L g)
    (hmorse : IsMorseDistinct d L g) (M : E d)
    (hnonessential : ¬ superlevelBar_isEssential g M)
    (hclosedLPC : LocallyPathConnectedSpace
      {q : torus_quotient d L hL //
        superlevelBar_deathHeight g M ≤ descendedHeight d L hL g hperiodic q}) :
    ∃ y : E d, IsCriticalPoint d g y ∧ g M < g y ∧
      ∃ Γ : Path M y,
        (∀ t : unitInterval, superlevelBar_deathHeight g M ≤ g (Γ t)) ∧
        ∃ t : unitInterval, g (Γ t) = superlevelBar_deathHeight g M := by
  obtain ⟨Q, hQ, hQolder, γ, hγ, t, ht⟩ :=
    quotient_death_attainment d L hL g hsmooth hperiodic hmorse M hnonessential hclosedLPC
  obtain ⟨y, Γ, hy, hΓ⟩ := torus_path_lift_from d L hL γ
  have hheight : g y = descendedHeight d L hL g hperiodic Q :=
    congrArg (descendedHeight d L hL g hperiodic) hy
  have hcritical : IsCriticalPoint d g y := by
    have hzero := (mem_quotientCriticalSet_iff hL hperiodic Q).mp hQ
    rw [← hy] at hzero
    exact hzero
  have hvalues : ∀ s : unitInterval,
      g (Γ s) = descendedHeight d L hL g hperiodic (γ s) :=
    fun s => congrArg (descendedHeight d L hL g hperiodic) (hΓ s)
  exact ⟨y, hcritical, (by rw [hheight]; exact hQolder), Γ,
    fun s => (hvalues s).symm ▸ hγ s, t, (hvalues t).trans ht⟩

end TorusCriticalAttainment
