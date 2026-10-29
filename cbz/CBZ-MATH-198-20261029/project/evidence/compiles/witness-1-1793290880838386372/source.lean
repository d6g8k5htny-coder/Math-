import General.BernoulliFinner

namespace UniversalLaw.General

open UniversalLaw.Spec.P15
open scoped BigOperators

variable {X : Type} [Fintype X] [DecidableEq X]

/-- Reciprocal reference hazards charged to one original coordinate. -/
noncomputable def witnessCoordinateLoad (D G : Finset (Finset X)) (v : X) : ℝ :=
  ∑ g ∈ G, if v ∈ g then 1 / restrictionHazardStar D g else 0

/-- The finite maximum incident load, including zero for the empty-ground case. -/
noncomputable def maximumWitnessLoad (D G : Finset (Finset X)) : ℝ :=
  (insert 0 ((Finset.univ : Finset X).image (witnessCoordinateLoad D G))).max'
    (Finset.insert_nonempty _ _)

theorem witnessCoordinateLoad_le_maximum (D G : Finset (Finset X)) (v : X) :
    witnessCoordinateLoad D G v ≤ maximumWitnessLoad D G := by
  apply Finset.le_max'
  exact Finset.mem_insert_of_mem (Finset.mem_image.mpr ⟨v, Finset.mem_univ v, rfl⟩)

theorem maximumWitnessLoad_pos (D : Finset (Finset X)) (hD : decreasing D)
    (G : Finset (Finset X)) (hG : G.Nonempty)
    (hnonempty : ∀ g ∈ G, g.Nonempty) (hbad : ∀ g ∈ G, g ∉ D) :
    0 < maximumWitnessLoad D G := by
  classical
  obtain ⟨g, hg⟩ := hG
  obtain ⟨v, hv⟩ := hnonempty g hg
  have hterm : 0 < 1 / restrictionHazardStar D g :=
    one_div_pos.mpr (restrictionHazardStar_pos D hD g (hnonempty g hg) (hbad g hg))
  have hsingle : 1 / restrictionHazardStar D g ≤ witnessCoordinateLoad D G v := by
    have h := Finset.single_le_sum (f := fun t =>
      if v ∈ t then 1 / restrictionHazardStar D t else 0) (s := G) ?_ hg
    · simpa only [hv, ite_true] using h
    · intro t ht
      split_ifs
      · exact (one_div_pos.mpr
          (restrictionHazardStar_pos D hD t (hnonempty t ht) (hbad t ht))).le
      · exact le_rfl
  exact hterm.trans_le (hsingle.trans (witnessCoordinateLoad_le_maximum D G v))

