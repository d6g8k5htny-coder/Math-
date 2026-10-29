import SourceSmoothTopology
import Mathlib.Analysis.Normed.Lp.lpHolder

noncomputable section
open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceSmoothTopology
open MeasureTheory Filter BoundedContinuousFunction TopologicalSpace
open scoped BigOperators Topology lp

set_option autoImplicit false

namespace I4SourceSmoothParameterSpace

abbrev Parameter := ℓ¹(SourceMode 2, ℝ)

theorem parameter_abs_summable (a : Parameter) : Summable (fun m => |a m|) := by
  simpa using (lp.memℓp a).summable

def weightedFourierField (L : ℝ) (w : SourceMode 2 → ℝ) (a : Parameter)
    (x : Fin 2 → ℝ) : ℝ := ∑' m, (a m / w m) * modeCoefficient 2 L m x

theorem weighted_mode_derivative_bound {L : ℝ} (hL : L ≠ 0)
    (w : SourceMode 2 → ℝ) (hw : ∀ m, 0 < w m)
    (hdom : ∀ k ≤ 5, ∀ m, orderModeBound k 2 L m ≤ w m)
    (a : Parameter) (k : ℕ) (hk : k ≤ 5) (m : SourceMode 2) (x : Fin 2 → ℝ) :
    ‖iteratedFDeriv ℝ k (fun y => (a m / w m) * modeCoefficient 2 L m y) x‖ ≤ |a m| := by
  have heq : (fun y => (a m / w m) * modeCoefficient 2 L m y) =
      (a m / w m) • modeCoefficient 2 L m := by
    ext y
    simp only [Pi.smul_apply,smul_eq_mul]
  rw [heq,iteratedFDeriv_const_smul_apply (modeCoefficient_contDiff 2 L m k).contDiffAt,
    norm_smul,Real.norm_eq_abs,abs_div,abs_of_pos (hw m)]
  calc
    _ ≤ (|a m| / w m) * w m := mul_le_mul_of_nonneg_left
      ((modeCoefficient_iteratedFDeriv_order_bound 2 hL m k x).trans (hdom k hk m))
      (div_nonneg (abs_nonneg _) (hw m).le)
    _ = |a m| := div_mul_cancel₀ _ (hw m).ne'

/-- Arbitrary parameters have genuine C5 fields; no all-order smooth carrier
property is inferred or assumed. -/
theorem weightedFourierField_contDiff {L : ℝ} (hL : L ≠ 0)
    (w : SourceMode 2 → ℝ) (hw : ∀ m, 0 < w m)
    (hdom : ∀ k ≤ 5, ∀ m, orderModeBound k 2 L m ≤ w m) (a : Parameter) :
    ContDiff ℝ 5 (weightedFourierField L w a) := by
  apply contDiff_tsum (v := fun _ m => |a m|)
  · intro m
    exact contDiff_const.mul (modeCoefficient_contDiff 2 L m 5)
  · intro _ _
    exact parameter_abs_summable a
  · intro k m x hk
    have hk' : k ≤ 5 := by exact_mod_cast hk
    exact weighted_mode_derivative_bound hL w hw hdom a k hk' m x

theorem weightedFourierField_derivative {L : ℝ} (hL : L ≠ 0)
    (w : SourceMode 2 → ℝ) (hw : ∀ m, 0 < w m)
    (hdom : ∀ k ≤ 5, ∀ m, orderModeBound k 2 L m ≤ w m)
    (a : Parameter) (k : ℕ) (hk : k ≤ 5) (x : Fin 2 → ℝ) :
    iteratedFDeriv ℝ k (weightedFourierField L w a) x =
      ∑' m, (a m / w m) • iteratedFDeriv ℝ k (modeCoefficient 2 L m) x := by
  have hf (m : SourceMode 2) :
      ContDiff ℝ (5 : ℕ∞) (fun y => (a m / w m) * modeCoefficient 2 L m y) :=
    contDiff_const.mul (modeCoefficient_contDiff 2 L m 5)
  have hmajor (j : ℕ) (_ : (j : ℕ∞) ≤ 5) : Summable (fun m => |a m|) :=
    parameter_abs_summable a
  have hbound (j : ℕ) (m : SourceMode 2) (y : Fin 2 → ℝ) (hj : (j : ℕ∞) ≤ 5) :
      ‖iteratedFDeriv ℝ j (fun z => (a m / w m) * modeCoefficient 2 L m z) y‖ ≤ |a m| :=
    weighted_mode_derivative_bound hL w hw hdom a j (by exact_mod_cast hj) m y
  have hd := iteratedFDeriv_tsum_apply hf hmajor hbound (k := k) (by exact_mod_cast hk) x
  change iteratedFDeriv ℝ k (fun y => ∑' m, (a m / w m) * modeCoefficient 2 L m y) x = _
  rw [hd]
  apply tsum_congr
  intro m
  have heq : (fun y => (a m / w m) * modeCoefficient 2 L m y) =
      (a m / w m) • modeCoefficient 2 L m := by ext y; simp
  rw [heq,iteratedFDeriv_const_smul_apply (modeCoefficient_contDiff 2 L m k).contDiffAt]

end I4SourceSmoothParameterSpace
