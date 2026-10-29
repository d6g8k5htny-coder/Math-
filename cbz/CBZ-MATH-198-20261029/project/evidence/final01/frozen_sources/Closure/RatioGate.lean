import Specifications.P15

/-!
An exact algebraic gate for the existing sufficient ratio test.  This file lives
outside the native search worker's import environment.  No cover theorem follows
from this calculation alone.
-/

namespace UniversalLaw.CertifiedFrontier

open UniversalLaw.Spec.P15

/-- Natural subtraction is harmless on the explicit capacity/demand domain. -/
theorem ratio_exponents (a d : ℕ) (ha : 1 ≤ a) (hd : 2 ≤ d) :
    1 ≤ a * d - a ∧ a * d + 1 ≤ 3 * (a * d - a) := by
  have had : 2 * a ≤ a * d := by
    simpa only [Nat.mul_comm] using Nat.mul_le_mul_left a hd
  omega

/-- Exact factorization; all powers have natural exponents. -/
theorem rhoTest_factor (a d : ℕ) (p : ℝ)
    (ha : 1 ≤ a) (hd : 2 ≤ d) (hp : p < 1) :
    rhoTest a d p =
      (p / (1 - p) ^ 3) ^ (a * d - a) *
        (1 - p) ^ (3 * (a * d - a) - (a * d + 1)) := by
  have hq : 1 - p ≠ 0 := ne_of_gt (sub_pos.mpr hp)
  have he := (ratio_exponents a d ha hd).2
  have hexp : a * d + 1 + (3 * (a * d - a) - (a * d + 1)) =
      3 * (a * d - a) := Nat.add_sub_of_le he
  have hpower : (1 - p) ^ (3 * (a * d - a)) =
      (1 - p) ^ (a * d + 1) *
        (1 - p) ^ (3 * (a * d - a) - (a * d + 1)) := by
    rw [← pow_add, hexp]
  unfold rhoTest
  rw [div_pow, ← pow_mul, hpower]
  field_simp

/-- Under the gate the pair a=1,d=2 is a uniform envelope, including p=0. -/
theorem rhoTest_envelope (a d : ℕ) (p : ℝ)
    (ha : 1 ≤ a) (hd : 2 ≤ d) (hp0 : 0 ≤ p) (hp1 : p < 1)
    (hgate : p ≤ (1 - p) ^ 3) :
    rhoTest a d p ≤ p / (1 - p) ^ 3 := by
  have hq0 : 0 < 1 - p := sub_pos.mpr hp1
  have hq1 : 1 - p ≤ 1 := by linarith
  have hr0 : 0 ≤ p / (1 - p) ^ 3 := div_nonneg hp0 (pow_nonneg hq0.le _)
  have hr1 : p / (1 - p) ^ 3 ≤ 1 := (div_le_one₀ (pow_pos hq0 _)).2 hgate
  have hn : a * d - a ≠ 0 := by
    have := (ratio_exponents a d ha hd).1
    omega
  rw [rhoTest_factor a d p ha hd hp1]
  calc
    _ ≤ (p / (1 - p) ^ 3) ^ (a * d - a) :=
      mul_le_of_le_one_right (pow_nonneg hr0 _) (pow_le_one₀ hq0.le hq1)
    _ ≤ p / (1 - p) ^ 3 := pow_le_of_le_one hr0 hr1 hn

/-- The exact uniform gate for this sufficient test, on its stated domain. -/
theorem rhoTest_uniform_iff (p : ℝ) (hp0 : 0 ≤ p) (hp1 : p < 1) :
    (∀ a d : ℕ, 1 ≤ a → 2 ≤ d → rhoTest a d p ≤ 1) ↔
      p ≤ (1 - p) ^ 3 := by
  constructor
  · intro h
    have h12 := h 1 2 (by omega) (by omega)
    have hq : 0 < (1 - p) ^ 3 := pow_pos (sub_pos.mpr hp1) _
    have hratio : p / (1 - p) ^ 3 ≤ 1 := by
      simpa [rhoTest] using h12
    exact (div_le_one₀ hq).1 hratio
  · intro hgate a d ha hd
    exact (rhoTest_envelope a d p ha hd hp0 hp1 hgate).trans
      ((div_le_one₀ (pow_pos (sub_pos.mpr hp1) _)).2 hgate)

/-- The zero endpoint is included in the theorem's domain. -/
theorem rhoTest_zero (a d : ℕ) (ha : 1 ≤ a) (hd : 2 ≤ d) :
    rhoTest a d 0 = 0 := by
  have hn : a * d - a ≠ 0 := by
    have := (ratio_exponents a d ha hd).1
    omega
  simp [rhoTest, hn]

/-- At one Lean's total division makes every ratio zero, outside the gate theorem. -/
theorem rhoTest_one_totalized (a d : ℕ) : rhoTest a d 1 = 0 := by
  simp [rhoTest]

/-- The strict upper domain bound cannot be replaced by p≤1. -/
theorem rhoTest_one_excluded :
    (∀ a d : ℕ, 1 ≤ a → 2 ≤ d → rhoTest a d 1 ≤ 1) ∧
      ¬ ((1 : ℝ) ≤ (1 - 1) ^ 3) := by
  constructor
  · intro a d _ _
    rw [rhoTest_one_totalized]
    norm_num
  · norm_num

end UniversalLaw.CertifiedFrontier

#print UniversalLaw.Spec.P15.rhoTest
#check UniversalLaw.CertifiedFrontier.ratio_exponents
#check UniversalLaw.CertifiedFrontier.rhoTest_factor
#check UniversalLaw.CertifiedFrontier.rhoTest_envelope
#check UniversalLaw.CertifiedFrontier.rhoTest_uniform_iff
#check UniversalLaw.CertifiedFrontier.rhoTest_zero
#check UniversalLaw.CertifiedFrontier.rhoTest_one_totalized
#check UniversalLaw.CertifiedFrontier.rhoTest_one_excluded
#print axioms UniversalLaw.CertifiedFrontier.ratio_exponents
#print axioms UniversalLaw.CertifiedFrontier.rhoTest_factor
#print axioms UniversalLaw.CertifiedFrontier.rhoTest_envelope
#print axioms UniversalLaw.CertifiedFrontier.rhoTest_uniform_iff
#print axioms UniversalLaw.CertifiedFrontier.rhoTest_zero
#print axioms UniversalLaw.CertifiedFrontier.rhoTest_one_totalized
#print axioms UniversalLaw.CertifiedFrontier.rhoTest_one_excluded
