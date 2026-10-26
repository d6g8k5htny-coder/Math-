import SourceGapPinCurvature
import SourceCurvatureDecomposition

noncomputable section

open Set MeasureTheory ProbabilityTheory
open scoped NNReal

set_option autoImplicit false

namespace SourceCompactGapNormalizer

/-- A positive lower density on the fixed negative unit interval. -/
def gaussianCompactLowerConstant (V M : ℝ) : ℝ :=
  (Real.sqrt (4 * Real.pi * V))⁻¹ * Real.exp (-(2 + M)^2 / V)

theorem gaussianCompactLowerConstant_pos {V : ℝ} (M : ℝ) (hV : 0 < V) :
    0 < gaussianCompactLowerConstant V M := by
  unfold gaussianCompactLowerConstant
  positivity

/-- The prefactor uses the variance upper bound, and the exponent the lower bound. -/
theorem gaussianPDFReal_lower_compact (V M μ : ℝ) (ν : ℝ≥0)
    (hV : 0 < V) (hM : 0 ≤ M) (hμ : |μ| ≤ M)
    (hνlo : V / 2 ≤ (ν : ℝ)) (hνhi : (ν : ℝ) ≤ 2 * V)
    {x : ℝ} (hx : x ∈ Icc (-2 : ℝ) (-1)) :
    gaussianCompactLowerConstant V M ≤ gaussianPDFReal μ ν x := by
  have hνpos : 0 < (ν : ℝ) := by linarith
  have hxabs : |x| ≤ 2 := abs_le.mpr ⟨hx.1, by linarith [hx.2]⟩
  have hdist : |x - μ| ≤ 2 + M :=
    (abs_sub x μ).trans (add_le_add hxabs hμ)
  have hsq : (x - μ)^2 ≤ (2 + M)^2 := by
    nlinarith [sq_abs (x - μ), abs_nonneg (x - μ)]
  have hden : V ≤ 2 * (ν : ℝ) := by linarith
  have hquot : (x - μ)^2 / (2 * (ν : ℝ)) ≤ (2 + M)^2 / V :=
    (div_le_div_of_nonneg_right hsq (by positivity)).trans
      (div_le_div_of_nonneg_left (sq_nonneg (2 + M)) hV hden)
  have hexp : Real.exp (-(2 + M)^2 / V) ≤
      Real.exp (-(x - μ)^2 / (2 * (ν : ℝ))) := by
    apply Real.exp_le_exp.mpr
    simpa only [neg_div] using neg_le_neg hquot
  have hsqrt : Real.sqrt (2 * Real.pi * (ν : ℝ)) ≤
      Real.sqrt (4 * Real.pi * V) := by
    apply Real.sqrt_le_sqrt
    calc
      2 * Real.pi * (ν : ℝ) ≤ 2 * Real.pi * (2 * V) :=
        mul_le_mul_of_nonneg_left hνhi (by positivity)
      _ = 4 * Real.pi * V := by ring
  have hpref : (Real.sqrt (4 * Real.pi * V))⁻¹ ≤
      (Real.sqrt (2 * Real.pi * (ν : ℝ)))⁻¹ :=
    inv_anti₀ (by positivity) hsqrt
  exact mul_le_mul hpref hexp (by positivity) (by positivity)

/-- Integration of the lower PDF over an interval of length one. -/
theorem gaussianReal_Icc_lower_compact (V M μ : ℝ) (ν : ℝ≥0)
    (hV : 0 < V) (hM : 0 ≤ M) (hμ : |μ| ≤ M)
    (hνlo : V / 2 ≤ (ν : ℝ)) (hνhi : (ν : ℝ) ≤ 2 * V) :
    gaussianCompactLowerConstant V M ≤ (gaussianReal μ ν).real (Icc (-2 : ℝ) (-1)) := by
  have hνpos : 0 < (ν : ℝ) := by linarith
  have hνne : ν ≠ 0 := by
    intro h
    simpa [h] using hνpos
  have hnonneg : 0 ≤ ∫ x in Icc (-2 : ℝ) (-1), gaussianPDFReal μ ν x :=
    integral_nonneg (fun x => gaussianPDFReal_nonneg μ ν x)
  have heq : (gaussianReal μ ν).real (Icc (-2 : ℝ) (-1)) =
      ∫ x in Icc (-2 : ℝ) (-1), gaussianPDFReal μ ν x := by
    rw [measureReal_def, gaussianReal_apply_eq_integral μ hνne,
      ENNReal.toReal_ofReal hnonneg]
  have hconst : IntegrableOn (fun _ : ℝ => gaussianCompactLowerConstant V M)
      (Icc (-2 : ℝ) (-1)) := continuous_const.integrableOn_Icc
  rw [heq]
  calc
    gaussianCompactLowerConstant V M =
        ∫ x in Icc (-2 : ℝ) (-1), gaussianCompactLowerConstant V M := by
      rw [setIntegral_const, smul_eq_mul, Real.volume_real_Icc_of_le (by norm_num :
        (-2 : ℝ) ≤ -1)]
      norm_num
    _ ≤ ∫ x in Icc (-2 : ℝ) (-1), gaussianPDFReal μ ν x :=
      setIntegral_mono_on hconst ((integrable_gaussianPDFReal μ ν).restrict)
        measurableSet_Icc (fun x hx => gaussianPDFReal_lower_compact V M μ ν
          hV hM hμ hνlo hνhi hx)

end SourceCompactGapNormalizer
