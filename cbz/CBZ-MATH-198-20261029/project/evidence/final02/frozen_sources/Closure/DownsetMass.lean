import Closure.ProductMass
import SpecificationProofs.P15Elementary

namespace UniversalLaw.P15Closure
open UniversalLaw.Spec.P15
open scoped BigOperators
attribute [local instance] Classical.propDecidable

/-- A weight with one coordinate omitted. -/
noncomputable def coordinateWeight {Y : Type} [Fintype Y] [DecidableEq Y]
    (p : Y → ℝ) (i : Y) (U : Finset Y) : ℝ :=
  (∏ v ∈ U.erase i, p v) * ∏ v ∈ (Finset.univ \ U).erase i, (1 - p v)

theorem coordinateWeight_nonneg {Y : Type} [Fintype Y] [DecidableEq Y]
    (p : Y → ℝ) (hp : ∀ i, 0 ≤ p i ∧ p i ≤ 1) (i : Y) (U : Finset Y) :
    0 ≤ coordinateWeight p i U := by
  apply mul_nonneg
  · exact Finset.prod_nonneg (fun v _ => (hp v).1)
  · exact Finset.prod_nonneg (fun v _ => sub_nonneg.mpr (hp v).2)

theorem coordinateWeight_erase {Y : Type} [Fintype Y] [DecidableEq Y]
    (p : Y → ℝ) (i : Y) (U : Finset Y) :
    coordinateWeight p i (U.erase i) = coordinateWeight p i U := by
  have heq : ((Finset.univ \ U.erase i).erase i) = ((Finset.univ \ U).erase i) := by
    ext j
    by_cases h : j = i <;> simp_all
  simp only [coordinateWeight, Finset.erase_idem, heq]

theorem weight_update_coordinate {Y : Type} [Fintype Y] [DecidableEq Y]
    (p : Y → ℝ) (i : Y) (s : ℝ) (U : Finset Y) :
    weight (Function.update p i s) U =
      (if i ∈ U then s else 1 - s) * coordinateWeight p i U := by
  have heq : (fun v => 1 - Function.update p i s v) =
      Function.update (fun v => 1 - p v) i (1 - s) := by
    funext v
    by_cases h : v = i <;> simp_all
  unfold weight coordinateWeight
  rw [heq]
  by_cases hi : i ∈ U
  · rw [Finset.prod_update_of_mem hi,
      Finset.prod_update_of_notMem (by simp [hi]), if_pos hi,
      Finset.sdiff_singleton_eq_erase]
    have hc : (Finset.univ \ U).erase i = Finset.univ \ U :=
      Finset.erase_eq_of_notMem (by simp [hi])
    rw [hc]
    ring
  · rw [Finset.prod_update_of_notMem hi,
      Finset.prod_update_of_mem (by simp [hi]), if_neg hi,
      Finset.sdiff_singleton_eq_erase, Finset.erase_eq_of_notMem hi]
    ring

/-- Endpoint coefficients of a finite downset satisfy the decreasing-coordinate order. -/
theorem coordinate_sections_order {Y : Type} [Fintype Y] [DecidableEq Y]
    (A : Finset (Finset Y))
    (hdown : ∀ U ∈ A, ∀ V : Finset Y, V ⊆ U → V ∈ A)
    (p : Y → ℝ) (hp : ∀ i, 0 ≤ p i ∧ p i ≤ 1) (i : Y) :
    (∑ U ∈ A.filter (fun U => i ∈ U), coordinateWeight p i U) ≤
      ∑ U ∈ A.filter (fun U => i ∉ U), coordinateWeight p i U := by
  apply Finset.sum_le_sum_of_injOn (fun U : Finset Y => U.erase i)
  · intro U hU V hV heq
    have hiU := (Finset.mem_filter.mp hU).2
    have hiV := (Finset.mem_filter.mp hV).2
    change U.erase i = V.erase i at heq
    exact (Finset.insert_erase hiU).symm.trans
      ((congrArg (fun W : Finset Y => insert i W) heq).trans (Finset.insert_erase hiV))
  · intro V hV
    obtain ⟨U, hU, rfl⟩ := Finset.mem_image.mp hV
    have hUA := (Finset.mem_filter.mp hU).1
    exact Finset.mem_filter.mpr
      ⟨hdown U hUA (U.erase i) (Finset.erase_subset i U), Finset.notMem_erase i U⟩
  · intro U _
    rw [coordinateWeight_erase]
  · intro U _ _
    exact coordinateWeight_nonneg p hp i U

