import SourceCurvatureDecomposition

noncomputable section
open I4Source I4SmoothCarrier I4SourceContact I4SourceEndpointRegression
open I4SourceSmoothConditional I4SourceCurvatureDecomposition
open MeasureTheory ProbabilityTheory Filter Set
open scoped Topology

set_option autoImplicit false

namespace I4CurvatureDecompositionControls

/-- A smooth sample outside the residual support does not have the regression
mean as its posterior curvature. This rejects the false all-residual premise. -/
theorem arbitrary_residual_can_change_posterior_curvature {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r)
    (x : Fin 6 → ℝ) :
    sourceContactQ L (posteriorSample hL r x
      (curvatureShift hL r 1 (curvatureResidualSample hL r (zeroSample 2 L)))) ≠
        curvatureMean L r x := by
  rw [sourceContactQ_posteriorSample_Z hL r hτ,
    curvatureZ_curvatureShift hL r 1 hG hτ,
    curvatureResidualSample_Z hL r hG hτ]
  simp only [zero_add, mul_one]
  have hσ := curvatureSigma_pos hτ
  linarith

/-- Reconstruction succeeds even on that sample, and for an arbitrary target
curvature. It does not depend on an unsupported all-residual mean identity. -/
example {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r)
    (x : Fin 6 → ℝ) (t : ℝ) :
    sourceContactQ L (curvatureReconstruct hL r x
      (curvatureShift hL r 1 (curvatureResidualSample hL r (zeroSample 2 L))) t) = t :=
  curvatureReconstruct_Q hL r hτ x _ t

/-- The product law is the actual full-carrier kernel at arbitrary pins. -/
example {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r)
    (x : Fin 6 → ℝ) :
    HasLaw (fun p : ℝ × SmoothSample 2 L => curvatureReconstruct hL r x p.2 p.1)
      (sourceSmoothKernel hL r x) ((curvatureScalarLaw L r x).prod (curvatureResidualLaw hL r)) :=
  curvatureReconstruct_hasLaw hL r hG hτ x

/-- Zero Gaussian variance is an atom and cannot obey a bounded interval
density estimate. The strictly positive actual Schur floor is necessary. -/
theorem zero_variance_rejects_density_bound (D : ℝ) :
    ¬ ((gaussianReal 0 0).real (Icc (0 : ℝ) 0) ≤ 2*D*0) := by
  simp [gaussianReal_zero_var]

/-- The actual source supplies the eventual product law with no covariance
or Gaussian-law premise. -/
example {L : ℝ} (hL : L ≠ 0) :
    ∀ᶠ r in 𝓝[>] (0 : ℝ), ∀ x : Fin 6 → ℝ,
      HasLaw (fun p : ℝ × SmoothSample 2 L => curvatureReconstruct hL r x p.2 p.1)
        (sourceSmoothKernel hL r x) ((curvatureScalarLaw L r x).prod (curvatureResidualLaw hL r)) :=
  sourceSmoothKernel_eventually_curvatureProduct hL

end I4CurvatureDecompositionControls
