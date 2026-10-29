import General.Finner
import General.Overlap

namespace UniversalLaw.General
open UniversalLaw.Spec.P15
open scoped BigOperators NNReal

variable {X : Type} [Fintype X] [DecidableEq X]

/-- True means that the original coordinate is selected. -/
def selectedFinset (a : X → Bool) : Finset X :=
  Finset.univ.filter (fun x => a x = true)

@[simp] theorem mem_selectedFinset (a : X → Bool) (x : X) :
    x ∈ selectedFinset a ↔ a x = true := by simp [selectedFinset]

/-- Boolean assignments and subsets encode exactly the same finite outcomes. -/
noncomputable def boolFinsetEquiv : (X → Bool) ≃ Finset X where
  toFun := selectedFinset
  invFun U x := decide (x ∈ U)
  left_inv a := by
    funext x
    cases h : a x <;> simp [h]
  right_inv U := by ext x; simp

/-- Independent original-coordinate Bernoulli weights, including zero and one. -/
def bernoulliWeights (p : X → ℝ) (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1)
    (x : X) (b : Bool) : ℝ≥0 :=
  if b then ⟨p x, (hp x).1⟩ else ⟨1 - p x, sub_nonneg.mpr (hp x).2⟩

@[simp] theorem coe_bernoulliWeights (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) (x : X) (b : Bool) :
    (bernoulliWeights p hp x b : ℝ) = if b then p x else 1 - p x := by
  cases b <;> rfl

theorem bernoulliWeights_sum (p : X → ℝ) (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1)
    (x : X) : ∑ b, bernoulliWeights p hp x b = 1 := by
  apply NNReal.eq
  simp only [NNReal.coe_sum, coe_bernoulliWeights, NNReal.coe_one]
  simp [Fintype.sum_bool]

/-- The tensor outcome weight is the existing specification's subset weight. -/
theorem bernoulli_product_weight (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) (a : X → Bool) :
    (∏ x, (bernoulliWeights p hp x (a x) : ℝ)) = weight p (selectedFinset a) := by
  classical
  simp_rw [coe_bernoulliWeights]
  have hite : (fun x => if a x then p x else 1 - p x) =
      (fun x => if a x = true then p x else 1 - p x) := by
    funext x
    cases a x <;> rfl
  rw [hite, Finset.prod_ite]
  unfold weight selectedFinset
  congr 2
  ext x
  simp

/-- Exact change of finite outcomes from Boolean assignments to subsets. -/
theorem bernoulli_sum_coe (p : X → ℝ) (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1)
    (f : Finset X → ℝ≥0) :
    ((∑ a : X → Bool, (∏ x, bernoulliWeights p hp x (a x)) * f (selectedFinset a) : ℝ≥0) : ℝ) =
      ∑ U : Finset X, weight p U * (f U : ℝ) := by
  simp only [NNReal.coe_sum, NNReal.coe_mul, NNReal.coe_prod]
  simp_rw [bernoulli_product_weight]
  exact (boolFinsetEquiv (X := X)).sum_comp (fun U => weight p U * (f U : ℝ))

/-- Global and restricted good-event indicators. -/
noncomputable def goodIndicator (D : Finset (Finset X)) (a : X → Bool) : ℝ≥0 :=
  if selectedFinset a ∈ D then 1 else 0

noncomputable def restrictionIndicator (D : Finset (Finset X)) (g : Finset X)
    (a : X → Bool) : ℝ≥0 := if selectedFinset a ∩ g ∈ D then 1 else 0

theorem bernoulli_good_sum_coe (D : Finset (Finset X)) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) :
    ((∑ a : X → Bool, (∏ x, bernoulliWeights p hp x (a x)) * goodIndicator D a : ℝ≥0) : ℝ) =
      muOf D p := by
  classical
  have h := bernoulli_sum_coe p hp (fun U => if U ∈ D then 1 else 0)
  change _ = _ at h
  unfold goodIndicator
  rw [h]
  simp only [NNReal.coe_ite, NNReal.coe_one, NNReal.coe_zero, mul_ite, mul_one, mul_zero]
  rw [← Finset.sum_filter]
  have hfilter : (Finset.univ : Finset (Finset X)).filter (· ∈ D) = D := by ext U; simp
  rw [hfilter]
  rfl

theorem bernoulli_restriction_sum_coe (D : Finset (Finset X)) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) (g : Finset X) :
    ((∑ a : X → Bool, (∏ x, bernoulliWeights p hp x (a x)) * restrictionIndicator D g a : ℝ≥0) : ℝ) =
      restrictionMass D p g := by
  classical
  have h := bernoulli_sum_coe p hp (fun U => if U ∩ g ∈ D then 1 else 0)
  change _ = _ at h
  unfold restrictionIndicator
  rw [h, restrictionMass_eq_ambient]
  simp only [NNReal.coe_ite, NNReal.coe_one, NNReal.coe_zero, mul_ite, mul_one, mul_zero]

/-- A restriction indicator depends only on original coordinates inside its support. -/
theorem restrictionIndicator_dependsOn (D : Finset (Finset X)) (g : Finset X) :
    functionDependsOn g (restrictionIndicator D g) := by
  intro a b hab
  have heq : selectedFinset a ∩ g = selectedFinset b ∩ g := by
    ext x
    by_cases hx : x ∈ g
    · simp only [Finset.mem_inter, mem_selectedFinset, hx, and_true]
      rw [hab x hx]
    · simp [hx]
  simp only [restrictionIndicator, heq]

/-- On every globally good outcome all actual restrictions are good. Otherwise the
global indicator is zero. This needs no independence between overlapping events. -/
theorem goodIndicator_le_prod_restrictionIndicator {I : Type} [Fintype I]
    (D : Finset (Finset X)) (hD : decreasing D) (S : I → Finset X)
    (w : I → ℝ≥0) (a : X → Bool) :
    goodIndicator D a ≤ ∏ i, restrictionIndicator D (S i) a ^ (w i : ℝ) := by
  classical
  by_cases ha : selectedFinset a ∈ D
  · have hlocal : ∀ i, selectedFinset a ∩ S i ∈ D :=
      fun i => hD.2 _ ha _ Finset.inter_subset_left
    simp [goodIndicator, restrictionIndicator, ha, hlocal]
  · simp [goodIndicator, ha]

end UniversalLaw.General
