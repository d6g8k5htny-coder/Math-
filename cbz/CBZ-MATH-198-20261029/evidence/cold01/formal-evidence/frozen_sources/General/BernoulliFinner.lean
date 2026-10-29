import General.FinnerBridge
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
  simp

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
  simp only [apply_ite, NNReal.coe_one, NNReal.coe_zero, mul_one, mul_zero]
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
  simp only [apply_ite, NNReal.coe_one, NNReal.coe_zero, mul_one, mul_zero]

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

/-- The Bernoulli tensor average is exactly the specification's global mass. -/
theorem bernoulli_tensor_good_coe (D : Finset (Finset X)) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) :
    (tensorAverage (bernoulliWeights p hp) (goodIndicator D) : ℝ) = muOf D p :=
  bernoulli_good_sum_coe D p hp

/-- The local tensor event has the ACTUAL restricted-coordinate mass, even for
an overlapping support. No ambient outside-coordinate factor survives. -/
theorem bernoulli_tensor_restriction_coe (D : Finset (Finset X)) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) (g : Finset X) :
    (tensorAverage (bernoulliWeights p hp) (restrictionIndicator D g) : ℝ) =
      restrictionMass D p g :=
  bernoulli_restriction_sum_coe D p hp g

theorem bernoulli_tensor_good (D : Finset (Finset X)) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) :
    tensorAverage (bernoulliWeights p hp) (goodIndicator D) = Real.toNNReal (muOf D p) := by
  apply NNReal.eq
  rw [bernoulli_tensor_good_coe, Real.coe_toNNReal _ (P15Closure.muOf_nonneg D p hp)]

theorem bernoulli_tensor_restriction (D : Finset (Finset X)) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) (g : Finset X) :
    tensorAverage (bernoulliWeights p hp) (restrictionIndicator D g) =
      Real.toNNReal (restrictionMass D p g) := by
  have hnonneg : 0 ≤ restrictionMass D p g := by
    rw [← bernoulli_tensor_restriction_coe D p hp g]
    exact (tensorAverage (bernoulliWeights p hp) (restrictionIndicator D g)).property
  apply NNReal.eq
  rw [bernoulli_tensor_restriction_coe, Real.coe_toNNReal _ hnonneg]

/-- Overlapping-restriction probability inequality under the ORIGINAL-coordinate
fractional load condition. The product-space theorem supplies the dependence
control; independence of the overlapping events is never assumed. Zero means,
zero weights, empty supports and probability endpoints are included. -/
theorem muOf_le_prod_restrictionMass_rpow {I : Type} [Fintype I]
    (D : Finset (Finset X)) (hD : decreasing D) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) (S : I → Finset X) (lam : I → ℝ)
    (hlam : ∀ i, 0 ≤ lam i)
    (hload : ∀ x, (∑ i, if x ∈ S i then lam i else 0) ≤ 1) :
    muOf D p ≤ ∏ i, (restrictionMass D p (S i)) ^ (lam i) := by
  classical
  let q := bernoulliWeights p hp
  let w : I → ℝ≥0 := fun i => ⟨lam i, hlam i⟩
  have hwcoe : ∀ i, (w i : ℝ) = lam i := fun _ => rfl
  have hload' : ∀ x, (∑ i, if x ∈ S i then w i else 0) ≤ 1 := by
    intro x
    change ((∑ i, if x ∈ S i then w i else 0 : ℝ≥0) : ℝ) ≤ 1
    rw [NNReal.coe_sum]
    have hcoe : ∀ i, ((if x ∈ S i then w i else 0 : ℝ≥0) : ℝ) =
        if x ∈ S i then lam i else 0 := by
      intro i
      split_ifs <;> rfl
    simp_rw [hcoe]
    exact hload x
  have hpoint : tensorAverage q (goodIndicator D) ≤
      tensorAverage q (fun a => ∏ i, restrictionIndicator D (S i) a ^ (w i : ℝ)) := by
    apply Finset.sum_le_sum
    intro a ha
    exact mul_le_mul_of_nonneg_left
      (goodIndicator_le_prod_restrictionIndicator D hD S w a) (by positivity)
  have hfinner := finner_tensor q (bernoulliWeights_sum p hp) S w hload'
    (fun i => restrictionIndicator D (S i)) (fun i => restrictionIndicator_dependsOn D (S i))
  have hreal := NNReal.coe_le_coe.mpr (hpoint.trans hfinner)
  simp only [NNReal.coe_prod, NNReal.coe_rpow, hwcoe] at hreal
  simpa only [q, bernoulli_tensor_good_coe,
    bernoulli_tensor_restriction_coe] using hreal

end UniversalLaw.General

#print axioms UniversalLaw.General.bernoulli_tensor_good
#print axioms UniversalLaw.General.bernoulli_tensor_restriction
#print axioms UniversalLaw.General.muOf_le_prod_restrictionMass_rpow
