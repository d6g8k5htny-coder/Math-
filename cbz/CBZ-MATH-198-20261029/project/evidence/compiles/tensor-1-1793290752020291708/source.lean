import General.Finner

namespace UniversalLaw.General
open scoped BigOperators

variable {X A : Type} [Fintype X] [DecidableEq X] [Fintype A]

/-- The explicit finite independent-coordinate expectation. -/
noncomputable def tensorAverage (q : X → A → ℝ≥0)
    (f : (X → A) → ℝ≥0) : ℝ≥0 :=
  ∑ a : X → A, (∏ x, q x (a x)) * f a

theorem tensor_weights_sum (q : X → A → ℝ≥0)
    (hq : ∀ x, ∑ v, q x v = 1) :
    (∑ a : X → A, ∏ x, q x (a x)) = 1 := by
  rw [← Fintype.prod_sum]
  simp_rw [hq]
  simp

theorem tensorAverage_const (q : X → A → ℝ≥0)
    (hq : ∀ x, ∑ v, q x v = 1) (c : ℝ≥0) :
    tensorAverage q (fun _ => c) = c := by
  unfold tensorAverage
  rw [← Finset.sum_mul, tensor_weights_sum q hq, one_mul]

private theorem tensorAverage_split (q : X → A → ℝ≥0)
    (f : (X → A) → ℝ≥0) (x : X) :
    tensorAverage q f = ∑ v : A, ∑ b : {y : X // y ≠ x} → A,
      (q x v * ∏ y : {y : X // y ≠ x}, q y.val (b y)) *
        f ((Equiv.funSplitAt x A).symm (v,b)) := by
  classical
  unfold tensorAverage
  rw [← (Equiv.funSplitAt x A).symm.sum_comp
    (fun a : X → A => (∏ y, q y (a y)) * f a)]
  rw [Fintype.sum_prod_type]
  apply Finset.sum_congr rfl
  intro v hv
  apply Finset.sum_congr rfl
  intro b hb
  congr 1
  rw [Fintype.prod_eq_mul_prod_subtype_ne _ x]
  simp [Equiv.funSplitAt, Equiv.piSplitAt]

theorem tensorAverage_coordinateAverage (q : X → A → ℝ≥0)
    (hq : ∀ x, ∑ v, q x v = 1) (x : X) (f : (X → A) → ℝ≥0) :
    tensorAverage q (coordinateAverage q x f) = tensorAverage q f := by
  classical
  let E := Equiv.funSplitAt x A
  have hu (v w : A) (b : {y : X // y ≠ x} → A) :
      Function.update (E.symm (v,b)) x w = E.symm (w,b) := by
    funext y
    by_cases hy : y = x
    · subst y
      simp [E, Equiv.funSplitAt, Equiv.piSplitAt]
    · simp [E, Equiv.funSplitAt, Equiv.piSplitAt, hy]
  have hca (v : A) (b : {y : X // y ≠ x} → A) :
      coordinateAverage q x f (E.symm (v,b)) = ∑ w, q x w * f (E.symm (w,b)) := by
    unfold coordinateAverage
    simp_rw [hu]
  rw [tensorAverage_split q (coordinateAverage q x f) x,
      tensorAverage_split q f x]
  change (∑ v : A, ∑ b : {y : X // y ≠ x} → A,
    (q x v * ∏ y : {y : X // y ≠ x}, q y.val (b y)) *
      coordinateAverage q x f (E.symm (v,b))) = _
  simp_rw [hca]
  rw [Finset.sum_comm]
  conv_rhs => rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro b hb
  let R := ∏ y : {y : X // y ≠ x}, q y.val (b y)
  let m := ∑ w, q x w * f (E.symm (w,b))
  change (∑ v, (q x v * R) * m) = ∑ v, (q x v * R) * f (E.symm (v,b))
  calc
    _ = (∑ v, q x v) * (R * m) := by
      rw [Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro v hv
      ac_rfl
    _ = R * m := by rw [hq x, one_mul]
    _ = _ := by
      dsimp [m]
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro v hv
      ac_rfl

theorem tensorAverage_productAverage (q : X → A → ℝ≥0)
    (hq : ∀ x, ∑ v, q x v = 1) (xs : List X) (f : (X → A) → ℝ≥0) :
    tensorAverage q (productAverage q xs f) = tensorAverage q f := by
  induction xs generalizing f with
  | nil => rfl
  | cons x xs ih =>
    change tensorAverage q (productAverage q xs (coordinateAverage q x f)) = _
    rw [ih, tensorAverage_coordinateAverage q hq]

/-- Complete coordinate averaging equals the explicit tensor sum, independently
of the initial assignment. -/
theorem productAverage_eq_tensor (q : X → A → ℝ≥0)
    (hq : ∀ x, ∑ v, q x v = 1) (xs : List X) (hxs : ∀ x, x ∈ xs)
    (f : (X → A) → ℝ≥0) (a : X → A) :
    productAverage q xs f a = tensorAverage q f := by
  have hconst : productAverage q xs f = fun _ => productAverage q xs f a := by
    funext b
    exact productAverage_eq_of_complete q xs hxs f b a
  calc
    _ = tensorAverage q (fun _ => productAverage q xs f a) :=
      (tensorAverage_const q hq _).symm
    _ = tensorAverage q (productAverage q xs f) := congrArg (tensorAverage q) hconst.symm
    _ = _ := tensorAverage_productAverage q hq xs f

/-- Finite product-space Finner inequality for explicit product expectations. -/
theorem finner_tensor {I : Type} [Fintype I] [Nonempty A]
    (q : X → A → ℝ≥0) (hq : ∀ x, ∑ v, q x v = 1)
    (S : I → Finset X) (w : I → ℝ≥0)
    (hload : ∀ x, (∑ i, if x ∈ S i then w i else 0) ≤ 1)
    (f : I → (X → A) → ℝ≥0) (hf : ∀ i, functionDependsOn (S i) (f i)) :
    tensorAverage q (fun a => ∏ i, f i a ^ (w i : ℝ)) ≤
      ∏ i, tensorAverage q (f i) ^ (w i : ℝ) := by
  classical
  let xs := (Finset.univ : Finset X).toList
  have hxs : ∀ x, x ∈ xs := by intro x; simp [xs]
  let a : X → A := fun _ => Classical.choice inferInstance
  have h := finner_productAverage q hq xs S w hload f hf a
  simp_rw [productAverage_eq_tensor q hq xs hxs] at h
  exact h

end UniversalLaw.General

#print axioms UniversalLaw.General.finner_tensor
