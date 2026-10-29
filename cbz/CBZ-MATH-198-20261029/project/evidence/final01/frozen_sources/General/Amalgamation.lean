import General.Safety

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
    (hlocal : ∀ i, localGeneratorCover D blk i (k i) (G i)) :
    generatorCover D K (Finset.univ.biUnion G) := by
  classical
  intro U hbad
  by_contra hnone
  have hdec : ∀ i, decomposable (localFamily D blk i) (k i) (U ∩ block blk i) := by
    intro i
    by_contra hn
    obtain ⟨g, hg, hsub⟩ := hlocal i (U ∩ block blk i) Finset.inter_subset_right hn
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
    simp only [label, dite_eq_left hex]
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
        change emb (blk v) (label (blk v) v) = j at hvcolor
        rw [hvi] at hvcolor
        exact hvcolor
      have heq : label i v = t := (emb i).injective (hcolor.trans ht.symm)
      simpa only [heq] using hvlabel
    · have hempty : colorClass U f j ∩ block blk i = ∅ := by
        apply Finset.eq_empty_iff_forall_notMem.mpr
        intro v hv
        obtain ⟨hvclass, hvblock⟩ := Finset.mem_inter.mp hv
        have hvcolor := (Finset.mem_filter.mp hvclass).2
        have hvi : blk v = i := (Finset.mem_filter.mp hvblock).2
        apply hex
        refine ⟨label i v, ?_⟩
        change emb (blk v) (label (blk v) v) = j at hvcolor
        rw [hvi] at hvcolor
        exact hvcolor
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

/-- P15-B B1 for arbitrary finite decreasing families and actual local restrictions.

No coloring of the full blocks is required: avoiding the local covers supplies fresh
local decompositions for the particular set being tested. Positive local demands
also supply default labels off that set, so the proof includes empty ground sets,
empty block index types, and the possible zero global palette.

The generator support hypothesis records the source's local-certificate interface;
the stronger uniform-safety lemma does not need it, since every generator used
there is already a subset of the tested block restriction.
-/
theorem localCover_amalgamation {b K : ℕ}
    (D : Finset (Finset X)) (hD : decreasing D)
    (blk : X → Fin b) (P : Fin b → Finset (Fin K))
    (k : Fin b → ℕ) (hk : ∀ i, 0 < k i)
    (hsize : ∀ i, k i ≤ (P i).card)
    (hPS : paletteSeparated D blk P)
    (G : Fin b → Finset (Finset X))
    (_hgsub : ∀ i g, g ∈ G i → g ⊆ block blk i)
    (hlocal : ∀ i, localGeneratorCover D blk i (k i) (G i)) :
    generatorCover D K (Finset.univ.biUnion G) := by
  exact localCover_amalgamation_of_safety D hD blk P k hk hsize
    ((paletteSafety_iff D hD blk P).mp hPS) G hlocal

namespace LocalGroundRegression

def fullFamily : Finset (Finset (Fin 2)) := Finset.univ.powerset

/-- Both distinct singleton blocks admit genuinely empty local covers. This
instance exercises the block-restricted quantifier in `localGeneratorCover`. -/
theorem twoBlock_emptyLocalCover :
    (0 : Fin 2) ≠ 1 ∧
    block (id : Fin 2 → Fin 2) 0 = {0} ∧
    block (id : Fin 2 → Fin 2) 1 = {1} ∧
    (∀ i : Fin 2, localGeneratorCover fullFamily id i 1 ∅) ∧
    generatorCover fullFamily 1 ∅ ∧
    UniversalLaw.Spec.P15.famPrice (fun _ : Fin 2 => (1 : ℝ)) ∅ = 0 := by
  classical
  have hD : decreasing fullFamily := by
    refine ⟨by simp [fullFamily], ?_⟩
    intro U hU V hVU
    exact Finset.mem_powerset.mpr (Finset.subset_univ V)
  have hlocal : ∀ i : Fin 2, localGeneratorCover fullFamily id i 1 ∅ := by
    intro i U hsub hbad
    exfalso
    apply hbad
    refine ⟨fun _ => U, ?_, ?_, ?_⟩
    · intro j
      exact Finset.mem_filter.mpr
        ⟨Finset.mem_powerset.mpr (Finset.subset_univ U), hsub⟩
    · intro j j' hne
      exact False.elim (hne (Subsingleton.elim j j'))
    · simp
  have hPS : paletteSeparated fullFamily (id : Fin 2 → Fin 2)
      (fun _ => (Finset.univ : Finset (Fin 1))) := by
    intro e he
    exact False.elim (he.1 (Finset.mem_powerset.mpr (Finset.subset_univ e)))
  have hglobal : generatorCover fullFamily 1 ∅ := by
    have h := localCover_amalgamation fullFamily hD (id : Fin 2 → Fin 2)
      (fun _ => (Finset.univ : Finset (Fin 1))) (fun _ => 1)
      (by intro i; decide) (by intro i; simp) hPS (fun _ => ∅)
      (by intro i g hg; exact False.elim (Finset.notMem_empty g hg)) hlocal
    have heq : (Finset.univ : Finset (Fin 2)).biUnion
        (fun _ => (∅ : Finset (Finset (Fin 2)))) = ∅ := by
      apply Finset.eq_empty_iff_forall_notMem.mpr
      intro g hg
      obtain ⟨i, _, hi⟩ := Finset.mem_biUnion.mp hg
      exact Finset.notMem_empty g hi
    rw [heq] at h
    exact h
  refine ⟨by decide, ?_, ?_, hlocal, hglobal, ?_⟩
  · ext v
    simp [block]
  · ext v
    simp [block]
  · simp [UniversalLaw.Spec.P15.famPrice]

/-- The former ambient-ground premise rejects the same valid empty local cover:
the singleton in the other block is an irrelevant ambient obstruction. -/
theorem ambientLocalCover_fails :
    ¬ generatorCover (localFamily fullFamily (id : Fin 2 → Fin 2) 0) 1 ∅ := by
  classical
  intro hcover
  have hbad : ¬ decomposable (localFamily fullFamily (id : Fin 2 → Fin 2) 0) 1 {1} := by
    rintro ⟨parts, hparts, _, hcoverparts⟩
    have hsub : Finset.univ.biUnion parts ⊆ block (id : Fin 2 → Fin 2) 0 := by
      intro v hv
      obtain ⟨j, _, hj⟩ := Finset.mem_biUnion.mp hv
      exact (Finset.mem_filter.mp (hparts j)).2 hj
    have hmem : (1 : Fin 2) ∈ block (id : Fin 2 → Fin 2) 0 := by
      apply hsub
      rw [hcoverparts]
      simp
    simp [block] at hmem
  obtain ⟨g, hg, _⟩ := hcover {1} hbad
  exact Finset.notMem_empty g hg

end LocalGroundRegression

end UniversalLaw.General
