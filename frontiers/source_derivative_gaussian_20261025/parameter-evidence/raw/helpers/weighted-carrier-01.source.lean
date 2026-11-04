import SourceSmoothTopology
import SourcePinCurvatureBounds
import Mathlib.Analysis.Normed.Lp.lpSpace

noncomputable section
open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceSmoothTopology
open I4SourceConditionalMajorant I4SourcePinCurvatureBounds MeasureTheory
open scoped BigOperators Topology lp

set_option autoImplicit false

namespace I4SourceSmoothParameterSpace

def parameterWeight (L : ℝ) (m : SourceMode 2) : ℝ :=
  ∑ k : Fin 6, orderModeBound k 2 L m

abbrev SmoothParameter := ℓ¹(SourceMode 2, ℝ)

theorem parameterWeight_nonneg (L : ℝ) (m : SourceMode 2) : 0 ≤ parameterWeight L m :=
  Finset.sum_nonneg (fun k _ => orderModeBound_nonneg k 2 L m)

theorem parameterWeight_mul_abs_summable (L : ℝ) (ω : SmoothSample 2 L) :
    Summable (fun m => parameterWeight L m * |ω.val m|) := by
  have h := summable_sum (fun k (_ : k ∈ (Finset.univ : Finset (Fin 6))) => ω.property k)
  simpa only [parameterWeight, Finset.sum_mul] using h

theorem weightedCarrier_memℓp (L : ℝ) (ω : SmoothSample 2 L) :
    Memℓp (fun m => parameterWeight L m * ω.val m) 1 := by
  apply memℓp_gen
  simpa only [ENNReal.toReal_one, Real.rpow_one, Real.norm_eq_abs, abs_mul,
    abs_of_nonneg (parameterWeight_nonneg L _)] using parameterWeight_mul_abs_summable L ω

def weightedCarrier (L : ℝ) (ω : SmoothSample 2 L) : SmoothParameter :=
  ⟨fun m => parameterWeight L m * ω.val m, weightedCarrier_memℓp L ω⟩

@[simp] theorem weightedCarrier_apply (L : ℝ) (ω : SmoothSample 2 L) (m : SourceMode 2) :
    weightedCarrier L ω m = parameterWeight L m * ω.val m := rfl

theorem weightedCarrier_norm (L : ℝ) (ω : SmoothSample 2 L) :
    ‖weightedCarrier L ω‖ = ∑ k : Fin 6, sourceDerivativeMajorant L k ω := by
  rw [lp.norm_eq_tsum_rpow (by norm_num : (0 : ℝ) < (1 : ℝ≥0∞).toReal)]
  simp only [ENNReal.toReal_one, Real.rpow_one, div_one, weightedCarrier_apply,
    Real.norm_eq_abs, abs_mul, abs_of_nonneg (parameterWeight_nonneg L _)]
  simp only [parameterWeight, Finset.sum_mul, sourceDerivativeMajorant, sampleMajorant]
  exact tsum_finsetSum (fun k _ => ω.property k)

theorem weightedCarrier_norm_eq_radius_sub_one (L : ℝ) (ω : SmoothSample 2 L) :
    ‖weightedCarrier L ω‖ = sourceGammaRadius L ω - 1 := by
  rw [weightedCarrier_norm]
  simp [sourceGammaRadius]

theorem weightedCarrier_stronglyMeasurable (L : ℝ) : StronglyMeasurable (weightedCarrier L) := by
  apply stronglyMeasurable_of_countable_hasSum
    (fun m (ω : SmoothSample 2 L) => lp.single (1 : ℝ≥0∞) m (parameterWeight L m * ω.val m))
  · intro m
    exact (lp.singleContinuousLinearMap ℝ (fun _ : SourceMode 2 => ℝ) 1 m).continuous.comp_stronglyMeasurable
      ((((measurable_pi_apply m).comp measurable_subtype_coe).const_mul _).stronglyMeasurable)
  · intro ω
    exact lp.hasSum_single (by simp) (weightedCarrier L ω)

theorem weightedCarrier_borel (L : ℝ) :
    @Measurable (SmoothSample 2 L) SmoothParameter _ (borel _) (weightedCarrier L) := by
  borelize SmoothParameter
  exact (weightedCarrier_stronglyMeasurable L).measurable

theorem smoothParameter_complete : CompleteSpace SmoothParameter := inferInstance

end I4SourceSmoothParameterSpace
