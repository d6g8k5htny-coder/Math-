import Closure.Assembly
import Completion.Benchmark
import Completion.PaletteFormula

namespace UniversalLaw.P15Completion
open UniversalLaw.Spec.P15
open UniversalLaw.P15Closure
open scoped BigOperators

 theorem benchmark816_constant_price (hF : IsRealizedFamily benchmark816) (r : ℝ) :
    famPrice (fun _ => r) (fullBlockFamily benchmark816) = 6 * r ^ 409 := by
  rw [famPrice_fullBlockFamily benchmark816 hF]
  have hcard : ∀ i : Fin benchmark816.b, (block benchmark816 i).card = 409 := by
    intro i
    simpa [benchmark816] using hF.2.2.1 i
  simp only [genPrice, Finset.prod_const, hcard]
  change (∑ _i : Fin 6, r ^ 409) = _
  rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin]
  simp only [nsmul_eq_mul, Nat.cast_ofNat]

 theorem benchmark816_phi : phi (1 / 40900) = Real.log (40900 / 40899) := by
  have hu := Real.log_le_sub_one_of_pos (by norm_num : (0 : ℝ) < 40900 / 40899)
  have hlog : -Real.log (1 - (1 / 40900 : ℝ)) = Real.log (40900 / 40899) := by
    have hn : 1 - (1 / 40900 : ℝ) = (40900 / 40899 : ℝ)⁻¹ := by norm_num
    rw [hn, Real.log_inv, neg_neg]
  rw [phi, if_pos (by norm_num), hlog, min_eq_right]
  linarith

 theorem benchmark816_log_upper : Real.log (40900 / 40899) ≤ (1 / 40899 : ℝ) := by
  have h := Real.log_le_sub_one_of_pos (by norm_num : (0 : ℝ) < 40900 / 40899)
  norm_num at h ⊢
  exact h

 theorem benchmark816_rational_admissible :
    (81801 / 3345620000 : ℝ) < phi (1 / 40900) := by
  have h := Real.sum_range_le_log_div (by norm_num : (0 : ℝ) ≤ 1 / 81799)
    (by norm_num : (1 / 81799 : ℝ) < 1) 1
  norm_num at h
  rw [benchmark816_phi]
  linarith

 theorem benchmark816_price_of_realized (hF : IsRealizedFamily benchmark816) :
    Benchmark816Price := by
  refine ⟨?_, by positivity⟩
  rw [benchmark816_constant_price hF]
  simp only [one_div_pow]
  ring

 theorem benchmark816_rationalPrice_of_realized (hF : IsRealizedFamily benchmark816) :
    Benchmark816RationalPrice := by
  refine ⟨?_, by norm_num, benchmark816_rational_admissible, benchmark816_constant_price hF _⟩
  calc
    6 * Real.log (40900 / 40899) ^ 409 ≤ 6 * (1 / 40899 : ℝ) ^ 409 := by
      apply mul_le_mul_of_nonneg_left _ (by norm_num)
      exact pow_le_pow_left₀ (Real.log_nonneg (by norm_num)) benchmark816_log_upper 409
    _ = (6 : ℝ) / 40899 ^ 409 := by rw [one_div_pow]; ring

 theorem benchmark816_family_le_one (hF : IsRealizedFamily benchmark816)
    (c : Fin 6 × Fin 409 → ℝ)
    (hc : ∀ v, 0 ≤ c v ∧ c v ≤ Real.log (40900 / 40899)) :
    famPrice c (fullBlockFamily benchmark816) ≤ 1 := by
  have hprice : famPrice c (fullBlockFamily benchmark816) ≤ 6 * (1 / 40899 : ℝ) ^ 409 := by
    rw [← benchmark816_constant_price hF]
    apply Finset.sum_le_sum
    intro g hg
    exact Finset.prod_le_prod₀ (fun v _ => (hc v).1)
      (fun v _ => (hc v).2.trans benchmark816_log_upper)
  have hpow : (1 / 40899 : ℝ) ^ 409 ≤ 1 / 40899 := by
    calc
      _ = (1 / 40899 : ℝ) ^ 408 * (1 / 40899) := by rw [pow_succ]
      _ ≤ 1 * (1 / 40899 : ℝ) :=
        mul_le_mul_of_nonneg_right (pow_le_one₀ (by norm_num) (by norm_num)) (by norm_num)
      _ = _ := one_mul _
  exact hprice.trans ((mul_le_mul_of_nonneg_left hpow (by norm_num)).trans (by norm_num))

 theorem benchmark816_transformedRange_of_realized (hF : IsRealizedFamily benchmark816)
    (hcover : IsGeneratorCover benchmark816 816 (fullBlockFamily benchmark816))
    (hpal : paletteNumber benchmark816.b benchmark816.H benchmark816.d ≤ 816) :
    Benchmark816TransformedRange := by
  refine ⟨benchmark816_phi, hcover, ?_⟩
  intro c hc
  have hd : ∀ i, 2 ≤ benchmark816.d i := by intro i; change 2 ≤ 408; omega
  have hp : ∀ v : Fin 6 × Fin 409, 0 ≤ (1 / 40900 : ℝ) ∧ (1 / 40900 : ℝ) ≤ 1 / 4 := by
    intro v; norm_num
  have hp01 : ∀ v : Fin 6 × Fin 409, 0 ≤ (1 / 40900 : ℝ) ∧ (1 / 40900 : ℝ) ≤ 1 := by
    intro v; norm_num
  have hcp : ∀ v, 0 ≤ c v ∧ c v ≤ phi (1 / 40900) := by
    intro v; simpa only [benchmark816_phi] using hc v
  constructor
  · by_cases hmu : 0 < mu benchmark816 (fun _ => (1 : ℝ) / 40900)
    · rw [cappedHazard, if_pos hmu]
      refine le_min (benchmark816_family_le_one hF c hc) ?_
      have hlocal := restrictedLocalBudget benchmark816 hF hd (fun _ => (1 : ℝ) / 40900) c hp hcp
      have hglobal := (independentBlockHazard benchmark816 hF (fun _ => (1 : ℝ) / 40900) hp01).2 hmu
      rw [famPrice_fullBlockFamily benchmark816 hF]
      calc
        _ ≤ ∑ i, (16 / 27 : ℝ) * localFailure benchmark816 (fun _ => (1 : ℝ) / 40900) i :=
          Finset.sum_le_sum (fun i _ => (hlocal i).1)
        _ = (16 / 27 : ℝ) * ∑ i, localFailure benchmark816 (fun _ => (1 : ℝ) / 40900) i :=
          (Finset.mul_sum _ _ _).symm
        _ ≤ (16 / 27 : ℝ) * (-Real.log (mu benchmark816 (fun _ => (1 : ℝ) / 40900))) :=
          mul_le_mul_of_nonneg_left (hglobal.1.trans hglobal.2) (by norm_num)
    · rw [cappedHazard, if_neg hmu]
      exact benchmark816_family_le_one hF c hc
  · exact restrictedTransformedPriceBudget benchmark816 hF hd (fun _ => (1 : ℝ) / 40900) c
      hp hcp 816 hpal

