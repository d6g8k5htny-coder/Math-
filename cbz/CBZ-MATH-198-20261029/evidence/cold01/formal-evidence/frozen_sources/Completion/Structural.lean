import Closure.PaletteCover
import Closure.LocalRatio

namespace UniversalLaw.P15Completion
open UniversalLaw.Spec.P15
open UniversalLaw.P15Closure

variable {X : Type} [Fintype X] [DecidableEq X]

/-- The exact local capacity formula, including the empty palette. -/
theorem localDecomposability (F : RealizedData X) : LocalDecomposability F := by
  classical
  intro hF i k S hS
  constructor
  · rintro ⟨parts,hgood,hdisj,hunion⟩
    have hpart (j : Fin k) : parts j ⊆ S := by
      intro x hx
      rw [← hunion]
      exact Finset.mem_biUnion.mpr ⟨j,Finset.mem_univ _,hx⟩
    calc
      S.card = ((Finset.univ : Finset (Fin k)).biUnion parts).card := congrArg Finset.card hunion.symm
      _ ≤ ∑ j : Fin k, (parts j).card := Finset.card_biUnion_le
      _ ≤ ∑ _j : Fin k, F.a i := Finset.sum_le_sum (fun j _ =>
        (localRestriction F hF i _ ((hpart j).trans hS)).mp (hgood j))
      _ = F.a i * k := by simp [Nat.mul_comm]
  · intro hcard
    obtain ⟨f,hf,hcap⟩ := exists_capacity_coloring S (Finset.univ : Finset (Fin k))
      (by simpa using hcard)
    let parts (j : Fin k) : Finset X :=
      (S.attach.filter (fun x => f x = j)).image Subtype.val
    have hmem (x : X) (j : Fin k) : x ∈ parts j ↔ ∃ hx : x ∈ S, f ⟨x,hx⟩ = j := by
      simp only [parts, Finset.mem_image, Finset.mem_filter, Finset.mem_attach, true_and]
      constructor
      · rintro ⟨y,hy,rfl⟩
        exact ⟨y.property,hy⟩
      · rintro ⟨hx,hj⟩
        exact ⟨⟨x,hx⟩,hj,rfl⟩
    refine ⟨parts,?_,?_,?_⟩
    · intro j
      apply (localRestriction F hF i _ ?_).mpr
      · have hinj : Function.Injective (Subtype.val : S → X) := Subtype.val_injective
        simpa only [parts, Finset.card_image_of_injective _ hinj,
          Finset.attach_eq_univ] using hcap j
      · intro x hx
        exact hS ((hmem x j).mp hx).choose
    · intro j j' hjj'
      apply Finset.disjoint_left.mpr
      intro x hx hx'
      obtain ⟨hxS,hxj⟩ := (hmem x j).mp hx
      obtain ⟨hxS',hxj'⟩ := (hmem x j').mp hx'
      exact hjj' (hxj.symm.trans hxj')
    · ext x
      simp only [Finset.mem_biUnion,Finset.mem_univ,true_and]
      constructor
      · rintro ⟨j,hj⟩
        exact ((hmem x j).mp hj).choose
      · intro hx
        exact ⟨f ⟨x,hx⟩,(hmem x _).mpr ⟨hx,rfl⟩⟩

/-- The local obstruction at demand is the full block alone. -/
theorem localObstructionIsFullBlock (F : RealizedData X) : LocalObstructionIsFullBlock F := by
  classical
  intro hF i S hS
  rw [localDecomposability F hF i (F.d i) S hS]
  constructor
  · intro hn
    apply Finset.eq_of_subset_of_card_le hS
    rw [hF.2.2.1 i]
    omega
  · rintro rfl
    rw [hF.2.2.1 i]
    omega

