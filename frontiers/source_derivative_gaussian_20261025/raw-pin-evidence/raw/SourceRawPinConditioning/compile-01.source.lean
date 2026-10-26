import SourceSmoothPalm
import Mathlib.LinearAlgebra.Matrix.ToLin

/-!
# Canonical whole-carrier conditioning on the literal raw six pins

Source: SOURCE_RAW_PIN_CONDITIONING.md, frozen before implementation.
The posterior is the literal raw coefficient covariance lift. Its equality
with the confluent posterior holds for every target and every carrier sample;
no almost-everywhere conditional-version uniqueness is evaluated at a null pin.
The physical weighted law is transported from the qualified source estimates.
This module does not formalize Kac–Rice or define a synthetic geometric count.

OpenAI author-side work by /root/palm_measure_transfer. Coordinate-change
algebra reuses its checked RawConfluentLift.lean scratch companion.
-/

noncomputable section
open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceGaussian I4SourceCovariance
open I4SourceDerivativeGaussian I4SourceConfluentPins I4SourceConfluentLimits
open I4SourceEndpointRegression I4SourceEndpointEstimates I4SourceSmoothConditional
open I4SourceSmoothPalm ResearchFormalCoreR1 MeasureTheory ProbabilityTheory Matrix Filter
open scoped BigOperators Matrix Topology
set_option autoImplicit false

namespace I4SourceRawPinConditioning

/-- The actual first six rows of the existing twelve-derivative source. -/
def rawPinCoefficient (L r : ℝ) (i : Fin 6) (m : SourceMode 2) : ℝ :=
  rawDerivativeCoefficient L r (Fin.castAdd 6 i) m

theorem rawPinCoefficient_summable {L : ℝ} (hL : L ≠ 0) (r : ℝ) (i : Fin 6) :
    Summable (rawPinCoefficient L r i) :=
  derivativeCoefficient_summable 2 hL (rawDerivativeOrder (Fin.castAdd 6 i))
    (rawDerivativePoint r (Fin.castAdd 6 i)) (rawDerivativeDirections (Fin.castAdd 6 i))

theorem rawPins_series {L : ℝ} (hL : L ≠ 0) (r : ℝ) (ω : SmoothSample 2 L) :
    rawPins L r ω =
      fun i => scalarSeries (rawPinCoefficient L r i) (sampleInclusion 2 L ω) := by
  funext i
  have h := congrFun (rawPinsWithHessians_series hL r ω) (Fin.castAdd 6 i)
  have hfirst : rawPinsWithHessians L r ω (Fin.castAdd 6 i) = rawPins L r ω i := by
    fin_cases i <;> rfl
  exact hfirst.symm.trans h

