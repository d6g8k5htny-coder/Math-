import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Sharp scalar Lagrange remainders. These new lemmas derive their Taylor
estimates from genuine smoothness and derivative bounds, with denominator
(n+1)!, rather than assuming a Taylor remainder or using the coarse n! bound. -/

noncomputable section
open Set
open scoped Nat
set_option autoImplicit false

namespace I4ActualQuarticTransfer

def scalarTaylor (g : ℝ → ℝ) (n : ℕ) (x : ℝ) : ℝ :=
  taylorWithinEval g n univ 0 x

private theorem scalarTaylor_eq_interval (g : ℝ → ℝ)
    (hg : ContDiff ℝ (⊤ : ℕ∞) g) (n : ℕ) (x : ℝ) (hx : 0 ≠ x) :
    scalarTaylor g n x = taylorWithinEval g n (uIcc 0 x) 0 x := by
  rw [scalarTaylor, taylor_within_apply, taylor_within_apply]
  apply Finset.sum_congr rfl
  intro k hk
  rw [iteratedDerivWithin_univ]
  have hkg : ContDiff ℝ k g := hg.of_le (by simp)
  rw [iteratedDerivWithin_eq_iteratedDeriv (uniqueDiffOn_uIcc hx)
    hkg.contDiffAt (left_mem_uIcc : (0 : ℝ) ∈ uIcc 0 x)]

/-- The sharp Lagrange factorial, valid on either side of the origin. -/
theorem scalar_taylor_remainder (g : ℝ → ℝ)
    (hg : ContDiff ℝ (⊤ : ℕ∞) g) (n : ℕ) (G : ℝ)
    (hG : ∀ y : ℝ, |iteratedDeriv (n+1) g y| ≤ G) (x : ℝ) :
    |g x - scalarTaylor g n x| ≤ G * |x| ^ (n+1) / (n+1)! := by
  by_cases hx : x = 0
  · subst x
    simp [scalarTaylor]
  have hnx : (0 : ℝ) ≠ x := Ne.symm hx
  have hgn : ContDiff ℝ (n+1) g := hg.of_le (by simp)
  obtain ⟨y,hy,heq⟩ := taylor_mean_remainder_lagrange_iteratedDeriv hnx hgn.contDiffOn
  rw [scalarTaylor_eq_interval g hg n x hnx, heq]
  simp only [sub_zero]
  calc
    _ = |iteratedDeriv (n+1) g y| * |x| ^ (n+1) / (n+1)! := by
      rw [abs_div, abs_mul, abs_pow, abs_of_nonneg (show 0 ≤ ((n+1)! : ℝ) from Nat.cast_nonneg _)]
    _ ≤ _ := div_le_div_of_nonneg_right
      (mul_le_mul_of_nonneg_right (hG y) (pow_nonneg (abs_nonneg x) _)) (Nat.cast_nonneg _)

theorem scalarTaylor_one (g : ℝ → ℝ) (x : ℝ) :
    scalarTaylor g 1 x = g 0 + x * deriv g 0 := by
  norm_num [scalarTaylor, taylor_within_apply, Finset.sum_range_succ,
    iteratedDerivWithin_univ, smul_eq_mul]

theorem scalarTaylor_three (g : ℝ → ℝ) (x : ℝ) :
    scalarTaylor g 3 x = g 0 + x * deriv g 0 +
      x^2 * iteratedDeriv 2 g 0 / 2 + x^3 * iteratedDeriv 3 g 0 / 6 := by
  norm_num [scalarTaylor, taylor_within_apply, Finset.sum_range_succ,
    iteratedDerivWithin_univ, smul_eq_mul]
  ring

theorem scalarTaylor_two (g : ℝ → ℝ) (x : ℝ) :
    scalarTaylor g 2 x = g 0 + x * deriv g 0 + x^2 * iteratedDeriv 2 g 0 / 2 := by
  norm_num [scalarTaylor, taylor_within_apply, Finset.sum_range_succ,
    iteratedDerivWithin_univ, smul_eq_mul]
  ring

theorem scalar_taylor_one_bound (g : ℝ → ℝ)
    (hg : ContDiff ℝ (⊤ : ℕ∞) g) (G : ℝ)
    (hG : ∀ y : ℝ, |iteratedDeriv 2 g y| ≤ G) (x : ℝ) :
    |g x - g 0 - x * deriv g 0| ≤ G * x^2 / 2 := by
  have hb := scalar_taylor_remainder g hg 1 G hG x
  rw [scalarTaylor_one] at hb
  norm_num only [Nat.reduceAdd, Nat.factorial_succ, Nat.factorial_zero, Nat.cast_ofNat] at hb
  rw [sq_abs] at hb
  convert hb using 1
  congr 1
  ring

theorem scalar_taylor_three_bound (g : ℝ → ℝ)
    (hg : ContDiff ℝ (⊤ : ℕ∞) g) (G : ℝ)
    (hG : ∀ y : ℝ, |iteratedDeriv 4 g y| ≤ G) (x : ℝ) :
    |g x - (g 0 + x * deriv g 0 + x^2 * iteratedDeriv 2 g 0 / 2 +
      x^3 * iteratedDeriv 3 g 0 / 6)| ≤ G * x^4 / 24 := by
  have hb := scalar_taylor_remainder g hg 3 G hG x
  rw [scalarTaylor_three] at hb
  norm_num only [Nat.reduceAdd, Nat.factorial_succ, Nat.factorial_zero, Nat.cast_ofNat] at hb
  have hpow : |x|^4 = x^4 := by rw [← abs_pow, abs_of_nonneg (by positivity : 0 ≤ x^4)]
  rw [hpow] at hb
  exact hb

theorem scalar_taylor_two_bound (g : ℝ → ℝ)
    (hg : ContDiff ℝ (⊤ : ℕ∞) g) (G : ℝ)
    (hG : ∀ y : ℝ, |iteratedDeriv 3 g y| ≤ G) (x : ℝ) :
    |g x - (g 0 + x * deriv g 0 + x^2 * iteratedDeriv 2 g 0 / 2)| ≤
      G * |x|^3 / 6 := by
  have hb := scalar_taylor_remainder g hg 2 G hG x
  rw [scalarTaylor_two] at hb
  norm_num only [Nat.reduceAdd, Nat.factorial_succ, Nat.factorial_zero, Nat.cast_ofNat] at hb
  exact hb

end I4ActualQuarticTransfer
