import Controls

open MeasureTheory RemoteJetGaussianControls

-- Sole mutation: omit m=1 from the claimed affine law; exact scalar adapter.
example : (Measure.dirac (0:ℝ)).map (fun z : ℝ => (0:ℝ)*z+1) =
    (Measure.dirac (0:ℝ)).map (fun z : ℝ => (0:ℝ)*z+0) := by
  simp only [finite_mean_omission_counterexample]
