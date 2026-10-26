import SourceConditionalMajorant

/-!+# Actual scalar curvature direction and full-carrier reconstruction

Every Gaussian law and independence assertion below comes from the literal
Fourier coefficients on the existing smooth sample carrier. See
SOURCE_CURVATURE_DECOMPOSITION.md. Author-side formal work is separate from
scientific review and geometric Palm identification.
-/

noncomputable section

open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceGaussian I4SourceCovariance
open I4SourceDerivativeGaussian I4SourceDerivativeContinuity I4SourceConfluentPins
open I4SourceConfluentLimits I4ContactCoefficientLimits I4SourceEndpointRegression
open I4SourceContact I4SourceSmoothConditional I4SourceConditionalMajorant I4ContactGram
open I4GaussianRegressionLimits MeasureTheory ProbabilityTheory Matrix Filter
open scoped BigOperators Topology NNReal

set_option autoImplicit false

namespace I4SourceCurvatureDecomposition

def curvatureCoefficient (L : ℝ) (m : SourceMode 2) : ℝ :=
  sourceContactCoefficient L 6 m

def curvatureCross (L r : ℝ) (i : Fin 6) : ℝ :=
  covariance (sourceContactQ L) (fun ω => sourceConfluentPinsAt L r ω i) (smoothLaw 2 L)

def curvatureBeta (L r : ℝ) : Fin 6 → ℝ :=
  curvatureCross L r ᵥ* (sourcePinCovarianceAt L r)⁻¹

def curvatureMean (L r : ℝ) (x : Fin 6 → ℝ) : ℝ := curvatureBeta L r ⬝ᵥ x

def curvatureVariance (L r : ℝ) : ℝ :=
  Var[sourceContactQ L; smoothLaw 2 L] - curvatureBeta L r ⬝ᵥ curvatureCross L r

def curvatureSigma (L r : ℝ) : ℝ := Real.sqrt (curvatureVariance L r)

def curvatureResidualCoefficient (L r : ℝ) (m : SourceMode 2) : ℝ :=
  curvatureCoefficient L m - ∑ i, curvatureBeta L r i * pinCoefficient L r i m

def curvatureDirection (L r : ℝ) (m : SourceMode 2) : ℝ :=
  curvatureResidualCoefficient L r m / curvatureSigma L r

def curvatureZ (L r : ℝ) (ω : SmoothSample 2 L) : ℝ :=
  scalarSeries (curvatureDirection L r) ω.val

theorem curvatureCoefficient_summable {L : ℝ} (hL : L ≠ 0) :
    Summable (curvatureCoefficient L) := sourceContactCoefficient_summable hL 6

theorem sourceContactQ_series {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    sourceContactQ L ω = scalarSeries (curvatureCoefficient L) ω.val :=
  smoothSourceField_derivative_series 2 hL ω 2 0 ![contactE1,contactE1]

theorem curvatureCoefficient_weighted_summable {L : ℝ} (hL : L ≠ 0)
    (ω : SmoothSample 2 L) :
    Summable (fun m => curvatureCoefficient L m * ω.val m) :=
  derivativeCoefficient_weighted_summable hL ω 2 0 ![contactE1,contactE1]

theorem curvatureCross_coefficient {L : ℝ} (hL : L ≠ 0) (r : ℝ) (i : Fin 6) :
    curvatureCross L r i = ∑' m, curvatureCoefficient L m * pinCoefficient L r i m := by
  unfold curvatureCross
  simp_rw [sourceContactQ_series hL, sourceConfluentPinsAt_series hL]
  change covariance (fun ω => scalarSeries (curvatureCoefficient L) (sampleInclusion 2 L ω))
    (fun ω => scalarSeries (pinCoefficient L r i) (sampleInclusion 2 L ω)) (smoothLaw 2 L) = _
  rw [covariance_comp_inclusion 2 hL _ _ (scalarSeries_measurable _) (scalarSeries_measurable _)]
  exact scalarSeries_covariance _ _ (curvatureCoefficient_summable hL) (pinCoefficient_summable hL r i)

theorem curvatureVariance_prior_coefficient {L : ℝ} (hL : L ≠ 0) :
    Var[sourceContactQ L; smoothLaw 2 L] = ∑' m, curvatureCoefficient L m * curvatureCoefficient L m := by
  rw [← sourceContactQVariance_eq_variance hL]
  change sourceContactCovariance L 6 6 = _
  rw [sourceContactCovariance_eq_coefficientGram hL]
  rfl

theorem curvatureResidualCoefficient_summable {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    Summable (curvatureResidualCoefficient L r) :=
  (curvatureCoefficient_summable hL).sub
    (summable_sum (fun i _ => (pinCoefficient_summable hL r i).mul_left _))

theorem curvatureDirection_summable {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    Summable (curvatureDirection L r) :=
  (curvatureResidualCoefficient_summable hL r).div_const _

theorem curvatureBeta_normal (L r : ℝ) (hG : IsUnit (sourcePinCovarianceAt L r)) :
    curvatureBeta L r ᵥ* sourcePinCovarianceAt L r = curvatureCross L r := by
  let _ : Invertible (sourcePinCovarianceAt L r) := hG.invertible
  rw [curvatureBeta, Matrix.vecMul_vecMul, Matrix.inv_mul_of_invertible, Matrix.vecMul_one]

end I4SourceCurvatureDecomposition
