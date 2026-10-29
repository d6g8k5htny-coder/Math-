import General.Definitions

namespace UniversalLaw.General

variable {X : Type} [Fintype X] [DecidableEq X]

/-- Every bad finite set contains an inclusion-minimal bad set. -/
theorem exists_minimalBad_subset (D : Finset (Finset X)) (e : Finset X)
    (he : e ∉ D) : ∃ v, v ⊆ e ∧ minimalBad D v := by
  classical
  revert he
  induction e using Finset.strongInductionOn with
  | H e ih =>
    intro he
    by_cases hmin : ∀ v ∈ e, e.erase v ∈ D
    · exact ⟨e, Finset.Subset.refl e, he, hmin⟩
    · push_neg at hmin
      obtain ⟨v, hv, hbad⟩ := hmin
      obtain ⟨w, hw, hwmin⟩ := ih (e.erase v) (Finset.erase_ssubset hv) hbad
      exact ⟨w, hw.trans (Finset.erase_subset v e), hwmin⟩

/-- Minimal bad sets in an empty-admissible family are nonempty. -/
theorem minimalBad_nonempty (D : Finset (Finset X)) (hD : decreasing D)
    (e : Finset X) (he : minimalBad D e) : e.Nonempty := by
  apply Finset.nonempty_iff_ne_empty.mpr
  intro hempty
  exact he.1 (by simpa [hempty] using hD.1)

/-- The erase-based definition implies goodness of every proper subset. -/
theorem proper_subset_good_of_minimal (D : Finset (Finset X))
    (hD : decreasing D) (e : Finset X) (he : minimalBad D e)
    {v : Finset X} (hv : v ⊂ e) : v ∈ D := by
  obtain ⟨a, ha, hsub⟩ := Finset.ssubset_iff_exists_subset_erase.mp hv
  exact hD.2 (e.erase a) (he.2 a ha) v hsub

/-- Every block fragment of a crossing set is a proper subset. -/
theorem crossing_block_inter_ssubset {b : ℕ} (blk : X → Fin b)
    (e : Finset X) (i : Fin b) (hcross : 1 < (e.image blk).card) :
    e ∩ block blk i ⊂ e := by
  classical
  apply Finset.ssubset_iff_subset_ne.mpr
  refine ⟨Finset.inter_subset_left, ?_⟩
  intro heq
  have hsame : ∀ i' ∈ e.image blk, i' = i := by
    intro i' hi'
    obtain ⟨v, hv, rfl⟩ := Finset.mem_image.mp hi'
    have hmem : v ∈ e ∩ block blk i := by rw [heq]; exact hv
    exact (Finset.mem_filter.mp (Finset.mem_inter.mp hmem).2).2
  have hcard : (e.image blk).card ≤ 1 := Finset.card_le_one.mpr
    (fun a ha b hb => (hsame a ha).trans (hsame b hb).symm)
  exact (Nat.not_lt_of_ge hcard) hcross

/-- Exact P15-B B3: palette separation characterizes safety of every
allowed locally good coloring, for every finite subset and every minimal witness. -/
theorem paletteSafety_iff (D : Finset (Finset X)) (hD : decreasing D)
    {b K : ℕ} (blk : X → Fin b) (P : Fin b → Finset (Fin K)) :
    paletteSeparated D blk P ↔
      ∀ (U : Finset X) (f : X → Fin K), allowed blk P U f →
        locallyGood D blk U f → ∀ j, colorClass U f j ∈ D := by
  classical
  constructor
  · intro hsep U f hallowed hlocal j
    by_contra hbad
    obtain ⟨e, hesub, hemin⟩ := exists_minimalBad_subset D (colorClass U f j) hbad
    by_cases hcross : 1 < (e.image blk).card
    · obtain ⟨i, hi, hnot⟩ := hsep e hemin hcross j
      obtain ⟨v, hv, hvblk⟩ := Finset.mem_image.mp hi
      have hvc := Finset.mem_filter.mp (hesub hv)
      have hp := hallowed v hvc.1
      exact hnot (by simpa [hvc.2, hvblk] using hp)
    · obtain ⟨v, hv⟩ := minimalBad_nonempty D hD e hemin
      have hcard : (e.image blk).card ≤ 1 := Nat.le_of_not_gt hcross
      have hsub : e ⊆ colorClass U f j ∩ block blk (blk v) := by
        intro w hw
        refine Finset.mem_inter.mpr ⟨hesub hw, ?_⟩
        have heq : blk w = blk v := Finset.card_le_one.mp hcard
          (blk w) (Finset.mem_image.mpr ⟨w, hw, rfl⟩)
          (blk v) (Finset.mem_image.mpr ⟨v, hv, rfl⟩)
        exact Finset.mem_filter.mpr ⟨Finset.mem_univ w, heq⟩
      exact hemin.1 (hD.2 _ (hlocal j (blk v)) e hsub)
  · intro hsafe e hemin hcross j
    by_contra hnot
    push_neg at hnot
    have hallowed : allowed blk P e (fun _ => j) := by
      intro v hv
      exact hnot (blk v) (Finset.mem_image.mpr ⟨v, hv, rfl⟩)
    have hlocal : locallyGood D blk e (fun _ => j) := by
      intro j' i
      by_cases hcolor : j = j'
      · have hclass : colorClass e (fun _ => j) j' = e := by
          simp [colorClass, hcolor]
        rw [hclass]
        exact proper_subset_good_of_minimal D hD e hemin
          (crossing_block_inter_ssubset blk e i hcross)
      · simpa [colorClass, hcolor] using hD.1
    have hgood := hsafe e (fun _ => j) hallowed hlocal j
    exact hemin.1 (by simpa [colorClass] using hgood)

end UniversalLaw.General