/-- Exact original benchmark price target. -/
theorem benchmark816Price : Benchmark816Price :=
  benchmark816_price_of_realized benchmark816IsRealized

/-- Exact original benchmark transformed range target. -/
theorem benchmark816TransformedRange : Benchmark816TransformedRange := by
  have hP : IsPaletteFeasible benchmark816.b benchmark816.H benchmark816.d 816 := by
    change IsPaletteFeasible 6 (completeClutter 6 3) (fun _ => 408) 816
    apply completeClutter_palette_feasible_iff.mpr
    constructor
    · intro i; norm_num
    · norm_num
  have hpal : paletteNumber benchmark816.b benchmark816.H benchmark816.d ≤ 816 :=
    Nat.sInf_le hP
  exact benchmark816_transformedRange_of_realized benchmark816IsRealized
    (fullBlockCover_of_palette_feasible benchmark816 benchmark816IsRealized hP) hpal

/-- Exact original benchmark rational price target. -/
theorem benchmark816RationalPrice : Benchmark816RationalPrice :=
  benchmark816_rationalPrice_of_realized benchmark816IsRealized

end UniversalLaw.P15Completion

#print axioms UniversalLaw.P15Completion.benchmark816Price
#print axioms UniversalLaw.P15Completion.benchmark816RationalPrice

#print axioms UniversalLaw.P15Completion.benchmark816TransformedRange
