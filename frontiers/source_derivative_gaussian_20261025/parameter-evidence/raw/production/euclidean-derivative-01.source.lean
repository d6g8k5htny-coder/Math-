import SourceSmoothParameterSpace

noncomputable section
open I4SourceSmoothTopology I4SourcePinPreservingQuartic BoundedContinuousFunction
open scoped Topology

set_option autoImplicit false

namespace I4SourceSmoothParameterSpace

/-- Fixed continuous transport of derivatives from Pi to Euclidean coordinates. -/
def euclideanDerivativeContraction :
    ((Fin 2 → ℝ) →L[ℝ] (Fin 2 → ℝ)) →L[ℝ]
      (EuclideanSpace ℝ (Fin 2) →L[ℝ] EuclideanSpace ℝ (Fin 2)) :=
  (ContinuousLinearMap.compL ℝ (EuclideanSpace ℝ (Fin 2)) (Fin 2 → ℝ)
    (EuclideanSpace ℝ (Fin 2)) piToEuclidean).comp
    ((ContinuousLinearMap.compL ℝ (EuclideanSpace ℝ (Fin 2)) (Fin 2 → ℝ)
      (Fin 2 → ℝ)).flip euclideanToPi)

@[simp] theorem euclideanDerivativeContraction_apply
    (D : (Fin 2 → ℝ) →L[ℝ] (Fin 2 → ℝ)) :
    euclideanDerivativeContraction D = piToEuclidean.comp (D.comp euclideanToPi) := rfl

def parameterGradientEuclideanDerivativeBCF {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :=
  euclideanDerivativeContraction.compLeftContinuousBounded (EuclideanSpace ℝ (Fin 2))
    ((parameterGradientDerivativeBCF hL a).compContinuous ⟨euclideanToPi,euclideanToPi.continuous⟩)

theorem parameterGradientEuclideanDerivativeBCF_continuous {L : ℝ} (hL : L ≠ 0) :
    Continuous (parameterGradientEuclideanDerivativeBCF hL) :=
  (euclideanDerivativeContraction.compLeftContinuousBounded (EuclideanSpace ℝ (Fin 2))).continuous.comp
    ((BoundedContinuousFunction.compContinuousCLM ((Fin 2 → ℝ) →L[ℝ] (Fin 2 → ℝ)) ℝ
      ⟨euclideanToPi,euclideanToPi.continuous⟩).continuous.comp
        (parameterGradientDerivativeBCF_continuous hL))

@[simp] theorem parameterGradientEuclideanDerivativeBCF_apply {L : ℝ} (hL : L ≠ 0)
    (a : SmoothParameter) (z : EuclideanSpace ℝ (Fin 2)) :
    parameterGradientEuclideanDerivativeBCF hL a z =
      fderiv ℝ (gradientEuclidean (weightedFourierField L (parameterWeight L) a)) z := by
  change piToEuclidean.comp
    ((parameterGradientDerivativeBCF hL a (euclideanToPi z)).comp euclideanToPi) = _
  rw [parameterGradientDerivativeBCF_apply]
  have hraw := ((parameterGradient_spatial_C2 hL a).differentiable (by norm_num)
    (euclideanToPi z)).hasFDerivAt
  have hE := piToEuclidean.hasFDerivAt.comp z
    (hraw.comp z euclideanToPi.hasFDerivAt)
  exact hE.fderiv.symm

end I4SourceSmoothParameterSpace
