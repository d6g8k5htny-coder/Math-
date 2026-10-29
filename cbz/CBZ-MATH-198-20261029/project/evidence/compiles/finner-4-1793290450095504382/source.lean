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
          · simp only [d, hwi, if_false]
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
        by_cases hwi : w i = 0 <;> simp [C, d, hwi]

end UniversalLaw.General
