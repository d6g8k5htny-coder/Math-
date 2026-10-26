import Controls

open I4SourceSmoothPalm I4SourceEndpointEstimates
open CompactGapNormalizerControls

/-- Deliberate false mutation: suppress the literal physical r-squared factor. -/
example : (1:ℝ) ≤ sourceEndpointWeight (1/4) ![-1,1,0,0,-1,-1] := by
  have counterexample := omitted_radius_square_counterexample
  rw [physical_unit_determinant_weight]
  norm_num