/-- Occupied labels in a decomposition give the palettes demanded by strict capacity
products. This is the rounding step needed for the entire ground set. -/
theorem shifted_palette_of_decomposable (F : RealizedData X) {K : ℕ} (U : Finset X)
    (hsize : ∀ i, F.a i * F.d i < (U ∩ block F i).card)
    (hdec : IsKDecomposable F K U) :
    IsPaletteFeasible F.b F.H (fun i => F.d i + 1) K := by
  classical
  obtain ⟨parts,hgood,hdisj,hunion⟩ := hdec
  let P : Fin F.b → Finset (Fin K) :=
    fun i => Finset.univ.filter (fun j => (parts j ∩ block F i).Nonempty)
  have hmem (i : Fin F.b) (j : Fin K) : j ∈ P i ↔ i ∈ supp F (parts j) := by
    simp only [P, Finset.mem_filter,Finset.mem_univ,true_and,supp,Finset.mem_image]
    constructor
    · rintro ⟨x,hx⟩
      exact ⟨x,(Finset.mem_inter.mp hx).1,by simpa [block] using (Finset.mem_inter.mp hx).2⟩
    · rintro ⟨x,hx,hxi⟩
      exact ⟨x,Finset.mem_inter.mpr ⟨hx,by simp [block,hxi]⟩⟩
  refine ⟨P,?_,?_⟩
  · intro i
    have hsub : U ∩ block F i ⊆ (P i).biUnion (fun j => parts j ∩ block F i) := by
      intro x hx
      have hxU : x ∈ (Finset.univ : Finset (Fin K)).biUnion parts :=
        hunion.symm ▸ (Finset.mem_inter.mp hx).1
      obtain ⟨j,hj,hxj⟩ := Finset.mem_biUnion.mp hxU
      have hxi : x ∈ parts j ∩ block F i := Finset.mem_inter.mpr ⟨hxj,(Finset.mem_inter.mp hx).2⟩
      have hPj : j ∈ P i := by
        simp only [P,Finset.mem_filter,Finset.mem_univ,true_and]
        exact ⟨x,hxi⟩
      exact Finset.mem_biUnion.mpr ⟨j,hPj,hxi⟩
    have hc : (U ∩ block F i).card ≤ (P i).card * F.a i := by
      calc
        _ ≤ ((P i).biUnion (fun j => parts j ∩ block F i)).card := Finset.card_le_card hsub
        _ ≤ ∑ j ∈ P i, (parts j ∩ block F i).card := Finset.card_biUnion_le
        _ ≤ ∑ j ∈ P i, F.a i := Finset.sum_le_sum (fun j hj => (hgood j).1 i)
        _ = (P i).card * F.a i := by simp
    have hstrict := (hsize i).trans_le hc
    change F.d i + 1 ≤ (P i).card
    by_contra hn
    have hle : (P i).card ≤ F.d i := by omega
    exact (not_lt_of_ge (Nat.mul_le_mul_left (F.a i) hle)) (by simpa [Nat.mul_comm] using hstrict)
  · intro e he j
    have hn := (hgood j).2 e he
    change ¬ ∀ i, i ∈ e → i ∈ supp F (parts j) at hn
    push Not at hn
    obtain ⟨i,hie,hi⟩ := hn
    exact ⟨i,hie,fun hip => hi ((hmem i j).mp hip)⟩

/-- The whole ground set needs exactly the shifted palette threshold. -/
theorem wholeGroundChromaticNumber (F : RealizedData X) : WholeGroundChromaticNumber F := by
  classical
  intro hF K
  constructor
  · intro hdec
    apply Nat.sInf_le
    apply shifted_palette_of_decomposable F Finset.univ _ hdec
    intro i
    simp only [Finset.univ_inter,hF.2.2.1 i]
    omega
  · intro hK
    have hP : IsPaletteFeasible F.b F.H (fun i => F.d i + 1) K := by
      apply palette_feasible_mono (fun e he =>
        Finset.card_pos.mp (by have := hF.2.2.2.1 e he; omega)) hK
      exact Nat.sInf_mem (palette_feasible_nonempty F.b F.H (fun i => F.d i + 1) hF.2.2.2.1)
    let G : RealizedData X := { F with d := fun i => F.d i + 1 }
    apply decomposable_of_palette G hP Finset.univ
    intro i
    change (Finset.univ ∩ block F i).card ≤ F.a i * (F.d i + 1)
    simp only [Finset.univ_inter,hF.2.2.1 i]
    have := hF.1 i
    nlinarith

