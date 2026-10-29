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

/-- Integrating an actual restriction event on the ambient product space cancels
the outside-coordinate factors exactly. This identity needs no downset premise. -/
theorem restrictionMass_eq_ambient (D : Finset (Finset X)) (p : X → ℝ) (g : Finset X) :
    restrictionMass D p g =
      ∑ U : Finset X, if U ∩ g ∈ D then weight p U else 0 := by
  classical
  let blk : X → Fin 2 := fun v => if v ∈ g then 0 else 1
  have hb0 : block blk 0 = g := by
    ext v
    by_cases hv : v ∈ g <;> simp [block, blk, hv]
  have hb1 : block blk 1 = gᶜ := by
    ext v
    by_cases hv : v ∈ g <;> simp [block, blk, hv]
  let f : Fin 2 → Finset X → ℝ := fun i S =>
    if i = 0 then (if S ∈ D then P15Closure.blockWeight p g S else 0)
    else P15Closure.blockWeight p gᶜ S
  have hone : (1 : Fin 2) ≠ 0 := by decide
  have hweight (U : Finset X) : weight p U =
      P15Closure.blockWeight p g (U ∩ g) * P15Closure.blockWeight p gᶜ (U ∩ gᶜ) := by
    simpa only [Fin.prod_univ_two, hb0, hb1] using weight_eq_prod_blockWeight blk p U
  symm
  calc
    _ = ∑ U : Finset X, ∏ i : Fin 2, f i (U ∩ block blk i) := by
      apply Finset.sum_congr rfl
      intro U hU
      rw [Fin.prod_univ_two]
      simp only [f, hb0, hb1, ite_true, hone, ite_false]
      by_cases hgood : U ∩ g ∈ D
      · simp only [hgood, ite_true]
        exact hweight U
      · simp only [hgood, ite_false, zero_mul]
    _ = ∏ i : Fin 2, ∑ S ∈ (block blk i).powerset, f i S := sum_block_functions blk f
    _ = restrictionMass D p g := by
      rw [Fin.prod_univ_two]
      simp only [f, hb0, hb1, ite_true, hone, ite_false]
      rw [P15Closure.sum_blockWeight, mul_one]
      rfl

/-- Actual restriction, enumerated on a standard finite ground type. -/
noncomputable def reindexedRestriction {n : ℕ} (D : Finset (Finset X))
    (e : Fin n ↪ X) : Finset (Finset (Fin n)) :=
  Finset.univ.powerset.filter (fun S => S.map e ∈ D)

omit [Fintype X] in
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

omit [Fintype X] in
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

omit [Fintype X] [DecidableEq X] in
theorem genPrice_reindex (c : X → ℝ) (g : Finset X) (n : ℕ)
    (e : Fin n ↪ X) (he : Finset.univ.map e = g) :
    genPrice c g = ∏ j : Fin n, c (e j) := by
  rw [← he]
  simp only [genPrice, Finset.prod_map]

omit [Fintype X] in
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

omit [Fintype X] in
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

omit [Fintype X] in
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

/-- Positive global mass implies positive mass on every actual restriction,
including overlapping restrictions. This uses a two-block partition for each
single restriction and makes no independence claim between witnesses. -/
theorem restrictionMass_pos_of_muOf_pos (D : Finset (Finset X)) (hD : decreasing D)
    (p : X → ℝ) (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1)
    (hmu : 0 < muOf D p) (g : Finset X) : 0 < restrictionMass D p g := by
  classical
  let blk : X → Fin 2 := fun v => if v ∈ g then 0 else 1
  have hb : block blk 0 = g := by
    ext v
    by_cases hv : v ∈ g <;> simp [block, blk, hv]
  simpa only [localMass, hb, restrictionMass] using
    localMass_pos_of_muOf_pos D hD blk p hp hmu 0

/-- Interpolation prices a finite witness family by the sum of its actual
hazard ratios. The separate coverage and weighted-hazard obligations are not
asserted here. -/
theorem famPrice_le_sum_restriction_hazard_ratios (D : Finset (Finset X))
    (hD : decreasing D) (G : Finset (Finset X))
    (hnonempty : ∀ g ∈ G, g.Nonempty) (hbad : ∀ g ∈ G, g ∉ D)
    (p c : X → ℝ) (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1)
    (hc : ∀ v, 0 ≤ c v ∧ c v ≤ phi (p v)) (hmu : 0 < muOf D p) :
    famPrice c G ≤ ∑ g ∈ G,
      (-Real.log (restrictionMass D p g)) / restrictionHazardStar D g := by
  apply Finset.sum_le_sum
  intro g hg
  exact restriction_genPrice_le_hazard_ratio D hD g (hnonempty g hg) (hbad g hg)
    p c hp hc (restrictionMass_pos_of_muOf_pos D hD p hp hmu g)

