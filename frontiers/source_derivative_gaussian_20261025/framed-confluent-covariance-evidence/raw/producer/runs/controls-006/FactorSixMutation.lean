import Controls
open I4SourceFinitePinKernel FramedConfluentControls

-- Sole mutation: row5 omits its literal factor6, while its contact pairing is claimed1.
-- Passed Controls proves this very original finite-source pairing is1/6.
example : finitePairing omittedFactorRow finiteDirection = (1:ℝ) := by
  rw [omitted_pairing_sixth]
  norm_num
