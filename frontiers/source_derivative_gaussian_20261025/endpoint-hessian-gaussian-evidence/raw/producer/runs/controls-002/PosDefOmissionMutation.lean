import Controls

open MeasureTheory ProbabilityTheory EndpointHessianGaussianControls

-- Sole mutation: drop PosDef from finiteGaussian3 determinant nonnullness.
-- Mean0/covariance0 is finite Dirac0, explicitly not an actual source parameter.
example : ∀ᵐ H ∂multivariateGaussian (0 : EuclideanSpace ℝ (Fin 3))
    (0 : Matrix (Fin 3) (Fin 3) ℝ), H 0*H 2-(H 1)^2 ≠ 0 := by
  simp only [finite_PosDef_omission_counterexample]