/-- Taking logarithms of a weighted product bound supplies the exact witness-load
hazard sum. Positivity is derived from global positive mass and actual restrictions. -/
theorem weightedHazard_of_productBound (D : Finset (Finset X)) (hD : decreasing D)
    (G : Finset (Finset X)) (hnonempty : ∀ g ∈ G, g.Nonempty)
    (hbad : ∀ g ∈ G, g ∉ D) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) (L : ℝ) (hL : 0 < L)
    (hmu : 0 < muOf D p)
    (hprod : muOf D p ≤ ∏ g ∈ G,
      (restrictionMass D p g) ^ (1 / (L * restrictionHazardStar D g))) :
    (∑ g ∈ G, (-Real.log (restrictionMass D p g)) / restrictionHazardStar D g) ≤
      L * (-Real.log (muOf D p)) := by
  have hM : ∀ g ∈ G, 0 < restrictionMass D p g :=
    fun g _ => restrictionMass_pos_of_muOf_pos D hD p hp hmu g
  have hH : ∀ g ∈ G, 0 < restrictionHazardStar D g :=
    fun g hg => restrictionHazardStar_pos D hD g (hnonempty g hg) (hbad g hg)
  have hlogprod : Real.log (∏ g ∈ G,
      (restrictionMass D p g) ^ (1 / (L * restrictionHazardStar D g))) =
      ∑ g ∈ G, (1 / (L * restrictionHazardStar D g)) * Real.log (restrictionMass D p g) := by
    rw [Real.log_prod (fun g hg => (Real.rpow_pos_of_pos (hM g hg) _).ne')]
    exact Finset.sum_congr rfl (fun g hg => Real.log_rpow (hM g hg) _)
  have hlog := Real.log_le_log hmu hprod
  rw [hlogprod] at hlog
  have hidentity : (∑ g ∈ G,
      (-Real.log (restrictionMass D p g)) / restrictionHazardStar D g) =
      L * (-(∑ g ∈ G,
        (1 / (L * restrictionHazardStar D g)) * Real.log (restrictionMass D p g))) := by
    rw [← Finset.sum_neg_distrib, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro g hg
    field_simp [hL.ne', (hH g hg).ne']
  rw [hidentity]
  exact mul_le_mul_of_nonneg_left (neg_le_neg hlog) hL.le

/-- Conditional witness-load assembly. The weighted-hazard bound remains an
explicit premise until discharged by a product-space inequality such as Finner.
The zero-global-mass branch uses the price-one empty-generator cover. -/
theorem witnessLoad_budget_of_weightedHazard (D : Finset (Finset X))
    (hD : decreasing D) (K : ℕ) (G : Finset (Finset X))
    (hG : generatorCover D K G)
    (hnonempty : ∀ g ∈ G, g.Nonempty) (hbad : ∀ g ∈ G, g ∉ D)
    (p c : X → ℝ) (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1)
    (hc : ∀ v, 0 ≤ c v ∧ c v ≤ phi (p v)) (L : ℝ)
    (hweighted : 0 < muOf D p →
      (∑ g ∈ G, (-Real.log (restrictionMass D p g)) / restrictionHazardStar D g) ≤
        L * (-Real.log (muOf D p))) :
    (0 < muOf D p → famPrice c G ≤ L * (-Real.log (muOf D p))) ∧
    (∃ H : Finset (Finset X), generatorCover D K H ∧
      famPrice c H ≤ cappedHazard L (muOf D p)) ∧
    coverCost D K c ≤ cappedHazard L (muOf D p) := by
  classical
  have hbudget : 0 < muOf D p → famPrice c G ≤ L * (-Real.log (muOf D p)) := by
    intro hmu
    exact (famPrice_le_sum_restriction_hazard_ratios D hD G hnonempty hbad p c hp hc hmu).trans
      (hweighted hmu)
  have hex : ∃ H : Finset (Finset X), generatorCover D K H ∧
      famPrice c H ≤ cappedHazard L (muOf D p) := by
    by_cases hmu : 0 < muOf D p
    · rw [cappedHazard, ite_eq_left hmu]
      by_cases hh : L * (-Real.log (muOf D p)) < 1
      · exact ⟨G, hG, (hbudget hmu).trans (le_of_eq (min_eq_right hh.le).symm)⟩
      · refine ⟨{∅}, emptyGenerator_cover D K, ?_⟩
        simp only [famPrice, Finset.sum_singleton, genPrice, Finset.prod_empty]
        rw [min_eq_left (le_of_not_gt hh)]
    · refine ⟨{∅}, emptyGenerator_cover D K, ?_⟩
      simp [cappedHazard, hmu, famPrice, genPrice]
  refine ⟨hbudget, hex, ?_⟩
  obtain ⟨H, hH, hprice⟩ := hex
  exact (coverCost_le_family D K c (fun v => (hc v).1) H hH).trans hprice

/-- The remaining analytic premise may equivalently be supplied as a weighted
product bound. Coverage remains a separate setwise certificate. -/
theorem witnessLoad_budget_of_productBound (D : Finset (Finset X))
    (hD : decreasing D) (K : ℕ) (G : Finset (Finset X))
    (hG : generatorCover D K G)
    (hnonempty : ∀ g ∈ G, g.Nonempty) (hbad : ∀ g ∈ G, g ∉ D)
    (p c : X → ℝ) (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1)
    (hc : ∀ v, 0 ≤ c v ∧ c v ≤ phi (p v)) (L : ℝ) (hL : 0 < L)
    (hprod : 0 < muOf D p → muOf D p ≤ ∏ g ∈ G,
      (restrictionMass D p g) ^ (1 / (L * restrictionHazardStar D g))) :
    (0 < muOf D p → famPrice c G ≤ L * (-Real.log (muOf D p))) ∧
    (∃ H : Finset (Finset X), generatorCover D K H ∧
      famPrice c H ≤ cappedHazard L (muOf D p)) ∧
    coverCost D K c ≤ cappedHazard L (muOf D p) :=
  witnessLoad_budget_of_weightedHazard D hD K G hG hnonempty hbad p c hp hc L
    (fun hmu => weightedHazard_of_productBound D hD G hnonempty hbad p hp L hL hmu (hprod hmu))

/-- The empty-witness-family branch has price zero whenever it supplies coverage. -/
theorem emptyWitnessFamily_coverCost (D : Finset (Finset X)) (K : ℕ) (c : X → ℝ)
    (hc : ∀ v, 0 ≤ c v) (hcover : generatorCover D K ∅) : coverCost D K c ≤ 0 := by
  simpa only [famPrice, Finset.sum_empty] using coverCost_le_family D K c hc ∅ hcover

end UniversalLaw.General
