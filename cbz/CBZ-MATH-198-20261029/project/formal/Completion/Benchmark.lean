import Closure.PaletteCover
import Completion.PaletteFormula
import Completion.Structural

namespace UniversalLaw.P15Completion
open UniversalLaw.Spec.P15

 theorem benchmarkBlock (i : Fin 6) :
    block benchmark816 i = (Finset.univ : Finset (Fin 409)).image (fun j => (i,j)) := by
  classical
  ext x
  change (x ∈ Finset.univ.filter (fun v : Fin 6 × Fin 409 => v.1 = i)) ↔ _
  simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_image]
  constructor
  · intro h; exact ⟨x.2,Prod.ext h.symm rfl⟩
  · rintro ⟨j,h⟩; exact (congrArg Prod.fst h).symm

 theorem benchmarkBlockCard (i : Fin 6) : (block benchmark816 i).card = 409 := by
  classical
  rw [benchmarkBlock, Finset.card_image_of_injective]
  · simp
  · intro x y h
    exact congrArg Prod.snd h

 theorem benchmark816IsRealized : Benchmark816IsRealized := by
  classical
  refine ⟨by intro i; exact Nat.le_refl _, by intro i; exact Nat.le_of_lt (by decide : 1 < 408), ?_, ?_, ?_⟩
  · intro i
    simpa [benchmark816] using benchmarkBlockCard i
  · intro e he
    have h : e.card = 4 := (Finset.mem_powersetCard.mp he).2
    omega
  · intro e he f hf hef
    exact Finset.eq_of_subset_of_card_le hef (by
      have hec : e.card = 4 := (Finset.mem_powersetCard.mp he).2
      have hfc : f.card = 4 := (Finset.mem_powersetCard.mp hf).2
      omega)

 theorem benchmark816Palette : Benchmark816Palette := by
  have h := elementaryPaletteFormula 6 3 (fun _ => 408) (by decide) (by decide)
    (fun _ => by decide)
  norm_num [Fin.sum_univ_succ, Finset.sup_const] at h
  exact h

 theorem benchmark816PaletteWhole :
    paletteNumber 6 (completeClutter 6 3) (fun _ => 409) = 818 := by
  have h := elementaryPaletteFormula 6 3 (fun _ => 409) (by decide) (by decide)
    (fun _ => by decide)
  norm_num [Fin.sum_univ_succ, Finset.sup_const] at h
  exact h

 theorem benchmark816Cover : Benchmark816Cover := by
  have h := UniversalLaw.P15Closure.fullBlockCoverIff benchmark816 benchmark816IsRealized
  have hp : paletteNumber benchmark816.b benchmark816.H benchmark816.d = 816 :=
    benchmark816Palette
  constructor
  · exact (h 816).mpr (by rw [hp])
  · intro hc
    have := (h 815).mp hc
    rw [hp] at this
    omega

 theorem benchmark816WholeGround : Benchmark816WholeGround := by
  have h := wholeGroundChromaticNumber benchmark816 benchmark816IsRealized
  have hp : paletteNumber benchmark816.b benchmark816.H (fun i => benchmark816.d i + 1) = 818 :=
    benchmark816PaletteWhole
  constructor
  · exact (h 818).mpr (by rw [hp])
  · intro hc
    have := (h 817).mp hc
    rw [hp] at this
    omega

 theorem benchmarkMemBlock (x : Fin 6 × Fin 409) (i : Fin 6) :
    x ∈ block benchmark816 i ↔ x.1 = i := by
  classical
  rw [benchmarkBlock]
  constructor
  · intro h
    obtain ⟨j,hj,heq⟩ := Finset.mem_image.mp h
    exact (congrArg Prod.fst heq).symm
  · intro h
    exact Finset.mem_image.mpr ⟨x.2,Finset.mem_univ _,Prod.ext h.symm rfl⟩

 def internalEncode (z : Fin 6 × {S : Finset (Fin 409) // S.card = 2}) :
    Finset (Fin 6 × Fin 409) := z.2.val.image (fun j => (z.1,j))

 theorem internalEncode_subset (z : Fin 6 × {S : Finset (Fin 409) // S.card = 2}) :
    internalEncode z ⊆ block benchmark816 z.1 := by
  classical
  intro x hx
  obtain ⟨j,hj,rfl⟩ := Finset.mem_image.mp hx
  change (z.1,j) ∈ Finset.univ.filter (fun v : Fin 6 × Fin 409 => v.1 = z.1)
  exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, rfl⟩

 theorem internalEncode_card (z : Fin 6 × {S : Finset (Fin 409) // S.card = 2}) :
    (internalEncode z).card = 2 := by
  classical
  rw [internalEncode, Finset.card_image_of_injective]
  · exact z.2.property
  · intro x y h
    exact congrArg Prod.snd h

 theorem internalEncode_support (z : Fin 6 × {S : Finset (Fin 409) // S.card = 2}) :
    supp benchmark816 (internalEncode z) = {z.1} := by
  classical
  have hn : z.2.val.Nonempty := Finset.card_pos.mp (by rw [z.2.property]; decide)
  change (z.2.val.image (fun j => (z.1,j))).image Prod.fst = {z.1}
  ext i
  simp only [Finset.mem_image, Finset.mem_singleton]
  constructor
  · rintro ⟨x,⟨j,hj,rfl⟩,rfl⟩
    rfl
  · rintro rfl
    obtain ⟨j,hj⟩ := hn
    exact ⟨(z.1,j),⟨j,hj,rfl⟩,rfl⟩

 theorem internalEncode_injective : Function.Injective internalEncode := by
  classical
  intro x y h
  have hi : x.1 = y.1 := by
    have hs := congrArg (supp benchmark816) h
    rw [internalEncode_support, internalEncode_support] at hs
    exact Finset.singleton_injective hs
  apply Prod.ext hi
  apply Subtype.ext
  have hs := congrArg (Finset.image Prod.snd) h
  simpa [internalEncode, Finset.image_image] using hs

 theorem internalEncode_surjective (U : Finset (Fin 6 × Fin 409))
    (hU : ∃ i, U ⊆ block benchmark816 i ∧ U.card = 2) :
    ∃ z : Fin 6 × {S : Finset (Fin 409) // S.card = 2}, internalEncode z = U := by
  classical
  obtain ⟨i,hi,hc⟩ := hU
  have hfst (x) (hx : x ∈ U) : x.1 = i := by
    exact (Finset.mem_filter.mp (hi hx)).2
  have hinj : Set.InjOn Prod.snd (↑U : Set (Fin 6 × Fin 409)) := by
    intro x hx y hy he
    exact Prod.ext ((hfst x hx).trans (hfst y hy).symm) he
  refine ⟨(i,⟨U.image Prod.snd, by rw [Finset.card_image_iff.mpr hinj,hc]⟩), ?_⟩
  ext x
  simp only [internalEncode, Finset.mem_image]
  constructor
  · rintro ⟨j,⟨y,hy,rfl⟩,hx⟩
    have hxy : (i,y.2) = y := Prod.ext (hfst y hy).symm rfl
    exact hx ▸ hxy.symm ▸ hy
  · intro hx
    exact ⟨x.2,⟨x,hx,rfl⟩,Prod.ext (hfst x hx).symm rfl⟩

 theorem internalGeometry_count :
    Set.ncard {U : Finset (Fin 6 × Fin 409) | ∃ i, U ⊆ block benchmark816 i ∧ U.card = 2}
      = 6 * Nat.choose 409 2 := by
  classical
  have hr : {U : Finset (Fin 6 × Fin 409) | ∃ i, U ⊆ block benchmark816 i ∧ U.card = 2} =
      internalEncode '' Set.univ := by
    ext U
    constructor
    · intro h
      obtain ⟨z,rfl⟩ := internalEncode_surjective U h
      exact ⟨z,Set.mem_univ _,rfl⟩
    · rintro ⟨z,hz,rfl⟩
      exact ⟨z.1,internalEncode_subset z,internalEncode_card z⟩
  rw [hr, Set.ncard_image_of_injective _ internalEncode_injective]
  simp [Set.ncard_univ, Nat.card_eq_fintype_card]

 abbrev FourEdges := {e : Finset (Fin 6) // e.card = 4}
 abbrev CrossingCode := Σ e : FourEdges, e.val → Fin 409

 def crossingEncode (z : CrossingCode) : Finset (Fin 6 × Fin 409) :=
    z.1.val.attach.image (fun i => (i.val,z.2 i))

 theorem crossingEncode_support (z : CrossingCode) :
    supp benchmark816 (crossingEncode z) = z.1.val := by
  classical
  change (z.1.val.attach.image (fun i => (i.val,z.2 i))).image Prod.fst = z.1.val
  ext i
  simp only [Finset.mem_image, Finset.mem_attach, true_and]
  constructor
  · rintro ⟨x,⟨j,rfl⟩,rfl⟩
    exact j.property
  · intro hi
    exact ⟨(i,z.2 ⟨i,hi⟩),⟨⟨i,hi⟩,rfl⟩,rfl⟩

 theorem crossingEncode_inter (z : CrossingCode) (i : z.1.val) :
    crossingEncode z ∩ block benchmark816 i.val = {(i.val,z.2 i)} := by
  classical
  ext x
  rw [Finset.mem_inter, benchmarkMemBlock]
  change ((x ∈ z.1.val.attach.image (fun j => (j.val,z.2 j))) ∧ x.1 = i.val) ↔ _
  simp only [Finset.mem_image, Finset.mem_attach, true_and, Finset.mem_singleton]
  constructor
  · rintro ⟨⟨j,rfl⟩,hji⟩
    have heq : j = i := Subtype.ext hji
    subst j
    rfl
  · rintro rfl
    exact ⟨⟨i,rfl⟩,rfl⟩

 theorem crossingEncode_transversal (z : CrossingCode) :
    IsTransversal benchmark816 z.1.val (crossingEncode z) := by
  classical
  refine ⟨crossingEncode_support z,?_⟩
  intro i hi
  rw [crossingEncode_inter z ⟨i,hi⟩]
  exact Finset.card_singleton _

 theorem crossingEncode_injective : Function.Injective crossingEncode := by
  classical
  rintro ⟨e,f⟩ ⟨e',g⟩ h
  have he : e = e' := Subtype.ext (by
    have hs := congrArg (supp benchmark816) h
    rw [crossingEncode_support, crossingEncode_support] at hs
    exact hs)
  subst e'
  congr 1
  funext i
  have hm : (i.val,f i) ∈ crossingEncode ⟨e,g⟩ := by
    rw [← h]
    exact Finset.mem_image.mpr ⟨i,Finset.mem_attach _ _,rfl⟩
  obtain ⟨j,hj,hji⟩ := Finset.mem_image.mp hm
  have heq : j = i := Subtype.ext (congrArg Prod.fst hji)
  subst j
  exact (congrArg Prod.snd hji).symm

 theorem crossingEncode_surjective (U : Finset (Fin 6 × Fin 409))
    (hU : ∃ e : Finset (Fin 6), e.card = 4 ∧ IsTransversal benchmark816 e U) :
    ∃ z : CrossingCode, crossingEncode z = U := by
  classical
  obtain ⟨e,he,hs,hlocal⟩ := hU
  have hchoice : ∀ i : e, ∃ j : Fin 409, (i.val,j) ∈ U := by
    intro i
    have hi : i.val ∈ supp benchmark816 U := hs.symm ▸ i.property
    obtain ⟨x,hx,hxi⟩ := Finset.mem_image.mp hi
    have hxi' : x.1 = i.val := hxi
    have hxeq : (i.val,x.2) = x := Prod.ext hxi'.symm rfl
    exact ⟨x.2,hxeq.symm ▸ hx⟩
  choose f hf using hchoice
  refine ⟨⟨⟨e,he⟩,f⟩,?_⟩
  ext x
  constructor
  · intro hx
    obtain ⟨i,hi,rfl⟩ := Finset.mem_image.mp hx
    exact hf i
  · intro hx
    have hi : x.1 ∈ e := hs ▸ Finset.mem_image.mpr ⟨x,hx,rfl⟩
    have hcard := hlocal x.1 hi
    obtain ⟨y,hy⟩ := Finset.card_eq_one.mp hcard
    have hxmem : x ∈ U ∩ block benchmark816 x.1 := by
      exact Finset.mem_inter.mpr ⟨hx, (benchmarkMemBlock _ _).mpr rfl⟩
    have hfmem : (x.1,f ⟨x.1,hi⟩) ∈ U ∩ block benchmark816 x.1 := by
      exact Finset.mem_inter.mpr ⟨hf ⟨x.1,hi⟩,(benchmarkMemBlock _ _).mpr rfl⟩
    rw [hy, Finset.mem_singleton] at hxmem hfmem
    exact Finset.mem_image.mpr ⟨⟨x.1,hi⟩,Finset.mem_attach _ _,hfmem.trans hxmem.symm⟩

 theorem crossingGeometry_count :
    Set.ncard {U : Finset (Fin 6 × Fin 409) |
      ∃ e : Finset (Fin 6), e.card = 4 ∧ IsTransversal benchmark816 e U}
      = 15 * 409 ^ 4 := by
  classical
  have hr : {U : Finset (Fin 6 × Fin 409) |
      ∃ e : Finset (Fin 6), e.card = 4 ∧ IsTransversal benchmark816 e U} =
      crossingEncode '' Set.univ := by
    ext U
    constructor
    · intro h
      obtain ⟨z,rfl⟩ := crossingEncode_surjective U h
      exact ⟨z,Set.mem_univ _,rfl⟩
    · rintro ⟨z,hz,rfl⟩
      exact ⟨z.1.val,z.1.property,crossingEncode_transversal z⟩
  rw [hr, Set.ncard_image_of_injective _ crossingEncode_injective, Set.ncard_univ,
    Nat.card_eq_fintype_card, Fintype.card_sigma]
  have hc (e : FourEdges) : Fintype.card (e.val → Fin 409) = 409 ^ 4 := by
    simp only [Fintype.card_fun, Fintype.card_fin, Fintype.card_coe, e.property]
  simp only [hc, Finset.sum_const, Finset.card_univ]
  have hec : Fintype.card FourEdges = 15 := by
    rw [Fintype.card_finset_len, Fintype.card_fin]
    decide
  rw [hec]
  rfl

 theorem crossingEncode_card (z : CrossingCode) : (crossingEncode z).card = 4 := by
  classical
  have hinj : Function.Injective (fun i : z.1.val => (i.val,z.2 i)) := by
    intro i j h
    exact Subtype.ext (congrArg Prod.fst h)
  rw [crossingEncode,Finset.card_image_of_injective _ hinj,Finset.card_attach]
  exact z.1.property

 theorem benchmark_minimal_encoding (U : Finset (Fin 6 × Fin 409)) :
    IsMinimalForbidden benchmark816 U ↔
      (∃ z, internalEncode z = U) ∨ (∃ z, crossingEncode z = U) := by
  classical
  constructor
  · intro h
    rcases (minimalForbiddenCharacterisation benchmark816 benchmark816IsRealized U).mp h with
      ⟨i,hi,hc⟩ | ⟨e,he,ht⟩
    · exact Or.inl (internalEncode_surjective U ⟨i,hi,hc⟩)
    · exact Or.inr (crossingEncode_surjective U ⟨e,(Finset.mem_powersetCard.mp he).2,ht⟩)
  · intro h
    apply (minimalForbiddenCharacterisation benchmark816 benchmark816IsRealized U).mpr
    rcases h with ⟨z,rfl⟩ | ⟨z,rfl⟩
    · exact Or.inl ⟨z.1,internalEncode_subset z,internalEncode_card z⟩
    · exact Or.inr ⟨z.1.val,Finset.mem_powersetCard.mpr ⟨Finset.subset_univ _,z.1.property⟩,
        crossingEncode_transversal z⟩

 theorem internalEncode_support_card (z : Fin 6 × {S : Finset (Fin 409) // S.card = 2}) :
    (supp benchmark816 (internalEncode z)).card = 1 := by
  exact (congrArg (fun s : Finset (Fin 6) => s.card) (internalEncode_support z)).trans
    (Finset.card_singleton _)

 theorem crossingEncode_support_card (z : CrossingCode) :
    (supp benchmark816 (crossingEncode z)).card = 4 := by
  exact (congrArg (fun s : Finset (Fin 6) => s.card) (crossingEncode_support z)).trans z.1.property

 theorem benchmark_minimal_support (U : Finset (Fin 6 × Fin 409))
    (h : IsMinimalForbidden benchmark816 U) :
    (supp benchmark816 U).card = 1 ∨ (supp benchmark816 U).card = 4 := by
  rcases (benchmark_minimal_encoding U).mp h with ⟨z,rfl⟩ | ⟨z,rfl⟩
  · exact Or.inl (internalEncode_support_card z)
  · exact Or.inr (crossingEncode_support_card z)

 theorem benchmark_minimal_card_one (U : Finset (Fin 6 × Fin 409))
    (h : IsMinimalForbidden benchmark816 U) (hs : (supp benchmark816 U).card = 1) :
    U.card = 2 := by
  rcases (benchmark_minimal_encoding U).mp h with ⟨z,rfl⟩ | ⟨z,rfl⟩
  · exact internalEncode_card z
  · have hc := crossingEncode_support_card z
    omega

 theorem benchmark_minimal_card_four (U : Finset (Fin 6 × Fin 409))
    (h : IsMinimalForbidden benchmark816 U) (hs : (supp benchmark816 U).card = 4) :
    U.card = 4 := by
  rcases (benchmark_minimal_encoding U).mp h with ⟨z,rfl⟩ | ⟨z,rfl⟩
  · have hc := internalEncode_support_card z
    omega
  · exact crossingEncode_card z

set_option maxRecDepth 4096 in
 theorem benchmark816MinimalForbiddenCounts : Benchmark816MinimalForbiddenCounts := by
  classical
  have hOne : {U : Finset (Fin 6 × Fin 409) |
      IsMinimalForbidden benchmark816 U ∧ (supp benchmark816 U).card = 1} =
      {U : Finset (Fin 6 × Fin 409) | ∃ i, U ⊆ block benchmark816 i ∧ U.card = 2} := by
    ext U
    constructor
    · rintro ⟨hm,hs⟩
      rcases (benchmark_minimal_encoding U).mp hm with ⟨z,rfl⟩ | ⟨z,rfl⟩
      · exact ⟨z.1,internalEncode_subset z,internalEncode_card z⟩
      · have hc := crossingEncode_support_card z
        omega
    · intro h
      obtain ⟨z,rfl⟩ := internalEncode_surjective U h
      exact ⟨(benchmark_minimal_encoding _).mpr (Or.inl ⟨z,rfl⟩),internalEncode_support_card z⟩
  have hFour : {U : Finset (Fin 6 × Fin 409) |
      IsMinimalForbidden benchmark816 U ∧ (supp benchmark816 U).card = 4} =
      {U : Finset (Fin 6 × Fin 409) |
        ∃ e : Finset (Fin 6), e.card = 4 ∧ IsTransversal benchmark816 e U} := by
    ext U
    constructor
    · rintro ⟨hm,hs⟩
      rcases (benchmark_minimal_encoding U).mp hm with ⟨z,rfl⟩ | ⟨z,rfl⟩
      · have hc := internalEncode_support_card z
        omega
      · exact ⟨z.1.val,z.1.property,crossingEncode_transversal z⟩
    · intro h
      obtain ⟨z,rfl⟩ := crossingEncode_surjective U h
      exact ⟨(benchmark_minimal_encoding _).mpr (Or.inr ⟨z,rfl⟩),crossingEncode_support_card z⟩
  have hOneCount : Set.ncard {U : Finset (Fin 6 × Fin 409) |
      IsMinimalForbidden benchmark816 U ∧ (supp benchmark816 U).card = 1} =
      6 * Nat.choose 409 2 := by rw [hOne]; exact internalGeometry_count
  have hFourCount : Set.ncard {U : Finset (Fin 6 × Fin 409) |
      IsMinimalForbidden benchmark816 U ∧ (supp benchmark816 U).card = 4} =
      15 * 409 ^ 4 := by rw [hFour]; exact crossingGeometry_count
  refine ⟨hOneCount,hFourCount,?_⟩
  have hAll : {U : Finset (Fin 6 × Fin 409) | IsMinimalForbidden benchmark816 U} =
      {U | IsMinimalForbidden benchmark816 U ∧ (supp benchmark816 U).card = 1} ∪
      {U | IsMinimalForbidden benchmark816 U ∧ (supp benchmark816 U).card = 4} := by
    ext U
    constructor
    · intro h
      rcases benchmark_minimal_support U h with h1 | h4
      · exact Or.inl ⟨h,h1⟩
      · exact Or.inr ⟨h,h4⟩
    · rintro (h|h) <;> exact h.1
  rw [hAll,Set.ncard_union_eq]
  · exact congrArg₂ Nat.add hOneCount hFourCount
  · apply Set.disjoint_left.mpr
    intro U h1 h4
    have := h1.2
    have := h4.2
    omega

#check benchmark816IsRealized
#print axioms benchmark816IsRealized
#check benchmark816Palette
#print axioms benchmark816Palette
#check benchmark816Cover
#print axioms benchmark816Cover
#check benchmark816WholeGround
#print axioms benchmark816WholeGround
#check benchmark816MinimalForbiddenCounts
#print axioms benchmark816MinimalForbiddenCounts

end UniversalLaw.P15Completion