theorem rawPins_measurable {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    Measurable (rawPins L r) := by
  have heq : rawPins L r = fun ω i =>
      scalarSeries (rawPinCoefficient L r i) (sampleInclusion 2 L ω) :=
    funext (rawPins_series hL r)
  rw [heq]
  exact Measurable.of_eval (fun i =>
    (scalarSeries_measurable _).comp (sampleInclusion_measurable 2 L))

/-- Literal covariance of the actual raw observation; the Gram identity is proved below. -/
def rawPinCovariance (L r : ℝ) : Matrix (Fin 6) (Fin 6) ℝ :=
  fun i j => covariance (fun ω => rawPins L r ω i)
    (fun ω => rawPins L r ω j) (smoothLaw 2 L)

theorem rawPinCovariance_coefficient {L : ℝ} (hL : L ≠ 0) (r : ℝ) (i j : Fin 6) :
    rawPinCovariance L r i j =
      ∑' m, rawPinCoefficient L r i m * rawPinCoefficient L r j m := by
  unfold rawPinCovariance
  simp_rw [rawPins_series hL]
  rw [covariance_comp_inclusion 2 hL _ _ (scalarSeries_measurable _)
    (scalarSeries_measurable _)]
  exact I4SourceCovariance.scalarSeries_covariance _ _
    (rawPinCoefficient_summable hL r i) (rawPinCoefficient_summable hL r j)

/-- Matrix of the already proved raw-to-confluent continuous linear equivalence. -/
def confluentMatrix (r : ℝ) (hr : r ≠ 0) : Matrix (Fin 6) (Fin 6) ℝ :=
  LinearMap.toMatrix' (confluentEquiv r hr).toLinearEquiv.toLinearMap

theorem confluentMatrix_mulVec (r : ℝ) (hr : r ≠ 0) (v : Fin 6 → ℝ) :
    confluentMatrix r hr *ᵥ v = confluentTransform r v :=
  LinearMap.toMatrix'_mulVec (confluentEquiv r hr).toLinearEquiv.toLinearMap v

theorem confluentMatrix_isUnit (r : ℝ) (hr : r ≠ 0) : IsUnit (confluentMatrix r hr) := by
  apply LinearMap.isUnit_toMatrix'_iff.mpr
  exact (Module.End.isUnit_iff _).mpr (confluentEquiv r hr).bijective

theorem pinCoefficient_eq_confluentMatrix (L r : ℝ) (hr : r ≠ 0) (m : SourceMode 2) :
    (fun i => pinCoefficient L r i m) =
      confluentMatrix r hr *ᵥ (fun i => rawPinCoefficient L r i m) := by
  rw [confluentMatrix_mulVec]
  rfl

theorem sourceConfluentPinsAt_eq_matrix (L r : ℝ) (hr : r ≠ 0)
    (ω : SmoothSample 2 L) :
    sourceConfluentPinsAt L r ω = confluentMatrix r hr *ᵥ rawPins L r ω := by
  rw [confluentMatrix_mulVec]
  rfl

/-- The literal raw covariance correction, retaining every target component. -/
def rawPinLift (L r : ℝ) (y : Fin 6 → ℝ) (m : SourceMode 2) : ℝ :=
  ∑ i, rawPinCoefficient L r i m * (((rawPinCovariance L r)⁻¹ *ᵥ y) i)

theorem rawPinLift_goodSample {L : ℝ} (hL : L ≠ 0) (r : ℝ) (y : Fin 6 → ℝ) :
    goodSample 2 L (rawPinLift L r y) := by
  intro n
  have hprod (i : Fin 6) : Summable (fun m =>
      orderModeBound n 2 L m * |rawPinCoefficient L r i m|) :=
    coefficient_product_summable (orderModeBound_summable n 2 hL)
      (rawPinCoefficient_summable hL r i).abs
  have hs : Summable (fun m => ∑ i,
      (orderModeBound n 2 L m * |rawPinCoefficient L r i m|) *
        |((rawPinCovariance L r)⁻¹ *ᵥ y) i|) :=
    summable_sum (fun i _ => (hprod i).mul_right _)
  apply Summable.of_nonneg_of_le (fun m =>
    mul_nonneg (orderModeBound_nonneg n 2 L m) (abs_nonneg _)) _ hs
  intro m
  calc
    _ ≤ orderModeBound n 2 L m *
        ∑ i, |rawPinCoefficient L r i m * (((rawPinCovariance L r)⁻¹ *ᵥ y) i)| :=
      mul_le_mul_of_nonneg_left (Finset.abs_sum_le_sum_abs _ _) (orderModeBound_nonneg n 2 L m)
    _ = _ := by simp only [abs_mul, Finset.mul_sum, mul_assoc]

theorem rawPinLift_measurable (L r : ℝ) : Measurable (rawPinLift L r) := by
  apply Measurable.of_eval
  intro m
  unfold rawPinLift
  fun_prop

/-- This map is the actual raw coefficient regression, not a chosen value on a raw fiber. -/
def rawPosteriorSample {L : ℝ} (hL : L ≠ 0) (r : ℝ) (t : Fin 6 → ℝ)
    (ω : SmoothSample 2 L) : SmoothSample 2 L :=
  ⟨sampleInclusion 2 L ω + rawPinLift L r (t - rawPins L r ω),
    goodSample_add _ _ ω.property (rawPinLift_goodSample hL r _)⟩

theorem rawPosteriorSample_val {L : ℝ} (hL : L ≠ 0) (r : ℝ) (t : Fin 6 → ℝ)
    (ω : SmoothSample 2 L) (m : SourceMode 2) :
    (rawPosteriorSample hL r t ω).val m =
      ω.val m + rawPinLift L r (t - rawPins L r ω) m := rfl

theorem rawPosteriorSample_measurable {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    Measurable (fun p : (Fin 6 → ℝ) × SmoothSample 2 L => rawPosteriorSample hL r p.1 p.2) := by
  unfold rawPosteriorSample
  apply Measurable.subtype_mk
  exact ((sampleInclusion_measurable 2 L).comp measurable_snd).add
    ((rawPinLift_measurable L r).comp
      (measurable_fst.sub ((rawPins_measurable hL r).comp measurable_snd)))

end I4SourceRawPinConditioning
