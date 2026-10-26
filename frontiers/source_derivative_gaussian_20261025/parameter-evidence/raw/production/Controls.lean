import SourceSmoothParameterSpace

noncomputable section
open I4Foundation I4Weights I4Source I4Smooth I4SmoothCarrier
open I4SourceSmoothTopology I4SourceSmoothConditional I4SourceEndpointRegression
open I4SourcePinPreservingQuartic I4SourceSmoothParameterSpace
open MeasureTheory ProbabilityTheory TopologicalSpace
open scoped BigOperators Topology lp

set_option autoImplicit false

attribute [local instance] coherentBCFSemi coherentBCFAdd coherentBCFModule
attribute [local instance] coherentJetSemi coherentJetAdd coherentJetModule

local instance controlsParameterMeasurable : MeasurableSpace SmoothParameter := borel _
local instance controlsParameterBorel : BorelSpace SmoothParameter := ⟨rfl⟩

namespace I4SmoothParameterControls

/-- All six orders contribute to the constant mode's parameter normalization. -/
example (L : ℝ) : parameterWeight L none = 6 * Real.sqrt (1 / sourceZ 2 L) := by
  simp [parameterWeight,orderModeBound]

/-- The source condition is L≠0, not an implicit positive-L restriction. -/
example (m : SourceMode 2) : 0 < parameterWeight (-1) m :=
  parameterWeight_pos (by norm_num) m

/-- The actual zero carrier has zero parameter, including the infinite index set. -/
example (L : ℝ) : weightedCarrier L (zeroSample 2 L) = 0 := by
  ext m
  simp [weightedCarrier,zeroSample]

/-- A normalized one-mode parameter recovers that literal source mode exactly. -/
theorem single_parameter_recovers_mode {L : ℝ} (hL : L ≠ 0)
    (m : SourceMode 2) (x : Fin 2 → ℝ) :
    parameterField L (lp.single 1 m (parameterWeight L m)) x = modeCoefficient 2 L m x := by
  unfold parameterField weightedFourierField
  rw [tsum_eq_single m]
  · rw [lp.single_apply_self,div_self (parameterWeight_pos hL m).ne',one_mul]
  · intro n hn
    have hz : (lp.single 1 m (parameterWeight L m) : SmoothParameter) n = 0 :=
      lp.single_apply_ne (E := fun _ : SourceMode 2 => ℝ) 1 m (parameterWeight L m) hn
    change (lp.single 1 m (parameterWeight L m) : SmoothParameter) n /
      parameterWeight L n * modeCoefficient 2 L n x = 0
    rw [hz]
    simp

/-- Whole Banach jet operator norm, not individual point evaluation bounds. -/
example {L : ℝ} (hL : L ≠ 0) : ‖parameterJetCLM hL‖ ≤ 1 :=
  parameterJetCLM_norm_le hL

/-- Arbitrary parameters require only ℓ1 membership and genuinely yield C5. -/
example {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :
    ContDiff ℝ 5 (parameterField L a) := parameterField_contDiff hL a

/-- The physical gradient has finite C2 regularity, with no C∞ premise. -/
example {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :
    ContDiff ℝ 2 (gradientEuclidean (parameterField L a)) :=
  parameterGradientEuclidean_spatial_C2 hL a

/-- The derivative assignment is the literal derivative of the same field. -/
example {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) (x : Fin 2 → ℝ) :
    parameterGradientDerivativeBCF hL a x = fderiv ℝ (gradientPi (parameterField L a)) x :=
  parameterGradientDerivativeBCF_apply hL a x

/-- The physical Euclidean derivative is transported consistently as well. -/
example {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) (z : EuclideanSpace ℝ (Fin 2)) :
    parameterGradientEuclideanDerivativeBCF hL a z =
      fderiv ℝ (gradientEuclidean (parameterField L a)) z :=
  parameterGradientEuclideanDerivativeBCF_apply hL a z

/-- Banach and Polish properties have proved witnesses on the whole parameter. -/
example : CompleteSpace SmoothParameter := smoothParameter_complete
example : SeparableSpace SmoothParameter := smoothParameter_separable
example : PolishSpace SmoothParameter := smoothParameter_polish

/-- Norm functionals of the parameter use the norm Borel conditional law. -/
example {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hG : IsUnit (sourcePinCovarianceAt L r)) :
    HasCondDistrib (fun ω => ‖weightedCarrier L ω‖) (sourceConfluentPinsAt L r)
      ((sourceSmoothKernel hL r).map (fun ω => ‖weightedCarrier L ω‖)) (smoothLaw 2 L) :=
  weightedCarrier_functional_hasCondDistrib hL r hG (fun a => ‖a‖) continuous_norm.borel_measurable

end I4SmoothParameterControls
