import SourceGapPinCurvature
import SourceCurvatureDecomposition
import SourceGapWeightedNumerator

/-!
# Compact positive-gap actual physical normalizer

A bounded negative-curvature event and a first-moment truncation give a
uniform positive quadratic floor for the literal physical determinant weight.
The affine target mean and the actual source posterior carrier are retained.
This supplies a coarse floor, with no contact-limit or geometric pairing claim.
-/

noncomputable section

open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceDerivativeGaussian
open I4SourceConfluentPins I4SourceConfluentLimits I4SourceEndpointRegression
open I4SourceEndpointEstimates I4SourceSmoothConditional I4SourceConditionalMajorant
open I4SourcePinCurvatureBounds I4SourceSmoothPalm I4SourceCompactTargetMoments
open I4SourceGapPinCurvature I4SourceCurvatureDecomposition I4SourceContact I4ContactGram
open I4SourceGapWeightedNumerator MeasureTheory ProbabilityTheory Set Filter Matrix
open scoped BigOperators Topology NNReal

set_option autoImplicit false

namespace SourceCompactGapNormalizer

/-- The six-factor estimate uses the actual Pi norm, with the affine mean intact. -/
theorem sourceGap_curvatureMean_bound (L r b k B K J : ℝ)
    (hr : 0 ≤ r) (hr1 : r ≤ 1) (hB : 0 ≤ B) (hK : 0 ≤ K) (hJ : 0 ≤ J)
    (hb : |b| ≤ B) (hk : |k| ≤ K)
    (hβ : ∀ i, |curvatureBeta L r i| ≤ J) :
    |curvatureMean L r (sourceGapPins r b k)| ≤ 6*J*(B+13*K) := by
  have hp := (sourceGapPins_norm_le r b k K hr hr1 hK hk).trans
    (add_le_add_right hb (13*K))
  have hi (i : Fin 6) : |sourceGapPins r b k i| ≤ B+13*K :=
    (show |sourceGapPins r b k i| ≤ ‖sourceGapPins r b k‖ by
      simpa only [Real.norm_eq_abs] using norm_le_pi_norm (sourceGapPins r b k) i).trans hp
  calc
    _ ≤ ∑ i : Fin 6, |curvatureBeta L r i * sourceGapPins r b k i| :=
      Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ _i : Fin 6, J*(B+13*K) := by
      apply Finset.sum_le_sum
      intro i _
      rw [abs_mul]
      exact mul_le_mul (hβ i) (hi i) (abs_nonneg _) hJ
    _ = _ := by simp; ring

/-- The existing all-target reconstruction gives the actual curvature marginal. -/
theorem sourceGapLaw_q_hasLaw {L : ℝ} (hL : L ≠ 0) (r b k : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r) :
    HasLaw (sourceQ L)
      (curvatureScalarLaw L r (sourceGapPins r b k)) (sourceGapLaw hL r b k) := by
  refine ⟨(sourceContactQ_measurable hL).aemeasurable, ?_⟩
  change (sourceSmoothKernel hL r (sourceGapPins r b k)).map (sourceContactQ L) = _
  rw [sourceSmoothKernel_eq_curvatureProduct_swap hL r hG hτ,
    Measure.map_map (sourceContactQ_measurable hL)
      (curvatureReconstruct_swap_measurable hL r (sourceGapPins r b k))]
  have hcomp : (sourceContactQ L ∘ fun p : ℝ × SmoothSample 2 L =>
      curvatureReconstruct hL r (sourceGapPins r b k) p.2 p.1) = Prod.fst := by
    funext p
    exact curvatureReconstruct_Q hL r hτ _ _ _
  rw [hcomp, Measure.map_fst_prod, measure_univ, one_smul]
  rfl

/-- This event uses the original radius and does not assert independence. -/
def sourceCompactGoodEvent (L A : ℝ) : Set (SmoothSample 2 L) :=
  {ω | sourceQ L ω ∈ Icc (-2 : ℝ) (-1) ∧ sourceGammaRadius L ω ≤ A}

theorem sourceCompactGoodEvent_measurable {L : ℝ} (hL : L ≠ 0) (A : ℝ) :
    MeasurableSet (sourceCompactGoodEvent L A) :=
  ((sourceContactQ_measurable hL) measurableSet_Icc).inter
    (measurableSet_le (sourceGammaRadius_measurable L) measurable_const)

/-- First-moment tail subtraction preserves half of the curvature-event mass. -/
theorem sourceCompactGoodEvent_mass {L : ℝ} (Q : Measure (SmoothSample 2 L))
    [IsFiniteMeasure Q] (η H : ℝ) (hη : 0 < η) (hH : 0 ≤ H)
    (hΓ : Integrable (sourceGammaRadius L) Q)
    (hmoment : (∫ ω, sourceGammaRadius L ω ∂Q) ≤ H)
    (hq : η ≤ Q.real {ω | sourceQ L ω ∈ Icc (-2 : ℝ) (-1)}) :
    η/2 ≤ Q.real (sourceCompactGoodEvent L (max 1 (2*H/η))) := by
  let A := max 1 (2*H/η)
  have hA : 0 < A := lt_of_lt_of_le (by norm_num) (le_max_left _ _)
  have hAH : 2*H ≤ A*η := (div_le_iff₀ hη).mp (le_max_right _ _)
  have hMarkov := mul_meas_ge_le_integral_of_nonneg
    (Eventually.of_forall (sourceGammaRadius_nonneg L)) hΓ A
  have hbad : Q.real {ω | A < sourceGammaRadius L ω} ≤ η/2 := by
    have hsub : {ω | A < sourceGammaRadius L ω} ⊆
        {ω | A ≤ sourceGammaRadius L ω} := fun _ h => h.le
    have htail := mul_le_mul_of_nonneg_left (measureReal_mono hsub) hA.le
    have hbound := htail.trans (hMarkov.trans hmoment)
    nlinarith
  have hsubtract := le_measureReal_sdiff (μ := Q)
    (s₁ := {ω | sourceQ L ω ∈ Icc (-2 : ℝ) (-1)})
    (s₂ := {ω | A < sourceGammaRadius L ω})
  have heq : {ω | sourceQ L ω ∈ Icc (-2 : ℝ) (-1)} \
      {ω | A < sourceGammaRadius L ω} = sourceCompactGoodEvent L A := by
    ext ω
    simp only [mem_sdiff, mem_setOf_eq, not_lt, sourceCompactGoodEvent]
  rw [heq] at hsubtract
  dsimp only [A] at hsubtract
  linarith

end SourceCompactGapNormalizer