/-- The finite product mass is affine in any single probability coordinate. -/
theorem muOf_update_affine {Y : Type} [Fintype Y] [DecidableEq Y]
    (A : Finset (Finset Y)) (p : Y → ℝ) (i : Y) (s : ℝ) :
    muOf A (Function.update p i s) =
      s * (∑ U ∈ A.filter (fun U => i ∈ U), coordinateWeight p i U) +
      (1 - s) * (∑ U ∈ A.filter (fun U => i ∉ U), coordinateWeight p i U) := by
  unfold muOf
  simp_rw [Finset.sum_filter, Finset.mul_sum]
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro U _
  rw [weight_update_coordinate]
  by_cases hi : i ∈ U <;> simp [hi]

/-- Endpoint form of affine dependence on a probability coordinate. -/
theorem muOf_update_endpoints {Y : Type} [Fintype Y] [DecidableEq Y]
    (A : Finset (Finset Y)) (p : Y → ℝ) (i : Y) (s : ℝ) :
    muOf A (Function.update p i s) =
      (1 - s) * muOf A (Function.update p i 0) +
      s * muOf A (Function.update p i 1) := by
  rw [muOf_update_affine, muOf_update_affine A p i 0,
    muOf_update_affine A p i 1]
  ring

/-- A downset loses mass when one coordinate is forced to one. -/
theorem muOf_update_one_le_zero {Y : Type} [Fintype Y] [DecidableEq Y]
    (A : Finset (Finset Y))
    (hdown : ∀ U ∈ A, ∀ V : Finset Y, V ⊆ U → V ∈ A)
    (p : Y → ℝ) (hp : ∀ i, 0 ≤ p i ∧ p i ≤ 1) (i : Y) :
    muOf A (Function.update p i 1) ≤ muOf A (Function.update p i 0) := by
  rw [muOf_update_affine, muOf_update_affine]
  simpa using coordinate_sections_order A hdown p hp i

/-- Every single-coordinate section of a downset mass is antitone. -/
theorem muOf_update_antitone {Y : Type} [Fintype Y] [DecidableEq Y]
    (A : Finset (Finset Y))
    (hdown : ∀ U ∈ A, ∀ V : Finset Y, V ⊆ U → V ∈ A)
    (p : Y → ℝ) (hp : ∀ i, 0 ≤ p i ∧ p i ≤ 1) (i : Y)
    (s t : ℝ) (hst : s ≤ t) :
    muOf A (Function.update p i t) ≤ muOf A (Function.update p i s) := by
  rw [muOf_update_endpoints A p i t, muOf_update_endpoints A p i s]
  have hord := muOf_update_one_le_zero A hdown p hp i
  have hm := mul_nonneg (sub_nonneg.mpr hst) (sub_nonneg.mpr hord)
  nlinarith

/-- Finite downset mass decreases under coordinatewise increases in probabilities. -/
theorem muOf_antitone {Y : Type} [Fintype Y] [DecidableEq Y]
    (A : Finset (Finset Y))
    (hdown : ∀ U ∈ A, ∀ V : Finset Y, V ⊆ U → V ∈ A)
    (p q : Y → ℝ) (hp : ∀ i, 0 ≤ p i ∧ p i ≤ 1)
    (hq : ∀ i, 0 ≤ q i ∧ q i ≤ 1) (hpq : ∀ i, p i ≤ q i) :
    muOf A q ≤ muOf A p := by
  have main : ∀ S : Finset Y,
      muOf A (fun j => if j ∈ S then q j else p j) ≤ muOf A p := by
    intro S
    induction S using Finset.induction_on with
    | empty => simpa
    | @insert i S hi ih =>
      let u : Y → ℝ := fun j => if j ∈ S then q j else p j
      have hu : ∀ j, 0 ≤ u j ∧ u j ≤ 1 := by
        intro j
        dsimp [u]
        split_ifs <;> first | exact hq j | exact hp j
      have hbase : Function.update u i (p i) = u := by
        funext j
        by_cases hj : j = i
        · subst j; simp [u, hi]
        · simp [Function.update_of_ne hj]
      have hstep : Function.update u i (q i) =
          fun j => if j ∈ insert i S then q j else p j := by
        funext j
        by_cases hj : j = i
        · subst j; simp
        · simp [Function.update_of_ne hj, u, hj]
      have h := muOf_update_antitone A hdown u hu i (p i) (q i) (hpq i)
      rw [hbase, hstep] at h
      exact h.trans ih
  simpa using main Finset.univ

#check coordinateWeight_nonneg
#check coordinateWeight_erase
#check weight_update_coordinate
#check coordinate_sections_order
#check muOf_update_affine
#check muOf_update_endpoints
#check muOf_update_one_le_zero
#check muOf_update_antitone
#check muOf_antitone
#print axioms coordinateWeight_nonneg
#print axioms coordinateWeight_erase
#print axioms weight_update_coordinate
#print axioms coordinate_sections_order
#print axioms muOf_update_affine
#print axioms muOf_update_endpoints
#print axioms muOf_update_one_le_zero
#print axioms muOf_update_antitone
#print axioms muOf_antitone

end UniversalLaw.P15Closure
