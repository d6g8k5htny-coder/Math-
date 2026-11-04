import SourceEndpointHessianGaussian
import Lean.Elab.Tactic.Omega

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix Topology
open I4Foundation I4Source I4Weights I4SmoothCarrier I4SourceDerivativeGaussian
open I4SourceConfluentPins I4SourceConfluentLimits I4SourceRawPinConditioning
open I4SourceFinitePinKernel I4SourceRemoteJetGaussian I4SourceEndpointHessianWitness
open I4SourceEndpointHessianGaussian MeasureTheory ProbabilityTheory WithLp

namespace EndpointHessianGaussianControls

/-- Literal ordinary raw rows, with no mixed derivative factor. -/
theorem literal_observation_order (L r : ℝ) (ω : SmoothSample 2 L) :
    endpointHessian L r 0 ω = ![rawPinsWithHessians L r ω 6,
      rawPinsWithHessians L r ω 7,rawPinsWithHessians L r ω 8] ∧
    endpointHessian L r 1 ω = ![rawPinsWithHessians L r ω 9,
      rawPinsWithHessians L r ω 10,rawPinsWithHessians L r ω 11] := by
  constructor <;> ext j <;> fin_cases j <;> rfl

/-- Ordinary symmetric2×2 determinant uses exactly the square of the mixed entry. -/
theorem ordinary_determinant_formula (H : Fin 3 → ℝ) :
    Matrix.det (![![H 0,H 1],![H 1,H 2]] : Matrix (Fin 2) (Fin 2) ℝ) = H 0*H 2-(H 1)^2 := by
  rw [Matrix.det_fin_two]
  ring

/-- A nonzero mixed entry detects the incorrect omission or factor on XY. -/
theorem determinant_mixed_example :
    Matrix.det (![![1,2],![2,3]] : Matrix (Fin 2) (Fin 2) ℝ) = -1 ∧
    (1:ℝ)*3-2^2 = -1 ∧ (1:ℝ)*1-0^2 = 1 := by
  norm_num [Matrix.det_fin_two]

/-- Signed period/repeated-pin radius: only the defined sampling law is asserted. -/
theorem negative_period_zero_radius_law (e : Fin 2) :
    (rawPinKernel (L := -2) (by norm_num) 0 ![1,2,3,4,5,6]).map
      (fun ω => toLp 2 (endpointHessian (-2) 0 e ω)) =
      multivariateGaussian (toLp 2 (endpointHessianMean (-2) 0 e ![1,2,3,4,5,6]))
        (endpointHessianCovariance (-2) 0 e) :=
  rawPinKernel_endpointHessian_eq_multivariateGaussian (by norm_num) 0 e _

/-- Both endpoint means retain the selected full49 target mean. -/
theorem selected_means (L r : ℝ) (t : Fin 6 → ℝ) :
    endpointHessianMean L r 0 t = ![remotePosteriorMean L r (endpointM r) t 3,
      remotePosteriorMean L r (endpointM r) t 4,remotePosteriorMean L r (endpointM r) t 5] ∧
    endpointHessianMean L r 1 t = ![remotePosteriorMean L r (endpointS r) t 3,
      remotePosteriorMean L r (endpointS r) t 4,remotePosteriorMean L r (endpointS r) t 5] := by
  constructor <;> ext j <;> fin_cases j <;> rfl

/-- The actual covariance is the target-free principal3..5 Gram block. -/
theorem selected_covariances (L r : ℝ) (e : Fin 2) (j k : Fin 3) :
    endpointHessianCovariance L r e j k =
      remoteResidualCovariance L r (![endpointM r,endpointS r] e) (![3,4,5] j) (![3,4,5] k) := rfl

private theorem separated_2_1 :
    I4Torus.torusProjection 2 2 (endpointM 1) ≠ I4Torus.torusProjection 2 2 (endpointS 1) := by
  intro h
  have hz : (((endpointM 1 0-endpointS 1 0):ℝ):AddCircle (2:ℝ)) = 0 := by
    rw [AddCircle.coe_sub,sub_eq_zero]
    exact congrFun h 0
  obtain ⟨n,hn⟩ := (AddCircle.coe_eq_zero_iff (p:=(2:ℝ))).mp hz
  norm_num [endpointM,endpointS,zsmul_eq_mul] at hn
  have hnZ : n*(2:ℤ)= -1 := by exact_mod_cast hn
  omega

/-- The concrete selected3×6 raw correction consumes50 at its actual49 matrix. -/
theorem selected_regression_Gram_posDef (e : Fin 2) :
    (I4ContactGram.coefficientGram (I4SourceFinitePinKernel.residualCoefficient
      (rawPinCoefficient 2 1) (endpointHessianCoefficient 2 1 e)
      (fun j a => remoteRegressionMatrix 2 1 (![endpointM 1,endpointS 1] e) (![3,4,5] j) a))).PosDef :=
  actual_endpointHessian_residual_coefficientGram_posDef (by norm_num) 1 separated_2_1 e _

/-- Both actual separated endpoint marginal laws and positive covariances, every raw target. -/
theorem actual_two_endpoint_laws (t : Fin 6 → ℝ) (e : Fin 2) :
    (rawPinKernel (L:=2) (by norm_num) 1 t).map (fun ω => toLp 2 (endpointHessian 2 1 e ω)) =
      multivariateGaussian (toLp 2 (endpointHessianMean 2 1 e t)) (endpointHessianCovariance 2 1 e) ∧
    (endpointHessianCovariance 2 1 e).PosDef :=
  ⟨rawPinKernel_endpointHessian_eq_multivariateGaussian (by norm_num) 1 e t,
    endpointHessianCovariance_posDef (by norm_num) 1 separated_2_1 e⟩

/-- One actual kernel-a.e. event contains determinant nonzero at both endpoints. -/
theorem actual_two_endpoint_determinants (t : Fin 6 → ℝ) :
    ∀ᵐ ω ∂rawPinKernel (L:=2) (by norm_num) 1 t, ∀ e : Fin 2,
      let H := endpointHessian 2 1 e ω
      H 0*H 2-(H 1)^2 ≠ 0 :=
  rawPinKernel_ae_endpointHessian_det_ne_zero (by norm_num) 1 separated_2_1 t

/-- This zero-covariance finite Gaussian is Dirac0, not an actual source configuration. -/
theorem finite_zero_gaussian_dirac :
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin 3)) (0 : Matrix (Fin 3) (Fin 3) ℝ) =
      Measure.dirac 0 := by
  simp [multivariateGaussian]

/-- Dropping PosDef permits determinant-zero mass1 in the finite counterexample. -/
theorem finite_zero_gaussian_det_zero_mass :
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin 3)) (0 : Matrix (Fin 3) (Fin 3) ℝ)
      {H | H 0*H 2-(H 1)^2=0} = 1 := by
  rw [finite_zero_gaussian_dirac]
  simp

/-- Concrete counterexample backing the sole private-adapter PosDef-omission mutation. -/
theorem finite_PosDef_omission_counterexample :
    ¬ (∀ᵐ H ∂multivariateGaussian (0 : EuclideanSpace ℝ (Fin 3))
      (0 : Matrix (Fin 3) (Fin 3) ℝ), H 0*H 2-(H 1)^2 ≠ 0) := by
  rw [finite_zero_gaussian_dirac]
  simp

end EndpointHessianGaussianControls
