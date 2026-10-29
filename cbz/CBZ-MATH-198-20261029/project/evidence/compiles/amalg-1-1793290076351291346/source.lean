import General.Definitions

namespace UniversalLaw.General

variable {X : Type} [Fintype X] [DecidableEq X]

/-- Local covers can be combined whenever every allowed locally good coloring is safe.
The local decompositions, and hence the coloring, are selected separately for each `U`.
-/
theorem localCover_amalgamation_of_safety {b K : ℕ}
    (D : Finset (Finset X)) (hD : decreasing D)
    (blk : X → Fin b) (P : Fin b → Finset (Fin K))
    (k : Fin b → ℕ) (hk : ∀ i, 0 < k i)
    (hsize : ∀ i, k i ≤ (P i).card)
    (hsafe : ∀ (U : Finset X) (f : X → Fin K),
      allowed blk P U f → locallyGood D blk U f →
      ∀ j, colorClass U f j ∈ D)
    (G : Fin b → Finset (Finset X))
    (hgsub : ∀ i g, g ∈ G i → g ⊆ block blk i)
    (hlocal : ∀ i, generatorCover (localFamily D blk i) (k i) (G i)) :
    generatorCover D K (Finset.univ.biUnion G) := by
  classical
  intro U hbad
  by_contra hnone
  have hdec : ∀ i, decomposable (localFamily D blk i) (k i) (U ∩ block blk i) := by
    intro i
    by_contra hn
    obtain ⟨g, hg, hsub⟩ := hlocal i (U ∩ block blk i) hn
    apply hnone
    exact ⟨g, Finset.mem_biUnion.mpr ⟨i, Finset.mem_univ i, hg⟩,
      hsub.trans Finset.inter_subset_left⟩
  choose parts hparts hdisjoint hcover using hdec
  let label : (i : Fin b) → X → Fin (k i) := fun i v =>
    if h : ∃ t, v ∈ parts i t then Classical.choose h else ⟨0, hk i⟩
  have hlabel : ∀ i v, v ∈ U ∩ block blk i → v ∈ parts i (label i v) := by
    intro i v hv
    have hex : ∃ t, v ∈ parts i t := by
      have hv' : v ∈ Finset.univ.biUnion (parts i) := by rw [hcover i]; exact hv
      obtain ⟨t, _, ht⟩ := Finset.mem_biUnion.mp hv'
      exact ⟨t, ht⟩
    simp only [label, dif_pos hex]
    exact Classical.choose_spec hex
  let emb : (i : Fin b) → Fin (k i) ↪o Fin K :=
    fun i => (P i).orderEmbOfCardLe (hsize i)
  let f : X → Fin K := fun v => emb (blk v) (label (blk v) v)
  have hallowed : allowed blk P U f := by
    intro v _
    exact (P (blk v)).orderEmbOfCardLe_mem (hsize (blk v)) (label (blk v) v)
  have hgood : locallyGood D blk U f := by
    intro j i
    by_cases hex : ∃ t, emb i t = j
    · obtain ⟨t, ht⟩ := hex
      apply hD.2 (parts i t) ((Finset.mem_filter.mp (hparts i t)).1)
      intro v hv
      obtain ⟨hvclass, hvblock⟩ := Finset.mem_inter.mp hv
      obtain ⟨hvU, hvcolor⟩ := Finset.mem_filter.mp hvclass
      have hvi : blk v = i := (Finset.mem_filter.mp hvblock).2
      have hvlabel := hlabel i v (Finset.mem_inter.mpr ⟨hvU, hvblock⟩)
      have hcolor : emb i (label i v) = j := by
        simpa only [f, hvi] using hvcolor
      have heq : label i v = t := (emb i).injective (hcolor.trans ht.symm)
      simpa only [heq] using hvlabel
    · have hempty : colorClass U f j ∩ block blk i = ∅ := by
        apply Finset.eq_empty_iff_forall_not_mem.mpr
        intro v hv
        obtain ⟨hvclass, hvblock⟩ := Finset.mem_inter.mp hv
        have hvcolor := (Finset.mem_filter.mp hvclass).2
        have hvi : blk v = i := (Finset.mem_filter.mp hvblock).2
        apply hex
        exact ⟨label i v, by simpa only [f, hvi] using hvcolor⟩
      rw [hempty]
      exact hD.1
  have hglobal := hsafe U f hallowed hgood
  apply hbad
  refine ⟨colorClass U f, hglobal, ?_, ?_⟩
  · intro j j' hne
    apply Finset.disjoint_left.mpr
    intro v hv hv'
    exact hne ((Finset.mem_filter.mp hv).2.symm.trans (Finset.mem_filter.mp hv').2)
  · apply Finset.ext
    intro v
    constructor
    · intro hv
      obtain ⟨j, _, hj⟩ := Finset.mem_biUnion.mp hv
      exact (Finset.mem_filter.mp hj).1
    · intro hv
      exact Finset.mem_biUnion.mpr ⟨f v, Finset.mem_univ _, Finset.mem_filter.mpr ⟨hv, rfl⟩⟩

end UniversalLaw.General
