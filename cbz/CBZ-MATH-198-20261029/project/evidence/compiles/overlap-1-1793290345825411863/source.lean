import General.Probability
import Closure.LocalRatio
import Closure.HazardInterpolation

namespace UniversalLaw.General

open UniversalLaw.Spec.P15
open scoped BigOperators

variable {X : Type} [Fintype X] [DecidableEq X]

/-- Probability of the actual restriction to `g`, with no outside-coordinate factors. -/
noncomputable def restrictionMass (D : Finset (Finset X)) (p : X → ℝ)
    (g : Finset X) : ℝ :=
  ∑ S ∈ g.powerset, if S ∈ D then P15Closure.blockWeight p g S else 0

/-- Reference hazard of the actual restriction to a witness. -/
noncomputable def restrictionHazardStar (D : Finset (Finset X)) (g : Finset X) : ℝ :=
  -Real.log (restrictionMass D (fun _ => pStar) g)

/-- Actual restriction, enumerated on a standard finite ground type. -/
noncomputable def reindexedRestriction {n : ℕ} (D : Finset (Finset X))
    (e : Fin n ↪ X) : Finset (Finset (Fin n)) :=
  Finset.univ.powerset.filter (fun S => S.map e ∈ D)

theorem restrictionMass_reindex (D : Finset (Finset X)) (p : X → ℝ)
    (g : Finset X) (n : ℕ) (e : Fin n ↪ X) (he : Finset.univ.map e = g) :
    restrictionMass D p g = muOf (reindexedRestriction D e) (fun j => p (e j)) := by
  classical
  have hsets : g.powerset =
      (Finset.univ : Finset (Fin n)).powerset.image (fun S => S.map e) := by
    rw [← he]
    simp only [Finset.map_eq_image, Finset.powerset_image]
  unfold restrictionMass muOf reindexedRestriction
  rw [hsets, Finset.sum_image]
  · rw [Finset.sum_filter]
    apply Finset.sum_congr rfl
    intro S hS
    by_cases hgood : S.map e ∈ D
    · simp only [hgood, ite_true]
      rw [← he]
      exact P15Closure.blockWeight_map n e p S
    · simp only [hgood, ite_false]
  · exact fun S _ T _ h => Finset.map_injective e h

theorem reindexedRestriction_isProper (D : Finset (Finset X)) (hD : decreasing D)
    (g : Finset X) (hbad : g ∉ D) (n : ℕ) (e : Fin n ↪ X)
    (he : Finset.univ.map e = g) : IsProperDownset (reindexedRestriction D e) := by
  classical
  refine ⟨?_, ?_, ?_⟩
  · simp [reindexedRestriction, hD.1]
  · simpa [reindexedRestriction, he] using hbad
  · intro U hU V hVU
    exact Finset.mem_filter.mpr ⟨Finset.mem_powerset.mpr (Finset.subset_univ _),
      hD.2 _ (Finset.mem_filter.mp hU).2 _ (Finset.map_subset_map.mpr hVU)⟩

theorem genPrice_reindex (c : X → ℝ) (g : Finset X) (n : ℕ)
    (e : Fin n ↪ X) (he : Finset.univ.map e = g) :
    genPrice c g = ∏ j : Fin n, c (e j) := by
  rw [← he]
  simp only [genPrice, Finset.prod_map]
  rfl

/-- Every nonempty forbidden witness has strictly positive actual reference hazard. -/
theorem restrictionHazardStar_pos (D : Finset (Finset X)) (hD : decreasing D)
    (g : Finset X) (hg : g.Nonempty) (hbad : g ∉ D) :
    0 < restrictionHazardStar D g := by
  classical
  obtain ⟨e, he⟩ := P15Closure.exists_block_embedding g
  have hproper := reindexedRestriction_isProper D hD g hbad g.card e he
  have hn : 1 ≤ g.card := Nat.succ_le_iff.mpr (Finset.card_pos.mpr hg)
  have h := UniversalLaw.Proofs.P15Elementary.hazardStarPositive g.card
    (reindexedRestriction D e) hn hproper
  simpa only [restrictionHazardStar, hazardStar,
    restrictionMass_reindex D (fun _ => pStar) g g.card e he] using h

/-- Full-ground interpolation applies to every actual finite witness restriction.
The cap also handles zero local mass; no capacity-family premise occurs. -/
theorem restriction_fullGroundPriceBound (D : Finset (Finset X)) (hD : decreasing D)
    (g : Finset X) (hg : g.Nonempty) (hbad : g ∉ D) (p c : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1)
    (hc : ∀ v, 0 ≤ c v ∧ c v ≤ phi (p v)) :
    genPrice c g ≤ cappedHazard (1 / restrictionHazardStar D g) (restrictionMass D p g) := by
  classical
  obtain ⟨e, he⟩ := P15Closure.exists_block_embedding g
  have hproper := reindexedRestriction_isProper D hD g hbad g.card e he
  have hn : 1 ≤ g.card := Nat.succ_le_iff.mpr (Finset.card_pos.mpr hg)
  have h := P15Closure.fullGroundPriceBound g.card (reindexedRestriction D e) hn hproper
    (fun j => p (e j)) (fun j => c (e j)) (fun j => hp (e j)) (fun j => hc (e j))
  simpa only [genPrice_reindex c g g.card e he, restrictionHazardStar, hazardStar,
    restrictionMass_reindex D p g g.card e he,
    restrictionMass_reindex D (fun _ => pStar) g g.card e he] using h

/-- Positive-mass witness ratio used in the witness-load assembly. -/
theorem restriction_genPrice_le_hazard_ratio (D : Finset (Finset X)) (hD : decreasing D)
    (g : Finset X) (hg : g.Nonempty) (hbad : g ∉ D) (p c : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1)
    (hc : ∀ v, 0 ≤ c v ∧ c v ≤ phi (p v))
    (hmass : 0 < restrictionMass D p g) :
    genPrice c g ≤ (-Real.log (restrictionMass D p g)) / restrictionHazardStar D g := by
  have h := restriction_fullGroundPriceBound D hD g hg hbad p c hp hc
  rw [cappedHazard, ite_eq_left hmass] at h
  exact (h.trans (min_le_right _ _)).trans_eq (by ring)

end UniversalLaw.General
