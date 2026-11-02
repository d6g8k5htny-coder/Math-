import Controls
open MeasureTheory ProbabilityTheory WithLp I4SourceRawPinConditioning
open I4SourceTwoRemoteFirstJetGaussian TwoRemoteFirstJetGaussianControls
noncomputable section
-- Sole mutation: actual equal-point sampling law with only cross3x3 blocks deleted.
example : (rawPinKernel (L:=2) (by norm_num) 0 0).map
    (fun ω => toLp 2 (twoRemoteFirstJet 2 ![1,0] ![1,0] ω)) =
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin 6)) zeroCrossCandidate := by
  simp only [actual_zero_cross_mutation_false]
