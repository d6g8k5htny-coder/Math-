import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.MeasureTheory.Constructions.BorelSpace.Real
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped NNReal ENNReal
namespace I4GaussianVarianceFloor

theorem gaussianPDFReal_le_of_variance_floor {a : ℝ} (ha : 0 < a)
    (m : ℝ) (v : ℝ≥0) (hav : a ≤ (v : ℝ)) (x : ℝ) :
    gaussianPDFReal m v x ≤ (Real.sqrt (2 * Real.pi * a))⁻¹ := by
  have hv : 0 < (v : ℝ) := lt_of_lt_of_le ha hav
  have hden : 0 < Real.sqrt (2 * Real.pi * a) := by positivity
  have hmono : Real.sqrt (2 * Real.pi * a) ≤ Real.sqrt (2 * Real.pi * v) := by
    apply Real.sqrt_le_sqrt
    exact mul_le_mul_of_nonneg_left hav (by positivity)
  have he : Real.exp (-(x-m)^2 / (2*(v:ℝ))) ≤ 1 :=
    Real.exp_le_one_iff.mpr (div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg _)) (by positivity))
  calc
    gaussianPDFReal m v x ≤ (Real.sqrt (2*Real.pi*v))⁻¹ * 1 :=
      mul_le_mul_of_nonneg_left he (by positivity)
    _ = (Real.sqrt (2*Real.pi*v))⁻¹ := mul_one _
    _ ≤ (Real.sqrt (2*Real.pi*a))⁻¹ := inv_anti₀ hden hmono

theorem gaussianReal_interval_mass_le_of_variance_floor {a : ℝ} (ha : 0 < a)
    (m : ℝ) (v : ℝ≥0) (hav : a ≤ (v : ℝ)) (t : ℝ) (ht : 0 ≤ t) :
    (gaussianReal m v).real (Icc (-t) t) ≤
      2 * (Real.sqrt (2*Real.pi*a))⁻¹ * t := by
  have hv : v ≠ 0 := by intro h; simp [h] at hav; linarith
  have hnn : 0 ≤ ∫ x in Icc (-t) t, gaussianPDFReal m v x :=
    integral_nonneg (fun x => gaussianPDFReal_nonneg m v x)
  have heq : (gaussianReal m v).real (Icc (-t) t) =
      ∫ x in Icc (-t) t, gaussianPDFReal m v x := by
    rw [measureReal_def, gaussianReal_apply_eq_integral m hv, ENNReal.toReal_ofReal hnn]
  rw [heq]
  have hconst : IntegrableOn (fun _ : ℝ => (Real.sqrt (2*Real.pi*a))⁻¹) (Icc (-t) t) :=
    continuous_const.integrableOn_Icc
  calc
    _ ≤ ∫ x in Icc (-t) t, (Real.sqrt (2*Real.pi*a))⁻¹ :=
      integral_mono ((integrable_gaussianPDFReal m v).restrict) hconst
        (fun x => gaussianPDFReal_le_of_variance_floor ha m v hav x)
    _ = 2 * (Real.sqrt (2*Real.pi*a))⁻¹ * t := by
      rw [setIntegral_const, smul_eq_mul, Real.volume_real_Icc_of_le (by linarith : -t ≤ t)]
      ring

end I4GaussianVarianceFloor
