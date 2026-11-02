import AdaptiveFoldBoundaryPath

noncomputable section
namespace I4ActualFoldNumeric
open AdaptiveFoldBoundaryPath

structure NumericalBudget (T r κ : ℝ) : Prop where
  kappa_pos : 0 < κ
  c_pos : 0 < κ / 2
  radius_pos : 0 < 4 / Real.sqrt κ
  radius_le : 4 / Real.sqrt κ ≤ 1 / 8
  twice_T_le : 2 * T ≤ κ / 2
  strict_center : T < 2 * Real.sqrt κ
  rT_le : r * T ≤ 1 / 100
  slope_le : 6 * T / κ ≤ 1
  error_le : profileError (κ / 2) (3 * T) T ≤ 72 * T ^ 2 / κ
  curvature : 1 + profileError (κ / 2) (3 * T) T ≤ 2 - 3 * r * T
  capture : T / (κ / 2) ≤ 4 / Real.sqrt κ
  drop : 1 ≤ ((κ / 2) / 2) * (4 / Real.sqrt κ - T / (κ / 2)) ^ 2
  radius_curvature_eq : (κ / 2) * (4 / Real.sqrt κ) = 2 * Real.sqrt κ

theorem numerical_budget {T r κ : ℝ}
    (hT : 1 ≤ T) (hr : 0 < r)
    (hrT : r * T ^ 5 ≤ 1 / 100) (hκ : 1024 * T ^ 5 ≤ κ) :
    NumericalBudget T r κ := by
  have hT0 : 0 ≤ T := by linarith
  have hTpos : 0 < T := by linarith
  have hT5 : 1 ≤ T ^ 5 := one_le_pow₀ hT
  have hT15 : T ≤ T ^ 5 := by
    simpa using pow_le_pow_right₀ hT (show 1 ≤ 5 by norm_num)
  have hT25 : T ^ 2 ≤ T ^ 5 := pow_le_pow_right₀ hT (by norm_num)
  have hk : 0 < κ := by linarith
  have hc : 0 < κ / 2 := by positivity
  have hsqrt : 0 < Real.sqrt κ := Real.sqrt_pos.mpr hk
  have hsqrt0 : 0 ≤ Real.sqrt κ := le_of_lt hsqrt
  have hsqrt_sq : Real.sqrt κ ^ 2 = κ := Real.sq_sqrt (le_of_lt hk)
  have hroot : 32 * T ≤ Real.sqrt κ := by
    apply (sq_le_sq₀ (by positivity) hsqrt0).mp
    nlinarith
  have hTroot : T ≤ Real.sqrt κ := by linarith
  have hradius : 4 / Real.sqrt κ ≤ 1 / 8 := by
    apply (div_le_iff₀ hsqrt).mpr
    linarith
  have htwice : 2 * T ≤ κ / 2 := by nlinarith
  have hcenter : T < 2 * Real.sqrt κ := by linarith
  have hrT1 : r * T ≤ 1 / 100 := by
    exact (mul_le_mul_of_nonneg_left hT15 (le_of_lt hr)).trans hrT
  let s := 6 * T / κ
  have hs0 : 0 ≤ s := by dsimp [s]; positivity
  have hs1 : s ≤ 1 := by
    dsimp [s]
    apply (div_le_iff₀ hk).mpr
    nlinarith
  have hfirst : T * (2 * s + s ^ 2) ≤ 18 * T ^ 2 / κ := by
    calc
      T * (2 * s + s ^ 2) ≤ T * (3 * s) := by
        apply mul_le_mul_of_nonneg_left _ hT0
        nlinarith
      _ = 18 * T ^ 2 / κ := by dsimp [s]; ring
  have hsecond : (6 * T ^ 2 / κ) * (1 + s) ^ 2 ≤ 24 * T ^ 2 / κ := by
    calc
      (6 * T ^ 2 / κ) * (1 + s) ^ 2 ≤ (6 * T ^ 2 / κ) * 4 := by
        apply mul_le_mul_of_nonneg_left _ (by positivity)
        nlinarith
      _ = 24 * T ^ 2 / κ := by ring
  have herr_eq : profileError (κ / 2) (3 * T) T =
      T * (2 * s + s ^ 2) + (6 * T ^ 2 / κ) * (1 + s) ^ 2 := by
    dsimp [profileError, accelerationRadius, s]
    field_simp [hk.ne']
    <;> ring
  have herr42 : profileError (κ / 2) (3 * T) T ≤ 42 * T ^ 2 / κ := by
    rw [herr_eq]
    calc
      _ ≤ 18 * T ^ 2 / κ + 24 * T ^ 2 / κ := add_le_add hfirst hsecond
      _ = 42 * T ^ 2 / κ := by ring
  have herr72 : profileError (κ / 2) (3 * T) T ≤ 72 * T ^ 2 / κ := by
    exact herr42.trans (div_le_div_of_nonneg_right (by nlinarith [sq_nonneg T])
      (le_of_lt hk))
  have hquotient : T ^ 2 / κ ≤ 1 / 1024 := by
    apply (div_le_iff₀ hk).mpr
    nlinarith
  have hcurv : 1 + profileError (κ / 2) (3 * T) T ≤ 2 - 3 * r * T := by
    have heq : 42 * T ^ 2 / κ = 42 * (T ^ 2 / κ) := by ring
    rw [heq] at herr42
    nlinarith
  have hcap2 : T / (κ / 2) ≤ 2 / Real.sqrt κ := by
    apply (div_le_div_iff₀ hc hsqrt).mpr
    have hprod := mul_le_mul_of_nonneg_right hTroot hsqrt0
    nlinarith
  have hcap : T / (κ / 2) ≤ 4 / Real.sqrt κ := by
    apply hcap2.trans
    exact div_le_div_of_nonneg_right (by norm_num) hsqrt0
  have hdropbase : 2 / Real.sqrt κ ≤ 4 / Real.sqrt κ - T / (κ / 2) := by
    have hsplit : 4 / Real.sqrt κ = 2 / Real.sqrt κ + 2 / Real.sqrt κ := by ring
    linarith
  have hdrop0 : 0 ≤ 2 / Real.sqrt κ := by positivity
  have hdrop_sq : (2 / Real.sqrt κ) ^ 2 ≤
      (4 / Real.sqrt κ - T / (κ / 2)) ^ 2 := by
    exact (sq_le_sq₀ hdrop0 (hdrop0.trans hdropbase)).mpr hdropbase
  have hdrop_id : ((κ / 2) / 2) * (2 / Real.sqrt κ) ^ 2 = 1 := by
    field_simp [hsqrt.ne']
    nlinarith only [hsqrt_sq]
  have hdrop : 1 ≤ ((κ / 2) / 2) *
      (4 / Real.sqrt κ - T / (κ / 2)) ^ 2 := by
    rw [← hdrop_id]
    exact mul_le_mul_of_nonneg_left hdrop_sq (by positivity)
  have hrc : (κ / 2) * (4 / Real.sqrt κ) = 2 * Real.sqrt κ := by
    field_simp [hsqrt.ne']
    nlinarith only [hsqrt_sq]
  exact ⟨hk, hc, by positivity, hradius, htwice, hcenter, hrT1, hs1,
    herr72, hcurv, hcap, hdrop, hrc⟩

end I4ActualFoldNumeric