/-- Erase minimality forces an edge-supported forbidden set to have exactly one
coordinate in every occupied block. -/
theorem minimal_edge_fiber (F : RealizedData X) (U : Finset X)
    (hmin : IsMinimalForbidden F U) (e : Finset (Fin F.b)) (he : e ∈ F.H)
    (hes : e ⊆ supp F U) (v : X) (hv : v ∈ U) :
    F.blk v ∈ e ∧ U ∩ block F (F.blk v) = {v} := by
  classical
  have hn := (hmin.2 v hv).2 e he
  have hex : ∃ j ∈ e, j ∉ supp F (U.erase v) := by
    by_contra hh
    push Not at hh
    exact hn hh
  obtain ⟨j,hje,hjn⟩ := hex
  obtain ⟨x,hx,hxj⟩ := Finset.mem_image.mp (hes hje)
  have hxv : x = v := by
    by_contra hne
    exact hjn (Finset.mem_image.mpr ⟨x,Finset.mem_erase.mpr ⟨hne,hx⟩,hxj⟩)
  subst x
  refine ⟨hxj ▸ hje,?_⟩
  apply Finset.eq_singleton_iff_unique_mem.mpr
  refine ⟨Finset.mem_inter.mpr ⟨hv,by simp [block]⟩,?_⟩
  intro y hy
  by_contra hyv
  have hyblk : F.blk y = F.blk v := by simpa [block] using (Finset.mem_inter.mp hy).2
  exact hjn (Finset.mem_image.mpr
    ⟨y,Finset.mem_erase.mpr ⟨hyv,(Finset.mem_inter.mp hy).1⟩,hyblk.trans hxj⟩)

/-- A transversal has at most one point in each block, including blocks outside its
support. -/
theorem transversal_local_card_le_one (F : RealizedData X) {e : Finset (Fin F.b)}
    {U : Finset X} (h : IsTransversal F e U) (i : Fin F.b) :
    (U ∩ block F i).card ≤ 1 := by
  classical
  by_cases hi : i ∈ e
  · exact (h.2 i hi).le
  · have he : U ∩ block F i = ∅ := by
      apply Finset.eq_empty_iff_forall_notMem.mpr
      intro v hv
      have hvi : F.blk v = i := by simpa [block] using (Finset.mem_inter.mp hv).2
      have hs : i ∈ supp F U := Finset.mem_image.mpr ⟨v,(Finset.mem_inter.mp hv).1,hvi⟩
      exact hi (h.1 ▸ hs)
    simp [he]

