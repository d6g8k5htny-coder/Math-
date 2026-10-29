means=open('/workspace/scratch/regression-kernel/endpoint-parameters/means/Means.lean').read()
mbody=means[means.index('theorem smoothSourceField_derivative_integral_zero'):means.rindex('end EndpointMeans')]
cov=open('/workspace/scratch/regression-kernel/endpoint-parameters/covariance/ResidualCovariance.lean').read()
cbody=cov[cov.index('theorem sourceEndpointResidual_covariance'):cov.rindex('end EndpointParametersCovarianceProbe')]
ident=open('/workspace/scratch/regression-kernel/endpoint-parameters/Identification.lean').read()
ibody=ident[ident.index('lemma finiteGaussian_law_parameters'):ident.rindex('end I4SourceEndpointParameters')]
header='''import SourceEndpointRegression
import Mathlib.Probability.Distributions.Gaussian.Multivariate

/-!
# Actual canonical endpoint-kernel Gaussian parameters

Unconditional means are derived from the literal differentiated source series.
The residual covariance is derived from bilinearity and the actual regression
normal equations. Its Schur matrix is positive semidefinite because it is an
actual Gaussian covariance; no positivity premise is added.

At every pin the canonical kernel, transported from the Pi space to Euclidean
space, equals the literal `multivariateGaussian` with mean `C G⁻¹ x` and Schur
covariance. Singular residual covariance is retained. Current pin covariance
invertibility is explicit pending the separate covariance-limit join.
See `SOURCE_ENDPOINT_PARAMETERS.md` for the frozen source contract.
-/

noncomputable section

open I4Foundation I4Source I4SourceGaussian I4SmoothCarrier I4SourceDerivativeGaussian
open I4SourceConfluentPins I4SourceEndpointRegression ResearchFormalCoreR1
open MeasureTheory ProbabilityTheory Matrix WithLp
open scoped BigOperators Matrix RealInnerProductSpace

set_option autoImplicit false

namespace I4SourceEndpointParameters

'''
actual='''/-- The actual adjusted-endpoint Schur covariance. -/
def sourceEndpointSchurAt (L r : ℝ) : Matrix (Fin 6) (Fin 6) ℝ :=
  sourceEndpointCovarianceAt L r -
    sourceCrossCovarianceAt L r * (sourcePinCovarianceAt L r)⁻¹ * (sourceCrossCovarianceAt L r)ᵀ

/-- Gaussianity is inherited from the actual jointly Gaussian pin/endpoint vector. -/
theorem sourceEndpointResidual_hasGaussianLaw {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    HasGaussianLaw (sourceEndpointResidual L r) (smoothLaw 2 L) := by
  have hR := (regression_residual_jointGaussian (sourcePins_adjusted_hasGaussianLaw hL r)
    (sourceRegressionMapAt L r) 0 0).snd
  unfold sourceEndpointResidual
  simpa only [sub_zero] using hR

/-- A literal posterior sample at a prescribed pin. -/
def sourceEndpointPosterior (L r : ℝ) (x : Fin 6 → ℝ) (ω : SmoothSample 2 L) : Fin 6 → ℝ :=
  sourceEndpointResidual L r ω + sourceRegressionMapAt L r x

theorem sourceEndpointPosterior_hasGaussianLaw {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x : Fin 6 → ℝ) : HasGaussianLaw (sourceEndpointPosterior L r x) (smoothLaw 2 L) := by
  have hR := sourceEndpointResidual_hasGaussianLaw hL r
  refine ⟨hR.aemeasurable.add aemeasurable_const, ?_⟩
  have : IsGaussian ((smoothLaw 2 L).map (sourceEndpointResidual L r)) := hR.isGaussian_map
  convert (inferInstance : IsGaussian (((smoothLaw 2 L).map (sourceEndpointResidual L r)).map
    (fun v => v + sourceRegressionMapAt L r x))) using 1
  rw [AEMeasurable.map_map_of_aemeasurable (by fun_prop) hR.aemeasurable]
  rfl

theorem sourceEndpointPosterior_integral {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x : Fin 6 → ℝ) : (∫ ω, sourceEndpointPosterior L r x ω ∂smoothLaw 2 L) =
      sourceRegressionMapAt L r x := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  unfold sourceEndpointPosterior
  rw [integral_add (sourceEndpointResidual_hasGaussianLaw hL r).integrable (integrable_const _),
    sourceEndpointResidual_integral_zero hL r, integral_const, zero_add]

theorem sourceEndpointPosterior_covariance {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (x : Fin 6 → ℝ) (i j : Fin 6) :
    covariance (fun ω => sourceEndpointPosterior L r x ω i)
      (fun ω => sourceEndpointPosterior L r x ω j) (smoothLaw 2 L) =
      sourceEndpointSchurAt L r i j := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  have hR := sourceEndpointResidual_hasGaussianLaw hL r
  change covariance (fun ω => sourceEndpointResidual L r ω i + sourceRegressionMapAt L r x i)
    (fun ω => sourceEndpointResidual L r ω j + sourceRegressionMapAt L r x j) _ = _
  rw [covariance_add_const_left (hR.eval i).integrable,
    covariance_add_const_right (hR.eval j).integrable]
  exact sourceEndpointResidual_covariance hL r hG i j

/-- The canonical all-pin law is the literal posterior sampling map. -/
theorem sourceEndpointKernel_eq_map_posterior {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x : Fin 6 → ℝ) : sourceEndpointKernel L r x =
      (smoothLaw 2 L).map (sourceEndpointPosterior L r x) := by
  rw [sourceEndpointKernel_apply hL r x,
    AEMeasurable.map_map_of_aemeasurable (by fun_prop)
      (sourceEndpointResidual_hasGaussianLaw hL r).aemeasurable]
  rfl

theorem sourceEndpointKernel_isGaussian {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x : Fin 6 → ℝ) : IsGaussian (sourceEndpointKernel L r x) := by
  rw [sourceEndpointKernel_eq_map_posterior hL r x]
  exact (sourceEndpointPosterior_hasGaussianLaw hL r x).isGaussian_map

/-- Positive semidefiniteness follows from the actual residual covariance, including singular cases. -/
theorem sourceEndpointSchurAt_posSemidef {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) : (sourceEndpointSchurAt L r).PosSemidef := by
  exact (finiteGaussian_law_parameters (sourceEndpointPosterior_hasGaussianLaw hL r 0)
    (sourceRegressionMapAt L r 0) (sourceEndpointPosterior_integral hL r 0)
    (sourceEndpointSchurAt L r) (sourceEndpointPosterior_covariance hL r hG 0)).1

/-- Exact literal multivariate Gaussian law at every prescribed pin, with no residual PSD premise. -/
theorem sourceEndpointKernel_eq_multivariateGaussian {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (x : Fin 6 → ℝ) :
    (sourceEndpointKernel L r x).map (toLp 2) =
      multivariateGaussian (toLp 2 (sourceRegressionMapAt L r x)) (sourceEndpointSchurAt L r) := by
  rw [sourceEndpointKernel_eq_map_posterior hL r x,
    AEMeasurable.map_map_of_aemeasurable (by fun_prop)
      (sourceEndpointPosterior_hasGaussianLaw hL r x).aemeasurable]
  exact (finiteGaussian_law_parameters (sourceEndpointPosterior_hasGaussianLaw hL r x)
    (sourceRegressionMapAt L r x) (sourceEndpointPosterior_integral hL r x)
    (sourceEndpointSchurAt L r) (sourceEndpointPosterior_covariance hL r hG x)).2

/-- The original Pi-space kernel mean is the actual regression mean. -/
theorem sourceEndpointKernel_integral {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x : Fin 6 → ℝ) : (∫ v, v ∂sourceEndpointKernel L r x) = sourceRegressionMapAt L r x := by
  rw [sourceEndpointKernel_eq_map_posterior hL r x,
    integral_map (sourceEndpointPosterior_hasGaussianLaw hL r x).aemeasurable (by fun_prop)]
  exact sourceEndpointPosterior_integral hL r x

/-- The original Pi-space kernel covariance is the derived actual Schur covariance. -/
theorem sourceEndpointKernel_covariance {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (x : Fin 6 → ℝ) (i j : Fin 6) :
    covariance (fun v => v i) (fun v => v j) (sourceEndpointKernel L r x) =
      sourceEndpointSchurAt L r i j := by
  rw [sourceEndpointKernel_eq_map_posterior hL r x,
    covariance_map_fun (by fun_prop) (by fun_prop)
      (sourceEndpointPosterior_hasGaussianLaw hL r x).aemeasurable]
  exact sourceEndpointPosterior_covariance hL r hG x i j

'''
open('SourceEndpointParameters.lean','w').write(header+mbody+cbody+ibody+actual+'end I4SourceEndpointParameters\n')
