import SourceSmoothTopology
import WeightedCarrier
import Mathlib.Analysis.Normed.Lp.lpHolder

noncomputable section
open I4SourceSmoothTopology I4SourceSmoothParameterSpace
open scoped lp

local instance coherentBCFSemi (d k : ℕ) : SeminormedAddCommGroup (DerivativeBCF d k) :=
  (inferInstance : NormedAddCommGroup (DerivativeBCF d k)).toSeminormedAddCommGroup
local instance coherentBCFAdd (d k : ℕ) : AddCommMonoid (DerivativeBCF d k) :=
  (coherentBCFSemi d k).toAddCommMonoid
local instance coherentBCFModule (d k : ℕ) : Module ℝ (DerivativeBCF d k) :=
  (inferInstance : NormedSpace ℝ (DerivativeBCF d k)).toModule

#synth Norm (ℝ →L[ℝ] DerivativeBCF 2 0)
#synth Norm (SmoothParameter →L[ℝ] DerivativeBCF 2 0)
#synth Norm (SmoothParameter →L[ℝ] ((k : Fin 4) → DerivativeBCF 2 k))
#check (ContinuousLinearMap.opNorm (ContinuousLinearMap.id ℝ (DerivativeBCF 2 0)))
