import Controls

open I4SourceCompactTargetMoments

/-- Deliberate false mutation: nondefault k=1 cannot use the k=1/6 target. -/
theorem false_nondefault_target_normalization (r : ℝ) : sourceGapPins r 3 1 5 = 2 := by
  have counterexample := (GapPinCurvatureControls.nondefault_slot5 r).2
  norm_num [sourceGapPins]
