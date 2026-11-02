import SourceSmoothTopology
import WeightedCarrier
import Mathlib.Analysis.Normed.Lp.lpHolder

noncomputable section
open I4SourceSmoothTopology I4SourceSmoothParameterSpace
open scoped lp

attribute [-instance] BoundedContinuousFunction.instAddCommMonoid
attribute [-instance] BoundedContinuousFunction.instModule

#synth Norm (ℝ →L[ℝ] DerivativeBCF 2 0)
#synth Norm (SmoothParameter →L[ℝ] DerivativeBCF 2 0)
#synth Norm (SmoothParameter →L[ℝ] ((k : Fin 4) → DerivativeBCF 2 k))
#check (ContinuousLinearMap.opNorm (ContinuousLinearMap.id ℝ (DerivativeBCF 2 0)))