/-- The exact minimal-forbidden classification for realized capacity/clutter data. -/
theorem minimalForbiddenCharacterisation (F : RealizedData X) :
    MinimalForbiddenCharacterisation F := by
  classical
  intro hF U
  constructor
  · intro hmin
    by_cases hcap : ∀ i, (U ∩ block F i).card ≤ F.a i
    · right
      have hex : ∃ e ∈ F.H, e ⊆ supp F U := by
        by_contra hh
        push Not at hh
        exact hmin.1 ⟨hcap,hh⟩
      obtain ⟨e,he,hes⟩ := hex
      refine ⟨e,he,?_,?_⟩
      · apply Finset.Subset.antisymm
        · intro i hi
          obtain ⟨v,hv,rfl⟩ := Finset.mem_image.mp hi
          exact (minimal_edge_fiber F U hmin e he hes v hv).1
        · exact hes
      · intro i hi
        obtain ⟨v,hv,hvi⟩ := Finset.mem_image.mp (hes hi)
        have hsingle := (minimal_edge_fiber F U hmin e he hes v hv).2
        rw [hvi] at hsingle
        simp [hsingle]
    · left
      push Not at hcap
      obtain ⟨i,hi⟩ := hcap
      have hsub : U ⊆ block F i := by
        intro v hv
        by_contra hvblock
        have heq : U.erase v ∩ block F i = U ∩ block F i := by
          ext x
          simp only [Finset.mem_inter,Finset.mem_erase]
          constructor
          · tauto
          · rintro ⟨hx,hxi⟩
            exact ⟨⟨fun h => hvblock (h ▸ hxi),hx⟩,hxi⟩
        have hgood := (hmin.2 v hv).1 i
        rw [heq] at hgood
        omega
      have hUcard : F.a i < U.card := by
        simpa only [Finset.inter_eq_left.mpr hsub] using hi
      obtain ⟨v,hv⟩ := Finset.card_pos.mp (by omega : 0 < U.card)
      have herase := (hmin.2 v hv).1 i
      rw [Finset.inter_eq_left.mpr ((Finset.erase_subset v U).trans hsub),
        Finset.card_erase_of_mem hv] at herase
      exact ⟨i,hsub,by omega⟩
  · rintro (⟨i,hsub,hcard⟩ | ⟨e,he,htrans⟩)
    · refine ⟨?_,?_⟩
      · intro hg
        have hc := hg.1 i
        rw [Finset.inter_eq_left.mpr hsub,hcard] at hc
        omega
      · intro v hv
        apply (localRestriction F hF i (U.erase v) ((Finset.erase_subset v U).trans hsub)).mpr
        rw [Finset.card_erase_of_mem hv,hcard]
        omega
    · refine ⟨fun hg => hg.2 e he (by rw [htrans.1]),?_⟩
      intro v hv
      have hsU : supp F (U.erase v) ⊆ supp F U := Finset.image_subset_image (Finset.erase_subset v U)
      have hvE : F.blk v ∈ e := htrans.1 ▸ Finset.mem_image.mpr ⟨v,hv,rfl⟩
      have hvblock : v ∈ U ∩ block F (F.blk v) := Finset.mem_inter.mpr ⟨hv,by simp [block]⟩
      have hsingle : U ∩ block F (F.blk v) = {v} := by
        obtain ⟨x,hx⟩ := Finset.card_eq_one.mp (htrans.2 _ hvE)
        have hvx : v = x := Finset.mem_singleton.mp (hx ▸ hvblock)
        simpa only [hvx] using hx
      have hvabsent : F.blk v ∉ supp F (U.erase v) := by
        intro hh
        obtain ⟨x,hx,hxv⟩ := Finset.mem_image.mp hh
        have hxorig : x ∈ U ∩ block F (F.blk v) :=
          Finset.mem_inter.mpr ⟨(Finset.mem_erase.mp hx).2,by simp [block,hxv]⟩
        have heq : x = v := Finset.mem_singleton.mp (hsingle ▸ hxorig)
        exact (Finset.mem_erase.mp hx).1 heq
      refine ⟨?_,?_⟩
      · intro i
        calc
          (U.erase v ∩ block F i).card ≤ (U ∩ block F i).card :=
            Finset.card_le_card (Finset.inter_subset_inter_right (Finset.erase_subset v U))
          _ ≤ 1 := transversal_local_card_le_one F htrans i
          _ ≤ F.a i := hF.1 i
      · intro f hf hfs
        have hfe : f ⊆ e := hfs.trans (hsU.trans (by rw [htrans.1]))
        have hEq : f = e := hF.2.2.2.2 f hf e he hfe
        exact hvabsent (hfs (hEq.symm ▸ hvE))

#check minimalForbiddenCharacterisation
#print axioms minimalForbiddenCharacterisation
#check localDecomposability
#print axioms localDecomposability
#check localObstructionIsFullBlock
#print axioms localObstructionIsFullBlock
#check wholeGroundChromaticNumber
#print axioms wholeGroundChromaticNumber

end UniversalLaw.P15Completion