/-- For a nonempty valid witness family, the maximum is attained at a coordinate. -/
theorem maximumWitnessLoad_attained (D : Finset (Finset X)) (hD : decreasing D)
    (G : Finset (Finset X)) (hG : G.Nonempty)
    (hnonempty : ∀ g ∈ G, g.Nonempty) (hbad : ∀ g ∈ G, g ∉ D) :
    ∃ v, witnessCoordinateLoad D G v = maximumWitnessLoad D G := by
  classical
  have hpos := maximumWitnessLoad_pos D hD G hG hnonempty hbad
  have hmem : maximumWitnessLoad D G ∈
      insert 0 ((Finset.univ : Finset X).image (witnessCoordinateLoad D G)) :=
    Finset.max'_mem _ _
  rcases Finset.mem_insert.mp hmem with hzero | himage
  · exact False.elim (hpos.ne' hzero)
  · obtain ⟨v, _, hv⟩ := Finset.mem_image.mp himage
    exact ⟨v, hv⟩

omit [Fintype X] in
/-- Divide an incident reciprocal-hazard load by its positive budget. -/
theorem normalize_incident_load {I : Type} [Fintype I]
    (S : I → Finset X) (H : I → ℝ) (L : ℝ) (hL : 0 < L)
    (hload : ∀ v, (∑ i, if v ∈ S i then 1 / H i else 0) ≤ L) :
    ∀ v, (∑ i, if v ∈ S i then 1 / (L * H i) else 0) ≤ 1 := by
  classical
  intro v
  have heq : (∑ i, if v ∈ S i then 1 / (L * H i) else 0) =
      (∑ i, if v ∈ S i then 1 / H i else 0) / L := by
    rw [Finset.sum_div]
    apply Finset.sum_congr rfl
    intro i hi
    by_cases hv : v ∈ S i
    · simp only [hv, ite_true, div_div, mul_comm (H i) L]
    · simp only [hv, ite_false, zero_div]
  rw [heq]
  exact (div_le_iff₀ hL).mpr (by simpa only [one_mul] using hload v)

/-- Witness-load extension on arbitrary finite decreasing families.

Every witness must be forbidden and nonempty, and the supplied family must
cover the global obstruction. Overlap is controlled solely by the displayed
coordinate loads. The product-space Finner theorem discharges the analytic
premise of `witnessLoad_budget_of_productBound`.
-/
theorem witnessLoad_budget (D : Finset (Finset X)) (hD : decreasing D)
    (K : ℕ) (G : Finset (Finset X)) (hG : generatorCover D K G)
    (hnonempty : ∀ g ∈ G, g.Nonempty) (hbad : ∀ g ∈ G, g ∉ D)
    (p c : X → ℝ) (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1)
    (hc : ∀ v, 0 ≤ c v ∧ c v ≤ phi (p v)) (L : ℝ) (hL : 0 < L)
    (hload : ∀ v, (∑ g ∈ G, if v ∈ g then 1 / restrictionHazardStar D g else 0) ≤ L) :
    (0 < muOf D p → famPrice c G ≤ L * (-Real.log (muOf D p))) ∧
    (∃ H : Finset (Finset X), generatorCover D K H ∧
      famPrice c H ≤ cappedHazard L (muOf D p)) ∧
    coverCost D K c ≤ cappedHazard L (muOf D p) := by
  classical
  apply witnessLoad_budget_of_productBound D hD K G hG hnonempty hbad p c hp hc L hL
  intro _
  let S : G → Finset X := fun g => g.val
  let H : G → ℝ := fun g => restrictionHazardStar D g.val
  let w : G → ℝ := fun g => 1 / (L * H g)
  have hw : ∀ g, 0 ≤ w g := by
    intro g
    exact (one_div_pos.mpr (mul_pos hL
      (restrictionHazardStar_pos D hD g.val (hnonempty g.val g.property)
        (hbad g.val g.property)))).le
  have hn : ∀ v, (∑ g : G, if v ∈ S g then w g else 0) ≤ 1 := by
    apply normalize_incident_load S H L hL
    intro v
    simpa only [S, H, Finset.sum_coe_sort] using hload v
  have h := muOf_le_prod_restrictionMass_rpow D hD p hp S w hw hn
  simpa only [S, H, w, Finset.prod_coe_sort] using h

theorem witnessLoad_coverCost (D : Finset (Finset X)) (hD : decreasing D)
    (K : ℕ) (G : Finset (Finset X)) (hG : generatorCover D K G)
    (hnonempty : ∀ g ∈ G, g.Nonempty) (hbad : ∀ g ∈ G, g ∉ D)
    (p c : X → ℝ) (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1)
    (hc : ∀ v, 0 ≤ c v ∧ c v ≤ phi (p v)) (L : ℝ) (hL : 0 < L)
    (hload : ∀ v, (∑ g ∈ G, if v ∈ g then 1 / restrictionHazardStar D g else 0) ≤ L) :
    coverCost D K c ≤ cappedHazard L (muOf D p) :=
  (witnessLoad_budget D hD K G hG hnonempty hbad p c hp hc L hL hload).2.2

/-- The canonical maximum load supplies its own normalization certificate. -/
theorem maximumWitnessLoad_budget (D : Finset (Finset X)) (hD : decreasing D)
    (K : ℕ) (G : Finset (Finset X)) (hG : generatorCover D K G) (hGne : G.Nonempty)
    (hnonempty : ∀ g ∈ G, g.Nonempty) (hbad : ∀ g ∈ G, g ∉ D)
    (p c : X → ℝ) (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1)
    (hc : ∀ v, 0 ≤ c v ∧ c v ≤ phi (p v)) :
    (0 < muOf D p → famPrice c G ≤ maximumWitnessLoad D G * (-Real.log (muOf D p))) ∧
    (∃ H : Finset (Finset X), generatorCover D K H ∧
      famPrice c H ≤ cappedHazard (maximumWitnessLoad D G) (muOf D p)) ∧
    coverCost D K c ≤ cappedHazard (maximumWitnessLoad D G) (muOf D p) :=
  witnessLoad_budget D hD K G hG hnonempty hbad p c hp hc (maximumWitnessLoad D G)
    (maximumWitnessLoad_pos D hD G hGne hnonempty hbad)
    (witnessCoordinateLoad_le_maximum D G)

end UniversalLaw.General
