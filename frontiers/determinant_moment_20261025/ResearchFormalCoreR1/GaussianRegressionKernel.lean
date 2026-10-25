import Mathlib.Probability.HasCondDistrib
import Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Independence

/-!
# Canonical Gaussian regression kernel

For a residual law `ν`, `regressionKernel ν B mX mY x` is the literal affine pushforward
`ν.map (fun r => r + mY + B (x - mX))` at every observation `x`. The kernel is constructed
measurably from a deterministic observation and a constant residual kernel, so it has a
specified value even where the observation has probability zero.

The Gaussian theorem derives observation/residual independence from joint Gaussianity and
zero coordinate cross-covariance. No nondegeneracy or residual covariance inverse is needed.
This generic construction does not identify concrete derivative observations, regression or
Schur covariance blocks, a Palm weight, or a conditional law of a literal smooth field.

Source contract: `SOURCE_REGRESSION_KERNEL.md` in this packet. Author-side Lean verification
is separate from source alignment and the required review by another model family.
-/

open MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory

set_option autoImplicit false

namespace ResearchFormalCoreR1

/-- Copying the first coordinate and retaining an independent second coordinate. -/
lemma regression_compProd_id_const {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    (μ : Measure α) (ν : Measure β) [SFinite μ] [SFinite ν] :
    μ ⊗ₘ (Kernel.id ×ₖ Kernel.const α ν) =
      (μ.prod ν).map (fun p : α × β => (p.1, p)) := by
  ext s hs
  rw [Measure.compProd_apply hs, Measure.map_apply (by fun_prop) hs,
    Measure.prod_apply (s := (fun p : α × β => (p.1, p)) ⁻¹' s) (hs.preimage (by fun_prop))]
  simp_rw [Kernel.prod_apply, Kernel.id_apply, Kernel.const_apply, Measure.dirac_prod]
  congr with x
  rw [Measure.map_apply (by fun_prop) (measurable_prodMk_left hs)]
  rfl

/-- An independent residual paired with the observation has the explicit product kernel. -/
lemma regression_pair_hasCondDistrib {Ω α β : Type*} [MeasurableSpace Ω]
    [MeasurableSpace α] [MeasurableSpace β] {P : Measure Ω} [IsProbabilityMeasure P]
    {X : Ω → α} {R : Ω → β} (hX : AEMeasurable X P) (hR : AEMeasurable R P)
    (hXR : IndepFun X R P) :
    HasCondDistrib (fun ω => (X ω, R ω)) X
      (Kernel.id ×ₖ Kernel.const α (P.map R)) P := by
  refine ⟨hX.prodMk (hX.prodMk hR), ?_⟩
  calc
    P.map (fun ω => (X ω, (X ω, R ω))) =
        (P.map (fun ω => (X ω, R ω))).map (fun p : α × β => (p.1, p)) := by
      rw [AEMeasurable.map_map_of_aemeasurable (by fun_prop) (hX.prodMk hR)]
      rfl
    _ = ((P.map X).prod (P.map R)).map (fun p : α × β => (p.1, p)) := by
      rw [hXR.map_prod_eq_prod_map_map hX hR]
    _ = (P.map X) ⊗ₘ (Kernel.id ×ₖ Kernel.const α (P.map R)) :=
      (regression_compProd_id_const (P.map X) (P.map R)).symm


/-- Affine reconstruction of the target from the observation and the regression residual. -/
def regressionReconstruction {n k : ℕ}
    (B : (Fin n → ℝ) →L[ℝ] (Fin k → ℝ)) (mX : Fin n → ℝ) (mY : Fin k → ℝ)
    (p : (Fin n → ℝ) × (Fin k → ℝ)) : Fin k → ℝ :=
  p.2 + mY + B (p.1 - mX)

lemma regressionReconstruction_measurable {n k : ℕ}
    (B : (Fin n → ℝ) →L[ℝ] (Fin k → ℝ)) (mX : Fin n → ℝ) (mY : Fin k → ℝ) :
    Measurable (regressionReconstruction B mX mY) := by
  unfold regressionReconstruction
  fun_prop

/-- The canonical regression law is specified at every observation, including null pins. -/
noncomputable def regressionKernel {n k : ℕ} (ν : Measure (Fin k → ℝ))
    (B : (Fin n → ℝ) →L[ℝ] (Fin k → ℝ)) (mX : Fin n → ℝ) (mY : Fin k → ℝ) :
    Kernel (Fin n → ℝ) (Fin k → ℝ) :=
  ((Kernel.id : Kernel (Fin n → ℝ) (Fin n → ℝ)) ×ₖ
    Kernel.const (Fin n → ℝ) ν).map (regressionReconstruction B mX mY)

instance regressionKernel_isMarkov {n k : ℕ} (ν : Measure (Fin k → ℝ))
    [IsProbabilityMeasure ν] (B : (Fin n → ℝ) →L[ℝ] (Fin k → ℝ))
    (mX : Fin n → ℝ) (mY : Fin k → ℝ) :
    IsMarkovKernel (regressionKernel ν B mX mY) := by
  unfold regressionKernel
  exact Kernel.IsMarkovKernel.map _ (regressionReconstruction_measurable B mX mY)

lemma regressionKernel_apply {n k : ℕ} (ν : Measure (Fin k → ℝ)) [SFinite ν]
    (B : (Fin n → ℝ) →L[ℝ] (Fin k → ℝ)) (mX : Fin n → ℝ) (mY : Fin k → ℝ)
    (x : Fin n → ℝ) :
    regressionKernel ν B mX mY x = ν.map (fun r => r + mY + B (x - mX)) := by
  rw [regressionKernel, Kernel.map_apply _ (regressionReconstruction_measurable B mX mY),
    Kernel.prod_apply, Kernel.id_apply, Kernel.const_apply, Measure.dirac_prod,
    Measure.map_map (regressionReconstruction_measurable B mX mY) (by fun_prop)]
  rfl

/-- Affine reconstruction from an independent residual has the canonical conditional kernel. -/
lemma independentResidual_hasCondDistrib {Ω : Type*} [MeasurableSpace Ω]
    {P : Measure Ω} [IsProbabilityMeasure P] {n k : ℕ}
    {X : Ω → Fin n → ℝ} {R : Ω → Fin k → ℝ}
    (hX : AEMeasurable X P) (hR : AEMeasurable R P) (hXR : IndepFun X R P)
    (B : (Fin n → ℝ) →L[ℝ] (Fin k → ℝ)) (mX : Fin n → ℝ) (mY : Fin k → ℝ) :
    HasCondDistrib (fun ω => R ω + mY + B (X ω - mX)) X
      (regressionKernel (P.map R) B mX mY) P := by
  exact (regression_pair_hasCondDistrib hX hR hXR).comp_left
    (regressionReconstruction_measurable B mX mY)

/-- Joint Gaussianity and vanishing observation/residual cross-covariance give the canonical
conditional law, without choosing an almost-everywhere version at a prescribed observation. -/
theorem gaussianRegression_hasCondDistrib {Ω : Type*} [MeasurableSpace Ω]
    {P : Measure Ω} {n k : ℕ} {X : Ω → Fin n → ℝ} {R : Ω → Fin k → ℝ}
    (hXR : HasGaussianLaw (fun ω => (X ω, R ω)) P)
    (hzero : ∀ i j, covariance (fun ω => X ω i) (fun ω => R ω j) P = 0)
    (B : (Fin n → ℝ) →L[ℝ] (Fin k → ℝ)) (mX : Fin n → ℝ) (mY : Fin k → ℝ) :
    HasCondDistrib (fun ω => R ω + mY + B (X ω - mX)) X
      (regressionKernel (P.map R) B mX mY) P := by
  have : IsProbabilityMeasure P := hXR.isProbabilityMeasure
  exact independentResidual_hasCondDistrib hXR.fst.aemeasurable hXR.snd.aemeasurable
    (hXR.indepFun_of_covariance_eval hzero) B mX mY

/-- Kernel measurability is pointwise in the observation and does not require a Gaussian law. -/
lemma regressionKernel_measurable {n k : ℕ} (ν : Measure (Fin k → ℝ))
    (B : (Fin n → ℝ) →L[ℝ] (Fin k → ℝ)) (mX : Fin n → ℝ) (mY : Fin k → ℝ) :
    Measurable (regressionKernel ν B mX mY) :=
  Kernel.measurable _

/-- All parts of the canonical Gaussian conditional-law construction, including the literal
pushforward at every prescribed observation. Zero-dimensional and degenerate laws are allowed. -/
theorem gaussianRegressionKernel_spec {Ω : Type*} [MeasurableSpace Ω]
    {P : Measure Ω} {n k : ℕ} {X : Ω → Fin n → ℝ} {R : Ω → Fin k → ℝ}
    (hXR : HasGaussianLaw (fun ω => (X ω, R ω)) P)
    (hzero : ∀ i j, covariance (fun ω => X ω i) (fun ω => R ω j) P = 0)
    (B : (Fin n → ℝ) →L[ℝ] (Fin k → ℝ)) (mX : Fin n → ℝ) (mY : Fin k → ℝ) :
    IsMarkovKernel (regressionKernel (P.map R) B mX mY) ∧
      Measurable (regressionKernel (P.map R) B mX mY) ∧
      (∀ x, regressionKernel (P.map R) B mX mY x =
        (P.map R).map (fun r => r + mY + B (x - mX))) ∧
      HasCondDistrib (fun ω => R ω + mY + B (X ω - mX)) X
        (regressionKernel (P.map R) B mX mY) P := by
  have : IsProbabilityMeasure P := hXR.isProbabilityMeasure
  exact ⟨inferInstance, regressionKernel_measurable _ B mX mY,
    regressionKernel_apply _ B mX mY, gaussianRegression_hasCondDistrib hXR hzero B mX mY⟩

end ResearchFormalCoreR1
