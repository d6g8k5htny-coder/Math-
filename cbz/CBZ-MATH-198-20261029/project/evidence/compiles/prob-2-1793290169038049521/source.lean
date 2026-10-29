import General.Definitions
import Closure.ProductMass

namespace UniversalLaw.General
open UniversalLaw.Spec.P15
open scoped BigOperators

variable {X : Type} [Fintype X] [DecidableEq X]

/-- The probability of the actual restriction, computed only on the block coordinates. -/
noncomputable def localMass {b : ℕ} (D : Finset (Finset X)) (blk : X → Fin b)
    (p : X → ℝ) (i : Fin b) : ℝ :=
  ∑ S ∈ (block blk i).powerset,
    if S ∈ D then P15Closure.blockWeight p (block blk i) S else 0

private def partitionData {b : ℕ} (blk : X → Fin b) : RealizedData X :=
  ⟨b, blk, fun _ => 0, fun _ => 0, ∅⟩

/-- No realized-family conditions are used by this finite partition identity. -/
theorem sum_block_functions {b : ℕ} (blk : X → Fin b)
    (f : Fin b → Finset X → ℝ) :
    (∑ U : Finset X, ∏ i, f i (U ∩ block blk i)) =
      ∏ i, ∑ S ∈ (block blk i).powerset, f i S :=
  P15Closure.sum_block_functions (partitionData blk) f

theorem weight_eq_prod_blockWeight {b : ℕ} (blk : X → Fin b)
    (p : X → ℝ) (U : Finset X) :
    weight p U = ∏ i, P15Closure.blockWeight p (block blk i) (U ∩ block blk i) :=
  P15Closure.weight_eq_prod_blockWeight (partitionData blk) p U

theorem localMass_nonneg {b : ℕ} (D : Finset (Finset X)) (blk : X → Fin b)
    (p : X → ℝ) (i : Fin b) (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) :
    0 ≤ localMass D blk p i := by
  classical
  apply Finset.sum_nonneg
  intro S hS
  split_ifs
  · exact P15Closure.blockWeight_nonneg p _ _ (Finset.mem_powerset.mp hS) (fun v _ => hp v)
  · exact le_rfl

theorem localMass_le_one {b : ℕ} (D : Finset (Finset X)) (blk : X → Fin b)
    (p : X → ℝ) (i : Fin b) (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) :
    localMass D blk p i ≤ 1 := by
  classical
  rw [← P15Closure.sum_blockWeight p (block blk i)]
  apply Finset.sum_le_sum
  intro S hS
  split_ifs
  · exact le_rfl
  · exact P15Closure.blockWeight_nonneg p _ _ (Finset.mem_powerset.mp hS) (fun v _ => hp v)

theorem localMass_emptyBlock {b : ℕ} (D : Finset (Finset X))
    (hD : decreasing D) (blk : X → Fin b) (p : X → ℝ) (i : Fin b)
    (hi : block blk i = ∅) : localMass D blk p i = 1 := by
  classical
  simp [localMass, hi, hD.1, P15Closure.blockWeight]

private theorem muOf_eq_sum_indicator (D : Finset (Finset X)) (p : X → ℝ) :
    muOf D p = ∑ U : Finset X, if U ∈ D then weight p U else 0 := by
  classical
  have hD : (Finset.univ : Finset (Finset X)).filter (· ∈ D) = D := by ext U; simp
  calc
    _ = ∑ U ∈ (Finset.univ : Finset (Finset X)).filter (· ∈ D), weight p U := by rw [hD]; rfl
    _ = _ := by rw [Finset.sum_filter]

/-- Global goodness implies all block restrictions are good. Crossing constraints need
not be independent, and the displayed inequality may be strict. -/
theorem muOf_le_prod_localMass {b : ℕ} (D : Finset (Finset X))
    (hD : decreasing D) (blk : X → Fin b) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) :
    muOf D p ≤ ∏ i, localMass D blk p i := by
  classical
  let f : Fin b → Finset X → ℝ := fun i S =>
    if S ∈ D then P15Closure.blockWeight p (block blk i) S else 0
  have hlocal : (∏ i, localMass D blk p i) =
      ∑ U : Finset X, ∏ i, f i (U ∩ block blk i) :=
    (sum_block_functions blk f).symm
  rw [hlocal, muOf_eq_sum_indicator]
  apply Finset.sum_le_sum
  intro U hU
  by_cases hgood : U ∈ D
  · rw [if_pos hgood, weight_eq_prod_blockWeight blk p U]
    apply le_of_eq
    apply Finset.prod_congr rfl
    intro i hi
    have hgi := hD.2 U hgood (U ∩ block blk i) Finset.inter_subset_left
    simp [f, hgi]
  · rw [if_neg hgood]
    apply Finset.prod_nonneg
    intro i hi
    dsimp [f]
    split_ifs
    · exact P15Closure.blockWeight_nonneg p _ _ Finset.inter_subset_right (fun v _ => hp v)
    · exact le_rfl

