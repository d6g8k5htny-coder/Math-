import Specifications.P15

namespace UniversalLaw.P15Completion

open UniversalLaw.Spec.P15

set_option maxHeartbeats 8000000
set_option maxRecDepth 10000

/-- The error is the sum of an exact rational discrepancy and Mathlib's
Taylor remainder. All instantiations below are proved by `norm_num`. -/
private theorem exp_certificate {x a : ℝ} (hx : |x| ≤ 1)
    (hc : |(∑ m ∈ Finset.range 26, x ^ m / m.factorial) - a| +
      |x| ^ 26 * ((27 : ℝ) / (Nat.factorial 26 * 26)) ≤ 1 / 10 ^ 24) :
    |Real.exp x - a| ≤ 1 / 10 ^ 24 := by
  have hb := Real.exp_bound hx (n := 26) (by norm_num)
  calc
    |Real.exp x - a| ≤
        |Real.exp x - (∑ m ∈ Finset.range 26, x ^ m / m.factorial)| +
          |(∑ m ∈ Finset.range 26, x ^ m / m.factorial) - a| := abs_sub_le _ _ _
    _ ≤ |x| ^ 26 * ((27 : ℝ) / (Nat.factorial 26 * 26)) +
          |(∑ m ∈ Finset.range 26, x ^ m / m.factorial) - a| :=
      add_le_add hb le_rfl
    _ ≤ 1 / 10 ^ 24 := by linarith [hc]

private theorem exp_one_certificate :
    |Real.exp 1 - 2.718281828459045235360287| ≤ 1 / 10 ^ 24 := by
  apply exp_certificate (by norm_num)
  norm_num [Finset.sum_range_succ]

private theorem exp_lower_half_certificate :
    |Real.exp ((3 - 1 / rhoStarLower) / 2) - 2.480896105317015427960665| ≤
      1 / 10 ^ 24 := by
  apply exp_certificate (by norm_num [rhoStarLower])
  norm_num [rhoStarLower, Finset.sum_range_succ]

private theorem exp_upper_half_certificate :
    |Real.exp ((3 - 1 / rhoStarUpper) / 2) - 2.480896105317015427978018| ≤
      1 / 10 ^ 24 := by
  apply exp_certificate (by norm_num [rhoStarUpper])
  norm_num [rhoStarUpper, Finset.sum_range_succ]

/-- Strict enclosure using degree-26 exponential Taylor certificates and monotonicity. -/
theorem rhoStarEnclosure : RhoStarEnclosure := by
  have he := abs_sub_le_iff.mp exp_one_certificate
  have hl := abs_sub_le_iff.mp exp_lower_half_certificate
  have hu := abs_sub_le_iff.mp exp_upper_half_certificate
  have hlExp : Real.exp (3 - 1 / rhoStarLower) < 3 * Real.exp 1 - 2 := by
    have hexp : Real.exp (3 - 1 / rhoStarLower) =
        Real.exp ((3 - 1 / rhoStarLower) / 2) ^ 2 := by
      calc
        Real.exp (3 - 1 / rhoStarLower) =
            Real.exp ((3 - 1 / rhoStarLower) / 2 + (3 - 1 / rhoStarLower) / 2) := by
          congr 1
          ring
        _ = Real.exp ((3 - 1 / rhoStarLower) / 2) ^ 2 := by
          rw [Real.exp_add, pow_two]
    rw [hexp]
    have hp := Real.exp_pos ((3 - 1 / rhoStarLower) / 2)
    nlinarith [sq_nonneg
      (Real.exp ((3 - 1 / rhoStarLower) / 2) -
        (2.480896105317015427960665 + 1 / 10 ^ 24))]
  have huExp : 3 * Real.exp 1 - 2 < Real.exp (3 - 1 / rhoStarUpper) := by
    have hexp : Real.exp (3 - 1 / rhoStarUpper) =
        Real.exp ((3 - 1 / rhoStarUpper) / 2) ^ 2 := by
      calc
        Real.exp (3 - 1 / rhoStarUpper) =
            Real.exp ((3 - 1 / rhoStarUpper) / 2 + (3 - 1 / rhoStarUpper) / 2) := by
          congr 1
          ring
        _ = Real.exp ((3 - 1 / rhoStarUpper) / 2) ^ 2 := by
          rw [Real.exp_add, pow_two]
    rw [hexp]
    have hp := Real.exp_pos ((3 - 1 / rhoStarUpper) / 2)
    nlinarith [sq_nonneg
      (Real.exp ((3 - 1 / rhoStarUpper) / 2) -
        (2.480896105317015427978018 - 1 / 10 ^ 24))]
  have hx : 0 < 3 * Real.exp 1 - 2 := by linarith [he.2]
  have hlLog := (Real.lt_log_iff_exp_lt hx).mpr hlExp
  have huLog := (Real.log_lt_iff_lt_exp hx).mpr huExp
  have hden : 0 < 3 - Real.log (3 * Real.exp 1 - 2) := by
    have hpos : 0 < 1 / rhoStarUpper := by norm_num [rhoStarUpper]
    linarith only [huLog, hpos]
  refine ⟨?_, ?_, ?_⟩
  · unfold rhoStar
    apply (lt_one_div (by norm_num [rhoStarLower]) hden).mpr
    linarith only [hlLog]
  · unfold rhoStar
    apply (one_div_lt hden (by norm_num [rhoStarUpper])).mpr
    linarith only [huLog]
  · norm_num [rhoStarUpper]

#print axioms rhoStarEnclosure

end UniversalLaw.P15Completion
