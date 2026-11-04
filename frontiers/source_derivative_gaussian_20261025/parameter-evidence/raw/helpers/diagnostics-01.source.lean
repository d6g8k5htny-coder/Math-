import SourceSmoothTopology
import WeightedCarrier
import Mathlib.Analysis.Normed.Lp.lpHolder

noncomputable section
open I4SourceSmoothTopology I4SourceSmoothParameterSpace
open scoped lp

#synth NormedSpace ℝ SmoothParameter
#synth NormedAddCommGroup SmoothParameter
#synth Module ℝ SmoothParameter
#synth NormedSpace ℝ (DerivativeBCF 2 0)
#synth NormedAddCommGroup (DerivativeBCF 2 0)
#synth Module ℝ (DerivativeBCF 2 0)
#synth Norm (SmoothParameter →L[ℝ] DerivativeBCF 2 0)
#synth Norm ((DerivativeBCF 2 0) →L[ℝ] SmoothParameter)
#synth NormedSpace ℝ ((k : Fin 4) → DerivativeBCF 2 k)
#synth Norm (SmoothParameter →L[ℝ] ((k : Fin 4) → DerivativeBCF 2 k))

variable (k : ℕ)
#synth NormedSpace ℝ (DerivativeBCF 2 k)
#synth NormedAddCommGroup (DerivativeBCF 2 k)
#synth Norm (SmoothParameter →L[ℝ] DerivativeBCF 2 k)
