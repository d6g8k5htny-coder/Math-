import SourceRawPinConditioning

open I4SmoothCarrier I4SourceConfluentPins

-- The two literal raw height observations coincide at the excluded zero radius.
example (ω : SmoothSample 2 1) : rawPins 1 0 ω 0 ≠ rawPins 1 0 ω 1 := by
  simp [rawPins, endpointM, endpointS]