theorem localMass_pos_of_muOf_pos {b : ℕ} (D : Finset (Finset X))
    (hD : decreasing D) (blk : X → Fin b) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) (hmu : 0 < muOf D p) (i : Fin b) :
    0 < localMass D blk p i := by
  have hprod : 0 < ∏ i, localMass D blk p i :=
    hmu.trans_le (muOf_le_prod_localMass D hD blk p hp)
  have hne : localMass D blk p i ≠ 0 :=
    (Finset.prod_ne_zero_iff.mp hprod.ne') i (Finset.mem_univ i)
  exact lt_of_le_of_ne (localMass_nonneg D blk p i hp) (Ne.symm hne)

theorem muOf_eq_zero_of_localMass_zero {b : ℕ} (D : Finset (Finset X))
    (hD : decreasing D) (blk : X → Fin b) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) (i : Fin b) (hi : localMass D blk p i = 0) :
    muOf D p = 0 := by
  have hmass := muOf_le_prod_localMass D hD blk p hp
  rw [Finset.prod_eq_zero (Finset.mem_univ i) hi] at hmass
  exact le_antisymm hmass (P15Closure.muOf_nonneg D p hp)

/-- Both the failure-probability and exact logarithmic budgets, on the positive-mass branch. -/
theorem independentBlockHazard {b : ℕ} (D : Finset (Finset X))
    (hD : decreasing D) (blk : X → Fin b) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) (hmu : 0 < muOf D p) :
    (∑ i, (1 - localMass D blk p i)) ≤ ∑ i, -Real.log (localMass D blk p i) ∧
      (∑ i, -Real.log (localMass D blk p i)) ≤ -Real.log (muOf D p) := by
  have hpos := localMass_pos_of_muOf_pos D hD blk p hp hmu
  constructor
  · apply Finset.sum_le_sum
    intro i hi
    have hlog := Real.log_le_sub_one_of_pos (hpos i)
    linarith
  · rw [Finset.sum_neg_distrib, ← Real.log_prod (fun i _ => (hpos i).ne')]
    exact neg_le_neg (Real.log_le_log hmu (muOf_le_prod_localMass D hD blk p hp))

/-- Local `phi` certificates can be summed using their actual local masses. -/
theorem sum_phi_le_hazard {b : ℕ} (D : Finset (Finset X))
    (hD : decreasing D) (blk : X → Fin b) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) (hmu : 0 < muOf D p) :
    (∑ i, phi (1 - localMass D blk p i)) ≤ -Real.log (muOf D p) := by
  apply le_trans _ (independentBlockHazard D hD blk p hp hmu).2
  apply Finset.sum_le_sum
  intro i hi
  have hpos := localMass_pos_of_muOf_pos D hD blk p hp hmu i
  have hlt : 1 - localMass D blk p i < 1 := by linarith
  have heq : 1 - (1 - localMass D blk p i) = localMass D blk p i := by ring
  rw [phi, if_pos hlt, heq]
  exact min_le_right _ _

theorem famPrice_nonneg (c : X → ℝ) (hc : ∀ v, 0 ≤ c v)
    (G : Finset (Finset X)) : 0 ≤ famPrice c G :=
  Finset.sum_nonneg (fun g _ => Finset.prod_nonneg (fun v _ => hc v))

/-- Repeated generators in different blocks are counted once in the actual union. -/
theorem famPrice_biUnion_le {b : ℕ} (c : X → ℝ) (hc : ∀ v, 0 ≤ c v)
    (G : Fin b → Finset (Finset X)) :
    famPrice c (Finset.univ.biUnion G) ≤ ∑ i, famPrice c (G i) := by
  classical
  let V := Finset.univ.biUnion G
  have hprice : ∀ g : Finset X, 0 ≤ genPrice c g :=
    fun g => Finset.prod_nonneg (fun v _ => hc v)
  calc
    _ ≤ ∑ g ∈ V, ∑ i : Fin b, if g ∈ G i then genPrice c g else 0 := by
      apply Finset.sum_le_sum
      intro g hg
      obtain ⟨i, hi, hgi⟩ := Finset.mem_biUnion.mp hg
      calc
        _ = (if g ∈ G i then genPrice c g else 0) := by rw [if_pos hgi]
        _ ≤ _ := by
          apply Finset.single_le_sum (f := fun j : Fin b =>
            if g ∈ G j then genPrice c g else 0) ?_ hi
          intro j hj
          split_ifs
          · exact hprice g
          · exact le_rfl
    _ = ∑ i : Fin b, ∑ g ∈ V, if g ∈ G i then genPrice c g else 0 := Finset.sum_comm
    _ = _ := by
      apply Finset.sum_congr rfl
      intro i hi
      rw [← Finset.sum_filter]
      have heq : V.filter (· ∈ G i) = G i := by
        ext g
        simp only [Finset.mem_filter]
        constructor
        · exact And.right
        · intro hg
          exact ⟨Finset.mem_biUnion.mpr ⟨i, Finset.mem_univ i, hg⟩, hg⟩
      rw [heq]
      rfl

theorem coverCost_le_family (D : Finset (Finset X)) (K : ℕ) (c : X → ℝ)
    (hc : ∀ v, 0 ≤ c v) (G : Finset (Finset X)) (hG : generatorCover D K G) :
    coverCost D K c ≤ famPrice c G := by
  apply csInf_le
  · refine ⟨0, ?_⟩
    rintro t ⟨H, _, rfl⟩
    exact famPrice_nonneg c hc H
  · exact ⟨G, hG, rfl⟩

theorem emptyGenerator_cover (D : Finset (Finset X)) (K : ℕ) :
    generatorCover D K ({∅} : Finset (Finset X)) := by
  intro U _
  exact ⟨∅, by simp, Finset.empty_subset U⟩

theorem coverCost_le_one (D : Finset (Finset X)) (K : ℕ) (c : X → ℝ)
    (hc : ∀ v, 0 ≤ c v) : coverCost D K c ≤ 1 := by
  classical
  simpa [famPrice, genPrice] using
    coverCost_le_family D K c hc {∅} (emptyGenerator_cover D K)

/-- A concrete cover realizes the cap: use the supplied cover when its hazard is below
one, and the singleton empty generator otherwise. -/
theorem exists_capped_cover_of_hazard (D : Finset (Finset X)) (K : ℕ)
    (c : X → ℝ) (m : ℝ) (G : Finset (Finset X)) (hG : generatorCover D K G)
    (hbudget : 0 < m → famPrice c G ≤ -Real.log m) :
    ∃ H : Finset (Finset X), generatorCover D K H ∧
      famPrice c H ≤ cappedHazard 1 m := by
  classical
  by_cases hm : 0 < m
  · rw [cappedHazard, if_pos hm, one_mul]
    by_cases hh : -Real.log m < 1
    · exact ⟨G, hG, (hbudget hm).trans (le_of_eq (min_eq_right hh.le).symm)⟩
    · refine ⟨{∅}, emptyGenerator_cover D K, ?_⟩
      simp only [famPrice, Finset.sum_singleton, genPrice, Finset.prod_empty]
      rw [min_eq_left (le_of_not_gt hh)]
  · refine ⟨{∅}, emptyGenerator_cover D K, ?_⟩
    simp [cappedHazard, hm, famPrice, genPrice]

/-- Conditional assembly, with the actual union cover hypothesis exposed. -/
theorem budget_of_union_cover {b : ℕ} (D : Finset (Finset X))
    (hD : decreasing D) (blk : X → Fin b) (p c : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) (hc : ∀ v, 0 ≤ c v)
    (K : ℕ) (G : Fin b → Finset (Finset X))
    (hG : generatorCover D K (Finset.univ.biUnion G))
    (hlocal : ∀ i, famPrice c (G i) ≤ phi (1 - localMass D blk p i)) :
    (famPrice c (Finset.univ.biUnion G) ≤ ∑ i, phi (1 - localMass D blk p i)) ∧
    (∃ H : Finset (Finset X), generatorCover D K H ∧
      famPrice c H ≤ cappedHazard 1 (muOf D p)) ∧
    coverCost D K c ≤ cappedHazard 1 (muOf D p) := by
  have hprice : famPrice c (Finset.univ.biUnion G) ≤
      ∑ i, phi (1 - localMass D blk p i) :=
    (famPrice_biUnion_le c hc G).trans (Finset.sum_le_sum (fun i _ => hlocal i))
  have hex := exists_capped_cover_of_hazard D K c (muOf D p)
    (Finset.univ.biUnion G) hG (fun hmu => hprice.trans (sum_phi_le_hazard D hD blk p hp hmu))
  refine ⟨hprice, hex, ?_⟩
  obtain ⟨H, hH, hbudget⟩ := hex
  exact (coverCost_le_family D K c hc H hH).trans hbudget

end UniversalLaw.General
