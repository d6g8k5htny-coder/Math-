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

local instance coherentJetSemi (K : ℕ) :
    SeminormedAddCommGroup ((k : Fin (K+1)) → DerivativeBCF 2 k) :=
  (inferInstance : NormedAddCommGroup ((k : Fin (K+1)) → DerivativeBCF 2 k)).toSeminormedAddCommGroup
local instance coherentJetAdd (K : ℕ) :
    AddCommMonoid ((k : Fin (K+1)) → DerivativeBCF 2 k) :=
  (coherentJetSemi K).toAddCommMonoid
local instance coherentJetModule (K : ℕ) :
    Module ℝ ((k : Fin (K+1)) → DerivativeBCF 2 k) :=
  (inferInstance : NormedSpace ℝ ((k : Fin (K+1)) → DerivativeBCF 2 k)).toModule

#synth Norm (ℝ →L[ℝ] DerivativeBCF 2 0)
#synth Norm (SmoothParameter →L[ℝ] DerivativeBCF 2 0)
#synth Norm (SmoothParameter →L[ℝ] ((k : Fin 4) → DerivativeBCF 2 k))
#check (ContinuousLinearMap.opNorm (ContinuousLinearMap.id ℝ (DerivativeBCF 2 0)))
