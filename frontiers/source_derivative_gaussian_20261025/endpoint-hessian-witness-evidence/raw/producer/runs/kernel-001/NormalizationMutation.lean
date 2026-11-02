import Controls

open I4SourceConfluentLimits I4SourceFinitePinKernel I4SourceFiniteTrig EndpointHessianControls

-- Sole mutation omits alpha^-1 but retains the actual claimed row6 pairing1.
example : finitePairing (rawDerivativeCoefficient 2 1 6) (toSource 2 unnormalizedPoly) = 1 := by
  simp only [scalar_normalization_counterexample]
