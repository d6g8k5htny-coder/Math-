import Closure.ProductMass

namespace UniversalLaw.P15Completion
open UniversalLaw.Spec.P15 UniversalLaw.P15Closure
open scoped BigOperators

variable {X : Type} [Fintype X] [DecidableEq X]

/-- A bad-set witness family yields a probability union bound, without any
independence claim between overlapping witness events. -/
theorem badWitness_union_bound (F : RealizedData X) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) (G : Finset (Finset X))
    (hG : ∀ U : Finset X, ¬ IsGood F U → ∃ g ∈ G, g ⊆ U) :
    1 - mu F p ≤ famPrice p G := by
  classical
  rw [← UniversalLaw.Proofs.P15Elementary.Aux.sum_weight_eq_one p]
  unfold mu
  rw [← Finset.sum_sub_distrib]
  calc
    _ ≤ ∑ U ∈ (Finset.univ : Finset X).powerset,
        ∑ g ∈ G, if g ⊆ U then weight p U else 0 := by
      apply Finset.sum_le_sum
      intro U hU
      have hnonneg : ∀ g ∈ G, 0 ≤ (if g ⊆ U then weight p U else 0) := by
        intro g hg
        split_ifs
        · exact weight_nonneg_mass p hp U
        · exact le_rfl
      by_cases hgood : U ∈ downset F
      · rw [Set.indicator_of_mem hgood, sub_self]
        exact Finset.sum_nonneg hnonneg
      · rw [Set.indicator_of_notMem hgood, sub_zero]
        obtain ⟨g, hg, hgU⟩ := hG U hgood
        have h := Finset.single_le_sum hnonneg hg
        simpa only [hgU, ite_true] using h
    _ = ∑ g ∈ G, ∑ U ∈ (Finset.univ : Finset X).powerset,
        if g ⊆ U then weight p U else 0 := Finset.sum_comm
    _ = famPrice p G := by
      apply Finset.sum_congr rfl
      intro g hg
      have h := cylinder_mass p (Finset.univ : Finset X) g (Finset.subset_univ g)
      rw [Finset.sum_filter] at h
      exact h

/-- Every bad finite set contains an inclusion-minimal bad subset. -/
theorem exists_minimalForbidden_subset (F : RealizedData X) (U : Finset X)
    (hU : ¬ IsGood F U) :
    ∃ g : Finset X, IsMinimalForbidden F g ∧ g ⊆ U := by
  classical
  let P : ℕ → Prop := fun n => ∃ g : Finset X, g ⊆ U ∧ ¬ IsGood F g ∧ g.card = n
  have hex : ∃ n, P n := ⟨U.card, U, Finset.Subset.refl U, hU, rfl⟩
  obtain ⟨g, hgU, hbad, hcard⟩ := Nat.find_spec hex
  refine ⟨g, ⟨hbad, ?_⟩, hgU⟩
  intro v hv
  by_contra herase
  have hmin : Nat.find hex ≤ (g.erase v).card :=
    Nat.find_min' hex ⟨g.erase v, (Finset.erase_subset v g).trans hgU, herase, rfl⟩
  have hstrict : (g.erase v).card < g.card :=
    Finset.card_lt_card (Finset.erase_ssubset hv)
  exact (not_le_of_gt hstrict) (hcard.trans_le hmin)

noncomputable def minimalForbiddenFamily (F : RealizedData X) : Finset (Finset X) := by
  classical
  exact Finset.univ.filter (IsMinimalForbidden F)

theorem minimalForbidden_union_bound (F : RealizedData X) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) :
    1 - mu F p ≤ famPrice p (minimalForbiddenFamily F) := by
  classical
  apply badWitness_union_bound F p hp
  intro U hU
  obtain ⟨g, hg, hgU⟩ := exists_minimalForbidden_subset F U hU
  exact ⟨g, by simp [minimalForbiddenFamily, hg], hgU⟩

end UniversalLaw.P15Completion

#print axioms UniversalLaw.P15Completion.badWitness_union_bound
#print axioms UniversalLaw.P15Completion.exists_minimalForbidden_subset
#print axioms UniversalLaw.P15Completion.minimalForbidden_union_bound
