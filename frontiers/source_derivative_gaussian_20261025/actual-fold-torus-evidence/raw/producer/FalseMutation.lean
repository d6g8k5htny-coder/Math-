import ActualTorusControls

open I4Torus ActualTorusControls

/-- Deliberately treat the global quotient projection as injective, collapsing
the two proved-distinct real lifts whose quotient images are equal. The already
proved noninjectivity rewrites this false obligation to the sole goal False. -/
theorem false_global_quotient_injection : False := by
  have wrong_injection : Function.Injective (torusProjection 2 (-1)) := by
    simp only [negative_period_projection_not_injective]
  exact negative_period_collapsed_lifts_counterexample
    (wrong_injection negative_period_lifts_same)
