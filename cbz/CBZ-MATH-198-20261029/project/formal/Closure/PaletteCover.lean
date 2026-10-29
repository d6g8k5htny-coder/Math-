import Specifications.P15

namespace UniversalLaw.P15Closure
open UniversalLaw.Spec.P15

/-- Distribute a finite set among a palette with uniform capacity. -/
theorem exists_capacity_coloring {X : Type} [Fintype X] [DecidableEq X]
    (S : Finset X) {K a : ℕ} (P : Finset (Fin K)) (h : S.card ≤ a * P.card) :
    ∃ f : S → Fin K, (∀ x, f x ∈ P) ∧
      ∀ j, (Finset.univ.filter (fun x : S => f x = j)).card ≤ a := by
  classical
  have hc : Fintype.card S ≤ Fintype.card (Fin a × P) := by simpa using h
  obtain ⟨e⟩ := Function.Embedding.nonempty_of_card_le hc
  let f : S → Fin K := fun x => (e x).2.val
  refine ⟨f, fun x => (e x).2.property, ?_⟩
  intro j
  have hj : Function.Injective (fun x : {x : S // f x = j} => (e x.val).1) := by
    intro x y hxy
    apply Subtype.ext
    apply e.injective
    apply Prod.ext hxy
    apply Subtype.ext
    exact x.property.trans y.property.symm
  have hcard := Fintype.card_le_of_injective _ hj
  simpa only [Fintype.card_subtype, Fintype.card_fin] using hcard

/-- A feasible palette decomposes every set whose local sizes meet the capacity budget. -/
theorem decomposable_of_palette {X : Type} [Fintype X] [DecidableEq X]
    (F : RealizedData X) {K : ℕ} (hP : IsPaletteFeasible F.b F.H F.d K)
    (U : Finset X) (hU : ∀ i, (U ∩ block F i).card ≤ F.a i * F.d i) :
    IsKDecomposable F K U := by
  classical
  obtain ⟨P, hPd, hPe⟩ := hP
  have hf : ∀ i : Fin F.b, ∃ f : ↥(U ∩ block F i) → Fin K,
      (∀ x, f x ∈ P i) ∧
      ∀ j, (Finset.univ.filter (fun x : ↥(U ∩ block F i) => f x = j)).card ≤ F.a i := by
    intro i
    apply exists_capacity_coloring
    exact (hU i).trans (Nat.mul_le_mul_left _ (hPd i))
  choose f hfP hfcap using hf
  let localPoint (x : U) : ↥(U ∩ block F (F.blk x.val)) :=
    ⟨x.val, Finset.mem_inter.mpr ⟨x.property, by simp [block]⟩⟩
  let color (x : U) : Fin K := f (F.blk x.val) (localPoint x)
  have hcolor (x : U) (i : Fin F.b) (hxi : F.blk x.val = i)
      (hx : x.val ∈ U ∩ block F i) : color x = f i ⟨x.val,hx⟩ := by
    cases hxi
    rfl
  let parts (j : Fin K) : Finset X :=
    (U.attach.filter (fun x => color x = j)).image Subtype.val
  have hmem (x : X) (j : Fin K) : x ∈ parts j ↔ ∃ hx : x ∈ U, color ⟨x,hx⟩ = j := by
    simp only [parts, Finset.mem_image, Finset.mem_filter, Finset.mem_attach, true_and]
    constructor
    · rintro ⟨y, hy, rfl⟩
      exact ⟨y.property, hy⟩
    · rintro ⟨hx, hj⟩
      exact ⟨⟨x,hx⟩, hj, rfl⟩
  refine ⟨parts, ?_, ?_, ?_⟩
  · intro j
    constructor
    · intro i
      let emb : ↥(parts j ∩ block F i) → {x : ↥(U ∩ block F i) // f i x = j} := fun x => by
        let hxU : x.val ∈ U := ((hmem x.val j).mp (Finset.mem_inter.mp x.property).1).choose
        have hxj : color ⟨x.val,hxU⟩ = j := ((hmem x.val j).mp (Finset.mem_inter.mp x.property).1).choose_spec
        have hxi : F.blk x.val = i := by
          simpa [block] using (Finset.mem_inter.mp x.property).2
        refine ⟨⟨x.val, Finset.mem_inter.mpr ⟨hxU, (Finset.mem_inter.mp x.property).2⟩⟩, ?_⟩
        exact (hcolor ⟨x.val,hxU⟩ i hxi _).symm.trans hxj
      have hinj : Function.Injective emb := by
        intro x y hxy
        apply Subtype.ext
        simpa only [emb] using congrArg (fun z => z.val.val) hxy
      have hc := Fintype.card_le_of_injective emb hinj
      have hc' : (parts j ∩ block F i).card ≤
          (Finset.univ.filter (fun x : ↥(U ∩ block F i) => f i x = j)).card := by
        rw [Fintype.card_coe, Fintype.card_subtype] at hc
        exact hc
      exact hc'.trans (hfcap i j)
    · intro e he hes
      obtain ⟨i, hie, hij⟩ := hPe e he j
      have hi : i ∈ supp F (parts j) := hes hie
      obtain ⟨x, hx, hxi⟩ := Finset.mem_image.mp hi
      obtain ⟨hxU,hxj⟩ := (hmem x j).mp hx
      have hp := hfP (F.blk x) (localPoint ⟨x,hxU⟩)
      change color ⟨x,hxU⟩ ∈ P (F.blk x) at hp
      rw [hxj, hxi] at hp
      exact hij hp
  · intro j j' hjj'
    apply Finset.disjoint_left.mpr
    intro x hx hx'
    obtain ⟨hxU,hxj⟩ := (hmem x j).mp hx
    obtain ⟨hxU',hxj'⟩ := (hmem x j').mp hx'
    exact hjj' (hxj.symm.trans hxj')
  · ext x
    simp only [Finset.mem_biUnion, Finset.mem_univ, true_and]
    constructor
    · rintro ⟨j,hj⟩
      exact ((hmem x j).mp hj).choose
    · intro hx
      exact ⟨color ⟨x,hx⟩, (hmem x _).mpr ⟨hx,rfl⟩⟩

/-- The full-block generators cover at every feasible palette size. -/
theorem fullBlockCover_of_palette_feasible {X : Type} [Fintype X] [DecidableEq X]
    (F : RealizedData X) (hF : IsRealizedFamily F) {K : ℕ}
    (hP : IsPaletteFeasible F.b F.H F.d K) :
    IsGeneratorCover F K (fullBlockFamily F) := by
  classical
  intro U hU
  by_contra hcover
  have hmiss : ∀ i, ¬ block F i ⊆ U := by
    intro i hi
    exact hcover ⟨block F i, Finset.mem_image.mpr ⟨i, Finset.mem_univ i, rfl⟩, hi⟩
  apply hU
  apply decomposable_of_palette F hP U
  intro i
  have hsub : U ∩ block F i ⊂ block F i := by
    refine Finset.ssubset_iff_subset_ne.mpr ⟨Finset.inter_subset_right, ?_⟩
    intro heq
    exact hmiss i (heq ▸ Finset.inter_subset_left)
  have hc := Finset.card_lt_card hsub
  rw [hF.2.2.1 i] at hc
  omega

/-- Disjoint block palettes always provide a finite feasible label universe. -/
theorem palette_feasible_nonempty (b : ℕ) (H : Finset (Finset (Fin b)))
    (d : Fin b → ℕ) (hH : ∀ e ∈ H, 2 ≤ e.card) :
    ∃ K, IsPaletteFeasible b H d K := by
  classical
  let S := Sigma (fun i : Fin b => Fin (d i))
  let E := Fintype.equivFin S
  let P : Fin b → Finset (Fin (Fintype.card S)) :=
    fun i => Finset.univ.image (fun j : Fin (d i) => E ⟨i,j⟩)
  refine ⟨Fintype.card S, P, ?_, ?_⟩
  · intro i
    have hInj : Function.Injective (fun j : Fin (d i) => E ⟨i,j⟩) := by
      intro j k h
      have h' := E.injective h
      cases h'
      rfl
    simp only [P, Finset.card_image_of_injective _ hInj, Finset.card_univ, Fintype.card_fin]
    exact le_rfl
  · intro e he l
    obtain ⟨i,hi,j,hj,hij⟩ := Finset.one_lt_card.mp (hH e he)
    by_contra hn
    push Not at hn
    obtain ⟨u,hu,heu⟩ := Finset.mem_image.mp (hn i hi)
    obtain ⟨v,hv,hev⟩ := Finset.mem_image.mp (hn j hj)
    exact hij (congrArg Sigma.fst (E.injective (heu.trans hev.symm)))

/-- Enlarge the label universe, assuming each forbidden edge is nonempty. -/
theorem palette_feasible_mono {b K L : ℕ} {H : Finset (Finset (Fin b))}
    {d : Fin b → ℕ} (hH : ∀ e ∈ H, e.Nonempty) (hKL : K ≤ L)
    (h : IsPaletteFeasible b H d K) : IsPaletteFeasible b H d L := by
  classical
  obtain ⟨P,hP,hE⟩ := h
  let f := Fin.castLEEmb hKL
  refine ⟨fun i => (P i).map f, ?_, ?_⟩
  · intro i
    simpa using hP i
  · intro e he l
    by_cases hl : ∃ k : Fin K, f k = l
    · obtain ⟨k,hk⟩ := hl
      obtain ⟨i,hi,hik⟩ := hE e he k
      refine ⟨i,hi,?_⟩
      intro hm
      obtain ⟨m,hm,hml⟩ := Finset.mem_map.mp hm
      have hmk : m = k := f.injective (hml.trans hk.symm)
      exact hik (hmk ▸ hm)
    · obtain ⟨i,hi⟩ := hH e he
      refine ⟨i,hi,?_⟩
      intro hm
      obtain ⟨m,hm,hml⟩ := Finset.mem_map.mp hm
      exact hl ⟨m,hml⟩

/-- The palette infimum is attained under the realized-family hypotheses. -/
theorem paletteNumberAttained {X : Type} [Fintype X] (F : RealizedData X) :
    PaletteNumberAttained F := by
  intro hF
  exact Nat.sInf_mem (palette_feasible_nonempty F.b F.H F.d hF.2.2.2.1)

/-- Every palette size at or above the palette number is feasible. -/
theorem palette_feasible_of_number_le {X : Type} [Fintype X]
    (F : RealizedData X) (hF : IsRealizedFamily F) {K : ℕ}
    (hK : paletteNumber F.b F.H F.d ≤ K) : IsPaletteFeasible F.b F.H F.d K := by
  exact palette_feasible_mono (fun e he =>
    Finset.card_pos.mp (by have := hF.2.2.2.1 e he; omega)) hK (paletteNumberAttained F hF)

/-- Sufficiency in the exact full-block cover criterion, with every endpoint allowed. -/
theorem fullBlockCover_of_paletteNumber_le {X : Type} [Fintype X] [DecidableEq X]
    (F : RealizedData X) (hF : IsRealizedFamily F) {K : ℕ}
    (hK : paletteNumber F.b F.H F.d ≤ K) :
    IsGeneratorCover F K (fullBlockFamily F) :=
  fullBlockCover_of_palette_feasible F hF (palette_feasible_of_number_le F hF hK)

/-- A decomposition occupying a local capacity-demand product induces feasible palettes. -/
theorem palette_feasible_of_decomposable {X : Type} [Fintype X] [DecidableEq X]
    (F : RealizedData X) (ha : ∀ i, 1 ≤ F.a i) {K : ℕ} (U : Finset X)
    (hsize : ∀ i, F.a i * F.d i ≤ (U ∩ block F i).card)
    (hdec : IsKDecomposable F K U) : IsPaletteFeasible F.b F.H F.d K := by
  classical
  obtain ⟨parts,hgood,hdisj,hunion⟩ := hdec
  let P : Fin F.b → Finset (Fin K) :=
    fun i => Finset.univ.filter (fun j => (parts j ∩ block F i).Nonempty)
  have hmem (i : Fin F.b) (j : Fin K) : j ∈ P i ↔ i ∈ supp F (parts j) := by
    simp only [P, Finset.mem_filter, Finset.mem_univ, true_and, supp, Finset.mem_image]
    constructor
    · rintro ⟨x,hx⟩
      exact ⟨x, (Finset.mem_inter.mp hx).1, by simpa [block] using (Finset.mem_inter.mp hx).2⟩
    · rintro ⟨x,hx,hxi⟩
      exact ⟨x, Finset.mem_inter.mpr ⟨hx, by simp [block,hxi]⟩⟩
  refine ⟨P, ?_, ?_⟩
  · intro i
    have hsub : U ∩ block F i ⊆ (P i).biUnion (fun j => parts j ∩ block F i) := by
      intro x hx
      have hxU : x ∈ (Finset.univ : Finset (Fin K)).biUnion parts :=
        hunion.symm ▸ (Finset.mem_inter.mp hx).1
      obtain ⟨j,hj,hxj⟩ := Finset.mem_biUnion.mp hxU
      have hxi : x ∈ parts j ∩ block F i :=
        Finset.mem_inter.mpr ⟨hxj,(Finset.mem_inter.mp hx).2⟩
      have hPj : j ∈ P i := by
        simp only [P, Finset.mem_filter, Finset.mem_univ, true_and]
        exact ⟨x,hxi⟩
      exact Finset.mem_biUnion.mpr ⟨j,hPj,hxi⟩
    have hc : (U ∩ block F i).card ≤ (P i).card * F.a i := by
      calc
        _ ≤ ((P i).biUnion (fun j => parts j ∩ block F i)).card := Finset.card_le_card hsub
        _ ≤ ∑ j ∈ P i, (parts j ∩ block F i).card := Finset.card_biUnion_le
        _ ≤ ∑ j ∈ P i, F.a i := Finset.sum_le_sum (fun j hj => (hgood j).1 i)
        _ = (P i).card * F.a i := by simp
    have := ha i
    have := (hsize i).trans hc
    nlinarith
  · intro e he j
    have hn := (hgood j).2 e he
    change ¬ ∀ i, i ∈ e → i ∈ supp F (parts j) at hn
    push Not at hn
    obtain ⟨i,hie,hi⟩ := hn
    exact ⟨i,hie, fun hip => hi ((hmem i j).mp hip)⟩

/-- Removing one point in every block witnesses necessity of the palette threshold. -/
theorem paletteNumber_le_of_fullBlockCover {X : Type} [Fintype X] [DecidableEq X]
    (F : RealizedData X) (hF : IsRealizedFamily F) {K : ℕ}
    (hcover : IsGeneratorCover F K (fullBlockFamily F)) :
    paletteNumber F.b F.H F.d ≤ K := by
  classical
  have hb : ∀ i, (block F i).Nonempty := by
    intro i
    apply Finset.card_pos.mp
    rw [hF.2.2.1 i]
    omega
  choose excluded hexcluded using hb
  have hexcludedblk (i : Fin F.b) : F.blk (excluded i) = i := by simpa [block] using hexcluded i
  let U : Finset X := Finset.univ.filter (fun x => x ≠ excluded (F.blk x))
  have hlocal (i : Fin F.b) : U ∩ block F i = (block F i).erase (excluded i) := by
    ext x
    simp only [Finset.mem_inter, U, Finset.mem_filter, Finset.mem_univ, true_and,
      Finset.mem_erase, block]
    constructor
    · rintro ⟨hx,hxi⟩
      exact ⟨by simpa only [hxi] using hx,hxi⟩
    · rintro ⟨hx,hxi⟩
      exact ⟨by simpa only [hxi] using hx,hxi⟩
  have hsize (i : Fin F.b) : F.a i * F.d i ≤ (U ∩ block F i).card := by
    rw [hlocal i, Finset.card_erase_of_mem (hexcluded i), hF.2.2.1 i]
    omega
  have hdec : IsKDecomposable F K U := by
    by_contra hn
    obtain ⟨g,hg,hgU⟩ := hcover U hn
    obtain ⟨i,hi,rfl⟩ := Finset.mem_image.mp hg
    have hu := hgU (hexcluded i)
    have hne : excluded i ≠ excluded (F.blk (excluded i)) := (Finset.mem_filter.mp hu).2
    exact hne (by rw [hexcludedblk i])
  exact Nat.sInf_le (palette_feasible_of_decomposable F hF.1 U hsize hdec)

/-- Exact full-block cover criterion, with the original specification type. -/
theorem fullBlockCoverIff {X : Type} [Fintype X] [DecidableEq X]
    (F : RealizedData X) : FullBlockCoverIff F := by
  intro hF K
  exact ⟨paletteNumber_le_of_fullBlockCover F hF, fullBlockCover_of_paletteNumber_le F hF⟩

#check paletteNumberAttained
#print axioms paletteNumberAttained
#check fullBlockCover_of_paletteNumber_le
#print axioms fullBlockCover_of_paletteNumber_le
#check fullBlockCoverIff
#print axioms fullBlockCoverIff
#check exists_capacity_coloring
#print axioms exists_capacity_coloring
#check decomposable_of_palette
#print axioms decomposable_of_palette
#check fullBlockCover_of_palette_feasible
#print axioms fullBlockCover_of_palette_feasible
end UniversalLaw.P15Closure
