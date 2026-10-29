import General.Definitions
import Mathlib.Analysis.MeanInequalities

namespace UniversalLaw.General
open scoped BigOperators NNReal

/-- Weighted AM-GM with an unused fraction of weight assigned to the constant one. -/
theorem nnreal_prod_rpow_le_affine {I : Type} [Fintype I]
    (w z : I → ℝ≥0) (hw : ∑ i, w i ≤ 1) :
    ∏ i, z i ^ (w i : ℝ) ≤ (1 - ∑ i, w i) + ∑ i, w i * z i := by
  classical
  let w' : Option I → ℝ≥0 := fun i => i.elim (1 - ∑ i, w i) w
  let z' : Option I → ℝ≥0 := fun i => i.elim 1 z
  have hsum : ∑ i, w' i = 1 := by
    simp only [Fintype.sum_option, w', Option.elim_none, Option.elim_some]
    exact tsub_add_cancel_of_le hw
  have h := NNReal.geom_mean_le_arith_mean_weighted Finset.univ w' z' hsum
  simpa [Fintype.prod_option, Fintype.sum_option, w', z'] using h

/-- Finite probability-space weighted Hölder, including zero means and zero weights. -/
theorem nnreal_weightedHolder {I Ω : Type} [Fintype I] [Fintype Ω]
    (q : Ω → ℝ≥0) (hq : ∑ a, q a = 1)
    (w : I → ℝ≥0) (hw : ∑ i, w i ≤ 1) (f : I → Ω → ℝ≥0) :
    (∑ a, q a * ∏ i, f i a ^ (w i : ℝ)) ≤
      ∏ i, (∑ a, q a * f i a) ^ (w i : ℝ) := by
  classical
  let m : I → ℝ≥0 := fun i => ∑ a, q a * f i a
  by_cases hz : ∃ i, w i ≠ 0 ∧ m i = 0
  · obtain ⟨i, hwi, hmi⟩ := hz
    have hwie : (w i : ℝ) ≠ 0 := by exact_mod_cast hwi
    have hright : (∏ i, m i ^ (w i : ℝ)) = 0 :=
      Finset.prod_eq_zero (Finset.mem_univ i) (by rw [hmi, NNReal.zero_rpow hwie])
    change _ ≤ ∏ i, m i ^ (w i : ℝ)
    rw [hright]
    apply le_of_eq
    apply Finset.sum_eq_zero
    intro a ha
    by_cases hqa : q a = 0
    · simp [hqa]
    · have hterm : q a * f i a = 0 :=
        (Finset.sum_eq_zero_iff.mp hmi) a (Finset.mem_univ a)
      have hfi : f i a = 0 := (mul_eq_zero.mp hterm).resolve_left hqa
      have hprod : (∏ i, f i a ^ (w i : ℝ)) = 0 :=
        Finset.prod_eq_zero (Finset.mem_univ i) (by rw [hfi, NNReal.zero_rpow hwie])
      rw [hprod, mul_zero]
  · have hgood : ∀ i, w i ≠ 0 → m i ≠ 0 := by simpa only [not_exists, not_and] using hz
    let d : I → ℝ≥0 := fun i => if w i = 0 then 1 else m i
    have hd : ∀ i, d i ≠ 0 := by
      intro i
      by_cases hi : w i = 0
      · simp [d, hi]
      · simpa [d, hi] using hgood i hi
    let C : ℝ≥0 := ∏ i, d i ^ (w i : ℝ)
    have hnorm : ∑ a, q a * ∏ i, (f i a / d i) ^ (w i : ℝ) ≤ 1 := by
      calc
        _ ≤ ∑ a, q a * ((1 - ∑ i, w i) + ∑ i, w i * (f i a / d i)) := by
          apply Finset.sum_le_sum
          intro a ha
          simpa only [mul_comm] using mul_le_mul_left (nnreal_prod_rpow_le_affine w (fun i => f i a / d i) hw) (q a)
        _ = (1 - ∑ i, w i) + ∑ i, w i := by
          simp only [mul_add, Finset.sum_add_distrib, ← Finset.sum_mul, hq, one_mul]
          simp_rw [Finset.mul_sum]
          rw [Finset.sum_comm]
          congr 1
          apply Finset.sum_congr rfl
          intro i hi
          by_cases hwi : w i = 0
          · simp [hwi]
          · simp only [d, hwi, ite_false]
            simp_rw [div_eq_mul_inv]
            calc
              (∑ a, q a * (w i * (f i a * (m i)⁻¹))) =
                  w i * ((∑ a, q a * f i a) * (m i)⁻¹) := by
                simp only [Finset.mul_sum, Finset.sum_mul]
                apply Finset.sum_congr rfl
                intro a ha
                ac_rfl
              _ = w i := by
                change w i * (m i * (m i)⁻¹) = w i
                rw [mul_inv_cancel₀ (hgood i hwi), mul_one]
        _ = 1 := tsub_add_cancel_of_le hw
    have hprod (a : Ω) : (∏ i, f i a ^ (w i : ℝ)) =
        C * ∏ i, (f i a / d i) ^ (w i : ℝ) := by
      simp only [C, NNReal.div_rpow, ← Finset.prod_mul_distrib]
      apply Finset.prod_congr rfl
      intro i hi
      exact (mul_div_cancel₀ (f i a ^ (w i : ℝ))
        (by simp only [ne_eq, NNReal.rpow_eq_zero_iff]; exact fun h => hd i h.1)).symm
    calc
      _ = C * (∑ a, q a * ∏ i, (f i a / d i) ^ (w i : ℝ)) := by
        simp_rw [hprod]
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro a ha
        ac_rfl
      _ ≤ C * 1 := by simpa only [mul_comm] using mul_le_mul_left hnorm C
      _ = ∏ i, m i ^ (w i : ℝ) := by
        rw [mul_one]
        apply Finset.prod_congr rfl
        intro i hi
        by_cases hwi : w i = 0 <;> simp [d, hwi]


/-- A factor is determined by the listed coordinates. -/
def functionDependsOn {X A : Type} (S : Finset X) (f : (X → A) → ℝ≥0) : Prop :=
  ∀ a b, (∀ x ∈ S, a x = b x) → f a = f b

/-- Average one coordinate, keeping the other coordinates fixed. -/
noncomputable def coordinateAverage {X A : Type} [DecidableEq X] [Fintype A]
    (q : X → A → ℝ≥0) (x : X) (f : (X → A) → ℝ≥0) (a : X → A) : ℝ≥0 :=
  ∑ v, q x v * f (Function.update a x v)

/-- Iterated independent-coordinate averaging. -/
noncomputable def productAverage {X A : Type} [DecidableEq X] [Fintype A]
    (q : X → A → ℝ≥0) : List X → ((X → A) → ℝ≥0) → (X → A) → ℝ≥0
  | [], f => f
  | x :: xs, f => productAverage q xs (coordinateAverage q x f)

theorem functionDependsOn_update {X A : Type} [DecidableEq X]
    {S : Finset X} {f : (X → A) → ℝ≥0} (hf : functionDependsOn S f)
    {x : X} (hx : x ∉ S) (a : X → A) (v : A) :
    f (Function.update a x v) = f a := by
  apply hf
  intro y hy
  have hyx : y ≠ x := by intro h; exact hx (h ▸ hy)
  simp [Function.update_apply, hyx]

theorem functionDependsOn_coordinateAverage {X A : Type} [DecidableEq X] [Fintype A]
    (q : X → A → ℝ≥0) (x : X) {S : Finset X} {f : (X → A) → ℝ≥0}
    (hf : functionDependsOn S f) : functionDependsOn S (coordinateAverage q x f) := by
  intro a b hab
  apply Finset.sum_congr rfl
  intro v hv
  congr 1
  apply hf
  intro y hy
  by_cases hyx : y = x
  · simp [Function.update_apply, hyx]
  · simpa [Function.update_apply, hyx] using hab y hy

theorem coordinateAverage_eq_of_not_mem {X A : Type} [DecidableEq X] [Fintype A]
    (q : X → A → ℝ≥0) (hq : ∀ x, ∑ v, q x v = 1)
    {S : Finset X} {f : (X → A) → ℝ≥0} (hf : functionDependsOn S f)
    {x : X} (hx : x ∉ S) (a : X → A) : coordinateAverage q x f a = f a := by
  unfold coordinateAverage
  simp_rw [functionDependsOn_update hf hx]
  rw [← Finset.sum_mul, hq x, one_mul]

/-- The one-coordinate Finner step charges only factors incident to that coordinate. -/
theorem coordinateAverage_prod_rpow {X A I : Type}
    [DecidableEq X] [Fintype A] [Fintype I]
    (q : X → A → ℝ≥0) (hq : ∀ x, ∑ v, q x v = 1)
    (S : I → Finset X) (w : I → ℝ≥0)
    (f : I → (X → A) → ℝ≥0) (hf : ∀ i, functionDependsOn (S i) (f i))
    (x : X) (hload : (∑ i, if x ∈ S i then w i else 0) ≤ 1) (a : X → A) :
    coordinateAverage q x (fun a => ∏ i, f i a ^ (w i : ℝ)) a ≤
      ∏ i, coordinateAverage q x (f i) a ^ (w i : ℝ) := by
  classical
  let active : I → ℝ≥0 := fun i => if x ∈ S i then w i else 0
  let C : ℝ≥0 := ∏ i, if x ∈ S i then 1 else f i a ^ (w i : ℝ)
  have hfactor (v : A) : (∏ i, f i (Function.update a x v) ^ (w i : ℝ)) =
      C * ∏ i, f i (Function.update a x v) ^ (active i : ℝ) := by
    rw [← Finset.prod_mul_distrib]
    apply Finset.prod_congr rfl
    intro i hi
    by_cases hxi : x ∈ S i
    · simp [C, active, hxi]
    · simp [C, active, hxi, functionDependsOn_update (hf i) hxi]
  have hright : (∏ i, coordinateAverage q x (f i) a ^ (w i : ℝ)) =
      C * ∏ i, coordinateAverage q x (f i) a ^ (active i : ℝ) := by
    rw [← Finset.prod_mul_distrib]
    apply Finset.prod_congr rfl
    intro i hi
    by_cases hxi : x ∈ S i
    · simp [C, active, hxi]
    · simp [C, active, hxi, coordinateAverage_eq_of_not_mem q hq (hf i) hxi]
  rw [hright]
  change (∑ v, q x v * ∏ i, f i (Function.update a x v) ^ (w i : ℝ)) ≤ _
  simp_rw [hfactor]
  have hleft : (∑ v, q x v * (C * ∏ i, f i (Function.update a x v) ^ (active i : ℝ))) =
      C * ∑ v, q x v * ∏ i, f i (Function.update a x v) ^ (active i : ℝ) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro v hv
    ac_rfl
  rw [hleft]
  have hholder := nnreal_weightedHolder (q x) (hq x) active hload
    (fun i v => f i (Function.update a x v))
  simpa only [mul_comm] using mul_le_mul_left hholder C

theorem productAverage_mono {X A : Type} [DecidableEq X] [Fintype A]
    (q : X → A → ℝ≥0) (xs : List X) {f g : (X → A) → ℝ≥0}
    (hfg : ∀ a, f a ≤ g a) : ∀ a, productAverage q xs f a ≤ productAverage q xs g a := by
  induction xs generalizing f g with
  | nil => exact hfg
  | cons x xs ih =>
    apply ih
    intro a
    apply Finset.sum_le_sum
    intro v hv
    simpa only [mul_comm] using mul_le_mul_left (hfg (Function.update a x v)) (q x v)

/-- Finite product-space Finner inequality in iterated-coordinate expectation form.
No independence between overlapping factor events is required. -/
theorem finner_productAverage {X A I : Type}
    [DecidableEq X] [Fintype A] [Fintype I]
    (q : X → A → ℝ≥0) (hq : ∀ x, ∑ v, q x v = 1)
    (xs : List X) (S : I → Finset X) (w : I → ℝ≥0)
    (hload : ∀ x, (∑ i, if x ∈ S i then w i else 0) ≤ 1)
    (f : I → (X → A) → ℝ≥0) (hf : ∀ i, functionDependsOn (S i) (f i)) :
    ∀ a, productAverage q xs (fun a => ∏ i, f i a ^ (w i : ℝ)) a ≤
      ∏ i, productAverage q xs (f i) a ^ (w i : ℝ) := by
  induction xs generalizing f with
  | nil => intro a; exact le_rfl
  | cons x xs ih =>
    intro a
    change productAverage q xs (coordinateAverage q x (fun a => ∏ i, f i a ^ (w i : ℝ))) a ≤ _
    calc
      _ ≤ productAverage q xs (fun a => ∏ i, coordinateAverage q x (f i) a ^ (w i : ℝ)) a :=
        productAverage_mono q xs (coordinateAverage_prod_rpow q hq S w f hf x (hload x)) a
      _ ≤ ∏ i, productAverage q xs (coordinateAverage q x (f i)) a ^ (w i : ℝ) :=
        ih (fun i => coordinateAverage q x (f i))
          (fun i => functionDependsOn_coordinateAverage q x (hf i)) a

end UniversalLaw.General
