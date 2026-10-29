import SourceSmoothParameterSpace
import SourcePinPreservingQuartic

noncomputable section
open I4SourceSmoothTopology I4SourceSmoothParameterSpace I4SourcePinPreservingQuartic
open BoundedContinuousFunction
open scoped Topology BigOperators

set_option autoImplicit false

namespace I4SourceSmoothParameterSpace

attribute [local instance] coherentBCFSemi coherentBCFAdd coherentBCFModule
attribute [local instance] coherentJetSemi coherentJetAdd coherentJetModule

/-- Coordinates of the covector in the fixed flat basis. -/
def coordinateGradientCLM : ((Fin 2 → ℝ) →L[ℝ] ℝ) →L[ℝ] (Fin 2 → ℝ) :=
  ContinuousLinearMap.pi (fun i => ContinuousLinearMap.apply ℝ ℝ (coordinateDirection i))

@[simp] theorem coordinateGradientCLM_apply (A : (Fin 2 → ℝ) →L[ℝ] ℝ) (i : Fin 2) :
    coordinateGradientCLM A i = A (coordinateDirection i) := rfl

/-- Contract the last derivative slot against the coordinate basis. -/
def gradientTensorContraction (k : ℕ) :
    DerivativeOperator 2 (k+1) →L[ℝ]
      ContinuousMultilinearMap ℝ (fun _ : Fin k => Fin 2 → ℝ) (Fin 2 → ℝ) :=
  (ContinuousLinearMap.compContinuousMultilinearMapL ℝ (fun _ : Fin k => Fin 2 → ℝ)
    ((Fin 2 → ℝ) →L[ℝ] ℝ) (Fin 2 → ℝ) coordinateGradientCLM).comp
    (continuousMultilinearCurryRightEquiv' ℝ k (Fin 2 → ℝ) ℝ).toContinuousLinearEquiv.toContinuousLinearMap

@[simp] theorem gradientTensorContraction_apply (k : ℕ)
    (A : DerivativeOperator 2 (k+1)) (u : Fin k → Fin 2 → ℝ) (i : Fin 2) :
    gradientTensorContraction k A u i = A (Fin.snoc u (coordinateDirection i)) := by
  simp [gradientTensorContraction, coordinateGradientCLM]

def parameterGradientTensorBCF {L : ℝ} (hL : L ≠ 0) (k : ℕ) (hk : k ≤ 2)
    (a : SmoothParameter) :=
  (gradientTensorContraction k).compLeftContinuousBounded (Fin 2 → ℝ)
    (parameterDerivativeCLM hL (k+1) (by omega) a)

theorem parameterGradientTensorBCF_continuous {L : ℝ} (hL : L ≠ 0)
    (k : ℕ) (hk : k ≤ 2) : Continuous (parameterGradientTensorBCF hL k hk) :=
  ((gradientTensorContraction k).compLeftContinuousBounded (Fin 2 → ℝ)).continuous.comp
    (parameterDerivativeCLM hL (k+1) (by omega)).continuous

theorem gradientPi_iteratedFDeriv {f : (Fin 2 → ℝ) → ℝ}
    (hf : ContDiff ℝ 5 f) (k : ℕ) (hk : k ≤ 2) (x : Fin 2 → ℝ)
    (u : Fin k → Fin 2 → ℝ) (i : Fin 2) :
    iteratedFDeriv ℝ k (gradientPi f) x u i =
      iteratedFDeriv ℝ (k+1) f x (Fin.snoc u (coordinateDirection i)) := by
  have hd : ContDiff ℝ 4 (fderiv ℝ f) := hf.fderiv_right (by norm_num)
  have heq : gradientPi f = coordinateGradientCLM ∘ fderiv ℝ f := rfl
  rw [heq, coordinateGradientCLM.iteratedFDeriv_comp_left hd.contDiffAt (by exact_mod_cast (show k ≤ 4 by omega))]
  change (iteratedFDeriv ℝ k (fderiv ℝ f) x u) (coordinateDirection i) = _
  rw [iteratedFDeriv_succ_apply_right]
  simp

theorem parameterGradientTensorBCF_apply {L : ℝ} (hL : L ≠ 0)
    (k : ℕ) (hk : k ≤ 2) (a : SmoothParameter) (x : Fin 2 → ℝ) :
    parameterGradientTensorBCF hL k hk a x =
      iteratedFDeriv ℝ k (gradientPi (weightedFourierField L (parameterWeight L) a)) x := by
  ext u i
  change gradientTensorContraction k (parameterDerivativeCLM hL (k+1) (by omega) a x) u i = _
  rw [gradientTensorContraction_apply, parameterDerivativeCLM_apply]
  exact (gradientPi_iteratedFDeriv
    (weightedFourierField_contDiff hL _ (parameterWeight_pos hL) (parameterWeight_dominates L) a)
    k hk x u i).symm

def parameterGradientBCF {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :=
  (ContinuousMultilinearMap.apply ℝ (fun _ : Fin 0 => Fin 2 → ℝ) (Fin 2 → ℝ)
    (fun j => Fin.elim0 j)).compLeftContinuousBounded (Fin 2 → ℝ)
    (parameterGradientTensorBCF hL 0 (by omega) a)

theorem parameterGradientBCF_continuous {L : ℝ} (hL : L ≠ 0) :
    Continuous (parameterGradientBCF hL) :=
  ((ContinuousMultilinearMap.apply ℝ (fun _ : Fin 0 => Fin 2 → ℝ) (Fin 2 → ℝ)
    (fun j => Fin.elim0 j)).compLeftContinuousBounded (Fin 2 → ℝ)).continuous.comp
      (parameterGradientTensorBCF_continuous hL 0 (by omega))

@[simp] theorem parameterGradientBCF_apply {L : ℝ} (hL : L ≠ 0)
    (a : SmoothParameter) (x : Fin 2 → ℝ) :
    parameterGradientBCF hL a x = gradientPi (weightedFourierField L (parameterWeight L) a) x := by
  change parameterGradientTensorBCF hL 0 (by omega) a x (fun j => Fin.elim0 j) = _
  rw [parameterGradientTensorBCF_apply, iteratedFDeriv_zero_apply]

def parameterGradientDerivativeBCF {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :=
  (continuousMultilinearCurryFin1 ℝ (Fin 2 → ℝ) (Fin 2 → ℝ)).toContinuousLinearEquiv.toContinuousLinearMap.compLeftContinuousBounded
    (Fin 2 → ℝ) (parameterGradientTensorBCF hL 1 (by omega) a)

theorem parameterGradientDerivativeBCF_continuous {L : ℝ} (hL : L ≠ 0) :
    Continuous (parameterGradientDerivativeBCF hL) :=
  ((continuousMultilinearCurryFin1 ℝ (Fin 2 → ℝ) (Fin 2 → ℝ)).toContinuousLinearEquiv.toContinuousLinearMap.compLeftContinuousBounded
    (Fin 2 → ℝ)).continuous.comp (parameterGradientTensorBCF_continuous hL 1 (by omega))

@[simp] theorem parameterGradientDerivativeBCF_apply {L : ℝ} (hL : L ≠ 0)
    (a : SmoothParameter) (x : Fin 2 → ℝ) :
    parameterGradientDerivativeBCF hL a x =
      fderiv ℝ (gradientPi (weightedFourierField L (parameterWeight L) a)) x := by
  ext v i
  change parameterGradientTensorBCF hL 1 (by omega) a x (Fin.snoc 0 v) i = _
  rw [parameterGradientTensorBCF_apply, iteratedFDeriv_one_apply]
  rfl

theorem parameterGradient_spatial_C2 {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :
    ContDiff ℝ 2 (gradientPi (weightedFourierField L (parameterWeight L) a)) := by
  have hf := weightedFourierField_contDiff hL _ (parameterWeight_pos hL) (parameterWeight_dominates L) a
  have hd : ContDiff ℝ 4 (fderiv ℝ (weightedFourierField L (parameterWeight L) a)) :=
    hf.fderiv_right (by norm_num)
  exact coordinateGradientCLM.contDiff.comp (hd.of_le (by norm_num))

/-- The physical Euclidean gradient is transported by the fixed continuous
linear equivalence, with its actual Euclidean norm retained. -/
def parameterGradientEuclideanBCF {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :=
  piToEuclidean.compLeftContinuousBounded (EuclideanSpace ℝ (Fin 2))
    ((parameterGradientBCF hL a).compContinuous ⟨euclideanToPi,euclideanToPi.continuous⟩)

theorem parameterGradientEuclideanBCF_continuous {L : ℝ} (hL : L ≠ 0) :
    Continuous (parameterGradientEuclideanBCF hL) :=
  (piToEuclidean.compLeftContinuousBounded (EuclideanSpace ℝ (Fin 2))).continuous.comp
    ((BoundedContinuousFunction.compContinuousCLM (Fin 2 → ℝ) ℝ
      ⟨euclideanToPi,euclideanToPi.continuous⟩).continuous.comp
        (parameterGradientBCF_continuous hL))

@[simp] theorem parameterGradientEuclideanBCF_apply {L : ℝ} (hL : L ≠ 0)
    (a : SmoothParameter) (z : EuclideanSpace ℝ (Fin 2)) :
    parameterGradientEuclideanBCF hL a z =
      gradientEuclidean (weightedFourierField L (parameterWeight L) a) z := by
  change piToEuclidean (parameterGradientBCF hL a (euclideanToPi z)) = _
  rw [parameterGradientBCF_apply]
  rfl

theorem parameterGradientEuclidean_spatial_C2 {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :
    ContDiff ℝ 2 (gradientEuclidean (weightedFourierField L (parameterWeight L) a)) :=
  piToEuclidean.contDiff.comp ((parameterGradient_spatial_C2 hL a).comp euclideanToPi.contDiff)

end I4SourceSmoothParameterSpace
