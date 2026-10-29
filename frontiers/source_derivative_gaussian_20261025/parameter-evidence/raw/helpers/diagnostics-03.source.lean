import SourceSmoothTopology
import WeightedCarrier
import Mathlib.Analysis.Normed.Lp.lpHolder

noncomputable section
open I4SourceSmoothTopology I4SourceSmoothParameterSpace
open scoped lp

#synth SeminormedAddCommGroup SmoothParameter
#synth NormedSpace ℝ SmoothParameter
#synth SeminormedAddCommGroup (DerivativeBCF 2 0)
#synth NormedSpace ℝ (DerivativeBCF 2 0)
#synth Norm (SmoothParameter →L[ℝ] ℝ)
#synth Norm (ℝ →L[ℝ] DerivativeBCF 2 0)
#synth Norm (ℝ →L[ℝ] ℝ)

set_option backward.isDefEq.respectTransparency false in
#synth Norm (SmoothParameter →L[ℝ] DerivativeBCF 2 0)

#check ContinuousLinearMap.opNorm
#check @ContinuousLinearMap.hasOpNorm
#check (ContinuousLinearMap.opNorm (ContinuousLinearMap.id ℝ SmoothParameter))
#check (ContinuousLinearMap.opNorm (ContinuousLinearMap.id ℝ (DerivativeBCF 2 0)))
